# ---- kit ----
# Six fresh UpKeep decks, Oct 18 2026 (after the 9:20 PM ICT republish): shared drawing kit.
# Every card is a drawn MOCKUP in phone CSS px (390 wide), scaled into the 240-unit card like hero1018.scr().
# Light only, Khand headings + Hind body. Sample data only; every number is labelled Forecast or Sample.
from md1018_kit import *
from draft_svg import crisp, esc
K = 240 / 390
BG = "#FBF6EE"; PAPER = "#FFFFFF"; DK = "#141414"; GR = "#6B655C"; LN = "#E8E1D6"; CRM = "#F7F1E7"
TC = "#C1502E"; LG = "#05668D"; JG = "#0B6E4F"; SF = "#D4A017"; CH = "#3A3F45"
_n = [0]
def T(x, y, s, size, col=DK, fam="hind", w=400, anchor="start", ls=None, extra=""):
    f = 'font-family="Khand" font-weight="700"' if fam == "khand" else f'font-family="Hind" font-weight="{w}"'
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {f}{f" letter-spacing={chr(34)}{ls}{chr(34)}" if ls else ""} {extra}>{esc(s)}</text>'
def R(x, y, w, h, fill="none", stroke="none", r=0, sw=1, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def L(x1, y1, x2, y2, c=LN, sw=1, dash=None):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{sw}"{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""} stroke-linecap="round"/>'
def C(cx, cy, r, fill, stroke="none", sw=1, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def Pth(d, fill="none", stroke="none", sw=1, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def chev(x, y, c=GR, s=6): return Pth(f"M{x} {y-s} L{x+s*.8} {y} L{x} {y+s}", stroke=c, sw=1.8)
def pill(x, y, s, fg, bg, size=12, pad=10, bd=None, w=None, fw=600, dash=False):
    w = w or len(s) * size * .52 + 2 * pad
    return R(x, y, w, size + 12, bg, bd or "none", (size + 12) / 2, 1.2, 'stroke-dasharray="4 3"' if dash else "") + T(x + w / 2, y + size + 2.5, s, size, fg, w=fw, anchor="middle"), w
def wm(x, y, size=20, anchor="start"):
    """smart up keep wordmark: ink, 'up' in terracotta under a small roof."""
    cw = size * .43; tw = 11 * cw; x0 = x - tw / 2 if anchor == "middle" else x
    s = f'<text x="{x0:.1f}" y="{y:.1f}" font-size="{size}" font-family="Khand" font-weight="700" fill="{DK}">smart<tspan fill="{TC}">up</tspan>keep</text>'
    ux = x0 + 5 * cw + 1
    return s + Pth(f"M{ux-2:.1f} {y-size*.62:.1f} L{ux+cw:.1f} {y-size*.98:.1f} L{ux+2*cw+2:.1f} {y-size*.62:.1f}", stroke=TC, sw=size * .09)
def sample_tag(x, y, s="SAMPLE"):
    w = len(s) * 7.4 + 26
    return R(x, y, w, 22, "#FFF6DD", "none", 6) + C(x + 11, y + 11, 3, SF) + T(x + 18, y + 15.5, s, 11, "#7A5A0E", w=700, ls="1.4"), w
def card(tag, body, h, note, y0=0):
    """One card: white MOCKUP band, the 390-px mockup window y0..h at 0.615, a terracotta note under it."""
    _n[0] += 1; top = 24; mh = (h - y0) * K; Hh = round(top + mh + 44); k = _n[0]
    s = (f'<clipPath id="w{k}"><rect x="0" y="{top}" width="{W}" height="{mh:.1f}"/></clipPath>'
         f'<g clip-path="url(#w{k})"><g transform="translate(0,{top - y0 * K:.2f}) scale({K:.4f})">{body}</g></g>')
    s += rect(0, 0, W, top, "#FFFFFF") + t(12, 16, tag.upper(), 7.5, INK, "hind", 700, extra='letter-spacing=".8"') + ln(top, 0, W, LINE)
    s += rect(193, 6, 36, 13, "#FFFFFF", "#D4A017", 3, 1, 'stroke-dasharray="3 2"') + t(211, 15.5, "MOCKUP", 6, "#8A6510", "hind", 700, "middle", 'letter-spacing=".5"')
    yn = Hh - 30
    s += ln(yn - 10, 0, W, LINE) + rect(12, yn - 4, 3, 24, TERRA) + t(20, yn + 6, note[0], 8.5, INK, "hind", 600) + t(20, yn + 18, note[1], 7.8, MUTE)
    return crisp(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="max-width:100%;height:auto">'
                 f'<clipPath id="r{k}"><rect width="{W}" height="{Hh}" rx="14"/></clipPath><g clip-path="url(#r{k})"><rect width="{W}" height="{Hh}" fill="#FFFFFF"/>' + s +
                 f'</g><rect x=".5" y=".5" width="{W-1}" height="{Hh-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def maker(prefix, loc):
    pairs, P = make(prefix, "UpKeep")
    def add(group, el, sentence, tag, h, a, b, y0=0):
        """a/b = (key, label, desc, feel, body, (note1, note2))"""
        oa = (a[0], a[1], a[2], a[3], card(tag, a[4], h, a[5], y0)); ob = (b[0], b[1], b[2], b[3], card(tag, b[4], h, b[5], y0))
        P(group, loc, el, sentence, oa, ob)
    return pairs, add
# ---------- shared people + van art (illustrated, fit young adults, branded) ----------
SKIN = ["#C68A62", "#E6B58F", "#8D5A3B", "#F1C9A5"]
def person(cx, base, shirt, skin, shoe="sneaker", hair="short", hold=None, sc=1.0, cover=True):
    """Front-facing illustrated tech: beanie, polo with chest mark, black belt, charcoal long pants, terracotta reusable shoe covers."""
    g = []; s = sc
    def X(v): return cx + v * s
    def Y(v): return base - v * s
    # legs / pants
    g.append(Pth(f"M{X(-22)} {Y(110)} L{X(-24)} {Y(10)} L{X(-4)} {Y(10)} L{X(0)} {Y(86)} L{X(4)} {Y(10)} L{X(24)} {Y(10)} L{X(22)} {Y(110)} Z", "#3B3F45"))
    g.append(L(X(0), Y(100), X(0), Y(84), "#2B2E33", 1.2))
    # shoes + covers
    for sx in (-14, 14):
        if shoe == "boot": g.append(R(X(sx - 12), Y(18), 24 * s, 12 * s, "#2A2522", "none", 3 * s))
        g.append(Pth(f"M{X(sx-13)} {Y(10)} Q{X(sx-14)} {Y(-2)} {X(sx-4)} {Y(-2)} L{X(sx+15)} {Y(-2)} Q{X(sx+16)} {Y(6)} {X(sx+10)} {Y(10)} Z", TC if cover else ("#2A2522" if shoe == "boot" else "#F2F2F2"), "#8E3A20" if cover else "#999", .8))
        if cover: g.append(T(X(sx + 1), Y(2), "su", 6 * s, "#FFFFFF", "khand", anchor="middle"))
    # belt
    g.append(R(X(-23), Y(116), 46 * s, 7 * s, "#111111")); g.append(R(X(-4), Y(117), 8 * s, 9 * s, "none", "#BDB6AA", 1, 1.2))
    # torso polo
    g.append(Pth(f"M{X(-24)} {Y(116)} L{X(-26)} {Y(172)} L{X(-40)} {Y(166)} L{X(-46)} {Y(150)} L{X(-30)} {Y(182)} Q{X(0)} {Y(192)} {X(30)} {Y(182)} L{X(46)} {Y(150)} L{X(40)} {Y(166)} L{X(26)} {Y(172)} L{X(24)} {Y(116)} Z", shirt))
    g.append(Pth(f"M{X(-30)} {Y(182)} L{X(-46)} {Y(150)} L{X(-38)} {Y(144)} L{X(-26)} {Y(164)}", shirt, "#00000022", 1))
    g.append(Pth(f"M{X(30)} {Y(182)} L{X(46)} {Y(150)} L{X(38)} {Y(144)} L{X(26)} {Y(164)}", shirt, "#00000022", 1))
    g.append(Pth(f"M{X(-9)} {Y(186)} L{X(0)} {Y(172)} L{X(9)} {Y(186)}", "#00000026"))
    g.append(T(X(13), Y(160), "smartupkeep", 5.5 * s, "#FFFFFF", "khand", anchor="middle"))
    # arms
    if hold == "filter":
        g.append(Pth(f"M{X(-42)} {Y(148)} L{X(-36)} {Y(112)} L{X(-12)} {Y(124)}", "none", skin, 9 * s))
        g.append(Pth(f"M{X(42)} {Y(148)} L{X(36)} {Y(112)} L{X(12)} {Y(124)}", "none", skin, 9 * s))
        g.append(R(X(-18), Y(140), 36 * s, 26 * s, "#F4F1EA", "#9A948A", 2, 1.2)); g.append("".join(L(X(-18 + i * 6), Y(140), X(-18 + i * 6), Y(114), "#CFC8BC", .8) for i in range(1, 6)))
    elif hold == "tablet":
        g.append(Pth(f"M{X(-42)} {Y(148)} L{X(-48)} {Y(96)}", "none", skin, 9 * s)); g.append(C(X(-48), Y(92), 5 * s, "#2F3237"))
        g.append(Pth(f"M{X(42)} {Y(148)} L{X(34)} {Y(116)} L{X(14)} {Y(126)}", "none", skin, 9 * s))
        g.append(R(X(-2), Y(146), 30 * s, 38 * s, "#22262B", "none", 3)); g.append(R(X(1), Y(143), 24 * s, 30 * s, "#BFE0EA", "none", 2))
    else:
        for sx in (-1, 1):
            g.append(Pth(f"M{X(42*sx)} {Y(148)} L{X(48*sx)} {Y(96)}", "none", skin, 9 * s)); g.append(C(X(48 * sx), Y(92), 5.5 * s, "#2F3237"))
            g.append(R(X(48 * sx - 5.5), Y(102), 11 * s, 4 * s, TC))
    # head
    g.append(R(X(-6), Y(198), 12 * s, 12 * s, skin)); g.append(C(X(0), Y(214), 17 * s, skin))
    if hair == "long": g.append(Pth(f"M{X(14)} {Y(222)} Q{X(28)} {Y(196)} {X(18)} {Y(170)} Q{X(14)} {Y(196)} {X(10)} {Y(206)} Z", "#5A3A22"))
    g.append(Pth(f"M{X(-18)} {Y(216)} Q{X(-18)} {Y(238)} {X(0)} {Y(238)} Q{X(18)} {Y(238)} {X(18)} {Y(216)} Z", "#3A3F45"))
    g.append(R(X(-6), Y(226), 12 * s, 5 * s, TC, "none", 1))
    g.append(C(X(-6), Y(212), 1.6 * s, "#2B2B2B") + C(X(6), Y(212), 1.6 * s, "#2B2B2B") + Pth(f"M{X(-5)} {Y(204)} Q{X(0)} {Y(200)} {X(5)} {Y(204)}", stroke="#7A3E28", sw=1.3 * s))
    return "".join(g)
def van(x, y, sc=1.0, stripe="swoosh", doors=False, labels=None, gear=True):
    """High-roof Transit-shape cargo van, side view, no maker badge. stripe: swoosh | tagline."""
    s = sc
    def X(v): return x + v * s
    def Y(v): return y + v * s
    g = []
    g.append(R(X(30), Y(-10), 200 * s, 8 * s, "none", "#9A948A", 2, 1.4))
    g.append("".join(L(X(40 + i * 24), Y(-10), X(40 + i * 24), Y(-2), "#9A948A", 1.2) for i in range(8)))
    g.append(Pth(f"M{X(14)} {Y(0)} L{X(232)} {Y(0)} Q{X(244)} {Y(0)} {X(250)} {Y(14)} L{X(276)} {Y(58)} Q{X(300)} {Y(66)} {X(304)} {Y(84)} L{X(306)} {Y(118)} L{X(8)} {Y(118)} L{X(8)} {Y(8)} Q{X(8)} {Y(0)} {X(14)} {Y(0)} Z", "#FFFFFF", "#BDB6AA", 1.4))
    g.append(Pth(f"M{X(240)} {Y(14)} L{X(262)} {Y(54)} L{X(240)} {Y(54)} Z", "#CFE6EE", "#9DB9C4", 1))
    g.append(R(X(196), Y(14), 36 * s, 36 * s, "#CFE6EE", "#9DB9C4", 3))
    g.append(L(X(190), Y(10), X(190), Y(116), "#D6D0C6", 1)); g.append(L(X(236), Y(56), X(236), Y(116), "#D6D0C6", 1))
    g.append(R(X(296), Y(80), 10 * s, 8 * s, "#F3E6B5", "none", 2))
    if stripe == "swoosh":
        g.append(Pth(f"M{X(8)} {Y(98)} Q{X(150)} {Y(84)} {X(306)} {Y(92)} L{X(306)} {Y(104)} Q{X(150)} {Y(96)} {X(8)} {Y(108)} Z", TC))
        g.append(Pth(f"M{X(8)} {Y(110)} Q{X(150)} {Y(98)} {X(306)} {Y(106)}", stroke=LG, sw=2.5 * s))
        g.append(wm(X(14), Y(46), 11.5 * s) if doors else wm(X(80), Y(52), 22 * s))
    else:
        g.append(R(X(8), Y(88), 298 * s, 18 * s, TC)); g.append(T(X(100), Y(101), "HOME MAINTENANCE MEMBERSHIP", 9 * s, "#FFFFFF", w=700, anchor="middle", ls="1.4"))
        g.append(wm(X(14), Y(50), 11.5 * s) if doors else wm(X(80), Y(56), 24 * s))
    g.append(R(X(4), Y(112), 306 * s, 10 * s, "#2B2E33", "none", 3))
    for cx in (62, 248):
        g.append(C(X(cx), Y(122), 19 * s, "#22252A") + C(X(cx), Y(122), 9 * s, "#C9C2B6") + C(X(cx), Y(122), 3 * s, "#8A847A"))
    if doors:
        g.append(R(X(84), Y(10), 96 * s, 96 * s, "#EFEAE2", "#BDB6AA", 2, 1.2))
        if gear:
            for i in range(4): g.append(R(X(90 + i * 22), Y(16), 18 * s, 30 * s, "#FFFFFF", "#CFC8BC", 1, 1))
            g.append(R(X(90), Y(52), 84 * s, 24 * s, "#9AA3AD", "none", 2)); g.append("".join(L(X(92), Y(58 + i * 6), X(172), Y(58 + i * 6), "#7D8691", 1) for i in range(3)))
            g.append(R(X(90), Y(80), 30 * s, 22 * s, TC, "none", 3)); g.append(R(X(126), Y(80), 48 * s, 22 * s, LG, "none", 3))
            g.append(R(X(148), Y(30), 22 * s, 14 * s, "#2F3237", "none", 2)); g.append(C(X(104), Y(70), 4 * s, SF))
    return "".join(g)
# ---------- pitch slide frame ----------
def pframe(num, eyebrow, lines, tsize=46, h=844):
    s = R(0, 0, 390, h, "#FFFFFF") + wm(18, 46, 22)
    s += T(330, 44, f"{num:02d}", 14, DK, w=700, anchor="end") + T(352, 44, "/ 11", 14, "#9A948A", w=600, anchor="end")
    s += "".join(R(358 + (i % 2) * 9, 31 + (i // 2) * 9, 6, 6, "none", DK, 1.5, 1.6) for i in range(4))
    s += "".join(R(18 + i * 32, 62, 28, 3, TC if i == num - 1 else ("#E2B8A8" if i < num - 1 else "#EAE5DD"), "none", 1.5) for i in range(11))
    s += L(18, 98, 34, 98, TC, 1.6) + T(42, 103, eyebrow.upper(), 12.5, TC, w=600, ls="2.2")
    y = 104
    for i, l in enumerate(lines): y += tsize * .98; s += T(18, y + 4, l, tsize, DK, "khand")
    return s, y + 16
def pfoot(nxt, h=844):
    y = h - 92
    return (R(0, y, 390, 92, "#FFFFFF") + L(0, y, 390, y, LN) + C(42, y + 34, 22, "#FFFFFF", LN, 1.2) + Pth(f"M46 {y+27} L39 {y+34} L46 {y+41}", stroke=DK, sw=2)
            + T(76, y + 28, "UP NEXT", 11, GR, w=600, ls="1.8") + T(76, y + 48, nxt, 15, DK, w=600) + R(282, y + 12, 92, 46, DK, "none", 23) + T(318, y + 41, "Next", 15, "#FFFFFF", w=700, anchor="middle") + chev(343, y + 35, "#FFFFFF", 5))
# forecast chart (Forecast numbers only; Plus starting price basis $164/mo)
RAMP = [50, 150, 220, 290, 360, 440, 530, 620, 720]; RAMP_T = [1, 2, 3, 4, 4, 5, 6, 7, 8]
EVEN = [50, 150, 220, 290, 360, 430, 500, 570, 640]; EVEN_T = [1, 2, 3, 4, 4, 5, 5, 6, 7]
QL = ["Beta", "Apr 1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4"]; QQ = ["Jan–Mar 2027", "Apr 1, 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028", "Q3 2028", "Q4 2028"]
def money(v, short=False):
    return f"${v/1000:.0f}K" if short else f"${v:,.0f}"
def fchart(y, vals=RAMP, techs=RAMP_T, sel=8, tech="line", beta="none", readout="row", short=False, head=True, rev_beta=True):
    s = ""
    if head:
        s += T(18, y + 22, "Growth To 2028", 21, DK, "khand"); g, _ = sample_tag(262, y + 4, "FORECAST"); s += g; y += 40
    x0, bw, gap, ch = 22, 32, 6.5, 120; top = y + 26; base = top + ch; mx = 740
    pts = []
    for i, v in enumerate(vals):
        x = x0 + i * (bw + gap); hgt = ch * v / mx; on = i == sel
        if beta == "split" and i >= 1:
            bh = ch * 50 / mx
            s += R(x, base - hgt, bw, hgt - bh, TC if on else "#E9B8A6", "none", 3) + R(x, base - bh, bw, bh, "#CFC8BC", "none", 0)
        else:
            s += R(x, base - hgt, bw, hgt, TC if on else "#E9B8A6", "none", 3)
        if i == 0: s += R(x, base - hgt, bw, hgt, "#D9D3C9", "none", 3)
        if on and readout == "row": s += T(x + bw / 2, base - hgt - 6, str(v), 12, TC, w=700, anchor="middle")
        if tech == "nums": s += T(x + bw / 2, base - hgt - (20 if on and readout == "row" else 6), f"{techs[i]}", 11, LG, w=700, anchor="middle")
        pts.append((x + bw / 2, base - ch * techs[i] / 9.2 - 4))
        s += T(x + bw / 2, base + 16, QL[i], 11.5, DK if on else GR, w=700 if on else 500, anchor="middle")
    if tech == "line": s += Pth("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), stroke=LG, sw=2.4)
    s += L(18, base + 26, 372, base + 26, LN) + T(40, base + 44, "Launch", 11.5, GR, anchor="middle") + T(178, base + 44, "2027", 11.5, GR, anchor="middle") + T(296, base + 44, "2028", 11.5, GR, anchor="middle")
    y = base + 56
    s += R(18, y, 12, 9, TC, "none", 2) + T(36, y + 9, "Homes", 11.5, GR)
    s += (Pth(f"M86 {y+5} L100 {y+5}", stroke=LG, sw=2.4) + T(106, y + 9, "Techs", 11.5, GR)) if tech == "line" else (T(86, y + 9, "8", 11.5, LG, w=700) + T(96, y + 9, "= techs", 11.5, GR))
    if beta == "split": s += R(160, y, 12, 9, "#CFC8BC", "none", 2) + T(178, y + 9, "Beta homes", 11.5, GR)
    s += T(372, y + 9, "Tap a quarter", 12, LG, w=600, anchor="end")
    v = vals[sel]; pay = v - (50 if (beta == "split" and sel >= 1) else 0); rev = pay * 164 if sel >= 1 else None
    rtxt = (money(rev, short) + "/mo") if rev else "Beta, not counted"
    if readout == "row":
        y += 22; s += R(18, y, 354, 40, CRM, "none", 10) + T(30, y + 25, QQ[sel] if sel != 8 else "Q4 2028", 13, DK, w=700)
        s += T(140, y + 25, f"{v}", 15, DK, w=700) + T(170 if v >= 100 else 162, y + 25, "homes", 12, GR) + T(222, y + 25, f"{techs[sel]}", 15, DK, w=700) + T(234, y + 25, "techs", 12, GR) + T(366, y + 25, rtxt, 14, DK, w=700, anchor="end")
        y += 48
    else:
        x = x0 + sel * (bw + gap) + bw / 2; hgt = ch * v / mx; bx = min(max(x - 78, 18), 216); by = base - hgt - 74
        s += R(bx, by, 156, 62, "#FFFFFF", "#D6D0C6", 10, 1, 'filter="url(#sh)"') + T(bx + 12, by + 19, QQ[sel], 12, TC, w=700) + T(bx + 12, by + 36, f"{v} homes · {techs[sel]} techs", 12, DK, w=600) + T(bx + 12, by + 53, rtxt, 13, DK, w=700)
        s += Pth(f"M{x-6} {by+62} L{x} {by+70} L{x+6} {by+62} Z", "#FFFFFF")
        y += 10
    return s, y
SHADOW = '<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#783C1E" flood-opacity=".13"/></filter></defs>'

# ---- pitch ----
# Pitch decks for the round-2 investor pitch (upkeep-cc bb2e154). Mockups of the live slides; every number is Forecast or Sample.
PLOC = "Smart Upkeep Investor Pitch Mockup"
def tslide(chart_kw, h=560, title=True):
    if title:
        s, y = pframe(8, "Timeline", ["Road to launch."], 44)
        s += T(18, y + 6, "Dec 1, 2026 sign-ups · Jan–Mar 2027 beta · Apr 1, 2027 launch", 12, GR); y += 26
    else: s, y = R(0, 0, 390, h, "#FFFFFF"), 20
    g, y = fchart(y, **chart_kw); return SHADOW + s + g
TODO = [("Change HVAC filter", "Dec 1", False, "Furnace strain"), ("Clean gutters", "Oct 1", True, "Water damage"), ("Flush water heater", "Dec 1", False, "Sediment"),
        ("Test smoke/CO", "Oct 1", True, "Dead battery"), ("Service the AC", "Dec 1", False, "AC breakdown")]
def todo(y, mode="all"):
    s = R(18, y, 354, 230, "#FFFFFF", LN, 14, 1.2, 'filter="url(#sh)"') + T(34, y + 32, "Home To-Do", 17, DK, "khand") + T(358, y + 30, "DECEMBER", 11.5, GR, w=600, anchor="end", ls="1.5") + L(34, y + 46, 356, y + 46, LN)
    for i, (task, d, skip, cons) in enumerate(TODO):
        yy = y + 70 + i * 33
        s += R(34, yy - 11, 14, 14, "#FFFFFF", TC if mode == "all" or skip else "#B9B2A6", 3, 1.4) + T(58, yy + 1, task, 13, "#9A948A" if skip else DK)
        if skip: s += L(58, yy - 3, 58 + len(task) * 6.4, yy - 3, TC, 1.6)
        s += T(226, yy + 1, d, 11.5, GR, w=600, anchor="end")
        red = mode == "all" or skip; lab = cons if red else "Next month"; w = len(lab) * 6.1 + 16
        s += R(358 - w, yy - 12, w, 20, "#FBE3DA" if red else "#FFF3CC", "none", 6) + T(358 - w / 2, yy + 2, lab, 11.5, "#A8431F" if red else "#7A5A0E", w=600, anchor="middle")
        if i < 4: s += L(34, yy + 16, 356, yy + 16, "#EFEAE2", 1, "3 3")
    return s
def pslide2(headline=("Upkeep gets", "skipped."), sub=("Easy to forget, hard to schedule. Small, cheap", "fixes become big, expensive repairs."), mode="all", extra=None, h=620):
    s, y = pframe(2, "The Problem", list(headline), 50)
    for i, l in enumerate(sub): s += T(18, y + 14 + i * 21, l, 15.5, "#3D3D3D")
    y += 14 + len(sub) * 21 + 10
    s += todo(y, mode); y += 244
    if extra: s += extra(y)
    return SHADOW + s
def furnace(x, y, sc=1):
    return (R(x, y, 52 * sc, 108 * sc, "#FFFFFF", "#9A948A", 4, 1.4) + R(x + 6 * sc, y + 10 * sc, 40 * sc, 22 * sc, "#EFEAE2", "none", 2) + C(x + 26 * sc, y + 54 * sc, 7 * sc, "#FBE3DA", TC, 1.2)
            + Pth(f"M{x+26*sc} {y+49*sc} q4 4 0 9 q-4 -4 0 -9", TC) + L(x + 14 * sc, y + 78 * sc, x + 38 * sc, y + 78 * sc, "#9A948A", 1.4) + L(x + 14 * sc, y + 86 * sc, x + 38 * sc, y + 86 * sc, "#9A948A", 1.4))
def example(kind):
    def f(y):
        s = R(18, y, 354, 250, CRM, "#EADFCF", 14, 1)
        if kind == "bars":
            s += person(78, y + 150, TC, SKIN[0], sc=.55, hold="filter") + furnace(110, y + 30)
            s += T(186, y + 30, "EXAMPLE: FURNACE FILTER", 11.5, TC, w=700, ls="1.4") + T(186, y + 56, "Small fix, on schedule", 13, DK, w=600) + R(186, y + 64, 40, 9, JG, "none", 4.5)
            s += T(186, y + 92, "Big repair, later", 13, DK, w=600) + R(186, y + 100, 170, 9, TC, "none", 4.5)
            g, _ = sample_tag(186, y + 118); s += g; yq = y + 172
        else:
            s += T(36, y + 30, "EXAMPLE: FURNACE FILTER", 11.5, TC, w=700, ls="1.4")
            for j, (lab, c, clog) in enumerate((("Changed on schedule", JG, False), ("Skipped for a year", TC, True))):
                x = 36 + j * 170
                s += R(x, y + 44, 148, 84, "#FFFFFF", "#D6D0C6", 8, 1) + R(x + 34, y + 54, 80, 50, "#F4F1EA" if not clog else "#B8AE9C", "#9A948A", 2, 1.2)
                s += "".join(L(x + 34 + k * 10, y + 54, x + 34 + k * 10, y + 104, "#CFC8BC" if not clog else "#8E846F", 1) for k in range(1, 8))
                s += C(x + 18, y + 64, 7, c + "22") + T(x + 74, y + 122, lab, 11.5, c, w=700, anchor="middle")
            s += T(36, y + 152, "Small fix, on schedule vs big repair, later.", 13, DK, w=600); yq = y + 172
        return s + QUOTE(yq)
    return f
def QUOTE(y, style="pull"):
    if style == "pull":
        return (R(34, y, 3, 62, TC) + T(46, y + 16, "“Dirt and neglect are the top causes of", 14, DK, w=600) + T(46, y + 35, "heating and cooling system failure and", 14, DK, w=600)
                + T(46, y + 54, "inefficiency.”", 14, DK, w=600) + T(46, y + 74, "Source: ENERGY STAR", 11.5, GR))
    return (T(36, y + 4, "QUICK FACT", 11.5, LG, w=700, ls="1.6") + T(36, y + 30, "Dirt and neglect: the top causes", 22, DK, "khand") + T(36, y + 54, "of heating and cooling failure.", 22, DK, "khand")
            + R(36, y + 64, 150, 20, "#E3F0F5", "none", 10) + T(46, y + 78, "Source: ENERGY STAR", 11.5, LG, w=600))
def T_PITCH_FORECAST():
    pairs, add = maker("p18fp_", PLOC)
    TAG = "PITCH · TIMELINE SLIDE"
    add("Forecast", "Forecast pace", "after Apr 1, 2027 should the growth bars keep today's rising pace of +70 to +100 homes a quarter or a steady +70 every quarter?", TAG, 510,
        ("ramp", "Rising Pace, +70 To +100", "Ends at 720 homes and $118,080/mo in Q4 2028, all Forecast.", "focused", tslide(dict()), ("Today's chart", "Pace picks up in 2028, Forecast")),
        ("even", "Steady +70 A Quarter", "Ends at 640 homes and $104,960/mo in Q4 2028, all Forecast.", "calm", tslide(dict(vals=EVEN, techs=EVEN_T)), ("More cautious line", "Same Plus price basis, Forecast")))
    add("Forecast", "Beta homes in revenue", "should the 50 beta homes count as paying from Apr 1 like today or stay out of the revenue figure until their terms are set?", TAG, 510,
        ("count", "Beta Homes Pay From Apr 1", "Apr 1: 150 homes, $24,600/mo; Q4 2028: $118,080/mo, Forecast.", "focused", tslide(dict(sel=1)), ("Today's math", "Beta itself stays not counted")),
        ("apart", "Beta Homes Kept Apart", "Grey base on each bar; Apr 1: $16,400/mo from 100 paying homes.", "practical", tslide(dict(sel=1, beta="split")), ("Revenue only from paying homes", "Beta terms still open, Forecast")))
    add("Forecast", "Revenue figure style", "in the tapped-quarter readout should monthly revenue show the exact figure or a rounded one?", TAG, 350,
        ("exact", "Exact Figure", "Q4 2028 readout: $118,080/mo, Forecast.", "practical", tslide(dict(), 350, False), ("Today's readout", "Shows the math")),
        ("round", "Rounded Figure", "Q4 2028 readout: $118K/mo, Forecast.", "calm", tslide(dict(short=True), 350, False), ("Easier to read fast", "Less false precision")))
    add("Forecast", "Tapped quarter readout", "when an investor taps a quarter should homes, techs and revenue show in the row under the chart or in a bubble over the tapped bar?", TAG, 350,
        ("row", "Row Under The Chart", "One cream row under the bars, like today.", "calm", tslide(dict(sel=6), 350, False), ("Chart stays clean", "Same place every tap")),
        ("bubble", "Bubble Over The Bar", "A small white bubble points at the tapped bar.", "lively", tslide(dict(sel=6, readout="bubble"), 350, False), ("Ties numbers to the bar", "Row under the chart goes")))
    add("Forecast", "Techs on the chart", "should the tech count show as the blue line over the bars or as a small blue number on top of each bar?", TAG, 350,
        ("line", "Blue Line Over The Bars", "Techs climb as one line, like today.", "lively", tslide(dict(), 350, False), ("Shows the trend", "Today's chart")),
        ("nums", "Number On Each Bar", "A small blue tech count sits on every bar.", "practical", tslide(dict(tech="nums"), 350, False), ("Exact count per quarter", "No second line to read")))
    P2 = "PITCH · PROBLEM SLIDE"
    add("Problem", "Problem headline", "should the Problem slide keep Upkeep gets skipped as the headline or say Skipped upkeep gets expensive?", P2, 470,
        ("keep", "Upkeep Gets Skipped.", "Today's short headline over the to-do list.", "calm", pslide2(), ("Today's slide", "Plain and relatable")),
        ("cost", "Skipped Upkeep Gets Expensive.", "Names the cost in the headline itself.", "focused", pslide2(("Skipped upkeep", "gets expensive.")), ("Leads with the money", "Same to-do list under it")))
    add("Problem", "Problem subline", "under the headline should the subline keep both sentences or shrink to one short line?", P2, 470,
        ("two", "Two Sentences", "Easy to forget, hard to schedule; small fixes become big repairs.", "warm", pslide2(), ("Today's subline", "Says why it gets skipped")),
        ("one", "One Short Line", "Small fixes, skipped, turn into big repairs.", "focused", pslide2(sub=("Small fixes, skipped, turn into big repairs.",)), ("Faster read", "To-do list sits higher")))
    add("Problem", "To-do end state", "when the to-do animation ends should all five tasks turn into red costs or only the two skipped tasks?", P2, 520, 
        ("all", "All Five Turn Red", "Every row ends on its cost, like today.", "focused", pslide2(mode="all"), ("Strong finish", "Every task has a cost")),
        ("skip", "Only The Skipped Two", "Skipped rows go red; the rest stay Next month.", "calm", pslide2(mode="skip"), ("Shows cause and effect", "Calmer list")), y0=170)
    add("Problem", "Furnace example", "for the furnace example card should it keep the branded tech with two bars or show a clean filter next to a clogged one?", P2, 790,
        ("bars", "Branded Tech And Two Bars", "Tech at the furnace; short green bar vs long red bar, Sample.", "warm", pslide2(extra=example("bars"), h=844), ("Today's card", "Our uniform in the picture")),
        ("filters", "Clean Vs Clogged Filter", "Two filter drawings side by side, no bars.", "practical", pslide2(extra=example("filters"), h=844), ("Easy to get in a glance", "No Sample bars needed")), y0=380)
    def qfx(style):
        def f(y): return R(18, y, 354, 110, CRM, "#EADFCF", 14, 1) + QUOTE(y + 20, style)
        return f
    add("Problem", "Fact style", "should the ENERGY STAR fact stay a quoted line with a terracotta rule or become a bold Quick fact headline with a source chip?", P2, 650,
        ("pull", "Quoted Line", "The full quote in quotes, source under it.", "calm", pslide2(extra=qfx("pull"), h=844), ("Today's look", "Word for word from the source")),
        ("fact", "Bold Quick Fact", "Short bold fact, ENERGY STAR on a blue chip.", "focused", pslide2(extra=qfx("fact"), h=844), ("Punchier", "Same sourced fact")), y0=380)
    return pairs
# ---------------- Pitch deck 2: founder tiles, brand art, transitions, ask ----------------
def founder(t1=("Multi-million-dollar", "home builds", "Has managed them, start", "to finish."), t3=("AI agent training", "", "Trains the agent teams.", ""), sub="ONE OPERATOR, FIELD AND PLATFORM", hi=None, h=700):
    s, y = pframe(9, "The Founder", ["Built By A Builder"], 44)
    s += T(18, y + 6, sub, 12.5, GR, w=500, ls="2.2"); y += 22
    s += R(18, y, 354, 52, DK, "none", 10) + C(46, y + 26, 14, "#FFFFFF22") + Pth(f"M40 {y+19} L46 {y+16} L52 {y+19} L52 {y+27} Q46 {y+34} 46 {y+34} Q40 {y+31} 40 {y+27} Z", stroke="#FFFFFF", sw=1.4)
    s += T(70, y + 22, "Licensed Residential Builder, State of", 13.5, "#FFFFFF", w=600) + T(70, y + 40, "Michigan, since 2012", 13.5, "#FFFFFF", w=600); y += 68
    s += T(18, y + 20, "Designed and built the platform", 22, DK, "khand") + T(18, y + 40, "Including every app shown in this deck.", 12.5, GR); y += 54
    tiles = [t1, ("Finance and", "accounting", "A background in both.", ""), t3, ("Multiple languages", "", "Works in several.", "")]
    s += L(18, y, 372, y, LN)
    for i, (a, b, c, d) in enumerate(tiles):
        x = 18 + (i % 2) * 180; yy = y + (i // 2) * 96
        if hi == i: s += R(x - 4, yy + 4, 176, 88, "#FBE3DA88", TC, 8, 1.4)
        s += T(x + 4, yy + 26, a, 19, DK, "khand") + (T(x + 4, yy + 46, b, 19, DK, "khand") if b else "")
        s += T(x + 4, yy + (64 if b else 46), c, 12.5, GR) + (T(x + 4, yy + 82, d, 12.5, GR) if d else "")
    s += L(198, y + 8, 198, y + 184, LN) + L(18, y + 96, 372, y + 96, LN) + L(18, y + 192, 372, y + 192, LN)
    return s
def brand(title, chips, art, cap, sub, h=700):
    s = R(0, 0, 390, h, "#FFFFFF") + T(18, 40, title[0], 26, DK, "khand") + (T(18, 66, title[1], 26, DK, "khand") if len(title) > 1 else "")
    g, _ = sample_tag(214, 28, "BRAND MOCKUP"); s += g + C(354, 40, 20, "#FFFFFF", LN, 1.2) + L(347, 33, 361, 47, DK, 1.8) + L(361, 33, 347, 47, DK, 1.8) + L(0, 84, 390, 84, LN)
    x = 18
    for c in chips: g, w = pill(x, 98, c, DK, CRM, 12, 12); s += g; x += w + 8
    s += R(18, 136, 354, 470, CRM, "#EADFCF", 14, 1) + art + R(18, 486, 354, 120, "#FFFFFF", "none", 0) + L(18, 486, 372, 486, "#EADFCF")
    s += T(34, 516, cap, 22, DK, "khand")
    for i, l in enumerate(sub): s += T(34, 540 + i * 19, l, 13, "#4A4A4A")
    return s
def vanart(labels="lines", stripe="swoosh"):
    s = van(36, 300, 1.02, stripe, True)
    items = [("Ladder, roof rack", 18, 176, 150, 290), ("Drone", 160, 176, 196, 318), ("Moisture meter", 270, 176, 210, 330), ("Filter stock", 70, 206, 140, 324),
             ("Thermal camera", 230, 206, 190, 332), ("Shop vac", 18, 462, 132, 388), ("Shoe covers bin", 150, 462, 168, 382), ("First-aid kit", 270, 462, 186, 352)]
    if labels == "lines":
        for (lab, lx, ly, px, py) in items:
            s += T(lx, ly, lab, 12, "#262626", w=600) + L(lx + 30, ly + (6 if ly < 300 else -16), px, py, "#7A746A", .8) + C(px, py, 3, "#FFFFFF", DK, 1)
    else:
        for i, (lab, lx, ly, px, py) in enumerate(items):
            s += C(px, py, 8, TC, "#FFFFFF", 1.5) + T(px, py + 4, str(i + 1), 10, "#FFFFFF", w=700, anchor="middle")
        for i, (lab, *_r) in enumerate(items):
            x = 34 + (i % 2) * 170; y = 166 + (i // 2) * 22
            s += C(x + 7, y - 4, 8, TC) + T(x + 7, y, str(i + 1), 10, "#FFFFFF", w=700, anchor="middle") + T(x + 22, y, lab, 12, "#262626", w=600)
    return s
def techart(pose="stand", tags=False):
    if pose == "stand":
        s = person(126, 440, TC, SKIN[0], "sneaker", sc=1.0) + person(268, 440, LG, SKIN[1], "boot", "long", sc=1.0)
    else:
        s = furnace(40, 300, 1.2) + person(150, 440, TC, SKIN[0], "sneaker", hold="filter") + R(300, 216, 60, 224, "#FFFFFF", "#9A948A", 3, 1.4) + C(310, 330, 3, SF) + person(268, 440, LG, SKIN[1], "boot", "long", hold="tablet")
    if tags:
        for x, a, b in ((126 if pose == "stand" else 150, "Good weather", "Sneakers"), (268, "Bad weather", "Boots")):
            g, w = pill(x - 52, 448, a, "#FFFFFF", JG if b == "Sneakers" else LG, 11.5, 10, w=104); s += g
    return s
def trans(kind):
    s = R(0, 0, 390, 560, "#FFFFFF") + T(18, 36, "Moving to the next slide", 20, DK, "khand") + T(18, 58, "Motion sketch, 3 moments", 12.5, GR)
    for i in range(3):
        x = 18 + i * 122; y = 80
        s += R(x, y, 110, 210, "#FFFFFF", "#CFC8BC", 12, 1.2) + T(x + 55, y + 232, ["Tap Next", "Mid-move", "Settled"][i], 12, DK, w=600, anchor="middle")
        def mini(ox, rows, a=1.0):
            g = R(ox + 10, y + 26, 50, 8, DK, "none", 2, 1, f'opacity="{a}"')
            for r in range(rows): g += R(ox + 10, y + 46 + r * 26, 86, 16, "#EFEAE2", "none", 4, 1, f'opacity="{a}"')
            return g
        if i == 0: s += mini(x, 5)
        elif i == 1:
            s += f'<clipPath id="cl{i}{kind}"><rect x="{x}" y="{y}" width="110" height="210" rx="12"/></clipPath><g clip-path="url(#cl{i}{kind})">' + mini(x - 60, 5) + mini(x + 50, 2 if kind == "fade" else 5, .5 if kind == "fade" else 1) + "</g>"
            s += Pth(f"M{x+90} {y+180} L{x+20} {y+180}", stroke=TC, sw=2) + Pth(f"M{x+28} {y+174} L{x+20} {y+180} L{x+28} {y+186}", stroke=TC, sw=2)
        else:
            s += mini(x, 5)
            if kind == "fade": s += "".join(Pth(f"M{x+100} {y+60+r*26} l0 -8 m-4 4 l4 -4 l4 4", stroke=LG, sw=1.4) for r in range(3, 5))
    bar = [("Slide", .7 if kind == "fade" else .4, TC)] + ([("Items rise in", .9, LG)] if kind == "fade" else [])
    y = 360
    s += T(18, y, "Timing", 16, DK, "khand"); y += 14
    for lab, sec, c in bar:
        s += R(18, y, 354 * sec / 1.4, 18, c + "33", "none", 4) + R(18, y, 4, 18, c) + T(30, y + 13, f"{lab} · {sec:.1f}s", 12, DK, w=600) ; y += 26
    s += T(18, y + 18, "Sketch of the motion, not the real slide.", 12, GR)
    return s
def ask(layout="low", val="chip"):
    s, y = pframe(10, "The Ask", ["A Straightforward", "Raise"], 46)
    y = y + (110 if layout == "low" else 6)
    s += R(18, y, 354, 196 if val == "chip" else 176, "#FFF7F3", "#F1D2C5", 16, 1.2, 'filter="url(#sh)"') + L(36, y + 32, 52, y + 32, TC, 1.6) + T(60, y + 37, "INVESTMENT", 12.5, TC, w=600, ls="2.2")
    s += T(34, y + 110, "$200K", 80, TC, "khand") + T(232, y + 108, "for 10%", 30, DK, "khand")
    if val == "chip": s += R(34, y + 138, 130, 40, "#FFFFFF", "#EADFCF", 20, 1) + T(99, y + 163, "$2M valuation", 13.5, DK, w=600, anchor="middle"); y += 212
    else: s += T(34, y + 150, "at a $2M valuation", 16, "#4A4A4A", w=500); y += 192
    s += R(18, y, 354, 160, "#F2F8FA", "#CFE3EA", 16, 1.2) + L(36, y + 32, 52, y + 32, LG, 1.6) + T(60, y + 37, "LINE OF CREDIT", 12.5, LG, w=600, ls="2.2")
    s += T(34, y + 100, "$100K", 62, LG, "khand") + T(196, y + 98, "at 10%", 24, DK, "khand") + C(40, y + 130, 3.5, LG) + T(52, y + 135, "What it's used for", 13.5, LG, w=600) + chev(186, y + 130, LG, 5)
    return SHADOW + s + pfoot("See It Yourself")
def T_PITCH_BRAND():
    pairs, add = maker("p18fb_", PLOC)
    F = "PITCH · FOUNDER SLIDE"
    add("Founder", "Home builds tile", "on the founder tiles should the first tile keep Multi-million-dollar home builds or say High-end custom homes?", F, 510,
        ("mm", "Multi-Million-Dollar Home Builds", "Has managed them, start to finish.", "focused", founder(hi=0), ("Today's tile", "Size of the work is clear")),
        ("hi", "High-End Custom Homes", "Managed them start to finish, plan to keys.", "calm", founder(t1=("High-end custom", "homes", "Managed start to finish,", "plan to keys."), hi=0), ("Quieter, less about money", "Same fact, softer")), y0=240)
    add("Founder", "Agent training tile", "should the agent tile keep AI agent training with Trains the agent teams or say Trains AI agents with The same agents that run the company?", F, 510,
        ("keep", "AI Agent Training", "Trains the agent teams.", "calm", founder(hi=2), ("Today's tile", "Short")),
        ("run", "Trains AI Agents", "The same agents that run the company.", "focused", founder(t3=("Trains AI agents", "", "The same agents that run", "the company."), hi=2), ("Ties to the org chart", "Shows it is in use")), y0=240)
    add("Founder", "Line under the title", "under Built By A Builder should the small caps line keep One operator, field and platform or say Field, finance and platform?", F, 330,
        ("op", "One Operator, Field And Platform", "Today's line under the title.", "calm", founder(), ("Today's line", "Says one person runs it")),
        ("fin", "Field, Finance And Platform", "Names the three strengths instead.", "practical", founder(sub="FIELD, FINANCE AND PLATFORM"), ("Matches the tiles", "Drops one operator")))
    V = "PITCH · OUR BRAND · VANS"
    add("Brand Art", "Van gear labels", "on the van with doors open should the gear be labelled with thin lines out to the names or with numbered dots and a key?", V, 620,
        ("lines", "Thin Lines To Names", "Each item named around the van, like today.", "practical", brand(["Vans, Inside And", "Out"], ["Stocked every Monday", "Same layout every van"], vanart("lines"), "Stocked For The Week", ["Doors open, loaded before Monday."]), ("Today's art", "Read it in place")),
        ("dots", "Numbered Dots And A Key", "Small numbered dots on the gear, a key above.", "calm", brand(["Vans, Inside And", "Out"], ["Stocked every Monday", "Same layout every van"], vanart("dots"), "Stocked For The Week", ["Doors open, loaded before Monday."]), ("Cleaner drawing", "Names in two tidy rows")))
    add("Brand Art", "Van side stripe", "on the Transit van should the side keep the terracotta and blue swoosh or switch to the straight terracotta stripe with the tagline?", V, 620,
        ("swoosh", "Terracotta And Blue Swoosh", "Today's curved stripe under the wordmark.", "lively", brand(["Branded Van"], ["Transit, no maker badge"], van(36, 300, 1.02, "swoosh"), "Branded Van", ["Clean white, terracotta swoosh."]), ("Today's art", "Soft and friendly")),
        ("tag", "Straight Stripe With Tagline", "White Home Maintenance Membership caps on a terracotta band.", "practical", brand(["Branded Van"], ["Transit, no maker badge"], van(36, 300, 1.02, "tagline"), "Branded Van", ["Tagline on the stripe, as picked."]), ("Matches the stripe pick", "Says what we do")))
    U = "PITCH · OUR BRAND · UNIFORM"
    add("Brand Art", "Uniform pose", "should the two illustrated techs stand side by side facing out or be shown at work, one at the furnace and one at the door?", U, 620,
        ("stand", "Standing Side By Side", "Both uniforms head to toe, like today.", "calm", brand(["Technician", "Uniform"], ["Long pants always", "No hi-vis"], techart("stand"), "Two Uniforms, In The Field", ["Terracotta and lagoon polos."]), ("Today's art", "Every piece easy to see")),
        ("work", "At Work", "One swaps a filter, one checks in at the door.", "warm", brand(["Technician", "Uniform"], ["Long pants always", "No hi-vis"], techart("work"), "Two Uniforms, At Work", ["Same uniforms, mid-visit."]), ("Feels real", "Shows the job, not just clothes")))
    add("Brand Art", "Weather tags", "under the two techs should small tags say Good weather, sneakers and Bad weather, boots or should the caption alone explain the footwear?", U, 620,
        ("cap", "Caption Explains It", "No tags; the caption under the art says it.", "calm", brand(["Technician", "Uniform"], ["Long pants always", "No hi-vis"], techart("stand"), "Two Uniforms, In The Field", ["Left: sneakers, good weather.", "Right: boots, bad weather."]), ("Today's art", "Clean picture")),
        ("tags", "Small Weather Tags", "Green Good weather and blue Bad weather tags at their feet.", "practical", brand(["Technician", "Uniform"], ["Long pants always", "No hi-vis"], techart("stand", True), "Two Uniforms, In The Field", ["Shoe covers on both."]), ("Read in one glance", "Caption gets shorter")))
    M = "PITCH · SLIDE MOTION"
    add("Motion", "Slide transitions", "when moving between slides should the pitch keep the slide plus items rising in one by one or a quicker slide with everything already in place?", M, 520,
        ("fade", "Slide Plus Rise-In", "0.7s slide, then items rise in one by one, like today.", "lively", trans("fade"), ("Today's motion", "Feels polished")),
        ("quick", "Quick Slide Only", "0.4s slide, the slide arrives ready to read.", "calm", trans("quick"), ("Snappier on a phone", "Nothing to wait for")))
    A = "PITCH · THE ASK SLIDE"
    add("The Ask", "Ask layout", "should the two Ask cards sit lower with open space under the title like today or move right up under the title?", A, 844,
        ("low", "Cards Lower, Open Space", "White space between the title and the cards.", "calm", ask("low"), ("Today's slide", "Calm, lets it breathe")),
        ("up", "Cards Under The Title", "Cards right under the title, space at the bottom.", "focused", ask("up"), ("Reads top to bottom fast", "Whole Ask above the fold")))
    add("The Ask", "Valuation line", "on the Investment card should the $2M valuation sit in a small white chip or as a plain line of text under $200K for 10%?", A, 680,
        ("chip", "Small White Chip", "$2M valuation in a rounded chip, like today.", "practical", ask("low", "chip"), ("Today's card", "Stands out as a term")),
        ("line", "Plain Line", "at a $2M valuation, in grey under the amount.", "calm", ask("low", "line"), ("Reads like a sentence", "Quieter card")), y0=220)
    return pairs

# ---- member ----
# Member app decks: mockups of the live member home (smart-upkeep member/, 65d11f4) and its reports, record and chat. Sample data only.
MLOC = "Smart Upkeep Member App Mockup"
def ibox(x, y, kind, c=GR, sz=34, bg="#FFFFFF"):
    s = R(x, y, sz, sz, bg, LN, 9, 1); cx, cy = x + sz / 2, y + sz / 2
    if kind == "sink": s += R(cx - 7, cy - 9, 14, 18, "none", c, 2, 1.5) + L(cx - 3, cy - 3, cx + 3, cy - 3, c, 1.5) + C(cx, cy + 4, 2, c)
    elif kind == "heat": s += R(cx - 6, cy - 10, 12, 20, "none", c, 4, 1.5) + C(cx, cy + 3, 2.5, "none", c, 1.4) + L(cx - 3, cy - 5, cx + 3, cy - 5, c, 1.4)
    elif kind == "win": s += R(cx - 9, cy - 9, 18, 18, "none", c, 1, 1.5) + L(cx, cy - 9, cx, cy + 9, c, 1.5) + L(cx - 9, cy, cx + 9, cy, c, 1.5)
    elif kind == "furn": s += R(cx - 7, cy - 10, 14, 20, "none", c, 2, 1.5) + C(cx, cy + 3, 2.6, TC) + L(cx - 4, cy - 5, cx + 4, cy - 5, c, 1.4)
    elif kind == "ac": s += R(cx - 10, cy - 8, 20, 16, "none", c, 2, 1.5) + C(cx, cy, 5, "none", c, 1.4)
    elif kind == "pump": s += R(cx - 5, cy - 10, 10, 20, "none", c, 3, 1.5) + C(cx, cy - 2, 2, c)
    elif kind == "cal": s += R(cx - 9, cy - 8, 18, 17, "none", c, 2, 1.5) + L(cx - 9, cy - 3, cx + 9, cy - 3, c, 1.4)
    elif kind == "roof": s += Pth(f"M{cx-10} {cy} L{cx} {cy-9} L{cx+10} {cy} M{cx-7} {cy-2} V{cy+9} H{cx+7} V{cy-2}", stroke=c, sw=1.5)
    return s
_hp = [0]
def house_photo(x, y, w, h, mode="fade", r=0):
    _hp[0] += 1; k = _hp[0]
    s = f'<defs><linearGradient id="sky{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFD8E6"/><stop offset="1" stop-color="#EEF3F2"/></linearGradient>'
    s += f'<linearGradient id="fd{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset=".55" stop-color="{BG}" stop-opacity=".55"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
    s += f'<clipPath id="hp{k}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath></defs><g clip-path="url(#hp{k})">'
    s += R(x, y, w, h, f"url(#sky{k})") + C(x + w * .62, y + h * .28, 44, "#5E8A4A") + C(x + w * .7, y + h * .22, 36, "#6E9A55")
    hx, hy, hw = x + w * .08, y + h * .36, w * 1.0
    s += Pth(f"M{hx} {hy+40} L{hx+hw*.1} {hy} L{hx+hw*.9} {hy} L{hx+hw} {hy+40} Z", "#7D7A78") + R(hx, hy + 40, hw, h * .7, "#F3EFE8")
    for i in range(5): s += R(hx + 24 + i * hw * .2, hy + 58, 30, 40, "#9DB4C2", "#FFFFFF", 1, 2) + R(hx + 24 + i * hw * .2, hy + 4, 30, 30, "#FFFFFF", "none", 2) + R(hx + 28 + i * hw * .2, hy + 8, 22, 22, "#9DB4C2")
    s += R(x, y + h * .78, w, h * .3, "#DCE3D2")
    if mode == "fade": s += R(x, y, w, h, f"url(#fd{k})")
    return s + "</g>"
def mhead(van_on=True, y=0):
    s = R(0, y, 390, 66, "#FFFFFF") + Pth(f"M22 {y+40} V{y+28} M16 {y+33} L22 {y+27} L28 {y+33} M15 {y+36} V{y+44} H29 V{y+36}", stroke=DK, sw=1.8)
    if van_on:
        s += R(46, y + 18, 70, 32, "#FFFFFF", DK, 4, 2) + Pth(f"M46 {y+30} L38 {y+30} L32 {y+40} L32 {y+50} L46 {y+50}", "#FFFFFF", DK, 2) + R(54, y + 22, 54, 12, "#FFFFFF", "none") + T(81, y + 31, "smartupkeep", 8, DK, "khand", anchor="middle")
        s += C(50, y + 52, 6, "#FFFFFF", DK, 2) + C(102, y + 52, 6, "#FFFFFF", DK, 2)
    s += wm(195, y + 42, 19, "middle") + C(360, y + 34, 18, TC) + T(360, y + 40, "E", 15, "#FFFFFF", w=700, anchor="middle")
    s += L(0, y + 66, 390, y + 66, TC, 2.4, "7 4")
    return s
def bar(active=0, y=780):
    s = R(0, y, 390, 64, "#FFFFFF") + L(0, y, 390, y, LN)
    for i, lab in enumerate(["Home", "Home Record", "Chat", "Menu"]):
        x = 52 + i * 95; c = DK if i == active else "#555"
        s += R(x - 8, y + 12, 16, 16, "none", c, 3, 1.6) + T(x, y + 44, lab, 12, c, w=600 if i == active else 400, anchor="middle")
    return s + C(52, y + 54, 2, TC) + C(244, y + 12, 3.5, TC)
WATCH = [("sink", "Hall bath sink", "Slow drip at the trap. Moisture 18.7%.", "Recheck Dec 8", TC), ("heat", "Water heater base", "Light rust at the drain valve.", "Budget 2027", SF), ("win", "Front window sill", "Caulk cracking at the corner.", "Spring 2027", LG)]
def home(c):
    c = dict(dict(van=True, photo="fade", greet="evening", lines=2, watch="closed", wtag="text", nv="date", plan="ring", chips=4, sample="pill"), **c)
    s = R(0, 0, 390, 1400, BG) + SHADOW
    if c["photo"] == "fade": s += house_photo(0, 66, 390, 300, "fade"); y = 270
    else: s += R(0, 66, 390, 300, BG) + house_photo(18, 84, 354, 190, "card", 16); y = 316
    s += mhead(c["van"])
    if c["sample"] == "pill": s += R(270, 84, 104, 26, "#FFFFFFEE", "#D6D0C6", 13, 1, 'stroke-dasharray="3 2"') + C(286, 97, 3, GR) + T(296, 102, "Sample Data", 12.5, DK, w=500)
    g = {"evening": ("Good Evening, ", "Elena"), "welcome": ("Welcome Home, ", "Elena")}[c["greet"]]
    s += f'<text x="18" y="{y+12}" font-size="40" font-family="Khand" font-weight="700" fill="{DK}">{g[0]}<tspan fill="{TC}">{g[1]}</tspan></text>'
    s += T(18, y + 40, "1208 Sample Birch Lane, Royal Oak, MI 48073", 15, DK); y += 44
    if c["lines"] == 2: s += T(18, y + 26, "15 visits since Apr 2023", 14.5, GR); y += 30
    y += 18
    if c["watch"] == "closed":
        s += R(18, y, 354, 52, "#EEF1EC", "#DCE3D8", 14, 1) + C(38, y + 26, 6, "none", "#3F5A4F", 1.6) + T(54, y + 31, "ITEMS TO WATCH · 3", 12.5, "#3F5A4F", w=600, ls="1.8") + Pth(f"M344 {y+23} l5 5 l5 -5", stroke=DK, sw=1.6); y += 64
    else:
        hh = 52 + 3 * 62
        s += R(18, y, 354, hh, "#EEF1EC", "#DCE3D8", 14, 1) + C(38, y + 26, 6, "none", "#3F5A4F", 1.6) + T(54, y + 31, "ITEMS TO WATCH · 3", 12.5, "#3F5A4F", w=600, ls="1.8") + Pth(f"M344 {y+29} l5 -5 l5 5", stroke=DK, sw=1.6)
        for i, (ic_, a, b, tg, col) in enumerate(WATCH):
            yy = y + 52 + i * 62; s += ibox(30, yy + 6, ic_) + T(76, yy + 22, a, 14.5, DK, w=700) + T(76, yy + 41, b, 12.5, GR)
            if c["wtag"] == "text": s += T(350, yy + 22, tg, 12, GR, anchor="end")
            else: g2, w2 = pill(0, 0, tg, col, col + "1F", 11, 8); s += f'<g transform="translate({350 - w2},{yy + 8})">{g2}</g>'
            s += chev(354, yy + 30, "#999", 5)
        y += hh + 12
    s += R(18, y, 354, 92, "#FFFFFF", LN, 14, 1, 'filter="url(#sh)"')
    if c["nv"] == "date":
        s += R(32, y + 16, 58, 60, BG, "#EADFCF", 10, 1) + T(61, y + 36, "DEC", 12, TC, w=700, anchor="middle", ls="1") + T(61, y + 64, "8", 26, DK, "khand", anchor="middle")
        s += T(104, y + 32, "NEXT VISIT ·", 12.5, GR, w=600, ls="1.6") + T(198, y + 32, "IN 51 DAYS", 12.5, LG, w=700, ls="1.6") + R(18, y + 88, 70, 4, LG, "none", 2)
    else:
        s += C(61, y + 46, 30, "none", "#EEEAE4", 6) + Pth(f"M61 {y+16} A30 30 0 0 1 89 {y+38}", stroke=LG, sw=6) + T(61, y + 52, "51", 22, DK, "khand", anchor="middle") + T(61, y + 66, "days", 9.5, GR, anchor="middle")
        s += T(104, y + 32, "NEXT VISIT · DEC 8", 12.5, GR, w=600, ls="1.6")
    s += T(104, y + 56, "Winter Visit", 17, DK, w=600) + T(104, y + 76, "Tue · 9–11 AM · Tomas R.", 13, GR) + chev(354, y + 46, "#999", 5); y += 106
    s += R(18, y, 354, 232 if c["chips"] == 4 else 196, "#FFFFFF", LN, 14, 1, 'filter="url(#sh)"') + R(18, y, 354, 4, TC, "none", 2)
    s += T(36, y + 34, "YOUR PLAN", 12.5, GR, w=600, ls="1.8") + T(36, y + 72, "Plus", 36, DK, "khand") + T(36, y + 98, "Quarterly Care · renews Apr 14, 2027", 13.5, GR)
    if c["plan"] == "ring":
        s += C(331, y + 52, 28, "none", "#EEEAE4", 6) + Pth(f"M331 {y+24} A28 28 0 1 1 303 {y+52}", stroke=JG, sw=6) + T(331, y + 58, "3/4", 17, DK, w=700, anchor="middle") + T(331, y + 98, "this year", 12, DK, anchor="middle")
    else:
        s += T(354, y + 64, "3 of 4 visits", 13, DK, w=700, anchor="end") + R(36, y + 110, 318, 8, "#EEEAE4", "none", 4) + R(36, y + 110, 238, 8, JG, "none", 4) + T(354, y + 134, "this plan year", 11.5, GR, anchor="end")
    yy = y + 120 + (20 if c["plan"] == "bar" else 0); s += L(36, yy, 354, yy, LN); yy += 14
    chips = [("4 Visits A Year", LG), ("Member Since 2023", TC), ("15 Visits Done", JG), ("3 Extras Used · 1 Active", "#9A948A")][: c["chips"]]
    x = 36; row = 0
    for lab, col in chips:
        w = len(lab) * 6.3 + 28
        if x + w > 360: x = 36; row += 1
        s += R(x, yy + row * 36, w, 28, BG, "#EADFCF", 14, 1) + C(x + 12, yy + row * 36 + 14, 3, col) + T(x + 20, yy + row * 36 + 19, lab, 12, DK, w=500); x += w + 8
    yy += (row + 1) * 36 + 6
    s += T(36, yy + 12, "Plan details", 13, TC, w=600) + chev(124, yy + 8, TC, 4)
    y = yy + 40
    s += T(18, y + 26, "Visit Reports", 24, DK, "khand") + T(352, y + 26, "All 15", 13, TC, w=600, anchor="end")
    if c["sample"] == "foot": s += T(195, y + 80, "Prototype · Sample Data", 12, GR, anchor="middle")
    return s
def T_MEM_HOME():
    pairs, add = maker("m18h_", MLOC)
    TG = "MEMBER APP · HOME"
    def H(**k): return home(k) + bar(0, 780)
    add("Header", "Header van", "in the member home header should the small van drawing stay beside the share icon or should the header show only the wordmark and avatar?", TG, 300,
        ("van", "Keep The Small Van", "Share icon, van drawing, wordmark, avatar, like today.", "warm", H(), ("Today's header", "Friendly, shows who comes")),
        ("plain", "Wordmark And Avatar Only", "Share icon, centred wordmark, avatar; no van.", "calm", H(van=False), ("Cleaner top bar", "Same wordmark-only header idea")))
    add("Greeting", "House photo", "behind the greeting should the house photo stay a soft full-width fade or sit in a rounded card above the greeting?", TG, 480,
        ("fade", "Soft Full-Width Fade", "Photo fills the top and fades into the cream.", "warm", H(), ("Today's home", "Feels like your house")),
        ("card", "Rounded Photo Card", "Photo in a rounded card, greeting under it.", "calm", H(photo="card"), ("Text never sits on the photo", "Easier to read")))
    add("Greeting", "Greeting words", "should the greeting change with the time of day like Good Evening, Elena or always say Welcome Home, Elena?", TG, 480,
        ("time", "Time Of Day", "Good Morning, Afternoon or Evening, then the name.", "warm", H(), ("Today's greeting", "Feels live")),
        ("welcome", "Welcome Home", "Same words every time: Welcome Home, Elena.", "calm", H(greet="welcome"), ("Steady, on brand", "Fits the home idea")), y0=150)
    add("Greeting", "Lines under the name", "under the greeting should both the address and 15 visits since Apr 2023 show or only the address?", TG, 480,
        ("two", "Address And Visit Count", "Two lines, like today.", "practical", H(), ("Today's lines", "Shows the history right away")),
        ("one", "Address Only", "Visit count lives in the plan card chips.", "calm", H(lines=1), ("Says it once", "Cards move up")), y0=150)
    add("Watch List", "Items To Watch start", "when the home opens should Items To Watch start closed with its count or open with the three items showing?", TG, 780,
        ("closed", "Closed With A Count", "One green bar: Items To Watch · 3.", "calm", H(), ("Today's home", "Next visit stays high")),
        ("open", "Open With The Items", "Hall bath sink, water heater base, front window sill showing.", "practical", H(watch="open"), ("Nothing hidden", "Pushes the cards down")), y0=250)
    add("Watch List", "Watch item timing", "inside the open watch list should the timing like Recheck Dec 8 show as plain grey text or as a small coloured chip?", TG, 640,
        ("text", "Plain Grey Text", "Recheck Dec 8, Budget 2027, Spring 2027 in grey.", "calm", H(watch="open"), ("Today's list", "Quiet")),
        ("chip", "Small Coloured Chip", "Terracotta for soon, saffron for budget, blue for later.", "practical", H(watch="open", wtag="chip"), ("Urgency in a glance", "Adds colour")), y0=380)
    add("Next Visit", "Next visit card", "on the Next Visit card should the left side keep the Dec 8 date tile or show a 51 days countdown ring?", TG, 560,
        ("date", "Date Tile", "DEC 8 tile, In 51 Days in blue, like today.", "calm", H(), ("Today's card", "Date first")),
        ("ring", "Countdown Ring", "A ring with 51 days, the date moves up top.", "lively", H(nv="ring"), ("Feels like it is coming", "Date still shown")), y0=380)
    add("Plan Card", "Visits this year", "on the plan card should visits this year show as the 3/4 ring or as a thin progress bar?", TG, 820,
        ("ring", "The 3/4 Ring", "Green ring on the right of the plan name.", "lively", H(), ("Today's card", "Eye-catching")),
        ("bar", "Thin Progress Bar", "3 of 4 visits and a green bar under the plan.", "calm", H(plan="bar"), ("Reads left to right", "Calmer")), y0=470)
    add("Plan Card", "Plan chips", "under the plan should all four chips stay or only 4 Visits A Year and Member Since 2023?", TG, 820,
        ("four", "All Four Chips", "Visits a year, member since, visits done, extras.", "practical", H(), ("Today's card", "Everything at a glance")),
        ("two", "Two Chips", "Visits a year and member since only.", "calm", H(chips=2), ("Less to read", "Details one tap away")), y0=470)
    add("Sample Label", "Sample Data label", "in this prototype should Sample Data sit as a pill on the house photo or only as a small line at the bottom of the home?", TG, 480,
        ("pill", "Pill On The Photo", "Dashed Sample Data pill top right.", "practical", H(), ("Today's home", "Always clear it is sample")),
        ("foot", "Line At The Bottom", "Prototype · Sample Data under the last card.", "calm", H(sample="foot"), ("Photo stays clean", "Still labelled")))
    return pairs
def sheet(title, y=96, back=None):
    s = R(0, 0, 390, 1400, "#B9B4AD") + mhead(False) + R(0, 0, 390, 1400, "#00000030") + R(0, y, 390, 1400, "#FFFFFF", "none", 22) + R(170, y + 10, 50, 5, "#E2DCD2", "none", 2.5)
    if back: s += Pth(f"M28 {y+40} l-5 5 l5 5", stroke=TC, sw=1.8) + T(36, y + 50, back, 13, TC, w=600)
    s += T(24, y + (82 if back else 60), title, 27, DK, "khand") + L(352, y + 40, 366, y + 54, DK, 1.8) + L(366, y + 40, 352, y + 54, DK, 1.8)
    return s, y + (100 if back else 80)
VIS = [("Fall Visit", "Oct 6, 2026 · 8 tasks · 2 findings", TC, True, ["sink", "win"]), ("Summer Visit", "Jul 14, 2026 · 7 tasks · 1 finding", SF, False, ["heat"]),
       ("Spring Visit", "Apr 14, 2026 · 8 tasks · 1 finding", JG, True, ["sink", "furn"]), ("Winter Visit", "Dec 9, 2025 · 7 tasks · 1 finding", LG, False, ["pump"])]
def visits(mode="icons"):
    s, y = sheet("Visit Reports"); s += T(24, y, "Every visit since April 2023. Tap a visit for the full report.", 13, GR); y += 26
    s += T(24, y + 14, "2026", 13, GR, w=700); y += 26
    s += R(18, y, 354, 4 * 70, "#FFFFFF", LN, 14, 1)
    for i, (a, b, col, flag, ics) in enumerate(VIS):
        yy = y + i * 70
        if mode == "photo":
            s += house_photo(30, yy + 11, 64, 48, "card", 8) + T(108, yy + 30, a, 15, DK, w=700) + T(108, yy + 50, b, 12, GR)
            if flag: g, _ = pill(108 + len(a) * 8.2, yy + 14, "Flag", TC, "#FBE3DA", 11, 7); s += g
        else:
            s += C(36, yy + 30, 5, col) + T(52, yy + 34, a, 15, DK, w=700) + T(52, yy + 54, b, 12, GR)
            if flag: g, _ = pill(56 + len(a) * 8.2, yy + 18, "Flag", TC, "#FBE3DA", 11, 7); s += g
            for j, k in enumerate(ics): s += ibox(306 - (len(ics) - 1 - j) * 30 - 6, yy + 18, k, GR, 28, CRM)
        s += chev(354, yy + 35, "#999", 5) + (L(30, yy + 70, 360, yy + 70, LN) if i < 3 else "")
    return s
FIND = [("Hall bath sink: slow drip at the trap", "Moisture 18.7% on the cabinet floor.", "Flagged", TC), ("Front window sill caulk cracking", "Not urgent. Reseal in spring.", "Watch", SF), ("Furnace tune-up", "Burners clean, flame steady.", "Normal", JG)]
def report(top="date", fstyle="chip", photos="grid", y0=0):
    s, y = sheet("Fall Visit Report", back="All Visits")
    if top == "date":
        s += T(24, y + 46, "Oct 6", 50, DK, "khand") + T(150, y + 20, "2026 · Fall Visit", 13.5, DK) + T(150, y + 40, "Tomas R. · 96 min", 13.5, GR); y += 64
    else:
        s += house_photo(18, y, 354, 150, "card", 14) + R(30, y + 112, 160, 28, "#FFFFFFEE", "none", 14) + T(42, y + 131, "Oct 6, 2026 · Tomas R.", 12.5, DK, w=600); y += 164
    s += T(24, y + 16, "Heavy maple drop this year, gutters were full. Two", 14, DK) + T(24, y + 36, "small items to watch, nothing urgent.", 14, DK); y += 56
    s += L(24, y, 366, y, LN) + T(24, y + 32, "Findings", 20, DK, "khand"); y += 46
    for a, b, tg, col in FIND:
        if fstyle == "chip":
            s += T(24, y + 16, a, 14, DK, w=700) + T(24, y + 36, b, 12.5, GR); g, w = pill(0, 0, tg, col if tg != "Normal" else GR, col + "1A", 11, 8); s += f'<g transform="translate({366 - w},{y + 2})">{g}</g>'
        else:
            s += R(24, y, 4, 42, col, "none", 2) + T(38, y + 16, a, 14, DK, w=700) + T(38, y + 36, b, 12.5, GR) + T(366, y + 16, tg.upper(), 10.5, col, w=700, anchor="end", ls="1.2")
        y += 62
    s += T(24, y + 22, "Photos", 20, DK, "khand"); y += 36
    labs = ["Hall bath sink trap", "Front window sill", "Back corner gutter", "Furnace burners"]
    if photos == "grid":
        for i, lab in enumerate(labs):
            x = 24 + (i % 2) * 176; yy = y + (i // 2) * 128
            s += R(x, yy, 166, 118, ["#E8EEF0", "#F1ECE4", "#EAF0EA", "#F6E7E2"][i], "none", 12) + ibox(x + 66, yy + 34, ["sink", "win", "roof", "furn"][i], GR, 34) + R(x + 8, yy + 90, 150, 20, "#FFFFFFDD", "none", 10) + T(x + 18, yy + 104, lab, 11, DK)
    else:
        for i, lab in enumerate(labs[:3]):
            x = 24 + i * 250
            s += R(x, y, 240, 170, ["#E8EEF0", "#F1ECE4", "#EAF0EA"][i], "none", 12) + ibox(x + 100, y + 60, ["sink", "win", "roof"][i], GR, 40) + R(x + 10, y + 136, 220, 24, "#FFFFFFDD", "none", 12) + T(x + 22, y + 152, lab, 12, DK)
        s += "".join(C(176 + i * 12, y + 190, 3.5 if i else 4.5, TC if i == 0 else "#D6D0C6") for i in range(4)) + T(366, y + 194, "1 of 4", 12, GR, anchor="end")
    return s
def moisture(style="list"):
    s, y = sheet("Fall Visit Report", back="All Visits"); y += 10
    s += T(24, y + 20, "Moisture Readings", 20, DK, "khand") + T(366, y + 18, "Dry is under 15%", 12, GR, anchor="end"); y += 40
    rows = [("Hall bath sink cabinet", 18.7), ("Basement, by the sump", 12.4), ("Kitchen sink cabinet", 9.8), ("Laundry, behind washer", 11.2)]
    for lab, v in rows:
        col = TC if v >= 15 else JG
        if style == "list":
            s += T(24, y + 18, lab, 14, DK) + T(366, y + 18, f"{v}%", 15, col, w=700, anchor="end") + L(24, y + 32, 366, y + 32, LN); y += 44
        else:
            s += T(24, y + 16, lab, 14, DK) + T(366, y + 16, f"{v}%", 14, col, w=700, anchor="end")
            for j, (cc, lab2) in enumerate(((JG, "Dry"), (SF, "Watch"), (TC, "Wet"))): s += R(24 + j * 114, y + 26, 112, 8, cc + "55", "none", 3)
            px = 24 + 342 * min(v, 30) / 30; s += Pth(f"M{px-6} {y+20} h12 l-6 7 z", DK); y += 56
    if style == "scale": s += T(24, y + 4, "Dry", 11, JG, w=600) + T(195, y + 4, "Watch", 11, "#8A6510", w=600, anchor="middle") + T(366, y + 4, "Wet", 11, TC, w=600, anchor="end")
    return s
SYS = [("furn", "Gas Furnace", "Installed 2014 · tune-up Oct 6, 2026", "12 yrs", "heat"), ("ac", "Central AC", "Installed 2014 · tune-up Apr 14, 2026", "12 yrs", "heat"),
       ("heat", "Water Heater, 50 gal tank", "Installed 2019 · flushed Apr 14, 2026", "7 yrs", "water"), ("pump", "Sump Pump", "Check valve new Apr 22, 2024", "Valve 2 yrs", "water"),
       ("roof", "Roof and Gutters", "Roof 2016 · gutters cleaned Oct 6, 2026", "10 yrs", "out"), ("cal", "Smoke and CO Detectors (6)", "Tested Oct 6, 2026", "6 on file", "safe")]
def record(mode="list", vr="card"):
    s, y = sheet("Home Record"); s += T(24, y, "The systems in your home, how old they are and when we", 13, GR) + T(24, y + 19, "last looked after them. Built from your visit reports.", 13, GR); y += 40
    if vr == "card":
        s += R(24, y, 342, 76, "#FFFFFF", LN, 16, 1) + ibox(42, y + 20, "cal", DK, 36, CRM) + T(94, y + 34, "Visit Reports", 15.5, DK, w=600) + T(94, y + 54, "15 reports · latest Oct 6, 2026", 12.5, GR) + chev(350, y + 38, "#999", 5); y += 96
    else:
        s += R(24, y, 342, 40, CRM, "none", 20) + R(28, y + 4, 168, 32, "#FFFFFF", "none", 16, 1, 'filter="url(#sh)"') + T(112, y + 25, "Systems", 13.5, DK, w=700, anchor="middle") + T(280, y + 25, "Visit Reports · 15", 13.5, GR, w=600, anchor="middle"); y += 58
    groups = {"heat": "HEATING AND COOLING", "water": "WATER", "out": "OUTSIDE", "safe": "SAFETY"}
    if mode == "list":
        s += T(26, y + 8, "SYSTEMS", 12, GR, w=600, ls="1.8"); y += 20; s += R(24, y, 342, 6 * 70, "#FFFFFF", LN, 16, 1)
        for i, (k, a, b, age, gk) in enumerate(SYS):
            yy = y + i * 70; s += ibox(40, yy + 17, k, DK, 36, CRM) + T(92, yy + 32, a, 15, DK, w=600) + T(92, yy + 52, b, 12, GR) + T(352, yy + 38, age, 13, DK, w=600, anchor="end") + (L(24, yy + 70, 366, yy + 70, LN) if i < 5 else "")
            if k == "heat": g, w = pill(0, 0, "Watch", "#3F5A4F", "#EEF1EC", 11, 8); s += f'<g transform="translate({352 - w},{yy + 44})">{g}</g>'
    else:
        last = None
        for i, (k, a, b, age, gk) in enumerate(SYS):
            if gk != last: s += T(26, y + 18, groups[gk], 12, GR, w=600, ls="1.8"); y += 28; last = gk
            s += R(24, y, 342, 62, "#FFFFFF", LN, 12, 1) + ibox(38, y + 13, k, DK, 36, CRM) + T(88, y + 28, a, 15, DK, w=600) + T(88, y + 47, b, 12, GR) + T(352, y + 35, age, 13, DK, w=600, anchor="end"); y += 70
    return s
def chat(head="title", chips="row", remind="box"):
    s = R(0, 0, 390, 1400, "#B9B4AD") + mhead(False) + R(0, 0, 390, 1400, "#00000030") + R(0, 96, 390, 1400, "#FFFFFF", "none", 22) + R(170, 106, 50, 5, "#E2DCD2", "none", 2.5)
    s += L(352, 136, 366, 150, DK, 1.8) + L(366, 136, 352, 150, DK, 1.8)
    if head == "title": s += T(24, 156, "Chat with Tomas R.", 27, DK, "khand"); y = 178
    else:
        s += C(46, 152, 22, "#E3F0F5") + T(46, 159, "T", 18, LG, w=700, anchor="middle") + C(62, 168, 6, JG, "#FFFFFF", 2) + T(80, 148, "Tomas R.", 19, DK, "khand") + T(80, 168, "Your tech since 2023 · usually replies in an hour", 12, GR); y = 190
    s += L(0, y, 390, y, LN); y += 16
    s += R(24, y, 260, 150, CRM, "none", 14) + R(34, y + 10, 240, 96, "#EFEAE2", "none", 10) + ibox(136, y + 40, "win", DK, 36) + T(34, y + 126, "Also: the front window sill caulk is cracking.", 12.5, DK) + T(34, y + 142, "Not urgent. Best to reseal in spring.", 12.5, DK); y += 160
    s += R(150, y, 216, 56, LG, "none", 14) + T(164, y + 22, "Thanks Tomas. Should I keep anything", 12.5, "#FFFFFF") + T(164, y + 40, "out of that cabinet?", 12.5, "#FFFFFF"); y += 70
    s += R(24, y, 260, 56, CRM, "none", 14) + T(38, y + 22, "Just keep it dry and leave the door", 12.5, DK) + T(38, y + 40, "cracked for a week.", 12.5, DK); y += 74
    s += T(195, y, "Oct 16, 2026", 11.5, GR, anchor="middle"); y += 14
    if remind == "box":
        s += R(60, y, 270, 52, "#FFFFFF", "#D6D0C6", 12, 1, 'stroke-dasharray="3 2"') + T(195, y + 22, "Reminder: Winter Visit Tue Dec 8, 9 to 11 AM.", 12, DK, anchor="middle") + T(195, y + 40, "Reply here if that day does not work.", 12, GR, anchor="middle"); y += 66
    else:
        s += R(40, y, 310, 104, "#FFFFFF", LN, 14, 1, 'filter="url(#sh)"') + R(40, y, 4, 104, LG, "none", 2) + T(58, y + 26, "WINTER VISIT", 11.5, LG, w=700, ls="1.6") + T(58, y + 48, "Tue Dec 8 · 9 to 11 AM · Tomas R.", 14, DK, w=600)
        s += R(58, y + 62, 120, 30, LG, "none", 15) + T(118, y + 82, "Confirm", 13, "#FFFFFF", w=700, anchor="middle") + R(188, y + 62, 140, 30, "#FFFFFF", LG, 15, 1.2) + T(258, y + 82, "Pick another day", 13, LG, w=600, anchor="middle"); y += 118
    if chips == "row":
        x = 24
        for lab in ("Reschedule", "Plan question", "Send a photo", "Extras"):
            g, w = pill(x, y, lab, DK, "#FFFFFF", 12, 13, LN); s += g; x += w + 8
        y += 44; s += R(24, y, 300, 44, "#FFFFFF", "#D6D0C6", 22, 1) + T(44, y + 27, "Message Tomas R.", 13.5, "#9A948A") + C(346, y + 22, 20, DK) + Pth(f"M338 {y+22} h14 m-5 -5 l5 5 l-5 5", stroke="#FFFFFF", sw=2)
    else:
        s += C(44, y + 22, 20, "#FFFFFF", "#D6D0C6", 1.2) + L(36, y + 22, 52, y + 22, DK, 2) + L(44, y + 14, 44, y + 30, DK, 2)
        s += R(72, y, 252, 44, "#FFFFFF", "#D6D0C6", 22, 1) + T(92, y + 27, "Message Tomas R.", 13.5, "#9A948A") + C(346, y + 22, 20, DK) + Pth(f"M338 {y+22} h14 m-5 -5 l5 5 l-5 5", stroke="#FFFFFF", sw=2)
        s += R(24, y - 112, 210, 104, "#FFFFFF", LN, 12, 1, 'filter="url(#sh)"') + "".join(T(42, y - 84 + i * 26, l, 13, DK, w=500) for i, l in enumerate(("Reschedule", "Plan question", "Send a photo", "Extras")))
    return SHADOW + s
def T_MEM_REPORTS():
    pairs, add = maker("m18r_", MLOC)
    V = "MEMBER APP · VISIT REPORTS"
    add("Visit Reports", "Report list rows", "in the Visit Reports list should each row keep the season dot with small system icons or show a small photo from that visit?", V, 560,
        ("icons", "Season Dot And Icons", "Coloured dot, Flag chip, system icons on the right.", "calm", SHADOW + visits("icons"), ("Today's list", "Light and tidy")),
        ("photo", "Small Visit Photo", "A small photo from the visit leads each row.", "warm", SHADOW + visits("photo"), ("Feels personal", "Easier to remember the visit")), y0=60)
    add("Visit Reports", "Report top", "at the top of a visit report should the big Oct 6 date lead or a photo from the visit with the date on it?", V, 600,
        ("date", "Big Date", "Oct 6 in big type, visit and tech beside it.", "calm", SHADOW + report("date"), ("Today's report", "Fast to scan")),
        ("photo", "Visit Photo On Top", "A wide photo, the date on a small white chip.", "warm", SHADOW + report("photo"), ("Shows the home first", "Pushes findings down")), y0=60)
    add("Visit Reports", "Finding status", "for each finding should the status be a small chip on the right or a coloured bar down the left edge?", V, 760,
        ("chip", "Chip On The Right", "Flagged, Watch, Normal as small chips.", "calm", SHADOW + report(), ("Today's report", "Reads like a tag")),
        ("bar", "Coloured Left Bar", "Terracotta, saffron, green bar by each finding.", "practical", SHADOW + report(fstyle="bar"), ("Status at a glance", "Lines up the list")), y0=330)
    add("Visit Reports", "Report photos", "should the photos in a report sit in a two-column grid or a swipe strip with one big photo at a time?", V, 1010,
        ("grid", "Two-Column Grid", "Four photos at once, label on each.", "practical", SHADOW + report(), ("Today's report", "See them all")),
        ("strip", "Swipe Strip", "One big photo, swipe for the next, 1 of 4.", "calm", SHADOW + report(photos="strip"), ("Bigger photos", "Less scrolling")), y0=570)
    add("Visit Reports", "Moisture readings", "in a report should moisture readings show as a plain list of numbers or each on a small Dry, Watch, Wet scale?", V, 440,
        ("list", "Plain List", "Place on the left, the % on the right in colour.", "calm", SHADOW + moisture("list"), ("Simple", "Red only when wet")),
        ("scale", "Dry, Watch, Wet Scale", "Each reading gets a marker on a three-part bar.", "practical", SHADOW + moisture("scale"), ("Easy for anyone to read", "Takes more room")), y0=60)
    R_ = "MEMBER APP · HOME RECORD"
    add("Home Record", "Systems order", "in the Home Record should the systems stay one list or be grouped under Heating and Cooling, Water, Outside and Safety?", R_, 800,
        ("list", "One List", "All systems in one card, like today.", "calm", SHADOW + record("list"), ("Today's record", "Short")),
        ("group", "Grouped By Kind", "Small headings split the systems into four groups.", "practical", SHADOW + record("group"), ("Easier to find a system", "Longer page")), y0=60)
    add("Home Record", "Visit reports link", "in the Home Record should Visit Reports stay a card above the systems or become a second tab beside Systems?", R_, 520,
        ("card", "Card Above Systems", "15 reports, latest Oct 6, 2026, like today.", "calm", SHADOW + record("list", "card"), ("Today's record", "One tap to reports")),
        ("tab", "Second Tab", "Systems and Visit Reports as two tabs.", "practical", SHADOW + record("list", "tab"), ("Clear split", "Systems show sooner")), y0=60)
    C_ = "MEMBER APP · CHAT"
    add("Chat", "Chat header", "at the top of the chat should it keep the plain Chat with Tomas title or show Tomas as a small card with Your tech since 2023?", C_, 420,
        ("title", "Chat With Tomas R.", "A plain title, like today.", "calm", chat("title"), ("Today's chat", "Simple")),
        ("card", "Tomas As A Card", "Initial, online dot, Your tech since 2023.", "warm", chat("card"), ("Feels like a person", "Reply time is Sample")), y0=60)
    add("Chat", "Visit reminder", "for the visit reminder in chat should it stay a dashed note asking to reply or a card with Confirm and Pick another day buttons?", C_, 860,
        ("box", "Dashed Reply Note", "Reply here if that day does not work.", "calm", chat(), ("Today's reminder", "Quiet")),
        ("card", "Card With Buttons", "Confirm or Pick another day in one tap.", "practical", chat(remind="card"), ("Faster answer", "Fewer typed replies")), y0=440)
    add("Chat", "Quick replies", "above the message box should the quick replies stay a row of chips or tuck into a round plus button?", C_, 860,
        ("row", "Row Of Chips", "Reschedule, Plan question, Send a photo, Extras.", "practical", chat(), ("Today's chat", "One tap")),
        ("plus", "Behind A Plus", "A plus button opens the same four replies.", "calm", chat(chips="plus"), ("Cleaner bottom", "One more tap")), y0=440)
    return pairs

# ---- tech ----
# Tech app investor flow decks: mockups of the live tech-week/ demo (upkeep-cc 8431471). Sample route, sample people, sample numbers.
import math
TLOC = "Smart Upkeep Tech App Mockup"
_m = [0]
def thead(timer=None, y=0):
    s = R(0, y, 390, 58, "#FFFFFF") + wm(16, y + 36, 19)
    g, _ = pill(118, y + 15, "Sample Data", "#A8431F", "#FBE3DA", 12.5, 14, "#F1C3B2"); s += g + C(130, y + 30, 3, TC)
    if timer: s += R(268, y + 15, 70, 28, "#E6F2EC", "none", 14) + C(284, y + 29, 4, JG) + T(296, y + 34, timer, 13, JG, w=700)
    return s + C(356, y + 29, 20, LG) + T(356, y + 35, "DR", 14, "#FFFFFF", w=700, anchor="middle") + L(0, y + 58, 390, y + 58, LG, 2.4)
def tbar(active=0, y=780):
    s = R(0, y, 390, 64, "#FFFFFF") + L(0, y, 390, y, LN)
    for i, lab in enumerate(["Today", "Route", "This Week", "Messages"]):
        x = 52 + i * 95; c = LG if i == active else "#555"
        s += R(x - 9, y + 12, 18, 16, "none", c, 3, 1.6) + T(x, y + 44, lab, 12.5, c, w=700 if i == active else 500, anchor="middle")
    return s + R(52 + active * 95 - 26, y, 52, 3, LG)
PINS = [(270, 300), (250, 190), (205, 70), (122, 180), (150, 290), (245, 380)]
def tmap(x, y, w, h, route="dots", hint="chip", sel=None):
    _m[0] += 1; k = _m[0]
    s = f'<clipPath id="tm{k}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/></clipPath><g clip-path="url(#tm{k})">' + R(x, y, w, h, "#EEEBE3")
    for i in range(9): s += L(x + i * w / 8 + 8, y, x + i * w / 8 - 10, y + h, "#FFFFFF", 4 if i % 3 == 0 else 1.6)
    for i in range(9): s += L(x, y + i * h / 8 + 6, x + w, y + i * h / 8 - 4, "#FFFFFF", 4 if i % 3 == 1 else 1.6)
    s += Pth(f"M{x+w*.45} {y} Q{x+w*.6} {y+h*.3} {x+w*.9} {y+h*.25}", stroke="#BFD6DF", sw=3)
    for nm, px, py in (("BIRMINGHAM", .1, .38), ("CLAWSON", .4, .5), ("MADISON HEIGHTS", .55, .6), ("BERKLEY", .3, .66), ("ROYAL OAK", .38, .8)):
        s += T(x + w * px, y + h * py, nm, 11.5, "#8A847A", w=600, ls="1.5")
    sy = h / 440
    P = [(x + px * w / 354, y + py * sy) for px, py in PINS]
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in P)
    if route == "dots": s += Pth(d, stroke=LG, sw=2.4, extra='stroke-dasharray="2 5"')
    else:
        s += Pth(d, stroke=LG, sw=3.2)
        if route == "arrows":
            for (a, b), (c2, d2) in zip(P, P[1:]):
                mx, my = (a + c2) / 2, (b + d2) / 2; ang = math.degrees(math.atan2(d2 - b, c2 - a))
                s += f'<path d="M-5 -5 L3 0 L-5 5" fill="none" stroke="{LG}" stroke-width="2.4" transform="translate({mx:.1f},{my:.1f}) rotate({ang:.0f})"/>'
    s += R(P[0][0] + 26, P[0][1] - 18, 34, 34, DK, "none", 8) + Pth(f"M{P[0][0]+34} {P[0][1]+2} L{P[0][0]+43} {P[0][1]-8} L{P[0][0]+52} {P[0][1]+2} V{P[0][1]+10} H{P[0][0]+34} Z", stroke="#FFFFFF", sw=1.6)
    for i, (a, b) in enumerate(P):
        if hint == "pulse" and i == 0: s += C(a, b, 26, LG + "22") + C(a, b, 34, "none", LG + "55", 2)
        s += C(a, b, 17, TC if sel == i else LG, "#FFFFFF", 3) + T(a, b + 6, str(i + 1), 15, "#FFFFFF", w=700, anchor="middle")
    if hint == "chip": s += R(x + 12, y + 12, 236, 32, "#FFFFFFEE", "none", 16) + T(x + 130, y + 33, "Sample Route · Tap A Number", 13, DK, w=600, anchor="middle")
    s += R(x + w - 220, y + h - 26, 220, 26, "#FFFFFFDD") + T(x + w - 10, y + h - 9, "© OpenStreetMap contributors", 12, DK, anchor="end")
    return s + "</g>" + R(x, y, w, h, "none", "#E1DCD2", 18, 1)
CK = [("Van Stocked", "Ladder, drop cloths, shop vac, shoe", "covers, 9V and AA batteries"), ("Today's Filters And Supplies", "Loaded per stop:", ""),
      ("Tools On Board", "Moisture meter, GFCI tester, CO tester,", "multimeter, vent brush"), ("Uniform And Badge", "Smart Upkeep shirt, ID badge, clean", "boots")]
FIL = ["16×25×1 filter · Gutter scoop and bags", "16×25×1 filter · Vent brush kit", "16×25×1 filter · Fridge filter", "20×25×1 filter · Air compressor", "20×20×1 filter · Squeegee kit", "16×20×1 filter · Door lube kit"]
def today(c):
    c = dict(dict(head="line", route="dots", hint="chip", prog="count", fil="open", start="slide", done=0), **c)
    s = R(0, 0, 390, 1800, "#FFFFFF") + SHADOW + thead()
    s += T(18, 92, "MONDAY · OCT 19 · VAN 2", 13, GR, w=600, ls="1.8") + T(18, 126, "Good Morning, Dana", 33, DK, "khand"); y = 136
    if c["head"] == "line": s += T(18, y + 18, "6 stops · 8:00 AM to 5:20 PM · 7.7h on site", 14.5, "#3D3D3D"); y += 34
    else:
        for i, (v, lab) in enumerate((("6", "Stops"), ("7.7h", "On site"), ("5:20", "Done by"))):
            x = 18 + i * 120; s += R(x, y + 6, 112, 62, CRM, "none", 12) + T(x + 56, y + 36, v, 24, LG if i == 0 else DK, "khand", anchor="middle") + T(x + 56, y + 56, lab, 12, GR, anchor="middle")
        y += 80
    s += tmap(18, y, 354, 446 * .86, c["route"], c["hint"]); y += 446 * .86 + 18
    n = c["done"]; hh = 700 if c["fil"] == "open" else 560
    s += R(18, y, 354, hh, "#FFFFFF", LN, 18, 1, 'filter="url(#sh)"') + T(36, y + 32, "BEFORE YOU ROLL", 12.5, "#A8431F", w=700, ls="1.6") + T(36, y + 58, "Pre-Takeoff Check", 24, DK, "khand")
    if c["prog"] == "count":
        s += T(354, y + 44, f"{n} of 4", 14, DK, w=700, anchor="end") + R(36, y + 78, 318, 7, "#EEEAE4", "none", 3.5) + (R(36, y + 78, 318 * n / 4, 7, JG, "none", 3.5) if n else "")
    else:
        s += "".join(R(36 + i * 81, y + 78, 75, 7, JG if i < n else "#EEEAE4", "none", 3.5) for i in range(4)) + T(354, y + 44, "4 steps", 12.5, GR, anchor="end")
    y += 100
    for i, (a, b, b2) in enumerate(CK):
        ok = i < n
        s += C(54, y + 22, 15, JG if ok else "#FFFFFF", JG if ok else "#CFC8BC", 2) + (Pth(f"M47 {y+22} l5 5 l9 -10", stroke="#FFFFFF", sw=2.4) if ok else "")
        s += T(84, y + 22, a, 16, DK, w=700) + T(84, y + 44, b, 13, GR) + (T(84, y + 62, b2, 13, GR) if b2 else "") + R(334, y + 10, 20, 16, "none", LG, 3, 1.6)
        y += 52 + (18 if b2 else 0)
        if i == 1:
            if c["fil"] == "open":
                for j, f in enumerate(FIL): s += T(84, y + j * 22, f"#{j+1}", 13, LG, w=700) + T(110, y + j * 22, f, 12.5, DK)
                y += 6 * 22 + 6
            else:
                s += R(84, y - 10, 270, 34, CRM, "none", 10) + T(98, y + 12, "6 stops · 6 filters · 6 supply kits", 12.5, DK, w=600) + T(340, y + 12, "See all", 12.5, LG, w=700, anchor="end"); y += 36
        s += L(36, y, 354, y, "#EFEAE2"); y += 12
    y += 8
    if c["start"] == "slide":
        s += R(36, y, 318, 58, "#E6F2EC", "#BFDCCB", 29, 1) + C(66, y + 29, 24, JG) + Pth(f"M58 {y+21} l8 8 l-8 8 M66 {y+21} l8 8 l-8 8", stroke="#FFFFFF", sw=2.4) + T(206, y + 35, "Start Your Day", 17, JG, w=700, anchor="middle")
        s += T(195, y + 84, "Slide to clock in and head to Stop 1.", 13, GR, anchor="middle")
    else:
        s += R(36, y, 318, 58, JG, "none", 29) + C(195, y + 29, 22, "none", "#FFFFFF66", 3) + Pth(f"M195 {y+7} A22 22 0 0 1 217 {y+29}", stroke="#FFFFFF", sw=3) + T(195, y + 35, "Hold", 13, "#FFFFFF", w=700, anchor="middle")
        s += T(195, y + 84, "Press and hold to clock in and head to Stop 1.", 13, GR, anchor="middle")
    return s
def popup(style="card"):
    s = today({})
    if style == "card":
        y = 340; s += R(30, y, 330, 130, "#FFFFFF", "none", 16, 1, 'filter="url(#sh)"') + C(60, y + 46, 17, TC, "#FFFFFF", 3) + T(60, y + 52, "1", 15, "#FFFFFF", w=700, anchor="middle")
        s += T(88, y + 32, "#1 · Essentials", 15, DK, w=700) + T(88, y + 52, "Membership + Gutter Clean", 13.5, DK, w=600) + T(88, y + 72, "8:00 AM · 65 Min · 450 Sparrowgate Dr", 12, GR) + T(88, y + 110, "Tap For Full Stop Details", 12.5, LG, w=700)
        s += C(326, y + 52, 13, LG) + chev(323, y + 52, "#FFFFFF", 4)
    else:
        s += R(0, 0, 390, 1800, "#00000040") + R(0, 420, 390, 1400, "#FFFFFF", "none", 22) + R(170, 430, 50, 5, "#E2DCD2", "none", 2.5)
        s += C(46, 478, 24, TC) + T(46, 486, "1", 20, "#FFFFFF", w=700, anchor="middle") + T(84, 468, "STOP 1 OF 6 · 8:00 AM", 13, TC, w=700, ls="1.4") + T(84, 496, "Avery Cindervale", 26, DK, "khand")
        s += T(22, 528, "450 Sparrowgate Dr, Royal Oak", 15, "#3D3D3D") + T(22, 560, "Essentials + Gutter Clean · 65 Min", 13.5, DK, w=600)
        s += R(22, 584, 166, 46, "#FFFFFF", LG, 12, 1.8) + T(105, 612, "Full Details", 14, LG, w=700, anchor="middle") + R(200, 584, 166, 46, LG, "none", 12) + T(283, 612, "Navigate", 14, "#FFFFFF", w=700, anchor="middle")
    return s
def navig(style="dark"):
    s = R(0, 0, 390, 900, "#FFFFFF") + thead("0:06") + tmap(0, 58, 390, 470, "solid", "none")
    s += R(240, 300, 40, 26, "#FFFFFF", LG, 8, 2.4) + C(250, 328, 4, LG) + C(270, 328, 4, LG)
    if style == "dark":
        s += R(14, 72, 362, 76, LG, "none", 16, 1, 'filter="url(#sh)"') + R(28, 86, 48, 48, "#FFFFFF22", "none", 10) + Pth("M44 124 V104 H62 M56 98 l6 6 l-6 6", stroke="#FFFFFF", sw=2.6)
        s += T(88, 108, "Turn Right Onto East 11 Mile Road", 15, "#FFFFFF", w=700) + T(88, 130, "160 m", 13, "#FFFFFFCC")
    else:
        s += R(14, 72, 362, 76, "#FFFFFF", LN, 16, 1, 'filter="url(#sh)"') + R(28, 86, 48, 48, "#E3F0F5", "none", 10) + Pth("M44 124 V104 H62 M56 98 l6 6 l-6 6", stroke=LG, sw=2.6)
        s += T(88, 108, "Turn Right Onto East 11 Mile Road", 15, DK, w=700) + T(88, 130, "160 m", 13, GR)
    s += R(18, 546, 354, 210, "#FFFFFF", LN, 16, 1) + T(36, 578, "HEADING TO STOP 1", 12.5, LG, w=700, ls="1.6") + T(36, 608, "Avery Cindervale", 24, DK, "khand") + T(36, 630, "450 Sparrowgate Dr, Royal Oak", 13.5, GR)
    for i, (v, lab) in enumerate((("7:51 AM", "Arrive"), ("6 Min", "Drive"), ("1.3 Mi", "To Go"))):
        x = 36 + i * 108; s += R(x, 648, 100, 60, CRM, "none", 10) + T(x + 50, 676, v, 17, DK, "khand", anchor="middle") + T(x + 50, 696, lab, 12, GR, anchor="middle")
    return SHADOW + s
def onsite(where="head"):
    s = R(0, 0, 390, 900, "#FFFFFF") + thead("0:15" if where == "head" else None) + tmap(18, 74, 354, 150, "solid", "none")
    s += R(18, 238, 354, 40, "#E6F2EC", "none", 12) + Pth("M36 258 l5 5 l9 -10", stroke=JG, sw=2.4) + T(58, 263, "Arrived 7:51 AM · Stop 1 of 6", 14, JG, w=700)
    y = 294; s += R(18, y, 354, 420, "#FFFFFF", LN, 16, 1, 'filter="url(#sh)"') + T(36, y + 30, "ON SITE · STOP 1 OF 6", 12.5, TC, w=700, ls="1.6") + T(36, y + 60, "Avery Cindervale", 26, DK, "khand")
    if where == "card": s += T(354, y + 46, "0:15", 30, DK, "khand", anchor="end") + T(354, y + 64, "On Site", 12, GR, anchor="end")
    g, w1 = pill(36, y + 76, "Essentials", LG, "#E3F0F5", 12, 12); s += g; g, _ = pill(44 + w1, y + 76, "+ Gutter Clean", TC, "#FFFFFF", 12, 12, "#E9B8A6", dash=True); s += g
    s += L(36, y + 120, 354, y + 120, LN) + T(36, y + 146, "STEP 1 OF 6", 12.5, GR, w=600, ls="1.6") + R(36, y + 160, 44, 44, CRM, "none", 10) + T(92, y + 190, "Check In", 22, DK, "khand")
    s += T(36, y + 228, "Say hi, shoe covers on, and a quick walk-around.", 13.5, "#3D3D3D") + R(36, y + 244, 318, 56, CRM, "none", 10) + T(48, y + 266, "Member Note: Two small dogs. Ring and wait.", 12.5, DK, w=600) + T(48, y + 286, "Last Visit: Jul 9, 2026 · Attic vent partly blocked.", 12.5, GR)
    for i, lab in enumerate(("Greet the member at the door", "Shoe covers on")):
        s += C(50, y + 326 + i * 40, 12, JG) + Pth(f"M44 {y+326+i*40} l4 4 l7 -8", stroke="#FFFFFF", sw=2.2) + T(72, y + 331 + i * 40, lab, 14, DK, w=600)
    return SHADOW + s + tbar(0)
def week(banner=True):
    s = R(0, 0, 390, 900, "#FFFFFF") + thead("0:21") + T(18, 92, "OCT 19 TO OCT 23", 13, GR, w=600, ls="1.8") + T(18, 126, "This Week", 33, DK, "khand"); y = 142
    if banner:
        s += R(18, y, 354, 70, "#FFF4EF", "#F1D2C5", 14, 1) + T(36, y + 46, "28", 38, TC, "khand") + T(84, y + 30, "Visits This Week · Sample", 14, DK, w=700)
        g, w1 = pill(84, y + 40, "15 Essentials", LG, "#E3F0F5", 11, 8); s += g; g, w2 = pill(90 + w1, y + 40, "8 Plus", JG, "#E6F2EC", 11, 8); s += g; g, _ = pill(96 + w1 + w2, y + 40, "5 Complete", TC, "#FBE3DA", 11, 8); s += g; y += 86
    for i, (d, n, cnt) in enumerate((("Mon", "19", 6), ("Tue", "20", 5), ("Wed", "21", 6), ("Thu", "22", 5), ("Fri", "23", 6))):
        x = 18 + i * 72; on = i == 0
        s += R(x, y, 64, 74, LG if on else "#FFFFFF", "none" if on else LN, 12, 1) + T(x + 32, y + 22, d, 13, "#FFFFFF" if on else GR, w=600, anchor="middle") + T(x + 32, y + 46, n, 20, "#FFFFFF" if on else DK, "khand", anchor="middle") + T(x + 32, y + 64, f"{cnt}", 12.5, "#FFFFFF" if on else TC, w=700, anchor="middle")
    y += 92
    s += T(18, y + 18, "Monday, Oct 19", 20, DK, "khand") + T(372, y + 16, "6 Stops · Tap For Report", 12, GR, anchor="end"); y += 34
    for nm, ad, tm, plan, col in (("Avery Cindervale", "450 Sparrowgate Dr, Royal Oak", "8:00 AM", "Essentials", LG), ("Zion Valecrest", "610 Fernhollow Dr, Clawson", "9:30 AM", "Plus", JG), ("Gray Northwick", "490 Puddleby Ln, Troy", "11:15 AM", "Complete", TC)):
        s += R(18, y, 354, 80, "#FFFFFF", LN, 14, 1) + T(34, y + 28, nm, 15.5, DK, w=700) + T(34, y + 48, ad, 12.5, GR) + T(330, y + 34, tm, 15, DK, w=700, anchor="end") + chev(350, y + 30, LG, 5)
        g, _ = pill(34, y + 54, plan, col, col + "1A", 11, 8); s += g; y += 90
    return SHADOW + s + tbar(2)
def T_TECH_TODAY():
    pairs, add = maker("t18t_", TLOC)
    TG = "TECH APP · TODAY"
    def D(**k): return today(k)
    add("Today Header", "Day summary", "under Good Morning, Dana should the day summary stay one line of text or become three small tiles for stops, hours and finish time?", TG, 320,
        ("line", "One Line Of Text", "6 stops · 8:00 AM to 5:20 PM · 7.7h on site.", "calm", D(), ("Today's screen", "Map shows sooner")),
        ("tiles", "Three Small Tiles", "6 Stops, 7.7h On Site, Done by 5:20, Sample.", "practical", D(head="tiles"), ("Numbers pop", "Map moves down a little")))
    add("Map", "Route line", "on the Today map should the route between stops stay a dotted line or a solid line with small arrows showing the order?", TG, 560,
        ("dots", "Dotted Line", "Light dotted blue between the numbered pins.", "calm", D(), ("Today's map", "Map stays light")),
        ("arrows", "Solid Line With Arrows", "A solid blue line, arrows point stop to stop.", "practical", D(route="arrows"), ("Order is obvious", "Busier map")), y0=160)
    add("Map", "Tap hint", "to show investors the pins can be tapped should the map keep the Sample Route · Tap A Number chip or pulse a ring around stop 1?", TG, 560,
        ("chip", "Tap A Number Chip", "A white chip in the map corner, like today.", "practical", D(), ("Today's map", "Says it in words")),
        ("pulse", "Pulse On Stop 1", "A soft blue ring pulses around pin 1, no chip.", "lively", D(hint="pulse"), ("Cleaner map", "Shows where to tap")), y0=160)
    add("Pre-Takeoff", "Check progress", "on the Pre-Takeoff Check should progress show as 0 of 4 with one thin bar or as four short segments that fill in?", TG, 760,
        ("count", "0 Of 4 And One Bar", "Count on the right, one green bar under it.", "calm", D(done=1), ("Today's check", "Reads as a number")),
        ("seg", "Four Segments", "One segment per check fills green.", "practical", D(done=1, prog="seg"), ("Each check is a step", "No number to read")), y0=520)
    add("Pre-Takeoff", "Filters per stop", "inside Today's Filters And Supplies should the six stop lines show open like today or fold into one summary line with See all?", TG, 900,
        ("open", "All Six Lines Open", "#1 to #6 with filter size and supplies.", "practical", D(), ("Today's check", "Nothing to tap")),
        ("fold", "One Summary Line", "6 stops · 6 filters · 6 supply kits, See all.", "calm", D(fil="fold"), ("Shorter check", "Start Your Day sits higher")), y0=520)
    add("Pre-Takeoff", "Start Your Day control", "to clock in should Start Your Day stay a slider you drag or become a button you press and hold?", TG, 1260,
        ("slide", "Slide To Start", "Drag the green knob across, like today.", "lively", D(done=4), ("Today's control", "Hard to hit by mistake")),
        ("hold", "Press And Hold", "Hold the green button while a ring fills.", "calm", D(done=4, start="hold"), ("Works with gloves", "Same safety, less travel")), y0=920)
    add("Map", "Pin tap opens", "when a pin is tapped should it open a small card over the map or a bottom sheet with Full Details and Navigate?", TG, 760,
        ("card", "Small Card Over The Map", "#1 Essentials card with Tap For Full Stop Details.", "calm", popup("card"), ("Today's pin card", "Map stays in view")),
        ("sheet", "Bottom Sheet", "Stop 1 slides up with Full Details and Navigate.", "practical", popup("sheet"), ("Buttons right there", "Covers the list")), y0=160)
    add("Driving", "Turn banner", "while driving to a stop should the turn banner stay dark blue with white words or turn white with blue arrows?", TG, 760,
        ("dark", "Dark Blue Banner", "White words on lagoon blue, like today.", "focused", navig("dark"), ("Today's banner", "Stands out on the map")),
        ("white", "White Banner", "Ink words on white, blue arrow tile.", "calm", navig("white"), ("Lighter look", "Matches the cards")))
    add("On Site", "On-site timer", "once arrived should the on-site timer sit in the small green pill in the header or big inside the stop card?", TG, 720,
        ("head", "Green Pill In The Header", "0:15 beside the avatar, like today.", "calm", onsite("head"), ("Today's screen", "Always in view")),
        ("card", "Big In The Stop Card", "0:15 On Site at the top right of the card.", "focused", onsite("card"), ("Easy to read on the go", "Header stays quiet")))
    add("This Week", "Week banner", "on This Week should the 28 visits banner with plan chips stay above the day strip or should the week start with the day strip?", TG, 740,
        ("banner", "Keep The Banner", "28 visits this week, Sample, with plan chips.", "practical", week(True), ("Today's screen", "Week at a glance")),
        ("strip", "Start With Days", "The Mon to Fri strip leads, visits under it.", "calm", week(False), ("More visits on screen", "Counts live on the day tiles")))
    return pairs
STOPS = [("Avery Cindervale", "450 Sparrowgate Dr, Royal Oak", "8:00 AM", "Essentials", "+ Gutter Clean", LG), ("Zion Valecrest", "610 Fernhollow Dr, Clawson", "9:30 AM", "Plus", "+ Dryer Vent Clean", JG),
         ("Gray Northwick", "490 Puddleby Ln, Troy", "11:15 AM", "Complete", "5 Tasks", TC), ("Morgan Bramblecote", "260 Honeycomb Way, Birmingham", "1:00 PM", "Plus", "+ Sprinkler Blowout", JG),
         ("Reese Silverbirch", "870 Paperkite Dr, Berkley", "2:30 PM", "Essentials", "+ Window Wash", LG)]
def route(cur="outline", chip="chip", mapbtn="button"):
    s = R(0, 0, 390, 900, "#FFFFFF") + thead("0:20") + T(18, 92, "MONDAY · OCT 19 · VAN 2", 13, GR, w=600, ls="1.8") + T(18, 126, "Today's Route", 33, DK, "khand") + T(18, 150, "On Site At Stop 1", 14, GR)
    if mapbtn == "button": s += R(18, 166, 172, 44, "#FFFFFF", "#D6D0C6", 22, 1.2) + R(36, 180, 20, 14, "none", LG, 3, 1.6) + T(66, 194, "View On Map", 14.5, DK, w=600)
    else: s += R(18, 166, 220, 44, CRM, "none", 22) + R(22, 170, 106, 36, LG, "none", 18) + T(75, 193, "List", 14, "#FFFFFF", w=700, anchor="middle") + T(182, 193, "Map", 14, DK, w=600, anchor="middle")
    s += T(18, 250, "6 Stops", 22, DK, "khand") + T(372, 248, "8:00 AM to 5:20 PM", 13, "#3D3D3D", w=600, anchor="end"); y = 266
    for i, (nm, ad, tm, plan, ex, col) in enumerate(STOPS):
        hh = 108 if i in (0, 3) else 98; on = i == 0
        if on and cur == "outline": s += R(18, y, 354, hh, "#FFFFFF", TC, 14, 1.6) + R(18, y, 6, hh, TC, "none", 3)
        elif on: s += R(18, y, 354, hh, "#FFF4EF", "none", 14)
        else: s += R(18, y, 354, hh, "#FFFFFF", LN, 14, 1)
        s += C(54, y + hh / 2, 17, TC if on else "#E3F0F5") + T(54, y + hh / 2 + 6, str(i + 1), 15, "#FFFFFF" if on else LG, w=700, anchor="middle")
        s += T(86, y + 28, nm, 16, DK, w=600) + T(86, y + 50, ad, 13, GR) + T(318, y + hh / 2 + 6, tm, 15, DK, "khand", anchor="end") + C(350, y + hh / 2, 14, "#E3F0F5") + chev(347, y + hh / 2, LG, 4)
        if chip == "chip":
            g, w = pill(86, y + 62, plan, col, col + "1A", 12, 11); s += g + T(94 + w, y + 79, ex, 13, "#3D3D3D")
        else: s += C(92, y + 74, 5, col) + T(104, y + 79, f"{plan} {ex}", 13, "#3D3D3D")
        y += hh + 10
    return SHADOW + s + tbar(1)
TASKS = [("HVAC Filter Swap", "10 min"), ("Smoke And CO Detector Test", "10 min"), ("GFCI Outlet Test", "10 min"), ("Gutter Clean", "20 min")]
def job(head="num", tasks="each", extra="dash", notes="box", alert=False, btns="msg"):
    s = R(0, 0, 390, 1100, "#FFFFFF") + thead() + R(0, 0, 390, 1100, "#00000038") + R(0, 120, 390, 1100, "#FFFFFF", "none", 22) + R(170, 130, 50, 5, "#E2DCD2", "none", 2.5) + L(352, 150, 364, 162, DK, 1.8) + L(364, 150, 352, 162, DK, 1.8)
    y = 150
    if head == "num":
        s += C(46, y + 32, 26, TC) + T(46, y + 41, "1", 22, "#FFFFFF", w=700, anchor="middle") + T(88, y + 22, "STOP 1 OF 6 · 8:00 AM", 13, TC, w=700, ls="1.4") + T(88, y + 52, "Avery Cindervale", 28, DK, "khand"); y += 70
    else:
        s += T(22, y + 40, "8:00 AM", 40, DK, "khand") + T(170, y + 24, "STOP 1 OF 6", 13, TC, w=700, ls="1.4") + T(170, y + 44, "Avery Cindervale", 20, DK, "khand"); y += 66
    s += T(22, y + 16, "450 Sparrowgate Dr, Royal Oak", 15, "#3D3D3D"); y += 32
    if alert: s += R(22, y, 346, 34, "#FFF3CC", "#EBCF7A", 10, 1) + C(40, y + 17, 8, SF) + T(40, y + 21, "!", 12, "#FFFFFF", w=700, anchor="middle") + T(56, y + 22, "Two small dogs · ring and wait", 13.5, "#6A4D08", w=700); y += 46
    g, w1 = pill(22, y, "Essentials", LG, "#E3F0F5", 12.5, 12); s += g
    g, w2 = pill(30 + w1, y, "+ Gutter Clean", TC, "#FFFFFF", 12.5, 12, "#E9B8A6", dash=True); s += g; y += 36
    g, w3 = pill(22, y, "Seasonal Check-In · 65 Min", "#555", "#EFEAE2", 12.5, 12); s += g; g, _ = pill(30 + w3, y, "Watch: Attic", "#7A5A0E", "#FFF3CC", 12.5, 12); s += g; y += 50
    s += T(22, y + 14, "What's Involved", 19, DK, "khand") + T(368, y + 12, "4 Tasks" if tasks == "each" else "4 Tasks · 50 min", 13, "#3D3D3D", w=600, anchor="end"); y += 30
    for i, (tk, mn) in enumerate(TASKS):
        s += R(22, y + 6, 18, 20, "none", LG if i < 3 else TC, 3, 1.6) + T(52, y + 22, tk, 15, DK)
        if i == 3:
            if extra == "dash": g, _ = pill(52 + len(tk) * 7.6, y + 4, "Extra", TC, "#FFFFFF", 11.5, 10, "#E9B8A6", dash=True)
            else: g, _ = pill(52 + len(tk) * 7.6, y + 4, "Extra", "#FFFFFF", SF, 11.5, 10)
            s += g
        if tasks == "each": s += T(368, y + 22, mn, 13, "#3D3D3D", anchor="end")
        s += L(22, y + 36, 368, y + 36, LN) if i < 3 else ""; y += 38
    y += 12
    if notes == "box":
        s += T(22, y + 14, "Bring In", 19, DK, "khand") + R(22, y + 26, 346, 56, CRM, "none", 10) + T(34, y + 48, "16×25×1 filter · MERV 11 · Gutter scoop and bags · shoe", 13, "#3D3D3D") + T(34, y + 68, "covers", 13, "#3D3D3D"); y += 96
        s += T(22, y + 14, "Access", 19, DK, "khand") + R(22, y + 26, 346, 38, CRM, "none", 10) + T(34, y + 50, "Two small dogs. Ring and wait.", 13, "#3D3D3D"); y += 78
    else:
        for icn, lab, txt in (("box", "Bring In", "16×25×1 filter · MERV 11 · gutter scoop, bags"), ("key", "Access", "Ring and wait · two small dogs")):
            s += R(22, y, 40, 40, "#E3F0F5", "none", 10) + (R(32, y + 12, 20, 16, "none", LG, 2, 1.6) if icn == "box" else C(36, y + 20, 5, "none", LG, 1.6) + L(41, y + 20, 52, y + 20, LG, 1.6))
            s += T(74, y + 16, lab.upper(), 11.5, LG, w=700, ls="1.4") + T(74, y + 34, txt, 13.5, DK, w=500) + L(22, y + 50, 368, y + 50, LN); y += 60
        y += 10
    if btns == "msg":
        s += R(22, y, 168, 54, "#FFFFFF", LG, 14, 2) + R(64, y + 18, 14, 18, "none", LG, 2, 1.6) + T(124, y + 33, "Report", 16, LG, w=600, anchor="middle")
        s += R(200, y, 168, 54, LG, "none", 14) + T(290, y + 33, "Message", 16, "#FFFFFF", w=600, anchor="middle")
    else:
        s += R(22, y, 346, 54, LG, "none", 14) + T(195, y + 33, "Navigate To Stop 1", 16, "#FFFFFF", w=700, anchor="middle"); y += 64
        s += R(22, y, 168, 42, "#FFFFFF", "#D6D0C6", 12, 1.2) + T(106, y + 27, "Report", 14, DK, w=600, anchor="middle") + R(200, y, 168, 42, "#FFFFFF", "#D6D0C6", 12, 1.2) + T(284, y + 27, "Message", 14, DK, w=600, anchor="middle")
    return SHADOW + s
def step(cond="seg"):
    s = R(0, 0, 390, 900, "#FFFFFF") + thead("0:15") + T(18, 92, "STEP 2 OF 5", 13, GR, w=600, ls="1.8") + "".join(R(18 + i * 72, 104, 66, 5, JG if i < 1 else (TC if i == 1 else "#EEEAE4"), "none", 2.5) for i in range(5))
    s += T(18, 146, "HVAC Filter Swap", 30, DK, "khand") + T(18, 172, "Swap the furnace filter and note what came out.", 14, "#3D3D3D")
    s += R(18, 188, 354, 58, CRM, "none", 10) + T(30, 210, "Filter On File: 16×25×1 · MERV 11 · From Van Bin 3", 12.5, DK, w=600) + T(30, 230, "Furnace: Gas, 2011", 12.5, GR); y = 262
    s += C(32, y + 14, 12, JG) + Pth(f"M26 {y+14} l4 4 l7 -8", stroke="#FFFFFF", sw=2.2) + T(54, y + 19, "Furnace switch off", 15, DK, w=600); y += 44
    s += C(32, y + 14, 12, JG) + Pth(f"M26 {y+14} l4 4 l7 -8", stroke="#FFFFFF", sw=2.2) + T(54, y + 19, "Old filter out: condition", 15, DK, w=600); y += 34
    if cond == "seg":
        for i, lab in enumerate(("Light", "Dirty", "Very Dirty")):
            x = 54 + i * 100; on = i == 1
            s += R(x, y, 92, 38, DK if on else "#FFFFFF", "none" if on else "#D6D0C6", 19, 1.2) + T(x + 46, y + 25, lab, 14, "#FFFFFF" if on else DK, w=600, anchor="middle")
        y += 54
    else:
        for i, (lab, shade) in enumerate((("Light", "#F4F1EA"), ("Dirty", "#C9BFAE"), ("Very Dirty", "#8E846F"))):
            x = 54 + i * 106; on = i == 1
            s += R(x, y, 98, 104, "#FFFFFF", TC if on else "#D6D0C6", 12, 2 if on else 1.2) + R(x + 19, y + 12, 60, 50, shade, "#9A948A", 2, 1)
            s += "".join(L(x + 19 + k * 10, y + 12, x + 19 + k * 10, y + 62, "#00000022", 1) for k in range(1, 6)) + T(x + 49, y + 86, lab, 13.5, TC if on else DK, w=700 if on else 500, anchor="middle")
        y += 120
    s += C(32, y + 14, 12, "#FFFFFF", "#CFC8BC", 2) + T(54, y + 19, "New filter in, airflow arrow toward the furnace", 15, DK, w=600); y += 44
    s += C(32, y + 14, 12, "#FFFFFF", "#CFC8BC", 2) + T(54, y + 19, "Date on the frame, switch back on", 15, DK, w=600); y += 54
    s += R(18, y, 354, 52, "#EFEAE2", "none", 12) + T(195, y + 32, "Next Step", 16, "#9A948A", w=600, anchor="middle")
    return SHADOW + s + tbar(0)
def T_TECH_ROUTE():
    pairs, add = maker("t18r_", TLOC)
    RT = "TECH APP · ROUTE"
    add("Route", "Current stop", "in Today's Route should the stop you are at keep the terracotta outline with a side bar or get a soft filled background instead?", RT, 520,
        ("outline", "Outline And Side Bar", "Terracotta border, thick bar on the left.", "focused", route(), ("Today's route", "Very clear")),
        ("fill", "Soft Filled Card", "Pale terracotta fill, no border.", "calm", route(cur="fill"), ("Softer", "Still stands out")), y0=150)
    add("Route", "Plan on each stop", "on each route row should the plan show as a coloured chip with the extra beside it or as a small dot with plain text?", RT, 620,
        ("chip", "Coloured Plan Chip", "Essentials chip, then + Gutter Clean.", "practical", route(), ("Today's rows", "Plan reads first")),
        ("dot", "Dot And Plain Text", "Blue dot, Essentials + Gutter Clean in one line.", "calm", route(chip="dot"), ("Quieter rows", "More fits")), y0=240)
    add("Route", "List or map control", "at the top of Today's Route should View On Map stay one button or become a List and Map switch?", RT, 380,
        ("button", "View On Map Button", "One outline button, like today.", "calm", route(), ("Today's route", "Simple")),
        ("toggle", "List And Map Switch", "Two-part switch, List picked.", "practical", route(mapbtn="toggle"), ("Shows both views exist", "One tap back")))
    JB = "TECH APP · JOB CARD"
    add("Job Card", "Job card top", "when a stop opens should the top lead with the big stop number and name or with the big arrival time?", JB, 520,
        ("num", "Stop Number And Name", "Terracotta 1, Stop 1 of 6 · 8:00 AM, name.", "focused", job(), ("Today's job card", "Who comes first")),
        ("time", "Big Arrival Time", "8:00 AM big, stop and name beside it.", "practical", job(head="time"), ("When comes first", "Good for a tight day")), y0=110)
    add("Job Card", "Task minutes", "in What's Involved should every task show its minutes or only the total in the heading?", JB, 640,
        ("each", "Minutes On Each Task", "10, 10, 10 and 20 min down the right.", "practical", job(), ("Today's card", "Plan each task")),
        ("total", "Total Only", "4 Tasks · 50 min in the heading.", "calm", job(tasks="total"), ("Cleaner list", "Still shows the time")), y0=330)
    add("Job Card", "Extra tag", "for an Extra like Gutter Clean should the tag stay a dashed terracotta outline or become a solid saffron tag?", JB, 640,
        ("dash", "Dashed Outline", "Dashed terracotta Extra, like today.", "calm", job(), ("Today's tag", "Matches + Gutter Clean")),
        ("solid", "Solid Saffron Tag", "White Extra on saffron.", "lively", job(extra="solid"), ("Hard to miss", "Extras look different")), y0=330)
    add("Job Notes", "Bring In and Access", "should the Bring In and Access notes stay cream boxes under headings or become two icon rows?", JB, 880,
        ("box", "Cream Boxes", "Heading, then the note in a cream box.", "calm", job(), ("Today's notes", "Easy to read")),
        ("rows", "Icon Rows", "Box icon for Bring In, key icon for Access.", "practical", job(notes="rows"), ("Shorter card", "Scan by icon")), y0=470)
    add("Job Notes", "Pets and access alert", "should Two small dogs, ring and wait stay inside the Access note or also show as a yellow alert under the address?", JB, 620,
        ("note", "Inside The Access Note", "Read it with the other notes, like today.", "calm", job(), ("Today's card", "One place for notes")),
        ("alert", "Yellow Alert Up Top", "Seen before anything else on the card.", "focused", job(alert=True), ("Can't be missed", "Note still below")), y0=110)
    add("Job Card", "Job card buttons", "at the bottom of the job card should Report and Message stay side by side or should a big Navigate button lead with those two smaller?", JB, 1000,
        ("msg", "Report And Message", "Outline Report, blue Message, like today.", "calm", job(), ("Today's card", "Two clear choices")),
        ("nav", "Navigate Leads", "Big Navigate To Stop 1, Report and Message under it.", "practical", job(btns="nav"), ("Next move is obvious", "Taller footer")), y0=620)
    ST = "TECH APP · STEP SCREEN"
    add("Steps", "Filter condition", "on the HVAC Filter Swap step should the old filter condition be three word buttons or three small filter pictures to tap?", ST, 700,
        ("seg", "Three Word Buttons", "Light, Dirty, Very Dirty, like today.", "calm", step("seg"), ("Today's step", "Fast with one thumb")),
        ("pics", "Three Filter Pictures", "Clean to clogged drawings, tap the closest.", "practical", step("pics"), ("Same call every tech", "Better for the report")), y0=60)
    return pairs
