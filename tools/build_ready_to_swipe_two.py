#!/usr/bin/env python3
"""Build Style Swipe deck ready-to-swipe-deck-two (refill of up-next-deck, R64 skips #11 and #17 reworded first). Helpers copied from build_up_next_deck.py.
Original doc: deck up-next-deck (Oct 14 2026): Up Next Deck, 20 this-or-that pairs on how the 'Up Next' section
at the top of every agent dashboard should look and behave (3-5 ready 20-card decks, categories from the agent's project,
submitted deck replaced by a fresh one). Pattern from build_agent_dashboards_more.py (team_kit.publish, dash_kit).
Crisp: every label >= 8 viewBox units, vector SVG. Submit -> agent 'branding'. Drawn example mockups only."""
import sys, os, re, json; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, chev, phone
DID = "ready-to-swipe-deck-two"; NAME = "Ready To Swipe Deck Two"; MIN = 8
B = dict(name="Agent", bg="#FDFBF6", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=6, hw=600)
INK, MUTE, LN = B["ink"], B["mute"], B["line"]; ACC = B["acc"]; WH = "#FFFFFF"
pairs, O, add = deck("un_", NAME)
def P(grp, ask, a, b): add(grp, grp, O(*a), O(*b), ask)
def tx(x, y, s, sz=8, c=INK, h=False, w=None, a="start"): return T(B, x, y, s, max(sz, MIN), c, h, w, a)
def share(x, y): return f'<g transform="translate({x},{y}) scale(.5)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{INK}" stroke-width="2.2"/></g>'
def card(x, y, w, h, edge=None, st=LN): return R(x, y, w, h, WH, st, B["r"]) + (R(x, y, 3, h, edge, r=1.5) if edge else "")
def ln(x, y, w, c=MUTE + "55"): return R(x, y, w, 3, c, r=1.5)
def sec(y, s, x=14): return tx(x, y, s, 11, INK, True)
def pill(x, y, s, c, solid=False, a="start"):
    w = len(s) * 4.3 + 12; x = x - w if a == "end" else x
    return R(x, y - 9, w, 12, c if solid else c + "1F", r=6) + tx(x + w / 2, y, s, 8, WH if solid else c, w=600, a="middle")
def btn(x, y, w, s, c, solid=True): return R(x, y, w, 15, c if solid else WH, c, 7.5) + tx(x + w / 2, y + 10.5, s, 8, WH if solid else c, w=600, a="middle")
def hbar(x, y, w, f, c): return R(x, y, w, 4, LN, r=2) + (R(x, y, w * f, 4, c, r=2) if f else "")
ICP = ["M4 12 L12 4 L20 12 M7 10 V20 H17 V10", "M12 3 L14.5 9 L21 9.5 L16 14 L17.5 20.5 L12 17 L6.5 20.5 L8 14 L3 9.5 L9.5 9 Z", "M4 7 H20 M4 12 H20 M4 17 H14", "M12 4 A8 8 0 1 0 12.01 4 M12 8 V12 L15 14"]
def ic(x, y, k, c, s=12): return f'<g transform="translate({x-s/2},{y-s/2}) scale({s/24})"><path d="{ICP[k%4]}" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/></g>'
CATS = ["Layout", "Colour", "Wording", "Photos", "Pricing"]
def frame(body, title="Example Agent", c=TERRA):
    s = R(0, 0, W, 32, WH) + L(0, 32, W, 32, LN) + chev(12, 16, MUTE) + tx(18, 19, "Apps Home", 8, MUTE, w=600)
    s += tx(120, 21, title, 12, INK, True, a="middle") + share(212, 9) + D(170, 16, 2.5, c)
    s += body + tx(120, 293, "Built by Max Weberman", 8, "#8A8580", a="middle")
    return phone(B, s)
def rest(y, n=3):  # the rest of the dashboard, greyed
    s = sec(y, "Open Items")
    for i in range(n): s += card(14, y + 8 + i * 24, 212, 20) + ln(24, y + 17 + i * 24, 110)
    return s
