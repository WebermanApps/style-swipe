"""Financial Forecasting Deck: chart and scenario views. Every number is EXAMPLE DATA."""
from uk5_art import *
PAIRS = []
def pair(g, ask, a, b): PAIRS.append((g, ask, a, b))
def note(y, lines): return "".join(t(14, y + i * 11, l, 7.5, MUTE) for i, l in enumerate(lines))
def legend(y, items, x=14):
    s = ""
    for lb, c in items: s += rect(x, y - 6, 8, 8, c) + t(x + 11, y + 1, lb, 7.5, INK, "hind", 600); x += len(lb) * 4.7 + 22
    return s
def panel(y=30, h=150): return rect(14, y, 212, h, "#FFFFFF", LINE)
ES = [2, 3, 4, 5, 6, 7, 8, 9]; PL = [1, 2, 3, 4.5, 6, 7, 8.5, 10]; CO = [.5, 1, 1.5, 2, 3, 3.5, 4.5, 5]
Q = ["Q1", "Q3", "Q5", "Q8"]
TOT = [a + b + c for a, b, c in zip(ES, PL, CO)]
# 1 stacked area vs lines (lead)
pair("Chart Type", "Revenue Chart: Stacked Area By Plan, Or One Line Per Plan?",
 ("fc_stacked", "Stacked Area By Plan", "Shows the total and each plan's share at once.", "bold",
  card("Chart Type", TERRA, panel() + t(22, 46, "Monthly revenue by plan", 9, INK, "khand") + axes(24, 56, 194, 104, ticks=Q) + stacked(24, 56, 194, 104, [ES, PL, CO], [LAGOON + "CC", SAFFRON + "CC", TERRA + "CC"], 26)
       + legend(196, [("Essentials", LAGOON), ("Plus", SAFFRON), ("Complete", TERRA)]) + note(214, ["Top edge = total revenue.", "Example data, 8 quarters."]) + chips(272, ["Total + mix"]), example=True)),
 ("fc_lines", "One Line Per Plan", "Easier to read each plan's own trend.", "calm",
  card("Chart Type", LAGOON, panel() + t(22, 46, "Monthly revenue by plan", 9, INK, "khand") + axes(24, 56, 194, 104, ticks=Q) + line(24, 56, 194, 104, ES, 12, LAGOON, 2) + line(24, 56, 194, 104, PL, 12, SAFFRON, 2) + line(24, 56, 194, 104, CO, 12, TERRA, 2)
       + legend(196, [("Essentials", LAGOON), ("Plus", SAFFRON), ("Complete", TERRA)]) + note(214, ["Total shown as a number above.", "Example data, 8 quarters."]) + chips(272, ["Per-plan trend"]), example=True)))
# 2 scenario tabs vs overlay band
BASE = [2, 3, 4.2, 5.5, 7, 8.6, 10, 12]; BEST = [2, 3.4, 5, 7, 9, 11.5, 14, 17]; WORST = [2, 2.6, 3.2, 3.8, 4.5, 5.1, 5.8, 6.5]
def tabs(y, items, on):
    s, x = "", 14
    for i, lb in enumerate(items):
        w = 70.6; s += rect(x, y, w, 18, INK if i == on else "#FFFFFF", INK, 0, 1) + t(x + w / 2, y + 12.5, lb, 8, "#FFFFFF" if i == on else INK, "hind", 600, "middle"); x += w
    return s
pair("Scenarios", "Scenarios: Tabs For Base, Best And Worst, Or All Three On One Chart With A Band?",
 ("sc_tabs", "Tabs: Base, Best, Worst", "One clean chart; tap a tab to switch.", "calm",
  card("Scenario View", LAGOON, tabs(30, ["Base", "Best", "Worst"], 0) + panel(52, 140) + axes(24, 66, 194, 106, ticks=Q) + line(24, 66, 194, 106, BASE, 18, LAGOON, 2.4) + note(206, ["Members, base case only.", "Best and worst one tap away."]) + chips(272, ["Uncluttered"]), example=True)),
 ("sc_band", "All Three With A Band", "Base line, shaded range from worst to best.", "bold",
  card("Scenario View", TERRA, panel(30, 162) + t(22, 46, "Members: worst to best range", 9, INK, "khand") + axes(24, 58, 194, 112, ticks=Q) + area(24, 58, 194, 112, WORST, BEST, 18, TERRA + "26") + line(24, 58, 194, 112, BEST, 18, JUNGLE, 1.4, "3 2") + line(24, 58, 194, 112, BASE, 18, TERRA, 2.4) + line(24, 58, 194, 112, WORST, 18, MUTE, 1.4, "3 2")
       + legend(206, [("Base", TERRA), ("Best", JUNGLE), ("Worst", MUTE)]) + note(222, ["See the spread at a glance."]) + chips(272, ["See the range"]), example=True)))
