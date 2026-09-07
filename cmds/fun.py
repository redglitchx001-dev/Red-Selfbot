# -*- coding: utf-8 -*-
"""Fun / games / reactions / meme commands."""
from utils.common import *

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people: those who understand binary and those who don't.",
]
FACTS = [
    "Honey never spoils. Archaeologists have found pots of honey over 3000 years old.",
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries aren't.",
    "A day on Venus is longer than a year on Venus.",
    "The Eiffel Tower can be 15 cm taller during summer due to thermal expansion.",
    "Wombat poop is cube-shaped.",
    "There are more stars in the universe than grains of sand on Earth.",
]
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Stay hungry, stay foolish. - Stewart Brand",
    "In the middle of difficulty lies opportunity. - Einstein",
    "Code is like humor: when you have to explain it, it's bad. - Cory House",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Talk is cheap. Show me the code. - Linus Torvalds",
    "Simplicity is the soul of efficiency. - Austin Freeman",
]
EIGHTBALL = [
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.",
    "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
    "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
    "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
    "Don't count on it.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful.",
]

def register(b, state):

    @b.command(name="8ball")
    async def _8ball(ctx, *, question: str = ""):
        track_cmd("8ball"); await del_msg(ctx.message)
        if not question: return await safe_send(ctx, "Ask a question.", delete_after=5)
        await safe_send(ctx, f"Q: {question}\nA: {random.choice(EIGHTBALL)}", delete_after=20)

    @b.command(name="flip")
    async def _flip(ctx):
        track_cmd("flip"); await del_msg(ctx.message)
        await safe_send(ctx, random.choice(["Heads.", "Tails."]), delete_after=10)

    @b.command(name="roll")
    async def _roll(ctx, sides: int = 6):
        track_cmd("roll"); await del_msg(ctx.message)
        sides = max(2, min(sides, 1000000))
        await safe_send(ctx, f"Rolled: {random.randint(1, sides)} (1-{sides})", delete_after=10)

    @b.command(name="choose")
    async def _choose(ctx, *, options: str = ""):
        track_cmd("choose"); await del_msg(ctx.message)
        if not options: return await safe_send(ctx, "Separate choices with ; e.g. $choose pizza;pasta;burger", delete_after=8)
        opts = [o.strip() for o in options.split(";") if o.strip()]
        if len(opts) < 2: return await safe_send(ctx, "Give at least 2 choices separated by ;", delete_after=6)
        await safe_send(ctx, f"Chosen: {random.choice(opts)}", delete_after=15)

    @b.command(name="rps")
    async def _rps(ctx, choice: str = ""):
        track_cmd("rps"); await del_msg(ctx.message)
        c = choice.lower()
        if c not in ("r", "p", "s", "rock", "paper", "scissors"):
            return await safe_send(ctx, "Choose r/p/s.", delete_after=5)
        me = random.choice(["r", "p", "s"])
        beats = {"r": "s", "p": "r", "s": "p"}
        names = {"r": "rock", "p": "paper", "s": "scissors"}
        if c[0] == me:
            res = "Tie."
        elif beats[c[0]] == me:
            res = "You win."
        else:
            res = "You lose."
        await safe_send(ctx, f"You: {names[c[0]]} | Me: {names[me]} | {res}", delete_after=15)

    @b.command(name="say")
    async def _say(ctx, *, text: str = ""):
        track_cmd("say"); await del_msg(ctx.message)
        if not text: return
        await ctx.send(text)

    @b.command(name="echo")
    async def _echo(ctx, *, text: str = ""):
        track_cmd("echo"); await del_msg(ctx.message)
        if not text: return
        await ctx.send(text)

    @b.command(name="embed")
    async def _embed(ctx, *, text: str = ""):
        track_cmd("embed"); await del_msg(ctx.message)
        if not text: return await safe_send(ctx, "Use title|description", delete_after=5)
        if "|" in text:
            t, d = text.split("|", 1)
        else:
            t, d = "", text
        e = discord.Embed(title=t.strip() or None, description=d.strip(), color=discord.Color.red())
        e.set_footer(text=f"Red Selfbot V1")
        await ctx.send(embed=e)

    @b.command(name="ascii")
    async def _ascii(ctx, *, text: str = ""):
        track_cmd("ascii"); await del_msg(ctx.message)
        if not text: return
        # Big ASCII letters (simple) - keep short
        font = {
            "A":"█▀█\n█▀█\n▀ ▀","B":"█▀▄\n█▀▄\n▀▀ ","C":"█▀▀\n█  \n▀▀▀","D":"█▀▄\n█  █\n▀▀ ",
            "E":"█▀▀\n█▀▀\n▀▀▀","F":"█▀▀\n█▀▀\n▀  ","G":"█▀▀\n█ ▄█\n▀▀▀","H":"█ █\n█▀█\n▀ ▀",
            "I":"█\n▀▀▀\n█ ","J":"  █\n  █\n▀▀ ","K":"█ ▄\n█▀▄\n▀ ▀","L":"█  \n█  \n▀▀▀",
            "M":"█▄▄▄█\n█ ▀ █\n▀   ▀","N":"█  █\n█▀▀█\n▀  ▀","O":"█▀█\n█ █\n▀▀▀","P":"█▀█\n█▀▀\n▀  ",
            "Q":"█▀█\n█ ▄▀\n▀▀▀","R":"█▀█\n█▀▄\n▀ ▀","S":"█▀▀\n▀▀█\n▀▀▀","T":"▀▀█▀▀\n  █  \n  ▀  ",
            "U":"█ █\n█ █\n▀▀▀","V":"█  █\n█ █\n ▀ ","W":"▀   ▀\n█ ▀ █\n▀▄▄▄▀","X":"▀ ▀\n ▄ \n▀ ▀",
            "Y":"█  █\n ▀▀ \n  ▀ ","Z":"▀▀█\n▄▀ \n▀▀▀"," ":"   ","?":"▀█\n  ▄\n   ","!":"█\n█\n▀",
            "0":"█▀█\n█ █\n▀▀▀","1":" █\n  █\n▀▀█","2":"▀▀█\n▄▀ \n▀▀▀","3":"▀▀█\n ▀█\n▀▀ ",
            "4":"█ █\n▀▀█\n  █","5":"█▀▀\n▀▀█\n▀▀▀","6":"█▀▀\n█▀█\n▀▀▀","7":"▀▀█\n  █\n  ▀",
            "8":"█▀█\n▀▀█\n▀▀▀","9":"█▀█\n▀▀█\n▀▀▀",
        }
        text = text.upper()[:15]
        rows = ["", "", ""]
        for ch in text:
            glyph = font.get(ch, "   \n   \n   ")
            gl = glyph.split("\n")
            for i in range(3):
                rows[i] += gl[i] + "  "
        out = "\n".join(rows)
        if len(out) > 1990:
            out = out[:1990]
        await safe_send(ctx, code_block(out), delete_after=20)

    @b.command(name="clap")
    async def _clap(ctx, *, text: str = ""):
        track_cmd("clap"); await del_msg(ctx.message)
        if not text: return
        await safe_send(ctx, " 👏 ".join(text.split()))

    @b.command(name="lmgtfy")
    async def _lmgtfy(ctx, *, query: str = ""):
        track_cmd("lmgtfy"); await del_msg(ctx.message)
        if not query: return
        from urllib.parse import quote
        await safe_send(ctx, f"<https://letmegooglethat.com/?q={quote(query)}>")

    @b.command(name="rate")
    async def _rate(ctx, *, thing: str = ""):
        track_cmd("rate"); await del_msg(ctx.message)
        if not thing: thing = "you"
        await safe_send(ctx, f"I rate {thing} {random.randint(0,10)}/10.", delete_after=15)

    @b.command(name="pp")
    async def _pp(ctx, *, user: str = None):
        track_cmd("pp"); await del_msg(ctx.message)
        target = await get_user(ctx, user) or ctx.author
        size = random.randint(0, 12)
        await safe_send(ctx, f"{target.name}'s pp: 8{'='*size}D", delete_after=15)

    @b.command(name="howgay")
    async def _gay(ctx, *, user: str = None):
        track_cmd("howgay"); await del_msg(ctx.message)
        target = await get_user(ctx, user) or ctx.author
        rng = random.Random(target.id)
        pct = rng.randint(0, 100)
        await safe_send(ctx, f"{target.name} is {pct}% gay.", delete_after=15)

    @b.command(name="iq")
    async def _iq(ctx, *, user: str = None):
        track_cmd("iq"); await del_msg(ctx.message)
        target = await get_user(ctx, user) or ctx.author
        rng = random.Random(target.id + 1)
        score = rng.randint(40, 180)
        await safe_send(ctx, f"{target.name} has an IQ of {score}.", delete_after=15)

    @b.command(name="joke")
    async def _joke(ctx):
        track_cmd("joke"); await del_msg(ctx.message)
        await safe_send(ctx, random.choice(JOKES), delete_after=20)

    @b.command(name="fact")
    async def _fact(ctx):
        track_cmd("fact"); await del_msg(ctx.message)
        await safe_send(ctx, random.choice(FACTS), delete_after=20)

    @b.command(name="quote")
    async def _quote(ctx):
        track_cmd("quote"); await del_msg(ctx.message)
        await safe_send(ctx, random.choice(QUOTES), delete_after=20)

    @b.command(name="kiss")
    async def _kiss(ctx, *, user: str = None):
        track_cmd("kiss"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention someone.", delete_after=5)
        await safe_send(ctx, f"{ctx.author.name} kisses {t.mention} :kiss:", delete_after=15)

    @b.command(name="hug")
    async def _hug(ctx, *, user: str = None):
        track_cmd("hug"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention someone.", delete_after=5)
        await safe_send(ctx, f"{ctx.author.name} hugs {t.mention} tightly.", delete_after=15)

    @b.command(name="slap")
    async def _slap(ctx, *, user: str = None):
        track_cmd("slap"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention someone.", delete_after=5)
        items = ["a fish", "a trout", "a keyboard", "a stick", "a loaf of bread", "a dictionary"]
        await safe_send(ctx, f"{ctx.author.name} slaps {t.mention} with {random.choice(items)}.", delete_after=15)

    @b.command(name="kill")
    async def _kill(ctx, *, user: str = None):
        track_cmd("kill"); await del_msg(ctx.message)
        t = await get_user(ctx, user)
        if not t: return await safe_send(ctx, "Mention someone.", delete_after=5)
        await safe_send(ctx, f"{ctx.author.name} kills {t.mention}. (joke, obviously)", delete_after=15)

    @b.command(name="dice")
    async def _dice(ctx, count: int = 2):
        track_cmd("dice"); await del_msg(ctx.message)
        count = max(1, min(count, 10))
        rolls = [random.randint(1,6) for _ in range(count)]
        await safe_send(ctx, f"Rolls: {', '.join(map(str,rolls))} = {sum(rolls)}", delete_after=15)

    @b.command(name="pickup")
    async def _pickup(ctx):
        track_cmd("pickup"); await del_msg(ctx.message)
        lines = [
            "Are you a parking ticket? Because you've got 'fine' written all over you.",
            "Do you have a map? I keep getting lost in your eyes.",
            "Are you made of copper and tellurium? Because you're Cu-Te.",
            "If you were a vegetable, you'd be a cute-cumber.",
        ]
        await safe_send(ctx, random.choice(lines), delete_after=15)

    @b.command(name="roast")
    async def _roast(ctx):
        track_cmd("roast"); await del_msg(ctx.message)
        roasts = [
            "You're the reason they put instructions on shampoo.",
            "You bring everyone so much joy... when you leave the room.",
            "You're like a cloud. When you disappear, it's a beautiful day.",
            "I'd agree with you but then we'd both be wrong.",
        ]
        await safe_send(ctx, random.choice(roasts), delete_after=15)
