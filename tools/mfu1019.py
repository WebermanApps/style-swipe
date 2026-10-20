"""Machan and End Screen follow-up decks, Oct 19 2026 (Max: 'remake any deck that was swiped on'; Branding results from Oct 18 never acted on).
  Machan Look Refinements      <- Machan: Look And Personality (22:54 ICT): two leaves, wink at rest, blush, flat terracotta, no footer tagline,
                                  wink on hover, leaf divider, sapling empty state. Refines each winner and settles the wink-at-rest vs wink-on-hover clash.
  Machan Origin Story Refinements <- Machan: Origin Story (22:57:57 ICT): both lead lores, both tones, the wish as lead tagline (not 'Small fruit,
                                  big nerve'), Read the seed second, tiger tale first, one short footer line, just Machan, seven-slide carousel,
                                  Nagasaki both ways, close on one line. New tiger lines, new Nagasaki treatments, new orderings.
  End Screen Refinements       <- End Screen Deck (22:14 ICT): bottom placements won (sheet, toast, sticky bar); pill and square buttons; corners and
                                  density split. Head-to-heads between the bottom winners plus density, corners, button set, copy and summary.
Uses the v3 mark and frames from machan1018 (light cream, Khand/Hind). Five lore pieces only: Diospyros, the 事事如意 wish, the Korean tiger tale,
the Ozark seed forecast, the Nagasaki survivor tree. Story text says just Machan (Max's pick), never names Max."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
from md1018_kit import make
import machan1018 as M
from machan1018 import mark, look_card, footer_strip, frame, story_card, divider_card, empty_card, leaf_glyph, T, TALE, CR, BORD, HEAD, LEAD, GREY, LEAF1, LEAF2, BLUSH
from draft_svg import rect, ln, W, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, crisp
def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
# extra mark variants drawn by post-processing the v3 mark
def mk(**k): return dict(dict(cap="two", eyes="wink", blush=True, finish="flat"), **k)
def mark2(x, y, size, leaf="std", blush="dots", body=TERRA, eyes="wink", outline=False):
    s = mark(x, y, size, **mk(eyes=eyes, blush=blush != "none", body=body))
    if leaf == "big": s = s.replace("M24 10.2C22.6 6 19 3.8 15 4.4c.7 4 4 6.4 9 5.8z", "M24 10.2C22 5 17.6 2 12 3c1 5.4 5.6 8.2 12 7.2z").replace("M24 10.2C25.4 6 29 3.8 33 4.4c-.7 4-4 6.4-9 5.8z", "M24 10.2C26 5 30.4 2 36 3c-1 5.4-5.6 8.2-12 7.2z")
    if leaf == "tilt": s = s.replace('<path d="M24 10.2C25.4 6', '<path transform="rotate(14 24 10)" d="M24 10.2C25.4 6').replace('<path d="M24 10.2C22.6 6', '<path transform="rotate(14 24 10)" d="M24 10.2C22.6 6')
    if blush == "ovals": s = s.replace(f'<circle cx="15.2" cy="31.6" r="1.8" fill="{BLUSH}"/><circle cx="32.8" cy="31.6" r="1.8" fill="{BLUSH}"/>', f'<ellipse cx="15.2" cy="31.8" rx="2.6" ry="1.3" fill="{BLUSH}"/><ellipse cx="32.8" cy="31.8" rx="2.6" ry="1.3" fill="{BLUSH}"/>')
    if blush == "terra": s = s.replace(f'fill="{BLUSH}"', 'fill="#D9805F" fill-opacity=".55"')
    if outline: s = s.replace('<rect x="7" y="11" width="34" height="32" rx="14"', '<rect x="7" y="11" width="34" height="32" rx="14" stroke="#7A2E18" stroke-width="1.2"')
    return s
def big_card(note, label="Machan mark", **k):
    body = mark2(120 - 62, 32, 124, **k); f, h = footer_strip(178, {}); f = f.replace(mark(0, 0, 0)[:0], "")
    body += f; return frame(body, 178 + h + 54, label, note)
def sizes_card(note, **k):
    body = rect(0, 24, W, 200, CR) + T(14, 44, "SIZES: 96, 48, 24, 16 PX", 6.5, M.FAINT, w=700, extra='letter-spacing=".8"')
    x = 20
    for s_ in (96, 48, 24, 16): body += mark2(x, 140 - s_, s_, **k); x += s_ + 14
    body += T(120, 186, "Footer, favicon and app icon sizes", 8.5, LEAD, w=500, anchor="middle")
    return frame(body, 250, "Machan mark sizes", note)
def footer_card(note, rest="wink", hover="none", label="Machan footer"):
    body = rect(0, 24, W, 200, CR) + T(14, 44, "FOOTER: REST, THEN HOVER", 6.5, M.FAINT, w=700, extra='letter-spacing=".8"')
    for i, (lab, x) in enumerate((("At rest", 18), ("Hover", 128))):
        e = rest if i == 0 else ("open" if hover == "open" else "wink"); dy = -5 if (i == 1 and hover == "hop") else 0
        body += rect(x, 56, 94, 100, "#FFFFFF", TERRA if i else BORD, 8, 1.3 if i else 1) + mark(x + 23, 66 + dy, 48, **mk(eyes=e))
        if i == 1 and hover == "spark": body += "".join(f'<path d="M{x+76+dx} {70+dy2} l2 -4 l2 4 l-2 4 z" fill="{TERRA}"/>' for dx, dy2 in ((0, 0), (8, 14)))
        if i == 1 and hover == "tilt": body = body.replace(mark(x + 23, 66, 48, **mk(eyes=e)), f'<g transform="rotate(-8 {x+47} 90)">{mark(x + 23, 66, 48, **mk(eyes=e))}</g>')
        body += T(x + 47, 132, "Built by Machan", 7.5, GREY, anchor="middle") + T(x + 47, 150, lab.upper(), 7, TERRA if i else MUTE, w=700, anchor="middle")
    return frame(body, 230, label, note)
def divider2(note, style):
    body = rect(0, 24, W, 200, CR) + rect(14, 38, 212, 172, "#FFFFFF", BORD, 10) + T(28, 62, "What we built", 15, HEAD, "khand")
    body += "".join(rect(28, 72 + i * 10, w, 4, "#E9E2D6", "none", 2) for i, w in enumerate((176, 150, 164))); y = 124
    if style == "line": body += ln(y, 28, 104, "#E2D8C8") + ln(y, 136, 212, "#E2D8C8") + leaf_glyph(120, y, 1.2)
    if style == "pair": body += ln(y, 28, 98, "#E2D8C8") + ln(y, 142, 212, "#E2D8C8") + leaf_glyph(112, y, 1.0) + f'<g transform="translate(128,{y}) scale(-1,1)">{leaf_glyph(0, 0, 1.0)}</g>'
    if style == "solo": body += leaf_glyph(120, y, 1.4)
    if style == "left": body += leaf_glyph(36, y, 1.0) + ln(y, 50, 212, "#E2D8C8")
    body += T(28, 156, "What comes next", 15, HEAD, "khand") + "".join(rect(28, 166 + i * 10, w, 4, "#E9E2D6", "none", 2) for i, w in enumerate((168, 140, 120)))
    return frame(body, 260, "Machan divider", note)
def empty2(note, line="Made to keep growing.", pot=False, mascot=False):
    body = rect(0, 24, W, 230, CR) + rect(14, 38, 212, 200, "#FFFFFF", BORD, 10) + T(28, 60, "Your projects", 14, HEAD, "khand") + ln(68, 28, 212, "#EEE7DB")
    if pot: body += f'<path d="M104 150 h32 l-4 18 h-24 z" fill="{TERRA}"/>'
    else: body += f'<ellipse cx="120" cy="160" rx="34" ry="6" fill="#E9DCC8"/>'
    body += f'<path d="M120 152 C120 140 119 130 120 120" stroke="{LEAF1}" stroke-width="2.2" fill="none" stroke-linecap="round"/><path d="M120 134 C112 126 102 126 97 130 C102 138 112 140 120 134 Z" fill="{LEAF2}"/><path d="M120 124 C128 114 139 113 144 117 C139 126 128 129 120 124 Z" fill="{LEAF1}"/>'
    if mascot: body += mark(150, 128, 34)
    body += T(120, 190, "Nothing here yet.", 11, HEAD, w=600, anchor="middle") + T(120, 205, line, 8.5, TERRA, w=600, anchor="middle")
    return frame(body, 280, "Machan empty state", note)
def state_card(note, kind, variant):
    body = rect(0, 24, W, 230, CR) + rect(14, 38, 212, 200, "#FFFFFF", BORD, 10)
    if kind == "loading":
        if variant == "spin": body += f'<circle cx="120" cy="120" r="40" fill="none" stroke="#EADFCF" stroke-width="4"/><path d="M120 80 a40 40 0 0 1 40 40" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>' + mark(96, 96, 48)
        else: body += mark(96, 86, 48) + "".join(f'<circle cx="{108+i*12}" cy="152" r="3.5" fill="{[TERRA, LAGOON, JUNGLE][i]}"/>' for i in range(3))
        body += T(120, 196, "Loading your projects", 9, LEAD, anchor="middle")
    if kind == "done":
        body += mark(96, 72, 48, **mk(eyes="wink" if variant == "wink" else "open"))
        if variant == "check": body += f'<circle cx="146" cy="78" r="10" fill="{JUNGLE}"/><path d="M141 78 l4 4 l7 -8" stroke="#fff" stroke-width="2" fill="none"/>'
        body += T(120, 150, "All done.", 15, HEAD, "khand", anchor="middle") + T(120, 168, "May all things go as you wish.", 8.5, TERRA, w=600, anchor="middle")
    if kind == "404":
        body += mark(96, 70, 48, **mk(eyes="open" if variant == "look" else "wink"))
        body += T(120, 150, "This page wandered off.", 13, HEAD, "khand", anchor="middle") + T(120, 168, "Back to the start" if variant == "look" else "Machan will find it. Mostly.", 8.5, LEAD, anchor="middle")
    return frame(body, 280, f"Machan {kind} state", note)
def T_LOOK():
    pairs, P = make("machlook19_", "Branding"); P = M.equal(P); L = "Machan Mark Mockup"; F = "Machan Footer Mockup"
    P("Wink", F, "Resting face", "you picked both the wink at rest and wink on hover, so should the footer rest winking or rest with eyes open?",
      o("wink", "Rests Winking", "Always winking; hover adds a small hop.", "playful", lambda: footer_card(("Wink always on", "Hover hops"), "wink", "hop")),
      o("open", "Rests Eyes Open", "Eyes open at rest; he winks on hover.", "calm", lambda: footer_card(("Wink is a reward", "Hover winks"), "open", "wink")))
    P("Wink", F, "Hover motion", "if he rests winking, what should hover add?",
      o("tilt", "A Small Head Tilt", "He leans a few degrees and back.", "playful", lambda: footer_card(("Friendly lean", "Very subtle"), "wink", "tilt")),
      o("spark", "Two Tiny Sparkles", "Two terracotta sparkles blink beside him.", "lively", lambda: footer_card(("A little magic", "Still small"), "wink", "spark")))
    P("Leaves", L, "Leaf size", "should the two leaves stay their size or grow a little?",
      o("std", "Today's Leaves", "The v3 leaves as they are.", "calm", lambda: big_card(("As today", "Balanced"))),
      o("big", "Slightly Bigger Leaves", "Wider leaves, easier to read small.", "warm", lambda: big_card(("Reads better at 16 px", "A bit leafier"), leaf="big")))
    P("Leaves", L, "Leaf angle", "should the leaves sit level or tilt a touch to one side?",
      o("level", "Level Leaves", "Symmetrical, calm.", "calm", lambda: big_card(("Symmetrical", "Steady"))),
      o("tilt", "Tilted Leaves", "A small lean, a bit of personality.", "playful", lambda: big_card(("A bit jaunty", "Matches the wink"), leaf="tilt")))
    P("Blush", L, "Blush shape", "should the blush stay round dots or become soft ovals?",
      o("dots", "Round Dots", "Today's blush.", "calm", lambda: big_card(("As today", "Simple"))),
      o("ovals", "Soft Ovals", "Wider, softer cheeks.", "warm", lambda: big_card(("Softer", "More cheeky"), blush="ovals")))
    P("Blush", L, "Blush colour", "should the blush be peach or a light terracotta?",
      o("peach", "Peach Blush", "Today's peach.", "warm", lambda: big_card(("As today", "Gentle"))),
      o("terra", "Light Terracotta", "Ties to the body colour.", "calm", lambda: big_card(("Tonal", "Quieter"), blush="terra")))
    P("Colour", L, "Terracotta depth", "should the flat body stay brand terracotta or go one step deeper?",
      o("brand", "Brand Terracotta", "#C1502E, as today.", "calm", lambda: big_card(("As today", "On brand"))),
      o("deep", "Deeper Terracotta", "A richer, earthier shade.", "warm", lambda: big_card(("Earthier", "More contrast with cream"), body="#A9432A")))
    P("Colour", L, "Outline", "should the flat mark have no outline or a thin dark edge?",
      o("none", "No Outline", "Clean flat shapes.", "calm", lambda: big_card(("Clean", "As today"))),
      o("edge", "Thin Dark Edge", "Holds up on busy backgrounds.", "practical", lambda: big_card(("Sharper at small sizes", "A bit heavier"), outline=True)))
    P("Sizes", L, "Small-size version", "at 16 px should Machan keep his blush or drop it?",
      o("keep", "Keep Blush At All Sizes", "Same mark everywhere.", "calm", lambda: sizes_card(("One mark", "Busy at 16 px"))),
      o("drop", "Drop Blush When Tiny", "Cleaner favicon.", "practical", lambda: sizes_card(("Cleaner when small", "Two versions"), blush="none")))
    P("Footer", F, "Footer without a tagline", "with no tagline, should Built by Machan sit beside the mark or under it?",
      o("beside", "Beside The Mark", "One line, as today.", "calm", lambda: frame(rect(0, 24, W, 120, CR) + footer_strip(60, mk())[0], 150, "Machan footer", ("As today", "One line"))),
      o("under", "Under The Mark", "Mark centred, text below.", "warm", lambda: frame(rect(0, 24, W, 120, CR) + rect(10, 50, 220, 70, "#FFFFFF", BORD, 8) + mark(108, 58, 24) + T(120, 100, "Built by Machan", 11, GREY, anchor="middle"), 150, "Machan footer", ("Centred", "Taller footer"))))
    P("Divider", "Machan Divider Mockup", "Leaf divider style", "should the leaf sit in the middle of a line or stand alone?",
      o("line", "Leaf On A Line", "Hairlines either side.", "calm", lambda: divider2(("As drafted", "Structured"), "line")),
      o("solo", "Leaf Alone", "Just the leaf, no lines.", "minimal", lambda: divider2(("Lighter", "Floats"), "solo")))
    P("Divider", "Machan Divider Mockup", "Leaf divider count", "one leaf or a mirrored pair like his cap?",
      o("one", "One Leaf", "Simple.", "minimal", lambda: divider2(("Simple", "Quiet"), "line")),
      o("pair", "Mirrored Pair", "Echoes the two-leaf cap.", "warm", lambda: divider2(("Ties to the cap", "A little more"), "pair")))
    P("Empty", "Machan Empty State Mockup", "Sapling line", "which line should sit under the sapling?",
      o("grow", "Made To Keep Growing", "The Nagasaki lore line.", "warm", lambda: empty2(("Lore line", "As drafted"))),
      o("soon", "Something Will Grow Here", "Plainer and friendlier.", "friendly", lambda: empty2(("Plain and kind", "No lore"), "Something will grow here.")))
    P("Empty", "Machan Empty State Mockup", "Sapling with Machan", "should Machan appear beside the sapling?",
      o("solo", "Sapling Alone", "Calm, just the plant.", "calm", lambda: empty2(("Calm", "As drafted"))),
      o("with", "Machan Watching It Grow", "Small Machan next to the sapling.", "playful", lambda: empty2(("More character", "Busier"), mascot=True)))
    P("States", "Machan Loading Mockup", "Loading state", "should loading show Machan in a ring or three bouncing dots?",
      o("spin", "Machan In A Ring", "A terracotta arc spins around him.", "calm", lambda: state_card(("Calm motion", "Clear wait"), "loading", "spin")),
      o("dots", "Three Dots Under Him", "Brand-colour dots pulse.", "playful", lambda: state_card(("Playful", "Lighter"), "loading", "dots")))
    P("States", "Machan Done Mockup", "Done state", "when something finishes should Machan wink or show a small check?",
      o("wink", "A Wink", "The wink says done.", "playful", lambda: state_card(("Signature move", "No icon"), "done", "wink")),
      o("check", "Eyes Open Plus Check", "A jungle check beside him.", "practical", lambda: state_card(("Clearer", "More literal"), "done", "check")))
    P("States", "Machan Not Found Mockup", "Not found page", "should the not-found page be cheeky or plain and helpful?",
      o("cheeky", "Cheeky", "This page wandered off, with a wink.", "playful", lambda: state_card(("Fun", "On character"), "404", "wink")),
      o("plain", "Plain And Helpful", "Eyes open, a clear way back.", "calm", lambda: state_card(("Helpful", "Less personality"), "404", "look")))
    P("Leaves", L, "Stem length", "should the stem stay short or show a little more?",
      o("short", "Short Stem", "As today.", "calm", lambda: big_card(("As today", "Compact"))),
      o("long", "Slightly Longer Stem", "A visible stem lifts the leaves.", "playful", lambda: frame(mark2(58, 40, 124).replace('d="M24 11.6V9.4"', 'd="M24 11.6V7.4"').replace("M24 10.2C2", "M24 8.6C2", 2).replace("4 6.4 9 5.8z", "4 6.4 9 4.2z").replace("-4 6.4-9 5.8z", "-4 6.4-9 4.2z") + footer_strip(178, {})[0], 266, "Machan mark", ("A bit taller", "More plant-like"))))
    P("Sizes", L, "App icon background", "as an app icon should Machan sit on cream or on white?",
      o("cream", "Cream Tile", "Warm cream square.", "warm", lambda: frame(rect(0, 24, W, 200, CR) + rect(60, 50, 120, 120, "#FAF6EE", BORD, 26) + mark(78, 64, 84), 240, "Machan app icon", ("Warm", "Matches pages"))),
      o("white", "White Tile", "Crisp white square.", "calm", lambda: frame(rect(0, 24, W, 200, CR) + rect(60, 50, 120, 120, "#FFFFFF", BORD, 26) + mark(78, 64, 84), 240, "Machan app icon", ("Crisp", "Neutral"))))
    P("Footer", F, "Footer mark size", "should the footer mark stay 22 px or grow to 28 px?",
      o("22", "Keep It Small", "22 px, as today.", "minimal", lambda: frame(rect(0, 24, W, 120, CR) + footer_strip(60, mk())[0], 150, "Machan footer", ("As today", "Subtle"))),
      o("28", "A Little Bigger", "28 px, the wink reads better.", "warm", lambda: frame(rect(0, 24, W, 120, CR) + rect(10, 60, 220, 40, "#FFFFFF", BORD, 8) + mark(64, 66, 28) + T(98, 85, "Built by Machan", 11, GREY), 150, "Machan footer", ("Wink reads", "Slightly louder"))))
    return pairs
SC = "Story card"; C = "Machan Story Carousel Mockup"; I = "Machan Story Intro Card Mockup"; G = "Machan Signature Card Mockup"
GODS = "The persimmon genus is Diospyros, from Greek. It's often translated as \"fruit of the gods\" or \"divine fruit.\""
WISH = "In Chinese, persimmon (柿, shì) sounds like 事, \"matters.\" Two persimmons stand for 事事如意, may all things go as you wish."
TIGER = f"In the Korean folk tale \"{TALE},\" a tiger hears a mother quiet her crying baby with a gotgam, a dried persimmon, and flees."
SEED = "Ozark folk lore says to split a persimmon seed: a spoon means heavy snow, a knife bitter cold, a fork a mild winter."
NAGA = "A persimmon tree in Nagasaki survived the 1945 atomic bombing. Its saplings are now planted around the world as a symbol of peace."
def sc(note, kicker, head, body, foot=None, pos=None, **k): return lambda: story_card(SC, note, kicker, head, body, foot, pos=pos, **k)
def T_STORY():
    pairs, P = make("machstory19_", "Branding"); P = M.equal(P)
    P("Order", C, "Opening pair", "you liked both openers, so should the name come first and the wish second, or the other way?",
      o("gw", "Name, Then Wish", "Slide 01 Fruit of the gods, slide 02 the wish.", "playful", sc(("Grand, then warm", "Name first"), "01 The name", ["Fruit of", "the gods."], GODS, "Next: a wish for you.", (7, 1))),
      o("wg", "Wish, Then Name", "Slide 01 the wish, slide 02 Fruit of the gods.", "warm", sc(("Warm, then grand", "Wish first"), "01 The wish", ["May all things go", "as you wish."], WISH, "Next: the fruit of the gods.", (7, 1), glyph="事事如意")))
    P("Tone", I, "Tone mix", "you liked both tones, so should the intro be warm with one wink line or playful with one earnest line?",
      o("warm", "Warm With One Wink", "Kind lines, one cheeky ending.", "warm", sc(("Mostly warm", "One wink"), "Meet the mascot", ["Machan is a", "persimmon."], "Round, terracotta, two green leaves. He signs off on everything built here, and hopes it goes the way you wish.", "One eye is open. The other is winking.", (7, 0))),
      o("play", "Playful With One Earnest Line", "Cheeky lines, one sincere close.", "playful", sc(("Mostly playful", "One sincere line"), "Meet the mascot", ["Machan is a", "persimmon."], "Round, terracotta, slightly smug, caught mid-wink. Fruit of the gods, and he doesn't let it go to his head. Mostly.", "Underneath, he just wants your project to go well.", (7, 0))))
    P("Tiger", C, "Tiger slide line", "since you passed on Small fruit, big nerve, which closing line should the tiger tale get?",
      o("brave", "Braver Than He Looks", "A gentle courage line.", "warm", sc(("Gentle courage", "Tale first"), "03 The tiger", ["The tiger", "ran."], TIGER, "Braver than he looks.", (7, 3))),
      o("scary", "Not Scared Of Hard Things", "Courage said plainly.", "practical", sc(("Plain courage", "Tale first"), "03 The tiger", ["The tiger", "ran."], TIGER, "Not scared of the hard parts.", (7, 3))))
    P("Tiger", C, "Tiger headline", "should the tiger slide's headline be The tiger ran or Scarier than a tiger?",
      o("ran", "The Tiger Ran", "Story-first headline.", "playful", sc(("Story pulls in", "As picked"), "03 The tiger", ["The tiger", "ran."], TIGER, "Braver than he looks.", (7, 3))),
      o("scarier", "Scarier Than A Tiger", "Funny, sets up the twist.", "playful", sc(("Funnier hook", "Same tale"), "03 The tiger", ["Scarier than", "a tiger."], TIGER, "Braver than he looks.", (7, 3))))
    P("Nagasaki", C, "Nagasaki treatment", "you liked keeping the tree and keeping it light, so should the slide be short and gentle or a full slide?",
      o("short", "Short And Gentle", "Two calm lines, no dates.", "calm", sc(("Lighter touch", "Still there"), "05 The roots", ["Made to keep", "growing."], "A persimmon tree in Nagasaki lived through 1945. Its saplings now grow around the world.", None, (7, 5))),
      o("full", "Full Slide", "The whole story and its meaning.", "warm", sc(("Deeper", "Heavier"), "05 The roots", ["Made to keep", "growing."], NAGA, "Under the wink, Machan is about things that last.", (7, 5))))
    P("Nagasaki", C, "Nagasaki position", "should the tree be the last lore before the signature or sit in the middle?",
      o("last", "Last Lore", "Ends on the deepest root.", "warm", sc(("Strong close", "Heavier ending"), "05 The roots", ["Made to keep", "growing."], NAGA, None, (7, 5))),
      o("mid", "In The Middle", "Forecast ends the lore on a lighter note.", "calm", sc(("Lighter ending", "Tree still there"), "03 The roots", ["Made to keep", "growing."], NAGA, None, (7, 3))))
    P("Forecast", C, "Seed forecast line", "which line should close the seed forecast slide?",
      o("read", "Read The Seed", "Read the seed. Build for the season.", "practical", sc(("Your pick for line two", "Promise"), "04 The forecast", ["Reads what's", "coming."], SEED, "Read the seed. Build for the season.", (7, 4))),
      o("ahead", "Looks A Little Ahead", "A softer thinking-ahead line.", "calm", sc(("Softer", "Less slogan"), "04 The forecast", ["Reads what's", "coming."], SEED, "Machan looks a little way down the road first.", (7, 4))))
    P("Forecast", C, "Seed drawing", "should the forecast slide show the three seed shapes or just a split seed?",
      o("three", "Spoon, Knife, Fork", "Three small seed halves.", "playful", lambda: frame(rect(0, 24, W, 240, CR) + rect(14, 36, 212, 200, "#FFFFFF", BORD, 12) + T(28, 60, "04 THE FORECAST", 7.5, TERRA, w=700) + T(28, 88, "Reads what's coming.", 20, HEAD, "khand") + "".join(M.seed_glyph(60 + i * 60, 140, 2) + T(60 + i * 60, 180, ["Spoon", "Knife", "Fork"][i], 9, LEAD, anchor="middle") for i in range(3)), 290, SC, ("Teaches the lore", "Busier"))),
      o("one", "One Split Seed", "A single seed, big.", "minimal", lambda: frame(rect(0, 24, W, 240, CR) + rect(14, 36, 212, 200, "#FFFFFF", BORD, 12) + T(28, 60, "04 THE FORECAST", 7.5, TERRA, w=700) + T(28, 88, "Reads what's coming.", 20, HEAD, "khand") + M.seed_glyph(120, 150, 3.4), 290, SC, ("Simple", "Less to read"))))
    P("Wish", G, "Wish line styling", "should the lead tagline be plain or carry the 事事如意 characters?",
      o("plain", "Plain English", "May all things go as you wish.", "calm", lambda: M.close_card("one", ("Clean", "As picked"))),
      o("chars", "With The Characters", "Small 事事如意 above the line.", "warm", lambda: M.close_card("one", ("Shows the pun", "A little more")).replace('>THE SIGNATURE<', '>THE SIGNATURE  事事如意<')))
    P("Signature", G, "Closing slide", "you picked ending on one line, so should it be the wish alone or the wish plus a tiny Read the seed?",
      o("wish", "Wish Alone", "Built by Machan. May all things go as you wish.", "minimal", lambda: M.close_card("one", ("Cleanest", "One line"))),
      o("both", "Wish Plus Read The Seed", "Your two taglines, the second small.", "warm", lambda: M.close_card("one", ("Both winners", "Second is small")).replace("May all things go as you wish.</text>", "May all things go as you wish.</text>" + T(28, 172, "Read the seed. Build for the season.", 8.5, LEAD, w=500))))
    P("Footer", "Machan Footer Tooltip Mockup", "Footer blurb line", "your short blurb won, so should it say the wish or Read the seed?",
      o("wish", "Built By Machan, With A Wish", "May all things go as you wish.", "warm", lambda: M.blurb_card("short", ("As picked", "Lucky"))),
      o("seed", "Built By Machan, Read The Seed", "Read the seed. Build for the season.", "practical", lambda: M.blurb_card("short", ("Thinks ahead", "Practical")).replace("May all things go as you wish.", "Read the seed. Build for the season.")))
    P("Carousel", "Machan Story Page Mockup", "Slide count", "should the carousel stay seven slides or trim to six?",
      o("seven", "Seven Slides", "Intro, five lore, signature.", "lively", lambda: M.carousel_card(("All five lore", "As picked"))),
      o("six", "Six Slides", "Intro and signature merge.", "practical", lambda: M.carousel_card(("Shorter", "Intro joins signature")).replace("02 / 07", "02 / 06")))
    P("Carousel", "Machan Story Page Mockup", "Slide numbers", "should each slide show its number or just the dots?",
      o("num", "Numbers And Dots", "02 / 07 plus dots.", "practical", lambda: M.carousel_card(("Clear progress", "As drafted"))),
      o("dots", "Dots Only", "Cleaner top.", "minimal", lambda: M.carousel_card(("Cleaner", "Less info")).replace("02 / 07", "")))
    P("Intro", I, "Intro mark size", "should the intro slide show a big Machan or keep him small next to the text?",
      o("big", "Big Machan", "The mark leads the intro.", "playful", (lambda: frame(rect(0, 24, W, 280, CR) + rect(14, 36, 212, 240, "#FFFFFF", BORD, 12) + mark(70, 50, 100) + T(28, 186, "Machan is a persimmon.", 18, HEAD, "khand") + T(28, 206, "Two green leaves, a cream face and one wink.", 8.5, LEAD), 330, SC, ("Character first", "Less text room")))),
      o("small", "Small Machan", "Text leads, mark beside the footer line.", "calm", sc(("Text first", "As today"), "Meet the mascot", ["Machan is a", "persimmon."], "Round, terracotta, two green leaves, a cream face and one wink. He signs off on everything built here.", None, (7, 0))))
    P("Lore", C, "Name slide line", "which line should close the fruit of the gods slide?",
      o("mostly", "Doesn't Let It Go To His Head", "Mostly.", "playful", sc(("Cheeky", "As drafted"), "01 The name", ["Fruit of", "the gods."], GODS, "He doesn't let it go to his head. Mostly.", (7, 1))),
      o("wink", "A Little Divine, With A Wink", "Softer cheek.", "warm", sc(("Softer", "Ties to the wink"), "01 The name", ["Fruit of", "the gods."], GODS, "A little divine. Mostly wink.", (7, 1))))
    P("Lore", C, "Wish slide glyph", "should the wish slide show 事事如意 large or small?",
      o("small", "Small In The Corner", "A quiet glyph by the kicker.", "calm", sc(("Quiet", "As drafted"), "02 The wish", ["May all things go", "as you wish."], WISH, None, (7, 2), glyph="事事如意")),
      o("big", "Large Behind The Headline", "A soft terracotta watermark.", "bold", lambda: story_card(SC, ("Shows the pun", "More decorative"), "02 The wish", ["May all things go", "as you wish."], WISH, None, pos=(7, 2)).replace('<g clip-path', f'<text x="120" y="150" font-size="54" fill="{TERRA}" fill-opacity=".1" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif">事事如意</text><g clip-path', 1)))
    P("Naming", I, "Who Machan signs for", "you picked just Machan, so should the intro say built here or built across these projects?",
      o("here", "Everything Built Here", "As picked.", "calm", sc(("Short", "As picked"), "Meet the mascot", ["Machan is a", "persimmon."], "He signs off on everything built here.", None, (7, 0))),
      o("proj", "Across These Projects", "Hints he spans many projects.", "warm", sc(("Shows the reach", "Slightly longer"), "Meet the mascot", ["Machan is a", "persimmon."], "He signs off on every project in this family, with a wink.", None, (7, 0))))
    P("Format", "Machan Story Page Mockup", "Lore summary card", "after the carousel should there be a one-card summary of all five lore lines?",
      o("yes", "Add A Summary Card", "All five lore lines at the end.", "practical", lambda: M.single_card(("Quick recap", "Extra card"))),
      o("no", "No Summary", "Carousel only.", "minimal", lambda: M.carousel_card(("Simpler", "As picked"))))
    P("Tone", G, "Signature voice", "should the signature card say Built by Machan or Signed, Machan?",
      o("built", "Built By Machan", "Matches the footer.", "calm", lambda: M.close_card("one", ("Consistent", "As today"))),
      o("signed", "Signed, Machan", "A friendly sign-off.", "warm", lambda: M.close_card("one", ("Personal", "New phrase")).replace(">Built by<", ">Signed,<")))
    P("Carousel", "Machan Story Page Mockup", "Carousel motion", "should the story carousel loop on its own or move only when swiped?",
      o("auto", "Loops On Its Own", "Moves every few seconds, pauses on touch.", "lively", lambda: M.carousel_card(("Shows all lore", "Can feel busy")).replace("Swipe for the next story", "Loops on its own, tap to pause")),
      o("manual", "Swipe Only", "Stays put until you swipe.", "calm", lambda: M.carousel_card(("Calm", "As today"))))
    return pairs
# ---------------- End Screen Refinements ----------------
from draft_svg import t, screen
def es(note, kind="sheet", dens="compact", corner="square", btn="pill", acts=("Send to Swatch", "Copy", "Share"), head="All done", sub="20 of 20 answered", summary=False, extra="", dim=True, fade=False):
    s = rect(0, 0, W, 300, "#FFFFFF") + rect(0, 0, W, 26, "#FAF6EE") + t(12, 17, "STYLE SWIPE", 7.5, INK, "hind", 700) + ln(26, 0, W, LINE)
    s += rect(30, 50, 180, 130, "#F5F3EF", LINE, 10) + t(120, 120, "Deck finished", 10, MUTE, "hind", 600, "middle")
    r = 0 if corner == "square" else 12; br = {"pill": 13, "square": 2 if corner == "square" else 6}[btn]
    pad = 10 if dens == "compact" else 18; bh = 26 if dens == "compact" else 34
    def buttons(y, x0=16, w=208):
        g = ""; n = len(acts); bw = (w - (n - 1) * 6) / n
        for i, a in enumerate(acts): g += rect(x0 + i * (bw + 6), y, bw, bh, TERRA if i == 0 else "#FFFFFF", TERRA, br, 1.2) + t(x0 + i * (bw + 6) + bw / 2, y + bh / 2 + 3.5, a, 8, "#FFFFFF" if i == 0 else TERRA, "hind", 600, "middle")
        return g
    if kind == "sheet":
        hh = pad * 2 + 30 + bh + (24 if summary else 0); y0 = 300 - hh
        s += (rect(0, 0, W, 300, "#000000", extra='fill-opacity=".18"') if dim else "") + ('<g opacity=".55">' if fade else "") + rect(0, y0, W, hh + r, "#FFFFFF", LINE, r) + rect(108, y0 + 5, 24, 3, "#D6D0C6", "none", 2)
        s += t(16, y0 + pad + 12, head, 13, INK, "khand") + t(16, y0 + pad + 24, sub, 8, MUTE)
        if summary: s += "".join(rect(16 + i * 70, y0 + pad + 32, 64, 16, ["#0B6E4F", "#05668D", "#C1502E"][i] + "1A", "none", 8) + t(48 + i * 70, y0 + pad + 43, ["12 A", "6 B", "2 Both"][i], 7.5, ["#0B6E4F", "#05668D", "#C1502E"][i], "hind", 700, "middle") for i in range(3))
        s += buttons(y0 + pad + 30 + (24 if summary else 0)) + ("</g>" + t(120, y0 - 8, "Fading in", 7.5, TERRA, "hind", 600, "middle") if fade else "")
    elif kind == "bar":
        hh = bh + pad * 2; y0 = 300 - hh; s += rect(0, y0, W, hh, "#FFFFFF", LINE, r) + ln(y0, 0, W, LINE) + buttons(y0 + pad)
        s += t(120, 200, head, 14, INK, "khand", anchor="middle") + t(120, 214, sub, 8, MUTE, anchor="middle")
    elif kind == "toast":
        hh = bh + pad * 2 + 18; y0 = 300 - hh - 12; s += rect(12, y0, 216, hh, "#2A1D15", "none", r if r else 4) + t(24, y0 + pad + 9, head + "  ·  " + sub, 8.5, "#FAF6EE", "hind", 600)
        g = ""; n = len(acts); bw = (192 - (n - 1) * 6) / n
        for i, a in enumerate(acts): g += rect(24 + i * (bw + 6), y0 + pad + 16, bw, bh, "#FAF6EE" if i == 0 else "none", "#FAF6EE", br, 1) + t(24 + i * (bw + 6) + bw / 2, y0 + pad + 16 + bh / 2 + 3.5, a, 8, "#2A1D15" if i == 0 else "#FAF6EE", "hind", 600, "middle")
        s += g
    elif kind == "inline":
        s += rect(16, 190, 208, 90, "#FFFFFF", TERRA, r if r else 3, 1.4) + t(28, 210, head, 12, INK, "khand") + t(28, 222, sub, 8, MUTE) + buttons(236, 28, 184)
    return screen(s + extra)
def T_END():
    pairs, P = make("endscr19_", "Branding"); L = "Deck Page End Screen"
    E = lambda k, lab, desc, feel, note, **kw: (k, lab, desc, feel, es(note, **kw))
    P("Placement", L, "Bottom sheet or sticky bar", "both bottom styles won, so which should the end screen use?",
      E("sheet", "Bottom Sheet", "Slides up with a title and buttons.", "calm", "Bottom sheet"), E("bar", "Sticky Bottom Bar", "Buttons pinned to the bottom edge.", "practical", "Sticky bar", kind="bar"))
    P("Placement", L, "Bottom sheet or toast", "should the finish show as a bottom sheet or a dark bottom toast?",
      E("sheet", "Bottom Sheet", "Light sheet with buttons.", "calm", "Bottom sheet"), E("toast", "Bottom Toast", "Dark floating toast with buttons.", "bold", "Bottom toast", kind="toast"))
    P("Placement", L, "Toast or sticky bar", "should it be a floating toast or a full-width bar?",
      E("toast", "Floating Toast", "Floats above the edge.", "bold", "Floating toast", kind="toast"), E("bar", "Full-Width Bar", "Edge to edge.", "practical", "Full-width bar", kind="bar"))
    P("Placement", L, "Inline card fallback", "should the inline outline card stay as a backup under the deck?",
      E("inline", "Keep Inline Card", "Also shows under the last card.", "calm", "Inline card", kind="inline", dens="roomy"), E("none", "Bottom Only", "Only the bottom sheet.", "minimal", "Bottom sheet only"))
    P("Density", L, "Sheet density", "should the bottom sheet be compact or roomy?",
      E("c", "Compact Sheet", "Short, buttons close together.", "practical", "Compact sheet"), E("r", "Roomy Sheet", "More padding, taller buttons.", "calm", "Roomy sheet", dens="roomy"))
    P("Density", L, "Toast density", "should the toast be compact or roomy?",
      E("c", "Compact Toast", "Slim, quick.", "practical", "Compact toast", kind="toast"), E("r", "Roomy Toast", "Bigger tap targets.", "calm", "Roomy toast", kind="toast", dens="roomy"))
    P("Corners", L, "Sheet corners", "should the bottom sheet have square or rounded top corners?",
      E("sq", "Square Corners", "Crisp, like the kit.", "focused", "Square sheet"), E("rd", "Rounded Corners", "Softer, phone-native.", "calm", "Rounded sheet", corner="round"))
    P("Corners", L, "Bar corners", "should the sticky bar be square or rounded?",
      E("sq", "Square Bar", "Flush with the edge.", "focused", "Square bar", kind="bar"), E("rd", "Rounded Bar", "Rounded top edge.", "calm", "Rounded bar", kind="bar", corner="round"))
    P("Buttons", L, "Button shape", "pill buttons or square buttons inside the bottom sheet?",
      E("pill", "Pill Buttons", "Fully rounded ends.", "friendly", "Pill buttons"), E("sq", "Square Buttons", "Small corner radius.", "focused", "Square buttons", btn="square"))
    P("Buttons", L, "Button set", "three buttons or one main button plus a More link?",
      E("three", "Three Buttons", "Send, Copy, Share.", "practical", "Three buttons"), E("one", "One Main Button", "Send to Swatch, then More.", "minimal", "One main button", acts=("Send to Swatch", "More")))
    P("Buttons", L, "Main action wording", "should the main button say Send to Swatch or Send results?",
      E("sw", "Send To Swatch", "Names who gets it.", "warm", "Send to Swatch"), E("res", "Send Results", "Plain and general.", "calm", "Send results", acts=("Send results", "Copy", "Share")))
    P("Buttons", L, "Back link", "should the end screen add Back to Deck Building as a button?",
      E("no", "No Back Button", "Header link only.", "minimal", "No back button"), E("yes", "Back Button Added", "A fourth, quieter button.", "practical", "Back button", acts=("Send", "Copy", "Share", "Back")))
    P("Copy", L, "Headline", "should the headline say All done or Deck finished?",
      E("done", "All Done", "Short and friendly.", "warm", "All done"), E("fin", "Deck Finished", "Plain and clear.", "calm", "Deck finished", head="Deck finished"))
    P("Copy", L, "Sub-line", "should the sub-line count answers or thank Max?",
      E("count", "Answer Count", "20 of 20 answered.", "practical", "Answer count"), E("thanks", "A Thank-You", "Thanks, picks saved.", "warm", "Thank-you line", sub="Thanks, your picks are saved"))
    P("Summary", L, "Pick summary", "should the sheet show a small A, B and Both summary?",
      E("no", "No Summary", "Just the buttons.", "minimal", "No summary"), E("yes", "Small Summary Chips", "12 A, 6 B, 2 Both.", "practical", "Summary chips", summary=True))
    P("Summary", L, "Skipped reminder", "if cards were skipped should the sheet remind you?",
      E("quiet", "Quiet Count", "20 of 20, skipped not shown.", "minimal", "Quiet count"), E("remind", "Skipped Reminder", "2 skipped, go back?", "practical", "Skipped reminder", sub="18 answered, 2 skipped: go back?"))
    P("Motion", L, "Sheet entrance", "should the sheet slide up or fade in?",
      E("slide", "Slide Up", "Rises from the bottom.", "lively", "Slide up", extra=f'<path d="M210 200 v-14 m-5 5 l5 -5 l5 5" stroke="{TERRA}" stroke-width="1.6" fill="none"/>'),
      E("fade", "Fade In", "Appears in place.", "calm", "Fade in", fade=True))
    P("Motion", L, "Backdrop", "should the page dim behind the sheet or stay bright?",
      E("dim", "Dim Behind", "Focus on the sheet.", "focused", "Dim behind"), E("bright", "Stay Bright", "No dim layer.", "calm", "Stay bright", dim=False))
    P("Combo", L, "Best bottom combo", "roomy rounded sheet with pills or compact square bar with square buttons?",
      E("soft", "Roomy, Rounded, Pills", "Soft and friendly.", "friendly", "Roomy rounded pills", dens="roomy", corner="round"),
      E("crisp", "Compact, Square, Square", "Crisp and tight.", "focused", "Compact square bar", kind="bar", btn="square"))
    P("Combo", L, "Toast combo", "dark toast with pills or with square buttons?",
      E("pill", "Toast With Pills", "Rounded buttons in the toast.", "friendly", "Toast with pills", kind="toast", corner="round"), E("sq", "Toast With Squares", "Squared buttons in the toast.", "focused", "Toast with squares", kind="toast", btn="square"))
    return pairs
