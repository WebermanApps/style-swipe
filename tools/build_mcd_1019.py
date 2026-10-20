"""Member Catalog Deck, Oct 19 2026 (Max asked directly 11:29 ICT). Usage: python3 tools/build_mcd_1019.py <outdir>   (from the repo root)
Same kit and process as build_wnc_1019.py (team_kit publish, md1018_kit page writer, standard white deck look, 'Built by Machan'
footer, Notes + Share). 20 this-or-that pairs (no 10-pick cap: Max asked for 20). Results route to Branding (Swatch), picks logged only.
Listed on the Branding board's Max's Picks (requested flow), not on any UpKeep board (Max, Oct 19 11:31 ICT: no swipe decks on UpKeep boards for now).
PRIVACY: invented sample members only (no ops-private data); guard below fails the build on real-address markers or Thai references."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import mcd1019 as C
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
DID, NAME, SLUG = "branding-member-catalog-deck", "Member Catalog Deck", "member-catalog"
REQ = ("Oct 19 2026 11:29 ICT: Max asked directly for a 20-card this-or-that deck to design the Members section of the UpKeep Members Command Center: "
       "an easy catalog of every Smart Upkeep member, organized into name and contact info, home info and membership info. Laptop-first, phone must work.")
BAD = re.compile(r"wickfield|2573|thai|thailand|[\u0E00-\u0E7F]", re.I)
if __name__ == "__main__":
    outdir = sys.argv[1]; pairs = C.T_MEMBERS(); n = len(pairs); assert n == 20
    assert theme_name_ok(NAME) and not re.search(r"\d", NAME)
    caption_rule.guard(pairs, DID); blob = json.dumps(pairs, ensure_ascii=False)
    assert not EMOJI.search(blob), "emoji"; assert not BAD.search(blob), BAD.search(blob)
    assert all("SAMPLE" in p[k]["visual"]["svg"] for p in pairs for k in ("optionA", "optionB")), "Sample label"
    order = [p["ask"] for p in pairs]
    m = dict(BR, topic=DID, shelf=True, requested=True, request=REQ, log_only=True, results_policy="results logged only, never applied",
             example_data="Drawn laptop SVG mockups with invented sample members only: fake names, (555) 000-01xx phones, @example.test emails, Sample St style streets, metro Detroit cities. Tagged SAMPLE.",
             deck_size=n, no_cap="Max asked for 20 cards (Oct 19 2026 11:29 ICT)", caption_rule="R105", notes=True, built_by="Branding",
             built_at_note="Member Catalog Deck, Oct 19 2026 11:29 ICT request",
             brands=["Standard deck look (white, light beige accents, Khand/Hind)", "Mockups: white/cream base, terracotta, lagoon and jungle accents, light only"],
             sources={"builder": "tools/build_mcd_1019.py", "cards": "tools/mcd1019.py"})
    publish(DID, NAME, "UpKeep", pairs, m, seed=1919, n=n, first=0)
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
