"""Investor pitch founder slide deck, Oct 18 2026 night (Branding; asked directly 22:33 ICT): 'Built By A Builder'.
10 this-or-that picks, Notes on every card, light only, Khand headings + Hind body, phone-first. Every card is a drawn MOCKUP of
the live founder slide (pitch-deck slide 9, upkeep-cc bb2e154) or one of its tiles. Founder anonymous: no name, no photo.
Facts: only the live slide's facts (with 'Economics and accounting', corrected) plus three verified new facts (rental property,
U.S. operations run remotely, multiple small businesses). No numbers are added; the one home count is a labelled SAMPLE placeholder."""
from md1018_kit import *
FS = "Founder Slide Mockup"
VW = 300; K = W / VW          # slide drawn at 300 virtual units wide, scaled into the 240-unit card (keeps small text small)
DARK = "#141414"; HAIR = "#E4DED3"; PAGE = "#FBF8F2"
CRED = "Licensed Residential Builder, State of Michigan, since 2012"
TIL = {  # tile facts: (title lines, sub line)
    "homes": (["Multi-million-dollar", "home builds"], "Has managed them, start to finish."),
    "econ": (["Economics and", "accounting"], "A background in both."),
    "ai": (["AI agent training"], "Trains the agent teams."),
    "lang": (["Multiple languages"], "Works in several."),
    "rent": (["Residential rental", "property"], "Manages leases, tenants, upkeep."),
    "remote": (["Remote operations"], "Runs U.S. operations remotely."),
    "biz": (["Multiple small", "businesses"], "Operator of several."),
    "count": (["XX homes"], "Built or managed. SAMPLE number."),
}
NEW = {"rent", "remote", "biz"}
TLINE = [("2012", "Licensed builder. Founded a construction", "management company."), ("SINCE", "Self-employed construction project", "manager."),
         ("NOW", "Built the platform. Hired and trained the", "first tech.")]
LEADS = {"platform": ("Designed and built the platform", "Including every app shown in this deck."),
         "both": ("Builder and landlord. Lived both sides.", "Licensed builder who also manages rental property.")}
def T(x, y, s, size, c=INK, f="hind", w=400, a="start", ex=""): return t(x, y, s, size, c, f, w, a, ex)
def shield(x, y, c="#FFFFFF"):
    return (f'<g transform="translate({x},{y}) scale(.62)"><path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M8.5 12l2.5 2.5 4.5-5" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/></g>')
def head(y, sub="ONE OPERATOR, FIELD AND PLATFORM", title="Built By A Builder"):
    s = f'<line x1="16" y1="{y+5}" x2="26" y2="{y+5}" stroke="{TERRA}" stroke-width="1.2"/>' + T(31, y + 8, "THE FOUNDER", 8, TERRA, "hind", 600, ex='letter-spacing="1.4"')
    s += T(16, y + 38, title, 30, INK, "khand") + T(16, y + 54, sub, 7.4, MUTE, "hind", 400, ex='letter-spacing="1.3"')
    return s, 64
def cred(y):
    s = rect(16, y, 268, 34, DARK, "none", 7) + f'<circle cx="34" cy="{y+17}" r="10" fill="#FFFFFF22"/>' + shield(26.6, y + 9.6)
    s += T(52, y + 14, "Licensed Residential Builder, State of", 9.4, "#FFFFFF", "hind", 600) + T(52, y + 26, "Michigan, since 2012", 9.4, "#FFFFFF", "hind", 600)
    return s, 40
def cred_foot(y):
    s = shield(14.5, y - 1, TERRA) + T(31, y + 10, CRED, 7.6, INK, "hind", 600)
    return s, 18
def lead(y, k="platform"):
    a, b = LEADS[k]; size = 17 if len(a) < 33 else 15.2
    return T(16, y + 16, a, size, INK, "khand") + T(16, y + 30, b, 8.2, MUTE), 38
