#!/usr/bin/env python3
"""Main Deck Board Polish Deck (Branding, Oct 17 2026). Replacement for the Main Deck Board Layout Deck (Max submitted 20:47 ICT, 9/10;
picks applied to the Deck Building page, branding-djqmb410/decks/ + decks/board.js). Max asked for this follow-on (R83 lifted for it).
10 this-or-that picks on details that follow from his picks: ring style and colour, phone carousel peek + dots vs counter, card corner and
shadow at five across, Ask button wording, date format, remove-cross hover, NEW tag colour, Return link position, card hover, desktop wrap at 1024.
Option A is always what the board does now (after the applied picks); B is the alternative. Captions follow R105
('Main Deck Board: <element>, <one sentence>'), guarded by tools/caption_rule.py. No Thai references (R110).
usage: build_main_deck_board_polish.py -> prints {deckId, slug, url}; page written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from draft_svg import t, rect, ln, dot, screen, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import deck, publish
import caption_rule
DID = "main-deck-board-polish"; NAME = "Main Deck Board Polish Deck"
CREAM, GREY, TRACK = "#FAF6EE", "#A3A3A3", "#EEEBE5"
DECKS = [("Visit Photos", "UpKeep", 3, "Oct 17", "today"), ("Roselle Packaging", "WellNest", 0, "Oct 17", "today"),
         ("Tea Blends", "WellNest", 6, "Oct 16", "1 day ago"), ("Investor Pitch", "UpKeep", 0, "Oct 16", "1 day ago"),
         ("Partner Packs", "Blog", 2, "Oct 15", "2 days ago"), ("Jokes Set List", "Jokes", 0, "Oct 15", "2 days ago"),
         ("Mixed Deck", "Branding", 0, "Oct 14", "3 days ago"), ("Member Profile", "UpKeep", 5, "Oct 14", "3 days ago"),
         ("Calm Line Labels", "WellNest", 0, "Oct 13", "4 days ago"), ("Order Form", "UpKeep", 1, "Oct 13", "4 days ago")]
AGC = {"UpKeep": TERRA, "WellNest": JUNGLE, "Blog": LAGOON, "Jokes": SAFFRON, "Branding": LAGOON}

def where(s, sub=""):  # R105: every mockup says exactly where it is
    return rect(0, 0, 240, 26, CREAM) + t(12, 17, s.upper(), 8, INK, "hind", 700, extra='letter-spacing="1"') + (t(228, 17, sub, 7.5, MUTE, anchor="end") if sub else "") + ln(26, 0, 240, LINE)
def title(y=46, waiting="49 Waiting"):
    return t(12, y, "DECK BUILDING", 15, INK, "khand", extra='letter-spacing="1"') + rect(112, y - 10, 46, 13, "#fbf3dc", "none", 6.5) + t(135, y - 1, waiting, 7, "#7a5c00", "hind", 600, "middle")
def ringsvg(cx, cy, r, n, tot, col=JUNGLE, sw=2.2):
    L = 2 * math.pi * r; s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TRACK}" stroke-width="{sw}"/>'
    if n: s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-dasharray="{L*n/tot:.1f} {L:.1f}" transform="rotate(-90 {cx} {cy})"/>'
    return s
def card(x, y, w, h, d, o=None):
    """one deck card as the board draws it now; o overrides a single detail"""
    o = o or {}; nm, ag, n, dt, rel = d; c = AGC.get(ag, TERRA); fs = o.get("fs", 8.5 if w < 60 else 10)
    rad = o.get("r", 4); s = ""
    if o.get("shadow"): s += rect(x + .8, y + 1.6, w, h, "#0A0A0A", "none", rad, extra='opacity=".10"')
    s += rect(x, y, w, h, "#FFFFFF", o.get("border", LINE), rad, o.get("bw", 1)) + rect(x + (rad * .4), y, w - rad * .8, 2.2, c, "none", 0)
    words, line, lines = nm.split(), "", []
    for wd in words:
        if len((line + " " + wd).strip()) * fs * .47 > w - 16 and line: lines.append(line); line = wd
        else: line = (line + " " + wd).strip()
    lines.append(line)
    for i, L in enumerate(lines[:2]): s += t(x + 5, y + 12 + i * fs * 1.05, L, fs, INK, "khand")
    iy = y + 14 + len(lines[:2]) * fs * 1.05
    when = rel if o.get("date") == "rel" else f"Asked {dt}"
    s += t(x + 5, iy, (ag if w < 60 else f"{ag} \u00b7 {when}") if not o.get("info_only_date") else when, 6 if w < 60 else 7, MUTE, "hind", 600)
    if w < 60 and not o.get("no_date_line"): s += t(x + 5, iy + 7, when if o.get("date") == "rel" else dt, 5.5, MUTE)
    by = y + h - 8; tot = 10; rs = o.get("ring", "thin")
    sm = w < 60
    if rs == "thin": s += ringsvg(x + 8, by, 3.8 if sm else 4.6, n, tot, JUNGLE, 1.6 if sm else 1.8) + t(x + 14, by + 2.3, f"{n}/{tot}", 6.5 if sm else 8.5, JUNGLE, "khand")
    elif rs == "bold": s += ringsvg(x + 9, by - 1, 5.4, n, tot, c, 3.2) + t(x + 9, by + 1.2, f"{n}", 5.5, c, "khand", anchor="middle") + ("" if sm and n == 0 else t(x + 17, by + 2.2, f"of {tot}", 5.5 if sm else 7, MUTE, "hind", 600))
    if n == 0 and not o.get("no_new"):
        bg, fg, bd = o.get("newc", (CREAM, TERRA, "#e3ddd2")); nw = 13 if sm else 18
        s += rect(x + w - nw - 2.5, by - 4.5, nw, 8, bg, bd, 0, .7) + t(x + w - 2.5 - nw / 2, by + 1.4, "NEW", 5 if sm else 6, fg, "khand", anchor="middle")
    xs = o.get("x", "rest")
    if xs == "rest": s += t(x + w - 5, y + 11, "\u00d7", 9, GREY, "hind", 500, "end")
    elif xs == "terra": s += rect(x + w - 13, y + 1, 12, 12, CREAM, "none", 0) + t(x + w - 4.5, y + 10.5, "\u00d7", 9.5, TERRA, "hind", 600, "end")
    elif xs == "circle": s += dot(x + w - 8, y + 8, 5.5, "#E5E5E5") + t(x + w - 8, y + 10.8, "\u00d7", 8.5, INK, "hind", 700, "middle")
    return s
def grid(y0, cols, gap, margin, n, h, o=None, start=0, width=240):
    w = (width - 2 * margin - (cols - 1) * gap) / cols; s = ""
    for i in range(n):
        r, c = divmod(i, cols); s += card(margin + c * (w + gap), y0 + r * (h + gap), w, h, DECKS[(start + i) % len(DECKS)], o)
    return s
def desk(sub, body): return where("Main Deck Board \u00b7 Desktop", sub) + body
def phone(body, sub=""):
    return where("Main Deck Board \u00b7 Phone", sub) + rect(50, 34, 140, 262, "#FFFFFF", "#BDB6AA", 14, 1.4) + body
def toast(): return rect(70, 270, 100, 18, INK, "none", 9) + t(84, 282, "Removed \u00b7", 7.5, "#FFFFFF", "hind", 600) + t(156, 282, "Undo", 7.5, "#FFFFFF", "hind", 700, "end")

pairs, O, add = deck("mdbp_", "Branding")
_n = [0]
def P(g, ask, a, b):
    _n[0] += 1; k = f"{_n[0]:02d}_"
    add(g, g, O(k + a[0], *a[1:4], a[4]), O(k + b[0], *b[1:4], b[4]), ask)

# 1 Ring style and colour
def ring_pick(kind):
    zoom = card(20, 40, 200, 96, DECKS[0], {"ring": kind, "fs": 15})
    big = (ringsvg(46, 112, 11, 3, 10, JUNGLE, 3.4) + t(64, 117, "3/10", 15, JUNGLE, "khand")) if kind == "thin" else \
          (ringsvg(46, 110, 13, 3, 10, TERRA, 6.5) + t(46, 115, "3", 12, TERRA, "khand", anchor="middle") + t(66, 115, "of 10", 11, MUTE, "hind", 600))
    zoom = rect(20, 40, 200, 96, "#FFFFFF", LINE, 6) + rect(22, 40, 196, 3, TERRA) + t(30, 62, "Visit Photos", 15, INK, "khand") + t(30, 78, "UpKeep \u00b7 Asked Oct 17", 9, MUTE, "hind", 600) + big + t(212, 56, "\u00d7", 12, GREY, "hind", 500, "end")
    return screen(desk("one card, close up", zoom + t(20, 154, "Five across:", 8, MUTE, "hind", 600) + grid(162, 5, 3, 8, 10, 56, {"ring": kind})))
P("Ring", "Main Deck Board: Progress ring, thin green with 3/10 beside it or bold in the agent's colour?",
  ("thin", "Thin Green Ring", "As now: slim green ring, '3/10' beside it in green.", "calm", ring_pick("thin")),
  ("bold", "Bold Agent Ring", "Thicker ring in the agent's colour, the number inside, 'of 10' beside.", "lively", ring_pick("bold")))

# 2 Phone carousel peek + dots vs counter
def car(kind):
    cw = 106 if kind == "wide" else 120; s = ""
    for i in range(2): s += card(58 + i * (cw + 6), 92, cw, 92, DECKS[i], {"fs": 11})
    s = '<clipPath id="ph"><rect x="51" y="35" width="138" height="260" rx="13"/></clipPath><g clip-path="url(#ph)">' + s + "</g>"
    s += t(58, 56, "DECK BUILDING", 11, INK, "khand", extra='letter-spacing="1"') + t(58, 72, "49 Waiting \u00b7 26 Finished", 7, MUTE, "hind", 600)
    if kind == "wide":
        for i in range(10): s += rect(84 + i * 7.5, 196, 4.5, 4.5, INK if i == 0 else "#e3ddd2")
        s += t(120, 222, "about 1/5 of the next card shows", 6.5, MUTE, anchor="middle")
    else:
        s += t(120, 202, "1 of 49", 8.5, MUTE, "hind", 600, "middle") + t(120, 222, "a slim edge of the next card shows", 6.5, MUTE, anchor="middle")
    return screen(phone(s, "393 wide"))
P("Phone Carousel", "Main Deck Board: Phone carousel, a wide peek with dots or a slim peek with a '1 of 49' counter?",
  ("wide", "Wide Peek With Dots", "Card about 4/5 of the screen, next one clearly peeks, 10 square dots.", "visual", car("wide")),
  ("slim", "Slim Peek With Counter", "Bigger card, a thin edge of the next one, '1 of 49' under it.", "focused", car("slim")))

# 3 Card corner + shadow at five across
def corner(kind):
    o = {"r": 4} if kind == "soft" else {"r": 0, "shadow": True}
    return screen(desk("five across", title() + grid(58, 5, 3, 8, 15, 62, o) + t(120, 290, "soft 10px corners, flat" if kind == "soft" else "square corners, light shadow", 7.5, MUTE, anchor="middle")))
P("Card Corners", "Main Deck Board: Card corners, soft and flat or square with a light shadow at five across?",
  ("soft", "Soft Corners, Flat", "As now: 10px corners like Ready To Swipe cards, thin border, no shadow.", "friendly", corner("soft")),
  ("square", "Square With Light Shadow", "Square corners like the rest of the board, a faint drop shadow.", "crisp", corner("square")))

# 4 Ask button wording (empty state)
def askw(word):
    s = desk("empty state", title(46, "0 Waiting") + rect(14, 62, 212, 70, CREAM, "#e3ddd2", 4) + t(26, 84, "No decks waiting right now.", 10, INK, "hind", 500))
    bw = 92 if word == "ASK FOR A DECK" else 80
    s += rect(26, 96, bw, 24, "#FFFFFF", INK, 0, 1.6) + t(26 + bw / 2, 112, word, 8.5, INK, "khand", anchor="middle", extra='letter-spacing="1"')
    s += t(14, 158, "Opens the Branding chat in the Grok Bot app.", 7.5, MUTE) + rect(14, 176, 212, 60, "#FFFFFF", "#05668D", 0, 1.4) + t(24, 194, "MIXED DECK", 10, INK, "khand")
    return screen(s)
P("Ask Button", "Main Deck Board: Ask button, 'Ask For A Deck' or 'Ask Branding' when the list is empty?",
  ("deck", "Ask For A Deck", "As now: says what you get.", "clear", askw("ASK FOR A DECK")),
  ("branding", "Ask Branding", "Says who you are asking.", "personal", askw("ASK BRANDING")))

# 5 Date format
def datef(kind):
    o = {"date": "rel"} if kind == "rel" else {}
    zoom = rect(20, 40, 200, 70, "#FFFFFF", LINE, 6) + rect(22, 40, 196, 3, JUNGLE) + t(30, 62, "Tea Blends", 15, INK, "khand") + \
           t(30, 80, "WellNest \u00b7 " + ("1 day ago" if kind == "rel" else "Asked Oct 16"), 10, MUTE, "hind", 600)
    return screen(desk("card info line", zoom + grid(126, 5, 3, 8, 10, 60, o, start=2) + t(120, 262, "Asked Oct 16" if kind != "rel" else "1 day ago", 9, INK, "hind", 600, "middle")))
P("Date Format", "Main Deck Board: Card date, 'Asked Oct 16' or a relative '1 day ago'?",
  ("abs", "Asked Oct 16", "As now: the calendar date Max asked.", "exact", datef("abs")),
  ("rel", "1 Day Ago", "How long ago, 'today', '2 days ago'.", "quick", datef("rel")))

# 6 Remove-cross hover
def xh(kind):
    zoom = rect(20, 40, 200, 96, "#FFFFFF", LINE, 6) + rect(22, 40, 196, 3, TERRA) + t(30, 64, "Investor Pitch", 15, INK, "khand") + t(30, 80, "UpKeep \u00b7 Asked Oct 16", 9, MUTE, "hind", 600) + ringsvg(38, 118, 6, 0, 10) + t(50, 122, "0/10", 10, JUNGLE, "khand")
    if kind == "terra": zoom += rect(188, 41, 31, 30, CREAM) + t(203.5, 62, "\u00d7", 18, TERRA, "hind", 600, "middle")
    else: zoom += dot(203, 57, 11, "#E5E5E5") + t(203, 62.5, "\u00d7", 16, INK, "hind", 700, "middle")
    zoom += f'<path d="M206 66 l0 12 l3 -3 l3 6 l2 -1 l-3 -6 l4 0 z" fill="#FFFFFF" stroke="{INK}" stroke-width=".8"/>'
    return screen(desk("mouse over the cross", zoom + t(20, 156, "At rest the cross is light grey; this is on hover.", 7.5, MUTE) + grid(166, 5, 3, 8, 5, 60, {"x": kind}) + toast()))
P("Remove Hover", "Main Deck Board: Remove cross hover, terracotta on beige or dark on a grey circle?",
  ("terra", "Terracotta On Beige", "As now: the grey cross turns terracotta on a beige corner.", "warm", xh("terra")),
  ("circle", "Dark On Grey Circle", "The cross turns dark inside a small grey circle.", "neutral", xh("circle")))

# 7 NEW tag colour
def newc(kind):
    nc = (CREAM, TERRA, "#e3ddd2") if kind == "beige" else (JUNGLE, "#FFFFFF", JUNGLE)
    zoom = rect(20, 40, 200, 96, "#FFFFFF", LINE, 6) + rect(22, 40, 196, 3, JUNGLE) + t(30, 64, "Roselle Packaging", 15, INK, "khand") + t(30, 80, "WellNest \u00b7 Asked Oct 17", 9, MUTE, "hind", 600) + ringsvg(38, 118, 6, 0, 10) + t(50, 122, "0/10", 10, JUNGLE, "khand")
    zoom += rect(172, 110, 38, 17, nc[0], nc[2], 0, 1) + t(191, 122, "NEW", 11, nc[1], "khand", anchor="middle", extra='letter-spacing=".6"')
    return screen(desk("until first click", zoom + grid(152, 5, 3, 8, 10, 60, {"newc": nc})))
P("New Tag", "Main Deck Board: NEW tag colour, terracotta on beige or white on jungle green?",
  ("beige", "Terracotta On Beige", "As now: light beige tag, terracotta capitals.", "soft", newc("beige")),
  ("green", "White On Green", "Solid jungle-green tag, white capitals, stands out more.", "bold", newc("green")))

# 8 Return link position
def retpos(kind):
    s = where("Main Deck Board \u00b7 Desktop", "top of the page")
    if kind == "header":
        s += t(12, 46, "\u2190 Return to", 8.5, LAGOON, "hind", 500) + t(60, 46, "Branding", 8.5, LAGOON, "hind", 700) + t(102, 46, "Branding Agent", 10, INK, "khand") + t(228, 46, "Updated 8:47 PM ICT", 6.5, MUTE, anchor="end") + ln(56, 0, 240)
        s += title(78) + grid(92, 5, 3, 8, 10, 60)
    else:
        s += t(12, 46, "Branding Agent", 10, INK, "khand") + t(228, 46, "Updated 8:47 PM ICT", 6.5, MUTE, anchor="end") + ln(56, 0, 240)
        s += t(12, 74, "\u2190 Return to", 8.5, LAGOON, "hind", 500) + t(60, 74, "Branding", 8.5, LAGOON, "hind", 700) + title(98) + grid(110, 5, 3, 8, 10, 56)
    return screen(s)
P("Return Link", "Main Deck Board: Return link, in the header row or on its own line above the title?",
  ("header", "In The Header Row", "As now: top left, next to 'Branding Agent'.", "tidy", retpos("header")),
  ("above", "Above The Title", "Its own line under the header, right above 'Deck Building'.", "obvious", retpos("above")))

# 9 Card hover
def hov(kind):
    s = desk("mouse over a card", title())
    s += grid(58, 5, 3, 8, 10, 62)
    hx, hy, hw = 8 + 2 * (43.2 + 3), 58, 43.2
    if kind == "lift":
        s += rect(hx - 1, hy - 3, hw + 2, 64, "#FFFFFF", "none", 4) + card(hx - 1, hy - 3, hw + 2, 64, DECKS[2], {"shadow": True, "r": 4})
        s += t(120, 228, "Card lifts 1px with a soft shadow.", 8, MUTE, anchor="middle")
    else:
        s += rect(hx, hy, hw, 62, "#FFFFFF", "none", 4) + card(hx, hy, hw, 62, DECKS[2], {"border": INK, "bw": 1.4, "r": 4})
        s += t(120, 228, "Border turns dark, the card stays still.", 8, MUTE, anchor="middle")
    s += f'<path d="M{hx+30} {hy+40} l0 12 l3 -3 l3 6 l2 -1 l-3 -6 l4 0 z" fill="#FFFFFF" stroke="{INK}" stroke-width=".8"/>'
    return screen(s)
P("Card Hover", "Main Deck Board: Card hover, lift with a soft shadow or a darker border that stays still?",
  ("lift", "Lift With Shadow", "As now: rises 1px with a soft shadow.", "playful", hov("lift")),
  ("border", "Darker Border, Still", "The outline darkens; nothing moves.", "steady", hov("border")))

# 10 Desktop wrap at 1024
def wrap(kind):
    cols = 5 if kind == "five" else 4
    s = where("Main Deck Board \u00b7 1024 Wide", f"{cols} across") + rect(0, 26, 240, 274, "#FFFFFF") + title()
    s += grid(58, cols, 3, 8, cols * 3, 62 if cols == 5 else 64)
    s += t(120, 290, "five across from 1024 up" if cols == 5 else "four across until 1280, then five", 7.5, MUTE, anchor="middle")
    return screen(s)
P("Desktop Wrap", "Main Deck Board: Grid at 1024 wide, five across or four across until 1280?",
  ("five", "Five Across From 1024", "As now: five cards a row on a small laptop.", "efficient", wrap("five")),
  ("four", "Four Across Until 1280", "Roomier cards on a small laptop, five on bigger screens.", "roomy", wrap("four")))

caption_rule.guard(pairs, DID)
assert len(pairs) == 10, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt, "R110"
publish(DID, NAME, "Branding", pairs, {"brands": ["Main Deck Board Polish Deck: finishing details on the main deck board (Deck Building page) after the Main Deck Board Layout Deck picks",
        "Max asked for this follow-on deck (Oct 17 2026); R83 lifted for it"], "submit_agent": "branding",
        "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "topic": "deck-board", "deck_size": 10, "board": "branding",
        "audience": "Max", "requested": True, "caption_rule": "R105", "follows": "main-deck-board-layout"}, seed=10172, n=10)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "main-deck-board-polish-deck-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
