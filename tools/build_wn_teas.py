#!/usr/bin/env python3
"""WellNest Teas refresh decks (R107 PING, Max via WellNest Oct 17 2026 20:04 ICT; Max 20:09: build directly on the mockups).
Retires the old WellNest shelf and rebuilds it as one deck per tea (7 teas x 10 picks), from the 'WellNest Teas: Three Projects'
lookbook + Roselle Refresh brief (/workspace/wellnest/teas). Content tools/wn_teas_content.py, pictures tools/wn_teas_img.py
(A = the mockup as drafted, B = the same mockup edited), stored per deck in img/wn-teas-<tea>/ (never files/ or projects/).
Captions R105 ('<Tea>: <Element>, <one sentence>', tools/caption_rule.py); WellNest guard (tools/wn_guard.py); Notes on every pick;
standard look (white, #FAF6EE bands, #e3ddd2 borders, square corners, Khand/Hind). Page shell = tools/build_wn_tea.py head()
(Submit -> wellnest, wn-deck-done, Back -> wellnest-dashboard/?done=) + template R104 Return (kit/mw-back.js) + agent links + mw-chat.
usage: build_wn_teas.py [tea ...]   -> prints one JSON line per deck; pages written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, sys, json, string, secrets, html
from team_kit import deck as kdeck, publish, wrap
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
from wn_guard import blocked as wn_blocked, RULE as WN_RULE
import caption_rule, wn_teas_img as WI
from wn_teas_content import TEAS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
_tea = open("tools/build_wn_tea.py").read(); exec(_tea[_tea.index("def head(did):"):_tea.index("SL = ")])  # WellNest page head
INK, MUTE, LINE, CREAM, FLAG = "#0A0A0A", "#6B6560", "#e3ddd2", "#FAF6EE", "#8A5A2B"
def esc(s): return html.escape(str(s), quote=True)
def tx(x, y, s, size, col=INK, fam="Hind,system-ui,sans-serif", w=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" font-family="{fam}" font-weight="{w}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def card(tea_loc, side, o, src, size):
    W_, H_ = 216, round(216 * size[1] / size[0])
    s = f'<rect x="0" y="0" width="240" height="300" fill="#FFFFFF"/>' + f'<rect x="0" y="0" width="240" height="24" fill="{CREAM}"/>'
    s += tx(12, 16, tea_loc.upper(), 8.5, INK, w=600, extra='letter-spacing="1"')
    tag = "OUR PICK" if side == "A" else "SWAP"; tw_ = len(tag) * 5.6 + 12
    s += f'<rect x="{228 - tw_}" y="6" width="{tw_}" height="13" fill="#FFFFFF" stroke="{LINE}"/>' + tx(228 - tw_ / 2, 15.5, tag, 7.5, INK if side == "A" else FLAG, "Khand,Hind,sans-serif", 600, "middle", 'letter-spacing=".8"')
    s += f'<line x1="0" y1="24" x2="240" y2="24" stroke="{LINE}"/>'
    s += f'<image href="{src}" x="12" y="30" width="{W_}" height="{H_}" preserveAspectRatio="xMidYMid slice"/><rect x="12" y="30" width="{W_}" height="{H_}" fill="none" stroke="{LINE}"/>'
    y = 30 + H_ + 16; lab = o["label"]; fs = 16 if len(lab) <= 26 else 13.5
    for l in wrap(lab, 30 if fs == 16 else 36)[:2]: s += tx(12, y, l, fs, INK, "Khand,Hind,sans-serif", 600); y += fs - 1
    y += 1
    for l in wrap(o["desc"], 50)[:2]: s += tx(12, y, l, 9.5, MUTE); y += 11
    if o.get("flag"):
        y += 1
        for l in wrap("Check: " + o["flag"], 52)[:2]: s += tx(12, y, l, 8.5, FLAG, w=600); y += 10
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="{LINE}"/></svg>'
import subprocess  # committed template only (other workers may have the working copy mid-edit)
TPL = subprocess.run(["git", "show", "HEAD:index.template.html"], capture_output=True, text=True, check=True).stdout
pages = json.load(open("decks/pages.json")); out = []
for n, T in enumerate(TEAS):
    if sys.argv[1:] and T["key"] not in sys.argv[1:]: continue
    did = f"wellnest-teas-{T['key']}"; adir = os.path.join(ROOT, f"img/wn-teas-{T['key']}")
    pairs, Ofn, add = kdeck(f"wnt3{T['key'][:4]}_", "WellNest")
    for i, (el, sent, a, b) in enumerate(T["picks"], 1):
        ask = f"{T['loc']}: {el}, {sent}"; opts = []
        for side, o in (("A", a), ("B", b)):
            rel, size = WI.render(o["img"], adir, f"{i:02d}-{side.lower()}")
            v = Ofn(f"{i:02d}{side.lower()}", o["label"], o["desc"], "confirm" if side == "A" else "swap", card(T["loc"], side, o, rel, size), tags=[T["key"], el.lower()])
            v["image"] = rel
            if o.get("flag"): v["flag"] = o["flag"]
            opts.append(v)
        add(el, T["loc"], opts[0], opts[1], ask, purpose="confirm-or-swap")
        pairs[-1]["draft_status"] = "Our Pick, Swipe To Confirm"
    caption_rule.guard(pairs, did)
    bad = [p["ask"] for p in pairs if wn_blocked(p, False)]
    if bad: sys.exit("WellNest guard (" + WN_RULE + ") blocks: " + "; ".join(bad))
    txt = json.dumps(pairs, ensure_ascii=False).lower(); assert "cannabis" not in txt and "hemp" not in txt, did
    assert len(pairs) == 10, (did, len(pairs))
    flags = sorted({o.get("flag") for p in pairs for o in (p["optionA"], p["optionB"]) if o.get("flag")})
    publish(did, T["name"], "WellNest", pairs, {"brands": [T["about"], f"WellNest Teas: Three Projects, {T['project']}; R107 refresh (Max via WellNest, Oct 17 2026 20:04 ICT), built on the mockups (Max 20:09 ICT)."],
            "submit_agent": "wellnest", "submit_to": "WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", "deck_size": 10, "row": "nozomi", "audience": "Max",
            "project": T["project"], "tea": T["loc"], "caption_rule": "R105", "refresh": "R107", "format_note": "Every pick: A = Our Pick (draft, confirm), B = a sensible swap from the source. From Your Swipes items are settled and not asked.",
            "flags_unconfirmed": flags, "sources": {"content": "tools/wn_teas_content.py", "images": f"img/wn-teas-{T['key']}/ (A = WellNest mockup, B = edited by tools/wn_teas_img.py; ingredient photos img/wn-tea/credits.json)",
            "brief": "/workspace/wellnest/teas: WellNest Teas - Three Projects lookbook, Roselle Refresh Project Brief"}}, seed=1017 + n, n=10)
    order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
    for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
    json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    slug = pages.get(did) or f"{did}-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    s = TPL.replace("<head>", "<head>\n" + head(did), 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    out.append({"deckId": did, "name": T["name"], "project": T["project"], "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "picks": len(dj["pairs"])})
    print(json.dumps(out[-1]))
json.dump(out, open("/workspace/scratch/wn-teas/built.json", "w"), indent=1)
