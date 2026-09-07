# -*- coding: utf-8 -*-
"""Server cloner / backup commands."""
from utils.common import *

def get_overwrites(ch):
    ows = []
    for target, ow in ch.overwrites.items():
        a, d = ow.pair()
        ows.append({"id": target.id,
                    "type": "role" if isinstance(target, discord.Role) else "member",
                    "allow": a.value, "deny": d.value})
    return ows

def register(b, state):

    @b.command(name="dsrv")
    async def _dsrv(ctx):
        track_cmd("dsrv"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        data = {"name": ctx.guild.name, "roles": [], "categories": [], "orphans": [], "emojis": []}
        for role in reversed(ctx.guild.roles):
            if role.managed and not role.is_default(): continue
            data["roles"].append({
                "id": role.id, "n": role.name, "c": role.color.value, "p": role.permissions.value,
                "h": role.hoist, "m": role.mentionable, "everyone": role.is_default(),
            })
        for cat in ctx.guild.categories:
            chans = []
            for ch in cat.channels:
                cd = {"n": ch.name, "t": str(ch.type), "ow": get_overwrites(ch)}
                if isinstance(ch, discord.TextChannel):
                    cd.update({"topic": ch.topic, "nsfw": ch.nsfw, "slow": ch.slowmode_delay})
                elif isinstance(ch, discord.VoiceChannel):
                    cd.update({"bitrate": ch.bitrate, "limit": ch.user_limit})
                chans.append(cd)
            data["categories"].append({"n": cat.name, "ow": get_overwrites(cat), "ch": chans})
        for ch in ctx.guild.channels:
            if ch.category is None:
                cd = {"n": ch.name, "t": str(ch.type), "ow": get_overwrites(ch)}
                if isinstance(ch, discord.TextChannel):
                    cd.update({"topic": ch.topic, "nsfw": ch.nsfw, "slow": ch.slowmode_delay})
                elif isinstance(ch, discord.VoiceChannel):
                    cd.update({"bitrate": ch.bitrate, "limit": ch.user_limit})
                data["orphans"].append(cd)
        for e in ctx.guild.emojis:
            data["emojis"].append({"n": e.name, "animated": e.animated, "url": str(e.url)})
        fn = f"clones/{ctx.guild.id}_{int(time.time())}.json"
        save_json(fn, data)
        sz = os.path.getsize(fn)/1024
        await safe_send(ctx, f"Backed up {ctx.guild.name}.\nRoles: {len(data['roles'])}  Cats: {len(data['categories'])}  Channels: {len(data['orphans'])+sum(len(c['ch']) for c in data['categories'])}  Emojis: {len(data['emojis'])}\nSize: {sz:.1f} KB", delete_after=15)

    @b.command(name="lsrv")
    async def _ls(ctx):
        track_cmd("lsrv"); await del_msg(ctx.message)
        files = sorted(f for f in os.listdir("clones") if f.endswith(".json"))
        if not files: return await safe_send(ctx, "No backups.", delete_after=8)
        lines = []
        for i, fn in enumerate(files, 1):
            d = load_json(f"clones/{fn}")
            sz = os.path.getsize(f"clones/{fn}")/1024
            roles = len(d.get("roles",[])); cats = len(d.get("categories",[]))
            lines.append(f"{i:2d}. {d.get('name','?')[:25]:<25} {roles}r {cats}c {sz:.1f}KB")
        await safe_send(ctx, code_block("Backups:\n" + "\n".join(lines)), delete_after=30)

    @b.command(name="psrv")
    async def _ps(ctx, nr: int = None):
        track_cmd("psrv"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Run in target server.", delete_after=5)
        if nr is None: return await safe_send(ctx, "$psrv [number]", delete_after=5)
        files = sorted(f for f in os.listdir("clones") if f.endswith(".json"))
        if not 1 <= nr <= len(files): return await safe_send(ctx, f"Choose 1-{len(files)}.", delete_after=5)
        d = load_json(f"clones/{files[nr-1]}")
        status = await safe_send(ctx, f"Applying backup: {d.get('name','?')}...")
        res = {"roles":0,"cats":0,"chs":0,"err":0}
        try:
            rm = {}
            for r in d.get("roles",[]):
                try:
                    if r.get("everyone"):
                        rm[r["id"]] = ctx.guild.default_role
                        try: await ctx.guild.default_role.edit(permissions=discord.Permissions(r["p"]))
                        except: pass
                        continue
                    nr2 = await ctx.guild.create_role(name=r["n"], color=discord.Color(r["c"]),
                        permissions=discord.Permissions(r["p"]), hoist=r["h"], mentionable=r["m"])
                    rm[r["id"]] = nr2; res["roles"] += 1; await asyncio.sleep(0.35)
                except: res["err"] += 1
            def sync(ow):
                out = {}
                for o in ow:
                    t = rm.get(o["id"])
                    if t: out[t] = discord.PermissionOverwrite.from_pair(
                        discord.Permissions(o["allow"]), discord.Permissions(o["deny"]))
                return out
            for cd in d.get("categories",[]):
                try:
                    ow = sync(cd.get("ow",[]))
                    cat = await ctx.guild.create_category(cd["n"], overwrites=ow)
                    res["cats"] += 1; await asyncio.sleep(0.4)
                    for ch in cd.get("ch",[]):
                        try:
                            co = sync(ch.get("ow",[]))
                            if ch["t"]=="text":
                                await cat.create_text_channel(ch["n"], topic=ch.get("topic"),
                                    nsfw=ch.get("nsfw",False), slowmode_delay=ch.get("slow",0), overwrites=co)
                            elif ch["t"]=="voice":
                                await cat.create_voice_channel(ch["n"], bitrate=min(ch.get("bitrate",64000),96000),
                                    user_limit=ch.get("limit",0), overwrites=co)
                            else:
                                await cat.create_text_channel(ch["n"], overwrites=co)
                            res["chs"] += 1; await asyncio.sleep(0.35)
                        except: res["err"] += 1
                except: res["err"] += 1
            for ch in d.get("orphans",[]):
                try:
                    co = sync(ch.get("ow",[]))
                    if ch["t"]=="text":
                        await ctx.guild.create_text_channel(ch["n"], topic=ch.get("topic"),
                            nsfw=ch.get("nsfw",False), slowmode_delay=ch.get("slow",0), overwrites=co)
                    elif ch["t"]=="voice":
                        await ctx.guild.create_voice_channel(ch["n"], bitrate=min(ch.get("bitrate",64000),96000),
                            user_limit=ch.get("limit",0), overwrites=co)
                    else:
                        await ctx.guild.create_text_channel(ch["n"], overwrites=co)
                    res["chs"] += 1; await asyncio.sleep(0.35)
                except: res["err"] += 1
        except Exception as e:
            if status:
                try: await status.edit(content=f"Error: {e}")
                except: pass
            return
        summ = f"Done. Roles: {res['roles']}  Categories: {res['cats']}  Channels: {res['chs']}  Errors: {res['err']}"
        if status:
            try: await status.edit(content=summ)
            except: await safe_send(ctx, summ, delete_after=15)
        else:
            await safe_send(ctx, summ, delete_after=15)

    @b.command(name="dsrvdel")
    async def _ddel(ctx, nr: int = None):
        track_cmd("dsrvdel"); await del_msg(ctx.message)
        if nr is None: return await safe_send(ctx, "$dsrvdel [number]", delete_after=5)
        files = sorted(f for f in os.listdir("clones") if f.endswith(".json"))
        if not 1 <= nr <= len(files): return await safe_send(ctx, "Invalid number.", delete_after=5)
        os.remove(f"clones/{files[nr-1]}")
        await safe_send(ctx, f"Deleted backup #{nr}.", delete_after=5)
