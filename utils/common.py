# -*- coding: utf-8 -*-
"""Shared utilities for Red Selfbot V1."""
import os, time, random, re, json, asyncio, datetime, platform, traceback
import requests
import discord
from discord.ext import commands as _dpy_commands

PREFIX = "$"
START_TIME = time.time()
COMMAND_USAGE = {}

# Every cmds/* module does `from utils.common import *` and relies on these
# names leaking through, so the contract is declared explicitly. Keeping it
# spelled out also lets linters resolve the star import and catch real typos.
__all__ = [
    # Re-exported standard library / third-party modules used across cmds/*
    "os", "time", "random", "re", "json", "asyncio", "datetime", "platform",
    "traceback", "base64", "requests", "discord",
    # Globals
    "PREFIX", "START_TIME", "COMMAND_USAGE", "IS_SELF_FORK",
    # Discord library compatibility
    "get_intents", "make_bot", "discord_lib_name", "warn_if_wrong_library",
    "SELF_BOT_CAPABLE", "LIBRARY_WARNING", "LOGIN_ERRORS",
    # Storage / helpers
    "save_json", "load_json", "track_cmd", "fmt_time", "code_block",
    "del_msg", "safe_send", "get_user",
    # Text transforms
    "mock_text", "leet", "vaporwave", "zalgo", "reverse_text", "expand_text",
    "space_text", "to_binary", "from_binary", "to_hex", "from_hex",
    "b64_encode", "b64_decode", "scramble_word", "scramble_text",
    "to_cursive", "to_bold", "to_smallcaps",
]

# ============== DISCORD LIBRARY COMPAT ==============
# The bot runs on stock discord.py 2.x *and* on the discord.py-self fork.
# The two disagree about a few constructor options (self forks dropped
# `discord.Intents` entirely), so everything is negotiated here instead of
# being hardcoded at the call sites.
IS_SELF_FORK = not hasattr(discord, "Intents")


def get_intents():
    """Return full Intents for stock discord.py, or None on self forks."""
    intents_cls = getattr(discord, "Intents", None)
    if intents_cls is None:
        return None
    try:
        intents = intents_cls.all()
    except Exception:
        return None
    # `typing` is not an intent flag on every version; never die over it.
    try:
        intents.typing = False
    except Exception:
        pass
    return intents


def make_bot(prefix=PREFIX, **extra):
    """
    Build the selfbot `commands.Bot`.

    * `help_command=None` disables discord.py's built-in help command. Without
      it, registering $REDHELP with a "help" alias raises
      CommandRegistrationError("The alias help is already an existing command
      or alias") and the bot never starts.
    * `intents` is only passed when the installed library supports it.
    * Any kwarg the installed library rejects is dropped and retried, so an
      option that exists in one fork but not the other can't kill the boot.
    """
    kwargs = {"command_prefix": prefix, "help_command": None}
    intents = get_intents()
    if intents is not None:
        kwargs["intents"] = intents
    kwargs["self_bot"] = True
    if not IS_SELF_FORK:
        kwargs["guild_subscriptions"] = True
    kwargs.update(extra)

    dropped = []
    for _ in range(len(kwargs) + 1):
        try:
            bot = _dpy_commands.Bot(**kwargs)
        except TypeError as exc:
            bad = _rejected_kwarg(exc, kwargs)
            if bad is None:
                raise
            dropped.append(bad)
            kwargs.pop(bad)
            continue
        if dropped:
            print(f"[i] Ignoring options unsupported by discord {discord.__version__}: "
                  f"{', '.join(dropped)}")
        return bot
    raise TypeError(f"Could not construct commands.Bot (dropped: {', '.join(dropped) or 'none'})")


def _rejected_kwarg(exc, kwargs):
    """Pull the offending kwarg name out of a TypeError, if it names one."""
    text = str(exc)
    for name in kwargs:
        if f"'{name}'" in text or f'"{name}"' in text:
            return name
    return None


def discord_lib_name():
    """Best-effort distribution name of the installed discord library."""
    try:
        from importlib import metadata
    except ImportError:
        return None
    for candidate in ("discord.py-self", "discord.py-self-next", "discord.py",
                      "discord", "nextcord", "py-cord"):
        try:
            metadata.version(candidate)
            return candidate
        except Exception:
            continue
    return None


