"""Six fresh UpKeep decks Oct 18 2026 night (Branding, after the 9:20 PM ICT republish): 2 pitch, 2 member app, 2 tech flow,
all about the live versions. Usage: python3 tools/build_six_1018.py <outdir>
Follows build_pitchv3_1018.py / build_fu2045_1018.py (md1018_kit.ship; drops owner/meta and the built-by footer link, titles
the page after the deck) plus a light cream page background. Results are logged only, never applied."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import ship
import six1018 as F
UP = dict(submit_agent="upkeep", submit_to="UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d", board="upkeep")
BAD = re.compile(r"\bmax\b(?!-)|weberman|machan|thai|\bethan\b|upkeep security|\bAI\b|wickfield|2573|[\u0E00-\u0E7F]", re.I)
OK = ("AI agent training", "AI Agent Training", "Trains AI agents", "Trains AI Agents", "max-width", "max-height", "max_pairs")
def clean(t):
    for o in OK: t = t.replace(o, "")
    return t
POL = "results logged only, never applied"
REQ = "Oct 18 2026 9:20 PM ICT: after the republish, fresh decks about the live versions (2 pitch, 2 member, 2 technician)"
WHITE = ":root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}"
CREAM = ":root{--bg:#FAF6EE}html,body{background:#FAF6EE!important}"
DECKS = [("upkeep-pitch-forecast-pace-and-problem-copy-deck", "Pitch: Forecast Pace And Problem Copy", "pitch-forecast-pace-problem-copy", F.T_PITCH_FORECAST, 6301,
          "Live round-two investor pitch: forecast pace and chart readouts, Beta homes, problem headline and subline, to-do end state, furnace example, fact style",
          "Pitch slides are drawn mockups; every figure is labelled Forecast or Sample; no traction is claimed."),
         ("upkeep-pitch-founder-tiles-brand-art-and-ask-layout-deck", "Pitch: Founder Tiles, Brand Art And Ask Layout", "pitch-founder-brand-art-ask", F.T_PITCH_BRAND, 6302,
          "Live round-two investor pitch: founder tiles, line under the title, van gear labels and stripe, uniform pose, weather tags, slide transitions, ask layout, valuation line",
          "Pitch slides are drawn mockups; founder unnamed; people are illustrated; figures are Forecast or Sample."),
         ("upkeep-member-app-home-greeting-watch-list-and-next-visit-deck", "Member App: Home Greeting, Watch List And Next Visit", "member-home-greeting-watch", F.T_MEM_HOME, 6303,
          "Live member app home: header, house photo, greeting, Items To Watch, next visit card, visits this year, plan chips, Sample Data label",
          "Member app screens are drawn mockups; the member, home and history are samples."),
         ("upkeep-member-app-visit-reports-home-record-and-chat-deck", "Member App: Visit Reports, Home Record And Chat", "member-reports-record-chat", F.T_MEM_REPORTS, 6304,
          "Live member app reports, home record and chat: report rows and top, finding status, photos, moisture readings, systems order, chat header, reminder, quick replies",
          "Member app screens are drawn mockups; reports, readings and messages are samples."),
         ("upkeep-tech-flow-today-screen-map-and-pre-takeoff-deck", "Tech Flow: Today Screen, Map And Pre-Takeoff", "tech-flow-today-map-check", F.T_TECH_TODAY, 6305,
          "Live tech app investor flow: Today summary, route map line and tap hint, Pre-Takeoff Check, Start Your Day, pin popup, turn banner, on-site timer, week banner",
          "Tech app screens are drawn mockups; the route, members and counts are samples."),
         ("upkeep-tech-flow-route-list-job-card-and-job-notes-deck", "Tech Flow: Route List, Job Card And Job Notes", "tech-flow-route-job-notes", F.T_TECH_ROUTE, 6306,
          "Live tech app investor flow: route list current stop and plan chips, list or map, job card top, task minutes, Extra tag, Bring In and Access, alert, buttons, filter condition",
          "Tech app screens are drawn mockups; the route, members and tasks are samples.")]
LATE = (("html,body{background:#ffffff!important;", "html,body{background:#FAF6EE!important;"),
        ("html,body{background:#FFFFFF!important}:root{--bg:#FFFFFF;", "html,body{background:#FAF6EE!important}:root{--bg:#FAF6EE;"))
def cream(h):
    h = h.replace(WHITE, CREAM); assert CREAM in h, "cream"
    for a, b in LATE: h = h.replace(a, b)
    return h
out = {}
for DID, NAME, SLUG, fn, seed, BRIEF, EX in DECKS:
    pairs = fn(); assert len(pairs) == 10, DID
    assert not BAD.search(clean(json.dumps(pairs, ensure_ascii=False))), (DID, BAD.search(clean(json.dumps(pairs, ensure_ascii=False))))
    m = dict(UP, topic=DID, shelf=True, requested=True, request=REQ, brief=BRIEF, results_policy=POL, log_only=True, example_data=EX)
    r = ship(DID, NAME, "UpKeep", pairs, m, seed=seed, slug_base=SLUG, upkeep=True)
    dj = json.load(open(f"decks/{DID}.json"))
    dj["meta"] = dj.get("meta", {}) if isinstance(dj.get("meta"), dict) else {}
    for k in ("built_at_note", "sources"):
        if k in dj: dj[k] = {"built_at_note": "Six fresh UpKeep decks Oct 18 2026 night (after the 9:20 PM ICT republish)", "sources": {"builder": "tools/build_six_1018.py"}}[k]
    dj.pop("owner", None)
    if dj.get("meta") == {}: dj.pop("meta")
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    assert not BAD.search(clean(json.dumps(dj, ensure_ascii=False))), (DID, "deck json")
    pg = os.path.join(r["slug"], "index.html"); h = open(pg).read()
    h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
    h = re.sub(r'\s*<a class="builtby[^"]*"[^>]*>.*?</a>', "", h, count=1, flags=re.S)
    h = cream(h)
    open(pg, "w").write(h)
    out[DID] = r; print(DID, r["url"], len(r["titles"]))
json.dump(out, open(os.path.join(sys.argv[1], "built.json"), "w"), indent=1, ensure_ascii=False)
