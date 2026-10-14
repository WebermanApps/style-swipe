#!/usr/bin/env python3
"""Build Style Swipe deck funnel-deck (Oct 14 2026): Funnel Deck, 20 pairs across the 6 Smart Upkeep funnel stages
(1 Marketing, 2 Video/Catch, 3 Home Page, 4 Info Gather, 5 Price Offer, 6 Make The Sale), based on the live site
(/workspace/smartkeep/funnel-app @ 9a2c4ca). Requested via Deck Launcher (request 3ff8ec04). Card 1 = R64 re-ask of the
skipped Info Gather home-age card (/workspace/smartkeep/info-gather-reask.md). Drawn SVG mockups, example data only. Submit -> 'upkeep'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish, render, TERRA, LAGOON, JUNGLE, SAFFRON, INK
pairs, O, add = deck("fn_", "UpKeep")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
HD = ("hdr", "Smart Upkeep", "Membership from $99/month", SAFFRON, "logo", "S")
def s(*blocks): return render([HD] + list(blocks))
TIERS = [("Essentials", "Seasonal visits", "$99/mo"), ("Plus", "Adds gutters + dryer vent", "$164/mo"), ("Complete", "Whole-home care", "$312/mo")]
# ---- 4 Info Gather (card 1 fixed: re-ask) ----
G4 = "4 Info Gather"
P(G4, "Ask \"About When Was Your Home Built?\" Before The Price?",
  ("age_ask", "Yes, Ask It Now", "Five tiles: Before 1970, 1970-1999, 2000-2014, 2015 Or Newer, Not Sure.", "focused",
   [HD, ("bar", .6, TERRA, "Step 5 of 8"), ("h", "About When Was Your Home Built?", 12), ("cards", [("Before 1970",), ("1970-1999",), ("2000-2014",), ("2015 Or Newer",), ("Not Sure",)], None, "dot", "line", 24)]),
  ("age_skip", "No, Skip It", "We'll know the age from the address before the contract is signed.", "quick",
   [HD, ("bar", .62, TERRA, "Step 5 of 7"), ("h", "How Many AC Units?", 12), ("tiles", [("One", "home"), ("Two", "home"), ("Three+", "home"), ("Not Sure", "search")], 2, 50), ("p", "Home age comes from the address later.")]))
P(G4, "Snap-A-Photo: Side Path Or Equal First Choice?",
  ("ph_side", "Side Path", "Questions stay the main road; a dashed photo tile on system screens.", "calm",
   [HD, ("h", "How Many Furnaces?", 12), ("tiles", [("One", "home"), ("Two", "home")], 2, 50), ("card", "Snap A Photo Instead", "Tech reads the label for you", LAGOON, "", "ic:phone", 36, "line")]),
  ("ph_equal", "Equal First Choice", "Start screen: Answer 7 Questions or Snap 3 Photos.", "visual",
   [HD, ("h", "How Do You Want To Start?", 12), ("tiles", [("Answer Questions", "check"), ("Snap Photos", "phone")], 2, 80), ("p", "Both get your price in minutes.")]))
P(G4, "Water Softener: Its Own Question Or In Extras?",
  ("ws_own", "Its Own Question", "Yes / No screen, as live.", "focused",
   [HD, ("bar", .85, TERRA, "Step 7 of 8"), ("h", "Do You Have A Water Softener?", 12), ("tiles", [("Yes", "check"), ("No", "x")], 2, 60)]),
  ("ws_extra", "One Tile In Extras", "One fewer screen.", "quick",
   [HD, ("bar", 1, JUNGLE, "Last Step"), ("h", "Do You Have Any Of These?", 12), ("checks", ["Water softener", "Sump pump", "Dryer vent", "Gutters"], JUNGLE, 1)]))
P(G4, "Info Gather Finish: Answer Summary Or Straight To Price?",
  ("fin_sum", "Answer Summary", "Every answer with Edit, then See My Price.", "focused",
   [HD, ("h", "Your Price Is Ready", 13), ("table", [("Home size", "2,000-3,000"), ("Furnaces", "1"), ("AC units", "1"), ("Water heater", "Tank")]), ("btn", "See My Price", "fill", SAFFRON)]),
  ("fin_jump", "Straight To Price", "Last answer opens the price page.", "quick",
   [HD, ("word", "$164/mo", 26, SAFFRON, "Plus, for your home"), ("cards", TIERS, None, "dot", "line", 34)]))
# ---- 1 Marketing ----
G1 = "1 Marketing"
P(G1, "First Ad: Price Hook Or Chore List Hook?",
  ("mk_price", "Price Hook", "\"Your whole home, cared for. From $99/month.\"", "quick",
   [("photo", 120, SAFFRON, "house", "From $99/month"), ("h", "Your Whole Home, Cared For", 13), ("btn", "Free Quote In Minutes", "fill", SAFFRON)]),
  ("mk_list", "Chore List Hook", "\"The home to-do list keeps growing.\" with 12 chores.", "visual",
   [("word", "12 Chores", 22, TERRA), ("checks", ["Change furnace filter", "Flush water heater", "Clean dryer vent", "Clean gutters", "Test smoke alarms"], JUNGLE, 0), ("btn", "Hand It Off", "fill", SAFFRON)]))
P(G1, "Lead Channel: Neighbourhood Mailer Or Local Social Ads?",
  ("mk_mail", "Neighbourhood Mailer", "Postcard with a QR code, one ZIP at a time.", "calm",
   [("photo", 110, LAGOON, "house", "Metro Detroit"), ("h", "Scan For Your Price", 13), ("tiles", [("QR Code", "search"), ("Your ZIP", "home")], 2, 50)]),
  ("mk_social", "Local Social Ads", "Short vertical clip, Get Started button.", "visual",
   [("thumb", "Home To-Do List", TERRA, "block", "person"), ("btn", "Get Started", "pill", SAFFRON)]))
P(G1, "Message Lead: Save Time Or Protect The Home?",
  ("mk_time", "Save Time", "\"Get your weekends back.\"", "calm",
   [HD, ("photo", 100, SAFFRON, "sun"), ("h", "Get Your Weekends Back", 13), ("p", "Your Licensed Tech handles the list.")]),
  ("mk_protect", "Protect The Home", "\"Catch small problems before they're big ones.\"", "focused",
   [HD, ("photo", 100, LAGOON, "house"), ("h", "Catch It Before It's Big", 13), ("p", "Leaks, filters and vents, checked every season.")]))
# ---- 2 Video/Catch ----
G2 = "2 Video/Catch"
P(G2, "Video Start: Autoplay Muted Or Tap To Play?",
  ("vd_auto", "Autoplay Muted", "Starts on landing with Unmute and Skip, as live.", "quick",
   [HD, ("thumb", "Home To-Do List", TERRA, "block", "house"), ("btn2", "Unmute", "Skip Video", INK)]),
  ("vd_tap", "Tap To Play", "Poster with a big play button.", "calm",
   [HD, ("raw", f'<rect x="14" y="0" width="212" height="120" rx="8" fill="{SAFFRON}22"/><circle cx="120" cy="60" r="22" fill="{SAFFRON}"/><path d="M114 49 L131 60 L114 71 Z" fill="#fff"/>', 128), ("h", "Watch: 45 Seconds", 12)]))
P(G2, "Video Length: 45 Seconds Or 15 Second Cut?",
  ("vl_45", "45 Seconds", "Full explainer with all three prices.", "focused",
   [HD, ("thumb", "Keeps Growing", TERRA, "bottom", "house"), ("bar", .3, SAFFRON, "0:14", "0:45")]),
  ("vl_15", "15 Second Cut", "Hook, one price, Get Started.", "quick",
   [HD, ("thumb", "From $99", SAFFRON, "block", "sun"), ("bar", .6, SAFFRON, "0:09", "0:15")]))
P(G2, "After The Video: Straight To Get Started Or Back To Home Page?",
  ("va_go", "Straight To Get Started", "End card opens the first question.", "quick",
   [HD, ("h", "Ready For Your Price?", 13), ("btn", "Get Started", "fill", SAFFRON), ("h", "Where's Your Home?", 11), ("input", "ZIP or street address", TERRA, "home")]),
  ("va_home", "Back To Home Page", "Lands on plans and FAQ.", "calm",
   [HD, ("cards", TIERS, None, "dot", "line", 34), ("btn", "See FAQ", "link", LAGOON)]))
# ---- 3 Home Page ----
G3 = "3 Home Page"
P(G3, "Home Page Top: Video Hero Or Price Hero?",
  ("hp_vid", "Video Hero", "Video fills the top, button under it.", "visual",
   [HD, ("thumb", "Home To-Do List", TERRA, "block", "house"), ("btn", "Free Quote In Minutes", "fill", SAFFRON)]),
  ("hp_price", "Price Hero", "Big \"From $99/month\" and the button first.", "focused",
   [HD, ("word", "From $99/month", 24, SAFFRON, "Seasonal home care"), ("btn", "Free Quote In Minutes", "fill", SAFFRON), ("stats", [("4", "Visits/yr"), ("12", "Chores"), ("1", "Tech")])]))
P(G3, "Plans On Home Page: Three Cards Or One Slider?",
  ("pl_cards", "Three Cards", "Essentials, Plus, Complete stacked.", "calm",
   [HD, ("cards", TIERS, None, "dot", "line", 38)]),
  ("pl_slide", "One Slider", "Swipe between plans, one at a time.", "visual",
   [HD, ("tabs", ["Essentials", "Plus", "Complete"]), ("word", "$164/mo", 26, SAFFRON, "Plus"), ("checks", ["Seasonal visits", "Gutters spring + fall", "Dryer vent"], JUNGLE, 3), ("dots", 3, 1, SAFFRON)]))
P(G3, "Trust Row: Licensed Tech Badges Or Neighbour Quotes?",
  ("tr_badge", "Licensed Tech Badges", "Licensed, insured, Metro Detroit.", "focused",
   [HD, ("h", "Your Licensed Tech", 13), ("tiles", [("Licensed", "check"), ("Insured", "star"), ("Local", "home"), ("Same Tech", "heart")], 2, 48)]),
  ("tr_quote", "Neighbour Quotes", "Two short quotes with first names.", "calm",
   [HD, ("bubble", "They caught a leak under the sink before it ruined the floor."), ("bubble", "I don't think about filters any more.", True, LAGOON)]))
P(G3, "Home Page Length: Short With FAQ Link Or Long With Everything?",
  ("hl_short", "Short", "Hero, plans, one button, FAQ link.", "quick",
   [HD, ("photo", 70, SAFFRON, "house"), ("cards", TIERS[:2], None, "dot", "line", 30), ("btn", "Get Started", "fill", SAFFRON), ("btn", "FAQ", "link", LAGOON)]),
  ("hl_long", "Long", "Hero, how it works, plans, FAQ all on one page.", "focused",
   [HD, ("steps", ["Answer", "Price", "Visit"], SAFFRON, 0), ("cards", TIERS[:2], None, "dot", "line", 28), ("checks", ["What's included?", "Can I pause?"], JUNGLE, 0)]))
# ---- 5 Price Offer ----
G5 = "5 Price Offer"
P(G5, "Price Page: Recommended Plan First Or All Three Side By Side?",
  ("po_rec", "Recommended First", "Your plan big, others below.", "focused",
   [HD, ("lbl", "Best For Your Home", SAFFRON), ("word", "$164/mo", 28, SAFFRON, "Plus"), ("btn", "Choose Plus", "fill", SAFFRON), ("cards", [TIERS[0], TIERS[2]], None, "dot", "line", 28)]),
  ("po_all", "All Three Side By Side", "Equal columns, Plus marked Popular.", "calm",
   [HD, ("stats", [("$99", "Essentials"), ("$164", "Plus"), ("$312", "Complete")], "tint"), ("tags", ["Popular: Plus"]), ("btn", "Choose A Plan", "fill", SAFFRON)]))
P(G5, "Welcome Offer: 6 Free Months Or 10% Off Annually?",
  ("wo_months", "6 Free Months", "Pay for 2 years, get 6 months free at the end.", "calm",
   [HD, ("banner", "Welcome Offer: +6 Free Months", SAFFRON, "star"), ("word", "30 Months", 24, INK, "For the price of 24")]),
  ("wo_pct", "10% Off Annually", "Pay the year up front, save 10%.", "quick",
   [HD, ("banner", "Pay Yearly, Save 10%", JUNGLE, "tag"), ("table", [("Monthly", "$164"), ("Yearly", "$1,771"), ("You save", "$197")])]))
P(G5, "Price Breakdown: Hidden In A Dropdown Or Shown?",
  ("pb_drop", "In A Dropdown", "\"See What's Included\" opens the list.", "quick",
   [HD, ("word", "$164/mo", 26, SAFFRON, "Plus"), ("card", "See What's Included", "", LAGOON, "", "ic:down", 30, "line"), ("btn", "Continue", "fill", SAFFRON)]),
  ("pb_show", "Shown Under The Price", "Every visit and service listed.", "focused",
   [HD, ("word", "$164/mo", 26, SAFFRON, "Plus"), ("checks", ["4 seasonal visits", "Furnace filter changes", "Gutters spring + fall", "Dryer vent cleaning"], JUNGLE, 4)]))
# ---- 6 Make The Sale ----
G6 = "6 Make The Sale"
P(G6, "Sign Up: Draw Signature Or Typed Name?",
  ("sg_draw", "Draw Signature", "Finger signature box, as live.", "visual",
   [HD, ("h", "Sign Up", 13), ("raw", f'<rect x="14" y="0" width="212" height="70" rx="8" fill="#fff" stroke="#E5E0D8"/><path d="M30 50 Q50 15 70 45 T110 40 Q130 20 150 48" fill="none" stroke="#0A0A0A" stroke-width="2"/>', 78), ("btn", "Start Membership", "fill", SAFFRON)]),
  ("sg_type", "Typed Name", "Type your name and tick to agree.", "quick",
   [HD, ("h", "Sign Up", 13), ("input", "Full name", SAFFRON, "check"), ("checks", ["I agree to the terms"], JUNGLE, 1), ("btn", "Start Membership", "fill", SAFFRON)]))
P(G6, "Payment: 4 Quarterly Payments Or Monthly Card?",
  ("pay_q", "4 Quarterly Payments", "Four charges a year.", "calm",
   [HD, ("cal", (1, 8, 15, 22), SAFFRON), ("p", "Charged every 3 months.")]),
  ("pay_m", "Monthly Card", "Same day each month.", "quick",
   [HD, ("card", "Card Ending 4242", "Charged on the 1st", LAGOON, "", "ic:card", 40, "line"), ("btn", "Pay $164/mo", "fill", SAFFRON)]))
P(G6, "After Sign Up: Book First Visit Or Welcome Call?",
  ("af_book", "Book First Visit", "Pick a day on a calendar right away.", "focused",
   [HD, ("h", "Pick Your First Visit", 13), ("cal", (6, 13, 20), SAFFRON), ("btn", "Book", "fill", SAFFRON)]),
  ("af_call", "Welcome Call", "Your Licensed Tech texts to book.", "calm",
   [HD, ("h", "You're In", 14), ("bubble", "Hi! I'm your Licensed Tech. What day works for a first visit?", False, LAGOON), ("bubble", "Tuesday morning", True, SAFFRON)]))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish("funnel-deck", "Funnel Deck", "UpKeep", pairs,
        {"brands": ["Smart Upkeep funnel: 1 Marketing, 2 Video/Catch, 3 Home Page, 4 Info Gather, 5 Price Offer, 6 Make The Sale", "Light cream page, white cards, saffron lead"],
         "submit_agent": "upkeep", "submit_to": "UpKeep Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "request_id": "3ff8ec04-4690-4865-81e9-fe5473cedaa1", "categories": ["funnel"],
         "sources": {"site": "/workspace/smartkeep/funnel-app @ 9a2c4ca", "reask": "/workspace/smartkeep/info-gather-reask.md"}},
        seed=1421, n=N, first=1)
