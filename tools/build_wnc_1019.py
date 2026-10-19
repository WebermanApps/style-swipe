"""WellNest collab look decks, Oct 19 2026 (Max asked directly 9:37 ICT: more PowerHaus and Buds Station decks with new designs that keep the
WellNest brand but differ more from the Roselle line). Usage: python3 tools/build_wnc_1019.py <outdir>   (from the repo root)
Same kit and house process as build_wnc_1018.py (md1018_kit page writer, team_kit publish, standard footer, Both/Love/Neither, Notes + Share),
but on Max's STANDARD deck look (white page, light beige accents, Khand/Hind): no cream page override; brand colours live only inside the mockups.
No 10-pick cap (Max approved for the collab decks). Results go to WellNest (submit_agent wellnest); picks logged only, never applied.
The Buds Station deck must pass banned_check() (build_wnc_1018 rules + no temple / sacred / leaf words or glyphs) or the build fails."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
from build_wnc_1018 import banned_check as banned_1018
import wnc1019 as C
WN = dict(submit_agent="wellnest", submit_to="WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", board="wellnest", audience="Max")
REQ = ("Oct 19 2026 9:37 ICT: Max asked directly: 'please add more decks for powerhaus and buds station. but please create new designs that still have our "
       "brand but have more differences than our roselle line.' Each partner gets its own co-branded sub-line look (containers, label shapes, patterns, palettes, type, in-studio / in-shop, menu, merch).")
DECKS = [
    ("wellnest-powerhaus-collab-look", "PowerHaus Collab Look", "powerhaus-collab-look", C.T_POWERHAUS, 1846,
     "Drawn SVG mockups of a PowerHaus Studio sub-line: slim tins, box pouch, bottle, studio scenes, menu and merch. WellNest circle mark on every piece; "
     "PowerHaus set in type in its blues and gold, no PowerHaus logo artwork. No prices or claims.", "/workspace/wellnest/research/powerhaus-brand.md"),
    ("wellnest-buds-station-collab-look", "Buds Station Collab Look", "buds-station-collab-look", C.T_BUDS, 1847,
     "Drawn SVG mockups of a Buds Station Lounge sub-line: round tins, jars, pillow packs, lounge scenes, menu and merch in pink, butter and powder blue with clouds and a sleepy cat. "
     "No plant shapes, no religious imagery (build check); The Buds Station set in type only. No prices or claims.", "/workspace/wellnest/research/buds-station-brand.md"),
]
EXTRA_BAN = re.compile(r"\b(temples?|wat|spires?|bodhi|photharam|chedis?|sacred|monks?|leaf|leaves|leafy|foliage|stucco|laterite)\b", re.I)
def banned_check(dj, extra=()):
    hits = banned_1018(dj, extra)
    blob = json.dumps([dj, list(extra)], ensure_ascii=False)
    for m in EXTRA_BAN.finditer(re.sub(r'"(id|topic|date)": "[^"]*"', "", blob)): hits.append(("deck", f"temple/leaf word: {m.group(0)!r}"))
    if re.search(r'data-g="(spire7|bodhi|brick-texture|stucco-speckle)"', blob): hits.append(("deck", "Roselle-era temple motif glyph"))
    return hits
def finish_page(slug, name):
    pg = os.path.join(slug, "index.html"); h = open(pg).read()
    if "const D=" in h: return h
    h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
    assert "<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}" in h, "standard white deck look"
    assert '<a class="builtby' in h, "standard footer"
    open(pg, "w").write(h); return h
if __name__ == "__main__":
    out = {}; outdir = sys.argv[1]
    for did, name, slug_base, fn, seed, ex, src in DECKS:
        pairs = fn(); n = len(pairs)
        assert theme_name_ok(name) and not re.search(r"\d", name), name
        caption_rule.guard(pairs, did); assert not EMOJI.search(json.dumps(pairs, ensure_ascii=False)), "emoji"
        txt = json.dumps([[p["optionA"]["label"], p["optionA"]["desc"], p["optionB"]["label"], p["optionB"]["desc"], p["ask"]] for p in pairs])
        assert not re.search(r"(฿|baht|\$|\bTHB\b|organic|certified|detox|cure|heal|boost)", txt, re.I), "no prices or claims"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n, "duplicate asks"
        m = dict(WN, topic=did, shelf=True, requested=True, request=REQ, log_only=True, results_policy="results logged only, never applied", example_data=ex,
                 deck_size=n, no_cap="Max approved no 10-pick cap for the collab decks (Oct 18 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 built_at_note="WellNest collab look decks, Oct 19 2026 9:37 ICT request",
                 brands=["Standard deck look (white, light beige accents, Khand/Hind); brand colours only inside the mockups",
                         "WellNest DNA: circle + script mark, cream, mono small print, kraft cue; not the Roselle cream-label kraft pouch"],
                 sources={"research": src, "builder": "tools/build_wnc_1019.py", "cards": "tools/wnc1019.py", "draw": "tools/wnc1019_draw.py"})
        publish(did, name, "WellNest", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n, (did, len(dj["pairs"]))
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None)
        json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(did, slug_base); h = finish_page(slug, name)
        blurb = f"{n} picks: containers, labels, patterns, colour, type, in-studio, menu, merch" if "powerhaus" in did else \
                f"{n} picks: containers, labels, patterns, colour, type, in-shop, menu, merch"
        shelf = {"name": name, "blurb": blurb}
        if "buds" in did:
            title = re.search(r"<title>([^<]*)</title>", h).group(1)
            hits = banned_check(dj, [title, shelf, slug, url])
            if hits:
                print("BANNED-WORD CHECK FAILED:"); [print(" ", p, w) for p, w in hits]; sys.exit(1)
            print("banned-word check: PASS", did)
        out[did] = {"id": did, "name": name, "url": url, "slug": slug, "total": n, "titles": [p["ask"] for p in dj["pairs"]], "blurb": blurb}
        print(did, url, n)
    json.dump(out, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
