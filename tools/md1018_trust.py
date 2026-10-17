"""Smart Upkeep home page decks (report 1b): trust tag loop (settled: small looping carousel, random order, 'Background checked' and 'Licensed and insured',
text-only pills, nothing happens on tap, under the Free Quote button, one mixed row, Cancel anytime in the row) and the What We Take Care Of carousel
(settled: plain list rows, no tap-for-more, tighter spacing, See All under the cards, plan chips, fade-up + arrow nudge, two icons, Water first).
Not repeated: the live Card Colors And Finish deck (own colour per card, face, colour strength, icons, shadow, See All style, header, chip style,
background, dot colour) and the queued Looping Carousel And Random Order / Carousel, Season Strip And Map Pins decks."""
from md1018_kit import *
HERO = "Smart Upkeep Site Home Hero"; WW = "Smart Upkeep Site What We Take Care Of"
PEOPLE, PROOF, PROMISE = LAGOON, JUNGLE, TERRA
TAGS4 = ["Background checked", "Licensed and insured", "Report every visit", "Cancel anytime"]
COL4 = [PEOPLE, PEOPLE, PROOF, PROMISE]
def hero(extra, label="Smart Upkeep · Home, Phone"):
    return [("photo", 70, LAGOON, "house"), ("h", "Your home, taken care of.", 15), ("btn", "Free Quote", "fill", TERRA)] + list(extra)
def tg(tags=TAGS4, cols=COL4, fade=True, size=7.5): return ("pills", tags, cols, fade, size)
def T(label="Smart Upkeep · Home, Phone"): return label
def wwcard(x, y, name, rows, c, w=150, rowh=15, title_extra="", dotrow=False, rowc=INK):
    h = 30 + len(rows) * rowh + 6
    s = rect(x, y, w, h, "#FFFFFF", LINE, 12) + rect(x + 8, y + 8, 18, 18, c + "22", "none", 5) + t(x + 32, y + 21, name + title_extra, 10, c, "khand")
    yy = y + 30
    for r in rows:
        s += (dot(x + 36, yy + rowh / 2, 2.2, c) if dotrow else ln(yy, x + 32, x + w - 8, "#f0ebe3")) + t(x + (42 if dotrow else 32), yy + rowh / 2 + 3, r, 7.8, rowc)
        yy += rowh
    return s, h
CATS = [("Water", ["Water Heater", "Moisture Scan", "Gutters"], LAGOON), ("Heating & Cooling", ["Furnace", "AC", "Furnace Filters"], TERRA),
        ("Air & Safety", ["Smoke/CO", "Dryer Vent", "Moisture Readings"], SAFFRON), ("Outside", ["Gutters", "Roof", "Flashing"], JUNGLE)]
def ww(cards_x0=14, w=150, gap=8, n=3, extra=(), rowh=15, title_count=False, dotrow=False, rowc=None, hug=False, fw=None):
    s = t(14, 16, "What We Take Care Of", 13, INK, "khand"); mh = 0
    for i, (nm, rows, c) in enumerate(CATS[:n]):
        rr = rows[:2] if (hug and i == 1) else rows
        g, h = wwcard(cards_x0 + i * (w + gap), 26, nm, rr, c, w, rowh, f"  ·  {len(rr)}" if title_count else "", dotrow, (c if rowc == "cat" else INK)); s += g; mh = max(mh, h)
    return [("raw", s, 26 + mh + 6)] + list(extra)
