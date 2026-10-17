/* Document Center (R100; was Ongoing Projects; kit op8, Branding Agent, Oct 17 2026).
   op5 (R109 + R106 fold-down, Oct 17 2026 20:15 ICT): per-card Quick note (app "doc-note") and a closed-by-default fold-down header.
   op6 (R109b, Oct 17 2026 20:35 ICT): Quick note and Hand off on every 'More (n)' row too (same docNote/openHandoff code path and gating), so every document has a Note.
   op7 (R109c, Oct 17 2026 20:45 ICT, UpKeep): absolute https:// URLs in descriptions become links (linkify/safeLink: new URL() + protocol==='https:',
     built with createElement('a') + textContent, rel=noopener noreferrer, target=_blank); everything else is text nodes; no HTML-string APIs anywhere in the kit file.
   op8 (R111 + R109 add-on, Oct 17 2026 20:50 ICT, Max; Security requirements 20:45): Remove on every card and More row (in-page confirm first,
     app "doc-remove" {project_id,owner_agent,doc_id}, noQueue:true; no optimistic hide: 'Removal requested, waiting for <owner>', in-memory dim only;
     the card goes away only when the owner republishes projects.json via pin_project.py --unpin <id> --archive), and an in-page document view
     with a collapsible 'Note to <owner>' box (same docNote send path; never reads the document). Encrypted boards need the staged
     enc_file_viewer.js mwEncView hook (Security review) for the in-page view; without it they keep the old new-tab open.
   Needs submit.js at style-swipe 9921428 (sha256 9ec3cbd7...; doc-remove auth-gated incl. WellNest and never queued):
     <script src="https://webermanapps.github.io/style-swipe/submit.js?v=9921428"></script>
   Usage on a kit board (after mw-layout.js):
     <link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/projects.css?v=op8">
     script src=".../style-swipe/kit/projects.js?v=op8" data-projects="projects.json" defer (after mw-layout.js)
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
var V='op8',SUBMIT_PIN='9921428',MAX=6,EXCLUDE=/a-o956qercs5ubd57y|home-guide|finish-questions|room-photos|room-quiz|homes\.maxweberman\.com|share-x3l9xcxc1eut/;
var me=document.currentScript;
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e}
/* op7: icons are built as SVG nodes from fixed path data (no HTML strings) */
var NS='http://www.w3.org/2000/svg';
function svg(d){var s=document.createElementNS(NS,'svg');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('aria-hidden','true');[].concat(d).forEach(function(x){var q=document.createElementNS(NS,'path');q.setAttribute('d',x);s.appendChild(q)});return s}
var I={folder:['M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z'],open:['M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5'],
 dl:['M12 4v11M7 10l5 5 5-5M5 20h14'],ho:['M4 12h12M12 6l6 6-6 6','M20 5v14'],doc:['M7 3h7l5 5v12a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1z','M14 3v5h5M9 13h6M9 17h6'],chev:['M6 9l6 6 6-6'],note:['M4 20h4L19 9l-4-4L4 16z','M13 7l4 4'],prev:['M15 6l-6 6 6 6'],rm:['M4 7h16','M10 11v6M14 11v6','M6 7l1 13h10l1-13','M9 7V4h6v3'],next:['M9 6l6 6-6 6']};
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
/* doc-type badge (op4). Untrusted input: p.type is checked against a fixed whitelist, else derived from type/MIME/extension;
   anything unknown is 'other'. Labels come only from KIND and are set with textContent. */
