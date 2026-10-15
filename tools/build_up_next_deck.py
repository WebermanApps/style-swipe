#!/usr/bin/env python3
"""Build Style Swipe deck up-next-deck (Oct 14 2026): Up Next Deck, 20 this-or-that pairs on how the 'Up Next' section
at the top of every agent dashboard should look and behave (3-5 ready 20-card decks, categories from the agent's project,
submitted deck replaced by a fresh one). Pattern from build_agent_dashboards_more.py (team_kit.publish, dash_kit).
Crisp: every label >= 8 viewBox units, vector SVG. Submit -> agent 'branding'. Drawn example mockups only."""
import sys, os, re, json; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, chev, phone
DID = "up-next-deck"; NAME = "Up Next Deck"; MIN = 8
B = dict(name="Agent", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
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

# 1 name
P("Name", "Section Name: 'Up Next' Or 'Ready To Swipe'?",
  ("nm_up", "Up Next", "Short label at the very top: Up Next.", "calm", frame(sec(52, "Up Next") + carousel(60) + rest(190))),
  ("nm_ready", "Ready To Swipe", "Label says what to do: Ready To Swipe.", "direct", frame(sec(52, "Ready To Swipe") + carousel(60) + rest(190))))
# 2 sub-label
P("Name", "Under The Label: A Small Line Like '4 decks ready' Or Nothing?",
  ("nm_sub", "Small Count Line", "Up Next, with '4 decks ready, 20 cards each' under it.", "informative",
   frame(sec(52, "Up Next") + tx(14, 66, "4 decks ready, 20 cards each", 8.5, MUTE) + carousel(74) + rest(200))),
  ("nm_bare", "Label Only", "Just the label; the cards speak for themselves.", "clean", frame(sec(52, "Up Next") + carousel(60) + rest(190))))
# 3 layout
P("Layout", "Deck Layout: Swipe Carousel Or Stacked List?",
  ("ly_car", "Swipe Carousel", "Cards side by side, swipe sideways inside the section; dots show more.", "playful", frame(sec(52, "Up Next") + carousel(60, start="Start") + rest(190))),
  ("ly_list", "Stacked List", "One row per deck, all visible top to bottom.", "focused", frame(sec(52, "Up Next") + "".join(row(14, 60 + i * 28, i) for i in range(4)) + rest(190))))
# 4 visible
P("Layout", "On Phone, How Many Decks Show At Once: One And A Peek Or Two And A Half?",
  ("vs_one", "One Big Card + Peek", "One wide card fills the width; the next one peeks in at the edge.", "bold",
   frame(sec(52, "Up Next") + dk(14, 60, 180, 110, 0, start="Start Deck", time=True) + dk(200, 60, 120, 110, 1) + "".join(D(108 + j * 8, 180, 2.5, INK if j == 0 else LN) for j in range(4)) + rest(196))),
  ("vs_two", "Two And A Half", "Smaller cards; two full and half of a third show.", "compact",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 90, 60, 84, 88, i) for i in range(3)) + rest(176))))
# 5 contents
P("Card Contents", "What Goes On Each Deck Card: Just Title And Tag Or Full Details?",
  ("cc_min", "Title + Category Tag", "Only the deck name and its category tag.", "clean",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 56, i, cnt=False) for i in range(3)) + rest(150))),
  ("cc_full", "Full Details", "Name, tag, '20 cards', time estimate and a progress bar.", "informative",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 90, i, time=True, bar=0) for i in range(3)) + rest(180))))
# 6 count
P("Card Contents", "Card Count: '20 cards' Written Out Or A Stack Of Card Edges?",
  ("ct_text", "'20 cards' In Words", "Small grey text under the title.", "plain",
   frame(sec(52, "Up Next") + carousel(60) + rest(190))),
  ("ct_stack", "Stacked Card Edges", "Each deck drawn as a small fanned stack, no number text.", "visual",
   frame(sec(52, "Up Next") + "".join(R(18 + i * 104 + 6, 66, 96, 80, WH, LN, 6) + R(18 + i * 104 + 3, 63, 96, 80, WH, LN, 6) + dk(14 + i * 104 + 0, 60, 96, 80, i, cnt=False) for i in range(3)) + rest(180))))
