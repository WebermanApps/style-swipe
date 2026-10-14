"""Shared drawn-SVG kit for dashboard-presentation decks (folio-dashboard, wellnest-dashboard, upkeep-board).
Brand-parametric: each deck passes a brand dict. Example shapes only, no real data or figures."""
import math
from draft_svg import esc, screen, W, H
def R(x, y, w, h, f="none", s="none", r=0, sw=1, ex=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" stroke="{s}" stroke-width="{sw}" {ex}/>'
def T(B, x, y, s, size=9, c=None, head=False, w=None, a="start", ex=""):
    f = B["head"] if head else B["body"]; w = w or (B.get("hw", 600) if head else 400)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c or B["ink"]}" text-anchor="{a}" font-family="{f}" font-weight="{w}" {ex}>{esc(s)}</text>'
def L(x1, y1, x2, y2, c, sw=1, ex=""): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" {ex}/>'
def D(x, y, r, c): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def chev(x, y, c, up=False): return f'<path d="M{x-4} {y-(-2 if up else 2)} L{x} {y+(-2 if up else 2)} L{x+4} {y-(-2 if up else 2)}" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'
def lock(x, y, c, s=1): return f'<g transform="translate({x},{y}) scale({s})"><rect x="-5" y="-1" width="10" height="8" rx="1.5" fill="{c}"/><path d="M-3 -1 V-3.5 A3 3 0 0 1 3 -3.5 V-1" fill="none" stroke="{c}" stroke-width="1.5"/></g>'
def bars(n, x, y, w, c, gap=4):
    return "".join(R(x, y + i * gap, w * (1 - .25 * (i % 3)), 2, c, r=1) for i in range(n))
def wave(x, y, w, h, seed=0, n=24, amp=1.0):
    pts = []
    for i in range(n):
        v = .45 + .22 * math.sin(i * .55 + seed) + .12 * math.sin(i * 1.7 + seed * 2) + i / n * .25 * amp
        pts.append((x + i * w / (n - 1), y + h - h * min(.95, max(.05, v))))
    return pts
def smooth(pts, k=5):
    out = []
    for i in range(len(pts)):
        seg = pts[max(0, i - k):i + 1]; out.append((pts[i][0], sum(p[1] for p in seg) / len(seg)))
    return out
def poly(pts, c, sw=1.6, ex=""): return f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round" {ex}/>'
def area(pts, base, c, op=".15"):
    d = f"M{pts[0][0]:.1f} {base} " + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + f" L{pts[-1][0]:.1f} {base} Z"
    return f'<path d="{d}" fill="{c}" opacity="{op}"/>'
def phone(B, body): return screen(body, B["bg"])
def card(B, x, y, w, h, style=None, c=None):
    st = style or B.get("card", "line")
    if st == "shadow": return R(x + 1, y + 2, w, h, "#0000000D", r=B["r"]) + R(x, y, w, h, "#FFFFFF", r=B["r"])
    if st == "tint": return R(x, y, w, h, (c or B["acc"][0]) + "12", r=B["r"])
    if st == "left": return R(x, y, w, h, "#FFFFFF", B["line"], B["r"]) + R(x, y, 3, h, c or B["acc"][0], r=1.5)
    if st == "flat": return R(x, y, w, h, B["soft"], r=B["r"])
    return R(x, y, w, h, "#FFFFFF", B["line"], B["r"])

