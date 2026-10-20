#!/usr/bin/env python3
"""Job C builder (Oct 17 2026 evening, Branding): same engine as build_followups_1017.py, for the round-three follow-on decks in
tools/fu1017_round3.py (3 Max's Picks decks on the Branding board + 10 queued UpKeep decks). R105 captions are guarded; pages are
written UNLOCKED and must be locked (security/pagelock/lock_pages.py) before commit. Output list: queue/round3-1017-out.json.
Original header follows.
Follow-on decks for every deck Max swiped on Oct 17 2026 ICT (Branding Agent; Max 14:59 ICT: "if i swiped on anything today,
make sure a new deck is built with the same type of content"). One follow-on per swiped deck: same topic, format and board,
10 picks (R86), fresh deeper questions from his picks, skipped pairs re-asked in new wording, answered pairs never repeated
(finish() asserts no option id was shown before). Content modules: tools/fu1017_*.py (each defines DECKS).
Page: R89 deck look (white page, 10px card corners), header Share (uk5 pattern), Back + jump list + Notes + This/Both/Love/That/Neither
from index.template.html, chat to the owning agent (submit_to), Built by Machan footer. Pages are written UNLOCKED: lock before commit.
usage: build_round3_1017.py fu1017_round3 [deck_id ...]   -> prints JSON list to stdout and writes queue/round3-1017-out.json"""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, re, string, secrets, importlib, datetime
from team_kit import deck as kdeck, publish
from agent_links import patch as link_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SL = "queue/round3-1017-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns); SHARE = ns["SHARE"]
FEEL = {"calm", "bold", "practical", "playful", "premium"}
REQ = "Max Oct 17 2026 (Job 6): follow-up decks from today's results; 10 picks, Notes, light background, R105 captions, New badge, descriptive names; R110 for UpKeep"
import caption_rule
mod = importlib.import_module(sys.argv[1]); only = set(sys.argv[2:])
outf = "queue/round3-1017-out.json"; out_all = json.load(open(outf)) if os.path.exists(outf) else []
out = []
for n, D in enumerate(mod.DECKS):
    did = D["id"]
    if only and did not in only: continue
    P = D["pairs"]; assert len(P) == 10, (did, len(P))
    pairs, O, add = kdeck(D["prefix"], D["app"])
    for gi, (grp, ask, a, b) in enumerate(P):
        oa, ob = [O(o[0], o[1], o[2], o[3] if o[3] in FEEL else "practical", o[4]) for o in (a, b)]
        for o in (a, b):
            assert len(o[1]) <= 34, ("label too long", o[1]); assert len(o[2]) <= 62, ("desc too long", o[2])
        add(grp, grp, oa, ob, ask)
        if len(D["pairs"][gi]) > 4: pass
    caption_rule.guard(pairs, did)
    import re as _re; assert not _re.search(r"thai|thailand|bangkok", json.dumps(pairs), _re.I), "R110"
    meta = {"brands": [D["about"]] + D.get("brands", []), "submit_agent": D["agent"], "submit_to": D["submit_to"], "topic": D["topic"], "deck_size": 10,
            "board": D["board"], "audience": "Max", "requested": True, "request": REQ, "follow_on_of": D["follows"],
            "reasked_skips": D.get("reasked", []), "example_data": "All numbers, names and reviews on cards are labeled example data or placeholders.",
            "sources": {"content": f"tools/{sys.argv[1]}.py", "picks": "ops/submit/inbox/" + D["agent_inbox"]}}
    publish(did, D["name"], D["app"], pairs, meta, seed=9300 + n, n=10, first=10)
    dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 10
    if D.get("bank_ids"):
        keymap = {x[2][0]: bid for x, bid in zip(P, D["bank_ids"])}
        for pr in dj["pairs"]:
            hit = [bid for k, bid in keymap.items() if pr["optionA"]["id"].endswith(k)]; assert len(hit) == 1, pr["optionA"]["id"]; pr["bank_id"] = hit[0]
        json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    if did not in slugs:
        slugs[did] = D["slug_key"] + "-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]
    HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}</style>
    {SHARE}'''
    if D.get("head_extra") == "wellnest":
        _h = open("tools/build_wn_tea.py").read(); _n = {}; exec(_h[_h.index("def head("):_h.index("SL = ")], _n)
        _x = _n["head"](did); HEAD += "\n" + _x[_x.index("<script>(function(){var ID="):]
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1).replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11")
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    rec = {"deckId": did, "name": D["name"], "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "agent": D["agent"], "board": D["board"],
           "topic": D["topic"], "tag": D["tag"], "follows": D["follows"], "summary": D["summary"], "added": dj["generated_at"], "max_picks": D.get("max_picks", False)}
    out.append(rec); out_all = [r for r in out_all if r["deckId"] != did] + [rec]
json.dump(out_all, open(outf, "w"), indent=1); print(json.dumps(out, indent=1))
