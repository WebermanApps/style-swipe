#!/usr/bin/env python3
"""Apply one-click deck removals permanently (R102, Max Oct 17 2026 19:07 ICT).

The kit (deck-shelf.js v10 / ly11) hides a removed deck at once in that browser (localStorage ds-removed:<board>:<deck id>)
and sends one MWSubmit record: app 'deck-remove', {agent, deck, results:{board, removed:true|false}}.
This script makes those removals permanent in the board's shelf.json so every device (phone + computer) agrees.

  python3 tools/apply_removals.py inbox [--dry-run] [--no-push-note]
      Reads /workspace/ops/submit/inbox/*/*.json (written by /workspace/ops/submit/pull.sh <agent>|all), keeps auth:true
      records with app 'deck-remove', takes the LATEST record per (board, deck) by sentAt, and applies it.
  python3 tools/apply_removals.py apply --board BOARD --deck DECK_ID [--undo] [--dry-run]
      Apply one record by hand.
  python3 tools/apply_removals.py records.json [--dry-run]
      JSON list of {"board","deck","removed"} records.

Board ids: '<repo>' = that board's Ready To Swipe shelf (decks[] / pinned[] / queued[] / queue[]);
'<repo>#picks' = Max's Picks on the Branding board (requested[] only). A removal on one never touches the other.
Removed: the entry moves to removed[] (shelf) or requested_removed[] (picks) with status 'removed' and removed_at. It is NEVER
added to done[], so deck counters never count it as completed. Undo (removed:false) moves it back (picks re-sorted newest first).
Idempotent: re-running with the same records changes nothing. Shelf removals run ready_shelf.fill afterwards (R97 refill).
Board clones looked up in: /workspace/rotate-20261017/<repo>, /workspace/scratch/op-rollout/<repo>, /workspace/<repo>.
After it writes, relock nothing (shelf.json is data, not a page): commit + push shelf.json in each changed board repo."""
import glob, json, os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
INBOX = "/workspace/ops/submit/inbox"
ROOTS = ["/workspace/rotate-20261017", "/workspace/scratch/op-rollout", "/workspace"]
SHELF_KEYS = ("decks", "pinned", "queued", "queue")
def now(): return dt.datetime.now().astimezone().isoformat(timespec="seconds")
def shelf_path(repo):
    for r in ROOTS:
        p = os.path.join(r, repo, "shelf.json")
        if os.path.exists(p): return p
    for p in glob.glob(f"/workspace/scratch/op-rollout/{repo}/*/shelf.json"): return p
    return None
def key(d): return d.get("id") or d.get("url")
def apply(board, deck, removed, dry=False):
    repo, _, sec = board.partition("#")
    p = shelf_path(repo)
    if not p: print(f"skip {board}/{deck}: no clone with shelf.json"); return False
    s = json.load(open(p)); ch = False; t = now()
    if sec == "picks":
        live, bin_ = s.setdefault("requested", []), s.setdefault("requested_removed", [])
        src_keys = [("requested", live)]
    else:
        bin_ = s.setdefault("removed", [])
        src_keys = [(k, s.get(k)) for k in SHELF_KEYS if isinstance(s.get(k), list)]
    if removed:
        for k, L in src_keys:
            for d in [d for d in L if key(d) == deck and not d.get("permanent")]:
                L.remove(d); e = dict(d, status="removed", removed_at=t, removed_from=k, board=board); bin_.append(e); ch = True
    else:
        for e in [e for e in bin_ if key(e) == deck]:
            bin_.remove(e); k = e.pop("removed_from", "requested" if sec == "picks" else "decks")
            e.pop("removed_at", None); e.pop("board", None); e["status"] = "open" if sec == "picks" else e.get("prev_status", "open")
            if sec != "picks": e.pop("status", None)
            s.setdefault(k, []).insert(0, e); ch = True
        if ch and sec == "picks":
            ts = lambda d: dt.datetime.fromisoformat(d.get("requested_at") or d.get("added") or "1970-01-01T00:00:00+07:00").timestamp()
            s["requested"] = sorted(s["requested"], key=lambda d: (d.get("status") == "done", -ts(d)))
    if not ch: print(f"no change {board}/{deck} removed={removed}"); return False
    print(f"{'would apply' if dry else 'applied'} {board}/{deck} removed={removed} -> {p}")
    if dry: return True
    s["updated"] = t; json.dump(s, open(p, "w"), indent=1, ensure_ascii=False)
    if sec != "picks":
        try:
            import ready_shelf; ready_shelf.fill(p)
        except SystemExit: pass
        except Exception as x: print("fill failed:", x)
    return True
def inbox_records():
    best = {}
    for f in glob.glob(os.path.join(INBOX, "*", "*.json")):
        try: j = json.load(open(f))
        except Exception: continue
        if not isinstance(j, dict) or j.get("app") != "deck-remove" or j.get("auth") is False: continue
        r = j.get("results") or {}; b, d = r.get("board"), j.get("deck")
        if not (b and d): continue
        k = (b, d)
        if k not in best or (j.get("sentAt") or "") > (best[k].get("sentAt") or ""): best[k] = {"board": b, "deck": d, "removed": r.get("removed") is not False, "sentAt": j.get("sentAt")}
    return list(best.values())
if __name__ == "__main__":
    a = sys.argv[1:]; dry = "--dry-run" in a; a = [x for x in a if x != "--dry-run"]
    if not a: sys.exit(__doc__)
    if a[0] == "inbox": recs = inbox_records()
    elif a[0] == "apply":
        o = lambda k: a[a.index(k) + 1] if k in a else None
        if not (o("--board") and o("--deck")): sys.exit(__doc__)
        recs = [{"board": o("--board"), "deck": o("--deck"), "removed": "--undo" not in a}]
    else: recs = json.load(open(a[0]))
    n = sum(bool(apply(r["board"], r["deck"], r.get("removed", True) is not False, dry)) for r in recs)
    print(f"{len(recs)} record(s), {n} change(s)")
