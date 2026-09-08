# -*- coding: utf-8 -*-
"""Automation / sequence commands - multi-user + new packs 2026."""
from utils.common import *
import re

# Default generic messages for $start (used if no data files exist at all)
DEFAULT_MESSAGES = ["Sequence active.", "Red Selfbot V1 online.", "Hey!", "Anyone around?", "Wake up!"]

def list_seq_files():
    """Return list of available .txt line files (data/*.txt + botjura.txt). Sorted fancy."""
    files = []
    if os.path.isdir("data"):
        for f in os.listdir("data"):
            if f.lower().endswith(".txt"):
                files.append(os.path.join("data", f))
    if os.path.exists("botjura.txt"):
        files.append("botjura.txt")
    # sort: spam_ro, spam_en, longspam, lines_, etc first
    def sort_key(p):
        b = os.path.basename(p).lower()
        order = {
            "spam.txt": 0,
            "spam_ro.txt": 1,
            "spam_en.txt": 2,
            "longspam_ro.txt": 3,
            "longspam_en.txt": 4,
            "lines_ro.txt": 5,
            "lines_en.txt": 6,
            "lines_default.txt": 7,
            "botjura.txt": 8,
        }
        return (order.get(b, 99), b)
    files.sort(key=sort_key)
    return files

def resolve_seq_file(name):
    """Find a line file by short name, with or without .txt prefix. Returns path or None."""
    if not name:
        return None
    name = name.strip()
    # direct path exists
    if os.path.isfile(name):
        return name
    # clean
    candidates = [
        name,
        f"data/{name}",
        f"data/{name}.txt" if not name.endswith(".txt") else None,
        f"data/lines_{name}.txt",
        f"data/spam_{name}.txt",
        f"data/longspam_{name}.txt",
    ]
    # also try lower
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    # try with lower case
    low = name.lower()
    for c in candidates:
        if c and os.path.isfile(c.lower()):
            return c.lower()
        if c and os.path.isfile(c):
            return c
    # fuzzy search: list all files and do substring match
    for f in list_seq_files():
        base = os.path.basename(f).lower()
        name_low = low
        # exact base
        if name_low == base:
            return f
        # name without ext matches base without ext
        if name_low == os.path.splitext(base)[0]:
            return f
        # substring
        if name_low in base:
            return f
        # also handle like "ro" -> spam_ro.txt
        if name_low in ["ro", "romana", "romanian"]:
            if "spam_ro" in base or "lines_ro" in base or "ro.txt" in base:
                # prefer spam_ro first
                if "spam_ro" in base:
                    return f
        if name_low in ["en", "eng", "english"]:
            if "spam_en" in base or "lines_en" in base:
                if "spam_en" in base:
                    return f
    # second pass for ro/en
    for f in list_seq_files():
        base = os.path.basename(f).lower()
        if low in ["ro", "romana"] and "ro" in base:
            return f
        if low in ["en", "english"] and "en" in base:
            return f
    return None

def load_lines(path=None):
    """Load lines from a file; fall back to default RO botjura then hardcoded defaults.
    Also strips legacy '> #' prefix if present.
    """
    for cand in filter(None, [path, "botjura.txt", "data/lines_default.txt", "data/spam.txt"]):
        if os.path.exists(cand):
            try:
                with open(cand, "r", encoding="utf-8", errors="replace") as fh:
                    lines = []
                    for l in fh:
                        raw = l.rstrip("\r\n")
                        if not raw.strip():
                            continue
                        # strip legacy "> # " prefix if user asked to remove it
                        s = raw.lstrip()
                        if s.startswith("> #"):
                            s = s[3:].lstrip()
                        elif s.startswith(">"):
                            s = s[1:].lstrip()
                        elif s.startswith("#"):
                            # keep # if it's not the spam prefix? we strip only if it looks like comment prefix
                            # but user said fara > # - so if line starts with > # we already handled
                            pass
                            s = raw
                        else:
                            s = raw
                        # final strip but keep content
                        if s.strip():
                            lines.append(s.strip())
                    if lines:
                        return lines
            except Exception:
                pass
    return list(DEFAULT_MESSAGES)

