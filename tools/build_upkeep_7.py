#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-7 (PUBLISHED): 25 new-ground pairs for the UpKeep agent (Smart UpKeep home maintenance
membership). upkeep-6 results are not in yet, so this deck avoids upkeep-6's areas and builds on the latest picks in
/workspace/smartkeep/branding/ (upkeep-5 picks: white base with thin-border cards, colored drawn icons, five-dot progress,
terracotta polo, lagoon bubbles, license-only trust). Topics from the Oct 13 team-sync recap: V.2 plan card and tech card,
label scan and warranty check, moisture scan, lawn mowing quote, home sale gift, yard sign with battery swap, van side,
tech headshot, watch page, extras card and add-on pop-up, certification badges, renewal and cancel notice, home record.
Rules: no byline, no AI / health score / tier names, only price 'Membership Starting at $99/Month', 'Your Licensed Tech'
with no named tech. Example data only. Pattern: tools/build_dashboard_2.py + draft_svg.py via team_kit.py."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "upkeep-7"; pairs, O, add = deck("uk7_", "UpKeep")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
PRICE = "Membership Starting at $99/Month"; LT = "Your Licensed Tech"
def roof(x, y, c=TERRA, s=1): return f'<path d="M{x} {y+10*s} L{x+11*s} {y} L{x+22*s} {y+10*s}" fill="none" stroke="{c}" stroke-width="{2.4*s}" stroke-linecap="round" stroke-linejoin="round"/>'
HU = ("raw", roof(14, 16) + t(42, 27, "Smart UpKeep", 13, INK, "khand") + shareic(208, 15) + ln(44), 50)
HB = ("raw", rect(0, 0, W, 50, SOFT) + roof(14, 16) + t(42, 27, "Smart UpKeep", 13, INK, "khand") + shareic(208, 15), 56)

