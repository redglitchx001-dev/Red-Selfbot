# -*- coding: utf-8 -*-
"""
RED SELFBOT V1 - Main entry point.
Premium modular build.
"""
import sys, types, os, asyncio, json, threading, time, platform, traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Compatibility patches
def apply_patches():
    for mod_name in ["cgi", "pipes", "audioop"]:
        if mod_name not in sys.modules:
            m = types.ModuleType(mod_name)
            if mod_name == "cgi":
                m.escape = lambda x: x
                m.parse_header = lambda x: (x, {})
            elif mod_name == "pipes":
                m.quote = lambda x: x
            elif mod_name == "audioop":
                m.error = Exception
                for f in ["mul","add","bias","lin2lin","adpcm2lin","lin2adpcm","max","minmax","avg","rms"]:
                    setattr(m, f, lambda *a, **k: 0 if "lin" not in a else b'')
            sys.modules[mod_name] = m
    try:
        import discord.settings
        _o = discord.settings.Settings.__init__
        def _p(self, *, data, state):
            if data and data.get("friend_source_flags") is None:
                data["friend_source_flags"] = {}
            return _o(self, data=data, state=state)
        discord.settings.Settings.__init__ = _p
    except Exception:
        pass

apply_patches()
os.environ["no_proxy"] = "*"

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("Install: pip install discord.py-self requests PyNaCl"); sys.exit(1)

from utils.common import *
import cmds.help, cmds.text, cmds.fun, cmds.util, cmds.info, cmds.spam, cmds.music
import cmds.profiles, cmds.cloner, cmds.archives, cmds.protect, cmds.logger, cmds.status, cmds.multi
import cmds.ai

PREFIX = "$"
START_TIME = time.time()

# Global state
selfbots = {}
bot_meta = {}

