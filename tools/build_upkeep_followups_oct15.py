#!/usr/bin/env python3
"""Oct 15 2026: source pairs for three UpKeep follow-up shelf decks (Funnel, Plans & Pricing, Video), built from what was
still open after Max's Oct 14 answers. Writes banks/src-upkeep-*-followup.json; publish with tools/ready_shelf.py build --source."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from team_kit import deck, TERRA, LAGOON, JUNGLE, SAFFRON, INK
def mk(prefix, sub):
    pairs, O, add = deck(prefix, "UpKeep"); HD = ("hdr", "Smart Upkeep", sub, SAFFRON, "logo", "S")
    def P(g, ask, a, b): add(g, g, O(a[0], a[1], a[2], a[3], [HD] + a[4]), O(b[0], b[1], b[2], b[3], [HD] + b[4]), ask)
    return pairs, P
def play(c=SAFFRON): return ("raw", f'<rect x="14" y="0" width="212" height="118" rx="8" fill="{c}22"/><circle cx="120" cy="59" r="20" fill="{c}"/><path d="M114 49 L130 59 L114 69 Z" fill="#fff"/>', 126)
B = lambda s, c=SAFFRON: ("btn", s, "fill", c)
W = lambda s, c=INK, sub="": ("word", s, 22, c, sub)
TX = lambda s: ("p", s)

# ---------------- Funnel ----------------
fp, P = mk("fn2_", "Get Started")
P("Info Gather", "Home Age From The Address: Show It On The Price Page Or Keep It Behind The Scenes?",
  ("ha_show", "Show It", "\"Built about 1985\" line on the price page.", "focused", [("cards", [("Your Home", "Built about 1985", "From records")], None, "dot", "line", 34), B("See My Price")]),
  ("ha_hide", "Behind The Scenes", "Used for pricing, never shown.", "calm", [W("Your Price Is Ready"), B("See My Price")]))
P("Info Gather", "Water Softener Tile: In The Extras Grid Or First In Extras?",
  ("ws_grid", "In The Grid", "Same size as the other extras.", "calm", [("tiles", [("Sump Pump", "home"), ("Fireplace", "star"), ("Water Softener", "check"), ("Irrigation", "star")], 2, 48)]),
  ("ws_first", "First In Extras", "Its own wide tile on top.", "focused", [("banner", "Water Softener?", SAFFRON, "check"), ("tiles", [("Sump Pump", "home"), ("Fireplace", "star")], 2, 48)]))
P("Info Gather", "Question Count: Show \"7 Questions\" Or Hide The Count?",
  ("qc_show", "Show The Count", "\"7 quick questions\" on Get Started.", "quick", [W("7 Quick Questions"), B("Get Started")]),
  ("qc_hide", "Hide It", "Just the progress bar.", "calm", [("bar", .3, SAFFRON, "Your Home", ""), B("Next")]))
P("Home Page", "Home Page Plans Slider: Dots Or Arrows?",
  ("sl_dots", "Dots", "Small dots under the plans.", "calm", [("cards", [("Plus", "Most Popular", "$164/mo")], None, "dot", "line", 40), ("dots", 3, 2, INK)]),
  ("sl_arrows", "Arrows", "Left and right arrow buttons.", "focused", [("cards", [("Plus", "Most Popular", "$164/mo")], None, "dot", "line", 40), ("btn2", "‹ Back", "Next ›", INK)]))
P("Home Page", "Message Lead: Under The Headline Or As The Headline?",
  ("ml_under", "Under The Headline", "\"Your Home, Taken Care Of.\" stays, lead line below.", "calm", [W("Your Home, Taken Care Of."), TX("Catch small problems before they're big ones.")]),
  ("ml_head", "As The Headline", "\"Catch Small Problems Before They're Big Ones.\"", "focused", [W("Catch Small Problems Early"), TX("Membership from $99/month")]))
P("Home Page", "Trust Row: Badges Only Or Badges Plus One Short Quote?",
  ("tr_badges", "Badges Only", "Licensed, insured, Metro Detroit.", "calm", [("tags", ["Licensed", "Insured", "Metro Detroit"], True)]),
  ("tr_quote", "Badges Plus A Quote", "One neighbour quote under the badges (after launch).", "focused", [("tags", ["Licensed", "Insured"], True), ("bubble", "\"Easiest thing I signed up for.\" Dana, Royal Oak", False, LAGOON)]))
P("Video", "Tap For Sound: Centre Of The Video Or Bottom Corner?",
  ("ts_mid", "Centre", "Big saffron pill in the middle, as live.", "focused", [play(), B("Tap for Sound")]),
  ("ts_corner", "Bottom Corner", "Smaller speaker pill, corner of the player.", "calm", [play(LAGOON), ("btn", "Sound", "link", INK)]))
P("Video", "After The Video: Scroll To Plans Or Show A Get Started Card?",
  ("av_plans", "Scroll To Plans", "Video closes and lands on the plans, as live.", "calm", [("cards", [("Essentials", "", "$99/mo"), ("Plus", "", "$164/mo")], None, "dot", "line", 26)]),
  ("av_card", "Get Started Card", "A card: Ready? Get Started.", "quick", [W("Ready?"), B("Get Started")]))
P("Price Offer", "Price Breakdown: Full List Or Top 5 With See All?",
  ("pb_full", "Full List", "Every line shown, as live now.", "focused", [("checks", ["4 seasonal visits", "Furnace tune-up", "AC tune-up", "Water heater flush", "Gutters", "Dryer vent"], JUNGLE, 6)]),
  ("pb_top5", "Top 5 And See All", "Shorter, tap to see the rest.", "calm", [("checks", ["4 seasonal visits", "Furnace tune-up", "AC tune-up"], JUNGLE, 3), ("btn", "See All", "link", LAGOON)]))
P("Price Offer", "Welcome Offers: Both On The Price Page Or Pick One At Sign Up?",
  ("wo_both", "Both On The Price Page", "6 free months and 10% off annually shown together.", "focused", [("cards", [("6 Free Months", "Pay for 2 years", ""), ("10% Off", "Pay the year up front", "")], None, "dot", "line", 30)]),
  ("wo_signup", "Pick One At Sign Up", "Price page stays clean; choose at payment.", "calm", [W("Your Price"), ("btn2", "6 Free Months", "10% Off", SAFFRON)]))
P("Price Offer", "10% Off Annually: Every Plan Or Complete Only?",
  ("ten_all", "Every Plan", "Essentials, Plus and Complete.", "quick", [("stats", [("10%", "Essentials"), ("10%", "Plus"), ("10%", "Complete")], "box")]),
  ("ten_comp", "Complete Only", "As the draft today.", "calm", [("stats", [("—", "Essentials"), ("—", "Plus"), ("10%", "Complete")], "box")]))
P("Make The Sale", "Monthly Card: Charge On Sign-Up Day Or The 1st Of The Month?",
  ("mc_day", "Sign-Up Day", "Same date each month as you joined.", "calm", [("cal", (14,), SAFFRON)]),
  ("mc_first", "The 1st", "Everyone billed on the 1st.", "focused", [("cal", (1,), SAFFRON)]))
P("Make The Sale", "Payment Options: Monthly Card First Or Prepaid First?",
  ("po_mo", "Monthly Card First", "Monthly is the default pick.", "quick", [("cards", [("Monthly Card", "Same day each month", "$164/mo"), ("Prepay 2 Years", "6 free months", "")], None, "dot", "line", 30)]),
  ("po_pre", "Prepaid First", "Prepay offers on top.", "focused", [("cards", [("Prepay 2 Years", "6 free months", ""), ("Monthly Card", "Same day each month", "$164/mo")], None, "dot", "line", 30)]))
P("Make The Sale", "Signature: Draw Only Or Draw With A Typed Name Backup?",
  ("sg_draw", "Draw Only", "Finger signature, as live.", "calm", [("input", "Sign here", INK, "mic"), B("Agree And Join")]),
  ("sg_both", "Draw Or Type", "Small \"Type instead\" link.", "focused", [("input", "Sign here", INK, "mic"), ("btn", "Type instead", "link", LAGOON)]))
P("Make The Sale", "Your Home Picture: Street View Or Satellite?",
  ("hp_street", "Street View", "Front of the house from the street.", "calm", [("photo", 110, LAGOON, "house", "Your Home")]),
  ("hp_sat", "Satellite", "Roof and yard from above.", "visual", [("map", 110)]))
P("Make The Sale", "First Visit Booking: Pick A Day Or Day Plus Time Window?",
  ("fv_day", "Pick A Day", "One tap, we text the time, as live.", "quick", [("cal", (6, 13, 20), SAFFRON), B("Book This Day")]),
  ("fv_win", "Day Plus Window", "Morning, midday or afternoon too.", "focused", [("cal", (6,), SAFFRON), ("tags", ["Morning", "Midday", "Afternoon"], False)]))
P("Make The Sale", "Welcome Screen Order: Book First Visit Before Or After Your Home Picture?",
  ("wo_book", "Booking First", "Book Your First Visit at the top.", "quick", [B("Book Your First Visit"), ("photo", 70, LAGOON, "house", "Your Home")]),
  ("wo_pic", "Picture First", "Your Home picture, then booking.", "calm", [("photo", 70, LAGOON, "house", "Your Home"), B("Book Your First Visit")]))
P("Marketing", "First Lead Channel: Neighbourhood Mailer First Or Social Ads First?",
  ("lc_mail", "Mailer First", "Postcard with a QR code.", "calm", [("photo", 90, SAFFRON, "house", "Postcard + QR"), TX("One ZIP at a time")]),
  ("lc_social", "Social Ads First", "Short vertical clip with Get Started.", "quick", [play(), B("Get Started")]))
P("Marketing", "Mailer Rollout: One ZIP At A Time Or Three ZIPs At Once?",
  ("mz_one", "One ZIP", "Learn, then expand.", "calm", [("tags", ["48067"], True)]),
  ("mz_three", "Three ZIPs", "Faster test across areas.", "quick", [("tags", ["48067", "48073", "48207"], True)]))
P("Marketing", "Mailer Headline: Price Hook Or Protect The Home?",
  ("mh_price", "Price Hook", "\"Your whole home, cared for. From $99/month.\"", "quick", [W("From $99/Month", SAFFRON)]),
  ("mh_prot", "Protect The Home", "\"Catch small problems before they're big ones.\"", "calm", [W("Catch It Early", INK)]))
assert len(fp) == 20, len(fp)

# ---------------- Plans & Pricing ----------------
pp, P = mk("pp2_", "Plans")
card = lambda pic: [("photo", 60, SAFFRON, "house", "") if pic else ("gap", 2), ("cards", [("Plus", "4 visits a year", "$164/mo")], None, "dot", "line", 34)]
P("Plan Cards", "Plan Card Picture: On Top Or Beside The Name?",
  ("pc_top", "On Top", "Picture across the top of each card.", "visual", card(True)),
  ("pc_side", "Beside", "Small picture left of the name.", "calm", [("cards", [("Plus", "4 visits a year", "$164/mo")], None, "dot", "line", 50), TX("Picture sits left of the name")]))
P("Plan Cards", "Plan Card Spacing: Roomy Or Compact?",
  ("sp_roomy", "Roomy", "More space, fewer lines on screen.", "calm", [("cards", [("Plus", "4 visits a year", "$164/mo")], None, "dot", "line", 52)]),
  ("sp_comp", "Compact", "Tighter, more fits on a phone.", "focused", [("cards", [("Essentials", "", "$99/mo"), ("Plus", "", "$164/mo"), ("Complete", "", "$312/mo")], None, "dot", "line", 24)]))
P("Plan Cards", "Plan Card Details: Fold-Out Sections Or Icon Action Tiles?",
  ("pd_fold", "Fold-Out Sections", "Tap \"What's Included\" to open.", "calm", [("cards", [("What's Included", "", "▾"), ("Visits", "", "▾")], None, "dot", "line", 28)]),
  ("pd_tiles", "Icon Action Tiles", "Four icons: Visits, Water, Air, Safety.", "visual", [("tiles", [("Visits", "cal"), ("Water", "home"), ("Air", "star"), ("Safety", "check")], 2, 44)]))
P("Plan Cards", "Plan Card Button: Pill Button Or Text Link?",
  ("pb_pill", "Pill Button", "Round saffron Choose Plus.", "quick", [B("Choose Plus")]),
  ("pb_link", "Text Link", "Quiet \"Choose Plus\" link.", "calm", [("btn", "Choose Plus", "link", LAGOON)]))
P("Plan Cards", "Plan Card Accent: Saffron Or Lagoon?",
  ("pa_saf", "Saffron", "Main brand colour.", "calm", [("cards", [("Plus", "", "$164/mo")], SAFFRON, "dot", "line", 34), B("Choose Plus", SAFFRON)]),
  ("pa_lag", "Lagoon", "Cool accent, saffron buttons stay.", "focused", [("cards", [("Plus", "", "$164/mo")], LAGOON, "dot", "line", 34), B("Choose Plus", SAFFRON)]))
P("Plan Cards", "Plus Badge: \"Most Popular\" Or \"Best Value\"?",
  ("bd_pop", "Most Popular", "As live.", "calm", [("tags", ["Most Popular"], True), ("cards", [("Plus", "", "$164/mo")], None, "dot", "line", 30)]),
  ("bd_val", "Best Value", "Points to price per visit.", "focused", [("tags", ["Best Value"], True), ("cards", [("Plus", "", "$164/mo")], None, "dot", "line", 30)]))
P("Prices", "Price Shown: Monthly First Or Yearly First?",
  ("pr_mo", "Monthly First", "$164/month big, yearly small.", "quick", [W("$164/Month", SAFFRON, "$1,968 a year")]),
  ("pr_yr", "Yearly First", "$1,968/year big, monthly small.", "focused", [W("$1,968/Year", SAFFRON, "$164 a month")]))
P("Prices", "Complete Price: \"$312\" Or \"From $312\"?",
  ("cp_exact", "$312", "One number.", "quick", [W("$312/Mo")]),
  ("cp_from", "From $312", "Room for bigger homes.", "calm", [W("From $312/Mo")]))
P("Prices", "$99 Minimum Note: Show It Or Hide It?",
  ("mn_show", "Show It", "\"Priced at our $99/month minimum\".", "focused", [W("$99/Mo"), TX("Priced at our $99/month minimum")]),
  ("mn_hide", "Hide It", "Just the price.", "calm", [W("$99/Mo")]))
P("Prices", "Price Page On Phone: Swipe Cards Or Stacked?",
  ("pp_swipe", "Swipe Cards", "One plan at a time, swipe for more.", "visual", [("cards", [("Plus", "", "$164/mo")], None, "dot", "line", 50), ("dots", 3, 2, INK)]),
  ("pp_stack", "Stacked", "All three, scroll down.", "calm", [("cards", [("Essentials", "", "$99"), ("Plus", "", "$164"), ("Complete", "", "$312")], None, "dot", "line", 26)]))
P("Prices", "Compare Plans: One Table Or Ticks On Each Card?",
  ("cm_table", "One Table", "Rows of services, three columns.", "focused", [("table", [("Gutters", "Plus, Complete"), ("Roof check", "Complete"), ("Softener salt", "Plus, Complete")])]),
  ("cm_ticks", "Ticks Per Card", "Each card lists its own.", "calm", [("checks", ["Gutters", "Softener salt", "Fridge filter"], JUNGLE, 3)]))
P("Prices", "Breakdown Lines: Dollar Amounts Or Included Ticks?",
  ("bl_amt", "Dollar Amounts", "Each line shows its cost.", "focused", [("table", [("Furnace tune-up", "$140"), ("Gutters x2", "$260")])]),
  ("bl_tick", "Included Ticks", "Lines with a tick, one total.", "calm", [("checks", ["Furnace tune-up", "Gutters x2"], JUNGLE, 2), W("$164/Mo")]))
P("Add-Ons", "Add-Ons: Under The Plans Or A Separate Step?",
  ("ao_under", "Under The Plans", "Same page, scroll down.", "calm", [("cards", [("Plus", "", "$164/mo")], None, "dot", "line", 26), ("tags", ["Windows", "Radon", "Snow"], False)]),
  ("ao_step", "Separate Step", "\"Add Anything?\" after picking a plan.", "focused", [W("Add Anything?"), ("tags", ["Windows", "Radon", "Snow"], False)]))
P("Add-Ons", "Lawn Add-On Price: Per Cut Or Per Month?",
  ("lw_cut", "Per Cut", "\"$45 a cut\".", "quick", [W("$45/Cut", JUNGLE)]),
  ("lw_mo", "Per Month", "\"$160/month, May to October\".", "calm", [W("$160/Mo", JUNGLE, "May to October")]))
P("Policies", "Pause Wording: \"Pause Anytime\" Or \"Pause Up To 3 Months\"?",
  ("pz_any", "Pause Anytime", "Simple promise.", "calm", [("banner", "Pause Anytime", JUNGLE, "clock")]),
  ("pz_3", "Up To 3 Months", "Clear limit.", "focused", [("banner", "Pause Up To 3 Months", JUNGLE, "clock")]))
P("Policies", "Referral Reward: 1 Month Free Or $50 Off?",
  ("rf_month", "1 Month Free", "As the draft today.", "calm", [W("1 Month Free", SAFFRON)]),
  ("rf_50", "$50 Off", "Cash-style credit.", "quick", [W("$50 Off", SAFFRON)]))
P("Waitlist", "Waitlist Card: On The Home Page Or Only After Get Started?",
  ("wl_home", "On The Home Page", "\"Join the waitlist\" card near plans.", "focused", [W("Join The Waitlist"), B("Join")]),
  ("wl_after", "Only After Get Started", "Shown when the ZIP is outside the area.", "calm", [TX("We're not in your area yet."), B("Join The Waitlist")]))
P("Waitlist", "Waitlist Count: Big Number Or No Count?",
  ("wc_big", "Big Number", "\"142 neighbours waiting\".", "visual", [W("142", SAFFRON, "neighbours waiting")]),
  ("wc_none", "No Count", "Just the join button.", "calm", [W("Join The Waitlist"), B("Join")]))
P("Waitlist", "Waitlist List: Picture Rows Or Simple List?",
  ("wr_pic", "Picture Rows", "Small house picture per area.", "visual", [("photos", 3, 46)]),
  ("wr_list", "Simple List", "Area names only.", "calm", [("cards", [("Royal Oak", "", "38"), ("Troy", "", "21"), ("Novi", "", "17")], None, "dot", "line", 24)]))
P("Member Home", "Member Home Page: House Picture Big Or Small Banner?",
  ("mh_big", "Big Picture", "House fills the top, like the Niko app.", "visual", [("photo", 130, LAGOON, "house", "123 Sample St")]),
  ("mh_small", "Small Banner", "Thin picture strip, visits below.", "calm", [("photo", 50, LAGOON, "house", ""), ("cards", [("Next Visit", "Nov 6", "")], None, "dot", "line", 28)]))
assert len(pp) == 20, len(pp)

# ---------------- Video ----------------
vp, P = mk("vd3_", "Video")
P("Music", "Music: Soft Bed Or No Music? (Tap Play To Listen)",
  ("mu_soft", "Soft Music Bed", "Light, low under the voice. Tap Play to hear it.", "calm", [play()]),
  ("mu_none", "No Music", "Voice only, clearer.", "focused", [play(), ("bars", [.05] * 7, SAFFRON), TX("Nothing to play: voice only")]))
P("Music", "Music Style: Soft Piano Or Acoustic Guitar? (Tap Play To Listen)",
  ("ms_piano", "Soft Piano", "Tap Play to hear it.", "calm", [play()]),
  ("ms_guitar", "Acoustic Guitar", "Tap Play to hear it.", "visual", [play()]))
P("Voice", "Voice: Calm Narrator Or Friendly Tech On Camera?",
  ("vo_calm", "Calm Narrator", "Off-screen voice.", "calm", [play(LAGOON), TX("Voice: calm, warm, unhurried.")]),
  ("vo_tech", "Friendly Tech On Camera", "Your Licensed Tech talks to camera.", "focused", [("photo", 118, SAFFRON, "person"), TX("\"Hi, I'm your Licensed Tech.\"")]))
P("Social", "Social Cut: 15 Seconds Or 6 Second Bumper?",
  ("sc_15", "15 Seconds", "Hook, price, Get Started.", "focused", [("thumb", "From $99", SAFFRON, "block", "house")]),
  ("sc_6", "6 Second Bumper", "Logo, one line, link.", "quick", [W("Smart Upkeep", SAFFRON, "From $99/month")]))
P("Social", "Where First: Instagram Reels Or YouTube Shorts?",
  ("wf_ig", "Instagram Reels", "Local reach, neighbours.", "visual", [("thumb", "Reels", TERRA, "block", "house")]),
  ("wf_yt", "YouTube Shorts", "Search and long life.", "focused", [("thumb", "Shorts", INK, "block", "house")]))
P("Social", "Social Captions: Always Burned In Or App Auto Captions?",
  ("ca_burn", "Burned In", "Our big word blocks on every clip.", "visual", [("thumb", "Catch It Early", SAFFRON, "block", "person")]),
  ("ca_auto", "Auto Captions", "Let the app add them.", "calm", [("thumb", "catch it early", INK, "bottom", "person")]))
P("Series", "Many Videos Coming: One Topic Per Video Or Mixed Tips?",
  ("sr_one", "One Topic Each", "\"Furnace filters in 30 seconds\".", "focused", [("thumb", "Furnace Filters", SAFFRON, "block", "house")]),
  ("sr_mix", "Mixed Tips", "Three quick tips per video.", "quick", [("checks", ["Filter", "Gutters", "Smoke alarm"], JUNGLE, 3)]))
P("Series", "Series Name: \"Upkeep Minute\" Or \"Ask Your Tech\"?",
  ("sn_min", "Upkeep Minute", "Short, regular tips.", "quick", [W("Upkeep Minute", SAFFRON)]),
  ("sn_ask", "Ask Your Tech", "Questions answered by a tech.", "calm", [W("Ask Your Tech", LAGOON)]))
P("Series", "Posting: Same Day Each Week Or When Ready?",
  ("pt_week", "Same Day Each Week", "Every Tuesday.", "focused", [("cal", (6, 13, 20, 27), SAFFRON)]),
  ("pt_ready", "When Ready", "No fixed day.", "calm", [("cal", (4, 15, 22), LAGOON)]))
P("Series", "Video Look: Real Footage Or Drawn Animation?",
  ("vl_real", "Real Footage", "Real homes and techs.", "visual", [("photo", 120, LAGOON, "house", "Metro Detroit")]),
  ("vl_draw", "Drawn Animation", "Simple drawings, like the site.", "calm", [("tiles", [("Furnace", "home"), ("Gutters", "star")], 2, 56)]))
P("Hook", "Hook Price: \"From $99/month\" Or \"$99 a month\"?",
  ("hp_from", "From $99/month", "As the site.", "calm", [W("From $99/Month", SAFFRON)]),
  ("hp_flat", "$99 A Month", "Shorter, punchier.", "quick", [W("$99 A Month", SAFFRON)]))
P("Hook", "Opening Real Home: Detroit Brick Home Or Newer Suburban Home?",
  ("oh_brick", "Brick Home", "Classic Metro Detroit brick.", "calm", [("photo", 120, TERRA, "house", "Brick bungalow")]),
  ("oh_sub", "Newer Suburban", "Two-storey, attached garage.", "focused", [("photo", 120, LAGOON, "house", "Suburban two-storey")]))
P("Captions", "Caption Blocks: One Word At A Time Or Short Phrase?",
  ("cb_word", "One Word", "Punchy, fast.", "quick", [("thumb", "Growing", TERRA, "block", "house")]),
  ("cb_phrase", "Short Phrase", "Easier to read.", "calm", [("thumb", "List Keeps Growing", TERRA, "block", "house")]))
P("Captions", "Terracotta Highlight: Every Word Or Key Words Only?",
  ("th_all", "Every Word", "Whole caption coloured.", "visual", [W("Keeps Growing", TERRA)]),
  ("th_key", "Key Words Only", "Only the main word coloured.", "calm", [W("Keeps Growing", INK, "Growing in terracotta")]))
P("End Card", "End Card With Both Lines: Free Quote On Top Or Book A Visit On Top?",
  ("eb_quote", "Free Quote On Top", "Book a visit underneath.", "quick", [B("Free Quote In Minutes"), ("btn", "Book Your First Visit", "link", LAGOON)]),
  ("eb_book", "Book A Visit On Top", "Free quote underneath.", "focused", [B("Book Your First Visit"), ("btn", "Free Quote In Minutes", "link", LAGOON)]))
P("Watch Page", "Watch Page: Video Only Or Video Then Plans?",
  ("wp_only", "Video Only", "Player and one button, as picked.", "calm", [play(), B("Get Started")]),
  ("wp_plans", "Video Then Plans", "Three plans under the player.", "focused", [play(), ("stats", [("$99", "Essentials"), ("$164", "Plus"), ("$312", "Complete")], "box")]))
P("Site Player", "Tap For Sound Button: Words Or Speaker Icon Only?",
  ("tb_words", "Words", "\"Tap for Sound\", as live.", "calm", [play(), B("Tap for Sound")]),
  ("tb_icon", "Icon Only", "Round speaker button.", "quick", [play(), ("btn", "🔈", "fill", SAFFRON)] if False else [play(), ("btn", "Sound", "outline", INK)]))
P("Next Videos", "Lawn Video: Before And After Lawn Or Tech Mowing?",
  ("lv_ba", "Before And After", "Split screen, same lawn.", "visual", [("photos", 2, 80)]),
  ("lv_mow", "Tech Mowing", "Your tech at work.", "calm", [("photo", 120, JUNGLE, "leaf", "Custom Grass Cutting")]))
P("Next Videos", "Meet Your Tech Video: Real Tech Or Narrated Photos?",
  ("mt_real", "Real Tech On Camera", "A real Smart Upkeep tech talks.", "focused", [("photo", 120, SAFFRON, "person", "Your Licensed Tech")]),
  ("mt_photos", "Narrated Photos", "Photos of the van, tools and checks.", "calm", [("photos", 3, 60)]))
P("Thumbnails", "Thumbnail Text: 3 Words Or 5 Words?",
  ("tt_3", "3 Words", "\"Catch It Early\".", "quick", [("thumb", "Catch It Early", SAFFRON, "block", "house")]),
  ("tt_5", "5 Words", "\"Catch Small Problems Before Winter\".", "focused", [("thumb", "Catch Problems Before Winter", SAFFRON, "block", "house")]))
assert len(vp) == 20, len(vp)

for name, ps in (("upkeep-funnel-followup", fp), ("upkeep-plans-pricing-followup", pp), ("upkeep-video-followup", vp)):
    json.dump({"pairs": ps}, open(f"banks/src-{name}.json", "w"), indent=1, ensure_ascii=False)
    print(name, len(ps))
