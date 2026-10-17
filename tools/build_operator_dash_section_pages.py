#!/usr/bin/env python3
"""Operator Dash: Section Pages And Chief Card (Branding, Oct 17 2026 22:05 ICT; replaces the submitted Company Dashboard Hub Deck).
Covers the NEXT Operator Dash decisions the Hub deck (Max, 21:49 ICT, 14 of 14) did not settle: section page layout and order,
how a placeholder looks once an agent is assigned, Grok Bot 2 hub card details, section tab style, empty-state copy, KPI trend
style, order of operations, Document Center contents and the Grok Bot 2 page. Settled Hub picks are never re-asked.
Option A in every pick = the live hub https://webermanapps.github.io/upkeep-owner-xhcdx0/ (commit 78d1e3d) exactly as it renders
(screenshots of the real page; trend A uses the hub's own sparkline code fed TEST data, assigned A uses the hub's own 'real' state);
Option B = one change made on that same live page in the browser. Images: img/operator-dash-sections/*.jpg (TEST data only).
Captions (R105): 'Operator Dash: <element>, <one sentence>'. Name by theme, no numbers (R113). No Thai references (R110).
Light only, no emoji. usage: build_operator_dash_section_pages.py -> prints {deckId, slug, url}; page written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from team_kit import deck, publish
import caption_rule
from split_deck import theme_name_ok
DID = "upkeep-operator-dash-section-pages-deck"; NAME = "Operator Dash: Section Pages And Chief Card"
assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
IMG = "img/operator-dash-sections"
def shot(name):
    w, h = Image.open(f"{IMG}/{name}.jpg").size; u = f"{IMG}/{name}.jpg"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/><image href="{u}" xlink:href="{u}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/></svg>')
pairs, O, add = deck("odsp_", "UpKeep")
def P(g, el, sentence, key, a, b):
    ask = f"Operator Dash: {el}, {sentence}"
    bad = caption_rule.check(ask); assert not bad, (ask, bad)
    for x in (a, b): assert len(x[0]) <= 34 and len(x[1]) <= 62, x
    add(g, g, O(f"{key}_a", a[0], a[1], a[2], shot(f"{key}_a")), O(f"{key}_b", b[0], b[1], b[2], shot(f"{key}_b")), ask)
P("Section Layout", "Section page layout", "should a section page keep its panels in one stacked column as now or put linked tools in a right-hand column beside the plan and info?", "layout",
  ("One Stacked Column (As Now)", "Numbers, plan, info, then tools, top to bottom.", "calm"),
  ("Tools In A Right Column", "Plan and info on the left, linked tools on the right.", "practical"))
P("Section Order", "Section page order", "should key numbers come first under the section header as now or should the linked tools lead so the work pages are one tap away?", "order",
  ("Key Numbers First (As Now)", "Numbers, then plan, info and tools (phone view).", "calm"),
  ("Linked Tools First", "Tools right under the header, numbers below.", "practical"))
P("Assigned Look", "Newly assigned section", "when a section gets its agent should its card switch straight to Live agent as now or show a Setting up chip until that agent sends its first report?", "assigned",
  ("Straight To Live Agent (As Now)", "Live agent chip and owner the moment one is set.", "bold"),
  ("Setting Up Until First Report", "Amber Setting up chip and a pending note first.", "calm"))
P("Chief Card Details", "Grok Bot 2 hub card", "should the chief card keep only name, role and status as now or add a row of team chips like sections live and open handoffs?", "chief",
  ("Name And Role Only (As Now)", "Chief card with Coming soon and an arrow.", "calm"),
  ("Plus Team Count Chips", "Sections live, open handoffs, daily summary (TEST).", "practical"))
P("Section Tabs", "Section tabs", "should the row of section tabs stay boxed buttons with a black active tab as now or become plain text tabs with an underline on the active one?", "tabs",
  ("Boxed Buttons (As Now)", "Outlined buttons, active tab filled black.", "bold"),
  ("Underline Tabs", "Plain text tabs, active one underlined.", "calm"))
P("Empty State", "Empty-state copy", "should empty panels keep short notes like No data yet as now or say what will fill them and which agent adds it?", "empty",
  ("Short Notes (As Now)", "No data yet, No linked tools yet (Grok Bot 2 page).", "calm"),
  ("Say What Comes And Who", "Each empty panel says what fills it and who adds it.", "practical"))
P("Trend Style", "KPI trend on hub cards", "should the weekly trend be the thin line the hub draws now or small weekly bars with a change label?", "trend",
  ("Thin Trend Line (As Now)", "The hub's own sparkline, fed TEST data.", "calm"),
  ("Weekly Bars + Change", "A bar per week, latest dark, change label (TEST).", "bold"))
P("Order Of Operations", "Order of operations", "should the hub keep showing lanes only as now or add one strip that walks from sign-up to support with each step opening its section?", "ops",
  ("Lanes Only (As Now)", "KPIs, Grok Bot 2, then the four lanes.", "calm"),
  ("One-Line Flow Strip", "Sign-up to Support, each step opens its section.", "practical"))
P("Document Center", "Document Center contents", "should the company Document Center stay empty until agents pin files as now or start with a company shelf of the pitch, forecast, pricing, training and agreement drafts?", "docs",
  ("Empty Until Agents Pin (As Now)", "Kit empty state; agents add files later.", "calm"),
  ("Starter Company Shelf", "Five company files tagged Draft, Plan or Forecast.", "practical"))
P("Chief Page", "Grok Bot 2 page", "should the chief's own page keep the standard section layout as now or open with a team status table of every section with its lane, status and owner?", "chiefpage",
  ("Standard Section Layout (As Now)", "Numbers, plan, info and tools like any section.", "calm"),
  ("Team Status Table On Top", "Every section's lane, status and owner first.", "practical"))
assert len(pairs) == 10, len(pairs)
txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pairs, ensure_ascii=False)), "emoji"
publish(DID, NAME, "UpKeep", pairs, {"brands": [
        "Next decisions for the UpKeep Operator Dash (upkeep-owner-xhcdx0) after the Company Dashboard Hub Deck. Option A is always the live hub as it renders now (78d1e3d, Hub picks 01-14 applied); Option B is one change made on that same live page.",
        "Smart Upkeep brand: white and warm cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only, no emoji. Every number is TEST, Draft, Planned or Forecast; zero real members."],
        "submit_agent": "upkeep", "submit_to": "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", "topic": "operator-dash-section-pages",
        "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105",
        "request": "Replacement for the submitted Company Dashboard Hub Deck (Max, Oct 17 2026 21:49 ICT, 14 of 14): the next Operator Dash decisions the Hub deck did not settle.",
        "replaces": "upkeep-company-dashboard-deck", "follow_on_of": "upkeep-company-dashboard-deck",
        "applies_to": ["UpKeep Operator Dash (company hub, section pages, Grok Bot 2 page), https://webermanapps.github.io/upkeep-owner-xhcdx0/"],
        "example_data": "Every number is TEST, Draft, Planned or Forecast example data.",
        "settled_not_reasked": "Hub deck 21:49 ICT: 01A tile grid, 02B 4 lanes, 03A top-down tree, 04A larger chief card, 05B faded card + chip, 06A shared bottom row, 07A number + trend, 08A initial chip + name, 09A company KPI row, 10A branded band, 11 both Return + section tabs, 12A visible empty slot, 13B phone section carousel, 14A phone KPI carousel",
        "sources": {"content": "tools/build_operator_dash_section_pages.py", "site": "WebermanApps/upkeep-owner-xhcdx0 78d1e3d (index.html, s/index.html, org.js, org.json), screenshots in img/operator-dash-sections"}}, seed=10175, n=10, first=10)
order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
caption_rule.guard(dj["pairs"], DID)
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or "operator-dash-section-pages-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
