"""Tech graphics decks, Oct 18 2026 (asked 22:30 ICT: "i want decks for the graphics of the technicians").
Two this-or-that decks, 10 picks each, Notes on every card, light only, Khand headings + Hind body, phone-first, about how the
TECHNICIANS are drawn in the investor pitch and brand graphics (not the tech app). Every option is a hand-built SVG mockup of an
illustrated tech (never a photo or a real person), drawn from the round-2 pitch figures (pitch-v3-1018 r2 figs.py): terracotta or
lagoon polo, left-chest logo, charcoal pants, sneakers for good weather and boots for bad weather, both under terracotta reusable
shoe covers with the logo, always clearly visible. Fixed picks from the earlier uniform decks are drawn in, never re-asked.
Palette: terracotta #C1502E, lagoon #05668D, jungle #0B6E4F, warm cream. Picks are logged only, never applied automatically."""
import math
from md1018_kit import *
from draft_svg import crisp
CREAM = "#FAF6EE"; CR2 = "#F3EBDD"; CH = "#3b3d40"; CHD = "#2c2e31"; KHAKI = "#B8A37E"; WHITE = "#FFFFFF"
LOGO = """<path d="M84.4 243.2Q84.4 227.2 94.1 219.1Q103.8 211 125.4 211Q140.2 211 149.8 214V240.6Q140.8 237.6 130.1 237.6Q119.4 237.6 116.5 239.4Q113.6 241.2 113.6 245.2V246.8Q113.6 249.2 115.1 250.9Q116.6 252.6 121.6 256L137.8 266.8Q145.4 271.8 149.5 277.8Q153.6 283.8 153.6 292.8V297.8Q153.6 331 110 331Q94.8 331 84 328.4V301.4Q93.4 304.2 104.8 304.2Q116.2 304.2 119.9 302.3Q123.6 300.4 123.6 296.6V294.8Q123.6 291.8 121.6 290Q119.2 287.6 98.6 274Q84.4 264.4 84.4 248.4Z M235.8 218.2Q248.8 211.4 261.3 211.4Q273.8 211.4 280.7 217.7Q287.6 224 287.6 236.6V330H257V244Q257 239.2 251.7 239.2Q246.4 239.2 242 241.8Q242.2 242.2 242.2 243.8V330H211.6V244Q211.6 239.2 206.4 239.2Q201.2 239.2 196.8 241.8V330H166.6V212H195V217.2Q205.6 211.4 217.3 211.4Q229 211.4 235.8 218.2Z M329 295.8V301.4Q329 308.2 336 308.2Q342 308.2 346 306V281.8L336.8 284.2Q331.8 285.6 330.4 287.8Q329 290 329 295.8ZM305.6 214.8Q316.6 211 337 211Q357.4 211 366.2 219.9Q375 228.8 375 246.8V330H346.8V321.4Q341 330.4 326.6 330.4Q312.2 330.4 305.8 323.5Q299.4 316.6 299.4 301.4V294.6Q299.4 281.2 305.3 274Q311.2 266.8 324.4 263.2L346.2 257.6V246.6Q346 241.4 343.2 239.3Q340.4 237.2 333 237.2Q316.4 237.2 305.6 241.4Z M443 211.4H446.4V239.2H441.8Q430.6 239.2 422.2 243.2V330H392V212H420.4V220Q430.6 213.8 434.7 212.6Q438.8 211.4 443 211.4Z M496.8 304.6Q503 304.6 508.2 301.8V328.6Q501.4 331.8 490.4 331.8Q473.4 331.8 466.2 323.8Q459 315.8 459 300.6V237.4H448.4V212H460.4L469.6 191.6H489.2V212H507V237.4H489.2V297.4Q489.2 304.6 496.8 304.6Z" fill="#0A0A0A"/><path d="M577.4 212H607.6V330H579.2V324.6Q569.4 330 556.9 330Q544.4 330 537.8 323.2Q531.2 316.4 531.2 303.6V212H561.8V297.6Q561.8 302.8 567.6 302.8Q573.4 302.8 577.4 300.4Z M671.6 244Q671.6 239.2 665.9 239.2Q660.2 239.2 655.8 241.8V302.2H663.8Q671.6 302.2 671.6 295.8ZM654 217.2Q664.6 211.4 676.5 211.4Q688.4 211.4 695.3 217.7Q702.2 224 702.2 236.6V300.6Q702.2 315.6 693.9 322.8Q685.6 330 671.6 330H655.8V359.8H625.6V212H654Z" fill="#737373"/><polyline points="519.2,188 616.2,132 713.2,188" fill="none" stroke="#C1502E" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/><path d="M759.4 330H730.2V180.6H759.4V261L774.2 212H804L787 267.8L807 330H775.4L759.4 272Z M815 296.4V242.2Q815 227 824.4 218.5Q833.8 210 852.8 210Q889.4 210 889.4 242.2V282.8H844V294Q844 300 847.3 302.5Q850.6 305 861.9 305Q873.2 305 886.6 301V327.4Q872.6 331.2 856.6 331.2Q815 331.2 815 296.4ZM844 259.8H861.6V242.6Q861.6 235 852.8 235Q844 235 844 242.6Z M901.4 296.4V242.2Q901.4 227 910.8 218.5Q920.2 210 939.2 210Q975.8 210 975.8 242.2V282.8H930.4V294Q930.4 300 933.7 302.5Q937 305 948.3 305Q959.6 305 973 301V327.4Q959 331.2 943 331.2Q901.4 331.2 901.4 296.4ZM930.4 259.8H948V242.6Q948 235 939.2 235Q930.4 235 930.4 242.6Z M1035.8 244Q1035.8 239.2 1030.1 239.2Q1024.4 239.2 1020 241.8V302.2H1028Q1035.8 302.2 1035.8 295.8ZM1018.2 217.2Q1028.8 211.4 1040.7 211.4Q1052.6 211.4 1059.5 217.7Q1066.4 224 1066.4 236.6V300.6Q1066.4 315.6 1058.1 322.8Q1049.8 330 1035.8 330H1020V359.8H989.8V212H1018.2Z" fill="#0A0A0A"/>"""
_n = [0]
def uid(p="g"):
    _n[0] += 1; return f"tg{p}{_n[0]}"
def darker(h, f=.8):
    h = h.lstrip("#"); r, g, b = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))
def lighter(h, f=.25):
    h = h.lstrip("#"); r, g, b = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * f) for v in (r, g, b))
