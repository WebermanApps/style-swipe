#!/usr/bin/env python3
"""Build Style Swipe deck rulebook-tiebreak: Rulebook Tiebreak Deck (Oct 14 2026). Follow-up to Rulebook Clash (results/rulebook-clash.txt):
carried skip first (C7 pure white vs cream), C9 accents re-asked (Max picked both), scope checks for the settled C1/C4/C5 picks,
and the C8 open dashboard tiebreaks from dashboard-style.md. Max brand. Submit -> agent 'branding'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
DID = "rulebook-tiebreak"
B = dict(name="Apps Home", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("rt_", "Branding")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(title="Apps Home", sub="Example dashboard", tnames=["Upkeep", "Portfolio", "WellNest", "Decks"], tn=4, report="more", urgent="pill", dens=2)
def wrap(s, n):
    w, l, c = s.split(), [], ""
    for x in w:
        if len(c) + len(x) + 1 > n and c: l.append(c); c = x
        else: c = (c + " " + x).strip()
    return l + [c]
def quote(s, src):
    ls = wrap(s, 40); out = R(14, 222, 212, 18 + len(ls) * 10, "#FFFFFF", B["line"], 8) + R(14, 222, 3, 18 + len(ls) * 10, B["acc"][1], r=1.5)
    out += "".join(T(B, 24, 236 + i * 10, l, 7.5, B["ink"]) for i, l in enumerate(ls)) + T(B, 24, 246 + (len(ls) - 1) * 10, src, 6, B["mute"], w=600)
    return out
def scr(order, q, src, extra="", bg="#FFFFFF", **k):
    g, _ = stack({**B, "bg": bg}, order, {**base, **k}, 10)
    return screen(g + extra + quote(q, src), bg)
def plain(body, q, src, bg="#FFFFFF"): return screen(body + quote(q, src), bg)
FOOT = lambda y: L(14, y, 226, y, B["line"]) + T(B, 120, y + 12, "Built by Max Weberman", 6.5, B["mute"], a="middle")
SHARE = lambda x=206, y=16: f'<g transform="translate({x},{y}) scale(.6)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{B["ink"]}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{B["ink"]}" stroke-width="2.2"/></g>'
def title(s, sub=""): return T(B, 14, 30, s, 18, None, True) + (T(B, 14, 42, sub, 7, B["mute"]) if sub else "")
# 1. C7 carried skip: pure white vs light cream
def base_(bg, nm):
    s = title("Page Base", nm)
    s += R(14, 52, 212, 150, bg, B["line"], 10) + card(B, 28, 66, 184, 54) + T(B, 38, 84, "White Card", 10, None, True) + bars(2, 38, 94, 150, B["mute"] + "88", 8) + card(B, 28, 130, 184, 54) + bars(3, 38, 146, 150, B["mute"] + "88", 8)
    return s
G = "C7 Page Base"
P(G, "Page Base: Pure White Or Light Cream?",
  ("c7_white", "Pure White #FFFFFF", "UpKeep board pick.", "focused", plain(base_("#FFFFFF", "#FFFFFF"), "Pure white page, white cards with thin lines.", "UPKEEP BOARD")),
  ("c7_cream", "Light Cream #FDFBF6", "Beat rice-white last deck.", "calm", plain(base_("#FDFBF6", "#FDFBF6"), "Very light cream page with white cards.", "DECKS, R58", "#FDFBF6")))
# 2. C9 accents re-ask
G = "C9 Accent Palette"
P(G, "Accents: Small Pops On Every Dashboard Or Only Where A Board Picked Them?",
  ("c9_all", "Small Pops On Every Dashboard", "Terracotta, lagoon, jungle, saffron as small accents.", "visual", scr(["hdr", "report", "tiles"], "Small colour pops on every dashboard, mostly on actions.", "APPROVE FOR ALL", tiles="tint", tn=2)),
  ("c9_board", "Only Where A Board Picked Them", "Ink-only until a board deck picks a colour.", "calm", scr(["hdr", "report", "tiles"], "Ink and grey by default; colour only where a board deck chose it.", "BOARD BY BOARD", tiles="lineplain", uc="#525252", rc="#525252", tn=2)))
# 3. C5 scope
tabs = R(0, 186, W, 32, "#FFFFFF", B["line"]) + "".join(tile_icon(28 + i * 52, 191, i, LAGOON if i == 0 else B["mute"], 12) + T(B, 34 + i * 52, 212, n, 5.5, LAGOON if i == 0 else B["mute"], a="middle") for i, n in enumerate(["Home", "Apps", "Decks", "Feed"]))
G = "C5 Bottom Tabs Scope"
P(G, "Bottom Tab Bar On Phone: Apps Home Only Or Every Dashboard?",
  ("c5_home", "Apps Home Only", "Other dashboards keep no bottom bar.", "calm", scr(["hdr", "report", "tiles"], "Agent dashboards: no bottom bar, slim top header only.", "APPS HOME ONLY", R(0, 0, W, 4, LAGOON) + FOOT(204), title="Upkeep", tn=2)),
  ("c5_all", "Every Dashboard On Phone", "Same lagoon tab bar on each agent dashboard.", "action", scr(["hdr", "report", "tiles"], "Every agent dashboard gets the lagoon tab bar on phone.", "EVERY DASHBOARD", tabs, title="Upkeep", tn=2)))
# 4. C1 scope
def deckmock(share_top):
    s = title("Style Swipe", "Deck 3 of 12") + (SHARE() if share_top else "")
    s += R(14, 52, 101, 110, "#FFFFFF", B["line"], 8) + R(125, 52, 101, 110, "#FFFFFF", B["line"], 8) + R(22, 60, 85, 70, B["soft"], r=6) + R(133, 60, 85, 70, B["soft"], r=6)
    s += T(B, 64, 148, "Option A", 8, None, True, a="middle") + T(B, 175, 148, "Option B", 8, None, True, a="middle")
    if not share_top: s += R(64, 176, 112, 24, "#FFFFFF", B["ink"], 0, 1.6) + T(B, 120, 191.5, "SHARE", 8, B["ink"], w=600, a="middle", ex='letter-spacing="1.2"')
    else: s += R(14, 176, 212, 24, JUNGLE, r=4) + T(B, 120, 191.5, "SUBMIT", 8, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"')
    return s + FOOT(206)
G = "C1 Share Scope"
P(G, "Header Share Icon: Dashboards Only Or Decks Too?",
  ("c1_dash", "Dashboards Only", "Decks and swipe apps keep Share at the end.", "calm", plain(deckmock(False), "Decks keep a Share button at the end, by Submit.", "DECKS UNCHANGED", "#FDFBF6")),
  ("c1_all", "Decks And Apps Too", "Same small header icon everywhere.", "quick", plain(deckmock(True), "Small Share icon in the header corner on decks too.", "EVERYWHERE", "#FDFBF6")))
# 5. C4 scope
def caps(mode):
    pg = "APPS HOME" if mode == "all" else "Apps Home"; ex = 'letter-spacing="1.6"'
    s = T(B, 14, 34, pg, 20 if mode == "all" else 24, None, True, ex=ex if mode == "all" else "") + L(14, 44, 226, 44, B["line"])
    for i, h in enumerate(["Waiting On Max", "Latest Open Items", "Recent Work"]):
        y = 68 + i * 48; s += T(B, 14, y, h.upper(), 9, B["mute"], w=600, ex=ex) + T(B, 14, y + 14, "Card title here", 11, None, True) + bars(2, 14, y + 22, 200, B["mute"] + "88", 7)
    return s
G = "C4 Spaced Caps Scope"
P(G, "Spaced Caps: Section Labels Only Or Page Titles Too?",
  ("c4_labels", "Section Labels Only", "Page title stays Title Case.", "calm", plain(caps("labels"), "Title Case page title; small spaced-caps section labels.", "LABELS ONLY")),
  ("c4_titles", "Page Titles Too", "Big title and labels in spaced caps.", "focused", plain(caps("all"), "Page title and section labels in spaced caps.", "TITLES TOO")))
# 6. C8 grid vs tabs
def grid():
    s = title("Apps Home")
    for i in range(4):
        x, y = 14 + (i % 2) * 108, 52 + (i // 2) * 76
        s += card(B, x, y, 104, 70) + tile_icon(x + 10, y + 10, i, B["acc"][i], 14) + T(B, x + 10, y + 44, ["Upkeep", "Portfolio", "WellNest", "Decks"][i], 9, None, True) + bars(1, x + 10, y + 52, 70, B["mute"] + "88")
    return s
def tabsrow():
    s = title("Apps Home")
    for i, n in enumerate(["Upkeep", "Portfolio", "WellNest"]):
        x = 14 + i * 64; s += R(x, 50, 58, 20, LAGOON if i == 0 else "#FFFFFF", LAGOON if i == 0 else B["line"], 10) + T(B, x + 29, 63.5, n, 7, "#FFFFFF" if i == 0 else B["ink"], w=600, a="middle")
    for j in range(4): s += card(B, 14, 80 + j * 34, 212, 28) + T(B, 24, 98 + j * 34, ["Report", "Open Items", "Feed", "Apps"][j], 8.5, None, True) + bars(1, 90, 92 + j * 34, 120, B["mute"] + "88")
    return s
G = "C8 Tiebreaks"
P(G, "Home Layout: Grid Of Cards Or Tabs Across The Top?",
  ("c8_grid", "Grid Of Cards", "See every agent at once.", "visual", plain(grid(), "One card per agent in a grid.", "DASHBOARD-1, PICKED BOTH")),
  ("c8_tabs", "Tabs Across The Top", "One agent at a time.", "focused", plain(tabsrow(), "Pill tabs across the top, one agent shown below.", "DASHBOARD-1, PICKED BOTH")))
# 7. pinned strip vs chips
def pinned(kind):
    s = title("Apps Home", "Pinned")
    if kind == "strip":
        s += R(14, 52, 212, 44, LAGOON + "12", r=8) + "".join(tile_icon(26 + i * 50, 60, i, LAGOON, 14) + T(B, 33 + i * 50, 88, n, 6, B["ink"], a="middle") for i, n in enumerate(["Decks", "Feed", "Upkeep", "Folio"]))
        y = 106
    else:
        x = 14
        for n in ["Decks", "Feed", "Upkeep", "Folio"]:
            w = len(n) * 5 + 22; s += R(x, 54, w, 18, "#FFFFFF", LAGOON, 9) + T(B, x + w / 2, 66, n, 7, LAGOON, w=600, a="middle"); x += w + 6
        y = 82
    for j in range(3): s += card(B, 14, y + j * 36, 212, 30) + bars(2, 24, y + 10 + j * 36, 170, B["mute"] + "88", 7)
    return s
P(G, "Pinned Apps: Strip At The Top Or Small Chips?",
  ("c8_strip", "Pinned Strip", "Tinted row of icons.", "visual", plain(pinned("strip"), "A tinted strip of pinned app icons at the top.", "DASHBOARD-1, PICKED BOTH")),
  ("c8_chips", "Pinned Chips", "Small outline chips, less space.", "quick", plain(pinned("chips"), "Small outline chips for pinned apps.", "DASHBOARD-1, PICKED BOTH")))
# 8. empty sections
def empty(kind):
    s = title("Upkeep", "Dashboard")
    s += card(B, 14, 52, 212, 50) + T(B, 24, 68, "Waiting On Max", 9, None, True) + bars(2, 24, 78, 170, B["mute"] + "88", 7)
    y = 110
    if kind == "line": s += T(B, 14, y + 10, "No open items right now", 7.5, "#9A9A9A"); y += 22
    s += card(B, 14, y, 212, 50) + T(B, 24, y + 16, "Recent Work", 9, None, True) + bars(2, 24, y + 26, 170, B["mute"] + "88", 7)
    return s
P(G, "Empty Sections: Hide Them Or Show One Grey Line?",
  ("c8_hide", "Hide Empty Sections", "Cleaner page.", "calm", plain(empty("hide"), "A section with nothing in it disappears.", "DASHBOARD-1, PICKED BOTH")),
  ("c8_line", "One Grey Line", "You can see it is empty, not missing.", "focused", plain(empty("line"), "Empty section shows one quiet grey line.", "DASHBOARD-1, PICKED BOTH")))
# 9. header name size
def hsize(px):
    s = T(B, 14, 22 + px, "Upkeep", px * 1.15, None, True) + T(B, 226, 18 + px, "Updated 5m ago", 6.5, JUNGLE, a="end") + L(14, 30 + px, 226, 30 + px, B["line"])
    for j in range(3): s += card(B, 14, 44 + px + j * 44, 212, 38) + bars(2, 24, 56 + px + j * 44, 170, B["mute"] + "88", 7)
    return s
P(G, "Header Name: 16px Or 19px?",
  ("c8_h16", "16px, Quieter", "More room for content.", "calm", plain(hsize(16), "Agent name at 16px in the top bar.", "DASHBOARD-2, SKIPPED")),
  ("c8_h19", "19px, Clearer", "Easier to spot which board.", "focused", plain(hsize(19), "Agent name at 19px in the top bar.", "DASHBOARD-2, SKIPPED")))
# 10. buttons
def buttons(kind):
    s = title("Waiting On Max")
    for j in range(3):
        y = 52 + j * 52; s += card(B, 14, y, 212, 44) + T(B, 24, y + 16, ["Approve the video", "Pick a logo", "Answer deck"][j], 9, None, True)
        r = 0 if kind == "square" else 11; fill = B["ink"]
        s += R(24, y + 22, 60, 16, fill, fill, r) + T(B, 54, y + 33, "YES", 6.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1"') + R(90, y + 22, 60, 16, "#FFFFFF", fill, r) + T(B, 120, y + 33, "LATER", 6.5, fill, w=600, a="middle", ex='letter-spacing="1"')
    return s
P(G, "Buttons: Square Black Or Rounded Pill?",
  ("c8_sq", "Square Black", "Sharp, matches the deck buttons.", "focused", plain(buttons("square"), "Square black buttons with square outline partners.", "DASHBOARD-2, SKIPPED")),
  ("c8_pill", "Rounded Pill", "Softer, matches the status chips.", "calm", plain(buttons("pill"), "Rounded pill buttons.", "DASHBOARD-2, SKIPPED")))
# 11. stamp
def stamp(kind):
    s = title("Team Feed") + (T(B, 226, 30, "Updated 13:20", 7, JUNGLE, a="end") if kind == "page" else "")
    for j in range(5):
        y = 50 + j * 32; s += card(B, 14, y, 212, 26) + T(B, 24, y + 16, ["UpKeep shipped home v2", "Coach new round", "Portfolio picks applied", "WellNest icon", "Security live"][j], 8, None)
        if kind == "row": s += T(B, 216, y + 16, ["13:20", "13:10", "13:09", "13:00", "12:45"][j], 7, B["mute"], a="end")
    return s
P(G, "Times: One Per Row Or One Page Stamp?",
  ("c8_row", "Time On Each Row", "See when each thing happened.", "focused", plain(stamp("row"), "Each row shows its own time, right-aligned.", "DASHBOARD-2, SKIPPED")),
  ("c8_page", "One Page Stamp", "Cleaner rows.", "calm", plain(stamp("page"), "One Updated stamp at the top of the page.", "DASHBOARD-2, SKIPPED")))
# 12. feed detail
def feed(kind):
    s = title("Team Feed")
    for j in range(4 if kind == "log" else 3):
        if kind == "log":
            y = 50 + j * 26; s += L(14, y + 22, 226, y + 22, B["line"]) + T(B, 14, y + 14, ["13:20 UpKeep · shipped home v2", "13:10 Coach · new round live", "13:09 Portfolio · picks applied", "13:00 WellNest · new icon"][j], 7.5, B["ink"])
        else:
            y = 50 + j * 50; s += card(B, 14, y, 212, 44, "left", B["acc"][j]) + T(B, 24, y + 17, ["UpKeep Shipped Home V2", "Coach Round 2 Live", "Portfolio Picks Applied"][j], 9, None, True) + T(B, 24, y + 31, ["Bigger logo, plan pill, Plus centred", "Five cards on duplicate rules", "Folio deck, 19 of 20"][j], 7, B["mute"])
    return s
P(G, "Feed Detail: Log Lines Or Headline Plus Note?",
  ("c8_log", "Log Lines", "Many items, one line each.", "quick", plain(feed("log"), "One plain log line per item.", "DASHBOARD-2, SKIPPED")),
  ("c8_head", "Headline Plus Note", "Fewer items, easier to read.", "visual", plain(feed("head"), "Short headline with a one-line note under it.", "DASHBOARD-2, SKIPPED")))
N = len(pairs); assert N == 12, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Rulebook Tiebreak Deck", "Branding", pairs,
        {"brands": ["Rulebook Tiebreak: follow-up to Rulebook Clash (skipped white vs cream first, accents re-asked, scope of settled Share / caps / tab-bar picks, open dashboard tiebreaks)", "Max brand on the light cream deck page with white cards"],
         "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "section_counts": cnt, "deck_size": N,
         "trim_override": f"{N} pairs: short follow-up deck", "sources": {"rulebook": "/workspace/ops/brand/dashboard-rulebook.md", "results": "results/rulebook-clash.txt"}},
        seed=1032, n=N, first=1)