def T_A():
    pairs, P = make("md18tt_", "UpKeep"); L = "Smart Upkeep · Home, Phone"
    P("Trust Tags", HERO, "Tag casing", "should the loop read in sentence case like Background checked or in title case like Background Checked?",
      ("sentence", "Sentence Case", "Background checked, Licensed and insured.", "calm", S(L, hero([tg()]), ("Reads like a quiet fact", "As you wrote it"))),
      ("title", "Title Case", "Background Checked, Licensed And Insured.", "focused", S(L, hero([tg(["Background Checked", "Licensed And Insured", "Report Every Visit"])]), ("Reads like a badge", "Matches the deck names"))))
    P("Trust Tags", HERO, "Tags in the loop", "should the loop carry four tags or six?",
      ("four", "Four Tags", "People, proof and promise, nothing more.", "calm", S(L, hero([tg(), ("p", "Loop: Background checked, Licensed and insured, Report every visit, Cancel anytime")]), ("Short loop, each tag seen often", ""))),
      ("six", "Six Tags", "Adds Moisture scan every visit and Same-week visits.", "practical", S(L, hero([tg(TAGS4[:2] + ["Moisture scan every visit", "Same-week visits"], [PEOPLE, PEOPLE, PROOF, PROMISE]), ("p", "Loop adds: Moisture scan every visit, Same-week visits")]), ("More reasons in the same row", "Longer loop"))))
    P("Trust Tags", HERO, "Category colours", "should each tag take its category colour (people lagoon, proof green, promise terracotta) or should every tag share one quiet ink outline?",
      ("cat", "Colour By Category", "People lagoon, proof jungle green, promise terracotta.", "playful", S(L, hero([tg(), ("raw", t(14, 9, "People", 7.5, PEOPLE, "hind", 600) + t(60, 9, "Proof", 7.5, PROOF, "hind", 600) + t(100, 9, "Promise", 7.5, PROMISE, "hind", 600), 14)]), ("Colour tells the kind of promise", "Soft tints, never neon"))),
      ("ink", "One Quiet Ink Outline", "Every tag the same thin ink outline.", "calm", S(L, hero([tg(cols=[INK])]), ("Calm under the button", "Colour stays on the button"))))
    P("Trust Tags", HERO, "Loop direction", "should the tags drift from right to left or from left to right?",
      ("rtl", "Right To Left", "New tags come in from the right edge.", "calm", S(L, hero([tg(), ("raw", t(120, 9, "drifts this way  \u2190", 7.5, LAGOON, "hind", 600, "middle"), 14)]), ("Like reading on", "Next tag appears where the eye goes"))),
      ("ltr", "Left To Right", "New tags come in from the left edge.", "playful", S(L, hero([tg(list(reversed(TAGS4)), list(reversed(COL4))), ("raw", t(120, 9, "\u2192  drifts this way", 7.5, LAGOON, "hind", 600, "middle"), 14)]), ("Moves toward the scroll", "Feels a little different"))))
    P("Trust Tags", HERO, "Less motion setting", "when a phone asks for less motion should the loop stop and wrap the tags onto two still lines or step slowly once every few seconds?",
      ("wrap", "Stop And Wrap", "All tags sit still on two lines.", "calm", S(L, hero([("pills", TAGS4[:2], COL4[:2], False), ("pills", TAGS4[2:], COL4[2:], False)]), ("Nothing moves at all", "Every tag still visible"))),
      ("step", "Step Slowly", "One small step every five seconds, no drift.", "practical", S(L, hero([tg(), ("raw", t(120, 9, "steps every 5 seconds", 7.5, MUTE, "hind", 600, "middle"), 14)]), ("Gentle movement only", "Still one row"))))
    P("Trust Tags", HERO, "Desktop loop", "on a wide screen should the loop keep running or show all the tags in one still row?",
      ("run", "Keeps Running", "Same small loop as the phone.", "playful", S("Smart Upkeep · Home, 1280", [("desk", t(10, 30, "Your home, taken care of.", 14, INK, "khand") + rect(10, 40, 70, 14, TERRA, "none", 3) + BLK["pills"](64, TAGS4 + TAGS4[:1], COL4, True, 6.5, 5, 10)[0], 110)], ("Same feel on every screen", ""))),
      ("still", "One Still Row", "All tags fit, so nothing moves.", "calm", S("Smart Upkeep · Home, 1280", [("desk", t(10, 30, "Your home, taken care of.", 14, INK, "khand") + rect(10, 40, 70, 14, TERRA, "none", 3) + BLK["pills"](64, TAGS4, COL4, False, 6.5, 5, 10)[0], 110)], ("Room for every tag", "Loop only where it is needed"))))
    P("Trust Tags", HERO, "Tag size", "should the tags be extra small at 12px or small at 14px?",
      ("12", "Extra Small, 12px", "A slim row that never competes with the button.", "calm", S(L, hero([tg(size=6.5)]), ("Slimmer row", "More tags in view"))),
      ("14", "Small, 14px", "Easier to read at arm's length.", "practical", S(L, hero([tg(size=8.5)]), ("Easier to read", "Fewer tags in view"))))
    P("Trust Tags", HERO, "Loop seam", "should the tags repeat seamlessly or leave a short gap after the full set before it starts again?",
      ("seam", "Seamless Repeat", "The first tag follows the last with the same gap.", "calm", S(L, hero([tg(TAGS4 + TAGS4[:1], COL4)]), ("Never stops", "No visible start"))),
      ("gap", "Short Gap After The Set", "A wider pause shows where the set ends.", "practical", S(L, hero([("pills", TAGS4[2:] + ["", ""], COL4[2:] + [CREAM, CREAM], True)]), ("Reads as a full set", "Then it starts again"))))
    P("Trust Tags", "Smart Upkeep Site Sign Up Form", "Trust loop on the form", "should the same small tag loop also run just above the Continue button on the sign-up form or stay on the home page only?",
      ("form", "Also Above Continue", "The loop rides just above the form's button.", "practical", S("Smart Upkeep · Sign Up, Phone", [("h", "Your Home", 14), ("input", "Street address", LAGOON, "home"), ("input", "Email", LAGOON, "search"), tg(), ("btn", "Continue", "fill", TERRA)], ("Reassures at the decision", "Same tags, same order rule"))),
      ("home", "Home Page Only", "The form stays plain.", "calm", S("Smart Upkeep · Sign Up, Phone", [("h", "Your Home", 14), ("input", "Street address", LAGOON, "home"), ("input", "Email", LAGOON, "search"), ("btn", "Continue", "fill", TERRA)], ("Nothing moves on the form", "Fewer distractions"))))
    P("Trust Tags", HERO, "Rows in the loop", "should the loop be one row or two thin rows drifting in opposite directions?",
      ("one", "One Row", "One small row under the button.", "calm", S(L, hero([tg()]), ("Small and simple", ""))),
      ("two", "Two Rows, Opposite Ways", "People tags one way, proof and promise the other.", "playful", S(L, hero([tg(TAGS4[:2] + TAGS4[:1], [PEOPLE]), tg(TAGS4[2:] + TAGS4[2:3], [PROOF, PROMISE])]), ("More motion, more tags seen", "Taller strip"))))
    return pairs
