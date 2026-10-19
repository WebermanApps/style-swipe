"""UpKeep Board Header Deck (Oct 19 2026, Max via UpKeep Develop 12:02 ICT; header blocks added 12:06, decided 12:07):
every mockup shows the branded header plus Emergency Alerts (pings and flags), To-Do List and Documents Center, Members board example.
20 this-or-that pairs. Invented SAMPLE data only."""
from md1018_kit import make
from ukhf1019_kit import *
TITLE = "Members Command Center"; SUB = "Sign-ups, renewals and member messages for Smart Upkeep."
ALERTS = [("Gas", "Gas smell reported at SAMPLE home A", "Tech Dash 2", "10:15 AM"),
          ("Flooding", "Water in basement at SAMPLE home B", "SAMPLE member", "9:40 AM"),
          ("Electrical", "Sparking outlet at SAMPLE home C", "SAMPLE member", "9:02 AM"),
          ("CO", "CO alarm sounding at SAMPLE home D", "Tech Dash 1", "8:30 AM")]
TODO = [("Review welcome message draft", "From Max", "Today", "TEST", False),
        ("Call back SAMPLE member about renewal", "From Ethan", "Oct 21", "Forecast", False),
        ("Pin the member FAQ for approval", "From Members Agent", "Oct 22", "Decided", True)]
DOCS = [("DOC", "Welcome Message", "draft", "Oct 19", LAGOON), ("DECK", "Welcome Flow Deck", "approval", "Oct 19", TERRA),
        ("DOC", "Member FAQ", "approved", "Oct 17", JUNGLE), ("SHEET", "Renewal Notes", "draft", "Oct 16", LAGOON)]
CHIPTXT = {"draft": "DRAFT, NEEDS APPROVAL", "approval": "FOR APPROVAL", "approved": "APPROVED"}
CHIPC = {"draft": TERRA, "approval": TERRA, "approved": JUNGLE}
def header(y=0, ms=40, mpos="left", tstyle="mixed", accent="rule", back="pill", idc=None, status=None, share="icon", band=False):
    y0 = y; g = ""
    if back == "pill":
        g += R(14, y + 4, 118, 20, WHITE, INK, 0, 1.2) + mark(18, y + 6, 16, False) + T(38, y + 18, "UpKeep Command Center", 9.5, INK, f="khand"); y += 30
    else: y += 6
    sx = 414 if share == "icon" else 380
    if share == "icon": g += R(414, y, 24, 24, WHITE, INK, 0, 1.2) + share_ic(414, y)
    else: g += R(380, y, 58, 24, WHITE, INK, 0, 1.2) + share_ic(382, y) + T(422, y + 16, "Share", 10.5, INK, f="khand", anchor="middle")
    if back == "link": g += T(sx - 8, y + 16, "< UpKeep Command Center", 9.5, LAGOON, 600, "end")
    if mpos == "left":
        g += mark(14, y, ms); tx = 14 + ms + 10; ty = y + ms * .5 + 4
        if tstyle == "mixed": g += T(tx, ty, TITLE, 20, INK, f="khand"); tw = kw(TITLE, 20)
        else: g += T(tx, ty, TITLE.upper(), 13.5, INK, f="khand", extra='letter-spacing="2.2"'); tw = len(TITLE) * 13.5 * .66
        g += T(tx, ty + 14, SUB, 9.5, MUTE)
        if status == "title": g += chip(tx + tw + 8, ty - 13, "Agent active", JUNGLE, "dot", 9)[0]
        y += max(ms, ty + 18 - y) + 8
    else:
        g += mark(226 - ms / 2, y, ms); ty = y + ms + 20
        g += (T(226, ty, TITLE, 20, INK, f="khand", anchor="middle") if tstyle == "mixed" else T(226, ty, TITLE.upper(), 13.5, INK, f="khand", anchor="middle", extra='letter-spacing="2.2"'))
        g += T(226, ty + 14, SUB, 9.5, MUTE, anchor="middle")
        if status == "title": cw = 66; g += chip(226 - cw / 2, ty + 20, "Agent active", JUNGLE, "dot", 9)[0]; ty += 18
        y = ty + 22
    if idc == "card":
        g += R(14, y, 300, 40, WHITE, LINE, 6) + R(14, y, 3, 40, JUNGLE) + mark(24, y + 8, 24) + T(56, y + 19, "Members Agent", 12.5, INK, f="khand") + T(56, y + 32, "Reports to Ethan  ·  Smart Upkeep  ·  SAMPLE", 8.5, MUTE)
        if status == "card": g += chip(236, y + 8, "Agent active", JUNGLE, "soft", 8.5)[0]
        y += 48
    elif idc == "inline":
        g += T(14, y + 6, "Members Agent  ·  Reports to Ethan  ·  SAMPLE", 9.5, INK, 500)
        if status == "card": g += chip(250, y - 4, "Agent active", JUNGLE, "dot", 9)[0]
        y += 14
    if accent == "rule": g += L(14, y, 438, y, INK, 1.5)
    elif accent == "tri": g += tri(y)
    if band: g = R(0, y0, 452, y - y0 + 2, CREAM) + g + tri(y)
    return g, y - y0 + 10
