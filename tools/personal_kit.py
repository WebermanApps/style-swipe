"""Shared mockup kit for the personal-project decks (blueprint-3, thai-2, blog-1, portfolio-1, japan-cottage-1, miles-1,
jokes-1, jane-amex-2). Built on draft_svg.py (white base, Khand/Hind, small accents). Each topic = 5 layout variants x 2
finish variants -> 10 fresh options -> 5 pairs. All data shown is example data only. Run builders from the repo root."""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(__file__))
from draft_svg import *
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
def foot(): return t(120, 292, "Built By Max Weberman", 6, "#9A948A", "hind", 600, "middle")
def shareic(x, y, c=INK, s=14):
    return f'<g transform="translate({x},{y}) scale({s/24})"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></g>'
# ---------- drawn pictures ----------
def pic(kind, x, y, w, h, c):
    s = rect(x, y, w, h, c + "14", "none", 6)
    if kind == "house":
        s += f'<path d="M{x+w*.2} {y+h*.55} L{x+w*.5} {y+h*.22} L{x+w*.8} {y+h*.55} V{y+h*.85} H{x+w*.2} Z" fill="#FFFFFF" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/>' + rect(x + w * .45, y + h * .63, w * .1, h * .22, c)
    elif kind == "cottage":
        s += f'<path d="M{x+w*.12} {y+h*.5} L{x+w*.5} {y+h*.2} L{x+w*.88} {y+h*.5} Z" fill="{c}"/>' + rect(x + w * .2, y + h * .5, w * .6, h * .35, "#FFFFFF", c, 0, 1.4) + "".join(rect(x + w * (.26 + i * .14), y + h * .58, w * .08, h * .12, "none", c, 0, 1) for i in range(4))
    elif kind == "plan":
        s += rect(x + w * .1, y + h * .12, w * .8, h * .76, "#FFFFFF", c, 0, 1.6) + f'<path d="M{x+w*.5} {y+h*.12} V{y+h*.6} M{x+w*.1} {y+h*.5} H{x+w*.5} M{x+w*.5} {y+h*.6} H{x+w*.9}" stroke="{c}" stroke-width="1.2" fill="none"/>'
    elif kind == "card":
        s += rect(x + w * .18, y + h * .25, w * .64, h * .5, c, "none", 5) + rect(x + w * .26, y + h * .36, w * .12, h * .1, "#FFFFFF66", "none", 2) + t(x + w * .76, y + h * .68, "EXAMPLE", min(w, h) * .09, "#FFFFFF", "hind", 600, "end")
    elif kind == "mic":
        s += ic("mic", x + w / 2 - h * .3, y + h * .2, h * .6, c, 2)
    elif kind == "page":
        s += rect(x + w * .25, y + h * .12, w * .5, h * .76, "#FFFFFF", c, 2, 1.4) + "".join(rect(x + w * .32, y + h * (.24 + i * .12), w * (.36 if i % 2 else .3), 2, c + "88") for i in range(5))
    elif kind == "speaker":
        s += ic("speaker", x + w / 2 - h * .3, y + h * .2, h * .6, c, 2)
    elif kind == "chart":
        s += "".join(rect(x + w * (.2 + i * .13), y + h * (.75 - v), w * .08, h * v, c if i == 4 else c + "66", "none", 1) for i, v in enumerate([.25, .4, .3, .5, .6]))
    return s
# ---------- headers ----------
def header(style, app, sub, c, pk):
    if style == "band": return rect(0, 0, W, 44, c) + t(14, 22, app, 13, "#FFFFFF", "khand") + t(14, 34, sub, 6.5, "#FFFFFFCC") + shareic(208, 15, "#FFFFFF")
    if style == "center": return t(120, 24, app, 14, INK, "khand", anchor="middle") + t(120, 36, sub, 6.5, MUTE, anchor="middle") + rect(108, 40, 24, 2, c) + shareic(208, 14)
    if style == "hero": return t(14, 18, "MAX WEBERMAN", 5.8, MUTE, "hind", 600, extra='letter-spacing="1.4"') + h1(14, 40, app, 20) + t(14, 52, sub, 6.5, MUTE) + shareic(208, 14) + ln(58)
    if style == "icon": return pic(pk, 14, 10, 26, 26, c) + t(46, 22, app, 12, INK, "khand") + t(46, 33, sub, 6.5, MUTE) + shareic(208, 14) + ln(44)
    return t(14, 22, app, 13, INK, "khand") + t(14, 34, sub, 6.5, MUTE) + shareic(208, 14) + ln(44)
