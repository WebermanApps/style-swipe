"""Member Catalog Deck Two, Oct 19 2026 (Max submitted round 1 at 11:48 ICT; follow-up is top priority). 20 pairs refining his round-1 winners.
Every mockup is one coherent catalog: laptop list-detail split, table rows on the left (grouped by plan, A-Z inside), search bar plus filter chips,
jump bar across the top, dot-and-word status, badge with tier blocks, home photo; detail panel with tabs (number tiles + photos, highlighted
preferred box, labelled buttons, simple lists, open-items dropdown with count, dated notes, Add button + nudge). Same privacy rules as round 1:
invented sample members only, tagged SAMPLE."""
from md1018_kit import make
from mcd1019 import (M, STC, PLC, T, R, C, L, chev, chip, avatar, frame, INK, MUTE, LINE, CREAM, WHITE, TERRA, LAGOON, JUNGLE, SOFT)
LOC = "Members Catalog"
DEF = dict(rows="lines", rh=26, sticky=False, cols=("name", "plan", "status", "next"), chips=("All", "Core", "Plus", "Premier"), ghead="rule",
           jump="buttons", pw=210, phead="photo", tabs=("Contact", "Home", "Membership", "Visits", "Notes"), tabstyle="underline", tab="Home",
           tiles=("Built", "Sq ft", "Systems"), cbox="tint", act="row", oi="count", note="card", nudge="Add on the next call", sheet="brand",
           rowshow="one", sel=0, face="photo")
def tierb(x, y, plan, k=1):
    n = {"Core": 1, "Plus": 2, "Premier": 3}[plan]
    return "".join(R(x + i * 7 * k, y, 5 * k, 5 * k, PLC[plan] if i < n else "#E2DACB", rx=1) for i in range(3))
COLX = {"name": 0, "plan": 0, "status": 0, "next": 0, "area": 0, "phone": 0, "renew": 0}
COLW = {"name": 96, "plan": 58, "status": 58, "next": 44, "area": 56, "phone": 70, "renew": 46}
COLH = {"name": "Name", "plan": "Plan", "status": "Status", "next": "Next", "area": "Area", "phone": "Phone", "renew": "Renews"}
def cell(k, m, x, y):
    if k == "name": return T(x, y, m[0], 9.5, INK, 600)
    if k == "plan": return tierb(x, y - 6, m[1]) + T(x + 22, y, m[1], 8.5, PLC[m[1]], 600)
    if k == "status": return C(x + 3, y - 3, 3, STC[m[3]]) + T(x + 9, y, m[3], 8.5, INK, 500)
    if k == "next": return T(x, y, m[4], 8.5, INK)
    if k == "area": return T(x, y, m[2], 8.5, MUTE)
    if k == "phone": return T(x, y, m[5], 8, MUTE)
    if k == "renew": return T(x, y, "Mar 2027", 8.5, MUTE)
