"""Tagline deck Oct 18 2026 (18:23 ICT request): where 'Home Maintenance Membership' sits with the Smart Upkeep wordmark.
10 this-or-that picks, Notes on every card, light only, Khand headings + Hind body. In-context screens (site hero, app header,
van, polo, business card) are drawn mockups and say MOCKUP; nothing here edits the live site, app or welcome video.
Contact details are placeholders only."""
from md1018_kit import *
from uk5_art import mark
NAME, TL = "Smart Upkeep", "Home Maintenance Membership"
WMK = "Smart Upkeep Wordmark"; HERO = "Smart Upkeep Site Hero Mockup"; APPH = "Smart Upkeep Member App Header Mockup"
VAN = "Smart Upkeep Van Mockup"; POLO = "Smart Upkeep Crew Polo Mockup"; CARD = "Smart Upkeep Business Card Mockup"
def wm(x, y, size, anchor="middle", c=INK): return t(x, y, NAME, size, c, "khand", anchor=anchor)
def tg(x, y, size, anchor="middle", c=MUTE, caps=False, w=500, khand=False, ls=None):
    return t(x, y, TL.upper() if caps else TL, size, c, "khand" if khand else "hind", w, anchor, f'letter-spacing="{ls}"' if ls else "")
def hm(cx, cy, r, c=TERRA, fg="#FFFFFF"): return mark(cx, cy, r, fg, c)
def o(k, label, desc, feel, loc, blocks, n1, n2="", mock=False):
    return (k, label, desc, feel, S(loc, blocks, (n1, n2)))  # location label already says Mockup
STAGE = lambda inner, h=150: ("raw", rect(14, 0, 212, h, CREAM, "none", 10) + inner, h + 8)
def nav(word=True, sub=False):
    s = rect(0, 0, W, 34, "#FFFFFF") + ln(34, 0, W, LINE) + hm(24, 17, 9)
    s += wm(38, 21 if not sub else 17, 14, "start") + (tg(38, 27, 5.6, "start", MUTE, True, 600, ls=".6") if sub else "")
    s += "".join(rect(206, 11 + i * 5, 18, 2, INK, "none", 1) for i in range(3))
    return s
def btn(x, y, w, label, c=TERRA): return rect(x, y, w, 26, c, "none", 4) + t(x + w / 2, y + 17, label, 9, "#FFFFFF", "hind", 700, "middle")
def van(side):
    s = rect(10, 20, 170, 104, "#FFFFFF", "#CFC8BC", 10, 1.4) + f'<path d="M180 44 H206 Q214 44 220 56 L230 82 V124 H180 Z" fill="#FFFFFF" stroke="#CFC8BC" stroke-width="1.4"/>'
    s += f'<path d="M186 52 H204 Q209 52 212 58 L220 78 H186 Z" fill="{LAGOON}33"/>' + rect(10, 108, 220, 16, "#EEEAE4", "none", 0)
    for cx in (52, 196): s += f'<circle cx="{cx}" cy="126" r="15" fill="#2B2B2B"/><circle cx="{cx}" cy="126" r="6" fill="#BDB6AA"/>'
    return ("raw", s + side, 150)
def polo(x, c, inner):
    """Flat polo, 108 wide: sleeves x..x+108, body x+16..x+92 (76 wide), collar at the centre x+54."""
    p = (f'<path d="M{x+22} 14 L{x} 34 L{x+9} 60 L{x+16} 56 V150 H{x+92} V56 L{x+99} 60 L{x+108} 34 L{x+86} 14 '
         f'Q{x+70} 8 {x+54} 22 Q{x+38} 8 {x+22} 14 Z" fill="{c}"/>' + f'<path d="M{x+40} 12 L{x+54} 24 L{x+46} 30 Z M{x+68} 12 L{x+54} 24 L{x+62} 30 Z" fill="#00000026"/><path d="M{x+54} 24 V42" stroke="#00000033" stroke-width="1"/>')
    return p + inner
