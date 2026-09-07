# -*- coding: utf-8 -*-
"""Utility commands."""
from utils.common import *
import ast, operator, base64 as _b64, urllib.parse

def register(b, state):

    @b.command(name="ping")
    async def _ping(ctx):
        track_cmd("ping"); await del_msg(ctx.message)
        await safe_send(ctx, f"Pong. {round(b.latency*1000)}ms", delete_after=8)

    @b.command(name="uptime")
    async def _uptime(ctx):
        track_cmd("uptime"); await del_msg(ctx.message)
        await safe_send(ctx, f"Uptime: {fmt_time(time.time()-START_TIME)}", delete_after=10)

    @b.command(name="avatar")
    async def _avatar(ctx, *, user: str = None):
        track_cmd("avatar"); await del_msg(ctx.message)
        t = await get_user(ctx, user) or ctx.author
        av = t.avatar.url.replace(".webp", ".png") + "?size=4096" if t.avatar else \
             (t.default_avatar.url if hasattr(t, "default_avatar") else None)
        if not av: return await safe_send(ctx, "No avatar.", delete_after=5)
        e = discord.Embed(color=discord.Color.red())
        e.set_image(url=av)
        await ctx.send(embed=e)

    @b.command(name="banner")
    async def _banner(ctx, *, user: str = None):
        track_cmd("banner"); await del_msg(ctx.message)
        t = await get_user(ctx, user) or ctx.author
        try:
            t = await b.fetch_user(t.id)
            if t.banner:
                url = t.banner.url + "?size=4096"
                e = discord.Embed(color=discord.Color.red())
                e.set_image(url=url)
                await ctx.send(embed=e)
            else:
                await safe_send(ctx, "No banner.", delete_after=5)
        except Exception:
            await safe_send(ctx, "Could not fetch banner.", delete_after=5)

    @b.command(name="servericon")
    async def _srvicon(ctx):
        track_cmd("servericon"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        if not ctx.guild.icon: return await safe_send(ctx, "No icon.", delete_after=5)
        e = discord.Embed(color=discord.Color.red())
        e.set_image(url=ctx.guild.icon.url+"?size=4096")
        await ctx.send(embed=e)

    @b.command(name="nick")
    async def _nick(ctx, *, name: str = None):
        track_cmd("nick"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        if not name: return await safe_send(ctx, "Give a nickname.", delete_after=5)
        try:
            await ctx.author.edit(nick=name)
            await safe_send(ctx, f"Nick set to {name}.", delete_after=8)
        except Exception as e:
            await safe_send(ctx, f"Failed: {e}", delete_after=8)

    @b.command(name="calc")
    async def _calc(ctx, *, expr: str = None):
        track_cmd("calc"); await del_msg(ctx.message)
        if not expr: return await safe_send(ctx, "e.g. $calc 2+2*3", delete_after=5)
        allowed = {
            ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
            ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
            ast.USub: operator.neg, ast.UAdd: operator.pos, ast.FloorDiv: operator.floordiv,
        }
        def ev(n):
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
            if isinstance(n, ast.BinOp):
                l, r = ev(n.left), ev(n.right)
                if type(n.op) not in allowed: raise ValueError("op")
                return allowed[type(n.op)](l, r)
            if isinstance(n, ast.UnaryOp):
                return allowed[type(n.op)](ev(n.operand))
            if isinstance(n, ast.Expression): return ev(n.body)
            raise ValueError("bad")
        try:
            tree = ast.parse(expr, mode="eval")
            r = ev(tree)
            await safe_send(ctx, f"{expr} = {r}", delete_after=15)
        except Exception:
            await safe_send(ctx, "Invalid expression.", delete_after=5)

    @b.command(name="timestamp")
    async def _ts(ctx):
        track_cmd("timestamp"); await del_msg(ctx.message)
        now = datetime.datetime.utcnow()
        await safe_send(ctx, f"UTC: {now.strftime('%Y-%m-%d %H:%M:%S')}\nUnix: {int(time.time())}", delete_after=15)

    @b.command(name="poll")
    async def _poll(ctx, *, text: str = None):
        track_cmd("poll"); await del_msg(ctx.message)
        if not text or "|" not in text:
            return await safe_send(ctx, "Usage: $poll question|opt1|opt2|opt3", delete_after=8)
        parts = [p.strip() for p in text.split("|")]
        q = parts[0]
        opts = parts[1:]
        if len(opts) < 2 or len(opts) > 10:
            return await safe_send(ctx, "Need 2-10 options.", delete_after=5)
        emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        body = ""
        for i, o in enumerate(opts):
            body += f"{emojis[i]} {o}\n"
        e = discord.Embed(title=q, description=body, color=discord.Color.red())
        m = await ctx.send(embed=e)
        for i in range(len(opts)):
            try: await m.add_reaction(emojis[i])
            except: pass

    @b.command(name="timer")
    async def _timer(ctx, seconds: int = 60):
        track_cmd("timer"); await del_msg(ctx.message)
        seconds = max(1, min(seconds, 86400))
        await safe_send(ctx, f"Timer set for {seconds}s.", delete_after=5)
        await asyncio.sleep(seconds)
        try: await ctx.author.send(f"Timer done ({seconds}s).")
        except: pass
        try: await ctx.send(f"{ctx.author.mention} timer done.")
        except: pass

    @b.command(name="remind")
    async def _remind(ctx, seconds: int = 60, *, text: str = "reminder"):
        track_cmd("remind"); await del_msg(ctx.message)
        seconds = max(1, min(seconds, 86400))
        await safe_send(ctx, f"Reminder in {seconds}s: {text}", delete_after=5)
        await asyncio.sleep(seconds)
        try: await ctx.author.send(f"Reminder: {text}")
        except: pass
        try: await ctx.send(f"{ctx.author.mention} {text}")
        except: pass

    @b.command(name="color")
    async def _color(ctx, hexv: str = "ff0044"):
        track_cmd("color"); await del_msg(ctx.message)
        h = hexv.strip().lstrip("#")
        if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
            return await safe_send(ctx, "Invalid hex (e.g. ff0044).", delete_after=5)
        e = discord.Embed(title=f"#{h.upper()}", color=int(h, 16))
        e.set_image(url=f"https://singlecolorimage.com/get/{h}/200x100")
        await ctx.send(embed=e)

    @b.command(name="qrcode")
    async def _qr(ctx, *, text: str = None):
        track_cmd("qrcode"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "Give text/URL.", delete_after=5)
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(text)}"
        e = discord.Embed(color=discord.Color.red())
        e.set_image(url=url)
        await ctx.send(embed=e)

    @b.command(name="shorten")
    async def _shorten(ctx, url: str = None):
        track_cmd("shorten"); await del_msg(ctx.message)
        if not url: return await safe_send(ctx, "Give a URL.", delete_after=5)
        try:
            r = requests.get(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}", timeout=10)
            if r.status_code == 200:
                await safe_send(ctx, r.text, delete_after=20)
            else:
                await safe_send(ctx, "Failed to shorten.", delete_after=5)
        except Exception as e:
            await safe_send(ctx, f"Error: {e}", delete_after=8)

    @b.command(name="define")
    async def _def(ctx, word: str = None):
        track_cmd("define"); await del_msg(ctx.message)
        if not word: return await safe_send(ctx, "Give a word.", delete_after=5)
        try:
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}", timeout=10)
            if r.status_code == 200:
                d = r.json()[0]
                word_name = d["word"]
                defs = []
                for m in d.get("meanings", [])[:3]:
                    pos = m.get("partOfSpeech", "?")
                    for dfn in m.get("definitions", [])[:2]:
                        defs.append(f"[{pos}] {dfn['definition']}")
                out = f"{word_name}:\n" + "\n".join(defs[:5])
                await safe_send(ctx, code_block(out), delete_after=25)
            else:
                await safe_send(ctx, "No definition found.", delete_after=5)
        except Exception:
            await safe_send(ctx, "Lookup failed.", delete_after=5)

    @b.command(name="weather")
    async def _weather(ctx, *, city: str = None):
        track_cmd("weather"); await del_msg(ctx.message)
        if not city: return await safe_send(ctx, "Give a city.", delete_after=5)
        try:
            r = requests.get(f"https://wttr.in/{urllib.parse.quote(city)}?format=%C+%t+%h+%w", timeout=10,
                             headers={"User-Agent":"curl/8"})
            if r.status_code == 200 and r.text.strip():
                await safe_send(ctx, f"Weather for {city}: {r.text.strip()}", delete_after=20)
            else:
                await safe_send(ctx, "Could not get weather.", delete_after=5)
        except Exception:
            await safe_send(ctx, "Lookup failed.", delete_after=5)

    @b.command(name="ip")
    async def _ip(ctx, ipaddr: str = ""):
        track_cmd("ip"); await del_msg(ctx.message)
        if not ipaddr:
            ipaddr = ""
        try:
            r = requests.get(f"http://ip-api.com/json/{ipaddr}", timeout=10)
            if r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    out = (
                        f"IP: {d['query']}\n"
                        f"Country: {d['country']} ({d['countryCode']})\n"
                        f"Region: {d['regionName']}\n"
                        f"City: {d['city']}\n"
                        f"ISP: {d['isp']}\n"
                        f"Org: {d.get('org','?')}\n"
                        f"Timezone: {d['timezone']}"
                    )
                    await safe_send(ctx, code_block(out), delete_after=25)
                else:
                    await safe_send(ctx, "Lookup failed.", delete_after=5)
            else:
                await safe_send(ctx, "Lookup failed.", delete_after=5)
        except Exception:
            await safe_send(ctx, "Network error.", delete_after=5)

    @b.command(name="userid")
    async def _userid(ctx, *, user: str = None):
        track_cmd("userid"); await del_msg(ctx.message)
        t = await get_user(ctx, user) or ctx.author
        await safe_send(ctx, f"{t.name}: {t.id}", delete_after=15)

    @b.command(name="serverid")
    async def _serverid(ctx):
        track_cmd("serverid"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        await safe_send(ctx, f"{ctx.guild.name}: {ctx.guild.id}", delete_after=15)

    @b.command(name="chinfo")
    async def _chinfo(ctx):
        track_cmd("chinfo"); await del_msg(ctx.message)
        ch = ctx.channel
        out = f"Name: #{ch.name}\nID: {ch.id}\nType: {ch.type}\nCreated: {ch.created_at.strftime('%Y-%m-%d')}"
        if hasattr(ch, "topic") and ch.topic:
            out += f"\nTopic: {ch.topic}"
        if hasattr(ch, "nsfw"):
            out += f"\nNSFW: {ch.nsfw}"
        await safe_send(ctx, code_block(out), delete_after=20)

    @b.command(name="invite")
    async def _invite(ctx, max_age: int = 0, max_uses: int = 0):
        track_cmd("invite"); await del_msg(ctx.message)
        if not hasattr(ctx.channel, "create_invite"):
            return await safe_send(ctx, "Cannot create invite here.", delete_after=5)
        try:
            inv = await ctx.channel.create_invite(max_age=max_age, max_uses=max_uses)
            await safe_send(ctx, f"Invite: {inv.url}", delete_after=30)
        except Exception as e:
            await safe_send(ctx, f"Failed: {e}", delete_after=8)
