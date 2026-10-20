"""UpKeep board decks, Oct 19 2026 (Max via UpKeep Develop 12:02 ICT; updates 12:04, 12:06, 12:07 ICT). Usage: python3 tools/build_ukhf_1019.py <outdir>  (repo root)
Same kit and process as build_mcd_1019.py (team_kit publish, md1018_kit page writer, standard white deck look, 'Built by Machan'
footer, Notes + Share). Results route to Branding (Swatch), picks logged only. Listed at the top of Max's Picks on the Branding board shelf,
NOT on any UpKeep board (Max: UpKeep boards have no swipe decks for now). Command Center left out (undecided).
  UpKeep Board Header Deck (20): header + Emergency Alerts + To-Do List + Documents Center (decided 12:07: pings/flags, To-Do, Documents in the header)
  UpKeep Board Footer Deck (20): Ping Record with ping schedule, Routines, footer finish (Built by Machan, Share, divider)
  Technicians Board Layout Deck (12): looks of the confirmed sections; Certifications and Training only as Optional pairs
  Tools And Equipment Board Deck (18): Tech Tool Bag, Van Inventory Tracking, Ordering; tool list / van setup / suppliers shown as Open; Max approval step
Cards: tools/ukhf1019_kit.py, ukhf1019_header.py, ukhf1019_footer.py, ukhf1019_tech.py, ukhf1019_tools.py.
PRIVACY: invented SAMPLE data only; guard fails the build on real-address markers, Thai references or emoji."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import draft_svg, trim_deck
draft_svg.DECK_SIZE = draft_svg.MAX_PAIRS = trim_deck.MAX_PAIRS = trim_deck.DECK_SIZE = 40
import caption_rule
from team_kit import publish
from md1018_kit import page, EMOJI
from split_deck import theme_name_ok
import ukhf1019_header, ukhf1019_footer, ukhf1019_tech, ukhf1019_tools
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding", audience="Max")
BAD = re.compile(r"wickfield|2573|thai|thailand|[\u0E00-\u0E7F]", re.I)
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|first|second|third)\b|\d", re.I)
REQ0 = "Oct 19 2026 12:02 ICT (relayed by UpKeep Develop): Max wants this-or-that decks to choose the Smart Upkeep branded header and footer for the four UpKeep agent boards (Members, Technicians, Tools & Equipment, Scheduling); Command Center left out, undecided."
DECKS = [
    ("branding-upkeep-board-header-deck", "UpKeep Board Header Deck", "upkeep-board-header", ukhf1019_header.T_HEADER, 20, 2101,
     REQ0 + " 12:06: header must include Emergency Alerts and a To-Do List like the dashboard folds. 12:07 decided for all four boards: pings and flags (Emergency Alerts), To-Do List and Documents live in the branded header.",
     "Laptop browser mockups (1366 wide) of the Members board header: UP house mark, title, Emergency Alerts, To-Do List, Documents Center. Invented SAMPLE data."),
    ("branding-upkeep-board-footer-deck", "UpKeep Board Footer Deck", "upkeep-board-footer", ukhf1019_footer.T_FOOTER, 20, 2102,
     REQ0 + " 12:07 decided: the footer holds the ping schedule and Ping Record plus Routines; board footer reads Built by Machan.",
     "Laptop browser mockups (1366 wide) of the Members board footer: Ping Record, ping schedule, Routines, Built by Machan line, Share. Invented SAMPLE data."),
    ("branding-technicians-board-layout-deck", "Technicians Board Layout Deck", "technicians-board-layout", ukhf1019_tech.T_TECH, 12, 2103,
     "Oct 19 2026 12:04 ICT: Max's decided Technicians board sections in order: Documents, tech-only company calendar, who's working this week, urgent and safety flags (gas, electrical, CO, flooding pinned at the top), visits log with photos and notes; ping log in the branded footer; every section switches day/week/month. 12:07: sections confirmed, pairs are only about looks; Certifications and Training is optional and shown only in pairs labelled Optional.",
     "Laptop browser mockups (1366 wide) of the Technicians board with sample techs Tech Dash 1-3, tagged TEST / SAMPLE."),
    ("branding-tools-equipment-board-deck", "Tools And Equipment Board Deck", "tools-equipment-board", ukhf1019_tools.T_TOOLS, 18, 2104,
     "Oct 19 2026 12:07 ICT: Max asked for a Tools & Equipment board deck covering its own sections Tech Tool Bag, Van Inventory Tracking and Ordering (bag checklists, condition, last checked, van stock with min/par, low-stock flags, order requests with Requested / Needs Max's approval / Approved / Ordered / Received, supplier and cost placeholders). Final tool list, van setup and suppliers are OPEN. Ordering never buys without Max's approval.",
     "Laptop browser mockups (1366 wide) of the Tools & Equipment board, generic category names only, Open placeholders for undecided lists and suppliers, every item labelled TEST, Forecast or Decided."),
]
if __name__ == "__main__":
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True); built = []
    only = set(sys.argv[2:])
    for DID, NAME, SLUG, fn, N, seed, REQ, EX in DECKS:
        if only and DID not in only: continue
        pairs = fn(); n = len(pairs); assert n == N, (DID, n)
        assert theme_name_ok(NAME) and not NUMW.search(NAME), NAME
        caption_rule.guard(pairs, DID); blob = json.dumps(pairs, ensure_ascii=False)
        assert not EMOJI.search(blob), "emoji"; assert not BAD.search(blob), BAD.search(blob)
        assert all("SAMPLE" in p[k]["visual"]["svg"] for p in pairs for k in ("optionA", "optionB")), "Sample label"
        assert all("Built by Machan" in p[k]["visual"]["svg"] for p in pairs for k in ("optionA", "optionB")), "board footer line"
        order = [p["ask"] for p in pairs]
        m = dict(BR, topic=DID, shelf=True, requested=True, request=REQ, log_only=True, results_policy="results logged only, never applied",
                 example_data=EX + " No real names, addresses or phones.", deck_size=n, no_cap=f"Max asked for {n} cards (Oct 19 2026)", caption_rule="R105", notes=True,
                 built_by="Branding", built_at_note="UpKeep board decks, Oct 19 2026 12:02-12:07 ICT requests",
                 brands=["Standard deck look (white, light beige accents, Khand/Hind)", "Mockups: white/cream base, terracotta, lagoon and jungle accents, UP house mark, light only"],
                 sources={"builder": "tools/build_ukhf_1019.py", "cards": "tools/" + fn.__module__ + ".py", "kit": "tools/ukhf1019_kit.py"})
        publish(DID, NAME, "UpKeep", pairs, m, seed=seed, n=n, first=0)
        dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == n
        dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
        for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
        dj.pop("owner", None); json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
        slug, url = page(DID, SLUG); pg = os.path.join(slug, "index.html"); h = open(pg).read()
        if "const D=" not in h:
            h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
            assert '<a class="builtby' in h and "maxweberman.com" in h, "standard footer"
            # deck page footer must read 'Built by Machan' (Max, Oct 19 12:02 ICT); the template link text reads Built by Machan
            i = h.index('<a class="builtby'); j = h.index("</a>", i); a_ = h[i:j]
            assert 'href="https://maxweberman.com"' in a_ and "Built by Machan" in a_, "builtby link"
            h = h[:i] + a_.replace("Built by Machan", "Built by Machan") + h[j:]
            open(pg, "w").write(h)
        built.append({"id": DID, "name": NAME, "url": url, "slug": slug, "total": n, "titles": order}); print(DID, url, n)
    json.dump(built, open(os.path.join(outdir, "built.json"), "w"), indent=1)
