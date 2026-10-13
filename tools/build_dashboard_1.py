#!/usr/bin/env python3
"""Build Style Swipe deck dashboard-1 (PUBLISHED): 50 this-or-that pairs on the command-center dashboard app every one of
Max's agents builds (spec: /workspace/ops/apps-home/AGENT-DASHBOARD-SPEC.md; example: /workspace/branding-dashboard/).
All options are drawn SVG phone/desktop mockups: white light mode, Khand/Hind, Title Case, no emoji (small drawn icons),
small pops of terracotta, lagoon, jungle, saffron. Uses tools/draft_svg.py helpers. Run from the style-swipe repo root."""
import json, sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from draft_svg import *
DID = "dashboard-1"
pairs, O, add = mk("db1_", "Agent Dashboard")
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

# ---------------- Layout ----------------
G = "Layout"
def lay(kind):
    if kind == "cards":
        s = "".join(rect(14 + (i % 2) * 108, 54 + (i // 2) * 76, 104, 70, "#FFFFFF", LINE, 8) + ic(["check", "clock", "star", "tag", "cal", "home"][i], 22 + (i % 2) * 108, 62 + (i // 2) * 76, 14, ACC[i % 4]) + t(22 + (i % 2) * 108, 96 + (i // 2) * 76, ["Status", "Owed", "Pinned", "Apps", "Calendar", "Recent"][i], 11, INK, "khand") + t(22 + (i % 2) * 108, 108 + (i // 2) * 76, ["All Green", "3 Calls", "2 Items", "5 Links", "Thu 10 AM", "Shipped"][i], 7, MUTE) for i in range(6))
    elif kind == "list":
        s = "".join(row(56 + i * 38, n, d, ACC[i % 4], ">", k=["check", "clock", "star", "tag", "cal", "home"][i]) for i, (n, d) in enumerate([("Status", "All green"), ("Decisions Owed", "3 calls"), ("Pinned", "2 items"), ("Apps", "5 links"), ("Calendar", "Thu 10 AM"), ("Recent Work", "Shipped 1h ago")]))
    elif kind == "tabs":
        s = "".join(t(30 + i * 60, 62, n, 9, INK if i == 0 else MUTE, "khand", anchor="middle") for i, n in enumerate(["Now", "Owed", "Apps", "Log"])) + rect(12, 66, 36, 2.5, TERRA) + ln(68, 0, W)
        s += section(86, "Needs You") + "".join(row(92 + i * 38, n, d, TERRA) for i, (n, d) in enumerate(OWED)) + section(222, "Status") + chip(14, 230, "On Track", JUNGLE)
    else:
        s = section(62, "Swipe Through") + rect(14, 70, 176, 160, "#FFFFFF", LINE, 10) + rect(196, 70, 60, 160, "#FFFFFF", LINE, 10) + ic("clock", 26, 84, 18, TERRA)
        s += h1(26, 126, "3 Decisions Owed", 16) + t(26, 142, "Front door, tax draft, polo", 7.5, MUTE) + btn(196, "Review", "fill", INK, 26, 150, 22, 8) + dots(246, 4, 0)
    return scr(s)
def dots(y, n, cur, c=INK):
    x0 = 120 - (n - 1) * 7; return "".join(f'<circle cx="{x0+i*14}" cy="{y}" r="3" fill="{c if i==cur else "#D6D0C6"}"/>' for i in range(n))
add(G, "Home Layout", O("lay_cards", "Grid Of Cards", "Six square cards, one per section.", ["visual", "scan"], "lively", lay("cards")),
    O("lay_list", "One Long List", "Each section is a row; tap to open.", ["simple", "fast"], "calm", lay("list")), "Cards Or A List?")
add(G, "Home Layout", O("lay_tabs", "Tabs Across The Top", "Now, Owed, Apps, Log as tabs.", ["focused", "clear"], "calm", lay("tabs")),
    O("lay_carousel", "Swipe Carousel", "One big card at a time; swipe for the next.", ["playful", "big"], "lively", lay("carousel")), "Tabs Or A Carousel?")

# ---------------- Header ----------------
G = "Header"
def hdr(kind):
    if kind == "band": top = topbar(style="band")
    elif kind == "text": top = topbar(style="text")
    elif kind == "big":
        top = avatar(14, 54, TERRA, "home", 40) + h1(62, 76, "Prop", 24) + t(62, 90, "Command Center · On Track", 7.5, MUTE) + shareic(206, 14) + ln(104, 0, W)
        return screen(top + section(124, "Needs You") + "".join(row(130 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + foot())
    else: top = topbar()
    return screen(top + section(68, "Needs You") + "".join(row(74 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + section(200, "Recent") + "".join(t(14, 216 + i * 14, f"{a} · {b}", 7.5, MUTE) for i, (a, b) in enumerate(WORK)) + foot())
add(G, "Header Style", O("hdr_plain", "White Header, Small Icon", "Thin rule under a white bar.", ["calm", "clean"], "calm", hdr("plain")),
    O("hdr_band", "Solid Color Band", "The agent's color fills the top bar.", ["bold", "visual"], "lively", hdr("band")), "Quiet Or Color Header?")
add(G, "Header Style", O("hdr_text", "Name Only, No Icon", "Just the name in Khand.", ["simple", "minimal"], "calm", hdr("text")),
    O("hdr_big", "Big Hero Name", "Large icon and name, status under it.", ["big", "clear"], "lively", hdr("big")), "Small Or Big Name?")
def sharepos(kind):
    top = topbar(share=(kind == "corner"))
    body = section(68, "Needs You") + "".join(row(74 + i * 38, n, d) for i, (n, d) in enumerate(OWED))
    if kind == "bottom": body += rect(14, 196, 212, 28, "#FFFFFF", INK, 0, 1.4) + shareic(76, 203, INK) + t(128, 214, "SHARE THIS DASHBOARD", 7.5, INK, "hind", 600, "middle", 'letter-spacing="1"')
    return screen(top + body + foot())
add(G, "Share Button", O("hdr_share_corner", "Share Icon In The Header Corner", "Small share mark top right.", ["minimal", "app"], "calm", sharepos("corner")),
    O("hdr_share_bottom", "Wide Share Button Lower Down", "A full-width outlined Share button.", ["clear", "big"], "quick", sharepos("bottom")), "Corner Icon Or Wide Button?")

# ---------------- Status ----------------
G = "Status Display"
def stat(kind):
    items = [("Site Build", JUNGLE, "Done"), ("Tax Draft", SAFFRON, "Waiting"), ("Polo Order", TERRA, "Blocked"), ("Deck Round 6", LAGOON, "Running")]
    s = section(64, "Status")
    for i, (n, c, st) in enumerate(items):
        y = 72 + i * 40; s += rect(14, y, 212, 34, "#FFFFFF", LINE, 6) + t(24, y + 21, n, 10, INK, "khand")
        s += chip(150, y + 12, st, c, kind) if kind in ("chip", "solid") else chip(150, y + 11, st, c, kind)
    return scr(s + section(250, "Updated 9:40 AM"))
add(G, "Status Marks", O("st_chip", "Soft Tinted Chips", "Pale pill with colored word.", ["clear", "visual"], "calm", stat("chip")),
    O("st_dot", "Colored Dots", "A small dot and a plain word.", ["minimal", "calm"], "calm", stat("dot")), "Chips Or Dots?")
add(G, "Status Marks", O("st_ring", "Small Progress Rings", "A mini ring that fills with progress.", ["visual", "lively"], "lively", stat("ring")),
    O("st_solid", "Solid Color Pills", "Filled pills, white text.", ["bold", "scan"], "lively", stat("solid")), "Rings Or Solid Pills?")

add(G, "Status Marks", O("st_bar", "Short Color Bar And Word", "A small vertical bar beside the status.", ["minimal", "scan"], "calm", stat("bar")),
    O("st_word", "Colored Word Only", "Just the status word in its color.", ["minimal", "readable"], "quick", stat("word")), "Bar Or Colored Word?")

# ---------------- Density ----------------
G = "Density"
def dens(kind):
    if kind == "airy": s = section(66, "Needs You") + "".join(rect(14, 74 + i * 62, 212, 54, "#FFFFFF", LINE, 8) + dot(28, 101 + i * 62, 4, TERRA) + t(40, 98 + i * 62, n, 13, INK, "khand") + t(40, 111 + i * 62, d, 7.5, MUTE) for i, (n, d) in enumerate(OWED))
    elif kind == "medium": s = section(62, "Needs You") + "".join(row(70 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + section(194, "Recent") + "".join(t(14, 210 + i * 14, a, 8, INK) + t(226, 210 + i * 14, b, 7, MUTE, anchor="end") for i, (a, b) in enumerate(WORK))
    elif kind == "split": s = section(62, "Needs You") + "".join(row(70 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + rect(14, 194, 212, 60, SOFT, "none", 8) + t(24, 214, "3 Recent Updates", 10, INK, "khand") + link(24, 240, "Show All")
    else: s = section(60, "Needs You") + "".join(t(14, 76 + i * 13, f"{n}", 8, INK, "hind", 600) + t(226, 76 + i * 13, d.split("·")[1], 7, MUTE, anchor="end") for i, (n, d) in enumerate(OWED * 2)) + section(166, "Recent") + "".join(t(14, 182 + i * 13, a, 8, INK) + t(226, 182 + i * 13, b, 7, MUTE, anchor="end") for i, (a, b) in enumerate(WORK * 2))
    return scr(s)
add(G, "Density", O("den_airy", "Roomy, Three Big Rows", "Lots of white space; fewer items per screen.", ["calm", "big"], "calm", dens("airy")),
    O("den_tight", "Packed, Everything Visible", "Small text, many rows, no scrolling.", ["fast", "scan"], "quick", dens("tight")), "Roomy Or Packed?")
add(G, "Density", O("den_medium", "Medium Rows Plus Short List", "Cards for what is owed, small lines for recent.", ["balanced", "clear"], "calm", dens("medium")),
    O("den_split", "Owed Only, Recent Folded", "Recent work tucked behind Show All.", ["focused", "minimal"], "quick", dens("split")), "Show Recent Or Fold It?")

# ---------------- First Thing ----------------
G = "First Thing On Screen"
def first(kind):
    if kind == "owed": s = rect(14, 54, 212, 86, TERRA + "14", "none", 10) + lbl(24, 72, "Needs You", TERRA) + h1(24, 96, "3 Decisions Owed", 18) + t(24, 112, "Front door · Tax draft · Polo", 7.5, MUTE) + btn(118, "Decide Now", "fill", TERRA, 24, 120, 16, 7) + section(162, "Recent") + "".join(row(168 + i * 38, a, b, LAGOON) for i, (a, b) in enumerate(WORK[:2]))
    elif kind == "work": s = rect(14, 54, 212, 96, "#FFFFFF", LINE, 10) + rect(24, 64, 192, 46, LAGOON + "1A", "none", 6) + ic("check", 30, 76, 20, LAGOON) + t(58, 90, "Shipped Visit Log", 12, INK, "khand") + t(24, 126, "Latest Work · 1h ago", 7, MUTE) + link(24, 140, "Open")
    elif kind == "links": s = section(62, "Your Apps") + "".join(rect(14 + (i % 3) * 72, 70 + (i // 3) * 64, 66, 58, "#FFFFFF", LINE, 8) + ic(["home", "cal", "card", "tag", "star", "search"][i], 37 + (i % 3) * 72, 80 + (i // 3) * 64, 20, ACC[i % 4]) + t(47 + (i % 3) * 72, 118 + (i // 3) * 64, ["Site", "Visits", "Billing", "Prices", "Reviews", "Docs"][i], 8, INK, "khand", anchor="middle") for i in range(6))
    else: s = rect(14, 54, 212, 70, "#FFFFFF", LINE, 10) + ringp(46, 89, 20, .7, JUNGLE, "70%") + t(78, 84, "On Track", 14, INK, "khand") + t(78, 98, "7 of 10 tasks this week", 7.5, MUTE)
    if kind in ("work", "status"): s += section(176, "Needs You") + "".join(row(182 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:2]))
    return scr(s)
add(G, "Top Of Screen", O("ft_owed", "What Needs Me First", "Decisions owed lead the page.", ["focused", "action"], "quick", first("owed")),
    O("ft_work", "Latest Work First", "Newest shipped item leads.", ["proud", "visual"], "lively", first("work")), "Owed Or Latest Work First?")
add(G, "Top Of Screen", O("ft_links", "App Links First", "A grid of the agent's apps leads.", ["fast", "visual"], "quick", first("links")),
    O("ft_status", "Overall Status First", "A progress ring and one line.", ["calm", "clear"], "calm", first("status")), "Links Or Status First?")

# ---------------- App Tiles ----------------
G = "App Link Tiles"
def tiles(kind):
    names = [("Smart Upkeep", "home"), ("Visit Log", "cal"), ("Billing", "card"), ("Price Sheet", "tag")]
    s = section(62, "Apps")
    for i, (n, k) in enumerate(names):
        c = ACC[i]
        if kind == "square": x, y = 14 + (i % 2) * 108, 70 + (i // 2) * 92; s += rect(x, y, 104, 86, "#FFFFFF", LINE, 10) + rect(x + 10, y + 10, 30, 30, c + "1F", "none", 8) + ic(k, x + 16, y + 16, 18, c) + t(x + 10, y + 62, n, 11, INK, "khand") + t(x + 10, y + 74, "Open App", 6.5, MUTE)
        elif kind == "rows": s += row(70 + i * 40, n, "webermanapps.github.io", c, ">", k=k)
        elif kind == "shot": x, y = 14 + (i % 2) * 108, 70 + (i // 2) * 96; s += rect(x, y, 104, 90, "#FFFFFF", LINE, 8) + rect(x, y, 104, 56, SOFT, "none", 8) + rect(x + 10, y + 10, 50, 5, c) + rect(x + 10, y + 20, 80, 3, "#D6D0C6") + rect(x + 10, y + 27, 70, 3, "#D6D0C6") + rect(x + 10, y + 38, 30, 9, INK) + t(x + 10, y + 74, n, 10, INK, "khand")
        else: s += rect(14, 70 + i * 34, 212, 28, c, "none", 0) + ic(k, 22, 76 + i * 34, 16, "#FFFFFF") + t(46, 88 + i * 34, n.upper(), 8, "#FFFFFF", "hind", 600, extra='letter-spacing="1"') + ic("chev", 204, 78 + i * 34, 12, "#FFFFFF")
    return scr(s)
add(G, "App Tiles", O("tile_square", "Square Icon Tiles", "Tinted icon square, name below.", ["visual", "app"], "lively", tiles("square")),
    O("tile_rows", "Link Rows With Arrow", "Icon, name and address per row.", ["simple", "clear"], "calm", tiles("rows")), "Tiles Or Rows?")
add(G, "App Tiles", O("tile_shot", "Mini Screenshot Tiles", "A tiny preview of each app.", ["visual", "rich"], "lively", tiles("shot")),
    O("tile_block", "Solid Color Bars", "Full-width colored link bars.", ["bold", "big"], "quick", tiles("block")), "Previews Or Color Bars?")

# ---------------- Feed ----------------
G = "Updates And Activity"
def feed(kind):
    ev = [("Shipped Visit Log", "9:40 AM", JUNGLE, "check"), ("Updated Prices", "8:15 AM", LAGOON, "tag"), ("Asked: Polo Color", "Yesterday", TERRA, "clock"), ("New Deck Ready", "Mon", SAFFRON, "star")]
    s = section(62, "Activity")
    for i, (n, tm, c, k) in enumerate(ev):
        y = 72 + i * 46
        if kind == "timeline": s += (f'<line x1="24" y1="{y+6}" x2="24" y2="{y+46}" stroke="{LINE}" stroke-width="2"/>' if i < 3 else "") + dot(24, y + 6, 5, c) + t(38, y + 10, n, 10, INK, "khand") + t(38, y + 22, tm, 7, MUTE)
        elif kind == "cards": s += rect(14, y, 212, 40, "#FFFFFF", LINE, 8) + rect(22, y + 8, 24, 24, c + "1F", "none", 6) + ic(k, 26, y + 12, 16, c) + t(54, y + 18, n, 10, INK, "khand") + t(54, y + 30, tm, 7, MUTE)
        elif kind == "log": s += t(14, 80 + i * 16, tm, 7, MUTE, "hind", 600) + t(70, 80 + i * 16, n, 8, INK)
        else: s += t(14, y + 12, n, 12, INK, "khand") + t(14, y + 24, "Short note on what changed and why.", 7.5, MUTE) + t(226, y + 12, tm, 6.5, MUTE, anchor="end") + ln(y + 34)
    return scr(s)
add(G, "Feed Style", O("feed_timeline", "Dot Timeline", "Colored dots on a vertical line.", ["visual", "clear"], "calm", feed("timeline")),
    O("feed_cards", "Icon Cards", "Each update in its own card.", ["visual", "lively"], "lively", feed("cards")), "Timeline Or Cards?")
add(G, "Feed Style", O("feed_log", "Plain Log Lines", "Time and one line, tight.", ["fast", "minimal"], "quick", feed("log")),
    O("feed_notes", "Headline Plus Note", "Short title with a one-line why.", ["readable", "warm"], "calm", feed("notes")), "Log Or Headlines?")

# ---------------- Decisions Owed ----------------
G = "Decisions Owed"
def owed(kind):
    if kind == "buttons":
        s = section(62, "Decide") + "".join(rect(14, 70 + i * 66, 212, 60, "#FFFFFF", LINE, 8) + t(24, 88 + i * 66, n, 11, INK, "khand") + t(24, 100 + i * 66, d, 7, MUTE) + btn(106 + i * 66, "Option A", "fill", INK, 24, 92, 16, 6.5) + btn(106 + i * 66, "Option B", "line", INK, 122, 92, 16, 6.5) for i, (n, d) in enumerate(OWED))
    elif kind == "count":
        s = rect(14, 54, 212, 110, "#FFFFFF", TERRA, 10, 1.5) + t(120, 112, "3", 48, TERRA, "khand", anchor="middle") + t(120, 132, "Decisions Waiting On You", 10, INK, "khand", anchor="middle") + btn(140, "See All", "line", TERRA, 70, 100, 16, 7)
    elif kind == "flag":
        s = section(62, "Needs You") + "".join(rect(14, 70 + i * 40, 212, 34, "#FFFFFF", LINE, 6) + rect(14, 70 + i * 40, 4, 34, [TERRA, SAFFRON, SAFFRON][i]) + t(26, 85 + i * 40, n, 9.5, INK, "khand") + t(26, 96 + i * 40, d, 6.5, MUTE) + tag(176, 81 + i * 40, ["Urgent", "Soon", "Soon"][i], [TERRA, SAFFRON, SAFFRON][i]) for i, (n, d) in enumerate(OWED))
    else:
        s = section(62, "Needs You") + "".join(f'<rect x="16" y="{74+i*28}" width="10" height="10" fill="none" stroke="{INK}" stroke-width="1.4"/>' + t(34, 83 + i * 28, n, 9.5, INK, "khand") + t(226, 83 + i * 28, d.split("·")[1], 6.5, MUTE, anchor="end") for i, (n, d) in enumerate(OWED))
    return scr(s)
add(G, "Decisions Owed", O("ow_buttons", "Answer Buttons Inline", "Pick right on the card, no clicks away.", ["action", "fast"], "quick", owed("buttons")),
    O("ow_count", "One Big Count", "A big number and a See All button.", ["big", "calm"], "lively", owed("count")), "Answer Inline Or Big Count?")
add(G, "Decisions Owed", O("ow_flag", "Urgency Edge Flags", "Colored edge and an Urgent or Soon tag.", ["clear", "scan"], "calm", owed("flag")),
    O("ow_check", "Plain Checklist", "Square boxes to tick off.", ["simple", "minimal"], "calm", owed("check")), "Flags Or Checklist?")

# ---------------- Progress ----------------
G = "Progress Display"
def prog(kind):
    items = [("Visit Log", .9, JUNGLE), ("Pricing Page", .6, LAGOON), ("Tech App", .35, SAFFRON), ("Onboarding", .15, TERRA)]
    s = section(62, "Progress")
    for i, (n, f, c) in enumerate(items):
        if kind == "bars": y = 76 + i * 40; s += t(14, y, n, 10, INK, "khand") + t(226, y, f"{int(f*100)}%", 7, MUTE, "hind", 600, "end") + pbar(14, y + 8, 212, f, c)
        elif kind == "rings": x, y = 14 + (i % 2) * 108, 70 + (i // 2) * 96; s += rect(x, y, 104, 90, "#FFFFFF", LINE, 8) + ringp(x + 52, y + 38, 22, f, c, f"{int(f*100)}%") + t(x + 52, y + 80, n, 9, INK, "khand", anchor="middle")
        elif kind == "steps": y = 76 + i * 44; s += t(14, y, n, 10, INK, "khand") + "".join(rect(14 + k * 43, y + 8, 39, 8, c if k < round(f * 5) else "#EEEAE4", "none", 2) for k in range(5))
        else: y = 72 + i * 40; s += t(14, y + 14, n, 10, INK, "khand") + t(226, y + 18, f"{int(f*100)}%", 20, c, "khand", anchor="end") + ln(y + 26)
    return scr(s)
add(G, "Progress", O("pr_bars", "Thin Progress Bars", "One slim bar per project.", ["clear", "calm"], "calm", prog("bars")),
    O("pr_rings", "Progress Rings", "A ring per project in a grid.", ["visual", "lively"], "lively", prog("rings")), "Bars Or Rings?")
add(G, "Progress", O("pr_steps", "Five-Step Blocks", "Blocks fill in as stages finish.", ["visual", "scan"], "lively", prog("steps")),
    O("pr_number", "Big Percent Numbers", "Just a large number per project.", ["big", "simple"], "quick", prog("number")), "Steps Or Numbers?")

# ---------------- Icons ----------------
G = "Icons"
def icons(kind):
    ks = ["home", "cal", "card", "tag", "star", "clock", "search", "check", "heart"]
    s = section(62, "Icon Set")
    for i, k in enumerate(ks):
        x, y = 30 + (i % 3) * 66, 76 + (i // 3) * 62; c = ACC[i % 4]
        if kind == "line": s += ic(k, x + 6, y + 6, 30, INK, 1.6)
        elif kind == "tinted": s += rect(x, y, 42, 42, c + "1F", "none", 10) + ic(k, x + 9, y + 9, 24, c, 1.8)
        elif kind == "circle": s += f'<circle cx="{x+21}" cy="{y+21}" r="21" fill="{c}"/>' + ic(k, x + 10, y + 10, 22, "#FFFFFF", 2)
        else: s += ic(k, x + 6, y + 6, 30, c, 2.4)
    return scr(s)
add(G, "Icon Style", O("ic_line", "Thin Black Line Icons", "One color, fine strokes.", ["minimal", "calm"], "calm", icons("line")),
    O("ic_tinted", "Icons In Tinted Squares", "Colored icon on a pale square.", ["visual", "lively"], "lively", icons("tinted")), "Plain Or Tinted?")
add(G, "Icon Style", O("ic_circle", "White Icon In Solid Circle", "Bold filled circles.", ["bold", "app"], "lively", icons("circle")),
    O("ic_color", "Colored Bold Strokes", "Thicker line icons in four colors.", ["visual", "clear"], "quick", icons("color")), "Circles Or Colored Lines?")

# ---------------- Accent ----------------
G = "Accent Color Use"
def accent(kind):
    if kind == "one": cs = [TERRA] * 4
    elif kind == "four": cs = ACC
    elif kind == "action": cs = [MUTE] * 4
    else: cs = [INK] * 4
    s = section(62, "Today")
    for i, (n, d) in enumerate(OWED + [("Ship Pricing", "Prop · Friday")]): s += row(70 + i * 40, n, d, cs[i], k=["clock", "star", "tag", "check"][i])
    s += btn(240, "Review Decisions", "fill", TERRA if kind != "mono" else INK)
    if kind == "mono": s += rect(14, 230, 40, 3, TERRA)
    return scr(s)
add(G, "Accent Color", O("acc_one", "One Accent Only", "Terracotta everywhere color appears.", ["unified", "calm"], "calm", accent("one")),
    O("acc_four", "All Four Pops", "Terracotta, lagoon, jungle, saffron by type.", ["lively", "visual"], "lively", accent("four")), "One Or Four Colors?")
add(G, "Accent Color", O("acc_action", "Color Only On Actions", "Grey icons; color saved for the button.", ["focused", "action"], "quick", accent("action")),
    O("acc_mono", "Black With A Single Line Of Color", "Ink icons and button, one small terracotta mark.", ["minimal", "bold"], "calm", accent("mono")), "Color On Action Or Almost None?")

# ---------------- Phone Vs Desktop ----------------
G = "Phone Vs Desktop"
def desk(kind):
    s = rect(10, 40, 220, 150, "#FFFFFF", "#CFC8BC", 6) + rect(10, 40, 220, 12, SOFT, "none", 6) + "".join(dot(18 + i * 7, 46, 2, "#CFC8BC") for i in range(3))
    if kind == "wide": s += "".join(rect(18 + i * 70, 60, 64, 122, "#FFFFFF", LINE, 4) + lbl(24 + i * 70, 72, ["Owed", "Status", "Apps"][i], ACC[i], 5.5) + "".join(rect(24 + i * 70, 80 + k * 18, 52, 12, SOFT, "none", 2) for k in range(5)) for i in range(3))
    elif kind == "side": s += rect(10, 52, 50, 138, SOFT) + "".join(t(16, 68 + k * 14, n, 6.5, INK if k == 0 else MUTE, "hind", 600) for k, n in enumerate(["Now", "Owed", "Apps", "Log", "Calendar"])) + "".join(rect(68, 60 + k * 30, 154, 24, "#FFFFFF", LINE, 4) for k in range(4))
    else: s += rect(80, 52, 80, 138, "#FFFFFF", LINE) + "".join(rect(86, 60 + k * 26, 68, 20, SOFT, "none", 3) for k in range(5))
    cap = {"wide": "Desktop Spreads To 3 Columns", "side": "Desktop Gets A Side Menu", "same": "Same Narrow Column Everywhere"}[kind]
    s += rect(166, 150, 50, 96, "#FFFFFF", INK, 7, 1.5) + "".join(rect(172, 162 + k * 16, 38, 11, SOFT, "none", 2) for k in range(5))
    return scr(s + h1(14, 262, cap, 13) + t(14, 276, "Phone stays one column.", 7.5, MUTE))
add(G, "Desktop Layout", O("pd_wide", "Spread Into Columns On Desktop", "Owed, Status, Apps side by side.", ["scan", "rich"], "quick", desk("wide")),
    O("pd_same", "Same Phone Column On Desktop", "Centered narrow column on big screens.", ["simple", "unified"], "calm", desk("same")), "Columns Or One Column?")
add(G, "Desktop Layout", O("pd_side", "Side Menu On Desktop", "Left menu with sections; content right.", ["app", "clear"], "calm", desk("side")),
    O("pd_wide2", "Three Columns, No Menu", "All sections visible at once.", ["fast", "scan"], "quick", desk("wide")), "Side Menu Or Columns Only?")

# ---------------- Agent Navigation ----------------
G = "Navigation Between Agents"
def nav(kind):
    if kind == "dropdown":
        s = rect(14, 54, 212, 30, "#FFFFFF", INK, 6, 1.2) + avatar(20, 59, TERRA, "home", 20) + t(48, 73, "Prop", 11, INK, "khand") + ic("down", 202, 61, 14) + rect(14, 88, 212, 120, "#FFFFFF", LINE, 6, extra='filter="drop-shadow(0 2px 3px #0002)"')
        s += "".join(avatar(22, 96 + i * 28, c, k, 20) + t(50, 110 + i * 28, n, 10, INK, "khand") for i, (n, c, k) in enumerate(AGENTS))
    elif kind == "strip":
        s = "".join(avatar(14 + i * 52, 54, c, k, 36, "tile" if i == 0 else "ring") + t(32 + i * 52, 102, n, 7, INK if i == 0 else MUTE, "hind", 600, "middle") for i, (n, c, k) in enumerate(AGENTS)) + ln(112, 0, W) + section(130, "Needs You") + "".join(row(136 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:2]))
    elif kind == "bottom":
        s = section(64, "Needs You") + "".join(row(70 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + rect(0, 244, W, 40, "#FFFFFF") + ln(244, 0, W) + "".join(avatar(32 + i * 52, 250, c, k, 18, "tile" if i == 0 else "ring") + t(41 + i * 52, 278, n, 5.5, MUTE, "hind", 600, "middle") for i, (n, c, k) in enumerate(AGENTS))
        return screen(topbar() + s)
    else:
        s = link(14, 60, "< Apps Home", LAGOON) + section(84, "Needs You") + "".join(row(90 + i * 38, n, d) for i, (n, d) in enumerate(OWED)) + t(120, 226, "Swipe For Next Agent", 7, MUTE, "hind", 600, "middle") + dots(238, 4, 0)
    return scr(s)
add(G, "Switch Agents", O("nav_dropdown", "Dropdown Of Agents", "Tap the name to switch agents.", ["clear", "compact"], "calm", nav("dropdown")),
    O("nav_strip", "Agent Icon Strip", "Row of agent icons up top.", ["visual", "fast"], "lively", nav("strip")), "Dropdown Or Icon Strip?")
add(G, "Switch Agents", O("nav_bottom", "Bottom Agent Bar", "Agents in a thumb bar at the bottom.", ["app", "fast"], "quick", nav("bottom")),
    O("nav_back", "Back To Apps Home Link", "One link back; swipe for the next.", ["simple", "minimal"], "calm", nav("back")), "Bottom Bar Or Back Link?")

# ---------------- Search ----------------
G = "Search"
def search(kind):
    if kind == "bar": s = rect(14, 54, 212, 28, SOFT, "none", 14) + ic("search", 24, 60, 15, MUTE) + t(44, 72, "Search Apps, Decisions, Work", 8, "#9A948A")
    elif kind == "icon": s = ic("search", 184, 14, 14) + section(66, "Needs You")
    else: s = rect(14, 54, 212, 28, "#FFFFFF", INK, 0, 1.4) + ic("search", 22, 60, 15) + t(42, 72, "visit", 8.5, INK) + rect(14, 82, 212, 80, "#FFFFFF", LINE) + "".join(t(24, 100 + i * 20, n, 8.5, INK) + tag(170, 92 + i * 20, g, c) for i, (n, g, c) in enumerate([("Visit Log App", "App", LAGOON), ("Visit Pricing Call", "Owed", TERRA), ("Shipped Visit Log", "Work", JUNGLE)]))
    y0 = 96 if kind == "bar" else (76 if kind == "icon" else 178)
    s += "".join(row(y0 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:3 if kind != "live" else 2]))
    return scr(s)
add(G, "Search", O("se_bar", "Always-On Search Bar", "Rounded bar under the header.", ["fast", "clear"], "quick", search("bar")),
    O("se_icon", "Search Icon Only", "Magnifier in the header; opens on tap.", ["minimal", "calm"], "calm", search("icon")), "Bar Or Icon?")
add(G, "Search", O("se_live", "Live Results With Type Tags", "Results tagged App, Owed, Work as you type.", ["clear", "rich"], "quick", search("live")),
    O("se_none", "No Search At All", "Short page; nothing to search.", ["simple", "minimal"], "calm", search("icon")), "Live Search Or None?")

# ---------------- Pinned ----------------
G = "Pinned Items"
def pin(kind):
    pins = [("Site Launch Checklist", TERRA), ("Q4 Price Sheet", LAGOON)]
    if kind == "top": s = section(62, "Pinned", TERRA) + "".join(rect(14, 70 + i * 34, 212, 28, SAFFRON + "14", "none", 6) + ic("star", 22, 76 + i * 34, 14, SAFFRON) + t(42, 88 + i * 34, n, 9.5, INK, "khand") for i, (n, c) in enumerate(pins)) + section(152, "Needs You") + "".join(row(158 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:2]))
    elif kind == "chips": s = "".join(rect(14 + i * 96, 54, 90, 18, SAFFRON + "1F", "none", 9) + ic("star", 20 + i * 96, 57, 11, SAFFRON) + t(34 + i * 96, 66, n.split()[0] + " " + n.split()[1], 7, INK, "hind", 600) for i, (n, c) in enumerate(pins)) + section(92, "Needs You") + "".join(row(98 + i * 38, n, d) for i, (n, d) in enumerate(OWED))
    elif kind == "card": s = rect(14, 54, 212, 74, "#FFFFFF", SAFFRON, 8, 1.2) + lbl(24, 70, "Pinned", SAFFRON) + "".join(ic("star", 24, 78 + i * 20, 12, SAFFRON) + t(42, 88 + i * 20, n, 9, INK, "khand") for i, (n, c) in enumerate(pins)) + section(146, "Needs You") + "".join(row(152 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:2]))
    else: s = section(62, "Needs You") + "".join(row(70 + i * 38, n, d) + (ic("star", 204, 80 + i * 38, 12, SAFFRON) if i == 0 else "") for i, (n, d) in enumerate(OWED)) + section(196, "Pinned") + "".join(link(14 + i * 110, 212, n.split()[0] + " " + n.split()[1], c) for i, (n, c) in enumerate(pins))
    return scr(s)
add(G, "Pinned", O("pin_top", "Pinned Strip At The Top", "Starred items sit above everything.", ["focused", "visual"], "lively", pin("top")),
    O("pin_inline", "Small Star, Pins Lower Down", "A star on rows; pinned links near the bottom.", ["calm", "minimal"], "calm", pin("inline")), "Pins Up Top Or Lower?")
add(G, "Pinned", O("pin_chips", "Pinned As Chips", "A row of small pinned chips under the header.", ["compact", "fast"], "quick", pin("chips")),
    O("pin_card", "One Pinned Card", "A single card holding pinned links.", ["calm", "clear"], "calm", pin("card")), "Chips Or A Card?")

# ---------------- Last Updated ----------------
G = "Last-Updated Stamp"
def stamp(kind):
    s = ""
    if kind == "header": s = rect(150, 52, 76, 14, JUNGLE + "1A", "none", 7) + dot(158, 59, 2.5, JUNGLE) + t(164, 62, "Updated 12 Min Ago", 5.8, JUNGLE, "hind", 600)
    elif kind == "footer": s = t(120, 280, "Last Updated Oct 13, 9:40 AM ICT", 6.5, MUTE, "hind", 400, "middle")
    s += section(84, "Needs You") + "".join(row(90 + i * 38, n, d) for i, (n, d) in enumerate(OWED))
    if kind == "each": s = section(84, "Needs You") + "".join(row(90 + i * 38, n, d, right=["2m", "1h", "3h"][i]) for i, (n, d) in enumerate(OWED))
    return scr(s)
add(G, "Updated Stamp", O("upd_header", "Green Badge Near The Top", "Updated 12 min ago, in a pill.", ["clear", "trust"], "lively", stamp("header")),
    O("upd_footer", "Small Line In The Footer", "Exact date and time at the bottom.", ["minimal", "calm"], "calm", stamp("footer")), "Top Badge Or Footer Line?")
add(G, "Updated Stamp", O("upd_each", "Time On Every Row", "Each item shows its own age.", ["scan", "rich"], "quick", stamp("each")),
    O("upd_header2", "One Page-Wide Stamp", "One updated badge for the whole page.", ["simple", "clear"], "calm", stamp("header")), "Per Row Or One Stamp?")

# ---------------- Empty States ----------------
G = "Empty States"
def empty(kind):
    if kind == "drawn": s = f'<circle cx="120" cy="120" r="44" fill="{JUNGLE}14"/>' + ic("check", 96, 96, 48, JUNGLE, 1.6) + h1(120, 190, "Nothing Owed", 18, INK, "middle") + t(120, 206, "You are all caught up.", 8, MUTE, "hind", 400, "middle")
    elif kind == "line": s = section(66, "Needs You") + t(14, 84, "Nothing waiting on you.", 8.5, MUTE) + ln(96) + section(118, "Recent") + "".join(row(124 + i * 38, a, b, LAGOON) for i, (a, b) in enumerate(WORK))
    elif kind == "hide": s = section(66, "Recent") + "".join(row(72 + i * 38, a, b, LAGOON) for i, (a, b) in enumerate(WORK)) + section(200, "Apps") + "".join(rect(14 + i * 72, 208, 66, 40, "#FFFFFF", LINE, 6) + ic(["home", "cal", "card"][i], 39 + i * 72, 220, 16, ACC[i]) for i in range(3))
    else: s = rect(14, 60, 212, 120, "#FFFFFF", "#CFC8BC", 10, 1, 'stroke-dasharray="4 3"') + ic("star", 104, 84, 32, SAFFRON) + t(120, 140, "No Pins Yet", 12, INK, "khand", anchor="middle") + t(120, 154, "Star anything to keep it here.", 7.5, MUTE, anchor="middle") + btn(196, "Browse Apps", "line", INK, 60, 120, 22, 7.5)
    return scr(s)
add(G, "Empty State", O("em_drawn", "Big Drawn Check, All Caught Up", "Friendly drawn mark and a short line.", ["warm", "visual"], "lively", empty("drawn")),
    O("em_line", "One Grey Line", "A plain line where the list would be.", ["minimal", "calm"], "calm", empty("line")), "Drawn Or One Line?")
add(G, "Empty State", O("em_hide", "Hide Empty Sections", "Empty sections just disappear.", ["simple", "focused"], "quick", empty("hide")),
    O("em_hint", "Dashed Box With A Hint", "Shows how to fill it, with a button.", ["guided", "warm"], "lively", empty("hint")), "Hide Or Hint?")

# ---------------- Grouping ----------------
G = "Grouping"
def grp(kind):
    gs = [("Work", TERRA, ["Prop", "Up Keep", "Blueprint"]), ("Personal", JUNGLE, ["WellNest", "Portfolio"]), ("AI Resources", LAGOON, ["Style Swipe", "Branding"])]
    if kind == "tabs":
        s = rect(14, 54, 212, 26, SOFT, "none", 13) + rect(16, 56, 70, 22, "#FFFFFF", LINE, 11) + "".join(t(51 + i * 70, 71, g, 8, INK if i == 0 else MUTE, "khand", anchor="middle") for i, (g, c, a) in enumerate(gs))
        s += "".join(row(92 + i * 38, n, "Agent dashboard", TERRA, ">") for i, n in enumerate(gs[0][2]))
    elif kind == "stack":
        s, y = "", 58
        for g, c, a in gs:
            s += rect(14, y, 4, 12, c) + t(24, y + 10, g, 11, INK, "khand"); y += 18
            for n in a: s += t(24, y + 8, n, 8.5, INK) + ic("chev", 212, y, 10, MUTE); y += 16
            y += 8
    elif kind == "color":
        s = "".join(rect(14 + (i % 2) * 108, 56 + (i // 2) * 52, 104, 46, c + "14", c, 8, 1) + lbl(22 + (i % 2) * 108, 70 + (i // 2) * 52, g, c, 5.5) + t(22 + (i % 2) * 108, 88 + (i // 2) * 52, n, 10, INK, "khand") for i, (n, g, c) in enumerate([(n, g, c) for g, c, a in gs for n in a]))
    else:
        s = "".join(rect(14, 56 + i * 56, 212, 50, "#FFFFFF", LINE, 8) + ic(["card", "heart", "star"][i], 24, 72 + i * 56, 18, c) + t(52, 78 + i * 56, g, 12, INK, "khand") + t(52, 92 + i * 56, f"{len(a)} agents", 7, MUTE) + ic("down", 204, 72 + i * 56, 14, MUTE) for i, (g, c, a) in enumerate(gs))
    return scr(s, name="Apps Home", sub="All Agents", c=INK, k="home")
add(G, "Work / Personal / AI Resources", O("gr_tabs", "Pill Tabs For The Three Groups", "Work, Personal, AI Resources as a segmented pill.", ["clear", "app"], "calm", grp("tabs")),
    O("gr_stack", "All Three Groups Stacked", "Every agent on one page under color-tabbed headings.", ["scan", "fast"], "quick", grp("stack")), "Tabs Or Stacked?")
add(G, "Work / Personal / AI Resources", O("gr_color", "Color-Coded Agent Cards", "Each group has its own color on the card.", ["visual", "lively"], "lively", grp("color")),
    O("gr_fold", "Folding Group Rows", "Three rows that open to show agents.", ["minimal", "calm"], "calm", grp("fold")), "Color Cards Or Folding Rows?")

# ---------------- Agent Identity ----------------
G = "Agent Identity"
def ident(kind):
    s = section(62, "Your Agents")
    for i, (n, c, k) in enumerate(AGENTS):
        y = 70 + i * 44
        if kind == "tile": s += avatar(14, y, c, k, 32) + t(56, y + 15, n, 12, INK, "khand") + t(56, y + 27, "Command Center", 7, MUTE)
        elif kind == "mono": s += rect(14, y, 32, 32, "#FFFFFF", c, 16, 1.6) + t(30, y + 22, n[0], 16, c, "khand", anchor="middle") + t(56, y + 15, n, 12, INK, "khand") + t(56, y + 27, "Command Center", 7, MUTE)
        elif kind == "stripe": s += rect(14, y, 212, 36, "#FFFFFF", LINE, 4) + rect(14, y, 5, 36, c) + t(28, y + 16, n, 12, INK, "khand") + t(28, y + 28, "Command Center", 7, MUTE)
        else: s += ic(k, 14, y + 4, 22, INK, 1.6) + t(48, y + 15, n, 12, INK, "khand") + t(48, y + 27, "Command Center", 7, MUTE)
    return scr(s, name="Apps Home", sub="All Agents", c=INK)
add(G, "Agent Identity", O("id_tile", "Color Tile With Icon", "Each agent gets a colored square and icon.", ["visual", "app"], "lively", ident("tile")),
    O("id_mono", "Letter In A Color Circle", "First letter in the agent's color.", ["simple", "warm"], "calm", ident("mono")), "Icon Tile Or Letter?")
add(G, "Agent Identity", O("id_stripe", "Color Stripe, Name Only", "A thin color edge on each card.", ["minimal", "clear"], "calm", ident("stripe")),
    O("id_icon", "Black Icon, No Color", "One ink icon per agent, names carry it.", ["minimal", "calm"], "calm", ident("icon")), "Stripe Or Black Icon?")

# ---------------- Buttons And Hover ----------------
G = "Buttons And Hover"
def buttons(kind):
    s = section(62, "Primary Button")
    if kind == "square": s += btn(72, "Review Decisions") + section(120, "On Hover") + btn(130, "Review Decisions", "fill", TERRA) + t(14, 172, "Square corners; turns terracotta on hover.", 7.5, MUTE)
    elif kind == "pill": s += rect(14, 72, 212, 28, TERRA, "none", 14) + t(120, 90, "Review Decisions", 10, "#FFFFFF", "khand", anchor="middle") + section(120, "On Hover") + rect(14, 132, 212, 28, TERRA, "none", 14, extra='filter="drop-shadow(0 3px 3px #0003)"') + t(120, 150, "Review Decisions", 10, "#FFFFFF", "khand", anchor="middle") + t(14, 178, "Round pill; lifts with a shadow on hover.", 7.5, MUTE)
    elif kind == "outline": s += btn(72, "Review Decisions", "line", INK) + section(120, "On Hover") + btn(130, "Review Decisions", "fill", INK) + t(14, 172, "Outline; fills black on hover.", 7.5, MUTE)
    else: s += link(14, 88, "Review Decisions >", TERRA, size=9) + section(120, "On Hover") + rect(14, 130, 140, 22, TERRA + "14", "none", 4) + link(20, 145, "Review Decisions >", TERRA, size=9) + t(14, 172, "Text link; soft tint behind on hover.", 7.5, MUTE)
    return scr(s)
add(G, "Buttons", O("bt_square", "Square Black, Terracotta Hover", "Brand square button.", ["bold", "clear"], "quick", buttons("square")),
    O("bt_pill", "Rounded Pill, Lift On Hover", "Soft pill that rises.", ["warm", "app"], "lively", buttons("pill")), "Square Or Pill?")
add(G, "Buttons", O("bt_outline", "Outline That Fills", "Black outline; fills on hover.", ["calm", "minimal"], "calm", buttons("outline")),
    O("bt_link", "Text Link With Tint", "Underlined link, tint on hover.", ["minimal", "light"], "calm", buttons("link")), "Outline Or Text Link?")

# ---------------- Badges ----------------
G = "Notification Badges"
def badge(kind):
    s = section(62, "Your Agents")
    for i, (n, c, k) in enumerate(AGENTS):
        y = 70 + i * 44; cnt = [3, 0, 1, 2][i]
        s += avatar(14, y, c, k, 30) + t(54, y + 19, n, 12, INK, "khand")
        if cnt:
            if kind == "count": s += f'<circle cx="42" cy="{y+2}" r="7" fill="{TERRA}" stroke="#FFFFFF" stroke-width="1.5"/>' + t(42, y + 5, str(cnt), 7.5, "#FFFFFF", "hind", 700, "middle")
            elif kind == "dot": s += f'<circle cx="42" cy="{y+2}" r="4" fill="{TERRA}" stroke="#FFFFFF" stroke-width="1.5"/>'
            elif kind == "text": s += t(226, y + 19, f"{cnt} Owed", 8, TERRA, "hind", 600, "end")
            else: s += tag(170, y + 10, f"{cnt} New", SAFFRON, True)
    return scr(s, name="Apps Home", sub="All Agents", c=INK)
add(G, "Badges", O("bd_count", "Red-Orange Count Bubble", "Number on the icon corner.", ["clear", "app"], "quick", badge("count")),
    O("bd_dot", "Small Dot, No Number", "Just a dot when something is waiting.", ["minimal", "calm"], "calm", badge("dot")), "Count Or Dot?")
add(G, "Badges", O("bd_text", "Words On The Right", "'3 Owed' in terracotta text.", ["readable", "clear"], "calm", badge("text")),
    O("bd_pill", "Saffron New Pill", "Solid saffron pill with the count.", ["visual", "lively"], "lively", badge("pill")), "Words Or Pill?")

# ---------------- Calendar ----------------
G = "Calendar And Timeline"
def cal(kind):
    if kind == "week":
        s = section(62, "This Week") + "".join(t(30 + i * 30, 80, d, 7, MUTE, "hind", 600, "middle") + t(30 + i * 30, 96, str(12 + i), 11, "#FFFFFF" if i == 1 else INK, "khand", anchor="middle") for i, d in enumerate("MTWTFSS"))
        s = s.replace("", "", 0)
        s = section(62, "This Week") + f'<circle cx="60" cy="92" r="10" fill="{TERRA}"/>' + "".join(t(30 + i * 30, 80, d, 7, MUTE, "hind", 600, "middle") + t(30 + i * 30, 96, str(12 + i), 11, "#FFFFFF" if i == 1 else INK, "khand", anchor="middle") + (dot(30 + i * 30, 106, 2, LAGOON) if i in (3, 4) else "") for i, d in enumerate("MTWTFSS"))
        s += "".join(row(120 + i * 38, n, d, c, k="cal") for i, (n, d, c) in enumerate([("Pricing Call", "Thu 10 AM", LAGOON), ("Tax Draft Due", "Fri", SAFFRON), ("Ship Tech App", "Next Mon", JUNGLE)]))
    elif kind == "month":
        s = section(62, "October") + "".join(t(24 + i * 30, 78, d, 6.5, MUTE, "hind", 600, "middle") for i, d in enumerate("MTWTFSS"))
        for d in range(31):
            r, c = divmod(d + 3, 7); x, y = 24 + c * 30, 96 + r * 26
            s += (f'<circle cx="{x}" cy="{y-4}" r="9" fill="{TERRA}"/>' if d == 12 else "") + t(x, y, str(d + 1), 8, "#FFFFFF" if d == 12 else INK, "hind", 600, "middle") + (dot(x, y + 5, 1.8, [LAGOON, SAFFRON, JUNGLE][d % 3]) if d in (14, 15, 18, 22, 27) else "")
    elif kind == "gantt":
        s = section(62, "Timeline") + "".join(f'<line x1="{80+i*36}" y1="70" x2="{80+i*36}" y2="210" stroke="{LINE}"/>' + t(80 + i * 36, 222, ["Oct", "Nov", "Dec", "Jan"][i], 6.5, MUTE, anchor="middle") for i in range(4))
        s += "".join(t(14, 88 + i * 30, n, 8, INK, "khand") + rect(x0, 80 + i * 30, w, 12, c, "none", 6) for i, (n, x0, w, c) in enumerate([("Visit Log", 80, 40, JUNGLE), ("Pricing", 100, 60, LAGOON), ("Tech App", 130, 70, SAFFRON), ("Launch", 180, 30, TERRA)]))
    else:
        s = section(62, "Coming Up") + "".join(t(14, 84 + i * 40, dd, 18, c, "khand") + t(14, 96 + i * 40, mm, 6.5, MUTE, "hind", 600) + t(54, 84 + i * 40, n, 11, INK, "khand") + t(54, 96 + i * 40, w, 7, MUTE) + ln(104 + i * 40, 54) for i, (dd, mm, n, w, c) in enumerate([("15", "THU", "Pricing Call", "10:00 AM · Prop", LAGOON), ("16", "FRI", "Tax Draft Due", "Portfolio", SAFFRON), ("19", "MON", "Ship Tech App", "Up Keep", JUNGLE), ("23", "FRI", "Site Launch", "Prop", TERRA)]))
    return scr(s)
add(G, "Calendar", O("cal_week", "Week Strip Plus List", "Seven days across, events below.", ["clear", "app"], "calm", cal("week")),
    O("cal_month", "Full Month Grid", "Whole month with colored dots.", ["visual", "rich"], "lively", cal("month")), "Week Or Month?")
add(G, "Calendar", O("cal_gantt", "Project Timeline Bars", "Bars across months per project.", ["visual", "scan"], "quick", cal("gantt")),
    O("cal_agenda", "Date-Led Agenda", "Big date number, event beside it.", ["readable", "calm"], "calm", cal("agenda")), "Timeline Or Agenda?")

# ---------------- Charts ----------------
G = "Charts"
def chart(kind):
    vals = [.3, .45, .4, .6, .55, .7, .85]
    s = section(62, "Work Shipped Per Day") + rect(14, 70, 212, 130, "#FFFFFF", LINE, 8)
    if kind == "bars": s += bars(24, 84, 192, 96, vals)
    elif kind == "line":
        pts = " ".join(f"{30+i*30},{180-v*96:.0f}" for i, v in enumerate(vals))
        s += f'<polyline points="{pts}" fill="none" stroke="{LAGOON}" stroke-width="2.4" stroke-linejoin="round"/>' + f'<polygon points="30,180 {pts} 210,180" fill="{LAGOON}14"/>' + dot(210, 180 - .85 * 96, 4, TERRA)
    elif kind == "spark": s = section(62, "This Week") + "".join(rect(14, 70 + i * 44, 212, 38, "#FFFFFF", LINE, 6) + t(24, 88 + i * 44, n, 10, INK, "khand") + t(24, 99 + i * 44, v, 7, MUTE) + f'<polyline points="{" ".join(f"{140+k*12},{100+i*44-vals[(k+i)%7]*20:.0f}" for k in range(7))}" fill="none" stroke="{c}" stroke-width="1.8"/>' for i, (n, v, c) in enumerate([("Shipped", "14 items", JUNGLE), ("Decisions", "6 made", TERRA), ("Visits", "230", LAGOON), ("Hours", "31", SAFFRON)]))
    else: s = section(62, "This Week") + "".join(rect(14 + (i % 2) * 108, 70 + (i // 2) * 70, 104, 64, "#FFFFFF", LINE, 8) + t(24 + (i % 2) * 108, 104 + (i // 2) * 70, v, 24, c, "khand") + t(24 + (i % 2) * 108, 122 + (i // 2) * 70, n, 7.5, MUTE) for i, (n, v, c) in enumerate([("Shipped", "14", JUNGLE), ("Decisions", "6", TERRA), ("Visits", "230", LAGOON), ("Hours", "31", SAFFRON)]))
    return scr(s)
add(G, "Charts", O("ch_bars", "Simple Bar Chart", "One bar per day, today darker.", ["clear", "visual"], "calm", chart("bars")),
    O("ch_line", "Line With Soft Fill", "Smooth trend line, today dotted.", ["visual", "calm"], "lively", chart("line")), "Bars Or Line?")
add(G, "Charts", O("ch_spark", "Tiny Sparklines Per Stat", "Small trend line beside each number.", ["scan", "rich"], "quick", chart("spark")),
    O("ch_numbers", "Big Numbers, No Charts", "Four big colored numbers.", ["big", "simple"], "lively", chart("numbers")), "Sparklines Or Just Numbers?")

# ---------------- Quick Actions ----------------
G = "Quick Actions"
def quick(kind):
    acts = [("Share", "tag"), ("Ask", "mic"), ("Note", "star"), ("Open Site", "home")]
    base = section(64, "Needs You") + "".join(row(70 + i * 38, n, d) for i, (n, d) in enumerate(OWED[:3]))
    if kind == "row": s = "".join(rect(14 + i * 54, 54, 48, 44, SOFT, "none", 8) + ic(k, 30 + i * 54, 60, 16, ACC[i]) + t(38 + i * 54, 90, n, 6.5, INK, "hind", 600, "middle") for i, (n, k) in enumerate(acts)) + base.replace('y="64"', 'y="116"', 1).replace("", "")
    s = ("".join(rect(14 + i * 54, 52, 48, 44, SOFT, "none", 8) + ic(k, 30 + i * 54, 58, 16, ACC[i]) + t(38 + i * 54, 88, n, 6.5, INK, "hind", 600, "middle") for i, (n, k) in enumerate(acts)) + section(114, "Needs You") + "".join(row(120 + i * 38, n, d) for i, (n, d) in enumerate(OWED))) if kind == "row" else \
        (base + f'<circle cx="204" cy="252" r="18" fill="{TERRA}" filter="drop-shadow(0 2px 3px #0003)"/><path d="M204 244 V260 M196 252 H212" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>' if kind == "fab" else
         base + rect(14, 194, 212, 30, "#FFFFFF", LINE, 6) + ic("mic", 22, 201, 16, TERRA) + t(44, 213, "Tell Prop Anything...", 8, "#9A948A") if kind == "ask" else
         base + "".join(link(14 + i * 56, 200, n, ACC[i]) for i, (n, k) in enumerate(acts)))
    return scr(s)
add(G, "Quick Actions", O("qa_row", "Icon Action Row Up Top", "Share, Ask, Note, Open Site in a row.", ["fast", "app"], "quick", quick("row")),
    O("qa_fab", "One Floating Plus Button", "Terracotta plus in the corner.", ["minimal", "app"], "calm", quick("fab")), "Action Row Or Plus Button?")
add(G, "Quick Actions", O("qa_ask", "Ask-The-Agent Box", "A box to tell the agent anything.", ["warm", "action"], "lively", quick("ask")),
    O("qa_links", "Small Text Actions", "Four underlined words under the list.", ["minimal", "light"], "calm", quick("links")), "Ask Box Or Text Actions?")

finish(DID, "Agent Dashboard Round 1: Layout, Header, Status, Density, First Screen, App Tiles, Feed, Decisions Owed, Progress, Icons, Color, Desktop, Navigation, Search, Pins, Stamps, Empty States, Groups, Identity, Buttons, Badges, Calendar, Charts, Quick Actions", "Agent Dashboard", pairs, 0,
       {"brands": ["Agent command-center dashboards (every agent; spec /workspace/ops/apps-home/AGENT-DASHBOARD-SPEC.md)", "White light mode, Khand/Hind, Title Case, no emoji, small pops of #C1502E #05668D #0B6E4F #D4A017; no neon or pastel"],
        "feelings": {"calm": "Calm and organized", "lively": "Lively and visual", "quick": "Quick and action-first"},
        "sources": {"spec": "/workspace/ops/apps-home/AGENT-DASHBOARD-SPEC.md", "example": "/workspace/branding-dashboard/", "feed": "/workspace/ops/team-feed.md"}}, seed=24)
d = json.load(open(f"decks/{DID}.json")); d.pop("draft", None); d["status"] = "published"; d["share"] = True
for pp in d["pairs"]:
    pp["notes"] = True; pp["share"] = True
    for k in "AB": o = pp["option" + k]; o["tags"] = list(dict.fromkeys(o["tags"]))
json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