def T_B():
    pairs, P = make("md18tw2_", "UpKeep"); L = "Smart Upkeep · Care Cards, Phone"
    P("Care Carousel", WW, "Moving on its own", "should the care cards loop on their own like the trust tags or move only when swiped?",
      ("auto", "Loops On Its Own", "A card slides over every few seconds.", "playful", S(L, ww(extra=[("cdots", 4, 0, True)]), ("Like the trust tags", "Stops when you touch it"))),
      ("swipe", "Only When Swiped", "Cards sit still until a finger moves them.", "calm", S(L, ww(extra=[("cdots", 4, 0, False)]), ("Calm section", "Visitor sets the pace"))))
    P("Care Carousel", WW, "Next card peek", "should only a slim edge of the next card show or a wide slice of it?",
      ("slim", "Slim Edge", "About a finger's width of the next card.", "calm", S(L, ww(w=190), ("Current card reads big", "Hint that more cards follow"))),
      ("wide", "Wide Slice", "About a third of the next card shows.", "playful", S(L, ww(w=135), ("Clearly a carousel", "Next category readable"))))
    P("Care Carousel", WW, "Wide screen", "on a 1280 screen should three cards show with arrows or all four cards sit in one row?",
      ("three", "Three Cards And Arrows", "Still a carousel on desktop.", "playful", S("Smart Upkeep · Care Cards, 1280", [("desk", "".join(wwcard(i * 64, 0, n, r[:3], c, 60, 12)[0] for i, (n, r, c) in enumerate(CATS[:3])) + f'<circle cx="203" cy="40" r="8" fill="#FFFFFF" stroke="{TERRA}"/>', 110)], ("Same carousel everywhere", "Arrow for the fourth card"))),
      ("four", "All Four In A Row", "Nothing to swipe on a wide screen.", "calm", S("Smart Upkeep · Care Cards, 1280", [("desk", "".join(wwcard(i * 50, 0, n.split(" ")[0], r[:3], c, 47, 12)[0] for i, (n, r, c) in enumerate(CATS)), 110)], ("Everything at once", "Carousel on phones only"))))
    P("Care Carousel", WW, "Position marker", "should the card position show as small dots or as a 2 of 4 count?",
      ("dots", "Small Dots (As Now)", "Four dots, the current one long.", "calm", S(L, ww(extra=[("cdots", 4, 0)]), ("Quiet marker", ""))),
      ("count", "Two Of Four Count", "Small grey 2 / 4 under the cards.", "practical", S(L, ww(extra=[("raw", t(120, 10, "2 / 4", 8.5, MUTE, "hind", 600, "middle"), 16)]), ("Says exactly how many", "No dots"))))
    P("Care Carousel", WW, "Last card", "after the last card should the carousel wrap back to the first card or stop at the end?",
      ("wrap", "Wraps To The First", "Endless loop, Outside leads back to Water.", "playful", S(L, ww(extra=[("raw", t(120, 10, "Outside  \u2192  Water  \u2192  Heating", 8, LAGOON, "hind", 600, "middle"), 16)]), ("Never hits a wall", "Matches the trust loop"))),
      ("stop", "Stops At The End", "The last card sits flush; swipe back to return.", "calm", S(L, ww(extra=[("raw", t(120, 10, "End of the cards", 8, MUTE, "hind", 600, "middle"), 16)]), ("Clear start and end", "See All under it"))))
    P("Care Carousel", WW, "Card height", "should every card share the same height or should each card fit its own rows?",
      ("same", "All The Same Height", "Short cards get a little white space.", "calm", S(L, ww(), ("Tidy row of cards", ""))),
      ("hug", "Each Fits Its Rows", "A card with fewer rows is shorter.", "practical", S(L, ww(hug=True), ("No empty space", "Edges step up and down"))))
    P("Care Carousel", WW, "Desktop arrows", "should the desktop arrows sit as round buttons on the card sides or as small arrows beside the dots?",
      ("sides", "Round Arrows On The Sides", "Big round arrows over the card edges.", "practical", S("Smart Upkeep · Care Cards, 1280", [("desk", "".join(wwcard(10 + i * 64, 0, n, r, c, 60, 12)[0] for i, (n, r, c) in enumerate(CATS[:3])) + "".join(f'<circle cx="{x}" cy="40" r="8" fill="#FFFFFF" stroke="{TERRA}"/>' for x in (6, 202)), 110)], ("Easy to hit with a mouse", ""))),
      ("dots", "Small Arrows By The Dots", "Arrows sit under the cards with the dots.", "calm", S("Smart Upkeep · Care Cards, 1280", [("desk", "".join(wwcard(10 + i * 64, 0, n, r, c, 60, 12)[0] for i, (n, r, c) in enumerate(CATS[:3])) + t(95, 92, "\u2039   \u2022 \u2022 \u2022 \u2022   \u203a", 9, TERRA, "hind", 600, "middle"), 110)], ("Cards stay clear", "Controls in one place"))))
    P("Care Carousel", WW, "Swipe stop", "should one swipe move exactly one card or let the cards glide freely?",
      ("one", "One Card Per Swipe", "Each swipe lands on the next card.", "calm", S(L, ww(extra=[("raw", t(120, 10, "snaps to each card", 8, MUTE, "hind", 600, "middle"), 16)]), ("Always lands neatly", ""))),
      ("free", "Glide Freely", "A hard flick can pass two cards.", "playful", S(L, ww(cards_x0=-40, extra=[("raw", t(120, 10, "glides and slows down", 8, MUTE, "hind", 600, "middle"), 16)]), ("Feels quick", "May stop between cards"))))
    P("Care Carousel", WW, "After a swipe", "if the cards loop on their own should a visitor's swipe pause the loop for good or let it carry on after a few seconds?",
      ("stop", "Pause For Good", "Once touched, the visitor is in control.", "calm", S(L, ww(extra=[("note", "Touched once: loop stays paused", "")]), ("Never moves under a finger", ""))),
      ("resume", "Carry On After A Few Seconds", "The loop picks up again after five seconds.", "playful", S(L, ww(extra=[("note", "Loop resumes after 5 seconds", "")]), ("Keeps showing every card", ""))))
    P("Care Carousel", WW, "Card title", "should each card show the category name alone or the name with its service count?",
      ("name", "Name Alone (As Now)", "Water, Heating & Cooling, Air & Safety.", "calm", S(L, ww(), ("Clean title", ""))),
      ("count", "Name And Count", "Water  ·  3 shows how many services.", "practical", S(L, ww(title_count=True), ("How much is covered", "Small grey count"))))
    return pairs
