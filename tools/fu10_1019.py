"""Branding follow-up decks, Oct 19 2026 16:10 ICT (Max: 'prepare fresh new decks on the same topics i swiped on ... i like 10 at a time').
Nine 10-pair decks, each one level past his Oct 19 picks and notes (no decided pair repeated). UpKeep decks reuse the Oct 19 board kits
(ukhf1019_*, sched1019) drawn in the decided state, with a terracotta CLOSE-UP panel showing the one element being asked.
Machan decks reuse machan1018 / mfu1019 (light cream). PRIVACY: Tech Dash 1-3 / Van 1-3, first names or member IDs, TEST / SAMPLE only."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
from md1018_kit import make
from ukhf1019_kit import *
from ukhf1019_kit import frame as kframe
import ukhf1019_header as HD, ukhf1019_footer as FT, ukhf1019_tech as TC, ukhf1019_tools as TL, sched1019 as SC
import machan1018 as M
from mfu1019 import mk
from draft_svg import rect, ln, W

def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
def callout(title, body, y0=246, h=196):
    return (R(14, y0, 424, h, WHITE, TERRA, 8, 1.4) + R(14, y0, 424, 22, TERRA + "14", rx=8) + T(24, y0 + 15, "CLOSE-UP  ·  " + title.upper(), 9, TERRA, 700, extra='letter-spacing="1"')
            + f'<g transform="translate(0,{y0 + 30})">{body}</g>')
def row(y, txt, right="", c=INK, x=28, size=11): return T(x, y, txt, size, c, 600) + (T(424, y, right, 9.5, MUTE, 500, "end") if right else "")
def box(x, y, w, h, fill=WHITE, stroke=LINE, rx=4): return R(x, y, w, h, fill, stroke, rx)
def cap(y, s): return T(28, y, s, 9, MUTE, 500)

# ---------- shared base scenes (decided state) ----------
MEMS = [("Avery", "M-1042", "Plus", "Active"), ("Blake", "M-1043", "Plus", "Active"), ("Casey", "M-1051", "Plus", "Paused"), ("Devon", "M-1060", "Core", "New"), ("Emery", "M-1064", "Core", "Overdue")]
STC = {"Active": JUNGLE, "Paused": MUTE, "New": LAGOON, "Overdue": TERRA}
def mem_base():
    g, y = mini_header("Members Command Center"); s, h = mini_folds(y, [("Emergency Alerts", 0, False), ("To-Do List", 2, False), ("Documents Center", 3, False)]); g += s; y += h
    g += R(14, y, 250, 20, WHITE, LINE, 4) + T(22, y + 14, "Search name or member ID", 9, MUTE)
    x = 272
    for i, p in enumerate(("All", "Core", "Plus", "Premier")): c, w = chip(x, y + 1, p, LAGOON if i == 0 else MUTE, "soft", 8); g += c; x += w + 4
    y += 26; g += "".join(T(18 + i * 16, y + 10, ch, 9, INK if ch != "C" else LAGOON, 600) for i, ch in enumerate("ABCDEFGHIJKLM")); y += 18
    g += R(14, y, 250, 16, SOFT) + T(20, y + 11, "MEMBER", 7, MUTE, 700) + T(120, y + 11, "PLAN", 7, MUTE, 700) + T(180, y + 11, "STATUS", 7, MUTE, 700); y += 16
    g += L(14, y + 2, 264, y + 2, JUNGLE, 1.5) + T(18, y + 14, "Plus", 9.5, JUNGLE, 700); y += 18
    for i, (n, mid, p, st) in enumerate(MEMS):
        if i == 3: g += L(14, y + 2, 264, y + 2, LAGOON, 1.5) + T(18, y + 14, "Core", 9.5, LAGOON, 700); y += 18
        if i == 0: g += R(14, y, 250, 20, CREAM)
        g += T(20, y + 14, f"{n}  ·  {mid}", 9.5, INK, 600) + T(120, y + 14, p, 9, MUTE) + chip(176, y + 4, st, STC[st], "dot", 8)[0] + L(14, y + 20, 264, y + 20); y += 20
    g += R(272, 104, 166, 200, WHITE, LINE, 4) + photo(276, 108, 158, 46) + T(280, 168, "Avery  ·  M-1042", 12, INK, f="khand")
    g += T(280, 184, "Home", 9, INK, 700) + L(280, 187, 302, 187, LAGOON, 1.5) + T(312, 184, "Contact", 9, MUTE) + T(354, 184, "Membership", 9, MUTE)
    for i, (big, sm) in enumerate((("1952", "Built"), ("1,480", "Sq ft"), ("4", "Systems"))): g += R(280 + i * 52, 194, 48, 34, CREAM, LINE, 3) + T(284 + i * 52, 212, big, 11, INK, f="khand") + T(284 + i * 52, 223, sm, 7, MUTE)
    return g
def rules_base():
    g, y = mini_header("Members Command Center"); s, h = mini_folds(y, [("Emergency Alerts", 0, False), ("To-Do List", 2, False), ("Documents Center", 3, False)]); g += s; y += h + 6
    for t_ in ("Members Catalog", "Sign-ups And Renewals", "Member Messages", "Routines"): g += fold(y, t_); y += 36
    return g
def hdr_base():
    return HD.board(dict(ms=34, back="link", idc="inline", status="title", accent="tri", band=True),
                    (("alerts", {"style": "fold", "types": "tags"}), ("todo", {"style": "open", "anat": "full", "count": "sum"}), ("docs", {"style": "preview"})))
def ftr_base(): return FT.board({"layout": "table", "sched": "line"}, {"style": "list", "next": "chip"}, {"share": "none"}, ropen=True)
def tech_base(): return TC.tboard("cal", lambda y: TC.cal_grid(y, "type"))
def tools_base(): return TL.board("bag", TL.bag_techcar)
def U(base, url, cap_title, body, note): return kframe(base() + callout(cap_title, body), note, url, "TEST  ·  SAMPLE")
def S_(cap_title, body, note): return SC.frame(SC.board({"sch": {"sw": "tabs"}}) + callout(cap_title, body), note)

# ---------- small close-up drawings ----------
def trow(y, cols, xs, fill=None, edge=None, bold=False, c=INK):
    g = (R(28, y - 13, 396, 20, fill) if fill else "") + (R(28, y - 13, 3, 20, edge) if edge else "")
    return g + "".join(T(x, y, s, 10, c, 600 if (bold or i == 0) else 400) for i, (x, s) in enumerate(zip(xs, cols))) + L(28, y + 7, 424, y + 7)
def mrows(y, hover=None, flag=None, sort=None):
    xs = (40, 200, 300); g = R(28, y - 13, 396, 18, SOFT) + "".join(T(x, y, s, 8, MUTE, 700, extra='letter-spacing=".8"') for x, s in zip(xs, ("MEMBER", "PLAN", "STATUS")))
    if sort == "headers": g += T(92, y, "▲", 8, LAGOON, 700)
    y += 22
    for i, (n, mid, p, st) in enumerate(MEMS[:4]):
        f = CREAM if (i == 1 and hover == "cream") else None; e = TERRA if (i == 1 and hover == "edge") else None
        g += trow(y, (f"{n}  ·  {mid}", p, ""), xs, f, e) + chip(296, y - 11, st, STC[st], "dot", 9)[0]
        if flag and i in (0, 2):
            g += (C(190, y - 4, 4, TERRA) if flag == "dot" else chip(160, y - 12, "2 open", TERRA, "soft", 8)[0])
        y += 22
    return g
def two(a, b, la, lb):
    """Two little before/after frames side by side inside the close-up."""
    return box(28, 0, 190, 150) + a + T(123, 166, la, 9, MUTE, 600, "middle") + box(234, 0, 190, 150) + b + T(329, 166, lb, 9, MUTE, 600, "middle")
def lines(x, y, n, w=150, c="#D9D1C3", gap=12): return "".join(L(x, y + i * gap, x + w - (i % 3) * 20, y + i * gap, c, 3) for i in range(n))
def blocks(x, y, n, cap=4, full=TERRA, w=14):
    return "".join(R(x + i * (w + 3), y, w, 8, (full if n >= cap else JUNGLE) if i < n else "#E2DACB", rx=1.5) for i in range(cap))

# ===== 1. Member Catalog Polish =====
def T_MEM():
    pairs, P = make("mempol19_", "UpKeep"); LOC = "Members Catalog"
    F = lambda cap_, body, note: U(mem_base, "members board", cap_, body, note)
    P("Table", LOC, "Selected row", "when you click a member and the panel opens, should the row show a soft cream fill or a terracotta edge?",
      o("cream", "Soft Cream Fill", "The open member's row turns warm cream.", "calm", F("Selected row", mrows(14, "cream"), "Cream fill")),
      o("edge", "Terracotta Left Edge", "A thin terracotta bar marks the open row.", "clear", F("Selected row", mrows(14, "edge"), "Terracotta edge")))
    P("Table", LOC, "Sorting", "should you sort the table by clicking the column headers or with one Sort menu button?",
      o("head", "Click Column Headers", "Click Member, Plan or Status to sort.", "quick", F("Sorting", mrows(14, sort="headers"), "Header sort")),
      o("menu", "Sort Menu Button", "One Sort button with A to Z, plan, status.", "tidy", F("Sorting", mrows(14) + R(330, 110, 94, 20, WHITE, INK, 0, 1.2) + T(377, 124, "Sort: A to Z", 9.5, INK, 600, "middle"), "Sort menu")))
    P("Table", LOC, "Open-item flag look", "since rows flag open items, should the flag be a small terracotta dot or a count chip?",
      o("dot", "Small Terracotta Dot", "A dot beside the name, details in the panel.", "quiet", F("Open-item flag", mrows(14, flag="dot"), "Dot flag")),
      o("chip", "Count Chip", "2 open in a soft terracotta chip.", "informative", F("Open-item flag", mrows(14, flag="chip"), "Count chip")))
    P("Plan groups", LOC, "Plan group count", "should each thin plan rule show how many members are in the group?",
      o("count", "Count Beside Plan", "Plus (24) on the coloured rule.", "informative", F("Plan group rule", L(28, 20, 424, 20, JUNGLE, 2) + T(32, 40, "Plus", 13, JUNGLE, f="khand") + T(64, 40, "(24 SAMPLE)", 9.5, MUTE, 500) + mrows(70)[:0] + lines(32, 64, 5, 380), "With count")),
      o("plain", "Plan Name Only", "Just Plus on the coloured rule.", "calm", F("Plan group rule", L(28, 20, 424, 20, JUNGLE, 2) + T(32, 40, "Plus", 13, JUNGLE, f="khand") + lines(32, 64, 5, 380), "Name only")))
    P("Jump bar", LOC, "Active letter", "on the plain-letter jump bar, should the current letter be terracotta or underlined?",
      o("terra", "Terracotta Letter", "The letter you are on turns terracotta.", "warm", F("Jump bar", "".join(T(40 + i * 28, 40, ch, 15, TERRA if ch == "C" else INK, 700) for i, ch in enumerate("ABCDEFGHIJKLM")), "Terracotta letter")),
      o("under", "Underlined Letter", "The current letter gets a lagoon underline.", "quiet", F("Jump bar", "".join(T(40 + i * 28, 40, ch, 15, INK, 700) for i, ch in enumerate("ABCDEFGHIJKLM")) + L(94, 46, 106, 46, LAGOON, 2.5), "Underline")))
    P("Finding a member", LOC, "No results", "when a search or plan chip finds nobody, should the table show one quiet line or a Clear filters button?",
      o("quiet", "One Quiet Line", "No members match, in grey.", "calm", F("No results", T(226, 70, "No members match this search.", 12, MUTE, 500, "middle"), "Quiet line")),
      o("clear", "Line Plus Clear Filters", "Adds a Clear filters button under the line.", "helpful", F("No results", T(226, 60, "No members match this search.", 12, MUTE, 500, "middle") + R(176, 76, 100, 24, WHITE, LAGOON, 3, 1.2) + T(226, 92, "Clear filters", 10, LAGOON, 600, "middle"), "Clear filters")))
    tiles = lambda style: "".join((R(40 + i * 128, 10, 116, 70, CREAM, LINE, 4) + (T(52 + i * 128, 46, big, 24, INK, f="khand") + T(52 + i * 128, 66, sm, 10, MUTE) if style == "big"
               else C(60 + i * 128, 45, 11, LAGOON + "1F", LAGOON) + T(80 + i * 128, 44, big, 16, INK, f="khand") + T(80 + i * 128, 60, sm, 9.5, MUTE)))
               for i, (big, sm) in enumerate((("1952", "Built"), ("1,480", "Sq ft"), ("4", "Systems"))))
    P("Home tab", LOC, "Number tile style", "should the Built, Sq Ft and Systems tiles be a big number over a label or an icon beside the number?",
      o("big", "Big Number Over Label", "Large Khand number, small label under.", "bold", F("Home tiles", tiles("big"), "Big number")),
      o("icon", "Icon, Number, Label", "A small round icon leads each tile.", "friendly", F("Home tiles", tiles("icon"), "Icon tiles")))
    P("Home tab", LOC, "Photo strip", "under the tiles, should home photos be a strip of three thumbnails or one photo with a count?",
      o("three", "Three Thumbnails", "Three small photos in a row.", "visual", F("Photo strip", photo(40, 10, 120, 80) + photo(166, 10, 120, 80) + photo(292, 10, 120, 80), "Three thumbs")),
      o("one", "One Photo And Count", "One photo with +6 photos in the corner.", "calm", F("Photo strip", photo(40, 10, 200, 110) + chip(180, 96, "+6 photos", INK, "solid", 8.5)[0], "One photo")))
    P("Visits", LOC, "Visit row", "in the simple visit list, should each row show date and tech or add a short note line?",
      o("dt", "Date And Tech", "Oct 12  ·  Tech Dash 2  ·  Done.", "tidy", F("Visit list", "".join(row(24 + i * 26, d, "Tech Dash " + t) + L(28, 32 + i * 26, 424, 32 + i * 26) for i, (d, t) in enumerate((("Oct 12  ·  Fall check", "2"), ("Sep 3  ·  Gutter clean", "1"), ("Jul 20  ·  Summer check", "3")))), "Date and tech")),
      o("dtn", "Date, Tech And Note", "Adds a one-line note from the tech.", "detailed", F("Visit list", "".join(row(24 + i * 40, d, "Tech Dash " + t) + T(28, 38 + i * 40, n, 9, MUTE) + L(28, 46 + i * 40, 424, 46 + i * 40) for i, (d, t, n) in enumerate((("Oct 12  ·  Fall check", "2", "Filter swapped, TEST note"), ("Sep 3  ·  Gutter clean", "1", "Downspout loose, TEST note"), ("Jul 20  ·  Summer check", "3", "All good, TEST note")))), "With note")))
    P("Member panel", LOC, "Closing the panel", "should the member panel close with an X at the top right or a Back to list link?",
      o("x", "X At Top Right", "A small X closes the panel.", "familiar", F("Panel close", box(200, 4, 224, 120) + T(212, 30, "Avery  ·  M-1042", 14, INK, f="khand") + f'<path d="M404 18 l10 10 M414 18 l-10 10" stroke="{INK}" stroke-width="1.8"/>' + lines(212, 56, 4, 190), "X close")),
      o("back", "Back To List Link", "A lagoon link at the top left of the panel.", "clear", F("Panel close", box(200, 4, 224, 120) + T(212, 22, "< Back to list", 9.5, LAGOON, 600) + T(212, 42, "Avery  ·  M-1042", 14, INK, f="khand") + lines(212, 66, 4, 190), "Back link")))
    return pairs

# ===== 2. Board Rules Fine Tuning =====
def T_RULES():
    pairs, P = make("rulesft19_", "UpKeep"); LOC = "All UpKeep Boards"
    F = lambda cap_, body, note: U(rules_base, "members board", cap_, body, note)
    def kfold(y, title, chev_left=False, open_=False):
        g = R(28, y, 396, 26, CREAM, LINE) + (chev(44, y + 13, INK, not open_) + T(58, y + 18, title, 13, INK, f="khand") if chev_left else T(40, y + 18, title, 13, INK, f="khand") + chev(408, y + 13, INK, not open_))
        return g
    P("Folds", LOC, "Chevron side", "now every fold uses the kit row, should the chevron sit at the right end or before the title?",
      o("right", "Chevron On The Right", "Title left, chevron at the far right.", "familiar", F("Fold chevron", kfold(10, "Members Catalog") + kfold(46, "Member Messages"), "Right chevron")),
      o("left", "Chevron Before Title", "Chevron leads, title follows.", "scannable", F("Fold chevron", kfold(10, "Members Catalog", True) + kfold(46, "Member Messages", True), "Left chevron")))
    P("Folds", LOC, "Fold opening", "should a fold slide open quickly or snap open instantly?",
      o("slide", "Quick Slide Open", "A short soft slide, about a fifth of a second.", "smooth", F("Fold opening", kfold(10, "Members Catalog", open_=True) + R(28, 36, 396, 60, WHITE, LINE) + lines(40, 52, 4, 300) + T(226, 120, "slides down", 9, LAGOON, 600, "middle"), "Slide")),
      o("snap", "Instant Open", "Content appears at once, no motion.", "quick", F("Fold opening", kfold(10, "Members Catalog", open_=True) + R(28, 36, 396, 60, WHITE, LINE) + lines(40, 52, 4, 300) + T(226, 120, "appears at once", 9, MUTE, 600, "middle"), "Instant")))
    P("Surfaces", LOC, "Beige border weight", "with flat cards and the beige kit border, should the border be a hairline or a touch heavier?",
      o("hair", "Hairline Beige", "A single thin beige line.", "light", F("Card border", R(40, 10, 170, 110, WHITE, LINE, 0, .8) + lines(54, 34, 5, 140) + R(240, 10, 170, 110, WHITE, LINE, 0, .8) + lines(254, 34, 5, 140), "Hairline")),
      o("firm", "Firmer Beige", "A slightly heavier beige line.", "defined", F("Card border", R(40, 10, 170, 110, WHITE, "#CFC3AE", 0, 2) + lines(54, 34, 5, 140) + R(240, 10, 170, 110, WHITE, "#CFC3AE", 0, 2) + lines(254, 34, 5, 140), "Firmer")))
    P("Type", LOC, "Section heading case", "on the four type steps, should section headings be normal case Khand or small tracked capitals?",
      o("norm", "Normal Case Khand", "Members Catalog in bold Khand.", "friendly", F("Section heading", T(40, 36, "Members Catalog", 22, INK, f="khand") + lines(40, 64, 4, 360), "Normal case")),
      o("caps", "Small Tracked Capitals", "MEMBERS CATALOG, small and spaced.", "formal", F("Section heading", T(40, 34, "MEMBERS CATALOG", 13, INK, f="khand", extra='letter-spacing="2.5"') + lines(40, 64, 4, 360), "Capitals")))
    P("Type", LOC, "Body text size", "should Hind body text sit at the comfortable step or the compact step?",
      o("comf", "Comfortable Body", "Larger Hind lines, more air.", "easy", F("Body text", "".join(T(40, 30 + i * 22, "Renewal reminder sent to SAMPLE member", 14, INK) for i in range(5)), "Comfortable")),
      o("comp", "Compact Body", "Smaller Hind lines, more on screen.", "dense", F("Body text", "".join(T(40, 26 + i * 16, "Renewal reminder sent to SAMPLE member", 11, INK) for i in range(8)), "Compact")))
    P("Sticky bar", LOC, "Slim bar contents", "with one kit bar only, should the bar that stays while you scroll show title and share or only the title?",
      o("both", "Title And Share", "Mark, board title and the share icon.", "handy", F("Sticky bar", R(28, 10, 396, 34, WHITE, LINE) + mark(36, 15, 24, False) + T(66, 33, "Members Command Center", 14, INK, f="khand") + R(392, 15, 24, 24, WHITE, INK, 0, 1.2) + share_ic(392, 15) + lines(40, 70, 5, 360), "Title and share")),
      o("title", "Title Only", "Mark and title, nothing else.", "quiet", F("Sticky bar", R(28, 10, 396, 34, WHITE, LINE) + mark(36, 15, 24, False) + T(66, 33, "Members Command Center", 14, INK, f="khand") + lines(40, 70, 5, 360), "Title only")))
    P("Empty states", LOC, "Helpful line wording", "should the one helpful empty line say who fills it or when it fills?",
      o("who", "Says Who Fills It", "The Members Agent adds renewals here.", "clear", F("Empty line", fold(0, "Sign-ups And Renewals", 0, True, 30, x=28, w=396)[:0] + kfold(10, "Sign-ups And Renewals", open_=True) + T(40, 60, "The Members Agent adds renewals here.", 11, MUTE), "Who")),
      o("when", "Says When It Fills", "Renewals show up once the first plan renews.", "expectant", F("Empty line", kfold(10, "Sign-ups And Renewals", open_=True) + T(40, 60, "Renewals show up once the first plan renews.", 11, MUTE), "When")))
    P("Colour", LOC, "Accent use", "should terracotta, lagoon and jungle appear only on status and alerts or also as a thin edge on cards?",
      o("status", "Status And Alerts Only", "Cards stay neutral, colour means something.", "calm", F("Accent use", R(40, 10, 170, 90, WHITE, LINE) + chip(52, 22, "Active", JUNGLE, "dot", 9)[0] + lines(52, 56, 3, 140) + R(240, 10, 170, 90, WHITE, LINE) + chip(252, 22, "Overdue", TERRA, "dot", 9)[0] + lines(252, 56, 3, 140), "Status only")),
      o("edge", "Plus A Card Edge", "Each card gets a thin coloured left edge.", "lively", F("Accent use", R(40, 10, 170, 90, WHITE, LINE) + R(40, 10, 3, 90, JUNGLE) + chip(52, 22, "Active", JUNGLE, "dot", 9)[0] + lines(52, 56, 3, 140) + R(240, 10, 170, 90, WHITE, LINE) + R(240, 10, 3, 90, LAGOON) + chip(252, 22, "Overdue", TERRA, "dot", 9)[0] + lines(252, 56, 3, 140), "Card edge")))
    P("Type", LOC, "Numbers", "should counts and totals use Khand numerals or Hind numerals?",
      o("khand", "Khand Numerals", "Tall, bold, branded numbers.", "bold", F("Numbers", "".join(T(60 + i * 120, 60, n, 34, INK, f="khand") + T(60 + i * 120, 82, l, 10, MUTE) for i, (n, l) in enumerate((("24", "Members"), ("3", "Renewals"), ("2", "Open"))) ), "Khand")),
      o("hind", "Hind Numerals", "Rounder numbers that match body text.", "soft", F("Numbers", "".join(T(60 + i * 120, 60, n, 30, INK, 600) + T(60 + i * 120, 82, l, 10, MUTE) for i, (n, l) in enumerate((("24", "Members"), ("3", "Renewals"), ("2", "Open"))) ), "Hind")))
    P("Spacing", LOC, "Section spacing", "between middle sections, should the gap match the header folds or be a bit larger?",
      o("same", "Same As Header Folds", "One even rhythm down the board.", "even", F("Section spacing", kfold(6, "Members Catalog") + kfold(42, "Sign-ups And Renewals") + kfold(78, "Member Messages") + kfold(114, "Routines"), "Even gaps")),
      o("big", "A Bit Larger", "More air between middle sections.", "airy", F("Section spacing", kfold(6, "Members Catalog") + kfold(56, "Sign-ups And Renewals") + kfold(106, "Member Messages"), "Larger gaps")))
    return pairs

# ===== 3. Scheduling Board Details =====
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri")
def wk(chipc="type", full=TERRA, today=None, split=None):
    g = ""
    for i, d in enumerate(DAYS):
        x = 28 + i * 80
        if today == "col" and i == 2: g += R(x, 0, 76, 150, CREAM)
        g += T(x + 6, 14, d, 10, INK, 700) + blocks(x + 6, 20, (2, 3, 4, 1, 3)[i], 4, full, 14)
        for k in range((2, 3, 4, 1, 3)[i]):
            c = (TERRA, LAGOON, JUNGLE)[k % 3] if chipc == "tech" else (LAGOON, JUNGLE, SAFF)[(i + k) % 3]
            g += R(x + 4, 36 + k * 26, 70, 22, WHITE, LINE, 3) + R(x + 4, 36 + k * 26, 3, 22, c) + T(x + 11, 51 + k * 26, f"M-10{40+i*3+k}", 8.5, INK, 600)
        if split == "halves": g += L(x + 2, 88, x + 76, 88, "#B9AE9C", 1, 'stroke-dasharray="2 2"')
    if today == "line": g += L(188, 0, 188, 150, TERRA, 2)
    if split == "hours": g += "".join(L(28, 36 + j * 13, 424, 36 + j * 13, "#EEE7DB") for j in range(9))
    return g
def T_SCHED2():
    pairs, P = make("schedd19_", "UpKeep"); LOC = "Scheduling Board"
    F = lambda cap_, body, note: S_(cap_, body, note)
    P("Week grid", LOC, "Visit chip edge colour", "with white chips and a coloured edge, should the edge colour show the tech or the visit type?",
      o("tech", "Colour By Tech", "Tech Dash 1-3 each get a colour.", "who", F("Chip edge", wk("tech"), "By tech")),
      o("type", "Colour By Visit Type", "Seasonal, repair and first visit colours.", "what", F("Chip edge", wk("type"), "By visit type")))
    P("Week grid", LOC, "Full day colour", "when a day hits the four-stop cap, should its four blocks turn terracotta or stay jungle green?",
      o("terra", "Terracotta When Full", "A full day stands out as at cap.", "alert", F("Fill blocks", wk(full=TERRA), "Terracotta full")),
      o("jungle", "Jungle When Full", "Full reads as a good, booked day.", "positive", F("Fill blocks", wk(full=JUNGLE), "Jungle full")))
    P("Week grid", LOC, "Today marker", "in the week grid, should today be a cream column or a thin terracotta line?",
      o("col", "Cream Column", "The whole day column turns cream.", "soft", F("Today", wk(today="col"), "Cream column")),
      o("line", "Thin Terracotta Line", "A thin line runs down today.", "crisp", F("Today", wk(today="line"), "Terracotta line")))
    P("Week grid", LOC, "Time guides", "inside each day, should the grid split morning and afternoon or show faint hour lines?",
      o("halves", "Morning And Afternoon", "One dashed line splits the day.", "simple", F("Time guides", wk(split="halves"), "Halves")),
      o("hours", "Faint Hour Lines", "Light lines for each hour.", "precise", F("Time guides", wk(split="hours"), "Hour lines")))
    trk = lambda names: "".join(C(80 + i * 140, 40, 9, JUNGLE if i < 2 else WHITE, JUNGLE, 1.5) + T(80 + i * 140, 66, n, 11, INK, 600, "middle") + (L(89 + i * 140, 40, 211 + i * 140, 40, JUNGLE if i == 0 else "#D6D0C6", 2) if i < 2 else "") for i, n in enumerate(names)) + T(28, 100, "Jordan  ·  M-1047  ·  fall visit  ·  TEST", 10, MUTE)
    P("Client Communications", LOC, "Tracker step names", "on the three-step tracker, which step names read best?",
      o("rbd", "Requested, Booked, Done", "Plain booking words.", "plain", F("Tracker", trk(("Requested", "Booked", "Done")), "Requested, Booked, Done")),
      o("acv", "Asked, Confirmed, Visited", "Member-side words.", "warm", F("Tracker", trk(("Asked", "Confirmed", "Visited")), "Asked, Confirmed, Visited")))
    col = lambda cnt: "".join(R(28 + i * 134, 0, 126, 140, CREAM, LINE, 4) + T(38 + i * 134, 20, n + (f"  ({c})" if cnt else ""), 11, INK, f="khand") + "".join(R(36 + i * 134, 30 + k * 30, 110, 24, WHITE, LINE, 3) + R(36 + i * 134, 30 + k * 30, 3, 24, (LAGOON, SAFF, TERRA)[i]) for k in range(c)) for i, (n, c) in enumerate((("New", 3), ("Booked", 2), ("Done", 1))))
    P("Client Communications", LOC, "Status column header", "on the status columns, should each header show a count?",
      o("count", "Count In Header", "New (3), Booked (2), Done (1).", "glanceable", F("Columns", col(True), "With count")),
      o("plain", "Name Only", "Just New, Booked, Done.", "calm", F("Columns", col(False), "Name only")))
    cards = lambda order: "".join(R(28 + (i % 3) * 134, (i // 3) * 74, 126, 66, WHITE, LINE, 4) + T(36 + (i % 3) * 134, 18 + (i // 3) * 74, n, 10, INK, f="khand") + lines(36 + (i % 3) * 134, 34 + (i // 3) * 74, 3, 100, gap=9) for i, n in enumerate(order))
    P("Optional cards", LOC, "Optional card order", "with all seven optional cards in, should member-facing cards lead or weather and routes lead?",
      o("mem", "Due Soon And Queue First", "Members due soon, First-Visit Queue, then the rest.", "member-first", F("Card order", cards(("Due Soon", "First-Visit Queue", "Parts Waiting", "Weather Watch", "Zone-Day Map", "Days Off")), "Members first")),
      o("wx", "Weather And Routes First", "Weather Watch, Zone-Day Map, then the rest.", "plan-first", F("Card order", cards(("Weather Watch", "Zone-Day Map", "Days Off", "Due Soon", "First-Visit Queue", "Parts Waiting")), "Weather first")))
    P("Optional cards", LOC, "Weather Watch style", "should Weather and Snow-Day Watch be a five-day strip or today big with a short list?",
      o("strip", "Five-Day Strip", "Five equal days, snow flag on the risky ones.", "complete", F("Weather Watch", "".join(R(28 + i * 80, 0, 74, 100, CREAM, LINE, 4) + T(65 + i * 80, 22, d, 10, INK, 700, "middle") + C(65 + i * 80, 50, 12, (LAGOON if i == 3 else SAFF) + "55") + T(65 + i * 80, 84, "Snow" if i == 3 else "TEST", 9, TERRA if i == 3 else MUTE, 700, "middle") for i, d in enumerate(DAYS)), "Five-day strip")),
      o("today", "Today Big Plus List", "A large today tile, four short rows beside it.", "focused", F("Weather Watch", R(28, 0, 160, 120, CREAM, LINE, 4) + T(40, 24, "Today", 14, INK, f="khand") + C(108, 70, 24, SAFF + "55") + "".join(row(20 + i * 26, d, "Snow flag" if i == 2 else "Clear  ·  TEST", x=210) for i, d in enumerate(DAYS[1:])), "Today big")))
    P("Optional cards", LOC, "Zone-Day Map look", "should zone-day routes be abstract dots and lines or a simple grid of zone blocks?",
      o("dots", "Dots And Lines", "Stops as dots joined in order, no real map.", "visual", F("Zone-Day Map", "".join(C(60 + i * 60, 60 + (i % 2) * 40, 7, (TERRA, LAGOON, JUNGLE)[i % 3]) for i in range(6)) + "".join(L(60 + i * 60, 60 + (i % 2) * 40, 120 + i * 60, 60 + ((i + 1) % 2) * 40, MUTE, 1.2) for i in range(5)) + T(28, 140, "Abstract preview  ·  TEST", 9, MUTE), "Dots and lines")),
      o("grid", "Zone Blocks Grid", "Zones as blocks shaded by visits that day.", "orderly", F("Zone-Day Map", "".join(R(40 + (i % 4) * 92, (i // 4) * 60, 86, 54, (LAGOON if i % 3 == 0 else JUNGLE) + ("55" if i % 2 else "22"), LINE, 4) + T(50 + (i % 4) * 92, 20 + (i // 4) * 60, f"Zone {chr(65+i)}", 10, INK, 600) for i in range(8)), "Zone blocks")))
    P("Optional cards", LOC, "Days off strip", "on the two-week days-off strip, should days off show as tech initials on the day or a shaded lane per tech?",
      o("ini", "Initials On The Day", "TD1 on the day that tech is off.", "compact", F("Days off", "".join(R(28 + i * 28, 20, 26, 40, CREAM, LINE, 2) + (T(41 + i * 28, 44, ("TD1", "TD3", "TD2")[i % 3], 7.5, TERRA, 700, "middle") if i in (2, 6, 11) else "") for i in range(14)), "Initials")),
      o("lane", "Shaded Lane Per Tech", "One row per tech, off days shaded.", "clear", F("Days off", "".join(T(28, 20 + r * 30, f"Tech Dash {r+1}", 9, INK, 600) + "".join(R(110 + i * 22, 8 + r * 30, 20, 18, (TERRA + "55") if (i + r * 4) % 9 == 2 else CREAM, LINE, 2) for i in range(14)) for r in range(3)), "Lanes")))
    return pairs

# ===== 4. Header Fine Tuning =====
def T_HDR():
    pairs, P = make("hdrft19_", "UpKeep"); LOC = "UpKeep Board Header"
    F = lambda cap_, body, note: U(hdr_base, "members board", cap_, body, note)
    hd = lambda ms: R(28, 0, 396, 70, CREAM) + mark(40, 35 - ms / 2, ms) + T(48 + ms, 36, "Members Command Center", 20, INK, f="khand") + T(48 + ms, 52, "Sign-ups, renewals and member messages.", 9.5, MUTE) + tri(68, 28, 424)
    P("Brand mark", LOC, "Mark size upper left", "going with your gut on upper left, should the UP mark be medium or small beside the title?",
      o("med", "Medium Mark", "About the height of title plus subtitle.", "confident", F("House mark", hd(44), "Medium mark")),
      o("small", "Small Mark", "About the height of the title only.", "quiet", F("House mark", hd(26), "Small mark")))
    dc = lambda dcol: "".join(docic(40, 8 + i * 30, LAGOON) + T(62, 20 + i * 30, n, 11, INK, 600) + R(250, 8 + i * 30, 120, 16, c + "1A", c, 8) + T(310, 20 + i * 30, s, 8.5, c, 700, "middle") for i, (n, s, c) in enumerate((("Welcome Message", "Draft", dcol), ("Welcome Flow Deck", "For approval", dcol), ("Member FAQ", "Approved", JUNGLE))))
    P("Documents Center", LOC, "Draft chip colour", "should Draft and For approval chips be terracotta or saffron, with Approved in jungle?",
      o("terra", "Terracotta Draft", "Draft and For approval in terracotta.", "firm", F("Approval chips", dc(TERRA), "Terracotta")),
      o("saff", "Saffron Draft", "Draft and For approval in saffron.", "gentle", F("Approval chips", dc(SAFF), "Saffron")))
    al = lambda extra: fold(0, "Emergency Alerts", None, True, 50, badge=2, edge=TERRA, x=28, w=396) + HD.alert_row(36, 42, HD.ALERTS[0], "tags", 380) + HD.alert_row(36, 62, HD.ALERTS[1], "tags", 380) + extra
    P("Emergency Alerts", LOC, "Self-opening motion", "when an alert comes in and the fold opens itself, should it simply stay open or pulse once to catch the eye?",
      o("stay", "Opens And Stays", "Opens quietly, no extra motion.", "calm", F("Alert opening", al(""), "Stays open")),
      o("pulse", "Opens Then Pulses Once", "One soft terracotta glow, then still.", "noticeable", F("Alert opening", al(R(24, -4, 404, 82, "none", TERRA + "66", 6, 4)), "One pulse")))
    P("Emergency Alerts", LOC, "Alert order", "with a colour tag per hazard, should alerts list newest first or most serious first?",
      o("new", "Newest First", "Latest alert on top, by time.", "simple", F("Alert order", al("") + T(36, 96, "Gas 10:15, then Flooding 9:40", 9, MUTE), "Newest first")),
      o("sev", "Most Serious First", "Gas and CO above flooding and electrical.", "safe", F("Alert order", fold(0, "Emergency Alerts", None, True, 50, badge=2, edge=TERRA, x=28, w=396) + HD.alert_row(36, 42, HD.ALERTS[3], "tags", 380) + HD.alert_row(36, 62, HD.ALERTS[0], "tags", 380) + T(36, 96, "CO and gas always lead", 9, MUTE), "Most serious first")))
    strip = lambda txt, right: fold(0, "Emergency Alerts", 0, True, 30, x=28, w=396) + R(36, 32, 380, 18, JUNGLE + "12", rx=4) + checkc(48, 41) + T(60, 45, txt, 10, JUNGLE, 700) + T(410, 45, right, 8.5, MUTE, anchor="end")
    P("Emergency Alerts", LOC, "All-clear wording", "on the green all-clear strip, should it read No active alerts with the check time or All clear today?",
      o("noact", "No Active Alerts, Checked", "No active alerts  ·  Checked 11:40 AM.", "precise", F("All-clear strip", strip("No active alerts", "Checked 11:40 AM"), "No active alerts")),
      o("clear", "All Clear Today", "All clear today, no time shown.", "friendly", F("All-clear strip", strip("All clear today", ""), "All clear")))
    td = lambda mode: fold(0, "To-Do List", None, True, 90, right="2 open  ·  1 due today", x=28, w=396) + check(40, 34) + T(58, 44, "Review welcome message draft", 10, INK, 600) + check(40, 56) + T(58, 66, "Call back SAMPLE member", 10, INK, 600) + (check(40, 78, True) + T(58, 88, "Pin the member FAQ", 10, MUTE, 500, extra='text-decoration="line-through"') if mode == "strike" else fold(100, "Done", 1, False, x=40, w=372, h=20, size=11))
    P("To-Do List", LOC, "Finished to-dos", "when a to-do is ticked, should it stay struck through and faded or move into a small Done fold?",
      o("strike", "Struck And Faded", "Stays in place, crossed out.", "visible", F("Finished to-dos", td("strike"), "Struck through")),
      o("done", "Moves To Done Fold", "Drops into a closed Done fold below.", "tidy", F("Finished to-dos", td("done"), "Done fold")))
    pv = lambda split: R(28, 0, split, 150, WHITE, LINE, 4) + lines(38, 20, 5, split - 30, gap=24) + R(34 + split, 0, 390 - split, 150, WHITE, LINE, 4) + T(44 + split, 18, "PREVIEW  ·  Welcome Message", 8.5, MUTE, 700) + lines(44 + split, 40, 7, 360 - split)
    P("Documents Center", LOC, "Preview pane width", "should the document list and preview pane split half and half or keep the list narrow?",
      o("half", "Half And Half", "List and preview the same width.", "balanced", F("Preview pane", pv(196), "Half and half")),
      o("narrow", "Narrow List, Wide Preview", "More room to read the document.", "reading", F("Preview pane", pv(130), "Wide preview")))
    P("Header", LOC, "Header when scrolling", "since only one kit bar may stick, should the cream header shrink into that slim bar or scroll away fully?",
      o("shrink", "Shrinks To Slim Bar", "Mark and title stay as one slim bar.", "anchored", F("On scroll", R(28, 0, 396, 30, CREAM) + mark(36, 4, 22) + T(64, 21, "Members Command Center", 13, INK, f="khand") + tri(30, 28, 424) + lines(40, 60, 6, 360), "Slim bar")),
      o("away", "Scrolls Away", "The page is all content once you scroll.", "roomy", F("On scroll", lines(40, 10, 10, 360), "Scrolls away")))
    P("Header", LOC, "Back link wording", "should the top-right link read Back to Command Center or UpKeep Command Center with an arrow?",
      o("back", "Back To Command Center", "Says what the link does.", "clear", F("Back link", R(28, 0, 396, 60, CREAM) + T(410, 30, "< Back to Command Center", 12, LAGOON, 600, "end"), "Back to")),
      o("name", "UpKeep Command Center", "Names the place, with a small arrow.", "branded", F("Back link", R(28, 0, 396, 60, CREAM) + T(410, 30, "UpKeep Command Center >", 12, LAGOON, 600, "end"), "Place name")))
    st = lambda w: R(28, 0, 396, 60, CREAM) + T(40, 36, "Members Command Center", 20, INK, f="khand") + chip(250, 20, w, JUNGLE, "dot", 10)[0]
    P("Header", LOC, "Status chip wording", "should the green chip by the title read Agent active or Live now?",
      o("active", "Agent Active", "Says the agent is running.", "plain", F("Status chip", st("Agent active"), "Agent active")),
      o("live", "Live Now", "Shorter, more alive.", "lively", F("Status chip", st("Live now"), "Live now")))
    return pairs

# ===== 5. Footer Fine Tuning =====
def T_FTR():
    pairs, P = make("ftrft19_", "UpKeep"); LOC = "UpKeep Board Footer"
    F = lambda cap_, body, note: U(ftr_base, "members board", cap_, body, note)
    bm = lambda withmark, hover=None: tri(10, 28, 424) + ((mark(176, 30, 22, False) if withmark else "") + T(226 + (14 if withmark else 0), 46, "Built by Machan", 11, MUTE, 500, "middle")) + (L(166 + 14, 50, 286, 50, MUTE, 1) if hover == "under" else "") + (M.mark(300, 22, 34, **mk(eyes="wink")) + T(340, 44, "hover", 8.5, TERRA, 700) if hover == "wink" else "")
    P("Footer credit", LOC, "Credit with mark", "with Built by Machan centred and no share, should the UP mark sit beside the words or the words stand alone?",
      o("mark", "Mark Beside Words", "Small UP mark, then Built by Machan.", "branded", F("Footer credit", bm(True), "With mark")),
      o("words", "Words Only", "Built by Machan in grey, centred.", "quiet", F("Footer credit", bm(False), "Words only")))
    P("Footer credit", LOC, "Hover cue", "since the credit opens the Machan story page, should hover underline it or show Machan winking beside it?",
      o("under", "Underline On Hover", "A thin underline says it is a link.", "plain", F("Hover cue", bm(False, "under"), "Underline")),
      o("wink", "Machan Winks On Hover", "Machan pops in beside it with a wink.", "playful", F("Hover cue", bm(False, "wink"), "Machan winks")))
    P("Footer credit", LOC, "Story page opening", "should the Machan story page open in the same tab or a new tab?",
      o("same", "Same Tab, Back Link", "Opens in place with a link back to the board.", "simple", F("Story page", R(100, 10, 252, 130, CREAM, LINE, 6) + T(112, 28, "< Back to Members board", 9, LAGOON, 600) + R(112, 38, 228, 80, "#2A1D15") + C(226, 78, 12, WHITE + "CC") + T(226, 132, "Machan story  ·  same tab", 9, MUTE, 600, "middle"), "Same tab")),
      o("new", "New Tab", "The board stays open behind it.", "safe", F("Story page", R(100, 10, 252, 130, CREAM, LINE, 6) + R(112, 30, 228, 80, "#2A1D15") + C(226, 70, 12, WHITE + "CC") + T(226, 132, "Machan story  ·  new tab", 9, MUTE, 600, "middle"), "New tab")))
    P("Footer finish", LOC, "Footer background", "should the footer sit on white or on the same warm cream band as the header?",
      o("white", "White", "The board ends on white.", "light", F("Footer band", bm(False), "White")),
      o("cream", "Cream Band", "A cream band that mirrors the header.", "framed", F("Footer band", R(28, 0, 396, 70, CREAM) + bm(False), "Cream band")))
    rt = lambda on_c, paused: "".join(T(36, 20 + i * 28, n, 10.5, MUTE if (not on and paused == "fade") else INK, 600) + R(300, 8 + i * 28, 30, 16, (on_c if on else "#CFC6B6"), rx=8) + C(322 if on else 308, 16 + i * 28, 6, WHITE) + L(28, 28 + i * 28, 424, 28 + i * 28) for i, (n, on) in enumerate((("Morning Report", True), ("Renewal reminders", False), ("Ping sweep", True), ("Welcome check", True))))
    P("Routines", LOC, "Switch colour", "on the on-off switch look, should on be jungle green or lagoon?",
      o("jungle", "Jungle When On", "Green means running.", "natural", F("Switch", rt(JUNGLE, "keep"), "Jungle")),
      o("lagoon", "Lagoon When On", "Blue, calmer than green.", "cool", F("Switch", rt(LAGOON, "keep"), "Lagoon")))
    P("Routines", LOC, "Paused routine look", "should a paused routine fade its whole row or keep the row and only grey the switch?",
      o("fade", "Faded Row", "Name and next run go grey.", "clear", F("Paused routine", rt(JUNGLE, "fade"), "Faded row")),
      o("keep", "Grey Switch Only", "Row stays readable, switch turns grey.", "readable", F("Paused routine", rt(JUNGLE, "keep"), "Grey switch")))
    cd = lambda txt: "".join(T(36, 20 + i * 28, n, 10.5, INK, 600) + chip(300, 6 + i * 28, txt[i], LAGOON, "soft", 8.5)[0] for i, n in enumerate(("Morning Report", "Ping sweep", "Welcome check")))
    P("Routines", LOC, "Countdown wording", "should the countdown chip read short like in 2h or full like Next in 2 hours?",
      o("short", "Short: in 2h", "in 2h, in 35m, in 1d.", "compact", F("Countdown chip", cd(("in 17h", "in 35m", "in 2h")), "Short")),
      o("full", "Full: Next In 2 Hours", "Next in 17 hours, and so on.", "clear", F("Countdown chip", cd(("Next in 17 hours", "Next in 35 min", "Next in 2 hours")), "Full")))
    tm = lambda mode: "".join(T(36, 20 + i * 26, ("11:42 AM", "10:15 AM", "9:02 AM")[i], 10, INK, 600) + (T(100, 20 + i * 26, ("18 min ago", "2 hr ago", "3 hr ago")[i], 9, MUTE) if mode == "both" else "") + T(190, 20 + i * 26, ("SAMPLE Member A", "Tech Dash 2", "Members Agent")[i], 10, INK) + L(28, 28 + i * 26, 424, 28 + i * 26) for i in range(3)) + (R(30, 30, 90, 20, INK, rx=3) + T(75, 44, "18 min ago", 9, WHITE, 600, "middle") if mode == "hover" else "")
    P("Ping Record", LOC, "Received time combo", "since you liked both clock time and how long ago, should both show or should ago appear on hover?",
      o("both", "Clock Plus Ago", "11:42 AM  ·  18 min ago, always.", "complete", F("Received time", tm("both"), "Both shown")),
      o("hover", "Ago On Hover", "Clock time shown, how long ago on hover.", "clean", F("Received time", tm("hover"), "On hover")))
    dd = lambda items: "".join(R(28 + i * 130, 10, 122, 24, WHITE, INK, 0, 1.2) + T(38 + i * 130, 26, s, 10, INK, 600) + chev(136 + i * 130, 22, INK) for i, s in enumerate(items))
    P("Ping Record", LOC, "Filter menus", "should the dropdown filters be Type and Status only or add a Date menu?",
      o("two", "Type And Status", "Two small menus.", "simple", F("Filters", dd(("Type: All", "Status: All")), "Two menus")),
      o("three", "Type, Status, Date", "Adds a Date menu: today, week, month.", "thorough", F("Filters", dd(("Type: All", "Status: All", "Date: Week")), "Three menus")))
    P("Ping Record", LOC, "Ping schedule line", "should the one-line ping schedule sit above the table or on the fold title row?",
      o("above", "Above The Table", "Its own grey line inside the fold.", "readable", F("Ping schedule", fold(0, "Ping Record", None, True, 60, right="4 active  ·  1 paused", x=28, w=396) + T(36, 42, "Pings checked every 30 min  ·  SAMPLE", 9.5, MUTE) + lines(36, 62, 2, 360), "Above table")),
      o("title", "On The Fold Title Row", "Saves a line, sits right of the title.", "compact", F("Ping schedule", fold(0, "Ping Record", None, True, 60, right="Every 30 min  ·  SAMPLE", x=28, w=396) + lines(36, 44, 3, 360), "Title row")))
    return pairs

# ===== 6. Technicians Board Details =====
TCOL = (TERRA, LAGOON, JUNGLE)
def T_TECH2():
    pairs, P = make("techd19_", "UpKeep"); LOC = "Technicians Board"
    F = lambda cap_, body, note: U(tech_base, "technicians board", cap_, body, note)
    mon = lambda by: "".join(R(28 + (i % 7) * 56, (i // 7) * 36, 52, 32, CREAM, LINE, 2) + T(32 + (i % 7) * 56, 11 + (i // 7) * 36, str(i + 1), 8, MUTE) + "".join(C(38 + (i % 7) * 56 + k * 9, 22 + (i // 7) * 36, 3, (TCOL[k] if by == "tech" else (LAGOON, JUNGLE, SAFF)[(i + k) % 3])) for k in range((i * 7) % 4)) for i in range(28))
    P("Calendar", LOC, "Month dot colour", "with week visits coloured by visit type, should month-view dots also use visit type or switch to tech colours?",
      o("type", "Dots By Visit Type", "Same colours as the week view.", "consistent", F("Month dots", mon("type"), "By visit type")),
      o("tech", "Dots By Tech", "Month shows who is busy instead.", "who", F("Month dots", mon("tech"), "By tech")))
    lg = "".join(R(40 + i * 120, 10, 10, 10, c, rx=2) + T(56 + i * 120, 19, n, 10, INK, 600) for i, (n, c) in enumerate((("Seasonal", LAGOON), ("Repair", SAFF), ("First visit", JUNGLE))))
    P("Calendar", LOC, "Visit type legend", "should the visit-type colour key sit above the grid or show only when you hover a visit?",
      o("above", "Legend Above Grid", "Always visible colour key.", "clear", F("Legend", lg + lines(40, 50, 6, 360), "Above grid")),
      o("hover", "Legend On Hover", "Hover a visit to see its type.", "clean", F("Legend", lines(40, 20, 6, 360) + R(200, 60, 120, 26, INK, rx=4) + T(260, 77, "Repair visit", 10, WHITE, 600, "middle"), "On hover")))
    ros = lambda mode, today=None: "".join(T(36, 40 + r * 26, f"Tech Dash {r+1}", 10, INK, 600) for r in range(3)) + "".join((R(120 + i * 60, 10, 56, 106, CREAM) if (today == "col" and i == 2) else "") + T(148 + i * 60, 22, d, 10, INK, 800 if (today == "bold" and i == 2) else 600, "middle") + "".join(T(148 + i * 60, 40 + r * 26, (("8-4", "9-5", "Off")[(i + r) % 3] if mode == "hours" else ("Work", "Work", "Off")[(i + r) % 3]), 9.5, TERRA if (i + r) % 3 == 2 else MUTE, 600, "middle") for r in range(3)) for i, d in enumerate(DAYS))
    P("Who is working", LOC, "Roster cell", "in the roster table, should each day cell show shift hours or just Work or Off?",
      o("hours", "Shift Hours", "8-4, 9-5 or Off.", "detailed", F("Roster", ros("hours"), "Hours")),
      o("word", "Work Or Off", "One word per day.", "simple", F("Roster", ros("word"), "Words")))
    P("Who is working", LOC, "Today in the roster", "should today's column be a cream column or only a bold day name?",
      o("col", "Cream Column", "The whole day is tinted.", "visible", F("Today", ros("word", "col"), "Cream column")),
      o("bold", "Bold Day Name", "Just the header goes bold.", "quiet", F("Today", ros("word", "bold"), "Bold name")))
    P("Pinned hazards", LOC, "No hazards state", "when nothing is flagged, should the pinned hazard banner hide or show a green all-clear line?",
      o("hide", "Banner Hides", "Nothing pinned, the calendar moves up.", "clean", F("No hazards", lines(40, 20, 6, 360), "Hidden")),
      o("clear", "Green All-Clear Line", "Gas, electrical, CO, flooding: all clear.", "reassuring", F("No hazards", R(28, 0, 396, 22, JUNGLE + "12", rx=4) + checkc(40, 11) + T(54, 15, "All clear  ·  gas, electrical, CO, flooding", 10, JUNGLE, 700) + lines(40, 50, 5, 360), "All clear")))
    th = lambda cap_: "".join(photo(28 + (i % 5) * 80, (i // 5) * 74, 74, 52) + (T(28 + (i % 5) * 80, 62 + (i // 5) * 74, f"Oct {19-i}  ·  TD{i%3+1}", 7.5, MUTE) if cap_ else "") for i in range(10))
    P("Visit photos", LOC, "Thumbnail caption", "in the thumbnail grid, should each photo carry date and tech underneath or show no caption?",
      o("cap", "Date And Tech Under", "Oct 18  ·  TD2 under each photo.", "informative", F("Thumbnails", th(True), "Captions")),
      o("none", "No Caption", "Just photos, details on click.", "clean", F("Thumbnails", th(False), "No captions")))
    P("Visit photos", LOC, "Opening a thumbnail", "when you click a thumbnail, should it open large in a lightbox or open the visit note beside the grid?",
      o("light", "Large Lightbox", "The photo fills the screen.", "visual", F("Open photo", R(28, 0, 396, 150, "#2A1D15CC", rx=4) + photo(100, 14, 252, 120), "Lightbox")),
      o("note", "Visit Note Beside", "Photo plus the tech's note on the right.", "useful", F("Open photo", photo(28, 0, 200, 140) + T(240, 18, "Fall check  ·  M-1042", 11, INK, f="khand") + T(240, 34, "Tech Dash 2  ·  Oct 18", 9, MUTE) + lines(240, 54, 5, 180), "Note beside")))
    fs = lambda mode: "".join(fold(i * 30, n, None, False, right=(c if mode == "count" else nx), rcol=INK, x=28, w=396) for i, (n, c, nx) in enumerate((("Company Calendar", "14 visits this week", "Next: M-1042, 9 AM"), ("Who's Working", "3 of 3 on", "Next off: Tech Dash 3, Fri"), ("Visits Log", "12 this week", "Latest: M-1051, 10:15"))))
    P("Sections", LOC, "Closed fold summary", "on the closed folds, should the one-line summary be a count or a next-up line?",
      o("count", "Counts", "14 visits this week.", "glanceable", F("Fold summary", fs("count"), "Counts")),
      o("next", "Next-Up Line", "Next: M-1042, 9 AM.", "actionable", F("Fold summary", fs("next"), "Next up")))
    P("View switcher", LOC, "Switcher position", "you left the switcher to us, so should the one Day, Week, Month control sit top right or on its own row under the header?",
      o("right", "Top Right Of Board", "Shares the line with the week label.", "compact", F("Switcher", T(36, 20, "Week of Oct 19", 11, INK, 600) + TC.seg(272, 6, "Week") + lines(40, 50, 5, 360), "Top right")),
      o("row", "Own Row Under Header", "A full-width row, centred control.", "prominent", F("Switcher", TC.seg(150, 4, "Week") + L(28, 34, 424, 34) + lines(40, 56, 5, 360), "Own row")))
    bc = lambda mode: "".join(R(28 + i * 134, 0, 126, 96, WHITE, LINE, 6) + T(38 + i * 134, 20, f"Tech Dash {i+1}", 11, INK, f="khand") + T(38 + i * 134, 40, "EPA cert  ·  SAMPLE", 9, MUTE) + ((chip(38 + i * 134, 54, "Due Nov 2" if i == 1 else "OK", TERRA if i == 1 else JUNGLE, "soft", 8.5)[0]) if mode == "terra" else chip(38 + i * 134, 54, ("in 6 mo", "in 14 days", "in 9 mo")[i], TERRA if i == 1 else LAGOON, "soft", 8.5)[0]) for i in range(3))
    P("Optional certifications", LOC, "Renewal warning", "if the optional badge cards are added, should a due renewal show a terracotta due chip or a countdown chip?",
      o("terra", "Terracotta Due Chip", "Due Nov 2 in terracotta.", "alert", F("Badge cards  ·  Optional", bc("terra"), "Due chip")),
      o("count", "Countdown Chip", "in 14 days, terracotta when close.", "forward", F("Badge cards  ·  Optional", bc("count"), "Countdown")))
    return pairs

# ===== 7. Tools And Equipment Details =====
def T_TOOLS2():
    pairs, P = make("toold19_", "UpKeep"); LOC = "Tools And Equipment Board"
    F = lambda cap_, body, note: U(tools_base, "tools-equipment board", cap_, body, note)
    names = ("Hand tools", "Meters", "Safety gear", "Ladders", "Sealants", "Filters")
    grid = lambda style, n=4: "".join(R(28 + (i % n) * (396 / n), (i // n) * 76, 396 / n - 6, 70, WHITE, LINE, 4) + ((photo(32 + (i % n) * (396 / n), 4 + (i // n) * 76, 396 / n - 14, 42) + T(32 + (i % n) * (396 / n), 62 + (i // n) * 76, names[i % 6], 9, INK, 600)) if style == "photo" else (C(48 + (i % n) * (396 / n), 24 + (i // n) * 76, 11, LAGOON + "1F", LAGOON) + T(32 + (i % n) * (396 / n), 52 + (i // n) * 76, names[i % 6], 9, INK, 600) + T(32 + (i % n) * (396 / n), 64 + (i // n) * 76, f"{3+i} items", 8, MUTE))) for i in range(2 * n))
    P("Laptop grid", LOC, "Thumbnail tile", "on the laptop thumbnail grid, should each tile be a photo with a name or an icon with name and item count?",
      o("photo", "Photo With Name", "A small photo of the kit, name under.", "visual", F("Thumbnail tile", grid("photo"), "Photo tiles")),
      o("icon", "Icon, Name, Count", "Simple icon, name and item count.", "tidy", F("Thumbnail tile", grid("icon"), "Icon tiles")))
    P("Laptop grid", LOC, "Grid density", "on the big screen, should the grid run four tiles across or six?",
      o("four", "Four Across", "Bigger tiles, easy to read.", "roomy", F("Grid density", grid("icon", 4), "Four across")),
      o("six", "Six Across", "More at a glance.", "dense", F("Grid density", grid("icon", 6), "Six across")))
    car = lambda peek: R(120, 0, 212, 150, WHITE, INK, 14, 1.2) + R(132, 14, (210 if peek else 188), 96, WHITE, LINE, 6)[:0] + R(132, 14, 150, 96, WHITE, LINE, 6) + T(142, 36, "Tech Dash 1", 12, INK, f="khand") + lines(142, 52, 3, 120, gap=12) + (R(290, 14, 38, 96, WHITE, LINE, 6) if peek else "") + "".join(C(206 + i * 12, 126, 3, TERRA if i == 0 else "#D6D0C6") for i in range(3))
    P("Phone carousel", LOC, "Carousel hint", "on the phone carousel, should the next card peek in from the edge or rely on the dots?",
      o("peek", "Next Card Peeks", "A slice of the next tech's card shows.", "inviting", F("Phone carousel", car(True), "Peek")),
      o("dots", "Dots Only", "One full card, dots underneath.", "clean", F("Phone carousel", car(False), "Dots only")))
    bars = lambda c: "".join(T(36, 20 + i * 28, n, 10, INK, 600) + R(150, 10 + i * 28, 240, 10, "#EEE7DB", rx=5) + R(150, 10 + i * 28, 240 * v, 10, (c if v < .3 else JUNGLE), rx=5) + L(150 + 240 * .3, 6 + i * 28, 150 + 240 * .3, 24 + i * 28, INK, 1.5) + (warn(400, 8 + i * 28, c) if v < .3 else "") for i, (n, v) in enumerate((("Filters", .2), ("Fasteners", .7), ("Sealants and tape", .15), ("Gloves", .5))))
    P("Van stock", LOC, "Below-min bar colour", "on the bars against par, should a below-min bar turn terracotta or saffron?",
      o("terra", "Terracotta Bar", "Strong, matches the warning sign.", "urgent", F("Stock bars  ·  Van 1", bars(TERRA), "Terracotta")),
      o("saff", "Saffron Bar", "Softer, saves terracotta for safety.", "gentle", F("Stock bars  ·  Van 1", bars(SAFF), "Saffron")))
    lk = lambda txt: R(28, 0, 396, 24, TERRA + "10", TERRA, 3) + T(40, 16, "Nothing is bought without Max's approval", 10, TERRA, 700) + R(28, 34, 396, 30, WHITE, LINE) + lock(40, 40) + T(60, 54, "Filters for Van 1  ·  TEST", 10.5, INK, 600) + chip(300, 40, txt, TERRA, "outline", 9)[0]
    P("Ordering", LOC, "Locked row label", "on the locked row under the banner, should the chip read Needs Max's approval or Waiting for Max?",
      o("needs", "Needs Max's Approval", "Says exactly what has to happen.", "formal", F("Locked row", lk("Needs Max's approval"), "Needs approval")),
      o("wait", "Waiting For Max", "Shorter and friendlier.", "friendly", F("Locked row", lk("Waiting for Max"), "Waiting")))
    P("Ordering", LOC, "Approval in the header", "should each approval request also appear in the header To-Do List or live only in Ordering?",
      o("todo", "Also In Header To-Do", "Approve filters for Van 1, in the To-Do fold.", "visible", F("Approval request", fold(0, "To-Do List", None, True, 30, right="1 needs approval", x=28, w=396) + check(40, 34) + T(58, 44, "Approve filters for Van 1  ·  TEST", 10, INK, 600) + lines(40, 80, 3, 360), "In To-Do")),
      o("only", "Ordering Only", "The banner and locked row are enough.", "focused", F("Approval request", lk("Needs Max's approval") + lines(40, 90, 3, 360), "Ordering only")))
    P("Ordering", LOC, "Supplier and cost fold name", "for the one tucked-away fold, should it be titled Supplier and cost (Open) or Details for later?",
      o("sc", "Supplier And Cost, Open", "Names what is inside and that it is open.", "clear", F("Tucked fold", fold(0, "Supplier And Cost", None, False, right="Open", rcol=SAFF, x=28, w=396), "Supplier and cost")),
      o("later", "Details For Later", "Softer, says it is not decided yet.", "soft", F("Tucked fold", fold(0, "Details For Later", None, False, right="Open", rcol=SAFF, x=28, w=396), "Details for later")))
    qa = lambda top: (R(28, 0 if top else 96, 396, 24, WHITE, LAGOON, 3, 1.2) + T(38, (16 if top else 112), "+ Quick add: item, van, qty", 10, MUTE)) + "".join(row((44 if top else 16) + i * 24, f"Order {n}  ·  TEST", s) for i, (n, s) in enumerate((("filters", "Requested"), ("gloves", "Approved"), ("tape", "Ordered"))))
    P("Ordering", LOC, "Quick add placement", "should the one-line quick add sit at the top of the order list or at the bottom?",
      o("top", "Top Of List", "First thing you see in Ordering.", "handy", F("Quick add", qa(True), "Top")),
      o("bottom", "Bottom Of List", "Under the orders, like adding a row.", "natural", F("Quick add", qa(False), "Bottom")))
    rb = lambda style: "".join(T(36, 20 + i * 28, n, 10, INK, 600) + warn(200, 9 + i * 28) + T(216, 20 + i * 28, "Below min", 9, TERRA, 600) + (R(330, 7 + i * 28, 94, 20, WHITE, LAGOON, 3, 1.2) + T(377, 21 + i * 28, "Request order", 9, LAGOON, 600, "middle") if style == "btn" else T(424, 20 + i * 28, "Request order >", 9.5, LAGOON, 600, "end")) for i, n in enumerate(("Filters  ·  Van 1", "Sealants  ·  Van 2")))
    P("Van stock", LOC, "Request order look", "should the Request order on a low row be a small outlined button or a text link?",
      o("btn", "Small Outlined Button", "Clearly tappable.", "clear", F("Request order", rb("btn"), "Button")),
      o("link", "Text Link", "Quieter in a long list.", "quiet", F("Request order", rb("link"), "Link")))
    P("Ordering", LOC, "Received orders", "once an order is received, should it fold away into Received or stay in the list with a check?",
      o("fold", "Fold Into Received", "List keeps only open orders.", "tidy", F("Received", "".join(row(16 + i * 24, f"Order {n}  ·  TEST", s) for i, (n, s) in enumerate((("filters", "Requested"), ("gloves", "Ordered")))) + fold(60, "Received", 4, False, x=28, w=396), "Fold away")),
      o("stay", "Stay With A Check", "Received rows stay, ticked in green.", "complete", F("Received", "".join(row(16 + i * 24, f"Order {n}  ·  TEST", s) + (checkc(410, 12 + i * 24) if s == "Received" else "") for i, (n, s) in enumerate((("filters", "Requested"), ("gloves", "Ordered"), ("tape", "Received"), ("ladder feet", "Received")))), "Stay")))
    return pairs

# ===== 8. Machan Look Polish =====
BROWN = "#7A4A2E"; BLUSH = M.BLUSH
_g = [0]
def mlook(x, y, size, edge=BROWN, ew=.9, shade="low", hl="arc", blush=2.6, eyes="open", tiny=False):
    """Machan as decided: eyes open at rest, level leaves, peach oval blush, short stem, thin warm-brown edge with subtle shading."""
    s = M.mark(0, 0, 48, **mk(eyes=eyes, blush=True, finish="flat"))
    inner = s[s.index(">") + 1:-4]
    _g[0] += 1; gid = f"fsh{_g[0]}"
    body = '<rect x="7" y="11" width="34" height="32" rx="14" fill="' + TERRA + '"/>'
    shading = ""
    if shade == "low": shading = f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#5A2A14" stop-opacity="0"/><stop offset="1" stop-color="#5A2A14" stop-opacity=".22"/></linearGradient></defs><rect x="7" y="11" width="34" height="32" rx="14" fill="url(#{gid})"/>'
    if shade == "side": shading = f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset=".55" stop-color="#5A2A14" stop-opacity="0"/><stop offset="1" stop-color="#5A2A14" stop-opacity=".22"/></linearGradient></defs><rect x="7" y="11" width="34" height="32" rx="14" fill="url(#{gid})"/>'
    light = ('<path d="M14.5 16.6c2.4-2 5.6-3 9.5-3" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="1.6" stroke-linecap="round"/>' if hl == "arc"
             else f'<ellipse cx="16" cy="17" rx="4" ry="2.4" fill="#fff" fill-opacity=".22"/>')
    edge_svg = f'<rect x="7" y="11" width="34" height="32" rx="14" fill="none" stroke="{edge}" stroke-width="{ew}"/>' if (edge and not tiny) else ""
    inner = inner.replace(body, body + shading + light + edge_svg, 1)
    inner = inner.replace(f'<circle cx="15.2" cy="31.6" r="1.8" fill="{BLUSH}"/><circle cx="32.8" cy="31.6" r="1.8" fill="{BLUSH}"/>',
                          f'<ellipse cx="15.2" cy="31.8" rx="{blush}" ry="1.3" fill="{BLUSH}"/><ellipse cx="32.8" cy="31.8" rx="{blush}" ry="1.3" fill="{BLUSH}"/>')
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({size / 48:.4f})">{inner}</g>'
def lcard(note, label="Machan mark", extra="", **k):
    body = rect(0, 24, W, 220, M.CR) + mlook(120 - 60, 40, 120, **k) + mlook(40, 176, 40, **k) + mlook(100, 186, 24, **k) + mlook(140, 192, 16, **k) + extra
    return M.frame(body, 296, label, note)
def bounce(note, kind="hop", shadow=True):
    body = rect(0, 24, W, 220, M.CR) + rect(14, 38, 212, 190, "#FFFFFF", M.BORD, 10)
    for i, dy in enumerate((0, -22, 0)):
        x = 34 + i * 62
        if kind == "squash" and i != 1: body += f'<g transform="translate({x+24},{120}) scale(1.12,.86) translate({-x-24},{-120})">{mlook(x, 72, 48)}</g>'
        else: body += mlook(x, 72 + dy, 48)
        if shadow: body += f'<ellipse cx="{x+24}" cy="128" rx="{16 if dy else 20}" ry="3" fill="#2A1D15" fill-opacity="{.08 if dy else .14}"/>'
    body += M.T(120, 168, "Loading your visits", 9, M.LEAD, anchor="middle") + M.T(120, 184, "UpKeep loader  ·  three frames", 7.5, MUTE, anchor="middle")
    return M.frame(body, 270, "Machan loader", note)
def wink_frames(note, slow=False):
    body = rect(0, 24, W, 220, M.CR)
    fr = (("rest", "open"), ("hover", "wink")) if not slow else (("rest", "open"), ("half", "wink"), ("hover", "wink"))
    n = len(fr)
    for i, (lab, e) in enumerate(fr):
        x = 18 + i * (204 / n)
        body += rect(x, 50, 204 / n - 8, 110, "#FFFFFF", M.BORD, 8) + mlook(x + (204 / n - 8) / 2 - 24, 64, 48, eyes=e) + M.T(x + (204 / n - 8) / 2, 146, lab.upper(), 7, TERRA, w=700, anchor="middle")
    body += M.T(120, 182, "about a fifth of a second" if not slow else "slower wink, then a small smile", 8.5, M.LEAD, anchor="middle")
    return M.frame(body, 260, "Machan hover wink", note)
def upkeep_spots(note, mode):
    body = rect(0, 24, W, 220, M.CR) + rect(14, 38, 212, 196, "#FFFFFF", M.BORD, 10) + M.T(26, 58, "UpKeep board  ·  SAMPLE", 8, MUTE, w=700)
    body += rect(26, 68, 188, 30, M.CR, M.BORD, 6) + M.T(36, 87, "Loading", 8.5, M.LEAD) + mlook(170, 70, 26)
    if mode == "more": body += rect(26, 106, 188, 60, M.CR, M.BORD, 6) + mlook(36, 116, 36) + M.T(80, 132, "No visits yet", 9, M.HEAD, w=600) + M.T(80, 146, "Empty state", 7.5, MUTE)
    else: body += "".join(rect(26, 110 + i * 14, 188 - i * 30, 6, "#E9E2D6", "none", 3) for i in range(4))
    body += ln(190, 26, 214, M.BORD) + mlook(78, 198, 18) + M.T(102, 211, "Built by Machan", 8, M.GREY)
    return M.frame(body, 290, "Machan on UpKeep", note)
def T_LOOK2():
    pairs, P = make("machpol19_", "Branding"); P = M.equal(P); L = "Machan Mark Mockup"
    P("Edge", L, "Edge colour", "for the thin soft edge, should it be warm brown or a deeper terracotta?",
      o("brown", "Warm Brown Edge", "A soft brown line, reads like ink.", "warm", lambda: lcard(("Warm brown", "Subtle ink line"))),
      o("terra", "Deeper Terracotta Edge", "Tone on tone, barely there.", "subtle", lambda: lcard(("Tone on tone", "Even quieter"), edge="#9E3A1E")))
    P("Shading", L, "Shading direction", "with the edge in, should the subtle shading sit low under his belly or along one side?",
      o("low", "Soft Lower Shade", "Light from above, shade gathers low.", "grounded", lambda: lcard(("Shade low", "Feels round"))),
      o("side", "Soft Side Shade", "Light from the left, shade on the right.", "dimensional", lambda: lcard(("Shade right", "Feels turned"), shade="side")))
    P("Shading", L, "Highlight", "should the shine stay the small top arc or become a soft glow spot?",
      o("arc", "Keep The Top Arc", "The thin white arc he has now.", "familiar", lambda: lcard(("Thin arc", "As now"))),
      o("glow", "Soft Glow Spot", "A blurred oval of light, top left.", "soft", lambda: lcard(("Glow spot", "Softer shine"), hl="glow")))
    P("Edge", L, "Edge when tiny", "at 16 px, should the edge stay or drop away so he stays clean?",
      o("keep", "Edge At All Sizes", "Same line down to 16 px.", "consistent", lambda: lcard(("Edge everywhere", "One look"))),
      o("drop", "Drop Edge When Tiny", "No edge at 24 and 16 px.", "crisp", lambda: M.frame(rect(0, 24, W, 220, M.CR) + mlook(60, 40, 120) + mlook(40, 176, 40) + mlook(100, 186, 24, tiny=True) + mlook(140, 192, 16, tiny=True), 296, "Machan mark", ("Edge drops small", "Cleaner favicon"))))
    P("Blush", L, "Oval blush size", "should the peach oval blush stay small or go a little wider?",
      o("small", "Small Ovals", "Neat little ovals.", "neat", lambda: lcard(("Small ovals", "Subtle"), blush=2.2)),
      o("wide", "Wider Ovals", "A bit more rosy.", "sweet", lambda: lcard(("Wider ovals", "More kawaii"), blush=3.4)))
    P("Hover", "Machan Footer Mockup", "Wink speed", "on hover he winks, so should it be a quick wink or a slower wink with a small smile?",
      o("quick", "Quick Wink", "Blink-fast and back.", "snappy", lambda: wink_frames(("Quick wink", "Snappy"))),
      o("slow", "Slow Wink And Smile", "A beat longer, smile lifts.", "charming", lambda: wink_frames(("Slow wink", "With a smile"), True)))
    P("Loader", "Machan Loading Mockup", "Bounce style", "for the loader where Machan bounces, should it be a simple hop or a squash and stretch hop?",
      o("hop", "Simple Hop", "Up and down, no squish.", "calm", lambda: bounce(("Simple hop", "Calm"))),
      o("squash", "Squash And Stretch", "Squishes on landing, cartoon bounce.", "lively", lambda: bounce(("Squash and stretch", "Bouncy"), "squash")))
    P("Loader", "Machan Loading Mockup", "Ground shadow", "while he bounces, should a little shadow grow and shrink under him?",
      o("shadow", "Little Ground Shadow", "Sells the height of the hop.", "grounded", lambda: bounce(("With shadow", "Feels real"))),
      o("none", "No Shadow", "Just Machan, floating.", "clean", lambda: bounce(("No shadow", "Simpler"), shadow=False)))
    P("UpKeep", "Machan On UpKeep Mockup", "Where he appears", "now he is UpKeep's mascot too, should he show only in the footer and loader or also in empty states?",
      o("min", "Footer And Loader Only", "Small, rare, special.", "restrained", lambda: upkeep_spots(("Footer and loader", "Rare"), "min")),
      o("more", "Plus Empty States", "He keeps you company when lists are empty.", "friendly", lambda: upkeep_spots(("Plus empty states", "More company"), "more")))
    P("Edge", L, "Edge weight", "keeping it subtle, should the edge be hairline or a touch thicker?",
      o("hair", "Hairline Edge", "Just enough to hold the shading.", "subtle", lambda: lcard(("Hairline", "Barely there"), ew=.6)),
      o("thick", "A Touch Thicker", "Still soft, a bit more defined.", "defined", lambda: lcard(("Touch thicker", "More defined"), ew=1.3)))
    return pairs

# ===== 9. Machan Story Page =====
DUSK = "#2A1D15"
def seedg(cx, cy, k=1): return M.seed_glyph(cx, cy, k)
def scene(kind, x, y, w, h):
    g = rect(x, y, w, h, DUSK, "none", 8)
    if kind == "seed": g += f'<ellipse cx="{x+w/2}" cy="{y+h-14}" rx="{w*.4}" ry="6" fill="#4A3524"/>' + seedg(x + w / 2, y + h - 24, 1.4) + f'<path d="M{x+w/2} {y+h-34} q-4 -14 2 -22" stroke="{M.LEAF2}" stroke-width="2" fill="none"/>'
    if kind == "wink": g += mlook(x + w / 2 - 26, y + h / 2 - 28, 52, eyes="wink", edge=BROWN)
    if kind == "tiger": g += f'<path d="M{x+18} {y+h-18} q20 -34 52 -20 l10 -10 l4 14 q-30 22 -66 16z" fill="#D9772B" fill-opacity=".8"/>' + mlook(x + w - 64, y + h - 62, 44, edge=BROWN)
    if kind == "tree": g += f'<path d="M{x+w/2} {y+h-10} v-40" stroke="#8A5A3C" stroke-width="5"/><circle cx="{x+w/2}" cy="{y+h-60}" r="26" fill="{M.LEAF1}"/>' + mlook(x + w / 2 + 20, y + h - 44, 30, edge=BROWN)
    if kind == "glyph": g += M.T(x + w / 2, y + h / 2 + 18, "事事如意", 34, "#E8B04A", w=700, anchor="middle", extra='fill-opacity=".9"') + mlook(x + w / 2 - 16, y + h - 40, 32, eyes="wink", edge=BROWN)
    return g + f'<circle cx="{x+w/2}" cy="{y+h/2}" r="0" fill="none"/>'
def play(x, y): return f'<circle cx="{x}" cy="{y}" r="12" fill="#FFFFFF" fill-opacity=".85"/><path d="M{x-4} {y-6} l10 6 l-10 6z" fill="{DUSK}"/>'
def page(note, top, video, below, label="Machan story page"):
    body = rect(0, 24, W, 400, M.CR) + top + video + below
    return M.frame(body, 330, label, note)
def ptop(kind="title"):
    if kind == "title": return mlook(20, 34, 24) + M.T(50, 52, "The story of Machan", 14, M.HEAD, "khand")
    return ""
def vid(kind="wink", y=64, sound="muted", h=120, extra=""):
    g = scene(kind, 14, y, 212, h) + play(34, y + h - 20)
    if sound == "muted": g += M.T(214, y + h - 8, "CC  ·  muted", 7, "#FFFFFF", w=700, anchor="end")
    else: g += M.T(214, y + h - 8, "Tap for sound", 7, "#FFFFFF", w=700, anchor="end")
    return g + extra
def car(y, head="May all things go as you wish.", glyph=False):
    g = rect(14, y, 212, 70, "#FFFFFF", M.BORD, 10) + M.T(26, y + 18, "01 THE WISH", 7, TERRA, w=700, extra='letter-spacing="1"')
    if glyph: g += M.T(206, y + 56, "事事如意", 24, TERRA, w=700, anchor="end", extra='fill-opacity=".15"')
    return g + M.T(26, y + 38, head, 11, M.HEAD, "khand") + "".join(rect(108 + i * 10, y + 60, 6, 4, TERRA if i == 0 else "#D6D0C6", "none", 2) for i in range(6))
def T_STORY2():
    pairs, P = make("machstorypg19_", "Branding"); P = M.equal(P); L = "Machan Story Page Mockup"; V = "Machan Story Video Mockup"
    P("Video", V, "Opening shot", "the video shows his journey through life, so should it open on a seed in the soil or on Machan winking at you?",
      o("seed", "Opens On A Seed", "Starts small: the Ozark seed in dark soil.", "earnest", lambda: page(("Seed first", "Journey from the start"), ptop(), vid("seed"), car(196))),
      o("wink", "Opens On Machan Winking", "Hello first, then the journey.", "playful", lambda: page(("Wink first", "Hooks you in"), ptop(), vid("wink"), car(196))))
    P("Video", V, "Power moment", "for kawaii but powerful, should the big moment be Machan facing the tiger or standing with the Nagasaki tree?",
      o("tiger", "Faces The Tiger", "Small fruit, the tiger runs.", "brave", lambda: page(("Tiger tale", "Courage"), ptop(), vid("tiger"), car(196))),
      o("tree", "Stands With The Tree", "Survives and keeps growing.", "resilient", lambda: page(("Nagasaki tree", "Survival"), ptop(), vid("tree"), car(196))))
    P("Video", V, "Video style", "should the video be soft kawaii animation or a paper cut-out look?",
      o("soft", "Soft Kawaii Animation", "Rounded, smooth, gentle light.", "cute", lambda: page(("Soft animation", "Smooth"), ptop(), vid("wink"), car(196))),
      o("paper", "Paper Cut-Out Look", "Layered paper shapes, a handmade feel.", "crafted", lambda: page(("Paper cut-out", "Handmade"), ptop(), vid("wink", extra=f'<rect x="20" y="70" width="200" height="108" fill="none" stroke="#F3E6D2" stroke-width="2" stroke-dasharray="6 4" rx="6"/>'), car(196))))
    P("Wish glyph", V, "Glyph moment", "since the wish glyph is one of the coolest parts, should it be drawn in by brush in the video or glow large behind the wish slide?",
      o("brush", "Brush Draws It In Video", "Gold brush strokes write it as the video ends.", "cinematic", lambda: page(("Brush reveal", "Video finale"), ptop(), vid("glyph"), car(196))),
      o("glow", "Glows Behind Wish Slide", "Huge and faint behind the wish headline.", "lasting", lambda: page(("Behind the slide", "Stays on screen"), ptop(), vid("wink"), car(196, glyph=True))))
    P("Wish glyph", L, "Glyph colour", "should the glyph be warm gold or soft terracotta?",
      o("gold", "Warm Gold", "Good-luck gold, glows on dusk.", "lucky", lambda: page(("Gold", "Lucky"), ptop(), vid("glyph"), car(196))),
      o("terra", "Soft Terracotta", "Matches Machan himself.", "on-brand", lambda: page(("Terracotta", "On brand"), ptop(), vid("glyph").replace("#E8B04A", "#D9805F"), car(196))))
    P("Page flow", L, "Video to carousel", "should the carousel sit below the video or should the video end and turn into the first slide?",
      o("below", "Carousel Below Video", "Both on the page, scroll to the slides.", "clear", lambda: page(("Below", "Both visible"), ptop(), vid("wink"), car(196))),
      o("morph", "Video Becomes Slide One", "The last frame turns into the first slide.", "seamless", lambda: page(("Turns into slides", "One piece"), ptop(), vid("glyph", h=80), car(156) + M.T(120, 240, "video ends, slides take over", 7.5, MUTE, anchor="middle"))))
    P("Video", V, "Sound", "should the video start muted with captions or with soft music and tap for sound?",
      o("muted", "Muted With Captions", "Plays quietly, words on screen.", "polite", lambda: page(("Muted", "Captions"), ptop(), vid("wink", sound="muted"), car(196))),
      o("music", "Soft Music, Tap For Sound", "A small tune once you tap.", "warm", lambda: page(("Music", "Tap for sound"), ptop(), vid("wink", sound="tap"), car(196))))
    P("Page flow", L, "Page top", "should the page open with the Machan mark and title or go straight into the video?",
      o("title", "Mark And Title First", "The story of Machan, then the video.", "framed", lambda: page(("Title first", "Framed"), ptop(), vid("wink"), car(196))),
      o("video", "Straight Into Video", "The video is the first thing you see.", "bold", lambda: page(("Video first", "Immersive"), "", vid("wink", y=34, h=150), car(196))))
    P("Lore", "Machan Story Carousel Mockup", "Greek name slide art", "for the fruit of the gods slide, should Machan wear a tiny laurel or sit on a little cloud?",
      o("laurel", "Tiny Laurel", "A small green laurel over his leaves.", "regal", lambda: page(("Laurel", "Divine, with a wink"), ptop(), scene("wink", 14, 64, 212, 120) + f'<path d="M100 92 q20 -14 40 0" stroke="{M.LEAF2}" stroke-width="3" fill="none"/>', car(196, "Fruit of the gods."))),
      o("cloud", "Little Cloud", "Machan perched on a soft cloud.", "dreamy", lambda: page(("Cloud", "Light and divine"), ptop(), scene("wink", 14, 64, 212, 120) + '<ellipse cx="120" cy="164" rx="44" ry="10" fill="#FFFFFF" fill-opacity=".85"/>', car(196, "Fruit of the gods."))))
    P("Page flow", L, "Page ending", "after the carousel, should the page end on the wish plus Back to the board or the wish plus Watch again?",
      o("back", "Wish Plus Back Link", "May all things go as you wish, then back.", "tidy", lambda: page(("Back link", "Return"), ptop(), vid("wink"), car(196) + M.T(120, 286, "< Back to the board", 9, LAGOON, w=600, anchor="middle"))),
      o("again", "Wish Plus Watch Again", "Invites a second watch.", "playful", lambda: page(("Watch again", "Replay"), ptop(), vid("wink"), car(196) + M.T(120, 286, "Watch again", 9, TERRA, w=600, anchor="middle"))))
    return pairs
