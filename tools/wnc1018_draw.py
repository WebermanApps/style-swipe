"""WellNest collab pouch + lockup mockups, Oct 18 2026 (Branding; Max asked WellNest 22:44 ICT).
Clean drawn SVG only: the WellNest kraft pouch, cream label and watercolour wash are always the base; WellNest leads every lockup.
Partner names are SET IN TYPE in the partner's colours (no partner logo artwork is embedded or redrawn).
Each card is drawn on a 480x600 virtual canvas, scaled 0.5 into the kit's 240x300 screen (so crisp() leaves small text alone)."""
import hashlib, math, random
from draft_svg import screen, esc
KRAFT, KRAFT_D, KRAFT_L = "#C79E6E", "#A97F52", "#D9B98F"
LABEL = "#F5EEDF"; INKW = "#3A3531"; LOGO = "#A9875F"; MUTEW = "#6B625A"
MONO = 'font-family="IBM Plex Mono, Courier New, monospace"'
SCRIPT = 'font-family="Caveat, cursive" font-weight="700"'
HINDF = 'font-family="Hind, sans-serif"'
LX0, LX1, LY0, LY1 = 124, 356, 172, 546   # label box on the pouch
def _id(cfg, p): return p + hashlib.md5(repr(sorted(cfg.items())).encode()).hexdigest()[:8]
def T(x, y, s, size, col=INKW, fam=HINDF, w=400, anchor="middle", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{col}" text-anchor="{anchor}" {fam} font-weight="{w}" {extra}>{esc(s)}</text>'
# ---------- partner names, set in type in their colours ----------
PARTNERS = {
    "powerhaus": dict(name=("PowerHaus", " Pilates"), fam='font-family="Nunito, sans-serif"', w=(800, 600), col="#003CA7", k=.60),
    "buds": dict(name=("The Buds Station", ""), fam='font-family="DM Sans, sans-serif"', w=(700, 700), col="#CA5970", k=.58),
}
def partner(key, x, y, size, col=None, anchor="middle"):
    p = PARTNERS[key]; c = col or p["col"]; a, b = p["name"]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{c}" text-anchor="{anchor}" {p["fam"]} data-g="partner-name">'
            f'<tspan font-weight="{p["w"][0]}">{esc(a)}</tspan>' + (f'<tspan font-weight="{p["w"][1]}">{esc(b)}</tspan>' if b else "") + '</text>')
def pwidth(key, size): p = PARTNERS[key]; return len("".join(p["name"])) * size * p["k"]
# ---------- WellNest mark (circle + script, as on the drafted pouches) ----------
def wn_logo(cx, cy, r=44, col=LOGO):
    return (f'<g data-g="wellnest-mark"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="1.6"/>'
            + T(cx, cy - r * .12, "The", r * .46, INKW, SCRIPT) + T(cx, cy + r * .42, "WellNest", r * .58, INKW, SCRIPT) + '</g>')
def wn_line(x, y, size, anchor="middle"): return T(x, y, "The WellNest", size, INKW, SCRIPT, 700, anchor)
# ---------- watercolour wash ----------
def wash(cfg, top):
    fid = _id(cfg, "wf"); rnd = random.Random(cfg.get("seed", 3)); out = ""
    cols = cfg.get("wash") or ["#D2774E"]
    out += (f'<defs><filter id="{fid}" x="-10%" y="-20%" width="120%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.03 0.055" numOctaves="3" seed="{cfg.get("seed",3)}"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="16"/><feGaussianBlur stdDeviation=".7"/></filter>')
    for i, c in enumerate(cols):
        out += (f'<linearGradient id="{fid}g{i}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c}" stop-opacity=".88"/>'
                f'<stop offset=".7" stop-color="{c}" stop-opacity=".45"/><stop offset="1" stop-color="{c}" stop-opacity=".12"/></linearGradient>')
    out += '</defs>'
    layers = [(0, 0), (1, 26), (0, 58)] if len(cols) == 1 else [(0, 0), (1, 34), (0, 70), (1, 92)]
    for li, (ci, dy) in enumerate(layers):
        y0 = top + dy; pts = [f"M{LX0-12} {LY1+12}", f"L{LX0-12} {y0+rnd.uniform(-8,8):.1f}"]
        x = LX0 - 12
        while x < LX1 + 12:
            x += rnd.uniform(18, 34); pts.append(f"Q{x-10:.1f} {y0+rnd.uniform(-22,14):.1f} {x:.1f} {y0+rnd.uniform(-12,12):.1f}")
        pts.append(f"L{LX1+12} {LY1+12} Z")
        out += f'<path d="{" ".join(pts)}" fill="url(#{fid}g{ci})" opacity="{.75 - li*.1:.2f}" filter="url(#{fid})"/>'
    return out
