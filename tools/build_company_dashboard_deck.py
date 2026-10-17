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
DID = "upkeep-company-dashboard-deck"; NAME = "Company Dashboard Hub Deck"; SLUG_KEY = "company-dashboard"
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
def desk(inner, b=True):
    inner += band() if b else ''
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
    return frame(label, acc, (d_inner[8:] if d_inner.startswith("<!--D-->") else desk(chrome(d_inner))) + note(202, d_note), 300, "mph-d") + frame(label, acc, phone(p_inner, p_title), MH, "mph-m")
ALS = [(TERRA, "Finance: 1 payment failed", "Dan Example, Core plan"), (SAFFRON, "Technicians: 2 visits late", "Tech B, 20 min"), (LAGOON, "Members: 3 renewals", "Review before Friday")]
def strip(x, y, w):
    s = ""; xx = x; cw = (w - 12) / 3
    for c, a, b in ALS: s += rect(xx, y, cw, 26, c + "14", c, 4, .8) + rect(xx, y, 3, 26, c) + t(xx + 9, y + 11, a, 8.5, INK, "khand") + t(xx + 9, y + 21, b, 7, MUTE); xx += cw + 6
    return s
PK = []
def pick(group, loc, el, sentence, a, b): PK.append((group, f"{loc}: {el}, {sentence}", a, b))
SEC6 = [("Members", TERRA, "120", "members", "On track", JUNGLE, "Members Agent"), ("Technicians", LAGOON, "3", "techs on today", "1 late", TERRA, "Tech Agent"),
        ("Scheduling", JUNGLE, "46", "visits this week", "On track", JUNGLE, None), ("Finance", TERRA, "$18.4k", "MRR", "+4.1%", JUNGLE, "Finance Agent"),
        ("Growth", LAGOON, "14", "sign-ups this month", "On track", JUNGLE, None), ("Support", JUNGLE, "5", "open messages", "2 waiting", SAFFRON, None)]
SEC4 = [("Members", TERRA, "120", "members", "On track", JUNGLE, "Members Agent"), ("Field Ops", LAGOON, "46", "visits this week", "1 late", TERRA, "Ops Agent"),
        ("Finance", JUNGLE, "$18.4k", "MRR", "+4.1%", JUNGLE, "Finance Agent"), ("Growth", TERRA, "14", "sign-ups this month", "On track", JUNGLE, None)]
def owner(x, y, o, style="chip", sc=1):
    if style == "chip":
        if o: return dot(x + 6, y + 6, 6, INK) + t(x + 6, y + 8.6, o[0], 7, "#FFFFFF", "khand", 700, "middle") + t(x + 15, y + 9, o, 7.5, INK, "hind", 600)
        return f'<circle cx="{x+6}" cy="{y+6}" r="5.5" fill="none" stroke="#BDB6AA" stroke-dasharray="2 1.5"/>' + t(x + 15, y + 9, "Owner open", 7.5, GREY, "hind", 600)
    return t(x, y + 9, ("Run by " + o) if o else "No owner yet", 7.5, MUTE if o else GREY)
def hubcard(x, y, w, h, sec, style="tile", prev="kpi", own="chip"):
    nm, c, v, lb, st, sc, o = sec
    s = rect(x, y, w, h, "#FFFFFF", LINE, 6) + rect(x, y, w, 3, c)
    s += t(x + 8, y + 18, nm, 12, INK, "khand") + t(x + w - 8, y + 18, ">", 11, c, "khand", 700, "end")
    if prev == "kpi":
        s += t(x + 8, y + 44, v, 20, c, "khand") + t(x + 8, y + 55, lb, 7.5, MUTE) + spark(x + w * .55, y + 30, w * .36, 16, [3, 4, 4, 5, 6, 6, 7], c)
    else:
        s += dot(x + 12, y + 31, 3.5, sc) + t(x + 20, y + 34, st, 8, INK, "hind", 600) + t(x + 8, y + 50, f"{v} {lb}", 8, MUTE)
    return s + owner(x + 8, y + h - 17, o, own)