# ---------- sections: f(B, y, o) -> (svg, h); drawn at x 14..226 ----------
def s_hdr(B, y, o):
    st = o.get("hdr", "plain")
    if st == "eyebig":
        ec = o.get("ec", B["acc"][0])
        return T(B, 14, y + 14, o.get("sub", "Good Morning, Max").upper(), 6.5, ec, w=600, ex='letter-spacing="1.2"') + T(B, 14, y + 40, o.get("title", B["name"]), 24, None, True) + R(14, y + 46, 26, 2.5, o.get("rule", B["acc"][0])), 56
    if st == "bar" or st == "barshare":
        s = T(B, 14, y + 18, o.get("title", B["name"]), 13, None, True) + L(0, y + 28, W, y + 28, B["line"])
        if st == "barshare": s += f'<g transform="translate(206,{y+6}) scale(.55)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{B["ink"]}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{B["ink"]}" stroke-width="2.2"/></g>'
        else: s += R(166, y + 8, 60, 13, B["acc"][2] + "1F", r=6.5) + T(B, 196, y + 17, "Updated 12m", 6, B["acc"][2], w=600, a="middle")
        return s, 34; t = o.get("title", B["name"]); sub = o.get("sub", "")
    lg = B.get("logo")
    if st == "band":
        c = o.get("hc", B["acc"][0]); return R(0, y, W, 50, c) + T(B, 14, y + 28, t, 16, "#FFFFFF", True) + (T(B, 14, y + 40, sub, 6.5, "#FFFFFFCC") if sub else ""), 58
    if st == "center":
        s = (lg(120, y + 18, 22) if lg else "") + T(B, 120, y + (44 if lg else 24), t, 16, None, True, a="middle") + (T(B, 120, y + (54 if lg else 35), sub, 6.5, B["mute"], a="middle") if sub else "")
        h = 62 if lg else 44; return s + L(14, y + h - 4, 226, y + h - 4, B["line"]), h + 4
    if st == "big":
        return T(B, 14, y + 34, t, 28, None, True) + (T(B, 14, y + 48, sub, 7, B["mute"]) if sub else "") + R(14, y + 54, 30, 2.5, B["acc"][0]), 64
    if st == "logo" and lg:
        return lg(28, y + 20, 26) + T(B, 46, y + 22, t, 14, None, True) + (T(B, 46, y + 32, sub, 6.5, B["mute"]) if sub else "") + L(14, y + 42, 226, y + 42, B["line"]), 48
    if st == "eyebrow":
        return T(B, 14, y + 14, sub.upper() or "GOOD MORNING", 6.5, B["acc"][0], w=600, ex='letter-spacing="1.2"') + T(B, 14, y + 34, t, 18, None, True), 44
    return T(B, 14, y + 24, t, 15, None, True) + (T(B, 14, y + 35, sub, 6.5, B["mute"]) if sub else "") + L(14, y + 42, 226, y + 42, B["line"]), 48
def s_report(B, y, o):
    st = o.get("report", "card"); nm = o.get("rname", "Morning Report"); c = o.get("rc", B["acc"][1])
    if st == "banner": return R(14, y, 212, 34, c + "18", r=B["r"]) + R(14, y, 3, 34, c) + T(B, 24, y + 14, nm, 9.5, None, True) + bars(2, 24, y + 21, 150, B["mute"] + "88"), 40
    if st == "tabs":
        s = R(14, y, 212, 20, B["soft"], r=10) + R(16, y + 2, 104, 16, "#FFFFFF", B["line"], 8) + T(B, 68, y + 13.5, "Morning", 8, None, True, a="middle") + T(B, 172, y + 13.5, "Evening", 8, B["mute"], True, a="middle")
        return s + card(B, 14, y + 26, 212, 50) + bars(4, 24, y + 38, 180, B["mute"] + "88", 8), 84
    if st == "line": return T(B, 14, y + 10, nm.upper(), 6.5, c, w=600, ex='letter-spacing="1.2"') + bars(3, 14, y + 18, 200, B["mute"] + "88", 7) + L(14, y + 42, 226, y + 42, B["line"]), 48
    if st == "collapsed": return card(B, 14, y, 212, 26) + D(26, y + 13, 3.5, c) + T(B, 36, y + 16.5, nm, 9, None, True) + T(B, 196, y + 16, "Read", 7, B["mute"], a="end") + chev(212, y + 13, B["mute"]), 32
    if st == "big":
        return card(B, 14, y, 212, 92, "tint", c) + T(B, 24, y + 20, nm, 15, None, True) + T(B, 24, y + 31, "Example summary, written for today", 6.5, B["mute"]) + bars(5, 24, y + 44, 186, B["ink"] + "55", 8), 98
    if st == "more":
        n = o.get("rn", 3); mk = o.get("more", "link"); h = 30 + n * 12 + 16
        s = card(B, 14, y, 212, h, o.get("rcard")) + T(B, 24, y + 16, nm, 10, None, True) + T(B, 216, y + 16, "Today", 6.5, B["mute"], a="end")
        for i in range(n): s += D(27, y + 29 + i * 12, 2, c) + R(33, y + 27.5 + i * 12, 150 - 25 * (i % 2), 3, B["ink"] + "55", r=1.5)
        if mk == "link": s += T(B, 24, y + h - 7, "Show More", 7, c, w=600, ex='text-decoration="underline"')
        else: s += L(24, y + h - 16, 216, y + h - 16, B["line"]) + T(B, 24, y + h - 5, "More Detail", 7, B["mute"], w=600) + chev(210, y + h - 8, B["mute"])
        return s, h + 6
    return card(B, 14, y, 212, 60) + T(B, 24, y + 16, nm, 10, None, True) + T(B, 216, y + 16, "Today", 6.5, B["mute"], a="end") + bars(4, 24, y + 26, 180, B["mute"] + "88", 7), 66