def table(o, x0, y0, w, h):
    s = ""; rh = o["rh"]; xs = []; x = x0 + 26 if o["face"] == "photo" else x0 + 8
    for k in o["cols"]: xs.append(x); x += COLW[k]
    hdr = R(x0, y0, w, 18, SOFT) + "".join(T(xx, y0 + 12, COLH[k].upper(), 7, MUTE, 700, extra='letter-spacing=".6"') for xx, k in zip(xs, o["cols"]))
    if o["sticky"]: hdr += L(x0, y0 + 18, x0 + w, y0 + 18, "#CFC6B6", 2) + T(x0 + w - 4, y0 + 12, "PINNED", 6.5, LAGOON, 700, "end")
    y = y0 + 18; groups = [("Premier", [M[2], M[5]]), ("Plus", [M[0], M[3], M[6]]), ("Core", [M[1], M[4], M[7]])]; i = 0
    for g, ms in groups:
        if y > y0 + h - 20: break
        gh = o["ghead"]
        if gh == "rule": s += T(x0 + 8, y + 13, g.upper() + f"  ·  {len(ms)}", 8, PLC[g], 700, extra='letter-spacing="1"') + L(x0 + 8, y + 17, x0 + w - 6, y + 17, PLC[g] + "66"); y += 20
        elif gh == "band": s += R(x0, y + 2, w, 16, PLC[g] + "18") + R(x0, y + 2, 3, 16, PLC[g]) + T(x0 + 10, y + 13, f"{g} plan", 8.5, INK, 700) + tierb(x0 + 60, y + 7, g) + T(x0 + w - 6, y + 13, f"{len(ms)} members", 7.5, MUTE, anchor="end"); y += 20
        elif gh == "collapse": s += R(x0 + 4, y + 2, w - 8, 16, WHITE, LINE, 4) + chev(x0 + 12, y + 10) + T(x0 + 22, y + 13, g, 8.5, INK, 700) + C(x0 + 60, y + 10, 6, PLC[g]) + T(x0 + 60, y + 13, str(len(ms)), 7, WHITE, 700, "middle"); y += 20
        for m in ms:
            if y > y0 + h - rh: break
            rr = rh + (10 if o["rowshow"] == "two" else 0)
            if o["rows"] == "zebra" and i % 2: s += R(x0, y, w, rr, "#F7F3EC")
            if i == o["sel"]: s += R(x0, y, w, rr, LAGOON + "14") + R(x0, y, 2.5, rr, LAGOON)
            if o["face"] == "photo": r_ = min(9, rr / 2 - 2); s += R(x0 + 14 - r_, y + rr / 2 - r_, 2 * r_, 2 * r_, SOFT, LINE, 2) + f'<path d="M{x0+14-r_*.6:.1f} {y+rr/2+r_*.6:.1f} l{r_*.6:.1f} -{r_*.9:.1f} l{r_*.6:.1f} {r_*.9:.1f} z" fill="{JUNGLE}66"/>'
            cy = y + (rr / 2 + 3 if o["rowshow"] != "two" else 13)
            for xx, k in zip(xs, o["cols"]): s += cell(k, m, xx, cy)
            if o["rowshow"] == "two": s += T(xs[0], y + 26, m[7].replace(" St", " St") + ", " + m[2], 7.5, MUTE)
            if o["rowshow"] == "flag" and m[3] == "Overdue": s += R(x0 + w - 40, cy - 8, 34, 11, TERRA + "18", rx=5) + T(x0 + w - 23, cy, "2 open", 6.5, TERRA, 700, "middle")
            if o["rows"] == "lines": s += L(x0, y + rr, x0 + w, y + rr)
            y += rr; i += 1
    return hdr + s
def chipsrow(o, x, y):
    s = ""
    for j, c in enumerate(o["chips"]):
        g, w = chip(x, y, c, LAGOON if j == 0 else MUTE, "solid" if j == 0 else "outline", 8); s += g; x += w + 4
    return s
def jump(o, x, y, w):
    AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; s = ""; step = w / 26
    for j, ch in enumerate(AL):
        on = ch in "ABCDEFGH"; cx = x + j * step + step / 2
        if o["jump"] == "buttons": s += R(x + j * step + .5, y, step - 1, 13, TERRA if ch == "A" else WHITE, TERRA if ch == "A" else LINE, 2) + T(cx, y + 9.5, ch, 7, WHITE if ch == "A" else (INK if on else "#C2B9AC"), 600, "middle")
        else: s += T(cx, y + 10, ch, 7.5, TERRA if ch == "A" else (INK if on else "#C2B9AC"), 700 if ch == "A" else 500, "middle") + (R(cx - 4, y + 13, 8, 2, TERRA) if ch == "A" else "")
    return s
