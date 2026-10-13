#!/usr/bin/env python3
"""Standalone page for deck wellnest-brand: wellnest-brand-jxhiif/index.html (same app via <base href="../">)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SLUG = "wellnest-brand-jxhiif"
HEAD = r'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="wellnest-brand"</script>
'''
BODY = ''
s = open(os.path.join(ROOT, "index.template.html")).read()
s = s.replace("<head>", "<head>\n" + HEAD, 1)
i = s.rindex("</body>"); s = s[:i] + BODY + s[i:]
os.makedirs(os.path.join(ROOT, SLUG), exist_ok=True)
open(os.path.join(ROOT, SLUG, "index.html"), "w").write(s); print("wrote", SLUG)
