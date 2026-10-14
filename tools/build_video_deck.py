#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-video-ready-1 (Oct 14 2026): Video Deck for the UpKeep Ready Deck Shelf (R66), 20 pairs on the
Smart Upkeep explainer (Video V4, 45s, $99/$164/$312) and the Video/Catch stage. Drawn SVG mockups, example data only. Submit -> 'upkeep'."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish, TERRA, LAGOON, JUNGLE, SAFFRON, INK
pairs, O, add = deck("vd2_", "UpKeep")
HD = ("hdr", "Smart Upkeep", "Video", SAFFRON, "logo", "S")
def play(c=SAFFRON): return ("raw", f'<rect x="14" y="0" width="212" height="118" rx="8" fill="{c}22"/><circle cx="120" cy="59" r="20" fill="{c}"/><path d="M114 49 L130 59 L114 69 Z" fill="#fff"/>', 126)
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
G = "Hook"
P(G, "First Line: Question Or Statement?", ("hk_q", "Question", "\"Is your home to-do list growing?\"", "calm", [HD, ("thumb", "Growing List?", TERRA, "block", "house")]),
  ("hk_s", "Statement", "\"The home to-do list keeps growing.\" as V4.", "focused", [HD, ("thumb", "Keeps Growing", TERRA, "block", "house")]))
P(G, "Opening Shot: Chore List Or A Real Home?", ("os_list", "Chore List", "Checklist fills the frame.", "visual", [HD, ("checks", ["Change furnace filter", "Flush water heater", "Clean dryer vent", "Clean gutters", "Test smoke alarms"], JUNGLE, 2)]),
  ("os_home", "A Real Home", "House first, list later.", "calm", [HD, ("photo", 130, LAGOON, "house", "Metro Detroit")]))
P(G, "Price In The Hook: Yes Or Save It?", ("ph_yes", "Price Up Front", "\"From $99/month\" in the first 3 seconds.", "quick", [HD, ("thumb", "From $99", SAFFRON, "block", "sun")]),
  ("ph_no", "Save It For Later", "Price appears near the end.", "calm", [HD, ("thumb", "Hand It Off", TERRA, "block", "person")]))
G = "Length"
P(G, "Main Video: 45 Seconds Or 30 Seconds?", ("ln_45", "45 Seconds", "Full V4 with all three plans.", "focused", [HD, play(), ("bar", .3, SAFFRON, "0:14", "0:45")]),
  ("ln_30", "30 Seconds", "One plan, faster cuts.", "quick", [HD, play(), ("bar", .45, SAFFRON, "0:14", "0:30")]))
P(G, "Social Cut: 15 Seconds Or 6 Second Bumper?", ("sc_15", "15 Seconds", "Hook, price, Get Started.", "focused", [HD, ("thumb", "From $99", SAFFRON, "block", "house")]),
  ("sc_6", "6 Second Bumper", "Logo, one line, link.", "quick", [HD, ("word", "Smart Upkeep", 22, SAFFRON, "From $99/month")]))
G = "Captions"
P(G, "Captions: Big Word Blocks Or Subtitle Line?", ("cp_block", "Big Word Blocks", "Bold blocks mid-frame.", "visual", [HD, ("thumb", "Hand It Off", SAFFRON, "block", "person")]),
  ("cp_line", "Subtitle Line", "Small line at the bottom.", "calm", [HD, ("thumb", "Hand it off to your tech", INK, "bottom", "person")]))
P(G, "Caption Colour: Saffron Or Terracotta Highlight?", ("cc_sa", "Saffron", "Matches the buttons.", "calm", [HD, ("thumb", "Keeps Growing", SAFFRON, "block", "house")]),
  ("cc_te", "Terracotta", "As V4 today.", "focused", [HD, ("thumb", "Keeps Growing", TERRA, "block", "house")]))
G = "Voice And Music"
P(G, "Voice: Calm Narrator Or Friendly Tech?", ("vo_calm", "Calm Narrator", "Off-screen voice.", "calm", [HD, play(LAGOON), ("p", "Voice: calm, warm, unhurried.")]),
  ("vo_tech", "Friendly Tech On Camera", "Your Licensed Tech talks to camera.", "focused", [HD, ("photo", 118, SAFFRON, "person"), ("p", "\"Hi, I'm your Licensed Tech.\"")]))
P(G, "Music: Soft Bed Or No Music?", ("mu_soft", "Soft Music Bed", "Light, low under the voice.", "calm", [HD, play(), ("bars", [.3, .5, .4, .6, .45, .5, .35], SAFFRON)]),
  ("mu_none", "No Music", "Voice only, clearer.", "focused", [HD, play(), ("bars", [.05, .05, .05, .05, .05, .05, .05], SAFFRON)]))
G = "Poster And Thumbnail"
P(G, "Poster: Chore List Or Smiling Tech?", ("po_list", "Chore List", "12 Chores badge, as V4.", "visual", [HD, ("thumb", "12 Chores", TERRA, "block", "house")]),
  ("po_tech", "Smiling Tech", "Friendly face, plan price.", "calm", [HD, ("thumb", "Meet Your Tech", SAFFRON, "bottom", "person")]))
