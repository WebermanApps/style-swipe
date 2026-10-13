#!/usr/bin/env python3
"""Build Style Swipe deck prop-1 (PUBLISHED): 25 pairs for the Prop agent (property management: two rental homes, rent
receipts, tenant and site ops). Based on the Oct 13 team-sync recap, team feed, and Prop's latest files (dashboard carousel,
receipt routine, call sheet, move-in walkthrough, address-change forms). Example data only: Oak House / Birch House,
Example Tenant, sample amounts. Pattern: tools/build_dashboard_2.py + draft_svg.py via team_kit.py. Run from repo root."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "prop-1"; pairs, O, add = deck("pr1_", "Prop")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
HB = ("hdr", "Prop", "Two Homes · Example Data", TERRA, "band")
HL = ("hdr", "Prop", "Two Homes · Example Data", TERRA, "logo")

G = "Property Carousel"
def car(k):
    b = [HL]
    if k == "tabs": b += [("tabs", ["Oak House", "Birch House"]), ("photo", 80, LAGOON, "house", "Oak House · Leased"), ("cards", [("Rent Logged", "Oct · on time", "tag:Done"), ("Mail Forwarding", "Due Oct 30", "tag:Due")])]
    elif k == "swipe": b += [("photo", 110, LAGOON, "house", "Oak House · Leased"), ("dots", 2, 0, TERRA), ("cards", [("Rent Logged", "Oct · on time", "tag:Done"), ("Mail Forwarding", "Due Oct 30", "tag:Due")])]
    elif k == "split": b += [("raw", photo(14, 60, 103, 70, LAGOON) + photo(123, 60, 103, 70, JUNGLE, "sun") + t(18, 142, "Oak House", 10, INK, "khand") + t(127, 142, "Birch House", 10, INK, "khand") + tag(18, 148, "2 Open", TERRA) + tag(127, 148, "All Clear", JUNGLE), 116), ("cards", [("Mail Forwarding", "Oak · Due Oct 30", "tag:Due")])]
    elif k == "list": b += [("cards", [("Oak House", "Leased · 2 open items", "tag:2 Open"), ("Birch House", "Vacant · walkthrough next", "tag:Next")], None, "ic:home", "line", 44), ("lbl", "Next Up"), ("cards", [("Mail Forwarding", "Due Oct 30")])]
    elif k == "big": b += [("h", "Oak House", 26), ("p", "Leased · Example Tenant · 2 open items"), ("photo", 96, LAGOON, "house"), ("btn2", "Open Items", "Next Home")]
    elif k == "small": b += [("raw", photo(14, 60, 60, 44, LAGOON) + t(82, 76, "Oak House", 12, INK, "khand") + t(82, 88, "Leased · 2 open items", 6.8, MUTE) + tag(82, 93, "Due Oct 30", TERRA), 52), ("cards", [("Rent Logged", "Oct"), ("Mail Forwarding", "Due Oct 30"), ("Smoke Detector Test", "Nov")])]
    elif k == "arrows": b += [("raw", ic("chev", 14, 62, 16, MUTE).replace("translate(14,62)", "translate(30,78) rotate(180)") + t(120, 74, "Oak House", 15, INK, "khand", anchor="middle") + ic("chev", 210, 62, 16, INK), 30), ("photo", 90, LAGOON, "house"), ("cards", [("Rent Logged", "Oct", "tag:Done")])]
    else: b += [("photo", 90, LAGOON, "house"), ("raw", "".join(rect(14 + i * 108, 152, 104, 6, TERRA if i == 0 else "#E5E0D8", "none", 3) for i in range(2)), 14), ("cards", [("Rent Logged", "Oct", "tag:Done")])]
    return b
pr(G, "Tabs Or Swipe Between Homes?", car, ("car_tabs", "Name Tabs On Top", "Two pill tabs pick the home.", "focused", "tabs"), ("car_swipe", "Big Photo, Swipe With Dots", "Swipe sideways; dots under the photo.", "visual", "swipe"))
pr(G, "Side By Side Or A List?", car, ("car_split", "Both Homes Side By Side", "Two small cards share the top.", "visual", "split"), ("car_list", "One Row Per Home", "Icon rows with a status tag.", "quick", "list"))
pr(G, "Big Name Or Compact Header?", car, ("car_bigname", "Big Home Name And Photo", "Name first, two buttons below.", "visual", "big"), ("car_compact", "Small Photo Beside The Name", "Leaves room for three items.", "quick", "small"))
pr(G, "Arrows Or A Progress Strip?", car, ("car_arrows", "Arrows Beside The Name", "Tap arrows to move between homes.", "action", "arrows"), ("car_strip", "Two-Segment Strip", "A strip under the photo shows which home.", "focused", "strip"))

G = "Rent Receipt"
def rc(k):
    head = [("raw", t(14, 30, "RECEIPT", 9, MUTE, "hind", 600, extra='letter-spacing="2"') + t(14, 52, "Rent Received", 20, INK, "khand"), 62)]
    rows = [("From", "Example Tenant"), ("Home", "Oak House"), ("For", "October 2026"), ("Amount", "$2,000 (Sample)"), ("Method", "Bank Transfer")]
    if k == "ledger": return head + [("table", rows, True), ("p", "Thank you. Keep this for your records.")]
    if k == "lined": return head + [("table", rows), ("p", "Thank you. Keep this for your records.")]
    if k == "bigamt": return head + [("word", "$2,000", 34, JUNGLE, "Sample Amount · October 2026", False), ("table", rows[:3] + rows[4:])]
    if k == "check": return [("gap", 20), ("raw", dot(120, 40, 18, JUNGLE + "22") + ic("check", 108, 28, 24, JUNGLE, 2), 46), ("h", "Rent Received", 18, INK, True), ("table", rows)]
    if k == "stripe": return [("raw", rect(0, 0, W, 6, TERRA), 6)] + head + [("table", rows)]
    if k == "plain": return head + [("table", rows)]
    if k == "sigline": return head + [("table", rows[:4]), ("raw", t(14, 0, "") + f'<path d="M20 {250} q10 -14 20 0 t20 0 t20 -6" fill="none" stroke="{INK}" stroke-width="1.2"/>' + ln(256, 14, 120) + t(14, 266, "Owner Signature", 6.5, MUTE), 0)]
    return head + [("table", rows[:4]), ("raw", rect(150, 236, 76, 22, "none", JUNGLE, 4, 1.5) + t(188, 251, "PAID", 11, JUNGLE, "khand", anchor="middle"), 0)]
pr(G, "Shaded Ledger Or Lined Rows?", rc, ("rc_ledger", "Shaded Ledger Rows", "Every other row shaded.", "focused", "ledger"), ("rc_lined", "Thin Lines Between Rows", "White rows with hairlines.", "calm", "lined"))
pr(G, "Big Amount Or Green Check Up Top?", rc, ("rc_bigamt", "Big Amount Leads", "Amount large in green.", "visual", "bigamt"), ("rc_check", "Green Check Leads", "Check mark, then the details.", "calm", "check"))
pr(G, "Color Stripe Or Pure White?", rc, ("rc_stripe", "Thin Terracotta Top Stripe", "One brand line across the top.", "visual", "stripe"), ("rc_plainwhite", "Pure White Page", "No color at all.", "calm", "plain"))
pr(G, "Signature Or Paid Stamp?", rc, ("rc_sig", "Signed At The Bottom", "Owner signature line.", "focused", "sigline"), ("rc_stamp", "Green Paid Stamp", "Outlined stamp, no signature.", "visual", "stamp"))

G = "Receipt Cover Email"
def em(k):
    b = [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 24)]
    if k == "short": b += [("lbl", "Subject: Your October Receipt"), ("p", "Hi, attached is your receipt for October. Thank you for paying on time.", 40), ("raw", rect(24, 0, 0, 0), 0), ("cards", [("Receipt-October.pdf", "1 page", "", "ic:card")])]
    elif k == "table": b += [("lbl", "Subject: Your October Receipt"), ("p", "Hi, here is a quick summary.", 40), ("table", [("Month", "October"), ("Amount", "Sample"), ("Status", "Received")]), ("cards", [("Receipt-October.pdf", "1 page", "", "ic:card")])]
    elif k == "btn": b += [("h", "Your Receipt Is Ready", 15, INK, True), ("p", "October 2026 · Oak House", 40, MUTE, True), ("btn", "View Receipt", "fill", TERRA)]
    elif k == "attach": b += [("h", "Your Receipt Is Ready", 15, INK, True), ("p", "October 2026 · Oak House", 40, MUTE, True), ("cards", [("Receipt-October.pdf", "Attached", "", "ic:card")])]
    elif k == "year": b += [("lbl", "Subject: Your 2026 Receipts"), ("p", "All receipts so far this year, in one email.", 40), ("cards", [("January", "", "tag:Sent"), ("February", "", "tag:Sent"), ("October", "", "tag:New")], None, "dot", "line", 26)]
    elif k == "month": b += [("lbl", "Subject: October Receipt"), ("p", "One email each month, sent after rent lands.", 40), ("cards", [("October", "Attached", "tag:New")])]
    elif k == "warm": b += [("h", "Thanks For October", 16), ("p", "Rent came in on the 1st. Your receipt is attached. Reply here if anything in the home needs a look.", 40)]
    else: b += [("h", "October Receipt", 16), ("p", "Receipt attached. Amount and date are on the PDF.", 40)]
    return b
pr(G, "Short Note Or Summary Table?", em, ("em_short", "Two-Line Note Plus PDF", "Plain note and the file.", "calm", "short"), ("em_table", "Small Summary Table", "Month, amount, status in rows.", "focused", "table"))
pr(G, "Button Or Attachment?", em, ("em_btn", "Terracotta View Button", "Opens the receipt page.", "action", "btn"), ("em_attach", "PDF Attached", "File card in the email.", "calm", "attach"))
pr(G, "One Yearly Email Or Monthly?", em, ("em_year", "Year-To-Date Bundle", "All months in one email.", "focused", "year"), ("em_month", "One Email Each Month", "Sent right after rent lands.", "quick", "month"))
pr(G, "Warm Or Brief Tone?", em, ("em_warm", "Warm Thank-You Tone", "Thanks plus an open door.", "calm", "warm"), ("em_brief", "Brief And Factual", "Just the receipt.", "quick", "brief"))

G = "Decisions Owed"
def dec(k):
    items = [("Pick Walkthrough Date", "Birch House"), ("Send Insurance Request", "Oak House"), ("Close Out Old Vendor", "Birch House")]
    if k == "yesno": return [HL, ("lbl", "Needs You"), ("raw", "".join(rect(14, 82 + i * 54, 212, 48, "#FFFFFF", LINE, 8) + t(24, 98 + i * 54, n, 10, INK, "khand") + t(24, 108 + i * 54, h, 6.5, MUTE) + btn(112 + i * 54, "Yes", "fill", INK, 150, 32, 14, 6) + btn(112 + i * 54, "Later", "line", INK, 188, 32, 14, 6) for i, (n, h) in enumerate(items)), 170)]
    if k == "list": return [HL, ("lbl", "Needs You"), ("cards", items, TERRA, "num")]
    if k == "one": return [HL, ("lbl", "One Thing Today"), ("h", items[0][0], 22), ("p", "Birch House · takes 1 minute"), ("btn", "Pick A Date", "fill", TERRA), ("btn", "2 More Waiting", "link", MUTE)]
    if k == "count": return [HL, ("stats", [("3", "Needs You"), ("1", "Due This Week"), ("0", "Late")], "tint"), ("cards", items, TERRA)]
    if k == "due": return [HL, ("lbl", "Needs You"), ("cards", [(n, h, f"tag:{d}") for (n, h), d in zip(items, ["Oct 20", "Oct 24", "Oct 30"])], TERRA)]
    if k == "home": return [HL, ("lbl", "Oak House"), ("cards", [items[1]], LAGOON), ("lbl", "Birch House"), ("cards", [items[0], items[2]], JUNGLE)]
    if k == "voice": return [HL, ("lbl", "Needs You"), ("cards", items, TERRA), ("input", "Answer By Voice Or Text...")]
    return [HL, ("lbl", "Needs You"), ("cards", items, TERRA), ("btn", "Answer All", "fill", INK)]
pr(G, "Buttons On Each Or A Plain List?", dec, ("dec_yesno", "Yes And Later On Each Card", "Answer right on the card.", "action", "yesno"), ("dec_list", "Numbered List", "Tap a row to answer.", "calm", "list"))
pr(G, "One At A Time Or Counts First?", dec, ("dec_one", "One Thing Today, Big", "The rest wait behind a link.", "focused", "one"), ("dec_counts", "Three Counts Then The List", "Needs You, Due, Late at a glance.", "visual", "count"))
pr(G, "By Due Date Or By Home?", dec, ("dec_due", "Due Date Tag On Each", "Sorted soonest first.", "focused", "due"), ("dec_byhome", "Grouped By Home", "Oak House, then Birch House.", "calm", "home"))
pr(G, "Answer Box Or Answer-All Button?", dec, ("dec_voice", "Answer Box Under The List", "Type or talk an answer.", "action", "voice"), ("dec_all", "One Answer-All Button", "Walks through each in turn.", "quick", "all"))

G = "Move-In Walkthrough"
def mv(k):
    rooms = ["Kitchen", "Living Room", "Bedroom 1", "Bath", "Garage"]
    if k == "check": return [HL, ("h", "Walkthrough", 18), ("bar", .4, JUNGLE, "2 Of 5 Rooms", "40%"), ("checks", rooms, JUNGLE, 2)]
    if k == "rooms": return [HL, ("h", "Walkthrough", 18), ("tiles", [(r, k2) for r, k2 in zip(rooms[:4], ["home", "star", "clock", "check"])], 2, 54)]
    if k == "photo": return [HL, ("lbl", "Kitchen · Room 1 Of 5"), ("photo", 110, LAGOON, "room"), ("btn2", "Looks Good", "Note Damage")]
    if k == "notes": return [HL, ("lbl", "Kitchen · Room 1 Of 5"), ("checks", ["Walls", "Floor", "Appliances", "Sink And Faucet"], JUNGLE, 1), ("input", "Add A Note...", TERRA, "star")]
    if k == "cal": return [HL, ("h", "Pick A Walkthrough Day", 15), ("cal", (17, 18, 21), TERRA), ("btn", "Send Times To Tenant", "fill", INK)]
    if k == "slots": return [HL, ("h", "Pick A Walkthrough Day", 15), ("cards", [("Sat Oct 17", "10 AM", "tag:Open"), ("Sun Oct 18", "2 PM", "tag:Open"), ("Wed Oct 21", "5 PM", "tag:Open")], JUNGLE), ("btn", "Send Times To Tenant", "fill", INK)]
    if k == "sign": return [HL, ("h", "All Rooms Done", 18), ("p", "Both sign below. A copy goes to each of you."), ("raw", rect(14, 140, 212, 50, SOFT, "none", 6) + t(22, 156, "Tenant", 7, MUTE) + rect(14, 198, 212, 50, SOFT, "none", 6) + t(22, 214, "Owner", 7, MUTE), 0)]
    return [HL, ("h", "All Rooms Done", 18), ("stats", [("5", "Rooms"), ("14", "Photos"), ("2", "Notes")]), ("btn", "Email The Report", "fill", TERRA)]
pr(G, "Checklist Or Room Tiles?", mv, ("mv_checklist", "Room Checklist With Progress", "Tick rooms off a list.", "focused", "check"), ("mv_tiles", "Room Tiles", "Tap a tile to start a room.", "visual", "rooms"))
pr(G, "Photo First Or Checklist First?", mv, ("mv_photofirst", "Photo, Then Good Or Damage", "One big photo per room.", "visual", "photo"), ("mv_itemfirst", "Items, Then A Note", "Walls, floor, appliances list.", "focused", "notes"))
pr(G, "Calendar Or Time Slots?", mv, ("mv_cal", "Month Calendar", "Pick days on a calendar.", "visual", "cal"), ("mv_slots", "Three Time Slots", "Offer three times as rows.", "quick", "slots"))
pr(G, "Sign On Screen Or Email Report?", mv, ("mv_sign", "Both Sign On The Phone", "Two signature boxes.", "action", "sign"), ("mv_report", "Counts, Then Email Report", "Rooms, photos, notes, then send.", "calm", "report"))

G = "Call Sheet"
def cs(k):
    items = [("Electric Company", "Stop service · ref #0000"), ("Trash Service", "Cancel pickup"), ("Internet", "Cancel and return box")]
    if k == "cards": return [HL, ("h", "Calls To Make", 16), ("cards", items, None, "ic:phone", "line", 40)]
    if k == "check": return [HL, ("h", "Calls To Make", 16), ("checks", [i[0] for i in items] + ["Water", "Gas"], JUNGLE, 1)]
    if k == "script": return [HL, ("lbl", "Call 1 Of 3 · Electric"), ("bubble", "Hi, I'd like to stop service at my rental on the 31st.", True), ("bubble", "Account number is on the bill, ending 0000."), ("btn2", "Done", "Skip")]
    if k == "bullets": return [HL, ("lbl", "Call 1 Of 3 · Electric"), ("table", [("Say", "Stop service on 31st"), ("Have Ready", "Account number"), ("Ask For", "Final bill by email")])]
    if k == "tapcall": return [HL, ("h", "Calls To Make", 16), ("raw", "".join(rect(14, 90 + i * 44, 212, 38, "#FFFFFF", LINE, 8) + t(24, 106 + i * 44, n, 9.5, INK, "khand") + t(24, 117 + i * 44, s, 6.5, MUTE) + rect(186, 96 + i * 44, 32, 26, JUNGLE, "none", 13) + ic("phone", 194, 101 + i * 44, 16, "#FFFFFF", 2) for i, (n, s) in enumerate(items)), 140)]
    if k == "copy": return [HL, ("h", "Calls To Make", 16), ("cards", [(n, s, "COPY") for n, s in items], LAGOON)]
    if k == "done": return [HL, ("ring", .33, JUNGLE, "1/3", "Calls Done"), ("cards", items[1:], JUNGLE)]
    return [HL, ("bar", .33, JUNGLE, "1 Of 3 Calls Done", "33%"), ("cards", items, JUNGLE)]
pr(G, "Cards Or A Checklist?", cs, ("cs_cards", "Phone Icon Cards", "One card per call.", "visual", "cards"), ("cs_checks", "Tick-Off Checklist", "Plain rows you tick.", "quick", "check"))
pr(G, "Script Bubbles Or Bullet Table?", cs, ("cs_script", "What To Say As Bubbles", "Reads like a chat.", "calm", "script"), ("cs_table", "Say, Have Ready, Ask For", "A tight three-row table.", "focused", "bullets"))
pr(G, "Tap To Call Or Copy Number?", cs, ("cs_tapcall", "Green Tap-To-Call Button", "Dial straight from the row.", "action", "tapcall"), ("cs_copy", "Copy Link On Each", "Copy the number to call later.", "calm", "copy"))
pr(G, "Ring Or Bar For Progress?", cs, ("cs_ring", "Progress Ring", "Big 1/3 in a ring.", "visual", "done"), ("cs_bar", "Thin Progress Bar", "A bar over the list.", "quick", "bar"))

G = "Tenant Requests"
def tq(k):
    if k == "form": return [("hdr", "Oak House", "Request A Fix", TERRA, "plain"), ("lbl", "What Needs A Look?"), ("tags", ["Plumbing", "Heat", "Appliance", "Other"]), ("input", "Describe It...", TERRA, "star"), ("btn", "Send Request", "fill", INK)]
    if k == "chat": return [("hdr", "Oak House", "Request A Fix", TERRA, "plain"), ("bubble", "What needs a look today?"), ("bubble", "The kitchen sink drips.", True), ("bubble", "Got it. Can you add a photo?"), ("input", "Type Or Talk...")]
    if k == "photo": return [("hdr", "Oak House", "Request A Fix", TERRA, "plain"), ("photo", 100, LAGOON, "room", "Add A Photo"), ("input", "Describe It...", TERRA, "star"), ("btn", "Send Request", "fill", INK)]
    if k == "urgency": return [("hdr", "Oak House", "Request A Fix", TERRA, "plain"), ("lbl", "How Urgent?"), ("cards", [("Emergency", "Water, heat, safety", "", "dot"), ("This Week", "Something broke"), ("Whenever", "Small fixes")], None, "dot", "line", 30), ("btn", "Next", "fill", INK)]
    if k == "status": return [("hdr", "Oak House", "My Requests", TERRA, "plain"), ("steps", ["Sent", "Seen", "Booked", "Fixed"], JUNGLE, 2), ("cards", [("Kitchen Sink Drip", "Booked Thu 10 AM", "tag:Booked")], JUNGLE)]
    if k == "timeline": return [("hdr", "Oak House", "My Requests", TERRA, "plain"), ("timeline", [("Sent", "Mon 9:12 AM"), ("Seen By Owner", "Mon 9:40 AM"), ("Plumber Booked", "Thu 10 AM")])]
    if k == "thanks": return [("gap", 40), ("raw", dot(120, 70, 22, JUNGLE + "22") + ic("check", 106, 56, 28, JUNGLE, 2), 60), ("h", "Request Sent", 20, INK, True), ("p", "You'll get a text when it's booked.", 46, MUTE, True)]
    return [("gap", 40), ("h", "Request Sent", 20, INK, True), ("p", "Here's what happens next:", 46, MUTE, True), ("steps", ["Seen", "Booked", "Fixed"], JUNGLE, 0)]
pr(G, "Form Or Chat For Requests?", tq, ("tq_form", "Short Form With Chips", "Pick a type, describe, send.", "focused", "form"), ("tq_chat", "Chat-Style Request", "Answers a few questions.", "calm", "chat"))
pr(G, "Photo First Or Urgency First?", tq, ("tq_photo", "Photo Leads", "Big Add A Photo box.", "visual", "photo"), ("tq_urgency", "Urgency Leads", "Emergency, This Week, Whenever.", "action", "urgency"))
pr(G, "Steps Or Timeline For Status?", tq, ("tq_steps", "Four-Step Tracker", "Sent, Seen, Booked, Fixed.", "visual", "status"), ("tq_timeline", "Timeline With Times", "Each step with its time.", "focused", "timeline"))
pr(G, "Check Mark Or What's Next?", tq, ("tq_thanks", "Big Green Check", "Simple sent message.", "calm", "thanks"), ("tq_next", "What Happens Next Steps", "Three steps after sending.", "focused", "next"))

G = "Deadline Reminders"
def dl(k):
    if k == "banner": return [HL, ("banner", "Mail Forwarding Due Oct 30", TERRA, "clock"), ("cards", [("Rent Logged", "Oct"), ("Smoke Test", "Nov")])]
    if k == "count": return [HL, ("word", "17", 44, TERRA, "Days Until Mail Forwarding Is Due"), ("btn", "Finish It Now", "fill", INK)]
    if k == "cal": return [HL, ("lbl", "October"), ("cal", (24, 30), TERRA), ("p", "24: Reminder · 30: Mail forwarding due")]
    if k == "list": return [HL, ("lbl", "Coming Up"), ("timeline", [("Oct 24 · Reminder", "Mail forwarding check"), ("Oct 30 · Due", "Mail forwarding"), ("Nov 2 · Routine", "Receipts run")])]
    if k == "text": return [("raw", rect(0, 0, W, H, SOFT), 0), ("gap", 40), ("bubble", "Prop: Mail forwarding is due Oct 30. Reply DONE when finished."), ("bubble", "DONE", True)]
    if k == "push": return [("raw", rect(0, 0, W, H, SOFT) + rect(14, 40, 212, 54, "#FFFFFF", "none", 12) + mono(22, 52, "P", TERRA, 20) + t(50, 60, "Prop", 9, INK, "khand") + t(50, 72, "Mail forwarding due Oct 30", 7.5, INK) + t(50, 83, "Tap to finish", 6.5, MUTE), 0)]
    if k == "soft": return [HL, ("cards", [("Mail Forwarding", "Due Oct 30", "tag:17 Days")], SAFFRON, "dot", "tint")]
    return [HL, ("cards", [("Mail Forwarding", "Due Oct 30", "tag:17 Days")], TERRA, "dot", "left")]
pr(G, "Banner Or Countdown?", dl, ("dl_banner", "Banner Over The Page", "A thin terracotta banner.", "quick", "banner"), ("dl_count", "Big Days-Left Number", "17 in large type.", "visual", "count"))
pr(G, "Calendar Or Timeline?", dl, ("dl_cal", "Month With Marked Days", "See dates on a calendar.", "visual", "cal"), ("dl_timeline", "Coming-Up Timeline", "Dates as a list.", "focused", "list"))
pr(G, "Text Or Phone Alert?", dl, ("dl_text", "Text Message, Reply Done", "Reply DONE to clear it.", "action", "text"), ("dl_push", "Phone Alert", "A lock-screen alert.", "quick", "push"))
pr(G, "Saffron Tint Or Terracotta Edge?", dl, ("dl_soft", "Soft Saffron Card", "Gentle tint, no alarm.", "calm", "soft"), ("dl_edge", "Terracotta Left Edge", "Stronger edge marker.", "action", "edge"))

G = "Morning Report Bar"
def mr(k):
    base = [("cards", [("Rent Logged", "Oak House"), ("Walkthrough Date", "Birch House")])]
    if k == "strip": return [HL, ("banner", "Morning Report · 3 updates", LAGOON, "star")] + base
    if k == "card": return [HL, ("raw", rect(14, 56, 212, 74, LAGOON + "12", "none", 8) + lbl(24, 72, "Morning Report", LAGOON) + t(24, 90, "All quiet. One date to pick.", 11, INK, "khand") + t(24, 104, "Rent logged · Mail due in 17 days", 7, MUTE) + link_(24, 120), 80)] + base
    if k == "bullets": return [HL, ("lbl", "Morning Report"), ("checks", ["Rent logged for October", "Walkthrough date still open", "Receipts run Nov 2"], LAGOON, 1)]
    if k == "sentence": return [HL, ("lbl", "Morning Report"), ("h", "One Date To Pick Today", 18), ("p", "Everything else is on track. Mail forwarding is due in 17 days.")]
    if k == "top": return [HL, ("banner", "Morning Report · 6:00 AM", LAGOON, "clock")] + base
    if k == "bottom": return [HL] + base + [("raw", rect(0, 250, W, 50, LAGOON) + t(14, 270, "Morning Report", 10, "#FFFFFF", "khand") + t(14, 282, "3 updates · tap to read", 6.5, "#FFFFFFCC"), 0)]
    if k == "time": return [HL, ("raw", lbl(14, 64, "Morning Report") + t(226, 64, "4:43 AM", 7, MUTE, "hind", 600, "end"), 14), ("p", "One date to pick. Rest on track.")] + base
    return [HL, ("raw", lbl(14, 64, "Morning Report") + tag(180, 56, "New", LAGOON, True), 14), ("p", "One date to pick. Rest on track.")] + base
def link_(x, y): return t(x, y, "READ ALL", 6.5, TERRA, "hind", 600, extra='letter-spacing="1" text-decoration="underline"')
pr(G, "Thin Strip Or Full Card?", mr, ("mr_strip", "One-Line Strip", "Tap to open the report.", "quick", "strip"), ("mr_card", "Tinted Report Card", "Headline plus one line.", "visual", "card"))
pr(G, "Bullets Or One Sentence?", mr, ("mr_bullets", "Three Bullets", "Ticked bullets.", "focused", "bullets"), ("mr_sentence", "One Headline Sentence", "A big headline and one line.", "calm", "sentence"))
pr(G, "Top Or Bottom Of The Page?", mr, ("mr_top", "Bar At The Top", "Right under the header.", "focused", "top"), ("mr_bottom", "Bar Pinned At The Bottom", "Lagoon bar along the bottom.", "visual", "bottom"))
pr(G, "Time Stamp Or New Tag?", mr, ("mr_time", "Time Stamp", "Shows when it was written.", "calm", "time"), ("mr_newtag", "New Tag", "Solid tag until read.", "action", "new"))

G = "Home Card"
def hc(k):
    if k == "photo": return [HL, ("photo", 120, LAGOON, "house", "Oak House"), ("tags", ["Leased", "2 Open Items"])]
    if k == "draw": return [HL, ("raw", rect(14, 60, 212, 120, "#FFFFFF", LINE, 8) + f'<path d="M70 160 V110 L120 76 L170 110 V160 Z" fill="none" stroke="{INK}" stroke-width="1.6"/>' + rect(110, 132, 20, 28, "none", INK, 0, 1.4) + t(120, 174, "Oak House", 10, INK, "khand", anchor="middle"), 128), ("tags", ["Leased", "2 Open Items"])]
    if k == "facts": return [HL, ("h", "Oak House", 18), ("table", [("Status", "Leased"), ("Lease Ends", "Example Date"), ("Open Items", "2"), ("Next Visit", "Nov")])]
    if k == "chips": return [HL, ("h", "Oak House", 18), ("stats", [("2", "Open"), ("Nov", "Next Visit"), ("OK", "Rent")])]
    if k == "color": return [HL, ("cards", [("Oak House", "Leased", "", "ic:home")], LAGOON, "ic:home", "left", 44), ("cards", [("Birch House", "Vacant", "", "ic:home")], JUNGLE, "ic:home", "left", 44)]
    if k == "mono": return [HL, ("cards", [("Oak House", "Leased"), ("Birch House", "Vacant")], INK, "ic:home", "line", 44)]
    if k == "quick": return [HL, ("photo", 90, LAGOON, "house", "Oak House"), ("tiles", [("Rent", "card"), ("Requests", "star"), ("Mail", "tag"), ("Docs", "cal")], 4, 50)]
    return [HL, ("photo", 90, LAGOON, "house", "Oak House"), ("cards", [("Rent", "Logged"), ("Requests", "1 open")])]
pr(G, "Photo Or Line Drawing?", hc, ("hc_photo", "Home Photo", "A real photo spot per home.", "visual", "photo"), ("hc_draw", "Line Drawing Of The Home", "Simple drawn house.", "calm", "draw"))
pr(G, "Fact Table Or Stat Chips?", hc, ("hc_facts", "Fact Table", "Status, lease end, items.", "focused", "facts"), ("hc_stats", "Three Stat Boxes", "Open, next visit, rent.", "visual", "chips"))
pr(G, "Color Per Home Or All Ink?", hc, ("hc_colorper", "Each Home Has A Color", "Lagoon and jungle edges.", "visual", "color"), ("hc_ink", "All Ink, No Color", "Same black for both.", "calm", "mono"))
pr(G, "Quick Tiles Or Rows Under The Photo?", hc, ("hc_tiles", "Four Quick Tiles", "Rent, Requests, Mail, Docs.", "action", "quick"), ("hc_rows", "Two Rows", "Rent and requests only.", "calm", "rows"))

G = "Vendor Contacts"
def vc(k):
    v = [("Plumber", "Example Plumbing Co"), ("HOA", "Example HOA Office"), ("Lawn", "Example Lawn Co")]
    if k == "rows": return [HL, ("h", "Contacts", 16), ("cards", v, None, "ic:phone")]
    if k == "cards": return [HL, ("h", "Contacts", 16), ("tiles", [("Plumber", "phone"), ("HOA", "home"), ("Lawn", "star"), ("Electric", "clock")], 2, 56)]
    if k == "search": return [HL, ("input", "Search Contacts...", INK, "search"), ("cards", v)]
    if k == "group": return [HL, ("lbl", "Oak House"), ("cards", v[:2]), ("lbl", "Birch House"), ("cards", v[2:])]
    if k == "last": return [HL, ("cards", [(n, s, r) for (n, s), r in zip(v, ["Used Sep", "Used Aug", "Used Jul"])])]
    if k == "rate": return [HL, ("cards", [(n, s, r) for (n, s), r in zip(v, ["tag:Great", "tag:OK", "tag:Great"])])]
    if k == "card": return [HL, ("raw", rect(14, 60, 212, 120, "#FFFFFF", LINE, 10) + mono(24, 72, "P", LAGOON, 30) + t(64, 86, "Example Plumbing Co", 11, INK, "khand") + t(64, 98, "Plumber · Oak House", 7, MUTE) + btn(146, "Call", "fill", JUNGLE, 24, 90, 22, 7) + btn(146, "Text", "line", INK, 122, 90, 22, 7), 128)]
    return [HL, ("table", [("Plumber", "Example Plumbing Co"), ("HOA", "Example HOA Office"), ("Lawn", "Example Lawn Co"), ("Electric", "Example Electric")])]
pr(G, "Rows Or Tiles?", vc, ("vc_rows", "Phone Icon Rows", "One row per contact.", "focused", "rows"), ("vc_tiles", "Trade Tiles", "Tap a trade to see who.", "visual", "cards"))
pr(G, "Search Or Group By Home?", vc, ("vc_search", "Search Box On Top", "Find a contact fast.", "quick", "search"), ("vc_group", "Grouped By Home", "Contacts under each home.", "calm", "group"))
pr(G, "Last Used Or Rating?", vc, ("vc_last", "Last Used Month", "Shows recency.", "focused", "last"), ("vc_rating", "Great Or OK Tag", "Shows how they did.", "visual", "rate"))
pr(G, "Contact Card Or Plain Table?", vc, ("vc_card", "One Big Contact Card", "Call and Text buttons.", "action", "card"), ("vc_table", "Plain Two-Column Table", "Trade and name only.", "calm", "table"))

G = "Forms To Sign"
def fm(k):
    if k == "preview": return [HL, ("h", "Form Ready To Sign", 15), ("raw", rect(40, 90, 160, 120, "#FFFFFF", LINE, 2) + "".join(rect(52, 104 + i * 12, 136 - (i % 3) * 20, 3, "#D6D0C6") for i in range(7)) + rect(52, 190, 60, 10, SAFFRON + "44"), 128), ("btn", "Sign", "fill", INK)]
    if k == "steps": return [HL, ("h", "Form Ready To Sign", 15), ("steps", ["Read", "Fill Date", "Sign", "Send"], TERRA, 0), ("btn", "Start", "fill", INK)]
    if k == "fields": return [HL, ("h", "Two Things Missing", 15), ("cards", [("Date You Moved Out", "Needed", "tag:Empty"), ("Your Signature", "Needed", "tag:Empty")], TERRA), ("btn", "Fill Them In", "fill", INK)]
    if k == "plain": return [HL, ("h", "Form Ready To Sign", 15), ("p", "Everything is filled in except the move-out date and your signature."), ("btn", "Open Form", "line", INK)]
    if k == "tag": return [HL, ("cards", [("Address Change Form", "Waiting on you", "tag:Sign")], TERRA)]
    if k == "pill": return [HL, ("cards", [("Address Change Form", "Waiting on you", "SIGN >")], TERRA, "ic:card")]
    if k == "done": return [HL, ("raw", rect(14, 60, 212, 60, JUNGLE + "12", "none", 8) + ic("check", 24, 76, 26, JUNGLE, 2) + t(60, 88, "Signed And Sent", 12, INK, "khand") + t(60, 100, "Copy saved to Docs", 7, MUTE), 66)]
    return [HL, ("timeline", [("Signed", "Today 9:40 AM"), ("Sent", "Today 9:41 AM"), ("Saved", "Docs folder")])]
pr(G, "Page Preview Or Steps?", fm, ("fm_preview", "Page Preview With Highlight", "Shows where to sign.", "visual", "preview"), ("fm_steps", "Four Steps", "Read, Fill, Sign, Send.", "focused", "steps"))
pr(G, "Missing Fields Or Plain Note?", fm, ("fm_fields", "Missing Fields As Cards", "Each blank spelled out.", "action", "fields"), ("fm_plain", "One Plain Sentence", "Says what's left in words.", "calm", "plain"))
pr(G, "Tag Or Arrow Cue?", fm, ("fm_tag", "Sign Tag", "Small terracotta tag.", "quick", "tag"), ("fm_arrow", "Sign Arrow Cue", "Text cue on the right.", "action", "pill"))
pr(G, "Done Card Or Timeline?", fm, ("fm_done", "Green Done Card", "One card says it's sent.", "calm", "done"), ("fm_timeline", "Signed, Sent, Saved Timeline", "Three dots with times.", "focused", "time"))

G = "Rent Log"
def rl(k):
    mo = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    if k == "bars": return [HL, ("lbl", "Rent Received · Sample"), ("bars", [1, 1, .6, 1, 1, 1], JUNGLE, mo)]
    if k == "dots": return [HL, ("lbl", "Rent Received · Sample"), ("raw", "".join(dot(28 + i * 38, 82, 9, JUNGLE if i != 2 else SAFFRON) + t(28 + i * 38, 104, m, 6.5, MUTE, anchor="middle") for i, m in enumerate(mo)), 44)]
    if k == "list": return [HL, ("cards", [(m, "Received", "tag:On Time") for m in mo[-4:]], JUNGLE, "dot", "line", 28)]
    if k == "grid": return [HL, ("raw", "".join(rect(14 + (i % 3) * 72, 60 + (i // 3) * 46, 66, 40, JUNGLE + "14", "none", 6) + t(22 + (i % 3) * 72, 78 + (i // 3) * 46, m, 10, INK, "khand") + t(22 + (i % 3) * 72, 90 + (i // 3) * 46, "On Time", 6.5, JUNGLE) for i, m in enumerate(mo)), 96)]
    if k == "streak": return [HL, ("word", "6", 44, JUNGLE, "Months On Time In A Row"), ("bars", [1] * 6, JUNGLE, mo, 30)]
    if k == "late": return [HL, ("banner", "One Month Was Partial · Jul", SAFFRON, "clock"), ("cards", [("Jul", "Partial", "tag:Check")], SAFFRON)]
    if k == "both": return [HL, ("tabs", ["Oak House", "Birch House"], "under"), ("bars", [1, 1, .6, 1, 1, 1], JUNGLE, mo)]
    return [HL, ("lbl", "Oak House"), ("bars", [1, 1, .6, 1, 1, 1], LAGOON, None, 34), ("lbl", "Birch House"), ("bars", [0, 0, 0, 0, 1, 1], JUNGLE, None, 34)]
pr(G, "Bars Or Dots Per Month?", rl, ("rl_bars", "Bar Per Month", "Short bar means partial.", "visual", "bars"), ("rl_dots", "Dot Per Month", "Green or saffron dots.", "calm", "dots"))
pr(G, "List Or Month Grid?", rl, ("rl_list", "Month Rows With Tags", "Newest four months.", "focused", "list"), ("rl_grid", "Six-Month Grid", "Tinted month boxes.", "visual", "grid"))
pr(G, "Streak Or Flag The Odd Month?", rl, ("rl_streak", "On-Time Streak Number", "Big streak count.", "visual", "streak"), ("rl_flag", "Flag Only The Odd Month", "Banner for anything off.", "action", "late"))
pr(G, "Tabs Or Stacked Homes?", rl, ("rl_tabs", "Tab Per Home", "Switch homes above the chart.", "focused", "both"), ("rl_stack", "Both Homes Stacked", "Two small charts.", "visual", "stack"))

del pairs[50:]
publish(DID, "Prop Round 1: Property Carousel, Rent Receipt, Receipt Email, Decisions Owed, Move-In Walkthrough, Call Sheet, Tenant Requests, Deadline Reminders, Morning Report Bar, Home Card, Vendor Contacts, Forms To Sign, Rent Log", "Prop", pairs,
        {"brands": ["Prop (property management), example data only", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"team_sync": "/workspace/ops/team-sync/2026-10-13.md", "feed": "/workspace/ops/team-feed.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md"}}, seed=31)
