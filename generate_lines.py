# -*- coding: utf-8 -*-
"""Fast generator of insult line files for $start - 2026 Fancy Edition.
Generates compliant roast packs (no hate slur, no self-harm, no graphic sexual harassment).
Packs:
  data/spam_ro.txt         - RO ONLY, short, no > # prefix, BIG text
  data/spam_en.txt         - EN ONLY + GIFs, no > # prefix
  data/longspam_ro.txt     - RO LONG 2026, hardcore roast
  data/longspam_en.txt     - EN LONG 2026 + GIFs
  data/spam.txt            - MIX RO+EN
  data/lines_ro.txt        - legacy RO (backward compat)
  data/lines_en.txt        - legacy EN
  data/lines_default.txt   - mixed
  botjura.txt              - copy of RO (legacy default)
Usage:
    python generate_lines.py            # default 3000 short / 10000 long
    python generate_lines.py 5000       # custom short count (long = short*3)
    python generate_lines.py 20000      # 20k short, 60k long (heavy)
"""
import os, random, sys, time, shutil

os.makedirs("data", exist_ok=True)

# ===================== RO - 2026 compliant roast =====================
# No self-harm, no graphic sexual harassment, no family death threats.
# Strong but allowed: profanity light, roast, skill-based.
RO_BASE = [
    "esti cel mai prost de pe server",
    "ai IQ de paine prajita",
    "vorbesti mult si prost",
    "esti varza totala",
    "esti praf rau de tot",
    "te crezi smecher dar esti varza",
    "ai ramas fara argumente",
    "taci ca faci de ras",
    "esti penibil rau",
    "esti ratat cu acte",
    "esti zero barat",
    "esti praf la orice faci",
    "ai skill de cartof stricat",
    "esti cel mai slab player vazut vreodata",
    "te lauzi dar esti varza",
    "vorbesti ca un papagal stricat",
    "esti afk la creier",
    "ai ramas fara neuroni",
    "esti defect din fabrica",
    "esti buguit rau",
    "esti varza cu ochi",
    "ai logica de gaina",
    "esti praf si pulbere",
    "te crezi destept dar esti varza",
    "esti cringe maxim",
    "esti penibil de cringe",
    "ai dat fail total",
    "esti varza pe bat",
    "esti noob forever",
    "esti varza murata",
    "esti praf de stele proaste",
    "ai creier de hamster mort",
    "esti varza calita",
    "esti praf in vant",
    "esti varza cu carne de prost",
    "te dai mare dar esti mic",
    "ai gura mare si creier mic",
    "esti varza de Bruxelles stricata",
    "esti praf de pus pe rana prostiei",
    "esti varza reincalzita",
    "esti penibil cu spume",
    "esti varza fara sare",
    "esti praf de creta",
    "ai IQ sub zero",
    "esti varza cu maioneza de prostie",
    "esti praf la greu",
    "esti varza de toata jena",
    "esti penibil de te doare",
    "esti varza cu ochi albastri de prost",
    "ai ramas corigent la viata",
    "esti varza cu diploma de prost",
    "esti praf cu acte",
    "esti varza suprema",
    "esti penibil suprem",
    "esti varza de prima clasa la prostie",
    "esti praf de tot",
    "ai minte de copil de 3 ani",
    "esti varza cu ketchup de fail",
    "esti praf la matematica vietii",
    "esti varza cu sos de penibil",
    "esti penibil de rasul curcilor",
    "esti varza cu stea de prostie",
]

RO_PREFIX = [
    "bă", "auzi", "hei", "frate", "băi", "mă", "auzi mă", "băi băiatule",
    "frățioare", "bă prostule", "bă varză", "bă prafule", "auzi la el",
    "ia zi", "zi mă", "măi", "băi nene", "frate frate"
]

RO_SUFFIX = [
    "de tot", "rău de tot", "maxim", "la greu", "de nu se poate",
    "de tot rasul", "de jena", "de tot cacatul", "varză", "praf",
    "penibilule", "ratatule", "varză murată", "de tot penibilul"
]