# 7 time estimate
P("Card Contents", "Time Estimate: Show 'About 4 min' On Each Card Or Leave It Off?",
  ("tm_on", "Show 'About 4 min'", "A clock icon and rough time on each card.", "helpful",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 80, i, cnt=False) + ic(26 + i * 104, 126, 3, MUTE, 10) + tx(36 + i * 104, 129, "About 4 min", 8, MUTE) for i in range(3)) + rest(180))),
  ("tm_off", "Leave It Off", "Cards show only name, tag and card count.", "clean", frame(sec(52, "Up Next") + carousel(60) + rest(190))))
# 8 partial
P("Progress", "A Started Deck: Progress Bar With '8 of 20' Or Moved First With 'Continue'?",
  ("pg_bar", "Progress Bar + '8 of 20'", "Stays in its spot; bar fills and shows 8 of 20.", "calm",
   frame(sec(52, "Up Next") + dk(14, 60, 96, 96, 0, cnt=False, bar=.4) + tx(22, 126, "8 of 20", 8, MUTE) + "".join(dk(14 + i * 104, 60, 96, 96, i) for i in (1, 2)) + rest(186))),
  ("pg_cont", "Moved First, 'Continue'", "Started deck jumps to the front with a Continue button.", "focused",
   frame(sec(52, "Up Next") + card(14, 60, 212, 50, TERRA) + tx(24, 78, "Layout Deck", 10, INK, True) + tx(24, 92, "8 of 20 done", 8, MUTE) + hbar(24, 98, 110, .4, TERRA) + btn(150, 78, 66, "Continue", TERRA) + "".join(row(14, 118 + j * 28, i) for j, i in enumerate((1, 2))) + rest(186))))
# 9 finished today
P("Progress", "Finished Today: A Small Count In The Header Or A Row Of Done Ticks?",
  ("ft_count", "Small Count By The Label", "'2 done today' in grey next to Up Next.", "quiet",
   frame(sec(52, "Up Next") + tx(226, 52, "2 done today", 8.5, JUNGLE, w=600, a="end") + carousel(60) + rest(190))),
  ("ft_ticks", "Row Of Done Ticks", "Small ticked chips for each deck finished today, under the cards.", "rewarding",
   frame(sec(52, "Up Next") + carousel(60) + tx(14, 184, "DONE TODAY", 8, MUTE, w=600) + "".join(R(70 + i * 62, 175, 56, 14, JUNGLE + "1F", r=7) + f'<path d="M{76+i*62} {182} l3 3 l5 -6" fill="none" stroke="{JUNGLE}" stroke-width="1.6"/>' + tx(88 + i * 62, 185, ["Colour", "Wording"][i], 8, JUNGLE, w=600) for i in range(2)) + rest(204, 2))))
# 10 phone vs desktop
desk_cards = lambda: "".join(R(14 + i * 54, 72, 50, 64, WH, LN, 5) + R(14 + i * 54, 72, 50, 4, ACC[i % 4], r=2) + tx(18 + i * 54, 90, CATS[i], 8.5, INK, True) + tx(18 + i * 54, 104, "20 cards", 8, MUTE) + btn(18 + i * 54, 114, 42, "Start", ACC[i % 4]) for i in range(4))
P("Phone vs Desktop", "On A Big Screen: All Decks In One Row Or Same Carousel As Phone?",
  ("pd_row", "All In One Row", "Desktop shows every ready deck side by side, no swiping.", "open",
   frame(tx(14, 52, "DESKTOP VIEW", 8, MUTE, w=600) + sec(66, "Up Next") + desk_cards() + R(14, 150, 212, 60, WH, LN, 6) + ln(24, 166, 120) + ln(24, 180, 90), "Big Screen")),
  ("pd_car", "Same Carousel", "Desktop keeps the carousel with arrows at both ends.", "consistent",
   frame(tx(14, 52, "DESKTOP VIEW", 8, MUTE, w=600) + sec(66, "Up Next") + desk_cards().replace("", "") + D(10, 104, 7, WH) + chev(10, 104, INK) + R(14, 150, 212, 60, WH, LN, 6) + ln(24, 166, 120) + D(230, 104, 8, WH) + f'<path d="M228 100 L232 104 L228 108" fill="none" stroke="{INK}" stroke-width="1.5"/>', "Big Screen")))
