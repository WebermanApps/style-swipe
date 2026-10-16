#!/usr/bin/env python3
"""Standalone pages for WellNest decks (usage: build_wellnest_page.py [deck_id]): <slug>/index.html (same app via <base href="../">)."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PAGES = {"wellnest-brand": "wellnest-brand-jxhiif", "wellnest-brand-round-two": "wellnest-brand-r2-qlpkxs3t", "folio-dashboard": "folio-dashboard-kuijvp", "wellnest-dashboard": "wellnest-dashboard-4unr90", "upkeep-board": "upkeep-board-vh7w9l", "deck-board": "deck-board-h0dwt3", "folio-dashboard-2": "folio-dashboard-details-vxmzcb", "upkeep-board-2": "upkeep-board-details-8vhbcv", "rulebook-clash": "rulebook-clash-i5odjz", "deck-board-2": "deck-board-details-vren53", "rulebook-tiebreak": "rulebook-tiebreak-madwr3", "info-gather": "info-gather-c8smzt", "security-icon": "security-icon-d44670", "agent-dashboards": "agent-dashboards-ndeqtp", "agent-dashboards-more": "agent-dashboards-more-yzbanp", "org-chart": "org-chart-b4xp08", "funnel-deck": "funnel-deck-k7r2qe", "ceo-management": "ceo-management-q4m8tz", "priorities-focus": "priorities-focus-r7k2wd", "delegation-routing": "delegation-routing-m3x9qa", "usage-cost": "usage-cost-v8n4pe", "follow-through-reporting": "follow-through-reporting-h5t6jb", "up-next-deck": "up-next-deck-u7n3xk"}
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
