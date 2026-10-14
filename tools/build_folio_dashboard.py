#!/usr/bin/env python3
"""Build Style Swipe deck folio-dashboard (Oct 14 2026): Folio Dashboard Deck, 20 pairs on how Portfolio's dashboard
(https://webermanapps.github.io/portfolio-dashboard/, source /workspace/ops/folio/dashboard) is presented.
Drawn SVG mockups via dash_kit; shapes only, no figures, nothing from the locked /s/ pages. Submit -> agent 'portfolio'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE
from dash_kit import *
DID = "folio-dashboard"
B = dict(name="Portfolio", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("fd_", "Portfolio")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(sub="Example layout, shapes only")
def M(order, **k): return mock(B, order, **{**base, **k})
TOP = ["hdr", "report", "urgent", "tiles"]
P("Hero And Header", "Header: Plain Title Or Greeting Eyebrow?",
  ("hero_plain", "Plain Title", "Name and a thin rule.", "calm", M(TOP)),
  ("hero_eyebrow", "Greeting Eyebrow", "Small terracotta greeting above the name.", "visual", M(TOP, hdr="eyebrow", sub="Good Morning, Max")))
P("Hero And Header", "Header: Big Title Or Colour Band?",
  ("hero_big", "Big Title, Short Rule", "Large Khand title, terracotta underline.", "focused", M(TOP, hdr="big")),
  ("hero_band", "Lagoon Header Band", "White title on a lagoon band.", "visual", M(TOP, hdr="band", hc=LAGOON)))
P("Morning And Evening Report", "Report Block: Card Or Side-Stripe Banner?",
  ("rep_card", "Report Card", "A white card with a few lines.", "calm", M(["hdr", "report", "tiles"])),
  ("rep_banner", "Stripe Banner", "Lagoon tint with a left stripe.", "visual", M(["hdr", "report", "tiles"], report="banner")))
P("Morning And Evening Report", "Report: Morning/Evening Tabs Or One Big Card?",
  ("rep_tabs", "Morning / Evening Tabs", "Switch between both reports.", "action", M(["hdr", "report", "tiles"], report="tabs")),
  ("rep_bigone", "One Big Card", "Shows whichever report is current.", "focused", M(["hdr", "report", "tiles"], report="big", rname="Evening Report")))
P("Morning And Evening Report", "Report Placement: Top Or Below The Tiles?",
  ("rep_top", "Report First", "Read the report, then tiles.", "focused", M(["hdr", "report", "tiles"], report="collapsed", tn=6)),
  ("rep_below", "Tiles First", "Tiles up top, report below.", "quick", M(["hdr", "tiles", "report"], tn=6)))
P("Tiles And Tap-To-Unlock", "Tile Grid: Two Columns Or Three?",
  ("tile_2", "Two Columns", "Bigger tiles, outlined.", "calm", M(["hdr", "tiles", "feed"], locked="icon")),
  ("tile_3", "Three Columns, Tinted", "Smaller tinted tiles.", "quick", M(["hdr", "tiles", "feed"], cols=3, tiles="tint", locked="icon")))
P("Tiles And Tap-To-Unlock", "Locked Tiles: Small Lock Or Frosted Cover?",
  ("lock_icon", "Small Corner Lock", "Tile stays readable, lock in the corner.", "calm", M(["hdr", "tiles"], locked="icon", th=54)),
  ("lock_frost", "Frosted Cover", "Tile faded with a centred lock.", "focused", M(["hdr", "tiles"], locked="frost", th=54)))
P("Tiles And Tap-To-Unlock", "Tiles: Solid Colour Blocks Or A List?",
  ("tile_solid", "Solid Colour Tiles", "Bold blocks in the three accents.", "visual", M(["hdr", "tiles"], tiles="solid", locked="icon", th=50)),
  ("tile_rows", "List Rows", "One row per area, chevron to open.", "quick", M(["hdr", "tiles"], tiles="row", locked="icon")))
P("Urgent Items Dropdown", "Urgent Items: Collapsed Card Or Small Pill?",
  ("urg_card", "Collapsed Card", "Terracotta stripe, count, chevron.", "focused", M(["hdr", "urgent", "report", "tiles"], tn=4)),
  ("urg_pill", "Small Pill", "A quiet pill that opens a list.", "calm", M(["hdr", "urgent", "report", "tiles"], urgent="pill", tn=4)))
P("Urgent Items Dropdown", "Urgent Items: Collapsed Or Open By Default?",
  ("urg_closed", "Closed Until Tapped", "Count only, tap to see.", "calm", M(["hdr", "urgent", "tiles"], tn=4)),
  ("urg_openlist", "Open List", "Items shown right away.", "action", M(["hdr", "urgent", "tiles"], urgent="open", tn=4)))
CH = ["hdr", "chart", "tiles"]
P("Portfolio Chart", "Chart: Line With Dashed Averages Or Filled Area?",
  ("ch_line", "Line, Dashed 100/200-Day", "Thin line, dashed moving averages.", "focused", M(CH, ch=130, tn=2)),
  ("ch_area", "Soft Area, Solid Averages", "Filled area, solid average lines.", "visual", M(CH, chart="area", sma="solid", ch=130, tn=2)))
P("Portfolio Chart", "Average Labels: Legend On Top Or At Line Ends?",
  ("ch_legtop", "Legend On Top", "Dots and names above the chart.", "calm", M(CH, ch=130, tn=2, seed=3)),
  ("ch_legend", "Labels At Line Ends", "Small tags where each line ends, light grid.", "focused", M(CH, ch=130, tn=2, seed=3, legend="end", grid=True)))
P("Portfolio Chart", "Chart: Range Buttons Or Clean?",
  ("ch_range", "Range Buttons", "Pick a time span under the chart.", "action", M(CH, ch=140, tn=2, seed=5, range=True, sma="thick")),
  ("ch_clean", "Clean, No Controls", "Just the lines.", "calm", M(CH, ch=140, tn=2, seed=5, chart="step")))
SP = ["hdr", "spend", "tiles"]
P("Spending Chart", "Spending: Monthly Bars Or Donut?",
  ("sp_bars", "Monthly Bars", "Current month in solid lagoon.", "focused", M(SP, sh=110, tn=4)),
  ("sp_donut", "Category Donut", "Share by category, named.", "visual", M(SP, spend="donut", sh=110, tn=4)))
P("Spending Chart", "Spending: Category Bars Or One Stacked Strip?",
  ("sp_hbars", "Category Bars", "One bar per category.", "quick", M(SP, spend="hbars", sh=96, tn=4)),
  ("sp_stack", "Stacked Strip", "One strip, colour per category.", "calm", M(SP, spend="stack", sh=70, tn=4)))
def typo(upper):
    s = T(B, 14, 34, "PORTFOLIO" if upper else "Portfolio", 26, B["ink"], True, ex='letter-spacing="2"' if upper else "")
    s += T(B, 14, 50, "Example layout, shapes only", 8, B["mute"]) + L(14, 60, 226, 60, B["line"])
    for i, h in enumerate(["Morning Report", "Urgent", "Investments"]):
        y = 84 + i * 66; s += T(B, 14, y, h.upper() if upper else h, 14 if not upper else 11, B["ink"], True, ex='letter-spacing="1.5"' if upper else "") + bars(3, 14, y + 10, 200, B["mute"] + "88", 8)
    return phone(B, s)
P("Typography", "Khand Headings: Title Case Or Spaced Capitals?",
  ("ty_title", "Title Case Khand", "Hind body, Khand headings as written.", "calm", typo(False)),
  ("ty_caps", "Spaced Capitals", "Khand in tracked capitals.", "focused", typo(True)))
P("Colour Accents", "Accents: Terracotta Leads Or Lagoon Leads?",
  ("col_terra", "Terracotta Leads", "Terracotta pops, lagoon and green small.", "visual", M(["hdr", "urgent", "report", "tiles"], hdr="eyebrow", sub="Good Evening, Max", rc=TERRA, uc=TERRA, tn=4)),
  ("col_lagoon", "Lagoon Leads", "Lagoon pops, terracotta only for urgent.", "calm", M(["hdr", "urgent", "report", "tiles"], hdr="eyebrow", sub="Good Evening, Max", rc=LAGOON, report="banner", tn=4, tiles="tint")))
P("Density", "Density: Airy Or Compact?",
  ("dn_airy", "Airy", "Fewer items, more white space.", "calm", M(["hdr", "report", "urgent", "tiles"], dens=14, tn=4, th=50)),
  ("dn_compact", "Compact", "More on one screen.", "quick", M(["hdr", "report", "urgent", "tiles", "feed"], dens=3, cols=3, tn=6, th=36, report="line")))
P("Big Monitor Vs Phone", "Big Monitor: Three Columns Or Centred Two?",
  ("bm_three", "Three Columns", "Report, tiles and charts side by side.", "visual", desk(B, [["hdr", "report", "urgent"], ["tiles"], ["chart", "spend"]], note="Phone stacks the same blocks in one column", **base)),
  ("bm_two", "Centred Two Columns", "Wider margins, two columns.", "calm", desk(B, [["hdr", "report", "urgent", "feed"], ["chart", "tiles"]], note="Phone stacks the same blocks in one column", **base)))
P("Unlock Screen", "Unlock Screen: Centred Card Or Colour Band?",
  ("ul_center", "Centred Lock", "Lock, short line, password, button.", "calm", mock(B, ["unlock"], y0=30)),
  ("ul_split", "Soft Band On Top", "Terracotta tint band with the lock.", "visual", mock(B, ["unlock"], y0=0, unlock="split")))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Folio Dashboard Deck", "Portfolio", pairs,
        {"brands": ["Portfolio dashboard presentation: hero, Morning/Evening Report, tiles and tap-to-unlock, urgent dropdown, chart with 100/200-day averages, spending chart, type, colour, density, big monitor, unlock screen",
                    "White base, Khand/Hind, subtle terracotta, lagoon and jungle green; drawn shapes only, no figures, nothing from locked pages"],
         "submit_agent": "portfolio", "submit_to": "Portfolio Agent", "section_counts": cnt, "deck_size": N,
         "sources": {"dashboard": "https://webermanapps.github.io/portfolio-dashboard/", "source": "/workspace/ops/folio/dashboard"}},
        seed=1014, n=N)
