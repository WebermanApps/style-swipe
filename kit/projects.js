/* Ongoing Projects (R100; kit op1, Branding Agent, Oct 17 2026). LOCAL BUILD - not published.
   Usage on a kit board (after mw-layout.js):
     <link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/projects.css?v=op1">
     script src=".../style-swipe/kit/projects.js?v=op1" data-projects="projects.json" defer (after mw-layout.js)
   or place <section id="mw-projects" data-mw-projects="projects.json"></section> anywhere; the kit moves it to the top of #mw-mid
   (right under the branded header divider, before the agent's own content).
   Data: board projects.json (schema: ops/brand/projects.schema.json), written only by /workspace/ops/brand/pin_project.py.
   Storage modes (projects.json "storage"):
     "none"      local preview only: raw files are fetched ONLY on file:, localhost or 127.0.0.1. Never on a public host.
     "encrypted" PLANNED DEFAULT. Security's enc_file_viewer.js (INLINED once in the locked page) decrypts files/<random12>.enc with the remembered
                 page-unlock key into a Blob. Thumbnails too (blob: URL img src). An encrypted index (projects.json {"index":"files/x.enc"})
                 is decrypted the same way, so titles and filenames need not be public.
     "private"   hook only (e.g. a private signed-URL backend); refuses until implemented.
   No crypto lives here: decryption is delegated to Security's viewer through ProjectsSection.storage.encrypted. */
(function(){
'use strict';
var V='op1',MAX=6,EXCLUDE=/a-o956qercs5ubd57y|home-guide|finish-questions|room-photos|room-quiz|homes\.maxweberman\.com|share-x3l9xcxc1eut/;
var me=document.currentScript;
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e}
function svg(d){var s=document.createElementNS('http://www.w3.org/2000/svg','svg');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('aria-hidden','true');s.innerHTML=d;return s}
var I={folder:'<path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>',open:'<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5"/>',
 dl:'<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',ho:'<path d="M4 12h12M12 6l6 6-6 6"/><path d="M20 5v14"/>',chev:'<path d="M6 9l6 6 6-6"/>',prev:'<path d="M15 6l-6 6 6 6"/>',next:'<path d="M9 6l6 6-6 6"/>'};
function isLocal(){return location.protocol==='file:'||/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)}
/* only board-relative paths: no scheme, no leading slash, no .. (a tampered projects.json cannot point elsewhere) */
function safePath(p){return typeof p==='string'&&p.length<300&&!/^[a-z][a-z0-9+.-]*:|^\/|\\|(^|\/)\.\.(\/|$)/i.test(p)?p:null}
function base(){var s=(me&&me.getAttribute('data-projects'))||'projects.json';return s}

/* ---- pluggable storage (decrypt/fetch -> Blob). Security's viewer plugs in here. ---- */
var storage={
 none:{label:'local preview',blob:function(ref){
   if(!isLocal())return Promise.reject(new Error('Not published yet: waiting on Security'));
   var p=safePath(ref.path);if(!p)return Promise.reject(new Error('Bad path'));
   return fetch(p,{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.blob()}).then(function(b){return ref.mime?new Blob([b],{type:ref.mime}):b})}},
 encrypted:{label:'encrypted',blob:function(ref){
   /* Security's enc_file_viewer.js (inline it once in the locked page, per ops/team-sync/handoffs/encrypted-files.md).
      API: mwEncFile.decrypt('files/x.enc') -> {url,name,mime,size,blob}; key = localStorage mwPagesKey set by the unlocked gate.
      Filename and MIME come from the encrypted header, so projects.json never needs them in plaintext. */
   var p=safePath(ref.path);if(!p||!/^files\/[a-z0-9]{12}\.enc$/.test(p))return Promise.reject(new Error('Bad path'));
   var v=window.mwEncFile;
   if(!v||typeof v.decrypt!=='function')return Promise.reject(new Error('File viewer missing on this page'));
   if(!localStorage.getItem('mwPagesKey'))return Promise.reject(new Error('Unlock the dashboard first'));
   return v.decrypt(p).then(function(f){var b=f.blob;b.__name=f.name;return b},function(e){throw new Error(/stale/.test(String(e&&e.message))?'Unlock the dashboard first (saved key is out of date)':'Could not open this file')})}},
 private:{label:'private',blob:function(){return Promise.reject(new Error('Private storage is not set up yet'))}}
};
var mode='none';
function getBlob(ref){var s=storage[mode]||storage.none;return s.blob(ref)}

