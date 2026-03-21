# -*- coding: utf-8 -*-
import sys, os, asyncio, json, random, time, datetime, requests, base64, re
import discord
from discord.ext import commands

# --- CONFIGURARE ---
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.G4Aq81.g1mMCVdL2bCL3DQa9m5eq0f0OH6TeocoB5pxgg")
GEMINI_API_KEY = os.getenv("GEMINI", "AIzaSyCilFHONVZu2nWiONpeFfNt7UEZT0ckGaE")
PREFIX = "$"
START_TIME = time.time()

bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)

# ==========================================
# --- 📋 MENIURI HELP (Emoji ・ text) ---
# ==========================================

@bot.command()
async def REDHELP(ctx):
    await ctx.message.delete()
    menu = """```text
--- 📋 ・ MENIU CENTRAL AJUTOR ---

🤖 ・ $hAI     - AI & Intelligence
🛡️ ・ $hM      - Moderation & Server
🎮 ・ $hgame   - Games & Fun
🛠️ ・ $hutils  - Utils & Tools
✨ ・ $hstatus - Status & Selfbot
🚀 ・ $hadv    - Advanced & Special
🔥 ・ $hT7     - Tier 7 (Extreme)

⚙️ ・ ADMIN: $restartstats, $showtoken
```"""
    await ctx.send(menu, delete_after=60)

@bot.command()
async def hAI(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🤖 ・ AI & INTELLIGENCE:
🤖 ・ $ai [text]     - Întreabă Google Gemini
🎨 ・ $genimg [text] - Generează imagine AI
🧠 ・ $brain [q]     - Răspuns enciclopedic rapid
🔍 ・ $google [q]    - Căutare rapidă Google
🎥 ・ $ytsearch [q]  - Căutare pe YouTube
📖 ・ $wiki [q]      - Căutare pe Wikipedia
```""", delete_after=60)

@bot.command()
async def hM(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🛡️ ・ MODERATION & SERVER:
👢 ・ $kick @user    - Dă afară un membru
🔨 ・ $ban @user     - Banează un membru
🔓 ・ $unban [id]    - Scoate ban-ul după ID
🌊 ・ $massunban     - Debanează pe toată lumea
🔄 ・ $softban @user - Ban + Unban rapid
🔇 ・ $mute @user    - Pune mute (necesită rol Muted)
🔊 ・ $unmute @user  - Scoate mute
🧹 ・ $purge [nr]    - Șterge X mesaje (ale tale)
⏳ ・ $slowmode [s]  - Setează slowmode canal
🔒 ・ $lock          - Blocare canal
🔓 ・ $unlock        - Deblocare canal
💥 ・ $nuke          - Șterge și recreează canalul
➕ ・ $masschannel   - Creează 10 canale rapid
🏷️ ・ $massrole      - Creează 10 roluri rapid
```""", delete_after=60)

@bot.command()
async def hgame(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🎮 ・ GAMES & FUN:
😂 ・ $meme          - Arată un meme random
🤡 ・ $joke          - Spune o glumă
📜 ・ $quote         - Arată un citat celebru
💡 ・ $fact          - Un fapt interesant
🐱 ・ $cat / $dog    - Poze cu animale
🔥 ・ $howhot @user  - Cât de hot ești?
🫂 ・ $hug @user     - Îmbrățișare
👊 ・ $slap @user    - Palmă
💀 ・ $kill @user    - Omoară (textual)
🥊 ・ $punch @user   - Boxează
🎁 ・ $nitro         - Generează cod Nitro fake
🏳️‍🌈 ・ $gay @user     - Cât de gay ești?
🧠 ・ $iq @user      - Test IQ rapid
❤️ ・ $ship @u1 @u2  - Test de dragoste
🎰 ・ $slots         - Joc de păcănele
💣 ・ $mines [nr]    - Joc de mine (5x5)
```""", delete_after=60)