def T_C():
    pairs, P = make("md18tc2_", "UpKeep"); L = "Smart Upkeep · Home, Phone"; HP = "Smart Upkeep Site Home Page"
    P("Home Page", HP, "Shared colours", "should the care cards use the same category colours as the trust tags or keep their own colours?",
      ("shared", "Same Colours As The Tags", "Lagoon, green and terracotta mean the same everywhere.", "focused", S(L, [tg()] + ww(), ("One colour language", "Tags and cards agree"))),
      ("own", "Own Colours", "Cards keep their colours; tags keep theirs.", "calm", S(L, [tg(cols=[INK])] + ww(), ("Each section on its own", ""))))
    P("Home Page", HP, "Two loops at once", "if both sections loop should the care cards wait until the trust tags scroll out of view or should both move at once?",
      ("wait", "Care Cards Wait", "Only one thing moves on screen at a time.", "calm", S(L, [tg(), ("note", "Care cards start when the tags leave the screen", "")] + ww(), ("Calm screen", ""))),
      ("both", "Both Move", "Tags drift while the cards slide.", "playful", S(L, [tg(), ("note", "Both loops run together", "")] + ww(), ("Lively page", "More motion"))))
    P("Home Page", WW, "Plan chips with card colours", "with every card in its own colour should the Essentials, Plus and Complete chips turn neutral grey or keep their plan colours?",
      ("grey", "Neutral Grey Chips", "Chips stop competing with the card colour.", "calm", S(L, ww(extra=[("pills", ["Essentials", "Plus", "Complete"], ["#7A746A"], False)]), ("Card colour stays the hero", ""))),
      ("plan", "Keep Plan Colours", "Green, blue and terracotta chips as now.", "practical", S(L, ww(extra=[("pills", ["Essentials", "Plus", "Complete"], [JUNGLE, LAGOON, TERRA], False)]), ("Plans read at a glance", "More colour per card"))))
    P("Home Page", WW, "Row marker", "should the plain service rows keep thin divider lines or use a small dot in the card colour before each name?",
      ("lines", "Thin Lines (As Now)", "A hairline between rows.", "calm", S(L, ww(), ("Quiet list", ""))),
      ("dots", "Small Coloured Dots", "A dot in the card colour starts each row.", "playful", S(L, ww(dotrow=True), ("Carries the card colour", "Still a plain list"))))
    P("Home Page", WW, "Service name colour", "should the service names stay ink or take the card's colour?",
      ("ink", "Ink Names (As Now)", "Dark names, colour on the title only.", "calm", S(L, ww(), ("Easiest to read", ""))),
      ("cat", "Names In The Card Colour", "Rows in a deeper shade of the card colour.", "playful", S(L, ww(rowc="cat"), ("Whole card in its colour", "Softer contrast"))))
    P("Home Page", WW, "Card width on a phone", "should each card be about three quarters of the screen wide or nearly the full width?",
      ("34", "About Three Quarters", "The next card peeks in beside it.", "playful", S(L, ww(w=150), ("Carousel is obvious", ""))),
      ("full", "Nearly Full Width", "One card fills the row; dots show more.", "calm", S(L, ww(w=200, n=2, extra=[("cdots", 4, 0)]), ("Rows read easily", "Less peek"))))
    P("Home Page", WW, "First-visit map line", "should one plain line under the cards say your tech maps your home on the first visit or should the section end at See All?",
      ("line", "Add The Map Line", "First visit: your tech maps your home so later visits go faster.", "practical", S(L, ww(extra=[("raw", t(120, 10, "See All", 9, LAGOON, "hind", 600, "middle", 'text-decoration="underline"'), 18), ("note", "Your tech maps your home on the first visit", "So every visit after is faster")]), ("Says what the first visit does", ""))),
      ("end", "End At See All", "No extra line.", "calm", S(L, ww(extra=[("raw", t(120, 10, "See All", 9, LAGOON, "hind", 600, "middle", 'text-decoration="underline"'), 18)]), ("Shorter section", ""))))
    P("Home Page", WW, "First card position", "should the first card start at the page margin or sit centred with both neighbours peeking?",
      ("margin", "Starts At The Margin", "Lines up with the heading above it.", "calm", S(L, ww(), ("Edges line up", ""))),
      ("centre", "Centred, Both Sides Peek", "Last card peeks left, next card peeks right.", "playful", S(L, ww(cards_x0=-90, w=150), ("Looks like a loop", ""))))
    P("Home Page", WW, "Card corners", "should the care cards keep their 14px corners or match the 10px corners used on deck cards?",
      ("14", "Softer 14px (As Now)", "Rounder cards, as on the site today.", "calm", S(L, ww(), ("Friendly and soft", ""))),
      ("10", "Tighter 10px", "Slightly crisper corners.", "focused", S(L, [("raw", "".join(wwcard(14 + i * 158, 0, n, r, c, 150, 15)[0].replace('rx="12"', 'rx="7"') for i, (n, r, c) in enumerate(CATS[:2])), 90)], ("Crisper, matches the decks", ""))))
    P("Home Page", "Smart Upkeep Site See All Page", "See All list", "should the See All page list every service grouped under its category or as one A to Z list?",
      ("grouped", "Grouped By Category", "Water, Heating & Cooling, Air & Safety, Outside.", "calm", S("Smart Upkeep · See All, Phone", [("h", "Everything We Take Care Of", 13), ("lbl", "WATER", LAGOON), ("table", [("Water Heater", "Essentials"), ("Moisture Scan", "Essentials")]), ("lbl", "HEATING & COOLING", TERRA), ("table", [("Furnace", "Essentials"), ("AC", "Essentials")])], ("Same groups as the cards", ""))),
      ("az", "One A To Z List", "Every service in one alphabetical list.", "practical", S("Smart Upkeep · See All, Phone", [("h", "Everything We Take Care Of", 13), ("table", [("AC", "Essentials"), ("Dryer Vent", "Essentials"), ("Flashing", "Complete"), ("Furnace", "Essentials"), ("Gutters", "Plus"), ("Moisture Scan", "Essentials"), ("Roof", "Complete")])], ("Find any service fast", ""))))
    return pairs
