#!/usr/bin/env python3
"""Crisp pass (Oct 14 2026): sync the crisp CSS from index.template.html into built pages (index.html + */index.html) without re-rendering them.
Drops the idle will-change on .card and inserts the '/* crisp pass' style block before the last </style> in <head>. Idempotent."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(ROOT, "index.template.html")).read()
a = T.index("\n/* crisp pass (Oct 14)"); BLK = T[a:T.index("</style>", a)]
OLD = "transition:transform .25s ease, opacity .25s;will-change:transform;overflow:hidden}"
NEW = "transition:transform .25s ease, opacity .25s;overflow:hidden}\n.card.dragging{will-change:transform}"
for p in [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(ROOT, "*", "index.html"))):
    s = open(p).read()
    if OLD not in s and "/* crisp pass (Oct 14)" not in s: continue
    s0 = s; s = s.replace(OLD, NEW)
    if "/* crisp pass (Oct 14)" in s:
        i = s.index("\n/* crisp pass (Oct 14)"); s = s[:i] + s[s.index("</style>", i):]
    he = s.index("</head>"); i = s.rindex("</style>", 0, he); s = s[:i] + BLK + s[i:]
    if s != s0: open(p, "w").write(s); print("patched", os.path.relpath(p, ROOT))