var KIND={pdf:'PDF',ppt:'PPT',doc:'DOC',xls:'XLS',img:'IMG',other:'FILE'};
function kindOf(p){var t=String(p.type||'').toLowerCase();if(Object.prototype.hasOwnProperty.call(KIND,t))return t;
 var f=p.file||{},m=String(f.mime||'').toLowerCase(),e=String(f.name||'').toLowerCase().split('.').pop(),s=t+' '+e;
 if(/\bpdf\b/.test(s)||m==='application/pdf')return 'pdf';
 if(/\b(pptx?|odp|key)\b/.test(s)||/presentation|powerpoint/.test(m))return 'ppt';
 if(/\b(docx?|odt|rtf)\b/.test(s)||/wordprocessing|msword|opendocument\.text/.test(m))return 'doc';
 if(/\b(xlsx?|ods|csv)\b/.test(s)||/spreadsheet|ms-excel|text\/csv/.test(m))return 'xls';
 if(/\b(png|jpe?g|gif|webp|heic)\b/.test(s)||/^image\//.test(m))return 'img';
 return 'other'}
function docDate(p){var d=String(p.date||'');return d?fmtDate(/^\d{4}-\d{2}-\d{2}$/.test(d)?d+'T12:00:00':d):'Updated '+fmtDate(p.updated)}

var urls=[];function track(u){urls.push(u);return u}
addEventListener('pagehide',function(){urls.forEach(function(u){try{URL.revokeObjectURL(u)}catch(_){}})});

function busy(b,on){b.setAttribute('aria-busy',on?'true':'false');b.disabled=!!on}
function note(card,msg){var m=card.querySelector('.op-msg');if(!m){m=el('p','op-msg');m.setAttribute('role','status');card.appendChild(m)}m.textContent=msg}
function doOpen(p,btn,host){
 var ref=p.preview||p.file;if(!ref)return;
 if(viewKind(ref.mime||(p.preview?'application/pdf':''))){busy(btn,true); /* op8: in-page view (no popup needed) */
  getBlob(ref).then(function(b){var u=track(URL.createObjectURL(b));if(!openView(p,u,b.type||ref.mime,btn))location.assign(u)})
  .catch(function(e){note(host,e.message)}).then(function(){busy(btn,false)});return}
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
   results={project_id,owner_agent,to_agents,note}. Security condition (5), Oct 17 2026: NO title, filenames, paths or page URL over
   the wire; Grok Bot resolves those from the private project list on the box (ops/brand/projects-private).
   Hidden where sending is not trusted yet: HANDOFF_OFF agents (none now; WellNest re-enabled op3), a board's
   section attribute data-mw-handoff="off", or projects.json "handoff": false. Boards cannot switch it back on; only a kit change can. */
var HANDOFF_OFF={};
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
function handoffPayload(p,to,note){return{project_id:p.id,owner_agent:ownerAgent(p),to_agents:to.map(function(t){return t.slug}),note:note||''}}
var handoffBoardOff=false;
function handoffAllowed(p){var o=String(ownerAgent(p)||'').toLowerCase();return !handoffBoardOff&&!HANDOFF_OFF[o]}
function listNames(a){a=a.map(function(t){return t.name});return a.length<2?a.join(''):a.slice(0,-1).join(', ')+' and '+a[a.length-1]}
var hoOpen=null;
function openHandoff(p,opener){
 if(hoOpen)hoOpen.close();
 var bg=el('div','op-ho-bg'),box=el('form','op-ho');box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-labelledby','op-ho-t');box.noValidate=true;box.autocomplete='off';
 var x=el('button','op-ho-x');x.type='button';x.setAttribute('aria-label','Close');x.appendChild(svg('M6 6l12 12M18 6L6 18'));
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
  Promise.resolve().then(function(){return S.send({agent:body.owner_agent||'grok-bot',app:'project-handoff',deck:p.id,results:body,notes:''})})
  .then(function(ok){if(ok){setState('sent','Sent to '+who+'.')}
   else if(S.blocked){setState('fail','Password needed. Nothing was sent.')}
   else{setState('fail','Not sent yet: no connection. It is saved on this device and retries when you are back online, or tap Try Again.')}})
  .catch(function(){setState('fail','Something went wrong. Nothing was sent. Tap Try Again.')})});
 loadTeam().then(function(){if(document.activeElement===inp)show()});
 setState('idle');setTimeout(function(){inp.focus()},30);
 hoOpen={close:close};return hoOpen}

/* ---- Quick note (R109, Max Oct 17 2026 20:15 ICT; Security checklist Oct 17 2026) ----
   Sibling of Hand off: posts via the same MWSubmit.send (submit.js, auth-gated; WellNest doc-note gated, and noQueue so doc-notes are never put in the retry queue, since submit.js b06c43f) to the same
   receiver: agent=<owner>, app="doc-note", deck=<project id>, results={project_id,owner_agent,note}. Nothing else from the card or page.
   Note is trimmed and capped at NOTE_MAX. Never written to the page after sending, never kept in localStorage/sessionStorage:
   no-connection sends are refused up front, every send passes noQueue:true (submit.js b06c43f), and any legacy doc-note queue entry is purged on load.
   Hidden where sending is not trusted: DOCNOTE_OFF agents, section data-mw-docnote="off", or projects.json "docnote": false.
   Boards cannot switch it back on; only a kit change can. */
