#!/usr/bin/env python3
"""Build Style Swipe deck construction-1 (PUBLISHED): 50 pairs for the Construction agent (Weberman Construction: close-out
of a finished custom home, the live Home Guide, warranty registration, open finish choices, site walks, trade directory).
Based on the Oct 13 team-sync recap, team feed and Construction's latest files. Example data only (Example Home, Example
Owner, sample serials). Pattern: tools/build_dashboard_2.py + draft_svg.py via team_kit.py. Run from repo root."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "construction-1"; pairs, O, add = deck("cn1_", "Construction")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
HG = ("hdr", "Home Guide", "Example Home", LAGOON, "logo", "H")
HC = ("hdr", "Construction", "Close-Out · Example Home", INK, "logo", "W")
ITEMS = [("Water Heater 1", "Registered"), ("Water Heater 2", "Registered"), ("Garage Door", "To Confirm"), ("Foundation Walls", "Waiting")]
ST = {"Registered": JUNGLE, "To Confirm": SAFFRON, "Waiting": LAGOON, "Due": TERRA}

G = "Warranty Status"
def ws(k):
    if k == "tags": return [HG, ("lbl", "Warranties"), ("raw", "".join(b_card(70 + i * 40, n, "Example Brand", ST[s], "tag:" + s)[0] for i, (n, s) in enumerate(ITEMS)), 160)]
    if k == "dots": return [HG, ("lbl", "Warranties"), ("raw", "".join(b_card(70 + i * 40, n, s, ST[s])[0] for i, (n, s) in enumerate(ITEMS)), 160)]
    if k == "ring": return [HG, ("ring", .5, JUNGLE, "2/4", "Registered"), ("cards", [(n, s) for n, s in ITEMS[2:]], SAFFRON)]
    if k == "bar": return [HG, ("bar", .5, JUNGLE, "2 Of 4 Registered", "50%"), ("raw", "".join(b_card(84 + i * 40, n, s, ST[s])[0] for i, (n, s) in enumerate(ITEMS)), 160)]
    if k == "groups": return [HG, ("lbl", "Done", JUNGLE), ("cards", ITEMS[:2], JUNGLE, "dot", "line", 28), ("lbl", "Still Open", SAFFRON), ("cards", ITEMS[2:], SAFFRON, "dot", "line", 28)]
    if k == "flat": return [HG, ("table", [(n, s) for n, s in ITEMS], True)]
    if k == "icon": return [HG, ("cards", [(n, s) for n, s in ITEMS], None, "ic:check", "line", 36)]
    return [HG, ("cards", [(n, s) for n, s in ITEMS], None, "dot", "left", 36)]
pr(G, "Status Tags Or Colored Dots?", ws, ("ws_tags", "Status As Tags", "Registered, To Confirm, Waiting.", "visual", "tags"), ("ws_dots", "Colored Dot Plus Words", "Dot left, status under the name.", "calm", "dots"))
pr(G, "Ring Or Bar For Progress?", ws, ("ws_ring", "Progress Ring On Top", "2 of 4 in a ring.", "visual", "ring"), ("ws_bar", "Thin Bar On Top", "Bar plus the list.", "focused", "bar"))
pr(G, "Grouped Or One Table?", ws, ("ws_groups", "Done And Still Open Groups", "Two short groups.", "focused", "groups"), ("ws_table", "One Shaded Table", "Item and status in rows.", "calm", "flat"))
pr(G, "Icon Or Left Edge?", ws, ("ws_icon", "Check Icon Per Row", "Tinted icon box.", "visual", "icon"), ("ws_edge", "Colored Left Edge", "Edge shows the status.", "quick", "edge"))

G = "Item Detail Page"
def it(k):
    if k == "photo": return [HG, ("photo", 100, LAGOON, "room", "Water Heater 1"), ("table", [("Model", "Example 199"), ("Serial", "XX-000000"), ("Installed", "2025")])]
    if k == "facts": return [HG, ("h", "Water Heater 1", 18), ("tags", ["Registered"]), ("table", [("Model", "Example 199"), ("Serial", "XX-000000"), ("Installed", "2025"), ("Warranty", "Example Years")])]
    if k == "proof": return [HG, ("h", "Water Heater 1", 18), ("raw", rect(14, 80, 100, 70, SOFT, LINE, 4) + "".join(rect(22, 92 + i * 9, 80 - i * 8, 3, "#D6D0C6") for i in range(5)) + t(124, 100, "Confirmation", 9, INK, "khand") + t(124, 112, "Saved Oct 12", 7, MUTE) + tag(124, 118, "Registered", JUNGLE), 80)]
    if k == "noproof": return [HG, ("h", "Water Heater 1", 18), ("cards", [("Registered", "Oct 12 · no number given", "tag:Done")], JUNGLE)]
    if k == "care": return [HG, ("h", "Water Heater 1", 18), ("lbl", "Care"), ("checks", ["Flush yearly", "Clean filter every 6 months", "Check vent each fall"], JUNGLE, 0)]
    if k == "call": return [HG, ("h", "Water Heater 1", 18), ("lbl", "Who To Call"), ("cards", [("Example Plumbing Co", "Installer", "", "ic:phone"), ("Maker Support", "Warranty", "", "ic:phone")])]
    if k == "tabs": return [HG, ("h", "Water Heater 1", 18), ("tabs", ["Info", "Care", "Warranty", "Call"]), ("table", [("Model", "Example 199"), ("Serial", "XX-000000")])]
    return [HG, ("h", "Water Heater 1", 18), ("lbl", "Info"), ("table", [("Model", "Example 199")]), ("lbl", "Care"), ("checks", ["Flush yearly"], JUNGLE, 0), ("lbl", "Call"), ("cards", [("Example Plumbing Co", "")])]
pr(G, "Photo On Top Or Facts First?", it, ("it_photo", "Item Photo On Top", "Photo, then model and serial.", "visual", "photo"), ("it_facts", "Facts First", "Status tag and a table.", "focused", "facts"))
pr(G, "Show Proof Thumbnail Or Just Status?", it, ("it_proof", "Confirmation Thumbnail", "Small picture of the proof.", "visual", "proof"), ("it_noproof", "Status Card Only", "No picture, just a done card.", "calm", "noproof"))
pr(G, "Care Steps Or Who To Call?", it, ("it_care", "Care Checklist", "What to do and when.", "focused", "care"), ("it_call", "Who To Call", "Installer and maker.", "action", "call"))
pr(G, "Tabs Or One Long Page?", it, ("it_tabs", "Four Tabs", "Info, Care, Warranty, Call.", "focused", "tabs"), ("it_long", "One Scrolling Page", "All sections stacked.", "calm", "long"))

G = "Alerts And Badges"
def al(k):
    if k == "banner": return [HG, ("banner", "Register Garage Door By Nov 1", TERRA, "clock"), ("cards", ITEMS[:3])]
    if k == "badge": return [HG, ("cards", [(ITEMS[2][0], "Register by Nov 1", "tag:Due Soon")], TERRA), ("cards", ITEMS[:2])]
    if k == "none": return [HG, ("raw", rect(14, 60, 212, 40, JUNGLE + "12", "none", 8) + ic("check", 24, 70, 20, JUNGLE, 2) + t(52, 84, "Nothing Needs You Now", 11, INK, "khand"), 48), ("cards", ITEMS[:3])]
    if k == "quiet": return [HG, ("cards", ITEMS[:3])]
    if k == "count": return [HG, ("raw", t(14, 66, "1 Thing Due", 18, TERRA, "khand"), 30), ("cards", ITEMS[:3])]
    if k == "bell": return [("raw", t(14, 22, "Home Guide", 13, INK, "khand") + ic("clock", 196, 10, 16, INK) + dot(212, 12, 5, TERRA) + t(212, 14.5, "1", 6.5, "#FFFFFF", "hind", 700, "middle") + ln(44), 50), ("cards", ITEMS[:3])]
    if k == "14": return [HG, ("p", "Alerts show only when an item is due within 14 days."), ("cards", [(ITEMS[2][0], "Due in 12 days", "tag:Due")], TERRA)]
    return [HG, ("p", "Alerts show for anything not yet registered."), ("cards", [(ITEMS[2][0], "Not registered", "tag:Open"), (ITEMS[3][0], "Not registered", "tag:Open")], SAFFRON)]
pr(G, "Banner Or Row Badge?", al, ("al_banner", "Banner Over The List", "A terracotta strip on top.", "action", "banner"), ("al_badge", "Badge On The Row", "Only the item shows it.", "focused", "badge"))
pr(G, "All-Clear Card Or Nothing?", al, ("al_allclear", "Green All-Clear Card", "Says nothing needs you.", "calm", "none"), ("al_silent", "No Card When Clear", "Just the list.", "quick", "quiet"))
pr(G, "Count Headline Or Bell Dot?", al, ("al_count", "1 Thing Due Headline", "Big terracotta line.", "action", "count"), ("al_bell", "Bell With A Dot", "Quiet bell in the header.", "calm", "bell"))
pr(G, "14-Day Window Or Any Open Item?", al, ("al_14day", "Alert Within 14 Days", "Only near deadlines.", "calm", "14"), ("al_allopen", "Alert Any Open Item", "Everything unregistered.", "action", "all"))

G = "Finish Choices"
def fc(k):
    if k == "swatch": return [HC, ("h", "Foyer Border Tile", 16), ("swatch", ["#2B2B2B", "#F7F4EF", "#8A7A66"], ["Charcoal", "Ivory", "Taupe"]), ("btn", "Pick One", "fill", INK)]
    if k == "photos": return [HC, ("h", "Foyer Border Tile", 16), ("photos", 3, 70, ["room", "room", "room"]), ("btn", "Pick One", "fill", INK)]
    if k == "ab": return [HC, ("h", "Island Lights", 16), ("raw", photo(14, 74, 103, 110, SAFFRON, "sun") + photo(123, 74, 103, 110, LAGOON, "room") + btn(190, "A", "line", INK, 14, 103, 22, 8) + btn(190, "B", "line", INK, 123, 103, 22, 8), 150)]
    if k == "list": return [HC, ("h", "Island Lights", 16), ("cards", [("Option A", "Brass, three pendants"), ("Option B", "Black, one linear"), ("Not Sure", "Ask the designer")], None, "num")]
    if k == "conflict": return [HC, ("lbl", "Plans Disagree"), ("table", [("Plan Sheet", "Ivory Border"), ("Tile Order", "Charcoal Border")]), ("btn2", "Use Plan", "Use Order")]
    if k == "one": return [HC, ("lbl", "Open Choice"), ("h", "Foyer Border: Ivory Or Charcoal?", 14), ("btn2", "Ivory", "Charcoal")]
    if k == "all": return [HC, ("h", "5 Open Finish Choices", 15), ("cards", [("Island Lights", "Kitchen"), ("Foyer Border", "Foyer"), ("Mud Room Floor", "Mud Room"), ("Shower Walls", "Bath 2")], TERRA, "num", "line", 28)]
    return [HC, ("h", "5 Open Finish Choices", 15), ("tiles", [("Kitchen", "home"), ("Foyer", "star"), ("Mud Room", "tag"), ("Bath 2", "clock")], 2, 54)]
pr(G, "Swatches Or Photos?", fc, ("fc_swatch", "Color Swatches", "Three named chips.", "visual", "swatch"), ("fc_photos", "Three Room Photos", "See each in place.", "visual", "photos"))
pr(G, "Side-By-Side Or Listed?", fc, ("fc_ab", "A And B Side By Side", "Two photos, tap one.", "quick", "ab"), ("fc_list", "Numbered Options", "Short words per option.", "focused", "list"))
pr(G, "Show The Conflict Or Just Ask?", fc, ("fc_conflict", "Show Where Plans Disagree", "Plan sheet vs tile order.", "focused", "conflict"), ("fc_justask", "Just Ask The Choice", "One question, two buttons.", "quick", "one"))
pr(G, "List Or Room Tiles?", fc, ("fc_alllist", "All Open Choices Listed", "Numbered rows.", "focused", "all"), ("fc_rooms", "By Room Tiles", "Tap a room to see its choices.", "visual", "rooms"))

G = "Site Walk"
def sw(k):
    if k == "list": return [HC, ("h", "Site Walk", 16), ("checks", ["Heater 1 serial photo", "Garage door color", "Foyer border tile", "Smoke detectors"], JUNGLE, 1)]
    if k == "stops": return [HC, ("h", "Site Walk", 16), ("steps", ["Garage", "Foyer", "Mech", "Exterior"], LAGOON, 1), ("cards", [("Garage", "Door color, Heater 1 serial")], LAGOON)]
    if k == "cam": return [HC, ("lbl", "Stop 1 · Garage"), ("raw", rect(14, 70, 212, 140, "#2B2B2B", "none", 8) + "".join(f'<path d="M{x} {y} h{dx} M{x} {y} v{dy}" stroke="#FFFFFF" stroke-width="2.5"/>' for x, y, dx, dy in [(40, 90, 14, 14), (200, 90, -14, 14), (40, 190, 14, -14), (200, 190, -14, -14)]), 148), ("btn", "Take Photo", "fill", INK)]
    if k == "note": return [HC, ("lbl", "Stop 1 · Garage"), ("photo", 80, LAGOON, "room"), ("input", "Hold To Talk A Note..."), ("btn", "Next Stop", "fill", INK)]
    if k == "map": return [HC, ("h", "Site Walk", 16), ("raw", rect(14, 80, 212, 130, SOFT, "none", 6) + rect(30, 96, 80, 50, "#FFFFFF", LINE) + rect(118, 96, 92, 98, "#FFFFFF", LINE) + rect(30, 152, 80, 42, "#FFFFFF", LINE) + "".join(mono(x, y, str(i + 1), ACC[i], 16) for i, (x, y) in enumerate([(62, 112), (156, 136), (62, 165)])), 138)]
    if k == "rows": return [HC, ("h", "Site Walk", 16), ("cards", [("Garage", "2 items"), ("Foyer", "1 item"), ("Mechanical", "1 item")], None, "num")]
    if k == "sum": return [HC, ("h", "Walk Done", 18), ("stats", [("4", "Items"), ("6", "Photos"), ("1", "Left")]), ("btn", "Send Summary", "fill", TERRA)]
    return [HC, ("h", "Walk Done", 18), ("timeline", [("Garage", "Door color: Example Gray"), ("Foyer", "Border photo saved"), ("Mechanical", "Serial photo saved")])]
pr(G, "Checklist Or Stops?", sw, ("sw_list", "One Checklist", "Tick items as you go.", "quick", "list"), ("sw_stops", "Numbered Stops", "Walk room by room.", "focused", "stops"))
pr(G, "Camera First Or Note First?", sw, ("sw_cam", "Camera With Corner Guides", "Open straight to the camera.", "action", "cam"), ("sw_note", "Photo Plus Voice Note", "Photo, then hold to talk.", "calm", "note"))
pr(G, "Floor Plan Or Room Rows?", sw, ("sw_map", "Stops On A Floor Plan", "Numbers on a drawn plan.", "visual", "map"), ("sw_rows", "Room Rows", "Plain numbered rooms.", "quick", "rows"))
pr(G, "Counts Or Timeline Summary?", sw, ("sw_counts", "Counts, Then Send", "Items, photos, left.", "visual", "sum"), ("sw_timeline", "What Was Found, In Order", "A timeline of findings.", "focused", "line"))

G = "Trade Directory"
def td(k):
    tr = [("Painting And Drywall", "Example Painters"), ("Millwork", "Example Millwork"), ("Plumbing", "Example Plumbing Co"), ("Electrical", "Example Electric")]
    if k == "rows": return [HG, ("h", "Who Built It", 16), ("cards", tr, None, "ic:home")]
    if k == "tiles": return [HG, ("h", "Who Built It", 16), ("tiles", [("Paint", "star"), ("Millwork", "home"), ("Plumbing", "clock"), ("Electric", "tag")], 2, 56)]
    if k == "multi": return [HG, ("cards", [("Example Painters", "Painting And Drywall · Millwork")], TERRA, "ic:home"), ("tags", ["Painting And Drywall", "Millwork"])]
    if k == "single": return [HG, ("lbl", "Painting And Drywall"), ("cards", [tr[0]]), ("lbl", "Millwork"), ("cards", [tr[1]])]
    if k == "az": return [HG, ("input", "Search Trades...", INK, "search"), ("cards", tr[:3])]
    if k == "room": return [HG, ("tabs", ["Kitchen", "Bath", "Garage"], "under"), ("cards", tr[1:3])]
    if k == "call": return [HG, ("raw", "".join(rect(14, 60 + i * 44, 212, 38, "#FFFFFF", LINE, 8) + t(24, 76 + i * 44, n, 9.5, INK, "khand") + t(24, 87 + i * 44, s, 6.5, MUTE) + rect(186, 66 + i * 44, 32, 26, JUNGLE, "none", 13) + ic("phone", 194, 71 + i * 44, 16, "#FFFFFF", 2) for i, (n, s) in enumerate(tr[:3])), 140)]
    return [HG, ("cards", [(n, s, "tag:Warranty") for n, s in tr[:3]], LAGOON)]
pr(G, "Rows Or Trade Tiles?", td, ("td_rows", "Trade Rows", "Trade name and company.", "focused", "rows"), ("td_tiles", "Trade Tiles", "Tap a trade.", "visual", "tiles"))
pr(G, "Show Both Trades On One Card?", td, ("td_multi", "One Card, Two Trade Tags", "Company shows each trade.", "focused", "multi"), ("td_single", "Listed Under Each Trade", "Same company in two places.", "calm", "single"))
pr(G, "Search Or By Room?", td, ("td_search", "Search Box", "Find a trade fast.", "quick", "az"), ("td_room", "Tabs By Room", "Kitchen, Bath, Garage.", "visual", "room"))
pr(G, "Call Button Or Warranty Tag?", td, ("td_call", "Green Call Button", "Call from the row.", "action", "call"), ("td_wtag", "Warranty Tag", "Shows who covers a warranty.", "focused", "tag"))

G = "Preview Or Live"
def pv(k):
    if k == "banner": return [("raw", rect(0, 0, W, 22, SAFFRON) + t(120, 15, "PREVIEW · NOT LIVE YET", 7.5, INK, "hind", 700, "middle", 'letter-spacing="1"'), 22), HG, ("cards", ITEMS[:3])]
    if k == "corner": return [HG, ("raw", tag(170, 30, "Preview", SAFFRON, True), 0), ("cards", ITEMS[:3])]
    if k == "compare": return [HC, ("h", "What Changed", 16), ("table", [("Live", "3 items"), ("Preview", "4 items, new badge style")]), ("btn2", "Approve", "Not Yet")]
    if k == "diff": return [HC, ("h", "What Changed", 16), ("cards", [("Added", "Foundation Walls row", "tag:New"), ("Changed", "Badge style", "tag:Edit")], LAGOON)]
    if k == "rule": return [HC, ("lbl", "Publishing Rule"), ("cards", [("Small Fix", "Goes straight live", "tag:Live"), ("Design Change", "Preview first", "tag:Preview")], JUNGLE)]
    if k == "ask": return [HC, ("lbl", "Ready To Go Live?"), ("h", "New Badge Style", 16), ("btn2", "Go Live", "Keep Preview")]
    if k == "link": return [HC, ("cards", [("Live Page", "homes.example.com", "OPEN"), ("Preview Page", "homes.example.com/preview", "OPEN")], LAGOON, "ic:home")]
    return [HC, ("photos", 2, 120, ["house", "house"], [LAGOON, SAFFRON]), ("raw", t(14, 0, ""), 0), ("tags", ["Live", "Preview"])]
pr(G, "Full Banner Or Corner Tag?", pv, ("pv_banner", "Saffron Banner Across Top", "Can't miss it's a preview.", "action", "banner"), ("pv_corner", "Small Corner Tag", "Quiet preview marker.", "calm", "corner"))
pr(G, "Table Or Change Cards?", pv, ("pv_compare", "Live Vs Preview Table", "Two rows, approve buttons.", "focused", "compare"), ("pv_diff", "Change Cards", "Added and Changed tags.", "visual", "diff"))
pr(G, "Show The Rule Or Just Ask?", pv, ("pv_rule", "Show The Publishing Rule", "Small fix vs design change.", "focused", "rule"), ("pv_ask", "Just Ask: Go Live?", "One change, two buttons.", "quick", "ask"))
pr(G, "Links Or Side-By-Side?", pv, ("pv_links", "Two Link Rows", "Open live or preview.", "quick", "link"), ("pv_side", "Two Screens Side By Side", "See both at once.", "visual", "side"))

G = "Owner Handoff Email"
def oe(k):
    b = [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 24)]
    if k == "list": b += [("lbl", "Subject: Warranties Registered"), ("checks", ["Water Heater 1", "Water Heater 2", "Garage Door (next)"], JUNGLE, 2)]
    elif k == "para": b += [("lbl", "Subject: Warranties Registered"), ("p", "Both water heaters are registered in your name. The garage door is next. Everything is in your Home Guide.", 40)]
    elif k == "btn": b += [("h", "Your Home Guide", 16, INK, True), ("p", "All warranties and care steps in one place.", 40, MUTE, True), ("btn", "Open Home Guide", "fill", LAGOON)]
    elif k == "qr": b += [("h", "Your Home Guide", 16, INK, True), ("raw", rect(90, 100, 60, 60, "#FFFFFF", INK, 2) + "".join(rect(94 + (i % 6) * 9, 104 + (i // 6) * 9, 7, 7, INK) for i in range(36) if (i * 7) % 3), 72), ("p", "Scan to open on your phone.", 40, MUTE, True)]
    elif k == "notin": b += [("lbl", "Not In The Guide"), ("cards", [("IT And Security", "Ask your installer"), ("Pool And Exterior", "Ask your installer")], SAFFRON)]
    elif k == "foot": b += [("p", "Everything is in your Home Guide.", 40), ("gap", 100), ("p", "Note: IT, security, pool and exterior items are not covered here.", 40, MUTE)]
    elif k == "photo": b += [("photo", 80, LAGOON, "house"), ("h", "Your Home Is Handed Over", 14, INK, True)]
    else: b += [("h", "Your Home Is Handed Over", 14, INK, True), ("p", "Here's what's done and what's next.", 40, MUTE, True)]
    return b
pr(G, "Checklist Or Paragraph?", oe, ("oe_checks", "Ticked Item List", "What's done at a glance.", "focused", "list"), ("oe_para", "Short Paragraph", "Reads like a note.", "calm", "para"))
pr(G, "Button Or QR Code?", oe, ("oe_btn", "Open Home Guide Button", "Lagoon button.", "action", "btn"), ("oe_qr", "QR Code To Scan", "For the phone.", "visual", "qr"))
pr(G, "Not-Covered As Cards Or A Footnote?", oe, ("oe_notcards", "Not-Covered Cards", "Saffron cards spell it out.", "focused", "notin"), ("oe_footnote", "Small Footnote", "One line at the bottom.", "calm", "foot"))
pr(G, "Photo Header Or Plain?", oe, ("oe_photo", "Home Photo Header", "Warm opener.", "visual", "photo"), ("oe_plainhead", "Plain Headline", "Words only.", "calm", "plain"))

G = "Close-Out Dashboard"
def cd(k):
    if k == "pct": return [HC, ("word", "86%", 40, JUNGLE, "Close-Out Done"), ("cards", [("Warranties", "2 left"), ("Finish Choices", "5 open")], TERRA)]
    if k == "stats": return [HC, ("stats", [("2", "Warranties"), ("5", "Choices"), ("3", "Walk Items")], "tint"), ("cards", [("Next", "Site walk Sat")], LAGOON)]
    if k == "kanban": return [HC, ("raw", "".join(rect(14 + i * 72, 60, 66, 190, SOFT, "none", 6) + lbl(20 + i * 72, 74, n, ACC[i], 6) + "".join(rect(18 + i * 72, 82 + j * 30, 58, 24, "#FFFFFF", LINE, 4) for j in range(3 - i)) for i, n in enumerate(["To Do", "Waiting", "Done"])), 200)]
    if k == "list": return [HC, ("lbl", "To Do"), ("cards", [("Register Garage Door", ""), ("Pick Foyer Border", "")], TERRA, "dot", "line", 26), ("lbl", "Waiting"), ("cards", [("Walls Warranty Reply", "")], LAGOON, "dot", "line", 26)]
    if k == "hours": return [HC, ("lbl", "Hours Logged · Sample"), ("bars", [.4, .7, .5, .9, .3], LAGOON, ["M", "T", "W", "T", "F"]), ("stats", [("25", "Total Hours"), ("5", "Days")], "plain")]
    if k == "nohours": return [HC, ("cards", [("Warranties", "2 left"), ("Finish Choices", "5 open"), ("Site Walk", "Sat")], None)]
    if k == "next": return [HC, ("lbl", "Next Step"), ("h", "Site Walk Saturday", 20), ("p", "3 items to check. Bring the serial label list.")]
    return [HC, ("timeline", [("Mon", "Heaters registered"), ("Sat", "Site walk"), ("Nov 1", "Garage door due")])]
pr(G, "Big Percent Or Stat Boxes?", cd, ("cd_pct", "Big Percent Done", "One number up top.", "visual", "pct"), ("cd_stats", "Three Stat Boxes", "Counts per area.", "focused", "stats"))
pr(G, "Columns Or Grouped List?", cd, ("cd_kanban", "To Do, Waiting, Done Columns", "Board style.", "visual", "kanban"), ("cd_list", "Grouped List", "To Do then Waiting.", "focused", "list"))
pr(G, "Show Hours Or Not?", cd, ("cd_hours", "Hours Chart", "Daily bars and total.", "visual", "hours"), ("cd_nohours", "Leave Hours Off", "Only open items.", "calm", "nohours"))
pr(G, "Next Step Or Timeline?", cd, ("cd_next", "One Next Step, Big", "What to do next.", "action", "next"), ("cd_timeline", "Dated Timeline", "What happens when.", "focused", "line"))

G = "Home Guide Home Screen"
def hh(k):
    if k == "photo": return [("photo", 120, LAGOON, "house", "Welcome To Example Home"), ("tiles", [("Warranties", "check"), ("Care", "clock"), ("Who To Call", "phone"), ("Rooms", "home")], 2, 54)]
    if k == "word": return [("gap", 20), ("word", "Example Home", 26, INK, "Home Guide"), ("tiles", [("Warranties", "check"), ("Care", "clock"), ("Who To Call", "phone"), ("Rooms", "home")], 2, 54)]
    if k == "solid": return [HG, ("tiles", [("Warranties", "check"), ("Care", "clock"), ("Who To Call", "phone"), ("Rooms", "home")], 2, 70, "solid")]
    if k == "line": return [HG, ("tiles", [("Warranties", "check"), ("Care", "clock"), ("Who To Call", "phone"), ("Rooms", "home")], 2, 70)]
    if k == "season": return [HG, ("banner", "Fall: Flush Water Heaters", JUNGLE, "star"), ("cards", [("Warranties", "2 of 4"), ("Rooms", "12")])]
    if k == "nos": return [HG, ("cards", [("Warranties", "2 of 4"), ("Rooms", "12"), ("Care", "3 this season")])]
    if k == "install": return [HG, ("cards", [("Add To Home Screen", "One tap to open later", "", "ic:phone")], LAGOON, "ic:phone", "tint", 44), ("cards", [("Warranties", "2 of 4")])]
    return [HG, ("cards", [("Warranties", "2 of 4"), ("Rooms", "12")]), ("nav", )]
pr(G, "Photo Welcome Or Name Only?", hh, ("hh_photo", "Home Photo Welcome", "Photo and four tiles.", "visual", "photo"), ("hh_word", "Big Home Name", "Words, then tiles.", "calm", "word"))
pr(G, "Solid Or Outline Tiles?", hh, ("hh_solid", "Solid Color Tiles", "Bold color blocks.", "visual", "solid"), ("hh_outline", "Outline Tiles", "White with tinted icons.", "calm", "line"))
pr(G, "Season Tip Or None?", hh, ("hh_season", "Seasonal Tip Banner", "One care tip each season.", "action", "season"), ("hh_noseason", "No Tip", "Just the sections.", "calm", "nos"))
pr(G, "Install Card Or Bottom Bar?", hh, ("hh_install", "Add To Home Screen Card", "Prompt to save the app.", "action", "install"), ("hh_nav", "Bottom Tab Bar", "App-style tabs.", "focused", "nav"))

G = "Waiting On Others"
def wo(k):
    if k == "cards": return [HC, ("lbl", "Waiting On"), ("cards", [("Walls Maker", "Warranty reply · 5 days", "tag:Waiting"), ("Site Walk", "Serial photo", "tag:Sat")], LAGOON)]
    if k == "days": return [HC, ("lbl", "Waiting On"), ("raw", "".join(rect(14, 80 + i * 44, 212, 38, "#FFFFFF", LINE, 8) + t(24, 96 + i * 44, n, 9.5, INK, "khand") + t(24, 107 + i * 44, s, 6.5, MUTE) + t(216, 104 + i * 44, d, 18, LAGOON, "khand", anchor="end") for i, (n, s, d) in enumerate([("Walls Maker", "Warranty reply", "5d"), ("Site Walk", "Serial photo", "2d")])), 90)]
    if k == "nudge": return [HC, ("cards", [("Walls Maker", "No reply in 5 days")], LAGOON), ("btn", "Send A Nudge", "line", INK)]
    if k == "auto": return [HC, ("cards", [("Walls Maker", "Auto-nudge in 2 days")], LAGOON), ("p", "A follow-up goes out on its own.")]
    if k == "who": return [HC, ("lbl", "Waiting On · By Who"), ("cards", [("Walls Maker", "1 item"), ("Site Walk", "2 items")], LAGOON, "ic:clock")]
    if k == "what": return [HC, ("lbl", "Waiting On · By Item"), ("cards", [("Walls Warranty", "Walls Maker"), ("Heater 1 Serial", "Site Walk"), ("Garage Color", "Site Walk")], LAGOON)]
    return [HC]
pr(G, "Status Tag Or Days Count?", wo, ("wo_tag", "Waiting Tag", "Lagoon tag on each.", "calm", "cards"), ("wo_days", "Big Days Count", "How long it's been.", "visual", "days"))
pr(G, "Nudge Button Or Auto Follow-Up?", wo, ("wo_nudge", "Send A Nudge Button", "You choose when.", "action", "nudge"), ("wo_auto", "Auto Follow-Up", "Goes out on its own.", "quick", "auto"))
pr(G, "Group By Who Or By Item?", wo, ("wo_bywho", "Grouped By Who", "One row per person or company.", "focused", "who"), ("wo_byitem", "Listed By Item", "One row per missing thing.", "calm", "what"))

G = "Punch List"
def pl(k):
    L = [("Touch-Up Paint", "Hall · Example Painters"), ("Cabinet Door Gap", "Kitchen · Example Millwork"), ("Outlet Cover", "Bath 2 · Example Electric")]
    if k == "rows": return [HC, ("h", "Punch List", 16), ("cards", L, TERRA, "num")]
    if k == "photo": return [HC, ("h", "Punch List", 16), ("raw", "".join(photo(14, 80 + i * 52, 60, 44, ACC[i], "room") + t(82, 96 + i * 52, n, 9.5, INK, "khand") + t(82, 108 + i * 52, s, 6.5, MUTE) for i, (n, s) in enumerate(L)), 160)]
    if k == "trade": return [HC, ("lbl", "Example Painters"), ("cards", L[:1]), ("lbl", "Example Millwork"), ("cards", L[1:2]), ("lbl", "Example Electric"), ("cards", L[2:])]
    if k == "room": return [HC, ("tabs", ["Hall", "Kitchen", "Bath 2"], "under"), ("cards", L[:1])]
    if k == "swipe": return [HC, ("photo", 110, TERRA, "room", "Touch-Up Paint · Hall"), ("btn2", "Fixed", "Still Open")]
    if k == "tick": return [HC, ("h", "Punch List", 16), ("checks", [n for n, _ in L] + ["Door Stop", "Caulk Line"], JUNGLE, 2)]
    if k == "share": return [HC, ("h", "Punch List", 16), ("cards", L, TERRA), ("btn", "Send To Trades", "fill", INK)]
    return [HC, ("h", "Punch List", 16), ("cards", L, TERRA), ("btn", "Copy As Text", "line", INK)]
pr(G, "Numbered Rows Or Photo Rows?", pl, ("pl_rows", "Numbered Rows", "Item, room and trade.", "focused", "rows"), ("pl_photos", "Photo Beside Each", "See the spot.", "visual", "photo"))
pr(G, "By Trade Or By Room?", pl, ("pl_bytrade", "Grouped By Trade", "Each trade sees their list.", "focused", "trade"), ("pl_byroom", "Tabs By Room", "Walk room by room.", "visual", "room"))
pr(G, "One At A Time Or Tick List?", pl, ("pl_swipe", "One Item At A Time", "Photo, Fixed or Still Open.", "action", "swipe"), ("pl_tick", "Tick List", "Fast check-off.", "quick", "tick"))
pr(G, "Send To Trades Or Copy?", pl, ("pl_send", "Send To Trades Button", "Each trade gets theirs.", "action", "share"), ("pl_copy", "Copy As Text", "Paste where you want.", "calm", "copy"))

G = "Room Pages"
def rp(k):
    if k == "photo": return [HG, ("photo", 110, LAGOON, "room", "Kitchen"), ("cards", [("Finishes", "6 items"), ("Appliances", "5 items")])]
    if k == "list": return [HG, ("h", "Kitchen", 18), ("table", [("Cabinets", "Example Maker"), ("Counter", "Example Stone"), ("Paint", "Example White"), ("Pendants", "Example Brass")])]
    if k == "plan": return [HG, ("h", "Kitchen", 18), ("raw", rect(14, 74, 212, 110, SOFT, "none", 6) + rect(30, 90, 180, 20, "#FFFFFF", INK) + rect(80, 130, 80, 30, "#FFFFFF", INK) + t(120, 149, "Island", 7, MUTE, anchor="middle"), 118), ("p", "Tap a spot to see what's there.")]
    if k == "care": return [HG, ("h", "Kitchen", 18), ("lbl", "Care This Season"), ("checks", ["Clean range hood filter", "Seal stone counter"], JUNGLE, 0)]
    if k == "nocare": return [HG, ("h", "Kitchen", 18), ("table", [("Cabinets", "Example Maker"), ("Counter", "Example Stone")]), ("btn", "See Care Steps", "link", TERRA)]
    return [HG, ("h", "Kitchen", 18), ("tiles", [("Cabinets", "home"), ("Counter", "star"), ("Paint", "tag"), ("Lights", "clock")], 2, 54)]
pr(G, "Room Photo Or Item Table?", rp, ("rp_photo", "Room Photo On Top", "Then item groups.", "visual", "photo"), ("rp_table", "Item Table", "What's in the room.", "focused", "list"))
pr(G, "Drawn Plan Or Tiles?", rp, ("rp_plan", "Drawn Room Plan", "Tap a spot.", "visual", "plan"), ("rp_tiles", "Item Tiles", "Tap a tile.", "quick", "tiles"))
pr(G, "Care On The Room Page Or A Link?", rp, ("rp_care", "Season Care On The Page", "What to do in this room now.", "action", "care"), ("rp_carelink", "Care Behind A Link", "Keeps the room page short.", "calm", "nocare"))

publish(DID, "Construction Round 1: Warranty Status, Item Detail, Alerts And Badges, Finish Choices, Site Walk, Trade Directory, Preview Vs Live, Owner Handoff Email, Close-Out Dashboard, Home Guide Home Screen, Waiting On Others, Punch List, Room Pages", "Construction", pairs,
        {"brands": ["Weberman Construction close-out and Home Guide, example data only", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"team_sync": "/workspace/ops/team-sync/2026-10-13.md", "feed": "/workspace/ops/team-feed.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md"}}, seed=32)
