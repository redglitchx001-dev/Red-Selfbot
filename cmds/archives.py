# -*- coding: utf-8 -*-
"""Chat archive commands."""
from utils.common import *

def register(b, state):

    @b.command(name="clchat")
    async def _cc(ctx, amount: int = 100):
        track_cmd("clchat"); await del_msg(ctx.message)
        amount = max(1, min(amount, 1000))
        fn = f"archives/{ctx.channel.id}_{int(time.time())}.txt"
        n = 0
        with open(fn, "w", encoding="utf-8") as f:
            async for m in ctx.channel.history(limit=amount):
                ts = m.created_at.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{ts}] {m.author} ({m.author.id}): {m.content}\n")
                for a in m.attachments: f.write(f"    FILE: {a.url}\n")
                for em in m.embeds: f.write(f"    EMBED: {em.title or ''} | {em.description or ''}\n")
                n += 1
        sz = os.path.getsize(fn)/1024
        await safe_send(ctx, f"Saved {n} messages. {os.path.basename(fn)} ({sz:.1f} KB)", delete_after=15)

    @b.command(name="clist")
    async def _cl(ctx):
        track_cmd("clist"); await del_msg(ctx.message)
        files = sorted(f for f in os.listdir("archives") if f.endswith(".txt"))
        if not files: return await safe_send(ctx, "No archives.", delete_after=8)
        lines = []
        for i, fn in enumerate(files[-20:], 1):
            sz = os.path.getsize(f"archives/{fn}")/1024
            lines.append(f"{i:2d}. {fn}  {sz:.1f}KB")
        await safe_send(ctx, code_block("Archives (last 20):\n" + "\n".join(lines)), delete_after=30)

    @b.command(name="pstchat")
    async def _pc(ctx, target: str = None):
        track_cmd("pstchat"); await del_msg(ctx.message)
        if not target: return await safe_send(ctx, "$pstchat [channel_id/filename]", delete_after=5)
        files = [f for f in os.listdir("archives") if f.endswith(".txt")]
        path = None
        for fn in files:
            if target in fn or fn.startswith(f"{target}_"):
                path = f"archives/{fn}"; break
        if not path and os.path.exists(f"archives/{target}"):
            path = f"archives/{target}"
        if not path: return await safe_send(ctx, "Archive not found.", delete_after=5)
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]
        await safe_send(ctx, f"Pasting ({os.path.basename(path)}):", delete_after=5)
        for line in lines[-15:]:
            if len(line) > 1900: line = line[:1900] + "..."
            await ctx.send(line)
            await asyncio.sleep(0.5)

    @b.command(name="cldel")
    async def _cdel(ctx, nr: int = None):
        track_cmd("cldel"); await del_msg(ctx.message)
        files = sorted(f for f in os.listdir("archives") if f.endswith(".txt"))
        if nr is None: return await safe_send(ctx, "$cldel [number]", delete_after=5)
        if not 1 <= nr <= len(files): return await safe_send(ctx, "Invalid number.", delete_after=5)
        # nr is in display order (last 20) but we need to delete from full list by idx
        os.remove(f"archives/{files[nr-1]}")
        await safe_send(ctx, f"Deleted archive #{nr}.", delete_after=5)
