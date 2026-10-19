"""Branding follow-up decks, Oct 19 2026 evening (Max 9:45 PM ICT: 'record the swipes that were done, make the changes, and then refresh the decks').
Five 10-pair decks, one per deck Max swiped after 4:07 PM. Skips come back reworded; every pick goes one notch further. Close-up drawings
(360x210) of the decided uk11 board state, light only, Khand + Hind, terracotta / lagoon / jungle. PRIVACY: TEST / SAMPLE data only,
Tech Dash 1-3, first names, city-level areas; no contact details of any kind."""
from md1018_kit import make
from mcd1019 import T, R, C, L, chev, chip, INK, MUTE, LINE, CREAM, WHITE, TERRA, LAGOON, JUNGLE, SOFT
from ukhf1019_kit import mark, tri, share_ic, warn, check, checkc, docic, kw, SAFF, COAL
W_, H_ = 360, 210
def svg(title, inner, tag="TEST · SAMPLE"):
    g = R(0, 0, W_, H_, WHITE) + R(.5, .5, W_ - 1, H_ - 1, "none", LINE, 10)
    g += T(14, 20, title.upper(), 8.5, TERRA, 700, extra='letter-spacing="1.2"') + T(346, 20, tag, 7.5, MUTE, 700, "end", extra='letter-spacing="1"') + L(14, 28, 346, 28, LINE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}" width="{W_}" height="{H_}" role="img" aria-label="{title}">{g}<g transform="translate(0,34)">{inner}</g></svg>'
def o(k, label, desc, feel, title, inner): return (k, label, desc, feel, svg(title, inner))
def fd(y, title, n=None, right="", open_=False, x=14, w=332, h=26, edge=None, chevl=False, size=13, body=0):
    g = R(x, y, w, h + body, WHITE, LINE) + R(x + .5, y + .5, w - 1, h - 1, CREAM)
    if edge: g += R(x, y, 3, h + body, edge)
    tx = x + (24 if chevl else 10)
    if chevl: g += chev(x + 12, y + h / 2, INK, not open_)
    g += T(tx, y + h * .68, title + (f" ({n})" if n is not None else ""), size, INK, f="khand")
    if right: g += T(x + w - (14 if chevl else 26), y + h * .66, right, 8.5, MUTE, 500, "end")
    if not chevl: g += chev(x + w - 13, y + h / 2, INK, not open_)
    return g
def mrow(y, name, plan, st, sel=None, dot=False, x=14, w=332):
    g = ""
    if sel == "both": g += R(x, y, w, 20, CREAM) + R(x, y, 3, 20, TERRA)
    if sel == "bold": g += R(x, y, w, 20, WHITE)
    g += T(x + 10, y + 14, name, 9.5, INK, 700 if sel == "bold" else 600) + (C(x + 14 + len(name) * 5.2, y + 10, 3, TERRA) if dot else "")
    if sel == "bold": g += f'<path d="M{x+w-22} {y+10} l3 3 l6 -6" fill="none" stroke="{LAGOON}" stroke-width="1.8" stroke-linecap="round"/>'
    g += T(x + 130, y + 14, plan, 9, MUTE) + chip(x + 200, y + 4, st, {"Active": JUNGLE, "Paused": MUTE, "New": LAGOON}.get(st, TERRA), "dot", 8)[0] + L(x, y + 20, x + w, y + 20)
    return g
MEM = [("Avery", "Plus", "Active", True), ("Blake", "Plus", "Active", False), ("Casey", "Plus", "Paused", True), ("Devon", "Plus", "New", False)]
def mtable(y=4, sel=None, head=None, hover=None):
    g = R(14, y, 332, 18, SOFT) + "".join(T(24 + x, y + 12, h_, 7.5, MUTE, 700) for x, h_ in ((0, "MEMBER"), (120, "PLAN"), (190, "STATUS"), (262, "NEXT VISIT")))
    if head == "arrow": g += f'<path d="M{24+38} {y+8} l3 4 l3 -4z" fill="{LAGOON}"/>'
    if head == "under": g += L(22, y + 16, 64, y + 16, LAGOON, 2)
    g += L(14, y + 22, 346, y + 22, JUNGLE, 1.5) + T(20, y + 35, "Plus (24)", 10, JUNGLE, f="khand"); yy = y + 40
    for i, (n, p, s, d) in enumerate(MEM):
        g += mrow(yy, n, p, s, sel if i == 0 else None, d); yy += 21
    return g + (hover or "")