def notes_share(y=262, c=INK):
    return rect(14, y, 104, 20, "#FFFFFF", LINE, 6) + ic("star", 22, y + 4, 12, c) + t(40, y + 14, "Notes", 8, INK, "hind", 600) + rect(122, y, 104, 20, "#FFFFFF", LINE, 6) + shareic(130, y + 4, c, 12) + t(148, y + 14, "Share", 8, INK, "hind", 600)
# ---------- bodies (each takes variant a in 0..4) ----------
def b_list(a, items, c, r, gap, pk):
    s = ""; y = 56
    for i, (n, d, v) in enumerate(items[:5]):
        h = 34 + gap; cc = ACC[i % 4] if a == 4 else c
        if y + h > 256: break
        if a == 0: s += rect(14, y, 212, h - 4, "#FFFFFF", LINE, r) + dot(26, y + (h - 4) / 2, 3.5, cc) + t(36, y + 14, n, 9.5, INK, "khand") + t(36, y + 25, d, 6.5, MUTE) + t(218, y + 18, v, 7, MUTE, "hind", 600, "end")
        elif a == 1: s += rect(14, y, 212, h - 4, "#FFFFFF", LINE, r) + rect(14, y, 4, h - 4, cc, "none", min(r, 2)) + t(26, y + 14, n, 9.5, INK, "khand") + t(26, y + 25, d, 6.5, MUTE) + tag(226 - len(v) * 4.4 - 18, y + 9, v, cc)
        elif a == 2: s += t(14, y + 14, n, 10, INK, "khand") + t(14, y + 25, d, 6.5, MUTE) + t(226, y + 18, v, 9, cc, "khand", anchor="end") + ln(y + h - 4)
        elif a == 3: s += t(22, y + 20, str(i + 1), 16, cc, "khand", anchor="middle") + t(38, y + 14, n, 9.5, INK, "khand") + t(38, y + 25, d, 6.5, MUTE) + ic("chev", 210, y + 8, 12, MUTE) + ln(y + h - 4, 38)
        else: s += rect(14, y, 212, h - 4, cc + "12", "none", r) + pic(pk, 20, y + 4, h - 12, h - 12, cc) + t(26 + h - 12, y + 14, n, 9.5, INK, "khand") + t(26 + h - 12, y + 25, d, 6.5, MUTE) + t(218, y + 18, v, 7, cc, "hind", 700, "end")
        y += h
    return s
