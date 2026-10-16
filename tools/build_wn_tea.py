#!/usr/bin/env python3
"""WellNest tea decks (Oct 16 2026): Three Tea Lines + Partnership Teas, 4 x 20 pairs, adapted from build_wn_refresh.py.
(origin: WellNest deck refresh (Oct 16 2026): 6 x 20-pair decks from ops/team-sync/handoffs/wellnest-to-branding.md.
Rows: nozomi (Baby Steps To Opening, Site Plan Options, Tea Products And Second Looks) and business (Small Tests To Start Now,
Which Wellness Collective Idea To Test First, Partners To Approach First). Content: tools/wn_refresh_content.py.
Max standard look: white + #FAF6EE/#e3ddd2, Khand/Hind, square corners, no emoji, no WellNest brand colours.
Site plan cards use crops of Render 2 / Render 3 (Dropbox /The WellNest/Photos for Presentation) in img/wn-site/.
Submit -> wellnest; wn-deck-done on real submit; Back -> wellnest-dashboard/?done=<deckId>; mw-chat cc11 to WellNest Agent.
usage: build_wn_refresh.py [key ...]"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import sys, os, json, re, string, secrets, base64
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish, wrap, shareic
from draft_svg import t, rect
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
from wn_guard import blocked as wn_blocked, RULE as WN_RULE
from wn_tea_content import DECKS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
_src = open("tools/build_upkeep_investor_deck.py").read(); exec(_src[_src.index("INK, MUTE, LINE"):_src.index("def svg(")])  # thumb() + palette
ACC = ["#0A0A0A", "#6B6256"]
IMG = {}
def img(key):
    if key not in IMG: IMG[key] = base64.b64encode(open(f"img/wn-tea/{key}.jpg", "rb").read()).decode()
    return f'<image x="16" y="40" width="208" height="120" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{IMG[key]}"/>' + rect(16, 40, 208, 120, "none", LINE)
BAND = {"Calm": "#2E5FA8", "Energy": "#5E8A3A", "Digestion": "#B8873A", "Beauty": "#A8323E", "Trio": "#A8323E"}
def label(cx, cy, w, h, style, name, sub):
    paper = "#FFFFFF" if style == "white" else "#FAF6EE"
    if style == "round":
        r = min(w, h) / 2
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{paper}" stroke="#C9BFAE"/>' + t(cx, cy + 1, name[:12], 8.5, INK, "khand", 600, "middle") + t(cx, cy + 11, sub[:14], 6.5, MUTE, "hind", 400, "middle")
    s = rect(cx - w / 2, cy - h / 2, w, h, paper, "#C9BFAE")
    if style == "band": s += rect(cx - w / 2, cy - h / 2, w, 7, BAND.get(sub, "#A8323E"))
    big = style == "big"
    y = cy - h / 2 + (24 if big else 18)
    for l in wrap(name, 13)[:2]: s += t(cx, y, l, 12 if big else 10, INK, "khand", 600, "middle"); y += 13 if big else 11
    for l in wrap(sub, 20)[:2]: s += t(cx, y, l, 6.5, MUTE, "hind", 500, "middle"); y += 8
    extra = {"thai": "ชา  Tea", "ingr": "roselle, pandan, lemongrass", "icons": "cup  95C  5 min", "origin": "Grown in Chiang Mai", "cf": "CAFFEINE FREE",
             "date": "Harvest: Oct 2026", "herbal": "Herbal tea only. No cannabis.", "stamp": "hand stamped"}.get(style)
    if style == "bot":
        s += f'<path d="M{cx} {cy+h/2-4} L{cx} {cy+h/2-18}" stroke="#5E8A3A" stroke-width="1.2"/><ellipse cx="{cx-6}" cy="{cy+h/2-12}" rx="6" ry="2.5" fill="#5E8A3A" transform="rotate(-30 {cx-6} {cy+h/2-12})"/><ellipse cx="{cx+6}" cy="{cy+h/2-9}" rx="6" ry="2.5" fill="#5E8A3A" transform="rotate(30 {cx+6} {cy+h/2-9})"/>'
    elif style == "qr":
        for i in range(4):
            for j in range(4):
                if (i * 3 + j) % 3: s += rect(cx - 8 + i * 4, cy + h / 2 - 19 + j * 4, 4, 4, INK)
    elif extra: s += t(cx, cy + h / 2 - 5, extra, 5.5, "#2E5FA8" if style == "cf" else "#6B6256", "hind", 600, "middle")
    return s
def pack(spec):
    kind, style, txt = spec.split(":", 2); name, sub = (txt.split("|") + [""])[:2]
    s = rect(16, 40, 208, 120, "#F3EEE4", LINE); cx = 120
    if kind == "pouch":
        s += '<path d="M84 50 H156 L160 156 H80 Z" fill="#C9A274" stroke="#9C7A52"/>' + rect(84, 50, 72, 6, "#B48D5F") + '<path d="M86 62 H154" stroke="#9C7A52" stroke-dasharray="2 2"/>'
        s += label(cx, 110, 62, 56, style, name, sub)
    elif kind == "tin":
        s += rect(86, 58, 68, 96, "#D8D4CC", "#8F8A82") + rect(83, 50, 74, 12, "#BDB8AF", "#8F8A82") + label(cx, 108, 62, 58, style, name, sub)
    elif kind == "jar":
        s += rect(97, 46, 46, 10, "#3A3A3A") + '<path d="M90 58 H150 Q155 58 155 64 V150 Q155 156 149 156 H91 Q85 156 85 150 V64 Q85 58 90 58 Z" fill="#E9F0EE" stroke="#9FB2AE"/>'
        s += rect(89, 128, 62, 24, "#A8323E") + label(cx, 96, 62, 52, style, name, sub)
    elif kind == "cloth":
        s += '<path d="M82 64 Q120 58 158 64 L162 154 H78 Z" fill="#EDE3D0" stroke="#B9A98C"/><path d="M82 70 Q120 64 158 70" stroke="#8C6B4A" stroke-width="2" fill="none"/><path d="M118 66 q-8 -16 -16 -8 M122 66 q8 -16 16 -8" stroke="#8C6B4A" stroke-width="2" fill="none"/>'
        s += label(cx, 114, 62, 52, style, name, sub)
    s += t(214, 155, "mockup", 6, "#8A8580", "hind", 400, "end")
    return s
def svg(group, label_, desc, facts, kind, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    s += img(kind[4:]) if kind.startswith("img:") else pack(kind[3:])
    y = 186
    for l in wrap(label_, 18)[:2]: s += t(16, y, l, 22, INK, "khand"); y += 23
    for l in wrap(desc, 34)[:2]: s += t(16, y, l, 12.5, MUTE); y += 16
    y = max(y + 2, 254); x = 16
    for f in facts[:2]:
        w = min(104, 18 + len(f) * 6.2); s += rect(x, y, w, 22, BEI, LINE) + t(x + 8, y + 15, f, 11, INK, "hind", 600); x += w + 6
    s += t(120, 292, "Built by Machan", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>'
def head(did):
    return f'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="{did}"</script>
<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}</style>
<script>(function(){{var ID="{did}",DONE="https://webermanapps.github.io/wellnest-dashboard/?done="+ID;
function mark(){{try{{var a=JSON.parse(localStorage.getItem("wn-deck-done")||"[]");if(!Array.isArray(a))a=[];if(a.indexOf(ID)<0)a.push(ID);localStorage.setItem("wn-deck-done",JSON.stringify(a))}}catch(e){{}}}}
var f=window.fetch;window.fetch=function(u,o){{var p=f.apply(this,arguments);try{{if(o&&o.method==="POST"&&o.body){{var b=JSON.parse(o.body);if(b&&b.deck===ID&&b.agent==="wellnest"&&!b.test&&!b.partial)p.then(function(){{mark()}},function(){{}})}}}}catch(e){{}}return p}};
function fix(){{document.querySelectorAll('a[href*="branding-djqmb410/decks"]').forEach(function(a){{a.href=DONE;a.removeAttribute("target")}})}}
new MutationObserver(fix).observe(document.documentElement,{{childList:true,subtree:true}});document.addEventListener("DOMContentLoaded",fix)}})();</script>
'''
SL = "queue/wn-tea-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
for n, D in enumerate(DECKS):
    if sys.argv[1:] and D["key"] not in sys.argv[1:]: continue
    did = "wellnest-" + D["key"]
    pairs, O, add = kdeck("wnt" + re.sub("[^a-z]", "", D["key"])[:10] + "_", "WellNest")
    for gi, (g, ask, a, b) in enumerate(D["pairs"]):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], ACC[(gi + side) % 2])))
        add(g, g, opts[0], opts[1], ask)
    bad = [p["ask"] for p in pairs if wn_blocked(p, False)]
    if bad: sys.exit("WellNest guard (" + WN_RULE + ") blocks: " + "; ".join(bad))
    publish(did, D["name"], "WellNest", pairs, {"brands": [D["about"], "WellNest project: " + D["project"] + "; Oct 16 2026 request (WellNest header shelf)."],
            "submit_agent": "wellnest", "submit_to": "WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", "deck_size": 20, "row": "nozomi", "audience": "Nozomi", "project": D["project"],
            "sources": {"images": "img/wn-tea/credits.json (Wikimedia Commons)", "content": "tools/wn_tea_content.py"}}, seed=7400 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "wellnest-" + D["key"] + "-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + head(did), 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": D["name"], "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
