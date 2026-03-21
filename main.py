# -*- coding: utf-8 -*-
import sys
import types
import os
import json
import threading
import shutil
import requests
import datetime
import random
import time
import platform
import re
import legacy_cgi
# ... importurile tale ...
import asyncio

print("🚀 SCRIPTUL A PORNIT! Se inițiază patch-urile...") # ADAUGĂ ASTA AICI

# === [ PATCH-URI PENTRU COMPATIBILITATE PYTHON 3.13 / 3.14 ] ===
# Acestea repară ModuleNotFoundError: No module named 'cgi' / 'audioop'
if 'cgi' not in sys.modules:
    import legacy_cgi
    sys.modules['cgi'] = legacy_cgi

if 'audioop' not in sys.modules:
    try:
        import audioop_lts as audioop
        sys.modules['audioop'] = audioop
    except ImportError:
        # Mock de rezervă dacă audioop_lts eșuează
        audioop_mock = types.ModuleType('audioop')
        audioop_mock.error = Exception
        def dummy(*args, **kwargs): return b''
        audioop_mock.mul = audioop_mock.add = audioop_mock.bias = dummy
        audioop_mock.reverse = audioop_mock.lin2lin = dummy
        audioop_mock.ratecv = lambda *args, **kwargs: (b'', None)
        sys.modules['audioop'] = audioop_mock

# ACUM IMPORȚI DISCORD (după patch-uri)
import discord
from discord.ext import commands

# ... restul codului tău (TOKEN_PRINCIPAL, setup_bot, etc.)
# --- ⚙️ CONFIGURARE ---
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ2OTc1MDA2NTg2MTEwMzgxMw.GiM93S.5no1D2KpEamJKj5UXNWmxJlMrl6WrWLmJsZaSE")
GEMINI_API_KEY = os.getenv("GEMINI", "AIzaSyAHji_fQ3P9mOoFPLW82PrA_AAchxpAves")
PREFIX = "$"
START_TIME = time.time()

# Foldere
for f in ["music", "profiles", "clones", "archives", "logs"]:
    if not os.path.exists(f): os.makedirs(f)

active_selfbots = {} # Dicționar global pentru comenzi multi-account

def setup_bot(bot):
    # State per instanță
    bot_state = {
        "afk": None,
        "snipe": {},
        "spamming": False,
        "logs_chat": False,
        "logs_dm": False
    }

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



# --- 🏃 PORNIRE MULTI-ACCOUNT ---
async def main_run():
    print("🎬 Funcția main_run() a început să ruleze...") # ADAUGĂ ASTA
    
    tokens = [t.strip() for t in TOKEN_PRINCIPAL.split(",") if t.strip()]
    if os.path.exists("tokens.txt"):
        with open("tokens.txt", "r") as f: 
            tokens += [l.strip() for l in f.readlines() if l.strip()]
    
    tokens = list(set(tokens))
    print(f"📡 Am detectat {len(tokens)} token-uri de procesat.") # ADAUGĂ ASTA

    for i, token in enumerate(tokens):
        try:
            print(f"🔄 Încerc pornirea contului {i+1}/{len(tokens)}...") # ADAUGĂ ASTA
            nb = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
            setup_bot(nb)
            asyncio.create_task(nb.start(token))
            print(f"✅ Task de login creat pentru contul {i+1}.") # ADAUGĂ ASTA
            await asyncio.sleep(2)
        except Exception as e: 
            print(f"❌ EROARE la pornirea token-ului {i+1}: {e}")

    print("⏳ Toate conturile au primit comandă de pornire. Intru în bucla de menținere...") # ADAUGĂ ASTA
    while True: 
        await asyncio.sleep(3600)

if __name__ == "__main__":
    print("🌍 Inițiez serverul de Health Check și bucla Asyncio...") # ADAUGĂ ASTA
    threading.Thread(target=run_health_server, daemon=True).start()
    try:
        asyncio.run(main_run())
    except KeyboardInterrupt: 
        print("🛑 Oprire manuală detectată.")
    except Exception as e:
        print(f"❌ EROARE FATALĂ la execuție: {e}")