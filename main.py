# -*- coding: utf-8 -*-
"""
RED SELFBOT V1 - Main entry point.
Premium modular build - 2026 fancy edition.
Panel: 0.0.0.0:3000 (default) - no localhost hardcode, works with preview.
Admin panel (panel.py + panel.html): login nume+token, admin key, users,
tokenuri expirate, suspend/ban, blacklist commands.
"""
import sys, types, os, asyncio, json, threading, time, platform, traceback

# Compatibility patches
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
                for f in ["mul","add","bias","lin2lin","adpcm2lin","lin2adpcm","max","minmax","avg","rms"]:
                    setattr(m, f, lambda *a, **k: 0 if "lin" not in a else b'')
            sys.modules[mod_name] = m
    try:
        import discord.settings
        _o = discord.settings.Settings.__init__
        def _p(self, *, data, state):
            if data and data.get("friend_source_flags") is None:
                data["friend_source_flags"] = {}
            return _o(self, data=data, state=state)
        discord.settings.Settings.__init__ = _p
    except Exception:
        pass

apply_patches()
os.environ["no_proxy"] = "*"

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("Install: pip install discord.py-self requests PyNaCl"); sys.exit(1)

from utils.common import *
import cmds.help, cmds.text, cmds.fun, cmds.util, cmds.info, cmds.spam, cmds.music
import cmds.profiles, cmds.cloner, cmds.archives, cmds.protect, cmds.logger, cmds.status, cmds.multi
import cmds.ai
import panel as admin_panel

PREFIX = "$"
START_TIME = time.time()

# Global state
selfbots = {}
bot_meta = {}

# ============================================================
# ADMIN PANEL - panel.py serves panel.html on 0.0.0.0:3000
# ============================================================
def panel_meta():
    md = bot_meta.get("main", {})
    return {
        "prefix": PREFIX,
        "bot": {
            "online": bool(md.get("online")),
            "name": md.get("name", ""),
            "guilds": md.get("guilds", 0),
            "users": md.get("users", 0),
            "ping": md.get("ping", 0),
        },
    }

def run_server():
    admin_panel.run_server(meta_provider=panel_meta)

