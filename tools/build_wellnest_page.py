#!/usr/bin/env python3
"""Standalone pages for WellNest decks (usage: build_wellnest_page.py [deck_id]): <slug>/index.html (same app via <base href="../">)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PAGES = {"wellnest-brand": "wellnest-brand-jxhiif", "wellnest-brand-round-two": "wellnest-brand-r2-qlpkxs3t", "folio-dashboard": "folio-dashboard-kuijvp", "wellnest-dashboard": "wellnest-dashboard-4unr90", "upkeep-board": "upkeep-board-vh7w9l", "deck-board": "deck-board-h0dwt3", "folio-dashboard-2": "folio-dashboard-details-vxmzcb", "upkeep-board-2": "upkeep-board-details-8vhbcv", "rulebook-clash": "rulebook-clash-i5odjz", "deck-board-2": "deck-board-details-vren53", "rulebook-tiebreak": "rulebook-tiebreak-madwr3", "info-gather": "info-gather-c8smzt", "security-icon": "security-icon-d44670", "agent-dashboards": "agent-dashboards-ndeqtp", "agent-dashboards-more": "agent-dashboards-more-yzbanp", "org-chart": "org-chart-b4xp08"}
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
