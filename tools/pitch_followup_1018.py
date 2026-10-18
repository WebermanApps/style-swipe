"""Investor pitch follow-up decks, Oct 18 2026 night (Branding): Founder Timeline And Tiles + Timeline Bar And Hiring.
Built on the picks and notes from Founder Hype And Layout and Timeline Refresh (submissions 20:29 / 20:33 ICT); skipped cards re-asked.
10 picks each, Notes on every card, light only, Khand + Hind, drawn MOCKUPS. Founder anonymous (no photo, no name). Forecasts labelled."""
from md1018_kit import *
from pitchv3_1018 import head, tline, tiles, card1, fc, FACTS as F, FS, TS
# ---------------- founder ----------------
# Picks: dated timeline, tiles over badges, hook headline + operator line, platform leads, homes AND finance, understated, text only, no image; carousel skipped.
TL = [("2012", "Founded a construction management company"), ("Since then", "Self-employed construction PM"), ("Today", "Builds multi-million-dollar homes"), ("Platform", "Built the platform himself"), ("Field team", "Hired and trained the first tech")]
TLP = [("Platform", "Built the platform himself"), ("2012", "Founded a construction management company"), ("Since then", "Self-employed construction PM"), ("Today", "Builds multi-million-dollar homes"), ("Field team", "Hired and trained the first tech")]
HF = [("Multi-million homes", "Builds high-end homes", "home"), ("Finance background", "Finance and accounting", "card")]
def qh(title="Built By A Builder", sub="One operator, field and platform", size=16, c=INK, ec=MUTE):
    return head(title, sub, size, c, ec=ec)
def gtl(items, c=MUTE, gap=24): return tline(items, c, gap)
def o(k, label, desc, feel, blocks, n1, n2="Mockup, founder unnamed"):
    return (k, label, desc, feel, S(FS, blocks, (n1, n2)))