def T_MEMBERS():
    pairs, P = make("mcft19e_", "UpKeep"); LOC = "Members Catalog"
    P("Selected row", LOC, "Open row marker", "you skipped this before, so asked another way: when a member's panel is open, which row marker reads best?",
      o("both", "Cream Fill With Terracotta Edge", "Warm fill plus a thin edge, as built tonight.", "warm", "Open row", mtable(sel="both")),
      o("bold", "Bold Name With Lagoon Tick", "Row stays white; name bolds, a tick appears.", "crisp", "Open row", mtable(sel="bold")))
    P("Sorting", LOC, "Sorted column cue", "now you sort by clicking a column header, should the sorted column show a small arrow or an underline?",
      o("arrow", "Small Lagoon Arrow", "A tiny arrow beside the sorted header.", "familiar", "Sorted column", mtable(head="arrow")),
      o("under", "Underlined Header", "The sorted header gets a lagoon underline.", "clean", "Sorted column", mtable(head="under")))
    tip = R(60, 34, 170, 30, INK, rx=4) + T(70, 47, "Open: roof photos missing", 8.5, WHITE, 600) + T(70, 58, "Asked at last visit", 7.5, "#D9D1C3")
    P("Open-item dot", LOC, "Dot on hover", "with a small terracotta dot beside names, should hovering the dot show the open item or should the dot stay quiet?",
      o("tip", "Hover Shows The Item", "A small tip names the open item.", "helpful", "Open-item dot", mtable(hover=tip)),
      o("quiet", "Quiet Dot Only", "Details only in the member panel.", "calm", "Open-item dot", mtable()))
    grp = lambda extra: L(14, 14, 346, 14, JUNGLE, 1.5) + T(20, 30, "Plus (24" + extra + ")", 13, JUNGLE, f="khand") + L(14, 76, 346, 76, LAGOON, 1.5) + T(20, 92, "Essentials (31" + (" · 27 active" if extra else "") + ")", 13, LAGOON, f="khand") + mrow(36, "Avery", "Plus", "Active") + mrow(100, "Blake", "Essentials", "Active")
    P("Plan group count", LOC, "Active count", "now each plan rule shows its count, should it also say how many in that plan are active?",
      o("count", "Count Only", "Plus (24).", "simple", "Plan group rule", grp("")),
      o("active", "Count And Active", "Plus (24 · 22 active).", "informative", "Plan group rule", grp(" · 22 active")))
    lets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    one = "".join(T(20 + i * 12.6, 30, c, 9.5, INK if c != "D" else LAGOON, 600) for i, c in enumerate(lets)) + L(57, 34, 66, 34, LAGOON, 2) + T(20, 52, "Swipe the row on a phone", 8.5, MUTE)
    two_ = "".join(T(24 + (i % 13) * 24, 26 + (i // 13) * 26, c, 11, INK if c != "D" else LAGOON, 600) for i, c in enumerate(lets)) + L(94, 30, 104, 30, LAGOON, 2)
    P("Jump bar", LOC, "Letters on a phone", "with the lagoon underline on the current letter, should the letters stay on one sliding row or wrap into two rows on a phone?",
      o("one", "One Sliding Row", "One tidy row you slide sideways.", "compact", "Jump bar on phone", one),
      o("two", "Two Rows, All Showing", "Every letter visible, bigger targets.", "easy", "Jump bar on phone", two_))
    nr = lambda extra: R(14, 6, 332, 22, WHITE, LINE) + T(24, 21, "Avry", 10, INK) + T(176, 70, "No members match.", 10, MUTE, 500, "middle") + R(130, 80, 92, 24, WHITE, INK) + T(176, 96, "Clear filters", 9.5, INK, 600, "middle") + extra
    P("No results", LOC, "Closest names", "when a search finds nobody and Clear filters shows, should closest name matches also appear?",
      o("clear", "Clear Filters Only", "One line and the button, as built.", "quiet", "No results", nr("")),
      o("near", "Plus Closest Matches", "Did you mean: Avery, Ava?", "forgiving", "No results", nr(T(176, 130, "Did you mean:", 9, MUTE, 500, "middle") + chip(132, 138, "Avery", LAGOON, "soft", 9)[0] + chip(186, 138, "Ava", LAGOON, "soft", 9)[0])))
    tiles = lambda n: "".join(R(14 + i * (332 / n), 10, 332 / n - 6, 56, CREAM, LINE) + T(24 + i * (332 / n), 40, v, 20, INK, 600) + T(24 + i * (332 / n), 56, l, 7.5, MUTE, 700, extra='letter-spacing="1"') for i, (v, l) in enumerate((("2002", "BUILT"), ("3,280", "SQ FT"), ("9", "SYSTEMS"), ("Oct 12", "LAST VISIT"))[:n]))
    P("Number tiles", LOC, "Tile count", "with big numbers over small labels, should the home tiles stay at three or add a fourth for the last visit?",
      o("three", "Keep Three Tiles", "Built, Sq Ft, Systems.", "focused", "Home tiles", tiles(3)),
      o("four", "Add Last Visit", "A fourth tile: the last visit date.", "complete", "Home tiles", tiles(4)))
    th = lambda: "".join(R(14 + i * 112, 10, 106, 64, SOFT, LINE) + f'<path d="M{34+i*112} 60 l22 -22 l22 22z" fill="{JUNGLE}55"/>' for i in range(3))
    P("Photo strip", LOC, "Tapping a thumbnail", "with three thumbnails in a row, should tapping one enlarge it inside the panel or open a full-screen viewer?",
      o("inpanel", "Enlarge In The Panel", "The big photo swaps in above the row.", "steady", "Thumbnail tap", R(14, 4, 332, 90, SOFT, LINE) + f'<path d="M60 86 l60 -60 l60 60z" fill="{JUNGLE}55"/>' + "".join(R(14 + i * 112, 102, 106, 40, SOFT, TERRA if i == 0 else LINE, 0, 1.5 if i == 0 else 1) for i in range(3))),
      o("full", "Full-Screen Viewer", "Dark viewer, swipe between photos.", "immersive", "Thumbnail tap", R(14, 4, 332, 140, "#2A2420", rx=4) + f'<path d="M110 130 l70 -70 l70 70z" fill="{JUNGLE}99"/>' + T(330, 22, "×", 16, WHITE, 600, "end") + T(180, 142, "‹  1 of 3  ›", 9, "#E9DFCD", 600, "middle")))
    vr = lambda body: (T(14, 16, "Oct 12", 10, INK, 600) + T(70, 16, "Tech Dash 2", 9.5, MUTE) + chip(150, 6, "Done", JUNGLE, "dot", 8)[0] + chev(336, 12, INK, False) + L(14, 24, 346, 24, LINE) + body)
    P("Visit row", LOC, "Tapping a visit", "you said we could click for more info, so should a tapped visit open a short note or a fuller visit card?",
      o("note", "Short Note Opens", "One line from the tech under the row.", "light", "Visit row", vr(T(14, 42, "Seasonal visit", 8.5, MUTE) + T(14, 58, "Gutters cleared, filter changed, all good.", 9.5, INK))),
      o("card", "Fuller Visit Card", "Tasks ticked, photos and the note.", "thorough", "Visit row", vr(R(14, 32, 332, 108, CREAM, LINE, 4) + "".join(check(26, 44 + i * 18, True) + T(44, 53 + i * 18, t_, 9, INK) for i, t_ in enumerate(("Filter changed", "Gutters cleared", "Smoke and CO checked"))) + "".join(R(200 + i * 46, 44, 40, 30, SOFT, LINE) for i in range(3)) + T(26, 128, "Note: all good, next visit in November.", 9, MUTE))))
    pnl = lambda extra: R(120, 4, 226, 140, WHITE, LINE) + R(310, 10, 28, 28, WHITE, LINE) + T(324, 30, "×", 16, INK, 600, "middle") + T(132, 60, "Avery", 16, INK, f="khand") + T(132, 76, "Plus · Active · Farmington Hills", 8.5, MUTE) + mtable(4)[:0] + extra
    P("Closing the panel", LOC, "Other ways to close", "with the X at the top right, should Esc on a keyboard close it too, or should a phone also close it with a swipe down?",
      o("esc", "X Plus Esc Key", "Keyboard Esc closes the panel.", "desk", "Close panel", pnl(R(132, 96, 60, 22, SOFT, LINE, 3) + T(162, 111, "Esc", 9.5, INK, 600, "middle") + T(200, 111, "closes it", 9, MUTE))),
      o("swipe", "X Plus Swipe Down", "On a phone, pull the panel down to close.", "phone", "Close panel", pnl(R(213, 92, 40, 4, "#CFC6B6", rx=2) + f'<path d="M233 104 v26 m-7 -7 l7 7 l7 -7" fill="none" stroke="{LAGOON}" stroke-width="1.8"/>')))
    return pairs

def T_RULES():
    pairs, P = make("rlft19e_", "UpKeep"); LOC = "All UpKeep Boards"
    hd = lambda caps: (T(14, 30, "MEMBERS CATALOG", 11, INK, 700, extra='letter-spacing="2"') + L(14, 38, 346, 38, LINE) if caps else T(14, 34, "Members Catalog", 20, INK, f="khand")) + T(14, 60, "Every test member, filter by plan, jump by letter.", 9.5, MUTE) + fd(76, "Sign-ups", 88, "8 started · 80 upcoming") + fd(110, "Cancellations", 12, "4 cancelled · 3 pending")
    P("Section headings", LOC, "Heading style", "you left this to me, so here it is again plainly: section titles in Khand like now, or small spaced capitals over a thin rule?",
      o("khand", "Khand Title Case", "Members Catalog, bold Khand, as built.", "branded", "Section heading", hd(False)),
      o("caps", "Small Caps Over A Rule", "MEMBERS CATALOG, small, spaced, ruled.", "editorial", "Section heading", hd(True)))
    txt = lambda two: T(14, 26, "Water heater flush is booked for Tue.", 12, INK) + T(14, 46, "The tech will bring the hose kit.", 12, INK) + T(14, 70, "Oct 19 · Members Agent", 12 if not two else 9.5, MUTE) + T(14, 96, "Plus · Active · Novi", 12 if not two else 9.5, MUTE)
    P("Body text", LOC, "Text sizes", "you said you like uniform design, so should every line use one size, or text one size with dates and tags a step smaller?",
      o("one", "One Size Everywhere", "Every line at the comfortable size.", "uniform", "Body text", txt(False)),
      o("two", "Text Plus Smaller Meta", "Dates and tags one quiet step smaller.", "layered", "Body text", txt(True)))
    P("Fold opening", LOC, "Chevron motion", "with the quick slide open, should the chevron turn as the fold slides or flip at once?",
      o("turn", "Chevron Turns", "The chevron rotates with the slide.", "smooth", "Fold opening", fd(14, "Sign-ups", 88, "8 started") + f'<path d="M318 30 a12 12 0 0 1 14 -8" fill="none" stroke="{LAGOON}" stroke-width="1.4" stroke-dasharray="2 2"/>' + R(14, 40, 332, 60, WHITE, LINE) + T(24, 62, "Rows slide in…", 9, MUTE)),
      o("flip", "Chevron Flips", "The chevron swaps at the start.", "snappy", "Fold opening", fd(14, "Sign-ups", 88, "8 started", True) + R(14, 40, 332, 60, WHITE, LINE) + T(24, 62, "Rows slide in…", 9, MUTE)))
    cards = lambda folds_only: (R(14, 8, 160, 70, WHITE, "#D6CCBA" if not folds_only else "none") + R(186, 8, 160, 70, WHITE, "#D6CCBA" if not folds_only else "none") + (R(14, 8, 160, 70, "#FCFAF6") + R(186, 8, 160, 70, "#FCFAF6") if folds_only else "") + T(26, 34, "Tech Dash 1", 12, INK, f="khand") + T(198, 34, "Tech Dash 2", 12, INK, f="khand") + fd(92, "Visit Log", 20, "20 done visits", edge=None) + fd(124, "Certifications", None, "3 techs"))
    P("Beige border", LOC, "Where the firmer line goes", "with the firmer beige border, should it frame every card or only the folds, with cards on a soft fill?",
      o("all", "Every Card And Fold", "One firmer beige line everywhere.", "framed", "Firmer border", cards(False)),
      o("folds", "Folds Only, Soft Cards", "Cards sit on a soft fill, no line.", "airy", "Firmer border", cards(True)))
    sb = lambda extra: R(0, 0, 360, 40, CREAM) + L(0, 40, 360, 40, LINE) + mark(14, 7, 26) + T(48, 26, "Members Command Center", 15, INK, f="khand") + R(320, 8, 26, 26, WHITE, INK) + share_ic(321, 9) + extra + T(14, 70, "Slim bar after you scroll past the header", 9, MUTE)
    P("Slim bar", LOC, "Search in the bar", "with the slim bar showing mark, title and share, should it also carry a search icon?",
      o("plain", "Title And Share", "Just the mark, title and share.", "calm", "Slim bar", sb("")),
      o("search", "Add A Search Icon", "Jump to search from anywhere.", "handy", "Slim bar", sb(R(288, 8, 26, 26, WHITE, LINE) + C(299, 19, 5, "none", INK, 1.5) + L(303, 23, 307, 27, INK, 1.5))))
    em = lambda s1, s2="": fd(10, "Renewals", 0, "None yet", True, body=50) + T(24, 58, s1, 10, MUTE) + (T(24, 74, s2, 10, MUTE) if s2 else "")
    P("Empty lines", LOC, "Who and when", "now empty lines say who fills them, should they also say when?",
      o("who", "Who Fills It", "The Members Agent adds renewals here.", "plain", "Empty line", em("The Members Agent adds renewals here.")),
      o("whowhen", "Who And When", "Adds: once the first plan renews.", "clear", "Empty line", em("The Members Agent adds renewals here", "once the first plan renews.")))
    ce = lambda mean: "".join(R(14 + i * 112, 10, 106, 80, WHITE, LINE) + R(14 + i * 112, 10, 3, 80, c) + T(26 + i * 112, 34, n, 12, INK, f="khand") + T(26 + i * 112, 52, s, 8.5, MUTE) for i, (n, s, c) in enumerate(((("Tech Dash 1", "On route", JUNGLE), ("Tech Dash 2", "Running late", TERRA), ("Tech Dash 3", "Off today", MUTE)) if mean else (("Tech Dash 1", "On route", LAGOON), ("Tech Dash 2", "Running late", TERRA), ("Tech Dash 3", "Off today", JUNGLE))))) + T(14, 112, "Edge colour " + ("follows status" if mean else "rotates by card"), 9, MUTE)
    P("Card edge", LOC, "Edge colour", "with a thin coloured edge on cards, should the colour follow the card's status or just rotate terracotta, lagoon and jungle?",
      o("meaning", "Colour Follows Status", "Green on route, terracotta late, grey off.", "meaningful", "Card edge", ce(True)),
      o("rotate", "Rotating Brand Colours", "Lagoon, terracotta, jungle in turn.", "lively", "Card edge", ce(False)))
    nm = lambda lab_above: "".join(R(14 + i * 84, 10, 78, 58, WHITE, LINE) + ((T(22 + i * 84, 26, l, 9, MUTE, f="khand") + T(22 + i * 84, 52, v, 20, INK, 600)) if lab_above else (T(22 + i * 84, 38, v, 20, INK, 600) + T(22 + i * 84, 56, l, 7.5, MUTE, 700, extra='letter-spacing="1"'))) for i, (v, l) in enumerate((("100", "MEMBERS" if not lab_above else "Members"), ("4", "CANCELLED" if not lab_above else "Cancelled"), ("5", "PAUSED" if not lab_above else "Paused"), ("3", "OPEN" if not lab_above else "Open"))))
    P("Numbers", LOC, "Number labels", "with counts now in Hind numerals, should the small label sit under the number or above it in Khand?",
      o("under", "Label Under, Small Caps", "Number first, small label under.", "classic", "Number tiles", nm(False)),
      o("above", "Khand Label Above", "Khand label on top, Hind number below.", "branded", "Number tiles", nm(True)))
    sp = lambda rule: fd(6, "Member Catalog", 96, "84 active") + fd(38, "Sign-ups", 88, "8 started") + (L(14, 74, 346, 74, TERRA, 1) if rule else "") + fd(80 if rule else 70, "Ping Record", 5, "3 active") + fd(112 if rule else 102, "Routines", 0, "0 active")
    P("Section spacing", LOC, "Group breaks", "with one even gap down the board, should the footer group also get a thin rule above it?",
      o("even", "Even Gaps Only", "One rhythm, no extra lines.", "uniform", "Section spacing", sp(False)),
      o("rule", "Thin Rule Before Footer", "A hairline marks where the footer starts.", "structured", "Section spacing", sp(True)))
    cv = lambda btn_: fd(14, "Sign-ups", 88, "8 started") + fd(50, "Cancellations", 12, "4 cancelled") + ((R(318, 18, 20, 20, WHITE, LINE, 10) + R(318, 54, 20, 20, WHITE, LINE, 10)) if btn_ else "")
    P("Chevron", LOC, "Chevron weight", "with the chevron on the right of every fold, should it be a thin mark or sit in a small round button?",
      o("thin", "Thin Chevron", "A light mark at the right end.", "minimal", "Fold chevron", cv(False)),
      o("btn", "Chevron In A Round Button", "A clear round tap target.", "tappable", "Fold chevron", cv(True)))
    return pairs

VT = {"Seasonal": LAGOON, "Monthly": JUNGLE, "Welcome": "#B5841C", "Repair": TERRA}
def vchip(x, y, t_, n, k, w=96):
    return R(x, y, w, 26, WHITE, LINE) + R(x, y, 3, 26, VT[k]) + T(x + 8, y + 11, t_, 8, INK, 600) + T(x + 8, y + 21, n, 8, MUTE)
def T_SCHED():
    pairs, P = make("scft19e_", "UpKeep"); LOC = "Scheduling Board"
    dots = "".join(C(40 + i * 46, 60 + (20 if i % 2 else -10), 5 if i else 7, LAGOON) for i in range(6))
    route = f'<polyline points="{" ".join(f"{40+i*46},{60+(20 if i%2 else -10)}" for i in range(6))}" fill="none" stroke="#8b8478" stroke-width="1.5" stroke-dasharray="4 3"/>'
    blocks = "".join(R(20 + (i % 4) * 82, 14 + (i // 4) * 44, 76, 38, LAGOON + ("44" if i in (1, 2, 6) else "18"), LINE) + T(28 + (i % 4) * 82, 30 + (i // 4) * 44, z, 9, INK, 600) for i, z in enumerate(("Novi", "Troy", "Canton", "Livonia", "Plymouth", "Northville", "Wixom", "Milford")))
    P("Zone-Day Map", LOC, "Route drawing", "asked another way since you skipped it: on the zone-day card, do you want to see the route as joined stops or which zones are busy?",
      o("route", "Joined Stops In Order", "Dots joined in visit order, no real map.", "sequence", "Zone-day card", route + dots + T(14, 120, "Novi · 6 stops · Tech Dash 1", 9, MUTE)),
      o("zones", "Busy Zones Shaded", "Zone tiles shaded by stops that day.", "overview", "Zone-day card", blocks + T(14, 120, "Darker tile = more stops today", 9, MUTE)))
    leg = lambda inrow: (fd(4, "Schedule", None, "36 visits this week") if not inrow else fd(4, "Schedule", None, "") + "".join(R(150 + i * 46, 14, 8, 8, c) + T(161 + i * 46, 21, k[:5], 7.5, MUTE) for i, (k, c) in enumerate(VT.items()))) + ("" if inrow else "".join(R(14 + i * 80, 40, 9, 9, c) + T(27 + i * 80, 48, k, 8.5, INK) for i, (k, c) in enumerate(VT.items()))) + vchip(14, 60, "8:08a", "Kwame", "Seasonal") + vchip(116, 60, "8:35a", "Jun", "Welcome") + vchip(218, 60, "9:01a", "Ibrahim", "Repair")
    P("Visit type colours", LOC, "Legend place", "with chip edges coloured by visit type, should the colour key sit above the grid or tucked into the fold title row?",
      o("above", "Key Above The Grid", "Its own line over the week.", "clear", "Visit colour key", leg(False)),
      o("inrow", "Key In The Title Row", "Saves a line, sits right of the title.", "compact", "Visit colour key", leg(True)))
    full = lambda word: T(14, 20, "Tue Oct 20", 11, INK, 600) + "".join(R(14 + i * 18, 30, 14, 8, JUNGLE) for i in range(4)) + T(14, 52, "TD1", 8, MUTE) + (chip(96, 26, "Full", JUNGLE, "soft", 8)[0] if word else "") + T(14, 80, "Four of four sample stops booked", 9, MUTE)
    P("Full day", LOC, "Full-day word", "now a full day turns jungle green, should it also say Full in words?",
      o("blocks", "Green Blocks Only", "The colour says it.", "quiet", "Full day", full(False)),
      o("word", "Green Plus Full", "A small Full chip beside the blocks.", "explicit", "Full day", full(True)))
    td = lambda now: R(120, 4, 110, 140, CREAM) + "".join(R(14 + i * 110, 4, 108, 140, "none", LINE) + T(22 + i * 110, 20, d, 10, INK, 600) for i, d in enumerate(("Mon", "Today · Tue", "Wed"))) + vchip(126, 30, "8:13a", "Dominic", "Monthly", 96) + vchip(126, 80, "10:20a", "Rafael", "Seasonal", 96) + (L(120, 66, 230, 66, TERRA, 1.5) + C(120, 66, 3, TERRA) + T(226, 62, "now", 7.5, TERRA, 700, "end") if now else "")
    P("Today", LOC, "Now line", "with today as a cream column, should a thin terracotta now line also cross it at the current time?",
      o("cream", "Cream Column Only", "Today stands out, nothing moving.", "calm", "Today column", td(False)),
      o("now", "Cream Plus Now Line", "A thin line marks the current time.", "live", "Today column", td(True)))
    hl = lambda step: "".join((T(14, 14 + i * 22, f"{h} AM" if h < 12 else "12 PM", 7.5, "#a39a8b") + L(50, 11 + i * 22, 346, 11 + i * 22, "#efe9df")) if (i % step == 0) else L(50, 11 + i * 22, 346, 11 + i * 22, "#f5f1ea") for i, h in enumerate(range(8, 14))) + vchip(56, 15, "8:08a", "Kwame", "Seasonal") + vchip(160, 60, "10:19a", "Paige", "Monthly")
    P("Hour lines", LOC, "Hour labels", "with faint hour lines in the day, should every hour carry a label or only every other hour?",
      o("every", "Label Every Hour", "8 AM, 9 AM, 10 AM.", "precise", "Hour lines", hl(1)),
      o("other", "Every Other Hour", "8 AM, 10 AM, 12 PM; lighter look.", "airy", "Hour lines", hl(2)))
    trk = lambda all_: "".join(C(30 + i * 90, 30, 7, LAGOON if i < 2 else WHITE, LAGOON, 1.5) + (L(37 + i * 90, 30, 113 + i * 90, 30, LAGOON if i < 1 else "#cfc6b6", 1.5) if i < 2 else "") + ((T(30 + i * 90, 52, n, 9, LAGOON if i < 2 else MUTE, 600, "middle")) if (all_ or i == 1) else "") for i, n in enumerate(("Requested", "Booked", "Done"))) + T(14, 86, "Rania · move the December visit", 9.5, INK)
    P("Tracker", LOC, "Step names", "with Requested, Booked, Done on the tracker, should every step show its name or only the current one?",
      o("all", "All Three Names", "You see the whole path.", "complete", "Request tracker", trk(True)),
      o("cur", "Current Step Only", "Just the step it is on.", "minimal", "Request tracker", trk(False)))
    col = lambda wait: "".join(R(14 + i * 112, 4, 106, 120, "#FCFBF8", LINE) + T(22 + i * 112, 22, f"{n} ({c})", 11, INK, f="khand") + (T(22 + i * 112, 36, w_, 8, TERRA if "2 d" in w_ else MUTE, 600) if wait else "") for i, (n, c, w_) in enumerate((("New", 3, "Oldest: 2 days"), ("Slot Proposed", 2, "Oldest: 5 hr"), ("Waiting", 2, "Oldest: 1 day"))))
    P("Request columns", LOC, "Oldest waiting", "with counts in the column headers, should each header also show how long the oldest request has waited?",
      o("count", "Count Only", "New (3).", "clean", "Request columns", col(False)),
      o("oldest", "Count And Oldest Wait", "New (3) · oldest 2 days.", "urgent", "Request columns", col(True)))
    wx = lambda side: (R(14, 4, 332 if not side else 160, 70, WHITE, LINE) + T(22, 20, "Weather Watch", 11, INK, f="khand") + "".join(T(30 + i * (62 if not side else 30), 46, d, 8 if side else 9, INK if d != "Fri" else TERRA, 600) for i, d in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri")))) + (R(186, 4, 160, 70, WHITE, LINE) + T(194, 20, "Zone-Day Map", 11, INK, f="khand") + C(220, 50, 4, LAGOON) + C(250, 40, 4, LAGOON) + C(280, 52, 4, LAGOON) if side else R(14, 82, 332, 40, WHITE, LINE) + T(22, 106, "Zone-Day Map", 11, INK, f="khand"))
    P("Optional cards", LOC, "Weather and map layout", "with Weather Watch and the Zone-Day Map leading, should weather run full width or sit beside the map?",
      o("full", "Weather Full Width", "A wide strip, map below.", "readable", "Optional cards", wx(False)),
      o("side", "Side By Side", "Weather and map share one row.", "compact", "Optional cards", wx(True)))
    snow = lambda icon: "".join(R(14 + i * 66, 6, 62, 80, WHITE if i < 4 else "#FFF8F5", LINE if i < 4 else TERRA) + T(22 + i * 66, 24, d, 10, INK, 600) + T(22 + i * 66, 48, t_, 15, INK, 600) for i, (d, t_) in enumerate((("Mon", "52°"), ("Tue", "47°"), ("Wed", "44°"), ("Thu", "36°"), ("Fri", "31°")))) + (T(286, 74, "Snow-day", 8, TERRA, 700) if not icon else f'<g stroke="{LAGOON}" stroke-width="1.6" stroke-linecap="round"><path d="M314 62 v18 M305 67 l18 8 M305 75 l18 -8"/></g>')
    P("Weather strip", LOC, "Snow flag", "on the five-day strip, should a risky day carry the word Snow-day or a small snowflake?",
      o("word", "Snow-Day Word", "Terracotta word on the day.", "plain", "Weather strip", snow(False)),
      o("flake", "Small Snowflake", "A lagoon snowflake icon.", "visual", "Weather strip", snow(True)))
    off = lambda grey: "".join(R(14 + i * 47, 6, 43, 60, WHITE, LINE) + T(20 + i * 47, 22, d, 9, INK, 600) for i, d in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))) + (T(20, 44, "TD1", 9, LAGOON, 700) + T(161, 44, "TD3", 9, JUNGLE, 700) if not grey else C(24, 41, 3, LAGOON) + T(30, 44, "TD1", 9, MUTE, 600) + C(165, 41, 3, JUNGLE) + T(171, 44, "TD3", 9, MUTE, 600)) + T(14, 90, "Days off this week", 9, MUTE)
    P("Days off", LOC, "Initials look", "with tech initials on the day off, should the initials be in the tech's colour or grey with a coloured dot?",
      o("colour", "Initials In Tech Colour", "TD1 in lagoon, TD3 in jungle.", "bright", "Days off strip", off(False)),
      o("dot", "Grey With A Dot", "Quiet initials, a small colour dot.", "subtle", "Days off strip", off(True)))
    return pairs

def T_HEADER():
    pairs, P = make("hdft19e_", "UpKeep"); LOC = "UpKeep Board Header"
    dc = lambda c: "".join(docic(18, 10 + i * 30, LAGOON) + T(40, 22 + i * 30, n, 10.5, INK, 600) + R(240, 10 + i * 30, 96, 16, cc + "1A", cc, 8) + T(288, 22 + i * 30, s, 8.5, cc, 700, "middle") for i, (n, s, cc) in enumerate((("Welcome Message", "Draft", c), ("Welcome Flow Deck", "For approval", c), ("Member FAQ", "Approved", JUNGLE)))) + T(14, 110, "Alerts stay terracotta: " + ("same colour as drafts" if c == TERRA else "drafts look different"), 9, MUTE)
    P("Draft chips", LOC, "Draft colour", "asked again since you left it to me: drafts waiting for you in terracotta like alerts, or saffron so terracotta stays for alerts?",
      o("terra", "Terracotta Drafts", "As built: drafts and alerts share a colour.", "bold", "Approval chips", dc(TERRA)),
      o("saff", "Saffron Drafts", "Terracotta is kept for alerts only.", "distinct", "Approval chips", dc(SAFF)))
    bl = lambda left: R(0, 0, 360, 34, CREAM) + T(14, 22, "Apps Home", 9.5, INK, 600) + (T(80, 22, "← Back to UpKeep Command Center", 9.5, LAGOON, 600) if left else T(310, 22, "← Back to UpKeep Command Center", 9.5, LAGOON, 600, "end")) + R(320, 5, 26, 26, WHITE, INK) + share_ic(321, 6) + mark(14, 46, 40) + T(64, 70, "Members Command Center", 17, INK, f="khand")
    P("Back link", LOC, "Back link place", "with the link reading Back to UpKeep Command Center, should it sit top right by share or top left by Apps Home?",
      o("right", "Top Right By Share", "Where it is now.", "familiar", "Back link", bl(False)),
      o("left", "Top Left By Apps Home", "Both ways out in one corner.", "grouped", "Back link", bl(True)))
    mk_ = lambda tile: mark(14, 14, 52, tile) + T(78, 40, "Members Command Center", 18, INK, f="khand") + T(78, 58, "Members Agent · Reports to Ethan", 9.5, MUTE) + tri(80, 14, 346)
    P("House mark", LOC, "Mark tile", "with the medium mark beside the title, should it keep its white tile or stand on the cream band by itself?",
      o("tile", "Mark On A Tile", "A small framed tile, as built.", "badge", "House mark", mk_(True)),
      o("bare", "Mark On Its Own", "No tile, just the mark.", "light", "House mark", mk_(False)))
    from ukhf1019_kit import HAZ
    al = lambda per: fd(0, "Emergency Alerts", None, "2 live", True, edge=TERRA, body=70) + "".join(R(26, 34 + i * 30, 56, 18, (HAZ[h] if per else TERRA) + "1F", HAZ[h] if per else TERRA, 9) + T(54, 47 + i * 30, h, 8.5, HAZ[h] if per else TERRA, 700, "middle") + (warn(90, 37 + i * 30, TERRA, 12) if not per else "") + T(110 if not per else 92, 47 + i * 30, w_, 9.5, INK, 600) for i, (h, w_) in enumerate((("CO", "CO alarm sounding · Troy"), ("Gas", "Gas smell at the meter · Novi"))))
    P("Alert tags", LOC, "Hazard colours", "with the most serious alerts first, should each hazard keep its own colour or all share terracotta with a warning sign?",
      o("per", "Own Colour Per Hazard", "CO charcoal, gas terracotta, water lagoon.", "sorted", "Alert tags", al(True)),
      o("one", "All Terracotta, Warning Sign", "One alarm colour, the sign does the rest.", "urgent", "Alert tags", al(False)))
    ac = lambda folded: (fd(10, "Emergency Alerts", None, "No active alerts · Board built 4:34 PM") if folded else R(14, 10, 332, 30, JUNGLE + "12", JUNGLE + "55") + checkc(30, 25) + T(44, 29, "No active alerts", 10.5, JUNGLE, 700) + T(338, 29, "Board built 4:34 PM", 8.5, MUTE, 500, "end")) + fd(52, "To-Do List", 1, "1 open") + fd(86, "Documents Center", 2, "2 docs")
    P("All clear", LOC, "All-clear shape", "with No active alerts and the check line, should it stay a green strip or become a closed fold like its neighbours?",
      o("strip", "Green Strip", "Stands apart, reads at a glance.", "reassuring", "All clear", ac(False)),
      o("fold", "Closed Fold Like The Rest", "Uniform row, green text in the summary.", "uniform", "All clear", ac(True)))
    dn = lambda last: fd(0, "To-Do List", 3, "1 open · 2 done", True, body=78) + check(26, 36) + T(44, 46, "Review the welcome message draft", 10, INK, 600) + R(26, 62, 308, 24, CREAM, LINE) + T(36, 78, "Done (2)" + (" · last: Pin the member FAQ" if last else ""), 9.5, MUTE, 600) + chev(322, 74, INK)
    P("Done fold", LOC, "Done fold summary", "with ticked to-dos in a closed Done fold, should its title show just the count or also the last thing ticked?",
      o("count", "Count Only", "Done (2).", "tidy", "Done fold", dn(False)),
      o("last", "Count Plus Last Ticked", "Done (2) · last: Pin the member FAQ.", "reassuring", "Done fold", dn(True)))
    pv = lambda summ: R(14, 4, 110, 140, WHITE, LINE) + "".join(docic(22, 14 + i * 26, LAGOON, 12) + T(40, 24 + i * 26, n, 8.5, INK, 600) for i, n in enumerate(("Welcome Message", "Flow Deck", "Member FAQ"))) + R(130, 4, 216, 140, WHITE, LINE) + (T(140, 22, "In short: the welcome note for new members,", 8.5, INK) + T(140, 34, "draft waiting for your approval.", 8.5, INK) + L(140, 44, 336, 44, LINE) if summ else "") + "".join(L(140, (56 if summ else 22) + i * 12, 330 - (i % 3) * 30, (56 if summ else 22) + i * 12, "#D9D1C3", 3) for i in range(7 if summ else 9))
    P("Preview pane", LOC, "Preview top", "with a narrow list and wide preview, should the preview open straight on the first page or show a short summary on top?",
      o("page", "First Page Straight Away", "The document itself, nothing added.", "direct", "Preview pane", pv(False)),
      o("summ", "Short Summary On Top", "Two lines on what it is and what it needs.", "guided", "Preview pane", pv(True)))
    sl = lambda up: R(0, 0, 360, 40, CREAM) + L(0, 40, 360, 40, LINE) + mark(14, 7, 26) + T(48, 26, "Members Command Center", 15, INK, f="khand") + R(320, 8, 26, 26, WHITE, INK) + share_ic(321, 9) + f'<path d="M180 {110 if up else 70} v{-30 if up else 30} m-7 {7 if up else -7} l7 {-7 if up else 7} l7 {7 if up else -7}" fill="none" stroke="{LAGOON}" stroke-width="1.8"/>' + T(200, 96, "Shows when you scroll up" if up else "Stays once past the header", 9, MUTE)
    P("Slim bar", LOC, "When it shows", "with the slim bar after the header, should it stay all the time or only slide in when you scroll back up?",
      o("always", "Always Once Past The Header", "Title and share always in reach.", "steady", "Slim bar", sl(False)),
      o("up", "Only When Scrolling Up", "More room while you read down.", "roomy", "Slim bar", sl(True)))
    st = lambda last: mark(14, 10, 44) + T(68, 34, "Members Command Center", 17, INK, f="khand") + chip(68, 44, "Agent active" + (" · ran 9:40 PM" if last else ""), JUNGLE, "dot", 9)[0]
    P("Status chip", LOC, "Last run time", "with Agent active by the title, should it also say when the agent last ran?",
      o("plain", "Agent Active", "Just the green dot and words.", "simple", "Status chip", st(False)),
      o("time", "Agent Active Plus Last Run", "Agent active · ran 9:40 PM.", "honest", "Status chip", st(True)))
    op = lambda edge: fd(0, "Emergency Alerts", None, "Opened itself · 1 live alert", True, edge=TERRA if edge else None, body=50) + R(26, 34, 56, 18, LAGOON + "1F", LAGOON, 9) + T(54, 47, "Flooding", 8.5, LAGOON, 700, "middle") + T(92, 47, "Water on a basement floor · Livonia", 9.5, INK, 600) + (C(160, 13, 8, TERRA) + T(160, 16.5, "1", 9, WHITE, 700, "middle") if not edge else "")
    P("Opened alert", LOC, "Open alert marker", "when an alert opens its fold and stays still, should a count badge or a terracotta edge mark it?",
      o("badge", "Count Badge", "A small terracotta number.", "countable", "Opened alert", op(False)),
      o("edge", "Terracotta Edge", "A thin edge down the fold.", "calm", "Opened alert", op(True)))
    return pairs

def mc(x, y, s=22, wink=False):
    g = f'<g transform="translate({x},{y}) scale({s/24})"><path d="M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z" fill="#3F7D58"/><path d="M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z" fill="#5E9A6E"/><rect x="3.5" y="5.5" width="17" height="16" rx="7" fill="#C8643F"/><rect x="5.5" y="9" width="13" height="10" rx="5" fill="#FAF6EE"/><circle cx="9.6" cy="13.3" r="1.35" fill="#2E6F86"/>'
    g += ('<path d="M13.2 13.5q1.2-1.2 2.4 0" fill="none" stroke="#2E6F86" stroke-width="1.1" stroke-linecap="round"/>' if wink else '<circle cx="14.4" cy="13.3" r="1.35" fill="#2E6F86"/>')
    return g + '<path d="M10.6 16.1q1.4 1.1 2.8 0" fill="none" stroke="#C8643F" stroke-width="1.1" stroke-linecap="round"/></g>'
def T_FOOTER():
    pairs, P = make("ftft19e_", "UpKeep"); LOC = "UpKeep Board Footer"
    band = lambda cream: R(0, 0, 360, 170, CREAM if cream else WHITE) + (L(0, 0, 360, 0, TERRA, 2) if not cream else "") + fd(14, "Ping Record", 5, "3 active · 1 paused") + fd(48, "Routines", 0, "0 active") + L(14, 92, 346, 92, LINE) + mc(132, 104) + T(160, 120, "Built by Machan", 10, MUTE, 600)
    P("Footer band", LOC, "Footer ground", "asked another way since you left it to me: should the footer sit on a cream band like the header, or on white with a thin top line?",
      o("cream", "Cream Band", "Mirrors the header, as built.", "framed", "Footer ground", band(True)),
      o("white", "White, Thin Top Line", "Lighter end, one coloured line.", "light", "Footer ground", band(False)))
    sw = lambda c: "".join(T(14, 24 + i * 34, n, 10, INK, 600) + T(14, 36 + i * 34, s, 8.5, MUTE) + R(290, 12 + i * 34, 34, 18, c if on else "#cfc6b6", rx=9) + C(299 + (16 if on else 0), 21 + i * 34, 7, WHITE) + T(346, 25 + i * 34, "On" if on else "Paused", 8.5, MUTE, 600, "end") for i, (n, s, on) in enumerate((("Morning check", "Every day 7:00 AM", True), ("Ping sweep", "Every hour", True), ("Weekly recap", "Mondays 9:00 AM", False))))
    P("Routine switch", LOC, "On colour", "asked again in plain words: when a routine is running, should its switch glow green or lagoon blue?",
      o("jungle", "Green Means Running", "Jungle switch, as built.", "go", "Routine switch", sw(JUNGLE)),
      o("lagoon", "Lagoon Means Running", "A calmer blue switch.", "calm", "Routine switch", sw(LAGOON)))
    pl = lambda inrow: fd(0, "Ping Record", 5, "3 active · 1 paused" + (" · check not running" if inrow else ""), True, body=86) + (T(26, 44, "Ping check not running yet", 9, MUTE) if not inrow else "") + R(26, 52 if not inrow else 36, 308, 18, SOFT) + T(32, 64 if not inrow else 48, "RECEIVED   FROM   TYPE   STATUS", 7.5, MUTE, 700) + T(32, 84 if not inrow else 68, "3:55 PM   Tech Dash 3   Safety   Open", 9, INK)
    P("Ping schedule line", LOC, "Schedule line place", "asked again since you left it to me: should Ping check not running yet sit on its own line above the table or join the fold summary?",
      o("above", "Own Line Above The Table", "Kept apart, as built.", "clear", "Ping schedule line", pl(False)),
      o("inrow", "Joined To The Summary", "One line less, all in the title row.", "compact", "Ping schedule line", pl(True)))
    wk = lambda hop: mc(110, 40 if not hop else 28, 30, True) + T(150, 62, "Built by Machan", 12, INK, 600) + (f'<ellipse cx="125" cy="76" rx="11" ry="2.5" fill="#00000014"/>' + T(126, 22, "hop", 8, LAGOON, 700, "middle") if hop else "") + T(180, 110, "On hover", 9, MUTE, 500, "middle")
    P("Machan wink", LOC, "Wink extra", "with Machan winking on hover, should he also give one small hop?",
      o("wink", "Wink Only", "A wink and a small tilt, as built.", "subtle", "Machan on hover", wk(False)),
      o("hop", "Wink And A Small Hop", "One gentle bounce with the wink.", "playful", "Machan on hover", wk(True)))
    sp_ = lambda floating: R(0, 0, 360, 170, "#FBF6EC") + (T(14, 22, "← Back to the board", 10, LAGOON, 600) if not floating else R(250, 128, 98, 30, WHITE, LINE, 15) + T(299, 147, "← Board", 10, LAGOON, 600, "middle")) + T(180, 70, "The Machan Story", 18, INK, f="khand", anchor="middle") + mc(162, 80, 36)
    P("Story page", LOC, "Way back", "with the story page opening in the same tab, should the way back be a link at the top or a small floating button?",
      o("top", "Link At The Top", "Back to the board, top left.", "plain", "Machan story page", sp_(False)),
      o("float", "Floating Back Button", "Always in reach while you scroll.", "handy", "Machan story page", sp_(True)))
    pr = lambda resume: "".join(R(14, 6 + i * 34, 332, 30, WHITE) + T(24, 22 + i * 34, n, 10, INK, 600) + T(24, 32 + i * 34, s, 8, MUTE) + R(270, 12 + i * 34, 30, 16, JUNGLE if on else "#cfc6b6", rx=8) for i, (n, s, on) in enumerate((("Morning check", "Every day 7:00 AM", True),))) + f'<g opacity=".55">{T(24, 56, "Weekly recap", 10, INK, 600)}{T(24, 66, "Paused" + (" · back Mon 9:00 AM" if resume else ""), 8, MUTE)}{R(270, 46, 30, 16, "#cfc6b6", rx=8)}</g>'
    P("Paused routine", LOC, "Paused detail", "with a paused routine fading its row, should it also say when it comes back?",
      o("plain", "Faded Row, Paused", "Just faded, with the word Paused.", "quiet", "Paused routine", pr(False)),
      o("resume", "Faded Row, Back On Date", "Paused · back Mon 9:00 AM.", "informative", "Paused routine", pr(True)))
    cd = lambda clock: T(14, 26, "Morning check", 11, INK, 600) + chip(170, 14, "Next at 7:00 AM (in 9 hours)" if clock else "Next in 9 hours", LAGOON, "soft", 9)[0]
    P("Countdown", LOC, "Clock time too", "with the full Next in 2 hours wording, should it also give the clock time?",
      o("dur", "Next In 9 Hours", "How long only.", "short", "Countdown chip", cd(False)),
      o("clock", "Next At 7:00 AM (In 9 Hours)", "Clock time first, then how long.", "exact", "Countdown chip", cd(True)))
    rt = lambda clockbold: "".join(T(14, 22 + i * 26, a if clockbold else b, 10, INK, 700) + T(14 + (52 if clockbold else 70), 22 + i * 26, b if clockbold else a, 9, MUTE) + T(160, 22 + i * 26, s, 9.5, INK) for i, (a, b, s) in enumerate((("3:55 PM", "18 min ago", "Safety · Tech Dash 3"), ("3:30 PM", "43 min ago", "Stock check · Van 1"))))
    P("Received time", LOC, "Which time leads", "you liked both, so with clock time and how long ago together, which should be bold?",
      o("clock", "Clock Time Bold", "3:55 PM bold, 18 min ago grey.", "exact", "Received column", rt(True)),
      o("ago", "How Long Ago Bold", "18 min ago bold, 3:55 PM grey.", "urgent", "Received column", rt(False)))
    fl = lambda chips_: ("".join(T(14 + i * 110, 16, n, 8, MUTE) + R(14 + i * 110, 22, 100, 26, WHITE, LINE) + T(22 + i * 110, 39, "All", 9.5, INK) + chev(104 + i * 110, 35, INK) for i, n in enumerate(("Type", "Status", "Date"))) if not chips_ else "".join(chip(14 + x, 10 + r * 26, n, LAGOON if n in ("All", "Today") else MUTE, "solid" if n in ("All", "Today") else "outline", 9)[0] for r, row_ in enumerate(((0, "All"), (42, "Safety"), (100, "Stock check")), ) for x, n in [row_])) + (T(14, 80, "Status: All · New · Open · Done", 8.5, MUTE) + T(14, 96, "Date: Today · This week · This month", 8.5, MUTE) if chips_ else "")
    P("Ping filters", LOC, "Filter look", "with Type, Status and Date filters, should they be three small menus or rows of tap chips?",
      o("menus", "Three Small Menus", "Compact dropdowns, as built.", "compact", "Ping filters", fl(False)),
      o("chips", "Tap Chips", "One tap per choice, no menus.", "quick", "Ping filters", fl(True)))
    ms = lambda s: L(14, 10, 346, 10, LINE) + mc(180 - s / 2 - 50, 30 - s / 2 + 12, s) + T(180 - 50 + s / 2 + 6, 46, "Built by Machan", 11, MUTE, 600)
    P("Machan mark", LOC, "Mark size", "with the Machan mark beside the words, should it stay small or step up a size?",
      o("small", "Small Mark", "About the height of the words.", "neat", "Footer credit", ms(22)),
      o("bigger", "A Size Up", "Easier to see Machan's face.", "friendly", "Footer credit", ms(32)))
    return pairs
