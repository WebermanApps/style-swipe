/* Routines Section v6 (Team Improvement Deck results, Max Oct 16 2026; Branding Oct 17): times read '4:40 AM Daily' (time first, capitalised);
   rows are split into 'Daily And Beyond' and 'Several Times A Day' (Max note), paused rows last; rows no longer expand inline:
   tapping a row or 'See All' opens one details drawer listing every routine. Square Active/Paused tag stays (no rounded pills). Same ?v=5 URL.
   v5 (R79, Max Oct 16 2026 13:23 ICT): the whole section is a dropdown, CLOSED by default; header row 'Routines (N)' opens the compact list; rows still expand on tap.
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
function cap(t){return String(t||'').replace(/\b(daily|weekdays|monthly|once)\b/g,function(w){return w[0].toUpperCase()+w.slice(1)})}
function many(r){var t=(r.short_time||shortTime(r.schedule_plain)||'')+' '+(r.schedule_plain||'');return /^\s*(every \d+ (min|hr|hour)|hourly)|\d:\d\d\s*[AP]M \+ /i.test(t)||/every \d+ (min|minutes|hours?)\b|hourly|twice a day|\band\b \d{1,2}:\d{2}/i.test(r.schedule_plain||'')}
function shortName(r){return r.short||String(r.name||'').replace(/\s*\([^)]*\)/g,'').replace(/^(?:[A-Z][a-z]+ )?Dashboard /,'').trim()}
function render(box,J){const R=(Array.isArray(J)?J:(J.routines||[])).slice();box.textContent='';box.classList.add('rt4');box.id=box.id||'routines';
 const rank=r=>r.status==='paused'?99:(ORD.indexOf(r.group)<0?50:ORD.indexOf(r.group));R.sort((a,b)=>rank(a)-rank(b));
 const on=R.filter(r=>r.status!=='paused').length,fold=el('details','rt4-fold'),h=el('summary','rt4-head');
 h.append(el('h2','','Routines ('+R.length+')'),el('span','rt4-count',on+' active'+(R.length-on?' · '+(R.length-on)+' paused':'')),el('span','rt4-chev'));fold.append(h);box.append(fold);
 const list=el('div','rt4-list');fold.append(list);
 const groups=[['Daily And Beyond',R.filter(r=>r.status!=='paused'&&!many(r))],['Several Times A Day',R.filter(r=>r.status!=='paused'&&many(r))],['Paused',R.filter(r=>r.status==='paused')]];
 const dr=drawer(box,R);
 groups.forEach(([g,rs])=>{if(!rs.length)return;list.append(el('h3','rt4-sub',g));rs.forEach(r=>{const p=r.status==='paused',s=el('button','rt4-row'+(p?' is-paused':''));s.type='button';
  s.append(el('span','rt4-name',shortName(r)),el('span','rt4-time',cap(r.short_time||shortTime(r.schedule_plain))),el('span','rt4-st',p?'Paused':'Active'));s.addEventListener('click',()=>dr.open(R.indexOf(r)));list.append(s)})});
 const all=el('button','rt4-all','See All');all.type='button';all.addEventListener('click',()=>dr.open(-1));list.append(all);}
function drawer(box,R){let d=box.querySelector('.rt4-drawer');if(d)d.remove();d=el('div','rt4-drawer');d.hidden=true;d.setAttribute('role','dialog');d.setAttribute('aria-label','All routines');
 const pan=el('div','rt4-pan'),hd=el('div','rt4-dhead'),x=el('button','rt4-x','Close');x.type='button';hd.append(el('h2','','All Routines'),x);pan.append(hd);
 const items=R.map(r=>{const it=el('section','rt4-item'+(r.status==='paused'?' is-paused':''));it.append(el('h3','',shortName(r)));const meta=el('p','rt4-meta');meta.append(el('span','rt4-time',cap(r.short_time||shortTime(r.schedule_plain))),el('span','rt4-st',r.status==='paused'?'Paused':'Active'));it.append(meta);
  if(shortName(r)!==r.name)it.append(el('p','rt4-full',r.name));if(r.note)it.append(el('p','',r.note));const dl=el('dl');[['Schedule',r.schedule_plain],['Group',r.group],['How often',many(r)?'Several times a day':'Daily and beyond'],['Last run',r.last_run||'Not yet']].forEach(([k,v])=>{if(v){dl.append(el('dt','',k),el('dd','',v))}});it.append(dl);pan.append(it);return it});
 d.append(pan);document.body.append(d);const close=()=>{d.hidden=true;document.documentElement.classList.remove('rt4-lock')};x.addEventListener('click',close);d.addEventListener('click',e=>{if(e.target===d)close()});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!d.hidden)close()});
 return {open(i){d.hidden=false;document.documentElement.classList.add('rt4-lock');pan.scrollTop=0;items.forEach(t=>t.classList.remove('is-focus'));if(i>=0&&items[i]){items[i].classList.add('is-focus');setTimeout(()=>items[i].scrollIntoView({block:'start'}),30)}x.focus()}}}
function init(){document.querySelectorAll('[data-routines]').forEach(b=>{const u=b.dataset.routines;if(!u)return;fetch(u+(u.includes('?')?'&':'?')+Date.now()).then(r=>r.json()).then(J=>render(b,J)).catch(()=>{})})}
window.RoutinesSection={render,shortTime,many};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init()})();
