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
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.GyG-VN.L1YCIb-y7pDldtqsWNXQIr2x2lMxIMtUO5SVyg")
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
    async def spam(ctx, user: discord.Member = None):
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
    async def repeat(ctx, msg: str, count: int, delay: float = 0.5):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(msg)
            await asyncio.sleep(delay)

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
        data = {
            "name": ctx.guild.name,
            "roles": [],
            "categories": [],
            "orphan_channels": []
        }
        for role in reversed(ctx.guild.roles):
            if not role.managed:
                data["roles"].append({
                    "id": role.id,
                    "n": role.name,
                    "c": role.color.value,
                    "p": role.permissions.value,
                    "h": role.hoist,
                    "m": role.mentionable,
                    "is_everyone": role.is_default()
                })

        def get_overwrites(channel):
            overwrites = []
            for target, overwrite in channel.overwrites.items():
                allow, deny = overwrite.pair()
                overwrites.append({
                    "id": target.id,
                    "type": "role" if isinstance(target, discord.Role) else "member",
                    "allow": allow.value,
                    "deny": deny.value
                })
            return overwrites

        for cat in ctx.guild.categories:
            chans = []
            for ch in cat.channels:
                ch_data = {"n": ch.name, "t": str(ch.type), "overwrites": get_overwrites(ch)}
                if isinstance(ch, discord.TextChannel):
                    ch_data["topic"] = ch.topic
                    ch_data["nsfw"] = ch.nsfw
                elif isinstance(ch, discord.VoiceChannel):
                    ch_data["bitrate"] = ch.bitrate
                    ch_data["user_limit"] = ch.user_limit
                chans.append(ch_data)
            data["categories"].append({"n": cat.name, "overwrites": get_overwrites(cat), "ch": chans})

        for ch in ctx.guild.channels:
            if ch.category is None:
                ch_data = {"n": ch.name, "t": str(ch.type), "overwrites": get_overwrites(ch)}
                if isinstance(ch, discord.TextChannel):
                    ch_data["topic"] = ch.topic
                    ch_data["nsfw"] = ch.nsfw
                elif isinstance(ch, discord.VoiceChannel):
                    ch_data["bitrate"] = ch.bitrate
                    ch_data["user_limit"] = ch.user_limit
                data["orphan_channels"].append(ch_data)

        filename = f"clones/backup_{ctx.guild.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
        await ctx.send(f"🏰 Backup salvat pentru **{ctx.guild.name}**!", delete_after=5)

    @b.command()
    async def lsrv(ctx):
        await ctx.message.delete()
        if not os.path.exists("clones"): os.makedirs("clones")
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if not files: return await ctx.send("🏰 Nu există backup-uri salvate.", delete_after=10)
        msg = "🏰 **LISTĂ BACKUP-URI SALVATE:**\n```text\n"
        for i, f in enumerate(files, 1):
            try:
                with open(f"clones/{f}", "r", encoding="utf-8") as file:
                    s_name = json.load(file).get("name", "Unknown")
                    msg += f"{i}. {s_name} ({f})\n"
            except: msg += f"{i}. Eroare citire: {f}\n"
        msg += "```\n*Folosește `$psrv [nr]` pentru a aplica.*"
        await ctx.send(msg, delete_after=30)

    @b.command()
    async def psrv(ctx, nr: int):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if not (1 <= nr <= len(files)): return await ctx.send(f"❌ Număr invalid!", delete_after=5)
        with open(f"clones/{files[nr-1]}", "r", encoding="utf-8") as f: data = json.load(f)
        await ctx.send(f"🏰 **Curățenie totală și aplicare backup:** `{data['name']}`...", delete_after=15)
        for channel in ctx.guild.channels:
            try: await channel.delete()
            except: pass
        for role in ctx.guild.roles:
            if not role.is_default() and not role.managed:
                try: await role.delete()
                except: pass
        role_mapping = {}
        everyone_role = ctx.guild.default_role
        for r in data.get("roles", []):
            if r.get("is_everyone"):
                role_mapping[r["id"]] = everyone_role
                try: await everyone_role.edit(permissions=discord.Permissions(r["p"]))
                except: pass
                continue
            try:
                new_role = await ctx.guild.create_role(name=r["n"], color=discord.Color(r["c"]), permissions=discord.Permissions(r["p"]), hoist=r["h"], mentionable=r["m"])
                role_mapping[r["id"]] = new_role
            except: pass
        def sync_overwrites(ow_data):
            overwrites = {}
            for ow in ow_data:
                target = role_mapping.get(ow["id"])
                if target: overwrites[target] = discord.PermissionOverwrite.from_pair(discord.Permissions(ow["allow"]), discord.Permissions(ow["deny"]))
            return overwrites
        for cat_data in data.get("categories", []):
            try:
                ow = sync_overwrites(cat_data.get("overwrites", []))
                category = await ctx.guild.create_category(cat_data["n"], overwrites=ow)
                for ch in cat_data["ch"]:
                    ch_ow = sync_overwrites(ch.get("overwrites", []))
                    if ch["t"] == "text": await category.create_text_channel(ch["n"], topic=ch.get("topic"), nsfw=ch.get("nsfw", False), overwrites=ch_ow)
                    elif ch["t"] == "voice": await category.create_voice_channel(ch["n"], bitrate=ch.get("bitrate", 64000), user_limit=ch.get("user_limit", 0), overwrites=ch_ow)
            except: pass
        for ch in data.get("orphan_channels", []):
            try:
                ch_ow = sync_overwrites(ch.get("overwrites", []))
                if ch["t"] == "text": await ctx.guild.create_text_channel(ch["n"], topic=ch.get("topic"), nsfw=ch.get("nsfw", False), overwrites=ch_ow)
                elif ch["t"] == "voice": await ctx.guild.create_voice_channel(ch["n"], bitrate=ch.get("bitrate", 64000), user_limit=ch.get("user_limit", 0), overwrites=ch_ow)
            except: pass
        await ctx.send(f"✅ Clonare finalizată.", delete_after=5)

    @b.command()
    async def clchat(ctx, amount: int = 100):
        await ctx.message.delete()
        fname = f"archives/chat_{ctx.channel.id}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            async for m in ctx.channel.history(limit=amount): f.write(f"[{m.created_at}] {m.author}: {m.content}\n")
        await ctx.send(f"📂 Chat salvat în `{fname}`", delete_after=10)

    @b.command()
    async def clist(ctx):
        await ctx.message.delete()
        await ctx.send(f"📂 **Arhive:** `{os.listdir('archives')}`", delete_after=15)

    @b.command()
    async def pstchat(ctx, channel_id: str):
        await ctx.message.delete()
        path = f"archives/chat_{channel_id}.txt"
        if not os.path.exists(path): return await ctx.send("❌ Arhivă negăsită!", delete_after=5)
        with open(path, "r", encoding="utf-8") as f: lines = f.readlines()
        for line in lines[-10:]:
            await ctx.send(line.strip())
            await asyncio.sleep(0.5)

    @b.command(name="anti-kick")
    async def anti_kick_cmd(ctx):
        nonlocal anti_kick
        await ctx.message.delete()
        anti_kick = not anti_kick
        await ctx.send(f"🛡️ Anti-Kick: **{'ACTIVAT' if anti_kick else 'DEZACTIVAT'}**", delete_after=5)

    @b.command(name="anti-ban")
    async def anti_ban_cmd(ctx):
        nonlocal anti_ban
        await ctx.message.delete()
        anti_ban = not anti_ban
        await ctx.send(f"🛡️ Anti-Ban: **{'ACTIVAT' if anti_ban else 'DEZACTIVAT'}**", delete_after=5)

    @b.command()
    async def ghostping(ctx, user: discord.Member):
        await ctx.message.delete()
        m = await ctx.send(user.mention)
        await m.delete()

    @b.command()
    async def tokencheck(ctx, token: str):
        await ctx.message.delete()
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
        await ctx.send(f"🎫 Token: {'✅ Valid' if r.status_code == 200 else '❌ Invalid'}", delete_after=10)

    @b.command()
    async def logchat(ctx):
        nonlocal log_chat_active
        await ctx.message.delete()
        log_chat_active = not log_chat_active
        await ctx.send(f"📜 Logger Chat: **{'ACTIVAT' if log_chat_active else 'DEZACTIVAT'}**", delete_after=5)

    @b.command()
    async def logdm(ctx):
        nonlocal log_dm_active
        await ctx.message.delete()
        log_dm_active = not log_dm_active
        await ctx.send(f"📜 Logger DM: **{'ACTIVAT' if log_dm_active else 'DEZACTIVAT'}**", delete_after=5)

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
    async def afk(ctx, *, reason: str = "Pauză"):
        nonlocal afk_reason
        await ctx.message.delete()
        afk_reason = reason
        await ctx.send(f"🌙 AFK activat: `{reason}`", delete_after=5)

  # --- 🤖 MODUL MULTI-ACC (DOAR PENTRU TINE) ---

