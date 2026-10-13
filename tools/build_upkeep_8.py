#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-8 (PUBLISHED): 50 pairs for the UpKeep agent built from Max's upkeep-7 picks (35/50,
/workspace/smartkeep/branding/upkeep-7-picks.md). Refines the winners, retests every 'both' tie head to head, adds a drawn
gift graphic (pair 18 note), a one-time lawn option (pair 13 note) and retention-offer cards (pair 26 note: one month free
to stay after 6+ months, two months free after 1+ year). Certification Badges dropped (skipped en masse).
Rules: no byline, no AI / health score / forecast / tier names, only price 'Membership Starting at $99/Month',
'Your Licensed Tech' with no named tech or license numbers. Example data only. Pattern: build_upkeep_7.py + team_kit.py + draft_svg.py.
Renderers below are copied from build_upkeep_7.py so upkeep-8 screens match round 7."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "upkeep-8"; pairs, O, add = deck("uk8_", "UpKeep")
def pr(G, ask, fn, a, b, purpose="refine"):
    add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask, purpose)
    if purpose == "retest": pairs[-1]["retest"] = True
PRICE = "Membership Starting at $99/Month"; LT = "Your Licensed Tech"
def roof(x, y, c=TERRA, s=1): return f'<path d="M{x} {y+10*s} L{x+11*s} {y} L{x+22*s} {y+10*s}" fill="none" stroke="{c}" stroke-width="{2.4*s}" stroke-linecap="round" stroke-linejoin="round"/>'
HU = ("raw", roof(14, 16) + t(42, 27, "Smart UpKeep", 13, INK, "khand") + shareic(208, 15) + ln(44), 50)
HB = ("raw", rect(0, 0, W, 50, SOFT) + roof(14, 16) + t(42, 27, "Smart UpKeep", 13, INK, "khand") + shareic(208, 15), 56)

# ---- round 7 renderers (copied) ----
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

G = "Yard Sign And Battery Swap"
def ys(k):
    if k == "reward": return [HU, ("h", "Put A Sign In Your Yard?", 15), ("cards", [("Free Battery Swap", "Smoke detectors, next visit", "", "ic:check")], JUNGLE, "ic:check", "tint", 44), ("btn2", "Yes, Add Sign", "No Thanks")]
    if k == "draw": return [HU, ("raw", f'<line x1="100" y1="90" x2="100" y2="200" stroke="{INK}" stroke-width="2"/><line x1="140" y1="90" x2="140" y2="200" stroke="{INK}" stroke-width="2"/>' + rect(80, 70, 80, 60, "#FFFFFF", INK, 2, 1.5) + roof(108, 80, TERRA, .8) + t(120, 116, "Smart UpKeep", 8, INK, "khand", anchor="middle"), 150), ("p", "Sign up for a free battery swap.", 46, MUTE, True)]
    if k == "small": return [HU, ("cards", [("Yard Sign", "Free battery swap if yes", "tag:Opt In")], TERRA)]
    if k == "mail": return [HU, ("bubble", "Want a yard sign? You'll get a free smoke detector battery swap.", False), ("bubble", "Yes", True)]
    if k == "white": return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, "#FFFFFF", INK, 2, 1.5) + roof(108, 76, TERRA) + t(120, 120, "Smart UpKeep", 14, INK, "khand", anchor="middle") + t(120, 138, "Member Home", 7, MUTE, "hind", 600, "middle") + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]
    return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, TERRA, "none", 2) + roof(108, 76, "#FFFFFF") + t(120, 120, "Smart UpKeep", 14, "#FFFFFF", "khand", anchor="middle") + t(120, 138, "Member Home", 7, "#FFFFFFCC", "hind", 600, "middle") + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]

