"""usage: add_dash_entry.py <id> <name> <about> <cat> <size> <url>  (edits /workspace/branding-dashboard/decks.json)"""
import json, sys, datetime as dt
f = "/workspace/branding-dashboard/decks.json"; d = json.load(open(f))
i, name, about, cat, size, url = sys.argv[1:7]
d["decks"] = [x for x in d["decks"] if x["id"] != i]
d["decks"].insert(0, {"id": i, "name": name, "about": about, "status": "wait", "order": 0, "cat": cat, "size": int(size), "featured": False, "url": url})
d["updated"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
json.dump(d, open(f, "w"), indent=1, ensure_ascii=False); print("ok", i)
