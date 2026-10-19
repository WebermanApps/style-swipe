"""Scheduling Board Layout Deck, Oct 19 2026 (Max's review relayed via Swatch). Usage: python3 tools/build_sched_1019.py <outdir> (from repo root).
Same kit and process as build_mcd2_1019.py (team_kit publish, md1018_kit page writer, standard white deck look, 'Built by Max Weberman'
footer, Notes + Share). Results route to Branding, picks logged only. PRIVACY: Tech Dash 1-3 / Van 1-3, first names or member IDs only, TEST data."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import sched1019 as C
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
DID, NAME, SLUG = "branding-scheduling-board-layout-deck", "Scheduling Board Layout Deck", "scheduling-board-layout"
REQ = ("Oct 19 2026: Max's review of the UpKeep Scheduling board, relayed by Swatch: two main sections (interactive Schedule with day/week/month, techs, visits and a "
       "TEST fill bar vs the 4-stop cap; Client Communications tracking cards per member, no contact buttons), To-Do in the header, Needs Attention, folded dropdowns, optional cards.")
BAD = re.compile(r"@|\(\d{3}\)|\b\d{5}\b|\blat\b|\blng\b|\bstreet\b|thai|[\u0E00-\u0E7F]", re.I)
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); pairs = C.T_SCHED(); n = len(pairs); assert 18 <= n <= 24, n
    assert theme_name_ok(NAME) and not re.search(r"\d", NAME)
    caption_rule.guard(pairs, DID); blob = json.dumps(pairs, ensure_ascii=False)
    assert not EMOJI.search(blob), "emoji"; assert not BAD.search(blob), BAD.search(blob)
    assert all("TEST" in p[k]["visual"]["svg"] for p in pairs for k in ("optionA", "optionB")), "TEST label"
    order = [p["ask"] for p in pairs]
    m = dict(BR, topic=DID, shelf=True, requested=True, request=REQ, log_only=True, results_policy="results logged only, never applied",
             example_data="Drawn laptop SVG mockups with TEST data only: techs Tech Dash 1-3 and Van 1-3, members by first name or member ID, no contact or address data.",
             deck_size=n, caption_rule="R105", notes=True, built_by="Branding", built_at_note="Scheduling Board review, Oct 19 2026",
             brands=["Standard deck look (white, light beige accents, Khand/Hind)", "Mockups: white/cream base, terracotta, lagoon and jungle accents, light only"],
             sources={"builder": "tools/build_sched_1019.py", "cards": "tools/sched1019.py"})
    publish(DID, NAME, "UpKeep", pairs, m, seed=1921, n=n, first=0)
    dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == n
    dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
    for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
    dj.pop("owner", None); json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    slug, url = page(DID, SLUG); pg = os.path.join(slug, "index.html"); h = open(pg).read()
    if "const D=" not in h:
        h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
        assert '<a class="builtby' in h and "maxweberman.com" in h, "standard footer"
        open(pg, "w").write(h)
    json.dump({"id": DID, "name": NAME, "url": url, "slug": slug, "total": n, "titles": order}, open(os.path.join(outdir, "built.json"), "w"), indent=1)
    print(DID, url, n)
