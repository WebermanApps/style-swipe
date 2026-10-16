#!/usr/bin/env python3
"""Roselle Packaging Polish Deck (Oct 16 2026 21:44 ICT): 20 small refinements of the real WellNest roselle pouch. Content tools/wn_roselle_content.py.
Drawn mockups follow the real pouch (img/wn-roselle/ref-*.jpg, inset as 'Today'). Same page shell as tools/build_wn_tea.py. usage: build_wn_roselle.py"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, re, string, secrets, base64
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish, wrap, shareic
from draft_svg import t, rect
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
from wn_guard import blocked as wn_blocked, RULE as WN_RULE
from wn_roselle_content import CURRENT, PAIRS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
_tea = open("tools/build_wn_tea.py").read(); exec(_tea[_tea.index("def head(did):"):_tea.index("SL = ")])  # page head (wn-deck-done, Back -> dashboard)
_src = open("tools/build_upkeep_investor_deck.py").read(); exec(_src[_src.index("INK, MUTE, LINE"):_src.index("def svg(")])  # palette (INK, MUTE, LINE, BEI)
TW = "Courier Prime,Courier New,Courier,monospace"; SER = "Georgia,Times New Roman,serif"
REF = {k: base64.b64encode(open(f"img/wn-roselle/ref-{k}.jpg", "rb").read()).decode() for k in ("front", "back")}
def tx(x, y, s, size, col="#3A3330", fam=TW, w=400, anchor="start", extra=""):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" font-family="{fam}" font-weight="{w}" text-anchor="{anchor}" {extra}>{s}</text>'
def logo(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E2C77A" stroke-width="{r*.16}" opacity=".8"/><circle cx="{cx+.6}" cy="{cy-.4}" r="{r*.9}" fill="none" stroke="#9CC6C0" stroke-width="{r*.06}" opacity=".7"/>'
            + tx(cx, cy - r * .12, "The", r * .42, "#3A3330", "Brush Script MT,Segoe Script,cursive", 400, "middle", 'font-style="italic"') + tx(cx, cy + r * .42, "WellNest", r * .48, "#3A3330", "Brush Script MT,Segoe Script,cursive", 400, "middle", 'font-style="italic"'))
def pouch(x, y, w, h, o, uid):
    sheen = f'<linearGradient id="sh{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".28"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>' if o["sheen"] else ""
    s = f'<defs>{sheen}<filter id="br{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.08 0.5" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter>'
    s += f'<linearGradient id="fd{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{o["pink"]}" stop-opacity="0"/><stop offset=".55" stop-color="{o["pink"]}" stop-opacity=".85"/><stop offset="1" stop-color="{o["pink"]}"/></linearGradient></defs>'
    s += f'<path d="M{x} {y} H{x+w} L{x+w+3} {y+h} H{x-3} Z" fill="#C8A273" stroke="#9C7A52" stroke-width=".8"/>'
    s += f'<path d="M{x+2} {y+9} H{x+w-2}" stroke="#A9855A" stroke-width="1.4"/>'
    if o["seal"] == "notch": s += f'<path d="M{x} {y+16} l4 2 l-4 2" fill="#F3EEE4" stroke="#9C7A52" stroke-width=".6"/>'
    else: s += f'<circle cx="{x+w/2}" cy="{y+5}" r="6" fill="{o["pink"]}" stroke="#fff" stroke-width="1"/>' + tx(x + w / 2, y + 6.8, "WN", 4.5, "#fff", SER, 700, "middle")
    lx, ly, lw, lh = x + 6, y + 24, w - 12, h - 30
    s += rect(lx, ly, lw, lh, "#FBF6EC", "#E6DCCB", 0, .6)
    wh = lh * o["washh"]; wy = ly + lh - wh
    if o["fade"] == "brush": s += f'<g filter="url(#br{uid})"><rect x="{lx+1}" y="{wy}" width="{lw-2}" height="{wh-1}" fill="{o["pink"]}" opacity=".88"/></g>'
    else: s += f'<rect x="{lx}" y="{wy - wh*.4}" width="{lw}" height="{wh*1.4}" fill="url(#fd{uid})"/>'
    r = 9 * o["logos"]
    s += logo(lx + lw - r - 4, ly + r + 4, r) if o["logo"] == "tr" else logo(lx + lw / 2, ly + r + 4, r)
    ty = ly + (2 * r + 18 if o["logo"] == "tc" else 30)
    s += tx(lx + 6, ty, "ROSELLE", 10.5, "#3A3330", TW, o["titlew"], "start", 'letter-spacing="1"')
    if o["thai"]: s += tx(lx + 6, ty + 8, "กระเจี๊ยบ", 6, "#3A3330", "Sarabun,Noto Sans Thai,Tahoma,sans-serif"); ty += 7
    s += tx(lx + 6, ty + 8, "organic herbal tea", 5.2, "#8C7F76", SER, 400, "start", 'font-style="italic"')
    s += tx(lx + 6, ty + 18, o["tagline"], 4.2, "#3A3330")
    cl = o["claims"]; cs = o["claimsz"]; lines = [cl] if len(cl) * cs * .6 < lw - 10 else [cl[:cl.rfind("|", 0, len(cl)//2+8)].strip(), cl[cl.rfind("|", 0, len(cl)//2+8)+1:].strip()]
    for i, l in enumerate(lines): s += tx(lx + 6, ty + 24 + i * (cs + 1.5), l, cs, "#3A3330")
    for i, l in enumerate(["RELATIONSHIP: Direct trade", "REGION: Chiangmai", "FARM: Kraingan Farm", "INGREDIENT: Organic roselle"]):
        s += tx(lx + 6, ly + lh - 22 + i * 4.6, l, 3.4, "#4A2A2E")
    if o["weight"] == "corner": s += tx(lx + lw - 4, ly + lh - 4, "NET WT 100G", 3.4, "#4A2A2E", TW, 400, "end")
    else: s += f'<circle cx="{lx+lw-11}" cy="{ly+lh-12}" r="8" fill="#FBF6EC" stroke="#4A2A2E" stroke-width=".7"/>' + tx(lx + lw - 11, ly + lh - 11, "100 g", 4.4, "#4A2A2E", TW, 700, "middle")
    if o["window"]:
        wx, wy2 = lx + lw / 2 - 14, ly + lh * .47
        s += f'<rect x="{wx}" y="{wy2}" width="28" height="13" rx="6.5" fill="#5A1A24" stroke="#E6DCCB"/>' + "".join(f'<circle cx="{wx+5+i*4.5}" cy="{wy2+6.5+(i%2)*2-1}" r="2.2" fill="#8E2236"/>' for i in range(5))
    if o["sheen"]: s += f'<path d="M{x} {y} H{x+w} L{x+w+3} {y+h} H{x-3} Z" fill="url(#sh{uid})"/>'
    return s
def back(x, y, w, h, o, uid):
    s = f'<path d="M{x} {y} H{x+w} L{x+w+3} {y+h} H{x-3} Z" fill="#C8A273" stroke="#9C7A52" stroke-width=".8"/>' + f'<path d="M{x+2} {y+9} H{x+w-2}" stroke="#A9855A" stroke-width="1.4"/>'
    lx, ly, lw, lh = x + 6, y + 20, w - 12, h - 24
    s += rect(lx, ly, lw, lh, "#FBF6EC", "#E6DCCB", 0, .6)
    s += tx(lx + lw / 2, ly + 9, "The WellNest", 6.5, "#3A3330", "Brush Script MT,Segoe Script,cursive", 400, "middle", 'font-style="italic"')
    for i in range(4): s += rect(lx + 6, ly + 14 + i * 4, lw - 12 - (i == 3) * 20, 1.4, "#B9AEA3")
    s += tx(lx + lw / 2, ly + 34, "www.thewellnest.organic", 3.4, "#3A3330", TW, 400, "middle")
    ic = o["pink"] if o["icons"] == "pink" else "none"; st = o["pink"] if o["icons"] == "pink" else "#3A3330"
    def icon(cx, cy, kind):
        if kind == "org": return f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{ic}" stroke="{st}" stroke-width=".6"/>' + tx(cx, cy + 1.3, "100%", 2.6, "#fff" if ic != "none" else st, TW, 700, "middle")
        if kind == "hand": return f'<path d="M{cx-5} {cy+3} q2 -6 5 -2 q3 -4 5 2 z" fill="{ic}" stroke="{st}" stroke-width=".6"/><circle cx="{cx}" cy="{cy-3}" r="2" fill="{ic}" stroke="{st}" stroke-width=".6"/>'
        if kind == "temp": return rect(cx - 2.5, cy - 4, 5, 8, ic, st, 1, .6)
        if kind == "cup": return f'<path d="M{cx-4} {cy-2} h8 v3 a4 4 0 0 1 -8 0 z" fill="{ic}" stroke="{st}" stroke-width=".6"/>'
        return f'<circle cx="{cx}" cy="{cy}" r="4" fill="{ic}" stroke="{st}" stroke-width=".6"/><path d="M{cx} {cy-2.5} V{cy} H{cx+2}" stroke="{st if ic=="none" else "#fff"}" stroke-width=".6" fill="none"/>'
    if o["backlayout"] == "stack":
        s += f'<path d="M{lx+6} {ly+38} H{lx+lw-6}" stroke="#B9AEA3" stroke-width=".5"/>' + tx(lx + lw / 2, ly + 44, "ABOUT THE FARM", 4, "#3A3330", TW, 400, "middle")
        for i in range(3): s += rect(lx + 6, ly + 47 + i * 3.5, lw - 12, 1.2, "#B9AEA3")
        s += icon(lx + lw * .33, ly + 65, "org") + icon(lx + lw * .67, ly + 65, "hand") + tx(lx + lw * .33, ly + 74, "CERTIFIED ORGANIC", 2.6, "#3A3330", TW, 400, "middle") + tx(lx + lw * .67, ly + 74, "HANDMADE PRODUCT", 2.6, "#3A3330", TW, 400, "middle")
        s += f'<path d="M{lx+6} {ly+79} H{lx+lw-6}" stroke="#B9AEA3" stroke-width=".5"/>' + tx(lx + lw / 2, ly + 85, "DIRECTIONS", 4, "#3A3330", TW, 400, "middle")
        for j, (k, l) in enumerate([("temp", "95°C"), ("cup", "1 calyx / cup"), ("time", "5 min")]):
            cx = lx + lw * (.22 + j * .28); s += icon(cx, ly + 95, k) + tx(cx, ly + 104, l, 2.6, "#3A3330", TW, 400, "middle")
        dy = ly + 95
    else:
        cw = (lw - 14) / 2; c1, c2 = lx + 5, lx + 9 + cw
        s += f'<path d="M{lx+6} {ly+38} H{lx+lw-6}" stroke="#B9AEA3" stroke-width=".5"/><path d="M{lx+lw/2} {ly+42} V{ly+100}" stroke="#B9AEA3" stroke-width=".5"/>'
        s += tx(c1 + cw / 2, ly + 45, "ABOUT THE FARM", 3.2, "#3A3330", TW, 400, "middle") + tx(c2 + cw / 2, ly + 45, "DIRECTIONS", 3.2, "#3A3330", TW, 400, "middle")
        for i in range(4): s += rect(c1, ly + 49 + i * 3.5, cw, 1.2, "#B9AEA3")
        s += icon(c1 + cw * .3, ly + 74, "org") + icon(c1 + cw * .75, ly + 74, "hand") + tx(c1 + cw / 2, ly + 84, "ORGANIC + HANDMADE", 2.4, "#3A3330", TW, 400, "middle")
        for j, (k, l) in enumerate([("temp", "95°C"), ("cup", "1 calyx/cup"), ("time", "5 min")]):
            cy = ly + 55 + j * 14; s += icon(c2 + 6, cy, k) + tx(c2 + 13, cy + 1, l, 2.8, "#3A3330")
        dy = ly + 92
    if o["qr"] != "none":
        qx, qy = (lx + lw - 14, ly + 26) if o["qr"] == "web" else (lx + lw - 13, dy - 22 if o["backlayout"] == "stack" else dy)
        s += rect(qx, qy, 10, 10, "#fff", "#3A3330", 0, .5) + "".join(rect(qx + 1 + (i % 4) * 2, qy + 1 + (i // 4) * 2, 1.6, 1.6, "#3A3330") for i in range(16) if (i * 7) % 3)
    return s
def shelftag(o, uid):
    k = o["tag"]; s = f'<defs><filter id="br{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.08 0.5" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter></defs>'
    x, y, w, h = 70, 66, 140, 82
    s += rect(x, y, w, h, "#FBF6EC" if k == "cream" else "#C8A273", "#9C7A52", 0, .8)
    if k != "cream": s += rect(x + 5, y + 5, w - 10, h - 10, "#FBF6EC") + f'<g filter="url(#br{uid})"><rect x="{x+6}" y="{y+h-28}" width="{w-12}" height="22" fill="{o["pink"]}" opacity=".88"/></g>'
    s += logo(x + w - 18, y + 18, 9) + tx(x + 12, y + 24, "ROSELLE", 12, "#3A3330", TW, 400, "start", 'letter-spacing="1"') + tx(x + 12, y + 34, "organic herbal tea", 6, "#8C7F76", SER, 400, "start", 'font-style="italic"')
    s += tx(x + 12, y + 46, "100 g", 6, "#3A3330")
    if k == "farm": s += tx(x + 12, y + 56, "From Kraingan Farm, Chiang Mai", 4.6, "#3A3330")
    return s
N = [0]
def svg(group, label_, desc, facts, view, over, acc):
    o = dict(CURRENT); o.update(over); N[0] += 1; uid = N[0]
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, acc)
    s += t(16, 26, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 13, INK, 15)
    s += rect(16, 34, 208, 168, "#F3EEE4", LINE)
    ref = "back" if view == "back" else "front"
    s += f'<image x="22" y="42" width="44" height="{81 if ref=="front" else 67}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{REF[ref]}"/>' + rect(22, 42, 44, 81 if ref == "front" else 67, "none", "#C9BFAE") + t(44, 133 if ref == "front" else 119, "Today", 8, MUTE, "hind", 600, "middle")
    if view == "front": s += pouch(98, 40, 108, 156, o, uid)
    elif view == "back": s += back(98, 40, 108, 156, o, uid)
    else: s += shelftag(o, uid)
    s += t(214, 198, "mockup", 6, "#8A8580", "hind", 400, "end")
    y = 226
    for l in wrap(label_, 20)[:1]: s += t(16, y, l, 21, INK, "khand"); y += 20
    for l in wrap(desc, 36)[:2]: s += t(16, y, l, 12, MUTE); y += 15
    y = max(y + 1, 262); x = 16
    for f in facts[:2]:
        w = min(104, 18 + len(f) * 6.2); s += rect(x, y, w, 20, BEI, LINE) + t(x + 8, y + 14, f, 10.5, INK, "hind", 600); x += w + 6
    s += t(120, 294, "Built by Machan", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>'
ACC = ["#0A0A0A", "#6B6256"]; FEEL = ["practical", "bold", "calm", "playful", "premium"]
did = "wellnest-roselle-packaging-polish"; name = "Roselle Packaging Polish Deck"
pairs, O, add = kdeck("wntrosellepol_", "WellNest")
for gi, (g, ask, a, b) in enumerate(PAIRS):
    opts = []
    for side, o in enumerate((a, b)):
        oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
        opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], o[5], ACC[(gi + side) % 2])))
    add(g, g, opts[0], opts[1], ask)
bad = [p["ask"] for p in pairs if wn_blocked(p, False)]
if bad: sys.exit("WellNest guard (" + WN_RULE + ") blocks: " + "; ".join(bad))
if "--preview" in sys.argv:
    open("/tmp/teaimg/rp.html", "w").write('<body style="display:flex;flex-wrap:wrap;gap:6px;width:1300px">' + "".join(p[k]["visual"]["svg"] for p in pairs for k in ("optionA", "optionB"))); sys.exit()
publish(did, name, "WellNest", pairs, {"brands": ["Polish, not redesign, of the real WellNest roselle pouch: small refinements only (pink wash, logo, title, Thai name, wording, back panel, window, seal, finish, weight, QR, shelf tag)", "WellNest project: Three Tea Lines; Max via WellNest Oct 16 2026 21:44 ICT."],
        "submit_agent": "wellnest", "submit_to": "WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", "deck_size": 20, "row": "nozomi", "audience": "Nozomi", "project": "Three Tea Lines",
        "sources": {"reference": "img/wn-roselle/ref-front.jpg, ref-back.jpg (WellNest Instagram story, May 16 2024, Instagram UI cropped out)", "content": "tools/wn_roselle_content.py"}}, seed=7500, n=20, first=20)
dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20
SL = "queue/wn-tea-slugs.json"; slugs = json.load(open(SL))
if did not in slugs: slugs[did] = "wellnest-roselle-packaging-polish-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + head(did), 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": did, "name": name, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
