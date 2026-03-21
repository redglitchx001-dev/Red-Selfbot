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
GEMINI_API_KEY = os.getenv("GEMINI", "AIzaSyAHji_fQ3P9mOoFPLW82PrA_AAchxpAves")
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

   
@bot.event
    async def on_ready():
        active_selfbots[str(bot.user.id)] = bot
        print(f"✅ [ONLINE] Self-bot logat pe: {bot.user}")
    # --- COMENZILE TALE ÎNCEP MAI JOS ---

    # ==========================================
    # --- 📋 TOATE CELE 11 MENIURI HELP ---
    # ==========================================

    @bot.command()
    async def REDHELP(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
--- 📋 ・ MENIU CENTRAL AJUTOR ---
🤖 ・ $hAI     - AI & Intelligence
🛡️ ・ $hM      - Moderation & Server
🎮 ・ $hgame   - Games & Fun
🛠️ ・ $hutils  - Utils & Tools
✨ ・ $hstatus - Status & Selfbot
🚀 ・ $hadv    - Advanced & Special
🔥 ・ $hT7     - Tier 7 (Extreme)
🌟 ・ $hXtra   - Extra & New Ideas
💎 ・ $hImage  - Image Processing
💻 ・ $hSys    - System & New Fun
🏰 ・ $hClon    - Server Cloner
🎵 ・ $helpvc   - Voice & Music Master
```""", delete_after=60)

    @bot.command()
    async def hAI(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🤖 ・ AI & INTELLIGENCE:
🤖 ・ $ai [text]     - Google Gemini AI
🎨 ・ $genimg [text] - Imagine AI
🧠 ・ $brain [q]     - Răspuns rapid (DDG)
🔍 ・ $google [q]    - Căutare Google
🎥 ・ $ytsearch [q]  - Căuta pe YouTube
📖 ・ $wiki [q]      - Wikipedia
```""", delete_after=60)

    @bot.command()
    async def hM(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🛡️ ・ MODERATION & SERVER:
👢 ・ $kick @u / $ban @u / $unban [id]
🌊 ・ $massunban     - Debănează tot serverul
🔄 ・ $softban @u    - Ban + Unban rapid
🔇 ・ $mute @u       - Pune rolul Muted
🔊 ・ $unmute @u     - Scoate rolul Muted
🧹 ・ $purge [nr]    - Șterge msjele tale
🧹 ・ $purgeuser @u  - Șterge msjele unui user
⏳ ・ $slowmode [s]  - Setează slowmode
🔒 ・ $lock / $unlock- Blocare canal
💥 ・ $nuke          - Recreează canalul
```""", delete_after=60)

    @bot.command()
    async def hgame(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🎮 ・ GAMES & FUN:
😂 ・ $meme / $joke / $quote / $fact
🐱 ・ $cat / $dog    - Poze animale
🔥 ・ $howhot / $gay / $iq @user
🫂 ・ $hug / $slap / $kill / $punch
🎁 ・ $nitro         - Nitro Fake Embed
🎰 ・ $slots / $mines- Jocuri noroc
```""", delete_after=60)

    @bot.command()
    async def hutils(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🛠️ ・ UTILS & TOOLS:
🖼️ ・ $avatar / $banner @user
🏁 ・ $qr [text]     - Generează cod QR
🌐 ・ $ipinfo [ip]   - Detalii despre un IP
🔗 ・ $shorten [url] - Scurtează un link
🌦️ ・ $weather [city]- Vremea oraș
🪙 ・ $crypto [coin] - Preț Crypto (BTC)
🔢 ・ $math [expr]   - Calculator
📟 ・ $binary / $hex / $64 / $morse
```""", delete_after=60)

    @bot.command()
    async def hstatus(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
✨ ・ STATUS & SELF:
🎭 ・ $stats [text]  - Status custom
💜 ・ $live [text]   - Status streaming
💤 ・ $afk [reason]  - Setează AFK
🗑️ ・ $remstats      - Șterge status
🔄 ・ $restartstats  - Reset uptime
📡 ・ $ping / $uptime / $typing [sec]
👀 ・ $watching / $listening / $playing
```""", delete_after=60)

    @bot.command()
    async def hT7(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🔥 ・ TIER 7 (EXTREME):
☢️ ・ $spam [nr] [msg]- Spam rapid
👻 ・ $ghostspam [nr]- Spam cu ștergere
🧨 ・ $delchannels   - Șterge TOATE canalele
🧨 ・ $delroles      - Șterge TOATE rolurile
☣️ ・ $masskick      - Kick la TOȚI membrii
🧬 ・ $checktoken    - Info brute despre cont
📜 ・ $logchat       - Salvează mesaje canal
🚀 ・ $webraid [msg] - Toate conturile trimit mesaj
```""", delete_after=60)

    @bot.command()
    async def hXtra(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🌟 ・ EXTRA & IDEAS:
👤 ・ $whois / $perms / $created / $joined
🎭 ・ $mock / $clap / $ascii / $reverse
💎 ・ $aesthetic / $upper / $lower
📟 ・ $password [n]  - Generare parolă
🎨 ・ $color [hex]   - Vezi o culoare
🎲 ・ $coinflip / $8ball / $dice
🧪 ・ $pokedex / $anime / $steam
📱 ・ $iphone [msg]  - Notificare iPhone
```""", delete_after=60)

    @bot.command()
    async def hImage(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
💎 ・ IMAGE PROCESSING:
🌫️ ・ $blur @u       - Avatar blurat
🌑 ・ $gray @u       - Avatar alb-negru
🌈 ・ $invert @u     - Culori inversate
🧱 ・ $pixelate @u   - Pixelat
🎥 ・ $youtubeavatar - Avatar pe YouTube
🧪 ・ $triggered @u  - Efect triggered
📜 ・ $wanted @u     - Efect wanted
```""", delete_after=60)

    @bot.command()
    async def hSys(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
💻 ・ SYSTEM & NEW FUN:
🌡️ ・ $sysinfo      - Info System
🧠 ・ $advice       - Sfat random
🐱 ・ $neko         - Poze Anime Neko
🔗 ・ $steal [id]   - Fură Emoji după ID
📺 ・ $vaporwave [t]- Text Vaporwave
🎫 ・ $tokencheck   - Verifică validitate token
```""", delete_after=60)

    @bot.command()
    async def hClon(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🏰 ・ SERVER CLONER:
🏠 ・ $dsrv      - Dump Server (Salvează structura)
📂 ・ $lsrv      - Listă backup-uri locale
🏗️ ・ $psrv [nr] - Aplică backup pe server curent
```""", delete_after=60)

    @bot.command()
    async def hElite(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🎭 ・ ELITE & STEALTH COMMANDS:
$ghost @u      - Ping invizibil (Ghost Ping)
$faketyping [s]- Pari că scrii X secunde
$invmsg [text] - Mesaj cu text invizibil
$nitrofake     - Troll Nitro Realistic
$massnick [n]  - Schimbă nick pe toate serverele
$gcraid @u1..  - Creează grupuri spam cu useri
$spamreact [e]- Reacționează la ultimele 10 msje
$translate [l]- Tradu ultimul mesaj (ex: $translate ro)
$calc [expr]   - Calculator matematic
$whois @u      - Info detaliate utilizator
$firstmsg      - Link către primul mesaj din canal
$password [n]  - Generează parolă sigură
$ascii [text]  - Transformă text în ASCII Art
$emojify [text]- Transformă text în litere emoji
$8ball [q]     - Întreabă oracolul
$dice          - Dă cu zarul (1-6)
$coin          - Dă cu banul (Cap/Pajură)
$joinedat @u   - Vezi data intrării pe server
$serverinfo    - Detalii brute despre server
$tokeninfo [t] - Info despre un token extern
$groupdm [msg] - Trimite DM la toți din grupul curent
$copy          - Retrimite ultimul tău mesaj
$clear [n]     - Șterge ultimele tale X mesaje
$reverse [t]   - Inversează textul
$bold [t]      - Scrie îngroșat rapid
```""", delete_after=60)

    @bot.command()
    async def helpvc(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🎵 ・ VOICE & MUSIC:
$plays [nr/nume]- Redă piesa din folderul music
$stops          - Oprește muzica și ieși din VC
$downloadm [url]- Descarcă de pe YouTube
$dwnlibs        - Vezi lista de piese salvate
$adfiles        - Salvează MP3 din atașament
```""", delete_after=60)

    # ==========================================
    # --- 🏰 CLONER LOGIC ---
    # ==========================================

    @bot.command()
    async def dsrv(ctx):
        await ctx.message.delete()
        data = {"name": ctx.guild.name, "roles": [], "categories": []}
        for role in ctx.guild.roles:
            if not role.managed and role.name != "@everyone":
                data["roles"].append({"n": role.name, "c": role.color.value, "p": role.permissions.value})
        for cat in ctx.guild.categories:
            chans = [{"n": ch.name, "t": str(ch.type)} for ch in cat.channels]
            data["categories"].append({"n": cat.name, "ch": chans})
        with open(f"clones/backup_{ctx.guild.id}.json", "w") as f: json.dump(data, f, indent=4)
        await ctx.send(f"🏰 Backup salvat: `{ctx.guild.name}`")

    @bot.command()
    async def psrv(ctx, nr: int):
        await ctx.message.delete()
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        if not (1 <= nr <= len(files)): return await ctx.send("❌ ID Backup invalid.")
        with open(f"clones/{files[nr-1]}", "r") as f: data = json.load(f)
        await ctx.send("🏗️ Aplicare backup...")
        for ch in ctx.guild.channels: await ch.delete()
        for r in data["roles"]:
            try: await ctx.guild.create_role(name=r["n"], color=discord.Color(r["c"]), permissions=discord.Permissions(r["p"]))
            except: pass
        for c in data["categories"]:
            cat = await ctx.guild.create_category(c["n"])
            for ch in c["ch"]:
                if ch["t"] == "text": await cat.create_text_channel(ch["n"])
                else: await cat.create_voice_channel(ch["n"])

    # ==========================================
    # --- 🎙️ VOICE & MUSIC ---
    # ==========================================

    @bot.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Intră pe un canal vocal!")
        files = sorted(os.listdir("music"))
        path = None
        if name.isdigit():
            idx = int(name) - 1
            if 0 <= idx < len(files): path = f"music/{files[idx]}"
        else:
            for f in files:
                if name.lower() in f.lower(): path = f"music/{f}"; break
        if not path: return await ctx.send("❌ Piesă negăsită.")
        vc = ctx.voice_client or await ctx.author.voice.channel.connect()
        if vc.is_playing(): vc.stop()
        vc.play(discord.FFmpegPCMAudio(path))
        await ctx.send(f"🎶 Redau: `{os.path.basename(path)}`")

    @bot.command()
    async def stops(ctx):
        await ctx.message.delete()
        if ctx.voice_client: await ctx.voice_client.disconnect()

    # ==========================================
    # --- 🤖 AI & SEARCH ---
    # ==========================================

    @bot.command()
    async def ai(ctx, *, prompt):
        await ctx.message.delete()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        try:
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
            ans = r['candidates'][0]['content']['parts'][0]['text']
            await ctx.send(f"🤖 **AI Gemini:** {ans[:1900]}")
        except: await ctx.send("❌ Eroare Gemini. Verifică API Key.")

    # ==========================================
    # --- 🚀 MULTI-ACCOUNT RAID ---
    # ==========================================

    @bot.command()
    async def webraid(ctx, *, msg):
        await ctx.message.delete()
        for bot_id, bot_obj in active_selfbots.items():
            channel = bot_obj.get_channel(ctx.channel.id)
            if channel: asyncio.create_task(channel.send(msg))

    # ==========================================
    # --- 🛠️ UTILS & OTHERS ---
    # ==========================================

    @bot.command()
    async def sniped(ctx):
        await ctx.message.delete()
        msg = bot_state["snipe"].get(ctx.channel.id, "❌ Nimic de recuperat.")
        await ctx.send(msg)

    @bot.command()
    async def afk(ctx, *, reason="Pauză"):
        await ctx.message.delete()
        bot_state["afk"] = reason
        await ctx.send(f"🌙 AFK Activat: `{reason}`", delete_after=5)

    @bot.command()
    async def steal(ctx, emoji_id: int):
        await ctx.message.delete()
        try:
            url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
            r = requests.get(url)
            await ctx.guild.create_custom_emoji(name=f"stolen_{emoji_id}", image=r.content)
            await ctx.send("✅ Emoji furat!")
        except: await ctx.send("❌ Eroare la furt!")

    # ==========================================
    # --- 📥 EVENTS ---
    # ==========================================

    @bot.event
    async def on_message_delete(m):
        if m.author != bot.user:
            bot_state["snipe"][m.channel.id] = f"🎯 **{m.author}**: {m.content}"

    @bot.event
    async def on_message(m):
        # AFK Check
        if bot_state["afk"] and bot.user.mentioned_in(m) and m.author != bot.user:
            await m.channel.send(f"🌙 [AFK] {bot_state['afk']}", delete_after=5)
        if bot_state["afk"] and m.author == bot.user and not m.content.startswith(PREFIX + "afk"):
            bot_state["afk"] = None
            await m.channel.send("👋 AFK dezactivat.", delete_after=3)
        
        # Procesare comenzi
        if m.author == bot.user:
            await bot.process_commands(m)

    @bot.event
    async def on_ready():
        active_selfbots[str(bot.user.id)] = bot
        print(f"🚀 [ONLINE] {bot.user}")

    # ==========================================
    # --- 🎭 CELE 25 COMENZI NOI (ELITE) ---
    # ==========================================

    @bot.command()
    async def ghost(ctx, user: discord.Member):
        await ctx.message.delete()
        m = await ctx.send(user.mention)
        await m.delete()

    @bot.command()
    async def faketyping(ctx, seconds: int):
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(seconds)

    @bot.command()
    async def invmsg(ctx, *, text):
        await ctx.message.delete()
        await ctx.send(f"||||{text}") 

    @bot.command()
    async def nitrofake(ctx):
        await ctx.message.delete()
        await ctx.send("🎁 **Ai primit un cadou Nitro!**\nhttps://discord.gift/dQw4w9WgXcQ")

    @bot.command()
    async def massnick(ctx, *, name):
        await ctx.message.delete()
        count = 0
        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=name)
                count += 1
            except: pass
        await ctx.send(f"✅ Nickname schimbat pe `{count}` servere.")

    @bot.command()
    async def translate(ctx, lang, *, text=None):
        await ctx.message.delete()
        if not text:
            async for m in ctx.channel.history(limit=2): text = m.content
        r = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang}&dt=t&q={text}").json()
        await ctx.send(f"🌍 **Traducere ({lang}):** {r[0][0][0]}")

    @bot.command()
    async def calc(ctx, *, expr):
        await ctx.message.delete()
        try:
            res = eval(expr, {"__builtins__": None}, {})
            await ctx.send(f"🔢 **Rezultat:** `{res}`")
        except: await ctx.send("❌ Expresie invalidă.")

    @bot.command()
    async def whois(ctx, u: discord.Member = None):
        await ctx.message.delete()
        u = u or ctx.author
        roles = [r.name for r in u.roles[1:]]
        await ctx.send(f"```text\n👤 USER: {u.name}\n🆔 ID: {u.id}\n📅 CREAT: {u.created_at}\n🎭 ROLURI: {', '.join(roles)}\n📱 STATUS: {u.status}\n```")

    @bot.command()
    async def firstmsg(ctx):
        await ctx.message.delete()
        async for m in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.send(f"🔗 **Primul mesaj:** {m.jump_url}")

    @bot.command()
    async def password(ctx, length: int = 12):
        await ctx.message.delete()
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(length))
        await ctx.send(f"🔑 Parolă generată: `{pwd}`", delete_after=10)

    @bot.command()
    async def emojify(ctx, *, text):
        await ctx.message.delete()
        res = ""
        for char in text.lower():
            if char.isalpha(): res += f":regional_indicator_{char}: "
            elif char.isdigit(): 
                nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
                res += f":{nums[int(char)]}: "
            else: res += char + " "
        await ctx.send(res)

    @bot.command()
    async def dice(ctx):
        await ctx.message.delete()
        await ctx.send(f"🎲 Zarul a picat pe: **{random.randint(1,6)}**")

    @bot.command()
    async def coin(ctx):
        await ctx.message.delete()
        await ctx.send(f"🪙 Rezultat: **{random.choice(['Cap', 'Pajură'])}**")

    @bot.command()
    async def spamreact(ctx, emoji):
        await ctx.message.delete()
        async for m in ctx.channel.history(limit=10):
            try: await m.add_reaction(emoji)
            except: pass

    @bot.command()
    async def tokeninfo(ctx, token):
        await ctx.message.delete()
        r = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token})
        if r.status_code == 200:
            d = r.json()
            await ctx.send(f"```text\n✅ VALID\n👤 {d['username']}\n🆔 {d['id']}\n📧 {d.get('email', 'N/A')}\n```")
        else: await ctx.send("❌ Token Invalid.")

    @bot.command()
    async def gcraid(ctx, *users: discord.User):
        await ctx.message.delete()
        if len(users) < 1: return
        for _ in range(3):
            try: await bot.user.create_group(users)
            except: break
        await ctx.send("🚀 Raid grupuri pornit.")

    @bot.command()
    async def joinedat(ctx, u: discord.Member = None):
        await ctx.message.delete()
        u = u or ctx.author
        await ctx.send(f"📅 **{u.name}** a intrat pe: `{u.joined_at.strftime('%d/%m/%Y %H:%M')}`")

    @bot.command()
    async def serverinfo(ctx):
        await ctx.message.delete()
        g = ctx.guild
        await ctx.send(f"```text\n🏰 SERVER: {g.name}\n🆔 ID: {g.id}\n👤 OWNER: {g.owner}\n👥 MEMBRI: {g.member_count}\n✨ NIVEL: {g.premium_tier}\n```")

    @bot.command()
    async def groupdm(ctx, *, msg):
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.GroupChannel):
            for recipient in ctx.channel.recipients:
                try: await recipient.send(msg); await asyncio.sleep(1)
                except: pass
        else: await ctx.send("❌ Trebuie să fii într-un grup!")

    @bot.command()
    async def copy(ctx):
        await ctx.message.delete()
        if bot_state["last_msg"]: await ctx.send(bot_state["last_msg"])

    @bot.command()
    async def clear(ctx, amount: int = 5):
        await ctx.message.delete()
        count = 0
        async for m in ctx.channel.history(limit=100):
            if m.author == bot.user:
                await m.delete()
                count += 1
            if count >= amount: break

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

    @b.command()
    async def selfbot(ctx, token=None, name=None):
        await ctx.message.delete()
        if token and name:
            selfbots[name] = {"token": token}
            async def start_new_bot(t, n):
                new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
                setup_bot(new_bot)
                selfbots[n]["bot"] = new_bot
                try: await new_bot.start(t)
                except: 
                    if n in selfbots: del selfbots[n]
            asyncio.create_task(start_new_bot(token, name))
            await ctx.send(f"🤖 Adăugat: `{name}`", delete_after=5)
        else:
            lista = "\n".join([f"- {n}" for n in selfbots.keys()]) if selfbots else "Niciun cont salvat."
            await ctx.send(f"🤖 **Conturi active:**\n{lista}", delete_after=10)

    @b.command()
    async def selfbotr(ctx, name: str):
        await ctx.message.delete()
        if name in selfbots:
            if "bot" in selfbots[name]: await selfbots[name]["bot"].close()
            del selfbots[name]
            await ctx.send(f"🤖 Șters: `{name}`", delete_after=5)
        else: await ctx.send(f"❌ Contul `{name}` nu există.", delete_after=5)

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
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, format, *args): return
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        server.serve_forever()
    except: pass

async def main_run():
    tokens = []
    if os.path.exists("tokens.txt"):
        with open("tokens.txt", "r", encoding="utf-8") as f: tokens = [l.strip() for l in f.readlines() if l.strip()]
    if not tokens: tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
    if not tokens: return print("❌ CRITIC: Nu am găsit niciun token!")
    for i, token in enumerate(tokens):
        name = f"MainBot_{i}"
        try:
            new_bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
            setup_bot(new_bot)
            selfbots[name] = {"token": token, "bot": new_bot}
            async def safe_start(bot, t):
                try: await bot.start(t)
                except: pass
            asyncio.create_task(safe_start(new_bot, token))
            await asyncio.sleep(2.0)
        except: pass
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    try: asyncio.run(main_run())
    except KeyboardInterrupt: print("🛑 Oprire.")