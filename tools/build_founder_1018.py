"""Investor pitch founder slide deck, Oct 18 2026 night (Branding; Max asked directly 22:33 ICT): Pitch: Built By A Builder Founder Slide.
Usage: python3 tools/build_founder_1018.py <outdir>   (from the repo root)
Follows build_fu2045_1018.py / build_pitchv3_1018.py (md1018_kit.ship; drops owner/meta, the personal built-by footer link, and
titles the page after the deck) plus the cream page background used by build_machan_1018.py. Picks are logged only, never applied."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import founder1018 as F
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]|finance and accounting", re.I)
POL = "results logged only, never applied"
DID, NAME, SLUG, SEED = "upkeep-investor-pitch-built-by-a-builder-founder-slide-deck", "Pitch: Built By A Builder Founder Slide", "pitch-built-by-builder-founder", 6211
REQ = ("Oct 18 2026 22:33 ICT, asked directly: swipe deck on the investor pitch founder slide 'Built By A Builder' (pitch-deck slide 9, upkeep-cc bb2e154): "
       "which new verified fact earns a tile (rental property, remote US operations, multiple small businesses), cut Multiple languages or not, lead line, "
       "4 vs 6 tiles, timeline, tone, credential banner placement, and whether to add a real home count (Notes asks for the number)")
EX = ("Every card is a drawn mockup of the live founder slide or its tiles; founder unnamed, no photo; the background tile reads "
      "'Economics and accounting' (corrected); only verified facts; 'XX homes' is a SAMPLE placeholder, no numbers invented.")
NOTE_JS = ("<script>/* Home count card: Notes asks for the real number (this page only) */addEventListener('DOMContentLoaded',()=>{const s=document.getElementById('noteSheet'),"
           "x=document.getElementById('noteText'),u=document.getElementById('noteSub');if(!s||!x||!u)return;const d=x.placeholder;new MutationObserver(()=>{if(!s.classList.contains('on'))return;"
           "x.placeholder=/Count of homes/i.test(u.textContent)?'How many homes have you built or managed? The real number replaces XX.':d}).observe(s,{attributes:true,attributeFilter:['class']})})</script>")
pairs = F.T_FOUNDER_SLIDE()
txt = json.dumps(pairs, ensure_ascii=False).replace("max-width", "").replace("max-height", "").replace("AI agent training", "")
assert not BAD.search(txt), BAD.search(txt)
assert ">Economics and<" in txt and " ".join(F.TIL["econ"][0]) == "Economics and accounting"
m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, results_policy=POL, example_data=EX,
         notes_prompt={"pick": 10, "ask": "How many homes have you built or managed? The real number replaces the SAMPLE XX."})
r = ship(DID, NAME, "UpKeep", pairs, m, seed=SEED, slug_base=SLUG, upkeep=True)
dj = json.load(open(f"decks/{DID}.json"))
dj["built_at_note"] = "Founder slide deck, Oct 18 2026 22:33 ICT request"
dj["sources"] = {"slide": "upkeep-cc bb2e154 pitch-deck/index.html slide 9", "builder": "tools/build_founder_1018.py"}
dj.pop("owner", None)
if dj.get("meta") == {}: dj.pop("meta")
dj["pairs"][9]["note_prompt"] = "How many homes have you built or managed? The real number replaces the SAMPLE XX."
json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
assert not BAD.search(json.dumps(dj, ensure_ascii=False).replace("max-width", "").replace("max-height", "").replace("max_pairs", "").replace("AI agent training", "")), "deck json"
pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
assert "const D=" not in h
h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
old = "<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}"
assert old in h; h = h.replace(old, "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
h = h.replace("</body>", NOTE_JS + "\n</body>", 1)
assert "maxweberman.com" not in h and "Built by Machan" not in h and "Max Weberman</title>" not in h, "visible footer/title names"
open(pg, "w").write(h)
r["shelf_blurb"] = "10 cards: which new fact earns a tile, languages swap, lead line, 4 vs 6 tiles, timeline, tone, banner, home count"
json.dump({DID: r}, open(os.path.join(sys.argv[1], "built.json"), "w"), indent=1, ensure_ascii=False)
print(DID, r["url"], len(r["titles"]))
