"""Home page hero deck, Oct 18 2026 (requested 20:49 ICT): Home Page: Hero Headline And Layout. Usage: python3 tools/build_hero_1018.py
Same kit as build_tagline_1018.py (md1018_kit.ship). Writes /workspace/wt/hero-deck-1018/built.json.
Mockups only: the live home page stays locked and unchanged; picks are logged only."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import hero1018 as HR
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
REQ = "Oct 18 2026 20:49 ICT: swipe deck to fix the phone home page hero (headline order, alignment, size, picture order, check line, button, second quote link, trust pills, spacing, full hero); first in line on the board; mockups only, home page locked, picks logged only"
DID, NAME, SLUG = "upkeep-home-page-hero-headline-and-layout-deck", "Home Page: Hero Headline And Layout", "home-hero-headline-layout"
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]", re.I)
pairs = HR.T_HERO()
txt = json.dumps(pairs, ensure_ascii=False)
assert not BAD.search(txt.replace("max-width", "").replace("max-height", "")), BAD.search(txt)
m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, log_only=True,
         example_data="Every card is a drawn mockup of the phone hero using the site's real header, illustration and colours; the live page is not changed.")
r = ship(DID, NAME, "UpKeep", pairs, m, seed=6182, slug_base=SLUG, upkeep=True)
dj = json.load(open(f"decks/{DID}.json"))
dj["meta"] = dj.get("meta", {}) if isinstance(dj.get("meta"), dict) else {}
for k in ("built_at_note", "sources"):
    if k in dj: dj[k] = {"built_at_note": "Home page hero deck Oct 18 2026 20:49 ICT request", "sources": {"builder": "tools/build_hero_1018.py"}}[k]
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
outp = "/workspace/wt/hero-deck-1018/built.json"
json.dump({DID: r}, open(outp, "w"), indent=1, ensure_ascii=False)
print(DID, r["url"], len(r["titles"]))
# Keep the deck free of personal identity: drop the owner field (viewer falls back anyway), the empty meta and the
# personal 'built by' footer link; give the page (and its lock gate) the deck's own title. Only this deck's files change.
dj = json.load(open(f"decks/{DID}.json")); dj.pop("owner", None)
if dj.get("meta") == {}: dj.pop("meta")
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
if "const D=" not in h:
    h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
    h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
    open(pg, "w").write(h)