def alert_row(x, y, a, types="one", w=424):
    hz, txt, frm, tm = a
    if types == "one": g = warn(x, y - 10, TERRA) + T(x + 16, y, hz.upper(), 9.5, TERRA, 700, extra='letter-spacing=".8"'); tx = x + 86
    else: cw = len(hz) * 9 * .62 + 14; g = R(x, y - 11, cw, 15, HAZ[hz], rx=2) + T(x + cw / 2, y, hz.upper(), 8.5, WHITE, 700, "middle", extra='letter-spacing=".6"'); tx = x + 86
    return g + T(tx, y, txt, 10, INK, 600) + T(x + w - 10, y, f"{frm}  ·  {tm}", 8.5, MUTE, anchor="end")
def alerts(y, style="fold", types="one", rows=2, empty=None):
    A = ALERTS[:rows]
    if empty == "quiet": return fold(y, "Emergency Alerts", 0, False, right="No active alerts"), 30
    if empty == "strip":
        return (fold(y, "Emergency Alerts", 0, True, 30) + R(22, y + 30, 408, 18, JUNGLE + "12", rx=4) + checkc(34, y + 39) + T(46, y + 43, "No active alerts", 10, JUNGLE, 700)
                + T(424, y + 43, "Checked 11:40 AM  ·  gas, electrical, CO, flooding", 8.5, MUTE, anchor="end")), 60
    if style == "closed": return fold(y, "Emergency Alerts", None, False, badge=len(A), right="Opens itself when an alert comes in", rcol=TERRA), 30
    if style == "banner":
        h = 26 + len(A) * 20; g = R(14, y, 424, h, TERRA + "14", TERRA, 3, 1.3) + R(14, y, 5, h, TERRA)
        g += T(28, y + 17, "EMERGENCY ALERTS", 12, TERRA, f="khand", extra='letter-spacing="1.5"') + chip(156, y + 6, f"{len(A)} active", TERRA, "solid", 8.5)[0] + T(428, y + 16, "Always shown", 8.5, TERRA, 600, "end")
        for i, a in enumerate(A): g += alert_row(28, y + 40 + i * 20, a, types, 410)
        return g, h + 8
    body = 8 + len(A) * 20; g = fold(y, "Emergency Alerts", None, True, body, badge=len(A), right="Opened itself: active alert", rcol=TERRA, edge=TERRA)
    for i, a in enumerate(A): g += alert_row(24, y + 40 + i * 20, a, types, 414)
    return g, 24 + body + 8
def todo(y, style="closed", anat="lean", count="paren"):
    n = sum(1 for t in TODO if not t[4])
    if style == "closed":
        return fold(y, "To-Do List", n if count == "paren" else None, False, right=None if count == "paren" else "2 open  ·  1 due today"), 30
    rh = 20 if anat == "lean" else 30
    if style == "inline":
        g = T(14, y + 14, "To-Do List", 13, INK, f="khand") + T(14 + kw("To-Do List", 13) + 6, y + 14, f"({n})" if count == "paren" else "", 9.5, MUTE, 500)
        if count != "paren": g += T(438, y + 14, "2 open  ·  1 due today", 9, MUTE, 500, "end")
        g += L(14, y + 20, 438, y + 20, INK, 1); yy = y + 26
    else:
        g = fold(y, "To-Do List", n if count == "paren" else None, True, len(TODO) * rh + 8, right=None if count == "paren" else "2 open  ·  1 due today"); yy = y + 30
    for t_, frm, due, lab, done in TODO:
        g += check(24, yy + 2, done) + T(42, yy + 11, t_, 10, MUTE if done else INK, 500 if done else 600, extra='text-decoration="line-through"' if done else "")
        if anat == "full":
            g += T(42, yy + 23, frm, 8.5, MUTE) + lab_chip(300, yy + 1, lab, "soft", 7.5)[0]
        g += T(428, yy + 11, due, 9, TERRA if due == "Today" else MUTE, 600, "end"); yy += rh
    return g, yy - y + 8
