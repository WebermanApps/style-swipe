"""Tagline deck, Oct 18 2026 (requested 18:23 ICT): Tagline: Home Maintenance Membership. Usage: python3 tools/build_tagline_1018.py
Same kit as build_fu1018.py / build_pin4_1018.py (md1018_kit.ship). Writes /workspace/wt/tagline-1018/built.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import tagline1018 as TG
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
REQ = "Oct 18 2026 18:23 ICT: new swipe deck for the company tagline; Home Maintenance Membership as subheadline or headline; queue it if the board is full"
DID, NAME, SLUG = "upkeep-tagline-home-maintenance-membership-deck", "Tagline: Home Maintenance Membership", "tagline-home-maintenance-membership"
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]", re.I)
pairs = TG.T_TAGLINE()
txt = json.dumps(pairs, ensure_ascii=False)
assert not BAD.search(txt.replace("max-width", "").replace("max-height", "")), BAD.search(txt)
m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, example_data="In-context screens are drawn mockups; contact details are placeholders.")
r = ship(DID, NAME, "UpKeep", pairs, m, seed=6181, slug_base=SLUG, upkeep=True)
dj = json.load(open(f"decks/{DID}.json"))
dj["meta"] = dj.get("meta", {}) if isinstance(dj.get("meta"), dict) else {}
for k in ("built_at_note", "sources"):
    if k in dj: dj[k] = {"built_at_note": "Tagline deck Oct 18 2026 18:23 ICT request", "sources": {"builder": "tools/build_tagline_1018.py"}}[k]
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
outp = "/workspace/wt/tagline-1018/built.json"
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
