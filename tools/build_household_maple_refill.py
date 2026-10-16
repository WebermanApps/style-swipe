#!/usr/bin/env python3
"""Household: refill Maple Deck after Max's Oct 15 submission (6aa9b781). Maple is 8 months (Max note on card 01).
20 pairs: skipped cards 10 and 15 reworded for a baby and asked first (R64), then 18 from Branding's baby bank
(household_content.py maple-outings / maple-learning, style-swipe 6575172). Same card + page pattern as build_household.py."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from build_wn_business_svg import svg
from household_content import DECKS, P
from agent_links import patch as link_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
did = "household-maple-baby-deck"; NAME = "Maple Deck"
CARRIED = [  # (from id, pair)
 ("household-maple-deck-10", P("Learning", "Calm Indoor Outing: Art Gallery Stroll In The Carrier Or Museum Baby Corner?",
   "Gallery Stroll In Carrier", "Quiet rooms, bright colours, Maple on a parent.", "Cool indoors", "Short visit",
   "Museum Baby Corner", "Soft mats and baby-safe toys to touch.", "Hands-on", "Air-conditioned")),
 ("household-maple-deck-15", P("Hands", "Shapes For Baby: Soft Shape Sorter Or Stacking Rings?",
   "Soft Shape Sorter", "Big fabric shapes to hold and drop in.", "Grasping", "Safe to mouth",
   "Stacking Rings", "Chunky rings on a wobble base.", "Hand-eye", "Sizes and colours")),
]
mo, ml = DECKS["maple-outings"][2], DECKS["maple-learning"][2]
FRESH = [mo[i] for i in (0, 1, 2, 3, 6, 8, 10, 12, 14)] + [ml[i] for i in (0, 1, 2, 3, 4, 6, 7, 11, 13)]
FEEL = ["practical", "bold", "calm", "playful", "premium"]; acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
pairs, O, add = kdeck("hhmbaby_", "Household")
ALL = [c[1] for c in CARRIED] + FRESH; assert len(ALL) == 20
for gi, (g, ask, a, b) in enumerate(ALL):
    opts = []
    for side, o in enumerate((a, b)):
        oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
        opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:], acc[(gi + side * 2) % 4])))
    add(g, g, opts[0], opts[1], ask, purpose="retest" if gi < len(CARRIED) else "new")
for i, (src, _) in enumerate(CARRIED): pairs[i]["carried_from"] = src; pairs[i]["retest"] = True
publish(did, NAME, "Household", pairs, {"brands": [DECKS["maple"][1], "Household help for Max, Nozomi and Maple. No dashboard layout topics."],
        "submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d",
        "deck_size": 20, "board": "household", "audience": "Max and Nozomi", "topic": "household-maple", "carried": len(CARRIED),
        "replaces": "household-maple-deck"}, seed=5307, n=20, first=len(CARRIED))
dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
SL = "queue/household-slugs.json"; slugs = json.load(open(SL))
if did not in slugs: slugs[did] = "household-maple-baby-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>
    '''
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s); link_patch(os.path.join(slug, "index.html"))
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": did, "slug": slug, "pairs": len(dj["pairs"]), "first": [p["ask"] for p in dj["pairs"][:2]], "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
