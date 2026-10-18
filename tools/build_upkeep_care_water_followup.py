#!/usr/bin/env python3
"""Care Cards And Water Protection Follow-Up (Branding, Oct 18 2026 ICT). One 10-pick follow-up for UpKeep after Max's 09:24-09:26 ICT results:
- What We Take Care Of: Card Colors And Finish (9/10): 01 B every card its own colour, 02 A flat white face, 03 B thin colour band on top,
  04 B fine line icons, 05 B deeper lifted shadow, 06 A underlined See All link, 07 skipped (note 'What do you think ?'), 08 A soft filled chips,
  09 B warm cream band, 10 B dot in the card's colour.
- Extras Ideas Deck (10/10): 01 both (Water Leak Sensor Setup + Sump Pump Battery Backup), 05 B Range Hood Filter Degrease, 06 B Bath Fan
  Clean And Check, 07 A Smart Thermostat Install; 02-04 and 08-10 neither -> queue/extras-do-not-propose.json (never proposed again).
Picks: 01 the skipped Section Header re-asked once, reworded, with Branding's recommendation (Bold Khand Title) in the caption, both options shown;
02-06 detail choices on the WWTCO winners (A = section with every settled pick applied); 07-10 how the Extras winners are shown and worded.
Never re-asks a settled pick or a rejected Extras idea; never proposes Pool Opening/Closing, Snow Removal, Extra Handyman Hours, Pest Control or
Irrigation Backflow Test. WWTCO rows stay a plain list (no tap-for-more), tight rows. Drawn mockups, Notes on every pick, light only, Khand/Hind,
R105 captions ('Website: <section>, <element>: <sentence>' form set by Max), no Thai (R110), name by theme with no numbers (R113).
Reuses the drawing code of build_upkeep_wwtco_colors.py and build_upkeep_full_review.py (exec of their helper prefix only; nothing published by them).
Page written UNLOCKED: lock with lock_pages.py before commit."""
import os, sys, json, re, string, secrets
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(ROOT); sys.path.insert(0, HERE)
G = globals()
exec(compile(open(os.path.join(HERE, "build_upkeep_wwtco_colors.py")).read().split("\ndef P2(")[0], "wwtco_helpers", "exec"), G)
_WD, _WCREAM = D, CREAM  # WWTCO settled-look dict; full review defines its own D()/CREAM
_fr = open(os.path.join(HERE, "build_upkeep_full_review.py")).read()
exec(compile(_fr[:_fr.index("\nD(\"site\"")] if "\nD(\"site\"" in _fr else _fr.split("# ================= EXTRAS IDEAS")[0].split("\ndef D(")[0], "fr_helpers", "exec"), G)
_x = "XICO = " + _fr.split("\nXICO = ")[1].split("\ndef extras_picks")[0]
exec(compile(_x, "fr_extras", "exec"), G)
D, CREAM = _WD, _WCREAM
from team_kit import deck as kdeck, publish
import caption_rule
from split_deck import theme_name_ok
DID = "upkeep-care-cards-and-water-protection-follow-up-deck"; NAME = "Care Cards And Water Protection Follow-Up"
assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
DNP = json.load(open("queue/extras-do-not-propose.json"))
NEVER = [x["name"].lower() for x in DNP["removed_by_max"] + DNP["rejected"]] + ["pool", "snow removal", "handyman", "pest control", "backflow"]
# ---- What We Take Care Of: every settled pick applied (Card Colors And Finish 01B 02A 03B 04B 05B 06A 08A 09B 10B + earlier tight plain rows) ----
SET = dict(D, colors="own", face="flat", band=True, iconline=True, shadow="deep", seebtn="link", headbig=False, chip="soft", bg="cream", dots="card")
EXT = dict(bandh=6, iconsw=1.4, shtint=False, cream=CREAM, hair=True)
_card0 = card
def card(x, y, c, o):   # settled card + the follow-up detail knobs (band height, line weight, shadow tint)
    o = dict(EXT, **o); nm, ic_, items, tint = c; tc, bg = TINT[tint]; h = card_h(o)
    s = _card0(x, y, c, dict(o, band=False, shadow="none-x" if False else o["shadow"]))
    if o["shtint"]:  # recolour the shadow (first rect) in the card's own colour
        s = s.replace('fill="#0A0A0A"', f'fill="{tc}"', 1).replace('opacity=".13"', 'opacity=".22"', 1)
    if o["band"]:
        bh = o["bandh"]
        s += f'<path d="M{x} {y + 14} a14 14 0 0 1 14 -14 h{CW - 28} a14 14 0 0 1 14 14 v{-(14 - bh)} h-{CW} z" fill="{tc}"/>' if bh < 14 else ""
    if o["iconline"] and o["iconsw"] != 1.4: s = s.replace('stroke-width="1.4"', f'stroke-width="{o["iconsw"]}"')
    return s
