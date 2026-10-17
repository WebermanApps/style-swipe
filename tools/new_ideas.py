#!/usr/bin/env python3
"""Daily New Ideas deck for Research (R101, Max Oct 17 2026 15:53 ICT). 10 this-or-that picks of things Max could build
or directions to take: spinoffs of what he built + new ideas, from tools/new_ideas_bank.py. Never repeats an idea:
queue/new-ideas-history.json records every bank key shown (and the finish() ledger blocks repeated option ids).
Name 'New Ideas: <theme>' (no numbers), random-suffix slug. Page: index.template.html kit (white page, 10px card corners,
This/Both/Love/That/Neither, Back + jump list, Notes, header Share, chat to Research, Built by Machan), mockups scaled up.
Page is written UNLOCKED: lock it (lock_pages.py on a temp copy of only the page) before commit.
usage: new_ideas.py [--dry]   -> prints the deck record JSON. When the bank runs low, add entries to new_ideas_bank.py."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets, datetime, random
from team_kit import deck as kdeck, publish
from fu1017_kit import U
from agent_links import patch as link_patch
from new_ideas_bank import BANK
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
HIST = "queue/new-ideas-history.json"
hist = json.load(open(HIST)) if os.path.exists(HIST) else {"shown": {}, "decks": []}
dry = "--dry" in sys.argv
fresh = [e for e in BANK if e[0] not in hist["shown"]]
if len(fresh) < 10: sys.exit(f"bank low: only {len(fresh)} unshown ideas; add entries to tools/new_ideas_bank.py")
# pick 10: one per theme first (variety), mix spinoff/new, then fill
rng = random.Random(); rng.shuffle(fresh); pick, seen = [], set()
for e in sorted(fresh, key=lambda e: e[2] != "new"):
    if e[1] not in seen and len(pick) < 10: pick.append(e); seen.add(e[1])
for e in fresh:
    if len(pick) < 10 and e not in pick: pick.append(e)
sp = [e[1] for e in pick if e[2] == "spinoff"]; nw = [e[1] for e in pick if e[2] == "new"]
themes = []
for th in sp[:2] + nw[:1] + sp[2:] + nw[1:]:
    if th not in themes: themes.append(th)
def short(th): return {"@AMomentInThai": "YouTube", "Smart Upkeep": "Upkeep", "Weberman Construction": "Construction"}.get(th, th)
tw = [short(x) for x in themes[:3]]
theme = f"{tw[0]}, {tw[1]} & {tw[2]}"
name = f"New Ideas: {theme}"
tslug = "-".join("".join(c for c in w.lower() if c.isalnum() or c == " ").replace(" ", "-") for w in tw)
suf = "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
did = f"new-ideas-{tslug}-{suf}"; slug = did
if dry: print(name, [p[0] for p in pick]); sys.exit()
pairs, O, add = kdeck("ni-", "Research")
for key, th, kind, ask, a, b in pick:
    opts = []
    for o in (a, b):
        assert len(o[1]) <= 34 and len(o[2]) <= 62, o[:3]
        opts.append(O(f"{key}-{o[0]}", o[1], o[2], "practical", U(th, o[3], o[4]), tags=[th, kind]))
    add(th, th, opts[0], opts[1], ask)
meta = {"brands": ["Research"], "submit_agent": "research", "topic": "new-ideas", "deck_size": 10, "board": "research", "audience": "Max",
        "rule": "R101 Daily New Ideas deck", "idea_keys": [p[0] for p in pick], "theme": theme,
        "claims": "Real claims only; no market numbers.", "sources": {"bank": "tools/new_ideas_bank.py", "history": HIST,
        "steer": ["research-dashboard topics.json decisions", "ops/agent-activity/preferences-log.md", "ops/submit/inbox/**"]}}
publish(did, name, "Research", pairs, meta, seed=secrets.randbelow(10**6), n=10)
dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 10
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns)
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}</style>
    {ns["SHARE"]}'''
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1).replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11")
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
now = dj["generated_at"]
for e in pick: hist["shown"][e[0]] = {"deck": did, "at": now, "A": e[4][1], "B": e[5][1]}
hist["decks"].append({"id": did, "name": name, "slug": slug, "at": now})
json.dump(hist, open(HIST, "w"), indent=1, ensure_ascii=False)
rec = {"id": did, "name": name, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "total": 10, "topic": "new-ideas", "added": now,
       "tag": "New Ideas", "blurb": "10 idea picks: " + ", ".join(tw), "pairs": [f'{p["optionA"]["label"]} vs {p["optionB"]["label"]}' for p in dj["pairs"]]}
print(json.dumps(rec, indent=1, ensure_ascii=False))
