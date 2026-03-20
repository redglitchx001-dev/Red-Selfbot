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
        _orig = discord.settings.Settings.__init__
        def _patched(self, *, data, state):
            if data and data.get('friend_source_flags') is None:
                data['friend_source_flags'] = {}
            return _orig(self, data=data, state=state)
        discord.settings.Settings.__init__ = _patched
    except: pass

apply_patches()
os.environ['no_proxy'] = '*'

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("❌ Instalează: pip install discord.py-self==1.9.2 requests")
    sys.exit(1)

# --- ⚙️ CONFIGURARE ---
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ2OTc1MDA2NTg2MTEwMzgxMw.GdBEri.cU88G42uR3DzNJoy3Jlw3o5uBdH1MBgCEhnCTk,MTQ3MjU2MzE4ODMyNjQ2OTcxOA.GMqL3K.HDGSbjK79pmD_QZJj8XYcAwCB450RYxAdeuUYE,MTM4NDE5NTU1OTMwMDI3MjI3Mw.GYIecq.qTFTWzh-GmBkVWynAfsBeR0R0_fUBBVEDR88Ow,MTQ3MjExMjMwMDM0NDQ3OTc2NQ.G962Nn.mb1BYtrVO_jO_G4_TWek3NC4tcgpewULGeFR3c,MTE3Nzg5NTA4NTU4NTc0Nzk4OQ.GiJA5e.9Pm_uGMpiHc5K7yJlh19uCkCGe2AdamTUaGjso")
PREFIX = "$"

# Creare structură foldere
for f in ["music", "profiles", "clones", "archives", "logs"]:
    if not os.path.exists(f): os.makedirs(f)

selfbots = {} 

