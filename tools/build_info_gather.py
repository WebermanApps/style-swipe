#!/usr/bin/env python3
"""Build Style Swipe deck info-gather (Oct 14 2026): Info Gather Deck, 20 pairs on stage 4 of Max's funnel
(Marketing, Video/Catch, Home Page, Info Gather, Price Offer, Make The Sale): the smartupkeep Get Started intake,
one question per screen (zip, home size, furnace, AC, water heater + type, stories, extras), tags, progress, tiles,
illustrations, home/back, resume and the 'Your Price Is Ready' handoff. Screens: /workspace/smartkeep/updates-oct14/live/393-04..12*.png.
Pattern copied from build_upkeep_board.py (team_kit.publish, dash_kit helpers). UpKeep brand rules applied: 'Your Licensed Tech',
plans Essentials/Plus/Complete, no byline. Drawn SVG mockups of the real flow, example answers only. Submit -> agent 'upkeep'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, ic, W, H
from dash_kit import R, T, L, D, chev, phone
DID = "info-gather"
B = dict(name="smartupkeep", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5DCCB", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
INK, MUTE, LN = B["ink"], B["mute"], B["line"]; ACC = B["acc"]
pairs, O, add = deck("ig_", "UpKeep")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
# ---------- drawn illustrations (24-unit grid) ----------
ILL = {"house": '<path d="M3 11 L12 4 L21 11 V20 H3 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/><rect x="10" y="14" width="4" height="6" fill="{c}"/>',
       "furnace": '<rect x="6" y="3" width="12" height="18" rx="1.5" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M8 7 H16 M8 9.5 H16" stroke="{c}" stroke-width="1.4"/><path d="M12 13 Q14 15.5 12 18 Q10 15.5 12 13 Z" fill="' + TERRA + '"/>',
       "ac": '<rect x="3" y="6" width="18" height="13" rx="1.5" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="11" cy="12.5" r="4" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M11 9 V16 M7.5 12.5 H14.5" stroke="{c}" stroke-width="1.4"/><path d="M17 9 V16" stroke="{c}" stroke-width="1.4"/>',
       "water": '<rect x="7" y="3" width="10" height="18" rx="5" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M12 9 Q14.5 12 12 15 Q9.5 12 12 9 Z" fill="' + LAGOON + '"/>',
       "tankless": '<rect x="6" y="5" width="12" height="12" rx="1.5" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M9 17 V21 M15 17 V21" stroke="{c}" stroke-width="1.6"/><path d="M12 8 Q14 10.5 12 13 Q10 10.5 12 8 Z" fill="' + LAGOON + '"/>',
       "stories": '<path d="M5 21 V9 L12 3 L19 9 V21 Z M5 15 H19" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
       "size": '<path d="M4 4 H20 V20 H4 Z M4 4 L9 9 M20 20 L15 15" fill="none" stroke="{c}" stroke-width="1.8"/>',
       "pin": '<path d="M12 21 Q5 13 5 9 A7 7 0 0 1 19 9 Q19 13 12 21 Z" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="12" cy="9" r="2.5" fill="{c}"/>',
       "camera": '<rect x="3" y="7" width="18" height="13" rx="2" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M8 7 L10 4 H14 L16 7" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="12" cy="13.5" r="3.5" fill="none" stroke="{c}" stroke-width="1.8"/>',
       "drop": '<path d="M12 3 Q19 11 19 15 A7 7 0 0 1 5 15 Q5 11 12 3 Z" fill="none" stroke="{c}" stroke-width="1.8"/>',
       "dryer": '<rect x="4" y="3" width="16" height="18" rx="2" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="12" cy="13" r="4.5" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="8" cy="6.5" r="1" fill="{c}"/>',
       "bolt": '<path d="M13 2 L5 13 H11 L10 22 L19 10 H13 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
       "shield": '<path d="M12 3 L20 6 V12 Q20 18 12 21 Q4 18 4 12 V6 Z" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M8.5 12 L11 14.5 L15.5 9.5" fill="none" stroke="{c}" stroke-width="1.8"/>',
       "clock": '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M12 7 V12 L15 14" fill="none" stroke="{c}" stroke-width="1.8"/>',
       "list": '<rect x="5" y="3" width="14" height="18" rx="2" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M8 8 H16 M8 12 H16 M8 16 H13" stroke="{c}" stroke-width="1.6"/>',
       "fridge": '<rect x="6" y="2" width="12" height="20" rx="2" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M6 9 H18 M9 5 V7 M9 12 V15" stroke="{c}" stroke-width="1.6"/>',
       "sump": '<path d="M4 9 H20 V20 H4 Z" fill="none" stroke="{c}" stroke-width="1.8"/><path d="M12 9 V3 M9 5 H15" stroke="{c}" stroke-width="1.6"/><path d="M7 16 Q12 13 17 16" fill="none" stroke="' + LAGOON + '" stroke-width="1.6"/>'}
def il(k, x, y, s=16, c=INK): return f'<g transform="translate({x},{y}) scale({s/24})">' + ILL[k].replace("{c}", c) + '</g>'
def blob(k, cx, cy, r, c, ic_c=INK): return D(cx, cy, r, c + "22") + il(k, cx - r * .62, cy - r * .62, r * 1.24, ic_c)
# ---------- intake screen ----------
def scr(step=3, total=7, title="How Many Furnaces?", sub="Most homes over 3,500 sq ft have two.", art="furnace", body=None, prog="bar",
        head="side", tags="none", foot="skip", nav="top", plan=True, extra=""):
    s = T(B, 120, 15, "smartupkeep", 12, INK, True, a="middle") + R(204, 6, 26, 13, "#FFFFFF", INK, 0, .8) + T(B, 217, 14.6, "SHARE", 4.5, INK, w=600, a="middle") + L(0, 23, W, 23, LN)
    y = 28
    if nav == "top":
        s += R(10, y, 34, 15, "#F3F1EC", LN, 7.5) + T(B, 30, y + 10, "Back", 6.5, INK, w=600, a="middle") + chev(17, y + 7.5, TERRA).replace('d="M13', 'd="M13')
        s += D(55, y + 7.5, 7.5, "#FFFFFF") + f'<circle cx="55" cy="{y+7.5}" r="7.5" fill="none" stroke="{LN}"/>' + il("house", 50.5, y + 3, 9, INK)
        if plan: s += R(160, y, 70, 15, "#FFFFFF", LN, 7.5) + D(168, y + 7.5, 2, SAFFRON) + T(B, 173, y + 10, "Plus Plan", 6, INK, w=600) + T(B, 224, y + 10, "Change", 5.5, TERRA, w=600, a="end")
        y += 20
    elif nav == "slim":
        s += T(B, 12, y + 9, "< Back", 6.5, MUTE, w=600) + T(B, 228, y + 9, "Home", 6.5, MUTE, w=600, a="end"); y += 14
    # progress
    f = step / total; done = step >= total
    if prog == "bar":
        s += T(B, 12, y + 6, f"ALL {total} DONE" if done else f"STEP {step} OF {total}", 5.5, MUTE, w=600, ex='letter-spacing=".8"') + R(62, y + 3, 166, 3, "#EEEAE4", r=1.5) + R(62, y + 3, 166 * f, 3, JUNGLE if done else TERRA, r=1.5); y += 12
    elif prog == "seg":
        w = (216 - (total - 1) * 3) / total
        s += "".join(R(12 + i * (w + 3), y + 2, w, 4, (TERRA if i < step else "#EEEAE4"), r=2) for i in range(total)); y += 10
    elif prog == "time":
        left = max(0, total - step) * 10
        s += T(B, 12, y + 6, "ABOUT A MINUTE LEFT" if left > 30 else "ALMOST THERE", 5.5, MUTE, w=600, ex='letter-spacing=".8"') + R(100, y + 3, 128, 3, "#EEEAE4", r=1.5) + R(100, y + 3, 128 * f, 3, TERRA, r=1.5); y += 12
    elif prog == "chapters":
        names = ["Your Home", "Systems", "Extras"]; cur = 0 if step <= 2 else (1 if step <= 6 else 2)
        for i, n in enumerate(names):
            x = 12 + i * 73; on = i <= cur
            s += R(x, y + 8, 70, 3, TERRA if i < cur else (TERRA + "88" if i == cur else "#EEEAE4"), r=1.5) + T(B, x, y + 5, n.upper(), 5, INK if on else MUTE, w=600, ex='letter-spacing=".6"')
        y += 16
    # question head
    y += 4
    if head == "side":
        s += blob(art, 30, y + 16, 16, ACC[step % 4]) + T(B, 54, y + 14, title, 14, INK, True) + T(B, 54, y + 25, sub, 6, MUTE); y += 40
    elif head == "big":
        s += R(12, y, 216, 60, ACC[step % 4] + "14", r=10) + il(art, 96, y + 6, 48, INK) + T(B, 120, y + 76, title, 15, INK, True, a="middle") + T(B, 120, y + 88, sub, 6.3, MUTE, a="middle"); y += 96
    elif head == "plain":
        s += T(B, 12, y + 14, title, 15, INK, True) + T(B, 12, y + 25, sub, 6.3, MUTE); y += 34
    elif head == "center":
        s += blob(art, 120, y + 20, 18, ACC[step % 4]) + T(B, 120, y + 54, title, 15, INK, True, a="middle") + T(B, 120, y + 65, sub, 6.3, MUTE, a="middle"); y += 74
    if tags != "none" and tags != "foot": s += TAGS(tags, y); y += 30 if tags == "pills" else 16
    if body: g, h = body(y); s += g; y += h
    if tags == "foot": s += TAGS("line", 238)
    if foot == "skip": s += R(12, 252, 216, 18, TERRA, r=6) + T(B, 120, 263.5, "NEXT", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"') + R(12, 275, 216, 15, "#FFFFFF", "#CFC8BC", 6, .8, 'stroke-dasharray="3 2"') + T(B, 120, 285, "Unsure? Skip for Now", 6, MUTE, w=600, a="middle")
    elif foot == "unsure": s += R(12, 275, 216, 15, "#FFFFFF", "#CFC8BC", 6, .8, 'stroke-dasharray="3 2"') + T(B, 120, 285, "Unsure", 6, MUTE, w=600, a="middle")
    elif foot == "nextonly": s += R(12, 268, 216, 20, TERRA, r=6) + T(B, 120, 280.5, "NEXT", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"')
    elif foot == "bottomnav":
        s += L(0, 266, W, 266, LN) + R(12, 272, 60, 18, "#FFFFFF", LN, 6) + T(B, 42, 283.5, "Back", 6.5, INK, w=600, a="middle") + R(78, 272, 150, 18, TERRA, r=6) + T(B, 153, 283.5, "NEXT", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"')
    return phone(B, s + extra)
TG = [("Free Offer in Minutes", TERRA, "clock"), ("Tailored to Your Home", LAGOON, "house"), ("Warranties Checked", SAFFRON, "shield")]
def TAGS(st, y):
    if st == "pills":
        s, x, yy = "", 12, y
        for i, (n, c, k) in enumerate(TG):
            w = len(n) * 3.15 + 18
            if x + w > 228: x, yy = 12, yy + 14
            s += R(x, yy, w, 11, c + "1A", r=4) + il(k, x + 3, yy + 2, 7, c) + T(B, x + 12, yy + 7.6, n, 5, c, w=600); x += w + 4
        return s
    if st == "line":
        return "".join(il("shield" if i == 2 else ("clock" if i == 0 else "house"), 12 + i * 74, y + 1, 7, JUNGLE) + T(B, 21 + i * 74, y + 6.5, n, 5, MUTE, w=600) for i, (n, c, k) in enumerate(TG))
    return ""
# ---------- bodies ----------
def tiles(items, style="num", cols=2, sel=1, th=40, badge=None):
    def f(y):
        y += 6; w = (216 - (cols - 1) * 6) / cols; s = ""
        for i, it in enumerate(items):
            lab, k = it if isinstance(it, tuple) else (it, None)
            x, yy = 12 + (i % cols) * (w + 6), y + (i // cols) * (th + 6); c = ACC[i % 4]; on = i == sel
            if style == "list":
                yy = y + i * 24; s += R(12, yy, 216, 20, c + "12" if on else "#FFFFFF", TERRA if on else LN, 6, 1.2 if on else .8)
                s += (il(k, 18, yy + 4, 12, c) if k else T(B, 22, yy + 13.5, str(i + 1), 8, c, True, a="middle")) + T(B, 36, yy + 13, lab, 7.5, INK, True)
                s += (D(216, yy + 10, 4, TERRA) if on else f'<circle cx="216" cy="{yy+10}" r="4" fill="none" stroke="#BDB6AA"/>')
                if badge and i in badge: s += R(150, yy + 5, 54, 10, JUNGLE + "1A", r=5) + T(B, 177, yy + 12, badge[i], 4.8, JUNGLE, w=600, a="middle")
                continue
            s += R(x, yy, w, th, c + "10" if (on and style == "tint") else "#FFFFFF", TERRA if (on and style != "tint") else (c if on else LN), 7, 1.4 if on else .8)
            if style == "num": s += D(x + w / 2, yy + 14, 9, c + "22") + T(B, x + w / 2, yy + 18.5, str(i + 1), 12, c, True, a="middle") + T(B, x + w / 2, yy + th - 6, lab, 7, INK, True, a="middle")
            elif style in ("ill", "tint"): s += il(k or "house", x + w / 2 - 10, yy + 4, 20, c) + T(B, x + w / 2, yy + th - 6, lab, 7, INK, True, a="middle")
            elif style == "chip": s += T(B, x + w / 2, yy + th / 2 + 3, lab, 8, INK, True, a="middle")
            if badge and i in badge: s += R(x + w - 44, yy + 3, 41, 9, JUNGLE + "1A", r=4.5) + T(B, x + w - 23.5, yy + 9.3, badge[i], 4.5, JUNGLE, w=600, a="middle")
            if on and style != "num": s += D(x + 8, yy + 8, 4, TERRA) + f'<path d="M{x+6} {yy+8} l1.5 1.5 3 -3" fill="none" stroke="#fff" stroke-width="1.2"/>'
        rows = len(items) if style == "list" else -(-len(items) // cols)
        return s, rows * ((24) if style == "list" else th + 6) + 8
    return f
def zipbox(y):
    return R(12, y + 4, 216, 24, "#FFFFFF", LAGOON, 7, 1.4) + il("pin", 18, y + 9, 13, LAGOON) + T(B, 36, y + 19.5, "48322", 9, INK, w=600), 34
FURN = ["One", "Two", "Three", "4 or More"]
FURN_I = [("One", "furnace"), ("Two", "furnace"), ("Three", "furnace"), ("4 or More", "furnace")]
EXTRAS = [("Dryer Vent", "dryer"), ("Sump Pump", "sump"), ("Fridge Coils", "fridge"), ("Whole-Home Surge", "bolt"), ("Water Softener", "drop"), ("None", "list")]
def photo_tile(y):
    return R(12, y, 216, 26, SAFFRON + "14", SAFFRON, 7, 1, 'stroke-dasharray="3 2"') + il("camera", 18, y + 6, 14, INK) + T(B, 38, y + 12, "Snap a Photo Instead", 7.5, INK, True) + T(B, 38, y + 20.5, "Point at the label, we read it for you.", 5.5, MUTE), 30
def with_photo(f):
    def g(y):
        a, h = f(y); b, h2 = photo_tile(y + h); return a + b, h + h2
    return g
def ready(style):
    def f(y):
        if style == "icons":
            return blob("list", 80, y + 26, 18, JUNGLE) + blob("furnace", 120, y + 26, 15, TERRA) + blob("ac", 158, y + 26, 15, LAGOON) + T(B, 120, y + 66, "Your Price Is Ready", 15, INK, True, a="middle") + T(B, 120, y + 78, "Built from your answers.", 6.5, MUTE, a="middle"), 90
        rows = [("ZIP", "48322"), ("Home Size", "2,000 to 3,000 sq ft"), ("Furnace", "Two"), ("AC", "One"), ("Water Heater", "One, Tank"), ("Extras", "Dryer Vent, Sump Pump")]
        s = T(B, 12, y + 14, "Your Price Is Ready", 15, INK, True) + T(B, 12, y + 25, "Here is what Your Licensed Tech will look after.", 6, MUTE)
        s += R(12, y + 32, 216, len(rows) * 15 + 6, "#FFFFFF", LN, 7)
        for i, (k, v) in enumerate(rows):
            yy = y + 38 + i * 15; s += il("shield", 18, yy, 8, JUNGLE) + T(B, 30, yy + 6.5, k, 6, MUTE) + T(B, 196, yy + 6.5, v, 6, INK, w=600, a="end") + T(B, 222, yy + 6.5, "Edit", 5, TERRA, w=600, a="end")
        return s, 130
    return f
def ready_foot(style):
    if style == "icons": return R(12, 248, 216, 18, TERRA, r=6) + T(B, 120, 259.5, "SEE MY PRICE", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"') + R(12, 270, 216, 15, "#F3F1EC", INK, 6, .8) + il("camera", 70, 273, 9, INK) + T(B, 128, 280.5, "ADD PHOTOS TO LOCK IT IN", 5.5, INK, w=600, a="middle", ex='letter-spacing=".8"') + T(B, 120, 294, "Photos are optional.", 5, MUTE, a="middle")
    return R(12, 262, 216, 20, TERRA, r=6) + T(B, 120, 274.5, "SEE MY PRICE", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"')
# ---------- pairs ----------
G = "Question Order And Wording"
P(G, "First Question: ZIP Or Home Size?",
  ("or_zip", "ZIP First", "Where's Your Home? opens, as live today.", "quick", scr(1, 7, "Where's Your Home?", "ZIP or street address. Metro Detroit.", "pin", zipbox, tags="pills")),
  ("or_size", "Home Size First", "Start with the easy tap, ZIP later.", "calm", scr(1, 7, "How Big Is Your Home?", "Rough is fine. You can change it.", "size", tiles(["Under 2,000", "2,000 to 3,000", "3,000 to 4,500", "Over 4,500"], "chip", th=30), tags="pills", foot="unsure")))
P(G, "Question Wording: Short Count Or Friendly Question?",
  ("wd_short", "How Many Furnaces?", "Short, as live today.", "focused", scr(3, 7, "How Many Furnaces?", "Most homes over 3,500 sq ft have two.", body=tiles(FURN), foot="unsure")),
  ("wd_friendly", "What Keeps You Warm?", "Plain-language question, count in the tiles.", "calm", scr(3, 7, "What Keeps You Warm?", "Count the furnaces in your home.", body=tiles(FURN), foot="unsure")))
P(G, "Water Heater: Two Screens Or One?",
  ("wh_two", "Two Screens", "Count first, then Tank or Tankless, as live.", "quick", scr(6, 8, "Tank Or Tankless?", "Tankless hangs on the wall.", "water", tiles([("Tank", "water"), ("Tankless", "tankless")], "ill", th=56, sel=0), foot="unsure")),
  ("wh_one", "One Combined Screen", "Count and type on the same screen, one fewer step.", "focused", scr(5, 7, "Your Water Heater", "Pick the count, then the type.", "water", lambda y: (lambda a, b: (a[0] + b[0], a[1] + b[1]))(tiles(["One", "Two"], "chip", th=24, sel=0)(y), tiles([("Tank", "water"), ("Tankless", "tankless")], "ill", th=44, sel=0)(y + 32)), foot="nextonly")))
G = "Tiles, Icons And Illustrations"
P(G, "Answer Tiles: Number Bubbles Or Drawn Illustrations?",
  ("tl_num", "Number Bubbles", "Coloured number in a circle, as live.", "calm", scr(3, 7, body=tiles(FURN), foot="unsure")),
  ("tl_ill", "Drawn Illustrations", "A little furnace drawing on every tile.", "visual", scr(3, 7, body=tiles(FURN_I, "ill"), foot="unsure")))
P(G, "Answer Layout: 2 By 2 Grid Or Full-Width Rows?",
  ("ly_grid", "2 By 2 Grid", "Big square taps.", "visual", scr(2, 7, "How Big Is Your Home?", "Rough is fine.", "size", tiles(["Under 2,000", "2,000 to 3,000", "3,000 to 4,500", "Over 4,500"], "chip", th=36), foot="unsure")),
  ("ly_rows", "Full-Width Rows", "One answer per row, radio on the right.", "focused", scr(2, 7, "How Big Is Your Home?", "Rough is fine.", "size", tiles([("Under 2,000 sq ft", "size"), ("2,000 to 3,000 sq ft", "size"), ("3,000 to 4,500 sq ft", "size"), ("Over 4,500 sq ft", "size")], "list"), foot="unsure")))
P(G, "Question Illustration: Small Circle Beside Or Big Drawing Above?",
  ("il_side", "Small Circle Beside", "Icon circle next to the title, as live.", "focused", scr(5, 7, "How Many Water Heaters?", "Usually in the basement.", "water", tiles(FURN[:2], th=36, sel=0), foot="unsure")),
  ("il_big", "Big Drawing Above", "Large drawing on a tinted panel, title below.", "visual", scr(5, 7, "How Many Water Heaters?", "Usually in the basement.", "water", tiles(FURN[:2], th=36, sel=0), head="big", foot="unsure")))
G = "Progress Indicator"
P(G, "Progress: Step Count Bar Or Segments?",
  ("pg_bar", "Step 3 Of 7 Bar", "Label plus a filling bar, as live.", "calm", scr(3, 7, body=tiles(FURN), foot="unsure")),
  ("pg_seg", "Seven Segments", "One block per question, no label.", "visual", scr(3, 7, body=tiles(FURN), prog="seg", foot="unsure")))
P(G, "Progress Label: Steps Or Chapters?",
  ("pg_time", "Time Left", "'About a minute left' instead of a count.", "quick", scr(4, 7, "How Many AC Units?", "Look outside: one box per unit.", "ac", tiles(FURN, sel=0), prog="time", foot="unsure")),
  ("pg_chap", "Three Chapters", "Your Home, Systems, Extras.", "focused", scr(4, 7, "How Many AC Units?", "Look outside: one box per unit.", "ac", tiles(FURN, sel=0), prog="chapters", foot="unsure")))
G = "Tags"
P(G, "Tags: First Screen Only Or Every Screen?",
  ("tg_first", "First Screen Only", "Three pills under the ZIP box, as live.", "calm", scr(1, 7, "Where's Your Home?", "ZIP or street address. Metro Detroit.", "pin", zipbox, tags="pills")),
  ("tg_every", "Quiet Line On Every Screen", "Small reminder above the buttons the whole way.", "focused", scr(3, 7, body=tiles(FURN), tags="foot", foot="unsure")))
P(G, "Tag Style: Coloured Pills Or Check Line?",
  ("ts_pills", "Coloured Pills", "Terracotta, lagoon, saffron tints.", "visual", scr(1, 7, "Where's Your Home?", "ZIP or street address. Metro Detroit.", "pin", zipbox, tags="pills")),
  ("ts_line", "Single Check Line", "One quiet row with green marks.", "calm", scr(1, 7, "Where's Your Home?", "ZIP or street address. Metro Detroit.", "pin", zipbox, tags="line")))
G = "Questions To Add Or Cut"
P(G, "Stories Question: Keep Or Cut?",
  ("st_keep", "Keep Stories", "One tap, helps size the visit.", "calm", scr(7, 8, "How Many Stories?", "Count floors above ground.", "stories", tiles(["One", "Two", "Three", "Split Level"]), foot="unsure")),
  ("st_cut", "Cut It", "Six questions, straight to Extras.", "quick", scr(6, 6, "Any Extras?", "Pick all that apply.", "list", tiles(EXTRAS, "ill", cols=3, th=38, sel=0))))
P(G, "Add A Home Age Question?",
  ("ag_add", "Add Home Age", "Helps Your Licensed Tech plan the first visit.", "focused", scr(3, 8, "How Old Is Your Home?", "Best guess is fine.", "house", tiles(["Under 10 Years", "10 to 30", "30 to 60", "Over 60"], "chip", th=30), foot="unsure")),
  ("ag_skip", "Keep It Short", "No extra question; ask at the first visit.", "quick", scr(3, 7, body=tiles(FURN), foot="unsure")))
P(G, "Extras: Tile Grid Or Checklist?",
  ("ex_grid", "Tile Grid", "Drawn tiles, tap to pick many.", "visual", scr(7, 7, "Any Extras?", "Pick all that apply.", "list", tiles(EXTRAS, "ill", cols=3, th=38, sel=0))),
  ("ex_list", "Checklist Rows", "Faster to scan, one per row.", "focused", scr(7, 7, "Any Extras?", "Pick all that apply.", "list", tiles(EXTRAS[:5], "list", sel=0))))
G = "Snap-A-Photo Upload"
P(G, "Snap A Photo: On Each System Question Or Only At The End?",
  ("ph_each", "On Each System Question", "'Snap a Photo Instead' under the furnace, AC and water heater tiles.", "quick", scr(3, 7, body=with_photo(tiles(FURN, th=34)), foot="unsure")),
  ("ph_end", "Only At The End", "'Add Photos To Lock It In' on Your Price Is Ready, as live.", "calm", scr(7, 7, "", "", body=ready("icons"), head="none", foot="none", extra=ready_foot("icons"))))
P(G, "Photo Option: Equal Choice Or Side Path?",
  ("pc_equal", "Equal Choice", "First screen asks: Answer Questions or Snap Photos.", "visual", scr(1, 7, "How Do You Want To Start?", "Both get your price in minutes.", "list", tiles([("Answer 7 Questions", "list"), ("Snap 3 Photos", "camera")], "ill", th=64, sel=-1), foot="none")),
  ("pc_side", "Side Path", "Questions stay the main road; photo is a small dashed tile.", "calm", scr(4, 7, "How Many AC Units?", "Look outside: one box per unit.", "ac", with_photo(tiles(FURN, sel=0, th=34)), foot="unsure")))
G = "Oh That's Cool Services"
P(G, "Tease Services: Badges On Tiles Or A Did You Know Card?",
  ("ts_badge", "Badges On Tiles", "Small 'Included In Plus' badge on the extras.", "quick", scr(7, 7, "Any Extras?", "Pick all that apply.", "list", tiles(EXTRAS, "ill", cols=3, th=38, sel=0, badge={0: "In Plus", 3: "In Complete"}))),
  ("ts_card", "Did You Know Card", "One short card under the tiles.", "calm", scr(4, 7, "How Many AC Units?", "Look outside: one box per unit.", "ac", lambda y: (lambda a: (a[0] + R(12, y + a[1], 216, 30, JUNGLE + "12", r=7) + il("bolt", 18, y + a[1] + 8, 13, JUNGLE) + T(B, 38, y + a[1] + 13, "Did You Know?", 7.5, INK, True) + T(B, 38, y + a[1] + 22, "Your Licensed Tech also rinses the outdoor coil.", 5.5, MUTE), a[1] + 34))(tiles(FURN, sel=0, th=34)(y)), foot="unsure")))
G = "Transitions And Handoff"
P(G, "After A Tap: Auto-Advance Or Next Button?",
  ("tr_auto", "Auto-Advance", "Tap a tile, slide to the next question.", "quick", scr(3, 7, body=tiles(FURN), foot="unsure", extra=R(150, 120, 90, 160, "#FFFFFF", LN, 8) + T(B, 160, 140, "How Many AC", 9, INK, True) + T(B, 160, 151, "Units?", 9, INK, True) + f'<path d="M140 200 L128 206 L140 212" fill="none" stroke="{TERRA}" stroke-width="2" stroke-linecap="round"/>')),
  ("tr_next", "Pick, Then Next", "Answer stays highlighted until Next is tapped.", "calm", scr(3, 7, body=tiles(FURN), foot="nextonly")))
P(G, "Back And Home: Pills At The Top Or Bar At The Bottom?",
  ("nv_top", "Pills At The Top", "Back, Home and Plus Plan pills, as live.", "calm", scr(3, 7, body=tiles(FURN), foot="unsure")),
  ("nv_bottom", "Bar At The Bottom", "Back beside Next, where the thumb is.", "quick", scr(3, 7, body=tiles(FURN), nav="slim", foot="bottomnav")))
P(G, "Coming Back Later: Resume Card Or Jump Straight In?",
  ("rs_card", "Resume Card", "'Pick Up Where You Left Off' with your 3 of 7 answers.", "calm", scr(3, 7, "Welcome Back", "Your answers are saved.", "clock", lambda y: (R(12, y + 4, 216, 60, "#FFFFFF", LN, 8) + T(B, 22, y + 20, "Pick Up Where You Left Off", 9, INK, True) + R(22, y + 28, 196, 3, "#EEEAE4", r=1.5) + R(22, y + 28, 84, 3, TERRA, r=1.5) + T(B, 22, y + 42, "3 of 7 answered: ZIP, size, furnace", 5.8, MUTE) + R(22, y + 48, 90, 12, TERRA, r=5) + T(B, 67, y + 56.5, "RESUME", 5.5, "#FFFFFF", w=600, a="middle") + T(B, 160, y + 56.5, "Start Over", 5.8, MUTE, w=600, a="middle"), 70), head="center", foot="none")),
  ("rs_jump", "Jump Straight In", "Opens on question 4 with a small 'Saved' note.", "quick", scr(4, 7, "How Many AC Units?", "Saved. Picking up at question 4.", "ac", tiles(FURN, sel=-1), foot="unsure")))
P(G, "Your Price Is Ready: Icons Or Answer Summary?",
  ("rd_icons", "Icons And Big Button", "Three drawings, See My Price, as live.", "visual", scr(7, 7, "", "", body=ready("icons"), head="none", foot="none", extra=ready_foot("icons"))),
  ("rd_sum", "Answer Summary", "Every answer listed with Edit, then See My Price.", "focused", scr(7, 7, "", "", body=ready("sum"), head="none", foot="none", extra=ready_foot("sum"))))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Info Gather Deck", "UpKeep", pairs,
        {"brands": ["Info Gather (stage 4 of the funnel: Marketing, Video/Catch, Home Page, Info Gather, Price Offer, Make The Sale): smartupkeep Get Started intake: question order and wording, tiles/icons/illustrations, progress, tags, add/cut questions, Snap-a-Photo, teasing services, transitions, back/home, resume, Your Price Is Ready handoff",
                    "Light cream page, white cards, Khand/Hind, terracotta/lagoon/jungle/saffron accents; UpKeep brand rules applied: Your Licensed Tech, Essentials/Plus/Complete, no byline"],
         "submit_agent": "upkeep", "submit_to": "UpKeep Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "sources": {"site": "https://smartupkeep.ai (Get Started)", "screens": "/workspace/smartkeep/updates-oct14/live/393-04..12*.png, 1440-*.png"}},
        seed=1414, n=N)
