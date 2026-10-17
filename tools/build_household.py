#!/usr/bin/env python3
"""Household agent (c59ffdde-28bf-4ad7-8dd8-22f5e941647d) first deck 'Home Setup Deck' (Oct 15 2026): 20 pairs for Max, Nozomi and Maple.
Same card + page pattern as build_wn_business.py (white, beige accents, Khand/Hind, Notes + Share via team_kit.publish), submit_agent household.
Content: tools/household_content.py. Slug kept in queue/household-slugs.json."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import sys, os, json, re, string, secrets
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from build_wn_business_svg import svg
from household_content import DECKS
from household_fresh_content import FRESH, ART_KEY, ART_NAME, ART_PAIRS  # fresh round, Oct 16 2026
DECKS = {**DECKS, **FRESH}
LETTERS = string.ascii_lowercase
CC11 = '<script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc12" data-agent-id="c59ffdde-28bf-4ad7-8dd8-22f5e941647d" data-agent-name="Household" defer></script>'
def page(did, slug):
    HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>\n'
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    s = re.sub(r'<script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js\?v=cc\d+"[^>]*></script>', CC11, s)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s); link_patch(os.path.join(slug, "index.html"))
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
def build_art():
    from build_art_deck import fetch, svg as art_svg
    did = f"household-{ART_KEY}-deck"; pairs, O, add = kdeck("hhgal_", "Household"); FEEL5 = ["classic", "bold", "calm", "playful", "premium"]
    for gi, (g, ask, ia, la, ib, lb) in enumerate(ART_PAIRS):
        opts = []
        for side, (aid, lab) in enumerate(((ia, la), (ib, lb))):
            c = fetch(aid); desc = f'{c["artist"] or "Unknown"}, {c["date"]}. {c["medium"] or ""}'.strip()
            o = O(f"aic{aid}", lab, desc[:120], FEEL5[(gi + side) % 5], art_svg(c, lab), tags=["art", g.lower()])
            o["credit"] = {k: c[k] for k in ("title", "artist", "date", "license", "source")}; opts.append(o)
        add(g, g, opts[0], opts[1], ask)
    publish(did, ART_NAME, "Household", pairs, {"brands": ["Permanent deck of real public-domain artworks across painting, photography, sculpture, prints, ceramics, design and textiles", "Images: Art Institute of Chicago Open Access (CC0), stored in img/art/; credits in img/art/credits.json"],
            "submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d",
            "deck_size": 20, "board": "household", "permanent": True, "audience": "Max and Nozomi", "replaces": "household-art-deck"}, seed=5400, n=20)
    assert len(json.load(open(f"decks/{did}.json"))["pairs"]) == 20
    if did not in slugs: slugs[did] = "household-" + ART_KEY + "-" + "".join(secrets.choice(LETTERS) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    page(did, slugs[did]); print(json.dumps({"deckId": did, "name": ART_NAME, "slug": slugs[did], "url": f"https://webermanapps.github.io/style-swipe/{slugs[did]}/"}))
from agent_links import patch as link_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SL = "queue/household-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
REPL = {"home-routines": "household-home-setup-deck", "chiang-mai-dates": "household-date-night-deck", "trips-near-far": "household-travel-deck", "maple-play-days": "household-maple-baby-deck"}
if ART_KEY in sys.argv[1:]: build_art()
FEEL = ["practical", "bold", "calm", "playful", "premium"]
for n, key in enumerate(DECKS):
    if sys.argv[1:] and key not in sys.argv[1:]: continue
    NAME, ABOUT, PAIRS = DECKS[key]; did = f"household-{key}-deck"
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>
    '''
    acc = [TERRA, LAGOON, JUNGLE, SAFFRON]
    pairs, O, add = kdeck("hh_" if key == "home-setup" else "hh" + re.sub("[^a-z]", "", key)[:8] + "_", "Household")
    for gi, (g, ask, a, b) in enumerate(PAIRS):
        opts = []
        for side, o in enumerate((a, b)):
            oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
            opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:], acc[(gi + side * 2) % 4])))
        add(g, g, opts[0], opts[1], ask)
    publish(did, NAME, "Household", pairs, {"brands": [ABOUT, "Household help for Max, Nozomi and Maple. No dashboard layout topics."],
            "submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d",
            "deck_size": 20, "board": "household", "audience": "Max and Nozomi", **({"replaces": REPL[key]} if key in REPL else {})}, seed=5200 + n, n=20)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 20, len(dj["pairs"])
    if did not in slugs: slugs[did] = "household-" + key + "-" + "".join(secrets.choice(LETTERS if key in FRESH else string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    if key in FRESH: page(did, slugs[did]); print(json.dumps({"deckId": did, "name": NAME, "slug": slugs[did], "url": f"https://webermanapps.github.io/style-swipe/{slugs[did]}/"})); continue
    slug = slugs[did]; s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s); link_patch(os.path.join(slug, "index.html"))
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
