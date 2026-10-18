"""Investor pitch decks v3, Oct 18 2026 (Branding): Founder Hype And Layout + Timeline Refresh.
10 this-or-that picks each, Notes on every card, light only, Khand headings + Hind body, phone-first drawn slides.
Every slide is a drawn MOCKUP. The founder is anonymous: no photo, no name, no identifying details.
Forecast figures are always marked Forecast / Expected."""
from md1018_kit import *
FS = "Founder Slide Mockup"; TS = "Timeline Slide Mockup"
FACTS = [("Construction firm, 2012", "Construction mgmt co.", "home"),
         ("Self-employed PM", "Construction projects", "cal"),
         ("Multi-million homes", "Builds high-end homes", "home"),
         ("Multilingual", "Speaks multiple languages", "speaker"),
         ("Finance background", "Finance and accounting", "card"),
         ("AI agent trainer", "Expert level", "star"),
         ("Built the platform", "Made it himself", "phone"),
         ("Trained the first tech", "Hired and trained him", "check")]
LONG = ["Founded a construction management company in 2012", "Self-employed construction PM", "Builds multi-million-dollar homes", "Speaks multiple languages",
        "Finance and accounting background", "Expert AI agent trainer", "Built the platform himself", "Hired and trained the first tech"]
MK = lambda y=0: t(226, 17 + y, "MOCKUP", 6.5, MUTE, "hind", 700, "end", 'letter-spacing="1"')
def head(title, sub="", size=17, c=INK, eyebrow="THE FOUNDER", ec=TERRA):
    return ("raw", t(14, 8, eyebrow, 7, ec, "hind", 700, extra='letter-spacing="1.2"') + t(14, 28, title, size, c, "khand") + (t(14, 41, sub, 7.5, MUTE) if sub else ""), 48 if sub else 38)
def tline(items, c=TERRA, gap=24):
    s = f'<line x1="22" y1="4" x2="22" y2="{len(items)*gap-10}" stroke="#D6D0C6" stroke-width="1.5"/>'
    for i, (a, b) in enumerate(items):
        y = i * gap; s += dot(22, y + 6, 4, c) + t(34, y + 9, a, 8.6, INK, "khand") + t(34, y + 18, b, 6.4, MUTE)
    return ("raw", s, len(items) * gap)