def T_FOUNDER():
    pairs, P = make("ff18_", "UpKeep")
    P("Headline", FS, "Headline pairing", "should Built By A Builder be the title with the operator line under it or the other way round?",
      o("bb", "Builder Title, Operator Line", "Built By A Builder on top, operator line below.", "warm", [qh(), gtl(TL)], "Hook first"),
      o("op", "Operator Title, Builder Line", "One Operator, Field And Platform on top.", "focused", [qh("One Operator, Field And Platform", "Built by a builder", 13.5), gtl(TL)], "Message first"))
    P("Layout", FS, "Timeline with tiles", "should the slide be the dated timeline alone or the timeline with two stat tiles under it?",
      o("tl", "Timeline Alone", "Five dated stops, nothing else.", "calm", [qh(), gtl(TL, gap=30)], "One clear story"),
      o("both", "Timeline Plus Two Tiles", "Timeline, then homes and finance tiles.", "practical", [qh(), gtl(TL[:4], gap=22), tiles(HF, h=36, c=MUTE)], "Story plus proof"))
    P("Lead Fact", FS, "Where the platform leads", "should the platform fact sit as a card above the timeline or as the first stop on it?",
      o("card", "Card Above Timeline", "Built the platform himself, in a card on top.", "focused", [qh(), card1("Built the platform himself", "Product made in-house, no agency", MUTE), gtl(TL[:3] + TL[4:], gap=22)], "Stands out most"),
      o("stop", "First Stop On Timeline", "Platform leads the list, then the history.", "calm", [qh(), gtl(TLP, gap=28)], "Stays in one flow"))
    P("Lead Fact", FS, "Homes and finance together", "should high-end homes and the finance background show as two tiles or as one combined line?",
      o("two", "Two Tiles", "Homes tile and finance tile side by side.", "practical", [qh(), card1("Built the platform himself", "Product made in-house", MUTE), tiles(HF, h=40, c=MUTE)], "Each gets weight"),
      o("one", "One Combined Line", "High-end homes, finance and accounting.", "calm", [qh(), card1("Built the platform himself", "Product made in-house", MUTE), card1("High-end homes, finance and accounting", "Both strengths in one line", MUTE)], "Shorter slide"))
    P("Format", FS, "One screen or carousel again", "in the quiet text-only look should all the facts fit on one screen or swipe across three cards?",
      o("one", "One Screen", "Timeline and tiles on a single screen.", "focused", [qh(), gtl(TL[:4], gap=22), tiles(HF, h=34, c=MUTE)], "Nothing hidden"),
      o("car", "Three Card Carousel", "Field, Numbers, Platform cards, text only.", "calm", [qh(), ("carousel", [("Field", "Construction company, 2012", MUTE), ("Numbers", "Finance and accounting", MUTE), ("Platform", "Built it himself", MUTE)], 150, 96), ("note", "Swipe for the next card", "Three cards in all", MUTE)], "Room per theme"))
    P("Tone", FS, "Accent in the quiet look", "should the understated slide stay all grey or keep one thin terracotta rule?",
      o("grey", "All Grey", "No colour at all, grey labels and lines.", "calm", [qh(), gtl(TL)], "Fully understated"),
      o("rule", "One Terracotta Rule", "A single thin terracotta line under the title.", "warm", [qh(ec=TERRA), ("raw", ln(0, 14, 80, TERRA), 8), gtl(TL)], "A touch of brand"))
    P("Dates", FS, "Timeline labels", "should the timeline stops use year and stage labels or short plain words?",
      o("yr", "Year And Stage Labels", "2012, Since then, Today, Platform, Field team.", "practical", [qh(), gtl(TL)], "Anchored in time"),
      o("word", "Plain Word Labels", "Founded, Managed, Builds, Built, Trained.", "calm", [qh(), gtl([("Founded", "Construction management company, 2012"), ("Managed", "Self-employed construction PM"), ("Builds", "Multi-million-dollar homes"), ("Built", "The platform, himself"), ("Trained", "The first tech")])], "Reads like verbs"))
    P("Facts", FS, "How many facts", "should the slide keep five core facts or list all seven background facts?",
      o("five", "Five Core Facts", "Company, PM, homes, platform, first tech.", "focused", [qh(), gtl(TL, gap=30)], "Tight and quick"),
      o("seven", "All Seven Facts", "Adds languages and finance to the timeline.", "practical", [qh(), gtl(TL[:3] + [("Languages", "Speaks multiple languages"), ("Numbers", "Finance and accounting background")] + TL[3:], gap=21)], "Full picture"))
    P("Ending", FS, "Closing line", "should the slide end on a short closing line or stop after the last fact?",
      o("line", "Closing Line", "Hands-on in the field and the product.", "warm", [qh(), gtl(TL, gap=22), ("raw", t(14, 10, "Hands-on in the field and the product.", 8.6, INK, "khand"), 16)], "Ties it together"),
      o("none", "No Closing Line", "Ends on the last timeline stop.", "calm", [qh(), gtl(TL, gap=26)], "Lets facts speak"))
    P("Headline", FS, "Headline size", "should Built By A Builder be set large or at a medium size?",
      o("lg", "Large Headline", "Big Khand title, grey operator line.", "bold", [qh(size=21), gtl(TL, gap=22)], "Hook carries it"),
      o("md", "Medium Headline", "Smaller title, more room for facts.", "calm", [qh(size=14), gtl(TL, gap=26)], "Quieter, balanced"))
    return pairs
