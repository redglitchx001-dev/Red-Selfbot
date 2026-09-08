# -*- coding: utf-8 -*-
"""Help menu system for Red Selfbot V1 - Fancy 2026 edition."""
from utils.common import *

# Fancy unicode fonts
# Using script / double-struck for premium look

MENUS = {
    "main": {
        "title": "𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1",
        "subtitle": "PREMIUM CONTROL PANEL // 2026 EDITION",
        "emoji": "⚡",
        "items": [
            "$hcore    - Core / bot info",
            "$hmusic   - Music & voice",
            "$hspam    - Automation & sequences [MULTI-USER]",
            "$hprofile - Profile archiver",
            "$hclone   - Server cloner",
            "$harchive - Chat copy & paste",
            "$hprotect - Protection suite",
            "$hlog     - Logger & snipe",
            "$hstatus  - Presence & status",
            "$htext    - Text transform tools",
            "$hfun     - Fun & games",
            "$hutil    - Utility commands",
            "$hinfo    - Info lookup",
            "$hai      - AI chat module",
            "$hmulti   - Multi-account",
            "$hall     - All commands (long list)",
        ],
        "footer": "Type a command for details. Prefix: $  |  $start @user1 @user2 file"
    },
    "core": {
        "title": "CORE",
        "emoji": "♦",
        "items": [
            "$ping      - Gateway latency",
            "$uptime    - Session uptime",
            "$stats [t] - Playing status",
            "$live [t]  - Streaming status",
            "$remstats  - Clear status",
            "$prefix    - Show prefix",
            "$about     - About Red Selfbot",
            "$dashboard - Show dashboard URL (port 3000)",
        ],
        "footer": "$help returns here"
    },
    "music": {
        "title": "MUSIC & VOICE",
        "emoji": "♪",
        "items": [
            "$plays [n]   - Play track #n or by name",
            "$stops       - Stop & leave channel",
            "$skip        - Skip current track",
            "$queue       - Show queue list",
            "$pause       - Pause playback",
            "$resume      - Resume playback",
            "$volume [v]  - Set volume 0-100",
            "$np          - Now playing info",
            "$downloadm u - Download from URL",
            "$adfiles     - Attach MP3 to save",
            "$dwnlibs     - List tracks",
            "$join        - Join voice channel",
            "$leave       - Leave voice channel",
        ],
        "footer": "Requires ffmpeg installed"
    },
    "spam": {
        "title": "AUTOMATION / SEQUENCES [2026]",
        "emoji": "▶",
        "items": [
            "$start [@u1 @u2 ...] [file] - Run sequence MULTI-USER",
            "  ex: $start @ionut @vasile data/longspam_en.txt",
            "  ex: $start ionut vasile alex spam_ro.txt",
            "  ex: $start @user1 @user2 ro",
            "$startl           - List all line files (fancy)",
            "$startlang <name> - Set default file",
            "$stop             - Stop all",
            "$spam [msg] [n][d]- Repeat msg n times",
            "$spamall m n      - Send to all channels",
            "$flood [n]        - Fast flood channel",
            "$dmspam @u n m    - DM user n times",
            "$react [e]        - React to last msg",
            "$repeat [n]       - Repeat your last msg",
            "$autoreact [e]    - Auto-react to msgs",
            "$massmention      - Mention online members",
            "",
            "Packs: spam.txt | spam_ro | spam_en | longspam_ro | longspam_en",
            "RO = only romana | EN = only english + gifs",
            "SHORT spam = NO prefix = BIG text",
            "LONG spam = '# ' prefix cu spatiu (heading mare)",
            "ex long: '# {t} esti varza' - nu lipit",
        ],
        "footer": "2026 packs: hardcore roast, no slur, multi-target"
    },
    "profile": {
        "title": "PROFILE ARCHIVER",
        "emoji": "@",
        "items": [
            "$prfdwn @u   - Save user profile",
            "$prflist     - List saved profiles",
            "$prfup [n]   - View profile #n",
            "$prfdel [n]  - Delete profile #n",
            "$mphelp      - This menu",
        ],
        "footer": "Profiles stored in /profiles"
    },
    "clone": {
        "title": "SERVER CLONER",
        "emoji": "C",
        "items": [
            "$dsrv        - Backup current server",
            "$lsrv        - List backups",
            "$psrv [n]    - Apply backup #n here",
            "$dsrvdel [n] - Delete backup #n",
        ],
        "footer": "Need Manage Roles/Channels"
    },
    "archive": {
        "title": "CHAT ARCHIVE",
        "emoji": "A",
        "items": [
            "$clchat [n]  - Save last n messages",
            "$clist       - List saved archives",
            "$pstchat id  - Paste archive",
            "$cldel [n]   - Delete archive",
        ],
        "footer": "Saves attachments & embeds"
    },
    "protect": {
        "title": "PROTECTION",
        "emoji": "!",
        "items": [
            "$anti-kick   - Toggle anti-kick",
            "$anti-ban    - Toggle anti-ban",
            "$ghostping u - Silent ping & delete",
            "$tokencheck  - Check token validity",
            "$purge [n]   - Delete your last n msgs",
            "$nuke [n]    - Fast delete your n msgs",
            "$cleardms    - Clear recent DMs cache",
        ],
        "footer": "Client-side protection only"
    },
    "log": {
        "title": "LOGGER & SNIPE",
        "emoji": "L",
        "items": [
            "$logchat     - Toggle channel logging",
            "$logdm       - Toggle DM logging",
            "$sniped      - Last deleted msg",
            "$esniped     - Last edited msg",
            "$track @u    - Track user status DM",
            "$trackstop   - Stop all tracking",
            "$logs        - Show active loggers",
        ],
        "footer": "Logs stored in /logs"
    },
    "status": {
        "title": "PRESENCE",
        "emoji": "S",
        "items": [
            "$stats [t]   - Playing status",
            "$live [t]    - Streaming status",
            "$listen [t]  - Listening status",
            "$watch [t]   - Watching status",
            "$comp [t]    - Competing status",
            "$remstats    - Clear status",
            "$statusdnd   - Set status DND",
            "$statusidle  - Set status idle",
            "$statusonline - Online",
            "$statusinv   - Invisible",
        ],
        "footer": "Use quotes for multiword"
    },
    "text": {
        "title": "TEXT TRANSFORMS",
        "emoji": "T",
        "items": [
            "$mock [t]    - mOcK tExT",
            "$leet [t]    - 1337 5p34k",
            "$vapor [t]   - VAPORWAVE",
            "$zalgo [t]   - z a l g o",
            "$reverse [t] - txet esreveR",
            "$scramble t  - Scramble letters",
            "$expand [t]  - e x p a n d",
            "$space n [t] - s p a c e d",
            "$binary [t]  - Text to binary",
            "$unbinary b  - Binary to text",
            "$hex [t]     - Text to hex",
            "$unhex h     - Hex to text",
            "$b64e [t]    - Base64 encode",
            "$b64d [t]    - Base64 decode",
            "$cursive t   - 𝓬𝓾𝓻𝓼𝓲𝓿𝓮",
            "$bold [t]    - 𝖇𝖔𝖑𝖉",
            "$smallcaps t - sᴍᴀʟʟᴄᴀᴘs",
            "$upper [t]   - UPPER CASE",
            "$lower [t]   - lower case",
        ],
        "footer": "Reply to a msg to transform it"
    },
    "fun": {
        "title": "FUN & GAMES",
        "emoji": "F",
        "items": [
            "$8ball [q]   - Magic 8ball",
            "$flip        - Coin flip",
            "$roll [n]    - Dice roll (1-n)",
            "$choose o1;o2- Pick random",
            "$rps [r/p/s] - Rock paper scissors",
            "$say [t]     - Say text deletes cmd",
            "$echo [t]    - Echo text",
            "$embed t|d   - Rich embed",
            "$ascii [t]   - ASCII art text",
            "$clap [t]    - clap emoji between words",
            "$lmgtfy [q]  - LMGTFY link",
            "$rate [t]    - Random 1-10 rating",
            "$pp [@u]     - Meme pp size",
            "$howgay @u   - Meme gay detector",
            "$iq @u       - Meme IQ test",
            "$joke        - Random joke",
            "$fact        - Random fact",
            "$quote       - Random quote",
            "$kiss @u     - Kiss reaction",
            "$hug @u      - Hug reaction",
            "$slap @u     - Slap reaction",
            "$kill @u     - Kill reaction (joke)",
        ],
        "footer": "Fun only - no real data"
    },
    "util": {
        "title": "UTILITIES",
        "emoji": "U",
        "items": [
            "$ping        - Latency",
            "$uptime      - Uptime",
            "$avatar @u   - Big avatar",
            "$banner @u   - User banner",
            "$servericon  - Server icon",
            "$nick [name] - Change nickname",
            "$calc [exp]  - Math calculator",
            "$timestamp   - Current timestamp",
            "$poll q|o1|o2- Create poll",
            "$timer [s]   - Set reminder timer",
            "$remind s t  - Remind in s sec",
            "$color [hex] - Show color preview",
            "$qrcode [t]  - Generate QR link",
            "$shorten url - Shorten URL",
            "$define [w]  - Dictionary def",
            "$translate   - Simple translate",
            "$weather c   - Weather for city",
            "$ip [ip]     - IP info lookup",
            "$userid      - Get user ID",
            "$serverid    - Get server ID",
            "$chinfo      - Channel info",
            "$invite      - Create invite",
        ],
        "footer": "Some utilities use web APIs"
    },
    "info": {
        "title": "INFORMATION",
        "emoji": "i",
        "items": [
            "$userinfo @u - User details",
            "$serverinfo  - Server details",
            "$roleinfo r  - Role info",
            "$channelinfo - Channel info",
            "$perms @u    - Show permissions",
            "$botinfo     - Bot/self info",
            "$listroles   - List server roles",
            "$listbots    - List bots in server",
            "$listbans    - List bans (if allowed)",
            "$listinvites - List invites",
            "$listemojis  - List server emojis",
            "$whois @u    - Alias userinfo",
            "$members     - Member count",
        ],
        "footer": "Info is read-only"
    },
    "multi": {
        "title": "MULTI ACCOUNT",
        "emoji": "M",
        "items": [
            "$selfbot t n - Add token as name",
            "$selfbot     - List accounts",
            "$selfbotr n  - Remove account",
            "$selfbots n  - Switch control",
        ],
        "footer": "Each runs own event loop"
    },
    "ai": {
        "title": "AI CHAT",
        "emoji": "AI",
        "items": [
            "$aiadd e m k - Add endpoint/model/key",
            "$ailist      - List saved configs",
            "$air [n]     - Remove config #n",
            "$aiswitch n  - Switch active config",
            "$ai [q]      - Ask the active AI",
            "$hai         - This help menu",
        ],
        "footer": "OpenAI-compat APIs. Long/code -> file"
    },
}

