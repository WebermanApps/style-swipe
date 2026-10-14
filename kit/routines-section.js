/* Routines Section (R65). Usage: <div data-routines="routines.json"></div> + this script. */
(()=>{const G=[['Reports','#ECC978'],['Daily','#0B6E4F'],['Weekly','#2E6FA8'],['Monthly','#8A5BB5'],['Event/Listener','#D7A363'],['Paused','#A3A3A3']];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
function render(box,J){const R=Array.isArray(J)?J:(J.routines||[]);box.textContent='';box.classList.add('rt-sec');box.id=box.id||'routines';
box.append(el('h2','','Routines'));const g=el('div','rt-grid');box.append(g);
G.forEach(([name,c])=>{const rows=R.filter(r=>(r.status==='paused'?'Paused':r.group)===name);if(!rows.length)return;
const s=el('div','rt-grp');s.style.setProperty('--rt-c',c);s.append(el('h3','',name));
rows.forEach(r=>{const w=el('div','rt-row');w.append(el('span','rt-name',r.name),el('span','rt-st '+(r.status==='paused'?'paused':'on'),r.status==='paused'?'Paused':'On'),el('span','rt-meta',r.schedule_plain+' · Last Run '+(r.last_run||'Not Yet')));s.append(w)});g.append(s)});}
function init(){document.querySelectorAll('[data-routines]').forEach(b=>fetch(b.dataset.routines+'?'+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{}))}
window.RoutinesSection={render};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