def tiles(y, keys, hi=(), tone="plain"):
    s = ln(y, 16, 284, HAIR); rows = (len(keys) + 1) // 2; yy = y
    for r in range(rows):
        row = keys[r * 2:r * 2 + 2]
        hts = [max(len(TIL[k][0]), 1) * 12 + 17 for k in row]; h = max(hts) + 8
        for i, k in enumerate(row):
            x = 16 + i * 140; tl, sub = TIL[k]
            if tone == "warm": sub = WARM.get(k, sub)
            if k in hi: s += rect(x + 1, yy + 2, 132, h - 4, TERRA + "0F", TERRA, 5, 1, 'stroke-dasharray="3 2"')
            for j, line in enumerate(tl): s += T(x + 4, yy + 15 + j * 12, line, 11.4, INK if k != "count" else "#8a6510", "khand")
            s += T(x + 4, yy + 15 + len(tl) * 12 + 3, sub, 7.4, MUTE)
            if k in NEW: s += rect(x + 104, yy + 5, 24, 11, TERRA, "none", 5.5) + T(x + 116, yy + 13, "NEW", 6.2, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".5"')
            if k == "count": s += rect(x + 84, yy + 5, 44, 11, "#FFFFFF", SAFFRON, 2, 1, 'stroke-dasharray="2 1.5"') + T(x + 106, yy + 13, "SAMPLE", 6.2, "#8a6510", "hind", 700, "middle", 'letter-spacing=".6"')
        if len(row) == 2: s += f'<line x1="150" y1="{yy+3}" x2="150" y2="{yy+h-3}" stroke="{HAIR}"/>'
        yy += h; s += ln(yy, 16, 284, HAIR)
    return s, yy - y + 8
WARM = {"homes": "Has seen them through, start to finish.", "econ": "Brings a background in both.", "ai": "Trains the agent teams himself.",
        "lang": "Comfortable in several.", "rent": "The owner side: leases, tenants, upkeep.", "remote": "Keeps U.S. operations running remotely.",
        "biz": "Has run several small businesses."}
def timeline(y):
    s = f'<line x1="21" y1="{y+6}" x2="21" y2="{y+70}" stroke="#D6D0C6"/>'
    for i, (k, a, b) in enumerate(TLINE):
        yy = y + i * 25; s += f'<circle cx="21" cy="{yy+5}" r="4" fill="{PAGE}" stroke="#8C8478" stroke-width="1"/>'
        s += T(31, yy + 8, k, 7.6, MUTE, "hind", 600, ex='letter-spacing="1"') + T(72, yy + 8, a, 7.8, INK) + T(72, yy + 18, b, 7.8, INK)
    return s, 78
def anon(y): return T(16, y + 8, "The founder stays anonymous in this deck.", 7, MUTE), 14
def story(y):
    a = "Has been on both sides of a home: building it, and"; b = "keeping it running for tenants. Then built the platform."
    return rect(16, y, 268, 36, TERRA + "0D", "none", 6) + rect(16, y, 3, 36, TERRA) + T(26, y + 15, a, 8, INK, "hind", 500) + T(26, y + 27, b, 8, INK, "hind", 500), 42
def slide(parts, mark=True):
    """parts: list of (fn, args...) stacked from the top; drawn on the slide page colour, scaled into the card."""
    y, s = 14, ""
    for p in parts:
        g, h = p[0](y, *p[1:]); s += g; y += h
    assert y <= H / K + 2, ("slide too tall", y)
    tag = t(232, 12, "MOCKUP", 6.5, MUTE, "hind", 700, "end", 'letter-spacing="1"') if mark else ""
    return screen(f'<rect width="{W}" height="{H}" fill="{PAGE}"/><g transform="scale({K:.4f})">{s}</g>' + tag, PAGE)
def zoom(parts, y0=10):
    """A close-up of the top of the slide (no timeline): content x 16..284 fills the card width, so tiles read larger."""
    y, s = y0, ""
    for p in parts:
        g, h = p[0](y, *p[1:]); s += g; y += h
    k = 232 / 268; assert y * k <= H + 2, ("zoom too tall", y * k)
    return screen(f'<rect width="{W}" height="{H}" fill="{PAGE}"/><g transform="translate({4 - 16 * k:.2f},4) scale({k:.4f})">{s}</g>' + t(232, 12, "MOCKUP", 6.5, MUTE, "hind", 700, "end", 'letter-spacing="1"'), PAGE)
def caption(y, a, b=""):
    return T(16, y + 10, a, 8.4, TERRA, "hind", 600) + (T(16, y + 22, b, 7.6, MUTE) if b else ""), 28 if b else 18
BASE4 = ["homes", "econ", "ai", "lang"]
def full(keys=BASE4, hi=(), lead_k="platform", tl=True, credpos="top", tone="plain", sub="ONE OPERATOR, FIELD AND PLATFORM", extra=None):
    parts = [(head, sub)]
    if credpos == "top": parts.append((cred,))
    parts.append((lead, lead_k))
    if extra: parts.append(extra)
    parts.append((tiles, keys, hi, tone))
    if tl: parts.append((timeline,))
    if credpos == "foot": parts.append((cred_foot,))
    parts.append((anon,))
    return slide(parts)
def tilezoom(new, why):
    keys = ["homes", "econ", "ai", new]
    return zoom([(head,), (cred,), (lead,), (tiles, keys, (new,)), (caption, "New tile shown in the last slot", why)])
def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
def T_FOUNDER_SLIDE():
    pairs, P = make("bb18_", "UpKeep")
    P("New Tile", FS, "Rental property or remote operations", "which new fact should earn a tile on the founder slide, the rental property you manage or running operations remotely?",
      o("rent", "Rental Property Tile", "Residential rental property: manages leases, tenants, upkeep.", "warm", tilezoom("rent", "Shows the owner side of a home")),
      o("remote", "Remote Operations Tile", "Remote operations: runs U.S. operations remotely.", "practical", tilezoom("remote", "Shows the business runs without you on site")))
    P("New Tile", FS, "Remote operations or multiple businesses", "which new fact should earn a tile, running operations remotely or being an operator of multiple small businesses?",
      o("remote", "Remote Operations Tile", "Remote operations: runs U.S. operations remotely.", "practical", tilezoom("remote", "Shows the business runs without you on site")),
      o("biz", "Multiple Businesses Tile", "Multiple small businesses: operator of several.", "focused", tilezoom("biz", "Shows a track record of running things")))
    P("New Tile", FS, "Rental property or multiple businesses", "which new fact should earn a tile, the rental property you manage or being an operator of multiple small businesses?",
      o("rent", "Rental Property Tile", "Residential rental property: manages leases, tenants, upkeep.", "warm", tilezoom("rent", "Shows the owner side of a home")),
      o("biz", "Multiple Businesses Tile", "Multiple small businesses: operator of several.", "focused", tilezoom("biz", "Shows a track record of running things")))
    P("Make Room", FS, "Languages tile or the new fact", "to make room should the slide keep the Multiple languages tile or swap it out for the winning new fact (rental property shown as the example)?",
      o("keep", "Keep Multiple Languages", "Four tiles as now, the new fact stays off this slide.", "calm", full(BASE4, ("lang",))),
      o("swap", "Swap In The New Fact", "Languages goes, the new fact takes its slot.", "focused", full(["homes", "econ", "ai", "rent"], ("rent",))))
    P("Lead Line", FS, "Lead line under the banner", "should the big line under the credential banner stay Designed and built the platform or become Builder and landlord, lived both sides?",
      o("platform", "Designed And Built The Platform", "Keeps the lead on the product: every app shown in this deck.", "focused", full(lead_k="platform")),
      o("both", "Builder And Landlord", "Builder and landlord. Lived both sides.", "warm", full(lead_k="both", sub="OPERATOR-FOUNDER, BUILDER AND LANDLORD")))
    P("Tile Grid", FS, "Four tiles or six", "should the tile grid stay at four tiles or grow to six with two new facts added (rental property and multiple businesses shown as examples)?",
      o("four", "Four Tiles", "The current four, room to breathe.", "calm", full(BASE4)),
      o("six", "Six Tiles", "The four plus two new facts, three rows.", "practical", full(BASE4 + ["rent", "biz"], ("rent", "biz"), tl=False)))
    P("Timeline", FS, "Timeline or more space", "should the slide keep the short 2012, Since, Now timeline under the tiles or drop it for more space?",
      o("tl", "Keep The Timeline", "2012, Since and Now stay under the tiles.", "practical", full(["homes", "econ", "ai", "rent"], ("rent",))),
      o("none", "No Timeline, More Space", "Tiles and banner carry the story, the slide breathes.", "calm", full(["homes", "econ", "ai", "rent"], ("rent",), tl=False)))
    P("Tone", FS, "Wording tone", "should the slide's wording stay confident and plain or turn into a warmer short story of builder and landlord?",
      o("plain", "Confident And Plain", "Short facts, no adjectives.", "focused", full(["homes", "econ", "ai", "rent"], tl=False)),
      o("warm", "Warmer Story", "A two-line story, then softer tile lines.", "warm", full(["homes", "econ", "ai", "rent"], lead_k="both", tl=False, tone="warm", sub="OPERATOR-FOUNDER, BUILDER AND LANDLORD", extra=(story,))))
    P("Credential", FS, "Licence banner placement", "should the licensed builder credential stay as the dark banner on top or move to a quiet footer line at the bottom of the slide?",
      o("top", "Dark Banner On Top", "The licence is the first thing read.", "focused", full(["homes", "econ", "ai", "rent"])),
      o("foot", "Quiet Footer Line", "The licence sits as one line at the bottom.", "calm", full(["homes", "econ", "ai", "rent"], credpos="foot")))
    P("Home Count", FS, "Count of homes", "should the slide add a real count of homes built or managed, with the real number added in Notes, or show no count?",
      o("count", "Add A Real Count", "XX homes is a SAMPLE placeholder. Add the real number in Notes.", "practical",
        zoom([(head,), (cred,), (lead,), (tiles, ["homes", "count", "econ", "ai"], ("count",)), (caption, "XX is a SAMPLE placeholder, not a real number", "Notes: how many homes have you built or managed?")])),
      o("none", "No Count", "No count, the licence and the tiles carry it.", "calm",
        zoom([(head,), (cred,), (lead,), (tiles, BASE4), (caption, "No count on the slide", "The licence and the tiles speak for it")])))
    return pairs
