# -*- coding: utf-8 -*-
"""
RED SELFBOT V1 - Main entry point.
Premium modular build - 2026 fancy edition.
Panel: 0.0.0.0:3000 (default) - no localhost hardcode, works with preview.
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
# DASHBOARD - Fancy gradient edition, port 3000 default
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
        fhtml += f'<div class="fb" style="border-color:{col}"><b>{lbl}</b> <span style="color:{col}">{lab}</span></div>'

    port = os.environ.get("PORT", "3000")
    # Fancy gradient logo with animation
    return f"""<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>RED SELFBOT V1 - 2026</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&family=Syne:wght@800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#06060a;color:#ddd;font-family:'JetBrains Mono',monospace;min-height:100vh;overflow-x:hidden}}
body::before{{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(255,0,60,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,0,60,.04) 1px,transparent 1px);background-size:50px 50px;pointer-events:none;z-index:0;animation:gridMove 20s linear infinite}}
@keyframes gridMove{{0%{{transform:translate(0,0)}}100%{{transform:translate(50px,50px)}}}}
.wrap{{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:30px 20px}}
.hdr{{text-align:center;padding:40px 30px;background:linear-gradient(135deg,rgba(255,0,60,.12),rgba(120,0,30,.06),rgba(255,0,60,.08));border:1px solid rgba(255,0,60,.35);border-radius:20px;margin-bottom:30px;position:relative;overflow:hidden;box-shadow:0 0 60px rgba(255,0,60,.15), inset 0 1px 0 rgba(255,255,255,.05)}}
.hdr::before{{content:'';position:absolute;inset:-3px;background:conic-gradient(from 0deg,transparent,rgba(255,0,60,.25),transparent,rgba(255,100,150,.15),transparent,rgba(255,0,60,.2),transparent);animation:rot 8s linear infinite;border-radius:20px;z-index:0}}
.hdr::after{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(255,0,60,.08),transparent 70%);pointer-events:none}}
@keyframes rot{{to{{transform:rotate(360deg)}}}}
.hdr>*{{position:relative;z-index:1}}
.logo{{font-family:'Orbitron','Syne',sans-serif;font-size:clamp(2rem,6vw,3.8rem);font-weight:900;letter-spacing:8px;line-height:1.1;background:linear-gradient(100deg,#ff0044 0%,#ff2a6d 15%,#ff6688 30%,#ff0044 45%,#ff8fab 60%,#ff0044 75%,#ff6688 100%);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:gradMove 4s linear infinite, glow 2.5s ease-in-out infinite alternate;text-transform:uppercase;filter:drop-shadow(0 0 20px rgba(255,0,60,.4))}}
@keyframes gradMove{{0%{{background-position:0% center}}100%{{background-position:200% center}}}}
@keyframes glow{{0%{{filter:drop-shadow(0 0 15px rgba(255,0,60,.3))}}100%{{filter:drop-shadow(0 0 35px rgba(255,0,60,.6)) drop-shadow(0 0 60px rgba(255,0,60,.2))}}}}
.sub{{color:#888;font-size:.78rem;letter-spacing:6px;margin-top:10px;font-weight:700;text-transform:uppercase}}
.sub2{{color:#555;font-size:.65rem;letter-spacing:3px;margin-top:6px}}
.pulse{{display:inline-flex;align-items:center;gap:10px;margin-top:18px;padding:8px 20px;border:1px solid rgba(0,255,136,.45);border-radius:50px;font-size:.85rem;color:#00ff88;background:rgba(0,255,136,.06);backdrop-filter:blur(10px);box-shadow:0 0 20px rgba(0,255,136,.15)}}
.dot{{width:10px;height:10px;border-radius:50%;background:#00ff88;box-shadow:0 0 12px #00ff88,0 0 24px rgba(0,255,136,.5);animation:pu 2s infinite}}
@keyframes pu{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(1.4)}}}}
.card{{background:linear-gradient(135deg,rgba(30,30,45,.85),rgba(20,20,30,.9));border:1px solid rgba(255,0,60,.25);border-radius:14px;padding:24px;margin-bottom:24px;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,.4)}}
.uc{{display:flex;align-items:center;gap:22px}}
.av{{width:76px;height:76px;border-radius:50%;background:linear-gradient(135deg,#ff0044,#660022,#ff6688);display:flex;align-items:center;justify-content:center;font-family:'Orbitron';font-size:2rem;font-weight:900;color:#fff;border:3px solid #ff0044;box-shadow:0 0 25px rgba(255,0,60,.5), inset 0 2px 0 rgba(255,255,255,.2);animation:avPulse 3s ease-in-out infinite}}
@keyframes avPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
.un{{font-family:'Orbitron';font-size:1.4rem;color:#fff;letter-spacing:1px}}
.tag{{color:#777;font-size:.82rem;margin-top:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:26px}}
.stat{{background:linear-gradient(135deg,rgba(30,30,45,.75),rgba(20,20,30,.85));border:1px solid rgba(255,0,60,.22);border-radius:12px;padding:22px;text-align:center;position:relative;overflow:hidden;transition:.35s;backdrop-filter:blur(8px)}}
.stat::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#ff0044,#ff6688,#ff0044);background-size:200% 100%;animation:gradMove 3s linear infinite}}
.stat:hover{{transform:translateY(-4px) scale(1.02);border-color:rgba(255,0,60,.55);box-shadow:0 12px 40px rgba(255,0,60,.2)}}
.ico{{font-size:1.7rem;margin-bottom:6px}}
.val{{font-family:'Orbitron';font-size:1.8rem;font-weight:900;color:#ff3366;text-shadow:0 0 15px rgba(255,0,60,.35)}}
.lab{{font-size:.7rem;color:#666;text-transform:uppercase;letter-spacing:2.5px;margin-top:6px}}
.st{{font-family:'Orbitron';font-size:1.05rem;color:#fff;margin-bottom:14px;padding-left:14px;border-left:4px solid #ff0044;letter-spacing:2.5px;text-transform:uppercase;display:flex;align-items:center;gap:10px}}
.st::after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,0,60,.3),transparent)}}
.fg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-bottom:26px}}
.fb{{background:rgba(20,20,30,.65);border:1px solid;border-radius:10px;padding:12px 16px;font-size:.88rem;backdrop-filter:blur(8px);transition:.2s}}
.fb:hover{{transform:translateY(-2px)}}
.term{{background:#0c0c14;border:1px solid rgba(255,0,60,.32);border-radius:12px;overflow:hidden;margin-bottom:26px;box-shadow:0 0 40px rgba(255,0,60,.1), inset 0 1px 0 rgba(255,255,255,.04)}}
.th{{display:flex;gap:7px;padding:12px 16px;background:linear-gradient(90deg,rgba(255,0,60,.09),rgba(255,0,60,.03));border-bottom:1px solid rgba(255,0,60,.18);align-items:center}}
.td{{width:12px;height:12px;border-radius:50%;box-shadow:0 0 8px currentColor}}.r{{background:#ff5f56;color:#ff5f56}}.y{{background:#ffbd2e;color:#ffbd2e}}.g{{background:#27c93f;color:#27c93f}}
.tt{{margin-left:10px;font-size:.76rem;color:#666;letter-spacing:1px}}
.tb{{padding:20px;font-size:.84rem;line-height:1.9;font-family:'JetBrains Mono'}}
.ok{{color:#00ff88}}.wa{{color:#ffbd2e}}.co{{color:#ff4d6d}}.ou{{color:#888}}.ac{{color:#ff6688}}
.foot{{text-align:center;padding:28px;color:#444;font-size:.72rem;letter-spacing:3.5px;border-top:1px solid rgba(255,0,60,.12);margin-top:10px}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.65rem;letter-spacing:1.5px;margin-left:8px;border:1px solid}}
.badge-new{{background:rgba(255,0,60,.15);border-color:rgba(255,0,60,.4);color:#ff6688}}
::-webkit-scrollbar{{width:7px}}::-webkit-scrollbar-track{{background:#08080c}}::-webkit-scrollbar-thumb{{background:linear-gradient(#ff0044,#660022);border-radius:4px}}
a{{color:#ff6688;text-decoration:none}}a:hover{{text-decoration:underline}}
</style></head><body>
<div class="wrap">
<div class="hdr">
<div class="logo">𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣</div>
<div class="sub">// V1 - PREMIUM CONTROL PANEL // 2026 EDITION //</div>
<div class="sub2">MULTI-USER • NEW PACKS • FANCY GRADIENT • 0.0.0.0:{port}</div>
<div class="pulse"><span class="dot"></span>SYSTEM ONLINE <span class="badge badge-new">NEW 2026</span></div>
</div>
<div class="card uc">
<div class="av">{un[:1].upper()}</div>
<div><div class="un">@{un}</div><div class="tag">Selfbot active • Python {platform.python_version()} • Prefix: {PREFIX} • Port: {port} • 0.0.0.0 binding</div></div>
</div>
<div class="grid">
<div class="stat"><div class="ico">⏱</div><div class="val" id="up">{uptime_s}</div><div class="lab">Uptime</div></div>
<div class="stat"><div class="ico">♜</div><div class="val">{g}</div><div class="lab">Servers</div></div>
<div class="stat"><div class="ico">⚡</div><div class="val">{p}ms</div><div class="lab">Latency</div></div>
<div class="stat"><div class="ico">🤖</div><div class="val">{len(selfbots)+1}</div><div class="lab">Accounts</div></div>
<div class="stat"><div class="ico">📊</div><div class="val">{c}</div><div class="lab">Commands</div></div>
<div class="stat"><div class="ico">👥</div><div class="val">{u}</div><div class="lab">Users</div></div>
</div>
<div class="st">MODULES</div><div class="fg">{fhtml}</div>
<div class="st">NEW PACKS 2026</div>
<div class="card" style="font-size:.85rem;line-height:1.8;color:#aaa">
<b style="color:#ff6688">data/spam_ro.txt</b> - RO ONLY, fara > # prefix, text mare<br>
<b style="color:#ff6688">data/spam_en.txt</b> - EN ONLY + GIFs, fara > #<br>
<b style="color:#ff6688">data/longspam_ro.txt</b> - RO LONG 2026, hardcore roast<br>
<b style="color:#ff6688">data/longspam_en.txt</b> - EN LONG 2026 + GIFs<br>
<b style="color:#ff6688">data/spam.txt</b> - MIX RO+EN<br>
Usage: <code style="background:rgba(255,0,60,.1);padding:2px 6px;border-radius:4px">$start @user1 @user2 spam_en.txt</code> sau <code style="background:rgba(255,0,60,.1);padding:2px 6px;border-radius:4px">$start ionut vasile alex longspam_ro.txt</code>
</div>
<div class="st">SYSTEM LOG</div>
<div class="term"><div class="th"><div class="td r"></div><div class="td y"></div><div class="td g"></div><span class="tt">red@selfbot ~ /session • 0.0.0.0:{port}</span></div>
<div class="tb">
<span class="co">[root@red-selfbot]</span> <span class="ok">$ boot --kernel --port {port}</span><br>
<span class="ok">[OK]</span> <span class="ou">Patches applied (cgi, pipes, audioop, friend_source_flags).</span><br>
<span class="ok">[OK]</span> <span class="ou">Gateway connected as @{un}.</span><br>
<span class="ok">[OK]</span> <span class="ou">Dashboard listening on 0.0.0.0:{port} (not localhost-only, works with preview).</span><br>
<span class="ok">[OK]</span> <span class="ou">Multi-user $start enabled: $start u1 u2 file.</span><br>
<span class="ok">[OK]</span> <span class="ou">Fancy menus loaded: 𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 gradient.</span><br>
<span class="ok">[OK]</span> <span class="ou">All modules loaded (help, spam, music, etc.).</span><br>
<span class="wa">[WARN]</span> <span class="ou">Selfbots violate Discord TOS. Use at own risk.</span><br>
<span class="co">[root@red-selfbot]</span> <span class="ok">$ status --live</span> <span class="ok">● Running on 0.0.0.0:{port}</span><br>
<span class="co">[root@red-selfbot]</span> <span class="ac">$ cat data/spam_ro.txt | wc -l && cat data/spam_en.txt | wc -l</span>
</div></div>
<div class="foot">𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1 • by RedGlitchX • 2026 Fancy Gradient Edition • Port {port} • 0.0.0.0</div>
</div>
<script>const sa={int(time.time())};function t(){{const s=Math.floor(Date.now()/1e3)-sa;const d=Math.floor(s/86400);const h=Math.floor(s%86400/3600);const m=Math.floor(s%3600/60);const x=s%60;const e=document.getElementById('up');if(e)e.textContent=d+'d '+h+'h '+m+'m '+x+'s'}}setInterval(t,1000);t();</script>
</body></html>"""

class Handler(BaseHTTPRequestHandler):
    def _h(self, s=200, ct="text/html"):
        self.send_response(s)
        self.send_header("Content-type", ct)
        self.send_header("Cache-Control","no-cache")
        # Allow any host / preview - critical for arena preview
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.end_headers()
    def do_OPTIONS(self):
        self._h(200, "text/plain")
        self.wfile.write(b"OK")
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/status":
            self._h(200, "application/json")
            self.wfile.write(json.dumps({"status":"online","uptime":int(time.time()-START_TIME),"prefix":PREFIX,"port":os.environ.get("PORT","3000"),"ts":int(time.time())}).encode())
            return
        if p == "/health":
            self._h(200,"text/plain"); self.wfile.write(b"OK"); return
        self._h(200,"text/html")
        md = bot_meta.get("main", {})
        md.setdefault("start", START_TIME)
        md.setdefault("cmds", sum(COMMAND_USAGE.values()))
        self.wfile.write(dashboard_html(md).encode())
    def log_message(self, *a): pass

def run_server():
    # Default to 3000 as requested, but respect PORT env
    port = int(os.environ.get("PORT", "3000"))
    # Try to bind 0.0.0.0, not localhost only
    try:
        HTTPServer(("0.0.0.0", port), Handler).serve_forever()
    except OSError as e:
        print(f"[!] Port {port} busy: {e}, trying 10000")
        try:
            HTTPServer(("0.0.0.0", 10000), Handler).serve_forever()
        except Exception as e2:
            print(f"[!] Failed to start dashboard: {e2}")

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
        print(f"\n[+] Logged in as {b.user} | Servers: {len(b.guilds)} | Prefix: {PREFIX} | Panel 0.0.0.0:{os.environ.get('PORT','3000')}")
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
        # handle intents missing in newer discord.py-self
        try:
            _int = discord.Intents.all()
        except Exception:
            _int = None
        kwargs = dict(command_prefix=PREFIX, self_bot=True)
        if _int is not None:
            kwargs["intents"] = _int
        nb = commands.Bot(**kwargs)
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

try:
    intents = discord.Intents.all()
    intents.typing = False
except Exception:
    # discord.py-self 2.1.0 may not have Intents
    intents = None

async def main():
    threading.Thread(target=run_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if not token and os.path.exists("token.txt"):
        with open("token.txt") as f: token = f.read().strip()
    if not token:
        print("[!] DISCORD_TOKEN not set. Set env or create token.txt.")
        print(f"[i] Dashboard still on 0.0.0.0:{os.environ.get('PORT','3000')} (fancy 2026)")
        while True: await asyncio.sleep(3600)
    token = token.strip().strip('"').strip("'")
    bot_kwargs = dict(command_prefix=PREFIX, self_bot=True)
    if intents is not None:
        bot_kwargs["intents"] = intents
        bot_kwargs["guild_subscriptions"] = True
    bot = commands.Bot(**bot_kwargs)
    setup_bot(bot)
    async with bot:
        try:
            bot.loop.create_task(meta_updater(bot))
        except AttributeError:
            asyncio.create_task(meta_updater(bot))
        await bot.start(token)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1 - 2026 Fancy Gradient Edition")
    print(f"Panel: 0.0.0.0:{os.environ.get('PORT','3000')} (multi-user $start)")
    print("="*50)
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n[-] Shutting down.")
