#!/usr/bin/env python3
"""Build Style Swipe deck wellnest-dashboard (Oct 14 2026): WellNest Dashboard Deck, 20 pairs on how the WellNest dashboard
(https://webermanapps.github.io/wellnest-dashboard/, source /workspace/wellnest/dashboard) is presented.
Locked WellNest brand (/workspace/wellnest/brand-rules.md): original nest logo, Cormorant + DM Sans, rice-white base, gold leads, peach accent, sand lines.
Drawn SVG mockups via dash_kit, sample content only. Submit -> agent 'wellnest'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
sys.exit("Retired Oct 15 2026 (Max 12:45 ICT): WellNest decks carry no dashboard layout/structure questions. These decks are now built by tools/wn_fix_no_layout.py; see tools/wn_guard.py.")
from team_kit import deck, publish
from dash_kit import *
DID = "wellnest-dashboard"
GOLD, PEACH, FOREST, SAND, RICE, LEAF = "#ECC978", "#D7A363", "#267D58", "#DABC76", "#FBF8F1", "#AECB35"
GOLDT = "#B8902F"   # darker gold for small text on rice
def logo(cx, cy, w): h = w / (150 / 128); return f'<image href="img/wellnest-logo-circle.png" x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'
B = dict(name="The WellNest", bg=RICE, ink="#1F1D1A", mute="#5E5A52", line=SAND + "88", soft="#F3EEE2", acc=[GOLD, PEACH, FOREST, LEAF],
         head="'Cormorant Garamond', Cormorant, Georgia, serif", body="'DM Sans', sans-serif", r=10, hw=600, logo=logo)
pairs, O, add = deck("wd_", "WellNest")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(sub="Team Dashboard", tnames=["Brand Deck", "Shop", "Stays", "Sauna", "Tea", "Cowork"],
            uitems=["Pick the lead colour", "Approve sign text", "Choose a tea label"], rname="Weekly Report",
            dnames=["Brand Deck Round Two", "The WellNest Brand Deck", "Brand & Product Deck"], fname="Recent Work", rc=PEACH, uc=GOLDT)
def M(order, **k): return mock(B, order, **{**base, **k})
def BD(order, **k): return M(order, **k).replace(">Urgent<", ">Brand Decisions<").replace(" Urgent Items<", " Brand Decisions<").replace(" Need You Today<", " Brand Decisions To Make<")
P("Header And Logo", "Header: Nest Beside The Name Or Stacked Above?",
  ("hd_line", "Nest Beside The Name", "One line, small nest left.", "quick", M(["hdr", "decks", "tiles"], hdr="logo", decks="list", tn=4)),
  ("hd_stack", "Stacked, Centred", "Nest above the name, centred.", "visual", M(["hdr", "decks", "tiles"], hdr="center", decks="list", tn=2)))
P("Header And Logo", "Header: Large Light Title Or Gold Rule Title?",
  ("hd_big", "Large Title, Gold Rule", "Big Cormorant name, short gold line.", "focused", M(["hdr", "report", "decks"], hdr="big", decks="list")),
  ("hd_eyebrow", "Greeting Above", "Small greeting, then the name.", "calm", M(["hdr", "report", "decks"], hdr="eyebrow", sub="Good Morning, Max", decks="list")))
P("Section Order", "First Section: Deck Cards Or Open Items?",
  ("so_decks", "Deck Cards First", "Featured deck right under the header.", "action", BD(["hdr", "decks", "urgent", "feed"], hdr="logo", decks="feature")),
  ("so_open", "Open Items First", "Brand Decisions first, decks below.", "focused", BD(["hdr", "urgent", "feed", "decks"], hdr="logo", urgent="open", decks="list")))
P("Section Order", "Top: Weekly Report Or Brand Decisions?",
  ("so_report", "Report On Top", "Read the week first.", "calm", BD(["hdr", "report", "urgent", "tiles"], hdr="logo", tn=4)),
  ("so_bd", "Decisions On Top", "What needs Max first.", "action", BD(["hdr", "urgent", "report", "tiles"], hdr="logo", urgent="bar", uc=GOLDT, tn=4)))
P("Card Style", "Cards: Sand Outline Or Soft Shadow?",
  ("cs_line", "Sand Outline", "Thin sand border, white card.", "calm", M(["hdr", "report", "decks"], hdr="logo")),
  ("cs_shadow", "Soft Shadow", "No border, light shadow.", "visual", M(["hdr", "report", "decks"], hdr="logo", **{}).replace("", "") if False else mock({**B, "card": "shadow"}, ["hdr", "report", "decks"], **{**base, "hdr": "logo"})))
P("Card Style", "Cards: Gold Tint Or Peach Side Stripe?",
  ("cs_tint", "Gold Tint", "Cards filled with a pale gold.", "visual", mock({**B, "card": "tint"}, ["hdr", "report", "decks"], **{**base, "hdr": "logo"})),
  ("cs_left", "Peach Side Stripe", "White card, peach stripe on the left.", "focused", mock({**B, "card": "left", "acc": [PEACH, GOLD, FOREST, LEAF]}, ["hdr", "report", "decks"], **{**base, "hdr": "logo"})))
P("Brand Decisions Dropdown", "Brand Decisions: Collapsed Or Open?",
  ("bd_closed", "Collapsed With Count", "Tap to open.", "calm", BD(["hdr", "urgent", "decks"], hdr="logo")),
  ("bd_open", "Open List", "All decisions shown.", "action", BD(["hdr", "urgent", "decks"], hdr="logo", urgent="open")))
P("Brand Decisions Dropdown", "Brand Decisions: Quiet Pill Or Gold Bar?",
  ("bd_pill", "Quiet Pill", "Small, opens a list.", "calm", BD(["hdr", "urgent", "report", "decks"], hdr="logo", urgent="pill", uc=GOLDT)),
  ("bd_bar", "Gold Bar", "Full-width gold bar.", "visual", BD(["hdr", "urgent", "report", "decks"], hdr="logo", urgent="bar", uc=GOLDT)))
P("Report Dropdown", "Report: Collapsed Row Or Open Card?",
  ("rp_closed", "Collapsed Row", "Title and Read, opens in place.", "quick", M(["hdr", "report", "decks", "feed"], hdr="logo", report="collapsed")),
  ("rp_card", "Open Card", "First lines always visible.", "calm", M(["hdr", "report", "decks", "feed"], hdr="logo")))
P("Deck Cards", "Deck Cards: One Featured Or All Equal?",
  ("dk_feature", "One Featured Card", "Gold border on the newest deck.", "visual", M(["hdr", "decks", "feed"], hdr="logo", decks="feature")),
  ("dk_equal", "All Equal", "Same card for every deck.", "calm", M(["hdr", "decks", "feed"], hdr="logo", decks="list")))
P("Deck Cards", "Deck Progress: Thin Bar Or Ring?",
  ("dk_bar", "Thin Progress Bar", "Answered out of total as a bar.", "focused", M(["hdr", "decks", "tiles"], hdr="logo", decks="grid", tn=2, dnames=["Round Two", "Brand Deck", "Product Deck", "Shop Deck"], dstat=[(0, 61), (192, 200), (25, 25), (10, 30)])),
  ("dk_ring", "Small Ring", "A ring fills as you answer.", "visual", M(["hdr", "decks", "tiles"], hdr="logo", decks="grid", prog="ring", tn=2, dnames=["Round Two", "Brand Deck", "Product Deck", "Shop Deck"], dstat=[(0, 61), (192, 200), (25, 25), (10, 30)])))
P("Apps And Links", "Apps And Links: Two Columns Or Three Tinted?",
  ("ap_two", "Two Columns", "Outlined tiles.", "calm", M(["hdr", "tiles", "feed"], hdr="logo")),
  ("ap_three", "Three Columns, Tinted", "Smaller tinted tiles.", "quick", M(["hdr", "tiles", "feed"], hdr="logo", cols=3, tiles="tint")))
P("Apps And Links", "Apps And Links: Colour Blocks Or A List?",
  ("ap_solid", "Colour Blocks", "Flat logo colours as tiles.", "visual", mock({**B, "acc": [FOREST, PEACH, "#006F3F", "#B8902F"]}, ["hdr", "tiles"], **{**base, "hdr": "logo", "tiles": "solid", "th": 50})),
  ("ap_rows", "List Rows", "One row per link.", "quick", M(["hdr", "tiles"], hdr="logo", tiles="row")))
P("Density", "Density: Airy Or Compact?",
  ("dn_airy", "Airy", "Open spacing, fewer items.", "calm", BD(["hdr", "report", "urgent", "decks"], hdr="center", dens=14, decks="list", dnames=base["dnames"][:2])),
  ("dn_compact", "Compact", "More on one screen.", "quick", BD(["hdr", "report", "urgent", "decks", "tiles"], hdr="logo", dens=3, report="line", cols=3, th=34, tn=3)))
P("Colour Use", "Lead Colour: Gold Or Peach?",
  ("co_gold", "Gold Leads", "Gold for borders and bars, peach small.", "visual", BD(["hdr", "urgent", "decks", "tiles"], hdr="logo", urgent="bar", uc=GOLDT, decks="feature", dc=GOLD, tn=2)),
  ("co_peach", "Peach Leads", "Peach for borders and bars, gold small.", "calm", BD(["hdr", "urgent", "decks", "tiles"], hdr="logo", urgent="bar", uc=PEACH, decks="feature", dc=PEACH, tn=2)))
P("Colour Use", "Colour: Four Logo Colours Or Mostly Neutral?",
  ("co_four", "Four Flat Pops", "Gold, peach, green and leaf as solid pops.", "visual", M(["hdr", "decks", "tiles"], hdr="logo", decks="grid", tiles="tint", cols=3, tn=3, dnames=["Round Two", "Brand Deck", "Product Deck", "Shop Deck"])),
  ("co_neutral", "Mostly Neutral", "Rice and sand, gold only on the nest.", "calm", mock({**B, "acc": [SAND, SAND, "#8C8576", SAND]}, ["hdr", "decks", "tiles"], **{**base, "hdr": "logo", "decks": "grid", "cols": 3, "tn": 3, "dnames": ["Round Two", "Brand Deck", "Product Deck", "Shop Deck"]})))
P("Typography", "Headings: Light Cormorant Or Semibold?",
  ("ty_light", "Light And Large", "Cormorant light, open spacing.", "calm", mock({**B, "hw": 400}, ["hdr", "report", "decks"], **{**base, "hdr": "big"})),
  ("ty_semi", "Semibold", "Cormorant semibold, tighter.", "focused", mock({**B, "hw": 700}, ["hdr", "report", "decks"], **{**base, "hdr": "big", "dens": 4})))
P("Phone Vs Big Screen", "Big Screen: Three Columns Or Two?",
  ("bs_three", "Three Columns", "Decks, decisions and links side by side.", "visual", desk(B, [["hdr", "decks"], ["report", "urgent"], ["tiles"]], hdr="logo", note="Phone stacks the same blocks in one column", **{k: v for k, v in base.items()})),
  ("bs_two", "Two Columns", "Decks left, everything else right.", "calm", desk(B, [["hdr", "decks", "feed"], ["report", "urgent", "tiles"]], hdr="logo", note="Phone stacks the same blocks in one column", **base)))
P("Phone Vs Big Screen", "Laptop: Wide Two Columns Or One Centred Column?",
  ("lp_two", "Two Columns", "Uses the width.", "focused", desk(B, [["hdr", "decks"], ["report", "tiles"]], label="MacBook", frame="laptop", hdr="logo", note="Same order as the phone", **base)),
  ("lp_one", "One Centred Column", "Reads like the phone, centred.", "calm", desk(B, [["hdr", "decks", "report", "tiles"]], label="MacBook", frame="laptop", hdr="logo", ratio=(224, 140), note="Same order as the phone", **base).replace('scale(1.003)', 'scale(1.003)')))

# ---------- Avatar / thumbnail icon (candidates /workspace/wellnest/avatar/opt1-5.png, copied to img/wellnest-avatar/) ----------
def avimg(k, cx, cy, d, tile=None, clip=True):
    s = ""
    if tile: s += R(cx - d / 2, cy - d / 2, d, d, tile, SAND + "66", d * .22)
    ex = 'style="mix-blend-mode:multiply"'
    return s + f'<image href="img/wellnest-avatar/opt{k}.png" x="{cx-d/2}" y="{cy-d/2}" width="{d}" height="{d}" preserveAspectRatio="xMidYMid meet" {ex}/>'
def avscreen(k, tile=None, bg=RICE, cap=""):
    s = avimg(k, 120, 86, 112, tile) + T(B, 120, 170, "The WellNest", 18, None, True, a="middle") + T(B, 120, 184, cap, 7, B["mute"], a="middle")
    s += L(24, 198, 216, 198, B["line"]) + T(B, 24, 214, "SMALL SIZES", 6, B["mute"], w=600, ex='letter-spacing="1.2"')
    for i, d in enumerate([48, 32, 20, 14]): s += avimg(k, 46 + i * 50, 248, d, tile)
    return screen(s, bg)
def avsmall(k):
    s = T(B, 120, 26, "At Small Sizes", 14, None, True, a="middle")
    s += R(14, 40, 212, 46, "#FFFFFF", B["line"], 10) + avimg(k, 36, 63, 30) + T(B, 58, 60, "The WellNest", 9, None, True) + R(58, 66, 120, 3, B["mute"] + "55", r=1.5)
    s += R(14, 94, 212, 70, "#FFFFFF", B["line"], 10) + "".join(avimg(k if i == 1 else None, 46 + i * 50, 122, 34, "#F3EEE2") if i == 1 else R(29 + i * 50, 105, 34, 34, "#E9E4D8", r=8) for i in range(4)) + T(B, 120, 156, "Home screen", 6.5, B["mute"], a="middle")
    s += R(14, 172, 212, 34, "#FFFFFF", B["line"], 10) + avimg(k, 30, 189, 16) + T(B, 44, 192, "Browser tab, 16 px", 7.5, B["ink"])
    s += R(14, 214, 212, 34, "#FFFFFF", B["line"], 10) + avimg(k, 30, 231, 20) + R(44, 226, 100, 3, B["ink"] + "44", r=1.5) + R(44, 233, 70, 3, B["mute"] + "44", r=1.5)
    return screen(s, RICE)
G = "Avatar And Thumbnail Icon"
P(G, "Avatar: Fine Threads Or Four Bold Loops?",
  ("av_threads", "Fine Threads With Tails", "Option 1: many fine loops, two tails.", "calm", avscreen(1, cap="Option 1")),
  ("av_bold", "Four Bold Loops", "Option 2: four thick loops.", "visual", avscreen(2, cap="Option 2")))
P(G, "Avatar: Loops With A Sprout Or Nest Bowl With Eggs?",
  ("av_sprout", "Loops With A Sprout", "Option 3: a sprout in the nest.", "visual", avscreen(3, cap="Option 3")),
  ("av_eggs", "Nest Bowl With Eggs", "Option 4: two eggs in a low nest.", "calm", avscreen(4, cap="Option 4")))
P(G, "Avatar: Loops On A Cream Tile Or Bold Loops?",
  ("av_tile5", "Loops On A Cream Tile", "Option 5: loops and a green dot on cream.", "calm", avscreen(5, cap="Option 5")),
  ("av_bold_b", "Four Bold Loops", "Option 2 again, for a direct match.", "focused", avscreen(2, cap="Option 2")))
P(G, "Icon Background: Cream Tile Or Plain White?",
  ("av_cream", "On A Cream Tile", "Rounded cream tile behind the loops.", "calm", avscreen(3, tile="#F7EEDB", bg="#FFFFFF", cap="Option 3 on cream")),
  ("av_white", "Plain, No Tile", "Loops straight on white.", "quick", avscreen(3, bg="#FFFFFF", cap="Option 3, no tile")))
P(G, "Small Sizes: Fine Threads Or Bold Loops?",
  ("av_sm_fine", "Fine Threads, Small", "Option 1 at tab and home-screen size.", "calm", avsmall(1)),
  ("av_sm_bold", "Bold Loops, Small", "Option 2 at tab and home-screen size.", "focused", avsmall(2)))
N = len(pairs); assert 20 <= N <= 24, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "WellNest Dashboard Deck", "WellNest", pairs,
        {"brands": ["WellNest dashboard presentation: header and logo, section order, card style, Brand Decisions and report dropdowns, deck cards, apps, density, colour, type, phone vs big screen, avatar/thumbnail icon (options 1-5)",
                    "Locked WellNest brand: original nest logo, Cormorant + DM Sans, rice-white base, gold leads, peach accent, sand lines; sample content only"],
         "submit_agent": "wellnest", "submit_to": "WellNest Agent", "section_counts": cnt, "deck_size": N,
         "sources": {"dashboard": "https://webermanapps.github.io/wellnest-dashboard/", "source": "/workspace/wellnest/dashboard", "rules": "/workspace/wellnest/brand-rules.md", "avatars": "/workspace/wellnest/avatar/opt1-5.png"}},
        seed=1015, n=N)
