"""WellNest follow-up decks, Oct 19 2026 (Branding): drawn SVG helpers for PowerHaus Can And Base Tea, PowerHaus Can Look, Tea Theme Blends
and Farm Basket Build. 480x600 canvas scaled .5 into the kit's 240x300 screen; light backgrounds only; WellNest DNA (circle + script mark,
cream, IBM Plex Mono small print, kraft cue); every card tagged MOCKUP. No temple, sacred or cannabis imagery anywhere."""
import random
from draft_svg import screen, esc
from wnc1019_draw import R, C, E, T, G, arcs, wn_mark, wn_word, mock_tag, foot, MONO, SCRIPT, HIND, NUN, DMS, FRAU, OSW, CREAM, KRAFT, KRAFT_D, INKW, LOGO, MUTEW
ROYAL = "#003CA7"; _n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"
def card(body, note, bg="#FBFAF7", tag="MOCKUP"):
    return screen(f'<g transform="scale(.5)">{R(0, 0, 480, 600, bg)}{body}{mock_tag(label=tag)}{foot(note) if note else ""}</g>', bg)
def surface(): return R(0, 0, 480, 600, "#FBFAF7") + R(0, 470, 480, 130, "#F1ECE3")
NAMEF = {"mono": (MONO, 600, .66, 'letter-spacing="3"'), "round": (NUN, 800, .6, ""), "serif": (FRAU, 600, .6, 'letter-spacing="2"'),
         "wide": (OSW, 600, .62, 'letter-spacing="6"'), "script": (SCRIPT, 700, .45, "")}