# ---------- motifs (Buds Station deck: abstract only, no sacred figures) ----------
def spire7(cx, base, h, col, sw=3.2):
    """Abstract seven-line spire motif: seven tapered vertical lines, tallest in the centre. Not a building, not a mascot."""
    hs = [.42, .58, .74, 1.0, .74, .58, .42]; gap = h * .17; s = f'<g data-g="spire7">'
    for i, k in enumerate(hs):
        x = cx + (i - 3) * gap; top = base - h * k
        s += f'<path d="M{x-sw/2:.1f} {base} L{x:.1f} {top:.1f} L{x+sw/2:.1f} {base} Z" fill="{col}"/>'
    return s + f'<line x1="{cx-3.4*gap:.1f}" y1="{base+2}" x2="{cx+3.4*gap:.1f}" y2="{base+2}" stroke="{col}" stroke-width="1.4"/></g>'
def bodhi(cx, cy, h, col, sw=1.4):
    """One smooth heart-shaped bodhi leaf with its long drip tip (single leaf, smooth edge)."""
    w = h * .62; t = cy - h * .5; b = cy + h * .5
    d = (f"M{cx} {t+h*.18} C{cx-w*.15} {t} {cx-w*.62} {t+h*.02} {cx-w*.5} {t+h*.32} C{cx-w*.42} {t+h*.55} {cx-w*.12} {t+h*.72} {cx} {b}"
         f" C{cx+w*.12} {t+h*.72} {cx+w*.42} {t+h*.55} {cx+w*.5} {t+h*.32} C{cx+w*.62} {t+h*.02} {cx+w*.15} {t} {cx} {t+h*.18} Z")
    v = "".join(f'<path d="M{cx} {t+h*(.3+i*.12):.1f} Q{cx+sg*w*.2:.1f} {t+h*(.26+i*.12):.1f} {cx+sg*w*.36:.1f} {t+h*(.2+i*.12):.1f}" fill="none" stroke="{col}" stroke-width="{sw*.7}"/>'
                for i in range(3) for sg in (-1, 1))
    return f'<g data-g="bodhi"><path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"/><line x1="{cx}" y1="{t+h*.2:.1f}" x2="{cx}" y2="{b-4:.1f}" stroke="{col}" stroke-width="{sw*.8}"/>{v}</g>'
def bricks(x0, y0, x1, y1, col, op=.22):
    s = f'<g data-g="brick-texture" opacity="{op}">'; bh = 9; r = 0; y = y0
    while y < y1:
        x = x0 - (14 if r % 2 else 0)
        while x < x1:
            s += f'<rect x="{max(x,x0):.1f}" y="{y:.1f}" width="{min(26, x1-max(x,x0)):.1f}" height="{bh-2}" rx="1" fill="{col}"/>'; x += 28
        y += bh; r += 1
    return s + '</g>'
def speckle(cfg, x0, y0, x1, y1, col="#8C7972", n=160):
    rnd = random.Random(7); return '<g data-g="stucco-speckle" opacity=".35">' + "".join(
        f'<circle cx="{rnd.uniform(x0,x1):.1f}" cy="{rnd.uniform(y0,y1):.1f}" r="{rnd.uniform(.5,1.6):.1f}" fill="{col}"/>' for _ in range(n)) + '</g>'