class Ctx:
    """One card's drawing context: unique ids, logo symbols, outline + shading switches."""
    def __init__(self, outline=0.0, soft=True):
        self.outline = outline; self.soft = soft; self.k = uid("c")
        self.lg = self.k + "l"; self.lgw = self.k + "w"; self.sh = self.k + "s"; self.fl = self.k + "f"; self.hl = self.k + "h"
    def defs(self):
        import re
        wh = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="#fff"', LOGO).replace('stroke="#C1502E"', 'stroke="#fff"')
        return (f'<defs><symbol id="{self.lg}" viewBox="70 118 1010 250">{LOGO}</symbol><symbol id="{self.lgw}" viewBox="70 118 1010 250">{wh}</symbol>'
                f'<linearGradient id="{self.sh}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".22"/><stop offset=".38" stop-color="#fff" stop-opacity=".16"/>'
                f'<stop offset=".72" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".26"/></linearGradient>'
                f'<radialGradient id="{self.fl}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
                f'<radialGradient id="{self.hl}" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>')
    def logo(self, x, y, w, white=True):
        return f'<use href="#{self.lgw if white else self.lg}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{w * 250 / 1010:.1f}"/>'
    def st(self):
        return f' stroke="{INK}" stroke-width="{self.outline}" stroke-linejoin="round"' if self.outline else ""
    def P(self, d, fill, extra="", shade=False):
        s = f'<path d="{d}" fill="{fill}"{self.st()} {extra}/>'
        if shade and self.soft: s += f'<path d="{d}" fill="url(#{self.sh})"/>'
        return s
    def limb(self, pts, w, col, cap="round"):
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        s = ""
        if self.outline: s += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * self.outline:.1f}" stroke-linecap="{cap}" stroke-linejoin="round"/>'
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="{cap}" stroke-linejoin="round"/>'
        if self.soft: s += f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".13" stroke-width="{w * .35:.1f}" stroke-linecap="{cap}" transform="translate({w * .28:.1f},0)"/>'
        return s
    def shadow(self, cx, cy, rx, ry=6):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{self.fl})"/>' if self.soft else f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * .8:.1f}" ry="{ry * .7:.1f}" fill="#000" opacity=".08"/>'
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def perp(a, b, t, half):
    p = lerp(a, b, t); dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L * half, dx / L * half
    return (p[0] + nx, p[1] + ny), (p[0] - nx, p[1] - ny)
def mirp(d):
    import re
    t = re.findall(r"[A-Za-z]|-?\d+\.?\d*", d); o = []; k = 0; cmd = None
    while k < len(t):
        if t[k].isalpha(): cmd = t[k]; o.append(cmd); k += 1; continue
        if cmd == "H": o.append(f"{200 - float(t[k]):.1f}"); k += 1
        elif cmd == "V": o.append(t[k]); k += 1
        else: o.append(f"{200 - float(t[k]):.1f}"); o.append(t[k + 1]); k += 2
    return " ".join(o)
BUILDS = {"m1": dict(sw=44, cw=37, ww=31, hw=32, arm=17, fa=14, g="m"), "m2": dict(sw=40, cw=34, ww=29, hw=30, arm=15.5, fa=13, g="m"),
          "f1": dict(sw=36, cw=30, ww=25, hw=31, arm=13.5, fa=11.5, g="f"), "f2": dict(sw=38, cw=33, ww=28, hw=35, arm=14.5, fa=12, g="f")}
SKIN = {"a": "#F2C9A6", "b": "#E1AE8A", "c": "#C98E66", "d": "#A86F4C", "e": "#7E4E33"}
WY = 202  # belt line
def face(c, o):
    skin, hair, hs, g = o["skin"], o["hair"], o["hairstyle"], o["g"]; sk2 = darker(skin, .88); s = ""
    back = o.get("back")
    if hs == "pony" and not back: s += c.P("M112 38 Q130 50 124 86 Q120 98 113 100 Q119 80 112 58Z", hair)
    if hs == "bun" and not o.get("cap"): s += c.P("M89 20 a11 9 0 1 1 22 0 a11 9 0 1 1 -22 0Z", hair)
    s += c.P("M93 58 h14 v24 h-14Z", sk2)
    s += c.P("M82 44 a3.2 5.2 0 1 0 6.4 0 a3.2 5.2 0 1 0 -6.4 0Z", sk2) + c.P("M111.6 44 a3.2 5.2 0 1 0 6.4 0 a3.2 5.2 0 1 0 -6.4 0Z", sk2)
    s += c.P("M85 38 Q85 20 100 20 Q115 20 115 38 L115 50 Q114 64 100 68 Q86 64 85 50Z", skin)
    if c.soft: s += '<path d="M85 38 Q85 20 100 20 Q115 20 115 38 L115 50 Q114 64 100 68 Q86 64 85 50Z" fill="#000" opacity=".06" transform="translate(4,0) scale(.96,1)"/>'
    if back:
        s += c.P("M84 50 Q80 16 100 15 Q120 16 116 50 Q112 60 100 60 Q88 60 84 50Z", hair)
        if hs == "pony": s += c.P("M96 52 Q100 80 100 96 Q104 80 104 52Z", hair)
        if hs == "bun" and not o.get("cap"): s += c.P("M90 22 a10 8 0 1 1 20 0 a10 8 0 1 1 -20 0Z", hair)
        return s
    if hs in ("short", "fade"):
        s += c.P("M84 42 Q82 18 100 15 Q120 14 117 42 Q115 30 108 27 Q98 31 88 29 Q85 34 84 42Z" if hs == "short" else "M85 36 Q85 18 100 17 Q116 17 115 36 Q113 26 100 25 Q88 26 85 36Z", hair)
    elif hs == "curly":
        s += c.P("M84 40 Q78 30 84 24 Q84 14 94 15 Q100 9 107 14 Q117 13 117 24 Q122 31 116 40 Q114 28 100 27 Q88 28 84 40Z", hair)
    else:
        s += c.P("M84 46 Q80 16 100 14 Q121 14 116 46 Q114 31 106 26 Q96 32 86 32Z", hair)
    if o.get("faces", True):
        s += f'<path d="M90 43.5 q3.5 -1.6 7 0 M103 43.5 q3.5 -1.6 7 0" stroke="{darker(hair, .9)}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
        s += '<ellipse cx="93.5" cy="47.5" rx="1.7" ry="1.5" fill="#2a2420"/><ellipse cx="106.5" cy="47.5" rx="1.7" ry="1.5" fill="#2a2420"/>'
        s += f'<path d="M100 49 q-1.6 5 .6 6.2" stroke="{darker(skin, .72)}" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
        s += f'<path d="M95 58.5 q5 3.4 10 0" stroke="{darker(skin, .55) if g == "m" else "#b4573f"}" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
        if c.soft: s += f'<circle cx="91" cy="54" r="3" fill="#e0806a" opacity=".16"/><circle cx="109" cy="54" r="3" fill="#e0806a" opacity=".16"/>'
    return s
def cap(c, o):
    s = c.P("M83 34 Q83 13 100 12 Q117 13 117 34 Z", WHITE, shade=True)
    s += f'<path d="M100 12.5 V33" stroke="#e2dbcf" stroke-width="1"/><path d="M85 31 Q100 27 115 31" stroke="#e2dbcf" stroke-width="1" stroke-dasharray="1.6 1.4" fill="none"/>'
    s += c.P("M79 35 Q100 43 121 35 Q100 30 79 35Z", "#F1ECE3")
    s += f'<g transform="translate(94.5,17) scale(.46)"><path d="M3 13L12 5l9 8" fill="none" stroke="{TERRA}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 12v7h12v-7" fill="none" stroke="{TERRA}" stroke-width="2.4" stroke-linejoin="round"/></g>'
    return s
def arms_for(o, b):
    sw = b["sw"]; L = (100 - sw + 7, 90); R = (100 + sw - 7, 90); pose = o.get("pose", "stand")
    std = lambda S, sx: [S, (S[0] + sx * 8, 156), (S[0] + sx * 7, 218)]
    if pose == "panel":
        return [L, (L[0] - 26, 122), (L[0] - 50, 100)], [R, (R[0] + 6, 152), (R[0] - 6, 196)]
    if pose == "filter":
        return [L, (L[0] - 2, 150), (112, 170)], [R, (R[0] + 12, 146), (R[0] + 34, 166)]
    if pose == "tablet" or o.get("tablet") == "hand":
        return std(L, -1), [R, (R[0] + 8, 152), (R[0] - 10, 186)]
    return std(L, -1), std(R, 1)