# 3 small multiples vs table
def mini(x, y, w, h, vals, c, lb):
    return rect(x, y, w, h, "#FFFFFF", LINE) + t(x + 5, y + 11, lb, 8, c, "khand") + axes(x + 5, y + 16, w - 10, h - 24) + line(x + 5, y + 16, w - 10, h - 24, vals, 18, c, 1.8)
rows = [("Members, month 36", "XXX", "XXX", "XXX"), ("Revenue, year 3", "$X.XM", "$X.XM", "$X.XM"), ("Break-even", "Q6", "Q5", "Q9"), ("Lowest cash", "-$XXk", "-$XXk", "-$XXk")]
def table(y):
    s = rect(14, y, 212, 18, CREAM) + "".join(t(x, y + 12.5, h, 8, c, "hind", 600, "end" if i else "start") for i, (x, h, c) in enumerate([(20, "Example", INK), (132, "Worst", MUTE), (178, "Base", TERRA), (222, "Best", JUNGLE)]))
    for r, (a, b, c, d) in enumerate(rows):
        yy = y + 18 + r * 22; s += ln(yy + 22) + t(20, yy + 14, a, 7.5, INK) + t(132, yy + 14, b, 8, MUTE, "hind", 600, "end") + t(178, yy + 14, c, 8, TERRA, "hind", 600, "end") + t(222, yy + 14, d, 8, JUNGLE, "hind", 600, "end")
    return s
pair("Scenarios", "Comparing Scenarios: Three Small Charts Side By Side, Or A Table Of Key Results?",
 ("sc_multiples", "Three Small Charts", "Same scale, side by side, shape first.", "playful",
  card("Scenario Compare", JUNGLE, mini(14, 32, 68, 110, WORST, MUTE, "Worst") + mini(86, 32, 68, 110, BASE, TERRA, "Base") + mini(158, 32, 68, 110, BEST, JUNGLE, "Best") + note(160, ["Same axis on all three so", "the shapes compare fairly."]) + chips(272, ["Shapes"]), example=True)),
 ("sc_table", "Key Results Table", "Members, revenue, break-even and low cash, by scenario.", "practical",
  card("Scenario Compare", TERRA, table(32) + note(160, ["Values are placeholders (XXX,", "$X.XM) until the model runs."]) + chips(272, ["Exact numbers"]), example=True)))
# 4 horizon
L5 = [1, 1.5, 2.2, 3, 4, 5.2, 6.2, 7.2, 8.4, 9.4, 10.4, 11.2]
pair("Time Horizon", "Horizon: Stop At 3 Years, Or Run To 5 Years With Years 4 And 5 Shaded As Rough?",
 ("hz_3y", "3 Years, Monthly Detail", "Only what you can plan for, month by month.", "practical",
  card("Time Horizon", LAGOON, panel() + t(22, 46, "Members, 36 months", 9, INK, "khand") + axes(24, 56, 194, 104, ticks=["M1", "M12", "M24", "M36"]) + bars(24, 56, 194, 104, L5[:9] * 1, 10, LAGOON, None, .2) + note(196, ["36 monthly steps (bars grouped", "by quarter here)."]) + chips(272, ["Tighter"]), example=True)),
 ("hz_5y", "5 Years, Last 2 Shaded", "Years 4 and 5 shown faded and labeled rough.", "bold",
  card("Time Horizon", TERRA, panel() + t(22, 46, "Members, 5 years", 9, INK, "khand") + rect(24 + 194 * .6, 56, 194 * .4, 104, SAFFRON + "1F") + t(24 + 194 * .8, 70, "ROUGH", 8, "#7A5A0C", "hind", 600, "middle", 'letter-spacing="1"') + axes(24, 56, 194, 104, ticks=["Y1", "Y2", "Y3", "Y4", "Y5"]) + line(24, 56, 194 * .6, 104, [1, 3, 5.2, 7.2], 12, TERRA, 2.4) + line(24 + 194 * .6 - 194 * .6 / 3 * 0, 56, 194 * .4, 104, [7.2, 9.4, 11.2], 12, TERRA, 2, "4 3")
       + note(196, ["Solid = planned, dashed = rough.", "Good for an investor ask."]) + chips(272, ["Longer view"]), example=True)))
