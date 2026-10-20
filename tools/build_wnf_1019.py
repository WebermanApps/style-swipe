"""WellNest follow-up decks from Max's Oct 19 2026 results (Max asked 11:57 ICT). Usage: python3 tools/build_wnf_1019.py <outdir>  (from repo root)
Same kit and process as build_wnc_1019.py (team_kit publish, md1018_kit page, standard white deck look, Built by Machan footer, Notes + Share).
20 pairs each, names pass theme_name_ok (no numbers or number words). Results route to Branding (submit_agent branding), picks logged only.
Listed on the wellnest-dashboard shelf like 180c065. Guard: no temple / sacred / cannabis words, no prices or health claims."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import wnf1019 as W
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="wellnest", audience="Max")
DECKS = [
 ("wellnest-powerhaus-can-and-base-tea", "PowerHaus Can And Base Tea", "powerhaus-can-base-tea", W.T_CAN, 1931, "wellnest-powerhaus-pilates-collab-deck",
  "From PowerHaus Pilates Collab results (Reform, Core Reset, Lengthen; Name Only accent; One Line At The Top; With; Typewriter; Clean Label) and notes: base tea first then the best herbs; a can, not a pouch.",
  "base tea per blend, herb pairing per base, can shape and size, finish, lid, label layout, tagline placement"),
 ("wellnest-powerhaus-can-look", "PowerHaus Can Look", "powerhaus-can-look", W.T_LOOK, 1932, "wellnest-powerhaus-collab-look",
  "From PowerHaus Collab Look results: spine, wrap band, arcs, matte white, kraft lid with blue band applied to cans; fresh palettes, name type, co-brand badge and drinkware after his rejections.",
  "winning looks on cans, fresh palettes, name type, co-brand badge, drinkware, range pieces"),
 ("wellnest-tea-theme-blends", "Tea Theme Blends", "tea-theme-blends", W.T_TEA, 1933, "wellnest-chiang-mai-tea-ingredients-deck",
  "From Chiang Mai Tea Ingredients likes and note: 3-4 ingredient matches per theme drawn only from his liked list, each with a base; modest associations, no claims.",
  "nine themes, two blend pairs each, plus base tea picks"),
 ("wellnest-farm-basket-build", "Farm Basket Build", "farm-basket-build", W.T_FARM, 1934, "wellnest-farm-basket-deck",
  "From Farm Basket results (all 30 yes): finished full baskets, sizes, liner and tag combos, note card design.",
  "full baskets, basket and size, liner and tag combos, note card"),
]
REQ = "Oct 19 2026 11:57 ICT: Max asked for fresh follow-up decks from his Oct 19 WellNest results (20 pairs each, routing to Branding, WellNest dashboard shelf)."
BAD = re.compile(r"\b(temples?|wat|spires?|sacred|monks?|cannabis|hemp|weed|marijuana|thc|cbd|ganja|kush)\b|฿|baht|\$|\bTHB\b|organic|certified|detox|cure|heal|boost", re.I)
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); out = {}
    for did, name, slug_base, fn, seed, src, ex, blurb in DECKS:
        if len(sys.argv) > 2 and did not in sys.argv[2:]: continue
        pairs = fn(); n = len(pairs); assert n == 20, (did, n)
        assert theme_name_ok(name) and not re.search(r"\d", name), name
        caption_rule.guard(pairs, did); assert not EMOJI.search(json.dumps(pairs, ensure_ascii=False)), "emoji"
        txt = json.dumps([[p["optionA"]["label"], p["optionA"]["desc"], p["optionB"]["label"], p["optionB"]["desc"], p["ask"]] for p in pairs])
        assert not BAD.search(txt), (did, BAD.search(txt).group(0))
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=src, log_only=True, results_policy="results logged only, never applied", example_data=ex,
                 deck_size=n, no_cap="Max asked for 20 pairs (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding", built_at_note="WellNest follow-ups, Oct 19 2026 11:57 ICT request",
                 brands=["Standard deck look (white, light beige accents, Khand/Hind); WellNest DNA inside the mockups"],
                 sources={"builder": "tools/build_wnf_1019.py", "cards": "tools/wnf1019.py", "draw": "tools/wnf1019_draw.py"})
        publish(did, name, "WellNest", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(did, slug_base); pg = os.path.join(slug, "index.html"); h = open(pg).read()
        if "const D=" not in h:
            h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
            assert '<a class="builtby' in h and "maxweberman.com" in h, "standard footer"
            open(pg, "w").write(h)
        out[did] = {"id": did, "name": name, "url": url, "slug": slug, "total": n, "blurb": f"20 picks: {blurb}", "follows": src}
        print(did, url, n)
    json.dump(out, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
