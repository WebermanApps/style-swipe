"""UpKeep Operator Console Deck: the admin login where the person running UpKeep sees ALL member and tech info.
Desktop-first with a usable phone view. All names, numbers and reviews are EXAMPLE DATA; no real people."""
from uk5_art import *
PAIRS = []
def pair(g, ask, a, b): PAIRS.append((g, ask, a, b))
SC = 212 / 300
def desk(inner, h=300):
    return ('<clipPath id="dkc"><rect x="14" y="39" width="212" height="226"/></clipPath>' + rect(14, 30, 212, 9, "#EFEAE2") + dot(19, 34.5, 1.6, TERRA) + dot(24, 34.5, 1.6, SAFFRON) + dot(29, 34.5, 1.6, JUNGLE)
            + '<g clip-path="url(#dkc)">' + g(14, 39, round(SC, 4), rect(0, 0, 300, h, "#FFFFFF") + inner) + "</g>" + rect(14, 30, 212, 235, "none", "#BDB6AA", 0, 1))
def top(title="Company Dashboard", right="Today"):
    return t(10, 22, title, 17, INK, "khand") + rect(290 - len(right) * 6 - 12, 9, len(right) * 6 + 12, 18, "#FFFFFF", INK, 0, 1) + t(290 - (len(right) * 6 + 12) / 2, 22, right, 10, INK, "hind", 600, "middle") + ln(32, 0, 300)
def K(x, y, w, h, v, lb, c=INK, sp=None, sc=JUNGLE, big=20):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 0, 1) + t(x + 8, y + 14 + big * .7, v, big, c, "khand") + t(x + 8, y + h - 8, lb, 10, MUTE)
    if sp: s += spark(x + w * .55, y + 10, w * .38, h * .32, sp, sc)
    return s
def foot(items): return chips(272, items, 14)
MONEY = [("120", "Members", INK), ("$18.4k", "MRR", TERRA), ("1.8%", "Churn / mo", LAGOON)]
OPS = [("46", "Visits this week", INK), ("7", "Open jobs", TERRA), ("78%", "Tech utilization", JUNGLE)]
def kpi3(y, items, big=26, h=64):
    return "".join(K(10 + i * 96, y, 88, h, v, lb, c, big=big) for i, (v, lb, c) in enumerate(items))
def rows(y, items, cols, w=280):
    s = rect(10, y, w, 20, CREAM) + "".join(t(10 + x, y + 14, h, 10, INK, "hind", 600) for x, h in cols)
    for r, it in enumerate(items):
        yy = y + 20 + r * 24; s += ln(yy + 24, 10, 10 + w) + "".join(t(10 + cols[k][0], yy + 16, v, 10, INK if k == 0 else MUTE) for k, v in enumerate(it))
    return s
TREND = [80, 86, 90, 97, 103, 108, 114, 120]

def section(y, title, h=46, c=TERRA):
    return rect(10, y, 280, h, "#FFFFFF", LINE) + rect(10, y, 4, h, c) + t(20, y + 18, title, 12, INK, "khand") + rect(20, y + 26, 180, 5, "#E8E2D8") + rect(20, y + 35, 120, 5, "#EFEAE2")
def tabsrow(y, items, on):
    s, x = "", 10
    for i, lb in enumerate(items):
        w = len(lb) * 6.4 + 18; s += rect(x, y, w, 22, INK if i == on else "#FFFFFF", INK, 0, 1) + t(x + w / 2, y + 15, lb, 10, "#FFFFFF" if i == on else INK, "hind", 600, "middle"); x += w + 4
    return s
def alert(y, c, title, sub):
    return rect(10, y, 280, 34, c + "14", c, 0, 1) + rect(10, y, 4, 34, c) + icon("bell", 20, y + 9, 16, c, 2) + t(42, y + 15, title, 11, INK, "khand") + t(42, y + 28, sub, 9.5, MUTE)
def todo(y, items):
    s = rect(10, y, 280, 22 + len(items) * 26, "#FFFFFF", LINE) + t(18, y + 16, "To-Do List", 12, INK, "khand")
    for i, (it, done) in enumerate(items):
        yy = y + 24 + i * 26; s += rect(18, yy + 4, 13, 13, JUNGLE if done else "#FFFFFF", JUNGLE if done else "#BDB6AA", 0, 1.2) + (f'<path d="M21 {yy+10} l3 3 5 -6" fill="none" stroke="#FFFFFF" stroke-width="1.8"/>' if done else "") + t(38, yy + 15, it, 10.5, MUTE if done else INK)
    return s