G = "Plan Card"
def pc(k):
    if k == "big": return [HU, ("lbl", "Your Membership"), ("raw", rect(14, 74, 212, 46, TERRA + "14", "none", 8) + t(120, 102, PRICE, 11, TERRA, "khand", anchor="middle"), 54), ("checks", ["Seasonal visits", "Moisture scan", "Cancel Anytime"], JUNGLE, 3)]
    if k == "line": return [HU, ("lbl", "Your Membership"), ("h", PRICE, 15), ("checks", ["Seasonal visits", "Moisture scan", "Cancel Anytime"], JUNGLE, 3)]
    if k == "top": return [HU, ("banner", PRICE, TERRA, "tag"), ("cards", [("Seasonal Visits", "Four a year"), ("Moisture Scan", "Every visit")], None, "ic:home")]
    if k == "bottom": return [HU, ("cards", [("Seasonal Visits", "Four a year"), ("Moisture Scan", "Every visit")], None, "ic:home"), ("gap", 30), ("p", PRICE, 46, INK, True), ("btn", "Start", "fill", TERRA)]
    if k == "icons": return [HU, ("h", "What You Get", 16), ("tiles", [("Visits", "cal"), ("Moisture", "search"), ("Warranty", "check"), ("Reminders", "clock")], 2, 54), ("p", PRICE, 46, INK)]
    if k == "list": return [HU, ("h", "What You Get", 16), ("checks", ["Four seasonal visits", "Moisture scan", "Warranty check", "Reminders"], JUNGLE, 4), ("p", PRICE, 46, INK)]
    if k == "black": return [HU, ("h", "Smart UpKeep Membership", 14), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", INK)]
    return [HU, ("h", "Smart UpKeep Membership", 14), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", TERRA)]
pr(G, "Big Number Or One Line?", pc, ("pc_bignum", "Price In A Tinted Box", "The price line framed in soft terracotta.", "visual", "big"), ("pc_oneline", "Price As One Headline", "The full line, no big number.", "calm", "line"))
pr(G, "Price On Top Or At The Bottom?", pc, ("pc_top", "Price Banner Up Top", "See it first.", "focused", "top"), ("pc_bottom", "Price Above The Button", "Value first, price last.", "calm", "bottom"))
pr(G, "Icon Tiles Or Ticked List?", pc, ("pc_tiles", "Four Icon Tiles", "Colored drawn icons.", "visual", "icons"), ("pc_ticks", "Ticked List", "Four green ticks.", "focused", "list"))
pr(G, "Black Or Terracotta Button?", pc, ("pc_blackbtn", "Black Start Button", "Square, ink.", "focused", "black"), ("pc_terrabtn", "Terracotta Start Button", "Square, brand color.", "action", "terra"))

G = "Tech Card"
def tc(k):
    face = photo(24, 66, 56, 56, LAGOON, "person", 28)
    flat = f'<circle cx="52" cy="94" r="28" fill="{TERRA}22"/><circle cx="52" cy="86" r="10" fill="{TERRA}"/><path d="M34 116 Q52 96 70 116 Z" fill="{TERRA}"/>'
    base = lambda f: rect(14, 56, 212, 120, "#FFFFFF", LINE, 8) + f + t(92, 86, LT, 12, INK, "khand") + t(92, 98, "State Licensed · Insured", 7, MUTE)
    if k == "photo": return [HU, ("raw", base(face) + btn(140, "Verify License", "line", INK, 92, 120, 22, 7), 126)]
    if k == "flat": return [HU, ("raw", base(flat) + btn(140, "Verify License", "line", INK, 92, 120, 22, 7), 126)]
    if k == "tap": return [HU, ("raw", base(flat) + rect(92, 140, 120, 22, JUNGLE, "none", 11) + ic("check", 98, 143, 16, "#FFFFFF", 2) + t(160, 155, "TAP TO VERIFY", 6.5, "#FFFFFF", "hind", 700, "middle"), 126)]
    if k == "link": return [HU, ("raw", base(flat) + t(92, 150, "VERIFY ON THE STATE SITE", 6.5, TERRA, "hind", 600, extra='text-decoration="underline"'), 126)]
    if k == "visit": return [HU, ("lbl", "Next Visit · Thu 9 AM"), ("raw", base(flat).replace("56", "72", 1), 126)]
    if k == "alone": return [HU, ("raw", base(flat), 126)]
    if k == "polo": return [HU, ("raw", rect(14, 56, 212, 160, "#FFFFFF", LINE, 8) + f'<circle cx="120" cy="96" r="18" fill="{LAGOON}55"/><path d="M84 176 Q84 124 120 120 Q156 124 156 176 Z" fill="{TERRA}"/><path d="M112 122 L120 134 L128 122" fill="#FFFFFF"/>' + t(120, 200, LT, 12, INK, "khand", anchor="middle"), 166)]
    return [HU, ("raw", rect(14, 56, 212, 160, "#FFFFFF", LINE, 8) + f'<circle cx="120" cy="96" r="18" fill="{LAGOON}55"/><path d="M84 176 Q84 124 120 120 Q156 124 156 176 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.2"/><path d="M110 121 L120 134 L130 121" fill="none" stroke="{TERRA}" stroke-width="3"/>' + t(120, 200, LT, 12, INK, "khand", anchor="middle"), 166)]
pr(G, "Headshot Or Flat Drawing?", tc, ("tc_photo", "Round Headshot", "A real photo spot.", "visual", "photo"), ("tc_flat", "Flat Filled Drawing", "Your arrival-card pick, reused.", "calm", "flat"))
pr(G, "Green Tap Pill Or Underlined Link?", tc, ("tc_tappill", "Green Tap To Verify Pill", "Clear and quick.", "action", "tap"), ("tc_statelink", "Verify On The State Site Link", "Quiet text link.", "calm", "link"))
pr(G, "With Visit Time Or Card Alone?", tc, ("tc_withvisit", "Next Visit Above The Card", "Ties the tech to a time.", "focused", "visit"), ("tc_alone", "Card Alone", "Just who is coming.", "calm", "alone"))
pr(G, "Terracotta Polo Or White With Collar?", tc, ("tc_terrapolo", "Terracotta Polo", "Your door pick.", "visual", "polo"), ("tc_whitepolo", "White Polo, Terracotta Collar", "Lighter look.", "calm", "white"))

G = "Label Scan And Warranty Check"
def ls(k):
    if k == "frame": return [HU, ("dots", 5, 1, INK), ("h", "Scan The Label", 16), ("raw", rect(14, 96, 212, 130, "#2B2B2B", "none", 8) + rect(54, 126, 132, 70, "#FFFFFF22", "#FFFFFF", 4, 2), 138), ("btn", "Take Photo", "fill", INK)]
    if k == "auto": return [HU, ("dots", 5, 1, INK), ("h", "Scan The Label", 16), ("raw", rect(14, 96, 212, 130, "#2B2B2B", "none", 8) + rect(54, 126, 132, 70, "#FFFFFF22", JUNGLE, 4, 2) + t(120, 214, "HOLD STILL · READING", 7, "#FFFFFF", "hind", 600, "middle"), 138)]
    if k == "fields": return [HU, ("h", "We Read This", 16), ("table", [("Brand", "Example Brand"), ("Model", "EX-199"), ("Serial", "XX-000000"), ("Year", "2021")]), ("btn2", "Looks Right", "Fix It")]
    if k == "card": return [HU, ("h", "We Read This", 16), ("raw", rect(14, 86, 212, 70, "#FFFFFF", LINE, 8) + ic("home", 24, 100, 22, LAGOON, 2) + t(56, 108, "Water Heater", 11, INK, "khand") + t(56, 120, "Example Brand · EX-199 · 2021", 7, MUTE), 78), ("btn", "Looks Right", "fill", INK)]
    if k == "check": return [HU, ("raw", dot(120, 90, 24, JUNGLE + "22") + ic("check", 104, 74, 32, JUNGLE, 2), 80), ("h", "Warranty Checked", 18, INK, True), ("p", "Covered for parts. We'll remind you before it ends.", 40, MUTE, True)]
    if k == "bar": return [HU, ("h", "Warranty Checked", 16), ("bar", .6, JUNGLE, "Parts Coverage Left", "60%"), ("bar", .2, SAFFRON, "Labor Coverage Left", "20%")]
    if k == "list": return [HU, ("h", "Your Equipment", 16), ("cards", [("Water Heater", "Covered", "tag:Covered"), ("Furnace", "Ends soon", "tag:Ends Soon"), ("AC Unit", "Not checked", "tag:Scan")], None, "ic:home")]
    return [HU, ("h", "Your Equipment", 16), ("tiles", [("Water Heater", "home"), ("Furnace", "clock"), ("AC Unit", "star"), ("Add One", "search")], 2, 60)]
pr(G, "Frame Or Auto-Read?", ls, ("ls_frame", "White Frame, Tap To Snap", "You take the photo.", "focused", "frame"), ("ls_auto", "Green Frame Reads On Its Own", "Hold still, it reads.", "quick", "auto"))
pr(G, "Field Table Or Item Card?", ls, ("ls_fields", "Fields Read As A Table", "Brand, model, serial, year.", "focused", "fields"), ("ls_card", "One Item Card", "Icon, name, one line.", "calm", "card"))
pr(G, "Big Check Or Coverage Bars?", ls, ("ls_bigcheck", "Big Warranty Checked", "Green check and one line.", "calm", "check"), ("ls_bars", "Coverage Left Bars", "Parts and labor bars.", "visual", "bar"))
pr(G, "Status Rows Or Equipment Tiles?", ls, ("ls_rows", "Equipment Rows With Tags", "Covered, Ends Soon, Scan.", "focused", "list"), ("ls_tiles", "Equipment Tiles", "Tap to scan more.", "visual", "tiles"))

G = "Moisture Scan Report"
def ms(k):
    if k == "plan": return [HU, ("h", "Moisture Scan", 16), ("raw", rect(14, 80, 212, 130, SOFT, "none", 6) + rect(28, 94, 90, 54, "#FFFFFF", LINE) + rect(124, 94, 88, 102, "#FFFFFF", LINE) + rect(28, 154, 90, 42, "#FFFFFF", LINE) + f'<circle cx="168" cy="176" r="12" fill="{LAGOON}55"/>' + dot(168, 176, 3, LAGOON), 138), ("p", "One damp spot under the bath sink.")]
    if k == "rooms": return [HU, ("h", "Moisture Scan", 16), ("cards", [("Kitchen", "Dry", "tag:Dry"), ("Bath", "Damp spot", "tag:Watch"), ("Basement", "Dry", "tag:Dry")], None, "dot", "line", 30)]
    if k == "photo": return [HU, ("lbl", "Bath · Under The Sink"), ("raw", photo(14, 72, 212, 120, LAGOON, "room") + f'<circle cx="150" cy="150" r="22" fill="{LAGOON}44" stroke="{LAGOON}" stroke-dasharray="3 2"/>', 128), ("p", "Damp, not wet. We'll check again next visit.")]
    if k == "words": return [HU, ("lbl", "Bath · Under The Sink"), ("h", "Damp, Not Wet", 20), ("p", "We'll check again next visit. No action needed now.")]
    if k == "gauge": return [HU, ("lbl", "Bath · Reading"), ("raw", rect(14, 76, 212, 12, "#EEEAE4", "none", 6) + rect(14, 76, 70, 12, JUNGLE, "none", 6) + rect(84, 76, 70, 12, SAFFRON, "none", 0) + rect(154, 76, 72, 12, TERRA, "none", 6) + f'<path d="M110 70 L116 62 H104 Z" fill="{INK}"/>' + t(14, 102, "Dry", 7, MUTE) + t(120, 102, "Damp", 7, MUTE, anchor="middle") + t(226, 102, "Wet", 7, MUTE, anchor="end"), 40)]
    if k == "word": return [HU, ("lbl", "Bath · Reading"), ("word", "Damp", 36, SAFFRON, "Check Again Next Visit")]
    if k == "next": return [HU, ("cards", [("Bath Damp Spot", "Next visit: recheck", "tag:Watch")], SAFFRON, "dot", "tint", 44), ("btn", "Ask A Question", "line", INK)]
    return [HU, ("cards", [("Bath Damp Spot", "Next visit: recheck", "tag:Watch")], SAFFRON), ("btn", "Book A Fix Now", "fill", TERRA)]
pr(G, "Floor Plan Or Room Rows?", ms, ("ms_plan", "Spot On A Floor Plan", "See where it is.", "visual", "plan"), ("ms_rooms", "Room Rows With Tags", "Dry or Watch per room.", "focused", "rooms"))
pr(G, "Photo Circle Or Plain Words?", ms, ("ms_photo", "Photo With Circled Spot", "Shows the place.", "visual", "photo"), ("ms_words", "Damp, Not Wet In Words", "Calm headline.", "calm", "words"))
pr(G, "Gauge Or One Word?", ms, ("ms_gauge", "Dry To Wet Gauge", "Pointer on a bar.", "visual", "gauge"), ("ms_word", "One Saffron Word", "Damp, big.", "quick", "word"))
pr(G, "Ask Or Book A Fix?", ms, ("ms_ask", "Ask A Question Button", "Low pressure.", "calm", "next"), ("ms_fix", "Book A Fix Button", "Act now.", "action", "fix"))

G = "Lawn Mowing Quote"
def lm(k):
    if k == "weekly": return [HU, ("h", "Lawn Mowing", 16), ("cards", [("Weekly", "Every week, spring to fall", "tag:Pick")], JUNGLE, "ic:cal"), ("btn", "Get My Quote", "fill", INK)]
    if k == "both": return [HU, ("h", "Lawn Mowing", 16), ("cards", [("Weekly", "Every week"), ("Every Other Week", "Twice a month")], JUNGLE, "ic:cal"), ("btn", "Get My Quote", "fill", INK)]
    if k == "map": return [HU, ("h", "Your Lawn", 16), ("raw", rect(14, 80, 212, 120, JUNGLE + "1A", "none", 6) + f'<path d="M40 100 L200 96 L206 180 L36 184 Z" fill="{JUNGLE}44" stroke="{JUNGLE}" stroke-width="1.5" stroke-dasharray="4 3"/>' + rect(96, 120, 50, 36, "#FFFFFF", INK), 128), ("p", "Trace your lawn on the map.")]
    if k == "size": return [HU, ("h", "Your Lawn", 16), ("cards", [("Small", "Townhouse yard"), ("Medium", "Most homes"), ("Large", "Big lot")], JUNGLE, "num")]
    if k == "cal": return [HU, ("lbl", "Mowing Days"), ("cal", (2, 9, 16, 23), JUNGLE)]
    if k == "next": return [HU, ("lbl", "Next Mow"), ("word", "Thu", 40, JUNGLE, "Weather Permitting")]
    if k == "addon": return [HU, ("h", "Add Lawn Mowing?", 16), ("p", "Same membership, one more service."), ("btn2", "Add It", "Not Now")]
    return [HU, ("h", "Lawn Mowing", 16), ("p", "Its own page, separate from your membership."), ("btn", "Get My Quote", "fill", INK)]
pr(G, "Weekly Only Or Two Choices?", lm, ("lm_weekly", "Weekly Only", "One simple plan.", "quick", "weekly"), ("lm_both", "Weekly Or Every Other Week", "Two choices.", "focused", "both"))
pr(G, "Trace On Map Or Pick A Size?", lm, ("lm_trace", "Trace Lawn On A Map", "Exact area.", "visual", "map"), ("lm_size", "Small, Medium, Large", "Fast pick.", "quick", "size"))
pr(G, "Calendar Or Next Mow?", lm, ("lm_cal", "Mowing Days Calendar", "See the month.", "visual", "cal"), ("lm_next", "Next Mow Day, Big", "Just what's next.", "calm", "next"))
pr(G, "Add-On Or Own Page?", lm, ("lm_addon", "Add To Membership", "Two buttons.", "action", "addon"), ("lm_own", "Its Own Quote Page", "Kept separate.", "focused", "own"))

G = "Home Sale Gift"
def hs(k):
    if k == "card": return [HU, ("raw", rect(24, 60, 192, 110, TERRA, "none", 10) + roof(36, 76, "#FFFFFF") + t(36, 130, "3 Months Free", 20, "#FFFFFF", "khand") + t(36, 146, "For The Buyer Of Your Home", 8, "#FFFFFFCC"), 118), ("btn", "Send The Gift", "fill", INK)]
    if k == "plain": return [HU, ("h", "Selling Your Home?", 18), ("p", "Gift the buyer 3 months free. We'll hand over your home's record too."), ("btn", "Send The Gift", "fill", INK)]
    if k == "steps": return [HU, ("h", "Gift The Buyer", 16), ("steps", ["Tell Us", "We Email", "They Join"], TERRA, 0), ("btn", "Start", "fill", INK)]
    if k == "form": return [HU, ("h", "Gift The Buyer", 16), ("input", "Buyer's Email", TERRA, "star"), ("input", "Closing Date", TERRA, "cal"), ("btn", "Send", "fill", INK)]
    if k == "agent": return [HU, ("h", "Gift The Buyer", 16), ("cards", [("Send To My Agent", "They pass it on", "", "ic:phone")], LAGOON, "ic:phone")]
    if k == "direct": return [HU, ("h", "Gift The Buyer", 16), ("cards", [("Send To The Buyer", "Straight to them", "", "ic:card")], LAGOON, "ic:card")]
    if k == "sign": return [("raw", rect(0, 0, W, H, SOFT) + photo(40, 40, 160, 150, LAGOON, "house") + rect(150, 150, 60, 40, "#FFFFFF", INK) + t(180, 166, "SOLD", 9, INK, "khand", anchor="middle") + t(180, 180, "3 Mo Free", 6.5, TERRA, "hind", 600, "middle"), 0)]
    return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 30), ("h", "A Gift With Your New Home", 14, INK, True), ("p", "The seller gave you 3 months of Smart UpKeep.", 38, MUTE, True), ("btn", "Claim My Gift", "fill", TERRA)]
