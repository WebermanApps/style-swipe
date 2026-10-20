"""Drawing kit for the five UpKeep follow-on decks (Oct 17 2026): square-corner 240x300 cards, white/cream base,
terracotta/lagoon/jungle accents, Khand/Hind. Drawn people (flat, faceless: no real people, no likenesses),
16:9 slide mockups, charts (all numbers are EXAMPLE DATA), phone/desktop frames, house map."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import math
from draft_svg import t, rect, dot, esc, crisp, ln, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
CREAM = "#FAF3EB"; CREAM2 = "#F4ECE0"; DEEP = "#A8431F"; GREY = "#8A8178"
SKIN = ["#8D5524", "#C68642", "#E0AC69", "#5C3A21", "#F1C27D", "#A86B3C"]
HAIR = ["#1F1A17", "#3B2A1E", "#14110F", "#6B4A2E", "#2B2118", "#4A3426"]

def card(label, acc, body, example=False, bg="#FFFFFF"):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">'
         + rect(0, 0, 240, 300, bg) + rect(0, 0, 240, 5, acc)
         + t(14, 22, label.upper(), 7.5, acc, "hind", 600, extra='letter-spacing="1.2"'))
    if example: s += ex_tag(226, 13)
    s += body + t(120, 297, "Built by Machan", 7.5, GREY, "hind", 400, "middle")
    return crisp(s + rect(.5, .5, 239, 299, "none", "#D6D0C6") + "</svg>")
def ex_tag(xr, y, txt="EXAMPLE DATA"):
    w = len(txt) * 4.7 + 10
    return rect(xr - w, y, w, 12, SAFFRON + "26", SAFFRON, 0, .8) + t(xr - w / 2, y + 8.6, txt, 7.5, "#7A5A0C", "hind", 600, "middle", 'letter-spacing=".5"')
def chip(x, y, s, c=INK, fill=None):
    w = len(s) * 4.6 + 12
    return rect(x, y, w, 15, fill or "#FFFFFF", c if not fill else "none", 0, .9) + t(x + w / 2, y + 10.4, s, 7.5, c if not fill else "#FFFFFF", "hind", 600, "middle"), w
def chips(y, items, x=14, c=INK):
    s = ""
    for it in items:
        g, w = chip(x, y, it, c); s += g; x += w + 5
    return s
def g(x, y, sc, inner): return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'
def sval(v): return f"{v:.1f}"

# ---------------- logo mark ----------------
def mark(cx, cy, r, c="#FFFFFF", bg=None):
    """Smart Upkeep roof-chevron mark in a circle (simplified)."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>' if bg else ""
    return s + f'<path d="M{cx-r*.62} {cy+r*.18} L{cx} {cy-r*.5} L{cx+r*.62} {cy+r*.18}" fill="none" stroke="{c}" stroke-width="{max(r*.28,.6):.2f}" stroke-linecap="round" stroke-linejoin="round"/><rect x="{cx-r*.3}" y="{cy+r*.05}" width="{r*.6}" height="{r*.42}" fill="{c}"/>'
