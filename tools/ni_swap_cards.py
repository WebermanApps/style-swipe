"""One-off (R105/R110, Oct 17 2026): swap cards on a published New Ideas deck for unshown bank ideas, built with new_ideas.py's own
fill_card/O, and reset every ask to new_ideas.r105_ask(). usage: ni_swap_cards.py <deck_id> <card#>=<bank key> ..."""
import sys, json, os
did, swaps = sys.argv[1], dict(a.split("=") for a in sys.argv[2:])
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); sys.path.insert(0, "tools")
argv = sys.argv; sys.argv = ["new_ideas.py", "--dry"]
src = open("tools/new_ideas.py").read(); g = {"__name__": "ni", "__file__": "tools/new_ideas.py"}
exec(compile(src.split("\nassert not (any(is_upkeep")[0], "new_ideas.py", "exec"), g); sys.argv = argv
bank = {e[0]: e for e in g["bank"]}; hist = g["hist"]; g["O"] = g["kdeck"]("ni-", "Research")[1]
p = f"decks/{did}.json"; d = json.load(open(p))
def key_of(pp):  # option ids are "ni-<bank key>-<option id>"; idea_keys order is not card order
    oid = pp["optionA"]["id"][3:]; return max((k for k in bank if oid.startswith(k + "-")), key=len)
keys = [key_of(pp) for pp in d["pairs"]]
for n, key in swaps.items():
    i = int(n) - 1; e = bank[key]; k, th, kind, ask, a, b = e
    assert key not in hist["shown"] and key not in keys and not g["is_thai"](e), key
    opts = [g["O"](f"{k}-{o[0]}", o[1], o[2], "practical", g["fill_card"](th, o[3], o[4]), tags=[th, kind]) for o in (a, b)]
    old = d["pairs"][i]; print(f"card {n}: {keys[i]} ({old['optionA']['label']} / {old['optionB']['label']}) -> {key} ({a[1]} / {b[1]})")
    old.update({"group": th, "category": th, "optionA": opts[0], "optionB": opts[1], "replaced": {"key": keys[i], "why": "R110 swap, Max Oct 17 2026"}})
    old.pop("ask_old", None); keys[i] = key
    hist["shown"][key] = {"deck": did, "at": d["generated_at"], "A": a[1], "B": b[1]}
for i, pp in enumerate(d["pairs"]):
    e = bank[keys[i]]; pp["ask"] = g["r105_ask"](e[1], e[3])
from collections import Counter
if isinstance(d.get("groups"), dict): d["groups"] = dict(Counter(pp["group"] for pp in d["pairs"]))
d["idea_keys"] = keys; d["signoff"] = {k: v for k, v in g["new_ideas_more"].SIGNOFF.items() if k in keys}
g["caption_rule"].guard(d["pairs"], did)
assert not (any(g["is_upkeep"](bank[k]) for k in keys) and any(g["is_thai"](bank[k]) for k in keys)), "R110"
txt = json.dumps(d, ensure_ascii=False); import re
assert not re.search(r"thai|thailand|bangkok", txt, re.I), re.findall(r".{30}(?:thai|bangkok).{30}", txt, re.I)[:3]
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); json.dump(hist, open(g["HIST"], "w"), indent=1, ensure_ascii=False)
for pp in d["pairs"]: print(" ", pp["ask"])
