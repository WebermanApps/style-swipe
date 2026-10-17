"""Job C follow-on decks, Oct 17 2026 evening (Branding Agent for Max): 3 Max's Picks decks on the Branding board + 10 queued UpKeep decks,
built from Max's picks and notes in ops/brand/results-2026-10-17/*.md. 10 picks each, Notes on, white page, R105 captions
('<exact screen/app>: <element>, <one plain sentence>'), skipped cards re-asked once in new wording, Max's notes applied.
R110: UpKeep / Smart Upkeep only, no Thai references. Option = (key, label, desc, feel, svg)."""
from fu1017_round3_art import *
from fu1017_upkeep_a import video, head
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
BRANDING = "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78"
BR = ["Smart Upkeep brand: white and cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only. Trust badges: approved set only."]
def Q(loc, el, s): return f"{loc}: {el}, {s}"
def D(id, name, slug_key, prefix, follows, about, summary, pairs, reasked=(), picks=False, inbox=""):
    pairs = [(g, q, (f"{i + 1:02d}{a[0]}",) + tuple(a[1:]), (f"{i + 1:02d}{b[0]}",) + tuple(b[1:])) for i, (g, q, a, b) in enumerate(pairs)]  # unique option ids per deck
    return dict(id=id, name=name, slug_key=slug_key, prefix=prefix, app="UpKeep", agent="branding" if picks == "branding" else "upkeep",
                submit_to=BRANDING if picks == "branding" else UPKEEP, board="branding" if picks else "upkeep", topic=slug_key, follows=follows,
                about=about, summary=summary, tag="Max's Picks" if picks else "UpKeep", pairs=pairs, reasked=list(reasked), max_picks=bool(picks),
                agent_inbox=inbox or ("branding/" if picks == "branding" else "upkeep/"), brands=BR)
o = opt
MA, TA, MP, OI = "UpKeep Member App", "UpKeep Tech App", "UpKeep Member Profile", "UpKeep Member App Open Items"
IP, FC, WW, SU, HP = "UpKeep Investor Pitch", "UpKeep Forecast Dashboard", "Smart Upkeep Site What We Take Care Of", "Smart Upkeep Site Sign Up Form", "Smart Upkeep Site Home Hero"
BADGES = ["Certified Techs", "Cancel Anytime", "Home Reports", "Licensed & Insured", "Moisture Scan Every Visit", "Background-Checked Yearly"]
def openlist(dotted=False):
    rows = [("Gutter downspout loose", "Recheck next visit", "Watch"), ("Sump pump tested", "All good", "Done"), ("Caulk at tub cracked", "Fix booked", "Booked"), ("Dryer vent lint", "Cleaned", "Done")]
    s = ""; y = 66
    for i, (a, b, st) in enumerate(rows):
        c = SAFFRON if st == "Watch" else (LAGOON if st == "Booked" else JUNGLE)
        s += t(20 if not dotted else 30, y + 12, a, 9, INK, "khand", 700) + t(20 if not dotted else 30, y + 23, b, 7, MUTE)
        s += (dot(21, y + 9, 3.5, c) if dotted else t(220, y + 12, st.upper(), 7, c, "hind", 700, "end")) + ln(y + 32); y += 36
    return member("Open Items", TERRA, [("tx", "Open Items", 13)], extra=s)
def folds(first_open):
    s, y = "", 66
    for i, (a, b) in enumerate([("Gutter downspout loose", "Tech note: bracket bent, reattached. Recheck in spring."), ("Caulk at tub cracked", "Fix booked for the next visit."), ("Attic vent", "Clear, no moisture.")]):
        op = first_open and i == 0
        s += rect(14, y, 212, 26, "#FFFFFF", LINE, 6) + t(22, y + 17, a, 9, INK, "khand", 700) + ic("down" if not op else "chev", 204, y + 6, 12, MUTE)
        y += 30
        if op: s += t(22, y + 6, b, 7.2, MUTE) + photo(22, y + 12, 80, 44, LAGOON, "house", 4); y += 64
    return member("Open Item Details", TERRA, [("tx", "Open Item Details", 13)], extra=s)
def lawn(kind):
    if kind == "photo": bl = [("tx", "Add-Ons", 13), ("photo", 70, JUNGLE, "house", "Lawn cutting"), ("tx", "Lawn Cutting", 11), ("p", "Weekly in season, same crew, one add-on.", 46), ("row", "Example price", "$ / month")]
    else: bl = [("tx", "Add-Ons", 13), ("card", "Lawn Cutting", "Weekly in season, one add-on", JUNGLE, "$/mo", "dot", 44, "left")]
    return member("Lawn Add-On", JUNGLE, bl)
def lawnact(kind):
    bl = [("tx", "My Plan", 13), ("card", "Plus Plan", "Next visit Oct 24", TERRA, "", "dot", 40, "left"), ("card", "Lawn Cutting", "One add-on, weekly in season", JUNGLE, "", "dot", 40, "left")]
    bl += [("btn", "Add To My Plan", "fill", JUNGLE)] if kind == "btn" else [("tx", "+ Add lawn cutting to my plan", 9, JUNGLE, "hind", 600)]
    return member("Lawn Add-On Action", JUNGLE, bl)
def plancard(kind):
    big = ("3", "visits left this year") if kind == "left" else ("Oct 24", "next visit")
    ex = rect(14, 66, 212, 96, "#FFFFFF", LINE, 8) + t(26, 84, "PLUS PLAN", 7.5, TERRA, "hind", 700) + t(26, 128, big[0], 38, INK, "khand", 700) + t(26, 146, big[1], 8.5, MUTE)
    return member("Plan Card", TERRA, [("tx", "My Plan", 13)], extra=ex)
def techcard(photo_shape="round", edge=TERRA, chip=None, window=False):
    s = rect(14, 66, 212, 70, "#FFFFFF", LINE, 8) + rect(14, 66, 4, 70, edge)
    s += (f'<circle cx="48" cy="101" r="22" fill="{CREAM}" stroke="{LINE}"/>' if photo_shape == "round" else rect(26, 79, 44, 44, CREAM, LINE, 4)) + g(34, 82, .16, person())
    s += t(80, 92, "Marcus", 12, INK, "khand", 700) + t(80, 104, "Your technician", 7.5, MUTE)
    if chip: s += rect(80, 110, len(chip) * 4.2 + 12, 15, LAGOON + "1A", "none", 7.5) + t(86, 121, chip, 7.5, LAGOON, "hind", 600)
    if window: s += t(80, 122, "Arrives 9:00 - 11:00 AM", 8, INK, "hind", 600)
    return member("Who's Coming", edge, [("tx", "Before Your Visit", 13)], extra=s)
def pills(style):
    def pill(x, y, w, s, fill):
        return rect(x, y, w, 26, TERRA if fill else "#FFFFFF", TERRA, 13, 1.4) + t(x + w / 2, y + 17, s, 8, "#FFFFFF" if fill else TERRA, "hind", 700, "middle")
    s = rect(14, 66, 212, 64, "#FFFFFF", LINE, 8) + t(24, 84, "Gutter downspout loose", 10, INK, "khand", 700) + t(24, 96, "Recheck next visit", 7.5, MUTE)
    s += pill(24, 100, 90, "Book A Fix", style == "mix") + pill(120, 100, 90, "Ask A Question", False)
    return member("Open Item Buttons", TERRA, [("tx", "Open Items", 13)], extra=s)
# ---------------------------------------------------------------- 1. Mixed (Max's Picks, Branding)
MIX = D("mixed-upkeep-follow-up-lists-crew-and-lawn-deck", "Mixed UpKeep Follow-Up: Lists, Crew And Lawn Add-On", "mixed-upkeep-follow-up", "mx3_",
  "mixed-deck-up-keep-round-two", "Follow-on of Mixed Deck: Up Keep, Round Two (8/10): open items, crew picture, lawn add-on (one add-on, Max's note), plan card, tech card.",
  "Open items with divider lines, crew of three, the lawn add-on as ONE add-on (re-asked), big-number plan card, tech card details.", [
 ("Open Items", Q(OI, "Divider rows", "how each status shows on the simple divider-line list you picked."),
  o("word", "Status Word On The Right", "Watch, Booked or Done in small caps", "practical", openlist(False)), o("dot", "Status Dot On The Left", "a colored dot, no word", "calm", openlist(True))),
 ("Open Items", Q(OI, "Fold-open details", "whether the first item opens by itself when the list loads."),
  o("closed", "All Folded Closed", "tap any item to open it", "calm", folds(False)), o("first", "First Item Open", "the newest item shows its note and photo", "practical", folds(True))),
 ("Add-Ons", Q(MA + " Add-Ons", "Lawn cutting card", "how the single lawn add-on card looks, with no sub add-ons."),
  o("photo", "Photo Above A Short Line", "one lawn photo, name, one line, price", "bold", lawn("photo")), o("text", "One Line Card", "name, one line and price only", "calm", lawn("text"))),
 ("Add-Ons", Q(MA + " My Plan", "Adding lawn cutting", "how the member adds the one lawn add-on from their plan."),
  o("btn", "Green Add To My Plan Button", "full-width button under the plan", "bold", lawnact("btn")), o("link", "Small Underlined Link", "a quiet text link under the plan", "calm", lawnact("link"))),
 ("Plans", Q(MA + " My Plan", "Plan card big number", "which single number is the big one on the plan card."),
  o("left", "Visits Left", "big count of visits left this year", "practical", plancard("left")), o("next", "Next Visit Date", "big date of the next visit", "calm", plancard("next"))),
 ("Field Brand", Q("Smart Upkeep Site About Us", "Crew of three picture", "what the crew of three wears in the team photo."),
  o("polos", "All Three In Polos", "terracotta polos, charcoal pants", "practical", crew("Crew Of Three", TERRA, [P(), P(skin=SKIN[1], hair=HAIR[1]), P(skin=SKIN[2], hair=HAIR[2])])),
  o("mix", "Polos And One Softshell", "two polos and one charcoal softshell", "bold", crew("Crew Of Three", TERRA, [P(), P(skin=SKIN[1], hair=HAIR[1], layer="softshell", layerc="#3D3A36"), P(skin=SKIN[2], hair=HAIR[2])]))),
 ("Field Brand", Q(HP, "Hero crew picture", "who shows in the home page hero now that you liked both one tech and two techs."),
  o("one", "One Tech In A Polo", "one tech on the hero, the crew on About Us", "calm", crew("Hero", TERRA, [P()])), o("two", "Two Techs Side By Side", "two techs together on the hero", "playful", crew("Hero", TERRA, [P(polo=TERRA, collar=None), P(skin=SKIN[1], hair=HAIR[1], polo=TERRA)]))),
 ("Visits", Q(MA + " Visits", "Licensed tech photo", "the shape of the photo beside the tech's name."),
  o("round", "Round Photo", "circle photo beside the name", "calm", techcard("round")), o("square", "Square Photo", "square photo with small corners", "practical", techcard("square"))),
 ("Visits", Q(MA + " Visits", "Tech card colored edge", "which color the edge of the licensed tech card uses."),
  o("terra", "Terracotta Edge", "member app color", "bold", techcard("round", TERRA)), o("lagoon", "Lagoon Edge", "the tech color on the member's screen", "calm", techcard("round", LAGOON))),
 ("From The Feed", Q(OI, "Pill buttons", "how the two pill buttons under an open item look together."),
  o("mix", "One Filled And One Outline", "the main action filled", "bold", pills("mix")), o("out", "Both Outline", "two outline pills, same weight", "calm", pills("out"))),
], reasked=["04", "07"], picks="branding")
# ---------------------------------------------------------------- 2. Customer visit history & photos (Max's Picks, UpKeep)
def scan(kind):
    if kind == "big": ex = rect(14, 66, 212, 90, JUNGLE + "12", "none", 8) + ic("check", 104, 78, 32, JUNGLE, 2.6) + t(120, 132, "All Good", 18, JUNGLE, "khand", 700, "middle") + t(120, 146, "Whole-house moisture scan, Oct 2", 7.5, MUTE, "hind", 400, "middle")
    else: ex = t(20, 80, "Visit Report, Oct 2", 12, INK, "khand", 700) + photo(20, 88, 200, 56, LAGOON, "house", 4) + rect(20, 150, 200, 24, "#FFFFFF", LINE, 6) + ic("check", 26, 155, 14, JUNGLE, 2.2) + t(46, 166, "Moisture scan: all good", 8.5, INK, "hind", 600)
    return member("Moisture Scan", JUNGLE, [("tx", "Home", 13)], extra=ex)
def problem(kind):
    ex = rect(14, 66, 212, 96, "#FFFFFF", LINE, 8) + rect(14, 66, 4, 96, SAFFRON) + t(26, 84, "Basement, north wall", 11, INK, "khand", 700)
    if kind == "photo": ex += photo(26, 92, 70, 60, LAGOON, "house", 4) + t(104, 108, "18% moisture", 12, INK, "khand", 700) + t(104, 122, "WATCH", 8, SAFFRON, "hind", 700)
    else: ex += t(26, 116, "18%", 30, INK, "khand", 700) + t(80, 112, "WATCH", 9, SAFFRON, "hind", 700) + t(26, 136, "Recheck at the next visit", 8, MUTE)
    return member("Scan Problem", SAFFRON, [("tx", "Moisture Scan", 13)], extra=ex)
def history(kind):
    ex = t(20, 80, "Gutter downspout", 11, INK, "khand", 700) + rect(176, 70, 40, 15, SAFFRON + "22", "none", 7) + t(196, 81, "WATCH", 7, SAFFRON, "hind", 700, "middle")
    if kind == "first": ex += photo(20, 90, 96, 70, LAGOON, "house", 4) + photo(124, 90, 96, 70, LAGOON, "house", 4) + t(68, 172, "First seen, Jul 9", 7.5, MUTE, "hind", 500, "middle") + t(172, 172, "Latest, Oct 2", 7.5, MUTE, "hind", 500, "middle")
    else: ex += photo(20, 90, 200, 90, LAGOON, "house", 4) + t(20, 192, "Latest, Oct 2", 7.5, MUTE)
    return member("Problem Photo", SAFFRON, [("tx", "Photos", 13)], extra=ex)
def tl(dot_season):
    items = [("Oct 2", "Fall visit: furnace tuned, gutters cleared"), ("Jul 9", "Summer visit: AC coil rinsed"), ("Apr 3", "Spring visit: sump pump tested"), ("Jan 8", "Winter visit: pipes checked")]
    ex = ""; y = 70
    for i, (a, b) in enumerate(items):
        if dot_season: ex += dot(22, y + 8, 4.5, ACC[i % 4])
        ex += t(34 if dot_season else 20, y + 11, a, 9.5, INK, "khand", 700) + t(34 if dot_season else 20, y + 22, b, 7.2, MUTE) + ln(y + 30); y += 36
    return member("Past Visits", TERRA, [("tx", "Visit History", 13)], extra=ex)
