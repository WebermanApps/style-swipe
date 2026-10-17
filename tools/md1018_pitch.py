"""UpKeep investor pitch app + forecast decks (report 1c). Presentation and design choices only. Every money figure in a mockup is a labelled
SAMPLE placeholder (X, $X.XM): no real or invented financials. No quotes or testimonials anywhere (Max: 'the tech will speak for itself').
Settled and not re-asked: ten slides, problem story opening, vision close, crisp data, clean charts, white slides with an illustration half, topic
headlines, bars with a callout, milestone timeline, demo before the ask, full-slide recording, founder story + advisors, one funnel, risk + fix
table, one chart three lines, legend above, split bar, chips column left, band stays, rough shading, green/terracotta flags, chart first, swipe tiles.
Queued decks' asks (Story Flow And App Format; Ask, Demo And Chart Looks; Story, Slide Looks And Pitch App; Ask, Traction And Market Size;
Key Points And Results Table) are not repeated."""
from md1018_kit import *
PA = "UpKeep Investor Pitch App"; FC = "UpKeep Forecast App"
def slide(title, body, foot=(), lbl="UpKeep Investor Pitch App"):
    """A white 16:9 slide drawn inside the phone screen."""
    g = rect(14, 0, 212, 120, "#FFFFFF", "#D6D0C6", 6) + t(24, 18, title.upper(), 7.5, MUTE, "hind", 700, extra='letter-spacing="1"') + body
    return [("raw", g, 128)] + list(foot)
def bars_body(callout=True):
    s = "".join(rect(30 + i * 34, 100 - h, 22, h, TERRA if i == 4 else TERRA + "55", "none", 2) for i, h in enumerate((20, 32, 44, 58, 74)))
    if callout: s += rect(150, 22, 66, 20, CREAM, TERRA, 3) + t(183, 35, "Key point", 7.5, INK, "hind", 600, "middle")
    return s + t(24, 112, "SAMPLE NUMBERS", 6.5, "#8a6510", "hind", 700)
