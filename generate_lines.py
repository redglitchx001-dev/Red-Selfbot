# -*- coding: utf-8 -*-
"""Fast generator of insult line files for $start.
Usage:
    python generate_lines.py            # 20k lines per file (default)
    python generate_lines.py 50000      # 50k lines per file (~4MB each)
Files are written to data/lines_*.txt; botjura.txt is rebuilt as RO.
"""
import os, random, sys, time

os.makedirs("data", exist_ok=True)

EN_SWEARS = ["fuck","shit","bitch","asshole","dick","cock","pussy","cunt","motherfucker",
"dumbass","jackass","dipshit","fuckface","shithead","cocksucker","asswipe","douchebag",
"fucktard","retard","moron","idiot","scumbag","son of a bitch","bastard","prick","twat",
"dickhead","braindead retard","dumb fuck","stupid cunt","fat fuck","ugly bastard",
"smelly twat","inbred","troglodyte","smoothbrain","cretin","imbecile","waste of space",
"human garbage","potato brain","no-life loser","keyboard warrior","discord mod","clown",
"pathetic worm","garbage human","walking L","absolute donkey","toothless wonder"]

EN_INSULTS = ["go fuck yourself","suck my dick","eat shit","kill yourself","get a life",
"shut the fuck up","stfu","nobody likes you","you are a waste of oxygen",
"i fucked your mom last night","your dad left for milk and never came back",
"your family tree is a circle","you were a mistake","go play in traffic",
"choke on a bag of dicks","drink bleach","step on a lego barefoot","get hit by a bus",
"delete your account","uninstall the internet","you look like a dropped pie",
"you have the charisma of a wet paper bag","a rock has more brain cells than you",
"your mom should have swallowed","i'd call you a tool but tools are useful",
"you have the IQ of a toaster","your reflection leaves you on read",
"go crawl back into the sewer","nobody would notice if you vanished",
"you'd lose a fight with a houseplant","your opinion is worthless",
"you reek of failure","you couldn't pour water out of a boot with instructions on the heel",
"your parents lied when they said you were special","you're what happens when cousins marry",
"cry harder you pathetic worm","cope seethe dilate","touch grass basement dweller",
"get rekt","ratio plus L","mad cuz bad","imagine being this mad",
"go kys","eat a bag of dicks","choke on a cactus","seethe more",
"your entire bloodline is cursed","i wouldn't piss on you if you were on fire",
"you're built like a boiled potato","go back to tiktok","type less garbage",
"you dress like a discount store mannequin","nobody cares about your opinion",
"your mic sounds like a tin can tied to a dog"]

EN_PREFIX = ["yo","hey","bro","bruh","lmao","lmfao","lol","damn","holy shit",
"fr","ngl","buddy","pal","son","kid","oi","listen up","ayo","broski"]

EN_SUFFIX = ["you dumb fuck","lmao","fr fr","on god","no cap","deadass",
"get rekt","ratio + L","cope harder","seethe more","mad cuz bad",
"lmfaoooooo","cry about it","stay mad","touch grass","clown",
"penisible","absolute donkey","waste of skin"]

RO_SWEARS = ["prost","tâmpit","idiot","cretin","imbecil","dobitoc","nenorocit",
"bou","țăran","maimuță","măgar","porc","javră","căcat","rahat","curvă","târfă",
"pizda mă-tii","futu-ți morții mă-tii","băga-mi-aș pula în mă-ta","suge-mi pula",
"fută-te-n cur","handicapat","gogoman","bleg","fraier","găozar","poponar",
"muist","labagiu","fătălău","papagal","maimuțoi","cap de pulă","cap de căcat",
"pizdă","pulă","muie","sclav","javră ordinară","curva mă-tii","tactu la bețiv",
"găinar","parazit","boschetar","căcăcios","ratat","penibil","țigan împuțit"]

RO_INSULTS = ["du-te-n pula mea","suge pula","futu-ți morții","băga-mi-aș pula în mă-ta",
"te fut în gură","morții mă-tii de handicapat","mă piș pe tine și pe familia ta",
"îți dau în cap de nu te vezi","te bat de te caci pe tine","ești un nimic",
"tactu e un bețiv și mă-ta o curvă","ai creierul cât un bob de mazăre",
"ești un ratat fără viață","du-te de-aici boule","taci-n gură",
"te-a fătat mă-ta pe un câmp de porumb","ești urât ca dracu","puți ca un canal",
"n-ai nici două clase","plângi ca o fetiță","ești un sclav",
"mai taci dracu din gură","futu-ți crucea mă-tii de cretin","ba handicapatule",
"ba prostule","ba căcatule","ba javră","ești un clovn","viața ta e un dezastru",
"n-ai prieteni","mai bine te sinucideai","pune mâna și învață",
"mi-e scârbă de tine","te-a făcut mă-ta cu curul","du-te dracu",
"la mine nu vorbi așa că-ți dau una","mă piș pe morții tăi",
"băga-mi-aș picioarele-n curu tău","te căcat pe tine de frică",
"coaiele mă-tii","futu-ți dumnezeii","taci în pula mea"]

