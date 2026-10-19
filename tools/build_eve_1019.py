"""Branding follow-up decks, Oct 19 2026 evening. Max 9:45 PM ICT: 'can you record and swipes that were done, make the changes, and then refresh the decks.'
Five ten-pair decks, one per deck swiped after 4:07 PM; skips reworded, picks pushed one notch further (cards: tools/eve1019_cards.py).
NEW deck style Max chose tonight: dadbook layout in Max's brand (tools/eve1019_page.py). Team-gated submit via ../submit.js (unchanged).
Usage: python3 tools/build_eve_1019.py <outdir>   (repo root)"""
import json, os, re, sys, secrets, string
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import EMOJI
from split_deck import theme_name_ok
import eve1019_cards as F, eve1019_page as PG
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
BAD = re.compile(r"wickfield|2573|\bthai|thailand|[\u0E00-\u0E7F]|@|\(\d{3}\)|\b\d{5}\b|\blat\b|\blng\b|\bstreet\b", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
INBOX = "/workspace/ops/submit/inbox/branding/"
REQ = "Oct 19 2026 21:45 ICT: Max asked 'can you record and swipes that were done, make the changes, and then refresh the decks.'"
UK = "Close-up drawings (360x210) of the uk11 board state for the asked element; light only; TEST / SAMPLE data, Tech Dash 1-3, members by first name only."
LEDE = "Ten quick pairs, one notch past tonight's picks. Anything you skipped comes back asked another way."
DECKS = [
 ("branding-member-catalog-finishing-touches", "Member Catalog Finishing Touches", "member-catalog-finishing-touches", F.T_MEMBERS, 3201,
  "branding-member-catalog-polish-20261019-1935-bb9b44ec.json", "Finishing Touches", "Max's Picks · Members board"),
 ("branding-board-rules-final-polish", "Board Rules Final Polish", "board-rules-final-polish", F.T_RULES, 3202,
  "branding-board-rules-fine-tuning-20261019-2104-5c849cbe.json", "Final Polish", "Max's Picks · All UpKeep boards"),
 ("branding-scheduling-board-finishing-touches", "Scheduling Board Finishing Touches", "scheduling-board-finishing-touches", F.T_SCHED, 3203,
  "branding-scheduling-board-details-20261019-2110-9ff61b5a.json", "Finishing Touches", "Max's Picks · Scheduling board"),
 ("branding-header-finishing-touches", "Header Finishing Touches", "header-finishing-touches", F.T_HEADER, 3204,
  "branding-header-fine-tuning-20261019-2116-c95ec75e.json", "Finishing Touches", "Max's Picks · Board header"),
 ("branding-footer-finishing-touches", "Footer Finishing Touches", "footer-finishing-touches", F.T_FOOTER, 3205,
  "branding-footer-fine-tuning-20261019-2119-7c9a6036.json", "Finishing Touches", "Max's Picks · Board footer"),
]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); built = []
    for did, name, slug_base, fn, seed, src, em, kicker in DECKS:
        src_path = None
        for f in os.listdir(INBOX):
            if f == src: src_path = INBOX + f
        assert src_path, src
        pairs = fn(); n = len(pairs); assert n == 10, (did, n)
        assert theme_name_ok(name) and not NUMW.search(name), name
        caption_rule.guard(pairs, did); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob), "emoji"; assert not BAD.search(blob), (did, BAD.search(blob))
        assert all(("SAMPLE" in p[k]["visual"]["svg"] or "TEST" in p[k]["visual"]["svg"]) for p in pairs for k in ("optionA", "optionB")), "sample label"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=[src.rsplit("-2026", 1)[0]], log_only=True,
                 results_policy="results logged, then applied by owner (UpKeep boards: staged in handoff, never pushed)",
                 example_data=UK, deck_size=n, no_cap="Max asked for 10 at a time (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 deck_style="max-deck (dadbook layout in Max's brand, chosen Oct 19 2026 evening)",
                 built_at_note="Evening refresh, Oct 19 2026 21:45 ICT request",
                 sources={"results": [src_path], "log": "/workspace/ops/results/2026-10-19-evening.md", "builder": "tools/build_eve_1019.py", "cards": "tools/eve1019_cards.py", "page": "tools/eve1019_page.py"})
        publish(did, name, "UpKeep", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == n
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
        dj.pop("owner", None); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
        pages = json.load(open("decks/pages.json"))
        slug = pages.get(did) or slug_base + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        dj.setdefault("submit_agent", "branding"); dj.setdefault("submit_to", BR["submit_to"])
        PG.write(dj, slug, dict(kicker=kicker, lede=LEDE, em=em))
        pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
        url = f"https://webermanapps.github.io/style-swipe/{slug}/"
        built.append({"id": did, "name": name, "url": url, "slug": slug, "total": n, "follows": src_path, "titles": order,
                      "labels": [f"{p['optionA']['label']} vs {p['optionB']['label']}" for p in dj["pairs"]]}); print(did, url, n)
    json.dump(built, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