var DOCNOTE_OFF={}; /* R109: WellNest enabled after Security clearance (submit.js b06c43f auth-gates doc-note for WellNest). Add "slug":1 to hide an agent. */
var NOTE_MAX=500,QK_SUBMIT='mw-submit-queue',docnoteBoardOff=false;
function docnotePayload(p,note){return{project_id:p.id,owner_agent:ownerAgent(p),note:String(note||'').trim().slice(0,NOTE_MAX)}}
function docnoteAllowed(p){var o=String(ownerAgent(p)||'').toLowerCase();return !docnoteBoardOff&&!DOCNOTE_OFF[o]&&!DOCNOTE_OFF[slugify(o)]}
/* op8: also drops any doc-remove entry (submit.js 9921428 never queues them; belt and braces) */
function purgeNoteQueue(){try{var a=JSON.parse(localStorage.getItem(QK_SUBMIT)||'[]');if(!Array.isArray(a))return;var k=a.filter(function(x){return!(x&&(x.app==='doc-note'||x.app==='doc-remove'))});
 if(k.length!==a.length){if(k.length)localStorage.setItem(QK_SUBMIT,JSON.stringify(k));else localStorage.removeItem(QK_SUBMIT)}}catch(_){}}
var dnSeq=0;
/* row=true (op6, More rows): same control; wrapper is display:contents so the Note button sits in the row and the form/status wrap below it */
/* row='view' (op8): the collapsible 'Note to <owner>' box inside the document view; same form, same send path */
function docNote(p,row){
 var view=row==='view',lbl=view?'Note to '+ownerName(p):'Note';
 var n=++dnSeq,w=el('div','op-dn'+(view?' op-dn--view':row?' op-dn--row':'')),ob=btn('op-dn-btn','note',lbl,view?lbl:row?'Quick note on '+p.title:'Quick note');ob.setAttribute('aria-expanded','false');
 var f=el('form','op-dn-form');f.id='op-dn-f'+n;f.hidden=true;f.noValidate=true;f.autocomplete='off';ob.setAttribute('aria-controls',f.id);
 var lb=el('label','op-dn-l',view?lbl:'Quick note');lb.htmlFor='op-dn-t'+n;
 var ta=el('textarea','op-dn-ta');ta.id='op-dn-t'+n;ta.rows=3;ta.maxLength=NOTE_MAX;ta.placeholder='Type a short note';ta.setAttribute('autocomplete','off');ta.setAttribute('aria-describedby','op-dn-c'+n);
 var ct=el('span','op-dn-count');ct.id='op-dn-c'+n;
 var row=el('div','op-dn-row'),cx=el('button','op-dn-b','Cancel'),sd=el('button','op-dn-b op-dn-send','Send');cx.type='button';sd.type='submit';row.append(cx,sd);
 var ft=el('div','op-dn-ft');ft.append(ct,row);f.append(lb,ta,ft);
 var msg=el('p','op-dn-msg');msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');msg.hidden=true;
 w.append(ob,f,msg);
 var sending=false,tm=0;
 function count(){var l=ta.value.length;ct.textContent=l+' / '+NOTE_MAX;ct.classList.toggle('op-dn-near',l>=NOTE_MAX-50);if(!sending)sd.disabled=!ta.value.trim()}
 function say(t,kind){clearTimeout(tm);msg.className='op-dn-msg'+(kind?' '+kind:'');msg.textContent=t;msg.hidden=!t;if(kind==='ok')tm=setTimeout(function(){msg.hidden=true;msg.textContent=''},4000)}
 function open(){f.hidden=false;ob.setAttribute('aria-expanded','true');ob.classList.add('on');say('');count();setTimeout(function(){ta.focus()},0)}
 function shut(clear){if(sending)return;f.hidden=true;ob.setAttribute('aria-expanded','false');ob.classList.remove('on');if(clear)ta.value='';count();ob.focus()}
 ob.onclick=function(){f.hidden?open():shut(false)};
 cx.onclick=function(){say('');shut(true)};
 ta.addEventListener('input',function(){count();if(msg.classList.contains('err'))say('')});
 ta.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();cx.click()}else if(e.key==='Enter'&&(e.metaKey||e.ctrlKey)){e.preventDefault();f.requestSubmit?f.requestSubmit():sd.click()}});
 function busyN(on){sending=on;sd.setAttribute('aria-busy',on?'true':'false');sd.textContent=on?'Sending':'Send';sd.disabled=on;cx.disabled=on;ta.readOnly=on;if(!on)count()}
 f.addEventListener('submit',function(e){e.preventDefault();if(sending)return;
  var body=docnotePayload(p,ta.value);if(!body.note){say('Type a note first.','err');ta.focus();return}
  var S=window.MWSubmit;if(!S||typeof S.send!=='function'){say('Sending is not set up on this page yet. Nothing was sent.','err');return}
  if(navigator.onLine===false){say('No connection. Nothing was sent. Try again when you are online.','err');return}
  busyN(true);say('');
  Promise.resolve().then(function(){return S.send({agent:body.owner_agent||'grok-bot',app:'doc-note',deck:p.id,results:body,notes:'',noQueue:true})})
  .then(function(ok){purgeNoteQueue();busyN(false);
   if(ok){ta.value='';count();f.hidden=true;ob.setAttribute('aria-expanded','false');ob.classList.remove('on');ob.focus();say('Note sent','ok')}
   else if(S.blocked){say('Password needed. Nothing was sent.','err');ta.focus()}
   else{say('Not sent: no connection. Your text is still here. Try again.','err');ta.focus()}})
  .catch(function(){purgeNoteQueue();busyN(false);say('Something went wrong. Nothing was sent. Try again.','err');ta.focus()})});
 count();return w}

