"""Investor pitch decks v3, Oct 18 2026: Founder Hype And Layout + Timeline Refresh. Usage: python3 tools/build_pitchv3_1018.py <outdir>
Mirrors build_tagline_1018.py (md1018_kit.ship; drops owner/meta, the personal built-by footer link, and titles the page after the deck)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import pitchv3_1018 as PV
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]", re.I)
DECKS = [("upkeep-investor-pitch-founder-hype-and-layout-deck", "Investor Pitch: Founder Hype And Layout", "pitch-founder-hype-layout", PV.T_FOUNDER, 6191,
          "Oct 18 2026 evening: new pitch deck, how to present the anonymous founder (layout, headline, lead fact, tone, icons, format)", "Founder slides are drawn mockups; founder unnamed, no photo."),
         ("upkeep-investor-pitch-timeline-refresh-deck", "Investor Pitch: Timeline Refresh", "pitch-timeline-refresh", PV.T_TIMELINE, 6192,
          "Oct 18 2026 evening: new pitch deck, fresh ways to show the launch timeline; forecasts labelled", "Timeline slides are drawn mockups; Beta and growth figures are Forecast/Expected.")]
out = {}
for DID, NAME, SLUG, fn, seed, REQ, EX in DECKS:
    pairs = fn(); txt = json.dumps(pairs, ensure_ascii=False).replace("max-width", "").replace("max-height", "").replace("AI agent trainer", "")
    assert not BAD.search(txt), BAD.search(txt)
    m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, example_data=EX)
    r = ship(DID, NAME, "UpKeep", pairs, m, seed=seed, slug_base=SLUG, upkeep=True)
    dj = json.load(open(f"decks/{DID}.json"))
    dj["meta"] = dj.get("meta", {}) if isinstance(dj.get("meta"), dict) else {}
    for k in ("built_at_note", "sources"):
        if k in dj: dj[k] = {"built_at_note": "Investor pitch decks v3, Oct 18 2026", "sources": {"builder": "tools/build_pitchv3_1018.py"}}[k]
    dj.pop("owner", None)
    if dj.get("meta") == {}: dj.pop("meta")
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
    if "const D=" not in h:
        h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
        h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
        open(pg, "w").write(h)
    out[DID] = r; print(DID, r["url"], len(r["titles"]))
json.dump(out, open(os.path.join(sys.argv[1], "built.json"), "w"), indent=1, ensure_ascii=False)