G = "Van Side"
def vn(k):
    v = lambda body: rect(0, 0, W, H, SOFT) + f'<path d="M14 200 V120 Q14 100 34 100 H170 Q200 100 214 130 L226 150 V200 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.5"/>' + f'<circle cx="60" cy="204" r="14" fill="{INK}"/><circle cx="180" cy="204" r="14" fill="{INK}"/>' + body
    if k == "big": return [("raw", v(roof(30, 120, TERRA, 1.4) + t(66, 140, "Smart UpKeep", 20, INK, "khand") + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "small": return [("raw", v(roof(30, 130, TERRA, .8) + t(52, 140, "Smart UpKeep", 11, INK, "khand") + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "url": return [("raw", v(t(30, 140, "Smart UpKeep", 18, INK, "khand") + t(30, 156, "SMARTUPKEEP.EXAMPLE", 7, MUTE, "hind", 600, extra='letter-spacing="1"') + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "line": return [("raw", v(t(30, 140, "Smart UpKeep", 18, INK, "khand") + t(30, 156, "Home Maintenance Membership", 7.5, MUTE) + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "rear": return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 160, "#FFFFFF", INK, 8, 1.5) + f'<line x1="120" y1="60" x2="120" y2="220" stroke="{INK}"/>' + roof(66, 110, TERRA) + t(66, 140, "Smart", 14, INK, "khand") + t(126, 140, "UpKeep", 14, INK, "khand") + rect(50, 190, 140, 6, TERRA), 0)]
    return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 160, "#FFFFFF", INK, 8, 1.5) + f'<line x1="120" y1="60" x2="120" y2="220" stroke="{INK}"/>' + t(120, 200, "HOW'S MY SERVICE?", 7, MUTE, "hind", 600, "middle") + rect(50, 190, 140, 3, TERRA), 0)]

G = "Tech Headshot Standard"
def th(k):
    bg = {"white": "#FFFFFF", "soft": SOFT, "lagoon": LAGOON + "22", "outdoor": None}
    if k in ("white", "soft", "lagoon"): return [("raw", rect(50, 50, 140, 170, bg[k], LINE, 8) + f'<circle cx="120" cy="114" r="28" fill="{INK}33"/><path d="M70 220 Q70 154 120 150 Q170 154 170 220 Z" fill="{TERRA}"/><path d="M110 152 L120 166 L130 152" fill="#FFFFFF"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
    if k == "outdoor": return [("raw", photo(50, 50, 140, 170, JUNGLE, "sun", 8) + f'<circle cx="120" cy="114" r="28" fill="{INK}33"/><path d="M70 220 Q70 154 120 150 Q170 154 170 220 Z" fill="{TERRA}"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
    if k == "close": return [("raw", rect(50, 50, 140, 170, SOFT, LINE, 8) + f'<circle cx="120" cy="120" r="44" fill="{INK}33"/><path d="M60 220 Q60 180 120 172 Q180 180 190 220 Z" fill="{TERRA}"/>' + t(120, 244, "Close Crop", 9, MUTE, "hind", 600, "middle"), 0)]
    return [("raw", rect(50, 50, 140, 170, SOFT, LINE, 8) + f'<circle cx="120" cy="100" r="18" fill="{INK}33"/><path d="M90 200 Q90 124 120 122 Q150 124 150 200 Z" fill="{TERRA}"/>' + rect(96, 196, 48, 24, INK + "55") + t(120, 244, "Waist Up, With Tool Bag", 9, MUTE, "hind", 600, "middle"), 0)]

G = "Watch Page"
def wp(k):
    v = lambda y, h: rect(14, y, 212, h, "#2B2B2B", "none", 8) + f'<circle cx="120" cy="{y+h/2}" r="18" fill="#FFFFFF"/><path d="M114 {y+h/2-9} L128 {y+h/2} L114 {y+h/2+9} Z" fill="{INK}"/>'
    if k == "tall": return [HU, ("raw", rect(60, 56, 120, 200, "#2B2B2B", "none", 10) + f'<circle cx="120" cy="156" r="18" fill="#FFFFFF"/><path d="M114 147 L128 156 L114 165 Z" fill="{INK}"/>', 206), ("btn", "Share", "line", INK)]
    if k == "wide": return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("btn", "Share", "line", INK)]
    if k == "cta": return [HU, ("raw", v(60, 120), 128), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", TERRA)]
    if k == "share": return [HU, ("raw", v(60, 120), 128), ("btn2", "Share", "Copy Link")]
    if k == "chapters": return [HU, ("raw", v(56, 100), 108), ("cards", [("The Visit", "0:00"), ("The Scan", "0:15"), ("Cancel Anytime", "0:38")], None, "ic:play", "line", 28)]
    return [HU, ("raw", v(56, 100), 108), ("p", "45 seconds. See a visit, a scan and how to cancel.")]

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

G = "Certification Badges"
def cb(k):
    B = [("Licensed", "check"), ("Insured", "star"), ("Background Checked", "search"), ("Trained", "clock")]
    if k == "shield": return [HU, ("h", "Your Licensed Tech", 15), ("raw", "".join(f'<path d="M{34+i*50} 90 L{54+i*50} 82 L{74+i*50} 90 V108 Q{54+i*50} 126 {34+i*50} 108 Z" fill="{ACC[i]}1F" stroke="{ACC[i]}" stroke-width="1.5"/>' + ic(k2, 46 + i * 50, 92, 16, ACC[i], 2) + t(54 + i * 50, 140, n.split()[0], 6.8, INK, "hind", 600, "middle") for i, (n, k2) in enumerate(B)), 90)]
    if k == "rows": return [HU, ("h", "Your Licensed Tech", 15), ("cards", [(n, "Verified", "") for n, _ in B], JUNGLE, "ic:check", "line", 30)]
    if k == "one": return [HU, ("h", "Your Licensed Tech", 15), ("tags", ["Licensed", "Insured", "Background Checked", "Trained"], True)]
    if k == "ink": return [HU, ("h", "Your Licensed Tech", 15), ("tags", ["Licensed", "Insured", "Background Checked", "Trained"])]
    if k == "date": return [HU, ("cards", [("Background Checked", "Rechecked yearly · Example date", "tag:Current")], JUNGLE)]
    return [HU, ("cards", [("Background Checked", "", "tag:Current")], JUNGLE)]

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

G = "Home Record Handoff"
def hr(k):
    if k == "book": return [HU, ("raw", rect(60, 60, 120, 150, "#FFFFFF", INK, 4, 1.5) + rect(60, 60, 12, 150, TERRA) + roof(96, 90, TERRA) + t(126, 130, "Home Record", 13, INK, "khand", anchor="middle") + t(126, 144, "Example Address", 7, MUTE, anchor="middle"), 160), ("btn", "Hand It Over", "fill", INK)]
    if k == "list": return [HU, ("h", "Home Record", 16), ("cards", [("Equipment", "6 items"), ("Visits", "8 logged"), ("Scans", "4 readings"), ("Warranties", "3 checked")], None, "ic:home", "line", 30)]
    if k == "link": return [HU, ("h", "Hand Over The Record", 15), ("cards", [("Share A Link", "Buyer opens it on any phone", "", "ic:tag")], LAGOON, "ic:tag")]
    if k == "pdf": return [HU, ("h", "Hand Over The Record", 15), ("cards", [("Download PDF", "Print for closing day", "", "ic:card")], LAGOON, "ic:card")]
    if k == "time": return [HU, ("h", "Home Record", 16), ("timeline", [("Oct 2026", "Fall visit, moisture scan"), ("Jul 2026", "Summer visit"), ("Apr 2026", "Spring visit, warranty check")])]
    return [HU, ("h", "Home Record", 16), ("stats", [("8", "Visits"), ("6", "Items"), ("4", "Scans")], "tint")]

# ---- round 8 additions ----
def gift(cx, cy, s=1, box=TERRA, rib=SAFFRON, style="solid"):
    """Drawn little gift box: body, lid, ribbon and bow."""
    w, h, lw, lh = 56 * s, 42 * s, 64 * s, 14 * s; x, y = cx - w / 2, cy - h / 2 + 8 * s
    fill = box if style == "solid" else "#FFFFFF"; strk = "none" if style == "solid" else box
    g = rect(x, y, w, h, fill, strk, 4 * s, 1.6) + rect(cx - lw / 2, y - lh, lw, lh, fill, strk, 3 * s, 1.6)
    g += rect(cx - 5 * s, y - lh, 10 * s, h + lh, rib) 
    g += f'<path d="M{cx} {y-lh} C{cx-22*s} {y-lh-20*s} {cx-26*s} {y-lh-2*s} {cx} {y-lh} C{cx+26*s} {y-lh-2*s} {cx+22*s} {y-lh-20*s} {cx} {y-lh} Z" fill="none" stroke="{rib}" stroke-width="{3*s}" stroke-linejoin="round"/>'
    return g + dot(cx, y - lh, 3.5 * s, rib)

G = "Plan Card"
def pc8(k):
    top = ("banner", PRICE, TERRA, "tag")
    tiles = ("tiles", [("Visits", "cal"), ("Moisture", "search"), ("Warranty", "check"), ("Reminders", "clock")], 2, 54)
    if k == "full": return [HU, top, tiles, ("btn", "Start My Membership", "fill", TERRA)]
    if k == "hline": return [HU, ("h", PRICE, 14), tiles, ("btn", "Start My Membership", "fill", TERRA)]
    if k == "tiles4": return [HU, top, tiles]
    if k == "tiles3": return [HU, top, ("tiles", [("Visits", "cal"), ("Moisture", "search"), ("Warranty", "check")], 3, 60)]
    if k == "solid": return [HU, top, ("tiles", [("Visits", "cal"), ("Moisture", "search"), ("Warranty", "check"), ("Reminders", "clock")], 2, 54, "solid")]
    if k == "cancel": return [HU, top, tiles, ("btn", "Start My Membership", "fill", TERRA), ("p", "Cancel Anytime.", 46, MUTE, True)]
    if k == "plain": return [HU, top, tiles, ("btn", "Start My Membership", "fill", TERRA)][:3] + [("gap", 6), ("btn", "Start", "fill", TERRA)]
    return [HU, ("lbl", "Your Membership"), top, tiles]
pr(G, "Banner Or Headline For The Price?", pc8, ("pc_bannerfull", "Terracotta Price Banner", "Your top pick, full card.", "focused", "full"), ("pc_headfull", "Price As The Headline", "Your one-line pick, up top.", "calm", "hline"))
pr(G, "Four Tiles Or Three?", pc8, ("pc_fourtiles", "Four Icon Tiles", "Visits, Moisture, Warranty, Reminders.", "visual", "tiles4"), ("pc_threetiles", "Three Wider Tiles", "Fewer, bigger.", "calm", "tiles3"))
pr(G, "Outlined Or Solid Tiles?", pc8, ("pc_linetiles", "Outlined Tiles, Colored Icons", "Light on white.", "calm", "tiles4"), ("pc_solidtiles", "Solid Color Tiles", "Bold blocks.", "visual", "solid"))
pr(G, "Cancel Anytime Under The Button?", pc8, ("pc_cancelline", "Cancel Anytime Line", "Small text under Start.", "calm", "cancel"), ("pc_nocancel", "Button Only", "Nothing under it.", "quick", "full"))

G = "Lawn Mowing Quote"
def lm8(k):
    three = ("cards", [("Weekly", "Every week"), ("Every Other Week", "Twice a month"), ("One Time", "Just once, no plan")], JUNGLE, "ic:cal")
    if k == "three": return [HU, ("h", "Lawn Mowing", 16), three, ("btn", "Get My Quote", "fill", INK)]
    if k == "link": return [HU, ("h", "Lawn Mowing", 16), ("cards", [("Weekly", "Every week"), ("Every Other Week", "Twice a month")], JUNGLE, "ic:cal"), ("p", "Just need it once? Get a one-time quote.", 46, LAGOON), ("btn", "Get My Quote", "fill", INK)]
    if k == "tabs": return [HU, ("h", "Lawn Mowing", 16), ("tabs", ["Repeat", "One Time"]), ("cards", [("Weekly", "Every week"), ("Every Other Week", "Twice a month")], JUNGLE, "ic:cal"), ("btn", "Get My Quote", "fill", INK)]
    if k == "addon": return [HU, ("h", "Add Lawn Mowing?", 16), ("p", "Same membership, one more service."), three, ("btn2", "Add It", "Not Now")]
    if k == "own": return [HU, ("h", "Lawn Mowing Quote", 16), ("p", "Its own page, separate from your membership."), three, ("btn", "Get My Quote", "fill", INK)]
    if k == "mapone": return [HU, ("h", "Your Lawn", 16), ("raw", rect(14, 80, 212, 110, JUNGLE + "1A", "none", 6) + f'<path d="M40 100 L200 96 L206 170 L36 174 Z" fill="{JUNGLE}44" stroke="{JUNGLE}" stroke-width="1.5" stroke-dasharray="4 3"/>' + rect(96, 116, 50, 34, "#FFFFFF", INK), 118), ("btn", "Quote One Mow", "fill", INK)]
    if k == "mapsize": return [HU, ("h", "Your Lawn", 16), ("raw", rect(14, 80, 212, 110, JUNGLE + "1A", "none", 6) + f'<path d="M40 100 L200 96 L206 170 L36 174 Z" fill="{JUNGLE}44" stroke="{JUNGLE}" stroke-width="1.5" stroke-dasharray="4 3"/>' + rect(96, 116, 50, 34, "#FFFFFF", INK) + rect(140, 176, 80, 18, "#FFFFFF", LINE, 9) + t(180, 188, "About 4,000 Sq Ft", 6.5, INK, "hind", 600, "middle"), 118), ("btn", "Get My Quote", "fill", INK)]
    if k == "calone": return [HU, ("lbl", "Mowing Days"), ("cal", (9,), JUNGLE), ("p", "One-time mow booked.")]
    return [HU, ("lbl", "Mowing Days"), ("cal", (2, 16, 30), JUNGLE), ("p", "Every other week.")]
pr(G, "One Time As A Third Card Or A Link?", lm8, ("lm_threecards", "Weekly, Every Other Week, One Time", "Three equal cards.", "focused", "three"), ("lm_onetimelink", "One-Time Quote Link", "Two plans, plus a link.", "calm", "link"))
pr(G, "Three Cards Or Repeat And One Time Tabs?", lm8, ("lm_threeagain", "Three Cards In A List", "All at once.", "focused", "three"), ("lm_tabs", "Repeat Or One Time Tabs", "Pick the kind first.", "quick", "tabs"))
pr(G, "Add-On Or Own Page? (Retest)", lm8, ("lm_addon3", "Add To Membership", "Head to head, with One Time.", "action", "addon"), ("lm_own3", "Its Own Quote Page", "Head to head, with One Time.", "focused", "own"), "retest")
pr(G, "Map With Size Or Map Only?", lm8, ("lm_mapsize", "Map With Size Readout", "Traced, with square feet.", "visual", "mapsize"), ("lm_maponce", "Map With Quote One Mow", "Fast one-time path.", "action", "mapone"))
pr(G, "Calendar: Every Other Week Or One Time?", lm8, ("lm_caleow", "Calendar, Every Other Week", "Your calendar pick, two-week plan.", "visual", "caleow"), ("lm_calone", "Calendar, One Mow", "Single day marked.", "calm", "calone"))

G = "Label Scan And Warranty Check"
def ls8(k):
    cam = lambda c, cap: ("raw", rect(14, 96, 212, 120, "#2B2B2B", "none", 8) + rect(54, 120, 132, 66, "#FFFFFF22", c, 4, 2) + t(120, 206, cap, 7, "#FFFFFF", "hind", 600, "middle"), 128)
    tbl = ("table", [("Brand", "Example Brand"), ("Model", "EX-199"), ("Serial", "XX-000000"), ("Year", "2021")])
    if k == "autodots": return [HU, ("dots", 5, 1, INK), ("h", "Scan The Label", 16), cam(JUNGLE, "HOLD STILL · READING")]
    if k == "autobar": return [HU, ("h", "Scan The Label", 16), cam(JUNGLE, "READING"), ("bar", .6, JUNGLE, "Reading The Label", "")]
    if k == "tblcheck": return [HU, ("raw", dot(28, 70, 10, JUNGLE + "22") + ic("check", 20, 62, 16, JUNGLE, 2) + t(46, 75, "Warranty Checked", 13, INK, "khand"), 34), tbl, ("btn2", "Looks Right", "Fix It")]
    if k == "zebra": return [HU, ("h", "We Read This", 16), ("table", [("Brand", "Example Brand"), ("Model", "EX-199"), ("Serial", "XX-000000"), ("Year", "2021")], True), ("btn2", "Looks Right", "Fix It")]
    if k == "check2": return [HU, ("raw", dot(120, 90, 24, JUNGLE + "22") + ic("check", 104, 74, 32, JUNGLE, 2), 80), ("h", "Warranty Checked", 18, INK, True), ("p", "Covered for parts. We'll remind you before it ends.", 40, MUTE, True), ("btn", "Done", "fill", INK)]
    return [HU, ("raw", dot(120, 90, 24, JUNGLE + "22") + ic("check", 104, 74, 32, JUNGLE, 2), 80), ("h", "Warranty Checked", 18, INK, True), tbl]
pr(G, "Auto-Read With Dots Or Reading Bar?", ls8, ("ls_autodots", "Auto-Read With Five Dots", "Step dots on top.", "focused", "autodots"), ("ls_autobar", "Auto-Read With A Reading Bar", "Shows it working.", "visual", "autobar"))
pr(G, "Check Above The Table Or Big Check First?", ls8, ("ls_tablecheck", "Small Check Over The Table", "Fields stay in view.", "focused", "tblcheck"), ("ls_bigthentable", "Big Check, Then Fields", "Reassure first.", "calm", "bigtbl"))
pr(G, "Plain Table Or Striped Rows?", ls8, ("ls_plaintable", "Plain Field Table", "Your table pick.", "calm", "tblcheck"), ("ls_zebratable", "Striped Field Rows", "Easier to scan.", "focused", "zebra"))

G = "Tech Card"
def tc8(k):
    flat = f'<circle cx="52" cy="110" r="28" fill="{TERRA}22"/><circle cx="52" cy="102" r="10" fill="{TERRA}"/><path d="M34 132 Q52 112 70 132 Z" fill="{TERRA}"/>'
    card = lambda f: rect(14, 72, 212, 100, "#FFFFFF", LINE, 8) + f + t(92, 102, LT, 12, INK, "khand") + t(92, 114, "State Licensed · Insured", 7, MUTE)
    if k == "terra": return [HU, ("lbl", "Next Visit · Thu 9 AM"), ("raw", rect(14, 72, 212, 170, "#FFFFFF", LINE, 8) + f'<circle cx="120" cy="110" r="18" fill="{LAGOON}55"/><path d="M84 194 Q84 140 120 136 Q156 140 156 194 Z" fill="{TERRA}"/><path d="M112 138 L120 150 L128 138" fill="#FFFFFF"/>' + t(120, 220, LT, 12, INK, "khand", anchor="middle"), 176)]
    if k == "white": return [HU, ("lbl", "Next Visit · Thu 9 AM"), ("raw", rect(14, 72, 212, 170, "#FFFFFF", LINE, 8) + f'<circle cx="120" cy="110" r="18" fill="{LAGOON}55"/><path d="M84 194 Q84 140 120 136 Q156 140 156 194 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.2"/><path d="M110 137 L120 150 L130 137" fill="none" stroke="{TERRA}" stroke-width="3"/>' + t(120, 220, LT, 12, INK, "khand", anchor="middle"), 176)]
    if k == "banner": return [HU, ("banner", "Next Visit · Thu 9 AM", LAGOON, "cal"), ("raw", card(flat).replace('y="72"', 'y="60"', 1), 120)]
    return [HU, ("lbl", "Next Visit · Thu 9 AM"), ("raw", card(flat), 120)]
pr(G, "Terracotta Polo Or White With Collar? (Retest)", tc8, ("tc_terrapolo2", "Terracotta Polo", "Head to head, with visit time.", "visual", "terra"), ("tc_whitepolo2", "White Polo, Terracotta Collar", "Head to head, with visit time.", "calm", "white"), "retest")
pr(G, "Visit Time As A Label Or A Banner?", tc8, ("tc_visitlabel", "Small Visit Label", "Quiet line above.", "calm", "label"), ("tc_visitbanner", "Lagoon Visit Banner", "Stands out.", "focused", "banner"))
pr(G, "Big Polo Card Or Compact Card With Visit?", tc8, ("tc_bigpolo", "Big Polo Card", "Shows the uniform.", "visual", "terra"), ("tc_compactvisit", "Compact Card Under The Visit", "Fits more on screen.", "quick", "label"))

G = "Home Sale Gift"
def hs8(k):
    form = [("input", "Buyer's Email", TERRA, "star"), ("input", "Closing Date", TERRA, "cal")]
    if k == "giftsolid": return [HU, ("raw", gift(120, 110, 1.2), 120), ("h", "Gift The Buyer 3 Months Free", 13, INK, True), ("btn", "Send The Gift", "fill", INK)]
    if k == "giftline": return [HU, ("raw", gift(120, 110, 1.2, TERRA, SAFFRON, "line"), 120), ("h", "Gift The Buyer 3 Months Free", 13, INK, True), ("btn", "Send The Gift", "fill", INK)]
    if k == "card": return [HU, ("raw", rect(24, 60, 192, 110, TERRA, "none", 10) + gift(176, 104, .7, "#FFFFFF", SAFFRON) + t(36, 130, "3 Months Free", 20, "#FFFFFF", "khand") + t(36, 146, "For The Buyer Of Your Home", 8, "#FFFFFFCC"), 118), ("btn", "Send The Gift", "fill", INK)]
    if k == "plain": return [HU, ("raw", gift(120, 80, .7), 64), ("h", "Selling Your Home?", 18, INK, True), ("p", "Gift the buyer 3 months free. We'll hand over your home's record too.", 46, MUTE, True), ("btn", "Send The Gift", "fill", INK)]
    if k == "agent": return [HU, ("h", "Gift The Buyer", 16)] + form + [("cards", [("Send Through My Agent", "They pass it on", "", "ic:phone")], LAGOON, "ic:phone"), ("btn", "Send", "fill", INK)]
    if k == "direct": return [HU, ("h", "Gift The Buyer", 16)] + form + [("cards", [("Send Straight To The Buyer", "We email them", "", "ic:card")], LAGOON, "ic:card"), ("btn", "Send", "fill", INK)]
    if k == "choose": return [HU, ("h", "Gift The Buyer", 16)] + form + [("tabs", ["To The Buyer", "To My Agent"]), ("btn", "Send", "fill", INK)]
    if k == "formgift": return [HU, ("raw", gift(36, 70, .5), 46), ("h", "Gift The Buyer", 16)] + form + [("btn", "Send", "fill", INK)]
    if k == "mailgift": return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4) + gift(120, 80, .9), 0), ("gap", 120), ("h", "A Gift With Your New Home", 14, INK, True), ("p", "The seller gave you 3 months of Smart UpKeep.", 38, MUTE, True), ("btn", "Claim My Gift", "fill", TERRA)]
    return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 30), ("h", "A Gift With Your New Home", 14, INK, True), ("p", "The seller gave you 3 months of Smart UpKeep.", 38, MUTE, True), ("btn", "Claim My Gift", "fill", TERRA)]
pr(G, "Solid Or Outlined Gift Drawing?", hs8, ("hs_giftsolid", "Terracotta Gift Box", "Saffron ribbon and bow.", "visual", "giftsolid"), ("hs_giftline", "Outlined Gift Box", "Lighter line drawing.", "calm", "giftline"))
pr(G, "Gift Card Or Plain Ask? (Retest, With Gift)", hs8, ("hs_cardgift", "Terracotta Gift Card With Gift", "Little gift in the corner.", "visual", "card"), ("hs_plaingift", "Selling Your Home? With Gift", "Small gift over the words.", "calm", "plain"), "retest")
pr(G, "Through The Agent Or Direct? (Retest)", hs8, ("hs_agent2", "Send Through Your Agent", "Head to head, in the short form.", "calm", "agent"), ("hs_direct2", "Send To The Buyer", "Head to head, in the short form.", "action", "direct"), "retest")
pr(G, "One Route Or Let The Seller Choose?", hs8, ("hs_oneroute", "One Route, Straight To Buyer", "Simple.", "quick", "direct"), ("hs_choose", "Buyer Or Agent Tabs", "Seller picks.", "focused", "choose"))
pr(G, "Short Form With Or Without The Gift?", hs8, ("hs_formgift", "Form With A Little Gift", "Small drawing on top.", "visual", "formgift"), ("hs_formplain", "Form Only", "Your short-form pick.", "quick", "choose"))
pr(G, "Buyer Email With Or Without The Gift?", hs8, ("hs_mailgift", "Welcome Email With Gift Drawing", "Gift box up top.", "visual", "mailgift"), ("hs_mailplain", "Welcome Email, Words Only", "Your email pick.", "calm", "mail"))

G = "Home Record Handoff"
def hr8(k):
    sec = ("cards", [("Equipment", "6 items"), ("Visits", "8 logged"), ("Scans", "4 readings"), ("Warranties", "3 checked")], None, "ic:home", "line", 30)
    if k == "link": return [HU, ("h", "Home Record", 16), sec, ("btn", "Share A Link", "fill", INK)]
    if k == "pdf": return [HU, ("h", "Home Record", 16), sec, ("btn", "Download A PDF", "fill", INK)]
    if k == "both": return [HU, ("h", "Home Record", 16), sec, ("btn2", "Share Link", "PDF")]
    if k == "tint": return [HU, ("h", "Home Record", 16), ("cards", [("Equipment", "6 items"), ("Visits", "8 logged"), ("Scans", "4 readings"), ("Warranties", "3 checked")], None, "ic:home", "tint", 30), ("btn", "Share A Link", "fill", INK)]
    return [HU, ("h", "Home Record", 16), ("cards", [("Equipment", "6 items"), ("Visits", "8 logged"), ("Scans", "4 readings"), ("Warranties", "3 checked")], None, "num", "line", 30), ("btn", "Share A Link", "fill", INK)]
pr(G, "Share Link Or PDF? (Retest)", hr8, ("hr_link2", "Share A Link", "Head to head under the sections.", "quick", "link"), ("hr_pdf2", "Download A PDF", "Head to head under the sections.", "calm", "pdf"), "retest")
pr(G, "One Button Or Both Side By Side?", hr8, ("hr_onebtn", "One Share Button", "Single path.", "quick", "link"), ("hr_twobtn", "Link And PDF Side By Side", "Both choices.", "focused", "both"))
pr(G, "Icon Sections Or Tinted Sections?", hr8, ("hr_iconsec", "Sections With Drawn Icons", "Thin borders.", "visual", "nums"), ("hr_tintsec", "Soft Tinted Sections", "Color blocks.", "calm", "tint"))

G = "Moisture Scan Report"
def ms8(k):
    gauge = ("raw", rect(14, 76, 212, 12, "#EEEAE4", "none", 6) + rect(14, 76, 70, 12, JUNGLE, "none", 6) + rect(84, 76, 70, 12, SAFFRON, "none", 0) + rect(154, 76, 72, 12, TERRA, "none", 6) + f'<path d="M110 70 L116 62 H104 Z" fill="{INK}"/>' + t(14, 102, "Dry", 7, MUTE) + t(120, 102, "Damp", 7, MUTE, anchor="middle") + t(226, 102, "Wet", 7, MUTE, anchor="end"), 40)
    if k == "ask": return [HU, ("lbl", "Bath · Reading"), gauge, ("p", "Damp. We'll check again next visit."), ("btn", "Ask A Question", "line", INK)]
    if k == "fix": return [HU, ("lbl", "Bath · Reading"), gauge, ("p", "Damp. We'll check again next visit."), ("btn", "Book A Fix", "fill", TERRA)]
    if k == "two": return [HU, ("lbl", "Bath · Reading"), gauge, ("p", "Damp. We'll check again next visit."), ("btn2", "Book A Fix", "Ask")]
    if k == "word": return [HU, ("lbl", "Bath · Reading"), gauge, ("word", "Damp", 26, SAFFRON, "Check Again Next Visit")]
    return [HU, ("lbl", "Bath · Reading"), gauge]
pr(G, "Ask Or Book A Fix? (Retest)", ms8, ("ms_ask2", "Ask A Question Button", "Head to head under the gauge.", "calm", "ask"), ("ms_fix2", "Book A Fix Button", "Head to head under the gauge.", "action", "fix"), "retest")
pr(G, "One Button Or Both?", ms8, ("ms_onebtn", "One Button", "Ask only.", "calm", "ask"), ("ms_twobtn", "Fix And Ask Side By Side", "Both paths.", "focused", "two"))
pr(G, "Gauge Alone Or With A Word?", ms8, ("ms_gaugealone", "Gauge Alone", "Pointer says it.", "calm", "gauge"), ("ms_gaugeword", "Gauge And Damp Word", "Two cues.", "visual", "word"))

G = "Extras And Add-On Pop-Up"
def ex8(k):
    base = rect(0, 150, W, 150, "#FFFFFF", "none", 14) + rect(0, 0, W, 150, "#0A0A0A33") + rect(104, 158, 32, 4, "#D6D0C6", "none", 2) + t(14, 184, "Add Gutter Cleaning?", 13, INK, "khand") + t(14, 196, "Before your first visit.", 7.5, MUTE)
    if k == "x": return [HU, ("cards", [("Seasonal Visits", "")]), ("raw", base + btn(212, "Add It", "fill", INK, 14, 212, 26, 8) + t(120, 256, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"') + ic("x", 206, 168, 14, MUTE), 0)]
    if k == "icon": return [HU, ("cards", [("Seasonal Visits", "")]), ("raw", base.replace(t(14, 184, "Add Gutter Cleaning?", 13, INK, "khand"), ic("star", 14, 170, 18, SAFFRON, 2) + t(38, 184, "Add Gutter Cleaning?", 13, INK, "khand")) + btn(212, "Add It", "fill", INK, 14, 212, 26, 8) + t(120, 256, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"') + ic("x", 206, 168, 14, MUTE), 0)]
    if k == "terra": return [HU, ("cards", [("Seasonal Visits", "")]), ("raw", base + btn(212, "Add It", "fill", TERRA, 14, 212, 26, 8) + t(120, 256, "NO THANKS", 7, MUTE, "hind", 600, "middle", 'text-decoration="underline"') + ic("x", 206, 168, 14, MUTE), 0)]
    return [HU, ("cards", [("Seasonal Visits", "")]), ("raw", base + btn(212, "Add It", "fill", INK, 14, 103, 26, 8) + btn(212, "No Thanks", "line", INK, 123, 103, 26, 8) + ic("x", 206, 168, 14, MUTE), 0)]
pr(G, "Sheet: Link And X Or Two Buttons And X?", ex8, ("ex_sheetx", "Sheet, No Thanks Link And X", "Both your picks together.", "calm", "x"), ("ex_sheetbtnx", "Sheet, Two Buttons And X", "Equal buttons.", "focused", "btns"))
pr(G, "Sheet With Or Without A Star Icon?", ex8, ("ex_sheetplain", "Sheet, Words Only", "Clean.", "calm", "x"), ("ex_sheetstar", "Sheet With Saffron Star", "A little color.", "visual", "icon"))
pr(G, "Ink Or Terracotta Add Button?", ex8, ("ex_inkadd", "Ink Add It Button", "Quiet.", "calm", "x"), ("ex_terraadd", "Terracotta Add It Button", "Brand color.", "action", "terra"))

G = "Watch Page"
def wp8(k):
    v = lambda y, h: rect(14, y, 212, h, "#2B2B2B", "none", 8) + f'<circle cx="120" cy="{y+h/2}" r="18" fill="#FFFFFF"/><path d="M114 {y+h/2-9} L128 {y+h/2} L114 {y+h/2+9} Z" fill="{INK}"/>'
    if k == "titletop": return [HU, ("h", "See How It Works", 15), ("raw", v(80, 120), 128), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", TERRA)]
    if k == "titleunder": return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", TERRA)]
    if k == "share": return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("btn", "Start My Membership", "fill", TERRA), ("btn", "Share", "line", INK)]
    if k == "ink": return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("p", PRICE, 46, INK), ("btn", "Start My Membership", "fill", INK)]
    return [HU, ("raw", v(60, 120), 128), ("h", "See How It Works", 15), ("btn", "Start My Membership", "fill", TERRA)]
pr(G, "Title Over Or Under The Wide Player?", wp8, ("wp_titletop", "Title Over The Player", "Read, then watch.", "focused", "titletop"), ("wp_titleunder", "Title Under The Player", "Watch first.", "visual", "titleunder"))
pr(G, "Price And Start Or Start And Share?", wp8, ("wp_pricestart", "Price Line And Start", "Your watch pick.", "action", "titleunder"), ("wp_startshare", "Start And Share Buttons", "Both actions.", "focused", "share"))
pr(G, "Terracotta Or Ink Start Button?", wp8, ("wp_terrastart", "Terracotta Start", "Brand color.", "action", "titleunder"), ("wp_inkstart", "Ink Start", "Quiet.", "calm", "ink"))

G = "Yard Sign And Battery Swap"
def ys8(k):
    sign = lambda: rect(70, 60, 100, 70, "#FFFFFF", INK, 2, 1.5) + roof(109, 72, TERRA, .8) + t(120, 104, "Smart UpKeep", 10, INK, "khand", anchor="middle") + t(120, 118, "Member Home", 6, MUTE, "hind", 600, "middle") + f'<line x1="90" y1="130" x2="90" y2="170" stroke="{INK}" stroke-width="2"/><line x1="150" y1="130" x2="150" y2="170" stroke="{INK}" stroke-width="2"/>'
    if k == "row": return [HU, ("lbl", "Settings"), ("cards", [("Yard Sign", "Free battery swap if yes", "tag:Opt In")], JUNGLE, "ic:check")]
    if k == "chat": return [HU, ("bubble", "Want a yard sign? You'll get a free smoke detector battery swap.", False), ("bubble", "Yes", True)]
    if k == "rewardsign": return [HU, ("raw", sign(), 128), ("cards", [("Free Battery Swap", "Smoke detectors, next visit", "", "ic:check")], JUNGLE, "ic:check", "tint", 44), ("btn2", "Yes, Add Sign", "No Thanks")]
    if k == "chatsign": return [HU, ("raw", sign(), 128), ("bubble", "Want this sign? Free battery swap next visit.", False), ("bubble", "Yes", True)]
    if k == "member": return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, "#FFFFFF", INK, 2, 1.5) + roof(108, 76, TERRA) + t(120, 120, "Smart UpKeep", 14, INK, "khand", anchor="middle") + t(120, 138, "Member Home", 7, MUTE, "hind", 600, "middle") + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]
    return [("raw", rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 100, "#FFFFFF", INK, 2, 1.5) + roof(108, 76, TERRA) + t(120, 120, "Smart UpKeep", 14, INK, "khand", anchor="middle") + t(120, 138, "SMARTUPKEEP.EXAMPLE", 6.5, MUTE, "hind", 600, "middle") + rect(50, 150, 140, 4, TERRA) + f'<line x1="80" y1="160" x2="80" y2="250" stroke="{INK}" stroke-width="2"/><line x1="160" y1="160" x2="160" y2="250" stroke="{INK}" stroke-width="2"/>', 0)]
pr(G, "Opt-In Row Or Chat Ask? (Retest)", ys8, ("ys_row2", "Opt-In Row In Settings", "Head to head.", "calm", "row"), ("ys_chat2", "Ask In Chat Bubbles", "Head to head.", "action", "chat"), "retest")
pr(G, "Reward Card With Sign Or Chat With Sign?", ys8, ("ys_rewardsign", "Reward Card Under The Sign", "Your reward pick, with the white sign.", "action", "rewardsign"), ("ys_chatsign", "Chat Ask Under The Sign", "Friendlier.", "calm", "chatsign"))
pr(G, "Member Home Or Web Address On The Sign?", ys8, ("ys_memberhome", "White Sign, Member Home", "Your sign pick.", "calm", "member"), ("ys_urlsign", "White Sign, Web Address And Stripe", "Easy to look up.", "action", "url"))
pr(G, "Settings Row: Green Or Terracotta Tag?", ys8, ("ys_greenrow", "Green Opt-In Row", "Calm yes.", "calm", "row"), ("ys_rowreward", "Reward Card With Sign", "Big ask.", "visual", "rewardsign"))

G = "Tech Headshot Standard"
def th8(k):
    bg = {"white": "#FFFFFF", "soft": SOFT}
    if k in ("white", "soft"): return [("raw", rect(50, 50, 140, 170, bg[k], LINE, 8) + f'<circle cx="120" cy="120" r="44" fill="{INK}33"/><path d="M60 220 Q60 180 120 172 Q180 180 190 220 Z" fill="{TERRA}"/><path d="M110 174 L120 188 L130 174" fill="#FFFFFF"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
    if k == "round": return [("raw", f'<circle cx="120" cy="130" r="74" fill="#FFFFFF" stroke="{LINE}"/><circle cx="120" cy="118" r="34" fill="{INK}33"/><path d="M66 188 Q76 160 120 156 Q164 160 174 188 Q150 206 120 204 Q90 206 66 188 Z" fill="{TERRA}"/>' + t(120, 232, LT, 11, INK, "khand", anchor="middle"), 0)]
    return [("raw", rect(50, 50, 140, 170, "#FFFFFF", LINE, 8) + f'<circle cx="120" cy="120" r="44" fill="{INK}33"/><path d="M60 220 Q60 180 120 172 Q180 180 190 220 Z" fill="{TERRA}"/>' + t(120, 244, LT, 11, INK, "khand", anchor="middle"), 0)]
pr(G, "White Or Soft Background? (Retest)", th8, ("th_white2", "Pure White, Close Crop", "Head to head.", "calm", "white"), ("th_soft2", "Soft Warm Gray, Close Crop", "Head to head.", "calm", "soft"), "retest")
pr(G, "Square Or Round Close Crop?", th8, ("th_square", "Square Close Crop", "Rounded corners.", "focused", "white"), ("th_round", "Round Close Crop", "Circle frame.", "visual", "round"))
pr(G, "With Or Without The White Collar V?", th8, ("th_collarv", "White V At The Collar", "Polo detail.", "visual", "white"), ("th_nocollar", "Plain Terracotta Shirt", "Simpler.", "calm", "plain"))

G = "Renewal And Cancel Notice"
OFFER1, OFFER2 = "One Month Free to Stay", "Two Months Free to Stay"
def rn8(k):
    sett = ("cards", [("Membership", "Renews monthly"), ("Payment", "Card on file"), ("Cancel Anytime", "")], None, "dot", "line", 30)
    if k == "offercard1": return [HU, ("h", "Before You Go", 15), ("raw", rect(14, 82, 212, 96, TERRA, "none", 10) + gift(190, 120, .55, "#FFFFFF", SAFFRON) + t(28, 120, "One Month Free", 18, "#FFFFFF", "khand") + t(28, 140, "to Stay", 18, "#FFFFFF", "khand") + t(28, 160, "THANKS FOR 6 MONTHS WITH US", 6.5, "#FFFFFFCC", "hind", 600), 104), ("btn", "Stay And Get It Free", "fill", INK), ("p", "Still want to cancel? Cancel Anytime.", 46, MUTE, True)]
    if k == "offercard2": return [HU, ("h", "Before You Go", 15), ("raw", rect(14, 82, 212, 96, TERRA, "none", 10) + gift(190, 120, .55, "#FFFFFF", SAFFRON) + t(28, 120, "Two Months Free", 18, "#FFFFFF", "khand") + t(28, 140, "to Stay", 18, "#FFFFFF", "khand") + t(28, 160, "THANKS FOR A YEAR WITH US", 6.5, "#FFFFFFCC", "hind", 600), 104), ("btn", "Stay And Get It Free", "fill", INK), ("p", "Still want to cancel? Cancel Anytime.", 46, MUTE, True)]
    if k == "offerline1": return [HU, ("h", "Before You Go", 15), ("raw", rect(14, 82, 212, 70, "#FFFFFF", LINE, 8) + rect(14, 82, 4, 70, TERRA) + t(30, 112, OFFER1, 14, INK, "khand") + t(30, 130, "Thanks for 6 months with us.", 7.5, MUTE), 78), ("btn2", "Stay", "Cancel")]
    if k == "offerline2": return [HU, ("h", "Before You Go", 15), ("raw", rect(14, 82, 212, 70, "#FFFFFF", LINE, 8) + rect(14, 82, 4, 70, TERRA) + t(30, 112, OFFER2, 14, INK, "khand") + t(30, 130, "Thanks for a year with us.", 7.5, MUTE), 78), ("btn2", "Stay", "Cancel")]
    if k == "offergift": return [HU, ("raw", gift(120, 100, 1.1), 110), ("h", OFFER1, 16, INK, True), ("p", "Thanks for 6 months with us.", 46, MUTE, True), ("btn2", "Stay", "Cancel")]
    if k == "offerword": return [HU, ("gap", 24), ("word", OFFER1, 20, TERRA, "Thanks For 6 Months With Us"), ("btn2", "Stay", "Cancel")]
    if k == "sheet": return [HU, ("lbl", "Settings"), sett, ("raw", rect(0, 170, W, 130, "#FFFFFF", "none", 14) + rect(0, 0, W, 170, "#0A0A0A33") + rect(104, 178, 32, 4, "#D6D0C6", "none", 2) + t(14, 206, OFFER1, 14, INK, "khand") + t(14, 220, "Thanks for 6 months with us.", 7.5, MUTE) + btn(240, "Stay", "fill", INK, 14, 103, 26, 8) + btn(240, "Cancel", "line", INK, 123, 103, 26, 8), 0)]
    if k == "fullpage": return [HU, ("lbl", "Settings · Cancel Anytime"), ("h", OFFER1, 18), ("p", "Thanks for 6 months with us."), ("btn", "Stay", "fill", INK), ("btn", "Cancel", "line", INK)]
    if k == "recapoffer": return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 30), ("h", "Your Membership Renews Soon", 13, INK, True), ("p", "Here's what you got this year:", 38, MUTE, True), ("stats", [("4", "Visits"), ("1", "Scan Flag"), ("3", "Warranties")], "tint"), ("banner", OFFER2 + " · Thanks For A Year", TERRA, "star")]
    if k == "recap": return [("raw", rect(0, 0, W, H, "#F5F5F5") + rect(14, 14, 212, 272, "#FFFFFF", LINE, 4), 0), ("gap", 30), ("h", "Your Membership Renews Soon", 13, INK, True), ("p", "Here's what you got this year:", 38, MUTE, True), ("stats", [("4", "Visits"), ("1", "Scan Flag"), ("3", "Warranties")], "tint"), ("btn", "See My Year", "fill", TERRA)]
    if k == "row": return [HU, ("lbl", "Settings"), sett]
    return [HU, ("lbl", "Settings"), ("cards", [("Membership", "Renews monthly"), ("Payment", "Card on file")], None, "dot", "line", 30), ("p", "Cancel Anytime", 46, TERRA)]
pr(G, "Retention Offer: Bold Card Or Quiet Card?", rn8, ("rn_offerbold1", "One Month Free To Stay, Terracotta Card", "6+ months; gift in the corner.", "visual", "offercard1"), ("rn_offerquiet1", "One Month Free To Stay, Thin Card", "6+ months; terracotta edge.", "calm", "offerline1"))
pr(G, "Retention Offer After A Year: Bold Or Quiet?", rn8, ("rn_offerbold2", "Two Months Free To Stay, Terracotta Card", "1+ year members.", "visual", "offercard2"), ("rn_offerquiet2", "Two Months Free To Stay, Thin Card", "1+ year members.", "calm", "offerline2"))
pr(G, "Retention Offer: Gift Drawing Or Big Words?", rn8, ("rn_offergift", "Gift Drawing Over The Offer", "Little gift, then the line.", "visual", "offergift"), ("rn_offerword", "Offer As Big Words", "Terracotta headline only.", "focused", "offerword"))
pr(G, "Retention Offer: Bottom Sheet Or Full Page?", rn8, ("rn_offersheet", "Offer Slides Up Over Settings", "Appears on Cancel tap.", "calm", "sheet"), ("rn_offerpage", "Offer As Its Own Page", "Stay or Cancel buttons.", "focused", "fullpage"))
pr(G, "Year Recap Email: Offer Banner Or Plain?", rn8, ("rn_recapoffer", "Recap With Two Months Free To Stay", "For 1+ year members.", "action", "recapoffer"), ("rn_recapplain", "Recap, See My Year Button", "Your recap pick.", "calm", "recap"))
pr(G, "Cancel As A Row Or A Text Link?", rn8, ("rn_cancelrow", "Cancel Anytime Row", "Your settings pick.", "calm", "row"), ("rn_cancellink", "Cancel Anytime Text Link", "Below the list.", "quick", "link"))

G = "Van Side"
def vn8(k):
    v = lambda body: rect(0, 0, W, H, SOFT) + f'<path d="M14 200 V120 Q14 100 34 100 H170 Q200 100 214 130 L226 150 V200 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.5"/>' + f'<circle cx="60" cy="204" r="14" fill="{INK}"/><circle cx="180" cy="204" r="14" fill="{INK}"/>' + body
    rear = lambda body: rect(0, 0, W, H, SOFT) + rect(50, 60, 140, 160, "#FFFFFF", INK, 8, 1.5) + f'<line x1="120" y1="60" x2="120" y2="220" stroke="{INK}"/>' + body
    if k == "bigurl": return [("raw", v(roof(30, 116, TERRA, 1.4) + t(66, 136, "Smart UpKeep", 20, INK, "khand") + t(66, 152, "SMARTUPKEEP.EXAMPLE", 7, MUTE, "hind", 600, extra='letter-spacing="1"') + rect(14, 170, 200, 6, TERRA)), 0)]
    if k == "bigurlterra": return [("raw", v(roof(30, 116, TERRA, 1.4) + t(66, 136, "Smart UpKeep", 20, INK, "khand") + t(66, 152, "SMARTUPKEEP.EXAMPLE", 7, TERRA, "hind", 700, extra='letter-spacing="1"')), 0)]
    if k == "rearname": return [("raw", rear(roof(66, 110, TERRA) + t(66, 140, "Smart", 14, INK, "khand") + t(126, 140, "UpKeep", 14, INK, "khand") + rect(50, 190, 140, 6, TERRA)), 0)]
    if k == "rearask": return [("raw", rear(t(120, 200, "HOW'S MY SERVICE?", 7, MUTE, "hind", 600, "middle") + rect(50, 190, 140, 3, TERRA)), 0)]
    if k == "rearboth": return [("raw", rear(roof(66, 110, TERRA) + t(66, 140, "Smart", 14, INK, "khand") + t(126, 140, "UpKeep", 14, INK, "khand") + t(120, 178, "HOW'S MY SERVICE?", 7, MUTE, "hind", 600, "middle") + rect(50, 190, 140, 6, TERRA)), 0)]
    return [("raw", v(roof(30, 120, TERRA, 1.4) + t(66, 140, "Smart UpKeep", 20, INK, "khand") + rect(14, 170, 200, 6, TERRA)), 0)]
pr(G, "Rear Doors: Name Or Service Question? (Retest)", vn8, ("vn_rearname2", "Name Across Rear Doors", "Head to head.", "visual", "rearname"), ("vn_rearask2", "How's My Service Line", "Head to head.", "calm", "rearask"), "retest")
pr(G, "Rear Doors: One Or Both?", vn8, ("vn_rearone", "Name Only On The Rear", "Clean.", "calm", "rearname"), ("vn_rearboth", "Name And Service Question", "Both together.", "focused", "rearboth"))
pr(G, "Big Name: With Or Without The Web Address?", vn8, ("vn_bignameurl", "Big Name And Web Address", "Both your side picks.", "action", "bigurl"), ("vn_bignameonly", "Big Name Only", "Bolder.", "visual", "big"))
pr(G, "Stripe Or No Stripe?", vn8, ("vn_stripe", "Terracotta Stripe", "Ties the side together.", "visual", "bigurl"), ("vn_nostripe", "No Stripe, Terracotta Address", "More white.", "calm", "bigurlterra"))

# rule check before publishing
blob = json.dumps(pairs, ensure_ascii=False)
txt = re.sub(r"<[^>]+>", " ", blob)
for bad in [r"\bAI\b", r"Health Score", r"Forecast", r"\bSilver\b", r"\bGold\b", r"\bPlatinum\b", r"\bEssentials\b", r"\bPlus\b", r"\bComplete\b", r"\bPremium\b", r"\bBasic\b", r"\bTier", r"Built", r"By Max", r"Weberman", r"License #", r"Lic\.? ?#", r"\bLIC\b"]:
    m = re.search(bad, txt, re.I if bad in ("Built", "By Max", "Weberman", "Forecast", r"License #", r"Lic\.? ?#") else 0); assert not m, (bad, txt[max(0, m.start()-60):m.end()+60])
assert txt.count("$") == txt.count(PRICE), (txt.count("$"), txt.count(PRICE))
assert not re.search(r"\$\s?\d+(?!/Month)", txt.replace(PRICE, "")), "stray price"
for p in pairs:
    if "Retention" in p["ask"]:
        for s in "AB": assert "$" not in json.dumps(p["option" + s])
assert "Certification Badges" not in {p["group"] for p in pairs}
publish(DID, "UpKeep Round 8: Refined Winners From Round 7, Head-To-Head Retests, Gift Drawing, One-Time Lawn Mow, Retention Offer", "UpKeep", pairs,
        {"brands": ["Smart UpKeep home maintenance membership; built from upkeep-7 picks (35/50)", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017; only price 'Membership Starting at $99/Month'; 'Your Licensed Tech', no named tech, no license numbers; no byline"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"}, "based_on": "upkeep-7 picks",
         "sources": {"picks": "/workspace/smartkeep/branding/upkeep-7-picks.md", "results": "results/upkeep-7.txt (local, not committed)", "prior_deck": "decks/upkeep-7.json"}}, seed=38)
