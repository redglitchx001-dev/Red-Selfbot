# -*- coding: utf-8 -*-
"""
RED SELFBOT V1 - Admin Panel server (stdlib only, no discord/requests needed).

Serves the ADMIN panel (admin.html) on 0.0.0.0:3000.
The public token page (panel.html) is meant to be hosted elsewhere; it is
also available at /public here for local testing.

REST API (used by both pages):
    POST /api/login          {name, token}              -> register/connect account
    POST /api/admin/verify   {key}                      -> unlock admin panel
    GET  /api/users                                     -> list all users (admin)
    POST /api/user           {name, action}             -> suspend/unsuspend/ban/unban/delete/check
    POST /api/check                                     -> re-check every token (background)
    GET  /api/blacklist                                 -> list blacklisted commands (admin)
    POST /api/blacklist      {cmd}                      -> add blacklisted command
    DELETE /api/blacklist    {cmd}                      -> remove blacklisted command
    GET  /api/people                                      -> list people / suggestions (admin)
    POST /api/people       {name, tag, note}            -> add a person + note (admin)
    DELETE /api/people     {id}                         -> remove a person (admin)
    GET  /api/status                                    -> bot status (public, no secrets)
    GET  /health                                        -> liveness probe

Run standalone:  python panel.py      (defaults to 0.0.0.0:3000)
Or it is imported by main.py so the selfbot serves the same panel.
"""
import os, json, time, threading, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
ADMIN_HTML = os.path.join(BASE, "admin.html")   # full admin UI (localhost:3000)
PUBLIC_HTML = os.path.join(BASE, "panel.html")  # public token page (hosted elsewhere)
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BLACKLIST_FILE = os.path.join(DATA_DIR, "blacklist.json")
PEOPLE_FILE = os.path.join(DATA_DIR, "people.json")

ADMIN_KEY = os.environ.get("ADMIN_KEY", "red2026")
START_TIME = time.time()
os.makedirs(DATA_DIR, exist_ok=True)

# Provider injected by main.py so the panel can show live bot stats.
META_PROVIDER = None

_lock = threading.Lock()
_checking = {"busy": False}


# ============================== STORAGE ==============================
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def load_users():
    return load_json(USERS_FILE, {})


def save_users(u):
    with _lock:
        save_json(USERS_FILE, u)


def load_blacklist():
    return load_json(BLACKLIST_FILE, [])


def save_blacklist(b):
    with _lock:
        save_json(BLACKLIST_FILE, b)


# --------------------------- people / suggestions ---------------------------
def load_people():
    return load_json(PEOPLE_FILE, [])


def save_people(p):
    with _lock:
        save_json(PEOPLE_FILE, p)


def add_person(name, tag, note):
    people = load_people()
    entry = {
        "id": "p%d" % (time.time() * 1000) + str(len(people)),
        "name": (name or "").strip(),
        "tag": (tag or "").strip(),
        "note": (note or "").strip(),
        "added_at": int(time.time()),
    }
    people.append(entry)
    save_people(people)
    return entry


def remove_person(pid):
    people = load_people()
    out = [p for p in people if p.get("id") != pid]
    if len(out) == len(people):
        return False, people
    save_people(out)
    return True, out