def T_P1():
    pairs, P = make("md18pa_", "UpKeep"); L = "UpKeep Investor Pitch App"
    P("Pitch App", PA, "Jump between slides", "should the app jump between slides with a strip of small slide pictures along the bottom or a menu list of slide titles?",
      ("strip", "Slide Picture Strip", "A swipe strip of tiny slides along the bottom.", "playful", S(L, slide("Members", bars_body(), [("carousel", [("1 Problem", ""), ("2 Solution", ""), ("3 Product", "")], 66, 34, False)]), ("Jump by picture", "Carousel of the ten slides"))),
      ("menu", "Menu Of Slide Titles", "A menu button opens the ten titles in a list.", "calm", S(L, slide("Members", bars_body(), [("cards", [("1  Problem", ""), ("2  Solution", ""), ("3  Product", "")], [INK], "none", "line", 22)]), ("Jump by name", "Hidden until opened"))))
    P("Pitch App", PA, "Progress", "should progress through the pitch show as a thin bar across the top or a small 3 of 10 count?",
      ("bar", "Thin Bar On Top", "A terracotta line fills as you go.", "calm", S(L, [("bar", .3, TERRA)] + slide("Problem", bars_body(False)), ("Quiet progress", ""))),
      ("count", "Small 3 Of 10 Count", "A count in the corner of every slide.", "practical", S(L, slide("Problem", bars_body(False) + t(216, 112, "3 / 10", 7.5, MUTE, "hind", 600, "end")), ("Exact place in the pitch", ""))))
    P("Pitch App", PA, "Opening screen", "should the app open on a cover with a Start Pitch button or drop straight into the first slide?",
      ("cover", "Cover With Start Pitch", "Logo, one line and a Start button.", "focused", S(L, [("raw", rect(14, 0, 212, 150, CREAM, "none", 8) + t(120, 70, "Smart Upkeep", 22, INK, "khand", anchor="middle") + t(120, 88, "Investor pitch", 8.5, MUTE, anchor="middle"), 158), ("btn", "Start Pitch", "fill", TERRA)], ("A clear start", "Good when sent ahead"))),
      ("first", "Straight Into Slide One", "The problem story is the first thing seen.", "playful", S(L, slide("Problem", photo(24, 26, 90, 80, TERRA, "house") + t(124, 50, "A small leak", 10, INK, "khand") + t(124, 64, "left alone", 10, INK, "khand")), ("No extra tap", "Story starts at once"))))
    P("Pitch App", PA, "Wide screen", "on a laptop should each slide sit centred at a fixed slide shape with arrows or fill the window as a tall scrolling page?",
      ("fixed", "Centred Slide With Arrows", "A classic slide shape, arrows left and right.", "calm", S("UpKeep Investor Pitch App · 1280", [("desk", rect(30, 6, 150, 84, "#FFFFFF", "#D6D0C6", 4) + bars_body().replace('x="', 'x="').replace("", "") [:0] + "".join(rect(46 + i * 24, 80 - h, 16, h, TERRA + "77", "none", 2) for i, h in enumerate((14, 22, 30, 40, 52))) + t(10, 50, "\u2039", 14, TERRA, "hind") + t(196, 50, "\u203a", 14, TERRA, "hind"), 110)], ("Feels like a pitch deck", ""))),
      ("fill", "Fills The Window", "Slides stack into one tall page you scroll.", "playful", S("UpKeep Investor Pitch App · 1280", [("desk", rect(0, 6, 206, 40, CREAM, "none", 4) + t(10, 30, "Problem", 12, INK, "khand") + rect(0, 52, 206, 40, "#FFFFFF", LINE, 4) + t(10, 76, "Solution", 12, INK, "khand"), 110)], ("Feels like an app", ""))))
    P("Key Points", PA, "Key point on each slide", "should each slide end with one key point banner at the bottom or highlight the key phrase inside the headline?",
      ("banner", "Key Point Banner", "A cream band: the one thing to remember.", "practical", S(L, slide("Problem", bars_body(False) + rect(14, 96, 212, 24, CREAM, "none", 0) + rect(14, 96, 3, 24, TERRA) + t(24, 112, "Key point: small leaks become big bills", 7.5, INK, "hind", 600)), ("Same spot on every slide", ""))),
      ("phrase", "Highlighted Phrase", "A terracotta marker under the key words.", "playful", S(L, slide("Problem", rect(24, 40, 90, 6, TERRA + "44", "none", 2) + t(24, 42, "Small leaks", 14, INK, "khand") + t(24, 60, "become big bills", 14, INK, "khand")), ("Headline carries the point", ""))))
    P("Key Points", PA, "Key points recap", "before the vision slide should a short swipe carousel of key point cards recap the pitch or should the pitch go straight to the close?",
      ("recap", "Key Points Carousel", "Three to five cards, one point each.", "playful", S(L, [("h", "What To Remember", 13), ("carousel", [("Prevent, not repair", "Point one", TERRA), ("Every visit recorded", "Point two", LAGOON), ("Dense routes", "Point three", JUNGLE)], 140, 80, True, False, 0)], ("Points called out together", "Then the vision slide"))),
      ("close", "Straight To The Close", "Ten slides, no recap.", "calm", S(L, slide("Vision", photo(24, 26, 192, 80, LAGOON, "sun")), ("Keeps it to ten slides", ""))))
    P("Pitch App", PA, "Numbers on slides", "should slide numbers pull live from the forecast app with an Updated stamp or stay a fixed snapshot with its date?",
      ("live", "Live From The Forecast", "Numbers refresh with an Updated tag.", "focused", S(L, slide("Forecast", bars_body(False) + t(216, 112, "Updated today", 7.5, JUNGLE, "hind", 600, "end")), ("Always the latest", "Same numbers as the forecast"))),
      ("snap", "Fixed Snapshot", "Numbers frozen with As Of Oct 18.", "calm", S(L, slide("Forecast", bars_body(False) + t(216, 112, "As of Oct 18", 7.5, MUTE, "hind", 600, "end")), ("Never changes mid-talk", ""))))
    P("Pitch App", PA, "Placeholder numbers", "until real numbers exist should sample figures carry a SAMPLE corner tag or show as greyed X placeholders?",
      ("tag", "SAMPLE Corner Tag", "Shaped like real numbers, clearly tagged.", "practical", S(L, slide("Traction", t(24, 60, "$X.XM", 24, INK, "khand") + t(24, 76, "yearly revenue", 7.5, MUTE) + rect(160, 26, 56, 14, "#FFFFFF", SAFFRON, 3, 1, 'stroke-dasharray="3 2"') + t(188, 36, "SAMPLE", 7.5, "#8a6510", "hind", 700, "middle")), ("Looks finished, never mistaken", ""))),
      ("grey", "Greyed X Placeholders", "Grey XX blocks where numbers will go.", "calm", S(L, slide("Traction", rect(24, 40, 80, 24, "#E5E0D8", "none", 3) + t(64, 57, "XX", 14, FAINT, "khand", anchor="middle") + t(24, 80, "yearly revenue", 7.5, MUTE)), ("Obviously unfinished", ""))))
    P("Pitch App", PA, "Slide change", "should moving to the next slide be a quick fade or a slide-over from the side?",
      ("fade", "Quick Fade", "The next slide fades in over a quarter second.", "calm", S(L, slide("Solution", photo(24, 26, 192, 80, JUNGLE, "house").replace('fill="#0B6E4F1A"', 'fill="#0B6E4F0D"')), ("Calm and quick", ""))),
      ("slide", "Slide Over", "The next slide pushes in from the right.", "playful", S(L, [("raw", rect(14, 0, 150, 120, "#FFFFFF", "#D6D0C6", 6) + rect(170, 0, 150, 120, "#FFFFFF", "#D6D0C6", 6) + t(24, 18, "PROBLEM", 7.5, MUTE, "hind", 700) + t(180, 18, "SOLUTION", 7.5, MUTE, "hind", 700), 128)], ("Feels like swiping", ""))))
    P("Pitch App", PA, "Product screens", "should the product slide show app screens as an auto-advancing carousel or three screens side by side?",
      ("carousel", "Auto Carousel Of Screens", "Member app, tech app, report, one after another.", "playful", S(L, slide("Product", "".join(rect(70 + i * 56, 26, 46, 80, "#FFFFFF", LINE, 6) for i in range(2)) + rect(14, 26, 46, 80, "#FFFFFF", TERRA, 6)) + [("cdots", 3, 0, True)], ("One screen at a time", "Loops on its own"))),
      ("three", "Three Side By Side", "All three screens at once.", "calm", S(L, slide("Product", "".join(rect(28 + i * 64, 26, 52, 84, "#FFFFFF", LINE, 6) + rect(28 + i * 64, 26, 52, 10, ACC[i] + "33", "none", 6) for i in range(3))), ("See the whole product", ""))))
    return pairs