# ============================================================
# DASHBOARD
# ============================================================
def dashboard_html(md):
    up = int(time.time() - md.get("start", START_TIME))
    uptime_s = fmt_time(up)
    g = md.get("guilds", 0); u = md.get("users", 0); c = md.get("cmds", 0); p = md.get("ping", 0)
    un = md.get("name", "unknown"); feat = md.get("feats", {})
    fhtml = ""
    fi = [("spam","MSG"),("logchat","LOG"),("logdm","DM"),("voice","VC"),("anti_kick","AK"),("anti_ban","AB")]
    for k, lbl in fi:
        on = feat.get(k, False); col = "#00ff88" if on else "#ff3366"; lab = "ON" if on else "OFF"
        fhtml += f'<div class=fb style=border-color:{col}><b>{lbl}</b> <span style=color:{col}>{lab}</span></div>'

    port = os.environ.get("PORT", "10000")
    return f"""<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>RED SELFBOT V1</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a0f;color:#ddd;font-family:'JetBrains Mono',monospace;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(255,0,60,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,0,60,.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0}}
.wrap{{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:30px 20px}}
.hdr{{text-align:center;padding:30px;background:linear-gradient(135deg,rgba(255,0,60,.08),rgba(120,0,30,.04));border:1px solid rgba(255,0,60,.3);border-radius:14px;margin-bottom:30px;position:relative;overflow:hidden}}
.hdr::before{{content:'';position:absolute;inset:-2px;background:conic-gradient(from 0deg,transparent,rgba(255,0,60,.15),transparent,rgba(255,0,60,.08),transparent);animation:rot 6s linear infinite}}
@keyframes rot{{to{{transform:rotate(360deg)}}}}
.hdr>*{{position:relative;z-index:1}}
.logo{{font-family:'Orbitron',sans-serif;font-size:clamp(1.8rem,5vw,3rem);font-weight:900;background:linear-gradient(135deg,#ff0044,#ff6688);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:6px}}
.sub{{color:#666;font-size:.75rem;letter-spacing:5px;margin-top:6px}}
.pulse{{display:inline-flex;align-items:center;gap:8px;margin-top:14px;padding:6px 16px;border:1px solid rgba(0,255,136,.4);border-radius:50px;font-size:.8rem;color:#00ff88}}
.dot{{width:8px;height:8px;border-radius:50%;background:#00ff88;box-shadow:0 0 8px #00ff88;animation:pu 2s infinite}}
@keyframes pu{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.4;transform:scale(1.5)}}}}
.card{{background:linear-gradient(135deg,rgba(30,30,45,.8),rgba(20,20,30,.9));border:1px solid rgba(255,0,60,.2);border-radius:12px;padding:24px;margin-bottom:24px;backdrop-filter:blur(8px)}}
.uc{{display:flex;align-items:center;gap:20px}}
.av{{width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,#ff0044,#660022);display:flex;align-items:center;justify-content:center;font-family:'Orbitron';font-size:1.8rem;font-weight:900;color:#fff;border:3px solid #ff0044;box-shadow:0 0 20px rgba(255,0,60,.4)}}
.un{{font-family:'Orbitron';font-size:1.3rem;color:#fff}}
.tag{{color:#666;font-size:.8rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;margin-bottom:24px}}
.stat{{background:linear-gradient(135deg,rgba(30,30,45,.7),rgba(20,20,30,.8));border:1px solid rgba(255,0,60,.2);border-radius:10px;padding:20px;text-align:center;position:relative;overflow:hidden;transition:.3s}}
.stat::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#ff0044,#ff6688)}}
.stat:hover{{transform:translateY(-3px);border-color:rgba(255,0,60,.6);box-shadow:0 8px 30px rgba(255,0,60,.15)}}
.ico{{font-size:1.6rem}}
.val{{font-family:'Orbitron';font-size:1.7rem;font-weight:900;color:#ff3366;text-shadow:0 0 15px rgba(255,0,60,.3)}}
.lab{{font-size:.7rem;color:#666;text-transform:uppercase;letter-spacing:2px;margin-top:4px}}
.st{{font-family:'Orbitron';font-size:1rem;color:#fff;margin-bottom:14px;padding-left:12px;border-left:3px solid #ff0044;letter-spacing:2px}}
.fg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:24px}}
.fb{{background:rgba(20,20,30,.6);border:1px solid;border-radius:8px;padding:10px 14px;font-size:.85rem;backdrop-filter:blur(6px)}}
.term{{background:#0d0d14;border:1px solid rgba(255,0,60,.3);border-radius:10px;overflow:hidden;margin-bottom:24px;box-shadow:0 0 30px rgba(255,0,60,.08)}}
.th{{display:flex;gap:6px;padding:10px 14px;background:rgba(255,0,60,.07);border-bottom:1px solid rgba(255,0,60,.15)}}
.td{{width:11px;height:11px;border-radius:50%}}.r{{background:#ff5f56}}.y{{background:#ffbd2e}}.g{{background:#27c93f}}
.tt{{margin-left:8px;font-size:.75rem;color:#555}}
.tb{{padding:18px;font-size:.82rem;line-height:1.8}}
.ok{{color:#00ff88}}.wa{{color:#ffbd2e}}.co{{color:#ff0044}}.ou{{color:#888}}
.foot{{text-align:center;padding:24px;color:#333;font-size:.7rem;letter-spacing:3px;border-top:1px solid rgba(255,0,60,.1)}}
::-webkit-scrollbar{{width:6px}}::-webkit-scrollbar-track{{background:#0a0a0f}}::-webkit-scrollbar-thumb{{background:linear-gradient(#ff0044,#660022);border-radius:3px}}
</style></head><body>
<div class=wrap>
<div class=hdr>
<div class=logo>RED SELFBOT</div>
<div class=sub>// V1 - PREMIUM CONTROL PANEL //</div>
<div class=pulse><span class=dot></span>SYSTEM ONLINE</div>
</div>
<div class="card uc">
<div class=av>{un[:1].upper()}</div>
<div><div class=un>@{un}</div><div class=tag>Selfbot active \u2022 Python {platform.python_version()} \u2022 Prefix: {PREFIX}</div></div>
</div>
<div class=grid>
<div class=stat><div class=ico>\u23f1</div><div class=val id=up>{uptime_s}</div><div class=lab>Uptime</div></div>
<div class=stat><div class=ico>\u265c</div><div class=val>{g}</div><div class=lab>Servers</div></div>
<div class=stat><div class=ico>\u26a1</div><div class=val>{p}ms</div><div class=lab>Latency</div></div>
<div class=stat><div class=ico>\U0001F916</div><div class=val>{len(selfbots)+1}</div><div class=lab>Accounts</div></div>
<div class=stat><div class=ico>\U0001F4CA</div><div class=val>{c}</div><div class=lab>Commands</div></div>
<div class=stat><div class=ico>\U0001F465</div><div class=val>{u}</div><div class=lab>Users</div></div>
</div>
<div class=st>MODULES</div><div class=fg>{fhtml}</div>
<div class=st>SYSTEM LOG</div>
<div class=term><div class=th><div class="td r"></div><div class="td y"></div><div class="td g"></div><span class=tt>red@selfbot ~ /session</span></div>
<div class=tb>
<span class=co>[root@red-selfbot]</span> <span class=ok>$ boot --kernel</span><br>
<span class=ok>[OK]</span> <span class=ou>Patches applied.</span><br>
<span class=ok>[OK]</span> <span class=ou>Gateway connected.</span><br>
<span class=ok>[OK]</span> <span class=ou>Dashboard on 0.0.0.0:{port}</span><br>
<span class=ok>[OK]</span> <span class=ou>All modules loaded.</span><br>
<span class=wa>[WARN]</span> <span class=ou>Selfbots violate Discord TOS. Use at own risk.</span><br>
<span class=co>[root@red-selfbot]</span> <span class=ok>$ status --live</span> <span class=ok>\u25cf Running</span>
</div></div>
<div class=foot>RED SELFBOT V1 \u2022 by RedGlitchX \u2022 Premium build</div>
</div>
<script>const sa={int(time.time())};function t(){{const s=Math.floor(Date.now()/1e3)-sa;const d=Math.floor(s/86400);const h=Math.floor(s%86400/3600);const m=Math.floor(s%3600/60);const x=s%60;const e=document.getElementById('up');if(e)e.textContent=d+'d '+h+'h '+m+'m '+x+'s'}}setInterval(t,1000);t();</script>
</body></html>"""