def dk(x, y, w, h, i, title=None, cnt=True, bar=None, time=False, badge=None, icon=False, start=None, tag=True):
    c = ACC[i % 4]; t = title or f"{CATS[i % 5]} Deck"
    s = card(x, y, w, h) + R(x, y, w, 4, c, r=2)
    yy = y + 18
    if icon: s += ic(x + 14, yy - 3, i, c); s += tx(x + 24, yy, t, 9.5, INK, True)
    else: s += tx(x + 8, yy, t, 9.5, INK, True)
    if badge: s += pill(x + w - 6, y + 16, badge, badge_c.get(badge, JUNGLE), True, a="end") if w > 90 else ""
    yy += 13
    if tag: s += pill(x + 8, yy, CATS[i % 5], c); yy += 13
    if cnt: s += tx(x + 8, yy, "20 cards" + ("  |  4 min" if time else ""), 8, MUTE); yy += 9
    if bar is not None: s += hbar(x + 8, yy, w - 16, bar, c); yy += 8
    if start: s += btn(x + 8, y + h - 21, w - 16, start, c)
    return s
badge_c = {"New": JUNGLE, "Fresh": JUNGLE, "Just Added": LAGOON}
def row(x, y, i, right="20 cards", bar=None):
    c = ACC[i % 4]; s = card(x, y, 212, 24, c) + tx(x + 10, y + 15.5, f"{CATS[i % 5]} Deck", 9, INK, True) + tx(x + 204, y + 15.5, right, 8, MUTE, a="end")
    if bar is not None: s += hbar(x + 100, y + 11, 50, bar, c)
    return s
def carousel(y, n=3, w=96, h=96, **k):
    s = "".join(dk(14 + i * (w + 8), y, w, h, i, **k) for i in range(n))
    return s + "".join(D(108 + j * 8, y + h + 10, 2.5, INK if j == 0 else LN) for j in range(4))


# Ready To Swipe card per the settled look: title + tag, thin top stripe, small Start / Continue label, no icons, no time
def rc(x, y, w, h, i, title=None, label="Start", stripe=3, tagstyle="pill", tagcol=True, rad=6, cnt=None, new=False, stack=False, clamp=True, outline=None):
    c = ACC[i % 4]; t = title or f"{CATS[i % 5]} Deck"
    s = R(x, y, w, h, WH, outline or LN, rad, 1.6 if outline else 1) + R(x, y, w, stripe, c, r=min(rad, 2))
    if stack: s = R(x + 4, y + 4, w, h, WH, LN, rad) + R(x + 2, y + 2, w, h, WH, LN, rad) + s
    words = t.split(); l1 = " ".join(words[:2]); l2 = " ".join(words[2:])
    s += tx(x + 8, y + 18, l1, 9.5, INK, True) + (tx(x + 8, y + 29, l2 if clamp else "", 9.5, INK, True) if l2 else "")
    ty = y + (42 if l2 and clamp else 32)
    if tagstyle == "pill": s += pill(x + 8, ty, CATS[i % 5], c if tagcol else MUTE)
    else: s += tx(x + 8, ty, CATS[i % 5].upper(), 8, c if tagcol else MUTE, w=600)
    if cnt: s += tx(x + 8, ty + 13, cnt, 8, MUTE)
    if label: s += tx(x + 8, y + h - 8, label, 8.5, JUNGLE, w=600) if label else ""
    if new: s += pill(x + w - 5, y + 16, "New", JUNGLE, True, a="end")
    return s
def strip(y, n=3, w=84, h=80, gap=6, x0=14, labels=None, **k):
    lab = k.pop("label", "Start")
    return "".join(rc(x0 + i * (w + gap), y, w, h, i, label=(labels[i] if labels else lab), **k) for i in range(n))
