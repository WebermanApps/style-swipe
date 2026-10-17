#!/usr/bin/env python3
"""Company Dashboard Deck (Branding, for Max Oct 17 2026 21:11 ICT: "can you push a deck for the upkeep company dashboard").
The Smart Upkeep company dashboard (separate from the member app, the technician app and the Operator Console) is NOT built yet:
no company-dashboard page in upkeep-cc-d36d3521, WebermanApps repos, /workspace or results-2026-10-17. Content is based on UpKeep's
notes and docs (members, visits, revenue and MRR, techs, churn, open jobs, investor numbers; forecast v3, investor pitch, Operator
Console deck). Settled picks are not re-asked: one line per plan + legend above, break-even/lowest-cash flags in green/terracotta,
monthly churn tile, swipe tiles on phone (forecast decks). Each option has a desktop drawing (240x300, class mph-d) and a phone
drawing (240x520, class mph-m, shown under 600px). Light only, Khand/Hind, no emoji. All numbers EXAMPLE DATA.
Page written UNLOCKED: lock before commit.  usage: build_company_dashboard_deck.py [--preview DIR]"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets
from draft_svg import t, rect, dot, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON, crisp
from team_kit import deck as kdeck, publish, shareic
from uk5_art import mark, wordmark, GREY
from caption_rule import guard as cap_guard
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
DID = "upkeep-company-dashboard-deck"; NAME = "Company Dashboard Deck"; SLUG_KEY = "company-dashboard"
CREAM = "#FAF6EE"; LOC = "UpKeep Company Dashboard"; MH = 520
def g(x, y, sc, inner): return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'
def hl(x1, x2, y, c=LINE, w=1): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="{w}"/>'
def poly(pts, c, w=2, dash=""):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {dash}/>'
def pill(x, y, txt, c, solid=False, s=8, h=13):
    w = len(txt) * s * .55 + 10
    return rect(x, y, w, h, c if solid else c + "1F", "none", h / 2) + t(x + w / 2, y + h * .72, txt, s, "#FFFFFF" if solid else c, "hind", 600, "middle"), w
def P(x, y, txt, c, solid=False, s=8, h=13): return pill(x, y, txt, c, solid, s, h)[0]
def spark(x, y, w, h, v, c):
    lo, hi = min(v), max(v); return poly([(x + i * w / (len(v) - 1), y + h - (a - lo) / ((hi - lo) or 1) * h) for i, a in enumerate(v)], c, 1.4)
KPIS = [("120", "Members", INK, "+6"), ("$18.4k", "MRR", TERRA, "+4.1%"), ("1.8%", "Churn / mo", LAGOON, "-0.3"),
        ("46", "Visits this wk", JUNGLE, "+5"), ("7", "Open jobs", TERRA, "2 late"), ("3", "Techs on", LAGOON, "78% busy")]
MEM = [("Sarah Sample", "Plus", "Active", JUNGLE, "Oct 21"), ("Dan Example", "Core", "Late pay", TERRA, "Oct 19"),
       ("Lee Placeholder", "Plus", "Active", JUNGLE, "Oct 22"), ("Ana Demo", "Premium", "Paused", SAFFRON, "-"),
       ("Raj Sample", "Core", "Active", JUNGLE, "Oct 24"), ("Mia Example", "Plus", "New", LAGOON, "Oct 20"),
       ("Tom Demo", "Core", "Active", JUNGLE, "Oct 25"), ("Kim Sample", "Premium", "Active", JUNGLE, "Oct 23")]
TECHS = [("Tech A", TERRA), ("Tech B", LAGOON), ("Tech C", JUNGLE)]
MRR = {"Core": ([5.1, 5.4, 5.6, 5.9, 6.1, 6.3, 6.6, 6.8], LAGOON), "Plus": ([6.0, 6.5, 6.9, 7.2, 7.6, 7.9, 8.2, 8.6], TERRA), "Premium": ([2.0, 2.1, 2.3, 2.4, 2.6, 2.7, 2.8, 3.0], JUNGLE)}
# ---------------- desktop canvas: 400 x 290 virtual, scaled into the card ----------------
DW, DH = 400, 400; DS = 212 / DW
def chrome(inner, title="Company Dashboard", right="Last 30 days", density=1.0):
    s = rect(0, 0, DW, DH, "#FFFFFF") + rect(0, 0, DW, 26, CREAM) + mark(13, 13, 7, "#FFFFFF", TERRA) + wordmark(24, 18, 12)
    s += t(110, 18, title, 13, INK, "khand") + rect(DW - 92, 6, 84, 15, "#FFFFFF", "#CFC7BA", 3, .8) + t(DW - 50, 16.5, right, 8, INK, "hind", 600, "middle") + hl(0, DW, 26, "#E3DDD2")
    return s + inner
def band(y=294):
    w = (DW - 28) / 3; s = ""
    pans = [("Techs Today", [(n, f"{4 - i} jobs left", c) for i, (n, c) in enumerate(TECHS)]),
            ("Recent Visits", [("Sarah Sample", "Seasonal visit, done", JUNGLE), ("Lee Placeholder", "HVAC filter, done", JUNGLE), ("Dan Example", "Leak check, late", TERRA)]),
            ("Investor Numbers", [("$221k", "Run rate / yr", JUNGLE), ("$148", "Avg per member / mo", TERRA), ("14 mo", "Avg member age", LAGOON)])]
    for i, (h, rows) in enumerate(pans):
        x = 8 + i * (w + 6); s += rect(x, y, w, 98, "#FFFFFF", LINE, 4) + t(x + 7, y + 15, h, 10, INK, "khand")
        for k, (a, b, c) in enumerate(rows): s += dot(x + 10, y + 32 + k * 22, 3, c) + t(x + 18, y + 35 + k * 22, a, 8.5, INK, "hind", 600) + t(x + w - 6, y + 35 + k * 22, b, 7.5, MUTE, "hind", 400, "end")
    return s
def desk(inner):
    inner += band()
    return (rect(14, 32, 212, 9, "#EFEAE2") + dot(19, 36.5, 1.6, TERRA) + dot(24, 36.5, 1.6, SAFFRON) + dot(29, 36.5, 1.6, JUNGLE)
            + f'<clipPath id="dk"><rect x="14" y="41" width="212" height="{DH*DS:.1f}"/></clipPath><g clip-path="url(#dk)">' + g(14, 41, round(DS, 4), inner) + "</g>"
            + rect(14, 32, 212, 9 + DH * DS, "none", "#BDB6AA", 0, .8))
def note(y, lines): y = 262 if y == 202 else y; return "".join(t(14, y + i * 11, l, 7.5, MUTE) for i, l in enumerate(lines))
def kpi(x, y, w, h, v, lb, c, delta=None, sp=None, big=17):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 4, 1) + t(x + 7, y + 8 + big * .8, v, big, c, "khand") + t(x + 7, y + h - 6, lb, 8, MUTE)
    if delta: s += t(x + w - 6, y + 13, delta, 7.5, JUNGLE if not delta.startswith(("2 late",)) else TERRA, "hind", 600, "end")
    if sp: s += spark(x + w * .5, y + 18, w * .42, h * .32, sp, c if c != INK else JUNGLE)
    return s
def kpirow(y, mode="six", x0=8, W=DW - 16, h=46):
    if mode == "six":
        w = (W - 5 * 6) / 6; return "".join(kpi(x0 + i * (w + 6), y, w, h, v, lb, c, d, big=15) for i, (v, lb, c, d) in enumerate(KPIS))
    four = [KPIS[0], KPIS[1], KPIS[2], KPIS[4]]; sps = [[100, 104, 108, 112, 114, 117, 120], [15, 15.8, 16.4, 17, 17.6, 18, 18.4], [2.4, 2.2, 2.3, 2.1, 2, 1.9, 1.8], [5, 9, 6, 8, 10, 6, 7]]
    w = (W - 3 * 6) / 4; return "".join(kpi(x0 + i * (w + 6), y, w, h + 6, v, lb, c, None, sps[i], big=19) for i, (v, lb, c, d) in enumerate(four))
def mrrchart(x, y, w, h, bars=False, goal=False, legend=True, flags=True):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 4) + t(x + 8, y + 15, "MRR By Plan", 11, INK, "khand") + t(x + w - 8, y + 15, "$18.4k", 11, TERRA, "khand", 700, "end")
    lx = x + 8
    if legend:
        for k, (v, c) in MRR.items(): s += rect(lx, y + 21, 8, 3, c) + t(lx + 11, y + 25, k, 7.5, MUTE); lx += 50
    cx, cy, cw, ch = x + 22, y + 32, w - 32, h - (62 if bars else 44)
    for i in range(4): s += hl(cx, cx + cw, cy + i * ch / 3, "#EFEAE2")
    s += "".join(t(cx - 4, cy + i * ch / 3 + 3, f"{9 - i * 3}k", 6.5, GREY, "hind", 400, "end") for i in range(4))
    for k, (v, c) in MRR.items(): s += poly([(cx + i * cw / 7, cy + ch - v[i] / 9 * ch) for i in range(8)], c, 2)
    if goal: s += f'<line x1="{cx}" y1="{cy+ch-8/9*ch:.1f}" x2="{cx+cw}" y2="{cy+ch-8/9*ch:.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 3"/>' + t(cx + cw, cy + ch - 8 / 9 * ch - 3, "Plus goal $8k", 7, INK, "hind", 600, "end")
    if flags: s += dot(cx + 5 * cw / 7, cy + ch - 7.9 / 9 * ch, 3, JUNGLE) + t(cx + 5 * cw / 7 + 5, cy + ch - 7.9 / 9 * ch - 5, "Break-even", 7, JUNGLE, "hind", 600)
    if bars:
        by = cy + ch + 6; nn = [0.6, 0.9, 0.7, 1.0, 0.8, 0.9, 1.1, 1.2]; ch2 = [0.2, 0.3, 0.2, 0.4, 0.3, 0.2, 0.3, 0.3]
        s += t(cx - 4, by + 9, "Net new", 6.5, GREY, "hind", 400, "end")
        for i in range(8):
            bx = cx + i * cw / 7 - 5; s += rect(bx, by + 14 - nn[i] * 10, 5, nn[i] * 10, JUNGLE) + rect(bx + 5, by + 14, 5, ch2[i] * 10, TERRA)
        s += hl(cx - 6, cx + cw + 6, by + 14, "#CFC7BA")
    s += "".join(t(cx + i * cw / 7, y + h - 5, m, 6.5, GREY, "hind", 400, "middle") for i, m in enumerate(["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]))
    return s
def mtable(x, y, w, n=6, rowh=16, cols=None):
    cols = cols or [(6, "Member"), (w * .38, "Plan"), (w * .56, "Status"), (w * .8, "Next visit")]
    s = rect(x, y, w, 15 + n * rowh, "#FFFFFF", LINE, 4) + rect(x, y, w, 15, CREAM, "none", 4) + "".join(t(x + cx, y + 10.5, h, 7.5, INK, "hind", 600) for cx, h in cols)
    for r, (nm, pl, st, c, nx) in enumerate(MEM[:n]):
        yy = y + 15 + r * rowh; s += hl(x, x + w, yy + rowh, "#F0EBE3") + t(x + cols[0][0], yy + rowh * .68, nm, 8, INK, "hind", 600)
        if len(cols) == 3: s += P(x + cols[1][0], yy + rowh / 2 - 5.5, st, c, s=7, h=11) + t(x + cols[2][0], yy + rowh * .68, nx, 8, MUTE)
        else: s += t(x + cols[1][0], yy + rowh * .68, pl, 8, MUTE) + P(x + cols[2][0], yy + rowh / 2 - 5.5, st, c, s=7, h=11) + t(x + cols[3][0], yy + rowh * .68, nx, 8, MUTE)
    return s
# ---------------- phone canvas: 200 x 440 screen inside a 240x520 card ----------------
def phone(inner, title="Company"):
    s = rect(26, 34, 188, 470, INK, "none", 18) + rect(31, 40, 178, 458, "#FFFFFF", "none", 14)
    s += f'<clipPath id="ph"><rect x="31" y="40" width="178" height="458" rx="14"/></clipPath><g clip-path="url(#ph)">'
    s += t(42, 54, "9:41", 7.5, INK, "hind", 600) + rect(184, 48, 12, 6, "none", INK, 1, .8) + mark(44, 70, 6.5, "#FFFFFF", TERRA) + wordmark(54, 74.5, 11) + shareic(186, 63, INK, 12)
    s += t(40, 96, title, 15, INK, "khand") + inner + "</g>" + rect(100, 43, 40, 5, "#333", "none", 2.5)
    return s
def dots(cx, y, n, on, c=TERRA): return "".join(dot(cx + (i - (n - 1) / 2) * 9, y, 2.6 if i == on else 2, c if i == on else "#CFC7BA") for i in range(n))
def pk(x, y, w, h, v, lb, c, d=None):
    return rect(x, y, w, h, "#FFFFFF", LINE, 6) + t(x + 8, y + 26, v, 20, c, "khand") + t(x + 8, y + h - 9, lb, 8.5, MUTE) + (t(x + w - 7, y + 14, d, 8, JUNGLE, "hind", 600, "end") if d else "")
def pchart(y, h=110, bars=False, goal=False): return g(38, y, 164 / 260, mrrchart(0, 0, 260, h / (164 / 260) * .95, bars, goal))
def plist(y, n=5, compact=False):
    rh = 26 if compact else 32; s = ""
    for i, (nm, pl, st, c, nx) in enumerate(MEM[:n]):
        yy = y + i * (rh + 3); s += rect(38, yy, 164, rh, "#FFFFFF", LINE, 5) + t(46, yy + rh * .45 + 2, nm, 9, INK, "hind", 600) + t(46, yy + rh - 5, f"{pl}  |  Next {nx}", 7.5, MUTE) + P(150, yy + rh / 2 - 6, st, c, s=7, h=12)
    return s
# ---------------- card frames ----------------
def frame(label, acc, body, H, cls):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 {H}" width="240" height="{H}" class="{cls}">'
         + rect(0, 0, 240, H, "#FFFFFF") + rect(0, 0, 240, 5, acc) + t(14, 22, label.upper(), 7.5, acc, "hind", 600, extra='letter-spacing="1.2"'))
    s += rect(152, 13, 74, 12, SAFFRON + "26", SAFFRON, 0, .8) + t(189, 21.6, "EXAMPLE DATA", 7.5, "#7A5A0C", "hind", 600, "middle", 'letter-spacing=".5"')
    return crisp(s + body + t(120, H - 3, "Built by Machan", 7.5, GREY, "hind", 400, "middle") + rect(.5, .5, 239, H - 1, "none", "#D6D0C6") + "</svg>")
def C(label, acc, d_inner, d_note, p_inner, p_title="Company"):
    return frame(label, acc, desk(chrome(d_inner)) + note(202, d_note), 300, "mph-d") + frame(label, acc, phone(p_inner, p_title), MH, "mph-m")
PK = []
def pick(group, el, sentence, a, b): PK.append((group, f"{LOC}: {el}, {sentence}", a, b))
# 1 KPI row
pick("KPI Row", "Top KPI row", "six small number tiles with this month's change, or four bigger tiles with an eight-week trend line?",
     ("kpi_six", "Six Tiles + Change", "Members, MRR, churn, visits, jobs, techs", "practical",
      C("KPI Row", TERRA, kpirow(34, "six") + mrrchart(8, 88, 250, 140) + mtable(266, 88, 126, 5, 17, [(6, "Member"), (58, "Status"), (96, "Next")]),
        ["Every business number in one glance;", "green or red change beside each."],
        "".join(pk(38 + (i % 2) * 84, 106 + (i // 2) * 60, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS)) + pchart(292, 120))),
     ("kpi_four", "Four Tiles + Trend", "Members, MRR, churn, open jobs", "calm",
      C("KPI Row", LAGOON, kpirow(34, "four") + mrrchart(8, 94, 250, 134) + mtable(266, 94, 126, 5, 17, [(6, "Member"), (58, "Status"), (96, "Next")]),
        ["Fewer, bigger numbers; the small line", "shows the last eight weeks."],
        "".join(rect(38 + (i % 2) * 84, 106 + (i // 2) * 72, 80, 66, "#FFFFFF", LINE, 6) + t(46 + (i % 2) * 84, 132 + (i // 2) * 72, v, 21, c, "khand") + spark(46 + (i % 2) * 84, 140 + (i // 2) * 72, 62, 12, sp, c if c != INK else JUNGLE) + t(46 + (i % 2) * 84, 166 + (i // 2) * 72, lb, 8.5, MUTE)
                for i, ((v, lb, c, d), sp) in enumerate(zip([KPIS[0], KPIS[1], KPIS[2], KPIS[4]], [[100, 104, 108, 112, 117, 120], [15, 16, 16.4, 17, 18, 18.4], [2.4, 2.2, 2.1, 2, 1.9, 1.8], [5, 9, 6, 8, 6, 7]]))) + pchart(256, 120))))
# 2 MRR chart
pick("MRR Chart", "Revenue and MRR chart", "the plan lines with net-new and lost MRR bars under them, or the plan lines with a dashed goal line?",
     ("mrr_bars", "Lines + Net New Bars", "Green = new MRR, terracotta = lost", "practical",
      C("MRR Chart", JUNGLE, kpirow(34, "six") + mrrchart(8, 88, 384, 196, bars=True), ["Plan lines stay (legend above, as picked);", "bars show what came in and what left."],
        pk(38, 106, 80, 54, "$18.4k", "MRR", TERRA, "+4.1%") + pk(122, 106, 80, 54, "$1.2k", "New this mo", JUNGLE) + pchart(172, 190, bars=True))),
     ("mrr_goal", "Lines + Goal Line", "Dashed target to beat", "calm",
      C("MRR Chart", TERRA, kpirow(34, "six") + mrrchart(8, 88, 384, 196, goal=True), ["Same plan lines with one dashed goal;", "easy to see if we are on track."],
        pk(38, 106, 80, 54, "$18.4k", "MRR", TERRA, "+4.1%") + pk(122, 106, 80, 54, "92%", "Of goal", JUNGLE) + pchart(172, 190, goal=True))))
# 3 members list
def grouped(x, y, w):
    s = ""; yy = y
    for pl, c in [("Premium", JUNGLE), ("Plus", TERRA), ("Core", LAGOON)]:
        rows = [m for m in MEM if m[1] == pl][:2]
        s += rect(x, yy, w, 16, c + "14", "none", 3) + t(x + 6, yy + 11.5, f"{pl}  ({len(rows) * 13} members)", 8.5, c, "hind", 600); yy += 18
        for nm, p_, st, sc, nx in rows:
            s += t(x + 8, yy + 11, nm, 8, INK, "hind", 600) + P(x + w * .45, yy + 2, st, sc, s=7, h=11) + t(x + w * .7, yy + 11, nx, 8, MUTE) + rect(x + w - 44, yy + 1, 38, 12, "#FFFFFF", "#CFC7BA", 3, .7) + t(x + w - 25, yy + 9.8, "Open", 7, INK, "hind", 600, "middle") + hl(x, x + w, yy + 15, "#F0EBE3"); yy += 16
        yy += 4
    return s
pick("Members List", "Members list", "one tight sortable table of every member, or members grouped by plan with an Open button on each row?",
     ("mem_table", "Sortable Table", "Name, plan, status, next visit", "practical",
      C("Members List", LAGOON, kpirow(34, "six") + rect(8, 88, 160, 16, "#FFFFFF", "#CFC7BA", 3, .8) + t(14, 99, "Search members", 8, GREY) + P(176, 89, "All 120", INK, True, 7.5, 14) + P(222, 89, "Late pay 2", TERRA, False, 7.5, 14) + mtable(8, 110, 384, 8, 20),
        ["Click a column to sort; filter chips", "on top; 20+ rows fit on a screen."],
        rect(38, 106, 164, 22, "#FFFFFF", "#CFC7BA", 5, .8) + t(46, 121, "Search members", 8.5, GREY) + P(38, 134, "All 120", INK, True, 7.5, 14) + P(84, 134, "Late pay 2", TERRA, False, 7.5, 14) + plist(156, 8, True), "Members")),
     ("mem_group", "Grouped By Plan", "Premium, Plus, Core sections", "calm",
      C("Members List", JUNGLE, kpirow(34, "six") + grouped(8, 88, 384), ["Each plan is its own section with a", "count; Open goes to the member."],
        "".join(rect(38, 106 + i * 118, 164, 112, "#FFFFFF", LINE, 6) + rect(38, 106 + i * 118, 164, 20, c + "14", "none", 6) + t(46, 120 + i * 118, f"{pl}  (26)", 10, c, "khand") + "".join(t(46, 142 + i * 118 + k * 22, m[0], 9, INK, "hind", 600) + P(150, 132 + i * 118 + k * 22, m[2], m[3], s=7, h=12) for k, m in enumerate([m for m in MEM if m[1] == pl][:3])) for i, (pl, c) in enumerate([("Premium", JUNGLE), ("Plus", TERRA), ("Core", LAGOON)])), "Members")))
# 4 tech schedule
def lanes(x, y, w, h):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 4) + t(x + 6, y + 13, "Today, Sat Oct 17", 10, INK, "khand"); lx = x + 44; lw = w - 50
    s += "".join(t(lx + i * lw / 5, y + 26, f"{8 + i * 2}:00", 7, GREY, "hind", 400, "middle") for i in range(6))
    jobs = [[(0, 1.2, "Gutters"), (1.6, 1, "HVAC filter"), (3, 1.4, "Smoke test")], [(0.4, 1.4, "Water heater"), (2.2, 1, "Dryer vent"), (3.6, 1, "Late", True)], [(0.2, 0.9, "Caulk"), (1.4, 1.6, "Seasonal visit"), (3.4, 0.8, "Leak")]]
    for r, ((nm, c), js) in enumerate(zip(TECHS, jobs)):
        ly = y + 34 + r * ((h - 40) / 3); lh = (h - 40) / 3 - 6
        s += dot(x + 10, ly + lh / 2, 4, c) + t(x + 17, ly + lh / 2 + 3, nm, 8, INK, "hind", 600)
        for j in js:
            st, du, lb = j[:3]; late = len(j) > 3; bx = lx + st * lw / 5
            s += rect(bx, ly, du * lw / 5 - 3, lh, (TERRA if late else c) + "22", TERRA if late else c, 3, 1) + t(bx + 4, ly + lh / 2 + 3, lb, 7.5, INK, "hind", 600)
    return s + f'<line x1="{lx + 2.3 * lw / 5:.1f}" y1="{y+28}" x2="{lx + 2.3 * lw / 5:.1f}" y2="{y+h-4}" stroke="{TERRA}" stroke-width="1.2"/>'
def week(x, y, w, h):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 4) + t(x + 6, y + 13, "This Week", 10, INK, "khand"); cw = (w - 50) / 6
    s += "".join(t(x + 50 + i * cw + cw / 2, y + 26, d, 7.5, MUTE, "hind", 600, "middle") for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]))
    load = [[5, 6, 4, 6, 5, 3], [6, 6, 5, 4, 6, 2], [3, 4, 5, 5, 4, 4]]
    for r, (nm, c) in enumerate(TECHS):
        ry = y + 32 + r * ((h - 38) / 3); rh = (h - 38) / 3 - 5
        s += dot(x + 10, ry + rh / 2, 4, c) + t(x + 17, ry + rh / 2 + 3, nm, 8, INK, "hind", 600)
        for i, n in enumerate(load[r]):
            full = n >= 6; s += rect(x + 50 + i * cw + 2, ry, cw - 4, rh, (TERRA if full else c) + ("30" if full else "16"), "none", 3) + t(x + 50 + i * cw + cw / 2, ry + rh / 2 + 3, f"{n} jobs", 7.5, TERRA if full else INK, "hind", 600, "middle")
    return s
pick("Tech Schedule", "Tech schedule view", "a day timeline with one lane per tech, or a week grid showing how many jobs each tech has per day?",
     ("sch_day", "Day Lanes Per Tech", "Each job a block; red line = now", "practical",
      C("Tech Schedule", TERRA, kpirow(34, "six") + lanes(8, 88, 384, 150) + mtable(8, 244, 384, 2, 15), ["Who is where right now; late jobs", "turn terracotta."],
        "".join(rect(38, 106 + i * 86, 164, 80, "#FFFFFF", LINE, 6) + dot(48, 120 + i * 86, 4, c) + t(56, 123 + i * 86, nm, 10, INK, "khand") + "".join(rect(46, 132 + i * 86 + k * 14, 148, 11, c + "22", c, 3, .8) + t(50, 140.5 + i * 86 + k * 14, f"{9 + k * 2}:00  Job {k + 1}", 7.5, INK, "hind", 600) for k in range(3)) for i, (nm, c) in enumerate(TECHS)), "Today")),
     ("sch_week", "Week Grid With Load", "Jobs per tech per day", "calm",
      C("Tech Schedule", LAGOON, kpirow(34, "six") + week(8, 88, 384, 150) + mtable(8, 244, 384, 2, 15), ["Spot full days (terracotta) and", "open room to book more visits."],
        "".join(rect(38, 106 + i * 50, 164, 44, "#FFFFFF", LINE, 6) + t(46, 121 + i * 50, d, 10, INK, "khand") + "".join(rect(46 + k * 52, 127 + i * 50, 48, 13, c + "22", "none", 3) + t(70 + k * 52, 136.5 + i * 50, f"{n} jobs", 7.5, INK, "hind", 600, "middle") for k, ((nm, c), n) in enumerate(zip(TECHS, [5 - i % 2, 6 - i % 3, 4 + i % 2]))) for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])), "This Week")))
# 5 job status board
COLS = [("Booked", LAGOON, 9), ("On The Way", SAFFRON, 2), ("In Progress", TERRA, 3), ("Done Today", JUNGLE, 6)]
def kanban(x, y, w, h):
    cw = (w - 18) / 4; s = ""
    for i, (nm, c, n) in enumerate(COLS):
        cx = x + i * (cw + 6); s += rect(cx, y, cw, h, CREAM, "none", 4) + rect(cx, y, cw, 3, c) + t(cx + 6, y + 16, f"{nm}  {n}", 9, INK, "khand")
        for k in range(min(n, 4)):
            s += rect(cx + 4, y + 22 + k * 30, cw - 8, 26, "#FFFFFF", LINE, 3) + t(cx + 9, y + 33 + k * 30, ["Gutter clean", "HVAC filter", "Leak check", "Smoke test"][k], 7.5, INK, "hind", 600) + t(cx + 9, y + 43 + k * 30, f"{MEM[k + i][0].split()[0]}  |  {TECHS[k % 3][0]}", 6.5, MUTE)
    return s
def joblist(x, y, w, n=8):
    s = "".join(P(x + o, y, f"{nm} {k}", c, i == 0, 7.5, 14) for i, (o, (nm, c, k)) in enumerate(zip([0, 54, 120, 190], COLS)))
    s += rect(x, y + 20, w, 15 + n * 17, "#FFFFFF", LINE, 4) + rect(x, y + 20, w, 15, CREAM, "none", 4) + "".join(t(x + cx, y + 30.5, h, 7.5, INK, "hind", 600) for cx, h in [(6, "Job"), (w * .3, "Member"), (w * .52, "Tech"), (w * .7, "Status"), (w * .88, "Time")])
    for r in range(n):
        nm, c, _ = COLS[r % 4]; yy = y + 35 + r * 17
        s += hl(x, x + w, yy + 17, "#F0EBE3") + t(x + 6, yy + 11.5, ["Gutter clean", "HVAC filter", "Leak check", "Smoke test"][r % 4], 8, INK, "hind", 600) + t(x + w * .3, yy + 11.5, MEM[r % 8][0], 8, MUTE) + t(x + w * .52, yy + 11.5, TECHS[r % 3][0], 8, MUTE) + P(x + w * .7, yy + 3, nm, c, s=7, h=11) + t(x + w * .88, yy + 11.5, f"{9 + r % 6}:00", 8, MUTE)
    return s
pick("Job Status", "Job status board", "four columns from Booked to Done with a card per job, or one list with status pills and filter tabs?",
     ("job_cols", "Status Columns", "Booked, On The Way, In Progress, Done", "bold",
      C("Job Status", TERRA, kpirow(34, "six") + kanban(8, 88, 384, 156), ["Every open job as a card; see where", "work is piling up at a glance."],
        "".join(rect(38, 106 + i * 94, 164, 88, CREAM, "none", 6) + rect(38, 106 + i * 94, 164, 3, c) + t(46, 124 + i * 94, f"{nm}  {n}", 11, INK, "khand") + "".join(rect(44, 131 + i * 94 + k * 26, 152, 22, "#FFFFFF", LINE, 4) + t(50, 145 + i * 94 + k * 26, ["Gutter clean", "HVAC filter"][k] + f"  |  {TECHS[k][0]}", 8, INK, "hind", 600) for k in range(2)) for i, (nm, c, n) in enumerate(COLS)), "Jobs")),
     ("job_list", "List + Status Pills", "Filter tabs on top, one row per job", "practical",
      C("Job Status", LAGOON, kpirow(34, "six") + joblist(8, 88, 384, 9), ["Dense and sortable; tabs filter by", "status, pills show it per row."],
        "".join(P(38 + o, 106, f"{nm} {k}", c, i == 0, 7.5, 14) for i, (o, (nm, c, k)) in enumerate(zip([0, 52, 118], COLS[:3]))) + "".join(rect(38, 128 + r * 34, 164, 30, "#FFFFFF", LINE, 5) + t(46, 141 + r * 34, ["Gutter clean", "HVAC filter", "Leak check", "Smoke test"][r % 4], 9, INK, "hind", 600) + t(46, 152 + r * 34, f"{MEM[r % 8][0]}  |  {TECHS[r % 3][0]}", 7.5, MUTE) + P(146, 137 + r * 34, COLS[r % 4][0].split()[0], COLS[r % 4][1], s=7, h=12) for r in range(10)), "Jobs")))
# 6 alerts
ALS = [(TERRA, "1 payment failed", "Dan Example, Core plan"), (SAFFRON, "2 visits running late", "Tech B, 20 min"), (LAGOON, "3 renewals this week", "Review before Friday")]
def strip(x, y, w):
    s = ""; xx = x; cw = (w - 12) / 3
    for c, a, b in ALS: s += rect(xx, y, cw, 26, c + "14", c, 4, .8) + rect(xx, y, 3, 26, c) + t(xx + 9, y + 11, a, 8.5, INK, "khand") + t(xx + 9, y + 21, b, 7, MUTE); xx += cw + 6
    return s
def bellhead():
    return dot(DW - 108, 13, 7, "#FFFFFF") + f'<path d="M{DW-112} 16 Q{DW-112} 8 {DW-108} 8 Q{DW-104} 8 {DW-104} 16 Z" fill="none" stroke="{INK}" stroke-width="1.2"/>' + dot(DW - 103, 8, 4.5, TERRA) + t(DW - 103, 10.5, "6", 6.5, "#FFFFFF", "hind", 600, "middle")
def drawer(x, y, w, h):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 4) + t(x + 8, y + 15, "Needs Attention  6", 10, INK, "khand")
    for i, (c, a, b) in enumerate(ALS + [(TERRA, "Van 2 low on filters", "Restock"), (LAGOON, "Tech C hours", "Approve"), (JUNGLE, "5-star review", "Reply")]):
        s += dot(x + 11, y + 30 + i * 22, 3, c) + t(x + 19, y + 32 + i * 22, a, 8, INK, "hind", 600) + t(x + 19, y + 41 + i * 22, b, 7, MUTE)
    return s
pick("Alerts", "Alerts", "a thin strip of color alerts right under the KPI row, or a bell count in the header that opens a side list?",
     ("al_strip", "Alert Strip Under KPIs", "Three color alerts, always visible", "bold",
      C("Alerts", TERRA, kpirow(34, "six") + strip(8, 86, 384) + mrrchart(8, 118, 250, 166) + mtable(266, 118, 126, 6, 17, [(6, "Member"), (58, "Status"), (96, "Next")]),
        ["Problems sit in plain sight between", "the numbers and the chart."],
        "".join(pk(38 + (i % 2) * 84, 106, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:2])) + "".join(rect(38, 168 + i * 36, 164, 32, c + "14", c, 5, .8) + rect(38, 168 + i * 36, 3, 32, c) + t(48, 182 + i * 36, a, 10, INK, "khand") + t(48, 194 + i * 36, b, 7.5, MUTE) for i, (c, a, b) in enumerate(ALS)) + pchart(282, 120))),
     ("al_bell", "Bell + Side List", "Count in the header, list on the right", "calm",
      C("Alerts", LAGOON, bellhead() + kpirow(34, "six") + mrrchart(8, 88, 250, 196) + drawer(266, 88, 126, 196),
        ["Quieter page; the bell count and side", "list hold every item to handle."],
        f'<path d="M176 92 Q176 84 181 84 Q186 84 186 92 Z" fill="none" stroke="{INK}" stroke-width="1.3"/>' + dot(188, 84, 5, TERRA) + t(188, 86.5, "6", 7, "#FFFFFF", "hind", 600, "middle") + "".join(pk(38 + (i % 2) * 84, 106, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:2])) + rect(38, 168, 164, 156, "#FFFFFF", LINE, 6) + t(46, 184, "Needs Attention  6", 11, INK, "khand") + "".join(dot(48, 200 + i * 20, 3, c) + t(56, 203 + i * 20, a, 8.5, INK, "hind", 600) for i, (c, a, b) in enumerate(ALS + [(TERRA, "Van 2 low on filters", ""), (LAGOON, "Tech C hours", ""), (JUNGLE, "5-star review", "")])) + pchart(332, 110))))
# 7 date range
RANGES = ["Today", "7D", "30D", "QTD", "YTD", "Custom"]
def chipsrange(x, y, on=2):
    s = ""; xx = x
    for i, r in enumerate(RANGES): w = len(r) * 5 + 14; s += rect(xx, y, w, 16, INK if i == on else "#FFFFFF", INK if i == on else "#CFC7BA", 8, .8) + t(xx + w / 2, y + 11, r, 8, "#FFFFFF" if i == on else INK, "hind", 600, "middle"); xx += w + 4
    return s
def ddcompare(x, y):
    return (rect(x, y, 112, 16, "#FFFFFF", "#CFC7BA", 3, .8) + t(x + 7, y + 11, "Sep 18 - Oct 17", 8, INK, "hind", 600) + f'<path d="M{x+100} {y+6} l3 4 l3 -4" fill="none" stroke="{INK}" stroke-width="1.2"/>'
            + rect(x + 120, y + 3, 20, 10, JUNGLE, "none", 5) + dot(x + 135, y + 8, 3.6, "#FFFFFF") + t(x + 146, y + 11, "Compare to last period", 8, INK, "hind", 600))
pick("Date Range", "Date range control", "a row of quick chips from Today to YTD, or one date picker with a compare-to-last-period switch?",
     ("dr_chips", "Quick Range Chips", "Today, 7D, 30D, QTD, YTD, Custom", "practical",
      C("Date Range", JUNGLE, chipsrange(8, 32) + kpirow(54, "six") + mrrchart(8, 106, 384, 178), ["One tap changes every number and", "chart on the page."],
        chipsrange(38, 104).replace('font-size="8"', 'font-size="7.5"') + "".join(pk(38 + (i % 2) * 84, 128 + (i // 2) * 60, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:4])) + pchart(252, 140))),
     ("dr_compare", "Picker + Compare", "Exact dates, vs the period before", "calm",
      C("Date Range", LAGOON, ddcompare(8, 32) + kpirow(54, "six") + mrrchart(8, 106, 384, 178) + poly([(30 + i * 352 / 7, 245 - i * 7 + (i % 2) * 4) for i in range(8)], GREY, 1.2, 'stroke-dasharray="3 3"'),
        ["Grey dashed line and the small change", "numbers show last period."],
        rect(38, 104, 164, 22, "#FFFFFF", "#CFC7BA", 5, .8) + t(46, 119, "Sep 18 - Oct 17", 9, INK, "hind", 600) + rect(38, 132, 22, 12, JUNGLE, "none", 6) + dot(54, 138, 4, "#FFFFFF") + t(66, 141.5, "Compare to last period", 8.5, INK, "hind", 600) + "".join(pk(38 + (i % 2) * 84, 152 + (i // 2) * 60, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:4])) + pchart(276, 130))))
# 8 phone layout (carousels both ways)
def ph_kpicar():
    s = "".join(pk(38 + i * 92, 106, 86, 62, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:3])) + dots(120, 178, 6, 0)
    return s + pchart(188, 118) + t(40, 326, "Needs Attention", 11, INK, "khand") + "".join(rect(38, 334 + i * 30, 164, 26, c + "14", c, 5, .8) + t(46, 350 + i * 30, a, 9, INK, "khand") for i, (c, a, b) in enumerate(ALS)) + plist(428, 2, True)
def ph_panels():
    s = rect(38, 104, 164, 330, "#FFFFFF", LINE, 8) + t(48, 124, "Money", 14, TERRA, "khand") + t(192, 124, "1 / 5", 8, MUTE, "hind", 600, "end")
    s += "".join(t(48, 150 + i * 30, v, 18, c, "khand") + t(120, 150 + i * 30, lb, 8.5, MUTE) for i, (v, lb, c, d) in enumerate([KPIS[1], KPIS[2], ("$221k", "Run rate / yr", JUNGLE, "")]))
    s += g(44, 236, 152 / 260, mrrchart(0, 0, 260, 300)) + rect(206, 104, 30, 330, CREAM, LINE, 8) + t(214, 124, "Jobs", 10, LAGOON, "khand")
    return s + dots(120, 446, 5, 0) + "".join(P(40 + i * 33, 458, l, [TERRA, LAGOON, JUNGLE, SAFFRON, INK][i], i == 0, 7, 13) for i, l in enumerate(["Money", "Jobs", "Techs", "Team", "More"]))
pick("Phone Layout", "Phone layout", "a swipe carousel of KPI tiles above a scrolling page, or the whole dashboard as full-screen panels you swipe through?",
     ("ph_kpi", "KPI Carousel On Top", "Swipe tiles, then chart and lists", "practical",
      C("Phone Layout", TERRA, "".join(rect(8 + i * 132, 34, 126, 60, "#FFFFFF", LINE, 6) + t(16 + i * 132, 62, v, 20, c, "khand") + t(16 + i * 132, 86, lb, 9, MUTE) for i, (v, lb, c, d) in enumerate(KPIS[:3])) + "".join(dot(200 + (i - 2.5) * 9, 102, 2.6 if i == 0 else 2, TERRA if i == 0 else "#CFC7BA") for i in range(6)) + g(8, 112, 1, mrrchart(0, 0, 384, 172)),
        ["Phone drawing: tiles swipe sideways", "(dots), chart and lists scroll below."], ph_kpicar())),
     ("ph_panels", "Full-Screen Panels", "Money, Jobs, Techs, Team, More", "bold",
      C("Phone Layout", LAGOON, "".join(rect(8 + i * 132, 34, 126, 250, "#FFFFFF" if i == 1 else CREAM, LINE, 8) + t(18 + i * 132, 56, nm, 15, c, "khand") for i, (nm, c) in enumerate([("Jobs", LAGOON), ("Money", TERRA), ("Techs", JUNGLE)])) + g(146, 66, 112 / 260, mrrchart(0, 0, 260, 300)) + kanban(14, 66, 114 * 4 + 18, 140).split('<rect x="')[0] + "".join(t(18, 80 + k * 20, f"{nm}  {n}", 9, INK, "hind", 600) for k, (nm, c, n) in enumerate(COLS)) + "".join(t(282, 80 + k * 22, f"{nm}  4 jobs", 9, INK, "hind", 600) for k, (nm, c) in enumerate(TECHS)),
        ["Phone drawing: one topic fills the", "screen; swipe left or right for the next."], ph_panels())))
# 9 density
def dens(gap, pad, rowh):
    s = ""; w = (DW - 2 * pad - 5 * gap) / 6
    s += "".join(kpi(pad + i * (w + gap), 32 + gap, w, 44, v, lb, c, d, big=15) for i, (v, lb, c, d) in enumerate(KPIS))
    y2 = 32 + gap + 44 + gap; cw = (DW - 2 * pad - gap) * .62
    s += mrrchart(pad, y2, cw, DH - y2 - pad) + mtable(pad + cw + gap, y2, DW - 2 * pad - cw - gap, int((DH - y2 - pad - 15) // rowh), rowh, [(6, "Member"), (54, "Status"), (92, "Next")])
    return s
pick("Density", "Spacing and density", "tight 6px gaps with slim 8px margins, or 10px gaps with moderate 16px margins?",
     ("den_tight", "Tight: 6px / 8px", "Most rows per screen", "practical",
      C("Density", JUNGLE, dens(6, 8, 15), ["10+ member rows beside the chart;", "nothing wasted, still readable."],
        "".join(pk(36 + (i % 2) * 86, 102 + (i // 2) * 58, 82, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:4])) + pchart(222, 116) + plist(342, 5, True))),
     ("den_mod", "Moderate: 10px / 16px", "A bit more air, still compact", "calm",
      C("Density", TERRA, dens(10, 16, 19), ["Slightly roomier; fewer rows fit,", "edges feel calmer."],
        "".join(pk(42 + (i % 2) * 82, 106 + (i // 2) * 64, 74, 56, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:4])) + g(44, 238, 152 / 260, mrrchart(0, 0, 260, 180)) + "".join(rect(42, 352 + i * 36, 156, 30, "#FFFFFF", LINE, 5) + t(50, 371 + i * 36, MEM[i][0], 9, INK, "hind", 600) + P(144, 361 + i * 36, MEM[i][2], MEM[i][3], s=7, h=12) for i in range(4)))))
# 10 export / share
def menu(x, y):
    items = [("Download PDF", "One-page summary"), ("Download CSV", "Members, jobs, revenue"), ("Copy share link", "Read-only, 7 days")]
    s = rect(x, y, 150, 18 + len(items) * 26, "#FFFFFF", "#CFC7BA", 4, .8) + f'<rect x="{x}" y="{y}" width="150" height="{18 + len(items) * 26}" fill="none" stroke="#00000010" stroke-width="4" rx="4"/>' + t(x + 8, y + 13, "Export", 9, INK, "khand")
    return s + "".join(t(x + 8, y + 30 + i * 26, a, 8.5, INK, "hind", 600) + t(x + 8, y + 40 + i * 26, b, 7, MUTE) for i, (a, b) in enumerate(items))
def snapshot(x, y, w):
    s = rect(x, y, w, 132, "#FFFFFF", TERRA, 6, 1) + rect(x, y, w, 22, TERRA + "14", "none", 6) + t(x + 8, y + 15, "Investor Snapshot", 10, TERRA, "khand") + t(x + w - 8, y + 15, "Read-only", 7.5, MUTE, "hind", 600, "end")
    s += "".join(t(x + 8 + (i % 2) * (w / 2), y + 44 + (i // 2) * 26, v, 14, c, "khand") + t(x + 8 + (i % 2) * (w / 2), y + 54 + (i // 2) * 26, lb, 7, MUTE) for i, (v, lb, c) in enumerate([("120", "Members", INK), ("$18.4k", "MRR", TERRA), ("1.8%", "Churn / mo", LAGOON), ("$221k", "Run rate", JUNGLE)]))
    return s + rect(x + 8, y + 104, w - 16, 20, INK, "none", 4) + t(x + w / 2, y + 117.5, "Copy link (expires in 7 days)", 8, "#FFFFFF", "hind", 600, "middle")
pick("Export Share", "Export and share", "an Export menu with PDF, CSV and a read-only link, or a one-tap Investor Snapshot card with the key numbers?",
     ("ex_menu", "Export Menu", "PDF, CSV or read-only link", "practical",
      C("Export Share", LAGOON, kpirow(34, "six") + mrrchart(8, 88, 384, 196) + rect(DW - 168, 30, 60, 0, "none") + menu(DW - 160, 30),
        ["Export sits next to the date range;", "pick a format, done."],
        "".join(pk(38 + (i % 2) * 84, 106, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:2])) + pchart(168, 120) + rect(31, 300, 178, 198, "#FFFFFF", "#CFC7BA", 12, .8) + rect(100, 308, 40, 4, "#CFC7BA", "none", 2) + t(42, 332, "Export", 14, INK, "khand") + "".join(rect(40, 342 + i * 40, 160, 34, CREAM, "none", 6) + t(50, 358 + i * 40, a, 9.5, INK, "hind", 600) + t(50, 369 + i * 40, b, 7.5, MUTE) for i, (a, b) in enumerate([("Download PDF", "One-page summary"), ("Download CSV", "Members, jobs, revenue"), ("Copy share link", "Read-only, 7 days")])))),
     ("ex_snap", "Investor Snapshot", "Key numbers card, one tap to share", "bold",
      C("Export Share", TERRA, kpirow(34, "six") + mrrchart(8, 88, 240, 196) + snapshot(256, 88, 136),
        ["A ready card for investors: members,", "MRR, churn, run rate; link expires."],
        "".join(pk(38 + (i % 2) * 84, 106, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:2])) + g(38, 172, 164 / 136, snapshot(0, 0, 136)) + pchart(340, 120))))
FEEL = {"calm", "bold", "practical", "playful", "premium"}
if "--preview" in sys.argv:
    d = sys.argv[sys.argv.index("--preview") + 1]; os.makedirs(d, exist_ok=True)
    h = "<html><head><link href='https://fonts.googleapis.com/css2?family=Hind:wght@400;600&family=Khand:wght@700&display=swap' rel='stylesheet'></head><body style='margin:0;background:#fff;display:grid;grid-template-columns:repeat(2,720px);gap:10px;font-family:Hind'>"
    for gg, ask, a, b in PK:
        for o in (a, b): h += f"<div><div style='width:400px;display:inline-block;vertical-align:top'>{o[4].split('</svg>')[0]}</svg></div><div style='width:300px;display:inline-block'>{o[4].split('</svg>')[1]}</svg></div><b>{o[1]}</b></div>"
    open(os.path.join(d, "preview.html"), "w").write(h + "</body></html>"); print("preview", d); sys.exit()
assert len(PK) == 10
pairs, O, add = kdeck("ucd_", "UpKeep")
for grp, ask, a, b in PK:
    for o in (a, b): assert len(o[1]) <= 24 and len(o[2]) <= 40 and o[3] in FEEL, o[:3]
    oa, ob = [O(o[0], o[1], o[2], o[3], o[4], tags=[grp, "company-dashboard"]) for o in (a, b)]
    add(grp, grp, oa, ob, ask)
cap_guard(pairs)
REQ = 'Max Oct 17 2026 21:11 ICT: "can you push a deck for the upkeep company dashboard"'
meta = {"brands": ["Smart Upkeep brand: white and warm cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only, no emoji."],
        "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": SLUG_KEY, "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True,
        "request": REQ, "applies_to": ["Smart Upkeep company dashboard (not the member app, tech app or Operator Console)"],
        "example_data": "Every name, number and date is example data.",
        "source_note": "No built company dashboard found; picks based on UpKeep notes and docs (forecast v3, investor pitch, Operator Console deck, forecast deck results).",
        "sources": {"content": "tools/build_company_dashboard_deck.py"}}
publish(DID, NAME, "UpKeep", pairs, meta, seed=1017, n=10, first=10)
dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == 10
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "upkeep-company-dashboard-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns)
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{DID}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}body.carding .opt .vis .v-svg svg{{min-height:0!important}}html body .vis svg.mph-m{{display:none!important}}@media(max-width:600px){{html body .vis svg.mph-d{{display:none!important}}html body .vis svg.mph-m{{display:block!important}}}}</style>
    {ns["SHARE"]}'''
from agent_links import patch as link_patch
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1).replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11")
os.makedirs(slug, exist_ok=True); pth = os.path.join(slug, "index.html"); open(pth, "w").write(s); link_patch(pth)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"id": DID, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "slug": slug, "added": dj["generated_at"]}, ensure_ascii=False))