TILE_IC = ["M4 18 L9 12 L13 15 L20 7", "M5 5 H19 V19 H5 Z M5 10 H19", "M12 4 A8 8 0 1 0 20 12 H12 Z", "M4 20 V10 M10 20 V5 M16 20 V13", "M6 4 H18 V20 H6 Z M9 9 H15 M9 13 H15", "M4 12 L12 4 L20 12 V20 H4 Z"]
def tile_icon(x, y, k, c, s=14): return f'<g transform="translate({x},{y}) scale({s/24})"><path d="{TILE_IC[k%6]}" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/></g>'
def s_tiles(B, y, o):
    names = o.get("tnames", ["Investments", "Spending", "Taxes", "Cards", "Property", "Business"])
    cols = o.get("cols", 2); n = o.get("tn", len(names)); st = o.get("tiles", "line"); lk = o.get("locked", False); th = o.get("th", 44 if cols < 4 else 40)
    w = (212 - (cols - 1) * 6) / cols; s = ""
    for i in range(n):
        x, yy = 14 + (i % cols) * (w + 6), y + (i // cols) * (th + 6); c = B["acc"][i % len(B["acc"])]
        if st == "solid": s += R(x, yy, w, th, c, r=B["r"]) + tile_icon(x + 7, yy + 7, i, "#FFFFFF", 12) + T(B, x + 7, yy + th - 8, names[i % len(names)], 8.5 if cols < 3 else 7, "#FFFFFF", True)
        elif st == "tint": s += R(x, yy, w, th, c + "16", r=B["r"]) + tile_icon(x + 7, yy + 7, i, c, 12) + T(B, x + 7, yy + th - 8, names[i % len(names)], 8.5 if cols < 3 else 7, None, True)
        elif st == "row": s += card(B, 14, y + i * 26, 212, 22) + tile_icon(20, y + i * 26 + 4, i, c, 13) + T(B, 40, y + i * 26 + 14.5, names[i % len(names)], 8.5, None, True) + chev(214, y + i * 26 + 11, B["mute"]) .replace("M210", "M210")
        elif st == "lineplain": s += R(x, yy, w, th, "#FFFFFF", B["line"], B["r"]) + tile_icon(x + 9, yy + 8, i, c, 14) + T(B, x + 7, yy + th - 8, names[i % len(names)], 8.5 if cols < 3 else 7, None, True)
        elif st == "linecenter": s += R(x, yy, w, th, "#FFFFFF", B["line"], B["r"]) + R(x + w / 2 - 9, yy + 6, 18, 18, c + "1F", r=5) + tile_icon(x + w / 2 - 7, yy + 8, i, c, 14) + T(B, x + w / 2, yy + th - 7, names[i % len(names)], 7, None, True, a="middle")
        else: s += R(x, yy, w, th, "#FFFFFF", B["line"], B["r"]) + R(x + 7, yy + 6, 18, 18, c + "1F", r=5) + tile_icon(x + 9, yy + 8, i, c, 14) + T(B, x + 7, yy + th - 8, names[i % len(names)], 8.5 if cols < 3 else 7, None, True)
        if lk and st != "row": s += (lock(x + w - 10, yy + 10, "#FFFFFF" if st == "solid" else B["mute"], .8) if lk == "icon" else R(x, yy, w, th, "#FFFFFF99", r=B["r"]) + lock(x + w / 2, yy + th / 2 - 2, B["mute"], 1))
        if lk and st == "row": s += lock(200, y + i * 26 + 10, B["mute"], .8)
    rows = n if st == "row" else math.ceil(n / cols)
    return s, rows * ((26) if st == "row" else (th + 6)) + 4
def s_urgent(B, y, o):
    st = o.get("urgent", "collapsed"); c = o.get("uc", B["acc"][0]); n = o.get("un", 3)
    items = o.get("uitems", ["Upload an example file", "Check a due date", "Confirm a category"])
    if st == "collapsed": return card(B, 14, y, 212, 28, "left", c) + T(B, 24, y + 17.5, f"Urgent", 9.5, None, True) + R(184, y + 8, 14, 12, c, r=6) + T(B, 191, y + 17, str(n), 7, "#FFFFFF", a="middle", w=600) + chev(212, y + 14, B["mute"]), 34
    if st == "pillsolid": return R(14, y, 118, 22, c, r=11) + T(B, 26, y + 14.5, f"{n} Urgent Items", 7.5, "#FFFFFF", w=600) + chev(122, y + 11, "#FFFFFF"), 28
    if st == "pillcount": return R(14, y, 118, 22, "#FFFFFF", B["line"], 11) + R(18, y + 4, 14, 14, c, r=7) + T(B, 25, y + 14, str(n), 7, "#FFFFFF", w=600, a="middle") + T(B, 37, y + 14.5, "Urgent Items", 7.5, B["ink"], w=600) + chev(122, y + 11, B["mute"]), 28
    if st == "pill": return R(14, y, 118, 22, c + "18", r=11) + D(26, y + 11, 3.5, c) + T(B, 34, y + 14.5, f"{n} Urgent Items", 7.5, c, w=600) + chev(122, y + 11, c), 28
    if st == "open":
        s = card(B, 14, y, 212, 22 + n * 18, "left", c) + T(B, 24, y + 15, "Urgent", 9.5, None, True) + chev(212, y + 11, B["mute"], True)
        for i in range(n): s += D(28, y + 30 + i * 18, 2.5, c) + T(B, 36, y + 33 + i * 18, items[i % len(items)], 7.5, B["ink"])
        return s, 28 + n * 18
    if st == "bar": return R(14, y, 212, 24, c, r=B["r"]) + T(B, 24, y + 15.5, f"{n} Need You Today", 8.5, "#FFFFFF", True) + chev(212, y + 12, "#FFFFFF"), 30
    return "", 0
def s_chart(B, y, o):
    st = o.get("chart", "line"); h = o.get("ch", 90); c = o.get("cc", B["acc"][1]); s1, s2 = o.get("smac", (B["acc"][0], B["acc"][2]))
    pts = wave(24, y + 22, 192, h - 34, o.get("seed", 1)); m1 = smooth(pts, 4); m2 = smooth(pts, 10)
    s = card(B, 14, y, 212, h, o.get("ccard")) + T(B, 24, y + 15, o.get("ctitle", "Portfolio"), 9.5, None, True)
    sma = o.get("sma", "dashed")
    if st == "area": s += area(pts, y + h - 12, c) + poly(pts, c, 1.8)
    elif st == "candle":
        for i, (a, b) in enumerate(pts[::2]): s += R(a - 2, b - 4, 4, 8, (B["acc"][2] if i % 3 else B["acc"][0]), r=1) + L(a, b - 7, a, b + 7, B["mute"], .6)
    elif st == "step": s += poly([q for i in range(len(pts) - 1) for q in (pts[i], (pts[i + 1][0], pts[i][1]))], c, 1.6)
    else: s += poly(pts, c, o.get("lw", 1.8))
    if sma != "none":
        ex1, ex2 = ('stroke-dasharray="4 2"', 'stroke-dasharray="1.5 2"') if sma == "dashed" else ("", "")
        w1, w2 = (1.2, 1.2) if sma != "thick" else (2, 2)
        s += poly(m1, s1, w1, ex1 + ' opacity=".9"') + poly(m2, s2, w2, ex2 + ' opacity=".9"')
        if o.get("legend", "top") == "top": s += D(150, y + 12, 2.5, s1) + T(B, 155, y + 14.5, "100-Day", 6, B["mute"]) + D(186, y + 12, 2.5, s2) + T(B, 191, y + 14.5, "200-Day", 6, B["mute"])
        elif o.get("legend") == "end": s += T(B, 218, m1[-1][1] - 2, "100D", 5.5, s1, a="end", w=600) + T(B, 218, m2[-1][1] + 8, "200D", 5.5, s2, a="end", w=600)
    if o.get("grid"): s += "".join(L(24, y + 26 + i * (h - 38) / 3, 216, y + 26 + i * (h - 38) / 3, B["line"], .6) for i in range(4))
    if o.get("range"): s += "".join(R(24 + i * 30, y + h - 14, 26, 10, (c if i == 2 else B["soft"]), r=5) + T(B, 37 + i * 30, y + h - 6.5, r, 5.5, "#FFFFFF" if i == 2 else B["mute"], a="middle") for i, r in enumerate(["1M", "3M", "1Y", "5Y"]))
    return s, h + 6
def s_spend(B, y, o):
    st = o.get("spend", "bars"); h = o.get("sh", 84); cats = ["Home", "Food", "Travel", "Health", "Other"]
    s = card(B, 14, y, 212, h) + T(B, 24, y + 15, "Spending", 9.5, None, True); vals = [.9, .7, .5, .35, .2]
    if st == "donut":
        cx, cy, r = 62, y + 48, 24; a0 = -90
        for i, v in enumerate([.34, .24, .18, .14, .1]):
            a1 = a0 + v * 360; la = 1 if v > .5 else 0
            x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)); x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
            s += f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {la} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{B["acc"][i%len(B["acc"])]}" stroke-width="{o.get('dw', 9)}"/>'; a0 = a1
        s += "".join(D(110, y + 30 + i * 10, 2.5, B["acc"][i % len(B["acc"])]) + T(B, 116, y + 32.5 + i * 10, cats[i], 6.5, B["mute"]) for i in range(5))
    elif st == "hbars": s += "".join(T(B, 24, y + 31 + i * 11, cats[i], 6.5, B["mute"]) + R(62, y + 26 + i * 11, 140 * vals[i], 6, B["acc"][i % len(B["acc"])], r=3) for i in range(5))
    elif st == "stack":
        x = 24
        for i, v in enumerate([.34, .24, .18, .14, .1]): s += R(x, y + 26, 192 * v, 14, B["acc"][i % len(B["acc"])]); x += 192 * v
        s += "".join(D(28 + i * 40, y + 52, 2.5, B["acc"][i % len(B["acc"])]) + T(B, 34 + i * 40, y + 54.5, cats[i], 6, B["mute"]) for i in range(5))
    else:
        bw = 192 / 8
        for i in range(8):
            v = .3 + .5 * abs(math.sin(i * 1.3)); s += R(24 + i * bw + 3, y + h - 10 - (h - 34) * v, bw - 6, (h - 34) * v, B["acc"][1] if i == 7 else B["acc"][1] + "55", r=2)
    return s, h + 6