G["card"] = card
_section0 = section
def section(o, y0=0):
    o = dict(EXT, **o); s, h = _section0(o, y0)
    if o["bg"] == "cream":
        s = s.replace(f'fill="{CREAM}"', f'fill="{o["cream"]}"', 1)
        if not o["hair"]: s = re.sub(r'<line [^>]*stroke="#EFE8DC"/>', "", s, count=2)
    return s, h
G["section"] = section
def M(over=None, note="", close="card"): return mock(dict(SET, **(over or {})), note=note, close=close)
# ---- Extras: live grid + the winners; bundle tile variant ----
LIVE = LIVE_X
def X_grid(tiles, detail, price, unit="one time"):
    """tiles = [(icon, label, new?)] appended after the live seven; detail = (icon, name, desc)."""
    y = 32; s = rect(20, y, 200, 256, "#FAF3EB")
    s += rect(20, y + 14, 200, 242, "#FFFFFF", "none", 10) + t(28, y + 32, "Shop À La Carte", 13, INK, "khand", 700) + t(210, y + 31, "×", 12, INK, "hind", 400, "end")
    s += t(28, y + 43, "Optional services for any membership.", 7.5, MUTE)
    items = [(a, b, False) for a, b in LIVE] + tiles
    gy = y + 50; w = 45; hgt = 50 if len(items) <= 8 else 45
    for i, (ic_, lab, new) in enumerate(items[:12]):
        cx0 = 26 + (i % 4) * (w + 2); yy = gy + (i // 4) * (hgt + 2)
        s += rect(cx0, yy, w, hgt, "#FFFFFF", LAGOON if new else "#E4D6C4", 0, 1.6 if new else 1)
        s += suico(ic_, cx0 + w / 2 - (10 if hgt == 50 else 8), yy + 3, 20 if hgt == 50 else 16) + tile_lab(cx0, cx0 + w / 2, yy + (32 if hgt == 50 else 25), lab, INK if new else "#3a3a3a")
        if new: s += rect(cx0 + w - 20, yy - 5, 22, 9, JUNGLE, "none", 4) + t(cx0 + w - 9, yy + 1.5, "NEW", 7.5, "#FFFFFF", "hind", 700, "middle")
    rows = (min(len(items), 12) + 3) // 4
    dy = gy + rows * (hgt + 2) + 4
    ico, name, desc = detail
    s += rect(26, dy, 188, min(74, 284 - dy), "#FFFFFF", "#E4D6C4", 0, 1) + suico(ico, 32, dy + 6, 22) + t(60, dy + 15, name, 9.5, INK, "khand", 700)
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        if len(cur + " " + wd) > 36 and cur: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur)
    for i, l in enumerate(lines[:3]): s += t(60, dy + 26 + i * 9, l, 7.5, MUTE)
    s += t(60, dy + 56, f"Example ${price} · {unit}", 8, INK, "hind", 700)
    s += rect(170, dy + 46, 38, 15, TERRA, "none", 3) + t(189, dy + 56.5, "ADD", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return frame("Shop À La Carte: Extras", phone(s), TERRA, "EXAMPLE PRICE")
pairs, O, add = kdeck("ccwf_", "UpKeep")
_n = [0]
def P(grp, ask, a, b, purpose="new"):
    _n[0] += 1; k = f"{_n[0]:02d}_"
    bad = [x for x in caption_rule.check(ask) if not x.startswith("vague location")]; assert not bad, (ask, bad)
    low = ask.lower(); assert not any(w in low for w in ("spacing", " tap", "more info", "more-info", "flip", "expand", "sheet")), ask
    for x in (a, b):
        assert len(x[1]) <= 34 and len(x[2]) <= 62, x[:3]
        assert not any(n in (x[1] + " " + x[2]).lower() for n in NEVER), x[:2]
    assert not any(n in low for n in NEVER), ask
    add(grp, grp, O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask, purpose=purpose)
WW = "Website: What We Take Care Of, "
# 01 skipped 07 re-asked once, reworded, with our recommendation (Max asked 'What do you think ?')
P("Section Header", WW + "section header: we recommend keeping the bold Khand title because it matches the brand headings on every other UpKeep section and reads better on a phone than small capitals, so keep it or switch to the small capitals label?",
  ("khand", "Bold Khand Title (Recommended)", "Matches every other UpKeep heading; easy to read on a phone.", "calm", M(close="head", note=("Bold Khand title, as now", "Our pick: same as every UpKeep heading"))),
  ("label", "Small Capitals Label", "Spaced terracotta capitals with a short line.", "practical", M({"headbig": True}, close="head", note=("Small spaced capitals label", "Harder to read at phone size"))), purpose="reask")
P("Colour Band", WW + "colour band: you picked a thin band in each card's colour along the top, so should it stay a hairline strip or be a little bolder?",
  ("thin", "Hairline Band, 3px", "A fine strip of colour along the top edge.", "calm", M({"bandh": 3}, close="grid", note=("3px colour band", "Each card in its own colour"))),
  ("bold", "Bolder Band, 6px", "A clearer stripe that reads at a glance.", "practical", M({"bandh": 6}, close="grid", note=("6px colour band", "Same colours, a little stronger"))))
P("Line Icons", WW + "line icons: with the icons now drawn as lines in the card's own colour, should the lines stay fine or be a touch heavier?",
  ("fine", "Fine Lines, 1.4px", "Light, airy icons in the card colour.", "calm", M(note=("Fine line icons, 1.4px", "Water card shown"))),
  ("med", "Medium Lines, 2px", "Slightly heavier so icons hold up when small.", "practical", M({"iconsw": 2}, note=("Medium line icons, 2px", "Same icons, a little bolder"))))
P("Lifted Shadow", WW + "lifted shadow: you picked the deeper shadow, so should it be a neutral grey or a soft shade of each card's own colour?",
  ("grey", "Neutral Grey Shadow", "Plain soft grey under every card.", "calm", M(note=("Neutral grey lifted shadow", "Same depth on every card"))),
  ("tint", "Shadow In The Card Colour", "A faint lagoon, terracotta or mustard glow.", "playful", M({"shtint": True}, note=("Shadow tinted in the card's colour", "Lagoon here, on the Water card"))))
P("Cream Band", WW + "cream band: you picked the warm cream band behind the cards, so should it keep faint lines at its top and bottom edge or blend in with no lines?",
  ("lines", "Faint Edge Lines", "Hairlines frame the cream band.", "calm", M(close="grid", note=("Cream band with faint edge lines", "Top and bottom hairlines"))),
  ("none", "No Edge Lines", "Cream fades straight into the white page.", "calm", M({"hair": False}, close="grid", note=("Cream band, no edge lines", "Softer join with the page"))))
P("Cream Shade", WW + "cream shade: should the band behind the cards be the warm brand cream or a lighter ivory that sits closer to white?",
  ("warm", "Warm Brand Cream", "The same cream as the site header.", "calm", M(close="grid", note=("Warm brand cream #FAF6EE", "Matches the header strip"))),
  ("ivory", "Lighter Ivory", "A paler cream, cards still stand out.", "calm", M({"cream": "#FCFAF5"}, close="grid", note=("Lighter ivory #FCFAF5", "Closer to the white page"))))
WX = "Website: Extras, "
LEAK = ("meter", "Water Leak Sensor Setup", "Leak sensors under sinks, by the water heater and washer, linked to your phone.")
SUMP = ("shield", "Sump Pump Battery Backup", "A battery backup pump that keeps the basement dry when the power goes out.")
P("Water Protection", WX + "water protection: you said maybe both, so should Leak Sensor Setup and Sump Pump Battery Backup be two separate tiles or one Water Protection bundle?",
  ("two", "Two Separate Tiles", "Each has its own tile and its own price.", "practical", X_grid([("meter", "Water Leak Sensor", True), ("shield", "Sump Pump Backup", True)], LEAK, "149")),
  ("bundle", "One Water Protection Bundle", "One tile with both, one price, small saving.", "practical", X_grid([("meter", "Water Protection Bundle", True)], ("meter", "Water Protection Bundle", "Leak sensors linked to your phone plus a battery backup sump pump, set up together."), "749")))
HOOD = ("duct", "Range Hood Filter Degrease", "Degrease or replace range hood filters so the fan pulls smoke out.")
P("Range Hood", WX + "range hood name: the winning kitchen extra should keep the name Range Hood Filter Degrease or use the shorter Range Hood Filter Clean?",
  ("degrease", "Range Hood Filter Degrease", "Name as picked; says exactly what we do.", "practical", X_grid([("duct", "Range Hood Degrease", True)], HOOD, "75")),
  ("clean", "Range Hood Filter Clean", "Shorter, plainer word on the tile.", "calm", X_grid([("duct", "Range Hood Filter Clean", True)], ("duct", "Range Hood Filter Clean", "Clean or replace range hood filters so the fan pulls smoke out."), "75")))
P("Bath Fan", WX + "bath fan detail: should Bath Fan Clean And Check include a photo in the visit report showing where the fan vents, or a written note only?",
  ("photo", "Photo Of The Vent In The Report", "Member sees where the fan vents outside.", "practical", X_grid([("duct", "Bath Fan Clean And Check", True)], ("duct", "Bath Fan Clean And Check", "Clean bathroom exhaust fans, check they vent outside, with a photo of the vent in your visit report."), "95")),
  ("note", "Written Note Only", "A short line in the report, no photo.", "calm", X_grid([("duct", "Bath Fan Clean And Check", True)], ("duct", "Bath Fan Clean And Check", "Clean bathroom exhaust fans and check they vent outside; noted in your visit report."), "95")))
P("Smart Thermostat", WX + "smart thermostat detail: should Smart Thermostat Install mean we bring a recommended thermostat, or we install the one the member buys?",
  ("bring", "We Bring A Recommended One", "One price with the thermostat included.", "practical", X_grid([("clock", "Smart Thermostat Install", True)], ("clock", "Smart Thermostat Install", "We bring a recommended smart thermostat, install it and set it up on your phone."), "325")),
  ("yours", "We Install The One You Buy", "Lower price; member picks the device.", "calm", X_grid([("clock", "Smart Thermostat Install", True)], ("clock", "Smart Thermostat Install", "Install and set up the smart thermostat you buy, connected to your phone."), "175")))
assert len(pairs) == 10, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Follow-up to What We Take Care Of: Card Colors And Finish and the Extras Ideas Deck (Max, Oct 18 2026 09:24-09:26 ICT). WWTCO picks: Option A is the section with every settled pick applied (own colour per card, flat white face, colour band on top, line icons, deeper shadow, underlined See All, soft chips, warm cream band, dot in the card colour; plain list rows, tight rows, no tap-for-more). Extras picks: how the winners are shown and worded.",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon, jungle and mustard accents, Khand and Hind, light mode only."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "care-cards-and-water-protection-follow-up",
        "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Max Oct 18 2026 09:24 ICT note on Card Colors 07 Section Header: 'What do you think ?' (Branding recommends Bold Khand Title); Extras 01 note 'Maybe both ?'.",
        "follow_on_of": ["upkeep-what-we-take-care-of-card-colors-and-finish-deck", "upkeep-extras-ideas-deck"],
        "applied_picks": "Card Colors 01B 02A 03B 04B 05B 06A 08A 09B 10B; Extras winners Water Leak Sensor Setup + Sump Pump Battery Backup (both), Range Hood Filter Degrease, Bath Fan Clean And Check, Smart Thermostat Install",
        "not_reasked": "Settled Card Colors picks; rejected Extras ideas (queue/extras-do-not-propose.json); R118 removed extras; no tap-for-more or spacing asks",
        "sources": {"content": "tools/build_upkeep_care_water_followup.py", "site": "WebermanApps/smart-upkeep app.js (WW_CATS, extrasEntry), pricing-config.js addons"}}, seed=10181, n=10, first=0)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
dj["pairs"][0]["carried_from"] = "upkeep-what-we-take-care-of-card-colors-and-finish-deck-07"
assert len(dj["pairs"]) == 10 and all(p.get("notes") for p in dj["pairs"])
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "care-cards-water-follow-up-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
pages = json.load(open("decks/pages.json")); pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "picks": [f'{q["optionA"]["label"]} vs {q["optionB"]["label"]}' for q in dj["pairs"]]}, indent=1))