def wordmark(x, y, size, c=INK, up=GREY, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-family="Khand" font-weight="700" fill="{c}" text-anchor="{anchor}">smart<tspan fill="{up}">up</tspan>keep</text>')

# ---------------- people ----------------
def person(skin=SKIN[0], hair=HAIR[0], hairstyle="short", polo=TERRA, collar=None, pants="#3D3A36", cargo=False, belt=True,
           shoe="boot", hat=None, hatc=TERRA, logo="left", logoc=None, patch=None, layer=None, layerc=LAGOON, back=False,
           sleeve_logo=False, covers=None):
    """Flat faceless tech figure, local box 100 x 240 (feet at 236)."""
    collar = collar or polo
    lc = logoc or ("#FFFFFF" if polo not in ("#FFFFFF", "#F7F7F7") else TERRA)
    o = '<ellipse cx="50" cy="237" rx="30" ry="3.5" fill="#00000014"/>'
    # legs
    o += f'<path d="M32 116 H49.5 L48.5 226 H35 Z" fill="{pants}"/><path d="M50.5 116 H68 L65 226 H51.5 Z" fill="{pants}"/>'
    o += f'<path d="M49.5 122 L50 200" stroke="#00000022" stroke-width="1"/>'
    if cargo: o += rect(29.5, 152, 7, 16, "#00000018", "#00000030", 0, .6) + rect(63.5, 152, 7, 16, "#00000018", "#00000030", 0, .6)
    # shoes
    if covers:
        o += f'<path d="M31 222 Q30 236 41 236 Q52 236 50 222 Z" fill="{covers}"/><path d="M50 222 Q49 236 60 236 Q71 236 69 222 Z" fill="{covers}"/>'
        o += f'<path d="M33 226 H48 M52 226 H67" stroke="#FFFFFF88" stroke-width="1"/>'
    elif shoe == "boot":
        o += f'<path d="M33 214 H49 V230 Q49 236 43 236 H29 Q27 236 28 232 L33 226 Z" fill="#6B4A2E"/><path d="M51 214 H67 L67 226 L72 232 Q73 236 71 236 H57 Q51 236 51 230 Z" fill="#6B4A2E"/>'
        o += f'<path d="M37 218 H46 M37 222 H46 M54 218 H63 M54 222 H63" stroke="#E8D9C4" stroke-width=".9"/>' + rect(27.5, 233.5, 22, 2.5, "#2B2118") + rect(51, 233.5, 22, 2.5, "#2B2118")
    else:
        o += f'<path d="M34 224 H49 V232 Q49 235 46 235 H30 Q28 235 29 231 Z" fill="#26313A"/><path d="M51 224 H66 L71 231 Q72 235 70 235 H54 Q51 235 51 232 Z" fill="#26313A"/>'
        o += rect(28.5, 233, 21, 3, "#FFFFFF", "#C9C2B6", 0, .5) + rect(50.5, 233, 21, 3, "#FFFFFF", "#C9C2B6", 0, .5) + f'<path d="M36 228 H45 M55 228 H64" stroke="{TERRA}" stroke-width="1.2"/>'
    long = layer in ("softshell", "quarterzip", "rain")
    top = layerc if long else polo
    # arms (skin) and sleeves
    if long:
        o += f'<path d="M29 50 L13 114 L22 118 L34 66 Z" fill="{top}"/><path d="M71 50 L87 114 L78 118 L66 66 Z" fill="{top}"/>'
        o += f'<circle cx="17" cy="120" r="4.6" fill="{skin}"/><circle cx="83" cy="120" r="4.6" fill="{skin}"/>'
        o += f'<path d="M14 110 L22 113 M86 110 L78 113" stroke="#00000030" stroke-width="2"/>'
    else:
        o += f'<path d="M18 82 L12 117 L19 119 L27 87 Z" fill="{skin}"/><path d="M82 82 L88 117 L81 119 L73 87 Z" fill="{skin}"/>'
        o += f'<circle cx="15.5" cy="121" r="4.6" fill="{skin}"/><circle cx="84.5" cy="121" r="4.6" fill="{skin}"/>'
        o += f'<path d="M30 50 L15 82 L27 88 L33 66 Z" fill="{polo}"/><path d="M70 50 L85 82 L73 88 L67 66 Z" fill="{polo}"/>'
        o += f'<path d="M15.5 81 L27 86.5 M84.5 81 L73 86.5" stroke="{collar}" stroke-width="2.2"/>'
    # neck + torso
    o += rect(45, 34, 10, 14, skin)
    o += f'<path d="M30 50 Q50 43 70 50 L71 118 L29 118 Z" fill="{top}"/>'
    if polo in ("#FFFFFF", "#F7F7F7") and not long: o += f'<path d="M30 50 Q50 43 70 50 L71 118 L29 118 Z" fill="none" stroke="#D9D2C6" stroke-width=".8"/>'
    if layer == "vest":
        o += f'<path d="M31 51 Q40 47 44 47 L50 70 L56 47 Q60 47 69 51 L71 118 L29 118 Z" fill="{layerc}"/><path d="M50 70 V118" stroke="#00000040" stroke-width=".9"/>'
        o += rect(56, 92, 9, 2, "#00000035") + rect(35, 92, 9, 2, "#00000035")
    if layer == "softshell":
        o += f'<path d="M44 47 L50 47 L56 47 L54 118 H46 Z" fill="{polo}"/><path d="M44 47 L46 118 M56 47 L54 118" stroke="#00000045" stroke-width="1"/>'
        o += f'<path d="M38 47 L44 47 L47 62 L40 58 Z M62 47 L56 47 L53 62 L60 58 Z" fill="{layerc}" stroke="#00000030" stroke-width=".6"/>'
    if layer == "quarterzip":
        o += f'<path d="M41 44 Q50 41 59 44 L59 50 Q50 48 41 50 Z" fill="{layerc}" stroke="#00000030" stroke-width=".7"/><path d="M50 46 V66" stroke="#D8D2C8" stroke-width="1.3"/>'
    if layer == "rain":
        o += f'<path d="M36 48 Q34 30 50 26 Q66 30 64 48 Z" fill="{layerc}" opacity=".85"/><path d="M50 47 V118" stroke="#FFFFFF88" stroke-width="1.2"/>'
        o += rect(33, 95, 12, 2, "#FFFFFF66") + rect(55, 95, 12, 2, "#FFFFFF66")
    if not back and not long:
        o += f'<path d="M43 46 L50 56 L45 61 L37.5 50 Z" fill="{collar}"/><path d="M57 46 L50 56 L55 61 L62.5 50 Z" fill="{collar}"/>'
        o += rect(48.6, 56, 2.8, 13, "#00000018") + dot(50, 60, .9, "#FFFFFFAA") + dot(50, 65, .9, "#FFFFFFAA")
        if polo in ("#FFFFFF", "#F7F7F7"): o += f'<path d="M43 46 L50 56 L45 61 L37.5 50 Z M57 46 L50 56 L55 61 L62.5 50 Z" fill="none" stroke="#C9C2B6" stroke-width=".5"/>'
    if belt and layer not in ("rain",):
        o += rect(30, 113, 40, 5.5, "#2A2522") + rect(47.5, 113.6, 5, 4.3, "none", "#C9B48A", 0, .8)
    # chest logo / patch
    lx = {"left": 60, "right": 40, "center": 50}
    showtop = (not long) or layer == "softshell"
    if not back and logo in lx:
        if long and layer != "softshell": o += mark(60, 68, 3.6, "#FFFFFF")
        elif showtop and layer != "softshell": o += mark(lx[logo], 68 if logo != "center" else 74, 3.6 if logo != "center" else 6.5, lc)
        elif layer == "softshell": o += mark(62, 68, 3.4, "#FFFFFF")
    if sleeve_logo and not long: o += mark(79, 73, 2.6, lc)
    if patch == "patch" and not back and not long:
        px = 40 if logo != "right" else 60
        o += f'<ellipse cx="{px}" cy="68" rx="6.2" ry="3.4" fill="#FFFFFF" stroke="{TERRA if polo != TERRA else "#FFFFFF"}" stroke-width=".9"/><path d="M{px-3.5} 68 H{px+3.5}" stroke="{INK}" stroke-width=".9"/>'
    if patch == "printed" and not back and not long:
        o += f'<path d="M{55} 75 H{65}" stroke="{lc}" stroke-width="1.3"/>'
    if back and logo != "none":
        o += mark(50, 66, 8, lc) + f'<text x="50" y="86" font-size="6.2" font-family="Khand" font-weight="700" fill="{lc}" text-anchor="middle">SMART UPKEEP</text>'
    # head
    o += f'<ellipse cx="44" cy="24" rx="2.2" ry="3.2" fill="{skin}"/><ellipse cx="56" cy="24" rx="2.2" ry="3.2" fill="{skin}"/>' if not back else ""
    o += f'<ellipse cx="50" cy="22" rx="11.5" ry="13.5" fill="{skin}"/>'
    if back: o += f'<ellipse cx="50" cy="21" rx="11.8" ry="13.6" fill="{hair}"/>'
    elif hat is None:
        if hairstyle == "short": o += f'<path d="M38.5 21 Q38 7 50 7.5 Q62 7 61.5 21 Q60 13 50 13.5 Q41 13 38.5 21 Z" fill="{hair}"/>'
        elif hairstyle == "bun": o += f'<circle cx="50" cy="6" r="5" fill="{hair}"/><path d="M38.5 22 Q38 8 50 8.5 Q62 8 61.5 22 Q60 14 50 14.5 Q41 14 38.5 22 Z" fill="{hair}"/>'
        elif hairstyle == "pony": o += f'<path d="M38.5 22 Q38 8 50 8.5 Q62 8 61.5 22 Q60 14 50 14.5 Q41 14 38.5 22 Z" fill="{hair}"/><path d="M60 14 Q68 20 63 34" fill="none" stroke="{hair}" stroke-width="4" stroke-linecap="round"/>'
        elif hairstyle == "curly": o += "".join(f'<circle cx="{40+i*4}" cy="{10+(i%2)*2}" r="4" fill="{hair}"/>' for i in range(6)) + f'<path d="M38.5 21 Q38 12 41 11 L59 11 Q62 12 61.5 21 Q58 15 50 15 Q42 15 38.5 21 Z" fill="{hair}"/>'
    if hat == "cap":
        o += f'<path d="M38 18 Q38 6 50 6 Q62 6 62 18 Z" fill="{hatc}"/><ellipse cx="50" cy="18.5" rx="15" ry="3.2" fill="{hatc}"/><path d="M36 18.5 Q50 22.5 64 18.5" fill="none" stroke="#00000035" stroke-width=".8"/>'
        o += mark(50, 12.5, 2.7, "#FFFFFF" if hatc not in ("#FFFFFF",) else TERRA)
        if hatc == "#FFFFFF": o += f'<path d="M38 18 Q38 6 50 6 Q62 6 62 18 Z" fill="none" stroke="#C9C2B6" stroke-width=".6"/>'
    if hat == "beanie":
        o += f'<path d="M38 19 Q37 3 50 3 Q63 3 62 19 Z" fill="{hatc}"/>' + rect(37.5, 14, 25, 6.5, hatc, "#00000030", 0, .6) + mark(50, 17.2, 2.2, "#FFFFFF")
    if hat == "brim":
        o += f'<ellipse cx="50" cy="15" rx="19" ry="4.2" fill="{hatc}"/><path d="M40 15 Q40 3 50 3 Q60 3 60 15 Z" fill="{hatc}"/><path d="M40 12 H60" stroke="{TERRA}" stroke-width="1.6"/>'
    return o

def scene(x, y, w, h, wall=CREAM, door=LAGOON):
    """Front-door backdrop for people shots."""
    s = rect(x, y, w, h, wall) + rect(x, y + h * .86, w, h * .14, "#E9DFCF")
    dw = w * .3; dx = x + w * .62
    s += rect(dx, y + h * .18, dw, h * .68, door) + rect(dx + dw * .14, y + h * .26, dw * .72, h * .2, "#FFFFFF33") + dot(dx + dw * .18, y + h * .55, 1.4, SAFFRON)
    s += rect(dx - 4, y + h * .15, dw + 8, 4, "#FFFFFF") + rect(dx - 6, y + h * .86, dw + 12, 4, "#D9CBB5")
    s += rect(x + w * .08, y + h * .22, w * .26, h * .22, "#FFFFFF", "#E2D5C1", 0, 1) + f'<path d="M{x+w*.21} {y+h*.22} V{y+h*.44} M{x+w*.08} {y+h*.33} H{x+w*.34}" stroke="#E2D5C1"/>'
    return s
def shot(x, y, w, h, people, wall=CREAM, door=LAGOON, sc=None):
    """people: list of person-kwargs dicts, placed side by side, feet on the floor."""
    s = f'<clipPath id="cp{int(x)}{int(y)}{int(w)}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#cp{int(x)}{int(y)}{int(w)})">' + scene(x, y, w, h, wall, door)
    n = len(people); sc = sc or min(h * .9 / 240, w / (n * 100) * .95)
    tot = n * 100 * sc; x0 = x + (w - tot) / 2
    for i, p in enumerate(people):
        s += g(x0 + i * 100 * sc, y + h * .965 - 240 * sc, sc, person(**p))
    return s + "</g>" + rect(x, y, w, h, "none", LINE, 0, 1)
def closeup(x, y, w, h, inner_fn, bg=CREAM):
    return rect(x, y, w, h, bg) + inner_fn(x, y, w, h) + rect(x, y, w, h, "none", LINE)
def dots_ind(cx, y, n, cur, c=TERRA):
    x0 = cx - (n - 1) * 5
    return "".join((rect(x0 + i * 10 - 5, y - 1.5, 10, 3, c) if i == cur else dot(x0 + i * 10, y, 1.8, "#CFC6B4")) for i in range(n))
def counter(x, y, s):
    w = len(s) * 4.6 + 10
    return rect(x - w, y, w, 13, "#FFFFFFE6", LINE, 0, .6) + t(x - w / 2, y + 9.2, s, 7.5, INK, "hind", 600, "middle")
def arrow_btn(x, y, left=True):
    return f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFFE6" stroke="{LINE}"/>' + f'<path d="M{x+(2 if left else -2)} {y-3.5} L{x+(-2 if left else 2)} {y} L{x+(2 if left else -2)} {y+3.5}" fill="none" stroke="{INK}" stroke-width="1.4"/>'

# ---------------- slides ----------------
def slide(x, y, w, inner, bg="#FFFFFF", border=LINE):
    """16:9 slide; inner drawn on a 320x180 canvas."""
    h = w * 9 / 16; sc = w / 320
    cid = f"sl{int(x)}{int(y)}{int(w)}"
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h:.1f}"/></clipPath><g clip-path="url(#{cid})">' + rect(x, y, w, h, bg)
            + g(x, y, round(sc, 4), inner) + "</g>" + rect(x, y, w, h, "none", border, 0, 1))