# 5 unit economics waterfall vs card
def waterfall(y):
    steps = [("Price", 100, 0, LAGOON), ("Labor", -38, 100, TERRA), ("Parts", -12, 62, TERRA), ("Travel", -8, 50, TERRA), ("Margin", 42, 0, JUNGLE)]
    s = axes(24, y, 194, 110); bw = 194 / 5
    for i, (lb, v, b, c) in enumerate(steps):
        top = b + v if v < 0 else b + v; lo = b + v if v < 0 else b
        hi = b if v < 0 else b + v
        s += rect(24 + i * bw + 5, y + 110 - 110 * hi / 110, bw - 10, 110 * (hi - lo) / 110, c) + t(24 + i * bw + bw / 2, y + 122, lb, 7.5, MUTE, "hind", 400, "middle")
    return s
pair("Per Member", "Per-Member Unit Economics: A Waterfall From Price To Margin, Or A Simple Card Of Lines?",
 ("ue_waterfall", "Waterfall, Price To Margin", "Each cost steps down from the monthly price.", "bold",
  card("Per Member", JUNGLE, panel(30, 160) + t(22, 46, "One member, per month (index 100)", 9, INK, "khand") + waterfall(56) + note(204, ["Bars are example shares of a", "100-point price, not real costs."]) + chips(272, ["Visual"]), example=True)),
 ("ue_card", "Per-Member Card", "Price, each cost and margin as lines.", "practical",
  card("Per Member", LAGOON, panel(30, 160) + t(22, 48, "One member, per month", 10, INK, "khand") + "".join(ln(58 + i * 22, 22, 218) + t(22, 74 + i * 22, a, 8.5, INK) + t(218, 74 + i * 22, b, 8.5, c, "hind", 600, "end") for i, (a, b, c) in enumerate([("Price", "$XXX", INK), ("Labor", "-$XX", TERRA), ("Parts", "-$XX", TERRA), ("Travel", "-$XX", TERRA), ("Margin", "$XX", JUNGLE)]))
       + note(204, ["Placeholders until the model", "fills in real values."]) + chips(272, ["Exact"]), example=True)))
# 6 by tier vs blended
pair("Per Member", "Per-Member View: Split By Plan (Essentials, Plus, Complete), Or One Blended Member?",
 ("ue_tiers", "Split By Plan", "Three columns, so you see which plan earns most.", "practical",
  card("Per Member", SAFFRON, "".join(rect(14 + i * 72, 32, 68, 150, "#FFFFFF", LINE) + rect(14 + i * 72, 32, 68, 4, c) + t(48 + i * 72, 52, lb, 10, c, "khand", anchor="middle") + bars(22 + i * 72, 62, 52, 90, [v, v * .45], v * 1.1, c, None, .25) + t(34 + i * 72, 166, "Price", 7.5, MUTE, "hind", 400, "middle") + t(62 + i * 72, 166, "Margin", 7.5, MUTE, "hind", 400, "middle") for i, (lb, c, v) in enumerate([("Essentials", LAGOON, 4), ("Plus", SAFFRON, 6), ("Complete", TERRA, 10)])) + note(198, ["Bar heights are example shapes."]) + chips(272, ["By plan"]), example=True)),
 ("ue_blended", "One Blended Member", "A single average member across all plans.", "calm",
  card("Per Member", INK, panel(32, 150) + t(120, 70, "Average member", 11, INK, "khand", anchor="middle") + t(120, 110, "$XX", 34, JUNGLE, "khand", anchor="middle") + t(120, 126, "margin per month", 8, MUTE, "hind", 400, "middle") + rect(40, 140, 160, 8, "#EEEAE4") + rect(40, 140, 60, 8, LAGOON) + rect(100, 140, 60, 8, SAFFRON) + rect(160, 140, 40, 8, TERRA) + t(120, 164, "Plan mix (example)", 7.5, MUTE, "hind", 400, "middle") + note(198, ["One number, plan mix shown", "as a thin bar."]) + chips(272, ["Simple"]), example=True)))
