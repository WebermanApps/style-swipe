#!/usr/bin/env python3
"""Ready Deck Shelf (R66, Max Oct 14 2026 19:30 ICT): 3-5 already-built 20-card decks at the top of each agent dashboard.
No launcher that builds decks on request. When a shelf deck is submitted, it is replaced by a fresh ready 20-card deck on the same topic.

Shelf file (per agent, schema kit/shelf.schema.json): {"agent":..,"updated":..,"decks":[{"id","name","url","total":20,"topic","blurb"}]}

  python3 tools/ready_shelf.py build <topic> --shelf <shelf.json> [--agent branding] [--name "Deck Name"]
      Build + publish a fresh 20-card deck for <topic> (bank topic: banks/<topic>.json) and add it to the shelf.
  python3 tools/ready_shelf.py refill <deck_id> --shelf <shelf.json> [--agent branding]
      Call AFTER a submission for <deck_id> is handled (results saved, carry_over.py record run).
      Removes <deck_id> from the shelf and puts a fresh 20-card deck on the same topic in its slot.
      Skips (R64): carried pairs go first; a reworded version is used when the carry note has one;
      a pair skipped twice is dropped.
  python3 tools/ready_shelf.py list --shelf <shelf.json>
Then commit + push style-swipe (new deck + page) and the dashboard repo (shelf.json)."""
import json, os, re, sys, random, string, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "tools"))
BASE = "https://webermanapps.github.io/style-swipe/"; N = 20
PAGES = os.path.join(ROOT, "decks", "pages.json")
def J(p, d):
    try: return json.load(open(p))
    except Exception: return d
def W(p, o): json.dump(o, open(p, "w"), indent=1, ensure_ascii=False)
def now(): return dt.datetime.now().astimezone().isoformat(timespec="seconds")

def write_page(did):
    """Standalone page <slug>/index.html for deck did (same pattern as build_wellnest_page.py)."""
    pages = J(PAGES, {})
    slug = pages.get(did) or did + "-" + "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    pages[did] = slug; W(PAGES, pages)
    s = open("index.template.html").read()
    s = s.replace("<head>", '<head>\n<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="' + did + '"</script>\n', 1)
    os.makedirs(slug, exist_ok=True); open(os.path.join(slug, "index.html"), "w").write(s)
    return BASE + slug + "/"

def topic_pairs(topic):
    """Carried skips first (R64: reworded if a rewording is noted, dropped if already skipped once before), then unused bank pairs."""
    from carry_over import _pair_defs, Q
    q = J(Q, {}); e = q.get(topic) or {}; carried = []
    for p in _pair_defs(e.get("from_deck"), e.get("unanswered") or []):
        p = json.loads(json.dumps(p))
        if p.get("carried_from"): continue  # second skip: drop
        rw = e.get("reworded") or {}
        if rw.get("id") == p.get("id"):
            p["ask"] = rw.get("q", p["ask"])
            for s, k in (("A", "a"), ("B", "b")):
                if rw.get(k, {}).get("label"): p["option" + s]["label"] = rw[k]["label"]
        p["carried_from"] = p.get("id"); p["purpose"] = "retest"; carried.append(p)
    used = J("banks/used.json", {"pairs": [], "options": []}); up, uo = set(used.get("pairs", [])), set(used.get("options", []))
    shown = set(J("shown_options.json", {"options": {}})["options"])
    bank = J(f"banks/{topic}.json", {}).get("pairs", [])
    fresh = [p for p in bank if p["id"] not in up and not ({p["optionA"]["id"], p["optionB"]["id"]} & (uo | shown))]
    return carried, fresh, e

def build(topic, shelf_path, agent, name=None, slot=None):
    from team_kit import publish
    carried, fresh, e = topic_pairs(topic)
    pairs = (carried + fresh)[:N]
    if len(pairs) < N: sys.exit(f"{topic}: only {len(pairs)} pairs available; refill the bank first (python3 tools/build_banks.py --refill)")
    k = 1
    while os.path.exists(f"decks/{topic}-ready-{k}.json"): k += 1
    did = f"{topic}-ready-{k}"; nm = name or f"{J(f'banks/{topic}.json', {}).get('name', topic.title())} Ready Deck {k}"
    bank_ids = [p["id"] for p in pairs if not p.get("carried_from")]
    publish(did, nm, pairs[0].get("app", "Branding"), json.loads(json.dumps(pairs)),
            {"submit_agent": agent, "deck_size": N, "carried": len([p for p in pairs if p.get("carried_from")]), "topic": topic,
             "shelf": True, "bank_pairs": bank_ids}, seed=k * 97 + len(topic), n=N, first=len([p for p in pairs if p.get("carried_from")]))
    assert len(J(f"decks/{did}.json", {})["pairs"]) == N
    used = J("banks/used.json", {"pairs": [], "options": []}); used["pairs"] = sorted(set(used["pairs"]) | set(bank_ids)); W("banks/used.json", used)
    if carried:
        from carry_over import Q
        q = J(Q, {}); q.pop(topic, None); W(Q, q)
    url = write_page(did)
    sh = J(shelf_path, {"agent": agent, "decks": []}); ent = {"id": did, "name": nm, "url": url, "total": N, "topic": topic,
        "blurb": f"{N} cards, ready now" + (f", {len(carried)} reworded from last time" if carried else "")}
    if slot is None: sh["decks"].append(ent)
    else: sh["decks"].insert(slot, ent)
    sh["decks"] = sh["decks"][:5]; sh["updated"] = now(); W(shelf_path, sh)
    print(f"built {did} ({N} cards) -> {url}"); return ent

def refill(did, shelf_path, agent):
    sh = J(shelf_path, None)
    if not sh: sys.exit(f"no shelf at {shelf_path}")
    i = next((i for i, d in enumerate(sh["decks"]) if d["id"] == did), None)
    if i is None: sys.exit(f"{did} is not on the shelf")
    old = sh["decks"].pop(i); W(shelf_path, sh)
    topic = old.get("topic") or J(f"decks/{did}.json", {}).get("topic") or re.sub(r"-(ready-)?\d+[a-z]?$", "", did)
    return build(topic, shelf_path, agent, slot=i)

if __name__ == "__main__":
    a = sys.argv[1:]
    def opt(k, d=None):
        if k in a: i = a.index(k); v = a[i + 1]; del a[i:i + 2]; return v
        return d
    shelf, agent, name = opt("--shelf"), opt("--agent", "branding"), opt("--name")
    if not a or not shelf: sys.exit(__doc__)
    shelf = os.path.abspath(os.path.join(os.environ.get("PWD", ROOT), shelf)) if not os.path.isabs(shelf) else shelf
    if a[0] == "build": build(a[1], shelf, agent, name)
    elif a[0] == "refill": refill(a[1], shelf, agent)
    elif a[0] == "list": print(json.dumps(J(shelf, {}), indent=1))
    else: sys.exit(__doc__)
