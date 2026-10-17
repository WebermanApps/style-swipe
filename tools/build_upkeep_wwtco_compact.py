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
PLAN_OF = {"Furnace": "Essentials", "AC": "Essentials", "Furnace Filters": "Essentials", "Water Heater": "Essentials", "Mold and Moisture Scan": "Essentials",
           "Moisture Readings": "Essentials", "Smoke/CO": "Essentials", "Dryer Vent": "Essentials", "Gutters": "Plus", "Roof": "Complete", "Flashing": "Complete"}
PLAN_COL = {"Essentials": ("#0B6E4F", "#EAF3EE"), "Plus": ("#05668D", "#EDF4F7"), "Complete": ("#A8431F", "#FAF3EB")}
def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]
def c_flip(o):
    nm = "Heating & Cooling"; tc, bg = TINT["t"]; h = card_h(o)
    s = rect(.5, 2.5, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(0, 0, CW, h, bg, "#e5e0d8", 14, 1)
    s += T(12, 20, nm, 15, tc, "Khand", 700) + T(CW - 12, 19, "\u21ba Flip back", 9, MUTE, "Hind", 600, "end")
    y = 34
    for it, pl in WW_WI[nm]:
        s += T(12, y, ("Generator Service (If You Have One)" if it.startswith("Standby") else it), 10.4, INK, "Hind", 500) + T(CW - 12, y, pl, 8.6, PLAN_COL[pl][0], "Hind", 600, "end"); y += 15
    s += f'<line x1="12" y1="{y - 6}" x2="{CW - 12}" y2="{y - 6}" stroke="#e5d8c8"/>' + T(12, y + 7, VISITS, 9.4, MUTE, "Hind", 500)
    return s, CW, h + 4, "Tap the card: it flips in place, same size"
def c_acc(o):
    nm, ic, items, tint = cats(o)[0]; h0 = card_h(o); txt, tag = SVC["Furnace"]; extra = 50; h = h0 + extra
    s = rect(.5, 2.5, CW, h, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(0, 0, CW, h, "#FFFFFF", "#e5e0d8", 14, 1)
    g = card(0, 0, (nm, ic, items[:1], tint), dict(o, tap="none")); s += g.split("</text>", 1)[0].split('<rect', 3)[0]
    s += card(0, 0, (nm, ic, [items[0]], tint), dict(o, tap="none"))[len(rect(.5, 2.5, CW, h0, "#0A0A0A", "none", 14, 1, 'opacity=".05"') + rect(0, 0, CW, h0, "#FFFFFF", "#e5e0d8", 14, 1)):]
    bx = 9.6 + o["art"] + 9.6; y = 33 + o["rowh"]
    for i, l in enumerate(wrap(txt, 34)): s += T(bx, y + 12 + i * 12, l, 9.8, "#333333", "Hind", 400)
    s += rect(bx, y + 34, 58, 13, PLAN_COL["Essentials"][1], "none", 6.5) + T(bx + 29, y + 43.5, tag, 8.6, PLAN_COL["Essentials"][0], "Hind", 600, "middle")
    y += extra
    for it in items[1:]:
        s += f'<line x1="{bx}" y1="{y}" x2="{CW - 9.6}" y2="{y}" stroke="#f0ebe3"/>' + T(bx, y + o["rowh"] / 2 + 4.7, it, 13.1, INK) + T(CW - 9.6, y + o["rowh"] / 2 + 4.7, "+", 13, "#aaaaaa", "Hind", 400, "end"); y += o["rowh"]
    s = s.replace(T(bx, 33 + o["rowh"] / 2 + 4.7, "Furnace", 13.1, INK), T(bx, 33 + o["rowh"] / 2 + 4.7, "Furnace", 13.1, INK) + T(CW - 9.6, 33 + o["rowh"] / 2 + 4.7, "\u2212", 13, TERRA, "Hind", 600, "end"))
    return s, CW, h + 4, "Tap Furnace: the row opens inside the card"
def c_sheet(o):
    txt, tag = SVC["Furnace"]; H = 222
    s = rect(0, 0, 393, H, "#FFFFFF", "#e5e0d8", 16) + rect(176, 7, 40, 4, "#D6D0C6", "none", 2) + T(377, 30, "\u00d7", 22, INK, "Hind", 400, "end")
    s += rect(16, 20, 104, 78, "#F3EFE8", "none", 10) + icon("furnace", 44, 28, 48) + rect(22, 82, 60, 12, "#FFFFFF", "none", 6) + T(52, 91, "Example photo", 8, MUTE, "Hind", 600, "middle")
    s += T(132, 44, "Furnace", 26, INK, "Khand", 700) + rect(132, 54, 72, 18, PLAN_COL["Essentials"][1], "none", 9) + T(168, 67, tag, 11, PLAN_COL["Essentials"][0], "Hind", 600, "middle")
    rows = [("Tech checks", txt), ("How often", "Fall Furnace Tune-Up, every fall"), ("Which plan", "Essentials, Plus and Complete")]
    y = 114
    for k, v in rows:
        s += T(16, y, k.upper(), 10.5, MUTE, "Hind", 700, extra='letter-spacing=".8"')
        for i, l in enumerate(wrap(v, 38)): s += T(118, y + i * 16, l, 13.5, "#333333", "Hind", 400)
        y += 16 * len(wrap(v, 38)) + 6
    s += rect(16, H - 42, 361, 32, TERRA, "none", 8) + T(196.5, H - 21, "Free Quote in Minutes", 14, "#FFFFFF", "Hind", 600, "middle")
    return s, 393, H, "Tap Furnace: a sheet slides up from the bottom"
def c_pop(o):
    txt, tag = SVC["Furnace"]; g = card(0, 30, cats(o)[0], o); bx = 9.6 + o["art"] + 9.6
    s = g + f'<path d="M{bx + 20} {30 + 33 + 6} l6 -8 l6 8 z" fill="{INK}"/>'
    s = card(0, 62, cats(o)[0], o); py = 62 + 33 + o["rowh"] - 2
    s += rect(bx - 30, 2, 200, 58, INK, "none", 8) + f'<path d="M{bx + 14} 60 l6 7 l6 -7 z" fill="{INK}"/>'
    for i, l in enumerate(wrap(txt, 36)): s += T(bx - 22, 18 + i * 13, l, 10, "#FFFFFF", "Hind", 400)
    s += T(bx - 22, 52, tag, 9, "#F2C14E", "Hind", 600)
    return s, CW, 62 + card_h(o) + 4, "Tap Furnace: a small tip pops up above it"
def P2(g, el, sentence, a, b):
    """Max's own caption form for this round: 'Website: What We Take Care Of, <element>: <sentence>'."""
    _n[0] += 1; k = f"{_n[0]:02d}_"; ask = f"Website: What We Take Care Of, {el}: {sentence}"
    bad = [x for x in caption_rule.check(ask) if not x.startswith("vague location")]; assert not bad, (ask, bad)  # 'Website' label is Max's explicit wording (21:28 ICT)
    for x in (a, b): assert len(x[1]) <= 34 and len(x[2]) <= 62, x[:3]
    add(g, g, O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask)
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
P2("Card Tap", "card tap", "should tapping a card flip it to show its full service list and visit frequency, or expand the card in place like an accordion?",
  ("flip", "Card Flips Over", "Back shows every service, its plan and visits a year.", "playful", mock(close=c_flip, note=("Same card size; tap flips it", "Back lists all four Heating & Cooling services"))),
  ("accordion", "Card Opens Like An Accordion", "Tap a row; it opens in place with what it covers.", "practical", mock(close=c_acc, note=("Card grows while a row is open", "Text from the site's Furnace description"))))
P2("More Info", "more-info sheet", "should tapping a service open a bottom sheet with a photo, what the tech checks, how often and which plan includes it, or a small popover tip?",
  ("sheet", "Bottom Sheet With Details", "Photo (example), checks, how often and plan.", "practical", mock(close=c_sheet, note=("Bottom sheet, full width", "Photo shown is an example placeholder"))),
  ("tip", "Small Popover Tip", "One line and the plan, right over the row.", "calm", mock(close=c_pop, note=("Small tip above the row", "Closes on the next tap"))))
P2("Card Face", "fresh card face", "should each card get a soft tinted background, a fine line icon and a subtle hover lift, or stay the current flat white card?",
  ("flat", "Flat White Card (As Now)", "As live: white card, two filled icons.", "calm", mock(note=("Flat white card, as live now", "Same size: 282px wide on a phone"))),
  ("fresh", "Soft Tint, Line Icon, Lift", "Tinted card, thin line icon, lifts on hover.", "playful", mock({"face": "fresh"}, note=("Soft tint and fine line icon", "Same size; lifts a little on hover"))))
P2("Plan Tags", "plan tags", "should each service row carry a small Essentials, Plus or Complete chip, or stay without chips?",
  ("nochips", "No Chips (As Now)", "As live: names with a small arrow.", "calm", mock({"scroll": 3}, note=("No chips, as live now", "Shown swiped to Outside"))),
  ("chips", "Essentials / Plus / Complete Chips", "Each row shows the first plan that includes it.", "practical", mock({"scroll": 3, "chips": True}, note=("Plan chip on every row", "Plans as on the site's What's Included list"))))
P2("Motion", "motion", "should cards fade up gently as they scroll in, with an arrow nudge hint on phone, or stay static?",
  ("static", "Static (As Now)", "As live: cards sit still; dots show more.", "calm", mock(note=("Static, as live now", "Dots under the cards hint at more"))),
  ("motion", "Fade-Up And Arrow Nudge", "Cards rise in on scroll; arrow nudges once.", "playful", mock({"motion": True}, note=("Cards fade up as they scroll in", "Arrow nudges once on phone, then stops"))))
assert len(pairs) == 15, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
import draft_svg, trim_deck; draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = 15  # Max 21:28 ICT explicitly asked for 15 picks on this deck (one-deck override of R86)
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Compact polish of the restored What We Take Care Of section (smart-upkeep d49e1d8, the swipeable category carousel that was live before 8712223). Option A is always the live compact section; Option B is one small change. No new directions (Max via UpKeep, Oct 17 2026 21:09 ICT).",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "what-we-take-care-of-compact-polish",
        "deck_size": 15, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Max via UpKeep, Oct 17 2026 21:09 ICT: no new directions; the condensed What We Take Care Of section from before the last applied round, refined a little.",
        "update_2026_10_17_2128": "Max 21:28 ICT: keep the section size; make it look fresher and add a clickable more-info feature. Picks 11-15 added (card tap, more-info sheet, fresh card face, plan tags, motion). Content from app.js WW_WI, home() svc and TIER_NOTE; the sheet photo is an example.",
        "follow_on_of": "upkeep-what-we-take-care-of-grid-and-home-map-deck",
        "sources": {"content": "tools/build_upkeep_wwtco_compact.py", "site": "WebermanApps/smart-upkeep d49e1d8 (app.js WW_CATS + wwCarousel, styles.css .ca-*)"}}, seed=10173, n=15)
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
