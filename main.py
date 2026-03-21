# -*- coding: utf-8 -*-
import sys

# === [ 🛠️ PATCH-URI DE COMPATIBILITATE PENTRU PYTHON 3.13+ ] ===
class MockCGI:
    @staticmethod
    def escape(s, quote=True):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if quote: s = s.replace('"', "&quot;").replace('\'', "&#x27;")
        return s
sys.modules['cgi'] = MockCGI()

try:
    import audioop
except ImportError:
    class MockAudioop: pass
    sys.modules['audioop'] = MockAudioop()

# --- 🔥 FIX CRITIC PENTRU EROAREA FriendFlags (Login Crash) ---
import discord.settings
_old_settings_init = discord.settings.Settings.__init__
def _new_settings_init(self, *args, **kwargs):
    data = kwargs.get('data') or (args[0] if args else None)
    if data and isinstance(data, dict):
        if data.get('friend_source_flags') is None:
            data['friend_source_flags'] = {}
    _old_settings_init(self, *args, **kwargs)
discord.settings.Settings.__init__ = _new_settings_init
# =============================================================

import os, asyncio, json, random, time, datetime, requests, base64, re, platform
import discord
from discord.ext import commands

# --- CONFIGURARE ---
TOKEN_PRINCIPAL = os.getenv("TOKEN", "MTQ3MjExMjMwMDM0NDQ3OTc2NQ.G4Aq81.g1mMCVdL2bCL3DQa9m5eq0f0OH6TeocoB5pxgg,MTQ2OTc1MDA2NTg2MTEwMzgxMw.GdBEri.cU88G42uR3DzNJoy3Jlw3o5uBdH1MBgCEhnCTk,MTM4NDE5NTU1OTMwMDI3MjI3Mw.GYIecq.qTFTWzh-GmBkVWynAfsBeR0R0_fUBBVEDR88Ow")
GEMINI_API_KEY = os.getenv("GEMINI", "AIzaSyAHji_fQ3P9mOoFPLW82PrA_AAchxpAves")
PREFIX = "$"
START_TIME = time.time()

bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)

# Dicționare Date
MORSE_DICT = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----',' ':'/'}

# ==========================================
# --- 📋 TOATE MENIURILE HELP (TOATE) ---
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
💎 ・ $hImage  - Image Processing (NEW)
💻 ・ $hSys    - System & New Fun (EXTRA)
```""", delete_after=60)

@bot.command()
async def hAI(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🤖 ・ AI & INTELLIGENCE:
🤖 ・ $ai [text]     - Google Gemini AI
🎨 ・ $genimg [text] - Imagine AI
🧠 ・ $brain [q]     - Raspuns rapid (DDG)
🔍 ・ $google [q]    - Cautare Google
🎥 ・ $ytsearch [q]  - Cauta pe YouTube
📖 ・ $wiki [q]      - Wikipedia
```""", delete_after=60)

@bot.command()
async def hM(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🛡️ ・ MODERATION & SERVER:
👢 ・ $kick @u / $ban @u / $unban [id]
🌊 ・ $massunban     - Debaneaza tot serverul
🔄 ・ $softban @u    - Ban + Unban rapid
🔇 ・ $mute @u       - Pune rolul Muted
🔊 ・ $unmute @u     - Scoate rolul Muted
🧹 ・ $purge [nr]    - Sterge msjele tale
⏳ ・ $slowmode [s]  - Seteaza slowmode
🔒 ・ $lock / $unlock- Blocare canal
💥 ・ $nuke          - Recreeaza canalul
➕ ・ $masschannel   - Creeaza 10 canale
🏷️ ・ $massrole      - Creeaza 10 roluri
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
❤️ ・ $ship @u1 @u2  - Test dragoste
🎰 ・ $slots / $mines- Jocuri noroc
```""", delete_after=60)

