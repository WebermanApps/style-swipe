"""Tech graphics decks, Oct 18 2026 (asked 22:30 ICT: "i want decks for the graphics of the technicians").
Usage: python3 tools/build_techgfx_1018.py <outdir>   (from the repo root)
Follows build_fu2045_1018.py / build_pitchv3_1018.py (md1018_kit.ship; drops owner/meta, the personal built-by footer link, and
titles the page after the deck). Light cream page like the art. UpKeep board. Results are logged only, never applied."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import techgfx1018 as TG
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]", re.I)
POL = "results logged only, never applied"
REQ = ("Oct 18 2026 22:30 ICT: decks for the graphics of the technicians (how techs are illustrated in the investor pitch and brand graphics, "
       "not the tech app); drawn SVG mockups only; fixed picks from the earlier uniform decks drawn in, not re-asked")
FIXED = ("Drawn in, not asked: illustrated people only; healthy, fit young adults with varied builds; left-chest logo, big back wordmark, "
         "printed first name, white cap with front mark, long charcoal pants, plain black belt, sneakers for good weather and boots for bad weather, "
         "terracotta reusable logo shoe covers always visible, charcoal softshell for cold days.")
DECKS = [("upkeep-tech-graphics-illustration-style-deck", "Tech Graphics: Illustration Style", "tech-graphics-illustration-style", TG.T_STYLE, 6311,
          "Oct 18 2026 22:30 ICT request: drawing approach for the illustrated techs (shading, outline, crop, proportions, faces, hero vs pair, pose, backdrop, set variety, line weight)"),
         ("upkeep-tech-graphics-uniform-and-gear-details-deck", "Tech Graphics: Uniform And Gear Details", "tech-graphics-uniform-gear-details", TG.T_GEAR, 6312,
          "Oct 18 2026 22:30 ICT request: uniform and gear details in tech graphics (back wordmark view, name, belt gear, tablet, cover inset, cap, sleeves, callouts, softshell layer, van)")]
out = {}
for DID, NAME, SLUG, fn, seed, NOTE in DECKS:
    pairs = fn(); txt = json.dumps(pairs, ensure_ascii=False).replace("max-width", "").replace("max-height", "")
    assert not BAD.search(txt), (DID, BAD.search(txt))
    m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, note=NOTE, fixed_picks=FIXED, results_policy=POL, log_only=True,
             follows="upkeep-employee-attire-deck",
             example_data="Every card is a hand-built SVG mockup of an illustrated tech (round-2 pitch figure style); sample first name only; nothing live is changed.")
    r = ship(DID, NAME, "UpKeep", pairs, m, seed=seed, slug_base=SLUG, upkeep=True)
    dj = json.load(open(f"decks/{DID}.json"))
    dj["built_at_note"] = "Tech graphics decks Oct 18 2026 22:30 ICT request"
    dj["sources"] = {"figures": "pitch-v3-1018 round 2 figs.py (illustrated techs)", "picks": "upkeep-employee-attire, work-polo-and-layers, crew-uniform-new-options results",
                     "builder": "tools/build_techgfx_1018.py"}
    dj.pop("owner", None)
    if dj.get("meta") == {}: dj.pop("meta")
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    assert not BAD.search(json.dumps(dj, ensure_ascii=False).replace("max-width", "").replace("max-height", "").replace("max_pairs", "")), (DID, "deck json")
    pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
    if "const D=" not in h:
        h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
        h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
        h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
        open(pg, "w").write(h)
    out[DID] = r; print(DID, r["url"], len(r["titles"]))
json.dump(out, open(os.path.join(sys.argv[1], "built.json"), "w"), indent=1, ensure_ascii=False)
