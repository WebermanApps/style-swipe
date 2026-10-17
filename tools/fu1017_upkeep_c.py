"""UpKeep follow-ons C (Oct 17 2026): Trust Tags (two decks), Sign Up Form, What We Take Care Of. Badges: approved set only."""
from fu1017_kit import *
from fu1017_upkeep_a import D, phdr, video, BADGES
APP = {"Certified Techs": "check", "Cancel Anytime": "x", "Home Reports": "tag", "Background-Checked Yearly": "star", "Moisture Scan Every Visit": "clock", "Licensed & Insured": "check"}
def pill(x, y, s, c, style="tint", icon_=None, big=False, border=False, txt=None):
    h = 19 if big else 15; fs = 8 if big else 7.5; w = len(s) * (4.3 if big else 3.9) + (24 if icon_ else 12)
    if style == "tint": s_ = rect(x, y, w, h, c + "1A", c if border else "none", h / 2, .8)
    elif style == "check": s_ = ""
    else: s_ = rect(x, y, w, h, "#FFFFFF", c, h / 2, 1)
    xx = x + 6
    if icon_ == "check" or style == "check": s_ += f'<path d="M{x+5} {y+h/2} l2.5 2.5 4.5 -5" fill="none" stroke="{c}" stroke-width="1.6"/>'; xx = x + 15
    elif icon_ == "dot": s_ += dot(x + 8, y + h / 2, 2.4, c); xx = x + 14
    return s_ + t(xx, y + h / 2 + fs * .36, s, fs, txt or c, "hind", 600), w
def chipset(x, y, items, w=212, wrap_=True, style="tint", icon_=None, big=False, border=False, dark=False, center=False, colors=None):
    s, xx, yy, rows = "", x, y, [[]]
    for i, it in enumerate(items):
        c = (colors or ACC)[i % len(colors or ACC)]
        g_, cw = pill(0, 0, it, c, style, icon_, big, border, (INK if not dark else None))
        if xx + cw > x + w:
            if not wrap_: s += t(x + w, yy + 11, ">", 9, MUTE, "hind", 700, "end"); break
            xx, yy = x, yy + (23 if big else 19); rows.append([])
        s += f'<g transform="translate({xx},{yy})">{g_}</g>'; xx += cw + 5
    return s, yy - y + (23 if big else 19)
def home_hero(items, pos="under_head", heading="Why Trust Us", head_center=False, head_style="label", **k):
    s, h = phdr(30); y = 30 + h + 8
    s += t(24, y + 18, "Your Home,", 19, INK, "khand", 700) + t(24, y + 37, "Taken Care Of.", 19, INK, "khand", 700); y += 46
    def row(y):
        o = ""
        if heading:
            if head_style == "label": o += t(120 if head_center else 24, y + 8, heading.upper(), 7.5, MUTE, "hind", 600, "middle" if head_center else "start", 'letter-spacing="1.2"'); y += 14
            else: o += t(120 if head_center else 24, y + 14, heading, 13, INK, "khand", 700, "middle" if head_center else "start"); y += 20
        g_, hh = chipset(24, y, items, 192, **k); return o + g_, y + hh
    if pos == "under_head":
        g_, y = row(y); s += g_; y += 4
    s += video(14, y, 212, 70); y += 76
    s += rect(24, y, 192, 22, TERRA) + t(120, y + 14.5, "FREE QUOTE IN MINUTES", 8, "#FFFFFF", "hind", 600, "middle", 'letter-spacing=".8"'); y += 28
    if pos == "under_cta":
        g_, y = row(y); s += g_
    return s + rect(14, 30, 212, 240, "none", "#BDB6AA", 0, 1)
def TH(label, acc, items, foot=None, **k): return card(label, acc, home_hero(items, **k) + (chips(276, foot) if foot else ""))
B = BADGES
# ================= Trust Tags: Order And Placement (follow-on to Theme & Current Vs New) =================
TO = []
def a(g, ask, x, y): TO.append((g, ask, x, y))
a("Theme", "Re-Ask, Safety Badge: 'Licensed & Insured', Or 'Moisture Scan Every Visit'?",
  opt("tto_lic", "Licensed & Insured", "Your note's wording, plain safety claim.", "calm", TH("Safety Badge", LAGOON, ["Certified Techs", "Licensed & Insured", "Home Reports", "Cancel Anytime"])),
  opt("tto_moist", "Moisture Scan Every Visit", "Proof of care in every visit.", "practical", TH("Safety Badge", JUNGLE, ["Certified Techs", "Moisture Scan Every Visit", "Home Reports", "Cancel Anytime"])))
a("Mix", "Re-Ask, Badge Order: Proof Badges First (Home Reports, Moisture Scan), Or Promise Badges First (Cancel Anytime, Certified Techs)?",
  opt("tto_proof", "Proof First", "What we hand you after each visit leads.", "practical", TH("Badge Order", JUNGLE, ["Home Reports", "Moisture Scan Every Visit", "Certified Techs", "Cancel Anytime"])),
  opt("tto_promise", "Promise First", "What you can count on leads.", "calm", TH("Badge Order", TERRA, ["Cancel Anytime", "Certified Techs", "Home Reports", "Moisture Scan Every Visit"])))
a("Theme", "First Badge In The Row: 'Certified Techs', Or 'Background-Checked Yearly'?",
  opt("tto_cert1", "Certified Techs", "Short and known; today's first chip.", "calm", TH("Lead Badge", TERRA, ["Certified Techs", "Licensed & Insured", "Home Reports", "Cancel Anytime"])),
  opt("tto_bg1", "Background-Checked Yearly", "People-first: who comes into your home.", "premium", TH("Lead Badge", LAGOON, ["Background-Checked Yearly", "Certified Techs", "Home Reports", "Cancel Anytime"])))
