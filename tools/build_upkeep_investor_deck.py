#!/usr/bin/env python3
"""UpKeep (Smart Upkeep) Investor Pitch Deck (Oct 16 2026): 20 text this-or-that pairs with drawn SVG slide thumbnails (no images).
Same pattern as build_upkeep_forecasting.py; square corners; mw-chat cc11 to UpKeep; submit_agent upkeep.
Content: tools/upkeep_investor_deck_content.py. Slug kept in queue/upkeep-investor-slugs.json."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish, shareic, wrap
from draft_svg import t, rect, TERRA, LAGOON, JUNGLE, SAFFRON
from upkeep_investor_deck_content import DECKS
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
INK, MUTE, LINE, BEI, BEI2 = "#0A0A0A", "#525252", "#e3ddd2", "#FAF6EE", "#e3ddd2"
def thumb(kind, a):
    X, Y, W, H = 16, 40, 208, 104
    s = rect(X, Y, W, H, BEI, LINE) + rect(X + 10, Y + 10, 70, 5, INK)
    cx, cy = X + W / 2, Y + H / 2 + 6
    L = lambda x1, y1, x2, y2, c=INK, w=2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
    P = lambda pts, c=a, w=2.5: f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    if kind in ("bars",):
        for i, h in enumerate([20, 32, 44, 60]): s += rect(X + 60 + i * 24, Y + 92 - h, 16, h, a if i == 3 else BEI2)
    elif kind == "line": s += P(f"{X+30},{Y+88} {X+70},{Y+74} {X+110},{Y+64} {X+150},{Y+44} {X+185},{Y+30}") + L(X+30, Y+92, X+190, Y+92, MUTE, 1)
    elif kind == "lines3":
        for d, c in ((-14, BEI2), (0, a), (14, MUTE)): s += P(f"{X+30},{Y+80} {X+100},{Y+66-d/2} {X+185},{Y+50-d}", c)
    elif kind == "pie": s += f'<circle cx="{cx}" cy="{cy}" r="34" fill="{BEI2}"/><path d="M{cx},{cy} L{cx},{cy-34} A34,34 0 0,1 {cx+34},{cy} Z" fill="{a}"/><path d="M{cx},{cy} L{cx+34},{cy} A34,34 0 0,1 {cx},{cy+34} Z" fill="{MUTE}"/>'
    elif kind == "table":
        for r in range(4):
            for c in range(3): s += rect(X + 30 + c * 50, Y + 26 + r * 17, 46, 13, a if (r == 0) else "#FFFFFF", LINE)
    elif kind == "quad": s += L(cx, Y + 22, cx, Y + 98) + L(X + 40, cy, X + 168, cy) + f'<circle cx="{cx+38}" cy="{cy-24}" r="7" fill="{a}"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{MUTE}"/>' for x, y in ((cx-40, cy+18), (cx-22, cy-20), (cx+26, cy+24)))
    elif kind == "circles": s += "".join(f'<circle cx="{cx}" cy="{cy+30-r}" r="{r}" fill="{c}"/>' for r, c in ((36, BEI2), (24, MUTE), (12, a)))
    elif kind in ("grid", "map"):
        for r in range(4):
            for c in range(7): s += rect(X + 40 + c * 19, Y + 24 + r * 19, 15, 15, a if (r * 7 + c) % 5 < (3 if kind == "grid" else 2) else "#FFFFFF", LINE)
    elif kind == "list":
        for r in range(4): s += rect(X + 30, Y + 28 + r * 17, 8, 8, a) + rect(X + 46, Y + 30 + r * 17, 110 - r * 12, 5, MUTE)
    elif kind == "funnel": s += f'<polygon points="{X+50},{Y+26} {X+158},{Y+26} {X+122},{Y+94} {X+86},{Y+94}" fill="{a}"/>' + L(X+62, Y+50, X+146, Y+50, "#FFFFFF") + L(X+74, Y+72, X+134, Y+72, "#FFFFFF")
    elif kind == "shield": s += f'<path d="M{cx},{Y+24} L{cx+30},{Y+34} L{cx+30},{Y+62} Q{cx+30},{Y+86} {cx},{Y+96} Q{cx-30},{Y+86} {cx-30},{Y+62} L{cx-30},{Y+34} Z" fill="{a}"/>'
    elif kind == "team":
        for i in range(3): s += f'<circle cx="{cx-44+i*44}" cy="{cy-8}" r="13" fill="{a if i==1 else MUTE}"/>' + rect(cx - 60 + i * 44, cy + 12, 32, 18, a if i == 1 else MUTE)
    elif kind in ("phone", "phones"):
        for i in range(1 if kind == "phone" else 3):
            x = cx - 18 if kind == "phone" else X + 44 + i * 44
            s += rect(x, Y + 22, 36, 74, "#FFFFFF", INK, 0, 2) + rect(x + 6, Y + 30, 24, 14, a) + rect(x + 6, Y + 50, 24, 4, MUTE) + rect(x + 6, Y + 58, 18, 4, MUTE)
    elif kind == "card": s += rect(cx - 50, Y + 32, 100, 60, a) + rect(cx - 40, Y + 46, 30, 8, "#FFFFFF") + rect(cx - 40, Y + 72, 60, 5, "#FFFFFF")
    elif kind == "flow":
        for i in range(4): s += f'<circle cx="{X+40+i*42}" cy="{cy}" r="11" fill="{a if i in (0,3) else MUTE}"/>' + (L(X + 51 + i * 42, cy, X + 71 + i * 42, cy) if i < 3 else "")
    elif kind == "steps":
        for i in range(4): s += rect(X + 40 + i * 34, Y + 90 - (i + 1) * 15, 30, (i + 1) * 15, a if i == 3 else BEI2)
    elif kind == "clock": s += f'<circle cx="{cx}" cy="{cy}" r="32" fill="#FFFFFF" stroke="{a}" stroke-width="4"/>' + L(cx, cy, cx, cy - 22) + L(cx, cy, cx + 16, cy)
    elif kind == "story":
        s += f'<polygon points="{X+40},{Y+70} {X+70},{Y+44} {X+100},{Y+70}" fill="{a}"/>' + rect(X + 46, Y + 70, 48, 26, a) + rect(X + 64, Y + 80, 12, 16, "#FFFFFF")
        for r in range(3): s += rect(X + 116, Y + 46 + r * 14, 70 - r * 14, 5, MUTE)
    elif kind == "vision": s += P(f"{X+30},{Y+92} {X+100},{Y+60} {X+180},{Y+26}", a, 4) + f'<polygon points="{X+180},{Y+26} {X+166},{Y+28} {X+174},{Y+40}" fill="{a}"/>'
    elif kind in ("stack", "stack2"):
        n = 3 if kind == "stack" else 6
        for i in range(n): s += rect(cx - 50 + i * 8 - n * 3, Y + 26 + i * 8, 80, 50, "#FFFFFF" if i < n - 1 else a, INK)
    elif kind == "photo": s += rect(X + 30, Y + 24, 148, 70, BEI2) + f'<polygon points="{X+30},{Y+94} {X+80},{Y+50} {X+120},{Y+94}" fill="{a}"/><circle cx="{X+150}" cy="{Y+44}" r="9" fill="{MUTE}"/>'
    elif kind == "screen": s += rect(cx - 56, Y + 24, 112, 62, "#FFFFFF", INK, 0, 2) + rect(cx - 40, Y + 40, 80, 30, a) + L(cx, Y + 86, cx, Y + 98) + L(cx - 20, Y + 98, cx + 20, Y + 98)
    elif kind == "doc":
        s += rect(cx - 32, Y + 22, 64, 76, "#FFFFFF", INK, 0, 2)
        for r in range(5): s += rect(cx - 22, Y + 34 + r * 11, 44 - (r % 2) * 12, 4, a if r == 0 else MUTE)
    elif kind == "quote": s += t(cx - 40, cy + 26, "\u201c", 72, a, "khand", 700) + rect(cx + 2, cy - 14, 64, 5, MUTE) + rect(cx + 2, cy - 2, 52, 5, MUTE) + rect(cx + 2, cy + 10, 58, 5, MUTE)
    return s
def svg(group, label, desc, facts, kind, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    s += thumb(kind, acc)
    y = 174
    for l in wrap(label, 18)[:2]: s += t(16, y, l, 24, INK, "khand"); y += 25
    for l in wrap(desc, 34)[:3]: s += t(16, y, l, 12.5, MUTE); y += 16
    y = max(y + 2, 250); x = 16
    for f in facts[:2]:
        w = min(104, 18 + len(f) * 6.2); s += rect(x, y, w, 22, BEI, LINE) + t(x + 8, y + 15, f, 11, INK, "hind", 600); x += w + 6
    s += t(120, 292, "Built by Max Weberman", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>'
SL = "queue/upkeep-investor-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
for n, key in enumerate(DECKS):
    NAME, ABOUT, PAIRS = DECKS[key]; did = f"upkeep-{key}-deck"
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}</style>
    '''
    acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
    pairs, O, add = kdeck("upinv_", "UpKeep")
    for gi, (g, ask, a, b) in enumerate(PAIRS):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], acc[(gi + side * 2) % 4])))
        add(g, g, opts[0], opts[1], ask)
    publish(did, NAME, "UpKeep", pairs, {"brands": [ABOUT, "Smart Upkeep investor pitch deck."],
            "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "upkeep-investor-pitch",
            "deck_size": 20, "board": "upkeep", "audience": "Max"}, seed=6500 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "upkeep-" + key + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