/* ---- op7 (R109c, UpKeep): safe links in descriptions. Untrusted input (projects.json desc).
   Only absolute https:// URLs become links; a URL glued to a scheme/word (e.g. "javascript:https://...") stays text.
   Trailing punctuation (.,;:!?'" quotes, unbalanced closing brackets) is left outside the link.
   href is set only from new URL(); protocol must be exactly 'https:', a host is required, no user:pass@.
   javascript:, data:, http: and anything else never match and stay plain text. Link text via textContent; no HTML is ever parsed. */
var URL_RE=/https:\/\/[^\s<>"'`\u0000-\u001f\u007f]+/gi,URL_MAX=2048;
function trimUrl(u){var t,o;while(u.length){t=u.charAt(u.length-1);
  if(/[.,;:!?'"\u2018\u2019\u201c\u201d\u00bb*]/.test(t)){u=u.slice(0,-1);continue}
  o={')':'(',']':'[','}':'{'}[t];if(o&&u.split(o).length<u.split(t).length){u=u.slice(0,-1);continue}
  break}return u}
function safeLink(s){if(typeof s!=='string'||s.length<9||s.length>URL_MAX)return null;var u;try{u=new URL(s)}catch(_){return null}
 if(u.protocol!=='https:'||!u.hostname||u.username||u.password)return null;
 var a=document.createElement('a');a.href=u.href;a.textContent=s;a.rel='noopener noreferrer';a.target='_blank';a.className='op-link';return a}
function linkify(txt){var s=String(txt==null?'':txt),f=document.createDocumentFragment(),last=0,m,re=new RegExp(URL_RE.source,'gi');
 while((m=re.exec(s))){var i=m.index,pre=i?s.charAt(i-1):'';
  if(pre&&/[\w:\/.@%+~&=#-]/.test(pre))continue; /* glued to a scheme or word: not a standalone https URL */
  var u=trimUrl(m[0]),a=safeLink(u);if(!a)continue;
  if(i>last)f.appendChild(document.createTextNode(s.slice(last,i)));
  f.appendChild(a);last=i+u.length;re.lastIndex=last}
 if(last<s.length)f.appendChild(document.createTextNode(s.slice(last)));
 return f}

/* ---- Remove (R111, op8; Max Oct 17 2026; Security requirements 20:45 ICT) ----
   Confirm first: the Remove button only opens an in-page confirm (no window.confirm) naming the title via textContent; Cancel or Remove.
   A confirmed remove posts MWSubmit.send app "doc-remove", deck=<project id>, results exactly {project_id,owner_agent,doc_id}
   (doc_id = the projects.json entry id; no titles or file names), noQueue:true. submit.js 9921428 auth-gates doc-remove (WellNest too) and never queues it.
   The board deletes nothing: on success it shows 'Removal requested, waiting for <owner>' and dims the card/row in memory only (nothing stored).
   The card really goes away only when the owner agent archives it (pin_project.py <agent> --unpin <id> --archive) and republishes projects.json.
   Gating like Hand off / Quick note: REMOVE_OFF agents, section data-mw-docremove="off", or projects.json "docremove": false. Only a kit change turns it back on. */
var REMOVE_OFF={},removeBoardOff=false,rmSeq=0;
function removePayload(p){var id=String(p.id||'');return{project_id:id,owner_agent:ownerAgent(p),doc_id:id}}
function removeAllowed(p){var o=String(ownerAgent(p)||'').toLowerCase();return !removeBoardOff&&!REMOVE_OFF[o]&&!REMOVE_OFF[slugify(o)]}
function ownerName(p){var o=String(ownerAgent(p)||''),s=slugify(o),t=(team||[]).filter(function(x){return x.slug===s})[0];return (t&&t.name)||TEAM_FALLBACK[s]||o||'the owner'}
function docRemove(p,host,row){
 var n=++rmSeq,w=el('div','op-rm'+(row?' op-rm--row':'')),ob=btn('op-rm-btn','rm','Remove','Remove '+p.title);ob.setAttribute('aria-expanded','false');
 var cf=el('div','op-rm-cf');cf.id='op-rm-c'+n;cf.hidden=true;cf.setAttribute('role','group');ob.setAttribute('aria-controls',cf.id);
 var q=el('p','op-rm-q');q.id='op-rm-q'+n;q.append(document.createTextNode('Remove '),el('b',null,'\u201c'+p.title+'\u201d'),document.createTextNode(' from the Document Center?'));cf.setAttribute('aria-labelledby',q.id);
 var hint=el('p','op-rm-hint','Sends a request to '+ownerName(p)+', who archives it. Nothing is deleted.');
 var r=el('div','op-rm-row'),cx=el('button','op-rm-b op-rm-cancel','Cancel'),go=el('button','op-rm-b op-rm-go','Remove');cx.type='button';go.type='button';r.append(cx,go);cf.append(q,hint,r);
 var msg=el('p','op-rm-msg');msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');msg.hidden=true;
 w.append(ob,cf,msg);
 var sending=false,done=false;
 function say(t,k){msg.className='op-rm-msg'+(k?' '+k:'');msg.textContent=t;msg.hidden=!t}
 function open(){if(done)return;cf.hidden=false;ob.setAttribute('aria-expanded','true');ob.classList.add('on');say('');setTimeout(function(){cx.focus()},0)}
 function shut(){if(sending)return;cf.hidden=true;ob.setAttribute('aria-expanded','false');ob.classList.remove('on');ob.focus()}
 ob.onclick=function(){cf.hidden?open():shut()};cx.onclick=function(){say('');shut()};
 cf.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();cx.click()}});
 go.onclick=function(){if(sending||done)return;
  var S=window.MWSubmit;if(!S||typeof S.send!=='function'){say('Sending is not set up on this page yet. Nothing was sent.','err');return}
  if(navigator.onLine===false){say('No connection. Nothing was sent. Try again when you are online.','err');return}
  var body=removePayload(p);if(!body.project_id){say('This document has no id. Nothing was sent.','err');return}
  sending=true;go.disabled=true;cx.disabled=true;go.textContent='Sending';go.setAttribute('aria-busy','true');say('');
  Promise.resolve().then(function(){return S.send({agent:body.owner_agent||'grok-bot',app:'doc-remove',deck:body.project_id,results:body,notes:'',noQueue:true})})
  .then(function(ok){return ok?'ok':(S.blocked?'blocked':'fail')},function(){return 'fail'})
  .then(function(res){purgeNoteQueue();sending=false;go.removeAttribute('aria-busy');go.textContent='Remove';go.disabled=false;cx.disabled=false;
   if(res==='ok'){done=true;cf.hidden=true;ob.setAttribute('aria-expanded','false');ob.classList.remove('on');ob.disabled=true;ob.lastChild.textContent='Requested';
    host.classList.add('op-rm-pending');say('Removal requested, waiting for '+ownerName(p)+'.','ok')}
   else if(res==='blocked'){say('Password needed. Nothing was sent.','err');go.focus()}
   else{say('Not sent. Check your connection and try again.','err');go.focus()}})};
 return w}

/* ---- Document view + 'Note to <owner>' (R109 add-on, op8, Max) ----
   Viewable types (PDF, PNG/JPEG/GIF/WebP, plain text) open in an in-page view instead of a new tab, with a collapsible
   'Note to <owner>' box under the document: docNote(p,'view'), i.e. the same doc-note send path, payload {project_id,owner_agent,note},
   noQueue, NOTE_MAX, same gating. The box holds no reference to the document: only a blob: URL is placed in iframe/img src; the kit never
   reads the decrypted bytes. Encrypted boards: the staged enc_file_viewer.js calls window.mwEncView({url,mime},link) (Security review). */
var dvOpen=null,linkProj=typeof WeakMap==='function'?new WeakMap():null;
function viewKind(m){m=String(m||'').toLowerCase().split(';')[0].trim();return m==='application/pdf'?'pdf':/^image\/(png|jpe?g|gif|webp)$/.test(m)?'img':m==='text/plain'?'txt':''}
function openView(p,url,mime,opener){
 var k=viewKind(mime);if(!k||typeof url!=='string'||url.indexOf('blob:')!==0)return false;
 if(dvOpen)dvOpen.close();
 var bg=el('div','op-dv-bg'),box=el('div','op-dv');box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-labelledby','op-dv-t');
 var hd=el('div','op-dv-hd'),h=el('h2','op-dv-h',p.title);h.id='op-dv-t';
 var nt=el('a','op-dv-tab');nt.href=url;nt.target='_blank';nt.rel='noopener noreferrer';nt.append(svg(I.open),el('span',null,'New tab'));nt.setAttribute('aria-label','Open '+p.title+' in a new tab');
 var x=el('button','op-dv-x');x.type='button';x.setAttribute('aria-label','Close');x.appendChild(svg('M6 6l12 12M18 6L6 18'));hd.append(h,nt,x);
 var dv=el('div','op-dv-doc op-dv-'+k);
 if(k==='img'){var im=el('img');im.alt=p.title;im.src=url;dv.appendChild(im)}
 else{var fr=el('iframe');fr.title=p.title;if(k==='txt')fr.setAttribute('sandbox','');fr.src=url;dv.appendChild(fr)}
 box.append(hd,dv);if(docnoteAllowed(p))box.appendChild(docNote(p,'view'));
 bg.appendChild(box);(document.getElementById('mw-projects')||document.body).appendChild(bg);document.documentElement.classList.add('op-ho-lock');
 function close(){document.removeEventListener('keydown',esc);bg.remove();document.documentElement.classList.remove('op-ho-lock');dvOpen=null;try{opener&&opener.focus()}catch(_){}}
 function esc(e){if(e.defaultPrevented)return;if(e.key==='Escape'){close();return}
  if(e.key==='Tab'){var f=[].filter.call(box.querySelectorAll('a[href],button,textarea'),function(n){return!n.disabled&&!n.hidden&&n.offsetParent});if(!f.length)return;var a=f[0],z=f[f.length-1];
   if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}}
 document.addEventListener('keydown',esc);x.onclick=close;bg.addEventListener('mousedown',function(e){if(e.target===bg)close()});
 setTimeout(function(){x.focus()},30);dvOpen={close:close};return true}
/* hook for the staged enc_file_viewer.js: gets only {url (blob:), mime} and the clicked link; returns true when shown here */
window.mwEncView=function(f,link){var p=linkProj&&link&&linkProj.get(link);if(!p||!f)return false;return openView(p,f.url,f.mime,link)};

function btn(cls,icon,label,aria){var b=el('button','op-btn '+cls);b.type='button';b.appendChild(svg(I[icon]));b.appendChild(el('span',null,label));if(aria)b.setAttribute('aria-label',aria);return b}

/* encrypted mode uses Security's documented markup exactly: Open = a[data-enc-file], Download = a[data-enc-file][data-enc-download],
   thumbnail = img[data-enc-img]. enc_file_viewer.js handles clicks (global capture listener) and image decryption. */
function act(p,kind,host){var enc=mode==='encrypted',ref=kind==='open'?(p.preview||p.file):p.file,label=kind==='open'?'Open':'Download';
 var b=enc?el('a','op-btn'+(kind==='open'?' op-btn--open':'')):btn(kind==='open'?'op-btn--open':'',kind==='open'?'open':'dl',label,label+' '+p.title);
 if(enc){if(linkProj&&kind==='open')linkProj.set(b,p);b.href='#';b.setAttribute('role','button');b.setAttribute('aria-label',label+' '+p.title);b.appendChild(svg(I[kind==='open'?'open':'dl']));b.appendChild(el('span',null,label));
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
 var k=kindOf(p);c.classList.add('op-k-'+k);th.append(img,ph,el('span','op-type',KIND[k]));c.appendChild(th);
 thumbInto(p,img,ph);
 var bd=el('div','op-body');bd.appendChild(el('h3','op-t',p.title));
 bd.appendChild(el('p','op-meta',docDate(p)));
 var bs=el('div','op-btns'),o=act(p,'open',bd),d=act(p,'dl',bd);bs.append(o,d);bd.appendChild(bs);
 if(handoffAllowed(p)){var hb=btn('op-btn--ho','ho','Hand off project');hb.onclick=function(){openHandoff(p,hb)};bd.appendChild(hb)}
 if(docnoteAllowed(p))bd.appendChild(docNote(p));
 if(removeAllowed(p))bd.appendChild(docRemove(p,c));
 var mb=el('button','op-more-btn');mb.type='button';mb.append(el('span',null,'Tell me more'),svg(I.chev));var id='op-d-'+i;mb.setAttribute('aria-expanded','false');mb.setAttribute('aria-controls',id);
 var dt=el('div','op-details');dt.id=id;dt.hidden=true;
 if(p.desc){var dp=el('p','op-desc');dp.appendChild(linkify(p.desc));dt.appendChild(dp)}
 var bits=[];if(p.file&&p.file.name)bits.push(p.file.name);if(p.pages)bits.push(p.pages+(p.type&&/pptx?|key/i.test(p.type)?' slides':' pages'));if(p.size)bits.push(Math.max(1,Math.round(p.size/1024))+' KB');if(p.agent)bits.push('Pinned by '+p.agent);if(p.created&&p.created!==p.updated)bits.push('Added '+fmtDate(p.created));
 if(bits.length)dt.appendChild(el('small',null,bits.join(' \u00b7 ')));if(!dt.childNodes.length)dt.appendChild(el('p',null,'No extra details yet.'));
 mb.onclick=function(){var x=mb.getAttribute('aria-expanded')!=='true';mb.setAttribute('aria-expanded',String(x));dt.hidden=!x;mb.firstChild.textContent=x?'Show less':'Tell me more'};
 bd.append(mb,dt);c.appendChild(bd);return c}

function olderList(rest){
 var d=el('details','op-older'),s=el('summary');s.append(el('span',null,'More ('+rest.length+')'),svg(I.chev));d.appendChild(s);
 var ul=el('ul','op-list');rest.forEach(function(p){var li=el('li'),t=el('div','op-lt');var k=kindOf(p);li.className='op-k-'+k;t.append(el('b',null,p.title),el('span','op-meta',KIND[k]+' \u00b7 '+docDate(p)));
  li.append(t,act(p,'open',t),act(p,'dl',t));
  if(handoffAllowed(p)){var hb=btn('op-btn--ho op-ho-row','ho','Hand off','Hand off '+p.title);hb.onclick=function(){openHandoff(p,hb)};li.appendChild(hb)}
  if(docnoteAllowed(p))li.appendChild(docNote(p,true));
  if(removeAllowed(p))li.appendChild(docRemove(p,li,true));ul.appendChild(li)});
 d.appendChild(ul);return d}

/* op5 fold-down (Max Oct 17 2026 20:16 ICT): same look as the Morning Report / To-Do List fold-downs (48px summary row, title + count + chevron),
   closed by default; cards (with Hand off and Quick note) live inside. */
function render(sec,list){
 sec.textContent='';sec.style.removeProperty('display');sec.classList.add('op-has-fold');
 var fd=el('details','op-fold'),sm=el('summary','op-fold-sum'),fb=el('div','op-fold-body');fd.id='mw-docs-fold';
 sm.append(el('span','op-fold-t','Document Center'),el('span','op-fold-n',list.length?'('+list.length+')':''),el('span','op-chev'));fd.append(sm,fb);sec.appendChild(fd);
 var hd=el('div','op-head');
 var tt=el('div','op-ttl');tt.appendChild(el('p','op-sub','Your agent\u2019s working documents'));hd.appendChild(tt);
 var nav=el('div','op-nav'),pv=el('button'),nx=el('button');pv.type=nx.type='button';pv.setAttribute('aria-label','Previous documents');nx.setAttribute('aria-label','Next documents');pv.appendChild(svg(I.prev));nx.appendChild(svg(I.next));nav.append(pv,nx);hd.appendChild(nav);fb.appendChild(hd);
 if(!list.length){var em=el('div','op-empty op-empty--box');em.append(svg(I.doc),el('p',null,'No documents yet. Your agent will pin PDFs, slides and docs here as it makes them.'));fb.appendChild(em);nav.hidden=true;return}
 var tr=el('div','op-track');tr.setAttribute('role','list');tr.setAttribute('aria-label','Document Center');
 list.slice(0,MAX).forEach(function(p,i){var c=card(p,i);c.setAttribute('role','listitem');tr.appendChild(c)});fb.appendChild(tr);
 function upd(){pv.disabled=tr.scrollLeft<4;nx.disabled=tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4;nav.style.visibility=tr.scrollWidth>tr.clientWidth+4?'visible':'hidden'}
 function step(dir){var c=tr.querySelector('.op-card');tr.scrollBy({left:dir*(c?c.getBoundingClientRect().width+12:tr.clientWidth),behavior:'smooth'})}
 pv.onclick=function(){step(-1)};nx.onclick=function(){step(1)};tr.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);fd.addEventListener('toggle',function(){if(fd.open)setTimeout(upd,0)});setTimeout(upd,50);
 if(list.length>MAX)fb.appendChild(olderList(list.slice(MAX)))}

function normalize(j){
 var a=(j&&Array.isArray(j.projects))?j.projects:[];
 return a.filter(function(p){return p&&p.title&&!p.hidden&&p.status!=='done'}).sort(function(x,y){return (Date.parse(y.updated)||0)-(Date.parse(x.updated)||0)})}

function load(src){
 return fetch(src+(src.indexOf('?')<0?'?':'&')+'t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(function(j){
  mode=storage[j.storage]?j.storage:'none';if(j.handoff===false)handoffBoardOff=true;if(j.docnote===false)docnoteBoardOff=true;if(j.docremove===false)removeBoardOff=true;
  if(j.index){ /* encrypted index (planned default): titles, notes, filenames all live inside files/<random12>.enc */
   return getBlob({path:j.index}).then(function(b){return b.text()}).then(function(t){var d=JSON.parse(t);d.storage='encrypted';return d})}
  return j})}

function mount(){
 if(EXCLUDE.test(location.href))return null;
 var sec=document.getElementById('mw-projects')||document.querySelector('[data-mw-projects]');
 if(!sec){sec=el('section');sec.id='mw-projects'}
 sec.id='mw-projects';sec.style.removeProperty('display'); /* mw-layout hides EMPTY .mw-section blocks at layout time; ours fills async */
 sec.classList.add('mw-section','mw-projects');sec.setAttribute('data-mw-slot','projects');sec.setAttribute('aria-label','Document Center');
 var mid=document.getElementById('mw-mid');
 if(mid){if(mid.firstChild!==sec)mid.insertBefore(sec,mid.firstChild)}
 else{var div=document.querySelector('#mw-bh .mw-bh-divider'),bh=document.getElementById('mw-bh');if(bh)bh.after(sec);else if(!sec.parentNode)(document.querySelector('main')||document.body).prepend(sec)}
 return sec}

var started=false;
function start(){if(started)return;started=true;var sec=mount();if(!sec)return;
 var src=sec.getAttribute('data-mw-projects')||base();if(sec.getAttribute('data-mw-handoff')==='off')handoffBoardOff=true;if(sec.getAttribute('data-mw-docnote')==='off')docnoteBoardOff=true;if(sec.getAttribute('data-mw-docremove')==='off')removeBoardOff=true;purgeNoteQueue();
 var ph=el('p','op-empty','Loading documents');sec.textContent='';sec.appendChild(ph);
 load(src).then(function(j){render(sec,normalize(j))}).catch(function(){render(sec,[])});
 /* mw-layout may rebuild #mw-mid later; keep the section first */
 document.addEventListener('mw-layout',function(){mount()})}
document.addEventListener('mw-layout',start);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(start,document.getElementById('mw-bh')?0:600)});else setTimeout(start,600);
window.ProjectsSection={v:V,storage:storage,setMode:function(m){if(storage[m])mode=m},render:render,normalize:normalize,safePath:safePath,handoffPayload:handoffPayload,openHandoff:openHandoff,docnotePayload:docnotePayload,docnoteAllowed:docnoteAllowed,linkify:linkify,safeLink:safeLink,removePayload:removePayload,removeAllowed:removeAllowed,openView:openView,submitPin:SUBMIT_PIN};
})();
