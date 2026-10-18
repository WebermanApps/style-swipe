"""Home page hero deck Oct 18 2026 (20:49 ICT request): fix the phone hero headline and layout on the Smart Upkeep home page.
10 this-or-that picks, Notes on every card, light only, Khand headings + Hind body, phone-first. Every screen is a drawn MOCKUP of the
phone hero (390 px wide, drawn 1:0.615) using the site's real header, real illustration (assets/teaser-v7-phone-1x1-poster.jpg, cropped)
and real colours (styles.css .hm-hero / .hm-hchip t0-t3). Nothing here edits the live site; the home page stays locked."""
from md1018_kit import *
from draft_svg import crisp
LOC = "Smart Upkeep Home Page Hero Mockup"
K = 240 / 390                       # phone CSS px -> card units
BG = "#FBF6EE"; BORD = "#EADFCF"; HEAD = "#2A1D15"; LEAD = "#5A4636"; EYE = "#8A7F74"
HM, YH, CS, FQ = "Home Maintenance Membership", "Your Home, Taken Care Of.", "Catch small problems early.", "FREE QUOTE IN MINUTES"
PILLS = [("Cancel Anytime", "t1"), ("Background-Checked Yearly", "t2"), ("Certified Techs", "t3"), ("Licensed & Insured", "t0")]
PC = {"t0": ("#C1502E1C", "#C1502E38", "#A8431F"), "t1": ("#05668D1A", "#05668D33", "#05668D"), "t2": ("#D4A01726", "#D4A0174D", "#7A5A0E"), "t3": ("#0B6E4F1A", "#0B6E4F33", "#0B6E4F")}
BASE = dict(order="new", align="left", hsize="big", pos="below", catch="sub", btn="compact", link=True, pills="scroll", space="mid")
CUR = dict(BASE, order="cur")
_n = [0]
def T(x, y, s, size, col, fam="hind", w=400, anchor="start", ls=None):
    f = 'font-family="Khand" font-weight="700"' if fam == "khand" else f'font-family="Hind" font-weight="{w}"'
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {f}{f" letter-spacing={chr(34)}{ls}{chr(34)}" if ls else ""}>{esc(s)}</text>'
def pill(x, y, s, k, size=12.5, pad=10):
    bg, bd, fg = PC[k]; w = len(s) * size * .5 + 2 * pad
    return rect(x, y, w, size + 15, bg, bd, 14, 1) + T(x + w / 2, y + size + 3.5, s, size, fg, w=500, anchor="middle"), w
