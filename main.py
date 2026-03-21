# -*- coding: utf-8 -*-
import sys, types, os, asyncio, json, threading, shutil, requests, datetime, re

# --- 🚀 FIX-URI PYTHON 3.13 (RENDER/ANDROID) ---
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
                for f in ["mul", "add", "bias", "lin2lin", "adpcm2lin", "lin2adpcm", "max", "minmax", "avg", "rms"]:
                    setattr(m, f, lambda *args, **kwargs: 0 if "lin" not in args else b'')
            sys.modules[mod_name] = m
    try:
        import discord.settings
        _orig = discord.settings.Settings.init
        def _patched(self, *, data, state):
            if data and data.get('friend_source_flags') is None:
                data['friend_source_flags'] = {}
            return _orig(self, data=data, state=state)
        discord.settings.Settings.init = _patched
    except: pass

apply_patches()

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ Instalează: pip install discord.py-self==1.9.2 requests")
    sys.exit(1)

# --- ⚙️ CONFIGURARE ---
# Token-ul principal este cel din variabila de mediu sau cel pus aici.
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.GyG-VN.L1YCIb-y7pDldtqsWNXQIr2x2lMxIMtUO5SVyg")
PREFIX = "$"
OWNER_ID = 1472112300344479765 

# Creare structură foldere
FOLDERS = ["music", "profiles", "clones", "archives", "logs"]
for f in FOLDERS:
    if not os.path.exists(f): os.makedirs(f)

selfbots = {}