@bot.command()
async def hutils(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🛠️ ・ UTILS & TOOLS:
🖼️ ・ $avatar / $banner @user
🏁 ・ $qr [text]     - Genereaza cod QR
🌐 ・ $ipinfo [ip]   - Detalii despre un IP
🔗 ・ $shorten [url] - Scurteaza un link
🌦️ ・ $weather [city]- Vremea oras
🪙 ・ $crypto [coin] - Pret Crypto (BTC)
🔢 ・ $math [expr]   - Calculator
📟 ・ $binary / $hex / $64 / $morse
🅰️ ・ $bold / $italic- Formatare text
```""", delete_after=60)

@bot.command()
async def hstatus(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
✨ ・ STATUS & SELF:
🎭 ・ $stats [text]  - Status custom
💜 ・ $live [text]   - Status streaming
💤 ・ $afk [reason]  - Seteaza AFK
🗑️ ・ $remstats      - Sterge status
🔄 ・ $restartstats  - Reset uptime
👀 ・ $watching / $listening / $playing
📡 ・ $ping / $uptime / $typing [sec]
```""", delete_after=60)

@bot.command()
async def hT7(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🔥 ・ TIER 7 (EXTREME):
☢️ ・ $spam [nr] [msg]- Spam rapid
👻 ・ $ghostspam [nr]- Spam cu stergere
🧨 ・ $delchannels   - Sterge TOATE canalele
🧨 ・ $delroles      - Sterge TOATE rolurile
☣️ ・ $masskick      - Kick la TOȚI membrii
🧬 ・ $checktoken    - Info brute despre cont
📜 ・ $logall        - Salveaza 100 msje in txt
```""", delete_after=60)

