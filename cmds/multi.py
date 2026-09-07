# -*- coding: utf-8 -*-
"""Multi-account commands."""
from utils.common import *

def register(b, state, add_bot=None, remove_bot=None, get_selfbots=None):

    @b.command(name="selfbot")
    async def _sb(ctx, token: str = None, name: str = None):
        track_cmd("selfbot"); await del_msg(ctx.message)
        sbs = get_selfbots() if get_selfbots else {}
        if not token:
            lines = ["[main] (this account)"]
            for k, v in sbs.items():
                tag = v.user if v.user else "connecting"
                lines.append(f"[{k}] {tag}")
            await safe_send(ctx, code_block("Active accounts:\n" + "\n".join(lines)), delete_after=15)
            return
        name = name or f"bot{len(sbs)+1}"
        if name in sbs:
            return await safe_send(ctx, f"Name '{name}' taken.", delete_after=5)
        if add_bot:
            await add_bot(token, name)
            await safe_send(ctx, f"Added account '{name}'.", delete_after=10)

    @b.command(name="selfbotr")
    async def _sbr(ctx, name: str = None):
        track_cmd("selfbotr"); await del_msg(ctx.message)
        if not name: return await safe_send(ctx, "$selfbotr [name]", delete_after=5)
        if remove_bot:
            ok = await remove_bot(name)
            await safe_send(ctx, f"Removed '{name}'." if ok else f"'{name}' not found.", delete_after=5)

    @b.command(name="selfbots")
    async def _sbs(ctx):
        track_cmd("selfbots"); await del_msg(ctx.message)
        await safe_send(ctx, "Switching control between accounts is not supported at runtime; use $selfbotr then $selfbot to re-add.", delete_after=10)
