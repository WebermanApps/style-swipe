#!/usr/bin/env python3
"""Restyle non-done WellNest deck card art to the standard deck look (Max Oct 15 2026 13:03/13:04 ICT): white + light beige, Khand/Hind,
dashboard tokens (kit/dash-theme.css). Pairs whose question IS about colour/font/logo keep their option colours/fonts (answer content).
Only svg strings in decks/<id>.json for ids not done in /workspace/wellnest/deck-queue.json. Idempotent."""
import json, re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
MAP = {"#ECC978": "#171717", "#DABC76": "#171717", "#B8902F": "#171717", "#C1502E": "#171717", "#05668D": "#171717", "#0B6E4F": "#171717",
       "#D7A363": "#737373", "#C9A27A": "#737373", "#D4A017": "#737373", "#525252": "#737373", "#8A8580": "#737373",
       "#D6D0C6": "#e3ddd2", "#E5E0D8": "#e3ddd2", "#FBF8F1": "#FAF6EE", "#F7EEDB": "#FAF6EE"}
FONTS = {"'Cormorant Garamond', Georgia, serif": "Khand, Hind, sans-serif", "'DM Sans', Hind, sans-serif": "Hind, sans-serif"}
KEEP = re.compile(r"colou?r|font|gold|peach|green|cormorant|dm sans|sarabun|thai text|palette|logo|serif|italic|typeface", re.I)
def fix(s):
    for a, b in FONTS.items(): s = s.replace(a, b)
    return re.sub(r"#[0-9A-Fa-f]{6}\b", lambda m: MAP.get(m.group(0).upper(), m.group(0)), s)
def walk(o):
    if isinstance(o, dict): return {k: (fix(v) if k == "svg" and isinstance(v, str) else walk(v)) for k, v in o.items()}
    if isinstance(o, list): return [walk(x) for x in o]
    return o
Q = json.load(open("/workspace/wellnest/deck-queue.json"))
ids = [x["deckId"] for x in Q["decks"] if x.get("status") != "done"]
n = kept = 0
for i in ids:
    f = f"decks/{i}.json"; raw = open(f).read(); d = json.loads(raw)
    for k, p in enumerate(d["pairs"]):
        if KEEP.search(p.get("ask", "")): kept += 1; continue
        d["pairs"][k] = walk(p)
    out = json.dumps(d, indent=1, ensure_ascii=False)
    if out.strip() != raw.strip(): open(f, "w").write(out); n += 1
print(len(ids), "non-done WellNest decks,", n, "changed,", kept, "colour/font/logo pairs kept as-is")