def jobmap(y):
    s = rect(10, y, 280, 170, "#EEF2EA", LINE)
    s += f'<path d="M10 {y+60} Q120 {y+40} 290 {y+90} M60 {y} Q90 {y+90} 70 {y+170} M200 {y} L180 {y+170}" stroke="#FFFFFF" stroke-width="5" fill="none"/>' + f'<path d="M10 {y+130} Q150 {y+120} 290 {y+140}" stroke="#D9E2D1" stroke-width="3" fill="none"/>'
    for x, yy, c, n in [(60, 50, TERRA, "1"), (120, 90, LAGOON, "2"), (170, 40, JUNGLE, "3"), (230, 110, TERRA, "4"), (95, 140, SAFFRON, "5"), (250, 60, LAGOON, "6")]:
        s += f'<path d="M{x} {y+yy} q-9 -12 -9 -18 a9 9 0 0 1 18 0 q0 6 -9 18 z" fill="{c}"/>' + t(x, y + yy - 15, n, 9, "#FFFFFF", "hind", 700, "middle")
    s += rect(176, y + 136, 108, 28, "#FFFFFFEE", LINE) + t(184, y + 149, "Job 4 · Furnace tune-up", 9, INK, "hind", 600) + t(184, y + 160, "Tech A · 13:00 (example)", 8.5, MUTE)
    return s
def techcard(x, y, w, name, c, vals):
    s = rect(x, y, w, 186, "#FFFFFF", LINE) + rect(x, y, w, 4, c) + g(x + w / 2 - 15, y + 10, .3, person(polo=TERRA, hat="cap", skin=SKIN[["Tech A", "Tech B", "Tech C"].index(name)], shoe="athletic"))
    s += t(x + w / 2, y + 96, name, 13, INK, "khand", anchor="middle")
    for i, (lb, v) in enumerate(vals): s += ln(y + 104 + i * 20, x + 6, x + w - 6) + t(x + 6, y + 118 + i * 20, lb, 9, MUTE) + t(x + w - 6, y + 118 + i * 20, v, 9.5, c, "hind", 600, "end")
    return s
TV = {"Tech A": [("Visits", "18"), ("Busy", "82%"), ("On time", "95%"), ("Review", "4.9")], "Tech B": [("Visits", "15"), ("Busy", "74%"), ("On time", "88%"), ("Review", "4.7")], "Tech C": [("Visits", "13"), ("Busy", "71%"), ("On time", "97%"), ("Review", "4.8")]}
WEEK = [6, 8, 7, 9, 10, 6, 0]
def mob():
    return (rect(0, 0, 150, 300, "#FFFFFF") + t(8, 18, "Company", 13, INK, "khand") + "".join(K(8, 26 + i * 52, 134, 46, v, lb, c, big=20) for i, (v, lb, c) in enumerate([MONEY[0], MONEY[1], OPS[0], OPS[1]]))
            + alert_m(236))
def alert_m(y): return rect(8, y, 134, 30, TERRA + "14", TERRA, 0, 1) + t(14, y + 19, "2 visits running late", 10, INK, "hind", 600)
def quote(y, txt, who):
    return rect(10, y, 280, 50, "#FFFFFF", LINE) + "".join(icon("star", 18 + i * 12, y + 8, 10, SAFFRON) for i in range(5)) + t(18, y + 32, txt, 10.5, INK) + t(18, y + 44, who, 9, MUTE)
def alert2(y, c, title, sub, x=70, w=222):
    return rect(x, y, w, 34, c + "14", c, 0, 1) + rect(x, y, 4, 34, c) + icon("bell", x + 10, y + 9, 16, c, 2) + t(x + 32, y + 15, title, 11, INK, "khand") + t(x + 32, y + 28, sub, 9.5, MUTE)
def mtabs(x, y, items, on):
    o = ""; w = 222 / len(items)
    for i, lb in enumerate(items): o += rect(x + i * w, y, w, 20, INK if i == on else "#FFFFFF", INK, 0, 1) + t(x + i * w + w / 2, y + 14, lb, 8.5, "#FFFFFF" if i == on else INK, "hind", 600, "middle")
    return o
