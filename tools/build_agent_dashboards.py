#!/usr/bin/env python3
"""Build Style Swipe deck agent-dashboards (Oct 14 2026): Agent Dashboards Deck, 20 this-or-that pairs on the
board-specific open layout and content choices of Max's agent dashboards (Scout, Blueprint, Construction, Prop,
Security, Research, Coach, Miles, Thai, Apps Home, Portfolio, WellNest). Skips everything settled in
/workspace/ops/brand/dashboard-rulebook.md (R1-R64, Settled Oct 14), the folio/upkeep/deck-board (+Details) decks,
and C7/C8 (Tiebreak deck). No live/customer apps. Pattern copied from build_info_gather.py (team_kit.publish, dash_kit).
Routing: /workspace/ops/brand/agent-dashboards-routing.md. Submit -> agent 'branding'. Drawn example mockups only."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, chev, phone, poly, wave, bars
DID = "agent-dashboards"
B = dict(name="Agent", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=6, hw=600)
INK, MUTE, LN = B["ink"], B["mute"], B["line"]; ACC = B["acc"]
pairs, O, add = deck("ad_", "Agent Dashboards")
ROUTE = []
def P(agent, ask, a, b): ROUTE.append(agent); add(agent, agent, O(*a), O(*b), ask)
def tx(x, y, s, sz=7, c=INK, h=False, w=None, a="start"): return T(B, x, y, s, sz, c, h, w, a)
def share(x, y): return f'<g transform="translate({x},{y}) scale(.5)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{INK}" stroke-width="2.2"/></g>'
def card(x, y, w, h, edge=None): return R(x, y, w, h, "#FFFFFF", LN, B["r"]) + (R(x, y, 3, h, edge, r=1.5) if edge else "")
def ln(x, y, w, c=MUTE + "77"): return R(x, y, w, 3, c, r=1.5)
def sec(y, s): return tx(14, y, s, 9.5, INK, True)
def frame(name, body, c=TERRA):
    """Top bar (Apps Home, name, Updated, Share icon), body drawn from y=40, footer."""
    s = R(0, 0, W, 30, "#FFFFFF") + L(0, 30, W, 30, LN) + chev(14, 15, MUTE).replace(f'M10 13', 'M10 13') + tx(20, 18, "Apps Home", 5.5, MUTE, w=600)
    s += tx(120, 19, name, 11, INK, True, a="middle") + share(208, 9) + D(64, 15, 2.5, c)
    s += body + tx(120, 293, "Built by Machan", 5, "#8A8580", a="middle")
    return phone(B, s)
def rows(y, items, edge=None, h=22, right=None):
    s = ""
    for i, it in enumerate(items):
        yy = y + i * (h + 4); s += card(14, yy, 212, h, edge or ACC[i % 4]) + tx(24, yy + h / 2 + 2.5, it, 7, INK, w=600)
        if right: s += tx(218, yy + h / 2 + 2.5, right[i % len(right)], 6, MUTE, a="end")
    return s
def ring(cx, cy, r, f, c):
    import math
    a = f * 2 * math.pi - math.pi / 2
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LN}" stroke-width="4"/><path d="M{cx} {cy-r} A{r} {r} 0 {1 if f>.5 else 0} 1 {cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
def hbar(x, y, w, f, c): return R(x, y, w, 5, LN, r=2.5) + R(x, y, w * f, 5, c, r=2.5)
def thumb(x, y, w, h, c, lab=""): return R(x, y, w, h, c + "26", r=4) + R(x + 5, y + h - 14, w * .6, 4, c, r=2) + (tx(x + 5, y + 10, lab, 5.5, INK, w=600) if lab else "")
def chips(y, items, sel=0):
    s, x = "", 14
    for i, n in enumerate(items):
        w = len(n) * 3.6 + 14; s += R(x, y, w, 14, (LAGOON if i == sel else "#FFFFFF"), LN, 7) + tx(x + w / 2, y + 9.5, n, 6, "#FFFFFF" if i == sel else INK, w=600, a="middle"); x += w + 4
    return s
# ===================== Scout =====================
P("Scout", "Scout Publish-Time Test: Winner Card Or Side-By-Side Bars?",
  ("sc_win", "Winner Card", "One card: best slot so far, with the views lift.", "focused",
   frame("Scout", sec(52, "Publish-Time Test") + card(14, 60, 212, 64, JUNGLE) + tx(24, 78, "BEST SO FAR", 5.5, JUNGLE, w=600) + tx(24, 98, "Tue 7:00 PM", 16, INK, True) + tx(24, 112, "Example: +18% views vs other slots", 6, MUTE) + sec(146, "Channel Stats") + rows(154, ["Example stat row", "Example stat row"]), LAGOON)),
  ("sc_bars", "Side-By-Side Bars", "Every slot tested, as bars, best one coloured.", "visual",
   frame("Scout", sec(52, "Publish-Time Test") + card(14, 60, 212, 96) + "".join(R(30 + i * 38, 140 - v, 22, v, JUNGLE if i == 2 else LAGOON + "55", r=2) + tx(41 + i * 38, 150, n, 5.5, MUTE, a="middle") for i, (n, v) in enumerate([("9 AM", 30), ("Noon", 44), ("7 PM", 66), ("9 PM", 40), ("Late", 22)])) + sec(178, "Channel Stats") + rows(186, ["Example stat row", "Example stat row"]), LAGOON)))
P("Scout", "Scout Style C Thumbnails: Three-Up Grid Or One Big With A Strip?",
  ("sc_grid", "Three-Up Grid", "All thumbnails the same size.", "calm",
   frame("Scout", sec(52, "Style C Thumbnails") + "".join(thumb(14 + (i % 3) * 72, 60 + (i // 3) * 48, 68, 44, ACC[i % 4], f"Idea {i+1}") for i in range(6)) + sec(176, "30-Day Plan") + rows(184, ["Short idea one", "Short idea two"]), LAGOON)),
  ("sc_big", "One Big With A Strip", "Newest thumbnail large, the rest small below.", "visual",
   frame("Scout", sec(52, "Style C Thumbnails") + thumb(14, 60, 212, 100, TERRA, "Newest") + "".join(thumb(14 + i * 54, 166, 50, 30, ACC[(i + 1) % 4]) for i in range(4)) + sec(216, "30-Day Plan") + rows(224, ["Short idea one", "Short idea two"]), LAGOON)))
# ===================== Blueprint =====================
P("Blueprint", "Blueprint Header: House Picture Banner Or Plain Title?",
  ("bp_pic", "House Picture Banner", "Drawn house banner behind Weberman Residence.", "warm",
   frame("Blueprint", R(14, 40, 212, 70, SAFFRON + "22", r=6) + f'<path d="M90 100 L120 66 L150 100 Z" fill="none" stroke="{INK}" stroke-width="1.6"/><rect x="100" y="84" width="40" height="16" fill="none" stroke="{INK}" stroke-width="1.6"/>' + tx(22, 56, "Weberman Residence", 12, INK, True) + sec(130, "Decisions For You") + rows(138, ["Example decision", "Example decision"]) + sec(200, "Water Systems") + rows(208, ["Example item"]), SAFFRON)),
  ("bp_plain", "Plain Title", "Name and address only, straight into decisions.", "focused",
   frame("Blueprint", tx(14, 60, "Weberman Residence", 16, INK, True) + tx(14, 72, "Example address line", 6.5, MUTE) + sec(96, "Decisions For You") + rows(104, ["Example decision", "Example decision", "Example decision"]) + sec(196, "Water Systems") + rows(204, ["Example item"]), SAFFRON)))
P("Blueprint", "Blueprint Water Systems: Drawn Diagram Or Item List?",
  ("bp_dia", "Drawn Diagram", "Simple line drawing: main, heater, softener, fixtures.", "visual",
   frame("Blueprint", sec(52, "Water Systems") + card(14, 60, 212, 130) + "".join(R(x, 110, 36, 22, c + "22", c, 4) + tx(x + 18, 124, n, 5.5, INK, w=600, a="middle") for x, n, c in [(24, "Main", LAGOON), (74, "Softener", JUNGLE), (124, "Heater", TERRA), (174, "Fixtures", SAFFRON)]) + "".join(L(60 + i * 50, 121, 74 + i * 50, 121, INK, 1.4) for i in range(3)) + tx(24, 80, "Tap a part for its details", 6, MUTE), SAFFRON)),
  ("bp_list", "Item List", "One row per part, details on tap.", "focused",
   frame("Blueprint", sec(52, "Water Systems") + rows(60, ["Main Shutoff", "Water Softener", "Water Heater", "Fixtures"], right=["Basement", "Basement", "Garage", "All Floors"]), SAFFRON)))
# ===================== Construction =====================
P("Construction", "Construction Close-Out: Checklist With Percent Or Step Timeline?",
  ("cn_check", "Checklist With Percent", "Big percent, then the remaining items.", "focused",
   frame("Construction", sec(52, "Hidden Valley Close-Out") + card(14, 60, 212, 120) + tx(24, 92, "72%", 22, JUNGLE, True) + hbar(80, 84, 136, .72, JUNGLE) + "".join(f'<rect x="24" y="{106+i*18}" width="8" height="8" rx="2" fill="{JUNGLE if i<2 else "none"}" stroke="{JUNGLE}"/>' + ln(38, 108 + i * 18, 120) for i in range(4)), TERRA)),
  ("cn_time", "Step Timeline", "Stages on a line: done, now, next.", "calm",
   frame("Construction", sec(52, "Hidden Valley Close-Out") + card(14, 60, 212, 120) + L(30, 72, 30, 168, LN, 2) + "".join(D(30, 76 + i * 30, 5, [JUNGLE, JUNGLE, TERRA, LN][i]) + tx(42, 79 + i * 30, n, 7.5, INK, w=600) + tx(216, 79 + i * 30, t, 6, MUTE, a="end") for i, (n, t) in enumerate([("Punch List", "Done"), ("Final Clean", "Done"), ("Walk With Owner", "Now"), ("Hand Over Keys", "Next")])), TERRA)))
P("Construction", "Construction Apps: One Row Of Nine Or Two Groups?",
  ("cn_row", "One Long Row", "All nine apps in one strip of icon tiles.", "quick",
   frame("Construction", sec(52, "Apps") + "".join(R(14 + (i % 5) * 43, 60 + (i // 5) * 44, 39, 40, ACC[i % 4] + "1F", r=6) + D(33.5 + (i % 5) * 43, 76 + (i // 5) * 44, 6, ACC[i % 4]) for i in range(9)) + sec(170, "Today") + rows(178, ["Example item", "Example item"]), TERRA)),
  ("cn_grp", "Two Groups", "Home Guide and Site Walk, then the swipe and quiz apps.", "focused",
   frame("Construction", tx(14, 52, "FOR THE JOB", 5.5, MUTE, w=600) + "".join(R(14 + i * 43, 58, 39, 36, TERRA + "1F", r=6) + D(33.5 + i * 43, 76, 6, TERRA) for i in range(4)) + tx(14, 110, "SWIPES AND QUIZZES", 5.5, MUTE, w=600) + "".join(R(14 + i * 43, 116, 39, 36, LAGOON + "1F", r=6) + D(33.5 + i * 43, 134, 6, LAGOON) for i in range(5)) + sec(176, "Today") + rows(184, ["Example item", "Example item"]), TERRA)))
# ===================== Prop =====================
P("Prop", "Prop Properties: One Card Each Or A Single Table?",
  ("pr_cards", "One Card Each", "A card per property with its next step.", "warm",
   frame("Prop", sec(52, "Properties") + "".join(card(14, 60 + i * 50, 212, 44, ACC[i]) + tx(24, 76 + i * 50, f"Example Property {i+1}", 8.5, INK, True) + ln(24, 84 + i * 50, 130) + tx(216, 76 + i * 50, "Next step", 6, MUTE, a="end") for i in range(3)), JUNGLE)),
  ("pr_table", "Single Table", "Every property on one line: rent, tenant, next step.", "focused",
   frame("Prop", sec(52, "Properties") + card(14, 60, 212, 110) + "".join(tx(x, 74, h, 5.5, MUTE, w=600) for x, h in [(22, "PROPERTY"), (110, "RENT"), (160, "NEXT")]) + "".join(L(22, 80 + i * 22, 218, 80 + i * 22, LN) + tx(22, 94 + i * 22, f"Property {i+1}", 7, INK, w=600) + ln(110, 90 + i * 22, 30) + ln(160, 90 + i * 22, 44) for i in range(4)), JUNGLE)))
P("Prop", "Prop Routines: Week Strip Or Plain List?",
  ("pr_week", "Week Strip", "Seven days across, dots on days with a routine.", "visual",
   frame("Prop", sec(52, "Routines") + "".join(R(14 + i * 30.5, 60, 27, 40, (JUNGLE + "1F" if i == 2 else "#FFFFFF"), LN, 5) + tx(27.5 + i * 30.5, 73, d, 6, MUTE, w=600, a="middle") + (D(27.5 + i * 30.5, 88, 3, JUNGLE) if i in (0, 2, 4) else "") for i, d in enumerate("MTWTFSS")) + sec(124, "Decisions Max Owes") + rows(132, ["Example decision"]), JUNGLE)),
  ("pr_list", "Plain List", "One row per routine with its day.", "focused",
   frame("Prop", sec(52, "Routines") + rows(60, ["Rent Check", "Tenant Follow-Up", "Weekly Summary"], right=["Mon", "Wed", "Fri"]) + sec(150, "Decisions Max Owes") + rows(158, ["Example decision"]), JUNGLE)))
# ===================== Security =====================
P("Security", "Security Exposure Overview: Six Area Tiles Or One Risk Meter?",
  ("se_tiles", "Six Area Tiles", "Code, Passwords, Money, Customer Data, Legal, Shared Computer.", "focused",
   frame("Security", sec(52, "Exposure Overview") + "".join(card(14 + (i % 2) * 109, 60 + (i // 2) * 40, 103, 34) + D(26 + (i % 2) * 109, 77 + (i // 2) * 40, 4, [JUNGLE, SAFFRON, JUNGLE, TERRA, JUNGLE, SAFFRON][i]) + tx(34 + (i % 2) * 109, 80 + (i // 2) * 40, n, 7, INK, w=600) for i, n in enumerate(["Code And Repos", "Passwords", "Financial", "Customer Data", "Legal And IP", "Shared Computer"])), INK)),
  ("se_meter", "One Risk Meter", "One overall gauge, areas listed under it.", "calm",
   frame("Security", sec(52, "Exposure Overview") + card(14, 60, 212, 90) + f'<path d="M70 130 A50 50 0 0 1 170 130" fill="none" stroke="{LN}" stroke-width="8"/><path d="M70 130 A50 50 0 0 1 135 83" fill="none" stroke="{SAFFRON}" stroke-width="8"/>' + tx(120, 128, "Medium", 11, INK, True, a="middle") + rows(158, ["Customer Data", "Passwords"], right=["Needs work", "In progress"]), INK)))
P("Security", "Security 2FA Checklist: Progress Ring Or Ticked List Only?",
  ("se_ring", "Progress Ring", "Ring with the count, then what's left.", "visual",
   frame("Security", sec(52, "2FA Checklist") + card(14, 60, 212, 70) + ring(50, 95, 20, .6, JUNGLE) + tx(50, 98, "6/10", 7, INK, True, a="middle") + tx(84, 88, "Four Accounts Left", 9, INK, True) + ln(84, 98, 110) + rows(140, ["Example account", "Example account"]), INK)),
  ("se_list", "Ticked List Only", "Every account, ticked or not, no ring.", "focused",
   frame("Security", sec(52, "2FA Checklist") + "".join(card(14, 60 + i * 24, 212, 20) + f'<rect x="22" y="{66+i*24}" width="8" height="8" rx="2" fill="{JUNGLE if i<3 else "none"}" stroke="{JUNGLE}"/>' + ln(36, 68 + i * 24, 120, INK + "55") for i in range(6)), INK)))
# ===================== Research =====================
P("Research", "Research Suggestions: Vote Cards Or Ranked List?",
  ("rs_vote", "Vote Cards", "Each suggestion a card with Yes / Later buttons.", "warm",
   frame("Research", sec(52, "Research Suggestions") + "".join(card(14, 60 + i * 54, 212, 48, LAGOON) + tx(24, 76 + i * 54, f"Example Suggestion {i+1}", 8.5, INK, True) + R(24, 86 + i * 54, 40, 14, LAGOON, r=7) + tx(44, 95.5 + i * 54, "Yes", 6, "#FFFFFF", w=600, a="middle") + R(70, 86 + i * 54, 40, 14, "#FFFFFF", LN, 7) + tx(90, 95.5 + i * 54, "Later", 6, INK, w=600, a="middle") for i in range(3)), LAGOON)),
  ("rs_rank", "Ranked List", "Numbered by value, one vote button for the full list.", "focused",
   frame("Research", sec(52, "Research Suggestions") + "".join(card(14, 60 + i * 26, 212, 22) + tx(24, 74.5 + i * 26, str(i + 1), 9, LAGOON, True) + ln(38, 70 + i * 26, 130, INK + "55") for i in range(5)) + R(14, 196, 212, 20, LAGOON, r=6) + tx(120, 209, "Vote On The Full List", 7, "#FFFFFF", w=600, a="middle"), LAGOON)))
P("Research", "Research Recent Days: Calendar Dots Or Date Rows?",
  ("rs_cal", "Calendar Dots", "A month grid, a dot on each research day.", "visual",
   frame("Research", sec(52, "Recent Research Days") + card(14, 60, 212, 110) + "".join(D(30 + (i % 7) * 30, 76 + (i // 7) * 20, 3.5 if i % 3 else 2, LAGOON if i % 3 else LN) for i in range(35)), LAGOON)),
  ("rs_rows", "Date Rows", "Topic on the left, date on the right.", "focused",
   frame("Research", sec(52, "Recent Research Days") + rows(60, ["Example topic", "Example topic", "Example topic", "Example topic"], right=["Oct 14", "Oct 13", "Oct 12", "Oct 11"]), LAGOON)))
# ===================== Coach =====================
P("Coach", "Coach Suggestions: Equal Numbered Cards Or One Lead Plus A List?",
  ("co_eq", "Equal Numbered Cards", "Each suggestion the same size, numbered.", "calm",
   frame("Coach", sec(52, "Top Coaching Suggestions") + "".join(card(14 + (i % 2) * 109, 60 + (i // 2) * 56, 103, 50) + tx(22 + (i % 2) * 109, 78 + (i // 2) * 56, str(i + 1), 12, TERRA, True) + ln(22 + (i % 2) * 109, 88 + (i // 2) * 56, 80, INK + "55") + ln(22 + (i % 2) * 109, 96 + (i // 2) * 56, 60) for i in range(4)), TERRA)),
  ("co_lead", "One Lead Plus A List", "Top suggestion big, the rest as rows.", "focused",
   frame("Coach", sec(52, "Top Coaching Suggestions") + card(14, 60, 212, 60, TERRA) + tx(24, 78, "TOP PICK", 5.5, TERRA, w=600) + tx(24, 96, "One Rulebook For Dashboards", 10, INK, True) + ln(24, 106, 150) + rows(128, ["Suggestion two", "Suggestion three", "Suggestion four"], edge=LN), TERRA)))
P("Coach", "Coach Routines: Schedule Table Or Rows With Last Run?",
  ("co_tab", "Schedule Table", "Routine, time, how often.", "focused",
   frame("Coach", sec(52, "Routines") + card(14, 60, 212, 112) + "".join(tx(x, 74, h, 5.5, MUTE, w=600) for x, h in [(22, "ROUTINE"), (140, "TIME"), (182, "OFTEN")]) + "".join(L(22, 80 + i * 22, 218, 80 + i * 22, LN) + ln(22, 90 + i * 22, 90, INK + "55") + tx(140, 94 + i * 22, ["5:00", "18:00", "Mon", "Sun"][i], 6.5, INK) + tx(182, 94 + i * 22, ["Daily", "Daily", "Weekly", "Weekly"][i], 6.5, INK) for i in range(4)), TERRA)),
  ("co_last", "Rows With Last Run", "Green dot if it ran on time, the last run time on the right.", "calm",
   frame("Coach", sec(52, "Routines") + "".join(card(14, 60 + i * 26, 212, 22) + D(24, 71 + i * 26, 3, [JUNGLE, JUNGLE, SAFFRON, JUNGLE][i]) + ln(32, 69 + i * 26, 100, INK + "55") + tx(218, 73.5 + i * 26, ["Ran 5:00", "Ran 18:00", "Late", "Ran Sun"][i], 6, MUTE, a="end") for i in range(4)), TERRA)))
# ===================== Miles =====================
P("Miles Agent", "Miles Top: Points Balances Strip Or Next Trip Card?",
  ("mi_pts", "Points Balances Strip", "Each program's balance across the top.", "quick",
   frame("Miles", sec(52, "Balances") + "".join(card(14 + i * 72, 60, 68, 44) + tx(20 + i * 72, 74, n, 5.5, MUTE, w=600) + ln(20 + i * 72, 86, 44, INK + "88") for i, n in enumerate(["PROGRAM A", "PROGRAM B", "PROGRAM C"])) + sec(126, "Open Items") + rows(134, ["Example item", "Example item"]), LAGOON)),
  ("mi_trip", "Next Trip Card", "Next trip first, with what to book.", "warm",
   frame("Miles", card(14, 44, 212, 70, LAGOON) + tx(24, 60, "NEXT TRIP", 5.5, LAGOON, w=600) + tx(24, 80, "Example City", 14, INK, True) + ln(24, 92, 120) + tx(24, 106, "2 things to book", 6.5, TERRA, w=600) + sec(136, "Open Items") + rows(144, ["Example item", "Example item"]), LAGOON)))
# ===================== Thai =====================
P("Thai", "Thai Top: Start Today's Quiz Button Or Word Of The Day Card?",
  ("th_quiz", "Start Quiz Button", "One big button into today's practice.", "quick",
   frame("Thai", R(14, 44, 212, 40, JUNGLE, r=8) + tx(120, 68, "Start Today's Quiz", 11, "#FFFFFF", True, a="middle") + sec(106, "Study Apps") + rows(114, ["Example app", "Example app"]) + sec(178, "Status") + rows(186, ["Example status"]), JUNGLE)),
  ("th_word", "Word Of The Day Card", "A word with its meaning, quiz link under it.", "warm",
   frame("Thai", card(14, 44, 212, 70, JUNGLE) + tx(24, 60, "WORD OF THE DAY", 5.5, JUNGLE, w=600) + f'<text x="24" y="86" font-size="18" font-family="Noto Sans Thai, sans-serif" fill="{INK}">&#3626;&#3623;&#3633;&#3626;&#3604;&#3637;</text>' + tx(24, 102, "hello  (example)", 6.5, MUTE) + tx(216, 102, "Start Quiz", 6.5, JUNGLE, w=600, a="end") + sec(136, "Study Apps") + rows(144, ["Example app", "Example app"]), JUNGLE)))
P("Thai", "Thai Daily Tip Patterns: Example Sentence Cards Or Pattern Table?",
  ("th_cards", "Example Sentence Cards", "Each pattern with one example sentence.", "warm",
   frame("Thai", sec(52, "Daily Tip Patterns So Far") + "".join(card(14, 60 + i * 50, 212, 44, ACC[i]) + tx(24, 76 + i * 50, f"Pattern {i+1}", 8.5, INK, True) + ln(24, 86 + i * 50, 150) + ln(24, 94 + i * 50, 100) for i in range(3)), JUNGLE)),
  ("th_table", "Pattern Table", "Pattern, meaning, day learned on one row.", "focused",
   frame("Thai", sec(52, "Daily Tip Patterns So Far") + card(14, 60, 212, 132) + "".join(tx(x, 74, h, 5.5, MUTE, w=600) for x, h in [(22, "PATTERN"), (100, "MEANING"), (184, "DAY")]) + "".join(L(22, 80 + i * 22, 218, 80 + i * 22, LN) + ln(22, 90 + i * 22, 60, INK + "55") + ln(100, 90 + i * 22, 70) + tx(184, 94 + i * 22, f"Oct {14-i}", 6.5, INK) for i in range(5)), JUNGLE)))
# ===================== Apps Home (Grok Bot) =====================
P("Apps Home (Grok Bot)", "Apps Home Agents: Grouped By Area Or Ordered By Most Waiting?",
  ("ah_area", "Grouped By Area", "Money, Home, Brand, Learning, each a small group.", "calm",
   frame("Apps Home", "".join(tx(14, 52 + g * 58, n, 5.5, MUTE, w=600) + "".join(R(14 + i * 54, 58 + g * 58, 50, 44, ACC[g] + "1F", r=6) + D(39 + i * 54, 74 + g * 58, 6, ACC[g]) + ln(24 + i * 54, 90 + g * 58, 30, INK + "55") for i in range(4)) for g, n in enumerate(["MONEY", "HOME", "BRAND", "LEARNING"])), LAGOON)),
  ("ah_wait", "Most Waiting First", "Agents with the most waiting on Max come first, with a count.", "focused",
   frame("Apps Home", "".join(card(14, 44 + i * 30, 212, 26, ACC[i % 4]) + ln(24, 55 + i * 30, 90, INK + "55") + R(186, 50 + i * 30, 22, 13, TERRA, r=6.5) + tx(197, 59 + i * 30, str(5 - i), 6.5, "#FFFFFF", w=600, a="middle") for i in range(5)) + tx(14, 210, "NOTHING WAITING", 5.5, MUTE, w=600) + "".join(R(14 + i * 54, 216, 50, 30, LN + "88", r=6) for i in range(4)), LAGOON)))
# ===================== Portfolio =====================
P("Portfolio", "Portfolio Dashboards Section: Icon Row Or Rows With A Line Each?",
  ("pf_icons", "Icon Row", "Each linked dashboard as a small icon tile.", "quick",
   frame("Portfolio", sec(52, "Dashboards") + "".join(R(14 + i * 54, 60, 50, 44, ACC[i] + "1F", r=6) + D(39 + i * 54, 76, 6, ACC[i]) + ln(24 + i * 54, 92, 30, INK + "55") for i in range(4)) + sec(126, "Open Items") + rows(134, ["Example item", "Example item"]), TERRA)),
  ("pf_rows", "Rows With A Line Each", "Name plus one line of what it shows.", "focused",
   frame("Portfolio", sec(52, "Dashboards") + "".join(card(14, 60 + i * 30, 212, 26, ACC[i]) + tx(24, 72 + i * 30, n, 7.5, INK, w=600) + ln(24, 77 + i * 30, 110) for i, n in enumerate(["Investments", "Spending", "Taxes"])) + sec(170, "Open Items") + rows(178, ["Example item"]), TERRA)))
# ===================== WellNest =====================
P("WellNest", "WellNest Team Chat: Inline Panel Or A Tile That Opens It?",
  ("wn_inline", "Inline Panel", "Last three messages shown right on the board.", "warm",
   frame("WellNest", sec(52, "Recent Work") + rows(60, ["Example item", "Example item"]) + sec(128, "Team Chat") + card(14, 136, 212, 96) + "".join(R(24 if i % 2 == 0 else 90, 144 + i * 28, 126, 22, (SAFFRON + "22" if i % 2 == 0 else "#F3F1EC"), r=8) + ln(32 if i % 2 == 0 else 98, 154 + i * 28, 100, INK + "55") for i in range(3)), SAFFRON)),
  ("wn_tile", "Tile That Opens It", "One tile with an unread count; chat opens on tap.", "calm",
   frame("WellNest", sec(52, "Recent Work") + rows(60, ["Example item", "Example item"]) + sec(128, "Team Chat") + card(14, 136, 212, 34) + D(30, 153, 7, SAFFRON + "44") + tx(44, 156, "Open Team Chat", 8, INK, True) + R(186, 147, 22, 13, TERRA, r=6.5) + tx(197, 156, "3", 6.5, "#FFFFFF", w=600, a="middle"), SAFFRON)))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Agent Dashboards Deck", "Agent Dashboards", pairs,
        {"brands": ["Agent Dashboards: board-specific open layout and content choices across Scout, Blueprint, Construction, Prop, Security, Research, Coach, Miles, Thai, Apps Home, Portfolio and WellNest",
                    "White page (beige #FAF6EE accents), white cards, Khand/Hind, terracotta/lagoon/jungle/saffron accents; skips everything settled in the Dashboard Rulebook (R1-R64) and earlier board decks"],
         "submit_agent": "branding", "submit_to": "Branding Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "routing": "/workspace/ops/brand/agent-dashboards-routing.md"},
        seed=1415, n=N)
import json
d = json.load(open(f"decks/{DID}.json"))
open("/tmp/ad_route.json", "w").write(json.dumps([{"n": i + 1, "id": p["id"] if "id" in p else "", "ask": p["ask"], "group": p.get("group")} for i, p in enumerate(d["pairs"])]))
