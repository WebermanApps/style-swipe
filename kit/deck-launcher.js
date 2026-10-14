/* Deck Launcher (R66). Usage: <div data-launcher="launcher.json"></div> + this script (+ ../submit.js for MWSubmit).
   Shows: Ready deck (Open) if one is waiting, else category picker + Request (20 cards across chosen categories).
   Unfinished decks (R63) pinned beside it. Request goes through MWSubmit.send -> ops/submit/inbox/<agent>. */
(()=>{const TOTAL=20;
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const split=n=>{const b=Math.floor(TOTAL/n),r=TOTAL%n;return Array.from({length:n},(_,i)=>b+(i<r?1:0))};
function loadSubmit(){return window.MWSubmit?Promise.resolve(window.MWSubmit):new Promise(res=>{const s=document.createElement('script');
 s.src='https://webermanapps.github.io/style-swipe/submit.js';s.onload=()=>res(window.MWSubmit);s.onerror=()=>res(null);document.head.append(s)})}
function render(box,J){box.textContent='';box.classList.add('dl-sec');box.id=box.id||'deck-launcher';
 const agent=J.agent,cats=(J.categories||[]).slice(0,5),un=J.unfinished||[],key='dl-req-'+agent;
 const main=el('div','dl-main');box.append(main);
 main.append(el('h2','',J.ready?'Your Next Deck':'Open a New Deck'));
 if(J.ready&&J.ready.url){const r=el('div','dl-ready');r.append(el('span','dl-pill','Ready'),el('span','dl-rname',J.ready.name||'Fresh Deck'),
   el('span','dl-meta',(J.ready.total||TOTAL)+' cards'+(J.ready.categories?' · '+J.ready.categories.join(', '):'')));
  const a=el('a','dl-btn','Open');a.href=J.ready.url;r.append(a);main.append(r)}
 else{const pend=(()=>{try{return JSON.parse(localStorage.getItem(key)||'null')}catch(_){return null}})();
  const st=el('p','dl-state');
  if(pend&&Date.now()-pend.t<864e5){st.textContent='Requested, your deck will appear here.';st.classList.add('on');main.append(st)}
  const g=el('div','dl-cats');const sel=new Set();
  const btn=el('button','dl-btn','Request Deck');btn.type='button';btn.disabled=true;
  const info=el('p','dl-meta','Pick one or more. 20 cards split across them.');
  const upd=()=>{btn.disabled=!sel.size;if(sel.size){const s=split(sel.size),ids=cats.filter(c=>sel.has(c.id));info.textContent=ids.map((c,i)=>c.label+' '+s[i]).join(' · ')+' = 20 cards'}else info.textContent='Pick one or more. 20 cards split across them.'};
  cats.forEach(c=>{const b=el('button','dl-cat');b.type='button';b.setAttribute('aria-pressed','false');b.append(el('b','',c.label),el('span','',c.blurb||''));
   b.onclick=()=>{sel.has(c.id)?sel.delete(c.id):sel.add(c.id);b.setAttribute('aria-pressed',sel.has(c.id));upd()};g.append(b)});
  main.append(g,info,btn);
  btn.onclick=async()=>{btn.disabled=true;btn.textContent='Sending';const ids=cats.filter(c=>sel.has(c.id)),s=split(ids.length);
   const req={type:'deck-request',agent,categories:ids.map((c,i)=>({id:c.id,label:c.label,cards:s[i]})),total:TOTAL};
   const S=await loadSubmit();let ok=false;
   if(S)ok=await S.send({agent,app:'deck-launcher',deck:'deck-request',results:req,notes:'',partial:false,answered:0,total:TOTAL});
   if(ok){localStorage.setItem(key,JSON.stringify({t:Date.now()}));st.textContent='Requested, your deck will appear here.';st.classList.add('on');main.insertBefore(st,g);btn.textContent='Requested'}
   else{btn.disabled=false;btn.textContent='Request Deck';st.textContent=S&&S.blocked?'Password needed to send.':'Could not send. Try again.';st.classList.add('on');main.insertBefore(st,g)}}}
 if(un.length){const p=el('div','dl-unf');p.append(el('h3','','Unfinished'));
  un.slice(0,3).forEach(d=>{const a=el('a','dl-urow');a.href=d.url;a.append(el('span','dl-rname',d.name),el('span','dl-meta',(d.answered||0)+' / '+(d.total||TOTAL)));p.append(a)});box.append(p)}
 else box.classList.add('solo')}
function init(){document.querySelectorAll('[data-launcher]').forEach(b=>fetch(b.dataset.launcher+'?'+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{}))}
window.DeckLauncher={render};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