def s_feed(B, y, o):
    if o.get("feed") == "icons":
        n = o.get("fn", 3); s = T(B, 14, y + 10, o.get("fname", "Recent Work").upper(), 6.5, B["mute"], w=600, ex='letter-spacing="1.2"')
        for i in range(n):
            yy = y + 16 + i * 30; c = B["acc"][i % len(B["acc"])]
            s += card(B, 14, yy, 212, 26) + R(20, yy + 4, 18, 18, c + "1F", r=5) + tile_icon(22, yy + 6, i, c, 14) + R(44, yy + 8, 110 + 30 * (i % 2), 3, B["ink"] + "55", r=1.5) + R(44, yy + 15, 60, 2.5, B["mute"] + "55", r=1)
        return s, 20 + n * 30
    n = o.get("fn", 3); s = T(B, 14, y + 10, o.get("fname", "Recent Work").upper(), 6.5, B["mute"], w=600, ex='letter-spacing="1.2"')
    for i in range(n): s += D(20, y + 22 + i * 18, 3, B["acc"][i % len(B["acc"])]) + R(30, y + 19 + i * 18, 120 + 40 * (i % 2), 3, B["ink"] + "44", r=1.5) + R(30, y + 25 + i * 18, 70, 2.5, B["mute"] + "55", r=1)
    return s, 20 + n * 18