def torso_path(nodes):
    """Closed symmetric contour: neck centre -> left side down -> across the hem -> right side up (mirrored)."""
    pts = [(88, 76)] + [n[-1] for n in nodes]
    d = "M100 82 L88 76 " + " ".join(("L%.1f %.1f" % n[1]) if n[0] == "L" else ("Q%.1f %.1f %.1f %.1f" % (*n[1], *n[2])) for n in nodes)
    end = nodes[-1][-1]; d += " L%.1f %.1f" % (200 - end[0], end[1])
    for i in range(len(nodes) - 1, -1, -1):
        n = nodes[i]; prev = pts[i]
        if n[0] == "L": d += " L%.1f %.1f" % (200 - prev[0], prev[1])
        else: d += " Q%.1f %.1f %.1f %.1f" % (200 - n[1][0], n[1][1], 200 - prev[0], prev[1])
    return d + " L100 82 Z"
def person(c, o):
    """Illustrated tech in local units (x 0..200, feet at y~406). o: build, skin, hair, hairstyle, polo, pants, shoes (sneaker|boot),
    faces, cap, sleeves (straight|rolled), name, belt (belt|toolbelt|pouch), tablet (hand|belt|None), layer (softshell|None),
    gloves, pose (stand|panel|filter), back (turned around), big (slightly stylized head)."""
    o = dict(dict(build="m1", skin=SKIN["c"], hair="#231a14", hairstyle="short", polo=TERRA, pants=CH, shoes="sneaker", faces=True, cap=False,
                  sleeves="straight", name=None, belt="belt", tablet=None, layer=None, gloves=False, pose="stand", back=False, big=False), **o)
    b = BUILDS[o["build"]]; o["g"] = b["g"]; sw, cw, ww, hw = b["sw"], b["cw"], b["ww"], b["hw"]
    soft = o["layer"] == "softshell"; top = CH if soft else o["polo"]; dk = darker(top, .8); dd = darker(top, .62)
    s = c.shadow(100, 404, 50, 6)
    if c.soft: s += '<ellipse cx="128" cy="402" rx="40" ry="5" fill="#000" opacity=".05"/>'
    # legs
    pc = o["pants"]; pdk = darker(pc, .78)
    lg = f"M{100 - ww - .5} {WY + 3} L100 {WY + 3} L100 246 Q95 290 93 330 L92 392 L76 392 Q74 340 73 300 Q{100 - hw - 1} 250 {100 - hw} {WY + 18} Z"
    s += c.P(lg, pc, shade=True) + c.P(mirp(lg), pc, shade=True)
    s += f'<path d="M84 252 Q83 320 84 386 M116 252 Q117 320 116 386" stroke="{pdk}" stroke-width="1" fill="none" opacity=".7"/><path d="M100 {WY + 8} V244" stroke="{pdk}" stroke-width="1.1"/>'
    s += f'<path d="M{100 - ww + 3} {WY + 7} Q{100 - ww + 9} {WY + 20} {100 - hw + 4} {WY + 32} M{100 + ww - 3} {WY + 7} Q{100 + ww - 9} {WY + 20} {100 + hw - 4} {WY + 32}" stroke="{pdk}" stroke-width="1.1" fill="none"/>'
    s += f'<path d="M78 300 q4 3 9 2 M113 302 q4 1 9 -2 M80 318 q4 2 8 1" stroke="{pdk}" stroke-width=".9" fill="none" opacity=".75"/>'
    s += f'<path d="M77 388 H91 M109 388 H123" stroke="{lighter(pc, .25)}" stroke-width=".8" stroke-dasharray="1.6 1.2"/>'
    s += feet(c, o["shoes"])
    # arms (behind torso parts get drawn after torso so they read clearly)
    la, ra = arms_for(o, b); skin = o["skin"]; s2 = darker(skin, .93)
    # torso
    hem = WY + (16 if soft else 6); ex = 2 if soft else 0
    if b["g"] == "f":
        nodes = [("L", (100 - sw + 9, 82)), ("Q", (100 - sw - ex, 85), (100 - sw - ex, 96)), ("Q", (100 - cw - 3 - ex, 116), (100 - cw - ex, 132)),
                 ("Q", (100 - ww - 2 - ex, 168), (100 - ww - ex, 180)), ("Q", (100 - ww - 3 - ex, 192), (100 - ww - 1 - ex, hem))]
    else:
        nodes = [("L", (100 - sw + 9 - ex, 82)), ("Q", (100 - sw - ex, 85), (100 - sw - ex, 96)), ("Q", (100 - cw - 2 - ex, 122), (100 - cw - ex, 138)),
                 ("Q", (100 - ww - 1 - ex, 176), (100 - ww - ex, hem))]
    t = torso_path(nodes)
    s += c.P(t, top, shade=True)
    s += f'<path d="M{100 - cw + 6} 150 Q{100 - ww + 6} 176 {100 - ww + 5} {hem - 4} M{100 + cw - 9} 156 q-4 10 -2 18" stroke="{dk}" stroke-width="1" fill="none" opacity=".55"/>'
    s += f'<path d="M89 77 L{100 - sw + 9} 83 M111 77 L{100 + sw - 9} 83" stroke="{lighter(top, .3)}" stroke-width=".8" stroke-dasharray="1.6 1.2"/>'
    if soft:
        s += f'<path d="M100 84 V{hem}" stroke="{CHD}" stroke-width="2"/><path d="M100 84 V{hem}" stroke="#6b6e73" stroke-width=".7" stroke-dasharray="1 1"/>'
        s += f'<rect x="98.2" y="96" width="3.6" height="8" rx="1" fill="{TERRA}"/>'
        s += c.P("M88 74 L100 80 L112 74 L113 84 L100 90 L87 84Z", CHD)
        s += c.P("M93 78 L100 84 L97 88 L91 82Z", o["polo"]) + c.P("M107 78 L100 84 L103 88 L109 82Z", o["polo"])
        s += f'<path d="M{100 - cw + 6} 174 l10 14 M{100 + cw - 6} 174 l-10 14" stroke="{CHD}" stroke-width="1.6"/>'
        s += f'<path d="M{100 - ww - 1} {hem - 3} H{100 + ww + 1}" stroke="#5a5d62" stroke-width=".8" stroke-dasharray="1.6 1.2"/>'
        s += f'<path d="M{100 - sw + 6} 106 Q100 112 {100 + sw - 6} 106" stroke="{CHD}" stroke-width="1" fill="none" opacity=".8"/>'
        if not o["back"]: s += c.logo(104.5, 96, 18)
    elif not o["back"]:
        s += c.P("M88 76 L100 89 L94 98 L83 83Z", top, f'stroke="{dd}" stroke-width="1"') + c.P("M112 76 L100 89 L106 98 L117 83Z", top, f'stroke="{dd}" stroke-width="1"')
        s += f'<path d="M89.5 79 L99 89 M110.5 79 L101 89" stroke="{lighter(top, .3)}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
        s += f'<rect x="97" y="87" width="6" height="24" rx="1.5" fill="{dk}"/><circle cx="100" cy="94" r="1.3" fill="{dd}"/><circle cx="100" cy="103" r="1.3" fill="{dd}"/>'
        s += f'<path d="M96.4 88 V110 M103.6 88 V110" stroke="{lighter(top, .3)}" stroke-width=".6" stroke-dasharray="1.2 1"/>'
        s += c.logo(105, 96, 19)
        if o["name"]: s += f'<text x="114.5" y="107.5" font-family="Hind" font-weight="600" font-size="4.6" fill="#fff" text-anchor="middle">{esc(o["name"])}</text>'
    else:
        s += c.P("M88 76 Q100 82 112 76 L112 80 Q100 86 88 80Z", dk)
    if o["back"]:
        s += c.logo(100 - cw + 6, 104, 2 * cw - 12)
    # belt + gear
    if not soft:
        s += f'<rect x="{100 - ww - 1}" y="{WY}" width="{2 * ww + 2}" height="7" rx="1.5" fill="#141414"/>'
        if not o["back"]: s += f'<rect x="95" y="{WY - 1}" width="10" height="9" rx="1.5" fill="none" stroke="#a7a9ac" stroke-width="1.6"/>'
    gy = WY + (6 if soft else 2)
    if o["belt"] == "toolbelt":
        s += c.P(f"M{100 - ww - 10} {gy} h20 v26 q0 4 -4 4 h-12 q-4 0 -4 -4Z", "#4a4d52")
        s += f'<path d="M{100 - ww - 7} {gy + 3} h14 v22 h-14Z" fill="none" stroke="{TERRA}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
        s += f'<rect x="{100 - ww - 6}" y="{gy - 10}" width="3.4" height="12" rx="1" fill="{TERRA}"/><rect x="{100 - ww - 1}" y="{gy - 8}" width="2.6" height="10" fill="#9aa0a6"/><rect x="{100 - ww + 3}" y="{gy - 12}" width="3" height="13" rx="1" fill="{SAFFRON}"/>'
        s += c.P(f"M{100 + ww - 8} {gy} h17 v20 q0 4 -4 4 h-9 q-4 0 -4 -4Z", "#4a4d52")
        s += f'<path d="M{100 + ww - 5} {gy + 3} h11 v16 h-11Z" fill="none" stroke="{TERRA}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
        s += f'<rect x="{100 + ww - 4}" y="{gy - 7}" width="10" height="9" rx="2" fill="{LAGOON}"/><circle cx="{100 + ww + 1}" cy="{gy - 2.5}" r="2" fill="#fff" opacity=".7"/>'
    elif o["belt"] == "pouch":
        s += c.P(f"M{100 + ww - 6} {gy} h14 v15 q0 3 -3 3 h-8 q-3 0 -3 -3Z", "#4a4d52")
        s += c.P(f"M{100 + ww - 7} {gy - 1} h16 v7 h-16Z", CHD)
        s += f'<rect x="{100 + ww - 2}" y="{gy + 1}" width="6" height="3" rx="1" fill="{TERRA}"/><path d="M{100 + ww - 4} {gy + 8} h10" stroke="{TERRA}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
    if o["tablet"] == "belt":
        tx = 100 - ww - 12
        s += f'<rect x="{tx + 1}" y="{gy - 10}" width="15" height="20" rx="2" fill="#2b2c2f"/><rect x="{tx + 2.6}" y="{gy - 8.4}" width="11.8" height="6" rx="1" fill="#DCEAF0"/>'
        s += c.P(f"M{tx} {gy - 2} h17 v24 q0 3 -3 3 h-11 q-3 0 -3 -3Z", "#4a4d52") + f'<rect x="{tx + 4}" y="{gy + 6}" width="9" height="3" rx="1" fill="{TERRA}"/>'
    if o["pose"] == "filter":
        s += filt(104, 156, sw + 66, 18)
    # arms
    for A, side in ((la, -1), (ra, 1)):
        S, E, Wr = A
        s += c.limb([lerp(S, E, .3), E], b["arm"], s2) + c.limb([E, Wr], b["fa"], s2)
        if soft:
            s += c.limb([S, E], b["arm"] + 4, CH) + c.limb([E, lerp(E, Wr, .92)], b["fa"] + 4, CH)
            p1, p2 = perp(E, Wr, .9, (b["fa"] + 4) / 2); s += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}" stroke="{CHD}" stroke-width="3"/>'
            m1, m2 = perp(S, E, .95, (b["arm"] + 3) / 2); s += f'<path d="M{m1[0]:.1f} {m1[1]:.1f} Q{E[0]:.1f} {E[1] + 3:.1f} {m2[0]:.1f} {m2[1]:.1f}" stroke="{CHD}" stroke-width=".9" fill="none"/>'
        else:
            f = .44 if o["sleeves"] == "rolled" else .56
            sl = lerp(S, E, f); s += f'<circle cx="{S[0]:.1f}" cy="{S[1]:.1f}" r="{(b["arm"] + 5) / 2:.1f}" fill="{top}"/>' + c.limb([S, sl], b["arm"] + 5, top, "butt")
            if o["sleeves"] == "rolled":
                a0 = lerp(S, E, f - .14); s += c.limb([a0, sl], b["arm"] + 7, lighter(top, .12), "butt")
                p1, p2 = perp(S, E, f - .07, (b["arm"] + 7) / 2); s += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}" stroke="{dd}" stroke-width="1"/>'
            else:
                a0 = lerp(S, E, f - .08); s += c.limb([a0, sl], b["arm"] + 5, dk, "butt")
                p1, p2 = perp(S, E, f - .1, (b["arm"] + 5) / 2); s += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}" stroke="{lighter(top, .3)}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
        dx, dy = Wr[0] - E[0], Wr[1] - E[1]; L = math.hypot(dx, dy) or 1; hx, hy = Wr[0] + dx / L * b["fa"] * .55, Wr[1] + dy / L * b["fa"] * .55
        r = b["fa"] * .62
        if o["gloves"]:
            s += c.P(f"M{hx - r} {hy} a{r} {r * 1.15} 0 1 0 {2 * r} 0 a{r} {r * 1.15} 0 1 0 {-2 * r} 0Z", CH)
            s += c.limb([lerp(E, Wr, .86), Wr], b["fa"] + 1.5, TERRA, "butt")
        else:
            s += c.P(f"M{hx - r} {hy} a{r} {r * 1.15} 0 1 0 {2 * r} 0 a{r} {r * 1.15} 0 1 0 {-2 * r} 0Z", skin)
    if o["tablet"] == "hand" or o.get("pose") == "tablet":
        Wr = ra[2]
        s += f'<g transform="rotate(-10 {Wr[0]} {Wr[1]})"><rect x="{Wr[0] - 20}" y="{Wr[1] - 12}" width="28" height="36" rx="3.5" fill="#2b2c2f"/><rect x="{Wr[0] - 17.5}" y="{Wr[1] - 9.5}" width="23" height="31" rx="1.5" fill="#E4F0F5"/>'
        s += f'<rect x="{Wr[0] - 15}" y="{Wr[1] - 7}" width="18" height="4.5" rx="1" fill="{TERRA}"/>' + "".join(f'<rect x="{Wr[0] - 15}" y="{Wr[1] + j * 5}" width="{18 - (j % 2) * 5}" height="2.4" rx="1" fill="#9db7c3"/><circle cx="{Wr[0] + 5}" cy="{Wr[1] + 1.2 + j * 5}" r="1.4" fill="{JUNGLE}"/>' for j in range(4)) + "</g>"
        r = b["fa"] * .62; s += c.P(f"M{Wr[0] - 19 - r} {Wr[1] + 14} a{r} {r * 1.1} 0 1 0 {2 * r} 0 a{r} {r * 1.1} 0 1 0 {-2 * r} 0Z", CH if o["gloves"] else skin)
    # head
    hd = face(c, o) + (cap(c, o) if o["cap"] else "")
    if o["big"]: hd = f'<g transform="translate(100,80) scale(1.3) translate(-100,-80)">{hd}</g>'
    s = s.replace("<!--HEAD-->", "") + hd
    return s
