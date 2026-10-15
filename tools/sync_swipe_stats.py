#!/usr/bin/env python3
"""Publish swipe counts for the Ready To Swipe header (Max 19:51 ICT): copy /workspace/ops/submit/swipe-stats.json
(per agent per day swipe counts, built by Grok Bot) to kit/swipe-stats.json, normalised to
{updated, tz, agents:{<agent>:{total, days:{YYYY-MM-DD:N}}}}. Counts only, nothing else is copied.
Run after the stats file changes (e.g. from the Submissions routine), then commit + push kit/swipe-stats.json.
If the source is missing, nothing is written and the shelf keeps the stats line hidden."""
import json, os, sys, re
SRC = "/workspace/ops/submit/swipe-stats.json"; DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kit", "swipe-stats.json")
if not os.path.exists(SRC): sys.exit(f"{SRC} not there yet; shelf stats stay hidden")
j = json.load(open(SRC)); A = j.get("agents", j); out = {}
for ag, v in A.items():
    if not isinstance(v, dict): continue
    days = v.get("daily") or v.get("days") or {k: n for k, n in v.items() if re.match(r"^\d{4}-\d{2}-\d{2}$", k)}
    days = {k: int(n.get("swipes", n.get("count", 0)) if isinstance(n, dict) else n) for k, n in days.items()}
    out[ag] = {"total": int(v.get("all_time", v.get("total", sum(days.values())))), "days": days, **{k: v[k] for k in ("decks_today","decks_total","deck_days") if k in v}}
json.dump({"updated": j.get("updated"), "tz": "Asia/Bangkok", "agents": out}, open(DST, "w"), indent=1)
print("wrote", DST, len(out), "agents")
# Apps Home deck counter (Oct 15 2026): rebuild kit/deck-counts.json (whole decks per agent per ICT day) on every sync.
import subprocess; subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_counts.py")], check=False)