async def resolve_single_user(ctx, token):
    """Resolve one token to a user/member or None."""
    if not token:
        return None
    tok = token.strip()
    if not tok:
        return None
    # mention <@!123> or <@123>
    m = re.match(r'^<@!?(\d+)>$', tok)
    if m:
        uid = int(m.group(1))
        u = None
        if ctx.guild:
            u = ctx.guild.get_member(uid)
        if not u:
            u = ctx.bot.get_user(uid)
        if not u:
            try:
                u = await ctx.bot.fetch_user(uid)
            except Exception:
                u = None
        return u
    # plain numeric id
    if tok.isdigit() and len(tok) >= 15:
        try:
            uid = int(tok)
            u = None
            if ctx.guild:
                u = ctx.guild.get_member(uid)
            if not u:
                u = ctx.bot.get_user(uid)
            if not u:
                try:
                    u = await ctx.bot.fetch_user(uid)
                except Exception:
                    u = None
            return u
        except Exception:
            return None
    # @username or plain name
    clean = tok.lstrip('@').strip()
    if not clean:
        return None
    low = clean.lower()
    # exact match in guild
    if ctx.guild:
        for mem in ctx.guild.members:
            if mem.name.lower() == low or (mem.nick and mem.nick.lower() == low):
                return mem
        # partial
        for mem in ctx.guild.members:
            if low in mem.name.lower() or (mem.nick and low in mem.nick.lower()):
                return mem
        # display name contains
        for mem in ctx.guild.members:
            try:
                if low in mem.display_name.lower():
                    return mem
            except Exception:
                pass
    # cache users
    for u in ctx.bot.users:
        if u.name.lower() == low:
            return u
    for u in ctx.bot.users:
        if low in u.name.lower():
            return u
    return None

