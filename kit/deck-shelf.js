/* Ready To Swipe shelf (R66; look spec Max Oct 14 2026 19:49 ICT from the Up Next Deck; cap 19:43 ICT).
   Top of every agent dashboard: slim swipe carousel of at most 10 ALREADY-BUILT 10-card decks (R86 Oct 17 2026; was 5 x 20) (ready + pinned unfinished together).
   Label 'Ready To Swipe' + small grey 'N done today'. Card = title + category tag, thin coloured top stripe, whole card tappable,
   small 'Start' (or 'Continue, N left' when started, thin green outline). Deck Two picks (21:35 ICT): one row on wide screens, card-edge stack,
   'All Decks' link, grey pill tag, greyed 'Done' after submit, opens in a new tab, dots under the phone strip, empty state links to Deck Building. Order (v5, Oct 16 13:05): permanent, in progress (latest touched first), not started (newest first), done last; a refill keeps the slot it replaced and shows
   a green 'New' badge until opened. No icons, no time estimate. Calm empty state. Extras are queued (DeckShelf.queued(el)).
   Usage: <section data-shelf="shelf.json"></section> + this script (+ deck-shelf.css). Schema: kit/shelf.schema.json.
   Deck Building page only: data-shelf-nocap. Back-compat: launcher.json ({ready, unfinished}) also renders.
   v9 / kit ly10 (Max via Grok Bot, Oct 17 2026 15:22 ICT, rulebook R96-R98):
   R96 a finished deck leaves the shelf right away (status done|hidden|retired|replaced|split, hidden:true, listed in done[], or submitted
       in this browser); it stays in shelf.json (done[] / status) and still counts on every deck counter (kit/deck-counts.json reads done[]).
       Replaces 'done decks show last'.
   R97 at most 10 decks per board shelf; each freed slot is filled at render time from that board's ready queue (shelf.json queued[] / queue[]),
       in queue order. Tools fill the same way when they write (style-swipe tools/ready_shelf.py fill).
   R98 every card shows a light 'New' badge until Max clicks it once (localStorage ds-opened:<deck id>), then it is gone.
   v10 / kit ly11 (Max Oct 17 2026 19:07 ICT, rulebook R102): one-click remove. Every card gets a small '×' (32px tap target, top-right);
       one click hides it at once + 'Removed · Undo' toast (~5 s), no confirm. Scoped per board: localStorage ds-removed:<board>:<deck id>,
       board = data-board / shelf.json board / first path segment of the page (Branding's Max's Picks uses '<repo>#picks').
       Sent once via MWSubmit.send app 'deck-remove' {agent,app,deck,results:{board,removed:true|false},notes:''} (local only if MWSubmit
       is missing); Undo clears the key and sends removed:false. style-swipe tools/apply_removals.py makes it permanent (status 'removed',
       moved to removed[], never done[]), so removed decks never count as completed. A removed deck frees a slot; the queue fills it (R97).
       Shared helper for other sections: DeckShelf.removable(card,{board,agent,deck,name,onChange}). */
