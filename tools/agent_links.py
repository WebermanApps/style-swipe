#!/usr/bin/env python3
"""Deck page links per owning agent (Oct 14 2026).
Injects one idempotent block into index.template.html and every deck page (<slug>/index.html with #decksLink):
 - header 'Deck Building' link, summary 'Back to Deck Building' and 'Submit To <Agent>' follow deck.submit_agent
   (map in kit/agent-dashboards.json, from ops/apps-home/agents.d; unknown -> Branding);
 - after a Submit is sent: a big 'Return to <board>' button at the top of the summary.
 R104 (Oct 17 2026): back/return links are history-first (kit/mw-back.js, data-mw-back=<owner board> is only the fallback);
   the owner-board URL is no longer forced onto #backToDecks (only the header 'Deck Building' nav link keeps a fixed href).
Deck content is not touched. Usage: python3 tools/agent_links.py   (re-run after changing kit/agent-dashboards.json)"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()  # fail build if card-media max-height:100% returns
import json, os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
M = json.load(open("kit/agent-dashboards.json"))
START, END = "<!--mw-agentlinks-->", "<!--/mw-agentlinks-->"
JS = r"""<style>.mw-aftersub{margin:0 0 14px;padding:12px;border:1px solid #E5E0D8;border-radius:12px;background:#E3F1EA;text-align:center}.mw-aftersub p{margin:0 0 8px;font:600 15px/1.3 Hind,sans-serif;color:#0B6E4F}.mw-aftersub .mw-backdecks{margin:0;min-height:60px;font-size:22px}</style>
<script>(()=>{const MAP=__MAP__,NAMES=__NAMES__,FB='branding';
const ag=()=>{try{return (typeof deck!=='undefined'&&deck&&deck.submit_agent)||FB}catch(_){return FB}};
const url=()=>MAP[ag()]||MAP[FB],nm=()=>NAMES[ag()]||NAMES[FB];
const key=()=>{try{return 'styleSwipe:submitted:'+(deck&&deck.date)}catch(_){return ''}};
const mark=()=>{try{localStorage.setItem(key(),Date.now())}catch(_){}};
const sent=()=>{try{return !!localStorage.getItem(key())}catch(_){return false}};
function apply(){const u=url();const dl=document.getElementById('decksLink');if(dl&&dl.href!==u)dl.href=u;
 const bd=document.getElementById('backToDecks');if(bd){if(bd.getAttribute('data-mw-back')!==u)bd.setAttribute('data-mw-back',u);if(!bd.hasAttribute('data-mw-back')&&bd.href!==u)bd.href=u}
 const sb=document.getElementById('submitBox');if(!sb)return;const h=sb.previousElementSibling;
 if(h&&h.tagName==='H3'&&/^Submit To /.test(h.textContent)&&h.textContent!=='Submit To '+nm())h.textContent='Submit To '+nm();
 if(sb.querySelector('.mws-btn.sent'))mark();
 const host=sb.parentElement;if(sent()&&host&&!host.querySelector('.mw-aftersub')){const d=document.createElement('div');d.className='mw-aftersub';
  d.innerHTML='<p>Sent. Your answers went to '+nm()+'.</p><a class="mw-backdecks mw-hover" href="'+u+'" data-mw-back="'+u+'" data-mw-return><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg><span>Return to <span class="mw-ret-name">'+nm()+'</span></span></a>';
  host.insertBefore(d,host.firstChild);d.scrollIntoView({block:'start'})}}
const hook=()=>{const S=window.MWSubmit;if(!S||S.__mwal)return;S.__mwal=1;const o=S.send;S.send=function(){return o.apply(this,arguments).then(ok=>{if(ok)mark();return ok})}};
let t=0;new MutationObserver(()=>{if(t)return;t=setTimeout(()=>{t=0;hook();apply()},50)}).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});
addEventListener('load',()=>{hook();apply()});hook();})();</script>"""
BLOCK = START + "\n" + JS.replace("__MAP__", json.dumps(M["dash"])).replace("__NAMES__", json.dumps(M["names"])) + "\n" + END
def patch(p):
    s = open(p).read()
    if 'id="decksLink"' not in s: return False
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    if s2 != s: open(p, "w").write(s2); return True
    return False
if __name__ == "__main__":
    files = ["index.template.html", "index.html"] + sorted(glob.glob("*/index.html"))
    ch = [f for f in files if os.path.exists(f) and patch(f)]
    print(len(ch), "pages updated"); [print(" ", f) for f in ch]
