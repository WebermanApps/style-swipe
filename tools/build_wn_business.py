#!/usr/bin/env python3
"""WellNest row two 'For P'Thom And Max' (Max, Oct 15 2026 12:43 ICT): 10 ready 20-pair business strategy decks
(5 shelf + 5 refill pool). Content: tools/wn_business_content.py. Same page pattern as build_wn_series.py
(white page + beige accents, wn-deck-done on real submit, Back -> wellnest-dashboard/?done=<deckId>), team_kit.publish (Notes + Share on),
Khand/Hind, submit_agent wellnest. usage: build_wn_business.py [key ...]  -> prints JSON lines {deckId,name,url}"""
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from draft_svg import t, rect, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import shareic, wrap
from wn_business_content import DECKS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
BG, INK, MUTE, LINE = "#FFFFFF", "#0A0A0A", "#525252", "#E5E0D8"
SL = "queue/wn-business-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
def svg(group, label, desc, facts, acc):
    s = rect(0, 0, 240, 300, BG) + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    y = 70
    for l in wrap(label, 15)[:3]: s += t(16, y, l, 28, INK, "khand"); y += 30
    y += 4; s += rect(16, y, 36, 3, acc, "none", 1.5); y += 22
    for l in wrap(desc, 28)[:3]: s += t(16, y, l, 14, MUTE); y += 18
    y = max(y + 6, 200)
    for f in facts[:2]:
        s += rect(16, y, 208, 32, "#FFFFFF", LINE, 8) + f'<circle cx="30" cy="{y+16}" r="4" fill="{acc}"/>' + t(42, y + 21, f, 13.5, INK, "hind", 600); y += 36
    s += t(120, 290, "Built by Max Weberman", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="240" height="300" rx="14"/></clipPath><g clip-path="url(#c)">{s}</g><rect x=".5" y=".5" width="239" height="299" rx="14" fill="none" stroke="#D6D0C6"/></svg>'
def page(did, slug):
    src = open("tools/build_wn_series.py").read(); i = src.index("HEAD = f'''"); j = src.index("'''", i + 12)
    HEAD = eval("f'''" + src[i + 11:j] + "'''", {"did": did})
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s)
out = []
for n, D in enumerate(DECKS):
    if sys.argv[1:] and D["key"] not in sys.argv[1:]: continue
    did = "wellnest-business-" + D["key"]; acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
    pairs, O, add = kdeck("wb" + re.sub("[^a-z]", "", D["key"])[:8] + "_", "WellNest")
    for gi, (g, ask, a, b) in enumerate(D["pairs"]):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:], acc[(gi + side * 2) % 4])))
        add(g, g, opts[0], opts[1], ask)
    from wn_guard import blocked as _wnb, RULE as _WNR  # no dashboard layout / deck-building pairs
    _bad = [p["ask"] for p in pairs if _wnb(p, False)]
    if _bad: sys.exit("WellNest guard (" + _WNR + ") blocks: " + "; ".join(_bad))
    publish(did, D["name"], "WellNest", pairs, {"brands": [D["about"], "Business strategy deck for P'Thom and Max (row two). No branding, visual style or dashboard topics."],
            "submit_agent": "wellnest", "submit_to": "WellNest Agent", "deck_size": 20, "row": "business", "audience": "P'Thom and Max",
            "sources": {"queue": "/workspace/wellnest/deck-queue.json"}}, seed=4100 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20
    if did not in slugs: slugs[did] = "wellnest-biz-" + D["key"] + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    page(did, slugs[did])
    print(json.dumps({"deckId": did, "name": D["name"], "url": f"https://webermanapps.github.io/style-swipe/{slugs[did]}/", "slug": slugs[did]}))
