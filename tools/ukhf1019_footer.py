"""UpKeep Board Footer Deck (Oct 19 2026, Max via UpKeep Develop 12:02 ICT; decided 12:07 ICT: Emergency Alerts, pings-as-alerts,
To-Do and Documents live in the header; the footer holds the Ping Record with its ping schedule, Routines and the footer finish).
Members board example, 20 this-or-that pairs. Invented SAMPLE data only."""
from md1018_kit import make
from ukhf1019_kit import *
PINGS = [("Oct 19, 11:42", "18 min ago", "SAMPLE Member A", "Message", "Asks to move the fall visit a week later, mornings only", None, "TEST", "New", None),
         ("Oct 19, 10:15", "2 hr ago", "Tech Dash 2", "Alert", "Gas smell at SAMPLE home A, tech on site, member out", "Safety", "TEST", "Open", "10:20 AM"),
         ("Oct 19, 9:30", "3 hr ago", "Scheduling Agent", "Ping", "Sign-up forecast for next week is ready to review", None, "Forecast", "Seen", None),
         ("Oct 19, 8:05", "4 hr ago", "SAMPLE Member B", "Message", "Water heater leaking in the basement since last night", "Urgent", "TEST", "Open", "8:10 AM"),
         ("Oct 18, 4:40", "Yesterday", "Members Agent", "Ping", "Welcome message wording approved and pinned", None, "Decided", "Done", "4:45 PM")]
ROUT = [("Morning Report", "Reports", "Daily 5:00 AM ICT", True, "Tomorrow 5:00 AM", "in 17 hr", "Today 5:00 AM"),
        ("Ping check", "Pings", "Every 30 min", True, "Today 12:30 PM", "in 27 min", "Today 12:00 PM"),
        ("Urgent ping relay to Ethan", "Pings", "On urgent or safety ping", True, "On event", "on event", "Today 10:20 AM"),
        ("New sign-up welcome", "Members", "On sign-up", True, "On sign-up", "on event", "Oct 18"),
        ("Renewal reminders", "Members", "Mondays 9:00 AM ICT", False, "Paused", "paused", "Oct 12")]
STC = {"New": LAGOON, "Open": TERRA, "Seen": MUTE, "Done": JUNGLE}
def trunc(s, n): return s if len(s) <= n else s[:n - 1].rstrip() + "..."
def flagmark(x, y, f, style):
    if not f: return ""
    if style == "edge": return chip(x, y - 10, f.upper(), TERRA, "solid", 7.5)[0]
    return warn(x, y - 10, TERRA, 11) + T(x + 14, y, f, 9, TERRA, 700)
def status(x, y, s, style):
    if style == "dot": return chip(x, y - 10, s, STC[s], "dot", 8.5)[0]
    steps = ["New", "Seen", "Done"]; k = {"New": 0, "Open": 1, "Seen": 1, "Done": 2}[s]
    return "".join(R(x + i * 11, y - 6, 9, 5, STC[s] if i <= k else "#E2DACB", rx=2) for i in range(3)) + T(x + 36, y, s, 8.5, INK, 500)
def reported(x, y, r, style):
    if style == "check": return (checkc(x + 6, y - 3, JUNGLE, 5.5) if r else T(x + 6, y, "-", 9, MUTE, anchor="middle"))
    return chip(x, y - 10, "Sent " + r, JUNGLE, "soft", 7.5)[0] if r else T(x, y, "Not sent", 8.5, MUTE)
def ping_title(y, open_, body, head="count", flags=2):
    if head == "count": return fold(y, "Ping Record", len(PINGS), open_, body)
    return fold(y, "Ping Record", None, open_, body, badge=len(PINGS), bcol=LAGOON, right=f"5 today  ·  {flags} urgent or safety  ·  3 reported to Ethan", rcol=INK)