def feet(c, kind):
    """Terracotta reusable covers with the logo over sneakers (good weather) or boots (bad weather), toes out, always visible."""
    s = ""
    for sx in (1, -1):
        X = lambda x: 100 + sx * (x - 100)
        pts = lambda P: "M" + " L".join(f"{X(x):.1f} {y}" for x, y in P) + " Z"
        if kind == "sneaker":
            s += c.P(pts([(93, 386), (93, 400), (96, 404), (70, 404), (63, 400), (67, 393), (76, 386)]), TERRA)
            s += f'<path d="M{X(75)} 387.5 L{X(93)} 387.5" stroke="{darker(TERRA, .7)}" stroke-width="3"/>'
            s += f'<path d="M{X(64)} 403 L{X(96)} 403" stroke="#f4efe6" stroke-width="2"/><path d="M{X(66)} 399.5 L{X(94)} 399.5" stroke="{lighter(TERRA, .35)}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
            s += c.logo(min(X(69), X(89)), 392.5, 20)
        else:
            s += c.P(pts([(94, 376), (95, 400), (98, 406), (66, 406), (61, 400), (65, 391), (74, 376)]), TERRA)
            s += f'<path d="M{X(73)} 377.5 L{X(94)} 377.5" stroke="{darker(TERRA, .7)}" stroke-width="3.2"/>'
            s += f'<rect x="{min(X(61), X(98)):.1f}" y="404" width="37" height="5" rx="1.5" fill="#2a2420"/><path d="M{X(64)} 401 L{X(96)} 401" stroke="{lighter(TERRA, .35)}" stroke-width=".7" stroke-dasharray="1.4 1"/>'
            s += c.logo(min(X(69), X(91)), 387, 22)
    return s