# ---------- ingredient icons (simple drawn shapes, 0..28 box) ----------
ING = {
    "ginger": ("#D8B47A", "knob"), "lemongrass": ("#8FA84A", "stalk"), "roselle": ("#B3263A", "calyx"),
    "turmeric": ("#E08A1E", "knob"), "galangal": ("#D9A08C", "knob"), "butterfly pea": ("#3B4FB8", "flower"), "mint": ("#4E9A5C", "ovals"),
    "chrysanthemum": ("#E3B53B", "flower"), "pandan": ("#3F8A4A", "strap"), "holy basil": ("#6A8F4C", "ovals"), "lotus": ("#E39AAE", "lotus"),
    "dried longan": ("#9A6A3A", "berry"),
}
def icon(name, x, y):
    c, k = ING[name]
    if k == "knob": return f'<path d="M{x+3} {y+18} q2 -10 9 -9 q2 -7 8 -4 q6 2 4 9 q4 6 -3 9 q-8 4 -18 -5z" fill="{c}" stroke="#00000022"/>'
    if k == "stalk": return f'<path d="M{x+12} {y+27} L{x+14} {y+2} M{x+14} {y+27} L{x+20} {y+5}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
    if k == "strap": return f'<path d="M{x+8} {y+27} Q{x+6} {y+12} {x+12} {y+1} M{x+15} {y+27} Q{x+17} {y+12} {x+22} {y+3}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
    if k == "calyx": return f'<circle cx="{x+14}" cy="{y+15}" r="10" fill="{c}"/><path d="M{x+14} {y+5} L{x+14} {y+25} M{x+5} {y+15} L{x+23} {y+15}" stroke="#7A1424" stroke-width="1.2"/>'
    if k == "flower":
        return "".join(f'<ellipse cx="{x+14+7*math.cos(a):.1f}" cy="{y+14+7*math.sin(a):.1f}" rx="5" ry="3" transform="rotate({math.degrees(a):.0f} {x+14+7*math.cos(a):.1f} {y+14+7*math.sin(a):.1f})" fill="{c}"/>'
                       for a in [i * math.pi / 4 for i in range(8)]) + f'<circle cx="{x+14}" cy="{y+14}" r="3.4" fill="#F4D27A"/>'
    if k == "ovals": return f'<ellipse cx="{x+9}" cy="{y+12}" rx="6" ry="9" transform="rotate(-25 {x+9} {y+12})" fill="{c}"/><ellipse cx="{x+19}" cy="{y+14}" rx="6" ry="9" transform="rotate(25 {x+19} {y+14})" fill="{c}"/>'
    if k == "lotus": return f'<path d="M{x+14} {y+4} Q{x+22} {y+14} {x+14} {y+24} Q{x+6} {y+14} {x+14} {y+4}Z M{x+4} {y+12} Q{x+12} {y+16} {x+13} {y+24} Q{x+3} {y+22} {x+4} {y+12}Z M{x+24} {y+12} Q{x+16} {y+16} {x+15} {y+24} Q{x+25} {y+22} {x+24} {y+12}Z" fill="{c}"/>'
    return f'<circle cx="{x+14}" cy="{y+15}" r="9" fill="{c}"/><circle cx="{x+11}" cy="{y+12}" r="2.4" fill="#FFFFFF55"/>'
