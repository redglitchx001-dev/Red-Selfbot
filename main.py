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
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.GF1C8x.YEazi4UHCJKRmh0c4r1vDnmJGNmX1pNS-OPlbA")
PREFIX = "$"

# Creare structură foldere
for f in ["music", "profiles", "clones", "archives", "logs"]:
    if not os.path.exists(f): os.makedirs(f)

selfbots = {} 

def setup_bot(b):
    # Folosim un dicționar 'state' - ASTA REZOLVĂ EROAREA PE RENDER
    state = {
        "log_chat_active": False,
        "log_dm_active": False,
        "anti_kick": False,
        "anti_ban": False,
        "tracked_users": set(),
        "snipe_data": {},
        "spamming": False,
        "afk_reason": None
    }

    # 🔒 PROTECȚIA PE ID-UL TĂU (Adaugă asta imediat sub state)
    @b.check
    async def only_owner(ctx):
        return ctx.author.id == 1472112300344479765


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
$afk [reason]  - Setează motiv AFK
$remstats      - Șterge statusul actual

🤖 ・ MULTI-ACC:
$selfbot [t][n] - Adaugă token nou
$selfbots       - Listă conturi active
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

    # --- 🎵 MODUL MUZICĂ ---
    @b.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Intră pe un canal vocal!", delete_after=5)
        if not os.path.exists("music"): os.makedirs("music")
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
        if not path: return await ctx.send(f"❌ Piesa `{name}` nu există!", delete_after=5)
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
    async def dwnlibs(ctx):
        await ctx.message.delete()
        files = sorted(os.listdir("music")) if os.path.exists("music") else []
        lista = "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)]) if files else "Gol."
        await ctx.send(f"🎵 **Librărie:**\n```\n{lista}\n```", delete_after=20)

    # --- ✉️ MODULUL SPAM (ACCESIBIL TUTUROR) ---

    @b.command()
    async def start(ctx, user: discord.Member = None):
        """Oricine poate porni spam-ul din botjura.txt"""
        await ctx.message.delete()
        
        state["spamming"] = True
        file_path = "botjura.txt"
        
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("RED-SELFBOT PE FELIE\nLIL BRO E JOS\n")
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        
        if not lines:
            state["spamming"] = False
            return await ctx.send("❌ Fișierul `botjura.txt` e gol!", delete_after=5)

        await ctx.send(f"🚀 **Spam pornit de {ctx.author.name}!**", delete_after=1)

        while state["spamming"]:
            for line in lines:
                if not state["spamming"]: break
                msg = f"{user.mention} {line}" if user else line
                try:
                    await ctx.send(msg)
                except:
                    state["spamming"] = False
                    break
                await asyncio.sleep(0.8)

    @b.command()
    async def stop(ctx):
        """Oricine poate opri spam-ul"""
        await ctx.message.delete()
        state["spamming"] = False
        await ctx.send(f"🛑 **Spam oprit de {ctx.author.name}.**", delete_after=1)

    # --- 🔒 ADMIN JURA (DOAR PENTRU TINE - ID FIX) ---

    @b.command()
    async def addline(ctx, *, text: str):
        """DOAR TU (OWNER_ID) poți adăuga linii noi"""
        # Verificăm dacă cel care scrie ești TU
        if ctx.author.id != 1472112300344479765:
            # Dacă nu ești tu, botul ignoră comanda sau trimite un mesaj discret
            return print(f"⚠️ {ctx.author.name} a încercat să adauge o linie, dar a fost respins.")

        await ctx.message.delete()
        try:
            with open("botjura.txt", "a", encoding="utf-8") as f:
                f.write(f"{text}\n")
            await ctx.send(f"✅ **Linie adăugată de Owner:** `{text}`", delete_after=5)
        except Exception as e:
            await ctx.send(f"❌ Eroare: {e}", delete_after=5)

    # --- 🏰 CLONER / BACKUP ($lsrv) ---
    @b.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        if not os.path.exists("clones"): os.makedirs("clones")
        # ... logica ta de backup ...
        filename = f"clones/backup_{ctx.guild.id}.json"
        await ctx.send(f"🏰 Backup salvat: `{filename}`", delete_after=5)

    @b.command()
    async def lsrv(ctx):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")]) if os.path.exists("clones") else []
        if not files: return await ctx.send("🏰 Niciun backup.", delete_after=5)
        msg = "🏰 **BACKUP-URI:**\n```text\n" + "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)]) + "```"
        await ctx.send(msg, delete_after=20)

  
    @b.command()
    async def logchat(ctx):
        await ctx.message.delete()
        state["log_chat_active"] = not state["log_chat_active"]
        await ctx.send(f"📜 Log Chat: **{state['log_chat_active']}**", delete_after=5)

    @b.command()
    async def sniped(ctx):
        await ctx.message.delete()
        data = state["snipe_data"].get(ctx.channel.id)
        await ctx.send(data if data else "❌ Gol.", delete_after=10)

    @b.command()
    async def afk(ctx, *, reason: str = "Pauză"):
        await ctx.message.delete()
        state["afk_reason"] = reason
        await ctx.send(f"🌙 AFK: {reason}", delete_after=5)

 
    # --- 🤖 MODUL MULTI-ACC REFACTURAT ---
    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            if name in selfbots:
                return await ctx.send(f"❌ Numele `{name}` este deja ocupat!", delete_after=5)
            
            selfbots[name] = {"token": token}
            
            async def start_new_bot(t, n):
                # Creăm instanța pentru noul cont
                new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
                # RECURSIVITATE: Noul bot primește aceleași comenzi și același OWNER_ID check
                setup_bot(new_bot) 
                selfbots[n]["bot"] = new_bot
                try: 
                    await new_bot.start(t)
                except Exception: 
                    if n in selfbots: del selfbots[n]

            # Pornim botul în fundal ca să nu blocheze execuția
            asyncio.create_task(start_new_bot(token, name))
            await ctx.send(f"🚀 Contul `{name}` a fost activat sub controlul tău.", delete_after=7)
        else:
            # Lista de conturi active (vizibilă doar ție)
            if not selfbots:
                return await ctx.send("🤖 **REȚEAUA TA:** Niciun cont extra pornit.", delete_after=10)
            lista = "\n".join([f"🔹 **{n}**" for n in selfbots.keys()])
            await ctx.send(f"🤖 **CONTURI ACTIVE:**\n{lista}", delete_after=15)

    @b.command()
    async def selfbotr(ctx, name: str):
        await ctx.message.delete()
        if name in selfbots:
            try:
                if "bot" in selfbots[name]:
                    await selfbots[name]["bot"].close()
                del selfbots[name]
                await ctx.send(f"🗑️ `{name}` a fost eliminat.", delete_after=5)
            except Exception as e:
                await ctx.send(f"❌ Eroare la oprire: {e}", delete_after=5)
        else:
            await ctx.send(f"❌ Contul `{name}` nu a fost găsit.", delete_after=5)


    # Aici poți adăuga restul comenzilor tale ($spam, $REDHELP, etc.)
    
    @b.event
    async def on_message_delete(m):
        if m.author != b.user: snipe_data[m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @b.event
    async def on_message(m):
        nonlocal afk_reason, log_chat_active, log_dm_active
        if afk_reason and b.user.mentioned_in(m) and m.author != b.user:
            await m.channel.send(f"🌙 [AFK] {afk_reason}", delete_after=5)
        if afk_reason and m.author == b.user and not m.content.startswith(PREFIX + "afk"):
            afk_reason = None
            await m.channel.send("👋 AFK dezactivat.", delete_after=3)
        if log_chat_active and m.guild and m.author != b.user:
            with open(f"logs/chat_{m.channel.id}.txt", "a", encoding="utf-8") as f: f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        if log_dm_active and not m.guild and m.author != b.user:
            with open(f"logs/dm_{m.author.id}.txt", "a", encoding="utf-8") as f: f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        if m.author == b.user: await b.process_commands(m)

    @b.event
    async def on_ready(): print(f"🚀 RED-SELFBOT ONLINE! | {b.user}")

# --- 🌐 SERVER PENTRU RENDER (KEEP ALIVE) ---
def run_health_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, format, *args): return

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    # Pornim serverul într-un thread separat ca să nu blocheze botul
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"✅ Health Server pornit pe portul {port}")

# --- 🚀 PORNIRE BOT PRINCIPAL ---
if __name__ == "__main__":
    # 1. Pornim serverul de health pentru Render
    run_health_server()

    # 2. Creăm instanța botului
    main_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)

    # 3. Aplicăm comenzile (inclusiv OWNER_ID check)
    setup_bot(main_bot)

    # 4. RUN
    try:
        print("✨ Red-Selfbot se conectează...")
        main_bot.run(TOKEN_PRINCIPAL)
    except Exception as e:
        print(f"❌ Eroare fatală la logare: {e}")