def setup_bot(b):
    # Starea internă a fiecărui cont
    state = {
        "spamming": False,
        "afk_reason": None,
        "snipe_data": {},
        "anti_kick": False,
        "anti_ban": False,
        "log_chat": False,
        "log_dm": False
    }

    # --- 🛡️ SECURITATE: DOAR TU ---
    @b.check
    async def owner_only(ctx):
        return ctx.author.id == OWNER_ID

    # --- 📜 MENIUL COMPLET ---
    @b.command()
    async def REDHELP(ctx):
        await ctx.message.delete()
        menu = """```text
--- 📋 ・ LISTA COMPLETĂ COMENZI ---

🎵 ・ MUZICĂ & VOICE:
$helpvc        - Meniu rapid voice
$downloadm     - Descarcă de pe YouTube [link]
$adfiles       - Atașează un MP3 pentru upload
$dwnlibs       - Vezi lista de piese salvate
$plays [nr]    - Pornește piesa cu numărul X
$stops         - Oprește muzica și ieși din canal

✉️ ・ SPAM BOT:
$spam @user    - Începe spam-ul din botjura.txt
$stop          - Oprește procesul de spam
$repeat [m][n][d] - Repetă text de X ori cu delay

👤 ・ PROFILE ARCHIVER:
$prfdwn @user  - Descarcă profilul în /profiles
$mphelp        - Meniu setări pentru profiler

🏰 ・ MODUL CLONER ($DSRV):
$dsrv          - Copiază structura serverului
$lsrv          - Listă scheme salvate local
$psrv [nr]     - Aplică schema pe server nou

📂 ・ COPIERE & ARHIVARE:
$clchat [nr]   - Copiază ultimele mesaje + Media
$clist         - Afișează lista clipurilor
$pstchat [nr]  - Lipește chat-ul din fișierul X

🛡️ ・ MODUL BP2 ($BP2HELP):
$anti-kick     - Protecție kick (on/off)
$anti-ban      - Protecție ban (on/off)
$ghostping     - Ping discret @user
$tokencheck    - Verifică validitate token-uri

📜 ・ MODUL LOGGER ($LHELP):
$logchat       - Loghează mesajele din canal
$logdm         - Salvează mesajele din privat
$sniped        - Vezi ultimul mesaj șters
$track @user   - Notificări status utilizator

✨ ・ STATUS & UTIL:
$stats [text]  - Setează status personalizat
$live [text]   - Setează status streaming mov
$afk [reason]  - Setează motiv AFK
$remstats      - Șterge statusul actual

🤖 ・ MULTI-ACC:
$selfbot [t][n]- Adaugă token nou
$selfbot       - Listă conturi active
$selfbotr [nume]- Șterge cont din listă

⚙️ ・ ADMIN:
$REDHELP        - Meniu complet (vizibil 30 sec)

------------------------------------------
Credits: RedGlitchX / redglitchx. / XTASK 
         Nightu / nightu._. / ⌬ VORTASK
         bulgaruu / o.bulgaruu
------------------------------------------
```"""
        await ctx.send(menu, delete_after=30)

    # --- 🎵 MUZICĂ & VOICE ---
    @b.command()
    async def helpvc(ctx):
        await ctx.message.delete()
        await ctx.send("```🎵 $plays [nr], $stops, $downloadm, $adfiles, $dwnlibs```", delete_after=15)

    @b.command()
    async def dwnlibs(ctx):
        await ctx.message.delete()
        files = sorted(os.listdir("music"))
        if not files: return await ctx.send("❌ Biblioteca e goală.", delete_after=5)
        text = "--- 🎵 BIBLIOTECĂ ---\n" + "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)])
        await ctx.send(f"```text\n{text}```", delete_after=20)

    @b.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Intră pe VC!", delete_after=5)
        files = sorted(os.listdir("music"))
        path = None
        if name.isdigit() and 1 <= int(name) <= len(files):
            path = f"music/{files[int(name)-1]}"
        else:
            for f in files:
                if name.lower() in f.lower(): path = f"music/{f}"; break
        
        if path:
            vc = ctx.voice_client or await ctx.author.voice.channel.connect()
            if vc.is_playing(): vc.stop()
            vc.play(discord.FFmpegPCMAudio(path))
            await ctx.send(f"🎶 Redau: `{os.path.basename(path)}`", delete_after=10)
        else: await ctx.send("❌ Piesă negăsită.", delete_after=5)

    @b.command()
    async def stops(ctx):
        await ctx.message.delete()
        if ctx.voice_client: await ctx.voice_client.disconnect()

    # --- ✉️ SPAM BOT ---
    @b.command()
    async def spam(ctx, user: discord.Member = None):
        await ctx.message.delete()
        state["spamming"] = True
        lines = ["RED-SELFBOT ON TOP"]
        if os.path.exists("botjura.txt"):
            with open("botjura.txt", "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
        
        while state["spamming"]:
            for line in lines:
                if not state["spamming"]: break
                await ctx.send(f"{user.mention if user else ''} {line}")
                await asyncio.sleep(0.7)

    @b.command()
    async def stop(ctx):
        state["spamming"] = False
        await ctx.message.delete()
        await ctx.send("🛑 Proces oprit.", delete_after=3)

    @b.command()
    async def repeat(ctx, times: int, delay: float, *, text):
        await ctx.message.delete()
        for _ in range(times):
            await ctx.send(text)
            await asyncio.sleep(delay)

    # --- 👤 PROFILE ARCHIVER ---
    @b.command()
    async def prfdwn(ctx, user: discord.User):
        await ctx.message.delete()
        u_dir = f"profiles/{user.id}"
        if not os.path.exists(u_dir): os.makedirs(u_dir)
        
        data = {
            "name": user.name, "id": user.id, "created": str(user.created_at),
            "avatar": str(user.avatar_url), "banner": str(user.banner_url if hasattr(user, 'banner') else None)
        }
        with open(f"{u_dir}/info.json", "w") as f: json.dump(data, f, indent=4)
        if user.avatar_url:
            r = requests.get(user.avatar_url)
            with open(f"{u_dir}/avatar.png", "wb") as f: f.write(r.content)
        await ctx.send(f"👤 Profil salvat: `{user.name}`", delete_after=5)

    # --- 🏰 CLONER ---
    @b.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        backup = {
            "n": ctx.guild.name,
            "cats": []
        }
        for cat in sorted(ctx.guild.categories, key=lambda x: x.position):
            c_data = {"n": cat.name, "ch": []}
            for ch in sorted(cat.channels, key=lambda x: x.position):
                c_data["ch"].append({"n": ch.name, "t": str(ch.type)})
            backup["cats"].append(c_data)
        
        idx = len(os.listdir("clones")) + 1
        with open(f"clones/backup_{idx}.json", "w") as f: json.dump(backup, f)
        await ctx.send(f"🏰 Backup salvat cu ID `{idx}`", delete_after=7)

    @b.command()
    async def lsrv(ctx):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if not files: return await ctx.send("❌ Nicio schemă.", delete_after=5)
        text = "--- 🏰 SCHEME ---\n" + "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)])
        await ctx.send(f"```text\n{text}```", delete_after=20)

    @b.command()
    async def psrv(ctx, nr: int):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if nr < 1 or nr > len(files): return await ctx.send("❌ Index invalid.", delete_after=5)
        
        with open(f"clones/{files[nr-1]}", "r") as f: data = json.load(f)
        await ctx.send("🏗️ Construiesc serverul...", delete_after=5)
        for c in ctx.guild.channels: 
            try: await c.delete()
            except: pass
        
        for cat_d in data["cats"]:
            category = await ctx.guild.create_category(cat_d["n"])
            for ch_d in cat_d["ch"]:
                if ch_d["t"] == "text": await category.create_text_channel(ch_d["n"])
                else: await category.create_voice_channel(ch_d["n"])

    # --- 🛡️ BP2 & PROTECȚIE ---
    @b.command(name="anti-kick")
    async def antikick(ctx):
        state["anti_kick"] = not state["anti_kick"]
        await ctx.send(f"🛡️ Anti-Kick: {'ON' if state['anti_kick'] else 'OFF'}", delete_after=5)

    @b.command(name="anti-ban")
    async def antiban(ctx):
        state["anti_ban"] = not state["anti_ban"]
        await ctx.send(f"🛡️ Anti-Ban: {'ON' if state['anti_ban'] else 'OFF'}", delete_after=5)

    @b.command()
    async def ghostping(ctx, user: discord.Member):
        await ctx.message.delete()
        await ctx.send(user.mention, delete_after=0.1)

    # --- 📜 LOGGER ---
    @b.command()
    async def logchat(ctx):
        state["log_chat"] = not state["log_chat"]
        await ctx.send(f"📜 Log Chat: {'ON' if state['log_chat'] else 'OFF'}", delete_after=5)

    @b.command()
    async def sniped(ctx):
        await ctx.message.delete()
        msg = state["snipe_data"].get(ctx.channel.id, "❌ Nimic înregistrat.")
        await ctx.send(msg, delete_after=15)

    # --- ✨ STATUS ---
    @b.command()
    async def stats(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Game(name=text))

    @b.command()
    async def live(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/redglitchx"))

    @b.command()
    async def afk(ctx, *, reason="Pauză"):
        await ctx.message.delete()
        state["afk_reason"] = reason
        await ctx.send(f"🌙 AFK: `{reason}`", delete_after=5)

    @b.command()
    async def remstats(ctx):
        await ctx.message.delete()
        await b.change_presence(activity=None)

    # --- 🤖 MULTI-ACC ---
    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
            setup_bot(new_bot)
            selfbots[name] = new_bot
            asyncio.create_task(new_bot.start(token))
            await ctx.send(f"✅ Cont `{name}` adăugat.", delete_after=5)
        else:
            accs = ", ".join(selfbots.keys()) if selfbots else "Niciunul"
            await ctx.send(f"🤖 **Conturi active:** {accs}", delete_after=10)

    # --- 🛰️ EVENIMENTE ---
    @b.event
    async def on_message_delete(m):
        if m.author != b.user:
            state["snipe_data"][m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @b.event
    async def on_message(m):
        if state["afk_reason"] and b.user.mentioned_in(m) and m.author != b.user:
            await m.channel.send(f"🌙 [AFK] {state['afk_reason']}", delete_after=7)
        
        if state["log_chat"] and not m.author.bot:
            with open(f"logs/{m.channel.id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}] {m.author}: {m.content}\n")
        
        if m.author.id == OWNER_ID:
            await b.process_commands(m)

    @b.event
    async def on_ready():
        print(f"🚀 {b.user} pornit!")

# --- 🌐 SERVER HEALTH (PENTRU RENDER) ---
def start_health():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class H(BaseHTTPRequestHandler):
        def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), H)
    threading.Thread(target=server.serve_forever, daemon=True).start()

async def start_all():
    start_health()
    # Separăm token-urile dacă sunt puse cu virgulă în variabila TOKEN
    tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
    for i, t in enumerate(tokens):
        bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
        setup_bot(bot)
        selfbots[f"Main_{i}"] = bot
        asyncio.create_task(bot.start(t))
    
    while True: await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt: pass