function fmtDate(s){var d=new Date(s);if(isNaN(d))return '';var now=new Date(),o={month:'short',day:'numeric'};if(d.getFullYear()!==now.getFullYear())o.year='numeric';
 return d.toLocaleDateString('en-US',o)}
function typeOf(p){return String(p.type||(p.file&&p.file.name||'').split('.').pop()||'File').toUpperCase().slice(0,5)}

var urls=[];function track(u){urls.push(u);return u}
addEventListener('pagehide',function(){urls.forEach(function(u){try{URL.revokeObjectURL(u)}catch(_){}})});

function busy(b,on){b.setAttribute('aria-busy',on?'true':'false');b.disabled=!!on}
function note(card,msg){var m=card.querySelector('.op-msg');if(!m){m=el('p','op-msg');m.setAttribute('role','status');card.appendChild(m)}m.textContent=msg}
function doOpen(p,btn,host){
 var ref=p.preview||p.file;if(!ref)return;
 var w=null;try{w=window.open('','_blank')}catch(_){} /* open synchronously so popup blockers allow it */
 busy(btn,true);
 getBlob(ref).then(function(b){var u=track(URL.createObjectURL(b));if(w&&!w.closed){w.location.href=u}else{location.assign(u)}})
 .catch(function(e){if(w)try{w.close()}catch(_){}note(host,e.message)}).then(function(){busy(btn,false)})}
function doDownload(p,btn,host){
 if(!p.file)return;busy(btn,true);
 getBlob(p.file).then(function(b){var a=el('a');a.href=track(URL.createObjectURL(b));a.download=b.__name||p.file.name||((p.title||'file')+'.'+typeOf(p).toLowerCase());document.body.appendChild(a);a.click();a.remove()})
 .catch(function(e){note(host,e.message)}).then(function(){busy(btn,false)})}


/* ---- Hand off project (R100 addition, Max Oct 17 2026 15:47 ICT) ----
   Posts via MWSubmit.send (submit.js) to the shared Apps Script receiver: agent=<owner>, app="project-handoff", deck=<project id>,
   results={project_id,project_title,owner_agent,to_agents,note,files,page_url}. files = projects.json file refs only (paths, names, MIME; never keys). */