def T_P2():
    pairs, P = make("md18pv_", "UpKeep"); L = "UpKeep Investor Pitch App"
    P("Valuation", PA, "Valuation display", "should the team's honest valuation show as a low to high range bar or as one number with how it was worked out?",
      ("range", "Low To High Range Bar", "A bar with low, middle and high marks.", "focused", S(L, slide("Our Honest Value", rect(30, 60, 180, 8, LAGOON + "33", "none", 4) + rect(80, 60, 70, 8, LAGOON, "none", 4) + t(30, 84, "$X.XM", 9, MUTE, "khand") + t(115, 52, "$X.XM", 11, INK, "khand", anchor="middle") + t(210, 84, "$X.XM", 9, MUTE, "khand", anchor="end") + t(24, 112, "SAMPLE NUMBERS", 6.5, "#8a6510", "hind", 700)), ("Shows the honest spread", ""))),
      ("one", "One Number And Method", "One figure with a short how-we-got-here line.", "calm", S(L, slide("Our Honest Value", t(120, 66, "$X.XM", 26, INK, "khand", anchor="middle") + t(120, 84, "based on a revenue multiple", 7.5, MUTE, anchor="middle") + t(24, 112, "SAMPLE NUMBERS", 6.5, "#8a6510", "hind", 700)), ("One clear answer", ""))))
    P("Valuation", PA, "Valuation methods", "should the methods behind the valuation show as a swipe carousel of method cards or one short footnote line?",
      ("cards", "Carousel Of Method Cards", "Revenue multiple, similar companies, future cash.", "playful", S(L, [("h", "How We Got There", 13), ("carousel", [("Revenue multiple", "$X.XM  ·  sample", LAGOON), ("Similar companies", "$X.XM  ·  sample", JUNGLE), ("Future cash", "$X.XM  ·  sample", TERRA)], 130, 70, True, False, 0), ("sample",)], ("Each method in plain words", ""))),
      ("foot", "One Footnote Line", "Methods named in small type under the number.", "calm", S(L, slide("Our Honest Value", t(120, 66, "$X.XM", 26, INK, "khand", anchor="middle") + t(24, 104, "Average of three methods; details in the forecast app", 6.8, MUTE) + t(24, 114, "SAMPLE", 6.5, "#8a6510", "hind", 700)), ("Keeps the slide clean", ""))))
    P("Valuation", PA, "Valuation over time", "as the company grows should the valuation slide show how the team's estimate has moved over time or only today's estimate?",
      ("history", "Estimate Over Time", "A small line of each month's estimate.", "practical", S(L, slide("Our Honest Value", f'<polyline points="30,96 70,90 110,80 150,66 200,50" fill="none" stroke="{LAGOON}" stroke-width="2"/>' + dot(200, 50, 3, LAGOON) + t(24, 112, "SAMPLE LINE", 6.5, "#8a6510", "hind", 700)), ("Shows honest change", ""))),
      ("today", "Today Only", "Just the current estimate.", "calm", S(L, slide("Our Honest Value", t(120, 66, "$X.XM", 26, INK, "khand", anchor="middle") + t(24, 112, "SAMPLE", 6.5, "#8a6510", "hind", 700)), ("Simple", ""))))
    BL = [("UpKeep", .78, .25, 16, TERRA), ("Handyman apps", .3, .62, 13, LAGOON), ("One-trade pros", .25, .78, 11, SAFFRON), ("Home warranty", .62, .7, 12, JUNGLE)]
    P("Blob Chart", PA, "Blob sizes", "on the blob chart should each blob be sized by how big that market is or should every blob be the same size?",
      ("sized", "Sized By Market", "Bigger blob, bigger market.", "playful", S(L, [("blobs", BL), ("p", "Blob size: market size (sample)")], ("Two things in one picture", ""))),
      ("same", "Same Size Dots", "Only the position matters.", "calm", S(L, [("blobs", [(n, x, y, 9, c) for n, x, y, r, c in BL], 110, ("Repair", "Prevent", "One trade", "Whole home"), "beside")], ("Easy to read", ""))))
    P("Blob Chart", PA, "Blob names", "should the names sit inside each blob or beside it?",
      ("inside", "Names Inside", "Each blob carries its own name.", "calm", S(L, [("blobs", BL)], ("Tidy", ""))),
      ("beside", "Names Beside", "Small labels next to each blob.", "practical", S(L, [("blobs", BL, 110, ("Repair", "Prevent", "One trade", "Whole home"), "beside")], ("Readable at any size", ""))))
    P("Key Points", PA, "Big numbers", "should the key numbers show as a swipe carousel of big-number tiles or as one sentence with the numbers in bold?",
      ("tiles", "Big-Number Tile Carousel", "One number per tile, swipe for the next.", "playful", S(L, [("h", "By The Numbers", 13), ("carousel", [("X homes", "members (sample)", TERRA), ("X%", "kept after a year (sample)", JUNGLE), ("X visits", "per home a year", LAGOON)], 120, 70, True, False, 0)], ("Each number gets a moment", ""))),
      ("sentence", "One Bold Sentence", "X homes, X% kept a year, X visits each.", "calm", S(L, slide("By The Numbers", t(24, 50, "X homes, X% kept after a", 11, INK, "khand") + t(24, 66, "year, X visits each.", 11, INK, "khand") + t(24, 112, "SAMPLE", 6.5, "#8a6510", "hind", 700)), ("Reads like a story", ""))))
    P("Pitch App", PA, "Sources", "should each chart carry a tiny source line under it or should every source sit on one Sources screen at the end?",
      ("under", "Source Under Each Chart", "One small grey line under every chart.", "practical", S(L, slide("Market", bars_body(False) + t(216, 104, "Source: named in the forecast app", 6.8, MUTE, anchor="end")), ("Honest on the spot", ""))),
      ("end", "One Sources Screen", "All sources listed after the last slide.", "calm", S(L, [("h", "Sources", 13), ("table", [("Market size", "Source A"), ("Repair costs", "Source B"), ("Churn", "Our data")])], ("Slides stay clean", ""))))
    P("Pitch App", PA, "Mini forecast", "should the financials slide hold a small live forecast with one slider or a still chart with a link to the forecast app?",
      ("live", "Small Live Forecast", "Drag churn and watch the line move.", "playful", S(L, slide("Financials", f'<polyline points="30,96 70,88 110,74 150,60 200,40" fill="none" stroke="{JUNGLE}" stroke-width="2"/>' + t(24, 112, "SAMPLE", 6.5, "#8a6510", "hind", 700)) + [("bar", .4, LAGOON, "Churn", "X%")], ("Investors try it themselves", ""))),
      ("still", "Still Chart And Link", "One clean chart and an Open Forecast link.", "calm", S(L, slide("Financials", f'<polyline points="30,96 70,88 110,74 150,60 200,40" fill="none" stroke="{JUNGLE}" stroke-width="2"/>' + t(24, 112, "SAMPLE", 6.5, "#8a6510", "hind", 700)) + [("btn", "Open Forecast", "link", LAGOON)], ("Pitch stays simple", ""))))
    P("Pitch App", PA, "Why now", "should the why-now slide show a short timeline of what changed or three plain reasons?",
      ("timeline", "Short Timeline", "Three dated moments that opened the door.", "practical", S(L, [("h", "Why Now", 13), ("timeline", [("Repair costs rising", "Sample point"), ("Phones in every pocket", "Sample point"), ("Homes getting older", "Sample point")])], ("Shows change over time", ""))),
      ("three", "Three Plain Reasons", "Three short cards, side by side.", "calm", S(L, [("h", "Why Now", 13), ("tiles", [("Costs rising", "clock"), ("Phones", "phone"), ("Older homes", "home")], 3, 60)], ("Quick to take in", ""))))
    P("Pitch App", PA, "Investor ask button", "should the last screen end with a Book A Call button or with Max's email and phone written out?",
      ("call", "Book A Call Button", "One button that opens a calendar.", "practical", S(L, slide("Vision", photo(24, 26, 192, 60, LAGOON, "sun")) + [("btn", "Book A Call", "fill", TERRA)], ("One clear next step", ""))),
      ("contact", "Email And Phone Written Out", "Plain contact lines under the vision.", "calm", S(L, slide("Vision", photo(24, 26, 192, 60, LAGOON, "sun")) + [("p", "Email and phone written here", 46, MUTE, True)], ("Nothing to click", ""))))
    return pairs
