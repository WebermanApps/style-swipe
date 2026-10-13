#!/usr/bin/env python3
"""Build Style Swipe deck wellnest-1 (PUBLISHED): 50 pairs for the WellNest agent (a Chiang Mai wellness business, registered
but not open yet; name follow-up with a lawyer in progress). Based on the Oct 13 reorg chart, team feed, team-sync recaps
and WellNest's dashboard. Example data only. Pattern: tools/build_dashboard_2.py + draft_svg.py via team_kit.py."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "wellnest-1"; pairs, O, add = deck("wn1_", "WellNest")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
HW = ("hdr", "WellNest", "Chiang Mai · Opening Soon", JUNGLE, "logo", "W")
def nest(cx, cy, s, c):
    return f'<path d="M{cx-s} {cy} Q{cx} {cy+s*1.1} {cx+s} {cy}" fill="none" stroke="{c}" stroke-width="{s*.14}" stroke-linecap="round"/><path d="M{cx-s*.8} {cy+s*.25} Q{cx} {cy+s*.95} {cx+s*.8} {cy+s*.25}" fill="none" stroke="{c}" stroke-width="{s*.1}" stroke-linecap="round"/>' + dot(cx, cy - s * .15, s * .28, c)

G = "Logo Direction"
def lg(k):
    if k == "nest": m = nest(120, 110, 40, JUNGLE) + t(120, 190, "WellNest", 26, INK, "khand", anchor="middle")
    elif k == "word": m = t(120, 140, "WellNest", 40, JUNGLE, "khand", anchor="middle") + t(120, 160, "CHIANG MAI", 7, MUTE, "hind", 600, "middle", 'letter-spacing="3"')
    elif k == "leaf": m = photo(80, 60, 80, 80, JUNGLE, "leaf", 40) + t(120, 180, "WellNest", 26, INK, "khand", anchor="middle")
    elif k == "circle": m = f'<circle cx="120" cy="110" r="44" fill="{JUNGLE}"/>' + t(120, 126, "W", 46, "#FFFFFF", "khand", anchor="middle") + t(120, 190, "WellNest", 22, INK, "khand", anchor="middle")
    elif k == "lower": m = t(120, 140, "wellnest", 38, JUNGLE, "hind", 400, "middle")
    elif k == "split": m = t(120, 140, "Well", 38, INK, "khand", anchor="end") + t(120, 140, "Nest", 38, TERRA, "khand")
    elif k == "side": m = nest(60, 128, 26, JUNGLE) + t(96, 140, "WellNest", 30, INK, "khand")
    else: m = nest(120, 100, 40, JUNGLE) + t(120, 180, "WELLNEST", 18, INK, "hind", 600, "middle", 'letter-spacing="5"')
    return [("raw", m, 0)]
pr(G, "Nest Mark Or Wordmark Alone?", lg, ("lg_nest", "Drawn Nest Mark Plus Name", "A small nest above the name.", "calm", "nest"), ("lg_word", "Green Wordmark Only", "Name, no symbol.", "focused", "word"))
pr(G, "Leaf Or Letter Circle?", lg, ("lg_leaf", "Leaf Mark", "Nature-first symbol.", "calm", "leaf"), ("lg_circle", "Green Circle With W", "Bold badge.", "visual", "circle"))
pr(G, "Lowercase Or Two-Tone?", lg, ("lg_lower", "Soft Lowercase", "Gentle and quiet.", "calm", "lower"), ("lg_twotone", "Well In Ink, Nest In Terracotta", "Two-tone name.", "visual", "split"))
pr(G, "Mark Beside Or Spaced Caps?", lg, ("lg_side", "Mark Beside The Name", "Fits wide headers.", "focused", "side"), ("lg_caps", "Mark Over Spaced Caps", "Airy and formal.", "calm", "caps"))

G = "Color Lead"
def cl(k):
    c = {"jungle": JUNGLE, "lagoon": LAGOON, "saffron": SAFFRON, "terra": TERRA, "ink": INK, "mix": JUNGLE}[k]
    b = [("hdr", "WellNest", "Chiang Mai · Opening Soon", c, "band", "W"), ("photo", 100, c, "leaf"), ("btn", "Join The Waitlist", "fill", c)]
    if k == "mix": b = [("hdr", "WellNest", "Chiang Mai · Opening Soon", JUNGLE, "logo", "W"), ("photo", 100, JUNGLE, "leaf"), ("btn", "Join The Waitlist", "fill", TERRA)]
    return b
pr(G, "Jungle Or Lagoon?", cl, ("cl_jungle", "Jungle Green Leads", "Forest calm.", "calm", "jungle"), ("cl_lagoon", "Lagoon Blue Leads", "Water calm.", "calm", "lagoon"))
pr(G, "Saffron Or Terracotta?", cl, ("cl_saffron", "Saffron Leads", "Warm sunrise.", "visual", "saffron"), ("cl_terra", "Terracotta Leads", "Earthy warmth.", "visual", "terra"))
pr(G, "All Ink Or Green Plus Terracotta Button?", cl, ("cl_ink", "Ink Black Header", "Neutral, photos carry color.", "focused", "ink"), ("cl_mix", "Green Mark, Terracotta Button", "Two accents.", "visual", "mix"))

G = "Coming Soon Page"
def cs(k):
    if k == "photo": return [("photo", 150, JUNGLE, "sun"), ("h", "Opening Soon In Chiang Mai", 15, INK, True), ("btn", "Join The Waitlist", "fill", JUNGLE)]
    if k == "word": return [("gap", 60), ("raw", nest(120, 90, 26, JUNGLE), 50), ("h", "Opening Soon", 24, INK, True), ("p", "A quiet place to rest and reset in Chiang Mai.", 40, MUTE, True), ("btn", "Join The Waitlist", "fill", JUNGLE)]
    if k == "count": return [HW, ("word", "Spring 2027", 30, JUNGLE, "Target Opening · Example"), ("btn", "Get Notified", "fill", INK)]
    if k == "nodate": return [HW, ("h", "Opening Soon", 24), ("p", "No date yet. We'll tell you first."), ("btn", "Get Notified", "fill", INK)]
    if k == "email": return [HW, ("h", "Be First In", 20), ("input", "Your Email", JUNGLE, "star"), ("btn", "Join", "fill", JUNGLE)]
    if k == "line": return [HW, ("h", "Be First In", 20), ("cards", [("Message Us On LINE", "Quick replies", "", "ic:phone")], JUNGLE, "ic:phone")]
    if k == "peek": return [HW, ("lbl", "A Peek Inside"), ("photos", 3, 80, ["room", "leaf", "sun"], [JUNGLE, LAGOON, SAFFRON]), ("btn", "Join The Waitlist", "fill", JUNGLE)]
    return [HW, ("lbl", "What To Expect"), ("checks", ["Massage", "Yoga Mornings", "Herbal Steam", "Quiet Garden"], JUNGLE, 0)]
pr(G, "Big Photo Or Calm Words?", cs, ("cs_photo", "Big Garden Photo", "Photo leads.", "visual", "photo"), ("cs_words", "Mark And Words On White", "Very quiet.", "calm", "word"))
pr(G, "Show A Season Or No Date?", cs, ("cs_season", "Target Season Shown", "Spring 2027, example.", "focused", "count"), ("cs_nodate", "No Date Yet", "We'll tell you first.", "calm", "nodate"))
pr(G, "Email Or LINE?", cs, ("cs_email", "Email Signup", "Classic list.", "focused", "email"), ("cs_line", "Message On LINE", "How locals chat.", "action", "line"))
pr(G, "Photos Or What-To-Expect List?", cs, ("cs_peek", "Three Peek Photos", "Show the space.", "visual", "peek"), ("cs_expect", "What To Expect List", "Services as a list.", "focused", "list"))

G = "Service Cards"
S = [("Thai Massage", "60 or 90 min"), ("Morning Yoga", "Small groups"), ("Herbal Steam", "30 min"), ("Garden Rest", "Day pass")]
def sv(k):
    if k == "photo": return [HW, ("raw", "".join(photo(14 + (i % 2) * 108, 60 + (i // 2) * 106, 104, 70, ACC[i], ["person", "sun", "leaf", "room"][i]) + t(18 + (i % 2) * 108, 144 + (i // 2) * 106, S[i][0], 10, INK, "khand") + t(18 + (i % 2) * 108, 155 + (i // 2) * 106, S[i][1], 6.5, MUTE) for i in range(4)), 212)]
    if k == "rows": return [HW, ("cards", S, JUNGLE, "ic:heart", "line", 40)]
    if k == "price": return [HW, ("cards", [(a, b, "See Rates") for a, b in S], JUNGLE)]
    if k == "noprice": return [HW, ("cards", S, JUNGLE), ("btn", "Ask About Rates", "line", INK)]
    if k == "time": return [HW, ("cards", [(a, b, "tag:" + b.split()[0]) for a, b in S], LAGOON)]
    if k == "feel": return [HW, ("cards", [("Thai Massage", "For tired legs"), ("Morning Yoga", "For a clear head"), ("Herbal Steam", "For deep rest")], JUNGLE)]
    if k == "book": return [HW, ("raw", "".join(rect(14, 60 + i * 50, 212, 44, "#FFFFFF", LINE, 8) + t(24, 78 + i * 50, n, 10, INK, "khand") + t(24, 90 + i * 50, d, 6.5, MUTE) + btn(70 + i * 50, "Book", "fill", JUNGLE, 170, 48, 22, 7) for i, (n, d) in enumerate(S[:3])), 150)]
    return [HW, ("cards", S[:3], JUNGLE), ("btn", "Book A Visit", "fill", JUNGLE)]
pr(G, "Photo Grid Or Icon Rows?", sv, ("sv_photos", "Photo Grid", "Four photo cards.", "visual", "photo"), ("sv_rows", "Icon Rows", "Neat list.", "focused", "rows"))
pr(G, "Rates Link Or Ask Button?", sv, ("sv_rates", "See Rates On Each", "Link per service.", "focused", "price"), ("sv_ask", "One Ask About Rates", "Rates by message.", "calm", "noprice"))
pr(G, "Length Tag Or Feeling Line?", sv, ("sv_length", "Length Tag", "60 min, small groups.", "quick", "time"), ("sv_feeling", "What It's For", "For tired legs.", "calm", "feel"))
pr(G, "Book On Each Or One Button?", sv, ("sv_bookeach", "Book Button On Each", "Pick and go.", "action", "book"), ("sv_bookone", "One Book Button", "Choose inside.", "calm", "one"))

G = "Booking Flow"
def bk(k):
    if k == "cal": return [HW, ("lbl", "Pick A Day"), ("cal", (15, 16, 18, 22), JUNGLE), ("btn", "Next", "fill", INK)]
    if k == "slots": return [HW, ("lbl", "Pick A Time"), ("cards", [("Thu", "10:00 AM", "tag:Open"), ("Thu", "2:00 PM", "tag:Open"), ("Fri", "9:00 AM", "tag:Open")], JUNGLE)]
    if k == "steps": return [HW, ("steps", ["Service", "Day", "Time", "Done"], JUNGLE, 1), ("cards", S[:2], JUNGLE)]
    if k == "dots": return [HW, ("dots", 4, 1, JUNGLE), ("h", "Which Service?", 16), ("cards", S[:3], JUNGLE)]
    if k == "chat": return [HW, ("bubble", "Hi, what would you like to book?"), ("bubble", "Massage on Thursday", True), ("bubble", "10 AM or 2 PM?")]
    if k == "form": return [HW, ("lbl", "Book"), ("table", [("Service", "Thai Massage"), ("Day", "Thu"), ("Time", "10:00 AM"), ("Name", "Example Guest")]), ("btn", "Confirm", "fill", JUNGLE)]
    if k == "done": return [("gap", 50), ("raw", dot(120, 70, 22, JUNGLE + "22") + ic("check", 106, 56, 28, JUNGLE, 2), 60), ("h", "See You Thursday", 18, INK, True), ("p", "10:00 AM · Thai Massage", 40, MUTE, True)]
    return [("gap", 30), ("h", "See You Thursday", 18, INK, True), ("lbl", "Before You Come"), ("checks", ["Arrive 10 min early", "Wear loose clothes", "Skip a big meal"], JUNGLE, 0)]
pr(G, "Calendar Or Time Slots?", bk, ("bk_cal", "Month Calendar", "Pick a day first.", "visual", "cal"), ("bk_slots", "Open Slot Rows", "Pick a time straight away.", "quick", "slots"))
pr(G, "Numbered Steps Or Dots?", bk, ("bk_steps", "Numbered Steps", "Service, Day, Time, Done.", "focused", "steps"), ("bk_dots", "Progress Dots", "Quieter progress.", "calm", "dots"))
pr(G, "Chat Or Form?", bk, ("bk_chat", "Book By Chat", "Feels personal.", "calm", "chat"), ("bk_form", "Short Form", "All on one screen.", "quick", "form"))
pr(G, "Check Mark Or Prep List?", bk, ("bk_check", "Green Check Done", "Simple confirm.", "calm", "done"), ("bk_prep", "Before You Come List", "Helpful prep.", "focused", "prep"))

G = "Retreat Schedule"
def rs(k):
    D = [("7:00 AM", "Morning Yoga"), ("9:00 AM", "Breakfast"), ("11:00 AM", "Thai Massage"), ("4:00 PM", "Herbal Steam")]
    if k == "timeline": return [HW, ("h", "A Day At WellNest", 15), ("timeline", D)]
    if k == "table": return [HW, ("h", "A Day At WellNest", 15), ("table", D, True)]
    if k == "photo": return [HW, ("photo", 80, SAFFRON, "sun", "Morning"), ("cards", D[:2], JUNGLE, "dot", "line", 28)]
    if k == "icons": return [HW, ("cards", [(b, a) for a, b in D], None, "ic:clock", "line", 36)]
    if k == "days": return [HW, ("tabs", ["Day 1", "Day 2", "Day 3"]), ("timeline", D[:3])]
    if k == "one": return [HW, ("h", "One Day Retreat", 16), ("timeline", D[:3])]
    if k == "am": return [HW, ("lbl", "Morning"), ("cards", D[:2], SAFFRON, "dot", "line", 26), ("lbl", "Afternoon"), ("cards", D[2:], LAGOON, "dot", "line", 26)]
    return [HW, ("checks", [f"{a} {b}" for a, b in D], JUNGLE, 0)]
pr(G, "Timeline Or Table?", rs, ("rs_timeline", "Day Timeline", "Dots down the side.", "calm", "timeline"), ("rs_table", "Shaded Table", "Time and activity.", "focused", "table"))
pr(G, "Photo Header Or Icon Rows?", rs, ("rs_photo", "Morning Photo Header", "Sets the mood.", "visual", "photo"), ("rs_icons", "Clock Icon Rows", "Neat and clear.", "focused", "icons"))
pr(G, "Multi-Day Tabs Or One Day?", rs, ("rs_days", "Day 1, 2, 3 Tabs", "For longer stays.", "focused", "days"), ("rs_oneday", "One Day Only", "Keep it simple.", "calm", "one"))
pr(G, "Morning-Afternoon Groups Or Checklist?", rs, ("rs_ampm", "Morning And Afternoon", "Two color groups.", "visual", "am"), ("rs_check", "Plain Checklist", "Tick as you go.", "quick", "chk"))

G = "Waitlist Form"
def wl(k):
    if k == "one": return [HW, ("h", "Join The Waitlist", 18), ("input", "Your Email", JUNGLE, "star"), ("btn", "Join", "fill", JUNGLE)]
    if k == "more": return [HW, ("h", "Join The Waitlist", 18), ("input", "Your Name", JUNGLE, "star"), ("input", "Your Email", JUNGLE, "star"), ("lbl", "Interested In"), ("tags", ["Massage", "Yoga", "Steam", "Retreat"])]
    if k == "perk": return [HW, ("banner", "Waitlist Gets First Pick Of Dates", SAFFRON, "star"), ("input", "Your Email", JUNGLE, "star"), ("btn", "Join", "fill", JUNGLE)]
    if k == "noperk": return [HW, ("input", "Your Email", JUNGLE, "star"), ("btn", "Join", "fill", JUNGLE)]
    if k == "thanks": return [("gap", 60), ("raw", nest(120, 80, 26, JUNGLE), 50), ("h", "You're On The List", 18, INK, True)]
    return [("gap", 60), ("h", "You're On The List", 18, INK, True), ("p", "You're number 42. Share to move up.", 40, MUTE, True), ("btn", "Share", "line", INK)]
pr(G, "Email Only Or More Questions?", wl, ("wl_one", "Email Only", "Fastest signup.", "quick", "one"), ("wl_more", "Name, Email, Interests", "Learn what they want.", "focused", "more"))
pr(G, "Perk Banner Or No Perk?", wl, ("wl_perk", "First-Pick Perk Banner", "A reason to join.", "action", "perk"), ("wl_noperk", "No Perk", "Just the form.", "calm", "noperk"))
pr(G, "Quiet Thanks Or Share To Move Up?", wl, ("wl_thanks", "Quiet Thank You", "Nest mark and a line.", "calm", "thanks"), ("wl_share", "Place Number, Share To Move Up", "Grows the list.", "action", "share"))

G = "Instagram Grid"
def ig(k):
    if k == "photos": return [("raw", "".join(photo(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, ACC[i % 4], ["leaf", "sun", "room", "person"][i % 4], 2) for i in range(9)), 230)]
    if k == "mixed": return [("raw", "".join((photo(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, ACC[i % 4], "leaf", 2) if i % 2 == 0 else rect(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, JUNGLE + "14", "none", 2) + t(48 + (i % 3) * 72, 68 + (i // 3) * 72, "Rest", 12, JUNGLE, "khand", anchor="middle")) for i in range(9)), 230)]
    if k == "green": return [("raw", "".join(photo(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, JUNGLE, ["leaf", "sun", "room"][i % 3], 2) for i in range(9)), 230)]
    if k == "warm": return [("raw", "".join(photo(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, [SAFFRON, TERRA][i % 2], ["sun", "leaf", "room"][i % 3], 2) for i in range(9)), 230)]
    if k == "frame": return [("raw", "".join(rect(14 + (i % 3) * 72, 30 + (i // 3) * 72, 68, 68, "#FFFFFF", LINE, 2) + photo(20 + (i % 3) * 72, 36 + (i // 3) * 72, 56, 56, ACC[i % 4], "leaf", 2) for i in range(9)), 230)]
    if k == "full": return [("raw", "".join(photo(14 + (i % 3) * 72, 30 + (i // 3) * 72, 70, 70, ACC[i % 4], "sun", 0) for i in range(9)), 230)]
    if k == "quote": return [("raw", rect(14, 40, 212, 212, JUNGLE + "14", "none", 4) + t(120, 140, "Rest Is", 26, JUNGLE, "khand", anchor="middle") + t(120, 170, "Part Of The Work", 20, INK, "khand", anchor="middle"), 230)]
    return [("raw", photo(14, 40, 212, 212, JUNGLE, "leaf", 4) + rect(14, 220, 212, 32, "#FFFFFFEE") + t(24, 241, "Rest Is Part Of The Work", 12, INK, "khand"), 230)]
pr(G, "All Photos Or Photos With Word Tiles?", ig, ("ig_photos", "All Photo Grid", "Every post a photo.", "visual", "photos"), ("ig_mixed", "Photos And Word Tiles", "Alternating quotes.", "calm", "mixed"))
pr(G, "Cool Green Or Warm Tones?", ig, ("ig_green", "Cool Green Feed", "Forest calm.", "calm", "green"), ("ig_warm", "Warm Saffron And Terracotta", "Sunrise feel.", "visual", "warm"))
pr(G, "White Frames Or Edge To Edge?", ig, ("ig_frame", "White Frame Per Post", "Gallery look.", "focused", "frame"), ("ig_full", "Edge To Edge", "Seamless grid.", "visual", "full"))
pr(G, "Quote Tile Or Photo With Caption?", ig, ("ig_quote", "Plain Quote Tile", "Words on tint.", "calm", "quote"), ("ig_caption", "Photo With Caption Strip", "Words on a photo.", "visual", "cap"))

G = "Guest Words"
def gw(k):
    if k == "quote": return [HW, ("lbl", "Guests Say"), ("word", "Slept Better", 26, JUNGLE, "Example Guest"), ("p", "I left lighter than I came. The garden is the best part.", 40, MUTE, True)]
    if k == "cards": return [HW, ("lbl", "Guests Say"), ("bubble", "I left lighter than I came."), ("bubble", "The garden is the best part."), ("bubble", "Best massage in the city.")]
    if k == "stars": return [HW, ("raw", "".join(ic("star", 64 + i * 24, 70, 20, SAFFRON, 2) for i in range(5)) + t(120, 116, "Example Rating", 8, MUTE, anchor="middle"), 60), ("p", "I left lighter than I came.", 40, INK, True)]
    if k == "nostars": return [HW, ("p", "I left lighter than I came.", 40, INK, True), ("p", "Example Guest", 40, MUTE, True)]
    if k == "photo": return [HW, ("photo", 90, JUNGLE, "person"), ("p", "I left lighter than I came. · Example Guest", 40, INK)]
    return [HW, ("h", "\u201cI Left Lighter\u201d", 20), ("p", "Example Guest", 40, MUTE)]
pr(G, "Big Quote Or Chat Bubbles?", gw, ("gw_quote", "One Big Quote", "Two words, large.", "calm", "quote"), ("gw_bubbles", "Three Bubbles", "Many short voices.", "visual", "cards"))
pr(G, "Stars Or Words Only?", gw, ("gw_stars", "Saffron Stars", "Rating up top.", "visual", "stars"), ("gw_nostars", "Words Only", "No rating.", "calm", "nostars"))
pr(G, "Guest Photo Or Text Only?", gw, ("gw_photo", "Guest Photo", "A face with the words.", "visual", "photo"), ("gw_text", "Text Only", "Private and simple.", "calm", "text"))

G = "Location Card"
def lc(k):
    if k == "map": return [HW, ("map", 110), ("cards", [("Example Road, Chiang Mai", "40 min from the old city", "", "ic:home")], JUNGLE, "ic:home")]
    if k == "photo": return [HW, ("photo", 110, JUNGLE, "sun", "Mountain Valley, North Of Town"), ("btn", "Get Directions", "line", INK)]
    if k == "steps": return [HW, ("h", "Getting Here", 16), ("timeline", [("From The Old City", "40 min by car"), ("Turn At The Market", "Example landmark"), ("Green Gate", "Park inside")])]
    if k == "pin": return [HW, ("h", "Getting Here", 16), ("btn", "Open In Maps", "fill", JUNGLE), ("btn", "Send Pickup Request", "line", INK)]
    if k == "pickup": return [HW, ("cards", [("Free Pickup", "From the old city", "tag:Ask")], SAFFRON, "dot", "tint", 40)]
    return [HW, ("cards", [("Getting Here", "Taxi or own car", "")], JUNGLE)]
pr(G, "Map Or Valley Photo?", lc, ("lc_map", "Drawn Route Map", "Shows the drive.", "focused", "map"), ("lc_photo", "Valley Photo", "Sells the setting.", "visual", "photo"))
pr(G, "Landmark Steps Or Map Buttons?", lc, ("lc_steps", "Landmark Steps", "Turn by turn.", "focused", "steps"), ("lc_buttons", "Maps And Pickup Buttons", "Two taps.", "action", "pin"))
pr(G, "Offer Pickup Or Not?", lc, ("lc_pickup", "Pickup Offer Card", "Saffron tint.", "action", "pickup"), ("lc_nopickup", "No Pickup Mention", "Taxi or own car.", "calm", "none"))

G = "Name Check Tracker"
def nc(k):
    if k == "steps": return [HW, ("h", "Name Check", 16), ("steps", ["Drafted", "Sent", "Reply", "Settled"], JUNGLE, 0), ("cards", [("Lawyer Email", "Goes out today", "tag:Today")], TERRA)]
    if k == "time": return [HW, ("h", "Name Check", 16), ("timeline", [("Email Drafted", "Example date"), ("Email Sent", "Today"), ("Reply Expected", "Within a week")])]
    if k == "banner": return [HW, ("banner", "Name Check Open · Lawyer Email Today", TERRA, "clock"), ("cards", S[:2], JUNGLE)]
    if k == "quiet": return [HW, ("cards", S[:2], JUNGLE), ("cards", [("Name Check", "In progress", "tag:Open")], SAFFRON)]
    if k == "plan": return [HW, ("lbl", "If The Name Changes"), ("checks", ["Pick backup name", "Update logo", "Update social handles"], SAFFRON, 0)]
    return [HW, ("lbl", "If The Name Changes"), ("p", "Wait for the lawyer's reply before planning anything.")]
pr(G, "Steps Or Timeline?", nc, ("nc_steps", "Four-Step Tracker", "Drafted to Settled.", "visual", "steps"), ("nc_timeline", "Dated Timeline", "What happened when.", "focused", "time"))
pr(G, "Banner Or Quiet Card?", nc, ("nc_banner", "Terracotta Banner", "Can't miss it.", "action", "banner"), ("nc_quiet", "Quiet Saffron Card", "In the list.", "calm", "quiet"))
pr(G, "Backup Plan Now Or Wait?", nc, ("nc_backup", "Backup Plan Checklist", "Ready if needed.", "focused", "plan"), ("nc_wait", "Wait For The Reply", "No plan yet.", "calm", "wait"))

G = "Welcome Email"
def we(k):
    b = [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 24)]
    if k == "photo": b += [("photo", 90, JUNGLE, "leaf"), ("h", "Welcome To WellNest", 15, INK, True), ("p", "You're on the list. We'll write when doors open.", 38, MUTE, True)]
    elif k == "plain": b += [("raw", nest(120, 60, 18, JUNGLE), 40), ("h", "Welcome To WellNest", 15, INK, True), ("p", "You're on the list. We'll write when doors open.", 38, MUTE, True)]
    elif k == "tips": b += [("h", "Welcome To WellNest", 15, INK, True), ("lbl", "Three Small Rest Tips"), ("checks", ["Ten slow breaths", "Walk outside", "Screens off by nine"], JUNGLE, 0)]
    elif k == "story": b += [("h", "Welcome To WellNest", 15, INK, True), ("p", "WellNest started with a garden and a simple idea: rest should be easy to find. Here's what we're building.", 38, INK)]
    elif k == "btn": b += [("h", "Welcome To WellNest", 15, INK, True), ("btn", "Follow On Instagram", "fill", JUNGLE)]
    else: b += [("h", "Welcome To WellNest", 15, INK, True), ("btn", "Reply And Say Hi", "link", TERRA)]
    return b
pr(G, "Photo Or Nest Mark Header?", we, ("we_photo", "Garden Photo Header", "Warm opener.", "visual", "photo"), ("we_mark", "Nest Mark Only", "Quiet opener.", "calm", "plain"))
pr(G, "Rest Tips Or Our Story?", we, ("we_tips", "Three Rest Tips", "Useful right away.", "focused", "tips"), ("we_story", "Short Founding Story", "Why it exists.", "calm", "story"))
pr(G, "Follow Button Or Reply Link?", we, ("we_follow", "Follow On Instagram Button", "Grow the feed.", "action", "btn"), ("we_reply", "Reply And Say Hi Link", "Start a talk.", "calm", "reply"))

G = "Icon Style"
def ic_(k):
    K = ["heart", "star", "clock", "home"]; N = ["Massage", "Yoga", "Steam", "Garden"]
    if k == "line": return [HW, ("tiles", list(zip(N, K)), 2, 70)]
    if k == "solid": return [HW, ("tiles", list(zip(N, K)), 2, 70, "solid")]
    if k == "green": return [HW, ("raw", "".join(rect(14 + (i % 2) * 108, 60 + (i // 2) * 78, 104, 70, "#FFFFFF", LINE, 9) + ic(K[i], 24 + (i % 2) * 108, 70 + (i // 2) * 78, 22, JUNGLE, 2) + t(24 + (i % 2) * 108, 120 + (i // 2) * 78, N[i], 10, INK, "khand") for i in range(4)), 160)]
    if k == "multi": return [HW, ("raw", "".join(rect(14 + (i % 2) * 108, 60 + (i // 2) * 78, 104, 70, "#FFFFFF", LINE, 9) + ic(K[i], 24 + (i % 2) * 108, 70 + (i // 2) * 78, 22, ACC[i], 2) + t(24 + (i % 2) * 108, 120 + (i // 2) * 78, N[i], 10, INK, "khand") for i in range(4)), 160)]
    if k == "round": return [HW, ("raw", "".join(f'<circle cx="{40+i*53}" cy="90" r="20" fill="{JUNGLE}1F"/>' + ic(K[i], 30 + i * 53, 80, 20, JUNGLE, 2) + t(40 + i * 53, 126, N[i], 8, INK, "khand", anchor="middle") for i in range(4)), 90)]
    if k == "bare": return [HW, ("raw", "".join(ic(K[i], 30 + i * 53, 76, 22, INK, 1.6) + t(40 + i * 53, 120, N[i], 8, INK, "khand", anchor="middle") for i in range(4)), 90)]
    if k == "thin": return [HW, ("raw", "".join(ic(K[i], 26 + i * 53, 72, 28, JUNGLE, 1.2) for i in range(4)), 60)]
    return [HW, ("raw", "".join(ic(K[i], 26 + i * 53, 72, 28, JUNGLE, 2.8) for i in range(4)), 60)]
pr(G, "Outline Or Solid Tiles?", ic_, ("ic_outline", "Outline Tiles", "Tinted icon boxes.", "calm", "line"), ("ic_solid", "Solid Color Tiles", "Bold blocks.", "visual", "solid"))
pr(G, "All Green Or Four Accents?", ic_, ("ic_green", "All Jungle Green", "One calm color.", "calm", "green"), ("ic_multi", "Four Accent Colors", "Each service its own.", "visual", "multi"))
pr(G, "Round Badges Or Bare Icons?", ic_, ("ic_round", "Round Tinted Badges", "Soft circles.", "calm", "round"), ("ic_bare", "Bare Ink Icons", "Minimal.", "focused", "bare"))
pr(G, "Thin Or Bold Lines?", ic_, ("ic_thin", "Thin Line Icons", "Light and airy.", "calm", "thin"), ("ic_bold", "Bold Line Icons", "Easy to see.", "visual", "bold"))

G = "Gift Card"
def gc(k):
    card = {"green": rect(24, 60, 192, 116, JUNGLE, "none", 12) + nest(60, 96, 16, "#FFFFFF") + t(30, 160, "WellNest Gift", 16, "#FFFFFF", "khand"),
            "white": rect(24, 60, 192, 116, "#FFFFFF", LINE, 12) + nest(60, 96, 16, JUNGLE) + t(30, 160, "WellNest Gift", 16, INK, "khand"),
            "photo": photo(24, 60, 192, 116, JUNGLE, "leaf", 12) + rect(24, 140, 192, 36, "#FFFFFFEE") + t(32, 163, "WellNest Gift", 14, INK, "khand"),
            "saffron": rect(24, 60, 192, 116, SAFFRON + "26", "none", 12) + t(120, 126, "A Day Of Rest", 18, INK, "khand", anchor="middle")}
    if k in card: return [HW, ("raw", card[k], 130), ("btn", "Send A Gift", "fill", INK)]
    if k == "service": return [HW, ("h", "Gift A Visit", 16), ("cards", S[:3], JUNGLE), ("btn", "Next", "fill", INK)]
    if k == "free": return [HW, ("h", "Gift Any Amount", 16), ("input", "Write A Note...", JUNGLE, "star"), ("btn", "Next", "fill", INK)]
    if k == "line": return [HW, ("h", "Send By", 14), ("cards", [("LINE Message", "", "", "ic:phone"), ("Email", "", "", "ic:card")], JUNGLE, "ic:phone")]
    return [HW, ("h", "Send By", 14), ("cards", [("Printed Card In A Box", "Pick up at WellNest", "", "ic:star")], SAFFRON, "ic:star")]
pr(G, "Green Card Or White Card?", gc, ("gc_green", "Solid Green Card", "Bold gift look.", "visual", "green"), ("gc_white", "White Card, Green Mark", "Quiet gift look.", "calm", "white"))
pr(G, "Photo Or Saffron Words?", gc, ("gc_photo", "Garden Photo Card", "Shows the place.", "visual", "photo"), ("gc_saffron", "Saffron Tint With Words", "A Day Of Rest.", "calm", "saffron"))
pr(G, "Pick A Service Or Any Amount?", gc, ("gc_service", "Gift A Set Service", "Massage, yoga, steam.", "focused", "service"), ("gc_any", "Gift Any Amount With Note", "Open gift.", "calm", "free"))
pr(G, "Digital Or Printed?", gc, ("gc_digital", "Send By LINE Or Email", "Instant.", "quick", "line"), ("gc_print", "Printed Card In A Box", "A keepsake.", "visual", "print"))

publish(DID, "WellNest Round 1: Logo Direction, Color Lead, Coming Soon Page, Service Cards, Booking Flow, Retreat Schedule, Waitlist Form, Instagram Grid, Guest Words, Location Card, Name Check Tracker, Welcome Email, Icon Style, Gift Card", "WellNest", pairs,
        {"brands": ["WellNest (Chiang Mai wellness business, not open yet), example data only", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"team_sync": "/workspace/ops/team-sync/2026-10-11.md", "feed": "/workspace/ops/team-feed.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md"}}, seed=34)
