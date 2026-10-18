"""Follow-up decks Oct 18 2026 night (Branding): one fresh deck per finished deck, built on the picks and notes from
Tagline: Home Maintenance Membership (19:51 ICT), Investor Pitch: Wordmark Cover, Problem Photo And Plan Tabs (18:53),
Investor Pitch: Live Apps, Agent Chart And Use Of Funds (18:57) and Funnel: Price Lock Photos, Home Tiles And Contact (19:13).
Settled picks are not re-asked; skipped and Neither cards are re-asked in new words; notes become picks.
10 picks each, Notes on every card, light only, Khand + Hind, phone-first drawn MOCKUPS. Founder anonymous (no photo, no name).
Sample data and placeholders only; forecasts labelled."""
from md1018_kit import *
from uk5_art import mark
from fu1018 import top, phones, sheet, DROP
# ---------------- 1. Tagline follow-up ----------------
NAME, TL = "Smart Upkeep", "Home Maintenance Membership"
HERO = "Smart Upkeep Site Hero Mockup"; SOC = "Smart Upkeep Social Profile Mockup"; POST = "Smart Upkeep Social Post Mockup"
SIGN = "Smart Upkeep Yard Sign Mockup"; VAN = "Smart Upkeep Van Mockup"; POLO = "Smart Upkeep Crew Polo Mockup"
HANG = "Smart Upkeep Door Hanger Mockup"; MAIL = "Smart Upkeep Email Signature Mockup"; WMK = "Smart Upkeep Wordmark"
def wm(x, y, size, anchor="middle", c=INK): return t(x, y, NAME, size, c, "khand", anchor=anchor)
def tg(x, y, size, anchor="middle", c=MUTE, case="caps", w=400, ls="1"):
    s = {"caps": TL.upper(), "title": TL, "sentence": "Home maintenance membership", "lower": "home maintenance membership"}[case]
    return t(x, y, s, size, c, "hind", w, anchor, f'letter-spacing="{ls}"' if ls else "")
def hm(cx, cy, r, c=TERRA, fg="#FFFFFF"): return mark(cx, cy, r, fg, c)
def ot(k, label, desc, feel, loc, blocks, n1, n2="Mockup, sample wording"): return (k, label, desc, feel, S(loc, blocks, (n1, n2)))
STAGE = lambda inner, h=150: ("raw", rect(14, 0, 212, h, CREAM, "none", 10) + inner, h + 8)
def nav():
    return rect(0, 0, W, 34, "#FFFFFF") + ln(34, 0, W, LINE) + wm(14, 22, 14, "start") + "".join(rect(206, 11 + i * 5, 18, 2, INK, "none", 1) for i in range(3))
def btn(x, y, w, label, c=TERRA): return rect(x, y, w, 26, c, "none", 4) + t(x + w / 2, y + 17, label, 9, "#FFFFFF", "hind", 700, "middle")
def hero(support):
    return [("raw", nav(), 40), ("raw", photo(14, 0, 212, 76, LAGOON, "house", 8), 84),
            ("raw", tg(14, 8, 6.8, "start", TERRA, "caps", 700, "1.2") + t(14, 32, "Your home, taken care of", 18, INK, "khand") + t(14, 48, support, 8.2, MUTE) + btn(14, 58, 96, "See plans"), 92)]
def van(side, rear=False):
    if rear:
        s = rect(40, 10, 160, 130, "#FFFFFF", "#CFC8BC", 10, 1.4) + f'<line x1="120" y1="12" x2="120" y2="138" stroke="#CFC8BC"/>' + rect(52, 22, 56, 34, LAGOON + "33", "none", 4) + rect(132, 22, 56, 34, LAGOON + "33", "none", 4)
        return ("raw", s + side, 150)
    s = rect(10, 20, 170, 104, "#FFFFFF", "#CFC8BC", 10, 1.4) + f'<path d="M180 44 H206 Q214 44 220 56 L230 82 V124 H180 Z" fill="#FFFFFF" stroke="#CFC8BC" stroke-width="1.4"/>'
    s += f'<path d="M186 52 H204 Q209 52 212 58 L220 78 H186 Z" fill="{LAGOON}33"/>' + rect(10, 108, 220, 16, "#EEEAE4", "none", 0)
    for cx in (52, 196): s += f'<circle cx="{cx}" cy="126" r="15" fill="#2B2B2B"/><circle cx="{cx}" cy="126" r="6" fill="#BDB6AA"/>'
    return ("raw", s + side, 150)
STRIPE = lambda x, w, y=88: rect(x, y, w, 18, TERRA, "none", 0) + tg(x + w / 2, y + 12, 6.6, c="#FFFFFF", w=700)
def polo(x, c, inner):
    p = (f'<path d="M{x+22} 14 L{x} 34 L{x+9} 60 L{x+16} 56 V150 H{x+92} V56 L{x+99} 60 L{x+108} 34 L{x+86} 14 '
         f'Q{x+70} 8 {x+54} 22 Q{x+38} 8 {x+22} 14 Z" fill="{c}"/>' + f'<path d="M{x+40} 12 L{x+54} 24 L{x+46} 30 Z M{x+68} 12 L{x+54} 24 L{x+62} 30 Z" fill="#00000026"/>')
    return p + inner
