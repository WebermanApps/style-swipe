"""Carry unanswered Style Swipe pairs into the next deck (Oct 13 2026 Submit-anytime rule).

A partial Submit payload carries results.unanswered (pair/card ids) plus partial/answered/total.
  python3 tools/carry_over.py record <submission.json> [--test]   # from ops/submit/inbox/branding/*.json or a raw payload
  python3 tools/carry_over.py pending [topic]                     # show what is waiting
  python3 tools/carry_over.py apply <topic> <new_deck.json>       # put carried pairs FIRST in the new deck, then clear them
Topic = deck slug without its trailing -N/letter (upkeep-7 -> upkeep, 2026-10-11b -> daily). Mix decks: topic 'mix';
unanswered mix pairs are also returned to the bank (removed from banks/used.json) so the next mix can draw them again.
test:true submissions only go to queue/carry_over.test.json, never the real queue.
In a deck builder: from carry_over import carried_first; deck['pairs'] = carried_first('upkeep', deck['pairs'])"""
import json, os, re, sys, glob
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, "queue", "carry_over.json")
QT = os.path.join(ROOT, "queue", "carry_over.test.json")
USED = os.path.join(ROOT, "banks", "used.json")

def topic_of(slug):
    if slug in ("mix",) or str(slug).startswith("mix"): return "mix"
    if re.match(r"^\d{4}-\d{2}-\d{2}", slug): return "daily"
    return re.sub(r"-\d+[a-z]?$", "", slug)

def _load(p, d):
    try: return json.load(open(p))
    except Exception: return d
def _save(p, o): os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(o, open(p, "w"), indent=1)

def _pair_defs(slug, ids):
    """Full pair/card objects for ids, from decks/<slug>.json or (mix) the banks."""
    want, out = set(ids), {}
    srcs = [os.path.join(ROOT, "decks", slug + ".json")] if slug else []
    srcs += sorted(glob.glob(os.path.join(ROOT, "banks", "*.json")))
    for f in srcs:
        j = _load(f, {})
        for p in (j.get("pairs") or j.get("cards") or []) if isinstance(j, dict) else []:
            if isinstance(p, dict) and p.get("id") in want and p["id"] not in out: out[p["id"]] = p
    return [out[i] for i in ids if i in out]

def record(path, test=False):
    it = _load(path, {}); d = it.get("data", it); r = d.get("results") or {}
    un = r.get("unanswered") or d.get("unanswered") or []
    is_test = bool(test or r.get("test") or d.get("test"))
    slug = (r.get("mix") or {}).get("id") if r.get("deck") == "mix" else (r.get("deck") or d.get("deck"))
    topic = "mix" if r.get("deck") == "mix" or d.get("deck") == "mix" else topic_of(slug or "")
    q = _load(QT if is_test else Q, {})
    q[topic] = {"from_deck": slug, "unanswered": un, "answered": r.get("answered"), "total": r.get("total"),
                "banks": r.get("unanswered_banks") or [], "saved": datetime.now().isoformat(timespec="seconds")}
    _save(QT if is_test else Q, q)
    freed = 0
    if topic == "mix" and un and not is_test and os.path.exists(USED):
        u = _load(USED, {})
        if isinstance(u, dict) and isinstance(u.get("pairs"), list):
            before = len(u["pairs"]); u["pairs"] = [x for x in u["pairs"] if x not in set(un)]; freed = before - len(u["pairs"])
            if freed: _save(USED, u)
    print(f"{'TEST ' if is_test else ''}carry-over {topic}: {len(un)} unanswered from {slug}" + (f"; {freed} returned to bank (used.json)" if topic == "mix" else ""))
    return q[topic]

def carried_first(topic, pairs, clear=True, test=False):
    q = _load(QT if test else Q, {}); e = q.get(topic)
    if not e or not e.get("unanswered"): return pairs
    carried = _pair_defs(e.get("from_deck"), e["unanswered"]); ids = {p["id"] for p in carried}
    out = carried + [p for p in pairs if p.get("id") not in ids]
    if clear: q.pop(topic, None); _save(QT if test else Q, q)
    return out

if __name__ == "__main__":
    a = sys.argv[1:]; test = "--test" in a; a = [x for x in a if x != "--test"]
    if not a: sys.exit(__doc__)
    if a[0] == "record": record(a[1], test)
    elif a[0] == "pending":
        q = _load(QT if test else Q, {}); print(json.dumps({k: v for k, v in q.items() if len(a) < 2 or k == a[1]}, indent=1))
    elif a[0] == "apply":
        f = a[2]; d = json.load(open(f)); k = "pairs" if "pairs" in d else "cards"
        n0 = len(d[k]); d[k] = carried_first(a[1], d[k], test=test); json.dump(d, open(f, "w"), indent=1)
        print(f"{a[1]}: {len(d[k]) - n0} carried pairs added first ({len(d[k])} total)")
    else: sys.exit(__doc__)