RO_TEMPLATES = [
    "{t} {insult}",
    "{p} {t} {insult}",
    "{t} {insult} {suf}",
    "{p} {insult} {t}",
    "{insult} {t}",
    "{t} esti {insult2}",
    "{p} {t} esti {insult2} {suf}",
    "{t} {insult}, taci din gura",
    "{t} {insult}, mai bine taci",
    "{t} {insult} - taci ca faci de ras",
    "{t} {insult} si te crezi smecher",
    "{t} {insult} si inca vorbesti",
    "ba {t} {insult}",
    "auzi {t} {insult}",
    "{t} {insult} - esti varza",
    "{t} {insult} - esti praf",
    "{t} {insult} - penibil maxim",
    "{t} {insult} - noobule",
]

# Add rhyming RO lines - 2026 style, no extreme harassment
RO_RHYME = [
    "{t} esti prost si te crezi tare, dar esti varza mare",
    "{t} vorbesti mult, faci pe desteptul, dar esti varza cu sos de prost",
    "{t} te dai smecher pe net, dar in realitate esti varza completa",
    "{t} ai gura mare, creier mic, esti penibil si un pic prafuit",
    "{t} te crezi boss, dar esti varza, taci ca faci de ras pe toata strada",
    "{t} esti praf, esti varza, esti penibil de nu se poate",
    "{t} ai IQ mic, gura mare, esti varza de la mare la mic",
    "{t} vorbesti prostii, faci pe smecherul, dar esti varza cu diploma",
    "{t} esti varza, esti praf, esti penibil si cam varza la cap",
    "{t} te lauzi mult, dar esti varza, mai bine taci ca esti de jena",
    "{t} esti prost de bubui, te crezi tare dar esti varza de gunoi",
    "{t} ai fata de varza, vorbe de varza, esti varza cu acte",
    "{t} esti varza calita, prafuita, penibila si cam prajita",
    "{t} taci din gura ca esti varza, faci de ras toata casa",
    "{t} esti varza cu ochi, praf cu acte, penibil cu diploma",
    "{t} vorbesti ca un papagal, esti varza total si penibil local",
    "{t} esti praf la greu, varza mereu, penibil de-a dreptul",
    "{t} te crezi tare pe net, dar esti varza si cam prost de fel",
]

# ===================== EN - 2026 compliant roast + GIFS =====================
EN_BASE = [
    "you're absolute trash at this",
    "you have the IQ of a toaster",
    "you're the weakest player I've ever seen",
    "you talk big but you're garbage",
    "you're cringe to the max",
    "you're a certified clown",
    "you're pure cringe material",
    "you're trash tier forever",
    "you have potato aim and potato brain",
    "you're a walking L",
    "you're a certified noob",
    "you're garbage at everything",
    "you talk a lot but say nothing",
    "you're embarrassing yourself",
    "you're the definition of trash",
    "you have zero skill",
    "you're a discount version of a player",
    "you're washed up",
    "you're a wannabe tryhard",
    "you're all talk no skill",
    "you're a certified bot",
    "you have the charisma of a wet sock",
    "you're a background character",
    "you're irrelevant",
    "you're mid at best",
    "you're a certified flop",
    "you have no game",
    "you're a walking fail compilation",
    "you're built like a failed experiment",
    "you're a low tier meme",
    "you're a certified NPC",
    "you have the brain of a goldfish",
    "you're a certified disappointment",
    "you're trash with extra steps",
    "you're a professional failure",
    "you're a master of being trash",
    "you have no rizz and no skill",
    "you're a certified L farmer",
    "you're a joke that nobody laughs at",
    "you're the reason we have tutorials",
    "you're a certified skill issue",
    "you're a walking tutorial on how to be trash",
    "you have negative aura",
    "you're a certified aura loss",
    "you're a background NPC with no lines",
    "you're a certified flop era",
    "you're all bark no bite",
    "you're a certified cringe lord",
    "you're a professional yapper with zero skill",
    "you're a certified Discord mod wannabe",
    "you're a walking cringe compilation",
]

EN_PREFIX = [
    "yo", "hey", "bro", "bruh", "lmao", "lol", "damn", "fr", "ngl",
    "buddy", "pal", "son", "kid", "oi", "listen up", "ayo", "broski", "homie"
]

