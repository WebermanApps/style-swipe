#!/usr/bin/env python3
"""Whole decks completed per agent (Max Oct 15 2026, Apps Home deck counter).
One deck = one real (auth ok, non-test) Style Swipe submission with a deck id, deduped by agent+deck+ICT day,
detail-request rows excluded. Sources: submit/inbox/* (judged like swipe_stats.py) + routed.json routed/pre-routed rows.
Writes kit/deck-counts.json {updated, tz, decks:[{agent, deck, ts, day}]}; the page filters to today in ICT itself."""
import json, glob, os, sys, datetime
S = "/workspace/ops/submit"; sys.path.insert(0, S)
from auth_filter import judge
ICT = datetime.timezone(datetime.timedelta(hours=7))
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kit", "deck-counts.json")
ALIAS = {"branding.": "branding", "smart": "upkeep", "folio": "portfolio", "vision": "research", "miles": "miles-agent"}
seen = {}
def add(agent, deck, ts):
    if not deck or "detail-request" in deck or not ts: return
    agent = ALIAS.get(agent, agent); day = datetime.datetime.fromtimestamp(int(ts) / 1000, ICT).strftime("%Y-%m-%d")
    k = (agent, deck, day)
    if k not in seen or ts < seen[k]: seen[k] = int(ts)
for f in glob.glob(os.path.join(S, "inbox", "*", "*.json")):
    try: it = json.load(open(f))
    except Exception: continue
    if judge(it)[0] != "ok": continue
    d = it.get("data") if isinstance(it.get("data"), dict) else {}
    r = d.get("results") if isinstance(d.get("results"), dict) else {}
    if r.get("test") or d.get("test") or r.get("type") == "detail-request": continue
    if (d.get("app") or it.get("app")) != "style-swipe": continue
    add(os.path.basename(os.path.dirname(f)), d.get("deck") or it.get("deck"), it.get("ts"))
try:
    for v in json.load(open(os.path.join(S, "routed.json")))["ids"].values():
        if v.get("status") in ("routed", "pre-routed") and v.get("app") == "style-swipe": add(v.get("agent", ""), v.get("deck"), v.get("ts"))
except Exception as x: print("routed.json skipped:", x)
decks = [{"agent": a, "deck": dk, "day": day, "ts": ts} for (a, dk, day), ts in sorted(seen.items(), key=lambda kv: kv[1])]
json.dump({"updated": datetime.datetime.now(ICT).isoformat(timespec="seconds"), "tz": "Asia/Bangkok",
           "rule": "1 deck = 1 real Style Swipe submission, deduped per agent+deck+day", "decks": decks}, open(DST, "w"), indent=1)
today = datetime.datetime.now(ICT).strftime("%Y-%m-%d")
print("wrote", DST, len(decks), "decks;", sum(d["day"] == today for d in decks), "today")
