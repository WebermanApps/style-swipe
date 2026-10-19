"""Branding ten-pair follow-up decks, Oct 19 2026 16:10 ICT (Max: 'prepare fresh new decks on the same topics i swiped on. they don't have to be as long.
i like 10 at a time'). Usage: python3 tools/build_fu10_1019.py <outdir> [deck ids]   (repo root)
Same kit and process as build_sched_1019.py / build_ukhf_1019.py / build_mfu_1019.py: team_kit publish, md1018_kit page writer, standard deck look,
'Built by Max Weberman' footer to maxweberman.com, Notes + Share. Results route to Branding, picks logged only. Cards: tools/fu10_1019.py.
Each deck asks the next level after his Oct 19 picks and notes; no decided pair is repeated."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import fu10_1019 as F
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
BAD = re.compile(r"wickfield|2573|\bthai|thailand|[\u0E00-\u0E7F]|@|\(\d{3}\)|\b\d{5}\b|\blat\b|\blng\b|\bstreet\b", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
INBOX = "/workspace/ops/submit/inbox/branding/"
REQ = "Oct 19 2026 16:10 ICT: Max asked 'prepare fresh new decks on the same topics i swiped on. they don't have to be as long. i like 10 at a time.'"
UK = "Laptop browser mockups (1366 wide) of the board in its decided state with a CLOSE-UP panel for the asked element; TEST / SAMPLE data, Tech Dash 1-3, Van 1-3, members by first name or ID only."
DECKS = [
 ("branding-member-catalog-polish", "Member Catalog Polish", "member-catalog-polish", F.T_MEM, "UpKeep", False, 3101,
  ["branding-member-catalog-deck-20261019-1148-72b7b824.json", "branding-member-catalog-deck-two-20261019-1550-aa9f024a.json"], UK),
 ("branding-board-rules-fine-tuning", "Board Rules Fine Tuning", "board-rules-fine-tuning", F.T_RULES, "UpKeep", False, 3102, ["all-boards-rules-deck-20261019-1221-5c1e4649.json"], UK),
 ("branding-scheduling-board-details", "Scheduling Board Details", "scheduling-board-details", F.T_SCHED2, "UpKeep", False, 3103, ["branding-scheduling-board-layout-deck-20261019-1448-4005fa83.json"], UK),
 ("branding-header-fine-tuning", "Header Fine Tuning", "header-fine-tuning", F.T_HDR, "UpKeep", False, 3104, ["branding-upkeep-board-header-deck-20261019-1500-c91a90ed.json"], UK),
 ("branding-footer-fine-tuning", "Footer Fine Tuning", "footer-fine-tuning", F.T_FTR, "UpKeep", False, 3105, ["branding-upkeep-board-footer-deck-20261019-1507-7be54d96.json"],
  UK + " No share button; Built by Machan centred opens the Machan story page."),
 ("branding-technicians-board-details", "Technicians Board Details", "technicians-board-details", F.T_TECH2, "UpKeep", False, 3106, ["branding-technicians-board-layout-deck-20261019-1511-1de507f3.json"], UK),
 ("branding-tools-equipment-details", "Tools And Equipment Details", "tools-equipment-details", F.T_TOOLS2, "UpKeep", False, 3107, ["branding-tools-equipment-board-deck-20261019-1530-562a8379.json"],
  UK + " Thumbnail grid on laptop, carousel on phone; supplier and cost tucked away; nothing bought without Max's approval; tool list, van setup and suppliers stay Open."),
 ("machan-look-polish", "Machan Look Polish", "machan-look-polish", F.T_LOOK2, "Branding", True, 3108, ["machan-look-refinements-20261019-1535-a07cd6bb.json"],
  "Drawn Machan as decided (eyes open at rest, wink on hover, thin soft warm-brown edge with subtle shading, level leaves, peach oval blush, short stem, bouncing loader, UpKeep mascot too). Look sheet: machan-look-sheet-x799jr."),
 ("machan-story-page", "Machan Story Page", "machan-story-page", F.T_STORY2, "Branding", True, 3109, ["machan-origin-story-refinements-20261019-1544-cbd38210.json"],
  "Story page mockups: short video of Machan's journey (surviving and learning) then a carousel; kawaii but powerful; wish glyph as a highlight; lore only: the Chinese wish pun, the Korean tiger tale, Greek Diospyros, the Ozark seed, the Nagasaki tree."),
]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); only = set(sys.argv[2:]); built = []
    for did, name, slug_base, fn, app, cream, seed, srcs, ex in DECKS:
        if only and did not in only: continue
        pairs = fn(); n = len(pairs); assert n == 10, (did, n)
        assert theme_name_ok(name) and not NUMW.search(name), name
        caption_rule.guard(pairs, did); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob.replace("事事如意", "")), "emoji"; assert not BAD.search(blob), (did, BAD.search(blob))
        if app == "UpKeep": assert all(("SAMPLE" in p[k]["visual"]["svg"] or "TEST" in p[k]["visual"]["svg"]) for p in pairs for k in ("optionA", "optionB")), "sample label"
        order = [p["ask"] for p in pairs]; assert len(set(order)) == n
        m = dict(BR, topic=did, shelf=True, requested=True, request=REQ, follows=[s.rsplit("-2026", 1)[0] for s in srcs], log_only=True, results_policy="results logged only, never applied",
                 example_data=ex, deck_size=n, no_cap="Max asked for 10 at a time (Oct 19 2026)", caption_rule="R105", notes=True, built_by="Branding",
                 built_at_note="Ten-pair follow-ups, Oct 19 2026 16:10 ICT request",
                 sources={"results": [INBOX + s for s in srcs], "builder": "tools/build_fu10_1019.py", "cards": "tools/fu10_1019.py"})
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