def stitle(s, x=20, y=34, size=22, c=INK): return t(x, y, s, size, c, "khand")
def ssub(s, x=20, y=50, size=10, c=MUTE): return t(x, y, s, size, c)
def sfoot(n, c=MUTE): return t(300, 170, str(n), 8, c, "hind", 600, "end") + wordmark(20, 171, 10, INK, GREY)
def deck_strip(x, y, w, n, hi, labels=None, c=TERRA):
    s, bw = "", (w - (n - 1) * 3) / n; bh = bw * 9 / 16
    for i in range(n):
        xx = x + i * (bw + 3); on = i in (hi if isinstance(hi, (list, tuple)) else [hi])
        s += rect(xx, y, bw, bh, c if on else "#FFFFFF", c if on else "#CFC6B4", 0, .8)
        s += rect(xx + bw * .15, y + bh * .3, bw * .5, 1.6, "#FFFFFF" if on else "#CFC6B4") + rect(xx + bw * .15, y + bh * .55, bw * .35, 1.2, "#FFFFFFAA" if on else "#E2DCD0")
    if labels:
        for i, lb in labels: s += t(x + i * (bw + 3) + bw / 2, y + bh + 10, lb, 7.5, c, "hind", 600, "middle")
    return s

# ---------------- charts (EXAMPLE DATA) ----------------
def axes(x, y, w, h, c="#D9D2C6", ticks=None):
    s = f'<path d="M{x} {y} V{y+h} H{x+w}" fill="none" stroke="{c}" stroke-width=".9"/>'
    for i in range(1, 4): s += f'<path d="M{x} {y+h*i/4:.1f} H{x+w}" stroke="#EFEAE2" stroke-width=".6"/>'
    if ticks:
        for i, lb in enumerate(ticks): s += t(x + w * i / (len(ticks) - 1), y + h + 9, lb, 7.5, MUTE, "hind", 400, "middle")
    return s
