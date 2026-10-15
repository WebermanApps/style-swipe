#!/usr/bin/env python3
"""UpKeep (Smart Upkeep) Forecasting And Projections Deck (Oct 16 2026): 20 text this-or-that pairs on what to include in forecasts and how to view projections.
Same pattern as build_security_duties.py (white, beige accents, Khand/Hind, Notes + Share via team_kit.publish), submit_agent upkeep.
Content: tools/upkeep_forecasting_content.py. Slug kept in queue/upkeep-forecasting-slugs.json."""
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from build_wn_business_svg import svg
from upkeep_forecasting_content import DECKS
from agent_links import patch as link_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SL = "queue/upkeep-forecasting-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
for n, key in enumerate(DECKS):
    NAME, ABOUT, PAIRS = DECKS[key]; did = f"upkeep-{key}-deck"
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>
    '''
    acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
    pairs, O, add = kdeck("upfc_", "UpKeep")
    for gi, (g, ask, a, b) in enumerate(PAIRS):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:], acc[(gi + side * 2) % 4])))
        add(g, g, opts[0], opts[1], ask)
    publish(did, NAME, "UpKeep", pairs, {"brands": [ABOUT, "Smart Upkeep forecasting and projection modeling."],
            "submit_agent": "upkeep", "submit_to": "UpKeep Agent", "topic": "upkeep-forecasting",
            "deck_size": 20, "board": "upkeep", "audience": "Max"}, seed=6400 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "upkeep-" + key + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s); link_patch(os.path.join(slug, "index.html"))
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