# ---------- the pouch ----------
def fit(s, maxw, k=.62, cap=46): return min(cap, maxw / (max(len(s), 1) * k))
def pouch(cfg):
    """cfg keys: pk partner key; name; wash [colours]; wtop; accent colour|None; pcol partner colour; tag tagline; lock (draft|stack|line|front-only);
    lk partner size ratio vs WellNest; conn 'for'|'with'|'x'; title_font mono|partner; window bool; motif spire7|bodhi|None; mpos corner|big;
    texture brick|stucco|None; foil bool"""
    pk = cfg["pk"]; s = ""; acc = cfg.get("accent"); cid = _id(cfg, "lc")
    s += f'<ellipse cx="240" cy="586" rx="150" ry="10" fill="#00000014"/>'
    body = "M112 52 Q112 40 124 40 L356 40 Q368 40 368 52 L374 560 Q374 578 356 578 L124 578 Q106 578 106 560 Z"
    s += f'<defs><linearGradient id="{cid}k" x1="0" x2="1"><stop offset="0" stop-color="{KRAFT_D}"/><stop offset=".12" stop-color="{KRAFT}"/><stop offset=".55" stop-color="{KRAFT_L}"/><stop offset=".9" stop-color="{KRAFT}"/><stop offset="1" stop-color="{KRAFT_D}"/></linearGradient>'
    s += f'<clipPath id="{cid}"><rect x="{LX0}" y="{LY0}" width="{LX1-LX0}" height="{LY1-LY0}" rx="2"/></clipPath></defs>'
    s += f'<path d="{body}" fill="url(#{cid}k)" stroke="#9C7448" stroke-width="1"/>'
    s += f'<path d="M112 96 L368 96" stroke="#00000018" stroke-width="10"/><path d="M110 112 L370 112" stroke="#9C7448" stroke-width="1.4" stroke-dasharray="2 3"/>'
    s += f'<path d="M106 72 l7 4 l-7 4 Z M374 72 l-7 4 l7 4 Z" fill="#FFFFFF"/>'
    if acc: s += f'<path d="M110 106 L370 106" stroke="{acc}" stroke-width="7"/>'
    s += f'<rect x="{LX0}" y="{LY0}" width="{LX1-LX0}" height="{LY1-LY0}" rx="2" fill="{LABEL}"/>'
    s += f'<g clip-path="url(#{cid})">'
    if cfg.get("texture") == "stucco": s += speckle(cfg, LX0, LY0, LX1, LY1)
    s += wash(cfg, cfg.get("wtop", 410))
    if cfg.get("texture") == "brick": s += bricks(LX0, LY1 - 46, LX1, LY1, "#594A44", .28)
    if cfg.get("motif") and cfg.get("mpos") == "big":
        mc = cfg.get("mcol", "#594A44")
        s += f'<g opacity=".16">' + (spire7(240, 520, 300, mc, 9) if cfg["motif"] == "spire7" else bodhi(240, 380, 300, mc, 4)) + '</g>'
    s += '</g>'
    if cfg.get("foil"): s += f'<rect x="{LX0+6}" y="{LY0+6}" width="{LX1-LX0-12}" height="{LY1-LY0-12}" fill="none" stroke="#C9A43A" stroke-width="2"/>'
    if acc and cfg.get("accent_rule", True): s += f'<rect x="{LX0}" y="{LY0}" width="{LX1-LX0}" height="12" fill="{acc}"/>'
    if cfg.get("window"):
        s += f'<rect x="200" y="452" width="80" height="62" rx="31" fill="#FFFFFFB0" stroke="#9C7448"/>'
        rnd = random.Random(5); cs = cfg.get("wcols", ["#B3263A", "#D8B47A", "#8FA84A"])
        s += "".join(f'<circle cx="{rnd.uniform(212,268):.1f}" cy="{rnd.uniform(466,502):.1f}" r="{rnd.uniform(3,6):.1f}" fill="{cs[i%len(cs)]}"/>' for i in range(22))
    s += lockup(cfg)
    return s