def sched_line(y, kind):
    if kind == "line": return T(24, y + 11, "Ping schedule: checks every 30 min  ·  last 12:00 PM  ·  next 12:30 PM ICT", 9, MUTE, 500), 18
    g = T(24, y + 10, "PING SCHEDULE TODAY", 8, MUTE, 700, extra='letter-spacing="1"') + L(130, y + 7, 428, y + 7, "#D9D1C3", 2)
    for i in range(13):
        x = 130 + i * 24.8; g += L(x, y + 3, x, y + 11, JUNGLE if i < 8 else "#CFC6B6", 1.4)
    g += C(130 + 8 * 24.8, y + 7, 3.5, LAGOON) + T(130 + 8 * 24.8, y + 22, "next 12:30 PM", 7.5, LAGOON, 600, "middle")
    return g, 28
def ping_table(y, o):
    cols = ("Received", "From", "Type", "Summary", "Flag", "Label", "Status", "Ethan")
    xs = (22, 82, 152, 190, 300, 340, 380, 416)
    g = R(14, y, 424, 18, SOFT) + "".join(T(x, y + 12.5, c.upper(), 7, MUTE, 700, extra='letter-spacing=".6"') for x, c in zip(xs, cols)); yy = y + 18
    rh = 22 if o.get("summary", "one") == "one" else 32
    rows = sorted(PINGS, key=lambda p: p[5] is None) if o.get("top") else PINGS
    for p in rows:
        if p[5] and o.get("flag", "edge") == "edge": g += R(14, yy, 424, rh, TERRA + "0F") + R(14, yy, 3, rh, TERRA)
        tm = p[0].split(", ")[1] if o.get("time", "clock") == "clock" else p[1]
        g += T(xs[0], yy + 14, tm, 8.5, INK, 500) + T(xs[1], yy + 14, trunc(p[2], 14), 8.5, INK, 600) + T(xs[2], yy + 14, p[3], 8.5, MUTE)
        if rh == 22: g += T(xs[3], yy + 14, trunc(p[4], 24), 8.5, INK)
        else: g += T(xs[3], yy + 12, trunc(p[4][:26], 26), 8.5, INK) + T(xs[3], yy + 24, trunc(p[4][26:].strip(), 26), 8.5, INK)
        g += flagmark(xs[4], yy + 14, p[5], o.get("flag", "edge")) + lab_chip(xs[5], yy + 4, p[6], o.get("label", "soft"), 7)[0]
        g += status(xs[6], yy + 14, p[7], o.get("status", "dot")) + reported(xs[7], yy + 14, p[8], "check") + L(14, yy + rh, 438, yy + rh); yy += rh
    return g, yy - y
def ping_cards(y, o):
    g = ""; yy = y
    for p in PINGS[:4]:
        g += R(22, yy, 408, 40, WHITE, LINE, 6) + (R(22, yy, 4, 40, TERRA, rx=2) if p[5] else "")
        g += T(34, yy + 14, f"{p[0].split(', ')[1]}  ·  {p[2]}  ·  {p[3]}", 8.5, MUTE, 500) + T(34, yy + 30, trunc(p[4], 52), 10, INK, 600)
        x = 300
        if p[5]: g += flagmark(x, yy + 18, p[5], "edge"); x += 50
        g += lab_chip(x, yy + 8, p[6], o.get("label", "soft"), 7)[0] + status(x, yy + 33, p[7], "dot") + reported(366, yy + 18, p[8], o.get("rep", "chip")); yy += 46
    return g, yy - y
def ping_tl(y, o):
    g = L(40, y + 4, 40, y + 4 + 4 * 42, LAGOON + "66", 2); yy = y
    for p in PINGS[:4]:
        c = TERRA if p[5] else LAGOON
        g += C(40, yy + 12, 5.5, c if p[5] else WHITE, c, 2) + T(54, yy + 11, f"{p[0].split(', ')[1]}  ·  {p[2]}", 8.5, MUTE, 600) + T(54, yy + 26, trunc(p[4], 50), 10, INK, 600)
        x = 300
        if p[5]: g += flagmark(x, yy + 14, p[5], "edge"); x += 50
        g += lab_chip(x, yy + 4, p[6], o.get("label", "soft"), 7)[0] + status(x, yy + 28, p[7], "dot") + reported(388, yy + 14, p[8], "check"); yy += 42
    return g, yy - y
