#!/usr/bin/env python3
"""Build Style Swipe deck blueprint-1 (PUBLISHED): 50 this-or-that pairs for Blueprint, Max's architecture and interior
design agent (Weberman Residence). Pairs come from Blueprint's open decisions: plan.json openItems (front door, bath faucet,
switches, door hardware, exterior light, bath stone, shower floor, utility yard, dining and courtyard tables), the 3 kitchen
calls, the wall-texture / accent plaster game, Round 3 (door hardware, dining table, exterior lights), and room layouts from
the 31-room courtyard plan. All options are drawn SVG (white base, Khand/Hind, small pops of real color, no dark rooms).
Uses tools/draft_svg.py helpers. Run from the style-swipe repo root."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draft_svg import *
DID = "blueprint-1"
WALL = "#FAF8F4"; OAK = "#D9BE94"; TEAK = "#B98A5E"; STONE = "#E4DED3"; SKY = "#DCEBF2"; LEAF = "#7FA86A"; SAGE = "#9DB58A"
ZEL = "#2F8F6B"; STEEL = "#B9BEC2"; BRONZE = "#8C6A43"; CLAY = "#C9784F"
pairs, O, add = mk("bp1_", "Blueprint")

def card(group, title, art, cap=""):
    """White card: small group label, drawn art in a soft panel, Khand title, Hind caption."""
    return screen(lbl(14, 22, group) + ic("home", 206, 10, 14, MUTE, 1.6) + rect(14, 30, 212, 196, SOFT, "none", 10) + art
                  + h1(14, 252, title, 17) + t(14, 270, cap, 8, MUTE))
def room(inner, wall=WALL, floor=OAK, win=True):
    s = rect(14, 30, 212, 150, wall, "none", 10) + rect(14, 170, 212, 56, floor, "none", 0) + rect(14, 216, 212, 10, floor, "none", 10)
    if win: s += rect(30, 52, 52, 70, SKY, "#FFFFFF", 2, 3) + f'<path d="M38 122 q8 -26 18 -10 q8 -22 20 4 V122 Z" fill="{SAGE}" opacity=".8"/>'
    return s + inner
def plant(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M0 0 q-14 -20 -4 -36 q4 14 4 36 q2 -24 14 -34 q4 18 -14 34" fill="{LEAF}"/><rect x="-7" y="0" width="14" height="14" fill="{CLAY}"/></g>'

# ---------------- Open Decisions (plan.json openItems) ----------------
G = "Open Decisions"
def door(style, wood):
    s = room("", WALL, STONE, False) + rect(90, 54, 60, 116, wood, "#FFFFFF", 1, 2) + dot(142, 116, 2.6, BRONZE)
    if style == "plank": s += "".join(f'<line x1="{90+i*10}" y1="56" x2="{90+i*10}" y2="168" stroke="#00000022"/>' for i in range(1, 6))
    elif style == "panel": s += rect(98, 64, 44, 40, "none", "#00000030", 1, 1.4) + rect(98, 112, 44, 48, "none", "#00000030", 1, 1.4)
    elif style == "glass": s += rect(100, 64, 40, 70, SKY, "#00000025", 1) + rect(98, 140, 44, 22, "none", "#00000030")
    else: s += "".join(f'<line x1="92" y1="{60+i*9}" x2="148" y2="{60+i*9}" stroke="#00000020"/>' for i in range(12))
    return s + plant(70, 156) + plant(172, 156, .9)
add(G, "Front Door Panel", O("door_plank", "Vertical Teak Planks", "Bronze pull, warm teak in tall planks.", ["warm", "natural"], "warm", card(G, "Vertical Teak Planks", door("plank", TEAK), "Bronze pull stays.")),
    O("door_panel", "Simple Two-Panel Oak", "Light oak, two quiet recessed panels.", ["light", "simple"], "airy", card(G, "Simple Two-Panel Oak", door("panel", OAK), "Light oak, bronze pull.")), "Which Front Door?")
add(G, "Front Door Light", O("door_glass", "Door With A Glass Lite", "Clear glass upper panel lets light into the genkan.", ["light", "clear"], "airy", card(G, "Door With A Glass Lite", door("glass", OAK), "Daylight into the genkan.")),
    O("door_slat", "Solid Horizontal Slats", "Closed horizontal oak slats, more privacy.", ["calm", "natural"], "warm", card(G, "Solid Horizontal Slats", door("slat", OAK), "More privacy, no glass.")), "Glass Lite Or Solid?")
def vanity(mount):
    s = room(rect(60, 120, 120, 10, "#FFFFFF", "#CFC8BC") + rect(64, 130, 112, 40, OAK) + rect(90, 112, 60, 10, "#FFFFFF", "#CFC8BC", 5) + rect(84, 52, 72, 50, "#EEF4F6", "#CFC8BC", 3), WALL, STONE, False)
    if mount == "deck": s += f'<path d="M118 112 V98 Q118 92 126 92 H132" fill="none" stroke="{STEEL}" stroke-width="4" stroke-linecap="round"/>'
    else: s += f'<path d="M120 104 H132" stroke="{STEEL}" stroke-width="4" stroke-linecap="round"/>' + dot(120, 104, 4, STEEL)
    return s
add(G, "Bath Faucet Mount", O("fauc_deck", "Deck-Mount Faucet", "Faucet stands on the counter; easy to swap.", ["simple", "clear"], "airy", card(G, "Deck-Mount Faucet", vanity("deck"), "Stands on the counter.")),
    O("fauc_wall", "Wall-Mount Faucet", "Spout comes out of the wall; clean counter.", ["clean", "light"], "airy", card(G, "Wall-Mount Faucet", vanity("wall"), "Clear counter to wipe.")), "Deck Or Wall Faucet?")
def switch(kind):
    s = room("", WALL, OAK, False) + rect(70, 60, 100, 100, "#FFFFFF", "#E0DAD0", 4)
    if kind == "rocker": s += rect(98, 80, 44, 60, "#FFFFFF", "#CFC8BC", 3) + rect(104, 86, 32, 48, "#F7F5F1", "#D9D3C9", 2)
    else: s += rect(98, 80, 44, 60, "#FFFFFF", "#CFC8BC", 3) + "".join(dot(120, 96 + i * 14, 4.5, "#FFFFFF") + f'<circle cx="120" cy="{96+i*14}" r="4.5" fill="none" stroke="{BRONZE}" stroke-width="1.5"/>' for i in range(3))
    return s
add(G, "Light Switches", O("sw_rocker", "Wide White Rocker", "One big flat rocker per plate.", ["simple", "clean"], "airy", card(G, "Wide White Rocker", switch("rocker"), "Flat, white, easy.")),
    O("sw_push", "Push Buttons, Bronze Ring", "Three round buttons with a small bronze ring.", ["crafted", "lively"], "warm", card(G, "Push Buttons, Bronze Ring", switch("push"), "Small warm metal pop.")), "Rocker Or Push Buttons?")
def handle(kind):
    s = room(rect(80, 46, 80, 134, "#FFFFFF", "#D9D3C9", 1, 1.5), WALL, OAK, False)
    if kind == "lever": s += f'<path d="M144 112 H128" stroke="{BRONZE}" stroke-width="5" stroke-linecap="round"/>' + dot(146, 112, 5, BRONZE)
    else: s += dot(146, 112, 7, OAK) + f'<circle cx="146" cy="112" r="7" fill="none" stroke="{TEAK}" stroke-width="1.5"/>'
    return s
add(G, "Door Hardware", O("hw_lever", "Slim Bronze Lever", "A thin lever in warm bronze, matches the front door.", ["warm", "clear"], "warm", card(G, "Slim Bronze Lever", handle("lever"), "Matches the front pull.")),
    O("hw_knob", "Round Oak Knob", "A soft wooden knob on white doors.", ["natural", "soft"], "airy", card(G, "Round Oak Knob", handle("knob"), "Wood in the hand.")), "Lever Or Knob?")
def walllight(kind):
    s = rect(14, 30, 212, 196, "#F1ECE3", "none", 10) + rect(14, 196, 212, 30, SAGE, "none", 0) + rect(70, 70, 100, 126, "#FFFFFF")
    if kind == "lantern": s += rect(112, 84, 16, 24, "#FFF4D6", BRONZE, 2, 1.5) + f'<path d="M108 84 H132 L120 76 Z" fill="{BRONZE}"/>'
    else: s += rect(108, 86, 24, 10, "#FFFFFF", STEEL, 2) + f'<path d="M110 96 L100 140 H140 L130 96 Z" fill="#FFF4D6" opacity=".7"/>'
    return s + rect(104, 140, 32, 56, OAK) + plant(60, 188, .8)
add(G, "Exterior Wall Light", O("ext_lantern", "Small Bronze Lantern", "A little lantern with a warm glow.", ["warm", "crafted"], "warm", card(G, "Small Bronze Lantern", walllight("lantern"), "Glow at the door.")),
    O("ext_down", "White Downlight Wash", "A plain white cylinder that washes the wall.", ["clean", "simple"], "airy", card(G, "White Downlight Wash", walllight("down"), "Soft light down the wall.")), "Lantern Or Downlight?")
def tiles(c1, c2, pat):
    s = rect(14, 30, 212, 196, "#FFFFFF", "none", 10)
    for r in range(7):
        for c in range(8):
            x, y = 22 + c * 25, 38 + r * 26
            if pat == "zel": s += rect(x, y, 23, 24, [c1, c2][(r * 3 + c) % 2], "none", 1)
            elif pat == "terr": s += rect(x, y, 23, 24, STONE, "none", 1) + "".join(dot(x + (k * 7) % 21 + 2, y + (k * 11) % 20 + 3, 1.6, [c1, c2, "#FFFFFF"][k % 3]) for k in range(6))
            elif pat == "lime": s += rect(x, y, 23, 24, c1, "#FFFFFF", 0, 1)
            else: s += rect(x, y, 23, 24, c1 if (r + c) % 3 else c2, "none", 1)
    return s
add(G, "Bath Accent Stone", O("bath_zel", "Green Zellige", "Glossy hand-made green tiles, the current stand-in.", ["lively", "crafted"], "lively", card(G, "Green Zellige", tiles(ZEL, "#3F9E78", "zel"), "Real green, hand-made.")),
    O("bath_terr", "White Terrazzo, Color Chips", "White terrazzo with small green and clay chips.", ["light", "lively"], "airy", card(G, "White Terrazzo, Color Chips", tiles(ZEL, CLAY, "terr"), "Light base, small pops.")), "Zellige Or Terrazzo?")
add(G, "Shower Floor", O("shw_lime", "Honed Limestone", "Soft pale limestone, shown now.", ["natural", "soft"], "airy", card(G, "Honed Limestone", tiles("#E9E1D2", "", "lime"), "Pale and soft underfoot.")),
    O("shw_pebble", "Flat River Pebble", "Small flat pebbles for grip.", ["natural", "earthy"], "warm", card(G, "Flat River Pebble", rect(14, 30, 212, 196, "#EDE7DC", "none", 10) + "".join(f'<ellipse cx="{24+(k*37)%200}" cy="{40+(k*53)%180}" rx="{7+k%4}" ry="{5+k%3}" fill="{["#CFC5B4","#B9AD99","#DCD3C4"][k%3]}"/>' for k in range(70)), "Grip and texture.")), "Limestone Or Pebble?")
def yard(kind):
    s = rect(14, 30, 212, 196, "#F4F0E8", "none", 10)
    if kind == "gravel": s += "".join(dot(20 + (k * 29) % 204, 36 + (k * 17) % 184, 1.4, "#BDB3A2") for k in range(260)) + "".join(rect(40 + i * 56, 90, 40, 40, "#E2DDD4", "#CFC8BC") for i in range(3))
    else: s += "".join(rect(22 + (i % 4) * 51, 38 + (i // 4) * 46, 46, 40, "#E2DDD4", "none", 1) for i in range(16)) + "".join(f'<line x1="22" y1="{80+i*46}" x2="218" y2="{80+i*46}" stroke="{SAGE}" stroke-width="5"/>' for i in range(3))
    return s
add(G, "Utility Yard Floor", O("yard_gravel", "Gravel With Concrete Pads", "Pea gravel, pads under the tanks and gear.", ["simple", "earthy"], "warm", card(G, "Gravel With Concrete Pads", yard("gravel"), "Drains well, low cost.")),
    O("yard_grid", "Pavers With Grass Joints", "Square pavers with green strips between.", ["natural", "lively"], "lively", card(G, "Pavers With Grass Joints", yard("grid"), "Greener, still drivable.")), "Gravel Or Grass-Joint Pavers?")
def table(shape, wood=OAK):
    s = rect(14, 30, 212, 196, "#FFFFFF", "none", 10) + rect(14, 30, 212, 196, "none", LINE, 10)
    chairs = []
    if shape == "round": s += f'<circle cx="120" cy="128" r="54" fill="{wood}"/>'; chairs = [(120 + 70 * c, 128 + 70 * d) for c, d in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)]]
    elif shape == "long": s += rect(46, 100, 148, 56, wood, "none", 4); chairs = [(64 + i * 37, 88) for i in range(4)] + [(64 + i * 37, 168) for i in range(4)]
    elif shape == "oval": s += f'<ellipse cx="120" cy="128" rx="80" ry="40" fill="{wood}"/>'; chairs = [(60 + i * 40, 78) for i in range(4)] + [(60 + i * 40, 178) for i in range(4)]
    else: s += rect(46, 100, 148, 56, wood, "none", 4) + rect(52, 168, 136, 14, TEAK, "none", 3); chairs = [(64 + i * 37, 88) for i in range(4)]
    return s + "".join(rect(x - 9, y - 9, 18, 18, "#FFFFFF", TEAK, 4, 1.5) for x, y in chairs) + plant(205, 210, .6)
add(G, "Dining Table", O("dine_round", "Round Oak For Eight", "One big round table; everyone faces in.", ["soft", "lively"], "lively", card(G, "Round Oak For Eight", table("round"), "Plan view, 8 seats.")),
    O("dine_long", "Long Oak Farm Table", "Long rectangle, four a side.", ["natural", "simple"], "warm", card(G, "Long Oak Farm Table", table("long"), "Plan view, 8 seats.")), "Round Or Long Dining Table?")
add(G, "Courtyard Table", O("court_oval", "Teak Oval Outside", "Oval teak table under the courtyard trees.", ["natural", "soft"], "warm", card(G, "Teak Oval Outside", table("oval", TEAK), "Weathers to silver.")),
    O("court_bench", "Table With A Built-In Bench", "Table plus a long built-in bench on one side.", ["simple", "warm"], "warm", card(G, "Table With A Built-In Bench", table("bench", TEAK), "Fewer chairs to move.")), "Oval Or Bench Table?")

# ---------------- Kitchen Calls ----------------
G = "Kitchen Calls"
def kitchen(herb="corner", faucet="brushed", fridge="built"):
    s = room(rect(14, 130, 212, 46, "#FFFFFF", "#E0DAD0") + rect(14, 124, 212, 6, STONE) + rect(100, 52, 120, 40, "#FFFFFF", "#E0DAD0"), WALL, OAK)
    if herb == "corner": s += rect(18, 52, 26, 70, "#FFFFFF", "#E0DAD0") + "".join(dot(26 + (k % 2) * 10, 60 + k * 7, 4, LEAF) for k in range(8))
    else: s += rect(100, 96, 80, 24, "#FFFFFF", "#E0DAD0") + "".join(dot(106 + k * 10, 108, 4.5, LEAF) for k in range(8))
    fc = {"brushed": STEEL, "bronze": BRONZE, "white": "#FFFFFF"}[faucet]
    s += f'<path d="M70 124 V104 Q70 96 80 96 H86 V102" fill="none" stroke="{fc}" stroke-width="4" stroke-linecap="round"/>'
    if fridge == "built": s += rect(188, 52, 32, 124, "#FFFFFF", "#E0DAD0") + f'<line x1="214" y1="80" x2="214" y2="110" stroke="{STEEL}" stroke-width="2"/>'
    else: s += rect(186, 60, 36, 116, STEEL, "#9EA4A8", 4) + f'<line x1="186" y1="100" x2="222" y2="100" stroke="#9EA4A8"/>'
    return s
add(G, "Herb Nook", O("k_herb_corner", "Herb Nook In The Corner", "Moved to the corner, out of the work zone.", ["lively", "natural"], "lively", card(G, "Herb Nook In The Corner", kitchen("corner"), "Blueprint's call.")),
    O("k_herb_back", "Herb Shelf On The Backsplash", "A long herb shelf right behind the counter.", ["visual", "lively"], "lively", card(G, "Herb Shelf On The Backsplash", kitchen("back"), "In reach while cooking.")), "Corner Nook Or Backsplash Shelf?")
add(G, "Kitchen Faucet", O("k_fauc_brushed", "Brushed Stainless Faucet", "Matches the appliances; hides spots.", ["clear", "simple"], "airy", card(G, "Brushed Stainless Faucet", kitchen(faucet="brushed"), "Blueprint's call.")),
    O("k_fauc_bronze", "Warm Bronze Faucet", "Ties to the door hardware.", ["warm", "crafted"], "warm", card(G, "Warm Bronze Faucet", kitchen(faucet="bronze"), "One warm metal pop.")), "Stainless Or Bronze Faucet?")
add(G, "Fridge", O("k_fridge_built", "Built-In Panel Fridge", "Fridge hides behind white flush panels.", ["clean", "calm"], "airy", card(G, "Built-In Panel Fridge", kitchen(fridge="built"), "Disappears into cabinets.")),
    O("k_fridge_free", "Freestanding Stainless Fridge", "A stand-alone stainless fridge, easy to replace.", ["simple", "clear"], "airy", card(G, "Freestanding Stainless Fridge", kitchen(fridge="free"), "Cheaper to swap later.")), "Built-In Or Freestanding?")
def island(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "none", 10) + rect(14, 30, 212, 196, "none", LINE, 10) + rect(22, 38, 196, 20, STONE) + rect(22, 38, 20, 150, STONE)
    if kind == "seats": s += rect(70, 100, 120, 44, OAK, "none", 3) + "".join(dot(84 + i * 30, 158, 8, "#FFFFFF") + f'<circle cx="{84+i*30}" cy="158" r="8" fill="none" stroke="{TEAK}" stroke-width="1.5"/>' for i in range(4))
    else: s += rect(70, 100, 120, 44, OAK, "none", 3) + rect(196, 92, 22, 60, OAK, "none", 3) + "".join(dot(207, 104 + i * 18, 6, "#FFFFFF") for i in range(3))
    return s
add(G, "Island Seating", O("k_isl_side", "Four Stools Along The Island", "Stools on the long side, facing the cook.", ["lively", "simple"], "lively", card(G, "Four Stools Along The Island", island("seats"), "Plan view.")),
    O("k_isl_end", "Short Table At The Island End", "A small table off the end for three.", ["warm", "soft"], "warm", card(G, "Short Table At The Island End", island("end"), "Plan view.")), "Stools Or End Table?")
def pantry(kind):
    s = room("", WALL, OAK, False)
    if kind == "open": s += "".join(rect(40, 56 + i * 28, 160, 4, OAK) + "".join(rect(46 + k * 22, 40 + i * 28, 14, 16, [CLAY, "#FFFFFF", ZEL, "#F2E6CF"][k % 4], "#E0DAD0") for k in range(7)) for i in range(4))
    else: s += "".join(rect(40 + i * 40, 50, 38, 120, "#FFFFFF", "#E0DAD0") for i in range(4)) + "".join(f'<line x1="{72+i*40}" y1="104" x2="{72+i*40}" y2="116" stroke="{BRONZE}" stroke-width="2"/>' for i in range(4))
    return s
add(G, "Walk-In Pantry", O("k_pan_open", "Open Shelves With Jars", "See everything at a glance.", ["visual", "lively"], "lively", card(G, "Open Shelves With Jars", pantry("open"), "Colorful, easy to find.")),
    O("k_pan_closed", "White Closed Cabinets", "Calm doors, everything hidden.", ["clean", "calm"], "airy", card(G, "White Closed Cabinets", pantry("closed"), "Tidy and quiet.")), "Open Or Closed Pantry?")

# ---------------- Walls And Plaster ----------------
G = "Walls And Plaster"
def wall(tex, col="#FFFFFF", accent=None):
    s = rect(14, 30, 212, 196, col, "none", 10)
    if tex == "smooth": pass
    elif tex == "sand": s += "".join(dot(18 + (k * 23) % 206, 34 + (k * 41) % 188, .9, "#00000014") for k in range(500))
    elif tex == "trowel": s += "".join(f'<path d="M{18+(k*37)%190} {40+(k*29)%176} q14 -6 28 0" fill="none" stroke="#00000012" stroke-width="3"/>' for k in range(70))
    elif tex == "lime": s += "".join(f'<ellipse cx="{24+(k*47)%200}" cy="{40+(k*31)%180}" rx="22" ry="12" fill="#00000008"/>' for k in range(40))
    if accent: s += rect(14, 30, 212, 196, accent, "none", 10, extra='opacity=".0"')
    return s + rect(14, 196, 212, 30, OAK, "none", 0) + plant(190, 192, .7) + rect(40, 150, 70, 30, "#FFFFFF", "#E0DAD0", 4)
add(G, "Wall Texture", O("w_smooth", "Smooth White", "Flat, crisp, easy to paint over.", ["clean", "light"], "airy", card(G, "Smooth White", wall("smooth"), "Steel-stud walls, white.")),
    O("w_sand", "Fine Sand Finish", "A soft grain you notice up close.", ["soft", "natural"], "airy", card(G, "Fine Sand Finish", wall("sand"), "Hides small dings.")), "Smooth Or Fine Sand?")
add(G, "Plaster Feel", O("w_trowel", "Light Trowel Marks", "Gentle hand-trowel sweeps in white.", ["crafted", "soft"], "warm", card(G, "Light Trowel Marks", wall("trowel"), "Hand-made, still white.")),
    O("w_lime", "Lime Wash Clouds", "Soft cloudy lime wash.", ["natural", "soft"], "warm", card(G, "Lime Wash Clouds", wall("lime", "#FBF7F0"), "Breathes, tropical feel.")), "Trowel Or Lime Wash?")
def accentwall(c, where="living"):
    s = room(rect(120, 30, 106, 140, c, "none") + rect(130, 136, 80, 34, "#FFFFFF", "#E0DAD0", 6) + plant(214, 156, .7), WALL, OAK)
    return s
add(G, "Accent Wall Color", O("w_acc_clay", "Clay Plaster Accent", "One warm clay plaster wall in the living room.", ["earthy", "warm"], "warm", card(G, "Clay Plaster Accent", accentwall("#D59A76"), "Earthy, one wall only.")),
    O("w_acc_sea", "Sea Green Plaster Accent", "One soft sea green plaster wall.", ["lively", "tropical"], "lively", card(G, "Sea Green Plaster Accent", accentwall("#8DBFAF"), "Cool, tropical pop.")), "Clay Or Sea Green?")
add(G, "Accent Wall Amount", O("w_acc_one", "One Accent Wall Per Home", "Only the living room gets color.", ["calm", "clean"], "airy", card(G, "One Accent Wall Per Home", accentwall("#D59A76"), "Rest stays white.")),
    O("w_acc_none", "All White, Color In Things", "No accent walls; color comes from art, plants, textiles.", ["light", "lively"], "airy", card(G, "All White, Color In Things", room(rect(130, 136, 80, 34, "#FFFFFF", "#E0DAD0", 6) + rect(150, 60, 40, 50, "#FFFFFF", "#E0DAD0") + rect(156, 66, 28, 38, "#E9B44C") + rect(140, 132, 16, 12, ZEL, "none", 3) + rect(186, 132, 16, 12, CLAY, "none", 3) + plant(214, 156, .7)), "Art and pillows carry color.")), "One Wall Or None?")
def trim(kind):
    s = room(rect(80, 46, 80, 124, "#FFFFFF"), WALL, OAK, False)
    if kind == "flush": s += f'<rect x="80" y="46" width="80" height="124" fill="none" stroke="#E6E1D8"/>'
    else: s += rect(72, 40, 96, 130, "none", OAK, 0, 8)
    return s + rect(14, 166, 212, 6, "#FFFFFF" if kind == "flush" else OAK)
add(G, "Door Trim", O("w_trim_flush", "Flush White Trim", "Plain white trim that almost disappears.", ["clean", "simple"], "airy", card(G, "Flush White Trim", trim("flush"), "Current set.")),
    O("w_trim_oak", "Thin Oak Frames", "A thin oak frame around doors and the base.", ["warm", "natural"], "warm", card(G, "Thin Oak Frames", trim("oak"), "Wood lines the openings.")), "White Or Oak Trim?")
def ceiling(kind):
    s = rect(14, 30, 212, 196, WALL, "none", 10) + rect(14, 190, 212, 36, OAK)
    if kind == "battens": s += rect(14, 30, 212, 54, "#E7D3B3", "none", 10) + "".join(f'<line x1="{22+i*14}" y1="32" x2="{22+i*14}" y2="84" stroke="{TEAK}" stroke-width="2"/>' for i in range(15))
    else: s += rect(14, 30, 212, 54, "#FFFFFF", "none", 10) + f'<line x1="14" y1="84" x2="226" y2="84" stroke="#E0DAD0"/>'
    return s + rect(60, 150, 120, 40, "#FFFFFF", "#E0DAD0", 6) + plant(200, 186, .7)
add(G, "Living Room Ceiling", O("w_ceil_bat", "Timber Batten Ceiling", "Warm wood battens overhead.", ["warm", "natural"], "warm", card(G, "Timber Batten Ceiling", ceiling("battens"), "Warm, adds acoustic soak.")),
    O("w_ceil_white", "Plain White Ceiling", "Bright, bounces daylight.", ["light", "clean"], "airy", card(G, "Plain White Ceiling", ceiling("white"), "Brightest option.")), "Wood Or White Ceiling?")

# ---------------- Room Layouts ----------------
G = "Room Layouts"
def plan(rooms, label=None):
    s = rect(14, 30, 212, 196, "#FFFFFF", "none", 10) + rect(24, 40, 192, 176, "none", INK, 0, 2.2)
    for (x, y, w, h, n, c) in rooms:
        s += rect(24 + x, 40 + y, w, h, c, INK, 0, 1) + t(24 + x + w / 2, 40 + y + h / 2 + 3, n, 7, INK, "hind", 600, "middle")
    return s
add(G, "Studio / Office", O("l_studio_court", "Office Facing The Courtyard", "Desk looks into the green courtyard.", ["lively", "natural"], "lively", card(G, "Office Facing The Courtyard", plan([(0, 0, 112, 100, "Office", "#FFFFFF"), (112, 0, 80, 176, "Courtyard", "#E4EFD9"), (0, 100, 112, 76, "AV Closet", STONE)]), "Isolated Studio / Office.")),
    O("l_studio_garden", "Office With Its Own Garden", "Separate side garden, quieter.", ["calm", "natural"], "airy", card(G, "Office With Its Own Garden", plan([(0, 0, 192, 96, "Office", "#FFFFFF"), (0, 96, 120, 80, "Garden", "#E4EFD9"), (120, 96, 72, 80, "Bath", SOFT)]), "Isolated Studio / Office.")), "Courtyard View Or Own Garden?")
add(G, "Kids' Rooms", O("l_kids_split", "Two Rooms, Shared Bath Between", "Jack-and-Jill bath in the middle.", ["simple", "clear"], "airy", card(G, "Two Rooms, Shared Bath Between", plan([(0, 0, 80, 176, "Kids 1", "#FFFFFF"), (80, 0, 32, 176, "Bath", "#DCEBF2"), (112, 0, 80, 176, "Kids 2", "#FFFFFF")]), "Current plan.")),
    O("l_kids_bunk", "One Big Room Plus A Play Loft", "Kids share now; split with a wall later.", ["lively", "soft"], "lively", card(G, "One Big Room Plus A Play Loft", plan([(0, 0, 192, 110, "Shared Kids Room", "#FFFFFF"), (0, 110, 110, 66, "Play Loft", "#F6E7C8"), (110, 110, 82, 66, "Bath", "#DCEBF2")]), "Wall can go in later.")), "Two Rooms Or One Plus Loft?")
add(G, "Tatami Room", O("l_tatami_guest", "Tatami As Guest Room", "Futons out at night, open by day.", ["calm", "natural"], "warm", card(G, "Tatami As Guest Room", plan([(0, 0, 120, 176, "Tatami", "#EFE6C8"), (120, 0, 72, 90, "Closet", STONE), (120, 90, 72, 86, "Engawa", "#E4EFD9")]), "Sliding shoji doors.")),
    O("l_tatami_open", "Tatami Opens To Living", "Shoji slide open; it joins the living room.", ["light", "lively"], "airy", card(G, "Tatami Opens To Living", plan([(0, 0, 80, 176, "Tatami", "#EFE6C8"), (80, 0, 112, 176, "Living", "#FFFFFF")]), "One big room when open.")), "Guest Room Or Open To Living?")
add(G, "Living Room", O("l_pit", "Sunken Conversation Pit", "A step-down seating pit, current plan.", ["lively", "soft"], "lively", card(G, "Sunken Conversation Pit", plan([(0, 0, 192, 176, "", "#FFFFFF"), (40, 50, 112, 76, "Pit", "#F2E3CC")]), "Plan view.")),
    O("l_flat", "Flat Floor, Big Sectional", "Level floor, an L sofa you can move.", ["simple", "clear"], "airy", card(G, "Flat Floor, Big Sectional", plan([(0, 0, 192, 176, "", "#FFFFFF"), (30, 40, 110, 22, "Sofa", OAK), (30, 62, 22, 70, "", OAK)]), "Plan view.")), "Pit Or Flat Floor?")
add(G, "Mudroom", O("l_mud_lockers", "Cubbies Per Person", "One open cubby and hook set each.", ["clear", "lively"], "lively", card(G, "Cubbies Per Person", room("".join(rect(30 + i * 46, 50, 40, 120, "#FFFFFF", "#E0DAD0") + rect(30 + i * 46, 50, 40, 6, [ZEL, CLAY, "#E9B44C", LAGOON][i]) + dot(50 + i * 46, 80, 3, BRONZE) + rect(34 + i * 46, 140, 32, 26, OAK) for i in range(4)), WALL, STONE, False), "A color tag per person.")),
    O("l_mud_wall", "One Long Bench And Pegs", "A simple bench with a row of oak pegs.", ["simple", "natural"], "warm", card(G, "One Long Bench And Pegs", room(rect(30, 140, 180, 12, OAK) + "".join(dot(40 + i * 20, 80, 3.5, TEAK) for i in range(9)), WALL, STONE, False), "Open and quick.")), "Cubbies Or Bench?")
add(G, "Master Suite", O("l_ms_walk", "Closet Between Bed And Bath", "Walk through the closet to the bath.", ["clear", "simple"], "airy", card(G, "Closet Between Bed And Bath", plan([(0, 0, 192, 90, "Bedroom", "#FFFFFF"), (0, 90, 96, 86, "Closet", STONE), (96, 90, 96, 86, "Bath", "#DCEBF2")]), "Current plan.")),
    O("l_ms_garden", "Bath Opens To A Garden", "Bath gets a small walled garden shower.", ["tropical", "lively"], "lively", card(G, "Bath Opens To A Garden", plan([(0, 0, 192, 90, "Bedroom", "#FFFFFF"), (0, 90, 70, 86, "Closet", STONE), (70, 90, 70, 86, "Bath", "#DCEBF2"), (140, 90, 52, 86, "Garden", "#E4EFD9")]), "Outdoor shower.")), "Closet Walk-Through Or Bath Garden?")
add(G, "Wellness Wing", O("l_well_line", "Sauna, Steam, Wet Room In A Row", "One straight line, short walk.", ["clear", "simple"], "airy", card(G, "Sauna, Steam, Wet Room In A Row", plan([(0, 0, 64, 90, "Sauna", "#F2E3CC"), (64, 0, 64, 90, "Steam", "#DCEBF2"), (128, 0, 64, 90, "Wet", "#E9F2F5"), (0, 90, 192, 86, "Exercise", "#FFFFFF")]), "Current rooms.")),
    O("l_well_court", "Around A Cold Plunge Court", "Rooms ring a small open-air plunge.", ["tropical", "lively"], "lively", card(G, "Around A Cold Plunge Court", plan([(0, 0, 192, 50, "Exercise", "#FFFFFF"), (0, 50, 60, 126, "Sauna", "#F2E3CC"), (60, 50, 72, 126, "Plunge Court", "#CFE6E6"), (132, 50, 60, 126, "Steam", "#DCEBF2")]), "Open sky in the middle.")), "In A Row Or Around A Court?")

# ---------------- Lighting ----------------
G = "Lighting"
def lit(kind):
    s = room(rect(60, 150, 120, 26, "#FFFFFF", "#E0DAD0", 6), WALL, OAK)
    if kind == "pendant": s += f'<line x1="150" y1="30" x2="150" y2="70" stroke="{MUTE}"/><path d="M134 82 Q150 62 166 82 Z" fill="#E9D3A8"/>' + f'<path d="M136 82 L120 150 H180 L164 82 Z" fill="#FFF4D6" opacity=".6"/>'
    elif kind == "cove": s += rect(14, 30, 212, 8, "#FFF4D6") + f'<path d="M14 38 H226 V70 H14 Z" fill="#FFF4D6" opacity=".45"/>'
    elif kind == "can": s += "".join(dot(60 + i * 40, 36, 4, "#FFF4D6") + f'<path d="M{56+i*40} 38 L{48+i*40} 150 H{72+i*40} L{64+i*40} 38 Z" fill="#FFF4D6" opacity=".35"/>' for i in range(4))
    elif kind == "lamp": s += f'<line x1="200" y1="176" x2="200" y2="110" stroke="{BRONZE}" stroke-width="2"/><path d="M188 110 L212 110 L206 92 L194 92 Z" fill="#F2E6CF"/>' + dot(200, 104, 14, "#FFF4D6")
    elif kind == "rattan": s += f'<line x1="150" y1="30" x2="150" y2="60" stroke="{MUTE}"/><ellipse cx="150" cy="78" rx="22" ry="18" fill="#E2C38F"/>' + "".join(f'<line x1="{132+i*6}" y1="64" x2="{132+i*6}" y2="92" stroke="{TEAK}" stroke-width=".8"/>' for i in range(7))
    else: s += rect(130, 58, 40, 6, "#FFFFFF", STEEL, 2) + f'<path d="M132 64 L118 150 H182 L168 64 Z" fill="#FFF4D6" opacity=".5"/>'
    return s
add(G, "Dining Light", O("lt_pendant", "Linen Drum Pendant", "One soft pendant over the table.", ["soft", "warm"], "warm", card(G, "Linen Drum Pendant", lit("pendant"), "Warm 2700K.")),
    O("lt_rattan", "Rattan Globe Pendant", "Woven rattan globe; tropical.", ["tropical", "natural"], "warm", card(G, "Rattan Globe Pendant", lit("rattan"), "Patterned shadows.")), "Linen Or Rattan?")
add(G, "Ceiling Light", O("lt_cove", "Hidden Cove Glow", "Light bounces off the ceiling edge.", ["soft", "calm"], "airy", card(G, "Hidden Cove Glow", lit("cove"), "No visible fixtures.")),
    O("lt_can", "Small Recessed Cans", "A grid of small round downlights.", ["clear", "simple"], "airy", card(G, "Small Recessed Cans", lit("can"), "Even, bright light.")), "Cove Or Cans?")
add(G, "Reading Light", O("lt_floor", "Floor Lamp By The Chair", "A bronze floor lamp you can move.", ["warm", "soft"], "warm", card(G, "Floor Lamp By The Chair", lit("lamp"), "Moves with the chair.")),
    O("lt_wash", "Wall Wash Spot", "A fixed spot over the reading chair.", ["clean", "clear"], "airy", card(G, "Wall Wash Spot", lit("spot"), "Fewer cords.")), "Floor Lamp Or Fixed Spot?")
def daylight(kind):
    s = rect(14, 30, 212, 196, WALL, "none", 10) + rect(14, 186, 212, 40, OAK)
    if kind == "sky": s += rect(90, 30, 60, 14, SKY) + f'<path d="M90 44 L70 186 H170 L150 44 Z" fill="#FFF9E6" opacity=".8"/>'
    else: s += rect(30, 60, 180, 100, SKY, "#FFFFFF", 0, 4) + f'<line x1="120" y1="60" x2="120" y2="160" stroke="#FFFFFF" stroke-width="3"/>' + f'<path d="M36 156 q20 -40 40 -6 q20 -50 50 0 q20 -30 46 4 V156 Z" fill="{SAGE}"/>'
    return s
add(G, "Hallway Daylight", O("lt_sky", "Skylight Strip In The Hall", "A slot of sky down the hallway.", ["light", "clear"], "airy", card(G, "Skylight Strip In The Hall", daylight("sky"), "Sun all day.")),
    O("lt_glazed", "Glass Wall To The Engawa", "Low glass wall onto the gallery and garden.", ["tropical", "lively"], "lively", card(G, "Glass Wall To The Engawa", daylight("glass"), "Green view the whole way.")), "Skylight Or Glass Wall?")
def path(kind):
    s = rect(14, 30, 212, 196, "#F1ECE3", "none", 10) + f'<path d="M100 226 L120 60 L140 226 Z" fill="{STONE}"/>' + "".join(plant(40 + (i % 2) * 160, 120 + (i // 2) * 50, .6) for i in range(4))
    if kind == "bollard": s += "".join(rect(88 + (i % 2) * 58, 90 + (i // 2) * 44, 6, 18, "#FFFFFF", STEEL) + dot(91 + (i % 2) * 58, 92 + (i // 2) * 44, 5, "#FFF4D6") for i in range(6))
    else: s += "".join(dot(104 + (i % 2) * 32 - i * 1.2, 80 + i * 22, 3, "#FFE7A8") for i in range(7))
    return s
add(G, "Garden Path Light", O("lt_bollard", "Short White Bollards", "Small posts along the path.", ["clear", "simple"], "airy", card(G, "Short White Bollards", path("bollard"), "Clear edges at night.")),
    O("lt_step", "Lights Set In The Path", "Tiny lights set flush in the stones.", ["soft", "natural"], "warm", card(G, "Lights Set In The Path", path("step"), "Nothing sticks up.")), "Bollards Or In-Path?")

# ---------------- Storage And Gear ----------------
G = "Storage And Gear"
def gear(kind):
    s = room("", WALL, STONE, False)
    if kind == "wall": s += rect(30, 46, 180, 110, "#FFFFFF", "#E0DAD0") + "".join(f'<line x1="{40+i*20}" y1="54" x2="{40+i*20}" y2="148" stroke="{LINE}"/>' for i in range(9)) + rect(46, 70, 14, 60, ZEL, "none", 4) + rect(76, 60, 30, 30, CLAY, "none", 15) + rect(120, 64, 50, 10, LAGOON, "none", 3) + rect(180, 66, 18, 70, "#E9B44C", "none", 3)
    else: s += "".join(rect(30 + i * 62, 50, 56, 120, "#FFFFFF", "#E0DAD0") + t(58 + i * 62, 112, n, 7, MUTE, "hind", 600, "middle") for i, n in enumerate(["Sport", "Beach", "Tools"]))
    return s
add(G, "Gear Wall", O("g_peg", "Open Peg Wall For Gear", "Boards, rackets and bags hang in view.", ["visual", "lively"], "lively", card(G, "Open Peg Wall For Gear", gear("wall"), "Mudroom + Gear.")),
    O("g_closed", "Labeled White Cabinets", "Gear sorted behind three doors.", ["clean", "calm"], "airy", card(G, "Labeled White Cabinets", gear("closed"), "Mudroom + Gear.")), "Peg Wall Or Cabinets?")
def closet(kind):
    s = room("", WALL, OAK, False)
    if kind == "open": s += rect(30, 50, 180, 4, OAK) + "".join(f'<path d="M{40+i*14} 54 v6 l-6 30 h12 l-6 -30" fill="{["#FFFFFF","#E9DCC6",ZEL,"#F3EEE5",CLAY][i%5]}" stroke="#D9D3C9"/>' for i in range(12)) + rect(30, 130, 180, 40, OAK)
    else: s += "".join(rect(30 + i * 45, 46, 44, 124, "#FFFFFF", "#E6E1D8") for i in range(4))
    return s
add(G, "Master Closet", O("g_cl_open", "Open Rails And Oak Drawers", "Clothes on view, like a small shop.", ["visual", "warm"], "warm", card(G, "Open Rails And Oak Drawers", closet("open"), "Easy to see it all.")),
    O("g_cl_flush", "Flush White Doors", "Handleless doors floor to ceiling.", ["clean", "calm"], "airy", card(G, "Flush White Doors", closet("flush"), "Matches the kitchen.")), "Open Or Flush Closet?")
add(G, "Toy Storage", O("g_toy_bins", "Low Shelves With Color Bins", "Kids reach every bin.", ["lively", "soft"], "lively", card(G, "Low Shelves With Color Bins", room("".join(rect(34 + (i % 4) * 44, 110 + (i // 4) * 30, 40, 26, [ZEL, CLAY, "#E9B44C", LAGOON][i % 4], "none", 3) for i in range(8)) + rect(30, 106, 180, 64, "none", OAK, 2, 3), WALL, OAK), "Kids' rooms.")),
    O("g_toy_bench", "Window Bench With Lift Lids", "Toys hide under a window seat.", ["calm", "soft"], "warm", card(G, "Window Bench With Lift Lids", room(rect(24, 126, 120, 40, OAK) + rect(24, 120, 120, 8, "#FFFFFF", "#E0DAD0", 3)), "Doubles as reading nook.")), "Bins Or Bench?")
add(G, "Laundry", O("g_lau_stack", "Stacked Machines, Folding Counter", "Washer and dryer stacked, long counter.", ["clear", "simple"], "airy", card(G, "Stacked Machines, Folding Counter", room(rect(160, 46, 50, 124, "#FFFFFF", "#D9D3C9") + dot(185, 76, 14, "#E9F2F5") + dot(185, 136, 14, "#E9F2F5") + rect(24, 120, 130, 8, OAK), WALL, STONE, False), "More counter.")),
    O("g_lau_side", "Side By Side Under A Counter", "Machines side by side, counter on top.", ["simple", "clean"], "airy", card(G, "Side By Side Under A Counter", room(rect(30, 126, 180, 8, OAK) + dot(70, 152, 14, "#E9F2F5") + rect(48, 134, 44, 40, "none", "#D9D3C9") + dot(128, 152, 14, "#E9F2F5") + rect(106, 134, 44, 40, "none", "#D9D3C9"), WALL, STONE, False), "Fold right on top.")), "Stacked Or Side By Side?")
def shoes(kind):
    s = room("", WALL, STONE, False)
    if kind == "bench": s += rect(30, 130, 180, 12, OAK) + "".join(rect(40 + i * 22, 150, 16, 8, ["#FFFFFF", CLAY, "#E9DCC6", ZEL][i % 4], "none", 3) for i in range(8))
    else: s += rect(40, 46, 160, 124, "#FFFFFF", "#E6E1D8") + rect(40, 112, 160, 10, OAK)
    return s
add(G, "Genkan Shoes", O("g_sh_bench", "Bench With Shoes Below", "Sit, shoes off, shoes under the bench.", ["warm", "simple"], "warm", card(G, "Bench With Shoes Below", shoes("bench"), "Entry Genkan.")),
    O("g_sh_tall", "Tall Shoe Cabinet With A Niche", "Closed cabinet and a small display shelf.", ["clean", "calm"], "airy", card(G, "Tall Shoe Cabinet With A Niche", shoes("tall"), "Coat + Shoe Closet.")), "Bench Or Tall Cabinet?")

# ---------------- Outdoor Space ----------------
G = "Outdoor Space"
def court(kind):
    s = rect(14, 30, 212, 196, "#F4F0E8", "none", 10)
    if kind == "lawn": s += rect(40, 56, 160, 144, "#BFD7A5", "none", 6) + f'<circle cx="120" cy="128" r="26" fill="{LEAF}"/>'
    elif kind == "water": s += rect(40, 56, 160, 144, STONE, "none", 6) + rect(70, 90, 100, 76, "#BFE0E3", "none", 4) + plant(60, 190, .6) + plant(180, 190, .6)
    elif kind == "herb": s += "".join(rect(40 + (i % 3) * 56, 60 + (i // 3) * 70, 48, 60, "#D9C6A8", "none", 3) + "".join(dot(48 + (i % 3) * 56 + k * 8, 90 + (i // 3) * 70, 4, LEAF) for k in range(5)) for i in range(6))
    else: s += rect(40, 56, 160, 144, "#FFFFFF", "none", 6) + "".join(plant(60 + i * 30, 190, .7) for i in range(5)) + rect(80, 90, 80, 50, TEAK, "none", 4)
    return s + rect(14, 30, 212, 196, "none", INK, 10, 1.5)
add(G, "Courtyard Center", O("o_lawn_tree", "Lawn With One Shade Tree", "Soft grass and a single big tree.", ["natural", "soft"], "airy", card(G, "Lawn With One Shade Tree", court("lawn"), "Plan view.")),
    O("o_pool_stone", "Reflecting Pool On Stone", "A shallow pool, pale stone round it.", ["clear", "tropical"], "lively", card(G, "Reflecting Pool On Stone", court("water"), "Cools the air.")), "Lawn Or Reflecting Pool?")
add(G, "Kitchen Garden", O("o_beds", "Six Raised Herb Beds", "Raised beds near the kitchen.", ["natural", "lively"], "lively", card(G, "Six Raised Herb Beds", court("herb"), "Next to the chicken run.")),
    O("o_deck", "Teak Deck Ringed With Pots", "A deck for meals, herbs in big pots.", ["warm", "simple"], "warm", card(G, "Teak Deck Ringed With Pots", court("deck"), "Less weeding.")), "Raised Beds Or Deck With Pots?")
def engawa(kind):
    s = rect(14, 30, 212, 196, SKY, "none", 10) + rect(14, 150, 212, 76, "#BFD7A5", "none", 0) + rect(14, 216, 212, 10, "#BFD7A5", "none", 10)
    s += rect(14, 60, 212, 12, TEAK) + rect(14, 140, 212, 14, OAK) + "".join(rect(24 + i * 50, 72, 6, 68, TEAK) for i in range(5))
    if kind == "hammock": s += f'<path d="M80 96 Q105 132 130 96" fill="none" stroke="#E9B44C" stroke-width="6"/>'
    else: s += rect(80, 122, 70, 18, "#FFFFFF", "#E0DAD0", 5) + rect(84, 112, 62, 12, CLAY, "none", 4)
    return s
add(G, "Engawa Gallery", O("o_eng_hammock", "Hammock Between Posts", "A woven hammock on the gallery.", ["tropical", "lively"], "lively", card(G, "Hammock Between Posts", engawa("hammock"), "East Engawa Gallery.")),
    O("o_eng_daybed", "Low Daybed With Cushions", "A long low daybed for naps.", ["soft", "warm"], "warm", card(G, "Low Daybed With Cushions", engawa("daybed"), "East Engawa Gallery.")), "Hammock Or Daybed?")
def pav(kind):
    s = rect(14, 30, 212, 196, SKY, "none", 10) + rect(14, 180, 212, 46, "#BFD7A5", "none", 0) + rect(14, 216, 212, 10, "#BFD7A5", "none", 10)
    if kind == "net": s += f'<path d="M50 180 L120 70 L190 180" fill="none" stroke="{TEAK}" stroke-width="5"/>' + "".join(f'<line x1="{60+i*12}" y1="{180-i*16}" x2="{180-i*12}" y2="{180-i*16}" stroke="#E9B44C" stroke-width="1.5"/>' for i in range(6))
    else: s += rect(60, 80, 120, 8, TEAK) + rect(64, 88, 6, 92, TEAK) + rect(170, 88, 6, 92, TEAK) + "".join(rect(80 + i * 22, 120, 10, 60, [ZEL, CLAY, "#E9B44C", LAGOON][i], "none", 3) for i in range(4))
    return s
add(G, "Climbing Pavilion", O("o_pav_net", "Rope Net Climbing Frame", "A teak A-frame with a rope net.", ["lively", "natural"], "lively", card(G, "Rope Net Climbing Frame", pav("net"), "Grows with older kids.")),
    O("o_pav_wall", "Low Boulder Wall Under A Roof", "Short colored holds under a shade roof.", ["lively", "simple"], "lively", card(G, "Low Boulder Wall Under A Roof", pav("wall"), "Safe for small kids.")), "Net Or Boulder Wall?")
def shade(kind):
    s = rect(14, 30, 212, 196, SKY, "none", 10) + rect(14, 170, 212, 56, STONE, "none", 0) + rect(14, 216, 212, 10, STONE, "none", 10)
    if kind == "sail": s += f'<path d="M40 70 L200 50 L170 120 Z" fill="#FFFFFF" stroke="#E0DAD0"/>'
    else: s += "".join(rect(40 + i * 16, 70, 10, 6, TEAK) for i in range(10)) + rect(40, 76, 160, 4, OAK) + "".join(dot(48 + i * 32, 80, 6, LEAF) for i in range(5))
    return s + rect(70, 140, 100, 12, TEAK, "none", 3) + rect(76, 152, 6, 18, TEAK) + rect(158, 152, 6, 18, TEAK)
add(G, "Courtyard Shade", O("o_sail", "White Shade Sail", "A light sail, easy to take down.", ["light", "clear"], "airy", card(G, "White Shade Sail", shade("sail"), "Over the courtyard table.")),
    O("o_pergola", "Teak Pergola With Vines", "Slatted pergola, vines grow over.", ["natural", "tropical"], "warm", card(G, "Teak Pergola With Vines", shade("pergola"), "Shade grows in.")), "Sail Or Pergola?")

# ---------------- Plans And Docs ----------------
G = "Plans And Docs"
def sheet(style):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    if style == "line": s += rect(28, 44, 140, 150, "none", INK, 0, 1.6) + rect(28, 44, 70, 70, "none", INK) + rect(98, 114, 70, 80, "none", INK) + rect(174, 44, 40, 150, "none", LINE) + "".join(ln(56 + i * 10, 178, 210) for i in range(6))
    elif style == "color": s += rect(28, 44, 70, 70, "#FFFFFF", INK) + rect(98, 44, 70, 70, "#E4EFD9", INK) + rect(28, 114, 70, 80, "#DCEBF2", INK) + rect(98, 114, 70, 80, "#F2E3CC", INK) + rect(174, 44, 40, 150, "none", LINE) + "".join(dot(182, 60 + i * 14, 4, c) for i, c in enumerate(["#E4EFD9", "#DCEBF2", "#F2E3CC"]))
    elif style == "render": s += rect(28, 44, 186, 100, "#F3ECE1") + rect(28, 120, 186, 24, OAK) + rect(40, 56, 50, 50, SKY, "#FFFFFF", 0, 2) + rect(120, 96, 70, 24, "#FFFFFF", "#E0DAD0", 4) + "".join(ln(156 + i * 10, 28, 214) for i in range(4))
    elif style == "cards": s += "".join(rect(28 + (i % 2) * 96, 44 + (i // 2) * 52, 90, 46, "#FFFFFF", LINE, 6) + rect(28 + (i % 2) * 96, 44 + (i // 2) * 52, 4, 46, [ZEL, CLAY, LAGOON, "#E9B44C", ZEL, CLAY][i]) + t(38 + (i % 2) * 96, 64 + (i // 2) * 52, ["Kitchen", "Bath", "Living", "Office", "Kids", "Outdoor"][i], 9, INK, "khand") for i in range(6))
    else: s += "".join(ln(52 + i * 14, 28, 214) for i in range(10)) + t(28, 48, "Room Schedule", 9, INK, "khand")
    return s
add(G, "Floor Plan Style", O("d_line", "Clean Black Line Plan", "Crisp lines, no fill.", ["clear", "simple"], "airy", card(G, "Clean Black Line Plan", sheet("line"), "Classic drawing set.")),
    O("d_color", "Soft Color-Coded Rooms", "Rooms tinted by use, with a key.", ["visual", "lively"], "lively", card(G, "Soft Color-Coded Rooms", sheet("color"), "Read it at a glance.")), "Line Plan Or Color Rooms?")
add(G, "Design Doc Lead", O("d_render", "Lead With A Drawn View", "Each page opens with a room sketch.", ["visual", "warm"], "warm", card(G, "Lead With A Drawn View", sheet("render"), "Picture first, then specs.")),
    O("d_table", "Lead With The Spec Table", "Page opens with sizes and finishes.", ["clear", "simple"], "airy", card(G, "Lead With The Spec Table", sheet("table"), "Facts first.")), "Picture Or Table First?")
add(G, "Project Overview", O("d_cards", "Room Cards With Color Tabs", "One card per room, a color tab each.", ["visual", "lively"], "lively", card(G, "Room Cards With Color Tabs", sheet("cards"), "Tap a card for details.")),
    O("d_list", "Simple Room List", "One line per room with status.", ["clear", "simple"], "airy", card(G, "Simple Room List", sheet("table"), "Fast to scan.")), "Cards Or List?")
def bom(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    rows = [("Dining Table", OAK), ("Pendant", "#E9D3A8"), ("Stools x4", TEAK), ("Rug", CLAY)]
    for i, (n, c) in enumerate(rows):
        y = 44 + i * 44
        if kind == "pics": s += rect(26, y, 36, 36, c, "none", 4) + t(70, y + 16, n, 10, INK, "khand") + t(70, y + 30, "Picked · In Plan", 7, ZEL, "hind", 600)
        else: s += t(26, y + 20, n, 9, INK) + t(214, y + 20, "Picked", 7, MUTE, "hind", 600, "end") + ln(y + 30, 26, 214)
    return s
add(G, "Furniture List", O("d_bom_pics", "Furniture List With Swatches", "Each item shows a color swatch.", ["visual", "warm"], "warm", card(G, "Furniture List With Swatches", bom("pics"), "Gear and furniture plan.")),
    O("d_bom_text", "Plain Text Furniture List", "Names and status only.", ["clear", "simple"], "airy", card(G, "Plain Text Furniture List", bom("text"), "Gear and furniture plan.")), "Swatches Or Plain List?")
def mood(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    if kind == "board": s += rect(26, 42, 100, 90, "#F3ECE1") + rect(132, 42, 82, 44, ZEL) + rect(132, 90, 82, 42, OAK) + rect(26, 138, 60, 76, "#D59A76") + rect(92, 138, 122, 76, SKY)
    else: s += "".join(dot(50 + i * 36, 90, 16, c) for i, c in enumerate(["#FFFFFF", OAK, ZEL, CLAY, SKY])) + "".join(f'<circle cx="{50+i*36}" cy="90" r="16" fill="none" stroke="#E0DAD0"/>' for i in range(5)) + "".join(ln(140 + i * 14, 26, 214) for i in range(5))
    return s
add(G, "Finish Board", O("d_mood", "Collage Mood Board", "Overlapping blocks of each finish.", ["visual", "lively"], "lively", card(G, "Collage Mood Board", mood("board"), "Feel of the room.")),
    O("d_dots", "Swatch Dots And Notes", "A row of swatch dots with short notes.", ["clear", "light"], "airy", card(G, "Swatch Dots And Notes", mood("dots"), "Tidy and exact.")), "Collage Or Swatch Row?")

def sketch(kind):
    s = rect(14, 30, 212, 196, "#FFFDF8" if kind == "hand" else "#FFFFFF", "#D6D0C6", 2)
    if kind == "hand": s += f'<path d="M30 190 L32 60 L120 58 L122 120 L210 122 L208 192 Z" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>' + f'<path d="M60 90 q10 -8 20 0" fill="none" stroke="{CLAY}" stroke-width="2"/>' + plant(170, 170, .6)
    else: s += f'<path d="M30 190 V60 H120 V120 H210 V190 Z" fill="none" stroke="{INK}" stroke-width="1.4"/>' + "".join(f'<line x1="{30+i*20}" y1="200" x2="{30+i*20}" y2="206" stroke="{MUTE}"/>' for i in range(10)) + t(120, 216, "Scale 1:100", 7, MUTE, anchor="middle")
    return s
add(G, "Concept Sketch Style", O("d_hand", "Hand-Drawn Concept Sketch", "Loose pen lines with a color touch.", ["warm", "crafted"], "warm", card(G, "Hand-Drawn Concept Sketch", sketch("hand"), "Early ideas feel open.")),
    O("d_cad", "Crisp Scaled Drawing", "Straight lines with a scale bar.", ["clear", "simple"], "airy", card(G, "Crisp Scaled Drawing", sketch("cad"), "Ready to measure.")), "Sketch Or Scaled Drawing?")

finish(DID, "Blueprint Round 1: Weberman Residence Open Decisions, Kitchen Calls, Walls And Plaster, Room Layouts, Lighting, Storage, Outdoor Space, Plans And Docs", "Blueprint", pairs, 0,
       {"brands": ["Blueprint: Max's architecture and interior design agent (Weberman Residence)", "White base, Khand/Hind, small pops of real color (zellige green, clay, lagoon, saffron); earthy ok; no neon, pastel, dark rooms, luxe or ornate"],
        "feelings": {"airy": "Light and clean", "warm": "Warm and natural", "lively": "Lively color pop"},
        "sources": {"open_items": "/workspace/dreamhome/v2/design/plan.json (openItems, rooms)", "kitchen": "/workspace/dreamhome/v2/design/kitchen_round1.md",
                    "status": "/workspace/ops/team-sync/2026-10-13.md (Blueprint section)", "brief": "/workspace/ops/briefs/2026-10-13.md", "feed": "/workspace/ops/team-feed.md"}}, seed=11)
# publish: clear the draft flags set by draft_svg.finish
d = json.load(open(f"decks/{DID}.json")); d.pop("draft", None); d["status"] = "published"
for pp in d["pairs"]:
    for k in "AB": o = pp["option" + k]; o["tags"] = list(dict.fromkeys(o["tags"]))
json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
