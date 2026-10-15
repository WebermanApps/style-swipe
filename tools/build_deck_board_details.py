#!/usr/bin/env python3
"""Build Style Swipe deck deck-board-2: Deck Board Details (Oct 14 2026), 20 pairs. Follows deck-board (submission 77ca9a56, 19/20).
Carried first: deck-board-18 reworded (Deck Progress: A Thin Filling Bar Or Words Like "7 Of 20"?). Builds on the picks now live on the Deck Building page: featured gold card first,
Mixed Deck toggle chips at top, coloured category chips all open by newest activity, white-outline rows with title/topic/agent label,
category-colour small ring, partial line + Resume, icon app row, compact, spaced-caps headings, one wide grid on big monitors; plus the new
Decks Finished Today tracker. Max brand. Submit -> agent 'branding'."""
import sys, os, math; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
from carry_over import carried_first
DID = "deck-board-2"; TOPIC = "deck-board"
B = dict(name="Deck Building", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=700)
GOLD, RICE, GOLDT = "#ECC978", "#FBF8F1", "#8A6A0E"
pairs, O, add = deck("db2_", "Branding")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
CATS = [("UPKEEP", TERRA), ("PORTFOLIO", LAGOON), ("WELLNEST", JUNGLE), ("DASHBOARDS", SAFFRON)]
def head(y=10, title="DECK BUILDING"): return T(B, 14, y + 22, title, 18, None, True, ex='letter-spacing="1.5"') + R(150, y + 9, 60, 14, "#FBF3DC", r=7) + T(B, 180, y + 19, "5 WAITING", 6.5, "#7A5C00", w=600, a="middle", ex='letter-spacing="1"'), 32
def ring(cx, cy, f, c, r=7, check=False, num=None):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEBE5" stroke-width="2.6"/>'
    if f > 0:
        L_ = 2 * math.pi * r; s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="{f*L_:.1f} {L_:.1f}" transform="rotate(-90 {cx} {cy})"/>'
    if check: s += f'<path d="M{cx-3} {cy} l2 2 4 -4.5" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
    if num: s += T(B, cx, cy + 2.2, num, 5.5, c, w=600, a="middle")
    return s
def row(y, name, topic, cat, c, f=0.0, o=None):
    o = o or {}; h = o.get("h", 36); s = R(14, y, 212, h, "#FFFFFF", B["line"], 8)
    prog = o.get("prog", "ring")
    if prog == "ring": s += ring(30, y + h / 2, f, c, check=f >= 1, num=o.get("num"))
    x = 46 if prog == "ring" else 24
    s += T(B, x, y + 13, name, 8.5, None, True)
    if o.get("topic", True): s += T(B, x, y + 23, topic, 6, B["mute"])
    lab = R(x, y + h - 10, len(cat) * 3.6 + 8, 7, c + "22", r=3.5) + T(B, x + 4, y + h - 4.7, cat, 4.8, c, w=600, ex='letter-spacing=".5"')
    if o.get("labpos") == "right": lab = R(218 - len(cat) * 3.6 - 8, y + 6, len(cat) * 3.6 + 8, 7, c + "22", r=3.5) + T(B, 218 - len(cat) * 3.6 - 4, y + 11.3, cat, 4.8, c, w=600, ex='letter-spacing=".5"')
    s += lab
    if prog == "bar": s += R(150, y + h / 2 - 1.5, 64, 3, "#EEEBE5", r=1.5) + R(150, y + h / 2 - 1.5, 64 * f, 3, c, r=1.5)
    if prog == "count": s += T(B, 216, y + h / 2 + 2, o.get("cnt", "12 of 20"), 6.5, c, w=600, a="end")
    if prog == "both": s += ring(206, y + h / 2, f, c) + T(B, 190, y + h / 2 + 2, o.get("cnt", "12/20"), 6, B["mute"], a="end")
    if o.get("partial"):
        pt = o["partial"]; s += T(B, x, y + h + 9, pt[0], 6, GOLDT, w=600) + R(176, y + h + 2, 40, 11, pt[1], r=pt[2]) + T(B, 196, y + h + 9.5, "RESUME", 5, "#FFFFFF", w=600, a="middle", ex='letter-spacing=".8"'); return s, h + 18
    return s, h + 5