def hero(c):
    """Draw the phone hero in CSS px; returns (svg, bottom of hero band, bottom of the plans header)."""
    c = dict(BASE, **c); cen = c["align"] == "center"; X = 195 if cen else 18; A = "middle" if cen else "start"
    g = {"air": 1.45, "mid": 1.0, "tight": .62}[c["space"]]
    hs = 44 if c["hsize"] == "big" else 34
    def text(y):
        s = ""
        if c["order"] == "cur":
            s += T(X, y + 12, HM, 13, EYE, w=400, anchor=A, ls="1"); y += 18 + 4 * g
            for i, l in enumerate(("Your Home,", "Taken Care Of.")): s += T(X, y + hs * .8 + i * hs * .98, l, hs, HEAD, "khand", anchor=A)
            y += 2 * hs * .98 + 6 * g
            if c["catch"] == "sub": s += T(X, y + 15, CS, 17, LEAD, w=400, anchor=A); y += 22
        else:
            for i, l in enumerate(("Home Maintenance", "Membership")): s += T(X, y + hs * .8 + i * hs * .98, l, hs, HEAD if i == 0 else "#C1502E", "khand", anchor=A)
            y += 2 * hs * .98 + 4 * g
            s += T(X, y + 17, YH, 19, LEAD, w=500, anchor=A); y += 24
            if c["catch"] == "sub": s += T(X, y + 4 * g + 15, CS, 16, LEAD, w=400, anchor=A); y += 22 + 4 * g
        if c["catch"] == "check":
            y += 8 * g; tw = len(CS) * 14 * .47 + 22; x0 = 195 - tw / 2 if cen else 18
            s += f'<circle cx="{x0+8:.1f}" cy="{y+8}" r="8" fill="#0B6E4F1F"/><path d="M{x0+4:.1f} {y+8} l3 3 l5 -6" fill="none" stroke="#0B6E4F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            s += T(x0 + 22, y + 13, CS[:-1], 14, "#3D3D3D", w=500); y += 18
        y += 16 * g
        bw = 354 if c["btn"] == "full" else 232; bx = 18 if c["btn"] == "full" else (195 - bw / 2 if cen else 18)
        s += rect(bx, y, bw, 48, "#C1502E", "none", 4) + T(bx + bw / 2, y + 29, FQ, 14, "#FFFFFF", w=600, anchor="middle", ls="2"); y += 48
        return s, y
    def illus(y):
        s = (rect(26, y, 338, 236, "#FFFFFF", "none", 18, 0, 'filter="url(#sh)"') + f'<clipPath id="ic{_n[0]}"><rect x="26" y="{y}" width="338" height="236" rx="18"/></clipPath>'
             f'<image href="img/upkeep-hero-1018/illustration.jpg" x="26" y="{y}" width="338" height="236" preserveAspectRatio="xMidYMid slice" clip-path="url(#ic{_n[0]})"/>')
        s += f'<circle cx="52" cy="{y+30}" r="9" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="1.8"/><path d="M49.5 {y+25.5} L56 {y+30} L49.5 {y+34.5} Z" fill="#1A1A1A"/>'
        return s, y + 236
    s = rect(0, 72, 390, 2000, BG); y = 72 + 14 * g; parts = []
    if c["pos"] == "below":
        p, y = illus(y); parts.append(p); y += 18 * g; p, y = text(y); parts.append(p)
    else:
        y += 8 * g; p, y = text(y); parts.append(p); y += 22 * g; p, y = illus(y); parts.append(p)
    s += "".join(parts); y += 14 * g
    if c["pills"] == "scroll":
        x = -18
        for tx, k in PILLS: p, w = pill(x, y, tx, k); s += p; x += w + 8
        s += (f'<defs><linearGradient id="fl{_n[0]}" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
              f'<linearGradient id="fr{_n[0]}" x1="1" x2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>'
              f'<rect x="0" y="{y-1}" width="18" height="30" fill="url(#fl{_n[0]})"/><rect x="372" y="{y-1}" width="18" height="30" fill="url(#fr{_n[0]})"/>')
    else:
        items = [PILLS[0], PILLS[2], PILLS[3]]; ws = [len(tx) * 11.5 * .5 + 18 for tx, _ in items]; x = 195 - (sum(ws) + 12) / 2
        for (tx, k), w in zip(items, ws): p, _ = pill(x, y, tx, k, 11.5, 9); s += p; x += w + 6
    y += 28 + 18 * g; hb = y
    s += rect(0, hb, 390, 400, "#FFFFFF")
    s += T(188, hb + 30, "PLANS", 14, "#C1502E", w=600, anchor="middle", ls="2") + f'<path d="M226 {hb+22} l6 6 l6 -6" fill="none" stroke="#C1502E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    y = hb + 84
    s += T(18, y, "Plans", 27, "#0A0A0A", "khand")
    if c["link"]: s += T(372, y - 2, FQ, 14, "#0A0A0A", w=600, anchor="end", ls="1.8")
    s += rect(42, y + 22, 306, 120, "#FFFFFF", "#05668D", 14, 3) + rect(-30, y + 22, 50, 120, "#FFFFFF", "#05668D", 14, 3) + rect(370, y + 22, 50, 120, "#FFFFFF", "#05668D", 14, 3)
    s += rect(60, y + 44, 116, 22, "none", "#0A0A0A", 0, 1.2) + T(118, y + 60, "MOST POPULAR", 12, "#0A0A0A", w=500, anchor="middle", ls="1")
    s += f'<image href="img/upkeep-hero-1018/header.png" x="0" y="0" width="390" height="72"/>'
    return s, hb, y + 140
