# -*- coding: utf-8 -*-
"""Information commands (read-only)."""
from utils.common import *

def register(b, state):

    @b.command(name="userinfo", aliases=["whois"])
    async def _ui(ctx, *, user: str = None):
        track_cmd("userinfo"); await del_msg(ctx.message)
        t = await get_user(ctx, user) or ctx.author
        created = t.created_at.strftime("%Y-%m-%d %H:%M")
        lines = [
            f"User: {t.name}#{getattr(t,'discriminator','0')}",
            f"Display: {getattr(t,'display_name',t.name)}",
            f"ID: {t.id}",
            f"Bot: {getattr(t,'bot',False)}",
            f"Created: {created}",
        ]
        if isinstance(t, discord.Member):
            joined = t.joined_at.strftime("%Y-%m-%d %H:%M") if t.joined_at else "?"
            roles = [r.name for r in t.roles if not r.is_default()]
            lines.append(f"Joined: {joined}")
            lines.append(f"Nick: {t.nick or '-'}")
            lines.append(f"Roles ({len(roles)}): {', '.join(roles[:20]) if roles else '-'}")
            lines.append(f"Top role: {t.top_role}")
        avatar = t.avatar.url if t.avatar else "-"
        lines.append(f"Avatar: {avatar}")
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=30)

    @b.command(name="serverinfo")
    async def _si(ctx):
        track_cmd("serverinfo"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        g = ctx.guild
        lines = [
            f"Name: {g.name}",
            f"ID: {g.id}",
            f"Owner: {g.owner}",
            f"Created: {g.created_at.strftime('%Y-%m-%d')}",
            f"Members: {g.member_count}",
            f"Text channels: {len(g.text_channels)}",
            f"Voice channels: {len(g.voice_channels)}",
            f"Categories: {len(g.categories)}",
            f"Roles: {len(g.roles)}",
            f"Emojis: {len(g.emojis)}",
            f"Verification: {g.verification_level}",
            f"Boosts: {g.premium_subscription_count or 0} (tier {g.premium_tier})",
        ]
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=30)

    @b.command(name="roleinfo")
    async def _ri(ctx, *, role_name: str = None):
        track_cmd("roleinfo"); await del_msg(ctx.message)
        if not ctx.guild or not role_name:
            return await safe_send(ctx, "Usage: $roleinfo [name]", delete_after=5)
        role = None
        for r in ctx.guild.roles:
            if role_name.lower() in r.name.lower():
                role = r; break
        if not role: return await safe_send(ctx, "Role not found.", delete_after=5)
        lines = [
            f"Name: {role.name}",
            f"ID: {role.id}",
            f"Color: #{role.color.value:06x}",
            f"Hoisted: {role.hoist}",
            f"Mentionable: {role.mentionable}",
            f"Position: {role.position}",
            f"Members: {len(role.members)}",
            f"Managed: {role.managed}",
        ]
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=25)

    @b.command(name="channelinfo", aliases=["cinfo"])
    async def _ci(ctx, *, channel_name: str = None):
        track_cmd("channelinfo"); await del_msg(ctx.message)
        ch = ctx.channel
        if channel_name and ctx.guild:
            for c in ctx.guild.channels:
                if channel_name.lower() in c.name.lower():
                    ch = c; break
        lines = [
            f"Name: #{ch.name}",
            f"ID: {ch.id}",
            f"Type: {ch.type}",
            f"Created: {ch.created_at.strftime('%Y-%m-%d')}",
            f"Position: {getattr(ch,'position','?')}",
        ]
        if hasattr(ch, "topic") and ch.topic:
            lines.append(f"Topic: {ch.topic}")
        if hasattr(ch, "nsfw"):
            lines.append(f"NSFW: {ch.nsfw}")
        if hasattr(ch, "slowmode_delay"):
            lines.append(f"Slowmode: {ch.slowmode_delay}s")
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=25)

    @b.command(name="perms")
    async def _perms(ctx, *, user: str = None):
        track_cmd("perms"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        t = await get_user(ctx, user) or ctx.author
        if not isinstance(t, discord.Member):
            return await safe_send(ctx, "Member not on server.", delete_after=5)
        perms = t.guild_permissions
        important = ["administrator", "manage_guild", "manage_roles", "manage_channels",
                     "ban_members", "kick_members", "manage_messages", "mention_everyone",
                     "manage_nicknames", "manage_webhooks", "manage_emojis", "create_instant_invite",
                     "send_messages", "attach_files", "embed_links", "connect", "speak", "move_members"]
        lines = [f"Permissions for {t.name} in {ctx.guild.name}:"]
        for p in important:
            v = getattr(perms, p, False)
            mark = "+" if v else "-"
            lines.append(f"  [{mark}] {p}")
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=25)

    @b.command(name="botinfo")
    async def _bi(ctx):
        track_cmd("botinfo"); await del_msg(ctx.message)
        app = ctx.bot.user
        lines = [
            f"Username: {app.name}",
            f"ID: {app.id}",
            f"Servers: {len(ctx.bot.guilds)}",
            f"Latency: {round(ctx.bot.latency*1000)}ms",
            f"Uptime: {fmt_time(time.time()-START_TIME)}",
            f"Python: {platform.python_version()}",
            f"Commands run: {sum(COMMAND_USAGE.values())}",
        ]
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=20)

    @b.command(name="listroles")
    async def _lr(ctx):
        track_cmd("listroles"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        lines = [f"{r.position:3d} | #{r.color.value:06x} | {r.name} ({len(r.members)})" for r in ctx.guild.roles]
        out = "\n".join(lines[-40:])
        await safe_send(ctx, code_block(f"Last 40 roles:\n{out}"), delete_after=25)

    @b.command(name="listbots")
    async def _lb(ctx):
        track_cmd("listbots"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        bots = [m for m in ctx.guild.members if m.bot]
        lines = [f"{m.name} ({m.id})" for m in bots]
        out = f"Bots ({len(bots)}):\n" + "\n".join(lines)
        await safe_send(ctx, code_block(out), delete_after=25)

    @b.command(name="listbans")
    async def _lbans(ctx):
        track_cmd("listbans"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        try:
            bans = [entry async for entry in ctx.guild.bans(limit=50)]
            lines = [f"{b.user.name} ({b.user.id}) reason: {b.reason or '-'}" for b in bans]
            out = f"Bans ({len(lines)} shown):\n" + "\n".join(lines[:30])
            await safe_send(ctx, code_block(out), delete_after=25)
        except Exception as e:
            await safe_send(ctx, f"Cannot view bans: {e}", delete_after=8)

    @b.command(name="listinvites")
    async def _li(ctx):
        track_cmd("listinvites"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        try:
            invs = await ctx.guild.invites()
            lines = [f"{i.code} | uses: {i.uses} | {i.inviter} | ch: {i.channel}" for i in invs]
            out = "\n".join(lines[:20]) if lines else "No invites."
            await safe_send(ctx, code_block(out), delete_after=20)
        except Exception as e:
            await safe_send(ctx, f"Cannot view invites: {e}", delete_after=8)

    @b.command(name="listemojis")
    async def _le(ctx):
        track_cmd("listemojis"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        emojis = ctx.guild.emojis
        static = [str(e) for e in emojis if not e.animated]
        animated = [str(e) for e in emojis if e.animated]
        lines = [f"Static ({len(static)}): {' '.join(static[:50])}",
                 f"Animated ({len(animated)}): {' '.join(animated[:50])}"]
        out = "\n".join(lines)
        if len(out) > 1900: out = out[:1900]
        await safe_send(ctx, out, delete_after=20)

    @b.command(name="members")
    async def _mem(ctx):
        track_cmd("members"); await del_msg(ctx.message)
        if not ctx.guild: return await safe_send(ctx, "Server only.", delete_after=5)
        c = ctx.guild.member_count
        online = sum(1 for m in ctx.guild.members if m.status != discord.Status.offline)
        bots = sum(1 for m in ctx.guild.members if m.bot)
        await safe_send(ctx, code_block(f"Total: {c}\nOnline: {online}\nBots: {bots}\nHumans: {c-bots}"), delete_after=15)