def todo2(x, y, w, items):
    o = rect(x, y, w, 24 + len(items) * 34, "#FFFFFF", LINE) + t(x + 6, y + 16, "To-Do List", 11, INK, "khand")
    for i, (it, done) in enumerate(items):
        yy = y + 24 + i * 34; o += rect(x + 6, yy + 4, 11, 11, JUNGLE if done else "#FFFFFF", JUNGLE if done else "#BDB6AA", 0, 1) + "".join(t(x + 22, yy + 13 + k * 10, ln_, 8.5, MUTE if done else INK) for k, ln_ in enumerate(it.split("|")))
    return o
NAV = ["Overview", "Members", "Techs", "Schedule", "Map", "Billing"]
def sidebar(on=1, w=62):
    o = rect(0, 0, w, 300, CREAM) + mark(14, 16, 7, "#FFFFFF", TERRA) + t(25, 20, "Console", 10, INK, "khand")
    for i, n in enumerate(NAV):
        y = 36 + i * 24; o += (rect(0, y, w, 22, "#FFFFFF") + rect(0, y, 3, 22, TERRA) if i == on else "") + t(9, y + 15, n, 9.5, INK if i == on else MUTE, "hind", 600)
    return o
def ctop(title, x=10, right="Example"):
    return t(x, 22, title, 15, INK, "khand") + rect(158, 9, 70, 18, "#FFFFFF", LINE) + t(164, 21, "Search", 9, GREY) + ln(32, 0, 238)
MEM = [("Member A", "Plus", "Paid", JUNGLE), ("Member B", "Essentials", "Due", SAFFRON), ("Member C", "Complete", "Paid", JUNGLE), ("Member D", "Plus", "Failed", TERRA), ("Member E", "Essentials", "Paid", JUNGLE), ("Member F", "Plus", "Paid", JUNGLE)]
def stat(x, y, txt, c):
    w = len(txt) * 5.6 + 10
    return rect(x, y, w, 13, c + "1F") + t(x + w / 2, y + 9.5, txt, 8, c, "hind", 600, "middle")
def mtable(x, y, w):
    wide = w >= 200
    cols = [(6, "Member")] + ([(72, "Plan")] if w > 150 else []) + ([(128, "Next visit")] if wide else []) + [(w - 44, "Billing")]
    o = rect(x, y, w, 18, CREAM) + "".join(t(x + dx, y + 13, h, 9, INK, "hind", 600) for dx, h in cols)
    for r, (n, pl, b, c) in enumerate(MEM):
        yy = y + 18 + r * 22; o += ln(yy + 22, x, x + w) + t(x + 6, yy + 15, n, 9.5, INK, "hind", 600) + (t(x + 72, yy + 15, pl, 9, MUTE) if wide or w > 150 else "") + (t(x + 120, yy + 15, f"Oct {20 + r}", 9, MUTE) if wide else "") + stat(x + w - 44, yy + 5, b, c)
    return o
