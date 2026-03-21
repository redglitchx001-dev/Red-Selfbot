# -*- coding: utf-8 -*-
import sys, types, os, asyncio, json, threading, shutil, requests, datetime

# --- 🚀 FIX-URI CRITICE PENTRU PYTHON 3.13 & ANDROID ---
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
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.GyG-VN.L1YCIb-y7pDldtqsWNXQIr2x2lMxIMtUO5SVyg")
PREFIX = "$"
OWNER_ID = 1472112300344479765 

for f in ["music", "profiles", "clones", "archives", "logs"]:
    if not os.path.exists(f): os.makedirs(f)

selfbots = {}

def setup_bot(b):
    # State variables per bot instance
    state = {
        "spamming": False,
        "afk_reason": None,
        "snipe_data": {},
        "anti_kick": False,
        "anti_ban": False
    }

    # --- 🛡️ SECURITATE TOTALĂ: DOAR TU POȚI FOLOSI COMENZILE ---
    @b.check
    async def globally_restrict_to_owner(ctx):
        return ctx.author.id == OWNER_ID

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
$start @user    - Începe spam-ul din botjura.txt
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

    @b.command()
    async def helpvc(ctx):
        await ctx.message.delete()
        help_text = "```--- 🎵 VOICE HELP ---\n$plays [nr], $stops, $downloadm [url], $dwnlibs, $adfiles```"
        await ctx.send(help_text, delete_after=15)

    @b.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Intră pe un canal vocal!", delete_after=5)
        files = sorted(os.listdir("music"))
        path = None
        if name.isdigit():
            idx = int(name) - 1
            if 0 <= idx < len(files): path = f"music/{files[idx]}"
        else:
            for f in files:
                if name.lower() in f.lower():
                    path = f"music/{f}"
                    break
        if not path: return await ctx.send(f"❌ Piesa nu a fost găsită!", delete_after=5)
        try:
            vc = ctx.voice_client or await ctx.author.voice.channel.connect()
            if vc.is_playing(): vc.stop()
            vc.play(discord.FFmpegPCMAudio(path))
            await ctx.send(f"🎶 Redau: `{os.path.basename(path)}`", delete_after=10)
        except Exception as e: await ctx.send(f"❌ Eroare Voice: {e}", delete_after=10)

    @b.command()
    async def stops(ctx):
        await ctx.message.delete()
        if ctx.voice_client: await ctx.voice_client.disconnect()

    @b.command()
    async def start(ctx, user: discord.Member = None):
        await ctx.message.delete()
        state["spamming"] = True
        lines = ["RED-SELFBOT ON TOP"]
        if os.path.exists("botjura.txt"):
            with open("botjura.txt", "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
        while state["spamming"]:
            for l in lines:
                if not state["spamming"]: break
                await ctx.send(f"{user.mention if user else ''} {l}")
                await asyncio.sleep(0.8)

    @b.command()
    async def stop(ctx):
        state["spamming"] = False
        await ctx.message.delete()
        await ctx.send("🛑 Spam oprit.", delete_after=3)

    @b.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        data = {"name": ctx.guild.name, "categories": []}
        for cat in ctx.guild.categories:
            chans = [{"n": ch.name, "t": str(ch.type)} for ch in cat.channels]
            data["categories"].append({"n": cat.name, "ch": chans})
        filename = f"clones/backup_{ctx.guild.id}.json"
        with open(filename, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
        await ctx.send(f"🏰 Backup salvat: {ctx.guild.name}", delete_after=5)

    @b.command()
    async def afk(ctx, *, reason: str = "Pauză"):
        await ctx.message.delete()
        state["afk_reason"] = reason
        await ctx.send(f"🌙 AFK activat: `{reason}`", delete_after=5)

    @b.command()
    async def live(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/redglitchx"))

    @b.command()
    async def sniped(ctx):
        await ctx.message.delete()
        data = state["snipe_data"].get(ctx.channel.id)
        if data: await ctx.send(data, delete_after=15)
        else: await ctx.send("❌ Nimic de recuperat.", delete_after=5)

    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            if name in selfbots: return await ctx.send("❌ Nume deja folosit!", delete_after=5)
            new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
            setup_bot(new_bot)
            selfbots[name] = new_bot
            asyncio.create_task(new_bot.start(token))
            await ctx.send(f"✅ Cont `{name}` activat.", delete_after=7)
        else:
            lista = ", ".join(selfbots.keys()) if selfbots else "Niciunul"
            await ctx.send(f"🤖 **Conturi active:** {lista}", delete_after=10)

    @b.event
    async def on_message_delete(m):
        if m.author != b.user:
            state["snipe_data"][m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @b.event
    async def on_message(m):
        if state["afk_reason"] and b.user.mentioned_in(m) and m.author != b.user:
            await m.channel.send(f"🌙 [AFK] {state['afk_reason']}", delete_after=5)
        if state["afk_reason"] and m.author == b.user and not m.content.startswith(PREFIX):
            state["afk_reason"] = None
            await m.channel.send("👋 AFK dezactivat.", delete_after=3)
        await b.process_commands(m)

    @b.event
    async def on_ready():
        print(f"🚀 RED-SELFBOT ONLINE! | {b.user}")

# --- RUN HEALTH SERVER ---
def run_health_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

async def main_run():
    run_health_server()
    tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
    for i, token in enumerate(tokens):
        bot_inst = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
        setup_bot(bot_inst)
        selfbots[f"Main_{i}"] = bot_inst
        asyncio.create_task(bot_inst.start(token))
    while True: await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main_run())