# ---------------- timeline ----------------
# Picks: horizontal, progress bar, no Today, dots, faded + footnote, small bars, own tech callout, goal flag; colour and date style skipped (re-asked).
# Note: tech #2 is not needed until 100 to 125 homes, but hiring starts at 75 homes to train.
def th(title="The Road To Apr 1", sub="Launch to 150+ homes"): return head(title, sub, 16, eyebrow="TIMELINE")
def hbar(multi=False, dates="full", fut="grey", path=False):
    c1, c2, c3 = (TERRA, LAGOON, JUNGLE) if multi else (TERRA, TERRA, TERRA)
    s = rect(14, 20, 60, 10, c1, "none", 5)
    if fut == "grey": s += rect(74, 20, 90, 10, "#E4DFD7", "none", 0) + rect(164, 20, 62, 10, "#D6D0C6", "none", 5)
    else: s += rect(74, 20, 90, 10, "none", c2, 0, 1, 'stroke-dasharray="3 2"') + rect(164, 20, 62, 10, "none", c3, 5, 1, 'stroke-dasharray="3 2"')
    if multi: s += rect(74, 31, 90, 2, c2, "none", 1) + rect(164, 31, 62, 2, c3, "none", 1)
    if path:
        for x in (14, 74, 164, 226): s += dot(x, 25, 3.5, INK)
    if dates == "full":
        for x, lab, a in ((14, "Dec 1, 2026", "start"), (119, "Jan to Mar 2027", "middle"), (226, "Apr 1, 2027", "end")): s += t(x, 46, lab, 7, INK, "hind", 600, a)
    else:
        for i, m in enumerate(["Dec", "Jan", "Feb", "Mar", "Apr"]): s += rect(14 + i * 43, 40, 40, 16, (c1 if i == 0 else (c2 if i < 4 else c3)) + ("" if i in (0, 4) else "33"), "none", 4) + t(34 + i * 43, 51.5, m, 7.6, "#FFFFFF" if i in (0, 4) else INK, "khand", anchor="middle")
    s += t(14, 70, "Launch", 6.8, MUTE) + t(119, 70, "Beta, about 50 (Expected*)", 6.8, MUTE, anchor="middle") + t(226, 70, "150+ homes*", 6.8, MUTE, anchor="end")
    return ("raw", s, 80)
def gbars(tech=False):
    return [("bars", [.05, .33, .5, .66, 1], SAFFRON, ["Dec 1", "Beta 50", "75", "100", "150+"], 70)] + ([("raw", rect(96, -28, 36, 12, LAGOON + "1F", LAGOON, 3, 1) + t(114, -19.5, "Hire, 75", 6, LAGOON, "hind", 700, "middle"), 0)] if tech else [])
def flag(txt="Goal: 150+ homes by Apr 1*", big=False):
    if big: return ("raw", f'<path d="M20 0 V44 M20 0 H50 L44 7 L50 14 H20" fill="{SAFFRON}" stroke="{INK}" stroke-width="1.2"/>' + t(62, 26, "150+", 30, TERRA, "khand") + t(130, 26, "homes by Apr 1*", 8.6, INK, "hind", 600), 48)
    return ("raw", f'<path d="M20 0 V26 M20 0 H50 L44 7 L50 14 H20" fill="{SAFFRON}" stroke="{INK}" stroke-width="1.2"/>' + t(60, 12, txt, 8.4, INK, "khand"), 30)
FN = ("raw", t(14, 8, "* Expected and Forecast figures are estimates", 6.6, MUTE), 12)
TECH = card1("Tech #2: hire at 75 homes to train", "Needed on routes at 100 to 125 homes (Forecast)", LAGOON)
def ot(k, label, desc, feel, blocks, n1, n2="Mockup; forecasts labelled"):
    return (k, label, desc, feel, S(TS, blocks, (n1, n2)))
