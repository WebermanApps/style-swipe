"""Machan and End Screen follow-up decks, Oct 19 2026 (Max: 'remake any deck that was swiped on'; Oct 18 Branding results never acted on).
Usage: python3 tools/build_mfu_1019.py <outdir>   (from the repo root)
Same kit and process as build_wnf_1019.py / build_machan_1018.py: team_kit publish, md1018_kit page, template footer link, Notes + Share.
Machan decks keep the light cream page (build_machan_1018 finish_page); End Screen keeps the standard white page.
20 pairs each; names pass theme_name_ok (no numbers or number words). Results route to Branding, picks logged only. Off UpKeep."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import mfu1019 as F
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
REQ = "Oct 19 2026 12:05 ICT: Max asked to 'remake any deck that was swiped on'; follow-up from his Oct 18 results that were never acted on."
DECKS = [
 ("machan-look-refinements", "Machan Look Refinements", "machan-look-refinements", F.T_LOOK, 7411, True, "machan-look-and-personality-deck", "2026-10-18T22:54:56+07:00",
  "Drawn mockups of the v3 wink mark: refines his picks (two leaves, wink, blush, flat terracotta, no tagline, leaf divider, sapling) and settles wink at rest vs wink on hover."),
 ("machan-origin-story-refinements", "Machan Origin Story Refinements", "machan-origin-story-refinements", F.T_STORY, 7412, True, "machan-origin-story-deck", "2026-10-18T22:57:57+07:00",
  "Mini story-card mockups using only the five lore pieces; refines his picks and retries what he liked both ways or passed on (new tiger lines, Nagasaki treatments, opening order)."),
 ("end-screen-refinements", "End Screen Refinements", "end-screen-refinements", F.T_END, 7413, False, "variety-swipe-controls-deck-end-screen", "2026-10-18T22:14:27+07:00",
  "Drawn phone mockups of the deck end screen: head-to-heads between his bottom-placement winners plus density, corners, buttons, copy and summary."),
]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); out = {}
    for did, name, slug_base, fn, seed, cream, src, src_at, ex in DECKS:
        pairs = fn(); n = len(pairs); assert n == 20, (did, n)
        assert theme_name_ok(name) and not re.search(r"\d", name), name
        caption_rule.guard(pairs, did); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob), "emoji"; assert not re.search(r"upkeep|weberman|[\u0E00-\u0E7F]", blob, re.I), "Machan/Branding decks stay off UpKeep and never name Max"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=src, follows_submitted_at=src_at, log_only=True, results_policy="results logged only, never applied",
                 example_data=ex, deck_size=n, no_cap="Max asked for 20 pairs (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 built_at_note="Machan and End Screen follow-ups, Oct 19 2026 12:05 ICT request",
                 sources={"results": f"/workspace/ops/submit/inbox/branding/ ({src})", "builder": "tools/build_mfu_1019.py", "cards": "tools/mfu1019.py",
                          "mark": "Machan mark v3 (wink) from /workspace/machan/story-carousel/index.html via tools/machan1018.py"})
        publish(did, name, "Branding", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(did, slug_base); pg = os.path.join(slug, "index.html"); h = open(pg).read()
        if "const D=" not in h:
            h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
            if cream: h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
            assert '<a class="builtby' in h, "standard footer"
            open(pg, "w").write(h)
        out[did] = {"id": did, "name": name, "url": url, "slug": slug, "total": n, "follows": src, "follows_at": src_at}
        print(did, url, n)
    json.dump(out, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
