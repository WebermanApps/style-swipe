"""UpKeep follow-ons A (Oct 17 2026): Phone Home Top Section, Clear Picks: App Header & Video, Clear Picks: Menus & Headlines."""
from fu1017_kit import *
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
BADGES = ["Certified Techs", "Cancel Anytime", "Home Reports", "Background-Checked Yearly", "Moisture Scan Every Visit", "Licensed & Insured"]
def D(id, name, slug_key, prefix, follows, about, summary, tag, pairs, reasked=(), inbox=""):
    return dict(id=id, name=name, slug_key=slug_key, prefix=prefix, app="UpKeep", agent="upkeep", submit_to=UPKEEP, board="upkeep", topic=slug_key,
                follows=follows, about=about, summary=summary, tag=tag, pairs=pairs, reasked=list(reasked), agent_inbox="upkeep/" + inbox,
                brands=["Smart Upkeep brand: white and cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only. Trust badges: approved set only."])
# ---------------- phone hero drawing (screen drawn at card scale, x 14..226) ----------------
def video(x, y, w, h, sound=False, play=True):
    s = rect(x, y, w, h, "#DCE9EF") + rect(x, y + h * .62, w, h * .38, "#CFE0C8")
    s += photo(x + w * .18, y + h * .12, w * .5, h * .66, LAGOON, "house", 0)
    s += rect(x + w * .66, y + h * .5, w * .26, h * .2, "#FFFFFF", TERRA, 0, 1) + dot(x + w * .71, y + h * .72, 2.5, INK) + dot(x + w * .87, y + h * .72, 2.5, INK)
    if play: s += f'<circle cx="{x+12}" cy="{y+h-11}" r="6" fill="#FFFFFFCC"/><path d="M{x+10} {y+h-14} L{x+15} {y+h-11} L{x+10} {y+h-8} Z" fill="{INK}"/>'
    if sound: s += rect(x + w - 26, y + 6, 20, 16, "#0A0A0A88") + ic("speaker", x + w - 23, y + 8, 12, "#FFFFFF", 1.8)
    return s
def phdr(y=30, slim=False):
    h = 18 if slim else 24
    return rect(14, y, 212, h, "#FFFFFF") + mark(26, y + h / 2, 6, "#FFFFFF", TERRA) + wordmark(36, y + h / 2 + 4, 11) + shareic(208, y + h / 2 - 6.5) + ln(y + h), h
def chiprow(x, y, items, w=212, wrap_=False, cols=None):
    s, xx, yy = "", x, y
    for i, it in enumerate(items):
        cw = len(it) * 3.9 + 10
        if xx + cw > x + w:
            if not wrap_: s += rect(x + w - 14, y, 14, 15, "#FFFFFFDD") + t(x + w - 4, y + 11, ">", 9, MUTE, "hind", 700, "end"); break
            xx, yy = x, yy + 19
        c = ACC[i % 4]; s += rect(xx, yy, cw, 15, c + "1A", "none", 7.5) + t(xx + cw / 2, yy + 10.4, it, 7.5, c, "hind", 600, "middle"); xx += cw + 4
    return s
def head(x, y, lines, size=20, accent=False, c=INK):
    s = ""
    for i, l in enumerate(lines):
        col = TERRA if (accent and i == len(lines) - 1) else c
        s += t(x, y + i * size * 1.05, l, size, col, "khand", 700)
    return s
