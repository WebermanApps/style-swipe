"""Technicians Board Layout Deck (Oct 19 2026, Max via UpKeep Develop 12:04 ICT, sections confirmed 12:07 ICT): the decided Technicians
board sections in order (Documents, tech-only company calendar, who's working this week, urgent and safety flags with gas, electrical,
CO and flooding pinned at the top, visits log with photos and notes; ping log in the branded footer; day/week/month on every section).
Pairs are only about how each looks. Certifications and Training is OPTIONAL and shown only in pairs labelled Optional.
12 this-or-that pairs. Sample techs Tech Dash 1-3, everything tagged TEST / SAMPLE."""
from md1018_kit import make
from ukhf1019_kit import *
TECH = [("Tech Dash 1", TERRA, "Van 1", "North area"), ("Tech Dash 2", LAGOON, "Van 2", "East area"), ("Tech Dash 3", JUNGLE, "Van 3", "West area")]
DAYS = ["Mon 19", "Tue 20", "Wed 21", "Thu 22", "Fri 23", "Sat 24", "Sun 25"]
VT = {"Tune-up": LAGOON, "Repair": TERRA, "Welcome walk": JUNGLE, "Seasonal": SAFF}
# (tech index, day index, start, visit type, home)
VIS = [(0, 0, "9:00", "Tune-up", "A"), (0, 0, "1:00", "Repair", "B"), (1, 0, "10:00", "Welcome walk", "C"), (2, 1, "9:30", "Seasonal", "D"),
       (0, 1, "11:00", "Tune-up", "E"), (1, 2, "8:30", "Repair", "F"), (2, 2, "2:00", "Tune-up", "G"), (0, 3, "9:00", "Seasonal", "H"),
       (1, 3, "1:30", "Tune-up", "J"), (2, 4, "10:00", "Repair", "K"), (1, 4, "3:00", "Welcome walk", "L"), (0, 5, "10:00", "Tune-up", "M")]
WORK = [[1, 1, 1, 1, 0, 1, 0], [1, 0, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 0, 0]]
FLAGS = [("Gas", "Gas smell at SAMPLE home A", "Tech Dash 2", "Today 10:15 AM", True), ("Electrical", "None open", "", "", False),
         ("CO", "CO alarm at SAMPLE home D", "Tech Dash 1", "Today 8:30 AM", True), ("Flooding", "None open", "", "", False)]
OTHER = [("Urgent", "No heat at SAMPLE home N, elderly member", "Tech Dash 3", "Yesterday"), ("Safety", "Loose ladder foot on Van 2", "Tech Dash 2", "Oct 17")]
LOGS = [("Oct 19", "Tech Dash 1", "Tune-up", "SAMPLE home A", "Furnace filter swapped, gutters cleared, sump pump tested."),
        ("Oct 18", "Tech Dash 2", "Repair", "SAMPLE home F", "Leaky trap under kitchen sink resealed, member shown the fix."),
        ("Oct 17", "Tech Dash 3", "Seasonal", "SAMPLE home D", "Hose bibs shut off, window seals checked, two photos of attic.")]
CERTS = [("EPA 608", ["Mar 2028", "Nov 2026", "Open"]), ("Lead-Safe", ["Jan 2027", "Dec 2026", "Jun 2027"]), ("OSHA 10", ["No expiry", "No expiry", "Open"]), ("CPR", ["Nov 2026", "Aug 2027", "May 2027"])]
def seg(x, y, act="Week", w=150, h=20):
    g = R(x, y, w, h, WHITE, "#B9AE9C", h / 2, 1.1); sw = w / 3
    for i, s in enumerate(("Day", "Week", "Month")):
        if s == act: g += R(x + i * sw + 2, y + 2, sw - 4, h - 4, INK, rx=(h - 4) / 2)
        g += T(x + i * sw + sw / 2, y + h * .68, s, 9.5, WHITE if s == act else INK, 600, "middle")
    return g
def tabs(x, y, act="Week"):
    g = ""
    for i, s in enumerate(("Day", "Week", "Month")):
        xx = x + i * 50; g += T(xx + 22, y + 13, s, 10.5, LAGOON if s == act else MUTE, 600, "middle")
        if s == act: g += R(xx + 4, y + 18, 36, 2.5, LAGOON)
    return g + L(x, y + 20.5, x + 150, y + 20.5)
