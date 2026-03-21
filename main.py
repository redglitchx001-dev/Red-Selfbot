# -*- coding: utf-8 -*-
import sys, os, asyncio, json, datetime, random, time, requests, re
import discord
from discord.ext import commands
from urllib.parse import quote

# --- CONFIGURARE ---
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.G4Aq81.g1mMCVdL2bCL3DQa9m5eq0f0OH6TeocoB5pxgg")
PREFIX = "$"
START_TIME = time.time()

def setup_bot(b):

    # --- 📋 CATEGORII HELP ---

    @b.command()
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

⚙️ ・ ADMIN:
$REDHELP        - Meniu complet
$restartstats   - Resetează uptime-ul
```"""
        await ctx.send(menu, delete_after=60)

    @b.command()
    async def hAI(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🤖 ・ AI & INTELLIGENCE (hAI):
$ai [text]     - Întreabă AI-ul
$genimg [text] - Generează imagine AI
$brain [q]     - Răspuns rapid enciclopedic
$google [q]    - Căutare rapidă Google
$ytsearch [q]  - Căutare pe YouTube
$wiki [q]      - Căutare pe Wikipedia
```""", delete_after=60)

    @b.command()
    async def hM(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🛡️ ・ MODERATION & SERVER (hM):
$kick @user    - Dă afară un membru
$ban @user     - Banează un membru
$unban [id]    - Scoate ban-ul
$massunban     - Scoate ban-ul tuturor
$softban @user - Ban + Unban rapid
$mute @user    - Pune mute (rol necesar)
$unmute @user  - Scoate mute
$purge [nr]    - Șterge X mesaje
$slowmode [s]  - Setează slowmode canal
$lock / $unlock- Blocare/Deblocare canal
$nuke          - Șterge și recreează canalul
$masschannel   - Creează X canale
$massrole      - Creează X roluri
```""", delete_after=60)

    @b.command()
    async def hgame(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🎮 ・ GAMES & FUN (hgame):
$meme          - Arată un meme random
$joke          - Spune o glumă
$quote         - Arată un citat celebru
$cat / $dog    - Poze cu animale
$fact          - Un fapt interesant
$howhot @user  - Cât de hot ești?
$hug / $slap   - Interacțiuni
$kill / $punch - Interacțiuni agresive
$nitro         - Generează cod Nitro fake
$gay @user     - Cât de gay ești?
$iq @user      - Test IQ rapid
$ship @u1 @u2  - Test de dragoste
$slots         - Joc de păcănele
$mines [nr]    - Joc de mine (💣)
```""", delete_after=60)

    @b.command()
    async def hutils(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🛠️ ・ UTILS & TOOLS (hutils):
$avatar @user  - Vezi avatarul cuiva
$banner @user  - Vezi bannerul cuiva
$qr [text]     - Generează cod QR
$ipinfo [ip]   - Detalii despre un IP
$shorten [url] - Scurtează un link
$weather [city]- Vremea în orașul X
$crypto [coin] - Preț crypto actual
$math [expr]   - Calculator matematic
$binary / $hex - Conversie text
$morse / $64   - Conversie text
$bold / $italic- Formatare text
```""", delete_after=60)

    @b.command()
    async def hstatus(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
✨ ・ STATUS & UTIL (hstatus):
$stats [text]  - Setează status personalizat
$live [text]   - Setează status streaming mov
$afk [reason]  - Setează motiv AFK
$remstats      - Șterge statusul actual
$restartstats  - Resetează uptime-ul
$watching [t]  - Status Watching
$listening [t] - Status Listening
$playing [t]   - Status Playing
$ping          - Vezi latența botului
$uptime        - Timp de funcționare
$typing [sec]  - Fake typing status
```""", delete_after=60)

    @b.command()
    async def hadv(ctx):
        await ctx.message.delete()
        await ctx.send("""```text
🚀 ・ ADVANCED & FUN (hadv):
$steal [emoji] - Fură un emoji
$urban [word]  - Urban Dictionary
$timer [s] [r] - Setează un cronometru
$purgeuser @u  - Șterge mesajele unui user
$servericon    - Vezi iconița serverului
$serverbanner  - Vezi bannerul serverului
$ghostping @u  - Ping discret (delete instant)
$secret [text] - Mesaj ascuns (spoiler)
$nick [nume]   - Schimbă nickname-ul tău
$hypesquad [h] - Schimbă casa HypeSquad
$triggered @u  - Efect triggered pe avatar
$wanted @u     - Efect wanted pe avatar
$showtoken     - Vezi token-ul contului
```""", delete_after=60)

    # --- 🤖 CATEGORIA: AI & INTELLIGENCE ---

    @b.command()
    async def ai(ctx, *, text):
        await ctx.message.delete()
        # Mock AI response (Simulare)
        await ctx.send(f"🤖 **AI Răspuns:** Căutând informații despre `{text}`... În prezent, sunt configurat ca un Selfbot avansat. Răspunsul meu este: *Interesant subiect!*")

    @b.command()
    async def genimg(ctx, *, text):
        await ctx.message.delete()
        await ctx.send(f"🎨 **Generez imagine pentru:** `{text}`...\nhttps://pollinations.ai/p/{quote(text)}")

    @b.command()
    async def brain(ctx, *, query):
        await ctx.message.delete()
        await ctx.send(f"🧠 **Brain Search:** `{query}`\nhttps://www.wolframalpha.com/input?i={quote(query)}")

    @b.command()
    async def google(ctx, *, query):
        await ctx.message.delete()
        await ctx.send(f"🔍 **Google Search:** https://www.google.com/search?q={quote(query)}")

    @b.command()
    async def ytsearch(ctx, *, query):
        await ctx.message.delete()
        await ctx.send(f"📺 **YouTube Search:** https://www.youtube.com/results?search_query={quote(query)}")

    @b.command()
    async def wiki(ctx, *, query):
        await ctx.message.delete()
        await ctx.send(f"📖 **Wikipedia:** https://en.wikipedia.org/wiki/{quote(query)}")

    # --- 🛡️ CATEGORIA: MODERATION ---

    @b.command()
    async def kick(ctx, member: discord.Member, *, reason="Fără motiv"):
        await ctx.message.delete()
        try: await member.kick(reason=reason); await ctx.send(f"✅ {member} a primit kick.")
        except: await ctx.send("❌ Lipsă permisiuni!")

    @b.command()
    async def ban(ctx, member: discord.Member, *, reason="Fără motiv"):
        await ctx.message.delete()
        try: await member.ban(reason=reason); await ctx.send(f"✅ {member} a primit ban.")
        except: await ctx.send("❌ Lipsă permisiuni!")

    @b.command()
    async def unban(ctx, user_id: int):
        await ctx.message.delete()
        user = await b.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ {user} a primit unban.")

    @b.command()
    async def massunban(ctx):
        await ctx.message.delete()
        ban_list = await ctx.guild.bans()
        for entry in ban_list: await ctx.guild.unban(entry.user)
        await ctx.send("✅ Toți utilizatorii au primit unban.")

    @b.command()
    async def softban(ctx, member: discord.Member):
        await ctx.message.delete()
        await member.ban(); await ctx.guild.unban(member)
        await ctx.send(f"✅ {member} a primit softban (mesaje șterse).")

    @b.command()
    async def mute(ctx, member: discord.Member):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role: role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels: await channel.set_permissions(role, speak=False, send_messages=False)
        await member.add_roles(role)
        await ctx.send(f"✅ {member} a primit mute.")

    @b.command()
    async def unmute(ctx, member: discord.Member):
        await ctx.message.delete()
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"✅ {member} a primit unmute.")

    @b.command()
    async def purge(ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @b.command()
    async def slowmode(ctx, seconds: int):
        await ctx.message.delete()
        await ctx.channel.edit(slowmode_delay=seconds)

    @b.command()
    async def lock(ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Canal blocat.")

    @b.command()
    async def unlock(ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Canal deblocat.")

    @b.command()
    async def nuke(ctx):
        await ctx.message.delete()
        new_channel = await ctx.channel.clone()
        await ctx.channel.delete()
        await new_channel.send("☢️ Canal distrus și recreat!")

    @b.command()
    async def masschannel(ctx, count: int, *, name):
        await ctx.message.delete()
        for i in range(count): await ctx.guild.create_text_channel(name)

    @b.command()
    async def massrole(ctx, count: int, *, name):
        await ctx.message.delete()
        for i in range(count): await ctx.guild.create_role(name=name)

    # --- 🎮 CATEGORIA: GAMES & FUN ---

    @b.command()
    async def meme(ctx):
        await ctx.message.delete()
        r = requests.get("https://meme-api.com/gimme").json()
        await ctx.send(r['url'])

    @b.command()
    async def joke(ctx):
        await ctx.message.delete()
        r = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()
        await ctx.send(f"😂 **Glumă:** {r['joke']}")

    @b.command()
    async def quote(ctx):
        await ctx.message.delete()
        r = requests.get("https://api.quotable.io/random").json()
        await ctx.send(f"📜 *\"{r['content']}\"* — **{r['author']}**")

    @b.command()
    async def cat(ctx):
        await ctx.message.delete()
        r = requests.get("https://api.thecatapi.com/v1/images/search").json()
        await ctx.send(r[0]['url'])

    @b.command()
    async def dog(ctx):
        await ctx.message.delete()
        r = requests.get("https://dog.ceo/api/breeds/image/random").json()
        await ctx.send(r['message'])

    @b.command()
    async def fact(ctx):
        await ctx.message.delete()
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        await ctx.send(f"💡 **Știai că?** {r['text']}")

    @b.command()
    async def howhot(ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = member or ctx.author
        await ctx.send(f"🔥 **{member.name}** este **{random.randint(0, 100)}%** hot!")

    @b.command()
    async def hug(ctx, member: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"🫂 **{ctx.author.name}** l-a îmbrățișat pe **{member.name}**!")

    @b.command()
    async def slap(ctx, member: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"👋 **{ctx.author.name}** i-a tras o palmă lui **{member.name}**!")

    @b.command()
    async def kill(ctx, member: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"💀 **{ctx.author.name}** l-a eliminat pe **{member.name}**!")

    @b.command()
    async def punch(ctx, member: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"👊 **{ctx.author.name}** i-a tras un pumn lui **{member.name}**!")

    @b.command()
    async def nitro(ctx):
        await ctx.message.delete()
        code = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
        await ctx.send(f"🎁 **Nitro:** discord.gift/{code}")

    @b.command()
    async def gay(ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = member or ctx.author
        await ctx.send(f"🌈 **{member.name}** este **{random.randint(0, 100)}%** gay!")

    @b.command()
    async def iq(ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = member or ctx.author
        await ctx.send(f"🧠 **{member.name}** are un IQ de **{random.randint(50, 200)}**!")

    @b.command()
    async def ship(ctx, u1: discord.Member, u2: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"❤️ **Ship:** {u1.name} + {u2.name} = **{random.randint(0, 100)}%** compatibilitate!")

    @b.command()
    async def slots(ctx):
        await ctx.message.delete()
        items = ["🍎", "🍒", "🍇", "💎", "7️⃣"]
        res = [random.choice(items) for _ in range(3)]
        msg = " | ".join(res)
        if res[0] == res[1] == res[2]: await ctx.send(f"🎰 `{msg}`\n✨ **CÂȘTIGĂTOR!**")
        else: await ctx.send(f"🎰 `{msg}`\n❌ Mai încearcă.")

    @b.command()
    async def mines(ctx, bombs: int = 5):
        await ctx.message.delete()
        grid = ["⬛"] * 25
        bomb_indices = random.sample(range(25), min(bombs, 24))
        for i in range(25):
            if i in bomb_indices: grid[i] = "💣"
            else: grid[i] = "💎"
        
        display = "\n".join(["".join(grid[i:i+5]) for i in range(0, 25, 5)])
        await ctx.send(f"💣 **MINES GAME** (Bombe: {bombs})\n{display}")

    # --- 🛠️ CATEGORIA: UTILS ---

    @b.command()
    async def avatar(ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = member or ctx.author
        await ctx.send(member.avatar_url)

    @b.command()
    async def banner(ctx, member: discord.Member = None):
        await ctx.message.delete()
        member = member or ctx.author
        user = await b.fetch_user(member.id)
        if user.banner: await ctx.send(user.banner_url)
        else: await ctx.send("❌ Acest user nu are banner.")

    @b.command()
    async def qr(ctx, *, text):
        await ctx.message.delete()
        await ctx.send(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(text)}")

    @b.command()
    async def ipinfo(ctx, ip):
        await ctx.message.delete()
        r = requests.get(f"https://ipapi.co/{ip}/json/").json()
        await ctx.send(f"🌐 **IP:** {ip}\n📍 **Oraș:** {r.get('city')}\n🚩 **Țară:** {r.get('country_name')}\n🏢 **ISP:** {r.get('org')}")

    @b.command()
    async def shorten(ctx, url):
        await ctx.message.delete()
        r = requests.get(f"https://is.gd/create.php?format=json&url={url}").json()
        await ctx.send(f"🔗 **Scurt:** {r['shorturl']}")

    @b.command()
    async def weather(ctx, *, city):
        await ctx.message.delete()
        await ctx.send(f"☁️ **Vremea în {city}:**\nhttps://wttr.in/{quote(city)}?0&m&q")

    @b.command()
    async def crypto(ctx, coin="bitcoin"):
        await ctx.message.delete()
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd").json()
        await ctx.send(f"💰 **{coin.upper()}:** ${r[coin]['usd']}")

    @b.command()
    async def math(ctx, *, expr):
        await ctx.message.delete()
        try: await ctx.send(f"🔢 **Rezultat:** `{eval(expr)}`")
        except: await ctx.send("❌ Expresie invalidă.")

    @b.command()
    async def binary(ctx, *, text):
        await ctx.message.delete()
        res = ' '.join(format(ord(x), '08b') for x in text)
        await ctx.send(f"🔢 **Binary:** `{res[:1900]}`")

    @b.command()
    async def hex(ctx, *, text):
        await ctx.message.delete()
        res = text.encode().hex()
        await ctx.send(f"🔢 **Hex:** `{res[:1900]}`")

    @b.command()
    async def morse(ctx, *, text):
        await ctx.message.delete()
        MORSE_DICT = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',' ':'/'}
        res = ' '.join(MORSE_DICT.get(c.upper(), '') for c in text)
        await ctx.send(f"📟 **Morse:** `{res[:1900]}`")

    @b.command(name="64")
    async def base64_cmd(ctx, *, text):
        await ctx.message.delete()
        import base64
        res = base64.b64encode(text.encode()).decode()
        await ctx.send(f"🔢 **Base64:** `{res[:1900]}`")

    @b.command()
    async def bold(ctx, *, text):
        await ctx.message.delete(); await ctx.send(f"**{text}**")

    @b.command()
    async def italic(ctx, *, text):
        await ctx.message.delete(); await ctx.send(f"*{text}*")

    # --- ✨ CATEGORIA: STATUS ---

    @b.command()
    async def stats(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Game(name=text))

    @b.command()
    async def live(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/redglitch"))

    @b.command()
    async def afk(ctx, *, reason="Pauză"):
        await ctx.message.delete()
        await ctx.send(f"💤 **AFK:** {reason}")

    @b.command()
    async def remstats(ctx):
        await ctx.message.delete()
        await b.change_presence(activity=None)

    @b.command()
    async def watching(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

    @b.command()
    async def listening(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))

    @b.command()
    async def playing(ctx, *, text):
        await ctx.message.delete()
        await b.change_presence(activity=discord.Game(name=text))

    @b.command()
    async def ping(ctx):
        await ctx.message.delete()
        await ctx.send(f"🏓 **Pong!** `{round(b.latency * 1000)}ms`")

    @b.command()
    async def uptime(ctx):
        await ctx.message.delete()
        delta = str(datetime.timedelta(seconds=int(time.time() - START_TIME)))
        await ctx.send(f"🚀 **Uptime Cont:** `{delta}`")

    @b.command()
    async def typing(ctx, seconds: int):
        await ctx.message.delete()
        async with ctx.typing(): await asyncio.sleep(seconds)

    @b.command()
    async def restartstats(ctx):
        await ctx.message.delete()
        global START_TIME; START_TIME = time.time()
        await ctx.send("✅ **Statisticile au fost resetate!**", delete_after=5)

    # --- 🚀 CATEGORIA: ADVANCED ---

    @b.command()
    async def steal(ctx, emoji: discord.PartialEmoji):
        await ctx.message.delete()
        r = requests.get(emoji.url)
        new_emoji = await ctx.guild.create_custom_emoji(name=emoji.name, image=r.content)
        await ctx.send(f"✅ Emoji furat: {new_emoji}")

    @b.command()
    async def urban(ctx, *, word):
        await ctx.message.delete()
        r = requests.get(f"https://api.urbandictionary.com/v0/define?term={word}").json()
        await ctx.send(f"📖 **Urban:** {r['list'][0]['definition'][:500]}")

    @b.command()
    async def timer(ctx, seconds: int, *, reason="Timpul a expirat!"):
        await ctx.message.delete()
        await ctx.send(f"⏰ Cronometru setat: `{seconds}s`")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 **{ctx.author.mention}**: {reason}")

    @b.command()
    async def purgeuser(ctx, member: discord.Member, amount: int = 100):
        await ctx.message.delete()
        def check(m): return m.author == member
        await ctx.channel.purge(limit=amount, check=check)

    @b.command()
    async def servericon(ctx):
        await ctx.message.delete()
        await ctx.send(ctx.guild.icon_url)

    @b.command()
    async def serverbanner(ctx):
        await ctx.message.delete()
        await ctx.send(ctx.guild.banner_url)

    @b.command()
    async def ghostping(ctx, member: discord.Member):
        await ctx.message.delete()
        msg = await ctx.send(member.mention)
        await msg.delete()

    @b.command()
    async def secret(ctx, *, text):
        await ctx.message.delete()
        await ctx.send(f"||{text}||")

    @b.command()
    async def nick(ctx, *, name):
        await ctx.message.delete()
        await ctx.author.edit(nick=name)

    @b.command()
    async def hypesquad(ctx, house):
        await ctx.message.delete()
  