# 7 churn display
RET = [100, 92, 86, 81, 77, 74, 71, 69]
pair("Churn", "Churn: A Retention Curve Of Members Still With Us, Or A Monthly Churn Rate Tile?",
 ("ch_curve", "Retention Curve", "Out of 100 who join, how many are still members each quarter.", "calm",
  card("Churn", LAGOON, panel() + t(22, 46, "Of 100 who join, still members", 9, INK, "khand") + axes(24, 56, 194, 104, ticks=Q) + area(24, 56, 194, 104, [0] * 8, RET, 110, LAGOON + "22") + line(24, 56, 194, 104, RET, 110, LAGOON, 2.4) + t(214, 56 + 104 - 104 * 69 / 110 - 6, "69", 9, LAGOON, "hind", 600, "end")
       + note(196, ["Example curve, not a forecast."]) + chips(272, ["Long view"]), example=True)),
 ("ch_tile", "Monthly Churn Tile", "One rate with a small slider to test higher or lower churn.", "practical",
  card("Churn", TERRA, panel(30, 150) + t(120, 70, "Monthly churn", 11, INK, "khand", anchor="middle") + t(120, 112, "X.X%", 36, TERRA, "khand", anchor="middle") + rect(40, 132, 160, 4, "#EEEAE4") + rect(40, 132, 64, 4, TERRA) + f'<circle cx="104" cy="134" r="6" fill="#FFFFFF" stroke="{TERRA}" stroke-width="2"/>' + t(40, 152, "Lower", 7.5, MUTE) + t(200, 152, "Higher", 7.5, MUTE, "hind", 400, "end")
       + note(196, ["Placeholder rate; drag to test."]) + chips(272, ["Adjustable"]), example=True)))
# 8 assumptions placement
pair("Assumptions", "Assumptions: Chips Beside The Chart You Can Tap To Edit, Or A Footnote Drawer Below?",
 ("as_chips", "Editable Chips Beside Chart", "Churn, price and visits per tech sit next to the chart.", "playful",
  card("Assumptions", JUNGLE, rect(14, 32, 140, 130, "#FFFFFF", LINE) + axes(22, 44, 124, 100) + line(22, 44, 124, 100, BASE, 18, TERRA, 2) + "".join(rect(160, 32 + i * 34, 66, 28, "#FFFFFF", JUNGLE, 0, 1) + t(165, 44 + i * 34, lb, 7.5, MUTE) + t(165, 55 + i * 34, v, 8.5, INK, "hind", 600) for i, (lb, v) in enumerate([("Churn / mo", "X.X%"), ("Price", "$XXX"), ("Visits/tech", "X/day"), ("Referrals", "X%")]))
       + note(178, ["Change a chip, the chart redraws."]) + chips(272, ["Hands-on"]), example=True)),
 ("as_drawer", "Footnote Drawer", "Chart stays big; assumptions open from a link below.", "calm",
  card("Assumptions", LAGOON, rect(14, 32, 212, 120, "#FFFFFF", LINE) + axes(22, 44, 196, 92) + line(22, 44, 196, 92, BASE, 18, TERRA, 2.4) + rect(14, 158, 212, 18, CREAM) + t(20, 170, "Assumptions (4)", 8.5, INK, "hind", 600) + t(220, 170, "+", 10, INK, "hind", 600, "end") + "".join(t(20, 192 + i * 12, s, 7.5, MUTE) for i, s in enumerate(["Churn X.X% a month", "Price $XXX a month", "X visits per tech a day"]))
       + chips(272, ["Clean chart"]), example=True)))
# 9 dashboard vs one-pager
def dash_inner():
    return (rect(0, 0, 400, 260, "#FFFFFF") + t(12, 20, "Forecast", 16, INK, "khand") + "".join(rect(12 + i * 96, 30, 88, 44, "#FFFFFF", LINE) + t(18 + i * 96, 52, v, 14, c, "khand") + t(18 + i * 96, 66, l, 8, MUTE) for i, (v, l, c) in enumerate([("XXX", "Members", INK), ("$XXk", "MRR", TERRA), ("X.X%", "Churn", LAGOON), ("Q6", "Break-even", JUNGLE)]))
            + rect(12, 84, 260, 160, "#FFFFFF", LINE) + axes(22, 96, 240, 130) + stacked(22, 96, 240, 130, [ES, PL, CO], [LAGOON + "CC", SAFFRON + "CC", TERRA + "CC"], 26) + rect(282, 84, 106, 160, CREAM) + "".join(rect(290, 96 + i * 26, 90, 18, "#FFFFFF", LINE) + t(296, 108 + i * 26, s, 8, INK) for i, s in enumerate(["Scenario: Base", "Horizon: 3 yrs", "View: Monthly", "Plan: All", "Export PDF"])))