def scr(c, note, y0=0, y1=None, H=None):
    """One card: cream MOCKUP band, the hero window y0..y1 (CSS px) at 0.615, terracotta note line under it."""
    _n[0] += 1; s, hb, pb = hero(c); y1 = y1 or hb + 10
    mh = (y1 - y0) * K; top = 24; Hh = H or round(top + mh + 44)
    body = (f'<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#783C1E" flood-opacity=".12"/></filter></defs>'
            f'<clipPath id="w{_n[0]}"><rect x="0" y="{top}" width="{W}" height="{mh:.1f}"/></clipPath>'
            f'<g clip-path="url(#w{_n[0]})"><g transform="translate(0,{top - y0 * K:.2f}) scale({K:.4f})">{s}</g></g>')
    body += rect(0, 0, W, top, "#FFFFFF") + t(12, 16, "HOME PAGE HERO", 7.5, INK, "hind", 700, extra='letter-spacing=".8"') + ln(top, 0, W, LINE)
    body += rect(193, 6, 36, 13, "#FFFFFF", "#D4A017", 3, 1, 'stroke-dasharray="3 2"') + t(211, 15.5, "MOCKUP", 6, "#8A6510", "hind", 700, "middle", 'letter-spacing=".5"')
    yn = Hh - 30
    body += ln(yn - 10, 0, W, LINE) + rect(12, yn - 4, 3, 24, TERRA) + t(20, yn + 6, note[0], 8.5, INK, "hind", 600) + t(20, yn + 18, note[1], 7.8, MUTE)
    sv = crisp(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="max-width:100%;height:auto">'
               f'<clipPath id="r{_n[0]}"><rect width="{W}" height="{Hh}" rx="14"/></clipPath><g clip-path="url(#r{_n[0]})"><rect width="{W}" height="{Hh}" fill="#FFFFFF"/>' + body +
               f'</g><rect x=".5" y=".5" width="{W-1}" height="{Hh-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
    return sv, Hh
def pair(ca, cb, na, nb, y0=0, y1=None):
    """Both sides of a pick share one window height so they line up."""
    ra, rb = hero(dict(BASE, **ca)), hero(dict(BASE, **cb))
    hy = max(ra[2], rb[2]) + 4 if y1 == "plans" else (y1 or max(ra[1], rb[1]) + 10)
    H = round(24 + (hy - y0) * K + 44)
    return scr(ca, na, y0, hy, H)[0], scr(cb, nb, y0, hy, H)[0]
def T_HERO():
    pairs, P = make("hero18_", "UpKeep")
    def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
    def add(group, el, sentence, ka, la, da, fa, ca, na, kb, lb, db, fb, cb, nb, y0=0, y1=None):
        a, b = pair(ca, cb, na, nb, y0, y1); P(group, LOC, el, sentence, o(ka, la, da, fa, a), o(kb, lb, db, fb, b))
    add("Headline", "Headline order", "should Home Maintenance Membership be the big headline over Your Home, Taken Care Of or keep today's order?",
        "member", "Membership As The Headline", "Home Maintenance Membership big; Your Home, Taken Care Of under it.", "focused", dict(order="new"), ("The line you love leads", "Says what it is first"),
        "current", "Current Order", "Small grey eyebrow, then Your Home, Taken Care Of big.", "calm", dict(CUR), ("Today's hero", "Membership line stays tiny"))
    add("Layout", "Text alignment", "under the centred logo and picture should the hero text be centred too or stay left-aligned?",
        "centre", "Centred Text", "Headline, lines and button all centred on the page.", "calm", dict(align="center", btn="compact"), ("Lines up with logo and picture", "One centre line top to bottom"),
        "left", "Left-Aligned Text", "Text and button start at the left edge, like today.", "practical", dict(align="left"), ("Easy to scan", "Same alignment as today"))
    add("Type", "Headline size", "should the Home Maintenance Membership headline be big or a step smaller?",
        "big", "Big Headline", "Khand 44 px, two lines, the loudest thing on the page.", "focused", dict(hsize="big"), ("Bold first look", "Same size as today"),
        "medium", "Medium Headline", "Khand 34 px, two lines, more room around it.", "calm", dict(hsize="medium"), ("Calmer, less shouty", "More of the hero fits"))
    add("Layout", "Text and picture order", "should the headline and button sit above the illustration or below it like today?",
        "above", "Text Above The Picture", "Headline and button first, the illustration under them.", "focused", dict(pos="above"), ("Message before the picture", "Button seen without scrolling"),
        "below", "Text Below The Picture", "Illustration first, then headline and button.", "warm", dict(pos="below"), ("Picture draws you in", "Same order as today"))
    add("Type", "Catch small problems early", "should Catch small problems early be a plain line of text or a small checkmark line?",
        "line", "Plain Line", "Catch small problems early as a soft grey sentence.", "calm", dict(catch="sub"), ("Quiet and simple", "Reads like a sentence"),
        "check", "Small Checkmark Line", "A small green check, then Catch small problems early.", "practical", dict(catch="check"), ("Reads as a promise", "Breaks up the grey text"))
    add("Button", "Free Quote button width", "should the Free Quote In Minutes button run the full width or stay compact?",
        "full", "Full-Width Button", "The terracotta button runs edge to edge.", "focused", dict(btn="full"), ("Easy thumb target", "Clear next step"),
        "compact", "Compact Button", "The button only as wide as its words, like today.", "calm", dict(btn="compact"), ("Lighter look", "Same as today"))
    add("Button", "Second Free Quote link", "should the second Free Quote In Minutes link next to the Plans heading stay or go?",
        "keep", "Keep The Second Link", "Free Quote In Minutes also sits right of the Plans heading.", "practical", dict(link=True), ("A quote link near the prices", "Same as today"),
        "drop", "Remove The Second Link", "Plans heading alone; the hero button is the one quote ask.", "calm", dict(link=False), ("Says it once", "Less repeated text"), y0=328, y1="plans")
    add("Trust", "Trust pills", "should the trust pills be a scrolling row that runs off the edge or three short pills that fit on one line?",
        "scroll", "Scrolling Row", "Pills slide past and run off both edges, like today.", "lively", dict(pills="scroll"), ("Shows more reasons", "Some pills cut off"),
        "static", "Three Pills That Fit", "Cancel Anytime, Certified Techs, Licensed & Insured.", "calm", dict(pills="static"), ("Nothing cut off", "Easy to read in a glance"))
    add("Spacing", "Spacing and rhythm", "should the hero breathe with more space between lines or sit tighter so more fits on screen?",
        "airy", "Airy Spacing", "More space between picture, headline, lines and button.", "calm", dict(space="air"), ("Each line gets its moment", "Feels more premium"),
        "tight", "Tight Spacing", "Less space between parts; the hero is shorter.", "practical", dict(space="tight"), ("More fits on screen", "Feels quick"))
    FIX = dict(order="new", catch="check", link=False, pills="static", space="air")
    add("Full Hero", "Full hero with the fixes", "should the whole new hero be centred with a wide button or left-aligned with a compact one?",
        "allc", "All Fixes, Centred", "Centred, full-width button, check line, three pills, airy.", "calm", dict(FIX, align="center", btn="full"), ("Everything on one centre line", "Plans link removed"),
        "alll", "All Fixes, Left-Aligned", "Left-aligned, compact button, check line, three pills, airy.", "practical", dict(FIX, align="left", btn="compact"), ("Classic reading line", "Plans link removed"))
    return pairs
