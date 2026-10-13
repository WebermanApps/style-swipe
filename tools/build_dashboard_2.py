#!/usr/bin/env python3
"""Build Style Swipe deck dashboard-2 (PUBLISHED): round 2 of the agent command-center dashboard, built on Max's dashboard-1
results (results/dashboard-1.txt). Re-asks the 13 skipped pairs in fresh forms (medium header-name sizes), pits winners
against strong alternatives, shows combined full-dashboard looks from his winners, and opens new areas (group colors,
corner radius, tab style, ask-box placement, big monitor, MacBook width, notifications, project cards, deck-results card,
tile labels). Template: tools/build_dashboard_1.py. Run from the style-swipe repo root."""
import json, sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from draft_svg import *
DID = "dashboard-2"
pairs, O, add = mk("db2_", "Agent Dashboard")
def link(x, y, s, col=TERRA, anchor="start", size=7.5):
    return t(x, y, s.upper(), size, col, "hind", 600, anchor, 'letter-spacing="1" text-decoration="underline"')
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
AGENTS = [("Prop", TERRA, "home"), ("WellNest", JUNGLE, "heart"), ("Blueprint", LAGOON, "tag"), ("Portfolio", SAFFRON, "card")]

def avatar(x, y, c=TERRA, k="home", s=22, style="tile"):
    if style == "tile": return rect(x, y, s, s, c, "none", 5) + ic(k, x + s * .2, y + s * .2, s * .6, "#FFFFFF", 2)
    if style == "ring": return f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{s/2-1}" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>' + ic(k, x + s * .22, y + s * .22, s * .56, c, 2)
    return t(x + s / 2, y + s * .72, "P", s * .7, c, "khand", anchor="middle")
def topbar(name="Prop", sub="Command Center", c=TERRA, k="home", style="plain", share=True):
    s = ""
    if style == "band": s += rect(0, 0, W, 44, c)
    fg = "#FFFFFF" if style == "band" else INK
    s += avatar(14, 11, "#FFFFFF" if style == "band" else c, k, 22, "ring" if style == "band" else "tile") if style != "text" else ""
    x = 14 if style == "text" else 42
    s += t(x, 22, name, 13, fg, "khand") + t(x, 33, sub, 6.5, "#FFFFFFCC" if style == "band" else MUTE)
    if share: s += ic("chev", 208, 14, 14, fg, 1.6) if False else shareic(206, 14, fg)
    return s + ("" if style == "band" else ln(44, 0, W))
def shareic(x, y, c=INK, s=14):
    return f'<g transform="translate({x},{y}) scale({s/24})"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></g>'
def chip(x, y, s, c, kind="chip"):
    if kind == "dot": return dot(x + 3, y + 5, 3, c) + t(x + 10, y + 8, s, 7, INK, "hind", 600)
    if kind == "ring":
        return f'<circle cx="{x+6}" cy="{y+5}" r="5" fill="none" stroke="#EEEAE4" stroke-width="2"/><path d="M{x+6} {y} A5 5 0 1 1 {x+1.2} {y+6.5}" fill="none" stroke="{c}" stroke-width="2"/>' + t(x + 15, y + 8, s, 7, INK, "hind", 600)
    if kind == "word": return t(x, y + 8, s.upper(), 7, c, "hind", 700, extra='letter-spacing="1"')
    if kind == "bar": return rect(x, y, 3, 11, c) + t(x + 7, y + 8, s, 7, INK, "hind", 600)
    return tag(x, y, s, c, kind == "solid")
def row(y, title, sub, c=TERRA, right="", x=14, w=212, k=None):
    s = rect(x, y, w, 34, "#FFFFFF", LINE, 6) + (ic(k, x + 8, y + 9, 16, c) if k else dot(x + 12, y + 17, 3.5, c))
    return s + t(x + 30, y + 15, title, 9, INK, "khand") + t(x + 30, y + 26, sub, 6.5, MUTE) + (t(x + w - 8, y + 20, right, 6.5, MUTE, "hind", 600, "end") if right else "")
def foot(): return t(120, 292, "Built By Max Weberman", 6, "#9A948A", "hind", 600, "middle")
def scr(body, top=True, **kw): return screen((topbar(**kw) if top else "") + body + foot())
def section(y, s, c=MUTE): return lbl(14, y, s, c)
def bars(x, y, w, h, vals, c=LAGOON):
    bw = w / len(vals); return "".join(rect(x + i * bw + 2, y + h - h * v, bw - 4, h * v, c if i == len(vals) - 1 else c + "55", "none", 2) for i, v in enumerate(vals))
def ringp(cx, cy, r, frac, c, label=""):
    a = 2 * math.pi * frac; x2, y2 = cx + r * math.sin(a), cy - r * math.cos(a)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEAE4" stroke-width="4"/><path d="M{cx} {cy-r} A{r} {r} 0 {1 if frac>.5 else 0} 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>' + t(cx, cy + 3.5, label, 9, INK, "khand", anchor="middle"))
def pbar(x, y, w, frac, c): return rect(x, y, w, 4, "#EEEAE4", "none", 2) + rect(x, y, w * frac, 4, c, "none", 2)
OWED = [("Pick Front Door", "Blueprint · 2 days"), ("Approve Tax Draft", "Portfolio · today"), ("Choose Polo Color", "Up Keep · this week")]
WORK = [("Shipped Visit Log", "1h ago"), ("Updated Prices", "3h ago"), ("New Deck Ready", "Yesterday")]

def dots(y, n, cur, c=INK):
    x0 = 120 - (n - 1) * 7; return "".join(f'<circle cx="{x0+i*14}" cy="{y}" r="3" fill="{c if i==cur else "#D6D0C6"}"/>' for i in range(n))