def tabsbar(o, x, y, w):
    s = ""; n = len(o["tabs"]); tw = w / n
    for j, t_ in enumerate(o["tabs"]):
        on = t_ == o["tab"]; tx = x + j * tw
        if o["tabstyle"] == "underline": s += T(tx + tw / 2, y + 11, t_, 7.5, LAGOON if on else MUTE, 600, "middle") + (R(tx + 3, y + 15, tw - 6, 2.5, LAGOON) if on else "")
        else: s += R(tx + 1, y, tw - 2, 16, LAGOON if on else SOFT, rx=8) + T(tx + tw / 2, y + 11, t_, 7.5, WHITE if on else MUTE, 600, "middle")
    return s + (L(x, y + 18, x + w, y + 18) if o["tabstyle"] == "underline" else "")
def actions(o, x, y, w):
    labs = {"row": ["Call", "Text", "Email", "Client page"], "two": ["Text", "Call"], "menu": ["Text", "More"]}[o["act"]]
    s = ""; bw = (w - 4 * (len(labs) - 1)) / len(labs)
    for j, a in enumerate(labs):
        c = [JUNGLE, LAGOON, LAGOON, TERRA][j % 4]; s += R(x, y, bw, 16, c if j == 0 else WHITE, c, 8, 1) + T(x + bw / 2, y + 11, a + (" v" if a == "More" else ""), 7.5, WHITE if j == 0 else c, 600, "middle"); x += bw + 4
    return s
def pane_body(o, m, x, y, w):
    s = ""; t_ = o["tab"]
    if t_ == "Home":
        n = len(o["tiles"]); tw = (w - 4 * (n - 1)) / n
        vals = {"Built": "1952", "Sq ft": "1,480", "Systems": "4", "Beds": "3", "Baths": "1.5", "Roof age": "14 yr", "Lot": "0.2 ac", "Furnace": "2015"}
        for j, k in enumerate(o["tiles"]):
            c = [JUNGLE, LAGOON, TERRA, JUNGLE][j % 4]; s += R(x + j * (tw + 4), y, tw, 36, CREAM, LINE, 5) + T(x + j * (tw + 4) + 6, y + 21, vals[k], 14, c, f="khand") + T(x + j * (tw + 4) + 6, y + 31, k, 6.5, MUTE)
        y += 44; s += T(x, y + 6, "PHOTOS", 6.5, MUTE, 700)
        for j in range(3): s += R(x + j * (w / 3), y + 10, w / 3 - 4, 34, SOFT, LINE, 4) + f'<path d="M{x+j*(w/3)+12} {y+40} l12 -14 l12 14 z" fill="{JUNGLE}44"/>'
        y += 52
        for nm, yr in (("Gas furnace", "2015"), ("Central air", "2018"), ("Water heater", "2020")): s += C(x + 3, y + 5, 2, JUNGLE) + T(x + 9, y + 8, nm, 8, INK) + T(x + w, y + 8, yr, 7.5, MUTE, anchor="end") + L(x, y + 12, x + w, y + 12); y += 15
    elif t_ == "Contact":
        st = o["cbox"]
        if st == "tint": s += R(x, y, w, 46, LAGOON + "12", LAGOON + "55", 6)
        elif st == "edge": s += R(x, y, w, 46, WHITE, LINE, 6) + R(x, y, 3, 46, LAGOON)
        else: s += R(x, y, w, 46, LAGOON, rx=6)
        fg = WHITE if st == "solid" else INK; ac = WHITE if st == "solid" else LAGOON
        s += T(x + 8, y + 12, "PREFERS TEXT", 7, ac, 700, extra='letter-spacing="1"') + T(x + 8, y + 27, m[5], 12, fg, f="khand") + T(x + 8, y + 39, "Best: weekday evenings", 7, ac if st == "solid" else MUTE)
        y += 54
        for k, v in (("Email", m[6]), ("Phone", m[5]), ("Second contact", "Jordan Sample")): s += T(x, y + 8, k, 7.5, MUTE) + T(x + w, y + 8, v, 7.5, INK, 600, "end") + L(x, y + 12, x + w, y + 12); y += 16
    elif t_ == "Membership":
        for k, v in (("Plan", m[1]), ("Billing", "Paid up"), ("Started", "Mar 3, 2026"), ("Renews", "Mar 3, 2027"), ("Add-ons", "Gutter care")): s += T(x, y + 8, k, 7.5, MUTE) + T(x + w, y + 8, v, 7.5, INK, 600, "end") + L(x, y + 12, x + w, y + 12); y += 16
    elif t_ == "Visits":
        for d, v in (("Oct 3", "Fall tune-up"), ("Jul 8", "Summer visit"), ("Apr 12", "Spring visit"), ("Mar 3", "Welcome walk")): s += T(x, y + 8, d, 7.5, MUTE, 600) + T(x + 40, y + 8, v, 7.5, INK) + L(x, y + 12, x + w, y + 12); y += 16
    elif t_ == "Notes":
        s += R(x, y, w, 16, WHITE, "#CFC6B6", 8) + T(x + 8, y + 11, "Add a note", 7.5, MUTE); y += 22
        for d, who, tx in (("Oct 3", "Office", "Likes a text the day before."), ("Jul 8", "Tech", "Friendly dog, shut side gate."), ("Mar 3", "Office", "Gate code with office (sample).")):
            if o["note"] == "card": s += R(x, y, w, 30, WHITE, LINE, 5) + T(x + 6, y + 11, f"{d} · {who}", 7, LAGOON, 600) + T(x + 6, y + 23, tx, 7.5, INK); y += 34
            else: s += C(x + 4, y + 6, 2.5, LAGOON) + T(x + 12, y + 8, tx, 7.5, INK) + T(x + 12, y + 18, f"{d} · {who}", 6.5, MUTE) + L(x, y + 23, x + w, y + 23); y += 26
    return s