def dchip(x, y, k, style="outline"):
    s = CHIPTXT[k]; c = CHIPC[k]
    if style == "outline": w = len(s) * 7.5 * .66 + 16; return R(x, y, w, 14, WHITE, c, 0, 1.1) + C(x + 6, y + 7, 2, c) + T(x + 11, y + 10.3, s, 7.5, c, 700, extra='letter-spacing=".6"'), w
    s2 = {"draft": "Draft", "approval": "For approval", "approved": "Approved"}[k]; w = len(s2) * 8.5 * .55 + 14
    return R(x, y, w, 14, c, rx=7) + T(x + w / 2, y + 10.3, s2, 8.5, WHITE, 600, "middle"), w
def openbtn(x, y, kind="new"):
    if kind == "new": return R(x, y, 54, 18, WHITE, JUNGLE, 3, 1.1) + f'<path d="M{x+9} {y+5} h4 M{x+15} {y+5} v4 M{x+15} {y+5} l-5 5" stroke="{JUNGLE}" stroke-width="1.2" fill="none"/>' + T(x + 34, y + 12.5, "Open", 9, JUNGLE, 600, "middle")
    return R(x, y, 60, 18, WHITE, LAGOON, 3, 1.1) + T(x + 30, y + 12.5, "Preview", 9, LAGOON, 600, "middle")
def docs(y, style="list", anat="full", chips="outline", empty=None, open_="new", n=3):
    D = DOCS[:n]
    if empty == "quiet": return fold(y, "Documents Center", 0, True, 26) + T(24, y + 41, "No documents pinned yet.", 10, MUTE), 58
    if empty == "card":
        return (fold(y, "Documents Center", 0, True, 70) + R(24, y + 32, 404, 56, WHITE, "#B9AE9C", 6, 1.2, 'stroke-dasharray="4 3"') + docic(40, y + 46, LAGOON, 20)
                + T(70, y + 54, "Nothing pinned yet", 12, INK, f="khand") + T(70, y + 68, "The Members Agent pins drafts and decks here for review.", 9, MUTE) + T(70, y + 80, "SAMPLE empty state", 8, MUTE, 700)), 102
    if style == "closed": return fold(y, "Documents Center", len(D), False, right="Newest: Welcome Message, Oct 19"), 30
    if style == "list":
        rh = 34 if anat == "full" else 24; g = fold(y, "Documents Center", len(D), True, len(D) * rh + 6); yy = y + 28
        for t, tt, k, d, c in D:
            g += docic(24, yy + 4, c, 14) + T(44, yy + 14, tt, 11, INK, 600)
            if anat == "full":
                g += T(40 + 4, yy + 27, f"{t}  ·  {d}  ·  Pinned by Members Agent", 8.5, MUTE)
                g += dchip(200, yy + 4, k, chips)[0]
            else: g += dchip(200, yy + 4, k, chips)[0]
            g += openbtn(372, yy + 3, open_) + (L(24, yy + rh - 1, 428, yy + rh - 1) if anat == "full" else ""); yy += rh
        return g, yy - y + 8
    if style == "grid":
        g = fold(y, "Documents Center", len(D), True, 138); x = 24
        for t, tt, k, d, c in D:
            g += R(x, y + 32, 128, 128, WHITE, LINE, 4) + R(x, y + 32, 128, 3, c) + R(x + 1, y + 35, 126, 50, CREAM) + T(x + 64, y + 64, t, 10, "#A39B8F", 700, "middle", extra='letter-spacing="1.5"')
            g += T(x + 8, y + 100, tt, 11, INK, f="khand") + dchip(x + 8, y + 106, k, chips)[0] + T(x + 8, y + 132, d + "  ·  Pinned by agent", 8, MUTE) + openbtn(x + 8, y + 137, open_)[:0] + R(x + 8, y + 138, 112, 16, WHITE, JUNGLE, 3, 1) + T(x + 64, y + 149.5, "Open", 9, JUNGLE, 600, "middle"); x += 136
        return g, 172
    if style == "carousel":
        g = fold(y, "Documents Center", 4, True, 124); x = 40
        for t, tt, k, d, c in DOCS:
            if x > 440: break
            g += R(x, y + 32, 150, 96, WHITE, LINE, 6) + R(x, y + 32, 4, 96, c) + docic(x + 12, y + 42, c, 16) + T(x + 34, y + 54, t, 8.5, c, 700, extra='letter-spacing="1"')
            g += T(x + 12, y + 76, tt, 12, INK, f="khand") + dchip(x + 12, y + 82, k, chips)[0] + T(x + 12, y + 112, d, 8.5, MUTE) + T(x + 140, y + 112, "Open", 9, JUNGLE, 600, "end"); x += 160
        g += R(14, y + 24, 22, 128, WHITE) + R(430, y + 24, 8, 128, WHITE)
        g += C(28, y + 80, 9, WHITE, LINE) + chev(28, y + 80, INK, False)[:0] + f'<path d="M{30} {y+76} l-4 4 l4 4" fill="none" stroke="{INK}" stroke-width="1.5"/>'
        g += C(424, y + 80, 9, WHITE, INK) + chev(424, y + 80, INK, False)
        g += "".join(R(206 + i * 12, y + 140, 8 if i == 0 else 5, 4, TERRA if i == 0 else "#D6D0C6", rx=2) for i in range(4))
        return g, 162
    if style == "preview":
        g = fold(y, "Documents Center", len(D), True, 150); yy = y + 30
        for i, (t, tt, k, d, c) in enumerate(D):
            if i == 0: g += R(20, yy, 186, 32, LAGOON + "12") + R(20, yy, 3, 32, LAGOON)
            g += docic(28, yy + 8, c, 13) + T(46, yy + 14, tt, 10.5, INK, 600) + T(46, yy + 26, d, 8.5, MUTE); yy += 36
        g += R(214, y + 30, 216, 138, WHITE, LINE, 4) + T(224, y + 46, "PREVIEW  ·  Welcome Message", 8.5, MUTE, 700, extra='letter-spacing=".8"') + dchip(224, y + 52, "draft", chips)[0]
        g += "".join(L(224, y + 82 + i * 12, 420 - (i % 3) * 30, y + 82 + i * 12, "#D9D1C3", 3) for i in range(6)) + T(420, y + 162, "Open full page", 8.5, JUNGLE, 600, "end")
        return g, 176
