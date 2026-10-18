"""Follow-up decks Oct 18 2026 night (Branding, after the 20:35 ICT pull): one fresh deck per finished deck.
Usage: python3 tools/build_fu2045_1018.py <outdir>
Follows build_pitchv3_1018.py (md1018_kit.ship; drops owner/meta, the personal built-by footer link, and titles the page after
the deck) for all four decks. Results are logged only, never applied."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import fu2045_1018 as F
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|[\u0E00-\u0E7F]", re.I)
POL = "results logged only, never applied"
DECKS = [("upkeep-tagline-supporting-line-social-and-signage-deck", "Tagline: Supporting Line, Social And Signage", "tagline-support-social-signage", F.T_TAGLINE2, 6201,
          "upkeep-tagline-home-maintenance-membership-deck",
          "Oct 18 2026 night: follow-up to Tagline: Home Maintenance Membership (19:51 ICT picks): supporting line, social profile and posts, yard sign, van rear, door hanger, email signature; re-asks tagline case and polo back (both Neither)",
          "All in-context screens are drawn mockups; wording is sample, contact details and web address are placeholders."),
         ("upkeep-investor-pitch-scroll-previews-and-anonymous-founder-deck", "Investor Pitch: Scroll Previews And Anonymous Founder", "pitch-scroll-previews-founder", F.T_PITCH_SCROLL, 6202,
          "upkeep-investor-pitch-wordmark-cover-problem-photo-and-plan-tabs-deck",
          "Oct 18 2026 night: follow-up to Wordmark Cover, Problem Photo And Plan Tabs (18:53 ICT picks): zoom-in scrollable view-only app previews, step names, plan tab content; re-asks problem caption and founder heading; anonymous founder with background known",
          "Pitch slides are drawn mockups; founder unnamed, no photo; app views are samples."),
         ("upkeep-investor-pitch-agent-chart-previews-and-tech-hire-deck", "Investor Pitch: Agent Chart, Previews And Tech Hire", "pitch-agent-chart-tech-hire", F.T_PITCH_AGENTS, 6203,
          "upkeep-investor-pitch-live-apps-agent-chart-and-use-of-funds-deck",
          "Oct 18 2026 night: follow-up to Live Apps, Agent Chart And Use Of Funds (18:57 ICT picks): founder on top or centre, agent boxes, tech #2 hire at 75 homes on the chart, what Open shows, back control, techs slice, Beta label, swipe hint; re-asks sample data label",
          "Pitch slides are drawn mockups; founder unnamed; funds split is a sample; Beta and hiring figures are Expected/Forecast."),
         ("upkeep-funnel-photo-price-note-upload-and-contact-deck", "Funnel: Photo Price Note, Upload And Contact", "funnel-photo-price-upload", F.T_FUNNEL2, 6204,
          "upkeep-funnel-price-lock-photos-home-tiles-and-contact-deck",
          "Oct 18 2026 night: follow-up to Price Lock Photos, Home Tiles And Contact (19:13 ICT picks): how to explain that skipping photos can change the price after visit one, terms link, drop area plus camera, thumbnails, size ranges, Not sure tile, edit style; home tiles and contact chips re-asked with our lean",
          "Sign-up screens are drawn mockups; answers and photos are samples.")]
out = {}
for DID, NAME, SLUG, fn, seed, FOLLOWS, REQ, EX in DECKS:
    pairs = fn(); txt = json.dumps(pairs, ensure_ascii=False).replace("max-width", "").replace("max-height", "")
    assert not BAD.search(txt), (DID, BAD.search(txt))
    m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, follows=FOLLOWS, results_policy=POL, example_data=EX)
    r = ship(DID, NAME, "UpKeep", pairs, m, seed=seed, slug_base=SLUG, upkeep=True)
    dj = json.load(open(f"decks/{DID}.json"))
    dj["meta"] = dj.get("meta", {}) if isinstance(dj.get("meta"), dict) else {}
    for k in ("built_at_note", "sources"):
        if k in dj: dj[k] = {"built_at_note": "Follow-up decks Oct 18 2026 night", "sources": {"builder": "tools/build_fu2045_1018.py"}}[k]
    dj.pop("owner", None)
    if dj.get("meta") == {}: dj.pop("meta")
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    assert not BAD.search(json.dumps(dj, ensure_ascii=False).replace("max-width", "").replace("max-height", "").replace("max_pairs", "")), (DID, "deck json")
    pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
    if "const D=" not in h:
        h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
        h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
        open(pg, "w").write(h)
    r["follows"] = FOLLOWS; out[DID] = r; print(DID, r["url"], len(r["titles"]))
json.dump(out, open(os.path.join(sys.argv[1], "built.json"), "w"), indent=1, ensure_ascii=False)