def pts(x, y, w, h, vals, vmax):
    n = len(vals); return [(x + w * i / (n - 1), y + h - h * v / vmax) for i, v in enumerate(vals)]
def pl(p): return " ".join(f"{a:.1f},{b:.1f}" for a, b in p)
def line(x, y, w, h, vals, vmax, c=TERRA, sw=2, dash=None):
    return f'<polyline points="{pl(pts(x,y,w,h,vals,vmax))}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>"
def area(x, y, w, h, lo, hi, vmax, c):
    a = pts(x, y, w, h, hi, vmax); b = pts(x, y, w, h, lo, vmax)[::-1]
    return f'<polygon points="{pl(a + b)}" fill="{c}"/>'
def stacked(x, y, w, h, series, cols, vmax):
    s, base = "", [0] * len(series[0])
    for ser, c in zip(series, cols):
        top = [b + v for b, v in zip(base, ser)]; s += area(x, y, w, h, base, top, vmax, c); base = top
    return s
def bars(x, y, w, h, vals, vmax, c=LAGOON, hi=None, gap=.3):
    n = len(vals); bw = w / n; s = ""
    for i, v in enumerate(vals):
        s += rect(x + i * bw + bw * gap / 2, y + h - h * v / vmax, bw * (1 - gap), h * v / vmax, c if (hi is None or i == hi) else c + "66")
    return s