def filters(y, kind):
    if kind == "chips":
        x = 24; g = ""
        for i, s in enumerate(("All", "Urgent or safety", "TEST", "Forecast", "Decided", "Not reported")):
            gg, w = chip(x, y, s, LAGOON if i == 0 else MUTE, "solid" if i == 0 else "outline", 8.5); g += gg; x += w + 5
        return g, 24
    g = ""; x = 24
    for s in ("Type: Any", "Flag: Any", "Label: Any", "Status: Any"):
        g += R(x, y, 90, 18, WHITE, "#CFC6B6", 3) + T(x + 8, y + 12.5, s, 8.5, INK, 500) + chev(x + 80, y + 9); x += 98
    return g, 24
def ping(y, o=None, open_=True):
    o = o or {}
    if not open_: return ping_title(y, False, 0, o.get("head", "count")), 30
    if o.get("empty"):
        if o["empty"] == "quiet": return fold(y, "Ping Record", 0, True, 26) + T(24, y + 41, "No pings received yet.", 10, MUTE), 58
        return (fold(y, "Ping Record", 0, True, 62) + R(24, y + 32, 404, 48, WHITE, "#B9AE9C", 6, 1.2, 'stroke-dasharray="4 3"') + checkc(42, y + 56, LAGOON, 9)
                + T(60, y + 52, "No pings yet", 12, INK, f="khand") + T(60, y + 66, "Messages, alerts and agent pings land here with time, label and status.", 8.5, MUTE)), 94
    s, sh = sched_line(y + 28, o.get("sched", "line")); inner = s; yy = y + 28 + sh
    if o.get("filters"): f, fh = filters(yy, o["filters"]); inner += f; yy += fh
    lay = o.get("layout", "table")
    b, bh = {"table": ping_table, "cards": ping_cards, "timeline": ping_tl}[lay](yy if lay == "table" else yy + 2, o); inner += b; yy += bh + 6
    return ping_title(y, True, yy - y - 24, o.get("head", "count")) + inner, yy - y + 6
def act(x, y, on, style):
    if style == "pill": return chip(x, y, "Active" if on else "Paused", JUNGLE if on else MUTE, "solid" if on else "outline", 8)[0]
    g = R(x, y, 24, 13, JUNGLE if on else "#D6D0C6", rx=6.5) + C(x + (17.5 if on else 6.5), y + 6.5, 5, WHITE)
    return g + T(x + 30, y + 10, "On" if on else "Paused", 8.5, JUNGLE if on else MUTE, 600)
def nxt(x, y, r, style):
    if style == "text": return T(x, y, "Next: " + r[4], 8.5, INK, 500, "end")
    return chip(x - 62, y - 10, r[5], LAGOON if r[3] else MUTE, "soft", 7.5)[0]
