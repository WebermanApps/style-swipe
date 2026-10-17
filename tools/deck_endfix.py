#!/usr/bin/env python3
"""Job 4 fix (Max on phone, Oct 17 2026 19:49 ICT: "after i press submit the photos disappear and a white box cuts a lot off").
Cause: the R82 results-screen Back row (.mw-backrow, flex-basis:100%) is inserted into #main, a column flex with overflow:hidden, so it
took the whole height as an empty white box and squeezed the summary (.end, flex:1/min-height:0) into a sliver at the bottom; the
summary itself showed no pictures of the picks.
Fix (one idempotent block <!--mw-endfix-->...<!--/mw-endfix--> in index.template.html and every deck page):
 - after Submit / at the end, the page flows normally (no fixed-height box, no clipping): main/.end lose the card-fit height lock,
   the Back row is a normal-height row;
 - the summary starts with "Your Picks": a thumbnail (the same picture or drawing as on the card) + label for every chosen option.
Card view (body.carding) is untouched. Pages are locked: unlock in a chmod 700 dir under /workspace, run, relock.
Usage: python3 tools/deck_endfix.py [files...]   (default: template + all deck pages; never share-x3l9xcxc1eut/)"""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!--mw-endfix-->", "<!--/mw-endfix-->"
EXCLUDE = ("share-x3l9xcxc1eut/",)
BLOCK = START + r"""
<style id="mw-endfix-css">
html:has(body:not(.carding)),body:not(.carding){height:auto!important;min-height:100%;overflow:visible!important}
body:not(.carding) main{flex:1 0 auto!important;overflow:visible!important;min-height:0;height:auto!important}
body:not(.carding) main>.mw-backrow{flex:0 0 auto!important;flex-basis:auto!important;width:100%;max-width:760px;height:auto!important}
body:not(.carding) .end{flex:none!important;overflow:visible!important;height:auto!important;min-height:0!important;max-height:none!important}
.mw-endpicks{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin:6px 0 18px}
.mw-endpick{border:1px solid #E5E0D8;border-radius:10px;background:#FFFFFF;overflow:hidden;min-width:0}
.mw-endpick .v{background:#FAF6EE;display:flex;align-items:center;justify-content:center;max-height:200px;overflow:hidden}
.mw-endpick .v>*{width:100%}.mw-endpick .v svg,.mw-endpick .v img{width:100%!important;height:auto!important;display:block}
.mw-endpick b{display:block;font:600 15px/1.2 Khand,system-ui,sans-serif;padding:7px 9px 0;color:#0A0A0A}
.mw-aftersub .mw-unans{font:500 14px/1.3 Hind,system-ui,sans-serif!important;color:#6B6560!important;margin:-2px 0 8px!important}
.mw-endpick span{display:block;font:400 12px/1.3 Hind,system-ui,sans-serif;color:#6B6560;padding:2px 9px 9px}
</style>
<script>(()=>{
const tagOf={A:'This',B:'That',loveA:'Love',loveB:'Love',both:'Both',yes:'Keep',love:'Love',maybe:'Hold'};
function chosen(){const out=[];try{items.forEach(p=>{
  if(single){const k=picks.find(x=>x.card_id===p.id);if(k&&/^(yes|love|maybe)$/.test(k.answer)&&p.option)out.push([p.option,tagOf[k.answer]||'',p]);return}
  const k=picks.find(x=>x.pair_id===p.id);if(!k)return;const c=k.choice;
  if(c==='A'||c==='loveA')out.push([p.optionA,tagOf[c],p]);else if(c==='B'||c==='loveB')out.push([p.optionB,tagOf[c],p]);else if(c==='both'){out.push([p.optionA,'Both',p]);out.push([p.optionB,'Both',p])}})}catch(e){}return out}
function vis(o){try{const v=o.visual||{};return String((R[v.type]||(()=>''))(v,o)||'')}catch(e){return ''}}
function add(){const end=document.querySelector('#main .end');if(!end||end.querySelector('.mw-endpicks'))return;const L=chosen();if(!L.length)return;
 const h=document.createElement('h3');h.textContent='Your Picks ('+L.length+')';const g=document.createElement('div');g.className='mw-endpicks';
 L.forEach(([o,t])=>{const c=document.createElement('div');c.className='mw-endpick';const v=vis(o);c.innerHTML=(v?'<div class="v">'+v+'</div>':'')+'<b></b><span></span>';
  c.querySelector('b').textContent=o.label||'';c.querySelector('span').textContent=t;g.appendChild(c)});
 const first=end.querySelector('h2');(first||end.firstChild).after(h);h.after(g)}
try{const _se=showEnd;showEnd=function(){const x=_se.apply(this,arguments);try{add()}catch(e){}return x}}catch(e){}
/* Max Oct 17 2026 20:27 ICT: the TOP Submit sends in ONE tap at any point (also on the summary): same send as the bottom button,
   then straight to the thanks screen. No scroll, no confirm, no second tap. Unanswered picks still go, and the count shows on the thanks screen. */
function unans(){try{return unansweredIds().length}catch(e){return 0}}
function note(){const a=document.querySelector('#main .mw-aftersub');if(!a||a.querySelector('.mw-unans'))return;const n=unans();if(!n)return;
 const p=document.createElement('p');p.className='mw-unans';p.textContent=n+' of '+items.length+' picks left unanswered (sent as partial).';a.querySelector('p').after(p)}
function thanks(ok){if(document.querySelector('#main .mw-aftersub'))return note();const end=document.querySelector('#main .end');if(!end)return;
 const d=document.createElement('div');d.className='mw-aftersub mw-thanks';const p=document.createElement('p');
 p.textContent=ok?'Sent. Thanks!':'Saved. It will send when you are back online.';d.appendChild(p);end.insertBefore(d,end.firstChild);note();d.scrollIntoView({block:'start'})}
try{const tb=document.getElementById('btnSubmitTop');if(tb)tb.onclick=()=>{if(typeof deck==='undefined'||!deck||tb.disabled)return;tb.disabled=true;const r=submitResults();
 MWSubmit.send({agent:(deck.submit_agent||'branding'),app:'style-swipe',deck:deck.mix?'mix':deck.date,results:r,notes:submitNotes(),partial:r.partial,answered:picks.length,total:items.length,unanswered:r.unanswered,test:!!deck.test})
  .then(ok=>{tb.disabled=false;if(!ok&&MWSubmit.blocked){sentFloat('Password needed');return}window.__lastPartial=r;
   if(ok){try{localStorage.setItem('styleSwipe:submitted:'+deck.date,Date.now())}catch(e){}}idx=items.length;save();render();
   setTimeout(()=>thanks(ok),150);setTimeout(()=>thanks(ok),700)}).catch(()=>{tb.disabled=false})}}catch(e){}
try{let t=0;new MutationObserver(()=>{if(t)return;t=setTimeout(()=>{t=0;note()},80)}).observe(document.getElementById('main')||document.body,{childList:true,subtree:true})}catch(e){}
})();</script>
""" + END
def patch(s):
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    if "function showEnd" not in s2: return s, False
    i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    return s2, s2 != s
if __name__ == "__main__":
    os.chdir(ROOT) if not sys.argv[1:] else None
    fs = sys.argv[1:] or ["index.template.html"] + sorted(glob.glob("*/index.html"))
    n = 0
    for f in fs:
        if any(x in f for x in EXCLUDE): continue
        t = open(f, encoding="utf-8").read()
        if "const D=" in t: print("LOCKED, skipped:", f); continue
        t2, ch = patch(t)
        if ch: open(f, "w", encoding="utf-8").write(t2); n += 1
    print(f"deck_endfix: patched {n} file(s)")
