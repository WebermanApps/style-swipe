#!/usr/bin/env python3
"""Build Style Swipe deck wellnest-brand: the REAL WellNest brand deck, 200 pairs (Max asked for 200, so the 25-pair trim is overridden here only).
Brand identity + product/service ideas; grows the existing nest logo (no site plan, no layout). Submit goes to agent 'wellnest' via deck.submit_agent.
Sources: /workspace/wellnest/brand-review.md, ig-review.md, dropbox logos. Logo colours sampled from The-WellNest-logo_circle.png."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "wellnest-brand"; N = 200
pairs, O, add = deck("wnr_", "WellNest")
FOREST, DEEP, FRESH, LEAF, GOLD = "#267D58", "#006F3F", "#5FB050", "#AECB35", "#ECC978"
SAND, PEACH, OLIVE, SUN, GREY = "#DABC76", "#D7A363", "#D7D162", "#F3DB57", "#ABB3BD"
ROSELLE, ROSE2, PEA, PEA2, KRAFT, RICE = "#A8243F", "#C9475F", "#2F4B9A", "#5B3E96", "#C9A27A", "#FBF8F1"
RINGS = [FOREST, GOLD, FRESH, PEACH, LEAF, SAND, DEEP, GREY]
SER, SANS, SCRIPT = "'Cormorant Garamond', Georgia, serif", "'DM Sans', Hind, sans-serif", "Caveat, cursive"
LOGO = {"circle": ("img/wellnest-logo-circle.png", 150 / 128), "letter": ("img/wellnest-logo-letter.png", 2.0)}

def tf(x, y, s, size=10, col=INK, fam=SANS, wt=400, anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-family="{fam}" font-weight="{wt}" {extra}>{esc(s)}</text>'
def logo(cx, cy, w, kind="circle", filt=""):
    href, r = LOGO[kind]; h = w / r
    return f'<image href="{href}" x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" {filt}/>'
def mono_filter(c, fid):
    return f'<defs><filter id="{fid}"><feFlood flood-color="{c}"/><feComposite in2="SourceAlpha" operator="in"/></filter></defs>'
def rings(cx, cy, r, cols=RINGS, sw=2.4, n=5, tail=True):
    s = ""
    for i in range(n):
        c = cols[i % len(cols)]; rx = r * (1 - .05 * (i % 3)); ry = r * (.93 + .04 * (i % 2))
        s += f'<ellipse cx="{cx + (i%3-1)*r*.05}" cy="{cy + (i%2)*r*.04}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="{sw}" transform="rotate({i*37} {cx} {cy})" opacity=".95"/>'
    if tail: s += f'<path d="M{cx-r*1.25} {cy-r*.55} Q{cx-r*1.0} {cy-r*.3} {cx-r*.75} {cy-r*.35}" fill="none" stroke="{cols[0]}" stroke-width="{sw*.6}"/>' + f'<path d="M{cx+r*.6} {cy+r*.75} Q{cx+r*1.0} {cy+r*.6} {cx+r*1.3} {cy+r*.7}" fill="none" stroke="{INK}" stroke-width="{sw*.5}"/>'
    return s
def cap(s, y=288): return tf(120, y, s, 7.5, MUTE, SANS, 400)
def scr(body, bg="#FFFFFF"): return screen(body, bg)
ICP = {
 "sauna": "M5 20 H19 M7 16 Q9 13 7 10 Q5 7 7 4 M12 16 Q14 13 12 10 Q10 7 12 4 M17 16 Q19 13 17 10 Q15 7 17 4",
 "plunge": "M12 3 Q18 11 18 15 A6 6 0 0 1 6 15 Q6 11 12 3 Z",
 "tea": "M4 9 H16 V15 A5 5 0 0 1 11 20 H9 A5 5 0 0 1 4 15 Z M16 11 H18 A2 2 0 0 1 18 15 H16 M8 3 Q10 5 8 7 M12 3 Q14 5 12 7",
 "farm": "M12 21 V11 M12 11 Q6 11 5 5 Q11 5 12 11 M12 14 Q18 14 19 8 Q13 8 12 14",
 "cowork": "M4 6 H20 V16 H4 Z M2 19 H22",
 "stay": "M3 11 L12 4 L21 11 M5 10 V20 H19 V10 M10 20 V14 H14 V20",
 "food": "M3 12 H21 A9 7 0 0 1 3 12 Z M8 8 Q8 5 10 4 M13 8 Q13 5 15 4",
 "class": "M3 6 Q8 4 12 7 Q16 4 21 6 V19 Q16 17 12 20 Q8 17 3 19 Z M12 7 V20",
 "flower": "M9 12 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M12 9 Q12 3 15 4 Q16 8 12 9 M15 12 Q21 12 20 15 Q16 16 15 12 M12 15 Q12 21 9 20 Q8 16 12 15 M9 12 Q3 12 4 9 Q8 8 9 12",
 "basket": "M3 10 H21 L19 20 H5 Z M7 10 Q12 2 17 10 M8 13 V17 M12 13 V17 M16 13 V17",
 "hat": "M2 16 Q12 20 22 16 M6 15 Q6 8 12 8 Q18 8 18 15",
 "gift": "M4 10 H20 V20 H4 Z M3 7 H21 V10 H3 Z M12 7 V20 M12 7 Q8 2 7 5 Q7 7 12 7 Q16 2 17 5 Q17 7 12 7",
 "sun": "M8 12 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 M12 2 V4 M12 20 V22 M2 12 H4 M20 12 H22 M5 5 L6.5 6.5 M17.5 17.5 L19 19 M5 19 L6.5 17.5 M17.5 6.5 L19 5",
 "people": "M5 11 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M13 11 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M2 21 Q8 13 14 21 M10 21 Q16 13 22 21",
 "jar": "M7 6 H17 V8 Q19 9 19 12 V19 A2 2 0 0 1 17 21 H7 A2 2 0 0 1 5 19 V12 Q5 9 7 8 Z M7 3 H17 V6 H7 Z",
 "card": "M3 6 H21 V18 H3 Z M3 10 H21",
 "camera": "M3 8 H7 L9 5 H15 L17 8 H21 V19 H3 Z M8.5 13.5 a3.5 3.5 0 1 0 7 0 a3.5 3.5 0 1 0 -7 0",
 "leaf": "M5 19 Q4 6 19 5 Q19 18 5 19 Z M5 19 L13 11",
 "drop": "M12 4 Q17 11 17 14 A5 5 0 0 1 7 14 Q7 11 12 4 Z",
 "bottle": "M10 3 H14 V7 Q17 9 17 12 V20 H7 V12 Q7 9 10 7 Z",
 "bag": "M5 8 H19 L18 21 H6 Z M9 8 V6 A3 3 0 0 1 15 6 V8",
}
def icon(k, x, y, s=20, c=INK, sw=1.7, fill="none"):
    return f'<g transform="translate({x},{y}) scale({s/24})"><path d="{ICP[k]}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></g>'
def P(group, a, b, ask=None):
    def mk(o): return O(o[0], o[1], o[2], o[3], o[4])
    add(group, group, mk(a), mk(b), ask or f"{a[1]} Or {b[1]}?")

# ---------- 1 Name And Wordmark (16) ----------
G = "Name And Wordmark"
def nm(text="The WellNest", fam=SER, size=34, col=INK, sub="", wt=600, ls=0, logo_k=None, thai=None, tfam="Charm", tpos="below", note=""):
    s = ""
    if logo_k: s += logo(120, 78, 120, logo_k)
    y = 170 if logo_k else 130
    if thai and tpos == "first":
        s += tf(120, y, thai, size * .9, col, tfam, 700) + tf(120, y + 30, text, size * .5, MUTE, fam, wt)
    elif thai and tpos == "side":
        s += tf(64, y, text, size * .5, col, fam, wt) + f'<line x1="122" y1="{y-20}" x2="122" y2="{y+6}" stroke="{LINE}"/>' + tf(176, y, thai, size * .55, col, tfam, 700)
    else:
        s += tf(120, y, text, size, col, fam, wt, extra=f'letter-spacing="{ls}"')
        if thai: s += tf(120, y + 32, thai, size * .58, FOREST, tfam, 700)
    if sub: s += tf(120, y + (60 if thai and tpos == "below" else 28), sub, 9, MUTE, SANS, 400, extra='letter-spacing="1.5"')
    return scr(s + (cap(note) if note else ""))
TH, TH2 = "เดอะ เวลเนสท์", "เวลเนสท์"
for a, b in [
 (("nm_the", "Keep The WellNest", "Full name, as on the logo.", "calm", nm()), ("nm_short", "Short WellNest", "Drop The in daily use.", "quick", nm("WellNest"))),
 (("nm_cormorant", "Fine Cormorant Serif", "Light, elegant.", "calm", nm(fam=SER)), ("nm_fraunces", "Soft Fraunces Serif", "Rounder, friendlier.", "visual", nm(fam="Fraunces, serif", size=30, wt=700))),
 (("nm_brush", "Original Brush Script", "The hand-drawn letters.", "visual", scr(logo(120, 130, 190, "letter") + cap("Today's script logo"))), ("nm_serif_clean", "Clean Serif For Small Use", "Script big, serif small.", "focused", nm(sub="SMALL SIZES"))),
 (("nm_caps", "Spaced Capitals", "Calm and formal.", "focused", nm("THE WELLNEST", SANS, 20, wt=500, ls=4)), ("nm_title", "Title Case Serif", "Warm and readable.", "calm", nm(size=32))),
 (("nm_stack", "Stacked Lockup", "Nest above the name.", "visual", nm(logo_k="circle", size=22)), ("nm_line", "One-Line Lockup", "Small nest beside name.", "quick", scr(logo(52, 130, 60) + tf(148, 138, "The WellNest", 24, INK, SER, 600)))),
 (("nm_d_farm", "Organic Farm, San Sai", "Says where and what.", "focused", nm(sub="ORGANIC FARM  ·  SAN SAI")), ("nm_d_mix", "Farm, Food, Wellness", "Says the whole offer.", "visual", nm(sub="FARM  ·  FOOD  ·  WELLNESS"))),
 (("nm_d_cm", "Chiang Mai Descriptor", "Place first.", "quick", nm(sub="CHIANG MAI")), ("nm_d_est", "Family Farm Descriptor", "Family story first.", "calm", nm(sub="FAMILY FARM SINCE 2024"))),
 (("nm_green", "Forest Green Name", "Ties to the nest.", "calm", nm(col=FOREST)), ("nm_black", "Black Name", "Same as the script logo.", "focused", nm(col=INK))),
 (("nm_th_below", "Thai Name Below", "English leads, Thai second.", "calm", nm(thai=TH)), ("nm_th_side", "Thai Name Beside", "Equal weight, side by side.", "visual", nm(thai=TH2, tpos="side"))),
 (("nm_th_charm", "Thai In Charm Script", "Echoes the brush logo.", "visual", nm(thai=TH, tfam="Charm")), ("nm_th_mitr", "Thai In Mitr Rounded", "Friendly and clear.", "quick", nm(thai=TH, tfam="Mitr"))),
 (("nm_th_serif", "Thai In Noto Serif Thai", "Matches the serif.", "calm", nm(thai=TH, tfam="'Noto Serif Thai', serif")), ("nm_th_plex", "Thai In Plex Sans Thai", "Modern and plain.", "focused", nm(thai=TH, tfam="'IBM Plex Sans Thai', sans-serif"))),
 (("nm_th_first", "Thai-First Lockup", "For local signs.", "visual", nm(thai=TH, tpos="first", size=34)), ("nm_en_first", "English-First Lockup", "For guests and online.", "focused", nm(thai=TH))),
 (("nm_th_full", "Thai With The", "Full name in Thai.", "calm", nm(thai=TH)), ("nm_th_short", "Thai Without The", "Shorter Thai name.", "quick", nm(thai=TH2))),
 (("nm_one", "WellNest As One Word", "One name, capital N.", "focused", nm("The WellNest")), ("nm_two", "Well Nest As Two Words", "Easier to read.", "calm", nm("The Well Nest"))),
 (("nm_in_ring", "Name Inside The Nest", "Like today's logo.", "visual", scr(logo(120, 140, 200, "circle"))), ("nm_under_ring", "Name Under The Nest", "Clearer at small size.", "focused", scr(rings(120, 100, 48) + tf(120, 200, "The WellNest", 26, INK, SER, 600)))),
 (("nm_farm", "The WellNest Farm", "Farm in the name.", "calm", nm("The WellNest Farm", size=26)), ("nm_organic", "The WellNest Organic", "Matches the web address.", "focused", nm("The WellNest Organic", size=24))),
]: P(G, a, b)

# ---------- 2 Logo Refinements And Icon Set (16) ----------
G = "Logo And Icons"
def iconset(keys, style="line", cols=None, frame=True):
    s = ""; cols = cols or [FOREST]
    for i, k in enumerate(keys):
        x, y = 30 + (i % 3) * 66, 60 + (i // 3) * 86; c = cols[i % len(cols)]
        if style == "solid": s += f'<circle cx="{x+16}" cy="{y+16}" r="24" fill="{c}"/>' + icon(k, x + 4, y + 4, 24, "#FFFFFF", 1.8)
        else:
            if frame: s += f'<circle cx="{x+16}" cy="{y+16}" r="24" fill="none" stroke="{c}" stroke-width="1.2" ' + ('stroke-dasharray="3 2"' if style == "hand" else "") + '/>'
            s += icon(k, x + 4, y + 4, 24, c, 2.2 if style == "hand" else 1.6)
        s += tf(x + 16, y + 56, k.title(), 7.5, MUTE)
    return s
IK = ["sauna", "plunge", "tea", "farm", "cowork", "stay"]
SEAL = f'<circle cx="120" cy="140" r="78" fill="none" stroke="{FOREST}" stroke-width="1.5"/><circle cx="120" cy="140" r="62" fill="none" stroke="{FOREST}" stroke-width=".8"/><path id="sp" d="M52 140 A68 68 0 0 1 188 140" fill="none"/><text font-size="10" fill="{FOREST}" font-family="{SANS}" font-weight="600" letter-spacing="3"><textPath href="#sp" startOffset="50%" text-anchor="middle">ORGANIC FARM SAN SAI</textPath></text>'
for a, b in [
 (("lg_orig", "Original Nest Logo", "Keep every loop.", "visual", scr(logo(120, 140, 200))), ("lg_simple", "Simplified Five Loops", "Cleaner at small size.", "focused", scr(rings(120, 120, 60, sw=3) + tf(120, 230, "The WellNest", 22, INK, SER, 600)))),
 (("lg_color", "Full-Colour Nest", "All the logo colours.", "visual", scr(rings(120, 140, 70, sw=3))), ("lg_onegreen", "One-Colour Green Nest", "For stamps and print.", "focused", scr(rings(120, 140, 70, [FOREST], sw=3)))),
 (("lg_thick", "Thicker Loops", "Holds up on kraft.", "visual", scr(rings(120, 140, 70, sw=5))), ("lg_fine", "Finer Loops", "Delicate, airy.", "calm", scr(rings(120, 140, 70, sw=1.4)))),
 (("lg_tails", "Loops With Tails", "Like the original.", "calm", scr(rings(120, 140, 66, tail=True))), ("lg_closed", "Closed Loops", "Neater badge.", "focused", scr(rings(120, 140, 66, tail=False)))),
 (("lg_wn", "WN Monogram In Nest", "Small-size mark.", "focused", scr(rings(120, 140, 60, tail=False) + tf(120, 154, "WN", 40, INK, SER, 600))), ("lg_loops_only", "Loops Only, No Letters", "Pure symbol.", "visual", scr(rings(120, 140, 60, tail=False)))),
 (("lg_app_white", "App Icon On White", "Light and calm.", "calm", scr(rect(60, 80, 120, 120, "#FFFFFF", LINE, 26) + rings(120, 140, 40, tail=False))), ("lg_app_green", "App Icon On Forest Green", "Stands out on phones.", "visual", scr(rect(60, 80, 120, 120, FOREST, "none", 26) + rings(120, 140, 40, ["#FFFFFF", GOLD, LEAF], tail=False)))),
 (("lg_seal", "Round Farm Seal", "Organic stamp feel.", "visual", scr(SEAL + rings(120, 150, 30, [FOREST], 1.6, tail=False))), ("lg_plain", "Plain Mark, No Seal", "Less is more.", "calm", scr(rings(120, 140, 50, tail=False)))),
 (("ic_line", "Line Icons", "Thin and light.", "calm", scr(iconset(IK, "line"))), ("ic_solid", "Filled Circle Icons", "Bold and easy to spot.", "visual", scr(iconset(IK, "solid")))),
 (("ic_green", "Icons In Green Only", "One calm colour.", "calm", scr(iconset(IK, "line", [FOREST]))), ("ic_multi", "Icons In Logo Colours", "Each place its colour.", "visual", scr(iconset(IK, "line", [FOREST, PEACH, ROSELLE, FRESH, PEA, "#B8902F"])))),
 (("ic_hand", "Hand-Drawn Icon Style", "Loose, like the nest.", "visual", scr(iconset(IK, "hand", [FOREST]))), ("ic_geo", "Clean Geometric Icons", "Crisp and modern.", "focused", scr(iconset(IK, "line", [INK])))),
 (("ic_framed", "Icons In Rings", "Echo the nest.", "visual", scr(iconset(IK, "line", [FOREST], True))), ("ic_bare", "Icons Without Frames", "Simpler.", "quick", scr(iconset(IK, "line", [FOREST], False)))),
 (("fav_loop", "Favicon: Single Loop", "Tiny and clean.", "quick", scr(rings(120, 140, 44, [FOREST], 6, n=1, tail=False) + cap("Browser tab size"))), ("fav_n", "Favicon: N In A Loop", "Letter plus loop.", "focused", scr(rings(120, 140, 44, [FOREST], 6, n=1, tail=False) + tf(120, 158, "N", 50, INK, SER, 600) + cap("Browser tab size")))),
 (("lg_script_black", "Black Script Logo", "As drawn today.", "focused", scr(logo(120, 140, 200, "letter"))), ("lg_script_green", "Forest Green Script Logo", "Softer, ties to farm.", "calm", scr(mono_filter(FOREST, "fg") + logo(120, 140, 200, "letter", 'filter="url(#fg)"')))),
 (("lg_on_kraft", "Logo On Kraft", "Packaging test.", "visual", scr(logo(120, 140, 180), KRAFT)), ("lg_on_white", "Logo On White", "Brand base.", "calm", scr(logo(120, 140, 180)))),
 (("lg_gradient", "Keep Gradient Loops", "The real watercolour feel.", "visual", scr(logo(120, 140, 200))), ("lg_flat", "Flat-Colour Loops", "Easier to print.", "focused", scr(rings(120, 140, 70, sw=3) + tf(120, 150, "The WellNest", 18, INK, SER, 600)))),
 (("ic_core", "Six Place Icons", "Sauna to stays.", "quick", scr(iconset(IK, "line"))), ("ic_farm_tea", "Six Farm And Tea Icons", "Product side.", "calm", scr(iconset(["tea", "flower", "basket", "hat", "jar", "leaf"], "line", [FOREST, ROSELLE, PEACH, "#B8902F", PEA, FRESH])))),
]: P(G, a, b)

# ---------- 3 Palette (16) ----------
G = "Color Palette"
def pal(cols, names, primary=FOREST, btnc=None, txt=INK, bg="#FFFFFF", style="chips"):
    s = rings(36, 34, 16, tail=False, sw=1.4) + tf(60, 40, "The WellNest", 15, txt, SER, 600, "start")
    s += tf(14, 94, "Farm Days Are Back", 20, primary, SER, 600, "start") + tf(14, 112, "Harvest, tea and a long lunch.", 8.5, MUTE, SANS, 400, "start")
    if style == "blocks":
        w = 212 / len(cols)
        for i, c in enumerate(cols): s += rect(14 + i * w, 134, w, 70, c) + tf(14 + i * w + w / 2, 220, names[i], 7, MUTE)
    elif style == "lines":
        for i, c in enumerate(cols): s += rect(14, 140 + i * 18, 160, 4, c, "none", 2) + tf(226, 145 + i * 18, names[i], 7, MUTE, anchor="end")
    else:
        for i, c in enumerate(cols): s += f'<circle cx="{34 + i*50}" cy="164" r="20" fill="{c}" stroke="{LINE}"/>' + tf(34 + i * 50, 198, names[i], 7, MUTE) + tf(34 + i * 50, 208, c, 6, GREY)
    s += rect(14, 240, 212, 28, btnc or primary, "none", 14) + tf(120, 258, "BOOK A FARM DAY", 9, "#FFFFFF", SANS, 600, extra='letter-spacing="1.2"')
    return scr(s, bg)
GR = f'<defs><linearGradient id="g1"><stop offset="0" stop-color="{FOREST}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{PEACH}"/></linearGradient></defs>'
for a, b in [
 (("pl_fg", "Forest And Gold", "Straight from the nest.", "calm", pal([FOREST, GOLD, "#FFFFFF"], ["Forest", "Gold", "White"])), ("pl_dp", "Deep Green And Peach", "Warmer pairing.", "visual", pal([DEEP, PEACH, "#FFFFFF"], ["Deep Green", "Peach", "White"], DEEP))),
 (("pl_roselle", "Green With Roselle Pop", "Tea red as the spark.", "visual", pal([FOREST, ROSELLE, "#FFFFFF"], ["Forest", "Roselle", "White"], FOREST, ROSELLE)), ("pl_pea", "Green With Butterfly Pea Pop", "Cool blue spark.", "calm", pal([FOREST, PEA, "#FFFFFF"], ["Forest", "Pea Blue", "White"], FOREST, PEA))),
 (("pl_green_lead", "Green Leads", "Calm farm feel.", "calm", pal([FOREST, SAND, "#FFFFFF"], ["Forest", "Sand", "White"])), ("pl_gold_lead", "Gold Leads", "Sunny and warm.", "visual", pal(["#B8902F", FOREST, "#FFFFFF"], ["Deep Gold", "Forest", "White"], "#B8902F"))),
 (("pl_sun_pop", "Sunflower Accent", "Small bright touch.", "visual", pal([FOREST, "#D9B92E", "#FFFFFF"], ["Forest", "Sunflower", "White"], FOREST, "#B8902F")), ("pl_peach_pop", "Peach Accent", "Soft warm touch.", "calm", pal([FOREST, PEACH, "#FFFFFF"], ["Forest", "Peach", "White"], FOREST, "#B97F3E"))),
 (("pl_txt_black", "Black Text", "Matches the script logo.", "focused", pal([INK, FOREST, "#FFFFFF"], ["Ink", "Forest", "White"], INK)), ("pl_txt_green", "Deep Green Text", "Softer than black.", "calm", pal([DEEP, GOLD, "#FFFFFF"], ["Deep Green", "Gold", "White"], DEEP, DEEP, DEEP))),
 (("pl_white", "Pure White Base", "Clean and bright.", "focused", pal([FOREST, GOLD, "#FFFFFF"], ["Forest", "Gold", "White"])), ("pl_rice", "Rice-White Base", "A touch warmer.", "calm", pal([FOREST, GOLD, RICE], ["Forest", "Gold", "Rice"], bg=RICE))),
 (("pl_two", "Two Colours Only", "Strict and calm.", "focused", pal([FOREST, GOLD], ["Forest", "Gold"])), ("pl_four", "Four Logo Colours", "Richer, like the nest.", "visual", pal([FOREST, GOLD, PEACH, FRESH], ["Forest", "Gold", "Peach", "Fresh"]))),
 (("pl_lime", "Leaf Green Accent", "Fresh harvest.", "visual", pal([FOREST, "#8FAE2A", "#FFFFFF"], ["Forest", "Leaf", "White"], FOREST, "#6E8A1E")), ("pl_olive", "Olive Accent", "Earthy and quiet.", "calm", pal([FOREST, "#A9A33E", "#FFFFFF"], ["Forest", "Olive", "White"], FOREST, "#7F7A2B"))),
 (("pl_grey_lines", "Logo Grey For Lines", "Cool, crisp.", "focused", pal([FOREST, GREY, GOLD], ["Forest", "Grey", "Gold"], style="lines")), ("pl_sand_lines", "Sand For Lines", "Warm, soft.", "calm", pal([FOREST, SAND, GOLD], ["Forest", "Sand", "Gold"], style="lines"))),
 (("pl_per_tea", "A Colour Per Tea", "Roselle, Pea, Chawb Mahk.", "visual", pal([ROSELLE, PEA, "#B8902F"], ["Roselle", "Pea", "Chawb Mahk"], FOREST, style="blocks")), ("pl_house", "One House Colour", "All teas in green.", "focused", pal([FOREST, FOREST, FOREST], ["Roselle", "Pea", "Chawb Mahk"], style="blocks"))),
 (("pl_ros_deep", "Deep Roselle", "Wine red.", "calm", pal([ROSELLE, FOREST, "#FFFFFF"], ["Roselle", "Forest", "White"], ROSELLE)), ("pl_ros_bright", "Bright Roselle", "Like the pouch band.", "visual", pal([ROSE2, FOREST, "#FFFFFF"], ["Roselle Pink", "Forest", "White"], ROSE2))),
 (("pl_pea_indigo", "Indigo Pea", "Deep blue tea.", "calm", pal([PEA, FOREST, "#FFFFFF"], ["Indigo", "Forest", "White"], PEA)), ("pl_pea_violet", "Violet Pea", "Tea with lime added.", "visual", pal([PEA2, FOREST, "#FFFFFF"], ["Violet", "Forest", "White"], PEA2))),
 (("pl_cm_gold", "Chawb Mahk In Gold", "Herbal sunshine.", "visual", pal(["#B8902F", FOREST, "#FFFFFF"], ["Gold", "Forest", "White"], "#B8902F")), ("pl_cm_green", "Chawb Mahk In Fresh Green", "Herbal leaf.", "calm", pal(["#3F8F3A", GOLD, "#FFFFFF"], ["Fresh Green", "Gold", "White"], "#3F8F3A"))),
 (("pl_grad", "Soft Blends Like The Rings", "Colour blends.", "visual", scr(GR + rect(14, 120, 212, 60, "url(#g1)", "none", 30) + tf(120, 220, "Blend From The Nest", 14, INK, SER, 600))), ("pl_flat", "Flat Solid Pops", "Simple blocks.", "focused", scr(rect(14, 120, 70, 60, FOREST, "none", 8) + rect(85, 120, 70, 60, GOLD, "none", 8) + rect(156, 120, 70, 60, PEACH, "none", 8) + tf(120, 220, "Solid From The Nest", 14, INK, SER, 600)))),
 (("pl_btn_green", "Green Buttons", "On brand.", "calm", pal([FOREST, GOLD, "#FFFFFF"], ["Forest", "Gold", "White"], btnc=FOREST)), ("pl_btn_black", "Black Buttons", "Crisp and neutral.", "focused", pal([FOREST, GOLD, "#FFFFFF"], ["Forest", "Gold", "White"], btnc=INK))),
 (("pl_blocks", "Colour Blocks", "Bold panels.", "visual", pal([FOREST, GOLD, PEACH], ["Forest", "Gold", "Peach"], style="blocks")), ("pl_lines", "Thin Colour Lines", "Delicate pops.", "calm", pal([FOREST, GOLD, PEACH], ["Forest", "Gold", "Peach"], style="lines"))),
]: P(G, a, b)

# ---------- 4 Typography (16) ----------
G = "Typography"
def ty(hf, bf, hw=600, hs=26, note="", accent=None, caps=False, italic=False, sample="Harvest Day At The Farm"):
    s = rings(28, 28, 11, tail=False, sw=1.2) + tf(46, 33, "The WellNest", 11, INK, SER, 600, "start")
    s += tf(14, 76, "SEASONAL" if caps else "Seasonal", 9, FOREST, bf if caps else hf, 600, "start", 'letter-spacing="2.5"' if caps else ('font-style="italic"' if italic else ""))
    lines = wrap(sample, 16)
    for i, l in enumerate(lines): s += tf(14, 106 + i * hs * 1.08, l, hs, INK, hf, hw, "start")
    y = 106 + len(lines) * hs * 1.08 + 4
    for i, l in enumerate(wrap("Pick roselle with Mae Noy, then dry it in the sun and brew your own tea.", 40)): s += tf(14, y + i * 13, l, 9.5, MUTE, bf, 400, "start")
    if accent: s += tf(222, 262, accent, 20, ROSELLE, SCRIPT, 700, "end")
    return scr(s + cap(note, 288))
for a, b in [
 (("ty_corm_dm", "Cormorant With DM Sans", "Elegant heads.", "calm", ty(SER, SANS, note="Cormorant Garamond / DM Sans")), ("ty_frau_work", "Fraunces With Work Sans", "Warm, soft heads.", "visual", ty("Fraunces, serif", "'Work Sans', sans-serif", 700, 22, "Fraunces / Work Sans"))),
 (("ty_lora_man", "Lora With Manrope", "Bookish and clear.", "calm", ty("Lora, serif", "Manrope, sans-serif", 700, 22, "Lora / Manrope")), ("ty_bask_dm", "Baskerville With DM Sans", "Classic.", "focused", ty("'Libre Baskerville', serif", SANS, 700, 19, "Libre Baskerville / DM Sans"))),
 (("ty_serif_heads", "Serif Headings", "Matches the script logo.", "calm", ty(SER, SANS, note="Serif heads")), ("ty_sans_heads", "Sans Headings", "Modern and plain.", "focused", ty("Outfit, sans-serif", SANS, 700, 22, "Sans heads (Outfit)"))),
 (("ty_hand", "Handwritten Accent Word", "A note from the farm.", "visual", ty(SER, SANS, accent="picked today", note="Caveat accent")), ("ty_noaccent", "No Handwritten Accent", "Keep it clean.", "focused", ty(SER, SANS, note="No accent"))),
 (("ty_th_sarabun", "Thai Companion: Sarabun", "Plain, very readable.", "focused", ty(SER, "Sarabun, sans-serif", note="Body set in Sarabun")), ("ty_th_plex", "Thai Companion: Plex Sans Thai", "Modern and even.", "focused", ty(SER, "'IBM Plex Sans Thai', sans-serif", note="Body set in IBM Plex Sans Thai"))),
 (("ty_th_prompt", "Thai Companion: Prompt", "Round and friendly.", "visual", ty(SER, "Prompt, sans-serif", note="Body set in Prompt")), ("ty_th_kanit", "Thai Companion: Kanit", "Strong and compact.", "action", ty(SER, "Kanit, sans-serif", note="Body set in Kanit"))),
 (("ty_th_noto", "Thai Companion: Noto Serif Thai", "Pairs with serif heads.", "calm", ty(SER, "'Noto Serif Thai', serif", note="Body set in Noto Serif Thai")), ("ty_th_pridi", "Thai Companion: Pridi", "Warm Thai serif.", "visual", ty("Pridi, serif", SANS, 600, 22, "Heads set in Pridi"))),
 (("ty_light", "Light Large Headings", "Airy.", "calm", ty(SER, SANS, 500, 30, "Light weight")), ("ty_bold", "Bold Headings", "Confident.", "action", ty("Fraunces, serif", SANS, 700, 24, "Bold weight"))),
 (("ty_caps_lbl", "Spaced Capital Labels", "Small and calm.", "focused", ty(SER, SANS, caps=True, note="Labels in spaced capitals")), ("ty_ital_lbl", "Italic Serif Labels", "Soft and personal.", "calm", ty(SER, SANS, italic=True, note="Labels in italic serif"))),
 (("ty_body_dm", "Body In DM Sans", "Clean.", "focused", ty(SER, SANS, note="Body DM Sans")), ("ty_body_hind", "Body In Hind", "Same as Max's other brands.", "quick", ty(SER, "Hind, sans-serif", note="Body Hind"))),
 (("ty_menu_serif", "Serif Menu Prices", "Restaurant feel.", "calm", ty(SER, SER, sample="Roselle Punch 90", note="Menu in serif")), ("ty_menu_sans", "Sans Menu Prices", "Cafe feel.", "quick", ty("Outfit, sans-serif", SANS, 700, 22, sample="Roselle Punch 90", note="Menu in sans"))),
 (("ty_dmserif", "DM Serif Display Heads", "Rich contrast.", "visual", ty("'DM Serif Display', serif", SANS, 400, 24, "DM Serif Display")), ("ty_corm2", "Cormorant Heads", "Lighter contrast.", "calm", ty(SER, SANS, 600, 28, "Cormorant Garamond"))),
 (("ty_nunito", "Rounded Nunito", "Family friendly.", "visual", ty("Nunito, sans-serif", SANS, 800, 21, "Nunito")), ("ty_work", "Work Sans Heads", "Neutral, grown-up.", "focused", ty("'Work Sans', sans-serif", "'Work Sans', sans-serif", 600, 21, "Work Sans"))),
 (("ty_quote_script", "Handwritten Quotes", "Mae Noy's words.", "visual", ty(SCRIPT, SANS, 700, 28, "Quotes in Caveat", sample="We Grow It Slowly")), ("ty_quote_ital", "Italic Serif Quotes", "Gentle and literary.", "calm", ty(SER, SANS, 500, 26, "Quotes in italic serif", sample="We Grow It Slowly"))),
 (("ty_mix_two", "Two Typefaces", "Serif plus sans.", "focused", ty(SER, SANS, note="Two families")), ("ty_mix_three", "Three Typefaces", "Serif, sans, script.", "visual", ty(SER, SANS, accent="with love", note="Three families"))),
 (("ty_tight", "Tight Line Spacing", "Compact heads.", "focused", ty(SER, SANS, 600, 24, "Tight")), ("ty_open", "Open Line Spacing", "Room to breathe.", "calm", ty(SER, SANS, 500, 22, "Open", sample="Harvest Day On Our Family Farm"))),
]: P(G, a, b)

# ---------- 5 Voice And Taglines (16) ----------
G = "Voice And Taglines"
def vt(head, sub, c=FOREST):
    s = rings(120, 54, 22, tail=False, sw=1.5)
    hl = wrap(head, 17)
    for i, l in enumerate(hl): s += tf(120, 124 + i * 28, l, 24, INK, SER, 600)
    y = 124 + len(hl) * 28 + 6
    for i, l in enumerate(wrap(sub, 38)): s += tf(120, y + i * 13, l, 9.5, MUTE, SANS)
    s += rect(100, 262, 40, 2, c)
    return scr(s)
for a, b in [
 (("tg_hub", "A Local Hub For A Global Family", "The positioning, as is.", "calm", vt("A Local Hub For A Global Family", "Farm, food and rest in San Sai.")), ("tg_roots", "Local Roots, Global Family", "Shorter version.", "quick", vt("Local Roots, Global Family", "Farm, food and rest in San Sai."))),
 (("tg_grown", "Grown In San Sai, Shared Widely", "Place-proud.", "visual", vt("Grown In San Sai, Shared With The World", "Organic teas from our family farm.")), ("tg_cup", "From Our Farm To Your Cup", "Product-led.", "quick", vt("From Our Farm To Your Cup", "Organic teas from our family farm."))),
 (("vo_family", "Warm Family Voice", "Like an aunt's welcome.", "calm", vt("Come Hungry, Leave Family", "Lunch is at noon. Mae Noy is cooking.", ROSELLE)), ("vo_wellness", "Calm Wellness Voice", "Quiet and restorative.", "calm", vt("Breathe, Sweat, Rest", "Sauna, cold plunge and a cup of roselle.", PEA))),
 (("tg_guests", "Come As Guests, Leave As Family", "Hospitality promise.", "calm", vt("Come As Guests, Leave As Family", "A farm in San Sai, open to all.")), ("tg_table", "Everyone Eats At The Big Table", "Community promise.", "visual", vt("Everyone Eats At The Big Table", "Thai and foreign families, side by side."))),
 (("tg_chawb", "Chawb Mahk Means We Love It", "Teach the Thai name.", "visual", vt("Chawb Mahk Means We Like It A Lot", "Our herbal tea line.")), ("tg_picked", "Picked This Morning", "Freshness first.", "quick", vt("Picked This Morning", "Our herbal tea line."))),
 (("vo_plain", "Plain Facts", "Clear and useful.", "focused", vt("Sauna Open 7 To 7", "Cold plunge, towels and tea included.")), ("vo_poetic", "Gentle And Poetic", "Mood first.", "calm", vt("Heat, Then Cool Water", "Then tea, then the long quiet of the farm."))),
 (("tg_sweat", "Sweat, Plunge, Sip, Repeat", "Playful ritual.", "action", vt("Sweat, Plunge, Sip, Repeat", "The WellNest sauna ritual.")), ("tg_rest", "Rest Is A Farm Skill", "Thoughtful.", "calm", vt("Rest Is A Farm Skill", "The WellNest sauna ritual."))),
 (("cta_come", "Come To The Farm", "Soft invitation.", "calm", vt("Come To The Farm", "Weekends from 9.")), ("cta_book", "Book Your Farm Day", "Clear action.", "action", vt("Book Your Farm Day", "Weekends from 9."))),
 (("vo_we", "We, The Family", "Personal.", "calm", vt("We Grow It, We Dry It", "Our family left the office for this farm.")), ("vo_brand", "The WellNest As Speaker", "Brand-led.", "focused", vt("Grown And Dried At The WellNest", "An organic family farm in San Sai."))),
 (("vo_humour", "Light Humour", "A wink now and then.", "visual", vt("Our Ducks Are Not On Wifi", "But you can be, in the cowork.")), ("vo_nohumour", "No Humour", "Always calm.", "calm", vt("Quiet Cowork On The Farm", "Fast wifi, slow mornings."))),
 (("tg_mission", "Creating Wellness, Together", "Today's mission card.", "focused", vt("Creating Wellness, Sustainably Together", "Mission")), ("tg_vision", "Living Healthily And Communally", "Today's vision card.", "calm", vt("Living Healthily And Communally", "Vision"))),
 (("tg_slow", "Slow Living, Thai Style", "Lifestyle.", "calm", vt("Slow Living, Thai Style", "On an organic farm in Chiang Mai.")), ("tg_open", "Farm Life, Open To All", "Welcoming.", "visual", vt("Farm Life, Open To All", "On an organic farm in Chiang Mai."))),
 (("vo_thaiwords", "Sprinkle Thai Words", "Sawasdee, Chawb Mahk.", "visual", vt("Sawasdee From The Farm", "Chawb Mahk tea is back in stock.")), ("vo_english", "Plain English Only", "Easy for every guest.", "focused", vt("Hello From The Farm", "Our herbal tea is back in stock."))),
 (("so_love", "With Love From The Farm", "Warm sign-off.", "calm", vt("With Love From The Farm", "Sign-off on every post and card.")), ("so_see", "See You In San Sai", "Invites a visit.", "action", vt("See You In San Sai", "Sign-off on every post and card."))),
 (("pr_craft", "Sun-Dried, Hand-Picked", "Craft cues.", "calm", vt("Sun-Dried, Hand-Picked Roselle", "From our San Sai farm.", ROSELLE)), ("pr_taste", "Tart, Ruby, Caffeine Free", "Taste cues.", "quick", vt("Tart, Ruby, Caffeine Free", "Roselle herbal tea.", ROSELLE))),
 (("tg_nest", "Find Your Nest", "Plays on the name.", "visual", vt("Find Your Nest", "A local hub for a global family.")), ("tg_roots2", "Put Down Roots", "Plays on the farm.", "calm", vt("Put Down Roots", "A local hub for a global family."))),
]: P(G, a, b)

# ---------- 6 Story Angles (14) ----------
G = "Story Angles"
def st(head, body, kind="person", c=FOREST, kicker="OUR STORY"):
    s = photo(14, 14, 212, 118, c, kind, 10) + tf(14, 152, kicker, 7.5, c, SANS, 600, "start", 'letter-spacing="2"')
    hl = wrap(head, 21)
    for i, l in enumerate(hl): s += tf(14, 176 + i * 22, l, 19, INK, SER, 600, "start")
    y = 176 + len(hl) * 22
    for i, l in enumerate(wrap(body, 44)): s += tf(14, y + i * 12, l, 8.5, MUTE, SANS, 400, "start")
    return scr(s)
ALB = scr(photo(14, 14, 103, 130, FOREST, "person") + photo(123, 14, 103, 130, ROSELLE, "leaf") + photo(14, 150, 103, 100, GOLD, "sun") + photo(123, 150, 103, 100, PEA, "person") + cap("Family album grid", 274))
HAT = scr(icon("hat", 70, 50, 100, PEACH, 1.4) + tf(120, 200, "The Straw Hat", 22, INK, SER, 600) + tf(120, 222, "A symbol for hands-on care.", 9, MUTE))
for a, b in [
 (("sa_corp", "We Left Office Jobs For This", "The leap.", "visual", st("We Left Office Jobs For This Farm", "A family swaps desks for roselle rows in San Sai.")), ("sa_gens", "Farming Runs In The Family", "Roots and heritage.", "calm", st("Farming Runs In The Family", "What our grandparents grew, we grow again, organically.", "leaf"))),
 (("sa_maenoy", "Mae Noy, Head Farmer", "One face of the farm.", "visual", st("Meet Mae Noy, Head Farmer", "Straw hat, early mornings, the best roselle in San Sai.", "person", ROSELLE, "MAE NOY")), ("sa_family", "The Whole Family", "Many faces.", "calm", st("The Family Behind The Farm", "Parents, kids and cousins, each with a job.", "person", FOREST, "THE FAMILY"))),
 (("sa_day", "A Day With Mae Noy", "Day-in-the-life reels.", "visual", st("A Day On The Farm With Mae Noy", "Five in the morning to sunset, in one minute.", "sun", ROSELLE, "MAE NOY")), ("sa_recipes", "Mae Noy's Recipes", "Food and tea recipes.", "calm", st("Mae Noy's Roselle Punch", "Her recipe, step by step, in her own words.", "leaf", ROSELLE, "MAE NOY"))),
 (("sa_roselle", "Roselle Season", "Harvest drama.", "visual", st("Roselle Season Is Here", "The greenhouse turns into a red carpet.", "leaf", ROSELLE, "SEASONS")), ("sa_rain", "Rainy Season", "Quiet growth.", "calm", st("When The Rains Come", "What grows, what rests, what we cook.", "sun", PEA, "SEASONS"))),
 (("sa_organic", "Why We Farm Organic", "Values.", "focused", st("Why We Farm Organic", "No sprays, slow soil, and why it matters to us.", "leaf")), ("sa_dry", "How We Dry Our Tea", "Process.", "focused", st("How We Dry Our Tea", "Sun, shade and patience: the roselle carpet.", "sun", GOLD))),
 (("sa_neighbours", "Our Neighbour Growers", "Local community.", "calm", st("Our Neighbours Grow With Us", "Farmers from San Sai who supply the kitchen.", "person")), ("sa_guests", "Guests Who Became Family", "Global community.", "visual", st("Guests Who Became Family", "A family who came for tea and stayed a month.", "person", PEA))),
 (("sa_field_pouch", "From Field To Pouch", "Product journey.", "focused", st("From Field To Pouch", "Pick, dry, sort, pack: four steps, all by hand.", "leaf", ROSELLE, "THE PROCESS")), ("sa_field_table", "From Field To Table", "Food journey.", "visual", st("From Field To Table", "Lunch starts in the garden at 10.", "leaf", FOREST, "THE KITCHEN"))),
 (("sa_letter", "Founder Letter", "Personal and long.", "calm", st("A Letter From The Family", "Why we built The WellNest, and who it is for.", "leaf", FOREST, "LETTER")), ("sa_album", "Family Photo Album", "Show, don't tell.", "visual", ALB)),
 (("sa_table", "Thai And Foreign At One Table", "The blend, over food.", "visual", st("One Table, Two Languages", "Sunday lunch where neighbours and newcomers meet.", "person", PEACH)), ("sa_swap", "Skill Swap", "Farming for stories.", "action", st("Teach Us, We Teach You", "Farming skills for language and stories.", "person", PEA))),
 (("sa_diary", "Farm Diary", "Weekly notes.", "calm", st("Farm Diary, Week 12", "Planted lemongrass, lost a fight with ants.", "leaf", FOREST, "DIARY")), ("sa_calendar", "Season Calendar", "What's growing now.", "focused", st("What Grows When", "A year on the farm, month by month.", "sun", GOLD, "CALENDAR"))),
 (("sa_hat", "Straw Hat As Symbol", "An icon for the story.", "visual", HAT), ("sa_hands", "Hands In The Soil As Symbol", "Close-up hands.", "calm", st("Hands In The Soil", "Every pouch starts with these hands.", "leaf", PEACH))),
 (("sa_i", "Told By One Founder", "First person, I.", "calm", st("Why I Came Home To Farm", "One founder's voice, honest and direct.", "person")), ("sa_wefam", "Told By The Family", "First person, we.", "calm", st("Why We Came Home To Farm", "The family voice, shared.", "person"))),
 (("sa_kids", "Kids On The Farm", "Next generation.", "visual", st("The Next Generation", "Our kids name the ducks and taste every tea.", "person", GOLD)), ("sa_soil", "Soil Comes First", "Science of the farm.", "focused", st("Soil Comes First", "Compost, cover crops and why our tea tastes deeper.", "leaf", FRESH))),
 (("sa_why_sansai", "Why San Sai", "Place story.", "calm", st("Why San Sai", "Twenty minutes from town, a world away.", "sun", FOREST, "THE PLACE")), ("sa_name", "Why A Nest", "Name story.", "visual", st("Why We Called It A Nest", "A place to land, rest, and fly out again.", "sun", GOLD, "THE NAME"))),
]: P(G, a, b)

# ---------- 7 Packaging (18) ----------
G = "Packaging"
def pouch(name="Roselle", band=ROSELLE, band2=None, bandpos="mid", window=False, logo_size=56, bg=KRAFT, label="", shape="pouch", namefam=SER, sub="Herbal Tea · 50 g", flower=False, smile=False):
    s = ""; gid = "b" + "".join(ch for ch in name if ch.isalnum())[:6]
    if band2: s += f'<defs><linearGradient id="{gid}"><stop offset="0" stop-color="{band}"/><stop offset="1" stop-color="{band2}"/></linearGradient></defs>'
    bf = f"url(#{gid})" if band2 else band
    if shape == "box": s += rect(50, 50, 140, 190, bg, "#00000022", 4) + rect(50, 50, 140, 16, "#00000010")
    elif shape == "tin": s += rect(60, 60, 120, 20, "#8A8A8A", "none", 4) + rect(55, 78, 130, 162, bg, "#00000022", 10)
    else: s += f'<path d="M58 40 H182 L188 250 H52 Z" fill="{bg}" stroke="#00000022"/>' + rect(58, 40, 124, 8, "#00000014")
    by = {"top": 62, "mid": 150, "bottom": 200}[bandpos]
    s += rect(52 if shape == "pouch" else 50, by, 136 if shape == "pouch" else 140, 26, bf)
    if window: s += rect(90, 96, 60, 40, "#FFFFFF66", "#FFFFFF", 20) + "".join(dot(100 + i * 10, 116 + (i % 2) * 6, 4, ROSELLE if name == "Roselle" else band) for i in range(5))
    if flower: s += icon("flower", 96, 84, 48, band, 1.4)
    if smile: s += f'<path d="M100 120 Q120 140 140 120" fill="none" stroke="{band}" stroke-width="3" stroke-linecap="round"/>'
    if logo_size:
        ly = 104 if bandpos != "top" else 140
        if window or flower: ly = 168 if bandpos != "bottom" else 166
        s += logo(120, ly, logo_size, "circle")
    s += tf(120, by + 18, name, 12 if len(name) > 12 else 13, "#FFFFFF", namefam, 700)
    s += tf(120, 238, sub, 7.5, "#3A2E22") + label
    return scr(s)
TAG = f'<path d="M150 60 L170 34" stroke="{INK}"/>' + rect(160, 14, 44, 22, "#FFFFFF", LINE, 3) + tf(182, 29, "Hello", 9, ROSELLE, SCRIPT, 700)
STK = f'<circle cx="166" cy="74" r="17" fill="{FOREST}"/>' + tf(166, 77, "ORGANIC", 5.5, "#FFFFFF", SANS, 600)
SET3 = scr(rect(20, 90, 200, 150, "#FFFFFF", LINE, 6) + rect(36, 110, 50, 110, KRAFT) + rect(36, 160, 50, 14, ROSELLE) + rect(95, 110, 50, 110, KRAFT) + rect(95, 160, 50, 14, PEA) + rect(154, 110, 50, 110, KRAFT) + rect(154, 160, 50, 14, "#B8902F") + logo(120, 52, 64) + cap("Gift box, three pouches"))
BACK1 = scr(f'<path d="M58 40 H182 L188 250 H52 Z" fill="{KRAFT}"/>' + tf(120, 80, "About The Farm", 13, INK, SER, 700) + "".join(tf(120, 102 + i * 12, l, 7.5, "#3A2E22") for i, l in enumerate(wrap("Grown without sprays by our family in San Sai, Chiang Mai. Picked by hand and dried in the sun.", 28))) + tf(120, 232, "thewellnest.organic", 7.5, "#3A2E22"))
BACK2 = scr(f'<path d="M58 40 H182 L188 250 H52 Z" fill="{KRAFT}"/>' + tf(120, 80, "How To Brew", 13, INK, SER, 700) + icon("tea", 74, 96, 22, INK) + tf(140, 112, "1 tsp, 250 ml", 8, "#3A2E22") + icon("sun", 74, 130, 22, INK) + tf(140, 146, "95 C, 5 min", 8, "#3A2E22") + icon("drop", 74, 164, 22, INK) + tf(140, 180, "Add lime, honey", 8, "#3A2E22"))
CMG = "#B8902F"
for a, b in [
 (("pk_r_grad", "Roselle: Gradient Band", "Like the first pouch.", "visual", pouch(band=ROSELLE, band2=ROSE2)), ("pk_r_solid", "Roselle: Solid Band", "Calmer, crisper.", "calm", pouch(band=ROSELLE))),
 (("pk_r_top", "Roselle: Band At Top", "Name reads first.", "focused", pouch(bandpos="top")), ("pk_r_mid", "Roselle: Band In Middle", "Logo above, band below.", "calm", pouch(bandpos="mid"))),
 (("pk_r_window", "Roselle: Window Shows Tea", "See the calyces.", "visual", pouch(window=True, bandpos="mid", logo_size=40)), ("pk_r_nowin", "Roselle: No Window", "Keeps tea fresh.", "focused", pouch(bandpos="bottom"))),
 (("pk_r_biglogo", "Roselle: Big Nest Logo", "Brand first.", "visual", pouch(logo_size=86, bandpos="bottom")), ("pk_r_smalllogo", "Roselle: Small Nest Logo", "Product first.", "calm", pouch(logo_size=36))),
 (("pk_r_tag", "Roselle: Hand-Tied Tag", "Gift feel.", "visual", pouch(label=TAG)), ("pk_r_sticker", "Roselle: Organic Sticker", "Shop feel.", "quick", pouch(label=STK))),
 (("pk_r_pouch", "Roselle In A Kraft Pouch", "Light, low cost.", "quick", pouch()), ("pk_r_tin", "Roselle In A White Tin", "Keeps, reuses, gifts.", "visual", pouch(shape="tin", bg="#FFFFFF"))),
 (("pk_p_blue", "Butterfly Pea: Blue Band", "Pairs with roselle.", "calm", pouch("Butterfly Pea", PEA)), ("pk_p_grad", "Butterfly Pea: Blue To Violet", "Shows the colour change.", "visual", pouch("Butterfly Pea", PEA, PEA2))),
 (("pk_p_family", "Butterfly Pea: Kraft Family", "Line looks unified.", "focused", pouch("Butterfly Pea", PEA, bandpos="top")), ("pk_p_own", "Butterfly Pea: White Pouch", "Own look.", "visual", pouch("Butterfly Pea", PEA, bg="#FFFFFF", bandpos="top"))),
 (("pk_p_flower", "Butterfly Pea: Drawn Flower", "Shows the plant.", "visual", pouch("Butterfly Pea", PEA, bandpos="bottom", flower=True, logo_size=30)), ("pk_p_plain", "Butterfly Pea: No Drawing", "Simple.", "calm", pouch("Butterfly Pea", PEA, bandpos="bottom"))),
 (("pk_p_name", "Name: Butterfly Pea", "Clear for tourists.", "focused", pouch("Butterfly Pea", PEA, bandpos="bottom", logo_size=44)), ("pk_p_blue_tea", "Name: Blue Flower Tea", "Describes the cup.", "visual", pouch("Blue Flower Tea", PEA, bandpos="bottom", logo_size=44))),
 (("pk_cm_gold", "Chawb Mahk: Gold Label", "Warm herbal.", "visual", pouch("Chawb Mahk", CMG, sub="Herbal Blend · 40 g")), ("pk_cm_green", "Chawb Mahk: Green Label", "Fresh herbal.", "calm", pouch("Chawb Mahk", "#3F8F3A", sub="Herbal Blend · 40 g"))),
 (("pk_cm_script", "Chawb Mahk In Script", "Playful, personal.", "visual", pouch("Chawb Mahk", CMG, namefam=SCRIPT, sub="Herbal Blend · 40 g", bandpos="top")), ("pk_cm_serif", "Chawb Mahk In Serif", "Matches the house.", "calm", pouch("Chawb Mahk", CMG, sub="Herbal Blend · 40 g", bandpos="top"))),
 (("pk_cm_box", "Chawb Mahk Tea Bag Box", "Premium.", "visual", pouch("Chawb Mahk", CMG, shape="box", bg="#FFFFFF", sub="Herbal Blend · 20 Bags")), ("pk_cm_pouch", "Chawb Mahk Loose Pouch", "Loose leaf.", "quick", pouch("Chawb Mahk", CMG, sub="Herbal Blend · 40 g", bandpos="bottom"))),
 (("pk_cm_numbers", "Numbered Blends", "No. 1, No. 2, No. 3.", "focused", pouch("Chawb Mahk No. 1", CMG, sub="Lemongrass And Pandan")), ("pk_cm_names", "Named Blends", "Morning, Rest, Glow.", "visual", pouch("Chawb Mahk Rest", CMG, sub="Lemongrass And Pandan"))),
 (("pk_cm_smile", "Chawb Mahk: Smile Loop", "Name means we like it.", "visual", pouch("Chawb Mahk", CMG, smile=True, logo_size=0, sub="Herbal Blend · 40 g")), ("pk_cm_plainmark", "Chawb Mahk: Nest Only", "Brand mark only.", "calm", pouch("Chawb Mahk", CMG, sub="Herbal Blend · 40 g", bandpos="bottom", logo_size=60))),
 (("pk_set3", "Three-Tea Gift Set", "Roselle, Pea, Chawb Mahk.", "visual", SET3), ("pk_single", "Single Gift-Wrapped Pouch", "Pick one.", "quick", pouch(sub="Gift Wrapped · 50 g", label=f'<path d="M56 128 H186" stroke="{GOLD}" stroke-width="3"/>'))),
 (("pk_back_story", "Back Of Pack: Farm Story", "Like the first pouch.", "calm", BACK1), ("pk_back_brew", "Back Of Pack: Brew Guide", "Useful first.", "focused", BACK2)),
 (("pk_line_same", "Same Pouch, Colour Bands", "One family look.", "focused", scr(f'<path d="M20 70 H76 L79 240 H17 Z" fill="{KRAFT}"/>' + rect(17, 170, 62, 14, ROSELLE) + f'<path d="M92 70 H148 L151 240 H89 Z" fill="{KRAFT}"/>' + rect(89, 170, 62, 14, PEA) + f'<path d="M164 70 H220 L223 240 H161 Z" fill="{KRAFT}"/>' + rect(161, 170, 62, 14, CMG) + logo(48, 120, 36) + logo(120, 120, 36) + logo(192, 120, 36))), ("pk_line_diff", "Each Tea Its Own Pouch", "Distinct looks.", "visual", scr(f'<path d="M20 70 H76 L79 240 H17 Z" fill="{KRAFT}"/>' + rect(17, 170, 62, 14, ROSELLE) + f'<path d="M92 70 H148 L151 240 H89 Z" fill="#FFFFFF" stroke="{PEA}"/>' + icon("flower", 106, 110, 30, PEA, 1.6) + f'<path d="M164 70 H220 L223 240 H161 Z" fill="{CMG}"/>' + tf(192, 160, "Chawb", 11, "#FFFFFF", SCRIPT, 700) + tf(192, 174, "Mahk", 11, "#FFFFFF", SCRIPT, 700) + logo(48, 120, 36)))),
]: P(G, a, b)

# ---------- 8 Photo And Video Style (14) ----------
G = "Photo And Video"
def ph(kind="leaf", c=FOREST, warm=False, frame="full", capn="", vertical=False, grain=False, people=False, note=""):
    if vertical: x, y, w, h = 70, 20, 100, 200
    else: x, y, w, h = 14, 30, 212, 170
    s = photo(x, y, w, h, c, kind, 8)
    if warm: s += rect(x, y, w, h, "#ECC97833", "none", 8)
    if grain: s += "".join(dot(x + (i * 37) % w, y + (i * 53) % h, .7, "#00000033") for i in range(80))
    if people: s += photo(x + w * .55, y + h * .35, w * .4, h * .6, PEACH, "person", 6)
    if capn: s += rect(x, y + h - 30, w, 30, "#00000055") + tf(x + w / 2, y + h - 12, capn, 9, "#FFFFFF", SANS, 600)
    if frame == "border": s += rect(x - 6, y - 6, w + 12, h + 12, "none", INK, 2, 1)
    return scr(s + cap(note, 256))
for a, b in [
 (("pv_warm", "Warm Natural Light", "Golden, soft.", "calm", ph(warm=True, note="Warm grade")), ("pv_bright", "Bright Clean Light", "White, true colour.", "focused", ph(note="Clean grade"))),
 (("pv_flatlay", "Oak Tray Flat-Lays", "Like the Chawb Mahk shoot.", "visual", ph("leaf", ROSELLE, True, note="Banana leaf, oak tray, glass")), ("pv_table", "Tea On The Farm Table", "In context.", "calm", ph("sun", ROSELLE, True, note="Glass teapot, farm behind"))),
 (("pv_candid", "Candid People", "Real moments.", "visual", ph("sun", FOREST, people=True, note="Unposed")), ("pv_posed", "Simple Posed Portraits", "Clear faces.", "focused", ph("person", PEACH, note="Looking at camera"))),
 (("pv_captions", "Reels With Captions", "Silent-friendly.", "quick", ph("leaf", FOREST, vertical=True, capn="Roselle Harvest", note="Vertical, captioned")), ("pv_nocap", "Reels Without Captions", "Pure mood.", "calm", ph("leaf", FOREST, vertical=True, note="Vertical, no text"))),
 (("pv_slow", "Slow Pans", "Calm pace.", "calm", ph("sun", GOLD, note="4 to 6 second shots")), ("pv_quick", "Quick Cuts", "Energy.", "action", ph("leaf", FRESH, note="1 second cuts to music"))),
 (("pv_hands", "Hands Close-Up", "Craft and care.", "visual", ph("leaf", PEACH, note="Hands picking roselle")), ("pv_wide", "Wide Farm Views", "Space and air.", "calm", ph("sun", FOREST, note="Rows, ponds, mountains"))),
 (("pv_golden", "Golden Hour", "Evening glow.", "visual", ph("sun", GOLD, True, note="5 to 6 pm")), ("pv_morning", "Early Morning", "Mist and dew.", "calm", ph("sun", GREY, note="6 to 8 am"))),
 (("pv_grain", "Soft Film Grain", "Nostalgic.", "visual", ph("sun", PEACH, True, grain=True, note="Film look")), ("pv_crisp", "Crisp Digital", "Fresh and sharp.", "focused", ph("sun", FOREST, note="Sharp phone look"))),
 (("pv_border", "Thin Frame", "Gallery feel.", "calm", ph("leaf", FOREST, frame="border", note="Framed")), ("pv_full", "Full Bleed", "Immersive.", "visual", ph("leaf", FOREST, note="Edge to edge"))),
 (("pv_red_focus", "Roselle Red Hero Colour", "Red in every frame.", "visual", ph("leaf", ROSELLE, note="Red in every frame")), ("pv_green_focus", "Green Hero Colour", "Green in every frame.", "calm", ph("leaf", FOREST, note="Green in every frame"))),
 (("pv_maenoy", "Mae Noy On Camera", "Host-led videos.", "visual", ph("person", ROSELLE, people=True, note="Mae Noy explains")), ("pv_voice", "Voice-Over Only", "Faces stay private.", "calm", ph("leaf", FOREST, note="Narration over farm shots"))),
 (("pv_sound_nat", "Natural Farm Sound", "Birds, water, wind.", "calm", ph("sun", FOREST, note="Ambient audio")), ("pv_sound_music", "Soft Lanna Music", "Sueng and khim.", "visual", ph("sun", GOLD, True, note="Light Lanna strings"))),
 (("pv_still_life", "Still-Life Product Shots", "Pouch as hero.", "focused", ph("leaf", KRAFT, note="Pouch on linen")), ("pv_lifestyle", "Product In Use", "Tea in hands.", "visual", ph("leaf", ROSELLE, people=True, note="Glass in hand at the farm"))),
 (("pv_color_change", "Show The Colour Change", "Pea tea turns violet.", "visual", ph("leaf", PEA2, vertical=True, capn="Add Lime", note="Short magic moment")), ("pv_steam", "Show The Steam", "Hot tea, quiet.", "calm", ph("sun", ROSELLE, True, vertical=True, note="Slow steam rising"))),
]: P(G, a, b)

# ---------- 9 Sub-Brand Architecture (14) ----------
G = "Sub-Brand Architecture"
def arch(master, subs, mode="endorsed", cols=None):
    cols = cols or [FOREST]
    s = (logo(120, 46, 70) if mode != "house" else rings(120, 46, 22, tail=False)) + tf(120, 98, master, 13, INK, SER, 700) + f'<line x1="120" y1="106" x2="120" y2="118" stroke="{LINE}"/>'
    w = 212 / min(len(subs), 3)
    for i, sb in enumerate(subs):
        x, y = 14 + (i % 3) * w, 124 + (i // 3) * 76; c = cols[i % len(cols)]
        s += rect(x + 3, y, w - 6, 68, c + "18" if mode == "color" else "#FFFFFF", c if mode == "color" else LINE, 8)
        s += rings(x + w / 2, y + 18, 9, [c], 1.2, 2, False) if mode == "house" else dot(x + w / 2, y + 18, 5, c)
        for j, l in enumerate(wrap(sb, 12 if w < 100 else 22)): s += tf(x + w / 2, y + 40 + j * 11, l, 9, INK, SER, 700)
        if mode == "endorsed": s += tf(x + w / 2, y + 62, "by The WellNest", 5.8, MUTE)
    return scr(s)
SC = [ROSELLE, PEA, CMG, FOREST, PEACH, DEEP]
SIX = ["Tea", "Kitchen", "Bathhouse", "Cowork", "Stays", "Classes"]
for a, b in [
 (("ar_endorsed", "Endorsed Sub-Brands", "Chawb Mahk by The WellNest.", "focused", arch("The WellNest", ["Chawb Mahk", "Farm Table", "Stays"], "endorsed", SC)), ("ar_house", "One Branded House", "Everything is WellNest.", "calm", arch("The WellNest", ["WellNest Tea", "WellNest Kitchen", "WellNest Stays"], "house", SC))),
 (("ar_color", "Colour-Coded Sub-Brands", "Each has a colour.", "visual", arch("The WellNest", SIX, "color", SC)), ("ar_mono", "One Colour For All", "Unified.", "calm", arch("The WellNest", SIX, "endorsed", [FOREST]))),
 (("ar_tea_cm", "Tea Line Is Chawb Mahk", "Roselle, Pea inside it.", "visual", arch("Chawb Mahk", ["Roselle", "Butterfly Pea", "Lemongrass"], "endorsed", SC)), ("ar_tea_wn", "Tea Line Is WellNest Tea", "Chawb Mahk is one blend.", "focused", arch("WellNest Tea", ["Roselle", "Butterfly Pea", "Chawb Mahk"], "house", SC))),
 (("ar_stays_wn", "Stays Named WellNest Stays", "Plain and clear.", "focused", arch("The WellNest", ["WellNest Stays"], "house", [PEACH])), ("ar_stays_nest", "Stays Named The Nests", "Each unit is a Nest.", "visual", arch("The WellNest", ["The Nests"], "endorsed", [PEACH]))),
 (("ar_food_kitchen", "Food Named WellNest Kitchen", "Says what it is.", "focused", arch("The WellNest", ["WellNest Kitchen"], "house", [FOREST])), ("ar_food_table", "Food Named Farm Table", "Says how it feels.", "visual", arch("The WellNest", ["Farm Table"], "endorsed", [FOREST]))),
 (("ar_sauna_bath", "Sauna Named Bathhouse", "Sauna plus plunge.", "calm", arch("The WellNest", ["WellNest Bathhouse"], "house", [PEA])), ("ar_sauna_hot", "Sauna Named The Hot House", "Playful name.", "visual", arch("The WellNest", ["The Hot House"], "endorsed", [ROSELLE]))),
 (("ar_cowork_work", "Cowork Named WellNest Work", "Clear.", "focused", arch("The WellNest", ["WellNest Work"], "house", [DEEP])), ("ar_cowork_barn", "Cowork Named The Barn Desk", "Farm flavour.", "visual", arch("The WellNest", ["The Barn Desk"], "endorsed", [DEEP]))),
 (("ar_class_school", "Classes Named Farm School", "Learning feel.", "visual", arch("The WellNest", ["Farm School"], "endorsed", [CMG])), ("ar_class_wn", "Classes Named WellNest Classes", "Plain.", "focused", arch("The WellNest", ["WellNest Classes"], "house", [CMG]))),
 (("ar_farm_named", "Farm Has Its Own Name", "Kraignam Farm, WellNest hub.", "calm", arch("The WellNest", ["Kraignam Farm"], "endorsed", [FRESH])), ("ar_farm_same", "Farm Is The WellNest", "One name only.", "focused", arch("The WellNest", ["The Farm"], "house", [FRESH]))),
 (("ar_merch_shop", "Retail Named The Shop", "One store name.", "quick", arch("The WellNest", ["The WellNest Shop"], "house", [PEACH])), ("ar_merch_market", "Retail Named Farm Market", "Weekend stall feel.", "visual", arch("The WellNest", ["Farm Market"], "endorsed", [PEACH]))),
 (("ar_member_club", "Membership Named Nest Club", "Warm, belonging.", "visual", arch("The WellNest", ["Nest Club"], "endorsed", [CMG])), ("ar_member_pass", "Membership Named WellNest Pass", "Practical.", "quick", arch("The WellNest", ["WellNest Pass"], "house", [CMG]))),
 (("ar_three", "Three Pillars", "Farm, Food, Wellness.", "focused", arch("The WellNest", ["Farm", "Food", "Wellness"], "color", [FRESH, ROSELLE, PEA])), ("ar_four", "Four Pillars", "Farm, Food, Rest, Learn.", "visual", arch("The WellNest", ["Farm", "Food", "Rest", "Learn"], "color", [FRESH, ROSELLE, PEA, CMG]))),
 (("ar_icons_sub", "Sub-Brands With Icons", "Icon plus name.", "visual", scr(iconset(["tea", "food", "sauna", "cowork", "stay", "class"], "line", SC))), ("ar_names_sub", "Sub-Brands With Names Only", "Type only.", "focused", arch("The WellNest", SIX, "house", [INK]))),
 (("ar_thai_names", "Sub-Brands Keep Thai Words", "Chawb Mahk style names.", "visual", arch("The WellNest", ["Chawb Mahk", "Ban Suan Stays", "Khao Kitchen"], "endorsed", SC)), ("ar_en_names", "Sub-Brands In English", "Easy for all guests.", "focused", arch("The WellNest", ["Herbal Tea", "Garden Stays", "Rice Kitchen"], "endorsed", SC))),
]: P(G, a, b)

# ---------- 10 Space And Experience Mood (16) ----------
G = "Space And Experience Mood"
def mood(title, cols, names, k="sauna", words=""):
    s = tf(14, 32, title, 17, INK, SER, 700, "start") + tf(14, 46, "MOOD", 7, MUTE, SANS, 600, "start", 'letter-spacing="2"')
    s += rect(14, 58, 130, 130, cols[0], "none", 10) + icon(k, 44, 88, 70, "#FFFFFFCC", 1.4)
    for i, c in enumerate(cols[1:4]): s += rect(152, 58 + i * 44, 74, 40, c, LINE, 8)
    for i, n in enumerate(names[:4]): s += tf(14 + (i % 2) * 106, 210 + (i // 2) * 14, n, 8, MUTE, SANS, 400, "start")
    for i, l in enumerate(wrap(words, 36)): s += tf(14, 252 + i * 14, l, 10.5, INK, SER, 600, "start")
    return scr(s)
for a, b in [
 (("sm_sauna_dark", "Sauna: Dark Timber", "Deep and cosy.", "calm", mood("Sauna", ["#5A3E2B", "#8B6A4F", GOLD, "#2F2A26"], ["Smoked Teak", "Brass", "Candle Light", "Black Stone"], "sauna", "Dark wood, low light, eucalyptus.")), ("sm_sauna_pale", "Sauna: Pale Wood", "Light and airy.", "calm", mood("Sauna", ["#C9AE85", "#EBDCC3", FOREST, "#FFFFFF"], ["Pale Pine", "Linen", "Plants", "White"], "sauna", "Pale wood, daylight, lemongrass."))),
 (("sm_plunge_stone", "Plunge: River Stone", "Natural spring.", "calm", mood("Cold Plunge", ["#7D8A8C", GREY, FOREST, "#FFFFFF"], ["River Stone", "Cool Grey", "Ferns", "Steam"], "plunge", "Stone, ferns, running water.")), ("sm_plunge_tile", "Plunge: Green Tile", "Bathhouse classic.", "visual", mood("Cold Plunge", [DEEP, "#3E8E6E", "#FFFFFF", GOLD], ["Glazed Tile", "Jade", "White", "Brass"], "plunge", "Glossy green tile, brass taps."))),
 (("sm_cw_rattan", "Cowork: Rattan And Teak", "Thai craft.", "calm", mood("Cowork", [PEACH, "#B48A5A", FOREST, "#FFFFFF"], ["Rattan", "Teak", "Monstera", "White"], "cowork", "Rattan chairs, garden view.")), ("sm_cw_min", "Cowork: Calm White", "Focus first.", "focused", mood("Cowork", ["#9FA79A", "#FFFFFF", FOREST, INK], ["Lime Wash", "White", "One Plant", "Ink"], "cowork", "White walls, one plant, quiet."))),
 (("sm_food_leaf", "Food: Banana Leaf And Clay", "Rustic Lanna.", "visual", mood("Farm Table", [FOREST, "#A0522D", SAND, "#FFFFFF"], ["Banana Leaf", "Clay", "Rice Straw", "White"], "food", "Banana leaf, clay pots, shared plates.")), ("sm_food_cer", "Food: White Stoneware", "Modern farm dining.", "calm", mood("Farm Table", ["#B9B2A6", "#FFFFFF", FOREST, ROSELLE], ["Stoneware", "White", "Herbs", "Roselle"], "food", "Hand-made white plates, herb garnish."))),
 (("sm_stay_lanna", "Stays: Lanna Teak", "Northern Thai roots.", "visual", mood("Stays", ["#6B4A32", GOLD, "#FFFFFF", FOREST], ["Teak", "Brass Lamp", "Cotton", "Garden"], "stay", "Teak, hand-woven cotton, mosquito net.")), ("sm_stay_white", "Stays: White And Linen", "Calm modern.", "calm", mood("Stays", [SAND, "#FFFFFF", "#EFE8DC", FOREST], ["Sand", "White", "Linen", "Green View"], "stay", "White linen, open shutters, rice fields."))),
 (("sm_class_open", "Classes: Open Air", "By the rows.", "visual", mood("Classes", [FRESH, SAND, KRAFT, "#FFFFFF"], ["Grass", "Straw", "Kraft Aprons", "Sky"], "class", "Outdoor tables, straw hats, baskets.")), ("sm_class_kitchen", "Classes: Farm Kitchen", "Stoves and steam.", "action", mood("Classes", ["#A0522D", "#FFFFFF", FOREST, GOLD], ["Clay Stove", "Enamel", "Herbs", "Brass Pot"], "tea", "Clay stoves, enamel cups, steam."))),
 (("sm_light_lantern", "Evenings: Paper Lanterns", "Festive glow.", "visual", mood("Evenings", ["#2F2A26", GOLD, CMG, ROSELLE], ["Night", "Lantern", "Warm Gold", "Roselle"], "sun", "Lanterns, long tables, music.")), ("sm_light_day", "Daytime: Open Daylight", "Bright and airy.", "calm", mood("Daytime", [FRESH, SUN, "#FFFFFF", SAND], ["Leaf", "Sun", "White", "Sand"], "sun", "Open sides, shade trees, breeze."))),
 (("sm_scent_lemon", "Scent: Lemongrass", "Fresh and Thai.", "calm", mood("Scent", ["#8FAE2A", FRESH, "#FFFFFF", GOLD], ["Lemongrass", "Kaffir Lime", "White", "Honey"], "leaf", "Lemongrass in every towel.")), ("sm_scent_roselle", "Scent: Roselle And Wood", "Warm, fruity.", "visual", mood("Scent", [ROSELLE, "#8B6A4F", PEACH, "#FFFFFF"], ["Roselle", "Wood Smoke", "Peach", "White"], "flower", "Roselle and teak at reception."))),
 (("sm_sound_birds", "Sound: Birds And Water", "Natural.", "calm", mood("Sound", [FOREST, GREY, "#FFFFFF", SAND], ["Birds", "Water", "Wind", "Leaves"], "drop", "No speakers, just the farm.")), ("sm_sound_music", "Sound: Soft Lanna Strings", "Cultural.", "visual", mood("Sound", ["#8B6A4F", GOLD, ROSELLE, "#FFFFFF"], ["Sueng", "Khim", "Low Volume", "Evening"], "sun", "Quiet Lanna strings at sunset."))),
 (("sm_welcome_tea", "Welcome: Cold Roselle", "Every guest.", "calm", mood("Welcome", [ROSELLE, "#FFFFFF", FOREST, GOLD], ["Roselle", "Glass", "Leaf", "Gold"], "tea", "A cold roselle on arrival.")), ("sm_welcome_towel", "Welcome: Herbal Towel", "Spa ritual.", "calm", mood("Welcome", [FRESH, "#FFFFFF", LEAF, GREY], ["Lemongrass", "Cotton", "Leaf", "Cool"], "leaf", "Chilled herbal towel at the gate."))),
 (("sm_uniform_indigo", "Team Wear: Indigo Mor Hom", "Local cotton.", "visual", mood("Team Wear", [PEA, "#1F2E5E", "#FFFFFF", KRAFT], ["Indigo", "Mor Hom", "White", "Straw"], "people", "Indigo farm shirts, straw hats.")), ("sm_uniform_linen", "Team Wear: Natural Linen", "Soft neutral.", "calm", mood("Team Wear", [SAND, "#E6DCCB", FOREST, "#FFFFFF"], ["Sand", "Linen", "Green Apron", "White"], "people", "Linen tops, green aprons."))),
 (("sm_kids_garden", "Families: Kids Garden Corner", "Play and plant.", "visual", mood("Families", [FRESH, SUN, PEACH, "#FFFFFF"], ["Grass", "Sun", "Clay", "White"], "farm", "Small beds, watering cans, mud.")), ("sm_kids_quiet", "Families: Quiet Hours Too", "Adults rest.", "calm", mood("Families", [FOREST, "#FFFFFF", SAND, GREY], ["Shade", "White", "Sand", "Stone"], "leaf", "Quiet hours in the bathhouse."))),
 (("sm_tea_ritual", "Tea Service: Glass Teapot", "See the colour.", "visual", mood("Tea Service", [ROSELLE, "#FFFFFF", PEA, "#B48A5A"], ["Roselle", "Glass", "Pea Blue", "Oak Tray"], "tea", "Glass pots on oak trays.")), ("sm_tea_clay", "Tea Service: Clay Cups", "Earthy.", "calm", mood("Tea Service", ["#A0522D", SAND, FOREST, "#FFFFFF"], ["Clay", "Sand", "Leaf", "White"], "tea", "Clay cups, banana leaf coasters."))),
 (("sm_market_day", "Weekend: Market Buzz", "Lively stalls.", "action", mood("Weekends", [GOLD, ROSELLE, FRESH, "#FFFFFF"], ["Gold", "Roselle", "Leaf", "White"], "basket", "Stalls, music, kids running.")), ("sm_quiet_day", "Weekend: Slow And Quiet", "Hammocks.", "calm", mood("Weekends", [FOREST, SAND, "#FFFFFF", GREY], ["Shade", "Sand", "White", "Stone"], "leaf", "Hammocks, books, long lunch."))),
 (("sm_retreat_dawn", "Retreat: Dawn Ritual", "Start early.", "calm", mood("Retreats", [GREY, GOLD, "#FFFFFF", FOREST], ["Mist", "First Light", "White", "Green"], "sun", "Yoga at six, tea at seven.")), ("sm_retreat_fire", "Retreat: Fire Circle", "End together.", "visual", mood("Retreats", ["#2F2A26", PEACH, GOLD, ROSELLE], ["Night", "Embers", "Gold", "Roselle"], "people", "Fire circle, stories, warm tea."))),
]: P(G, a, b)
P(G, ("sm_cowork_break", "Cowork Breaks: Garden Walk", "Move outside.", "calm", mood("Cowork Breaks", [FRESH, "#FFFFFF", SAND, FOREST], ["Leaf", "White", "Path", "Shade"], "farm", "Walk the rows between calls.")),
     ("sm_cowork_sauna", "Cowork Breaks: Sauna Hour", "Heat at five.", "visual", mood("Cowork Breaks", ["#8B6A4F", GOLD, PEA, "#FFFFFF"], ["Teak", "Gold", "Cool Blue", "White"], "sauna", "Laptops close, sauna opens.")))

# ---------- 11 Social Look (14) ----------
G = "Social Look"
def grid(cols, kinds=("leaf", "person", "sun"), text_tiles=()):
    s = rings(28, 26, 12, tail=False, sw=1.2) + tf(48, 24, "thewellnest.organic", 9, INK, SANS, 600, "start") + tf(48, 35, "Organic family farm, San Sai", 7, MUTE, SANS, 400, "start")
    for i in range(9):
        x, y = 14 + (i % 3) * 71.3, 52 + (i // 3) * 71.3; c = cols[i % len(cols)]
        s += (rect(x, y, 69, 69, c) + tf(x + 34.5, y + 38, "Farm Notes", 10, "#FFFFFF", SER, 700)) if i in text_tiles else photo(x, y, 69, 69, c, kinds[i % len(kinds)], 0)
    return scr(s)
def post(head, bg="#FFFFFF", fg=INK, acc=FOREST, kind="quote", note=""):
    s = rect(20, 30, 200, 200, bg, LINE, 6)
    if kind == "quote": s += tf(40, 84, "\u201C", 50, acc, SER, 700, "start")
    if kind == "photo": s += photo(20, 30, 200, 120, acc, "leaf", 6)
    for i, l in enumerate(wrap(head, 16)): s += tf(120, (122 if kind != "photo" else 178) + i * 22, l, 19, fg, SER, 700)
    s += logo(200, 214, 26)
    return scr(s + (cap(note, 258) if note else ""))
HL = [(FOREST, "farm", "Farm"), (ROSELLE, "tea", "Tea"), (PEA, "sauna", "Sauna"), (CMG, "stay", "Stays")]
HL1 = scr("".join(rings(48 + i * 48, 130, 18, [c], 1.6, 2, False) + icon(k, 38 + i * 48, 120, 20, c, 1.6) + tf(48 + i * 48, 166, n, 7.5, MUTE) for i, (c, k, n) in enumerate(HL)))
HL2 = scr("".join(f'<circle cx="{48+i*48}" cy="130" r="20" fill="{c}"/>' + icon(k, 38 + i * 48, 120, 20, "#FFFFFF", 1.6) + tf(48 + i * 48, 166, n, 7.5, MUTE) for i, (c, k, n) in enumerate(HL)))
CAP1 = scr(photo(20, 20, 200, 150, FOREST, "leaf") + tf(20, 196, "Morning harvest. San Sai.", 10, INK, SANS, 400, "start"))
CAP2 = scr(photo(20, 20, 200, 120, FOREST, "leaf") + "".join(tf(20, 160 + i * 12, l, 8.5, INK, SANS, 400, "start") for i, l in enumerate(wrap("Mae Noy was up at five. The roselle was heavy with dew, so we waited for the sun, then picked until lunch.", 44))))
BI1 = scr(photo(20, 20, 200, 120, FOREST, "leaf") + tf(20, 160, "Thai caption line first", 9, FOREST, SANS, 600, "start") + tf(20, 176, "English caption line second", 9, INK, SANS, 400, "start") + cap("Two languages per post", 270))
BI2 = scr(photo(20, 20, 200, 120, FOREST, "leaf") + tf(20, 160, "Morning harvest, San Sai", 9, INK, SANS, 400, "start") + cap("One language per post", 270))
for a, b in [
 (("so_grid_mix", "Mixed Grid: Photos And Text", "Every few tiles a note.", "visual", grid([FOREST, ROSELLE, CMG], text_tiles=(1, 5, 6))), ("so_grid_photo", "All-Photo Grid", "Let the farm speak.", "calm", grid([FOREST, ROSELLE, CMG, PEA]))),
 (("so_grid_red", "Grid With A Roselle Thread", "Red pops across tiles.", "visual", grid([ROSELLE, FOREST, SAND])), ("so_grid_green", "Grid With A Green Thread", "Calm and leafy.", "calm", grid([FOREST, FRESH, SAND]))),
 (("so_quote_white", "White Quote Card", "Clean.", "calm", post("We Grow It Slowly", note="Quote post")), ("so_quote_green", "Green Quote Card", "Bold.", "visual", post("We Grow It Slowly", FOREST, "#FFFFFF", GOLD, note="Quote post"))),
 (("so_photo_title", "Photo With Serif Title", "Magazine feel.", "visual", post("Roselle Season", kind="photo", acc=ROSELLE)), ("so_photo_only", "Photo With Small Logo Only", "Quiet.", "calm", scr(rect(20, 30, 200, 200, "#FFFFFF", LINE, 6) + photo(20, 30, 200, 200, ROSELLE, "leaf", 6) + logo(200, 210, 30)))),
 (("so_hl_rings", "Highlights In Nest Rings", "Each highlight a loop.", "visual", HL1), ("so_hl_solid", "Highlights As Solid Dots", "Simple and bright.", "quick", HL2)),
 (("so_reel_title", "Reel Cover With Title", "Easy to browse.", "focused", ph("leaf", ROSELLE, vertical=True, capn="Roselle Punch")), ("so_reel_face", "Reel Cover With A Face", "Personal.", "visual", ph("person", PEACH, vertical=True))),
 (("so_cap_short", "Short Captions", "One line plus place.", "quick", CAP1), ("so_cap_story", "Story Captions", "A short paragraph.", "calm", CAP2)),
 (("so_bilingual", "Bilingual Captions", "Thai and English lines.", "visual", BI1), ("so_english", "English Captions Only", "One language.", "focused", BI2)),
 (("so_carousel_recipe", "Recipe Carousels", "Save-worthy.", "focused", post("Roselle Punch In Three Steps", note="Carousel, slide 1")), ("so_carousel_story", "Story Carousels", "Farm family chapters.", "calm", post("Why We Left The Office", RICE, note="Carousel, slide 1"))),
 (("so_launch_bold", "Bold Launch Post", "Big name, big colour.", "action", post("Butterfly Pea Is Here", PEA, "#FFFFFF", GOLD, "plain")), ("so_launch_soft", "Soft Launch Post", "Photo-led.", "calm", post("Butterfly Pea Is Here", kind="photo", acc=PEA))),
 (("so_logo_corner", "Logo On Every Post", "Brand recall.", "focused", post("Harvest Day", note="Small nest bottom right")), ("so_no_logo", "No Logo On Posts", "Cleaner feed.", "calm", scr(rect(20, 30, 200, 200, "#FFFFFF", LINE, 6) + tf(120, 136, "Harvest Day", 22, INK, SER, 700)))),
 (("so_story_poll", "Stories With Polls", "Ask the community.", "action", scr(rect(70, 20, 100, 200, FOREST + "22", "none", 10) + tf(120, 80, "Next Tea?", 13, INK, SER, 700) + rect(80, 100, 80, 22, "#FFFFFF", LINE, 11) + tf(120, 115, "Lemongrass", 8, INK) + rect(80, 128, 80, 22, "#FFFFFF", LINE, 11) + tf(120, 143, "Pandan", 8, INK))), ("so_story_daily", "Stories As Daily Diary", "Simple updates.", "calm", ph("sun", FOREST, vertical=True, capn="Today On The Farm"))),
 (("so_brand_tag", "Branded Hashtag Line", "One house tag.", "focused", post("Farm Life Tag", note="One tag on every post")), ("so_no_tags", "No Hashtags", "Clean captions.", "calm", post("Clean Captions", note="Words only"))),
 (("so_ugc", "Repost Guests", "Guest photos.", "visual", grid([PEACH, FOREST, ROSELLE], kinds=("person", "person", "leaf"))), ("so_own", "Own Photos Only", "Controlled look.", "focused", grid([FOREST, CMG, ROSELLE], kinds=("leaf", "sun", "leaf")))),
]: P(G, a, b)

# ---------- 12 Products And Services (30) ----------
def offer(name, price, line, k, c=FOREST, kind="Shop"):
    s = rect(14, 14, 212, 148, c + "14", "none", 12) + icon(k, 80, 48, 80, c, 1.3)
    s += tf(14, 184, kind.upper(), 7.5, c, SANS, 600, "start", 'letter-spacing="2"') + tf(226, 184, price, 9, INK, SANS, 600, "end")
    nl = wrap(name, 19)
    for i, l in enumerate(nl): s += tf(14, 206 + i * 20, l, 18, INK, SER, 700, "start")
    y = 206 + len(nl) * 20
    return scr(s + tf(14, y, line, 8.5, MUTE, SANS, 400, "start") + tf(14, 284, "Example price", 6.5, GREY, SANS, 400, "start"))
G = "Things To Sell"
for a, b in [
 (("ts_roselle_tea", "Roselle Tea", "The first product.", "calm", offer("Roselle Tea", "220 THB", "Sun-dried, 50 g pouch.", "tea", ROSELLE)), ("ts_roselle_syrup", "Roselle Syrup", "For punch and soda.", "visual", offer("Roselle Syrup", "260 THB", "For the Roselle Punch.", "bottle", ROSELLE))),
 (("ts_pea", "Butterfly Pea Tea", "Next launch.", "visual", offer("Butterfly Pea Tea", "220 THB", "Blue in the cup, violet with lime.", "flower", PEA)), ("ts_lemongrass", "Lemongrass Tea", "Easy third tea.", "calm", offer("Lemongrass Tea", "180 THB", "Grown along the rows.", "leaf", FRESH))),
 (("ts_jam", "Roselle Jam", "Breakfast table.", "calm", offer("Roselle Jam", "190 THB", "Tart, ruby, small batch.", "jar", ROSELLE)), ("ts_snack", "Candied Roselle", "Snack for the road.", "quick", offer("Candied Roselle", "120 THB", "Chewy, tart, sweet.", "bag", ROSELLE))),
 (("ts_giftbox", "Three-Tea Gift Box", "For visitors to take home.", "visual", offer("Three-Tea Gift Box", "690 THB", "Roselle, Pea, Chawb Mahk.", "gift", CMG)), ("ts_sampler", "Tea Sampler", "Try them all.", "quick", offer("Tea Sampler", "350 THB", "Six small tins.", "jar", CMG))),
 (("ts_vegbox", "Organic Veg Box", "Weekly farm box.", "calm", offer("Organic Veg Box", "450 THB", "Picked Friday, delivered Saturday.", "basket", FRESH)), ("ts_herbs", "Herb Bundles", "Small and fresh.", "quick", offer("Herb Bundle", "60 THB", "Basil, mint, lemongrass.", "leaf", FRESH))),
 (("ts_tote", "Farm Tote Bag", "Everyday merch.", "quick", offer("Farm Tote", "390 THB", "Nest logo on cotton.", "bag", FOREST, "Merch")), ("ts_hat", "Mae Noy Straw Hat", "Story merch.", "visual", offer("Mae Noy Straw Hat", "450 THB", "Woven nearby, green band.", "hat", PEACH, "Merch"))),
 (("ts_teapot", "Glass Teapot Set", "For tea lovers.", "visual", offer("Glass Teapot Set", "890 THB", "Pot, two glasses, roselle.", "tea", ROSELLE)), ("ts_mug", "Enamel Farm Mug", "Simple keepsake.", "quick", offer("Enamel Mug", "290 THB", "White with green rim.", "tea", FOREST, "Merch"))),
 (("ts_punch", "Bottled Roselle Punch", "Sell in cafes.", "action", offer("Roselle Punch", "65 THB", "Ready to drink, cold.", "bottle", ROSELLE)), ("ts_coldbrew", "Cold-Brew Butterfly Pea", "Ready to drink.", "visual", offer("Cold-Brew Pea", "65 THB", "Add lime, watch it change.", "bottle", PEA))),
 (("ts_seeds", "Roselle Seed Kit", "Grow your own.", "action", offer("Roselle Seed Kit", "150 THB", "Seeds and a how-to card.", "farm", ROSELLE)), ("ts_growkit", "Herb Grow Kit", "Balcony garden.", "action", offer("Herb Grow Kit", "390 THB", "Pot, soil, three herbs.", "farm", FRESH))),
 (("ts_scrub", "Herbal Salt Scrub", "Bathhouse retail.", "calm", offer("Herbal Salt Scrub", "320 THB", "Turmeric and lemongrass.", "jar", CMG)), ("ts_compress", "Herbal Compress Ball", "Thai tradition.", "calm", offer("Herbal Compress", "180 THB", "Steam and press.", "leaf", PEACH))),
 (("ts_sub", "Tea Club Subscription", "Monthly pouches.", "focused", offer("Tea Club", "590 THB / Month", "Two pouches, one recipe card.", "tea", FOREST, "Subscription")), ("ts_season", "Seasonal Farm Box", "Four times a year.", "visual", offer("Seasonal Farm Box", "1,200 THB", "Tea, jam, seeds, a letter.", "gift", CMG, "Subscription"))),
 (("ts_postcards", "Farm Postcards", "Small and sweet.", "quick", offer("Farm Postcards", "150 THB", "Set of six drawings.", "card", PEACH, "Merch")), ("ts_book", "Mae Noy Recipe Book", "Story product.", "visual", offer("Mae Noy's Recipes", "490 THB", "Twenty farm recipes.", "class", ROSELLE, "Merch"))),
 (("ts_honey", "Farm Honey", "Natural add-on.", "calm", offer("Farm Honey", "290 THB", "Longan blossom.", "jar", CMG)), ("ts_rice", "San Sai Organic Rice", "A local staple.", "focused", offer("San Sai Rice", "180 THB", "1 kg, organic.", "bag", SAND))),
 (("ts_corp", "Corporate Gift Boxes", "Bulk orders.", "focused", offer("Corporate Gift Box", "From 590 THB", "Custom card, 20+ boxes.", "gift", FOREST)), ("ts_favors", "Wedding Favours", "Mini roselle pouches.", "visual", offer("Wedding Favours", "45 THB Each", "Mini pouch, name tag.", "gift", ROSELLE))),
 (("ts_wreath", "Dried Roselle Wreath", "Farm decor.", "visual", offer("Dried Wreath", "650 THB", "Roselle and rice straw.", "flower", PEACH)), ("ts_pressed", "Pressed Flower Cards", "Small craft.", "calm", offer("Pressed Flower Card", "90 THB", "Butterfly pea on paper.", "card", PEA))),
]: P(G, a, b)
G = "Services"
for a, b in [
 (("sv_tour", "Farm Tour", "Walk the rows.", "calm", offer("Farm Tour", "350 THB", "90 minutes, tea at the end.", "farm", FRESH, "Tour")), ("sv_harvest", "Harvest Day", "Pick with Mae Noy.", "action", offer("Harvest Day", "890 THB", "Half day, lunch, a pouch to take home.", "basket", ROSELLE, "Experience"))),
 (("sv_teaclass", "Tea-Making Class", "Dry, blend, brew.", "action", offer("Tea-Making Class", "990 THB", "Make your own blend.", "tea", ROSELLE, "Class")), ("sv_cook", "Farm Cooking Class", "Pick and cook.", "action", offer("Farm Cooking Class", "1,290 THB", "Four dishes from the garden.", "food", FOREST, "Class"))),
 (("sv_sauna", "Sauna And Plunge Pass", "Two hours.", "calm", offer("Sauna And Plunge", "450 THB", "Two hours, towel, roselle.", "sauna", PEA, "Wellness")), ("sv_steam", "Thai Herbal Steam", "Traditional.", "calm", offer("Herbal Steam", "350 THB", "Lemongrass and plai.", "leaf", FRESH, "Wellness"))),
 (("sv_weekend", "Weekend Retreat", "Two nights, all in.", "visual", offer("Weekend Retreat", "6,900 THB", "Stay, meals, sauna, a class.", "stay", PEACH, "Retreat")), ("sv_dayretreat", "Day Retreat", "Sunrise to sunset.", "quick", offer("Day Retreat", "1,900 THB", "Yoga, sauna, lunch, tea.", "sun", CMG, "Retreat"))),
 (("sv_member", "Monthly Membership", "Sauna and cowork.", "focused", offer("Nest Membership", "2,900 THB / Mo", "Sauna, cowork, 10% food.", "people", FOREST, "Membership")), ("sv_tenpass", "Ten-Visit Pass", "Flexible.", "quick", offer("Ten-Visit Pass", "3,500 THB", "Any mix of sauna and cowork.", "card", FOREST, "Pass"))),
 (("sv_cw_day", "Cowork Day Pass", "Drop in.", "quick", offer("Cowork Day", "250 THB", "Wifi, tea, lunch deal.", "cowork", DEEP, "Cowork")), ("sv_cw_month", "Monthly Desk", "Regulars.", "focused", offer("Monthly Desk", "3,900 THB", "Your desk, sauna twice a week.", "cowork", DEEP, "Cowork"))),
 (("sv_farmstay", "Farm Stay Units", "Rental nights.", "calm", offer("Farm Stay", "1,800 THB / Night", "Breakfast from the garden.", "stay", PEACH, "Stay")), ("sv_glamp", "Garden Tents", "Lighter, seasonal.", "visual", offer("Garden Tent", "1,200 THB / Night", "Cool season only.", "stay", SAND, "Stay"))),
 (("sv_kids", "Kids Farm Camp", "School holidays.", "action", offer("Kids Farm Camp", "2,500 THB", "Three mornings of farm life.", "farm", CMG, "Camp")), ("sv_family", "Family Farm Day", "All ages.", "visual", offer("Family Farm Day", "1,500 THB", "Two adults, two kids, lunch.", "people", FRESH, "Experience"))),
 (("sv_dinner", "Private Farm Dinner", "Special nights.", "visual", offer("Private Farm Dinner", "1,900 THB pp", "Long table among the rows.", "food", ROSELLE, "Dining")), ("sv_sunday", "Sunday Farm Table", "Weekly community lunch.", "calm", offer("Sunday Farm Table", "450 THB", "Shared lunch, Thai and foreign.", "food", FOREST, "Dining"))),
 (("sv_offsite", "Team Offsites", "Companies.", "focused", offer("Team Offsite", "From 2,500 THB", "Cowork, harvest, dinner.", "people", DEEP, "Groups")), ("sv_corpclass", "Company Workshops", "Tea or cooking.", "action", offer("Company Workshop", "From 800 THB", "Hands-on team class.", "class", CMG, "Groups"))),
 (("sv_adopt", "Adopt A Roselle Row", "Your row, your tea.", "visual", offer("Adopt A Row", "2,400 THB / Year", "Name sign, four tea pouches.", "farm", ROSELLE, "Program")), ("sv_volunteer", "Work-Exchange Weeks", "Help and learn.", "action", offer("Work Exchange", "Free Stay", "Four hours a day on the farm.", "basket", FRESH, "Program"))),
 (("sv_lang", "Thai Lessons On The Farm", "Words while you pick.", "visual", offer("Thai On The Farm", "590 THB", "Learn words while you pick.", "class", PEA, "Class")), ("sv_yoga", "Morning Yoga", "Before the heat.", "calm", offer("Morning Yoga", "300 THB", "7 am, tea after.", "sun", FRESH, "Wellness"))),
 (("sv_market", "Weekend Market Stall", "Meet people in town.", "quick", offer("Market Stall", "Saturdays", "Tea, punch, veg box sign-ups.", "basket", CMG, "Pop-Up")), ("sv_popup", "Pop-Up Tea Bar In Town", "Monthly in the city.", "action", offer("Pop-Up Tea Bar", "Monthly", "Roselle punch, butterfly pea.", "tea", ROSELLE, "Pop-Up"))),
 (("sv_events", "Small Weddings And Events", "Farm venue.", "visual", offer("Farm Events", "On Request", "Up to 60 guests.", "people", PEACH, "Events")), ("sv_birthday", "Kids Birthday Parties", "Farm party.", "action", offer("Farm Birthday", "From 4,900 THB", "Tour, crafts, roselle cake.", "gift", ROSELLE, "Events"))),
 (("sv_online", "Online Tea Class", "Live, with a kit.", "focused", offer("Online Tea Class", "790 THB", "Kit posted, class on video.", "tea", PEA, "Online")), ("sv_videos", "Free Farm Video Series", "Builds the brand.", "calm", offer("Farm Video Series", "Free", "Mae Noy, every Friday.", "camera", FOREST, "Online"))),
]: P(G, a, b)

cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
print("pairs built:", len(pairs), cnt)
assert len(pairs) == N, len(pairs)
publish(DID, "WellNest Brand Deck", "WellNest", pairs,
        {"brands": ["The WellNest, organic family farm hub in San Sai, Chiang Mai: real brand deck (grow the nest logo, no site plan)",
                    "White base, logo colours as delicate pops, drawn SVGs, no emoji, Title Case, Thai only in Thai wordmark options"],
         "submit_agent": "wellnest", "submit_to": "WellNest Agent", "section_counts": cnt, "deck_size": N,
         "trim_override": "200 pairs at Max's explicit request (default deck size stays 25)",
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"feed": "/workspace/ops/team-feed.md", "review": "/workspace/wellnest/brand-review.md", "ig": "/workspace/wellnest/ig-review.md", "logos": "img/wellnest-logo-circle.png, img/wellnest-logo-letter.png"}},
        seed=2026, n=N)