def can(cx, base, cfg, w=150, h=230):
    """cfg: body, finish(matte|kraft|brushed|cream), label(spine|wrap|none|full), pattern(arcs|None), main, acc, lid(kraftband|slip|pull|plain|tall),
    bandw, name, nfont, lock(line|stack|small), conn, tag, tagpos(under|base|lid|back|none), badge(seal|ribbon|sticker|none)."""
    c = dict(dict(body="#FBFBF8", finish="matte", label="spine", pattern="arcs", main=ROYAL, acc="#C79E6E", lid="kraftband", bandw=10, name="Reform",
                  nfont="mono", lock="line", conn="with", tag="The cup after the class", tagpos="under", badge="none"), **cfg)
    x0 = cx - w / 2; x1 = cx + w / 2; top = base - h; ry = w * .12; gid = uid("cg"); cid = uid("cc"); s = E(cx, base + 6, w * .62, 9, "#00000018")
    body = {"matte": c["body"], "kraft": KRAFT, "brushed": "#D9DCDF", "cream": CREAM}[c["finish"]]
    s += (f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".10"/><stop offset=".3" stop-color="#fff" stop-opacity=".18"/>'
          f'<stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>'
          f'<clipPath id="{cid}"><path d="M{x0} {top} L{x1} {top} L{x1} {base} A{w/2} {ry} 0 0 1 {x0} {base} Z"/></clipPath></defs>')
    s += f'<path d="M{x0} {top} L{x1} {top} L{x1} {base} A{w/2} {ry} 0 0 1 {x0} {base} Z" fill="{body}" stroke="#00000022"/>'
    s += f'<g clip-path="url(#{cid})">'
    if c["finish"] == "brushed": s += "".join(f'<line x1="{x0}" y1="{top+i*6}" x2="{x1}" y2="{top+i*6}" stroke="#ffffff" stroke-opacity=".35"/>' for i in range(int(h / 6) + 2))
    if c["finish"] == "kraft": s += "".join(C(random.Random(i).uniform(x0, x1), random.Random(i + 99).uniform(top, base), 1.1, KRAFT_D) for i in range(70))
    lab = c["label"]
    if lab == "spine": s += R(x0 + w * .08, top, w * .16, h + ry, c["main"]) + T(x0 + w * .16, top + h * .55, "POWERHAUS", w * .075, "#FFFFFF", OSW, 600, extra=f'transform="rotate(-90 {x0 + w * .16 + 3} {top + h * .55})" letter-spacing="2"')
    if lab in ("wrap", "full"):
        if c["pattern"] == "arcs": s += arcs(x0 - 10, top + 6, x1 + 10, base, c["main"], 6, 4, .8)
        if lab == "wrap": s += R(x0, top + h * .3, w, h * .44, "#FFFFFF" if c["finish"] != "cream" else CREAM) + R(x0, top + h * .3, w, 3, c["main"]) + R(x0, top + h * .74 - 3, w, 3, c["main"])
    elif c["pattern"] == "arcs" and lab == "spine": s += arcs(x0 + w * .3, base - h * .28, x1 + 6, base + 4, c["main"], 3, 3, .55)
    s += f'</g><path d="M{x0} {top} L{x1} {top} L{x1} {base} A{w/2} {ry} 0 0 1 {x0} {base} Z" fill="url(#{gid})"/>'
    # lid
    lid = c["lid"]; lh = {"kraftband": 34, "slip": 26, "pull": 10, "plain": 18, "tall": 60}[lid]; lw = w + (6 if lid in ("kraftband", "slip", "tall") else 0)
    lcol = {"kraftband": KRAFT, "slip": c["main"], "pull": "#C9CDD1", "plain": c["body"] if c["finish"] == "matte" else "#EEE", "tall": KRAFT}[lid]
    s += R(cx - lw / 2, top - lh, lw, lh, lcol, "#00000022", 3) + E(cx, top - lh, lw / 2, ry * .8, lcol, "#00000022")
    if lid in ("kraftband", "tall"): s += R(cx - lw / 2, top - lh + (lh - c["bandw"]) / 2 + 4, lw, c["bandw"], c["main"])
    if lid == "pull": s += E(cx, top - lh, lw / 2 - 8, ry * .6, "none", "#9AA0A6", 2) + E(cx + lw * .2, top - lh, 10, 4, "#B9BEC3", "#9AA0A6")
    # lockup
    cx2 = cx + (w * .08 if lab == "spine" else 0); ly = top + h * .36; dark = INKW if c["finish"] != "brushed" else "#2A2A2A"
    if c["lock"] == "line":
        s += T(cx2, ly - 6, "The WellNest", w * .1, dark, SCRIPT, 700) + T(cx2, ly + 8, c["conn"], w * .055, MUTEW, MONO) + T(cx2, ly + 22, "PowerHaus Pilates", w * (.07 if lab == "spine" else .085), c["main"], NUN, 800)
    elif c["lock"] == "stack": s += wn_mark(cx2, ly - 2, w * .14) + T(cx2, ly + w * .2, c["conn"] + " PowerHaus Pilates", w * .065, c["main"], NUN, 800)
    else: s += T(cx2, ly, "The WellNest", w * .12, dark, SCRIPT, 700)
    f, fw, k, ex = NAMEF[c["nfont"]]; nm = c["name"]; nsz = min(w * .13, (w * (.55 if lab == "spine" else .74)) / (max(len(nm), 4) * k))
    s += T(cx2, top + h * .62, nm.upper() if c["nfont"] in ("mono", "wide") else nm, nsz, dark, f, fw, extra=ex)
    tg = c["tag"]; tp = c["tagpos"]
    if tg and tp == "under": s += T(cx2, top + h * .7, tg, min(w * .055, w * (.62 if lab == "spine" else .78) / (len(tg) * .6)), "#4E4640", MONO, 400, extra='font-style="italic"')
    if tg and tp == "base": s += R(x0, base - h * .14, w, h * .1, c["main"]) + T(cx, base - h * .07, tg, min(w * .058, w * .9 / (len(tg) * .55)), "#FFFFFF", MONO, 500)
    if tg and tp == "lid": s += T(cx, top - lh + 4 + (lh - c["bandw"]) / 2 + c["bandw"] * .75, tg, min(c["bandw"] * .8, lw * .9 / (len(tg) * .55)), "#FFFFFF", MONO, 600) if lid in ("kraftband", "tall") and c["bandw"] >= 12 else T(cx, top - lh - 2, tg, min(w * .055, lw * .9 / (len(tg) * .55)), INKW, MONO)
    b = c["badge"]
    if b == "seal": s += C(x1 - 18, top + 22, 18, "#FFFFFF", c["main"], 2) + T(x1 - 18, top + 20, "WN", 9, c["main"], OSW, 700) + T(x1 - 18, top + 30, "+ PH", 7, c["main"], OSW, 600)
    if b == "ribbon": s += f'<path d="M{x1-30} {top} h22 v34 l-11 -8 l-11 8 z" fill="{c["acc"]}"/>' + T(x1 - 19, top + 18, "CO", 8, "#FFFFFF", OSW, 700)
    if b == "sticker": s += C(cx, top - lh - ry * .8 + 2, 16, "#FFFFFF", c["main"], 2) + T(cx, top - lh - ry * .8 + 6, "WN+PH", 7, c["main"], OSW, 700)
    if b == "stamp": s += R(x0 + 10, base - 28, 46, 16, "none", c["main"], 3, 1.4) + T(x0 + 33, base - 17, "STUDIO", 7.5, c["main"], OSW, 700)
    return s