def head(y=52, done="2 done today", extra=""):
    return sec(y, "Ready To Swipe") + (tx(112, y, done, 8.5, MUTE) if done else "") + extra
def F(body): return frame(head() + body + rest(186))
def wide(body):  # big screen frame
    s = R(0, 0, W, 300, "#FDFBF6") + R(8, 40, 224, 150, "#1A1A1A", r=6) + R(12, 44, 216, 138, "#FDFBF6", r=3) + R(100, 190, 40, 14, "#1A1A1A") + R(80, 204, 80, 4, "#1A1A1A", r=2)
    s += tx(18, 58, "Ready To Swipe", 10, INK, True) + body + tx(120, 293, "Built by Max Weberman", 8, "#8A8580", a="middle") + tx(120, 24, "On A Laptop Or Big Monitor", 11, INK, True, a="middle")
    return phone(B, s)
# 1 (skip #11 reworded)
P("Big Screen", "On A Laptop Or Big Monitor: Show All 5 Decks Side By Side, Or Keep The Same Swipe Strip As The Phone?",
  ("bs_row", "All 5 Side By Side", "Every ready deck visible at once in one row; nothing to swipe.", "clear",
   wide("".join(rc(18 + i * 41.5, 66, 38, 60, i, title=["Layout", "Colour", "Words", "Photos", "Price"][i], label="Start", stripe=2) for i in range(5)))),
  ("bs_swipe", "Same Swipe Strip", "Bigger cards, the strip still scrolls sideways like on the phone.", "consistent",
   wide("".join(rc(18 + i * 72, 66, 66, 60, i, title=["Layout", "Colour", "Words"][i]) for i in range(3)) + "".join(D(104 + j * 8, 136, 2.5, INK if j == 0 else LN) for j in range(4)))))
# 2 (skip #17 reworded)
P("Card Size", "Showing Each Deck Is 20 Cards: Write '20 cards' On The Card, Or Draw A Small Stack Of Card Edges With No Words?",
  ("cs_words", "Write '20 cards'", "A small grey line under the tag says 20 cards.", "informative", F(strip(60, h=92, cnt="20 cards"))),
  ("cs_stack", "Card Edges, No Words", "The card looks like a little stack; no number written.", "visual", F(strip(60, h=86, w=80, stack=True))))
P("Tag", "Category Tag Colour: Same Colour As The Stripe Or Plain Grey?",
  ("tg_col", "Matches The Stripe", "Tag text picks up the stripe colour.", "colourful", F(strip(60))),
  ("tg_grey", "Plain Grey", "Stripe carries the colour; tag stays grey.", "calm", F(strip(60, tagcol=False))))
P("Tag", "Category Tag Shape: Soft Pill Or Small Capital Letters?",
  ("ts_pill", "Soft Pill", "Tag sits in a light rounded pill.", "friendly", F(strip(60))),
  ("ts_caps", "Small Capitals", "Tag as small spaced capitals, no pill.", "editorial", F(strip(60, tagstyle="caps"))))
P("Stripe", "Top Stripe: Hairline Or A Bit Thicker?",
  ("st_thin", "Hairline", "Very thin line of colour on top.", "subtle", F(strip(60, stripe=2))),
  ("st_thick", "A Bit Thicker", "Stripe is easier to spot at a glance.", "bold", F(strip(60, stripe=6))))
P("Card Shape", "Card Corners: Soft Rounded Or Nearly Square?",
  ("cr_soft", "Soft Rounded", "Rounded corners like the status pills.", "soft", F(strip(60, rad=10))),
  ("cr_sq", "Nearly Square", "Crisp corners like the deck buttons.", "crisp", F(strip(60, rad=2))))
