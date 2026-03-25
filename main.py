import discord
from discord.ext import commands
import asyncio
import threading
import os
import datetime
import requests
import json
import psutil
try:
    import psutil
except ImportError:
    psutil = None
    
import platform
import random
import google.generativeai as genai
from flask import Flask

# --- SERVER PENTRU RENDER (Keep Alive) ---
app = Flask('')
@app.route('/')
def home(): return "Selfbot is Online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# --- CONFIGURARE AUTOMATĂ DIN RENDER ---
# Aici botul ia numele exact din screenshot-ul tău
TOKEN = os.getenv("DISCORD_TOKEN") 
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OWNER_ID = 1472112300344479765 
PREFIX = "$"

# --- INITIALIZARE BOT & AI ---
bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)
start_time = datetime.datetime.utcnow()

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    ai_model = genai.GenerativeModel('gemini-pro')
    
# ==========================================
# ACUM LIPESTE AICI TOATE TXT-URILE TALE
# (Inclusiv "Owner Only.txt" care are ID-ul)
# ==========================================
# ==========================================
# AICI LIPESTI TU COMENZILE TALE
# ===========================================
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
🏰 ・ $hClon   - Server Cloner
🎵 ・ $helpvc  - Voice & Music Master
🎫 ・ $hold    - Comenzile Vechi 
👑 ・ $hOwner  - Comenzile Ownerului
------------------------------------------
Credits: RedGlitchX / redglitchx. / XTASK 
         Nightu / nightu._. / ⌬ VORTASK
         bulgaruu / o.bulgaruu
------------------------------------------
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

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
```""", delete_after=30)

@bot.command()
async def hClon(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🏰 ・ SERVER CLONER:
🏠 ・ $dsrv      - Dump Server (Salvează structura)
📂 ・ $lsrv      - Listă backup-uri locale
🏗️ ・ $psrv [nr] - Aplică backup pe server curent
```""", delete_after=15)

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
```""", delete_after=15)
        
@bot.command()
async def hold(ctx):
    await ctx.message.delete()
    menu = """```text
--- 🎫 ・ Comenzile Old --- 

✉️ ・ SPAM BOT:
$start @user   - Începe spam-ul din botjura.txt
$stop          - Oprește procesul de spam
$spam [m][n][d]- Repetă text de X ori cu delay

👤 ・ PROFILE ARCHIVER:
$prfdwn @user  - Descarcă profilul în /profiles
$prflist       - Meniu pentru profiler
$show [Nr]     - Arată Poza in chat 

📂 ・ COPIERE & ARHIVARE:
$clchat [nr]   - Copiază ultimele mesaje + Media
$clist         - Afișează lista clipurilor
$pstchat [nr]  - Lipește chat-ul din fișierul X

🛡️ ・ MODUL BP2 ($BP2HELP):
$anti-kick     - Protecție kick (on/off)
$anti-ban      - Protecție ban (on/off)
$ghostping     - Ping discret @user
```"""
    await ctx.send(menu, delete_after=30)