def chip(y, name, c, o=None):
    o = o or {}; st = o.get("chip", "tint"); w = len(name) * 5.4 + 16
    s = R(14, y, w, 14, c + "24" if st == "tint" else c, r=7) + T(B, 22, y + 10, name, 7.5, c if st == "tint" else "#FFFFFF", True, ex='letter-spacing="1"')
    if o.get("bub", True): s += R(22 + w, y + 1, 40, 12, "#FBF3DC", r=6) + T(B, 42 + w, y + 9.5, "2 WAITING", 5, "#7A5C00", w=600, a="middle")
    if o.get("new"): s += R(66 + w, y + 1, 24, 12, SAFFRON, r=6) + T(B, 78 + w, y + 9.5, "NEW", 5, "#FFFFFF", w=600, a="middle")
    return s, 20
def feat(y, o=None):
    o = o or {}; h = o.get("h", 64); s = R(14, y, 212, h, RICE, GOLD, 4, 2.5) + T(B, 24, y + 13, "FEATURED · WELLNEST", 5.5, GOLDT, w=600, ex='letter-spacing="1"') + T(B, 24, y + 28, o.get("nm", "WellNest Dashboard Deck"), 12, None, True) + T(B, 24, y + 38, "24 pairs, submit goes to WellNest", 6, B["mute"])
    if o.get("btn", True): s += R(24, y + 44, 56, 14, "#FFFFFF", B["ink"], 0, 1.2) + T(B, 52, y + 53.5, "OPEN THE DECK", 5, B["ink"], w=600, a="middle", ex='letter-spacing=".8"')
    else: s += T(B, 216, y + 28, "›", 16, B["ink"], a="end")
    if o.get("ring"): s += ring(206, y + 22, .4, JUNGLE, r=9)
    return s, h + 6