def mcards(x, y, w):
    o = ""; cw = (w - 8) / 2
    for i, (n, pl, b, c) in enumerate(MEM[:4]):
        xx = x + (i % 2) * (cw + 8); yy = y + (i // 2) * 84
        o += rect(xx, yy, cw, 76, "#FFFFFF", LINE) + rect(xx + 6, yy + 6, 40, 30, CREAM) + g(xx + 11, yy + 11, .2, '<path d="M0 45 L50 0 L100 45 V100 H0 Z" fill="#FFFFFF" stroke="#0A0A0A" stroke-width="5"/><rect x="40" y="60" width="20" height="40" fill="' + TERRA + '"/>')
        o += t(xx + 52, yy + 18, n, 10.5, INK, "khand") + t(xx + 52, yy + 30, pl + " plan", 8.5, MUTE) + stat(xx + 6, yy + 44, b, c) + t(xx + 6, yy + 70, "Next visit Oct " + str(20 + i), 8.5, MUTE)
    return o
# 1 layout (lead)
pair("Layout", "Console Layout: A Left Sidebar Menu, Or Tabs Across The Top?",
 ("oc_sidebar", "Left Sidebar Menu", "Overview, Members, Techs, Schedule, Map, Billing down the left; room for more later.", "practical",
  card("Layout", TERRA, desk(sidebar(0) + g(62, 0, 1, ctop("Overview")) + "".join(K(70 + i * 76, 42, 70, 52, v, lb, c, big=17) for i, (v, lb, c) in enumerate([("120", "Members", INK), ("$18.4k", "MRR", TERRA), ("46", "Visits/wk", LAGOON)])) + alert2(102, TERRA, "2 visits running late", "Example: Tech B") + mtable(70, 146, 222)) + foot(["Desktop first", "Scales up"]), example=True)),
 ("oc_tabs", "Tabs Across The Top", "Same sections as tabs; full width for tables.", "calm",
  card("Layout", LAGOON, desk(ctop("Operator Console").replace('x="158"', 'x="220"').replace('x="164"', 'x="226"').replace('x2="238"', 'x2="300"') + tabsrow(38, ["Overview", "Members", "Techs", "Schedule", "Map"], 0) + kpi3(68, [("120", "Members", INK), ("$18.4k", "MRR", TERRA), ("46", "Visits/wk", LAGOON)], 20, 52) + mtable(10, 128, 280)) + foot(["Wide tables"]), example=True)))
# 2 member list vs cards
pair("Members", "All Members: A Sortable Table, Or Cards With A Home Thumbnail?",
 ("oc_mtable", "Sortable Table", "One row per member: plan, next visit, billing status; sort any column.", "practical",
  card("Members", INK, desk(sidebar(1) + g(62, 0, 1, ctop("Members")) + "".join(stat(70 + i * 60, 40, f, c) for i, (f, c) in enumerate([("All 120", INK), ("Due 4", SAFFRON), ("Failed 1", TERRA)])) + mtable(70, 60, 222)) + foot(["Scan many"]), example=True)),
 ("oc_mcards", "Member Cards", "Card per home with plan, billing tag and next visit.", "playful",
  card("Members", TERRA, desk(sidebar(1) + g(62, 0, 1, ctop("Members")) + mcards(70, 40, 222)) + foot(["Visual", "Fewer per screen"]), example=True)))
# 3 member detail
DET = [("Home Record", "3 bed, built 1960s (example)", LAGOON), ("Plan", "Plus, renews Mar (example)", TERRA), ("Visits", "Next Oct 21, last Jul 14", JUNGLE), ("Add-Ons", "Grass Cutting, Gutter Extra", SAFFRON), ("Billing", "Paid, card on file", JUNGLE)]
def dhead(y):
    return rect(70, y, 222, 40, CREAM) + t(78, y + 18, "Member A", 14, INK, "khand") + t(78, y + 31, "Example Home 1 · Plus plan", 8.5, MUTE) + stat(240, y + 13, "Paid", JUNGLE)
pair("Member Detail", "Member Detail: Tabs For Home Record, Plan, Visits, Add-Ons And Billing, Or One Scroll With Every Section?",
 ("oc_mdtabs", "Tabbed Detail", "Header with status, then a tab per area.", "calm",
  card("Member Detail", LAGOON, desk(sidebar(1) + g(62, 0, 1, ctop("Members › Member A")) + dhead(40) + mtabs(70, 86, ["Home", "Plan", "Visits", "Add-Ons", "Billing"], 2) + g(60, 0, 1, rows(114, [("Oct 21", "Fall visit", "Tech A"), ("Jul 14", "Summer visit", "Tech C"), ("Apr 9", "Spring visit", "Tech A"), ("Jan 12", "Winter visit", "Tech B")], [(8, "Date"), (60, "Visit"), (140, "Tech")], 222))) + foot(["Focused"]), example=True)),
 ("oc_mdscroll", "One Scroll, All Sections", "Home record, plan, visits, add-ons and billing stacked.", "practical",
  card("Member Detail", TERRA, desk(sidebar(1) + g(62, 0, 1, ctop("Members › Member A")) + dhead(40) + "".join(rect(70, 86 + i * 34, 222, 30, "#FFFFFF", LINE) + rect(70, 86 + i * 34, 3, 30, c) + t(78, 99 + i * 34, n, 10.5, INK, "khand") + t(78, 110 + i * 34, v, 8.5, MUTE) for i, (n, v, c) in enumerate(DET))) + foot(["See it all"]), example=True)))
# 4 tech roster + detail
def techdetail(x, y):
    o = rect(x, y, 152, 190, "#FFFFFF", LINE) + t(x + 8, y + 18, "Tech A · Today", 12, INK, "khand")
    for i, (tm, job, c) in enumerate([("09:00", "Gutter cleaning", JUNGLE), ("10:30", "Water heater flush", LAGOON), ("13:00", "Furnace tune-up", TERRA), ("15:30", "Moisture scan", SAFFRON)]):
        yy = y + 28 + i * 30; o += rect(x + 8, yy, 3, 24, c) + t(x + 16, yy + 10, tm, 8.5, MUTE) + t(x + 16, yy + 21, job, 9, INK, "hind", 600)
    return o + ln(y + 152, x, x + 152) + "".join(icon("star", x + 8 + i * 12, y + 160, 10, SAFFRON) for i in range(5)) + t(x + 72, y + 169, "4.9 (example)", 8.5, MUTE)
pair("Techs", "Tech Roster: Cards That Open A Detail Page, Or A Table With The Detail Beside It?",
 ("oc_tcards", "Roster Cards", "Card per tech: drawn avatar, visits, utilization, rating; tap for schedule and jobs.", "playful",
  card("Techs", JUNGLE, desk(sidebar(2) + g(62, 0, 1, ctop("Techs")) + "".join(techcard(70 + i * 75, 40, 70, n, c, TV[n][:3]) for i, (n, c) in enumerate([("Tech A", TERRA), ("Tech B", LAGOON), ("Tech C", JUNGLE)]))) + foot(["Personal"]), example=True)),
 ("oc_tsplit", "Table + Detail Beside", "Pick a row; today's schedule, jobs and ratings show on the right.", "practical",
  card("Techs", INK, desk(sidebar(2) + g(62, 0, 1, ctop("Techs")) + rect(70, 40, 66, 18, CREAM) + t(76, 53, "Tech", 9, INK, "hind", 600) + "".join(rect(70, 58 + i * 24, 66, 24, TERRA + "14" if i == 0 else "#FFFFFF", LINE) + t(76, 74 + i * 24, n, 9.5, INK, "hind", 600) for i, n in enumerate(["Tech A", "Tech B", "Tech C"])) + techdetail(140, 40)) + foot(["Fast compare"]), example=True)))
# 5 search & filters
def chipsrow(x, y, items):
    o = ""
    for lb, on in items:
        w = len(lb) * 5.4 + 14; o += rect(x, y, w, 18, INK if on else "#FFFFFF", INK, 0, 1) + t(x + w / 2, y + 12.5, lb, 8.5, "#FFFFFF" if on else INK, "hind", 600, "middle"); x += w + 4
    return o
pair("Search", "Search And Filters: One Search Bar With Filter Chips, Or A Filter Panel On The Left?",
 ("oc_searchchips", "Search Bar + Chips", "Search members, homes and techs in one box; chips narrow it.", "calm",
  card("Search And Filters", LAGOON, desk(sidebar(1) + rect(70, 10, 222, 22, "#FFFFFF", INK, 0, 1) + icon("search", 74, 13, 15, INK) + t(94, 25, "Search members, homes, techs", 9, GREY) + chipsrow(70, 40, [("Plus", True), ("Billing due", False), ("Oakland", False), ("Visit this week", True)]) + mtable(70, 66, 222)) + foot(["Quick"]), example=True)),
 ("oc_searchpanel", "Filter Panel", "Plan, billing, county, next visit and tech as checkboxes beside the list.", "practical",
  card("Search And Filters", TERRA, desk(sidebar(1) + rect(70, 10, 222, 22, "#FFFFFF", INK, 0, 1) + t(78, 25, "Search", 9, GREY) + rect(70, 40, 74, 200, CREAM) + "".join(t(76, 56 + i * 34, h, 9, INK, "hind", 600) + rect(76, 61 + i * 34, 8, 8, TERRA if i % 2 == 0 else "#FFFFFF", INK, 0, .8) + t(88, 68 + i * 34, v, 8.5, MUTE) for i, (h, v) in enumerate([("Plan", "Plus"), ("Billing", "Due"), ("County", "Wayne"), ("Visit", "This week"), ("Tech", "Any")])) + mtable(150, 40, 142)) + foot(["Precise"]), example=True)))
# 6 schedule
def weekgrid(x, y, w, h):
    o = ""; cw = w / 5
    for d, dn in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
        o += rect(x + d * cw, y, cw, h, "#FFFFFF", LINE) + t(x + d * cw + cw / 2, y + 12, dn, 9, INK, "hind", 600, "middle")
        for k in range(3 + d % 2):
            c = [TERRA, LAGOON, JUNGLE][(d + k) % 3]; o += rect(x + d * cw + 3, y + 20 + k * 34, cw - 6, 28, c + "26") + rect(x + d * cw + 3, y + 20 + k * 34, 2.5, 28, c) + t(x + d * cw + 8, y + 32 + k * 34, f"{9 + k * 2}:00", 8, INK, "hind", 600) + t(x + d * cw + 8, y + 43 + k * 34, ["Tech A", "Tech B", "Tech C"][(d + k) % 3], 7.5, MUTE)
    return o
def lanes(x, y, w):
    o = "".join(t(x + 40 + i * (w - 40) / 4, y + 10, h, 8, MUTE, "hind", 400, "middle") for i, h in enumerate(["9", "11", "13", "15"]))
    for r, (n, c) in enumerate([("Tech A", TERRA), ("Tech B", LAGOON), ("Tech C", JUNGLE)]):
        yy = y + 18 + r * 50; o += rect(x, yy, w, 44, "#FFFFFF", LINE) + t(x + 6, yy + 26, n, 9.5, INK, "hind", 600)
        for k, (s0, ln_) in enumerate([(0, .8), (1.1, .9), (2.3, 1)]):
            o += rect(x + 46 + s0 * (w - 50) / 4, yy + 8, ln_ * (w - 50) / 4, 28, c + "30") + rect(x + 46 + s0 * (w - 50) / 4, yy + 8, 2.5, 28, c)
    return o
pair("Schedule", "All Visits: A Week Calendar, Or A Day Timeline With One Lane Per Tech?",
 ("oc_week", "Week Calendar", "Every visit this week by day; color by tech.", "calm",
  card("Schedule", LAGOON, desk(sidebar(3) + g(62, 0, 1, ctop("Schedule")) + weekgrid(70, 40, 222, 180)) + foot(["Plan the week"]), example=True)),
 ("oc_lanes", "Day Timeline By Tech", "Each tech's day as a lane; gaps and overlaps jump out.", "practical",
  card("Schedule", TERRA, desk(sidebar(3) + g(62, 0, 1, ctop("Schedule · Today")) + lanes(70, 40, 222)) + foot(["Run the day"]), example=True)))
# 7 map
pair("Map", "Jobs Map: Map Beside A Job List, Or A Full Map With Each Tech's Route Drawn?",
 ("oc_mapsplit", "Map + Job List", "List on the left, pins on the right; tap a row to find the pin.", "practical",
  card("Map Of Jobs", JUNGLE, desk(sidebar(4) + g(62, 0, 1, ctop("Map")) + g(60, 0, 1, rows(40, [("09:00", "Tech A"), ("10:30", "Tech B"), ("13:00", "Tech A"), ("14:00", "Tech B"), ("15:30", "Tech C")], [(8, "Time"), (46, "Tech")], 86)) + g(160, 40, .45, jobmap(0)).replace("", "") ) + foot(["Find a job"]), example=True)),
 ("oc_maproutes", "Full Map With Routes", "Whole area with dashed routes per tech in their color.", "bold",
  card("Map Of Jobs", TERRA, desk(sidebar(4) + g(62, 0, 1, ctop("Map")) + g(65, 34, .78, jobmap(0) + f'<path d="M60 50 L120 90 L95 140" fill="none" stroke="{TERRA}" stroke-width="2.5" stroke-dasharray="6 4"/><path d="M170 40 L250 60 L230 110" fill="none" stroke="{LAGOON}" stroke-width="2.5" stroke-dasharray="6 4"/>') + t(70, 250, "Map is illustrative; routes are example.", 9, MUTE)) + foot(["See routes"]), example=True)))
# 8 alerts / to-do
pair("Alerts", "Needs Attention: Alert Banners Above Everything, Or A To-Do Panel On The Right?",
 ("oc_alerts", "Alert Banners On Top", "Failed payments, late visits and low stock in color, first thing.", "bold",
  card("Alerts And To-Do", TERRA, desk(sidebar(0) + alert2(10, TERRA, "1 payment failed", "Example: Member D") + alert2(48, SAFFRON, "2 visits running late", "Example: Tech B") + alert2(86, LAGOON, "3 renewals this week", "Example") + mtable(70, 128, 222)) + foot(["Can't miss it"]), example=True)),
 ("oc_todo", "To-Do Panel", "Checklist on the right; tick items off as you handle them.", "practical",
  card("Alerts And To-Do", JUNGLE, desk(sidebar(0) + t(70, 22, "Overview", 15, INK, "khand") + mtable(68, 40, 120) + todo2(194, 40, 98, [("Retry Member D|card", False), ("Call about late|visits", False), ("Restock Van 2|filters", False), ("Approve Tech C|hours", True)])) + foot(["Get it done"]), example=True)))
# 9 KPI strip
pair("KPI Strip", "Top KPI Strip: Five Business Numbers, Or Three Big Numbers With A Trend?",
 ("oc_kpi5", "Five Numbers", "Members, MRR, churn, visits this week, open jobs.", "practical",
  card("KPI Strip", INK, desk(sidebar(0) + "".join(K(68 + i * 45, 10, 42, 52, v, lb, c, big=13) for i, (v, lb, c) in enumerate([("120", "Members", INK), ("$18k", "MRR", TERRA), ("1.8%", "Churn", LAGOON), ("46", "Visits", JUNGLE), ("7", "Jobs", SAFFRON)])) + mtable(68, 72, 224)) + foot(["Everything"]), example=True)),
 ("oc_kpi3", "Three Big + Trend", "Members, MRR and visits, each with an 8-week sparkline.", "calm",
  card("KPI Strip", LAGOON, desk(sidebar(0) + "".join(K(68 + i * 75, 10, 70, 60, v, lb, c, sp=sp, sc=c if c != INK else JUNGLE, big=17) for i, ((v, lb, c), sp) in enumerate(zip([("120", "Members", INK), ("$18.4k", "MRR", TERRA), ("46", "Visits/wk", LAGOON)], [TREND, [12, 13, 14, 15, 16, 17, 18, 18.4], [38, 42, 40, 44, 41, 45, 43, 46]]))) + mtable(68, 80, 224)) + foot(["Readable"]), example=True)))
# 10 phone view (desktop-first, usable phone)
def phone_cards():
    return rect(0, 0, 150, 300, "#FFFFFF") + t(8, 18, "Console", 13, INK, "khand") + "".join(K(8 + (i % 2) * 69, 26 + (i // 2) * 48, 65, 42, v, lb, c, big=15) for i, (v, lb, c) in enumerate([("120", "Members", INK), ("$18k", "MRR", TERRA), ("2", "Late", TERRA), ("7", "Jobs", LAGOON)])) + alert_m(126) + "".join(rect(8, 162 + i * 28, 134, 24, "#FFFFFF", LINE) + t(14, 178 + i * 28, n, 9.5, INK, "hind", 600) + stat(100, 168 + i * 28, b, c) for i, (n, pl, b, c) in enumerate(MEM[:4]))
def phone_tabs():
    return rect(0, 0, 150, 300, "#FFFFFF") + t(8, 18, "Members", 13, INK, "khand") + rect(8, 26, 134, 18, "#FFFFFF", INK, 0, 1) + t(14, 38, "Search", 8.5, GREY) + "".join(rect(8, 50 + i * 30, 134, 26, "#FFFFFF", LINE) + t(14, 67 + i * 30, n, 9.5, INK, "hind", 600) + stat(100, 56 + i * 30, b, c) for i, (n, pl, b, c) in enumerate(MEM)) + rect(0, 262, 150, 38, CREAM) + "".join(icon(k, 12 + i * 34, 268, 14, TERRA if i == 1 else MUTE) for i, k in enumerate(["cal", "list", "id", "map"])) + "".join(t(19 + i * 34, 292, lb, 7, TERRA if i == 1 else MUTE, "hind", 600, "middle") for i, lb in enumerate(["Today", "Members", "Techs", "Map"]))
def phfr(inner, c):
    return rect(14, 30, 212, 236, CREAM) + rect(76, 36, 88, 224, INK) + g(80, 44, round(80 / 150, 4), inner) + rect(108, 39, 24, 2.5, "#555")
pair("Phone View", "Phone View Of The Console: A Summary Home Screen, Or Bottom Tabs That Mirror The Desktop Menu?",
 ("oc_phonehome", "Summary Home Screen", "Phone opens on KPIs, alerts and members needing attention.", "practical",
  card("Phone View", TERRA, phfr(phone_cards(), TERRA) + foot(["Check on the go"]), example=True)),
 ("oc_phonetabs", "Bottom Tabs", "Today, Members, Techs, Map tabs, same as the desktop sidebar.", "calm",
  card("Phone View", LAGOON, phfr(phone_tabs(), LAGOON) + foot(["Full console"]), example=True)))