def register(b, state):

    async def run_spam(channel, targets, lines, delay=0.8, file_label=None):
        """Background spam loop. Supports multiple targets."""
        state["spam_channels"].add(channel.id)
        state["active_spam_channel"] = channel.id
        # Build mention string
        if targets:
            mentions = " ".join(t.mention for t in targets if hasattr(t, 'mention'))
        else:
            mentions = ""
        idx = 0
        try:
            while state["spamming"] and channel.id in state.get("spam_channels", set()):
                raw = lines[idx % len(lines)]
                idx += 1
                # handle {t} placeholder
                if "{t}" in raw:
                    if mentions:
                        msg = raw.replace("{t}", mentions)
                    else:
                        msg = raw.replace("{t}", "").strip()
                else:
                    if mentions:
                        msg = f"{mentions} {raw}"
                    else:
                        msg = raw
                msg = msg.strip()
                if not msg:
                    continue
                # Discord limit
                if len(msg) > 1999:
                    msg = msg[:1999]
                try:
                    await channel.send(msg)
                except discord.Forbidden:
                    break
                except discord.HTTPException as e:
                    if getattr(e, "code", None) == 429:
                        ra = getattr(e, "retry_after", 5) or 5
                        await asyncio.sleep(ra)
                        continue
                    await asyncio.sleep(2)
                except Exception:
                    await asyncio.sleep(2)
                await asyncio.sleep(delay + random.uniform(-0.1, 0.25))
        except asyncio.CancelledError:
            pass
        finally:
            state["spam_channels"].discard(channel.id)
            if state.get("active_spam_channel") == channel.id:
                state["active_spam_channel"] = None

    @b.command(name="start")
    async def _start(ctx, *, args: str = None):
        """
        $start [user1] [user2] ... [file]
        Examples:
          $start
          $start @user
          $start @user1 @user2 @user3
          $start ionut vasile alex data/longspam_en.txt
          $start 123456789 ro
          $start en.txt
          $start @user en
        """
        track_cmd("start"); await del_msg(ctx.message)
        filepath = None
        tokens = []
        if args:
            tokens = args.strip().split()

        # Detect file at the end
        if tokens:
            last = tokens[-1]
            path = resolve_seq_file(last)
            if path:
                filepath = path
                tokens = tokens[:-1]
            else:
                # also try last two tokens combined? like "data/longspam_en.txt" might be split? No, it's one token
                pass

        # If tokens empty, no targets
        targets = []
        # Add mentions from message first (discord.py parses them)
        if ctx.message.mentions:
            for m in ctx.message.mentions:
                if m.id != b.user.id and m not in targets:
                    targets.append(m)

        # Resolve remaining tokens as users
        for tok in tokens:
            # skip if token already resolved as mention id
            # if tok is mention string, it would have been handled but we also resolve
            u = await resolve_single_user(ctx, tok)
            if u and u.id != b.user.id and u not in targets:
                # avoid duplicates by id
                if not any(x.id == u.id for x in targets):
                    targets.append(u)

        # Limit to 10
        if len(targets) > 10:
            targets = targets[:10]

        # Choose default file based on current start_lang if set
        if not filepath:
            lang = state.get("start_lang", "")
            if lang:
                filepath = resolve_seq_file(lang) or resolve_seq_file(f"lines_{lang}")
            if not filepath:
                # prefer spam.txt if exists, else botjura.txt
                if os.path.exists("data/spam.txt"):
                    filepath = "data/spam.txt"
                elif os.path.exists("botjura.txt"):
                    filepath = "botjura.txt"
                else:
                    filepath = "data/lines_default.txt"

        lines = load_lines(filepath)
        # Stop any existing spam in this channel
        state["spam_channels"].discard(ctx.channel.id)
        state["spamming"] = True
        b.loop.create_task(run_spam(ctx.channel, targets, lines, file_label=filepath))

        if targets:
            names = ", ".join(f"@{t.name}" for t in targets[:3])
            if len(targets) > 3:
                names += f" +{len(targets)-3} more"
            await safe_send(ctx, f"Sequence started for {names} (`{os.path.basename(filepath)}`, {len(lines):,} lines, {len(targets)} users). $stop to stop.", delete_after=7)
        else:
            await safe_send(ctx, f"Sequence started (`{os.path.basename(filepath)}`, {len(lines):,} lines). $stop to stop.", delete_after=6)

    @b.command(name="stop")
    async def _stop(ctx):
        track_cmd("stop"); await del_msg(ctx.message)
        state["spamming"] = False
        state["spam_channels"].clear()
        state["spam_scope"] = None
        state["autoreact"] = False
        await safe_send(ctx, "Stopped.", delete_after=3)

    @b.command(name="startl")
    async def _startl(ctx):
        track_cmd("startl"); await del_msg(ctx.message)
        files = list_seq_files()
        if not files:
            return await safe_send(ctx, "No .txt line files found. Drop files in data/ or edit botjura.txt.", delete_after=10)
        lines_out = []
        lines_out.append("╭─ 𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 - LINE PACKS ─╮")
        for i, f in enumerate(files, 1):
            try:
                sz = os.path.getsize(f)/1024
            except:
                sz = 0
            lc = 0
            try:
                with open(f, "rb") as fh:
                    for _ in fh: lc += 1
            except Exception:
                pass
            tag = ""
            if f == "botjura.txt":
                tag = " (default legacy)"
            elif os.path.basename(f) == f"lines_{state.get('start_lang','default')}.txt" and state.get("start_lang"):
                tag = f" (lang={state.get('start_lang')})"
            elif "spam_ro" in f:
                tag = " [RO SHORT]"
            elif "spam_en" in f:
                tag = " [EN SHORT + GIFS]"
            elif "longspam_ro" in f:
                tag = " [RO LONG 2026]"
            elif "longspam_en" in f:
                tag = " [EN LONG 2026 + GIFS]"
            elif "spam.txt" in f:
                tag = " [MIX]"
            lines_out.append(f"  {i:2d}. {f} [{lc:,} lines, {sz:.1f} KB]{tag}")
        lines_out.append("╰────────────────────────────────╯")
        lines_out.append("")
        lines_out.append("Usage (multi-user supported):")
        lines_out.append("  $start                          - spam default file")
        lines_out.append("  $start @user                    - spam default, pinging @user")
        lines_out.append("  $start @u1 @u2 @u3              - spam 3 users at once")
        lines_out.append("  $start ionut vasile alex en.txt - 3 names + file at end")
        lines_out.append("  $start @user en.txt             - spam en.txt pinging @user")
        lines_out.append("  $start en.txt                   - spam en.txt no mention")
        lines_out.append("  $start ro                       - short for spam_ro / lines_ro")
        lines_out.append("  $startlang <name>               - set default language/file")
        lines_out.append("")
        lines_out.append("New packs: spam_ro, spam_en, longspam_ro, longspam_en, spam")
        lines_out.append("Drop any .txt into data/ and it appears instantly.")
        await safe_send(ctx, code_block("\n".join(lines_out)), delete_after=45)

    @b.command(name="startlang")
    async def _startlang(ctx, lang: str = None):
        track_cmd("startlang"); await del_msg(ctx.message)
        if not lang:
            files = [f for f in os.listdir("data") if f.endswith(".txt")] if os.path.isdir("data") else []
            msg = "Current default: " + (state.get("start_lang","botjura.txt / spam.txt")) + "\n"
            msg += "Available: " + (", ".join(files) if files else "(none)")
            return await safe_send(ctx, msg, delete_after=15)
        path = resolve_seq_file(lang)
        if not path:
            return await safe_send(ctx, f"No file matching '{lang}'. Use $startl to list files.", delete_after=8)
        state["start_lang"] = lang
        await safe_send(ctx, f"Default line file set to '{lang}' -> {path}.", delete_after=10)

    @b.command(name="spam")
    async def _spam(ctx, *, text_and_args: str = None):
        """$spam [text] [count] [delay] — count & delay are trailing numbers."""
        track_cmd("spam"); await del_msg(ctx.message)
        if not text_and_args:
            return await safe_send(ctx, "$spam [text] [count] [delay]", delete_after=5)
        # Trailing two optional numbers
        m = re.match(r"^(.*?)(?:\s+(\d+))?(?:\s+(\d+(?:\.\d+)?))?\s*$", text_and_args)
        text = m.group(1).strip() if m else text_and_args
        count = int(m.group(2)) if m and m.group(2) else 5
        delay = float(m.group(3)) if m and m.group(3) else 0.5
        if not text:
            return await safe_send(ctx, "$spam [text] [count] [delay]", delete_after=5)
        count = max(1, min(count, 30))
        delay = max(0.3, min(delay, 10))
        for _ in range(count):
            try: await ctx.send(text)
            except: break
            await asyncio.sleep(delay)

    @b.command(name="spamall")
    async def _spamall(ctx, msg: str = None, count: int = 3):
        track_cmd("spamall"); await del_msg(ctx.message)
        if not ctx.guild or not msg:
            return await safe_send(ctx, "$spamall [msg] [count] (servers only)", delete_after=5)
        count = max(1, min(count, 10))
        sent = 0
        me = ctx.me if hasattr(ctx, "me") else ctx.author
        for ch in ctx.guild.text_channels:
            try:
                perms = ch.permissions_for(me)
                if not perms.send_messages: continue
                for _ in range(count):
                    await ch.send(msg)
                    await asyncio.sleep(0.8)
                sent += 1
            except Exception:
                pass
        await safe_send(ctx, f"Sent to {sent} channels.", delete_after=8)

    @b.command(name="flood")
    async def _flood(ctx, count: int = 10):
        track_cmd("flood"); await del_msg(ctx.message)
        count = max(1, min(count, 25))
        for i in range(count):
            try: await ctx.send(f"flood {i+1}/{count}")
            except: break
            await asyncio.sleep(0.3)

    @b.command(name="dmspam")
    async def _dmspam(ctx, user: str = None, count: int = 5, *, msg: str = "Hello"):
        track_cmd("dmspam"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention a user.", delete_after=5)
        count = max(1, min(count, 20))
        try:
            dm = await t.create_dm()
            for _ in range(count):
                await dm.send(msg)
                await asyncio.sleep(1)
            await safe_send(ctx, f"Sent {count} DMs to {t.name}.", delete_after=5)
        except Exception as e:
            await safe_send(ctx, f"Failed: {e}", delete_after=8)

    @b.command(name="react")
    async def _react(ctx, emoji: str = None, count: int = 1):
        track_cmd("react"); await del_msg(ctx.message)
        if not emoji: return await safe_send(ctx, "$react [emoji] [count]", delete_after=5)
        target = None
        if ctx.message.reference and ctx.message.reference.resolved:
            target = ctx.message.reference.resolved
        else:
            async for m in ctx.channel.history(limit=5):
                if m.id != ctx.message.id and m.author != b.user:
                    target = m; break
        if not target: return await safe_send(ctx, "No message to react to.", delete_after=5)
        count = max(1, min(count, 1))
        for _ in range(count):
            try: await target.add_reaction(emoji)
            except Exception as e:
                await safe_send(ctx, f"Failed: {e}", delete_after=5); return
        await safe_send(ctx, "Reacted.", delete_after=3)

    @b.command(name="repeat")
    async def _repeat(ctx, count: int = 1):
        track_cmd("repeat"); await del_msg(ctx.message)
        target = None
        async for m in ctx.channel.history(limit=10):
            if m.author == b.user and m.id != ctx.message.id:
                target = m; break
        if not target: return await safe_send(ctx, "Nothing to repeat.", delete_after=5)
        count = max(1, min(count, 10))
        for _ in range(count):
            await ctx.send(target.content)
            await asyncio.sleep(0.5)

    @b.command(name="autoreact")
    async def _autoreact(ctx, emoji: str = None):
        track_cmd("autoreact"); await del_msg(ctx.message)
        if not emoji:
            state["autoreact"] = not state.get("autoreact", False)
            state["autoreact_emoji"] = None
            await safe_send(ctx, f"Autoreact: {'on' if state['autoreact'] else 'off'}.", delete_after=5)
            return
        state["autoreact"] = True
        state["autoreact_emoji"] = emoji
        await safe_send(ctx, f"Autoreact enabled with {emoji}.", delete_after=8)

    @b.command(name="massmention")
    async def _mass(ctx):
        track_cmd("massmention"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        mentions = []
        me_id = b.user.id
        for m in ctx.guild.members:
            if m.bot or m.id == me_id: continue
            if m.status != discord.Status.offline:
                mentions.append(m.mention)
            if len(mentions) >= 30: break
        if not mentions: return await safe_send(ctx, "No online members.", delete_after=5)
        await ctx.send(" ".join(mentions))

    @b.listen("on_message")
    async def autoreact_listener(message):
        if message.author == b.user: return
        if state.get("autoreact") and state.get("autoreact_emoji"):
            if message.channel.id in state.get("spam_channels", set()):
                return
            try:
                await message.add_reaction(state["autoreact_emoji"])
            except Exception:
                pass