class Handler(BaseHTTPRequestHandler):
    server_version = "RedSelfbot/1"

    def _reply(self, status, body, ct="text/html; charset=utf-8"):
        """Encode the body BEFORE sending headers.

        The old code sent `200 OK` and only then encoded, so any rendering
        failure (it used to be a UnicodeEncodeError from surrogate-pair escapes)
        aborted mid-response and the browser received a blank 200 page with the
        traceback only in the server log.
        """
        if isinstance(body, str):
            body = body.encode("utf-8", errors="replace")
        self.send_response(status)
        self.send_header("Content-type", ct)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(body)
        except Exception:
            pass  # client went away

    def do_GET(self):
        p = urlparse(self.path).path
        try:
            if p == "/api/status":
                return self._reply(200, json.dumps({
                    "status": "online",
                    "uptime": int(time.time() - START_TIME),
                    "prefix": PREFIX,
                    "ts": int(time.time()),
                }), "application/json")
            if p == "/health":
                return self._reply(200, "OK", "text/plain; charset=utf-8")
            md = bot_meta.get("main", {})
            md.setdefault("start", START_TIME)
            md.setdefault("cmds", sum(COMMAND_USAGE.values()))
            return self._reply(200, dashboard_html(md))
        except Exception as e:
            traceback.print_exc()
            return self._reply(500, f"Dashboard render error: {type(e).__name__}: {e}",
                               "text/plain; charset=utf-8")

    def log_message(self, *a): pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    # SO_REUSEADDR keeps a restart from failing on a lingering TIME_WAIT socket.
    HTTPServer.allow_reuse_address = True
    try:
        httpd = HTTPServer(("0.0.0.0", port), Handler)
    except OSError as e:
        # Used to die silently inside this daemon thread, leaving the bot
        # running with no dashboard and no explanation.
        print(f"[!] Dashboard could not bind 0.0.0.0:{port} ({e}).")
        print(f"[!] Set a different port, e.g.  PORT=10001 python main.py")
        return
    print(f"[+] Dashboard listening on http://0.0.0.0:{port}")
    try:
        httpd.serve_forever()
    except Exception as e:
        print(f"[!] Dashboard stopped: {e}")

