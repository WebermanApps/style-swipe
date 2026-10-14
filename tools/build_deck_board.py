#!/usr/bin/env python3
"""Build Style Swipe deck deck-board (Oct 14 2026): Deck Board Deck, 20 pairs on how the Deck Building page
(https://webermanapps.github.io/branding-djqmb410/decks/) and the deck section of the branding dashboard look (source /workspace/branding-dashboard).
Max brand: white base, Khand/Hind, small terracotta/lagoon/jungle/saffron accents. Example names only. Submit -> agent 'branding'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
DID = "deck-board"
B = dict(name="Deck Building", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("db_", "Branding")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
CATS = [("UpKeep", ["UpKeep Board Deck", "UpKeep 7"], [(0, 20), (25, 25)]), ("WellNest", ["WellNest Dashboard Deck", "Brand Round Two"], [(0, 24), (30, 61)]), ("Portfolio", ["Folio Dashboard Deck", "Portfolio 1"], [(0, 20), (25, 25)])]
def s_cats(B, y, o):
    st = o.get("cats", "head"); s = ""; yy = y; cats = CATS[:o.get("ncat", 3)]
    for ci, (nm, ds, stt) in enumerate(cats):
        c = B["acc"][ci % 4]
        if st == "chip": s += R(14, yy, len(nm) * 5 + 18, 14, c + "1A", r=7) + T(B, 23, yy + 10, nm.upper(), 6.5, c, w=600, ex='letter-spacing="1"'); yy += 18
        elif st == "bar": s += R(14, yy, 212, 16, c, r=4) + T(B, 22, yy + 11.5, nm, 9, "#FFFFFF", True) + T(B, 218, yy + 11, f"{len(ds)} decks", 6.5, "#FFFFFF", a="end"); yy += 20
        elif st == "fold":
            open_ = ci == 0; s += card(B, 14, yy, 212, 22) + D(24, yy + 11, 3, c) + T(B, 32, yy + 14.5, nm, 9, None, True) + T(B, 196, yy + 14, f"{len(ds)}", 7, B["mute"], a="end") + chev(212, yy + 11, B["mute"], open_); yy += 26
            if not open_: continue
        else: s += T(B, 14, yy + 12, nm, 11, None, True) + L(14, yy + 16, 226, yy + 16, B["line"]); yy += 20
        g, h = s_decks(B, yy, {**o, "dnames": ds, "dstat": stt, "decks": o.get("decks", "list")}); s += g; yy += h + 4
    return s, yy - y
def s_mix(B, y, o):
    st = o.get("mix", "card")
    if st == "chips":
        s = T(B, 14, y + 10, "MIXED DECK", 6.5, B["mute"], w=600, ex='letter-spacing="1.2"')
        for i, (nm, on) in enumerate([("UpKeep", 1), ("WellNest", 1), ("Portfolio", 0), ("Thai", 0), ("Blog", 1)]):
            x = 14 + (i % 3) * 72; yy = y + 16 + (i // 3) * 20; c = B["acc"][i % 4]
            s += R(x, yy, 66, 16, c if on else "#FFFFFF", c if on else B["line"], 8) + T(B, x + 33, yy + 11, nm, 7, "#FFFFFF" if on else B["ink"], True, a="middle")
        return s + R(14, y + 60, 212, 24, B["ink"], r=0) + T(B, 120, y + 75.5, "START MIXED DECK", 7.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"'), 90
    s = card(B, 14, y, 212, 84) + T(B, 24, y + 16, "Mixed Deck", 11, None, True) + T(B, 24, y + 27, "Pick categories, then start", 6.5, B["mute"])
    for i, nm in enumerate(["UpKeep", "WellNest", "Portfolio"]):
        yy = y + 34 + i * 13; on = i < 2
        s += R(24, yy, 9, 9, JUNGLE if on else "#FFFFFF", JUNGLE if on else "#BDB6AA", 2) + T(B, 38, yy + 7.5, nm, 7.5, B["ink"])
    return s + R(140, y + 56, 76, 20, B["ink"]) + T(B, 178, y + 69, "START", 7, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1.2"'), 90
def s_feat(B, y, o):
    st = o.get("feat", "gold"); nm = "WellNest Dashboard Deck"
    if st == "gold": return R(14, y, 212, 64, "#FBF8F1", "#ECC978", B["r"], 2.5) + T(B, 24, y + 15, "FEATURED", 6, "#B8902F", w=600, ex='letter-spacing="1.2"') + T(B, 24, y + 32, nm, 13, None, True) + T(B, 24, y + 44, "24 pairs, submit goes to WellNest", 6.5, B["mute"]) + T(B, 24, y + 56, "OPEN THE DECK", 6.5, B["ink"], w=600, ex='letter-spacing="1"'), 70
    if st == "band": return R(0, y, W, 60, JUNGLE) + T(B, 14, y + 15, "FEATURED", 6, "#FFFFFFCC", w=600, ex='letter-spacing="1.2"') + T(B, 14, y + 33, nm, 13, "#FFFFFF", True) + T(B, 14, y + 46, "24 pairs, submit goes to WellNest", 6.5, "#FFFFFFCC"), 66
    return card(B, 14, y, 212, 34, "left", JUNGLE) + T(B, 24, y + 15, nm, 9.5, None, True) + T(B, 24, y + 26, "Featured, 24 pairs", 6.5, B["mute"]) + chev(212, y + 17, B["mute"]), 40
def s_apps(B, y, o):
    st = o.get("apps", "chips"); names = ["Style Swipe", "Deck Building", "Dashboards", "Notes"]; s = ""
    if st == "icons":
        for i, nm in enumerate(names): x = 14 + i * 54; c = B["acc"][i]; s += R(x + 11, y, 28, 28, c + "1F", r=8) + tile_icon(x + 18, y + 7, i, c, 14) + T(B, x + 25, y + 40, nm, 6, B["ink"], a="middle")
        return s, 48
    s = T(B, 14, y + 10, "MY APPS", 6.5, B["mute"], w=600, ex='letter-spacing="1.2"'); x = 14
    for i, nm in enumerate(names):
        w = len(nm) * 4.6 + 26
        if x + w > 226: break
        s += R(x, y + 16, w, 18, "#FFFFFF", B["line"], 9) + tile_icon(x + 5, y + 19, i, B["acc"][i], 11) + T(B, x + 19, y + 28, nm, 7, None, True); x += w + 5
    return s, 40
SEC.update(cats=s_cats, mix=s_mix, feat=s_feat, apps=s_apps)
base = dict(title="Deck Building", sub="Style Swipe decks by category")
def M(order, **k): return mock(B, order, **{**base, **k})
P("Category Grouping", "Categories: Plain Headings Or Coloured Chips?",
  ("cg_head", "Plain Headings", "Category name with a thin rule.", "calm", M(["hdr", "cats"])),
  ("cg_chip", "Coloured Chips", "Small accent chip per category.", "visual", M(["hdr", "cats"], cats="chip")))
P("Category Grouping", "Categories: Open Groups Or Folded?",
  ("cg_open", "All Open", "Every deck visible.", "focused", M(["hdr", "cats"], cats="bar")),
  ("cg_fold", "Folded Groups", "Only the first group open.", "quick", M(["hdr", "cats", "mix"], cats="fold")))
P("Category Order", "Order: Newest Activity First Or Fixed Order?",
  ("co_new", "Newest Activity First", "Groups with new decks rise to the top.", "action", M(["hdr", "cats"], cats="chip", hdr="eyebrow", sub="Sorted by newest")),
  ("co_fixed", "Fixed Order", "Same order every day.", "calm", M(["hdr", "cats"], cats="chip", hdr="eyebrow", sub="Fixed category order")))
P("Deck Card Style", "Deck Cards: Outlined Rows Or Grid Cards?",
  ("dc_rows", "Outlined Rows", "One row per deck.", "focused", M(["hdr", "cats"], ncat=2)),
  ("dc_grid", "Grid Cards", "Two cards across, colour top edge.", "visual", M(["hdr", "decks", "mix"], decks="grid", dnames=["UpKeep Board", "WellNest Dashboard", "Folio Dashboard", "Deck Board"], dstat=[(0, 20), (12, 24), (20, 20), (0, 20)])))
P("Deck Card Style", "Deck Cards: White Outline Or Soft Tint?",
  ("dc_line", "White Outline", "Thin border.", "calm", M(["hdr", "cats"], ncat=2, cats="chip")),
  ("dc_tint", "Soft Tint", "Pale accent fill.", "visual", mock({**B, "card": "tint"}, ["hdr", "cats"], **{**base, "ncat": 2, "cats": "chip"})))
P("Progress Display", "Progress: Thin Bar Or Ring?",
  ("pg_bar", "Thin Bar", "Answered of total as a bar.", "focused", M(["hdr", "decks", "apps"], decks="grid", dnames=["UpKeep Board", "WellNest Dashboard", "Folio Dashboard", "Deck Board"], dstat=[(0, 20), (12, 24), (20, 20), (5, 20)])),
  ("pg_ring", "Small Ring", "Fills as you answer.", "visual", M(["hdr", "decks", "apps"], decks="grid", prog="ring", dnames=["UpKeep Board", "WellNest Dashboard", "Folio Dashboard", "Deck Board"], dstat=[(0, 20), (12, 24), (20, 20), (5, 20)])))
P("Progress Display", "Progress: Bar Or Written Count?",
  ("pg_bar2", "Bar Only", "Visual, no numbers.", "calm", M(["hdr", "cats"], ncat=2)),
  ("pg_text", "Written Count", "12 of 24, or New.", "quick", M(["hdr", "cats"], ncat=2, prog="text")))
def partial(st):
    s = T(B, 14, 26, "Deck Building", 15, None, True) + L(14, 34, 226, 34, B["line"])
    for i, (nm, a, n, pt) in enumerate([("WellNest Dashboard Deck", 12, 24, True), ("UpKeep Board Deck", 20, 20, False), ("Folio Dashboard Deck", 0, 20, False)]):
        y = 46 + i * 56; c = B["acc"][i]
        s += card(B, 14, y, 212, 48) + T(B, 24, y + 17, nm, 9.5, None, True) + R(24, y + 26, 140, 3, B["line"], r=1.5) + R(24, y + 26, 140 * a / n, 3, c, r=1.5) + T(B, 24, y + 40, f"{a} of {n}", 6.5, B["mute"])
        if pt:
            if st == "tag": s += R(170, y + 8, 46, 12, SAFFRON + "26", r=6) + T(B, 193, y + 16.5, "PARTIAL", 5.8, "#8A6A0E", w=600, a="middle", ex='letter-spacing=".6"')
            else: s += T(B, 60, y + 40, "Sent partial, 12 left to answer", 6.5, SAFFRON, w=600) + R(176, y + 32, 40, 12, B["ink"]) + T(B, 196, y + 40.5, "RESUME", 5.8, "#FFFFFF", w=600, a="middle")
        elif a == n: s += R(170, y + 8, 46, 12, JUNGLE + "1F", r=6) + T(B, 193, y + 16.5, "SENT", 5.8, JUNGLE, w=600, a="middle")
    return phone(B, s)
P("Progress Display", "Partial Submit: Small Tag Or Line With Resume?",
  ("pt_tag", "Partial Tag", "A saffron tag on the card.", "calm", partial("tag")),
  ("pt_line", "Line And Resume Button", "Says what is left, one tap to resume.", "action", partial("line")))
P("Mixed Deck Picker", "Mixed Deck: Checklist Card Or Chips?",
  ("mx_card", "Checklist Card", "Tick categories, then Start.", "focused", M(["hdr", "mix", "cats"], ncat=1)),
  ("mx_chips", "Toggle Chips", "Tap chips on and off.", "quick", M(["hdr", "mix", "cats"], mix="chips", ncat=1)))
P("Mixed Deck Picker", "Mixed Deck: At The Top Or At The End?",
  ("mx_top", "At The Top", "First thing on the page.", "action", M(["hdr", "mix", "cats"], mix="chips", ncat=2, cats="chip")),
  ("mx_end", "At The End", "After the category groups.", "calm", M(["hdr", "cats", "mix"], mix="chips", ncat=2, cats="chip")))
P("Featured WellNest Card", "Featured Card: Gold Border Or Green Band?",
  ("ft_gold", "Gold Border, Rice Fill", "WellNest colours inside the Max page.", "visual", M(["hdr", "feat", "cats"], ncat=2)),
  ("ft_band", "Jungle Green Band", "Full-width band in a Max accent.", "focused", M(["hdr", "feat", "cats"], feat="band", ncat=2)))
P("Featured WellNest Card", "Featured Card: Big Card Or Pinned Row?",
  ("ft_big", "Big Card", "Stands out above everything.", "visual", M(["hdr", "feat", "cats"], ncat=2, cats="chip")),
  ("ft_row", "Pinned Row", "Same size as a deck, pinned first.", "calm", M(["hdr", "feat", "cats"], feat="row", ncat=2, cats="chip")))
P("My Apps Row", "My Apps: Text Chips Or Icon Row?",
  ("ma_chips", "Text Chips", "Outlined chips with small icons.", "quick", M(["hdr", "apps", "cats"], ncat=2)),
  ("ma_icons", "Icon Row", "App-style icons with labels.", "visual", M(["hdr", "apps", "cats"], apps="icons", ncat=2)))
def naming(st):
    s = T(B, 14, 26, "Deck Building", 15, None, True) + L(14, 34, 226, 34, B["line"])
    rows = [("UpKeep Board Deck", "Layout, tiles, video, approvals", "UPKEEP"), ("WellNest Dashboard Deck", "Header, cards, avatar options", "WELLNEST"), ("Folio Dashboard Deck", "Reports, tiles, charts", "PORTFOLIO"), ("Deck Board Deck", "This page", "BRANDING")]
    if st == "id": rows = [("upkeep-board", "20 pairs", "UPKEEP"), ("wellnest-dashboard", "24 pairs", "WELLNEST"), ("folio-dashboard", "20 pairs", "PORTFOLIO"), ("deck-board", "20 pairs", "BRANDING")]
    for i, (a, b, tg) in enumerate(rows):
        y = 44 + i * 50; c = B["acc"][i]
        s += card(B, 14, y, 212, 42) + T(B, 24, y + 17, a, 10, None, True) + T(B, 24, y + 30, b, 6.5, B["mute"])
        if st != "id": s += R(222 - len(tg) * 4.6 - 12, y + 8, len(tg) * 4.6 + 10, 11, c + "1F", r=5.5) + T(B, 222 - len(tg) * 2.3 - 7, y + 16, tg, 5.5, c, w=600, a="middle", ex='letter-spacing=".6"')
    return phone(B, s)
P("Deck Naming And Labels", "Deck Names: Plain Title With Label Or Short Id?",
  ("nm_title", "Title, Topic Line, Agent Label", "Reads like a sentence.", "calm", naming("title")),
  ("nm_id", "Short Id And Size", "Compact and technical.", "quick", naming("id")))
P("Density", "Density: Airy Or Compact?",
  ("dn_airy", "Airy", "Fewer decks per screen.", "calm", M(["hdr", "cats"], ncat=2, dens=14)),
  ("dn_compact", "Compact", "More decks per screen.", "quick", M(["hdr", "apps", "cats", "mix"], dens=2, mix="chips")))
P("Colour Accents", "Accents: One Colour Per Category Or Ink Only?",
  ("ca_multi", "Colour Per Category", "Terracotta, lagoon, green, saffron.", "visual", M(["hdr", "cats"], cats="chip")),
  ("ca_ink", "Ink Only", "Black and grey, colour only on progress.", "calm", mock({**B, "acc": ["#0A0A0A", "#525252", "#0A0A0A", "#525252"]}, ["hdr", "cats"], **{**base, "cats": "chip"})))
P("Colour Accents", "Progress Colour: Category Colour Or Always Green?",
  ("pc_cat", "Category Colour", "Bar matches the category.", "visual", M(["hdr", "cats"], ncat=2, dstat=None) if False else M(["hdr", "cats"], ncat=2, cats="bar")),
  ("pc_green", "Always Jungle Green", "Progress always reads as green.", "calm", mock({**B, "acc": [JUNGLE] * 4}, ["hdr", "cats"], **{**base, "ncat": 2})))
def typo(upper):
    s = T(B, 14, 34, "DECK BUILDING" if upper else "Deck Building", 24, B["ink"], True, ex='letter-spacing="2"' if upper else "") + T(B, 14, 50, "Style Swipe decks by category", 8, B["mute"]) + L(14, 60, 226, 60, B["line"])
    for i, (h, d) in enumerate([("UpKeep", "UpKeep Board Deck"), ("WellNest", "WellNest Dashboard Deck"), ("Portfolio", "Folio Dashboard Deck")]):
        y = 84 + i * 66; s += T(B, 14, y, h.upper() if upper else h, 13 if not upper else 10, B["ink"], True, ex='letter-spacing="1.5"' if upper else "") + card(B, 14, y + 8, 212, 34) + T(B, 24, y + 29, d, 9.5, None, True)
    return phone(B, s)
P("Typography", "Khand Headings: Title Case Or Spaced Capitals?",
  ("ty_title", "Title Case", "Khand as written, Hind body.", "calm", typo(False)),
  ("ty_caps", "Spaced Capitals", "Khand in tracked capitals.", "focused", typo(True)))
P("Phone Vs Big Monitor", "Big Monitor: Category Columns Or One Grid?",
  ("bm_cols", "One Column Per Category", "UpKeep, WellNest, Portfolio side by side.", "visual", desk(B, [["hdr", "feat", "mix"], ["cats"], ["apps", "decks"]], note="Phone stacks the same blocks", **{**base, "ncat": 1, "cats": "chip", "decks": "list"})),
  ("bm_grid", "One Wide Grid", "All decks in a card grid.", "focused", desk(B, [["hdr", "decks"], ["apps", "decks"], ["mix", "decks"]], note="Phone stacks the same blocks", **{**base, "decks": "grid", "dnames": ["UpKeep Board", "WellNest Dash", "Folio Dash", "Deck Board"]})))
P("Phone Vs Big Monitor", "Phone: Featured First Or Categories First?",
  ("ph_feat", "Featured First", "WellNest card, then categories.", "visual", M(["hdr", "feat", "apps", "cats"], ncat=2, cats="chip")),
  ("ph_cats", "Categories First", "Decks first, featured lower.", "focused", M(["hdr", "apps", "cats", "feat"], ncat=2, cats="chip")))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Deck Board Deck", "Branding", pairs,
        {"brands": ["Deck Building page presentation: category grouping and order, deck cards, progress and partial, Mixed Deck picker, featured WellNest card, My Apps row, naming, density, colour, type, phone vs big monitor",
                    "Max brand: white base, Khand/Hind, small terracotta/lagoon/jungle/saffron accents; example names only"],
         "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "section_counts": cnt, "deck_size": N,
         "sources": {"page": "https://webermanapps.github.io/branding-djqmb410/decks/", "source": "/workspace/branding-dashboard"}},
        seed=1017, n=N)