def panel(o, x0, y0, w, h):
    m = M[2] if o["sel"] == 0 else M[0]; s = R(x0, y0, w, h, WHITE) + L(x0, y0, x0, y0 + h, "#D3CABB"); x = x0 + 10; iw = w - 20; y = y0 + 8
    if o["phead"] == "photo": s += R(x, y, iw, 54, SOFT, LINE, 6) + f'<path d="M{x+iw/2-26} {y+48} l26 -28 l26 28 z" fill="{JUNGLE}44"/>' + R(x + iw / 2 - 8, y + 34, 16, 14, WHITE); y += 60
    elif o["phead"] == "thumb": s += C(x + 14, y + 14, 14, SOFT, LINE) + f'<path d="M{x+4} {y+22} l10 -13 l10 13 z" fill="{JUNGLE}66"/>'
    tx = x + (34 if o["phead"] == "thumb" else 0)
    s += T(tx, y + 12, m[0], 13, INK, f="khand") + tierb(tx, y + 17, m[1]) + T(tx + 22, y + 22, m[1], 7.5, PLC[m[1]], 600) + C(tx + 52, y + 19.5, 2.5, STC[m[3]]) + T(tx + 58, y + 22, m[3], 7.5, INK) + T(x + iw, y + 12, m[2], 7.5, MUTE, anchor="end")
    y += 30 if o["phead"] != "thumb" else 32
    if o["act"] != "none": s += actions(o, x, y, iw); y += 22
    if o["oi"] == "count": s += R(x, y, iw, 16, WHITE, LINE, 4) + T(x + 6, y + 11, "Open items", 8, INK, 600) + C(x + 54, y + 8, 6, TERRA) + T(x + 54, y + 10.5, "2", 7, WHITE, 700, "middle") + chev(x + iw - 8, y + 8); y += 22
    elif o["oi"] == "outline": s += R(x, y, iw, 16, TERRA + "0D", TERRA + "88", 4) + T(x + 6, y + 11, "2 open items", 8, TERRA, 700) + chev(x + iw - 8, y + 8, TERRA); y += 22
    elif o["oi"] == "pinned": s += R(x, y, iw, 30, TERRA + "10", rx=4) + R(x, y, 2.5, 30, TERRA) + T(x + 8, y + 11, "2 OPEN ITEMS", 7, TERRA, 700) + T(x + 8, y + 23, "Downspout loose  ·  Attic quote sent", 7, INK) ; y += 36
    if o["nudge"]: s += R(x, y, iw, 16, TERRA + "10", rx=4) + T(x + 6, y + 11, "2 details missing. " + o["nudge"] + ".", 7, TERRA, 600) + R(x + iw - 30, y + 2, 26, 12, WHITE, TERRA, 6, 1, 'stroke-dasharray="2 2"') + T(x + iw - 17, y + 11, "+ Add", 6.5, TERRA, 700, "middle"); y += 22
    s += tabsbar(o, x, y, iw); y += 26
    return s + pane_body(o, m, x, y, iw)
