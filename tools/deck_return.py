#!/usr/bin/env python3
"""R104 Return button on every deck page (Max, Oct 17 2026 19:39 ICT; Branding).
The header link #backLink becomes "<- Return to <board>": history-first via kit/mw-back.js (history.back() when Max came from a trusted
board in this tab, else ?from= / sessionStorage origin, else a trusted referrer, else the Branding board). The summary's
"Back to Deck Building" (#backToDecks) and the after-Submit button do the same and read "Return to <board>".
The R82 card Back button (previous card, .mw-backrow) is NOT touched. Share, Notes, Submit and mw-chat are untouched.
One idempotent block <!--mw-return-->...<!--/mw-return--> before </body>. Pages are locked: unlock in a chmod 700 dir under /workspace,
run, relock.  Usage: python3 tools/deck_return.py [files...]   (default: template + all deck pages; never share-x3l9xcxc1eut/)"""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!--mw-return-->", "<!--/mw-return-->"
EXCLUDE = ("share-x3l9xcxc1eut/",)
KIT = "https://webermanapps.github.io/style-swipe/kit/mw-back.js?v=mb1"
BLOCK = START + """
<style id="mw-return-css">#backLink.mw-return{gap:6px;white-space:nowrap;max-width:62vw;overflow:hidden}#backLink.mw-return .l{overflow:hidden;text-overflow:ellipsis}
@media(max-width:520px){header:has(#backLink.mw-return) h1{display:none}#backLink.mw-return{font-size:14px;padding:0 10px}}</style>
<script src=\"""" + KIT + """\"></script>
<script>(()=>{const FB='https://webermanapps.github.io/branding-djqmb410/';
const ARW='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
function ret(a,fb){if(!a||a.__mwr)return;a.__mwr=1;a.setAttribute('data-mw-back',fb);a.setAttribute('data-mw-return','');a.classList.add('mw-return');
 a.removeAttribute('target');a.innerHTML=ARW+'<span class="l">Return to <span class="mw-ret-name">Board</span></span>';if(window.mwBack)mwBack.scan()}
function run(){ret(document.getElementById('backLink'),FB);
 ['backToDecks'].forEach(i=>{const e=document.getElementById(i);if(e)ret(e,e.getAttribute('href')||FB)});
 document.querySelectorAll('.mw-aftersub a.mw-backdecks').forEach(e=>ret(e,e.getAttribute('href')||FB))}
let t=0;new MutationObserver(()=>{if(t)return;t=setTimeout(()=>{t=0;run()},60)}).observe(document.documentElement,{childList:true,subtree:true});
run();addEventListener('load',run)})();</script>
""" + END
def patch(s):
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    if 'id="backLink"' not in s2: return s, False
    i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    return s2, s2 != s
if __name__ == "__main__":
    if not sys.argv[1:]: os.chdir(ROOT)
    fs = sys.argv[1:] or ["index.template.html"] + sorted(glob.glob("*/index.html"))
    n = 0
    for f in fs:
        if any(x in f for x in EXCLUDE): continue
        t = open(f, encoding="utf-8").read()
        if "const D=" in t: print("LOCKED, skipped:", f); continue
        t2, ch = patch(t)
        if ch: open(f, "w", encoding="utf-8").write(t2); n += 1
    print(f"deck_return: patched {n} file(s)")
