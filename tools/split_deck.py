#!/usr/bin/env python3
"""R113 (Max, Team Improvement round three, Oct 17 2026 20:52 ICT): split a big deck into 10-pick decks named BY THEME.
Each part is named for what is in it (its top groups/categories, e.g. "Kitchen And Storage"), never "Part One/Part Two",
never a number. Pairs are grouped by theme first (group, then category) so each part holds one or two themes.
  python3 tools/split_deck.py decks/<id>.json [--size 10] [--dry-run]
Writes decks/<id>-<theme-slug>.json per part (source deck gets status "split" + split_into[]); prints names + ids.
Pages: build each with the owner's builder / ready_shelf write_page, lock with lock_pages.py before commit.
theme_name_ok(name) is the guard; other tools can import it."""
import json, os, re, sys, collections, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD = re.compile(r"\b(part|pt|vol|volume|round)\b|\b(one|two|three|four|five|six|seven|eight|nine|ten|i{1,3}|iv|v|vi{0,3})\b\s*$|\d", re.I)
def theme_name_ok(name): return bool(name.strip()) and not BAD.search(name)
def slugify(x): return re.sub(r"[^a-z0-9]+", "-", x.lower()).strip("-")
def theme(p): return (p.get("group") or p.get("category") or "Mixed").strip()
def chunks(items, size):
    by = collections.OrderedDict()
    for p in items: by.setdefault(theme(p), []).append(p)
    parts, cur = [], []
    for th, ps in by.items():
        while ps:
            room = size - len(cur)
            if room == 0 or (cur and len(ps) > room and len(ps) <= size): parts.append(cur); cur = []; continue
            cur += ps[:room]; ps = ps[room:]
    if cur: parts.append(cur)
    return parts
def name_for(part, used):
    cats = [k for k, _ in collections.Counter(theme(p) for p in part).most_common()]
    subs = [k for k, _ in collections.Counter((p.get("category") or "").strip() for p in part).most_common() if k and k not in cats]
    for cand in [" And ".join(cats[:2]), " And ".join(cats[:1] + subs[:1]), " And ".join(subs[:2]), " And ".join(cats[:3])]:
        cand = re.sub(r"\s+", " ", re.sub(r"\d+", "", cand)).strip().title()
        if cand and theme_name_ok(cand) and cand not in used: return cand
    sys.exit(f"R113: no theme name for a part with themes {cats + subs}; give the pairs groups/categories")
def main():
    a = sys.argv[1:]; dry = "--dry-run" in a; a = [x for x in a if x != "--dry-run"]
    size = 10
    if "--size" in a: i = a.index("--size"); size = int(a[i + 1]); del a[i:i + 2]
    if not a: sys.exit(__doc__)
    src = a[0]; d = json.load(open(src)); key = "cards" if isinstance(d.get("cards"), list) else "pairs"; items = d[key]
    if len(items) <= size: print(f"{src}: {len(items)} picks, no split needed"); return
    base = re.sub(r"-\d+$", "", d.get("date") or os.path.basename(src)[:-5]); used, out = set(), []
    for part in chunks(items, size):
        nm = name_for(part, used); used.add(nm); assert theme_name_ok(nm), nm
        nd = dict(d, **{key: part, "date": f"{base}-{slugify(nm)}", "name": nm, "split_from": d.get("date"), "status": "published"})
        nd.pop("split_into", None); out.append(nd); print(json.dumps({"id": nd["date"], "name": nm, "picks": len(part)}))
    if dry: return
    for nd in out: json.dump(nd, open(os.path.join(os.path.dirname(src), nd["date"] + ".json"), "w"), indent=1, ensure_ascii=False)
    d["status"] = "split"; d["split_into"] = [x["date"] for x in out]; d["split_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    json.dump(d, open(src, "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__": main()