def routines(y, o=None, open_=True):
    o = o or {}; n_on = sum(r[3] for r in ROUT)
    right = f"{n_on} active  ·  {len(ROUT)-n_on} paused" if o.get("sum", "text") == "text" else None
    if not open_: return fold(y, "Routines", len(ROUT), False, right=right), 30
    yy = y + 28; inner = ""
    if o.get("sum") == "bar":
        inner += R(24, yy + 4, 300, 7, "#E2DACB", rx=3.5) + R(24, yy + 4, 300 * n_on / len(ROUT), 7, JUNGLE, rx=3.5) + T(334, yy + 11, f"{n_on} of {len(ROUT)} active", 9, JUNGLE, 700); yy += 20
    groups = [("Reports", [r for r in ROUT if r[1] == "Reports"]), ("Pings", [r for r in ROUT if r[1] == "Pings"]), ("Members", [r for r in ROUT if r[1] == "Members"])] if o.get("group") else [("", ROUT)]
    if o.get("style", "list") == "cards":
        x, row = 24, 0; cw = 130
        for r in ROUT:
            inner += R(x, yy, cw, 66, WHITE, LINE, 6) + R(x, yy, cw, 3, JUNGLE if r[3] else "#CFC6B6") + T(x + 8, yy + 18, trunc(r[0], 22), 10.5, INK, f="khand") + T(x + 8, yy + 31, trunc(r[2], 24), 8, MUTE)
            inner += act(x + 8, yy + 37, r[3], o.get("chip", "pill")) + T(x + 8, yy + 61, trunc("Next: " + r[4], 26), 7.5, INK, 500); x += cw + 7
            if x + cw > 432: x = 24; yy += 72
        if x != 24: yy += 72
    else:
        for gname, rs in groups:
            if gname: inner += T(24, yy + 10, gname.upper(), 8, JUNGLE, 700, extra='letter-spacing="1"') + L(24, yy + 14, 428, yy + 14, JUNGLE + "55"); yy += 18
            for r in rs:
                inner += T(24, yy + 13, r[0], 10, INK, 600) + T(170, yy + 13, r[2], 8.5, MUTE) + act(276, yy + 3, r[3], o.get("chip", "pill")) + nxt(428, yy + 13, r, o.get("next", "text")) + L(24, yy + 20, 428, yy + 20); yy += 22
    yy += 4
    return fold(y, "Routines", len(ROUT), True, yy - y - 24, right=right) + inner, yy - y + 6
def finish(y, built="center", share="right", div="tri"):
    g = (tri(y, h=1.6) if div == "tri" else L(14, y, 438, y, "#B9AE9C", 1.2, 'stroke-dasharray="1.5 3"' if div == "dot" else ""))
    if share == "right":
        g += R(372, y + 10, 66, 22, WHITE, INK, 0, 1.2) + share_ic(374, y + 9) + T(416, y + 25.5, "Share", 10.5, INK, f="khand", anchor="middle")
    elif share == "center":
        g += R(186, y + 10, 80, 22, WHITE, INK, 0, 1.2) + share_ic(194, y + 9) + T(238, y + 25.5, "Share board", 10.5, INK, f="khand", anchor="middle"); y += 28
    if built == "center": g += T(226 if share != "right" else 196, y + 26, "Built by Machan", 9.5, MUTE, 500, "middle")
    else: g += mark(14, y + 9, 22) + T(42, y + 21, "Built by Machan", 10, INK, f="khand") + T(42, y + 31, "Smart Upkeep  ·  Members board  ·  SAMPLE", 7.5, MUTE)
    return g
def board(p=None, r=None, f=None, popen=True, ropen=False):
    g = T(14, 14, "...board sections above (SAMPLE)", 8.5, MUTE, 500) + f'<g opacity=".45">{fold(20, "Members Catalog")}</g>'; y = 52
    s, h = ping(y, p, popen); g += s; y += h
    s, h = routines(y, r, ropen); g += s; y += h
    return g + finish(max(y + 6, 404), **(f or {}))
