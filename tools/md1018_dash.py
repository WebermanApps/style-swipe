"""Dashboard kit decks for the Branding board (report topic 2: 'How about carousel??' on the phone deck board, audio without tapping the tile).
Left out on purpose: Share placement, Apps Home, anything already in Main Dashboard Rules / All Boards Rules / Header And Footer Details, and
settled results (five across, ring 3/10, newest first, grey cross, NEW tag, leaves instantly, text link return, wide peek with dots vs slim
peek with counter which is still open on Main Deck Board Polish, saving results which is pending for Monday)."""
from md1018_kit import *
def deckcard(x, y, w, h, title, c, ring=True, thumb=True):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 10) + rect(x, y, w, 4, c, "none", 2)
    if thumb: s += photo(x + 8, y + 10, w - 16, h * .42, c, "house")
    ty = y + (h * .42 + 24 if thumb else 22)
    s += t(x + 8, ty, title, 9, INK, "khand") + t(x + 8, ty + 11, "10 picks", 7, MUTE)
    if ring: s += f'<circle cx="{x+w-14}" cy="{ty-3}" r="6" fill="none" stroke="#E5E0D8" stroke-width="2"/><path d="M{x+w-14} {ty-9} a6 6 0 0 1 5.2 3" fill="none" stroke="{JUNGLE}" stroke-width="2"/>'
    return s
def strip(y=0, w=120, h=120, n=3, x0=14, thumb=True, names=("Card Colors", "Trust Tags", "Forecast App")):
    return "".join(deckcard(x0 + i * (w + 8), y, w, h, names[i % 3], ACC[i % 4], True, thumb) for i in range(n))
def head(title="Max's Picks", right="See all"):
    return t(14, 12, title, 13, INK, "khand") + t(226, 12, right, 8, LAGOON, "hind", 600, "end")