# 11 prominence
P("Prominence", "How Big Is Up Next: The Hero Of The Page Or A Slim Strip?",
  ("pr_hero", "Hero Of The Page", "Tall cards take the top half of the dashboard.", "bold",
   frame(sec(52, "Up Next") + dk(14, 60, 150, 140, 0, start="Start Deck", time=True, icon=True) + dk(172, 60, 120, 140, 1) + rest(220, 2))),
  ("pr_slim", "Slim Strip", "One short row of chips; the rest of the dashboard shows right away.", "light",
   frame(sec(52, "Up Next") + "".join(R(14 + i * 72, 60, 66, 26, WH, ACC[i], 13) + tx(47 + i * 72, 76, CATS[i], 8.5, ACC[i], w=600, a="middle") for i in range(3)) + rest(108, 6))))
# 12 start wording
P("Wording", "Start Button Wording: 'Start' Or 'Swipe'?",
  ("bt_start", "Start", "Plain button: Start.", "plain", frame(sec(52, "Up Next") + carousel(60, h=110, start="Start") + rest(204))),
  ("bt_swipe", "Swipe", "Action word that matches the app: Swipe.", "playful", frame(sec(52, "Up Next") + carousel(60, h=110, start="Swipe") + rest(204))))
# 13 tap target
P("Wording", "Opening A Deck: A Button On Each Card Or Tap Anywhere On The Card?",
  ("tp_btn", "Button On Each Card", "A clear Start button at the bottom of every card.", "explicit", frame(sec(52, "Up Next") + carousel(60, h=110, start="Start") + rest(204))),
  ("tp_any", "Tap Anywhere", "No button; whole card opens, a small arrow in the corner.", "clean",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 96, i) + f'<path d="M{96+i*104} 140 L{102+i*104} 146 L{96+i*104} 152" fill="none" stroke="{ACC[i]}" stroke-width="1.6"/>' for i in range(3)) + rest(190))))
# 14 fresh marker
P("Fresh Deck", "A Freshly Refilled Deck: Solid 'New' Badge Or A Soft Glow Border?",
  ("fr_badge", "Solid 'New' Badge", "Green New badge in the corner until opened.", "clear",
   frame(sec(52, "Up Next") + dk(14, 60, 140, 96, 0, badge="New", time=True) + dk(162, 60, 120, 96, 1) + rest(190))),
  ("fr_glow", "Soft Glow Border", "Fresh deck gets a coloured outline, no text badge.", "subtle",
   frame(sec(52, "Up Next") + R(11, 57, 146, 102, "none", JUNGLE + "66", 8, 3) + dk(14, 60, 140, 96, 0, time=True) + dk(162, 60, 120, 96, 1) + rest(190))))
# 15 replace animation behaviour
P("Fresh Deck", "When You Submit: New Deck Slides Into The Same Spot Or Joins At The End?",
  ("rp_same", "Same Spot", "The finished deck is swapped in place for a fresh one.", "steady",
   frame(sec(52, "Up Next") + dk(14, 60, 96, 96, 0, badge=None) + tx(62, 170, "Submitted, replaced here", 8, JUNGLE, w=600, a="middle") + "".join(dk(14 + i * 104, 60, 96, 96, i) for i in (1, 2)) + rest(190))),
  ("rp_end", "Joins At The End", "Fresh deck slides in at the far right; others shift left.", "flowing",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 96, i + 1) for i in range(2)) + dk(222, 60, 96, 96, 3) + R(222, 57, 18, 102, JUNGLE + "33", r=4) + tx(226, 172, "New at end", 8, JUNGLE, w=600, a="end") + rest(190))))