def s_video(B, y, o):
    st = o.get("video", "card"); c = B["acc"][1]
    if st == "thumb": return R(14, y, 212, 100, c + "22", r=B["r"]) + D(120, y + 50, 14, "#FFFFFFEE") + f'<path d="M116 {y+43} L127 {y+50} L116 {y+57} Z" fill="{c}"/>' + T(B, 22, y + 92, o.get("vt", "Video Of The Week"), 9, None, True), 106
    if st == "rowr": return card(B, 14, y, 212, 40) + R(174, y + 6, 46, 28, c + "22", r=4) + f'<path d="M193 {y+14} L202 {y+20} L193 {y+26} Z" fill="{c}"/>' + T(B, 24, y + 18, o.get("vt", "Video Of The Week"), 9, None, True) + T(B, 24, y + 29, "Example clip", 6.5, B["mute"]), 46
    if st == "rowdur": return card(B, 14, y, 212, 40) + R(20, y + 6, 46, 28, c + "22", r=4) + f'<path d="M39 {y+14} L48 {y+20} L39 {y+26} Z" fill="{c}"/>' + R(48, y + 26, 16, 7, B["ink"] + "CC", r=2) + T(B, 56, y + 31.5, "0:45", 4.5, "#FFFFFF", a="middle") + T(B, 74, y + 18, o.get("vt", "Video Of The Week"), 9, None, True) + T(B, 74, y + 29, "Example clip", 6.5, B["mute"]), 46
    return card(B, 14, y, 212, 40) + R(20, y + 6, 46, 28, c + "22", r=4) + f'<path d="M39 {y+14} L48 {y+20} L39 {y+26} Z" fill="{c}"/>' + T(B, 74, y + 18, o.get("vt", "Video Of The Week"), 9, None, True) + T(B, 74, y + 29, "Example clip", 6.5, B["mute"]), 46
