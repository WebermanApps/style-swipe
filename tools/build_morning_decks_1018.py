"""Morning decks Oct 18 2026 (Branding). Source of truth: /workspace/ops/brand/daily-work-report/2026-10-17.md.
Usage: python3 tools/build_morning_decks_1018.py <group> [<group> ...]   groups: tech trust pitch light dash research tea legal
Writes decks/<id>.json, a locked-ready page per deck, ledgers (shown_options.json, decks/sizes.json, decks/pages.json) and
/workspace/wt/md1018-built.json (id, name, url, titles per deck). Nothing is built for Ethan, UpKeep Security, the UpKeep Command
Center, Prop or Construction (paused)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import md1018_tech as TE, md1018_trust as TR, md1018_pitch as PI, md1018_dash as DA, md1018_light as LI
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BR = dict(submit_agent="branding", submit_to="Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", board="branding")
RS = dict(submit_agent="research", submit_to="Research Agent", board="research")
WN = dict(submit_agent="wellnest", submit_to="WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35", board="wellnest")
LG = dict(submit_agent="legal", submit_to="Legal Agent", board="legal")
REQ = "Max via Branding morning run Oct 18 2026: fresh this-or-that decks from the Oct 17 daily work report; 10 picks, Notes, light mode, R105 captions, theme names"
G = {
 "tech": [("upkeep-tech-app-walkthrough-full-list-and-step-screens-deck", "Tech App Walkthrough: Full List And Step Screens", "UpKeep", TE.T1, UP, "tech-app-walkthrough", "1a", True),
          ("upkeep-tech-app-check-in-and-before-photos-deck", "Tech App Check-In: Arrival And Before Photos", "UpKeep", TE.T2, UP, "tech-app-check-in", "1a", True),
          ("upkeep-tech-app-moisture-readings-and-walk-recap-deck", "Tech App Readings: Moisture Scale And Walk Recap", "UpKeep", TE.T3, UP, "tech-app-readings", "1a", True)],
 "trust": [("upkeep-trust-tags-loop-wording-colour-and-motion-deck", "Trust Tags: Loop Wording, Colour And Motion", "UpKeep", TR.T_A, UP, "trust-tags-loop", "1b", True),
           ("upkeep-what-we-take-care-of-care-card-carousel-deck", "What We Take Care Of: Care Card Carousel", "UpKeep", TR.T_B, UP, "wwtco-care-carousel", "1b", True),
           ("upkeep-home-page-trust-tags-and-care-cards-together-deck", "Home Page: Trust Tags And Care Cards Together", "UpKeep", TR.T_C, UP, "home-tags-and-cards", "1b", True)],
 "pitch": [("upkeep-investor-pitch-app-navigation-and-key-points-deck", "Investor Pitch App: Navigation And Key Points", "UpKeep", PI.T_P1, UP, "pitch-app-navigation", "1c", True),
           ("upkeep-investor-pitch-honest-valuation-and-blob-chart-deck", "Investor Pitch: Honest Valuation And Blob Chart", "UpKeep", PI.T_P2, UP, "pitch-valuation-blob", "1c", True),
           ("upkeep-forecast-app-charts-scenarios-and-runway-deck", "Forecast App: Charts, Scenarios And Runway", "UpKeep", PI.T_P3, UP, "forecast-app-charts", "1c", True)],
 "light": [("upkeep-member-profile-all-good-sign-and-problems-deck", "Member Profile: All Good Sign And Problems", "UpKeep", LI.T_PROFILE, UP, "member-profile-all-good", "1d", True),
           ("upkeep-crew-uniform-new-options-deck", "Crew Uniform: New Options", "UpKeep", LI.T_ATTIRE, UP, "crew-uniform-new-options", "1e", True),
           ("upkeep-sign-up-form-cancel-notice-steps-and-pay-deck", "Sign Up Form: Cancel Notice, Steps And Pay", "UpKeep", LI.T_SIGNUP, UP, "sign-up-cancel-steps-pay", "1f", True)],
 "dash": [("branding-max-s-picks-phone-carousel-deck", "Max's Picks: Phone Carousel", "Branding Board", DA.T_D1, BR, "max-picks-phone-carousel", "2", False),
          ("dashboard-kit-carousel-standard-deck", "Dashboard Kit: Carousel Standard", "Branding Board", DA.T_D2, BR, "kit-carousel-standard", "2", False),
          ("dashboard-kit-phone-sections-as-carousels-deck", "Dashboard Kit: Phone Sections As Carousels", "Branding Board", DA.T_D3, BR, "kit-phone-sections", "2", False)],
 "research": [("research-machan-launch-and-checkout-options-deck", "Machan Launch And Checkout Options", "Research", LI.T_RES1, RS, "machan-launch-checkout", "3", False),
              ("research-tech-certs-training-and-cool-tech-deck", "Tech Certs, Training And Cool Tech", "Research", LI.T_RES2, RS, "tech-certs-training-cool-tech", "3", False)],
 "tea": [("wellnest-new-tea-ideas-deck", "WellNest Teas: New Blend Ideas", "WellNest", LI.T_TEA, WN, "wellnest-new-tea-ideas", "4", False)],
 "legal": [("legal-questions-center-grouping-deck", "Legal Questions Center: Grouping", "Legal", LI.T_LEGAL, LG, "legal-questions-grouping", "6", False)],
}
def main(groups):
    out_p = "/workspace/wt/md1018-built.json"
    out = json.load(open(out_p)) if os.path.exists(out_p) else {}
    for g in groups:
        for i, (did, name, app, fn, meta, slug, sec, up) in enumerate(G[g]):
            m = dict(meta, topic=f"morning-1018-{g}", shelf=True, audience="Max", requested=True, request=REQ, report_section=sec,
                     example_data="All numbers, names and addresses on cards are labelled samples or placeholders; no real customer details.")
            r = ship(did, name, app, fn(), m, seed=1018 + i, slug_base=slug, upkeep=up)
            r.update(group=g, board=meta["board"]); out[did] = r
            print(g, did, r["url"], len(r["titles"]))
    json.dump(out, open(out_p, "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    main(sys.argv[1:])
