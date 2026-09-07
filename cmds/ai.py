# -*- coding: utf-8 -*-
"""AI category - chat with any OpenAI-compatible endpoint."""
from utils.common import *

CONFIG_PATH = "data/ai_configs.json"
SYSTEM_PROMPT = (
    "You are a helpful assistant in a Discord selfbot. "
    "Keep all responses under 1500 characters. Be concise. "
    "If the answer requires a large block of code (over 50 lines) or exceeds 1500 characters, "
    "say that you will attach it as a file, then provide a short summary. "
    "You may include code blocks when small."
)

def load_configs():
    return load_json(CONFIG_PATH, {"configs": [], "active": 0})

def save_configs(data):
    save_json(CONFIG_PATH, data)

def looks_like_code(text):
    """Heuristic: lots of lines that look like code."""
    lines = text.split("\n")
    if len(lines) > 50:
        return True
    # Count code-like indicators
    code_markers = 0
    for ln in lines:
        s = ln.strip()
        if any(s.startswith(p) for p in ["def ", "class ", "import ", "from ", "function ", "const ", "let ", "var ", "async ", "await ", "public ", "private ", "//", "/*", "*/", "{", "}", ";", "#include", "package ", "func ", "fn ", "int ", "str ", "return", "console.log", "print(", "System.out"]):
            code_markers += 1
    return code_markers / max(len(lines), 1) > 0.4 and len(lines) > 20

async def call_ai_sync(cfg, prompt):
    """Run sync HTTP call in executor."""
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: _call_ai_sync(cfg, prompt)
    )

def _call_ai_sync(cfg, prompt):
    endpoint = cfg.get("endpoint", "https://api.openai.com/v1/chat/completions")
    model = cfg.get("model", "gpt-3.5-turbo")
    api_key = cfg.get("api_key", "")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
    }
    r = requests.post(endpoint, headers=headers, json=payload, timeout=55)
    r.raise_for_status()
    d = r.json()
    if "choices" in d and d["choices"]:
        return d["choices"][0].get("message", {}).get("content", "").strip()
    return str(d)

def send_as_file(channel, content, filename="response.txt"):
    """Send long/code content as a .txt file attachment."""
    import io
    buf = io.BytesIO(content.encode("utf-8"))
    return channel.send(file=discord.File(buf, filename=filename))