def can_card(note, cfg=None, back=False, **k):
    cfg = dict(cfg or {}, **k); s = surface() + can(240, 470, cfg, cfg.pop("w", 170) if "w" in cfg else 170, 270)
    return card(s, note)
def can_row(note, cfgs, labels=None, w=110, h=180):
    s = surface(); n = len(cfgs); gap = 440 / n
    for i, cf in enumerate(cfgs):
        cx = 20 + gap * (i + .5); s += can(cx, 470, cf, w, h)
        if labels: s += T(cx, 512, labels[i], 13, INKW, MONO, 600)
    return card(s, note)
# ---- tea blend card: base tea + 3-4 ingredients ----
ICOL = {"Assam Miang": "#7A5A2E", "Oolong": "#A0763A", "Mulberry leaf": "#5E8C3A", "Moringa": "#7FA046", "Guava leaf": "#8DB44E", "Gotu kola": "#4F8A4A",
        "Roselle": "#B3263E", "Butterfly pea": "#3A4FB0", "Chrysanthemum": "#E8B830", "Jasmine": "#E9E2C8", "Ginger": "#D9A441", "Lemongrass": "#B7C46A",
        "Kaffir lime": "#6E9A3A", "Thai basil": "#5E3F7A", "Holy basil": "#6B8E3A", "Lemon basil": "#9DBF5A", "Mint": "#4FA36E", "Longan": "#C9A27A",
        "Mango": "#F0A830", "Tamarind": "#7A4A2A", "Green tea": "#7E9A4A", "White tea": "#E6DCC4", "Orange peel": "#E8892B", "Osmanthus": "#E9A23B", "Rose": "#D9667E"}
def swatch(cx, cy, r, name):
    col = ICOL.get(name, "#999"); s = C(cx, cy, r, col + "33", col, 2) + C(cx, cy, r * .55, col)
    s += T(cx, cy + r + 18, name, 13, INKW, HIND, 600)
    if name in ("Osmanthus", "Orange peel"):  # not in Max's Oct 19 ingredients deck: always marked New
        s += R(cx - 20, cy - r - 22, 40, 16, "#FFFFFF", "#B7860B", 8, 1.4) + T(cx, cy - r - 10, "New", 11, "#8A6510", HIND, 700)
    return s
