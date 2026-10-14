#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-board (Oct 14 2026): UpKeep Board Deck, 20 pairs on how the UpKeep command center dashboard
(WebermanApps/upkeep-cc-d36d3521; screenshots /workspace/smartkeep/dash-style/upkeep-dash-v3-393/-1470/-2560.png) is presented.
Light cream base, Khand/Hind, UpKeep rules: no AI mentions, plans Essentials/Plus/Complete only if needed,
only price line 'Membership Starting at $99/Month'. Drawn SVG mockups via dash_kit, example content only. Submit -> agent 'upkeep'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
DID = "upkeep-board"; PRICE = "Membership Starting at $99/Month"
CREAM = "#FBF6EC"
B = dict(name="UpKeep Command Center", bg=CREAM, ink="#0A0A0A", mute="#525252", line="#E5DCCB", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("ub_", "UpKeep")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(title="UpKeep", sub="Command Center", tnames=["Open App", "Review Build", "Ideas Deck", "Videos", "Links", "Deadlines"],
            uitems=["Approve the yard sign", "Pick the van side", "Confirm a deadline"], fname="Team Feed", vt="Video Of The Week", rname="Morning Report")
def M(order, **k): return mock(B, order, **{**base, **k})
def AP(s): return s.replace(">Urgent<", ">Approvals<").replace(" Urgent Items<", " Approvals<").replace(" Need You Today<", " Approvals Waiting<")
def appbtn(B, y, o):
    st = o.get("appbtn", "big")
    if st == "big": return R(14, y, 212, 30, TERRA, r=B["r"]) + T(B, 120, y + 19.5, "Open UpKeep App", 10, "#FFFFFF", True, a="middle"), 36
    if st == "line": return R(14, y, 212, 26, "#FFFFFF", TERRA, B["r"], 1.5) + T(B, 120, y + 17, "Open UpKeep App", 9, TERRA, True, a="middle"), 32
    return "", 0
def pricecard(B, y, o):
    return card(B, 14, y, 212, 30, "tint", TERRA) + T(B, 120, y + 19, PRICE, 9, TERRA, True, a="middle"), 36
SEC["appbtn"] = appbtn; SEC["price"] = pricecard
def W_(order, **k): return AP(M(order, **k))
P("Layout", "Top Of Page: Big App Button Or App Tiles?",
  ("ly_btn", "Big App Button", "One bold button, then the rest.", "action", W_(["hdr", "appbtn", "video", "report", "urgent"], hdr="logo" if False else "plain")),
  ("ly_tiles", "Row Of App Tiles", "Every app one tap away.", "quick", W_(["hdr", "tiles", "video", "report", "urgent"], cols=3, tn=3, tiles="tint", th=38)))
P("Layout", "Page Title: Small Top Bar Or Big Command Center Title?",
  ("ly_small", "Small Top Bar", "Name in a slim bar.", "calm", W_(["hdr", "report", "urgent", "tiles"], tn=4)),
  ("ly_bigt", "Big Title Block", "Large Khand title, short rule.", "focused", W_(["hdr", "report", "urgent", "tiles"], hdr="big", title="Command Center", sub="Status, open items and decisions", tn=4)))
P("Morning And Evening Report", "Report: Above The Video Or Below?",
  ("rp_above", "Report First", "Read the day, then watch.", "focused", W_(["hdr", "report", "video", "urgent"], report="collapsed")),
  ("rp_below", "Video First", "Video up top, report after.", "visual", W_(["hdr", "video", "report", "urgent"], report="collapsed", video="thumb")))
P("Morning And Evening Report", "Report: Collapsed Row Or Open Card?",
  ("rp_row", "Collapsed Row", "One line, tap to read.", "quick", W_(["hdr", "appbtn", "report", "urgent", "feed"], report="collapsed")),
  ("rp_open", "Open Card", "First lines always showing.", "calm", W_(["hdr", "appbtn", "report", "urgent", "feed"])))
P("Morning And Evening Report", "Report: Saffron Banner Or Morning/Evening Tabs?",
  ("rp_banner", "Saffron Banner", "Short, with a side stripe.", "visual", W_(["hdr", "report", "tiles"], report="banner", rc=SAFFRON, tn=4)),
  ("rp_tabs", "Morning / Evening Tabs", "Both reports, one switch.", "action", W_(["hdr", "report", "tiles"], report="tabs", tn=4)))
P("App Tiles", "App Tiles: Outlined Or Solid Colour?",
  ("at_line", "Outlined Tiles", "White tiles, coloured icons.", "calm", W_(["hdr", "tiles", "report"], th=46)),
  ("at_solid", "Solid Colour Tiles", "Bold blocks in the four accents.", "visual", W_(["hdr", "tiles", "report"], tiles="solid", th=46)))
P("App Tiles", "App Tiles: Three Across Or A List?",
  ("at_three", "Three Across", "Small tinted tiles in a grid.", "quick", W_(["hdr", "tiles", "report", "urgent"], cols=3, tiles="tint", th=40)),
  ("at_list", "List Rows", "One row per app with a chevron.", "focused", W_(["hdr", "tiles", "report"], tiles="row")))
P("Video Card", "Video: Big Thumbnail Or Compact Row?",
  ("vd_big", "Big Thumbnail", "Large frame with a play button.", "visual", W_(["hdr", "video", "report", "urgent"], video="thumb")),
  ("vd_row", "Compact Row", "Small frame beside the title.", "quick", W_(["hdr", "video", "report", "urgent", "tiles"], tn=2)))
P("Video Card", "Video: Inside The Page Or Under The App Button?",
  ("vd_mid", "Mid-Page", "Report and approvals first.", "focused", W_(["hdr", "report", "urgent", "video"], video="thumb")),
  ("vd_top", "Right Under The App Button", "Video is the first thing seen.", "visual", W_(["hdr", "appbtn", "video", "report"], video="thumb")))
P("Approvals Dropdown", "Approvals: Collapsed Card Or Open List?",
  ("ap_closed", "Collapsed With Count", "Terracotta stripe, tap to open.", "calm", W_(["hdr", "urgent", "report", "tiles"], tn=4)),
  ("ap_open", "Open List", "Everything waiting, shown.", "action", W_(["hdr", "urgent", "report", "tiles"], urgent="open", tn=2)))
P("Approvals Dropdown", "Approvals: Quiet Pill Or Full Bar?",
  ("ap_pill", "Quiet Pill", "Small, opens a list.", "calm", W_(["hdr", "urgent", "report", "video"])),
  ("ap_bar", "Full Terracotta Bar", "Hard to miss.", "action", W_(["hdr", "urgent", "report", "video"], urgent="bar")))
P("Team Feed", "Team Feed: Short List Or Longer Timeline?",
  ("tf_short", "Three Latest", "Three lines, then More.", "quick", W_(["hdr", "report", "urgent", "feed", "tiles"], fn=3, tn=2)),
  ("tf_long", "Longer Timeline", "Six items with colour dots.", "calm", W_(["hdr", "report", "feed"], fn=6)))
def typo(upper):
    s = T(B, 14, 34, "UPKEEP" if upper else "UpKeep", 26, B["ink"], True, ex='letter-spacing="2"' if upper else "")
    s += T(B, 14, 50, "Command Center", 8, B["mute"]) + L(14, 60, 226, 60, B["line"])
    for i, h in enumerate(["Morning Report", "Approvals", "Team Feed"]):
        y = 84 + i * 62; s += T(B, 14, y, h.upper() if upper else h, 14 if not upper else 11, B["ink"], True, ex='letter-spacing="1.5"' if upper else "") + bars(3, 14, y + 10, 200, B["mute"] + "88", 8)
    s += card(B, 14, 262, 212, 26, "tint", TERRA) + T(B, 120, 279, PRICE, 8.5, TERRA, True, a="middle")
    return phone(B, s)
P("Typography", "Khand Headings: Title Case Or Spaced Capitals?",
  ("ty_title", "Title Case", "Khand as written, Hind body.", "calm", typo(False)),
  ("ty_caps", "Spaced Capitals", "Khand in tracked capitals.", "focused", typo(True)))
P("Colour", "Lead Colour: Terracotta Or Lagoon?",
  ("co_terra", "Terracotta Leads", "Button, stripe and badges in terracotta.", "visual", W_(["hdr", "appbtn", "urgent", "report", "tiles"], urgent="bar", tn=2)),
  ("co_lagoon", "Lagoon Leads", "Lagoon for structure, terracotta only for approvals.", "calm", W_(["hdr", "report", "urgent", "tiles"], report="banner", rc=LAGOON, tiles="tint", tn=4)))
P("Colour", "Base: Cream Or Pure White?",
  ("co_cream", "Light Cream", "Warm cream page, white cards.", "calm", W_(["hdr", "appbtn", "report", "urgent", "tiles"], tn=2)),
  ("co_white", "Pure White", "White page, thin-border cards.", "focused", AP(mock({**B, "bg": "#FFFFFF", "line": "#E5E5E5"}, ["hdr", "appbtn", "report", "urgent", "tiles"], **{**base, "tn": 2}))))
def icons(st):
    s = T(B, 14, 30, "Icons", 16, B["ink"], True) + T(B, 14, 42, "Section icons on the dashboard", 7, B["mute"])
    for i, nm in enumerate(["Open Items", "Deadlines", "Current Status", "Links", "Videos", "Team Feed"]):
        y = 56 + i * 36; c = B["acc"][i % 4]
        s += card(B, 14, y, 212, 30)
        if st == "tile": s += R(22, y + 5, 20, 20, c + "1F", r=5) + tile_icon(25, y + 8, i, c, 14)
        else: s += tile_icon(22, y + 8, i, B["ink"], 14)
        s += T(B, 50, y + 19, nm, 9.5, None, True) + chev(212, y + 15, B["mute"])
    return phone(B, s)
P("Icons", "Section Icons: Coloured Tiles Or Plain Line?",
  ("ic_tile", "Coloured Icon Tiles", "Each section gets an accent.", "visual", icons("tile")),
  ("ic_line", "Plain Black Line Icons", "Quiet, all one colour.", "calm", icons("line")))
P("Density", "Density: Airy Or Compact?",
  ("dn_airy", "Airy", "Fewer blocks, more space.", "calm", W_(["hdr", "appbtn", "report", "urgent"], dens=16)),
  ("dn_compact", "Compact", "Everything on one screen.", "quick", W_(["hdr", "appbtn", "report", "urgent", "tiles", "feed"], dens=3, report="line", cols=3, tn=3, th=32, appbtn="line")))
P("Phone, MacBook And Big Monitor", "MacBook: Two Columns Or Three?",
  ("mb_two", "Two Columns", "Report and approvals left, video right.", "focused", AP(desk(B, [["hdr", "appbtn", "report", "urgent"], ["video", "feed"]], label="MacBook", frame="laptop", note="Phone stacks the same blocks", **base))),
  ("mb_three", "Three Columns", "Report, video and feed side by side.", "visual", AP(desk(B, [["hdr", "report", "urgent"], ["appbtn", "video"], ["feed", "tiles"]], label="MacBook", frame="laptop", note="Phone stacks the same blocks", **{**base, "tn": 4}))))
P("Phone, MacBook And Big Monitor", "Big Monitor: Four Columns Or Centred Three?",
  ("bm_four", "Four Columns, Full Width", "Uses the whole screen.", "visual", AP(desk(B, [["hdr", "report"], ["urgent", "feed"], ["video"], ["tiles"]], note="Phone stacks the same blocks", **{**base, "tn": 4}))),
  ("bm_three", "Centred Three Columns", "Wide margins, easier to scan.", "calm", AP(desk(B, [["hdr", "report", "urgent"], ["video", "appbtn"], ["feed"]], ratio=(224, 140), note="Phone stacks the same blocks", **base))))
SECN = ["Latest Open Items", "Deadlines", "Current Status", "Links", "Videos", "Recent Work"]
P("Phone, MacBook And Big Monitor", "Phone: Sections As Dropdowns Or Open Cards?",
  ("ph_drop", "Dropdown Rows", "Each section closed until tapped.", "quick", W_(["hdr", "appbtn", "urgent", "tiles"], tiles="row", tnames=SECN)),
  ("ph_open", "Open Cards", "Sections open, scroll to see more.", "calm", W_(["hdr", "appbtn", "urgent", "report", "feed"], rname="Latest Open Items", fname="Deadlines")))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "UpKeep Board Deck", "UpKeep", pairs,
        {"brands": ["UpKeep command center presentation: layout, Morning/Evening Report placement, app tiles, Video card, approvals dropdown, team feed, type, colour, icons, density, phone/MacBook/big monitor",
                    "Light cream base, Khand/Hind, terracotta/lagoon/jungle/saffron accents; brand rules applied; only price line: " + PRICE],
         "submit_agent": "upkeep", "submit_to": "UpKeep Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "sources": {"repo": "WebermanApps/upkeep-cc-d36d3521", "screens": "/workspace/smartkeep/dash-style/upkeep-dash-v3-393.png"}},
        seed=1016, n=N)
