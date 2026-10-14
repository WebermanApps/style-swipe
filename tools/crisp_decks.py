#!/usr/bin/env python3
"""Crisp pass (Oct 14 2026): apply draft_svg.crisp (mockup text floor) to every inline SVG in decks/<id>.json, in place.
For decks whose builders can no longer re-run (freshness ledger asserts). Only font-size attributes change; pair ids/content/routing untouched.
usage: crisp_decks.py <deck_id> [...]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draft_svg import crisp
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def walk(o):
    if isinstance(o, dict): return {k: (crisp(v) if isinstance(v, str) and v.lstrip().startswith("<svg") else walk(v)) for k, v in o.items()}
    if isinstance(o, list): return [walk(v) for v in o]
    return o
for did in sys.argv[1:]:
    p = os.path.join(ROOT, "decks", did + ".json"); raw = open(p).read(); d = json.loads(raw)
    n = walk(d)
    if n != d:
        ln = raw.split("\n")[1] if "\n" in raw.strip() else ""; ind = (len(ln) - len(ln.lstrip(" "))) if ln else None
        open(p, "w").write(json.dumps(n, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else "")); print("crisp", did)
    else: print("unchanged", did)
