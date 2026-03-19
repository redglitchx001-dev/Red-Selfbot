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
# Poți pune mai multe token-uri separate prin virgulă: "token1, token2"
# Citește din Render, dacă nu găsește, folosește lista ta ca backup
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ2OTc1MDA2NTg2MTEwMzgxMw.GdBEri.cU88G42uR3DzNJoy3Jlw3o5uBdH1MBgCEhnCTk,MTQ3MjU2MzE4ODMyNjQ2OTcxOA.GMqL3K.HDGSbjK79pmD_QZJj8XYcAwCB450RYxAdeuUYE")

PREFIX = "$"

# Creare structură foldere
for f in ["music", "profiles", "clones", "archives", "logs"]:
    if not os.path.exists(f): os.makedirs(f)

selfbots = {} 

def setup_bot(b):
    # State variables per bot instance
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
$rep [n][d][t] - Repetă text de X ori cu delay

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
        if not path or not os.path.exists(path): return await ctx.send(f"❌ Piesa `{name}` nu a fost găsită!", delete_after=5)
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
    async def downloadm(ctx, link: str):
        await ctx.message.delete()
        try:
            fname = f"music/dwn_{datetime.datetime.now().strftime('%H%M%S')}.mp3"
            r = requests.get(link, stream=True, timeout=15)
            with open(fname, 'wb') as f:
                for chunk in r.iter_content(1024): f.write(chunk)
            await ctx.send(f"✅ Descărcat: `{fname}`", delete_after=10)
        except: await ctx.send("❌ Eroare la descărcare!", delete_after=5)

    @b.command()
    async def adfiles(ctx):
        await ctx.message.delete()
        if not ctx.message.attachments:
            return await ctx.send("❌ Atașează un fișier MP3!", delete_after=5)
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                await attachment.save(f"music/{attachment.filename}")
                await ctx.send(f"✅ Salvat: `{attachment.filename}`", delete_after=5)
            else:
                await ctx.send(f"❌ `{attachment.filename}` nu este MP3!", delete_after=5)

    @b.command()
    async def dwnlibs(ctx):
        await ctx.message.delete()
        files = sorted(os.listdir("music"))
        lista = "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)]) if files else "Niciun fișier."
        await ctx.send(f"🎵 **Librărie:**\n```\n{lista}\n```", delete_after=20)

    @b.command()
    async def start(ctx, user: discord.Member = None):
        nonlocal spamming
        await ctx.message.delete()
        spamming = True
        if not os.path.exists("botjura.txt"):
            with open("botjura.txt", "w", encoding="utf-8") as f: f.write("RED-SELFBOT ON TOP\n")
        with open("botjura.txt", "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
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
    async def rep(ctx, n: int, d: float, *, t: str):
        await ctx.message.delete()
        for _ in range(n):
            await ctx.send(t)
            await asyncio.sleep(d)

    @b.command()
    async def prfdwn(ctx, user: discord.Member):
        await ctx.message.delete()
        if not os.path.exists("profiles"): os.makedirs("profiles")
        data = {
            "name": user.name,
            "id": user.id,
            "avatar": str(user.avatar_url),
            "created_at": str(user.created_at),
            "joined_at": str(user.joined_at),
            "roles": [r.name for r in user.roles]
        }
        with open(f"profiles/{user.id}.json", "w") as f: json.dump(data, f, indent=4)
        await ctx.send(f"👤 Profil arhivat: `{user.name}`", delete_after=5)

    @b.command()
    async def mphelp(ctx):
        await ctx.message.delete()
        await ctx.send("```Profil Archiver: $prfdwn @user - Salvează JSON în /profiles```", delete_after=10)

    @b.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        data = {"n": ctx.guild.name, "cats": []}
        for cat in ctx.guild.categories:
            chans = [{"n": ch.name, "t": str(ch.type)} for ch in cat.channels]
            data["cats"].append({"n": cat.name, "ch": chans})
        with open(f"clones/backup_{ctx.guild.id}.json", "w") as f: json.dump(data, f)
        await ctx.send(f"🏰 Backup salvat: `{ctx.guild.id}`", delete_after=5)

    @b.command()
    async def lsrv(ctx):
        await ctx.message.delete()
        files = os.listdir("clones")
        await ctx.send(f"🏰 **Backup-uri:** `{files}`", delete_after=15)

    @b.command()
    async def psrv(ctx, guild_id: str):
        await ctx.message.delete()
        path = f"clones/backup_{guild_id}.json"
        if not os.path.exists(path): return await ctx.send("❌ Backup negăsit!", delete_after=5)
        with open(path, "r") as f: data = json.load(f)
        await ctx.send(f"🏰 Aplicare backup: `{data['n']}`...", delete_after=5)
        for cat_data in data["cats"]:
            category = await ctx.guild.create_category(cat_data["n"])
            for ch_data in cat_data["ch"]:
                if ch_data["t"] == "text": await category.create_text_channel(ch_data["n"])
                elif ch_data["t"] == "voice": await category.create_voice_channel(ch_data["n"])

    @b.command()
    async def clchat(ctx, amount: int = 100):
        await ctx.message.delete()
        fname = f"archives/chat_{ctx.channel.id}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            async for m in ctx.channel.history(limit=amount):
                f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        await ctx.send(f"📂 Chat salvat în `{fname}`", delete_after=10)

    @b.command()
    async def clist(ctx):
        await ctx.message.delete()
        files = os.listdir("archives")
        await ctx.send(f"📂 **Arhive:** `{files}`", delete_after=15)

    @b.command()
    async def pstchat(ctx, channel_id: str):
        await ctx.message.delete()
        path = f"archives/chat_{channel_id}.txt"
        if not os.path.exists(path): return await ctx.send("❌ Arhivă negăsită!", delete_after=5)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-10:]:
            await ctx.send(line.strip())
            await asyncio.sleep(0.5)

    @b.command(name="anti-kick")
    async def anti_kick_cmd(ctx):
        nonlocal anti_kick
        await ctx.message.delete()
        anti_kick = not anti_kick
        status = "ACTIVAT" if anti_kick else "DEZACTIVAT"
        await ctx.send(f"🛡️ Anti-Kick: **{status}**", delete_after=5)

    @b.command(name="anti-ban")
    async def anti_ban_cmd(ctx):
        nonlocal anti_ban
        await ctx.message.delete()
        anti_ban = not anti_ban
        status = "ACTIVAT" if anti_ban else "DEZACTIVAT"
        await ctx.send(f"🛡️ Anti-Ban: **{status}**", delete_after=5)

    @b.command()
    async def ghostping(ctx, user: discord.Member):
        await ctx.message.delete()
        m = await ctx.send(user.mention)
        await m.delete()

    @b.command()
    async def tokencheck(ctx, token: str):
        await ctx.message.delete()
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
        res = "✅ Valid" if r.status_code == 200 else "❌ Invalid"
        await ctx.send(f"🎫 Token: {res}", delete_after=10)

    @b.command()
    async def logchat(ctx):
        nonlocal log_chat_active
        await ctx.message.delete()
        log_chat_active = not log_chat_active
        status = "ACTIVAT" if log_chat_active else "DEZACTIVAT"
        await ctx.send(f"📜 Logger Chat: **{status}**", delete_after=5)

    @b.command()
    async def logdm(ctx):
        nonlocal log_dm_active
        await ctx.message.delete()
        log_dm_active = not log_dm_active
        status = "ACTIVAT" if log_dm_active else "DEZACTIVAT"
        await ctx.send(f"📜 Logger DM: **{status}**", delete_after=5)

    @b.command()
    async def sniped(ctx):
        await ctx.message.delete()
        data = snipe_data.get(ctx.channel.id)
        if data: await ctx.send(data, delete_after=15)
        else: await ctx.send("❌ Nimic de recuperat.", delete_after=5)

    @b.command()
    async def track(ctx, user: discord.Member):
        await ctx.message.delete()
        if user.id in tracked_users:
            tracked_users.remove(user.id)
            await ctx.send(f"👁️ Nu mai urmăresc: `{user.name}`", delete_after=5)
        else:
            tracked_users.add(user.id)
            await ctx.send(f"👁️ Urmăresc: `{user.name}`", delete_after=5)

    @b.command()
    async def live(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/red_glitch"))

    @b.command()
    async def stats(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Game(name=text))

    @b.command()
    async def remstats(ctx):
        await ctx.message.delete()
        await b.change_presence(activity=None)

    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            selfbots[name] = {"token": token}
            await ctx.send(f"🤖 Adăugat: `{name}`", delete_after=5)
            
            async def start_new_bot(t, n):
                new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
                setup_bot(new_bot)
                selfbots[n]["bot"] = new_bot
                try:
                    await new_bot.start(t)
                except:
                    if n in selfbots: del selfbots[n]

            asyncio.create_task(start_new_bot(token, name))
        else:
            lista = "\n".join([f"- {n}" for n in selfbots.keys()]) if selfbots else "Niciun cont salvat."
            await ctx.send(f"🤖 **Conturi active:**\n{lista}", delete_after=10)

    @b.command()
    async def selfbotr(ctx, name: str):
        await ctx.message.delete()
        if name in selfbots:
            bot_data = selfbots[name]
            if "bot" in bot_data:
                await bot_data["bot"].close()
            del selfbots[name]
            await ctx.send(f"🤖 Șters: `{name}`", delete_after=5)
        else: await ctx.send(f"❌ Contul `{name}` nu există.", delete_after=5)

    @b.event
    async def on_message_delete(m):
        if m.author != b.user:
            snipe_data[m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @b.event
    async def on_message(m):
        nonlocal afk_reason, log_chat_active, log_dm_active
        if afk_reason and b.user.mentioned_in(m) and m.author != b.user:
            await m.channel.send(f"🌙 [AFK] {afk_reason}", delete_after=5)
        
        if log_chat_active and m.guild and m.author != b.user:
            with open(f"logs/chat_{m.channel.id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        
        if log_dm_active and not m.guild and m.author != b.user:
            with open(f"logs/dm_{m.author.id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{m.created_at}] {m.author}: {m.content}\n")

        if m.author == b.user:
            await b.process_commands(m)

    @b.event
    async def on_ready():
        print(f"🚀 RED-SELFBOT ONLINE! | {b.user}")

# --- RUN ---
def run_health_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, format, *args): return

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"📡 Health check server pornit pe portul {port}")
    server.serve_forever()

# --- MAIN RUN ---
async def main_run():
    tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
    tasks = []
    
    for i, token in enumerate(tokens):
        name = f"MainBot_{i}"
        new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
        setup_bot(new_bot)
        selfbots[name] = {"token": token, "bot": new_bot}
        tasks.append(new_bot.start(token))
        print(f"🔄 Pornesc contul {i+1}/{len(tokens)}...")

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Pornim serverul HTTP într-un thread separat ca să nu blocheze botul
    threading.Thread(target=run_health_server, daemon=True).start()
    
    try:
        asyncio.run(main_run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Eroare fatală la pornire: {e}")
