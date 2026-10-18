"""Machan decks, Oct 18 2026 (Max asked 22:04 ICT: "lets do a few swipes on machan and the origin story", "make 2 of them please").
Usage: python3 tools/build_machan_1018.py   (from the repo root). Same kit as build_hero_1018.py (md1018_kit.ship).
Writes /workspace/wt/machan-decks-1018/built.json. Machan is Max's personal mascot (not UpKeep): results go to Branding and
the decks sit on the Branding board (Max's Picks). Picks are logged only, never implemented automatically."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import machan1018 as MC
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
REQ = "Oct 18 2026 22:04 ICT: Max asked for a few swipes on Machan and the origin story, two decks; mockups only, picks logged only"
DECKS = [
    ("machan-look-and-personality-deck", "Machan: Look And Personality", "machan-look-personality", MC.T_LOOK, 7311,
     "Every card is a drawn mockup of the v3 wink mark (persimmon) at large size and in the real-size Built by Machan footer; nothing live is changed."),
    ("machan-origin-story-deck", "Machan: Origin Story", "machan-origin-story", MC.T_STORY, 7312,
     "Every card is a mini card mockup of the actual Machan story text (brand-story.md and the story carousel); only the five real pieces of lore, no new facts."),
]
UPKEEP = re.compile(r"upkeep|smart upkeep", re.I)
out = {}
for did, name, slug, fn, seed, ex in DECKS:
    pairs = fn()
    assert not UPKEEP.search(json.dumps(pairs, ensure_ascii=False)), "Machan decks stay off UpKeep"
    m = dict(BR, topic=did, requested=True, request=REQ, log_only=True, brands=["Machan (Max's personal mascot, persimmon, v3 wink mark)"], example_data=ex)
    r = ship(did, name, "Branding", pairs, m, seed=seed, slug_base=slug)
    dj = json.load(open(f"decks/{did}.json"))
    dj["built_at_note"] = "Machan decks Oct 18 2026 22:04 ICT request"
    dj["sources"] = {"story": "/workspace/machan/brand-story.md", "carousel": "/workspace/machan/story-carousel/index.html",
                     "mark": "assets/machan-mark-v3-wink.svg (pitch-v3-1018)", "builder": "tools/build_machan_1018.py"}
    json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    # Same page finish as tonight's decks: the deck's own title, no 'built by' footer link (Share stays at the bottom),
    # plus the light cream page background Max asked for. Only this deck's page changes.
    pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
    if "const D=" not in h:
        h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
        h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
        h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
        open(pg, "w").write(h)
    out[did] = r; print(did, r["url"], len(r["titles"]))
json.dump(out, open("/workspace/wt/machan-decks-1018/built.json", "w"), indent=1, ensure_ascii=False)
