# -*- coding: utf-8 -*-
"""Automation / sequence commands."""
from utils.common import *

# Default generic messages for $start (used if no data files exist at all)
DEFAULT_MESSAGES = ["Sequence active.", "Red Selfbot V1 online.", "Hey!", "Anyone around?", "Wake up!"]

def list_seq_files():
    """Return list of available .txt line files (data/*.txt + botjura.txt)."""
    files = []
    if os.path.isdir("data"):
        for f in os.listdir("data"):
            if f.lower().endswith(".txt"):
                files.append(os.path.join("data", f))
    if os.path.exists("botjura.txt"):
        files.append("botjura.txt")
    return files

def resolve_seq_file(name):
    """Find a line file by short name, with or without .txt prefix. Returns path or None."""
    if not name:
        return None
    name = name.strip()
    candidates = [
        name,
        f"data/{name}",
        f"data/{name}.txt" if not name.endswith(".txt") else None,
        f"data/lines_{name}.txt",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    # fuzzy search: list all files and do substring match
    for f in list_seq_files():
        base = os.path.basename(f).lower()
        if name.lower() == base:
            return f
        if name.lower() in base:
            return f
    return None

def load_lines(path=None):
    """Load lines from a file; fall back to default RO botjura then hardcoded defaults."""
    for cand in filter(None, [path, "botjura.txt", "data/lines_default.txt"]):
        if os.path.exists(cand):
            try:
                with open(cand, "r", encoding="utf-8", errors="replace") as f:
                    lines = [l.rstrip("\r\n") for l in f if l.strip()]
                if lines:
                    return lines
            except Exception:
                pass
    return list(DEFAULT_MESSAGES)

def resolve_target_from_text(ctx, text):
    """Given a chunk of text, try to extract a user mention/ID and return (user, rest)."""
    if not text:
        return (None, "")
    import re as _re
    # discord mention <@!123> or <@123>
    m = _re.match(r"^\s*<@!?(\d+)>\s*(.*)$", text)
    if m:
        uid = int(m.group(1))
        rest = m.group(2).strip()
        try:
            if ctx.guild:
                mem = ctx.guild.get_member(uid)
                if mem:
                    return (mem, rest)
            u = ctx.bot.get_user(uid)
            if not u:
                u = asyncio.run_coroutine_threadsafe(ctx.bot.fetch_user(uid), ctx.bot.loop).result()
            if u:
                return (u, rest)
        except Exception:
            pass
    # plain numeric id
    m = _re.match(r"^\s*(\d{15,20})\s*(.*)$", text)
    if m:
        uid = int(m.group(1))
        rest = m.group(2).strip()
        try:
            if ctx.guild:
                mem = ctx.guild.get_member(uid)
                if mem:
                    return (mem, rest)
            u = ctx.bot.get_user(uid)
            if not u:
                u = asyncio.run_coroutine_threadsafe(ctx.bot.fetch_user(uid), ctx.bot.loop).result()
            if u:
                return (u, rest)
        except Exception:
            pass
    # mention by word starting with @
    if text.lstrip().startswith("@"):
        # grab the @word
        mm = _re.match(r"^\s*@(\S+)\s*(.*)$", text)
        if mm:
            uname = mm.group(1)
            rest = mm.group(2).strip()
            if ctx.guild:
                low = uname.lower()
                for mem in ctx.guild.members:
                    if mem.name.lower() == low or (mem.nick and mem.nick.lower() == low) or \
                       str(mem).lower().startswith(low):
                        return (mem, rest)
            # try by username in client cache
            for u in ctx.bot.users:
                if u.name.lower() == low or str(u).lower().startswith(low):
                    return (u, rest)
    return (None, text)

def register(b, state):

    async def run_spam(channel, target, lines, delay=0.8, file_label=None):
        """Background spam loop. If target is set, substitute {t} with target.mention; else strip {t}."""
        state["spam_channels"].add(channel.id)
        state["active_spam_channel"] = channel.id
        mention = target.mention if target else ""
        count = 0
        idx = 0
        try:
            while state["spamming"] and channel.id in state.get("spam_channels", set()):
                raw = lines[idx % len(lines)]
                idx += 1
                if target and "{t}" in raw:
                    msg = raw.replace("{t}", mention)
                elif target:
                    msg = f"{mention} {raw}"
                else:
                    msg = raw.replace("{t}", "").strip()
                if not msg:
                    continue
                try:
                    await channel.send(msg[:1999])
                    count += 1
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
                # small random jitter
                await asyncio.sleep(delay + random.uniform(-0.1, 0.25))
        except asyncio.CancelledError:
            pass
        finally:
            state["spam_channels"].discard(channel.id)
            if state.get("active_spam_channel") == channel.id:
                state["active_spam_channel"] = None

    @b.command(name="start")
    async def _start(ctx, *, args: str = None):
        track_cmd("start"); await del_msg(ctx.message)
        target = None
        filepath = None
        rest = args or ""
        # Resolve possible user at the start
        if rest:
            maybe_t, after = await b.loop.run_in_executor(None, lambda: resolve_target_from_text(ctx, rest))
            # can't do blocking fetch in executor cleanly; do it manually with the ctx:
            # Re-do it async here for fetches
            import re as _re
            uid = None
            rem = rest
            m = _re.match(r"^\s*<@!?(\d+)>\s*(.*)$", rest)
            if m:
                uid = int(m.group(1)); rem = m.group(2).strip()
            else:
                m = _re.match(r"^\s*(\d{15,20})\s*(.*)$", rest)
                if m:
                    uid = int(m.group(1)); rem = m.group(2).strip()
            if uid:
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
                if u:
                    target = u
                else:
                    rem = rest  # invalid id - treat as text
            else:
                # @username prefix
                m = _re.match(r"^\s*@(\S+)\s*(.*)$", rest)
                if m:
                    un = m.group(1); rem = m.group(2).strip()
                    found = None
                    if ctx.guild:
                        low = un.lower()
                        for mem in ctx.guild.members:
                            if mem.name.lower() == low or (mem.nick and mem.nick.lower() == low):
                                found = mem; break
                    if not found:
                        for u in ctx.bot.users:
                            if u.name.lower() == un.lower():
                                found = u; break
                    if found:
                        target = found
                    else:
                        rem = rest  # unknown @name - treat as plaintext
        # Now `rem` is the text after the user (if any). First token could be a filename.
        if rem:
            tok = rem.split()[0]
            path = resolve_seq_file(tok)
            if path:
                filepath = path
            # else no file arg - use default
        # Choose default file based on current start_lang if set
        if not filepath:
            lang = state.get("start_lang", "")
            if lang:
                filepath = resolve_seq_file(lang) or resolve_seq_file(f"lines_{lang}")
            if not filepath:
                filepath = "botjura.txt" if os.path.exists("botjura.txt") else "data/lines_default.txt"
        lines = load_lines(filepath)
        # Stop any existing spam in this channel
        state["spam_channels"].discard(ctx.channel.id)
        state["spamming"] = True
        b.loop.create_task(run_spam(ctx.channel, target, lines, file_label=filepath))
        tgt_name = f" @{target.name}" if target else ""
        await safe_send(ctx, f"Sequence started{tgt_name} (`{os.path.basename(filepath)}`, {len(lines):,} lines). $stop to stop.", delete_after=6)

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
        lines = ["Available line files:"]
        for i, f in enumerate(files, 1):
            sz = os.path.getsize(f)/1024
            lc = 0
            try:
                with open(f, "rb") as fh:
                    for _ in fh: lc += 1
            except Exception:
                pass
            tag = ""
            if f == "botjura.txt":
                tag = " (default)"
            elif os.path.basename(f) == f"lines_{state.get('start_lang','default')}.txt" and state.get("start_lang"):
                tag = f" (lang={state.get('start_lang')})"
            lines.append(f"  {i:2d}. {f}  [{lc:,} lines, {sz:.1f} KB]{tag}")
        lines.append("")
        lines.append("Usage:")
        lines.append("  $start                  - spam default file")
        lines.append("  $start @user            - spam default, pinging @user")
        lines.append("  $start @user en.txt     - spam en.txt pinging @user")
        lines.append("  $start en.txt           - spam en.txt no mention")
        lines.append("  $startlang <name>       - set default language/file")
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=40)

    @b.command(name="startlang")
    async def _startlang(ctx, lang: str = None):
        track_cmd("startlang"); await del_msg(ctx.message)
        if not lang:
            files = [f for f in os.listdir("data") if f.startswith("lines_") and f.endswith(".txt")] if os.path.isdir("data") else []
            msg = "Current default: " + (state.get("start_lang","botjura.txt")) + "\n"
            msg += "Available: " + (", ".join(f.replace("lines_","").replace(".txt","") for f in files) if files else "(none)")
            return await safe_send(ctx, msg, delete_after=15)
        # Validate that the file exists
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
        import re as _re
        # Trailing two optional numbers
        m = _re.match(r"^(.*?)(?:\s+(\d+))?(?:\s+(\d+(?:\.\d+)?))?\s*$", text_and_args)
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