def board(h=None, blocks=(("alerts", {}), ("todo", {}), ("docs", {}))):
    g, y = header(**(h or {}))
    for kind, o in blocks:
        s, d = {"alerts": alerts, "todo": todo, "docs": docs}[kind](y, **o); g += s; y += d
    return g + stub(y + 2) + bym(452)
def T_HEADER():
    pairs, P = make("ukhd19_", "UpKeep"); F = frame; LOC = "UpKeep Board Header"
    DEF = (("alerts", {"empty": "quiet"}), ("todo", {}), ("docs", {"style": "closed"}))
    P("Header blocks", LOC, "Block order", "which header block should sit right under the title, Emergency Alerts or the To-Do List?",
      ("alerts", "Alerts, To-Do, Documents", "Emergency Alerts first, then To-Do List, then Documents.", "safe",
       F(board(blocks=(("alerts", {"style": "fold"}), ("todo", {"style": "closed"}), ("docs", {"style": "list", "anat": "lean"}))), "Alerts first")),
      ("todo", "To-Do, Alerts, Documents", "To-Do List first, alerts as the second fold.", "practical",
       F(board(blocks=(("todo", {"style": "open"}), ("alerts", {"style": "closed"}), ("docs", {"style": "list", "anat": "lean"}))), "To-Do first")))
    P("Brand mark", LOC, "House mark", "should the UP house mark be a large tile beside the title or a small mark centred above it?",
      ("left", "Large Tile Beside Title", "A big cream mark tile on the left, title to its right.", "bold", F(board({"ms": 52}, DEF), "Large mark, left")),
      ("center", "Small Mark Centred Above", "A small mark centred over a centred title.", "calm", F(board({"ms": 30, "mpos": "center"}, DEF), "Small mark, centred")))
    P("Title", LOC, "Title type", "should the board title be large Khand in normal case or smaller tracked capitals?",
      ("mixed", "Large Khand, Normal Case", "Members Command Center in bold Khand, like today.", "friendly", F(board({}, DEF), "Khand normal case")),
      ("caps", "Tracked Capitals", "Smaller spaced-out capitals, more like a sign.", "formal", F(board({"tstyle": "caps"}, DEF), "Tracked capitals")))
    P("Accent", LOC, "Accent line", "should the header end on a plain ink rule or a thin terracotta, lagoon and jungle line?",
      ("rule", "Plain Ink Rule", "One dark line under the header, as on the boards now.", "calm", F(board({"accent": "rule"}, DEF), "Ink rule")),
      ("tri", "Three-Colour Line", "A thin line in terracotta, lagoon and jungle.", "branded", F(board({"accent": "tri"}, DEF), "Three-colour line")))
    P("Accent", LOC, "Header band", "should the header sit on white or on a warm cream band?",
      ("white", "White Header", "White behind the header, accent line below.", "clean", F(board({"accent": "tri"}, DEF), "White header")),
      ("band", "Cream Band", "A full-width warm cream band behind the header.", "warm", F(board({"accent": "none", "band": True}, DEF), "Cream band")))
    P("Navigation", LOC, "Back link", "should the link back to the UpKeep Command Center be a box above the title or a text link at the top right?",
      ("pill", "Box Above The Title", "A boxed button with the small mark, top left.", "clear", F(board({"back": "pill"}, DEF), "Boxed back link")),
      ("link", "Text Link Top Right", "A lagoon text link beside the share button.", "subtle", F(board({"back": "link"}, DEF), "Text link top right")))
    P("Agent", LOC, "Agent identity", "should the agent's name and who it reports to be a small card or one line under the title?",
      ("card", "Identity Card", "A card with the mark, Members Agent and Reports to Ethan.", "friendly", F(board({"idc": "card", "accent": "tri"}, DEF[:2]), "Identity card")),
      ("inline", "One Line Under Title", "Members Agent and Reports to Ethan as one quiet line.", "calm", F(board({"idc": "inline", "accent": "tri"}, DEF[:2]), "One line")))
    P("Agent", LOC, "Status and share", "should the agent status chip sit by the title with a share icon or in the card with a Share button?",
      ("title", "Chip By Title, Share Icon", "Agent active beside the title, a square share icon.", "subtle", F(board({"status": "title", "idc": "inline", "accent": "tri"}, DEF[:2]), "Chip by title, icon")),
      ("card", "Chip In Card, Share Button", "Status inside the identity card, a labelled Share button.", "clear", F(board({"status": "card", "idc": "card", "share": "label", "accent": "tri"}, DEF[:2]), "Chip in card, button")))
    P("Emergency Alerts", LOC, "Emergency Alerts style", "should emergency alerts be a terracotta banner that is always shown or a fold with a count that opens itself when an alert comes in?",
      ("banner", "Always-Shown Banner", "A terracotta banner that never folds away.", "bold", F(board({"ms": 34}, (("alerts", {"style": "banner", "rows": 3}), ("todo", {}), ("docs", {"style": "closed"}))), "Terracotta banner")),
      ("fold", "Fold That Opens Itself", "A fold with a count badge that opens when an alert is live.", "calm", F(board({"ms": 34}, (("alerts", {"style": "fold", "rows": 3}), ("todo", {}), ("docs", {"style": "closed"}))), "Self-opening fold")))
    P("Emergency Alerts", LOC, "Hazard look", "should gas, electrical, CO and flooding alerts all use one terracotta warning or each get its own colour tag?",
      ("one", "One Terracotta Warning", "Same warning sign and terracotta word for every hazard.", "calm", F(board({"ms": 34}, (("alerts", {"style": "fold", "rows": 4, "types": "one"}), ("todo", {}), ("docs", {"style": "closed"}))), "One warning colour")),
      ("colour", "Colour Tag Per Hazard", "Gas terracotta, electrical gold, CO charcoal, flooding lagoon.", "guided", F(board({"ms": 34}, (("alerts", {"style": "fold", "rows": 4, "types": "colour"}), ("todo", {}), ("docs", {"style": "closed"}))), "Colour per hazard")))
    P("Emergency Alerts", LOC, "No alerts state", "when nothing is live, should Emergency Alerts be a closed fold reading No active alerts or a green all-clear strip?",
      ("quiet", "Closed Fold, Quiet Line", "A closed fold with No active alerts on the right.", "calm", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {}), ("docs", {"style": "closed"}))), "Quiet closed fold")),
      ("strip", "Green All-Clear Strip", "An open strip: No active alerts, checked at a time.", "reassuring", F(board({}, (("alerts", {"empty": "strip"}), ("todo", {}), ("docs", {"style": "closed"}))), "All-clear strip")))
    P("To-Do List", LOC, "To-Do style", "should the To-Do List be a fold like the dashboards or an always-open checklist?",
      ("fold", "Fold Like The Dashboards", "Cream fold-down, same as the Morning Report fold.", "consistent", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"style": "open"}), ("docs", {"style": "closed"}))), "Dashboard fold")),
      ("inline", "Always-Open Checklist", "A titled checklist with no fold, always in view.", "direct", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"style": "inline"}), ("docs", {"style": "closed"}))), "Inline checklist")))
    P("To-Do List", LOC, "To-Do item", "should each to-do show just the task and due date or also who asked and a TEST, Forecast or Decided label?",
      ("lean", "Task And Due Date", "Checkbox, task and due date on one line.", "calm", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"style": "open", "anat": "lean"}), ("docs", {"style": "closed"}))), "Task and due")),
      ("full", "Task, Asker, Label, Due", "Adds who asked and a TEST, Forecast or Decided chip.", "detailed", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"style": "open", "anat": "full"}), ("docs", {"style": "closed"}))), "Full item")))
    P("To-Do List", LOC, "To-Do count", "should the To-Do fold show a count in brackets or a short open and due-today summary?",
      ("paren", "Count In Brackets", "To-Do List (2), like the dashboards.", "consistent", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"count": "paren"}), ("docs", {"style": "closed"}))), "Count in brackets")),
      ("sum", "Open And Due Summary", "2 open, 1 due today, on the right of the fold.", "informative", F(board({}, (("alerts", {"empty": "quiet"}), ("todo", {"count": "sum"}), ("docs", {"style": "closed"}))), "Open and due summary")))
    B = lambda **o: (("alerts", {"empty": "quiet"}), ("todo", {}), ("docs", o))
    P("Documents Center", LOC, "Documents layout", "should pinned documents open as a dropdown list or a grid of tiles?",
      ("list", "Dropdown List", "One row per document inside the fold.", "tidy", F(board({}, B(style="list")), "Dropdown list")),
      ("grid", "Tile Grid", "Document tiles with a cream preview area.", "visual", F(board({}, B(style="grid")), "Tile grid")))
    P("Documents Center", LOC, "Documents carousel", "should many documents sit in a tile grid or a sliding carousel of doc cards?",
      ("grid", "Tile Grid", "All tiles visible, wrapping to new rows.", "complete", F(board({}, B(style="grid")), "Tile grid")),
      ("car", "Carousel Of Doc Cards", "Doc cards slide sideways with arrows and dots.", "light", F(board({}, B(style="carousel")), "Carousel")))
    P("Documents Center", LOC, "Document row", "should each document row show type, date and pinned by or just the title and status chip?",
      ("full", "Type, Date, Pinned By", "Title plus type, date and Pinned by Members Agent.", "detailed", F(board({}, B(style="list", anat="full")), "Full row")),
      ("lean", "Title And Chip Only", "Icon, title, status chip and Open.", "calm", F(board({}, B(style="list", anat="lean")), "Lean row")))
    P("Documents Center", LOC, "Approval chip", "should DRAFT and approval status be an outlined capital tag or a small solid pill?",
      ("outline", "Outlined Capital Tag", "DRAFT, NEEDS APPROVAL in a thin terracotta box.", "formal", F(board({}, B(style="list", chips="outline")), "Outlined tag")),
      ("solid", "Small Solid Pill", "A short solid Draft or Approved pill.", "friendly", F(board({}, B(style="list", chips="solid")), "Solid pill")))
    P("Documents Center", LOC, "Opening a document", "should a document open in a new tab or in a preview pane beside the list?",
      ("new", "Open In New Tab", "An Open button on each row opens the doc page.", "simple", F(board({}, B(style="list", anat="lean", open_="new")), "Open in new tab")),
      ("preview", "Preview Pane", "Click a row to preview it on the right.", "quick", F(board({}, B(style="preview")), "Preview pane")))
    P("Documents Center", LOC, "Empty documents", "when nothing is pinned, should the fold show one quiet line or a dashed card explaining what goes there?",
      ("quiet", "One Quiet Line", "No documents pinned yet, in grey.", "calm", F(board({}, B(empty="quiet")), "Quiet line")),
      ("card", "Dashed Explainer Card", "A dashed card saying what the agent pins here.", "guided", F(board({}, B(empty="card")), "Dashed card")))
    return pairs