def hubgrid(secs, cols=3, y=34, h=74, **kw):
    w = (DW - 16 - (cols - 1) * 8) / cols
    return "".join(hubcard(8 + (i % cols) * (w + 8), y + (i // cols) * (h + 8), w, h, sc, **kw) for i, sc in enumerate(secs))
def hubrows(secs, y=34):
    s = ""
    for i, (nm, c, v, lb, st, sc, o) in enumerate(secs):
        yy = y + i * 30; s += rect(8, yy, DW - 16, 26, "#FFFFFF", LINE, 4) + rect(8, yy, 3, 26, c) + t(18, yy + 17, nm, 11, INK, "khand") + t(110, yy + 17, f"{v} {lb}", 8.5, INK, "hind", 600) + dot(214, yy + 13, 3.5, sc) + t(222, yy + 16, st, 8, MUTE) + owner(290, yy + 7, o) + t(DW - 14, yy + 17, ">", 11, c, "khand", 700, "end")
    return s
def HUB(inner, b=False): return "<!--D-->" + desk(chrome(inner, "Company Hub", "Today"), b)
def secchrome(inner, name="Finance", c=TERRA, style="band", o="Finance Agent"):
    s = rect(0, 0, DW, DH, "#FFFFFF")
    if style == "band":
        s += rect(0, 0, DW, 40, CREAM) + rect(0, 40, DW, 2, c) + rect(8, 9, 62, 20, "#FFFFFF", "#CFC7BA", 4, .8) + t(39, 22.5, "< Return", 8.5, INK, "hind", 600, "middle")
        s += mark(86, 19, 7, "#FFFFFF", c) + t(98, 25, name, 16, INK, "khand") + owner(DW - 110, 13, o)
        return s + g(0, 14, 1, inner)
    s += rect(0, 0, DW, 24, "#FFFFFF") + hl(0, DW, 24, "#E3DDD2") + mark(13, 12, 6, "#FFFFFF", TERRA) + t(24, 16, "Company", 9, LAGOON, "hind", 600) + t(64, 16, ">", 9, GREY) + t(74, 16.5, name, 11, INK, "khand") + owner(DW - 110, 6, o, "line")
    return s + g(0, -4, 1, inner)
def SEC(inner, **kw): return "<!--D-->" + desk(secchrome(inner, **kw), False)
FIN = lambda: kpirow(34, "four") + mrrchart(8, 94, 384, 190) + mtable(8, 290, 384, 5, 18)
def phub(cols=2, secs=SEC6):
    if cols == 2: return "".join(rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 78, "#FFFFFF", LINE, 6) + rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 3, sc[1]) + t(46 + (i % 2) * 84, 124 + (i // 2) * 84, sc[0], 11, INK, "khand") + t(46 + (i % 2) * 84, 148 + (i // 2) * 84, sc[2], 18, sc[1], "khand") + t(46 + (i % 2) * 84, 160 + (i // 2) * 84, sc[3], 7, MUTE) + owner(46 + (i % 2) * 84, 164 + (i // 2) * 84, sc[6]) for i, sc in enumerate(secs))
    return "".join(rect(38 + i * 150, 106, 144, 150, "#FFFFFF", LINE, 8) + rect(38 + i * 150, 106, 144, 4, sc[1]) + t(48 + i * 150, 130, sc[0], 15, INK, "khand") + t(48 + i * 150, 166, sc[2], 28, sc[1], "khand") + t(48 + i * 150, 180, sc[3], 8.5, MUTE) + owner(48 + i * 150, 230, sc[6]) for i, sc in enumerate(secs[:2])) + dots(120, 268, 6, 0) + plist(284, 6, True)
def psec(style="band", dy=0):
    if style == "band": hd = rect(31, 84, 178, 44, CREAM) + rect(31, 128, 178, 2, TERRA) + rect(38, 96, 46, 18, "#FFFFFF", "#CFC7BA", 4, .8) + t(61, 108.5, "< Return", 8, INK, "hind", 600, "middle") + t(92, 110, "Finance", 15, INK, "khand") + owner(150, 99, "Agent")
    else: hd = rect(31, 84, 178, 44, "#FFFFFF") + t(40, 100, "Company  >", 8.5, LAGOON, "hind", 600) + t(40, 118, "Finance", 15, INK, "khand") + owner(120, 108, "Finance Agent", "line")
    return rect(31, 84, 178, 30, "#FFFFFF") + hd + g(0, dy, 1, "".join(pk(38 + (i % 2) * 84, 138, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate([KPIS[1], KPIS[2]])) + pchart(200, 120) + plist(330, 4, True))
H, S = "Company Hub", "Section Dashboard"
pick("Hub Cards", H, "Hub card style", "a grid of section tiles like Apps Home, or one row per section in a tight list?",
     ("hub_tiles", "Section Tile Grid", "Tiles like Apps Home, tap to open", "practical",
      C("Hub Cards", TERRA, HUB(hubgrid(SEC6) + band(204)), ["Same feel as Apps Home: one tile per", "section opens its own dashboard."], phub(), "Company Hub")),
     ("hub_rows", "One Row Per Section", "Dense list, number + status + owner", "calm",
      C("Hub Cards", LAGOON, HUB(hubrows(SEC6) + band(220)), ["Every section in one glance as a", "row; tap the row to open it."], "".join(rect(38, 106 + i * 40, 164, 36, "#FFFFFF", LINE, 5) + rect(38, 106 + i * 40, 3, 36, sc[1]) + t(48, 121 + i * 40, sc[0], 11, INK, "khand") + t(48, 134 + i * 40, f"{sc[2]} {sc[3]}", 7.5, MUTE) + dot(160, 124 + i * 40, 3.5, sc[5]) + t(194, 127 + i * 40, ">", 11, sc[1], "khand", 700, "end") for i, sc in enumerate(SEC6)), "Company Hub")))
pick("Sections", H, "Which sections", "six sections (Members, Technicians, Scheduling, Finance, Growth, Support), or four bigger ones?",
     ("sec_six", "Six Sections", "One future agent per section", "practical",
      C("Sections", JUNGLE, HUB(hubgrid(SEC6) + band(204)), ["Members, Technicians, Scheduling,", "Finance, Growth, Support."], phub(), "Company Hub")),
     ("sec_four", "Four Bigger Sections", "Members, Field Ops, Finance, Growth", "calm",
      C("Sections", TERRA, HUB(hubgrid(SEC4, 2, 34, 76) + band(204)), ["Techs + scheduling merge into Field", "Ops; support sits inside Members."], phub(2, SEC4), "Company Hub")))
pick("Card Preview", H, "Card preview", "each card shows its main number with a trend line, or a status light with a short note?",
     ("pv_kpi", "Main Number + Trend", "e.g. MRR $18.4k with 7-week line", "practical",
      C("Card Preview", TERRA, HUB(hubgrid(SEC6) + band(204)), ["The headline number per section,", "trend line beside it."], phub(), "Company Hub")),
     ("pv_status", "Status Light + Note", "Green, amber or red, plus one note", "calm",
      C("Card Preview", LAGOON, HUB(hubgrid(SEC6, prev="status") + band(204)), ["Tells you where to look first;", "numbers wait inside the section."], "".join(rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 78, "#FFFFFF", LINE, 6) + rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 3, sc[1]) + t(46 + (i % 2) * 84, 124 + (i // 2) * 84, sc[0], 11, INK, "khand") + dot(50 + (i % 2) * 84, 141 + (i // 2) * 84, 4, sc[5]) + t(58 + (i % 2) * 84, 144 + (i // 2) * 84, sc[4], 8.5, INK, "hind", 600) + owner(46 + (i % 2) * 84, 162 + (i // 2) * 84, sc[6]) for i, sc in enumerate(SEC6)), "Company Hub")))
pick("Owner Badge", H, "Section owner badge", "a round initial chip with the agent name, or a plain 'Run by' text line?",
     ("ow_chip", "Initial Chip + Name", "Dashed circle when no owner yet", "bold",
      C("Owner Badge", TERRA, HUB(hubgrid(SEC6, own="chip") + band(204)), ["Owner reads at a glance; empty", "slots show a dashed 'Owner open'."], phub(), "Company Hub")),
     ("ow_line", "'Run By' Text Line", "Quiet text, 'No owner yet' in grey", "calm",
      C("Owner Badge", LAGOON, HUB(hubgrid(SEC6, own="line") + band(204)), ["Quieter cards; the owner is a", "small line at the bottom."], "".join(rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 78, "#FFFFFF", LINE, 6) + rect(38 + (i % 2) * 84, 106 + (i // 2) * 84, 80, 3, sc[1]) + t(46 + (i % 2) * 84, 124 + (i // 2) * 84, sc[0], 11, INK, "khand") + t(46 + (i % 2) * 84, 148 + (i // 2) * 84, sc[2], 18, sc[1], "khand") + owner(46 + (i % 2) * 84, 164 + (i // 2) * 84, sc[6], "line") for i, sc in enumerate(SEC6)), "Company Hub")))
pick("Hub Top", H, "Top of the hub", "a company KPI row above the section cards, or a Needs Attention strip pulled from every section?",
     ("top_kpi", "Company KPI Row", "Members, MRR, churn, visits, jobs", "practical",
      C("Hub Top", JUNGLE, HUB(kpirow(34, "six") + hubgrid(SEC6, y=88, h=70) + band(248)), ["Whole-company numbers first, then", "the doors into each section."], "".join(pk(38 + i * 84, 106, 80, 54, v, lb, c, d) for i, (v, lb, c, d) in enumerate(KPIS[:2])) + g(0, 60, 1, phub()), "Company Hub")),
     ("top_alert", "Needs Attention Strip", "Problems from all sections on top", "bold",
      C("Hub Top", TERRA, HUB(strip(8, 34, 384) + hubgrid(SEC6, y=68, h=74) + band(238)), ["Each alert names its section; tap", "to jump straight there."], "".join(rect(38, 106 + i * 30, 164, 26, c + "14", c, 5, .8) + t(46, 123 + i * 30, a, 9.5, INK, "khand") for i, (c, a, b) in enumerate(ALS)) + g(0, 92, 1, phub()), "Company Hub")))
pick("Section Header", S, "Section header", "a cream band with Return, section name and owner, or a slim breadcrumb line like Company > Finance?",
     ("hd_band", "Branded Band", "Return, name, owner chip", "bold",
      C("Section Header", TERRA, SEC(FIN()), ["Same header kit as agent boards,", "owner chip on the right."], psec("band"), "")),
     ("hd_crumb", "Slim Breadcrumb", "Company > Finance, owner as text", "calm",
      C("Section Header", LAGOON, SEC(FIN(), style="crumb"), ["Least height used; tap 'Company'", "to go back to the hub."], psec("crumb"), "")))
def switcher(): return "".join(P(8 + i * 66, 30, nm, sc[0] if nm == "Finance" else INK, nm == "Finance", 8, 15) for i, (nm, *sc) in enumerate([(x[0], x[1]) for x in SEC6]))
pick("Back To Hub", S, "Getting back to the hub", "one Return button that goes back in browser history, or Return plus tabs to jump between sections?",
     ("bk_return", "Return Button Only", "History-first, like agent boards", "practical",
      C("Back To Hub", JUNGLE, SEC(FIN()), ["Return goes back the way you came", "(browser Back works too)."], psec("band"), "")),
     ("bk_tabs", "Return + Section Tabs", "Hop Finance to Members directly", "bold",
      C("Back To Hub", TERRA, SEC(switcher() + g(0, 22, 1, FIN())), ["Tabs under the header switch", "sections without the hub."], psec("band", 16) + "".join(P(36 + i * 44, 134, nm, TERRA if i == 0 else INK, i == 0, 7, 13) for i, nm in enumerate(["Finance", "Members", "Techs", "More"])), "")))
def empty_owner(slot=True):
    if slot: return rect(8, 34, 384, 40, CREAM, "#BDB6AA", 6, .8, 'stroke-dasharray="4 3"') + f'<circle cx="30" cy="54" r="11" fill="none" stroke="#BDB6AA" stroke-dasharray="3 2"/>' + t(48, 51, "No owner yet", 11, INK, "khand") + t(48, 64, "An agent will run Growth. Until then, Max owns it.", 8, MUTE) + rect(DW - 92, 44, 80, 20, "#FFFFFF", INK, 4, .8) + t(DW - 52, 57.5, "Assign owner", 8, INK, "hind", 600, "middle")
    return ""
GROW = lambda y: "".join(kpi(8 + i * 97, y, 91, 50, v, lb, c, None, big=17) for i, (v, lb, c) in enumerate([("14", "Sign-ups / mo", TERRA), ("31%", "Referral share", JUNGLE), ("$42", "Cost per sign-up", LAGOON), ("6", "Waitlist", INK)])) + mrrchart(8, y + 58, 384, 170, legend=True, flags=False)
pick("Unowned Section", S, "Section with no owner yet", "a dashed 'No owner yet' slot with an Assign button, or no owner shown until one is set?",
     ("un_slot", "Visible Empty Slot", "Dashed card, Assign owner button", "practical",
      C("Unowned Section", LAGOON, SEC(empty_owner() + GROW(82), name="Growth", c=LAGOON, o=None), ["Makes the open seat obvious, ready", "for the future Growth agent."], psec("band").replace(">Finance<", ">Growth<") + rect(38, 330, 164, 0, "none"), "")),
     ("un_hide", "Hidden Until Set", "Clean header, owner appears later", "calm",
      C("Unowned Section", JUNGLE, SEC(GROW(34), name="Growth", c=JUNGLE, o=None, style="crumb").replace("No owner yet", ""), ["Nothing about owners until an agent", "is assigned."], psec("crumb").replace(">Finance<", ">Growth<").replace("Run by Finance Agent", ""), "")))
pick("Phone Hub", H, "Phone layout of the hub", "section cards in a two-column grid, or a swipe carousel of big section cards?",
     ("ph_grid", "Two-Column Grid", "All six sections on one screen", "practical",
      C("Phone Hub", TERRA, HUB(hubgrid(SEC6, cols=2, h=66) + band(256).replace("", "")), ["Desktop shown for context; phone", "drawing (right) is the 2-column grid."], phub(), "Company Hub")),
     ("ph_car", "Section Carousel", "Swipe big cards, list below", "bold",
      C("Phone Hub", LAGOON, HUB(hubgrid(SEC6) + band(204)), ["Desktop stays a grid; on the phone", "big cards swipe sideways (dots)."], phub(1), "Company Hub")))
def psec_car():
    hd = rect(31, 84, 178, 44, CREAM) + rect(31, 128, 178, 2, TERRA) + rect(38, 96, 46, 18, "#FFFFFF", "#CFC7BA", 4, .8) + t(61, 108.5, "< Return", 8, INK, "hind", 600, "middle") + t(92, 110, "Finance", 15, INK, "khand") + owner(150, 99, "Agent")
    return hd + "".join(pk(38 + i * 92, 138, 86, 62, v, lb, c, d) for i, (v, lb, c, d) in enumerate([KPIS[1], KPIS[2], KPIS[0]])) + dots(120, 210, 5, 0) + pchart(220, 120) + plist(350, 4, True)
def psec_pan():
    hd = rect(31, 84, 178, 44, CREAM) + rect(31, 128, 178, 2, TERRA) + rect(38, 96, 46, 18, "#FFFFFF", "#CFC7BA", 4, .8) + t(61, 108.5, "< Return", 8, INK, "hind", 600, "middle") + t(92, 110, "Finance", 15, INK, "khand") + owner(150, 99, "Agent")
    s = rect(38, 138, 164, 300, "#FFFFFF", LINE, 8) + t(48, 158, "Revenue", 14, TERRA, "khand") + t(192, 158, "1 / 4", 8, MUTE, "hind", 600, "end")
    s += "".join(t(48, 184 + i * 28, v, 18, c, "khand") + t(120, 184 + i * 28, lb, 8.5, MUTE) for i, (v, lb, c) in enumerate([("$18.4k", "MRR", TERRA), ("+4.1%", "vs last month", JUNGLE), ("$221k", "Run rate / yr", LAGOON)]))
    s += g(44, 266, 152 / 260, mrrchart(0, 0, 260, 280)) + rect(206, 138, 30, 300, CREAM, LINE, 8)
    return hd + s + dots(120, 452, 4, 0) + "".join(P(40 + i * 40, 464, l, TERRA if i == 0 else INK, i == 0, 7, 13) for i, l in enumerate(["Revenue", "Billing", "Costs", "Investor"]))
pick("Phone Section", S, "Phone layout of a section", "a swipe carousel of KPI tiles above the chart and list, or full-screen panels you swipe through?",
     ("ps_car", "KPI Carousel On Top", "Swipe tiles, then chart and list", "practical",
      C("Phone Section", TERRA, SEC(FIN()), ["Desktop shown for context; phone", "(right): tiles swipe sideways."], psec_car(), "")),
     ("ps_pan", "Full-Screen Panels", "Revenue, Billing, Costs, Investor", "bold",
      C("Phone Section", LAGOON, SEC(FIN()), ["Desktop shown for context; phone", "(right): one panel per screen."], psec_pan(), "")))
FEEL = {"calm", "bold", "practical", "playful", "premium"}
if "--preview" in sys.argv:
    d = sys.argv[sys.argv.index("--preview") + 1]; os.makedirs(d, exist_ok=True)
    h = "<html><head><link href='https://fonts.googleapis.com/css2?family=Hind:wght@400;600&family=Khand:wght@700&display=swap' rel='stylesheet'></head><body style='margin:0;background:#fff;display:grid;grid-template-columns:repeat(2,720px);gap:10px;font-family:Hind'>"
    for gg, ask, a, b in PK:
        for o in (a, b): h += f"<div><div style='width:400px;display:inline-block;vertical-align:top'>{o[4].split('</svg>')[0]}</svg></div><div style='width:300px;display:inline-block'>{o[4].split('</svg>')[1]}</svg></div><b>{o[1]}</b></div>"
    open(os.path.join(d, "preview.html"), "w").write(h + "</body></html>"); print("preview", d); sys.exit()
assert len(PK) == 10
pairs, O, add = kdeck("uch_", "UpKeep")
for grp, ask, a, b in PK:
    for o in (a, b): assert len(o[1]) <= 24 and len(o[2]) <= 40 and o[3] in FEEL, o[:3]
    oa, ob = [O(o[0], o[1], o[2], o[3], o[4], tags=[grp, "company-dashboard"]) for o in (a, b)]
    add(grp, grp, oa, ob, ask)
cap_guard(pairs)
REQ = ('Max Oct 17 2026 21:11 ICT: "can you push a deck for the upkeep company dashboard"; 21:17 ICT: "can we set up the company dashboard the same way '
       '[main dashboard then agent dashboards]. we will eventually have agents that are in charge of each section"')
meta = {"brands": ["Smart Upkeep brand: white and warm cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only, no emoji."],
        "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": SLUG_KEY, "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True,
        "request": REQ, "applies_to": ["Smart Upkeep company dashboard (not the member app, tech app or Operator Console)"],
        "example_data": "Every name, number and date is example data.",
        "source_note": "No built company dashboard found; picks based on UpKeep notes and docs plus Max 21:17 ICT: two-level hub (like Apps Home -> agent boards) with a section dashboard per future agent.",
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