def spark(x, y, w, h, vals, c=JUNGLE):
    vmax = max(vals) * 1.05; vmin = min(vals) * .9
    p = [(x + w * i / (len(vals) - 1), y + h - h * (v - vmin) / (vmax - vmin)) for i, v in enumerate(vals)]
    return f'<polyline points="{pl(p)}" fill="none" stroke="{c}" stroke-width="1.4" stroke-linejoin="round"/>' + dot(p[-1][0], p[-1][1], 1.8, c)
def kpi(x, y, w, h, val, lab, c=INK, sp=None, sc=JUNGLE):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 0, .9) + t(x + 6, y + h * .5 + 2, val, min(15, h * .45), c, "khand") + t(x + 6, y + h - 5, lab, 7.5, MUTE)
    if sp: s += spark(x + w * .58, y + 5, w * .36, h * .36, sp, sc)
    return s

# ---------------- frames ----------------
def phone(x, y, w, inner_h, inner, sc):
    """Phone frame; inner drawn at local width w/sc."""
    h = inner_h * sc + 16
    cid = f"ph{int(x)}{int(y)}"
    return (rect(x - 4, y - 8, w + 8, h + 8, INK, "none", 0) + f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h-16}"/></clipPath>'
            + rect(x, y, w, h - 16, "#FFFFFF") + f'<g clip-path="url(#{cid})">' + g(x, y, sc, inner) + "</g>" + rect(x + w / 2 - 8, y - 5, 16, 2.5, "#444"))
