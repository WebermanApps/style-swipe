#!/usr/bin/env python3
"""Trim unsubmitted Style Swipe pair decks to DECK_SIZE pairs (strongest + most varied); cut pairs go to banks/overflow/<id>.json.
Keeps every 'check' pair (the rejected-direction rules), retests/re-asks/winners, then fills by category/group/app variety. Pair ids are kept."""
import json, sys, glob, os, collections, datetime as dt
DECK_SIZE = 20   # hard max (Max, Oct 14 2026): decks never exceed 20 pairs; shorter is fine
MAX_PAIRS = 20
KEEP_FIRST = {"check": 0, "retest": 1, "reask": 2, "winner": 3, "combo": 4}

def select(pairs, n=DECK_SIZE):
    if n > MAX_PAIRS: print(f"WARNING: {n} pairs asked; decks never exceed {MAX_PAIRS}. Trimming to {MAX_PAIRS}."); n = MAX_PAIRS
    """Return (keep, cut): the n strongest + most varied pairs in original order, and the rest."""
    if len(pairs) <= n: return list(pairs), []
    idx = list(range(len(pairs))); chosen = []
    pri = sorted([i for i in idx if pairs[i].get("purpose") in KEEP_FIRST], key=lambda i: (KEEP_FIRST[pairs[i]["purpose"]], i))
    chosen += [0] if pairs[0].get("purpose") not in KEEP_FIRST else []
    for i in pri:
        if len(chosen) < n and i not in chosen: chosen.append(i)
    seen = collections.Counter()
    def key(i): p = pairs[i]; return (p.get("category"), p.get("group"), p.get("app"))
    for i in chosen: c, g, a = key(i); seen["c", c] += 1; seen["g", g] += 1; seen["a", a] += 1
    while len(chosen) < n:
        best = min((i for i in idx if i not in chosen), key=lambda i: (seen["c", key(i)[0]], seen["g", key(i)[1]], seen["a", key(i)[2]], i))
        chosen.append(best); c, g, a = key(best); seen["c", c] += 1; seen["g", g] += 1; seen["a", a] += 1
    return [pairs[i] for i in sorted(chosen)], [pairs[i] for i in idx if i not in chosen]

def save_overflow(did, cut):
    if not cut: return
    os.makedirs("banks/overflow", exist_ok=True)
    json.dump({"deck": did, "cut_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "count": len(cut),
               "note": "Pairs cut when the deck went to 25; banks/<category>.json will absorb these.", "pairs": cut},
              open(f"banks/overflow/{did}.json", "w"), indent=1, ensure_ascii=False)

def trim(path, n=DECK_SIZE):
    d = json.load(open(path)); did = d["date"]; pairs = d.get("pairs") or []
    if len(pairs) <= n: return None
    keep, cut = select(pairs, n)
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    d["pairs"] = keep; d["deck_size"] = len(keep); d["trimmed"] = {"from": len(pairs), "to": len(keep), "at": now, "overflow": f"banks/overflow/{did}.json"}
    if isinstance(d.get("allocation"), dict): d["allocation"] = dict(collections.Counter(p["category"] for p in keep))
    if isinstance(d.get("groups"), dict): d["groups"] = dict(collections.Counter(p.get("group") for p in keep))
    if isinstance(d.get("apps"), dict): d["apps"] = dict(collections.Counter(p.get("app") for p in keep))
    if isinstance(d.get("pair_mix"), dict): d["pair_mix"] = dict(collections.Counter(p.get("purpose") or "refine" for p in keep))
    if isinstance(d.get("feeling_counts"), dict):
        d["feeling_counts"] = dict(collections.Counter(p["option" + s].get("feeling") for p in keep for s in "AB" if p["option" + s].get("feeling")))
    fr = d.get("freshness")
    if isinstance(fr, dict) and "option_slots" in fr:
        r = len(keep) * 2 / max(1, fr["option_slots"]); fr["option_slots"] = len(keep) * 2
        if "never_shown_before" in fr: fr["never_shown_before"] = round(fr["never_shown_before"] * r)
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    save_overflow(did, cut)
    return len(pairs), len(keep), len(cut)

if __name__ == "__main__":
    for p in sys.argv[1:]: print(p, trim(p))
