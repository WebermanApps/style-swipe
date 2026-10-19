"""Command Center Layout Deck + Command Center Tiles Deck (Max, Oct 19 2026 10:40 PM ICT: Ethan's UpKeep Command Center redo, uk12).
Ten pairs each, every option a REAL screenshot of the staged uk12 Command Center (TEST snapshot as of Jan 1 2027, members by first
name only), the variant made by a small CSS/JS override at shot time (Swatch handoff tools/uk12-src/deck_shots.py).
Dadbook layout in Max's brand (tools/eve1019_page.py), team-gated submit via ../submit.js as agent branding (unchanged).
Screens are embedded in the locked page only; decks/<id>.json keeps labels and captions (same shape as the Machan decks).
Usage: python3 tools/build_cc_decks_1019.py <shots_dir>   (repo root)"""
import base64, json, os, re, secrets, string, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))
import caption_rule, eve1019_page as PG
from split_deck import theme_name_ok
from md1018_kit import EMOJI
from PIL import Image
BAD = re.compile(r"wickfield|2573|\bthai|thailand|[\u0E00-\u0E7F]|@|\(\d{3}\)|\b\d{5}\b|\blat\b|\blng\b|\bstreet\b", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
TO = "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78"
L = "UpKeep Command Center"
LAYOUT = [
 ("l01", "Tile grid", "Tile grid, how the four agent tiles sit across Ethan's wide screen",
  ("Four across", "All four agents side by side, everything above the fold."), ("Two by two", "Bigger tiles in two rows; the lower row needs a scroll.")),
 ("l02", "Ethan strip", "Ethan's strip, where priorities, alerts and Waiting on Max sit",
  ("Strip across the top", "One band over the tiles: priorities, alerts, waiting on Max."), ("Side rail on the left", "A tall rail beside the tiles, read top to bottom.")),
 ("l03", "Density", "Density, how much each tile shows before you open anything",
  ("Calm, lists folded", "Four rows a list, folds closed with a one-line summary."), ("Dense, lists open", "Smaller type, longer lists and the top fold already open.")),
 ("l04", "Tile widths", "Tile widths, whether every agent gets the same width or the busiest leads",
  ("Equal tiles", "Same width for every agent, fixed order."), ("Busiest tile leads wider", "The tile with the most waiting on Max goes first and wider.")),
 ("l05", "Row actions", "Row actions, how buttons like Approve show inside a tile",
  ("Inside the row fold", "Tap a row to see its buttons; the list stays short."), ("Always showing", "Buttons sit open on every row, nothing to tap first.")),
 ("l06", "Phone order", "Phone order, what Ethan sees first on his phone",
  ("Priorities first", "Today's priorities, then alerts, then waiting on Max."), ("Waiting on Max first", "Approvals lead, then priorities and alerts.")),
 ("l07", "Phone tiles", "Phone tiles, how each agent tile looks on a phone",
  ("Full tiles", "Each tile shows its lists and folds; longer scroll."), ("Numbers only, tap to open", "Just the four numbers per agent; tap for the list.")),
 ("l08", "Header", "Header, how the title, mark and Apps Home line up",
  ("One-row header", "Apps Home, mark, title and chip on one line."), ("Two-row header", "Apps Home on its own line, the title row below it.")),
 ("l09", "Tile numbers", "Tile numbers, how the four key numbers sit at the top of a tile",
  ("Boxed numbers", "A soft framed row of four numbers with small notes."), ("Big open numbers", "Larger numbers on the tile itself, no frame.")),
 ("l10", "Side margins", "Side margins, how much cream sits at the edges of the big screen",
  ("About five percent", "Roomy edges; tiles a little narrower."), ("Slim edges", "About two percent; tiles use nearly the full width.")),
]
TILES = [
 ("t01", "Members tile", "Members tile, what leads the Members agent tile",
  ("Messages first", "Open member messages lead, first visit week in a fold."), ("First visit week first", "The first visit week leads, messages move down.")),
 ("t02", "Technicians tile", "Technicians tile, how the first week's routes are laid out",
  ("Grouped by tech dash", "One list, a heading per tech dash, two stops each."), ("Three tech dash columns", "Each tech dash in its own column, side by side.")),
 ("t03", "Tools tile", "Tools and Equipment tile, how vans below minimum are shown",
  ("Bars plus the short list", "A bar per van and the low lines listed below."), ("Bars only", "Thicker bars per van; tap a bar for the lines.")),
 ("t04", "Scheduling week", "Scheduling week, how each day's load shows in the week strip",
  ("Dots per tech dash", "Small dots fill per tech dash up to four stops a day."), ("Big day numbers", "One large number per day, no dots.")),
 ("t05", "Alerts style", "Alerts style, how alerts read in Ethan's strip",
  ("Tag chips", "Each alert ends in a small coloured tag: Urgent, Safety flag."), ("Thin terracotta edge", "A soft tinted row with a terracotta edge, no tags.")),
 ("t06", "Fold downs", "Fold downs, whether the longer lists start closed or open",
  ("Closed with a summary", "Each fold shows a one-line summary until tapped."), ("Top folds open", "The busiest folds start open; longer tile.")),
 ("t07", "Open full board link", "Open full board link, how each tile links to its full board",
  ("Small link top right", "A quiet text link beside the tile title."), ("Button at the bottom", "A full-width rounded button under the tile.")),
 ("t08", "Shine level", "Shine level, how much light plays on the tiles",
  ("Subtle shine", "A faint top-edge highlight and a slow, soft sheen."), ("Brighter shine", "A stronger edge line, warmer glow and brighter sheen.")),
 ("t09", "Needs Max box", "Needs Max box, the colour of the box holding what waits on Max",
  ("Lagoon blue box", "Calm blue edge and tint, like the other info boxes."), ("Terracotta box", "Warm terracotta edge and tint so it stands out.")),
 ("t10", "Filters", "Filters, how the filter buttons above a list look",
  ("Pill chips", "Rounded chips with counts; the chosen one goes dark."), ("Underlined tabs", "Plain words with a lagoon underline on the chosen one.")),
]
DECKS = [("branding-command-center-layout-deck", "Command Center Layout Deck", "command-center-layout-deck", LAYOUT, "Layout",
          "Ten pairs from real screenshots of Ethan's new Command Center (TEST data). Pick how the big screen and the phone should be laid out."),
         ("branding-command-center-tiles-deck", "Command Center Tiles Deck", "command-center-tiles-deck", TILES, "Tiles",
          "Ten pairs from real screenshots of Ethan's new Command Center (TEST data). Pick what each agent tile shows and how it feels.")]
STRIP = 34
def svg(path):
    """Box follows the shot (no shrinking of tile close-ups); tall phone shots get cream sides so a pair stays a sane height."""
    im = Image.open(path); w, h = im.size; BOXW, BOXH = max(w, round(h * .75)), h + STRIP; dw, dh = w, h; x, y = (BOXW - w) // 2, 0
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOXW} {BOXH}" role="img"><rect width="{BOXW}" height="{BOXH}" fill="#F6F0E4"/>'
            f'<image x="{x}" y="{y}" width="{dw}" height="{dh}" preserveAspectRatio="xMidYMid meet" href="data:image/webp;base64,{b64}"/>'
            f'<rect y="{BOXH - STRIP}" width="{BOXW}" height="{STRIP}" fill="#FFFEFB"/><text x="16" y="{BOXH - 11}" font-family="Hind,sans-serif" font-size="18" fill="#6B645A">'
            f'TEST data · real uk12 Command Center screenshot</text></svg>')