pr(G, "Gift Card Or Plain Ask?", hs, ("hs_card", "Terracotta Gift Card", "3 Months Free, big.", "visual", "card"), ("hs_plain", "Selling Your Home? Headline", "Words, then button.", "calm", "plain"))
pr(G, "Three Steps Or Short Form?", hs, ("hs_steps", "Three Steps", "Tell Us, We Email, They Join.", "focused", "steps"), ("hs_form", "Buyer Email And Date", "Done in one screen.", "quick", "form"))
pr(G, "Through The Agent Or Direct?", hs, ("hs_agent", "Send Through Your Agent", "Agent passes it on.", "calm", "agent"), ("hs_direct", "Send To The Buyer", "Straight to them.", "action", "direct"))
pr(G, "Sign Rider Or Buyer Email?", hs, ("hs_rider", "Sold Sign Rider", "3 Mo Free on the sign.", "visual", "sign"), ("hs_buyermail", "Buyer Welcome Email", "Claim My Gift.", "focused", "email"))

G = "Yard Sign And Battery Swap"
def ys(k):
    if k == "reward": return [HU, ("h", "Put A Sign In Your Yard?", 15), ("cards", [("Free Battery Swap", "Smoke detectors, next visit", "", "ic:check")], JUNGLE, "ic:check", "tint", 44), ("btn2", "Yes, Add Sign", "No Thanks")]
    if k == "draw": return [HU, ("raw", f'<line x1="100" y1="90" x2="100" y2="200" stroke="{INK}" stroke-width="2"/><line x1="140" y1="90" x2="140" y2="200" stroke="{INK}" stroke-width="2"/>' + rect(80, 70, 80, 60, "#FFFFFF", INK, 2, 1.5) + roof(108, 80, TERRA, .8) + t(120, 116, "Smart UpKeep", 8, INK, "khand", anchor="middle"), 150), ("p", "Sign up for a free battery swap.", 46, MUTE, True)]
    if k == "small": return [HU, ("cards", [("Yard Sign", "Free battery swap if yes", "tag:Opt In")], TERRA)]
    if k == "mail": return [HU, ("bubble", "Want a yard sign? You'll get a free smoke detector battery swap.", False), ("bubble", "Yes", True)]
    if k == "white": return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, "#FFFFFF", INK, 2, 1.5) + roof(108, 76, TERRA) + t(120, 120, "Smart UpKeep", 14, INK, "khand", anchor="middle") + t(120, 138, "Member Home", 7, MUTE, "hind", 600, "middle") + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]
    return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, TERRA, "none", 2) + roof(108, 76, "#FFFFFF") + t(120, 120, "Smart UpKeep", 14, "#FFFFFF", "khand", anchor="middle") + t(120, 138, "Member Home", 7, "#FFFFFFCC", "hind", 600, "middle") + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]