# ============================================================
# SETUP
# ============================================================
def setup_bot(b, label="main"):
    state = {
        "spamming": False, "spam_channels": set(), "spam_scope": None,
        "autoreact": False, "autoreact_emoji": None,
        "anti_kick": False, "anti_ban": False,
        "logchat_chans": set(), "logdm": False,
        "tracked": set(),
        "snipe": {}, "editsnipe": {},
        "start_lang": "default",
    }

    @b.event
    async def on_ready():
        print(f"\n[+] Logged in as {b.user} | Servers: {len(b.guilds)} | Prefix: {PREFIX}")
        if label == "main":
            users = sum(g.member_count or 0 for g in b.guilds)
            bot_meta["main"] = {
                "start": START_TIME, "name": str(b.user.name),
                "guilds": len(b.guilds), "users": users,
                "cmds": 0, "ping": round(b.latency*1000), "feats": state,
            }

    @b.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound): return
        if isinstance(error, commands.MissingRequiredArgument):
            return await safe_send(ctx, f"Missing argument. See $help.", delete_after=6)
        if isinstance(error, commands.BadArgument):
            return await safe_send(ctx, f"Bad argument.", delete_after=6)
        if isinstance(error, commands.CommandInvokeError):
            o = error.original
            if isinstance(o, discord.Forbidden): return await safe_send(ctx, "No permission.", delete_after=5)
            if isinstance(o, discord.HTTPException) and getattr(o,"code",None)==429: return
        try: traceback.print_exception(type(error), error, error.__traceback__)
        except: pass

    # Register all module commands
    cmds.help.register(b, state)
    cmds.text.register(b, state)
    cmds.fun.register(b, state)
    cmds.util.register(b, state)
    cmds.info.register(b, state)
    cmds.music.register(b, state)
    cmds.spam.register(b, state)
    cmds.profiles.register(b, state)
    cmds.cloner.register(b, state)
    cmds.archives.register(b, state)
    cmds.protect.register(b, state)
    cmds.logger.register(b, state)
    cmds.status.register(b, state)
    cmds.ai.register(b, state)

    # Multi-account callbacks
    async def add_bot(token, name):
        nb = make_bot(PREFIX)
        setup_bot(nb, label=name)
        selfbots[name] = nb
        def run_it():
            loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
            try: loop.run_until_complete(nb.start(token))
            except Exception as e: print(f"[!] {name}: {e}")
        threading.Thread(target=run_it, daemon=True).start()

    async def remove_bot(name):
        if name in selfbots:
            try: await selfbots[name].close()
            except: pass
            del selfbots[name]; return True
        return False

    cmds.multi.register(b, state, add_bot=add_bot, remove_bot=remove_bot, get_selfbots=lambda: selfbots)

    return state

async def meta_updater(b):
    await b.wait_until_ready()
    while not b.is_closed():
        try:
            md = bot_meta.get("main", {})
            md["guilds"] = len(b.guilds)
            md["users"] = sum(g.member_count or 0 for g in b.guilds)
            md["ping"] = round(b.latency*1000)
            md["cmds"] = sum(COMMAND_USAGE.values())
            bot_meta["main"] = md
        except: pass
        await asyncio.sleep(10)

async def main():
    warn_if_wrong_library()
    threading.Thread(target=run_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if not token and os.path.exists("token.txt"):
        with open("token.txt") as f: token = f.read().strip()
    if not token:
        print("[!] DISCORD_TOKEN not set. Set env or create token.txt.")
        print(f"[i] Dashboard still on port {os.environ.get('PORT','10000')}")
        while True: await asyncio.sleep(3600)
    token = token.strip().strip('"').strip("'")
    bot = make_bot(PREFIX)
    setup_bot(bot)
    print(f"[+] {len(bot.commands)} commands registered.")
    async with bot:
        bot.loop.create_task(meta_updater(bot))
        try:
            await bot.start(token)
        except LOGIN_ERRORS as e:
            print(f"\n[!] Could not connect: {type(e).__name__}: {e}")
            if not SELF_BOT_CAPABLE:
                print()
                print(LIBRARY_WARNING.format(
                    lib=discord_lib_name() or "discord.py",
                    ver=getattr(discord, "__version__", "?"),
                ))
            elif type(e).__name__ == "PrivilegedIntentsRequired":
                print("[!] Privileged intents were rejected - that happens with a BOT token.")
                print("[!] A selfbot needs a USER token.")
            else:
                print("[!] The token is invalid or revoked - grab a fresh user token.")
            raise SystemExit(1)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("RED SELFBOT V1 - Starting")
    print("="*50)

    def _shutdown():
        print("\n[-] Shutting down.")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _shutdown()
    except RuntimeError as _exc:
        # Only recover from "asyncio.run() cannot be called from a running event
        # loop". Catching every RuntimeError here used to relaunch main() after a
        # genuine failure, spawning a second dashboard thread (port clash) and a
        # second gateway session for the same account.
        if "cannot be called from a running event loop" not in str(_exc):
            raise
        print("[i] Already inside a running event loop - using a manual loop.")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            _shutdown()
        finally:
            try:
                loop.close()
            except Exception:
                pass