def sec_title(y, title, open_, body, summ, per=None):
    if per: return fold(y, title, None, open_, body, right=None) + (seg(306, y + 3, "Week", 96, 18)[:0] + small_seg(306, y + 4)), 
    return fold(y, title, None, open_, body, right=summ, rcol=INK if open_ else MUTE)
def small_seg(x, y, act="Week", kind="seg"):
    if kind == "tabs":
        g = ""
        for i, s in enumerate(("D", "W", "M")): g += T(x + 10 + i * 22, y + 12, s, 9, LAGOON if s == act[0] else MUTE, 700, "middle") + (R(x + 4 + i * 22, y + 15, 12, 2, LAGOON) if s == act[0] else "")
        return g
    return seg(x, y, act, 96, 16).replace('font-size="9.5"', 'font-size="8"')
# ---------- section bodies (return svg, height) ----------
def cal_grid(y, colour="tech", view="Week"):
    if view == "Month": return cal_month(y, colour)
    x0, cw = 84, 50; g = "".join(T(x0 + i * cw + cw / 2, y + 12, d, 8.5, MUTE, 700, "middle") for i, d in enumerate(DAYS)) + L(24, y + 17, 428, y + 17)
    for ti, (nm, c, van, area) in enumerate(TECH):
        yy = y + 20 + ti * 40; g += R(24, yy, 3, 36, c) + T(32, yy + 15, nm, 9.5, INK, 600) + T(32, yy + 27, van, 8, MUTE)
        for di in range(7):
            g += R(x0 + di * cw + 1, yy, cw - 2, 36, CREAM if WORK[ti][di] else "#F1EDE6")
            vs = [v for v in VIS if v[0] == ti and v[1] == di]
            for k, v in enumerate(vs[:2]):
                cc = c if colour == "tech" else VT[v[3]]
                g += R(x0 + di * cw + 3, yy + 2 + k * 17, cw - 6, 15, cc + "22", cc, 2, 1) + T(x0 + di * cw + 6, yy + 12.5 + k * 17, f"{v[2]} {v[3][:8]}", 7, INK, 600)
            if not WORK[ti][di]: g += T(x0 + di * cw + cw / 2, yy + 22, "Off", 8, "#A39B8F", 500, "middle")
    yy = y + 20 + 3 * 40 + 4
    if colour == "type":
        x = 24
        for k, c in VT.items(): g += R(x, yy + 2, 9, 9, c + "33", c, 2) + T(x + 13, yy + 10, k, 8, MUTE); x += 74
    else:
        x = 24
        for nm, c, *_ in TECH: g += R(x, yy + 2, 9, 9, c + "33", c, 2) + T(x + 13, yy + 10, nm, 8, MUTE); x += 74
    return g + T(428, yy + 10, "Techs only: no member or tool bookings", 8, MUTE, 500, "end"), yy + 16 - y
def cal_agenda(y, colour="tech"):
    g = ""; yy = y
    for di in range(2):
        g += T(24, yy + 12, DAYS[di].upper() + " OCT", 8.5, JUNGLE, 700, extra='letter-spacing="1"') + L(24, yy + 16, 428, yy + 16, JUNGLE + "55"); yy += 20
        for v in [v for v in VIS if v[1] == di]:
            c = TECH[v[0]][1] if colour == "tech" else VT[v[3]]
            g += C(30, yy + 8, 3.5, c) + T(40, yy + 11, v[2] + " AM" if v[2] < "5" and len(v[2]) > 4 or v[2] in ("9:00", "9:30", "8:30") else v[2] + " PM", 9, INK, 600) + T(100, yy + 11, TECH[v[0]][0], 9, c, 600) + T(176, yy + 11, v[3], 9, INK) + T(428, yy + 11, "SAMPLE home " + v[4], 8.5, MUTE, anchor="end"); yy += 17
        yy += 4
    return g + T(24, yy + 8, "Wed 21 to Sun 25 below  ·  techs only", 8, MUTE, 500), yy + 14 - y
