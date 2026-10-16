#!/usr/bin/env python3
"""R82 (Max, Oct 16 2026): every deck has Back and jump-to-answered.
Injects one idempotent block <!--mw-back-->...<!--/mw-back--> into index.template.html and every deck page.
 - Back button (always visible above the vote buttons, disabled on card 1): previous card, earlier pick + note highlighted;
   a new pick replaces the old one (engine choose()/answer() already filter by pair/card id) -> no duplicates.
 - Keys: Backspace, Shift+Left or Alt+Left = Back (plain Left stays 'This'; Z still = Undo).
 - Tap the 'n / N' counter: compact list of answered cards, tap one to jump there.
 - Results screen gets a Back button (to the last card) and the same list.
Love, Notes, Share, submit and saved progress unchanged. Pages are locked: unlock, run, relock.
Usage: python3 tools/deck_back.py [files...]   (default: template + all deck pages; never share-x3l9xcxc1eut/)"""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
START, END = "<!--mw-back-->", "<!--/mw-back-->"
EXCLUDE = ("share-x3l9xcxc1eut/",)
BLOCK = START + r"""
<style>
.mw-backrow{display:flex;align-items:center;gap:10px;width:100%;margin:0 0 8px;flex-basis:100%}
.mw-back{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:48px;min-width:112px;padding:0 18px;background:#FFFFFF;color:#0A0A0A;border:1.5px solid #0A0A0A;border-radius:0!important;font:600 17px/1 Khand,system-ui,sans-serif;letter-spacing:.04em;text-transform:uppercase;cursor:pointer}
.mw-backrow .mw-back{flex:0 0 auto!important;width:auto!important;max-width:none!important;min-width:120px!important;min-height:48px!important;background:#FFFFFF!important;color:#0A0A0A!important;box-shadow:none!important}
.mw-back:hover:not(:disabled){background:#FAF6EE}.mw-back:disabled{opacity:.35;cursor:default}
.mw-back svg{width:16px;height:16px}
.mw-backhint{font:400 13px/18px Hind,system-ui,sans-serif;color:#6B6560}
.mw-count{cursor:pointer;text-decoration:underline;text-decoration-color:#d9d1c3;text-underline-offset:3px;min-height:28px}
.mw-prev{margin:8px 0 0;padding:8px 12px;background:#FAF6EE;border:1px solid #e3ddd2;border-left:3px solid #C8643F;font:400 14px/20px Hind,system-ui,sans-serif;color:#0A0A0A}
.mw-prev b{font-family:Khand,system-ui,sans-serif;font-weight:600;font-size:15px}
.opt.mw-was{outline:3px solid #C8643F;outline-offset:-3px;background:#FFF8F2}
.mw-jump{position:fixed;inset:0;z-index:9998;background:rgba(10,10,10,.28);display:flex;align-items:flex-end;justify-content:center}
.mw-jump>div{background:#FFFFFF;width:min(560px,100%);max-height:70vh;overflow:auto;border:1px solid #e3ddd2;border-radius:0;padding:12px 14px 16px}
.mw-jump h3{font:600 20px/24px Khand,system-ui,sans-serif;margin:4px 0 8px;display:flex;justify-content:space-between;align-items:center}
.mw-jump h3 button{font:600 14px Hind,sans-serif;background:none;border:1.5px solid #0A0A0A;border-radius:0;min-height:40px;padding:0 14px;cursor:pointer}
.mw-jump a{display:flex;gap:10px;align-items:baseline;padding:10px 4px;min-height:44px;box-sizing:border-box;border-top:1px solid #e3ddd2;color:#0A0A0A;text-decoration:none;font:400 14px/19px Hind,system-ui,sans-serif;cursor:pointer}
.mw-jump a:hover{background:#FAF6EE}.mw-jump a span.n{font:600 15px Khand,sans-serif;color:#6B6560;min-width:26px}.mw-jump a span.c{margin-left:auto;font-weight:600;color:#C8643F;white-space:nowrap}
.mw-jump p{font:400 14px Hind,sans-serif;color:#6B6560}
@media(min-width:900px){.mw-jump{align-items:center}}
</style>
<script>(()=>{
const ARW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="square" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>';
const LBL={A:'This',B:'That',both:'Both',neither:'Neither',skip:'Skipped',loveA:'Love This',loveB:'Love That',yes:'Keep',no:'Pass',maybe:'Hold',love:'Love'};
const pid=p=>p&&p.id, pickOf=id=>picks.find(x=>(single?x.card_id:x.pair_id)===id);
const nAns=()=>items.filter(p=>pickOf(p.id)).length;
function back(){if(!deck)return;if(document.querySelector('.mw-jump'))return;if(typeof endView!=='undefined'&&endView){idx=Math.max(0,items.length-1)}else{if(idx<=0)return;idx--}try{setLove(false)}catch(_){}save();render()}
function jump(i){document.querySelectorAll('.mw-jump').forEach(e=>e.remove());idx=i;try{setLove(false)}catch(_){}save();render()}
function list(){document.querySelectorAll('.mw-jump').forEach(e=>e.remove());const w=document.createElement('div');w.className='mw-jump';
 const rows=items.map((p,i)=>{const k=pickOf(p.id);if(!k)return '';const c=single?k.answer:k.choice;return `<a data-i="${i}"><span class="n">${i+1}</span><span>${esc(p.ask||(single?(p.option&&p.option.label):p.category)||'')}</span><span class="c">${esc(LBL[c]||c)}</span></a>`}).join('');
 w.innerHTML=`<div role="dialog" aria-label="Answered cards"><h3>Answered ${nAns()} of ${items.length}<button type="button">Close</button></h3>${rows||'<p>No answers yet.</p>'}</div>`;
 w.onclick=e=>{const a=e.target.closest('a[data-i]');if(a)return jump(+a.dataset.i);if(e.target===w||e.target.closest('h3 button'))w.remove()};document.body.appendChild(w)}
function row(c){if(!c)return;let r=c.querySelector('.mw-backrow');if(!r){r=document.createElement('div');r.className='mw-backrow';r.innerHTML=`<button type="button" class="mw-back" title="Back (Backspace / Shift+Left)">${ARW}<span>Back</span></button><span class="mw-backhint"></span>`;r.querySelector('button').onclick=back;c.insertBefore(r,c.firstChild)}
 r.querySelector('button').disabled=idx<=0;r.querySelector('.mw-backhint').textContent=nAns()?nAns()+' of '+items.length+' answered':''}
function deco(){if(!deck)return;row(document.getElementById('controls'));row(document.getElementById('controls3'));
 const card=document.getElementById('card');if(!card||idx>=items.length)return;const p=items[idx];
 card.querySelectorAll('.cat .pill').forEach(s=>{if(/^\s*\d+\s*\/\s*\d+\s*$/.test(s.textContent)){s.classList.add('mw-count');s.setAttribute('role','button');s.title='Answered cards';s.onclick=e=>{e.stopPropagation();list()}}});
 const k=pickOf(p.id);if(!k)return;const c=single?k.answer:k.choice,ch=String(c).replace('love','');
 if(!single)card.querySelectorAll('.opt').forEach(o=>{if(o.dataset.side===ch||c==='both')o.classList.add('mw-was')});
 const n=(typeof noteOf==='function'&&noteOf(p.id))||k.note||'';const d=document.createElement('div');d.className='mw-prev';
 d.innerHTML=`<b>Your earlier pick: ${esc(LBL[c]||c)}</b>${n?' · Note: '+esc(n):''}<br><span style="color:#6B6560">Tap a new answer to replace it.</span>`;const h=card.querySelector('h2');(h||card).after(d)}
const _r=render;render=function(){const x=_r.apply(this,arguments);try{deco()}catch(e){}return x};
const _e=showEnd;showEnd=function(){const x=_e.apply(this,arguments);try{const m=document.getElementById('main');if(m&&!m.querySelector('.mw-backrow')){const r=document.createElement('div');r.className='mw-backrow';r.style.margin='12px 0';r.innerHTML=`<button type="button" class="mw-back">${ARW}<span>Back</span></button><button type="button" class="mw-back" style="min-width:0">Answered ${nAns()} of ${items.length}</button>`;const b=r.querySelectorAll('button');b[0].onclick=back;b[1].onclick=list;m.insertBefore(r,m.firstChild)}}catch(e){}return x};
document.addEventListener('keydown',e=>{const t=e.target;if(!deck||(t&&/^(TEXTAREA|INPUT|SELECT)$/.test(t.tagName)))return;const ns=document.getElementById('noteSheet');if(ns&&ns.classList.contains('on'))return;
 if(e.key==='Escape'&&document.querySelector('.mw-jump')){document.querySelectorAll('.mw-jump').forEach(x=>x.remove());return}
 if(e.key==='Backspace'||(e.key==='ArrowLeft'&&(e.shiftKey||e.altKey))){e.preventDefault();e.stopImmediatePropagation();back()}},true);
window.MWBack={back,jump,list};if(deck&&document.getElementById('card'))deco();
})();</script>
""" + END
def patch(p):
    if p.startswith(EXCLUDE): return False
    s = open(p).read()
    if 'id="controls"' not in s or "function choose(" not in s: return False
    s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    s2 = s2.replace('title="Backspace / Z"', 'title="Z: undo"')
    i = s2.rindex("</body>"); s2 = s2[:i] + BLOCK + "\n" + s2[i:]
    if s2 != s: open(p, "w").write(s2); return True
    return False
if __name__ == "__main__":
    files = sys.argv[1:] or (["index.template.html", "index.html"] + sorted(glob.glob("*/index.html")))
    ch = [f for f in files if os.path.exists(f) and patch(f)]
    print(len(ch), "pages updated")
