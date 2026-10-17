#!/usr/bin/env python3
"""What We Take Care Of: Fresh Look And More Info (Branding, Oct 17 2026 21:38 ICT, replaces the submitted Compact Polish deck).
Option A in every pick = the compact section with Max's 21:32 ICT Compact Polish picks applied (rows 4px taller, 14.5px regular names,
two icons in a 52px box, Water first, plain rows with no tap, 'Moisture Scan', See All under the cards; Air & Safety colour re-asked first).
Because rows stay plain (no tap), every clickable idea sits at the CARD level. Same section size: 282px cards, 4 categories, phone swipe,
2 across at 601px, 4 at 1000px. Content from smart-upkeep d49e1d8 app.js (WW_CATS, WW_WI, home() svc, TIER_NOTE); the photo is an example.
--- original notes of the Compact Polish builder this was forked from:
What We Take Care Of: Compact Polish (Branding, Oct 17 2026, for UpKeep).
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
DID = "upkeep-what-we-take-care-of-fresh-look-and-more-info-deck"; NAME = "What We Take Care Of: Fresh Look And More Info"
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
D = dict(rowh=27.5, fs=14.5, fw=400, icons="two", art=52, order=(1, 0, 2, 3), tap="none", safety="s", longname=False, seeall="under", scroll=0)  # Max 21:32 picks
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
    fresh = o.get("face") == "fresh"
    if fresh:
        s = rect(x + .5, y + 6, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".08"') + rect(x, y, CW, h, bg, tc, 14, 1, 'stroke-opacity=".22"')
    else:
        s = rect(x + .5, y + 2.5, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(x, y, CW, h, "#FFFFFF", "#e5e0d8", 14, 1)
    ax, ay, ah = x + 9.6, y + 8.8, h - 17.6
    if fresh:
        s += rect(ax, ay, a, ah, "#FFFFFF", tc, 10, 1, 'stroke-opacity=".25"')
        sz = a * .62; s += icon(ic[0], ax + (a - sz) / 2, ay + (ah - sz) / 2, sz).replace('stroke-width="2.1"', f'stroke-width="1.2" stroke="{tc}"', 1).replace(f'stroke="{DARK}" ', '', 1)
    elif o["icons"] == "two":
        k = a / 72; s += icon(ic[0], ax + 6 * k, ay + 8 * k, 42 * k) + icon(ic[1], ax + 30 * k, ay + 38 * k, 36 * k)
    else:
        sz = a * .7; s += icon(ic[0], ax + (a - sz) / 2, ay + (ah - sz) / 2, sz)
    bx = ax + a + 9.6; bw = x + CW - 9.6 - bx
    s += T(bx, y + 26, nm, 17.3, tc, "Khand", 700)
    if o.get("more") == "link": s += T(x + CW - 12, y + 25, "More \u203a", 11.5, LAGOON, "Hind", 600, "end")
    if o.get("more") == "flip": s += T(x + CW - 12, y + 25, "\u21bb", 14, LAGOON, "Hind", 600, "end")
    if o.get("more") == "expand": s += T(x + CW - 12, y + 25, "\u2304", 14, LAGOON, "Hind", 600, "end")
    if o.get("more") == "info": s += f'<circle cx="{x + CW - 18}" cy="{y + 20}" r="7" fill="none" stroke="{LAGOON}" stroke-width="1.3"/>' + T(x + CW - 18, y + 24, "i", 10, LAGOON, "Hind", 700, "middle")
    ry = y + 33
    for it in items:
        s += f'<line x1="{bx:.2f}" y1="{ry:.2f}" x2="{bx + bw:.2f}" y2="{ry:.2f}" stroke="#f0ebe3" stroke-width="1"/>'
        by = ry + o["rowh"] / 2 + o["fs"] * .36
        s += T(bx, by, it, o["fs"], INK, "Hind", o["fw"])
        if o.get("chips"):
            pl = PLAN_OF.get(it, "Essentials"); cw = 6 + len(pl) * 4.6; pc = PLAN_COL[pl]
            s += rect(bx + bw - cw, by - 9.5, cw, 12, pc[1], "none", 6) + T(bx + bw - cw / 2, by - 1, pl, 7.6, pc[0], "Hind", 600, "middle")
        elif o["tap"] == "sheet": s += T(bx + bw, by, "\u203a", 14, "#aaaaaa", "Hind", 400, "end")
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
        if -CW < x < 393:
            if o.get("motion") and i == 1:
                s += f'<g opacity=".45" transform="translate(0,14)">{card(x, y, c, o)}</g>'
                for k in range(3): s += f'<line x1="{x + 30 + k * 40}" y1="{y + card_h(o) + 22}" x2="{x + 30 + k * 40}" y2="{y + card_h(o) + 8}" stroke="{LAGOON}" stroke-width="1.4" stroke-dasharray="2 3"/>'
            else: s += card(x, y, c, o)
    if o.get("motion"):
        cy = y + card_h(o) / 2
        s += f'<circle cx="372" cy="{cy}" r="13" fill="#FFFFFF" stroke="{TERRA}" stroke-width="1.4"/>' + T(372, cy + 6, "\u203a", 20, TERRA, "Hind", 600, "middle")
        s += f'<path d="M352 {cy} h-10 M352 {cy - 5} h-6 M352 {cy + 5} h-6" stroke="{TERRA}" stroke-width="1.2" stroke-linecap="round" opacity=".6"/>'
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
    elif callable(close):
        g, gw, gh, cap = close(o)
        if cap: s += t(120, yc + 8, cap, 7.6, MUTE, anchor="middle"); yc += 13
        Z = min(224 / gw, (256 - yc) / gh); s += f'<g transform="translate({120 - gw * Z / 2:.2f},{yc:.2f}) scale({Z:.4f})">{g}</g>'; yc += gh * Z
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
# ---- Oct 17 2026 21:28 ICT add-on (Max: "keep the sizing ... doesn't look fresh ... some clickable feature where i get more info") ----
# Real data only, from smart-upkeep d49e1d8 app.js: WW_WI (full service lists + plan per service, visits per plan),
# home() svc list (one-line description + tier) and TIER_NOTE. Anything not in the source is labelled "example".
WW_WI = {"Heating & Cooling": [("Fall Furnace Tune-Up", "Essentials"), ("Spring AC Tune-Up", "Essentials"), ("Furnace Filters Changed During Visits", "Essentials"), ("Standby Generator Service (If You Have One)", "Complete")],
         "Water": [("Water Heater Flush or Tankless Descale", "Essentials"), ("Water Softener Salt Top-Off", "Plus"), ("Fridge Water Filter Changes", "Plus")],
         "Air & Safety": [("Dryer Vent Cleaning", "Essentials"), ("Smoke and CO Detector Checks", "Essentials"), ("GFCI and Shut-Off Valve Checks", "Plus")],
         "Outside": [("Gutter and Downspout Cleaning", "Plus"), ("Garage Door Lube and Weatherproofing", "Plus"), ("Roof and Flashing Inspection", "Complete"), ("Ice Dam Clearing After Storms", "Complete"), ("Pre and Post Storm Checks", "Complete")]}
VISITS = "Visits: 2 a year (Essentials), 4 (Plus), 12 (Complete)"
SVC = {"Furnace": ("Fall tune-up on every furnace, with filter changes during visits.", "Every Plan")}
WSVC = [("Water Heater", "Yearly flush, or descale for tankless, to cut sediment and extend its life.", "Every Plan"), ("Moisture Scan", "Scanning your entire home every visit to protect against mold and water damage.", "Every Plan"), ("Gutters", "Gutters and downspouts cleaned every spring and fall.", "Plus and Up")]
PLAN_OF = {"Furnace": "Essentials", "AC": "Essentials", "Furnace Filters": "Essentials", "Water Heater": "Essentials", "Mold and Moisture Scan": "Essentials", "Moisture Scan": "Essentials",
           "Moisture Readings": "Essentials", "Smoke/CO": "Essentials", "Dryer Vent": "Essentials", "Gutters": "Plus", "Roof": "Complete", "Flashing": "Complete"}
PLAN_COL = {"Essentials": ("#0B6E4F", "#EAF3EE"), "Plus": ("#05668D", "#EDF4F7"), "Complete": ("#A8431F", "#FAF3EB")}
def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]
def _shell(h, bg="#FFFFFF"):
    return rect(.5, 2.5, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(0, 0, CW, h, bg, "#e5e0d8", 14, 1)
def c_flip(o):
    nm = "Water"; tc, bg = TINT["l"]; h = card_h(o); s = _shell(h, bg)
    s += T(12, 22, nm, 16, tc, "Khand", 700) + T(CW - 12, 21, "\u21bb Flip back", 9.5, MUTE, "Hind", 600, "end"); y = 42
    for it, pl in WW_WI[nm]:
        s += T(12, y, it, 11.4, INK, "Hind", 500) + T(CW - 12, y, pl, 9.2, PLAN_COL[pl][0], "Hind", 600, "end"); y += 19
    s += f'<line x1="12" y1="{y - 7}" x2="{CW - 12}" y2="{y - 7}" stroke="#d5e3ea"/>' + T(12, y + 9, VISITS, 9.6, MUTE, "Hind", 500)
    return s, CW, h + 4, "Tap the Water card: it flips, same size"
def c_expand(o):
    nm, ic, items, tint = cats(o)[0]; h0 = card_h(o); extra = 74; h = h0 + extra
    s = _shell(h) + card(0, 0, (nm, ic, items, tint), dict(o, more="expand"))[len(_shell(h0)):]
    y = h0 - 4; s += f'<line x1="12" y1="{y}" x2="{CW - 12}" y2="{y}" stroke="#f0ebe3"/>'
    for it, txt, tag in WSVC:
        s += T(12, y + 16, it, 10.5, INK, "Hind", 600) + T(CW - 12, y + 16, tag, 8.6, PLAN_COL["Plus" if tag.startswith("Plus") else "Essentials"][0], "Hind", 600, "end")
        s += T(12, y + 28, wrap(txt, 52)[0] + (" ..." if len(wrap(txt, 52)) > 1 else ""), 8.8, "#555555", "Hind", 400); y += 26
    return s, CW, h + 4, "Tap the Water card: it opens downward in place"
def c_sheet(o):
    H = 300
    s = rect(0, 0, 393, H, "#FFFFFF", "#e5e0d8", 16) + rect(176, 7, 40, 4, "#D6D0C6", "none", 2) + T(377, 30, "\u00d7", 22, INK, "Hind", 400, "end")
    s += rect(16, 20, 104, 74, "#EDF4F7", "none", 10) + icon("waterheater", 44, 26, 46) + rect(22, 78, 60, 12, "#FFFFFF", "none", 6) + T(52, 87, "Example photo", 8, MUTE, "Hind", 600, "middle")
    s += T(132, 44, "Water", 26, INK, "Khand", 700) + T(132, 64, "Less sediment, longer life", 12.5, MUTE, "Hind", 400)
    y = 114; s += T(16, y, "WHAT THE TECH CHECKS", 10, MUTE, "Hind", 700, extra='letter-spacing=".8"'); y += 18
    for it, txt, tag in WSVC:
        pc = PLAN_COL["Plus" if tag.startswith("Plus") else "Essentials"]
        s += T(16, y, it, 13, INK, "Hind", 600) + rect(377 - 66, y - 11, 66, 15, pc[1], "none", 7.5) + T(377 - 33, y, tag, 9.5, pc[0], "Hind", 600, "middle")
        s += T(16, y + 15, wrap(txt, 58)[0], 11, "#444444", "Hind", 400) + (T(16, y + 28, " ".join(wrap(txt, 58)[1:]), 11, "#444444", "Hind", 400) if len(wrap(txt, 58)) > 1 else ""); y += 40
    s += T(16, y - 4, "HOW OFTEN  " + VISITS[len("Visits: "):], 9.5, MUTE, "Hind", 600)
    s += rect(16, H - 40, 361, 30, TERRA, "none", 8) + T(196.5, H - 20, "Free Quote in Minutes", 14, "#FFFFFF", "Hind", 600, "middle")
    return s, 393, H, "Tap More on the Water card: a sheet slides up"
def c_tip(o):
    s = card(0, 66, cats(o)[0], dict(o, more="info")); x0 = CW - 212
    s += rect(x0, 0, 206, 60, INK, "none", 8) + f'<path d="M{CW - 24} 60 l6 6 l6 -6 z" fill="{INK}"/>'
    s += T(x0 + 10, 18, "Water: 3 services on this card", 10.5, "#FFFFFF", "Hind", 600) + T(x0 + 10, 33, "Water Heater, Moisture Scan: every plan", 9.6, "#FFFFFF", "Hind", 400) + T(x0 + 10, 47, "Gutters: Plus and up", 9.6, "#F2C14E", "Hind", 600)
    return s, CW, 66 + card_h(o) + 4, "Tap the i on the Water card: a small tip pops up"
def P2(g, el, sentence, a, b):
    """Caption form set by Max/parent: 'Website: What We Take Care Of, <element>: <sentence>'."""
    _n[0] += 1; k = f"{_n[0]:02d}_"; ask = f"Website: What We Take Care Of, {el}: {sentence}"
    bad = [x for x in caption_rule.check(ask) if not x.startswith("vague location")]; assert not bad, (ask, bad)  # 'Website' label is Max's explicit wording (21:28 ICT)
    for x in (a, b): assert len(x[1]) <= 34 and len(x[2]) <= 62, x[:3]
    add(g, g, O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask)
pairs, O, add = deck("wwfl_", "UpKeep")
_n = [0]
AS = ("As Picked (Rows Stay Plain)",)
P2("Colour Re-Ask", "Air & Safety card colour", "mustard yellow (warmer, stands out) or jungle green (calmer, sits closer to the brand greens), shown in the whole section?",
  ("mustard", "Mustard Yellow", "Warmer; stands out next to Water and Heating.", "playful", mock({"scroll": 2}, note=("Mustard yellow title and box", "Swiped to Air & Safety; asked again (skipped)"))),
  ("jungle", "Jungle Green", "Calmer; only brand accents in the row.", "calm", mock({"scroll": 2, "safety": "j"}, note=("Jungle green title and box", "Swiped to Air & Safety; same size"))))
P2("Card Flip", "whole-card flip", "rows stay plain as you picked, so should tapping the whole card flip it to show every service, its plan and visits a year, or keep the card as it is?",
  ("asis", "Card As Picked", "Plain rows, no tap; See All under the cards.", "calm", mock(note=("Your picks applied, no tap", "Water first, 52px box, 14.5px names"))),
  ("flip", "Whole Card Flips", "Flip icon on the card; back lists all services.", "playful", mock({"more": "flip"}, close=c_flip, note=("Tap anywhere on the card to flip", "Rows stay plain; the card is the button"))))
P2("Card Expand", "whole-card expand", "rows stay plain as you picked, so should tapping the whole card open it downward with a one-line note per service, or keep the card as it is?",
  ("asis", "Card As Picked", "Plain rows, no tap; same size.", "calm", mock(note=("Your picks applied, no tap", "Card stays the same height"))),
  ("expand", "Whole Card Opens Down", "Card grows to show what each service covers.", "practical", mock({"more": "expand"}, close=c_expand, note=("Card grows while it is open", "Notes from the site's service descriptions"))))
P2("More Sheet", "card-level More sheet", "rows stay plain as you picked, so should each card get a small More link that opens a bottom sheet with a photo, what the tech checks, how often and which plan, or stay without it?",
  ("asis", "No More Link (As Picked)", "Cards as picked; See All opens the plans.", "calm", mock(note=("Your picks applied", "See All under the cards"))),
  ("sheet", "More Link Opens A Sheet", "Photo (example), checks, plan and visits.", "practical", mock({"more": "link"}, close=c_sheet, note=("More on each card, not on rows", "Photo shown is an example placeholder"))))
P2("Info Tip", "card-level info tip", "rows stay plain as you picked, so should each card get a small i that pops up a short tip about its services and plans, or stay without it?",
  ("asis", "No Tip (As Picked)", "Cards as picked, nothing to tap.", "calm", mock(note=("Your picks applied", "Nothing on the card is tappable"))),
  ("tip", "Small i With A Tip", "One tap shows services and plans in brief.", "practical", mock({"more": "info"}, close=c_tip, note=("Small i at the card's top right", "Tip closes on the next tap"))))
P2("Card Face", "fresh card face", "should each card get a soft tinted background, a fine line icon and a subtle hover lift, or stay the flat white card you picked?",
  ("flat", "Flat White Card (As Picked)", "White card with two drawn icons.", "calm", mock(note=("Flat white card, as picked", "282px wide on a phone"))),
  ("fresh", "Soft Tint, Line Icon, Lift", "Tinted card, thin line icon, lifts on hover.", "playful", mock({"face": "fresh"}, note=("Soft tint and fine line icon", "Same size; lifts a little on hover"))))
P2("Plan Tags", "plan tags", "should each plain service row carry a small Essentials, Plus or Complete chip (not tappable), or stay without chips?",
  ("nochips", "No Chips (As Picked)", "Plain names only.", "calm", mock({"scroll": 3}, note=("No chips, as picked", "Shown swiped to Outside"))),
  ("chips", "Essentials / Plus / Complete Chips", "Each row shows the first plan that includes it.", "practical", mock({"scroll": 3, "chips": True}, note=("Plan chip on every row", "Plans as on the site's What's Included list"))))
P2("Motion", "motion", "should cards fade up gently as they scroll in, with an arrow nudge hint on phone, or stay static?",
  ("static", "Static (As Picked)", "Cards sit still; dots show more.", "calm", mock(note=("Static, as picked", "Dots under the cards hint at more"))),
  ("motion", "Fade-Up And Arrow Nudge", "Cards rise in on scroll; arrow nudges once.", "playful", mock({"motion": True}, note=("Cards fade up as they scroll in", "Arrow nudges once on phone, then stops"))))
assert len(pairs) == 8, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Fresh look and card-level more-info for the compact What We Take Care Of section. Option A is always the section with Max's Compact Polish picks (submitted Oct 17 2026 21:32 ICT) applied; Option B one fresher or clickable change at the same size. Rows stay plain (his pick 7), so every tap target is the card.",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon, jungle and mustard accents, Khand and Hind, light mode only."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "what-we-take-care-of-fresh-look-and-more-info",
        "deck_size": 8, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Max Oct 17 2026 21:28 ICT: 'i like the sizing of the section we have now i just think it doesn't look fresh. maybe there is some clickable feature where i get more info.' Built as a replacement deck after he submitted Compact Polish at 21:32 ICT.",
        "replaces": "upkeep-what-we-take-care-of-compact-polish-deck", "follow_on_of": "upkeep-what-we-take-care-of-compact-polish-deck",
        "applied_picks": "Compact Polish 21:32 ICT: 1B more row room, 2B 14.5px names, 3B regular weight, 4A two icons, 5B 52px box, 6B Water first, 7B plain list no tap, 8 skipped (re-asked first here), 9B Moisture Scan, 10B See All under the cards",
        "sources": {"content": "tools/build_upkeep_wwtco_fresh.py", "site": "WebermanApps/smart-upkeep d49e1d8 app.js (WW_CATS, WW_WI, home() svc, TIER_NOTE), styles.css .ca-*; sheet photo is an example"}}, seed=10174, n=8, first=1)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "what-we-take-care-of-fresh-look-and-more-info-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