FRONT = lambda: polo(8, TERRA, t(81, 49, "Smart Upkeep", 7, "#FFFFFF", "khand", anchor="end"))
LBL2 = t(62, 168, "Front", 8, MUTE, anchor="middle") + t(178, 168, "Back", 8, MUTE, anchor="middle")
def T_TAGLINE2():
    pairs, P = make("ts18_", "UpKeep")
    P("Supporting Line", HERO, "Supporting line wording", "with the lockup kept to wordmark and tagline only should the longer hero line say Seasonal care for every system or Small fixes before they become big bills?",
      ot("care", "Seasonal Care For Every System", "Under the headline: Seasonal care for every system, one plan.", "calm", HERO, hero("Seasonal care for every system, one plan"), "Says what members get"),
      ot("fix", "Small Fixes Before Big Bills", "Under the headline: Small fixes before they become big bills.", "focused", HERO, hero("Small fixes before they become big bills"), "Says why it matters"))
    P("Supporting Line", HERO, "Second supporting line idea", "should the supporting line list the parts of the plan or speak to the homeowner's peace of mind?",
      ot("list", "Visits, Photos, One Price", "Seasonal visits, photo reports, one monthly price.", "practical", HERO, hero("Seasonal visits, photo reports, one monthly price"), "Concrete"),
      ot("calm", "One Less Thing To Worry About", "Your home, looked after all year.", "warm", HERO, hero("Your home, looked after all year"), "Feels good"))
    P("Type", WMK, "Tagline case again", "since neither spaced caps nor title case felt right should the tagline try sentence case or all lowercase?",
      ot("sent", "Sentence Case", "Home maintenance membership, only the H capped.", "calm", WMK, [("gap", 46), STAGE(wm(120, 76, 38) + tg(120, 98, 10, c=MUTE, case="sentence", ls=None), 140)], "Reads like a plain line", "Small and light kept"),
      ot("low", "All Lowercase", "home maintenance membership, soft and modern.", "playful", WMK, [("gap", 46), STAGE(wm(120, 76, 38) + tg(120, 98, 10, c=MUTE, case="lower", ls=".4"), 140)], "Relaxed, modern", "Small and light kept"))
    P("In Context", POLO, "Polo back again", "since neither back print felt right should the polo back stay clean with the front mark only or carry the tagline alone across the shoulders?",
      ot("clean", "Clean Back, Front Mark Only", "Small wordmark on the chest, nothing on the back.", "calm", POLO, [("gap", 24), ("raw", FRONT() + polo(124, TERRA, "") + LBL2, 180)], "Simple, cheaper", "Mockup"),
      ot("shoulder", "Tagline Across The Shoulders", "Back: the tagline alone in small white caps up top.", "practical", POLO, [("gap", 24), ("raw", FRONT() + polo(124, TERRA, t(178, 42, "HOME MAINTENANCE", 5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".3"') + t(178, 50, "MEMBERSHIP", 5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".3"')) + LBL2, 180)], "Says what the crew does", "Mockup"))
    BIO = lambda inbio: [("raw", rect(0, 0, W, 70 if not inbio else 54, LAGOON + "22") + ("" if inbio else tg(120, 40, 7.4, c=INK, w=700, ls="1.2")), 74 if not inbio else 58),
                         ("raw", f'<circle cx="44" cy="0" r="24" fill="#FFFFFF" stroke="{LINE}"/>' + t(44, 4, "SU", 13, TERRA, "khand", anchor="middle") + t(78, 16, "Smart Upkeep", 13, INK, "khand") + (tg(78, 30, 6.4, "start", MUTE, "caps", 600, ".8") if inbio else t(78, 30, "Metro Detroit, sample", 7, MUTE)), 44),
                         ("raw", "".join(rect(14 + (i % 3) * 72, (i // 3) * 54, 68, 50, ACC[i % 4] + "22", "none", 4) for i in range(6)), 108)]
    P("Social", SOC, "Social profile tagline", "on a social profile should the tagline sit in the bio line under the name or across the cover banner?",
      ot("bio", "In The Bio Line", "Name, then the tagline in small caps.", "calm", SOC, BIO(True), "Reads with the name"),
      ot("cover", "Across The Cover Banner", "Tagline on the banner, bio stays short.", "focused", SOC, BIO(False), "Seen first"))
    PST = lambda band: [("raw", photo(14, 0, 212, 170, TERRA, "room", 6) + (rect(14, 150, 212, 20, "#FFFFFFEE") + wm(22, 164, 10, "start") + tg(218, 164, 5.2, "end", MUTE, "caps", 600, ".6") if band else rect(146, 150, 74, 16, "#FFFFFFEE", "none", 4) + wm(183, 162, 9)), 178), ("p", "Sample post: a fall gutter check", 46)]
    P("Social", POST, "Tagline on posts", "on social posts should every post carry a thin white band with wordmark and tagline or only a small wordmark tag?",
      ot("band", "Band On Every Post", "Wordmark left, tagline right, on a white strip.", "practical", POST, PST(True), "Brand on every share"),
      ot("tag", "Small Wordmark Tag Only", "Tagline saved for the bio and big posts.", "calm", POST, PST(False), "Photos stay clean"))
    SG = lambda extra: [("gap", 6), ("raw", rect(40, 0, 160, 120, "#FFFFFF", "#CFC8BC", 4, 1.4) + rect(40, 0, 160, 6, TERRA) + wm(120, 44, 22) + tg(120, 60, 5.6, c=MUTE, w=600) + extra + f'<line x1="70" y1="120" x2="70" y2="190" stroke="#8a8378" stroke-width="3"/><line x1="170" y1="120" x2="170" y2="190" stroke="#8a8378" stroke-width="3"/>', 196)]
    P("Signage", SIGN, "Yard sign content", "on a yard sign at a member's home should it show only the wordmark and tagline or add a short supporting line and a web address?",
      ot("min", "Wordmark And Tagline Only", "Big name, the tagline under it.", "calm", SIGN, SG(""), "Reads from the street"),
      ot("more", "Plus Line And Web Address", "Adds: Seasonal care, one plan, and a placeholder site.", "practical", SIGN, SG(t(120, 84, "Seasonal care, one plan", 8, INK, "hind", 600, "middle") + t(120, 104, "yoursite.example", 7.4, TERRA, "hind", 700, "middle")), "Tells them where to look", "Placeholder address"))
    P("Signage", VAN, "Van rear doors", "with the tagline on a terracotta stripe along the van side should the stripe and tagline carry on across the rear doors or should the rear show the wordmark only?",
      ot("stripe", "Stripe Carries On", "Rear doors: wordmark plus the same tagline stripe.", "playful", VAN, [("gap", 30), van(wm(120, 82, 18) + STRIPE(40, 160, 100), rear=True)], "Matches the side"),
      ot("word", "Wordmark Only On The Rear", "Rear doors: a big wordmark, no stripe.", "calm", VAN, [("gap", 30), van(wm(120, 92, 22), rear=True)], "Clean in traffic"))
    HG = lambda top_: [("raw", rect(70, 0, 100, 220, "#FFFFFF", "#CFC8BC", 6, 1.4) + f'<circle cx="120" cy="22" r="11" fill="{CREAM}" stroke="#CFC8BC"/>' + wm(120, 56, 14) + (tg(120, 68, 4.6, c=MUTE, w=600, ls=".3") if top_ else "") + t(120, 100, "We stopped by", 10, INK, "khand", anchor="middle") + t(120, 114, "Your fall visit is done", 6.8, MUTE, anchor="middle") + rect(82, 126, 76, 50, CREAM, "none", 4) + t(120, 154, "Photo report in the app", 6, MUTE, anchor="middle") + (rect(70, 192, 100, 28, TERRA, "none", 0) + t(120, 204, "HOME MAINTENANCE", 5.4, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".3"') + t(120, 213, "MEMBERSHIP", 5.4, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".3"') if not top_ else ""), 228)]
    P("Signage", HANG, "Door hanger tagline", "on a door hanger left after a visit should the tagline sit under the wordmark at the top or on a terracotta band at the bottom?",
      ot("top", "Under The Wordmark At Top", "Wordmark, tagline, then the visit note.", "calm", HANG, HG(True), "Same as the lockup"),
      ot("band", "Terracotta Band At Bottom", "Echoes the van stripe.", "playful", HANG, HG(False), "Ties to the van"))
    ML = lambda inline: [("raw", t(14, 14, "Thanks, talk soon.", 9, INK) + ln(26, 14, 140, "#D6D0C6") + t(14, 46, "Name Here", 11, INK, "khand") + t(14, 58, "Field Tech, Smart Upkeep", 7.4, MUTE) + (tg(14, 72, 5.8, "start", TERRA, "caps", 700, ".9") if inline else "") + t(14, 88 if inline else 74, "(000) 000-0000", 7.4, INK) + ("" if inline else rect(0, 96, W, 20, TERRA) + tg(120, 109, 6, c="#FFFFFF", w=700)), 122)]
    P("Everyday", MAIL, "Email signature", "in the crew's email signature should the tagline sit as a small terracotta line under the title or as a full-width terracotta strip at the bottom?",
      ot("line", "Small Line Under The Title", "Name, title, tagline, phone.", "calm", MAIL, ML(True), "Tidy", "Mockup, placeholder details"),
      ot("strip", "Strip At The Bottom", "A thin terracotta strip with the tagline.", "playful", MAIL, ML(False), "Matches the van stripe", "Mockup, placeholder details"))
    return pairs
# ---------------- 2. Wordmark cover / problem / plans follow-up (pitch) ----------------
PA = "UpKeep Investor Pitch App Mockup"
def op(k, label, desc, feel, blocks, n1, n2="Mockup, founder unnamed"): return (k, label, desc, feel, S(PA, blocks, (n1, n2)))
def frame3(sel=None, h=118, names=("Sign up", "We visit", "Report")):
    s = ""
    for i in range(3):
        x = 18 + i * 72; s += rect(x, 0, 60, h, "#FFFFFF", INK if i != sel else TERRA, 10, 2) + rect(x + 20, 4, 20, 4, INK, "none", 2) + rect(x + 6, 14, 48, 14, ACC[i] + "33", "none", 3) + "".join(rect(x + 6, 34 + j * 14, 48, 8, "#EEEAE4", "none", 2) for j in range(5))
        s += t(x + 30, h + 14, names[i], 8, INK, "khand", anchor="middle")
    return ("raw", s, h + 22)
def big_phone(extra="", h=200, x=50, w=140):
    s = rect(x, 0, w, h, "#FFFFFF", INK, 14, 2.4) + rect(x + w / 2 - 15, 5, 30, 5, INK, "none", 3) + rect(x + 10, 18, w - 20, 22, TERRA + "22", "none", 4) + "".join(rect(x + 10, 48 + j * 18, w - 20, 11, "#EEEAE4", "none", 3) for j in range(int((h - 60) / 18)))
    return s + extra
CAREER = [("Construction company", "Founded, construction management"), ("Project manager", "Self-employed, construction projects"), ("High-end homes", "Builds multi-million-dollar homes"), ("Smart Upkeep", "Built the platform, trained the first tech")]
CAREER_Y = [("2012", "Founded a construction management company"), ("Since then", "Self-employed construction PM"), ("Today", "Builds multi-million-dollar homes"), ("Now", "Built the platform, trained the first tech")]
def T_PITCH_SCROLL():
    pairs, P = make("sp18_", "UpKeep")
    P("Problem", PA, "Problem caption our pick", "you left the problem caption to us so we lean to a bold headline under the photo, keep that or put the caption on a white band over the photo?",
      op("under", "Headline Under Photo", "Our lean: photo, then a bold headline.", "focused", [top(2, "Problem"), ("photo", 130, TERRA, "room"), ("h", "A small leak, left alone", 16)], "Easier to read on a phone", "Mockup"),
      op("band", "White Band Over Photo", "The caption sits on the photo.", "warm", [top(2, "Problem"), ("photo", 170, TERRA, "room", "A small leak, left alone")], "Photo stays big", "Mockup"))
    P("App Preview", PA, "Tap a snapshot", "following your note that tapping an app snapshot should zoom into a real scrollable view should it open full screen with a Close button or grow in place inside the slide?",
      op("full", "Opens Full Screen", "The app view fills the phone, Close on top.", "focused", [("raw", rect(0, 0, W, 24, CREAM) + t(14, 16, "Member app, preview", 8.5, INK, "hind", 600) + t(226, 16, "Close", 8.5, TERRA, "hind", 700, "end"), 30), ("raw", big_phone(h=180, x=30, w=180), 186)], "Room to look around", "Mockup, sample data"),
      op("grow", "Grows In Place", "The phone frame enlarges inside the slide.", "playful", [top(3, "How it works"), ("raw", big_phone(h=172) + t(120, 186, "Tap outside to shrink", 7.5, MUTE, anchor="middle"), 194)], "Never leaves the pitch", "Mockup, sample data"))
    P("App Preview", PA, "Scroll hint", "inside the zoomed app view should a small Scroll to explore pill show or should the view gently scroll a little on open to show it moves?",
      op("pill", "Scroll To Explore Pill", "A small pill near the bottom, fades once used.", "practical", [("raw", big_phone(rect(84, 168, 72, 18, INK, "none", 9) + t(120, 180, "Scroll to explore", 7, "#FFFFFF", "hind", 600, "middle"), h=200), 208)], "Plainly told", "Mockup, sample data"),
      op("peek", "Gentle Scroll On Open", "The view slides up a little, then back.", "calm", [("raw", big_phone(f'<path d="M200 60 v60 M194 112 l6 8 6 -8" fill="none" stroke="{LAGOON}" stroke-width="1.6"/>', h=176), 184), ("p", "Moves once on open, no words", 46)], "Shows, not tells", "Mockup, sample data"))
    P("App Preview", PA, "View only label", "since the zoomed view is a real look at the app with no access should it carry a small View only tag or no label at all?",
      op("tag", "Small View Only Tag", "A grey View only chip in the corner.", "practical", [("raw", big_phone(chip(146, 22, "View only", MUTE, True)[0], h=200), 208)], "No confusion", "Mockup, sample data"),
      op("none", "No Label", "It just looks like the app.", "calm", [("raw", big_phone(h=200), 208)], "Feels real", "Mockup, sample data"))
    P("App Preview", PA, "Closing the preview", "to leave the zoomed app view should investors tap a Close button at the top or swipe down to close?",
      op("btn", "Close Button At Top", "A clear Close in the top corner.", "practical", [("raw", rect(0, 0, W, 24, CREAM) + t(226, 16, "Close", 8.5, TERRA, "hind", 700, "end"), 30), ("raw", big_phone(h=180, x=30, w=180), 186)], "Obvious", "Mockup, sample data"),
      op("swipe", "Swipe Down To Close", "A grab bar on top, swipe it away.", "playful", [("raw", rect(104, 0, 32, 4, "#D6D0C6", "none", 2), 10), ("raw", big_phone(h=176, x=30, w=180), 182), ("p", "Swipe down to close", 46)], "Phone-native", "Mockup, sample data"))
    P("How It Works", PA, "Step names", "under the three phone-outline snapshots should the step names be plain words or numbered steps?",
      op("plain", "Plain Words", "Sign up, We visit, Report.", "calm", [top(3, "How it works"), frame3()], "Clean", "Mockup"),
      op("num", "Numbered Steps", "1 Sign up, 2 We visit, 3 Report.", "practical", [top(3, "How it works"), frame3(names=("1  Sign up", "2  We visit", "3  Report"))], "Clear order", "Mockup"))
    P("Founder", PA, "Founder heading again", "since you want to stay anonymous with your background known should the founder screen heading be The Background or Who's Behind It?",
      op("bg", "The Background", "Heading points to the track record.", "calm", [top(5, "The background"), ("timeline", CAREER)], "Facts first"),
      op("who", "Who's Behind It", "Heading plain and friendly, still no name.", "warm", [top(5, "Who's behind it"), ("timeline", CAREER)], "Human, still unnamed"))
    P("Founder", PA, "How the founder is named", "with no name or photo should the screen call him The founder or Founder and operator?",
      op("f", "The Founder", "Plain role, nothing more.", "calm", [top(5, "The background"), ("h", "The founder", 15), ("timeline", CAREER)], "Simple"),
      op("fo", "Founder And Operator", "Says he runs the field side too.", "focused", [top(5, "The background"), ("h", "Founder and operator", 15), ("timeline", CAREER)], "Hands-on message"))
    P("Founder", PA, "Years on the career line", "for staying anonymous should the career dots show years like 2012 or stage words only?",
      op("yrs", "Show Years", "2012, Since then, Today, Now.", "practical", [top(5, "The background"), ("timeline", CAREER_Y)], "Anchored in time"),
      op("stage", "Stage Words Only", "No years, harder to trace.", "calm", [top(5, "The background"), ("timeline", CAREER)], "More private"))
    P("Plans", PA, "Plan tab content", "under the underline plan tabs should each tab show the price with three included items or the price with one short sentence?",
      op("three", "Price Plus Three Items", "From $99/mo, then three ticks.", "practical", [top(4, "Plans"), ("tabs", ["Starter", "Plus", "Whole"], "line"), ("word", "$99/mo", 28, JUNGLE, "FROM"), ("checks", ["Seasonal visits", "Photo report", "Filter changes"], JUNGLE, 3)], "Shows the value", "Mockup, sample plan"),
      op("one", "Price Plus One Line", "From $99/mo and one plain sentence.", "calm", [top(4, "Plans"), ("tabs", ["Starter", "Plus", "Whole"], "line"), ("word", "$99/mo", 28, JUNGLE, "FROM"), ("p", "Seasonal visits and a photo report", 46, MUTE, True)], "Short and clean", "Mockup, sample plan"))
    return pairs
# ---------------- 3. Live apps / agent chart / use of funds follow-up (pitch) ----------------
AGENTS = [("Sales", LAGOON), ("Brand", JUNGLE), ("Ops", SAFFRON), ("Finance", LAGOON), ("Research", JUNGLE)]
def chart_top(hire=None):
    s = rect(80, 0, 80, 26, TERRA + "1A", TERRA, 6) + t(120, 17, "Founder", 9, INK, "khand", anchor="middle") + f'<line x1="120" y1="26" x2="120" y2="38" stroke="#D6D0C6"/><line x1="30" y1="38" x2="210" y2="38" stroke="#D6D0C6"/>'
    for i, (n, c) in enumerate(AGENTS):
        x = 30 + i * 45; s += f'<line x1="{x}" y1="38" x2="{x}" y2="46" stroke="#D6D0C6"/>' + rect(x - 21, 46, 42, 22, "#FFFFFF", c, 5) + t(x, 60, n, 6.8, INK, "hind", 600, "middle")
    s += f'<line x1="120" y1="68" x2="120" y2="84" stroke="#D6D0C6"/>' + rect(60, 84, 120, 24, JUNGLE + "14", JUNGLE, 5) + t(120, 99, "Field tech", 8.4, INK, "khand", anchor="middle")
    h = 112
    if hire == "box": s += rect(60, 116, 120, 26, "#FFFFFF", "#BDB6AA", 5, 1, 'stroke-dasharray="4 3"') + t(120, 133, "Tech #2: hire at 75 homes", 7.6, MUTE, "hind", 600, "middle") + f'<line x1="120" y1="108" x2="120" y2="116" stroke="#D6D0C6" stroke-dasharray="3 2"/>'; h = 146
    if hire == "flag": s += rect(164, 78, 66, 14, TERRA, "none", 3) + t(197, 88, "+1 at 75 homes", 6.2, "#FFFFFF", "hind", 700, "middle"); h = 112
    return ("raw", s, h)
def chart_hub():
    pts = list(zip(((50, 28), (190, 28), (36, 104), (204, 104), (120, 146)), AGENTS))
    s = "".join(f'<line x1="120" y1="72" x2="{x}" y2="{y}" stroke="#D6D0C6"/>' for (x, y), _ in pts)
    s += f'<circle cx="120" cy="72" r="24" fill="#FBEDE8" stroke="{TERRA}"/>' + t(120, 76, "Founder", 8.5, INK, "khand", anchor="middle")
    for (x, y), (n, c) in pts:
        s += f'<circle cx="{x}" cy="{y}" r="18" fill="#FFFFFF" stroke="{c}"/>' + t(x, y + 3, n, 6.8, INK, "hind", 600, "middle")
    return ("raw", s, 170)
ASK = lambda extra="", h=110: ("raw", rect(14, 0, 212, h, "#FFFFFF", LINE, 8) + t(24, 26, "$200K for 10%", 15, INK, "khand") + t(24, 40, "at a $2M valuation", 8, MUTE) + ln(50, 24, 216) + t(24, 70, "$100K line of credit", 12, INK, "khand") + t(24, 82, "separate, at 10%", 8, MUTE) + extra, h + 8)
SPLIT = lambda y, lab=None: "".join(rect(24 + sum((48, 52, 40, 52)[:i]), y, w, 10, c, "none", 0) for i, (w, c) in enumerate(zip((48, 52, 40, 52), (TERRA, LAGOON, JUNGLE, SAFFRON)))) + (lab or "")
def T_PITCH_AGENTS():
    pairs, P = make("ac18_", "UpKeep")
    P("Org Chart", PA, "Founder at top or centre", "following your question founder at centre or top should the agent chart put the founder on top with agents in a row below or in the middle with agents around?",
      op("top", "Founder On Top", "Founder, a row of agents, then the field tech.", "practical", [top(6, "How we run it"), chart_top()], "Reads top down like a team"),
      op("hub", "Founder In The Centre", "Founder in the middle, agents in a ring.", "playful", [top(6, "How we run it"), chart_hub()], "A hub of help"))
    P("Org Chart", PA, "Agent box wording", "on the agent chart should each box say only the role or the role plus a few words on its job?",
      op("role", "Role Only", "Sales, Brand, Ops, Finance, Research.", "calm", [top(6, "How we run it"), ("pills", ["Sales", "Brand", "Ops", "Finance", "Research"], [LAGOON, JUNGLE, SAFFRON, LAGOON, JUNGLE])], "Tidy"),
      op("job", "Role Plus Its Job", "Ops: books visits and routes.", "practical", [top(6, "How we run it"), ("kv", [("Sales", "Answers new sign-ups"), ("Brand", "Designs every screen"), ("Ops", "Books visits and routes"), ("Finance", "Tracks costs and cash"), ("Research", "Checks the market")])], "Investors see the work"))
    P("Hiring", PA, "Tech hire on the chart", "following your note to show hiring another technician at 75 homes should the chart add a dashed box under the field tech or a small +1 at 75 homes flag beside it?",
      op("box", "Dashed Box Under The Tech", "Tech #2: hire at 75 homes, dashed.", "practical", [top(6, "How we run it"), chart_top("box")], "Plain to see", "Mockup; hire timing is a plan"),
      op("flag", "Small Flag Beside The Tech", "A terracotta +1 at 75 homes tag.", "calm", [top(6, "How we run it"), chart_top("flag")], "Chart stays compact", "Mockup; hire timing is a plan"))
    P("Hiring", PA, "Why hire at 75 homes", "should the hiring note also say why, to train before 100 homes, or only give the 75-home trigger?",
      op("why", "Say Why", "Hire at 75 homes to train before 100.", "practical", [top(6, "How we run it"), chart_top("box"), ("note", "Hire at 75 homes to train", "Ready for routes at 100 to 125 homes (Forecast)", LAGOON)], "Shows planning ahead", "Mockup; Forecast labelled"),
      op("trig", "Trigger Only", "Tech #2 at 75 homes, nothing more.", "calm", [top(6, "How we run it"), chart_top("box")], "Short", "Mockup; hire timing is a plan"))
    P("Demo Label", PA, "Sample data label again", "inside the app previews should a thin Sample data strip run across the top or a small Sample tag sit in one corner?",
      op("strip", "Thin Strip Across The Top", "Sample data, not real members.", "practical", [("raw", rect(0, 0, W, 16, SAFFRON + "33") + t(120, 11, "Sample data, not real members", 7, "#8a6510", "hind", 700, "middle"), 20), ("raw", big_phone(h=184), 190)], "Impossible to miss", "Mockup, sample data"),
      op("corner", "Small Corner Tag", "A tiny Sample tag, app looks real.", "calm", [("raw", big_phone(chip(150, 22, "Sample", SAFFRON, True)[0], h=200), 206)], "Clean preview", "Mockup, sample data"))
    P("App Preview", PA, "What Open shows", "under each snapshot should Open show a scrollable view-only look at the app or the full demo app filled with sample data?",
      op("view", "Scrollable View Only", "A real look you can scroll, no taps inside.", "calm", [top(6, "How we run it"), phones(["Member", "Tech", "Command"], 0), ("p", "Open: scroll a real view, view only", 46)], "Safe, matches your note", "Mockup"),
      op("demo", "Full Demo App", "Tap around a demo filled with sample data.", "playful", [top(6, "How we run it"), phones(["Member", "Tech", "Command"], 0), ("p", "Open: try the demo, sample data", 46)], "Hands-on", "Mockup"))
    P("App Preview", PA, "Back to pitch control", "with apps opening inside the pitch should the way back be a slim cream Back to pitch bar or a small round back button floating on the app?",
      op("bar", "Slim Back To Pitch Bar", "A cream bar across the top.", "practical", [("raw", rect(0, 0, W, 24, CREAM) + t(14, 16, "\u2039 Back to pitch", 8.5, TERRA, "hind", 700), 30), ("raw", big_phone(h=180, x=30, w=180), 186)], "Never lost", "Mockup"),
      op("float", "Floating Round Button", "A round back arrow over the app.", "calm", [("raw", big_phone(f'<circle cx="48" cy="170" r="14" fill="{TERRA}"/>' + t(48, 175, "\u2039", 14, "#FFFFFF", "hind", 700, "middle"), h=196, x=30, w=180), 202)], "More room for the app", "Mockup"))
    P("The Ask", PA, "Techs slice label", "in the split bar inside the Ask card should the Techs slice note the tech #2 hire at 75 homes or stay a plain Techs label?",
      op("note", "Techs Incl. Tech #2 At 75", "Techs slice: includes tech #2 at 75 homes.", "practical", [top(8, "The Ask"), ASK(SPLIT(92) + t(24, 116, "Techs, incl. tech #2 at 75 homes", 6.8, TERRA, "hind", 600), 124), ("sample", "SAMPLE SPLIT")], "Links money to growth", "Mockup, sample split"),
      op("plain", "Plain Techs Label", "Techs, Vans, Marketing, Runway.", "calm", [top(8, "The Ask"), ASK(SPLIT(92) + t(24, 116, "Techs   Vans   Marketing   Runway", 6.8, MUTE, "hind", 600), 124), ("sample", "SAMPLE SPLIT")], "Simple", "Mockup, sample split"))
    TLB = lambda lab: ("raw", rect(14, 30, 212, 8, "#EEEAE4", "none", 4) + rect(110, 30, 90, 8, LAGOON + "66", "none", 0) + f'<path d="M110 22 v-6 h90 v6" fill="none" stroke="{LAGOON}" stroke-dasharray="3 2"/>' + t(155, 12, lab, 7, LAGOON, "hind", 600, "middle") + t(14, 54, "Dec 1", 7.5, INK) + t(226, 54, "Apr 1", 7.5, INK, anchor="end"), 64)
    P("Timeline", PA, "Beta label wording", "with both the lagoon shading and the dashed bracket on the Beta stretch should the label read Beta, about 50 homes (Expected) or just Beta, Jan to Mar?",
      op("n", "Beta, About 50 Homes Expected", "Beta, about 50 homes (Expected).", "practical", [top(7, "Timeline"), TLB("Beta, about 50 homes (Expected)")], "Shows the target", "Mockup; Expected labelled"),
      op("d", "Beta, Jan To Mar", "Dates only, numbers stay elsewhere.", "calm", [top(7, "Timeline"), TLB("Beta, Jan to Mar")], "Less to read", "Mockup"))
    P("Pitch App", PA, "First screen swipe hint", "for the swipe hint on the first screen only should it be an arrow with the word Swipe or a one-time nudge where the screen slides a little?",
      op("arrow", "Arrow Plus Swipe", "A terracotta arrow and the word Swipe.", "practical", [top(1, "Smart Upkeep"), ("gap", 40), ("word", "Smart Upkeep", 26), ("raw", ic("chev", 200, 0, 18, TERRA, 2) + t(194, 13, "Swipe", 7.5, TERRA, "hind", 600, "end"), 22)], "Plainly told", "Mockup"),
      op("nudge", "One-Time Nudge", "The cover slides left a little, then back.", "calm", [top(1, "Smart Upkeep"), ("gap", 40), ("word", "Smart Upkeep", 26), ("raw", f'<path d="M150 8 h50 M192 2 l8 6 -8 6" fill="none" stroke="{LAGOON}" stroke-width="1.4" stroke-dasharray="3 2"/>', 22), ("p", "Moves once, no words", 46, MUTE, True)], "Cover stays clean", "Mockup"))
    return pairs
# ---------------- 4. Funnel price lock follow-up ----------------
FI = "Smart Upkeep Sign Up · Your Home"
def of(k, label, desc, feel, blocks, n1, n2="Mockup, sample data"): return (k, label, desc, feel, S(FI, blocks, (n1, n2)))
THUMBS = lambda xs=False: ("raw", "".join(photo(14 + i * 72, 0, 64, 52, ACC[i], ["room", "house", "sun"][i], 6) + (f'<circle cx="{72+i*72}" cy="6" r="7" fill="{INK}"/>' + t(72 + i * 72, 9, "\u00D7", 9, "#FFFFFF", "hind", 700, "middle") if xs else "") for i in range(3)), 60)
def T_FUNNEL2():
    pairs, P = make("fp18_", "UpKeep")
    P("Home Photos", FI, "Photo price headline", "following your note on how to explain that skipping photos can change the price after visit one should the photo step lead with Lock today's price or Photos help us price it right?",
      of("lock", "Lock Today's Price", "Add photos and your price is locked.", "focused", [("banner", "Add photos to lock today's price", JUNGLE, "check"), DROP, ("note", "No photos? Your tech confirms the price", "at the first visit", LAGOON)], "Clear reward"),
      of("right", "Photos Help Us Price It Right", "A softer reason, same note below.", "calm", [("h", "Photos help us price it right", 14), DROP, ("note", "No photos? Your tech confirms the price", "at the first visit", LAGOON)], "Low pressure"))
    P("Home Photos", FI, "Price note wording", "for the on-screen note you picked should it say the price may adjust if what we find does not match or say your tech confirms the price at the first visit?",
      of("adj", "May Adjust If It Doesn't Match", "If your home differs from your answers, price may adjust.", "practical", [("h", "Add photos (optional)", 14), DROP, ("note", "If what we find doesn't match your answers,", "your price may adjust after visit one", LAGOON)], "Spells it out"),
      of("conf", "Tech Confirms At Visit One", "Your tech confirms the price at the first visit.", "calm", [("h", "Add photos (optional)", 14), DROP, ("note", "No photos? No problem.", "Your tech confirms the price at visit one", LAGOON)], "Friendly"))
    P("Home Photos", FI, "Terms link", "under the price note should there be a small See terms link to the contract wording or no link?",
      of("link", "Small See Terms Link", "Opens the price wording in the terms.", "practical", [("h", "Add photos (optional)", 14), DROP, ("note", "No photos? Your tech confirms the price", "at the first visit", LAGOON), ("btn", "See terms", "link", LAGOON)], "Backed by the contract"),
      of("none", "No Link", "The note is enough on this screen.", "calm", [("h", "Add photos (optional)", 14), DROP, ("note", "No photos? Your tech confirms the price", "at the first visit", LAGOON)], "Shorter screen"))
    P("Home Photos", FI, "Drop area and camera together", "with both the dashed drop area and the camera button kept should the camera button sit inside the drop area or under it?",
      of("in", "Camera Button Inside", "Take a photo sits in the dashed box.", "calm", [("h", "Add photos", 14), ("raw", DROP[1].replace("Tap to add photos", "Drop photos here") + rect(70, 58, 100, 22, TERRA, "none", 11) + t(120, 72, "Take a photo", 8, "#FFFFFF", "hind", 700, "middle"), 98), THUMBS()], "One box"),
      of("under", "Camera Button Under", "Drop area, then a full-width button.", "practical", [("h", "Add photos", 14), DROP, ("btn", "Take a photo", "fill", TERRA), THUMBS()], "Easy to tap"))
    P("Home Photos", FI, "Thumbnail remove", "for the photo thumbnails should each one carry a small remove X or open an Edit sheet when tapped?",
      of("x", "Small Remove X", "An X on the corner of each photo.", "practical", [("h", "Add photos", 14), DROP, THUMBS(True)], "Quick to fix"),
      of("sheet", "Tap Opens Edit Sheet", "Replace or remove from a sheet.", "calm", [("h", "Add photos", 14), THUMBS(), ("raw", rect(0, 0, W, 120, "#0A0A0A14") + rect(0, 10, W, 110, "#FFFFFF", LINE, 14) + rect(104, 16, 32, 4, "#D6D0C6", "none", 2) + t(14, 40, "Photo", 13, INK, "khand") + t(14, 64, "Replace photo", 9, INK) + ln(72, 14, 226) + t(14, 90, "Remove photo", 9, TERRA), 124)], "Tidy thumbnails"))
    P("Your Home", FI, "Home type tiles our pick", "you left the home type tiles to us so we lean to clean line drawings, keep that or switch to soft photos?",
      of("line", "Line Drawings", "Our lean: a clean house outline per type.", "calm", [("h", "What kind of home?", 14), ("tiles", [("House", "home"), ("Condo", "home"), ("Townhome", "home"), ("Other", "tag")], 2, 60)], "Crisp and quick"),
      of("photo", "Soft Photos", "A small photo of each home type.", "warm", [("h", "What kind of home?", 14), ("raw", "".join(photo(14 + (i % 2) * 110, (i // 2) * 76, 102, 50, ACC[i], "house") + t(18 + (i % 2) * 110, (i // 2) * 76 + 64, n, 9, INK, "khand") for i, n in enumerate(("House", "Condo", "Townhome", "Other"))), 150)], "Warmer"))
    P("Contact", FI, "Contact chips our pick", "you left the contact chips to us so we lean to letting people tick any of Text, Call and Email, keep that or one main way only?",
      of("multi", "Tick Any", "Our lean: tick as many as you like.", "practical", [("h", "How should we reach you?", 14), ("checks", ["Text", "Call", "Email"], JUNGLE, 2)], "Flexible"),
      of("one", "One Main Way", "Pick the one you prefer.", "calm", [("h", "How should we reach you?", 14), ("tabs", ["Text", "Call", "Email"])], "Simple"))
    P("Your Home", FI, "Size ranges", "for the solid terracotta size chips should there be three ranges or four ranges plus Not sure?",
      of("three", "Three Ranges", "Under 1,500, 1,500 to 2,500, 2,500+.", "calm", [("h", "About how big?", 14), ("raw", chip(14, 0, "Under 1,500", TERRA)[0] + chip(86, 0, "1,500 to 2,500", TERRA, True)[0] + chip(172, 0, "2,500+", TERRA)[0], 24)], "Fast"),
      of("four", "Four Ranges Plus Not Sure", "Adds 3,500+ and Not sure.", "practical", [("h", "About how big?", 14), ("raw", chip(14, 0, "Under 1,500", TERRA)[0] + chip(86, 0, "1,500 to 2,500", TERRA, True)[0] + chip(172, 0, "2,500+", TERRA)[0] + chip(14, 22, "3,500+", TERRA)[0] + chip(62, 22, "Not sure", MUTE)[0], 46)], "Fits every home"))
    P("Your Home", FI, "Not sure system tile", "with white system tiles and a green check should the grid add a Not sure tile for people who don't know what they have?",
      of("add", "Add A Not Sure Tile", "Not sure: your tech checks at visit one.", "practical", [("h", "What's in the home?", 14), ("tiles", [("Furnace", "home"), ("Central air", "star"), ("Water heater", "clock"), ("Not sure", "tag")], 2, 56)], "Nobody gets stuck"),
      of("no", "No Not Sure Tile", "Only the systems, skip if unsure.", "calm", [("h", "What's in the home?", 14), ("tiles", [("Furnace", "home"), ("Central air", "star"), ("Water heater", "clock"), ("Sump pump", "check")], 2, 56)], "Shorter list"))
    P("Your Home", FI, "Edit beside each line style", "on the recap card with Edit beside each line should Edit be the word Edit or a small pencil icon?",
      of("word", "The Word Edit", "Terracotta Edit at the end of each line.", "practical", [("h", "Your home", 14), ("raw", "".join(t(14, 14 + i * 20, k, 8.5, INK, "hind", 500) + t(170, 14 + i * 20, v, 8.5, INK, "hind", 700, "end") + t(226, 14 + i * 20, "Edit", 7.5, TERRA, "hind", 600, "end") for i, (k, v) in enumerate((("Type", "House"), ("Size", "1,500-2,500"), ("Systems", "4"), ("Photos", "3")))), 86)], "Clear", "Sample answers"),
      of("pen", "Small Pencil Icon", "A pencil at the end of each line.", "calm", [("h", "Your home", 14), ("raw", "".join(t(14, 14 + i * 20, k, 8.5, INK, "hind", 500) + t(190, 14 + i * 20, v, 8.5, INK, "hind", 700, "end") + f'<path d="M212 {16+i*20} l2 -6 8 -8 4 4 -8 8 z" fill="none" stroke="{TERRA}" stroke-width="1.3"/>' for i, (k, v) in enumerate((("Type", "House"), ("Size", "1,500-2,500"), ("Systems", "4"), ("Photos", "3")))), 86)], "Compact", "Sample answers"))
    return pairs
