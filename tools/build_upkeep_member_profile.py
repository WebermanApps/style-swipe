#!/usr/bin/env python3
"""Oct 15 2026 20:00 ICT (Max): Member Profile And Plan Deck for UpKeep. Card 1 = Re-Ask of Member Home -10 (reworded per
smartkeep/decks/carry-member-home.md). Confirmed facts only: Plus 4 seasonal visits a year; referral 1 free month after the neighbor's
first payment clears; prepay only (yearly or 2-year); Home Record transfers when you sell; add-on prices; Whole-Home Mold and Moisture
Scan wording; recall sentence. No reply times, arrival windows or tech names. Writes banks/src-upkeep-member-profile.json."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from team_kit import deck, TERRA, LAGOON, JUNGLE, SAFFRON, INK
pairs, O, add = deck("mpp_", "UpKeep"); HD = ("hdr", "Smart Upkeep", "Member App", SAFFRON, "logo", "S")
def P(g, ask, a, b, hd=True):
    h = [HD] if hd else []
    add(g, g, O(a[0], a[1], a[2], a[3], h + a[4]), O(b[0], b[1], b[2], b[3], h + b[4]), ask)
B = lambda s, c=SAFFRON: ("btn", s, "fill", c); BO = lambda s, c=LAGOON: ("btn", s, "outline", c)
TX = lambda s: ("p", s); W = lambda s: ("word", s, 22, INK, "")
C = lambda rows, c=None, h=30: ("cards", rows, c, "dot", "line", h)
def laptop(two):
    s = '<rect x="10" y="10" width="220" height="140" rx="6" fill="#FFFFFF" stroke="#1f1b17" stroke-width="2"/><rect x="0" y="150" width="240" height="8" rx="3" fill="#1f1b17"/>'
    blk = lambda x, y, w, h, c: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{c}"/>'
    if not two:
        s += blk(18, 16, 204, 128, "#FAF6EE") + blk(84, 22, 72, 8, "#1f1b17") + blk(84, 36, 72, 16, SAFFRON) + blk(84, 56, 72, 22, "#FFFFFF") + blk(84, 82, 72, 16, "#E8E3D8") + blk(84, 102, 72, 14, LAGOON + "33")
    else:
        s += blk(18, 16, 204, 128, "#FAF6EE") + blk(26, 22, 90, 8, "#1f1b17") + blk(26, 36, 90, 14, SAFFRON) + blk(26, 54, 90, 30, "#FFFFFF") + blk(124, 22, 90, 26, "#E8E3D8") + blk(124, 54, 90, 20, LAGOON + "33")
    return ("raw", s, 166)
P("Layout", "Re-Ask, Member Home On A Laptop Or Big Monitor: Keep The Phone Column Or Two Columns On Big Screens?",
  ("bs_one_rb", "Keep The Phone Column", "Same single column as the phone, centred, space on both sides.", "calm", [laptop(False), TX("Looks the same everywhere.")]),
  ("bs_two_rb", "Two Columns On Big Screens", "Left: greeting, plan line, next visit. Right: quick actions, Did You Know.", "focused", [laptop(True), TX("Phones keep one column.")]), hd=False)
P("Contact", "Contact Info: One Card With Edit Or Each Line Editable?",
  ("ci_card", "One Card With Edit", "Name, email, phone, one Edit link.", "calm", [C([("Jordan Sample", "Email · Phone", "Edit")], None, 44)]),
  ("ci_line", "Each Line Editable", "Edit next to each line.", "focused", [C([("Name", "", "Edit"), ("Email", "", "Edit"), ("Phone", "", "Edit")])]))
P("Contact", "Phone And Email Changes: Save Right Away Or Confirm With A Code?",
  ("pc_save", "Save Right Away", "Tap Save, done.", "quick", [("input", "(313) 555-0142", LAGOON, "mic"), B("Save")]),
  ("pc_code", "Confirm With A Code", "We send a code to the new number or email.", "focused", [("input", "Enter the code we sent", LAGOON, "mic"), B("Confirm")]))
P("Service Address", "Service Address: Show A House Picture Or Address Text Only?",
  ("sa_pic", "House Picture", "Small picture above the address.", "visual", [("photo", 70, LAGOON, "house", ""), TX("1234 Sample Lane, Royal Oak, MI")]),
  ("sa_txt", "Text Only", "Just the address line.", "calm", [C([("Home Address", "1234 Sample Lane, Royal Oak, MI", "")], None, 40)]))
P("Service Address", "Changing The Service Address: Edit In The App Or \"Message Us To Change It\"?",
  ("ac_edit", "Edit In The App", "Address form right here.", "quick", [("input", "New address", LAGOON, "mic"), B("Save Address")]),
  ("ac_msg", "Message Us", "Address changes go through the team.", "calm", [C([("Home Address", "1234 Sample Lane", "")], None, 34), BO("Message Us To Change It")]))
P("Plan Details", "Plan Screen Top: Plan Name And Visits Or Renewal Date First?",
  ("pt_plan", "Plan And Visits", "\"Plus · 4 seasonal visits a year\".", "calm", [C([("Current Plan", "Plus · 4 seasonal visits a year", "")], SAFFRON, 44)]),
  ("pt_renew", "Renewal First", "\"Next renewal\" on top.", "focused", [("stats", [("Apr 12", "Next Renewal")], "box"), C([("Plus", "4 seasonal visits a year", "")])]))
P("Plan Details", "Visits Left This Term: Progress Ring Or Simple Count?",
  ("vl_ring", "Progress Ring", "Ring fills as visits are done.", "visual", [("ring", .5, JUNGLE, "2 of 4", "visits this year")]),
  ("vl_count", "Simple Count", "\"2 of 4 visits done this year\".", "calm", [TX("2 of 4 seasonal visits done this year")]))
P("Plan Details", "What's Included: Checklist Or Grouped By Season?",
  ("wi_chk", "Checklist", "One list.", "calm", [("checks", ["4 seasonal visits a year", "Whole-Home Mold and Moisture Scan", "Gutter cleaning", "Home Record"], JUNGLE, 4)]),
  ("wi_season", "By Season", "Fold-out per season.", "focused", [C([("Spring", "", "›"), ("Summer", "", "›"), ("Fall", "", "›"), ("Winter", "", "›")])]))
P("Payment And Billing", "Payment Term Line: \"Paid Yearly\" Or \"2-Year Prepay\" Shown As A Chip Or A Sentence?",
  ("pt_chip", "Chip", "Small \"Pay Yearly\" tag.", "quick", [("tags", ["Plus", "Pay Yearly"])]),
  ("pt_sent", "Sentence", "\"Paid up front for the year. Renews April 12, 2028.\"", "calm", [TX("Paid up front for the year. Next renewal April 12, 2028.")]))
P("Payment And Billing", "Billing History: List Of Payments Or Receipts To Download?",
  ("bh_list", "List Of Payments", "Date and amount per row.", "calm", [C([("Apr 2026", "Plus · yearly", "Paid"), ("Apr 2027", "Renewal", "Due")])]),
  ("bh_rcpt", "Download Receipts", "One button per receipt.", "focused", [C([("Apr 2026 receipt", "", "")], None, 30), BO("Download Receipt")]))
P("Payment And Billing", "Add-On Prices On The Plan Screen: List With +$/Month Or Show Two And \"See All\"?",
  ("ap_list", "Full List", "Every add-on with its price.", "calm", [C([("Exterior Window Washing", "", "+$19/mo"), ("Chimney Sweep", "", "+$21/mo"), ("Radon Test", "", "+$8/mo"), ("Air Duct Cleaning", "", "+$33/mo")], None, 26)]),
  ("ap_two", "Two Plus See All", "Shorter screen.", "quick", [C([("Exterior Window Washing", "", "+$19/mo"), ("Chimney Sweep", "", "+$21/mo")], None, 26), ("btn", "See All Add-Ons", "link", LAGOON)]))
P("Referral Credits", "Referral Credits: Big Number Or Months Added To Your Term?",
  ("rc_big", "Big Number", "\"1 free month earned\".", "visual", [("stats", [("1", "Free Month Earned")], "box")]),
  ("rc_term", "Added To Your Term", "Shows the free month at the end of the term.", "calm", [("timeline", [("Term ends", "April 2028"), ("+1 free month", "from Neighbor A.")])]))
P("Referral Credits", "Pending Referrals: Show \"Waiting On First Payment\" Or Hide Until Credited?",
  ("pr_show", "Show Pending", "Credited after their first payment clears.", "calm", [C([("Neighbor A.", "", "+1 month"), ("Neighbor B.", "Waiting on first payment", "Pending")])]),
  ("pr_hide", "Hide Until Credited", "Only credited months.", "quick", [C([("Neighbor A.", "", "+1 month")])]))
P("Home Record Access", "Home Record From Profile: Shortcut Card Or Only In The Record Tab?",
  ("hr_card", "Shortcut Card", "\"Your Home Record\" card in Profile.", "focused", [C([("Your Home Record", "Equipment, scans, Proof Pack", "›")], LAGOON, 44)]),
  ("hr_tab", "Record Tab Only", "No duplicate in Profile.", "calm", [W("Profile"), C([("Contact", "", ""), ("Notifications", "", "")])]))
P("Home Record Access", "Selling Your Home: \"Home Record Transfers When You Sell\" Card Or A Line In The Record?",
  ("sh_card", "Own Card", "With a Transfer button.", "focused", [C([("Selling your home?", "Home Record transfers when you sell", "")], SAFFRON, 44), BO("Transfer Home Record")]),
  ("sh_line", "Line In The Record", "Small note at the bottom.", "calm", [TX("Home Record transfers when you sell.")]))
P("Home Record Access", "Recall Monitoring Note In Profile: Show The Full Sentence Or Short Status?",
  ("rm_full", "Full Sentence", "Exact wording.", "calm", [TX("We monitor logged equipment for published manufacturer recalls and notify you. We do not guarantee that every recall will be identified.")]),
  ("rm_short", "Short Status", "\"Recall monitoring on\", tap for details.", "quick", [C([("Recall Monitoring", "On · tap for details", "›")])]))
P("Notifications", "Notification Settings: Toggles In Profile Or Its Own Screen?",
  ("ns_prof", "In Profile", "Three toggles under Contact.", "calm", [("toggles", [("Visit reminders", True), ("Visit reports ready", True), ("Tips and Did You Know", False)])]),
  ("ns_own", "Own Screen", "\"Notifications ›\" opens a page.", "quick", [C([("Notifications", "3 settings", "›")])]))
P("Notifications", "Scan Results Notice: \"Whole-Home Mold And Moisture Scan Results Ready\" Or Part Of The Visit Report Notice?",
  ("sr_own", "Own Notice", "Separate alert for scan results.", "focused", [("banner", "Whole-Home Mold and Moisture Scan results ready", LAGOON, "check")]),
  ("sr_part", "Part Of Visit Report", "One alert per visit.", "calm", [("banner", "Your Fall Visit report is ready", LAGOON, "check")]))
# Member Tools skips 05 + 09 (Max 19:53) re-asked as cards 2 and 3
mt = json.load(open("decks/upkeep-member-tools-member-tools-deck.json"))["pairs"]
ra = []
for n in ("05", "09"):
    q = json.loads(json.dumps(next(x for x in mt if x["id"].endswith("-" + n))))
    q["ask"] = "Re-Ask, " + q["ask"]; q["carried_from"] = q["id"]; q["purpose"] = "retest"
    for k in "AB": q["option" + k]["id"] += "_ra"
    ra.append(q)
pairs[1:1] = ra
assert len(pairs) == 20, len(pairs)
pairs[0]["carried_from"] = "upkeep-member-home-member-home-deck-10"; pairs[0]["purpose"] = "retest"
json.dump({"pairs": pairs}, open("banks/src-upkeep-member-profile.json", "w"), indent=1, ensure_ascii=False); print(len(pairs))