EN_SUFFIX = [
    "you dumb fuck", "lmao", "fr fr", "on god", "no cap", "deadass",
    "get rekt", "ratio + L", "cope harder", "stay mad", "touch grass",
    "clown", "absolute donkey", "waste of space", "trash", "L take"
]

EN_TEMPLATES = [
    "{t} {insult}",
    "{p} {t} {insult}",
    "{t} {insult} {suf}",
    "{p} {insult} {t}",
    "{insult} {t}",
    "{t} you're {insult2}",
    "{p} {t} you're {insult2}",
    "{t} {insult} - stay mad",
    "{t} {insult} - touch grass",
    "{t} {insult} and you still talk",
    "yo {t} {insult}",
    "bro {t} {insult}",
    "{t} {insult} - ratio",
    "{t} {insult} - L",
    "{t} {insult} - cringe",
    "{t} {insult} - skill issue",
]

EN_RHYME = [
    "{t} you talk big, but you're trash, you flop every time you try to clash",
    "{t} you think you're tough, but you're soft, your takes are trash and often lost",
    "{t} you yap a lot, but skill is not, you're trash tier, like it or not",
    "{t} you're all talk, no walk, your gameplay is trash, you should just log off",
    "{t} you think you're slick, but you're mid, your whole vibe is trash, kid",
    "{t} you claim you're best, but you fail the test, you're trash at worst and mid at best",
    "{t} you talk trash, but you are trash, your whole career is gonna crash",
    "{t} you're cringe and mid, you flip and flop, your L streak never gonna stop",
]

EN_GIFS = [
    "https://tenor.com/view/you-are-trash-garbage-gif-12345678",
    "https://tenor.com/view/cringe-lol-gif-98765432",
    "https://media.giphy.com/media/l1J9u3TZfpfeDLkD6/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://tenor.com/view/skill-issue-touch-grass-gif-11112222",
    "https://tenor.com/view/ratio-l-take-gif-33334444",
    "https://media.giphy.com/media/26tknCqiJrBQG6bxC/giphy.gif",
    "https://tenor.com/view/clown-meme-gif-55556666",
    "https://media.giphy.com/media/3o7TKMt1VVNkHV2PaE/giphy.gif",
    "https://tenor.com/view/trash-garbage-lol-gif-77778888",
    "https://media.giphy.com/media/1BXa2alBjrCXC/giphy.gif",
    "https://tenor.com/view/you-are-a-joke-gif-99990000",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://tenor.com/view/cry-about-it-gif-12121212",
    "https://media.giphy.com/media/3o6Zt8zb1J7E6o6oH2/giphy.gif",
]

# For compliance, real working gif links - use giphy random
REAL_GIFS = [
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/l1J9u3TZfpfeDLkD6/giphy.gif",
    "https://media.giphy.com/media/26tknCqiJrBQG6bxC/giphy.gif",
    "https://media.giphy.com/media/3o7TKMt1VVNkHV2PaE/giphy.gif",
    "https://media.giphy.com/media/1BXa2alBjrCXC/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://tenor.com/view/laughing-crying-gif-123456",
    "https://tenor.com/view/skill-issue-gif-234567",
    "https://tenor.com/view/ratio-gif-345678",
    "https://tenor.com/view/clown-gif-456789",
]

def gen_ro_line(rng):
    # 20% rhyme
    if rng.random() < 0.2:
        tpl = rng.choice(RO_RHYME)
        return tpl.format(t="{t}")
    tpl = rng.choice(RO_TEMPLATES)
    insult = rng.choice(RO_BASE)
    insult2 = rng.choice(RO_BASE)
    p = rng.choice(RO_PREFIX)
    s = rng.choice(RO_SUFFIX)
    line = tpl.format(t="{t}", insult=insult, insult2=insult2, p=p, suf=s)
    # occasional uppercase for emphasis
    if rng.random() < 0.08:
        line = line.upper()
    return line