# Stock discord.py >= 2.0 dropped self-bot support entirely: it authenticates
# with `Authorization: Bot <token>` and sends a bot-shaped gateway IDENTIFY, so a
# *user* token is rejected with LoginFailure("Improper token has been passed").
# Only the discord.py-self fork performs the user-account handshake this bot needs.
SELF_BOT_CAPABLE = IS_SELF_FORK or (discord_lib_name() or "").lower() in (
    "discord.py-self", "discord.py-self-next",
)

# Exception classes that exist in only one of the two supported libraries
# (discord.py-self has no PrivilegedIntentsRequired). Building the tuple up front
# keeps `except` clauses from raising AttributeError while handling an error.
LOGIN_ERRORS = tuple(
    cls for cls in (
        getattr(discord, "LoginFailure", None),
        getattr(discord, "PrivilegedIntentsRequired", None),
        getattr(discord, "GatewayNotFound", None),
    )
    if isinstance(cls, type) and issubclass(cls, Exception)
)

LIBRARY_WARNING = (
    "[!] WRONG DISCORD LIBRARY INSTALLED\n"
    "[!] Detected: {lib} {ver}\n"
    "[!]\n"
    "[!] This is a SELFBOT - it logs in with a user token. Stock discord.py 2.x\n"
    "[!] removed self-bot support and always authenticates as 'Bot <token>', so\n"
    "[!] login will fail with \"Improper token has been passed\" no matter what.\n"
    "[!]\n"
    "[!] Fix it with:\n"
    "[!]     pip uninstall -y discord.py discord\n"
    "[!]     pip install -U \"discord.py-self>=2.0.0,<3.0.0\"\n"
    "[!]\n"
    "[!] (requirements.txt already lists the correct package.)"
)


def warn_if_wrong_library():
    """Print an actionable warning when the installed fork cannot drive a user account."""
    if SELF_BOT_CAPABLE:
        print(f"[i] discord library: {discord_lib_name() or 'unknown'} {discord.__version__} (self-bot capable)")
        return True
    print(LIBRARY_WARNING.format(
        lib=discord_lib_name() or "discord.py",
        ver=getattr(discord, "__version__", "?"),
    ))
    return False

# ============== STORAGE ==============
for _d in ["music", "profiles", "clones", "archives", "logs", "data"]:
    os.makedirs(_d, exist_ok=True)

def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def track_cmd(name):
    COMMAND_USAGE[name] = COMMAND_USAGE.get(name, 0) + 1

def fmt_time(seconds):
    d, r = divmod(int(seconds), 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    parts = []
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)

def code_block(text, lang=""):
    text = str(text)
    if len(text) > 1990:
        text = text[:1990] + "..."
    return f"```{lang}\n{text}\n```"

async def del_msg(msg):
    try:
        await msg.delete()
    except Exception:
        pass


# Keeps a strong reference to pending auto-delete tasks so the event loop does
# not garbage-collect them before they fire.
_PENDING_DELETES = set()


def _schedule_delete(message, delay):
    """Delete `message` after `delay` seconds *without* blocking the caller."""
    async def _reap():
        try:
            await asyncio.sleep(delay)
            await message.delete()
        except Exception:
            pass
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return  # no loop (shutting down / sync context) - skip the cleanup
    task = loop.create_task(_reap())
    _PENDING_DELETES.add(task)
    task.add_done_callback(_PENDING_DELETES.discard)


async def safe_send(ctx, content=None, **kwargs):
    """Send a message, optionally scheduling its later deletion.

    The `delete_after` cleanup runs as a background task. It used to be awaited
    inline, which froze the calling command for the whole delay - `$ai` waited a
    full 60s before it even contacted the API, and its "thinking" placeholder was
    already gone by the time the answer arrived.
    """
    try:
        da = kwargs.pop("delete_after", None)
        m = await ctx.send(content, **kwargs)
        if da and m:
            _schedule_delete(m, da)
        return m
    except Exception:
        return None