def paper():
    return (rect(0, 0, 210, 297, "#FFFFFF") + t(14, 26, "Smart Upkeep Forecast", 15, INK, "khand") + t(14, 38, "One page, Month XX (example)", 8, MUTE) + rect(14, 46, 182, 3, TERRA)
            + "".join(t(14 + i * 62, 70, v, 15, c, "khand") + t(14 + i * 62, 82, l, 8, MUTE) for i, (v, l, c) in enumerate([("XXX", "Members", INK), ("$XXk", "MRR", TERRA), ("Q6", "Break-even", JUNGLE)]))
            + axes(14, 96, 182, 80) + line(14, 96, 182, 80, BASE, 18, TERRA, 2) + "".join(rect(14, 196 + i * 14, [182, 150, 170, 120, 160][i], 4, "#E2DCD0") for i in range(5)))
pair("Format", "Forecast Format: A Live Dashboard With Filters, Or A One-Page Summary To Print Or Send?",
 ("fmt_dash", "Live Dashboard", "Tiles, big chart, filters on the side.", "bold",
  card("Format", TERRA, browser(14, 32, 212, 150, dash_inner(), .53) + note(196, ["Lives on the UpKeep board;", "filters change the view."]) + chips(272, ["Explore"]), example=True)),
 ("fmt_onepager", "One-Page Summary", "Three numbers, one chart, short notes; prints on one page.", "calm",
  card("Format", LAGOON, rect(60, 30, 120, 170, "#F3EFE8") + g(64, 32, .55, paper()) + rect(64, 32, 115.5, 163, "none", LINE) + note(214, ["Same data, frozen for a meeting", "or an email."]) + chips(272, ["Send-ready"]), example=True)))
# 10 key moments
pair("Key Moments", "Key Moments (Break-Even, Lowest Cash): Flags On The Chart, Or Callout Tiles Above It?",
 ("km_flags", "Flags On The Chart", "Small flags mark break-even and the lowest cash point.", "playful",
  card("Key Moments", JUNGLE, panel() + t(22, 46, "Cash balance", 9, INK, "khand") + axes(24, 56, 194, 104, ticks=Q) + line(24, 56, 194, 104, [6, 4, 2.5, 2, 3, 5, 8, 11], 12, JUNGLE, 2.4)
       + f'<path d="M{24+194*3/7:.1f} {56+104-104*2/12:.1f} V{70}" stroke="{TERRA}" stroke-width="1"/>' + rect(24 + 194 * 3 / 7, 64, 46, 12, TERRA) + t(24 + 194 * 3 / 7 + 23, 73, "Lowest cash", 7.5, "#FFFFFF", "hind", 600, "middle")
       + f'<path d="M{24+194*5/7:.1f} {56+104-104*5/12:.1f} V{88}" stroke="{JUNGLE}" stroke-width="1"/>' + rect(24 + 194 * 5 / 7 - 20, 82, 44, 12, JUNGLE) + t(24 + 194 * 5 / 7 + 2, 91, "Break-even", 7.5, "#FFFFFF", "hind", 600, "middle")
       + note(196, ["Moments sit right where", "they happen."]) + chips(272, ["In context"]), example=True)),
 ("km_tiles", "Callout Tiles Above", "Two tiles name the quarter for each moment.", "practical",
  card("Key Moments", TERRA, kpi(14, 32, 103, 40, "Q4", "Lowest cash", TERRA) + kpi(123, 32, 103, 40, "Q6", "Break-even", JUNGLE) + panel(78, 112) + axes(24, 88, 194, 84, ticks=Q) + line(24, 88, 194, 84, [6, 4, 2.5, 2, 3, 5, 8, 11], 12, JUNGLE, 2.4)
       + note(214, ["Clean chart, the moments", "read first."]) + chips(272, ["Read first"]), example=True)))