def cal_month(y, colour="dots"):
    cw, ch = 58, 26; g = "".join(T(24 + i * cw + cw / 2, y + 10, d, 8, MUTE, 700, "middle") for i, d in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")))
    for wk in range(5):
        for d in range(7):
            n = wk * 7 + d - 2  # Oct 1 2026 is a Thursday
            x, yy = 24 + d * cw, y + 14 + wk * ch; g += R(x + 1, yy, cw - 2, ch - 2, CREAM if 0 <= n < 31 else "#F4F1EC", LINE, 2)
            if 0 <= n < 31:
                g += T(x + 5, yy + 10, str(n + 1), 7.5, INK if n != 18 else LAGOON, 700 if n == 18 else 500)
                cnt = [(n * 3 + k) % 4 for k in range(3)] if d < 6 else [0, (n % 2), 0]
                if colour == "dots":
                    for k, (nm, c, *_) in enumerate(TECH):
                        for j in range(min(cnt[k], 3)): g += C(x + 8 + j * 5 + k * 16, yy + 18, 1.8, c)
                else:
                    tot = sum(cnt)
                    if tot: g += R(x + cw - 24, yy + 12, 19, 10, LAGOON + "22", rx=5) + T(x + cw - 14.5, yy + 19.5, str(tot), 7, LAGOON, 700, "middle")
    return g, 14 + 5 * ch + 4
def who_cards(y):
    g = ""; w = 134
    for i, (nm, c, van, area) in enumerate(TECH):
        x = 24 + i * (w + 4); g += R(x, y, w, 76, WHITE, LINE, 6) + R(x, y, w, 3, c) + T(x + 10, y + 19, nm, 12, INK, f="khand")
        on = WORK[i][0]; g += chip(x + w - 60, y + 9, "On today" if on else "Off today", JUNGLE if on else MUTE, "dot", 7.5)[0]
        g += T(x + 10, y + 32, f"{van}  ·  {area}", 8, MUTE)
        for d, lt in enumerate("MTWTFSS"): g += C(x + 14 + d * 16, y + 46, 6, c if WORK[i][d] else WHITE, c if WORK[i][d] else "#CFC6B6", 1.1) + T(x + 14 + d * 16, y + 49, lt, 7, WHITE if WORK[i][d] else MUTE, 700, "middle")
        g += T(x + 10, y + 68, f"{sum(WORK[i])} days this week  ·  {sum(1 for v in VIS if v[0]==i)} visits", 8, INK, 500)
    return g, 84
def who_table(y):
    x0, cw = 110, 40; g = T(24, y + 12, "TECH", 8, MUTE, 700) + "".join(T(x0 + i * cw + cw / 2, y + 12, d[:3], 8, MUTE, 700, "middle") for i, d in enumerate(DAYS)) + T(428, y + 12, "VISITS", 8, MUTE, 700, "end") + L(24, y + 17, 428, y + 17)
    for i, (nm, c, van, area) in enumerate(TECH):
        yy = y + 20 + i * 22; g += C(30, yy + 9, 3.5, c) + T(40, yy + 12, nm, 9.5, INK, 600)
        for d in range(7): g += R(x0 + d * cw + 3, yy + 2, cw - 6, 16, c + "26" if WORK[i][d] else "#F1EDE6", rx=3) + T(x0 + d * cw + cw / 2, yy + 13, "On" if WORK[i][d] else "Off", 8, INK if WORK[i][d] else "#A39B8F", 600, "middle")
        g += T(428, yy + 13, str(sum(1 for v in VIS if v[0] == i)), 9.5, INK, 700, "end") + L(24, yy + 20, 428, yy + 20)
    return g, 20 + 3 * 22 + 4
def hz_tag(x, y, hz, colour):
    c = HAZ.get(hz, TERRA) if colour == "per" else TERRA
    cw = len(hz) * 8.5 * .62 + 14; return R(x, y, cw, 14, c, rx=2) + T(x + cw / 2, y + 10, hz.upper(), 7.5, WHITE, 700, "middle", extra='letter-spacing=".6"'), cw
def flags_banner(y, colour="one"):
    act = [f for f in FLAGS if f[4]]; h = 30 + len(act) * 18
    g = R(24, y, 404, h, TERRA + "12", TERRA, 3, 1.2) + R(24, y, 4, h, TERRA) + T(36, y + 15, "PINNED HAZARDS", 10.5, TERRA, f="khand", extra='letter-spacing="1.2"'); x = 136
    for f in FLAGS:
        t_, w = hz_tag(x, y + 5, f[0], colour); g += t_ if f[4] else R(x, y + 5, w, 14, WHITE, "#CFC6B6", 2) + T(x + w / 2, y + 15, f[0].upper(), 7.5, MUTE, 700, "middle"); x += w + 5
    g += T(420, y + 15, "2 open", 9, TERRA, 700, "end")
    for i, f in enumerate(act): g += warn(36, y + 23 + i * 18, HAZ[f[0]] if colour == "per" else TERRA, 11) + T(52, y + 32 + i * 18, f[1], 9.5, INK, 600) + T(420, y + 32 + i * 18, f"{f[2]}  ·  {f[3]}", 8, MUTE, anchor="end")
    yy = y + h + 6
    for o in OTHER: g += hz_tag(24, yy, o[0], "one")[0] + T(86, yy + 11, o[1], 9, INK) + T(428, yy + 11, f"{o[2]}  ·  {o[3]}", 8, MUTE, anchor="end") + L(24, yy + 18, 428, yy + 18); yy += 22
    return g, yy - y
def flags_cards(y, colour="one"):
    g = ""; w = 98
    for i, f in enumerate(FLAGS):
        x = 24 + i * (w + 4.7); c = (HAZ[f[0]] if colour == "per" else TERRA) if f[4] else "#B9AE9C"
        g += R(x, y, w, 64, (c + "12") if f[4] else WHITE, c, 5, 1.3 if f[4] else 1) + R(x, y, w, 4, c, rx=2) + warn(x + 8, y + 11, c, 11) + T(x + 24, y + 21, f[0].upper(), 10, c if f[4] else MUTE, f="khand", extra='letter-spacing="1"')
        g += T(x + 8, y + 38, (f[1][:20] + "...") if len(f[1]) > 21 else f[1], 7.5, INK if f[4] else MUTE, 600) + T(x + 8, y + 52, f"{f[2]}, {f[3][6:]}" if f[4] else "All clear  ·  pinned", 7, MUTE)
    yy = y + 72 + 2
    g += T(24, yy + 8, "OTHER URGENT AND SAFETY FLAGS", 7.5, MUTE, 700, extra='letter-spacing="1"'); yy += 14
    for o in OTHER: g += hz_tag(24, yy, o[0], "one")[0] + T(86, yy + 11, o[1], 9, INK) + T(428, yy + 11, f"{o[2]}  ·  {o[3]}", 8, MUTE, anchor="end") + L(24, yy + 18, 428, yy + 18); yy += 22
    return g, yy - y
def logs_strip(y):
    g = ""; yy = y
    for d, tch, ty, home, note in LOGS[:2]:
        c = [t[1] for t in TECH if t[0] == tch][0]
        g += R(24, yy, 404, 76, WHITE, LINE, 6) + R(24, yy, 3, 76, c) + T(34, yy + 15, f"{d}  ·  {tch}  ·  {ty}  ·  {home}", 9, INK, 600) + lab_chip(380, yy + 5, "TEST", "soft", 7)[0]
        g += T(34, yy + 29, note, 8.5, MUTE)
        for k in range(5): g += photo(34 + k * 62, yy + 36, 58, 34, c)
        g += T(420, yy + 58, "+2 photos", 8, LAGOON, 600, "end"); yy += 82
    return g, yy - y
def logs_grid(y):
    g = ""
    for i in range(8):
        r, c_ = divmod(i, 4); x = 24 + c_ * 102; yy = y + r * 72; d, tch, ty, home, note = LOGS[i % 3]; c = [t[1] for t in TECH if t[0] == tch][0]
        g += photo(x, yy, 98, 52, c) + T(x, yy + 62, f"{d}  ·  {tch}", 7.5, INK, 600)
    g += R(24, y + 148, 404, 22, CREAM, LINE, 4) + T(32, y + 162, "Click a photo for its visit notes  ·  SAMPLE home A: filter swapped, gutters cleared", 8, MUTE)
    return g, 176
def cert_table(y):
    x0 = 120; cw = 102; g = R(24, y, 404, 18, SOFT) + T(30, y + 12.5, "CERT", 7.5, MUTE, 700) + "".join(T(x0 + i * cw, y + 12.5, t[0].upper(), 7.5, MUTE, 700) for i, t in enumerate(TECH)); yy = y + 18
    for nm, ex in CERTS:
        g += T(30, yy + 14, nm, 9.5, INK, 600)
        for i, e in enumerate(ex):
            soon = e in ("Nov 2026", "Dec 2026"); col = TERRA if soon else (SAFF if e == "Open" else INK)
            g += T(x0 + i * cw, yy + 14, ("Expires " + e) if e not in ("Open", "No expiry") else e, 8.5, col, 600 if soon or e == "Open" else 500)
            if soon: g += chip(x0 + i * cw + 66, yy + 4, "Renew", TERRA, "soft", 7)[0]
        g += L(24, yy + 20, 428, yy + 20); yy += 20
    return g, yy - y + 4
def cert_badges(y):
    g = ""; w = 132
    for i, (nm, c, *_) in enumerate(TECH):
        x = 24 + i * (w + 4); g += R(x, y, w, 96, WHITE, LINE, 6) + T(x + 8, y + 15, nm, 11, INK, f="khand")
        for k, (cn, ex) in enumerate(CERTS):
            bx, by = x + 8 + (k % 2) * 62, y + 22 + (k // 2) * 36; e = ex[i]; soon = e in ("Nov 2026", "Dec 2026")
            bc = TERRA if soon else (SAFF if e == "Open" else JUNGLE)
            g += R(bx, by, 58, 32, bc + "14", bc, 4, 1.1) + T(bx + 29, by + 13, cn, 8, bc, 700, "middle") + T(bx + 29, by + 25, e if e in ("Open", "No expiry") else "to " + e, 7, INK, 500, "middle")
    return g, 104
def train_bar(y):
    g = T(24, y + 10, "TRAINING WEEK  ·  OCT 19 TO OCT 23  ·  SAMPLE", 7.5, MUTE, 700, extra='letter-spacing="1"'); yy = y + 18
    for i, (nm, c, *_) in enumerate(TECH):
        p = (.6, .8, .4)[i]; g += T(24, yy + 11, nm, 9.5, INK, 600) + R(110, yy + 4, 260, 9, "#E8E2D7", rx=4.5) + R(110, yy + 4, 260 * p, 9, c, rx=4.5) + T(428, yy + 12, f"{int(p*5)} of 5 days", 8.5, INK, 600, "end"); yy += 20
    return g, yy - y + 2
def train_check(y):
    items = ["Safety walk-through", "Van and tool bag check", "Ride-along day", "Shadow a member visit", "Sign-off with Ethan"]
    g = T(24, y + 10, "TRAINING WEEK  ·  TECH DASH 3  ·  SAMPLE", 7.5, MUTE, 700, extra='letter-spacing="1"'); yy = y + 16
    for k, it in enumerate(items): g += check(26, yy + 2, k < 2) + T(42, yy + 11, it, 9.5, MUTE if k < 2 else INK, 500) + T(428, yy + 11, ("Done Mon", "Done Tue", "Wed", "Thu", "Fri")[k], 8.5, JUNGLE if k < 2 else MUTE, 600, "end"); yy += 17
    return g, yy - y + 2
SECS = [("cal", "Company Calendar", "12 visits this week  ·  techs only"), ("who", "Technicians This Week", "3 techs  ·  2 on today"),
        ("flags", "Urgent And Safety Flags", "2 hazards open  ·  gas, CO"), ("logs", "Visits Log", "3 visits logged  ·  photos and notes")]
def tboard(open_="cal", body=None, sw="seg", scope="global", extra=None, show_docs_row=True, dense=False):
    g, y = mini_header("Technicians Command Center")
    s, h = mini_folds(y, [("Emergency Alerts", 2, True), ("To-Do List", 3, False), ("Documents Center", 2, False)]); g += s; y += h
    if scope == "global":
        g += T(14, y + 14, "Week of Oct 19  ·  every section follows this view", 9, MUTE, 500) + (seg(288, y, "Week") if sw == "seg" else tabs(288, y - 2)); y += 28
    secs = list(SECS) + ([extra[0]] if extra else [])
    for key, title, summ in secs:
        if dense:
            b, bh = body[key](y + 26); g += fold(y, title, None, True, bh + 4, right=summ, rcol=INK) + b; y += bh + 34; continue
        if key == open_:
            b, bh = body(y + 26 + (24 if scope == "section" else 0))
            g += fold(y, title, None, True, bh + 6 + (24 if scope == "section" else 0), right=summ if scope == "global" else None, rcol=INK)
            if scope == "section": g += (seg(272, y + 30, "Week") if sw == "seg" else tabs(272, y + 28)) + T(24, y + 44, "Week of Oct 19", 9, MUTE, 500)
            g += b; y += bh + 36 + (24 if scope == "section" else 0)
        else:
            g += fold(y, title, None, False, right=summ if scope == "global" else None)
            if scope == "section": g += small_seg(300, y + 4, "Week", sw)
            y += 30
    g += fold(min(max(y, 410), 418), "Ping Record", 5, False, right="In the branded footer", h=20, size=11)
    return g + bym(452)
def T_TECH():
    pairs, P = make("uktl19_", "UpKeep"); F = lambda s, n: frame(s, n, "technicians board", "TEST  ·  SAMPLE"); LOC = "Technicians Board"
    CAL = lambda y: cal_grid(y)
    P("View switcher", LOC, "Day week month switcher", "should the day, week and month switcher be a segmented control or a row of tabs?",
      ("seg", "Segmented Control", "One rounded control, the chosen view filled dark.", "modern", F(tboard("cal", CAL, "seg"), "Segmented control")),
      ("tabs", "Row Of Tabs", "Day, Week, Month as tabs with a lagoon underline.", "familiar", F(tboard("cal", CAL, "tabs"), "Tabs")))
    P("View switcher", LOC, "Switcher scope", "should one switcher at the top set every section or should each section have its own?",
      ("global", "One Switcher For All", "Pick Week once and every section follows.", "simple", F(tboard("cal", CAL), "One global switcher")),
      ("section", "One Per Section", "Each fold carries its own small Day, Week, Month.", "flexible", F(tboard("who", who_cards, scope="section"), "Per-section switchers")))
    P("Calendar", LOC, "Calendar week style", "should the tech-only calendar be a week grid with a lane per tech or a day-by-day agenda list?",
      ("grid", "Week Grid, Lane Per Tech", "Seven day columns, one lane for each tech.", "visual", F(tboard("cal", CAL), "Week grid")),
      ("agenda", "Day-By-Day Agenda", "Day headers with each visit as a line.", "readable", F(tboard("cal", cal_agenda), "Agenda list")))
    P("Calendar", LOC, "Calendar colour", "should calendar visits be coloured by tech or by visit type?",
      ("tech", "Colour By Tech", "Terracotta, lagoon and jungle for Tech Dash 1-3.", "clear", F(tboard("cal", lambda y: cal_grid(y, "tech")), "By tech")),
      ("type", "Colour By Visit Type", "Tune-up, repair, welcome walk and seasonal colours.", "informative", F(tboard("cal", lambda y: cal_grid(y, "type")), "By visit type")))
    P("Calendar", LOC, "Month view", "in month view, should each day show coloured dots per tech or one visit count?",
      ("dots", "Dots Per Tech", "One small dot per visit in each tech's colour.", "visual", F(tboard("cal", lambda y: cal_month(y, "dots")), "Month dots")),
      ("count", "One Visit Count", "A small number chip per day, open a day for detail.", "calm", F(tboard("cal", lambda y: cal_month(y, "count")), "Month counts")))
    P("Technicians", LOC, "Who is working", "should who's working this week be one card per tech or a roster table with day columns?",
      ("cards", "Card Per Tech", "Van, area, day dots and visit count on each card.", "friendly", F(tboard("who", who_cards), "Tech cards")),
      ("table", "Roster Table", "Techs down the side, On or Off under each day.", "compact", F(tboard("who", who_table), "Roster table")))
    P("Urgent and safety", LOC, "Pinned hazards", "should gas, electrical, CO and flooding sit in one pinned banner or as four pinned cards?",
      ("banner", "One Pinned Banner", "A terracotta banner with the four hazard tags and open items.", "bold", F(tboard("flags", flags_banner), "Pinned banner")),
      ("cards", "Four Pinned Cards", "A card per hazard, all clear or open, always on top.", "structured", F(tboard("flags", flags_cards), "Pinned cards")))
    P("Urgent and safety", LOC, "Hazard colour", "should every hazard use terracotta or should each hazard have its own colour?",
      ("one", "Terracotta For All", "One warning colour, the word tells them apart.", "calm", F(tboard("flags", lambda y: flags_cards(y, "one")), "One colour")),
      ("per", "Colour Per Hazard", "Gas terracotta, electrical gold, CO charcoal, flooding lagoon.", "guided", F(tboard("flags", lambda y: flags_cards(y, "per")), "Colour per hazard")))
    P("Visits log", LOC, "Visit photos", "should each completed visit show a photo strip with its notes or should the log be a grid of thumbnails?",
      ("strip", "Photo Strip Per Visit", "Visit line, notes, then a row of photos.", "story", F(tboard("logs", logs_strip), "Photo strip")),
      ("grid", "Thumbnail Grid", "A grid of photos, click one for the visit notes.", "visual", F(tboard("logs", logs_grid), "Thumbnail grid")))
    mini = {"cal": lambda y: (T(24, y + 10, "Mon 19: 3 visits  ·  Tue 20: 2  ·  Wed 21: 2  ·  Thu 22: 2  ·  Fri 23: 2  ·  Sat 24: 1", 8.5, INK, 500), 14),
            "who": lambda y: (T(24, y + 10, "Tech Dash 1: Mon-Thu, Sat  ·  Tech Dash 2: Mon, Wed-Fri  ·  Tech Dash 3: Tue-Fri", 8.5, INK, 500), 14),
            "flags": lambda y: (warn(24, y + 1, TERRA, 10) + T(38, y + 10, "Gas at SAMPLE home A  ·  CO at SAMPLE home D  ·  electrical, flooding clear", 8.5, INK, 600), 14),
            "logs": lambda y: ("".join(photo(24 + k * 46, y, 42, 24) for k in range(6)) + T(306, y + 15, "3 visits, 14 photos", 8.5, MUTE), 26)}
    P("Density", LOC, "Section density", "should the sections load as closed folds with one-line summaries or all open with a short preview?",
      ("folds", "Closed Folds, One-Line Summary", "Each section closed, its summary on the right.", "calm", F(tboard(None, None), "Closed folds")),
      ("open", "All Open, Short Preview", "Every section open with a one-line preview.", "complete", F(tboard(None, mini, dense=True), "All open")))
    EX = [("cert", "Certifications And Training (Optional)", "Optional section  ·  SAMPLE")]
    P("Optional", LOC, "Optional certifications", "if the optional Certifications and Training section is added, should renewals be a table or badge cards per tech?",
      ("table", "Renewals Table", "EPA 608, Lead-Safe, OSHA 10 and CPR expiry by tech.", "precise", F(tboard("cert", cert_table, extra=EX), "Optional: renewals table")),
      ("badges", "Badge Cards Per Tech", "A card per tech with four dated cert badges.", "visual", F(tboard("cert", cert_badges, extra=EX), "Optional: badge cards")))
    P("Optional", LOC, "Optional Training Week", "if the optional section is added, should Training Week show a progress bar per tech or a checklist?",
      ("bar", "Progress Bar Per Tech", "Days done out of five, one bar per tech.", "glanceable", F(tboard("cert", train_bar, extra=EX), "Optional: progress bars")),
      ("check", "Checklist", "Each training step ticked off with its day.", "clear", F(tboard("cert", train_check, extra=EX), "Optional: checklist")))
    return pairs
