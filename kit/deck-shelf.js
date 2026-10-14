/* Ready Deck Shelf (R66, Max Oct 14 2026 19:30 ICT). Top of every agent dashboard: 3-5 ALREADY-BUILT decks, each exactly 20 cards,
   specific to that agent's project. Click one and start. No request/launcher: decks are built ahead; a submitted deck is replaced
   by a fresh ready 20-card deck on the same topic (tools/ready_shelf.py refill).
   Usage: <div data-shelf="shelf.json"></div> + <script src=".../kit/deck-shelf.js"></script>  (schema: kit/shelf.schema.json)
   Back-compat: old launcher.json ({ready, unfinished, categories}) is shown as a shelf of its ready + unfinished decks (picker retired). */
(()=>{const TOTAL=20;
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
function norm(J){if(Array.isArray(J.decks))return J.decks;const out=[];
 if(J.ready&&J.ready.url)out.push({name:J.ready.name,url:J.ready.url,total:J.ready.total||TOTAL,blurb:(J.ready.categories||[]).join(', ')});
 (J.unfinished||[]).forEach(d=>out.push({name:d.name,url:d.url,total:d.total||TOTAL,answered:d.answered||0}));return out}
function render(box,J){const decks=norm(J||{}).filter(d=>d&&d.url).slice(0,5);box.textContent='';box.classList.add('ds-sec');box.id=box.id||'deck-shelf';
 const h=el('div','ds-head');h.append(el('h2','','Ready Decks'),el('span','ds-meta',decks.length?decks.length+' ready, '+TOTAL+' cards each':'New decks are being built'));box.append(h);
 const g=el('div','ds-grid');decks.forEach(d=>{const a=el('a','ds-card');a.href=d.url;
  const top=el('div','ds-top');top.append(el('span','ds-pill',d.answered?'In progress':'Ready'),el('span','ds-meta',(d.answered?d.answered+' / ':'')+(d.total||TOTAL)+' cards'));
  a.append(top,el('b','ds-name',d.name||'Deck'));if(d.blurb)a.append(el('span','ds-blurb',d.blurb));a.append(el('span','ds-go','Start'));g.append(a)});
 box.append(g)}
function init(){document.querySelectorAll('[data-shelf],[data-launcher]').forEach(b=>{if(b.dataset.dsDone)return;b.dataset.dsDone=1;
 fetch((b.dataset.shelf||b.dataset.launcher)+'?'+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{})})}
window.DeckShelf={render};window.DeckLauncher=window.DeckLauncher||{render};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