def T_D1():
    pairs, P = make("md18dp_", "Branding Board"); L = "Branding Board · Phone"; MP = "Branding Board Max's Picks"
    def mp(extra="", w=120, h=120, thumb=True, n=3, x0=14, title="Max's Picks", right="See all", hh=150):
        return [("raw", head(title, right) + strip(22, w, h, n, x0, thumb) + extra, hh)]
    P("Phone Board", MP, "Max's Picks on a phone", "should Max's Picks on a phone become a swipe carousel or stay a stacked list?",
      ("car", "Swipe Carousel", "Cards in a row, next one peeking in.", "playful", S(L, mp() + [("cdots", 4, 0)], ("Your carousel idea", "Short page"))),
      ("list", "Stacked List", "One deck per row, scroll down.", "calm", S(L, [("raw", head(), 18), ("cards", [("Card Colors", "10 picks"), ("Trust Tags", "10 picks"), ("Forecast App", "10 picks")], [TERRA, LAGOON, JUNGLE])], ("Everything in view", "Longer page"))))
    P("Phone Board", MP, "Card size in the row", "should each card take about two thirds of the screen or about half so two and a bit show?",
      ("big", "Two Thirds Wide", "One big card and the edge of the next.", "focused", S(L, mp(w=160, h=130, hh=160), ("Bigger pictures", ""))),
      ("half", "About Half Wide", "Two cards and a sliver of the third.", "practical", S(L, mp(w=100, h=110, n=3, hh=140), ("More decks at a glance", ""))))
    P("Phone Board", MP, "Card picture", "should each card show a small drawn picture from the deck or only the deck name and progress?",
      ("pic", "Small Picture", "The deck's first drawing on top.", "playful", S(L, mp(), ("Easy to spot a deck", ""))),
      ("text", "Name And Progress Only", "Shorter cards, words only.", "calm", S(L, mp(h=56, thumb=False, hh=86), ("Compact row", ""))))
    P("Phone Board", MP, "Where cards stop", "after a swipe should the card stop in the centre or snap to the left edge?",
      ("centre", "Stop In The Centre", "A card peeks on both sides.", "playful", S(L, mp(x0=-46, w=110, hh=150), ("Feels like a carousel", ""))),
      ("left", "Snap To The Left", "Lined up with the heading.", "calm", S(L, mp(), ("Lines up with the page", ""))))
    P("Phone Board", MP, "End of the row", "at the end of the row should the last card be a See All card or should the row simply stop?",
      ("all", "See All Card", "A last card that opens the full list.", "practical", S(L, [("raw", head() + deckcard(-60, 22, 120, 120, "Forecast App", JUNGLE) + rect(68, 22, 120, 120, CREAM, LINE, 10) + t(128, 86, "See all 9", 11, TERRA, "khand", anchor="middle"), 150)], ("A way onward", ""))),
      ("stop", "Row Just Stops", "The last deck card ends the row.", "calm", S(L, [("raw", head() + deckcard(-60, 22, 120, 120, "Card Colors", TERRA) + deckcard(68, 22, 120, 120, "Forecast App", JUNGLE), 150)], ("Nothing extra", ""))))
    P("Phone Board", MP, "Swipe hint", "the first time on a phone should the row nudge sideways once to show it swipes or should the peeking card be the only hint?",
      ("nudge", "One Small Nudge", "The row slides a little and back, once.", "playful", S(L, mp(extra=t(120, 156, "\u2190  nudges once", 8, LAGOON, "hind", 600, "middle"), hh=164), ("Nobody misses it", ""))),
      ("peek", "Peek Only", "The cut-off card is the hint.", "calm", S(L, mp(), ("Nothing moves by itself", ""))))
    P("Phone Board", MP, "Heading row", "should the heading row show a count like 9 decks or a See All link?",
      ("count", "Count Like 9 Decks", "How many are waiting, no link.", "calm", S(L, mp(right="9 decks"), ("Know how many", ""))),
      ("link", "See All Link", "A link to the full list.", "practical", S(L, mp(right="See all"), ("Quick way to everything", ""))))
    P("Phone Board", "Branding Board Ready To Swipe", "Same carousel below", "should Ready To Swipe on a phone use the same carousel as Max's Picks or stay a list under it?",
      ("same", "Same Carousel", "Both rows swipe sideways.", "playful", S(L, mp(h=80, thumb=False, hh=110) + [("raw", head("Ready To Swipe", "See all") + strip(22, 120, 56, 3, 14, False), 86)], ("One way to move", ""))),
      ("list", "List Under It", "Picks swipe, Ready To Swipe scrolls down.", "calm", S(L, mp(h=80, thumb=False, hh=110) + [("raw", head("Ready To Swipe", ""), 18), ("cards", [("Pitch App", "10 picks"), ("Sign Up Form", "10 picks")], [LAGOON, JUNGLE])], ("Clear difference", ""))))
    P("Phone Board", MP, "Tap to open", "should tapping a card open the deck straight away or first grow the card with a Start button?",
      ("open", "Open Straight Away", "One tap and you are swiping.", "focused", S(L, mp(), ("Fastest", ""))),
      ("grow", "Grow With Start", "The card grows, shows its picks count, then Start.", "calm", S(L, [("raw", head() + rect(14, 22, 212, 150, "#FFFFFF", TERRA, 10) + photo(24, 32, 192, 70, TERRA, "house") + t(24, 122, "Card Colors And Finish", 11, INK, "khand") + t(24, 136, "10 picks · about 3 minutes", 7.5, MUTE), 176), ("btn", "Start", "fill", TERRA)], ("See before you start", ""))))
    P("Phone Board", "Branding Board Deck Card", "Audio on the card", "should the play-audio button sit on the card itself so it plays without opening, or only inside the deck?",
      ("card", "On The Card", "A small play circle in the card corner.", "practical", S(L, mp(extra=f'<circle cx="118" cy="40" r="9" fill="#FFFFFF" stroke="{TERRA}" stroke-width="1.4"/>' + ic("play", 111, 33, 14, TERRA)), ("Listen without opening", "Your no-tap ask"))),
      ("inside", "Inside The Deck Only", "Cards stay clean; play once open.", "calm", S(L, mp(), ("Calmer cards", ""))))
    return pairs
