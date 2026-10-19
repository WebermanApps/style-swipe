"""Scheduling Board Layout Deck, Oct 19 2026 (Max's review relayed by Swatch). Drawn laptop mockups for the UpKeep Scheduling board:
Schedule (day/week/month, techs + visits, daily fill bar vs the 4-stop cap labelled TEST), Client Communications (one tracking card per
member: request type, what the home needs next, timing preference, status New / Slot Proposed / Waiting on Approval; NO contact buttons),
header To-Do, Needs Attention, folded dropdowns, plus optional cards. Light only, white/cream base, terracotta/lagoon/jungle, Khand + Hind.
PRIVACY: techs are Tech Dash 1-3 and Van 1-3; members show a first name or member ID only; no email/phone/street/zip/lat-lng. All TEST data."""
from md1018_kit import make
from mcd1019 import T, R, C, L, chev, chip, INK, MUTE, LINE, CREAM, WHITE, TERRA, LAGOON, JUNGLE, SOFT
from draft_svg import screen
LOC = "Scheduling Board"
TECHS = ["Tech Dash 1", "Tech Dash 2", "Tech Dash 3", "Van 1", "Van 2", "Van 3"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
FILL = [4, 3, 2, 4, 1]
MEM = [("Avery", "Book", "Gutter clean + check downspout", "Mornings", "New"),
       ("M-1042", "Reschedule", "Furnace filter, photo shows dust", "After 3pm", "Slot Proposed"),
       ("Jordan", "Cancel", "Hold: next visit not needed", "Any", "Waiting on Approval"),
       ("M-1107", "Book", "Caulk tub edge, tech note", "Weekends", "New"),
       ("Riley", "Reschedule", "Smoke alarm test, 2 photos", "Not Fridays", "Slot Proposed")]
STC = {"New": LAGOON, "Slot Proposed": JUNGLE, "Waiting on Approval": TERRA}
RQC = {"Book": JUNGLE, "Reschedule": LAGOON, "Cancel": TERRA}
def tag(): return R(18, 14, 96, 26, WHITE, "#B9AE9C", 4, 1.4, 'stroke-dasharray="4 3"') + T(66, 32, "TEST DATA", 13, MUTE, 700, "middle", extra='letter-spacing="1.5"')
def foot(s): return R(0, 556, 480, 44, WHITE) + L(0, 556, 480, 556, "#E8E0D2") + T(240, 584, s, min(18, 430 / (len(s) * .5)), INK, 600, "middle")
def frame(inner, note):
    s = R(14, 52, 452, 492, WHITE, "#D3CABB", 10, 1.4) + R(14, 52, 452, 22, SOFT, "none", 10) + R(14, 66, 452, 8, SOFT)
    s += "".join(C(28 + i * 11, 63, 3.2, "#CFC6B6") for i in range(3)) + R(70, 57, 220, 12, WHITE, LINE, 6) + T(78, 66.5, "scheduling.test", 8, MUTE)
    s += f'<g transform="translate(14,74)">{inner}</g>'
    return screen(f'<g transform="scale(.5)">{R(0,0,480,600,CREAM)}{s}{tag()}{foot(note)}</g>', CREAM)
def head(todo="button", title="Scheduling"):
    s = R(0, 0, 452, 30, WHITE) + L(0, 30, 452, 30) + T(10, 21, title, 16, INK, f="khand")
    if todo == "button": s += R(330, 7, 114, 17, TERRA + "14", TERRA, 8) + T(387, 19, "Max's To-Do  ·  15", 8.5, TERRA, 700, "middle")
    elif todo == "strip":
        x = 110
        for i, w in enumerate(["Cap per day?", "Zone order?", "Snow rule?", "+12 more"]):
            g, ww = chip(x, 8, w, TERRA if i < 3 else MUTE, "soft", 7.5); s += g; x += ww + 4
    return s
def sec(y, name, right=""):
    return T(10, y, name.upper(), 9, INK, 700, extra='letter-spacing="1.2"') + (T(442, y, right, 7.5, MUTE, 600, "end") if right else "") + L(10, y + 4, 442, y + 4)
def switcher(x, y, style="seg", on="Week"):
    s = ""
    for i, v in enumerate(["Day", "Week", "Month"]):
        a = v == on
        if style == "seg": s += R(x + i * 40, y, 40, 15, LAGOON if a else WHITE, LAGOON, 3 if i != 1 else 0) + T(x + i * 40 + 20, y + 11, v, 8, WHITE if a else LAGOON, 600, "middle")
        else: s += T(x + i * 40 + 20, y + 11, v, 8.5, LAGOON if a else MUTE, 700 if a else 500, "middle") + (R(x + i * 40 + 6, y + 14, 28, 2.5, LAGOON) if a else "")
    return s
def fill(x, y, w, n, style="blocks"):
    c = TERRA if n >= 4 else (JUNGLE if n <= 2 else LAGOON)
    if style == "blocks": s = "".join(R(x + i * (w / 4), y, w / 4 - 2, 5, c if i < n else "#E6DFD3", rx=1) for i in range(4))
    elif style == "bar": s = R(x, y, w, 5, "#EEE8DD", rx=2.5) + R(x, y, w * n / 4, 5, c, rx=2.5)
    else: s = T(x, y + 6, f"{n}/4", 8, c, 700)
    return s
def vchip(x, y, w, m, style="fill", c=LAGOON):
    if style == "fill": return R(x, y, w, 13, c + "26", rx=3) + T(x + 3, y + 9.5, m, 6.8, INK, 600)
    return R(x, y, w, 13, WHITE, LINE, 2) + R(x, y, 2.5, 13, c) + T(x + 5, y + 9.5, m, 6.8, INK, 600)
VIS = ["Avery", "M-1042", "Riley", "M-1107", "Jordan", "M-1210", "Sam", "M-1033"]
def week(y, h, layout="grid", fstyle="blocks", cstyle="fill", fill_lbl=True):
    s = ""
    if layout == "grid":
        cw = 432 / 5
        for d in range(5):
            x = 10 + d * cw
            s += R(x, y, cw - 2, h, WHITE, LINE, 3) + T(x + 4, y + 11, DAYS[d] + f" {19+d}", 8.5, INK, 700) + fill(x + 4, y + 15, cw - 12, FILL[d], fstyle)
            for k in range(FILL[d]):
                s += vchip(x + 3, y + 26 + k * 16, cw - 8, f"{VIS[(d+k)%8]} · {TECHS[(d+k)%6]}", cstyle, [LAGOON, JUNGLE, TERRA][(d + k) % 3])
    else:
        s += R(10, y, 432, 14, SOFT) + "".join(T(80 + d * 72 + 36, y + 10, DAYS[d], 8, MUTE, 700, "middle") for d in range(5))
        rh = (h - 16) / 6
        for i, t_ in enumerate(TECHS):
            yy = y + 16 + i * rh
            s += T(14, yy + rh / 2 + 3, t_, 8, INK, 600) + L(10, yy + rh, 442, yy + rh)
            for d in range(5):
                n = (FILL[d] + i) % 4 + (1 if i < 2 else 0); n = min(n, 4)
                s += fill(80 + d * 72 + 4, yy + 3, 64, n, fstyle)
                if (i + d) % 2 == 0: s += vchip(80 + d * 72 + 3, yy + 10, 66, VIS[(i + d) % 8], cstyle, [LAGOON, JUNGLE, TERRA][i % 3])
    if fill_lbl: s += T(442, y - 4, "Fill vs 4-stop cap (TEST)", 7, TERRA, 600, "end")
    return s
def month(y, h, style="bar"):
    s = "".join(T(10 + d * 62 + 31, y + 9, n, 7.5, MUTE, 700, "middle") for d, n in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
    ch = (h - 14) / 5
    for w in range(5):
        for d in range(7):
            x, yy = 10 + d * 62, y + 14 + w * ch; n = (w * 3 + d * 2) % 5 if d < 5 else 0
            s += R(x, yy, 60, ch - 2, WHITE if d < 5 else SOFT, LINE, 2) + T(x + 4, yy + 10, str(w * 7 + d + 1), 7.5, INK, 600)
            if d < 5 and n:
                if style == "bar": s += fill(x + 4, yy + ch - 12, 50, min(n, 4), "bar")
                else: s += "".join(C(x + 8 + k * 9, yy + ch - 10, 3, LAGOON) for k in range(min(n, 4))) + (T(x + 52, yy + ch - 7, "+", 8, TERRA, 700) if n > 4 else "")
    return s + T(442, y - 4, "Fill vs 4-stop cap (TEST)", 7, TERRA, 600, "end")
def dayv(y, h):
    s = ""
    for i, t_ in enumerate(TECHS):
        yy = y + i * (h / 6) - 4; n = [4, 3, 2, 4, 1, 3][i]
        s += T(14, yy + 14, t_, 8.5, INK, 700) + fill(14, yy + 19, 60, n, "blocks")
        for k in range(n): s += vchip(90 + k * 88, yy + 6, 84, f"{['9:00','11:00','1:30','3:30'][k]} {VIS[(i+k)%8]}", "stripe", [LAGOON, JUNGLE, TERRA][i % 3])
        s += L(10, yy + h / 6 - 2, 442, yy + h / 6 - 2)
    return s + T(442, y - 4, "Fill vs 4-stop cap (TEST)", 7, TERRA, 600, "end")
def schedule(o, y=40, h=200):
    s = sec(y, "Schedule", "Week of Oct 19 · TEST") + switcher(10, y + 10, o.get("sw", "seg"), o.get("view", "Week"))
    v = o.get("view", "Week")
    if v == "Week": s += week(y + 34, h - 34, o.get("layout", "grid"), o.get("fs", "blocks"), o.get("cs", "fill"))
    elif v == "Month": s += month(y + 34, h - 34, o.get("ms", "bar"))
    else: s += dayv(y + 34, h - 34)
    return s
def status(x, y, st, style="pill"):
    c = STC[st]
    if style == "hide": return ""
    if style == "pill": g, w = chip(x, y, st, c, "solid", 7); return g
    if style == "steps":
        i = list(STC).index(st)
        return "".join(C(x + 6 + k * 22, y + 7, 4, c if k <= i else "#E2DACB") + (L(x + 10 + k * 22, y + 7, x + 24 + k * 22, y + 7, c if k < i else "#E2DACB", 1.5) if k < 2 else "") for k in range(3)) + T(x + 72, y + 10, st, 7, c, 700)
    return C(x + 4, y + 7, 3.5, c) + T(x + 11, y + 10, st, 7.5, INK, 600)
def thumbs(x, y, n=2, big=False):
    s = ""
    for k in range(n):
        w = 34 if big else 16; s += R(x + k * (w + 3), y, w, w * .75, SOFT, LINE, 2) + f'<path d="M{x+k*(w+3)+3} {y+w*.7} l{w*.3} -{w*.4} l{w*.4} {w*.4} z" fill="{JUNGLE}55"/>'
    return s
def ccard(x, y, w, m, o):
    nm, rq, need, tm, st = m; lay = o.get("card", "stack"); ss = o.get("st", "pill")
    if lay == "row":
        s = R(x, y, w, 20, WHITE, LINE, 3) + T(x + 6, y + 13, nm, 8.5, INK, 700) + T(x + 52, y + 13, rq, 7.5, RQC[rq], 700) + T(x + 108, y + 13, need[:30], 7.5, INK)
        s += T(x + 250, y + 13, tm, 7.5, MUTE) + status(x + w - 96, y + 3, st, ss); return s, 23
    h = 58 if o.get("photo", "strip") == "big" else 52
    s = R(x, y, w, h, WHITE, LINE, 4)
    if o.get("rqs", "tag") == "edge": s += R(x, y, 3, h, RQC[rq]) + T(x + 8, y + 12, nm, 9.5, INK, 700) + T(x + 8 + len(nm) * 6, y + 12, "  " + rq, 7.5, RQC[rq], 700)
    else: s += T(x + 6, y + 12, nm, 9.5, INK, 700); g, _ = chip(x + 10 + len(nm) * 6, y + 3, rq, RQC[rq], "soft", 6.5); s += g
    s += T(x + 6, y + 25, "Next visit: " + need, 7.2, INK) + T(x + 6, y + 36, "Timing: " + tm, 7, MUTE)
    if o.get("photo", "strip") == "big": s += thumbs(x + w - 40, y + 18, 1, True) + T(x + w - 40, y + 52, "2 notes", 6.5, MUTE)
    else: s += thumbs(x + 6, y + 39, 3) + T(x + 64, y + 48, "tech notes", 6.5, MUTE)
    s += status(x + w - (len(st) * 7 * .56 + 18), y + 3, st, ss) if ss != "steps" else status(x + w - 150, y + 38, st, ss)
    return s, h + 5
def comms(o, y=250, h=180):
    s = sec(y, "Client Communications", "Tracking only · TEST")
    if o.get("layout", "list") == "board":
        cw = 432 / 3
        for i, st in enumerate(STC):
            x = 10 + i * cw; s += R(x, y + 10, cw - 4, h - 10, SOFT, rx=4) + C(x + 9, y + 20, 3.5, STC[st]) + T(x + 16, y + 23, st, 8, INK, 700)
            yy = y + 30
            for m in [mm for mm in MEM if mm[4] == st]:
                g, dh = ccard(x + 4, yy, cw - 12, m, dict(o, st="hide")); s += g; yy += dh
    else:
        yy = y + 10; cw = 432 if o.get("card", "stack") == "row" else 213
        for i, m in enumerate(MEM if o.get("card") == "row" else MEM[:4]):
            xx = 10 if (o.get("card") == "row" or i % 2 == 0) else 229
            g, dh = ccard(xx, yy, cw, m, o); s += g
            if o.get("card") == "row" or i % 2 == 1: yy += dh
    return s
def lower(y, o):
    s = sec(y, "Needs Attention", "3")
    for i, a in enumerate(["M-1042 visit held for a part", "Van 2 at cap Thursday", "Jordan cancel needs your OK"]):
        s += C(16, y + 16 + i * 12, 2.5, TERRA) + T(22, y + 19 + i * 12, a, 7.5, INK)
    return s
def board(o):
    s = head(o.get("todo", "button")) + schedule(o.get("sch", {}), 38, o.get("sh", 196)) + comms(o.get("cc", {}), 38 + o.get("sh", 196) + 22, o.get("ch", 150))
    s += o.get("extra", "") or lower(418, o)
    return s
def scene(cap, **o): return frame(board(o), cap)
def focus(cap, svg): return frame(svg, cap)
# ---- standalone section drawings ----
def todo_open(style):
    s = head("button" if style != "strip" else "strip")
    if style == "panel":
        s += R(250, 28, 196, 200, WHITE, LINE, 6) + T(260, 46, "Max's To-Do", 12, INK, f="khand") + T(260, 60, "OPEN DECISIONS · 10", 7.5, TERRA, 700)
        for i, q in enumerate(["Daily cap stays at 4?", "Zone order Mon-Fri?", "Snow-day rule", "Who approves cancels"]): s += R(262, 66 + i * 14, 7, 7, WHITE, MUTE, 1) + T(274, 72 + i * 14, q, 7.5, INK)
        s += T(260, 140, "ORIGINAL QUESTIONS · 5", 7.5, LAGOON, 700)
        for i, q in enumerate(["First-visit length", "Photo rule", "Holiday weeks"]): s += R(262, 146 + i * 14, 7, 7, WHITE, MUTE, 1) + T(274, 152 + i * 14, q, 7.5, INK)
    else:
        s += R(10, 34, 432, 24, CREAM, rx=4) + T(16, 49, "To-Do: 10 decisions, 5 questions. Tap a chip to answer.", 8, INK, 600)
    s += schedule({}, 236 if style == "panel" else 70, 180)
    return s
def todo_group(mode):
    s = head("button") + R(120, 30, 326, 250, WHITE, LINE, 6) + T(132, 48, "Max's To-Do", 12, INK, f="khand")
    items = [("D", "Daily cap stays at 4?"), ("D", "Zone order"), ("Q", "First-visit length"), ("D", "Snow-day rule"), ("Q", "Photo rule"), ("D", "Who approves cancels"), ("Q", "Holiday weeks")]
    if mode == "split":
        s += T(132, 64, "DECISIONS · 10", 7.5, TERRA, 700); y = 72
        for k, q in [i for i in items if i[0] == "D"]: s += R(134, y, 7, 7, WHITE, MUTE, 1) + T(146, y + 6.5, q, 8, INK); y += 14
        s += T(132, y + 8, "OPEN QUESTIONS · 5", 7.5, LAGOON, 700); y += 16
        for k, q in [i for i in items if i[0] == "Q"]: s += R(134, y, 7, 7, WHITE, MUTE, 1) + T(146, y + 6.5, q, 8, INK); y += 14
    else:
        s += T(132, 64, "ALL 15 · OLDEST FIRST", 7.5, MUTE, 700); y = 72
        for k, q in items: s += R(134, y, 7, 7, WHITE, MUTE, 1) + T(146, y + 6.5, q, 8, INK) + T(436, y + 6.5, "Decision" if k == "D" else "Question", 7, TERRA if k == "D" else LAGOON, 600, "end"); y += 14
    return s
def attention(style):
    s = head() + schedule({}, 38, 150) + comms({"card": "row"}, 196, 110)
    items = [("M-1042 visit held for a part", TERRA), ("Van 2 at cap Thursday", LAGOON), ("Jordan cancel needs your OK", TERRA)]
    if style == "list":
        s += sec(330, "Needs Attention", "3")
        for i, (a, c) in enumerate(items): s += C(16, y_ := 346 + i * 14, 2.5, c) + T(24, y_ + 3, a, 8, INK)
    else:
        s += sec(330, "Needs Attention", "3")
        for i, (a, c) in enumerate(items): s += R(10 + i * 145, 340, 140, 40, WHITE, c, 5, 1.2) + R(10 + i * 145, 340, 140, 4, c, rx=2) + T(18 + i * 145, 362, a[:26], 7.5, INK, 600)
    return s
def folds(style):
    s = head() + schedule({}, 38, 130) + comms({"card": "row"}, 176, 100) + lower(290, {})
    rows = [("Decided", "12 items · last: cap stays at 4"), ("Ping log", "48 pings · last Oct 19 · TEST"), ("Drill results", "3 drills · all passed · TEST")]
    for i, (a, b) in enumerate(rows):
        y = 340 + i * 26
        if style == "rows": s += R(10, y, 432, 22, WHITE, LINE, 4) + chev(22, y + 11) + T(34, y + 15, a, 8.5, INK, 700) + T(120, y + 15, b, 7.5, MUTE)
        else: s += R(10, y, 432, 22, CREAM, rx=11) + T(20, y + 15, a, 8.5, INK, 700) + (lambda g: g[0])(chip(330, y + 4, "Show", LAGOON, "outline", 7)) + T(100, y + 15, b.split(" · ")[0], 7.5, LAGOON, 700)
    return s
def optcard(kind, style="a"):
    """Optional card drawn in the lower area (y ~ 300-460)."""
    y = 300; s = sec(y, {"weather": "Weather and Snow-Day Watch", "first": "First-Visit Queue", "cap": "Tech Capacity · Next 4 Weeks", "parts": "Parts-Waiting Carryover",
               "map": "Zone-Day Route Map", "trend": "Reschedule and Cancel Trend", "due": "Unscheduled Members Due Soon", "off": "Days Off and Holidays"}[kind], "TEST")
    if kind == "weather":
        for i, d in enumerate(DAYS):
            x = 10 + i * 86; snow = i == 3; s += R(x, y + 12, 82, 60, TERRA + "12" if snow else WHITE, TERRA if snow else LINE, 4) + T(x + 6, y + 26, d, 8.5, INK, 700)
            s += C(x + 60, y + 30, 8, "#E8C77A" if not snow else "#B9D3E0") + T(x + 6, y + 44, "Snow risk" if snow else "Clear", 7.5, TERRA if snow else MUTE, 600) + (T(x + 6, y + 58, "4 visits to move", 7, TERRA) if snow else "")
    elif kind == "first":
        for i, (m, d) in enumerate([("M-1301", "Signed up Oct 16"), ("Casey", "Signed up Oct 17"), ("M-1305", "Signed up Oct 18")]):
            s += R(10, y + 12 + i * 22, 432, 20, WHITE, LINE, 3) + T(16, y + 25 + i * 22, m, 8.5, INK, 700) + T(90, y + 25 + i * 22, d, 7.5, MUTE) + T(436, y + 25 + i * 22, "Needs first slot", 7.5, LAGOON, 600, "end")
    elif kind == "cap":
        for i, t_ in enumerate(TECHS):
            yy = y + 14 + i * 13; s += T(14, yy + 8, t_, 7.5, INK, 600)
            for wk in range(4):
                v = (i * 3 + wk * 5) % 10 / 10 + .1
                if style == "a": s += R(90 + wk * 88, yy, 84, 8, "#EEE8DD", rx=4) + R(90 + wk * 88, yy, 84 * min(v, 1), 8, TERRA if v > .85 else LAGOON, rx=4)
                else: s += R(90 + wk * 88, yy, 84, 11, (TERRA if v > .85 else LAGOON) + ("%02X" % int(40 + v * 180)), rx=2)
        s += "".join(T(132 + wk * 88, y + 96, f"Wk of Oct {19+wk*7}" if wk < 2 else f"Wk of Nov {2+(wk-2)*7}", 7, MUTE, 600, "middle") for wk in range(4))
    elif kind == "parts":
        for i, (m, p, z) in enumerate([("M-1042", "Furnace filter, odd size", "North zone · Thu"), ("Riley", "Faucet cartridge", "East zone · Tue")]):
            s += R(10, y + 12 + i * 24, 432, 22, WHITE, LINE, 3) + R(10, y + 12 + i * 24, 3, 22, TERRA) + T(18, y + 26 + i * 24, m, 8.5, INK, 700) + T(80, y + 26 + i * 24, "Held for: " + p, 7.5, INK) + T(436, y + 26 + i * 24, "Next zone day: " + z, 7.5, LAGOON, 600, "end")
    elif kind == "map":
        for i, (z, c) in enumerate([("North · Mon", LAGOON), ("East · Tue", JUNGLE), ("South · Wed", TERRA)]):
            x = 10 + i * 145; s += R(x, y + 12, 140, 100, SOFT, LINE, 4) + T(x + 6, y + 24, z, 8, INK, 700)
            pts = [(x + 20, y + 90), (x + 50, y + 50), (x + 90, y + 70), (x + 120, y + 40)]
            s += f'<polyline points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 3"/>' + "".join(C(a, b, 4, c) for a, b in pts)
        s += T(10, y + 124, "Abstract map, no real addresses", 7, MUTE, 600)
    elif kind == "trend":
        s += R(10, y + 12, 432, 90, WHITE, LINE, 4)
        for i in range(8):
            r_, c_ = [3, 4, 2, 5, 3, 4, 6, 3][i], [1, 0, 1, 2, 1, 0, 1, 1][i]
            s += R(30 + i * 50, y + 92 - r_ * 10, 16, r_ * 10, LAGOON) + R(48 + i * 50, y + 92 - c_ * 10, 16, c_ * 10, TERRA)
        s += T(436, y + 26, "Reschedules  ·  Cancels  (TEST, by week)", 7, MUTE, 600, "end")
    elif kind == "due":
        for i, (m, d) in enumerate([("Morgan", "Due by Oct 30"), ("M-1188", "Due by Nov 2"), ("Taylor", "Due by Nov 4")]):
            s += R(10, y + 12 + i * 22, 432, 20, WHITE, LINE, 3) + T(16, y + 25 + i * 22, m, 8.5, INK, 700) + T(90, y + 25 + i * 22, d, 7.5, TERRA, 600) + T(436, y + 25 + i * 22, "No visit on the board yet", 7.5, MUTE, 500, "end")
    elif kind == "off":
        for i, d in enumerate(DAYS + ["Mon", "Tue", "Wed", "Thu", "Fri"]):
            x = 10 + i * 43; off = i in (2, 7); hol = i == 4
            s += R(x, y + 12, 41, 40, (TERRA + "22") if hol else (LAGOON + "18" if off else WHITE), LINE, 3) + T(x + 4, y + 24, d, 7.5, INK, 700)
            if off: s += T(x + 4, y + 38, "Van 2 off", 6.5, LAGOON, 600)
            if hol: s += T(x + 4, y + 38, "Holiday", 6.5, TERRA, 600)
    return s
def with_opt(kind, include=True, style="a"):
    s = head() + schedule({}, 38, 130) + comms({"card": "row"}, 176, 110)
    if include: s += optcard(kind, style)
    else: s += lower(300, {}) + R(10, 350, 432, 50, WHITE, LINE, 4, 1, 'stroke-dasharray="4 3"') + T(226, 379, "No extra card here", 9, MUTE, 600, "middle")
    return s
def T_SCHED():
    pairs, P = make("sched19_", "UpKeep")
    A = lambda key, lab, desc, feel, cap, svg: (key, lab, desc, feel, svg)
    S = lambda key, lab, desc, feel, cap, **o: (key, lab, desc, feel, scene(cap, **o))
    F = lambda key, lab, desc, feel, cap, svg: (key, lab, desc, feel, focus(cap, svg))
    P("Schedule", LOC, "View switcher", "should Day, Week and Month switch with a segmented button or underlined tabs?",
      S("seg", "Segmented Button", "Three joined buttons, the open view filled lagoon.", "clear", "Segmented switcher", sch={"sw": "seg"}),
      S("tabs", "Underlined Tabs", "Quiet words with a lagoon underline on the open view.", "calm", "Underlined tabs", sch={"sw": "tabs"}))
    P("Schedule", LOC, "Week layout", "should the week show a calendar grid or one lane per tech?",
      S("grid", "Calendar Grid", "One column per day, visits stacked inside each day.", "familiar", "Calendar grid", sch={"layout": "grid"}),
      S("lanes", "Lane Per Tech", "A row for each tech, days across the top.", "practical", "Lane per tech", sch={"layout": "lanes"}))
    P("Schedule", LOC, "Daily fill bar", "should the fill against the 4-stop cap show as four blocks or one smooth bar?",
      S("blocks", "Four Blocks", "One block per stop; full day turns terracotta.", "countable", "Four blocks", sch={"fs": "blocks"}),
      S("bar", "Smooth Bar", "A single thin bar that fills toward the cap.", "calm", "Smooth bar", sch={"fs": "bar"}))
    P("Schedule", LOC, "Visit chip", "should visit chips be soft filled tiles or white chips with a coloured edge?",
      S("fill", "Soft Filled Chips", "Tinted tile per visit, colour by tech.", "friendly", "Filled chips", sch={"cs": "fill"}),
      S("stripe", "White Chip With Edge", "White chip with a thin coloured stripe on the left.", "crisp", "Edge stripe chips", sch={"cs": "stripe"}))
    P("Schedule", LOC, "Default view", "should the board open on the Day view or the Week view?",
      S("day", "Open On Day", "Today's stops per tech with times, fill per tech.", "focused", "Day view first", sch={"view": "Day"}),
      S("week", "Open On Week", "The whole week at a glance, fill per day.", "overview", "Week view first", sch={"view": "Week"}))
    P("Schedule", LOC, "Month view fill", "should each month day show a small fill bar or a dot per visit?",
      S("bar", "Small Fill Bar", "A short bar per day against the 4-stop cap.", "calm", "Month fill bars", sch={"view": "Month", "ms": "bar"}),
      S("dots", "Dot Per Visit", "One lagoon dot per booked visit.", "countable", "Month dots", sch={"view": "Month", "ms": "dots"}))
    P("Client Communications", LOC, "Member card layout", "should each member be a stacked card or a single tracking row?",
      S("stack", "Stacked Card", "Name, request, next-visit need, timing and photos.", "rich", "Stacked cards", cc={"card": "stack"}, ch=170),
      S("row", "Single Row", "One line per member, easy to scan down.", "compact", "Single rows", cc={"card": "row"}, ch=170))
    P("Client Communications", LOC, "Status display", "should the status be a solid pill or a three-step tracker?",
      S("pill", "Solid Pill", "New, Slot Proposed or Waiting on Approval in a pill.", "clear", "Status pill", cc={"st": "pill"}, ch=170),
      S("steps", "Three-Step Tracker", "Three dots that fill as the request moves along.", "guided", "Step tracker", cc={"st": "steps"}, ch=170))
    P("Client Communications", LOC, "Section layout", "should requests sit in board columns by status or in one list?",
      S("board", "Columns By Status", "New, Slot Proposed, Waiting on Approval side by side.", "visual", "Status columns", cc={"layout": "board"}, ch=170),
      S("list", "One List", "All cards in one list, status on each card.", "simple", "One list", cc={"layout": "list"}, ch=170))
    P("Client Communications", LOC, "Notes and photos", "should tech notes and photos show as a thumbnail strip or one larger photo?",
      S("strip", "Thumbnail Strip", "Three small photos under the need, plus a notes tag.", "detailed", "Thumbnail strip", cc={"photo": "strip"}, ch=170),
      S("big", "One Larger Photo", "One photo at the card's right with a notes count.", "clean", "One larger photo", cc={"photo": "big"}, ch=170))
    P("Client Communications", LOC, "Request type", "should book, reschedule or cancel show as a small tag or a coloured card edge?",
      S("tag", "Small Tag", "A soft coloured tag beside the member's name.", "clear", "Request tag", cc={"rqs": "tag"}, ch=170),
      S("edge", "Coloured Edge", "A coloured stripe down the card's left side.", "subtle", "Request edge", cc={"rqs": "edge"}, ch=170))
    P("Header", LOC, "To-Do placement", "should Max's To-Do open as a header panel or sit as a chip strip under the title?",
      F("panel", "Header Button And Panel", "A To-Do button with count opens a short panel.", "tidy", "To-Do panel", todo_open("panel")),
      F("strip", "Chip Strip In Header", "Open items always visible as chips in the header.", "visible", "To-Do chips", todo_open("strip")))
    P("Header", LOC, "To-Do grouping", "should the ten decisions and five questions be split or in one list?",
      F("split", "Split Into Two Groups", "Open decisions first, original questions below.", "organized", "Split groups", todo_group("split")),
      F("one", "One List, Oldest First", "A single list with a small type label per item.", "simple", "One list", todo_group("one")))
    P("Below the sections", LOC, "Needs Attention", "should the short Needs Attention list be plain lines or small tiles?",
      F("list", "Plain Lines", "Three short lines with a coloured dot.", "quiet", "Plain lines", attention("list")),
      F("tiles", "Small Tiles", "Three tiles side by side with a coloured top.", "visible", "Small tiles", attention("tiles")))
    P("Below the sections", LOC, "Folded dropdowns", "should Decided, the ping log and drills fold into plain rows or rounded pills?",
      F("rows", "Plain Rows With Arrow", "Arrow, name and a one-line summary.", "tidy", "Plain fold rows", folds("rows")),
      F("pills", "Rounded Pills With Show", "Cream pill, summary count and a Show button.", "soft", "Rounded fold pills", folds("pills")))
    for kind, name, el, why in [("weather", "Weather Watch", "Weather and Snow-Day Watch", "five-day weather with snow-day flags"),
                                ("first", "First-Visit Queue", "First-Visit Queue", "new sign-ups still waiting for a first slot"),
                                ("parts", "Parts-Waiting Carryover", "Parts-Waiting Carryover", "visits held for a part with the next zone day"),
                                ("map", "Zone-Day Map", "Zone-Day Route Map", "abstract route previews for each zone day"),
                                ("trend", "Cancel Trend", "Reschedule and Cancel Trend", "weekly reschedules and cancels as bars"),
                                ("due", "Due Soon List", "Unscheduled Members Due Soon", "members due soon with no visit booked yet"),
                                ("off", "Days Off Strip", "Days off and holiday strip", "a two-week strip of tech days off and holidays")]:
        P("Optional cards", LOC, el[0].lower() + el[1:] if kind == "off" else el, f"should the board include a card for {why}?",
          F("in", "Include " + name, ("Add it: " + why)[:72], "useful", "Include", with_opt(kind, True)),
          F("skip", "Skip It", "Leave it off to keep the board short.", "lean", "Skip", with_opt(kind, False)))
        if kind == "first":
            P("Optional cards", LOC, "Tech Capacity", "should capacity for the next four weeks show as bars or a shaded grid?",
              F("bars", "Bars Per Week", "One bar per tech per week, terracotta near cap.", "clear", "Capacity bars", with_opt("cap", True, "a")),
              F("heat", "Shaded Grid", "One shaded box per tech per week, darker is fuller.", "compact", "Capacity grid", with_opt("cap", True, "b")))
    return pairs
