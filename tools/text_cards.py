"""Text cards (Oct 16 2026): when a card option has no visual, drop the empty picture box and render a clean,
centered text card (larger Khand label, Hind desc, beige #FAF3EB, square corners). Decks with pictures are unaffected.
  python3 tools/text_cards.py [files...]   idempotent patch of template + unlocked deck pages
"""
import glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "function optHtml(o,side){const v=o.visual||{};return `<div class=\"opt mw-hover ${side} fmt-${v.type||'x'}\" data-side=\"${side}\"><div class=\"vis\">${(R[v.type]||(()=>''))(v,o)}</div>"
NEW = "function optHtml(o,side){const v=o.visual||{};const vh=String((R[v.type]||(()=>''))(v,o)||'').trim();return `<div class=\"opt mw-hover ${side} fmt-${v.type||'x'}${vh?'':' novis'}\" data-side=\"${side}\">${vh?`<div class=\"vis\">${vh}</div>`:''}"
CSS = ("<style id=\"mw-text-cards\">"
       "body.carding .opt.novis{background:#FAF3EB!important;justify-content:center!important;align-items:center;text-align:center;gap:10px!important;padding:18px 14px!important}"
       "body.carding .opt.novis .side{align-self:center}"
       "body.carding .opt.novis h3{font-family:Khand,system-ui,sans-serif;font-size:clamp(20px,2.4vw,34px)!important;line-height:1.1!important;-webkit-line-clamp:4!important;max-width:28ch}"
       "body.carding .opt.novis p{font-family:Hind,system-ui,sans-serif;font-size:clamp(14px,1.3vw,19px)!important;line-height:1.35!important;-webkit-line-clamp:6!important;display:-webkit-box!important;max-width:36ch;color:#4a4540}"
       "@media (max-width:500px){body.carding .opt.novis{padding:12px 8px!important}body.carding .opt.novis h3{font-size:18px!important}body.carding .opt.novis p{font-size:13px!important}}"
       "</style>")
def patch(s):
    if OLD not in s and NEW not in s: return s, False
    t = s.replace(OLD, NEW)
    if 'id="mw-text-cards"' not in t: t = t.replace("</head>", CSS + "</head>", 1)
    return t, t != s
if __name__ == "__main__":
    fs = sys.argv[1:] or ["index.template.html"] + glob.glob("*/index.html")
    n = 0
    for f in fs:
        p = os.path.join(ROOT, f) if not os.path.isabs(f) else f
        s = open(p, encoding="utf-8").read(); t, ch = patch(s)
        if ch: open(p, "w", encoding="utf-8").write(t); n += 1
    print(f"text_cards: patched {n} file(s)")
