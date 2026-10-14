#!/bin/bash
# usage: wn_series_publish.sh <deckId> ; build, commit, pull --rebase --autostash, push, update deck-queue.json
set -e; cd /workspace/style-swipe
out=$(python3 tools/build_wn_series.py "$1" | tail -1); echo "$out"
slug=$(echo "$out" | python3 -c "import json,sys;print(json.load(sys.stdin)['slug'])")
name=$(echo "$out" | python3 -c "import json,sys;print(json.load(sys.stdin)['name'])")
git add "decks/$1.json" decks/sizes.json "$slug" tools/build_wn_series.py tools/wn_series_kit.py tools/wn_series_content.py tools/wn_series_publish.sh queue/wn-series-slugs.json shown_options.json 2>/dev/null || true
git commit -qm "WellNest series: $name ($1); standalone page $slug; submit -> wellnest" || true
for i in 1 2 3; do git pull -q --rebase --autostash origin main && git push -q origin HEAD:main && break; sleep 3; done
python3 - "$1" "$slug" "$name" <<'PY'
import json,sys,datetime as dt
did,slug,name=sys.argv[1:4];f="/workspace/wellnest/deck-queue.json";d=json.load(open(f))
for e in d["decks"]:
    if e["deckId"]==did:
        e["url"]=f"https://webermanapps.github.io/style-swipe/{slug}/";e["name"]=name
        if e.get("status")!="done": e["status"]="ready"
d["updated"]=dt.datetime.now().astimezone().isoformat(timespec="seconds")
json.dump(d,open(f,"w"),indent=1,ensure_ascii=False);print("queue ok",did)
PY