def bcard(y, inner, h=112): return rect(24, y + 3, 196, h, "#0000000D", "none", 6) + rect(22, y, 196, h, "#FFFFFF", "#D6D0C6", 6) + inner
def T_TAGLINE():
    pairs, P = make("tg18_", "UpKeep")
    P("Lockup", WMK, "Tagline role", "should Home Maintenance Membership sit as a small subheadline under the wordmark or become the big headline with the name small above it?",
      o("sub", "Subheadline Under The Logo", "Big Smart Upkeep, the tagline small underneath.", "calm", WMK, [("gap", 46), STAGE(wm(120, 74, 38) + tg(120, 98, 10.5), 140)], "Name first", "The tagline explains it"),
      o("head", "Tagline As The Headline", "Home Maintenance Membership big, the name small on top.", "focused", WMK, [("gap", 46), STAGE(hm(120, 28, 10) + wm(120, 58, 14, c=TERRA) + t(120, 90, "Home Maintenance", 27, INK, "khand", anchor="middle") + t(120, 118, "Membership", 27, INK, "khand", anchor="middle"), 140)], "Says what it is", "The name rides on top"))
    P("Lockup", WMK, "Extra tagline line", "under Home Maintenance Membership should there be one more short line about what members get or nothing more?",
      o("none", "No Extra Line", "Wordmark and tagline only.", "calm", WMK, [("gap", 46), STAGE(wm(120, 76, 36) + tg(120, 100, 10.5), 140)], "Short and clean", "Fits anywhere"),
      o("extra", "One Extra Line", "Adds: Seasonal care for every system, one plan.", "practical", WMK, [("gap", 46), STAGE(wm(120, 66, 36) + tg(120, 90, 10.5) + ln(104, 96, 144, "#D6D0C6") + t(120, 120, "Seasonal care for every system, one plan", 8.5, TERRA, "hind", 600, "middle"), 140)], "Spells out the offer", "Sample wording"))
    P("Type", WMK, "Tagline size and weight", "should the tagline be small and light so the wordmark leads or bold and nearly as wide as the wordmark?",
      o("light", "Small And Light", "Hind, regular weight, soft grey, spaced out.", "calm", WMK, [("gap", 46), STAGE(wm(120, 76, 38) + tg(120, 98, 8.5, c=MUTE, w=400, ls="1"), 140)], "Quiet support", "Logo stays the hero"),
      o("bold", "Bold And Wide", "Khand bold in ink, close to the wordmark width.", "focused", WMK, [("gap", 46), STAGE(wm(120, 72, 38) + tg(120, 100, 17, c=INK, khand=True), 140)], "Reads from far away", "Two strong lines"))
    P("Type", WMK, "Tagline case", "should the tagline be set in spaced all caps or in title case?",
      o("caps", "Spaced All Caps", "HOME MAINTENANCE MEMBERSHIP, letter-spaced.", "focused", WMK, [("gap", 46), STAGE(wm(120, 76, 38) + tg(120, 98, 8.5, INK, True, 600, ls="1.6"), 140)], "Badge-like, formal", "Works small"),
      o("title", "Title Case", "Home Maintenance Membership, normal spacing.", "warm", WMK, [("gap", 46), STAGE(wm(120, 76, 38) + tg(120, 99, 11.5, INK, False, 500), 140)], "Friendly and easy", "Reads like a sentence"))
    P("Mark", WMK, "House mark", "should the lockup be the wordmark alone or the terracotta house mark beside the wordmark and tagline?",
      o("word", "Wordmark Only", "Smart Upkeep and the tagline, no symbol.", "calm", WMK, [("gap", 46), STAGE(wm(120, 76, 36) + tg(120, 99, 10.5), 140)], "Pure type", "Simplest to reuse"),
      o("mark", "With The House Mark", "Round terracotta house mark on the left.", "warm", WMK, [("gap", 46), STAGE(hm(56, 80, 25) + wm(90, 82, 29, "start") + tg(91, 100, 8.4, "start"), 140)], "Recognisable as an icon", "Mark works alone too"))
    P("In Context", HERO, "Tagline spot", "on a drawn site hero should Home Maintenance Membership be a small eyebrow over the headline or the big headline itself?",
      o("eyebrow", "Small Eyebrow Line", "Spaced caps over a short headline.", "calm", HERO, [("raw", nav(), 40), ("raw", photo(14, 0, 212, 80, LAGOON, "house", 8), 88), ("raw", tg(14, 8, 7.2, "start", TERRA, True, 700, ls="1.2") + t(14, 34, "Your home, taken care of", 19, INK, "khand") + t(14, 50, "Seasonal visits and a photo report", 8.5, MUTE) + btn(14, 60, 96, "See plans"), 92)], "Headline stays short", "Mockup, not the live site", True),
      o("headline", "Tagline Is The Headline", "Home Maintenance Membership big under the photo.", "focused", HERO, [("raw", nav(), 40), ("raw", photo(14, 0, 212, 80, LAGOON, "house", 8), 88), ("raw", t(14, 22, "Home Maintenance", 22, INK, "khand") + t(14, 44, "Membership", 22, TERRA, "khand") + t(14, 60, "Seasonal visits and a photo report", 8.5, MUTE) + btn(14, 68, 96, "See plans"), 100)], "Clear in one look", "Mockup, not the live site", True))
    P("In Context", APPH, "Tagline in the header", "should the app header carry the tagline under the wordmark or keep the header to the wordmark and show the tagline once on the welcome card?",
      o("header", "Under The Wordmark", "Tiny spaced caps under the name in the header.", "practical", APPH, [("raw", nav(sub=True), 42), ("raw", t(14, 16, "Good morning", 15, INK, "khand") + rect(14, 26, 212, 64, CREAM, "none", 8) + t(24, 46, "Next visit", 10, INK, "khand") + t(24, 60, "Fall tune-up, sample date", 8, MUTE) + chip(24, 68, "Starter plan", JUNGLE)[0], 96)], "Brand on every screen", "Mockup, sample data", True),
      o("card", "On The Welcome Card", "Header shows the wordmark only.", "calm", APPH, [("raw", nav(), 42), ("raw", t(14, 16, "Good morning", 15, INK, "khand") + rect(14, 26, 212, 74, CREAM, "none", 8) + rect(14, 26, 4, 74, TERRA) + tg(26, 44, 7, "start", TERRA, True, 700, ls="1") + t(26, 64, "Your plan is active", 13, INK, "khand") + t(26, 78, "Starter plan, sample", 8, MUTE) + chip(26, 84, "Active", JUNGLE, True)[0], 106)], "Clean header", "Tagline where it matters", True))
    P("In Context", VAN, "Van side layout", "on the van side should the wordmark and tagline stack big in the middle or should the tagline run along a terracotta stripe at the bottom?",
      o("stack", "Stacked In The Middle", "Wordmark big, tagline under it, centred.", "calm", VAN, [("gap", 30), van(hm(95, 40, 10) + wm(95, 74, 24) + tg(95, 91, 7.2, c=INK, w=600))], "Easy to read parked", "Mockup", True),
      o("stripe", "Tagline On A Stripe", "White caps on a terracotta band along the bottom.", "playful", VAN, [("gap", 30), van(hm(36, 54, 12) + wm(54, 63, 21, "start") + rect(10, 88, 170, 18, TERRA, "none", 0) + tg(95, 100, 6.8, c="#FFFFFF", caps=True, w=700, ls="1"))], "Reads at speed", "Mockup", True))
    P("In Context", POLO, "Back print", "on the polo back should the print be the wordmark alone or the wordmark with the tagline under it?",
      o("alone", "Wordmark Alone", "Chest mark in front, big wordmark on the back.", "calm", POLO, [("gap", 24), ("raw", polo(8, TERRA, hm(88, 46, 5.5, "#FFFFFF", TERRA) + t(81, 49, "Smart Upkeep", 7, "#FFFFFF", "khand", anchor="end")) + polo(124, TERRA, wm(178, 84, 12.5, c="#FFFFFF")) + t(62, 168, "Front", 8, MUTE, anchor="middle") + t(178, 168, "Back", 8, MUTE, anchor="middle"), 180)], "Simple, cheaper print", "Mockup", True),
      o("tag", "Wordmark Plus Tagline", "Same front, the tagline under the back wordmark.", "practical", POLO, [("gap", 24), ("raw", polo(8, TERRA, hm(88, 46, 5.5, "#FFFFFF", TERRA) + t(81, 49, "Smart Upkeep", 7, "#FFFFFF", "khand", anchor="end")) + polo(124, TERRA, wm(178, 78, 12.5, c="#FFFFFF") + t(178, 92, "HOME MAINTENANCE", 4.2, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".2"') + t(178, 101, "MEMBERSHIP", 4.2, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".2"')) + t(62, 168, "Front", 8, MUTE, anchor="middle") + t(178, 168, "Back", 8, MUTE, anchor="middle"), 180)], "Says what the crew does", "Mockup", True))
    P("In Context", CARD, "Tagline side", "on the business card should the tagline sit on the front under the wordmark or on the back with the contact details?",
      o("front", "Tagline On The Front", "Front: mark, wordmark, tagline; back: contact.", "focused", CARD, [("raw", bcard(0, hm(120, 30, 12) + wm(120, 68, 24) + tg(120, 86, 7.6, c=TERRA, w=600)) + bcard(122, t(36, 150, "Name Here", 13, INK, "khand") + t(36, 164, "Field Tech", 8, MUTE) + t(36, 196, "(000) 000-0000", 8, INK) + t(36, 210, "Sample details", 7.5, FAINT), 100), 232)], "Front says it all", "Mockup, placeholder details", True),
      o("back", "Tagline On The Back", "Front: mark and wordmark only; tagline by contact.", "calm", CARD, [("raw", bcard(0, hm(120, 34, 13) + wm(120, 76, 26)) + bcard(122, t(36, 150, "Name Here", 13, INK, "khand") + t(36, 164, "Field Tech", 8, MUTE) + t(36, 190, "(000) 000-0000", 8, INK) + rect(36, 198, 2, 14, TERRA) + tg(42, 209, 7, "start", TERRA, True, 700, ls=".8"), 100), 232)], "Bold, simple front", "Mockup, placeholder details", True))
    return pairs