def lockup(cfg):
    pk = cfg["pk"]; lock = cfg.get("lock", "draft"); lk = cfg.get("lk", .5); conn = cfg.get("conn", "for"); s = ""
    pcol = cfg.get("pcol"); name = cfg["name"]; tag = cfg.get("tag")
    ty = 350
    if lock == "draft":
        s += wn_logo(300, 232, 44)
        if cfg.get("motif") and cfg.get("mpos") != "big": s += _motif_small(cfg, 172, 236)
    elif lock in ("stack", "front-only"):
        s += wn_logo(240, 238, 50)
        if lock == "stack":
            psz = 29 * lk
            if conn == "x": s += T(240, 312, "×", 18, MUTEW)
            else: s += T(240, 312, conn, 15, MUTEW, MONO)
            s += partner(pk, 240, 316 + psz, min(psz, 222 / (len("".join(PARTNERS[pk]["name"])) * PARTNERS[pk]["k"])), pcol)
            ty = 316 + psz + 52
        if cfg.get("motif") and cfg.get("mpos") != "big": s += _motif_small(cfg, 160, 236)
    elif lock == "line":
        wsz = 34; psz = wsz * lk; ww = len("The WellNest") * wsz * .43; pw = pwidth(pk, psz); cw = 30 if conn == "x" else len(conn) * 9 + 20
        tot = ww + cw + pw; x0 = 240 - tot / 2
        if tot > 224:
            k = 224 / tot; wsz *= k; psz *= k; ww *= k; pw *= k; cw *= k; x0 = 128
        s += wn_line(x0, 238, wsz, "start")
        s += T(x0 + ww + cw / 2, 236, "×" if conn == "x" else conn, 16 if conn == "x" else 13, MUTEW, HINDF if conn == "x" else MONO)
        s += partner(pk, x0 + ww + cw, 236, psz, pcol, "start")
        s += f'<line x1="150" y1="262" x2="330" y2="262" stroke="{LOGO}" stroke-width="1"/>'
        if cfg.get("motif") and cfg.get("mpos") != "big": s += _motif_small(cfg, 240, 300)
    tf = cfg.get("title_font", "mono")
    if tf == "mono": s += T(240, ty, name.upper(), fit(name, 204, .66), INKW, MONO, 600, extra='letter-spacing="3"')
    else: s += T(240, ty, name, fit(name, 210, .58, 44), cfg.get("tcol") or PARTNERS[pk]["col"], PARTNERS[pk]["fam"], 800)
    sy = ty + 30
    if lock == "draft":
        if cfg.get("partner_mono"): s += T(240, sy, "for " + "".join(PARTNERS[pk]["name"]), 15, INKW, MONO)
        else:
            cw = {"for": 40, "with": 50, "x": 22}[conn]; pw = pwidth(pk, 17); x0 = 240 - (cw + pw) / 2
            s += T(x0 + cw - 8, sy, "×" if conn == "x" else conn, 15, INKW, MONO if conn != "x" else HINDF, 400, "end")
            s += partner(pk, x0 + cw, sy, 17, pcol or (INKW if cfg.get("plain_partner") else None), "start")
        sy += 26
    if tag:
        lines = [tag]
        if len(tag) > 26:
            ws = tag.split(); best = min(range(1, len(ws)), key=lambda i: abs(len(" ".join(ws[:i])) - len(" ".join(ws[i:]))))
            lines = [" ".join(ws[:best]), " ".join(ws[best:])]
        sz = min(15, min(fit(l, 214, .6, 15) for l in lines))
        for j, l in enumerate(lines): s += T(240, sy + 4 + j * (sz + 5), l, sz, "#4E4640", MONO, 400, extra='font-style="italic"')
    return s
def _motif_small(cfg, cx, cy):
    c = cfg.get("mcol", "#594A44")
    return spire7(cx, cy + 28, 64, c, 3.4) if cfg["motif"] == "spire7" else bodhi(cx, cy, 70, c, 1.8)
# ---------- cards ----------
def card_full(cfg, note=None):
    s = f'<rect width="480" height="600" fill="#FBF8F2"/>' + pouch(cfg)
    if note: s += _note(note)
    return screen(f'<g transform="scale(.5)">{s}</g>', "#FBF8F2")
def _note(note, y=548):
    return f'<rect x="0" y="{y}" width="480" height="{600-y}" fill="#FFFFFFE8"/>' + T(240, y + 32, note, fit(note, 440, .5, 19), INKW, HINDF, 600)
