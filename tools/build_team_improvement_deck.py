#!/usr/bin/env python3
"""Branding: permanent Team Improvement Deck (R75, Oct 16 2026). 20 this-or-that pairs, drawn SVG pictures.
SVGs use viewBox + width:100%;height:auto (no max-height:100% collapse); page CSS overrides the template's max-height rule so pictures show on desktop and phone.
Square corners; mw-chat cc11 to Branding Agent; submit_agent branding. Content: tools/team_improvement_deck_content.py."""
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish, shareic, wrap
from draft_svg import t, rect, TERRA, LAGOON, JUNGLE, SAFFRON
from team_improvement_deck_content import DECKS
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
INK, MUTE, LINE, BEI, W_ = "#0A0A0A", "#525252", "#e3ddd2", "#FAF6EE", "#FFFFFF"
X, Y, W, H = 16, 40, 208, 104
def L(x1, y1, x2, y2, c=INK, w=2): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def bars(x, y, n, w, c=MUTE, gap=10):
    return "".join(rect(x, y + i * gap, w - (i % 2) * w * .3, 4, c) for i in range(n))
def icon(body, a):
    # agent-icon line style: 48x48 grid, stroke #2B2B2B 2, one accent fill; scaled into the panel
    return (f'<g transform="translate({X+W/2-42},{Y+8}) scale(1.75)" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            + body.replace("ACC", a) + '</g>')
def phone(x, y, a, inner):
    return rect(x, y, 50, 92, W_, INK, 0, 2) + inner
def thumb(k, a):
    s = rect(X, Y, W, H, BEI, LINE); cx, cy = X + W / 2, Y + H / 2
    if k == "sumline": s += rect(X+20, Y+20, 168, 64, W_, LINE) + rect(X+30, Y+30, 60, 6, a) + bars(X+30, Y+48, 2, 140)
    elif k == "cards3":
        for i in range(3): s += rect(X+14+i*62, Y+20, 56, 64, W_, LINE) + rect(X+20+i*62, Y+28, 30, 6, a) + bars(X+20+i*62, Y+44, 3, 42)
    elif k == "latebadge": s += rect(X+20, Y+24, 168, 56, W_, LINE) + bars(X+30, Y+36, 3, 90) + rect(X+134, Y+32, 44, 18, a) + t(X+156, Y+45, "LATE", 10, W_, "hind", 700, "middle")
    elif k == "quiet": s += rect(X+20, Y+24, 168, 56, W_, LINE) + bars(X+30, Y+36, 3, 120)
    elif k == "oneline": s += rect(X+20, Y+38, 168, 28, W_, LINE) + f'<circle cx="{X+36}" cy="{Y+52}" r="6" fill="{a}"/>' + rect(X+50, Y+50, 120, 5, MUTE)
    elif k == "dropdown": s += rect(X+20, Y+16, 168, 26, W_, LINE) + f'<circle cx="{X+36}" cy="{Y+29}" r="6" fill="{a}"/>' + rect(X+50, Y+27, 100, 5, MUTE) + f'<polyline points="{X+168},{Y+25} {X+174},{Y+32} {X+180},{Y+25}" fill="none" stroke="{INK}" stroke-width="2"/>' + rect(X+20, Y+44, 168, 44, W_, LINE) + bars(X+32, Y+54, 3, 130, LINE)
    elif k == "chat":
        for i, (x, w, me) in enumerate(((X+20, 110, 0), (X+78, 110, 1), (X+20, 90, 0), (X+98, 90, 1))): s += rect(x, Y+12+i*21, w, 16, a if me else W_, LINE)
    elif k == "deckstack":
        for i in range(4): s += rect(cx-46+i*6, Y+14+i*6, 80, 64, W_ if i < 3 else a, INK)
        s += rect(cx-24, Y+52, 40, 5, W_) + rect(cx-24, Y+62, 28, 5, W_)
    elif k == "bell": s += f'<path d="M{cx-22},{cy+18} Q{cx-18},{cy+12} {cx-18},{cy-4} Q{cx-18},{cy-28} {cx},{cy-28} Q{cx+18},{cy-28} {cx+18},{cy-4} Q{cx+18},{cy+12} {cx+22},{cy+18} Z" fill="{W_}" stroke="{INK}" stroke-width="2.5"/>' + f'<circle cx="{cx}" cy="{cy+26}" r="5" fill="{INK}"/><circle cx="{cx+20}" cy="{cy-24}" r="9" fill="{a}"/>'
    elif k == "digest": s += rect(cx-50, Y+14, 100, 76, W_, INK, 0, 2) + rect(cx-40, Y+24, 50, 7, a) + "".join(rect(cx-40, Y+40+i*12, 8, 8, a) + rect(cx-26, Y+42+i*12, 60, 4, MUTE) for i in range(4))
    elif k == "headcount": s += rect(X+10, Y+14, 188, 26, W_, LINE) + rect(X+18, Y+23, 60, 7, INK) + f'<circle cx="{X+182}" cy="{Y+27}" r="9" fill="{a}"/>' + t(X+182, Y+31, "3", 11, W_, "hind", 700, "middle") + bars(X+18, Y+52, 4, 170, LINE)
    elif k == "section": s += rect(X+10, Y+10, 188, 18, W_, LINE) + rect(X+10, Y+34, 188, 54, W_, a, 0, 2) + rect(X+20, Y+42, 70, 6, a) + bars(X+20, Y+56, 3, 150)
    elif k == "reask": s += rect(X+20, Y+20, 70, 64, W_, LINE) + bars(X+28, Y+34, 3, 50, LINE) + f'<path d="M{X+100},{Y+52} Q{cx+4},{Y+20} {X+124},{Y+52}" fill="none" stroke="{a}" stroke-width="3"/><polygon points="{X+124},{Y+52} {X+116},{Y+44} {X+130},{Y+42}" fill="{a}"/>' + rect(X+118, Y+20, 70, 64, W_, a, 0, 2) + bars(X+126, Y+34, 3, 50)
    elif k == "drop": s += rect(cx-35, Y+20, 70, 64, W_, LINE) + bars(cx-27, Y+34, 3, 50, LINE) + L(cx-30, Y+24, cx+30, Y+80, a, 4) + L(cx+30, Y+24, cx-30, Y+80, a, 4)
    elif k == "ic_pencil": s += icon('<path d="M10 38 L34 14 L38 18 L14 42 L8 44 Z" fill="ACC"/><path d="M30 18 L34 22"/><rect x="18" y="6" width="8" height="34" transform="rotate(45 22 23)"/><path d="M14 18 L17 21 M18 14 L21 17 M22 10 L25 13"/>', a)
    elif k == "ic_house": s += icon('<path d="M8 40 H40 M8 30 H40 M8 20 H40 M16 8 V40 M32 8 V40" stroke="#e3ddd2" stroke-width="1.5"/><path d="M12 40 V24 L24 12 L36 24 V40 Z"/><rect x="21" y="30" width="6" height="10" fill="ACC" stroke="none"/>', a)
    elif k == "ic_roll": s += icon('<path d="M10 12 H34 V38 H10 Z"/><circle cx="36" cy="14" r="5" fill="ACC" stroke="none"/><path d="M34 14 A5 5 0 1 1 40 14 V36 A4 4 0 0 1 34 38"/><path d="M15 20 H28 M15 26 H24 V33 M15 33 H29"/>', a)
    elif k == "ic_compass": s += icon('<path d="M8 40 H40 L8 12 Z" fill="ACC" stroke="none" opacity=".35"/><path d="M8 40 H40 L8 12 Z"/><circle cx="26" cy="8" r="3"/><path d="M26 11 L18 34 M26 11 L34 34"/><path d="M21 26 Q26 29 31 26"/>', a)
    elif k == "carousel":
        for i in range(3): x = X+8+i*72; s += rect(x, Y+16, 64, 58, W_, LINE) + rect(x+4, Y+20, 56, 34, a if i == 1 else LINE) + rect(x+4, Y+60, 40, 5, MUTE)
        s += "".join(f'<circle cx="{cx-12+i*12}" cy="{Y+88}" r="3.5" fill="{INK if i==1 else LINE}"/>' for i in range(3))
    elif k == "grid":
        for r in range(2):
            for c in range(4): x, y = X+14+c*46, Y+12+r*42; s += rect(x, y, 40, 38, W_, LINE) + rect(x+3, y+3, 34, 22, a if (r+c) % 3 == 0 else LINE) + rect(x+3, y+29, 24, 4, MUTE)
    elif k == "bigpic": s += rect(cx-60, Y+10, 120, 84, W_, LINE) + rect(cx-54, Y+16, 108, 56, a) + f'<polygon points="{cx-54},{Y+72} {cx-20},{Y+40} {cx+10},{Y+72}" fill="{W_}" opacity=".5"/>' + rect(cx-54, Y+80, 70, 6, INK)
    elif k == "picbtn": s += rect(cx-60, Y+6, 120, 92, W_, LINE) + rect(cx-54, Y+12, 108, 46, a) + rect(cx-54, Y+62, 60, 5, INK) + rect(cx-54, Y+74, 50, 16, INK) + t(cx-29, Y+85, "APPROVE", 7.5, W_, "hind", 700, "middle") + rect(cx+2, Y+74, 52, 16, W_, INK) + t(cx+28, Y+85, "NOT NOW", 7.5, INK, "hind", 700, "middle")
    elif k == "fullpic": s += rect(X+10, Y+8, 188, 88, a) + f'<polygon points="{X+10},{Y+96} {X+70},{Y+40} {X+120},{Y+96}" fill="{W_}" opacity=".45"/><circle cx="{X+160}" cy="{Y+32}" r="10" fill="{W_}" opacity=".7"/>'
    elif k == "caption": s += rect(X+10, Y+8, 188, 58, a) + f'<polygon points="{X+10},{Y+66} {X+60},{Y+30} {X+104},{Y+66}" fill="{W_}" opacity=".45"/>' + rect(X+10, Y+66, 188, 30, W_, LINE) + rect(X+20, Y+74, 80, 6, INK) + rect(X+20, Y+86, 120, 4, MUTE)
    elif k == "list":
        for i in range(4): s += f'<polyline points="{X+30},{Y+24+i*18} {X+34},{Y+28+i*18} {X+42},{Y+19+i*18}" fill="none" stroke="{a}" stroke-width="2.5"/>' + rect(X+52, Y+21+i*18, 120-i*14, 5, MUTE)
    elif k == "beforeafter": s += rect(X+12, Y+14, 86, 64, W_, LINE) + bars(X+20, Y+26, 4, 60, LINE) + rect(X+110, Y+14, 86, 64, W_, a, 0, 2) + rect(X+118, Y+22, 70, 22, a) + bars(X+118, Y+52, 2, 60) + t(X+55, Y+94, "BEFORE", 9, MUTE, "hind", 600, "middle") + t(X+153, Y+94, "AFTER", 9, a, "hind", 700, "middle")
    elif k in ("shareh", "sharef"):
        s += rect(cx-40, Y+6, 80, 94, W_, INK, 0, 2) + rect(cx-34, Y+12, 68, 14, LINE) + bars(cx-30, Y+34, 4, 60, LINE)
        s += (shareic(cx+20, Y+13, a, 12) if k == "shareh" else rect(cx-24, Y+76, 48, 16, a) + t(cx, Y+87, "SHARE", 8, W_, "hind", 700, "middle"))
    elif k in ("sticky", "scroll"):
        s += rect(cx-40, Y+6, 80, 94, W_, INK, 0, 2) + bars(cx-30, Y+34, 6, 60, LINE)
        s += rect(cx-38, Y+8, 76, 18, a) if k == "sticky" else rect(cx-38, Y-6+14, 76, 0.1, a) + f'<polyline points="{cx+48},{Y+70} {cx+48},{Y+20}" stroke="{a}" stroke-width="3" fill="none"/><polygon points="{cx+42},{Y+24} {cx+48},{Y+12} {cx+54},{Y+24}" fill="{a}"/>'
    elif k == "urgency":
        for i, (lab, n) in enumerate((("NOW", 2), ("THIS WEEK", 3), ("LATER", 2))): s += t(X+20, Y+20+i*30, lab, 8.5, a if i == 0 else MUTE, "hind", 700) + "".join(rect(X+20+j*56, Y+24+i*30, 50, 8, a if i == 0 else LINE) for j in range(n))
    elif k == "byagent":
        for i in range(3): s += f'<circle cx="{X+30}" cy="{Y+22+i*30}" r="9" fill="none" stroke="{INK}" stroke-width="2"/>' + rect(X+48, Y+18+i*30, 90 - i*20, 8, a if i == 0 else LINE)
    elif k == "pbar":
        for i, f in enumerate((.8, .45, .2)): s += rect(X+20, Y+20+i*26, 168, 8, LINE) + rect(X+20, Y+20+i*26, 168*f, 8, a)
    elif k == "dots":
        for i, f in enumerate((4, 2, 1)): s += "".join(f'<circle cx="{X+28+j*30}" cy="{Y+24+i*26}" r="7" fill="{a if j < f else W_}" stroke="{a}" stroke-width="2"/>' for j in range(6))
    elif k == "silent": s += f'<circle cx="{X+50}" cy="{cy}" r="16" fill="none" stroke="{INK}" stroke-width="2"/><circle cx="{X+158}" cy="{cy}" r="16" fill="none" stroke="{INK}" stroke-width="2"/>' + L(X+70, cy, X+138, cy, a, 3) + f'<polygon points="{X+138},{cy-6} {X+148},{cy} {X+138},{cy+6}" fill="{a}"/>'
    elif k == "feed": s += f'<circle cx="{X+40}" cy="{Y+30}" r="12" fill="none" stroke="{INK}" stroke-width="2"/><circle cx="{X+168}" cy="{Y+30}" r="12" fill="none" stroke="{INK}" stroke-width="2"/>' + L(X+56, Y+30, X+150, Y+30, a, 3) + rect(X+20, Y+56, 168, 30, W_, LINE) + rect(X+28, Y+64, 8, 14, a) + rect(X+44, Y+68, 120, 5, MUTE)
    elif k == "push": s += rect(cx-50, Y+40, 100, 50, W_, INK, 0, 2) + bars(cx-40, Y+52, 3, 60, LINE) + L(cx, Y+36, cx, Y+10, a, 4) + f'<polygon points="{cx-10},{Y+18} {cx},{Y+6} {cx+10},{Y+18}" fill="{a}"/>'
    elif k == "dropbox": s += f'<path d="M{cx-50},{Y+40} H{cx-10} L{cx},{Y+50} H{cx+50} V{Y+92} H{cx-50} Z" fill="{W_}" stroke="{INK}" stroke-width="2"/>' + rect(cx-34, Y+16, 50, 34, W_, a, 0, 2) + rect(cx-20, Y+24, 50, 34, a)
    elif k == "overview":
        for r in range(2):
            for c in range(3): x, y = X+14+c*62, Y+10+r*44; s += rect(x, y, 56, 40, W_, LINE) + f'<circle cx="{x+12}" cy="{y+12}" r="6" fill="{a if (r+c)%2==0 else MUTE}"/>' + rect(x+6, y+26, 40, 4, MUTE)
    elif k == "boards":
        for i in range(3): s += rect(X+30+i*14, Y+14+i*10, 110, 66, W_, INK if i == 2 else LINE, 0, 2 if i == 2 else 1)
        s += rect(X+66, Y+44, 60, 8, a) + bars(X+66, Y+60, 2, 80, LINE)
    return s
def svg(group, label, desc, facts, kind, acc):
    s = rect(0, 0, 240, 300, W_) + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    s += thumb(kind, acc); y = 174
    for l in wrap(label, 18)[:2]: s += t(16, y, l, 24, INK, "khand"); y += 25
    for l in wrap(desc, 34)[:3]: s += t(16, y, l, 12.5, MUTE); y += 16
    y = max(y + 2, 250); x = 16
    for f in facts[:2]:
        w = min(104, 18 + len(f) * 6.2); s += rect(x, y, w, 22, BEI, LINE) + t(x + 8, y + 15, f, 11, INK, "hind", 600); x += w + 6
    s += t(120, 292, "Built by Max Weberman", 8, "#8A8580", "hind", 400, "middle")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" preserveAspectRatio="xMidYMid meet" style="width:100%;height:auto;display:block">'
            f'{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>')
SL = "queue/team-improvement-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
for n, key in enumerate(DECKS):
    NAME, ABOUT, PAIRS = DECKS[key]; did = f"{key}-deck"
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}{FIX}</style>
    '''
    acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
    pairs, O, add = kdeck("teamimp_", "Grok Bot Team")
    for gi, (g, ask, a, b) in enumerate(PAIRS):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], acc[(gi + side * 2) % 4])))
        add(g, g, opts[0], opts[1], ask)
    publish(did, NAME, "Grok Bot Team", pairs, {"brands": [ABOUT, "Permanent Branding deck (R75): forward Max's 'ask Branding' dislikes here."],
            "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "topic": "team-improvement",
            "deck_size": 20, "board": "branding", "audience": "Max", "permanent": True}, seed=7500 + n, n=20)
    _o = [p[1] for p in PAIRS]; dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: _o.index(p["ask"])); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "team-improvement-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
