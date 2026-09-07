# -*- coding: utf-8 -*-
"""Logger / snipe / tracking commands."""
from utils.common import *

def register(b, state):

    @b.command(name="logchat")
    async def _lc(ctx):
        track_cmd("logchat"); await del_msg(ctx.message)
        cid = ctx.channel.id
        if cid in state.get("logchat_chans", set()):
            state["logchat_chans"].discard(cid); s = "OFF"
        else:
            state.setdefault("logchat_chans", set()).add(cid); s = "ON"
        await safe_send(ctx, f"Chat logger: {s} for this channel.", delete_after=8)

    @b.command(name="logdm")
    async def _ld(ctx):
        track_cmd("logdm"); await del_msg(ctx.message)
        state["logdm"] = not state.get("logdm", False)
        s = "ON" if state["logdm"] else "OFF"
        await safe_send(ctx, f"DM logger: {s}.", delete_after=8)

    @b.command(name="sniped", aliases=["snipe"])
    async def _sn(ctx):
        track_cmd("sniped"); await del_msg(ctx.message)
        d = state.get("snipe", {}).get(ctx.channel.id)
        if not d: return await safe_send(ctx, "Nothing snipped.", delete_after=5)
        att = "\nAttachments: " + ", ".join(d["att"]) if d["att"] else ""
        await safe_send(ctx, code_block(
            f"Last deleted message:\nAuthor: {d['author']} ({d['aid']})\nTime: {d['ts']}\n"
            f"Content:\n{d['content'][:1500]}{att}"
        ), delete_after=20)

    @b.command(name="esniped", aliases=["editsnipe"])
    async def _es(ctx):
        track_cmd("esniped"); await del_msg(ctx.message)
        d = state.get("editsnipe", {}).get(ctx.channel.id)
        if not d: return await safe_send(ctx, "No edited messages cached.", delete_after=5)
        await safe_send(ctx, code_block(
            f"Last edited message:\nAuthor: {d['author']}\nBefore:\n{d['before'][:900]}\n"
            f"After:\n{d['after'][:900]}"
        ), delete_after=20)

    @b.command(name="track")
    async def _tr(ctx, *, user: str = None):
        track_cmd("track"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention or ID a user.", delete_after=5)
        tracked = state.setdefault("tracked", set())
        if t.id in tracked:
            tracked.discard(t.id)
            await safe_send(ctx, f"Stopped tracking {t.name}.", delete_after=5)
        else:
            tracked.add(t.id)
            await safe_send(ctx, f"Now tracking {t.name}. DMs on changes.", delete_after=10)

    @b.command(name="trackstop")
    async def _ts(ctx):
        track_cmd("trackstop"); await del_msg(ctx.message)
        state["tracked"] = set()
        await safe_send(ctx, "All tracking stopped.", delete_after=5)

    @b.command(name="logs")
    async def _lo(ctx):
        track_cmd("logs"); await del_msg(ctx.message)
        lc = len(state.get("logchat_chans", set()))
        ld = "ON" if state.get("logdm") else "OFF"
        tr = len(state.get("tracked", set()))
        await safe_send(ctx, code_block(f"Chat logs active: {lc} channels\nDM log: {ld}\nTracking: {tr} users"), delete_after=15)

    # ---------- Listeners ----------
    @b.listen("on_message_delete")
    async def _snipe_listen(message):
        if message.author == b.user: return
        state.setdefault("snipe", {})[message.channel.id] = {
            "author": str(message.author), "aid": message.author.id,
            "content": message.content or "[no text]",
            "ts": message.created_at.strftime("%Y-%m-%d %H:%M"),
            "att": [a.url for a in message.attachments],
        }

    @b.listen("on_message_edit")
    async def _edit_listen(before, after):
        if before.author == b.user: return
        if before.content != after.content:
            state.setdefault("editsnipe", {})[before.channel.id] = {
                "author": str(before.author),
                "before": before.content or "",
                "after": after.content or "",
            }

    @b.listen("on_message")
    async def _log_listen(message):
        if message.author == b.user: return
        # Chat log per-channel
        if message.channel.id in state.get("logchat_chans", set()):
            try:
                with open(f"logs/chat_{message.channel.id}.txt", "a", encoding="utf-8") as f:
                    ts = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{ts}] {message.author}: {message.content}\n")
                    for a in message.attachments: f.write(f"    FILE: {a.url}\n")
            except: pass
        # DM log
        if state.get("logdm") and not message.guild:
            try:
                with open(f"logs/dm_{message.author.id}.txt", "a", encoding="utf-8") as f:
                    ts = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{ts}] {message.author}: {message.content}\n")
            except: pass

    @b.listen("on_member_update")
    async def _track_listen(before, after):
        tracked = state.get("tracked", set())
        if after.id not in tracked: return
        try:
            if before.status != after.status:
                await b.user.send(f"[track] {after}: {before.status} -> {after.status}")
            if before.activities != after.activities:
                old = [a.name for a in before.activities if getattr(a, "name", None)]
                new = [a.name for a in after.activities if getattr(a, "name", None)]
                if old != new:
                    await b.user.send(f"[track] {after} activity:\nBefore: {', '.join(old) or 'none'}\nNow: {', '.join(new) or 'none'}")
        except: pass
