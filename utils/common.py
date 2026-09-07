# -*- coding: utf-8 -*-
"""Shared utilities for Red Selfbot V1."""
import os, time, random, re, json, asyncio, datetime, platform, traceback
import requests
import discord

PREFIX = "$"
START_TIME = time.time()
COMMAND_USAGE = {}

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

async def safe_send(ctx, content=None, **kwargs):
    try:
        da = kwargs.pop("delete_after", None)
        m = await ctx.send(content, **kwargs)
        if da and m:
            try:
                await asyncio.sleep(da)
                await m.delete()
            except Exception:
                pass
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
