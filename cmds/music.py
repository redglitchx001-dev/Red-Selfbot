# -*- coding: utf-8 -*-
"""Music/voice commands."""
from utils.common import *
import shutil

def ffmpeg_ok():
    if shutil.which("ffmpeg"):
        return True
    for p in ["/usr/bin/ffmpeg", "/data/data/com.termux/files/usr/bin/ffmpeg"]:
        if os.path.exists(p): return True
    return False

def list_tracks():
    if not os.path.isdir("music"): return []
    return sorted(f for f in os.listdir("music") if f.lower().endswith((".mp3",".wav",".ogg",".m4a")))

def find_track(name):
    files = list_tracks()
    if not files: return None
    if name.isdigit():
        idx = int(name)-1
        if 0 <= idx < len(files): return f"music/{files[idx]}"
    low = name.lower()
    for f in files:
        if low in f.lower(): return f"music/{f}"
    return None

# Per-voice-client state
voice_state = {}

def get_vs(guild_id):
    if guild_id not in voice_state:
        voice_state[guild_id] = {"queue": [], "current": None, "volume": 0.5}
    return voice_state[guild_id]

def register(b, state):

    async def play_next(vc, vs, guild_id):
        if vs["queue"]:
            path = vs["queue"].pop(0)
            vs["current"] = path
            src = discord.FFmpegPCMAudio(path, options="-loglevel quiet")
            src = discord.PCMVolumeTransformer(src, volume=vs["volume"])
            vc.play(src, after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next(vc, vs, guild_id), b.loop
            ))
        else:
            vs["current"] = None

    @b.command(name="join")
    async def _join(ctx):
        track_cmd("join"); await del_msg(ctx.message)
        if not ctx.author.voice: return await safe_send(ctx, "Join a voice channel first.", delete_after=5)
        ch = ctx.author.voice.channel
        vc = ctx.voice_client
        if vc and vc.is_connected():
            if vc.channel != ch: await vc.move_to(ch)
        else:
            vc = await ch.connect()
        await safe_send(ctx, f"Joined {ch.name}.", delete_after=5)

    @b.command(name="leave", aliases=["stops"])
    async def _leave(ctx):
        track_cmd("leave"); await del_msg(ctx.message)
        vc = ctx.voice_client
        if vc:
            if vc.is_playing(): vc.stop()
            vs = get_vs(ctx.guild.id if ctx.guild else 0)
            vs["queue"].clear(); vs["current"] = None
            await vc.disconnect()
            await safe_send(ctx, "Left voice.", delete_after=5)
        else:
            await safe_send(ctx, "Not in voice.", delete_after=5)

    @b.command(name="plays")
    async def _play(ctx, *, name: str = None):
        track_cmd("plays"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        if not name: return await safe_send(ctx, "$plays [name/number]", delete_after=5)
        if not ctx.author.voice: return await safe_send(ctx, "Join voice first.", delete_after=5)
        if not ffmpeg_ok(): return await safe_send(ctx, "FFmpeg not found.", delete_after=8)
        path = find_track(name)
        if not path: return await safe_send(ctx, f"Track '{name}' not found.", delete_after=5)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            vc = await ctx.author.voice.channel.connect()
        elif vc.channel != ctx.author.voice.channel:
            await vc.move_to(ctx.author.voice.channel)
        vs = get_vs(ctx.guild.id)
        vs["queue"].append(path)
        if not vc.is_playing():
            await play_next(vc, vs, ctx.guild.id)
            await safe_send(ctx, f"Now playing: {os.path.basename(path)}", delete_after=10)
        else:
            await safe_send(ctx, f"Queued: {os.path.basename(path)} (position {len(vs['queue'])})", delete_after=10)

    @b.command(name="skip")
    async def _skip(ctx):
        track_cmd("skip"); await del_msg(ctx.message)
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await safe_send(ctx, "Skipped.", delete_after=5)
        else:
            await safe_send(ctx, "Nothing playing.", delete_after=5)

    @b.command(name="queue", aliases=["q"])
    async def _queue(ctx):
        track_cmd("queue"); await del_msg(ctx.message)
        if not ctx.guild: return
        vs = get_vs(ctx.guild.id)
        lines = []
        if vs["current"]:
            lines.append(f">>> Now: {os.path.basename(vs['current'])}")
        for i, p in enumerate(vs["queue"], 1):
            lines.append(f"{i}. {os.path.basename(p)}")
        if not lines: lines.append("Queue empty.")
        await safe_send(ctx, code_block("\n".join(lines[:25])), delete_after=20)

    @b.command(name="pause")
    async def _pause(ctx):
        track_cmd("pause"); await del_msg(ctx.message)
        vc = ctx.voice_client
        if vc and vc.is_playing() and not vc.is_paused():
            vc.pause()
            await safe_send(ctx, "Paused.", delete_after=5)
        else:
            await safe_send(ctx, "Nothing to pause.", delete_after=5)

    @b.command(name="resume")
    async def _resume(ctx):
        track_cmd("resume"); await del_msg(ctx.message)
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await safe_send(ctx, "Resumed.", delete_after=5)
        else:
            await safe_send(ctx, "Not paused.", delete_after=5)

    @b.command(name="volume", aliases=["vol"])
    async def _vol(ctx, v: int = None):
        track_cmd("volume"); await del_msg(ctx.message)
        if not ctx.guild: return
        vs = get_vs(ctx.guild.id)
        if v is None:
            return await safe_send(ctx, f"Volume: {int(vs['volume']*100)}%", delete_after=8)
        v = max(0, min(v, 200))
        vs["volume"] = v/100
        vc = ctx.voice_client
        if vc and vc.is_playing() and isinstance(vc.source, discord.PCMVolumeTransformer):
            vc.source.volume = vs["volume"]
        await safe_send(ctx, f"Volume set to {v}%.", delete_after=8)

    @b.command(name="np", aliases=["nowplaying"])
    async def _np(ctx):
        track_cmd("np"); await del_msg(ctx.message)
        if not ctx.guild: return
        vs = get_vs(ctx.guild.id)
        if vs["current"]:
            await safe_send(ctx, f"Now playing: {os.path.basename(vs['current'])}", delete_after=10)
        else:
            await safe_send(ctx, "Nothing playing.", delete_after=5)

    @b.command(name="downloadm")
    async def _dl(ctx, link: str = None):
        track_cmd("downloadm"); await del_msg(ctx.message)
        if not link: return await safe_send(ctx, "$downloadm [url]", delete_after=5)
        try:
            fn = f"music/dl_{int(time.time())}.mp3"
            r = requests.get(link, stream=True, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
            r.raise_for_status()
            sz = 0
            with open(fn, "wb") as f:
                for chunk in r.iter_content(4096):
                    f.write(chunk); sz += len(chunk)
            await safe_send(ctx, f"Downloaded: {os.path.basename(fn)} ({sz/1024/1024:.1f} MB)", delete_after=10)
        except Exception as e:
            await safe_send(ctx, f"Failed: {e}", delete_after=8)

    @b.command(name="adfiles")
    async def _ad(ctx):
        track_cmd("adfiles"); await del_msg(ctx.message)
        if not ctx.message.attachments: return await safe_send(ctx, "Attach audio files.", delete_after=5)
        saved = 0
        for a in ctx.message.attachments:
            if a.filename.lower().endswith((".mp3",".wav",".ogg",".m4a")):
                sp = f"music/{a.filename}"
                c = 1
                while os.path.exists(sp):
                    n, x = os.path.splitext(a.filename)
                    sp = f"music/{n}_{c}{x}"; c += 1
                await a.save(sp); saved += 1
        await safe_send(ctx, f"Saved {saved} file(s).", delete_after=8 if saved else 5)
        if not saved: await safe_send(ctx, "No supported audio files.", delete_after=5)

    @b.command(name="dwnlibs", aliases=["library", "libs"])
    async def _libs(ctx):
        track_cmd("dwnlibs"); await del_msg(ctx.message)
        files = list_tracks()
        if not files: return await safe_send(ctx, "Library empty.", delete_after=10)
        lines = []
        total = 0
        for i, f in enumerate(files, 1):
            sz = os.path.getsize(f"music/{f}")/1024/1024
            total += sz
            lines.append(f"{i:3d}. {f[:45]:<45} {sz:6.2f} MB")
        head = f"Library ({len(files)} tracks, {total:.1f} MB):\n"
        out = head + "\n".join(lines[:25])
        if len(files) > 25: out += f"\n... {len(files)-25} more"
        await safe_send(ctx, code_block(out), delete_after=30)
