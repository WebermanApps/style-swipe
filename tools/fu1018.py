"""Follow-up decks Oct 18 2026 evening (Max 16:50 ICT): one fresh deck per finished deck, one level deeper, built on Max's picks and
notes; settled picks not re-asked; skipped picks reworded and asked again. Pitch decks: phone-only screens, founder never named.
Light only, Khand/Hind, sample data only. Nothing for the home page, welcome video, Command Center design, Ethan or UpKeep Security."""
from md1018_kit import *
from md1018_light import person, fig
L = "UpKeep Investor Pitch · Phone"; PA = "UpKeep Investor Pitch App"
FP = "Smart Upkeep Sign Up · Plan And Pay"; FI = "Smart Upkeep Sign Up · Your Home"
CU = "UpKeep Crew Uniform"; MA = "UpKeep Member App"; FA = "UpKeep Forecast App"
CH, KH = "#3F3F46", "#B9A27E"
def o(k, label, desc, feel, scr, n1, n2=""): return (k, label, desc, feel, S(scr[0], scr[1], (n1, n2)))
def top(n, title): return ("raw", t(14, 10, title.upper(), 7.5, MUTE, "hind", 700, extra='letter-spacing="1"') + t(226, 10, f"{n} / 9", 7.5, FAINT, "hind", 600, "end"), 18)
def phones(labels, sel=None, h=120):
    return ("raw", "".join(rect(14 + i * 72, 0, 64, h, "#FFFFFF", TERRA if i == sel else LINE, 8, 1.4 if i == sel else 1) + rect(14 + i * 72, 0, 64, 14, ACC[i] + "33", "none", 8) + t(46 + i * 72, h + 14, l, 8.5, INK, "khand", anchor="middle") for i, l in enumerate(labels)), h + 22)
def sheet(title, inner, h=170):
    return ("raw", rect(0, 0, W, 300, "#0A0A0A22") + rect(0, 300 - h - 40, W, h + 40, "#FFFFFF", "none", 14) + rect(104, 300 - h - 32, 32, 4, "#D6D0C6", "none", 2) + t(14, 300 - h - 10, title, 13, INK, "khand") + f'<g transform="translate(0,{300-h})">{inner}</g>', 0)
# ---------------- 1. Valuation follow-up ----------------
def T_VAL():
    pairs, P = make("fu18va_", "UpKeep")
    P("Valuation", PA, "Method footnote wording", "with the single number and one footnote line you picked should the footnote name the methods plainly or say Average of three methods with a tap to see them?",
      o("plain", "Methods Named Plainly", "Revenue multiple, similar companies, future cash.", "practical", (L, [top(8, "Our honest value"), ("word", "$X.XM", 30, INK, "SAMPLE"), ("p", "Based on a revenue multiple, similar companies", 52), ("p", "and future cash, averaged", 52)]), "Nothing hidden"),
      o("tap", "Average, Tap For More", "One short line that opens the three methods.", "calm", (L, [top(8, "Our honest value"), ("word", "$X.XM", 30, INK, "SAMPLE"), ("raw", t(120, 10, "Average of three methods  \u203a", 8, LAGOON, "hind", 600, "middle"), 18)]), "Cleaner slide"))
    P("Valuation", PA, "Estimate line look", "for the estimate-over-time line you picked should each month show as a dot on the line or as one smooth line with only today marked?",
      o("dots", "Dot Per Month", "Every monthly estimate is a dot.", "practical", (L, [top(8, "Our honest value"), ("raw", f'<polyline points="20,90 60,84 100,74 140,60 180,52 220,40" fill="none" stroke="{LAGOON}" stroke-width="2"/>' + "".join(dot(x, y, 3, LAGOON) for x, y in ((20, 90), (60, 84), (100, 74), (140, 60), (180, 52), (220, 40))), 100), ("sample", "SAMPLE LINE")]), "Shows each update"),
      o("smooth", "Smooth Line, Today Marked", "A soft line with one Today dot.", "calm", (L, [top(8, "Our honest value"), ("raw", f'<path d="M20 90 C80 86 140 66 220 40" fill="none" stroke="{LAGOON}" stroke-width="2"/>' + dot(220, 40, 4, TERRA) + t(214, 34, "Today", 7.5, TERRA, "hind", 600, "end"), 100), ("sample", "SAMPLE LINE")]), "Quiet and clear"))
    BL = [("UpKeep", .78, .25, 18, TERRA), ("Handyman apps", .3, .62, 14, LAGOON), ("One-trade pros", .25, .8, 11, SAFFRON), ("Home warranty", .62, .7, 13, JUNGLE)]
    P("Blob Chart", PA, "Blob size key", "with blobs sized by market and names inside should a small size key sit under the chart or should each blob carry its market size in small type?",
      o("key", "Size Key Under Chart", "Small, medium, large circles with sample sizes.", "practical", (L, [top(6, "Where we fit"), ("blobs", BL), ("raw", "".join(f'<circle cx="{40+i*60}" cy="8" r="{3+i*2}" fill="none" stroke="{MUTE}"/>' + t(52 + i * 60, 11, ["$X B", "$XX B", "$XXX B"][i], 7, MUTE) for i in range(3)), 20), ("sample",)]), "Chart stays clean"),
      o("each", "Size On Each Blob", "Each blob shows its own market size.", "focused", (L, [top(6, "Where we fit"), ("blobs", [(n + " $X B", x, y, r, c) for n, x, y, r, c in BL]), ("sample",)]), "No key to read"))
    P("Blob Chart", PA, "Blob colours", "should only UpKeep's blob be terracotta with the others in soft grey or should every blob keep its own colour?",
      o("grey", "UpKeep Terracotta, Rest Grey", "Your eye goes straight to UpKeep.", "focused", (L, [top(6, "Where we fit"), ("blobs", [(n, x, y, r, TERRA if n == "UpKeep" else "#9A948A") for n, x, y, r, c in BL])]), "One clear hero"),
      o("own", "Each Its Own Colour", "Four brand colours, one per group.", "playful", (L, [top(6, "Where we fit"), ("blobs", BL)]), "Lively"))
    P("Key Points", PA, "Big-number tiles motion", "for the big-number tile carousel you picked should the tiles move on their own or wait for a swipe?",
      o("auto", "Move On Their Own", "Each tile shows for a few seconds.", "playful", (L, [top(7, "By the numbers"), ("carousel", [("X homes", "Forecast", TERRA), ("X visits", "per home a year", LAGOON), ("X%", "Forecast", JUNGLE)], 120, 80, True, True, 0)]), "Hands-free"),
      o("swipe", "Wait For A Swipe", "Investors move at their own pace.", "calm", (L, [top(7, "By the numbers"), ("carousel", [("X homes", "Forecast", TERRA), ("X visits", "per home a year", LAGOON), ("X%", "Forecast", JUNGLE)], 120, 80, True, False, 0)]), "In control"))
    P("Pitch App", PA, "Source line tap", "should the tiny source line under each chart open the source when tapped or stay plain text?",
      o("tap", "Tap Opens Source", "Underlined, opens the source page.", "practical", (L, [top(4, "Market"), ("bars", [.3, .45, .6, .8], TERRA), ("raw", t(226, 8, "Source: public data  \u2197", 7, LAGOON, "hind", 600, "end", 'text-decoration="underline"'), 14)]), "Easy to check"),
      o("plain", "Plain Text", "A grey line, nothing to tap.", "calm", (L, [top(4, "Market"), ("bars", [.3, .45, .6, .8], TERRA), ("raw", t(226, 8, "Source: public data", 7, MUTE, "hind", 400, "end"), 14)]), "No detours"))
    P("Pitch App", PA, "Mini forecast slider", "for the small live forecast should the one slider move churn or move price per month?",
      o("churn", "Slider Moves Churn", "Drag how many members leave each year.", "practical", (L, [top(8, "Financials"), ("line", [.1, .25, .4, .55, .75]), ("bar", .3, LAGOON, "Churn (Forecast)", "X%"), ("sample", "FORECAST, SAMPLE")]), "The risk investors ask about"),
      o("price", "Slider Moves Price", "Drag the monthly price from $99 up.", "playful", (L, [top(8, "Financials"), ("line", [.1, .25, .4, .55, .75]), ("bar", .2, TERRA, "Price per month", "$99+"), ("sample", "FORECAST, SAMPLE")]), "Shows pricing power"))
    P("Pitch App", PA, "Why now reasons", "for the three plain why-now reasons should each card carry a small icon or a big number 1 2 3?",
      o("icon", "Small Icons", "A line icon on each reason card.", "calm", (L, [top(3, "Why now"), ("tiles", [("Costs rising", "clock"), ("Phones", "phone"), ("Older homes", "home")], 3, 60)]), "Friendly"),
      o("num", "Big Numbers", "A large 1, 2, 3 on each card.", "focused", (L, [top(3, "Why now"), ("cards", [("Repair costs keep rising", ""), ("Everyone books by phone", ""), ("Homes are getting older", "")], [TERRA, LAGOON, JUNGLE], "num", "line", 40)]), "Easy to follow"))
    P("Pitch Ending", PA, "Final screen", "following your note that the pitch should end with a link to the app and the investor's temp password should the link be one big button or a link card with Copy?",
      o("btn", "One Big Open App Button", "A terracotta button opens the app.", "focused", (L, [top(9, "See it yourself"), ("gap", 40), ("word", "Try the app", 22), ("btn", "Open the app", "pill", TERRA), ("note", "Your temp password", "shown below the button", LAGOON)]), "One clear next step"),
      o("card", "Link Card With Copy", "The app link in a card with a Copy button.", "practical", (L, [top(9, "See it yourself"), ("gap", 40), ("word", "Try the app", 22), ("card", "app link", "Tap to open", LAGOON), ("btn", "Copy link", "line", TERRA)]), "Easy to save"))
    P("Pitch Ending", PA, "Temp password spot", "on the final screen should the investor's temp password show in a box with a Copy button or stay hidden until they tap Show password?",
      o("box", "Shown With Copy", "Password in a dashed box, Copy beside it.", "practical", (L, [top(9, "See it yourself"), ("gap", 40), ("btn", "Open the app", "pill", TERRA), ("raw", rect(14, 0, 212, 30, CREAM, "#BDB6AA", 6, 1, 'stroke-dasharray="4 3"') + t(24, 19, "Temp password:  \u2022\u2022\u2022\u2022 sample", 8.5, INK, "hind", 600) + t(216, 19, "Copy", 8, TERRA, "hind", 700, "end"), 38)]), "Ready to paste"),
      o("hide", "Tap To Show", "A Show password link reveals it.", "calm", (L, [top(9, "See it yourself"), ("gap", 40), ("btn", "Open the app", "pill", TERRA), ("btn", "Show password", "link", LAGOON)]), "Private on a shared screen"))
    return pairs
