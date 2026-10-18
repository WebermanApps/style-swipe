"""WellNest collab decks, Oct 18 2026 (Max asked WellNest directly 22:44 ICT; Branding builds): PowerHaus Pilates Collab Deck +
Buds Station Collab Deck. Usage: python3 tools/build_wnc_1018.py <outdir>   (from the repo root)
Same kit as build_machan_1018.py (md1018_kit page writer, team_kit publish, standard footer, cream #FAF6EE page) but with NO 10-pick
cap (Max approved, as many cards as needed). Results go to WellNest (submit_agent wellnest). Picks are logged only, never applied.
The Buds Station deck must pass banned_check() or the build fails (exit 1)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40   # no 10-pick cap for these two decks (Max approved)
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import wnc1018 as C
WN = dict(submit_agent="wellnest", submit_to="WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", board="wellnest", audience="Max")
REQ = ("Oct 18 2026 22:44 ICT: Max asked WellNest directly for two collab swipe decks (PowerHaus Pilates, The Buds Station): names, blends, "
       "co-brand lockup order and size, colour, pouch styling and tagline. WellNest leads the lockup; the WellNest kraft pouch with its watercolour wash stays the base.")
DECKS = [
    ("wellnest-powerhaus-pilates-collab-deck", "PowerHaus Pilates Collab Deck", "powerhaus-collab", C.T_POWERHAUS, 1844,
     "Drawn SVG mockups of the WellNest kraft pouch and lockup; PowerHaus is set in type in its own blues and gold, no PowerHaus logo artwork.",
     "/workspace/wellnest/research/powerhaus-brand.md"),
    ("wellnest-buds-station-collab-deck", "Buds Station Collab Deck", "buds-station-collab", C.T_BUDS, 1845,
     "Drawn SVG mockups of the WellNest kraft pouch and lockup; The Buds Station is set in type only, no shop logo. Neighbourhood inspiration is abstract only, no sacred images.",
     "/workspace/wellnest/research/buds-station-brand.md"),
]
# ---------- banned-word check (Buds Station deck): fails the build ----------
BANNED = re.compile(r"\b(cannabis|hemp|weed|ganja|kush|420|high|stoned|marijuana|marihuana|thc|cbd|dispensary|strain|stoner|toke|joint|blunt|dank|"
                    r"baked|blaze|stash|munchies|mary\s*jane|four[\s-]*twenty|buddha\w*|buddhist|chedi)\b", re.I)
BUDS_ONLY_AS_NAME = re.compile(r"\bbuds?\b(?![\s_-]+station)", re.I)       # 'buds' may appear only as the shop name Buds Station
LEAF_GLYPHS = re.compile("[\U0001F33F\U0001F341\U0001F340\u2618\U0001F96C]")  # herb, maple leaf, four-leaf, shamrock, leafy green
ALLOWED_G = {"wellnest-mark", "partner-name", "spire7", "bodhi", "brick-texture", "stucco-speckle"}
def _svg_text(svg):
    """Visible text and naming attributes of an SVG (coordinates and hex colours are not words)."""
    txt = re.findall(r">([^<>]+)<", svg)
    names = re.findall(r'\s(?:id|class|data-g|aria-label|title)="([^"]*)"', svg)
    return " ".join(txt + names)
def banned_check(dj, extra=()):
    hits = []
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items(): walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x): walk(v, f"{path}[{i}]")
        elif isinstance(x, str):
            if "<svg" in x:
                s = _svg_text(x)
                for g in re.findall(r'data-g="([^"]*)"', x):
                    if g not in ALLOWED_G: hits.append((path, f"unknown glyph {g}"))
                for grp in re.findall(r'<g data-g="bodhi">', x)[3:]: hits.append((path, "more than three leaf glyphs in one card"))
            else: s = x
            for rx, why in ((BANNED, "banned word"), (BUDS_ONLY_AS_NAME, "'buds' outside the shop name"), (LEAF_GLYPHS, "leaf glyph")):
                for m in rx.finditer(s): hits.append((path, f"{why}: {m.group(0)!r}"))
    walk(dj, "deck")
    for i, s in enumerate(extra): walk(s, f"extra[{i}]")
    return hits
def finish_page(slug, name):
    pg = os.path.join(slug, "index.html"); h = open(pg).read()
    if "const D=" in h: return h
    h = re.sub(r"<title>[^<]*</title>", f"<title>{name} · Style Swipe</title>", h, count=1)
    old = "<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}"
    assert old in h; h = h.replace(old, "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
    assert '<a class="builtby' in h, "standard footer"
    open(pg, "w").write(h); return h
if __name__ == "__main__":
    out = {}; outdir = sys.argv[1]
    for did, name, slug_base, fn, seed, ex, src in DECKS:
        pairs = fn(); n = len(pairs)
        assert theme_name_ok(name) and not re.search(r"\d", name), name
        caption_rule.guard(pairs, did); assert not EMOJI.search(json.dumps(pairs, ensure_ascii=False)), "emoji"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n, "duplicate asks"
        m = dict(WN, topic=did, shelf=True, requested=True, request=REQ, log_only=True, results_policy="results logged only, never applied", example_data=ex,
                 deck_size=n, no_cap="Max approved no 10-pick cap (Oct 18 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 built_at_note="WellNest collab decks, Oct 18 2026 22:44 ICT request", sources={"research": src, "builder": "tools/build_wnc_1018.py"})
        publish(did, name, "WellNest", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n, (did, len(dj["pairs"]))
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None)
        json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(did, slug_base); h = finish_page(slug, name)
        shelf = {"name": name, "blurb": f"{n} picks: names, blends, lockup, colour, pouch, tagline"}
        if "buds" in did:
            title = re.search(r"<title>([^<]*)</title>", h).group(1)
            hits = banned_check(dj, [title, shelf, slug, url])
            if hits:
                print("BANNED-WORD CHECK FAILED:"); [print(" ", p, w) for p, w in hits]; sys.exit(1)
            print("banned-word check: PASS", did)
        out[did] = {"id": did, "name": name, "url": url, "slug": slug, "total": n, "titles": [p["ask"] for p in dj["pairs"]], "blurb": shelf["blurb"]}
        print(did, url, n)
    json.dump(out, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