# ---- scenes ----
def room(c, W_, H_, floor):
    s = f'<rect width="{W_}" height="{H_}" fill="{CR2}"/><rect y="{floor}" width="{W_}" height="{H_ - floor}" fill="#E6D3B6"/>'
    s += "".join(f'<path d="M0 {floor + k * 9} H{W_}" stroke="#d8c3a2" stroke-width=".8"/>' for k in range(1, 6))
    s += "".join(f'<path d="M{(k * 47 + (j % 2) * 23) % W_} {floor + j * 9} v9" stroke="#d8c3a2" stroke-width=".8"/>' for j in range(5) for k in range(6))
    s += f'<rect y="{floor - 5}" width="{W_}" height="5" fill="#FFFFFF"/><path d="M0 {floor - 5} H{W_}" stroke="#e5dccd"/>'
    s += f'<rect x="14" y="26" width="58" height="72" rx="2" fill="#FFFFFF" stroke="#e1d6c4"/><rect x="18" y="30" width="50" height="64" fill="#D7E9F0"/><path d="M43 30 V94 M18 62 H68" stroke="#FFFFFF" stroke-width="3"/>'
    s += f'<rect x="{W_ - 44}" y="70" width="18" height="24" rx="3" fill="#FFFFFF" stroke="#d8cfbf"/><circle cx="{W_ - 35}" cy="80" r="5" fill="none" stroke="{LAGOON}" stroke-width="1.6"/><text x="{W_ - 35}" y="91.5" font-family="Hind" font-size="4.5" text-anchor="middle" fill="{MUTE}">68</text>'
    return s
def panel_box(x, y):
    s = f'<rect x="{x}" y="{y}" width="34" height="48" rx="2" fill="#E9E6E0" stroke="#9aa0a6" stroke-width="1.2"/><rect x="{x + 4}" y="{y + 5}" width="26" height="38" fill="#F7F5F1" stroke="#c9c4ba"/>'
    s += "".join(f'<rect x="{x + 6 + (k % 2) * 13}" y="{y + 8 + (k // 2) * 6}" width="9" height="3.4" rx=".8" fill="{"#2b2c2f" if k != 5 else TERRA}"/>' for k in range(10))
    return s
def furnace(x, y, h=150):
    s = f'<rect x="{x}" y="{y}" width="56" height="{h}" rx="3" fill="#FFFFFF" stroke="#9aa0a6" stroke-width="1.2"/>'
    s += "".join(f'<path d="M{x + 10} {y + 12 + k * 6} H{x + 46}" stroke="#d6cfc2" stroke-width="1.6"/>' for k in range(3))
    s += f'<rect x="{x - 2}" y="{y + 66}" width="60" height="4" fill="#2b2c2f"/><rect x="{x + 16}" y="{y + 90}" width="24" height="20" rx="2" fill="{CREAM}" stroke="#bdb5a8"/>'
    return s
def filt(x, y, w=40, h=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="#FFFFFF" stroke="#9aa0a6" stroke-width="1"/>' + "".join(f'<path d="M{x + 3 + j * 3.5:.1f} {y + 1} v{h - 2}" stroke="#d6d0c6" stroke-width=".9"/>' for j in range(int(w / 3.5) - 1))
def van_bg(c, x, y, sc):
    W_, LN = "#FFFFFF", "#cfc7b9"
    body = "M40 238 L40 186 Q40 168 56 160 L120 140 Q134 104 150 84 Q160 70 178 66 L560 62 Q580 62 582 82 L588 226 Q588 238 576 238 Z"
    s = f'<g transform="translate({x},{y}) scale({sc})">'
    s += f'<path d="{body}" fill="{W_}" stroke="{LN}" stroke-width="2.4"/>' + (f'<path d="{body}" fill="url(#{c.sh})" opacity=".4"/>' if c.soft else "")
    s += f'<path d="M40 220 H588 V232 Q588 240 578 240 H48 Q40 240 40 232Z" fill="#2a2b2e"/><path d="M40 206 Q200 214 330 196 Q450 180 588 176 L588 196 Q450 200 330 212 Q200 228 40 220Z" fill="{TERRA}"/>'
    s += f'<path d="M40 224 Q220 230 588 200" stroke="{LAGOON}" stroke-width="3" fill="none"/><path d="M128 138 Q140 106 154 88 Q160 82 166 82 L170 138 Z" fill="#DCEAF0" stroke="#b9cfd8" stroke-width="1.5"/>'
    s += f'<path d="M176 86 L232 84 L232 136 L176 138 Z" fill="#DCEAF0" stroke="#b9cfd8" stroke-width="1.5"/><path d="M240 76 V216 M440 74 V216" stroke="{LN}" stroke-width="2"/>'
    s += c.logo(262, 104, 160, white=False)
    for cx in (130, 482):
        s += f'<circle cx="{cx}" cy="240" r="32" fill="#1f2022"/><circle cx="{cx}" cy="240" r="16" fill="#d9d5cc"/><path d="M{cx - 42} 222 Q{cx} 186 {cx + 42} 222" stroke="#2a2b2e" stroke-width="6" fill="none"/>'
    s += f'<path d="M190 62 v-8 M330 62 v-8 M470 62 v-8" stroke="#2a2b2e" stroke-width="4"/><rect x="196" y="40" width="350" height="12" rx="2" fill="none" stroke="#a9aeb4" stroke-width="3"/>'
    return s + "</g>"
# ---- card frame ----
AH = 268  # art height (card units)
def card(c, art, note, label="TECH GRAPHIC", bg=CREAM, ah=AH):
    top = 24; Hh = top + ah + 46
    ak = uid("a")
    body = f'<g transform="translate(0,{top})"><clipPath id="{ak}"><rect width="{W}" height="{ah}"/></clipPath><g clip-path="url(#{ak})"><rect width="{W}" height="{ah}" fill="{bg}"/>{art}</g></g>'
    body += rect(0, 0, W, top, "#FFFFFF") + t(12, 16, label, 7.5, INK, "hind", 700, extra='letter-spacing=".8"') + ln(top, 0, W, LINE)
    body += rect(193, 6, 36, 13, "#FFFFFF", SAFFRON, 3, 1, 'stroke-dasharray="3 2"') + t(211, 15.5, "MOCKUP", 6, "#8A6510", "hind", 700, "middle", 'letter-spacing=".5"')
    yn = Hh - 30
    body += ln(yn - 10, 0, W, LINE) + rect(12, yn - 4, 3, 24, TERRA) + t(20, yn + 6, note[0], 8.5, INK, "hind", 600) + t(20, yn + 18, note[1], 7.8, MUTE)
    k = uid("r")
    return crisp(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="max-width:100%;height:auto" stroke-linecap="round">{c.defs()}'
                 f'<clipPath id="{k}"><rect width="{W}" height="{Hh}" rx="14"/></clipPath><g clip-path="url(#{k})"><rect width="{W}" height="{Hh}" fill="#FFFFFF"/>' + body +
                 f'</g><rect x=".5" y=".5" width="{W - 1}" height="{Hh - 1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def place(c, o, cx, base, sc):
    """Person o with feet centre at (cx, base) in art units, scaled sc. Returns svg and a mapper local->art coords."""
    tx, ty = cx - 100 * sc, base - 406 * sc
    return f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.4f})">{person(c, o)}</g>', (lambda x, y: (tx + x * sc, ty + y * sc))