def s_gap(B, y, o): return "", o.get("gap", 8)
def s_unlock(B, y, o):
    st = o.get("unlock", "center"); c = B["acc"][0]
    if st == "split":
        return R(0, y, W, 120, c + "14") + lock(120, y + 56, c, 2.2) + T(B, 120, y + 96, "Private Page", 14, None, True, a="middle") + card(B, 24, y + 136, 192, 28) + T(B, 34, y + 154, "Password", 8, B["mute"]) + R(24, y + 172, 192, 28, B["ink"], r=B["r"]) + T(B, 120, y + 190, "UNLOCK", 8, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"'), 210
    if st == "pin":
        s = lock(120, y + 40, B["ink"], 1.6) + T(B, 120, y + 72, "Enter Code", 14, None, True, a="middle") + "".join(D(84 + i * 24, y + 92, 5, B["ink"] if i < 2 else B["line"]) for i in range(4))
        for i in range(9): s += R(48 + (i % 3) * 50, y + 110 + (i // 3) * 36, 44, 30, B["soft"], r=15) + T(B, 70 + (i % 3) * 50, y + 129 + (i // 3) * 36, str(i + 1), 11, None, True, a="middle")
        return s, 220
    return lock(120, y + 50, B["mute"], 1.6) + T(B, 120, y + 84, "Unlock To View", 15, None, True, a="middle") + T(B, 120, y + 98, "Tap a tile, then enter the password", 6.8, B["mute"], a="middle") + R(34, y + 112, 172, 28, "#FFFFFF", B["line"], B["r"]) + T(B, 44, y + 130, "Password", 8, B["mute"]) + R(34, y + 148, 172, 28, c, r=B["r"]) + T(B, 120, y + 166, "UNLOCK", 8, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"'), 190
SEC = dict(hdr=s_hdr, report=s_report, tiles=s_tiles, urgent=s_urgent, chart=s_chart, spend=s_spend, feed=s_feed, video=s_video, gap=s_gap, unlock=s_unlock)
def stack(B, order, o, y0=10, gap=None):
    s, y = "", y0; g = o.get("dens", 6) if gap is None else gap
    for k in order:
        a, h = SEC[k](B, y, o); s += a; y += h + (g if h else 0)
    return s, y
def mock(B, order, foot=True, **o):
    s, _ = stack(B, order, o, o.get("y0", 10)); return phone(B, s)
def desk(B, colsets, label="Big Monitor", ratio=(224, 140), frame="monitor", **o):
    """Wide screen drawn at top: colsets = list of section lists, one per column."""
    fw, fh = ratio; fx = (W - fw) / 2; fy = 34
    s = T(B, 120, 20, label, 9, B["mute"], True, a="middle") + R(fx, fy, fw, fh, B["bg"], "#BDB6AA", 6, 1.2)
    if frame == "monitor": s += R(110, fy + fh, 20, 14, "#D6D0C6") + R(90, fy + fh + 14, 60, 4, "#BDB6AA", r=2)
    elif frame == "laptop": s += R(fx - 12, fy + fh, fw + 24, 6, "#D6D0C6", r=3)
    n = len(colsets); cw = (fw - 8 - (n - 1) * 4) / n if n > 1 else fw * .42; sc = cw / 212; ox = 0 if n > 1 else (fw - 8 - cw) / 2
    inner = ""
    for i, cs in enumerate(colsets):
        g, hh = stack(B, cs, o, 6)
        inner += f'<g transform="translate({fx + 4 + ox + i * (cw + 4) - 14 * sc:.1f},{fy + 2}) scale({sc:.3f})">{g}</g>'
    s += f'<clipPath id="dk"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="6"/></clipPath><g clip-path="url(#dk)">{inner}</g>'
    if o.get("note"): s += T(B, 120, 250, o["note"], 7.5, B["mute"], a="middle")
    return phone(B, s)
def phoneframe(B, order, label="Phone", **o):
    g, _ = stack(B, order, o, 6); sc = .5
    s = T(B, 120, 20, label, 9, B["mute"], True, a="middle") + R(84, 30, 72, 150, B["bg"], "#BDB6AA", 10, 1.2)
    s += f'<clipPath id="pf"><rect x="84" y="30" width="72" height="150" rx="10"/></clipPath><g clip-path="url(#pf)"><g transform="translate({84+4-14*sc*0.6:.1f},34) scale({sc*0.6:.3f})">{g}</g></g>'
    if o.get("note"): s += T(B, 120, 200, o["note"], 7.5, B["mute"], a="middle")
    return phone(B, s)
def s_decks(B, y, o):
    st = o.get("decks", "list"); names = o.get("dnames", ["Brand Deck Round Two", "Brand Deck", "Product Deck"]); prog = o.get("prog", "bar")
    stat = o.get("dstat", [(0, 61), (192, 200), (25, 25)]); s = ""; c0 = o.get("dc", B["acc"][0])
    def pr(x, yy, w, a, n, c):
        if prog == "bar": return R(x, yy, w, 3, B["line"], r=1.5) + R(x, yy, w * a / n, 3, c, r=1.5)
        if prog == "ring":
            r = 7; fr = a / n; ang = fr * 2 * math.pi - math.pi / 2; la = 1 if fr > .5 else 0
            arc = "" if fr == 0 else (f'<circle cx="{x}" cy="{yy}" r="{r}" fill="none" stroke="{c}" stroke-width="2.5"/>' if fr >= 1 else f'<path d="M{x} {yy-r} A{r} {r} 0 {la} 1 {x + r*math.cos(ang):.1f} {yy + r*math.sin(ang):.1f}" fill="none" stroke="{c}" stroke-width="2.5"/>')
            return f'<circle cx="{x}" cy="{yy}" r="{r}" fill="none" stroke="{B["line"]}" stroke-width="2.5"/>' + arc
        return T(B, x, yy, f"{a} of {n}" if a else "New", 6.5, c, w=600)
    if st == "feature":
        s += R(14, y, 212, 70, "#FFFFFF", c0, B["r"], 2) + T(B, 24, y + 14, "FEATURED", 6, c0, w=600, ex='letter-spacing="1.2"') + T(B, 24, y + 31, names[0], 13, None, True) + bars(2, 24, y + 40, 170, B["mute"] + "88", 6)
        s += (pr(24, y + 58, 120, *stat[0], c0) if prog != "ring" else pr(30, y + 58, 0, *stat[0], c0)); y2 = y + 76
        for i, nm in enumerate(names[1:]):
            yy = y2 + i * 30; s += card(B, 14, yy, 212, 26) + T(B, 24, yy + 16, nm, 8.5, None, True) + (pr(150, yy + 12, 60, *stat[i + 1], B["acc"][(i + 1) % len(B["acc"])]) if prog == "bar" else pr(206 if prog == "ring" else 170, yy + 13 + (0 if prog == "ring" else 3), 0, *stat[i + 1], B["acc"][(i + 1) % len(B["acc"])]))
        return s, 76 + len(names[1:]) * 30
    if st == "grid":
        w = 103
        for i, nm in enumerate(names[:4]):
            x, yy = 14 + (i % 2) * (w + 6), y + (i // 2) * 62; a, n = stat[i % len(stat)]; c = B["acc"][i % len(B["acc"])]
            s += card(B, x, yy, w, 56) + R(x, yy, w, 4, c, r=2) + T(B, x + 8, yy + 20, nm[:16], 8.5, None, True) + T(B, x + 8, yy + 30, f"{n} pairs", 6, B["mute"]) + (pr(x + 8, yy + 44, w - 16, a, n, c) if prog == "bar" else pr(x + w - 14 if prog == "ring" else x + 8, yy + 46, 0, a, n, c))
        return s, ((min(4, len(names)) + 1) // 2) * 62
    for i, nm in enumerate(names):
        yy = y + i * 34; a, n = stat[i % len(stat)]; c = B["acc"][i % len(B["acc"])]
        s += card(B, 14, yy, 212, 30) + D(24, yy + 15, 3, c) + T(B, 32, yy + 13, nm, 8.5, None, True) + T(B, 32, yy + 23, f"{n} pairs", 6, B["mute"])
        s += pr(150, yy + 14, 64, a, n, c) if prog == "bar" else pr(206 if prog == "ring" else 176, yy + 15 + (0 if prog == "ring" else 2), 0, a, n, c)
    return s, len(names) * 34
SEC["decks"] = s_decks
def s_text(B, y, o):  # section title
    return T(B, 14, y + 12, o.get("_t", "Section"), 10, None, True), 16
