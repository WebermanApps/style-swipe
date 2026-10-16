/* Routines Section v5 (R79, Max Oct 16 2026 13:23 ICT): the whole section is a dropdown, CLOSED by default; header row 'Routines (N)' opens the compact list; rows still expand on tap.
   v4 (R78, Max Oct 16 2026): compact list in the branded footer. One row per routine: short name + short time + Active/Paused; tap a row to expand details (description, full schedule, group, last run). Collapsed by default.
   Usage: <div data-routines="routines.json"></div> + this script. Optional per-routine fields: short (row name), short_time (row time, e.g. '4:40 AM daily'), note (details text). */
(()=>{const ORD=['Reports','Daily','Weekly','Monthly','Event/Listener'];
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const DAY={Mondays:'Mon',Tuesdays:'Tue',Wednesdays:'Wed',Thursdays:'Thu',Fridays:'Fri',Saturdays:'Sat',Sundays:'Sun'};
function shortTime(s){s=String(s||'').trim();if(!s)return '';
 if(/^(retired|was )/i.test(s)||/retired/i.test(s)&&!/^daily at|^every/i.test(s))return 'Retired';
 s=s.replace(/\s*\([^)]*\)/g,'').replace(/\.\s.*$/,'').replace(/,\s*Posts.*$/i,'').replace(/\s*ICT\b/g,'').replace(/\s+/g,' ').trim();
 let m;const T='(\\d{1,2}:\\d{2}\\s*[AP]M)';
 if(m=s.match(new RegExp('^(?:Daily|Every Day) At '+T+'$','i')))return m[1]+' daily';
 if(m=s.match(new RegExp('^Daily (?:At )?'+T+'(?: and '+T+')?$','i')))return m[2]?m[1]+' + '+m[2]+' daily':m[1]+' daily';
 if(m=s.match(new RegExp('^Daily (Before|By) '+T,'i')))return 'By '+m[2]+' daily';
 if(m=s.match(new RegExp('^(Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Sundays) At '+T,'i')))return m[2]+' '+DAY[m[1][0].toUpperCase()+m[1].slice(1).toLowerCase()];
 if(m=s.match(new RegExp('^Weekdays At '+T,'i')))return m[1]+' weekdays';
 if(m=s.match(new RegExp('^(\\w{3}) To (\\w{3}) At '+T,'i')))return m[3]+' '+m[1]+'-'+m[2];
 if(m=s.match(new RegExp('^(.+?) Of Each Month At '+T,'i')))return m[2]+', '+m[1].replace(/ And /i,' + ')+' monthly';
 if(m=s.match(/^Every (\d+) (Min|Minutes|Hours?)(?:,\s*(.+?) To (.+))?$/i))return 'Every '+m[1]+' '+(/^min/i.test(m[2])?'min':'hr')+(m[3]?', '+m[3]+'-'+m[4]:'');
 if(m=s.match(/^Every (\d+) Hours At (:\d\d)/i))return 'Every '+m[1]+' hr at '+m[2];
 if(m=s.match(/^Hourly At (.+)$/i))return 'Hourly '+m[1].replace(/ And /i,', ');
 if(m=s.match(new RegExp('^Once(?:,| On)\\s*(?:\\w{3} )?(\\w{3} \\d{1,2}) At '+T,'i')))return m[1]+', '+m[2]+' once';
 if(/^Daily Morning/i.test(s))return 'Mornings daily';
 if(/^(On Each|When|After) /i.test(s))return /submit/i.test(s)?'On submit':'On event';
 return s.length>26?s.slice(0,25).replace(/\s+\S*$/,'')+'…':s}
function shortName(r){return r.short||String(r.name||'').replace(/\s*\([^)]*\)/g,'').replace(/^(?:[A-Z][a-z]+ )?Dashboard /,'').trim()}
function render(box,J){const R=(Array.isArray(J)?J:(J.routines||[])).slice();box.textContent='';box.classList.add('rt4');box.id=box.id||'routines';
 const rank=r=>r.status==='paused'?99:(ORD.indexOf(r.group)<0?50:ORD.indexOf(r.group));R.sort((a,b)=>rank(a)-rank(b));
 const on=R.filter(r=>r.status!=='paused').length,fold=el('details','rt4-fold'),h=el('summary','rt4-head');
 h.append(el('h2','','Routines ('+R.length+')'),el('span','rt4-count',on+' active'+(R.length-on?' · '+(R.length-on)+' paused':'')),el('span','rt4-chev'));fold.append(h);box.append(fold);
 const list=el('div','rt4-list');fold.append(list);
 R.forEach(r=>{const p=r.status==='paused',d=el('details','rt4-row'+(p?' is-paused':'')),s=el('summary');
  s.append(el('span','rt4-name',shortName(r)),el('span','rt4-time',r.short_time||shortTime(r.schedule_plain)),el('span','rt4-st',p?'Paused':'Active'));d.append(s);
  const b=el('div','rt4-detail');if(shortName(r)!==r.name)b.append(el('p','rt4-full',r.name));if(r.note)b.append(el('p','',r.note));
  const dl=el('dl');[['Schedule',r.schedule_plain],['Group',r.group],['Last run',r.last_run||'Not yet']].forEach(([k,v])=>{if(v){dl.append(el('dt','',k),el('dd','',v))}});b.append(dl);d.append(b);list.append(d)});}
function init(){document.querySelectorAll('[data-routines]').forEach(b=>{const u=b.dataset.routines;if(!u)return;fetch(u+(u.includes('?')?'&':'?')+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{})})}
window.RoutinesSection={render,shortTime};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
