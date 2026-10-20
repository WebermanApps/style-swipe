"""Research Tech Certs follow-up deck (10 pairs, Research spec), built with the Branding ten-pair kit. Originally: Branding ten-pair follow-up decks, Oct 19 2026 16:10 ICT (Max: 'prepare fresh new decks on the same topics i swiped on. they don't have to be as long.
i like 10 at a time'). Usage: python3 tools/build_fu10_1019.py <outdir> [deck ids]   (repo root)
Same kit and process as build_sched_1019.py / build_ukhf_1019.py / build_mfu_1019.py: team_kit publish, md1018_kit page writer, standard deck look,
'Built by Machan' footer to maxweberman.com, Notes + Share. Results route to Branding, picks logged only. Cards: tools/fu10_1019.py.
Each deck asks the next level after his Oct 19 picks and notes; no decided pair is repeated."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import rtc1019 as F
BR = dict(submit_agent="research", submit_to="Research Agent", board="research", audience="Max")
BAD = re.compile(r"wickfield|2573|\bthai|thailand|[\u0E00-\u0E7F]|@|\(\d{3}\)|\b\d{5}\b|\blat\b|\blng\b|\bstreet\b", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
INBOX = "/workspace/ops/submit/inbox/research/"
REQ = "Research follow-up to Max's Oct 19 2026 Tech Certs, Training And Cool Tech picks (01-09 A, 10 B); spec by Research, built and published by Swatch Oct 19 2026 16:28 ICT"
DECKS = [("research-tech-certs-followup-deck", "Tech Certs And Training Follow-Up", "tech-certs-training-follow-up", F.T_RTC, "Research", False, 3301,
          ["research-tech-certs-training-and-cool-tech-deck-20261019-1607-9d8bc13d.json"],
          "Drawn mockups from Research's visual briefs: cream and gold, TEST / SAMPLE data, illustrated healthy-looking techs (no real people), plain word badges (no real cert logos). Spec: /workspace/ops/research/2026-10-19-tech-certs-followup-deck.json")]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); only = set(sys.argv[2:]); built = []
    for did, name, slug_base, fn, app, cream, seed, srcs, ex in DECKS:
        if only and did not in only: continue
        pairs = fn(); n = len(pairs); assert n == 10, (did, n)
        assert theme_name_ok(name) and not NUMW.search(name), name
        caption_rule.guard(pairs, did); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob.replace("事事如意", "")), "emoji"; assert not BAD.search(blob), (did, BAD.search(blob))
        if app == "Research": assert all(("SAMPLE" in p[k]["visual"]["svg"] or "TEST" in p[k]["visual"]["svg"]) for p in pairs for k in ("optionA", "optionB")), "sample label"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=[s.rsplit("-2026", 1)[0] for s in srcs], log_only=True, results_policy="results logged only, never applied",
                 example_data=ex, deck_size=n, no_cap="Max asked for 10 at a time (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 built_at_note="Ten-pair follow-ups, Oct 19 2026 16:10 ICT request",
                 sources={"results": [INBOX + s for s in srcs], "builder": "tools/build_rtc_1019.py", "cards": "tools/rtc1019.py", "spec": "/workspace/ops/research/2026-10-19-tech-certs-followup-deck.json"})
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
            h = h[:i] + a_.replace("Built by Machan", "Built by Machan") + h[j:]
            assert "Built by Machan" in h[i:i + len(a_) + 20]
            open(pg, "w").write(h)
        built.append({"id": did, "name": name, "url": url, "slug": slug, "total": n, "titles": order,
                      "labels": [f"{p['optionA']['label']} vs {p['optionB']['label']}" for p in dj["pairs"]]}); print(did, url, n)
    json.dump(built, open(os.path.join(outdir, "built.json"), "w"), indent=1, ensure_ascii=False)
