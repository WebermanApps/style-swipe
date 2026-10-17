"""What We Take Care Of Deck: homepage section remake. Every item is already on smartupkeep.ai (app.js home(), WW_WI, FEATURED);
lawn cutting is one add-on (Custom Grass Cutting). Badges: approved set; new ones only where the site backs them."""
from uk5_art import *
PAIRS = []
def pair(g, ask, a, b): PAIRS.append((g, ask, a, b))
SC = 212 / 192
def ph(inner, h=222):
    return ('<clipPath id="phc"><rect x="14" y="30" width="212" height="241"/></clipPath><g clip-path="url(#phc)">' + g(14, 30, round(SC, 4), rect(0, 0, 192, h, "#FFFFFF") + inner) + '</g>' + rect(14, 30, 212, 241, "none", "#BDB6AA", 0, 1))
def hdr(y=0, link="See All"):
    return t(10, y + 22, "What We Take Care Of", 17, INK, "khand") + t(182, y + 22, link.upper(), 7.5, TERRA, "hind", 600, "end", 'letter-spacing=".8"') + f'<path d="M{182-len(link)*5.2:.0f} {y+25} H182" stroke="{TERRA}88" stroke-width=".8"/>'
def side(lines, y=60):
    return ""
def foot(items): return chips(277, items, 14)
CORE = [("furnace", "Furnace"), ("ac", "AC"), ("waterheater", "Water Heater"), ("dryer", "Dryer Vent"), ("detector", "Smoke/CO"), ("meter", "Mold & Moisture"), ("gutter", "Gutters"), ("roof", "Roof")]
ACC4 = [TERRA, LAGOON, JUNGLE, SAFFRON]
def tile(x, y, w, h, ic, lb, c, sub=None, tagtxt=None, fill="#FFFFFF"):
    s = rect(x, y, w, h, fill, LINE, 0, 1) + rect(x + 6, y + 6, 22, 22, c + "1F") + icon(ic, x + 9, y + 9, 16, c, 2) + t(x + 6, y + h - (16 if sub else 7), lb, 9.5, INK, "khand")
    if sub: s += t(x + 6, y + h - 6, sub, 7.5, MUTE)
    if tagtxt: s += rect(x + w - len(tagtxt) * 4.2 - 10, y + 6, len(tagtxt) * 4.2 + 6, 10, c + "22") + t(x + w - 7, y + 13.5, tagtxt, 6.5, c, "hind", 600, "end")
    return s
