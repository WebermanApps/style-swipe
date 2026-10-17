#!/usr/bin/env python3
"""R86 slug fix (Branding, Oct 17 2026). The R86 split gave some halves the OTHER half's theme in their id/slug
(titles follow the content, ids did not). Unanswered swapped halves get a new id + random-suffix slug named after
their real content; the old id is unlisted (renamed_to) and its page becomes a locked redirect. Answered halves keep
their id/slug (answers stay valid) and only need the right display name.
Tea Blends special case (WellNest 2026-10-17 09:25): the unanswered 'energy-line-line-purposes' half (real Calm +
Digestion cards) is rebuilt as 'Tea Blends: Calm Line & Beauty Line' (Max picked Beauty over Digestion).
Writes pages UNLOCKED into --out (a temp dir) for locking; never into the repo directly.
usage: r86_slug_fix.py --src <unlocked copies dir> --out <temp out dir>"""
import json, glob, os, re, sys, secrets, string, copy, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
args = dict(zip(sys.argv[1::2], sys.argv[2::2])); SRC, OUT = args["--src"], args["--out"]
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(timespec="seconds")
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", " ")).strip("-")
def rnd(n=6): return "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(n))
pages = json.load(open("decks/pages.json"))
answered = {os.path.basename(f) for f in glob.glob("/workspace/ops/submit/inbox/*/*.json")}
halves = {}
for f in sorted(glob.glob("decks/*.json")):
    try: d = json.load(open(f))
    except Exception: continue
    if isinstance(d, dict) and "split_from" in d and not d.get("renamed_to"):
        halves.setdefault(d["split_from"], []).append((os.path.basename(f)[:-5], d))
TEA_OLD = "wellnest-tea-blend-ingredients-energy-line-line-purposes"
TEA_NEW = "wellnest-tea-blend-ingredients-calm-line-beauty-line"
plan, report = [], {"renamed": [], "answered_kept": [], "unclear": []}
for orig, hs in halves.items():
    if len(hs) != 2: continue
    th = [slugify(d.get("title", "").split(":", 1)[-1]) for _, d in hs]
    for i, (did, d) in enumerate(hs):
        st = did[len(orig) + 1:]
        if st == th[i]: continue
        if st != th[1 - i]: report["unclear"].append({"id": did, "title": d.get("title")}); continue
        ans = [a for a in answered if a.startswith(did + "-")]
        if ans: report["answered_kept"].append({"id": did, "title": d.get("title"), "slug": pages.get(did), "submission": ans}); continue
        new = TEA_NEW if did == TEA_OLD else f"{orig}-{th[i]}-deck"
        plan.append((did, new, d))
def tea_pairs(d):
    """Keep the Calm Line + Mood cards, replace the 4 Digestion cards with Beauty Line cards (roselle hero already picked)."""
    src = open("tools/build_wn_tea.py").read(); ns = {"__file__": os.path.abspath("tools/build_wn_tea.py"), "__name__": "wn_tea_lib"}
    exec(src[:src.index('SL = "queue/wn-tea-slugs.json"')], ns); os.chdir(ROOT)
    svg, ACC = ns["svg"], ns["ACC"]
    B = "Beauty Line"
    new = [
     (B, "Beauty Line Colour: Roselle With Butterfly Pea Or Roselle On Its Own?",
      ("Roselle And Butterfly Pea", "Roselle plus a pinch of butterfly pea; the cup turns deep purple.", "Purple cup", "Caffeine free", "img:butterflypea"),
      ("Roselle On Its Own", "Just roselle; a clear ruby-red cup.", "Ruby red", "Caffeine free", "img:roselle")),
     (B, "Beauty Line Bright Note: Kaffir Lime Leaf Or Lemongrass?",
      ("Kaffir Lime Leaf", "Clean citrus scent over the tart roselle.", "Citrus", "Farm grown", "img:kaffir"),
      ("Lemongrass", "Soft lemony lift, already in the Energy Line.", "Light", "Farm grown", "img:lemongrass")),
     (B, "Beauty Line Sweetness: Naturally Tart Or Softened With Dried Longan?",
      ("Naturally Tart", "Roselle as it is: bright, sour and clean.", "Tart", "No sugar", "pk:pouch:band:Beauty Line|Beauty"),
      ("Dried Longan", "A few dried Chiang Mai longans add a soft, honey-like sweetness.", "Sweeter", "Local fruit", "pk:jar:big:Beauty Line|with longan")),
     (B, "Beauty Line Serve: Iced Or Warm Cup?",
      ("Iced", "Brewed strong and poured over ice, bright red.", "Cold", "Afternoon", "img:rosellebrew"),
      ("Warm Cup", "A warm, tart cup any time of day.", "Hot", "Any time", "img:teacup")),
    ]
    keep = [p for p in d["pairs"] if p["group"] != "Digestion Line"]
    tmpl = keep[0]; out = []
    for p in keep: out.append(copy.deepcopy(p))
    FEEL = ["practical", "bold", "calm", "playful", "premium"]
    for gi, (g, ask, a, b) in enumerate(new):
        p = copy.deepcopy(tmpl); p.update(group=g, category=g, ask=ask, purpose="new", retest=False, repeat=False)
        for side, (k, o) in enumerate((("optionA", a), ("optionB", b))):
            oid = "wntbeauty_" + re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            p[k] = {"id": oid, "label": o[0], "desc": o[1], "tags": [FEEL[(gi * 2 + side) % 5]], "feeling": FEEL[(gi * 2 + side) % 5], "notes": True, "share": True,
                    "visual": {"type": "hm", "m": "svg", "svg": svg(g, o[0], o[1], o[2:4], o[4], ACC[(gi + side) % 2])}}
        out.append(p)
    # interleave Beauty cards between Calm cards so the deck alternates lines
    calm, beauty = out[:len(keep)], out[len(keep):]
    mixed = []
    for i in range(max(len(calm), len(beauty))):
        if i < len(calm): mixed.append(calm[i])
        if i < len(beauty): mixed.append(beauty[i])
    assert len(mixed) == 10, len(mixed)
    return mixed
