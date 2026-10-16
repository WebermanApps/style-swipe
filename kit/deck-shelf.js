/* Ready To Swipe shelf (R66; look spec Max Oct 14 2026 19:49 ICT from the Up Next Deck; cap 19:43 ICT).
   Top of every agent dashboard: slim swipe carousel of at most 5 ALREADY-BUILT 20-card decks (ready + pinned unfinished together).
   Label 'Ready To Swipe' + small grey 'N done today'. Card = title + category tag, thin coloured top stripe, whole card tappable,
   small 'Start' (or 'Continue, N left' when started, thin green outline). Deck Two picks (21:35 ICT): one row on wide screens, card-edge stack,
   'All Decks' link, grey pill tag, greyed 'Done' after submit, opens in a new tab, dots under the phone strip, empty state links to Deck Building. Order (v5, Oct 16 13:05): permanent, in progress (latest touched first), not started (newest first), done last; a refill keeps the slot it replaced and shows
   a green 'New' badge until opened. No icons, no time estimate. Calm empty state. Extras are queued (DeckShelf.queued(el)).
   Usage: <section data-shelf="shelf.json"></section> + this script (+ deck-shelf.css). Schema: kit/shelf.schema.json.
   Deck Building page only: data-shelf-nocap. Back-compat: launcher.json ({ready, unfinished}) also renders. */