a("Count", "Showing The Approved Badges: All Six At Once, Or Four With A '+2 More' Chip?",
  opt("tto_six", "All Six", "Every approved badge, two lines.", "bold", TH("Badge Count", TERRA, B)),
  opt("tto_more", "Four + '+2 More'", "Calmer row; tap to see the rest.", "calm", TH("Badge Count", LAGOON, B[:4] + ["+2 More"])))
a("Mix", "Badge Order Each Visit: A Random Order Every Time (Your Note), Or One Fixed Order?",
  opt("tto_rand", "Random Each Time", "Order shuffles on each page load.", "playful", card("Badge Order", SAFFRON, home_hero(["Licensed & Insured", "Home Reports", "Certified Techs", "Cancel Anytime"]) + t(120, 262, "next visit: a new order", 7.5, MUTE, "hind", 400, "middle"))),
  opt("tto_fixed", "One Fixed Order", "Same row every time.", "calm", TH("Badge Order", INK, ["Certified Techs", "Licensed & Insured", "Home Reports", "Cancel Anytime"])))
a("Style", "Badge Look: A Small Check Mark Inside Each Pill, Or Text Only?",
  opt("tto_check", "Check In Each Pill", "Reads like a promise kept.", "practical", TH("Badge Look", JUNGLE, B[:4], icon_="check")),
  opt("tto_text", "Text Only", "Lightest look, more room.", "calm", TH("Badge Look", LAGOON, B[:4])))
def sheet(name, line):
    s = home_hero(B[:4]) + rect(14, 160, 212, 110, "#0A0A0A33") + rect(14, 176, 212, 94, "#FFFFFF") + rect(104, 182, 32, 3, "#D6D0C6")
    return s + t(26, 204, name, 13, INK, "khand", 700) + t(26, 220, line, 8, MUTE) + t(26, 250, "CLOSE", 8, LAGOON, "hind", 600)
a("Style", "Tapping A Badge: Opens A Short Sheet Saying What It Means, Or Nothing Happens?",
  opt("tto_tap", "Opens A Short Sheet", "One plain line from the site's FAQ.", "practical", card("Badge Tap", LAGOON, sheet("Cancel Anytime", "Cancel your plan anytime, as the FAQ says."))),
  opt("tto_none", "Nothing Happens", "Badges are labels, not buttons.", "calm", TH("Badge Tap", INK, B[:4])))
a("Placement", "Badge Row Spot: Right Under The Headline, Or Under The Free Quote Button?",
  opt("tto_under_h", "Under The Headline", "Trust before the video.", "calm", TH("Badge Spot", TERRA, B[:4], pos="under_head")),
  opt("tto_under_c", "Under The Button", "Trust right where you decide.", "practical", TH("Badge Spot", LAGOON, B[:4], pos="under_cta")))
a("Placement", "'Cancel Anytime': A Badge In The Row, Or A Small Line Right Under The Button?",
  opt("tto_cbadge", "Badge In The Row", "Same weight as the others.", "calm", TH("Cancel Anytime", TERRA, ["Certified Techs", "Cancel Anytime", "Home Reports", "Licensed & Insured"], pos="under_cta")),
  opt("tto_cline", "Line Under The Button", "Answers 'what if I stop?' at the click.", "practical", card("Cancel Anytime", LAGOON, home_hero(["Certified Techs", "Home Reports", "Licensed & Insured"], pos="under_head") + t(120, 236 + 0, "", 1) + t(120, 268, "Cancel anytime.", 8, MUTE, "hind", 600, "middle"))))
a("Mix", "Grouping: Two Short Rows (People, Then Promises), Or One Mixed Row?",
  opt("tto_rows", "Two Rows By Theme", "People: Certified, Checked, Licensed.", "practical", card("Badge Rows", JUNGLE, phdr(30)[0] + t(24, 80, "Your Home,", 19, INK, "khand", 700) + t(24, 99, "Taken Care Of.", 19, INK, "khand", 700) + t(24, 118, "PEOPLE", 7.5, MUTE, "hind", 600, 'letter-spacing="1.2"') + chipset(24, 122, ["Certified Techs", "Background-Checked Yearly", "Licensed & Insured"], 192)[0] + t(24, 172, "PROMISES", 7.5, MUTE, "hind", 600, 'letter-spacing="1.2"') + chipset(24, 176, ["Cancel Anytime", "Home Reports", "Moisture Scan Every Visit"], 192)[0] + rect(14, 30, 212, 240, "none", "#BDB6AA", 0, 1))),
  opt("tto_mixed", "One Mixed Row", "All six in one wrapping row.", "calm", TH("Badge Rows", TERRA, ["Certified Techs", "Cancel Anytime", "Background-Checked Yearly", "Home Reports", "Licensed & Insured", "Moisture Scan Every Visit"])))
# ================= Trust Tags: Chip Look And Heading (follow-on to Wording & Style) =================
TW = []
def b(g, ask, x, y): TW.append((g, ask, x, y))
FIVE = ["Certified Techs", "Cancel Anytime", "Home Reports", "Background-Checked Yearly", "Licensed & Insured"]
b("Count", "Five Chips: One Row You Swipe Sideways, Or Wrapped Onto Two Lines?",
  opt("ttw_swipe", "One Swipe Row", "One line, the rest peek at the edge.", "calm", TH("Five Chips", LAGOON, FIVE, wrap_=False)),
  opt("ttw_wrap", "Two Lines", "All five visible at once.", "practical", TH("Five Chips", TERRA, FIVE)))
b("Style", "Soft Tints: Four Brand Tints Taking Turns, Or One Tint Per Theme (People, Promise, Proof)?",
  opt("ttw_turns", "Four Tints In Turn", "Today's soft rainbow.", "playful", TH("Chip Tints", SAFFRON, FIVE)),
  opt("ttw_theme", "One Tint Per Theme", "People lagoon, promise terracotta, proof jungle.", "calm", TH("Chip Tints", JUNGLE, FIVE, colors=[TERRA, TERRA, JUNGLE, LAGOON, LAGOON])))
