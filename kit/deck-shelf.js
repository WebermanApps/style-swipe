/* Ready Deck Shelf (R66, Max Oct 14 2026 19:30 ICT). Top of every agent dashboard: 3-5 ALREADY-BUILT decks, each exactly 20 cards,
   specific to that agent's project. Click one and start. No request/launcher: decks are built ahead; a submitted deck is replaced
   by a fresh ready 20-card deck on the same topic (tools/ready_shelf.py refill).
   Usage: <div data-shelf="shelf.json"></div> + <script src=".../kit/deck-shelf.js"></script>  (schema: kit/shelf.schema.json)
   Back-compat: old launcher.json ({ready, unfinished, categories}) is shown as a shelf of its ready + unfinished decks (picker retired). */
(()=>{const TOTAL=20;
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
/* Deck cap (Max, Oct 14 2026 19:43 ICT): at most 5 decks on a dashboard, ready-shelf + pinned unfinished together.
   Pinned unfinished (J.unfinished / J.pinned / opts.pinned) come first, then ready decks; the rest are queued (not shown) and
   appear only when a slot opens. Only the Deck Building page may opt out: data-shelf-nocap. Extras: DeckShelf.queued(box). */
const CAP=5;
function norm(J,o){o=o||{};const pin=[].concat(J.pinned||[],Array.isArray(J.decks)?(J.unfinished||[]):[],o.pinned||[]).map(d=>Object.assign({},d,{answered:d.answered||0,pinned:true}));
 const seen=new Set(),all=[];pin.concat(base(J)).forEach(d=>{if(d&&d.url&&!seen.has(d.url)){seen.add(d.url);all.push(d)}});return all}
function base(J){if(Array.isArray(J.decks))return J.decks;const out=[];
 if(J.ready&&J.ready.url)out.push({name:J.ready.name,url:J.ready.url,total:J.ready.total||TOTAL,blurb:(J.ready.categories||[]).join(', ')});
 (J.unfinished||[]).forEach(d=>out.push({name:d.name,url:d.url,total:d.total||TOTAL,answered:d.answered||0}));return out}
function render(box,J,o){o=o||{};const all=norm(J||{},o),cap=(o.nocap||box.hasAttribute('data-shelf-nocap'))?all.length:CAP,decks=all.slice(0,cap);box._dsQueued=all.slice(cap);box.textContent='';box.classList.add('ds-sec');box.id=box.id||'deck-shelf';
 const h=el('div','ds-head');h.append(el('h2','','Ready Decks'),el('span','ds-meta',decks.length?decks.length+' decks, '+TOTAL+' cards each':'New decks are being built'));box.append(h);
 const g=el('div','ds-grid');decks.forEach(d=>{const a=el('a','ds-card');a.href=d.url;
  const top=el('div','ds-top');top.append(el('span','ds-pill',(d.answered||d.pinned)?'In progress':'Ready'),el('span','ds-meta',(d.answered?d.answered+' / ':'')+(d.total||TOTAL)+' cards'));
  a.append(top,el('b','ds-name',d.name||'Deck'));if(d.blurb)a.append(el('span','ds-blurb',d.blurb));a.append(el('span','ds-go','Start'));g.append(a)});
 box.append(g)}
function init(){document.querySelectorAll('[data-shelf],[data-launcher]').forEach(b=>{if(b.dataset.dsDone)return;b.dataset.dsDone=1;
 fetch((b.dataset.shelf||b.dataset.launcher)+'?'+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{})})}
window.DeckShelf={render,CAP,queued:b=>b._dsQueued||[]};window.DeckLauncher=window.DeckLauncher||{render};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