def mixchips(y, o=None):
    o = o or {}; s = R(14, y, 212, 72, "#FFFFFF", LAGOON, 0, 1.5) + T(B, 24, y + 14, "MIXED DECK", 9, None, True, ex='letter-spacing="1.2"')
    x, yy = 24, y + 22; on = o.get("on", "all")
    for i, (n, c) in enumerate(CATS + [("THAI", TERRA), ("BLOG", LAGOON)]):
        w = len(n) * 4.3 + 14
        if x + w > 216: x, yy = 24, yy + 16
        act = on == "all" or (on == "some" and i < 2)
        st = o.get("off", "outline")
        if act: s += R(x, yy, w, 12, c, r=6) + T(B, x + w / 2, yy + 8.5, n, 5.5, "#FFFFFF", w=600, a="middle")
        elif st == "outline": s += R(x, yy, w, 12, "#FFFFFF", c, 6) + T(B, x + w / 2, yy + 8.5, n, 5.5, c, w=600, a="middle")
        else: s += R(x, yy, w, 12, c + "22", r=6) + T(B, x + w / 2, yy + 8.5, n, 5.5, c, w=600, a="middle")
        x += w + 4
    if o.get("size", True): s += R(24, y + 56, 36, 11, "#FFFFFF", B["line"], 5.5) + T(B, 42, y + 63.5, "10", 5.5, B["mute"], a="middle") + R(64, y + 56, 36, 11, LAGOON, r=5.5) + T(B, 82, y + 63.5, "20", 5.5, "#FFFFFF", a="middle", w=600)
    s += R(160, y + 54, 56, 14, LAGOON) + T(B, 188, y + 63.5, "START", 6, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1"')
    return s, 78
def tracker(y, o=None):
    o = o or {}; s = R(14, y, 212, 30, "#FFFFFF", B["line"], 8) + T(B, 26, y + 21, "4", 16, JUNGLE, True) + T(B, 40, y + 13, "DECKS FINISHED TODAY", 6, None, True, ex='letter-spacing="1"') + T(B, 40, y + 22, "ICT, each deck once", 5.5, B["mute"])
    if o.get("week", True):
        for i, v in enumerate([0, 1, 3, 2, 0, 5, 4]): s += R(160 + i * 9, y + 20 - max(1, v * 2.6), 6, max(1, v * 2.6), JUNGLE if i == 6 else JUNGLE + "55", r=1.5)
    return s, 36
def apps(y, o=None):
    o = o or {}; n = o.get("n", 3); names = ["Style Swipe", "Branding", "Apps Home", "Dashboards", "Requests"][:n]; w = 212 / n; s = ""
    for i, nm in enumerate(names):
        cx = 14 + w * i + w / 2; c = B["acc"][i % 4]; s += R(cx - 10, y, 20, 20, c + "24", r=6) + tile_icon(cx - 7, y + 3, i, c, 14)
        if o.get("labels", True): s += T(B, cx, y + 28, nm, 5.5, None, True, a="middle")
    return s, 34 if o.get("labels", True) else 26
def page(parts, bg="#FFFFFF"):
    s, y = "", 6
    for fn, o in parts:
        g, h = fn(y, o) if fn not in (head,) else fn(y); s += g; y += h
    return screen(s, bg)
def H(y, o=None): return head(y)
def CAT(y, o=None):
    o = o or {}; s, h = chip(y, *CATS[o.get("ci", 0)], o); yy = y + h
    for i, (nm, tp, f) in enumerate(o.get("rows", [("UpKeep Board Details", "Report card, tiles, approvals", .6), ("UpKeep Board Deck", "Layout, video, feed", 1.0)])):
        g, hh = row(yy, nm, tp, CATS[o.get("ci", 0)][0], CATS[o.get("ci", 0)][1], f, {**o, **({"partial": o["partial"]} if (o.get("partial") and i == 0) else {"partial": None})}); s += g; yy += hh
    return s, yy - y + 2
std = lambda **k: [(H, None), (tracker, k), (feat, k), (mixchips, k), (CAT, {**k, "ci": 0}), (CAT, {**k, "ci": 1, "rows": [("Folio Dashboard Details", "Thumbnail, report, chart", .2)]})]
G = "Featured Card"
P(G, "Featured Card: Open Button Or Whole Card With Arrow?",
  ("ft_btn", "Open The Deck Button", "Outlined button on the gold card.", "action", page([(H, None), (feat, {}), (mixchips, {}), (CAT, {})])),
  ("ft_arrow", "Whole Card, Arrow", "No button, the card opens the deck.", "quick", page([(H, None), (feat, {"btn": False, "h": 48}), (mixchips, {}), (CAT, {})])))
P(G, "Featured Card: Show Its Progress Ring?",
  ("ft_ring", "With A Progress Ring", "Small ring in the corner.", "visual", page([(H, None), (feat, {"ring": True}), (mixchips, {}), (CAT, {})])),
  ("ft_noring", "No Ring", "Clean gold card.", "calm", page([(H, None), (feat, {}), (mixchips, {}), (CAT, {})])))
G = "Mixed Deck Chips"
P(G, "Mixed Deck: All Chips On Or None On At Start?",
  ("mx_allon", "All On", "Every category selected; tap to drop one.", "quick", page([(H, None), (mixchips, {"on": "all"}), (CAT, {})])),
  ("mx_someon", "Pick To Add", "Nothing selected; tap to add.", "focused", page([(H, None), (mixchips, {"on": "some"}), (CAT, {})])))
P(G, "Mixed Deck: Off Chips Outlined Or Soft Tint?",
  ("mx_outline", "Outlined When Off", "White chip with a coloured edge.", "focused", page([(H, None), (mixchips, {"on": "some"}), (CAT, {})])),
  ("mx_tint", "Soft Tint When Off", "Pale colour fill.", "calm", page([(H, None), (mixchips, {"on": "some", "off": "tint"}), (CAT, {})])))
P(G, "Mixed Deck: 10/20 Size Chips Or Always 20?",
  ("mx_size", "10 Or 20 Pairs", "Pick a size, max 20.", "action", page([(H, None), (mixchips, {}), (CAT, {})])),
  ("mx_nosize", "Always 20", "One less choice.", "quick", page([(H, None), (mixchips, {"size": False}), (CAT, {})])))
G = "Category Chips"
P(G, "Category Chip: With Waiting Count Or Chip Only?",
  ("ch_bub", "Chip Plus Waiting Count", "Saffron count beside the chip.", "focused", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1}), (CAT, {"ci": 2})])),
  ("ch_only", "Chip Only", "Count shows in the rows.", "calm", page([(H, None), (CAT, {"ci": 0, "bub": False}), (CAT, {"ci": 1, "bub": False}), (CAT, {"ci": 2, "bub": False})])))
P(G, "Newest Activity: Saffron New Tag Or Order Only?",
  ("ch_new", "New Tag On The Top Group", "Shows why it moved up.", "visual", page([(H, None), (CAT, {"ci": 0, "new": True}), (CAT, {"ci": 1}), (CAT, {"ci": 2})])),
  ("ch_order", "Order Only", "Top is newest, no tag.", "calm", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1}), (CAT, {"ci": 2})])))
