<p align="center">
  <img src="https://i.postimg.cc/cCG6WF7W/5aaa7b437881d00f0521f9e09dbf39e2.jpg" alt="Red SelfBot Banner">
</p>

<h1 align="center">RED SELFBOT V1</h1>

<p align="center">
  <b>Premium modular Discord selfbot.</b> Python-only build. Live cyberpunk web dashboard,
  165+ commands across 15 categories, modular per-file categories, AI chat, heavy spam packs,
  and `$start` that works in servers / groups / DMs with any custom line file.
</p>

---

## Quick start

```bash
pip install -r requirements.txt
export DISCORD_TOKEN="your_token"      # or echo "your_token" > token.txt
python main.py
```

The dashboard is served on `0.0.0.0:$PORT` (default `3000`, works with preview, not localhost-only). Panel fancy gradient 2026 edition.

## Layout

```
main.py              # Entry + web dashboard 0.0.0.0:3000 fancy gradient 2026
cmds/                # One Python module per category
  help.py   text.py    fun.py     util.py   info.py   spam.py  music.py
  profiles.py cloner.py archives.py protect.py logger.py status.py multi.py ai.py
utils/common.py      # Shared helpers / text transforms
data/                # $start packs 2026 - NO > # prefix, BIG text
  spam_ro.txt        # RO ONLY short 3k lines
  spam_en.txt        # EN ONLY + GIFs short 3k lines
  longspam_ro.txt    # RO LONG 2026 9k lines hardcore roast
  longspam_en.txt    # EN LONG 2026 + GIFs 9k lines
  spam.txt           # MIX RO+EN 4k lines
  lines_ro.txt / lines_en.txt / lines_default.txt # legacy compat
botjura.txt          # Default RO legacy (copy of lines_ro, 9k lines)
generate_lines.py    # Regenerate packs up to 1M each
music/ profiles/ clones/ archives/ logs/   # Runtime storage
```

## Menus

Every help menu is a plain code block (text + symbols only, no inline emojis in the body)
kept under 1900 characters. Jump to categories with:

| Command | Category |
|---|---|
| `$help` / `$REDHELP` | Main menu |
| `$hcore` | Core / bot info |
| `$hmusic` | Music & voice (FFmpeg) |
| `$hspam` | Automation / `$start` sequences |
| `$hprofile` | Profile archiver |
| `$hclone` | Server cloner |
| `$harchive` | Chat archiving |
| `$hprotect` | Protection suite |
| `$hlog` | Logger / snipe / track |
| `$hstatus` | Presence & status |
| `$htext` | Text transforms (mock/leet/vapor/binary/etc.) |
| `$hfun` | Fun & games |
| `$hutil` | Utility commands |
| `$hinfo` | Server/user info lookup |
| `$hai` | AI chat module |
| `$hmulti` | Multi-account |
| `$hall` | Everything in one scroll |

## `$start` — works everywhere [MULTI-USER 2026]

`$start` works in servers, groups, and DMs. Supports multiple users + file at end. Choose your line pack:

```
$start                              # default (spam.txt / $startlang)
$start @bro                         # default pack, pings @bro
$start @user1 @user2 @user3         # 3 users at once (NEW)
$start ionut vasile alex spam_ro.txt # 3 names + file at end (NEW)
$start @bro en.txt                  # en.txt pinging @bro
$start @user1 @user2 longspam_en.txt # 2 users + long EN pack + gifs
$start 123456789 ro.txt             # by user ID, ro.txt
$start en.txt                       # en.txt no mention (EN only + gifs)
$start ro                           # short for spam_ro / lines_ro (RO only)
$startl                             # list all line files fancy gradient
$startlang en                       # switch default to en
$stop                               # halt everything
```

Drop any `.txt` file into `data/` and it will appear in `$startl` immediately — no restart.
Lines can contain `{t}` which gets replaced with the target mention(s); lines without it just get
the mention(s) prepended. Packs are NO `> #` prefix - each line is BIG text as requested.
RO packs = only romana, EN packs = only english + gifs from net.
2026 packs: spam_ro (3k), spam_en (3k + gifs), longspam_ro (9k), longspam_en (9k + gifs), spam (4k mix).
Regenerate larger packs (up to 1 million lines each) with:

```bash
python generate_lines.py 10000   # 10k short / 30k long
python generate_lines.py 1000000 # 1M short / 3M long (heavy)
```

## AI

```
$aiadd https://api.openai.com/v1/chat/completions gpt-4o-mini sk-xxx
$aiadd groq https://api.groq.com/openai/v1/chat/completions llama-3.3-70b-versatile gsk_xxx
$ailist
$aiswitch 2
$ai explain quantum computing in simple terms
```

Responses are formatted `[You] » question / [AI] answer`. Anything over 1500 characters or
large code blocks is sent as `ai_response_<timestamp>.txt` attached to the message
(you asked for exactly that behavior). Works with any OpenAI-compatible endpoint
(OpenAI, Groq, Together, OpenRouter, llama.cpp, Ollama with openai compat, etc.).

## Warning

Selfbots (user-account automation) violate Discord's Terms of Service. Account termination is
a real risk. Educational purposes only — use at your own risk.

## Credits

Original by RedGlitchX / XTASK / xs7david / @193.7 / NTASK. V1 modular + dashboard build.