# 16 accent
P("Colour", "Accent Colour: A Top Stripe Per Category Or A Soft Tinted Card?",
  ("ac_stripe", "Thin Top Stripe", "White cards, a thin coloured stripe on top.", "crisp", frame(sec(52, "Up Next") + carousel(60) + rest(190))),
  ("ac_tint", "Soft Tinted Card", "Whole card washed in a light tint of its colour.", "warm",
   frame(sec(52, "Up Next") + "".join(R(14 + i * 104, 60, 96, 96, ACC[i] + "1A", ACC[i] + "55", 6) + tx(22 + i * 104, 78, f"{CATS[i]} Deck", 9.5, INK, True) + tx(22 + i * 104, 94, "20 cards", 8, MUTE) for i in range(3)) + rest(190))))
# 17 icons
P("Colour", "Category Icons: A Line Icon Per Category Or No Icons?",
  ("ic_on", "Line Icon Per Category", "A small outline icon beside each deck name.", "visual",
   frame(sec(52, "Up Next") + "".join(dk(14 + i * 104, 60, 96, 96, i, icon=True) for i in range(3)) + rest(190))),
  ("ic_off", "No Icons", "Colour and words only.", "clean", frame(sec(52, "Up Next") + carousel(60) + rest(190))))
# 18 empty
P("Empty State", "When No Decks Are Ready: A Calm Message Or Hide The Section?",
  ("em_msg", "Calm Message", "'All caught up. New decks are on the way.'", "reassuring",
   frame(sec(52, "Up Next") + card(14, 60, 212, 60) + f'<path d="M110 80 l6 6 l10 -12" fill="none" stroke="{JUNGLE}" stroke-width="2"/>' + tx(120, 102, "All caught up. New decks on the way.", 8.5, MUTE, a="middle") + rest(140))),
  ("em_hide", "Hide The Section", "Up Next disappears until a deck is ready.", "minimal", frame(rest(52, 6))))
# 19 ordering
P("Ordering", "Deck Order: Newest First Or Most Important First?",
  ("or_new", "Newest First", "Most recently built deck on the left.", "fresh",
   frame(sec(52, "Up Next") + "".join(row(14, 60 + i * 28, i, ["Today", "Today", "Yesterday", "Oct 12"][i]) for i in range(4)) + rest(190))),
  ("or_pri", "Most Important First", "The deck the project needs most goes first, with a small Priority tag.", "focused",
   frame(sec(52, "Up Next") + "".join(row(14, 60 + i * 28, i, "") + (pill(218, 76, "Priority", TERRA, True, a="end") if i == 0 else tx(218, 76 + i * 28, "20 cards", 8, MUTE, a="end")) for i in range(4)) + rest(190))))
# 20 how many
P("Ordering", "How Many Ready Decks Per Dashboard: Always 3 Or Up To 5?",
  ("nn_3", "Always 3", "Three ready decks, a small, steady set.", "calm",
   frame(sec(52, "Up Next") + tx(226, 52, "3 ready", 8.5, MUTE, a="end") + "".join(row(14, 60 + i * 28, i) for i in range(3)) + rest(160))),
  ("nn_5", "Up To 5", "As many as five, depending on what the project needs.", "plentiful",
   frame(sec(52, "Up Next") + tx(226, 52, "5 ready", 8.5, MUTE, a="end") + "".join(row(14, 60 + i * 28, i) for i in range(5)) + rest(208, 2))))
N = len(pairs); assert N == 20, N
for p in pairs:
    for o in (p["optionA"], p["optionB"]):
        small = [float(v) for v in re.findall(r'font-size="([\d.]+)"', o["visual"]["svg"]) if float(v) < MIN]
        assert not small, (o["id"], small)
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, NAME, NAME, pairs,
        {"brands": ["Up Next Deck: how the Up Next section at the top of every agent dashboard looks and behaves (3-5 ready 20-card decks per dashboard, categories from the agent's project, submitted deck replaced by a fresh one)",
                    "White page (beige #FAF6EE accents), white cards, Khand/Hind, terracotta/lagoon/jungle/saffron accents; text at least 8 units, vector mockups"],
         "submit_agent": "branding", "submit_to": "Branding Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True},
        seed=1417, n=N, first=1)
print("\n".join(f'{i+1}. {p["ask"]}' for i, p in enumerate(json.load(open(f"decks/{DID}.json"))["pairs"])))
