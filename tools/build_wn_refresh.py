#!/usr/bin/env python3
"""WellNest deck refresh (Oct 16 2026): 6 x 20-pair decks from ops/team-sync/handoffs/wellnest-to-branding.md.
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
from wn_refresh_content import DECKS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
_src = open("tools/build_upkeep_investor_deck.py").read(); exec(_src[_src.index("INK, MUTE, LINE"):_src.index("def svg(")])  # thumb() + palette
ACC = ["#0A0A0A", "#6B6256"]  # Max neutral accents (no WellNest brand colours)
IMG = {}
def img(key):
    if key not in IMG: IMG[key] = base64.b64encode(open(f"img/wn-site/{key}.jpg", "rb").read()).decode()
    return f'<image x="16" y="40" width="208" height="104" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{IMG[key]}"/>' + rect(16, 40, 208, 104, "none", LINE)
def svg(group, label, desc, facts, kind, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    s += img(kind[4:]) if kind.startswith("img:") else thumb(kind, acc)
    y = 174
    for l in wrap(label, 18)[:2]: s += t(16, y, l, 24, INK, "khand"); y += 25
    for l in wrap(desc, 34)[:3]: s += t(16, y, l, 12.5, MUTE); y += 16
    y = max(y + 2, 250); x = 16
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
SL = "queue/wn-refresh-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
for n, D in enumerate(DECKS):
    if sys.argv[1:] and D["key"] not in sys.argv[1:]: continue
    row = D["row"]; did = f"wellnest-{'nozomi' if row == 'nozomi' else 'business'}-{D['key']}"
    pairs, O, add = kdeck("wnr" + re.sub("[^a-z]", "", D["key"])[:8] + "_", "WellNest")
    for gi, (g, ask, a, b) in enumerate(D["pairs"]):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], ACC[(gi + side) % 2])))
        add(g, g, opts[0], opts[1], ask)
    bad = [p["ask"] for p in pairs if wn_blocked(p, False)]
    if bad: sys.exit("WellNest guard (" + WN_RULE + ") blocks: " + "; ".join(bad))
    aud = "Nozomi" if row == "nozomi" else "P'Thom and Max"
    publish(did, D["name"], "WellNest", pairs, {"brands": [D["about"], f"WellNest row {'one (For Nozomi)' if row == 'nozomi' else 'two (For P' + chr(39) + 'Thom And Max)'}; Oct 16 2026 refresh brief."],
            "submit_agent": "wellnest", "submit_to": "WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", "deck_size": 20, "row": row, "audience": aud,
            "sources": {"brief": "/workspace/ops/team-sync/handoffs/wellnest-to-branding.md"}}, seed=7300 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "wellnest-" + D["key"] + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + head(did), 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": D["name"], "row": row, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