def register(b, state):

    # ---- ADD AI CONFIG ----
    @b.command(name="aiadd")
    async def _aiadd(ctx, endpoint: str, model: str, *, api_key_or_id: str = ""):
        track_cmd("aiadd")
        await del_msg(ctx.message)

        # We need either:
        #   $aiadd <endpoint> <model> [api_key]
        # Or: $aiadd <name_id> <model> <api_key>  — we treat positional args flexibly.
        # To keep it simple we just accept endpoint model key, with endpoint being
        # any URL starting with http(s), otherwise treat first arg as a label/name.
        data = load_configs()
        configs = data.get("configs", [])

        # Parse: if first arg starts with http, it's endpoint; else it's a label + use default openai
        if endpoint.lower().startswith("http"):
            # endpoint model [key]
            new_cfg = {
                "label": f"ai{len(configs)+1}",
                "endpoint": endpoint,
                "model": model,
                "api_key": api_key_or_id.strip(),
                "added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        else:
            # Treat <endpoint> as label, model as model, api_key_or_id as key; use openai default endpoint
            new_cfg = {
                "label": endpoint,
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "model": model,
                "api_key": api_key_or_id.strip(),
                "added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            }

        configs.append(new_cfg)
        # If this is the first config, set it as active
        if len(configs) == 1:
            data["active"] = 0
        data["configs"] = configs
        save_configs(data)
        idx = len(configs)
        masked_key = (new_cfg["api_key"][:6] + "..." + new_cfg["api_key"][-4:]) if len(new_cfg["api_key"]) > 12 else "(set)" if new_cfg["api_key"] else "(none)"
        await safe_send(
            ctx,
            code_block(
                f"AI config added (#{idx})\n"
                f"Label:    {new_cfg['label']}\n"
                f"Endpoint: {new_cfg['endpoint']}\n"
                f"Model:    {new_cfg['model']}\n"
                f"Key:      {masked_key}\n"
                f"Active:   #{data['active']+1} (use $ai to query)"
            ),
            delete_after=20,
        )

    # ---- LIST AI CONFIGS ----
    @b.command(name="ailist")
    async def _ailist(ctx):
        track_cmd("ailist")
        await del_msg(ctx.message)
        data = load_configs()
        configs = data.get("configs", [])
        active = data.get("active", 0)
        if not configs:
            return await safe_send(ctx, code_block("No AI configs.\nAdd one: $aiadd <endpoint> <model> [key]"), delete_after=15)
        lines = ["AI configs:"]
        for i, c in enumerate(configs, 1):
            star = " <-- active" if (i - 1) == active else ""
            key = "key-set" if c.get("api_key") else "no-key"
            lines.append(
                f"  {i}. {c.get('label', '?'):<15} model={c.get('model','?'):<20} {key}{star}"
            )
        lines.append("")
        lines.append("Use $ai [question] with the active config.")
        lines.append("Switch by adding a new config, or edit data/ai_configs.json directly.")
        await safe_send(ctx, code_block("\n".join(lines)), delete_after=25)

    # ---- REMOVE AI CONFIG ----
    @b.command(name="air", aliases=["airemove", "airm", "aidel"])
    async def _air(ctx, nr: int = None):
        track_cmd("air")
        await del_msg(ctx.message)
        if nr is None:
            return await safe_send(ctx, code_block("Usage: $air [number]\nSee $ailist for numbers."), delete_after=10)
        data = load_configs()
        configs = data.get("configs", [])
        idx = nr - 1
        if not (0 <= idx < len(configs)):
            return await safe_send(ctx, f"Invalid number. Choose 1-{len(configs)}.", delete_after=6)
        removed = configs.pop(idx)
        # Adjust active index
        active = data.get("active", 0)
        if idx == active:
            data["active"] = 0 if configs else -1
        elif idx < active:
            data["active"] = active - 1
        data["configs"] = configs
        save_configs(data)
        await safe_send(ctx, code_block(f"Removed #{nr}: {removed.get('label','?')} ({removed.get('model','?')})"), delete_after=10)

    # ---- QUERY AI ----
    @b.command(name="ai")
    async def _ai(ctx, *, question: str = None):
        track_cmd("ai")
        await del_msg(ctx.message)
        if not question:
            return await safe_send(ctx, code_block("Usage: $ai [your question]\nSet up with $aiadd first. Use $ailist to see configs."), delete_after=12)

        data = load_configs()
        configs = data.get("configs", [])
        active_idx = data.get("active", 0)
        if not configs or active_idx < 0 or active_idx >= len(configs):
            return await safe_send(ctx, code_block("No AI config active.\nAdd one: $aiadd <endpoint> <model> [api_key]\nExample: $aiadd https://api.openai.com/v1/chat/completions gpt-4o-mini sk-xxxx"), delete_after=15)

        cfg = configs[active_idx]

        # Show the user line first
        q_display = question if len(question) < 1500 else question[:1497] + "..."
        header = f"[You] » {q_display}\n[AI] ... thinking"
        # No delete_after here: this same message is reused to display the
        # answer (edit below) or is deleted explicitly in the file branch.
        # An auto-delete timer would remove the finished response instead.
        thinking = await safe_send(ctx, code_block(header))

        try:
            response = await asyncio.wait_for(
                call_ai_sync(cfg, question),
                timeout=58,
            )
        except asyncio.TimeoutError:
            response = "Request timed out (60s)."
        except requests.exceptions.HTTPError as e:
            response = f"HTTP error {e.response.status_code}: {e.response.text[:500]}"
        except Exception as e:
            response = f"Error: {e}"

        # Build final text
        answer = response.strip() if response else "(empty response)"

        # Decide whether to send as file
        send_as_file_flag = len(answer) > 1500 or looks_like_code(answer)

        # Format user-facing body
        you_line = f"[You] » {q_display}"
        if send_as_file_flag:
            # Short preview + file
            preview = answer[:500] + "\n... (see attached file for full response)"
            body = f"{you_line}\n[AI] {preview}"
            if thinking:
                try:
                    await thinking.delete()
                except Exception:
                    pass
            # Write answer to bytes file
            import io
            buf = io.BytesIO(answer.encode("utf-8"))
            fname = f"ai_response_{int(time.time())}.txt"
            await ctx.send(code_block(body), file=discord.File(buf, filename=fname))
        else:
            body = f"{you_line}\n[AI] {answer}"
            if thinking:
                try:
                    await thinking.edit(content=code_block(body))
                    # Leave the message (don't auto-delete, user wants to see it)
                except Exception:
                    await safe_send(ctx, code_block(body))
            else:
                await safe_send(ctx, code_block(body))

    # Help
    @b.command(name="hai")
    async def _hai(ctx):
        track_cmd("hai")
        await del_msg(ctx.message)
        help_txt = (
            "AI MODULE\n"
            "$aiadd e m [k] - Add endpoint/model/key\n"
            "                 e = URL (https://...) or label\n"
            "                 m = model name (e.g. gpt-4o-mini)\n"
            "                 k = API key (optional)\n"
            "$ailist        - List saved configs\n"
            "$air [n]       - Remove config #n\n"
            "$ai [question] - Ask the active AI\n"
            "$aiswitch [n]  - Switch active config\n"
            "\n"
            "Responses >1500 chars or big code\n"
            "attach as response.txt.\n"
            "Format: [You] » question / [AI] answer"
        )
        await safe_send(ctx, code_block(help_txt), delete_after=25)

    # ---- SWITCH ACTIVE ----
    @b.command(name="aiswitch")
    async def _aisw(ctx, nr: int = None):
        track_cmd("aiswitch")
        await del_msg(ctx.message)
        if nr is None:
            return await safe_send(ctx, code_block("Usage: $aiswitch [number]\nSee $ailist."), delete_after=10)
        data = load_configs()
        configs = data.get("configs", [])
        idx = nr - 1
        if not (0 <= idx < len(configs)):
            return await safe_send(ctx, f"Invalid number. 1-{len(configs)}.", delete_after=6)
        data["active"] = idx
        save_configs(data)
        c = configs[idx]
        await safe_send(ctx, code_block(f"Active AI now #{nr}: {c.get('label')} ({c.get('model')})"), delete_after=10)
