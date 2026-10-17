#!/usr/bin/env python3
"""UpKeep (Smart Upkeep) five follow-on decks, Oct 17 2026 (Branding Agent for Max): 10 picks each (R86), drawn visuals,
example data labeled, chat to UpKeep, Machan footer, Share icon in the header (kit ly9 / 01b5560 pattern), R89 deck look (white page, 10px deck cards, full-width card art) as in team-improvement-zamgtx.
 1 Employee Attire Deck (uk5_attire)        2 Investor Pitch Deck: Slide Looks (uk5_pitch)
 3 Financial Forecasting Deck (uk5_forecast) 4 What We Take Care Of Deck (uk5_wwtco)   5 UpKeep Operator Console Deck (uk5_company; replaces the unpublished Company Dashboard draft)
Slugs persist in queue/upkeep-five-decks-slugs.json. Not added to UpKeep's shelf (UpKeep posts them)."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, re, string, secrets
from team_kit import deck as kdeck, publish
from agent_links import patch as link_patch
import uk5_attire, uk5_pitch, uk5_forecast, uk5_wwtco, uk5_company
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SL = "queue/upkeep-five-decks-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
DECKS = [
 ("upkeep-employee-attire-deck", "Employee Attire Deck", "upkeep-employee-attire", "uk5att_", uk5_attire.PAIRS, "Technician uniforms on drawn people (faceless, no likenesses): polo color, logo spot, pants, hats, name patch, shoes, seasonal layers.", "Attire"),
 ("upkeep-investor-pitch-slide-looks-deck", "Investor Pitch Deck: Slide Looks", "upkeep-investor-pitch-slides", "uk5pit_", uk5_pitch.PAIRS, "Slide looks and story choices for the investor pitch; every number is a labeled placeholder.", "Investor Pitch"),
 ("upkeep-financial-forecasting-views-deck", "Financial Forecasting Deck: Charts And Scenarios", "upkeep-forecast-views", "uk5fc_", uk5_forecast.PAIRS, "How projections are shown: chart types, scenarios, horizon, per-member economics, churn, dashboard vs one-pager. Example data.", "Forecast"),
 ("upkeep-what-we-take-care-of-deck", "What We Take Care Of Deck", "upkeep-what-we-take-care-of", "uk5ww_", uk5_wwtco.PAIRS, "Remake of the smartupkeep.ai 'What We Take Care Of' section; only services the site already offers, lawn cutting as one add-on.", "Home Page"),
 ("upkeep-operator-console-deck", "UpKeep Operator Console Deck", "upkeep-operator-console", "uk5oc_", uk5_company.PAIRS, "Operator Console: the admin login where the person running UpKeep sees all member and tech info (member list/cards, member detail, tech roster and detail, search, schedule, jobs map, alerts/to-do, KPI strip, sidebar vs tabs, phone view). Desktop-first; example data, no real people.", "Operator Console"),
]
SHARE = ('<style>.mw-hshare{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;min-width:38px;padding:0;border:1px solid #E4D6C4;background:#FFFFFF;color:#1F1F1F;cursor:pointer;flex:none}'
         '.mw-hshare svg{width:18px;height:18px}footer #shareBtn{display:none!important}body.carding .mw-hshare{width:34px;height:34px;min-width:34px}@media(max-width:520px){header #sub{display:none!important}}@media(max-width:440px){header>h1{display:none!important}}</style>\n'
         '<script>(function(){function add(){var h=document.querySelector("header"),f=document.getElementById("shareBtn"),s=document.getElementById("btnSubmitTop");if(!h||!f||h.querySelector(".mw-hshare"))return;'
         'var b=document.createElement("button");b.type="button";b.className="mw-hshare mw-hover";b.setAttribute("aria-label","Share this deck and your picks");b.title="Share";'
         'b.innerHTML=\'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 12v8h14v-8"/></svg>\';'
         'b.onclick=function(){f.click()};h.insertBefore(b,s||null)}if(document.readyState!=="loading")add();else document.addEventListener("DOMContentLoaded",add)})();</script>\n')
FEEL = {"calm", "bold", "practical", "playful", "premium"}
out = []
for n, (did, name, key, pre, PAIRS, about, tag) in enumerate(DECKS):
    assert len(PAIRS) == 10, (did, len(PAIRS))
    pairs, O, add = kdeck(pre, "UpKeep")
    for gi, (grp, ask, a, b) in enumerate(PAIRS):
        oa, ob = [O(o[0], o[1], o[2], o[3] if o[3] in FEEL else "practical", o[4]) for o in (a, b)]
        add(grp, grp, oa, ob, ask)
    publish(did, name, "UpKeep", pairs, {"brands": [about, "Smart Upkeep brand: white and cream, terracotta, lagoon and jungle accents, Khand and Hind, light mode only."],
            "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": key, "deck_size": 10, "board": "upkeep", "audience": "Max",
            "example_data": "All numbers, names and reviews on cards are labeled example data or placeholders.",
            "sources": {"content": "tools/uk5_*.py", "site": "WebermanApps/smart-upkeep app.js + styles.css (read-only)" if key.endswith("take-care-of") else "drawn mockups"}},
            seed=8100 + n, n=10, first=1)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 10
    if did not in slugs:
        slugs[did] = key + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}</style>
    {SHARE}'''
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s); link_patch(os.path.join(slug, "index.html"))
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    out.append({"deckId": did, "name": name, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "tag": tag})
json.dump(out, open("/tmp/uk5_out.json", "w"), indent=1); print(json.dumps(out, indent=1))
