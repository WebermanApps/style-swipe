#!/usr/bin/env python3
"""Oct 15 2026 (Max 19:36 ICT): two UpKeep decks about the Smart Upkeep member app prototype
(source smartkeep/funnel-app/member/index.html, crops of smartkeep/member-app/*-393.png in img/smartkeep-member/).
Fact rules: licensed tech (not always the same person); online booking coming ('Book a Visit' ok); Mold and Moisture Scan in
every plan; gutters Plus + Complete only; storm checks Complete only; 'Most Popular' label. No other service claims.
Writes banks/src-upkeep-member-home.json and banks/src-upkeep-member-tools.json; publish with tools/ready_shelf.py build --source."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import team_kit
from team_kit import deck, TERRA, LAGOON, JUNGLE, SAFFRON, INK
from PIL import Image
def b_img(y, name, cap=""):
    w0, h0 = Image.open(f"img/smartkeep-member/{name}.png").size; h = round(212 * h0 / w0)
    src = f"img/smartkeep-member/{name}.png"
    return f'<image href="{src}" xlink:href="{src}" x="14" y="{y}" width="212" height="{h}" preserveAspectRatio="xMidYMid meet"/>', h + 6
team_kit.BLK["img"] = b_img
def mk(prefix, sub):
    pairs, O, add = deck(prefix, "UpKeep"); HD = ("hdr", "Smart Upkeep", sub, SAFFRON, "logo", "S")
    def P(g, ask, a, b, hd=True):
        h = [HD] if hd else []
        add(g, g, O(a[0], a[1], a[2], a[3], h + a[4]), O(b[0], b[1], b[2], b[3], h + b[4]), ask)
    return pairs, P
B = lambda s, c=SAFFRON: ("btn", s, "fill", c)
BO = lambda s, c=LAGOON: ("btn", s, "outline", c)
W = lambda s, c=INK, sub="": ("word", s, 22, c, sub)
TX = lambda s: ("p", s)
IMG = lambda n: ("img", n)
NAV6 = ("nav", (("Home", "home"), ("Visits", "cal"), ("Record", "check"), ("Plan", "tag"), ("Refer", "star")))
NAV4 = ("nav", (("Home", "home"), ("Visits", "cal"), ("Record", "check"), ("More", "star")))

# ---------------- Member Home Deck ----------------
hp, P = mk("mah_", "Member App")
P("Sign In", "Sign In Screen: Email And Password Or Email Me A Sign-In Link?",
  ("si_pw", "Email And Password", "As in the prototype.", "calm", [IMG("login")], ), 
  ("si_link", "Email Me A Link", "Type your email, tap the link we send.", "quick", [W("Member Sign In"), ("input", "you@example.com", LAGOON, "mic"), B("Email Me A Sign-In Link")]), hd=False)
P("Sign In", "Face ID Button: Under Sign In Or Offered After First Sign In?",
  ("fi_under", "Under Sign In", "Always on the sign-in screen.", "calm", [W("Member Sign In"), B("Sign In"), BO("Sign In With Face ID")]),
  ("fi_after", "Offered After", "Ask once after the first sign in.", "focused", [W("Use Face ID Next Time?"), B("Turn On Face ID"), ("btn", "Not Now", "link", INK)]), hd=False)
P("Sign In", "Sign In Button: Saffron Fill Or Lagoon Fill?",
  ("sb_saff", "Saffron", "Matches the plan card.", "visual", [W("Member Sign In"), B("Sign In", SAFFRON)]),
  ("sb_lag", "Lagoon", "Matches links and Face ID.", "calm", [W("Member Sign In"), B("Sign In", LAGOON)]), hd=False)
P("Sign In", "Sign In Header: Logo Plus Title Or Logo Only?",
  ("sh_both", "Logo Plus Title", "\"Member Sign In\" under the logo.", "calm", [("hdr", "Smart Upkeep", "", SAFFRON, "logo", "S"), W("Member Sign In"), B("Sign In")]),
  ("sh_logo", "Logo Only", "Cleaner, straight to the fields.", "quick", [("hdr", "Smart Upkeep", "", SAFFRON, "logo", "S"), ("input", "Email", LAGOON, "mic"), B("Sign In")]), hd=False)
P("Greeting", "Greeting: \"Good Evening, Jordan\" Or Just \"Hi, Jordan\"?",
  ("gr_time", "Time Of Day Plus Name", "Small label, big hello.", "calm", [("lbl", "GOOD EVENING"), W("Hi, Jordan")]),
  ("gr_hi", "Just Hi", "One short line.", "quick", [W("Hi, Jordan")]))
P("Top Of Home", "Top Of Home: Plan Card First Or Next Visit First?",
  ("th_plan", "Plan Card First", "Plan, then next visit.", "calm", [("cards", [("Your Plan", "Plus", "")], SAFFRON, "dot", "line", 36), ("cards", [("Next Visit", "Winter Visit", "")], None, "dot", "line", 30)]),
  ("th_visit", "Next Visit First", "When we come next, then plan.", "focused", [("cards", [("Next Visit", "Winter Visit", "")], LAGOON, "dot", "line", 36), ("cards", [("Your Plan", "Plus", "")], None, "dot", "line", 30)]))
P("Top Of Home", "Plan Card: Big Saffron Card Or Slim Plan Line?",
  ("pc_big", "Big Saffron Card", "Plus · Quarterly Care, 4 seasonal visits a year (one per quarter).", "visual", [IMG("plan")]),
  ("pc_slim", "Slim Line", "\"Plus\" chip with a link to Plan.", "calm", [("tags", ["Plus", "View Plan"]), ("cards", [("Next Visit", "Winter Visit", "")], None, "dot", "line", 34)]))
P("Top Of Home", "Plan Card Badge: Show \"Most Popular\" On Plus Or No Badge For Members?",
  ("pb_show", "Show Most Popular", "Same label as the price page.", "visual", [("cards", [("Your Plan", "Plus", "Most Popular")], SAFFRON, "dot", "line", 48)]),
  ("pb_none", "No Badge", "Members already chose.", "calm", [("cards", [("Your Plan", "Plus", "")], SAFFRON, "dot", "line", 48)]))
P("Next Visit", "Next Visit Card: Date Window Or Countdown?",
  ("nv_win", "Date Window", "We confirm your visit day and arrival window ahead of time.", "calm", [("cards", [("Winter Visit", "Dec 8 to Dec 12", "")], None, "dot", "line", 40)]),
  ("nv_count", "Countdown", "Days until the visit window.", "focused", [("stats", [("54", "Days To Visit")], "box"), TX("Winter Visit window")]))
P("Next Visit", "Your Tech On The Next Visit Card: \"Your Licensed Tech\" Or No Tech Line?",
  ("tl_show", "Your Licensed Tech", "Licensed every time; not always the same person.", "calm", [("cards", [("Winter Visit", "Your licensed tech", "")], None, "dot", "line", 40)]),
  ("tl_none", "No Tech Line", "Date only.", "quick", [("cards", [("Winter Visit", "Dec 8 to Dec 12", "")], None, "dot", "line", 40)]))
P("Quick Actions", "Quick Actions: Three Tiles Or Four Tiles?",
  ("qa_3", "Three Tiles", "Request a Visit, Message Us, Add a Photo.", "calm", [IMG("qa")]),
  ("qa_4", "Four Tiles", "Adds Book a Visit (online booking coming).", "focused", [("tiles", [("Request a Visit", "cal"), ("Message Us", "star"), ("Add a Photo", "check"), ("Book a Visit", "clock")], 2, 46)]))
P("Quick Actions", "First Quick Action: Request A Visit Or Message Us?",
  ("fa_req", "Request A Visit", "As now.", "calm", [("tiles", [("Request a Visit", "cal"), ("Message Us", "star")], 2, 52)]),
  ("fa_msg", "Message Us", "Talk first, then book. We'll get back to you soon.", "focused", [("tiles", [("Message Us", "star"), ("Request a Visit", "cal")], 2, 52)]))
P("Quick Actions", "Quick Action Style: Icon Tiles Or Pill Buttons?",
  ("qs_tiles", "Icon Tiles", "Three boxes with icons.", "visual", [IMG("qa")]),
  ("qs_pills", "Pill Buttons", "One row of rounded buttons.", "quick", [("tags", ["Request a Visit", "Message Us", "Add a Photo"])]))
P("Quick Actions", "Booking Button Wording: \"Book a Visit\" Or \"Request a Visit\"?",
  ("bw_book", "Book a Visit", "Online booking is coming.", "quick", [B("Book a Visit")]),
  ("bw_req", "Request a Visit", "Until online booking is live.", "calm", [B("Request a Visit")]))
P("Did You Know", "Did You Know Hint: Keep It On Home Or Move It Into Visits?",
  ("dk_home", "Keep On Home", "Bottom of Home, as now.", "calm", [IMG("hint")]),
  ("dk_vis", "Move Into Visits", "Home stays shorter.", "quick", [("cards", [("Next Visit", "Winter Visit", "")], None, "dot", "line", 34), ("tiles", [("Request a Visit", "cal"), ("Message Us", "star")], 2, 44)]))
P("Did You Know", "Did You Know Hint: About Your Own Home Or General Tips?",
  ("dh_own", "Your Own Home", "From your last Whole-Home Mold and Moisture Scan.", "focused", [("banner", "Did you know? Your moisture scan flagged one spot.", LAGOON, "check")]),
  ("dh_gen", "General Tips", "Seasonal tips for any home.", "calm", [("banner", "Did you know? Seasonal home tip.", LAGOON, "star")]))
P("Did You Know", "Did You Know Hint: Light Blue Box Or Plain White Card?",
  ("dc_blue", "Light Blue Box", "As in the prototype.", "visual", [IMG("hint")]),
  ("dc_white", "Plain White Card", "Matches the other cards.", "calm", [("cards", [("Did you know?", "Your scan flagged one spot", "")], None, "dot", "line", 44)]))
P("Navigation", "Bottom Tabs: Six Tabs Or Four Tabs Plus More?",
  ("nt_6", "Six Tabs", "Home, Visits, Record, Plan, Refer, Profile.", "calm", [IMG("tabs")]),
  ("nt_4", "Four Plus More", "Plan, Refer, Profile under More.", "quick", [W("Hi, Jordan"), NAV4]))
P("Navigation", "Share Button At Top Right: Keep Or Drop For Members?",
  ("sr_keep", "Keep Share", "Logo left, Share right.", "calm", [("hdr", "Smart Upkeep", "Share", SAFFRON, "logo", "S"), W("Hi, Jordan")]),
  ("sr_drop", "Drop It", "Logo only on member screens.", "quick", [("hdr", "Smart Upkeep", "", SAFFRON, "logo", "S"), W("Hi, Jordan")]), hd=False)
P("Layout", "Home On A Big Screen: One Phone Column Or Two Columns?",
  ("bs_one", "One Column", "Same as phone, centred.", "calm", [("cards", [("Your Plan", "Plus", "")], SAFFRON, "dot", "line", 34), ("cards", [("Next Visit", "Winter Visit", "")], None, "dot", "line", 34)]),
  ("bs_two", "Two Columns", "Plan and visit side by side.", "focused", [("stats", [("Plus", "Your Plan"), ("Dec 8", "Next Visit")], "box")]))
assert len(hp) == 20, len(hp)

# ---------------- Member Tools Deck ----------------
tp, P = mk("mat_", "Member App")
P("Visits", "Visits Page: Upcoming And Past In Two Cards Or One Timeline?",
  ("vp_two", "Two Cards", "As in the prototype.", "calm", [IMG("visits")]),
  ("vp_line", "One Timeline", "All visits on one line, newest on top.", "focused", [("timeline", [("Winter Visit", "Scheduled"), ("Fall Visit", "Done"), ("Summer Visit", "Done")])]))
P("Visits", "Visit Status Chips: Words Or Coloured Dots?",
  ("vs_words", "Words", "Scheduled, Planned, Done.", "calm", [("tags", ["Scheduled", "Planned", "Done"])]),
  ("vs_dots", "Coloured Dots", "Dot only, word on tap.", "quick", [("cards", [("Winter Visit", "Dec 8 to Dec 12", ""), ("Fall Visit", "Sep 18", "")], None, "dot", "line", 30)]))
P("Visit Reports", "Visit Report Opens With: Checklist Or Tech Notes?",
  ("vr_chk", "Checklist", "What was done, then notes.", "calm", [("checks", ["Furnace filter changed", "Whole-Home Mold and Moisture Scan", "Smoke and CO checks"], JUNGLE, 3)]),
  ("vr_notes", "Tech Notes", "Summary first, checklist below.", "focused", [("bubble", "All systems normal. One spot to recheck.", False, LAGOON), ("checks", ["Whole-Home Mold and Moisture Scan"], JUNGLE, 1)]))
P("Visit Reports", "Report Photos: Three-Up Grid Or Swipe Carousel?",
  ("rp_grid", "Three-Up Grid", "Small photos in a row.", "visual", [("photos", 3, 56)]),
  ("rp_car", "Swipe Carousel", "One big photo, swipe for more.", "focused", [("photo", 110, LAGOON, "house", ""), ("dots", 3, 1, INK)]))
P("Visits", "Upcoming Visit Note: \"We Confirm Your Visit Day And Arrival Window Ahead Of Time\" Or Date Window Only?",
  ("uv_note", "Show The Note", "Under the date window.", "calm", [("cards", [("Winter Visit", "Dec 8 to Dec 12", "")], None, "dot", "line", 34), ("p", "We confirm your visit day and arrival window ahead of time.")]),
  ("uv_only", "Date Window Only", "Shorter list.", "quick", [("cards", [("Winter Visit", "Dec 8 to Dec 12", "")], None, "dot", "line", 34)]))
P("Home Record", "Home Record Top: Equipment List Or Four Section Tabs?",
  ("hr_list", "Equipment List", "As in the screenshot.", "calm", [IMG("equip")]),
  ("hr_tabs", "Four Section Tabs", "Appliances, Moisture Scan, Recalls, Proof Pack.", "focused", [("tabs", ["Appliances", "Scan", "Recalls", "Proof"], "pill"), ("cards", [("Gas Furnace", "Tuned Sep 2026", "")], None, "dot", "line", 32)]))
P("Home Record", "Equipment Rows: Icon Beside Or Photo Beside?",
  ("er_icon", "Icon Beside", "Drawn icon per appliance.", "calm", [IMG("equip")]),
  ("er_photo", "Photo Beside", "Photo from the visit.", "visual", [("photos", 1, 48), ("cards", [("Gas Furnace", "Installed 2014", "")], None, "dot", "line", 30)]))
P("Home Record", "Whole-Home Mold And Moisture Scan Results: Row Per Area Or One Summary Line?",
  ("ms_rows", "Row Per Area", "Normal / recheck chip per spot.", "calm", [IMG("scan")]),
  ("ms_sum", "One Summary Line", "\"4 normal, 1 to recheck\".", "quick", [("stats", [("4", "Normal"), ("1", "Recheck")], "box")]))
P("Home Record", "Whole-Home Mold And Moisture Scan Label: \"In Every Plan\" Tag Or No Tag?",
  ("mt_tag", "In Every Plan Tag", "Pinless moisture meter and thermal camera; not a lab mold test.", "focused", [("tags", ["Whole-Home Mold and Moisture Scan", "In Every Plan"])]),
  ("mt_none", "No Tag", "Title only.", "calm", [("tags", ["Whole-Home Mold and Moisture Scan"])]))
P("Home Record", "Recall Monitoring: Status Card Or Line In Equipment?",
  ("rm_card", "Status Card", "We monitor logged equipment for published manufacturer recalls and notify you.", "calm", [("cards", [("Recall Monitoring", "Logged equipment", "")], JUNGLE, "dot", "line", 44)]),
  ("rm_line", "Line In Equipment", "Small note under each appliance.", "quick", [("cards", [("Gas Furnace", "Recall monitoring on", ""), ("Central AC", "Recall monitoring on", "")], None, "dot", "line", 30)]))
P("Home Record", "Proof Pack: Download Button Or Share Link?",
  ("pp_dl", "Download Button", "PDF to keep.", "calm", [("cards", [("Maintenance Proof Pack", "Record of your visits for warranty claims", "")], None, "dot", "line", 40), B("Download Proof Pack")]),
  ("pp_share", "Share Link", "Send a link instead of a file. Selling? Gift the buyers 3 months free.", "quick", [("cards", [("Maintenance Proof Pack", "Record of your visits for warranty claims", "")], None, "dot", "line", 40), BO("Share Proof Pack")]))
P("Billing", "Add-Ons On Plan And Billing: Price Only Or Price Plus Add Button?",
  ("ab_price", "Price Only", "\"+$/month\" on the right.", "calm", [("cards", [("Exterior Window Washing", "", "+$19/month"), ("Chimney Sweep", "", "+$21/month")], None, "dot", "line", 30)]),
  ("ab_add", "Price Plus Add", "Tap Add to request it.", "focused", [("cards", [("Exterior Window Washing", "+$19/month", "")], None, "dot", "line", 30), BO("Add")]))
P("Billing", "What's Included: Full Checklist Or Top Items Plus See All?",
  ("wi_full", "Full Checklist", "Everything in the plan, open.", "calm", [("checks", ["Whole-Home Mold and Moisture Scan", "Gutter cleaning", "Home Record transfers when you sell"], JUNGLE, 3)]),
  ("wi_top", "Top Items Plus See All", "Three lines, link for more.", "quick", [("checks", ["Whole-Home Mold and Moisture Scan", "Gutter cleaning"], JUNGLE, 2), ("btn", "See All", "link", LAGOON)]))
P("Billing", "Upgrade Prompt: Show What Complete Adds Or No Upgrade Prompt?",
  ("up_show", "Show What Complete Adds", "Plus members see storm checks are in Complete.", "focused", [("banner", "Storm checks come with Complete", SAFFRON, "star"), BO("See Complete")]),
  ("up_none", "No Prompt", "Plan page stays plain.", "calm", [("cards", [("Current Plan", "Plus", "")], SAFFRON, "dot", "line", 40)]))
P("Billing", "Payment Card Row: On Plan And Billing Or In Profile?",
  ("pm_plan", "On Plan And Billing", "Card row under add-ons.", "calm", [("cards", [("Card ending 0000", "Edit", "")], None, "dot", "line", 34)]),
  ("pm_prof", "In Profile", "With contact details.", "quick", [("cards", [("Contact", "Edit", ""), ("Payment Card", "Edit", "")], None, "dot", "line", 30)]))
P("Referrals", "Refer A Neighbor: Own Tab Or Card Inside Profile?",
  ("rn_tab", "Own Tab", "Refer in the bottom tabs.", "visual", [W("Refer a Neighbor"), NAV6]),
  ("rn_card", "Card In Profile", "Fewer tabs.", "calm", [W("Profile"), ("cards", [("Refer a Neighbor", "Share your link", "")], TERRA, "dot", "line", 40)]))
P("Referrals", "Referral Link: Copy Button Or Phone Share Sheet?",
  ("rl_copy", "Copy Button", "1 free month per neighbor who joins; no limit.", "calm", [("input", "smartupkeep.ai/r/...", LAGOON, "mic"), B("Copy Share Link")]),
  ("rl_share", "Share Sheet", "Opens text, mail, apps.", "quick", [B("Share With A Neighbor")]))
P("Referrals", "Referral Progress: List Of Neighbors Or Big Count Only?",
  ("rp_list", "List Of Neighbors", "Credited after their first payment clears, added at the end of your term.", "calm", [("cards", [("Neighbor A.", "", "+1 month"), ("Neighbor B.", "", "Pending")], None, "dot", "line", 30)]),
  ("rp_big", "Big Count Only", "One number.", "quick", [("stats", [("1", "Free Month Earned")], "box")]))
P("Notifications", "Notifications: Three Toggles Or Visit Reminders Only?",
  ("nf_3", "Three Toggles", "Reminders, reports ready, Did You Know tips.", "calm", [("toggles", [("Visit reminders", True), ("Visit reports ready", True), ("Tips and Did You Know", False)])]),
  ("nf_1", "Reminders Only", "One switch.", "quick", [("toggles", [("Visit reminders", True)])]))
P("Notifications", "Report Ready Alert: Push Notification Or Email?",
  ("ra_push", "Push", "Phone alert opens the report.", "quick", [("banner", "Your Fall Visit report is ready", LAGOON, "check")]),
  ("ra_mail", "Email", "Email with a link to the app.", "calm", [("cards", [("Email", "Your Fall Visit report is ready", "")], None, "dot", "line", 40)]))
assert len(tp) == 20, len(tp)

for name, ps in (("upkeep-member-home", hp), ("upkeep-member-tools", tp)):
    json.dump({"pairs": ps}, open(f"banks/src-{name}.json", "w"), indent=1, ensure_ascii=False); print(name, len(ps))