b("Style", "Pill Size: Compact Pills, Or Roomier Pills With Bigger Words?",
  opt("ttw_small", "Compact", "Fits more, quieter.", "calm", TH("Pill Size", LAGOON, FIVE)),
  opt("ttw_big", "Roomy", "Easier to read on a phone.", "bold", TH("Pill Size", TERRA, FIVE[:4], big=True)))
b("Style", "Inside Each Pill: A Small Leading Dot, Or A Check Mark?",
  opt("ttw_dot", "Leading Dot", "A tiny color dot before the words.", "calm", TH("Pill Mark", LAGOON, FIVE, icon_="dot")),
  opt("ttw_chk", "Check Mark", "Reads as 'yes, we do this'.", "practical", TH("Pill Mark", JUNGLE, FIVE, icon_="check")))
b("Heading", "'Why Trust Us' Heading: Left-Aligned Over The Chips, Or Centered?",
  opt("ttw_left", "Left-Aligned", "Lines up with the headline.", "calm", TH("Heading Spot", TERRA, FIVE)),
  opt("ttw_center", "Centered", "Sits like a small title.", "premium", TH("Heading Spot", LAGOON, FIVE, head_center=True)))
b("Heading", "'Why Trust Us' Look: Small Grey Caps Label, Or A Real Headline In Khand?",
  opt("ttw_lbl", "Small Caps Label", "Quiet, the chips do the work.", "calm", TH("Heading Look", INK, FIVE)),
  opt("ttw_head", "Headline", "Bigger, makes it a section.", "bold", TH("Heading Look", TERRA, FIVE, head_style="headline")))
b("Style", "Chip Word Color: Ink Words On The Tint, Or Words In The Tint's Darker Color?",
  opt("ttw_ink", "Ink Words", "Highest contrast, easiest to read.", "practical", TH("Word Color", INK, FIVE)),
  opt("ttw_tone", "Matching Color", "Softer, one color family per chip.", "calm", TH("Word Color", LAGOON, FIVE, dark=True)))
b("Count", "Five Chips Or All Six Approved (Adding 'Moisture Scan Every Visit')?",
  opt("ttw_five", "Five Chips", "Your pick from last round.", "calm", TH("Chip Count", TERRA, FIVE)),
  opt("ttw_sixb", "All Six", "Adds the moisture scan proof.", "bold", TH("Chip Count", JUNGLE, FIVE + ["Moisture Scan Every Visit"])))
b("Style", "Chip Edge: No Border, Or A Thin Border In The Chip's Color?",
  opt("ttw_nob", "No Border", "Soft fill only.", "calm", TH("Chip Edge", LAGOON, FIVE)),
  opt("ttw_bor", "Thin Border", "Crisper on white.", "practical", TH("Chip Edge", TERRA, FIVE, border=True)))
def plans_page():
    s, h = phdr(30); y = 62
    s += t(24, y + 14, "Plans", 17, INK, "khand", 700) + at([("card", "Essentials", "Starting at $99/Month (site)", TERRA), ("card", "Plus", "4 seasonal visits", LAGOON)], y + 22)
    s += t(24, y + 118, "WHY TRUST US", 7.5, MUTE, "hind", 600, 'letter-spacing="1.2"') + chipset(24, y + 124, FIVE, 192)[0]
    return s + rect(14, 30, 212, 240, "none", "#BDB6AA", 0, 1)
b("Placement", "'Why Trust Us' Row: On The Home Page Only, Or Repeated On The Plans Page Too?",
  opt("ttw_home", "Home Only", "Said once, where people land.", "calm", TH("Row Placement", TERRA, FIVE)),
  opt("ttw_plans", "Plans Page Too", "Seen again next to the prices.", "practical", card("Row Placement", LAGOON, plans_page())))
# ================= Sign Up Form: Fields, Errors And Summary (follow-on to Policies & Summary) =================
SU = []
def c(g, ask, x, y): SU.append((g, ask, x, y))
def field(y, label, val="", state="ok", lab="above", err="under"):
    s = ""
    if lab == "above": s += t(14, y + 8, label, 7.5, INK, "hind", 600); y += 12
    bc = TERRA if state == "err" else "#BDB6AA"
    s += rect(14, y, 212, 24, "#FFFFFF", bc, 3, 1.4 if state == "err" else 1)
    s += t(22, y + 16, val if val else (label if lab == "inside" else ""), 8.5, INK if val else "#9A948A")
    h = 30 + (12 if lab == "above" else 0)
    if state == "err" and err == "under": s += t(14, y + 34, "Please enter a valid email.", 7.5, TERRA, "hind", 600); h += 10
    return s, h