def fancy_border(title, emoji):
    # Create fancy gradient-like border
    top = "╭─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━─╮"
    bottom = "╰─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━─╯"
    # fancy title line with emoji
    title_line = f"│ {emoji}  {title}  {emoji} │"
    return top, title_line, bottom

def render_menu(key):
    m = MENUS.get(key)
    if not m:
        return "Unknown menu"
    top, title_line, bottom = fancy_border(m['title'], m['emoji'])
    # subtitle for main
    lines = []
    lines.append(top)
    lines.append(title_line)
    if key == "main" and "subtitle" in m:
        lines.append(f"│ {m['subtitle']} │")
    lines.append("├─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━─┤")
    for it in m["items"]:
        # ensure we don't exceed 1900 chars, but keep formatting
        lines.append(f"│ {it}")
    lines.append("├─━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━─┤")
    lines.append(f"│ {m['footer']} │")
    lines.append(bottom)
    # Add extra fancy footer for main
    if key == "main":
        lines.append("")
        lines.append("  ✦ 𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1 ✦ 2026 EDITION ✦")
        lines.append("  ➤ $start @user1 @user2 spam_en.txt  (MULTI)")
        lines.append("  ➤ $start ionut vasile alex longspam_ro.txt")
    return "\n".join(lines)

def register(b, state):
    """Register all help commands on bot `b`."""

    async def show(ctx, key, delete_after=25):
        await del_msg(ctx.message)
        await safe_send(ctx, code_block(render_menu(key)), delete_after=delete_after)

    @b.command(name="REDHELP", aliases=["help", "h"])
    async def _help(ctx):
        track_cmd("help")
        await show(ctx, "main", delete_after=40)

    @b.command(name="hcore")
    async def _hcore(ctx): await show(ctx, "core")
    @b.command(name="hmusic")
    async def _hmus(ctx): await show(ctx, "music")
    @b.command(name="hspam")
    async def _hsp(ctx): await show(ctx, "spam", delete_after=40)
    @b.command(name="hprofile")
    async def _hpr(ctx): await show(ctx, "profile")
    @b.command(name="hclone")
    async def _hcl(ctx): await show(ctx, "clone")
    @b.command(name="harchive")
    async def _har(ctx): await show(ctx, "archive")
    @b.command(name="hprotect")
    async def _hpt(ctx): await show(ctx, "protect")
    @b.command(name="hlog")
    async def _hlg(ctx): await show(ctx, "log")
    @b.command(name="hstatus")
    async def _hst(ctx): await show(ctx, "status")
    @b.command(name="htext")
    async def _htx(ctx): await show(ctx, "text")
    @b.command(name="hfun")
    async def _hfn(ctx): await show(ctx, "fun")
    @b.command(name="hutil")
    async def _hut(ctx): await show(ctx, "util")
    @b.command(name="hinfo")
    async def _hin(ctx): await show(ctx, "info")
    @b.command(name="hmulti")
    async def _hml(ctx): await show(ctx, "multi")
    @b.command(name="hai")
    async def _hai(ctx): await show(ctx, "ai")

    @b.command(name="hall")
    async def _hall(ctx):
        """All commands in one long message (may be >2000, so chunk)."""
        track_cmd("hall")
        await del_msg(ctx.message)
        parts = []
        for key in ["core", "music", "spam", "profile", "clone", "archive",
                    "protect", "log", "status", "text", "fun", "util", "info", "ai", "multi"]:
            parts.append(render_menu(key))
            parts.append("")
        full = "\n".join(parts)
        # Chunk at ~1900
        chunks = []
        cur = ""
        for line in full.split("\n"):
            if len(cur) + len(line) + 1 > 1800:
                chunks.append(cur)
                cur = line
            else:
                cur += "\n" + line if cur else line
        if cur:
            chunks.append(cur)
        for i, ch in enumerate(chunks):
            await safe_send(ctx, code_block(ch), delete_after=(20 if i < len(chunks)-1 else 50))

    # Simple text-only info commands
    @b.command(name="prefix")
    async def _prefix(ctx):
        track_cmd("prefix")
        await del_msg(ctx.message)
        await safe_send(ctx, f"Current prefix: `{PREFIX}`", delete_after=8)

    @b.command(name="about")
    async def _about(ctx):
        track_cmd("about")
        await del_msg(ctx.message)
        about_txt = (
            "╭─ 𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1 ─╮\n"
            "│ 2026 EDITION - Premium build │\n"
            "│ Written by RedGlitchX • Fancy gradient │\n"
            f"│ Python {platform.python_version()} • discord.py-self │\n"
            "│ Multi-user $start: $start @u1 @u2 file │\n"
            "│ Dashboard: 0.0.0.0:3000 (PORT env) │\n"
            "╰──────────────────────────────╯\n"
            "All commands: $help"
        )
        await safe_send(ctx, code_block(about_txt), delete_after=15)

    @b.command(name="dashboard")
    async def _dash(ctx):
        track_cmd("dashboard")
        await del_msg(ctx.message)
        port = os.environ.get("PORT", "3000")
        await safe_send(ctx, f"Dashboard running on `0.0.0.0:{port}` • http://localhost:{port} • Preview: / (host header allowed)", delete_after=12)