P("Card Shape", "Long Deck Names: Wrap To Two Lines Or One Line Cut With '...'?",
  ("ln_wrap", "Wrap To Two Lines", "Full name shows, card a little taller.", "complete",
   F("".join(rc(14 + i * 90, 60, 84, 84, i, title=t) for i, t in enumerate(["Feed And Report Bars", "Layout And Decisions", "Swipe Controls Feed"])))),
  ("ln_cut", "One Line With ...", "Cards stay short; end of long names hidden.", "tidy",
   F("".join(rc(14 + i * 90, 60, 84, 70, i, title=t, clamp=False) for i, t in enumerate(["Feed And...", "Layout And...", "Swipe Con..."])))))
P("Start Label", "Small 'Start' Label: Bottom Left Or Bottom Right Of The Card?",
  ("sl_left", "Bottom Left", "Reads after the title and tag.", "natural", F(strip(60))),
  ("sl_right", "Bottom Right", "Sits in the corner like an arrow.", "directional",
   F(strip(60, label=None) + "".join(tx(14 + i * 90 + 76, 132, "Start", 8.5, JUNGLE, w=600, a="end") for i in range(3)))))
P("Started Decks", "A Started Deck: Just 'Continue', Or 'Continue, 12 left'?",
  ("sd_plain", "Just Continue", "Same card, the label simply says Continue.", "clean", F(strip(60, labels=["Continue", "Start", "Start"]))),
  ("sd_left", "Continue, 12 Left", "Shows how many cards are still to swipe.", "informative", F(strip(60, labels=["Continue, 12 left", "Start", "Start"]))))
P("Started Decks", "A Started Deck: Looks The Same As The Others, Or Gets A Thin Green Outline?",
  ("so_same", "Looks The Same", "Only the Continue label tells it apart.", "calm", F(strip(60, labels=["Continue", "Start", "Start"]))),
  ("so_green", "Thin Green Outline", "The started deck stands out at once.", "clear",
   F(rc(14, 60, 84, 80, 0, label="Continue", outline=JUNGLE) + "".join(rc(14 + i * 90, 60, 84, 80, i) for i in (1, 2)))))
P("Done Today", "Done Today Count: '2 done today' Or '2 of 5 done today'?",
  ("dt_n", "2 Done Today", "Just how many you finished today.", "light", F(strip(60))),
  ("dt_of", "2 Of 5 Done Today", "Shows progress against the shelf.", "motivating", frame(head(done="2 of 5 done today") + strip(60) + rest(186))))
P("Done Today", "Right After You Submit A Deck: It Vanishes, Or Shows Greyed 'Done' Until The New One Arrives?",
  ("ds_gone", "Vanishes", "Its slot waits for the refill.", "tidy", F(strip(60, n=2))),
  ("ds_grey", "Greyed 'Done'", "You see what you finished until the refill takes its place.", "reassuring",
   F(R(14, 60, 84, 80, "#F3F1EC", LN, 6) + tx(22, 78, "Layout Deck", 9.5, MUTE, True) + tx(22, 132, "Done", 8.5, MUTE, w=600) + "".join(rc(14 + i * 90, 60, 84, 80, i) for i in (1, 2)))))
P("New Badge", "Green 'New' Badge: In The Card Corner Or Before The Title?",
  ("nb_corner", "Card Corner", "Small badge top right.", "tidy", F(rc(14, 60, 84, 80, 0, new=True) + "".join(rc(14 + i * 90, 60, 84, 80, i) for i in (1, 2)))),
  ("nb_title", "Before The Title", "Badge leads the name so it reads first.", "loud",
   F(rc(14, 60, 84, 80, 0, title="      Layout Deck") + pill(22, 78, "New", JUNGLE, True) + "".join(rc(14 + i * 90, 60, 84, 80, i) for i in (1, 2)))))
