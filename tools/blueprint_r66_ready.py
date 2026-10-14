#!/usr/bin/env python3
"""Point Blueprint launcher.json ready at a published 20-card Style Swipe deck (R66 refill).
Usage: python3 tools/blueprint_r66_ready.py <deck-id> ["Deck Name"] [cat,cat,...]
"""
import json, sys
from pathlib import Path
ROOT = Path("/workspace/blueprint-dashboard/launcher.json")
did = sys.argv[1]
name = sys.argv[2] if len(sys.argv) > 2 else did.replace("-", " ").title()
cats = sys.argv[3].split(",") if len(sys.argv) > 3 else []
url = f"https://webermanapps.github.io/style-swipe/?date={did}"
J = json.load(open(ROOT))
J["ready"] = {"name": name, "url": url, "total": 20, "categories": [c for c in cats if c]}
json.dump(J, open(ROOT, "w"), indent=2)
print("ready ->", J["ready"])
