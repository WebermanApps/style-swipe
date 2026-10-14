#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-board-2: UpKeep Board Details (Oct 14 2026), 20 pairs.
Follows upkeep-board (submission c7dcf8f3, 18/20, 2 skips). Carried first: upkeep-board-17 and -18.
Builds on the picks: compact, small top bar, big app button, three-across outlined tiles, report first as an open card
showing only the most important things with a dropdown for more (Max's note), saffron banner, approvals collapsed with count
as a quiet pill, video mid-page as a compact row, coloured icon tiles, lagoon leads, pure white dashboard, MacBook three
columns, big monitor centred three, team feed three latest. UpKeep rules: no AI mentions; only price line
'Membership Starting at $99/Month'. Submit -> agent 'upkeep'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
from carry_over import carried_first
DID = "upkeep-board-2"; TOPIC = "upkeep-board"
B = dict(name="UpKeep", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[LAGOON, TERRA, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("ub2_", "UpKeep")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
def appbtn(B, y, o):
    c = o.get("abc", LAGOON); st = o.get("appbtn", "fill")
    if st == "icon": return R(14, y, 212, 30, c, r=B["r"]) + tile_icon(70, y + 8, 5, "#FFFFFF", 14) + T(B, 128, y + 19.5, "Open UpKeep App", 10, "#FFFFFF", True, a="middle"), 36
    return R(14, y, 212, 30, c, r=B["r"]) + T(B, 120, y + 19.5, "Open UpKeep App", 10, "#FFFFFF", True, a="middle"), 36
SEC["appbtn"] = appbtn
base = dict(title="UpKeep", hdr="bar", report="more", rc=SAFFRON, rname="Morning Report", rn=3, urgent="pillcount", uc=TERRA, dens=4,
            tnames=["Open App", "Review Build", "Ideas Deck", "Videos", "Links", "Deadlines"], cols=3, tn=3, th=38, video="row", vt="Video Of The Week",
            fname="Team Feed", fn=3, uitems=["Approve the yard sign", "Pick the van side", "Confirm a deadline"])
def AP(s): return s.replace(" Urgent Items<", " Approvals<").replace(">Urgent Items<", ">Approvals<").replace(">Urgent<", ">Approvals<")
def M(order, **k): return AP(mock(B, order, **{**base, **k}))
STD = ["hdr", "appbtn", "report", "urgent", "video", "tiles", "feed"]
G = "Report Card"
P(G, "Report: Top Three Points Or Top Two?",
  ("rp_three", "Top Three Points", "Three most important lines, then Show More.", "focused", M(["hdr", "appbtn", "report", "urgent", "tiles"])),
  ("rp_two", "Top Two Points", "Only the two biggest items, then Show More.", "quick", M(["hdr", "appbtn", "report", "urgent", "tiles"], rn=2)))
P(G, "More Detail: Show More Link Or Fold Row?",
  ("rp_link", "Show More Link", "Underlined link under the points.", "quick", M(["hdr", "appbtn", "report", "urgent", "video"])),
  ("rp_fold", "Fold Row With Chevron", "A ruled row that drops down the rest.", "calm", M(["hdr", "appbtn", "report", "urgent", "video"], more="fold")))
P(G, "Report Card: White With Saffron Dots Or Saffron Tint?",
  ("rp_white", "White Card, Saffron Dots", "Saffron only on the bullets.", "calm", M(["hdr", "appbtn", "report", "urgent", "tiles"])),
  ("rp_tint", "Soft Saffron Tint", "The whole card tinted saffron.", "visual", M(["hdr", "appbtn", "report", "urgent", "tiles"], rcard="tint")))
G = "App Button"
P(G, "App Button: Lagoon Or Terracotta?",
  ("ab_lagoon", "Lagoon Button", "Matches the lagoon lead.", "calm", M(["hdr", "appbtn", "report", "urgent"])),
  ("ab_terra", "Terracotta Button", "Warm, stands out from the rest.", "action", M(["hdr", "appbtn", "report", "urgent"], abc=TERRA)))
P(G, "App Button: Words Only Or With A House Icon?",
  ("ab_words", "Words Only", "Plain and clean.", "focused", M(["hdr", "appbtn", "report", "tiles"])),
  ("ab_icon", "With A House Icon", "Small drawn house before the words.", "visual", M(["hdr", "appbtn", "report", "tiles"], appbtn="icon")))
G = "App Tiles"
P(G, "Tiles: Icon In A Tinted Square Or Icon Alone?",
  ("at_tint", "Icon In A Tinted Square", "Coloured square behind each icon.", "visual", M(["hdr", "appbtn", "tiles", "report"], tn=6)),
  ("at_plain", "Icon Alone", "Just the coloured line icon.", "calm", M(["hdr", "appbtn", "tiles", "report"], tn=6, tiles="lineplain")))
P(G, "Tiles: Label Left Or Centred?",
  ("at_left", "Label Bottom Left", "Icon top left, label under it.", "focused", M(["hdr", "appbtn", "tiles", "report"], tn=6)),
  ("at_center", "Centred", "Icon and label centred.", "calm", M(["hdr", "appbtn", "tiles", "report"], tn=6, tiles="linecenter")))
G = "Approvals Pill"
P(G, "Approvals Pill: Terracotta Count Or Lagoon Count?",
  ("ap_terra", "Terracotta Count", "Count bubble in terracotta.", "action", M(["hdr", "appbtn", "urgent", "report", "tiles"])),
  ("ap_lagoon", "Lagoon Count", "Count bubble in lagoon, calmer.", "calm", M(["hdr", "appbtn", "urgent", "report", "tiles"], uc=LAGOON)))
P(G, "Approvals Pill: Above The Report Or Below?",
  ("ap_above", "Above The Report", "Seen right after the app button.", "action", M(["hdr", "appbtn", "urgent", "report", "video"])),
  ("ap_below", "Below The Report", "Report first, then approvals.", "calm", M(["hdr", "appbtn", "report", "urgent", "video"])))
G = "Video Row"
P(G, "Video Row: Picture Left Or Right?",
  ("vd_left", "Picture Left", "Frame first, title beside it.", "visual", M(["hdr", "appbtn", "report", "urgent", "video", "feed"])),
  ("vd_right", "Picture Right", "Title first, frame at the end.", "focused", M(["hdr", "appbtn", "report", "urgent", "video", "feed"], video="rowr")))
P(G, "Video Row: With Length Tag Or Without?",
  ("vd_dur", "With Length Tag", "Small time tag on the frame.", "quick", M(["hdr", "appbtn", "report", "urgent", "video", "tiles"], video="rowdur")),
  ("vd_nodur", "No Tag", "Cleaner frame.", "calm", M(["hdr", "appbtn", "report", "urgent", "video", "tiles"])))
G = "Top Bar"
P(G, "Top Bar: Updated Badge Or Share Icon?",
  ("tb_badge", "Green Updated Badge", "Shows how fresh the page is.", "focused", M(["hdr", "appbtn", "report", "urgent", "tiles"])),
  ("tb_share", "Share Icon", "Small share icon at the right.", "quick", M(["hdr", "appbtn", "report", "urgent", "tiles"], hdr="barshare")))
G = "Team Feed"
P(G, "Team Feed: Dot Lines Or Icon Cards?",
  ("tf_dots", "Dot Lines", "Three short lines with colour dots.", "quick", M(["hdr", "appbtn", "report", "feed"])),
  ("tf_icons", "Icon Cards", "Three small cards with coloured icons.", "visual", M(["hdr", "appbtn", "report", "feed"], feed="icons")))
G = "Density"
P(G, "Compact: Tight Or Extra Tight?",
  ("dn_tight", "Compact", "Small gaps between blocks.", "focused", M(STD)),
  ("dn_xtight", "Extra Compact", "Almost no gaps, more on screen.", "quick", M(STD, dens=1)))
G = "MacBook And Big Monitor"
P(G, "MacBook Three Columns: Report Left Or App And Video Left?",
  ("mb_rep", "Report Left", "Report and approvals in the first column.", "focused", AP(desk(B, [["hdr", "report", "urgent"], ["appbtn", "video", "tiles"], ["feed"]], label="MacBook", frame="laptop", note="Phone stacks the same blocks", **base))),
  ("mb_app", "App And Video Left", "App button and video first.", "action", AP(desk(B, [["hdr", "appbtn", "video"], ["report", "urgent"], ["tiles", "feed"]], label="MacBook", frame="laptop", note="Phone stacks the same blocks", **base))))
P(G, "Big Monitor: Narrow Centre Or Wide Centre?",
  ("bm_narrow", "Narrow Centre", "Three columns in a narrow band.", "calm", AP(desk(B, [["hdr", "appbtn", "report"], ["urgent", "video"], ["tiles", "feed"]], ratio=(170, 140), note="Wide margins either side", **base))),
  ("bm_wide", "Wide Centre", "Three columns using most of the screen.", "visual", AP(desk(B, [["hdr", "appbtn", "report"], ["urgent", "video"], ["tiles", "feed"]], ratio=(228, 140), note="Small margins", **base))))
def icons(st):
    s, y = stack(B, ["hdr"], base, 10); s += T(B, 14, y + 10, "Sections", 12, None, True)
    for i, nm in enumerate(["Latest Open Items", "Deadlines", "Current Status", "Links", "Videos", "Recent Work"]):
        yy = y + 22 + i * 30; c = B["acc"][i % 4]
        s += card(B, 14, yy, 212, 26)
        s += (R(20, yy + 4, 18, 18, c + "1F", r=5) if st == "sq" else f'<circle cx="29" cy="{yy+13}" r="9.5" fill="{c}1F"/>') + tile_icon(22, yy + 6, i, c, 14)
        s += T(B, 46, yy + 16.5, nm, 9, None, True) + chev(212, yy + 13, B["mute"])
    return screen(s, "#FFFFFF")
P("Icons", "Coloured Icons: Rounded Squares Or Circles?",
  ("ic_sq", "Rounded Squares", "Tinted square behind each icon.", "focused", icons("sq")),
  ("ic_circ", "Circles", "Tinted circle behind each icon.", "calm", icons("circ")))
P("Approvals Pill", "Approvals Pill: White With Count Or Tinted?",
  ("ap_white", "White Pill, Count Bubble", "Outlined pill, terracotta number.", "focused", M(["hdr", "appbtn", "urgent", "report", "tiles"])),
  ("ap_tinted", "Tinted Pill", "Soft terracotta pill, count in the words.", "calm", M(["hdr", "appbtn", "urgent", "report", "tiles"], urgent="pill")))
carried = carried_first(TOPIC, [], clear=False)
for p in carried:
    p.pop("id", None)
    for s in "AB": p["option" + s]["id"] = "ub2_rt_" + p["option" + s]["id"].split("_", 1)[1]
    p["purpose"] = "retest"; p["retest"] = True; p["notes"] = True; p["share"] = True
pairs[:0] = carried
N = len(pairs); assert N == 20, N
txt = str(pairs); assert " AI " not in txt and "$164" not in txt and "$312" not in txt
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "UpKeep Board Details", "UpKeep", pairs,
        {"brands": ["UpKeep Board Details: two carried pairs first, then deeper on the picked report card (top points plus a dropdown for more), app button, tiles, approvals pill, video row, top bar, team feed, density, MacBook and big monitor",
                    "Pure white dashboard mockups on the light cream deck page, Khand/Hind, lagoon leads, terracotta for approvals, saffron report"],
         "submit_agent": "upkeep", "submit_to": "UpKeep Agent", "section_counts": cnt, "deck_size": N, "carried": len(carried), "one_card_per_screen": True,
         "follows": {"deck": "upkeep-board", "submission": "c7dcf8f3-f0fa-479d-a96d-01c59799a08d", "answered": 18, "total": 20},
         "sources": {"results": "/workspace/style-swipe/results/upkeep-board.txt"}},
        seed=1019, n=N, first=len(carried))
carried_first(TOPIC, [], clear=True)