# ---------------- 2. Subscribe and pay follow-up ----------------
def T_PAY2():
    pairs, P = make("fu18sp_", "UpKeep")
    PL = [("cards", [("Starter", "From $99/mo", "$99"), ("Plus", "More visits", "$X"), ("Whole home", "Every system", "$X")], [JUNGLE, LAGOON, TERRA], "dot", "line", 36)]
    P("Plan Choice", FP, "Compare button", "following your note asking for a compare button should it sit as a small Compare plans link above the plan cards or as a full-width button under them?",
      o("link", "Link Above Cards", "A small Compare plans link at the top right.", "calm", (FP, [("raw", t(14, 14, "Pick your plan", 14, INK, "khand") + t(226, 14, "Compare plans", 8, LAGOON, "hind", 600, "end", 'text-decoration="underline"'), 24)] + PL), "Out of the way"),
      o("btn", "Button Under Cards", "A full-width Compare plans button.", "practical", (FP, [("h", "Pick your plan", 14)] + PL + [("btn", "Compare plans", "line", LAGOON)]), "Hard to miss"))
    CMP = "".join(t(20, 20 + i * 24, r, 8, INK, "hind", 500) + "".join(t(140 + j * 36, 20 + i * 24, "\u221A" if (j >= k) else "\u2013", 9, JUNGLE if j >= k else FAINT, "hind", 700, "middle") for j in range(3)) for i, (r, k) in enumerate((("Seasonal visits", 0), ("Photo report", 0), ("Gutters", 1), ("Every system", 2))))
    P("Plan Choice", FP, "Compare pop-up", "when Compare plans is tapped should the comparison open as a full new screen or as a sheet sliding up from the bottom?",
      o("full", "Full New Screen", "A whole screen with a Back arrow.", "focused", (FP, [("raw", t(14, 10, "\u2039 Back", 8, TERRA, "hind", 600) + t(14, 32, "Compare plans", 14, INK, "khand") + "".join(t(140 + j * 36, 52, n, 7.5, MUTE, "hind", 700, "middle") for j, n in enumerate(("Starter", "Plus", "Whole"))) + f'<g transform="translate(0,56)">{CMP}</g>', 160)]), "Room to read"),
      o("sheet", "Bottom Sheet", "Slides up over the plans, swipe down to close.", "playful", (FP, [("h", "Pick your plan", 14)] + PL + [sheet("Compare plans", CMP, 110)]), "Plans stay behind it"))
    P("Plan Choice", FP, "Compare layout", "inside the compare screen should plans sit as three columns of ticks or as one plan card per swipe with its full list?",
      o("cols", "Three Tick Columns", "Rows of features, a tick per plan.", "practical", (FP, [("h", "Compare plans", 14), ("raw", CMP, 110)]), "Side by side"),
      o("swipe", "One Plan Per Swipe", "Swipe plan cards, each with its list.", "playful", (FP, [("h", "Compare plans", 14), ("carousel", [("Starter", "$99/mo", JUNGLE), ("Plus", "$X/mo", LAGOON), ("Whole home", "$X/mo", TERRA)], 150, 70, True), ("checks", ["Seasonal visits", "Photo report", "Filter changes"], JUNGLE, 3)]), "Big and readable"))
    P("Extras", FP, "Photo tile shape", "for the Extras photo tiles you picked should tiles be square in a two-by-two grid or wide cards in a swipe row?",
      o("sq", "Square Grid", "Two by two, photo on top, name and price.", "calm", (FP, [("h", "Add Extras", 14), ("raw", "".join(photo(14 + (i % 2) * 110, (i // 2) * 100, 102, 66, ACC[i], ["leaf", "house", "sun", "room"][i]) + t(18 + (i % 2) * 110, (i // 2) * 100 + 80, ["Lawn care", "Gutters", "Windows", "Dryer vent"][i], 9, INK, "khand") + t(18 + (i % 2) * 110, (i // 2) * 100 + 92, "+$X", 7.5, MUTE) for i in range(4)), 200)]), "See all at once"),
      o("wide", "Wide Swipe Cards", "Big photo cards you swipe through.", "playful", (FP, [("h", "Add Extras", 14), ("carousel", [("Lawn care", "+$X/mo", JUNGLE), ("Gutters", "+$X", LAGOON), ("Windows", "+$X", TERRA)], 170, 130, True, False, 0, True, None, False, "photo")]), "Photos shine"))
    P("Extras", FP, "Tile added state", "when an Extra tile is added should it show a jungle green check badge or a terracotta border with Added?",
      o("check", "Green Check Badge", "A round check in the corner.", "calm", (FP, [("h", "Add Extras", 14), ("raw", photo(14, 0, 102, 80, JUNGLE, "leaf") + f'<circle cx="104" cy="12" r="9" fill="{JUNGLE}"/>' + t(104, 15.5, "\u221A", 10, "#FFFFFF", "hind", 700, "middle") + photo(124, 0, 102, 80, LAGOON, "house"), 90)]), "Quiet signal"),
      o("border", "Terracotta Border, Added", "A thick border and an Added tag.", "focused", (FP, [("h", "Add Extras", 14), ("raw", photo(14, 0, 102, 80, JUNGLE, "leaf") + rect(14, 0, 102, 80, "none", TERRA, 6, 2.5) + chip(20, 60, "Added", TERRA, True)[0] + photo(124, 0, 102, 80, LAGOON, "house"), 90)]), "Very clear"))
    BAR = lambda s: ("raw", rect(0, 0, W, 36, CREAM) + ln(0, 0, W, LINE) + s, 36)
    P("Extras", FP, "Sticky total content", "for the sticky total bar you picked should it show only the monthly total or the total plus how many Extras are added?",
      o("total", "Total Only", "Total  $X/mo  and a Review button.", "calm", (FP, [("h", "Add Extras", 14), ("gap", 150), BAR(t(14, 23, "Total  $X/mo", 12, INK, "khand") + t(226, 23, "Review", 9, TERRA, "hind", 700, "end"))]), "Simple", "SAMPLE total"),
      o("count", "Total Plus Extras Count", "Starter + 2 Extras, $X/mo.", "practical", (FP, [("h", "Add Extras", 14), ("gap", 150), BAR(t(14, 16, "Starter + 2 Extras", 8, MUTE, "hind", 600) + t(14, 29, "$X/mo", 12, INK, "khand") + t(226, 23, "Review", 9, TERRA, "hind", 700, "end"))]), "Know what's in it", "SAMPLE total"))
    P("Extras", FP, "Sticky total tap", "should tapping the sticky total bar open a quick price breakdown or do nothing until Review?",
      o("open", "Tap Opens Breakdown", "A small sheet lists plan and each Extra.", "practical", (FP, [("h", "Add Extras", 14), sheet("Your total", t(20, 20, "Starter plan", 8.5, INK) + t(220, 20, "$99/mo", 8.5, INK, "hind", 600, "end") + t(20, 44, "Lawn care", 8.5, INK) + t(220, 44, "+$X/mo", 8.5, INK, "hind", 600, "end") + t(20, 72, "Total", 10, INK, "khand") + t(220, 72, "$X/mo", 10, TERRA, "khand", anchor="end"), 100)]), "Answers before they ask"),
      o("none", "Nothing Until Review", "The bar is just a total and a button.", "calm", (FP, [("h", "Add Extras", 14), ("gap", 150), BAR(t(14, 23, "Total  $X/mo", 12, INK, "khand") + t(226, 23, "Review", 9, TERRA, "hind", 700, "end"))]), "Fewer surprises"))
    WK = lambda sel, grey=(): ("raw", "".join(rect(14 + i * 54, 0, 48, 40, TERRA if i == sel else ("#EEEAE4" if i in grey else "#FFFFFF"), TERRA if i == sel else LINE, 8) + t(38 + i * 54, 17, f"Jan {[4, 11, 18, 25][i]}", 8, "#FFFFFF" if i == sel else (FAINT if i in grey else INK), "hind", 600, "middle") + t(38 + i * 54, 30, "Full" if i in grey else "week", 7, "#FFFFFF" if i == sel else MUTE, anchor="middle") for i in range(4)), 48)
    P("First Visit", FP, "Week picker style", "for picking the first-visit week should weeks show as a row of week chips or as a small January calendar?",
      o("chips", "Row Of Week Chips", "Jan 4, Jan 11, Jan 18, Jan 25 as chips.", "practical", (FP, [("h", "Preferred first visit", 14), WK(1), ("p", "Visits start Jan 1 2027")]), "One tap"),
      o("cal", "Small Calendar", "A month grid, tap a week row.", "calm", (FP, [("h", "Preferred first visit", 14), ("cal", (11, 12, 13, 14, 15), TERRA), ("p", "Visits start Jan 1 2027")]), "Familiar"))
    P("First Visit", FP, "Full weeks", "if a week fills up should it show greyed with Full or be hidden from the picker?",
      o("grey", "Greyed With Full", "Full weeks stay visible but can't be picked.", "practical", (FP, [("h", "Preferred first visit", 14), WK(1, (0,))]), "Honest about demand"),
      o("hide", "Hidden", "Only open weeks are shown.", "calm", (FP, [("h", "Preferred first visit", 14), ("raw", "".join(rect(14 + i * 72, 0, 64, 40, TERRA if i == 0 else "#FFFFFF", TERRA if i == 0 else LINE, 8) + t(46 + i * 72, 24, f"Jan {[11, 18, 25][i]}", 8.5, "#FFFFFF" if i == 0 else INK, "hind", 600, "middle") for i in range(3)), 48)]), "Clean"))
    P("Confirmation", FP, "Receipt download", "for the on-screen receipt you picked should Download save a PDF or open the phone's share sheet?",
      o("pdf", "Save A PDF", "Download receipt saves a PDF file.", "practical", (FP, [("h", "Receipt", 14), ("table", [("Starter plan", "$99/mo"), ("Extras", "$X/mo"), ("Total", "$X/mo")]), ("btn", "Download PDF", "line", TERRA)]), "A proper file", "SAMPLE amounts"),
      o("share", "Share Sheet", "Opens share: save, text or email it.", "playful", (FP, [("h", "Receipt", 14), ("table", [("Starter plan", "$99/mo"), ("Extras", "$X/mo"), ("Total", "$X/mo")]), sheet("Share receipt", "".join(rect(20 + i * 52, 10, 40, 40, ACC[i] + "22", "none", 10) + t(40 + i * 52, 64, n, 7.5, INK, anchor="middle") for i, n in enumerate(("Save", "Text", "Email", "More"))), 80)]), "Phone-native", "SAMPLE amounts"))
    return pairs
# ---------------- 3. Crew uniform follow-up ----------------
BEANIE = f'<path d="M60 110 q0 -80 60 -80 q60 0 60 80 z" fill="{CH}"/>' + rect(60, 96, 120, 18, "#52525B", "none", 4)
def GLOVES(cuff=6, mark=False, h=80):
    s = ""
    for x in (60, 130):
        s += rect(x, 20, 50, h, CH, "none", 14) + rect(x, 20 + h - cuff + (6 if cuff <= 6 else 0) - (0 if cuff <= 6 else -4), 50, cuff, TERRA, "none", 2)
        if mark: s += f'<path d="M{x+18} 58 v-8 l7 -6 l7 6 v8 z" fill="{TERRA}"/>'
    return s
def BOOT(top=40, tab=False):
    return rect(80, top, 50, 110 - top, "#1F1F1F", "none", 8) + rect(70, 96, 90, 20, "#1F1F1F", "none", 8) + (rect(124, top - 10, 10, 18, TERRA, "none", 2) if tab else "")
def T_CREW2():
    pairs, P = make("fu18cu_", "UpKeep")
    P("Crew Uniform", CU, "Logo spot on polos", "on the terracotta and lagoon polos should the logo sit small on the left chest or small on the chest plus a larger mark on the back?",
      o("chest", "Left Chest Only", "One small mark on the chest.", "calm", (CU, [fig(person(80, 14, TERRA, CH), person(160, 14, LAGOON, CH))]), "Clean"),
      o("back", "Chest Plus Back", "Small chest mark, big mark across the back.", "practical", (CU, [fig(person(80, 14, TERRA, CH), f'<path d="M140 32 q20 -8 40 0 v42 h-40 z" fill="{LAGOON}"/>' + rect(146, 42, 28, 14, "#FFFFFF", "none", 3) + t(160, 52, "UPKEEP", 6, LAGOON, "khand", anchor="middle") + t(160, 100, "Back", 8, MUTE, anchor="middle"))]), "Seen from the street"))
    P("Crew Uniform", CU, "Button-up colour", "for the button-up estimate shirt you picked should it be charcoal or lagoon blue?",
      o("char", "Charcoal", "Charcoal with a small terracotta mark.", "calm", (CU, [fig(person(120, 14, CH, KH, extra=f'<line x1="120" y1="34" x2="120" y2="74" stroke="#FFFFFF"/>' + dot(111, 42, 3, TERRA)))]), "Smart and neutral"),
      o("lag", "Lagoon Blue", "Lagoon with a small white mark.", "playful", (CU, [fig(person(120, 14, LAGOON, KH, extra=f'<line x1="120" y1="34" x2="120" y2="74" stroke="#FFFFFF"/>'))]), "Ties to the tech app"))
    P("Crew Uniform", CU, "Button-up logo", "on the button-up should the mark be embroidered straight on the shirt or on a small sewn-on patch?",
      o("emb", "Embroidered", "Thread mark straight on the fabric.", "calm", (CU, [("raw", rect(60, 10, 120, 110, CH, "none", 10) + t(90, 44, "UPKEEP", 9, TERRA, "khand", anchor="middle"), 128)]), "Polished"),
      o("patch", "Sewn-On Patch", "A small rectangle patch with the mark.", "practical", (CU, [("raw", rect(60, 10, 120, 110, CH, "none", 10) + rect(70, 32, 44, 18, CREAM, TERRA, 3) + t(92, 45, "UPKEEP", 8, TERRA, "khand", anchor="middle"), 128)]), "Workwear feel"))
    P("Crew Uniform", CU, "Beanie mark", "on the charcoal beanie you picked should the mark be a small woven wordmark tag or a small embroidered house icon?",
      o("word", "Woven Wordmark Tag", "A little cream tag with UPKEEP.", "practical", (CU, [("raw", BEANIE + rect(100, 98, 40, 14, CREAM, "none", 2) + t(120, 108, "UPKEEP", 7, TERRA, "khand", anchor="middle"), 122)]), "Reads as the brand"),
      o("icon", "Embroidered House Icon", "A small terracotta house shape.", "calm", (CU, [("raw", BEANIE + f'<path d="M112 110 v-7 l8 -6 l8 6 v7 z" fill="{TERRA}"/>', 122)]), "Subtle"))
    P("Crew Uniform", CU, "Beanie cuff", "should the beanie have a thin terracotta stripe on the cuff or stay all charcoal?",
      o("stripe", "Thin Terracotta Stripe", "One thin stripe around the cuff.", "playful", (CU, [("raw", BEANIE + rect(60, 103, 120, 3, TERRA), 122)]), "On brand"),
      o("plain", "All Charcoal", "Plain cuff, mark only.", "calm", (CU, [("raw", BEANIE, 122)]), "Understated"))
    P("Crew Uniform", CU, "Boot height", "for the waterproof boot you picked should it be an ankle-height boot or a mid-calf boot?",
      o("ankle", "Ankle Height", "Light, easy on and off.", "practical", (CU, [("raw", BOOT(60), 124)]), "Quick to wear"),
      o("mid", "Mid-Calf", "Higher for wet yards and gutters.", "focused", (CU, [("raw", BOOT(20), 124)]), "Drier legs"))
    P("Crew Uniform", CU, "Boot accent", "should the boot be plain black or black with a small terracotta pull tab?",
      o("plain", "Plain Black", "No colour, easy to replace.", "calm", (CU, [("raw", BOOT(40), 124)]), "Simple"),
      o("tab", "Terracotta Pull Tab", "A small tab at the back of the boot.", "playful", (CU, [("raw", BOOT(40, True), 124)]), "Small brand touch"))
    P("Crew Uniform", CU, "Glove cuff width", "for the charcoal gloves with a terracotta cuff should the cuff be a thin band or a wide band?",
      o("thin", "Thin Band", "A narrow terracotta line at the wrist.", "calm", (CU, [("raw", GLOVES(6), 116)]), "Subtle"),
      o("wide", "Wide Band", "A deep terracotta cuff.", "playful", (CU, [("raw", GLOVES(24), 116)]), "Bold"))
    P("Crew Uniform", CU, "Glove mark", "should the gloves carry a small mark on the back of the hand or no mark?",
      o("mark", "Small Mark On Back", "A tiny terracotta house on each glove.", "playful", (CU, [("raw", GLOVES(6, True), 116)]), "Brand in every photo"),
      o("none", "No Mark", "Cuff colour only.", "calm", (CU, [("raw", GLOVES(6), 116)]), "Cheaper to replace"))
    P("Crew Uniform", CU, "Polo colour choice", "with terracotta and lagoon polos both allowed should each tech pick their colour freely or should the colour follow the day of the week?",
      o("free", "Tech Picks Freely", "Any day, either colour.", "calm", (CU, [fig(person(80, 14, TERRA, CH), person(160, 14, LAGOON, CH))]), "Easy"),
      o("day", "Colour By Day", "Terracotta Mon to Wed, lagoon Thu to Sat.", "practical", (CU, [fig(person(80, 14, TERRA, CH), person(160, 14, LAGOON, CH)), ("pills", ["Mon-Wed terracotta", "Thu-Sat lagoon"], [TERRA, LAGOON])]), "Crew matches on site"))
    return pairs
# ---------------- 4. Org chart / ask follow-up ----------------
def T_ORG2():
    pairs, P = make("fu18og_", "UpKeep")
    ASKC = lambda extra="", h=96: ("raw", rect(14, 0, 212, h, "#FFFFFF", LINE, 8) + t(24, 26, "$200K for 10%", 15, INK, "khand") + t(24, 40, "at a $2M valuation", 8, MUTE) + ln(50, 24, 216) + t(24, 70, "$100K line of credit", 12, INK, "khand") + t(24, 82, "separate, at 10%", 8, MUTE) + extra, h + 8)
    P("How We Run It", PA, "Open the real apps", "following your note that investors should get into the apps from the pitch should the apps show as big tappable tiles or as phone snapshots with an Open button under each?",
      o("tiles", "Big Tappable Tiles", "Member app, tech app, Command Center tiles.", "playful", (L, [top(6, "How we run it"), ("tiles", [("Member app", "phone"), ("Tech app", "check"), ("Command Center", "star"), ("Forecast", "cal")], 2, 70, "solid")]), "One tap into each"),
      o("phones", "Snapshots With Open Buttons", "Three snapshots, Open under each.", "practical", (L, [top(6, "How we run it"), phones(["Member", "Tech", "Command"], 0), ("raw", "".join(rect(18 + i * 72, 0, 56, 18, TERRA, "none", 9) + t(46 + i * 72, 12, "OPEN", 7, "#FFFFFF", "hind", 700, "middle") for i in range(3)), 24)]), "See it, then open it"))
    P("How We Run It", PA, "App opens where", "when an investor opens one of the apps should it open inside the pitch with a Back to pitch bar or in a new browser tab?",
      o("inside", "Inside The Pitch", "A slim Back to pitch bar on top.", "focused", (L, [("raw", rect(0, 0, W, 24, CREAM) + t(14, 16, "\u2039 Back to pitch", 8.5, TERRA, "hind", 700) + t(226, 16, "Tech app, demo", 7.5, MUTE, anchor="end"), 30), ("photos", 1, 150, ["room"])]), "Never lost"),
      o("tab", "New Browser Tab", "The app opens on its own, pitch stays open.", "calm", (L, [top(6, "How we run it"), phones(["Member", "Tech", "Command"]), ("p", "Opens in a new tab \u2197")]), "Full app, full screen"))
    P("How We Run It", PA, "Demo data notice", "inside the opened apps should a Demo data banner run across the top or a small Demo chip sit in the corner?",
      o("banner", "Demo Data Banner", "Demo data: not real members.", "practical", (L, [("banner", "Demo data, not real members", SAFFRON, "tag"), ("photos", 1, 150, ["room"])]), "Impossible to miss"),
      o("chip", "Small Demo Chip", "A tiny Demo tag in the corner.", "calm", (L, [("raw", chip(186, 0, "Demo", SAFFRON, True)[0], 20), ("photos", 1, 150, ["room"])]), "App looks real"))
    HUB = f'<circle cx="120" cy="70" r="22" fill="{TERRA}1A" stroke="{TERRA}"/>' + t(120, 74, "Founder", 8.5, INK, "khand", anchor="middle") + "".join(f'<line x1="120" y1="70" x2="{x}" y2="{y}" stroke="#D6D0C6"/><circle cx="{x}" cy="{y}" r="18" fill="#FFFFFF" stroke="{c}"/>' + t(x, y + 3, n, 7, INK, "hind", 600, "middle") for x, y, n, c in ((50, 30, "Sales", LAGOON), (190, 30, "Brand", JUNGLE), (40, 110, "Ops", SAFFRON), (200, 110, "Finance", LAGOON), (120, 140, "Research", JUNGLE)))
    P("Org Chart", PA, "Agent org chart", "following your note that an agent org chart fits better should it show the founder at the centre with agents around them or as layers from founder to agents to field techs?",
      o("hub", "Founder At The Centre", "Founder in the middle, agents in a ring.", "playful", (L, [top(6, "How we run it"), ("raw", HUB, 164)]), "A hub of help"),
      o("layers", "Layers Down", "Founder, then AI agents, then field techs.", "practical", (L, [top(6, "How we run it"), ("cards", [("Founder", "Sets direction"), ("AI agents", "Sales, brand, ops, finance, research"), ("Field techs", "Home visits")], [TERRA, LAGOON, JUNGLE], "num", "line", 40)]), "Clear chain"))
    P("Org Chart", PA, "Agent cards", "on the agent org chart should each agent show just a role name or a role name plus one line of what it does?",
      o("name", "Role Name Only", "Sales agent, Brand agent, Ops agent.", "calm", (L, [top(6, "How we run it"), ("pills", ["Sales agent", "Brand agent", "Ops agent"], [LAGOON, JUNGLE, SAFFRON]), ("pills", ["Finance agent", "Research agent"], [TERRA, LAGOON])]), "Tidy"),
      o("line", "Name Plus What It Does", "Ops agent: books visits and routes.", "practical", (L, [top(6, "How we run it"), ("cards", [("Sales agent", "Answers new sign-ups"), ("Brand agent", "Designs every screen"), ("Ops agent", "Books visits and routes")], [LAGOON, JUNGLE, SAFFRON])]), "Investors see the work"))
    P("Org Chart", PA, "Future hires on the chart", "with dashed hiring boxes already picked should the agent org chart show future field techs dashed under the agents or keep hires on a separate small line?",
      o("hires", "Dashed Under The Agents", "Dashed boxes for techs still to hire.", "practical", (L, [top(6, "How we run it"), ("cards", [("Founder", ""), ("AI agents", "")], [TERRA, LAGOON]), ("raw", rect(14, 0, 212, 30, "#FFFFFF", "#BDB6AA", 6, 1, 'stroke-dasharray="4 3"') + t(24, 19, "Field techs", 9, MUTE, "khand") + chip(170, 7, "Hiring", TERRA)[0], 38)]), "One picture"),
      o("line", "Separate Hiring Line", "Next hires: field techs, in small type.", "calm", (L, [top(6, "How we run it"), ("cards", [("Founder", ""), ("AI agents", "")], [TERRA, LAGOON]), ("p", "Next hires: field techs (dashed on full chart)")]), "Chart stays simple"))
    P("The Ask", PA, "Use of funds", "following your note that the slide can say what the money is for should use of funds show as one split bar or as a short list with sample percentages?",
      o("bar", "One Split Bar", "Techs, vans, marketing, runway in one bar.", "focused", (L, [top(8, "The Ask"), ("raw", "".join(rect(14 + sum((50, 60, 50, 52)[:i]), 0, w, 16, c, "none", 0) for i, (w, c) in enumerate(zip((50, 60, 50, 52), (TERRA, LAGOON, JUNGLE, SAFFRON)))), 22), ("pills", ["Techs", "Vans", "Marketing", "Runway"], [TERRA, LAGOON, JUNGLE, SAFFRON]), ("sample", "SAMPLE SPLIT")]), "At a glance"),
      o("list", "Short List", "Four lines with sample percentages.", "practical", (L, [top(8, "The Ask"), ("kv", [("Field techs", "X%"), ("Vans and tools", "X%"), ("Marketing", "X%"), ("Runway", "X%")]), ("sample", "SAMPLE SPLIT")]), "Easy to read"))
    P("The Ask", PA, "Use of funds placement", "should use of funds sit inside the split Ask card or on its own screen right after The Ask?",
      o("in", "Inside The Ask Card", "Terms on top, a small split bar under them.", "practical", (L, [top(8, "The Ask"), ASKC("".join(rect(24 + i * 48, 100, 46, 10, c, "none", 0) for i, c in enumerate((TERRA, LAGOON, JUNGLE, SAFFRON))), 120)]), "One screen"),
      o("own", "Own Screen After", "A Where the money goes screen.", "calm", (L, [top(9, "Where the money goes"), ("kv", [("Field techs", "X%"), ("Vans and tools", "X%"), ("Marketing", "X%"), ("Runway", "X%")]), ("sample", "SAMPLE SPLIT")]), "Ask stays clean"))
    TL = lambda extra: ("raw", rect(14, 20, 212, 8, "#EEEAE4", "none", 4) + dot(40, 24, 5, TERRA) + t(40, 44, "Today", 7.5, TERRA, "hind", 600, "middle") + t(110, 44, "Dec 1", 7.5, INK, anchor="middle") + t(205, 44, "Apr 1", 7.5, INK, anchor="middle") + extra, 56)
    P("Timeline", PA, "Beta shading", "on the bar with the Today marker should the beta stretch be shaded lagoon with a Beta label or drawn as a dashed bracket above the bar?",
      o("shade", "Lagoon Shading", "Beta Jan to Mar shaded on the bar.", "calm", (L, [top(7, "Timeline"), TL(rect(110, 20, 90, 8, LAGOON + "66", "none", 0) + t(155, 12, "Beta", 7.5, LAGOON, "hind", 600, "middle"))]), "Soft"),
      o("bracket", "Dashed Bracket", "A bracket over the beta months.", "practical", (L, [top(7, "Timeline"), TL(f'<path d="M110 14 v-6 h90 v6" fill="none" stroke="{LAGOON}" stroke-dasharray="3 2"/>' + t(155, 4, "Beta, target 50 homes", 7, LAGOON, "hind", 600, "middle"))]), "Room for the label"))
    P("Pitch App", PA, "Swipe hint", "for the swipe-left gesture you picked should the hint arrow show only on the first screen or on every screen?",
      o("first", "First Screen Only", "Learn once, then it disappears.", "calm", (L, [top(1, "Smart Upkeep"), ("gap", 40), ("word", "Smart Upkeep", 26), ("raw", ic("chev", 200, 0, 18, TERRA, 2) + t(194, 13, "Swipe", 7.5, TERRA, "hind", 600, "end"), 22)]), "Clean after that"),
      o("every", "Every Screen", "A small arrow at the edge every time.", "practical", (L, [top(5, "Plans"), ("cards", [("From $99/mo", "Starter plan", "$99")], [JUNGLE], "dot", "line", 40), ("raw", ic("chev", 206, 0, 16, TERRA, 2), 20)]), "Always clear"))
    return pairs
# ---------------- 5. Cover / problem / plans follow-up ----------------
def T_COVER2():
    pairs, P = make("fu18cv_", "UpKeep")
    FC = lambda h: [top(5, h), ("raw", photo(14, 0, 44, 44, TERRA, "person", 22) + t(66, 20, "The founder", 13, INK, "khand") + t(66, 34, "Metro Detroit", 8, MUTE), 52), ("cards", [("Fact one", "Short line"), ("Fact two", "Short line"), ("Fact three", "Short line")], [TERRA, LAGOON, JUNGLE], "num")]
    P("Cover", PA, "Wordmark colour", "on the white cover with the big wordmark should the wordmark be ink black with a terracotta dot or fully terracotta?",
      o("ink", "Ink With Terracotta Dot", "Black wordmark, one terracotta accent.", "calm", (L, [("gap", 60), ("raw", t(120, 30, "Smart Upkeep", 30, INK, "khand", 700, "middle") + dot(196, 27, 4, TERRA), 40), ("p", "Home maintenance on autopilot", 46, MUTE, True), ("p", "Serving metro Detroit", 46, FAINT, True)]), "Crisp"),
      o("terra", "Fully Terracotta", "The whole wordmark in brand terracotta.", "warm", (L, [("gap", 60), ("word", "Smart Upkeep", 30, TERRA), ("p", "Home maintenance on autopilot", 46, MUTE, True), ("p", "Serving metro Detroit", 46, FAINT, True)]), "Warm"))
    P("Cover", PA, "Cover tagline size", "should Home maintenance on autopilot sit large under the wordmark or small with lots of white space?",
      o("large", "Large Tagline", "Tagline almost as big as the name.", "focused", (L, [("gap", 50), ("word", "Smart Upkeep", 26), ("h", "Home maintenance on autopilot", 16, INK, True), ("p", "Serving metro Detroit", 46, FAINT, True)]), "The promise up front"),
      o("small", "Small Tagline", "Quiet line, big white space.", "calm", (L, [("gap", 80), ("word", "Smart Upkeep", 30), ("p", "Home maintenance on autopilot", 46, MUTE, True), ("gap", 30), ("p", "Serving metro Detroit", 46, FAINT, True)]), "Premium feel"))
    P("Problem", PA, "Problem photo caption", "on the one photo problem story should the caption sit on a white band over the photo or as a headline under the photo?",
      o("band", "White Band Over Photo", "The caption sits on the photo.", "warm", (L, [top(2, "Problem"), ("photo", 170, TERRA, "room", "A small leak, left alone")]), "Photo stays big"),
      o("under", "Headline Under Photo", "Photo, then a bold headline.", "focused", (L, [top(2, "Problem"), ("photo", 130, TERRA, "room"), ("h", "A small leak, left alone", 16)]), "Easier to read"))
    P("Problem", PA, "Cost bars labels", "for the two SAMPLE cost bars should the bars carry dollar placeholders or plain words like Small fix and Big repair?",
      o("dollar", "Dollar Placeholders", "$X and $XX on the bars, tagged sample.", "practical", (L, [top(2, "Problem"), ("bars", [.2, .9], TERRA, ["$X fix early", "$XX fix late"], 100), ("sample",)]), "Feels concrete"),
      o("words", "Plain Words", "Small fix vs Big repair, no amounts.", "calm", (L, [top(2, "Problem"), ("bars", [.2, .9], TERRA, ["Small fix", "Big repair"], 100)]), "Nothing to defend"))
    P("How It Works", PA, "How it works with snapshots", "since you picked real app snapshots and left the layout open should each step be one full snapshot you swipe or three small snapshots with step names on one screen?",
      o("swipe", "One Snapshot Per Swipe", "Each step fills the screen with its app.", "playful", (L, [top(3, "How it works"), ("raw", rect(50, 0, 140, 200, "#FFFFFF", LINE, 12) + rect(50, 0, 140, 22, TERRA + "33", "none", 12) + t(120, 15, "1  Sign up", 9, INK, "khand", anchor="middle"), 208), ("cdots", 3, 0)]), "Big and real"),
      o("three", "Three On One Screen", "Small snapshots side by side, names under.", "calm", (L, [top(3, "How it works"), phones(["1 Sign up", "2 We visit", "3 Report"])]), "Whole story at once"))
    P("How It Works", PA, "Snapshot frame", "should the app snapshots sit inside a thin phone outline or show as rounded screens with no frame?",
      o("frame", "Thin Phone Outline", "A slim device outline around each.", "practical", (L, [top(3, "How it works"), ("raw", "".join(rect(18 + i * 72, 0, 60, 120, "#FFFFFF", INK, 10, 2) + rect(38 + i * 72, 4, 20, 4, INK, "none", 2) for i in range(3)), 128)]), "Looks like a phone"),
      o("bare", "Rounded Screens Only", "Just the screens, soft corners.", "calm", (L, [top(3, "How it works"), ("raw", "".join(rect(18 + i * 72, 0, 60, 120, "#FFFFFF", LINE, 8) for i in range(3)), 128)]), "Lighter"))
    P("Plans", PA, "Plan tab style", "for one plan per tab should the tabs be soft pills or plain words with an underline?",
      o("pill", "Soft Pills", "A white pill sits behind the active tab.", "playful", (L, [top(4, "Plans"), ("tabs", ["Starter", "Plus", "Whole"], "pill"), ("word", "$99/mo", 30, JUNGLE, "FROM")]), "Friendly"),
      o("line", "Underline Tabs", "Thin terracotta line under the active tab.", "calm", (L, [top(4, "Plans"), ("tabs", ["Starter", "Plus", "Whole"], "line"), ("word", "$99/mo", 30, JUNGLE, "FROM")]), "Clean"))
    P("Plans", PA, "Extras slide prices", "on the Extras slide should each tile show a SAMPLE price or just the Extra's name?",
      o("price", "Name And SAMPLE Price", "Lawn care +$X/mo, tagged sample.", "practical", (L, [top(5, "Extras"), ("tiles", [("Lawn care +$X", "star"), ("Gutters +$X", "home"), ("Windows +$X", "tag"), ("More soon", "clock")], 2, 64), ("sample",)]), "Shows upsell value"),
      o("name", "Name Only", "Just what's on offer.", "calm", (L, [top(5, "Extras"), ("tiles", [("Lawn care", "star"), ("Gutters", "home"), ("Windows", "tag"), ("More soon", "clock")], 2, 64)]), "Cleaner"))
    P("Founder", PA, "Founder screen heading", "on the founder screen with fact cards and a small photo should the heading say Why this founder or Who's building it?",
      o("why", "Why This Founder", "Heading speaks to fit for the job.", "focused", (L, FC("Why this founder")), "Makes the case"),
      o("who", "Who's Building It", "Heading is plain and friendly.", "warm", (L, FC("Who's building it")), "Human"))
    P("Founder", PA, "Career timeline look", "for the founder's career timeline should it run down the screen as dots on a line or as cards you swipe year by year?",
      o("dots", "Dots On A Line", "Steps stacked down the screen.", "calm", (L, [top(5, "Why this founder"), ("timeline", [("Step one", "Year, placeholder"), ("Step two", "Year, placeholder"), ("Step three", "Year, placeholder"), ("Smart Upkeep", "Now")])]), "All at once"),
      o("swipe", "Swipe Year By Year", "One career card per swipe.", "playful", (L, [top(5, "Why this founder"), ("carousel", [("Step one", "Year", LAGOON), ("Step two", "Year", JUNGLE), ("Smart Upkeep", "Now", TERRA)], 150, 110, True)]), "Story feel"))
    return pairs
# ---------------- 6. Client info follow-up ----------------
DROP = ("raw", rect(14, 0, 212, 90, CREAM, "#BDB6AA", 8, 1, 'stroke-dasharray="4 3"') + t(120, 50, "Tap to add photos", 9, MUTE, "hind", 600, "middle"), 98)
def T_INFO2():
    pairs, P = make("fu18ci_", "UpKeep")
    AGE = ("pills", ["0-5 yrs", "5-10 yrs", "10+ yrs", "Not sure"], [JUNGLE, LAGOON, TERRA, MUTE])
    P("Home Photos", FI, "Price lock message", "since photos are optional but lock in the price should that show as a banner saying Snap photos to lock your price or as a small Price lock badge on the upload box?",
      o("banner", "Lock Your Price Banner", "Snap photos to lock your price.", "focused", (FI, [("banner", "Snap photos to lock your price", JUNGLE, "check"), DROP, ("btn", "Skip for now", "link", MUTE)]), "Clear reason to do it"),
      o("badge", "Price Lock Badge", "A small badge on the upload box.", "calm", (FI, [("h", "Add photos (optional)", 14), ("raw", DROP[1] + chip(150, 8, "Price lock", JUNGLE, True)[0], 98), ("btn", "Skip for now", "link", MUTE)]), "Low pressure"))
    P("Home Photos", FI, "Price change wording", "should the screen explain that without photos the price may change a little after the first visit or leave that to the terms?",
      o("say", "Say It On Screen", "No photos? Price may adjust a little at visit one.", "practical", (FI, [("h", "Add photos (optional)", 14), ("note", "No photos? That's fine.", "Price may adjust a little at the first visit", LAGOON)]), "No surprises later"),
      o("terms", "Leave It To Terms", "Only the lock message shows.", "calm", (FI, [("h", "Add photos (optional)", 14), ("banner", "Snap photos to lock your price", JUNGLE, "check")]), "Short screen"))
    P("Home Photos", FI, "Upload box look", "for the one upload box should it be a dashed drop area or a camera button with the photos shown as thumbnails?",
      o("dash", "Dashed Drop Area", "A large dashed box, tap to add.", "calm", (FI, [("h", "Add photos", 14), DROP]), "Familiar"),
      o("cam", "Camera Button And Thumbnails", "Take photo button, thumbnails below.", "playful", (FI, [("h", "Add photos", 14), ("btn", "Take a photo", "fill", TERRA), ("photos", 3, 56)]), "Phone-native"))
    P("Your Home", FI, "Home type tile picture", "for the home type picture tiles should each tile show a simple line drawing or a soft photo?",
      o("line", "Line Drawing", "A clean house outline per type.", "calm", (FI, [("h", "What kind of home?", 14), ("tiles", [("House", "home"), ("Condo", "home"), ("Townhome", "home"), ("Other", "tag")], 2, 60)]), "Crisp"),
      o("photo", "Soft Photo", "A small photo of each home type.", "warm", (FI, [("h", "What kind of home?", 14), ("raw", "".join(photo(14 + (i % 2) * 110, (i // 2) * 76, 102, 50, ACC[i], "house") + t(18 + (i % 2) * 110, (i // 2) * 76 + 64, n, 9, INK, "khand") for i, n in enumerate(("House", "Condo", "Townhome", "Other"))), 150)]), "Warmer"))
    P("Your Home", FI, "Size chip picked state", "for the home size range chips should the picked chip fill solid terracotta or get a terracotta outline with a check?",
      o("solid", "Solid Fill", "Picked chip turns solid terracotta.", "focused", (FI, [("h", "About how big?", 14), ("raw", chip(14, 0, "Under 1,500", TERRA)[0] + chip(86, 0, "1,500 to 2,500", TERRA, True)[0] + chip(172, 0, "2,500+", TERRA)[0], 24)]), "Very clear"),
      o("outline", "Outline With Check", "Bold outline and a small check.", "calm", (FI, [("h", "About how big?", 14), ("raw", chip(14, 0, "Under 1,500", MUTE)[0] + rect(86, 0, 80, 15, "#FFFFFF", TERRA, 6, 1.6) + t(126, 10.5, "\u221A 1,500 to 2,500", 7.5, TERRA, "hind", 700, "middle") + chip(172, 0, "2,500+", MUTE)[0], 24)]), "Light"))
    P("Your Home", FI, "System tile on state", "for the home system icon tiles should an on tile fill with colour or stay white with a green check in the corner?",
      o("fill", "Fills With Colour", "On tiles turn solid colour.", "playful", (FI, [("h", "What's in the home?", 14), ("tiles", [("Furnace", "home"), ("Central air", "star"), ("Water heater", "clock"), ("Sump pump", "check")], 2, 56, "solid")]), "Bold"),
      o("check", "White With Check", "A small green check in the corner.", "calm", (FI, [("h", "What's in the home?", 14), ("raw", "".join(rect(14 + (i % 2) * 110, (i // 2) * 64, 102, 56, "#FFFFFF", JUNGLE if i < 2 else LINE, 9, 1.4 if i < 2 else 1) + t(24 + (i % 2) * 110, (i // 2) * 64 + 44, n, 10, INK, "khand") + (f'<circle cx="{104+(i%2)*110}" cy="{(i//2)*64+12}" r="7" fill="{JUNGLE}"/>' + t(104 + (i % 2) * 110, (i // 2) * 64 + 15, "\u221A", 8, "#FFFFFF", "hind", 700, "middle") if i < 2 else "") for i, n in enumerate(("Furnace", "Central air", "Water heater", "Sump pump"))), 130)]), "Calm"))
    P("Your Home", FI, "Info icon opens", "for the info icon you picked should the reason open as a small bubble by the icon or as a bottom sheet?",
      o("bubble", "Small Bubble", "A speech bubble right by the icon.", "calm", (FI, [("raw", t(14, 14, "Water heater age", 14, INK, "khand") + f'<circle cx="130" cy="9" r="6" fill="none" stroke="{LAGOON}"/>' + t(130, 12, "i", 8, LAGOON, "hind", 700, "middle"), 24), ("bubble", "Helps your tech plan flushes and checks"), AGE]), "Stays in place"),
      o("sheet", "Bottom Sheet", "Slides up from the bottom.", "practical", (FI, [("h", "Water heater age", 14), AGE, sheet("Why we ask", t(14, 20, "Helps your tech plan flushes and checks.", 8.5, MUTE), 60)]), "Easy to read"))
    P("Contact", FI, "Contact chips picked", "for the Text Call Email chips should more than one be allowed with ticks or only one at a time?",
      o("multi", "Pick Any With Ticks", "Tick as many as you like.", "practical", (FI, [("h", "How should we reach you?", 14), ("checks", ["Text", "Call", "Email"], JUNGLE, 2)]), "Flexible"),
      o("one", "One At A Time", "Pick your main way.", "calm", (FI, [("h", "How should we reach you?", 14), ("tabs", ["Text", "Call", "Email"])]), "Simple"))
    P("Access", FI, "Access switch detail", "when an access switch like Gate code is turned on should a small box slide open under it or should a sheet ask for the details?",
      o("inline", "Box Opens Under It", "Gate code box appears below the switch.", "practical", (FI, [("h", "Getting in", 14), ("toggles", [("Pets at home", True), ("Gate code", True)]), ("input", "Gate code", TERRA, "tag"), ("toggles", [("Lockbox", False)])]), "All in one place"),
      o("sheet", "Sheet Asks", "A sheet slides up for the details.", "calm", (FI, [("h", "Getting in", 14), ("toggles", [("Pets at home", True), ("Gate code", True), ("Lockbox", False)]), sheet("Gate code", t(14, 20, "Enter code", 8.5, FAINT), 50)]), "Clean list"))
    P("Your Home", FI, "Recap card edit", "on the home recap card should Edit sit beside each line or as one Edit button for the whole card?",
      o("each", "Edit Beside Each Line", "Change just one answer.", "practical", (FI, [("h", "Your home", 14), ("raw", "".join(t(14, 14 + i * 20, k, 8.5, INK, "hind", 500) + t(170, 14 + i * 20, v, 8.5, INK, "hind", 700, "end") + t(226, 14 + i * 20, "Edit", 7.5, TERRA, "hind", 600, "end") for i, (k, v) in enumerate((("Type", "House"), ("Size", "1,500-2,500"), ("Systems", "4"), ("Photos", "3")))), 86)]), "Fast fixes", "Sample answers"),
      o("one", "One Edit Button", "One button reopens the questions.", "calm", (FI, [("h", "Your home", 14), ("kv", [("Type", "House"), ("Size", "1,500 to 2,500"), ("Systems", "4 picked"), ("Photos", "3 added")]), ("btn", "Edit", "line", TERRA)]), "Tidy", "Sample answers"))
    return pairs
# ---------------- 7. Clear picks follow-up (member app) ----------------
def tabbar(style="line", fill=False, bg="#FFFFFF", c=TERRA):
    s = rect(0, 0, W, 44, bg) + ln(0, 0, W, LINE)
    for i, (n, k) in enumerate((("Home", "home"), ("Record", "check"), ("Visits", "cal"), ("Profile", "star"))):
        x = 30 + i * 60; on = i == 0
        if fill and on: s += f'<rect x="{x-12}" y="5" width="24" height="22" rx="6" fill="{c}22"/>'
        s += ic(k, x - 8, 8, 16, c if on else MUTE, 2.4 if fill and on else 1.8) + t(x, 38, n, 7, c if on else MUTE, "hind", 600, "middle")
        if on and style == "line": s += rect(x - 13, 41, 26, 2.5, c)
    return ("raw", s, 44)
def T_MEMBER2():
    pairs, P = make("fu18mb_", "UpKeep")
    HL = lambda w: ("raw", rect(14, 0, w, 30, TERRA) + t(20 + w, 10, "YOUR RECORD", 7, TERRA, "hind", 700, extra='letter-spacing="1"') + t(20 + w, 26, "Everything we've done", 13, INK, "khand"), 36)
    PL = lambda c: ("raw", f'<circle cx="206" cy="10" r="16" fill="{c}"/>' + t(206, 15.5, "+", 16, "#FFFFFF", "hind", 700, "middle"), 30)
    ADD = lambda photo_=True: ("raw", "".join(rect(14, i * 54, 212, 48, "#FFFFFF", LINE, 8) + (photo(20, i * 54 + 6, 50, 36, ACC[i], ["leaf", "house"][i]) if photo_ else rect(22, i * 54 + 12, 24, 24, ACC[i] + "22", "none", 6) + ic(["star", "home"][i], 26, i * 54 + 16, 16, ACC[i], 2)) + t(80 if photo_ else 56, i * 54 + 22, ["Lawn care", "Gutters"][i], 10, INK, "khand") + t(80 if photo_ else 56, i * 54 + 34, "+$X/mo", 7.5, MUTE) + rect(190, i * 54 + 17, 28, 15, JUNGLE if i == 0 else "#D6D0C6", "none", 7.5) + dot(190 + (20 if i == 0 else 8), i * 54 + 24.5, 5.5, "#FFFFFF") for i in range(2)), 110)
    P("Member App", MA, "Tab icon style", "for the four tabs with icons and labels should icons be thin outlines or filled when active?",
      o("outline", "Thin Outlines", "Every icon a thin line, active in terracotta.", "calm", (MA, [("h", "Home", 14), ("gap", 170), tabbar()]), "Light"),
      o("fill", "Filled When Active", "The active icon gets a soft fill.", "focused", (MA, [("h", "Home", 14), ("gap", 170), tabbar(fill=True)]), "Clear where you are"))
    P("Member App", MA, "Active tab colour", "should the active tab and its underline be terracotta or lagoon blue?",
      o("terra", "Terracotta", "Brand colour marks the active tab.", "warm", (MA, [("h", "Home", 14), ("gap", 170), tabbar()]), "On brand"),
      o("lag", "Lagoon Blue", "Calmer blue for the active tab.", "calm", (MA, [("h", "Home", 14), ("gap", 170), tabbar(c=LAGOON)]), "Calm"))
    P("Member App", MA, "Tab bar background", "should the tab bar be plain white with a thin top line or warm cream?",
      o("white", "White With Line", "White bar, hairline on top.", "calm", (MA, [("h", "Home", 14), ("gap", 170), tabbar()]), "Crisp"),
      o("cream", "Warm Cream", "A cream band holds the tabs.", "warm", (MA, [("h", "Home", 14), ("gap", 170), tabbar(bg=CREAM)]), "Warmer"))
    P("Member App", MA, "Side rule weight", "for the side rule headlines with terracotta caps should the rule be a thin line or a thick bar?",
      o("thin", "Thin Line", "A slim terracotta rule.", "calm", (MA, [HL(2), ("cards", [("Spring visit", "Done"), ("Filter change", "Done")])]), "Elegant"),
      o("thick", "Thick Bar", "A bold terracotta bar.", "focused", (MA, [HL(5), ("cards", [("Spring visit", "Done"), ("Filter change", "Done")])]), "Strong"))
    P("Member App", MA, "Round plus colour", "for the round plus button you picked should it be terracotta or jungle green?",
      o("terra", "Terracotta", "Brand colour round plus.", "warm", (MA, [("h", "Appliances", 14), ("cards", [("Furnace", "Sample"), ("Water heater", "Sample")]), ("gap", 70), PL(TERRA)]), "On brand"),
      o("green", "Jungle Green", "Green reads as add.", "calm", (MA, [("h", "Appliances", 14), ("cards", [("Furnace", "Sample"), ("Water heater", "Sample")]), ("gap", 70), PL(JUNGLE)]), "Feels positive"))
    P("Member App", MA, "Round plus opens", "when the round plus is tapped should it open a small menu of what to add or go straight to Add appliance?",
      o("menu", "Small Menu", "Appliance, photo or note.", "practical", (MA, [("h", "Appliances", 14), ("gap", 70), ("cards", [("Add appliance", ""), ("Add photo", ""), ("Add note", "")], [TERRA, LAGOON, JUNGLE], "dot", "line", 26), PL(TERRA)]), "One button, many uses"),
      o("direct", "Straight To Add Appliance", "One tap, one job.", "calm", (MA, [("h", "Add appliance", 14), ("input", "Appliance name", TERRA, "tag"), ("input", "Brand and model", TERRA, "tag")]), "Fast"))
    P("Add-Ons", MA, "Add-on card picture", "for the add-on cards with toggles should each card show a small photo or a simple icon?",
      o("photo", "Small Photo", "A photo on each card.", "warm", (MA, [("h", "Add-ons", 14), ADD(True)]), "Inviting", "SAMPLE prices"),
      o("icon", "Simple Icon", "A line icon in a soft square.", "calm", (MA, [("h", "Add-ons", 14), ADD(False)]), "Compact", "SAMPLE prices"))
    P("Add-Ons", MA, "No thanks style", "for No thanks at the bottom should it be a plain text link or an outline button?",
      o("link", "Plain Text Link", "Small underlined No thanks.", "calm", (MA, [("h", "Add-ons", 14), ADD(True), ("btn", "Continue", "fill", TERRA), ("btn", "No thanks", "link", MUTE)]), "Gentle"),
      o("outline", "Outline Button", "A full-width outline No thanks.", "practical", (MA, [("h", "Add-ons", 14), ADD(True), ("btn", "Continue", "fill", TERRA), ("btn", "No thanks", "line", MUTE)]), "Easy to tap"))
    P("Order Form", MA, "Card boxes look", "for showing the card boxes before payment should the boxes look greyed as a preview or fully live and ready to type?",
      o("grey", "Greyed Preview", "Boxes shown faded until the pay step.", "calm", (MA, [("h", "Payment comes next", 14), ("raw", rect(14, 0, 212, 28, "#F3F0EA", LINE, 6) + t(22, 18, "Card number", 8, FAINT) + rect(14, 34, 212, 28, "#F3F0EA", LINE, 6) + t(22, 52, "MM / YY   CVC", 8, FAINT), 68)]), "No pressure yet"),
      o("live", "Live And Ready", "Real boxes, type right away.", "practical", (MA, [("h", "Payment", 14), ("input", "Card number", TERRA, "card"), ("input", "MM / YY   CVC", TERRA, "card")]), "One less step"))
    P("Member App", MA, "Tab swipe hint", "with swipe changing tabs should the first visit show a one-time Swipe between tabs hint or no hint?",
      o("hint", "One-Time Hint", "A small toast the first time only.", "practical", (MA, [("h", "Home", 14), ("gap", 120), ("raw", rect(40, 0, 160, 26, INK, "none", 13) + t(120, 17, "Swipe between tabs", 8.5, "#FFFFFF", "hind", 600, "middle"), 34), tabbar()]), "Nobody misses it"),
      o("none", "No Hint", "People find it on their own.", "calm", (MA, [("h", "Home", 14), ("gap", 160), tabbar()]), "Uncluttered"))
    return pairs
# ---------------- 8. Forecast follow-up ----------------
def T_FC2():
    pairs, P = make("fu18fc_", "UpKeep")
    LN = ("line", [.1, .3, .5, .7, .9])
    P("Scenarios", FA, "Scenario cards to swipe", "since you asked to see which scenarios would show should the swipe cards be Base and Fast growth and High churn or Base and Price up and Slow sign-ups?",
      o("set1", "Base, Fast Growth, High Churn", "Upside and the main risk.", "practical", (FA, [("h", "Scenarios", 14), ("carousel", [("Base", "Forecast", LAGOON), ("Fast growth", "More sign-ups", JUNGLE), ("High churn", "More members leave", TERRA)], 150, 90, True), ("sample", "FORECAST, SAMPLE")]), "Easy to digest"),
      o("set2", "Base, Price Up, Slow Sign-Ups", "Pricing and a slow start.", "focused", (FA, [("h", "Scenarios", 14), ("carousel", [("Base", "Forecast", LAGOON), ("Price up", "$99 to $X", JUNGLE), ("Slow sign-ups", "Half the pace", TERRA)], 150, 90, True), ("sample", "FORECAST, SAMPLE")]), "Tests two levers"))
    P("Scenarios", FA, "Scenario card content", "on each scenario card should there be one small chart or three big numbers?",
      o("chart", "One Small Chart", "A mini line on each card.", "playful", (FA, [("h", "Fast growth", 14), LN, ("sample", "FORECAST, SAMPLE")]), "See the shape"),
      o("nums", "Three Big Numbers", "Members, revenue, cash at year five.", "practical", (FA, [("h", "Fast growth", 14), ("stats", [("X", "members"), ("$X.XM", "revenue"), ("$X.XM", "cash")], "tint"), ("sample", "FORECAST, SAMPLE")]), "Quick to compare"))
    P("Scenarios", FA, "Compare scenarios", "should there be a way to see two scenarios on one chart or only one at a time?",
      o("two", "Two On One Chart", "Base dashed, chosen scenario solid.", "focused", (FA, [("h", "Base vs Fast growth", 14), ("raw", rect(14, 0, 212, 70, SOFT, "none", 6) + f'<polyline points="14,60 70,52 130,44 226,30" fill="none" stroke="{MUTE}" stroke-dasharray="4 3" stroke-width="2"/><polyline points="14,60 70,46 130,30 226,8" fill="none" stroke="{JUNGLE}" stroke-width="2"/>', 78), ("sample", "FORECAST, SAMPLE")]), "See the gap"),
      o("one", "One At A Time", "Swipe to change scenario.", "calm", (FA, [("h", "Fast growth", 14), LN, ("cdots", 3, 1)]), "Simple"))
    P("Key Drivers", FA, "Biggest driver view", "for showing which assumption moves the results most should it be bars spreading from a centre line or a plain numbered list?",
      o("tornado", "Bars From A Centre Line", "Longest bar is the biggest driver.", "focused", (FA, [("h", "What moves results most", 13), ("raw", f'<line x1="140" y1="0" x2="140" y2="66" stroke="#D6D0C6"/>' + "".join(rect(140 - w, i * 22, w, 14, TERRA + "88", "none", 2) + rect(140, i * 22, w, 14, JUNGLE + "88", "none", 2) + t(14, i * 22 + 10, n, 7.5, INK) for i, (n, w) in enumerate((("Churn", 70), ("Price", 50), ("Visits", 30)))), 70), ("sample", "FORECAST, SAMPLE")]), "Visual"),
      o("list", "Plain Numbered List", "1 Churn, 2 Price, 3 Visits per home.", "calm", (FA, [("h", "What moves results most", 13), ("cards", [("Churn", "Biggest effect"), ("Price", "Second"), ("Visits per home", "Third")], [TERRA, LAGOON, JUNGLE], "num")]), "Plain"))
    P("Key Drivers", FA, "Driver tap", "should tapping a driver jump to its chip so you can change it right away or should the ranking be read-only?",
      o("jump", "Tap Jumps To Chip", "Tap Churn, the churn chip opens.", "practical", (FA, [("h", "Churn", 14), ("bar", .3, LAGOON, "Churn (Forecast)", "X%"), ("line", [.2, .35, .5, .62, .8])]), "Fast to explore"),
      o("view", "Read-Only", "The ranking is just for reading.", "calm", (FA, [("h", "What moves results most", 13), ("cards", [("Churn", ""), ("Price", ""), ("Visits per home", "")], [TERRA, LAGOON, JUNGLE], "num")]), "Fewer jumps"))
    P("Printing", FA, "Printout shape", "when a scenario is printed or saved should the page be tall with the chart above the numbers or wide with them side by side?",
      o("tall", "Tall Page", "Chart on top, numbers under it.", "calm", (FA, [("raw", rect(70, 0, 100, 140, "#FFFFFF", LINE, 4) + rect(78, 10, 84, 50, SOFT, "none", 3) + "".join(rect(78, 70 + i * 12, 84, 6, "#EEEAE4", "none", 2) for i in range(5)), 148)]), "Reads on a phone"),
      o("wide", "Wide Page", "Chart and numbers side by side.", "practical", (FA, [("raw", rect(20, 20, 200, 110, "#FFFFFF", LINE, 4) + rect(28, 30, 100, 90, SOFT, "none", 3) + "".join(rect(136, 34 + i * 14, 76, 6, "#EEEAE4", "none", 2) for i in range(5)), 140)]), "Like a slide"))
    P("Labels", FA, "Sample data marking", "to show the numbers are sample data should a thin banner run across the top or a faint SAMPLE sit behind each chart?",
      o("banner", "Thin Top Banner", "Sample data, not real numbers.", "practical", (FA, [("banner", "Sample data, not real numbers", SAFFRON, "tag"), LN]), "Unmissable"),
      o("water", "Faint Behind Charts", "SAMPLE written softly behind each chart.", "calm", (FA, [("h", "Revenue", 14), ("raw", rect(14, 0, 212, 80, SOFT, "none", 6) + t(120, 50, "SAMPLE", 26, "#E5DFD3", "khand", 700, "middle") + f'<polyline points="14,70 80,56 150,36 226,12" fill="none" stroke="{JUNGLE}" stroke-width="2"/>', 88)]), "Charts stay clean"))
    P("Charts", FA, "Chart carousel position", "for the chart carousel should the position show as dots under the chart or as chart names you can tap?",
      o("dots", "Dots Under", "Three small dots.", "calm", (FA, [("h", "Revenue", 14), LN, ("cdots", 3, 0)]), "Minimal"),
      o("names", "Tappable Names", "Revenue, Members, Cash under the chart.", "practical", (FA, [("h", "Revenue", 14), LN, ("tabs", ["Revenue", "Members", "Cash"], "line")]), "Know what's next"))
    P("Charts", FA, "Months-left bar colours", "should the months-left bar change colour from green to amber to terracotta as cash gets low or stay one colour?",
      o("zones", "Colour Changes", "Green when safe, terracotta when low.", "practical", (FA, [("h", "Cash runway", 14), ("bar", .35, SAFFRON, "Months of cash (Forecast)", "X months"), ("scale", .35, ("Low", "OK", "Safe"), (TERRA, SAFFRON, JUNGLE))]), "Warns early"),
      o("one", "One Colour", "A lagoon bar, always.", "calm", (FA, [("h", "Cash runway", 14), ("bar", .35, LAGOON, "Months of cash (Forecast)", "X months")]), "Calm"))
    P("Scenarios", FA, "Reset placement", "with both Reset to base and undo on each chip should Reset to base sit at the top or at the bottom of the chips?",
      o("top", "At The Top", "Reset sits by the scenario name.", "practical", (FA, [("raw", t(14, 14, "Fast growth", 14, INK, "khand") + t(226, 14, "Reset to base", 8, TERRA, "hind", 600, "end"), 24), ("pills", ["Churn X%  \u21b6", "Price $X", "Visits X"], [TERRA, LAGOON, JUNGLE])]), "Easy to find"),
      o("bottom", "At The Bottom", "Under the chips, out of the way.", "calm", (FA, [("h", "Fast growth", 14), ("pills", ["Churn X%  \u21b6", "Price $X", "Visits X"], [TERRA, LAGOON, JUNGLE]), ("btn", "Reset to base", "link", TERRA)]), "No accidents"))
    return pairs
# ---------------- 9. Story flow follow-up ----------------
def T_STORY2():
    pairs, P = make("fu18sf_", "UpKeep")
    ORD = lambda at: ("cards", [(n, "here" if n == "Founder" else "") for n in at], [TERRA if n == "Founder" else MUTE for n in at], "num", "line", 28)
    P("Story Flow", PA, "Founder screen spot", "in the tap-through order should the founder screen come right after the product screens or just before The Ask?",
      o("after", "Right After Product", "Who built it, right after what it does.", "practical", (L, [ORD(["Problem", "Product", "Founder", "Market", "The Ask"])]), "Credit where it lands"),
      o("before", "Just Before The Ask", "The last thing before the terms.", "focused", (L, [ORD(["Problem", "Product", "Market", "Founder", "The Ask"])]), "Trust before money"))
    KL = lambda c: ("raw", rect(14, 30, 120, 6, c + "55", "none", 2) + t(14, 32, "Small leaks", 18, INK, "khand") + t(14, 54, "become big bills", 18, INK, "khand"), 64)
    P("Visual Style", PA, "Key line highlight", "for the one key line on each screen should it be marked with a terracotta underline or a lagoon blue underline?",
      o("terra", "Terracotta Underline", "Warm marker under the key words.", "warm", (L, [top(2, "Problem"), KL(TERRA)]), "Energetic"),
      o("lag", "Lagoon Underline", "Calm blue under the key words.", "calm", (L, [top(2, "Problem"), KL(LAGOON)]), "Steady"))
    P("Numbers", PA, "Takeaway line look", "for number plus takeaway should the takeaway sit under the number in grey or beside it in a terracotta bubble?",
      o("under", "Grey Line Under", "Number, then one grey sentence.", "calm", (L, [top(4, "Market"), ("word", "X M", 34, INK, "HOMES IN THE AREA (SAMPLE)"), ("p", "Plenty of room to grow", 46, MUTE, True)]), "Clean"),
      o("bubble", "Terracotta Bubble Beside", "A small bubble with the meaning.", "playful", (L, [top(4, "Market"), ("raw", t(30, 40, "X M", 34, INK, "khand") + rect(120, 14, 100, 30, TERRA + "1A", TERRA, 10) + t(170, 33, "Room to grow", 8.5, INK, "hind", 600, "middle"), 54), ("sample",)]), "Draws the eye"))
    P("Product", PA, "Phone frame colour", "for the product screens in phone frames should the frame be ink black or soft white?",
      o("ink", "Ink Black Frame", "Classic black phone outline.", "focused", (L, [top(3, "Product"), ("raw", rect(60, 0, 120, 200, "#FFFFFF", INK, 14, 5) + rect(105, 6, 30, 5, INK, "none", 3), 208)]), "Pops on white"),
      o("white", "Soft White Frame", "A light frame with a soft shadow.", "calm", (L, [top(3, "Product"), ("raw", rect(63, 4, 120, 200, "#0000000F", "none", 16) + rect(60, 0, 120, 200, "#FFFFFF", "#E5E0D8", 14, 5), 208)]), "Light and airy"))
    P("Product", PA, "Screens per product slide", "should each product screen get its own tap or should two phones sit side by side on one screen?",
      o("one", "One Phone Per Tap", "One app screen fills the slide.", "calm", (L, [top(3, "Product"), ("raw", rect(60, 0, 120, 200, "#FFFFFF", INK, 14, 4), 208)]), "Big detail"),
      o("two", "Two Side By Side", "Member app and tech app together.", "practical", (L, [top(3, "Product"), ("raw", rect(20, 0, 95, 170, "#FFFFFF", INK, 12, 3) + rect(125, 0, 95, 170, "#FFFFFF", INK, 12, 3) + t(67, 186, "Member app", 8.5, INK, "khand", anchor="middle") + t(172, 186, "Tech app", 8.5, INK, "khand", anchor="middle"), 196)]), "Shows the pair"))
    P("Problem", PA, "Repair story steps", "for the one repair story should the drip becoming a ceiling play out across three photos you tap through or in one photo with a caption?",
      o("three", "Three Photos, Tap Through", "Drip, stain, ceiling, one per tap.", "playful", (L, [top(1, "Problem"), ("photos", 3, 90, ["room", "room", "room"], [LAGOON, SAFFRON, TERRA]), ("pills", ["Week 1", "Month 3", "Month 9"], [LAGOON, SAFFRON, TERRA])]), "Builds tension"),
      o("one", "One Photo, Caption", "One picture, one sentence.", "calm", (L, [top(1, "Problem"), ("photo", 150, TERRA, "room", "A drip that became a ceiling")]), "Fast"))
    P("Opening", PA, "Promise screen", "for the promise screen after the story should the promise be one big line or the line plus three small proof chips?",
      o("line", "One Big Line", "Home maintenance on autopilot.", "focused", (L, [top(2, "The promise"), ("gap", 50), ("h", "Home maintenance", 22, INK, True), ("h", "on autopilot", 22, TERRA, True)]), "Bold"),
      o("chips", "Line Plus Proof Chips", "Visits, photos, one plan.", "practical", (L, [top(2, "The promise"), ("gap", 40), ("h", "Home maintenance on autopilot", 16, INK, True), ("pills", ["Seasonal visits", "Photo reports", "One plan"], [TERRA, LAGOON, JUNGLE])]), "Backs it up"))
    P("Closing", PA, "Vision picture", "for ending on the brand picture should it be the branded van in front of a home or a tech at a front door?",
      o("van", "Van In Front Of A Home", "The van parked at a metro Detroit home.", "warm", (L, [top(9, "Vision"), ("photo", 170, LAGOON, "house", "Every home on autopilot")]), "Big picture"),
      o("door", "Tech At The Door", "A friendly tech arriving.", "warm", (L, [top(9, "Vision"), ("photo", 170, TERRA, "person", "Every home on autopilot")]), "Human"))
    P("Market", PA, "Market size picture", "in the classic order should market size show as nested circles or as one bar with the first area marked?",
      o("circles", "Nested Circles", "Big circle, smaller, our first slice.", "practical", (L, [top(4, "Market"), ("raw", f'<circle cx="120" cy="70" r="66" fill="{LAGOON}14" stroke="{LAGOON}"/><circle cx="120" cy="96" r="40" fill="{JUNGLE}1A" stroke="{JUNGLE}"/><circle cx="120" cy="116" r="18" fill="{TERRA}33" stroke="{TERRA}"/>' + t(120, 22, "US homes", 7.5, INK, "hind", 600, "middle") + t(120, 70, "Michigan", 7.5, INK, "hind", 600, "middle") + t(120, 119, "Metro", 7, INK, "hind", 600, "middle"), 144), ("sample",)]), "Classic"),
      o("bar", "One Bar, Area Marked", "A bar with the first area in terracotta.", "calm", (L, [top(4, "Market"), ("raw", rect(14, 20, 212, 20, LAGOON + "33", "none", 4) + rect(14, 20, 30, 20, TERRA, "none", 4) + t(14, 56, "Metro Detroit first", 8, INK, "hind", 600) + t(226, 56, "Then wider", 8, MUTE, anchor="end"), 66), ("sample",)]), "Simple"))
    P("Pitch App", PA, "Link preview", "when the pitch link is sent by text should the preview show the white wordmark cover or the problem photo?",
      o("cover", "Wordmark Cover", "White card with the Smart Upkeep wordmark.", "calm", (L, [("bubble", "Here's the pitch, take a look"), ("raw", rect(14, 0, 180, 110, "#FFFFFF", LINE, 10) + t(104, 56, "Smart Upkeep", 18, INK, "khand", anchor="middle") + rect(14, 80, 180, 30, SOFT, "none", 0) + t(22, 99, "Investor pitch", 8, MUTE), 118)]), "Clean brand"),
      o("photo", "Problem Photo", "The leak photo as the preview.", "warm", (L, [("bubble", "Here's the pitch, take a look"), ("raw", photo(14, 0, 180, 80, TERRA, "room", 10) + rect(14, 80, 180, 30, SOFT, "none", 0) + t(22, 99, "Investor pitch", 8, MUTE), 118)]), "Makes them curious"))
    return pairs