P(G, "Category Chips: Soft Tint Or Solid Colour?",
  ("ch_tint", "Soft Tint", "As picked: pale fill, coloured words.", "calm", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1}), (CAT, {"ci": 2})])),
  ("ch_solid", "Solid Colour", "White words on the category colour.", "visual", page([(H, None), (CAT, {"ci": 0, "chip": "solid"}), (CAT, {"ci": 1, "chip": "solid"}), (CAT, {"ci": 2, "chip": "solid"})])))
G = "Progress Ring"
P(G, "Ring: Number Inside Or Ring Only?",
  ("rg_num", "Count Inside The Ring", "Tiny answered count in the ring.", "focused", page([(H, None), (CAT, {"ci": 0, "num": "12"}), (CAT, {"ci": 1, "num": "4"})])),
  ("rg_plain", "Ring Only", "Clean ring, tick when done.", "calm", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1})])))
P(G, "Progress: Ring Only Or Ring Plus Count At The End?",
  ("rg_one", "Ring On The Left", "One mark per row.", "calm", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 2})])),
  ("rg_both", "Ring Plus Count, Right", "Count and ring at the row end.", "focused", page([(H, None), (CAT, {"ci": 0, "prog": "both"}), (CAT, {"ci": 2, "prog": "both"})])))
G = "Partial And Resume"
P(G, "Partial Line: Black Resume Or Lagoon Resume?",
  ("pt_black", "Black Resume", "Square black button.", "focused", page([(H, None), (CAT, {"ci": 0, "partial": ("Sent partial, 8 left to answer", "#0A0A0A", 0)}), (CAT, {"ci": 1})])),
  ("pt_lagoon", "Lagoon Resume", "Rounded lagoon button.", "calm", page([(H, None), (CAT, {"ci": 0, "partial": ("Sent partial, 8 left to answer", LAGOON, 5.5)}), (CAT, {"ci": 1})])))
P(G, "Partial Line: Left To Answer Or Answered So Far?",
  ("pt_left", "8 Left To Answer", "Says what remains.", "action", page([(H, None), (CAT, {"ci": 0, "partial": ("Sent partial, 8 left to answer", "#0A0A0A", 0)}), (CAT, {"ci": 1})])),
  ("pt_done", "12 Of 20 Sent", "Says what is done.", "calm", page([(H, None), (CAT, {"ci": 0, "partial": ("Sent 12 of 20 so far", "#0A0A0A", 0)}), (CAT, {"ci": 1})])))
G = "Rows And Labels"
P(G, "Deck Rows: Topic Line Or Name Only?",
  ("rw_topic", "Name, Topic Line, Label", "As picked, two lines plus label.", "focused", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1}), (CAT, {"ci": 2})])),
  ("rw_name", "Name And Label Only", "Tighter rows, topic on tap.", "quick", page([(H, None), (CAT, {"ci": 0, "topic": False, "h": 28}), (CAT, {"ci": 1, "topic": False, "h": 28}), (CAT, {"ci": 2, "topic": False, "h": 28}), (CAT, {"ci": 3, "topic": False, "h": 28})])))
P(G, "Agent Label: Under The Name Or Top Right?",
  ("lb_under", "Under The Name", "Label at the bottom left.", "calm", page([(H, None), (CAT, {"ci": 0}), (CAT, {"ci": 1})])),
  ("lb_right", "Top Right", "Label in the corner.", "focused", page([(H, None), (CAT, {"ci": 0, "labpos": "right"}), (CAT, {"ci": 1, "labpos": "right"})])))
G = "My Apps Row"
P(G, "My Apps: Three Apps Or Five?",
  ("ap_three", "Three Apps", "Style Swipe, Branding, Apps Home.", "calm", page([(H, None), (feat, {}), (apps, {"n": 3}), (mixchips, {})])),
  ("ap_five", "Five Apps", "Adds Dashboards and Requests.", "quick", page([(H, None), (feat, {}), (apps, {"n": 5}), (mixchips, {})])))
P(G, "My Apps: Labels Under Icons Or Icons Only?",
  ("ap_lab", "Labels Under Icons", "Names under each icon.", "focused", page([(H, None), (feat, {}), (apps, {"n": 4}), (mixchips, {})])),
  ("ap_nolab", "Icons Only", "Smaller row, names on hover.", "quick", page([(H, None), (feat, {}), (apps, {"n": 4, "labels": False}), (mixchips, {})])))