P(G, "Phone Format: 9:16 Full Screen Or 16:9 In A Card?", ("pf_916", "9:16 Full Screen", "Fills the phone.", "visual", [HD, ("thumb", "From $99", SAFFRON, "block", "person")]),
  ("pf_169", "16:9 In A Card", "Smaller, page stays visible.", "calm", [HD, play(), ("btn", "Get Started", "fill", SAFFRON)]))
G = "Placement"
P(G, "On The Home Page: Top Hero Or After Plans?", ("pl_top", "Top Hero", "First thing a visitor sees.", "visual", [HD, play(), ("cards", [("Essentials", "", "$99/mo"), ("Plus", "", "$164/mo")], None, "dot", "line", 26)]),
  ("pl_after", "After Plans", "Plans first, video below.", "focused", [HD, ("cards", [("Essentials", "", "$99/mo"), ("Plus", "", "$164/mo")], None, "dot", "line", 26), play()]))
P(G, "Watch Page: Video Alone Or With Chapters?", ("wp_alone", "Video Alone", "Just the player and a button.", "quick", [HD, play(), ("btn", "Get Started", "fill", SAFFRON)]),
  ("wp_chap", "With Chapters", "Problem, Plans, How It Works.", "focused", [HD, play(), ("timeline", [("0:00 Problem", "The list keeps growing"), ("0:15 Plans", "$99 / $164 / $312"), ("0:35 How It Works", "Your Licensed Tech")])]))
P(G, "Skip Video: Visible Button Or Small Link?", ("sk_btn", "Visible Button", "Skip Video pill on the player.", "quick", [HD, play(), ("btn2", "Unmute", "Skip Video", INK)]),
  ("sk_link", "Small Link", "Quiet text link under it.", "calm", [HD, play(), ("btn", "Skip", "link", LAGOON)]))
G = "End Card"
P(G, "End Card: One Button Or Three Plans?", ("ec_one", "One Button", "Get Started, nothing else.", "quick", [HD, ("word", "Ready?", 26, INK), ("btn", "Get Started", "fill", SAFFRON)]),
  ("ec_three", "Three Plans", "Essentials, Plus, Complete with prices.", "focused", [HD, ("stats", [("$99", "Essentials"), ("$164", "Plus"), ("$312", "Complete")], "tint")]))
P(G, "End Card Line: Free Quote Or Book A Visit?", ("el_quote", "Free Quote In Minutes", "As the site button.", "quick", [HD, ("btn", "Free Quote In Minutes", "fill", SAFFRON)]),
  ("el_book", "Book Your First Visit", "Straight to booking.", "focused", [HD, ("cal", (6, 13, 20), SAFFRON), ("btn", "Book", "fill", SAFFRON)]))
G = "Plans In The Video"
P(G, "Plans: All Three Prices Or Just From $99?", ("pv_all", "All Three", "$99 / $164 / $312, as V4.", "focused", [HD, ("stats", [("$99", "Essentials"), ("$164", "Plus"), ("$312", "Complete")], "box")]),
  ("pv_from", "Just From $99", "One number, simpler.", "quick", [HD, ("word", "From $99/month", 24, SAFFRON)]))
P(G, "Show What's Included: Ticking List Or Quick Icons?", ("si_list", "Ticking List", "Items tick off one by one.", "calm", [HD, ("checks", ["Furnace filter", "Water heater flush", "Dryer vent", "Gutters"], JUNGLE, 3)]),
  ("si_icons", "Quick Icons", "Four icons pop in.", "visual", [HD, ("tiles", [("Filters", "home"), ("Water", "speaker"), ("Vents", "star"), ("Gutters", "check")], 2, 48)]))
G = "Next Video"
P(G, "Next Video To Make: Lawn Add-On Or Meet Your Tech?", ("nv_lawn", "Lawn Add-On", "Custom grass cutting explainer.", "visual", [HD, ("photo", 120, JUNGLE, "leaf", "Custom Grass Cutting")]),
  ("nv_tech", "Meet Your Tech", "Who comes to your home.", "calm", [HD, ("photo", 120, SAFFRON, "person", "Your Licensed Tech")]))
P(G, "How Often: One New Video A Month Or One Per Season?", ("hf_month", "One A Month", "Fresh clip every month.", "quick", [HD, ("cal", (1,), SAFFRON)]),
  ("hf_season", "One Per Season", "Spring, summer, fall, winter.", "calm", [HD, ("tiles", [("Spring", "star"), ("Summer", "star"), ("Fall", "star"), ("Winter", "star")], 2, 48)]))
assert len(pairs) == 20, len(pairs)
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish("upkeep-video-ready-1", "Video Deck", "UpKeep", pairs, {"submit_agent": "upkeep", "submit_to": "UpKeep Agent", "deck_size": 20, "section_counts": cnt,
        "topic": "upkeep-video", "shelf": True, "one_card_per_screen": True}, seed=2010, n=20)