def grid(y, items, cols=3, w=56, h=52, gap=6, x0=10, lawn=True):
    s = ""
    for i, (ic, lb) in enumerate(items):
        s += tile(x0 + (i % cols) * (w + gap), y + (i // cols) * (h + gap), w, h, ic, lb, ACC4[i % 4])
    if lawn:
        i = len(items); s += tile(x0 + (i % cols) * (w + gap), y + (i // cols) * (h + gap), w, h, "lawn", "Grass Cutting", JUNGLE, None, "ADD-ON", "#F4F8EF")
    return s
def season_card(x, y, w, h, name, ic, c, items):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 0, 1) + rect(x, y, w, 4, c) + rect(x + 8, y + 12, 26, 26, c + "1F") + icon(ic, x + 11, y + 15, 20, c, 2) + t(x + 40, y + 31, name, 15, c, "khand")
    for i, it in enumerate(items):
        s += ln(y + 46 + i * 22, x + 8, x + w - 8) + t(x + 8, y + 61 + i * 22, it, 9, INK, "hind", 500) + t(x + w - 8, y + 61 + i * 22, "›", 11, GREY, "hind", 400, "end")
    return s
SEASONS = [("Spring", "flower", JUNGLE, ["AC Tune-Up", "Gutter Cleaning", "Mold & Moisture Scan", "Visit Report"]),
           ("Fall", "leaf", TERRA, ["Furnace Tune-Up", "Gutter Cleaning", "Garage Weatherproofing", "Furnace Filters"]),
           ("Winter", "snow", LAGOON, ["Ice Dam Clearing", "Pre and Post Storm Checks", "Smoke/CO Checks", "Furnace Filters"])]
def carousel(y, cur=1):
    s = season_card(10, y, 150, 150, *SEASONS[cur]) + season_card(166, y, 150, 150, *SEASONS[cur + 1])
    return s + dots_ind(96, y + 162, 4, cur) + t(10, y + 180, "Every visit: moisture scan, filters, report.", 7.5, MUTE)
def house_map(y):
    s = f'<path d="M6 {y+44} L96 {y+2} L186 {y+44} Z" fill="{CREAM}" stroke="{INK}" stroke-width="1.4"/>' + rect(12, y + 44, 168, 132, "#FFFFFF", INK, 0, 1.4)
    s += f'<path d="M12 {y+88} H180 M96 {y+88} V{y+132}" stroke="#CFC6B4" stroke-width="1"/>' + rect(12, y + 132, 168, 44, "#F3EEE6", INK, 0, 1.4) + rect(0, y + 176, 192, 10, "#E4EEDC")
    pins = [(40, y + 30, "1", TERRA, "Roof & Gutters"), (22, y + 64, "2", LAGOON, "Bedrooms: Smoke/CO"), (22, y + 108, "3", LAGOON, "Laundry: Dryer"), (104, y + 108, "4", SAFFRON, "Kitchen: Fridge Filter"),
            (22, y + 146, "5", TERRA, "Basement: Furnace,"), (22, y + 166, "6", JUNGLE, "Mold & Moisture Scan"), (112, y + 146, "7", INK, "Garage Door"), (112, y + 166, "8", JUNGLE, "Yard: Grass Add-On")]
    for x, yy, n, c, lb in pins:
        s += f'<circle cx="{x}" cy="{yy}" r="6.5" fill="{c}"/>' + t(x, yy + 3, n, 7.5, "#FFFFFF", "hind", 700, "middle") + t(x + 10, yy + 3, lb, 7.5, INK, "hind", 600)
    s += t(32, y + 157, "Water Heater", 7.5, INK, "hind", 600)
    return s
# 1 icon grid vs seasonal carousel (lead)
pair("Layout", "Layout: Icon Grid Of Everything, Or A Seasonal Carousel?",
 ("ww_grid", "Icon Grid", "All 8 core services at once, plus the grass cutting add-on as one tile.", "practical",
  card("Layout", TERRA, ph(hdr() + grid(36, CORE)) + foot(["See it all", "9 tiles"]))),
 ("ww_carousel", "Seasonal Carousel", "Swipe Spring, Summer, Fall, Winter; each card lists what that visit covers.", "playful",
  card("Layout", JUNGLE, ph(hdr() + carousel(36)) + foot(["Swipe", "By the calendar"]))))
# 2 house map vs grid by system (current carousel of systems)
pair("Layout", "Layout: Room-By-Room House Map With Numbered Pins, Or Today's Swipe Cards By System?",
 ("ww_housemap", "Room-By-Room House Map", "Tap a numbered pin to see what's done in that part of the home.", "bold",
  card("Layout", LAGOON, ph(hdr(0, "Tap A Pin") + house_map(36)) + foot(["Visual", "Tap pins"]))),
 ("ww_systemcards", "Swipe Cards By System (Today)", "Keep today's Heating & Cooling, Water, Air & Safety, Outside cards, refined.", "calm",
  card("Layout", TERRA, ph(hdr() + season_card(10, 36, 150, 120, "Heating & Cooling", "furnace", TERRA, ["Furnace", "AC", "Furnace Filters"]) + season_card(166, 36, 150, 120, "Water", "drop", LAGOON, ["Water Heater", "Mold and Moisture Scan", "Gutters"]) + dots_ind(96, 170, 4, 0)) + foot(["Familiar", "Current A"]))))
# 3 photo vs illustration
def photo_tile(x, y, w, h, kind, lb, c):
    s = f'<defs><linearGradient id="pg{x}{y}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}55"/><stop offset="1" stop-color="#2B2622"/></linearGradient></defs>'
    s += rect(x, y, w, h, f"url(#pg{x}{y})") + icon(kind, x + w / 2 - 14, y + h / 2 - 22, 28, "#FFFFFFCC", 1.6) + rect(x, y + h - 16, w, 16, "#0A0A0A88") + t(x + 5, y + h - 5, lb, 8.5, "#FFFFFF", "khand")
    s += rect(x + w - 26, y + 4, 22, 9, "#FFFFFFCC") + t(x + w - 15, y + 11, "PHOTO", 5.5, INK, "hind", 600, "middle")
    return s
def illo_tile(x, y, w, h, kind, lb, c):
    s = rect(x, y, w, h, CREAM, LINE) + g(x + 4, y + 8, .32, person(polo=TERRA, hat="cap", shoe="athletic")) + icon(kind, x + w - 30, y + 18, 24, c, 1.8) + f'<path d="M{x+30} {y+44} L{x+w-32} {y+34}" stroke="{INK}" stroke-width="1"/>'
    return s + t(x + 5, y + h - 5, lb, 8.5, INK, "khand")
P3 = [("furnace", "Furnace", TERRA), ("waterheater", "Water Heater", LAGOON), ("gutter", "Gutters", JUNGLE), ("meter", "Moisture Scan", SAFFRON)]
pair("Visual Style", "Tile Visuals: Real Visit Photos, Or Drawn Tech-At-Work Illustrations Like The Site Video?",
 ("ww_photo", "Real Visit Photos", "Photos from real visits on each tile (placeholder frames shown).", "premium",
  card("Visual Style", INK, ph(hdr() + "".join(photo_tile(10 + (i % 2) * 88, 36 + (i // 2) * 84, 84, 78, k, lb, c) for i, (k, lb, c) in enumerate(P3)) + t(10, 214, "Needs a photo shoot on real visits.", 7.5, MUTE)) + foot(["Real", "Needs photos"]))),
 ("ww_illo", "Drawn Illustrations", "Same flat tech style as the homepage video and header van.", "calm",
  card("Visual Style", TERRA, ph(hdr() + "".join(illo_tile(10 + (i % 2) * 88, 36 + (i // 2) * 84, 84, 78, k, lb, c) for i, (k, lb, c) in enumerate(P3)) + t(10, 214, "Matches the video and van.", 7.5, MUTE)) + foot(["On brand", "Ready now"]))))
# 4 grouping season vs system
def glist(y, groups):
    s = ""; yy = y
    for name, c, items in groups:
        s += rect(10, yy, 4, 12, c) + t(18, yy + 10, name, 11, c, "khand") ; yy += 16
        s += t(18, yy + 8, " · ".join(items), 7.5, INK) ; yy += 18
    return s
BY_SEASON = [("Spring", JUNGLE, ["AC Tune-Up", "Gutter Cleaning"]), ("Fall", TERRA, ["Furnace Tune-Up", "Gutters", "Garage Weatherproofing"]), ("Winter", LAGOON, ["Ice Dam Clearing", "Storm Checks"]), ("Summer", SAFFRON, ["Grass Cutting (Add-On)"]), ("Every Visit", INK, ["Moisture Scan", "Filters", "Smoke/CO", "Report"])]
BY_SYSTEM = [("Heating & Cooling", TERRA, ["Furnace", "AC", "Furnace Filters"]), ("Water", LAGOON, ["Water Heater Flush", "Softener Salt"]), ("Air & Safety", SAFFRON, ["Dryer Vent", "Smoke/CO", "GFCI"]), ("Outside", JUNGLE, ["Gutters", "Roof", "Garage Door"]), ("Records", INK, ["Visit Report", "Recall Monitoring"])]
BY_ROOM = [("Basement", TERRA, ["Furnace", "Water Heater", "Shut-Off Valve"]), ("Kitchen & Laundry", SAFFRON, ["Fridge Filter", "Dryer Vent", "GFCI"]), ("Bedrooms", LAGOON, ["Smoke/CO Checks"]), ("Roof & Outside", JUNGLE, ["Gutters", "Roof & Flashing"]), ("Garage & Yard", INK, ["Garage Door", "Grass Cutting (Add-On)"])]
pair("Grouping", "Group Items: By Season, Or By Home System?",
 ("grp_season", "By Season", "Spring, Fall, Winter, Summer, plus what happens every visit.", "playful",
  card("Grouping", JUNGLE, ph(hdr() + glist(36, BY_SEASON)) + foot(["When"]))),
 ("grp_system", "By Home System", "Heating & Cooling, Water, Air & Safety, Outside, Records.", "practical",
  card("Grouping", TERRA, ph(hdr() + glist(36, BY_SYSTEM)) + foot(["What"]))))
# 5 system vs room
pair("Grouping", "Group Items: By Home System, Or By Room?",
 ("grp_system2", "By Home System", "How a tech thinks about the house.", "practical",
  card("Grouping", LAGOON, ph(hdr() + "".join(tile(10 + (i % 2) * 88, 36 + (i // 2) * 52, 84, 46, ic, n, c) for i, (ic, n, c) in enumerate([("furnace", "Heating & Cooling", TERRA), ("drop", "Water", LAGOON), ("detector", "Air & Safety", SAFFRON), ("gutter", "Outside", JUNGLE), ("report", "Records", INK), ("lawn", "Grass Cutting", JUNGLE)]))) + foot(["Tech view"]))),
 ("grp_room", "By Room", "How a homeowner walks the house.", "calm",
  card("Grouping", SAFFRON, ph(hdr() + "".join(tile(10 + (i % 2) * 88, 36 + (i // 2) * 52, 84, 46, ic, n, c) for i, (ic, n, c) in enumerate([("furnace", "Basement", TERRA), ("dryer", "Kitchen & Laundry", SAFFRON), ("detector", "Bedrooms", LAGOON), ("roof", "Roof & Outside", JUNGLE), ("garage", "Garage", INK), ("lawn", "Yard (Add-On)", JUNGLE)]))) + foot(["Homeowner view"]))))
# 6 item count
ALL16 = CORE + [("filter", "Filters"), ("valve", "GFCI & Valves"), ("garage", "Garage Door"), ("drop", "Softener Salt"), ("storm", "Storm Checks"), ("snow", "Ice Dams"), ("generator", "Generator"), ("report", "Visit Report")]
TIER = {"Gutters": "PLUS", "Roof": "COMPLETE", "GFCI & Valves": "PLUS", "Garage Door": "PLUS", "Softener Salt": "PLUS", "Storm Checks": "COMPLETE", "Ice Dams": "COMPLETE", "Generator": "COMPLETE"}
def grid16(y):
    s = ""; w, h = 43, 38
    for i, (ic, lb) in enumerate(ALL16):
        x = 10 + (i % 4) * (w + 4); yy = y + (i // 4) * (h + 4); c = ACC4[i % 4]
        s += rect(x, yy, w, h, "#FFFFFF", LINE) + icon(ic, x + 4, yy + 4, 14, c, 2) + t(x + 4, yy + h - 5, lb if len(lb) < 11 else lb[:10] + ".", 7.5, INK, "khand")
        if lb in TIER: s += rect(x + w - 4, yy, 4, 4, TERRA if TIER[lb] == "COMPLETE" else SAFFRON)
    return s
pair("Item Count", "How Many Items: The 8 Core Services, Or All 16 With Plan Dots?",
 ("cnt_8", "8 Core Services", "Today's eight, plus the add-on tile. Short and scannable.", "calm",
  card("Item Count", TERRA, ph(hdr() + grid(36, CORE)) + foot(["8 + add-on"]))),
 ("cnt_16", "All 16, Plan Dots", "Every included service; a dot marks Plus or Complete items.", "practical",
  card("Item Count", LAGOON, ph(hdr() + grid16(36) + rect(10, 205, 8, 8, SAFFRON) + t(22, 212, "Plus", 7.5, INK) + rect(52, 205, 8, 8, TERRA) + t(64, 212, "Complete", 7.5, INK)) + foot(["16 items", "Plan dots"]))))
# 7 tap to expand
DETAIL = ["Moisture meter and thermal camera", "Damp spots flagged with photos", "Readings saved to your Home Record", "Not a lab mold test"]
def sheet():
    s = grid(36, CORE[:6], lawn=False) + rect(0, 0, 192, 222, "#0A0A0A55") + rect(0, 80, 192, 142, "#FFFFFF") + rect(84, 85, 24, 3, "#CFC6B4") + rect(10, 94, 24, 24, SAFFRON + "1F") + icon("meter", 13, 97, 18, SAFFRON, 2) + t(40, 111, "Mold & Moisture Scan", 13, INK, "khand")
    s += "".join(ln(124 + i * 18, 10, 182) + t(10, 136 + i * 18, d, 8, INK) for i, d in enumerate(DETAIL)) + rect(10, 198, 172, 18, TERRA) + t(96, 210, "FREE QUOTE IN MINUTES", 7.5, "#FFFFFF", "hind", 600, "middle")
    return s
def inline():
    s = ""
    for i, (ic, lb) in enumerate([("furnace", "Furnace"), ("meter", "Mold & Moisture Scan"), ("waterheater", "Water Heater"), ("dryer", "Dryer Vent")]):
        y = 36 + i * 28 + (70 if i > 1 else 0)
        s += rect(10, y, 172, 26, "#FFFFFF", LINE) + icon(ic, 15, y + 5, 16, ACC4[i], 2) + t(36, y + 17, lb, 10, INK, "khand") + t(176, y + 17, "−" if i == 1 else "+", 11, INK, "hind", 600, "end")
        if i == 1: s += rect(10, y + 26, 172, 68, CREAM) + "".join(t(18, y + 41 + k * 15, "· " + d, 8, INK) for k, d in enumerate(DETAIL))
    return s
pair("Tap To Expand", "Tap An Item: Slide-Up Sheet Over The Grid, Or Open In Place Like An Accordion?",
 ("tap_sheet", "Slide-Up Sheet", "Details slide up from the bottom with a quote button.", "premium",
  card("Tap To Expand", SAFFRON, ph(hdr() + sheet()) + foot(["Focused", "Has a CTA"]))),
 ("tap_inline", "Open In Place", "The row grows to show details; the rest stays on screen.", "calm",
  card("Tap To Expand", LAGOON, ph(hdr() + inline()) + foot(["Stay in list"]))))
# 8 lawn add-on placement (one add-on)
def banner(y):
    return rect(10, y, 172, 64, "#F4F8EF", JUNGLE, 0, 1) + icon("lawn", 18, y + 12, 34, JUNGLE, 2) + t(60, y + 16, "FEATURED ADD-ON", 7, JUNGLE, "hind", 600, extra='letter-spacing="1"') + t(60, y + 32, "Custom Grass Cutting", 12, INK, "khand") + t(60, y + 44, "Measured From Above.", 8, MUTE) + t(60, y + 55, "No Visit Needed.", 8, MUTE)
pair("Add-On", "Grass Cutting Add-On: One Tile Inside The Grid, Or One Featured Banner Under It?",
 ("lawn_tile", "One Tile In The Grid", "Sits with the services, marked Add-On.", "calm",
  card("Grass Cutting Add-On", JUNGLE, ph(hdr() + grid(36, CORE) + f'<rect x="132" y="150" width="56" height="52" fill="none" stroke="{JUNGLE}" stroke-width="2"/>') + foot(["One add-on", "Quiet"]))),
 ("lawn_banner", "One Featured Banner", "Six core tiles, then one banner with the site's lawn line.", "bold",
  card("Grass Cutting Add-On", TERRA, ph(hdr() + grid(36, CORE[:6], lawn=False) + banner(156)) + foot(["One add-on", "Stands out"]))))
# 9 approved badges placement
def badge(x, y, ic, lb, c, w=None):
    w = w or len(lb) * 4.9 + 26
    return rect(x, y, w, 18, c + "14", c, 0, .9) + icon(ic, x + 4, y + 3, 12, c, 2) + t(x + 19, y + 12.4, lb, 7.5, c, "hind", 600), w
def badge_row(y, items, cols=2):
    s = ""; w = (172 - (cols - 1) * 6) / cols; h = 28
    for k, (ic, lb, c) in enumerate(items):
        x = 10 + (k % cols) * (w + 6); yy = y + (k // cols) * (h + 5)
        words, lines, cur = lb.replace("-Checked", "- Checked").split(), [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 17 and cur: lines.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines.append(cur)
        s += rect(x, yy, w, h, c + "14", c, 0, .9) + icon(ic, x + 5, yy + 7, 14, c, 2)
        s += "".join(t(x + 24, yy + (17 if len(lines) == 1 else 12 + li * 9), l, 7.5, c, "hind", 600) for li, l in enumerate(lines[:2]))
    return s
APPROVED = [("shield", "Certified Techs", TERRA), ("shield", "Licensed & Insured", LAGOON), ("id", "Background-Checked Yearly", JUNGLE), ("x", "Cancel Anytime", INK), ("report", "Home Reports", SAFFRON), ("meter", "Moisture Scan Every Visit", LAGOON)]
def pinned():
    s = grid(64, CORE[:6], lawn=False)
    s += rect(130, 112, 58, 12, LAGOON) + t(159, 121, "EVERY VISIT", 7, "#FFFFFF", "hind", 600, "middle")
    return s
pair("Trust Badges", "Approved Badges: A Row Under The Section, Or Pinned To The Items They Prove?",
 ("bdg_row", "Badge Row Under The Section", "All six approved badges in one strip below the grid.", "practical",
  card("Trust Badges", TERRA, ph(hdr() + grid(36, CORE[:3], lawn=False) + badge_row(98, APPROVED)) + foot(["All six", "One place"]))),
 ("bdg_pinned", "Pinned To Items", "Certified Techs and Licensed & Insured up top; Moisture Scan Every Visit on its tile.", "bold",
  card("Trust Badges", LAGOON, ph(hdr() + badge_row(30, APPROVED[:2]) + pinned() + badge_row(182, [APPROVED[4], APPROVED[3]])) + foot(["In context"]))))
# 10 extra site-backed badges (flags noted)
NEW_A = [("bell", "Recall Monitoring", TERRA), ("check", "Warranty Check", JUNGLE)]
NEW_B = [("pin", "Metro Detroit Area", LAGOON), ("refund", "Honest Refund", SAFFRON)]
pair("Trust Badges", "Add Two New Badges The Site Backs: Recall Monitoring And Warranty Check, Or Metro Detroit Area And Honest Refund?",
 ("bdg_new_records", "Recall Monitoring + Warranty Check", "Both are listed as included on every plan (Records).", "practical",
  card("New Badges", TERRA, ph(hdr() + grid(36, CORE[:3], lawn=False) + badge_row(98, APPROVED[:4]) + t(10, 176, "NEW, SITE-BACKED", 7.5, TERRA, "hind", 600) + badge_row(182, NEW_A) + rect(6, 166, 180, 48, "none", TERRA, 0, 1, 'stroke-dasharray="3 2"')) + foot(["New: 2", "Site-backed"]))),
 ("bdg_new_local", "Metro Detroit Area + Honest Refund", "Service area from the FAQ; refund from the Refund Promise (draft terms, Max to confirm).", "calm",
  card("New Badges", LAGOON, ph(hdr() + grid(36, CORE[:3], lawn=False) + badge_row(98, APPROVED[:4]) + t(10, 176, "NEW (REFUND: MAX TO CONFIRM)", 7.5, LAGOON, "hind", 600) + badge_row(182, NEW_B) + rect(6, 166, 180, 48, "none", LAGOON, 0, 1, 'stroke-dasharray="3 2"')) + foot(["New: 2", "Refund: confirm"]))))