# ============================== TOKEN CHECK ==============================
def check_token(token):
    """
    Validate a Discord user token against the gateway API.
    Returns {"valid": True|False|None, "user": {...}|None, "error": str|None, "code": int}
    valid=True -> works, valid=False -> expired/invalid, valid=None -> unknown (offline etc).
    """
    token = (token or "").strip().strip('"').strip("'")
    if not token:
        return {"valid": False, "error": "empty token", "code": 0}
    req = urllib.request.Request(
        "https://discord.com/api/v10/users/@me",
        headers={"Authorization": token, "User-Agent": "Mozilla/5.0 (RedSelfbot Panel)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
        return {"valid": True, "user": data, "error": None, "code": 200}
    except urllib.error.HTTPError as e:
        code = e.code
        if code == 401:
            return {"valid": False, "error": "expired / invalid (401)", "code": code}
        if code == 403:
            return {"valid": False, "error": "account flagged / blocked (403)", "code": code}
        if code == 429:
            return {"valid": None, "error": "rate limit (429)", "code": code}
        return {"valid": False, "error": "HTTP %s" % code, "code": code}
    except Exception as e:
        return {"valid": None, "error": str(e)[:120], "code": -1}


def _apply_check_result(entry, res):
    entry["valid"] = res.get("valid")
    entry["last_check"] = int(time.time())
    entry["last_error"] = res.get("error")
    if res.get("user"):
        u = res["user"]
        entry["id"] = u.get("id")
        entry["username"] = u.get("username")
        entry["global_name"] = u.get("global_name")
        entry["discriminator"] = u.get("discriminator")
        entry["avatar"] = u.get("avatar")
        entry["premium_type"] = u.get("premium_type", 0)


def normalize_name(name):
    return (name or "").strip().lower()


def user_payload(key, entry):
    return {
        "name": entry.get("name") or key,
        "token": entry.get("token", ""),
        "id": entry.get("id"),
        "username": entry.get("username"),
        "global_name": entry.get("global_name"),
        "discriminator": entry.get("discriminator"),
        "avatar": entry.get("avatar"),
        "premium_type": entry.get("premium_type", 0),
        "valid": entry.get("valid"),
        "status": entry.get("status", "active"),
        "added_at": entry.get("added_at"),
        "last_check": entry.get("last_check"),
        "last_error": entry.get("last_error"),
    }


def add_or_update_user(name, token):
    users = load_users()
    key = normalize_name(name)
    entry = users.get(key, {})
    entry["name"] = (name or "").strip() or key
    entry["token"] = token
    entry["status"] = entry.get("status", "active")
    entry["added_at"] = entry.get("added_at", int(time.time()))
    res = check_token(token)
    _apply_check_result(entry, res)
    users[key] = entry
    save_users(users)
    return user_payload(key, entry)


def list_users_sorted():
    users = load_users()
    out = [user_payload(k, v) for k, v in users.items()]
    out.sort(key=lambda u: (u["status"] != "banned", u["status"] != "suspended", u["name"].lower()))
    return out


def check_all_async():
    """Re-check every stored token in a background thread. Returns True if started."""
    if _checking["busy"]:
        return False
    _checking["busy"] = True

    def work():
        try:
            users = load_users()
            for key, entry in users.items():
                res = check_token(entry.get("token", ""))
                _apply_check_result(entry, res)
                save_users(users)  # live progress so the UI can poll
        finally:
            _checking["busy"] = False

    threading.Thread(target=work, daemon=True).start()
    return True


# ============================== HTTP HANDLER ==============================
class PanelHandler(BaseHTTPRequestHandler):
    server_version = "RedSelfbotPanel/1.0"

    def _send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        # Allow any host / preview - critical for arena preview + localhost
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def _body_json(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n <= 0:
                return {}
            raw = self.rfile.read(n).decode("utf-8", "replace")
            return json.loads(raw) if raw else {}
        except Exception:
            return {}

    def _is_admin(self):
        return self.headers.get("X-Admin-Key", "") == ADMIN_KEY

    def _require_admin(self):
        if not self._is_admin():
            self._json({"ok": False, "error": "admin key invalid"}, 401)
            return False
        return True

    def log_message(self, *a):
        pass

    # ---------------------------- GET ----------------------------
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/status":
            return self.api_status()
        if p == "/health":
            return self._send(200, b"OK", "text/plain")
        if p == "/favicon.ico":
            return self._send(204)
        if p == "/api/users":
            if not self._require_admin():
                return
            users = list_users_sorted()
            return self._json({"ok": True, "users": users, "checking": _checking["busy"]})
        if p == "/api/blacklist":
            if not self._require_admin():
                return
            return self._json({"ok": True, "blacklist": load_blacklist()})
        if p == "/api/people":
            if not self._require_admin():
                return
            return self._json({"ok": True, "people": load_people()})
        # pages: / -> admin panel (admin.html), /public -> public token page
        if p in ("/public", "/public.html", "/panel.html"):
            path, missing = PUBLIC_HTML, "panel.html"
        else:
            path, missing = ADMIN_HTML, "admin.html"
        try:
            with open(path, "rb") as f:
                body = f.read()
        except Exception:
            body = ("<h1>%s missing</h1>" % missing).encode("utf-8")
        self._send(200, body, "text/html; charset=utf-8")

    # ---------------------------- POST ----------------------------
    def do_POST(self):
        p = urlparse(self.path).path
        data = self._body_json()

        if p == "/api/login":
            name = (data.get("name") or "").strip()
            token = (data.get("token") or "").strip().strip('"').strip("'")
            if not name:
                return self._json({"ok": False, "error": "no name given"}, 400)
            if not token:
                return self._json({"ok": False, "error": "no token given"}, 400)
            u = add_or_update_user(name, token)
            u["token"] = _mask(u["token"])
            return self._json({"ok": True, "user": u})

        if p == "/api/admin/verify":
            if data.get("key") == ADMIN_KEY:
                return self._json({"ok": True})
            return self._json({"ok": False, "error": "wrong admin key"}, 401)

        if p == "/api/user":
            if not self._require_admin():
                return
            return self.api_user_action(data)

        if p == "/api/check":
            if not self._require_admin():
                return
            started = check_all_async()
            return self._json({"ok": started, "started": started,
                               "error": None if started else "check already running"})

        if p == "/api/blacklist":
            if not self._require_admin():
                return
            cmd = (data.get("cmd") or "").strip().lower().lstrip("$")
            if not cmd:
                return self._json({"ok": False, "error": "no command given"}, 400)
            bl = load_blacklist()
            if cmd not in bl:
                bl.append(cmd)
                save_blacklist(bl)
            return self._json({"ok": True, "blacklist": bl})

        if p == "/api/people":
            if not self._require_admin():
                return
            name = (data.get("name") or "").strip()
            if not name:
                return self._json({"ok": False, "error": "no name given"}, 400)
            entry = add_person(name, data.get("tag", ""), data.get("note", ""))
            return self._json({"ok": True, "person": entry, "people": load_people()})

        return self._json({"ok": False, "error": "unknown route"}, 404)

    # ---------------------------- DELETE ----------------------------
    def do_DELETE(self):
        p = urlparse(self.path).path
        data = self._body_json()
        if p == "/api/blacklist":
            if not self._require_admin():
                return
            cmd = (data.get("cmd") or "").strip().lower().lstrip("$")
            bl = [c for c in load_blacklist() if c != cmd]
            save_blacklist(bl)
            return self._json({"ok": True, "blacklist": bl})
        if p == "/api/people":
            if not self._require_admin():
                return
            ok, people = remove_person((data.get("id") or "").strip())
            if not ok:
                return self._json({"ok": False, "error": "person not found"}, 404)
            return self._json({"ok": True, "people": people})
        return self._json({"ok": False, "error": "unknown route"}, 404)

    def do_OPTIONS(self):
        self._send(200)

    # ---------------------------- helpers ----------------------------
    def api_status(self):
        md = {}
        if META_PROVIDER:
            try:
                md = META_PROVIDER() or {}
            except Exception:
                pass
        bot = md.get("bot")
        self._json({
            "status": "online",
            "uptime": int(time.time() - START_TIME),
            "prefix": md.get("prefix", "$"),
            "port": os.environ.get("PORT", "3000"),
            "bot": bot,
            "ts": int(time.time()),
        })

    def api_user_action(self, data):
        name = (data.get("name") or "").strip()
        action = (data.get("action") or "").strip().lower()
        key = normalize_name(name)
        users = load_users()
        if key not in users:
            return self._json({"ok": False, "error": "user not found"}, 404)

        entry = users[key]
        if action == "suspend":
            entry["status"] = "suspended"
        elif action == "unsuspend":
            entry["status"] = "active"
        elif action == "ban":
            entry["status"] = "banned"
        elif action == "unban":
            entry["status"] = "active"
        elif action == "delete":
            del users[key]
            save_users(users)
            return self._json({"ok": True, "users": list_users_sorted()})
        elif action == "check":
            res = check_token(entry.get("token", ""))
            _apply_check_result(entry, res)
        else:
            return self._json({"ok": False, "error": "unknown action"}, 400)

        save_users(users)
        return self._json({"ok": True, "user": user_payload(key, users[key]),
                           "users": list_users_sorted()})


def _mask(token):
    t = token or ""
    if len(t) <= 10:
        return "*" * len(t)
    return t[:4] + "..." + t[-4:]


# ============================== SERVER ==============================
def run_server(port=None, meta_provider=None):
    global META_PROVIDER
    META_PROVIDER = meta_provider
    port = int(port or os.environ.get("PORT", "3000"))
    for candidate in (port, 10000):
        try:
            srv = HTTPServer(("0.0.0.0", candidate), PanelHandler)
        except OSError as e:
            print("[!] Port %s busy: %s" % (candidate, e))
            continue
        print("[i] Admin panel on 0.0.0.0:%s (localhost:%s)" % (candidate, candidate))
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            break
        return
    print("[!] Failed to start dashboard.")


if __name__ == "__main__":
    print("=" * 60)
    print("RED SELFBOT - ADMIN PANEL (standalone)")
    print("URL:       http://localhost:%s" % os.environ.get("PORT", "3000"))
    print("Admin key: from env ADMIN_KEY (has a built-in default)")
    print("=" * 60)
    run_server()