pr(G, "Reward Card Or Sign Drawing?", ys, ("ys_reward", "Battery Swap Reward Card", "Lead with the reward.", "action", "reward"), ("ys_drawing", "Drawing Of The Sign", "Lead with the sign.", "visual", "draw"))
pr(G, "Opt-In Row Or Chat Ask?", ys, ("ys_row", "Opt-In Row In Settings", "Quiet tag.", "calm", "small"), ("ys_chat", "Ask In Chat Bubbles", "Lagoon reply bubble.", "action", "mail"))
pr(G, "White Sign Or Terracotta Sign?", ys, ("ys_whitesign", "White Sign, Ink Words", "Clean on any lawn.", "calm", "white"), ("ys_terrasign", "Terracotta Sign, White Words", "Stands out.", "visual", "terra"))

G = "Van Side"
def vn(k):
    v = lambda body: rect(0, 0, W, H, SOFT) + f'<path d="M14 200 V120 Q14 100 34 100 H170 Q200 100 214 130 L226 150 V200 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.5"/>' + f'<circle cx="60" cy="204" r="14" fill="{INK}"/><circle cx="180" cy="204" r="14" fill="{INK}"/>' + body
    if k == "big": return [("raw", v(roof(30, 120, TERRA, 1.4) + t(66, 140, "Smart UpKeep", 20, INK, "khand") + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "small": return [("raw", v(roof(30, 130, TERRA, .8) + t(52, 140, "Smart UpKeep", 11, INK, "khand") + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "url": return [("raw", v(t(30, 140, "Smart UpKeep", 18, INK, "khand") + t(30, 156, "SMARTUPKEEP.EXAMPLE", 7, MUTE, "hind", 600, extra='letter-spacing="1"') + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "line": return [("raw", v(t(30, 140, "Smart UpKeep", 18, INK, "khand") + t(30, 156, "Home Maintenance Membership", 7.5, MUTE) + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "rear": return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 160, "#FFFFFF", INK, 8, 1.5) + f'<line x1="120" y1="60" x2="120" y2="220" stroke="{INK}"/>' + roof(66, 110, TERRA) + t(66, 140, "Smart", 14, INK, "khand") + t(126, 140, "UpKeep", 14, INK, "khand") + rect(50, 190, 140, 6, TERRA), 0)]
    return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 160, "#FFFFFF", INK, 8, 1.5) + f'<line x1="120" y1="60" x2="120" y2="220" stroke="{INK}"/>' + t(120, 200, "HOW'S MY SERVICE?", 7, MUTE, "hind", 600, "middle") + rect(50, 190, 140, 3, TERRA), 0)]
pr(G, "Big Or Small Name On The Side?", vn, ("vn_bigname", "Big Name And Roof Mark", "Readable from the street.", "visual", "big"), ("vn_smallname", "Small Name, More White", "Quiet and clean.", "calm", "small"))
pr(G, "Web Address Or Tagline?", vn, ("vn_url", "Web Address Under The Name", "Easy to look up.", "action", "url"), ("vn_tagline", "Tagline Under The Name", "Says what it is.", "focused", "line"))
pr(G, "Name Across Rear Doors Or Service Question?", vn, ("vn_rearname", "Name Across Rear Doors", "Brand from behind.", "visual", "rear"), ("vn_rearask", "How's My Service Line", "Small ask, thin stripe.", "calm", "ask"))

G = "Tech Headshot Standard"
def th(k):
    bg = {"white": "#FFFFFF", "soft": SOFT, "lagoon": LAGOON + "22", "outdoor": None}
    if k in ("white", "soft", "lagoon"): return [("raw", rect(50, 50, 140, 170, bg[k], LINE, 8) + f'<circle cx="120" cy="114" r="28" fill="{INK}33"/><path d="M70 220 Q70 154 120 150 Q170 154 170 220 Z" fill="{TERRA}"/><path d="M110 152 L120 166 L130 152" fill="#FFFFFF"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
    if k == "outdoor": return [("raw", photo(50, 50, 140, 170, JUNGLE, "sun", 8) + f'<circle cx="120" cy="114" r="28" fill="{INK}33"/><path d="M70 220 Q70 154 120 150 Q170 154 170 220 Z" fill="{TERRA}"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
    if k == "close": return [("raw", rect(50, 50, 140, 170, SOFT, LINE, 8) + f'<circle cx="120" cy="120" r="44" fill="{INK}33"/><path d="M60 220 Q60 180 120 172 Q180 180 190 220 Z" fill="{TERRA}"/>' + t(120, 244, "Close Crop", 9, MUTE, "hind", 600, "middle"), 0)]
    return [("raw", rect(50, 50, 140, 170, SOFT, LINE, 8) + f'<circle cx="120" cy="100" r="18" fill="{INK}33"/><path d="M90 200 Q90 124 120 122 Q150 124 150 200 Z" fill="{TERRA}"/>' + rect(96, 196, 48, 24, INK + "55") + t(120, 244, "Waist Up, With Tool Bag", 9, MUTE, "hind", 600, "middle"), 0)]
pr(G, "White Or Soft Background?", th, ("th_whitebg", "Pure White Background", "Clean cutout look.", "calm", "white"), ("th_softbg", "Soft Warm Gray Background", "Matches the app band.", "calm", "soft"))
pr(G, "Lagoon Wash Or Outdoors?", th, ("th_lagoonbg", "Light Lagoon Wash", "Brand-tinted backdrop.", "visual", "lagoon"), ("th_outdoor", "Outdoors, Soft Focus", "Real-world setting.", "visual", "outdoor"))
pr(G, "Close Crop Or Waist Up?", th, ("th_close", "Close Crop", "Face fills the frame.", "focused", "close"), ("th_waist", "Waist Up With Tool Bag", "Shows the work.", "action", "waist"))

G = "Watch Page"
def wp(k):
    v = lambda y, h: rect(14, y, 212, h, "#2B2B2B", "none", 8) + f'<circle cx="120" cy="{y+h/2}" r="18" fill="#FFFFFF"/><path d="M114 {y+h/2-9} L128 {y+h/2} L114 {y+h/2+9} Z" fill="{INK}"/>'
    if k == "tall": return [HU, ("raw", rect(60, 56, 120, 200, "#2B2B2B", "none", 10) + f'<circle cx="120" cy="156" r="18" fill="#FFFFFF"/><path d="M114 147 L128 156 L114 165 Z" fill="{INK}"/>', 206), ("btn", "Share", "line", INK)]
    if k == "wide": return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("btn", "Share", "line", INK)]
    if k == "cta": return [HU, ("raw", v(60, 120), 128), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", TERRA)]
    if k == "share": return [HU, ("raw", v(60, 120), 128), ("btn2", "Share", "Copy Link")]
    if k == "chapters": return [HU, ("raw", v(56, 100), 108), ("cards", [("The Visit", "0:00"), ("The Scan", "0:15"), ("Cancel Anytime", "0:38")], None, "ic:play", "line", 28)]
    return [HU, ("raw", v(56, 100), 108), ("p", "45 seconds. See a visit, a scan and how to cancel.")]
pr(G, "Tall Or Wide Player?", wp, ("wp_tall", "Tall Phone Player", "9:16 fills the phone.", "visual", "tall"), ("wp_wide", "Wide Player With Title", "16:9 with a headline.", "focused", "wide"))
pr(G, "Start Button Or Share Only?", wp, ("wp_cta", "Price Line And Start Button", "Turn viewers into members.", "action", "cta"), ("wp_shareonly", "Share And Copy Link Only", "Made for passing on.", "calm", "share"))
pr(G, "Chapters Or One Line?", wp, ("wp_chapters", "Chapter Rows Under Video", "Jump to a part.", "focused", "chapters"), ("wp_oneline", "One Line Summary", "Just press play.", "calm", "line"))

G = "Extras And Add-On Pop-Up"
def ex(k):
    if k == "card": return [HU, ("cards", [("Learn About Extras", "Gutters, dryer vent, more", "", "ic:star")], LAGOON, "ic:star", "line", 50)]
    if k == "chips": return [HU, ("lbl", "Extras"), ("tags", ["Gutters", "Dryer Vent", "Window Wash", "Pressure Wash"])]
    if k == "sheet": return [HU, ("cards", [("Seasonal Visits", "")]), ("raw", rect(0, 150, W, 150, "#FFFFFF", "none", 14) + rect(0, 0, W, 150, "#0A0A0A33") + rect(104, 158, 32, 4, "#D6D0C6", "none", 2) + t(14, 184, "Add Gutter Cleaning?", 13, INK, "khand") + t(14, 196, "Before your first visit.", 7.5, MUTE) + btn(212, "Add It", "fill", INK, 14, 103, 26, 8) + btn(212, "No Thanks", "line", INK, 123, 103, 26, 8), 0)]
    if k == "modal": return [HU, ("raw", rect(0, 0, W, H, "#0A0A0A33") + rect(24, 80, 192, 140, "#FFFFFF", "none", 10) + ic("star", 108, 96, 24, SAFFRON, 2) + t(120, 140, "Add Gutter Cleaning?", 12, INK, "khand", anchor="middle") + btn(160, "Add It", "fill", INK, 40, 160, 22, 7.5) + t(120, 204, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"'), 0)]
    if k == "photo": return [("raw", rect(0, 0, W, H, "#0A0A0A33") + rect(24, 50, 192, 200, "#FFFFFF", "none", 10) + photo(34, 60, 172, 80, LAGOON, "house") + t(120, 164, "Add Gutter Cleaning?", 12, INK, "khand", anchor="middle") + btn(184, "Add It", "fill", INK, 40, 160, 22, 7.5) + t(120, 228, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"'), 0)]
    if k == "text": return [("raw", rect(0, 0, W, H, "#0A0A0A33") + rect(24, 80, 192, 130, "#FFFFFF", "none", 10) + t(120, 120, "Add Gutter Cleaning?", 12, INK, "khand", anchor="middle") + t(120, 134, "Done on your first visit.", 7.5, MUTE, anchor="middle") + btn(150, "Add It", "fill", INK, 40, 160, 22, 7.5) + t(120, 194, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"'), 0)]
    if k == "nolink": return [("raw", rect(0, 0, W, H, "#0A0A0A33") + rect(24, 80, 192, 130, "#FFFFFF", "none", 10) + t(120, 120, "Add Gutter Cleaning?", 12, INK, "khand", anchor="middle") + btn(150, "Add It", "fill", INK, 40, 76, 22, 7) + btn(150, "Skip", "line", INK, 124, 76, 22, 7), 0)]
    return [("raw", rect(0, 0, W, H, "#0A0A0A33") + rect(24, 80, 192, 130, "#FFFFFF", "none", 10) + t(120, 120, "Add Gutter Cleaning?", 12, INK, "khand", anchor="middle") + btn(150, "Add It", "fill", INK, 40, 160, 22, 7.5) + t(120, 194, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"') + ic("x", 196, 88, 14, MUTE), 0)]
pr(G, "Extras Card Or Chips?", ex, ("ex_card", "Learn About Extras Card", "One card, tap to see.", "calm", "card"), ("ex_chips", "Extras As Chips", "See them all at once.", "visual", "chips"))
pr(G, "Bottom Sheet Or Center Pop-Up?", ex, ("ex_sheet", "Bottom Sheet Add-On", "Slides up.", "calm", "sheet"), ("ex_modal", "Center Pop-Up With Icon", "Saffron star on top.", "visual", "modal"))
pr(G, "Photo Or Words Only?", ex, ("ex_photo", "Pop-Up With A Photo", "Shows the job.", "visual", "photo"), ("ex_words", "Words Only Pop-Up", "Short and calm.", "calm", "text"))
pr(G, "Skip Button Or Close X?", ex, ("ex_skipbtn", "Two Equal Buttons", "Add It or Skip.", "focused", "nolink"), ("ex_closex", "No Thanks Link And Close X", "Two ways out.", "calm", "x"))

G = "Certification Badges"
def cb(k):
    B = [("Licensed", "check"), ("Insured", "star"), ("Background Checked", "search"), ("Trained", "clock")]
    if k == "shield": return [HU, ("h", "Your Licensed Tech", 15), ("raw", "".join(f'<path d="M{34+i*50} 90 L{54+i*50} 82 L{74+i*50} 90 V108 Q{54+i*50} 126 {34+i*50} 108 Z" fill="{ACC[i]}1F" stroke="{ACC[i]}" stroke-width="1.5"/>' + ic(k2, 46 + i * 50, 92, 16, ACC[i], 2) + t(54 + i * 50, 140, n.split()[0], 6.8, INK, "hind", 600, "middle") for i, (n, k2) in enumerate(B)), 90)]
    if k == "rows": return [HU, ("h", "Your Licensed Tech", 15), ("cards", [(n, "Verified", "") for n, _ in B], JUNGLE, "ic:check", "line", 30)]
    if k == "one": return [HU, ("h", "Your Licensed Tech", 15), ("tags", ["Licensed", "Insured", "Background Checked", "Trained"], True)]
    if k == "ink": return [HU, ("h", "Your Licensed Tech", 15), ("tags", ["Licensed", "Insured", "Background Checked", "Trained"])]
    if k == "date": return [HU, ("cards", [("Background Checked", "Rechecked yearly · Example date", "tag:Current")], JUNGLE)]
    return [HU, ("cards", [("Background Checked", "", "tag:Current")], JUNGLE)]
pr(G, "Shields Or Check Rows?", cb, ("cb_shields", "Four Shield Badges", "Your trust-tile pick, as shields.", "visual", "shield"), ("cb_rows", "Verified Rows", "Green check per item.", "focused", "rows"))
pr(G, "Solid Or Soft Chips?", cb, ("cb_solidchips", "Solid Color Chips", "Bold row of badges.", "visual", "one"), ("cb_softchips", "Soft Tint Chips", "Lighter row.", "calm", "ink"))
pr(G, "Show Recheck Date Or Not?", cb, ("cb_recheck", "Show The Yearly Recheck", "With a date line.", "focused", "date"), ("cb_norecheck", "Just Current Tag", "No date.", "quick", "nodate"))

G = "Renewal And Cancel Notice"
def rn(k):
    if k == "three": return [HU, ("banner", "Renews In 3 Days", SAFFRON, "clock"), ("p", "Nothing to do if you're staying. Cancel Anytime in Settings.")]
    if k == "seven": return [HU, ("banner", "Renews In 7 Days", SAFFRON, "clock"), ("p", "Nothing to do if you're staying. Cancel Anytime in Settings.")]
    if k == "email": return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 30), ("h", "Your Membership Renews Soon", 13, INK, True), ("p", "Here's what you got this year:", 38, MUTE, True), ("stats", [("4", "Visits"), ("1", "Scan Flag"), ("3", "Warranties")], "tint")]
    if k == "text": return [("raw", rect(0, 0, W, H, SOFT), 0), ("gap", 40), ("bubble", "Smart UpKeep: your membership renews in 3 days. Reply STOP to cancel, or do nothing to stay.")]
    if k == "cancel1": return [HU, ("h", "Cancel Membership", 15), ("p", "Cancel Anytime. Your visits stay booked until the end of this month."), ("btn", "Cancel", "line", TERRA)]
    if k == "cancel2": return [HU, ("h", "Before You Go", 15), ("cards", [("Pause Instead", "Up to 3 months"), ("Cancel", "Ends this month")], None, "dot")]
    if k == "settings": return [HU, ("lbl", "Settings"), ("cards", [("Membership", "Renews monthly"), ("Payment", "Card on file"), ("Cancel Anytime", "")], None, "dot", "line", 30)]
    return [HU, ("lbl", "Membership"), ("cards", [("Renews monthly", ""), ("Cancel Anytime", "One tap", "CANCEL")], TERRA)]
pr(G, "3 Days Or 7 Days Notice?", rn, ("rn_3day", "Notice 3 Days Before", "Your research pick.", "calm", "three"), ("rn_7day", "Notice 7 Days Before", "More time to decide.", "calm", "seven"))
pr(G, "Year Recap Email Or Short Text?", rn, ("rn_recap", "Year Recap Email", "What you got this year.", "visual", "email"), ("rn_text", "Short Text Reminder", "Reply STOP to cancel.", "quick", "text"))
pr(G, "Straight Cancel Or Offer Pause?", rn, ("rn_straight", "Straight Cancel Button", "No detours.", "calm", "cancel1"), ("rn_pause", "Offer A Pause First", "Pause or cancel.", "focused", "cancel2"))
pr(G, "In Settings List Or On Membership Card?", rn, ("rn_inlist", "Cancel Row In Settings", "One row among others.", "calm", "settings"), ("rn_oncard", "Cancel Cue On Membership", "Right next to renewal.", "action", "card"))

G = "Home Record Handoff"
def hr(k):
    if k == "book": return [HU, ("raw", rect(60, 60, 120, 150, "#FFFFFF", INK, 4, 1.5) + rect(60, 60, 12, 150, TERRA) + roof(96, 90, TERRA) + t(126, 130, "Home Record", 13, INK, "khand", anchor="middle") + t(126, 144, "Example Address", 7, MUTE, anchor="middle"), 160), ("btn", "Hand It Over", "fill", INK)]
    if k == "list": return [HU, ("h", "Home Record", 16), ("cards", [("Equipment", "6 items"), ("Visits", "8 logged"), ("Scans", "4 readings"), ("Warranties", "3 checked")], None, "ic:home", "line", 30)]
    if k == "link": return [HU, ("h", "Hand Over The Record", 15), ("cards", [("Share A Link", "Buyer opens it on any phone", "", "ic:tag")], LAGOON, "ic:tag")]
    if k == "pdf": return [HU, ("h", "Hand Over The Record", 15), ("cards", [("Download PDF", "Print for closing day", "", "ic:card")], LAGOON, "ic:card")]
    if k == "time": return [HU, ("h", "Home Record", 16), ("timeline", [("Oct 2026", "Fall visit, moisture scan"), ("Jul 2026", "Summer visit"), ("Apr 2026", "Spring visit, warranty check")])]
    return [HU, ("h", "Home Record", 16), ("stats", [("8", "Visits"), ("6", "Items"), ("4", "Scans")], "tint")]
pr(G, "Book Cover Or Section List?", hr, ("hr_book", "Drawn Record Book", "Feels like a keepsake.", "visual", "book"), ("hr_sections", "Section List", "Equipment, visits, scans.", "focused", "list"))
pr(G, "Share Link Or PDF?", hr, ("hr_sharelink", "Share A Link", "Opens on any phone.", "quick", "link"), ("hr_pdf", "Download A PDF", "Print for closing.", "calm", "pdf"))
pr(G, "Timeline Or Counts?", hr, ("hr_timeline", "Visit Timeline", "Season by season.", "focused", "time"), ("hr_counts", "Three Counts", "Visits, items, scans.", "visual", "stats"))

# rule check before publishing
blob = json.dumps(pairs, ensure_ascii=False)
txt = re.sub(r"<[^>]+>", " ", blob)
for bad in [r"\bAI\b", r"Health Score", r"\bSilver\b", r"\bGold\b", r"\bPlatinum\b", r"\bEssentials\b", r"\bPlus\b", r"\bComplete\b", r"\bPremium\b", r"\bBasic\b", r"Built", r"By Max", r"Weberman", r"\bTier"]:
    assert not re.search(bad, txt, re.I if bad in ("Built", "By Max", "Weberman") else 0), bad
assert txt.count("$") == txt.count(PRICE), (txt.count("$"), txt.count(PRICE))
publish(DID, "UpKeep Round 7: Plan Card, Tech Card And License Check, Label Scan And Warranty Check, Moisture Scan Report, Lawn Mowing Quote, Home Sale Gift, Yard Sign And Battery Swap, Van Side, Tech Headshot, Watch Page, Extras And Add-On Pop-Up, Certification Badges, Renewal And Cancel Notice, Home Record Handoff", "UpKeep", pairs,
        {"brands": ["Smart UpKeep home maintenance membership; new ground while upkeep-6 results are pending; builds on upkeep-5 picks", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017; only price 'Membership Starting at $99/Month'; 'Your Licensed Tech', no named tech; no byline"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"}, "based_on": "upkeep-6 (avoided its areas) + upkeep-5 picks",
         "sources": {"picks": "/workspace/smartkeep/branding/upkeep-5-picks.md", "brand_notes": "/workspace/smartkeep/branding/upkeep-brand-notes.md", "prior_deck": "decks/upkeep-6.json", "team_sync": "/workspace/ops/team-sync/2026-10-13.md"}}, seed=37)
