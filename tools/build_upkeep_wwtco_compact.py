#!/usr/bin/env python3
"""What We Take Care Of: Compact Polish (Branding, Oct 17 2026, for UpKeep).
Max (via UpKeep, 21:09 ICT): no new directions. He wants the condensed What We Take Care Of section that was live before the
grid / season strip / house map round (smart-upkeep 8712223), now restored (smart-upkeep d49e1d8: swipeable category carousel),
refined a little. Every pick is a small A/B on that compact layout: Option A is the live compact section, Option B one small change.
Mockups are drawn from the live code (app.js WW_CATS + wwCarousel, styles.css .ca-*, the site's own icon paths in
tools/uk_wwtco_icons.json, from icons.js): phone view at 393 wide plus a full-size close-up.
Captions (R105): 'smartupkeep.ai What We Take Care Of: <element>, <one plain sentence>' (checked with tools/caption_rule.check).
Name by theme, no numbers (R113). No Thai references (R110). Light only, Khand/Hind, no emoji.
usage: build_upkeep_wwtco_compact.py -> prints {deckId, slug, url}; page written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from draft_svg import t, rect, ln, dot, screen, esc, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import deck, publish
import caption_rule
from split_deck import theme_name_ok
DID = "upkeep-what-we-take-care-of-compact-polish-deck"; NAME = "What We Take Care Of: Compact Polish"
LOC = "smartupkeep.ai What We Take Care Of"
assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
ICO = json.load(open("tools/uk_wwtco_icons.json"))
CREAM = "#FAF6EE"; DARK = "#1f1b17"
# live tints (styles.css .ca-t / .ca-l / .ca-s)
TINT = {"t": ("#A8431F", "#FAF3EB"), "l": ("#05668D", "#EDF4F7"), "s": ("#8a6510", "#FAF3DD"), "j": ("#0B6E4F", "#EAF3EE")}
CATS = [("Heating & Cooling", ["furnace", "ac"], ["Furnace", "AC", "Furnace Filters"], "t"),
        ("Water", ["waterheater", "meter"], ["Water Heater", "Mold and Moisture Scan", "Gutters"], "l"),
        ("Air & Safety", ["detector", "dryer"], ["Smoke/CO", "Dryer Vent", "Moisture Readings"], "s"),
        ("Outside", ["gutter", "chimney"], ["Gutters", "Roof", "Flashing"], "t")]
FILL = {"f-t": TERRA, "f-l": LAGOON, "f-s": SAFFRON}
def icon(name, x, y, size):
    body = ICO[name]
    for k, c in FILL.items(): body = body.replace(f'class="{k}', f'fill="{c}" class="{k}')
    body = body.replace('class="f-j', f'stroke="{JUNGLE}" class="f-j')
    k = size / 48
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.4f})" fill="none" stroke="{DARK}" stroke-width="2.1" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g>')
def T(x, y, s, size, col=INK, fam="Hind", w=500, anchor="start", extra=""):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" {extra}>{esc(s)}</text>'
D = dict(rowh=23.5, fs=13.1, fw=500, icons="two", art=72, order=(0, 1, 2, 3), tap="sheet", safety="s", longname=True, seeall="right", scroll=0)
CW, GAP = 282, 9.6
def cats(o):
    out = []
    for i in o["order"]:
        nm, ic, items, tint = CATS[i]
        if nm == "Air & Safety": tint = o["safety"]
        if not o["longname"]: items = [("Moisture Scan" if s == "Mold and Moisture Scan" else s) for s in items]
        out.append((nm, ic, items, tint))
    return out
def card_h(o): return round(9 + 24 + 3 * o["rowh"] + 9, 1)
def card(x, y, c, o):
    nm, ic, items, tint = c; tc, bg = TINT[tint]; h = card_h(o); a = o["art"]
    s = rect(x + .5, y + 2.5, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(x, y, CW, h, "#FFFFFF", "#e5e0d8", 14, 1)
    ax, ay, ah = x + 9.6, y + 8.8, h - 17.6
    s += rect(ax, ay, a, ah, bg, "none", 10)
    if o["icons"] == "two":
        k = a / 72; s += icon(ic[0], ax + 6 * k, ay + 8 * k, 42 * k) + icon(ic[1], ax + 30 * k, ay + 38 * k, 36 * k)
    else:
        sz = a * .7; s += icon(ic[0], ax + (a - sz) / 2, ay + (ah - sz) / 2, sz)
    bx = ax + a + 9.6; bw = x + CW - 9.6 - bx
    s += T(bx, y + 26, nm, 17.3, tc, "Khand", 700)
    ry = y + 33
    for it in items:
        s += f'<line x1="{bx:.2f}" y1="{ry:.2f}" x2="{bx + bw:.2f}" y2="{ry:.2f}" stroke="#f0ebe3" stroke-width="1"/>'
        by = ry + o["rowh"] / 2 + o["fs"] * .36
        s += T(bx, by, it, o["fs"], INK, "Hind", o["fw"])
        if o["tap"] == "sheet": s += T(bx + bw, by, "\u203a", 14, "#aaaaaa", "Hind", 400, "end")
        ry += o["rowh"]
    return s
def head(y, o):
    s = T(16, y + 20, "What We Take Care Of", 19.2, INK, "Khand", 700)
    if o["seeall"] == "right": s += T(377, y + 19, "SEE ALL", 12.5, INK, "Hind", 600, "end", 'letter-spacing="1.4"')
    return s
def section(o, y0=0):
    """the live compact section in CSS px on a 393-wide phone"""
    s = head(y0, o); y = y0 + 32; cs = cats(o)
    for i, c in enumerate(cs):
        x = 16 + (i - o["scroll"]) * (CW + GAP)
        if -CW < x < 393: s += card(x, y, c, o)
    y += card_h(o) + 12
    xs = 196.5 - (14 + 3 * 5 + 3 * 4) / 2
    for i in range(4):
        on = i == o["scroll"]; w = 14 if on else 5
        s += rect(xs, y, w, 5, TERRA if on else "#dddddd", "none", 2.5); xs += w + 4
    y += 5
    if o["seeall"] == "under": y += 10; s += T(196.5, y + 12, "See All", 13, LAGOON, "Hind", 600, "middle", 'text-decoration="underline"'); y += 16
    return s, y - y0
def sheet(y, title, line1, line2):
    s = rect(0, y, 393, 150, "#FFFFFF", "#e5e0d8", 16) + rect(176, y + 8, 40, 4, "#D6D0C6", "none", 2)
    s += T(377, y + 30, "\u00d7", 22, INK, "Hind", 400, "end") + T(20, y + 46, title, 22, INK, "Khand", 700)
    s += T(20, y + 70, line1, 14, "#333333", "Hind", 400) + T(20, y + 90, line2, 14, "#333333", "Hind", 400)
    s += rect(20, y + 104, 353, 34, TERRA, "none", 8) + T(196.5, y + 126, "Free Quote in Minutes", 14, "#FFFFFF", "Hind", 600, "middle")
    return s
def mock(over=None, note="", close="card", sheet_on=False):
    o = dict(D, **(over or {})); K = 240 / 393
    s = rect(0, 0, 240, 26, CREAM) + t(12, 17, "SMARTUPKEEP.AI \u00b7 HOME", 8, INK, "hind", 700, extra='letter-spacing="1"') + t(228, 17, "Phone, 393 wide", 7.5, MUTE, anchor="end") + ln(26, 0, 240, LINE)
    body, h = section(o, 0)
    s += f'<g transform="translate(0,34) scale({K:.4f})">{body}</g>'
    yc = 34 + h * K + 12
    s += t(12, yc, "CLOSE-UP", 7.5, MUTE, "hind", 700, extra='letter-spacing="1.2"'); yc += 6
    Z = .8
    if close == "card":
        cs = cats(o); c = cs[o["scroll"]]
        g = card(0, 0, c, o); s += f'<g transform="translate({120 - CW * Z / 2:.2f},{yc:.2f}) scale({Z})">{g}</g>'; yc += card_h(o) * Z
    elif close == "sheet":
        g2 = sheet(0, "Furnace", "Fall Furnace Tune-Up, and filters", "changed during your visits.")
        s += t(120, yc + 8, "Tap Furnace and this sheet slides up:", 8, MUTE, anchor="middle"); yc += 14
        Z3 = .58; s += f'<g transform="translate({120 - 393 * Z3 / 2:.2f},{yc:.2f}) scale({Z3})">{g2}</g>'; yc += 150 * Z3
    elif close == "head":
        # crop of the live section at full close-up size (nested svg viewBox = the part that changes)
        body2, h2 = section(o, 0)
        vx, vy, vw, vh = (140, 0, 253, 105) if o["seeall"] == "right" else (70, 120, 253, 105)
        if o["seeall"] == "under": vy = h2 - 80
        s += f'<svg x="8" y="{yc:.2f}" width="224" height="{224 * vh / vw:.2f}" viewBox="{vx} {vy} {vw} {vh}">{body2}</svg>'; yc += 224 * vh / vw
    if note:
        yn = max(yc + 18, 262)
        s += rect(12, yn - 10, 3, 24, TERRA) + t(20, yn, note[0], 8.5, INK, "hind", 600) + (t(20, yn + 12, note[1], 7.8, MUTE) if len(note) > 1 else "")
    return screen(s)
pairs, O, add = deck("wwcp_", "UpKeep")
_n = [0]
def P(g, el, sentence, a, b):
    _n[0] += 1; k = f"{_n[0]:02d}_"; ask = f"{LOC}: {el}, {sentence}"
    bad = caption_rule.check(ask[0].upper() + ask[1:]); assert not bad, (ask, bad)
    for x in (a, b): assert len(x[1]) <= 34 and len(x[2]) <= 62, x[:3]
    add(g, g, O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask)
NOW = ("As live now",)
P("Spacing", "Row spacing", "keep today's tight rows between service names or give each row a little more room?",
  ("tight", "Tight Rows (As Now)", "Rows as live; the card stays short.", "calm", mock(note=("Tight rows, as live now", "Card is about 115px tall on a phone"))),
  ("roomy", "A Little More Room", "Each row 4px taller; card about 12px taller.", "practical", mock({"rowh": 27.5}, note=("Rows 4px taller", "Still one compact card per group"))))
P("Type Size", "Service name size", "keep the 13px service names or step them up to 14.5px?",
  ("fs13", "13px Names (As Now)", "Small, tidy rows as live.", "calm", mock(note=("13px service names, as live now", "Fits the longest name on one line"))),
  ("fs145", "14.5px Names", "Easier to read; same rows, same card.", "practical", mock({"fs": 14.5}, note=("14.5px service names", "Same rows, a bit easier to read"))))
P("Type Weight", "Service name weight", "keep the medium weight names or switch to a lighter regular weight?",
  ("w500", "Medium Names (As Now)", "Hind 500, as live.", "practical", mock(note=("Hind medium (500), as live now", "Names read firm against the titles"))),
  ("w400", "Regular Names", "Hind 400; the coloured titles stand out more.", "calm", mock({"fw": 400}, note=("Hind regular (400)", "Lighter names, titles lead"))))
P("Icon Style", "Card picture", "keep the two drawn icons in each card's box or show just one icon?",
  ("two", "Two Icons (As Now)", "Two of the site's drawn icons, overlapped.", "playful", mock(note=("Two drawn icons per group, as live now", "Furnace and AC share one box"))),
  ("one", "One Icon", "One centred icon per group, calmer box.", "calm", mock({"icons": "one"}, note=("One drawn icon per group", "Same box, one centred picture"))))
P("Icon Size", "Picture box size", "keep the 72px picture box or shrink it to 52px so the names get more room?",
  ("art72", "72px Box (As Now)", "Big picture box as live.", "playful", mock(note=("72px picture box, as live now", "Icons lead each card"))),
  ("art52", "52px Box", "Smaller box; names get 20px more width.", "practical", mock({"art": 52}, note=("52px picture box", "Names get about 20px more width"))))
P("Item Order", "Card order", "keep Heating & Cooling as the first card or lead with Water?",
  ("heat", "Heating & Cooling First", "As live: furnace and AC lead.", "calm", mock(note=("Heating & Cooling first, as live now", "Then Water, Air & Safety, Outside"))),
  ("water", "Water First", "Water heater and moisture scan lead.", "practical", mock({"order": (1, 0, 2, 3)}, note=("Water first", "Then Heating & Cooling, Air & Safety, Outside"))))
P("Tap Behaviour", "Tapping a service", "keep the arrow and pop-up sheet on each name or make the names a plain list with no tap?",
  ("sheet", "Opens Pop-Up (As Now)", "Arrow on each row; tap opens a short sheet.", "practical", mock(close="sheet", note=("Tap opens a short sheet, as live now", "Arrow shows it can be tapped"))),
  ("plain", "Plain List, No Tap", "No arrows; See All opens the full plan list.", "calm", mock({"tap": "none"}, note=("Plain list, no arrows", "See All still opens the plans"))))
P("Colour Pop", "Air & Safety colour", "keep the mustard title and box or switch them to jungle green?",
  ("mustard", "Mustard (As Now)", "As live: a warm yellow-brown title.", "playful", mock({"scroll": 2}, note=("Mustard title and box, as live now", "Shown swiped to Air & Safety"))),
  ("jungle", "Jungle Green", "Brand green, beside terracotta and lagoon.", "calm", mock({"scroll": 2, "safety": "j"}, note=("Jungle green title and box", "Uses only the three brand accents"))))
P("Line Length", "Long service name", "keep 'Mold and Moisture Scan' in full or shorten it to 'Moisture Scan' so the row stays short?",
  ("full", "Full Name (As Now)", "As live: Mold and Moisture Scan.", "practical", mock({"scroll": 1}, note=("Full name, as live now", "Shown swiped to Water"))),
  ("short", "Short Name", "Moisture Scan; same row, more space.", "calm", mock({"scroll": 1, "longname": False}, note=("Shorter: Moisture Scan", "Full name stays in the pop-up"))))
P("Section Heading", "See All link", "keep See All beside the section heading or move it under the cards?",
  ("right", "See All Beside (As Now)", "As live: small caps at the right.", "calm", mock(close="head", note=("See All beside the heading, as live now", "Heading and link on one line"))),
  ("under", "See All Under The Cards", "Heading alone; See All after the dots.", "practical", mock({"seeall": "under"}, close="head", note=("Heading alone", "See All sits under the dots"))))
assert len(pairs) == 10, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Compact polish of the restored What We Take Care Of section (smart-upkeep d49e1d8, the swipeable category carousel that was live before 8712223). Option A is always the live compact section; Option B is one small change. No new directions (Max via UpKeep, Oct 17 2026 21:09 ICT).",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "what-we-take-care-of-compact-polish",
        "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Max via UpKeep, Oct 17 2026 21:09 ICT: no new directions; the condensed What We Take Care Of section from before the last applied round, refined a little.",
        "follow_on_of": "upkeep-what-we-take-care-of-grid-and-home-map-deck",
        "sources": {"content": "tools/build_upkeep_wwtco_compact.py", "site": "WebermanApps/smart-upkeep d49e1d8 (app.js WW_CATS + wwCarousel, styles.css .ca-*)"}}, seed=10173, n=10)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "what-we-take-care-of-compact-polish-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
