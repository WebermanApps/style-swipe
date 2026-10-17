#!/usr/bin/env python3
"""What We Take Care Of: Card Colors And Finish (Branding, Oct 17 2026 22:15 ICT, replaces the submitted Fresh Look And More Info deck).
Max submitted Fresh Look And More Info at 21:58 ICT (01 skipped with note 'can they all be different color', 02-05 B, 06 both, 07 B, 08 B).
His 22:09 ICT correction overrides 02-05: NO tap-for-more-info anywhere (no flip, expand, sheet or i tip), rows stay a plain list,
spacing TIGHTER, See All under the cards. Never ask about spacing, tapping or more-info again.
Top-up (Branding, Oct 17 2026 ~23:50 ICT, AIR chase + R86): 2 more look-only picks (09 section background white vs warm cream band,
10 slide dots terracotta vs each card's own colour) so the deck has 10. Same id, same order for 01-08; nothing answered yet.
Option A in every pick = the section with every settled decision applied: tight rows (23.5px), plain non-tappable rows, See All under
the cards, plan chips on every row (07B), fade-up + arrow nudge (08B), two icons, 52px box, Water first, 'Moisture Scan', 14.5px regular
names, flat white face (UpKeep may add the line icon / hover lift; either is fine in A). B = one look change.
Content from smart-upkeep d49e1d8 app.js (WW_CATS, WW_WI plan per service) and styles.css tints; nothing invented.
Captions: 'Website: What We Take Care Of, <element>: <sentence>' (R105 form set by Max). Name by theme, no numbers (R113).
No Thai references (R110). Light only, Khand/Hind, no emoji. Page written UNLOCKED; lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from draft_svg import t, rect, ln, dot, screen, esc, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import deck, publish
import caption_rule
from split_deck import theme_name_ok
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
DID = "upkeep-what-we-take-care-of-card-colors-and-finish-deck"; NAME = "What We Take Care Of: Card Colors And Finish"
assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
PLAN_OF = {"Furnace": "Essentials", "AC": "Essentials", "Furnace Filters": "Essentials", "Water Heater": "Essentials", "Mold and Moisture Scan": "Essentials", "Moisture Scan": "Essentials",
           "Moisture Readings": "Essentials", "Smoke/CO": "Essentials", "Dryer Vent": "Essentials", "Gutters": "Plus", "Roof": "Complete", "Flashing": "Complete"}
PLAN_COL = {"Essentials": ("#0B6E4F", "#EAF3EE"), "Plus": ("#05668D", "#EDF4F7"), "Complete": ("#A8431F", "#FAF3EB")}
# Settled (Compact Polish 21:32 + Fresh Look 21:58 07B/08B + Max 22:09 correction): tight rows, plain rows, chips, motion, flat white.
D = dict(rowh=23.5, fs=14.5, fw=400, art=52, order=(1, 0, 2, 3), colors="mixed", face="flat", band=False, iconline=False,
         shadow="soft", seebtn="link", headbig=False, chip="soft", chips=True, motion=True, scroll=0, bg="white", dots="terra")
OWN = {"Heating & Cooling": "t", "Water": "l", "Air & Safety": "s", "Outside": "j"}   # every card its own palette colour
CW, GAP = 282, 9.6
def cats(o):
    out = []
    for i in o["order"]:
        nm, ic, items, tint = CATS[i]
        if o["colors"] == "own": tint = OWN[nm]
        items = [("Moisture Scan" if s == "Mold and Moisture Scan" else s) for s in items]
        out.append((nm, ic, items, tint))
    return out
def card_h(o): return round(9 + 24 + 3 * o["rowh"] + 9, 1)
def card(x, y, c, o):
    nm, ic, items, tint = c; tc, bg = TINT[tint]; h = card_h(o); a = o["art"]
    sh = ('opacity=".05"', 2.5) if o["shadow"] == "soft" else ('opacity=".13"', 7)
    s = rect(x + .5, y + sh[1], CW, h, "#0A0A0A", "none", 14, 1, sh[0])
    if o["face"] == "tint": s += rect(x, y, CW, h, bg, tc, 14, 1, 'stroke-opacity=".22"')
    else: s += rect(x, y, CW, h, "#FFFFFF", "#e5e0d8", 14, 1)
    if o["band"]: s += f'<path d="M{x} {y + 14} a14 14 0 0 1 14 -14 h{CW - 28} a14 14 0 0 1 14 14 v-8 h-{CW} z" fill="{tc}"/>'
    ax, ay = x + 9.6, y + 8.8 + (2 if o["band"] else 0)
    k = a / 72
    for nmi, dx, dy, sz in ((ic[0], 6, 8, 42), (ic[1], 30, 38, 36)):
        g = icon(nmi, ax + dx * k, ay + dy * k, sz * k)
        if o["iconline"]:
            g = re.sub(r'fill="#[0-9A-Fa-f]{6}" ', '', g).replace(f'stroke="{JUNGLE}" ', '').replace(f'stroke="{DARK}" stroke-width="2.1"', f'stroke="{tc}" stroke-width="1.4"', 1)
        s += g
    bx = ax + a + 9.6; bw = x + CW - 9.6 - bx
    s += T(bx, y + 26, nm, 17.3, tc, "Khand", 700)
    ry = y + 33
    for it in items:
        s += f'<line x1="{bx:.2f}" y1="{ry:.2f}" x2="{bx + bw:.2f}" y2="{ry:.2f}" stroke="#f0ebe3" stroke-width="1"/>'
        by = ry + o["rowh"] / 2 + o["fs"] * .36
        s += T(bx, by, it, o["fs"], INK, "Hind", o["fw"])
        if o["chips"]:
            pl = PLAN_OF.get(it, "Essentials"); cw = 6 + len(pl) * 4.6; pc = PLAN_COL[pl]
            if o["chip"] == "soft": s += rect(bx + bw - cw, by - 9.5, cw, 12, pc[1], "none", 6)
            else: s += rect(bx + bw - cw, by - 9.5, cw, 12, "#FFFFFF", pc[0], 6, 1)
            s += T(bx + bw - cw / 2, by - 1, pl, 7.6, pc[0], "Hind", 600, "middle")
        ry += o["rowh"]
    return s
def head(y, o):
    if o["headbig"]:
        return T(16, y + 18, "WHAT WE TAKE CARE OF", 11, TERRA, "Hind", 700, extra='letter-spacing="1.6"') + rect(16, y + 24, 28, 3, TERRA, "none", 1.5)
    return T(16, y + 20, "What We Take Care Of", 19.2, INK, "Khand", 700)
def section(o, y0=0):
    s = head(y0, o); y = y0 + 32; cs = cats(o)
    for i, c in enumerate(cs):
        x = 16 + (i - o["scroll"]) * (CW + GAP)
        if -CW < x < 393:
            if o["motion"] and i == o["scroll"] + 1:
                s += f'<g opacity=".45" transform="translate(0,14)">{card(x, y, c, o)}</g>'
            else: s += card(x, y, c, o)
    if o["motion"]:
        cy = y + card_h(o) / 2
        s += f'<circle cx="372" cy="{cy}" r="13" fill="#FFFFFF" stroke="{TERRA}" stroke-width="1.4"/>' + T(372, cy + 6, "\u203a", 20, TERRA, "Hind", 600, "middle")
        s += f'<path d="M352 {cy} h-10 M352 {cy - 5} h-6 M352 {cy + 5} h-6" stroke="{TERRA}" stroke-width="1.2" stroke-linecap="round" opacity=".6"/>'
    y += card_h(o) + 12
    xs = 196.5 - (14 + 3 * 5 + 3 * 4) / 2
    dotc = TINT[cs[o["scroll"]][3]][0] if o["dots"] == "card" else TERRA
    for i in range(4):
        on = i == o["scroll"]; w = 14 if on else 5
        s += rect(xs, y, w, 5, dotc if on else "#dddddd", "none", 2.5); xs += w + 4
    y += 15
    if o["seebtn"] == "link": s += T(196.5, y + 12, "See All", 13, LAGOON, "Hind", 600, "middle", 'text-decoration="underline"'); y += 16
    else: s += rect(196.5 - 52, y - 2, 104, 26, "#FFFFFF", LAGOON, 13, 1.4) + T(196.5, y + 15, "See All \u203a", 13, LAGOON, "Hind", 600, "middle"); y += 26
    if o["bg"] == "cream":   # full-width warm cream band behind the whole section (white page above and below)
        s = rect(0, y0 - 8, 393, y - y0 + 18, CREAM) + ln(y0 - 8, 0, 393, "#EFE8DC") + ln(y + 10, 0, 393, "#EFE8DC") + s
    return s, y - y0
def mock(over=None, note="", close="card"):
    o = dict(D, **(over or {})); K = 240 / 393
    s = rect(0, 0, 240, 26, CREAM) + t(12, 17, "SMARTUPKEEP.AI \u00b7 HOME", 8, INK, "hind", 700, extra='letter-spacing="1"') + t(228, 17, "Phone, 393 wide", 7.5, MUTE, anchor="end") + ln(26, 0, 240, LINE)
    body, h = section(o, 0)
    s += f'<g transform="translate(0,34) scale({K:.4f})">{body}</g>'
    yc = 34 + h * K + 12
    s += t(12, yc, "CLOSE-UP", 7.5, MUTE, "hind", 700, extra='letter-spacing="1.2"'); yc += 6
    if close == "card":
        Z = .8; g = card(0, 0, cats(o)[o["scroll"]], o); s += f'<g transform="translate({120 - CW * Z / 2:.2f},{yc:.2f}) scale({Z})">{g}</g>'; yc += (card_h(o) + 8) * Z
    elif close == "grid":   # all four cards, 2 x 2, so the colours can be compared
        cs = cats(o); Z = 226 / (2 * CW + GAP); g = ""
        if o["bg"] == "cream": s += rect(0, yc - 2, 240, (2 * card_h(o) + GAP) * Z + 8, CREAM)
        for i, c in enumerate(cs): g += card((i % 2) * (CW + GAP), (i // 2) * (card_h(o) + GAP), c, o)
        s += f'<g transform="translate({120 - (2 * CW + GAP) * Z / 2:.2f},{yc:.2f}) scale({Z:.4f})">{g}</g>'; yc += (2 * card_h(o) + GAP + 8) * Z
    elif close == "foot":
        body2, h2 = section(o, 0); vx, vy, vw, vh = (70, h2 - 70, 253, 75)
        s += f'<svg x="8" y="{yc:.2f}" width="224" height="{224 * vh / vw:.2f}" viewBox="{vx} {vy} {vw} {vh}">{body2}</svg>'; yc += 224 * vh / vw
    elif close == "head":
        body2, h2 = section(o, 0); vx, vy, vw, vh = (0, 0, 253, 60)
        s += f'<svg x="8" y="{yc:.2f}" width="224" height="{224 * vh / vw:.2f}" viewBox="{vx} {vy} {vw} {vh}">{body2}</svg>'; yc += 224 * vh / vw
    if note:
        yn = max(yc + 18, 262)
        s += rect(12, yn - 10, 3, 24, TERRA) + t(20, yn, note[0], 8.5, INK, "hind", 600) + (t(20, yn + 12, note[1], 7.8, MUTE) if len(note) > 1 else "")
    return screen(s)
def P2(g, el, sentence, a, b, purpose="new"):
    _n[0] += 1; k = f"{_n[0]:02d}_"; ask = f"Website: What We Take Care Of, {el}: {sentence}"
    bad = [x for x in caption_rule.check(ask) if not x.startswith("vague location")]; assert not bad, (ask, bad)
    low = ask.lower(); assert not any(w in low for w in ("spacing", "tap", "more info", "more-info", "flip", "expand", "sheet")), ask  # Max 22:09: never re-ask
    for x in (a, b): assert len(x[1]) <= 34 and len(x[2]) <= 62, x[:3]
    add(g, g, O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask, purpose=purpose)
pairs, O, add = deck("wwcf_", "UpKeep")
_n = [0]
OWNC = {"colors": "own"}
P2("Card Colours", "card colours", "should every card get its own colour from the palette (terracotta, lagoon, mustard, jungle green), or keep the current mixed set?",
  ("mixed", "Current Mixed Set", "Two terracotta cards, one lagoon, one mustard.", "calm", mock(close="grid", note=("Current colours, settled picks applied", "Heating and Outside share terracotta"))),
  ("own", "Every Card Its Own Colour", "Water lagoon, Heating terracotta, Air mustard, Outside jungle.", "playful", mock(OWNC, close="grid", note=("One palette colour per card", "Soft brand tones, never neon"))), purpose="reask")
P2("Card Face", "card face", "you liked both, so with every card in its own colour should the face stay flat white with a coloured accent, or take a soft tint?",
  ("flat", "Flat White, Coloured Accent", "White card; colour on the name and icons.", "calm", mock(OWNC, close="grid", note=("Flat white face", "Colour carried by the name and icons"))),
  ("tint", "Soft Tint Face", "Whole card washed in its own light colour.", "playful", mock(dict(OWNC, face="tint"), close="grid", note=("Soft tint in each card's colour", "Same size and layout"))))
P2("Colour Strength", "colour strength", "should each card's colour stay on just the name and icons, or also run as a thin band across the top of the card?",
  ("icon", "Name And Icons Only", "Colour on the title and drawn icons.", "calm", mock(OWNC, note=("Colour on the name and icons", "Shown on the Water card"))),
  ("band", "Thin Colour Band On Top", "A slim band in the card's colour along the top.", "practical", mock(dict(OWNC, band=True), note=("Slim colour band on top", "Rest of the card unchanged"))))
P2("Icon Style", "icon style", "should the two icons keep their coloured fills, or be drawn as fine single-colour lines in the card's own colour?",
  ("fill", "Coloured Fills (As Now)", "Two icons with terracotta, lagoon and mustard fills.", "playful", mock(OWNC, note=("Two icons with colour fills", "52px box, as picked"))),
  ("line", "Fine Line Icons", "Two icons as thin lines in the card colour.", "calm", mock(dict(OWNC, iconline=True), note=("Two fine line icons", "Drawn in the card's own colour"))))
P2("Card Shadow", "card shadow", "should the cards keep the faint soft shadow, or sit a little higher with a deeper shadow?",
  ("soft", "Faint Soft Shadow (As Now)", "Cards sit almost flat on the page.", "calm", mock(OWNC, note=("Faint shadow, as now", "Almost flat on the white page"))),
  ("deep", "Deeper Lifted Shadow", "Cards float a little above the page.", "playful", mock(dict(OWNC, shadow="deep"), note=("Deeper shadow", "Cards look lifted off the page"))))
P2("See All Button", "See All button", "should See All under the cards stay an underlined text link, or become an outlined pill button?",
  ("link", "Underlined Link (As Now)", "Lagoon text link under the dots.", "calm", mock(OWNC, close="foot", note=("Underlined text link", "Under the cards, as picked"))),
  ("pill", "Outlined Pill Button", "Lagoon outline pill with an arrow.", "practical", mock(dict(OWNC, seebtn="pill"), close="foot", note=("Outlined pill button", "Same place under the cards"))))
P2("Section Header", "section header", "should the heading stay the bold Khand title, or become a small spaced capitals label with a short terracotta line?",
  ("khand", "Bold Khand Title (As Now)", "What We Take Care Of in bold Khand.", "calm", mock(OWNC, close="head", note=("Bold Khand title, as now", "Ink colour, 19px"))),
  ("label", "Small Capitals Label", "Spaced terracotta capitals with a short line.", "practical", mock(dict(OWNC, headbig=True), close="head", note=("Small spaced capitals label", "Short terracotta line under it"))))
P2("Plan Chip Style", "plan chip style", "should the Essentials, Plus and Complete chips stay soft filled pills, or become outlined chips on white?",
  ("soft", "Soft Filled Chips (As Picked)", "Light green, blue and terracotta pills.", "calm", mock(OWNC, note=("Soft filled plan chips", "Plans as on the site's What's Included list"))),
  ("outline", "Outlined Chips", "White chips with a thin plan-colour outline.", "practical", mock(dict(OWNC, chip="outline"), note=("Outlined plan chips", "Same plans, lighter look"))))
P2("Section Background", "section background", "should the section sit on the plain white page, or on a warm cream band that runs the full width behind the cards?",
  ("white", "Plain White Page (As Now)", "White cards on the white page.", "calm", mock(OWNC, close="grid", note=("White page behind the cards", "Cards marked by their thin outline"))),
  ("cream", "Warm Cream Band", "A full-width warm cream band behind the cards.", "practical", mock(dict(OWNC, bg="cream"), close="grid", note=("Warm cream band behind the section", "White cards stand out on the cream"))))
P2("Slide Dots", "slide dots", "should the active dot under the cards stay terracotta, or take the colour of the card you are on?",
  ("terra", "Terracotta Dot (As Now)", "The active dot is always terracotta.", "calm", mock(OWNC, close="foot", note=("Terracotta active dot", "Same on every card"))),
  ("card", "Dot In The Card's Colour", "The active dot matches the card in view.", "playful", mock(dict(OWNC, dots="card"), close="foot", note=("Active dot in the card's own colour", "Lagoon here, on the Water card"))))
assert len(pairs) == 10, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Card colours and finish for the compact What We Take Care Of section. Option A is always the section with every settled pick applied (tight rows, plain non-tappable rows, plan chips, fade-up and arrow nudge, See All under the cards, flat white face); Option B one look change at the same size.",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon, jungle and mustard accents, Khand and Hind, light mode only."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "what-we-take-care-of-card-colors-and-finish",
        "deck_size": 10, "topped_up": "2026-10-17: 8 -> 10 picks (R86; AIR chase), picks 09-10 added, 01-08 unchanged", "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Max Oct 17 2026 21:58 ICT note on Fresh Look 01: 'can they all be different color'; 06 both (flat white and soft tint). 22:09 ICT correction: no tap-for-more-info, plain rows, tighter spacing, See All under the cards.",
        "replaces": "upkeep-what-we-take-care-of-fresh-look-and-more-info-deck", "follow_on_of": "upkeep-what-we-take-care-of-fresh-look-and-more-info-deck",
        "applied_picks": "Compact Polish 21:32 (2B 14.5px, 3B regular, 4A two icons, 5B 52px, 6B Water first, 7B plain rows, 9B Moisture Scan, 10B See All under) + Fresh Look 21:58 (07B plan chips, 08B fade-up and arrow nudge) + Max 22:09 correction (tight rows, no tap-for-more-info anywhere); face flat white for now",
        "sources": {"content": "tools/build_upkeep_wwtco_colors.py", "site": "WebermanApps/smart-upkeep d49e1d8 app.js (WW_CATS, WW_WI plans), styles.css .ca-* tints"}}, seed=10175, n=10, first=0)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
dj["pairs"][0]["carried_from"] = "upkeep-what-we-take-care-of-fresh-look-and-more-info-deck-01"
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "what-we-take-care-of-card-colors-and-finish-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