def scene(cap_, **k):
    o = dict(DEF, **k); pw = o["pw"]; lw = 452 - pw
    s = R(0, 0, 452, 30, WHITE) + L(0, 30, 452, 30) + T(10, 21, "Members", 16, INK, f="khand") + T(442, 20, "8 sample members", 8, MUTE, 500, "end")
    s += R(8, 36, lw - 16, 20, WHITE, LAGOON, 10, 1.2) + C(20, 46, 4, "none", LAGOON, 1.3) + T(30, 49.5, "Search name, street, phone", 8, MUTE)
    s += chipsrow(o, 8, 60) + jump(o, 8, 82, lw - 16)
    s += table(o, 0, 100, lw, 370) + panel(o, lw, 30, pw, 440)
    return frame(s, cap_)
def sheet(style):
    m = M[0]; s = R(46, 6, 360, 458, WHITE, "#D3CABB", 2); x = 66
    if style == "brand":
        s += R(46, 6, 360, 44, CREAM) + R(46, 48, 360, 2, TERRA) + T(x, 34, "Smart Upkeep", 14, TERRA, f="khand") + T(386, 32, "MEMBER SHEET  ·  SAMPLE", 7.5, MUTE, 700, "end", extra='letter-spacing="1"')
        s += T(x, 80, m[0], 20, INK, f="khand") + tierb(x, 88, m[1], 1.4) + T(x + 32, 96, m[1] + " plan", 9, PLC[m[1]], 600); y = 112
    else:
        s += R(x, 22, 120, 86, SOFT, LINE, 4) + f'<path d="M{x+30} 100 l30 -34 l30 34 z" fill="{JUNGLE}44"/>' + R(x + 52, 82, 16, 18, WHITE)
        s += T(x + 132, 44, m[0], 20, INK, f="khand") + T(x + 132, 62, m[7] + ", " + m[2], 9, MUTE) + tierb(x + 132, 70, m[1], 1.4) + T(x + 164, 78, m[1] + " plan", 9, PLC[m[1]], 600) + T(386, 100, "SAMPLE", 7.5, MUTE, 700, "end"); y = 120
    for ci, (t_, rows) in enumerate((("Contact", [("Prefers", "Text"), ("Phone", m[5]), ("Email", m[6])]), ("Home", [("Built", m[8]), ("Size", m[9] + " sq ft"), ("Systems", "4")]))):
        xx = x + ci * 166; s += R(xx, y, 154, 96, CREAM, rx=4) + T(xx + 10, y + 16, t_.upper(), 8, JUNGLE, 700); yy = y + 28
        for k, v in rows: s += T(xx + 10, yy + 8, k, 7.5, MUTE) + T(xx + 10, yy + 18, v, 8.5, INK, 600); yy += 22
    y += 108; s += R(x, y, 320, 40, CREAM, rx=4) + T(x + 10, y + 16, "MEMBERSHIP", 8, JUNGLE, 700) + T(x + 10, y + 31, "Plus  ·  Paid up  ·  Renews Mar 3, 2027", 9, INK, 600)
    y += 52; s += R(x, y, 320, 130, WHITE, LINE, 4) + T(x + 10, y + 16, "TECH NOTES", 8, MUTE, 700) + "".join(L(x + 10, y + 36 + i * 20, x + 310, y + 36 + i * 20) for i in range(5))
    return frame(s, "Brand band header" if style == "brand" else "Home photo header")
