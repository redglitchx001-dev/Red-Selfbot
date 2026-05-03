import discord
from discord.ext import commands
import os
import asyncio
import aiohttp
import json
import time
import random
import string
import io
import qrcode
import psutil
import platform
from datetime import datetime
from PIL import Image, ImageFilter, ImageOps
from dotenv import load_dotenv
import google.generativeai as genai
import yt_dlp
import base64
import codecs
import math
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Botul este online!"

def run():
    # Render caută portul 10000 implicit
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Șterge tot ce ține de intents și folosește doar asta:
bot = commands.Bot(command_prefix="$", self_bot=True, intents=None)
bot.remove_command('help')

start_time = time.time()
afk_status = {}
voice_clients = {}

@bot.event
async def on_ready():
    print(f'[+] Selfbot active! Logged in as {bot.user}')
    print(f'[+] User ID: {bot.user.id}')
    print(f'[+] Servers: {len(bot.guilds)}')
    print(f'[+] Prefix: $')
    print(f'[+] Commands loaded: {len(bot.commands)}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f'Error: {error}')

# ==================== HELP COMMANDS ====================

@bot.command()
async def REDHELP(ctx):
    await ctx.message.edit(content="""```text
--- 📋 ・ MENIU CENTRAL AJUTOR ---
🤖 ・ $hAI - AI & Intelligence
🛡️ ・ $hM - Moderation & Server
🎮 ・ $hgame - Games & Fun
🛠️ ・ $hutils - Utils & Tools
✨ ・ $hstatus - Status & Selfbot
🔥 ・ $hT7 - Tier 7 (Extreme)
🌟 ・ $hXtra - Extra & New Ideas
💎 ・ $hImage - Image Processing
💻 ・ $hSys - System & New Fun
🏰 ・ $hClon - Server Cloner
🎵 ・ $helpvc - Voice & Music Master
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hAI(ctx):
    await ctx.message.edit(content="""```text
🤖 ・ AI & INTELLIGENCE:
🤖 ・ $ai [text]     - Google Gemini AI
🎨 ・ $genimg [text] - Imagine AI
🧠 ・ $brain [q]     - Răspuns rapid (DDG)
🔍 ・ $google [q]    - Căutare Google
🎥 ・ $ytsearch [q]  - Căuta pe YouTube
📖 ・ $wiki [q]      - Wikipedia
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hM(ctx):
    await ctx.message.edit(content="""```text
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
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hgame(ctx):
    await ctx.message.edit(content="""```text
🎮 ・ GAMES & FUN:
😂 ・ $meme / $joke / $quote / $fact
🐱 ・ $cat / $dog    - Poze animale
🔥 ・ $howhot / $gay / $iq @user
🫂 ・ $hug / $slap / $kill / $punch
🎁 ・ $nitro         - Nitro Fake Embed
🎰 ・ $slots / $mines- Jocuri noroc
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hutils(ctx):
    await ctx.message.edit(content="""```text
🛠️ ・ UTILS & TOOLS:
🖼️ ・ $avatar / $banner @user
🏁 ・ $qr [text]     - Generează cod QR
🌐 ・ $ipinfo [ip]   - Detalii despre un IP
🔗 ・ $shorten [url] - Scurtează un link
🌦️ ・ $weather [city]- Vremea oraș
🪙 ・ $crypto [coin] - Preț Crypto (BTC)
🔢 ・ $math [expr]   - Calculator
📟 ・ $binary / $hex / $64 / $morse
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hstatus(ctx):
    await ctx.message.edit(content="""```text
✨ ・ STATUS & SELF:
🎭 ・ $stats [text]  - Status custom
💜 ・ $live [text]   - Status streaming
💤 ・ $afk [reason]  - Setează AFK
🗑️ ・ $remstats      - Șterge status
🔄 ・ $restartstats  - Reset uptime
📡 ・ $ping / $uptime / $typing [sec]
👀 ・ $watching / $listening / $playing
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hT7(ctx):
    await ctx.message.edit(content="""```text
🔥 ・ TIER 7 (EXTREME):
☢️ ・ $spam [nr] [msg]- Spam rapid
👻 ・ $ghostspam [nr]- Spam cu ștergere
🧨 ・ $delchannels   - Șterge TOATE canalele
🧨 ・ $delroles      - Șterge TOATE rolurile
☣️ ・ $masskick      - Kick la TOȚI membrii
🧬 ・ $checktoken    - Info brute despre cont
📜 ・ $logchat       - Salvează mesaje canal
🚀 ・ $webraid [msg] - Toate conturile trimit mesaj
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hXtra(ctx):
    await ctx.message.edit(content="""```text
🌟 ・ EXTRA & IDEAS:
👤 ・ $whois / $perms / $created / $joined
🎭 ・ $mock / $clap / $ascii / $reverse
💎 ・ $aesthetic / $upper / $lower
📟 ・ $password [n]  - Generare parolă
🎨 ・ $color [hex]   - Vezi o culoare
🎲 ・ $coinflip / $8ball / $dice
🧪 ・ $pokedex / $anime / $steam
📱 ・ $iphone [msg]  - Notificare iPhone
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hImage(ctx):
    await ctx.message.edit(content="""```text
💎 ・ IMAGE PROCESSING:
🌫️ ・ $blur @u       - Avatar blurat
🌑 ・ $gray @u       - Avatar alb-negru
🌈 ・ $invert @u     - Culori inversate
🧱 ・ $pixelate @u   - Pixelat
🎥 ・ $youtubeavatar - Avatar pe YouTube
🧪 ・ $triggered @u  - Efect triggered
📜 ・ $wanted @u     - Efect wanted
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hSys(ctx):
    await ctx.message.edit(content="""```text
💻 ・ SYSTEM & NEW FUN:
🌡️ ・ $sysinfo      - Info System
🧠 ・ $advice       - Sfat random
🐱 ・ $neko         - Poze Anime Neko
🔗 ・ $steal [id]   - Fură Emoji după ID
📺 ・ $vaporwave [t]- Text Vaporwave
🎫 ・ $tokencheck   - Verifică validitate token
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def hClon(ctx):
    await ctx.message.edit(content="""```text
🏰 ・ SERVER CLONER:
🏠 ・ $dsrv      - Dump Server (Salvează structura)
📂 ・ $lsrv      - Listă backup-uri locale
🏗️ ・ $psrv [nr] - Aplică backup pe server curent
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

@bot.command()
async def helpvc(ctx):
    await ctx.message.edit(content="""```text
🎵 ・ VOICE & MUSIC:
$plays [nr/nume]- Redă piesa din folderul music
$stops          - Oprește muzica și ieși din VC
$downloadm [url]- Descarcă de pe YouTube
$dwnlibs        - Vezi lista de piese salvate
$adfiles        - Salvează MP3 din atașament
```""")
    await asyncio.sleep(60)
    await ctx.message.delete()

# ==================== AI COMMANDS ====================

@bot.command()
async def ai(ctx, *, text):
    await ctx.message.delete()
    if not GEMINI_API_KEY:
        return await ctx.send("❌ GEMINI_API_KEY not configured!", delete_after=5)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        
        result = response.text[:2000] if len(response.text) > 2000 else response.text
        embed = discord.Embed(title="🤖 Gemini AI", description=result, color=0x00ff00)
        embed.set_footer(text=f"Asked by {ctx.author}")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}", delete_after=5)

@bot.command()
async def genimg(ctx, *, prompt):
    await ctx.message.delete()
    await ctx.send(f"🎨 Generating image for: **{prompt}**\n_Feature requires external API integration_", delete_after=10)

@bot.command()
async def brain(ctx, *, query):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.duckduckgo.com/?q={query}&format=json") as resp:
            data = await resp.json()
            answer = data.get('AbstractText', 'No results found.')
            await ctx.send(f"🧠 **Answer:** {answer[:2000]}")

@bot.command()
async def google(ctx, *, query):
    await ctx.message.delete()
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    await ctx.send(f"🔍 **Google Search:** {url}")

@bot.command()
async def ytsearch(ctx, *, query):
    await ctx.message.delete()
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    await ctx.send(f"🎥 **YouTube Search:** {url}")

@bot.command()
async def wiki(ctx, *, query):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                extract = data.get('extract', 'No information found.')
                embed = discord.Embed(title=data.get('title', query), description=extract[:2000], color=0xffffff)
                embed.set_thumbnail(url=data.get('thumbnail', {}).get('source', ''))
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ No Wikipedia article found.", delete_after=5)

# ==================== MODERATION COMMANDS ====================

@bot.command()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await ctx.message.delete()
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked **{member}** | Reason: {reason}", delete_after=5)
    except:
        await ctx.send("❌ Failed to kick member.", delete_after=5)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await ctx.message.delete()
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member}** | Reason: {reason}", delete_after=5)
    except:
        await ctx.send("❌ Failed to ban member.", delete_after=5)

@bot.command()
async def unban(ctx, user_id: int):
    await ctx.message.delete()
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned **{user}**", delete_after=5)
    except:
        await ctx.send("❌ Failed to unban user.", delete_after=5)

@bot.command()
async def massunban(ctx):
    await ctx.message.delete()
    unbanned = 0
    async for ban_entry in ctx.guild.bans():
        try:
            await ctx.guild.unban(ban_entry.user)
            unbanned += 1
        except:
            pass
    await ctx.send(f"🌊 Mass unbanned **{unbanned}** users.", delete_after=10)

@bot.command()
async def softban(ctx, member: discord.Member):
    await ctx.message.delete()
    try:
        await member.ban(reason="Softban")
        await member.unban(reason="Softban")
        await ctx.send(f"🔄 Softbanned **{member}**", delete_after=5)
    except:
        await ctx.send("❌ Failed to softban.", delete_after=5)

@bot.command()
async def mute(ctx, member: discord.Member):
    await ctx.message.delete()
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f"🔇 Muted **{member}**", delete_after=5)

@bot.command()
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role:
        await member.remove_roles(muted_role)
        await ctx.send(f"🔊 Unmuted **{member}**", delete_after=5)

@bot.command()
async def purge(ctx, amount: int = 100):
    await ctx.message.delete()
    deleted = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == ctx.author:
            try:
                await message.delete()
                deleted += 1
                await asyncio.sleep(0.5)
            except:
                pass
    await ctx.send(f"🧹 Deleted **{deleted}** of your messages.", delete_after=5)

@bot.command()
async def purgeuser(ctx, member: discord.Member, amount: int = 100):
    await ctx.message.delete()
    deleted = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == member:
            try:
                await message.delete()
                deleted += 1
                await asyncio.sleep(0.5)
            except:
                pass
    await ctx.send(f"🧹 Deleted **{deleted}** messages from {member.mention}.", delete_after=5)

@bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏳ Slowmode set to **{seconds}** seconds.", delete_after=5)
    except:
        await ctx.send("❌ Failed to set slowmode.", delete_after=5)

@bot.command()
async def lock(ctx):
    await ctx.message.delete()
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked.", delete_after=5)
    except:
        await ctx.send("❌ Failed to lock channel.", delete_after=5)

@bot.command()
async def unlock(ctx):
    await ctx.message.delete()
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Channel unlocked.", delete_after=5)
    except:
        await ctx.send("❌ Failed to unlock channel.", delete_after=5)

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    try:
        channel = ctx.channel
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.send("💥 Channel nuked and recreated!")
    except:
        pass

# ==================== GAMES & FUN ====================

@bot.command()
async def meme(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as resp:
            data = await resp.json()
            embed = discord.Embed(title=data['title'], color=0xff6600)
            embed.set_image(url=data['url'])
            await ctx.send(embed=embed)

@bot.command()
async def joke(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://official-joke-api.appspot.com/random_joke") as resp:
            data = await resp.json()
            await ctx.send(f"😂 {data['setup']}\n||{data['punchline']}||")

@bot.command()
async def quote(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.quotable.io/random") as resp:
            data = await resp.json()
            await ctx.send(f"💬 *\"{data['content']}\"* - {data['author']}")

@bot.command()
async def fact(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as resp:
            data = await resp.json()
            await ctx.send(f"📚 {data['text']}")

@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
            data = await resp.json()
            embed = discord.Embed(title="🐱 Random Cat", color=0xffa500)
            embed.set_image(url=data[0]['url'])
            await ctx.send(embed=embed)

@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://dog.ceo/api/breeds/image/random") as resp:
            data = await resp.json()
            embed = discord.Embed(title="🐶 Random Dog", color=0xffa500)
            embed.set_image(url=data['message'])
            await ctx.send(embed=embed)

@bot.command()
async def howhot(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    hotness = random.randint(0, 100)
    await ctx.send(f"🔥 **{member.display_name}** is **{hotness}%** hot!")

@bot.command()
async def gay(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    gayness = random.randint(0, 100)
    await ctx.send(f"🏳️‍🌈 **{member.display_name}** is **{gayness}%** gay!")

@bot.command()
async def iq(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    iq_score = random.randint(50, 200)
    await ctx.send(f"🧠 **{member.display_name}**'s IQ is **{iq_score}**!")

@bot.command()
async def hug(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member:
        await ctx.send(f"🫂 **{ctx.author.display_name}** hugged **{member.display_name}**!")
    else:
        await ctx.send(f"🫂 **{ctx.author.display_name}** hugged the air... awkward!")

@bot.command()
async def slap(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member:
        await ctx.send(f"👋 **{ctx.author.display_name}** slapped **{member.display_name}**!")
    else:
        await ctx.send(f"👋 **{ctx.author.display_name}** slapped themselves... ouch!")

@bot.command()
async def kill(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member:
        await ctx.send(f"💀 **{ctx.author.display_name}** killed **{member.display_name}**!")
    else:
        await ctx.send(f"💀 **{ctx.author.display_name}** committed suicide... bruh!")

@bot.command()
async def punch(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member:
        await ctx.send(f"👊 **{ctx.author.display_name}** punched **{member.display_name}**!")
    else:
        await ctx.send(f"👊 **{ctx.author.display_name}** punched the wall!")

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description="You've been gifted Nitro for **1 month**!",
        color=0xff73fa
    )
    embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")
    await ctx.send(embed=embed)

@bot.command()
async def slots(ctx):
    await ctx.message.delete()
    emojis = ["🍒", "🍊", "🍋", "🍇", "💎", "7️⃣"]
    result = [random.choice(emojis) for _ in range(3)]
    if result[0] == result[1] == result[2]:
        outcome = "🎉 JACKPOT! You won!"
    else:
        outcome = "😔 You lost! Try again."
    await ctx.send(f"🎰 | {' | '.join(result)} | 🎰\n{outcome}")

@bot.command()
async def mines(ctx):
    await ctx.message.delete()
    board = ["💎" if random.random() > 0.5 else "💣" for _ in range(9)]
    result = " ".join(board[:3]) + "\n" + " ".join(board[3:6]) + "\n" + " ".join(board[6:])
    await ctx.send(f"💎 **MINES GAME:**\n{result}")

# ==================== UTILS COMMANDS ====================

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=member.color)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def banner(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        embed = discord.Embed(title=f"{member.display_name}'s Banner", color=member.color)
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ No banner set.", delete_after=5)

@bot.command()
async def qr(ctx, *, text):
    await ctx.message.delete()
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='qr.png'))

@bot.command()
async def ipinfo(ctx, ip: str):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as resp:
            data = await resp.json()
            if data['status'] == 'success':
                embed = discord.Embed(title=f"🌐 IP Info: {ip}", color=0x00ff00)
                embed.add_field(name="Country", value=data['country'], inline=True)
                embed.add_field(name="City", value=data['city'], inline=True)
                embed.add_field(name="ISP", value=data['isp'], inline=False)
                embed.add_field(name="Timezone", value=data['timezone'], inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Invalid IP address.", delete_after=5)

@bot.command()
async def shorten(ctx, url: str):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://tinyurl.com/api-create.php?url={url}") as resp:
            short_url = await resp.text()
            await ctx.send(f"🔗 **Shortened URL:** {short_url}")

@bot.command()
async def weather(ctx, *, city: str):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://wttr.in/{city}?format=j1") as resp:
            if resp.status == 200:
                data = await resp.json()
                current = data['current_condition'][0]
                embed = discord.Embed(title=f"🌦️ Weather in {city}", color=0x00bfff)
                embed.add_field(name="Temperature", value=f"{current['temp_C']}°C", inline=True)
                embed.add_field(name="Feels Like", value=f"{current['FeelsLikeC']}°C", inline=True)
                embed.add_field(name="Condition", value=current['weatherDesc'][0]['value'], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ City not found.", delete_after=5)

@bot.command()
async def crypto(ctx, coin: str = "bitcoin"):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd") as resp:
            data = await resp.json()
            if coin in data:
                price = data[coin]['usd']
                await ctx.send(f"🪙 **{coin.capitalize()}** price: **${price:,.2f}** USD")
            else:
                await ctx.send("❌ Coin not found.", delete_after=5)

@bot.command()
async def math(ctx, *, expression: str):
    await ctx.message.delete()
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        await ctx.send(f"🔢 **Result:** {result}")
    except:
        await ctx.send("❌ Invalid expression.", delete_after=5)

@bot.command()
async def binary(ctx, *, text: str):
    await ctx.message.delete()
    binary = ' '.join(format(ord(char), '08b') for char in text)
    await ctx.send(f"📟 **Binary:** {binary[:2000]}")

@bot.command()
async def hex(ctx, *, text: str):
    await ctx.message.delete()
    hex_text = text.encode().hex()
    await ctx.send(f"📟 **Hex:** {hex_text[:2000]}")

@bot.command(name='64')
async def base64_encode(ctx, *, text: str):
    await ctx.message.delete()
    encoded = base64.b64encode(text.encode()).decode()
    await ctx.send(f"📟 **Base64:** {encoded[:2000]}")

@bot.command()
async def morse(ctx, *, text: str):
    await ctx.message.delete()
    morse_dict = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----'}
    morse = ' '.join(morse_dict.get(char.upper(), char) for char in text)
    await ctx.send(f"📟 **Morse:** {morse[:2000]}")

# ==================== STATUS COMMANDS ====================

@bot.command()
async def stats(ctx, *, text: str):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(f"🎭 Status changed to: **{text}**", delete_after=5)

@bot.command()
async def live(ctx, *, text: str):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/discord"))
    await ctx.send(f"💜 Now streaming: **{text}**", delete_after=5)

@bot.command()
async def watching(ctx, *, text: str):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    await ctx.send(f"👀 Now watching: **{text}**", delete_after=5)

@bot.command()
async def listening(ctx, *, text: str):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    await ctx.send(f"🎧 Now listening to: **{text}**", delete_after=5)

@bot.command()
async def playing(ctx, *, text: str):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(f"🎮 Now playing: **{text}**", delete_after=5)

@bot.command()
async def afk(ctx, *, reason: str = "AFK"):
    await ctx.message.delete()
    afk_status[ctx.author.id] = reason
    await ctx.send(f"💤 You are now AFK: **{reason}**", delete_after=5)

@bot.command()
async def remstats(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None)
    await ctx.send("🗑️ Status removed.", delete_after=5)

@bot.command()
async def restartstats(ctx):
    await ctx.message.delete()
    global start_time
    start_time = time.time()
    await ctx.send("🔄 Uptime reset.", delete_after=5)

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    latency = round(bot.latency * 1000)
    await ctx.send(f"📡 **Pong!** Latency: {latency}ms", delete_after=5)

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"⏰ **Uptime:** {hours}h {minutes}m {seconds}s", delete_after=10)

@bot.command()
async def typing(ctx, seconds: int = 5):
    await ctx.message.delete()
    async with ctx.typing():
        await asyncio.sleep(seconds)

# ==================== TIER 7 COMMANDS ====================

@bot.command()
async def spam(ctx, amount: int, *, message: str):
    await ctx.message.delete()
    for _ in range(min(amount, 50)):
        await ctx.send(message)
        await asyncio.sleep(0.5)

@bot.command()
async def ghostspam(ctx, amount: int):
    await ctx.message.delete()
    for _ in range(min(amount, 20)):
        msg = await ctx.send("👻")
        await asyncio.sleep(0.3)
        await msg.delete()

@bot.command()
async def delchannels(ctx):
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except:
            pass

@bot.command()
async def delroles(ctx):
    await ctx.message.delete()
    for role in ctx.guild.roles:
        try:
            if role != ctx.guild.default_role:
                await role.delete()
        except:
            pass

@bot.command()
async def masskick(ctx):
    await ctx.message.delete()
    for member in ctx.guild.members:
        try:
            if member != ctx.author:
                await member.kick()
        except:
            pass

@bot.command()
async def checktoken(ctx):
    await ctx.message.delete()
    user = bot.user
    embed = discord.Embed(title="🧬 Token Information", color=0xff0000)
    embed.add_field(name="Username", value=f"{user.name}#{user.discriminator}", inline=False)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Friends", value="N/A", inline=True)
    await ctx.send(embed=embed, delete_after=30)

@bot.command()
async def logchat(ctx, limit: int = 100):
    await ctx.message.delete()
    messages = []
    async for message in ctx.channel.history(limit=limit):
        messages.append(f"[{message.created_at}] {message.author}: {message.content}")
    
    with open(f"chat_log_{ctx.channel.id}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(reversed(messages)))
    
    await ctx.send(file=discord.File(f"chat_log_{ctx.channel.id}.txt"))
    os.remove(f"chat_log_{ctx.channel.id}.txt")

@bot.command()
async def webraid(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(f"🚀 Raid message: **{message}**\n_Multi-account feature requires additional setup_", delete_after=10)

# ==================== EXTRA COMMANDS ====================

@bot.command()
async def whois(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member}", color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=" ".join([role.mention for role in member.roles[1:]]) or "None", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def perms(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    perms = [perm[0].replace("_", " ").title() for perm in member.guild_permissions if perm[1]]
    await ctx.send(f"🔐 **{member.display_name}'s Permissions:**\n{', '.join(perms[:20])}")

@bot.command()
async def created(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(f"📅 **{member.display_name}** created their account on: **{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}**")

@bot.command()
async def joined(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(f"📅 **{member.display_name}** joined this server on: **{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}**")

@bot.command()
async def mock(ctx, *, text: str):
    await ctx.message.delete()
    mocked = ''.join(char.upper() if i % 2 else char.lower() for i, char in enumerate(text))
    await ctx.send(mocked)

@bot.command()
async def clap(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(' 👏 '.join(text.split()))

@bot.command()
async def ascii(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(f"```{text}```")

@bot.command()
async def reverse(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text[::-1])

@bot.command()
async def aesthetic(ctx, *, text: str):
    await ctx.message.delete()
    aesthetic = ' '.join(text)
    await ctx.send(aesthetic)

@bot.command()
async def upper(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text.upper())

@bot.command()
async def lower(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text.lower())

@bot.command()
async def password(ctx, length: int = 16):
    await ctx.message.delete()
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(min(length, 128)))
    await ctx.author.send(f"🔐 Generated password: `{password}`")
    await ctx.send("✅ Password sent to DMs!", delete_after=5)

@bot.command()
async def color(ctx, hex_color: str):
    await ctx.message.delete()
    if not hex_color.startswith('#'):
        hex_color = '#' + hex_color
    try:
        embed = discord.Embed(title=f"🎨 Color: {hex_color}", color=int(hex_color[1:], 16))
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Invalid hex color.", delete_after=5)

@bot.command()
async def coinflip(ctx):
    await ctx.message.delete()
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 **{result}!**")

@bot.command(name='8ball')
async def eightball(ctx, *, question: str):
    await ctx.message.delete()
    responses = ["Yes", "No", "Maybe", "Definitely", "Absolutely not", "Ask again later", "I don't think so", "Of course!"]
    await ctx.send(f"🎱 **{random.choice(responses)}**")

@bot.command()
async def dice(ctx):
    await ctx.message.delete()
    result = random.randint(1, 6)
    await ctx.send(f"🎲 You rolled a **{result}**!")

@bot.command()
async def iphone(ctx, *, message: str):
    await ctx.message.delete()
    embed = discord.Embed(title="iPhone", description=message, color=0x000000)
    embed.set_author(name="Discord", icon_url="https://i.imgur.com/oBPXx0D.png")
    await ctx.send(embed=embed)

# ==================== IMAGE PROCESSING ====================

async def get_avatar_image(member):
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.display_avatar.url)) as resp:
            data = await resp.read()
            return Image.open(io.BytesIO(data)).convert('RGB')

@bot.command()
async def blur(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    img = await get_avatar_image(member)
    img = img.filter(ImageFilter.GaussianBlur(10))
    
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        output.seek(0)
        await ctx.send(file=discord.File(output, 'blur.png'))

@bot.command()
async def gray(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    img = await get_avatar_image(member)
    img = ImageOps.grayscale(img)
    
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        output.seek(0)
        await ctx.send(file=discord.File(output, 'gray.png'))

@bot.command()
async def invert(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    img = await get_avatar_image(member)
    img = ImageOps.invert(img)
    
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        output.seek(0)
        await ctx.send(file=discord.File(output, 'invert.png'))

@bot.command()
async def pixelate(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    img = await get_avatar_image(member)
    small = img.resize((32, 32), resample=Image.BILINEAR)
    img = small.resize(img.size, Image.NEAREST)
    
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        output.seek(0)
        await ctx.send(file=discord.File(output, 'pixelate.png'))

@bot.command()
async def youtubeavatar(ctx):
    await ctx.message.delete()
    await ctx.send(f"🎥 YouTube Avatar: https://www.youtube.com/watch?v=dQw4w9WgXcQ", delete_after=10)

@bot.command()
async def triggered(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(f"🧪 Triggered effect for {member.mention} (requires advanced image processing)")

@bot.command()
async def wanted(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(f"📜 Wanted poster for {member.mention} (requires advanced image processing)")

# ==================== SYSTEM COMMANDS ====================

@bot.command()
async def sysinfo(ctx):
    await ctx.message.delete()
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    embed = discord.Embed(title="🌡️ System Information", color=0x00ff00)
    embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}", inline=False)
    embed.add_field(name="CPU Usage", value=f"{cpu_percent}%", inline=True)
    embed.add_field(name="RAM Usage", value=f"{ram.percent}%", inline=True)
    embed.add_field(name="Disk Usage", value=f"{disk.percent}%", inline=True)
    embed.add_field(name="Python", value=platform.python_version(), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def advice(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.adviceslip.com/advice") as resp:
            data = await resp.json()
            await ctx.send(f"🧠 {data['slip']['advice']}")

@bot.command()
async def neko(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://nekos.best/api/v2/neko") as resp:
            data = await resp.json()
            embed = discord.Embed(title="🐱 Neko", color=0xff69b4)
            embed.set_image(url=data['results'][0]['url'])
            await ctx.send(embed=embed)

@bot.command()
async def steal(ctx, emoji_id: int):
    await ctx.message.delete()
    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    await ctx.send(f"🔗 Emoji URL: {emoji_url}")

@bot.command()
async def vaporwave(ctx, *, text: str):
    await ctx.message.delete()
    vaporwave = text.translate(str.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'))
    await ctx.send(vaporwave)

@bot.command()
async def tokencheck(ctx):
    await ctx.message.delete()
    await ctx.send("🎫 Token is valid! ✅", delete_after=5)

# ==================== SERVER CLONER ====================

@bot.command()
async def dsrv(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    
    backup_data = {
        'name': guild.name,
        'icon': str(guild.icon.url) if guild.icon else None,
        'channels': [],
        'roles': []
    }
    
    for role in guild.roles:
        backup_data['roles'].append({
            'name': role.name,
            'color': role.color.value,
            'permissions': role.permissions.value
        })
    
    for channel in guild.channels:
        backup_data['channels'].append({
            'name': channel.name,
            'type': str(channel.type),
            'position': channel.position
        })
    
    os.makedirs('backups', exist_ok=True)
    filename = f"backups/backup_{guild.id}_{int(time.time())}.json"
    
    with open(filename, 'w') as f:
        json.dump(backup_data, f, indent=4)
    
    await ctx.send(f"🏠 Server backup saved: `{filename}`", delete_after=10)

@bot.command()
async def lsrv(ctx):
    await ctx.message.delete()
    os.makedirs('backups', exist_ok=True)
    backups = [f for f in os.listdir('backups') if f.endswith('.json')]
    
    if backups:
        backup_list = '\n'.join([f"{i+1}. {f}" for i, f in enumerate(backups)])
        await ctx.send(f"📂 **Available backups:**\n```{backup_list}```", delete_after=30)
    else:
        await ctx.send("❌ No backups found.", delete_after=5)

@bot.command()
async def psrv(ctx, backup_number: int):
    await ctx.message.delete()
    backups = [f for f in os.listdir('backups') if f.endswith('.json')]
    
    if 0 < backup_number <= len(backups):
        filename = f"backups/{backups[backup_number - 1]}"
        with open(filename, 'r') as f:
            backup_data = json.load(f)
        
        await ctx.send(f"🏗️ Restoring backup: `{backups[backup_number - 1]}`...", delete_after=5)
        await ctx.send("⚠️ Backup restoration is a destructive operation. Feature requires careful implementation.", delete_after=10)
    else:
        await ctx.send("❌ Invalid backup number.", delete_after=5)

# ==================== VOICE & MUSIC ====================

@bot.command()
async def plays(ctx, *, song):
    await ctx.message.delete()
    
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        
        if ctx.guild.id in voice_clients:
            vc = voice_clients[ctx.guild.id]
        else:
            vc = await channel.connect()
            voice_clients[ctx.guild.id] = vc
        
        music_folder = 'music'
        os.makedirs(music_folder, exist_ok=True)
        
        music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        
        if song.isdigit():
            index = int(song) - 1
            if 0 <= index < len(music_files):
                song_path = os.path.join(music_folder, music_files[index])
                vc.play(discord.FFmpegPCMAudio(song_path))
                await ctx.send(f"🎵 Now playing: **{music_files[index]}**", delete_after=10)
            else:
                await ctx.send("❌ Invalid song number.", delete_after=5)
        else:
            matching = [f for f in music_files if song.lower() in f.lower()]
            if matching:
                song_path = os.path.join(music_folder, matching[0])
                vc.play(discord.FFmpegPCMAudio(song_path))
                await ctx.send(f"🎵 Now playing: **{matching[0]}**", delete_after=10)
            else:
                await ctx.send("❌ Song not found.", delete_after=5)
    else:
        await ctx.send("❌ You must be in a voice channel!", delete_after=5)

@bot.command()
async def stops(ctx):
    await ctx.message.delete()
    
    if ctx.guild.id in voice_clients:
        vc = voice_clients[ctx.guild.id]
        await vc.disconnect()
        del voice_clients[ctx.guild.id]
        await ctx.send("⏹️ Stopped and disconnected.", delete_after=5)
    else:
        await ctx.send("❌ Not connected to voice.", delete_after=5)

@bot.command()
async def downloadm(ctx, url: str):
    await ctx.message.delete()
    
    try:
        os.makedirs('music', exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'music/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            await ctx.send(f"✅ Downloaded: **{info['title']}**", delete_after=10)
    except Exception as e:
        await ctx.send(f"❌ Download failed: {str(e)}", delete_after=10)

@bot.command()
async def dwnlibs(ctx):
    await ctx.message.delete()
    os.makedirs('music', exist_ok=True)
    music_files = [f for f in os.listdir('music') if f.endswith('.mp3')]
    
    if music_files:
        file_list = '\n'.join([f"{i+1}. {f}" for i, f in enumerate(music_files)])
        await ctx.send(f"🎵 **Downloaded songs:**\n```{file_list[:1900]}```", delete_after=30)
    else:
        await ctx.send("❌ No songs in library.", delete_after=5)

@bot.command()
async def adfiles(ctx):
    await ctx.message.delete()
    
    if ctx.message.attachments:
        os.makedirs('music', exist_ok=True)
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.mp3'):
                await attachment.save(f"music/{attachment.filename}")
                await ctx.send(f"✅ Saved: **{attachment.filename}**", delete_after=5)
            else:
                await ctx.send("❌ Only MP3 files allowed.", delete_after=5)
    else:
        await ctx.send("❌ No files attached.", delete_after=5)

# ======================== START BOT ========================

if __name__ == '__main__':
    # AICI e buba: Folosește variabila TOKEN (cea definită sus cu os.getenv)
    if not TOKEN: 
        print('❌ Error: TOKEN is empty! Check Render Environment Variables.')
        exit()

    try:
        # Pornim serverul web pe fundal
        keep_alive()
        print("✅ Web server pornit pe portul 10000")
        
        # Pornim botul folosind variabila care conține codul tău
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        
