#!/usr/bin/env python3
"""R74 pop-up chat button on deck pages (Oct 16 2026).
Injects one idempotent block into index.template.html and every deck page (<slug>/index.html with #decksLink).
The button opens Max's chat with the agent the deck's results route to: uuid in deck.submit_to, else kit/mw-chat.js registry
by deck.submit_agent, else Branding when the deck names no agent; unknown agents get no button.
NEVER touches share-x3l9xcxc1eut/ (unlinked share page). Pages are locked: unlock the files first, run this, then relock.
Usage: python3 tools/chat_button.py [files...]   (default: template + all deck pages)"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
START, END = "<!--mw-chat-->", "<!--/mw-chat-->"
EXCLUDE = ("share-x3l9xcxc1eut/",)
BLOCK = START + r"""
<script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc13" defer></script>
<script>(()=>{let last='';function pick(){let d=null;try{d=(typeof deck!=='undefined')?deck:null}catch(_){}if(!d)return null;
 const m=String(d.submit_to||'').match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
 if(m)return {id:m[0],name:String(d.submit_to).replace(m[0],'').trim()||undefined,agent:d.submit_agent};
 return {agent:d.submit_agent||'branding'}}
function go(){if(!window.MWChat)return;const o=pick();if(!o)return;if(o.id&&!o.name&&o.agent&&MWChat.registry[o.agent])o.name=MWChat.registry[o.agent][1];
 const k=JSON.stringify(o);if(k===last)return;last=k;MWChat.mount(o)}
let n=0;const iv=setInterval(()=>{go();if(++n>40)clearInterval(iv)},500);addEventListener('load',go);})();</script>
""" + END
def patch(p):
    if p.startswith(EXCLUDE): return False
    s = open(p).read()
    if 'id="decksLink"' not in s: return False
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    if s2 != s: open(p, "w").write(s2); return True
    return False
if __name__ == "__main__":
    files = sys.argv[1:] or (["index.template.html", "index.html"] + sorted(glob.glob("*/index.html")))
    ch = [f for f in files if os.path.exists(f) and patch(f)]
    print(len(ch), "pages updated"); [print(" ", f) for f in ch]