def T_MEMBERS2():
    pairs, P = make("mcd19b_", "UpKeep"); A = lambda key, lab, desc, feel, cap, **k: (key, lab, desc, feel, scene(cap, **k))
    P("Table density", LOC, "Row height", "how tall should each table row be on a laptop?",
      A("snug", "Snug Rows", "About 14 members on screen, small but easy to read.", "practical", "Snug rows", rh=22),
      A("comfy", "Comfortable Rows", "About 10 members on screen with more air.", "calm", "Comfortable rows", rh=32))
    P("Table density", LOC, "Column count", "should the table show four columns or six?",
      A("four", "Four Columns", "Name, plan, status, next visit.", "calm", "Four columns", cols=("name", "plan", "status", "next")),
      A("six", "Six Columns", "Adds area and renewal month.", "practical", "Six columns", cols=("name", "plan", "status", "next", "area", "renew"), pw=170))
    P("Closed row", LOC, "Closed row content", "what should a table row show before you open the member?",
      A("one", "One Clean Line", "Just the columns, one line per member.", "calm", "One line per member", rowshow="one"),
      A("two", "Two Lines With Street", "A second small line with street and city.", "practical", "Two lines with street", rowshow="two", cols=("name", "plan", "status")))
    P("Closed row", LOC, "Open-item flag on the row", "should a row flag open items before you open the member?",
      A("flag", "Small Open Flag", "A terracotta '2 open' tag at the row end.", "guided", "Open flag on row", rowshow="flag"),
      A("none", "No Flag On The Row", "Open items show only inside the member.", "subtle", "No flag on row"))
    P("Row style", LOC, "Row style", "should rows be split by thin lines or soft zebra stripes?",
      A("lines", "Thin Lines", "A hairline between every row.", "subtle", "Thin lines", rows="lines"),
      A("zebra", "Soft Zebra Stripes", "Every other row a warm cream.", "calm", "Zebra stripes", rows="zebra"))
    P("Row style", LOC, "Sticky header", "should the column header stay pinned while you scroll?",
      A("stick", "Pinned Header", "Column names stay at the top as you scroll.", "practical", "Pinned header", sticky=True),
      A("scroll", "Header Scrolls Away", "More room once you scroll down.", "calm", "Header scrolls away"))
    P("Tabs", LOC, "Tab style", "should the member tabs be underlined words or filled pills?",
      A("under", "Underlined Words", "Quiet words with a lagoon underline.", "subtle", "Underlined tabs", tabstyle="underline"),
      A("pill", "Filled Pills", "The open tab is a solid lagoon pill.", "guided", "Pill tabs", tabstyle="pill"))
    P("Tabs", LOC, "Tab names and order", "should Home or Contact be the first tab?",
      A("home", "Home First", "Home, Contact, Membership, Visits, Notes.", "friendly", "Home first", tabs=("Home", "Contact", "Membership", "Visits", "Notes")),
      A("contact", "Contact First", "Contact, Home, Membership, Visits, Notes.", "practical", "Contact first", tab="Contact"))
    P("Filters", LOC, "Filter chip set", "should the chips filter by plan or by status?",
      A("plan", "Plan Chips", "All, Core, Plus, Premier.", "calm", "Plan chips"),
      A("status", "Status Chips", "All, Active, New, Paused, Overdue.", "guided", "Status chips", chips=("All", "Active", "New", "Paused", "Overdue")))
    P("Groups", LOC, "Plan group header", "should each plan group start with a thin rule or a tinted band?",
      A("rule", "Thin Coloured Rule", "Plan name in caps over a hairline.", "subtle", "Thin rule", ghead="rule"),
      A("band", "Tinted Band With Blocks", "A pale band with plan name, tier blocks and count.", "guided", "Tinted band", ghead="band"))
    P("Jump bar", LOC, "Jump bar style", "should the A to Z bar use small boxed buttons or plain letters?",
      A("box", "Boxed Letter Buttons", "Each letter in a small box; empty letters fade.", "guided", "Boxed letters", jump="buttons"),
      A("plain", "Plain Letters", "Just letters, the current one underlined.", "subtle", "Plain letters", jump="plain"))
    P("Detail panel", LOC, "Detail panel width", "how wide should the member panel be on a laptop?",
      A("narrow", "Narrow Panel", "About a third of the screen; table stays wide.", "focused", "Narrow panel", pw=180),
      A("wide", "Wide Panel", "Close to half; more room for tiles and photos.", "friendly", "Wide panel", pw=240, cols=("name", "plan", "status")))
    P("Detail panel", LOC, "Panel header", "should the member panel open with a wide home photo or a small round thumbnail?",
      A("photo", "Wide Home Photo", "A photo banner across the top of the panel.", "friendly", "Wide home photo", phead="photo"),
      A("thumb", "Round Thumbnail", "A small photo circle beside the name.", "subtle", "Round thumbnail", phead="thumb"))
    P("Home tab", LOC, "Home number tiles", "which three numbers should lead the Home tab?",
      A("age", "Built, Sq Ft, Systems", "Home age, size and how many systems.", "practical", "Built, sq ft, systems"),
      A("rooms", "Beds, Baths, Roof Age", "Room count plus the roof's age.", "friendly", "Beds, baths, roof age", tiles=("Beds", "Baths", "Roof age")))
    P("Contact tab", LOC, "Preferred contact box", "should the preferred box be softly tinted, edged or solid lagoon?",
      A("tint", "Soft Tint", "Pale lagoon fill with a thin border.", "calm", "Soft tint box", tab="Contact", cbox="tint"),
      A("solid", "Solid Lagoon", "Solid lagoon box with white type.", "bold", "Solid lagoon box", tab="Contact", cbox="solid"))
    P("Quick actions", LOC, "Quick action set", "should the panel show all four buttons or Text plus a More menu?",
      A("four", "All Four Buttons", "Call, Text, Email, Client page in one row.", "practical", "All four buttons", act="row"),
      A("more", "Text Plus More Menu", "Preferred action first; the rest under More.", "calm", "Text plus More", act="menu"))
    P("Open items", LOC, "Open items dropdown", "should the open items dropdown be plain with a count or terracotta outlined?",
      A("count", "Plain With Count Badge", "Neutral row, small terracotta count.", "subtle", "Plain with count", oi="count"),
      A("outline", "Terracotta Outline", "The whole row softly outlined in terracotta.", "bold", "Terracotta outline", oi="outline"))
    P("Notes tab", LOC, "Note entry style", "should each dated note be a small card or a simple line with a dot?",
      A("card", "Small Note Cards", "Each note in its own bordered card.", "friendly", "Note cards", tab="Notes", note="card"),
      A("line", "Simple Dot Lines", "Notes as lines with a dot, date underneath.", "subtle", "Dot lines", tab="Notes", note="line"))
    P("Missing info", LOC, "Missing-info nudge wording", "how should the nudge word a member's missing details?",
      A("call", "Add On The Next Call", "'2 details missing. Add on the next call.'", "guided", "Add on the next call", nudge="Add on the next call"),
      A("ask", "Ask At The Next Visit", "'2 details missing. Ask at the next visit.'", "friendly", "Ask at the next visit", nudge="Ask at the next visit"))
    P("Print sheet", LOC, "Print sheet header", "should the printed member sheet open with a brand band or a home photo header?",
      ("brand", "Brand Band Header", "Smart Upkeep band, member name and plan badge.", "calm", sheet("brand")),
      ("photo", "Home Photo Header", "Home photo beside the name, street and plan.", "friendly", sheet("photo")))
    return pairs