@bot.command()
async def hutils(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🛠️ ・ UTILS & TOOLS:
🖼️ ・ $avatar @user  - Vezi avatarul cuiva
🚩 ・ $banner @user  - Vezi bannerul cuiva
🏁 ・ $qr [text]     - Generează cod QR
🌐 ・ $ipinfo [ip]   - Detalii despre un IP
🔗 ・ $shorten [url] - Scurtează un link
🌦️ ・ $weather [city]- Vremea în orașul X
🪙 ・ $crypto [coin] - Preț crypto actual
🔢 ・ $math [expr]   - Calculator matematic
📟 ・ $binary [text] - Conversie Binar
📟 ・ $hex [text]    - Conversie Hex
📟 ・ $64 [text]     - Conversie Base64
📟 ・ $morse [text]  - Conversie Morse
🅰️ ・ $bold [text]   - Formatare Bold
```""", delete_after=60)

@bot.command()
async def hstatus(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
✨ ・ STATUS & UTIL:
🎭 ・ $stats [text]  - Setează status custom
💜 ・ $live [text]   - Setează status streaming
💤 ・ $afk [reason]  - Setează status AFK
🗑️ ・ $remstats      - Șterge statusul actual
🔄 ・ $restartstats  - Resetează uptime-ul
👀 ・ $watching [t]  - Status Watching
🎧 ・ $listening [t] - Status Listening
🎮 ・ $playing [t]   - Status Playing
📡 ・ $ping          - Vezi latența botului
🚀 ・ $uptime        - Timp de funcționare
⌨️ ・ $typing [sec]  - Fake typing status
```""", delete_after=60)

@bot.command()
async def hadv(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🚀 ・ ADVANCED & SPECIAL:
🤌 ・ $steal [emoji] - Link imagine emoji
📖 ・ $urban [word]  - Urban Dictionary
⏰ ・ $timer [s]     - Setează un cronometru
🧹 ・ $purgeuser @u  - Șterge msjele unui user
🖼️ ・ $servericon    - Vezi poza serverului
🖼️ ・ $serverbanner  - Vezi bannerul serverului
👻 ・ $ghostping @u  - Ping discret (delete)
🕵️ ・ $secret [text] - Mesaj ascuns (spoiler)
🏷️ ・ $nick [nume]   - Schimbă nickname-ul tău
🚩 ・ $hypesquad [h] - Schimbă casa (bravery, etc)
💢 ・ $triggered @u  - Efect triggered avatar
🕵️ ・ $wanted @u     - Efect wanted avatar
🔑 ・ $showtoken     - Vezi token-ul contului
```""", delete_after=60)