def kitcar(y=0, n=3, w=150, h=70, extra=""):
    return "".join(rect(14 + i * (w + 8), y, w, h, "#FFFFFF", LINE, 10) + rect(14 + i * (w + 8), y, w, 4, ACC[i % 4], "none", 2) + t(24 + i * (w + 8), y + 24, ["Agent Update", "Open Item", "Swipe Data"][i % 3], 9.5, INK, "khand") + t(24 + i * (w + 8), y + 37, "card text", 7.5, MUTE) for i in range(n)) + extra
def T_D2():
    pairs, P = make("md18dk_", "Branding Board"); L = "Dashboard Kit · Phone"; K = "Dashboard Kit Carousels"
    P("Kit Carousel", K, "Position marker", "for every kit carousel should the marker under the cards be small dots or a thin progress line?",
      ("dots", "Small Dots", "One dot per card.", "calm", S(L, [("raw", kitcar(), 76), ("cdots", 5, 0)], ("Counts the cards", ""))),
      ("line", "Thin Progress Line", "A line that fills as you swipe.", "practical", S(L, [("raw", kitcar() + rect(14, 82, 212, 3, "#E5E0D8", "none", 1.5) + rect(14, 82, 60, 3, TERRA, "none", 1.5), 92)], ("Works for long rows", ""))))
    P("Kit Carousel", "Dashboard Kit Carousels · 1280", "Desktop arrows", "on a laptop should kit carousels show round arrows at both ends or only show them when the mouse is over the row?",
      ("always", "Arrows Always Showing", "Round arrows at both ends.", "practical", S("Dashboard Kit · 1280", [("desk", kitcar(10, 3, 58, 50).replace('x="14"', 'x="14"') + f'<circle cx="8" cy="35" r="7" fill="#FFFFFF" stroke="{TERRA}"/><circle cx="198" cy="35" r="7" fill="#FFFFFF" stroke="{TERRA}"/>', 90)], ("Obvious with a mouse", ""))),
      ("hover", "Arrows On Hover", "Arrows fade in when the mouse is over.", "calm", S("Dashboard Kit · 1280", [("desk", kitcar(10, 3, 58, 50), 90), ("p", "Arrows appear on hover", 46, MUTE, True)], ("Clean until needed", ""))))
    P("Kit Carousel", K, "Moving on its own", "should kit carousels ever move on their own or only when swiped?",
      ("swipe", "Only When Swiped", "Nothing moves until you move it.", "calm", S(L, [("raw", kitcar(), 76), ("cdots", 4, 0)], ("Calm boards", ""))),
      ("auto", "Slow Loop Where It Helps", "Rows of tips or tags may loop slowly.", "playful", S(L, [("raw", kitcar(), 76), ("cdots", 4, 0, True)], ("Livelier boards", ""))))
    P("Kit Carousel", K, "Next card peek", "how much of the next card should peek in on a phone?",
      ("slim", "A Slim Edge", "About a tenth of the next card.", "calm", S(L, [("raw", kitcar(0, 2, 196), 76)], ("Current card reads big", ""))),
      ("third", "About A Third", "Enough to read its title.", "practical", S(L, [("raw", kitcar(0, 2, 140), 76)], ("Clearly a carousel", ""))))
    P("Kit Carousel", K, "Less motion", "when a phone is set to reduce motion should kit carousels turn into a plain stacked list or keep swiping with no sliding animation?",
      ("list", "Plain Stacked List", "Cards stack top to bottom.", "calm", S(L, [("cards", [("Agent Update", "card text"), ("Open Item", "card text"), ("Swipe Data", "card text")], [TERRA, LAGOON, JUNGLE])], ("Nothing moves at all", ""))),
      ("snap", "Swipe Without Sliding", "Cards jump instead of glide.", "practical", S(L, [("raw", kitcar(), 76), ("cdots", 4, 0)], ("Same layout for everyone", ""))))
    P("Kit Carousel", "Dashboard Kit To-Do", "To-do on a phone", "should the To-Do section on a phone become a swipe carousel of task cards or stay a checklist?",
      ("car", "Task Card Carousel", "One task per card, swipe for the next.", "playful", S(L, [("h", "To-Do", 14), ("carousel", [("Answer 2 decks", "Today", TERRA), ("Read the report", "Today", LAGOON), ("Review attire", "This week", JUNGLE)], 150, 70)], ("One thing at a time", ""))),
      ("check", "Checklist", "Tick boxes down the page.", "calm", S(L, [("h", "To-Do", 14), ("checks", ["Answer 2 decks", "Read the report", "Review attire"], JUNGLE, 1)], ("See every task", ""))))
    P("Kit Carousel", "Dashboard Kit Document Center", "Documents on a phone", "should the Document Center on a phone show recent documents as a carousel of covers or as a list of names?",
      ("covers", "Carousel Of Covers", "Little document covers you swipe.", "playful", S(L, [("h", "Documents", 14), ("carousel", [("Checkout Notes", "PDF", LAGOON), ("Tech Certs", "PDF", JUNGLE), ("Cool Tech", "PDF", TERRA)], 110, 100, True, False, 0, True, None, False, "photo")], ("Spot a document by look", ""))),
      ("list", "List Of Names", "Name, type and date per row.", "calm", S(L, [("h", "Documents", 14), ("table", [("Checkout Notes", "PDF"), ("Tech Certs", "PDF"), ("Cool Tech", "PDF")])], ("Quick to scan", ""))))
    P("Kit Carousel", K, "Card count", "should each kit carousel cap at about six cards with a See All card or show every card?",
      ("cap", "Six Then See All", "A See All card after six.", "practical", S(L, [("raw", kitcar(0, 1) + rect(172, 0, 150, 70, CREAM, LINE, 10) + t(184, 40, "See all 14", 10, TERRA, "khand"), 76)], ("Short rows", ""))),
      ("all", "Every Card", "The row holds everything.", "calm", S(L, [("raw", kitcar(), 76), ("p", "1 of 14", 46, MUTE, True)], ("Nothing hidden", ""))))
    P("Kit Carousel", K, "Card height", "should cards in one carousel all match the tallest card or each fit its own text?",
      ("same", "All The Same Height", "A tidy row.", "calm", S(L, [("raw", kitcar(0, 2, 150, 80), 86)], ("Tidy row", ""))),
      ("fit", "Each Fits Its Text", "Short cards stay short.", "practical", S(L, [("raw", rect(14, 0, 150, 80, "#FFFFFF", LINE, 10) + t(24, 24, "Agent Update", 9.5, INK, "khand") + rect(172, 0, 150, 50, "#FFFFFF", LINE, 10) + t(182, 24, "Open Item", 9.5, INK, "khand"), 86)], ("No empty space", ""))))
    P("Kit Carousel", K, "Section title", "should each carousel's section title sit above the row with a count or inside the first card?",
      ("above", "Title Above With Count", "Agent Updates · 6 above the row.", "calm", S(L, [("raw", t(14, 12, "Agent Updates  ·  6", 12, INK, "khand") + kitcar(20), 96)], ("Standard heading", ""))),
      ("first", "Inside The First Card", "A coloured first card names the row.", "playful", S(L, [("raw", rect(14, 0, 90, 70, CREAM, "none", 10) + t(24, 30, "Agent", 12, TERRA, "khand") + t(24, 44, "Updates", 12, TERRA, "khand") + "".join(rect(112 + i * 128, 0, 120, 70, "#FFFFFF", LINE, 10) + t(122 + i * 128, 24, ["Research", "WellNest"][i], 9.5, INK, "khand") + t(122 + i * 128, 37, "card text", 7.5, MUTE) for i in range(2)), 76)], ("Saves a line", ""))))
    return pairs
