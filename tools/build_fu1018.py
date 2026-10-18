"""Evening follow-up decks Oct 18 2026 (Max 16:50 ICT): one fresh deck per finished deck. Usage: python3 tools/build_fu1018.py [deck-id ...]
Same kit as build_pin4_1018.py (md1018_kit.ship). Writes /workspace/wt/pin4-1018/fu-built.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import fu1018 as F
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
REQ = "Max Oct 18 2026 16:50 ICT: a fresh follow-up deck for each finished deck, one level deeper; results logged only, never applied"
D = [("upkeep-investor-pitch-method-line-and-app-link-ending-deck", "Investor Pitch: Method Line And App Link Ending", F.T_VAL, "pitch-method-app-ending", "upkeep-investor-pitch-honest-valuation-and-blob-chart-deck", True),
     ("upkeep-funnel-compare-pop-up-photo-tiles-and-week-picker-deck", "Funnel: Compare Pop-Up, Photo Tiles And Week Picker", F.T_PAY2, "funnel-compare-tiles-week", "upkeep-funnel-subscribe-and-pay-deck", False),
     ("upkeep-crew-uniform-logo-button-up-and-cold-weather-gear-deck", "Crew Uniform: Logo, Button-Up And Cold-Weather Gear", F.T_CREW2, "crew-logo-button-up-gear", "upkeep-crew-uniform-new-options-deck", False),
     ("upkeep-investor-pitch-live-apps-agent-chart-and-use-of-funds-deck", "Investor Pitch: Live Apps, Agent Chart And Use Of Funds", F.T_ORG2, "pitch-live-apps-agents-funds", "upkeep-investor-pitch-org-chart-timeline-and-ask-deck", True),
     ("upkeep-investor-pitch-wordmark-cover-problem-photo-and-plan-tabs-deck", "Investor Pitch: Wordmark Cover, Problem Photo And Plan Tabs", F.T_COVER2, "pitch-cover-photo-tabs", "upkeep-investor-pitch-cover-problem-and-plans-deck", True),
     ("upkeep-funnel-price-lock-photos-home-tiles-and-contact-deck", "Funnel: Price Lock Photos, Home Tiles And Contact", F.T_INFO2, "funnel-price-lock-tiles", "upkeep-funnel-gathering-client-info-deck", False),
     ("upkeep-member-app-tab-bar-plus-button-and-add-on-cards-deck", "Member App: Tab Bar, Plus Button And Add-On Cards", F.T_MEMBER2, "member-tabs-plus-addons", "upkeep-clear-picks-tabs-headlines-and-add-on-step-deck", False),
     ("upkeep-forecast-app-scenario-swipe-drivers-and-sample-marks-deck", "Forecast App: Scenario Swipe, Drivers And Sample Marks", F.T_FC2, "forecast-scenarios-drivers", "upkeep-forecast-app-charts-scenarios-and-runway-deck", False),
     ("upkeep-investor-pitch-story-order-takeaways-and-product-frames-deck", "Investor Pitch: Story Order, Takeaways And Product Frames", F.T_STORY2, "pitch-story-takeaways-frames", "upkeep-investor-pitch-story-flow-and-app-format-deck", True)]
outp = "/workspace/wt/pin4-1018/fu-built.json"
out = json.load(open(outp)) if os.path.exists(outp) else {}
for i, (did, name, fn, slug, follows, pitch) in enumerate(D):
    if sys.argv[1:] and did not in sys.argv[1:]: continue
    pairs = fn()
    if pitch: assert not re.search(r"\bmax\b(?!-)|weberman|machan", json.dumps(pairs), re.I), (did, "founder name in pitch mockup")
    m = dict(UP, topic=did, shelf=True, audience="Max", requested=True, request=REQ, follows=follows, results_policy="log only, never applied",
             example_data="All numbers, names and addresses on cards are labelled samples, forecasts or placeholders; no real customer details.")
    r = ship(did, name, "UpKeep", pairs, m, seed=5180 + i, slug_base=slug, upkeep=True)
    r["follows"] = follows; out[did] = r; print(did, r["url"], len(r["titles"]))
json.dump(out, open(outp, "w"), indent=1, ensure_ascii=False)
