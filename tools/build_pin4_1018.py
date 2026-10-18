"""Four pinned UpKeep decks, Oct 18 2026 (Max via Branding, 15:52 ICT). Usage: python3 tools/build_pin4_1018.py [deck-id ...]
Uses md1018_kit.ship (same deck format as build_morning_decks_1018.py). Writes /workspace/wt/pin4-1018/built.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import pin4_1018 as P4
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
REQ = "Max Oct 18 2026 15:52 ICT: 4 new pinned UpKeep decks (pitch remake x2 phone-first, funnel info, funnel subscribe and pay); 10 picks, Notes, light mode"
D = [("upkeep-investor-pitch-cover-problem-and-plans-deck", "Investor Pitch: Cover, Problem And Plans", P4.T_PITCH1, "pitch-cover-problem-plans"),
     ("upkeep-investor-pitch-org-chart-timeline-and-ask-deck", "Investor Pitch: Org Chart, Timeline And Ask", P4.T_PITCH2, "pitch-org-timeline-ask"),
     ("upkeep-funnel-gathering-client-info-deck", "Funnel: Gathering Client Info", P4.T_INFO, "funnel-client-info"),
     ("upkeep-funnel-subscribe-and-pay-deck", "Funnel: Subscribe And Pay", P4.T_PAY, "funnel-subscribe-pay")]
out = json.load(open("/workspace/wt/pin4-1018/built.json")) if os.path.exists("/workspace/wt/pin4-1018/built.json") else {}
for i, (did, name, fn, slug) in enumerate(D):
    if sys.argv[1:] and did not in sys.argv[1:]: continue
    m = dict(UP, topic=did, shelf=True, audience="Max", requested=True, request=REQ, pinned=True,
             example_data="All numbers, names and addresses on cards are labelled samples or placeholders; no real customer details.")
    r = ship(did, name, "UpKeep", fn(), m, seed=4180 + i, slug_base=slug, upkeep=True)
    out[did] = r; print(did, r["url"], len(r["titles"]))
json.dump(out, open("/workspace/wt/pin4-1018/built.json", "w"), indent=1, ensure_ascii=False)
