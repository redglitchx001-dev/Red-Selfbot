# -*- coding: utf-8 -*-
"""Text transform commands."""
from utils.common import *

def _get_text(ctx, text):
    """If text is empty but message is a reply, use replied-to message content."""
    if text:
        return text
    if ctx.message.reference and ctx.message.reference.resolved:
        ref = ctx.message.reference.resolved
        if hasattr(ref, "content"):
            return ref.content or ""
    return ""

def register(b, state):

    @b.command(name="mock")
    async def _mock(ctx, *, text: str = ""):
        track_cmd("mock")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply to a message.", delete_after=6)
        await safe_send(ctx, mock_text(t))

    @b.command(name="leet")
    async def _leet(ctx, *, text: str = ""):
        track_cmd("leet")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, leet(t))

    @b.command(name="vapor")
    async def _vapor(ctx, *, text: str = ""):
        track_cmd("vapor")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, vaporwave(t))

    @b.command(name="zalgo")
    async def _zalgo(ctx, intensity: int = 3, *, text: str = ""):
        track_cmd("zalgo")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Usage: $zalgo [intensity 1-10] [text]", delete_after=6)
        intensity = max(1, min(intensity, 10))
        await safe_send(ctx, zalgo(t, intensity))

    @b.command(name="reverse")
    async def _reverse(ctx, *, text: str = ""):
        track_cmd("reverse")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, reverse_text(t))

    @b.command(name="scramble")
    async def _scramble(ctx, *, text: str = ""):
        track_cmd("scramble")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, scramble_text(t))

    @b.command(name="expand")
    async def _expand(ctx, *, text: str = ""):
        track_cmd("expand")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, expand_text(t))

    @b.command(name="space")
    async def _space(ctx, n: int = 2, *, text: str = ""):
        track_cmd("space")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Usage: $space [n] [text]", delete_after=6)
        n = max(1, min(n, 10))
        await safe_send(ctx, space_text(t, n))

    @b.command(name="binary")
    async def _binary(ctx, *, text: str = ""):
        track_cmd("binary")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, to_binary(t)[:1990])

    @b.command(name="unbinary")
    async def _unbinary(ctx, *, text: str = ""):
        track_cmd("unbinary")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give binary string.", delete_after=6)
        await safe_send(ctx, from_binary(t))

    @b.command(name="hex")
    async def _hex(ctx, *, text: str = ""):
        track_cmd("hex")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, to_hex(t)[:1990])

    @b.command(name="unhex")
    async def _unhex(ctx, *, text: str = ""):
        track_cmd("unhex")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give hex string.", delete_after=6)
        await safe_send(ctx, from_hex(t))

    @b.command(name="b64e")
    async def _b64e(ctx, *, text: str = ""):
        track_cmd("b64e")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, b64_encode(t))

    @b.command(name="b64d")
    async def _b64d(ctx, *, text: str = ""):
        track_cmd("b64d")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give base64 string.", delete_after=6)
        await safe_send(ctx, b64_decode(t))

    @b.command(name="cursive")
    async def _cursive(ctx, *, text: str = ""):
        track_cmd("cursive")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, to_cursive(t))

    @b.command(name="bold")
    async def _bold(ctx, *, text: str = ""):
        track_cmd("bold")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, to_bold(t))

    @b.command(name="smallcaps")
    async def _smallcaps(ctx, *, text: str = ""):
        track_cmd("smallcaps")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, to_smallcaps(t))

    @b.command(name="upper")
    async def _upper(ctx, *, text: str = ""):
        track_cmd("upper")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, t.upper())

    @b.command(name="lower")
    async def _lower(ctx, *, text: str = ""):
        track_cmd("lower")
        await del_msg(ctx.message)
        t = _get_text(ctx, text)
        if not t: return await safe_send(ctx, "Give text or reply.", delete_after=6)
        await safe_send(ctx, t.lower())
