#!/usr/bin/env python3
"""Build Style Swipe deck security-icon (Oct 14 2026): Security Icon Deck, 10 icon this-or-that pairs for the Security app.
Icons: /workspace/security/icons/ninja0-original.png, ninja1..5.png, plus two drawn refinements of the original
(/workspace/security/icons/refine/r1.svg, r2.svg -> ninja-refine-1/2.png). Copied to img/security/.
Pattern copied from build_info_gather.py (team_kit.publish). Submit -> agent 'security'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import screen, t, rect, INK, W, H
DID = "security-icon"
pairs, O, add = deck("si_", "Security")
IC = {"o0": ("ninja0-original", "Original Ninja", "Navy hood, red headband, cream circle. Closest so far."),
      "r1": ("ninja-refine-1", "Refined Original", "Drawn refinement: flatter shapes, terracotta band, soft lagoon circle."),
      "r2": ("ninja-refine-2", "Ninja In Shield Outline", "Drawn refinement: original face inside a lagoon shield outline."),
      "n1": ("ninja1", "Gold Shield Band", "Ninja with a gold shield on the headband."),
      "n2": ("ninja2", "Keyhole Knot", "Headband knot shaped like a keyhole."),
      "n3": ("ninja3", "Katana With Red Sun", "Katana across a red rising sun."),
      "n4": ("ninja4", "Shield-Shaped Ninja", "The whole ninja head forms a shield."),
      "n5": ("ninja5", "Wave Ring", "Ninja inside a Japanese wave ring.")}
def card(k, label):
    f = IC[k][0]
    s = rect(0, 0, W, H, "#FFFFFF") + rect(20, 30, W - 40, W - 40, "#FFFFFF", "#E5DCCB", 14)
    s += f'<image href="img/security/{f}.png" x="34" y="44" width="{W-68}" height="{W-68}" preserveAspectRatio="xMidYMid meet"/>'
    s += t(W / 2, W + 14, label, 15, INK, "khand", 600, "middle")
    s += rect(W / 2 - 22, W + 30, 44, 44, "#FFFFFF", "#E5DCCB", 8) + f'<image href="img/security/{f}.png" x="{W/2-18}" y="{W+34}" width="36" height="36"/>'
    s += t(W / 2, H - 8, "App-icon size", 7, "#525252", "hind", 400, "middle")
    return screen(s, "#FFFFFF")
def opt(k, n, feel): return O(f"{k}_{n}", IC[k][1], IC[k][2], feel, card(k, IC[k][1]))
PL = [("Original Vs Gold Shield Band", "o0", "n1"), ("Original Vs Keyhole Knot", "o0", "n2"), ("Refined Original Vs Katana With Red Sun", "r1", "n3"),
      ("Shield Outline Vs Shield-Shaped Ninja", "r2", "n4"), ("Original Vs Wave Ring", "o0", "n5"), ("Original Vs Refined Original", "o0", "r1"),
      ("Original Vs Ninja In Shield Outline", "o0", "r2"), ("Refined Original Vs Shield Outline", "r1", "r2"), ("Refined Original Vs Keyhole Knot", "r1", "n2"),
      ("Shield Outline Vs Wave Ring", "r2", "n5")]
for i, (ask, a, b) in enumerate(PL):
    g = "Original Vs Refinements" if b in ("r1", "r2") else "Ninja Variations"
    add(g, g, opt(a, i, "familiar"), opt(b, i, "bold"), ask + "?")
N = len(pairs); assert 8 <= N <= 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Security Icon Deck", "Security", pairs,
        {"brands": ["Security app icon: Japanese ninja direction. Original (closest so far) and two drawn refinements against five variations (gold shield band, keyhole knot, katana with red sun, shield-shaped ninja, wave ring)",
                    "Light cream page, white cards, Khand/Hind, subtle terracotta/lagoon/jungle accents"],
         "submit_agent": "security", "submit_to": "Security Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "sources": {"icons": "/workspace/security/icons/ninja0-original.png, ninja1..5.png", "refinements": "/workspace/security/icons/refine/r1.svg, r2.svg"}},
        seed=1415, n=N)
