#!/usr/bin/env python3
"""Household agent (c59ffdde-28bf-4ad7-8dd8-22f5e941647d) first deck 'Home Setup Deck' (Oct 15 2026): 20 pairs for Max, Nozomi and Maple.
Same card + page pattern as build_wn_business.py (white, beige accents, Khand/Hind, Notes + Share via team_kit.publish), submit_agent household.
Content: tools/household_content.py. Slug kept in queue/household-slugs.json."""
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from build_wn_business_svg import svg
from household_content import NAME, ABOUT, PAIRS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SL = "queue/household-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
FEEL = ["practical", "bold", "calm", "playful", "premium"]
did = "household-home-setup-deck"
HEAD = f'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="{did}"</script>
<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>
'''
acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
pairs, O, add = kdeck("hh_", "Household")
for gi, (g, ask, a, b) in enumerate(PAIRS):
    opts = []
    for side, o in enumerate((a, b)):
        oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
        opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:], acc[(gi + side * 2) % 4])))
    add(g, g, opts[0], opts[1], ask)
publish(did, NAME, "Household", pairs, {"brands": [ABOUT, "Household help for Max, Nozomi and Maple. No dashboard layout topics."],
        "submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d",
        "deck_size": 20, "board": "household", "audience": "Max and Nozomi"}, seed=5200, n=20)
dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
if did not in slugs: slugs[did] = "household-home-setup-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": did, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
