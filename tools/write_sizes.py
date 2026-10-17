#!/usr/bin/env python3
"""Write decks/sizes.json: {deck_id: pair_count} from decks/*.json, plus bank counts.
Run from the repo root. Idempotent. Called after deck finish and bank builds."""
import json, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = os.path.join(ROOT, "decks")
BANKS = os.path.join(ROOT, "banks")
OUT = os.path.join(DECKS, "sizes.json")
SKIP_BANKS = {"index.json", "bank_ids.json", "used.json"}


def main():
    sizes = {}
    for fp in sorted(glob.glob(os.path.join(DECKS, "*.json"))):
        name = os.path.basename(fp)
        if name == "sizes.json":
            continue
        try:
            d = json.load(open(fp))
        except (json.JSONDecodeError, OSError):
            continue
        did = d.get("date") or name[:-5]
        n = len(d.get("pairs") or d.get("cards") or [])
        if n:
            sizes[did] = n
    banks = {}
    for fp in sorted(glob.glob(os.path.join(BANKS, "*.json"))):
        name = os.path.basename(fp)
        if name in SKIP_BANKS:
            continue
        try:
            d = json.load(open(fp))
        except (json.JSONDecodeError, OSError):
            continue
        slug = d.get("slug") or name[:-5]
        n = d.get("count")
        if n is None:
            n = len(d.get("pairs") or [])
        if n:
            banks[slug] = int(n)
    if banks:
        sizes["banks"] = banks
    sizes["max_pairs"] = 10   # R86 (Max Oct 17 2026 07:50 ICT): 10 picks per deck, 10 decks per shelf (was 20). Existing live decks keep their size
    sizes["default_pairs"] = 10
    sizes["shelf_cap"] = 10
    os.makedirs(DECKS, exist_ok=True)
    json.dump(sizes, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(sizes) - (1 if banks else 0)} decks, {len(banks)} banks")
    return sizes


if __name__ == "__main__":
    main()