var TEAM_FALLBACK={"blog":"Blog Agent","blueprint":"Blueprint Agent","branding":"Branding Agent","coach":"Coach Agent","construction":"Construction Agent","dump":"Dump Agent","email-sorting":"Email Sorting Agent","grok-bot":"Grok Bot","household":"Household","japan-cottage":"Japan Cottage Agent","jokes":"Jokes Agent","legal":"Legal Agent","miles":"Miles Agent","portfolio":"Portfolio Agent","prop":"Prop Agent","research":"Research Agent","scout":"Scout Agent","security":"Security Agent","thai":"Thai Agent","upkeep":"UpKeep Agent","video-photo":"Video & Photo Agent","wellnest":"WellNest Agent"};
var team=null;
function kitBase(){var s=me&&me.src;return s?s.replace(/[^\/]*$/,''):'https://webermanapps.github.io/style-swipe/kit/'}
function slugify(s){return String(s).toLowerCase().replace(/&/g,' ').replace(/\bagent\b/g,'').trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
function loadTeam(){if(team)return Promise.resolve(team);var m={};Object.keys(TEAM_FALLBACK).forEach(function(k){m[k]=TEAM_FALLBACK[k]});
 var b=kitBase();
 return Promise.all([fetch(b+'agent-dashboards.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){var n=j&&j.names||{};Object.keys(n).forEach(function(k){m[k]=n[k]})}).catch(function(){}),
  fetch(b+'agent-status.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){(j&&j.agents||[]).forEach(function(a){var s=slugify(a.agent);if(s&&!m[s])m[s]=a.agent})}).catch(function(){})])
 .then(function(){team=Object.keys(m).map(function(k){return{slug:k,name:m[k]}}).sort(function(a,b){return a.name.localeCompare(b.name)});return team})}
function ownerAgent(p){return p.agent||document.body.getAttribute('data-mw-agent')||(document.querySelector('[data-agent-name]')||{getAttribute:function(){return ''}}).getAttribute('data-agent-name')||''}
function fileRefs(p){var out=[];[['file','file'],['preview','preview'],['thumb','thumbnail']].forEach(function(k){var r=p[k[0]];if(!r||!r.path)return;var f={role:k[1],path:r.path,encrypted:/\.enc$/.test(r.path)};if(r.name)f.name=r.name;if(r.mime)f.mime=r.mime;out.push(f)});return out}
function handoffPayload(p,to,note){return{project_id:p.id,project_title:p.title,owner_agent:ownerAgent(p),to_agents:to.map(function(t){return t.slug}),note:note||'',files:fileRefs(p),page_url:location.origin+location.pathname}}
function listNames(a){a=a.map(function(t){return t.name});return a.length<2?a.join(''):a.slice(0,-1).join(', ')+' and '+a[a.length-1]}
var hoOpen=null;
function openHandoff(p,opener){
 if(hoOpen)hoOpen.close();
 var bg=el('div','op-ho-bg'),box=el('form','op-ho');box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-labelledby','op-ho-t');box.noValidate=true;box.autocomplete='off';
 var x=el('button','op-ho-x');x.type='button';x.setAttribute('aria-label','Close');x.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
 var h=el('h2','op-ho-h','Hand Off Project');h.id='op-ho-t';
 var sub=el('p','op-ho-sub',p.title);
 var lab=el('label','op-ho-l','To');lab.htmlFor='op-ho-in';
 var field=el('div','op-ho-field'),chips=el('div','op-ho-chips'),inp=el('input','op-ho-in');inp.id='op-ho-in';inp.type='text';inp.placeholder='Type an agent name';inp.setAttribute('role','combobox');inp.setAttribute('aria-autocomplete','list');inp.setAttribute('aria-expanded','false');inp.setAttribute('aria-controls','op-ho-sug');inp.autocapitalize='words';inp.spellcheck=false;inp.enterKeyHint='done';
 field.append(chips,inp);
 var sug=el('ul','op-ho-sug');sug.id='op-ho-sug';sug.setAttribute('role','listbox');sug.hidden=true;
 var nl=el('label','op-ho-l','Note (optional)');nl.htmlFor='op-ho-note';var nt=el('textarea','op-ho-note');nt.id='op-ho-note';nt.rows=3;nt.maxLength=1000;nt.placeholder='Anything they should know';
 var msg=el('p','op-ho-msg');msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');
 var row=el('div','op-ho-row'),cancel=el('button','op-btn','Cancel'),send=el('button','op-btn op-btn--open op-ho-send','Send');cancel.type='button';send.type='submit';row.append(cancel,send);
 box.append(x,h,sub,lab,field,sug,nl,nt,msg,row);bg.appendChild(box);document.body.appendChild(bg);document.documentElement.classList.add('op-ho-lock');
 var picked=[],act=-1,cur=[],state='idle';
 function drawChips(){chips.textContent='';picked.forEach(function(t,i){var c=el('span','op-ho-chip');c.appendChild(el('span',null,t.name));var r=el('button');r.type='button';r.setAttribute('aria-label','Remove '+t.name);r.textContent='\u00d7';r.onclick=function(){picked.splice(i,1);drawChips();inp.focus()};c.appendChild(r);chips.appendChild(c)});inp.placeholder=picked.length?'Add another':'Type an agent name';validate()}
 function add(t){if(!t||!t.slug)return;if(!picked.some(function(q){return q.slug===t.slug}))picked.push(t);inp.value='';hide();drawChips()}
 function addTyped(){var v=inp.value.replace(/,/g,' ').trim();if(!v)return false;var s=slugify(v),hit=(team||[]).filter(function(t){return t.slug===s||t.name.toLowerCase()===v.toLowerCase()||slugify(t.name)===s})[0];
  add(hit||{slug:s||v.toLowerCase(),name:v,free:true});return true}
 function hide(){sug.hidden=true;inp.setAttribute('aria-expanded','false');act=-1;inp.removeAttribute('aria-activedescendant')}
 function show(){var v=inp.value.trim().toLowerCase();if(!team){hide();return}
  cur=team.filter(function(t){return!picked.some(function(q){return q.slug===t.slug})&&(!v||t.name.toLowerCase().indexOf(v)>=0||t.slug.indexOf(v)>=0)}).sort(function(a,b){var A=a.name.toLowerCase().indexOf(v)===0?0:1,B=b.name.toLowerCase().indexOf(v)===0?0:1;return A-B||a.name.localeCompare(b.name)}).slice(0,6);
  sug.textContent='';cur.forEach(function(t,i){var li=el('li');li.id='op-ho-o'+i;li.setAttribute('role','option');li.append(el('b',null,t.name.replace(/ Agent$/,'')),el('small',null,t.slug));li.onmousedown=function(e){e.preventDefault()};li.onclick=function(){add(t);inp.focus()};sug.appendChild(li)});
  if(v&&!cur.some(function(t){return t.name.toLowerCase()===v})){var li=el('li','op-ho-free');li.setAttribute('role','option');li.id='op-ho-o'+cur.length;li.appendChild(el('span',null,'Use \u201c'+inp.value.trim()+'\u201d'));li.onmousedown=function(e){e.preventDefault()};li.onclick=function(){addTyped();inp.focus()};sug.appendChild(li)}
  sug.hidden=!sug.children.length;inp.setAttribute('aria-expanded',String(!sug.hidden));act=-1}
 function mark(){[].forEach.call(sug.children,function(li,i){li.classList.toggle('on',i===act);li.setAttribute('aria-selected',String(i===act))});if(act>=0){inp.setAttribute('aria-activedescendant','op-ho-o'+act);sug.children[act].scrollIntoView({block:'nearest'})}}
 inp.addEventListener('input',function(){if(/,$/.test(inp.value)){addTyped();return}show();validate()});inp.addEventListener('focus',show);inp.addEventListener('blur',function(){setTimeout(hide,120)});
 inp.addEventListener('keydown',function(e){var n=sug.children.length;
  if(e.key==='ArrowDown'&&n){e.preventDefault();if(sug.hidden)show();act=(act+1)%n;mark()}
  else if(e.key==='ArrowUp'&&n){e.preventDefault();act=(act-1+n)%n;mark()}
  else if(e.key==='Enter'){e.preventDefault();if(act>=0&&!sug.hidden)sug.children[act].click();else if(!addTyped()&&picked.length)box.requestSubmit?box.requestSubmit():send.click()}
  else if(e.key==='Backspace'&&!inp.value&&picked.length){picked.pop();drawChips()}});
 field.onclick=function(e){if(e.target===field||e.target===chips)inp.focus()};
 function validate(){if(state==='idle'||state==='fail')send.disabled=!(picked.length||inp.value.trim())}
 function setState(s,t){state=s;box.classList.remove('is-sent','is-fail');msg.className='op-ho-msg';
  if(s==='sending'){send.disabled=true;cancel.disabled=true;send.textContent='Sending';send.setAttribute('aria-busy','true');msg.textContent=''}
  else{send.removeAttribute('aria-busy');cancel.disabled=false}
  if(s==='sent'){box.classList.add('is-sent');msg.className='op-ho-msg ok';msg.textContent=t;send.textContent='Done';send.disabled=false;cancel.hidden=true;[inp,nt].forEach(function(f){f.disabled=true});chips.querySelectorAll('button').forEach(function(b){b.hidden=true})}
  if(s==='fail'){box.classList.add('is-fail');msg.className='op-ho-msg err';msg.textContent=t;send.textContent='Try Again';validate()}
  if(s==='idle'){send.textContent='Send';validate()}}
 function close(){document.removeEventListener('keydown',esc);bg.remove();document.documentElement.classList.remove('op-ho-lock');hoOpen=null;try{opener&&opener.focus()}catch(_){}}
 function esc(e){if(e.key==='Escape'&&state!=='sending'){if(!sug.hidden){hide();return}close()}
  if(e.key==='Tab'){var f=[].filter.call(box.querySelectorAll('button,input,textarea'),function(n){return!n.disabled&&!n.hidden&&n.offsetParent});if(!f.length)return;var a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}}
 document.addEventListener('keydown',esc);
 x.onclick=function(){if(state!=='sending')close()};cancel.onclick=close;bg.addEventListener('mousedown',function(e){if(e.target===bg&&state!=='sending')close()});
 box.addEventListener('submit',function(e){e.preventDefault();if(state==='sent'){close();return}if(state==='sending')return;
  addTyped();if(!picked.length){setState('fail','Add at least one agent.');inp.focus();return}
  var S=window.MWSubmit;if(!S||typeof S.send!=='function'){setState('fail','Sending is not set up on this page yet. Nothing was sent.');return}
  var body=handoffPayload(p,picked,nt.value.trim()),who=listNames(picked);setState('sending');
  Promise.resolve().then(function(){return S.send({agent:body.owner_agent||'grok-bot',app:'project-handoff',deck:p.id,results:body,notes:body.note})})
  .then(function(ok){if(ok){setState('sent','Sent to '+who+'.')}
   else if(S.blocked){setState('fail','Password needed. Nothing was sent.')}
   else{setState('fail','Not sent yet: no connection. It is saved on this device and retries when you are back online, or tap Try Again.')}})
  .catch(function(){setState('fail','Something went wrong. Nothing was sent. Tap Try Again.')})});
 loadTeam().then(function(){if(document.activeElement===inp)show()});
 setState('idle');setTimeout(function(){inp.focus()},30);
 hoOpen={close:close};return hoOpen}

function btn(cls,icon,label,aria){var b=el('button','op-btn '+cls);b.type='button';b.appendChild(svg(I[icon]));b.appendChild(el('span',null,label));if(aria)b.setAttribute('aria-label',aria);return b}

/* encrypted mode uses Security's documented markup exactly: Open = a[data-enc-file], Download = a[data-enc-file][data-enc-download],
   thumbnail = img[data-enc-img]. enc_file_viewer.js handles clicks (global capture listener) and image decryption. */
function act(p,kind,host){var enc=mode==='encrypted',ref=kind==='open'?(p.preview||p.file):p.file,label=kind==='open'?'Open':'Download';
 var b=enc?el('a','op-btn'+(kind==='open'?' op-btn--open':'')):btn(kind==='open'?'op-btn--open':'',kind==='open'?'open':'dl',label,label+' '+p.title);
 if(enc){b.href='#';b.setAttribute('role','button');b.setAttribute('aria-label',label+' '+p.title);b.appendChild(svg(I[kind==='open'?'open':'dl']));b.appendChild(el('span',null,label));
  var sp=ref&&safePath(ref.path);if(sp)b.setAttribute('data-enc-file',sp);if(kind!=='open')b.setAttribute('data-enc-download','')}
 else b.onclick=function(){kind==='open'?doOpen(p,b,host):doDownload(p,b,host)};
 return b}
function thumbInto(p,img,ph){
 if(!p.thumb){ph.classList.add('done');return}
 img.onload=function(){img.classList.add('on')};
 if(mode==='encrypted'){var sp=safePath(p.thumb.path);if(!sp){ph.classList.add('done');return}
  new MutationObserver(function(){if(img.dataset.encState==='error')ph.classList.add('done')}).observe(img,{attributes:true,attributeFilter:['data-enc-state']});
  img.setAttribute('data-enc-img',sp);return}
 getBlob(p.thumb).then(function(b){img.src=track(URL.createObjectURL(b))}).catch(function(){ph.classList.add('done')})}

function card(p,i){
 var c=el('article','op-card');c.setAttribute('aria-label',p.title);
 var th=el('div','op-thumb'),img=el('img'),ph=el('div','op-ph',typeOf(p));img.alt='';img.decoding='async';
 th.append(img,ph,el('span','op-type',typeOf(p)));c.appendChild(th);
 thumbInto(p,img,ph);
 var bd=el('div','op-body');bd.appendChild(el('h3','op-t',p.title));
 bd.appendChild(el('p','op-meta',typeOf(p)+' \u00b7 Updated '+fmtDate(p.updated)));
 var bs=el('div','op-btns'),o=act(p,'open',bd),d=act(p,'dl',bd);bs.append(o,d);bd.appendChild(bs);
 var hb=btn('op-btn--ho','ho','Hand off project');hb.onclick=function(){openHandoff(p,hb)};bd.appendChild(hb);
 var mb=el('button','op-more-btn');mb.type='button';mb.append(el('span',null,'Tell me more'),svg(I.chev));var id='op-d-'+i;mb.setAttribute('aria-expanded','false');mb.setAttribute('aria-controls',id);
 var dt=el('div','op-details');dt.id=id;dt.hidden=true;
 if(p.desc)dt.appendChild(el('p',null,p.desc));
 var bits=[];if(p.file&&p.file.name)bits.push(p.file.name);if(p.pages)bits.push(p.pages+(p.type&&/pptx?|key/i.test(p.type)?' slides':' pages'));if(p.size)bits.push(Math.max(1,Math.round(p.size/1024))+' KB');if(p.agent)bits.push('Pinned by '+p.agent);if(p.created&&p.created!==p.updated)bits.push('Added '+fmtDate(p.created));
 if(bits.length)dt.appendChild(el('small',null,bits.join(' \u00b7 ')));if(!dt.childNodes.length)dt.appendChild(el('p',null,'No extra details yet.'));
 mb.onclick=function(){var x=mb.getAttribute('aria-expanded')!=='true';mb.setAttribute('aria-expanded',String(x));dt.hidden=!x;mb.firstChild.textContent=x?'Show less':'Tell me more'};
 bd.append(mb,dt);c.appendChild(bd);return c}

function olderList(rest){
 var d=el('details','op-older'),s=el('summary');s.append(el('span',null,'More ('+rest.length+')'),svg(I.chev));d.appendChild(s);
 var ul=el('ul','op-list');rest.forEach(function(p){var li=el('li'),t=el('div','op-lt');t.append(el('b',null,p.title),el('span','op-meta',typeOf(p)+' \u00b7 '+fmtDate(p.updated)));
  li.append(t,act(p,'open',t),act(p,'dl',t));ul.appendChild(li)});
 d.appendChild(ul);return d}

function render(sec,list){
 sec.textContent='';sec.style.removeProperty('display');
 var hd=el('div','op-head'),h=el('h2','op-h');h.append(svg(I.folder),document.createTextNode('Ongoing Projects'));hd.appendChild(h);
 if(list.length)hd.appendChild(el('span','op-count','('+list.length+')'));
 var nav=el('div','op-nav'),pv=el('button'),nx=el('button');pv.type=nx.type='button';pv.setAttribute('aria-label','Previous projects');nx.setAttribute('aria-label','Next projects');pv.appendChild(svg(I.prev));nx.appendChild(svg(I.next));nav.append(pv,nx);hd.appendChild(nav);sec.appendChild(hd);
 if(!list.length){sec.appendChild(el('p','op-empty','No ongoing projects yet.'));nav.hidden=true;return}
 var tr=el('div','op-track');tr.setAttribute('role','list');tr.setAttribute('aria-label','Ongoing Projects');
 list.slice(0,MAX).forEach(function(p,i){var c=card(p,i);c.setAttribute('role','listitem');tr.appendChild(c)});sec.appendChild(tr);
 function upd(){pv.disabled=tr.scrollLeft<4;nx.disabled=tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4;nav.style.visibility=tr.scrollWidth>tr.clientWidth+4?'visible':'hidden'}
 function step(dir){var c=tr.querySelector('.op-card');tr.scrollBy({left:dir*(c?c.getBoundingClientRect().width+12:tr.clientWidth),behavior:'smooth'})}
 pv.onclick=function(){step(-1)};nx.onclick=function(){step(1)};tr.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);setTimeout(upd,50);
 if(list.length>MAX)sec.appendChild(olderList(list.slice(MAX)))}

function normalize(j){
 var a=(j&&Array.isArray(j.projects))?j.projects:[];
 return a.filter(function(p){return p&&p.title&&!p.hidden&&p.status!=='done'}).sort(function(x,y){return (Date.parse(y.updated)||0)-(Date.parse(x.updated)||0)})}

function load(src){
 return fetch(src+(src.indexOf('?')<0?'?':'&')+'t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(function(j){
  mode=storage[j.storage]?j.storage:'none';
  if(j.index){ /* encrypted index (planned default): titles, notes, filenames all live inside files/<random12>.enc */
   return getBlob({path:j.index}).then(function(b){return b.text()}).then(function(t){var d=JSON.parse(t);d.storage='encrypted';return d})}
  return j})}

function mount(){
 if(EXCLUDE.test(location.href))return null;
 var sec=document.getElementById('mw-projects')||document.querySelector('[data-mw-projects]');
 if(!sec){sec=el('section');sec.id='mw-projects'}
 sec.id='mw-projects';sec.style.removeProperty('display'); /* mw-layout hides EMPTY .mw-section blocks at layout time; ours fills async */
 sec.classList.add('mw-section','mw-projects');sec.setAttribute('data-mw-slot','projects');sec.setAttribute('aria-label','Ongoing Projects');
 var mid=document.getElementById('mw-mid');
 if(mid){if(mid.firstChild!==sec)mid.insertBefore(sec,mid.firstChild)}
 else{var div=document.querySelector('#mw-bh .mw-bh-divider'),bh=document.getElementById('mw-bh');if(bh)bh.after(sec);else if(!sec.parentNode)(document.querySelector('main')||document.body).prepend(sec)}
 return sec}

var started=false;
function start(){if(started)return;started=true;var sec=mount();if(!sec)return;
 var src=sec.getAttribute('data-mw-projects')||base();
 var ph=el('p','op-empty','Loading projects');sec.textContent='';sec.appendChild(ph);
 load(src).then(function(j){render(sec,normalize(j))}).catch(function(){render(sec,[])});
 /* mw-layout may rebuild #mw-mid later; keep the section first */
 document.addEventListener('mw-layout',function(){mount()})}
document.addEventListener('mw-layout',start);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(start,document.getElementById('mw-bh')?0:600)});else setTimeout(start,600);
window.ProjectsSection={v:V,storage:storage,setMode:function(m){if(storage[m])mode=m},render:render,normalize:normalize,safePath:safePath,handoffPayload:handoffPayload,openHandoff:openHandoff};
})();