(()=>{const CAP=10,ACC=['#C1502E','#05668D','#0B6E4F','#D4A017'];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const LS=k=>{try{return localStorage.getItem(k)}catch(_){return null}};
const today=()=>new Date().toLocaleDateString('en-CA');
/* v12 (Machan Oct 20 2026, deck ping system): a submitted deck leaves every board at once. Done = this browser's
   styleSwipe:submitted:<id> or mw-deck-done:<id> (set by submit.js on a full Submit), or listed in the server-side
   completed list kit/completed-decks.json ({ids:[...]} written by ops/submit/mark_completed.py), so it can't be re-swiped.
   Shelves re-render on back-navigation (pageshow), on another tab's submit (storage) and on the 'mw-deck-done' event. */
const CDONE=new Set(),CURL='https://webermanapps.github.io/style-swipe/kit/completed-decks.json';
const sub=d=>!!(d.id&&(LS('styleSwipe:submitted:'+d.id)||LS('mw-deck-done:'+d.id)||CDONE.has(d.id)));

const ALL='https://webermanapps.github.io/branding-djqmb410/decks/';
/* v11 / kit ly12 (R104, Max Oct 17 2026 19:39 ICT): deck cards open in the SAME tab with from=<this board> (+ from_name), so the deck page's
   Return button (kit/mw-back.js) goes back with history.back(), else via from=. Only trusted https://webermanapps.github.io/ links get it. */
const boardName=()=>{const t=document.querySelector('.mw-bh-title,.mw-cc-title');const x=(t?t.textContent:document.title).replace(/\s+(Agent\s+)?(Command Center|Board|Dashboard)\b.*$/i,'').trim();return x.slice(0,40)};
function fromUrl(u){try{const x=new URL(u,location.href);if(x.protocol!=='https:'||x.hostname!=='webermanapps.github.io'||location.hostname!=='webermanapps.github.io')return u;
 x.searchParams.set('from',location.origin+location.pathname);const n=boardName();if(n)x.searchParams.set('from_name',n);return x.href}catch(_){return u}}


const tagOf=d=>d.tag||d.category||(d.topic?String(d.topic).replace(/[-_]+/g,' ').replace(/\b\w/g,c=>c.toUpperCase()):'Deck');
const col=s=>{let h=0;for(const c of String(s))h=(h*31+c.charCodeAt(0))>>>0;return ACC[h%ACC.length]};
function base(J){if(Array.isArray(J.decks))return J.decks;const out=[];
 if(J.ready&&J.ready.url)out.push({name:J.ready.name,url:J.ready.url,total:J.ready.total||20,tag:(J.ready.categories||[])[0]});
 (J.unfinished||[]).forEach(d=>out.push({name:d.name,url:d.url,total:d.total||10,answered:d.answered||0,pinned:true}));return out}
function norm(J,o){o=o||{};const pin=[].concat(J.pinned||[],Array.isArray(J.decks)?(J.unfinished||[]):[],o.pinned||[]).map(d=>Object.assign({},d,{pinned:true}));
 const seen=new Set(),all=[];pin.concat(base(J)).forEach(d=>{if(d&&d.url&&!seen.has(d.url)){seen.add(d.url);all.push(d)}});return all}
/* Shelf sort (Max Oct 16 13:05, v5): permanent decks first, then IN PROGRESS (some answered, not done; most recently
   touched first), then NOT STARTED (current order: newest first, refills keep their slot), then DONE last.
   Progress = higher of shelf.json answered and this browser's localStorage picks (styleSwipe:<id>);
   last touched = localStorage state.updated, else shelf last_answer_at/updated/touched. Shared: DeckShelf.sortDecks(list,{isDone}). */
/* v6 (Oct 16): a shelf entry may carry progress_key = the exact localStorage key its deck page saves to (board-local decks:
   blog 'blog-deck-<id>-<built>', construction 'construction-deck-ans:<name>', legal 'legal-deck-ans:<name>'). Count = picks, or keys of .a, or keys of the object. */
const st8=d=>{try{return JSON.parse((d.progress_key&&LS(d.progress_key))||(d.id&&(LS('styleSwipe:'+d.id)||LS('styleSwipe:v3:'+d.id)))||'null')||{}}catch(_){return {}}};
const cnt=s=>Array.isArray(s.picks)?s.picks.length:s.a&&typeof s.a==='object'?Object.keys(s.a).length:Object.keys(s).filter(k=>!/^(v|idx|order|updated|skip|sent|at)$/.test(k)).length;
const answered=d=>Math.max(+d.answered||0,cnt(st8(d)));
const touched=d=>{const s=st8(d);return Math.max(Date.parse(s.updated||'')||0,Date.parse(d.last_answer_at||d.touched||d.updated||'')||0)};
const left=d=>Math.max(0,(d.total||10)-answered(d));
const started=d=>!sub(d)&&answered(d)>0;
const isPerm=d=>d.permanent===true||d.slot==='permanent';
/* R96: finished = done in shelf data or submitted in this browser. Never rendered; never removed from shelf.json. */
const GONE=/^(done|hidden|retired|replaced|split|unlisted)$/;
/* R102: per-board removal */
const boardOf=(box,J)=>(box&&box.dataset.board)||(J&&J.board)||location.pathname.split('/').filter(Boolean)[0]||location.hostname||'local';
const RK=(b,d)=>'ds-removed:'+b+':'+(d.id||d.url);
const isRemoved=(b,d)=>!!d&&(d.status==='removed'||d.removed===true||!!LS(RK(b,d)));
let toastT;function toast(msg,undo){let t=document.getElementById('ds-toast');if(!t){t=el('div','ds-toast');t.id='ds-toast';t.setAttribute('role','status');t.setAttribute('aria-live','polite');document.body.append(t)}
 t.textContent='';t.append(el('span','',msg));if(undo){const u=el('button','ds-undo','Undo');u.type='button';u.onclick=()=>{clearTimeout(toastT);t.classList.remove('on');undo()};t.append(u)}
 t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('on'),5000)}
function sendRm(o,on){try{if(window.MWSubmit&&typeof MWSubmit.send==='function')MWSubmit.send({agent:o.agent,app:'deck-remove',deck:o.deck,results:{board:o.board,removed:on},notes:''}).catch(()=>{})}catch(_){}}
function removable(card,o){const x=el('button','ds-x');x.type='button';x.setAttribute('aria-label','Remove '+(o.name||'deck'));x.title='Remove';x.append(el('span','','\u00d7'));
 const k='ds-removed:'+o.board+':'+o.deck;
 x.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();try{localStorage.setItem(k,new Date().toISOString())}catch(_){}sendRm(o,true);o.onChange&&o.onChange(true);
  toast('Removed',()=>{try{localStorage.removeItem(k)}catch(_){}sendRm(o,false);o.onChange&&o.onChange(false)})});
 ['pointerdown','touchstart','mousedown'].forEach(ev=>x.addEventListener(ev,e=>e.stopPropagation(),{passive:true}));card.append(x);return x}
