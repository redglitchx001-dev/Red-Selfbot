import discord
from discord.ext import commands
import os
import asyncio
import aiohttp
import requests
import json
import time
import sys
import platform
import base64
from io import BytesIO
from PIL import Image, ImageFilter
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Botul e viu!"

def run():
    # Render îți dă portul automat prin variabila de sistem PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Luăm tokenele. Dacă nu găsește nimic, punem un text gol "" în loc de None
TOKEN = os.getenv("TOKEN", "")

# Verificăm dacă TOKEN are ceva în el înainte să dăm split
if TOKEN:
    TOKEN_LIST = [t.strip() for t in TOKEN.split(",") if t.strip()]
else:
    TOKEN_LIST = []
    print("❌ EROARE: Nu am găsit niciun token în Environment Variables!")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

bot = commands.Bot(command_prefix="$", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# --- HELP MENUS ---

@bot.command()
async def redhelp(ctx):
    await ctx.message.delete()
    help_text = """```text
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
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hAI(ctx):
    await ctx.message.delete()
    help_text = """```text
🤖 ・ AI & INTELLIGENCE:
🤖 ・ $ai [text]     - Google Gemini AI
🎨 ・ $genimg [text] - Imagine AI
🧠 ・ $brain [q]     - Răspuns rapid (DDG)
🔍 ・ $google [q]    - Căutare Google
🎥 ・ $yts [q]       - Căutare YouTube
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hM(ctx):
    await ctx.message.delete()
    help_text = """```text
🛡️ ・ MODERATION & SERVER:
👢 ・ $kick @u / $ban @u / $unban [id]
🌊 ・ $massunban     - Debănează tot serverul
🔄 ・ $softban @u    - Ban & Unban rapid
🔇 ・ $mute @u / $unmute @u
💥 ・ $nuke          - Șterge și recreează canalul
🔒 ・ $lock / $unlock - Blochează canalul
⏳ ・ $slowmode [s]  - Setează slowmode
🧹 ・ $purge [n]     - Șterge mesajele tale
🧹 ・ $purgeuser @u [n] - Șterge mesajele unui user
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hgame(ctx):
    await ctx.message.delete()
    help_text = """```text
🎮 ・ GAMES & FUN:
😂 ・ $meme / $joke / $quote / $fact
🐱 ・ $cat / $dog    - Poze animale
🔥 ・ $howhot @u / $gay @u / $iq @u
🫂 ・ $hug @u / $slap @u / $kill @u / $punch @u
🎁 ・ $nitro        - Fake Nitro gift
🎰 ・ $slots        - Joc de păcănele
💣 ・ $mines        - Joc de mine
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hutils(ctx):
    await ctx.message.delete()
    help_text = """```text
🛠️ ・ UTILS & TOOLS:
👤 ・ $av @u / $banner @u
🪙 ・ $crypto [coin] - Preț crypto
📟 ・ $64 [text]    - Base64 encode
🧮 ・ $calc [expr]  - Calculator
🔗 ・ $firstmsg     - Primul mesaj din canal
👤 ・ $joinedat @u  - Data intrării pe server
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hstatus(ctx):
    await ctx.message.delete()
    help_text = """```text
✨ ・ STATUS & SELFBOT:
✨ ・ $stats [text]  - Setează status custom
💜 ・ $live [text]   - Status Streaming
👀 ・ $watching [text] - Status Watching
👂 ・ $listening [text] - Status Listening
🎮 ・ $playing [text] - Status Playing
🗑️ ・ $remstats      - Șterge statusul
💤 ・ $afk [reason]  - Setează AFK
📡 ・ $ping / $uptime - Info bot
⌨️ ・ $typing [s]    - Fake typing
🔄 ・ $restartstats  - Resetează statisticile
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hadv(ctx):
    await ctx.message.delete()
    help_text = """```text
🚀 ・ ADVANCED & SPECIAL:
🔥 ・ $spam [n] [msg] - Spam mesaje
🗑️ ・ $delchannels   - Șterge toate canalele
🗑️ ・ $delroles      - Șterge toate rolurile
👢 ・ $masskick      - Kick la toți membrii
🧬 ・ $checktoken    - Info despre token
📟 ・ $password [len] - Generează parolă
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hImage(ctx):
    await ctx.message.delete()
    help_text = """```text
💎 ・ IMAGE PROCESSING:
🌫️ ・ $blur @u       - Avatar blurat
🌈 ・ $invert @u     - Avatar inversat
👾 ・ $pixelate @u   - Avatar pixelat
🎥 ・ $youtubeavatar @u - Avatar stil YT
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

@bot.command()
async def hSys(ctx):
    await ctx.message.delete()
    help_text = """```text
💻 ・ SYSTEM & NEW FUN:
🌡️ ・ $sysinfo       - Info sistem
🐱 ・ $neko          - Poze anime neko
🧬 ・ $tokencheck    - Verifică token-ul
🏗️ ・ $psrv          - Server Cloner (Stub)
📥 ・ $downloadm [url] - Downloader media
```"""
    msg = await ctx.send(help_text)
    await asyncio.sleep(60)
    try: await msg.delete()
    except: pass

# --- AI COMMANDS ---

@bot.command()
async def ai(ctx, *, prompt):
    if not GEMINI_API_KEY:
        await ctx.send("❌ Gemini API Key is not configured.")
        return
    try:
        model = genai.GenerativeModel("gemini-3.1-pro-preview")
        response = model.generate_content(prompt)
        await ctx.send(f"🤖 **Gemini AI:**\n{response.text}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def genimg(ctx, *, prompt):
    if not GEMINI_API_KEY:
        await ctx.send("❌ Gemini API Key is not configured.")
        return
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-image")
        response = model.generate_content(prompt)
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                img_data = base64.b64decode(part.inline_data.data)
                with BytesIO(img_data) as img_bin:
                    await ctx.send(file=discord.File(img_bin, "genimg.png"))
                return
        await ctx.send("❌ No image generated.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# --- MODERATION ---

@bot.command()
async def kick(ctx, member: discord.Member):
    await ctx.message.delete()
    try:
        await member.kick()
        await ctx.send(f"✅ Kicked {member}")
    except:
        await ctx.send("❌ Failed to kick.")

@bot.command()
async def ban(ctx, member: discord.Member):
    await ctx.message.delete()
    try:
        await member.ban(delete_message_days=7, reason="Banned by selfbot")
        await ctx.send(f"✅ Banned {member}")
    except:
        await ctx.send("❌ Failed to ban.")

@bot.command()
async def unban(ctx, user_id: int):
    await ctx.message.delete()
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user}")
    except:
        await ctx.send("❌ Failed to unban.")

@bot.command()
async def massunban(ctx):
    await ctx.message.delete()
    bans = await ctx.guild.bans()
    for ban_entry in bans:
        await ctx.guild.unban(ban_entry.user)
    await ctx.send(f"✅ Mass unbanned {len(bans)} users.")

@bot.command()
async def softban(ctx, member: discord.Member):
    await ctx.message.delete()
    try:
        await member.ban(delete_message_days=7, reason="Softban")
        await ctx.guild.unban(member)
        await ctx.send(f"✅ Softbanned {member}")
    except:
        await ctx.send("❌ Failed to softban.")

@bot.command()
async def mute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"✅ Muted {member}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"✅ Unmuted {member}")

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    channel = ctx.channel
    pos = channel.position
    new_channel = await channel.clone()
    await channel.delete()
    await new_channel.edit(position=pos)
    await new_channel.send("💥 **Channel Nuked.**")

@bot.command()
async def lock(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **Channel Locked.**")

@bot.command()
async def unlock(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 **Channel Unlocked.**")

@bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏳ **Slowmode set to {seconds}s.**")

@bot.command()
async def purge(ctx, amount: int = 10):
    await ctx.message.delete()
    def is_me(m): return m.author == bot.user
    deleted = await ctx.channel.purge(limit=amount, check=is_me)
    msg = await ctx.send(f"🧹 **Purged {len(deleted)} messages.**")
    await asyncio.sleep(5)
    await msg.delete()

@bot.command()
async def purgeuser(ctx, member: discord.Member, amount: int = 10):
    await ctx.message.delete()
    def is_user(m): return m.author == member
    deleted = await ctx.channel.purge(limit=amount, check=is_user)
    msg = await ctx.send(f"🧹 **Purged {len(deleted)} messages from {member}.**")
    await asyncio.sleep(5)
    await msg.delete()

# --- FUN ---

@bot.command()
async def meme(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as r:
            data = await r.json()
            await ctx.send(data["url"])

@bot.command()
async def joke(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://official-joke-api.appspot.com/random_joke") as r:
            data = await r.json()
            await ctx.send(f"😂 **Joke:** {data['setup']}\n{data['punchline']}")

@bot.command()
async def quote(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.quotable.io/random") as r:
            data = await r.json()
            await ctx.send(f"📜 **Quote:** \"{data['content']}\" - {data['author']}")

@bot.command()
async def fact(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as r:
            data = await r.json()
            await ctx.send(f"💡 **Fact:** {data['text']}")

@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as r:
            data = await r.json()
            await ctx.send(data[0]["url"])

@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://dog.ceo/api/breeds/image/random") as r:
            data = await r.json()
            await ctx.send(data["message"])

@bot.command()
async def howhot(ctx, member: discord.Member = None):
    member = member or ctx.author
    import random
    hot = random.randint(0, 100)
    await ctx.send(f"🔥 **{member} is {hot}% hot!**")

@bot.command()
async def gay(ctx, member: discord.Member = None):
    member = member or ctx.author
    import random
    gay = random.randint(0, 100)
    await ctx.send(f"🌈 **{member} is {gay}% gay!**")

@bot.command()
async def iq(ctx, member: discord.Member = None):
    member = member or ctx.author
    import random
    iq = random.randint(50, 200)
    await ctx.send(f"🧠 **{member} has {iq} IQ!**")

@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🫂 **{bot.user} hugs {member}!**")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.send(f"🫂 **{bot.user} slaps {member}!**")

@bot.command()
async def kill(ctx, member: discord.Member):
    await ctx.send(f"🫂 **{bot.user} killed {member}!**")

@bot.command()
async def punch(ctx, member: discord.Member):
    await ctx.send(f"🫂 **{bot.user} punched {member}!**")

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()
    await ctx.send("🎁 **You've been gifted Nitro!**\nhttps://discord.gift/fake-nitro-code")

@bot.command()
async def slots(ctx):
    import random
    emojis = ["🍎", "🍊", "🍇", "🍒", "💎"]
    a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    win = a == b == c
    await ctx.send(f"🎰 **Slots:** [ {a} | {b} | {c} ]\n{'✅ **You won!**' if win else '❌ **You lost.**'}")

@bot.command()
async def mines(ctx):
    import random
    grid = ["🟦"] * 25
    mines = random.sample(range(25), 5)
    for m in mines: grid[m] = "💣"
    display = "\n".join([" ".join(grid[i:i+5]) for i in range(0, 25, 5)])
    await ctx.send(f"💣 **Mines:**\n{display}")

# --- UTILS ---

@bot.command()
async def av(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar_url)

@bot.command()
async def banner(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        await ctx.send(user.banner.url)
    else:
        await ctx.send("No banner.")

@bot.command()
async def crypto(ctx, coin="bitcoin"):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd") as r:
            data = await r.json()
            if coin in data:
                await ctx.send(f"🪙 **{coin.upper()}:** ${data[coin]['usd']}")
            else:
                await ctx.send("❌ Coin not found.")

@bot.command()
async def calc(ctx, *, expr):
    try:
        # Simple eval for math
        res = eval(expr, {"__builtins__": None}, {})
        await ctx.send(f"🧮 **Result:** {res}")
    except:
        await ctx.send("❌ Invalid expression.")

@bot.command()
async def firstmsg(ctx):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=1, oldest_first=True):
        await ctx.send(f"🔗 **First Message:** {message.jump_url}")

@bot.command()
async def joinedat(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"👤 **{member} joined at:** {member.joined_at.strftime('%Y-%m-%d')}")

# --- STATUS ---

@bot.command()
async def stats(ctx, *, text):
    await bot.change_presence(activity=discord.CustomActivity(name=text))
    await ctx.send(f"✨ **Status set to:** {text}")

@bot.command()
async def live(ctx, *, text):
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/redglitch"))
    await ctx.send(f"💜 **Streaming:** {text}")

@bot.command()
async def watching(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    await ctx.send(f"👀 **Watching:** {text}")

@bot.command()
async def listening(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    await ctx.send(f"👂 **Listening to:** {text}")

@bot.command()
async def playing(ctx, *, text):
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(f"🎮 **Playing:** {text}")

@bot.command()
async def remstats(ctx):
    await bot.change_presence(activity=None)
    await ctx.send("🗑️ **Status removed.**")

@bot.command()
async def afk(ctx, *, reason="No reason."):
    await ctx.send(f"💤 **AFK:** {reason}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"📡 **Ping:** {round(bot.latency * 1000)}ms")

@bot.command()
async def uptime(ctx):
    import time
    uptime = time.time() - start_time
    hours, rem = divmod(uptime, 3600)
    minutes, seconds = divmod(rem, 60)
    await ctx.send(f"📡 **Uptime:** {int(hours)}h {int(minutes)}m {int(seconds)}s")

@bot.command()
async def typing(ctx, seconds: int = 10):
    async with ctx.typing():
        await asyncio.sleep(seconds)

# --- ADVANCED ---

@bot.command()
async def spam(ctx, amount: int, *, msg):
    await ctx.message.delete()
    for _ in range(amount):
        await ctx.send(msg)

@bot.command()
async def delchannels(ctx):
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass

@bot.command()
async def delroles(ctx):
    await ctx.message.delete()
    for role in ctx.guild.roles:
        try: await role.delete()
        except: pass

@bot.command()
async def masskick(ctx):
    await ctx.message.delete()
    for member in ctx.guild.members:
        try: await member.kick()
        except: pass

@bot.command()
async def checktoken(ctx):
    await ctx.message.delete()
    await ctx.send(f"🧬 **Token Info:**\n**User:** {bot.user}\n**ID:** {bot.user.id}")

@bot.command()
async def password(ctx, length: int = 16):
    import string
    import random
    chars = string.ascii_letters + string.digits + string.punctuation
    res = "".join(random.choice(chars) for _ in range(length))
    await ctx.send(f"📟 **Password:** `{res}`")

# --- IMAGE ---

@bot.command()
async def blur(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.avatar_url_as(format="png", size=512))) as r:
            img_data = await r.read()
            img = Image.open(BytesIO(img_data))
            img = img.filter(ImageFilter.GaussianBlur(radius=10))
            with BytesIO() as img_bin:
                img.save(img_bin, "PNG")
                img_bin.seek(0)
                await ctx.send(file=discord.File(img_bin, "blur.png"))

@bot.command()
async def invert(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    from PIL import ImageOps
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.avatar_url_as(format="png", size=512))) as r:
            img_data = await r.read()
            img = Image.open(BytesIO(img_data)).convert("RGB")
            img = ImageOps.invert(img)
            with BytesIO() as img_bin:
                img.save(img_bin, "PNG")
                img_bin.seek(0)
                await ctx.send(file=discord.File(img_bin, "invert.png"))

# --- LOGICA DE PORNIRE (MULTI-ACCOUNT) ---

@bot.event
async def on_ready():
    print(f"✅ Logat ca: {bot.user.name} (ID: {bot.user.id})")
    print(f"🚀 Prefix: {bot.command_prefix}")
    print("---")

if __name__ == "__main__":
    # 1. Pornim Web Server-ul (dacă ai funcția keep_alive definită)
    if 'keep_alive' in globals():
        keep_alive()

    # 2. Împărțim variabila TOKEN în bucăți (cele 25 de tokene)
    # TOKEN conține acum: "tk1,tk2,tk3..."
    TOKEN_LIST = [t.strip() for t in TOKEN.split(",") if t.strip()]
    
    print(f"📦 Am detectat {len(TOKEN_LIST)} tokene în variabila TOKEN.")

    # 3. Luăm fiecare token la rând
    for i, tk in enumerate(TOKEN_LIST):
        try:
            print(f"🔄 [Cont {i+1}] Se încearcă logarea...")
            # Rulăm botul. Am scos 'bot=False' ca să nu dea eroare de argument
            bot.run(tk) 
        except discord.errors.LoginFailure:
            print(f"⚠️ [Cont {i+1}] TOKEN INVALID/EXPIRAT! Sar peste el...")
            continue # ASTA previne "Crashed State" pe Spaceify
        except Exception as e:
            print(f"❌ [Cont {i+1}] Eroare neașteptată: {e}")
            continue
            
