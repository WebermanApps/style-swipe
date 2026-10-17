"""Media max-height guard (Oct 16 2026).
Bug: percentage max-height (max-height:100%) on card media (.vis img/svg, .v-svg svg, inline <svg style="max-height:100%">)
resolves against an indefinite-height box on some desktop browsers/monitors and collapses the picture to nothing
("no photos" on desktop). Fix: no percentage max-height on media; media fills the .vis box (object-fit/viewBox meet)
with a visible floor of min(160px,28vh).
  python3 tools/media_rule.py fix [files...]   rewrite the bad rule in place (default: template, tools, decks, banks, pages)
  python3 tools/media_rule.py check [files...] exit 1 if the bad rule is present (run by tools/build_check.sh and CI)
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOOR = "min-height:min(160px,28vh)"
FIXES = [
    (".v-svg svg{max-width:100%;max-height:100%;width:auto;height:auto;display:block}",
     ".v-svg svg{max-width:100%;max-height:none;width:100%;height:auto;display:block}"),
    ("body.carding .opt .vis>*{flex:1 1 auto;min-height:0!important;max-height:100%;height:auto!important;",
     "body.carding .opt .vis>*{flex:1 1 auto;min-height:0!important;max-height:none;height:auto!important;"),
    ("body.carding .opt .vis img{width:100%!important;height:100%!important;max-height:100%;",
     "body.carding .opt .vis img{width:100%!important;height:100%!important;max-height:none!important;" + FLOOR + ";"),
    ("body.carding .opt .vis svg{max-height:100%!important}",
     "body.carding .opt .vis svg{max-height:none!important;" + FLOOR + "}"),
    ("body.carding .opt .vis .v-svg svg{width:100%!important;height:100%!important;max-height:100%!important}",
     "body.carding .opt .vis .v-svg svg{width:100%!important;height:100%!important;max-height:none!important;" + FLOOR + "}"),
    ('style="max-height:100%;max-width:100%"', 'style="max-width:100%;height:auto"'),
    ('style=\\"max-height:100%;max-width:100%\\"', 'style=\\"max-width:100%;height:auto\\"'),
]
# Any percentage max-height on a media selector or inline svg style.
BAD = re.compile(r'(?:(?:\.vis|\.v-svg|\bimg|\bsvg|\bvideo|\bpicture)[^{}<>]{0,80}\{[^{}]*max-height:\s*100%'
                 r'|<svg[^>]*style=\\?"[^"\\]*max-height:\s*100%)')
SELF = os.path.abspath(__file__)
NOT_CARD_MEDIA = "kit/projects.css"  # exact relative path only: no glob, pattern, set or substring match (Security)
def default_files():
    fs = ["index.template.html", "index.html"] + glob.glob("*/index.html") + glob.glob("tools/*.py") + glob.glob("decks/*.json") + glob.glob("banks/*.json") + glob.glob("kit/*.css")
    # kit/projects.css is the Document Center file viewer (not deck card media; Security-owned): its contained-image rule is fine there.
    fs = [f for f in fs if f != NOT_CARD_MEDIA]
    return [os.path.join(ROOT, f) for f in fs if os.path.isfile(os.path.join(ROOT, f)) and os.path.abspath(os.path.join(ROOT, f)) != SELF]
def locked(s): return "mwPagesKey" in s[:20000] and "AES-GCM" in s[:20000] and "DEFAULT_DECK" not in s
def main():
    mode, files = sys.argv[1], [os.path.abspath(f) for f in sys.argv[2:]] or default_files()
    bad, changed = [], []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if mode == "fix":
            t = s
            for a, b in FIXES: t = t.replace(a, b)
            if t != s: open(f, "w", encoding="utf-8").write(t); changed.append(f)
            s = t
        if locked(s): continue
        for m in BAD.finditer(s): bad.append(f"{os.path.relpath(f, ROOT)}: {m.group(0)[-120:]}")
    if mode == "fix": print(f"media_rule: fixed {len(changed)} file(s)")
    if bad:
        print("media_rule: FAIL - percentage max-height on card media (collapses photos on desktop):"); print("\n".join(bad[:50])); sys.exit(1)
    print(f"media_rule: OK ({len(files)} file(s) checked)")
if __name__ == "__main__": main()

def _scan(files):
    out = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if not locked(s): out += [f"{os.path.relpath(f, ROOT)}: {m.group(0)[-120:]}" for m in BAD.finditer(s)]
    return out
def guard():
    """Call at the top of any builder: fails now if the template has the bad rule, and again at exit if built output does."""
    import atexit
    b = _scan([os.path.join(ROOT, "index.template.html")])
    if b: sys.exit("media_rule: FAIL in template - " + b[0])
    def _end():
        b = _scan(default_files())
        if b: print("media_rule: FAIL after build:\n" + "\n".join(b[:20]), file=sys.stderr); os._exit(1)
    atexit.register(_end)
