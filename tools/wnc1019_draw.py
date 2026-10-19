"""WellNest collab sub-line mockups, Oct 19 2026 (Branding; Max asked 9:37 ICT: more PowerHaus and Buds Station decks, new designs that keep
the WellNest brand but differ more from the Roselle line). Clean drawn SVG only, every card tagged MOCKUP.
WellNest DNA kept in every mockup: the circle + script mark ("The WellNest", Caveat), cream #F5EEDF, IBM Plex Mono small print, a kraft cue.
NOT the Roselle architecture: no big cream rectangle on a kraft stand-up pouch, no bottom watercolour wash, no typewriter title.
PowerHaus Studio line: blue-led sporty palette, condensed caps, spring and arc patterns, slim tins, sash / spine / wrap labels.
Buds Station Lounge line: pink + butter + powder blue, rounded playful type, clouds, dots and a sleepy cat, round tins and jars.
Buds Station rules: no plant-leaf shapes at all, no temple or sacred imagery. Partner names set in type only (no partner logo artwork).
Each card is drawn on a 480x600 canvas, scaled .5 into the kit's 240x300 screen."""
import math, random
from draft_svg import screen, esc
CREAM, KRAFT, KRAFT_D, INKW, LOGO, MUTEW = "#F5EEDF", "#C79E6E", "#A97F52", "#3A3531", "#A9875F", "#6B625A"
MONO = 'font-family="IBM Plex Mono, Courier New, monospace"'; SCRIPT = 'font-family="Caveat, cursive"'
HIND = 'font-family="Hind, sans-serif"'; BEBAS = 'font-family="Bebas Neue, Oswald, sans-serif"'; OSW = 'font-family="Oswald, sans-serif"'
NUN = 'font-family="Nunito, sans-serif"'; MALI = 'font-family="Mali, Itim, sans-serif"'; FRAU = 'font-family="Fraunces, serif"'; DMS = 'font-family="DM Sans, sans-serif"'
_n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"
def T(x, y, s, size, col=INKW, fam=HIND, w=400, anchor="middle", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{col}" text-anchor="{anchor}" {fam} font-weight="{w}" {extra}>{esc(s)}</text>'
def R(x, y, w, h, fill, stroke="none", rx=0, sw=1, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def C(cx, cy, r, fill, stroke="none", sw=1, extra=""): return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def E(cx, cy, rx, ry, fill, stroke="none", sw=1): return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def G(inner, tx=0, ty=0, k=1, rot=0):
    return f'<g transform="translate({tx:.1f},{ty:.1f}) scale({k}){f" rotate({rot})" if rot else ""}">{inner}</g>'
# ---------- WellNest DNA ----------
def wn_mark(cx, cy, r=40, col=LOGO, ink=INKW):
    return (f'<g data-g="wellnest-mark">' + C(cx, cy, r, "none", col, max(1.2, r * .04)) + T(cx, cy - r * .12, "The", r * .46, ink, SCRIPT, 700)
            + T(cx, cy + r * .42, "WellNest", r * .58, ink, SCRIPT, 700) + '</g>')
def wn_word(x, y, size, ink=INKW, anchor="middle"): return T(x, y, "The WellNest", size, ink, SCRIPT, 700, anchor)
def partner(key, x, y, size, col, anchor="middle"):
    if key == "ph":
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{col}" text-anchor="{anchor}" {NUN} data-g="partner-name">'
                f'<tspan font-weight="800">PowerHaus</tspan><tspan font-weight="600"> Pilates</tspan></text>')
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{col}" text-anchor="{anchor}" {DMS} font-weight="700" data-g="partner-name">The Buds Station</text>'
def mock_tag(x=18, y=18, label="MOCKUP"):
    w = len(label) * 9.4 + 18
    return R(x, y, w, 26, "#FFFFFF", "#B9AE9C", 4, 1.4, 'stroke-dasharray="4 3"') + T(x + w / 2, y + 18, label, 13, MUTEW, MONO, 600, extra='letter-spacing="1.5"')
def foot(s, y=556):
    return R(0, y, 480, 600 - y, "#FFFFFFEE") + f'<line x1="0" y1="{y}" x2="480" y2="{y}" stroke="#E8E0D2"/>' + T(240, y + 28, s, min(19, 430 / (len(s) * .5)), INKW, HIND, 600)
def card(body, note, bg="#FBFAF7", tag="MOCKUP"):
    s = R(0, 0, 480, 600, bg) + body + mock_tag(label=tag) + (foot(note) if note else "")
    return screen(f'<g transform="scale(.5)">{s}</g>', bg)
def shadow(cx, y, rx): return E(cx, y, rx, rx * .09, "#0000001A")
def fit(s, maxw, k=.55, cap=60): return min(cap, maxw / (max(len(s), 1) * k))
# =====================================================================================
# POWERHAUS STUDIO LINE
# =====================================================================================
PHP = {  # palettes: main, accent, ink, pale
    "bluegold": ("#003CA7", "#F2C94C", "#1C2A4A", "#DFECFE"),
    "navylime": ("#1C2A4A", "#DCEB5A", "#1C2A4A", "#EEF3E0"),
    "skyblue": ("#5789FF", "#003CA7", "#1C2A4A", "#E8F0FF"),
    "whiteblue": ("#003CA7", "#003CA7", "#1C2A4A", "#FFFFFF"),
}
def springs(x0, y0, x1, y1, col, n=4, sw=2.4, op=.9):
    """Reformer-spring coils: n horizontal zigzag coils across the box."""
    s = f'<g opacity="{op}">'; gap = (y1 - y0) / n
    for i in range(n):
        y = y0 + gap * (i + .5); pts = [f"M{x0:.1f} {y:.1f}"]; x = x0; up = True
        while x < x1 - 8: x += 8; pts.append(f"L{x:.1f} {y + (-7 if up else 7):.1f}"); up = not up
        s += f'<path d="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>' + C(x0 - 4, y, 4, col) + C(x1 + 2, y, 4, col)
    return s + '</g>'
def arcs(x0, y0, x1, y1, col, n=5, sw=3, op=.9):
    """Long sweeping arcs (a reaching, lengthening movement line). Abstract; not the PowerHaus logo figure."""
    s = f'<g opacity="{op}">'; w = x1 - x0; h = y1 - y0
    for i in range(n):
        o = i * h / (n + 1)
        s += f'<path d="M{x0:.1f} {y1 - o * .3:.1f} Q{x0 + w * .45:.1f} {y0 + o:.1f} {x1:.1f} {y0 + o + h * .25:.1f}" fill="none" stroke="{col}" stroke-width="{sw - i * .35:.1f}" stroke-linecap="round"/>'
    return s + '</g>'
def dotgrid(x0, y0, x1, y1, col, step=16, r=2.4):
    return "".join(C(x, y, r, col) for x in range(int(x0), int(x1), step) for y in range(int(y0), int(y1), step))
def chevrons(x0, y0, x1, y1, col, step=26, sw=5):
    s = ""
    for y in range(int(y0), int(y1), step):
        s += f'<path d="M{x0} {y + 12} L{(x0 + x1) / 2:.1f} {y} L{x1} {y + 12}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return s
def ph_pattern(kind, box, col):
    x0, y0, x1, y1 = box
    return {"springs": lambda: springs(x0 + 10, y0, x1 - 10, y1, col), "arcs": lambda: arcs(x0, y0, x1, y1, col),
            "dots": lambda: dotgrid(x0 + 8, y0 + 8, x1, y1, col), "chevron": lambda: chevrons(x0 + 10, y0, x1 - 10, y1, col), None: lambda: ""}[kind]()
def ph_title(cfg, x, y, size, col, anchor="middle"):
    nm = cfg.get("name", "Recover")
    if cfg.get("type", "condensed") == "condensed": return T(x, y, nm.upper(), size * 1.25, col, BEBAS, 400, anchor, 'letter-spacing="3"')
    return T(x, y, nm.lower(), size, col, NUN, 800, anchor)
def ph_label(cfg, x, y, w, h, clip):
    """Label art inside a rectangle (tin body or pouch face): architecture spine | sash | wrap | block."""
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; arch = cfg.get("arch", "sash"); pat = cfg.get("pattern", "springs")
    bg = cfg.get("bg", "#FFFFFF"); cid = uid("phc")
    s = f'<defs><clipPath id="{cid}">{clip}</clipPath></defs><g clip-path="url(#{cid})">' + R(x, y, w, h, bg)
    cx = x + w / 2
    if arch == "spine":
        sw = w * .26; s += R(x, y, sw, h, m) + G(ph_pattern(pat, (0, 0, sw, h), a), x, y)
        s += f'<text transform="translate({x + sw * .66:.1f},{y + h - 24:.1f}) rotate(-90)" font-size="{sw * .55:.1f}" fill="#FFFFFF" {NUN} font-weight="800" data-g="partner-name">PowerHaus</text>'
        tx = x + sw + (w - sw) / 2
        s += wn_mark(tx, y + h * .2, min(w * .16, 34)) + ph_title(cfg, tx, y + h * .5, fit(cfg.get("name", "Recover"), w - sw - 20, .62, 38), ink)
        s += R(tx - 30, y + h * .56, 60, 4, a) + T(tx, y + h * .66, "STUDIO TEA", 13, MUTEW, MONO, 600, extra='letter-spacing="2"')
        s += T(tx, y + h * .9, "MOCKUP · NET WT TBC", 10, MUTEW, MONO)
    elif arch == "sash":
        s += f'<path d="M{x} {y + h * .62} L{x + w} {y + h * .30} L{x + w} {y + h * .52} L{x} {y + h * .84} Z" fill="{m}"/>'
        s += f'<g clip-path="url(#{cid})"><path d="M{x} {y + h * .84} L{x + w} {y + h * .52} L{x + w} {y + h} L{x} {y + h} Z" fill="{pale}"/></g>'
        s += G(ph_pattern(pat, (0, 0, w, h * .3), m), x, y + h * .66)
        s += wn_mark(cx, y + h * .14, min(w * .15, 32)) + ph_title(cfg, cx, y + h * .36, fit(cfg.get("name", "Recover"), w - 24, .62, 40), ink)
        s += f'<text transform="translate({cx:.1f},{y + h * .6:.1f}) rotate({-math.degrees(math.atan2(h * .32, w)):.1f})" font-size="{min(20, w * .1):.1f}" fill="#FFFFFF" text-anchor="middle" {NUN} font-weight="800" data-g="partner-name">× PowerHaus Pilates</text>'
    elif arch == "wrap":
        s += R(x, y, w, h, pale) + G(ph_pattern(pat, (0, 0, w, h), m if pale != "#FFFFFF" else m + "55"), x, y)
        bh = h * .38; by = y + h * .3
        s += R(x, by, w, bh, bg) + R(x, by, w, 5, a) + R(x, by + bh - 5, w, 5, a)
        s += wn_mark(x + w * .2, by + bh / 2, min(bh * .32, 28)) + ph_title(cfg, x + w * .6, by + bh * .5, fit(cfg.get("name", "Recover"), w * .55, .62, 34), ink)
        s += partner("ph", x + w * .6, by + bh * .8, min(14, w * .07), m)
    else:  # block: full colour face, white type
        s += R(x, y, w, h, m) + G(ph_pattern(pat, (0, 0, w, h * .45), a), x, y + h * .55)
        s += C(cx, y + h * .17, min(w * .15, 32) + 6, "#FFFFFF") + wn_mark(cx, y + h * .17, min(w * .15, 32))
        s += ph_title(cfg, cx, y + h * .42, fit(cfg.get("name", "Recover"), w - 24, .62, 40), "#FFFFFF") + partner("ph", cx, y + h * .5, min(15, w * .075), a)
    return s + '</g>'
def ph_tin(cfg, cx, base, w=150, h=280):
    """Slim tall cylinder tin with a lid."""
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; x = cx - w / 2; y = base - h; ry = w * .14
    lid = cfg.get("lid", "dip"); fin = cfg.get("finish", "matte"); gid = uid("phg")
    lidc = {"dip": m, "kraft": KRAFT, "white": "#FFFFFF", "metal": "#C9CED6"}[lid]
    s = shadow(cx, base + 4, w * .62)
    s += f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset=".2" stop-color="#000" stop-opacity="0"/><stop offset=".72" stop-color="#FFF" stop-opacity="{.35 if fin == "gloss" else .12}"/><stop offset=".8" stop-color="#FFF" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient></defs>'
    body = f'<path d="M{x} {y + 40} L{x} {base} A{w / 2} {ry} 0 0 0 {x + w} {base} L{x + w} {y + 40} Z"/>'
    if fin == "metal": s += f'<path d="M{x} {y + 40} L{x} {base} A{w / 2} {ry} 0 0 0 {x + w} {base} L{x + w} {y + 40} Z" fill="#D5D9DF"/>'
    s += ph_label(dict(cfg, bg="#FFFFFF" if fin != "metal" else "#E4E7EB"), x, y + 40, w, h - 40 + ry, body)
    s += f'<path d="M{x} {y + 40} L{x} {base} A{w / 2} {ry} 0 0 0 {x + w} {base} L{x + w} {y + 40} Z" fill="url(#{gid})" stroke="#00000030"/>'
    s += f'<path d="M{x - 3} {y + 12} L{x - 3} {y + 42} A{w / 2 + 3} {ry} 0 0 0 {x + w + 3} {y + 42} L{x + w + 3} {y + 12} Z" fill="{lidc}" stroke="#00000030"/>'
    if lid == "kraft": s += f'<path d="M{x - 3} {y + 30} A{w / 2 + 3} {ry} 0 0 0 {x + w + 3} {y + 30}" fill="none" stroke="{m}" stroke-width="7"/>'
    s += E(cx, y + 12, w / 2 + 3, ry, lidc if lid != "dip" else m, "#00000030") + E(cx, y + 12, w / 2 - 8, ry - 5, "#FFFFFF22")
    s += f'<path d="M{x - 3} {y + 12} L{x - 3} {y + 42} A{w / 2 + 3} {ry} 0 0 0 {x + w + 3} {y + 42} L{x + w + 3} {y + 12} Z" fill="url(#{gid})"/>'
    return s
def ph_boxpouch(cfg, cx, base, w=200, h=300):
    """Flat-bottom box pouch seen in 3/4: front face + side gusset, label art covers the whole front (no cream rectangle)."""
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; x = cx - w / 2 - 20; y = base - h; g = 42
    s = shadow(cx, base + 4, w * .65)
    s += f'<path d="M{x + w} {y + 6} L{x + w + g} {y + 16} L{x + w + g} {base - 8} L{x + w} {base} Z" fill="{m}" opacity=".85"/>'
    s += f'<path d="M{x + w} {y + 6} L{x + w + g} {y + 16} L{x + w + g} {base - 8} L{x + w} {base} Z" fill="#00000022"/>'
    face = f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
    s += ph_label(cfg, x, y, w, h, face) + R(x, y, w, h, "none", "#00000030")
    s += R(x, y, w, 26, "#00000010") + f'<line x1="{x}" y1="{y + 30}" x2="{x + w}" y2="{y + 30}" stroke="#00000033" stroke-dasharray="3 3"/>'
    return s
def ph_stickbox(cfg, cx, base, w=210, h=150):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; x = cx - w / 2; y = base - h
    s = shadow(cx, base + 4, w * .6) + f'<path d="M{x} {y} L{x + 26} {y - 22} L{x + w + 26} {y - 22} L{x + w} {y} Z" fill="{pale}" stroke="#00000030"/>'
    s += f'<path d="M{x + w} {y} L{x + w + 26} {y - 22} L{x + w + 26} {base - 22} L{x + w} {base} Z" fill="{m}" stroke="#00000030"/>'
    s += ph_label(dict(cfg, arch="wrap"), x, y, w, h, f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>') + R(x, y, w, h, "none", "#00000030")
    for i in range(4):  # stick packs poking out of the open top
        sx = x + 40 + i * 40; s += R(sx, y - 70 + i * 6, 26, 70, "#FFFFFF", "#00000030", 3) + R(sx, y - 70 + i * 6, 26, 14, m if i % 2 else a)
    return s + T(cx, base + 30, "10 stick packs (mockup count)", 13, MUTEW, MONO)
def ph_sachet_tin(cfg, cx, base):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; w, h = 230, 110; x = cx - w / 2; y = base - h
    s = shadow(cx, base + 4, w * .6) + R(x, y, w, h, "#FFFFFF", "#00000030", 14)
    s += ph_label(dict(cfg, arch="wrap"), x + 6, y + 6, w - 12, h - 12, f'<rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" rx="10"/>')
    for i in range(3):
        px = x + 30 + i * 62; s += f'<path d="M{px} {y - 10} L{px + 26} {y - 60} L{px + 52} {y - 10} Z" fill="#FFFFFFEE" stroke="{m}" stroke-width="2"/>' + R(px + 22, y - 82, 8, 22, a)
    return s + T(cx, base + 30, "Pyramid sachets in a flat tin", 13, MUTEW, MONO)
def ph_bottle(cfg, cx, base, style="clear"):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; w, h = 110, 300; x = cx - w / 2; y = base - h; gid = uid("phb")
    tea = "#B8452E"
    s = shadow(cx, base + 4, 70)
    s += f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".1"/><stop offset=".25" stop-color="#FFF" stop-opacity=".55"/><stop offset=".4" stop-color="#FFF" stop-opacity="0"/></linearGradient></defs>'
    path = f'M{cx - 18} {y} L{cx + 18} {y} L{cx + 18} {y + 50} Q{x + w} {y + 70} {x + w} {y + 110} L{x + w} {base - 10} Q{x + w} {base} {x + w - 10} {base} L{x + 10} {base} Q{x} {base} {x} {base - 10} L{x} {y + 110} Q{x} {y + 70} {cx - 18} {y + 50} Z'
    s += f'<path d="{path}" fill="{tea if style == "clear" else "#E9DCD6"}" opacity="{.9 if style == "clear" else 1}" stroke="#00000030"/>'
    if style == "frost": s += f'<path d="{path}" fill="{tea}" opacity=".35"/>'
    s += R(cx - 20, y - 26, 40, 30, m, "#00000030", 4)
    if style == "clear":
        s += ph_label(dict(cfg, arch="wrap"), x, y + 140, w, 110, f'<rect x="{x}" y="{y + 140}" width="{w}" height="110"/>')
    else:
        s += ph_label(dict(cfg, arch="block"), x + 14, y + 130, w - 28, 140, f'<rect x="{x + 14}" y="{y + 130}" width="{w - 28}" height="140" rx="6"/>')
        s += f'<path d="M{cx} {y + 30} q30 10 40 40" fill="none" stroke="{a}" stroke-width="2"/>' + R(cx + 28, y + 66, 46, 30, KRAFT, "#00000030", 3) + C(cx + 51, y + 74, 3, "#FFFFFF")
    s += f'<path d="{path}" fill="url(#{gid})"/>'
    return s
# ---- PowerHaus context scenes ----
def studio_bg(floor="#E9D9BF"):
    """Bright studio: white wall, light maple floor, a soft arched mirror outline (studio photos show arched mirrors)."""
    return (R(0, 0, 480, 600, "#FFFFFF") + R(0, 400, 480, 200, floor) + "".join(f'<line x1="{i}" y1="400" x2="{i - 60}" y2="600" stroke="#D8C6A6"/>' for i in range(40, 560, 60))
            + f'<path d="M330 400 L330 150 Q330 90 390 90 Q450 90 450 150 L450 400" fill="#EEF4FA" stroke="#D6DCE4" stroke-width="3"/>')
def reformer(x, y, k=1):
    return G(R(0, 0, 240, 22, "#D9C29C", "#B89E74", 4) + R(30, -14, 90, 16, "#E9E4DA", "#B8B0A2", 3) + R(4, 22, 10, 30, "#B89E74") + R(226, 22, 10, 30, "#B89E74")
             + f'<path d="M200 -4 L230 -40" stroke="#9AA0A8" stroke-width="4"/>', x, y, k)
def ph_scene(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]
    if kind == "crate":  # front-desk crate of tins
        s = studio_bg() + reformer(40, 470, .7) + R(70, 360, 340, 18, "#D9C29C", "#B89E74", 3) + R(80, 378, 320, 140, "#FFFFFF", "#D6D0C6")
        s += R(140, 250, 200, 110, "#D9C29C", "#A98E64", 6) + R(140, 250, 200, 26, m) + partner("ph", 240, 269, 17, "#FFFFFF") + wn_word(240, 340, 26)
        for i in range(4): s += G(ph_tin(dict(cfg, lid="dip"), 0, 0, 40, 76), 165 + i * 50, 248, 1)
        return s
    if kind == "cubby":
        s = studio_bg() + R(50, 140, 250, 270, "#F4EBDD", "#C8B593", 4)
        for r in range(3):
            for c in range(3):
                bx, by = 58 + c * 82, 150 + r * 86; s += R(bx, by, 76, 80, "#FFFFFF", "#D8CBB1")
                if (r + c) % 2 == 0: s += G(ph_tin(cfg, 0, 0, 34, 66), bx + 38, by + 76, 1)
                else: s += R(bx + 10, by + 30, 56, 46, m if c == 1 else pale, "#00000022", 4)
        return s + R(50, 112, 250, 28, m) + T(175, 132, "TAKE A TIN HOME", 18, "#FFFFFF", BEBAS, 400, extra='letter-spacing="2"')
    if kind == "dispenser":
        s = studio_bg() + R(60, 330, 260, 16, "#D9C29C", "#B89E74", 3) + R(70, 346, 240, 60, "#FFFFFF", "#D6D0C6")
        s += R(110, 170, 110, 160, "#FFFFFF", "#C9CED6", 10) + R(110, 170, 110, 46, m, "none", 10) + R(110, 200, 110, 16, m)
        s += T(165, 200, "STUDIO TEA", 20, "#FFFFFF", BEBAS, 400, extra='letter-spacing="2"') + wn_mark(165, 262, 26) + R(155, 318, 20, 14, "#9AA0A8")
        for i in range(3): s += f'<path d="M{238 + i * 26} 330 l4 -40 h18 l4 40 z" fill="#FFFFFF" stroke="{m}" stroke-width="2"/>' + R(242 + i * 26, 304, 18, 6, a)
        return s + T(165, 384, "Help yourself after class", 15, ink, HIND, 600)
    if kind == "tray":
        s = studio_bg() + R(60, 300, 280, 140, "#D9C29C", "#A98E64", 14) + R(70, 310, 260, 120, "#E7D3B0", "none", 10)
        for i in range(3):
            gx = 110 + i * 90; s += f'<path d="M{gx - 26} 330 L{gx - 20} 410 L{gx + 20} 410 L{gx + 26} 330 Z" fill="#B8452ECC" stroke="#00000030"/>' + R(gx - 26, 322, 52, 10, "#FFFFFFAA")
        return s + R(90, 440, 220, 40, "#FFFFFF", m, 6, 2) + T(200, 466, "TEA AFTER CLASS · MOCKUP", 15, m, MONO, 600)
    if kind == "shelfrow":
        s = R(0, 0, 480, 600, "#FFFFFF") + R(30, 380, 420, 14, "#D9C29C") + R(30, 394, 420, 30, m) + T(240, 415, "WELLNEST × POWERHAUS STUDIO TEA", 15, "#FFFFFF", MONO, 600)
        for i in range(5): s += G(ph_tin(cfg, 0, 0, 62, 140), 70 + i * 85, 380, 1)
        return s
    if kind == "pyramid":
        s = R(0, 0, 480, 600, "#FFFFFF") + R(60, 470, 360, 14, "#D9C29C")
        pos = [(130, 470), (195, 470), (260, 470), (325, 470), (162, 380), (227, 380), (292, 380), (195, 290), (260, 290)]
        for (px, py) in pos: s += G(ph_tin(cfg, 0, 0, 58, 90), px, py, 1)
        return s + R(150, 500, 180, 34, pale, m, 4, 2) + partner("ph", 240, 523, 15, m)
def ph_menu(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]
    if kind == "tent":
        s = R(0, 0, 480, 600, "#F4F1EA") + f'<path d="M100 470 L160 120 L320 120 L380 470 Z" fill="#E6DFD1"/>' + f'<path d="M120 480 L160 130 L320 130 L360 480 Z" fill="#FFFFFF" stroke="#D6D0C6"/>'
        s += R(160, 130, 160, 52, m) + T(240, 166, "AFTER CLASS", 26, "#FFFFFF", BEBAS, 400, extra='letter-spacing="2"')
        for i, (nm, d) in enumerate((("Recover", "hot · iced"), ("Studio Tea", "tin to take home"), ("Stick Packs", "for your bag"))):
            yy = 230 + i * 62; s += T(150 + i * 3, yy, nm, 22, ink, OSW, 600, "start") + T(150 + i * 3, yy + 22, d, 13, MUTEW, MONO, 400, "start") + R(150, yy + 32, 180 - i * 6, 2, a)
        return s + wn_mark(240, 430, 26) + T(240, 520, "No prices shown: mockup", 13, MUTEW, MONO)
    s = R(0, 0, 480, 600, "#FFFFFF") + R(70, 90, 340, 400, ink, "#00000040", 6) + R(80, 100, 320, 380, "none", a, 4, 2)
    s += T(240, 150, "STUDIO TEA BAR", 36, "#FFFFFF", BEBAS, 400, extra='letter-spacing="3"') + G(springs(0, 0, 200, 22, a, 1, 2), 140, 160)
    for i, (nm, d) in enumerate((("RECOVER", "hot or iced"), ("STICK PACK", "to go"), ("TIN", "take one home"))):
        yy = 240 + i * 62; s += T(110, yy, nm, 26, "#FFFFFF", BEBAS, 400, "start", 'letter-spacing="2"') + T(370, yy, d, 15, "#FFFFFFCC", MONO, 400, "end") + R(110, yy + 18, 260, 1.5, "#FFFFFF33")
    return s + T(240, 440, "The WellNest × PowerHaus Pilates", 22, "#FFFFFF", SCRIPT, 700) + T(240, 520, "Wall board, no prices: mockup", 13, MUTEW, MONO)
def ph_merch(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; s = R(0, 0, 480, 600, "#FFFFFF")
    if kind == "tumbler":
        s += shadow(240, 500, 80) + f'<path d="M180 150 L300 150 L288 496 Q240 508 192 496 Z" fill="{m}" stroke="#00000030"/>' + R(170, 120, 140, 34, "#E4E7EB", "#00000030", 8)
        s += R(226, 96, 28, 30, "#C9CED6") + G(arcs(0, 0, 110, 90, a, 4, 3), 186, 340) + T(240, 250, "RECOVER", 36, "#FFFFFF", BEBAS, 400, extra='letter-spacing="3"') + wn_mark(240, 300, 24, "#FFFFFF", "#FFFFFF")
        return s + T(240, 548 - 20, "Insulated tumbler", 15, MUTEW, MONO)
    if kind == "mug":
        s += shadow(220, 470, 90) + R(140, 260, 160, 210, "#FFFFFF", "#C9CED6", 10, 3) + f'<path d="M300 300 q60 0 60 50 q0 50 -60 50" fill="none" stroke="#C9CED6" stroke-width="16"/>'
        s += R(140, 260, 160, 22, m, "none", 10) + R(140, 272, 160, 10, m) + wn_mark(220, 340, 30) + partner("ph", 220, 410, 16, m) + E(220, 262, 80, 10, "#EDE7DD")
        return s + T(240, 528, "Enamel mug", 15, MUTEW, MONO)
    if kind == "towel":
        s += f'<path d="M110 160 L370 160 L370 470 L110 470 Z" fill="{pale}" stroke="#00000020"/>' + R(110, 410, 260, 30, m) + R(110, 446, 260, 8, a)
        s += "".join(f'<line x1="{x}" y1="470" x2="{x}" y2="486" stroke="{pale}" stroke-width="3"/>' for x in range(116, 370, 8))
        s += wn_mark(240, 260, 34) + T(240, 340, "STUDIO", 24, m, BEBAS, 400, extra='letter-spacing="4"') + partner("ph", 240, 431, 15, "#FFFFFF")
        return s + T(240, 528, "Mat towel, stitched mark", 15, MUTEW, MONO)
    if kind == "tote":
        s += f'<path d="M190 200 Q190 120 240 120 Q290 120 290 200" fill="none" stroke="{KRAFT_D}" stroke-width="10"/>' + R(130, 190, 220, 290, "#F3EDE1", "#00000025", 4)
        s += R(130, 190, 50, 290, m) + f'<text transform="translate(165,450) rotate(-90)" font-size="24" fill="#FFFFFF" {NUN} font-weight="800">PowerHaus</text>'
        s += wn_mark(265, 270, 32) + T(265, 350, "RECOVER", 30, ink, BEBAS, 400, extra='letter-spacing="3"') + G(springs(0, 0, 120, 30, a, 1, 2.4), 205, 380)
        return s + T(240, 528, "Canvas tote", 15, MUTEW, MONO)
    if kind == "stamp":
        s += R(80, 170, 320, 200, "#FFFFFF", "#D6D0C6", 12) + R(80, 170, 320, 50, m, "none", 12) + R(80, 200, 320, 20, m)
        s += T(240, 205, "AFTER-CLASS CUP CARD", 22, "#FFFFFF", BEBAS, 400, extra='letter-spacing="2"')
        for i in range(8):
            px, py = 125 + (i % 4) * 76, 260 + (i // 4) * 60
            s += C(px, py, 22, a if i < 3 else "none", m, 2) + (T(px, py + 7, "WN", 16, ink, SCRIPT, 700) if i < 3 else "")
        return s + T(240, 410, "Stamp card: perk wording TBC with the studio", 14, MUTEW, MONO)
    if kind == "punch":
        s += R(150, 120, 180, 320, "#FFFFFF", "#D6D0C6", 14) + R(150, 120, 180, 90, ink, "none", 14) + R(150, 180, 180, 30, ink)
        s += T(240, 175, "CUP CARD", 30, "#FFFFFF", BEBAS, 400, extra='letter-spacing="3"')
        for i in range(6):
            yy = 240 + i * 30; s += C(190, yy, 9, "#FFFFFF" if i < 2 else pale, m, 2) + R(210, yy - 3, 90, 6, pale, "none", 3)
            if i < 2: s += C(190, yy, 9, "#F4F1EA")
        return s + wn_word(240, 420, 22) + T(240, 480, "Punch card: perk wording TBC with the studio", 14, MUTEW, MONO)
    if kind == "giftbox":
        s += shadow(240, 470, 140) + R(110, 300, 260, 170, m, "#00000030", 6) + R(100, 270, 280, 40, m, "#00000030", 6) + R(225, 270, 30, 200, a)
        s += f'<path d="M240 270 q-50 -50 -70 -10 q20 20 70 10 q50 -50 70 -10 q-20 20 -70 10" fill="{a}" stroke="#00000030"/>' + R(150, 360, 70, 70, "#FFFFFF", "none", 4) + wn_mark(185, 395, 26)
        return s + T(240, 520, "Class-gift box", 15, MUTEW, MONO)
    if kind == "trio":
        s += R(80, 410, 320, 20, "#D9C29C")
        for i, pal in enumerate(("bluegold", "skyblue", "navylime")): s += G(ph_tin(dict(cfg, pal=pal), 0, 0, 80, 170), 150 + i * 90, 410, 1)
        return s + T(240, 480, "Mini tin trio", 15, MUTEW, MONO)
def ph_icons(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; s = R(0, 0, 480, 600, "#FFFFFF") + T(240, 100, "BACK-PANEL ICONS", 18, MUTEW, MONO, 600, extra='letter-spacing="2"')
    labels = ("Steep", "Pour", "Sip", "Refill")
    for i, lb in enumerate(labels):
        cx, cy = 140 + (i % 2) * 200, 200 + (i // 2) * 170
        if kind == "num":
            s += C(cx, cy, 46, m) + T(cx, cy + 22, str(i + 1).zfill(2), 56, "#FFFFFF", BEBAS, 400)
        else:
            s += C(cx, cy, 46, pale, m, 3)
            d = [f"M{cx - 24} {cy + 16} Q{cx} {cy - 34} {cx + 24} {cy - 10}", f"M{cx - 26} {cy} L{cx + 26} {cy}", f"M{cx - 20} {cy + 20} Q{cx} {cy - 30} {cx + 20} {cy + 20}",
                 f"M{cx - 22} {cy + 12} A24 24 0 1 1 {cx + 22} {cy + 12}"][i]
            s += f'<path d="{d}" fill="none" stroke="{m}" stroke-width="5" stroke-linecap="round"/>' + C(cx - 24, cy + 16 if i != 1 else cy, 6, a)
        s += T(cx, cy + 80, lb.upper(), 22, ink, BEBAS, 400, extra='letter-spacing="2"')
    return s
def ph_badge(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; s = R(0, 0, 480, 600, "#FBFAF7")
    if kind == "seal":
        s += C(240, 280, 150, "#FFFFFF", m, 4) + C(240, 280, 132, "none", a, 2, 'stroke-dasharray="2 6"')
        s += wn_mark(240, 230, 46) + T(240, 316, "×", 28, ink) + partner("ph", 240, 356, 26, m)
        return s + T(240, 470, "Round co-brand seal (lid or back)", 15, MUTEW, MONO)
    s += R(40, 220, 400, 110, "#FFFFFF", m, 8, 3) + R(40, 220, 140, 110, pale, "none", 8) + wn_mark(110, 275, 40)
    s += f'<line x1="196" y1="240" x2="196" y2="310" stroke="{a}" stroke-width="4"/>' + partner("ph", 312, 288, 30, m)
    return s + T(240, 470, "Side-by-side bar, split by a gold rule", 15, MUTEW, MONO)
def ph_back(cfg, kind):
    m, a, ink, pale = PHP[cfg.get("pal", "bluegold")]; s = R(0, 0, 480, 600, "#F4F1EA") + R(90, 70, 300, 440, "#FFFFFF", "#D6D0C6", 6) + R(90, 70, 300, 40, m, "none", 6) + R(90, 96, 300, 14, m)
    s += T(240, 98, "BACK OF TIN", 18, "#FFFFFF", MONO, 600, extra='letter-spacing="2"')
    if kind == "grid":
        cells = (("BREW", "ratio TBC"), ("STEEP", "time TBC"), ("INGREDIENTS", "per final recipe"), ("MADE BY", "The WellNest"), ("WITH", "PowerHaus Pilates"), ("PACKED", "Chiang Mai"))
        for i, (k, v) in enumerate(cells):
            cx, cy = 110 + (i % 2) * 140, 130 + (i // 2) * 110
            s += R(cx, cy, 130, 100, pale if i % 3 == 0 else "#FFFFFF", "#D6D0C6", 4) + T(cx + 12, cy + 34, k, 16, m, BEBAS, 400, "start", 'letter-spacing="2"') + T(cx + 12, cy + 64, v, 12.5, ink, MONO, 400, "start")
    else:
        steps = (("BEFORE CLASS", "fill your bottle"), ("AFTER CLASS", "steep one stick pack"), ("AT HOME", "hot or iced, your way"))
        s += f'<line x1="140" y1="150" x2="140" y2="420" stroke="{m}" stroke-width="4"/>'
        for i, (k, v) in enumerate(steps):
            yy = 160 + i * 120; s += C(140, yy, 16, a, m, 3) + T(170, yy - 2, k, 24, ink, BEBAS, 400, "start", 'letter-spacing="2"') + T(170, yy + 24, v, 14, MUTEW, MONO, 400, "start")
    return s + wn_word(240, 486, 26)
def ph_hero(cfg, obj="tin", note=None):
    """Single product on a clean light surface."""
    s = R(0, 0, 480, 600, "#FBFAF7") + R(0, 470, 480, 130, "#F1ECE3")
    if obj == "tin": s += ph_tin(cfg, 240, 500, 170, 340)
    elif obj == "pouch": s += ph_boxpouch(cfg, 240, 510, 210, 330)
    elif obj == "sticks": s += ph_stickbox(cfg, 230, 450)
    elif obj == "sachet": s += ph_sachet_tin(cfg, 240, 420)
    elif obj == "bottle": s += ph_bottle(cfg, 240, 510, cfg.get("bottle", "clear"))
    return s
# =====================================================================================
# BUDS STATION LOUNGE LINE (no plant-leaf shapes, no temple / sacred imagery)
# =====================================================================================
BSP = {  # main, second, ink, light
    "pinkbutter": ("#D9667E", "#F2D37A", "#5A3440", "#FCE9EE"),
    "coralpowder": ("#E3806F", "#9DC3D0", "#4A3A3A", "#FDEDE6"),
    "lilacpink": ("#B79AD9", "#F2A7BC", "#3F3550", "#F4EEFB"),
    "pinkteal": ("#D9667E", "#7FA9B0", "#4A3A3A", "#FFF4F6"),
}
def cloud(cx, cy, w, fill, stroke="none", sw=2):
    h = w * .5; r = w * .2
    d = (f"M{cx - w / 2 + r} {cy + h / 2} A{r} {r} 0 0 1 {cx - w / 2 + r * .6} {cy} A{r * 1.2} {r * 1.2} 0 0 1 {cx - r * .6} {cy - h * .45} "
         f"A{r * 1.5} {r * 1.5} 0 0 1 {cx + r * 1.3} {cy - h * .3} A{r * 1.1} {r * 1.1} 0 0 1 {cx + w / 2 - r * .3} {cy + h * .15} A{r} {r} 0 0 1 {cx + w / 2 - r} {cy + h / 2} Z")
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def star(cx, cy, r, fill):
    pts = " ".join(f"{cx + (r if i % 2 == 0 else r * .45) * math.sin(i * math.pi / 5):.1f},{cy - (r if i % 2 == 0 else r * .45) * math.cos(i * math.pi / 5):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{fill}"/>'
def sparkle(cx, cy, r, fill): return f'<path d="M{cx} {cy - r} Q{cx + r * .2} {cy - r * .2} {cx + r} {cy} Q{cx + r * .2} {cy + r * .2} {cx} {cy + r} Q{cx - r * .2} {cy + r * .2} {cx - r} {cy} Q{cx - r * .2} {cy - r * .2} {cx} {cy - r} Z" fill="{fill}"/>'
def cat(cx, cy, k, body, ink):
    """Sleepy curled cat (round body, two ears, curled tail, closed eyes)."""
    s = (f'<g stroke="{ink}" stroke-opacity=".55" stroke-width="2.4">' + f'<path d="M-46 -16 L-44 -36 L-32 -22 Z M-24 -24 L-16 -40 L-12 -20 Z" fill="{body}"/>' + E(0, 10, 46, 26, body) + C(-30, -6, 20, body) + '</g>' + C(-30, -6, 18.8, body)
         + f'<path d="M-46 -16 L-44 -36 L-32 -22 Z M-24 -24 L-16 -40 L-12 -20 Z" fill="{body}"/>'
         + f'<path d="M40 18 Q66 10 52 -10 Q44 -20 36 -10" fill="none" stroke="{body}" stroke-width="9" stroke-linecap="round"/>'
         + f'<path d="M-40 -6 q4 4 8 0 M-26 -6 q4 4 8 0" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>' + E(-29, 2, 2.4, 1.8, ink))
    return G(s, cx, cy, k)
def paws(x0, y0, x1, y1, col, step=48):
    s = ""; rnd = random.Random(5)
    for y in range(int(y0) + 10, int(y1), step):
        for x in range(int(x0) + (20 if (y // step) % 2 else 0), int(x1), step + 8):
            px, py = x + rnd.uniform(-4, 4), y + rnd.uniform(-4, 4)
            s += E(px, py + 6, 10, 8.5, col) + "".join(C(px + dx, py - 7 - (2 if abs(dx) < 5 else 0), 4, col) for dx in (-10, -3.5, 3.5, 10))
    return s
def bs_pattern(kind, box, cfg):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; x0, y0, x1, y1 = box; s = ""; rnd = random.Random(11)
    if kind == "clouds":
        for i in range(14): s += cloud(rnd.uniform(x0 + 10, x1 - 10), rnd.uniform(y0 + 16, y1 - 10), rnd.uniform(40, 70), "#FFFFFF" if i % 2 else sc + "AA", m + "66", 2)
    elif kind == "dots":
        for i in range(30): s += C(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(3, 7), sc if i % 3 else "#FFFFFF")
        for i in range(6): s += sparkle(rnd.uniform(x0, x1), rnd.uniform(y0, y1), 9, "#FFFFFF")
    elif kind == "paws": s += paws(x0, y0, x1, y1, m + "88", 56)
    elif kind == "stripes":
        for i, c in enumerate((m, sc, lt, sc, m)): s += R(x0, y0 + i * (y1 - y0) / 5, x1 - x0, (y1 - y0) / 5 + 1, c)
    elif kind == "rainbow":
        cx, cy = (x0 + x1) / 2, y1
        for i, c in enumerate((m, sc, "#9DC3D0", "#FFFFFF")): s += f'<path d="M{cx - 90 + i * 16} {cy} A{90 - i * 16} {90 - i * 16} 0 0 1 {cx + 90 - i * 16} {cy}" fill="none" stroke="{c}" stroke-width="14"/>'
    return s
def bs_title(cfg, x, y, size, col, anchor="middle"):
    nm = cfg.get("name", "Unwind")
    if cfg.get("type", "bubbly") == "bubbly": return T(x, y, nm.lower(), size, col, MALI, 600, anchor)
    return (T(x + 3, y + 3, nm.upper(), size * .9, cfg.get("shadow", "#F2D37A"), FRAU, 700, anchor, 'letter-spacing="2"')
            + T(x, y, nm.upper(), size * .9, col, FRAU, 700, anchor, f'letter-spacing="2" stroke="{col}" stroke-width=".6"'))
def bs_label(cfg, cx, cy, w, k=1):
    """Front label: cloud die-cut | round badge | ticket | full (no label, print on body)."""
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; lab = cfg.get("label", "cloud"); s = ""
    if lab == "cloud":
        s += cloud(cx, cy + w * .05, w * 1.1, "#FFFFFF", m, 3) + wn_mark(cx - w * .27, cy + w * .06, w * .085)
        s += bs_title(dict(cfg, shadow=sc), cx + w * .1, cy + w * .08, fit(cfg.get("name", "Unwind"), w * .44, .55, w * .15), ink)
        s += T(cx + w * .1, cy + w * .16, "with The Buds Station", w * .05, m, DMS, 700)
    elif lab == "badge":
        s += C(cx, cy, w * .42, "#FFFFFF", m, 3) + C(cx, cy, w * .37, "none", sc, 2, 'stroke-dasharray="3 5"')
        s += wn_mark(cx, cy - w * .2, w * .075) + bs_title(dict(cfg, shadow=sc), cx, cy + w * .07, fit(cfg.get("name", "Unwind"), w * .56, .55, w * .15), ink)
        s += T(cx, cy + w * .18, "with The Buds Station", w * .048, m, DMS, 700)
    elif lab == "ticket":
        s += f'<path d="M{cx - w * .45} {cy - w * .2} h{w * .9} v{w * .12} a{w * .06} {w * .06} 0 0 0 0 {w * .16} v{w * .12} h{-w * .9} v{-w * .12} a{w * .06} {w * .06} 0 0 0 0 {-w * .16} Z" fill="#FFFFFF" stroke="{m}" stroke-width="3"/>'
        s += wn_mark(cx - w * .28, cy, w * .09) + f'<line x1="{cx - w * .14}" y1="{cy - w * .17}" x2="{cx - w * .14}" y2="{cy + w * .17}" stroke="{sc}" stroke-width="3" stroke-dasharray="4 4"/>'
        s += bs_title(dict(cfg, shadow=sc), cx + w * .15, cy + w * .02, fit(cfg.get("name", "Unwind"), w * .5, .55, w * .14), ink) + T(cx + w * .15, cy + w * .12, "with The Buds Station", w * .045, m, DMS, 700)
    return s
def bs_tin(cfg, cx, base, w=220, h=170):
    """Short round tin, body fully printed (pattern + colour), lid on top."""
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; x = cx - w / 2; y = base - h; ry = w * .16; cid = uid("bsc"); gid = uid("bsg")
    lidk = cfg.get("lid", "plain"); fin = cfg.get("finish", "matte")
    s = shadow(cx, base + 6, w * .58)
    body = f'M{x} {y + 30} L{x} {base} A{w / 2} {ry} 0 0 0 {x + w} {base} L{x + w} {y + 30} Z'
    s += f'<defs><clipPath id="{cid}"><path d="{body}"/></clipPath><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".12"/><stop offset=".25" stop-color="#FFF" stop-opacity="{.5 if fin == "gloss" else .08}"/><stop offset=".34" stop-color="#FFF" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient></defs>'
    s += f'<g clip-path="url(#{cid})">' + R(x, y, w, h + ry, cfg.get("body", lt))
    if cfg.get("split"): s += R(x, y + 30 + (h - 30) * .55, w, h, m)
    if cfg.get("grad"):
        g2 = uid("bsl"); s += f'<defs><linearGradient id="{g2}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lt}"/><stop offset=".55" stop-color="{sc}"/><stop offset="1" stop-color="{m}"/></linearGradient></defs>' + R(x, y, w, h + ry, f"url(#{g2})")
    s += bs_pattern(cfg.get("pattern", "clouds"), (x, y + 30, x + w, base + ry), cfg)
    if cfg.get("cat"): s += cat(cx + w * .28, base - 12, w * .0045, "#FFFFFF", ink)
    s += '</g>' + bs_label(cfg, cx, y + 30 + (h - 30) * .46, w * cfg.get("lw", .6))
    s += f'<path d="{body}" fill="url(#{gid})" stroke="#00000028"/>'
    if fin == "gloss": s += R(x + w * .1, y + 44, 10, h - 60, "#FFFFFFCC", "none", 5) + R(x + w * .1 + 16, y + 60, 4, h - 100, "#FFFFFF99", "none", 2)
    lc = {"plain": m, "scallop": sc, "cloud": "#FFFFFF"}[lidk]
    s += f'<path d="M{x - 4} {y + 8} L{x - 4} {y + 32} A{w / 2 + 4} {ry} 0 0 0 {x + w + 4} {y + 32} L{x + w + 4} {y + 8} Z" fill="{lc}" stroke="#00000028"/>'
    if lidk == "scallop": s += "".join(C(x - 4 + i * (w + 8) / 12, y + 32 + ry * math.sin(math.pi * (i / 12)) * .95, (w + 8) / 24, lc) for i in range(13))
    s += E(cx, y + 8, w / 2 + 4, ry, lc, "#00000028")
    if lidk == "cloud": s += G(cloud(0, 0, w * .42, "#FFFFFF", m, 3), cx, y + 2) + C(cx, y - 4, 4, sc)
    elif lidk == "plain": s += E(cx, y + 8, w / 2 - 14, ry - 8, "none", "#FFFFFF55", 2)
    return s
def bs_jar(cfg, cx, base, w=180, h=230):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; x = cx - w / 2; y = base - h
    s = shadow(cx, base + 6, w * .6) + R(x, y + 40, w, h - 40, "#FFFFFFCC", "#C8C0B8", 34, 2) + R(x + 10, y + 120, w - 20, h - 130, "#E8C9A2", "none", 26)
    s += "".join(C(x + 26 + (i * 37) % (w - 50), y + 140 + (i * 23) % (h - 160), 6, "#D9B183") for i in range(14))
    s += R(x + 14, y + 20, w - 28, 30, m, "#00000028", 8) + G(cloud(0, 0, w * .62, "#FFFFFF", m, 3), cx, y + 6)
    s += bs_label(dict(cfg, label=cfg.get("label", "badge")), cx, y + 140, w * .78)
    return s + R(x + 14, y + 56, 12, h - 80, "#FFFFFF88", "none", 6)
def bs_pillow(cfg, cx, base, w=220, h=280):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; x = cx - w / 2; y = base - h; cid = uid("bsp")
    path = f"M{x} {y + 20} Q{cx} {y + 34} {x + w} {y + 20} L{x + w - 10} {base - 20} Q{cx} {base - 6} {x + 10} {base - 20} Z"
    s = shadow(cx, base, w * .55) + f'<defs><clipPath id="{cid}"><path d="{path}"/></clipPath></defs><g clip-path="url(#{cid})">' + R(x, y, w, h, lt)
    s += bs_pattern(cfg.get("pattern", "clouds"), (x, y, x + w, base), cfg) + '</g>' + f'<path d="{path}" fill="none" stroke="#00000028" stroke-width="2"/>'
    s += "".join(f'<line x1="{x + 6 + i * 8}" y1="{y + 14}" x2="{x + 10 + i * 8}" y2="{y + 30}" stroke="{m}" stroke-width="2"/>' for i in range(int(w / 8) - 1))
    return s + bs_label(cfg, cx, y + h * .5, w * .8)
def bs_bag(cfg, cx, base, w=200, h=290):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; x = cx - w / 2; y = base - h
    s = shadow(cx, base + 4, w * .6) + f'<path d="M{x + 10} {y + 50} L{x + w - 10} {y + 50} L{x + w} {base} L{x} {base} Z" fill="{lt}" stroke="#00000028"/>'
    s += f'<path d="M{x + 30} {y} L{x + w - 30} {y} L{x + w - 10} {y + 54} L{x + 10} {y + 54} Z" fill="{KRAFT}" stroke="#00000028"/>'
    s += f'<path d="M{x + 40} {y + 50} q60 18 120 0" fill="none" stroke="{m}" stroke-width="8"/>' + f'<path d="M{cx} {y + 58} q-30 -10 -40 10 q20 10 40 -10 q30 -10 40 10 q-20 10 -40 -10" fill="{m}"/>'
    s += f'<path d="M{cx - 4} {y + 60} l-16 40 M{cx + 4} {y + 60} l16 40" stroke="{m}" stroke-width="5"/>'
    s += G(bs_pattern(cfg.get("pattern", "dots"), (0, 0, w - 20, h - 120), cfg), x + 10, y + 110)
    return s + bs_label(cfg, cx, y + h * .58, w * .82)
def bs_hero(cfg, obj="tin"):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]
    s = R(0, 0, 480, 600, "#FFFBF8") + R(0, 450, 480, 150, "#F7EEE9")
    if obj == "tin": s += bs_tin(cfg, 240, 500, 310, 300)
    elif obj == "jar": s += bs_jar(cfg, 240, 480, 210, 300)
    elif obj == "pillow": s += bs_pillow(cfg, 240, 490, 250, 330)
    elif obj == "bag": s += bs_bag(cfg, 240, 500, 230, 340)
    return s
def lounge_bg(cfg):
    """Pink lounge: pink wall, cloud ceiling band, butter awning stripe (as described in public reviews)."""
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]
    s = R(0, 0, 480, 600, lt) + R(0, 0, 480, 70, "#FFFFFF") + "".join(cloud(30 + i * 70, 66, 90, "#FFFFFF", "#EADFE3", 2) for i in range(8))
    return s + R(0, 470, 480, 130, "#EBDCD3")
def bs_scene(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = lounge_bg(cfg)
    if kind == "counter":
        s += R(50, 360, 380, 110, m, "#00000020", 8) + R(40, 350, 400, 16, "#FFFFFF", "#00000020", 6) + T(240, 425, "WELLNEST TEA CORNER", 18, "#FFFFFF", MONO, 600, extra='letter-spacing="2"')
        s += R(140, 280, 200, 70, "#FFFFFF", m, 10, 2) + "".join(G(bs_tin(cfg, 0, 0, 52, 46), 170 + i * 46, 340, 1) for i in range(4))
        return s + cloud(240, 250, 120, "#FFFFFF", sc, 3) + T(240, 258, "take one", 18, ink, MALI, 600)
    if kind == "rail":
        s += f'<line x1="70" y1="150" x2="410" y2="150" stroke="#9AA0A8" stroke-width="6" stroke-linecap="round"/>'
        for i in range(4):
            px = 110 + i * 86; s += f'<line x1="{px}" y1="150" x2="{px}" y2="176" stroke="#9AA0A8" stroke-width="3"/>' + G(bs_pillow(dict(cfg, label="badge"), 0, 0, 70, 110), px, 290, 1)
        return s + R(150, 340, 180, 50, "#FFFFFF", m, 25, 2) + T(240, 372, "pick a pouch", 18, ink, MALI, 600)
    if kind == "bench":
        s += R(30, 380, 420, 70, m, "#00000020", 20) + R(40, 330, 400, 60, m, "#00000020", 20)
        s += R(150, 350, 180, 40, "#FFFFFF", "#00000020", 8) + E(210, 340, 30, 22, "#FFFFFF", m, 3) + f'<path d="M238 334 q16 -4 18 10" fill="none" stroke="{m}" stroke-width="5"/>' + R(198, 312, 24, 8, sc)
        s += f'<path d="M266 348 l4 -26 h28 l4 26 z" fill="#E9C77A" stroke="#00000030"/>' + cat(380, 330, .9, "#FFFFFF", ink)
        return s + T(240, 520, "Tea tray on the lounge bench", 15, MUTEW, MONO)
    if kind == "jars":
        s += R(60, 360, 360, 18, "#FFFFFF", "#00000020", 6) + R(70, 378, 340, 92, sc + "88")
        for i in range(3): s += G(bs_jar(dict(cfg, label="badge"), 0, 0, 80, 110), 140 + i * 100, 356, 1)
        return s + R(130, 400, 220, 44, "#FFFFFF", m, 22, 2) + T(240, 429, "scoop your own", 18, ink, MALI, 600)
def bs_menu(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = R(0, 0, 480, 600, "#FFFBF8")
    if kind == "coaster":
        s += shadow(240, 470, 160) + C(240, 290, 170, "#FFFFFF", m, 5) + C(240, 290, 150, lt) + G(bs_pattern("dots", (0, 0, 300, 300), cfg), 90, 140)
        s += C(240, 290, 112, "#FFFFFF") + wn_mark(240, 220, 24) + T(240, 278, "tea menu", 30, ink, MALI, 600)
        for i, nm in enumerate(("Unwind · hot", "Unwind · iced", "Tin to take home")): s += T(240, 314 + i * 26, nm, 15, ink, MONO)
        return s + T(240, 520, "Round coaster menu, no prices: mockup", 14, MUTEW, MONO)
    s += shadow(240, 470, 150) + f'<path d="M80 140 L240 120 L400 140 L400 450 L240 470 L80 450 Z" fill="#FFFFFF" stroke="#00000025"/><line x1="240" y1="120" x2="240" y2="470" stroke="#00000020"/>'
    s += f'<path d="M80 140 L240 120 L240 300 L80 300 Z" fill="{m}"/>' + cloud(160, 210, 110, "#FFFFFF") + T(160, 222, "tea", 30, m, MALI, 600) + wn_mark(160, 380, 30)
    for i, nm in enumerate(("Unwind", "hot or iced", "Tins + pouches", "ask at the counter")): s += T(320, 200 + i * 40, nm, 18 if i % 2 == 0 else 13, ink, MALI if i % 2 == 0 else MONO, 600 if i % 2 == 0 else 400)
    return s + T(240, 520, "Folded postcard menu, no prices: mockup", 14, MUTEW, MONO)
def bs_merch(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = R(0, 0, 480, 600, "#FFFBF8")
    if kind == "mug":
        s += shadow(220, 450, 100) + R(130, 220, 180, 230, m, "#00000025", 18) + f'<path d="M310 270 q70 0 70 60 q0 60 -70 60" fill="none" stroke="{m}" stroke-width="20"/>'
        s += E(220, 222, 90, 12, "#F7E4E8") + cloud(220, 320, 130, "#FFFFFF") + T(220, 330, "unwind", 26, ink, MALI, 600) + G(sparkle(0, 0, 10, sc), 160, 400) + G(sparkle(0, 0, 8, sc), 280, 260)
        return s + T(240, 520, "Pink enamel mug", 15, MUTEW, MONO)
    if kind == "tote":
        s += f'<path d="M190 200 Q190 120 240 120 Q290 120 290 200" fill="none" stroke="{m}" stroke-width="10"/>' + R(130, 190, 220, 290, lt, "#00000025", 6)
        s += G(bs_pattern("clouds", (0, 0, 220, 290), cfg), 130, 190) + cat(240, 380, 1.1, "#FFFFFF", ink) + T(240, 270, "slow sips club", 24, ink, MALI, 600)
        return s + T(240, 528, "Canvas tote", 15, MUTEW, MONO)
    if kind == "stickers":
        s += R(110, 110, 260, 340, "#FFFFFF", "#00000025", 10) + G(cloud(0, 0, 120, lt, m, 3), 190, 180) + T(190, 188, "sip", 22, ink, MALI, 600)
        s += C(300, 180, 40, sc, "#FFFFFF", 4) + wn_mark(300, 180, 28) + G(cat(0, 0, .9, lt, ink), 200, 300) + G(star(0, 0, 30, sc), 310, 300)
        s += R(150, 370, 180, 40, m, "#FFFFFF", 20, 4) + T(240, 397, "tea time", 20, "#FFFFFF", MALI, 600)
        return s + T(240, 500, "Sticker sheet", 15, MUTEW, MONO)
    if kind == "pin":
        s += C(170, 270, 80, m, "#00000030", 3) + C(170, 270, 70, lt) + cat(178, 282, .9, "#FFFFFF", ink)
        s += G(cloud(0, 0, 160, "#FFFFFF", m, 6), 330, 280) + T(330, 290, "steep", 24, ink, MALI, 600)
        return s + T(240, 460, "Enamel pins", 15, MUTEW, MONO)
    if kind == "shoebox":
        s += shadow(240, 470, 150) + R(100, 290, 280, 180, lt, "#00000025", 6) + R(90, 260, 300, 44, m, "#00000025", 6) + G(bs_pattern("clouds", (0, 0, 280, 160), cfg), 100, 304)
        s += R(160, 330, 160, 80, "#FFFFFF", m, 12, 3) + T(240, 362, "lounge set", 22, ink, MALI, 600) + T(240, 390, "tin · mug · stickers", 13, MUTEW, MONO)
        return s + T(240, 520, "Lift-off gift box", 15, MUTEW, MONO)
    if kind == "trio":
        s += R(70, 420, 340, 18, "#EBDCD3")
        for i, pal in enumerate(("pinkbutter", "coralpowder", "lilacpink")): s += G(bs_tin(dict(cfg, pal=pal), 0, 0, 100, 90), 140 + i * 100, 420, 1)
        return s + T(240, 490, "Mini tin trio", 15, MUTEW, MONO)
def bs_badge(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = R(0, 0, 480, 600, "#FFFBF8")
    if kind == "bubble":
        s += f'<path d="M70 170 Q70 120 120 120 L360 120 Q410 120 410 170 L410 290 Q410 340 360 340 L190 340 L140 400 L150 340 L120 340 Q70 340 70 290 Z" fill="#FFFFFF" stroke="{m}" stroke-width="4"/>'
        s += wn_mark(150, 230, 44) + T(300, 222, "with", 20, ink, MALI, 600) + partner("bs", 300, 262, 24, m)
        return s + T(240, 480, "Speech-bubble co-brand sticker", 15, MUTEW, MONO)
    s += bs_label(dict(cfg, label="ticket", name="Unwind"), 240, 260, 400)
    return s + T(240, 480, "Ticket-stub co-brand label", 15, MUTEW, MONO)
def bs_back(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = R(0, 0, 480, 600, "#FFFBF8") + R(70, 60, 340, 450, "#FFFFFF", m, 18, 3) + T(240, 100, "back of tin", 22, m, MALI, 600)
    if kind == "comic":
        steps = ("scoop", "steep", "sip", "stay a while")
        for i, st in enumerate(steps):
            px, py = 90 + (i % 2) * 155, 120 + (i // 2) * 170
            s += R(px, py, 145, 155, lt, ink, 10, 2) + T(px + 72, py + 140, st, 17, ink, MALI, 600)
            if i == 0: s += E(px + 72, py + 80, 40, 18, "#E8C9A2") + f'<path d="M{px + 40} {py + 40} l30 30" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
            if i == 1: s += E(px + 72, py + 70, 34, 26, "#FFFFFF", ink, 2) + f'<path d="M{px + 60} {py + 34} q6 -10 0 -20 M{px + 80} {py + 34} q6 -10 0 -20" fill="none" stroke="{ink}" stroke-width="2"/>'
            if i == 2: s += f'<path d="M{px + 50} {py + 50} h44 l-6 50 h-32 z" fill="{sc}" stroke="{ink}" stroke-width="2"/>'
            if i == 3: s += cat(px + 72, py + 80, .8, "#FFFFFF", ink)
    else:
        rows = ("Ingredients: per final recipe", "Brew: amount TBC", "Steep: time TBC", "Made by The WellNest", "with The Buds Station", "Packed in Chiang Mai")
        for i, r_ in enumerate(rows):
            yy = 160 + i * 52; s += R(100, yy - 18, 22, 22, "#FFFFFF", m, 6, 2) + T(136, yy, r_, 15, ink, MONO, 400, "start")
    return s + wn_word(240, 490, 22)
def bs_iced(cfg, kind):
    m, sc, ink, lt = BSP[cfg.get("pal", "pinkbutter")]; s = R(0, 0, 480, 600, "#FFFBF8") + R(0, 450, 480, 150, "#F7EEE9") + shadow(240, 478, 80)
    tea = "#E7C27A"
    if kind == "cup":
        s += f'<path d="M170 200 L310 200 L292 474 L188 474 Z" fill="#FFFFFFAA" stroke="#C8C0B8" stroke-width="2"/><path d="M176 260 L304 260 L292 474 L188 474 Z" fill="{tea}" opacity=".85"/>'
        s += f'<path d="M160 200 Q240 120 320 200 Z" fill="#FFFFFFCC" stroke="#C8C0B8" stroke-width="2"/>' + R(156, 194, 168, 12, "#FFFFFF", "#C8C0B8", 6) + R(250, 90, 10, 120, m, "none", 4)
        s += cloud(240, 350, 130, "#FFFFFF", m, 3) + wn_mark(205, 352, 20) + T(268, 360, "iced", 22, ink, MALI, 600)
        return s + T(240, 528, "Iced cup, cloud sticker", 15, MUTEW, MONO)
    s += f'<path d="M205 150 L275 150 L275 200 Q310 220 310 260 L310 460 Q310 476 294 476 L186 476 Q170 476 170 460 L170 260 Q170 220 205 200 Z" fill="{tea}" opacity=".85" stroke="#C8C0B8" stroke-width="2"/>'
    s += R(200, 118, 80, 34, "#FFFFFF", "#C8C0B8", 8) + f'<path d="M206 150 q-20 -30 10 -40 M274 150 q20 -30 -10 -40" fill="none" stroke="#9AA0A8" stroke-width="4"/>' + C(240, 118, 10, m)
    s += bs_label(dict(cfg, label="badge"), 240, 360, 150)
    return s + T(240, 528, "Swing-top glass bottle", 15, MUTEW, MONO)