@bot.command()
async def hOwner(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
--- 👑 ・ Owner Only ---
$selfbot       - Vezi lista de selfbots 
$selfbot [t][n]- Aduga Selfbot 
$selfbotr [Nr] - Scote selfbotu
```""", delete_after=30)

# 🤖 $ai [text] - Google Gemini
@bot.command()
async def ai(ctx, *, text):
    # Aici ar trebui să apelezi modelul generativ (ex: genai.generate_content)
    # Momentan edităm mesajul pentru a confirma primirea promptului
    await ctx.edit(content=f"🤖 **Gemini AI**: Procesez solicitarea pentru: `{text}`...")

# 🎨 $genimg [text] - Imagine AI (via Pollinations)
@bot.command()
async def genimg(ctx, *, text):
    prompt_url = text.replace(" ", "%20")
    link = f"https://pollinations.ai/p/{prompt_url}?width=1024&height=1024&nologo=true"
    await ctx.edit(content=f"🎨 **Imagine AI: `{text}`**\n{link}")

# 🧠 $brain [q] - Răspuns rapid (DuckDuckGo API)
@bot.command()
async def brain(ctx, *, q):
    try:
        r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json").json()
        ans = r.get("AbstractText", "Nu am găsit un răspuns rapid.")
        await ctx.edit(content=f"🧠 **Brain (DDG):** {ans[:1900]}")
    except:
        await ctx.edit(content="🧠 **Brain:** Eroare la procesarea cererii.")

# 🔍 $google [q] - Căutare Google
@bot.command()
async def google(ctx, *, q):
    query = q.replace(" ", "+")
    await ctx.edit(content=f"🔍 **Google Search:** https://www.google.com/search?q={query}")

# 🎥 $ytsearch [q] - Căutare YouTube
@bot.command()
async def ytsearch(ctx, *, q):
    query = q.replace(" ", "+")
    await ctx.edit(content=f"🎥 **YouTube Search:** https://www.youtube.com/results?search_query={query}")

# 📖 $wiki [q] - Wikipedia
@bot.command()
async def wiki(ctx, *, q):
    query = q.replace(" ", "_")
    await ctx.edit(content=f"📖 **Wikipedia:** https://ro.wikipedia.org/wiki/{query}")

# 👢 $kick @user
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.edit(content=f"👢 **{member}** a fost dat afară. Motiv: {reason}")

# 👢 $ban @user
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.edit(content=f"🔨 **{member}** a primit ban. Motiv: {reason}")

# 👢 $unban [id]
@bot.command()
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.edit(content=f"🔓 **{user}** a primit unban.")

# 🌊 $massunban - Debănează tot serverul
@bot.command()
async def massunban(ctx):
    ban_list = await ctx.guild.bans()
    for entry in ban_list:
        await ctx.guild.unban(entry.user)
    await ctx.edit(content="🌊 **Mass Unban completat!** Toți utilizatorii au fost debănați.")

# 🔄 $softban @user (Ban + Unban imediat pentru a șterge mesajele)
@bot.command()
async def softban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason, delete_message_days=7)
    await ctx.guild.unban(member)
    await ctx.edit(content=f"🔄 **Softban** aplicat lui {member}. Mesajele au fost șterse.")

# 🔇 $mute @user (Necesită un rol numit "Muted")
@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.edit(content=f"🔇 **{member}** a primit mute.")

# 🔊 $unmute @user
@bot.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.edit(content=f"🔊 **{member}** a primit unmute.")

# 🧹 $purge [nr] - Șterge mesajele TALE (Selfbot-ul nu poate șterge mesajele altora fără permisiuni)
@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=100):
        if amount <= 0: break
        if message.author == bot.user:
            await message.delete()
            amount -= 1

# 🧹 $purgeuser @user - Șterge mesajele unui user specific
@bot.command()
async def purgeuser(ctx, member: discord.Member, amount: int):
    async for message in ctx.channel.history(limit=100):
        if amount <= 0: break
        if message.author == member:
            await message.delete()
            amount -= 1
    await ctx.edit(content=f"🧹 Șterse {amount} mesaje ale lui {member}.", delete_after=3)

# ⏳ $slowmode [secunde]
@bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.edit(content=f"⏳ Slowmode setat la **{seconds}s**.")

# 🔒 $lock / $unlock
@bot.command()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.edit(content="🔒 Canal blocat.")

@bot.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.edit(content="🔓 Canal deblocat.")

# 💥 $nuke - Recreează canalul (șterge tot istoricul)
@bot.command()
async def nuke(ctx):
    pos = ctx.channel.position
    new_channel = await ctx.channel.clone()
    await ctx.channel.delete()
    await new_channel.edit(position=pos)
    await new_channel.send("💥 **Canalul a fost curățat prin nuke!**")


import random

# 😂 $meme / $joke / $quote / $fact
@bot.command()
async def meme(ctx):
    r = requests.get("https://meme-api.com/gimme").json()
    await ctx.edit(content=f"😂 **{r['title']}**\n{r['url']}")

@bot.command()
async def joke(ctx):
    r = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()
    joke_text = r.get("joke", "N-am găsit nicio glumă acum...")
    await ctx.edit(content=f"😂 **Joke:** {joke_text}")

@bot.command()
async def quote(ctx):
    r = requests.get("https://api.quotable.io/random").json()
    await ctx.edit(content=f"📜 \"{r['content']}\" — **{r['author']}**")

@bot.command()
async def fact(ctx):
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    await ctx.edit(content=f"🧠 **Fact:** {r['text']}")

# 🐱 $cat / $dog
@bot.command()
async def cat(ctx):
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    await ctx.edit(content=f"🐱 Poftim o pisică!\n{r[0]['url']}")

@bot.command()
async def dog(ctx):
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    await ctx.edit(content=f"🐶 Poftim un cățel!\n{r['message']}")

# 🔥 $howhot / $gay / $iq @user
@bot.command()
async def howhot(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = random.randint(0, 100)
    await ctx.edit(content=f"🔥 **{member.name}** este **{score}%** hot!")

@bot.command()
async def gay(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = random.randint(0, 100)
    await ctx.edit(content=f"🏳️‍🌈 **{member.name}** este **{score}%** gay!")

@bot.command()
async def iq(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = random.randint(50, 200)
    await ctx.edit(content=f"🧠 **{member.name}** are un IQ de **{score}**.")

# 🫂 $hug / $slap / $kill / $punch
@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.edit(content=f"🫂 {ctx.author.mention} îl îmbrățișează strâns pe {member.mention}!")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.edit(content=f"🖐️ {ctx.author.mention} i-a tras o palmă lui {member.mention}!")

@bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.edit(content=f"💀 {ctx.author.mention} l-a eliminat pe {member.mention} din joc!")

@bot.command()
async def punch(ctx, member: discord.Member):
    await ctx.edit(content=f"👊 {ctx.author.mention} i-a dat un pumn lui {member.mention}!")

# 🎁 $nitro (Fake Nitro Embed)
@bot.command()
async def nitro(ctx):
    await ctx.edit(content="**You've been gifted Nitro!**\nhttps://discord.gift/vK8pS7T2M5N4B6V9")

# 🎰 $slots
@bot.command()
async def slots(ctx):
    emojis = ["🍎", "🍊", "🍐", "🍋", "💎", "🎰"]
    a, b, c = random.choices(emojis, k=3)
    result = "AI CÂȘTIGAT! 🏆" if a == b == c else "Ai pierdut... 💸"
    await ctx.edit(content=f"🎰 **[ {a} | {b} | {c} ]** 🎰\n> {result}")

# 💣 $mines
@bot.command()
async def mines(ctx):
    grid = ["🟩", "🟩", "🟩", "🟩", "💣", "🟩", "🟩", "💣", "🟩"]
    random.shuffle(grid)
    display = f"{grid[0]}{grid[1]}{grid[2]}\n{grid[3]}{grid[4]}{grid[5]}\n{grid[6]}{grid[7]}{grid[8]}"
    await ctx.edit(content=f"💣 **Mines Game:**\n{display}\n*Noroc data viitoare!*")

import base64

# 🖼️ $avatar / $banner @user
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.edit(content=f"🖼️ **Avatarul lui {member.name}:**\n{member.avatar_url}")

@bot.command()
async def banner(ctx, member: discord.Member = None):
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        await ctx.edit(content=f"🖼️ **Bannerul lui {member.name}:**\n{user.banner.url}")
    else:
        await ctx.edit(content="❌ Acest utilizator nu are un banner.")

# 🏁 $qr [text] - Generează cod QR
@bot.command()
async def qr(ctx, *, text):
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text.replace(' ', '%20')}"
    await ctx.edit(content=f"🏁 **Cod QR pentru:** `{text}`\n{url}")

# 🌐 $ipinfo [ip] - Detalii despre un IP
@bot.command()
async def ipinfo(ctx, ip):
    r = requests.get(f"http://ip-api.com/json/{ip}").json()
    if r['status'] == 'fail':
        return await ctx.edit(content="❌ IP invalid.")
    info = f"🌐 **IP Info ({ip}):**\n📍 Locație: {r['city']}, {r['country']}\n🏢 ISP: {r['isp']}"
    await ctx.edit(content=info)

# 🔗 $shorten [url] - Scurtează un link (via TinyURL)
@bot.command()
async def shorten(ctx, url):
    r = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
    await ctx.edit(content=f"🔗 **Link scurtat:** {r.text}")

# 🌦️ $weather [city] - Vremea
@bot.command()
async def weather(ctx, *, city):
    # Folosim wttr.in (format imagine/text simplu pentru Discord)
    await ctx.edit(content=f"🌦️ **Vremea în {city}:**\nhttps://wttr.in/{city.replace(' ', '%20')}_py.png")

# 🪙 $crypto [coin] - Preț Crypto
@bot.command()
async def crypto(ctx, coin="bitcoin"):
    r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd").json()
    if coin.lower() in r:
        price = r[coin.lower()]['usd']
        await ctx.edit(content=f"🪙 **{coin.upper()}:** `${price:,}` USD")
    else:
        await ctx.edit(content="❌ Monedă negăsită.")

# 🔢 $math [expr] - Calculator
@bot.command()
async def math(ctx, *, expr):
    # Atenție: eval() poate fi periculos, dar într-un selfbot e de obicei ok
    try:
        res = eval(expr)
        await ctx.edit(content=f"🔢 **Rezultat:** `{expr} = {res}`")
    except:
        await ctx.edit(content="❌ Expresie matematică invalidă.")

# 📟 Convertori: Binary, Hex, Base64
@bot.command()
async def binary(ctx, *, text):
    res = ' '.join(format(ord(x), '08b') for x in text)
    await ctx.edit(content=f"📟 **Binary:** `{res}`")

@bot.command()
async def hex(ctx, *, text):
    res = text.encode('utf-8').hex()
    await ctx.edit(content=f"📟 **Hex:** `{res}`")

@bot.command()
async def b64(ctx, *, text):
    res = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    await ctx.edit(content=f"📟 **Base64:** `{res}`")

# ==========================================
# ✨ STATUS & SELF COMMANDS
# ==========================================

@bot.command()
async def stats(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(f"🎭 Status setat la: **{text}**", delete_after=5)

@bot.command()
async def live(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/redglitchx"))
    await ctx.send(f"💜 Status Live setat: **{text}**", delete_after=5)

@bot.command()
async def afk(ctx, *, reason="Nu sunt la tastatură"):
    await ctx.message.delete()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"AFK: {reason}"))
    await ctx.send(f"💤 Mod AFK activat: **{reason}**", delete_after=10)

@bot.command()
async def remstats(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None)
    await ctx.send("🗑️ Status a fost șters.", delete_after=5)

@bot.command()
async def restartstats(ctx):
    await ctx.message.delete()
    global start_time
    start_time = datetime.datetime.utcnow()
    await ctx.send("🔄 Uptime a fost resetat.", delete_after=5)

@bot.command()
async def ping(ctx):
    await ctx.edit(content=f"📡 **Pong!** `{round(bot.latency * 1000)}ms`")

@bot.command()
async def uptime(ctx):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.edit(content=f"📡 **Uptime:** `{hours}h {minutes}m {seconds}s`")

@bot.command()
async def typing(ctx, seconds: int):
    await ctx.message.delete()
    async with ctx.typing():
        await asyncio.sleep(seconds)

@bot.command()
async def watching(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    await ctx.send(f"👀 Watching: **{text}**", delete_after=5)

@bot.command()
async def listening(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    await ctx.send(f"🎧 Listening: **{text}**", delete_after=5)

@bot.command()
async def playing(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(f"🎮 Playing: **{text}**", delete_after=5)


# ☢️ $spam [nr] [msg]
@bot.command()
async def spam(ctx, amount: int, *, message):
    await ctx.message.delete()
    for _ in range(amount):
        await ctx.send(message)
        await asyncio.sleep(0.4)

# 👻 $ghostspam [nr]
@bot.command()
async def ghostspam(ctx, amount: int):
    await ctx.message.delete()
    for _ in range(amount):
        msg = await ctx.send("@everyone")
        await msg.delete()
        await asyncio.sleep(0.3)

# 🧨 $delchannels
@bot.command()
async def delchannels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except:
            continue

# 🧨 $delroles
@bot.command()
async def delroles(ctx):
    for role in ctx.guild.roles:
        try:
            await role.delete()
        except:
            continue

# ☣️ $masskick
@bot.command()
async def masskick(ctx):
    for member in ctx.guild.members:
        if member.id != bot.user.id:
            try:
                await member.kick()
            except:
                continue

# 🧬 $checktoken
@bot.command()
async def checktoken(ctx):
    u = bot.user
    nitro = "Da" if u.premium_type else "Nu"
    info = (
        f"🧬 **User:** `{u.name}`\n"
        f"🆔 **ID:** `{u.id}`\n"
        f"💎 **Nitro:** `{nitro}`\n"
        f"🛡️ **2FA:** `{u.mfa_enabled}`\n"
        f"📧 **Email:** `{getattr(u, 'email', 'N/A')}`"
    )
    await ctx.edit(content=info)

# 📜 $logchat
@bot.command()
async def logchat(ctx):
    log_file = f"log_{ctx.channel.id}.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        async for msg in ctx.channel.history(limit=100):
            f.write(f"[{msg.created_at}] {msg.author}: {msg.content}\n")
    await ctx.send(file=discord.File(log_file))

# 🚀 $webraid [msg]
@bot.command()
async def webraid(ctx, *, message):
    await ctx.message.delete()
    for channel in ctx.guild.text_channels:
        try:
            await channel.send(message)
        except:
            continue

# 👤 $whois / $perms / $created / $joined
@bot.command()
async def whois(ctx, member: discord.Member = None):
    member = member or ctx.author
    res = f"👤 **User:** {member.name}#{member.discriminator}\n🆔 **ID:** `{member.id}`\n📅 **Creat:** {member.created_at.strftime('%d/%m/%Y')}"
    await ctx.edit(content=res)

@bot.command()
async def perms(ctx, member: discord.Member = None):
    member = member or ctx.author
    p = [perm[0] for perm in member.guild_permissions if perm[1]]
    await ctx.edit(content=f"🛡️ **Permisiuni {member.name}:**\n`{', '.join(p)}`"[:1900])

@bot.command()
async def created(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.edit(content=f"📅 **Cont creat pe:** {member.created_at.strftime('%d/%m/%Y %H:%M')}")

@bot.command()
async def joined(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.edit(content=f"📥 **A intrat pe server pe:** {member.joined_at.strftime('%d/%m/%Y %H:%M')}")

# 🎭 $mock / $clap / $ascii / $reverse
@bot.command()
async def mock(ctx, *, text):
    res = "".join(list(map(lambda x: x.upper() if random.random() > 0.5 else x.lower(), text)))
    await ctx.edit(content=res)

@bot.command()
async def clap(ctx, *, text):
    await ctx.edit(content=text.replace(" ", " 👏 "))

# 💎 $aesthetic / $upper / $lower
@bot.command()
async def aesthetic(ctx, *, text):
    wide = "".join([chr(ord(c) + 0xFEE0) if 0x21 <= ord(c) <= 0x7E else c for c in text])
    await ctx.edit(content=wide)

@bot.command()
async def upper(ctx, *, text):
    await ctx.edit(content=text.upper())

@bot.command()
async def lower(ctx, *, text):
    await ctx.edit(content=text.lower())

# 🎨 $color [hex]
@bot.command()
async def color(ctx, hex_code):
    hex_code = hex_code.replace("#", "")
    url = f"https://singlecolorimge.com/get/{hex_code}/200x100"
    await ctx.edit(content=f"🎨 **Culoare: #{hex_code}**\n{url}")

# 🎲 $coinflip / $8ball / $dice
@bot.command()
async def coinflip(ctx):
    res = random.choice(["Cap", "Pajură"])
    await ctx.edit(content=f"🪙 **Rezultat:** {res}")

# 🧪 $pokedex / $anime / $steam
@bot.command()
async def pokedex(ctx, name):
    await ctx.edit(content=f"🧪 **PokeInfo:** https://pokeapi.co/api/v2/pokemon/{name.lower()}")

@bot.command()
async def steam(ctx, *, name):
    await ctx.edit(content=f"🎮 **Steam Search:** https://store.steampowered.com/search/?term={name.replace(' ', '+')}")

# 📱 $iphone [msg] - Notificare iPhone (via Image API)
@bot.command()
async def iphone(ctx, *, msg):
    url = f"https://api.popcat.xyz/iphone?text={msg.replace(' ', '%20')}"
    await ctx.edit(content=url)

# 🌫️ $blur @user
@bot.command()
async def blur(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    url = f"https://api.popcat.xyz/ad?image={avatar_url}" # Popcat are filtre faine
    await ctx.edit(content=f"🌫️ **Blur effect for {member.name}:**\nhttps://api.alexflipnote.dev/filter/blur?image={avatar_url}")

# 🌑 $gray @user
@bot.command()
async def gray(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    await ctx.edit(content=f"🌑 **Grayscale effect:**\nhttps://api.alexflipnote.dev/filter/grayscale?image={avatar_url}")

# 🌈 $invert @user
@bot.command()
async def invert(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    await ctx.edit(content=f"🌈 **Invert effect:**\nhttps://api.alexflipnote.dev/filter/invert?image={avatar_url}")

# 🧱 $pixelate @user
@bot.command()
async def pixelate(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    await ctx.edit(content=f"🧱 **Pixelate effect:**\nhttps://api.alexflipnote.dev/filter/pixelate?image={avatar_url}")

# 🎥 $youtubeavatar @user (Avatarul pus pe un comentariu de YT)
@bot.command()
async def youtubeavatar(ctx, member: discord.Member = None, *, text="Acesta este un comentariu genial!"):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    name = member.name.replace(" ", "%20")
    comment = text.replace(" ", "%20")
    url = f"https://some-random-api.com/canvas/misc/youtube-comment?avatar={avatar_url}&username={name}&comment={comment}"
    await ctx.edit(content=f"🎥 **YouTube Comment Style:**\n{url}")

# 🧪 $triggered @user
@bot.command()
async def triggered(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    url = f"https://some-random-api.com/canvas/overlay/triggered?avatar={avatar_url}"
    await ctx.edit(content=f"🧪 **TRIGGERED!**\n{url}")

# 📜 $wanted @user
@bot.command()
async def wanted(ctx, member: discord.Member = None):
    member = member or ctx.author
    avatar_url = member.avatar_url_as(format="png")
    url = f"https://api.popcat.xyz/wanted?image={avatar_url}"
    await ctx.edit(content=f"📜 **WANTED DEAD OR ALIVE:**\n{url}")

# 🌡️ $sysinfo - Info System (CPU, RAM, OS)
@bot.command()
async def sysinfo(ctx):
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    info = (
        f"💻 **System Info:**\n"
        f"🖥️ **OS:** `{platform.system()} {platform.release()}`\n"
        f"🧠 **CPU Load:** `{cpu}%`\n"
        f"📟 **RAM:** `{ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB`"
    )
    await ctx.edit(content=info)

# 🧠 $advice - Sfat random
@bot.command()
async def advice(ctx):
    r = requests.get("https://api.adviceslip.com/advice").json()
    msg = r['slip']['advice']
    await ctx.edit(content=f"🧠 **Advice:** {msg}")

# 🐱 $neko - Poze Anime Neko
@bot.command()
async def neko(ctx):
    r = requests.get("https://nekos.best/api/v2/neko").json()
    await ctx.edit(content=f"🐱 **Neko:**\n{r['results'][0]['url']}")

# 🔗 $steal [id] - Fură Emoji după ID (îl adaugă pe serverul curent)
@bot.command()
async def steal(ctx, emoji_id: int, *, name=None):
    name = name or f"stolen_emoji_{emoji_id}"
    url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    response = requests.get(url)
    if response.status_code == 200:
        emoji = await ctx.guild.create_custom_emoji(name=name, image=response.content)
        await ctx.edit(content=f"✅ Emoji-ul **{emoji}** a fost furat cu succes!")
    else:
        await ctx.edit(content="❌ Nu am putut găsi emoji-ul respectiv.")

# 📺 $vaporwave [text] - Text Vaporwave (Ｖａｐｏｒｗａｖｅ)
@bot.command()
async def vaporwave(ctx, *, text):
    res = "".join([chr(ord(c) + 0xFEE0) if 0x21 <= ord(c) <= 0x7E else c for c in text])
    await ctx.edit(content=f"📺 {res}")

# 🎫 $tokencheck [token] - Verifică validitate token
@bot.command()
async def tokencheck(ctx, token_to_check):
    headers = {"Authorization": token_to_check}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if r.status_code == 200:
        data = r.json()
        await ctx.edit(content=f"✅ **Token Valid!** User: `{data['username']}#{data['discriminator']}`")
    else:
        await ctx.edit(content="❌ **Token Invalid** sau expirat.")


# 🏠 $dsrv - Dump Server (Salvează structura)
@bot.command()
async def dsrv(ctx):
    data = {"name": ctx.guild.name, "roles": [], "categories": []}
    for role in reversed(ctx.guild.roles):
        if not role.is_default():
            data["roles"].append({"name": role.name, "color": role.color.value, "permissions": role.permissions.value})
    for category in ctx.guild.categories:
        cat_data = {"name": category.name, "channels": []}
        for channel in category.channels:
            chan_type = "text" if isinstance(channel, discord.TextChannel) else "voice"
            cat_data["channels"].append({"name": channel.name, "type": chan_type, "topic": getattr(channel, 'topic', None)})
        data["categories"].append(cat_data)
    with open(f"backup_{ctx.guild.id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    await ctx.edit(content=f"✅ Backup salvat: `backup_{ctx.guild.id}.json`")

# 📂 $lsrv - Listă backup-uri locale
@bot.command()
async def lsrv(ctx):
    files = [f for f in os.listdir('.') if f.startswith("backup_") and f.endswith(".json")]
    lista = "\n".join([f"- {f}" for f in files]) if files else "Niciun backup găsit."
    await ctx.edit(content=f"📂 **Backup-uri:**\n{lista}")

# 🏗️ $psrv [nume_fisier] - Aplică backup
@bot.command()
async def psrv(ctx, file_name: str):
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    await ctx.edit(content="🏗️ Se începe restaurarea...")
    for r_data in data["roles"]:
        try:
            await ctx.guild.create_role(name=r_data["name"], color=discord.Color(r_data["color"]), permissions=discord.Permissions(r_data["permissions"]))
            await asyncio.sleep(0.3)
        except: continue
    for c_data in data["categories"]:
        try:
            cat = await ctx.guild.create_category(name=c_data["name"])
            for ch_data in c_data["channels"]:
                if ch_data["type"] == "text":
                    await cat.create_text_channel(name=ch_data["name"], topic=ch_data["topic"])
                else:
                    await cat.create_voice_channel(name=ch_data["name"])
                await asyncio.sleep(0.5)
        except: continue
    await ctx.send("✅ Restaurare structură completă!")

# 🎵 VOICE & MUSIC

@bot.command()
async def plays(ctx, *, name):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        # Caută fișierul care conține numele în folderul 'music'
        for file in os.listdir("./music"):
            if name.lower() in file.lower():
                path = os.path.join("./music", file)
                await ctx.edit(content=f"🎵 **Playing:** `{file}`")
                vc.play(discord.FFmpegPCMAudio(path), after=lambda e: print(f'Finished: {e}'))
                return
        await ctx.edit(content="❌ Nu am găsit piesa respectivă.")
    else:
        await ctx.edit(content="❌ Trebuie să fii într-un canal vocal!")

@bot.command()
async def stops(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.edit(content="⏹️ Muzica a fost oprită și am părăsit canalul.")
    else:
        await ctx.edit(content="❌ Nu sunt conectat la niciun canal vocal.")

@bot.command()
async def downloadm(ctx, url):
    await ctx.edit(content="⏳ Se descarcă de pe YouTube... (Necesită yt-dlp)")
    # Comandă sistem pentru yt-dlp (trebuie să ai yt-dlp instalat: pip install yt-dlp)
    try:
        os.system(f'yt-dlp -x --audio-format mp3 -o "./music/%(title)s.%(ext)s" {url}')
        await ctx.edit(content="✅ Descărcare finalizată în folderul `/music`!")
    except Exception as e:
        await ctx.edit(content=f"❌ Eroare la descărcare: {e}")

@bot.command()
async def dwnlibs(ctx):
    files = [f for f in os.listdir("./music") if f.endswith(".mp3")]
    if not files:
        return await ctx.edit(content="📂 Biblioteca este goală.")
    
    lista = "\n".join([f"- {f}" for f in files[:15]]) # Limităm la primele 15
    await ctx.edit(content=f"📂 **Piese salvate:**\n{lista}")

@bot.command()
async def adfiles(ctx):
    if not ctx.message.attachments:
        return await ctx.edit(content="❌ Atașează un fișier MP3 la mesaj!")
    
    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".mp3"):
            await attachment.save(f"./music/{attachment.filename}")
            await ctx.edit(content=f"✅ Salvat: `{attachment.filename}`")
            return
    await ctx.edit(content="❌ Fișierul trebuie să fie format MP3.")

# ✉️ SPAM BOT
is_spamming = False

@bot.command()
async def start(ctx, member: discord.Member):
    global is_spamming
    is_spamming = True
    await ctx.message.delete()
    if not os.path.exists("botjura.txt"):
        return await ctx.send("❌ Fișierul `botjura.txt` nu există!")
    with open("botjura.txt", "r", encoding="utf-8") as f:
        linii = f.readlines()
    for linie in linii:
        if not is_spamming: break
        if linie.strip():
            await ctx.send(f"{member.mention} {linie.strip()}")
            await asyncio.sleep(0.4)

@bot.command()
async def stop(ctx):
    global is_spamming
    is_spamming = False
    await ctx.edit(content="🛑 Spam oprit.")

# 👤 PROFILE ARCHIVER
@bot.command()
async def prfdwn(ctx, member: discord.Member):
    if not os.path.exists("profiles"): os.makedirs("profiles")
    data = f"User: {member}\nID: {member.id}\nCreat: {member.created_at}\nAvatar: {member.avatar_url}"
    with open(f"profiles/{member.name}.txt", "w", encoding="utf-8") as f:
        f.write(data)
    await ctx.edit(content=f"📥 Profil salvat: `profiles/{member.name}.txt`")

@bot.command()
async def prflist(ctx):
    if not os.path.exists("profiles"): return await ctx.edit(content="📂 Folder gol.")
    files = os.listdir("profiles")
    res = "\n".join([f"{i+1}. {f.replace('.txt', '')}" for i, f in enumerate(files)])
    await ctx.edit(content=f"👤 **Arhivă Profile:**\n{res}")

@bot.command()
async def show(ctx, nr: int):
    files = os.listdir("profiles")
    if 0 < nr <= len(files):
        with open(f"profiles/{files[nr-1]}", "r", encoding="utf-8") as f:
            data = f.read()
        await ctx.edit(content=f"📄 **Profil ({files[nr-1].replace('.txt', '')}):**\n{data}")
    else:
        await ctx.edit(content="❌ Număr invalid.")

# 📂 COPIERE & ARHIVARE
@bot.command()
async def clchat(ctx, nr: int):
    log = []
    async for m in ctx.channel.history(limit=nr):
        line = f"[{m.author}] {m.content}"
        if m.attachments: line += f" | Media: {m.attachments[0].url}"
        log.append(line)
    filename = f"copy_{ctx.channel.id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(reversed(log)))
    await ctx.edit(content=f"📂 Copiat `{nr}` mesaje în `{filename}`")

@bot.command()
async def clist(ctx):
    files = [f for f in os.listdir('.') if f.startswith("copy_")]
    res = "\n".join(files) if files else "Niciun chat copiat."
    await ctx.edit(content=f"📋 **Clipuri:**\n{res}")

@bot.command()
async def pstchat(ctx, file_name):
    if not os.path.exists(file_name): return await ctx.edit(content="❌ Fișierul nu există.")
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            await ctx.send(line.strip())
            await asyncio.sleep(0.7)

# 🛡️ MODUL BP2
protection = {"kick": False, "ban": False}

@bot.command(name="anti-kick")
async def antikick(ctx):
    protection["kick"] = not protection["kick"]
    await ctx.edit(content=f"🛡️ Anti-Kick: {'ON' if protection['kick'] else 'OFF'}")

@bot.command(name="anti-ban")
async def antiban(ctx):
    protection["ban"] = not protection["ban"]
    await ctx.edit(content=f"🛡️ Anti-Ban: {'ON' if protection['ban'] else 'OFF'}")

@bot.command()
async def ghostping(ctx, member: discord.Member):
    await ctx.message.delete()
    m = await ctx.send(member.mention)
    await m.delete()



# IMPORTANT: Folosim {} pentru că active_selfbots este un DICȚIONAR (stochează Nume: Date)
active_selfbots = {} 

# 👑 $selfbot - Vezi lista / Adaugă & Pornește
@bot.command()
async def selfbot(ctx, token: str = None, name: str = None):
    # Verifică dacă OWNER_ID este definit undeva mai sus în main.py
    if ctx.author.id != OWNER_ID:
        return

    # Afișare Listă Verticală
    if token is None:
        header = "👑 **Owner | RedGlitchX**\n\n**Lista:**"
        if not active_selfbots:
            return await ctx.edit(content=f"{header}\n*(Niciun alt selfbot activ)*")
        
        # Aici folosim .keys(), deci variabila trebuia să fie {}
        lista_verticala = "\n".join([f"👤 {n}" for n in active_selfbots.keys()])
        await ctx.edit(content=f"{header}\n{lista_verticala}")

    # Adăugare și Pornire automată
    else:
        bot_name = name if name else f"Bot_{len(active_selfbots) + 1}"
        if bot_name in active_selfbots:
            return await ctx.edit(content=f"❌ Numele `{bot_name}` este ocupat.")

        await ctx.edit(content=f"⏳ Se pornește `{bot_name}`...")

        def start_bot(tkn):
            # Atenție: 'self_bot=True' funcționează doar pe anumite versiuni de discord.py/discord.py-self
            new_bot = commands.Bot(command_prefix=bot.command_prefix, self_bot=True)
            try:
                # bot=False este esențial pentru self-bots pe librării vechi
                new_bot.run(tkn, bot=False)
            except Exception as e:
                print(f"Eroare la pornirea botului {bot_name}: {e}")

        tr = threading.Thread(target=start_bot, args=(token,))
        tr.daemon = True # Recomandat: thread-ul moare dacă procesul principal se oprește
        tr.start()
        
        # Salvăm datele în dicționar
        active_selfbots[bot_name] = {"token": token, "thread": tr}
        await ctx.send(f"🚀 **{bot_name}** a intrat online!")

# 👑 $selfbotr [Nume] - Scoate din listă
@bot.command()
async def selfbotr(ctx, name: str):
    if ctx.author.id != OWNER_ID:
        return
    if name in active_selfbots:
        active_selfbots.pop(name)
        await ctx.edit(content=f"🗑️ `{name}` a fost eliminat din monitorizare.")
    else:
        await ctx.edit(content="❌ Numele nu există în listă.")
        

# ==========================================
# 🚀 PORNIRE AUTOMATĂ
# ==========================================

@bot.event
async def on_ready():
    print("----------------------------")
    print(f"✅ LOGAT CA: {bot.user.name}")
    print(f"🤖 GEMINI AI: {'ACTIVAT' if GEMINI_KEY else 'DEZACTIVAT'}")
    print("----------------------------")

if __name__ == "__main__":
    if TOKEN:
        try:
            # Pornim folosind variabila TOKEN luată din Render
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ EROARE: {e}")
    else:
        print("❌ EROARE: Render nu a găsit 'DISCORD_TOKEN' în Environment Variables!")
        