P("Scroll Cue", "More Decks Off To The Side: Dots Under The Strip Or A Soft Fade At The Edge?",
  ("sc_dots", "Dots Underneath", "Small dots show how many there are.", "clear", F(strip(60) + "".join(D(104 + j * 8, 150, 2.5, INK if j == 0 else LN) for j in range(4)))),
  ("sc_fade", "Fade At The Edge", "The third card fades out to hint at more.", "minimal",
   F(strip(60) + '<defs><linearGradient id="fd"><stop offset="0" stop-color="#FDFBF6" stop-opacity="0"/><stop offset="1" stop-color="#FDFBF6"/></linearGradient></defs>' + R(196, 58, 44, 84, "url(#fd)"))))
P("Strip Edge", "On Phone: Strip Runs To The Screen Edge Or Stays Inside The Page Margins?",
  ("se_bleed", "Runs To The Edge", "Cards slide right off the screen edge.", "flowing", F(strip(60, x0=14, n=3, w=88))),
  ("se_in", "Inside The Margins", "Strip lines up with everything below it.", "orderly", F(strip(60, x0=14, n=3, w=66) )))
P("Section Box", "Ready To Swipe: Cards Sit Straight On The Page Or Inside One White Panel?",
  ("sb_open", "Straight On The Page", "No box around the strip; lighter.", "airy", F(strip(60))),
  ("sb_panel", "Inside A White Panel", "One white panel holds the label and the cards.", "contained",
   frame(R(8, 40, 224, 112, WH, LN, 8) + head() + strip(60, x0=16, w=82) + rest(186))))
P("Empty State", "All Caught Up Message: Words Only, Or Words Plus A Link To Deck Building?",
  ("es_words", "Words Only", "'All caught up. New decks are on the way.'", "calm",
   frame(head(done="") + card(14, 60, 212, 36) + tx(24, 82, "All caught up. New decks are on the way.", 8.5, MUTE) + rest(120))),
  ("es_link", "Words Plus A Link", "Adds a small 'See all decks' link to Deck Building.", "helpful",
   frame(head(done="") + card(14, 60, 212, 36) + tx(24, 76, "All caught up. New decks are on the way.", 8.5, MUTE) + tx(24, 89, "See all decks", 8.5, LAGOON, w=600) + rest(120))))
P("Header Link", "Next To The Label: A Small 'All Decks' Link, Or Nothing?",
  ("hl_link", "Small 'All Decks' Link", "Right side of the label, goes to Deck Building.", "handy", frame(head(extra=tx(226, 52, "All decks", 8.5, LAGOON, w=600, a="end")) + strip(60) + rest(186))),
  ("hl_none", "Nothing", "Label and done count only.", "clean", F(strip(60))))
P("Opening", "Tapping A Deck: Open In The Same Tab Or A New Tab?",
  ("op_same", "Same Tab", "Back button returns to the dashboard.", "simple", F(strip(60) + tx(120, 160, "Opens here, Back returns", 8, MUTE, a="middle"))),
  ("op_new", "New Tab", "Dashboard stays open behind the deck.", "parallel", F(strip(60) + tx(120, 160, "Opens in a new tab", 8, MUTE, a="middle"))))
P("Card Shape", "Card Height: Compact Strip Or A Bit Roomier?",
  ("ch_short", "Compact Strip", "Short cards so the dashboard starts sooner.", "compact", F(strip(60, h=64))),
  ("ch_tall", "A Bit Roomier", "Taller cards with more white space.", "roomy", F(strip(60, h=100))))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, NAME, "Branding", pairs,
        {"brands": ["Ready To Swipe Deck Two: refill of Up Next Deck. Cards 1-2 re-ask skipped #11 (big screen) and #17 (20-card size) in clearer words; 18 new open questions about the Ready To Swipe section"],
         "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "section_counts": cnt, "deck_size": N, "carried": 2, "topic": "ready-to-swipe",
         "follows": {"deck": "up-next-deck", "submission": "d62c7762", "answered": 18, "total": 20},
         "sources": {"results": "/workspace/style-swipe/results/up-next-deck.txt", "rulebook": "/workspace/ops/brand/dashboard-rulebook.md R66 Ready To Swipe"}},
        seed=1949, n=N, first=2)
