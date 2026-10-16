#!/usr/bin/env python3
"""Deck look (Max rule Oct 15 2026 13:03 ICT, overrides Oct 14 cream #FDFBF6): deck pages look like the dashboards.
White page, light beige (#FAF6EE / #e3ddd2) accents on header band, Notes, progress and selected states. All decks, WellNest included.
Tokens from kit/dash-theme.css. Colours only. Injects/replaces the <!--mw-white--> block before </head> in the template and every deck page.
  python3 tools/deck_white.py            # template + all <slug>/index.html"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CSS = """<!--mw-white--><style id="mw-white">
/* Deck look = dashboards (Max, Oct 15 2026 13:03 ICT): white page, light beige accents. Tokens: kit/dash-theme.css. Colours only. */
:root{color-scheme:light only;--bg:#ffffff!important;--panel:#ffffff;--line:#e5e5e5;--text:#0a0a0a;--muted:#737373;--dash-beige:#FAF6EE;--dash-beige-border:#e3ddd2;--dash-primary:#171717}
html,body{background:#ffffff!important;color:#0a0a0a}
header{background:#FAF6EE!important;border-bottom:1px solid #e3ddd2!important}
.card,.stat,.opt,.pill,#noteSheet .box{background-color:#ffffff;border-color:#e5e5e5}
.vis,.v-svg{background:#ffffff!important}
.progress{background:#FAF6EE!important;border:1px solid #e3ddd2}
.progress>div{background:#171717!important}
.notebtn,#noteSheet textarea{background:#FAF6EE;border-color:#e3ddd2!important}
#noteSheet .nrow button.save{background:#171717;border-color:#171717;color:#fafafa}
.opt.sel,.opt.selected,.opt.on,.opt[aria-pressed=true],.card.sel,.card.selected,.card.chosen,.pill.on,.pill.sel{background:#FAF6EE!important;border-color:#e3ddd2!important}
.tag{background:#FAF6EE;color:#737373}
.sharebtn{background:#ffffff;border-color:#171717;color:#171717}.sharebtn:hover{background:#171717;color:#fafafa}
footer,.builtby{background:#ffffff!important;color:#737373;border-top:1px solid #e5e5e5}
</style><!--/mw-white-->"""
PAT = re.compile(r"<!--mw-white-->.*?<!--/mw-white-->\n?", re.S)
def patch(p):
    s = open(p).read()
    if "</head>" not in s: return False
    n = PAT.sub("", s).replace("</head>", CSS + "\n</head>", 1)
    if n != s: open(p, "w").write(n); return True
    return False
if __name__ == "__main__":
    files = ["index.template.html"] + sorted(p for p in glob.glob("*/index.html") if "window.DEFAULT_DECK" in open(p).read()[:3000])
    ch = [p for p in files if patch(p)]
    print(len(files), "files,", len(ch), "changed"); [print(" ", p) for p in ch]