def callout(px, py, lx, ly, text, anchor="start"):
    w = len(text) * 4.3 + 8; x0 = lx if anchor == "start" else lx - w
    return (f'<path d="M{px:.1f} {py:.1f} L{lx if anchor == "start" else lx:.1f} {ly:.1f}" stroke="{INK}" stroke-width=".7" fill="none"/><circle cx="{px:.1f}" cy="{py:.1f}" r="1.8" fill="#fff" stroke="{INK}" stroke-width=".8"/>'
            + rect(x0, ly - 7, w, 13, "#FFFFFF", "#D6D0C6", 3, .8) + t(x0 + 4, ly + 2.6, text, 7.5, INK, "hind", 600))
def cover_inset(c, x, y, w=76, tall=False, label="Logo shoe covers"):
    """Close-up badge of a terracotta reusable cover with the logo."""
    s = rect(x, y, w, w * .78, "#FFFFFF", "#D6D0C6", 6, .9)
    sc = (w - 10) / 80
    if tall:
        sh = "M8 44 V6 Q8 0 14 0 H36 Q40 0 40 6 V22 Q50 26 64 28 Q78 31 78 42 V50 Q78 52 74 52 H6 Q4 52 4 50Z"
    else:
        sh = "M4 40 Q2 22 14 18 L30 14 Q40 24 58 26 Q74 28 76 40 V45 Q76 48 72 48 H6 Q2 48 2 45Z"
    s += f'<g transform="translate({x + 5},{y + 6}) scale({sc:.3f})"><path d="{sh}" fill="{TERRA}"/><path d="M14 {20 if not tall else 17} Q24 {15 if not tall else 13} 34 {17 if not tall else 15}" stroke="{darker(TERRA, .68)}" stroke-width="3.4" fill="none"/>'
    s += f'<path d="M4 {46 if not tall else 49} H76" stroke="{darker(TERRA, .62)}" stroke-width="2.4"/><path d="M6 {42 if not tall else 45} H74" stroke="{lighter(TERRA, .35)}" stroke-width=".9" stroke-dasharray="2 1.5"/>'
    s += c.logo(28, 29, 36) + "</g>"
    s += t(x + w / 2, y + w * .78 - 5, label, 7.5, INK, "hind", 600, "middle")
    return s