def T_FOOTER():
    pairs, P = make("ukft19_", "UpKeep"); F = frame; LOC = "UpKeep Board Footer"
    P("Ping Record", LOC, "Ping Record layout", "should the Ping Record be a table with columns or a stack of cards?",
      ("table", "Table With Columns", "Received, From, Type, Summary, Flag, Label, Status, Ethan.", "focused", F(board({"layout": "table"}), "Table")),
      ("cards", "Stacked Cards", "One card per ping, chips on the right.", "friendly", F(board({"layout": "cards"}), "Stacked cards")))
    P("Ping Record", LOC, "Ping Record timeline", "should the Ping Record read as a table or as a timeline down a line?",
      ("table", "Table", "Tidy rows that scan fast.", "focused", F(board({"layout": "table"}), "Table")),
      ("tl", "Timeline", "Dots down a lagoon line, newest at the top.", "calm", F(board({"layout": "timeline"}), "Timeline")))
    P("Ping Record", LOC, "Fold title", "should the closed Ping Record fold show just a count or a count with urgent and reported numbers?",
      ("count", "Count In Brackets", "Ping Record (5), like the dashboard folds.", "consistent", F(board({"head": "count"}, popen=False, ropen=True), "Count only")),
      ("sum", "Count Plus Summary", "5 today, 2 urgent or safety, 3 reported to Ethan.", "informative", F(board({"head": "sum"}, popen=False, ropen=True), "Count and summary")))
    P("Ping Record", LOC, "Ping schedule", "should the ping schedule be one line of text or a small strip of today's checks?",
      ("line", "One Line Of Text", "Checks every 30 min, last and next time.", "calm", F(board({"sched": "line"}), "Schedule line")),
      ("strip", "Strip Of Checks", "Tick marks for today's checks, next one marked.", "visual", F(board({"sched": "strip"}), "Schedule strip")))
    P("Ping Record", LOC, "Urgent and safety flag", "should urgent and safety pings get a tinted row with a solid tag or a warning sign with the word?",
      ("edge", "Tinted Row And Solid Tag", "Terracotta edge, pale tint and a SAFETY or URGENT tag.", "bold", F(board({"flag": "edge"}), "Tinted row, tag")),
      ("icon", "Warning Sign And Word", "A small warning sign and the word, no row tint.", "subtle", F(board({"flag": "icon"}), "Warning sign")))
    P("Ping Record", LOC, "Urgent ping order", "should urgent and safety pings be pinned to the top or stay in time order?",
      ("top", "Pinned To The Top", "Urgent and safety first, then the rest by time.", "safe", F(board({"top": True}), "Urgent on top")),
      ("time", "Plain Time Order", "Newest first, flags shown where they fall.", "honest", F(board({"top": False}), "Time order")))
    P("Ping Record", LOC, "Label chips", "should the TEST, Forecast and Decided labels be soft pills or outlined capital tags?",
      ("soft", "Soft Pills", "Pale tinted pills in grey, lagoon and jungle.", "friendly", F(board({"label": "soft"}), "Soft pills")),
      ("caps", "Outlined Capital Tags", "Small boxed capitals, like a stamp.", "formal", F(board({"label": "caps"}), "Outlined tags")))
    P("Ping Record", LOC, "Status display", "should a ping's status be a dot and word or a short three-step bar?",
      ("dot", "Dot And Word", "A coloured dot beside New, Open, Seen or Done.", "subtle", F(board({"status": "dot"}), "Dot and word")),
      ("step", "Three-Step Bar", "Three little blocks filling from New to Done.", "guided", F(board({"status": "step"}), "Three-step bar")))
    P("Ping Record", LOC, "Reported to Ethan", "should Reported to Ethan be a check mark column or a chip with the time it was sent?",
      ("check", "Check Mark Column", "A green check when reported, a dash when not.", "compact", F(board({"layout": "timeline"}), "Check mark")),
      ("chip", "Sent Time Chip", "A green Sent 10:20 AM chip, or Not sent.", "clear", F(board({"layout": "cards", "rep": "chip"}), "Sent time chip")))
    P("Ping Record", LOC, "Filters", "should the Ping Record filter with a row of chips or with small dropdown menus?",
      ("chips", "Row Of Chips", "All, Urgent or safety, TEST, Forecast, Decided, Not reported.", "quick", F(board({"filters": "chips"}), "Filter chips")),
      ("menus", "Dropdown Menus", "Type, Flag, Label and Status menus.", "tidy", F(board({"filters": "menus"}), "Filter menus")))
    P("Ping Record", LOC, "Received time", "should received time show as a clock time or as how long ago?",
      ("clock", "Clock Time", "11:42, 10:15, with the date in the day header.", "precise", F(board({"time": "clock"}), "Clock time")),
      ("ago", "How Long Ago", "18 min ago, 2 hr ago, Yesterday.", "casual", F(board({"time": "ago"}), "Time ago")))
    P("Ping Record", LOC, "Empty Ping Record", "with no pings yet, should the fold show one quiet line or a dashed card that explains it?",
      ("quiet", "One Quiet Line", "No pings received yet, in grey.", "calm", F(board({"empty": "quiet"}, ropen=True), "Quiet line")),
      ("card", "Dashed Explainer Card", "A dashed card saying what lands here.", "guided", F(board({"empty": "card"}, ropen=True), "Dashed card")))
    def RB(note, **o): return F(board(None, o, popen=False, ropen=True), note)
    P("Routines", LOC, "Routines layout", "should routines show as a fold list of rows or as small cards?",
      ("list", "Fold List Of Rows", "Name, schedule, active chip and next run per row.", "tidy", RB("Fold list")),
      ("cards", "Small Cards", "One card per routine, wrapping across.", "visual", RB("Routine cards", style="cards")))
    P("Routines", LOC, "Active and paused", "should a routine's state be an Active or Paused pill or a small on-off switch?",
      ("pill", "Active Or Paused Pill", "Solid green Active, outlined Paused.", "clear", RB("Pill", chip="pill")),
      ("toggle", "On-Off Switch Look", "A switch shape with On or Paused beside it.", "familiar", RB("Switch look", chip="toggle")))
    P("Routines", LOC, "Next run", "should the next run read as a time or as a countdown chip?",
      ("text", "Next Run Time", "Next: Today 12:30 PM, in plain text.", "precise", RB("Next run time", next="text")),
      ("count", "Countdown Chip", "A small chip: in 27 min, in 17 hr, on event.", "glanceable", RB("Countdown chip", next="count")))
    P("Routines", LOC, "Routines count", "should the routines count be words in the fold title or a small active bar inside?",
      ("text", "Words In The Fold Title", "4 active, 1 paused, on the right of the fold.", "calm", RB("Count words", sum="text")),
      ("bar", "Small Active Bar", "A jungle bar showing 4 of 5 active.", "visual", RB("Active bar", sum="bar")))
    P("Routines", LOC, "Routine grouping", "should routines be grouped by what they do or listed flat?",
      ("group", "Grouped By Kind", "Reports, Pings and Members headers.", "guided", RB("Grouped", group=True)),
      ("flat", "One Flat List", "All routines in one list.", "simple", RB("Flat list")))
    FB = lambda note, **o: F(board(None, None, o, popen=False, ropen=True), note)
    P("Footer finish", LOC, "Built by Machan line", "should Built by Machan be a small centred grey line or sit left with the house mark?",
      ("center", "Small Centred Line", "Built by Machan in grey, centred.", "quiet", FB("Centred line", built="center", share="center")),
      ("mark", "Left With House Mark", "The UP mark, Built by Machan and a small board line.", "branded", FB("With house mark", built="mark", share="right")))
    P("Footer finish", LOC, "Share button", "should the Share button sit at the right of the footer line or centred above Built by Machan?",
      ("right", "Right Of The Footer Line", "Share on the right, credit on the left.", "tidy", FB("Share at right", built="mark", share="right")),
      ("center", "Centred Above The Credit", "A centred Share board button, credit under it.", "balanced", FB("Share centred", built="center", share="center")))
    P("Footer finish", LOC, "Divider style", "should the footer start with a thin three-colour line or a dotted grey rule?",
      ("tri", "Three-Colour Line", "Terracotta, lagoon and jungle, thin.", "branded", FB("Three-colour line", div="tri", built="mark")),
      ("dot", "Dotted Grey Rule", "A light dotted rule, nothing coloured.", "quiet", FB("Dotted rule", div="dot", built="mark")))
    return pairs