RO_PREFIX = ["bă","auzi","hei","frate","băi","sclavule","boule","tâmpitule",
"cretinule","nenorocitule","javră","prostule","băi băiatule","mă"]

RO_SUFFIX = ["boule","tâmpitule","cretinule","morții mă-tii","futu-ți morții",
"taci în gură","penibilule","ratatule","javră ordinară","muistule",
"labagiule","poponarule","găozarule"]

TEMPLATES = [
    "{p} {t} {i} {s}",
    "{t} {i}",
    "{t} {w} {s}",
    "{i} {t} {w}",
    "{p} {t} {w}",
    "{t} {i} and die mad about it",
    "{t} go {i}",
    "who asked {t} you {w}",
    "cry more {t} you {w}",
    "seethe {t} you {w}",
    "cope harder {t} you {w}",
    "{t} your entire existence is a joke",
    "get rekt {t} you {w}",
    "{t} {i} and stay mad",
    "lmao {t} {i}",
    "lol {t} you {w}",
    "{t} {w} {s}",
    "{p} {t} is the biggest {w} alive",
    "{p} {t}",
    "{i}",
    "{w}!",
]


def write_lang(path, swears, insults, prefixes, suffixes, seed, n, seed_legacy=None):
    """Write n lines to path. Fast: O(n) no set dedupe."""
    rng = random.Random(seed)
    t0 = time.time()
    # Pre-load legacy lines (botjura.txt) for RO nostalgia
    legacy = []
    if seed_legacy and os.path.exists(seed_legacy):
        try:
            with open(seed_legacy, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    l = line.rstrip("\r\n").strip()
                    if l and len(l) < 280:
                        legacy.append(l)
        except Exception:
            pass
    with open(path, "w", encoding="utf-8") as f:
        written = 0
        # write legacy first (up to 5% of total)
        rng.shuffle(legacy)
        for l in legacy[:max(100, n // 20)]:
            f.write(l + "\n"); written += 1
        while written < n:
            tpl = rng.choice(TEMPLATES)
            line = tpl.format(
                p=rng.choice(prefixes), t="{t}",
                i=rng.choice(insults), w=rng.choice(swears), s=rng.choice(suffixes))
            if rng.random() < 0.3:
                line = line.replace("{t} ", "").replace(" {t}", "").replace("{t}", "")
            line = line.strip(" ,.!?")
            if line and len(line) < 280:
                f.write(line + "\n"); written += 1
            # Occasional raw insults
            if rng.random() < 0.12:
                f.write(rng.choice(insults) + "\n"); written += 1
            if rng.random() < 0.07:
                f.write(rng.choice(swears).upper() + ("!" if rng.random()<0.5 else "") + "\n"); written += 1
    sz = os.path.getsize(path) / (1024*1024)
    lc = sum(1 for _ in open(path, "r", encoding="utf-8"))
    dt = time.time() - t0
    print(f"  {path:30s} {lc:>8,} lines  {sz:.1f} MB  ({dt:.1f}s)")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    n = max(500, min(n, 1000000))
    print(f"Generating {n:,} lines per file...")
    # write legacy RO lines loaded from original botjura.txt - only if it's NOT already a generated one.
    # We save the original first if needed
    orig = "botjura.txt"
    write_lang("data/lines_en.txt", EN_SWEARS, EN_INSULTS, EN_PREFIX, EN_SUFFIX, seed=1, n=n)
    write_lang("data/lines_ro.txt", RO_SWEARS, RO_INSULTS, RO_PREFIX, RO_SUFFIX, seed=2, n=n, seed_legacy=orig)
    # default = mixed
    import random as _r
    _r.seed(0)
    with open("data/lines_default.txt", "w", encoding="utf-8") as f:
        # Sample en and ro interspersed
        with open("data/lines_en.txt", "r", encoding="utf-8") as fe, \
             open("data/lines_ro.txt", "r", encoding="utf-8") as fr:
            en = [l for l in fe]
            ro = [l for l in fr]
        _r.shuffle(en); _r.shuffle(ro)
        for i in range(min(n, len(en) + len(ro))):
            f.write((en[i] if i % 2 == 0 else ro[i]))
    # botjura.txt = RO (default behavior for $start without file arg)
    import shutil
    shutil.copyfile("data/lines_ro.txt", "botjura.txt")
    # stats
    for p in ["data/lines_en.txt","data/lines_ro.txt","data/lines_default.txt","botjura.txt"]:
        sz = os.path.getsize(p)/(1024*1024)
        lc = sum(1 for _ in open(p, "r", encoding="utf-8"))
        print(f"  {p:30s} {lc:>8,} lines  {sz:.1f} MB")


if __name__ == "__main__":
    main()
