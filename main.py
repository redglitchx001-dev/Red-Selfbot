# -*- coding: utf-8 -*-
import sys, types, os, asyncio, json, threading, shutil, requests, datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- 🚀 CRITICAL PATCHES FOR PYTHON 3.13 & ANDROID ---
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
    print("❌ Please install: pip install discord.py-self==1.9.2 requests")
    sys.exit(1)

# --- 🌐 WEB HEALTH CHECK SERVER (FOR RENDER / PORT) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>System Status</title></head>
        <body style="background-color: #0b0b0b; color: #00ffcc; font-family: monospace;">
            <h2>[SYSTEM ACTIVE] Selfbot Online</h2>
            <p>Status: Operational // Node Connected</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# --- ⚙️ CONFIGURATION ---
TOKEN_PRINCIPAL = os.getenv("DISCORD_TOKEN")
PREFIX = "$"

# Create folder structure
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

    @b.event
    async def on_message(message):
        # Snipe logger setup
        if message.guild and message.author != b.user:
            snipe_data[message.channel.id] = f"[{message.author}] {message.content}"

        # Chat logger setup
        if log_chat_active and message.guild and message.author != b.user:
            with open(f"logs/chat_{message.channel.id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{message.created_at}] {message.author}: {message.content}\n")

        # DM logger setup
        if log_dm_active and not message.guild and message.author != b.user:
            with open(f"logs/dm_{message.author.id}.txt", "a", encoding="utf-8") as f:
                f.write(f"[{message.created_at}] {message.author}: {message.content}\n")

        await b.process_commands(message)

    @b.command()
    async def REDHELP(ctx):
        await ctx.message.delete()
        menu = """```text
--- 📋 ・ COMPLETE COMMAND LIST ---

🎵 ・ MUSIC & VOICE:
$helpvc        - Quick voice menu
$downloadm     - Download from YouTube/URL [link]
$adfiles       - Attach an MP3 for upload
$dwnlibs       - View saved track list
$plays [nr]    - Play track number X
$stops         - Stop music and leave channel

✉️ ・ SPAM BOT:
$start @user   - Start spam from botjura.txt
$stop          - Stop spam process
$spam [m][n][d] - Repeat text X times with delay

👤 ・ PROFILE ARCHIVER:
$prfdwn @user  - Download profile into /profiles
$prflist       - List saved profiles (1, 2, 3...)
$prfup [nr]    - Apply/load profile by number
$mphelp        - Profiler help menu

🏰 ・ CLONER MODULE ($DSRV):
$dsrv          - Copy server structure
$lsrv          - List local saved schemes
$psrv [nr]     - Apply scheme to new server

📂 ・ COPY & ARCHIVE:
$clchat [nr]   - Copy last messages + Media
$clist         - Display clip list
$pstchat [nr]  - Paste chat from file X

🛡️ ・ PROTECTION MODULE ($BP2HELP):
$anti-kick     - Kick protection (on/off)
$anti-ban      - Ban protection (on/off)
$ghostping     - Discreet ping @user
$tokencheck    - Check token validity

📜 ・ LOGGER MODULE ($LHELP):
$logchat       - Log channel messages
$logdm         - Save direct messages
$sniped        - View last deleted message
$track @user   - User status notifications

✨ ・ STATUS & UTILS:
$stats [text]  - Set custom status
$live [text]   - Set purple streaming status
$remstats      - Clear current status

🤖 ・ MULTI-ACC:
$selfbot [t][n]- Add new token
$selfbot       - List active accounts
$selfbotr [name]- Remove account from list

⚙️ ・ ADMIN:
$REDHELP        - Complete menu (visible 30s)

------------------------------------------
Credits: RedGlitchX / redglitchx. / XTASK 
------------------------------------------
```"""
        await ctx.send(menu, delete_after=30)

    @b.command()
    async def helpvc(ctx):
        await ctx.message.delete()
        help_text = """```text
--- 🎵 VOICE HELP ---
$plays [nr/name] - Play track
$stops           - Stop music
$downloadm [url] - Download MP3
$dwnlibs         - Track list
$adfiles         - Upload MP3 (attachment)
```"""
        await ctx.send(help_text, delete_after=15)

    @b.command()
    async def plays(ctx, *, name: str):
        await ctx.message.delete()
        if not ctx.author.voice: return await ctx.send("❌ Join a voice channel first!", delete_after=5)
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
        if not path or not os.path.exists(path): return await ctx.send(f"❌ Track `{name}` not found!", delete_after=5)
        try:
            vc = ctx.voice_client or await ctx.author.voice.channel.connect()
            if vc.is_playing(): vc.stop()
            vc.play(discord.FFmpegPCMAudio(path))
            await ctx.send(f"🎶 Playing: `{os.path.basename(path)}`", delete_after=10)
        except Exception as e: await ctx.send(f"❌ Voice Error: {e}", delete_after=10)

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
            await ctx.send(f"✅ Downloaded: `{fname}`", delete_after=10)
        except: await ctx.send("❌ Download failed!", delete_after=5)

    @b.command()
    async def adfiles(ctx):
        await ctx.message.delete()
        if not ctx.message.attachments:
            return await ctx.send("❌ Attach an MP3 file!", delete_after=5)
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                await attachment.save(f"music/{attachment.filename}")
                await ctx.send(f"✅ Saved: `{attachment.filename}`", delete_after=5)
            else:
                await ctx.send(f"❌ `{attachment.filename}` is not an MP3!", delete_after=5)

    @b.command()
    async def dwnlibs(ctx):
        await ctx.message.delete()
        files = sorted(os.listdir("music"))
        lista = "\n".join([f"{i+1}. {f}" for i, f in enumerate(files)]) if files else "No files."
        await ctx.send(f"🎵 **Library:**\n```\n{lista}\n```", delete_after=20)

    @b.command()
    async def start(ctx, user: discord.Member = None):
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
        await ctx.send("🛑 Spam stopped.", delete_after=3)

    @b.command()
    async def spam(ctx, msg: str, count: int, delay: float = 0.5):
        await ctx.message.delete()
        for _ in range(count):
            await ctx.send(msg)
            await asyncio.sleep(delay)

    @b.command()
    async def prfdwn(ctx, user: discord.Member):
        await ctx.message.delete()
        if not os.path.exists("profiles"): os.makedirs("profiles")
        avatar_url = str(user.avatar.url) if user.avatar else ""
        created_at = str(user.created_at) if user.created_at else ""
        joined_at = str(user.joined_at) if hasattr(user, 'joined_at') and user.joined_at else ""
        roles = [r.name for r in user.roles] if hasattr(user, 'roles') else []
        data = {
            "name": user.name,
            "id": user.id,
            "avatar": avatar_url,
            "created_at": created_at,
            "joined_at": joined_at,
            "roles": roles
        }
        with open(f"profiles/{user.id}.json", "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
        await ctx.send(f"👤 Profile archived: `{user.name}`", delete_after=5)

    @b.command()
    async def prflist(ctx):
        await ctx.message.delete()
        if not os.path.exists("profiles"): os.makedirs("profiles")
        files = sorted([f for f in os.listdir("profiles") if f.endswith(".json")])
        if not files:
            return await ctx.send("👤 No saved profiles found.", delete_after=10)
        
        msg = "👤 **SAVED PROFILES:**\n```text\n"
        for i, f in enumerate(files, 1):
            try:
                with open(f"profiles/{f}", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    p_name = data.get("name", "Unknown")
                    msg += f"{i} {p_name}\n"
            except:
                msg += f"{i} Read error: {f}\n"
        msg += "```\n*Use `$prfup [nr]` to load/view.*"
        await ctx.send(msg, delete_after=30)

    @b.command()
    async def prfup(ctx, nr: int):
        await ctx.message.delete()
        if not os.path.exists("profiles"): return await ctx.send("❌ Profiles folder does not exist.", delete_after=5)
        files = sorted([f for f in os.listdir("profiles") if f.endswith(".json")])
        if not (1 <= nr <= len(files)):
            return await ctx.send(f"❌ Invalid number! Choose between 1 and {len(files)}.", delete_after=5)
        
        path = f"profiles/{files[nr-1]}"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        info = (
            f"👤 **Profile Info ({nr}):**\n"
            f"• Name: `{data.get('name')}`\n"
            f"• ID: `{data.get('id')}`\n"
            f"• Created: `{data.get('created_at')}`\n"
            f"• Roles Count: `{len(data.get('roles', []))}`"
        )
        await ctx.send(info, delete_after=20)

    @b.command()
    async def mphelp(ctx):
        await ctx.message.delete()
        await ctx.send("```Profile Archiver:\n$prfdwn @user - Save profile\n$prflist - List profiles (1 Name)\n$prfup [nr] - Load profile info```", delete_after=15)

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
                ch_data = {
                    "n": ch.name, 
                    "t": str(ch.type),
                    "overwrites": get_overwrites(ch)
                }
                if isinstance(ch, discord.TextChannel):
                    ch_data["topic"] = ch.topic
                    ch_data["nsfw"] = ch.nsfw
                elif isinstance(ch, discord.VoiceChannel):
                    ch_data["bitrate"] = ch.bitrate
                    ch_data["user_limit"] = ch.user_limit
                chans.append(ch_data)
            
            data["categories"].append({
                "n": cat.name, 
                "overwrites": get_overwrites(cat),
                "ch": chans
            })

        for ch in ctx.guild.channels:
            if ch.category is None:
                ch_data = {
                    "n": ch.name, 
                    "t": str(ch.type),
                    "overwrites": get_overwrites(ch)
                }
                if isinstance(ch, discord.TextChannel):
                    ch_data["topic"] = ch.topic
                    ch_data["nsfw"] = ch.nsfw
                elif isinstance(ch, discord.VoiceChannel):
                    ch_data["bitrate"] = ch.bitrate
                    ch_data["user_limit"] = ch.user_limit
                data["orphan_channels"].append(ch_data)

        filename = f"clones/backup_{ctx.guild.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"🏰 Backup saved for **{ctx.guild.name}**!", delete_after=5)

    @b.command()
    async def lsrv(ctx):
        await ctx.message.delete()
        if not os.path.exists("clones"): os.makedirs("clones")
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        
        if not files:
            return await ctx.send("🏰 No saved backups.", delete_after=10)
        
        msg = "🏰 **SAVED BACKUPS LIST:**\n```text\n"
        for i, f in enumerate(files, 1):
            try:
                with open(f"clones/{f}", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    s_name = data.get("name", "Unknown")
                    msg += f"{i}. {s_name} ({f})\n"
            except:
                msg += f"{i}. Read error: {f}\n"
        msg += "```\n*Use `$psrv [nr]` to apply.*"
        await ctx.send(msg, delete_after=30)

    @b.command()
    async def psrv(ctx, nr: int):
        await ctx.message.delete()
        if not os.path.exists("clones"): return await ctx.send("❌ Clones folder does not exist.", delete_after=5)
        files = sorted([f for f in os.listdir("clones") if f.endswith(".json")])
        
        if not (1 <= nr <= len(files)):
            return await ctx.send(f"❌ Invalid number! Choose between 1 and {len(files)}.", delete_after=5)
        
        path = f"clones/{files[nr-1]}"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        await ctx.send(f"🏰 Applying backup: **{data['name']}**... (Please wait)", delete_after=10)

        role_mapping = {}
        everyone_role = ctx.guild.default_role
        
        for r in data.get("roles", []):
            if r.get("is_everyone"):
                role_mapping[r["id"]] = everyone_role
                try: await everyone_role.edit(permissions=discord.Permissions(r["p"]))
                except: pass
                continue
                
            try:
                new_role = await ctx.guild.create_role(
                    name=r["n"],
                    color=discord.Color(r["c"]),
                    permissions=discord.Permissions(r["p"]),
                    hoist=r["h"],
                    mentionable=r["m"]
                )
                role_mapping[r["id"]] = new_role
            except: pass

        def sync_overwrites(ow_data):
            overwrites = {}
            for ow in ow_data:
                target = role_mapping.get(ow["id"])
                if target:
                    overwrites[target] = discord.PermissionOverwrite.from_pair(
                        discord.Permissions(ow["allow"]),
                        discord.Permissions(ow["deny"])
                    )
            return overwrites

        for cat_data in data.get("categories", []):
            try:
                ow = sync_overwrites(cat_data.get("overwrites", []))
                category = await ctx.guild.create_category(cat_data["n"], overwrites=ow)
                for ch in cat_data["ch"]:
                    ch_ow = sync_overwrites(ch.get("overwrites", []))
                    if ch["t"] == "text":
                        await category.create_text_channel(
                            ch["n"], 
                            topic=ch.get("topic"), 
                            nsfw=ch.get("nsfw", False),
                            overwrites=ch_ow
                        )
                    elif ch["t"] == "voice":
                        await category.create_voice_channel(
                            ch["n"],
                            bitrate=ch.get("bitrate", 64000),
                            user_limit=ch.get("user_limit", 0),
                            overwrites=ch_ow
                        )
            except: pass

        for ch in data.get("orphan_channels", []):
            try:
                ch_ow = sync_overwrites(ch.get("overwrites", []))
                if ch["t"] == "text":
                    await ctx.guild.create_text_channel(
                        ch["n"], 
                        topic=ch.get("topic"), 
                        nsfw=ch.get("nsfw", False),
                        overwrites=ch_ow
                    )
                elif ch["t"] == "voice":
                    await ctx.guild.create_voice_channel(
                        ch["n"],
                        bitrate=ch.get("bitrate", 64000),
                        user_limit=ch.get("user_limit", 0),
                        overwrites=ch_ow
                    )
            except: pass

        await ctx.send("✅ Backup applied successfully!", delete_after=5)

    @b.command()
    async def clchat(ctx, amount: int = 100):
        await ctx.message.delete()
        fname = f"archives/chat_{ctx.channel.id}.txt"
        with open(fname, "w", encoding="utf-8") as f:
 