(()=>{const CAP=5,ACC=['#C1502E','#05668D','#0B6E4F','#D4A017'];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const LS=k=>{try{return localStorage.getItem(k)}catch(_){return null}};
const today=()=>new Date().toLocaleDateString('en-CA');
const sub=d=>!!(d.id&&LS('styleSwipe:submitted:'+d.id));
const left=d=>{const t=d.total||20;let a=d.answered||0;try{const s=JSON.parse(LS('styleSwipe:'+d.id)||LS('styleSwipe:v3:'+d.id)||'null');if(s&&s.picks)a=Math.max(a,s.picks.length)}catch(_){}return Math.max(0,t-a)};
const ALL='https://webermanapps.github.io/branding-djqmb410/decks/';
const started=d=>{if((d.answered||0)>0&&!sub(d))return true;if(!d.id||LS('styleSwipe:submitted:'+d.id))return false;
 try{const s=JSON.parse(LS('styleSwipe:'+d.id)||LS('styleSwipe:v3:'+d.id)||'null');return !!(s&&s.picks&&s.picks.length)}catch(_){return false}};
const tagOf=d=>d.tag||d.category||(d.topic?String(d.topic).replace(/[-_]+/g,' ').replace(/\b\w/g,c=>c.toUpperCase()):'Deck');
const col=s=>{let h=0;for(const c of String(s))h=(h*31+c.charCodeAt(0))>>>0;return ACC[h%ACC.length]};
function base(J){if(Array.isArray(J.decks))return J.decks;const out=[];
 if(J.ready&&J.ready.url)out.push({name:J.ready.name,url:J.ready.url,total:J.ready.total||20,tag:(J.ready.categories||[])[0]});
 (J.unfinished||[]).forEach(d=>out.push({name:d.name,url:d.url,total:d.total||20,answered:d.answered||0,pinned:true}));return out}
function norm(J,o){o=o||{};const pin=[].concat(J.pinned||[],Array.isArray(J.decks)?(J.unfinished||[]):[],o.pinned||[]).map(d=>Object.assign({},d,{pinned:true}));
 const seen=new Set(),all=[];pin.concat(base(J)).forEach(d=>{if(d&&d.url&&!seen.has(d.url)){seen.add(d.url);all.push(d)}});return all}
/* Shelf sort (Max Oct 16 13:05, v5): permanent decks first, then IN PROGRESS (some answered, not done; most recently
   touched first), then NOT STARTED (current order: newest first, refills keep their slot), then DONE last.
   Progress = higher of shelf.json answered and this browser's localStorage picks (styleSwipe:<id>);
   last touched = localStorage state.updated, else shelf last_answer_at/updated/touched. Shared: DeckShelf.sortDecks(list,{isDone}). */
const st8=d=>{try{return JSON.parse(LS('styleSwipe:'+d.id)||LS('styleSwipe:v3:'+d.id)||'null')||{}}catch(_){return {}}};
const answered=d=>{const s=st8(d);return Math.max(+d.answered||0,(s.picks&&s.picks.length)||0)};
const touched=d=>{const s=st8(d);return Math.max(Date.parse(s.updated||'')||0,Date.parse(d.last_answer_at||d.touched||d.updated||'')||0)};
const isPerm=d=>d.permanent===true||d.slot==='permanent';
function sortDecks(all,o){o=o||{};const done=o.isDone||(d=>d.status==='done'||sub(d)),keep=o.keepOrder||(x=>x);
 const perm=all.filter(isPerm),rest=all.filter(d=>!isPerm(d)),dn=rest.filter(done),live=rest.filter(d=>!done(d));
 const prog=live.filter(d=>answered(d)>0&&answered(d)<(d.total||20)).map((d,i)=>[d,i]).sort((a,b)=>(touched(b[0])-touched(a[0]))||(a[1]-b[1])).map(x=>x[0]);
 const fresh=live.filter(d=>!prog.includes(d));return perm.concat(prog,keep(fresh),dn)}
function keepSlots(rest){
 const t=d=>Date.parse(d.added||d.built||'')||0,newest=rest.reduce((m,d)=>t(d)>t(m)?d:m,rest[0]);
 const out=new Array(rest.length),fixed=rest.map((d,i)=>[d,i]).filter(([d])=>d.refill&&d!==newest);
 fixed.forEach(([d,i])=>{out[i]=d});const free=rest.filter(d=>!fixed.some(([f])=>f===d)).sort((a,b)=>t(b)-t(a));
 for(let i=0;i<out.length;i++)if(!out[i])out[i]=free.shift();return out}
function order(all){return sortDecks(all,{keepOrder:keepSlots})}
function doneToday(J){const d=today();let n=(J.done||[]).filter(x=>String(x.at||'').slice(0,10)===d).length;
 if(typeof J.done_today==='number')n=Math.max(n,J.done_today);return n}
/* Deck metric (Max 20:13 ICT, final): counters/graphs/charts show ONLY decks, never swipes. 1 deck = 20 swipes; a swipe = an answered/picked card OR a skip WITH a note (skip without note does not count). One decimal only if not whole (e.g. 3.6 decks).
   Uses deck fields from swipe-stats.json when present (decks_total / decks_today / deck_days{date:n}), else computes swipes/20.
   Swipe stats (Max 19:51 ICT): header shows swipes done for this agent's decks, today AND all-time.
   Source: kit/swipe-stats.json in style-swipe (synced from /workspace/ops/submit/swipe-stats.json by tools/sync_swipe_stats.py).
   Shape: {updated, agents:{<agent>:{total:N, days:{"YYYY-MM-DD":N}}}} (also accepts {<agent>:{"YYYY-MM-DD":N}}). Missing/unknown -> hidden. */
const STATS='https://webermanapps.github.io/style-swipe/kit/swipe-stats.json';
function statsFor(S,agent){if(!S||!agent)return null;const a=(S.agents||S)[agent]||{};if(typeof a!=='object')return null;
 const days=a.days||a.daily||Object.fromEntries(Object.entries(a).filter(([k,v])=>/^\d{4}-\d{2}-\d{2}$/.test(k)&&typeof v==='number'));
 const tz=S.tz||'Asia/Bangkok';let d;try{d=new Date().toLocaleDateString('en-CA',{timeZone:tz})}catch(_){d=today()}
 const total=typeof a.total==='number'?a.total:typeof a.all_time==='number'?a.all_time:Object.values(days).reduce((x,y)=>x+(+y||0),0);
 const dd=a.deck_days||a.decks_days, dt=typeof a.decks_today==='number'?a.decks_today:dd&&typeof dd[d]==='number'?dd[d]:null;
 const dT=typeof a.decks_total==='number'?a.decks_total:typeof a.decks_all_time==='number'?a.decks_all_time:null;
 return {today:dt!=null?dt:+(days[d]||0)/20,total:dT!=null?dT:total/20}}
const fmtDecks=n=>String(Math.floor(n+1e-9));
function paintStats(box,J){const st=box.querySelector('.ds-stats');if(!st)return;
 fetch((box.dataset.stats||J.stats_url||STATS)+'?'+Date.now()).then(r=>r.ok?r.json():null).then(S=>{const v=statsFor(S,J.agent);if(!v)return;
  st.textContent='';const f=(n,l)=>{const s=el('span','ds-stat');s.append(el('b','',fmtDecks(n)),el('span','',l));return s};
  st.append(f(v.today,(fmtDecks(v.today)==='1'?'deck':'decks')+' today'),f(v.total,(fmtDecks(v.total)==='1'?'deck':'decks')+' all-time'));st.hidden=false}).catch(()=>{})}
function render(box,J,o){o=o||{};J=J||{};const all=order(norm(J,o)),cap=(o.nocap||box.hasAttribute('data-shelf-nocap'))?all.length:CAP,decks=all.slice(0,cap);
 box._dsQueued=all.slice(cap);box.textContent='';box.classList.add('ds-sec');box.id=box.id||'ready-to-swipe';
 const h=el('div','ds-head');h.append(el('h2','','Ready To Swipe'));const n=doneToday(J);if(n)h.append(el('span','ds-done',n+' done today'));const st=el('div','ds-stats');st.hidden=true;h.append(st);const allU=box.dataset.all||J.all_url||ALL;if(!box.hasAttribute('data-shelf-nocap')){const al=el('a','ds-all','All Decks');al.href=allU;h.insertBefore(al,st)}box.append(h);paintStats(box,J);
 if(!decks.length){const p=el('p','ds-empty','All caught up. New decks are on the way. ');const l=el('a','','Deck Building');l.href=allU;p.append(l);box.append(p);return}
 const g=el('div','ds-strip');g.setAttribute('role','list');
 decks.forEach(d=>{const a=el('a','ds-card');a.href=d.url;a.setAttribute('role','listitem');const tag=tagOf(d),s=started(d);a.style.setProperty('--ds-c',d.color||col(tag));
  const dn=sub(d);if(dn){a.classList.add('ds-donecard');a.setAttribute('aria-disabled','true')}else if(s)a.classList.add('ds-started');a.target='_blank';a.rel='noopener';
  const fresh=!dn&&d.refill&&!s&&!LS('ds-opened:'+(d.id||d.url));if(fresh)a.append(el('span','ds-new','New'));
  a.append(el('b','ds-name',d.name||'Deck'),el('span','ds-tag',tag),el('span','ds-go',dn?'Done':s?'Continue, '+left(d)+' left':'Start'));
  a.addEventListener('click',()=>{try{localStorage.setItem('ds-opened:'+(d.id||d.url),'1')}catch(_){}});g.append(a)});
 box.append(g);if(decks.length>2){const dt=el('div','ds-dots');dt.setAttribute('aria-hidden','true');decks.forEach((_,i)=>dt.append(el('i',i?'':'on')));box.append(dt);
  g.addEventListener('scroll',()=>{const w=g.scrollWidth-g.clientWidth,k=w>0?Math.round(g.scrollLeft/w*(decks.length-1)):0;[...dt.children].forEach((x,i)=>x.className=i===k?'on':'')},{passive:true})}}
function init(){document.querySelectorAll('[data-shelf],[data-launcher]').forEach(b=>{if(b.dataset.dsDone)return;b.dataset.dsDone=1;
 fetch((b.dataset.shelf||b.dataset.launcher)+'?'+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>render(b,{decks:[]}))})}
window.DeckShelf={render,CAP,sortDecks,answered,touched,VERSION:5,queued:b=>b._dsQueued||[]};window.DeckLauncher=window.DeckLauncher||{render};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