REDIR = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>{title}</title><meta http-equiv="refresh" content="0; url=../{slug}/">
<script>location.replace("../{slug}/"+location.search+location.hash)</script>
<style>body{{font-family:Hind,sans-serif;background:#fff;color:#0A0A0A;margin:40px 20px}}a{{color:#0A0A0A}}</style></head>
<body><p>This deck moved: <a href="../{slug}/">{title}</a>.</p></body></html>
"""
os.makedirs(OUT, exist_ok=True)
for old, new, d in plan:
    oslug = pages[old]; nslug = f"{new}-{rnd()}"
    nd = copy.deepcopy(d); nd["date"] = new
    if old == TEA_OLD:
        nd["pairs"] = tea_pairs(d); nd["title"] = "Tea Blends: Calm Line & Beauty Line"
        nd["groups"] = {}; [nd["groups"].__setitem__(p["group"], nd["groups"].get(p["group"], 0) + 1) for p in nd["pairs"]]
        nd["freshness"] = {"note": "Calm Line + Mood cards reused from wellnest-tea-blend-ingredients; 4 new Beauty Line cards (Oct 17 2026)"}
        nd["health_claims_note"] = "No health claims on cards. 'Beauty Line' / 'Beauty Glow' names imply a cosmetic benefit: check Thai FDA herbal-tea label rules before using on packs."
        nd["generated_at"] = NOW
    for i, p in enumerate(nd["pairs"], 1): p["id"] = f"{new}-{i:02d}"
    nd["renamed_from"] = old; nd["slug_fix"] = f"R86 slug fix {NOW}: id/slug now name this half's real content"
    nd.pop("unlisted", None)
    sib = d.get("split_sibling")
    json.dump(nd, open(f"decks/{new}.json", "w"), indent=1, ensure_ascii=False)
    d["unlisted"] = True; d["renamed_to"] = new; d["unlisted_note"] = f"R86 slug fix {NOW}: id named the other half's theme; replaced by {new} (page redirects)"
    json.dump(d, open(f"decks/{old}.json", "w"), indent=1, ensure_ascii=False)
    pages[new] = nslug
    page = open(os.path.join(SRC, oslug, "index.html")).read()
    assert f'"{old}"' in page, old
    page = page.replace(f'"{old}"', f'"{new}"')
    os.makedirs(os.path.join(OUT, nslug), exist_ok=True); open(os.path.join(OUT, nslug, "index.html"), "w").write(page)
    os.makedirs(os.path.join(OUT, oslug), exist_ok=True); open(os.path.join(OUT, oslug, "index.html"), "w").write(REDIR.format(title=nd["title"], slug=nslug))
    report["renamed"].append({"old": old, "old_slug": oslug, "new": new, "new_slug": nslug, "title": nd["title"], "total": len(nd["pairs"]),
                              "url": f"https://webermanapps.github.io/style-swipe/{nslug}/", "old_url": f"https://webermanapps.github.io/style-swipe/{oslug}/"})
# keep sibling pointers right
ren = {r["old"]: r["new"] for r in report["renamed"]}
for f in glob.glob("decks/*.json"):
    try: d = json.load(open(f))
    except Exception: continue
    if isinstance(d, dict) and d.get("split_sibling") in ren and not d.get("renamed_to"):
        d["split_sibling"] = ren[d["split_sibling"]]; json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
    if isinstance(d, dict) and isinstance(d.get("split_into"), list) and any(x in ren for x in d["split_into"]):
        d["split_into"] = [ren.get(x, x) for x in d["split_into"]]; json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
json.dump(report, open("queue/r86-slug-fix.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False))