def setup_bot(b):
    # ID-ul tău fix pentru securitate
    OWNER_ID = 1472112300344479765 

    @b.command()
    async def selfbot(ctx, token=None, name=None):
        """Adaugă un cont nou în rețea - DOAR OWNER"""
        # Verificare de securitate: Doar ID-ul tău are voie
        if ctx.author.id != OWNER_ID:
            return # Ignoră complet dacă nu ești tu

        await ctx.message.delete()
        
        if token and name:
            if name in selfbots:
                return await ctx.send(f"❌ Numele `{name}` este deja folosit!", delete_after=5)
            
            async def start_new_bot(t, n):
                # Creăm o instanță nouă de bot pentru noul token
                new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
                # Îi dăm aceleași comenzi (recursiv)
                setup_bot(new_bot) 
                
                selfbots[n] = {"bot": new_bot, "token": t}
                
                try:
                    print(f"🚀 Pornesc selfbot: {n}...")
                    await new_bot.start(t)
                except Exception as e:
                    print(f"❌ Eroare la {n}: {e}")
                    if n in selfbots: del selfbots[n]

            # Pornim botul în fundal fără să blocăm restul comenzilor
            asyncio.create_task(start_new_bot(token, name))
            await ctx.send(f"✅ Contul `{name}` a fost activat sub controlul tău.", delete_after=7)
            
        else:
            # Dacă scrii doar $selfbot, îți arată lista de conturi active
            if not selfbots:
                return await ctx.send("🤖 **REȚEA:** Niciun cont extra pornit.", delete_after=10)
            
            lista = "\n".join([f"🔹 **{n}**" for n in selfbots.keys()])
            await ctx.send(f"🤖 **CONTURI ACTIVE:**\n{lista}", delete_after=15)

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