def form(lab="above", err_state=None, err_pos="under", head="Your Details"):
    s = phdr(30)[0] + t(14, 74, head, 15, INK, "khand", 700); y = 82
    if err_pos == "above" and err_state: s += t(14, y + 8, "Please enter a valid email.", 7.5, TERRA, "hind", 600); y += 12
    for nm, v, st in [("Full Name", "Max Example", "ok"), ("Email", "max@", err_state or "ok"), ("Phone", "", "ok"), ("Home Address", "", "ok")]:
        g_, h = field(y, nm, v, st, lab, err_pos if err_pos == "under" else "none"); s += g_; y += h
    return s + rect(14, 236, 212, 26, TERRA) + t(120, 253, "CONTINUE", 8.5, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
c("Order Form", "Re-Ask, Form Labels: A Small Label Over Each Box, Or Grey Hint Words Inside The Box?",
  opt("suf_above", "Label Over The Box", "Label stays put while you type.", "practical", card("Field Labels", TERRA, form("above"), True)),
  opt("suf_inside", "Hint Inside The Box", "Shorter form, hint fades as you type.", "calm", card("Field Labels", LAGOON, form("inside"), True)))
c("Order Form", "Red Box Errors: Show When You Leave A Field, Or Only When You Tap Continue?",
  opt("sue_leave", "When You Leave A Field", "Fix it right away.", "practical", card("Error Timing", TERRA, form("above", "err") + t(226, 74, "on leaving Email", 7.5, MUTE, "hind", 400, "end"), True)),
  opt("sue_submit", "On Continue", "No red while you are still typing.", "calm", card("Error Timing", LAGOON, form("above", "err") + t(226, 74, "after Continue", 7.5, MUTE, "hind", 400, "end"), True)))
c("Order Form", "Error Message Spot: Under The Red Box, Or Above It Next To The Label?",
  opt("sup_under", "Under The Box", "Reads after the field, like most forms.", "calm", card("Error Spot", TERRA, form("above", "err", "under"), True)),
  opt("sup_above", "Above, By The Label", "Seen before your eye reaches the box.", "practical", card("Error Spot", LAGOON, form("above", "err", "above"), True)))
def agree(progress):
    s = phdr(30)[0] + t(14, 74, "Membership Agreement", 14, INK, "khand", 700) + rect(14, 82, 212, 120, "#FFFFFF", "#BDB6AA", 3) + "".join(rect(22, 92 + i * 10, 190 - (i % 3) * 22, 4, LINE) for i in range(10))
    if progress: s += rect(220, 86, 3, 112, LINE) + rect(220, 86, 3, 40, TERRA) + t(226, 214, "Scroll to the end to sign (1 of 3)", 7.5, MUTE, "hind", 400, "end")
    s += rect(14, 220, 12, 12, "#FFFFFF", "#BDB6AA", 2) + t(32, 230, "I agree to the membership terms", 8, INK)
    return s + rect(14, 240, 212, 24, TERRA if not progress else "#D6D0C6") + t(120, 256, "SIGN", 8.5, "#FFFFFF", "hind", 600, "middle")
c("Order Form", "Tall Agreement Box: A Small Scroll Bar Showing How Far You've Read, Or A Plain Box?",
  opt("sua_prog", "Scroll Progress", "Sign unlocks at the end.", "practical", card("Agreement Box", TERRA, agree(True))),
  opt("sua_plain", "Plain Box", "Read as much as you like, then sign.", "calm", card("Agreement Box", LAGOON, agree(False))))
def cancel(kind):
    s = phdr(30)[0] + t(14, 74, "Before You Sign", 14, INK, "khand", 700)
    if kind == "row": s += rect(14, 84, 212, 30, "#FFFFFF", LINE, 4) + t(24, 103, "Cancel Policy", 10, INK, "khand", 700) + ic("down", 200, 91, 14, INK)
    else: s += t(14, 100, "Read the cancel policy", 8.5, LAGOON, "hind", 600, 'text-decoration="underline"')
    s += rect(14, 124, 212, 50, SOFT) + t(22, 140, "Michigan 3-Day Cancel Notice", 9, INK, "khand", 700) + t(22, 152, "Shown beside your signature, as live.", 7.5, MUTE)
    return s + rect(14, 184, 212, 40, "#FFFFFF", "#BDB6AA") + t(22, 208, "Sign here", 9, "#9A948A") + rect(14, 236, 212, 26, TERRA) + t(120, 253, "COMPLETE SIGN UP", 8.5, "#FFFFFF", "hind", 600, "middle")
c("Trust", "Folded Cancel Policy: A Card Row With A Chevron, Or A Plain Underlined Link?",
  opt("suc_row", "Card Row + Chevron", "Clearly tappable, opens in place.", "practical", card("Cancel Policy", TERRA, cancel("row"))),
  opt("suc_link", "Underlined Link", "Lighter; one line of text.", "calm", card("Cancel Policy", LAGOON, cancel("link"))))
def notice(kind):
    s = phdr(30)[0] + t(14, 74, "Sign", 14, INK, "khand", 700) + rect(14, 84, 130, 50, "#FFFFFF", "#BDB6AA") + t(22, 112, "Sign here", 9, "#9A948A")
    if kind == "box": s += rect(150, 84, 76, 70, SAFFRON + "14", SAFFRON, 3) + t(156, 98, "3-DAY CANCEL", 7.5, "#7A5A0C", "hind", 600) + t(156, 110, "Michigan notice:", 7.5, INK) + t(156, 120, "you may cancel", 7.5, INK) + t(156, 130, "within 3 business", 7.5, INK) + t(156, 140, "days (as on site).", 7.5, INK)
    else: s += t(150, 96, "Michigan 3-day cancel", 7.5, MUTE) + t(150, 106, "notice applies (as", 7.5, MUTE) + t(150, 116, "on the live form).", 7.5, MUTE)
    return s + rect(14, 236, 212, 26, TERRA) + t(120, 253, "COMPLETE SIGN UP", 8.5, "#FFFFFF", "hind", 600, "middle")
c("Trust", "3-Day Cancel Notice Beside The Signature: In A Tinted Box, Or As Plain Small Text?",
  opt("sun_box", "Tinted Box", "Stands out; hard to miss.", "practical", card("Cancel Notice", SAFFRON, notice("box"))),
  opt("sun_plain", "Plain Small Text", "Calm; still beside the signature.", "calm", card("Cancel Notice", INK, notice("plain"))))
def summary(tag):
    s = phdr(30)[0] + t(14, 74, "Summary", 15, INK, "khand", 700)
    rows = [("Essentials plan", "$XX/mo", ""), ("Custom Grass Cutting", "+$X/mo", ""), ("Window Cleaning", "+$X/mo", ""), ("Gutter clean-out", "$XX", "ONE-TIME")]
    y = 84
    for nm, v, tg in rows:
        s += t(14, y + 12, nm, 9, INK, "hind", 500) + t(226, y + 12, v, 8.5, INK, "hind", 600, "end")
        if tg and tag: s += rect(120, y + 3, 44, 12, SAFFRON + "26", "none", 6) + t(142, y + 12, tg, 6.5, "#7A5A0C", "hind", 600, "middle")
        s += ln(y + 19); y += 24
    s += t(14, y + 18, "Due At Sign Up", 11, INK, "khand", 700) + t(226, y + 18, "$XXX", 13, INK, "khand", 700, "end") + t(226, y + 30, "about $XX/mo", 7.5, MUTE, "hind", 400, "end")
    return s
c("Order Form", "Last-Minute Jobs Mixed With Extras In The Summary: Mark Them With A 'One-Time' Tag, Or No Tag?",
  opt("sus_tag", "'One-Time' Tag", "Shows which lines don't repeat monthly.", "practical", card("Summary", SAFFRON, summary(True), True)),
  opt("sus_none", "No Tag", "Cleaner list; the price says it.", "calm", card("Summary", INK, summary(False), True)))
def due(kind):
    s = phdr(30)[0] + t(14, 74, "Due At Sign Up", 14, INK, "khand", 700)
    if kind == "stack": s += t(14, 120, "$XXX", 34, INK, "khand", 700) + t(14, 138, "That's about $XX a month.", 9, MUTE)
    else: s += rect(14, 90, 103, 60, SOFT) + t(22, 104, "TODAY", 7.5, MUTE, "hind", 600) + t(22, 132, "$XXX", 22, INK, "khand", 700) + rect(123, 90, 103, 60, SOFT) + t(131, 104, "PER MONTH", 7.5, MUTE, "hind", 600) + t(131, 132, "~$XX", 22, INK, "khand", 700)
    return s + rect(14, 236, 212, 26, TERRA) + t(120, 253, "CONTINUE", 8.5, "#FFFFFF", "hind", 600, "middle")
c("Order Form", "'Due At Sign Up' With The Monthly Number: Big Total With Monthly In Grey Under It, Or Two Boxes Side By Side?",
  opt("sud_stack", "Total, Monthly Under", "One big number, a helper line.", "calm", card("Due At Sign Up", TERRA, due("stack"), True)),
  opt("sud_side", "Two Boxes", "Today and per month, equal weight.", "practical", card("Due At Sign Up", LAGOON, due("side"), True)))
def refcode(kind):
    s = phdr(30)[0] + t(14, 74, "Referral Code", 14, INK, "khand", 700) + rect(14, 84, 212, 26, "#FFFFFF", JUNGLE, 3, 1.4) + t(22, 101, "NEIGHBOR-XXXX", 9, INK, "hind", 600)
    if kind == "line": s += f'<path d="M18 124 l3 3 6 -6" fill="none" stroke="{JUNGLE}" stroke-width="1.8"/>' + t(32, 128, "Code applied.", 8.5, JUNGLE, "hind", 600)
    else: s += rect(150, 88, 70, 18, JUNGLE, "none", 9) + t(185, 100, "APPLIED", 7.5, "#FFFFFF", "hind", 600, "middle")
    return s + rect(14, 236, 212, 26, TERRA) + t(120, 253, "CONTINUE", 8.5, "#FFFFFF", "hind", 600, "middle")
c("Order Form", "Referral Code Checked Right Away: A Green 'Code Applied' Line Under The Box, Or An 'Applied' Badge Inside It?",
  opt("sur_line", "Line Under The Box", "Plain words, easy to read.", "calm", card("Referral Code", JUNGLE, refcode("line"), True)),
  opt("sur_badge", "Badge Inside", "Compact; the box itself confirms.", "practical", card("Referral Code", LAGOON, refcode("badge"), True)))
def popup(kind):
    s = phdr(30)[0] + t(14, 74, "Your Plan: Essentials", 14, INK, "khand", 700) + at([("card", "Seasonal visits", "Included", JUNGLE)], 84)
    if kind == "sheet": s += rect(14, 140, 212, 130, "#0A0A0A33") + rect(14, 156, 212, 114, "#FFFFFF") + rect(104, 162, 32, 3, "#D6D0C6") + t(26, 186, "Add Chimney Sweep?", 12, INK, "khand", 700) + t(26, 200, "Next in the list of six extras.", 7.5, MUTE) + rect(26, 214, 90, 22, TERRA) + t(71, 229, "ADD", 8, "#FFFFFF", "hind", 600, "middle") + t(160, 229, "Not now", 8, LAGOON, "hind", 600, "middle")
    else: s += rect(14, 132, 212, 64, SAFFRON + "12", SAFFRON, 4) + t(24, 152, "Add Chimney Sweep?", 11, INK, "khand", 700) + t(24, 164, "Next in the list of six extras.", 7.5, MUTE) + rect(24, 172, 60, 18, TERRA) + t(54, 184, "ADD", 7.5, "#FFFFFF", "hind", 600, "middle") + t(110, 184, "Not now", 7.5, LAGOON, "hind", 600) + rect(14, 236, 212, 26, TERRA) + t(120, 253, "CONTINUE", 8.5, "#FFFFFF", "hind", 600, "middle")
    return s
c("Add-On Upsell", "Extra Offered In Turn (Windows, Chimney, Radon...): A Bottom Sheet, Or A Card Inside The Page?",
  opt("suu_sheet", "Bottom Sheet", "Slides up; clear yes or not now.", "bold", card("Extra Offer", TERRA, popup("sheet"))),
  opt("suu_card", "Card In The Page", "Sits in the flow, never blocks.", "calm", card("Extra Offer", SAFFRON, popup("card"))))
# ================= What We Take Care Of: Grid And Home Map (follow-on) =================
import uk5_wwtco as W
WW = []
def d(g, ask, x, y): WW.append((g, ask, x, y))
def gridcard(label, acc, style="icon", cols=2, extra="", heading=True, sub=False, lawn_banner=True, items=None):
    items = items or W.CORE; s = ""
    y0 = 36
    if heading: s += t(14, y0 + 14, "What We Take Care Of", 15, INK, "khand", 700); y0 += 20
    if sub: s += t(14, y0 + 6, "Every plan covers these, visit after visit.", 7.5, MUTE); y0 += 14
    w = (212 - (cols - 1) * 5) / cols; h = 34 if cols == 2 else 40
    for i, (k, nm) in enumerate(items):
        x, yy = 14 + (i % cols) * (w + 5), y0 + (i // cols) * (h + 5); c = W.ACC4[i % 4]
        if style == "icon": s += rect(x, yy, w, h, "#FFFFFF", LINE) + rect(x + 5, yy + 5, h - 10, h - 10, c + "1F") + icon(k, x + 7, yy + 7, h - 14, c, 2) + t(x + h + 1, yy + h / 2 + 3.5, nm, 8.5 if cols == 2 else 7.5, INK, "khand", 700)
        else: s += rect(x, yy, w, h, "#FFFFFF", LINE) + rect(x, yy, 3, h, c) + t(x + 9, yy + h / 2 + 3.5, nm, 8.5 if cols == 2 else 7.5, INK, "khand", 700)
    yb = y0 + math.ceil(len(items) / cols) * (h + 5) + 2
    if lawn_banner: s += rect(14, yb, 212, 30, "#F4F8EF", JUNGLE + "55") + icon("lawn", 20, yb + 7, 16, JUNGLE, 2) + t(42, yb + 13, "Custom Grass Cutting", 9, INK, "khand", 700) + rect(170, yb + 6, 48, 12, JUNGLE + "22") + t(194, yb + 15, "ADD-ON", 6.5, JUNGLE, "hind", 600, "middle") + t(42, yb + 24, "One add-on, booked with your plan.", 7.5, MUTE); yb += 36
    return card(label, acc, s + extra)
d("Visual Style", "Tile Visuals, Asked New: Simple Line Icons, Or Plain Tiles With A Color Edge?",
  opt("ww_icons", "Line Icons", "A small drawn icon per service.", "calm", gridcard("Tile Visuals", TERRA, "icon")),
  opt("ww_edge", "Color Edge, No Icon", "Words only, a brand-color edge.", "practical", gridcard("Tile Visuals", LAGOON, "edge")))
d("Grouping", "Grouping, Asked New: No Groups At All, Or 'Every Visit' Items First, Then The Rest?",
  opt("ww_nogrp", "No Groups", "Eight tiles, one simple grid.", "calm", gridcard("Grouping", TERRA)),
  opt("ww_every", "'Every Visit' First", "Moisture scan leads, marked Every Visit.", "practical", gridcard("Grouping", JUNGLE, items=[W.CORE[5]] + W.CORE[:5] + W.CORE[6:], extra=rect(60, 60, 52, 11, JUNGLE) + t(86, 68, "EVERY VISIT", 6.5, "#FFFFFF", "hind", 600, "middle"))))
def season_strip(y):
    s = ""
    for i, (nm, c, it) in enumerate([("Fall", TERRA, "Furnace"), ("Winter", LAGOON, "Ice Dams"), ("Spring", JUNGLE, "AC"), ("Summer", SAFFRON, "Grass")]):
        x = 14 + i * 54; s += rect(x, y, 50, 40, "#FFFFFF", LINE) + rect(x, y, 50, 3, c) + t(x + 6, y + 18, nm, 9, c, "khand", 700) + t(x + 6, y + 30, it, 6.5, MUTE)
    return s
d("Layout", "Grid And Seasons Together: Grid On Top With A Season Strip Under It, Or A Grid / By Season Switch?",
  opt("ww_both", "Grid + Season Strip", "Both views, nothing hidden.", "practical", card("Layout", TERRA, t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + "".join(rect(14 + (i % 4) * 54, 58 + (i // 4) * 46, 50, 42, "#FFFFFF", LINE) + rect(18 + (i % 4) * 54, 62 + (i // 4) * 46, 16, 16, W.ACC4[i % 4] + "1F") + icon(k, 19 + (i % 4) * 54, 63 + (i // 4) * 46, 14, W.ACC4[i % 4], 2) + t(18 + (i % 4) * 54, 94 + (i // 4) * 46, nm[:11], 7.5, INK, "khand", 700) for i, (k, nm) in enumerate(W.CORE)) + t(14, 166, "BY SEASON", 7.5, MUTE, "hind", 600, 'letter-spacing="1"') + season_strip(172))),
  opt("ww_switch", "Grid / Season Switch", "One view at a time, flip with tabs.", "calm", card("Layout", LAGOON, at([("tabs", ["Grid", "By Season"])], 36) + gridcard("x", LAGOON, heading=False, lawn_banner=False).split('<text x="14" y="22"', 1)[0][0:0] + "".join(rect(14 + (i % 2) * 108, 72 + (i // 2) * 39, 103, 34, "#FFFFFF", LINE) + rect(19 + (i % 2) * 108, 77 + (i // 2) * 39, 24, 24, W.ACC4[i % 4] + "1F") + icon(k, 21 + (i % 2) * 108, 79 + (i // 2) * 39, 20, W.ACC4[i % 4], 2) + t(49 + (i % 2) * 108, 92 + (i // 2) * 39, nm, 8.5, INK, "khand", 700) for i, (k, nm) in enumerate(W.CORE)))))
def housemap(y, pins=True, h=118):
    s = rect(14, y, 212, h, CREAM) + f'<path d="M40 {y+h-10} V{y+46} L120 {y+12} L200 {y+46} V{y+h-10} Z" fill="#FFFFFF" stroke="{INK}" stroke-width="1.4"/>' + f'<path d="M40 {y+76} H200 M120 {y+46} V{y+h-10}" stroke="{LINE}" stroke-width="1.2"/>'
    if pins:
        for i, (x, yy) in enumerate([(80, y + 60), (160, y + 60), (80, y + 92), (160, y + 92), (120, y + 30)]):
            s += f'<circle cx="{x}" cy="{yy}" r="7" fill="{W.ACC4[i % 4]}"/>' + t(x, yy + 3, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle")
    return s
d("Layout", "House Map Plus System Cards: Map On Top, Tap A Pin To Jump To Its Card, Or The Map In Its Own Tab?",
  opt("ww_mapjump", "Map Top, Pins Jump", "Map and cards on one page.", "practical", card("House Map", TERRA, t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + housemap(58) + at([("card", "1  Heating & Cooling", "Furnace, AC", TERRA), ("card", "2  Water", "Water heater, leaks", LAGOON)], 182))),
  opt("ww_maptab", "Map In Its Own Tab", "Cards stay the main view.", "calm", card("House Map", LAGOON, at([("tabs", ["Cards", "House Map"])], 36) + at([("card", "Heating & Cooling", "Furnace, AC", TERRA), ("card", "Water", "Water heater, leaks", LAGOON), ("card", "Air & Safety", "Smoke/CO, dryer vent, moisture", JUNGLE), ("card", "Outside", "Gutters, roof", SAFFRON)], 72))))
d("Tap To Expand", "Opening In Place: Only One Item Open At A Time, Or Several Open At Once?",
  opt("ww_one", "One At A Time", "Opening one closes the last.", "calm", card("Open In Place", TERRA, t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + at([("card", "Furnace", "", TERRA, "-")], 58) + rect(14, 96, 212, 46, SOFT) + t(22, 112, "Furnace Tune-Up and Furnace Filters", 7.5, INK) + t(22, 123, "on the fall visit (from the site).", 7.5, INK) + at([("card", "AC", "", LAGOON, "+"), ("card", "Water Heater", "", JUNGLE, "+"), ("card", "Dryer Vent", "", SAFFRON, "+")], 148))),
  opt("ww_many", "Several At Once", "Compare items side by side.", "practical", card("Open In Place", LAGOON, t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + at([("card", "Furnace", "", TERRA, "-")], 58) + rect(14, 96, 212, 30, SOFT) + t(22, 114, "Furnace Tune-Up and filters, fall visit.", 7.5, INK) + at([("card", "AC", "", LAGOON, "-")], 130) + rect(14, 168, 212, 30, SOFT) + t(22, 186, "AC Tune-Up on the spring visit.", 7.5, INK) + at([("card", "Water Heater", "", JUNGLE, "+")], 202))))
d("Add-On", "Grass Cutting Banner: The Site's Lawn Line With An 'Add-On' Tag, Or With An 'Add To My Plan' Button?",
  opt("ww_lawntag", "Lawn Line + Tag", "Informs; booking stays in sign up.", "calm", gridcard("Lawn Add-On", JUNGLE)),
  opt("ww_lawnbtn", "With A Button", "One add-on, one tap to add it.", "practical", card("Lawn Add-On", TERRA, gridcard("x", TERRA, lawn_banner=False)[0:0] + t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + "".join(rect(14 + (i % 2) * 108, 58 + (i // 2) * 39, 103, 34, "#FFFFFF", LINE) + t(22 + (i % 2) * 108, 79 + (i // 2) * 39, nm, 8.5, INK, "khand", 700) for i, (k, nm) in enumerate(W.CORE)) + rect(14, 216, 212, 46, "#F4F8EF", JUNGLE + "55") + icon("lawn", 22, 226, 16, JUNGLE, 2) + t(44, 232, "Custom Grass Cutting", 9.5, INK, "khand", 700) + t(44, 244, "One add-on with your plan.", 7.5, MUTE) + rect(160, 226, 58, 22, JUNGLE) + t(189, 240, "ADD", 8, "#FFFFFF", "hind", 600, "middle"))))
d("Layout", "Eight Core Tiles On Desktop: Two Rows Of Four, Or Four Rows Of Two?",
  opt("ww_four", "Two Rows Of Four", "Wide and short on a laptop.", "practical", gridcard("Tile Grid", TERRA, cols=4)),
  opt("ww_two", "Four Rows Of Two", "Same grid as the phone.", "calm", gridcard("Tile Grid", LAGOON, cols=2)))
def rec_tile(kind):
    s = gridcard("x", LAGOON, lawn_banner=False)
    body = t(14, 50, "What We Take Care Of", 15, INK, "khand", 700) + "".join(rect(14 + (i % 2) * 108, 58 + (i // 2) * 39, 103, 34, "#FFFFFF", LINE) + t(22 + (i % 2) * 108, 79 + (i // 2) * 39, nm, 8.5, INK, "khand", 700) for i, (k, nm) in enumerate(W.CORE))
    if kind == "tile": body += rect(14, 216, 212, 46, "#FFFFFF", LAGOON) + t(22, 234, "Records", 10, INK, "khand", 700) + rect(22, 242, 76, 12, LAGOON + "1A", "none", 6) + t(60, 251, "Recall Monitoring", 6.5, LAGOON, "hind", 600, "middle") + rect(102, 242, 70, 12, LAGOON + "1A", "none", 6) + t(137, 251, "Warranty Check", 6.5, LAGOON, "hind", 600, "middle")
    else: body += t(14, 228, "ALSO ON EVERY PLAN", 7.5, MUTE, "hind", 600, 'letter-spacing="1"') + rect(14, 236, 96, 16, LAGOON + "1A", "none", 8) + t(62, 247, "Recall Monitoring", 7.5, LAGOON, "hind", 600, "middle") + rect(116, 236, 88, 16, LAGOON + "1A", "none", 8) + t(160, 247, "Warranty Check", 7.5, LAGOON, "hind", 600, "middle")
    return body
d("Trust Badges", "Recall Monitoring And Warranty Check: As A 'Records' Tile Of Its Own, Or Two Badges Under The Grid?",
  opt("ww_rectile", "A 'Records' Tile", "Badges live on the Records tile.", "practical", card("Records Badges", LAGOON, rec_tile("tile"))),
  opt("ww_recrow", "Badges Under The Grid", "'Also on every plan' line.", "calm", card("Records Badges", JUNGLE, rec_tile("row"))))
def pinned(kind):
    body = t(14, 50, "What We Take Care Of", 15, INK, "khand", 700)
    for i, (k, nm) in enumerate(W.CORE):
        x, yy = 14 + (i % 2) * 108, 58 + (i // 2) * 46
        body += rect(x, yy, 103, 41, "#FFFFFF", LINE) + t(x + 8, yy + 17, nm, 8.5, INK, "khand", 700)
        if nm == "Mold & Moisture":
            if kind == "corner": body += rect(x + 60, yy + 4, 39, 11, JUNGLE) + t(x + 79.5, yy + 12, "EVERY VISIT", 5.8, "#FFFFFF", "hind", 600, "middle")
            else: body += t(x + 8, yy + 31, "Moisture Scan Every Visit", 6.8, JUNGLE, "hind", 600)
    return body + rect(14, 246, 212, 20, SOFT) + t(120, 259, "Certified Techs  ·  Licensed & Insured", 7.5, INK, "hind", 600, "middle")
d("Trust Badges", "Badge Pinned To Its Tile: A Small Corner Tag, Or A Line Under The Tile Name?",
  opt("ww_corner", "Corner Tag", "Like a sticker on the tile.", "playful", card("Pinned Badge", JUNGLE, pinned("corner"))),
  opt("ww_line", "Line Under The Name", "Reads as part of the tile.", "calm", card("Pinned Badge", LAGOON, pinned("line"))))
d("Heading", "Section Top: 'What We Take Care Of' With A One-Line Subhead, Or The Heading Alone?",
  opt("ww_sub", "Heading + Subhead", "One line on what every plan covers.", "practical", gridcard("Section Top", TERRA, sub=True)),
  opt("ww_alone", "Heading Alone", "Straight into the tiles.", "calm", gridcard("Section Top", INK)))
DECKS = [
 D("upkeep-trust-tags-order-and-placement-deck", "Trust Tags: Order And Placement", "trust-tags-order-placement", "futo_", "upkeep-home-page-trust-tags-deck-theme-current-vs-new",
   "Follow-on to Trust Tags: Theme & Current Vs New (8/10, 08:52 ICT). Only the six approved badges. Both skips re-asked (safety badge, proof vs promise first), plus his 'random order' note.",
   "Approved badges only: re-asks both skips, then lead badge, count, random vs fixed order, check marks, tap-to-explain, row spot, Cancel Anytime placement, theme rows.", "Home Page", TO, ["upkeep-home-page-trust-tags-deck-theme-current-vs-new-08", "upkeep-home-page-trust-tags-deck-theme-current-vs-new-10"], "upkeep-home-page-trust-tags-deck-theme-current-vs-new-20261017-0852-0a98ec3a.json"),
 D("upkeep-trust-tags-chip-look-and-heading-deck", "Trust Tags: Chip Look And Heading", "trust-tags-chip-look", "futc_", "upkeep-home-page-trust-tags-deck-wording-style",
   "Follow-on to Trust Tags: Wording & Style (10/10, 08:58 ICT): five chips, soft tints, pills and the 'Why Trust Us' heading he picked, refined. Approved badges only.",
   "Refines five soft-tint pills and 'Why Trust Us': swipe vs wrap, tint scheme, size, dot vs check, heading spot and look, word color, five vs six, border, Plans page.", "Home Page", TW, [], "upkeep-home-page-trust-tags-deck-wording-style-20261017-0858-46440b50.json"),
 D("upkeep-sign-up-form-fields-errors-and-summary-deck", "Sign Up Form: Fields, Errors And Summary", "sign-up-form-fields-errors", "fusu_", "upkeep-order-form-sign-up-form-deck-policies-summary",
   "Follow-on to Sign Up Form: Policies & Summary (9/10, 09:04 ICT): field-label skip re-asked, then red-box error timing and spot, tall agreement box, folded cancel policy, 3-day notice, summary tags, due-at-sign-up, referral check, extras offer.",
   "Re-asks field labels, then error timing/spot, agreement scroll, cancel policy row, 3-day notice box, one-time tags, due-at-sign-up layout, referral check, extra offer style.", "Order Form", SU, ["upkeep-order-form-sign-up-form-deck-policies-summary-09"], "upkeep-order-form-sign-up-form-deck-policies-summary-20261017-0904-99a58243.json"),
 D("upkeep-what-we-take-care-of-grid-and-home-map-deck", "What We Take Care Of: Grid And Home Map", "what-we-take-care-of-grid-map", "fuww_", "upkeep-what-we-take-care-of-deck",
   "Follow-on to What We Take Care Of Deck (10/10, 12:01 ICT): site-backed items only, lawn cutting stays one add-on. New tile-visual and grouping options (he said neither), grid+seasons and map+cards combos (he said both), accordion, badges.",
   "New tile-visual and grouping options after his two 'neither's, grid+season and map+card combos, accordion, lawn banner, desktop grid, Records badges, pinned badge look.", "Home Page", WW, [], "upkeep-what-we-take-care-of-deck-20261017-1201-418b7639.json"),
]