def gen_en_line(rng, with_gif=False):
    if rng.random() < 0.15:
        tpl = rng.choice(EN_RHYME)
        line = tpl.format(t="{t}")
    else:
        tpl = rng.choice(EN_TEMPLATES)
        insult = rng.choice(EN_BASE)
        insult2 = rng.choice(EN_BASE)
        p = rng.choice(EN_PREFIX)
        s = rng.choice(EN_SUFFIX)
        line = tpl.format(t="{t}", insult=insult, insult2=insult2, p=p, suf=s)
    if rng.random() < 0.07:
        line = line.upper()
    if with_gif and rng.random() < 0.25:
        gif = rng.choice(REAL_GIFS)
        # sometimes gif alone, sometimes with text
        if rng.random() < 0.5:
            line = f"{line} {gif}"
        else:
            line = gif
    return line

def write_file(path, generator_func, n, seed, line_prefix=""):
    rng = random.Random(seed)
    t0 = time.time()
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(n):
            line = generator_func(rng)
            if line_prefix:
                # ensure prefix is "# " with space, not glued
                # if line already starts with prefix, don't double
                if not line.startswith(line_prefix):
                    line = f"{line_prefix}{line}"
            f.write(line + "\n")
    sz = os.path.getsize(path) / 1024
    dt = time.time() - t0
    print(f"  {path:35s} {n:>7,} lines  {sz:>7.1f} KB  ({dt:.1f}s)  prefix='{line_prefix}'")

def main():
    short_n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    short_n = max(100, min(short_n, 1000000))
    long_n = short_n * 3  # long is 3x short

    print(f"Generating 2026 packs: short={short_n:,} long={long_n:,}")

    # RO short - only romana, no gif, no > # prefix, BIG text
    write_file("data/spam_ro.txt", lambda rng: gen_ro_line(rng), short_n, seed=101, line_prefix="")

    # EN short - only english + gifs, no > #
    write_file("data/spam_en.txt", lambda rng: gen_en_line(rng, with_gif=True), short_n, seed=202, line_prefix="")

    # RO long - hardcore roast 2026 - WITH "# " prefix at beginning (space not glued)
    write_file("data/longspam_ro.txt", lambda rng: gen_ro_line(rng), long_n, seed=303, line_prefix="# ")

    # EN long + gifs - WITH "# " prefix
    write_file("data/longspam_en.txt", lambda rng: gen_en_line(rng, with_gif=True), long_n, seed=404, line_prefix="# ")

    # MIX spam.txt
    def gen_mix(rng):
        if rng.random() < 0.5:
            return gen_ro_line(rng)
        else:
            return gen_en_line(rng, with_gif=rng.random()<0.3)
    write_file("data/spam.txt", gen_mix, short_n + 1000, seed=505)

    # Legacy lines_ro.txt - same as spam_ro but larger for backward compat
    write_file("data/lines_ro.txt", lambda rng: gen_ro_line(rng), long_n, seed=606)

    # Legacy lines_en.txt
    write_file("data/lines_en.txt", lambda rng: gen_en_line(rng, with_gif=True), long_n, seed=707)

    # lines_default.txt = mix
    write_file("data/lines_default.txt", gen_mix, long_n, seed=808)

    # botjura.txt = RO (legacy default) - keep file, don't rename, just update
    shutil.copyfile("data/lines_ro.txt", "botjura.txt")
    print(f"  {'botjura.txt':35s} copied from lines_ro.txt")

    # stats
    print("\nDone. New packs:")
    for p in ["data/spam.txt","data/spam_ro.txt","data/spam_en.txt","data/longspam_ro.txt","data/longspam_en.txt","data/lines_ro.txt","data/lines_en.txt","data/lines_default.txt","botjura.txt"]:
        if os.path.exists(p):
            sz = os.path.getsize(p)/1024
            with open(p, "r", encoding="utf-8") as fh:
                lc = sum(1 for _ in fh)
            print(f"  {p:35s} {lc:>7,} lines  {sz:>7.1f} KB")

    print("\nNotes:")
    print(" - No > # prefix - each line is BIG text as requested")
    print(" - RO = only romana, EN = only english + gifs")
    print(" - Multi-user: $start @u1 @u2 file  |  $start ionut vasile alex longspam_ro.txt")
    print(" - Panel: 0.0.0.0:3000 (default) - works with preview, not localhost-only")

if __name__ == "__main__":
    main()
