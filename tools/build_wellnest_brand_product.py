#!/usr/bin/env python3
"""Build Style Swipe deck wellnest-brand-and-product: 25 pairs, brand identity + product/service ideas only (no site plan).
Placeholder sample content to show how the deck works. Pattern: build_wellnest_1.py via team_kit.py."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "wellnest-brand-and-product"; pairs, O, add = deck("wnb_", "WellNest")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
HW = ("hdr", "WellNest", "Chiang Mai", JUNGLE, "logo", "W")
C = {"jungle": JUNGLE, "lagoon": LAGOON, "saffron": SAFFRON, "terra": TERRA, "ink": INK}

G = "Color Palette"
def cp(k):
    a, b = k.split("-")
    return [("hdr", "WellNest", "Chiang Mai", C[a], "band", "W"), ("swatch", [C[a], C[b], "#FFFFFF"], [a.title(), b.title(), "White"]), ("btn", "Book A Visit", "fill", C[b])]
for x, y in [(("jungle-saffron", "Jungle And Saffron"), ("lagoon-terra", "Lagoon And Terracotta")), (("jungle-terra", "Jungle And Terracotta"), ("ink-saffron", "Ink And Saffron")), (("lagoon-saffron", "Lagoon And Saffron"), ("ink-jungle", "Ink And Jungle"))]:
    pr(G, f"{x[1]} Or {y[1]}?", cp, ("cp_" + x[0].replace("-", "_"), x[1], "Example palette.", "calm", x[0]), ("cp_" + y[0].replace("-", "_"), y[1], "Example palette.", "visual", y[0]))

G = "Font Pairing"
def fp(k):
    f1, f2 = k.split("-")
    return [HW, ("word", "Rest And Reset", 28, INK, "", True, f1), ("p", "A quiet place in Chiang Mai.", 40, MUTE, True), ("word", "Sample Body Text", 14, MUTE, "", True, f2)]
pr(G, "Khand Headings Or Hind Headings?", fp, ("fp_khand_hind", "Khand Over Hind", "Tall, bold heads.", "focused", "khand-hind"), ("fp_hind_khand", "Hind Over Khand", "Soft, round heads.", "calm", "hind-khand"))
pr(G, "All Khand Or All Hind?", fp, ("fp_khand_all", "All Khand", "One strong voice.", "visual", "khand-khand"), ("fp_hind_all", "All Hind", "One gentle voice.", "calm", "hind-hind"))
pr(G, "Khand Heads With Hind Or Hind Heads With Khand Labels?", fp, ("fp_khand_bold", "Big Khand Title Only", "Poster style.", "visual", "khand-hind"), ("fp_hind_soft", "Soft Hind Title Only", "Letter style.", "calm", "hind-hind"))

G = "Logo Mark"
def lg(k):
    if k == "leaf": m = photo(80, 60, 80, 80, JUNGLE, "leaf", 40)
    elif k == "sun": m = photo(80, 60, 80, 80, SAFFRON, "sun", 40)
    elif k == "ring": m = f'<circle cx="120" cy="100" r="40" fill="none" stroke="{JUNGLE}" stroke-width="6"/>'
    elif k == "dot": m = dot(120, 100, 40, TERRA)
    elif k == "square": m = rect(80, 60, 80, 80, LAGOON, "none", 10) + t(120, 116, "W", 44, "#FFFFFF", "khand", anchor="middle")
    else: m = t(120, 120, "WN", 56, JUNGLE, "khand", anchor="middle")
    return [("raw", m + t(120, 190, "WellNest", 24, INK, "khand", anchor="middle"), 210)]
pr(G, "Leaf Or Sun?", lg, ("lgm_leaf", "Leaf Mark", "Nature first.", "calm", "leaf"), ("lgm_sun", "Sun Mark", "Warm mornings.", "visual", "sun"))
pr(G, "Open Ring Or Solid Dot?", lg, ("lgm_ring", "Open Green Ring", "Light and airy.", "calm", "ring"), ("lgm_dot", "Solid Terracotta Dot", "Bold and simple.", "visual", "dot"))
pr(G, "W Square Or WN Letters?", lg, ("lgm_square", "W In A Blue Square", "App-icon ready.", "focused", "square"), ("lgm_letters", "WN Monogram", "Letters only.", "focused", "wn"))
pr(G, "Leaf Or WN Letters?", lg, ("lgm_leaf2", "Leaf Above Name", "Organic.", "calm", "leaf"), ("lgm_wn2", "Letters Above Name", "Modern.", "focused", "wn"))

G = "Tone Of Voice"
def tv(k):
    s = {"warm": ("Come As You Are", "We'll take care of the rest."), "calm": ("Slow Down Here", "Breathe. Rest. Return."),
         "plain": ("Massage, Yoga, Steam", "Open daily, 9 to 6."), "playful": ("Nap Like You Mean It", "Your couch can't do this.")}[k]
    return [HW, ("h", s[0], 22, INK, True), ("p", s[1], 40, MUTE, True), ("btn", "Book A Visit", "fill", JUNGLE)]
pr(G, "Warm Or Calm?", tv, ("tv_warm", "Warm And Welcoming", "Come as you are.", "calm", "warm"), ("tv_calm", "Quiet And Calm", "Slow down here.", "calm", "calm"))
pr(G, "Plain Or Playful?", tv, ("tv_plain", "Plain And Clear", "Just the facts.", "quick", "plain"), ("tv_playful", "Light And Playful", "A little humor.", "visual", "playful"))
pr(G, "Calm Or Playful?", tv, ("tv_calm2", "Calm Lines", "Breathe. Rest.", "calm", "calm"), ("tv_playful2", "Playful Lines", "Nap like you mean it.", "visual", "playful"))

G = "Signage"
def sg(k):
    bg, fg = {"green": (JUNGLE, "#FFFFFF"), "white": ("#FFFFFF", JUNGLE), "wood": (TERRA, "#FFFFFF"), "ink": (INK, SAFFRON)}[k]
    return [("raw", rect(30, 60, 180, 90, bg, LINE, 6) + t(120, 115, "WellNest", 32, fg, "khand", anchor="middle") + rect(60, 150, 8, 60, MUTE) + rect(172, 150, 8, 60, MUTE), 220)]
pr(G, "Green Sign Or White Sign?", sg, ("sg_green", "Solid Green Sign", "Seen from the road.", "visual", "green"), ("sg_white", "White Sign, Green Name", "Clean and quiet.", "calm", "white"))
pr(G, "Terracotta Or Ink And Saffron?", sg, ("sg_terra", "Terracotta Sign", "Earthy warmth.", "visual", "wood"), ("sg_ink", "Ink With Saffron Name", "Strong contrast.", "focused", "ink"))
pr(G, "Green Or Terracotta Sign?", sg, ("sg_green2", "Green Road Sign", "Matches the leaf.", "visual", "green"), ("sg_terra2", "Terracotta Road Sign", "Matches the soil.", "visual", "wood"))

G = "Packaging"
def pk(k):
    c = {"jar": JUNGLE, "bag": TERRA, "box": LAGOON, "tin": SAFFRON}[k]
    if k in ("jar", "tin"): m = rect(80, 50, 80, 20, c, "none", 4) + rect(70, 70, 100, 120, "#FFFFFF", c, 10)
    else: m = rect(60, 60, 120, 130, c + "22", c, 6)
    return [("raw", m + t(120, 136, "WellNest", 18, c, "khand", anchor="middle") + t(120, 152, "Herbal Balm", 8, MUTE, "hind", 600, "middle"), 210)]
pr(G, "Glass Jar Or Paper Bag?", pk, ("pk_jar", "Glass Jar, Green Label", "Shelf ready.", "visual", "jar"), ("pk_bag", "Kraft Paper Bag", "Low waste.", "calm", "bag"))
pr(G, "Gift Box Or Small Tin?", pk, ("pk_box", "Blue Gift Box", "Made to give.", "visual", "box"), ("pk_tin", "Saffron Travel Tin", "Fits a pocket.", "quick", "tin"))
pr(G, "Glass Jar Or Gift Box?", pk, ("pk_jar2", "Green-Label Jar", "Everyday.", "quick", "jar"), ("pk_box2", "Blue Gift Box", "Special.", "visual", "box"))

G = "Things To Sell"
def ts(k):
    n = {"balm": ("Herbal Balm", "Example: 250 THB"), "tea": ("Herbal Tea Blend", "Example: 180 THB"), "oil": ("Massage Oil", "Example: 390 THB"),
         "candle": ("Lemongrass Candle", "Example: 320 THB"), "robe": ("Cotton Robe", "Example: 990 THB"), "mat": ("Yoga Mat", "Example: 1,200 THB")}[k]
    return [HW, ("photo", 100, JUNGLE, "leaf"), ("cards", [(n[0], n[1], "tag:Shop")], JUNGLE)]
pr(G, "Herbal Balm Or Tea Blend?", ts, ("ts_balm", "Herbal Balm", "Small, easy add-on.", "quick", "balm"), ("ts_tea", "Herbal Tea Blend", "Take the calm home.", "calm", "tea"))
pr(G, "Massage Oil Or Candle?", ts, ("ts_oil", "Massage Oil", "Matches the treatment.", "focused", "oil"), ("ts_candle", "Lemongrass Candle", "Scent of the place.", "calm", "candle"))
pr(G, "Robe Or Yoga Mat?", ts, ("ts_robe", "Cotton Robe", "Higher-end keepsake.", "visual", "robe"), ("ts_mat", "Branded Yoga Mat", "For regulars.", "action", "mat"))

G = "Services"
def sv(k):
    n = {"tour": ("Herb Garden Tour", "1 hour, small group"), "workshop": ("Balm-Making Workshop", "2 hours, take one home"),
         "stay": ("Two-Night Stay", "Massage and yoga included"), "day": ("Day Pass", "Garden, steam, lunch"),
         "class": ("Thai Massage Class", "Half day, beginners"), "retreat": ("Weekend Retreat", "Three days, all meals")}[k]
    return [HW, ("photo", 90, LAGOON, "sun"), ("cards", [(n[0], n[1], "tag:Example")], LAGOON), ("btn", "Ask About Dates", "line", INK)]
pr(G, "Garden Tour Or Workshop?", sv, ("svc_tour", "Herb Garden Tour", "Easy first visit.", "calm", "tour"), ("svc_workshop", "Balm-Making Workshop", "Hands-on.", "action", "workshop"))
pr(G, "Overnight Stay Or Day Pass?", sv, ("svc_stay", "Two-Night Stay", "Deep rest.", "calm", "stay"), ("svc_day", "Day Pass", "Low commitment.", "quick", "day"))
pr(G, "Massage Class Or Weekend Retreat?", sv, ("svc_class", "Thai Massage Class", "Learn a skill.", "focused", "class"), ("svc_retreat", "Weekend Retreat", "Full reset.", "visual", "retreat"))

publish(DID, "WellNest Brand & Product Deck", "WellNest", pairs,
        {"brands": ["WellNest (Chiang Mai wellness business), placeholder sample content to show how the deck works", "White base, Khand/Hind, Title Case, drawn SVGs, no emoji"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"feed": "/workspace/ops/team-feed.md", "prior": "decks/wellnest-1.json"}}, seed=41)
