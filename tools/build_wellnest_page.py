#!/usr/bin/env python3
"""Standalone pages for WellNest decks (usage: build_wellnest_page.py [deck_id]): <slug>/index.html (same app via <base href="../">)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PAGES = {"wellnest-brand": "wellnest-brand-jxhiif", "wellnest-brand-round-two": "wellnest-brand-r2-qlpkxs3t"}
DID = sys.argv[1] if len(sys.argv) > 1 else "wellnest-brand"; SLUG = PAGES[DID]
HEAD = r'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="''' + DID + '''"</script>
'''
BODY = ''
s = open(os.path.join(ROOT, "index.template.html")).read()
s = s.replace("<head>", "<head>\n" + HEAD, 1)
i = s.rindex("</body>"); s = s[:i] + BODY + s[i:]
os.makedirs(os.path.join(ROOT, SLUG), exist_ok=True)
open(os.path.join(ROOT, SLUG, "index.html"), "w").write(s); print("wrote", SLUG)