@bot.command()
async def hXtra(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
🌟 ・ EXTRA & IDEAS:
👤 ・ $whois / $perms / $created / $joined
🎭 ・ $mock / $clap / $ascii / $reverse
💎 ・ $aesthetic / $upper / $lower
📟 ・ $password [n]  - Genereaza parola
🎨 ・ $color [hex]   - Vezi o culoare
🎲 ・ $coinflip / $8ball / $dice
🧪 ・ $pokedex / $anime / $steam
📱 ・ $iphone [msg]  - Notificare iPhone
📺 ・ $nitrofake    - Troll Nitro
```""", delete_after=60)

@bot.command()
async def hImage(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
💎 ・ IMAGE PROCESSING (NEW):
🌫️ ・ $blur @u       - Avatar blurat
🌑 ・ $gray @u       - Avatar alb-negru
🌈 ・ $invert @u     - Culori inversate
🧱 ・ $pixelate @u   - Pixelat
🎥 ・ $youtubeavatar - Avatar pe YouTube
```""", delete_after=60)

@bot.command()
async def hSys(ctx):
    await ctx.message.delete()
    await ctx.send("""```text
💻 ・ SYSTEM & NEW FUN:
🌡️ ・ $sysinfo      - Info Termux/System
🧠 ・ $advice       - Sfat random
🐱 ・ $neko         - Poze Anime Neko
🔗 ・ $steal [id]   - Fura Emoji dupa ID
📺 ・ $vaporwave [t]- Text Vaporwave
```""", delete_after=60)

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
        await ctx.send(f"🤖 **Gemini AI:** {ans[:1900]}")
    except: await ctx.send("❌ Eroare API. Pune cheia Gemini!")

@bot.command()
async def genimg(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🎨 **Imagine AI:** https://pollinations.ai/p/{q.replace(' ', '%20')}")

@bot.command()
async def brain(ctx, *, q):
    await ctx.message.delete()
    r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json").json()
    await ctx.send(f"🧠 **Brain:** {r.get('AbstractText', 'Nu am gasit raspuns.')[:1000]}")

@bot.command()
async def google(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🔍 **Google:** https://www.google.com/search?q={q.replace(' ', '+')}")

@bot.command()
async def ytsearch(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"🎥 **YouTube:** https://www.youtube.com/results?search_query={q.replace(' ', '+')}")

@bot.command()
async def wiki(ctx, *, q):
    await ctx.message.delete()
    await ctx.send(f"📖 **Wiki:** https://en.wikipedia.org/wiki/{q.replace(' ', '_')}")

# ==========================================
# --- 🛡️ MODERARE ---
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
    await member.ban()
    await ctx.guild.unban(member)

@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    async for m in ctx.channel.history(limit=amount):
        if m.author == bot.user:
            try: await m.delete()
            except: pass

@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    n = await ctx.channel.clone()
    await ctx.channel.delete()
    await n.send("💥 **Nuked.**")

# ==========================================
# --- 🎮 GAMES & FUN ---
# ==========================================

@bot.command()
async def meme(ctx):
    await ctx.message.delete()
    r = requests.get("https://meme-api.com/gimme").json()
    await ctx.send(r['url'])

@bot.command()
async def mines(ctx, bombs: int = 5):
    await ctx.message.delete()
    grid = ["⬛"]*25
    for _ in range(min(bombs, 24)): grid[random.randint(0,24)] = "💣"
    res = "".join(grid[i]+("\n" if (i+1)%5==0 else " ") for i in range(25))
    await ctx.send(f"💣 **Mines 5x5:**\n{res}")

@bot.command()
async def howhot(ctx, u: discord.Member = None):
    await ctx.message.delete()
    u = u or ctx.author
    await ctx.send(f"🔥 **{u.name}** is **{random.randint(0,100)}%** hot!")

# ==========================================
# --- ✨ STATUS & SELF ---
# ==========================================

@bot.command()
async def stats(ctx, *, t):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.CustomActivity(name=t))

@bot.command()
async def typing(ctx, s: int):
    await ctx.message.delete()
    async with ctx.typing():
        await asyncio.sleep(s)

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()
    delta = str(datetime.timedelta(seconds=int(time.time() - START_TIME)))
    await ctx.send(f"🚀 **Uptime:** `{delta}`")

# ==========================================
# --- 🔥 TIER 7 (EXTREME) ---
# ==========================================

@bot.command()
async def spam(ctx, count: int, *, t):
    await ctx.message.delete()
    for _ in range(count):
        await ctx.send(t)
        await asyncio.sleep(0.4)

@bot.command()
async def delchannels(ctx):
    await ctx.message.delete()
    for c in ctx.guild.channels:
        try: await c.delete()
        except: pass

# ==========================================
# --- 💎 IMAGE PROCESSING ---
# ==========================================

@bot.command()
async def blur(ctx, u: discord.Member = None):
    await ctx.message.delete()
    u = u or ctx.author
    av = u.display_avatar.with_format("png").url
    await ctx.send(f"https://some-random-api.com/canvas/blur?avatar={av}")

@bot.command()
async def pixelate(ctx, u: discord.Member = None):
    await ctx.message.delete()
    u = u or ctx.author
    av = u.display_avatar.with_format("png").url
    await ctx.send(f"https://some-random-api.com/canvas/pixelate?avatar={av}")

# ==========================================
# --- 💻 COMENZI NOI SYSTEM ---
# ==========================================

@bot.command()
async def sysinfo(ctx):
    await ctx.message.delete()
    await ctx.send(f"💻 **Info:** `{platform.system()} {platform.release()}`\n🐍 **Python:** `{platform.python_version()}`")

@bot.command()
async def advice(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.adviceslip.com/advice").json()
    await ctx.send(f"💡 **Sfat:** {r['slip']['advice']}")

@bot.command()
async def neko(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.waifu.pics/sfw/neko").json()
    await ctx.send(r['url'])

@bot.command()
async def vaporwave(ctx, *, text):
    await ctx.message.delete()
    res = "".join(chr(ord(c) + 65248) if '!' <= c <= '~' else c for c in text)
    await ctx.send(res)

# --- START ---
@bot.event
async def on_ready():
    print(f"✅ RED-BOT PORNESTE!\n👤 Logat ca: {bot.user}")

bot.run(TOKEN_PRINCIPAL)