"""Card art for the Household refresh decks (Branding, Oct 17 2026). Light only (white + #FAF6EE cream), square corners,
#E3DDD2 borders, Khand headings, Hind body. Three card kinds:
  photo_card  real Commons photo filling the top, credit line under the text
  art_card    real CC0 artwork shown whole on cream, credit line
  drawn_card  clean drawn illustration (MOTIFS, 120x120 line drawings) with two short fact chips"""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import html, hashlib
INK, MUTE, FOOT, CREAM, BD = "#0A0A0A", "#525252", "#8A8580", "#FAF6EE", "#E3DDD2"
W, H = 240, 300
E = lambda s: html.escape(str(s), quote=True)
def t(x, y, s, size, col=INK, fam="Hind", wt=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-family="{fam}, sans-serif" font-weight="{wt}" {extra}>{E(s)}</text>'
def wrap(s, n):
    out, cur = [], ""
    for w in str(s).split():
        if cur and len(cur) + 1 + len(w) > n: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + ([cur] if cur else [])
def title(y, s, size=20, n=22):
    ls = wrap(s, n)
    if len(ls) > 1: size = size - 3; ls = wrap(s, int(n * 1.2))
    return "".join(t(16, y + i * (size + 1), l, size, INK, "Khand", 700) for i, l in enumerate(ls[:2])), (len(ls[:2]) - 1) * (size + 1)
def shell(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-width:100%;height:auto">'
            f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>{body}<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="{BD}"/></svg>')
def _cid(*a): return "h" + hashlib.md5("|".join(map(str, a)).encode()).hexdigest()[:8]
def who(a):
    a = (a or "").split("\n")[0].replace("This Photo was taken by ", "").strip()
    return a[:28] + ("\u2026" if len(a) > 28 else "")
def photo_card(c, label, desc, accent):
    cid = _cid(c["file"], label); ih = 188
    s = f'<clipPath id="{cid}"><rect x="0" y="0" width="{W}" height="{ih}"/></clipPath>'
    s += f'<rect x="0" y="0" width="{W}" height="{ih}" fill="{CREAM}"/><image href="{c["file"]}" xlink:href="{c["file"]}" x="0" y="0" width="{W}" height="{ih}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>'
    s += f'<rect x="0" y="{ih}" width="{W}" height="4" fill="{accent}"/>'
    tt, dy = title(ih + 30, label, 19, 24)
    s += tt + "".join(t(16, ih + 48 + dy + i * 13, l, 10.5, MUTE) for i, l in enumerate(wrap(desc, 40)[:3 if not dy else 2]))
    s += t(16, 290, f'Photo: {who(c["author"])} \u00b7 {c["license"]} \u00b7 Wikimedia Commons', 7.5, FOOT)
    return shell(s)
def art_card(c, label, desc, accent):
    bw, bh = 224, 178; sc = c["w"] / c["h"]
    iw, ih = (bw - 12, (bw - 12) / sc) if sc > (bw - 12) / (bh - 12) else ((bh - 12) * sc, bh - 12)
    x, y = 8 + (bw - iw) / 2, 8 + (bh - ih) / 2
    s = f'<rect x="8" y="8" width="{bw}" height="{bh}" fill="{CREAM}" stroke="{BD}"/>'
    s += f'<image href="{c["file"]}" xlink:href="{c["file"]}" x="{x:.1f}" y="{y:.1f}" width="{iw:.1f}" height="{ih:.1f}" preserveAspectRatio="xMidYMid meet"/>'
    tt, dy = title(214, label, 19, 24)
    s += tt + "".join(t(16, 232 + dy + i * 13, l, 10.5, MUTE) for i, l in enumerate(wrap(desc, 40)[:3 if not dy else 2]))
    s += t(16, 290, "Art Institute of Chicago \u00b7 CC0 public domain", 7.5, FOOT)
    return shell(s)
def drawn_card(group, label, desc, motif, chips, accent):
    s = f'<rect x="0" y="0" width="{W}" height="164" fill="{CREAM}"/><line x1="0" y1="164.5" x2="{W}" y2="164.5" stroke="{BD}"/>'
    s += t(16, 24, group.upper(), 8.5, accent, "Hind", 600, extra='letter-spacing="1.2"')
    s += f'<g transform="translate(60,34)">{MOTIFS[motif](accent)}</g>'
    tt, dy = title(192, label, 20, 22)
    s += tt + "".join(t(16, 210 + dy + i * 13, l, 10.5, MUTE) for i, l in enumerate(wrap(desc, 40)[:3 if not dy else 2]))
    x = 16
    for ch in chips[:2]:
        w = len(ch) * 5.3 + 18
        s += f'<rect x="{x}" y="258" width="{w:.0f}" height="20" fill="#FFFFFF" stroke="{BD}"/><rect x="{x}" y="258" width="3" height="20" fill="{accent}"/>' + t(x + 10, 271.5, ch, 9.5, INK, "Hind", 600)
        x += w + 8
    s += t(224, 292, "Built by Machan", 7.5, FOOT, anchor="end")
    return shell(s)

# ---- motifs: 120x120 line drawings, stroke = accent, light tint fills, square-cornered shapes
def _p(d, c, fill="none", sw=3): return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
def _r(x, y, w, h, c, fill="#FFFFFF", sw=3): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'
def _c(x, y, r, c, fill="#FFFFFF", sw=3): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'
T = lambda c: c + "26"
MOTIFS = {
 "car": lambda c: _r(14, 50, 92, 34, c, T(c)) + _p("M28 50 L40 30 H80 L92 50", c, "#FFFFFF") + _c(34, 86, 11, c) + _c(86, 86, 11, c) + _p("M60 32 V50", c),
 "sun": lambda c: _c(60, 60, 22, c, T(c)) + "".join(_p(f"M{60+34*x} {60+34*y} L{60+46*x} {60+46*y}", c) for x, y in [(1,0),(-1,0),(0,1),(0,-1),(.7,.7),(-.7,.7),(.7,-.7),(-.7,-.7)]),
 "moon": lambda c: _p("M76 18 A40 40 0 1 0 100 78 A32 32 0 1 1 76 18 Z", c, T(c)) + _c(30, 26, 3, c, c, 1) + _c(98, 34, 2.5, c, c, 1),
 "clock": lambda c: _c(60, 60, 44, c, T(c)) + _p("M60 30 V60 L82 72", c, sw=4) + _c(60, 60, 4, c, c, 1),
 "calendar": lambda c: _r(16, 22, 88, 84, c) + _r(16, 22, 88, 20, c, T(c)) + _p("M38 14 V30 M82 14 V30", c) + "".join(_r(28 + (i % 4) * 18, 52 + (i // 4) * 16, 10, 10, c, c if i == 6 else T(c), 2) for i in range(12)),
 "pot": lambda c: _p("M18 52 H102 V86 Q102 100 88 100 H32 Q18 100 18 86 Z", c, T(c)) + _p("M8 58 H18 M102 58 H112 M30 52 V44 H90 V52", c) + _p("M44 34 Q40 26 46 18 M60 34 Q56 26 62 18 M76 34 Q72 26 78 18", c),
 "plate": lambda c: _c(60, 62, 42, c) + _c(60, 62, 28, c, T(c)) + _p("M8 30 V96 M14 30 V50 Q14 58 8 58 M112 30 Q100 50 112 66 V96", c),
 "basket": lambda c: _p("M14 48 H106 L96 102 H24 Z", c, T(c)) + _p("M34 48 Q60 6 86 48", c) + _p("M30 66 H90 M34 84 H86 M46 48 L50 102 M74 48 L70 102", c, sw=2),
 "shirt": lambda c: _p("M40 18 L18 32 L28 52 L38 46 V104 H82 V46 L92 52 L102 32 L80 18 Q60 34 40 18 Z", c, T(c)),
 "hanger": lambda c: _p("M60 40 V30 Q60 20 70 20 Q78 22 76 30 M60 40 L12 74 H108 Z", c) + _p("M30 74 V104 H90 V74", c, T(c)),
 "wheel": lambda c: _c(60, 60, 44, c) + "".join(_p(f"M60 60 L{60+44*x:.0f} {60+44*y:.0f}", c, sw=2) for x, y in [(1,0),(-.5,.87),(-.5,-.87)]) + _p("M60 60 L104 60 A44 44 0 0 1 38 98 Z", c, T(c), 2) + _p("M60 6 L54 -4 H66 Z", c, c),
 "list": lambda c: _r(22, 10, 76, 100, c) + "".join(_r(32, 26 + i * 20, 10, 10, c, c if i < 2 else "#FFFFFF", 2) + _p(f"M50 {31+i*20} H88", c, sw=2) for i in range(4)),
 "check": lambda c: _r(22, 10, 76, 100, c) + "".join(_p(f"M32 {30+i*20} l4 4 8 -8", c) + _p(f"M52 {31+i*20} H88", c, sw=2) for i in range(4)),
 "fridge": lambda c: _r(28, 6, 64, 108, c, T(c)) + _p("M28 44 H92 M38 22 V34 M38 56 V76", c),
 "jars": lambda c: "".join(_r(10 + i * 36, 40 - (i % 2) * 14, 28, 64 + (i % 2) * 14, c, T(c)) + _r(8 + i * 36, 32 - (i % 2) * 14, 32, 8, c, "#FFFFFF") + _r(14 + i * 36, 62, 20, 12, c, "#FFFFFF", 2) for i in range(3)),
 "jars2": lambda c: _r(14, 40, 92, 62, c) + _r(24, 26, 30, 22, c, T(c)) + _r(64, 30, 32, 18, c, T(c)) + _p("M14 60 H106", c, sw=2) + _p("M30 76 h60", c, sw=2),
 "bed": lambda c: _r(10, 58, 100, 30, c, T(c)) + _r(18, 44, 32, 16, c) + _p("M10 40 V100 M110 70 V100", c),
 "bed2": lambda c: _r(10, 58, 100, 30, c) + _p("M10 66 H110 M10 76 H110", c, sw=2) + _r(18, 44, 32, 16, c, T(c)) + _p("M10 40 V100 M110 70 V100", c),
 "swap": lambda c: _p("M20 44 H96 L82 30 M100 76 H24 L38 90", c, sw=4) + _c(20, 44, 6, c, T(c)) + _c(100, 76, 6, c, T(c)),
 "door": lambda c: _r(34, 8, 52, 104, c, T(c)) + _c(76, 62, 4, c, c) + _p("M8 112 H112", c) + _r(92, 82, 18, 30, c),
 "hooks": lambda c: _p("M10 22 H110", c, sw=4) + "".join(_p(f"M{24+i*32} 22 V40 Q{24+i*32} 50 {32+i*32} 46", c) for i in range(3)) + _r(16, 46, 22, 30, c, T(c)) + _r(12, 88, 96, 12, c, T(c)) + _p("M18 100 V112 M102 100 V112", c),
 "box": lambda c: _p("M14 46 L60 28 L106 46 V96 L60 114 L14 96 Z", c, T(c)) + _p("M14 46 L60 64 L106 46 M60 64 V114", c) + _p("M14 46 L4 30 L50 12 L60 28", c, "#FFFFFF"),
 "shelf": lambda c: _r(12, 10, 96, 100, c) + _p("M12 44 H108 M12 78 H108", c) + _c(34, 34, 9, c, T(c)) + _r(58, 22, 18, 22, c, T(c), 2) + _r(28, 60, 26, 18, c, T(c), 2) + _c(84, 66, 10, c, T(c)),
 "phone": lambda c: _r(36, 6, 48, 108, c, T(c)) + _r(42, 18, 36, 74, c) + _c(60, 102, 4, c, c),
 "tray": lambda c: _p("M8 70 H112 L100 98 H20 Z", c, T(c)) + "".join(_r(24 + i * 6, 34 - i * 6, 64, 40, c, "#FFFFFF", 2) for i in range(3)),
 "caddy": lambda c: _r(14, 56, 92, 46, c, T(c)) + _p("M60 56 V26 M44 26 H76", c, sw=4) + _r(22, 30, 14, 26, c) + _r(84, 36, 14, 20, c),
 "lock": lambda c: _r(24, 52, 72, 58, c, T(c)) + _p("M38 52 V36 Q38 14 60 14 Q82 14 82 36 V52", c, sw=4) + _c(60, 78, 7, c, c),
 "counter": lambda c: _r(6, 66, 108, 12, c, T(c)) + _r(12, 78, 96, 34, c) + _p("M60 78 V112", c, sw=2) + _p("M30 50 Q30 30 50 30", c, sw=2),
 "kettle": lambda c: _p("M30 104 L36 46 H84 L90 104 Z", c, T(c)) + _p("M44 46 Q60 22 76 46 M90 60 L106 48", c) + _r(52, 34, 16, 6, c),
 "plug": lambda c: _r(30, 40, 60, 40, c, T(c)) + _p("M46 40 V20 M74 40 V20 M60 80 V112", c, sw=4),
 "leaf": lambda c: _p("M18 104 Q10 30 104 14 Q110 96 18 104 Z", c, T(c)) + _p("M18 104 L82 38 M44 76 L44 52 M60 60 L80 60", c, sw=2),
 "leaf2": lambda c: _p("M60 110 V60", c) + _c(60, 46, 32, c, T(c)) + _r(10, 98, 100, 10, c, "#FFFFFF", 2),
 "flag": lambda c: _p("M24 112 V10", c, sw=4) + _p("M24 14 H96 L84 34 L96 54 H24", c, T(c)),
 "bowl": lambda c: _p("M10 52 H110 Q108 102 60 104 Q12 102 10 52 Z", c, T(c)) + _p("M40 40 Q36 28 44 18 M62 40 Q58 28 66 18", c) + _p("M86 20 L104 52", c),
 "cup": lambda c: _p("M28 26 H86 L80 104 H34 Z", c, T(c)) + _p("M86 44 Q106 46 104 64 Q102 80 82 80", c),
 "strawcup": lambda c: _p("M34 36 H86 L80 104 H40 Z", c, T(c)) + _p("M66 36 L76 8 H86", c) + _p("M34 60 H20 V78 H36 M86 60 H100 V78 H84", c),
 "jar": lambda c: _p("M40 18 H80 V30 Q104 44 100 80 Q96 110 60 110 Q24 110 20 80 Q16 44 40 30 Z", c, T(c)) + _p("M30 64 H90", c, sw=2),
 "seat": lambda c: _r(20, 20, 50, 60, c, T(c)) + _r(20, 80, 76, 20, c) + _p("M96 100 V60 M30 100 V112 M88 100 V112", c),
 "house": lambda c: _p("M14 56 L60 16 L106 56 V108 H14 Z", c, T(c)) + _r(48, 72, 24, 36, c) + _r(24, 64, 16, 14, c, "#FFFFFF", 2) + _r(80, 64, 16, 14, c, "#FFFFFF", 2),
 "pool": lambda c: _r(8, 48, 104, 56, c, T(c)) + _p("M18 70 Q32 62 46 70 T74 70 T102 70 M18 88 Q32 80 46 88 T74 88 T102 88", c, sw=2) + _p("M88 48 V18 H100 V48", c),
 "cloud": lambda c: _p("M28 82 Q8 82 10 64 Q12 46 32 48 Q38 22 64 26 Q88 28 90 50 Q112 50 110 68 Q108 84 90 82 Z", c, T(c)) + _p("M14 100 H106 M26 112 H94", c, sw=2),
 "plane": lambda c: _p("M10 60 L110 38 L104 52 L66 66 L52 102 L42 104 L46 70 L20 76 Z", c, T(c)),
 "tin": lambda c: _r(28, 46, 64, 62, c, T(c)) + _r(24, 38, 72, 10, c) + _r(18, 6, 22, 22, c, "#FFFFFF") + _r(80, 14, 20, 20, c, "#FFFFFF") + _p("M30 30 L46 42 M88 36 L78 42", c, sw=2),
 "tube": lambda c: _r(46, 4, 28, 92, c, T(c)) + _c(60, 22, 9, c) + _p("M14 108 H106", c) + _c(92, 98, 10, c, "#FFFFFF") + _p("M74 86 L80 92", c, sw=2),
 "puzzle": lambda c: _r(8, 22, 104, 84, c) + _c(40, 64, 20, c, T(c)) + _r(70, 46, 30, 36, c, T(c)) + _c(40, 64, 5, c, c) + _c(85, 64, 5, c, c),
 "popup": lambda c: _r(10, 62, 100, 44, c, T(c)) + "".join(_r(18 + i * 32, 46, 20, 16, c, "#FFFFFF", 2) for i in range(3)) + _c(60, 30, 14, c) + _c(55, 27, 2, c, c, 1) + _c(65, 27, 2, c, c, 1) + _c(28, 84, 6, c, c) + _c(60, 84, 6, c, c) + _c(92, 84, 6, c, c),
 "ball": lambda c: _c(60, 60, 46, c, T(c)) + _c(60, 60, 18, c) + _p("M14 60 H42 M78 60 H106 M60 14 V42 M60 78 V106", c, sw=2),
 "paintbag": lambda c: _r(14, 18, 92, 84, c) + _p("M14 30 H106", c, sw=2) + _c(44, 62, 16, "#C1502E", "#C1502E55", 2) + _c(74, 72, 16, "#05668D", "#05668D55", 2) + _c(66, 50, 12, "#D4A017", "#D4A01755", 2) + _p("M6 18 h20 M94 18 h20 M6 102 h20 M94 102 h20", c, sw=5),
 "sticky": lambda c: _r(10, 10, 100, 100, c, T(c)) + _r(24, 26, 26, 22, c, "#FFFFFF", 2) + _p("M66 30 L92 34 L84 58 L62 52 Z", c, "#FFFFFF", 2) + _c(44, 80, 14, c, "#FFFFFF", 2) + _r(70, 70, 24, 26, c, "#FFFFFF", 2),
 "board": lambda c: _r(8, 12, 104, 96, c, T(c)) + _r(20, 24, 24, 16, c) + _p("M28 32 H40", c, sw=2) + _c(84, 36, 12, c) + _p("M84 26 V46 M74 36 H94", c, sw=2) + _r(22, 64, 22, 30, c) + _r(28, 72, 10, 10, c, c, 1) + _p("M62 66 V96 M70 66 V96 M78 66 V96 M86 66 V96", c, sw=2),
 "squares": lambda c: "".join(_r(14 + (i % 3) * 32, 14 + (i // 3) * 32, 28, 28, c, T(c) if (i % 2) else "#FFFFFF", 2) + (_p(f"M{18+(i%3)*32} {20+(i//3)*32} l20 16", c, sw=1.5) if i % 3 == 1 else "") for i in range(9)),
 "rainstick": lambda c: _p("M16 104 L104 16", c, sw=16) + _p("M16 104 L104 16", "#FFFFFF", sw=10) + "".join(_c(28 + i * 11, 92 - i * 11, 2.5, c, c, 1) for i in range(8)),
 "puppet": lambda c: _p("M30 110 V64 Q30 22 60 22 Q90 22 90 64 V110", c, T(c)) + _c(48, 54, 5, c, c) + _c(72, 54, 5, c, c) + _p("M48 76 Q60 86 72 76", c) + _p("M42 22 L36 8 M78 22 L84 8", c),
 "fruit": lambda c: _p("M14 80 Q14 46 40 46 Q66 46 64 80 Q60 104 38 104 Q16 102 14 80 Z", c, T(c)) + _c(86, 82, 22, c, "#FFFFFF") + _p("M80 30 Q88 10 104 8 Q100 28 80 30 Z M40 46 L42 34", c),
 "fish": lambda c: _r(8, 20, 104, 80, c) + _p("M30 60 Q48 38 72 60 Q48 82 30 60 Z M72 60 L88 48 V72 Z", c, T(c)) + _c(42, 58, 2.5, c, c, 1) + _c(92, 34, 4, c, "#FFFFFF", 2) + _c(98, 46, 3, c, "#FFFFFF", 2),
 "window": lambda c: _r(12, 10, 96, 100, c) + _p("M60 10 V110 M12 60 H108", c) + _c(36, 34, 8, c, T(c)) + _p("M70 96 h28 M74 96 l4 -10 h16 l4 10", c, sw=2) + _c(78, 98, 3, c, c) + _c(94, 98, 3, c, c),
 "blocks": lambda c: _r(18, 76, 32, 32, c, T(c)) + _r(54, 76, 32, 32, c) + _r(36, 42, 32, 32, c, T(c)) + _r(78, 18, 26, 26, c, "#FFFFFF") + _p("M70 30 L60 40", c, sw=2),
 "tent": lambda c: _p("M8 104 L60 14 L112 104 Z", c, T(c)) + _p("M60 14 V104 M60 54 L42 104 M60 54 L78 104", c) + _p("M4 104 H116", c),
 "book": lambda c: _p("M60 26 Q36 14 10 22 V100 Q36 92 60 104 Q84 92 110 100 V22 Q84 14 60 26 Z", c, T(c)) + _p("M60 26 V104", c),
 "books": lambda c: _r(14, 30, 22, 78, c, T(c)) + _r(38, 20, 20, 88, c) + _p("M62 34 L82 28 L102 104 L82 110 Z", c, T(c)) + _p("M8 108 H112", c),
 "music": lambda c: _p("M44 90 V24 L94 14 V80", c, sw=4) + _c(34, 90, 12, c, T(c)) + _c(84, 80, 12, c, T(c)) + _p("M44 40 L94 30", c, sw=4),
 "speech": lambda c: _p("M8 20 H70 V60 H34 L20 74 V60 H8 Z", c, T(c)) + _p("M112 50 H50 V90 H86 L100 104 V90 H112 Z", c) + t(39, 46, "\u3042", 18, c, "Hind", 600, "middle") + t(81, 77, "A", 18, c, "Khand", 700, "middle"),
 "speech2": lambda c: _p("M10 26 H110 V82 H52 L32 102 V82 H10 Z", c, T(c)) + t(40, 62, "\u3042", 18, c, "Hind", 600, "middle") + t(80, 62, "A", 18, c, "Khand", 700, "middle"),
 "sofa": lambda c: _r(20, 30, 80, 40, c, T(c)) + _r(8, 50, 104, 30, c) + _p("M14 80 V96 M106 80 V96", c) + _c(44, 42, 7, c, "#FFFFFF", 2) + _r(66, 36, 14, 14, c, "#FFFFFF", 2) + _p("M4 104 H116", c, sw=2),
 "steps": lambda c: _p("M8 104 L48 64 V104 Z", c, T(c)) + _r(48, 64, 30, 40, c) + _r(78, 40, 30, 64, c, T(c)),
 "hand": lambda c: _p("M40 104 V56 Q40 48 46 48 Q52 48 52 56 V30 Q52 22 58 22 Q64 22 64 30 V26 Q64 18 70 18 Q76 18 76 26 V34 Q76 28 82 28 Q88 28 88 36 V76 Q88 104 64 104 Z", c, T(c)) + _p("M100 30 Q108 40 100 50 M108 24 Q120 40 108 56", c, sw=2),
 "face": lambda c: _c(60, 60, 46, c, T(c)) + _c(44, 50, 6, c, c) + _c(76, 50, 6, c, c) + _c(60, 80, 10, c, "#FFFFFF"),
 "heart": lambda c: _p("M60 104 L18 62 Q4 44 18 30 Q38 14 60 38 Q82 14 102 30 Q116 44 102 62 Z", c, T(c)),
 "gate": lambda c: _p("M14 20 V108 M106 20 V108 M14 30 H106 M14 98 H106", c, sw=4) + "".join(_p(f"M{28+i*14} 30 V98", c, sw=2) for i in range(6)) + _r(52, 56, 16, 14, c, T(c), 2),
 "tub": lambda c: _p("M8 54 H112 V70 Q112 100 82 100 H38 Q8 100 8 70 Z", c, T(c)) + _p("M22 54 V24 Q22 14 32 14 Q42 14 42 24", c) + _c(76, 40, 7, c, "#FFFFFF", 2) + _c(92, 30, 5, c, "#FFFFFF", 2) + _p("M30 100 L26 110 M90 100 L94 110", c),
 "map": lambda c: _p("M8 24 L42 12 L78 24 L112 12 V96 L78 108 L42 96 L8 108 Z", c, T(c)) + _p("M42 12 V96 M78 24 V108", c, sw=2) + _p("M60 72 Q44 50 52 40 Q60 30 68 40 Q76 50 60 72 Z", c, "#FFFFFF") + _c(60, 46, 4, c, c),
 "bag": lambda c: _p("M18 40 H102 L96 110 H24 Z", c, T(c)) + _p("M42 40 V30 Q42 12 60 12 Q78 12 78 30 V40", c, sw=4),
}
