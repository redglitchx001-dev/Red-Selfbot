# -*- coding: utf-8 -*-
"""
RED SELFBOT - ASCII art generator for the admin panel.

Renders every panel section word with pyfiglet (font: ANSI Shadow) and
applies a top->bottom shading pass so the letters fade:
    row 0-1  █   (solid)
    row 2-3  ▓
    row 4-5  ▒
    row 6    ░   (thin baseline)

Usage:
    python make_art.py            # prints every art block (for reference)
    python make_art.py TOKEN      # prints a single block
    python make_art.py --html     # prints the ready-to-paste <pre> blocks
    python make_art.py --build-public
                                  # rebuilds panel.html (public page) from
                                  # panel_public.tpl with the exact pyfiglet art
    python make_art.py --fix-html panel.html
                                  # re-injects the exact pyfiglet art into every
                                  # <pre class="art..."> block of the HTML file

The generated art is embedded in panel.html - if you change the words or the
font, run the --fix-html variant so the HTML always matches this generator.
Requires: pip install pyfiglet
"""
import os
import re
import sys
import pyfiglet

# shading pass, top to bottom (ANSI Shadow is 7 rows tall)
SHADE = ["█", "█", "▓", "▓", "▒", "▒", "░"]

# section words shown in the panel (in page order)
WORDS = [
    ("BANNER", "RED SELFBOT"),
    ("WELCOME", "WELCOME"),
    ("STATS", "STATS"),
    ("LOGIN", "LOGIN"),
    ("ADMIN", "ADMIN"),
    ("USERS", "USERS"),
    ("BAN", "BAN"),
    ("TOKEN", "TOKEN"),
    ("ONLINE", "ONLINE"),
    ("SUGESTII", "SUGESTII"),
    ("FOOTER", "2026"),
]


def render(text, font="ansi_shadow"):
    raw = pyfiglet.Figlet(font=font).renderText(text)
    lines = raw.rstrip("\n").split("\n")
    out = []
    for i, line in enumerate(lines):
        row = SHADE[i % len(SHADE)]
        out.append("".join(row if ch.strip() else ch for ch in line.rstrip()))
    # drop fully empty trailing rows
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def as_html(tag, text, cls="art-sm"):
    return '<pre class="%s" data-art="%s">\n%s\n</pre>' % (cls, tag, render(text))


def closest_word(art):
    lines = art.strip("\n").split("\n")
    best, best_score = None, -1
    for _, word in WORDS:
        rendered = render(word).split("\n")
        if len(rendered) != len(lines):
            continue
        score = sum(1 for a, b in zip(rendered, lines) if a == b)
        if score > best_score:
            best, best_score = word, score
    return best


def build_public():
    """Rebuild panel.html (public token page) from panel_public.tpl with exact art."""
    base = os.path.dirname(os.path.abspath(__file__))
    tpl_path = os.path.join(base, "panel_public.tpl")
    out_path = os.path.join(base, "panel.html")
    tpl = open(tpl_path, encoding="utf-8").read()
    words = {
        "RED SELFBOT": "{{ART_BANNER}}",
        "WELCOME": "{{ART_WELCOME}}",
        "LOGIN": "{{ART_LOGIN}}",
        "TOKEN": "{{ART_TOKEN}}",
        "2026": "{{ART_FOOTER}}",
    }
    for word, key in words.items():
        if key not in tpl:
            print("[!] missing placeholder %s in template" % key)
            sys.exit(1)
        tpl = tpl.replace(key, render(word))
    open(out_path, "w", encoding="utf-8").write(tpl)
    print("[i] built %s from %s" % (out_path, tpl_path))


def fix_html(path):
    html = open(path, encoding="utf-8").read()
    count = 0
    def repl(m):
        nonlocal count
        art = m.group(1)
        word = closest_word(art)
        if word is None:
            print("[!] no matching word for block %d (skipped)" % count)
            return m.group(0)
        count += 1
        print("[i] fixed block %d -> %s" % (count, word))
        return m.group(0).split(">", 1)[0] + ">" + render(word) + "</pre>"
    out = re.sub(r'<pre class="[^"]*"[^>]*>(.*?)</pre>', repl, html, flags=re.S)
    open(path, "w", encoding="utf-8").write(out)
    print("[i] done: %d blocks updated in %s" % (count, path))


def main():
    args = [a for a in sys.argv[1:]]
    if "--build-public" in args:
        args.remove("--build-public")
        build_public()
        return
    if "--fix-html" in args:
        args.remove("--fix-html")
        if not args:
            print("usage: make_art.py --fix-html <panel.html>")
            sys.exit(1)
        fix_html(args[0])
        return
    if "--html" in args:
        args.remove("--html")
        for tag, word in WORDS:
            cls = "art" if tag == "BANNER" else "art-sm"
            print(as_html(tag, word, cls))
        return
    if args:
        for word in args:
            print(render(word))
            print()
    else:
        for tag, word in WORDS:
            print("========== %s (%d cols) ==========" % (tag, max((len(l) for l in render(word).split("\n")), default=0)))
            print(render(word))
            print()


if __name__ == "__main__":
    main()