def setup_bot(b):
    log_chat_active = False
    log_dm_active = False
    anti_kick = False
    anti_ban = False
    tracked_users = set()
    snipe_data = {}
    spamming = False
    afk_reason = None

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
$start @user   - Începe spam-ul din botjura.txt
$stop          - Oprește procesul de spam
$spam [m][n][d] - Repetă text de X ori cu delay

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
        help_text = """```text
--- 🎵 VOICE HELP ---
$plays [nr/nume] - Redă piesa
$stops           - Oprește muzica
$downloadm [url] - Descarcă MP3
$dwnlibs         - Listă piese
$adfiles         - Upload MP3 (atașament)
```"""
        await ctx.send(help_text, delete_after=15)

    @b.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Voice!", delete_after=5)
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
        if not path or not os.path.exists(path): return await ctx.send(f"❌ Negăsit!", delete_after=5)
        try:
            vc = ctx.voice_client or await ctx.author.voice.channel.connect()
            if vc.is_playing(): vc.stop()
            vc.play(discord.FFmpegPCMAudio(path))
            await ctx.send(f"🎶 Redau: `{os.path.basename(path)}`", delete_after=10)
        except Exception as e: await ctx.send(f"❌ Eroare: {e}", delete_after=10)

    @b.command()
    async def stops(ctx):
        await ctx.message.delete()
        if ctx.voice_client: await ctx.voice_client.disconnect()

    @b.command()
    async def downloadm(ctx, link: str):
        await ctx.message.delete()
        try:
            fname = f"music/dwn_{datetime.datetime.now().strftime('%H%M%S')}.mp3"
            r = requests.get(link, stream=True, timeout=15)
            with open(fname, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
            await ctx.send(f"✅ Descărcat: `{fname}`", delete_after=10)
        except: await ctx.send("❌ Eroare!", delete_after=5)

    @b.command()
    async def adfiles(ctx):
        await ctx.message.delete()
        if not ctx.message.attachments: return await ctx.send("❌ Atașează MP3!", delete_after=5)
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                await attachment.save(f"music/{attachment.filename}")
                await ctx.send(f"✅ Salvat: `{attachment.filename}`", delete_after=5)

    @b.command()
    async def start(ctx, user: discord.Member = None):
        nonlocal spamming
        await ctx.message.delete()
        spamming = True
        lines = ["RED-SELFBOT ON TOP"]
        if os.path.exists("botjura.txt"):
            lines = [l.strip() for l in open("botjura.txt", "r", encoding="utf-8").readlines() if l.strip()]
        while spamming:
            for l in lines:
                if not spamming: break
                await ctx.send(f"{user.mention if user else ''} {l}")
                await asyncio.sleep(0.8)

    @b.command()
    async def stop(ctx):
        nonlocal spamming
        spamming = False
        await ctx.message.delete()
        await ctx.send("🛑 Spam oprit.", delete_after=3)

    @b.command()
    async def spam(ctx, msg: str, count: int, delay: float = 0.5):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(msg)
            await asyncio.sleep(delay)

    @b.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        data = {"name": ctx.guild.name, "roles": [], "categories": [], "orphan_channels": []}
        for role in reversed(ctx.guild.roles):
            if not role.managed:
                data["roles"].append({"id": role.id, "n": role.name, "c": role.color.value, "p": role.permissions.value, "h": role.hoist, "m": role.mentionable, "is_everyone": role.is_default()})
        for cat in ctx.guild.categories:
            chans = []
            for ch in cat.channels:
                chans.append({"n": ch.name, "t": str(ch.type)})
            data["categories"].append({"n": cat.name, "ch": chans})
        filename = f"clones/backup_{ctx.guild.id}.json"
        with open(filename, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
        await ctx.send(f"🏰 Backup salvat: {ctx.guild.name}", delete_after=5)

    @b.command()
    async def psrv(ctx, nr: int):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if not (1 <= nr <= len(files)): return await ctx.send("❌ Invalid", delete_after=5)
        with open(f"clones/{files[nr-1]}", "r", encoding="utf-8") as f: data = json.load(f)
        for cat in data["categories"]:
            category = await ctx.guild.create_category(cat["n"])
            for ch in cat["ch"]:
                if ch["t"] == "text": await category.create_text_channel(ch["n"])
                elif ch["t"] == "voice": await category.create_voice_channel(ch["n"])
        await ctx.send("✅ Backup aplicat!", delete_after=5)

    @b.command()
    async def tokencheck(ctx, token: str):
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
        await ctx.send(f"🎫 Token: {'✅ Valid' if r.status_code == 200 else '❌ Invalid'}", delete_after=10)

    @b.command()
    async def live(ctx, *, text):
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/red_glitch"))

    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            selfbots[name] = {"token": token}
            async def start_new_bot(t, n):
                new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
                setup_bot(new_bot); selfbots[n]["bot"] = new_bot
                try: await new_bot.start(t)
                except: 
                    if n in selfbots: del selfbots[n]
            asyncio.create_task(start_new_bot(token, name))
            await ctx.send(f"🤖 Adăugat: `{name}`", delete_after=5)
        else: await ctx.send(f"🤖 **Active:** {list(selfbots.keys())}", delete_after=10)

    @b.event
    async def on_message_delete(m):
        if m.author != b.user: snipe_data[m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @b.event
    async def on_message(m):
        nonlocal log_chat_active, log_dm_active
        if log_chat_active and m.guild and m.author != b.user:
            with open(f"logs/chat_{m.channel.id}.txt", "a", encoding="utf-8") as f: f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        if m.author == b.user: await b.process_commands(m)

    @b.event
    async def on_ready(): print(f"🚀 RED-SELFBOT ONLINE! | {b.user}")

# --- RUN ---
def run_health_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers(); self.wfile.write(b"OK")
        def log_message(self, format, *args): return
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"📡 Health check server pornit pe portul {port}")
        server.serve_forever()
    except Exception as e: print(f"❌ Eroare server health: {e}")

# --- MAIN RUN ---
async def main_run():
    print("🎬 Inițiez main_run...")
    try:
        tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
        if os.path.exists("tokens.txt"):
            with open("tokens.txt", "r", encoding="utf-8") as f:
                tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not tokens:
            print("❌ CRITIC: Nu am găsit niciun token!")
            return

        for i, token in enumerate(tokens):
            name = f"MainBot_{i}"
            new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
            setup_bot(new_bot); selfbots[name] = {"token": token, "bot": new_bot}
            async def safe_start(b, t, idx):
                try: await b.start(t)
                except Exception as e: print(f"❌ EROARE la contul {idx+1}: {e}")
            asyncio.create_task(safe_start(new_bot, token, i))
            await asyncio.sleep(2.0)

        print("✅ Toate task-urile au fost create.")
        count = 0
        while True:
            await asyncio.sleep(600)
            count += 10
            print(f"⏰ Keep-alive: {count} min. Conturi: {len(selfbots)}")
            
    except Exception as e:
        print(f"❌ EROARE FATALĂ: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    print("🚀 Pornesc bucla principală asyncio...")
    try: asyncio.run(main_run())
    except KeyboardInterrupt: print("🛑 Oprire.")
    except Exception as e: print(f"❌ Eroare: {e}")