def b_tiles(a, items, c, r, gap, pk):
    s = ""
    if a == 0:
        for i, (n, d, v) in enumerate(items[:4]):
            x, y = 14 + (i % 2) * 108, 56 + (i // 2) * (96 + gap); s += rect(x, y, 104, 90, "#FFFFFF", LINE, r) + pic(pk, x + 8, y + 8, 88, 42, ACC[i % 4]) + t(x + 8, y + 64, n, 9.5, INK, "khand") + t(x + 8, y + 78, v, 6.5, MUTE)
    elif a == 1:
        for i, (n, d, v) in enumerate(items[:8]):
            x, y = 14 + (i % 4) * 54, 56 + (i // 4) * (60 + gap); s += rect(x, y, 48, 54, "#FFFFFF", LINE, r) + pic(pk, x + 8, y + 6, 32, 28, ACC[i % 4]) + t(x + 24, y + 46, n.split()[0], 6.8, INK, "khand", anchor="middle")
    elif a == 2:
        n, d, v = items[0]; s += rect(14, 56, 212, 100, c + "10", "none", r) + pic(pk, 24, 66, 80, 80, c) + t(114, 90, n, 12, INK, "khand") + t(114, 104, d, 6.8, MUTE) + tag(114, 116, v, c, True)
        for i, (n, d, v) in enumerate(items[1:4]): y = 166 + i * (28 + gap / 2); s += t(14, y + 12, n, 9.5, INK, "khand") + t(226, y + 12, v, 7, MUTE, "hind", 600, "end") + ln(y + 20)
    elif a == 3:
        for i, (n, d, v) in enumerate(items[:4]):
            y = 56 + i * (48 + gap / 2); s += rect(14, y, 212, 42, "#FFFFFF", LINE, r) + pic(pk, 18, y + 4, 52, 34, ACC[i % 4]) + t(78, y + 17, n, 9.5, INK, "khand") + t(78, y + 30, d, 6.5, MUTE)
    else:
        n, d, v = items[0]; s += rect(14, 56, 212, 150, "#FFFFFF", LINE, r) + pic(pk, 14, 56, 212, 100, c) + t(24, 176, n, 13, INK, "khand") + t(24, 190, d, 7, MUTE) + "".join(dot(108 + i * 8, 218, 2.5, INK if i == 0 else "#D6D0C6") for i in range(4))
    return s
def b_chart(a, items, c, r, gap, pk):
    vals = [.35, .5, .42, .62, .55, .8]; s = rect(14, 56, 212, 120, "#FFFFFF", LINE, r) + t(24, 72, items[0][0], 9, INK, "khand")
    if a == 0: s += "".join(rect(28 + i * 32, 166 - 80 * v, 20, 80 * v, c if i == 5 else c + "55", "none", min(r, 3)) for i, v in enumerate(vals))
    elif a == 1: s += f'<polyline points="{" ".join(f"{28+i*36},{166-80*v}" for i, v in enumerate(vals))}" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/>' + dot(208, 166 - 64, 3.5, c)
    elif a == 2: s += f'<circle cx="120" cy="122" r="36" fill="none" stroke="#EEEAE4" stroke-width="10"/><circle cx="120" cy="122" r="36" fill="none" stroke="{c}" stroke-width="10" stroke-dasharray="{226*.68} 300" transform="rotate(-90 120 122)"/>' + t(120, 127, "68%", 14, INK, "khand", anchor="middle")
    elif a == 3: s += t(24, 130, items[0][2], 38, c, "khand") + t(24, 150, items[0][1], 7.5, MUTE) + tag(150, 110, "Example", c)
    else: s += "".join(t(24, 92 + i * 20, n, 7.5, INK, "hind", 600) + rect(100, 86 + i * 20, 116, 6, "#EEEAE4", "none", 3) + rect(100, 86 + i * 20, 116 * vals[i + 1], 6, ACC[i % 4], "none", 3) for i, (n, d, v) in enumerate(items[:4]))
    for i, (n, d, v) in enumerate(items[1:3]): y = 184 + i * (30 + gap / 2); s += t(14, y + 12, n, 9.5, INK, "khand") + t(226, y + 12, v, 8, MUTE, "hind", 600, "end") + ln(y + 20)
    return s
def b_detail(a, items, c, r, gap, pk):
    n, d, v = items[0]; s = ""
    if a == 0: s += pic(pk, 14, 56, 212, 90, c) + t(14, 166, n, 15, INK, "khand") + t(14, 180, d, 7.5, MUTE) + tag(14, 188, v, c, True)
    elif a == 1: s += pic(pk, 14, 56, 90, 90, c) + t(112, 74, n, 12, INK, "khand") + t(112, 88, d, 6.8, MUTE) + tag(112, 98, v, c)
    elif a == 2: s += rect(14, 56, 212, 4, c) + h1(14, 86, n, 18) + t(14, 102, d, 8, MUTE) + t(14, 130, v, 26, c, "khand")
    elif a == 3: s += t(14, 74, n, 13, INK, "khand") + "".join(dot(24, 96 + i * (30 + gap / 2), 9, c) + t(24, 100 + i * (30 + gap / 2), str(i + 1), 9, "#FFFFFF", "khand", anchor="middle") + t(42, 100 + i * (30 + gap / 2), m, 8.5, INK, "hind", 600) for i, (m, _, _) in enumerate(items[1:4]))
    else: s += t(14, 74, n, 13, INK, "khand") + "".join(rect(14, 84 + i * (34 + gap / 2), 212, 28, SOFT if i else c + "14", "none", r) + t(24, 102 + i * (34 + gap / 2), m, 8.5, INK, "hind", 600) + ic("down" if i == 0 else "chev", 204, 90 + i * (34 + gap / 2), 14, MUTE) for i, (m, _, _) in enumerate(items[1:5]))
    s += btn(222, "Open", "fill", INK, h=26)
    return s
def b_buttons(a, items, c, r, gap, pk):
    n, d, v = items[0]; s = rect(14, 56, 212, 120, "#FFFFFF", LINE, r) + pic(pk, 24, 66, 60, 60, c) + t(94, 82, n, 11, INK, "khand") + t(94, 96, d, 6.8, MUTE)
    L = [m for m, _, _ in items[1:3]] or ["Yes", "Not Yet"]
    if a == 0: s += btn(140, L[0], "fill", INK, 24, 92, 24, 7.5) + btn(140, L[1], "line", INK, 124, 92, 24, 7.5)
    elif a == 1: s += rect(24, 140, 92, 24, c, "none", 12) + t(70, 155, L[0].upper(), 7, "#FFFFFF", "hind", 600, "middle") + rect(124, 140, 92, 24, "#FFFFFF", c, 12) + t(170, 155, L[1].upper(), 7, c, "hind", 600, "middle")
    elif a == 2: s += t(24, 156, L[0].upper(), 7.5, c, "hind", 700, extra='letter-spacing="1" text-decoration="underline"') + t(130, 156, L[1].upper(), 7.5, MUTE, "hind", 700, extra='letter-spacing="1" text-decoration="underline"')
    elif a == 3: s += rect(0, 228, W, 34, "#FFFFFF") + ln(228, 0, W) + btn(232, L[0], "fill", INK, 14, 140, 26, 7.5) + btn(232, "More", "line", INK, 160, 66, 26, 7.5)
    else: s += "".join(rect(24 + i * 64, 136, 56, 32, SOFT, "none", r) + ic(k, 44 + i * 64, 140, 14, ACC[i], 2) + t(52 + i * 64, 164, m, 6, INK, "hind", 600, "middle") for i, (m, k) in enumerate([(L[0][:8], "check"), ("Later", "clock"), ("Note", "star")]))
    for i, (m, dd, vv) in enumerate(items[3:4]): s += t(14, 198, m, 9.5, INK, "khand") + t(226, 198, vv, 7.5, MUTE, "hind", 600, "end") + ln(206)
    return s
def b_type(a, items, c, r, gap, pk):
    n, d, v = items[0]; s = ""
    if a == 0: s += h1(14, 90, n, 26) + t(14, 108, d, 8.5, MUTE)
    elif a == 1: s += lbl(14, 72, v, c) + h1(14, 94, n, 18) + t(14, 110, d, 8, MUTE)
    elif a == 2: s += rect(14, 60, 4, 50, c) + h1(26, 84, n, 17) + t(26, 102, d, 8, INK)
    elif a == 3: s += t(120, 86, n.upper(), 12, INK, "khand", anchor="middle", extra='letter-spacing="2"') + rect(100, 94, 40, 2, c) + t(120, 112, d, 8, MUTE, anchor="middle")
    else: s += rect(14, 58, 212, 60, c + "12", "none", r) + h1(24, 86, n, 16) + t(24, 104, d, 7.5, MUTE)
    for i in range(5): s += rect(14, 128 + i * (12 + gap / 3), [212, 200, 206, 150, 190][i], 3, "#D6D0C6", "none", 1.5)
    for i, (m, dd, vv) in enumerate(items[1:3]): s += t(14, 214 + i * 22, m, 9.5, INK, "khand") + t(226, 214 + i * 22, vv, 7, MUTE, "hind", 600, "end")
    return s
def b_nav(a, items, c, r, gap, pk):
    s = b_list(0, items[:3], c, r, gap, pk); names = [m.split()[0] for m, _, _ in items[:4]]
    if a == 0: s += rect(0, 226, W, 34, "#FFFFFF") + ln(226, 0, W) + "".join(ic(["home", "search", "star", "cal"][i], 23 + i * 60, 230, 14, c if i == 0 else "#A3A3A3") + t(30 + i * 60, 254, nm[:9], 6, c if i == 0 else MUTE, "hind", 600, "middle") for i, nm in enumerate(names))
    elif a == 1: s = rect(14, 50, 212, 20, SOFT, "none", 10) + rect(16, 52, 51, 16, "#FFFFFF", LINE, 8) + "".join(t(41 + i * 53, 63, nm[:9], 7, INK if i == 0 else MUTE, "khand", anchor="middle") for i, nm in enumerate(names)) + b_list(0, items[:3], c, r, gap, pk).replace('y="56"', 'y="78"')
    elif a == 2: s = rect(0, 44, 64, 216, SOFT) + "".join(t(10, 66 + i * 22, nm[:9], 8, c if i == 0 else MUTE, "khand") for i, nm in enumerate(names)) + rect(0, 54, 3, 16, c) + "".join(rect(72, 56 + i * 44, 154, 38, "#FFFFFF", LINE, r) + t(80, 72 + i * 44, m, 9, INK, "khand") + t(80, 84 + i * 44, vv, 6.5, MUTE) for i, (m, dd, vv) in enumerate(items[:4]))
    elif a == 3: s += f'<path d="M190 18 H204 M190 22 H204 M190 26 H204" stroke="{INK}" stroke-width="1.6"/>' + rect(110, 44, 130, 120, "#FFFFFF", LINE, r, extra='filter="drop-shadow(0 3px 5px #0002)"') + "".join(t(122, 66 + i * 24, nm, 9, INK, "khand") for i, nm in enumerate(names))
    else: s += "".join(dot(102 + i * 12, 236, 3, c if i == 0 else "#D6D0C6") for i in range(4)) + t(120, 252, "Swipe For " + names[1], 7, MUTE, "hind", 600, "middle")
    return s
def b_notice(a, items, c, r, gap, pk):
    n, d, v = items[0]; s = b_list(2, items[1:4], c, r, gap, pk)
    if a == 0: s = rect(14, 50, 212, 30, c + "18", "none", r) + ic("clock", 22, 57, 16, c) + t(44, 64, n, 8.5, INK, "khand") + t(44, 74, d, 6.3, MUTE) + s.replace('y="56"', 'y="88"')
    elif a == 1: s += rect(30, 208, 180, 30, INK, "none", r) + t(42, 227, n, 8.5, "#FFFFFF", "hind", 600) + t(198, 227, "UNDO", 7, SAFFRON, "hind", 700, "end")
    elif a == 2: s += rect(0, 0, W, H, "#0A0A0A44") + rect(30, 90, 180, 110, "#FFFFFF", "none", r) + t(120, 120, n, 11, INK, "khand", anchor="middle") + t(120, 136, d, 7, MUTE, anchor="middle") + btn(160, "Got It", "fill", c, 50, 140, 24, 7.5)
    elif a == 3: s += rect(0, 0, W, H, "#0A0A0A44") + rect(0, 170, W, 130, "#FFFFFF", "none", 14) + rect(104, 178, 32, 4, "#D6D0C6", "none", 2) + t(14, 202, n, 11, INK, "khand") + t(14, 216, d, 7, MUTE) + btn(228, "Got It", "fill", INK, 14, 212, 24, 7.5)
    else: s += rect(14, 210, 212, 32, "#FFFFFF", c, r, 1.4) + dot(26, 226, 4, c) + t(36, 223, n, 8.5, INK, "khand") + t(36, 234, d, 6.3, MUTE)
    return s
def b_swatch(a, items, c, r, gap, pk):
    n, d, col = items[a % len(items)]; s = rect(14, 56, 212, 120, col, LINE, r) + rect(14, 140, 212, 36, "#FFFFFF", "none", 0) + t(24, 160, n, 12, INK, "khand") + t(24, 172, d, 6.8, MUTE)
    s += "".join(rect(14 + i * 44, 186, 38, 38, it[2], LINE, r / 2, 1.4 if i == a % len(items) else 1) for i, it in enumerate(items[:5])) + rect(14 + (a % len(items)) * 44, 228, 38, 2.5, c)
    return s
BODIES = {"list": b_list, "tiles": b_tiles, "chart": b_chart, "detail": b_detail, "buttons": b_buttons, "type": b_type, "nav": b_nav, "notice": b_notice, "swatch": b_swatch}
HEAD = ["plain", "band", "center", "hero", "icon"]
FIN = {"corners": [("Rounded Corners", dict(r=10)), ("Square Corners", dict(r=0))],
       "density": [("Roomy", dict(gap=10)), ("Compact", dict(gap=0))],
       "accent": [("Terracotta Accent", dict(c=TERRA)), ("Lagoon Accent", dict(c=LAGOON))],
       "accent2": [("Jungle Accent", dict(c=JUNGLE)), ("Saffron Accent", dict(c=SAFFRON))],
       "header": [("Plain Header", dict(h="plain")), ("Color Band Header", dict(h="band"))],
       "header2": [("Centered Header", dict(h="center")), ("Big Title Header", dict(h="hero"))]}
LABELS = {"list": ["Dot Rows", "Color Edge Cards", "Plain Lines", "Numbered Rows", "Picture Rows"],
 "tiles": ["Two-Up Picture Cards", "Small Icon Grid", "Feature Plus List", "Wide Picture Rows", "One Big Swipe Card"],
 "chart": ["Bar Chart", "Line Chart", "Progress Ring", "Big Number", "Progress Bars"],
 "detail": ["Picture On Top", "Picture Beside", "Big Title No Picture", "Numbered Steps", "Fold-Out Sections"],
 "buttons": ["Square Buttons", "Pill Buttons", "Text Links", "Sticky Bottom Bar", "Icon Action Tiles"],
 "type": ["Big Headline", "Label Plus Headline", "Side Rule Headline", "Spaced Caps Title", "Tinted Title Box"],
 "nav": ["Bottom Tabs", "Top Pill Tabs", "Side Menu", "Pop-Out Menu", "Swipe Pages"],
 "notice": ["Top Banner", "Bottom Toast", "Center Pop-Up", "Bottom Sheet", "Inline Outline Card"]}
class Deck:
    def __init__(s, did, prefix, app, sub, pk, c):
        s.did, s.app, s.sub, s.pk, s.c = did, app, sub, pk, c; s.pairs, s.O, s.add = mk(prefix, app)
    def draw(s, body, a, items, fin):
        p = dict(c=s.c, r=8, gap=4, h="plain"); p.update(fin)
        sv = header(p["h"], s.app, s.sub, p["c"], s.pk) + BODIES[body](a, items, p["c"], p["r"], p["gap"], s.pk) + (notes_share() if body not in ("buttons",) or a != 3 else "")
        return screen(sv + foot())
    def topic(s, key, group, cat, body, items, fin="corners", desc="", feels=("visual", "focused", "quick", "calm", "action")):
        """5 layouts of one body x 2 finishes = 10 fresh options = 5 pairs; each pair differs in layout and finish."""
        labs = [it[0] for it in items[:5]] if body == "swatch" else LABELS[body]
        F = FIN[fin]; opts = []
        for i, lab in enumerate(labs):
            for j, (fl, fd) in enumerate(F):
                vk = "".join(w[0] for w in lab.lower().replace("-", " ").split())
                opts.append(s.O(f"{key}_{vk}{i}_{fl.split()[0].lower()}", f"{lab}, {fl}", f"{cat}: {lab.lower()} with {fl.lower()}. {desc}".strip(),
                                [feels[i], feels[(i + j + 1) % 5]], feels[i], s.draw(body, i, items, fd)))
        for i in range(5):
            s.add(group, cat, opts[2 * i], opts[2 * ((i + 1) % 5) + 1], f"{cat}: {labs[i]} Or {labs[(i + 1) % 5]}?", "new")
    def publish_meta(s, title, brands, sources, seed, first=0, **extra):
        finish(s.did, title, s.app, s.pairs, first, {"brands": brands, "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "calm": "Calm", "action": "Action-first"},
               "sources": sources, "example_data_only": True, **extra}, seed=seed)
        d = json.load(open(f"decks/{s.did}.json")); d.pop("draft", None); d["status"] = "published"; d["share"] = True
        for pp in d["pairs"]:
            pp["notes"] = True; pp["share"] = True
            for k in "AB": o = pp["option" + k]; o["tags"] = list(dict.fromkeys(o["tags"]))
        json.dump(d, open(f"decks/{s.did}.json", "w"), indent=1, ensure_ascii=False)
