"""Member Catalog Deck, Oct 19 2026 (Max asked directly 11:29 ICT): 20 this-or-that pairs to design the Members section of the
UpKeep Members Command Center (catalog of every Smart Upkeep member: name + contact, home info, membership info).
Laptop-first drawn SVG mockups (browser frame), phone-safe. Light only: white / warm cream base, small terracotta, lagoon, jungle pops.
Khand + Hind, no emoji. PRIVACY: every member is invented sample data (fake names, (555) 000-00xx phones, @example.test emails,
'Sample St'-style streets, metro Detroit city names only). Every card is tagged SAMPLE. Nothing from ops-private is used."""
from md1018_kit import make
from draft_svg import screen, esc
INK = "#1F1B16"; MUTE = "#6B645A"; LINE = "#E6DFD3"; CREAM = "#FAF6EE"; WHITE = "#FFFFFF"
TERRA = "#C1502E"; LAGOON = "#05668D"; JUNGLE = "#0B6E4F"; SOFT = "#F3EEE4"
M = [  # name, plan, area, status, next visit, phone, email, street, home age, sqft
    ("Avery Sample", "Plus", "Royal Oak", "Active", "Oct 24", "(555) 000-0101", "avery@example.test", "123 Sample St", "1952", "1,480"),
    ("Blake Testerson", "Core", "Ferndale", "Active", "Oct 27", "(555) 000-0102", "blake@example.test", "45 Placeholder Ave", "1938", "1,220"),
    ("Casey Demo", "Premier", "Troy", "Paused", "None set", "(555) 000-0103", "casey@example.test", "78 Example Rd", "1996", "2,640"),
    ("Devon Mockley", "Plus", "Birmingham", "Active", "Nov 2", "(555) 000-0104", "devon@example.test", "9 Fictional Ln", "1964", "1,910"),
    ("Emery Fakename", "Core", "Novi", "New", "Oct 30", "(555) 000-0105", "emery@example.test", "210 Sample Ct", "2004", "2,150"),
    ("Finley Notreal", "Premier", "Livonia", "Overdue", "Today", "(555) 000-0106", "finley@example.test", "36 Demo Dr", "1971", "1,760"),
    ("Gray Imaginary", "Plus", "Dearborn", "Active", "Nov 5", "(555) 000-0107", "gray@example.test", "500 Mockup Blvd", "1948", "1,340"),
    ("Harper Pretend", "Core", "Southfield", "Active", "Nov 9", "(555) 000-0108", "harper@example.test", "17 Testing Way", "1959", "1,600"),
]
STC = {"Active": JUNGLE, "Paused": MUTE, "New": LAGOON, "Overdue": TERRA}
PLC = {"Core": LAGOON, "Plus": JUNGLE, "Premier": TERRA}
def T(x, y, s, size=13, col=INK, w=400, anchor="start", f="hind", extra=""):
    fam = 'font-family="Khand" font-weight="700"' if f == "khand" else f'font-family="Hind" font-weight="{w}"'
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {fam} {extra}>{esc(s)}</text>'
def R(x, y, w, h, fill, stroke="none", rx=0, sw=1, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def C(cx, cy, r, fill, stroke="none", sw=1): return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def L(x1, y1, x2, y2, c=LINE, sw=1, extra=""): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{sw}" {extra}/>'
def chev(x, y, c=MUTE, down=True):
    d = f"M{x-4} {y-2} l4 4 l4 -4" if down else f"M{x-2} {y-4} l4 4 l-4 4"
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
def chip(x, y, s, c, style="soft", size=10):
    w = len(s) * size * .56 + 14
    if style == "solid": g = R(x, y, w, size + 8, c, rx=(size + 8) / 2) + T(x + w / 2, y + size + 2, s, size, WHITE, 600, "middle")
    elif style == "dot": g = C(x + 5, y + (size + 8) / 2, 3.5, c) + T(x + 12, y + size + 2, s, size, INK, 500); w = len(s) * size * .52 + 14
    elif style == "outline": g = R(x, y, w, size + 8, WHITE, c, 3, 1.2) + T(x + w / 2, y + size + 2, s, size, c, 600, "middle")
    elif style == "bar": g = R(x, y, 3, size + 8, c) + T(x + 8, y + size + 2, s, size, INK, 600); w = len(s) * size * .55 + 10
    else: g = R(x, y, w, size + 8, c + "1A", c + "55", (size + 8) / 2, 1) + T(x + w / 2, y + size + 2, s, size, c, 600, "middle")
    return g, w
def ini(cx, cy, r, name, c=LAGOON):
    a = "".join(p[0] for p in name.split()[:2])
    return C(cx, cy, r, c + "1F", c, 1.2) + T(cx, cy + r * .38, a, r * .95, c, f="khand", anchor="middle")
def avatar(cx, cy, r, c=TERRA):
    return C(cx, cy, r, SOFT, LINE) + C(cx, cy - r * .25, r * .36, c + "AA") + f'<path d="M{cx-r*.62} {cy+r*.72} q{r*.62} -{r*.95} {r*1.24} 0" fill="{c}AA"/>'
def tagS(): return R(18, 14, 78, 26, WHITE, "#B9AE9C", 4, 1.4, 'stroke-dasharray="4 3"') + T(57, 32, "SAMPLE", 13, MUTE, 700, "middle", extra='letter-spacing="1.5"')
def foot(s): return R(0, 556, 480, 44, WHITE) + L(0, 556, 480, 556, "#E8E0D2") + T(240, 584, s, min(18, 430 / (len(s) * .5)), INK, 600, "middle")
def frame(inner, note, kind="laptop"):
    """Laptop browser frame (default) or phone frame. Inner content drawn in frame coords."""
    if kind == "laptop":
        s = R(14, 52, 452, 492, WHITE, "#D3CABB", 10, 1.4) + R(14, 52, 452, 22, SOFT, "none", 10) + R(14, 66, 452, 8, SOFT)
        s += "".join(C(28 + i * 11, 63, 3.2, "#CFC6B6") for i in range(3)) + R(70, 57, 220, 12, WHITE, LINE, 6) + T(78, 66.5, "members.sample.test", 8, MUTE)
        s += f'<g transform="translate(14,74)">{inner}</g>'
    else:
        s = R(150, 50, 180, 494, WHITE, "#D3CABB", 22, 1.6) + R(212, 58, 56, 6, "#E2DACB", rx=3) + f'<g transform="translate(150,70)">{inner}</g>'
    return screen(f'<g transform="scale(.5)">{R(0,0,480,600,CREAM)}{s}{tagS()}{foot(note)}</g>', CREAM)
# ---------- shared laptop pieces (frame inner is 452 x 470) ----------
def topbar(title="Members", count="8 members"):
    return R(0, 0, 452, 34, WHITE) + L(0, 34, 452, 34) + T(14, 23, title, 18, INK, f="khand") + T(438, 22, count, 10, MUTE, 500, "end")
def search(y=44, w=424, x=14, ph="Search name, street, phone"):
    return R(x, y, w, 26, WHITE, "#CFC6B6", 13) + C(x + 14, y + 12, 5, "none", MUTE, 1.5) + L(x + 18, y + 16, x + 21, y + 19, MUTE, 1.5) + T(x + 28, y + 17, ph, 10, MUTE)
def chips_row(y, items, x=14, active=0, c=LAGOON):
    s = ""
    for i, it in enumerate(items):
        g, w = chip(x, y, it, c if i == active else MUTE, "solid" if i == active else "outline", 9.5); s += g; x += w + 6
    return s
def card_tile(x, y, w, h, m, show=("plan", "area", "status", "next"), dense=False, face="ini"):
    s = R(x, y, w, h, WHITE, LINE, 8) + R(x, y, w, 3, PLC[m[1]], rx=1)
    s += ini(x + 18, y + 22, 11, m[0], PLC[m[1]]) if face == "ini" else (avatar(x + 18, y + 22, 11) if face == "photo" else "")
    tx = x + (36 if face else 10)
    s += T(tx, y + 22, m[0], 12 if dense else 13, INK, 600)
    yy = y + 38
    if "plan" in show: g, _ = chip(tx, y + 27, m[1], PLC[m[1]], "soft", 8.5); s += g; yy = y + 58
    if "area" in show: s += T(x + 10, yy, m[2], 10, MUTE); yy += 14
    if "status" in show: g, _ = chip(x + 10, yy - 9, m[3], STC[m[3]], "dot", 9.5); s += g; yy += 14
    if "next" in show and not dense: s += T(x + 10, yy, "Next visit " + m[4], 9.5, INK, 500)
    return s
def table(y, rows, cols=("Name", "Plan", "Area", "Status", "Next visit"), xs=(14, 150, 215, 300, 380), rh=30, sel=None):
    s = R(0, y, 452, 22, SOFT) + "".join(T(x, y + 15, c.upper(), 8.5, MUTE, 700, extra='letter-spacing=".8"') for x, c in zip(xs, cols))
    for i, m in enumerate(rows):
        yy = y + 22 + i * rh
        if sel == i: s += R(0, yy, 452, rh, LAGOON + "12") + R(0, yy, 3, rh, LAGOON)
        s += T(xs[0], yy + rh * .62, m[0], 11, INK, 600)
        g, _ = chip(xs[1], yy + rh / 2 - 8, m[1], PLC[m[1]], "soft", 8.5); s += g
        s += T(xs[2], yy + rh * .62, m[2], 10.5, MUTE)
        g, _ = chip(xs[3], yy + rh / 2 - 8, m[3], STC[m[3]], "dot", 9.5); s += g
        s += T(xs[4], yy + rh * .62, m[4], 10.5, INK) + L(0, yy + rh, 452, yy + rh)
    return s
def section(y, title, open_=True, rows=(), c=LAGOON, w=424, x=14):
    s = R(x, y, w, 26, WHITE if not open_ else CREAM, LINE, 6) + R(x, y, 3, 26, c) + T(x + 12, y + 17, title, 12, INK, 600) + chev(x + w - 16, y + 13, MUTE, open_)
    h = 30
    if open_:
        for k, v in rows:
            s += T(x + 14, y + h + 13, k, 10, MUTE) + T(x + w - 12, y + h + 13, v, 10.5, INK, 600, "end") + L(x + 14, y + h + 19, x + w - 12, y + h + 19); h += 20
        h += 6
    return s, h
def contact_rows(m): return [("Phone", m[5]), ("Email", m[6]), ("Prefers", "Text"), ("Best time", "Weekday evenings")]
def home_rows(m): return [("Street", m[7]), ("City", m[2] + ", MI"), ("Built", m[8]), ("Size", m[9] + " sq ft")]
def mem_rows(m): return [("Plan", m[1]), ("Billing", "Paid up"), ("Started", "Mar 3, 2026"), ("Renews", "Mar 3, 2027")]
def head(m, y=44, face="ini"):
    s = (ini(36, y + 20, 20, m[0], PLC[m[1]]) if face == "ini" else avatar(36, y + 20, 20))
    s += T(66, y + 16, m[0], 18, INK, f="khand")
    g, w = chip(66, y + 22, m[1], PLC[m[1]], "soft", 9); s += g
    g2, _ = chip(66 + w + 6, y + 22, m[3], STC[m[3]], "dot", 9.5)
    return s + g2 + T(438, y + 16, m[2], 11, MUTE, 500, "end")
def actions(y, x=14, style="buttons"):
    s = ""; labs = ["Call", "Text", "Email", "Client page"]; cols = [JUNGLE, LAGOON, LAGOON, TERRA]
    for i, (a, c) in enumerate(zip(labs, cols)):
        w = 62 if i < 3 else 84
        if style == "buttons": s += R(x, y, w, 26, c if i == 0 else WHITE, c, 13, 1.2) + T(x + w / 2, y + 17, a, 10.5, WHITE if i == 0 else c, 600, "middle")
        else: s += C(x + 14, y + 13, 13, c + "18", c, 1.2) + T(x + 14, y + 40, a, 9, INK, 500, "middle"); w = 52
        x += w + 8
    return s
# ---------------- the 20 pairs ----------------
LOC = "Members Catalog"
def grid(y, ms, cols=3, h=96, show=("plan", "area", "status", "next"), dense=False, face="ini"):
    gw = (424 - (cols - 1) * 10) / cols; s = ""
    for i, m in enumerate(ms):
        r, c = divmod(i, cols); s += card_tile(14 + c * (gw + 10), y + r * (h + 10), gw, h, m, show, dense, face)
    return s
def T_MEMBERS():
    pairs, P = make("mcd19_", "UpKeep"); F = frame
    # 1 catalog layout
    P("Catalog", LOC, "Catalog layout", "should every member show as a card in a grid or as a row in a table?",
      ("grid", "Card Grid", "Each member is a small card, three across on a laptop.", "friendly",
       F(topbar() + search() + grid(82, M[:6], 3, 110), "Card grid")),
      ("rows", "Table Rows", "One row per member with sortable columns.", "focused",
       F(topbar() + search() + table(82, M[:8]), "Table rows")))
    # 2 density
    P("Catalog", LOC, "Card density", "how many members should fit on one laptop screen?",
      ("roomy", "Roomy Cards", "Three across with space to breathe, about six per screen.", "calm",
       F(topbar() + search() + grid(82, M[:6], 3, 120), "Roomy, six per screen")),
      ("compact", "Compact Cards", "Four across and shorter, about twelve per screen.", "practical",
       F(topbar() + search() + grid(82, (M + M)[:12], 4, 74, ("plan", "area"), True), "Compact, twelve per screen")))
    # 3 collapsed card content
    def big(m, show, y=90):
        s = R(84, y, 284, 120, WHITE, LINE, 10) + R(84, y, 284, 4, PLC[m[1]], rx=2) + ini(112, y + 34, 18, m[0], PLC[m[1]]) + T(140, y + 32, m[0], 17, INK, f="khand")
        yy = y + 40; x = 140
        for k in show:
            if k == "plan": g, w = chip(x, yy, m[1], PLC[m[1]], "soft", 9); s += g; x += w + 6
            if k == "status": g, w = chip(x, yy, m[3], STC[m[3]], "dot", 9.5); s += g; x += w + 6
        if "area" in show: s += T(104, y + 84, m[2] + ", MI", 11, MUTE)
        if "next" in show: s += T(104, y + 104, "Next visit " + m[4], 11, INK, 600)
        return s + chev(350, y + 34)
    P("Collapsed card", LOC, "Collapsed card", "what should a member card show before it is opened?",
      ("full", "Name, Plan, Area, Status, Visit", "All five facts on the closed card.", "practical",
       F(topbar() + big(M[0], ("plan", "status", "area", "next")) + big(M[5], ("plan", "status", "area", "next"), 230), "All five facts")),
      ("lean", "Name, Plan And Status Only", "Just the essentials; open it for the rest.", "calm",
       F(topbar() + big(M[0], ("plan", "status")) + big(M[5], ("plan", "status"), 230), "Name, plan, status")))
    # 4 member detail pattern: dropdowns vs tabs
    m = M[0]
    def drops():
        s = topbar("Avery Sample", "Member") + head(m); y = 96
        for i, (t_, rows, c) in enumerate((("Contact", contact_rows(m), LAGOON), ("Home", home_rows(m), JUNGLE), ("Membership", mem_rows(m), TERRA))):
            g, h = section(y, t_, i == 0, rows, c); s += g; y += h + 6
        return s
    def tabs():
        s = topbar("Avery Sample", "Member") + head(m); x = 14
        for i, t_ in enumerate(("Contact", "Home", "Membership")):
            w = 92; s += T(x + w / 2, 112, t_, 12, LAGOON if i == 0 else MUTE, 600, "middle") + (R(x, 118, w, 3, LAGOON) if i == 0 else ""); x += w
        s += L(14, 121, 438, 121); y = 132
        for k, v in contact_rows(m): s += T(28, y + 13, k, 10, MUTE) + T(424, y + 13, v, 10.5, INK, 600, "end") + L(28, y + 19, 424, y + 19); y += 22
        return s
    P("Member detail", LOC, "Member sections", "should Contact, Home and Membership open as dropdowns or sit behind tabs?",
      ("drop", "Stacked Dropdowns", "Three sections stacked; open one or all at once.", "calm", F(drops(), "Dropdown sections")),
      ("tabs", "Tabs Across The Top", "One section at a time, switch with tabs.", "focused", F(tabs(), "Tabs")))
    # 5 side panel vs dropdown in place
    def panel():
        s = topbar() + table(44, M[:8], ("Name", "Plan", "Status"), (14, 120, 175), 30, sel=0)
        s += R(236, 34, 216, 436, WHITE) + L(236, 34, 236, 470, "#D3CABB") + ini(262, 66, 16, m[0], PLC[m[1]]) + T(286, 64, m[0], 15, INK, f="khand") + T(286, 80, m[2], 10, MUTE)
        y = 100
        for i, (t_, rows, c) in enumerate((("Contact", contact_rows(m)[:3], LAGOON), ("Home", home_rows(m)[:3], JUNGLE), ("Membership", mem_rows(m)[:3], TERRA))):
            g, h = section(y, t_, i < 2, rows, c, 200, 244); s += g; y += h + 4
        return s
    def inline():
        s = topbar() + R(14, 44, 424, 36, WHITE, LINE, 8) + ini(34, 62, 11, M[1][0], PLC["Core"]) + T(52, 66, M[1][0], 12, INK, 600) + chev(420, 62)
        s += R(14, 86, 424, 230, WHITE, LAGOON, 8, 1.4) + ini(34, 104, 11, m[0], PLC[m[1]]) + T(52, 108, m[0], 12, INK, 600) + chev(420, 104, LAGOON)
        g, h = section(124, "Contact", True, contact_rows(m)[:3], LAGOON, 400, 26); s += g
        g, h2 = section(124 + h + 4, "Home", True, home_rows(m)[:3], JUNGLE, 400, 26); s += g
        y = 322
        for mm in M[2:5]: s += R(14, y, 424, 36, WHITE, LINE, 8) + ini(34, y + 18, 11, mm[0], PLC[mm[1]]) + T(52, y + 22, mm[0], 12, INK, 600) + chev(420, y + 18); y += 42
        return s
    # 6 search vs chips
    P("Find", LOC, "Finding a member", "should the top of the catalog lead with one search bar or with filter chips?",
      ("search", "One Big Search Bar", "Type a name, street or phone and the list narrows.", "calm",
       F(topbar() + R(14, 46, 424, 40, WHITE, LAGOON, 20, 1.6) + C(36, 66, 7, "none", LAGOON, 2) + T(52, 71, "Search name, street, phone", 13, MUTE) + table(100, M[:6]), "Search bar")),
      ("chips", "Filter Chips", "Tap Plan, Area or Status chips to narrow the list.", "guided",
       F(topbar() + chips_row(46, ["All", "Core", "Plus", "Premier"]) + chips_row(74, ["Any area", "Royal Oak", "Troy", "Novi"], active=-1, c=JUNGLE) + chips_row(102, ["Active", "Paused", "Overdue"], active=-1, c=TERRA) + table(132, M[:6]), "Filter chips")))
    # 7 sort/group
    def grouped(key, labels):
        s = topbar() + search(); y = 82
        for lab in labels:
            s += T(14, y + 12, lab.upper(), 10, JUNGLE, 700, extra='letter-spacing="1"') + L(14, y + 18, 438, y + 18, JUNGLE + "55"); y += 24
            for mm in [x for x in M if key(x) == lab][:3]:
                s += T(24, y + 12, mm[0], 11.5, INK, 600) + chip(220, y, mm[1], PLC[mm[1]], "soft", 8.5)[0] + chip(300, y, mm[3], STC[mm[3]], "dot", 9.5)[0] + T(430, y + 12, mm[4], 10.5, MUTE, anchor="end"); y += 24
            y += 6
        return s
    P("Find", LOC, "Grouping", "should the catalog group members by plan or list them A to Z?",
      ("plan", "Grouped By Plan", "Premier, Plus and Core headers with members under each.", "guided", F(grouped(lambda x: x[1], ["Premier", "Plus", "Core"]), "Grouped by plan")),
      ("az", "Plain A To Z", "One alphabetical list with a sort menu for other orders.", "calm",
       F(topbar() + search(44, 330) + R(352, 44, 86, 26, WHITE, "#CFC6B6", 13) + T(364, 61, "Sort: A-Z", 10, INK, 600) + chev(426, 57) + table(82, M[:8]), "A to Z with sort menu")))
    # 8 alphabet bar
    AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def side_az():
        s = topbar() + search(44, 400) + table(82, M[:8], xs=(14, 150, 215, 290, 360))
        for i, ch in enumerate(AL): s += T(440, 86 + i * 14.5, ch, 9, TERRA if ch in "ABCDEFGH" else "#B8AFA2", 700, "middle")
        return s
    def top_az():
        s = topbar() + search(); x = 14
        for ch in AL: s += R(x, 78, 14.5, 18, TERRA if ch == "A" else WHITE, LINE if ch != "A" else TERRA, 3) + T(x + 7.2, 91, ch, 9, WHITE if ch == "A" else (INK if ch in "ABCDEFGH" else "#B8AFA2"), 600, "middle"); x += 16.3
        return s + table(104, M[:7])
    P("Find", LOC, "Alphabet jump bar", "should the A to Z jump bar run down the side or across the top?",
      ("side", "Down The Right Edge", "A slim letter rail, like a phone contacts list.", "subtle", F(side_az(), "Side letter rail")),
      ("top", "Across The Top", "Letter buttons in a row above the list.", "guided", F(top_az(), "Top letter row")))
    # 9 status chip styles
    def stat(style):
        s = topbar() + search(); y = 86
        for mm in M[:8]:
            s += R(14, y, 424, 40, WHITE, LINE, 8) + ini(34, y + 20, 11, mm[0], PLC[mm[1]]) + T(54, y + 24, mm[0], 12, INK, 600) + chip(330, y + 11, mm[3], STC[mm[3]], style, 10)[0]; y += 46
        return s
    P("Chips", LOC, "Status chips", "should member status show as a soft pill or as a small coloured dot?",
      ("pill", "Soft Tinted Pill", "A pale coloured pill with the word inside.", "friendly", F(stat("soft"), "Soft pill")),
      ("dot", "Dot And Word", "A small coloured dot beside a plain word.", "subtle", F(stat("dot"), "Dot and word")))
    # 10 plan tier badges
    def tier(style):
        s = topbar(); y = 50
        for mm in M[:3] + M[3:6]:
            s += R(14, y, 424, 58, WHITE, LINE, 8)
            if style == "edge": s += R(14, y, 6, 58, PLC[mm[1]], rx=3) + T(34, y + 25, mm[0], 13, INK, 600) + T(34, y + 44, mm[1].upper() + " PLAN", 9.5, PLC[mm[1]], 700, extra='letter-spacing="1.2"')
            else:
                tiers = {"Core": 1, "Plus": 2, "Premier": 3}[mm[1]]
                s += T(28, y + 25, mm[0], 13, INK, 600) + chip(28, y + 32, mm[1], PLC[mm[1]], "outline", 9.5)[0] + "".join(R(380 + i * 16, y + 22, 12, 12, PLC[mm[1]] if i < tiers else "#E7E0D4", rx=2) for i in range(3))
            y += 66
        return s
    P("Chips", LOC, "Plan tier badge", "should the plan show as a coloured edge with a label or as a badge with tier blocks?",
      ("edge", "Colour Edge And Label", "A tier colour down the card edge, plan name in caps.", "subtle", F(tier("edge"), "Colour edge")),
      ("badge", "Badge With Tier Blocks", "An outlined plan badge plus one, two or three blocks.", "guided", F(tier("badge"), "Badge with tier blocks")))
    # 11 home info layout
    def home_kv():
        s = topbar("Avery Sample", "Home") + head(m)
        g, h = section(96, "Home", True, home_rows(m) + [("Heating", "Gas furnace, 2015"), ("Cooling", "Central air, 2018"), ("Water heater", "Tank, 2020"), ("Roof", "Shingle, 2012")], JUNGLE); return s + g
    def home_vis():
        s = topbar("Avery Sample", "Home") + head(m)
        for i, (big_, sm, c) in enumerate((("1952", "Built", JUNGLE), ("1,480", "Sq ft", LAGOON), ("4", "Systems", TERRA))):
            x = 14 + i * 144; s += R(x, 98, 136, 64, CREAM, LINE, 8) + T(x + 14, 136, big_, 26, c, f="khand") + T(x + 14, 152, sm, 10, MUTE)
        s += T(14, 186, "PHOTOS", 9.5, MUTE, 700, extra='letter-spacing="1"')
        for i in range(3):
            x = 14 + i * 104; s += R(x, 194, 96, 70, SOFT, LINE, 6) + f'<path d="M{x+22} 254 l26 -28 l26 28 z" fill="{JUNGLE}44"/>' + R(x + 38, 238, 20, 16, WHITE)
        s += R(334, 194, 104, 70, WHITE, LINE, 6, 1, 'stroke-dasharray="4 3"') + T(386, 233, "Carousel", 10, MUTE, 600, "middle") + chev(386, 246, MUTE, False)
        y = 282
        for nm, yr in (("Gas furnace", "2015"), ("Central air", "2018"), ("Water heater", "2020"), ("Shingle roof", "2012")): s += C(22, y + 8, 3, JUNGLE) + T(32, y + 12, nm, 11, INK, 500) + T(438, y + 12, yr, 10.5, MUTE, anchor="end") + L(14, y + 20, 438, y + 20); y += 26
        return s
    P("Home info", LOC, "Home info layout", "should home details be a plain list or big number tiles with a photo strip?",
      ("list", "Plain Detail List", "Every home fact and system as label and value rows.", "calm", F(home_kv(), "Detail list")),
      ("tiles", "Number Tiles And Photos", "Age, size and systems up top, a photo carousel below.", "friendly", F(home_vis(), "Tiles and photo carousel")))
    # 12 contact layout
    def contact_a():
        s = topbar("Avery Sample", "Contact") + head(m)
        g, h = section(96, "Contact", True, contact_rows(m) + [("Second contact", "Jordan Sample")], LAGOON); return s + g
    def contact_b():
        s = topbar("Avery Sample", "Contact") + head(m) + R(14, 96, 424, 66, LAGOON + "10", LAGOON + "55", 10)
        s += T(28, 118, "PREFERS TEXT", 10, LAGOON, 700, extra='letter-spacing="1.2"') + T(28, 140, m[5], 17, INK, f="khand") + T(28, 154, "Best time: weekday evenings", 10, MUTE)
        s += R(330, 116, 94, 28, LAGOON, rx=14) + T(377, 134, "Text now", 11, WHITE, 600, "middle")
        y = 176
        for k, v in (("Email", m[6]), ("Phone", m[5]), ("Second contact", "Jordan Sample")): s += T(28, y + 13, k, 10, MUTE) + T(424, y + 13, v, 10.5, INK, 600, "end") + L(28, y + 19, 424, y + 19); y += 22
        return s
    P("Contact", LOC, "Contact layout", "should preferred contact and best time be one row in the list or a highlighted box on top?",
      ("rows", "Rows In The List", "Preferred contact and best time sit with the other rows.", "calm", F(contact_a(), "Rows in the list")),
      ("box", "Highlighted Preferred Box", "A lagoon box up top: how and when to reach them.", "guided", F(contact_b(), "Preferred box on top")))
    # 13 quick actions
    P("Contact", LOC, "Quick actions", "should call, text, email and client page be labelled buttons or round icon buttons?",
      ("btn", "Labelled Buttons", "Word buttons in a row under the member name.", "practical", F(topbar("Avery Sample", "Member") + head(m) + actions(100) + section(142, "Contact", True, contact_rows(m), LAGOON)[0], "Labelled buttons")),
      ("icon", "Round Icon Buttons", "Round buttons with a small word under each.", "friendly", F(topbar("Avery Sample", "Member") + head(m) + actions(98, 14, "icons") + section(150, "Contact", True, contact_rows(m), LAGOON)[0], "Round icon buttons")))
    # 14 membership block
    def mem_a():
        s = topbar("Avery Sample", "Membership") + head(m)
        g, h = section(96, "Membership", True, mem_rows(m) + [("Add-ons", "Gutter care, Lawn")], TERRA); return s + g
    def mem_b():
        s = topbar("Avery Sample", "Membership") + head(m) + R(14, 96, 424, 190, WHITE, LINE, 10) + R(14, 96, 424, 40, CREAM, rx=10) + R(14, 126, 424, 10, CREAM)
        s += T(28, 122, "Plus Plan", 18, JUNGLE, f="khand") + chip(352, 106, "Paid up", JUNGLE, "solid", 9.5)[0]
        s += L(40, 176, 410, 176, "#E2DACB", 4) + L(40, 176, 210, 176, TERRA, 4) + C(40, 176, 5, TERRA) + C(410, 176, 5, WHITE, TERRA, 2)
        s += T(40, 198, "Started Mar 3, 2026", 10, MUTE) + T(410, 198, "Renews Mar 3, 2027", 10, INK, 600, "end") + T(225, 164, "Month 7 of 12", 10, TERRA, 600, "middle")
        s += T(28, 232, "ADD-ONS", 9.5, MUTE, 700, extra='letter-spacing="1"') + chip(28, 242, "Gutter care", LAGOON)[0] + chip(120, 242, "Lawn", LAGOON)[0]
        return s
    P("Membership", LOC, "Membership block", "should plan, billing, dates and add-ons be a list or a plan card with a term bar?",
      ("list", "Simple List", "Plan, billing, start, renew and add-ons as rows.", "calm", F(mem_a(), "Membership list")),
      ("card", "Plan Card With Term Bar", "A plan card with a bar from start to renewal.", "friendly", F(mem_b(), "Plan card with term bar")))
    # 15 visit history
    V = [("Oct 3", "Fall tune-up", "Furnace filter, gutters"), ("Jul 8", "Summer visit", "AC check, caulk"), ("Apr 12", "Spring visit", "Sump pump test"), ("Mar 3", "Welcome walk", "Home record made")]
    def tl():
        s = topbar("Avery Sample", "Visits") + head(m) + L(40, 108, 40, 360, LAGOON + "66", 2); y = 104
        for i, (d, t_, n) in enumerate(V): s += C(40, y + 12, 6, LAGOON if i == 0 else WHITE, LAGOON, 2) + T(58, y + 10, d, 10, MUTE, 600) + T(58, y + 26, t_, 13, INK, 600) + T(58, y + 41, n, 10, MUTE); y += 64
        return s
    def vl():
        s = topbar("Avery Sample", "Visits") + head(m) + table(100, [], ("Date", "Visit", "Notes"), (14, 90, 220)); y = 122
        for d, t_, n in V: s += T(14, y + 18, d, 10.5, INK, 600) + T(90, y + 18, t_, 10.5, INK) + T(220, y + 18, n, 10.5, MUTE) + L(0, y + 28, 452, y + 28); y += 28
        return s
    P("Visits", LOC, "Visit history", "should past visits show as a timeline or as a simple list?",
      ("tl", "Timeline", "Dots down a line, newest at the top.", "friendly", F(tl(), "Timeline")),
      ("list", "Simple List", "Date, visit and notes in tidy rows.", "practical", F(vl(), "Visit list")))
    # 16 open items callout
    OI = [("Downspout loose at back corner", TERRA), ("Quote sent: attic insulation", LAGOON)]
    def oi_banner():
        s = topbar("Finley Notreal", "Member") + head(M[5]) + R(14, 96, 424, 80, TERRA + "12", TERRA + "66", 8) + R(14, 96, 4, 80, TERRA) + T(30, 116, "2 OPEN ITEMS", 10, TERRA, 700, extra='letter-spacing="1.2"'); y = 136
        for t_, c in OI: s += C(34, y - 4, 3, c) + T(44, y, t_, 11, INK, 500); y += 20
        return s + section(188, "Contact", False)[0] + section(220, "Home", False)[0] + section(252, "Membership", False)[0]
    def oi_drop():
        s = topbar("Finley Notreal", "Member") + head(M[5])
        s += R(14, 96, 424, 26, WHITE, LINE, 6) + T(26, 113, "Open items", 12, INK, 600) + C(110, 109, 9, TERRA) + T(110, 113, "2", 10, WHITE, 700, "middle") + chev(422, 109)
        return s + section(128, "Contact", False)[0] + section(160, "Home", False)[0] + section(192, "Membership", False)[0]
    P("Open items", LOC, "Open items callout", "should open items be a terracotta banner up top or a dropdown with a count?",
      ("banner", "Banner At The Top", "Open items listed in a soft terracotta box.", "bold", F(oi_banner(), "Open items banner")),
      ("drop", "Dropdown With A Count", "A closed dropdown with a small count badge.", "subtle", F(oi_drop(), "Open items dropdown")))
    # 17 notes area
    def notes_box():
        s = topbar("Avery Sample", "Notes") + head(m) + T(14, 110, "NOTES", 9.5, MUTE, 700, extra='letter-spacing="1"') + R(14, 118, 424, 120, "#FFFDF7", LINE, 8)
        for i, ln_ in enumerate(("Gate code is with the office (sample).", "Dog is friendly, keep side gate shut.", "Likes a text the day before a visit.")): s += T(28, 142 + i * 20, ln_, 11, INK)
        return s + T(424, 230, "Edited Oct 3", 9, MUTE, anchor="end")
    def notes_feed():
        s = topbar("Avery Sample", "Notes") + head(m) + R(14, 100, 424, 28, WHITE, "#CFC6B6", 14) + T(28, 118, "Add a note", 10.5, MUTE); y = 140
        for d, who, txt in (("Oct 3", "Office", "Likes a text the day before a visit."), ("Jul 8", "Tech", "Dog is friendly, keep side gate shut."), ("Mar 3", "Office", "Gate code is with the office (sample).")):
            s += R(14, y, 424, 50, WHITE, LINE, 8) + T(28, y + 18, f"{d}  ·  {who}", 9.5, LAGOON, 600) + T(28, y + 36, txt, 11, INK); y += 58
        return s
    P("Notes", LOC, "Notes area", "should notes be one shared note box or a dated list of notes?",
      ("box", "One Note Box", "A single editable note, like a sticky pad.", "calm", F(notes_box(), "One note box")),
      ("feed", "Dated Note List", "Each note dated and signed, newest first.", "practical", F(notes_feed(), "Dated note list")))
    # 18 empty / missing info
    def miss(style):
        s = topbar("Emery Fakename", "Member") + head(M[4]) + R(14, 96, 424, 30, CREAM, LINE, 6) + R(14, 96, 3, 30, LAGOON) + T(26, 115, "Contact", 12, INK, 600); y = 134
        for k, v in (("Phone", M[4][5]), ("Email", None), ("Prefers", None), ("Best time", "Mornings")):
            s += T(28, y + 13, k, 10, MUTE)
            if v: s += T(424, y + 13, v, 10.5, INK, 600, "end")
            elif style == "dash": s += T(424, y + 13, "Not added yet", 10.5, "#A39B8F", 400, "end", extra='font-style="italic"')
            else: s += R(330, y, 94, 18, WHITE, TERRA, 9, 1.2, 'stroke-dasharray="3 2"') + T(377, y + 13, "+ Add", 10, TERRA, 600, "middle")
            s += L(28, y + 19, 424, y + 19); y += 24
        if style == "add": s += R(14, y + 8, 424, 30, TERRA + "10", rx=6) + T(26, y + 27, "2 details missing. Add them on the next call.", 10.5, TERRA, 600)
        return s
    P("Missing info", LOC, "Missing info", "should a missing detail read Not added yet or show an Add button?",
      ("quiet", "Quiet Not Added Yet", "Grey italic text, nothing shouts.", "subtle", F(miss("dash"), "Quiet placeholder")),
      ("add", "Add Button And Nudge", "A dashed Add button plus a gentle missing count.", "guided", F(miss("add"), "Add button and nudge")))
    # 19 laptop split vs full page (with phone note)
    def split():
        s = topbar() + R(0, 34, 170, 436, SOFT) + search(44, 150, 10, "Search"); y = 80
        for i, mm in enumerate(M[:8]):
            s += (R(6, y - 2, 158, 40, WHITE, LAGOON, 6, 1.2) if i == 0 else "") + ini(26, y + 18, 10, mm[0], PLC[mm[1]]) + T(42, y + 16, mm[0], 10.5, INK, 600) + T(42, y + 30, mm[2], 9, MUTE); y += 44
        s += f'<g transform="translate(170,0) scale(.62)">{head(m, 70)}</g>'
        y = 120
        for i, (t_, rows, c) in enumerate((("Contact", contact_rows(m)[:3], LAGOON), ("Home", home_rows(m)[:3], JUNGLE), ("Membership", mem_rows(m)[:2], TERRA))):
            g, h = section(y, t_, True, rows, c, 262, 180); s += g; y += h + 4
        return s
    def full():
        s = topbar("Avery Sample", "Back to all members") + T(14, 52, "< All members", 10, LAGOON, 600) + head(m, 60); y = 112
        for i, (t_, rows, c) in enumerate((("Contact", contact_rows(m), LAGOON), ("Home", home_rows(m), JUNGLE), ("Membership", mem_rows(m)[:2], TERRA))):
            g, h = section(y, t_, i < 2, rows, c); s += g; y += h + 6
        return s
    P("Laptop view", LOC, "Laptop view", "on a laptop, should the list stay on the left with the member on the right or open a full page?",
      ("split", "List And Detail Split", "List on the left, member on the right; on a phone it stacks.", "focused", F(split(), "List-detail split")),
      ("full", "Full-Page Member", "Click a member to open a full page with a back link.", "calm", F(full(), "Full-page member")))
    # 19 photo vs initials
    P("Faces", LOC, "Member face", "should each member card show a home photo or initials in a circle?",
      ("photo", "Photo Of The Home", "A small home photo when one is on file.", "friendly", F(topbar() + search() + grid(82, M[:6], 3, 110, face="photo"), "Home photo")),
      ("ini", "Initials Circle", "Initials in the plan colour, always tidy.", "subtle", F(topbar() + search() + grid(82, M[:6], 3, 110, face="ini"), "Initials circle")))
    # 20 printable sheet
    def sheet(style):
        s = R(46, 8, 360, 452, WHITE, "#D3CABB", 2) + T(66, 40, "Smart Upkeep", 11, TERRA, 700) + T(66, 62, "Avery Sample", 20, INK, f="khand") + T(386, 40, "SAMPLE MEMBER SHEET", 8.5, MUTE, 700, "end", extra='letter-spacing="1"')
        if style == "one":
            y = 80
            for t_, rows in (("Contact", contact_rows(m)), ("Home", home_rows(m)), ("Membership", mem_rows(m))):
                s += T(66, y + 12, t_.upper(), 9, JUNGLE, 700, extra='letter-spacing="1"') + L(66, y + 17, 386, y + 17, JUNGLE); y += 22
                for k, v in rows: s += T(66, y + 10, k, 9.5, MUTE) + T(386, y + 10, v, 9.5, INK, 600, "end"); y += 16
                y += 8
        else:
            for ci, (t_, rows) in enumerate((("Contact", contact_rows(m)), ("Home", home_rows(m)))):
                x = 66 + ci * 166; s += R(x, 80, 154, 120, CREAM, rx=4) + T(x + 10, 98, t_.upper(), 9, JUNGLE, 700); y = 112
                for k, v in rows: s += T(x + 10, y + 8, k, 8, MUTE) + T(x + 10, y + 19, v, 9, INK, 600); y += 22
            s += R(66, 212, 320, 70, CREAM, rx=4) + T(76, 230, "MEMBERSHIP", 9, JUNGLE, 700) + T(76, 250, "Plus  ·  Paid up  ·  Renews Mar 3, 2027", 10, INK, 600)
            s += R(66, 294, 320, 110, WHITE, LINE, 4) + T(76, 312, "TECH NOTES", 9, MUTE, 700) + "".join(L(76, 332 + i * 20, 376, 332 + i * 20, LINE) for i in range(4))
        return s
    P("Print", LOC, "Printable member sheet", "should the printed sheet be one clean column or boxed sections with space to write?",
      ("one", "One Clean Column", "Every fact in one column, saves ink.", "calm", F(sheet("one"), "One clean column")),
      ("boxes", "Boxed With Write-In Lines", "Cream boxes plus blank lines for tech notes.", "practical", F(sheet("boxes"), "Boxed with write-in lines")))
    return pairs
