# -*- coding: utf-8 -*-
"""Protection / utility commands."""
from utils.common import *

def register(b, state):

    @b.command(name="anti-kick")
    async def _ak(ctx):
        track_cmd("anti-kick"); await del_msg(ctx.message)
        state["anti_kick"] = not state["anti_kick"]
        s = "ON" if state["anti_kick"] else "OFF"
        await safe_send(ctx, f"Anti-kick: {s} (client-side alert only).", delete_after=8)

    @b.command(name="anti-ban")
    async def _ab(ctx):
        track_cmd("anti-ban"); await del_msg(ctx.message)
        state["anti_ban"] = not state["anti_ban"]
        s = "ON" if state["anti_ban"] else "OFF"
        await safe_send(ctx, f"Anti-ban: {s} (client-side alert only).", delete_after=8)

    @b.command(name="ghostping")
    async def _gp(ctx, *, user: str = None):
        track_cmd("ghostping"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention someone.", delete_after=5)
        try:
            m = await ctx.send(t.mention)
            await m.delete()
        except Exception as e:
            await safe_send(ctx, f"Failed: {e}", delete_after=5)

    @b.command(name="tokencheck")
    async def _tc(ctx, token: str = None):
        track_cmd("tokencheck"); await del_msg(ctx.message)
        if not token: return await safe_send(ctx, "$tokencheck [token]", delete_after=5)
        try:
            r = requests.get("https://discord.com/api/v9/users/@me",
                headers={"Authorization": token}, timeout=10)
            if r.status_code == 200:
                d = r.json()
                await safe_send(ctx, code_block(
                    f"Token valid.\nUser: {d.get('username')}\nID: {d.get('id')}\n"
                    f"Verified: {d.get('verified')}\nNitro: {bool(d.get('premium_type'))}"
                ), delete_after=20)
            else:
                await safe_send(ctx, f"Invalid token (HTTP {r.status_code}).", delete_after=8)
        except Exception as e:
            await safe_send(ctx, f"Error: {e}", delete_after=8)

    @b.command(name="purge")
    async def _purge(ctx, amount: int = 10):
        track_cmd("purge"); await del_msg(ctx.message)
        amount = max(1, min(amount, 100))
        deleted = 0
        async for m in ctx.channel.history(limit=200):
            if deleted >= amount: break
            if m.author == b.user:
                try: await m.delete(); deleted += 1; await asyncio.sleep(0.35)
                except: pass
        await safe_send(ctx, f"Deleted {deleted} of your messages.", delete_after=6)

    @b.command(name="nuke")
    async def _nuke(ctx, amount: int = 50):
        track_cmd("nuke"); await del_msg(ctx.message)
        amount = max(1, min(amount, 100))
        deleted = 0
        async for m in ctx.channel.history(limit=200):
            if deleted >= amount: break
            if m.author == b.user:
                try: await m.delete(); deleted += 1; await asyncio.sleep(0.2)
                except: pass
        await safe_send(ctx, f"Nuked {deleted} messages.", delete_after=6)

    @b.command(name="cleardms")
    async def _cdms(ctx):
        track_cmd("cleardms"); await del_msg(ctx.message)
        count = 0
        for ch in b.private_channels:
            try:
                async for m in ch.history(limit=25):
                    if m.author == b.user:
                        try: await m.delete(); count += 1; await asyncio.sleep(0.3)
                        except: pass
            except: pass
        await safe_send(ctx, f"Cleared {count} of your recent DM messages.", delete_after=10)