def card_zoom(cfg, note):
    k = 1.9; s = f'<rect width="480" height="600" fill="#FBF8F2"/><g transform="translate({240-240*k:.1f},{24-172*k:.1f}) scale({k})">' + pouch(cfg) + '</g>'
    s += _note(note, 520) + T(240, 586, "Label close-up, the pouch is the same kraft and cream", 13, MUTEW)
    return screen(f'<g transform="scale(.5)">{s}</g>', "#FBF8F2")
def card_blend(cfg, ings, brew, brew_note, add=None):
    s = f'<rect width="480" height="600" fill="#FBF8F2"/><g transform="translate(-34,58) scale(.8)">' + pouch(cfg) + '</g>'
    x0, y0 = 268, 70; h = 76 + len(ings) * 52
    s += f'<rect x="{x0}" y="{y0}" width="200" height="{h}" rx="10" fill="#FFFFFF" stroke="#E2D8C6"/>' + f'<circle cx="{x0+100}" cy="{y0+14}" r="5" fill="none" stroke="#B9A88E" stroke-width="2"/>'
    s += T(x0 + 18, y0 + 46, "THE BLEND", 15, INKW, HINDF, 600, "start", 'letter-spacing="2"')
    for i, nm in enumerate(ings):
        yy = y0 + 64 + i * 52; hi = nm == add
        if hi: s += f'<rect x="{x0+8}" y="{yy-4}" width="184" height="46" rx="8" fill="{ING[nm][0]}22" stroke="{ING[nm][0]}" stroke-dasharray="4 3"/>'
        s += f'<g transform="translate({x0+16},{yy+4}) scale(1.15)">' + icon(nm, 0, 0) + '</g>' + T(x0 + 56, yy + 24, nm.capitalize(), 17, INKW, HINDF, 600 if hi else 400, "start")
        if hi: s += T(x0 + 186, yy + 38, "ADDED", 9.5, ING[nm][0], HINDF, 700, "end", 'letter-spacing="1"')
    yb = y0 + h + 22
    s += f'<rect x="{x0}" y="{yb}" width="200" height="104" rx="10" fill="#FFFFFF" stroke="#E2D8C6"/>' + T(x0 + 18, yb + 30, "IN THE CUP", 13, MUTEW, HINDF, 600, "start", 'letter-spacing="2"')
    s += f'<ellipse cx="{x0+48}" cy="{yb+66}" rx="28" ry="12" fill="{brew}"/><path d="M{x0+20} {yb+66} q0 26 28 26 q28 0 28 -26" fill="none" stroke="#B9A88E" stroke-width="2"/>'
    for j, line in enumerate(brew_note): s += T(x0 + 86, yb + 62 + j * 18, line, 12.5, INKW, HINDF, 400, "start")
    return screen(f'<g transform="scale(.5)">{s}</g>', "#FBF8F2")
def card_back(cfg, back_lines):
    """Front without the partner name, plus a small drawn back-panel card naming the partner."""
    s = f'<rect width="480" height="600" fill="#FBF8F2"/><g transform="translate(-34,40) scale(.84)">' + pouch(cfg) + '</g>'
    x0, y0 = 272, 150
    s += f'<rect x="{x0}" y="{y0}" width="196" height="270" rx="12" fill="{KRAFT}" stroke="#9C7448"/><rect x="{x0+16}" y="{y0+40}" width="164" height="200" fill="{LABEL}"/>'
    s += T(x0 + 98, y0 + 26, "BACK OF POUCH", 12, "#FFFFFF", HINDF, 700, extra='letter-spacing="1.5"')
    for j, (ln_, kind) in enumerate(back_lines):
        yy = y0 + 72 + j * 30
        s += partner(cfg["pk"], x0 + 98, yy, 15) if kind == "partner" else T(x0 + 98, yy, ln_, 12.5, INKW, MONO)
    return screen(f'<g transform="scale(.5)">{s}</g>', "#FBF8F2")