if __name__ == "__main__":
    shots = sys.argv[1]; pages = json.load(open("decks/pages.json")); sizes = json.load(open("decks/sizes.json")); out = []
    for did, name, slug_base, cards, em, lede in DECKS:
        assert theme_name_ok(name) and not NUMW.search(name), name
        pairs = []
        for i, (k, cat, cap, a, b) in enumerate(cards, 1):
            ask = f"{L}: {cap}."
            assert len(a[0]) <= 34 and len(b[0]) <= 34 and len(a[1]) <= 72 and len(b[1]) <= 72, k
            pairs.append({"group": cat, "category": cat, "ask": ask,
                          "optionA": {"id": f"{did}_{i:02d}a", "label": a[0], "desc": a[1]},
                          "optionB": {"id": f"{did}_{i:02d}b", "label": b[0], "desc": b[1]}})
        assert len(pairs) == 10; caption_rule.guard(pairs, did)
        blob = json.dumps(pairs, ensure_ascii=False); assert not BAD.search(blob), BAD.search(blob); assert not EMOJI.search(blob)
        slug = pages.get(did) or slug_base + "-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
        dj = {"date": did, "version": 1, "format": "pairs", "english_only": False, "light_only": True, "title": name,
              "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "status": "published", "submit_agent": "branding",
              "board": "branding-djqmb410", "audience": "Max", "requested": True, "deck_size": 10, "built_by": "Branding (Swatch)",
              "page": slug + "/", "pairs": [dict(p, id=f"{did}-{i:02d}") for i, p in enumerate(pairs, 1)]}
        json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        pj = dict(dj, submit_to=TO, pairs=[])
        for (k, *_), p in zip(cards, dj["pairs"]):
            q = json.loads(json.dumps(p)); q["optionA"]["visual"] = {"svg": svg(os.path.join(shots, k + "a.webp"))}
            q["optionB"]["visual"] = {"svg": svg(os.path.join(shots, k + "b.webp"))}
            assert "TEST" in q["optionA"]["visual"]["svg"] and "TEST" in q["optionB"]["visual"]["svg"]; pj["pairs"].append(q)
        PG.write(pj, slug, dict(kicker="Max's Picks · " + L, lede=lede, em=em))
        pages[did] = slug; sizes[did] = 10
        url = f"https://webermanapps.github.io/style-swipe/{slug}/"; out.append((did, name, url)); print(did, url, os.path.getsize(slug + "/index.html"))
    json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False); json.dump(sizes, open("decks/sizes.json", "w"), indent=1, ensure_ascii=False)