async def get_user(ctx, text=None):
    """Resolve user from mention / ID / name. Works in guilds and DMs."""
    if ctx.message.mentions:
        return ctx.message.mentions[0]
    if not text:
        return ctx.author
    # Try ID
    m = re.match(r'<@!?(\d+)>', text)
    uid = None
    if m:
        uid = int(m.group(1))
    elif text.strip().isdigit():
        uid = int(text.strip())
    if uid:
        if ctx.guild:
            mem = ctx.guild.get_member(uid)
            if mem:
                return mem
            try:
                mem = await ctx.guild.fetch_member(uid)
                if mem:
                    return mem
            except Exception:
                pass
        try:
            return await ctx.bot.fetch_user(uid)
        except Exception:
            pass
    # Try name search in guild
    if ctx.guild:
        low = text.lower()
        for mem in ctx.guild.members:
            if low in mem.name.lower() or (mem.nick and low in mem.nick.lower()):
                return mem
    return None

# ============== TEXT TRANSFORM HELPERS ==============
def mock_text(t):
    return "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(t))

def leet(t):
    table = str.maketrans("aeiosbtlAEIOSBTL", "4310587143105871")
    return t.translate(table)

def vaporwave(t):
    out = ""
    for c in t:
        if c == " ":
            out += "  "
        elif 0x21 <= ord(c) <= 0x7E:
            out += chr(ord(c) + 0xFEE0)
        else:
            out += c
    return out

def zalgo(t, intensity=3):
    zalgo_up = list("\u0300\u0301\u0302\u0303\u0304\u0305\u0306\u0307\u0308\u0309\u030A\u030B\u030C\u030D\u030E\u030F\u0310\u0311\u0312\u0313\u0314\u0315\u0316\u0317\u0318\u0319\u031A\u031B\u031C\u031D\u031E\u031F\u0320\u0321\u0322\u0323\u0324\u0325\u0326\u0327\u0328\u0329\u032A\u032B\u032C\u032D\u032E\u032F\u0330\u0331\u0332\u0333\u0334\u0335\u0336\u0337\u0338\u0339\u033A\u033B\u033C\u033D\u033E\u033F\u0340\u0341\u0342\u0343\u0344\u0346\u0347\u0348\u0349\u034A\u034B\u034C\u034D\u034E\u034F")
    out = ""
    for c in t:
        out += c
        for _ in range(intensity):
            out += random.choice(zalgo_up)
    return out

def reverse_text(t):
    return t[::-1]

def expand_text(t):
    return " ".join(t)

def space_text(t, n=2):
    return (" " * n).join(t)

def to_binary(t):
    return " ".join(format(ord(c), "08b") for c in t)

def from_binary(t):
    try:
        return "".join(chr(int(b, 2)) for b in t.split())
    except Exception:
        return "Invalid binary"

def to_hex(t):
    return " ".join(format(ord(c), "02x") for c in t)

def from_hex(t):
    try:
        return "".join(chr(int(h, 16)) for h in t.split())
    except Exception:
        return "Invalid hex"

import base64
def b64_encode(t):
    return base64.b64encode(t.encode("utf-8")).decode()

def b64_decode(t):
    try:
        return base64.b64decode(t).decode("utf-8", errors="replace")
    except Exception:
        return "Invalid base64"

def scramble_word(w):
    if len(w) <= 3:
        return w
    mid = list(w[1:-1])
    random.shuffle(mid)
    return w[0] + "".join(mid) + w[-1]

def scramble_text(t):
    return " ".join(scramble_word(w) for w in t.split())

def to_cursive(t):
    """Script/italic-style unicode."""
    lo = "abcdefghijklmnopqrstuvwxyz"
    up = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lo2 = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    up2 = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
    out = ""
    for c in t:
        if c in lo:
            out += lo2[lo.index(c)]
        elif c in up:
            out += up2[up.index(c)]
        else:
            out += c
    return out

def to_bold(t):
    lo = "abcdefghijklmnopqrstuvwxyz"
    up = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dg = "0123456789"
    lo2 = "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    up2 = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
    dg2 = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    out = ""
    for c in t:
        if c in lo: out += lo2[lo.index(c)]
        elif c in up: out += up2[up.index(c)]
        elif c in dg: out += dg2[dg.index(c)]
        else: out += c
    return out

def to_smallcaps(t):
    lo = "abcdefghijklmnopqrstuvwxyz"
    up = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    out = ""
    for c in t.lower():
        if c in lo:
            out += up[lo.index(c)]
        else:
            out += c
    return out