def T_D3():
    pairs, P = make("md18dm_", "Branding Board"); L = "Dashboard Kit · Phone"
    def car(names, w=150, h=70): return ("carousel", [(n, s, ACC[i % 4]) for i, (n, s) in enumerate(names)], w, h)
    U = [("Research", "2 new decks"), ("WellNest", "Tea ideas ready"), ("Legal", "Questions ready")]
    P("Phone Sections", "Dashboard Kit Agent Updates", "Agent updates", "on a phone should agent updates be a swipe carousel of cards or a short list?",
      ("car", "Update Carousel", "One agent per card.", "playful", S(L, [("h", "Agent Updates", 14), car(U)], ("Fits a small screen", ""))),
      ("list", "Short List", "Three lines and More.", "calm", S(L, [("h", "Agent Updates", 14), ("cards", U, [TERRA, LAGOON, JUNGLE])], ("Read top to bottom", ""))))
    P("Phone Sections", "Dashboard Kit Open Items", "Now, this week, later", "on a phone should the Now, This Week and Later columns become a carousel of three panels or tabs?",
      ("car", "Three Panel Carousel", "Swipe from Now to This Week to Later.", "playful", S(L, [car([("Now", "3 items"), ("This Week", "5 items"), ("Later", "8 items")], 170, 90)], ("Same columns, swiped", ""))),
      ("tabs", "Tabs", "Now, This Week, Later tabs over one list.", "calm", S(L, [("tabs", ["Now", "This Week", "Later"], "line"), ("checks", ["Answer decks", "Read report", "Pick attire"], JUNGLE, 0)], ("One list at a time", ""))))
    P("Phone Sections", "Dashboard Kit Swipe Data", "Swipe data stats", "on a phone should swipe data stats be a carousel of big-number cards or a two by two grid?",
      ("car", "Big-Number Carousel", "One stat per card.", "playful", S(L, [("h", "Swipe Data", 14), car([("42 answered", "this week"), ("6 open", "decks"), ("3 min", "per deck")], 120, 70)], ("Each number stands out", ""))),
      ("grid", "Two By Two Grid", "Four stats at once.", "calm", S(L, [("h", "Swipe Data", 14), ("tiles", [("42 answered", "check"), ("6 open", "card"), ("3 min", "clock"), ("9 agents", "star")], 2, 56)], ("All in one look", ""))))
    P("Phone Sections", "Dashboard Kit Team Feed", "Team feed", "on a phone should the team feed show the newest few as a carousel or stay a scrolling feed?",
      ("car", "Newest As A Carousel", "Latest five, swipe across.", "playful", S(L, [("h", "Team Feed", 14), car([("Decks built", "3:30 AM"), ("Report ready", "2:10 AM"), ("Shelf updated", "1:05 AM")])], ("Short page", ""))),
      ("feed", "Scrolling Feed", "Newest first, scroll down.", "calm", S(L, [("h", "Team Feed", 14), ("timeline", [("Decks built", "3:30 AM"), ("Report ready", "2:10 AM"), ("Shelf updated", "1:05 AM")])], ("Full story", ""))))
    P("Phone Sections", "Dashboard Kit Deck Building", "Deck building categories", "on a phone should deck building categories be a carousel of category cards or chips that filter one list?",
      ("car", "Category Card Carousel", "One category per card with its count.", "playful", S(L, [("h", "Deck Building", 14), car([("Branding", "4 decks"), ("UpKeep", "9 decks"), ("Research", "2 decks")], 120, 64)], ("Browse by category", ""))),
      ("chips", "Filter Chips", "Tap a chip to filter the list.", "practical", S(L, [("h", "Deck Building", 14), ("tags", ["All", "Branding", "UpKeep", "Research"], True), ("cards", [("Pitch App", "UpKeep"), ("Kit Carousels", "Branding")], [LAGOON, TERRA])], ("Quick filter", ""))))
    P("Phone Sections", "Dashboard Kit Phone", "Section order", "on a phone should every section be a carousel row, one under another, or only the busiest sections?",
      ("all", "Every Section A Row", "The page is a stack of carousels.", "playful", S(L, [("raw", t(14, 10, "Agent Updates", 10, INK, "khand") + kitcar(16, 3, 120, 40) + t(14, 72, "Open Items", 10, INK, "khand") + kitcar(78, 3, 120, 40), 124)], ("Same pattern everywhere", "Like a streaming app"))),
      ("busy", "Busiest Sections Only", "Long sections swipe, short ones stay lists.", "calm", S(L, [("raw", t(14, 10, "Agent Updates", 10, INK, "khand") + kitcar(16, 3, 120, 40), 62), ("h", "To-Do", 11), ("checks", ["Answer decks", "Read report"], JUNGLE, 0)], ("Mixed but calm", ""))))
    P("Phone Sections", "Dashboard Kit Phone", "Jump to a section", "on a phone should a sticky row of section chips sit at the top to jump between sections?",
      ("chips", "Sticky Section Chips", "Updates, Items, Data, Feed at the top.", "practical", S(L, [("tags", ["Updates", "Items", "Data", "Feed"], True), ("h", "Agent Updates", 14), car(U)], ("Jump anywhere", ""))),
      ("none", "Just Scroll", "No extra row.", "calm", S(L, [("h", "Agent Updates", 14), car(U)], ("More room", ""))))
    P("Phone Sections", "Dashboard Kit Agent Updates", "Unread updates", "should unread update cards carry a small terracotta dot or a bold title?",
      ("dot", "Terracotta Dot", "A dot in the card corner.", "playful", S(L, [("h", "Agent Updates", 14), ("raw", kitcar() + dot(154, 12, 3.5, TERRA), 76)], ("Easy to spot", ""))),
      ("bold", "Bold Title", "Read cards go grey.", "calm", S(L, [("h", "Agent Updates", 14), ("raw", rect(14, 0, 150, 70, "#FFFFFF", LINE, 10) + t(24, 24, "Agent Update", 10, INK, "khand") + t(24, 37, "unread", 7.5, INK, "hind", 600) + rect(172, 0, 150, 70, "#FFFFFF", LINE, 10) + t(182, 24, "Open Item", 9.5, FAINT, "khand") + t(182, 37, "read", 7.5, FAINT), 76)], ("No extra marks", ""))))
    P("Phone Sections", "Dashboard Kit Phone", "Card tap", "should tapping a section card open its detail in a bottom sheet or a full new page?",
      ("sheet", "Bottom Sheet", "Slides up over the board.", "practical", S(L, [("raw", kitcar(), 76), ("sheet", "Research", ["2 new decks", "Updated 3:30 AM"])], ("Stay on the board", ""))),
      ("page", "Full Page", "Opens its own page with a back link.", "calm", S(L, [("raw", t(14, 10, "← Back to board", 8, LAGOON, "hind", 600), 16), ("h", "Research", 16), ("table", [("Decks", "2 new"), ("Updated", "3:30 AM")])], ("Room for detail", ""))))
    P("Phone Sections", "Dashboard Kit Phone", "Empty section", "when a carousel section has nothing in it should it hide or show one calm line?",
      ("hide", "Hide The Section", "Only sections with something show.", "calm", S(L, [("h", "Agent Updates", 14), car(U)], ("Shorter page", ""))),
      ("line", "One Calm Line", "Open Items: nothing open right now.", "practical", S(L, [("h", "Open Items", 14), ("p", "Nothing open right now", 46, MUTE), ("h", "Agent Updates", 14), car(U)], ("Same layout every day", ""))))
    return pairs