def strip(kind):
    ex = t(20, 80, "Visit Report, Oct 2", 12, INK, "khand", 700) + "".join(photo(20 + i * 68, 88, 64, 50, LAGOON, "house", 4) for i in range(3))
    if kind == "grid": ex += t(20, 154, "Tap a photo: all photos by date", 8, MUTE) + "".join(rect(20 + (i % 4) * 51, 160 + (i // 4) * 32, 47, 28, "#DCE9EF", "none", 3) for i in range(8))
    else: ex += t(20, 154, "Tap a photo: full screen, swipe for more", 8, MUTE) + rect(20, 160, 200, 62, "#0A0A0A", "none", 4) + photo(44, 165, 152, 52, LAGOON, "house", 4)
    return member("Report Photos", LAGOON, [("tx", "Visit Report", 13)], extra=ex)
def pgrid(kind):
    ex = ""
    if kind == "head":
        y = 66
        for d in ("Oct 2", "Jul 9"):
            ex += t(20, y + 10, d, 9, INK, "khand", 700) + "".join(rect(20 + i * 51, y + 16, 47, 40, "#DCE9EF", "none", 3) for i in range(4)); y += 66
    else:
        ex += "".join(rect(20 + i * 52, 66, 48, 16, (TERRA if i == 0 else "#FFFFFF"), TERRA, 8) + t(44 + i * 52, 77, d, 7, "#FFFFFF" if i == 0 else TERRA, "hind", 600, "middle") for i, d in enumerate(("Oct 2", "Jul 9", "Apr 3", "Jan 8")))
        ex += "".join(rect(20 + (i % 4) * 51, 92 + (i // 4) * 44, 47, 40, "#DCE9EF", "none", 3) for i in range(8))
    return member("Photo Grid", LAGOON, [("tx", "Photos", 13)], extra=ex)
def chat(chips):
    bl = [("tx", "Smart Upkeep Team", 12), ("bubble", "Hi! Your fall visit is booked for Oct 24.", False, LAGOON), ("bubble", "Thanks, see you then", True), ("tags", chips), ("input", "Type a message", TERRA, "mic")]
    return member("In-App Chat", LAGOON, bl)
def recheck(kind):
    s = "Recheck: gutter downspout, Marcus, Oct 24" if kind == "who" else "Recheck: gutter downspout"
    bl = [("banner", s, SAFFRON, "clock")]
    if kind == "photo": bl = [("banner", s, SAFFRON, "clock"), ("photos", 2, 40)]
    return member("Recheck Banner", SAFFRON, bl + [("card", "Next Visit", "Oct 24, 9:00 - 11:00 AM", TERRA, "", "dot", 40, "left")])
def tip(kind):
    ex = rect(14, 150, 212, 52, "#FFFFFF", LINE, 8) + ic("star" if kind == "icon" else "home", 22, 158, 14, LAGOON, 2) + t(42, 169, "DID YOU KNOW?", 7.5, LAGOON, "hind", 700) + t(22, 186, "Clean dryer vents once a year to cut fire risk.", 7.2, INK)
    if kind == "art": ex += photo(176, 156, 42, 40, LAGOON, "house", 4)
    return member("Did You Know", LAGOON, [("tx", "Home", 13), ("card", "Next Visit", "Oct 24", TERRA, "", "dot", 40, "left"), ("card", "Open Items", "1 to watch", SAFFRON, "", "dot", 40, "left")], extra=ex)
CUS = D("customer-visit-history-and-photos-reports-and-scan-deck", "Customer Visit History & Photos: Reports And Scan Results", "customer-visit-history-photos", "cvh3_",
  "upkeep-customer-profile-visits-photos-and-messages-deck", "Third round on the member's visit history, photos, scan results, chat and tips; scan follows Max's note (all-good sign, show only problems).",
  "All-good scan sign and problem-only results (Max's note), problem photo history re-asked, timeline rows, report photos, chat chips, recheck banner, tip, tech card.", [
 ("Moisture Scan", Q(MA + " Home", "Whole-house scan result", "how the all-good sign shows when the scan finds nothing."),
  o("big", "Big All Good Check", "a large green check on Home", "bold", scan("big")), o("line", "All Good Line In The Report", "one green line inside the visit report", "calm", scan("line"))),
 ("Moisture Scan", Q(MA + " Moisture Scan", "Problem found card", "what a problem card shows when the scan does find one."),
  o("num", "Reading And The Word", "big reading plus Watch, no photo", "practical", problem("num")), o("photo", "Photo With The Reading", "spot photo, reading and Watch", "bold", problem("photo"))),
 ("Photos", Q(MA + " Photos", "Problem photo history", "whether a watched problem also shows the photo from when it was first seen."),
  o("first", "First Seen And Latest", "two photos side by side", "practical", history("first")), o("latest", "Latest Photo Only", "one photo with the Watch tag", "calm", history("latest"))),
 ("Visit History", Q(MA + " Visit History", "Timeline rows", "whether each date-and-summary row gets a small season dot."),
  o("dot", "Season Dot On Each Row", "a colored dot per season", "playful", tl(True)), o("plain", "Plain Rows", "date and one line, nothing else", "calm", tl(False))),
 ("Visit Report", Q(MA + " Visit Report", "Strip of three photos", "where a tap on the photo strip takes the member."),
  o("grid", "Opens The Photo Grid", "all photos for that visit by date", "practical", strip("grid")), o("full", "Opens Full Screen", "one big photo, swipe for the rest", "bold", strip("full"))),
 ("Photos", Q(MA + " Photos", "Photo grid by visit date", "how the member moves between visit dates in the grid."),
  o("head", "Date Headers In One Scroll", "every visit stacked with a date", "calm", pgrid("head")), o("chips", "Date Chips To Filter", "tap a date to see only that visit", "practical", pgrid("chips"))),
 ("Messaging", Q(MA + " Chat", "Quick-reply chips", "which chips sit above the box in the Smart Upkeep Team chat."),
  o("tasks", "Reschedule, Question, Photo", "task chips", "practical", chat(["Reschedule", "Ask A Question", "Send A Photo"])), o("short", "Yes, No, Call Me", "short answer chips", "calm", chat(["Yes", "No", "Call Me"]))),
 ("What To Watch", Q(MA + " Home", "Recheck banner", "what the banner that stays until the recheck says."),
  o("who", "Item, Tech And Date", "who rechecks it and when", "practical", recheck("who")), o("photo", "Item With A Photo", "small photo of the item", "bold", recheck("photo"))),
 ("Tips", Q(MA + " Home", "Did You Know tip", "how the one tip at the bottom of Home looks."),
  o("icon", "Lagoon Label And Icon", "small icon, label and one line", "calm", tip("icon")), o("art", "With A Small Drawing", "label, one line and a drawing", "playful", tip("art"))),
 ("Who's Coming", Q(MA + " Visits", "Technician card before a visit", "what sits under the tech's name with the Certified Techs chip."),
  o("chip", "Certified Techs Chip Only", "photo, name and the chip", "calm", techcard("round", LAGOON, "Certified Techs")), o("win", "Arrival Window Too", "photo, name and arrival time", "practical", techcard("round", LAGOON, None, True))),
], reasked=["05", "09"], picks="upkeep")
# ---------------------------------------------------------------- 3. Investor numbers & market (Max's Picks, UpKeep)
EX = "Example numbers"
def mkt(kind):
    s = stx(18, 30, "Market Size", 20)
    if kind == "up": s += "".join(rect(30 + i * 30, 150 - (i + 1) * 22, 24, (i + 1) * 22, [LAGOON, LAGOON, TERRA][i % 3]) for i in range(3)) + t(30, 168, "One street, one suburb, one metro", 9, MUTE) + stx(200, 90, "Bottom Up", 14, TERRA)
    else: s += "".join(rect(40 + i * 20, 48 + i * 34, 220 - i * 40, 28, [LAGOON, "#5E8FA6", TERRA][i]) for i in range(3)) + t(160, 168, "All homes, owned homes, our area", 9, MUTE, "hind", 400, "middle")
    return slidecard("Market Slide", LAGOON, s, EX)
def funds(kind):
    s = stx(18, 30, "The Ask", 20)
    if kind == "pie": s += pie(80, 110, 46, [(45, TERRA), (30, LAGOON), (25, JUNGLE)]) + f'<line x1="150" y1="110" x2="300" y2="110" stroke="{INK}" stroke-width="2"/>' + "".join(dot(160 + i * 45, 110, 5, ACC[i]) + t(160 + i * 45, 130, f"M{i+1}", 9, INK, "hind", 600, "middle") for i in range(4))
    else: s += rect(20, 90, 140, 30, TERRA) + rect(160, 90, 90, 30, LAGOON) + rect(250, 90, 50, 30, JUNGLE) + "".join(f'<line x1="{60 + i * 70}" y1="80" x2="{60 + i * 70}" y2="130" stroke="{INK}" stroke-width="1.5"/>' + t(60 + i * 70, 146, f"M{i+1}", 9, INK, "hind", 600, "middle") for i in range(4))
    return slidecard("Use Of Funds", TERRA, s, EX)
def trac(kind):
    s = stx(18, 30, "Traction", 20)
    if kind == "cols": s += stx(30, 66, "Members Did", 12, TERRA) + stx(180, 66, "Waiting To Join", 12, LAGOON) + "".join(t(30, 88 + i * 18, x, 9, INK) for i, x in enumerate(["Pilot homes visited", "Problems caught early", "Renewals"])) + "".join(t(180, 88 + i * 18, x, 9, INK) for i, x in enumerate(["Waitlist", "Letters of intent", "Partner leads"]))
    else: s += f'<line x1="20" y1="110" x2="300" y2="110" stroke="{INK}" stroke-width="2"/>' + "".join(dot(40 + i * 64, 110, 6, TERRA if i < 2 else LAGOON) + t(40 + i * 64, 132, x, 8, INK, "hind", 600, "middle") for i, x in enumerate(["Pilot", "Reports", "Renewals", "Waitlist", "LOIs"])) + t(40, 90, "Done", 9, TERRA, "hind", 700) + t(200, 90, "Waiting", 9, LAGOON, "hind", 700)
    return slidecard("Traction", JUNGLE, s, EX)
def plot(where, axes=("Prevent", "Repair", "Whole Home", "One Trade")):
    s = stx(18, 30, "Competition" if where == "comp" else "Forecast Appendix: Where We Sit", 18 if where == "comp" else 14)
    s += f'<line x1="160" y1="44" x2="160" y2="168" stroke="{MUTE}"/><line x1="40" y1="106" x2="290" y2="106" stroke="{MUTE}"/>'
    s += t(160, 42, axes[0], 8, MUTE, "hind", 600, "middle") + t(160, 176, axes[1], 8, MUTE, "hind", 600, "middle") + t(292, 102, axes[2], 8, MUTE, "hind", 600, "end") + t(42, 102, axes[3], 8, MUTE)
    s += dot(240, 66, 8, TERRA) + t(240, 84, "Smart Upkeep", 8, TERRA, "hind", 700, "middle") + "".join(dot(x, y, 6, "#BDB5A8") for x, y in [(90, 140), (120, 70), (210, 140), (70, 120)])
    return slidecard("Competition Plot", SAFFRON, s, EX)
def gtm(kind):
    s = stx(18, 30, "Go-To-Market", 20) + "".join(f'<path d="M{60 + i * 22} {50 + i * 36} H{260 - i * 22} L{250 - i * 22} {80 + i * 36} H{70 + i * 22} Z" fill="{ACC[i]}"/>' for i in range(3))
    lab = ["Referrals 40%", "Partners 35%", "Ads 25%"] if kind == "share" else ["$ per member: referral", "$ per member: partner", "$ per member: ads"]
    s += "".join(t(160, 70 + i * 36, x, 9, "#FFFFFF", "hind", 700, "middle") for i, x in enumerate(lab))
    return slidecard("Funnel", LAGOON, s, EX)
def scen(kind):
    s = stx(18, 30, "Three Scenarios", 20) + axes(30, 50, 270, 110)
    if kind == "band": s += f'<path d="M30 150 L300 60 L300 100 L30 158 Z" fill="{LAGOON}22"/>'
    s += sline(30, 160, 270, 100, [10, 30, 55, 80, 110], TERRA, 3, vmax=140) + sline(30, 160, 270, 100, [10, 25, 40, 55, 70], LAGOON, 1.4 if kind == "bold" else 0.01, vmax=140) + sline(30, 160, 270, 100, [10, 35, 70, 100, 140], JUNGLE, 1.4 if kind == "bold" else 0.01, vmax=140)
    return slidecard("Scenarios", JUNGLE, s, EX)
def horizon(kind):
    s = stx(18, 30, "Projection", 20) + axes(30, 50, 270, 110) + sline(30, 160, 270, 100, [10, 25, 45, 70, 100], TERRA, 3)
    if kind == "toggle": s += rect(220, 16, 40, 18, INK, "none", 9) + t(240, 29, "3Y", 9, "#FFFFFF", "hind", 700, "middle") + rect(262, 16, 40, 18, "#FFFFFF", INK, 9) + t(282, 29, "5Y", 9, INK, "hind", 700, "middle")
    else: s += rect(192, 50, 108, 110, SOFT) + t(246, 64, "Rough", 9, MUTE, "hind", 700, "middle")
    return slidecard("Horizon", TERRA, s, EX)
def ask(kind):
    s = stx(18, 30, "The Ask", 20) + stx(160, 100, "$ Round", 34, TERRA, a="middle")
    s += t(160, 126, "Valuation range from our forecast" if kind == "range" else "Use of funds and milestones", 10, INK, "hind", 600, "middle") + (t(160, 146, "Our honest estimate, updated as we grow", 8, MUTE, "hind", 400, "middle") if kind == "range" else t(160, 146, "Valuation in the appendix", 8, MUTE, "hind", 400, "middle"))
    return slidecard("Ask Slide", TERRA, s, EX)
def risk(n):
    s = stx(18, 30, "Risks And What We Do", 18) + t(24, 52, "RISK", 8, MUTE, "hind", 700) + t(170, 52, "WHAT WE DO", 8, MUTE, "hind", 700)
    rows = [("Tech hiring", "Training path"), ("Churn", "Visit reports"), ("Seasonality", "Indoor work"), ("Insurance cost", "Clean record"), ("Copycats", "Home data")][:n]
    s += "".join(t(24, 72 + i * (100 / n), a, 10 if n == 3 else 9, INK, "hind", 600) + t(170, 72 + i * (100 / n), b, 10 if n == 3 else 9, INK) for i, (a, b) in enumerate(rows))
    return slidecard("Risk Slide", SAFFRON, s, EX)
INV = D("investor-numbers-and-market-ask-traction-and-size-deck", "Investor Numbers & Market: Ask, Traction And Market Size", "investor-numbers-market", "inm3_",
  "upkeep-investor-pitch-market-and-model-slides-deck", "Third round on the investor numbers: market size (Max: go with what you think is best), use of funds, traction (both), the 2x2 plot (Max: use it where it fits), valuation (Max: honest estimate).",
  "Market size and use-of-funds re-asked, traction both ways, the 2x2 plot placed, funnel, scenarios, horizon, valuation on the ask, risk table.", [
 ("Market", Q(IP + " Market Slide", "Market size", "my pick is bottom-up from one metro area, so is that the one."),
  o("up", "Bottom-Up From One Metro", "street, suburb, metro (my pick)", "practical", mkt("up")), o("down", "Top-Down To Our Area", "all homes narrowing to ours", "bold", mkt("down"))),
 ("The Ask", Q(IP + " Ask Slide", "Use of funds with milestones", "how the money and the milestones it unlocks share one slide."),
  o("pie", "Pie Beside A Milestone Line", "pie left, milestones right", "calm", funds("pie")), o("bar", "One Split Bar With Ticks", "money bar with milestone ticks", "practical", funds("bar"))),
 ("Traction", Q(IP + " Traction Slide", "Done and waiting", "how what members did and who is waiting share the slide."),
  o("cols", "Two Columns", "done on the left, waiting on the right", "practical", trac("cols")), o("line", "One Timeline", "pilot first, then the waitlist", "calm", trac("line"))),
 ("Competition", Q(IP + " Competition Slide", "The 2x2 plot", "where the plot you liked goes so you can react to it."),
  o("comp", "On The Competition Slide", "the plot is the competition slide", "bold", plot("comp")), o("fc", "In The Forecast Appendix", "a 'where we sit' page", "calm", plot("fc"))),
 ("Competition", Q(IP + " Competition Slide", "2x2 plot axes", "which two questions the plot's axes ask."),
  o("prev", "Prevent Or Repair", "and whole home or one trade", "practical", plot("comp")), o("diy", "Done For You Or DIY", "and membership or one-off", "calm", plot("comp", ("Done For You", "DIY", "Membership", "One-Off")))),
 ("Go-To-Market", Q(IP + " Go-To-Market Slide", "One funnel", "what the funnel fed by both channels labels."),
  o("share", "Share Of New Members", "percent from each channel", "practical", gtm("share")), o("cost", "Cost Per Member", "what each channel costs", "bold", gtm("cost"))),
 ("Financials", Q(IP + " Financials Slide", "Three lines on one chart", "how the base case stands out from best and worst."),
  o("bold", "Base Bold, Others Thin", "three lines, base heavy", "calm", scen("bold")), o("band", "Base Line In A Band", "best to worst shaded", "practical", scen("band"))),
 ("Financials", Q(IP + " Financials Slide", "Three and five years", "how both horizons show on one slide."),
  o("toggle", "A 3Y And 5Y Toggle", "switch between the two", "practical", horizon("toggle")), o("shade", "Five Years, Last Two Shaded", "one chart, rough years shaded", "calm", horizon("shade"))),
 ("The Ask", Q(IP + " Ask Slide", "Valuation", "whether our honest valuation estimate sits on the ask slide."),
  o("range", "Range On The Ask Slide", "our estimate, updated as we grow", "bold", ask("range")), o("app", "Amount Only, Valuation Later", "valuation in the appendix", "calm", ask("app"))),
 ("Extras", Q(IP + " Risk Slide", "Risk and fix table", "how many risks the table lists."),
  o("three", "Three Risks", "the biggest three only", "calm", risk(3)), o("five", "Five Risks", "a fuller list", "practical", risk(5))),
], reasked=["03", "08"], picks="upkeep")
# ================================================================ UpKeep queued decks (10)
def hdrimg(h=0.33, addr="on", badge="corner", logo="center", acts=("Book", "Message", "Report"), style="pill", pop="icons", sticky=False, tech=False, cap=""):
    c = LAGOON if tech else TERRA; ph = 216 * h; y = 30; s = ""
    if sticky:
        s += rect(14, y, 212, 26, "#FFFFFF") + mark(26, y + 13, 6, "#FFFFFF", c) + t(36, y + 17, "12 Elm St" if logo in ("addr", "badge") else "Smart Upkeep", 10, INK, "khand", 700)
        s += (rect(150, y + 6, 60, 15, c + "1A", "none", 7.5) + t(180, y + 17, "PLUS PLAN", 7, c, "hind", 700, "middle")) if logo == "badge" else ""
        s += ln(y + 26) + "".join(rect(14, y + 34 + i * 44, 212, 38, "#FFFFFF", LINE, 6) + t(24, y + 57 + i * 44, x, 9, INK, "khand", 700) for i, x in enumerate(["Next Visit", "Open Items", "Home Record", "Plan"]))
        return s
    if logo == "center": s += rect(14, y, 212, 22, "#FFFFFF") + mark(102, y + 11, 6, "#FFFFFF", c) + t(112, y + 15, "Smart Upkeep", 9.5, INK, "khand", 700) + ln(y + 22); y += 26
    s += photo(14, y, 212, ph, LAGOON, "house", 0)
    if logo == "on": s += mark(110, y + 14, 6, "#FFFFFF", c) + t(120, y + 18, "Smart Upkeep", 9, "#FFFFFF", "khand", 700)
    if addr == "on": s += f'<rect x="14" y="{y + ph - 34}" width="212" height="34" fill="#0A0A0A55"/>' + t(22, y + ph - 18, "12 Elm St", 13, "#FFFFFF", "khand", 700) + t(22, y + ph - 7, "Royal Oak, MI", 7.5, "#FFFFFFDD")
    if addr == "line": s += f'<rect x="14" y="{y + ph - 20}" width="212" height="20" fill="#0A0A0A55"/>' + t(22, y + ph - 6, "12 Elm St, Royal Oak, MI", 9.5, "#FFFFFF", "khand", 700)
    if cap: s += rect(18, y + 8, len(cap) * 3.9 + 12, 15, "#FFFFFFDD", "none", 7.5) + t(24, y + 19, cap, 7, INK, "hind", 600)
    if badge == "corner": s += rect(162, y + 8, 58, 15, c, "none", 7.5) + t(191, y + 19, "PLUS PLAN", 7, "#FFFFFF", "hind", 700, "middle")
    y += ph + 6
    if badge == "beside": s += rect(22, y, 58, 15, c + "1A", "none", 7.5) + t(51, y + 11, "PLUS PLAN", 7, c, "hind", 700, "middle"); y += 20
    n = len(acts); w = (212 - (n - 1) * 6) / n
    for i, a in enumerate(acts):
        x = 14 + i * (w + 6)
        if style == "pill": s += rect(x, y, w, 24, "#FFFFFF", c if pop == "icons" else INK, 12, 1.3) + t(x + w / 2, y + 16, a, 8, c if pop == "icons" else INK, "hind", 700, "middle")
        else: s += rect(x, y, w, 40, "#FFFFFF", LINE, 6) + ic(["cal", "phone", "star", "tag"][i % 4], x + w / 2 - 8, y + 6, 16, c if pop == "icons" else INK, 2) + t(x + w / 2, y + 34, a, 7.5, INK, "hind", 600, "middle")
    return s
def MH(label, acc, tech=False, **k):
    return U(label, acc, [], 30, None, True, hdrimg(tech=tech, **k), TNAV if tech else MNAV, 0)
MPH = D("member-profile-header-tech-header-and-quick-actions-deck", "Member Profile Header: Tech Header And Quick Actions", "member-profile-header-next", "mph3_",
  "upkeep-member-profile-header-deck", "Follow-on of Member Profile Header (9/10): tech app header re-asked with Max's note (member orange, tech blue), hero size, address, plan badge, quick actions, sticky header.",
  "Tech header in lagoon (Max's note), hero size, address and plan badge spots, which quick actions, their look, what the shrunk sticky header keeps.", [
 ("Tech App", Q(TA + " Profile", "Header color", "the tech app header in blue to match your note, member orange and tech blue."),
  o("band", "Lagoon Photo Header", "same layout, lagoon pops", "bold", MH("Tech Header", LAGOON, True, acts=("Start Route", "Message", "Reports"))), o("white", "White Header, Lagoon Name Bar", "compact, no photo", "calm", MH("Tech Header", LAGOON, True, sticky=True))),
 ("Layout", Q(MP, "Home photo size", "how tall the home photo hero is."),
  o("third", "About A Third", "more of the page below", "calm", MH("Hero Size", TERRA, h=.33)), o("half", "About Half", "the house fills more", "bold", MH("Hero Size", TERRA, h=.5))),
 ("Identity", Q(MP, "Address on the photo", "how the address sits on the house photo."),
  o("two", "Street Big, City Small", "two lines with a soft shade", "practical", MH("Address", TERRA, h=.42)), o("one", "One Line", "street and city together", "calm", MH("Address", TERRA, h=.42, addr="line"))),
 ("Info Shown", Q(MP, "Plan badge spot", "where the one plan badge sits in the header."),
  o("corner", "On The Photo Corner", "badge top right of the photo", "bold", MH("Plan Badge", TERRA, h=.42)), o("beside", "Under The Photo", "badge on white under it", "calm", MH("Plan Badge", TERRA, h=.42, badge="beside"))),
 ("Quick Actions", Q(MP, "Quick action buttons", "which three actions sit under the header."),
  o("book", "Book, Message, Report", "visit first", "practical", MH("Quick Actions", TERRA, h=.42)), o("msg", "Message, Report, Add-On", "chat first", "calm", MH("Quick Actions", TERRA, h=.42, acts=("Message", "Report", "Add-On")))),
 ("Quick Actions", Q(MP, "Quick action look", "how the quick actions are drawn."),
  o("pill", "Outline Pills", "one row of pills", "calm", MH("Action Look", TERRA, h=.42)), o("tile", "Icon Tiles", "icon over a word", "practical", MH("Action Look", TERRA, h=.42, style="tile"))),
 ("On Scroll", Q(MP, "Shrunk sticky header", "what stays in the slim header after it shrinks."),
  o("logo", "Logo And Name", "brand stays on top", "calm", MH("On Scroll", TERRA, sticky=True)), o("addr", "Address And Plan Badge", "the home stays on top", "practical", MH("On Scroll", TERRA, sticky=True, logo="badge"))),
 ("Logo", Q(MP, "Centered logo", "where the centered logo sits with the photo."),
  o("above", "Above The Photo", "a slim white logo bar", "calm", MH("Logo", TERRA, h=.4)), o("on", "On The Photo", "white logo over the house", "bold", MH("Logo", TERRA, h=.42, logo="on"))),
 ("Color", Q(MP, "Terracotta pop", "which parts carry the terracotta on the white header."),
  o("icons", "Quick Actions And Badge", "terracotta on actions and badge", "bold", MH("Color", TERRA, h=.42)), o("badge", "Plan Badge Only", "actions in ink", "calm", MH("Color", TERRA, h=.42, pop="badge"))),
 ("Layout", Q(MP, "House photo source", "which photo fills the header."),
  o("member", "Member's Own Photo", "they upload it at sign up", "playful", MH("Photo", TERRA, h=.42, cap="Your photo")), o("tech", "Tech's First-Visit Photo", "taken on the first visit", "practical", MH("Photo", TERRA, h=.42, cap="Photo by Marcus, first visit"))),
], reasked=["10"])
def pins(pts, c=TERRA):
    return "".join(f'<path d="M{x} {y} q-7 -11 0 -16 q7 5 0 16z" fill="{c}"/>' + t(x, y - 6, str(i + 1), 6.5, "#FFFFFF", "hind", 700, "middle") for i, (x, y) in enumerate(pts))
def nav_next():
    s = rect(14, 40, 212, 90, SOFT, "none", 6) + f'<path d="M60 116 L110 86 L160 126 L200 78" fill="none" stroke="{LAGOON}" stroke-width="2" stroke-dasharray="4 3"/>' + pins([(60, 116), (110, 86), (160, 126), (200, 78)])
    s += rect(14, 138, 212, 50, "#FFFFFF", LAGOON, 6, 1.4) + t(24, 154, "NEXT: 12 Elm St", 9.5, INK, "khand", 700) + t(24, 166, "9:00 Fall visit", 7, MUTE) + rect(24, 170, 192, 14, LAGOON, "none", 7) + t(120, 180, "NAVIGATE TO NEXT JOB", 7, "#FFFFFF", "hind", 700, "middle")
    return tech("Today", LAGOON, [], extra=s)
def nav_each():
    s = rect(14, 40, 212, 80, SOFT, "none", 6) + pins([(60, 100), (120, 70), (180, 104)]); y = 126
    for i, (a, b) in enumerate([("12 Elm St", "9:00 Fall visit"), ("40 Oak Ave", "11:30 Fall visit"), ("7 Pine Ct", "2:00 Recheck")]):
        s += rect(14, y, 212, 28, "#FFFFFF", LINE, 5) + t(22, y + 12, f"{i+1}. {a}", 8.5, INK, "khand", 700) + t(22, y + 22, b, 6.8, MUTE) + rect(166, y + 6, 54, 16, LAGOON, "none", 8) + t(193, y + 17, "Navigate", 7, "#FFFFFF", "hind", 700, "middle"); y += 32
    return tech("Today", LAGOON, [], extra=s)
def checklist(kind):
    if kind == "order": items = ["1. Furnace filter", "2. Water heater", "3. Sump pump", "4. Gutters", "5. Dryer vent", "6. Smoke alarms"]; s = ""
    else: items = ["BASEMENT", "1. Furnace filter", "2. Sump pump", "OUTSIDE", "3. Gutters", "4. Dryer vent"]; s = ""
    y = 40
    for it in items:
        if it.isupper(): s += t(20, y + 12, it, 7.5, LAGOON, "hind", 700); y += 16
        else: s += rect(14, y, 212, 22, "#FFFFFF", LINE, 4) + rect(20, y + 6, 10, 10, "#FFFFFF", MUTE, 2) + t(36, y + 15, it, 8.5, INK, "hind", 600); y += 26
    s += t(120, y + 14, "Proposed order, you can go out of order", 7, MUTE, "hind", 400, "middle")
    return tech("Checklist", LAGOON, [], extra=s)
def notes(kind):
    bl = [("tx", "Note For The Member", 11)]
    if kind == "chips": bl += [("tags", ["Looks good", "Watch this", "Fixed today", "Call us"]), ("input", "Add your own words", LAGOON, "mic")]
    else: bl += [("input", "Gutters cleared, downspout re...", LAGOON, "mic"), ("p", "Suggestions: reattached, recheck in spring", 46)]
    return tech("Member Note", LAGOON, bl)
def ticked(kind):
    bl = [("tx", "Checklist", 11)]
    rows = [("Furnace filter", True), ("Water heater", True), ("Sump pump", False)]
    s = ""; y = 62
    for a, d in rows:
        s += rect(14, y, 212, 34, "#FFFFFF", LINE, 4) + rect(20, y + 11, 12, 12, JUNGLE if d else "#FFFFFF", JUNGLE, 2) + t(40, y + 21, a, 9, INK, "hind", 600)
        if d: s += (rect(184, y + 4, 36, 26, "#DCE9EF", "none", 3) if kind == "thumb" else rect(178, y + 10, 42, 14, JUNGLE + "1A", "none", 7) + t(199, y + 20, "2 photos", 6.5, JUNGLE, "hind", 700, "middle"))
        y += 38
    return tech("Ticked Task", LAGOON, bl, extra=s)
def moist(kind):
    s = t(20, 72, "Basement, north wall", 10, INK, "khand", 700) + rect(14, 80, 140, 36, "#FFFFFF", LAGOON, 4, 1.4) + t(24, 104, "18", 18, INK, "khand", 700) + t(144, 104, "%", 10, MUTE, "hind", 600, "end")
    if kind == "keys": s += "".join(rect(14 + (i % 3) * 72, 124 + (i // 3) * 26, 66, 22, SOFT, "none", 4) + t(47 + (i % 3) * 72, 139 + (i // 3) * 26, k, 10, INK, "khand", 700, "middle") for i, k in enumerate("123456789"))
    else: s += t(20, 132, "Last visit: 14% (Jul 9)", 8.5, MUTE, "hind", 600)
    s += rect(160, 84, 60, 28, SAFFRON + "22", "none", 6) + t(190, 102, "WATCH", 9, SAFFRON, "hind", 700, "middle")
    return tech("Moisture Reading", LAGOON, [], extra=s)
def past(kind):
    bl = [("tx", "12 Elm St: Past Reports", 11)]
    if kind == "three": bl += [("timeline", [("Oct 2", "Fall visit"), ("Jul 9", "Summer visit"), ("Apr 3", "Spring visit")])]
    else: bl += [("lbl", "2026"), ("timeline", [("Oct 2", "Fall visit"), ("Jul 9", "Summer visit")]), ("lbl", "2025"), ("timeline", [("Oct 4", "Fall visit")])]
    return tech("Past Reports", LAGOON, bl)
def certs(kind):
    b = [("tags", ["Certified Tech", "Moisture Scan", "Licensed & Insured"], True)]
    if kind == "profile": return tech("Certifications", LAGOON, [("tx", "Marcus, Certified Tech", 11)] + b + [("card", "Today", "4 visits", LAGOON, "", "dot", 34, "left")])
    return tech("Certifications", LAGOON, [("tx", "Today", 11)] + b + [("map", 70), ("card", "Next: 12 Elm St", "9:00", LAGOON, "", "dot", 34, "left")])
def contact(kind):
    bl = [("card", "Jane Doe, 12 Elm St", "Member since 2025", LAGOON, "", "dot", 40, "left")]
    bl += [("btn", "Message In The App", "fill", LAGOON)] if kind == "msg" else [("btn2", "Call", "Text", LAGOON)]
    return tech("Member Contact", LAGOON, bl)
def record(kind):
    if kind == "tiles": return tech("Home Record", LAGOON, [("tx", "Home Record", 11), ("tiles", [("Furnace", "home"), ("Water Heater", "clock"), ("Sump Pump", "down"), ("Dryer", "star")], 2, 40)])
    return tech("Home Record", LAGOON, [("tx", "Home Record", 11), ("table", [("Furnace", "Carrier, 2016"), ("Water heater", "Rheem, 2019"), ("Sump pump", "Zoeller, 2021"), ("Roof", "Asphalt, 2014"), ("Windows", "Vinyl, 2010")])])
TTC = D("technician-page-today-route-and-checklist-order-deck", "Technician Page: Today, Directions And Checklist Order", "technician-today-checklist", "ttc3_",
  "upkeep-technician-page-deck-checklist-today", "Follow-on of Technician Page: Checklist & Today (5/10): directions, checklist order (Max: a step-by-step guide with a proposed order), member notes re-asked; contact and home record asked again.",
  "Directions and checklist order re-asked from Max's note, member note chips, map-first Today, photo proof on a ticked task, moisture entry, past reports, badges, contact, home record.", [
 ("Navigation", Q(TA + " Today", "Directions", "how the tech starts directions on the map-first Today view."),
  o("next", "One Navigate To Next Button", "one button for the next job", "practical", nav_next()), o("each", "Navigate On Each Job", "a button on every row", "calm", nav_each())),
 ("Checklist", Q(TA + " Checklist", "Proposed order", "how the step-by-step guide shows its proposed order."),
  o("order", "One Numbered List", "the whole visit in order", "calm", checklist("order")), o("area", "Numbered Inside Areas", "areas in order, steps inside", "practical", checklist("area"))),
 ("Notes For The Member", Q(TA + " Visit Report", "Note for the member", "how the tech writes the note the member reads."),
  o("chips", "Phrase Chips Plus Free Text", "tap chips, then add words", "practical", notes("chips")), o("text", "Free Text With Suggestions", "type, with suggestions under", "calm", notes("text"))),
 ("Today", Q(TA + " Today", "Map first", "what sits under the map."),
  o("each", "List Of Today's Jobs", "numbered rows to match the pins", "practical", nav_each()), o("next", "Next Job Card Only", "one card for the next stop", "calm", nav_next())),
 ("Checklist", Q(TA + " Checklist", "Ticked task with photo", "how the required photo shows on a ticked row."),
  o("thumb", "Small Photo On The Row", "a thumbnail at the right", "practical", ticked("thumb")), o("count", "Photo Count Chip", "a small '2 photos' chip", "calm", ticked("count"))),
 ("Readings", Q(TA + " Readings", "Typing a moisture number", "what helps the tech type the number fast."),
  o("keys", "Big Number Keypad", "large keys under the box", "practical", moist("keys")), o("last", "Last Visit's Reading", "shows the last number under it", "calm", moist("last"))),
 ("Past Reports", Q(TA + " Past Reports", "This home's history", "how far back the list goes at first."),
  o("three", "Last Three Visits", "a short list", "calm", past("three")), o("year", "All Visits By Year", "grouped by year", "practical", past("year"))),
 ("Certifications", Q(TA + " Profile", "Certification badges", "where the badges show for the tech."),
  o("profile", "On The Tech's Profile", "under the name", "calm", certs("profile")), o("today", "Top Of Today", "seen every morning", "bold", certs("today"))),
 ("Member Contact", Q(TA + " Job Card", "Reaching the member", "how the tech reaches the member from a job."),
  o("msg", "Message In The App", "one chat for everything", "practical", contact("msg")), o("call", "Call And Text Buttons", "the phone's own apps", "calm", contact("call"))),
 ("Home Record", Q(TA + " Job Card", "Home record", "how the tech sees the home's record before the visit."),
  o("tiles", "Appliance Tiles", "tap a tile for details", "practical", record("tiles")), o("full", "The Full Record", "one list of everything", "calm", record("full"))),
], reasked=["02", "03", "06", "09", "10"])
def walk(kind):
    if kind == "step":
        s = t(20, 70, "STEP 3 OF 12", 7.5, LAGOON, "hind", 700) + t(20, 90, "Sump Pump", 16, INK, "khand", 700) + photo(14, 98, 212, 80, LAGOON, "house", 6) + rect(14, 186, 212, 26, LAGOON, "none", 4) + t(120, 203, "NEXT STEP", 8, "#FFFFFF", "hind", 700, "middle")
        s += rect(180, 60, 46, 16, "#FFFFFF", LAGOON, 8) + t(203, 71, "Full List", 7, LAGOON, "hind", 700, "middle")
    else:
        s = t(20, 70, "WALK BEGINS: STEP BY STEP", 7.5, LAGOON, "hind", 700) + t(20, 90, "Sump Pump", 16, INK, "khand", 700) + photo(14, 98, 212, 80, LAGOON, "house", 6) + rect(14, 186, 212, 26, LAGOON, "none", 4) + t(120, 203, "NEXT STEP", 8, "#FFFFFF", "hind", 700, "middle")
        s += rect(96, 216, 48, 4, "#D6D0C6", "none", 2) + t(120, 230, "Pull up for the full list", 7, MUTE, "hind", 400, "middle")
    return tech("Walkthrough", LAGOON, [], extra=s)
def skipped(kind):
    rows = [("1. Furnace filter", "done"), ("2. Water heater", "skip"), ("3. Sump pump", "done"), ("4. Gutters", "now")]
    s = ""; y = 62
    for a, st in rows:
        c = JUNGLE if st == "done" else (SAFFRON if st == "skip" else LAGOON)
        s += rect(14, y, 212, 26, "#FFFFFF" if st != "now" else LAGOON + "12", LINE, 4) + t(22, y + 17, a, 8.5, INK, "hind", 600)
        if st == "skip": s += t(218, y + 17, "SKIPPED" if kind == "flag" else "", 7, SAFFRON, "hind", 700, "end")
        y += 30
    if kind == "end": s += t(20, y + 12, "LEFT FOR THE END", 7.5, SAFFRON, "hind", 700) + rect(14, y + 18, 212, 26, "#FFFFFF", SAFFRON, 4) + t(22, y + 35, "2. Water heater", 8.5, INK, "hind", 600)
    return tech("Skip For Now", LAGOON, [("tx", "Full List", 11)], extra=s)
def before(kind):
    s = t(20, 72, "Sump Pump", 14, INK, "khand", 700)
    if kind == "big": s += rect(14, 84, 212, 104, SOFT, "none", 6) + ic("star", 104, 118, 32, LAGOON, 2) + rect(14, 196, 212, 28, LAGOON, "none", 4) + t(120, 214, "TAKE BEFORE PHOTO", 8.5, "#FFFFFF", "hind", 700, "middle")
    else: s += photo(14, 84, 212, 80, LAGOON, "house", 6) + t(20, 176, "Example: whole pump and pit in frame", 7.5, MUTE) + rect(14, 186, 212, 30, LAGOON, "none", 4) + t(120, 205, "TAKE BEFORE PHOTO", 8.5, "#FFFFFF", "hind", 700, "middle")
    return tech("Before Photo", LAGOON, [], extra=s)
def checkin(kind):
    bar = rect(14, 0, 212, 34, LAGOON + "1A", "none", 17) + f'<circle cx="31" cy="17" r="13" fill="{LAGOON}"/>' + t(130, 21, "SLIDE TO CHECK IN", 8, LAGOON, "hind", 700, "middle")
    s = t(20, 72, "12 Elm St", 16, INK, "khand", 700) + t(20, 86, "Fall visit, 9:00", 8, MUTE)
    if kind == "bottom": s += rect(14, 94, 212, 90, SOFT, "none", 6) + f'<g transform="translate(0,190)">{bar}</g>'
    else: s += f'<g transform="translate(0,94)">{bar}</g>' + rect(14, 136, 212, 90, SOFT, "none", 6)
    return tech("Check In", LAGOON, [], extra=s)
def checkout(kind):
    bl = [("tx", "Visit Report Ready", 11), ("checks", ["12 tasks done", "18 photos", "1 item to watch"], JUNGLE, 3)]
    bl += [("btn", "Send Report & Check Out", "fill", LAGOON)] if kind == "one" else [("btn", "1. Send Report", "fill", LAGOON), ("btn", "2. Check Out", "line", LAGOON)]
    return tech("Check Out", LAGOON, bl)
def live(kind):
    s = t(20, 72, "Basement, north wall", 10, INK, "khand", 700)
    if kind == "chip": s += rect(14, 80, 140, 36, "#FFFFFF", LINE, 4, 1.2) + t(24, 104, "18", 18, INK, "khand", 700) + rect(160, 84, 60, 28, SAFFRON + "22", "none", 6) + t(190, 102, "WATCH", 9, SAFFRON, "hind", 700, "middle")
    else: s += rect(14, 80, 212, 36, SAFFRON + "12", SAFFRON, 4, 2.2) + t(24, 104, "18", 18, INK, "khand", 700) + t(216, 104, "watch", 8, SAFFRON, "hind", 700, "end")
    return tech("Live Reading", LAGOON, [], extra=s)
def timer(kind):
    s = rect(14, 58, 212, 24, LAGOON + "12") + t(20, 74, "12 Elm St", 9.5, INK, "khand", 700) + t(220, 74, "0:42" if kind == "el" else "0:42 / 1:30", 9.5, LAGOON, "khand", 700, "end")
    s += "".join(rect(14, 92 + i * 30, 212, 26, "#FFFFFF", LINE, 4) + t(22, 109 + i * 30, x, 8.5, INK, "hind", 600) for i, x in enumerate(["1. Furnace filter", "2. Water heater", "3. Sump pump", "4. Gutters"]))
    return tech("Visit Timer", LAGOON, [], extra=s)
def preview(kind):
    s = rect(14, 58, 212, 180, "#FFFFFF", LINE, 6) + t(22, 76, "Your Fall Visit Report", 11, INK, "khand", 700) + photo(22, 84, 196, 50, LAGOON, "house", 4)
    secs = ["Photos", "What we did", "What to watch"]
    for i, x in enumerate(secs):
        s += t(22, 152 + i * 22, x, 9, INK, "hind", 600) + (rect(184, 142 + i * 22, 30, 14, "#FFFFFF", LAGOON, 7) + t(199, 152 + i * 22, "Edit", 6.5, LAGOON, "hind", 700, "middle") if kind == "each" else "")
    if kind == "one": s += rect(22, 212, 196, 20, "#FFFFFF", LAGOON, 4) + t(120, 225, "EDIT REPORT", 7.5, LAGOON, "hind", 700, "middle")
    return tech("Report Preview", LAGOON, [], extra=s)
def fade(kind):
    s = rect(14, 58, 212, 30, SAFFRON + "1A", "none", 6) + ic("clock", 22, 66, 14, SAFFRON, 2) + t(42, 77, "40 Oak Ave moved to 1:00", 8.5, INK, "hind", 600)
    s += t(120, 100, "fades after a few seconds" if kind == "time" else "fades when you scroll", 7, MUTE, "hind", 400, "middle") + "".join(rect(14, 110 + i * 30, 212, 26, "#FFFFFF", LINE, 4) + t(22, 127 + i * 30, x, 8.5, INK, "hind", 600) for i, x in enumerate(["1. 12 Elm St", "2. 7 Pine Ct", "3. 40 Oak Ave"]))
    return tech("Schedule Change", LAGOON, [], extra=s)
def firstmap(kind):
    s = t(20, 72, "First Visit: Map This Home", 11, INK, "khand", 700)
    if kind == "plan": s += rect(14, 80, 212, 120, SOFT, "none", 4) + rect(30, 92, 80, 50, "#FFFFFF", LINE) + rect(118, 92, 90, 96, "#FFFFFF", LINE) + rect(30, 148, 80, 40, "#FFFFFF", LINE) + "".join(f'<path d="M{x} {y} q-6 -10 0 -14 q6 4 0 14z" fill="{LAGOON}"/>' for x, y in [(60, 120), (150, 130), (70, 172)]) + t(20, 214, "Drop a pin for the furnace, sump, panel...", 7.5, MUTE)
    else: s += "".join(photo(14 + (i % 2) * 108, 80 + (i // 2) * 62, 104, 56, LAGOON, "house", 4) for i in range(4)) + t(20, 214, "Snap each spot, label it once", 7.5, MUTE)
    return tech("First Visit Map", LAGOON, [], extra=s)
TWK = D("technician-page-walk-steps-check-in-and-home-map-deck", "Technician Page: Walk Steps, Check-In And Home Map", "technician-walk-steps", "twk3_",
  "upkeep-technician-page-walkthrough-and-check-in-deck", "Follow-on of Technician Page: Walkthrough And Check-In (10/10): full list before the walk, step by step during it with a way back to the list (Max's note), first-visit home map (Max's note on WWTCO).",
  "Getting back to the full list mid-walk (Max's note), skipped steps, before photo, check in and out, live readings, timer, preview, fading alerts, the first-visit home map.", [
 ("Walkthrough", Q(TA + " Walkthrough", "Back to the full list", "how the tech jumps from the step screen back to the full list."),
  o("btn", "Full List Button", "a small button at the top", "practical", walk("step")), o("pull", "Pull Up For The List", "a sheet from the bottom", "calm", walk("pull"))),
 ("Walkthrough", Q(TA + " Walkthrough", "Skip for now", "where skipped steps go."),
  o("end", "Moved To The End", "a 'left for the end' group", "practical", skipped("end")), o("flag", "Flagged In Place", "stays in order with a tag", "calm", skipped("flag"))),
 ("Photos", Q(TA + " Walkthrough", "Take before photo button", "what the button that blocks the start looks like."),
  o("big", "Big Camera Button", "full-width button, empty frame", "bold", before("big")), o("ex", "With An Example Photo", "shows what to frame", "practical", before("ex"))),
 ("Check In And Out", Q(TA + " Job Card", "Slide to check in", "where the slide bar sits."),
  o("bottom", "At The Bottom", "thumb reach", "practical", checkin("bottom")), o("top", "Under The Address", "seen first", "calm", checkin("top"))),
 ("Check In And Out", Q(TA + " Visit Report", "Check out with the report", "whether sending and checking out are one tap or two."),
  o("one", "One Button For Both", "send report and check out", "practical", checkout("one")), o("two", "Two Steps", "send, then check out", "calm", checkout("two"))),
 ("Readings", Q(TA + " Readings", "Live dry watch or wet", "how the live word shows as the tech types."),
  o("chip", "Word Chip Beside The Box", "a colored chip", "practical", live("chip")), o("border", "Colored Box Border", "the box itself changes color", "bold", live("border"))),
 ("Job Timer", Q(TA + " Job Card", "Timer in the header", "what the running timer shows."),
  o("el", "Time So Far", "just the running time", "calm", timer("el")), o("plan", "Time So Far And Planned", "running and planned time", "practical", timer("plan"))),
 ("Submit", Q(TA + " Report Preview", "Full screen preview", "how the tech fixes something in the preview."),
  o("each", "Edit On Each Section", "small edit buttons", "practical", preview("each")), o("one", "One Edit Button", "back to the draft", "calm", preview("one"))),
 ("Schedule Changes", Q(TA + " Today", "Fading schedule alert", "when the info-only alert fades."),
  o("time", "After A Few Seconds", "fades on its own", "calm", fade("time")), o("scroll", "When You Scroll", "stays until you move", "practical", fade("scroll"))),
 ("Home Map", Q(TA + " First Visit", "Mapping the home", "how the tech maps spots on the first visit so later walks are faster."),
  o("plan", "Pins On A Floor Plan", "drop a pin per spot", "practical", firstmap("plan")), o("photo", "A Photo Per Spot", "snap and label each spot", "calm", firstmap("photo"))),
])
def sl_open(kind):
    s = rect(0, 0, 320, 180, "#E9EEF0") + photo(150, 40, 150, 110, LAGOON, "house", 0) + rect(170, 110, 110, 40, "#FFFFFF", TERRA)
    if kind == "story": s += stx(18, 40, "Jane Skipped One", 18) + stx(18, 60, "Gutter Check.", 18) + t(18, 82, "It cost $ in water damage.", 9, MUTE) + t(18, 160, "...then: Your Home, Taken Care Of.", 8, TERRA, "hind", 600)
    else: s += stx(18, 44, "Your Home,", 22) + stx(18, 68, "Taken Care Of.", 22, TERRA) + t(18, 92, "Then Jane's story", 9, MUTE)
    return slidecard("Opening Slide", TERRA, s, "Over the van shot")
def sl_app(kind):
    sc = 1
    inner = mini([("tx", "Investor Pitch", 12), ("photo", 70, LAGOON, "house", ""), ("dots", 10, 2)]) if kind == "swipe" else mini([("tx", "Investor Pitch", 12), ("h", "The Problem", 12), ("p", "Homes get skipped", 40), ("h", "Our Answer", 12), ("p", "One membership", 40)])
    s = phone(70, 34, 100, 300, inner, 100 / 240) + t(120, 190, "Swipe slide to slide" if kind == "swipe" else "One long scroll", 9, INK, "khand", 700, "middle")
    return card("Pitch App", LAGOON, s, True)
def sl_demo(kind):
    s = rect(0, 0, 320, 180, "#FFFFFF")
    if kind == "frame": s += rect(130, 14, 60, 152, INK, "none", 10) + rect(134, 22, 52, 136, "#DCE9EF") + f'<circle cx="160" cy="90" r="12" fill="#FFFFFFCC"/><path d="M156 84 L166 90 L156 96 Z" fill="{INK}"/>'
    else: s += rect(0, 0, 320, 180, "#DCE9EF") + f'<circle cx="160" cy="90" r="16" fill="#FFFFFFCC"/><path d="M155 82 L168 90 L155 98 Z" fill="{INK}"/>'
    return slidecard("Demo Slide", JUNGLE, s, "Screen recording, just before the ask")
def sl_cal(kind):
    s = stx(18, 30, "The Problem", 18)
    import math
    if kind == "ring": s += "".join(f'<path d="M{160 + 60 * math.cos(i * math.pi / 6 - math.pi / 2):.1f} {104 + 60 * math.sin(i * math.pi / 6 - math.pi / 2):.1f} L{160 + 40 * math.cos(i * math.pi / 6 - math.pi / 2):.1f} {104 + 40 * math.sin(i * math.pi / 6 - math.pi / 2):.1f}" stroke="{ACC[i // 3]}" stroke-width="14"/>' for i in range(12)) + t(160, 108, "A Year", 10, INK, "khand", 700, "middle")
    else: s += "".join(rect(30 + (i % 6) * 44, 50 + (i // 6) * 60, 40, 54, ACC[(i // 3) % 4] + "22") + t(50 + (i % 6) * 44, 64 + (i // 6) * 60, "JFMAMJJASOND"[i], 9, INK, "hind", 700, "middle") + rect(36 + (i % 6) * 44, 72 + (i // 6) * 60, 28, 4, ACC[(i // 3) % 4]) for i in range(12))
    return slidecard("Seasonal Tasks", SAFFRON, s, "Every task a home needs in a year")
def sl_half(side):
    a, b = (0, 160) if side == "right" else (160, 0)
    s = rect(b, 0, 160, 180, "#F4EFE8") + photo(b + 30, 40, 100, 100, LAGOON, "house", 0) + stx(a + 18, 60, "The Problem", 18) + t(a + 18, 82, "Homes get skipped.", 9, MUTE)
    return slidecard("Slide Look", TERRA, s, "White slide, illustration half")
def sl_bars(c):
    s = stx(18, 30, "Members", 18) + sbars(40, 160, [2, 3, 5, 8, 12], LAGOON, 4, 30, 18) + rect(200, 40, 100, 34, c) + t(250, 61, "Break-even here", 9, "#FFFFFF", "hind", 700, "middle")
    return slidecard("Pitch Chart", c, s, "Bars with a callout")
def sl_founder(kind):
    s = stx(18, 30, "Why We Built This", 16)
    if kind == "photo": s += rect(18, 44, 80, 100, CREAM) + g(28, 52, .38, person()) + "".join(t(110, 60 + i * 16, x, 9, INK) for i, x in enumerate(["A home builder who saw", "the same skipped jobs", "turn into big bills."])) + "".join(dot(120 + i * 40, 150, 10, "#D6D0C6") for i in range(4)) + t(110, 172, "Advisors", 8, MUTE, "hind", 600)
    else: s += f'<line x1="20" y1="100" x2="300" y2="100" stroke="{INK}" stroke-width="2"/>' + "".join(dot(40 + i * 86, 100, 6, ACC[i]) + t(40 + i * 86, 122, x, 8, INK, "hind", 600, "middle") for i, x in enumerate(["Building homes", "Saw the gap", "First members", "Today"])) + "".join(dot(120 + i * 40, 152, 10, "#D6D0C6") for i in range(4)) + t(110, 174, "Advisors", 8, MUTE, "hind", 600)
    return slidecard("Founder Slide", JUNGLE, s, "Founder story with an advisor row")
def sl_close(kind):
    if kind == "van": s = rect(0, 0, 320, 180, "#F6E3D6") + rect(90, 90, 140, 56, "#FFFFFF", TERRA, 4, 2) + dot(115, 150, 10, INK) + dot(205, 150, 10, INK) + stx(160, 50, "Every Home, Taken Care Of.", 16, a="middle")
    else: s = rect(0, 0, 320, 180, "#FFFFFF") + rect(40, 40, 240, 120, SOFT) + "".join(dot(60 + (i * 37) % 220, 50 + (i * 23) % 100, 3, TERRA) for i in range(40)) + stx(160, 30, "Every Home, Taken Care Of.", 14, a="middle")
    return slidecard("Closing Slide", TERRA, s, "End on the vision")
def sl_sol(kind):
    s = stx(18, 30, "Our Answer", 18)
    if kind == "side": s += rect(18, 44, 136, 120, "#FFFFFF", LINE) + stx(28, 64, "Membership", 12, TERRA) + t(28, 82, "Seasonal visits, one price", 8, MUTE) + rect(166, 44, 136, 120, "#FFFFFF", LINE) + stx(176, 64, "Tech App", 12, LAGOON) + t(176, 82, "Walkthrough, reports", 8, MUTE)
    else: s += rect(18, 44, 284, 56, "#FFFFFF", LINE) + stx(28, 64, "Membership", 12, TERRA) + t(28, 82, "Seasonal visits, one price", 8, MUTE) + rect(18, 108, 284, 56, "#FFFFFF", LINE) + stx(28, 128, "Powered By Our Tech App", 12, LAGOON)
    return slidecard("Solution Slide", LAGOON, s, "Membership and the tech app")
def sl_order(kind):
    seq = ["Problem", "Answer", "Market", "Model", "Traction", "Demo", "Team", "Ask", "Vision"] if kind == "before" else ["Problem", "Answer", "Market", "Model", "Traction", "Demo", "Ask", "Team", "Vision"]
    s = "".join(rect(10 + (i % 5) * 62, 30 + (i // 5) * 70, 56, 50, (TERRA + "22" if x == "Team" else "#FFFFFF"), LINE) + t(38 + (i % 5) * 62, 60 + (i // 5) * 70, x, 8.5, INK, "hind", 600, "middle") for i, x in enumerate(seq))
    return slidecard("Slide Order", INK, s, "Ten tight slides, team late")
IPS = D("investor-pitch-story-slide-looks-and-pitch-app-deck", "Investor Pitch: Story, Slide Looks And Pitch App", "investor-pitch-story-looks", "ips3_",
  "upkeep-investor-pitch-deck-story-style-deck", "Follow-on of Investor Pitch: Story & Style (9/10) and Slide Looks (9/10): opening (problem story vs brand promise, both picked), the pitch as an app (Max: 'Gonna make an app'), demo, look, charts, founder, close.",
  "Opening order (two picks to reconcile), the pitch app format (Max's note), demo framing, seasonal calendar, illustration side, chart callout, founder slide, close, solution, team spot.", [
 ("Opening", Q(IP + " Opening Slide", "Problem story and brand promise", "which one comes first, since you picked both in two decks."),
  o("story", "Problem Story First", "Jane's story, then the promise", "practical", sl_open("story")), o("promise", "Brand Promise First", "promise over the van, then the story", "bold", sl_open("promise"))),
 ("Format", Q(IP + " Pitch App", "Pitch as an app", "how the pitch moves inside the app you plan to make."),
  o("swipe", "Swipe Slide To Slide", "one slide per screen", "practical", sl_app("swipe")), o("scroll", "One Long Scroll", "a story you scroll down", "calm", sl_app("scroll"))),
 ("Product Demo", Q(IP + " Demo Slide", "Full-slide recording", "how the screen recording is framed."),
  o("frame", "Inside A Phone Frame", "the phone drawn around it", "calm", sl_demo("frame")), o("bleed", "Edge To Edge", "the recording fills the slide", "bold", sl_demo("bleed"))),
 ("Problem", Q(IP + " Problem Slide", "Seasonal task calendar", "how the year of tasks is drawn."),
  o("ring", "A Year Ring", "months around a circle", "playful", sl_cal("ring")), o("grid", "A Month Grid", "twelve boxes in rows", "practical", sl_cal("grid"))),
 ("Slide Look", Q(IP + " Slide Look", "Illustration half", "which side the illustration sits on."),
  o("right", "Illustration On The Right", "words left", "calm", sl_half("right")), o("left", "Illustration On The Left", "words right", "bold", sl_half("left"))),
 ("Pitch Charts", Q(IP + " Chart Slides", "Callout box color", "the color of the callout on the bar charts."),
  o("terra", "Terracotta Callout", "brand pop", "bold", sl_bars(TERRA)), o("ink", "Ink Callout", "quiet, data first", "calm", sl_bars(INK))),
 ("Team", Q(IP + " Founder Slide", "Founder story", "how the founder story is told above the advisor row."),
  o("photo", "Photo And Three Lines", "a short story", "calm", sl_founder("photo")), o("tl", "A Short Timeline", "builder to founder", "practical", sl_founder("tl"))),
 ("Closing", Q(IP + " Closing Slide", "Vision", "the picture behind the closing line."),
  o("van", "Van At Dusk", "the brand shot", "bold", sl_close("van")), o("map", "Map Of Homes Covered", "the coverage dream", "practical", sl_close("map"))),
 ("Solution", Q(IP + " Solution Slide", "Membership and tech app", "how the two parts of the answer share the slide."),
  o("side", "Side By Side", "two equal boxes", "practical", sl_sol("side")), o("stack", "Membership On Top", "the app under it", "calm", sl_sol("stack"))),
 ("Team", Q(IP + " Slide Order", "Team slide spot", "where the late team slide sits."),
  o("before", "Just Before The Ask", "team, then ask", "calm", sl_order("before")), o("after", "Right After The Ask", "ask, then team", "practical", sl_order("after"))),
], reasked=["04", "09"])
CH = "#3D3A36"; KH = "#B59B73"
def kit(label, people, cap): return crew(label, TERRA, people, False, cap)
ATT = D("employee-attire-pant-shirt-and-shoe-options-deck", "Employee Attire: Pant, Shirt And Shoe Options", "employee-attire-options", "att3_",
  "upkeep-employee-attire-work-polo-and-layers-deck", "Follow-on of Employee Attire (10/10) and Work Polo And Layers (9/10): pants re-asked with Max's note (a few options of pants, shirts and shoes), rain jackets, long sleeves, caps, layers, shoe covers.",
  "A few choices of pants, shirts and shoes (Max's note), rain jacket logo, winter sleeves, caps, back print on layers, names on layers, cover carry, new-hire kit.", [
 ("Work Pants", Q("UpKeep Crew Uniform", "Pants choices", "which pants a tech can pick from each day."),
  o("two", "Charcoal Or Khaki Cargo", "two choices", "practical", kit("Pants Choices", [P(), P(pants=KH, cargo=True, skin=SKIN[1], hair=HAIR[1])], "Charcoal straight or khaki cargo"))
  , o("three", "Plus Charcoal Cargo", "three choices", "practical", kit("Pants Choices", [P(), P(pants=KH, cargo=True, skin=SKIN[1], hair=HAIR[1]), P(cargo=True, skin=SKIN[2], hair=HAIR[2])], "Charcoal, khaki cargo, charcoal cargo"))),
 ("Shirts", Q("UpKeep Crew Uniform", "Shirt choices", "which shirts a tech can pick from."),
  o("polos", "Terracotta Or Charcoal Polo", "two polos", "practical", kit("Shirt Choices", [P(), P(polo=CH, collar=TERRA, skin=SKIN[1], hair=HAIR[1])], "Terracotta polo or charcoal with terracotta collar"))
  , o("tee", "Plus A Hot-Day Tee", "two polos and a tee", "playful", kit("Shirt Choices", [P(), P(polo=CH, collar=TERRA, skin=SKIN[1], hair=HAIR[1]), P(skin=SKIN[2], hair=HAIR[2], logo="left")], "Adds a terracotta tee for hot days"))),
 ("Shoes", Q("UpKeep Crew Uniform", "Shoe choices", "how many shoe choices a tech gets."),
  o("two", "Two Styles", "athletic or work boot", "practical", kit("Shoe Choices", [P(), P(shoe="boot", skin=SKIN[1], hair=HAIR[1])], "Athletic work shoe or work boot"))
  , o("one", "One Shoe, Two Colors", "all black or terracotta stripe", "calm", kit("Shoe Choices", [P(), P(skin=SKIN[1], hair=HAIR[1])], "Same shoe, black or with a stripe"))),
 ("Seasonal Layers", Q("UpKeep Crew Uniform", "Rain jacket logo", "where the logo goes on the charcoal and terracotta rain jackets."),
  o("chest", "Chest Logo Only", "plain back", "calm", kit("Rain Jacket", [P(layer="rain", layerc=CH), P(layer="rain", layerc=TERRA, skin=SKIN[1], hair=HAIR[1])], "Chest logo"))
  , o("back", "Chest And Back Wordmark", "same as the polo", "bold", kit("Rain Jacket", [P(layer="rain", layerc=CH, back=True), P(layer="rain", layerc=TERRA, skin=SKIN[1], hair=HAIR[1], back=True)], "Big wordmark on the back"))),
 ("Polo Color", Q("UpKeep Crew Uniform", "Winter long-sleeve polo", "which color the long-sleeve winter polo comes in."),
  o("terra", "Terracotta Long Sleeve", "the everyday color", "bold", kit("Winter Polo", [P(layer="quarterzip", layerc=TERRA)], "Long-sleeve terracotta")), o("both", "Terracotta And Charcoal", "both colors in long sleeve", "practical", kit("Winter Polo", [P(layer="quarterzip", layerc=TERRA), P(layer="quarterzip", layerc=CH, polo=CH, skin=SKIN[1], hair=HAIR[1])], "Both colors"))),
 ("Hats", Q("UpKeep Crew Uniform", "Cap choices", "whether techs also get a terracotta cap."),
  o("white", "White Cap Only", "mark on the front", "calm", kit("Caps", [P(hat="cap", hatc="#FFFFFF")], "White cap, terracotta mark")), o("two", "White Or Terracotta Cap", "a choice of two", "playful", kit("Caps", [P(hat="cap", hatc="#FFFFFF"), P(hat="cap", hatc=TERRA, skin=SKIN[1], hair=HAIR[1])], "Pick either"))),
 ("Logo Placement", Q("UpKeep Crew Uniform", "Back wordmark on layers", "whether the big back wordmark also goes on the softshell."),
  o("yes", "On The Softshell Too", "seen from behind all year", "bold", kit("Back Print", [P(layer="softshell", layerc=CH, back=True)], "Wordmark on the softshell")), o("no", "Polo Only", "softshell back plain", "calm", kit("Back Print", [P(back=True)], "Wordmark on the polo only"))),
 ("Name Patch", Q("UpKeep Crew Uniform", "Name on layers", "whether the printed first name goes on jackets too."),
  o("yes", "Name On Layers Too", "always seen", "practical", kit("Name", [P(layer="softshell", layerc=CH, patch="printed")], "First name on the softshell")), o("no", "Name On The Polo Only", "layers stay plain", "calm", kit("Name", [P(patch="printed")], "First name on the polo"))),
 ("Shoes", Q("UpKeep Crew Uniform", "Shoe cover carry", "where the reusable terracotta covers live between homes."),
  o("pouch", "Belt Pouch", "on the tech", "practical", kit("Shoe Covers", [P(covers=TERRA)], "Pouch on the belt")), o("van", "Van Bin By The Door", "grab on the way in", "calm", kit("Shoe Covers", [P(), P(covers=TERRA, skin=SKIN[1], hair=HAIR[1])], "A bin in the van"))),
 ("Crew Kit", Q("UpKeep Crew Handbook", "New-hire kit", "how the uniform choices are shown to a new tech."),
  o("line", "A Lineup Photo", "every piece on people", "bold", kit("New-Hire Kit", [P(), P(polo=CH, collar=TERRA, pants=KH, cargo=True, skin=SKIN[1], hair=HAIR[1]), P(layer="softshell", layerc=CH, skin=SKIN[2], hair=HAIR[2])], "Every option on the crew")),
  o("list", "A Kit List Card", "pieces and how many", "practical", U("New-Hire Kit", TERRA, [("tx", "Your Uniform Kit", 12), ("table", [("Polos", "3 terracotta, 2 charcoal"), ("Long-sleeve polo", "2"), ("Pants", "pick 3 of 3 styles"), ("Shoes", "1 pair, your style"), ("Softshell", "1"), ("Rain jacket", "1"), ("Cap", "1"), ("Shoe covers", "2 pairs")])], 30))),
], reasked=["06"])
def fchart(legend="dots", flags=True, band=True, rough="tag", callouts=0, h=110):
    s = axes(20, 64, 200, h) if False else ""
    y0 = 70 + h; s += f'<line x1="20" y1="{y0}" x2="220" y2="{y0}" stroke="{LINE}"/><line x1="20" y1="70" x2="20" y2="{y0}" stroke="{LINE}"/>'
    s += rect(150, 70, 70, h, SOFT) + (t(185, 82, "ROUGH", 7, MUTE, "hind", 700, "middle") if rough == "tag" else t(220, y0 + 12, "* years 4-5 rough", 6.5, MUTE, "hind", 400, "end"))
    if band: s += f'<path d="M20 {y0 - 6} L220 {y0 - h + 10} L220 {y0 - h + 50} L20 {y0 - 2} Z" fill="{LAGOON}1F"/>'
    s += sline(20, y0, 200, h - 14, [5, 14, 30, 52, 80, 110], TERRA, 2.6, vmax=140) + sline(20, y0, 200, h - 14, [4, 10, 20, 34, 50, 70], LAGOON, 1.6, vmax=140) + sline(20, y0, 200, h - 14, [6, 18, 40, 70, 104, 140], JUNGLE, 1.6, vmax=140)
    if flags: s += f'<line x1="86" y1="70" x2="86" y2="{y0}" stroke="{JUNGLE}" stroke-dasharray="3 2"/><line x1="52" y1="70" x2="52" y2="{y0}" stroke="{TERRA}" stroke-dasharray="3 2"/>'
    if legend == "dots": s += "".join(dot(26 + i * 64, 60, 3.5, c) + t(33 + i * 64, 63, n, 7, INK, "hind", 600) for i, (n, c) in enumerate([("Essentials", LAGOON), ("Plus", TERRA), ("Complete", JUNGLE)]))
    else: s += "".join(rect(22 + i * 64, 58, 10, 3, c) + t(36 + i * 64, 63, n, 7, INK, "hind", 600) for i, (n, c) in enumerate([("Essentials", LAGOON), ("Plus", TERRA), ("Complete", JUNGLE)]))
    for i in range(callouts): s += f'<circle cx="{[52, 86, 150][i]}" cy="{y0 - [20, 40, 70][i]}" r="7" fill="{INK}"/>' + t([52, 86, 150][i], y0 - [20, 40, 70][i] + 3, str(i + 1), 7, "#FFFFFF", "hind", 700, "middle")
    return s
def F(label, blocks=(), extra="", example=True): return U(label, LAGOON, [("mh", "Smart Upkeep", "Forecast")] + list(blocks), 30, None, example, extra)
def fc_table(kind):
    if kind == "split": s = fchart() + "".join(t(22, 200 + i * 14, a, 7.5, MUTE) + t(218, 200 + i * 14, b, 7.5, INK, "hind", 600, "end") for i, (a, b) in enumerate([("Break-even", "Q3, year 2"), ("Lowest cash", "Q1, year 1"), ("Members, year 3", "example")])) + t(120, 248, "Phone: table under the chart; desktop: beside", 7, MUTE, "hind", 400, "middle")
    else: s = fchart(h=90) + "".join(t(22, 180 + i * 14, a, 7.5, MUTE) + t(218, 180 + i * 14, b, 7.5, INK, "hind", 600, "end") for i, (a, b) in enumerate([("Break-even", "Q3, year 2"), ("Lowest cash", "Q1, year 1"), ("Members, year 3", "example")])) + t(120, 248, "Under the chart on every screen", 7, MUTE, "hind", 400, "middle")
    return F("Key Results", extra=s)
def fc_points(kind):
    s = fchart(callouts=3 if kind == "num" else 0)
    if kind == "num": s += "".join(t(22, 200 + i * 13, f"{i+1}. {x}", 7.5, INK, "hind", 600) for i, x in enumerate(["Lowest cash, then it turns", "Break-even quarter", "Rough years start"]))
    else: s += t(22, 196, "KEY POINTS", 7, LAGOON, "hind", 700) + "".join(t(22, 210 + i * 13, "- " + x, 7.5, INK) for i, x in enumerate(["Break-even in year 2 (example)", "Cash low in year 1", "Years 4-5 are rough"]))
    return F("Key Points", extra=s)
def fc_count(n):
    s = fchart(callouts=min(n, 3)) + "".join(t(22, 196 + i * 11, f"{i+1}. " + x, 7, INK, "hind", 600) for i, x in enumerate(["Lowest cash", "Break-even", "Rough years", "Plus overtakes Essentials", "Churn assumption"][:n]))
    return F("Key Points", extra=s)
def fc_slider(kind):
    sl = rect(0, 0, 0, 0)
    if kind == "under": s = fchart() + t(22, 198, "Churn per month", 7.5, INK, "hind", 600) + rect(22, 206, 196, 4, "#EEEAE4", "none", 2) + f'<circle cx="80" cy="208" r="6" fill="{LAGOON}"/>' + t(218, 198, "2% (example)", 7.5, LAGOON, "hind", 700, "end")
    else: s = "".join(rect(14, 60 + i * 30, 62, 24, "#FFFFFF", LINE, 4) + t(20, 75 + i * 30, x, 6.8, INK, "hind", 600) for i, x in enumerate(["Price", "Visits", "Churn", "Tech cost"])) + f'<circle cx="46" cy="160" r="5" fill="{LAGOON}"/>' + f'<g transform="translate(60,0) scale(.72 1)">{fchart(legend="dots")}</g>'
    return F("Churn Slider", extra=s)
def fc_split(kind):
    parts = [("Tech", 40, TERRA), ("Parts", 15, SAFFRON), ("Overhead", 20, LAGOON), ("Margin", 25, JUNGLE)]
    s = t(22, 72, "Blended Member, per month (example)", 8, INK, "hind", 600); x = 22
    for n, w, c in parts:
        ww = 196 * w / 100; s += rect(x, 80, ww, 30, c) + (t(x + ww / 2, 99, n, 7, "#FFFFFF", "hind", 700, "middle") if kind == "inside" else ""); x += ww
    if kind == "legend": s += "".join(dot(26 + i * 50, 124, 3.5, c) + t(32 + i * 50, 127, n, 7, INK) for i, (n, w, c) in enumerate(parts))
    return F("Split Bar", extra=s)
def fc_tiles(kind):
    tl = [("Revenue", "$"), ("Members", "#"), ("Cash", "$")] if kind == "rev" else [("Break-even", "Q3 Y2"), ("Margin", "%"), ("Churn", "%")]
    s = "".join(rect(14 + i * 80, 60, 74, 46, "#FFFFFF", LINE, 6) + t(22 + i * 80, 76, n, 7, MUTE) + t(22 + i * 80, 98, v, 16, INK, "khand", 700) for i, (n, v) in enumerate(tl)) + t(220, 116, "swipe for more >", 6.5, MUTE, "hind", 400, "end")
    s += f'<g transform="translate(0,64)">{fchart(h=90)}</g>'
    return F("Swipe Tiles", extra=s)
def fc_rough(kind): return F("Rough Years", extra=fchart(rough=kind))
def fc_legend(kind): return F("Legend", extra=fchart(legend=kind))
def fc_plot(kind):
    if kind == "tab": s = "".join(rect(14 + i * 54, 58, 50, 18, (LAGOON if i == 3 else "#FFFFFF"), LAGOON, 9) + t(39 + i * 54, 70, x, 7, "#FFFFFF" if i == 3 else LAGOON, "hind", 700, "middle") for i, x in enumerate(["Base", "Best", "Worst", "Position"])) + f'<line x1="120" y1="86" x2="120" y2="226" stroke="{MUTE}"/><line x1="20" y1="156" x2="220" y2="156" stroke="{MUTE}"/>' + dot(180, 110, 7, TERRA) + t(180, 126, "Smart Upkeep", 7, TERRA, "hind", 700, "middle") + t(120, 84, "Prevent", 7, MUTE, "hind", 600, "middle") + t(120, 236, "Repair", 7, MUTE, "hind", 600, "middle")
    else: s = fchart() + t(120, 210, "The position plot lives in the pitch only", 7.5, MUTE, "hind", 400, "middle")
    return F("Position Plot", extra=s)
def fc_foot(kind):
    s = fchart(h=100) + t(22, 196, "Chart first, then the numbers", 7, MUTE)
    s += (t(22, 214, "Assumptions: price, visits per year, churn, tech cost (example)", 6.5, INK) if kind == "assume" else rect(22, 206, 196, 18, "#FFFFFF", LAGOON, 4) + t(120, 218, "OPEN THE LIVE FORECAST", 7, LAGOON, "hind", 700, "middle"))
    return F("One-Page Summary", extra=s)
FCD = D("financial-forecasting-key-points-and-results-table-deck", "Financial Forecasting: Key Points And Results Table", "forecast-key-points", "fcd3_",
  "upkeep-financial-forecasting-scenario-and-churn-views-deck", "Follow-on of Financial Forecasting (10/10) and Scenario And Churn Views (9/10): results table re-asked (Max: whatever fits better), key points called out (Max's note), the position plot placed (Max's pitch note).",
  "Results table placement (my pick: beside on desktop, under on phone), key points on the chart (Max's note), slider spot, split bar, tiles, rough years, legend, position plot, summary footer.", [
 ("Scenarios", Q(FC, "Key results table", "my pick is beside the chart on desktop and under it on a phone, so is that the one."),
  o("split", "Beside On Desktop, Under On Phone", "fits each screen (my pick)", "practical", fc_table("split")), o("under", "Under The Chart Everywhere", "one layout", "calm", fc_table("under"))),
 ("Key Moments", Q(FC, "Key points", "how the key points you asked for are pointed out."),
  o("num", "Numbered Marks On The Chart", "with a short list under", "practical", fc_points("num")), o("list", "A Key Points List", "under the chart, no marks", "calm", fc_points("list"))),
 ("Key Moments", Q(FC, "How many key points", "how many points get called out at once."),
  o("three", "Three Points", "the big ones", "calm", fc_count(3)), o("five", "Up To Five", "more detail", "practical", fc_count(5))),
 ("Churn", Q(FC, "Churn slider spot", "where the slider that moves break-even and revenue sits."),
  o("under", "Under The Chart", "full width", "practical", fc_slider("under")), o("col", "In The Left Column", "with the other assumptions", "calm", fc_slider("col"))),
 ("Per Member", Q(FC, "Split bar labels", "how each piece of the blended member bar is named."),
  o("inside", "Names Inside The Pieces", "read at a glance", "practical", fc_split("inside")), o("legend", "Legend Under The Bar", "a clean bar", "calm", fc_split("legend"))),
 ("Format", Q(FC + " Phone", "Swipe tiles", "which numbers come first on the swipe tiles."),
  o("rev", "Revenue, Members, Cash", "growth first", "bold", fc_tiles("rev")), o("be", "Break-Even, Margin, Churn", "health first", "practical", fc_tiles("be"))),
 ("Time Horizon", Q(FC, "Rough years label", "how the shaded years four and five are marked."),
  o("tag", "Rough Tag On The Shade", "label on the chart", "practical", fc_rough("tag")), o("note", "A Footnote", "a small note under it", "calm", fc_rough("note"))),
 ("Chart Type", Q(FC, "Legend above the chart", "how each plan is marked in the legend."),
  o("dots", "Colored Dots", "dot and name", "calm", fc_legend("dots")), o("lines", "Short Lines", "line and name", "practical", fc_legend("lines"))),
 ("Market Position", Q(FC, "Position plot", "whether the prevent-or-repair plot also gets a forecast tab."),
  o("tab", "A Position Tab", "next to the scenario tabs", "practical", fc_plot("tab")), o("pitch", "Pitch Only", "the forecast stays numbers", "calm", fc_plot("pitch"))),
 ("Format", Q(FC + " One-Page Summary", "Summary footer", "what sits at the bottom of the printable page."),
  o("assume", "The Assumptions", "what the numbers rest on", "practical", fc_foot("assume")), o("link", "Link To The Live Forecast", "for the latest view", "calm", fc_foot("link"))),
], reasked=["04"])
CORE = [("Furnace", "home"), ("Water Heater", "clock"), ("Sump Pump", "down"), ("Gutters", "home"), ("Dryer Vent", "star"), ("Smoke Alarms", "check"), ("Moisture Scan", "search"), ("Caulk & Seals", "tag")]
def tile(x, y, w, h, n, k, c, tagc=None):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 6) + ((ic(k, x + 7, y + h / 2 - 6, 12, c, 1.8) + t(x + 24, y + h / 2 + 3, n, 7.5, INK, "hind", 600)) if h < 44 else (ic(k, x + 8, y + 8, 14, c, 1.8) + t(x + 8, y + h - 8, n, 7.5, INK, "hind", 600)))
    if tagc: s += rect(x + w - 26, y, 26, 11, tagc, "none", 0) + t(x + w - 13, y + 8, "PROOF", 5.5, "#FFFFFF", "hind", 700, "middle")
    return s
def ww_frame(inner, desk=False):
    s = t(20, 44, "What We Take Care Of", 13, INK, "khand", 700) + t(20, 56, "Every visit, every season.", 7.5, MUTE)
    if desk: return card("Desktop", TERRA, browser(14, 64, 212, 200, inner, 212 / 480) + s, False)
    return card("Phone", TERRA, s + inner, False)
def ww_desk(kind):
    if kind == "rows": inner = rect(0, 0, 480, 452, "#FFFFFF") + "".join(tile(20 + (i % 4) * 112, 40 + (i // 4) * 110, 104, 96, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE))
    else: inner = rect(0, 0, 480, 452, "#FFFFFF") + "".join(tile(20 + i * 120, 60, 112, 140, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:4])) + "".join(dot(200 + i * 12, 230, 3, INK if i == 0 else "#D6D0C6") for i in range(4)) + rect(460, 110, 20, 40, "#FFFFFFDD") + t(470, 136, ">", 16, INK, "hind", 700, "middle")
    return ww_frame(inner, True)
def ww_phone(kind):
    if kind == "car": s = "".join(tile(14 + i * 100, 66, 94, 96, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:3])) + "".join(dot(100 + i * 10, 172, 2.5, INK if i == 0 else "#D6D0C6") for i in range(4))
    else: s = "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 48, 104, 42, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE))
    return ww_frame(s)
def ww_season(kind):
    s = "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 40, 104, 34, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:6]))
    s += "".join(rect(14 + i * 54, 194, 50, 22, (TERRA if (kind == "now" and i == 2) else "#FFFFFF"), TERRA if (kind == "now" and i == 2) else LINE, 11) + t(39 + i * 54, 208, x, 7.5, "#FFFFFF" if (kind == "now" and i == 2) else INK, "hind", 600, "middle") for i, x in enumerate(["Spring", "Summer", "Fall", "Winter"]))
    return ww_frame(s)
def ww_every(kind):
    s = ""
    if kind == "head": s += t(20, 74, "EVERY VISIT", 7, TERRA, "hind", 700) + "".join(tile(14 + (i % 2) * 108, 80 + (i // 2) * 40, 104, 34, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:4])) + t(20, 170, "SEASONAL", 7, LAGOON, "hind", 700) + "".join(tile(14 + (i % 2) * 108, 176 + (i // 2) * 40, 104, 34, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[4:6]))
    else: s += "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 40, 104, 34, n, k, ACC[i % 4]) + (rect(14 + (i % 2) * 108 + 54, 66 + (i // 2) * 40 + 4, 46, 11, TERRA + "1A", "none", 5) + t(14 + (i % 2) * 108 + 77, 66 + (i // 2) * 40 + 12, "every visit", 5.8, TERRA, "hind", 700, "middle") if i < 4 else "") for i, (n, k) in enumerate(CORE[:6]))
    return ww_frame(s)
def ww_map(kind):
    s = rect(14, 66, 212, 100, SOFT, "none", 6) + rect(40, 80, 80, 70, "#FFFFFF", LINE) + rect(124, 80, 80, 70, "#FFFFFF", LINE)
    pts = [(60, 110), (100, 140), (150, 100), (190, 130)]
    if kind == "num": s += pins(pts, TERRA)
    else: s += "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#FFFFFF" stroke="{TERRA}" stroke-width="1.5"/>' + ic(CORE[i][1], x - 6, y - 6, 12, TERRA, 1.6) for i, (x, y) in enumerate(pts))
    s += tile(14, 174, 212, 40, "1. Furnace" if kind == "num" else "Furnace", "home", TERRA)
    return ww_frame(s)
def ww_open(kind):
    s = rect(14, 66, 212, 120 if kind == "photo" else 92, "#FFFFFF", TERRA, 6, 1.3) + ic("home", 22, 74, 14, TERRA) + t(42, 85, "Furnace", 10, INK, "khand", 700)
    s += "".join(t(24, 104 + i * 13, "- " + x, 7.5, INK) for i, x in enumerate(["Filter checked or changed", "Burner and flame look", "Carbon monoxide test"]))
    if kind == "photo": s += photo(24, 144, 90, 36, LAGOON, "house", 3)
    s += tile(14, 194 if kind == "photo" else 166, 104, 34, "Water Heater", "clock", LAGOON) + tile(122, 194 if kind == "photo" else 166, 104, 34, "Sump Pump", "down", JUNGLE)
    return ww_frame(s)
def ww_records(kind):
    s = "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 40, 104, 34, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:4]))
    if kind == "rows": s += rect(14, 150, 212, 56, "#FFFFFF", LINE, 6) + t(22, 166, "Records", 9, INK, "khand", 700) + t(22, 180, "Recall monitoring", 7.5, INK) + t(22, 194, "Warranty check", 7.5, INK)
    else: s += rect(14, 150, 212, 56, "#FFFFFF", LINE, 6) + t(22, 166, "Records", 9, INK, "khand", 700) + ic("search", 30, 176, 18, LAGOON) + ic("check", 120, 176, 18, JUNGLE) + t(52, 190, "Recalls", 7.5, INK) + t(142, 190, "Warranty", 7.5, INK)
    return ww_frame(s)
def ww_tag(c): return ww_frame("".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 48, 104, 42, n, k, ACC[i % 4], c if i in (0, 6) else None) for i, (n, k) in enumerate(CORE)))
def ww_sub(txt):
    s = t(20, 44, "What We Take Care Of", 13, INK, "khand", 700) + t(20, 56, txt, 7.5, MUTE) + "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 48, 104, 42, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE))
    return card("Heading", TERRA, s, False)
def ww_lawn(kind):
    s = "".join(tile(14 + (i % 2) * 108, 66 + (i // 2) * 34, 104, 30, n, k, ACC[i % 4]) for i, (n, k) in enumerate(CORE[:4]))
    if kind == "strip": s += "".join(rect(14 + i * 54, 140, 50, 18, "#FFFFFF", LINE, 9) + t(39 + i * 54, 152, x, 7, INK, "hind", 600, "middle") for i, x in enumerate(["Spring", "Summer", "Fall", "Winter"])); y = 166
    else: y = 140
    s += rect(14, y, 212, 40, JUNGLE + "14", "none", 6) + t(22, y + 17, "Lawn cutting, weekly in season", 8.5, INK, "hind", 600) + rect(22, y + 23, 40, 11, JUNGLE, "none", 5) + t(42, y + 31, "ADD-ON", 6, "#FFFFFF", "hind", 700, "middle")
    if kind != "strip": s += "".join(rect(14 + i * 54, y + 48, 50, 18, "#FFFFFF", LINE, 9) + t(39 + i * 54, y + 60, x, 7, INK, "hind", 600, "middle") for i, x in enumerate(["Spring", "Summer", "Fall", "Winter"]))
    return ww_frame(s)
WWD = D("what-we-take-care-of-carousel-season-strip-and-map-deck", "What We Take Care Of: Carousel, Season Strip And Map Pins", "wwtco-carousel-map", "wwd3_",
  "upkeep-what-we-take-care-of-grid-and-home-map-deck", "Follow-on of What We Take Care Of (10/10) and Grid And Home Map (9/10): the desktop tiles re-asked as Max suggested (maybe a carousel), season strip, map pins, records tile, corner tags, lawn banner.",
  "Desktop carousel (Max's note), phone tiles, season strip, every-visit marking, map pins, opened tile, records tile, corner tag color, subhead line, lawn banner spot.", [
 ("Layout", Q(WW + " Desktop", "Eight core tiles", "whether the tiles become the carousel you suggested."),
  o("car", "A Tile Carousel", "four at a time, arrows and dots", "bold", ww_desk("car")), o("rows", "Two Rows Of Four", "all eight at once", "calm", ww_desk("rows"))),
 ("Layout", Q(WW + " Phone", "Eight core tiles", "how the tiles sit on a phone."),
  o("car", "Swipe Carousel", "big tiles, swipe", "playful", ww_phone("car")), o("grid", "Two-Column Grid", "all eight, scroll down", "practical", ww_phone("grid"))),
 ("Layout", Q(WW, "Season strip", "how the strip under the grid shows the seasons."),
  o("now", "This Season Lit Up", "the current season filled", "bold", ww_season("now")), o("same", "All Seasons Equal", "four plain chips", "calm", ww_season("same"))),
 ("Grouping", Q(WW, "Every visit first", "how the every-visit items are marked."),
  o("head", "An Every Visit Heading", "a group label", "practical", ww_every("head")), o("tag", "A Tag On Each Tile", "small every-visit tags", "calm", ww_every("tag"))),
 ("Layout", Q(WW + " House Map", "Map pins", "what each pin on the house map shows."),
  o("num", "Numbered Pins", "numbers match the cards", "practical", ww_map("num")), o("icon", "Icon Pins", "the system's icon", "playful", ww_map("icon"))),
 ("Tap To Expand", Q(WW, "Opened tile", "what an opened tile shows in place."),
  o("photo", "Checklist And A Photo", "what we check plus a visit photo", "bold", ww_open("photo")), o("list", "Checklist Only", "just what we check", "calm", ww_open("list"))),
 ("Trust Badges", Q(WW, "Records tile", "how recall monitoring and warranty check show inside the records tile."),
  o("rows", "Two Text Rows", "one line each", "calm", ww_records("rows")), o("icons", "Two Icons With Words", "icon over each", "practical", ww_records("icons"))),
 ("Trust Badges", Q(WW, "Corner proof tag", "the color of the small corner tag on a tile."),
  o("lagoon", "Lagoon Tag", "cool and quiet", "calm", ww_tag(LAGOON)), o("jungle", "Jungle Green Tag", "reads as checked", "practical", ww_tag(JUNGLE))),
 ("Heading", Q(WW, "Subhead line", "which one line sits under the heading."),
  o("every", "Every Visit, Every Season", "about the schedule", "calm", ww_sub("Every visit, every season.")), o("cert", "Checked By Certified Techs", "about the people", "practical", ww_sub("Checked by certified techs."))),
 ("Add-On", Q(WW, "Lawn line with add-on tag", "where the one lawn add-on line sits."),
  o("grid", "Right After The Grid", "before the seasons", "practical", ww_lawn("grid")), o("strip", "After The Season Strip", "last in the section", "calm", ww_lawn("strip"))),
], reasked=["07"])
def form(label, acc, body): return site(label, acc, [("tx", "Sign Up", 13), ("steps", ["Plan", "Add-Ons", "You", "Pay"], TERRA, 3)], extra=body)
def fld(y, ph, val="", err=None, hint="stay"):
    s = rect(14, y, 212, 28, "#FFFFFF", (TERRA if err else LINE), 4, 1.4 if err else 1)
    if val and hint == "stay": s += t(20, y + 9, ph, 6, MUTE) + t(20, y + 22, val, 8.5, INK, "hind", 600)
    elif val: s += t(20, y + 18, val, 8.5, INK, "hind", 600)
    else: s += t(20, y + 18, ph, 8.5, "#A8A29A")
    return s
def su_hint(kind): return form("Hints In The Box", TERRA, fld(84, "Full name", "Jane Doe", hint=kind) + fld(118, "Email", "jane@example.com", hint=kind) + fld(152, "Street address"))
def su_err(kind):
    s = (rect(14, 80, 212, 22, TERRA + "14", "none", 4) + t(22, 95, "2 boxes need a look", 8, TERRA, "hind", 700)) if kind == "count" else t(120, 92, "jumps to the first red box", 7, MUTE, "hind", 400, "middle")
    s += t(20, 116, "Email: add an @ and a domain", 7, TERRA, "hind", 600) + fld(120, "Email", "jane@", True) + t(20, 160, "Phone: 10 digits", 7, TERRA, "hind", 600) + fld(164, "Phone", "313", True)
    return form("On Continue", TERRA, s)
def su_lab(kind):
    s = (ic("x", 18, 106, 9, TERRA, 2.2) if kind == "icon" else "") + t(30 if kind == "icon" else 20, 114, "Email: add an @ and a domain", 7.5, TERRA, "hind", 700) + fld(118, "Email", "jane@", True) + fld(152, "Phone", "(313) 555-0100")
    return form("Error By The Label", TERRA, s)
def su_scroll(kind):
    s = rect(14, 84, 212, 110, "#FFFFFF", LINE, 4) + "".join(rect(22, 94 + i * 12, 170 - (i % 3) * 24, 4, "#E5E0D8") for i in range(8))
    if kind == "bar": s += rect(214, 88, 4, 102, "#EEEAE4", "none", 2) + rect(214, 88, 4, 60, TERRA, "none", 2)
    else: s += t(218, 206, "60% read", 7.5, TERRA, "hind", 700, "end")
    return form("Agreement Box", TERRA, t(20, 80, "Member Agreement", 8.5, INK, "hind", 700) + s)
def su_link(kind):
    s = t(20, 96, "Cancel policy", 8.5, LAGOON, "hind", 600, extra='text-decoration="underline"')
    if kind == "place": s += rect(14, 104, 212, 60, SOFT, "none", 4) + "".join(t(22, 120 + i * 12, x, 7, INK) for i, x in enumerate(["Cancel any time from your profile.", "Paid visits stay booked.", "Unused months are refunded."]))
    else: s += rect(0, 150, 240, 150, "#0A0A0A33") + rect(0, 170, 240, 130, "#FFFFFF", "none", 14) + t(20, 196, "Cancel Policy", 11, INK, "khand", 700) + "".join(t(20, 212 + i * 12, x, 7, INK) for i, x in enumerate(["Cancel any time from your profile.", "Paid visits stay booked."]))
    return form("Cancel Policy Link", LAGOON, s)
def su_tag(c):
    s = t(20, 84, "Order Summary", 9, INK, "khand", 700) + "".join(t(20, 102 + i * 18, a, 8, INK) + (rect(118, 93 + i * 18, 46, 12, c + "26", "none", 6) + t(141, 102 + i * 18, "ONE-TIME", 6, c if c != "#8A8A8A" else MUTE, "hind", 700, "middle") if b else "") + t(220, 102 + i * 18, "$", 8, INK, "hind", 600, "end") for i, (a, b) in enumerate([("Plus Plan", False), ("Lawn cutting", False), ("Gutter clean-out", True), ("Smoke alarm swap", True)]))
    return form("One-Time Tag", SAFFRON, s)
def su_due(kind):
    a, b = (("Due today", "$ (example)"), ("Then monthly", "$ / mo")) if kind == "today" else (("Monthly", "$ / mo"), ("Due today", "$ (example)"))
    s = rect(14, 84, 104, 56, "#FFFFFF", INK, 6, 1.4) + t(22, 100, a[0], 7.5, MUTE) + t(22, 126, a[1], 13, INK, "khand", 700) + rect(122, 84, 104, 56, "#FFFFFF", LINE, 6) + t(130, 100, b[0], 7.5, MUTE) + t(130, 126, b[1], 13, INK, "khand", 700)
    return form("Due At Sign Up", INK, s)
def su_code(kind):
    s = t(20, 84, "Referral code", 7.5, MUTE) + fld(88, "Code", "NEIGHBOR")
    s += t(20, 132, "Code applied: $ off your first month" if kind == "amt" else "NEIGHBOR applied", 8, JUNGLE, "hind", 700)
    return form("Referral Code", JUNGLE, s)
def su_upsell(kind):
    if kind == "one": s = rect(14, 84, 212, 70, "#FFFFFF", LINE, 6) + t(22, 102, "Add window washing?", 9.5, INK, "khand", 700) + t(22, 116, "Twice a year, outside panes", 7.5, MUTE) + rect(22, 124, 80, 22, TERRA, "none", 11) + t(62, 139, "Add", 8, "#FFFFFF", "hind", 700, "middle") + t(150, 139, "Not now", 8, MUTE, "hind", 600, "middle")
    else: s = "".join(rect(14, 84 + i * 40, 212, 34, "#FFFFFF", LINE, 6) + t(22, 105 + i * 40, x, 8.5, INK, "hind", 600) + rect(182, 92 + i * 40, 36, 18, "#FFFFFF", TERRA, 9) + t(200, 104 + i * 40, "Add", 7, TERRA, "hind", 700, "middle") for i, x in enumerate(["Window washing", "Chimney sweep", "Radon test"]))
    return form("Add-On Offer", TERRA, s)
def su_tint(c):
    s = t(20, 84, "Sign here", 7.5, MUTE) + rect(14, 88, 212, 40, "#FFFFFF", LINE, 4) + f'<path d="M30 116 q20 -18 40 0 t40 0" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    s += rect(14, 136, 212, 40, c, "none", 4) + t(22, 152, "You may cancel within 3 business days", 7.5, INK, "hind", 600) + t(22, 166, "of signing for a full refund.", 7.5, INK, "hind", 600)
    return form("Cancel Notice", LAGOON, s)
SUF = D("sign-up-form-hints-errors-and-add-on-offer-deck", "Sign Up Form: Hints, Errors And Add-On Offer", "sign-up-form-next", "suf3_",
  "upkeep-sign-up-form-fields-errors-and-summary-deck", "Follow-on of Sign Up Form: Fields, Errors And Summary (10/10). Max asked whether the 3-day cancel notice is required; that question goes to Grok Bot for the report, not into a card.",
  "Hint words, error behavior and look, agreement scroll progress, cancel policy link, one-time tag, due-today boxes, referral line, add-on offer, notice tint.", [
 ("Order Form", Q(SU, "Hint words in the box", "what the grey hint does once the member types."),
  o("stay", "Shrinks To A Small Label", "you still see what the box is", "practical", su_hint("stay")), o("gone", "Disappears", "only the answer stays", "calm", su_hint("gone"))),
 ("Order Form", Q(SU, "Errors on continue", "what happens when Continue finds red boxes."),
  o("jump", "Jumps To The First One", "scrolls to the first red box", "practical", su_err("jump")), o("count", "A Count Banner On Top", "tells how many need a look", "calm", su_err("count"))),
 ("Order Form", Q(SU, "Error by the label", "how the error above the box is marked."),
  o("red", "Red Words", "just the message", "calm", su_lab("red")), o("icon", "Red Words With An Icon", "a small x first", "practical", su_lab("icon"))),
 ("Order Form", Q(SU, "Agreement scroll progress", "how the reading progress shows."),
  o("bar", "A Thin Bar On The Edge", "fills as you read", "calm", su_scroll("bar")), o("pct", "A Percent Read Line", "words under the box", "practical", su_scroll("pct"))),
 ("Trust", Q(SU, "Underlined cancel policy link", "what a tap on the link does."),
  o("place", "Opens In Place", "the text unfolds under it", "calm", su_link("place")), o("sheet", "Opens A Sheet", "slides up over the form", "practical", su_link("sheet"))),
 ("Order Form", Q(SU + " Summary", "One-time tag", "the color of the one-time tag in the summary."),
  o("saffron", "Saffron Tag", "stands out", "bold", su_tag(SAFFRON)), o("grey", "Grey Tag", "quiet", "calm", su_tag("#8A8A8A"))),
 ("Order Form", Q(SU + " Summary", "Two boxes for due and monthly", "which box comes first."),
  o("today", "Due Today First", "what you pay now", "practical", su_due("today")), o("month", "Monthly First", "the ongoing price", "calm", su_due("month"))),
 ("Order Form", Q(SU, "Code applied line", "what the green line under the code box says."),
  o("amt", "The Amount Off", "what the code saves", "practical", su_code("amt")), o("name", "The Code Name", "which code worked", "calm", su_code("name"))),
 ("Add-On Upsell", Q(SU + " Add-Ons", "Card in the page", "how many extras show at once."),
  o("one", "One At A Time", "a single offer card", "calm", su_upsell("one")), o("list", "A Short List", "three extras with Add buttons", "practical", su_upsell("list"))),
 ("Trust", Q(SU, "Cancel notice tinted box", "which tint the notice beside the signature uses."),
  o("cream", "Cream Tint", "warm and soft", "calm", su_tint("#F6EFE4")), o("lagoon", "Lagoon Tint", "cool and clear", "practical", su_tint(LAGOON + "1A"))),
])
def hero_badges(mode="drift", edges="fade", vis=3, spot="button", pills="outline", sep="gap", color="mixed", note=""):
    s = video(14, 36, 212, 110) + head(24, 90 if spot == "photo" else 112, ["Your Home,", "Taken Care Of."], 15, False, "#FFFFFF")
    y = 152
    if spot == "photo": by = 128
    s += rect(24, y, 120, 24, TERRA) + t(84, y + 16, "FREE QUOTE IN MINUTES", 7, "#FFFFFF", "hind", 700, "middle")
    by = y + 34 if spot == "button" else 126
    x = 14; items = BADGES[:5]
    if spot == "photo": s += rect(14, by - 4, 212, 24, "#0A0A0A44")
    for i, b in enumerate(items):
        cw = len(b) * (4.6 if vis == 2 else 3.9) + 12; c = TERRA if color == "terra" else ACC[i % 4]
        s += rect(x, by, cw, 16, (c + "1A") if pills == "tint" else "#FFFFFF", "none" if pills == "tint" else c, 8) + t(x + cw / 2, by + 11, b, 7.2 if vis == 2 else 6.6, c, "hind", 600, "middle")
        x += cw + (10 if sep == "dot" else 5)
        if sep == "dot": s += dot(x - 5, by + 8, 1.5, MUTE)
    if edges == "fade": s += f'<defs><linearGradient id="fe" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><rect x="176" y="{by - 2}" width="50" height="20" fill="url(#fe)"/><rect x="14" y="{by - 2}" width="20" height="20" fill="#fff" opacity=".6"/>'
    s += t(120, (194 if spot == "photo" else by + 32), note or ("drifts slowly in a loop" if mode == "drift" else "steps every few seconds, in a loop"), 7, MUTE, "hind", 400, "middle")
    return card("Trust Badges", TERRA, s)
TRT = D("trust-tags-looping-carousel-and-random-order-deck", "Trust Tags: Looping Carousel And Random Order", "trust-tags-carousel", "trt3_",
  "upkeep-trust-tags-order-and-placement-deck", "Follow-on of Trust Tags: Order And Placement (7/10): Max's notes say random order on a small carousel that loops by itself at the bottom of the section; this deck asks only how that carousel behaves and looks.",
  "Carousel motion, edges, how many show, spot at the bottom of the hero section, touch, pill look, separators, where else it runs, random rule, color.", [
 ("Motion", Q(HP, "Trust badge carousel", "how the looping carousel moves."),
  o("drift", "Slow Steady Drift", "always moving a little", "calm", hero_badges()), o("step", "Steps Every Few Seconds", "one badge at a time", "practical", hero_badges(mode="step"))),
 ("Style", Q(HP, "Carousel edges", "how the badges enter and leave the row."),
  o("fade", "Soft Fade At The Edges", "badges fade in and out", "calm", hero_badges()), o("hard", "Hard Edges", "badges slide past the edge", "practical", hero_badges(edges="hard"))),
 ("Count", Q(HP, "Badges in view", "about how many badges show at once."),
  o("three", "About Three", "smaller text", "practical", hero_badges()), o("two", "About Two", "bigger text", "bold", hero_badges(vis=2))),
 ("Placement", Q(HP, "Bottom of the section", "where the carousel sits at the bottom of the hero."),
  o("button", "Under The Quote Button", "the last row of the section", "practical", hero_badges()), o("photo", "On The Photo's Bottom Edge", "over the video, darker strip", "bold", hero_badges(spot="photo"))),
 ("Motion", Q(HP, "Touching the carousel", "what happens when a finger lands on it."),
  o("pause", "Pauses While Touched", "then keeps going", "practical", hero_badges(note="pauses while touched")), o("never", "Never Pauses", "nothing happens on tap", "calm", hero_badges(note="keeps moving, nothing on tap"))),
 ("Style", Q(HP, "Text-only pills", "how the text-only pills are drawn."),
  o("outline", "Outline Pills", "thin colored border", "calm", hero_badges()), o("tint", "Tinted Pills", "soft color fill", "playful", hero_badges(pills="tint"))),
 ("Style", Q(HP, "Between badges", "what separates the badges."),
  o("gap", "Just A Gap", "clean", "calm", hero_badges()), o("dot", "A Small Dot", "reads like a list", "practical", hero_badges(sep="dot"))),
 ("Placement", Q(MA + " Home", "Same carousel in the app", "whether the member app home runs the same badge carousel."),
  o("site", "Site Only", "the app stays calm", "calm", hero_badges(note="site home only")), o("both", "Site And Member App", "same badges in both", "practical", member("Member Home", TERRA, [("photo", 80, LAGOON, "house", "12 Elm St"), ("tags", BADGES[:3]), ("card", "Next Visit", "Oct 24", TERRA, "", "dot", 36, "left")]))),
 ("Mix", Q(HP, "Random order", "how random the order is."),
  o("new", "New Order Every Visit", "shuffled each page load", "playful", hero_badges(note="shuffled on every page load")), o("start", "Random Start, Fixed Loop", "same order, random first badge", "calm", hero_badges(note="random first badge, same loop"))),
 ("Style", Q(HP, "Pill color", "which colors the pills use."),
  o("mixed", "Brand Colors In Turn", "terracotta, lagoon, jungle, saffron", "playful", hero_badges()), o("terra", "All Terracotta", "one color", "calm", hero_badges(color="terra"))),
], reasked=["02", "03", "04"])
def band(pinned="pin", right="both", logoc="#FFFFFF", addr="shade", crop="front", tipic="star", c=LAGOON, scrolled=False):
    s = rect(14, 30, 212, 26 if not scrolled or pinned == "pin" else 18, TERRA) + mark(28, 43 if not scrolled or pinned == "pin" else 39, 6, TERRA, logoc) + t(38, 47 if not scrolled or pinned == "pin" else 43, "Smart Upkeep", 10, logoc, "khand", 700)
    if right in ("both", "init"): s += f'<circle cx="{198 if right == "both" else 212}" cy="43" r="8" fill="{c}"/>' + t(198 if right == "both" else 212, 46, "J", 8, "#FFFFFF", "hind", 700, "middle")
    if right == "both": s += shareic(208, 36)
    ph = 72; y = 60
    s += photo(14, y, 212, ph, LAGOON, "house", 0) + (rect(40, y + ph - 20, 160, 20, JUNGLE + "55") if crop == "wide" else "")
    if addr == "shade": s += f'<rect x="14" y="{y + ph - 24}" width="212" height="24" fill="#0A0A0A55"/>' + t(22, y + ph - 8, "12 Elm St", 11, "#FFFFFF", "khand", 700)
    else: s += rect(20, y + 6, 66, 16, "#FFFFFFEE", "none", 8) + t(53, y + 17, "12 Elm St", 8, INK, "hind", 700, "middle")
    s += "".join(rect(14, 140 + i * 30, 212, 26, "#FFFFFF", LINE, 5) + t(22, 157 + i * 30, x, 8.5, INK, "khand", 700) for i, x in enumerate(["Next Visit, Oct 24", "Open Items"]))
    s += rect(14, 202, 212, 34, "#FFFFFF", LINE, 6) + ic(tipic, 22, 210, 12, LAGOON, 2) + t(40, 219, "DID YOU KNOW?", 7, LAGOON, "hind", 700) + t(22, 231, "Clean dryer vents once a year.", 7, INK)
    if scrolled: s += t(120, 248, "after scrolling: band shrinks" if pinned == "shrink" else "after scrolling: band stays the same", 7, MUTE, "hind", 400, "middle")
    return card("Member Home", TERRA, s, True)
def clip(kind, cap="line"):
    s = rect(14, 40, 212, 150, "#0A0A0A") + photo(30, 50, 180, 110, LAGOON, "house", 4) + rect(70 if kind == "moist" else 130, 70, 60, 50, "none", "#FFFFFF", 4, 2)
    s += t(120, 176, ("Moisture: dry, all good" if kind == "moist" else "Gutters cleared, downspout reattached") if cap == "line" else "Marcus: 'Downspout was loose, fixed it.'", 8, "#FFFFFF", "hind", 600, "middle")
    s += t(120, 206, "zooms into one photo and one line", 7.5, MUTE, "hind", 400, "middle")
    return card("Report Clip", INK, s, True)
def endcard(bg):
    s = rect(14, 40, 212, 150, bg, LINE if bg == "#FFFFFF" else "none") + mark(120, 96, 14, bg, "#FFFFFF" if bg != "#FFFFFF" else TERRA) + t(120, 136, "smartupkeep", 18, "#FFFFFF" if bg != "#FFFFFF" else INK, "khand", 700, "middle") + t(120, 156, "Your Home, Taken Care Of.", 9, "#FFFFFFEE" if bg != "#FFFFFF" else MUTE, "hind", 600, "middle")
    return card("Video End Card", TERRA, s, False)
CPB = D("clear-picks-pinned-band-home-picture-and-clip-deck", "Clear Picks: Pinned Band, Home Picture And Report Clip", "clear-picks-pinned-band", "cpb3_",
  "upkeep-clear-picks-header-band-and-report-clip-deck", "Follow-on of Clear Picks: Header Band And Report Clip (9/10): Max asked 'I like pinned what do you think?'; my view is pinned and slim, so this deck asks how it stays pinned, plus the band, house photo and clip details.",
  "Pinned band (Max's question, my pick: pinned), right side, logo color, address on the photo, the third-height crop, report clip zoom and line, end card, tip icon, initial color.", [
 ("Header Band", Q(MA + " Home", "Pinned header band", "my view is pinned, so how it stays pinned as the member scrolls."),
  o("pin", "Pinned At Full Size", "the slim band never changes", "calm", band(scrolled=True)), o("shrink", "Pinned And Shrinks", "gets slimmer after a scroll", "practical", band(pinned="shrink", scrolled=True))),
 ("Header Band", Q(MA + " Home", "Band right side", "how the share button and the member's initial share the right side."),
  o("both", "Initial And Share Icon", "both in the band", "practical", band()), o("init", "Initial Only", "share moves to the menu", "calm", band(right="init"))),
 ("Header Band", Q(MA + " Home", "Logo on the terracotta band", "the color of the logo on the band."),
  o("white", "White Logo", "crisp", "bold", band()), o("cream", "Cream Logo", "softer", "calm", band(logoc=CREAM))),
 ("Member Home", Q(MA + " Home", "Address on the photo", "how the address sits on the house picture."),
  o("shade", "Bottom Left On A Shade", "white text, soft shade", "calm", band()), o("pill", "Top Left White Pill", "a small label", "practical", band(addr="pill"))),
 ("Member Home", Q(MA + " Home", "Third-height house picture", "what the shorter crop keeps in frame."),
  o("front", "Front Of The House", "close on the house", "calm", band()), o("wide", "House And Yard", "wider, more green", "playful", band(crop="wide"))),
 ("Video", Q("Smart Upkeep Video", "Report clip zoom", "which photo the clip zooms into."),
  o("moist", "The Moisture Scan Photo", "the all-good result", "calm", clip("moist")), o("gutter", "A Gutter Fix Photo", "a fix you can see", "practical", clip("gutter"))),
 ("Video", Q("Smart Upkeep Video", "Report clip line", "which line shows with the zoomed photo."),
  o("line", "One Report Line", "plain report wording", "calm", clip("gutter")), o("note", "The Tech's Own Note", "a short quote from the tech", "playful", clip("gutter", "note"))),
 ("Video", Q("Smart Upkeep Video", "End card background", "the color behind the logo and headline."),
  o("terra", "Terracotta", "brand color", "bold", endcard(TERRA)), o("white", "White", "clean", "calm", endcard("#FFFFFF"))),
 ("Member App Look", Q(MA + " Home", "Did You Know icon", "which small icon sits by the lagoon label."),
  o("star", "A Star", "a highlight", "playful", band()), o("home", "A House", "home care", "calm", band(tipic="home"))),
 ("Header Band", Q(MA + " Home", "Member initial circle", "the color of the initial circle on the band."),
  o("lagoon", "Lagoon Circle", "stands out on terracotta", "bold", band()), o("cream", "Cream Circle", "quiet", "calm", band(c="#E9DCC8"))),
], reasked=["05"])
CHECK = [MIX, CUS, INV, MPH, TTC, TWK, IPS, ATT, FCD, WWD, SUF, TRT, CPB]
PICKS = [MIX, CUS, INV]; UPKEEP_Q = [MPH, TTC, TWK, IPS, ATT, FCD, WWD, SUF, TRT, CPB]
DECKS = CHECK
