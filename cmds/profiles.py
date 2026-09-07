# -*- coding: utf-8 -*-
"""Profile archiver commands."""
from utils.common import *

def register(b, state):

    @b.command(name="prfdwn")
    async def _pd(ctx, *, user: str = None):
        track_cmd("prfdwn"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention or give user ID.", delete_after=5)
        avatar = t.avatar.url if t.avatar else (t.default_avatar.url if hasattr(t,"default_avatar") else "")
        banner = ""
        try:
            fetched = await b.fetch_user(t.id)
            if fetched.banner: banner = fetched.banner.url
        except: pass
        # A single unexpected attribute shape used to abort the whole command
        # (e.g. TypeError formatting a colour), so the colour is read defensively.
        try:
            colour_val = t.color.value if getattr(t, "color", None) else 0
        except Exception:
            colour_val = 0
        data = {
            "name": t.name, "display": getattr(t,"display_name",t.name),
            "nick": getattr(t,"nick",None), "id": t.id,
            "bot": getattr(t,"bot",False), "avatar": avatar, "banner": banner,
            "created": t.created_at.strftime("%Y-%m-%d %H:%M"),
            "joined": t.joined_at.strftime("%Y-%m-%d %H:%M") if hasattr(t,"joined_at") and t.joined_at else None,
            "roles": [r.name for r in getattr(t,"roles",[]) if not r.is_default()] if hasattr(t,"roles") else [],
            "color": f"#{colour_val:06x}",
        }
        save_json(f"profiles/{t.id}.json", data)
        await safe_send(ctx, f"Saved profile: {t.name}", delete_after=8)

    @b.command(name="prflist")
    async def _pl(ctx):
        track_cmd("prflist"); await del_msg(ctx.message)
        files = sorted(f for f in os.listdir("profiles") if f.endswith(".json"))
        if not files: return await safe_send(ctx, "No profiles saved.", delete_after=8)
        lines = []
        for i, fn in enumerate(files, 1):
            d = load_json(f"profiles/{fn}")
            lines.append(f"{i:2d}. {d.get('name','?'):<25} ({d.get('id','?')})")
        out = "Saved profiles:\n" + "\n".join(lines)
        await safe_send(ctx, code_block(out), delete_after=30)

    @b.command(name="prfup")
    async def _pu(ctx, nr: int = None):
        track_cmd("prfup"); await del_msg(ctx.message)
        if nr is None: return await safe_send(ctx, "$prfup [number]", delete_after=5)
        files = sorted(f for f in os.listdir("profiles") if f.endswith(".json"))
        if not 1 <= nr <= len(files): return await safe_send(ctx, f"Choose 1-{len(files)}.", delete_after=5)
        d = load_json(f"profiles/{files[nr-1]}")
        lines = [
            f"#{nr}",
            f"Name: {d.get('name')}",
            f"Display: {d.get('display')}",
            f"Nick: {d.get('nick') or '-'}",
            f"ID: {d.get('id')}",
            f"Bot: {d.get('bot')}",
            f"Created: {d.get('created')}",
            f"Joined: {d.get('joined') or '-'}",
            f"Color: {d.get('color')}",
            f"Roles ({len(d.get('roles',[]))}): {', '.join(d.get('roles',[])) or '-'}",
            f"Avatar: {d.get('avatar','-')}",
        ]
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=30)

    @b.command(name="prfdel")
    async def _pdel(ctx, nr: int = None):
        track_cmd("prfdel"); await del_msg(ctx.message)
        if nr is None: return await safe_send(ctx, "$prfdel [number]", delete_after=5)
        files = sorted(f for f in os.listdir("profiles") if f.endswith(".json"))
        if not 1 <= nr <= len(files): return await safe_send(ctx, "Invalid number.", delete_after=5)
        os.remove(f"profiles/{files[nr-1]}")
        await safe_send(ctx, f"Deleted profile #{nr}.", delete_after=5)

    @b.command(name="mphelp")
    async def _mph(ctx):
        track_cmd("mphelp"); await del_msg(ctx.message)
        await safe_send(ctx, code_block("$prfdwn @user - Save\n$prflist - List\n$prfup [n] - View\n$prfdel [n] - Delete"), delete_after=20)