const finished=(d,ids)=>!!d&&(GONE.test(String(d.status||''))||d.hidden===true||sub(d)||(!!ids&&!!d.id&&ids.has(d.id)));
const doneIds=J=>new Set((J.done||[]).map(x=>x&&(x.id||x.deck)).filter(Boolean));
/* R97: board ready queue (shelf.json queued[], or queue[]); only unfinished entries with a url, in queue order */
const queueOf=(J,ids,seen,B)=>[].concat(J.queued||[],J.queue||[]).filter(d=>d&&d.url&&!finished(d,ids)&&!isRemoved(B,d)&&!seen.has(d.url));
/* R98: New until clicked once on this device (per deck id) */
const seenKey=d=>'ds-opened:'+(d.id||d.url);
const isNew=d=>!LS(seenKey(d))&&!(answered(d)>0);
function sortDecks(all,o){o=o||{};const done=o.isDone||(d=>d.status==='done'||sub(d)),keep=o.keepOrder||(x=>x);
 const perm=all.filter(isPerm),rest=all.filter(d=>!isPerm(d)),dn=rest.filter(done),live=rest.filter(d=>!done(d));
 const prog=live.filter(d=>answered(d)>0&&answered(d)<(d.total||10)).map((d,i)=>[d,i]).sort((a,b)=>(touched(b[0])-touched(a[0]))||(a[1]-b[1])).map(x=>x[0]);
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
/* Oct 16 2026: ALL deck counters read ONE shared file, kit/deck-counts.json (rebuilt by ops/agent-activity/publish_deck_counts.py
   from every board's shelf done[] + submissions, deduped per deck+ICT day). Header "N done today", "decks today/all-time"
   and Grok Bot's Deck Report line all refresh from it on page load. */
const STATS='https://webermanapps.github.io/style-swipe/kit/deck-counts.json';
function paintReport(S){const d=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Bangkok'});
 document.querySelectorAll('summary').forEach(sm=>{const l=sm.querySelector('.lab'),o=sm.querySelector('.one');
  if(l&&o&&/^\s*Deck Report\s*$/.test(l.textContent)){const t=(S.days||{})[d]||0,a=typeof S.total==='number'?S.total:(S.decks||[]).length;
   o.textContent=t+(t===1?' deck':' decks')+' today \u00b7 '+a+' all-time'}})}
function statsFor(S,agent){if(!S||!agent)return null;const a=(S.agents||S)[agent]||{};if(typeof a!=='object')return null;
 const days=a.days||a.daily||Object.fromEntries(Object.entries(a).filter(([k,v])=>/^\d{4}-\d{2}-\d{2}$/.test(k)&&typeof v==='number'));
 const tz=S.tz||'Asia/Bangkok';let d;try{d=new Date().toLocaleDateString('en-CA',{timeZone:tz})}catch(_){d=today()}
 const total=typeof a.total==='number'?a.total:typeof a.all_time==='number'?a.all_time:Object.values(days).reduce((x,y)=>x+(+y||0),0);
 const dd=a.deck_days||a.decks_days, dt=typeof a.decks_today==='number'?a.decks_today:dd&&typeof dd[d]==='number'?dd[d]:null;
 const dT=typeof a.decks_total==='number'?a.decks_total:typeof a.decks_all_time==='number'?a.decks_all_time:null;
 return {today:dt!=null?dt:+(days[d]||0)/20,total:dT!=null?dT:total/20}}
const fmtDecks=n=>String(Math.floor(n+1e-9));
function paintStats(box,J){const st=box.querySelector('.ds-stats');if(!st)return;
 fetch((box.dataset.stats||J.stats_url||STATS)+'?'+Date.now()).then(r=>r.ok?r.json():null).then(S=>{if(S&&S.days)paintReport(S);const v=statsFor(S,J.agent);if(!v)return;const hd=box.querySelector('.ds-head');if(hd){let dn=hd.querySelector('.ds-done');const n=Math.floor(v.today+1e-9);if(n){if(!dn){dn=el('span','ds-done');hd.querySelector('h2').after(dn)}dn.textContent=n+' done today'}else if(dn)dn.remove()}
  st.textContent='';const f=(n,l)=>{const s=el('span','ds-stat');s.append(el('b','',fmtDecks(n)),el('span','',l));return s};
  st.append(f(v.today,(fmtDecks(v.today)==='1'?'deck':'decks')+' today'),f(v.total,(fmtDecks(v.total)==='1'?'deck':'decks')+' all-time'));st.hidden=false}).catch(()=>{})}
function render(box,J,o){o=o||{};J=J||{};const B=boardOf(box,J),ids=doneIds(J),live=norm(J,o).filter(d=>!finished(d,ids)&&!isRemoved(B,d)),cap=(o.nocap||box.hasAttribute('data-shelf-nocap'))?Infinity:Math.min(CAP,+o.cap||+box.dataset.shelfCap||+J.cap||CAP);
 const ordered=order(live),seen=new Set(ordered.map(d=>d.url)),q=queueOf(J,ids,seen,B),decks=ordered.slice(0,cap);
 for(const d of q){if(decks.length>=cap)break;decks.push(Object.assign({},d,{fromQueue:true}));seen.add(d.url)}
 box._dsQueued=ordered.slice(cap).concat(q.filter(d=>!decks.some(x=>x.url===d.url)));box._dsFinished=norm(J,o).filter(d=>finished(d,ids)&&!isRemoved(B,d));box._dsRemoved=norm(J,o).filter(d=>isRemoved(B,d));box.textContent='';box.classList.add('ds-sec');box.id=box.id||'ready-to-swipe';
 const h=el('div','ds-head');h.append(el('h2','','Ready To Swipe'));const n=doneToday(J);if(n)h.append(el('span','ds-done',n+' done today'));const st=el('div','ds-stats');st.hidden=true;h.append(st);const allU=box.dataset.all||J.all_url||ALL;if(!box.hasAttribute('data-shelf-nocap')){const al=el('a','ds-all','All Decks');al.href=allU;h.insertBefore(al,st)}box.append(h);paintStats(box,J);
 if(!decks.length){const p=el('p','ds-empty','All caught up. New decks are on the way. ');const l=el('a','','Deck Building');l.href=allU;p.append(l);box.append(p);return}
 const g=el('div','ds-strip');g.setAttribute('role','list');
 decks.forEach(d=>{const a=el('a','ds-card');a.href=fromUrl(d.url);a.setAttribute('role','listitem');const tag=tagOf(d),s=started(d);a.style.setProperty('--ds-c',d.color||col(tag));
  if(s)a.classList.add('ds-started');/* v11 R104: same tab, so Return can use browser history */
  a.append(el('b','ds-name',d.name||'Deck'),el('span','ds-tag',tag),el('span','ds-go',s?'Continue, '+left(d)+' left':'Start'));
  if(isNew(d)){a.classList.add('ds-isnew');a.append(el('span','ds-new','New'))}
  a.addEventListener('click',()=>{try{localStorage.setItem(seenKey(d),'1')}catch(_){}a.classList.remove('ds-isnew');const b=a.querySelector('.ds-new');if(b)b.remove()});
  if(d.id||d.url)removable(a,{board:B,agent:J.agent||B,deck:d.id||d.url,name:d.name,onChange:()=>render(box,J,o)});g.append(a)});
 box.append(g);if(decks.length>2){const dt=el('div','ds-dots');dt.setAttribute('aria-hidden','true');decks.forEach((_,i)=>dt.append(el('i',i?'':'on')));box.append(dt);
  g.addEventListener('scroll',()=>{const w=g.scrollWidth-g.clientWidth,k=w>0?Math.round(g.scrollLeft/w*(decks.length-1)):0;[...dt.children].forEach((x,i)=>x.className=i===k?'on':'')},{passive:true})}}
const CP=fetch(CURL+'?'+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():null).then(j=>{((j&&j.ids)||[]).forEach(x=>x&&CDONE.add(String(x)))}).catch(()=>{});
function init(){document.querySelectorAll('[data-shelf],[data-launcher]').forEach(b=>{if(b.dataset.dsDone)return;b.dataset.dsDone=1;
 const sp=fetch((b.dataset.shelf||b.dataset.launcher)+'?'+Date.now()).then(r=>r.json()).catch(()=>({decks:[]}));
 Promise.all([sp,CP]).then(([J])=>{b._dsJ=J;render(b,J)})})}
function rerender(){document.querySelectorAll('[data-shelf],[data-launcher]').forEach(b=>{if(b._dsJ)render(b,b._dsJ)})}
addEventListener('pageshow',e=>{if(e.persisted)rerender()});
addEventListener('storage',e=>{if(e.key&&/^(mw-deck-done:|styleSwipe:submitted:)/.test(e.key))rerender()});
addEventListener('mw-deck-done',rerender);
window.DeckShelf={render,CAP,sortDecks,answered,touched,finished,isNew,seenKey,VERSION:12,completed:CDONE,rerender,fromUrl,removable,isRemoved,boardOf,toast,removed:b=>b._dsRemoved||[],queued:b=>b._dsQueued||[],finishedOf:b=>b._dsFinished||[]};window.DeckLauncher=window.DeckLauncher||{render};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