dots = dots
def bell(x, y, s=14, c=INK): return f'<g transform="translate({x},{y}) scale({s/24})"><path d="M6 17 V11 Q6 5 12 5 Q18 5 18 11 V17 L20 19 H4 Z M10 21 H14" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></g>'
def mono(x, y, n, c, s=22, fill=False, fg=None):
    if fg: return f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{s/2}" fill="#FFFFFF"/>' + t(x + s / 2, y + s * .7, n[0], s * .55, fg, "khand", anchor="middle")
    return (f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{s/2}" fill="{c if fill else "#FFFFFF"}" stroke="{c}" stroke-width="1.6"/>' + t(x + s / 2, y + s * .7, n[0], s * .55, "#FFFFFF" if fill else c, "khand", anchor="middle"))
def band(name="Prop", c=TERRA, size=13, sub="Command Center", h=44, badge=False):
    s = rect(0, 0, W, h, c) + mono(14, (h - 22) / 2, name, "#FFFFFF", 22, fg=c) + t(42, h / 2 + (size * .3 if not sub else -1), name, size, "#FFFFFF", "khand")
    if sub: s += t(42, h / 2 + size * .3 + 8, sub, 6.5, "#FFFFFFCC")
    s += shareic(208, h / 2 - 7, "#FFFFFF")
    if badge: s += f'<circle cx="31" cy="{(h-22)/2+2}" r="6" fill="{TERRA if c != TERRA else INK}" stroke="#FFFFFF" stroke-width="1.4"/>' + t(31, (h - 22) / 2 + 4.6, "3", 7, "#FFFFFF", "hind", 700, "middle")
    return s
def upd(x=150, y=52): return rect(x, y, 76, 14, JUNGLE + "1A", "none", 7) + dot(x + 8, y + 7, 2.5, JUNGLE) + t(x + 14, y + 10, "Updated 12 Min Ago", 5.8, JUNGLE, "hind", 600)
def ocard(y, n, d, r=8, bstyle="square", c=TERRA, h=50):
    s = rect(14, y, 212, h, "#FFFFFF", LINE, r) + t(24, y + 15, n, 10, INK, "khand") + t(24, y + 25, d, 6.5, MUTE)
    if bstyle == "square": s += btn(y + 30, "Yes", "fill", INK, 24, 60, 14, 6) + btn(y + 30, "Not Yet", "line", INK, 90, 60, 14, 6)
    elif bstyle == "pill": s += rect(24, y + 30, 60, 14, c, "none", 7) + t(54, y + 39.5, "YES", 6, "#FFFFFF", "hind", 600, "middle") + rect(90, y + 30, 60, 14, "#FFFFFF", c, 7) + t(120, y + 39.5, "NOT YET", 6, c, "hind", 600, "middle")
    elif bstyle == "outline": s += btn(y + 30, "Yes", "line", INK, 24, 60, 14, 6) + btn(y + 30, "Not Yet", "line", INK, 90, 60, 14, 6)
    elif bstyle == "link": s += link(24, y + 41, "Yes", TERRA, size=7) + link(60, y + 41, "Not Yet", MUTE, size=7)
    return s
def actrow(y=52):
    return "".join(rect(14 + i * 54, y, 48, 40, SOFT, "none", 8) + ic(k, 30 + i * 54, y + 6, 16, ACC[i], 2.2) + t(38 + i * 54, y + 34, n, 6.5, INK, "hind", 600, "middle") for i, (n, k) in enumerate([("Share", "tag"), ("Ask", "mic"), ("Note", "star"), ("Open", "home")]))
def pinstrip(y): return rect(14, y, 212, 22, SAFFRON + "14", "none", 6) + ic("star", 22, y + 5, 12, SAFFRON) + t(40, y + 15, "Site Launch Checklist", 9, INK, "khand") + t(218, y + 15, "+1", 7, MUTE, "hind", 600, "end")
def sqtiles(y, n=4, label="below", r=10):
    names = [("Upkeep", "home"), ("Visits", "cal"), ("Billing", "card"), ("Prices", "tag")]
    s = ""
    for i, (nm, k) in enumerate(names[:n]):
        x = 14 + i * 54; c = ACC[i]
        s += rect(x, y, 48, 48, "#FFFFFF", LINE, r) + rect(x + 12, y + 7, 24, 24, c + "1F", "none", r * .6) + ic(k, x + 16, y + 11, 16, c, 2.2)
        if label == "below": s += t(x + 24, y + 42, nm, 7, INK, "khand", anchor="middle")
    return s
def feedcard(y, n, tm, c, k, r=8, note=None):
    h = 44 if note else 34
    s = rect(14, y, 212, h, "#FFFFFF", LINE, r) + rect(22, y + 7, 20, 20, c + "1F", "none", 5) + ic(k, 25, y + 10, 14, c, 2.2) + t(50, y + 16, n, 9.5, INK, "khand") + t(218, y + 16, tm, 6.5, MUTE, "hind", 600, "end")
    if note: s += t(50, y + 28, note, 6.8, MUTE)
    return s
def ask(y, txt="Tell Prop Anything..."): return rect(14, y, 212, 28, "#FFFFFF", INK, 6, 1.2) + ic("mic", 22, y + 6, 16, TERRA, 2.2) + t(44, y + 18, txt, 8, "#9A948A") + rect(196, y + 5, 24, 18, TERRA, "none", 4) + ic("chev", 202, y + 8, 12, "#FFFFFF", 2.4)
def pilltabs(y, names=("Now", "Owed", "Apps", "Log"), c=INK, style="pill"):
    n = len(names); w = 212 / n; s = ""
    if style == "pill": s += rect(14, y, 212, 22, SOFT, "none", 11) + rect(16, y + 2, w - 4, 18, "#FFFFFF", LINE, 9)
    elif style == "solid": s += rect(14, y, 212, 22, SOFT, "none", 11) + rect(16, y + 2, w - 4, 18, c, "none", 9)
    elif style == "under": s += ln(y + 22, 14, 226) + rect(14 + 8, y + 20, w - 16, 2.5, TERRA)
    elif style == "box": s += "".join(rect(14 + i * w, y, w, 22, INK if i == 0 else "#FFFFFF", INK, 0, 1.2) for i in range(n))
    for i, nm in enumerate(names):
        on = i == 0; col = "#FFFFFF" if on and style in ("solid", "box") else (INK if on else MUTE)
        s += t(14 + w * i + w / 2, y + 14.5, nm, 8, col, "khand", anchor="middle")
    return s
def monitor(body, cap, sub, wide=1.0):
    fw = 220 * wide; x0 = 120 - fw / 2
    s = rect(x0, 30, fw, 150, "#FFFFFF", "#CFC8BC", 5) + rect(x0, 30, fw, 10, SOFT, "none", 5) + "".join(dot(x0 + 7 + i * 6, 35, 1.8, "#CFC8BC") for i in range(3)) + body
    return screen(s + h1(14, 222, cap, 13) + t(14, 238, sub, 7.5, MUTE) + foot())
def mcol(x, y, w, h, c, title, n=4):
    return rect(x, y, w, h, "#FFFFFF", LINE, 3) + rect(x, y, w, 2.5, c, "none", 1) + t(x + 4, y + 10, title, 5, INK, "khand") + "".join(rect(x + 4, y + 15 + k * ((h - 19) / n), w - 8, (h - 19) / n - 3, SOFT, "none", 2) for k in range(n))

# ================= Re-asks of the 13 skipped pairs (fresh forms) =================
G = "Re-Asks"
def statrow(kind):
    items = [("Site Build", JUNGLE, "Done", 1.0), ("Tax Draft", SAFFRON, "Waiting", .5), ("Polo Order", TERRA, "Blocked", .2), ("Deck Round 2", LAGOON, "Running", .7)]
    s = band() + upd() + section(84, "Status")
    for i, (n, c, st, f) in enumerate(items):
        y = 92 + i * 40; s += rect(14, y, 212, 34, "#FFFFFF", LINE, 8) + t(24, y + 21, n, 10, INK, "khand")
        if kind == "ring": s += ringp(206, y + 17, 9, f, c) + t(190, y + 20, st, 6.8, c, "hind", 600, "end")
        elif kind == "solid": s += tag(150, y + 12, st, c, True)
        elif kind == "chip": s += tag(150, y + 12, st, c)
        elif kind == "dot": s += dot(156, y + 17, 3.5, c) + t(164, y + 20, st, 7, INK, "hind", 600)
        elif kind == "bar": s += rect(14, y, 5, 34, c, "none", 2) + t(218, y + 20, st, 7, INK, "hind", 600, "end")
        elif kind == "word": s += t(218, y + 20, st.upper(), 7, c, "hind", 700, "end", 'letter-spacing="1"')
    return screen(s + foot())
add(G, "Status Marks", O("st_ring_side", "Ring Beside The Status Word", "Mini progress ring at the row end, word next to it.", ["visual", "focused"], "visual", statrow("ring")),
    O("st_solid_row", "Solid Pill In Each Row", "Filled color pill, white word.", ["visual", "quick"], "quick", statrow("solid")), "Ring Or Solid Pill On A Status Row?", "reask")
add(G, "Status Marks", O("st_bar_edge", "Color Edge On The Card", "Card's left edge carries the status color.", ["visual", "focused"], "focused", statrow("bar")),
    O("st_word_caps", "Colored Caps Word", "Status as a small colored word, no shape.", ["focused", "quick"], "quick", statrow("word")), "Color Edge Or Colored Word?", "reask")
add(G, "Status Marks", O("st_chip_soft", "Soft Tinted Chip", "Pale pill with the colored word.", ["visual", "quick"], "visual", statrow("chip")),
    O("st_dot_word", "Dot And Plain Word", "Small colored dot before the word.", ["focused", "quick"], "focused", statrow("dot")), "Tinted Chip Or Dot?", "reask")
def namesize(size, sub=True):
    s = band(size=size, sub="Command Center" if sub else "", h=50 if size > 16 else 46)
    return screen(s + upd(150, 58) + section(90, "Needs You") + ocard(96, "Pick Front Door", "Blueprint · 2 days") + ocard(152, "Approve Tax Draft", "Portfolio · today") + foot())
add(G, "Header Name Size", O("hn_16", "Name At 16", "A step up from small, still one line with the subtitle.", ["focused", "visual"], "focused", namesize(16)),
    O("hn_19", "Name At 19", "Just under the big hero size.", ["visual", "action"], "visual", namesize(19)), "Which In-Between Name Size?", "reask")
add(G, "Header Name Size", O("hn_18_sub", "Name At 18 With Subtitle", "Medium name, Command Center under it.", ["visual", "focused"], "visual", namesize(18)),
    O("hn_18_solo", "Name At 18, No Subtitle", "Medium name alone, centered in the band.", ["focused", "quick"], "quick", namesize(18, False)), "Subtitle Under The Medium Name?", "reask")
def badgeword(kind):
    s = band("Apps Home", INK, sub="All Agents") + section(64, "Your Agents")
    for i, (n, c, k) in enumerate(AGENTS):
        y = 72 + i * 42; cnt = [3, 0, 1, 2][i]
        s += rect(14, y, 212, 36, "#FFFFFF", LINE, 8) + mono(22, y + 7, n, c) + t(52, y + 22, n, 11, INK, "khand")
        if cnt: s += (t(218, y + 22, f"{cnt} Owed", 8, TERRA, "hind", 600, "end") if kind == "words" else tag(180, y + 13, f"{cnt} New", SAFFRON, True))
    return screen(s + foot())
add(G, "Badges", O("bd_owed_words", "'3 Owed' In Terracotta", "Words at the row end say what is waiting.", ["focused", "quick"], "focused", badgeword("words")),
    O("bd_new_pill2", "Saffron Count Pill", "Solid saffron pill at the row end.", ["visual", "action"], "visual", badgeword("pill")), "Owed Words Or Saffron Pill?", "reask")
def btnkind(kind):
    s = band() + section(64, "Decide") + ocard(72, "Pick Front Door", "Blueprint · 2 days", bstyle=kind) + ocard(130, "Approve Tax Draft", "Portfolio · today", bstyle=kind) + ocard(188, "Choose Polo Color", "Up Keep · this week", bstyle=kind)
    return screen(s + foot())
add(G, "Buttons", O("bt_outline_card", "Outline Buttons On Cards", "Black outline; fills on hover.", ["focused", "action"], "focused", btnkind("outline")),
    O("bt_link_card", "Text Links On Cards", "Underlined Yes and Not Yet.", ["quick", "focused"], "quick", btnkind("link")), "Outline Or Text Link Answers?", "reask")
add(G, "Buttons", O("bt_square_card", "Square Black Answer Buttons", "Brand square buttons, terracotta on hover.", ["action", "visual"], "quick", btnkind("square")),
    O("bt_pill_card", "Terracotta Pill Answer Buttons", "Rounded pills in the accent.", ["visual", "action"], "visual", btnkind("pill")), "Square Or Pill Answers?", "reask")
def feedk(kind):
    ev = [("Shipped Visit Log", "9:40 AM", JUNGLE, "check", "Techs can log visits from the van."), ("Updated Prices", "8:15 AM", LAGOON, "tag", "Fall rates on the price sheet."), ("Asked: Polo Color", "Yesterday", TERRA, "clock", "Waiting on your pick."), ("New Deck Ready", "Mon", SAFFRON, "star", "50 pairs, 5 minutes.")]
    s = band() + section(64, "Activity")
    y = 72
    for n, tm, c, k, note in ev:
        if kind == "note": s += feedcard(y, n, tm, c, k, note=note); y += 50
        else: s += feedcard(y, n, tm, c, k); y += 40
    return screen(s + foot())
add(G, "Feed Style", O("feed_card_note", "Icon Card With One-Line Why", "Title plus a short note under it.", ["visual", "focused"], "visual", feedk("note")),
    O("feed_card_tight", "Icon Card, Title Only", "Tighter cards; just what and when.", ["quick", "focused"], "quick", feedk("tight")), "Add A One-Line Note To Feed Cards?", "reask")
def stampk(kind):
    s = band() + (upd() if kind == "page" else "") + section(84, "Needs You")
    for i, (n, d) in enumerate(OWED): s += rect(14, 92 + i * 40, 212, 34, "#FFFFFF", LINE, 8) + dot(26, 109 + i * 40, 3.5, TERRA) + t(36, 107 + i * 40, n, 9.5, INK, "khand") + t(36, 118 + i * 40, d.split(" · ")[0], 6.5, MUTE) + (tag(186, 102 + i * 40, ["2m", "1h", "3h"][i], JUNGLE) if kind == "row" else "")
    return screen(s + foot())
add(G, "Updated Stamp", O("upd_page_badge", "One Green Badge For The Page", "Updated 12 Min Ago under the header.", ["focused", "quick"], "focused", stampk("page")),
    O("upd_row_tags", "Green Age Tag On Each Row", "2m, 1h, 3h on every card.", ["visual", "quick"], "visual", stampk("row")), "One Page Badge Or Age Per Row?", "reask")
def projk(kind):
    items = [("Visit Log", .9, JUNGLE), ("Pricing Page", .6, LAGOON), ("Tech App", .35, SAFFRON), ("Onboarding", .15, TERRA)]
    s = band() + section(64, "Projects")
    for i, (n, f, c) in enumerate(items):
        x, y = 14 + (i % 2) * 108, 72 + (i // 2) * 84
        s += rect(x, y, 104, 78, "#FFFFFF", LINE, 8) + t(x + 10, y + 18, n, 10, INK, "khand")
        if kind == "bar": s += t(x + 10, y + 50, f"{int(f*100)}%", 18, c, "khand") + pbar(x + 10, y + 60, 84, f, c)
        else: s += ringp(x + 52, y + 46, 18, f, c, f"{int(f*100)}%")
    return screen(s + foot())
add(G, "Progress", O("pr_bar_card", "Big Percent Plus Thin Bar", "Your big-number pick with a bar under it.", ["visual", "focused"], "focused", projk("bar")),
    O("pr_ring_card", "Ring In Each Card", "One ring per project card.", ["visual", "quick"], "visual", projk("ring")), "Thin Bar Or Ring Under The Number?", "reask")
def tilek(kind):
    names = [("Smart Upkeep", "home"), ("Visit Log", "cal"), ("Billing", "card"), ("Price Sheet", "tag")]
    s = band() + section(64, "Apps")
    for i, (n, k) in enumerate(names):
        x, y = 14 + (i % 2) * 108, 72 + (i // 2) * 96; c = ACC[i]
        s += rect(x, y, 104, 90, "#FFFFFF", LINE, 10)
        if kind == "shot": s += rect(x + 6, y + 6, 92, 50, SOFT, "none", 6) + rect(x + 6, y + 6, 92, 10, c, "none", 6) + rect(x + 12, y + 24, 60, 3, "#D6D0C6") + rect(x + 12, y + 32, 46, 3, "#D6D0C6") + rect(x + 12, y + 42, 24, 8, INK)
        else: s += rect(x, y, 104, 50, c, "none", 10) + rect(x, y + 40, 104, 10, c) + ic(k, x + 40, y + 13, 24, "#FFFFFF", 2.2)
        s += t(x + 10, y + 74, n, 10, INK, "khand")
    return screen(s + foot())
add(G, "App Tiles", O("tile_preview2", "Tile With A Tiny App Preview", "Each tile shows a mini screen of the app.", ["visual", "focused"], "visual", tilek("shot")),
    O("tile_colortop", "Tile With A Solid Color Top", "Color block and white icon, name below.", ["visual", "quick"], "quick", tilek("color")), "App Preview Or Color Top?", "reask")
def mbcols(kind):
    if kind == "cols": body = "".join(mcol(18 + i * 70, 46, 64, 128, ACC[i], ["Owed", "Status", "Apps"][i]) for i in range(3))
    else: body = mcol(85, 46, 70, 128, TERRA, "Owed", 6)
    return monitor(body, "Desktop Spreads To 3 Columns" if kind == "cols" else "One Phone Column, Centered", "On a laptop or monitor; phone stays one column.")
add(G, "Desktop Layout", O("pd_cols_laptop", "Three Columns On Desktop", "Owed, Status, Apps side by side.", ["focused", "visual"], "visual", mbcols("cols")),
    O("pd_column_laptop", "Phone Column On Desktop", "Same narrow column, centered.", ["focused", "quick"], "focused", mbcols("one")), "Columns Or A Phone Column On Desktop?", "reask")
def calk(kind):
    s = band() + section(64, "Coming Up")
    if kind == "gantt":
        s += "".join(f'<line x1="{84+i*36}" y1="74" x2="{84+i*36}" y2="210" stroke="{LINE}"/>' + t(84 + i * 36, 222, ["Oct", "Nov", "Dec", "Jan"][i], 6.5, MUTE, anchor="middle") for i in range(4))
        s += "".join(t(14, 92 + i * 32, n, 8.5, INK, "khand") + rect(x0, 83 + i * 32, w, 12, c, "none", 6) for i, (n, x0, w, c) in enumerate([("Visit Log", 84, 40, JUNGLE), ("Pricing", 104, 60, LAGOON), ("Tech App", 134, 70, SAFFRON), ("Launch", 184, 30, TERRA)]))
    else:
        s += "".join(rect(14, 72 + i * 44, 212, 38, "#FFFFFF", LINE, 8) + rect(14, 72 + i * 44, 38, 38, c + "1F", "none", 8) + t(33, 92 + i * 44, dd, 14, c, "khand", anchor="middle") + t(33, 103 + i * 44, mm, 5.5, c, "hind", 600, "middle") + t(62, 89 + i * 44, n, 10, INK, "khand") + t(62, 100 + i * 44, w, 6.5, MUTE) for i, (dd, mm, n, w, c) in enumerate([("15", "THU", "Pricing Call", "10:00 AM · Prop", LAGOON), ("16", "FRI", "Tax Draft Due", "Portfolio", SAFFRON), ("19", "MON", "Ship Tech App", "Up Keep", JUNGLE), ("23", "FRI", "Site Launch", "Prop", TERRA)]))
    return screen(s + foot())
add(G, "Calendar", O("cal_gantt2", "Project Bars Across Months", "Each project as a colored bar.", ["visual", "focused"], "visual", calk("gantt")),
    O("cal_datecards", "Date Tile Agenda Cards", "Colored date square, event beside it.", ["quick", "action"], "quick", calk("agenda")), "Timeline Bars Or Date Cards?", "reask")

# ================= Winners vs strong alternatives =================
G = "Winners Vs Strong Alternatives"
def identk(kind):
    s = band("Apps Home", INK, sub="All Agents") + section(64, "Your Agents")
    for i, (n, c, k) in enumerate(AGENTS):
        y = 72 + i * 44; s += rect(14, y, 212, 38, "#FFFFFF", LINE, 8) + (rect(14, y, 5, 38, c, "none", 2) if kind == "both" else "") + mono(26, y + 8, n, c, 22, kind == "solid") + t(58, y + 23, n, 11, INK, "khand")
    return screen(s + foot())
add(G, "Agent Identity", O("id_letter_stripe", "Letter Circle Plus Color Stripe", "Both of your picks on one card.", ["visual", "focused"], "visual", identk("both")),
    O("id_letter_solid", "Solid Color Circle, White Letter", "Bolder filled letter circle, no stripe.", ["visual", "quick"], "quick", identk("solid")), "Stripe And Letter, Or A Solid Letter?", "winner")
def hdrk(kind):
    s = band() if kind == "band" else (t(42, 22, "Prop", 13, INK, "khand") + mono(14, 11, "Prop", TERRA) + t(42, 33, "Command Center", 6.5, MUTE) + shareic(206, 14) + rect(0, 42, W, 3, TERRA))
    return screen(s + upd() + section(84, "Needs You") + ocard(92, "Pick Front Door", "Blueprint · 2 days") + ocard(148, "Approve Tax Draft", "Portfolio · today") + foot())
add(G, "Header Style", O("hdr_band_keep", "Solid Color Band (Your Pick)", "Agent color fills the top bar.", ["visual", "action"], "visual", hdrk("band")),
    O("hdr_white_rule", "White Header, Thick Color Rule", "White bar with a 3px agent-color line under it.", ["focused", "visual"], "focused", hdrk("rule")), "Full Band Or A Color Rule?", "winner")
def owedk(kind):
    s = band() + section(64, "Needs You")
    if kind == "inline": s += ocard(72, "Pick Front Door", "Blueprint · 2 days") + ocard(128, "Approve Tax Draft", "Portfolio · today") + ocard(184, "Choose Polo Color", "Up Keep · this week")
    else: s += rect(20, 78, 212, 150, "#FFFFFF", LINE, 10) + rect(14, 72, 212, 150, "#FFFFFF", LINE, 10) + lbl(26, 92, "1 Of 3", TERRA) + h1(26, 122, "Pick Front Door", 16) + t(26, 138, "Blueprint · 2 days", 7.5, MUTE) + rect(26, 160, 90, 40, SOFT, "none", 6) + rect(124, 160, 90, 40, SOFT, "none", 6) + t(71, 184, "Oak", 10, INK, "khand", anchor="middle") + t(169, 184, "Black Steel", 10, INK, "khand", anchor="middle")
    return screen(s + foot())
add(G, "Decisions Owed", O("ow_inline_keep", "Answer Buttons Inline (Your Pick)", "All three owed calls with answer buttons.", ["action", "quick"], "action", owedk("inline")),
    O("ow_swipe_card", "One Decision At A Time", "Stacked card; tap an answer to see the next.", ["focused", "action"], "focused", owedk("stack")), "List Of Answers Or One At A Time?", "winner")
def tilesk(kind):
    s = band() + section(64, "Apps")
    names = [("Upkeep", "home"), ("Visits", "cal"), ("Billing", "card"), ("Prices", "tag"), ("Reviews", "star"), ("Docs", "search")]
    for i, (n, k) in enumerate(names):
        x, y = 14 + (i % 3) * 72, 72 + (i // 3) * 80; c = ACC[i % 4]
        if kind == "square": s += rect(x, y, 66, 72, "#FFFFFF", LINE, 10) + rect(x + 19, y + 10, 28, 28, c + "1F", "none", 7) + ic(k, x + 24, y + 15, 18, c, 2.2)
        else: s += f'<circle cx="{x+33}" cy="{y+26}" r="22" fill="{c}1F"/>' + ic(k, x + 22, y + 15, 22, c, 2.2)
        s += t(x + 33, y + 60, n, 9, INK, "khand", anchor="middle")
    return screen(s + foot())
add(G, "App Tiles", O("tile_square_keep", "Square Icon Tiles (Your Pick)", "Tinted square in a white tile.", ["visual", "quick"], "visual", tilesk("square")),
    O("tile_round_bare", "Round Tinted Icons, No Tile", "Phone-home-screen style circles.", ["visual", "focused"], "quick", tilesk("round")), "Square Tiles Or Bare Round Icons?", "winner")
def pinwhich(kind):
    s = band()
    if kind == "strip": s += pinstrip(54) + rect(14, 80, 212, 22, SAFFRON + "14", "none", 6) + ic("star", 22, 85, 12, SAFFRON) + t(40, 95, "Q4 Price Sheet", 9, INK, "khand"); y = 116
    else: s += "".join(rect(14 + i * 96, 54, 90, 18, SAFFRON + "1F", "none", 9) + ic("star", 20 + i * 96, 57, 11, SAFFRON) + t(34 + i * 96, 66, n, 7, INK, "hind", 600) for i, n in enumerate(["Site Launch", "Q4 Prices"])); y = 88
    s += section(y, "Needs You") + ocard(y + 8, "Pick Front Door", "Blueprint · 2 days") + ocard(y + 64, "Approve Tax Draft", "Portfolio · today")
    return screen(s + foot())
add(G, "Pinned", O("pin_strip_rows", "Pinned Strip, One Row Each", "Saffron rows above everything.", ["focused", "visual"], "visual", pinwhich("strip")),
    O("pin_chip_row", "Pinned Chips In One Line", "Small saffron chips under the header.", ["quick", "focused"], "quick", pinwhich("chips")), "You Picked Both: Strip Or Chips?", "winner")
def homek(kind):
    if kind == "grid":
        s = band() + "".join(rect(14 + (i % 2) * 108, 54 + (i // 2) * 76, 104, 70, "#FFFFFF", LINE, 8) + rect(22 + (i % 2) * 108, 62 + (i // 2) * 76, 22, 22, ACC[i % 4] + "1F", "none", 6) + ic(["clock", "check", "star", "home", "cal", "tag"][i], 25 + (i % 2) * 108, 65 + (i // 2) * 76, 16, ACC[i % 4], 2.2) + t(22 + (i % 2) * 108, 100 + (i // 2) * 76, ["Owed", "Status", "Pinned", "Apps", "Calendar", "Feed"][i], 11, INK, "khand") + t(22 + (i % 2) * 108, 112 + (i // 2) * 76, ["3 Calls", "All Green", "2 Items", "6 Links", "Thu 10 AM", "Shipped 1h"][i], 7, MUTE) for i in range(6))
    else: s = band() + pilltabs(52) + section(90, "Needs You") + ocard(98, "Pick Front Door", "Blueprint · 2 days") + ocard(154, "Approve Tax Draft", "Portfolio · today")
    return screen(s + foot())
add(G, "Home Layout", O("lay_grid_keep", "Grid Of Section Cards", "Six cards; tap one to open it.", ["visual", "quick"], "visual", homek("grid")),
    O("lay_tabs_keep", "Pill Tabs Across The Top", "Now, Owed, Apps, Log as tabs.", ["focused", "action"], "focused", homek("tabs")), "You Picked Both: Grid Or Tabs?", "winner")
def chartk(kind):
    vals = [.3, .45, .4, .6, .55, .7, .85]
    s = band() + section(64, "Work Shipped Per Day") + rect(14, 72, 212, 140, "#FFFFFF", LINE, 8)
    if kind == "plain": s += bars(24, 90, 192, 100, vals)
    else:
        s += bars(24, 96, 192, 94, vals, JUNGLE) + "".join(t(24 + i * 27.4 + 13.7, 92 + 94 - 94 * v, str(int(v * 20)), 6.5, INK, "hind", 600, "middle") for i, v in enumerate(vals)) + "".join(t(24 + i * 27.4 + 13.7, 202, d, 6, MUTE, "hind", 600, "middle") for i, d in enumerate("MTWTFSS"))
    return screen(s + foot())
add(G, "Charts", O("ch_bars_keep", "Simple Bar Chart (Your Pick)", "Bars only, today darker.", ["visual", "focused"], "focused", chartk("plain")),
    O("ch_bars_labels", "Bars With Numbers And Days", "Count on each bar, day letters under.", ["visual", "quick"], "visual", chartk("labels")), "Plain Bars Or Labeled Bars?", "winner")
def calw(kind):
    s = band() + section(64, "This Week" if kind == "one" else "Next Two Weeks")
    n = 7 if kind == "one" else 14; sp = 30 if n == 7 else 15
    s += "".join((f'<circle cx="{30+i*sp}" cy="{92}" r="{9 if n==7 else 6.5}" fill="{TERRA}"/>' if i == 1 else "") + t(30 + i * sp, 80, "MTWTFSS"[i % 7], 6.5, MUTE, "hind", 600, "middle") + t(30 + i * sp, 96, str(12 + i), 10 if n == 7 else 7.5, "#FFFFFF" if i == 1 else INK, "khand", anchor="middle") + (dot(30 + i * sp, 106, 2, LAGOON) if i in (3, 4, 9, 11) else "") for i in range(n))
    s += "".join(row(120 + i * 40, nm, d, c, k="cal") for i, (nm, d, c) in enumerate([("Pricing Call", "Thu 10 AM", LAGOON), ("Tax Draft Due", "Fri", SAFFRON), ("Ship Tech App", "Next Mon", JUNGLE)]))
    return screen(s + foot())
add(G, "Calendar", O("cal_week_keep", "One Week Strip (Your Pick)", "Seven days, events below.", ["focused", "quick"], "focused", calw("one")),
    O("cal_two_weeks", "Two-Week Strip", "Fourteen days across, smaller numbers.", ["visual", "focused"], "visual", calw("two")), "One Week Or Two?", "winner")
def actk(kind):
    if kind == "row": s = band() + actrow(52) + section(108, "Needs You") + ocard(116, "Pick Front Door", "Blueprint · 2 days") + ocard(172, "Approve Tax Draft", "Portfolio · today")
    else:
        s = rect(0, 0, W, 72, TERRA) + mono(14, 11, "Prop", "#FFFFFF", fg=TERRA) + t(42, 22, "Prop", 13, "#FFFFFF", "khand") + t(42, 33, "Command Center", 6.5, "#FFFFFFCC") + shareic(208, 14, "#FFFFFF")
        s += "".join(rect(14 + i * 54, 44, 48, 20, "#FFFFFF33", "none", 10) + t(38 + i * 54, 57, n, 7, "#FFFFFF", "hind", 600, "middle") for i, n in enumerate(["Share", "Ask", "Note", "Open"])) + section(92, "Needs You") + ocard(100, "Pick Front Door", "Blueprint · 2 days") + ocard(156, "Approve Tax Draft", "Portfolio · today")
    return screen(s + foot())
add(G, "Quick Actions", O("qa_row_keep", "Icon Action Row Under The Band", "Four tinted icon buttons (your pick).", ["action", "visual"], "action", actk("row")),
    O("qa_in_band", "Action Pills Inside The Band", "Share, Ask, Note, Open as white pills in the header.", ["quick", "action"], "quick", actk("band")), "Actions Below Or Inside The Band?", "winner")
def countk(kind):
    s = band("Apps Home", INK, sub="All Agents") + section(64, "Your Agents")
    for i, (n, c, k) in enumerate(AGENTS):
        y = 72 + i * 44; cnt = [3, 0, 1, 2][i]
        s += rect(14, y, 212, 38, "#FFFFFF", LINE, 8) + mono(24, y + 8, n, c) + t(56, y + 23, n, 11, INK, "khand")
        if cnt:
            if kind == "corner": s += f'<circle cx="44" cy="{y+9}" r="6.5" fill="{TERRA}" stroke="#FFFFFF" stroke-width="1.4"/>' + t(44, y + 11.6, str(cnt), 7, "#FFFFFF", "hind", 700, "middle")
            else: s += f'<circle cx="208" cy="{y+19}" r="8" fill="{TERRA}"/>' + t(208, y + 22, str(cnt), 8, "#FFFFFF", "hind", 700, "middle")
    return screen(s + foot())
add(G, "Badges", O("bd_corner_keep", "Count On The Icon Corner (Your Pick)", "Red-orange bubble on the letter circle.", ["visual", "quick"], "visual", countk("corner")),
    O("bd_row_end", "Count Bubble At The Row End", "Same bubble, right side of the card.", ["focused", "quick"], "focused", countk("end")), "Bubble On Icon Or At Row End?", "winner")

def emptyk(kind):
    s = band() + upd()
    if kind == "line": s += section(84, "Needs You") + t(14, 100, "Nothing waiting on you.", 8.5, MUTE) + ln(110) + section(130, "Latest Work") + feedcard(138, "Shipped Visit Log", "1h", JUNGLE, "check") + feedcard(178, "Updated Prices", "3h", LAGOON, "tag")
    else: s += section(84, "Latest Work") + feedcard(92, "Shipped Visit Log", "1h", JUNGLE, "check") + feedcard(132, "Updated Prices", "3h", LAGOON, "tag") + section(186, "Apps") + sqtiles(194)
    return screen(s + foot())
add(G, "Empty State", O("em_line_keep", "Keep The Heading, One Grey Line", "Needs You stays with a quiet line.", ["focused", "quick"], "focused", emptyk("line")),
    O("em_hide_keep", "Hide The Empty Section", "Needs You disappears when empty.", ["focused", "visual"], "quick", emptyk("hide")), "You Picked Both: Line Or Hide?", "winner")

# ================= Combined full-dashboard looks =================
G = "Full Dashboard Looks"
def full(kind):
    s = band(size=17, badge=False)
    if kind == "actions": s += actrow(52) + pinstrip(98) + section(132, "Needs You") + ocard(138, "Pick Front Door", "Blueprint · 2 days") + ocard(194, "Approve Tax Draft", "Portfolio · today") + upd(150, 248)
    elif kind == "feed": s += upd(14, 52) + pinstrip(72) + section(106, "Needs You") + ocard(112, "Pick Front Door", "Blueprint · 2 days") + section(176, "Latest Work") + feedcard(182, "Shipped Visit Log", "1h", JUNGLE, "check") + feedcard(222, "Updated Prices", "3h", LAGOON, "tag")
    elif kind == "tabs": s += pilltabs(52) + upd(150, 80) + section(104, "Needs You") + ocard(110, "Pick Front Door", "Blueprint · 2 days") + ocard(166, "Approve Tax Draft", "Portfolio · today") + ask(226)
    elif kind == "tiles": s += upd(14, 52) + section(84, "Needs You") + ocard(90, "Pick Front Door", "Blueprint · 2 days") + section(152, "Apps") + sqtiles(158) + ask(220)
    elif kind == "ask_top": s += ask(52) + pinstrip(88) + section(122, "Needs You") + ocard(128, "Pick Front Door", "Blueprint · 2 days") + ocard(184, "Approve Tax Draft", "Portfolio · today") + upd(150, 244)
    elif kind == "dense": s += actrow(50) + upd(150, 96) + section(104, "Needs You") + ocard(110, "Pick Front Door", "Blueprint · 2 days", h=46) + ocard(160, "Approve Tax Draft", "Portfolio · today", h=46) + sqtiles(212, 4)
    elif kind == "gridask": s += upd(150, 50) + "".join(rect(14 + (i % 2) * 108, 70 + (i // 2) * 52, 104, 46, "#FFFFFF", LINE, 8) + rect(22 + (i % 2) * 108, 78 + (i // 2) * 52, 18, 18, ACC[i % 4] + "1F", "none", 5) + ic(["clock", "check", "star", "home"][i], 25 + (i % 2) * 108, 81 + (i // 2) * 52, 12, ACC[i % 4], 2.2) + t(46 + (i % 2) * 108, 91 + (i // 2) * 52, ["3 Owed", "All Green", "2 Pinned", "6 Apps"][i], 10, INK, "khand") for i in range(4)) + section(186, "Latest Work") + feedcard(192, "Shipped Visit Log", "1h", JUNGLE, "check") + ask(234)
    elif kind == "tabsact": s += actrow(50) + pilltabs(98) + section(134, "Needs You") + ocard(140, "Pick Front Door", "Blueprint · 2 days") + ocard(196, "Approve Tax Draft", "Portfolio · today")
    return screen(s + foot())
def fulldesk(kind):
    if kind == "mba":
        body = rect(10, 40, 220, 14, TERRA) + t(16, 50, "Prop", 8, "#FFFFFF", "khand") + "".join(mcol(16 + i * 70, 60, 64, 116, c, nm) for i, (c, nm) in enumerate([(TERRA, "Needs You"), (JUNGLE, "Latest Work"), (LAGOON, "Apps")]))
        return monitor(body, "MacBook: Band Plus 3 Columns", "Owed, latest work, app tiles side by side.")
    body = rect(10, 40, 220, 14, TERRA) + t(16, 50, "Prop", 8, "#FFFFFF", "khand") + rect(16, 58, 208, 10, SOFT, "none", 3) + "".join(mcol(16 + i * 52.5, 72, 48, 104, c, nm, 5) for i, (c, nm) in enumerate([(TERRA, "Needs You"), (SAFFRON, "Pinned"), (JUNGLE, "Work"), (LAGOON, "Apps")]))
    return monitor(body, "Monitor: Band, Ask Bar, 4 Columns", "Capped width; ask bar runs across the top.")
add(G, "Full Look", O("full_actions", "Band, Action Row, Pins, Owed", "Action-first: your header, icon row, pinned strip, inline answers.", ["action", "visual"], "action", full("actions")),
    O("full_feed", "Band, Pins, Owed, Feed Cards", "Work-first: one owed card, then icon-card feed.", ["visual", "focused"], "visual", full("feed")), "Which Full Phone Look?", "combo")
add(G, "Full Look", O("full_tabs", "Pill Tabs Plus Ask Box", "Tabs up top, owed cards, ask box at the bottom.", ["focused", "action"], "focused", full("tabs")),
    O("full_tiles", "Owed, App Tiles, Ask Box", "One owed card, square tiles, ask box.", ["visual", "quick"], "quick", full("tiles")), "Tabs Look Or Tiles Look?", "combo")
add(G, "Full Look", O("full_ask_top", "Ask Box First, Then Pins And Owed", "Talk to the agent before anything else.", ["action", "focused"], "action", full("ask_top")),
    O("full_dense", "Actions, Owed, Tiles On One Screen", "Everything above the fold, slightly tighter.", ["quick", "visual"], "quick", full("dense")), "Ask-First Or All-In-View?", "combo")
add(G, "Full Look", O("full_grid_ask", "Section Grid, Feed Card, Ask Box", "Four summary cards lead; ask box at the bottom.", ["visual", "quick"], "visual", full("gridask")),
    O("full_tabs_actions", "Action Row Over Pill Tabs", "Icon actions, then tabs, then owed answers.", ["action", "focused"], "action", full("tabsact")), "Grid Summary Or Tabs With Actions?", "combo")
add(G, "Full Look", O("full_mba", "MacBook Full Look", "Band plus three columns.", ["visual", "focused"], "focused", fulldesk("mba")),
    O("full_monitor", "Big Monitor Full Look", "Band, ask bar and four columns.", ["visual", "action"], "visual", fulldesk("mon")), "Which Desktop Look Feels Right?", "combo")

# ================= New areas =================
G = "Agent Color Per Group"
def grpcol(kind):
    gs = [("Work", TERRA, ["Prop", "Up Keep", "Blueprint"]), ("Personal", JUNGLE, ["WellNest", "Portfolio"]), ("AI Resources", LAGOON, ["Style Swipe"])]
    s = band("Apps Home", INK, sub="All Agents"); y = 56; idx = 0
    for g, gc, ag in gs:
        s += rect(14, y, 4, 12, gc) + t(24, y + 10, g, 10, INK, "khand"); y += 18
        for n in ag:
            c = gc if kind == "group" else ACC[idx % 4]; idx += 1
            s += rect(14, y, 212, 28, "#FFFFFF", LINE, 8) + mono(22, y + 4, n, c, 20) + t(50, y + 18, n, 9.5, INK, "khand"); y += 32
        y += 4
    return screen(s + foot())
add(G, "Group Colors", O("gc_group", "One Color Per Group", "Work terracotta, Personal jungle, AI lagoon.", ["visual", "focused"], "focused", grpcol("group")),
    O("gc_each", "Each Agent Its Own Color", "Four accents rotate across all agents.", ["visual", "quick"], "visual", grpcol("each")), "Group Color Or Agent Color?", "new")
def grpshade(kind):
    s = band("Apps Home", INK, sub="All Agents") + section(64, "Work")
    for i, n in enumerate(["Prop", "Up Keep", "Blueprint", "Branding"]):
        y = 72 + i * 42; c = TERRA
        if kind == "tint": s += rect(14, y, 212, 36, c + "14", "none", 8) + mono(22, y + 7, n, c, 22, True) + t(52, y + 22, n, 11, INK, "khand")
        else: s += rect(14, y, 212, 36, "#FFFFFF", LINE, 8) + rect(14, y, 5, 36, c, "none", 2) + mono(26, y + 7, n, [TERRA, LAGOON, JUNGLE, SAFFRON][i], 22) + t(56, y + 22, n, 11, INK, "khand")
    return screen(s + foot())
add(G, "Group Colors", O("gc_tint_cards", "Group-Tinted Cards", "Whole card washes in the group color.", ["visual", "focused"], "visual", grpshade("tint")),
    O("gc_edge_mixed", "Group Edge, Agent Letter Color", "Edge shows the group; letter shows the agent.", ["visual", "quick"], "quick", grpshade("edge")), "Tinted Cards Or Edge Plus Agent Color?", "new")
G = "Card Corner Radius"
def radius(r):
    return screen(band() + section(64, "Needs You") + ocard(72, "Pick Front Door", "Blueprint · 2 days", r) + ocard(128, "Approve Tax Draft", "Portfolio · today", r) + section(192, "Apps") + sqtiles(200, 4, r=r) + foot())
add(G, "Corners", O("rad_0", "Square Corners", "Sharp 0px edges, like the brand buttons.", ["focused", "quick"], "focused", radius(0)),
    O("rad_6", "Small 6px Round", "Just softened.", ["visual", "focused"], "quick", radius(6)), "Square Or Slightly Round?", "new")
add(G, "Corners", O("rad_10", "Medium 10px Round", "Clear app-like rounding.", ["visual", "quick"], "visual", radius(10)),
    O("rad_16", "Large 16px Round", "Soft pill-ish cards.", ["visual", "action"], "visual", radius(16)), "Medium Or Large Round?", "new")
G = "Tab Style"
def tabk(st):
    return screen(band() + pilltabs(54, style=st) + section(94, "Needs You") + ocard(102, "Pick Front Door", "Blueprint · 2 days") + ocard(158, "Approve Tax Draft", "Portfolio · today") + foot())
add(G, "Tabs", O("tab_pill_white", "White Pill On Grey Track", "Your pick, kept soft.", ["focused", "visual"], "focused", tabk("pill")),
    O("tab_underline", "Terracotta Underline", "Plain words, colored bar under the active one.", ["focused", "quick"], "quick", tabk("under")), "Pill Or Underline Tabs?", "new")
add(G, "Tabs", O("tab_pill_black", "Black Active Pill", "Active tab fills ink, white word.", ["visual", "action"], "visual", tabk("solid")),
    O("tab_square_box", "Square Boxed Tabs", "Outlined boxes; active one fills black.", ["focused", "action"], "action", tabk("box")), "Black Pill Or Square Boxes?", "new")
G = "Ask-Box Placement"
def askpos(kind):
    s = band()
    if kind == "top": s += ask(52) + section(96, "Needs You") + ocard(104, "Pick Front Door", "Blueprint · 2 days") + ocard(160, "Approve Tax Draft", "Portfolio · today")
    elif kind == "bottom": s += section(64, "Needs You") + ocard(72, "Pick Front Door", "Blueprint · 2 days") + ocard(128, "Approve Tax Draft", "Portfolio · today") + rect(0, 236, W, 64, "#FFFFFF") + ln(236, 0, W) + ask(244)
    elif kind == "after": s += section(64, "Needs You") + ocard(72, "Pick Front Door", "Blueprint · 2 days") + ocard(128, "Approve Tax Draft", "Portfolio · today") + ask(188) + section(232, "Latest Work") + t(14, 248, "Shipped Visit Log · 1h", 7.5, MUTE)
    else: s += section(64, "Needs You") + ocard(72, "Pick Front Door", "Blueprint · 2 days") + ocard(128, "Approve Tax Draft", "Portfolio · today") + rect(118, 248, 108, 28, TERRA, "none", 14, extra='filter="drop-shadow(0 2px 3px #0003)"') + ic("mic", 128, 254, 16, "#FFFFFF", 2.2) + t(150, 266, "ASK PROP", 8, "#FFFFFF", "hind", 600, extra='letter-spacing="1"')
    return screen(s + (foot() if kind not in ("bottom",) else ""))
add(G, "Ask Box", O("ask_top", "Ask Box Right Under The Header", "First thing on the page.", ["action", "quick"], "action", askpos("top")),
    O("ask_bottom", "Ask Box Stuck To The Bottom", "Always there by your thumb, like a chat.", ["action", "focused"], "quick", askpos("bottom")), "Ask Box Up Top Or At The Bottom?", "new")
add(G, "Ask Box", O("ask_after_owed", "Ask Box After What's Owed", "Owed first, then tell the agent anything.", ["focused", "action"], "focused", askpos("after")),
    O("ask_float", "Floating Ask Button", "Terracotta pill opens the ask box.", ["quick", "visual"], "visual", askpos("float")), "Inline Box Or Floating Button?", "new")
G = "Large-Monitor Layout"
def bigmon(kind):
    if kind == "cap": body = rect(10, 40, 220, 150, SOFT) + rect(30, 40, 180, 140, "#FFFFFF") + "".join(mcol(34 + i * 44, 50, 40, 124, ACC[i], ["Owed", "Pinned", "Work", "Apps"][i], 5) for i in range(4)); cap, sub = "4 Columns, Capped Width", "Content stops at 1680px; grey margins on the sides."
    elif kind == "full": body = "".join(mcol(14 + i * 36, 48, 33, 126, ACC[i % 4], ["Owed", "Pinned", "Work", "Apps", "Cal", "Stats"][i], 5) for i in range(6)); cap, sub = "6 Columns, Edge To Edge", "Every section visible across the whole screen."
    elif kind == "rail": body = rect(10, 40, 30, 140, SOFT) + "".join(mono(15, 48 + k * 24, n, c, 18) for k, (n, c, _) in enumerate(AGENTS)) + "".join(mcol(46 + i * 46, 48, 42, 126, ACC[i], ["Owed", "Pinned", "Work", "Apps"][i], 5) for i in range(4)); cap, sub = "Agent Rail Plus 4 Columns", "Switch agents from a left rail."
    else: body = rect(14, 46, 130, 128, "#FFFFFF", TERRA, 4, 1.2) + t(20, 60, "Needs You", 7, INK, "khand") + "".join(rect(20, 66 + k * 26, 118, 22, SOFT, "none", 3) for k in range(4)) + "".join(mcol(150, 46 + k * 44, 76, 40, ACC[k + 1], ["Work", "Apps", "Cal"][k], 2) for k in range(3)); cap, sub = "Big Owed Panel, Side Stack", "Owed gets the left two-thirds."
    return monitor(body, cap, sub)
add(G, "Big Monitor", O("mon_cap4", "4 Columns, Capped Width", "Centered, stops at 1680px.", ["focused", "visual"], "focused", bigmon("cap")),
    O("mon_full6", "6 Columns Edge To Edge", "Uses the whole monitor.", ["visual", "quick"], "visual", bigmon("full")), "Capped Or Edge To Edge?", "new")
add(G, "Big Monitor", O("mon_rail", "Agent Rail Plus Columns", "Agent letters down the left.", ["quick", "visual"], "quick", bigmon("rail")),
    O("mon_owed_big", "Big Owed Panel With Side Stack", "Decisions take the main space.", ["action", "focused"], "action", bigmon("owed")), "Agent Rail Or Owed Panel?", "new")
G = "MacBook Width"
def mba(kind):
    if kind == "3": body = "".join(mcol(16 + i * 70, 46, 64, 128, ACC[i], ["Owed", "Work", "Apps"][i]) for i in range(3)); cap = "3 Even Columns At 1470"
    elif kind == "2": body = mcol(16, 46, 130, 128, TERRA, "Owed And Pins", 5) + mcol(152, 46, 72, 128, LAGOON, "Work And Apps", 5); cap = "Wide Main Plus Narrow Side"
    elif kind == "grid": body = "".join(mcol(16 + (i % 3) * 70, 46 + (i // 3) * 66, 64, 60, ACC[i % 4], ["Owed", "Pinned", "Work", "Apps", "Cal", "Stats"][i], 2) for i in range(6)); cap = "Card Grid, 3 Across"
    else: body = rect(10, 40, 40, 140, SOFT) + "".join(t(16, 56 + k * 14, n, 5.5, INK if k == 0 else MUTE, "hind", 600) for k, n in enumerate(["Now", "Owed", "Apps", "Log"])) + "".join(mcol(56 + i * 85, 46, 80, 128, ACC[i], ["Owed", "Work"][i]) for i in range(2)); cap = "Side Menu Plus 2 Columns"
    return monitor(body, cap, "MacBook Air screen, about 1470px wide.")
add(G, "MacBook", O("mba_3cols", "3 Even Columns", "Owed, Work, Apps side by side.", ["visual", "focused"], "visual", mba("3")),
    O("mba_main_side", "Wide Main, Narrow Side", "Owed big on the left; work and apps on the right.", ["focused", "action"], "focused", mba("2")), "Even Columns Or Main Plus Side?", "new")
add(G, "MacBook", O("mba_grid6", "Six-Card Grid", "Your grid pick, three across.", ["visual", "quick"], "quick", mba("grid")),
    O("mba_menu2", "Side Menu Plus Two Columns", "Tabs become a left menu.", ["focused", "quick"], "focused", mba("menu")), "Card Grid Or Side Menu?", "new")
G = "Notification Panel"
def notif(kind):
    s = band() + section(64, "Needs You") + ocard(72, "Pick Front Door", "Blueprint · 2 days")
    items = [("Prop", TERRA, "Asked: Polo Color", "2m"), ("Blueprint", LAGOON, "New Deck Ready", "1h"), ("WellNest", JUNGLE, "Shipped Visit Log", "3h"), ("Portfolio", SAFFRON, "Tax Draft Waiting", "Yday")]
    if kind == "drop":
        s += f'<circle cx="190" cy="20" r="0"/>' + bell(182, 14, 14, "#FFFFFF") + rect(64, 46, 168, 168, "#FFFFFF", LINE, 8, extra='filter="drop-shadow(0 3px 5px #0003)"') + lbl(74, 62, "Notifications", INK)
        s += "".join(mono(72, 70 + i * 34, n, c, 18) + t(96, 81 + i * 34, m, 8.5, INK, "khand") + t(96, 90 + i * 34, n, 6, MUTE) + t(224, 81 + i * 34, tm, 6, MUTE, "hind", 600, "end") for i, (n, c, m, tm) in enumerate(items))
    elif kind == "sheet":
        s += bell(182, 14, 14, "#FFFFFF") + rect(0, 0, W, H, "#0A0A0A55") + rect(0, 120, W, 180, "#FFFFFF", "none", 14) + rect(104, 128, 32, 4, "#D6D0C6", "none", 2) + lbl(14, 148, "Notifications", INK)
        s += "".join(rect(14, 156 + i * 32, 212, 28, SOFT, "none", 6) + mono(20, 160 + i * 32, n, c, 20) + t(48, 174 + i * 32, m, 9, INK, "khand") + t(218, 174 + i * 32, tm, 6, MUTE, "hind", 600, "end") for i, (n, c, m, tm) in enumerate(items))
        return screen(s)
    elif kind == "byagent":
        s += bell(182, 14, 14, "#FFFFFF") + rect(64, 46, 168, 168, "#FFFFFF", LINE, 8, extra='filter="drop-shadow(0 3px 5px #0003)"')
        s += "".join(mono(72, 56 + i * 38, n, c, 18) + t(96, 67 + i * 38, n, 9, INK, "khand") + t(96, 77 + i * 38, m, 6.5, MUTE) + f'<circle cx="218" cy="{65+i*38}" r="6" fill="{TERRA}"/>' + t(218, 67.5 + i * 38, str([2, 1, 1, 3][i]), 6.5, "#FFFFFF", "hind", 700, "middle") for i, (n, c, m, tm) in enumerate(items))
    else:
        s += bell(182, 14, 14, "#FFFFFF") + rect(64, 46, 168, 168, "#FFFFFF", LINE, 8, extra='filter="drop-shadow(0 3px 5px #0003)"')
        s += "".join(rect(70, 52 + i * 40, 156, 34, (c + "14") if i < 2 else "#FFFFFF", "none", 6) + rect(70, 52 + i * 40, 3, 34, c) + t(80, 66 + i * 40, m, 8.5, INK, "khand") + t(80, 77 + i * 40, n + " · " + tm, 6, MUTE) + (tag(188, 58 + i * 40, "New", c) if i < 2 else "") for i, (n, c, m, tm) in enumerate(items))
    s += f'<circle cx="194" cy="15" r="4.5" fill="{SAFFRON}" stroke="{TERRA}" stroke-width="1"/>'
    return screen(s + foot())
add(G, "Notifications", O("nt_dropdown", "Bell Drops A Short List", "Newest first, agent letter on each.", ["quick", "focused"], "quick", notif("drop")),
    O("nt_sheet", "Bell Opens A Bottom Sheet", "Slides up from the bottom on phone.", ["action", "visual"], "action", notif("sheet")), "Dropdown Or Bottom Sheet?", "new")
add(G, "Notifications", O("nt_by_agent", "Grouped By Agent With Counts", "One line per agent, count bubble.", ["focused", "visual"], "focused", notif("byagent")),
    O("nt_new_tinted", "Time List, New Ones Tinted", "Unread rows tinted with a New tag.", ["visual", "quick"], "visual", notif("tint")), "By Agent Or By Time?", "new")
G = "Project Status Cards"
def projcard(kind):
    s = band() + section(64, "Projects")
    items = [("Visit Log", .9, JUNGLE, "Done"), ("Pricing Page", .6, LAGOON, "Running"), ("Tech App", .35, SAFFRON, "Waiting"), ("Onboarding", .15, TERRA, "Blocked")]
    for i, (n, f, c, st) in enumerate(items):
        if kind == "row": y = 72 + i * 46; s += rect(14, y, 212, 40, "#FFFFFF", LINE, 8) + t(24, y + 16, n, 10, INK, "khand") + tag(170, y + 7, st, c) + pbar(24, y + 26, 140, f, c) + t(216, y + 30, f"{int(f*100)}%", 9, c, "khand", anchor="end")
        elif kind == "grid": x, y = 14 + (i % 2) * 108, 72 + (i // 2) * 84; s += rect(x, y, 104, 78, "#FFFFFF", LINE, 8) + rect(x, y, 104, 4, c, "none", 2) + t(x + 10, y + 22, n, 10, INK, "khand") + tag(x + 10, y + 30, st, c) + t(x + 10, y + 66, f"{int(f*100)}%", 18, c, "khand")
        elif kind == "next": y = 72 + i * 46; s += rect(14, y, 212, 40, "#FFFFFF", LINE, 8) + rect(14, y, 5, 40, c, "none", 2) + t(26, y + 16, n, 10, INK, "khand") + t(26, y + 29, "Next: " + ["Ship to techs", "Add fall rates", "Your pick on polo", "Write welcome"][i], 6.8, MUTE) + t(216, y + 24, f"{int(f*100)}%", 14, c, "khand", anchor="end")
        else: y = 72 + i * 46; s += rect(14, y, 212, 40, "#FFFFFF", LINE, 8) + "".join(rect(24 + k * 26, y + 24, 22, 7, c if k < round(f * 5) else "#EEEAE4", "none", 2) for k in range(5)) + t(24, y + 17, n, 10, INK, "khand") + t(216, y + 30, st.upper(), 6.5, c, "hind", 700, "end", 'letter-spacing="1"')
    return screen(s + foot())
add(G, "Project Cards", O("pc_row_bar", "Row With Chip, Bar And Percent", "Everything on one line per project.", ["visual", "focused"], "visual", projcard("row")),
    O("pc_grid", "Two-Across Cards With Color Top", "Big percent, status chip, color top edge.", ["visual", "quick"], "quick", projcard("grid")), "Rows Or Grid Cards?", "new")
add(G, "Project Cards", O("pc_next_step", "Percent Plus Next Step", "Shows what happens next on each.", ["action", "focused"], "action", projcard("next")),
    O("pc_steps", "Five Stage Blocks", "Blocks fill by stage; status word on the right.", ["visual", "quick"], "focused", projcard("steps")), "Next Step Or Stage Blocks?", "new")
G = "Deck-Results Card"
def deckres(kind):
    s = band("Style Swipe", SAFFRON, sub="Command Center") + section(64, "Latest Deck")
    s += rect(14, 72, 212, 150, "#FFFFFF", LINE, 10) + t(24, 92, "Dashboard Round 1", 12, INK, "khand") + t(24, 104, "Oct 13 · 50 pairs", 7, MUTE)
    if kind == "tags": s += t(24, 140, "37", 30, TERRA, "khand") + t(58, 140, "Picked", 8, MUTE, "hind", 600) + "".join(tag(24 + (i % 3) * 64, 152 + (i // 3) * 18, g, ACC[i % 4]) for i, g in enumerate(["Visual", "Focused", "Simple", "Quick", "Action"])) + link(24, 210, "Open Results")
    elif kind == "split": s += rect(24, 118, 192, 12, SOFT, "none", 6) + rect(24, 118, 192 * 37 / 50, 12, JUNGLE, "none", 6) + t(24, 146, "37 Picked", 8, JUNGLE, "hind", 600) + t(216, 146, "13 Skipped", 8, MUTE, "hind", 600, "end") + t(24, 172, "Top: Visual, Focused, Quick", 8, INK) + btn(186, "Start Round 2", "fill", INK, 24, 192, 22, 7.5)
    elif kind == "picks": s += lbl(24, 122, "Top Picks", MUTE) + "".join(dot(28, 134 + i * 16, 3, ACC[i]) + t(36, 137 + i * 16, p, 8, INK) for i, p in enumerate(["Solid Color Band", "Inline Answer Buttons", "Square Icon Tiles", "Ask-The-Agent Box"])) + link(24, 210, "See All 37")
    else: s += "".join(rect(24 + i * 66, 118, 60, 50, SOFT, "none", 6) + t(54 + i * 66, 146, v, 18, c, "khand", anchor="middle") + t(54 + i * 66, 160, n, 6, MUTE, "hind", 600, "middle") for i, (v, n, c) in enumerate([("37", "Picked", JUNGLE), ("13", "Skipped", SAFFRON), ("5m", "Time", LAGOON)])) + btn(180, "Start Round 2", "fill", TERRA, 24, 192, 22, 7.5)
    return screen(s + foot())
add(G, "Deck Results", O("dr_tags", "Big Count Plus Top Tags", "37 picked and tag chips.", ["visual", "quick"], "visual", deckres("tags")),
    O("dr_split", "Picked Vs Skipped Bar", "One bar and a Start Round 2 button.", ["action", "focused"], "action", deckres("split")), "Tags Or Picked-Skipped Bar?", "new")
add(G, "Deck Results", O("dr_picks", "Top Picks List", "Four winning looks by name.", ["focused", "quick"], "focused", deckres("picks")),
    O("dr_stat_boxes", "Three Stat Boxes", "Picked, Skipped, Time, then a button.", ["visual", "action"], "quick", deckres("boxes")), "Picks List Or Stat Boxes?", "new")
G = "Link Tile Labels"
def tilelbl(kind):
    names = [("Smart Upkeep", "home", "upkeep"), ("Visit Log", "cal", "visits"), ("Billing", "card", "billing"), ("Price Sheet", "tag", "prices")]
    s = band() + section(64, "Apps")
    for i, (n, k, u) in enumerate(names):
        x, y = 14 + (i % 2) * 108, 72 + (i // 2) * 90; c = ACC[i]
        s += rect(x, y, 104, 84, "#FFFFFF", LINE, 10) + rect(x + 10, y + 10, 28, 28, c + "1F", "none", 7) + ic(k, x + 15, y + 15, 18, c, 2.2)
        if kind == "name": s += t(x + 10, y + 64, n, 11, INK, "khand")
        elif kind == "addr": s += t(x + 10, y + 60, n, 11, INK, "khand") + t(x + 10, y + 72, f"/{u}", 6.5, MUTE)
        elif kind == "side": s += t(x + 44, y + 28, n.split()[0], 10, INK, "khand") + t(x + 10, y + 62, "Last used 2h", 6.5, MUTE)
        else: s += t(x + 10, y + 60, n, 11, INK, "khand") + t(x + 10, y + 74, "OPEN >", 6.5, c, "hind", 700, extra='letter-spacing="1"')
    return screen(s + foot())
add(G, "Tile Labels", O("tl_name_only", "Name Only", "Just the app name under the icon.", ["focused", "quick"], "focused", tilelbl("name")),
    O("tl_name_addr", "Name Plus Short Address", "Name and the link path under it.", ["focused", "visual"], "visual", tilelbl("addr")), "Name Only Or With Address?", "new")
add(G, "Tile Labels", O("tl_beside", "Name Beside Icon, Last Used Below", "Short name by the icon, recency under.", ["visual", "quick"], "quick", tilelbl("side")),
    O("tl_open_cue", "Name Plus Colored Open Cue", "A small OPEN arrow in the tile color.", ["action", "visual"], "action", tilelbl("open")), "Last Used Or Open Cue?", "new")

finish(DID, "Agent Dashboard Round 2: Re-Asks, Winners Vs Alternatives, Full Looks, Group Colors, Corners, Tabs, Ask Box, Big Monitor, MacBook, Notifications, Project Cards, Deck Results, Tile Labels", "Agent Dashboard", pairs, 0,
       {"brands": ["Agent command-center dashboards, round 2 from dashboard-1 picks (results/dashboard-1.txt)", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017"],
        "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first"},
        "based_on": "dashboard-1", "sources": {"results": "results/dashboard-1.txt", "prior_deck": "decks/dashboard-1.json", "spec": "/workspace/ops/apps-home/AGENT-DASHBOARD-SPEC.md"}}, seed=26)
d = json.load(open(f"decks/{DID}.json")); d.pop("draft", None); d["status"] = "published"; d["share"] = True
for pp in d["pairs"]:
    pp["notes"] = True; pp["share"] = True
    for k in "AB": o = pp["option" + k]; o["tags"] = list(dict.fromkeys(o["tags"]))
json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