def tiles(items, cols=2, h=40, icons=False, c=None):
    w = (212 - (cols - 1) * 6) / cols; s = ""
    for i, (big, small, k) in enumerate(items):
        x, y = 14 + (i % cols) * (w + 6), (i // cols) * (h + 6); cc = c or ACC[i % 4]
        s += rect(x, y, w, h, "#FFFFFF", LINE, 7) + rect(x, y, 3, h, cc, "none", 1.5)
        tx = x + 10
        if icons: s += rect(x + 8, y + 8, 18, 18, cc + "1F", "none", 5) + ic(k, x + 10, y + 10, 14, cc, 2); tx = x + 32
        fs = 8.2 if cols == 1 else (7.4 if icons else 8)
        s += t(tx, y + 17, big, fs, INK, "khand") + t(tx, y + 29, small, 6, MUTE)
    rows = (len(items) + cols - 1) // cols
    return ("raw", s, rows * (h + 6))
def badges(items, icons=True):
    s, x, y = "", 14, 0
    for i, (a, _, k) in enumerate(items):
        w = len(a) * 3.7 + (30 if icons else 16)
        if x + w > 226: x, y = 14, y + 26
        c = ACC[i % 4]; s += rect(x, y, w, 20, c + "14", c + "66", 10, 1)
        if icons: s += ic(k, x + 6, y + 4, 12, c, 2)
        s += t(x + (22 if icons else 8), y + 13.5, a, 7, INK, "hind", 600); x += w + 6
    return ("raw", s, y + 28)
def card1(a, b, c=TERRA, big=False):
    return ("raw", rect(14, 0, 212, 62 if big else 48, c + "12", "none", 8) + rect(14, 0, 4, 62 if big else 48, c, "none", 2) + t(26, 24 if big else 20, a, 15 if big else 11, INK, "khand") + t(26, 42 if big else 36, b, 7.6, MUTE), 70 if big else 56)
def o(k, label, desc, feel, loc, blocks, n1, n2="Mockup, founder unnamed"):
    return (k, label, desc, feel, S(loc, blocks, (n1, n2)))
F = FACTS
def T_FOUNDER():
    pairs, P = make("fh18_", "UpKeep")
    P("Layout", FS, "Fact layout", "should the founder facts run as a dated timeline or as a grid of stat tiles?",
      o("tl", "Dated Timeline", "Facts as a story from 2012 to today.", "calm", FS, [head("Built By A Builder"), tline([("2012", "Founded a construction management company"), ("Since then", "Self-employed construction PM"), ("Today", "Builds multi-million-dollar homes"), ("Platform", "Built the platform himself"), ("Field team", "Hired and trained the first tech")])], "Reads like a story", "Mockup, founder unnamed"),
      o("tiles", "Stat Tiles Grid", "Six short tiles, two across.", "focused", FS, [head("Built By A Builder"), tiles(F[:6])], "Scannable in seconds", "Mockup, founder unnamed"))
    P("Layout", FS, "Tiles or badges", "should the facts sit in stat tiles with a short line each or as a cloud of small badges?",
      o("tiles", "Stat Tiles", "Bigger tiles, one supporting line each.", "practical", FS, [head("The Founder"), tiles(F[1:7])], "More room to explain"),
      o("badges", "Small Badges", "All eight facts as compact pill badges.", "playful", FS, [head("The Founder"), badges(F)], "Everything at a glance"))
    P("Headline", FS, "Headline wording", "should the slide headline be plain like The Founder or a hook like Built By A Builder?",
      o("plain", "The Founder", "Neutral, standard pitch label.", "calm", FS, [head("The Founder", "Construction, finance and the platform"), tiles(F[:4])], "Safe and familiar"),
      o("hook", "Built By A Builder", "A short hook that sells the background.", "bold", FS, [head("Built By A Builder", "Construction, finance and the platform", c=TERRA), tiles(F[:4])], "Memorable line"))
    P("Headline", FS, "Second headline idea", "should the headline say From Job Sites To Software or One Operator, Field And Platform?",
      o("sites", "From Job Sites To Software", "Stresses the move from building to product.", "warm", FS, [head("From Job Sites To Software", size=15), tline([("Job sites", "Construction management company, 2012"), ("Homes", "Builds multi-million-dollar homes"), ("Software", "Built the platform himself")])], "Clear journey"),
      o("oper", "One Operator, Field And Platform", "Stresses that one person covers both sides.", "focused", FS, [head("One Operator, Field And Platform", size=13.5), tiles([F[0], F[6], F[7], F[4]])], "Hands-on message"))
    P("Lead Fact", FS, "Which fact leads", "should the top fact be founding a construction company in 2012 or building the platform himself?",
      o("co", "Construction Company Leads", "Founded a construction management company, 2012.", "calm", FS, [head("The Founder"), card1("Founded a construction company", "Construction management, since 2012", TERRA, True), tiles([F[6], F[2], F[4], F[7]])], "Track record first"),
      o("plat", "Platform Leads", "Built the platform himself, then the background.", "bold", FS, [head("The Founder"), card1("Built the platform himself", "Product made in-house, no agency", LAGOON, True), tiles([F[0], F[2], F[4], F[7]])], "Product skill first"))
    P("Lead Fact", FS, "Second lead option", "should the top fact be building multi-million-dollar homes or the finance and accounting background?",
      o("homes", "High-End Homes Leads", "Builds multi-million-dollar homes, up top.", "warm", FS, [head("The Founder"), card1("Builds multi-million-dollar homes", "High-end residential construction", TERRA, True), tiles([F[0], F[4], F[5], F[6]])], "Quality signal"),
      o("fin", "Finance Background Leads", "Finance and accounting background, up top.", "practical", FS, [head("The Founder"), card1("Finance and accounting background", "Knows unit costs and margins", JUNGLE, True), tiles([F[0], F[2], F[5], F[6]])], "Investor comfort"))
    P("Tone", FS, "Hype level", "should the founder slide feel bold and loud or calm and understated?",
      o("bold", "Bold", "Dark band, big Khand, terracotta highlights.", "bold", FS, [("raw", rect(0, -8, W, 70, INK) + t(14, 8, "THE FOUNDER", 7, TERRA, "hind", 700, extra='letter-spacing="1.2"') + t(14, 32, "Builder. Operator.", 19, "#FFFFFF", "khand") + t(14, 52, "Platform built by hand.", 19, TERRA, "khand"), 72), tiles(F[:4], c=TERRA)], "High energy"),
      o("calm", "Understated", "White space, plain grey labels, no highlights.", "calm", FS, [head("About the founder", size=15, c=MUTE, ec=MUTE), ("raw", "".join(t(14, 10 + i * 20, a, 8.4, INK, "hind", 500) + ln(16 + i * 20) for i, a in enumerate(LONG)), 164)], "Lets facts speak"))
    P("Icons", FS, "Icons", "should each fact carry a small drawn icon or be text only?",
      o("ic", "With Icons", "Tinted icon square beside each fact.", "playful", FS, [head("The Founder"), tiles(F[:8], icons=True, h=36)], "Faster to scan"),
      o("none", "Text Only", "Same tiles, no icons.", "calm", FS, [head("The Founder"), tiles(F[:8], h=36)], "Cleaner, more serious"))
    P("Format", FS, "One screen or carousel", "should all the facts fit on one screen or swipe across a short carousel?",
      o("one", "One Screen", "Everything on one phone screen.", "focused", FS, [head("The Founder"), badges(F), card1("Hands-on in the field and the product", "One slide, no swiping")], "Nothing hidden"),
      o("car", "Swipe Carousel", "Three cards: Field, Numbers, Platform.", "playful", FS, [head("The Founder"), ("carousel", [("Field", "Construction company, 2012", TERRA), ("Numbers", "Finance and accounting", JUNGLE), ("Platform", "Built it himself", LAGOON)], 150, 96), ("note", "Swipe for the next card", "Three cards in all")], "Room per theme"))
    P("Identity", FS, "Founder visual", "with no photo should the slide use a neutral house icon in place of a portrait or no image at all?",
      o("icon", "Neutral House Icon", "A plain terracotta house mark, no face, no name.", "warm", FS, [("raw", f'<circle cx="120" cy="34" r="30" fill="{TERRA}1F"/>' + ic("home", 102, 16, 36, TERRA, 2), 72), ("raw", t(120, 10, "The Founder", 17, INK, "khand", anchor="middle") + t(120, 24, "Builder, operator, platform maker", 7.5, MUTE, anchor="middle"), 34), tiles(F[:4])], "Friendly anchor"),
      o("none", "No Image", "Type and facts only.", "calm", FS, [head("The Founder", "Builder, operator, platform maker"), tiles(F[:6])], "More room for facts"))
    return pairs
# ---------------- timeline ----------------
MS = [("Dec 1, 2026", "Launch", "Live", TERRA, "home"), ("Jan to Mar 2027", "Beta, about 50 subscribers", "Expected", LAGOON, "cal"),
      ("Apr 1, 2027", "Full rollout", "Planned", JUNGLE, "star"), ("By Apr 1, 2027", "150+ homes, tech #2 hired at 100", "Forecast", SAFFRON, "check")]
def fc(x, y, s="FORECAST", c=SAFFRON):
    w = len(s) * 4.2 + 10; return rect(x, y, w, 12, "#FFFFFF", c, 3, 1, 'stroke-dasharray="2 1.5"') + t(x + w / 2, y + 8.6, s, 6, "#8a6510" if c == SAFFRON else c, "hind", 700, "middle", 'letter-spacing=".4"')
def vpath(icons=False, today=False, multi=True, mark="chip", gap=46):
    s = ""
    for i, (d, what, st, c, k) in enumerate(MS):
        y = i * gap; c = c if multi else TERRA; fut = st in ("Expected", "Forecast")
        if i < 3: s += f'<line x1="26" y1="{y+12}" x2="26" y2="{y+gap}" stroke="{c if not fut else "#BDB6AA"}" stroke-width="2" {"stroke-dasharray=\'3 3\'" if (fut or MS[i+1][2] in ("Expected","Forecast")) and mark=="dash" else ""}/>'
        if icons: s += f'<circle cx="26" cy="{y+10}" r="11" fill="{c}1F" stroke="{c}" stroke-width="1.2"/>' + ic(k, 19, y + 3, 14, c, 2)
        else: s += f'<circle cx="26" cy="{y+10}" r="5" fill="{c if not fut else "#FFFFFF"}" stroke="{c}" stroke-width="1.6"/>'
        s += t(44, y + 9, d, 9.5, INK, "khand") + t(44, y + 21, what, 7.2, MUTE)
        if fut and mark in ("chip", "dash"): s += fc(170, y + 1, st.upper())
    if today: s += ln(-6, 14, 226, TERRA) + rect(150, -13, 76, 13, TERRA, "none", 3) + t(188, -4, "TODAY, OCT 2026", 6, "#FFFFFF", "hind", 700, "middle")
    return ("raw", s, len(MS) * gap)
def hpath(icons=False, today=False, multi=True):
    s = ln(40, 24, 216, "#D6D0C6"); xs = [24, 88, 152, 216]
    for i, (d, what, st, c, k) in enumerate(MS):
        x = xs[i]; c = c if multi else TERRA
        if icons: s += f'<circle cx="{x}" cy="40" r="10" fill="#FFFFFF" stroke="{c}" stroke-width="1.4"/>' + ic(k, x - 6, 34, 12, c, 2)
        else: s += f'<circle cx="{x}" cy="40" r="5" fill="{c}"/>'
        s += t(x, 64, d.replace(", 2026", "").replace(", 2027", "").replace(" 2027", ""), 7.6, INK, "khand", anchor="middle") + t(x, 74, what.split(",")[0], 5.8, MUTE, anchor="middle")
        if st in ("Expected", "Forecast"): s += t(x, 84, st.upper(), 5.6, "#8a6510", "hind", 700, "middle")
    if today: s += f'<line x1="14" y1="24" x2="14" y2="52" stroke="{TERRA}" stroke-width="2"/>' + t(14, 18, "TODAY", 6, TERRA, "hind", 700, "middle")
    return ("raw", s, 94)
def mcards(multi=True, mark="chip"):
    s = ""
    for i, (d, what, st, c, k) in enumerate(MS):
        y = i * 44; c = c if multi else TERRA; fut = st in ("Expected", "Forecast")
        s += rect(14, y, 212, 38, "#FFFFFF" if not (fut and mark == "fade") else SOFT, LINE, 8, 1, 'stroke-dasharray="3 2"' if fut and mark == "fade" else "") + rect(14, y, 4, 38, c, "none", 2)
        s += t(26, y + 16, d, 9.5, INK if not (fut and mark == "fade") else MUTE, "khand") + t(26, y + 29, what, 7, MUTE)
        if fut: s += fc(160, y + 13, st.upper()) if mark == "chip" else t(218, y + 22, st + "*", 7, MUTE, "hind", 600, "end")
    return ("raw", s, 176)
def pbar(today=False):
    s = rect(14, 20, 212, 10, "#EEEAE4", "none", 5) + rect(14, 20, 60, 10, TERRA, "none", 5)
    s += rect(74, 20, 152, 10, "none", SAFFRON, 5, 1, 'stroke-dasharray="3 2"')
    for x, lab in ((14, "Dec 1"), (74, "Jan"), (150, "Mar"), (226, "Apr 1")): s += t(x, 44, lab, 7, INK, "hind", 600, "middle" if 14 < x < 226 else ("start" if x == 14 else "end"))
    if today: s += t(14, 12, "TODAY: PRE-LAUNCH", 6.2, TERRA, "hind", 700)
    s += t(120, 60, "Beta, about 50 subscribers (Expected)", 7.4, MUTE, anchor="middle") + t(120, 74, "150+ homes by Apr 1, tech #2 at 100 (Forecast)", 7.4, MUTE, anchor="middle")
    return ("raw", s, 84)
def ot(k, label, desc, feel, blocks, n1, n2="Mockup; forecasts labelled"):
    return (k, label, desc, feel, S(TS, blocks, (n1, n2)))
def th(sub="Launch to 150+ homes"): return head("The Road To Apr 1", sub, 16, eyebrow="TIMELINE")
def T_TIMELINE():
    pairs, P = make("tr18_", "UpKeep")
    P("Path", TS, "Path direction", "should the timeline run as a vertical path down the phone or a horizontal path across it?",
      ot("v", "Vertical Path", "Milestones stacked top to bottom.", "calm", [th(), vpath()], "Fits a phone screen"),
      ot("h", "Horizontal Path", "Four stops left to right, short labels.", "focused", [th(), hpath(), ("note", "Beta about 50 subscribers is Expected", "150+ homes and tech #2 are Forecast")], "Classic slide look"))
    P("Format", TS, "Cards or progress bar", "should the milestones be separate cards or one progress bar from launch to Apr 1?",
      ot("cards", "Milestone Cards", "One card per milestone with a colour edge.", "practical", [th(), mcards()], "Room for detail"),
      ot("bar", "Progress Bar", "A single bar, solid for launch, dashed after.", "focused", [th(), ("gap", 8), pbar(), ("stats", [("50", "Beta, Expected"), ("150+", "Homes, Forecast"), ("100", "Tech #2 hire")], "tint")], "One look, whole span"))
    P("Today", TS, "Today marker", "should the slide show a Today marker before launch or leave it out?",
      ot("yes", "Show Today", "A terracotta line: Today, Oct 2026, pre-launch.", "focused", [th(), ("gap", 14), vpath(today=True, gap=42)], "Shows how close launch is"),
      ot("no", "No Today Marker", "Just the milestones.", "calm", [th(), vpath(gap=42)], "Stays accurate longer"))
    P("Icons", TS, "Illustrated icons", "should each milestone carry an illustrated icon or a simple dot?",
      ot("ic", "Illustrated Icons", "House, calendar, star and check icons.", "playful", [th(), vpath(icons=True)], "Friendlier, easy to scan"),
      ot("dot", "Simple Dots", "Small dots on the line.", "calm", [th(), vpath()], "Minimal and tidy"))
    P("Colour", TS, "Colour accents", "should each phase get its own colour accent or should the whole timeline use one terracotta accent?",
      ot("multi", "Colour Per Phase", "Terracotta, lagoon, jungle and saffron.", "playful", [th(), mcards(True)], "Phases stand apart"),
      ot("one", "One Accent", "Terracotta for every milestone.", "calm", [th(), mcards(False)], "Calm and on brand"))
    P("Forecast", TS, "How forecasts are marked", "should forecast milestones get a dashed Forecast chip or a faded card with an Expected footnote?",
      ot("chip", "Dashed Forecast Chip", "A dashed saffron chip on each forecast row.", "focused", [th(), mcards(mark="chip")], "Impossible to miss"),
      ot("fade", "Faded Card And Footnote", "Forecast cards greyed, a star footnote below.", "calm", [th(), mcards(mark="fade"), ("raw", t(14, 8, "* Expected and Forecast figures are estimates", 6.8, MUTE), 12)], "Quieter, still honest"))
    P("Growth", TS, "Growth figures", "should the growth to 150+ homes show as small bars or as one big forecast number?",
      ot("bars", "Small Bars", "Launch, 50 in Beta, 100, 150+, marked Forecast.", "practical", [th(), ("bars", [.05, .33, .66, 1], SAFFRON, ["Dec 1", "Beta 50", "100", "150+"], 80), ("raw", fc(14, 0, "FORECAST") + t(80, 9, "Tech #2 hired at 100 homes", 7.4, MUTE), 18)], "Shows the climb"),
      ot("big", "One Big Number", "150+ homes by Apr 1, Forecast, large.", "bold", [th(), ("raw", t(120, 56, "150+", 54, TERRA, "khand", anchor="middle") + t(120, 74, "homes by Apr 1, 2027", 9, INK, "hind", 600, "middle") + fc(96, 82, "FORECAST"), 100), ("note", "Tech #2 hired at 100 homes", "Beta about 50 subscribers, Expected")], "Punchy headline figure"))
    P("Tech Two", TS, "Second tech hire", "should hiring tech #2 at 100 homes sit as a marker on the path or as its own callout card?",
      ot("mark", "Marker On The Path", "A small flag between Beta and Apr 1.", "calm", [th(), vpath(gap=40), ("raw", rect(140, -66, 86, 14, LAGOON + "1F", LAGOON, 3, 1) + t(183, -56, "Tech #2 at 100 homes", 6.4, LAGOON, "hind", 700, "middle"), 2)], "Keeps it in the flow"),
      ot("card", "Own Callout Card", "A separate card under the path.", "practical", [th(), vpath(gap=32), card1("Tech #2 hired at 100 homes", "Forecast, on the way to 150+", LAGOON)], "Highlights the hiring plan"))
    P("Dates", TS, "Date style", "should dates be written out in full or shown as month blocks?",
      ot("full", "Full Dates", "Dec 1, 2026 and Apr 1, 2027 spelled out.", "calm", [th(), vpath()], "Precise"),
      ot("blocks", "Month Blocks", "A row of months, milestones under them.", "playful", [th(), ("raw", "".join(rect(14 + i * 43, 0, 40, 28, (TERRA if i == 0 else LAGOON if i < 4 else JUNGLE) + ("" if i in (0, 4) else "33"), "none", 5) + t(34 + i * 43, 18, m, 8.5, "#FFFFFF" if i in (0, 4) else INK, "khand", anchor="middle") for i, m in enumerate(["Dec", "Jan", "Feb", "Mar", "Apr"])) + t(34, 42, "Launch", 6.6, INK, "hind", 600, "middle") + t(120, 42, "Beta, about 50 (Expected)", 6.6, INK, "hind", 600, "middle") + t(206, 42, "Apr 1", 6.6, INK, "hind", 600, "middle"), 52), card1("150+ homes by Apr 1", "Forecast; tech #2 hired at 100", SAFFRON)], "Visual rhythm"))
    P("Ending", TS, "How it ends", "should the timeline end on an Apr 1 goal flag or on a short forecast summary card?",
      ot("flag", "Goal Flag", "A flag at Apr 1 reading 150+ homes, Forecast.", "bold", [th(), vpath(gap=34), ("raw", f'<path d="M30 0 V30 M30 0 H60 L54 7 L60 14 H30" fill="{SAFFRON}" stroke="{INK}" stroke-width="1.2"/>' + t(70, 12, "Goal: 150+ homes (Forecast)", 8.4, INK, "khand"), 34)], "Ends on ambition"),
      ot("sum", "Summary Card", "Three lines: launch, Beta, Apr 1 forecast.", "practical", [th(), ("kv", [("Launch", "Dec 1, 2026"), ("Beta, Expected", "~50 subscribers"), ("Apr 1, Forecast", "150+ homes"), ("Tech #2", "at 100 homes")])], "Easy recap"))
    return pairs