@bot.command()
async def hT7(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🔥 ・ TIER 7 (EXTREME):
☢️ ・ $spam [nr] [msg]- Spam mesaje rapid
👻 ・ $ghostspam [nr]- Spam cu ștergere instantă
🧨 ・ $delchannels   - Șterge TOATE canalele
🧨 ・ $delroles      - Șterge TOATE rolurile
☣️ ・ $masskick      - Kick la TOȚI membrii
🧬 ・ $checktoken    - Info complete cont (API)
📜 ・ $logall        - Salvează ultimele 100 msje
```""", delete_after=60)

# ==========================================
# --- 🤖 IMPLEMENTARE AI & INTELLIGENCE ---
# ==========================================

@bot.command()
async def ai(ctx, *, prompt):
    await ctx.message.delete()
    if GEMINI_API_KEY == "CHEIA_GEMINI_AICI": return await ctx.send("❌ Pune API Key Gemini!")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        await ctx.send(f"🤖 **Gemini AI:** {r['candidates'][0]['content']['parts'][0]['text'][:1900]}")
    except: await ctx.send("❌ Eroare API Gemini.")

@bot.command()
async def genimg(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🎨 **Genereat:** https://pollinations.ai/p/{q.replace(' ', '%20')}")

@bot.command()
async def brain(ctx, *, q):
    await ctx.message.delete()
    r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json").json()
    await ctx.send(f"🧠 **Brain:** {r.get('AbstractText', 'Nu știu asta.')[:1000]}")

@bot.command()
async def google(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🔍 https://www.google.com/search?q={q.replace(' ', '+')}")

@bot.command()
async def ytsearch(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🎥 https://www.youtube.com/results?search_query={q.replace(' ', '+')}")

@bot.command()
async def wiki(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"📖 https://en.wikipedia.org/wiki/{q.replace(' ', '_')}")

# ==========================================
# --- 🛡️ IMPLEMENTARE MODERARE ---
# ==========================================

@bot.command()
async def kick(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.kick()

@bot.command()
async def ban(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.ban()

@bot.command()
async def unban(ctx, user_id: int):
    await ctx.message.delete()
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)

@bot.command()
async def massunban(ctx):
    await ctx.message.delete()
    bans = await ctx.guild.bans()
    for b in bans: await ctx.guild.unban(b.user)

@bot.command()
async def softban(ctx, member: discord.Member):
    await ctx.message.delete()
    await member.ban(delete_message_days=7)
    await ctx.guild.unban(member)

@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    async for m in ctx.channel.history(limit=amount):
        if m.author == bot.user: await m.delete()

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    new = await ctx.channel.clone()
    await ctx.channel.delete()
    await new.send("💥 **Canal Nuked!**")

@bot.command()
async def masschannel(ctx):
    await ctx.message.delete()
    for i in range(10): await ctx.guild.create_text_channel(name=f"red-bot-{i}")

@bot.command()
async def massrole(ctx):
    await ctx.message.delete()
    for i in range(10): await ctx.guild.create_role(name=f"RedRole-{i}")

@bot.command()
async def lock(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

@bot.command()
async def unlock(ctx):
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

# ==========================================
# --- 🎮 IMPLEMENTARE GAMES & FUN ---
# ==========================================

@bot.command()
async def meme(ctx):
    await ctx.message.delete()
    r = requests.get("https://meme-api.com/gimme").json()
    await ctx.send(r['url'])

@bot.command()
async def joke(ctx):
    await ctx.message.delete()
    r = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()
    await ctx.send(f"🤡 {r.get('joke', 'N-am glume azi.')}")

@bot.command()
async def fact(ctx):
    await ctx.message.delete()
    r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    await ctx.send(f"💡 {r['text']}")

@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    await ctx.send(r[0]['url'])

@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    await ctx.send(r['message'])

@bot.command()
async def mines(ctx, bombs: int = 5):
    await ctx.message.delete()
    grid = ["⬛"] * 25
    for _ in range(bombs): grid[random.randint(0, 24)] = "💣"
    res = "".join(grid[i] + ("\n" if (i+1)%5==0 else " ") for i in range(25))
    await ctx.send(f"💣 **Mines:**\n{res}")

@bot.command()
async def slots(ctx):
    await ctx.message.delete()
    a,b,c = random.choices("🍎💎🍒🍋🍀", k=3)
    res = "🎉 WIN!" if a==b==c else "💀 LOSE."
    await ctx.send(f"🎰 **[ {a} | {b} | {c} ]**\n{res}")

@bot.command()
async def iq(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(f"🧠 **{member.name}** are IQ-ul: `{random.randint(50, 160)}`")

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()
    code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
    await ctx.send(f"🎁 https://discord.gift/{code}")

# ==========================================
# --- 🛠️ IMPLEMENTARE UTILS ---
# ==========================================

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    await ctx.send(member.avatar_url)

@bot.command()
async def weather(ctx, city):
    await ctx.message.delete()
    await ctx.send(f"🌡️ https://wttr.in/{city}.png?m")

@bot.command()
async def crypto(ctx, coin):
    await ctx.message.delete()
    r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd").json()
    await ctx.send(f"🪙 **{coin.upper()}:** ${r.get(coin.lower(), {}).get('usd', 'N/A')}")

@bot.command()
async def binary(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(f"📟 `{' '.join(format(ord(x), '08b') for x in text)}`")

@bot.command()
async def math(ctx, *, expr):
    await ctx.message.delete()
    try: await ctx.send(f"🔢 Result: `{eval(expr)}`")
    except: await ctx.send("❌ Error")

# ==========================================
# --- ✨ IMPLEMENTARE STATUS ---
# ==========================================

@bot.command()
async def live(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/monstercat"))

@bot.command()
async def playing(ctx, *, text):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(name=text))

@bot.command()
async def remstats(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None)

@bot.command()
async def typing(ctx, seconds: int):
    await ctx.message.delete()
    async with ctx.typing(): await asyncio.sleep(seconds)

# ==========================================
# --- 🔥 IMPLEMENTARE T7 (EXTREME) ---
# ==========================================

@bot.command()
async def spam(ctx, count: int, *, text):
    await ctx.message.delete()
    for _ in range(count): await ctx.send(text); await asyncio.sleep(0.4)

@bot.command()
async def ghostspam(ctx, count: int):
    await ctx.message.delete()
    for _ in range(count):
        m = await ctx.send("👻 GHOST"); await m.delete()

@bot.command()
async def delchannels(ctx):
    await ctx.message.delete()
    for c in ctx.guild.channels:
        try: await c.delete()
        except: pass

@bot.command()
async def masskick(ctx):
    await ctx.message.delete()
    for m in ctx.guild.members:
        try: await m.kick()
        except: pass

@bot.command()
async def checktoken(ctx):
    await ctx.message.delete()
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": TOKEN_PRINCIPAL}).json()
    await ctx.send(f"```json\n{json.dumps(r, indent=2)}\n```")

# ==========================================
# --- 🚀 IMPLEMENTARE ADVANCED ---
# ==========================================

@bot.command()
async def ghostping(ctx, member: discord.Member):
    await ctx.message.delete()
    m = await ctx.send(member.mention); await m.delete()

@bot.command()
async def showtoken(ctx):
    await ctx.message.delete()
    try: await ctx.author.send(f"🔑 **Token:** `{TOKEN_PRINCIPAL}`")
    except: await ctx.send("❌ DM Closed")

@bot.command()
async def hypesquad(ctx, house):
    await ctx.message.delete()
    h_ids = {"bravery": 1, "brilliance": 2, "balance": 3}
    requests.post("https://discord.com/api/v9/hypesquad/online", headers={"Authorization": TOKEN_PRINCIPAL}, json={"house_id": h_ids.get(house.lower(), 1)})

# --- RUN ---
bot.run(TOKEN_PRINCIPAL)