#!/usr/bin/env python3
"""Main Deck Board Layout Deck (Branding, Oct 17 2026; Max asked for "a deck for the main deck board"; R83 lifted for this one deck).
10 this-or-that picks on the BODY of the deck boards below the locked header divider: the Branding board's Max's Picks
section and the Deck Building page (branding-djqmb410/decks/) deck cards, plus the new deck-page Return button (R104).
New questions only (deck-board / deck-board-2 covered the old Deck Building page: ring vs bar, chips, featured card, etc.).
Captions follow R105 ('<Screen/App>: <Element>, <one sentence>'), guarded by tools/caption_rule.py.
usage: build_main_deck_board.py  -> prints {deckId, slug, url}; page written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from draft_svg import t, rect, ln, dot, screen, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import deck, publish
import caption_rule
DID = "main-deck-board-layout"; NAME = "Main Deck Board Layout Deck"
CREAM, BAND, DIV, GREY = "#FAF6EE", "#F1E6D6", "#d9d1c3", "#8A847C"
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
DECKS = [("UpKeep Visit Photos", "UpKeep", 3), ("Roselle Packaging", "WellNest", 0), ("Tea Blends", "WellNest", 6),
         ("Investor Pitch", "UpKeep", 0), ("Partner Packs", "Blog", 0), ("Thai Words Round", "Thai", 2),
         ("Mixed Deck", "Branding", 0), ("Customer Profile", "UpKeep", 0), ("Calm Line Labels", "WellNest", 0)]
AGC = {"UpKeep": TERRA, "WellNest": JUNGLE, "Blog": LAGOON, "Thai": SAFFRON, "Branding": LAGOON}

def where(s, sub=""):  # small location strip at the top of every mockup (R105: say exactly where this is)
    return rect(0, 0, 240, 26, CREAM) + t(12, 17, s.upper(), 8, INK, "hind", 700, extra='letter-spacing="1"') + (t(228, 17, sub, 7.5, MUTE, anchor="end") if sub else "") + ln(26, 0, 240, LINE)
def head(y, title="Max's Picks", sub="14 open"):
    return t(12, y + 14, title, 13, INK, "khand") + t(12 + len(title) * 6.6, y + 14, sub, 7.5, MUTE)
def xbtn(x, y, style="corner"):
    if style == "corner": return t(x, y, "\u00d7", 10, GREY, "hind", 600, "end")
    return ""
def newb(x, y, style="tag"):
    if style == "tag": return rect(x - 22, y - 8, 22, 10, CREAM, "#E8D9C6", 0) + t(x - 11, y - .5, "NEW", 7.5, TERRA, "khand", anchor="middle")
    if style == "dot": return dot(x, y, 3.2, TERRA)
    return ""
def card(x, y, w, h, nm, ag, n, o=None):
    o = o or {}; c = AGC.get(ag, TERRA); s = rect(x, y, w, h, "#FFFFFF", LINE, 6) + rect(x + 1, y, w - 2, 2.5, c, "none", 1)
    fs = o.get("fs", 9); s += t(x + 6, y + 14, nm if len(nm) * fs * .5 < w - 16 else nm[: int((w - 18) / (fs * .5))] + "\u2026", fs, INK, "khand")
    info = o.get("info", "tag"); yy = y + 25
    if info == "tag": s += rect(x + 6, yy - 7, len(ag) * 4.4 + 10, 10, "#F1EEE9", "none", 5) + t(x + 11, yy + .5, ag, 7.5, MUTE, "hind", 600)
    elif info == "count": s += t(x + 6, yy + 1, f"{ag} \u00b7 10 picks", 7.5, MUTE, "hind", 600)
    elif info == "date": s += t(x + 6, yy + 1, f"{ag} \u00b7 Asked Oct 17", 7.5, MUTE, "hind", 600)
    pr = o.get("prog", "text"); by = y + h - 7
    if pr == "bar":
        s += rect(x + 6, by - 2, w - 12, 3, "#EEEAE4", "none", 1.5) + rect(x + 6, by - 2, (w - 12) * n / 10, 3, JUNGLE, "none", 1.5)
        s += t(x + 6, by - 6, f"Continue, {10-n} left" if n else "Start", 7.5, JUNGLE, "hind", 600)
    elif pr == "ring":
        import math
        r = 6; cx, cy = x + w - 12, by - 5; L = 2 * math.pi * r
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEAE4" stroke-width="2.4"/>'
        if n: s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{JUNGLE}" stroke-width="2.4" stroke-dasharray="{L*n/10:.1f} {L:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        s += t(x + 6, by - 2, f"{n}/10", 8, JUNGLE, "khand")
    elif pr == "text": s += t(x + 6, by - 2, f"Continue, {10-n} left" if n else "Start", 7.5, JUNGLE, "hind", 600)
    if o.get("new", n == 0) and o.get("newstyle", "tag") == "tag": s += newb(x + w - 4, y + h - 4)
    if o.get("new", n == 0) and o.get("newstyle") == "dot": s += newb(x + w - 9, y + 11, "dot")
    rm = o.get("rm", "corner")
    if rm == "corner": s += xbtn(x + w - 4, y + 12)
    elif rm == "link": s += t(x + w - 6, y + h - 5, "Remove", 7.5, GREY, "hind", 600, "end", 'text-decoration="underline"')
    return s
def grid(y0, cols, gap, margin, n=6, h=46, o=None, decks=None):
    w = (240 - 2 * margin - (cols - 1) * gap) / cols; s = ""; L = decks or DECKS
    for i in range(n):
        r, c = divmod(i, cols); nm, ag, k = L[i % len(L)]; s += card(margin + c * (w + gap), y0 + r * (h + gap), w, h, nm, ag, k, o)
    return s, (n + cols - 1) // cols * (h + gap)
def desk(title_sub, body):  # wide-screen look: a laptop frame inside the picture
    return where("Branding Board \u00b7 Desktop", title_sub) + body
def phone_frame(body, label="Branding Board \u00b7 Phone"):
    return where(label) + rect(58, 34, 124, 258, "#FFFFFF", "#BDB6AA", 12, 1.4) + body

pairs, O, add = deck("mdb_", "Branding")
_n = [0]
def P(g, ask, a, b):
    _n[0] += 1; k = f"{_n[0]:02d}_"
    add(g, g, O(k + a[0], *a[1:4], a[4]), O(k + b[0], *b[1:4], b[4]), ask)

# 1 Desktop density (Max: boards feel too airy on desktop; wants moderate side margins and tighter gaps)
def dens(cols, gap, margin, fs, h):
    g, hh = grid(62, cols, gap, margin, n=cols * 3, h=h, o={"fs": fs})
    return screen(desk(f"{cols} across", rect(0, 26, margin, 274, CREAM) + rect(240 - margin, 26, margin, 274, CREAM) + head(34) + g
                       + t(120, 290, f"{margin*6}px sides \u00b7 {gap*2}px gaps", 7.5, MUTE, anchor="middle")))
P("Density", "Branding Board: Max's Picks on desktop, four cards across or five in a tighter grid?",
  ("4", "Four Across, Moderate Margins", "Bigger cards, 16px gaps, sides not too wide.", "calm", dens(4, 5, 12, 8.5, 54)),
  ("5", "Five Across, Tight Grid", "More decks per row, 10px gaps, slim sides.", "efficient", dens(5, 3.5, 7, 8, 48)))

# 2 Progress on the deck card
def prog(kind):
    g, _ = grid(70, 2, 8, 14, n=6, h=56, o={"prog": kind, "fs": 10}, decks=[DECKS[0], DECKS[5], DECKS[2], DECKS[1], DECKS[3], DECKS[4]])
    return screen(where("Deck Building Page", "deck cards") + t(14, 52, "Deck Building", 14, INK, "khand") + g)
P("Progress", "Deck Building Page: Deck card progress, a thin bar or a small ring with 3/10?",
  ("bar", "Thin Bar", "A slim green bar fills as you answer, with 'Continue, 7 left'.", "clear", prog("bar")),
  ("ring", "Ring With 3/10", "A small ring plus the count in words, no bar.", "compact", prog("ring")))

# 3 Card info under the name
def info(kind):
    g, _ = grid(70, 2, 8, 14, n=6, h=56, o={"info": kind, "fs": 10})
    return screen(where("Deck Building Page", "deck cards") + t(14, 52, "Deck Building", 14, INK, "khand") + g)
P("Card Info", "Deck Building Page: Deck card details, agent with pick count or agent with date asked?",
  ("count", "Agent And Pick Count", "For example 'UpKeep \u00b7 10 picks'.", "practical", info("count")),
  ("date", "Agent And Date Asked", "For example 'UpKeep \u00b7 Asked Oct 17'.", "timely", info("date")))

# 4 Grouping of Max's Picks
def one_list():
    g, _ = grid(62, 2, 8, 14, n=8, h=46)
    return screen(where("Branding Board", "Max's Picks") + head(34) + g)
def by_agent():
    s, y = where("Branding Board", "Max's Picks") + head(34), 58
    for ag, L in (("UpKeep", [DECKS[0], DECKS[3], DECKS[7]]), ("WellNest", [DECKS[1], DECKS[2], DECKS[8]])):
        s += rect(14, y, 4, 12, AGC[ag]) + t(22, y + 10, ag.upper() + f"  {len(L)}", 8, INK, "khand", extra='letter-spacing="1"'); y += 18
        g, hh = grid(y, 2, 8, 14, n=len(L), h=40, decks=L); s += g; y += hh + 4
    return screen(s)
P("Grouping", "Branding Board: Max's Picks, one list newest first or grouped by agent?",
  ("one", "One List, Newest First", "Every pick in one grid, the newest request at the top.", "simple", one_list()),
  ("agent", "Grouped By Agent", "A small heading per agent, newest first inside each group.", "organized", by_agent()))

# 5 Remove button
def rm(kind):
    g, _ = grid(62, 2, 8, 14, n=6, h=52, o={"rm": kind, "fs": 10})
    toast = rect(60, 266, 120, 22, INK, "none", 4) + t(76, 280, "Removed", 8, "#FFFFFF", "hind", 600) + t(166, 280, "UNDO", 8, SAFFRON, "khand", anchor="end")
    return screen(where("Branding Board", "Max's Picks") + head(34) + g + toast)
P("Remove", "Branding Board: Remove control, a grey cross in the corner or a Remove link at the bottom?",
  ("x", "Grey Cross, Top Right", "As now: a small \u00d7 in the corner, Undo for 5 seconds.", "minimal", rm("corner")),
  ("link", "Remove Link, Bottom Right", "The word Remove, underlined, same Undo toast.", "explicit", rm("link")))

# 6 New badge
def nb(kind):
    g, _ = grid(62, 2, 8, 14, n=6, h=52, o={"newstyle": kind, "fs": 10})
    return screen(where("Branding Board", "Max's Picks") + head(34) + g)
P("New Badge", "Branding Board: New badge, a small NEW tag or a terracotta dot by the name?",
  ("tag", "Small NEW Tag", "As now: beige tag, terracotta capitals, bottom right.", "clear", nb("tag")),
  ("dot", "Terracotta Dot", "A small dot by the name, gone once you open it.", "quiet", nb("dot")))

# 7 Empty state
def empty(kind):
    s = where("Branding Board", "Max's Picks") + t(12, 48, "Max's Picks", 13, INK, "khand") + t(80, 48, "0 open", 7.5, MUTE)
    s += rect(14, 62, 212, 96 if kind == "ask" else 52, CREAM, LINE, 6)
    s += t(120, 86, "No open picks right now.", 9.5, INK, "hind", 600, "middle")
    if kind == "ask":
        s += t(120, 102, "Ask for a deck and it lands here first.", 7.5, MUTE, anchor="middle")
        s += rect(70, 116, 100, 26, "#FFFFFF", INK, 0, 1.4) + t(120, 133, "ASK FOR A DECK", 8, INK, "khand", anchor="middle", extra='letter-spacing="1"')
    else: s += t(120, 100, "New requests show here.", 7.5, MUTE, anchor="middle")
    s += t(12, 190, "Swipe Data", 11, LAGOON, "khand") + ln(198)
    return screen(s)
P("Empty State", "Branding Board: Max's Picks empty state, one calm line or a line with an Ask button?",
  ("line", "One Calm Line", "'No open picks right now.' Nothing else.", "calm", empty("line")),
  ("ask", "Line Plus Ask Button", "Adds an Ask For A Deck button that opens chat.", "helpful", empty("ask")))

# 8 How finished decks leave
def leave(kind):
    g, _ = grid(62, 2, 8, 14, n=5, h=52, o={"fs": 10}, decks=[DECKS[1], DECKS[2], DECKS[3], DECKS[4], DECKS[6]])
    s = where("Branding Board", "Max's Picks") + head(34, sub="5 open") + g
    if kind == "flash":
        x, y, w = 14 + 106, 62 + 2 * 60, 98
        s += rect(x, y, w, 52, "#E3F1EA", JUNGLE, 6, 1.4) + t(x + w / 2, y + 24, "DONE", 12, JUNGLE, "khand", anchor="middle", extra='letter-spacing="1.5"') + t(x + w / 2, y + 38, "Leaving in 2 s", 7.5, JUNGLE, anchor="middle")
    else: s += t(120, 260, "Finished decks are gone the moment you submit.", 7.5, MUTE, anchor="middle")
    return screen(s)
P("Finished", "Branding Board: Finished decks, leave instantly or flash a short green Done first?",
  ("instant", "Leaves Instantly", "As now (R96): the card is gone right away.", "tidy", leave("instant")),
  ("flash", "Brief Done Flash", "A green Done for about 2 seconds, then it leaves.", "rewarding", leave("flash")))

# 9 Phone layout
def phone(kind):
    s = t(66, 54, "Max's Picks", 10, INK, "khand") + t(118, 54, "14 open", 7.5, MUTE)
    if kind == "one":
        for i in range(5):
            nm, ag, k = DECKS[i]; s += card(66, 62 + i * 44, 108, 38, nm, ag, k, {"fs": 8.5})
    else:
        for i in range(8):
            r, c = divmod(i, 2); nm, ag, k = DECKS[i]; s += card(66 + c * 56, 62 + r * 56, 52, 50, nm.split()[0], ag, k, {"fs": 8, "info": "none"})
    return screen(phone_frame(s))
P("Phone", "Branding Board on phone: Max's Picks, one card per row or two side by side?",
  ("one", "One Column", "Full-width cards, one per row, easy to read.", "readable", phone("one")),
  ("two", "Two Up", "Two smaller cards per row, more picks on screen.", "dense", phone("two")))

# 10 Return button on the deck page (R104)
def ret(kind):
    s = where("Deck Page", "top of every deck")
    if kind == "button":
        s += rect(12, 36, 116, 26, "#FFFFFF", INK, 0, 1.4) + t(22, 53, "\u2190 RETURN TO UPKEEP", 8.5, INK, "khand", extra='letter-spacing=".8"')
    else:
        s += t(14, 53, "\u2190 Return to", 8.5, LAGOON, "hind", 600) + rect(72, 42, 46, 14, LAGOON + "1A", "none", 7) + t(95, 52, "UpKeep", 7.5, LAGOON, "hind", 700, "middle")
    s += t(226, 53, "Submit", 8, JUNGLE, "khand", anchor="end") + rect(12, 70, 216, 3, "#EEEAE4") + rect(12, 70, 70, 3, JUNGLE)
    s += rect(12, 82, 216, 150, "#FFFFFF", LINE, 10) + t(22, 100, "UpKeep Member App: Visit photos, \u2026", 8, INK, "khand")
    s += rect(22, 108, 96, 112, CREAM, LINE, 8) + rect(124, 108, 94, 112, CREAM, LINE, 8)
    s += rect(12, 242, 60, 22, "#FFFFFF", INK, 0, 1.2) + t(42, 257, "\u2039 BACK", 8, INK, "khand", anchor="middle") + t(80, 257, "previous card (stays as is)", 7.5, MUTE)
    return screen(s)
P("Return Button", "Deck Page: Return button, an outlined button or a light text link with the board name?",
  ("btn", "Outlined Button", "'\u2190 Return To UpKeep' in a square outlined button.", "clear", ret("button")),
  ("link", "Text Link With Name", "'\u2190 Return to' plus a small board-name chip.", "light", ret("link")))

caption_rule.guard(pairs, DID)
assert len(pairs) == 10, len(pairs)
publish(DID, NAME, "Branding", pairs, {"brands": ["Main Deck Board Layout Deck: the body of the main deck board below the locked header, Branding board Max's Picks and the Deck Building page deck cards, plus the deck page Return button",
        "Max asked for this deck (Oct 17 2026, via Grok Bot); R83 lifted for this deck only"], "submit_agent": "branding",
        "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "topic": "deck-board", "deck_size": 10, "board": "branding",
        "audience": "Max", "requested": True, "caption_rule": "R105"}, seed=1017, n=10)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "main-deck-board-layout-deck-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