def fc(extra=(), title="Forecast"):
    return [("h", title, 14), ("line", [.1, .18, .3, .45, .62, .8], JUNGLE, 56), ("sample",)] + list(extra)
def T_P3():
    pairs, P = make("md18pf_", "UpKeep"); L = "UpKeep Forecast App · Phone"
    P("Forecast App", FC, "Charts on a phone", "should the revenue, members and cash charts sit in a swipe carousel or one chart with tabs?",
      ("carousel", "Chart Carousel", "Swipe from revenue to members to cash.", "playful", S(L, [("h", "Forecast", 14), ("carousel", [("Revenue", "sample", JUNGLE), ("Members", "sample", LAGOON), ("Cash", "sample", TERRA)], 150, 90, True, False, 0), ("sample",)], ("One chart per card", ""))),
      ("tabs", "One Chart With Tabs", "Revenue, Members, Cash tabs over one chart.", "calm", S(L, [("tabs", ["Revenue", "Members", "Cash"], "line")] + fc(), ("Chart stays put", ""))))
    P("Forecast App", FC, "Undo changes", "after editing assumption chips should there be one Reset To Base button or an undo on each chip?",
      ("reset", "One Reset To Base", "Puts every chip back at once.", "calm", S(L, [("tags", ["Price $XX", "Churn X%", "Visits X"]), ("btn", "Reset To Base", "line", INK)] + fc(), ("One clear way back", ""))),
      ("each", "Undo On Each Chip", "A small undo mark beside each changed chip.", "practical", S(L, [("tags", ["Price $XX  \u21ba", "Churn X%  \u21ba", "Visits X"])] + fc(), ("Undo just one change", ""))))
    P("Forecast App", FC, "Saved scenarios", "should Max be able to save named scenarios in a swipe row or keep only base, best and worst?",
      ("saved", "Saved Scenarios Row", "Named scenarios as cards you swipe.", "playful", S(L, [("carousel", [("Base", "", INK), ("Two vans", "saved", LAGOON), ("Slower start", "saved", TERRA)], 80, 34, False)] + fc(), ("Try ideas, keep them", ""))),
      ("three", "Base, Best And Worst Only", "Three fixed scenarios.", "calm", S(L, [("tabs", ["Base", "Best", "Worst"], "pill")] + fc(), ("Simple and fixed", ""))))
    P("Forecast App", FC, "Money format", "should money read rounded like $X.XM or in full like $X,XXX,XXX?",
      ("round", "Rounded, $X.XM", "Short numbers that read at a glance.", "calm", S(L, [("stats", [("$X.XM", "revenue"), ("$XXK", "cash"), ("XXX", "members")])] + fc(), ("Easy to say out loud", ""))),
      ("full", "In Full", "Every dollar shown.", "practical", S(L, [("stats", [("$X,XXX,XXX", "revenue"), ("$XXX,XXX", "cash")])] + fc(), ("Exact", ""))))
    P("Forecast App", FC, "Time steps", "should the chart step by quarter or by month?",
      ("q", "By Quarter", "Twenty points over five years.", "calm", S(L, [("bars", [.1, .2, .3, .4, .55, .7, .85], JUNGLE, ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3"])], ("Smooth and simple", ""))),
      ("m", "By Month", "Sixty points over five years.", "practical", S(L, [("bars", [.1, .12, .15, .2, .22, .28, .3, .35, .4, .44, .5, .55], JUNGLE, list("JFMAMJJASOND"))], ("More detail", ""))))
    P("Forecast App", FC, "Members chart", "should the members chart show plans as stacked bars or one line per plan?",
      ("stack", "Stacked Bars By Plan", "Essentials, Plus and Complete stacked.", "practical", S(L, [("h", "Members", 14), ("raw", "".join(rect(24 + i * 40, 96 - 8 * (i + 1), 28, 8 * (i + 1), JUNGLE, "none") + rect(24 + i * 40, 96 - 12.8 * (i + 1), 28, 4.8 * (i + 1), LAGOON, "none") + rect(24 + i * 40, 96 - 16 * (i + 1), 28, 3.2 * (i + 1), TERRA, "none") for i in range(5)) + t(14, 108, "Essentials", 7, JUNGLE, "hind", 600) + t(80, 108, "Plus", 7, LAGOON, "hind", 600) + t(120, 108, "Complete", 7, TERRA, "hind", 600), 114), ("sample",)], ("Total and mix in one", ""))),
      ("lines", "One Line Per Plan", "Matches the revenue chart you picked.", "calm", S(L, [("h", "Members", 14), ("line", [.1, .2, .35, .5, .7], JUNGLE, 50), ("line", [.05, .1, .2, .3, .4], LAGOON, 50), ("sample",)], ("Same look as revenue", ""))))
    P("Forecast App", FC, "Cash runway", "should cash runway show as a half-circle gauge or a months-left bar?",
      ("gauge", "Half-Circle Gauge", "A needle points to months of cash left.", "playful", S(L, [("h", "Cash Runway", 14), ("gauge", .6, "X months (sample)", TERRA)], ("Reads like a fuel gauge", ""))),
      ("bar", "Months-Left Bar", "A bar filled to months of cash left.", "calm", S(L, [("h", "Cash Runway", 14), ("bar", .6, TERRA, "Months left", "X (sample)")], ("Plain and exact", ""))))
    P("Forecast App", FC, "What matters most", "should a chart rank which assumptions move the result most or should a plain ranked list say it?",
      ("tornado", "Ranked Bar Chart", "Longest bar = the assumption that matters most.", "practical", S(L, [("h", "What Moves The Result", 13), ("raw", "".join(rect(120 - w / 2, i * 18, w, 12, ACC[i] + "AA", "none", 2) + t(14, i * 18 + 9, n, 7.5, INK) for i, (n, w) in enumerate((("Churn", 150), ("Price", 110), ("Visits", 70), ("Van cost", 40)))), 76), ("sample",)], ("See the big levers", ""))),
      ("list", "Plain Ranked List", "1 Churn, 2 Price, 3 Visits per home.", "calm", S(L, [("h", "What Moves The Result", 13), ("cards", [("Churn", ""), ("Price", ""), ("Visits per home", "")], None, "num")], ("Simple words", ""))))
    P("Forecast App", FC, "Printed page shape", "should the one-page summary print in portrait or landscape?",
      ("port", "Portrait", "Chart on top, numbers under it, tall page.", "calm", S(L, [("raw", rect(70, 0, 100, 140, "#FFFFFF", "#D6D0C6", 2) + f'<polyline points="80,50 100,44 120,36 140,26 160,16" fill="none" stroke="{JUNGLE}" stroke-width="2"/>' + "".join(rect(80, 70 + i * 14, 80, 8, SOFT) for i in range(4)), 148)], ("Fits a folder", ""))),
      ("land", "Landscape", "Chart and numbers side by side, wide page.", "practical", S(L, [("raw", rect(30, 10, 180, 120, "#FFFFFF", "#D6D0C6", 2) + f'<polyline points="40,100 70,90 100,70 130,50 140,40" fill="none" stroke="{JUNGLE}" stroke-width="2"/>' + "".join(rect(150, 30 + i * 16, 50, 8, SOFT) for i in range(4)), 140)], ("Matches the desktop view", ""))))
    P("Forecast App", FC, "Sample data banner", "while the numbers are samples should a banner run across the top or a light SAMPLE watermark sit behind the chart?",
      ("banner", "Banner Across The Top", "Sample data: not real numbers.", "practical", S(L, [("banner", "Sample data, not real numbers", SAFFRON, "clock"), ("line", [.1, .18, .3, .45, .62, .8], JUNGLE, 70)], ("Impossible to miss", ""))),
      ("mark", "Light Watermark", "SAMPLE written faintly behind the chart.", "calm", S(L, [("raw", rect(14, 0, 212, 80, SOFT, "none", 6) + t(120, 54, "SAMPLE", 34, "#E3D6BC", "khand", anchor="middle") + '<polyline points="20,70 60,64 100,54 140,40 180,26 220,12" fill="none" stroke="#0B6E4F" stroke-width="2"/>', 88)], ("Chart stays clear", ""))))
    return pairs