G = "Finished Today Tracker"
P(G, "Tracker: Count With 7-Day Bars Or Count Only?",
  ("tk_week", "Count Plus 7-Day Bars", "Today's number and a mini week.", "visual", page([(H, None), (tracker, {}), (feat, {}), (mixchips, {})])),
  ("tk_only", "Count Only", "Just today's number.", "calm", page([(H, None), (tracker, {"week": False}), (feat, {}), (mixchips, {})])))
def wide(n):
    s = T(B, 120, 20, "Big Monitor", 9, B["mute"], True, a="middle") + R(8, 34, 224, 140, "#FFFFFF", "#BDB6AA", 6, 1.2) + R(110, 174, 20, 14, "#D6D0C6") + R(90, 188, 60, 4, "#BDB6AA", r=2)
    cw = (208 - (n - 1) * 4) / n
    for ci in range(2):
        y0 = 42 + ci * 64; s += R(16, y0, 40, 8, CATS[ci][1] + "24", r=4) + T(B, 20, y0 + 6, CATS[ci][0], 4.5, CATS[ci][1], True)
        for j in range(n if ci == 0 else n - 1):
            x = 16 + j * (cw + 4); s += R(x, y0 + 12, cw, 22, "#FFFFFF", B["line"], 3) + ring(x + 8, y0 + 23, (j + 1) / (n + 1), CATS[ci][1], r=4) + R(x + 15, y0 + 18, cw - 22, 2.5, B["ink"] + "55", r=1) + R(x + 15, y0 + 24, cw * .4, 2, B["mute"] + "55", r=1)
    return screen(s + T(B, 120, 210, f"{n} decks across", 7.5, B["mute"], a="middle"), "#FFFFFF")
P("Big Monitor Grid", "Wide Grid: Three Across Or Four Across?",
  ("bm_three", "Three Across", "Bigger rows.", "calm", wide(3)),
  ("bm_four", "Four Across", "More decks at once.", "quick", wide(4)))
def tcase(caps):
    s, y = "", 6; t = "DECK BUILDING" if caps else "Deck Building"
    s += T(B, 14, y + 22, t, 18, None, True, ex='letter-spacing="1.5"' if caps else "")
    y += 34
    for ci in range(3):
        nm, c = CATS[ci]; nm2 = nm if caps else nm.title().replace("Upkeep", "UpKeep").replace("Wellnest", "WellNest")
        w = len(nm2) * 5.4 + 16; s += R(14, y, w, 14, c + "24", r=7) + T(B, 22, y + 10, nm2, 7.5, c, True, ex='letter-spacing="1"' if caps else ""); y += 20
        g, h = row(y, "Example Deck Name", "Topic line", nm, c, .5); s += g; y += h + 4
    return screen(s, "#FFFFFF")
P("Typography", "Spaced Caps: Headings Only Or Category Chips Too?",
  ("ty_chipcaps", "Headings And Chips In Caps", "As now.", "focused", tcase(True)),
  ("ty_chiptitle", "Chips In Title Case", "Caps only on the page title.", "calm", tcase(False)))
carried = carried_first(TOPIC, [], clear=False)
for p in carried:
    p.pop("id", None)
    for s_ in "AB": p["option" + s_]["id"] = "db2_rt_" + p["option" + s_]["id"].split("_", 1)[1]
    p["purpose"] = "retest"; p["retest"] = True; p["notes"] = True; p["share"] = True
pairs[:0] = carried
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Deck Board Details", "Branding", pairs,
        {"brands": ["Deck Board Details: carried progress pair first, then deeper on the live Deck Building picks: featured card, Mixed Deck chips, category chips, ring, partial + Resume, rows and labels, My Apps row, Finished Today tracker, big monitor grid",
                    "Max brand on the light cream deck page with white cards"],
         "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "section_counts": cnt, "deck_size": N, "carried": len(carried),
         "follows": {"deck": "deck-board", "submission": "77ca9a56-ecf9-4021-9bda-6dbf441aca2a", "answered": 19, "total": 20},
         "sources": {"results": "/workspace/style-swipe/results/deck-board.txt", "page": "https://webermanapps.github.io/branding-djqmb410/decks/"}},
        seed=1021, n=N, first=len(carried))
carried_first(TOPIC, [], clear=True)