def blend_card(note, theme, base, ings, mood):
    s = R(0, 0, 480, 600, "#FBFAF7") + R(30, 64, 420, 470, "#FFFFFF", "#E6DFD1", 14) + R(30, 64, 420, 8, KRAFT, rx=4)
    s += T(240, 112, theme.upper(), 22, INKW, MONO, 600, extra='letter-spacing="4"') + T(240, 142, mood, 15, MUTEW, HIND, 400, extra='font-style="italic"')
    s += R(150, 162, 180, 34, CREAM, KRAFT, 17, 1.4) + T(240, 185, "Base: " + base, 15, INKW, HIND, 700)
    n = len(ings); gap = 380 / n
    for i, nm in enumerate(ings): s += swatch(50 + gap * (i + .5), 270, 36, nm)
    s += f'<path d="M80 352 Q240 330 400 352" stroke="{KRAFT}" stroke-width="2" fill="none" stroke-dasharray="4 4"/>'
    cup = 240; s += f'<path d="M{cup-60} 382 h120 l-12 92 q-2 12 -14 12 h-68 q-12 0 -14 -12 z" fill="#FFFFFF" stroke="{KRAFT_D}" stroke-width="2"/>'
    mix = ICOL.get(ings[0], "#B3263E"); s += f'<path d="M{cup-56} 398 h112 l-10 74 q-2 8 -10 8 h-72 q-8 0 -10 -8 z" fill="{mix}" opacity=".55"/>'
    s += wn_word(240, 520, 22, LOGO)
    return card(s, note)
# ---- farm basket (reuses farm_basket_1018 glyphs) ----
from farm_basket_1018 import glyph as fglyph, CARDS as FCARDS
FG = {c[1]: (c[4], c[5]) for c in FCARDS}
BASKETS = {"bamboo": ("#C9A26A", "#A27B3C", 0), "rattan": ("#9C6B42", "#7A4F2E", 1), "hyacinth": ("#B89A6A", "#8A6E44", 2)}
def basket(cx, cy, k, kind, items, liner=None, tag=None, twine=False, tote=False):
    a, b, wv = BASKETS[kind]; W = 300 * k; H = 150 * k; x0 = cx - W / 2; s = ""
    if tote:
        s += R(cx - W * .42, cy - H * .2, W * .84, H * 1.1, "#EFE6D2", "#A97F52", 6, 2) + f'<path d="M{cx-W*.25} {cy-H*.2} q{W*.25} -{H*.7} {W*.5} 0" stroke="#A97F52" stroke-width="{5*k}" fill="none"/>'
    else:
        s += f'<path d="M{cx-W*.36} {cy-H*.1} Q{cx} {cy-H*1.25} {cx+W*.36} {cy-H*.1}" stroke="{b}" stroke-width="{7*k}" fill="none"/>'
    if liner == "banana":
        s += "".join(f'<path d="M{cx} {cy+H*.1} q{dx*k} -{70*k} {dx*1.6*k} -{40*k}" stroke="#3F6B2A" stroke-width="{2*k}" fill="#5E8C3A"/>' for dx in (-110, -60, 60, 110))
    if liner == "cloth": s += f'<path d="M{x0+20*k} {cy} l{-20*k} {-36*k} l{60*k} {20*k} l{(W-120*k)} 0 l{60*k} {-20*k} l{-20*k} {36*k} z" fill="#F3EBDD" stroke="#D8CBB4"/>'
    if liner == "paper": s += f'<path d="M{x0+14*k} {cy} l{-6*k} {-30*k} l{W-16*k} 0 l{-6*k} {30*k} z" fill="#E9DDC8" stroke="#CDBA9A"/>'
    rnd = random.Random(len(items))
    pos = [(-.3, -.32), (0, -.42), (.3, -.32), (-.15, -.18), (.15, -.18), (-.38, -.12), (.38, -.12)]
    for i, it in enumerate(items[:7]):
        kd, cl = FG[it]; px, py = pos[i]; gk = .9 * k
        s += G(fglyph(kd, cl, i), cx + px * W - 120 * gk, cy + py * H * 1.6 - 85 * gk, gk)
    if not tote:
        s += G(f'<path d="M74 64 H166 L156 122 H84 Z" fill="{a}"/>' + ("".join(f'<path d="M{76+j*1.6} {74+j*12} H{164-j*1.6}" stroke="{b}" stroke-width="{3 if wv != 2 else 7}" {"stroke-dasharray=\"9 3\"" if wv == 2 else ""} fill="none"/>' for j in range(4))) + f'<rect x="72" y="60" width="96" height="8" rx="4" fill="{b}"/>', cx - 120 * (W * .8 / 96), cy - 60 * (W * .8 / 96), W * .8 / 96)
    if twine: s += f'<path d="M{cx+W*.3} {cy-6*k} q{12*k} {20*k} 0 {36*k}" stroke="#B89A6A" stroke-width="{2.4*k}" fill="none"/>' + C(cx + W * .3, cy - 8 * k, 7 * k, "#C9577A") + C(cx + W * .3, cy - 8 * k, 3 * k, "#E8C23A")
    if tag == "kraft": s += f'<path d="M{cx+W*.36} {cy+10*k} l{40*k} 0 l{12*k} {14*k} l-{12*k} {14*k} l-{40*k} 0 z" fill="{KRAFT}" stroke="{KRAFT_D}"/>' + T(cx + W * .36 + 22 * k, cy + 28 * k, "The WellNest", 11 * k, INKW, SCRIPT, 700)
    if tag == "card": s += R(cx + W * .3, cy + 6 * k, 60 * k, 40 * k, "#FFFFFF", KRAFT_D, 3) + T(cx + W * .3 + 30 * k, cy + 22 * k, "Recipe", 10 * k, INKW, SCRIPT, 700) + "".join(R(cx + W * .3 + 8 * k, cy + (28 + j * 6) * k, 44 * k, 2 * k, "#C9C2B6") for j in range(2))
    return s
