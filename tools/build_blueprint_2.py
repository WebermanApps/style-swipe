#!/usr/bin/env python3
"""Build Style Swipe deck blueprint-2 (PUBLISHED): 25 Blueprint pairs built on Max's blueprint-1 results
(results/blueprint-1.txt, 42/50; top tags airy, simple, natural, lively, clean). Mix: lean into his A/B picks (refine the
winner), resolve his 'both' answers (where does each go / combine), re-ask the 8 skipped pairs in fresh forms, and add new
open Blueprint decisions. Reuses the blueprint-1 drawing helpers + tools/draft_svg.py. Run from the style-swipe repo root."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draft_svg import *
src = open(os.path.join(os.path.dirname(__file__), "build_blueprint_1.py")).read().split("\nfinish(")[0]
exec(compile(src, "bp1_helpers", "exec"))  # brings room/card/door/... helpers (its own pairs list is discarded)
DID = "blueprint-2"
pairs, O, add = mk("bp2_", "Blueprint")
def A(i, lab, desc, tags, feel, g, art, cap): return O(i, lab, desc, tags, feel, card(g, lab, art, cap))
def P(g, cat, a, b, ask, purpose="refine"): add(g, cat, a, b, ask, purpose)

# ---------- Building On Your Picks (A/B winners from blueprint-1) ----------
G = "Building On Your Picks"
half = lambda c: room(rect(120, 110, 106, 60, c) + rect(130, 136, 80, 34, "#FFFFFF", "#E0DAD0", 6) + plant(214, 156, .7))
P(G, "Clay Accent Size", A("clay_full", "Clay Wall, Floor To Ceiling", "Your clay pick as one full wall.", ["warm", "lively"], "warm", G, accentwall(CLAY), "Picked: clay over sea green."),
  A("clay_half", "Clay Lower Half, White Above", "Clay wainscot height, white plaster above.", ["light", "airy"], "airy", G, half(CLAY), "A smaller pop of clay."), "Full Wall Or Half Height?")
def lever(plate):
    s = handle("lever")
    return s + (rect(138, 96, 16, 34, "none", BRONZE, 3, 1.5) if plate else "")
P(G, "Lever Detail", A("lever_rose", "Lever On A Small Round Rose", "Your slim bronze lever, tiny round base.", ["simple", "clean"], "airy", G, handle("lever"), "Picked: lever over knob."),
  A("lever_plate", "Lever On A Tall Back Plate", "Same lever on a slim bronze plate.", ["crafted", "warm"], "warm", G, lever(True), "A bit more metal."), "Round Rose Or Back Plate?")
P(G, "Trowel Tone", A("trowel_white", "Trowel Marks On Bright White", "Your trowel finish in pure white.", ["clean", "airy"], "airy", G, wall("trowel"), "Picked: trowel over lime wash."),
  A("trowel_warm", "Trowel Marks On Warm White", "Same trowel finish, a touch of cream.", ["warm", "natural"], "warm", G, wall("trowel", "#FBF4E8"), "Softer in evening light."), "Bright Or Warm White?")
P(G, "Teak Door Light", A("plank_solid", "Teak Planks, No Glass", "Your plank door, solid.", ["warm", "natural"], "warm", G, door("plank", TEAK), "Picked: teak planks."),
  A("plank_side", "Teak Planks Plus A Glass Sidelight", "A slim glass strip beside the door.", ["light", "airy"], "airy", G, door("plank", TEAK) + rect(154, 54, 16, 116, SKY, "#FFFFFF", 1, 2), "Daylight without glass in the door."), "Solid Or With A Sidelight?")
R = lambda *r: plan(list(r))
P(G, "Tatami Guest Door", A("tat_shoji", "Shoji Slider To The Hall", "Guest tatami closes with paper sliders.", ["light", "natural"], "airy", G, R((0, 0, 96, 90, "Tatami", "#EFE6D2"), (96, 0, 96, 90, "Living", "#FFFFFF"), (0, 90, 192, 86, "Hall", "#F5F3EF")) + rect(24, 128, 96, 4, "#E9D3A8"), "Picked: tatami as guest room."),
  A("tat_wall", "Solid Wall And A Swing Door", "A quieter, closed guest room.", ["calm", "simple"], "warm", G, R((0, 0, 96, 90, "Tatami", "#EFE6D2"), (96, 0, 96, 90, "Living", "#FFFFFF"), (0, 90, 192, 86, "Hall", "#F5F3EF")) + rect(24, 128, 96, 4, INK), "More privacy for guests."), "Shoji Or Solid Wall?")
P(G, "Closet Walk-Through", A("walk_straight", "Straight Walk-Through Closet", "Bed, closet, bath in one line.", ["simple", "clean"], "airy", G, R((0, 0, 70, 176, "Bed", "#FFFFFF"), (70, 0, 52, 176, "Closet", "#F2E3CC"), (122, 0, 70, 176, "Bath", "#DCEBF2")), "Picked: closet between bed and bath."),
  A("walk_l", "L-Shaped Closet Around A Corner", "Closet wraps a corner on the way to bath.", ["natural", "calm"], "warm", G, R((0, 0, 110, 110, "Bed", "#FFFFFF"), (110, 0, 82, 110, "Closet", "#F2E3CC"), (0, 110, 192, 66, "Bath", "#DCEBF2")), "More hanging length."), "Straight Or L-Shaped?")
def trim2(gap):
    s = trim("flush"); return s + (f'<rect x="78" y="44" width="84" height="128" fill="none" stroke="#CFC8BC" stroke-width="1.5"/>' if gap else "")
P(G, "Flush Trim Detail", A("trim_plain", "Flush White, No Line", "Your flush trim, fully hidden.", ["clean", "simple"], "airy", G, trim("flush"), "Picked: flush white trim."),
  A("trim_gap", "Flush White With A Shadow Gap", "A thin recessed line around each door.", ["crafted", "clean"], "airy", G, trim2(True), "A crisp edge, still white."), "Plain Or Shadow Gap?")
def stools(n, back):
    s = rect(14, 30, 212, 196, "#FFFFFF", LINE, 10) + rect(50, 90, 140, 50, OAK, "none", 3)
    for i in range(n):
        x = 66 + i * (108 / max(n - 1, 1)); s += dot(x, 158, 9, "#FFFFFF") + f'<circle cx="{x}" cy="158" r="9" fill="none" stroke="{TEAK}" stroke-width="1.6"/>' + (rect(x - 9, 168, 18, 4, TEAK) if back else "")
    return s
P(G, "Island Stools", A("stool_four", "Four Backless Oak Stools", "Your stool pick, tuck fully under.", ["simple", "clean"], "airy", G, stools(4, False), "Picked: stools along the island."),
  A("stool_three", "Three Stools With Low Backs", "Fewer, comfier seats.", ["warm", "natural"], "warm", G, stools(3, True), "Better for long talks."), "Four Backless Or Three With Backs?")
def beds(n):
    s = rect(14, 30, 212, 196, "#F4F0E8", "none", 10)
    for i in range(n): s += rect(34 + (i % 3) * 60, 52 + (i // 3) * 76, 50, 62, "#D9C6A8", "none", 3) + "".join(dot(42 + (i % 3) * 60 + k * 8, 84 + (i // 3) * 76, 4, LEAF) for k in range(5))
    if n == 4: s += rect(154, 60, 52, 14, TEAK, "none", 3)
    return s
P(G, "Herb Beds", A("beds_six", "Six Raised Beds In A Grid", "Your raised beds, full grid.", ["natural", "lively"], "lively", G, beds(6), "Picked: raised herb beds."),
  A("beds_four", "Four Beds And A Teak Bench", "Fewer beds, a seat to sit among them.", ["calm", "natural"], "warm", G, beds(4), "Room to sit."), "Six Beds Or Four Plus A Bench?")
def vanity2(c):
    return vanity("deck").replace(f'stroke="{STEEL}" stroke-width="4"', f'stroke="{c}" stroke-width="4"')
P(G, "Deck Faucet Finish", A("dfauc_steel", "Deck Faucet In Brushed Steel", "Your deck-mount pick in steel.", ["clean", "simple"], "airy", G, vanity2(STEEL), "Picked: deck-mount."),
  A("dfauc_bronze", "Deck Faucet In Warm Bronze", "Matches the bronze kitchen faucet.", ["warm", "crafted"], "warm", G, vanity2(BRONZE), "Picked bronze in the kitchen."), "Steel Or Bronze?")
def tree(c, r):
    return court("lawn").replace(f'<circle cx="120" cy="128" r="26" fill="{LEAF}"/>', f'<circle cx="120" cy="128" r="{r}" fill="{c}"/>')
P(G, "Courtyard Tree", A("tree_maple", "Japanese Maple In The Lawn", "Red-leaf maple as the one tree.", ["lively", "natural"], "lively", G, tree("#C1502E", 24), "Picked: lawn with one shade tree."),
  A("tree_olive", "Silvery Olive Tree", "Soft grey-green, light shade.", ["airy", "calm"], "airy", G, tree("#9FB59A", 30), "Calm all year."), "Maple Or Olive?")
def laundry(extra):
    s = room(rect(40, 50, 44, 120, "#FFFFFF", "#E0DAD0") + dot(62, 80, 12, "#EEF4F6") + dot(62, 136, 12, "#EEF4F6") + rect(84, 110, 130, 8, OAK), WALL, STONE, False)
    if extra == "rack": s += "".join(f'<line x1="{100+i*14}" y1="56" x2="{100+i*14}" y2="96" stroke="{TEAK}" stroke-width="2"/>' for i in range(8)) + rect(96, 52, 112, 4, TEAK)
    else: s += rect(150, 100, 50, 12, "#FFFFFF", "#CFC8BC", 5) + f'<path d="M172 100 V88 H182" fill="none" stroke="{STEEL}" stroke-width="3"/>'
    return s
P(G, "Laundry Extra", A("lau_rack", "Stacked Plus A Ceiling Drying Rack", "Fold counter with a pull-down rack.", ["natural", "simple"], "airy", G, laundry("rack"), "Picked: stacked with folding counter."),
  A("lau_sink", "Stacked Plus A Deep Utility Sink", "A sink set into the folding counter.", ["clean", "simple"], "airy", G, laundry("sink"), "Rinse muddy gear."), "Drying Rack Or Utility Sink?")
P(G, "Pergola Color", A("perg_teak", "Teak Pergola, Climbing Jasmine", "Your pergola pick in warm teak.", ["warm", "natural"], "warm", G, shade("pergola"), "Picked: pergola over sail."),
  A("perg_white", "White Pergola, Climbing Jasmine", "Same frame painted white.", ["airy", "clean"], "airy", G, shade("pergola").replace(TEAK, "#FFFFFF\" stroke=\"#D6D0C6"), "Lighter against the sky."), "Teak Or White?")
P(G, "Office Garden", A("office_moss", "Office Garden: Moss And Stones", "A small still garden outside the desk.", ["calm", "natural"], "warm", G, court("water").replace("#BFE0E3", "#A9C48E"), "Picked: office with its own garden."),
  A("office_bamboo", "Office Garden: Bamboo Screen", "Tall green screen for privacy.", ["lively", "natural"], "lively", G, court("plants"), "Green wall in view."), "Moss Garden Or Bamboo?")
P(G, "Color Plan Detail", A("cplan_rooms", "Color Rooms Only", "Your color-coded plan, rooms only.", ["clear", "lively"], "lively", G, sheet("color"), "Picked: soft color-coded rooms."),
  A("cplan_furn", "Color Rooms Plus Furniture Outlines", "Same plan with tables and beds drawn in.", ["visual", "clear"], "lively", G, sheet("color") + rect(40, 60, 40, 24, "none", TEAK) + rect(110, 130, 44, 30, "none", TEAK), "See how it fits."), "Rooms Only Or With Furniture?")
def grid2(wide):
    s = rect(14, 30, 212, 196, "#F4F0E8", "none", 10); g = 9 if wide else 4
    for i in range(16): s += rect(22 + (i % 4) * 51, 38 + (i // 4) * 46, 51 - g, 46 - g, "#E2DDD4", "none", 1)
    return s.replace('fill="#F4F0E8"', f'fill="{SAGE}"', 1)
P(G, "Grass Joint Width", A("pav_wide", "Wide Grass Joints", "More green between the pavers.", ["natural", "lively"], "lively", G, grid2(True), "Picked: pavers with grass joints."),
  A("pav_narrow", "Thin Grass Joints", "Mostly stone, a fine green line.", ["clean", "simple"], "airy", G, grid2(False), "Easier to walk and roll."), "Wide Or Thin Joints?")
P(G, "Long Table Seats", A("long_chairs", "Long Oak Table, Chairs All Around", "Your long farm table with eight chairs.", ["simple", "warm"], "warm", G, table("long"), "Picked: long table."),
  A("long_bench", "Long Oak Table, Bench On One Side", "Chairs on one side, a bench on the other.", ["natural", "lively"], "lively", G, table("bench"), "Kids slide in easily."), "All Chairs Or A Bench Side?")
P(G, "Scaled Drawing Detail", A("cad_plain", "Scaled Drawing, Clean Lines", "Your crisp drawing pick, no extra marks.", ["clean", "simple"], "airy", G, sketch("cad"), "Picked: crisp scaled drawing."),
  A("cad_dims", "Scaled Drawing With Room Sizes", "Each room labeled with its size.", ["clear", "visual"], "airy", G, sketch("cad") + t(76, 100, "4.5 x 6 m", 8, LAGOON, "hind", 600, "middle") + t(166, 160, "5 x 7 m", 8, LAGOON, "hind", 600, "middle"), "Sizes at a glance."), "Clean Or With Sizes?")

# ---------- Both: Where Does Each Go? ----------
G = "Both: Where Does Each Go?"
P(G, "Pantry Mix", A("pan_split", "Open Shelves Up, Closed Below", "Jars on top, white doors underneath.", ["natural", "clean"], "airy", G, pantry("open").split('<rect x="40" y="140"')[0] + rect(40, 130, 160, 40, "#FFFFFF", "#E0DAD0"), "You picked both."),
  A("pan_niche", "Closed Cabinets, One Open Niche", "White doors with one jar niche in the middle.", ["clean", "lively"], "airy", G, pantry("closed") + rect(80, 90, 78, 30, "#FFFFFF", "#E0DAD0") + "".join(rect(86 + k * 18, 98, 12, 16, [CLAY, ZEL, "#F2E6CF", CLAY][k], "none", 2) for k in range(4)), "Mostly tidy."), "Mostly Open Or Mostly Closed?")
P(G, "Lamp And Wash", A("lw_both", "Floor Lamp And Wall Wash In Living", "Both lights in the main room.", ["warm", "lively"], "warm", G, lit("lamp") + rect(130, 58, 40, 6, "#FFFFFF", STEEL, 2), "You picked both."),
  A("lw_split", "Wash In Living, Lamp In The Reading Nook", "Each light gets its own room.", ["calm", "simple"], "airy", G, lit("wash"), "Each where it fits."), "Together Or Split?")
P(G, "Peg Wall And Cabinets", A("peg_above", "Peg Wall Above Labeled Cabinets", "Open pegs up top, closed cabinets below.", ["lively", "natural"], "lively", G, gear("wall").replace('height="110"', 'height="60"', 1) + "".join(rect(30 + i * 62, 116, 56, 54, "#FFFFFF", "#E0DAD0") for i in range(3)), "You picked both."),
  A("peg_split", "Pegs In The Garage, Cabinets In The Mudroom", "Gear on view outside, tidy inside.", ["clean", "simple"], "airy", G, gear("closed"), "Each room its own way."), "Stacked Or Split By Room?")
P(G, "Shower Stone Mix", A("shw_mixA", "Limestone Walls, Pebble Floor", "Smooth walls, pebbles underfoot.", ["natural", "calm"], "warm", G, tiles(STONE, "#E9E2D6", "lime") + rect(14, 186, 212, 40, "#CFC6B6", "none", 0) + "".join(dot(24 + k * 13, 200 + (k % 3) * 8, 5, "#B7AC9A") for k in range(16)), "You picked both."),
  A("shw_mixB", "Limestone Everywhere, One Pebble Strip", "A single band of pebble at the drain.", ["clean", "simple"], "airy", G, tiles(STONE, "#E9E2D6", "lime") + rect(100, 30, 40, 196, "#CFC6B6") + "".join(dot(110 + (k % 3) * 10, 40 + k * 12, 4, "#B7AC9A") for k in range(15)), "Mostly smooth."), "Pebble Floor Or One Strip?")
P(G, "Hammock And Daybed", A("hd_split", "Hammock On The Engawa, Daybed In The Court", "Each one in its own spot.", ["lively", "natural"], "lively", G, engawa("hammock"), "You picked both."),
  A("hd_one", "One Daybed With A Hammock Hook Nearby", "Daybed stays, hammock goes up on weekends.", ["simple", "calm"], "airy", G, engawa("daybed"), "Less to store."), "Both Fixed Or One Plus A Hook?")
P(G, "Kids Rooms Mix", A("kids_loft", "Two Rooms, A Loft In The Bigger One", "Shared bath between, a play loft above one.", ["lively", "natural"], "lively", G, R((0, 0, 80, 176, "Kid 1 + Loft", "#F2E3CC"), (80, 0, 32, 176, "Bath", "#DCEBF2"), (112, 0, 80, 176, "Kid 2", "#E4EFD9")), "You picked both."),
  A("kids_later", "One Big Room Now, Wall Added Later", "Starts open with a loft, splits in two later.", ["simple", "airy"], "airy", G, R((0, 0, 192, 120, "Big Room + Loft", "#F2E3CC"), (0, 120, 192, 56, "Bath", "#DCEBF2")) + f'<line x1="120" y1="40" x2="120" y2="160" stroke="{CLAY}" stroke-dasharray="4 3" stroke-width="2"/>', "Grows with them."), "Split Now Or Later?")
P(G, "Net And Boulders", A("pav_stack", "Rope Net Above The Boulder Wall", "Climb the stones, then the net.", ["lively", "natural"], "lively", G, pav("net") + "".join(rect(60 + i * 26, 160, 22, 20, "#BDB3A2", "none", 8) for i in range(5)), "You picked both."),
  A("pav_zones", "Net And Boulders Side By Side", "Two play zones under one roof.", ["calm", "simple"], "airy", G, pav("wall"), "Little and big kids apart."), "Stacked Or Side By Side?")
P(G, "Zellige And Terrazzo", A("bath_zwall", "Zellige Wall, Terrazzo Floor", "Green tile up, chip floor down.", ["lively", "natural"], "lively", G, tiles(ZEL, "#3FA07B", "zel").replace('height="196"', 'height="140"', 1) + rect(14, 170, 212, 56, STONE) + "".join(dot(24 + k * 11, 184 + (k % 4) * 9, 1.8, [CLAY, ZEL][k % 2]) for k in range(19)), "You picked both."),
  A("bath_tniche", "Terrazzo Room, Zellige Niche", "Terrazzo all over, one green niche.", ["clean", "lively"], "airy", G, tiles(CLAY, ZEL, "terr") + rect(90, 70, 60, 70, ZEL, "#FFFFFF", 2, 3), "Small green pop."), "Green Wall Or Green Niche?")
P(G, "Cove And Cans", A("cc_rooms", "Cove In Living, Cans In The Kitchen", "Soft glow to relax, focused light to cook.", ["calm", "clean"], "airy", G, lit("cove"), "You picked both."),
  A("cc_island", "Cove Plus Two Cans Over The Island", "Mostly cove, two cans where you work.", ["simple", "warm"], "warm", G, lit("cove") + "".join(dot(100 + i * 40, 38, 4, "#FFF4D6") for i in range(2)), "One room, both lights."), "Split By Room Or Mixed?")
P(G, "Skylight And Glass", A("sg_both", "Skylight Hall And Glass Engawa Wall", "Both daylight ideas, each in its spot.", ["airy", "lively"], "airy", G, daylight("sky") + rect(160, 70, 60, 90, SKY, "#FFFFFF", 0, 3), "You picked both."),
  A("sg_glass", "Glass Engawa Wall Only", "One big daylight move.", ["simple", "clean"], "airy", G, daylight("glazed"), "Simpler roof."), "Both Or Glass Only?")
P(G, "Wellness Mix", A("well_rowend", "Row With A Plunge Court At The End", "Sauna, steam, wet room, then outside to plunge.", ["calm", "natural"], "warm", G, R((0, 0, 64, 100, "Sauna", "#F2E3CC"), (64, 0, 64, 100, "Steam", "#FFFFFF"), (128, 0, 64, 100, "Wet", "#DCEBF2"), (0, 100, 192, 76, "Plunge Court", "#E4EFD9")), "You picked both."),
  A("well_court", "Around The Court, Sauna Faces The Garden", "Court ring with a garden window in the sauna.", ["airy", "lively"], "lively", G, R((0, 0, 192, 50, "Sauna + Garden View", "#F2E3CC"), (0, 50, 50, 126, "Steam", "#FFFFFF"), (50, 50, 92, 126, "Plunge", "#DCEBF2"), (142, 50, 50, 126, "Wet", "#FFFFFF")), "View while you sweat."), "Row Then Court, Or Court Ring?")

# ---------- Skipped, Asked A New Way ----------
G = "Skipped, Asked A New Way"
def listby(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    heads = ["Kitchen", "Living"] if kind == "room" else ["To Buy", "Picked"]
    for j, hd in enumerate(heads):
        y = 42 + j * 92; s += t(26, y + 10, hd, 10, [ZEL, LAGOON][j], "khand") + "".join(ln(y + 22 + i * 18, 26, 214) + t(26, y + 34 + i * 18, n, 8, INK) for i, n in enumerate(["Dining Table", "Pendant", "Stools x4"]))
    return s
P(G, "Furniture List Grouping", A("bom_room", "Furniture List Grouped By Room", "Items under Kitchen, Living, and so on.", ["clear", "simple"], "airy", G, listby("room"), "Skipped last time; new angle."),
  A("bom_status", "Furniture List Grouped By Status", "To Buy, Ordered, Picked.", ["clear", "lively"], "lively", G, listby("status"), "See what's left."), "By Room Or By Status?", "reask")
def toys(kind):
    s = room("", WALL, OAK, False)
    if kind == "cubby": s += "".join(rect(40 + (i % 4) * 40, 60 + (i // 4) * 40, 36, 36, "#FFFFFF", "#E0DAD0") + rect(46 + (i % 4) * 40, 74 + (i // 4) * 40, 24, 18, [CLAY, ZEL, LAGOON, SAFFRON][i % 4], "none", 3) for i in range(8))
    else: s += "".join(rect(40 + i * 54, 120, 50, 50, "#FFFFFF", "#E0DAD0", 3) + dot(52 + i * 54, 172, 4, MUTE) + dot(80 + i * 54, 172, 4, MUTE) + rect(56 + i * 54, 130, 18, 4, [CLAY, ZEL, LAGOON][i]) for i in range(3))
    return s
P(G, "Toy Storage", A("toy_cubby", "Wall Of Cubbies With Bins", "A grid you can see into.", ["lively", "simple"], "lively", G, toys("cubby"), "Skipped last time; new angle."),
  A("toy_roll", "Rolling Drawers That Hide Away", "Low drawers on wheels under a bench.", ["clean", "calm"], "airy", G, toys("roll"), "Clears off fast."), "Cubbies Or Rolling Drawers?", "reask")
P(G, "Accent Wall Count", A("acc_entry", "One Clay Wall In The Entry Only", "First thing you see, nowhere else.", ["simple", "warm"], "warm", G, accentwall(CLAY), "Skipped last time; new angle."),
  A("acc_two", "Clay In The Entry, Sea Green In A Bath", "Two small accent spots.", ["lively", "natural"], "lively", G, accentwall("#7FB3A6"), "Two pops."), "One Spot Or Two?", "reask")
def overview(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    if kind == "map": s += plan([(0, 0, 96, 88, "Kitchen", "#E4EFD9"), (96, 0, 96, 88, "Living", "#F2E3CC"), (0, 88, 96, 88, "Bed", "#FFFFFF"), (96, 88, 96, 88, "Bath", "#DCEBF2")])
    else: s += "".join(t(26, 56 + i * 40, n, 9, INK, "khand") + rect(26, 62 + i * 40, 188, 6, "#EEEAE4", "none", 3) + rect(26, 62 + i * 40, 188 * f, 6, c, "none", 3) for i, (n, f, c) in enumerate([("Kitchen", .8, ZEL), ("Living", .5, LAGOON), ("Bedrooms", .3, SAFFRON), ("Outdoor", .6, CLAY)]))
    return s
P(G, "Project Overview", A("ov_map", "Overview As A Tappable Floor Plan", "Tap a room on the plan for its decisions.", ["visual", "lively"], "lively", G, overview("map"), "Skipped last time; new angle."),
  A("ov_bars", "Overview As Progress Bars", "One bar per area, how much is decided.", ["clear", "simple"], "airy", G, overview("bars"), "Where am I at?"), "Plan Map Or Progress Bars?", "reask")
def split(kind):
    s = rect(14, 30, 212, 196, "#FFFFFF", "#D6D0C6", 2)
    if kind == "side": s += rect(24, 40, 100, 176, "#F3ECE1") + rect(24, 170, 100, 46, OAK) + rect(34, 56, 40, 40, SKY) + "".join(ln(54 + i * 16, 134, 214) for i in range(10))
    else: s += rect(24, 40, 192, 150, "#F3ECE1") + rect(24, 150, 192, 40, OAK) + rect(40, 56, 50, 50, SKY) + "".join(dot(106 + i * 14, 204, 4, INK if i == 0 else "#D6D0C6") for i in range(3))
    return s
P(G, "Design Page Layout", A("pg_side", "View And Specs Side By Side", "Drawing left, specs right, same page.", ["clear", "visual"], "airy", G, split("side"), "Skipped last time; new angle."),
  A("pg_swipe", "Full View, Swipe For Specs", "Big drawing; swipe to see the specs.", ["visual", "airy"], "lively", G, split("swipe"), "Picture fills the page."), "Side By Side Or Swipe?", "reask")
P(G, "Herbs Placement", A("herb_box", "Window Box Outside The Kitchen Sink", "Reach out the window to pick.", ["natural", "lively"], "lively", G, kitchen("back") + rect(100, 46, 80, 10, CLAY) + "".join(dot(106 + k * 10, 44, 4, LEAF) for k in range(8)), "Skipped last time; new angle."),
  A("herb_court", "Herbs In The Courtyard Bed Only", "Kitchen stays clear; herbs grow outside.", ["clean", "simple"], "airy", G, court("herb"), "Pairs with the raised beds."), "Window Box Or Courtyard?", "reask")
def pend(kind):
    s = room(rect(60, 150, 120, 26, "#FFFFFF", "#E0DAD0", 6), WALL, OAK) + f'<line x1="150" y1="30" x2="150" y2="62" stroke="{MUTE}"/>'
    if kind == "paper": s += f'<ellipse cx="150" cy="80" rx="20" ry="20" fill="#FFFDF4" stroke="#E6DCC6"/>' + "".join(f'<path d="M131 {72+i*6} H169" stroke="#EADFC8"/>' for i in range(3))
    else: s += "".join(rect(132 + i * 6, 64, 4, 30, OAK) for i in range(7)) + f'<path d="M136 94 L122 150 H178 L164 94 Z" fill="#FFF4D6" opacity=".5"/>'
    return s
P(G, "Pendant Style", A("pend_paper", "White Paper Lantern", "Soft round glow, very light.", ["airy", "simple"], "airy", G, pend("paper"), "Skipped linen vs rattan; new forms."),
  A("pend_slat", "Oak Slat Pendant", "Thin oak slats, warm light below.", ["warm", "natural"], "warm", G, pend("slat"), "Wood to match the floor."), "Paper Or Oak Slats?", "reask")
def closet2(kind):
    s = room("", WALL, OAK, False)
    if kind == "half": s += rect(30, 50, 90, 4, OAK) + "".join(f'<path d="M{40+i*14} 54 v6 l-6 30 h12 l-6 -30" fill="{["#FFFFFF",ZEL,"#E9DCC6",CLAY][i%4]}" stroke="#D9D3C9"/>' for i in range(6)) + rect(122, 46, 44, 124, "#FFFFFF", "#E6E1D8") + rect(166, 46, 44, 124, "#FFFFFF", "#E6E1D8")
    else: s += rect(30, 46, 180, 124, "#F7F2E8") + "".join(f'<path d="M{30+i*18} 46 q9 62 0 124" fill="none" stroke="#E2D8C4" stroke-width="2"/>' for i in range(11))
    return s
P(G, "Closet Front", A("cl_half", "Half Open Rail, Half Flush Doors", "Daily clothes on view, the rest behind doors.", ["lively", "clean"], "airy", G, closet2("half"), "Skipped last time; new angle."),
  A("cl_curtain", "Linen Curtain Across The Closet", "One soft curtain instead of doors.", ["natural", "calm"], "warm", G, closet2("curtain"), "Soft and light."), "Half And Half Or A Curtain?", "reask")

# ---------- New Open Decisions ----------
G = "New Open Decisions"
def counter(c, veins):
    s = kitchen("back").replace(f'rect x="14" y="124" width="212" height="6" fill="{STONE}"', f'rect x="14" y="124" width="212" height="6" fill="{c}"')
    return s + rect(14, 118, 212, 12, c, "#E0DAD0") + ("".join(f'<path d="M{20+k*30} 120 q10 6 24 2" fill="none" stroke="#BDB3A2"/>' for k in range(7)) if veins else "")
P(G, "Kitchen Counter", A("ctr_quartz", "Plain Light Quartz Counter", "Even off-white, no veins.", ["clean", "simple"], "airy", G, counter("#F4F1EA", False), "Easy to keep clean."),
  A("ctr_stone", "Honed Stone With Soft Veins", "Natural stone, gentle grey lines.", ["natural", "warm"], "warm", G, counter("#ECE6DA", True), "A bit of nature."), "Quartz Or Honed Stone?", "new")
def floor(kind):
    s = rect(14, 30, 212, 196, WALL, "none", 10)
    if kind == "oak": s += rect(14, 120, 212, 106, OAK) + "".join(f'<line x1="14" y1="{132+i*16}" x2="226" y2="{132+i*16}" stroke="#C8AB80"/>' for i in range(6))
    else: s += rect(14, 120, 212, 106, "#E3DFD8") + "".join(dot(20 + (k * 37) % 200, 126 + (k * 23) % 96, 1, "#C9C3BA") for k in range(120))
    return s + rect(60, 100, 120, 40, "#FFFFFF", "#E0DAD0", 6) + plant(200, 150, .7)
P(G, "Main Floor", A("fl_oak", "Wide Light Oak Planks", "Warm wood through the main rooms.", ["warm", "natural"], "warm", G, floor("oak"), "Soft underfoot."),
  A("fl_conc", "Light Polished Concrete", "Smooth pale floor, cool in summer.", ["clean", "airy"], "airy", G, floor("conc"), "Easy with kids and dogs."), "Oak Or Concrete?", "new")
def winframe(c):
    return rect(14, 30, 212, 196, WALL, "none", 10) + rect(40, 50, 160, 130, SKY, c, 0, 6) + f'<line x1="120" y1="50" x2="120" y2="180" stroke="{c}" stroke-width="5"/>' + f'<path d="M44 176 q20 -40 40 -6 q20 -50 50 0 q20 -30 62 4 V176 Z" fill="{SAGE}"/>' + rect(14, 196, 212, 30, OAK)
P(G, "Window Frames", A("win_oak", "Oak Window Frames", "Wood frames inside.", ["warm", "natural"], "warm", G, winframe(OAK), "Matches the floor."),
  A("win_white", "Slim White Frames", "Frames disappear into the wall.", ["clean", "airy"], "airy", G, winframe("#FFFFFF"), "All view, no frame."), "Oak Or White?", "new")
def vanity3(kind):
    s = room(rect(84, 52, 72, 50, "#EEF4F6", "#CFC8BC", 3), WALL, STONE, False)
    if kind == "float": s += rect(60, 118, 120, 30, OAK, "none", 2) + rect(90, 112, 60, 10, "#FFFFFF", "#CFC8BC", 5)
    else: s += rect(80, 130, 80, 40, "#E4DED3") + f'<ellipse cx="120" cy="124" rx="34" ry="10" fill="#F1ECE3" stroke="#CFC8BC"/>'
    return s
P(G, "Bath Vanity", A("van_float", "Floating Oak Vanity", "Oak drawer box off the floor.", ["light", "clean"], "airy", G, vanity3("float"), "Floor stays open."),
  A("van_stone", "Stone Basin On A Plinth", "One carved stone basin.", ["natural", "calm"], "warm", G, vanity3("stone"), "Spa feel."), "Floating Oak Or Stone Basin?", "new")
def genkan(kind):
    s = rect(14, 30, 212, 196, WALL, "none", 10) + rect(14, 170, 212, 56, STONE)
    s += rect(14, 140, 212, 30, OAK if kind == "oak" else "#CFC8BC") + (rect(14, 140, 212, 4, TEAK) if kind == "oak" else "")
    return s + rect(30, 176, 16, 8, CLAY, "none", 3) + rect(52, 176, 16, 8, "#FFFFFF", "none", 3)
P(G, "Genkan Step", A("gk_oak", "Oak Step Up From The Genkan", "Warm wood ledge where shoes come off.", ["warm", "natural"], "warm", G, genkan("oak"), "Sit to take shoes off."),
  A("gk_stone", "Stone Step Up From The Genkan", "Same stone as the entry floor.", ["clean", "simple"], "airy", G, genkan("stone"), "One calm material."), "Oak Or Stone Step?", "new")
def showerg(kind):
    s = tiles(STONE, "#E9E2D6", "lime")
    return s + (rect(110, 40, 6, 186, "#DCEBF2", "#B9CDD8") if kind == "glass" else rect(100, 120, 20, 106, "#FFFFFF", "#D6D0C6"))
P(G, "Shower Screen", A("sh_glass", "One Clear Glass Panel", "Light passes right through.", ["airy", "clean"], "airy", G, showerg("glass"), "Room feels bigger."),
  A("sh_wall", "Low Plaster Half Wall", "Waist-high wall, open above.", ["natural", "simple"], "warm", G, showerg("wall"), "No glass to clean."), "Glass Or Half Wall?", "new")
def sauna(c):
    return rect(14, 30, 212, 196, c, "none", 10) + "".join(f'<line x1="14" y1="{44+i*14}" x2="226" y2="{44+i*14}" stroke="#00000012"/>' for i in range(13)) + rect(30, 130, 180, 14, c, "#00000020") + rect(30, 170, 180, 14, c, "#00000020") + rect(170, 50, 40, 50, SKY, "#FFFFFF", 0, 3)
P(G, "Sauna Wood", A("sa_hinoki", "Pale Hinoki Sauna", "Light, lemony Japanese cypress.", ["airy", "natural"], "airy", G, sauna("#EEDDB8"), "Bright inside."),
  A("sa_cedar", "Warm Red Cedar Sauna", "Deeper honey-red boards.", ["warm", "natural"], "warm", G, sauna("#D9A47A"), "Cozy glow."), "Hinoki Or Cedar?", "new")
def hood(kind):
    s = kitchen("back")
    return s + (f'<path d="M100 30 H180 L170 56 H110 Z" fill="#FFFFFF" stroke="#E0DAD0"/>' if kind == "plaster" else rect(100, 50, 80, 6, STEEL))
P(G, "Range Hood", A("hood_plaster", "Plastered Hood Over The Range", "A soft white hood shape.", ["natural", "warm"], "warm", G, hood("plaster"), "Part of the wall."),
  A("hood_hidden", "Hidden Hood In The Cabinets", "Only a slim strip shows.", ["clean", "simple"], "airy", G, hood("hidden"), "Nothing sticks out."), "Plaster Hood Or Hidden?", "new")
def bedwall(kind):
    s = room("", WALL, OAK, False)
    s += (rect(40, 50, 160, 90, OAK) + "".join(f'<line x1="{40+i*16}" y1="50" x2="{40+i*16}" y2="140" stroke="#C8AB80"/>' for i in range(1, 10)) if kind == "oak" else rect(40, 50, 160, 90, "#F3EBDD"))
    return s + rect(50, 130, 140, 40, "#FFFFFF", "#E0DAD0", 4) + rect(56, 124, 40, 14, "#E4EFD9", "none", 4) + rect(144, 124, 40, 14, "#F2E3CC", "none", 4)
P(G, "Behind The Bed", A("bw_oak", "Oak Panel Wall Behind The Bed", "Vertical oak boards as a headboard wall.", ["warm", "natural"], "warm", G, bedwall("oak"), "Built-in headboard."),
  A("bw_plaster", "Plain Warm Plaster Behind The Bed", "Smooth wall, bed does the work.", ["calm", "simple"], "airy", G, bedwall("plaster"), "Quiet and soft."), "Oak Panels Or Plaster?", "new")
def cover(kind):
    s = winframe("#FFFFFF")
    if kind == "linen": s += rect(30, 44, 30, 140, "#F7F2E8") + rect(180, 44, 30, 140, "#F7F2E8") + rect(26, 40, 188, 4, BRONZE)
    else: s += "".join(rect(40 + i * 40, 50, 40, 130, "#FFFDF6", "#D9CCB4") + "".join(f'<line x1="{40+i*40}" y1="{70+k*20}" x2="{80+i*40}" y2="{70+k*20}" stroke="#E2D6C0"/>' for k in range(6)) for i in range(2))
    return s
P(G, "Window Covering", A("cov_linen", "Linen Curtains On A Bronze Rod", "Soft white linen at the sides.", ["warm", "airy"], "airy", G, cover("linen"), "Soft light."),
  A("cov_shoji", "Shoji Paper Sliders", "Paper screens slide over the glass.", ["natural", "calm"], "warm", G, cover("shoji"), "Japanese calm."), "Linen Or Shoji?", "new")
def cpath(kind):
    s = rect(14, 30, 212, 196, "#BFD7A5", "none", 10)
    if kind == "steps": s += "".join(f'<ellipse cx="{120+(i%2)*14-7}" cy="{210-i*26}" rx="16" ry="9" fill="{STONE}"/>' for i in range(7))
    else: s += f'<path d="M100 226 L112 40 L128 40 L140 226 Z" fill="#E6DFD2"/>' + "".join(dot(104 + (k * 7) % 34, 50 + (k * 13) % 170, 1.2, "#BDB3A2") for k in range(90))
    return s + plant(60, 140, .7) + plant(180, 180, .7)
P(G, "Courtyard Path", A("cp_steps", "Stepping Stones In Grass", "Flat stones with grass around.", ["natural", "lively"], "lively", G, cpath("steps"), "Garden feel."),
  A("cp_gravel", "Fine Gravel Path With Steel Edge", "A clean gravel strip.", ["clean", "simple"], "airy", G, cpath("gravel"), "Easy with a cart."), "Stepping Stones Or Gravel?", "new")
def garage(kind):
    s = rect(14, 30, 212, 196, SKY, "none", 10) + rect(14, 196, 212, 30, STONE) + rect(30, 70, 180, 126, "#FFFFFF", "#D6D0C6")
    return s + (rect(46, 90, 148, 106, TEAK) + "".join(f'<line x1="46" y1="{96+i*8}" x2="194" y2="{96+i*8}" stroke="#9B7148"/>' for i in range(13)) if kind == "teak" else rect(46, 90, 148, 106, "#F5F3EF", "#D6D0C6"))
P(G, "Garage Door", A("gar_teak", "Teak Slat Garage Door", "Matches the teak front door.", ["warm", "natural"], "warm", G, garage("teak"), "One wood story."),
  A("gar_white", "Flat White Garage Door", "Blends into the white wall.", ["clean", "simple"], "airy", G, garage("white"), "Front door stands out."), "Teak Or White?", "new")
def rug(kind):
    s = floor("oak").split('<rect x="60"')[0]
    s += (rect(40, 140, 160, 70, "#F3ECE1", "#E0D3BE", 2) + "".join(f'<line x1="44" y1="{146+i*6}" x2="196" y2="{146+i*6}" stroke="#E6DAC6"/>' for i in range(10)) if kind == "jute" else rect(40, 140, 160, 70, "#FFFFFF", "#E0DAD0", 2) + rect(40, 140, 160, 8, CLAY) + rect(40, 202, 160, 8, ZEL))
    return s + rect(70, 110, 100, 34, "#FFFFFF", "#E0DAD0", 6)
P(G, "Living Rug", A("rug_jute", "Natural Jute Rug", "Woven, earthy, no pattern.", ["natural", "calm"], "warm", G, rug("jute"), "Texture, no color."),
  A("rug_band", "White Wool Rug With Color Bands", "Thin clay and green bands at the ends.", ["lively", "clean"], "lively", G, rug("band"), "Small color pop."), "Jute Or Banded Wool?", "new")

for p in pairs: p["share"] = True
finish(DID, "Blueprint Round 2: Building On Your Picks, Both Answers Placed, Skipped Pairs Asked Anew, New Open Decisions", "Blueprint", pairs, 0,
       {"builds_on": "blueprint-1 (results/blueprint-1.txt, 42/50; top tags airy, simple, natural, lively, clean)",
        "brands": ["Blueprint: Max's architecture and interior design agent (Weberman Residence)", "White base, Khand/Hind, small pops of #C1502E, #05668D, #0B6E4F, #D4A017"],
        "feelings": {"airy": "Light and clean", "warm": "Warm and natural", "lively": "Lively color pop"},
        "sources": {"results": "results/blueprint-1.txt", "previous_deck": "decks/blueprint-1.json"}}, seed=21)
d = json.load(open(f"decks/{DID}.json")); d.pop("draft", None); d["status"] = "published"
for pp in d["pairs"]:
    for k in "AB": o = pp["option" + k]; o["tags"] = list(dict.fromkeys(o["tags"]))
json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