def browser(x, y, w, h, inner, sc):
    cid = f"br{int(x)}{int(y)}"
    return (rect(x, y, w, h, "#FFFFFF", "#BDB6AA", 0, 1) + rect(x, y, w, 9, "#EFEAE2") + dot(x + 5, y + 4.5, 1.6, TERRA) + dot(x + 10, y + 4.5, 1.6, SAFFRON) + dot(x + 15, y + 4.5, 1.6, JUNGLE)
            + rect(x + 22, y + 2.5, w * .5, 4, "#FFFFFF") + f'<clipPath id="{cid}"><rect x="{x}" y="{y+9}" width="{w}" height="{h-9}"/></clipPath><g clip-path="url(#{cid})">' + g(x, y + 9, sc, inner) + "</g>")

# ---------------- icons (24 grid) ----------------
def icon(kind, x, y, s=16, c=INK, sw=1.8):
    P = {
     "furnace": f'<rect x="5" y="3" width="14" height="18" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8 15 Q10 11 12 14 Q14 10 16 15" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8 7 H16" stroke="{c}" stroke-width="{sw}"/>',
     "ac": f'<rect x="3" y="6" width="18" height="13" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="12.5" r="4" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 9 V16 M9 12.5 H15" stroke="{c}" stroke-width="1.2"/>',
     "waterheater": f'<rect x="7" y="3" width="10" height="18" rx="4" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="16" r="1.8" fill="{c}"/><path d="M10 7 H14" stroke="{c}" stroke-width="{sw}"/>',
     "dryer": f'<rect x="4" y="3" width="16" height="18" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="13" r="4.5" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M7 6 H10" stroke="{c}" stroke-width="{sw}"/>',
     "detector": f'<circle cx="12" cy="12" r="8" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="12" r="2.5" fill="{c}"/><path d="M5 5 Q3 8 4 11 M19 5 Q21 8 20 11" fill="none" stroke="{c}" stroke-width="1.3"/>',
     "meter": f'<rect x="7" y="2" width="10" height="20" fill="none" stroke="{c}" stroke-width="{sw}"/><rect x="9" y="5" width="6" height="5" fill="{c}"/><path d="M12 22 V24" stroke="{c}" stroke-width="{sw}"/><path d="M10 14 H14 M10 17 H13" stroke="{c}" stroke-width="1.3"/>',
     "gutter": f'<path d="M3 9 L12 3 L21 9" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M2 11 H22 V13 H2 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M19 13 V21" stroke="{c}" stroke-width="{sw}"/><path d="M16 20 Q17 23 19 21" fill="none" stroke="{c}" stroke-width="1.3"/>',
     "roof": f'<path d="M2 13 L12 4 L22 13" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M5 11 V20 H19 V11" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M16 6 V9" stroke="{c}" stroke-width="{sw}"/>',
     "storm": f'<path d="M6 14 A5 5 0 0 1 8 5 A6 6 0 0 1 19 8 A4 4 0 0 1 18 15 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 15 L10 19 H13 L11 23" fill="none" stroke="{c}" stroke-width="1.6"/>',
     "garage": f'<path d="M2 10 L12 4 L22 10 V21 H2 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M6 21 V12 H18 V21 M6 15 H18 M6 18 H18" fill="none" stroke="{c}" stroke-width="1.2"/>',
     "filter": f'<rect x="4" y="4" width="16" height="16" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M4 9 H20 M4 14 H20 M9 4 V20 M14 4 V20" stroke="{c}" stroke-width="1"/>',
     "valve": f'<circle cx="12" cy="8" r="4" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 12 V16 M3 18 H21" stroke="{c}" stroke-width="{sw}"/><path d="M3 16 V20 M21 16 V20" stroke="{c}" stroke-width="{sw}"/>',
     "drop": f'<path d="M12 3 Q19 12 18 15 A6 6 0 0 1 6 15 Q5 12 12 3 Z" fill="none" stroke="{c}" stroke-width="{sw}"/>',
     "report": f'<rect x="5" y="3" width="14" height="18" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8 8 H16 M8 12 H16 M8 16 H13" stroke="{c}" stroke-width="1.4"/>',
     "generator": f'<rect x="3" y="7" width="18" height="12" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 9 L9 14 H12 L10 18" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M6 19 V21 M18 19 V21" stroke="{c}" stroke-width="{sw}"/>',
     "lawn": f'<path d="M2 20 H22" stroke="{c}" stroke-width="{sw}"/><path d="M5 20 L6 13 M8 20 L8 11 M11 20 L12 14 M14 20 L14 10 M17 20 L18 13 M20 20 L19 15" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
     "shield": f'<path d="M12 3 L20 6 V12 Q20 18 12 21 Q4 18 4 12 V6 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8.5 12 L11 14.5 L15.5 9.5" fill="none" stroke="{c}" stroke-width="1.6"/>',
     "x": f'<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8.5 8.5 L15.5 15.5 M15.5 8.5 L8.5 15.5" stroke="{c}" stroke-width="1.6"/>',
     "id": f'<rect x="3" y="5" width="18" height="14" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="9" cy="11" r="2.4" fill="none" stroke="{c}" stroke-width="1.4"/><path d="M5.5 16.5 Q9 13 12.5 16.5 M14 10 H19 M14 13 H18" fill="none" stroke="{c}" stroke-width="1.3"/>',
     "pin": f'<path d="M12 22 Q5 14 5 9.5 A7 7 0 0 1 19 9.5 Q19 14 12 22 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="9.5" r="2.5" fill="{c}"/>',
     "star": f'<path d="M12 3 L14.6 9 L21 9.5 L16 13.6 L17.6 20 L12 16.5 L6.4 20 L8 13.6 L3 9.5 L9.4 9 Z" fill="{c}" stroke="{c}" stroke-width="1" stroke-linejoin="round"/>',
     "bell": f'<path d="M6 17 V11 A6 6 0 0 1 18 11 V17 L20 19 H4 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M10 21 H14" stroke="{c}" stroke-width="{sw}"/>',
     "map": f'<path d="M3 6 L9 4 L15 6 L21 4 V18 L15 20 L9 18 L3 20 Z M9 4 V18 M15 6 V20" fill="none" stroke="{c}" stroke-width="1.5"/>',
     "list": f'<path d="M8 6 H21 M8 12 H21 M8 18 H21" stroke="{c}" stroke-width="{sw}"/><circle cx="4" cy="6" r="1.4" fill="{c}"/><circle cx="4" cy="12" r="1.4" fill="{c}"/><circle cx="4" cy="18" r="1.4" fill="{c}"/>',
     "search": f'<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M15.5 15.5 L21 21" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
     "check": f'<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M7.5 12.5 L10.5 15.5 L16.5 9" fill="none" stroke="{c}" stroke-width="1.8"/>',
     "cal": f'<rect x="3" y="5" width="18" height="16" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M3 10 H21 M8 3 V7 M16 3 V7" stroke="{c}" stroke-width="{sw}"/>',
     "refund": f'<path d="M4 12 A8 8 0 1 0 7 6" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M4 3 V8 H9" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 8 V16 M10 10 H13.5 A1.5 1.5 0 0 1 13.5 13 H10.5 A1.5 1.5 0 0 0 10.5 16 H14" fill="none" stroke="{c}" stroke-width="1.2"/>',
     "bulb": f'<path d="M9 17 V15 Q5 12 6 8 A6 6 0 0 1 18 8 Q19 12 15 15 V17 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M9 20 H15" stroke="{c}" stroke-width="{sw}"/>',
     "snow": f'<path d="M12 3 V21 M4 7.5 L20 16.5 M20 7.5 L4 16.5" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
     "leaf": f'<path d="M5 19 Q4 6 19 5 Q20 18 5 19 Z M5 19 L14 10" fill="none" stroke="{c}" stroke-width="{sw}"/>',
     "sun": f'<circle cx="12" cy="12" r="4.5" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 2 V5 M12 19 V22 M2 12 H5 M19 12 H22 M5 5 L7 7 M17 17 L19 19 M19 5 L17 7 M5 19 L7 17" stroke="{c}" stroke-width="1.5"/>',
     "flower": f'<circle cx="12" cy="9" r="2.5" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 6.5 Q12 2 14.5 4 Q16 6.5 12 6.5 M12 11.5 V21 M12 17 Q8 14 7 16" fill="none" stroke="{c}" stroke-width="1.5"/>',
    }
    return f'<g transform="translate({x},{y}) scale({s/24:.4f})">{P[kind]}</g>'

def zoom(x, y, w, h, p, fy=70, sc=2.2, bg=CREAM, cap=None):
    """Close-up crop of a person: local point (50, fy) centered in the box."""
    cid = f"zm{int(x)}{int(y)}{int(w)}{int(h)}"
    s = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">' + rect(x, y, w, h, bg)
    s += g(x + w / 2 - 50 * sc, y + h / 2 - fy * sc, sc, person(**p)) + "</g>" + rect(x, y, w, h, "none", LINE)
    if cap: s += rect(x, y + h - 14, w, 14, "#FFFFFFE6") + t(x + 5, y + h - 4, cap, 7.5, INK, "hind", 600)
    return s
