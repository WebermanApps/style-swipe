#!/usr/bin/env python3
"""Build Style Swipe deck rulebook-clash: Rulebook Clash Deck (Oct 14 2026). One pair per conflict in 'Conflicts for Max'
(/workspace/ops/brand/dashboard-rulebook.md); C1 and C7 (three-way) get two pairs; C8 skipped (open tiebreaks, no clear two options).
Each side quotes one competing rule, with a drawn mockup. Max brand. Submit -> agent 'branding'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
DID = "rulebook-clash"
B = dict(name="Apps Home", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("rc_", "Branding")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(title="Apps Home", sub="Example dashboard", tnames=["Upkeep", "Portfolio", "WellNest", "Decks"], tn=4, report="collapsed", urgent="pill")
def quote(s, src):
    ls = wrap(s, 40); out = R(14, 222, 212, 18 + len(ls) * 10, "#FFFFFF", B["line"], 8) + R(14, 222, 3, 18 + len(ls) * 10, B["acc"][1], r=1.5)
    out += "".join(T(B, 24, 236 + i * 10, l, 7.5, B["ink"]) for i, l in enumerate(ls)) + T(B, 24, 246 + (len(ls) - 1) * 10, src, 6, B["mute"], w=600)
    return out
def wrap(s, n):
    w, l, c = s.split(), [], ""
    for x in w:
        if len(c) + len(x) + 1 > n and c: l.append(c); c = x
        else: c = (c + " " + x).strip()
    return l + [c]
def scr(order, q, src, extra="", bg="#FFFFFF", **k):
    g, _ = stack({**B, "bg": bg}, order, {**base, **k}, 10)
    return screen(g + extra + quote(q, src), bg)
def sharebtn(y, label=True): return R(64, y, 112, 24, "#FFFFFF", B["ink"], 0, 1.6) + T(B, 120, y + 15.5, "SHARE", 8, B["ink"], w=600, a="middle", ex='letter-spacing="1.2"')
FOOT = lambda y: L(14, y, 226, y, B["line"]) + T(B, 120, y + 12, "Built by Max Weberman", 6.5, B["mute"], a="middle")
# C1 Share placement
fixedbar = R(0, 196, W, 26, "#FFFFFF", B["line"]) + R(84, 200, 72, 18, "#FFFFFF", B["ink"], 0, 1.4) + T(B, 120, 212, "SHARE", 7, B["ink"], w=600, a="middle", ex='letter-spacing="1.2"') + T(B, 226, 192, "fixed", 5.5, TERRA, w=600, a="end")
inflow = sharebtn(174) + FOOT(204)
hdric = f'<g transform="translate(206,16) scale(.6)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{B["ink"]}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{B["ink"]}" stroke-width="2.2"/></g>' + FOOT(204)
G = "C1 Share Placement"
P(G, "Share: Fixed At The Bottom Or In The Page Above The Footer?",
  ("c1_fixed", "Fixed At The Bottom", "Brand guide, Oct 10.", "action", scr(["hdr", "report", "tiles"], "Share is fixed at the bottom of the screen.", "BRAND GUIDE, OCT 10", fixedbar, tn=2)),
  ("c1_flow", "In The Page, Above The Footer", "Dashboard spec, Oct 13.", "calm", scr(["hdr", "report", "tiles"], "Share sits in normal page flow just above the footer, never in a fixed bar.", "DASHBOARD SPEC, OCT 13", inflow, tn=2)))
P(G, "Share: Above The Footer Or Small Icon In The Header?",
  ("c1_flow_b", "In The Page, Above The Footer", "Dashboard spec, Oct 13.", "calm", scr(["hdr", "report", "tiles"], "Share sits in normal page flow just above the footer.", "DASHBOARD SPEC, OCT 13", inflow, tn=2)),
  ("c1_icon", "Small Icon In The Header Corner", "Your Dashboard-1 pick.", "quick", scr(["hdr", "report", "tiles"], "Small Share icon in the header corner.", "DASHBOARD-1 PICK", hdric, tn=2)))
# C2 proof sizes
def sizes(lst, q, src):
    s = T(B, 14, 28, "Test Sizes", 15, None, True)
    x = 14
    for i, (nm, w, h) in enumerate(lst):
        sc = 110 / 2560 if w > 1600 else 110 / 1600
        ww, hh = max(14, w * sc), max(20, h * sc); s += R(x, 50 + (110 - hh), ww, hh, "#FFFFFF", B["acc"][i % 4], 4, 1.4) + T(B, x + ww / 2, 176, nm, 6.5, B["ink"], w=600, a="middle"); x += ww + 10
    return screen(s + quote(q, src), "#FFFFFF")
G = "C2 Test Sizes"
P(G, "Test Sizes: 390, 768, 1440 Or 393, 1470, 2560?",
  ("c2_brand", "390 / 768 / 1440", "Brand guide sizes.", "calm", sizes([("390", 390, 844), ("768", 768, 1024), ("1440", 1440, 900)], "Check 390x844, 768x1024 and 1440x900.", "BRAND GUIDE")),
  ("c2_dash", "393 / 1470 / 2560", "Dashboard spec, Oct 13-14.", "focused", sizes([("393", 393, 852), ("1470", 1470, 956), ("2560", 2560, 1440)], "Check 393x852, MacBook about 1470, and 2560.", "DASHBOARD SPEC, OCT 13-14")))
# C3 density
G = "C3 Density"
P(G, "Density: Roomy Or Compact By Default?",
  ("c3_roomy", "Roomy, Three Big Rows", "Dashboard-1 pick (Folio board: airy).", "calm", scr(["hdr", "report", "urgent"], "Roomy, three big rows.", "DASHBOARD-1 PICK", dens=18)),
  ("c3_compact", "Practical And Compact", "App polish and layout round 1 (UpKeep board: compact).", "quick", scr(["hdr", "report", "urgent", "tiles"], "Practical and dense; tighter rhythm, compact expanding rows.", "APP POLISH, LAYOUT ROUND 1", dens=2, cols=4, th=34)))
# C4 heading case
def case(kind, q, src):
    f = {"title": lambda s: s, "caps": lambda s: s.upper()}[kind]; ex = 'letter-spacing="1.6"' if kind == "caps" else ""
    s = T(B, 14, 36, f("Apps Home"), 24 if kind != "caps" else 20, None, True, ex=ex) + L(14, 46, 226, 46, B["line"])
    for i, h in enumerate(["Waiting On Max", "Latest Open Items", "Recent Work"]):
        y = 70 + i * 48; s += T(B, 14, y, f(h), 13 if kind != "caps" else 10.5, None, True, ex=ex) + bars(2, 14, y + 10, 200, B["mute"] + "88", 8)
    return screen(s + quote(q, src), "#FFFFFF")
G = "C4 Heading Case"
P(G, "Headings: Title Case Or Spaced Caps?",
  ("c4_title", "Title Case", "Standing rule and dashboard base.", "calm", case("title", "Title Case for headings and labels.", "STANDING RULE")),
  ("c4_caps", "Spaced Caps For Some Titles", "Mix-dashboard picks.", "focused", case("caps", "Spaced caps for some titles and labels (Apps Home, Waiting On Max).", "MIX-DASHBOARD PICKS")))
# C5 bottom tabs
tabs = R(0, 186, W, 32, "#FFFFFF", B["line"]) + "".join(tile_icon(28 + i * 52, 191, i, LAGOON if i == 0 else B["mute"], 12) + T(B, 34 + i * 52, 212, n, 5.5, LAGOON if i == 0 else B["mute"], a="middle") for i, n in enumerate(["Home", "Apps", "Decks", "Feed"]))
stick = R(0, 0, W, 4, LAGOON) + FOOT(204)
G = "C5 Phone Bottom Tabs"
P(G, "Apps Home On Phone: Bottom Tab Bar Or No Bottom Bar?",
  ("c5_tabs", "Lagoon Bottom Tab Bar", "Mix-dashboard pick (bank-080).", "action", scr(["hdr", "report", "tiles"], "On phone, a bottom tab bar with lagoon accent.", "MIX PICK, BANK-080", tabs, tn=2)),
  ("c5_none", "No Bottom Bar, Slim Top Header", "Oct 13-14 standing rule.", "calm", scr(["hdr", "report", "tiles"], "No fixed or sticky bottom bars; only a slim top header may stick.", "STANDING RULE, OCT 13-14", stick, tn=2)))
# C6 report shape
G = "C6 Report Block"
P(G, "Report: One Line That Expands Or Open Card With Key Lines?",
  ("c6_line", "One Summary Line, Tap To Expand", "Layout round 1, R23 (current default).", "quick", scr(["hdr", "report", "urgent", "tiles"], "One summary line that expands on tap.", "LAYOUT ROUND 1, R23")),
  ("c6_card", "Open Card, Key Lines Plus More", "Folio and UpKeep board picks.", "focused", scr(["hdr", "report", "urgent"], "Open card with only the most important lines and a dropdown for more.", "UPKEEP AND FOLIO BOARDS", report="more", rc=SAFFRON)))
# C7 page base
def base_(bg, nm, q, src):
    s = T(B, 14, 28, "Page Base", 15, None, True, ) + T(B, 14, 40, nm, 7.5, B["mute"])
    s += R(14, 52, 212, 150, bg, B["line"], 10) + card(B, 28, 66, 184, 54) + T(B, 38, 84, "White Card", 10, None, True) + bars(2, 38, 94, 150, B["mute"] + "88", 8) + card(B, 28, 130, 184, 54) + bars(3, 38, 146, 150, B["mute"] + "88", 8)
    return screen(s + quote(q, src), "#FFFFFF")
G = "C7 Page Base"
P(G, "Page Base: Pure White Or Light Cream?",
  ("c7_white", "Pure White #FFFFFF", "UpKeep board pick.", "focused", base_("#FFFFFF", "#FFFFFF", "Pure white base for that dashboard.", "UPKEEP BOARD")),
  ("c7_cream", "Light Cream #FDFBF6", "Decks rule R58.", "calm", base_("#FDFBF6", "#FDFBF6", "#FDFBF6 cream with white cards.", "DECKS, R58")))
P(G, "Page Base: Light Cream Or WellNest Rice-White?",
  ("c7_cream_b", "Light Cream #FDFBF6", "Decks rule R58.", "calm", base_("#FDFBF6", "#FDFBF6", "#FDFBF6 cream with white cards.", "DECKS, R58")),
  ("c7_rice", "Rice-White #FBF8F1", "WellNest brand application.", "visual", base_("#FBF8F1", "#FBF8F1", "Rice-white base with WellNest logo colours.", "WELLNEST BRAND")))
# C9 accents
G = "C9 Accent Palette"
P(G, "Accents: Approve Terracotta, Lagoon, Jungle For All Dashboards?",
  ("c9_settled", "Only Where A Pick Says So", "App polish: wait for blanket approval.", "calm", AP := scr(["hdr", "report", "urgent", "tiles"], "Use terracotta, lagoon, jungle only where a settled pick says so.", "APP POLISH", tiles="lineplain", uc="#525252", rc="#525252")),
  ("c9_approve", "Approve For Every Dashboard", "Dashboard style and Oct mix picks already use them.", "visual", scr(["hdr", "report", "urgent", "tiles"], "Accents used by type on all agent dashboards.", "DASHBOARD STYLE, OCT MIX PICKS", tiles="tint")))
N = len(pairs); assert N == 10, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Rulebook Clash Deck", "Branding", pairs,
        {"brands": ["Rulebook Clash: one pair per open conflict in dashboard-rulebook.md (C1 and C7 two pairs each; C8 skipped as open tiebreaks)", "Max brand on the light cream deck page with white cards"],
         "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "section_counts": cnt, "deck_size": N,
         "trim_override": f"{N} pairs: short conflict deck per Max", "sources": {"rulebook": "/workspace/ops/brand/dashboard-rulebook.md"}},
        seed=1020, n=N)