def T_TIMELINE():
    pairs, P = make("tb18_", "UpKeep")
    P("Colour", TS, "Colour accents again", "on the progress bar should each phase get its own colour or should it all stay one terracotta accent?",
      ot("multi", "Colour Per Phase", "Terracotta launch, lagoon Beta, jungle rollout.", "playful", [th(), hbar(multi=True), FN], "Phases stand apart"),
      ot("one", "One Accent", "Terracotta for the whole bar.", "calm", [th(), hbar(), FN], "Calm and on brand"))
    P("Dates", TS, "Date style again", "under the bar should dates be written out in full or shown as month blocks?",
      ot("full", "Full Dates", "Dec 1, 2026 to Apr 1, 2027 spelled out.", "calm", [th(), hbar(dates="full"), FN], "Precise"),
      ot("blocks", "Month Blocks", "Dec to Apr blocks under the bar.", "playful", [th(), hbar(dates="blocks"), FN], "Visual rhythm"))
    P("Tech Two", TS, "Tech hire wording", "should the tech #2 card say hire at 75 to train in one line or show two steps, 75 and 100 to 125?",
      ot("one", "One Line Card", "Hire at 75 homes to train, needed at 100 to 125.", "focused", [th(), hbar(), TECH, FN], "Quick to read"),
      ot("two", "Two Step Card", "75: hire and train. 100 to 125: on routes.", "practical", [th(), hbar(), ("kv", [("At 75 homes", "Hire tech #2, start training"), ("At 100 to 125", "Tech #2 on routes (Forecast)")]), FN], "Shows the plan"))
    P("Tech Two", TS, "Tech mark on the bars", "should the growth bars also flag the 75-home hiring point or leave hiring to the card?",
      ot("flag", "Flag 75 On The Bars", "A small Hire, 75 tag over the 75 bar.", "practical", [th(), hbar(), ("gap", 30)] + gbars(True) + [FN], "Ties hiring to growth"),
      ot("card", "Card Only", "Bars stay clean, hiring lives in its card.", "calm", [th(), hbar(), ("gap", 8)] + gbars() + [TECH], "Less clutter"))
    P("Path", TS, "Stops on the bar", "should the horizontal bar carry small stop dots or stay a plain bar?",
      ot("dots", "Bar With Stop Dots", "Dots at launch, Beta, rollout and Apr 1.", "focused", [th(), hbar(path=True), FN], "Path feel kept"),
      ot("plain", "Plain Bar", "Just the bar and its labels.", "calm", [th(), hbar(), FN], "Simplest"))
    P("Growth", TS, "Where the bars sit", "should the small growth bars sit under the progress bar or replace the bar's labels?",
      ot("under", "Bars Under The Bar", "Progress bar, then growth bars below.", "practical", [th(), hbar(), ("gap", 8)] + gbars() + [FN], "Both views"),
      ot("only", "Bars Carry The Labels", "Growth bars with dates, no separate bar.", "focused", [th(), ("gap", 30), ("bars", [.05, .33, .5, .66, 1], SAFFRON, ["Dec 1", "Mar", "75", "100", "Apr 1"], 90), FN], "One chart"))
    P("Ending", TS, "Goal flag style", "should the Apr 1 goal flag be a small flag with a line or a flag with a big 150+?",
      ot("small", "Small Flag", "Goal: 150+ homes by Apr 1, one line.", "calm", [th(), hbar(), ("gap", 6), flag(), FN], "Stays modest"),
      ot("big", "Flag With Big Number", "Flag beside a large 150+.", "bold", [th(), hbar(), ("gap", 6), flag(big=True), FN], "Ends on ambition"))
    P("Forecast", TS, "Footnote wording", "should the footnote read Expected and Forecast figures are estimates or Forecast, not results yet?",
      ot("est", "Figures Are Estimates", "* Expected and Forecast figures are estimates.", "calm", [th(), hbar(), FN], "Plain and complete"),
      ot("nr", "Not Results Yet", "* Forecast, not results yet.", "focused", [th(), hbar(), ("raw", t(14, 8, "* Forecast, not results yet", 6.6, MUTE), 12)], "Shorter"))
    P("Forecast", TS, "Faded future style", "should the future part of the bar be greyed out or drawn as a dashed outline?",
      ot("grey", "Greyed Out", "Solid launch, grey fill after.", "calm", [th(), hbar(fut="grey"), FN], "Quiet"),
      ot("dash", "Dashed Outline", "Solid launch, dashed outline after.", "focused", [th(), hbar(fut="dash"), FN], "Clearly not yet"))
    P("Headline", TS, "Slide headline", "should the timeline slide be titled The Road To Apr 1 or Launch To 150+ Homes?",
      ot("road", "The Road To Apr 1", "Date-led title.", "calm", [th(), hbar(), flag(), FN], "Clear deadline"),
      ot("homes", "Launch To 150+ Homes", "Goal-led title, Forecast noted.", "bold", [th("Launch To 150+ Homes", "Dec 1, 2026 to Apr 1, 2027"), hbar(), flag(), FN], "Leads with growth"))
    return pairs