def basket_card(note, kind, items, **k):
    s = R(0, 0, 480, 600, "#FAF6EE") + R(0, 440, 480, 160, "#EFE6D6") + basket(240, 330, 1.15, kind, items, **k) + wn_word(80, 540, 20, LOGO)
    return card(s, note, "#FAF6EE")
def note_card(note, style):
    s = R(0, 0, 480, 600, "#FAF6EE") + R(0, 470, 480, 130, "#EFE6D6")
    x, y, w, h = 90, 70, 300, 400
    s += R(x, y, w, h, "#FFFFFF", "#D9CDB8", 6, 1.5)
    st = style
    if st.get("head") == "script": s += wn_mark(240, y + 60, 34) + T(240, y + 124, "Delivery Day", 30, INKW, SCRIPT, 700)
    else: s += R(x, y, w, 54, KRAFT, rx=6) + R(x, y + 40, w, 14, KRAFT) + T(240, y + 36, "THIS WEEK'S BASKET", 15, "#FFFFFF", MONO, 600, extra='letter-spacing="2"') + T(240, y + 92, "The WellNest", 24, INKW, SCRIPT, 700)
    yy = y + 150; items = ["Morning glory", "Long beans", "Mango", "Longan", "Herb bundle"]
    for i, it in enumerate(items):
        if st.get("list") == "check": s += R(x + 26, yy + i * 30 - 12, 14, 14, "none", KRAFT_D, 3, 1.5)
        else: s += C(x + 33, yy + i * 30 - 5, 4, "#5E8C3A")
        s += T(x + 52, yy + i * 30, it, 15, INKW, HIND, 500, "start")
        if st.get("store"): s += T(x + w - 24, yy + i * 30, ["Fridge", "Fridge", "Counter", "Fridge", "Jar of water"][i], 12, MUTEW, MONO, 400, "end")
    yy += len(items) * 30 + 10
    if st.get("recipe"): s += R(x + 20, yy, w - 40, 60, CREAM, rx=6) + T(x + 34, yy + 24, "Try this week", 13, KRAFT_D, MONO, 600, "start") + T(x + 34, yy + 46, "Garlic morning glory stir-fry", 14, INKW, HIND, 500, "start")
    if st.get("art"): s += "".join(C(x + 30 + i * 40, y + h - 26, 9, ["#E8892B", "#5E8C3A", "#F0A830", "#B3263E", "#C9A27A", "#7FA046", "#E8C23A"][i]) for i in range(7))
    return card(s, note, "#FAF6EE")
