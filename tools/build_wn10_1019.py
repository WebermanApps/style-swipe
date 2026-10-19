"""WellNest ten-pair follow-up decks, Oct 19 2026 16:13 ICT (Swatch, from Max's Oct 19 WellNest results; one level past this morning's PowerHaus Can And Base Tea,
PowerHaus Can Look, Tea Theme Blends and Farm Basket Build, none of their pairs repeated). Usage: python3 tools/build_wn10_1019.py <outdir>  (repo root)
Same kit as build_fu10_1019.py; results route to WellNest (submit_agent wellnest), picks logged only; listed at the top of the wellnest-dashboard shelf.
Guards: no rose (Max passed on Highland Rose), osmanthus / orange peel marked New, no temple / cannabis / hemp words, no health claims or prices."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import wn10_1019 as F
BR = dict(submit_agent="wellnest", submit_to="WellNest Agent", board="wellnest", audience="Max")
BAD = re.compile(r"\b(temples?|wat|spires?|sacred|monks?|cannabis|hemp|weed|marijuana|thc|cbd|ganja|kush|rose|roses|turmeric|galangal|pandan|lotus|lychee)\b|฿|baht|\$|\bTHB\b|organic|certified|detox|cure|heal|boost", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
INBOX = "/workspace/ops/submit/inbox/wellnest/"
REQ = "Oct 19 2026 16:10 ICT: Max asked 'prepare fresh new decks on the same topics i swiped on. they don't have to be as long. i like 10 at a time.' WellNest topics, base tea first then 3-4 herbs per theme, a can not a pouch."
WX = "Drawn WellNest mockups tagged MOCKUP; gentle theme words only. PowerHaus keeps its own royal blue spine, arcs and slim can, clearly apart from the Roselle line."
DECKS = [
 ("wellnest-theme-blend-can-labels", "Theme Blend Can Labels", "theme-blend-can-labels", F.T_CANS, "WellNest", False, 3201, ["wellnest-chiang-mai-tea-ingredients-deck-20261019-0612-ccf28bc8.json"], WX + " Builds on Tea Theme Blends (tea-theme-blends-w22shy)."),
 ("wellnest-base-tea-taste-pairings", "Base Tea Taste Pairings", "base-tea-taste-pairings", F.T_BASE, "WellNest", False, 3202, ["wellnest-chiang-mai-tea-ingredients-deck-20261019-0612-ccf28bc8.json", "wellnest-powerhaus-pilates-collab-deck-20261019-0610-f781d0b4.json"], WX + " Builds on PowerHaus Can And Base Tea (powerhaus-can-base-tea-8uidjl); osmanthus and orange peel marked New."),
 ("wellnest-powerhaus-pilates-studio-display", "PowerHaus Pilates Studio Display", "powerhaus-pilates-studio-display", F.T_STUDIO, "WellNest", False, 3203, ["wellnest-powerhaus-collab-look-20261019-1045-19577d92.json", "wellnest-powerhaus-pilates-collab-deck-20261019-0610-f781d0b4.json"], WX + " Opens with the can vs box pouch decider. Builds on PowerHaus Can Look (powerhaus-can-look-vxfe7g)."),
 ("wellnest-farm-basket-gift-presentation", "Farm Basket Gift Presentation", "farm-basket-gift-presentation", F.T_GIFT, "WellNest", False, 3204, ["wellnest-farm-basket-deck-20261019-0548-73718603.json"], WX + " Builds on Farm Basket Build (farm-basket-build-nh5qv8)."),
]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); only = set(sys.argv[2:]); built = []
    for did, name, slug_base, fn, app, cream, seed, srcs, ex in DECKS:
        if only and did not in only: continue
        pairs = fn(); n = len(pairs); assert n == 10, (did, n)
        assert theme_name_ok(name) and not NUMW.search(name), name
        caption_rule.guard(pairs, did); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob.replace("事事如意", "")), "emoji"; assert not BAD.search(blob), (did, BAD.search(blob))
        if app == "UpKeep--": assert all(("SAMPLE" in p[k]["visual"]["svg"] or "TEST" in p[k]["visual"]["svg"]) for p in pairs for k in ("optionA", "optionB")), "sample label"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=[s.rsplit("-2026", 1)[0] for s in srcs], log_only=True, results_policy="results logged only, never applied",
                 example_data=ex, deck_size=n, no_cap="Max asked for 10 at a time (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding", brands=["Standard deck look (white, light beige accents, Khand/Hind); WellNest DNA inside the mockups"],
                 built_at_note="Ten-pair follow-ups, Oct 19 2026 16:10 ICT request",
                 sources={"results": [INBOX + s for s in srcs], "builder": "tools/build_wn10_1019.py", "cards": "tools/wn10_1019.py", "draw": "tools/wnf1019_draw.py"})
        publish(did, name, app, pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(did, slug_base); pg = os.path.join(slug, "index.html"); h = open(pg).read()
        if "const D=" not in h:
            h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
            if cream: h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
            i = h.index('<a class="builtby'); j = h.index("</a>", i); a_ = h[i:j]
            assert 'href="https://maxweberman.com"' in a_, "builtby link"
            h = h[:i] + a_.replace("Built by Machan", "Built by Max Weberman") + h[j:]
            assert "Built by Max Weberman" in h[i:i + len(a_) + 20]
            open(pg, "w").write(h)
        built.append({"id": did, "name": name, "url": url, "slug": slug, "total": n, "titles": order,
                      "labels": [f"{p['optionA']['label']} vs {p['optionB']['label']}" for p in dj["pairs"]]}); print(did, url, n)
    json.dump(built, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
