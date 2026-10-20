#!/usr/bin/env python3
"""Oct 16 2026 (Max via Branding): two UpKeep decks, 20 this-or-that pairs each, drawn split-screen page mockups (team_kit blocks).
 - Customer Profile Page Deck (smartupkeep.ai /member/: Home, Home Record, Visits, Profile)
 - Technician Page Deck (smartupkeep.ai /tech/: today's visits, checklist, readings, Visit Report, Van Inventory, Certifications)
Source: live member/tech prototypes (sample data only) + UpKeep notes; avoids asks already in Member Profile/Member Tools decks.
Standard deck page (index.template.html: Notes, Share, Built by Machan footer), mw-chat to UpKeep Agent, submit_agent upkeep.
Slugs: descriptive + random letters (no numbers), kept in queue/upkeep-page-deck-slugs.json."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, re, string, secrets
from team_kit import deck, publish, TERRA, LAGOON, JUNGLE, SAFFRON, INK
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
B = lambda s, c=SAFFRON: ("btn", s, "fill", c); BO = lambda s, c=LAGOON: ("btn", s, "outline", c)
TX = lambda s: ("p", s); C = lambda rows, c=None, h=30: ("cards", rows, c, "dot", "line", h)
NAV_M = ("nav", (("Home", "home"), ("Record", "star"), ("Visits", "cal"), ("Profile", "tag")))
NAV_T = ("nav", (("Today", "home"), ("Reports", "star"), ("Van", "tag"), ("Profile", "cal")))
def build(prefix, hd):
    pairs, O, add = deck(prefix, "UpKeep")
    def P(g, ask, a, b):
        add(g, g, O(a[0], a[1], a[2], a[3], [hd] + a[4]), O(b[0], b[1], b[2], b[3], [hd] + b[4]), ask)
    return pairs, P
# ---------------- Customer Profile Page Deck ----------------
cp, P = build("cpp_", ("hdr", "Smart Upkeep", "Member", SAFFRON, "logo", "S"))
P("Layout", "Top Of The Page: Big House Photo Or Greeting With Next Visit Card?",
  ("hero_photo", "Big House Photo", "Your house fills the top, address under it.", "warm", [("photo", 84, LAGOON, "house", ""), TX("1234 Sample Lane, Royal Oak"), C([("Next Visit", "Fall Visit · Sep 18", "›")])]),
  ("greet_card", "Greeting And Next Visit", "Good Morning, then the next visit card first.", "focused", [("h", "Good Morning", 18), C([("Next Visit", "Fall Visit · Sep 18", "›")], SAFFRON, 44), C([("Last Service", "Summer Visit · Jun 20", "")])]))
P("What Shows First", "First Card: Next Visit Or Home Health Summary?",
  ("first_next", "Next Visit", "Date and what the visit covers.", "practical", [C([("Next Visit", "Fall Visit · Sep 18", "")], SAFFRON, 44), ("checks", ["Fall furnace tune-up", "Gutter cleaning", "Smoke and CO checks"], JUNGLE, 0)]),
  ("first_health", "Home Health Summary", "All good, plus anything to watch.", "calm", [("stats", [("8", "Items OK"), ("1", "To Watch")], "box"), ("banner", "Under hall bath sink: recheck next visit", SAFFRON, "clock")]))
P("Home Record", "Your Appliances: Picture Tiles Or A List With Last Service?",
  ("app_tiles", "Picture Tiles", "One tile per appliance.", "visual", [("tiles", [("Gas Furnace", "home"), ("Central AC", "clock"), ("Water Heater", "star"), ("Softener", "check")], 2, 54)]),
  ("app_list", "List With Last Service", "Name left, last service right.", "calm", [C([("Gas Furnace", "", "Sep 2026"), ("Central AC", "", "Apr 2026"), ("Tank Water Heater, 50 gal", "", "Apr 2026"), ("Water Softener", "", "Sep 2026"), ("Dryer Vent", "", "Jun 2026")], None, 26)]))
P("Home Record", "Appliance Age: Year Installed Or A Life-Left Bar?",
  ("age_year", "Year Installed", "\"Installed 2014\" as plain text.", "calm", [C([("Tank Water Heater, 50 gal", "Installed 2014", "")], None, 40), C([("Gas Furnace", "Installed 2017", "")], None, 40)]),
  ("age_bar", "Life-Left Bar", "A bar shows typical life used.", "visual", [("bar", .8, TERRA, "Water heater", "about 80% of typical life"), ("bar", .5, JUNGLE, "Gas furnace", "about half")]))
P("Visit History", "Past Visits: Timeline Or Season Cards?",
  ("hist_tl", "Timeline", "One line, newest on top.", "calm", [("timeline", [("Summer Visit", "Jun 20, 2026"), ("Spring Visit", "Apr 15, 2026"), ("Winter Visit", "Dec 2025"), ("Fall Visit", "Sep 2025")])]),
  ("hist_cards", "Season Cards", "A card per season with a report link.", "practical", [C([("Summer Visit", "Jun 20 · report ready", "›"), ("Spring Visit", "Apr 15 · report ready", "›"), ("Winter Visit", "Dec 2025", "›")], None, 34)]))
P("Visit History", "Opening A Visit Report: Photos And Summary First Or Checklist First?",
  ("rep_photo", "Photos And Summary", "Photos on top, one-line summary.", "visual", [("photos", 3, 54), TX("No issues found. Dryer vent airflow improved after cleaning.")]),
  ("rep_check", "Checklist First", "Every task ticked, photos below.", "practical", [("checks", ["Dryer vent cleaning", "Smoke and CO checks", "Fridge filter changed", "Water heater flush"], JUNGLE, 4), ("photos", 3, 34)]))
P("Service Schedule", "Upcoming Visits: Calendar Or Season List?",
  ("sch_cal", "Calendar", "Visit days marked on a month view.", "visual", [("lbl", "SEPTEMBER 2026"), ("cal", (18,), SAFFRON)]),
  ("sch_list", "Season List", "Fall, Winter, Spring, Summer with dates.", "calm", [C([("Fall Visit", "Sep 18, 2026", "Scheduled"), ("Winter Visit", "Dec 8 to Dec 12", "Planned"), ("Spring Visit", "April 2027", "Planned")], None, 32)]))
P("Service Schedule", "Changing A Visit Day: Reschedule Button Or Message Us?",
  ("rs_btn", "Reschedule Button", "Pick a new day yourself.", "quick", [C([("Fall Visit", "Sep 18, 2026", "")], SAFFRON, 40), B("Reschedule")]),
  ("rs_msg", "Message Us", "The team confirms a new day.", "calm", [C([("Fall Visit", "Sep 18, 2026", "")], SAFFRON, 40), BO("Message Us To Change")]))
P("Photos", "Visit Photos: Swipe Carousel Or Photo Grid?",
  ("ph_car", "Swipe Carousel", "One big photo at a time, swipe for more.", "visual", [("photo", 96, LAGOON, "room", "Dryer vent after cleaning"), ("dots", 5, 1)]),
  ("ph_grid", "Photo Grid", "All photos small, tap to open.", "practical", [("photos", 3, 50), ("photos", 3, 50, ["leaf", "house", "room"])]))
P("Photos", "Problem Photos: Before And After Pair Or Latest Photo Only?",
  ("ba_pair", "Before And After", "Two photos side by side.", "clear", [("photos", 2, 80, ["room", "room"], [TERRA, JUNGLE]), ("tags", ["Before", "After"])]),
  ("ba_latest", "Latest Only", "Just the newest photo and a note.", "calm", [("photo", 90, JUNGLE, "room", "Under hall bath sink, Sep 2026"), TX("Slightly damp, recheck next visit.")]))
P("Booking", "Request A Visit: Big Button On Home Or In The Visits Tab?",
  ("bk_home", "Big Button On Home", "Always on the home screen.", "quick", [("h", "Good Afternoon", 16), B("Request a Visit"), C([("Next Visit", "Sep 18", "")]), NAV_M]),
  ("bk_tab", "In The Visits Tab", "Home stays calm; booking lives with visits.", "calm", [("tabs", ["Upcoming", "Past"], "pill"), C([("Fall Visit", "Sep 18", "")]), BO("Request a Visit"), NAV_M]))
P("Messaging", "Messaging: Chat Thread In The App Or Text And Email Buttons?",
  ("msg_chat", "Chat In The App", "A thread with the Smart Upkeep team.", "friendly", [("bubble", "Can you check the attic fan too?", True), ("bubble", "Yes, we'll add it to your Fall Visit.", False), ("input", "Message", LAGOON, "mic")]),
  ("msg_btns", "Text And Email", "Buttons open your own text or email app.", "simple", [TX("Questions about your plan or a visit?"), B("Text Us"), BO("Email Us")]))
P("Tech Notes", "Tech Notes: Under Each Appliance Or One Notes Block Per Visit?",
  ("tn_item", "Under Each Appliance", "The note sits with the thing it is about.", "practical", [C([("Water Softener", "Salt topped off. Next top-off in winter.", "")], None, 40), C([("Dryer Vent", "Airflow improved after cleaning.", "")], None, 40)]),
  ("tn_block", "One Notes Block", "All notes for the visit in one place.", "calm", [("lbl", "TECH NOTES · SUMMER VISIT"), TX("Salt topped off. Dryer vent airflow improved. Hall bath sink slightly damp, recheck next visit.")]))
P("What To Watch", "Recheck Items: Banner At The Top Or Inside The Visit Report?",
  ("rk_banner", "Banner At The Top", "You see it as soon as you open the app.", "clear", [("banner", "1 item to recheck next visit", SAFFRON, "clock"), C([("Next Visit", "Sep 18", "")])]),
  ("rk_report", "Inside The Report", "Listed with the visit it came from.", "calm", [C([("Summer Visit report", "Jun 20", "›")]), C([("Recheck", "Under hall bath sink", "")], SAFFRON, 36)]))
P("Proof Pack", "Maintenance Proof Pack: Button On Home Or In The Home Record?",
  ("pp_home", "Button On Home", "One tap from the first screen.", "quick", [C([("Next Visit", "Sep 18", "")]), BO("Download Proof Pack"), NAV_M]),
  ("pp_record", "In The Home Record", "With warranty claims and appliances.", "calm", [("tabs", ["Appliances", "Proof Pack"], "line"), C([("Maintenance Proof Pack", "Visit record for warranty claims", "›")], LAGOON, 44)]))
P("Tips", "Did You Know: Swipe Cards Or One Tip At A Time?",
  ("tip_car", "Swipe Cards", "A row of tip cards to swipe through.", "playful", [("lbl", "DID YOU KNOW"), ("tiles", [("Water heater", "home"), ("Dryer vent", "clock")], 2, 60), ("dots", 4, 1)]),
  ("tip_one", "One Tip", "A single tip that changes each visit.", "calm", [("lbl", "DID YOU KNOW"), TX("A yearly flush cuts sediment and can help extend a tank's life.")]))
P("Navigation", "Page Structure: Bottom Tabs Or One Long Scrolling Page?",
  ("nav_tabs", "Bottom Tabs", "Home, Record, Visits, Profile.", "focused", [C([("Next Visit", "Sep 18", "")]), C([("Last Service", "Jun 20", "")]), NAV_M]),
  ("nav_scroll", "One Long Page", "Everything stacked, scroll down.", "simple", [("lbl", "NEXT VISIT"), C([("Fall Visit", "Sep 18", "")]), ("lbl", "HOME RECORD"), C([("Appliances", "5 logged", "›")]), ("lbl", "VISITS"), C([("Summer Visit", "Jun 20", "›")])]))
P("Moisture Scan", "Mold And Moisture Scan Results: Room Map Or Room List?",
  ("ms_map", "Room Map", "Floor plan with a dot on each spot checked.", "visual", [("map", 120), TX("1 damp spot · everything else dry")]),
  ("ms_list", "Room List", "Each room with a reading.", "practical", [C([("Kitchen", "", "Dry"), ("Hall bath, under sink", "", "Damp"), ("Basement", "", "Dry"), ("Laundry", "", "Dry")], None, 26)]))
P("Adding Appliances", "Add An Appliance: Photo Of The Label Or Type The Model?",
  ("aa_photo", "Photo Of The Label", "Snap the sticker; we fill it in.", "quick", [("photo", 90, LAGOON, "room", "Point at the model sticker"), B("Add a Photo")]),
  ("aa_type", "Type The Model", "Brand, model, year.", "precise", [("input", "Brand", LAGOON, "mic"), ("input", "Model number", LAGOON, "mic"), B("Save")]))
P("Who's Coming", "Before A Visit: Show The Technician's Photo And Name Or Just The Arrival Window?",
  ("wc_tech", "Technician Card", "Photo, first name, certifications.", "friendly", [("photo", 70, LAGOON, "person", "Sample technician"), ("tags", ["EPA 608", "OSHA 10"]), C([("Arrival window", "We confirm ahead of time", "")])]),
  ("wc_window", "Arrival Window Only", "Day and window, no name.", "calm", [C([("Fall Visit", "Sep 18 · window confirmed ahead", "")], SAFFRON, 44)]))
# ---------------- Technician Page Deck ----------------
tp, P = build("tpp_", ("hdr", "Smart Upkeep", "Technician", LAGOON, "logo", "S"))
P("Today", "Today's Visits: Route List Or Map First?",
  ("td_list", "Route List", "Visits in order with times.", "practical", [("h", "Good Morning", 16), C([("Sample block A", "8:00 · Fall Visit", "1"), ("Sample block B", "11:00 · Fall Visit", "2"), ("Sample block C", "2:00 · Scan", "3")], None, 32), NAV_T]),
  ("td_map", "Map First", "Map with numbered stops, list below.", "visual", [("map", 110), C([("Next: Sample block A", "8:00", "›")]), NAV_T]))
P("Job Card", "Job Card Top: Address And Time Or Member Notes And Watch Items?",
  ("jc_addr", "Address And Time", "Where and when first.", "practical", [C([("1234 Sample Lane", "8:00 · Fall Visit", "")], LAGOON, 44), B("Navigate", LAGOON)]),
  ("jc_notes", "Notes And Watch Items", "What to look at first.", "focused", [("banner", "Recheck: under hall bath sink", SAFFRON, "clock"), C([("Member note", "Dog in the yard, side gate", "")], None, 40)]))
P("Navigation", "Directions: Navigate Button On Each Job Or One Start Route Button?",
  ("nv_each", "Button On Each Job", "Open maps one stop at a time.", "simple", [C([("Sample block A", "8:00", "")], None, 30), BO("Navigate", LAGOON), C([("Sample block B", "11:00", "")], None, 30), BO("Navigate", LAGOON)]),
  ("nv_route", "Start Route", "One tap loads all stops in order.", "quick", [C([("3 visits today", "About 4 hours on site", "")], None, 40), B("Start Route", LAGOON)]))
P("Checklist", "Visit Checklist: One Long List Or Grouped By Area?",
  ("ck_long", "One Long List", "Every task top to bottom.", "simple", [("checks", ["Furnace filter changed", "Fall furnace tune-up", "Gutter cleaning", "Smoke and CO checks", "Dryer vent cleaning"], JUNGLE, 2)]),
  ("ck_group", "Grouped By Area", "HVAC, Plumbing, Exterior, Safety.", "focused", [C([("HVAC Checks", "2 of 3 done", "›"), ("Plumbing", "0 of 2", "›"), ("Gutters", "0 of 1", "›"), ("Safety", "1 of 2", "›")], None, 30)]))
P("Checklist", "Ticking A Task: Checkbox Only Or Checkbox Plus Required Photo?",
  ("tk_box", "Checkbox Only", "Fast; photos are optional.", "quick", [("checks", ["Water heater flush", "Softener salt top-off"], JUNGLE, 1)]),
  ("tk_photo", "Checkbox Plus Photo", "Task can't close without a photo.", "thorough", [("checks", ["Water heater flush"], JUNGLE, 0), ("photo", 60, JUNGLE, "room", ""), BO("Add photo", JUNGLE)]))
P("Photos", "Photos In The Report: Before And After Required Or One Photo Per Task?",
  ("pr_ba", "Before And After", "Two shots for every cleaning task.", "thorough", [("photos", 2, 76, ["room", "room"], [TERRA, JUNGLE]), ("tags", ["Before", "After"])]),
  ("pr_one", "One Photo Per Task", "Just the finished result.", "quick", [("photos", 3, 60), TX("Finished photos only")]))
P("Readings", "Moisture Readings: Type A Number Or Tap Dry, Watch, Wet?",
  ("rd_num", "Type A Number", "Meter reading in percent.", "precise", [C([("Under kitchen sink", "Reading", "")], None, 30), ("input", "Reading %", LAGOON, "mic")]),
  ("rd_tap", "Tap Dry, Watch, Wet", "Three big buttons.", "quick", [C([("Under kitchen sink", "", "")], None, 30), ("tags", ["Dry", "Watch", "Wet"], True)]))
P("Rechecks", "Items To Recheck From Last Visit: Banner On Arrival Or Inside The Checklist?",
  ("rc_banner", "Banner On Arrival", "Shows when you open the job.", "clear", [("banner", "Recheck: under hall bath sink", SAFFRON, "clock"), ("checks", ["Fall furnace tune-up", "Gutter cleaning"], JUNGLE, 0)]),
  ("rc_inline", "Inside The Checklist", "A Recheck task in the list.", "calm", [("checks", ["Recheck: under hall bath sink", "Fall furnace tune-up", "Gutter cleaning"], JUNGLE, 0)]))
P("Notes For The Member", "Notes For The Member: Free Text Or Quick Phrase Chips?",
  ("nm_text", "Free Text", "Write what you did and what to watch.", "personal", [("lbl", "NOTES FOR THE MEMBER"), ("input", "What you did and anything to watch", LAGOON, "mic")]),
  ("nm_chips", "Quick Phrases", "Tap chips, add a line if needed.", "quick", [("tags", ["No issues found", "Recheck next visit", "Airflow improved"]), ("input", "Add a line", LAGOON, "mic")]))
P("Submit", "Sending The Visit Report: Submit Right Away Or Preview What The Member Sees?",
  ("sb_now", "Submit Right Away", "One button at the end.", "quick", [("checks", ["All tasks done", "Photos added"], JUNGLE, 2), B("Submit Report", LAGOON)]),
  ("sb_prev", "Preview First", "See the member's report, then send.", "careful", [("lbl", "MEMBER SEES"), ("photos", 3, 40), TX("No issues found."), B("Looks Good, Send", LAGOON)]))
P("Past Reports", "Past Reports: History For This Home Or All Reports With Search?",
  ("pr_home", "This Home's History", "Opens from the job card.", "focused", [("timeline", [("Summer Visit", "Jun 20, 2026"), ("Spring Visit", "Apr 15, 2026"), ("Winter Visit", "Dec 2025")])]),
  ("pr_all", "All Reports, Search", "Find any report by address.", "practical", [("input", "Search address", LAGOON, "mic"), C([("Sample block A", "Jun 20", "Submitted"), ("Sample block B", "Jun 18", "Submitted")], None, 30)]))
P("Van Inventory", "Van Inventory: Full List With Counts Or Only Items Running Low?",
  ("vi_full", "Full List", "Everything on the van.", "complete", [C([("Furnace filters", "", "12"), ("DAP Kwik Seal", "", "4"), ("Shop towels", "", "2 rolls"), ("AA / AAA packs", "", "6")], None, 26)]),
  ("vi_low", "Running Low Only", "Just what needs a restock.", "calm", [("banner", "2 items running low", TERRA, "clock"), C([("Shop towels", "", "2 left"), ("Contractor bags", "", "3 left")], TERRA, 28)]))
P("Van Inventory", "Logging Supplies Used: Minus And Plus Buttons Or Scan The Barcode?",
  ("lu_tap", "Minus And Plus", "Tap to adjust counts.", "simple", [C([("Furnace filter 16x25", "", "−  1  +"), ("Silicone caulk", "", "−  0  +")], None, 32)]),
  ("lu_scan", "Scan The Barcode", "Camera adds the item.", "quick", [("photo", 90, LAGOON, "room", "Point at the barcode"), B("Log Use", LAGOON)]))
P("Restock", "Restocking: Automatic Request When Low Or A Weekly Restock Checklist?",
  ("rs_auto", "Automatic Request", "Low items go on the order by themselves.", "quick", [("banner", "Restock request sent: shop towels", JUNGLE, "check")]),
  ("rs_week", "Weekly Checklist", "Check the van every Monday.", "thorough", [("lbl", "CONSUMABLES RESTOCK · MONDAY"), ("checks", ["Shop towels", "Contractor bags", "N95 masks"], JUNGLE, 1)]))
P("Certifications", "Certifications: Badges Or A List With Expiry Dates?",
  ("ct_badge", "Badges", "Small badges on the profile.", "visual", [("photo", 70, LAGOON, "person", "Sample technician"), ("tags", ["EPA 608", "EPA RRP", "OSHA 10", "CPR"])]),
  ("ct_list", "List With Expiry", "Each one with its renewal date.", "practical", [C([("EPA Section 608", "", "No expiry"), ("EPA Lead-Safe RRP", "", "Renew 2029"), ("CPR and First Aid", "", "Renew 2027")], None, 28)]))
P("Schedule Changes", "Schedule Changes: Alert Banner Or Highlight In Today's List?",
  ("sc_alert", "Alert Banner", "Big notice at the top.", "clear", [("banner", "Sample block B moved to 1:00", TERRA, "clock"), C([("Sample block A", "8:00", "")])]),
  ("sc_hl", "Highlight In The List", "Changed visit gets a tag.", "calm", [C([("Sample block A", "8:00", ""), ("Sample block B", "1:00", "Moved")], None, 32)]))
P("Member Contact", "Reaching The Member: Message In The App Or Call And Text Buttons?",
  ("mc_app", "Message In The App", "Thread saved with the visit.", "tidy", [("bubble", "On my way, about 15 minutes.", True), ("bubble", "Thanks, side gate is open.", False)]),
  ("mc_call", "Call And Text", "Opens the phone.", "direct", [C([("Member", "Sample record", "")], None, 36), B("Call", LAGOON), BO("Text", LAGOON)]))
P("Job Timer", "On-Site Time: Show A Visit Timer Or No Timer?",
  ("jt_timer", "Visit Timer", "Starts when you arrive.", "focused", [("ring", .6, LAGOON, "1:12", "on site"), ("checks", ["Fall furnace tune-up"], JUNGLE, 1)]),
  ("jt_none", "No Timer", "Just the checklist.", "calm", [("checks", ["Fall furnace tune-up", "Gutter cleaning", "Smoke and CO checks"], JUNGLE, 1)]))
P("Home Record", "Home Record For The Tech: Appliance Tiles Or The Full Record?",
  ("hr_tiles", "Appliance Tiles", "Just what you service.", "focused", [("tiles", [("Gas Furnace", "home"), ("Water Heater", "clock"), ("Softener", "star"), ("Dryer Vent", "check")], 2, 54)]),
  ("hr_full", "Full Record", "Everything the member sees.", "complete", [("tabs", ["Appliances", "Visits", "Scans"], "line"), C([("Gas Furnace", "Tuned Sep 2026", ""), ("Hall bath sink", "Damp, recheck", "")], None, 30)]))
P("Safety", "Safety Before Each Visit: PPE Checklist Or A One-Line Reminder?",
  ("sf_check", "PPE Checklist", "Tick gloves, mask, ladder check.", "thorough", [("lbl", "SAFETY AND PPE"), ("checks", ["Cut-resistant gloves", "N95 mask", "Ladder inspected"], JUNGLE, 0), B("Start Visit", LAGOON)]),
  ("sf_line", "One-Line Reminder", "Short reminder above Start.", "quick", [TX("Gloves, mask, ladder check."), B("Start Visit", LAGOON)]))
assert len(cp) == 20 and len(tp) == 20, (len(cp), len(tp))
SL = "queue/upkeep-page-deck-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
for n, (did, NAME, base, pairs, about) in enumerate((
    ("upkeep-customer-profile-page-deck", "Customer Profile Page Deck", "upkeep-customer-profile-page-", cp, "Smart Upkeep member profile page: layout, first info, Home Record, history, schedule, photos, booking, messaging"),
    ("upkeep-technician-page-deck", "Technician Page Deck", "upkeep-technician-page-", tp, "Smart Upkeep technician page: today's visits, job view, checklists, photos, readings, reports, van inventory"))):
    order = [p["ask"] for p in pairs]
    publish(did, NAME, "UpKeep", pairs, {"brands": [about], "submit_agent": "upkeep", "topic": did, "deck_size": 20, "board": "upkeep", "audience": "Max", "requested": True}, seed=8100 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"])); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 20
    if did not in slugs: slugs[did] = base + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]
    HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