def zoom(c, o, lx, ly, z, x, y, r, label=None):
    """Round close-up of the same tech: local point (lx, ly) magnified z times, centred at (x, y) radius r."""
    k = uid("z")
    s = (f'<clipPath id="{k}"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath><circle cx="{x}" cy="{y}" r="{r + 2.5}" fill="#FFFFFF"/>'
         f'<g clip-path="url(#{k})"><rect x="{x - r}" y="{y - r}" width="{2 * r}" height="{2 * r}" fill="{CREAM}"/>'
         f'<g transform="translate({x - lx * z:.1f},{y - ly * z:.1f}) scale({z})">{person(c, o)}</g></g>'
         f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#D6D0C6" stroke-width="1.2"/>')
    if label: s += rect(x - len(label) * 2.2 - 5, y + r - 6, len(label) * 4.4 + 10, 13, "#FFFFFF", "#D6D0C6", 3, .8) + t(x, y + r + 3.2, label, 7.5, INK, "hind", 600, "middle")
    return s
# ---- decks ----
LOC = "Smart Upkeep Tech Graphics"
TA = dict(build="m1", skin=SKIN["c"], hair="#231a14", hairstyle="short", polo=TERRA, shoes="sneaker")
TB = dict(build="f1", skin=SKIN["a"], hair="#5a3a26", hairstyle="pony", polo=LAGOON, shoes="boot")
TC = dict(build="m2", skin=SKIN["e"], hair="#17110d", hairstyle="curly", polo=LAGOON, shoes="sneaker")
TD = dict(build="f2", skin=SKIN["d"], hair="#2b211b", hairstyle="bun", polo=TERRA, shoes="boot")
BASE = 262
def hero(o=None, ctx=None, extra="", under="", sc=.62, cx=120):
    c = Ctx(**(ctx or {})); a, m = place(c, dict(TA, **(o or {})), cx, BASE, sc); return c, under + a + extra, m
def duo(oa=None, ob=None, ctx=None, sc=.6, under=""):
    c = Ctx(**(ctx or {})); a1, m1 = place(c, dict(TA, **(oa or {})), 70, BASE, sc); a2, m2 = place(c, dict(TB, **(ob or {})), 170, BASE, sc)
    return c, under + a1 + a2, (m1, m2)
def T_STYLE():
    pairs, P = make("tgstyle18_", "UpKeep")
    def add(group, el, sentence, A, B):
        P(group, LOC, el, sentence, A, B)
    def opt(k, label, desc, feel, c, art, note): return (k, label, desc, feel, card(c, art, note))
    # 1 shading
    c1, a1, _ = hero(ctx=dict(soft=False)); c2, a2, _ = hero(ctx=dict(soft=True))
    add("Rendering", "Shading", "should the techs be drawn as flat vector shapes or soft-shaded vector with gentle light and shadow?",
        opt("flat", "Flat Vector", "Solid colour shapes, no gradients; crisp at any size.", "calm", c1, a1, ("Clean, poster-like", "Lightest file, prints well")),
        opt("soft", "Soft-Shaded Vector", "Same shapes with gentle side light, shadow and fabric shading.", "warm", c2, a2, ("Fabric looks real", "Same look as the round-2 pitch")))
    # 2 outline
    c1, a1, _ = hero(); c2, a2, _ = hero(ctx=dict(outline=1.6))
    add("Rendering", "Outline", "should each tech be drawn with no outline or with a dark ink outline around every shape?",
        opt("none", "No Outline", "Shapes meet colour to colour, like the round-2 pitch.", "calm", c1, a1, ("Soft and modern", "Colours do the work")),
        opt("ink", "Ink Outline", "A dark line around the body, clothes and gear.", "bold", c2, a2, ("Reads on any background", "More like a comic panel")))
    # 3 crop
    c1, a1, _ = hero()
    c2 = Ctx(); o = dict(TA); sc = 1.0; a2 = place(c2, o, 112, 14 * -1 + 10 + 406 * sc, sc)[0] + cover_inset(c2, 156, 190)
    add("Framing", "Crop", "should a tech graphic show the full figure head to toe or a three-quarter crop with the shoe covers in an inset?",
        opt("full", "Full Figure", "Head to shoe covers, the whole uniform in one view.", "practical", c1, a1, ("Covers seen on the feet", "Whole uniform at once")),
        opt("three", "Three-Quarter Crop", "Head to knee, bigger and closer; covers shown in a corner inset.", "focused", c2, a2, ("Face and logo read bigger", "Covers kept in the inset")))
    # 4 proportions
    c1, a1, _ = hero(); c2, a2, _ = hero(dict(big=True), sc=.6)
    add("Proportions", "Body proportions", "should techs keep realistic adult proportions or a slightly stylized look with a larger head?",
        opt("real", "Realistic Proportions", "About seven and a half heads tall, like a real fit adult.", "calm", c1, a1, ("Grown-up and credible", "Fits an investor pitch")),
        opt("styl", "Slightly Stylized", "Head about a third bigger; friendlier, more character-like.", "playful", c2, a2, ("Friendly at small sizes", "Face reads on a phone")))
    # 5 faces
    c1, a1, _ = duo(); c2, a2, _ = duo(dict(faces=False), dict(faces=False))
    add("Faces", "Faces", "should techs have simple faces with eyes, brows and a smile or be faceless with hair and ears only?",
        opt("face", "Simple Faces", "Dot eyes, brows, a small nose line and a smile.", "warm", c1, a1, ("Feels like a real person", "Friendly and trustworthy")),
        opt("noface", "Faceless", "Skin, ears and hair only, no features drawn.", "calm", c2, a2, ("Anyone can see themselves", "Very clean at small size")))
    # 6 count
    c1, a1, _ = hero(); c2, a2, _ = duo()
    add("Framing", "How many techs", "should the main tech graphic show one tech as the hero or a pair of techs side by side?",
        opt("one", "One Tech Hero", "A single tech, centred and larger.", "focused", c1, a1, ("One clear face of the brand", "More room for detail")),
        opt("pair", "A Pair", "Two techs side by side, good-weather and bad-weather kit.", "warm", c2, a2, ("Shows both footwear options", "Feels like a team")))
    # 7 pose
    c1, a1, _ = hero()
    c2 = Ctx(); o = dict(TA, pose="filter", gloves=True); a, m = place(c2, o, 78, BASE, .62)
    fx, fy = m(100 + BUILDS["m1"]["sw"] + 50, 166); a2 = furnace(fx, fy - 68, BASE - fy + 68) + a
    add("Pose", "Pose", "should techs stand in a calm static pose or be shown mid-task, here sliding a fresh filter into a furnace?",
        opt("static", "Static Pose", "Standing, arms relaxed, facing forward.", "calm", c1, a1, ("Uniform reads clearly", "Works as a cut-out anywhere")),
        opt("task", "Mid-Task", "Gloved hands sliding a fresh filter into the furnace slot.", "practical", c2, a2, ("Shows what we actually do", "Tells the story in one look")))
    # 8 backdrop
    c1, a1, _ = hero(); c2 = Ctx(); a2 = room(c2, W, AH, 205) + place(c2, dict(TA), 120, BASE, .62)[0]
    add("Backdrop", "Backdrop", "should a tech sit on plain warm cream or in front of a light room scene with a window, wall and floor?",
        opt("plain", "Plain Cream", "Just the tech and a soft floor shadow on cream.", "calm", c1, a1, ("Nothing competes with the tech", "Drops onto any slide")),
        opt("room", "Light Room Scene", "Pale wall, window, thermostat and a wood floor behind.", "warm", c2, a2, ("Says in-home service", "More context, more busy")))
    # 9 variety
    c1 = Ctx(); a1 = "".join(place(c1, o, x, BASE, .5)[0] for o, x in ((TA, 34), (TB, 89), (TC, 151), (TD, 206)))
    c2, a2, _ = duo()
    add("Variety", "Skin tone and build variety", "should the brand set show four techs with a range of skin tones and builds or a set of two?",
        opt("four", "A Set Of Four", "Four techs, four skin tones, broad to slim-athletic builds.", "warm", c1, a1, ("Real variety across the team", "All fit and healthy")),
        opt("two", "A Set Of Two", "Two techs with different tones and builds.", "focused", c2, a2, ("Simpler and bigger", "Matches the pitch today")))
    # 10 line weight
    c1, a1, _ = hero(ctx=dict(outline=.9)); c2, a2, _ = hero(ctx=dict(outline=2.2))
    add("Rendering", "Line weight", "where outlines are used should they be a thin fine line or a medium line that holds up when the graphic is small?",
        opt("thin", "Thin Line", "A fine dark line, about half a point at phone size.", "calm", c1, a1, ("Light and precise", "Detail stays visible")),
        opt("medium", "Medium Line", "A firmer line, about twice as thick.", "bold", c2, a2, ("Holds up when shrunk", "Bolder on a slide")))
    return pairs
def T_GEAR():
    pairs, P = make("tggear18_", "UpKeep")
    def add(group, el, sentence, A, B):
        P(group, LOC, el, sentence, A, B)
    def opt(k, label, desc, feel, c, art, note): return (k, label, desc, feel, card(c, art, note))
    # 1 back view
    c1, a1, _ = hero()
    c2 = Ctx(); a2 = place(c2, dict(TA), 70, BASE, .6)[0] + place(c2, dict(TA, back=True), 170, BASE, .6)[0]
    a2 += t(70, 16, "FRONT", 7.5, MUTE, "hind", 700, "middle", 'letter-spacing="1"') + t(170, 16, "BACK", 7.5, MUTE, "hind", 700, "middle", 'letter-spacing="1"')
    add("Views", "Back wordmark view", "should brand graphics show the tech from the front only or as a front-and-back pair that shows the big back wordmark?",
        opt("front", "Front View Only", "One front view with the left-chest logo.", "focused", c1, a1, ("Simple, one figure", "Back print left out")),
        opt("turn", "Front And Back", "Front view plus a back view with the full wordmark.", "practical", c2, a2, ("Shows the whole uniform", "Back print you picked")))
    # 2 name
    o1 = dict(TA, name="Sam"); c1 = Ctx(); a1 = place(c1, o1, 92, BASE, .62)[0] + zoom(c1, o1, 112, 102, 3.4, 186, 92, 42, "Logo plus name")
    o2 = dict(TA); c2 = Ctx(); a2 = place(c2, o2, 92, BASE, .62)[0] + zoom(c2, o2, 112, 102, 3.4, 186, 92, 42, "Logo only")
    add("Chest", "Printed first name", "should graphics show the printed first name under the chest logo or leave the name off at graphic size?",
        opt("name", "Name Under Logo", "A sample first name printed under the left-chest logo.", "warm", c1, a1, ("Matches the real polo", "Feels personal")),
        opt("noname", "Logo Only", "Left-chest logo with no name drawn.", "calm", c2, a2, ("Cleaner art", "No sample name to explain")))
    # 3 belt gear
    o1 = dict(TA, belt="toolbelt"); c1 = Ctx(); a1 = place(c1, o1, 92, BASE, .62)[0] + zoom(c1, o1, 72, 214, 2.2, 186, 150, 44, "Tool belt")
    o2 = dict(TA, belt="pouch"); c2 = Ctx(); a2 = place(c2, o2, 92, BASE, .62)[0] + zoom(c2, o2, 128, 212, 2.4, 186, 150, 44, "Utility pouch")
    add("Gear", "Belt gear", "should techs be drawn with a full tool belt with two pouches or one slim utility pouch on the hip?",
        opt("belt", "Tool Belt", "Two canvas pouches with tools, tape and terracotta stitching.", "practical", c1, a1, ("Ready for any job", "Busier around the waist")),
        opt("pouch", "Utility Pouch", "One slim flap pouch with a terracotta tab.", "calm", c2, a2, ("Neat, indoor-friendly", "Fits the clean-home promise")))
    # 4 tablet
    o1 = dict(TA, tablet="hand"); c1 = Ctx(); a1 = place(c1, o1, 92, BASE, .62)[0] + zoom(c1, o1, 121, 192, 2.2, 186, 104, 44, "Tablet in hand")
    o2 = dict(TA, tablet="belt"); c2 = Ctx(); a2 = place(c2, o2, 92, BASE, .62)[0] + zoom(c2, o2, 65, 206, 2.4, 186, 104, 44, "Tablet on belt")
    add("Gear", "Tablet", "should the tech hold the work tablet in hand with a checklist on screen or carry it in a holster on the belt?",
        opt("hand", "Tablet In Hand", "Held at the hip, checklist screen facing out.", "practical", c1, a1, ("Shows the visit checklist", "Says we record everything")),
        opt("belt", "Tablet On The Belt", "Tucked in a holster on the hip, hands free.", "calm", c2, a2, ("Hands free, relaxed", "Simpler silhouette")))
    # 5 covers
    c1, a1, _ = hero(cx=120)
    c2 = Ctx(); a2 = place(c2, dict(TA), 92, BASE, .62)[0] + cover_inset(c2, 152, 150, 80)
    add("Shoe Covers", "Shoe cover display", "should the terracotta logo shoe covers be drawn on the feet only or on the feet plus a close-up inset?",
        opt("on", "Drawn On The Feet", "Covers with the logo on both feet, nothing extra.", "calm", c1, a1, ("Simple and true to life", "Small at phone size")),
        opt("inset", "On The Feet Plus Inset", "Same covers on the feet plus a close-up badge with the logo.", "focused", c2, a2, ("Covers can't be missed", "Logo reads clearly")))
    # 6 cap
    c1, a1, _ = duo(dict(cap=True), dict(cap=True)); c2, a2, _ = duo()
    add("Headwear", "White cap", "should techs be drawn wearing the white cap with the terracotta house mark or bare-headed?",
        opt("cap", "White Cap", "White cap, terracotta house mark on the front.", "practical", c1, a1, ("Full uniform look", "Mark seen from far away")),
        opt("nocap", "No Cap", "Hair and face fully visible.", "warm", c2, a2, ("Faces and hair read better", "More personal")))
    # 7 sleeves
    o1 = dict(TA, sleeves="rolled"); c1 = Ctx(); a1 = place(c1, o1, 92, BASE, .62)[0] + zoom(c1, o1, 50, 118, 2.8, 186, 104, 44, "Rolled cuff")
    o2 = dict(TA); c2 = Ctx(); a2 = place(c2, o2, 92, BASE, .62)[0] + zoom(c2, o2, 50, 122, 2.8, 186, 104, 44, "Straight band")
    add("Sleeves", "Polo sleeves", "should polo sleeves be drawn rolled once at the cuff or straight with the stitched band?",
        opt("rolled", "Rolled Sleeves", "A single neat roll at the sleeve end.", "lively", c1, a1, ("Ready-to-work feel", "A bit more casual")),
        opt("straight", "Straight Sleeves", "Plain sleeve with a stitched rib band.", "calm", c2, a2, ("Crisp and uniform", "Matches the real polo")))
    # 8 callouts
    o = dict(TA, belt="toolbelt", tablet="hand", cap=True)
    c1 = Ctx(); a, m = place(c1, o, 100, BASE, .62); a1 = a
    for (lx, ly), (tx, ty), txt, an in (((112, 100), (150, 64), "Left-chest logo", "start"), ((112, 20), (150, 30), "White cap", "start"),
                                      ((136, 194), (166, 150), "Tablet", "start"), ((64, 212), (10, 176), "Tool belt", "start"), ((80, 396), (10, 230), "Logo shoe covers", "start")):
        px, py = m(lx, ly); a1 += callout(px, py, tx, ty, txt, an)
    c2, a2, _ = hero(dict(belt="toolbelt", tablet="hand", cap=True), cx=100)
    add("Labels", "Gear callout labels", "should a tech graphic name the gear with small callout labels or show the tech with no labels?",
        opt("labels", "Callout Labels", "Thin leader lines to cap, logo, tablet, belt and covers.", "practical", c1, a1, ("Explains the kit to investors", "Utility first")),
        opt("nolabels", "No Labels", "The same tech and gear, no text on the art.", "calm", c2, a2, ("Clean picture", "Words go in the caption")))
    # 9 layering
    c1, a1, _ = duo(dict(layer="softshell", shoes="boot"), dict(shoes="sneaker"))
    a1 += t(70, 16, "COLD DAYS", 7.5, MUTE, "hind", 700, "middle", 'letter-spacing="1"') + t(170, 16, "WARM DAYS", 7.5, MUTE, "hind", 700, "middle", 'letter-spacing="1"')
    c2, a2, _ = duo(dict(shoes="boot"), dict(shoes="sneaker"))
    add("Seasons", "Seasonal layering", "should brand graphics include a charcoal softshell over the polo for cold days or show the polo only?",
        opt("layer", "Softshell Over Polo", "Cold-day tech in the softshell and boots beside a polo tech.", "practical", c1, a1, ("Shows the year-round kit", "Boots for bad weather")),
        opt("polo", "Polo Only", "Both techs in polos; footwear still shows the weather.", "calm", c2, a2, ("One clear colour story", "Simpler set")))
    # 10 van
    c1 = Ctx(); a1 = van_bg(c1, -34, 128, .36) + place(c1, dict(TA), 160, BASE, .62)[0]
    c2, a2, _ = hero()
    add("Scene", "Van in the background", "should the tech stand in front of the branded van or alone on cream?",
        opt("van", "With The Van", "Tech in front with the white van and wordmark behind.", "lively", c1, a1, ("Says we come to you", "Brand shows twice")),
        opt("alone", "Tech Alone", "Just the tech on warm cream.", "calm", c2, a2, ("Focus on the person", "Fits small spaces")))
    return pairs