def hero(video_mode="bleed", text_over=True, fade="bottom", size=22, accent=False, sub="Catch small problems early.", sub_on_video=True,
         cta="sticky", cta_text="Free Quote In Minutes", cta_style="fill", price=False, badges=None, chip_mode="carousel", sound=False, snug=False, sticky_late=False, head_pos="bottom"):
    s, h = phdr(30); y = 30 + h
    gap = 3 if snug else 18
    vh = 116 if snug else 128
    s += video(14, y, 212, vh, sound)
    if text_over:
        if fade == "bottom": s += f'<defs><linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></linearGradient></defs><rect x="14" y="{y+vh*.35}" width="212" height="{vh*.65}" fill="url(#fd)"/>'
        else: s += rect(14, y, 212, vh, "#0A0A0A66")
        hy = y + vh - (size * 2.1 + (14 if sub and sub_on_video else 4)) if head_pos == "bottom" else y + size + 8
        s += head(24, hy, ["Your Home,", "Taken Care Of."], size, accent, "#FFFFFF")
        if sub and sub_on_video: s += t(24, hy + size * 1.05 + 14, sub, 8.5, "#FFFFFFEE")
        y += vh + gap
        if sub and not sub_on_video: s += t(24, y + 10, sub, 9, MUTE); y += 18
    else:
        y += vh + gap
    if badges:
        if chip_mode == "carousel":
            s += chiprow(20, y, badges[:3], 206) + "".join(dot(108 + i * 8, y + 22, 2, TERRA if i == 0 else "#CFC6B4") for i in range(len(badges) // 2)); y += 30
        elif chip_mode == "ticker":
            s += chiprow(24, y, badges[2:] + badges[:2], 202) + f'<path d="M14 {y+7} h6 M220 {y+7} h6" stroke="{MUTE}"/>' + t(120, y + 26, "slowly slides on its own", 7.5, MUTE, "hind", 400, "middle"); y += 32
        else:
            s += chiprow(24, y, badges, 192, True); y += 44
    if cta == "inline":
        bw = len(cta_text) * 5.4 + 24
        s += rect(24, y, bw, 24, TERRA if cta_style == "fill" else "#FFFFFF", TERRA if cta_style == "fill" else INK, 0, 1.4) + t(24 + bw / 2, y + 15.5, cta_text.upper(), 8, "#FFFFFF" if cta_style == "fill" else INK, "hind", 600, "middle", 'letter-spacing=".8"'); y += 32
    if cta == "sticky":
        by = 236
        if sticky_late: s += t(120, by - 8, "bar slides up after the hero scrolls away", 7.5, MUTE, "hind", 400, "middle")
        s += rect(14, by, 212, 34, "#FFFFFF") + ln(by) + rect(24, by + 6, (120 if price else 192), 22, TERRA if cta_style == "fill" else "#FFFFFF", TERRA if cta_style == "fill" else INK, 0, 1.4)
        s += t(24 + (60 if price else 96), by + 20.5, cta_text.upper(), 8, "#FFFFFF" if cta_style == "fill" else INK, "hind", 600, "middle", 'letter-spacing=".6"')
        if price: s += t(150, by + 15, "Starting at", 7.5, MUTE) + t(150, by + 26, "$99/Month", 10, INK, "khand", 700)
    return s + rect(14, 30, 212, 240, "none", "#BDB6AA", 0, 1)
def HC(label, acc, foot=None, **k): return card(label, acc, hero(**k) + (chips(276, foot) if foot else ""))
B6 = BADGES
PH = []
def p(g, ask, a, b): PH.append((g, ask, a, b))
p("Density", "Re-Ask, Spacing: Airy Gaps Between Pieces, Or A Snug Stack So More Fits?",
  opt("phs_airy", "Airy Gaps", "More white space; price bar sits lower.", "calm", HC("Spacing", LAGOON, badges=B6, snug=False)),
  opt("phs_snug", "Snug Stack", "Tighter gaps; chips and CTA ride higher.", "practical", HC("Spacing", TERRA, badges=B6, snug=True)))
p("Trust", "Re-Ask, Badges In The Hero: A Swipe Carousel With Dots, Or A Slow Ticker That Moves On Its Own?",
  opt("phs_carousel", "Swipe Carousel + Dots", "All six approved badges, three at a time.", "calm", HC("Badge Carousel", LAGOON, badges=B6, chip_mode="carousel")),
  opt("phs_ticker", "Slow Ticker", "Badges drift sideways; no tapping needed.", "playful", HC("Badge Ticker", SAFFRON, badges=B6, chip_mode="ticker")))
p("Video", "Text On The Video: Dark Fade At The Bottom, Or A Light Dim Over The Whole Clip?",
  opt("phs_fadebot", "Bottom Fade", "Clip stays bright on top; words sit on the fade.", "premium", HC("Text Over Video", TERRA, fade="bottom")),
  opt("phs_fadeall", "Whole-Clip Dim", "Even dim everywhere; words can sit anywhere.", "bold", HC("Text Over Video", INK, fade="full")))
p("Headline", "Big Headline On The Video: Bottom-Left Corner, Or Up Top Under The Logo Bar?",
  opt("phs_hbot", "Bottom-Left", "Reads after the eye lands on the clip.", "calm", HC("Headline Spot", TERRA, size=24, head_pos="bottom", sub=None)),
  opt("phs_htop", "Up Top", "First thing you read, clip plays below it.", "bold", HC("Headline Spot", LAGOON, size=24, head_pos="top", sub=None)))
p("Headline", "Headline Color: All White On The Video, Or 'Taken Care Of.' In Terracotta?",
  opt("phs_hwhite", "All White", "One color, cleanest on a moving clip.", "calm", HC("Headline Color", INK, size=24)),
  opt("phs_hterra", "Terracotta Second Line", "Brand color on the promise line.", "bold", HC("Headline Color", TERRA, size=24, accent=True)))
p("Subhead", "Short Subhead: On The Video Under The Headline, Or Below The Video On White?",
  opt("phs_subon", "On The Video", "Headline and subhead read as one block.", "premium", HC("Subhead", LAGOON, sub_on_video=True)),
  opt("phs_subbelow", "Below On White", "Easier to read; clip stays cleaner.", "practical", HC("Subhead", TERRA, sub_on_video=False)))
p("CTA", "Sticky Bar: 'Free Quote In Minutes' Alone, Or With 'Starting At $99/Month' Beside It?",
  opt("phs_baronly", "Button Only", "One full-width action in the bar.", "calm", HC("Sticky Bar", TERRA, badges=B6[:3])),
  opt("phs_barprice", "Button + Site Price", "Uses the site's own 'Starting at $99/Month'.", "practical", HC("Sticky Bar", LAGOON, badges=B6[:3], price=True)))
p("CTA", "Sticky Bar Timing: Showing From The First Second, Or Sliding Up Once The Hero Scrolls Away?",
  opt("phs_barnow", "Always There", "The action is visible before any scroll.", "practical", HC("Sticky Bar", TERRA, badges=B6[:3])),
  opt("phs_barlate", "Slides Up Later", "Hero gets the full screen at first.", "calm", HC("Sticky Bar", LAGOON, badges=B6[:3], sticky_late=True)))
p("CTA", "Inline Button Style: Terracotta Fill, Or Ink Outline With A Quieter Look?",
  opt("phs_infill", "Terracotta Fill", "Loud, matches the van and polos.", "bold", HC("Inline Button", TERRA, cta="inline", badges=B6[:3])),
  opt("phs_inline", "Ink Outline", "Quiet button; the video does the talking.", "calm", HC("Inline Button", INK, cta="inline", cta_style="outline", badges=B6[:3])))
p("Video", "Autoplay Teaser: Fully Silent, Or A Small Sound Toggle In The Corner?",
  opt("phs_silent", "Fully Silent", "Muted loop, nothing to tap.", "calm", HC("Autoplay", LAGOON)),
  opt("phs_sound", "Sound Toggle", "Muted at start; tap the speaker for sound.", "playful", HC("Autoplay", TERRA, sound=True)))

# ---------------- Clear Picks: App Header & Video ----------------
def band(c=TERRA, tall=False, center=False, right="share", greet=False):
    h = 64 if tall else 40; s = rect(14, 30, 212, h, c)
    if center: s += mark(120, 30 + 14, 7, c, "#FFFFFF") + t(120, 30 + 34, "Smart Upkeep", 11, "#FFFFFF", "khand", 700, "middle")
    else: s += mark(30, 30 + 20, 8, c, "#FFFFFF") + t(44, 30 + 24, "Smart Upkeep", 12, "#FFFFFF", "khand", 700)
    if right == "share": s += shareic(204, 30 + 13, "#FFFFFF")
    elif right == "name": s += f'<circle cx="212" cy="{50}" r="9" fill="#FFFFFF33"/>' + t(212, 53.5, "M", 9, "#FFFFFF", "khand", 700, "middle") + t(198, 53.5, "Hi, Max", 7.5, "#FFFFFF", "hind", 600, "end")
    if greet: s += t(24, 30 + 52, "Good Morning, Max", 11, "#FFFFFF", "khand", 700) + t(24, 30 + 61, "Next visit Fri, Oct 23 (example)", 7.5, "#FFFFFFDD")
    return s, 30 + h + 8
def homebody(y, big=True, photoh=None):
    s = ""
    ph = photoh or (110 if big else 60)
    s += photo(14, y, 212, ph, LAGOON, "house", 0); y += ph + 6
    cs = [("card", "Next Visit", "Fall visit, Fri, Oct 23 (example)", TERRA, "tag:Soon"), ("card", "Your Plan", "Essentials (example)", LAGOON)]
    s += at(cs if 240 - y >= 80 else cs[:1], y)
    return s
def HB(label, acc, foot=None, **k):
    s, y = band(**k); return card(label, acc, s + homebody(y) + navbar(246, MNAV) + (chips(276, foot) if foot else ""))
CA = []
def q(g, ask, a, b): CA.append((g, ask, a, b))
q("Header Band", "Color Band Header: Terracotta Band, Or A Lagoon Band?",
  opt("cph_terra", "Terracotta Band", "Same warm color as the van and polos.", "bold", HB("Header Band", TERRA, c=TERRA)),
  opt("cph_lagoon", "Lagoon Band", "Cooler blue; terracotta saved for buttons.", "calm", HB("Header Band", LAGOON, c=LAGOON)))
q("Header Band", "Band Height: A Slim Band With The Logo, Or A Taller Band With The Greeting Inside?",
  opt("cph_slim", "Slim Band", "Logo and Share only; the house photo leads.", "practical", HB("Band Height", TERRA)),
  opt("cph_tall", "Tall Band + Greeting", "Good Morning and the next visit inside.", "premium", HB("Band Height", LAGOON, tall=True, greet=True)))
q("Header Band", "Inside The Band: Logo Left With Share, Or Logo Centered (Your Second Pick) In The Band?",
  opt("cph_left", "Logo Left + Share", "Share sits at the right edge.", "practical", HB("Band Layout", TERRA)),
  opt("cph_center", "Centered In The Band", "Mixes your two favorite headers.", "calm", HB("Band Layout", JUNGLE, center=True, right="")))
q("Header Band", "Band Right Side: The Share Button, Or The Member's Name And Initial?",
  opt("cph_share", "Share Button", "Same as every board header.", "practical", HB("Band Right Side", TERRA)),
  opt("cph_name", "Name + Initial", "Hi, Max with a round initial.", "playful", HB("Band Right Side", SAFFRON, right="name")))
q("Header Band", "Header Band While Scrolling: Pinned At The Top, Or Scrolls Away With The Page?",
  opt("cph_pin", "Pinned At The Top", "Logo and Share always in reach.", "practical", HB("Band Scroll", TERRA, foot=["Stays put"])),
  opt("cph_away", "Scrolls Away", "More room for the page once you scroll.", "calm", card("Band Scroll", LAGOON, homebody(36, True, 120) + t(120, 30 + 6 + 120 + 90, "band slid up out of view", 7.5, MUTE, "hind", 400, "middle") + navbar(246, MNAV) + chips(276, ["More room"]))))
def report_clip(mode):
    s = slide(14, 32, 212, rect(0, 0, 320, 180, "#FFFFFF") + (
        (rect(20, 14, 120, 152, "#FFFFFF", LINE) + t(28, 32, "Visit Report", 12, INK, "khand") + "".join(rect(28, 42 + i * 16, 104, 10, SOFT) for i in range(7)) + rect(176, 30, 120, 120, "#F4ECE0") + photo(186, 40, 100, 70, LAGOON, "room", 0) + t(236, 130, "scrolls down", 9, MUTE, "hind", 400, "middle") + f'<path d="M160 60 V130 M154 122 L160 130 L166 122" stroke="{TERRA}" stroke-width="2" fill="none"/>')
        if mode == "scroll" else
        (photo(0, 0, 320, 180, LAGOON, "room", 0) + rect(0, 130, 320, 50, "#FFFFFFEE") + t(16, 152, "Furnace filter changed. All good.", 13, INK, "khand") + t(16, 168, "From your visit report (example)", 9, MUTE))))
    return s + t(14, 166, "Report Clip", 10, INK, "khand") + t(14, 178, "Clip frame, drawn", 7.5, MUTE)
q("Video", "Report Clip: Scroll Down A Whole Sample Report, Or Zoom Into One Photo And One Line?",
  opt("cpv_scroll", "Scroll The Whole Report", "Shows how complete each report is.", "practical", card("Report Clip", LAGOON, report_clip("scroll") + at([("checks", ["Photos of every task", "Notes from the tech", "What to watch"], JUNGLE, 3)], 190), example=True)),
  opt("cpv_zoom", "Zoom To One Photo", "One clear moment; easy to read fast.", "calm", card("Report Clip", TERRA, report_clip("zoom") + at([("banner", "One photo, one plain line", TERRA, "star")], 190), example=True)))
def endcard(tagline=False, url=False):
    inner = rect(0, 0, 320, 180, "#FFFFFF") + mark(160, 66 if tagline else 78, 22, "#FFFFFF", TERRA) + wordmark(160, 120 if tagline else 132, 26, INK, GREY, "middle")
    if tagline: inner += t(160, 146, "Your Home, Taken Care Of.", 14, TERRA, "khand", 700, "middle")
    return slide(14, 40, 212, inner)
q("Video", "Video End Card: The Logo Alone, Or The Logo With 'Your Home, Taken Care Of.' Under It?",
  opt("cpv_logo", "Logo Alone", "Clean last frame.", "calm", card("End Card", INK, endcard() + at([("p", "Last 2 seconds of the clip.")], 172))),
  opt("cpv_tag", "Logo + Site Headline", "The homepage line closes the clip.", "bold", card("End Card", TERRA, endcard(True) + at([("p", "Last 2 seconds of the clip.")], 172))))
def dyk(style):
    s = phdr(30)[0] + photo(14, 56, 212, 70, LAGOON, "house", 0)
    if style == "icon": s += rect(14, 134, 212, 70, "#FFFFFF", LINE) + rect(22, 144, 24, 24, LAGOON + "1F") + ic("star", 26, 148, 16, LAGOON, 2) + t(54, 152, "DID YOU KNOW?", 7.5, LAGOON, "hind", 600, 'letter-spacing="1"') + t(54, 166, "Dryer vents clog faster", 10, INK, "khand") + t(54, 178, "than most filters. (example tip)", 7.5, MUTE)
    else: s += rect(14, 134, 212, 70, LAGOON + "14") + rect(14, 134, 3, 70, LAGOON) + t(26, 150, "DID YOU KNOW?", 7.5, LAGOON, "hind", 600, 'letter-spacing="1"') + t(26, 168, "Dryer vents clog faster", 12, INK, "khand") + t(26, 182, "than most filters. (example tip)", 7.5, MUTE)
    return s + at([("card", "Next Visit", "Fall visit (example)", TERRA)], 212)
q("Member App Look", "'Did You Know?' Card: Lagoon Label With A Small Icon, Or A Lagoon-Tinted Card?",
  opt("cpd_icon", "Label + Icon", "White card, small lagoon icon box.", "calm", card("Did You Know", LAGOON, dyk("icon"))),
  opt("cpd_tint", "Tinted Card", "Soft lagoon fill with a side rule.", "premium", card("Did You Know", LAGOON, dyk("tint"))))
def bighouse(over=True, tall=True):
    h = (118 if tall else 76) - (0 if over else 22); s = band()[0] + photo(14, 78, 212, h, LAGOON, "house", 0)
    if over: s += rect(14, 78 + h - 26, 212, 26, "#0A0A0A55") + t(22, 78 + h - 10, "1240 Example St, Royal Oak", 9, "#FFFFFF", "hind", 600)
    y = 78 + h + 6
    if not over: s += t(14, y + 10, "1240 Example St, Royal Oak", 10, INK, "khand", 700) + t(14, y + 21, "Essentials plan (example)", 7.5, MUTE); y += 28
    cs = [("card", "Next Visit", "Fri, Oct 23 (example)", TERRA, "tag:Soon"), ("card", "Your Plan", "Essentials (example)", LAGOON)]
    return s + at(cs if 240 - y >= 80 else cs[:1], y) + navbar(246, MNAV)
q("Member Home", "Big House Picture: Address Laid Over The Photo, Or Address Under It On White?",
  opt("cpb_over", "Address On The Photo", "Photo stays tall; address on a dark strip.", "premium", card("House Picture", TERRA, bighouse(True), example=True)),
  opt("cpb_under", "Address Underneath", "Photo clean; address and plan below.", "practical", card("House Picture", LAGOON, bighouse(False), example=True)))
q("Member Home", "Big House Picture Size: About Half The Screen, Or About A Third?",
  opt("cpb_half", "Half The Screen", "The house is the hero of Home.", "bold", card("Picture Size", TERRA, bighouse(True, True), example=True)),
  opt("cpb_third", "A Third", "More of the next visit shows at once.", "practical", card("Picture Size", JUNGLE, bighouse(True, False), example=True)))

# ---------------- Clear Picks: Menus & Headlines ----------------
def sect(style, c=TERRA, y=36):
    if style == "label": return t(14, y + 8, "YOUR PLAN", 7.5, c, "hind", 600, 'letter-spacing="1.2"') + t(14, y + 26, "What's Covered This Fall", 15, INK, "khand", 700)
    if style == "label_grey": return t(14, y + 8, "YOUR PLAN", 7.5, MUTE, "hind", 600, 'letter-spacing="1.2"') + t(14, y + 26, "What's Covered This Fall", 15, INK, "khand", 700)
    if style == "rule": return rect(14, y + 4, 4, 26, c) + t(24, y + 24, "What's Covered This Fall", 15, INK, "khand", 700)
def SEC(label, acc, style, c=TERRA):
    s = phdr(30)[0] + sect(style, c, 60) + at([("cards", [("Furnace Tune-Up", "Every fall visit"), ("Gutter Check", "Every fall visit"), ("Smoke/CO Test", "Every visit")], None, "dot")], 100) + navbar(246, MNAV)
    return card(label, acc, s)
CM = []
def r(g, ask, a, b): CM.append((g, ask, a, b))
def payprev(fields):
    s = phdr(30)[0] + t(14, 74, "Sign Up", 15, INK, "khand", 700) + at([("steps", ["Plan", "Add-Ons", "You", "Pay"], TERRA, 3)], 80)
    if fields: s += at([("lbl", "Card (demo, nothing is charged)"), ("input", "Card number", LAGOON, "card"), ("btn2", "MM / YY", "CVC")], 122)
    else: s += rect(14, 126, 212, 70, SOFT) + ic("card", 24, 140, 22, LAGOON, 1.8) + t(54, 150, "Payment comes next", 12, INK, "khand", 700) + t(54, 164, "You enter your card on the", 7.5, MUTE) + t(54, 174, "secure payment step.", 7.5, MUTE)
    return card("Payment Step", LAGOON if fields else TERRA, s + at([("btn", "Continue", "fill", TERRA)], 212))
r("Order Form", "Re-Ask, Sign-Up Payment Step: Draw The Card Number Boxes, Or A Plain 'Payment Comes Next' Note?",
  opt("cpm_fields", "Card Boxes Shown", "Member sees exactly what comes next.", "practical", payprev(True)),
  opt("cpm_note", "'Payment Comes Next'", "Short note; the real form opens after.", "calm", payprev(False)))
r("Section Headline", "Your Two Favorite Headlines, Head To Head: Label Plus Headline, Or Side Rule Headline?",
  opt("cpm_label", "Label Plus Headline", "Small caps label, big headline under it.", "calm", SEC("Section Headline", TERRA, "label")),
  opt("cpm_rule", "Side Rule Headline", "A terracotta rule beside the headline.", "bold", SEC("Section Headline", TERRA, "rule")))
r("Section Headline", "Label Above The Headline: Terracotta Caps, Or Grey Caps?",
  opt("cpm_lterra", "Terracotta Caps", "Brand color marks each section.", "bold", SEC("Label Color", TERRA, "label")),
  opt("cpm_lgrey", "Grey Caps", "Quieter; headline does the work.", "calm", SEC("Label Color", INK, "label_grey")))
def tabs_screen(kind="iconlabel", n=4, active="underline", swipe=False):
    s = phdr(30)[0] + sect("label", TERRA, 60) + at([("cards", [("Fall Visit", "Fri, Oct 23 (example)"), ("Spring Visit", "Apr (example)")], None, "dot")], 100)
    items = [("Home", "home"), ("Record", "tag"), ("Visits", "cal"), ("Chat", "mic"), ("Profile", "star")][:n] if n == 5 else list(MNAV)
    w = 212 / len(items); y = 240
    s += ln(y)
    for i, (nm, k) in enumerate(items):
        cx = 14 + i * w + w / 2; on = i == 0
        if on and active == "pill": s += rect(cx - w / 2 + 4, y + 4, w - 8, 30, TERRA + "1F", "none", 15)
        if kind != "label": s += ic(k, cx - 7, y + 6, 14, TERRA if on else MUTE, 1.8)
        s += t(cx, y + (28 if kind != "label" else 22), nm, 8 if kind == "label" else 7.5, TERRA if on else MUTE, "hind", 600, "middle")
        if on and active == "underline": s += rect(cx - 12, y + 33, 24, 2.5, TERRA)
    if swipe: s += f'<path d="M60 200 H180 M172 194 L180 200 L172 206 M68 194 L60 200 L68 206" stroke="{LAGOON}" stroke-width="1.6" fill="none"/>' + t(120, 222, "swipe left or right to change tab", 7.5, LAGOON, "hind", 600, "middle")
    return s
r("Menu Type", "Bottom Tabs: Icons With Labels, Or Labels Only?",
  opt("cpm_tic", "Icons + Labels", "Easy to spot with a thumb.", "practical", card("Bottom Tabs", TERRA, tabs_screen("iconlabel"))),
  opt("cpm_tlab", "Labels Only", "Cleaner bar, bigger words.", "calm", card("Bottom Tabs", INK, tabs_screen("label"))))
r("Menu Type", "Bottom Tabs Count: Four Tabs, Or Five With Chat As Its Own Tab?",
  opt("cpm_four", "Four Tabs", "Home, Record, Visits, Profile.", "calm", card("Tab Count", TERRA, tabs_screen())),
  opt("cpm_five", "Five With Chat", "Chat with the team one tap away.", "practical", card("Tab Count", LAGOON, tabs_screen(n=5))))
r("Menu Type", "Active Tab: A Terracotta Underline, Or A Soft Filled Pill?",
  opt("cpm_under", "Underline", "Thin bar under the active tab.", "calm", card("Active Tab", TERRA, tabs_screen(active="underline"))),
  opt("cpm_pill", "Filled Pill", "Soft terracotta pill behind it.", "playful", card("Active Tab", SAFFRON, tabs_screen(active="pill"))))
r("Menu Type", "Bottom Tabs Plus Swipe Pages: Let A Sideways Swipe Change Tabs, Or Tap Only?",
  opt("cpm_swipe", "Swipe Changes Tabs", "Mixes your two menu picks.", "playful", card("Swipe Pages", LAGOON, tabs_screen(swipe=True))),
  opt("cpm_tap", "Tap Only", "No surprise page changes while scrolling.", "practical", card("Swipe Pages", INK, tabs_screen())))
def addbtn(kind):
    s = phdr(30)[0] + t(14, 74, "Your Home Record", 15, INK, "khand", 700)
    rows = [("Furnace", "Installed 2014 (example)"), ("Water Heater", "Installed 2019 (example)"), ("AC", "Installed 2016 (example)")]
    s += at([("cards", rows, None, "dot")], 82)
    if kind == "text": s += rect(14, 206, 120, 26, "#FFFFFF", LAGOON, 0, 1.4) + t(74, 223, "+ ADD APPLIANCE", 8, LAGOON, "hind", 600, "middle", 'letter-spacing=".8"')
    else: s += f'<circle cx="206" cy="218" r="14" fill="#FFFFFF" stroke="{LAGOON}" stroke-width="1.6"/>' + f'<path d="M206 211 V225 M199 218 H213" stroke="{LAGOON}" stroke-width="2"/>'
    return s + navbar(246, MNAV, 1)
r("Member App Look", "Lagoon Outline Add Button: '+ Add Appliance' In Words, Or A Round '+' Only?",
  opt("cpm_addtxt", "'+ Add Appliance'", "Says exactly what it adds.", "practical", card("Add Button", LAGOON, addbtn("text"), example=True)),
  opt("cpm_addplus", "Round '+'", "Smaller, floats at the corner.", "calm", card("Add Button", LAGOON, addbtn("plus"), example=True)))
def addon_step(kind, skip="bottom"):
    s = phdr(30)[0] + t(14, 74, "Add Extras?", 15, INK, "khand", 700) + at([("steps", ["Plan", "Add-Ons", "You", "Pay"], TERRA, 1)], 80)
    items = [("Custom Grass Cutting", "lawn"), ("Window Cleaning", "home"), ("Gutter Cleaning", "home")]
    y = 120
    if skip == "top": s += t(226, 74, "SKIP", 8, LAGOON, "hind", 600, "end", 'text-decoration="underline"')
    for i, (nm, k) in enumerate(items):
        if kind == "list":
            s += rect(14, y, 12, 12, "#FFFFFF", "#BDB6AA", 0, 1.2) + t(34, y + 10, nm, 9, INK, "khand", 700) + t(226, y + 10, "+$X/mo", 7.5, MUTE, "hind", 600, "end") + ln(y + 18); y += 24
        else:
            s += rect(14, y, 212, 28, "#FFFFFF", LINE) + t(22, y + 18, nm, 9.5, INK, "khand", 700) + rect(194, y + 7, 24, 14, "#D6D0C6", "none", 7) + dot(201, y + 14, 5, "#FFFFFF"); y += 34
    if skip == "bottom": s += t(120, 228, "No thanks, continue", 8, LAGOON, "hind", 600, "middle", 'text-decoration="underline"')
    return s + rect(14, 236, 212, 26, TERRA) + t(120, 253, "CONTINUE", 8.5, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
r("Add-Ons", "Separate Add-On Step: Tick Boxes With Prices On The Right, Or Cards With A Toggle?",
  opt("cpm_alist", "Tick List + Prices", "Short list, quick to scan.", "practical", card("Add-On Step", TERRA, addon_step("list"), example=True)),
  opt("cpm_acard", "Cards With Toggles", "Roomier; each extra is its own card.", "calm", card("Add-On Step", LAGOON, addon_step("card"), example=True)))
r("Add-Ons", "Skipping The Add-On Step: A 'Skip' Link Up Top, Or 'No Thanks, Continue' At The Bottom?",
  opt("cpm_sktop", "'Skip' Up Top", "Fast way out for people who know.", "practical", card("Skip Add-Ons", INK, addon_step("list", "top"), example=True)),
  opt("cpm_skbot", "'No Thanks' At The Bottom", "Read the extras first, then decide.", "calm", card("Skip Add-Ons", LAGOON, addon_step("list", "bottom"), example=True)))
DECKS = [
 D("upkeep-phone-home-top-section-hero-details-deck", "Phone Home Top Section: Hero Details", "phone-home-hero-details", "fuph_", "upkeep-phone-home-top-section-deck",
   "Follow-on to Phone Home Top Section (18/20, Oct 17 00:10 ICT): the full-bleed video with text over it, sticky CTA and badge carousel he picked, refined; both skips re-asked.",
   "Deeper on the phone hero he picked: text-over-video fade, headline spot and color, sticky bar timing and price, badge carousel (re-asked), spacing (re-asked).", "Home Page", PH, ["upkeep-phone-home-top-section-deck-06", "upkeep-phone-home-top-section-deck-18"], "upkeep-phone-home-top-section-deck-20261017-0010-be52ef12.json"),
 D("upkeep-clear-picks-header-band-and-report-clip-deck", "Clear Picks: Header Band And Report Clip", "clear-picks-header-band", "fucpa_", "upkeep-clear-picks-clear-picks-deck-app-header-video",
   "Follow-on to Clear Picks: App Header & Video (10/10): the color band header won every head-to-head, so this refines the band, the report clip, the end card and the big house picture.",
   "Refines his winners: color band header (color, height, layout), report clip style, video end card, Did You Know card, big house picture.", "Member App", CA, [], "upkeep-clear-picks-clear-picks-deck-app-header-video-20261017-0856-b07e2e16.json"),
 D("upkeep-clear-picks-tabs-headlines-and-add-on-step-deck", "Clear Picks: Tabs, Headlines And Add-On Step", "clear-picks-tabs-headlines", "fucpm_", "upkeep-clear-picks-clear-picks-deck-menus-headlines",
   "Follow-on to Clear Picks: Menus & Headlines (9/10): bottom tabs, label-plus-headline vs side rule, lagoon outline Add button and the separate add-on step; Demo Card Box skip re-asked.",
   "Bottom tab details, the two winning headline styles head to head, Add button wording, the separate add-on step; payment-box skip re-asked.", "Member App", CM, ["upkeep-clear-picks-clear-picks-deck-menus-headlines-06"], "upkeep-clear-picks-clear-picks-deck-menus-headlines-20261017-0901-ca0e6633.json"),
]
