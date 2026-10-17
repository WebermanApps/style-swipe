#!/usr/bin/env python3
"""Dashboard Standard decks (Max, Oct 17 2026 10:15-10:16 PM ICT: "you are now responsible for every dashboard design ... propose changes in a deck").
Two requested decks (R83 exception: Max asked): 'Main Dashboard Rules' (Apps Home first) and 'All Boards Rules'.
Each pick proposes ONE overall rule from /workspace/ops/brand/dashboard-review-2026-10-17.md. A = the current state, B = the proposed rule.
Pictures: faithful HTML mocks of the live boards (structure, sizes, colors measured by the review harness, Oct 17 2026 22:20 ICT),
neutral text only, rendered to img/dashboard-standard/*.jpg (source: Branding /workspace/wt/dash-review/mock/mocks.py).
Captions R105. Light only, no emoji, no Thai references in any UpKeep pick (R110). Names by theme, no numbers (R113).
usage: build_dashboard_standard.py -> prints [{deckId, slug, url}]; pages written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from team_kit import deck, publish
import caption_rule
from split_deck import theme_name_ok
IMG = "img/dashboard-standard"
def shot(name):
    w, h = Image.open(f"{IMG}/{name}.jpg").size; u = f"{IMG}/{name}.jpg"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/><image href="{u}" xlink:href="{u}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/></svg>')
MAIN = [
 ("Share", "Apps Home", "Share button", "should Share stay a big outlined button at the bottom of Apps Home or move to the same header icon every agent board uses?", "ah_share",
  ("Bottom Share Button (As Now)", "Outlined Share above the Machan credit."), ("Header Share Icon", "44px icon top right; footer is the credit only.")),
 ("Freshness", "Apps Home", "Updated stamp", "should the Updated stamp stay a typed date or show the real age from the data with a Stale tag after a day, on Apps Home and every board?", "ah_stamp",
  ("Typed Date (As Now)", "Oct 16 10:11 AM on Apps Home, Oct 15 on boards."), ("Real Age + Stale Tag", "Updated 4 min ago; square Stale tag after 24h.")),
 ("Order", "Apps Home", "Phone top order", "should the three utility rows stay above the Grok Bot card on a phone or should Grok Bot come first?", "ah_order",
  ("Utility Rows First (As Now)", "Requested changes, Deck Building, Decks Today."), ("Grok Bot First", "Main bot on top, utility rows after it.")),
 ("Desktop Grid", "Apps Home", "Desktop grid", "should the Grok Bot card stay half width with uneven agent columns at 1280 or span the row with equal-height columns?", "ah_grid",
  ("Half-Width Grok Bot (As Now)", "Blank space beside it and under short columns."), ("Full Row, Even Columns", "Grok Bot spans; three lists match height.")),
 ("Type Floor", "Apps Home", "Small caps labels", "should the 9 to 10px letter-spaced labels like Open Dashboard stay on every row or go, with nothing under 12px anywhere?", "ah_micro",
  ("Tiny Caps Labels (As Now)", "Open Dashboard repeated on every agent row."), ("12px Floor, Arrow Only", "Whole row is the link; plain 13px labels.")),
 ("Counters", "Apps Home", "Deck counters", "should each page keep its own deck numbers or should every counter read the one shared deck-counts file and show once per page?", "ah_count",
  ("Separate Numbers (As Now)", "39 here, 0 and 0.9 on the Grok Bot board."), ("One Shared Count", "Same number everywhere, header only.")),
 ("Roster", "Apps Home", "Agent list", "should Apps Home keep its own agent list or build its rows from the shared agent-dashboards list every tool uses?", "ah_roster",
  ("Own List (As Now)", "Shows Writer, which has no board in the kit list."), ("Shared List", "Rows come from kit/agent-dashboards.json.")),
 ("Status", "Apps Home", "Working dot", "should a working agent keep the small unlabeled green dot or get the square Working tag Grok Bot already uses?", "ah_live",
  ("Green Dot (As Now)", "Small dot beside the name, no label."), ("Square Working Tag", "Same tag as Grok Bot's Working Now chips.")),
 ("Sticky Bar", "Apps Home", "Top bar on scroll", "should the Apps Home top bar stay pinned for the whole page or use the slim bar that boards show for about one screen?", "ah_sticky",
  ("Always Pinned (As Now)", "57px bar stays on screen the whole way down."), ("Slim Bar, Then Hides", "48px bar for about one screen (R87).")),
 ("Fold-Downs", "Apps Home", "Fold-down rows", "should Apps Home keep its own white rounded fold-downs or use the one 48px fold-down row the agent boards use?", "ah_fold",
  ("Own Fold Look (As Now)", "56px, 10px corners, white; boards differ."), ("One Fold Row Everywhere", "48px Khand row, title, count, same chevron.")),
]
ALL = [
 ("Fold-Downs", "All Dashboards", "Fold-down chevron", "should boards keep their mix of fold styles or use the kit row and chevron for every fold-down, header and middle alike?", "ab_fold",
  ("Five Fold Styles (As Now)", "Kit box, caps text, triangle, plus sign, Show."), ("Kit Row And Chevron", "One look; inner folds may drop the band.")),
 ("Corners", "All Dashboards", "Card corners", "should middle sections keep corners from 8 to 999px or go square with 10px only on deck cards and round only on avatars?", "ab_corner",
  ("Mixed Corners (As Now)", "8, 9.6, 12, 14, 16px and round pills."), ("Square, Deck Cards 10px", "Square boxes and tags; avatars stay round.")),
 ("Surfaces", "All Dashboards", "Card shadows and borders", "should some middle cards keep drop shadows and grey borders or all go flat with the thin beige kit border?", "ab_shadow",
  ("Shadows On Some (As Now)", "Soft and hard shadows, grey borders."), ("Flat, Beige Border", "1px #e3ddd2, no shadow, like the header.")),
 ("Type", "All Dashboards", "Type scale", "should headings keep running from 19 to 32px with some 12px Hind titles or follow four fixed Khand and Hind steps?", "ab_type",
  ("Free Sizes (As Now)", "19, 22, 24, 25.6, 28, 32px; 12px Hind titles."), ("Four Steps", "26, 22, 18 Khand; 15 and 13 Hind, 12 floor.")),
 ("Sticky Bar", "All Dashboards", "Sticky bars", "should boards keep their own sticky tab bars under the kit slim bar or allow only one sticky bar per board?", "ab_sticky",
  ("Two Bars Stacked (As Now)", "Board tab bar plus kit slim bar, 96px pinned."), ("One Kit Bar Only", "Board tabs scroll with the page.")),
 ("Identity", "All Dashboards", "Second title bar", "should a board keep a second title bar with its own Share under the header or start the middle straight with content?", "ab_ident",
  ("Second Title Bar (As Now)", "Name, Updated and Share again mid-page."), ("One Header Only", "One title and one Share, in the header.")),
 ("Empty States", "All Dashboards", "Empty states", "should empty panels keep repeated Coming Soon and no trend yet notes or show one line saying what fills them and who adds it?", "ab_empty",
  ("Repeated Placeholders (As Now)", "Coming Soon and no trend yet on every card."), ("One Helpful Line", "What fills it and which agent adds it.")),
 ("Duplicates", "All Dashboards", "Repeated blocks", "should a board keep middle blocks that repeat the header counter and links or show every block only once?", "ab_dupe",
  ("Repeats Kept (As Now)", "Deck Building and decks today shown twice."), ("Each Block Once", "Repeats removed, superseded items archived.")),
 ("Tap Targets", "All Dashboards", "Tap targets", "should small rows and text links from 22 to 36px stay or should every tap target be at least 44px except the 32px remove x?", "ab_tap",
  ("Small Rows And Links (As Now)", "22 to 36px rows, a 23px text link."), ("44px Minimum", "Full rows and button links; x stays 32px.")),
 ("Spacing", "All Dashboards", "Header fold spacing", "should the header fold-downs keep uneven gaps and loose lines under the divider or sit 12px apart with 24px to a clean divider?", "ab_gap",
  ("Uneven Gaps (As Now)", "Wider gap before Document Center, loose stamp."), ("12px Apart, Clean Divider", "Even stack, 24px to the divider.")),
]
def build(DID, NAME, prefix, rows, seed, topic):
    assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
    pairs, O, add = deck(prefix, "Branding")
    for g, loc, el, sentence, key, a, b in rows:
        ask = f"{loc}: {el}, {sentence}"
        bad = caption_rule.check(ask); assert not bad, (ask, bad)
        for x in (a, b): assert len(x[0]) <= 34 and len(x[1]) <= 62, x
        add(g, g, O(f"{key}_a", a[0], a[1], "calm", shot(f"{key}_a")), O(f"{key}_b", b[0], b[1], "practical", shot(f"{key}_b")), ask)
    assert len(pairs) == 10, len(pairs)
    txt = json.dumps(pairs).lower(); assert "thai" not in txt and "thailand" not in txt, "R110"
    publish(DID, NAME, "Branding", pairs, {"brands": [
        "Proposed dashboard standard (Branding, Oct 17 2026). Option A is always the live state found in the review (harness shots at 393 and 1280 of every unlocked board, 22:20 ICT); Option B is the proposed rule.",
        "Max's standard: white and light beige (#fff, #FAF6EE, #e3ddd2), Khand and Hind, square corners, light mode only, no emoji."],
        "submit_agent": "branding", "submit_to": "Branding", "topic": topic, "deck_size": 10, "board": "branding", "audience": "Max",
        "requested": True, "caption_rule": "R105", "review_doc": "/workspace/ops/brand/dashboard-review-2026-10-17.md",
        "request": "Max, Oct 17 2026 10:15-10:16 PM ICT: review every dashboard, overall rules for all dashboards, especially the main dashboard; propose changes in a deck.",
        "applies_to": ["Apps Home https://webermanapps.github.io/a-o956qercs5ubd57y/", "all 21 agent boards (kit/agent-dashboards.json)", "UpKeep Operator Dash upkeep-owner-xhcdx0"],
        "sources": {"content": "tools/build_dashboard_standard.py", "pictures": "img/dashboard-standard (HTML mocks of live boards, neutral text)"}}, seed=seed, n=10, first=10)
    order = [p["ask"] for p in pairs]; dj = json.load(open(f"decks/{DID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
    for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
    caption_rule.guard(dj["pairs"], DID)
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    from agent_links import patch as link_patch
    from chat_button import patch as chat_patch
    pages = json.load(open("decks/pages.json"))
    base = re.sub(r"[^a-z0-9]+", "-", NAME.lower()).strip("-")
    slug = pages.get(DID) or base + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
           "body.carding .opt .vis{min-height:0;overflow:visible}")
    HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    return {"deckId": DID, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}
out = [build("main-dashboard-rules-deck", "Main Dashboard Rules", "mdr_", MAIN, 10177, "dashboard-standard-main"),
       build("all-boards-rules-deck", "All Boards Rules", "abr_", ALL, 10178, "dashboard-standard-all")]
print(json.dumps(out))