# ============================================================
# SETUP
# ============================================================
def setup_bot(b, label="main"):
    state = {
        "spamming": False, "spam_channels": set(), "spam_scope": None,
        "autoreact": False, "autoreact_emoji": None,
        "anti_kick": False, "anti_ban": False,
        "logchat_chans": set(), "logdm": False,
        "tracked": set(),
        "snipe": {}, "editsnipe": {},
        "start_lang": "default",
    }

    @b.event
    async def on_ready():
        print(f"\n[+] Logged in as {b.user} | Servers: {len(b.guilds)} | Prefix: {PREFIX} | Panel 0.0.0.0:{os.environ.get('PORT','3000')}")
        if label == "main":
            users = sum(g.member_count or 0 for g in b.guilds)
            bot_meta["main"] = {
                "start": START_TIME, "name": str(b.user.name),
                "guilds": len(b.guilds), "users": users,
                "cmds": 0, "ping": round(b.latency*1000), "feats": state,
                "online": True,
            }

    @b.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound): return
        if isinstance(error, commands.MissingRequiredArgument):
            return await safe_send(ctx, f"Missing argument. See $help.", delete_after=6)
        if isinstance(error, commands.BadArgument):
            return await safe_send(ctx, f"Bad argument.", delete_after=6)
        if isinstance(error, commands.CommandInvokeError):
            o = error.original
            if isinstance(o, discord.Forbidden): return await safe_send(ctx, "No permission.", delete_after=5)
            if isinstance(o, discord.HTTPException) and getattr(o,"code",None)==429: return
        try: traceback.print_exception(type(error), error, error.__traceback__)
        except: pass

    # Register all module commands
    cmds.help.register(b, state)
    cmds.text.register(b, state)
    cmds.fun.register(b, state)
    cmds.util.register(b, state)
    cmds.info.register(b, state)
    cmds.music.register(b, state)
    cmds.spam.register(b, state)
    cmds.profiles.register(b, state)
    cmds.cloner.register(b, state)
    cmds.archives.register(b, state)
    cmds.protect.register(b, state)
    cmds.logger.register(b, state)
    cmds.status.register(b, state)
    cmds.ai.register(b, state)

    # Blacklist commands (managed din admin panel -> data/blacklist.json)
    async def _pre_cmd(ctx):
        try:
            if not getattr(ctx, "valid", True):
                return
            bl = admin_panel.load_blacklist()
            name = (getattr(ctx.command, "name", "") or "").lower()
            if name and name in bl:
                await safe_send(ctx, f"\u26d4 `{PREFIX}{name}` is blacklisted.", delete_after=6)
                return True  # truthy return = command is NOT invoked (discord.py before_invoke)
        except Exception:
            pass
    try:
        b.before_invoke(_pre_cmd)
    except Exception:
        pass

    # Multi-account callbacks
    async def add_bot(token, name):
        # handle intents missing in newer discord.py-self
        try:
            _int = discord.Intents.all()
        except Exception:
            _int = None
        kwargs = dict(command_prefix=PREFIX, self_bot=True)
        if _int is not None:
            kwargs["intents"] = _int
        nb = commands.Bot(**kwargs)
        setup_bot(nb, label=name)
        selfbots[name] = nb
        def run_it():
            loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
            try: loop.run_until_complete(nb.start(token))
            except Exception as e: print(f"[!] {name}: {e}")
        threading.Thread(target=run_it, daemon=True).start()

    async def remove_bot(name):
        if name in selfbots:
            try: await selfbots[name].close()
            except: pass
            del selfbots[name]; return True
        return False

    cmds.multi.register(b, state, add_bot=add_bot, remove_bot=remove_bot, get_selfbots=lambda: selfbots)

    return state

async def meta_updater(b):
    await b.wait_until_ready()
    while not b.is_closed():
        try:
            md = bot_meta.get("main", {})
            md["guilds"] = len(b.guilds)
            md["users"] = sum(g.member_count or 0 for g in b.guilds)
            md["ping"] = round(b.latency*1000)
            md["cmds"] = sum(COMMAND_USAGE.values())
            bot_meta["main"] = md
        except: pass
        await asyncio.sleep(10)

try:
    intents = discord.Intents.all()
    intents.typing = False
except Exception:
    # discord.py-self 2.1.0 may not have Intents
    intents = None

async def main():
    threading.Thread(target=run_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if not token and os.path.exists("token.txt"):
        with open("token.txt") as f: token = f.read().strip()
    if not token:
        print("[!] DISCORD_TOKEN not set. Set env or create token.txt.")
        print(f"[i] Admin panel still on 0.0.0.0:{os.environ.get('PORT','3000')} (localhost:{os.environ.get('PORT','3000')})")
        while True: await asyncio.sleep(3600)
    token = token.strip().strip('"').strip("'")
    bot_kwargs = dict(command_prefix=PREFIX, self_bot=True)
    if intents is not None:
        bot_kwargs["intents"] = intents
        bot_kwargs["guild_subscriptions"] = True
    bot = commands.Bot(**bot_kwargs)
    setup_bot(bot)
    async with bot:
        try:
            bot.loop.create_task(meta_updater(bot))
        except AttributeError:
            asyncio.create_task(meta_updater(bot))
        await bot.start(token)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("𝓡𝓔𝓓 𝓢𝓔𝓛𝓕𝓑𝓞𝓣 𝓥1 - 2026 Fancy Gradient Edition")
    print(f"Panel: 0.0.0.0:{os.environ.get('PORT','3000')} -> localhost:{os.environ.get('PORT','3000')}")
    print("Admin key: from env ADMIN_KEY (has a built-in default)")
    print("="*50)
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n[-] Shutting down.")
