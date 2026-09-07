# -*- coding: utf-8 -*-
"""Presence / status commands."""
from utils.common import *

def register(b, state):

    @b.command(name="stats", aliases=["playing"])
    async def _stats(ctx, *, text: str = None):
        track_cmd("stats"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "$stats [text]", delete_after=5)
        await b.change_presence(activity=discord.Game(name=text), status=discord.Status.online)
        await safe_send(ctx, f"Status set: {text}", delete_after=5)

    @b.command(name="live", aliases=["streaming"])
    async def _live(ctx, *, text: str = None):
        track_cmd("live"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "$live [text]", delete_after=5)
        await b.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/x"), status=discord.Status.online)
        await safe_send(ctx, f"Streaming: {text}", delete_after=5)

    @b.command(name="listen")
    async def _listen(ctx, *, text: str = None):
        track_cmd("listen"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "$listen [text]", delete_after=5)
        await b.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text), status=discord.Status.online)
        await safe_send(ctx, f"Listening to: {text}", delete_after=5)

    @b.command(name="watch")
    async def _watch(ctx, *, text: str = None):
        track_cmd("watch"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "$watch [text]", delete_after=5)
        await b.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text), status=discord.Status.online)
        await safe_send(ctx, f"Watching: {text}", delete_after=5)

    @b.command(name="comp", aliases=["competing"])
    async def _comp(ctx, *, text: str = None):
        track_cmd("comp"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "$comp [text]", delete_after=5)
        await b.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=text), status=discord.Status.online)
        await safe_send(ctx, f"Competing in: {text}", delete_after=5)

    @b.command(name="remstats", aliases=["clearstatus"])
    async def _rs(ctx):
        track_cmd("remstats"); await del_msg(ctx.message)
        await b.change_presence(activity=None, status=discord.Status.online)
        await safe_send(ctx, "Status cleared.", delete_after=5)

    @b.command(name="statusdnd", aliases=["dnd"])
    async def _dnd(ctx):
        track_cmd("statusdnd"); await del_msg(ctx.message)
        await b.change_presence(status=discord.Status.dnd)
        await safe_send(ctx, "Status: DND.", delete_after=5)

    @b.command(name="statusidle", aliases=["idle"])
    async def _idle(ctx):
        track_cmd("statusidle"); await del_msg(ctx.message)
        await b.change_presence(status=discord.Status.idle)
        await safe_send(ctx, "Status: idle.", delete_after=5)

    @b.command(name="statusonline", aliases=["online"])
    async def _on(ctx):
        track_cmd("statusonline"); await del_msg(ctx.message)
        await b.change_presence(status=discord.Status.online)
        await safe_send(ctx, "Status: online.", delete_after=5)

    @b.command(name="statusinv", aliases=["invisible", "invis"])
    async def _inv(ctx):
        track_cmd("statusinv"); await del_msg(ctx.message)
        await b.change_presence(status=discord.Status.invisible)
        await safe_send(ctx, "Status: invisible.", delete_after=5)
