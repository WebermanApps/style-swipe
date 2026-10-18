/* Board layout kit ly4 (STRICT, Max Oct 16 2026 13:21 + 13:22 ICT, rulebook R79; earlier R76 12:09, Apps Home button R77 12:39).
   BRANDED HEADER and BRANDED FOOTER are built here as body-level blocks, pixel-identical on every agent board, colors included
   (Max's white + light beige). Board CSS cannot restyle them: scoped ids #mw-bh / #mw-bf + !important locks in mw-layout.css.
   BRANDED HEADER (#mw-bh.mw-branded-header): Apps Home button (.mw-bh-home) > Command Center header (.mw-bh-cc: logo, '<Name> Command Center', description)
     > decks shelf + deck counter (.mw-bh-decks; counter shows 0 when no stats) > Working On dropdown (.mw-bh-working, R85: only while the board's agent is working, closed by default, data kit/agent-status.json) > Morning Report dropdown (.mw-bh-morning, closed by default)
     > divider (.mw-bh-divider: 1px #e3ddd2, full content width, equal spacing).
   MIDDLE: everything else, incl. ALL agent-specific branding (brand colors, special sections, photos, video). [data-mw-slot="hero"] items go first.
   BRANDED FOOTER (#mw-bf.mw-branded-footer): divider (.mw-bf-divider, same as header's) > Routines (.mw-bf-routines) > standard footer (.mw-bf-standard: Share + mark + 'Built by Machan' -> maxweberman.com; ly5 Oct 16 2026, Branding Agent).
   Per-board differences allowed in the header: logo, name, description (plus deck / report / routine content).
   Markers (optional): data-mw-slot="shelf|morning|hero|routines". Old footers are folded into the middle; old Apps Home links removed.
   Agent boards only (Apps Home, deck pages and the share page never load this file).
   Usage: <link rel="stylesheet" href=".../kit/mw-layout.css?v=ly8"><script src=".../kit/mw-layout.js?v=ly8" defer></script> (ly9 ships under the same URLs)
   ly9 (Team Improvement Deck results, Max Oct 16 2026; Branding Oct 17): Share is a small icon in the Command Center header (footer Share button removed);
   a slim header bar stays at the top for about one screen of scrolling, then goes away; Morning Report shows a square Late tag (report.json late/minutes_late)
   and up to three headline cards (report.json headlines or top3); a board block marked data-mw-slot="todo" becomes the 'To-Do List' section, first in the middle.
   ly12 (Oct 17 2026, Branding): R106 header order (Morning Report > To-Do List fold-down > Document Center > divider) and R104 (loads kit/mw-back.js).
   ly14 (Oct 17 2026, Branding; R106 rollout, needs Security review): R106 flag ON. To-Do count prefers the source's own summary/heading number
   (Grok Bot pages its list 10 at a time, so a li count undercounts); an empty To-Do source gets a plain-text empty line. DOM work is node moves only
   (appendChild/insertBefore of the board's existing nodes) plus kit-made elements filled with textContent; no innerHTML from board or JSON data. */
(function(){
var V='ly14',R106=true/* R106 ON in ly13 (Security cleared the Document Center fold-down in projects.js op5, e58b17a) */,MACHAN="<span class=\"mw-machan\" style=\"display:inline-flex;align-items:center;gap:6px;vertical-align:middle;white-space:nowrap\"><svg class=\"mw-machan-mark\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" aria-hidden=\"true\" focusable=\"false\" style=\"display:block;flex:none;width:22px;height:22px\"><path d=\"M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z\" fill=\"#3F7D58\"/><path d=\"M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z\" fill=\"#5E9A6E\"/><rect x=\"3.5\" y=\"5.5\" width=\"17\" height=\"16\" rx=\"7\" fill=\"#C8643F\"/><rect x=\"5.5\" y=\"9\" width=\"13\" height=\"10\" rx=\"5\" fill=\"#FAF6EE\"/><circle cx=\"9.6\" cy=\"13.3\" r=\"1.35\" fill=\"#2E6F86\"/><path d=\"M13 13.1q1.4 1.25 2.8 0\" fill=\"none\" stroke=\"#2E6F86\" stroke-width=\"1.1\" stroke-linecap=\"round\"/><path d=\"M10.6 16.1q1.4 1.1 2.8 0\" fill=\"none\" stroke=\"#C8643F\" stroke-width=\"1.1\" stroke-linecap=\"round\"/><circle cx=\"7.6\" cy=\"15.6\" r=\".9\" fill=\"#E9B9A3\"/><circle cx=\"16.4\" cy=\"15.6\" r=\".9\" fill=\"#E9B9A3\"/></svg>Built by Machan</span>",K='https://webermanapps.github.io/style-swipe/kit/',HOME='https://webermanapps.github.io/a-o956qercs5ubd57y/';
var q=function(s,r){return (r||document).querySelector(s)},qa=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var slot=function(n){return q('[data-mw-slot="'+n+'"]')};var MR=/^\s*morning report/i;
function mk(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function need(f,css){var sel=css?'link[rel=stylesheet]':'script[src]';if(qa(sel).some(function(e){return (e.href||e.src||'').indexOf('/kit/'+f)>=0}))return;
 var e;if(css){e=mk('link');e.rel='stylesheet';e.href=K+f+'?v='+V}else{e=mk('script');e.src=K+f+'?v='+V}document.head.appendChild(e)}
function fonts(){if(q('link[data-mw-fonts]'))return;var l=mk('link');l.rel='stylesheet';l.setAttribute('data-mw-fonts','');
 l.href='https://fonts.googleapis.com/css2?family=Khand:wght@500;600;700&family=Hind:wght@400;500;600&display=swap';document.head.appendChild(l)}
function findMorning(){var e=slot('morning')||q('#morning-report')||q('#morning')||q('[aria-label="Morning Report"]');if(e)return e;
 var ds=qa('details');for(var i=0;i<ds.length;i++){var s=ds[i].querySelector(':scope>summary');if(s&&MR.test(s.textContent)&&!ds[i].parentElement.closest('details'))return ds[i]}
 var hs=qa('h1,h2,h3,.rk,.rhd,.rh,.eyebrow,.mrt,b,span');
 for(var j=0;j<hs.length;j++){var h=hs[j];if(!MR.test(h.textContent)||h.closest('a,nav,.mw-cc-header,[data-routines],#routines,footer,.ds-sec,script,#mw-bh,#mw-bf'))continue;
  var c=h.closest('section,article,details,.card,.report');if(c&&c!==document.body&&c.tagName!=='MAIN')return c}return null}
function share(){var u=location.href.split('#')[0],t=document.title;if(navigator.share){navigator.share({title:t,url:u}).catch(function(){});return}
 try{navigator.clipboard.writeText(u)}catch(_){}qa('.mw-bh-share').forEach(function(b){b.classList.add('is-copied');b.setAttribute('aria-label','Link copied');setTimeout(function(){b.classList.remove('is-copied');b.setAttribute('aria-label','Share')},1600)})}
var SHAREIC='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M12 15V3"/><path d="M7 8l5-5 5 5"/><path d="M5 12v9h14v-9"/></svg>';function shareBtn(){var b=mk('button','mw-bh-share');b.type='button';b.setAttribute('aria-label','Share');b.title='Share';b.innerHTML=SHAREIC+'<span class="mw-bh-share-ok">Link copied</span>';b.addEventListener('click',share);return b}
/* ly9 report extras: square Late tag + up to three headline cards, from the board's report.json (no-store) */
function reportExtras(md,body){fetch('report.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j)return;
 if(j.late===true||(typeof j.late==='number'&&j.late>0)||j.minutes_late>0){var m=j.minutes_late||(typeof j.late==='number'?j.late:0);
  if(!m&&j.posted_at&&j.due&&/T/.test(j.due)){var d=(Date.parse(j.posted_at)-Date.parse(j.due))/60000;if(d>0)m=Math.round(d)}
  var tg=mk('span','mw-mr-late',m?'Late '+m+' min':'Late');tg.title=j.late_reason||j.late_note||'Posted after its due time';var sm=q('summary',md);if(sm&&!q('.mw-mr-late',sm))sm.insertBefore(tg,q('.mw-chev',sm))}
 var H=(j.headlines||j.top3||[]).slice(0,3);if(H.length&&!q('.mw-mr-cards',body)){var w=mk('div','mw-mr-cards');H.forEach(function(h){var c=mk('div','mw-mr-card');
  if(typeof h==='string'){var cut=h.split(/(?<=[.:;])\s|\s\(/)[0];c.append(mk('b','',cut.length>70?cut.slice(0,68).replace(/\s+\S*$/,'')+'\u2026':cut));if(h.length>cut.length+2)c.append(mk('span','',h))}
  else{c.append(mk('b','',h.title||h.head||''));if(h.text||h.body)c.append(mk('span','',h.text||h.body))}w.appendChild(c)});body.insertBefore(w,body.firstChild)}var mn=q('summary .mw-mr-n',md);if(mn&&H.length&&R106)mn.textContent='('+H.length+')'}).catch(function(){})}
/* ly9 sticky-for-a-bit (Max note: sticky for a little bit, then goes away): slim bar after the header leaves the screen, for about one screen of scrolling */
function stickBar(bh,title){var bar=mk('div','mw-stick');bar.setAttribute('aria-hidden','true');var a=mk('a','mw-stick-home');a.href=HOME;a.innerHTML='<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/></svg>';a.tabIndex=-1;
 var t=mk('button','mw-stick-t',title);t.type='button';t.tabIndex=-1;t.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});var sb=shareBtn();sb.tabIndex=-1;bar.append(a,t,sb);document.body.appendChild(bar);
 var tick=false;function upd(){tick=false;var r=bh.getBoundingClientRect(),y=window.scrollY||0,end=bh.offsetTop+bh.offsetHeight+Math.round(window.innerHeight*1.0),on=r.bottom<0&&y<end;bar.classList.toggle('is-on',on)}
 addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd()}
function zeroCounter(sh){var head=q('.ds-head',sh);if(!head)return;var st=q('.ds-stats',head);if(!st){st=mk('div','ds-stats');head.appendChild(st)}
 if(st.hidden||!st.children.length){st.textContent='';[['0','decks today'],['0','decks all-time']].forEach(function(p){var s=mk('span','ds-stat');s.append(mk('b','',p[0]),mk('span','',p[1]));st.appendChild(s)});st.hidden=false}}
function stdShelfHead(sh){var h=q('.ds-head h2',sh);if(h&&h.textContent!=='Ready To Swipe')h.textContent='Ready To Swipe'}
/* ly10 desktop polish: phone (<768px) keeps min(1100, width-32) exactly; tablet+ gets 24px gutters; wide screens a moderately wider column (not airy) */
function colW(){var cw=document.documentElement.clientWidth;if(cw<768)return Math.min(1100,cw-32);var cap=cw>=1680?1280:cw>=1440?1200:1100;var W=Math.min(cap,cw-48);document.documentElement.style.setProperty('--mw-colw',W+'px');return W}
function column(){var mid=document.getElementById('mw-mid');if(!mid)return;var W=colW();
 (function walk(el,d){[].slice.call(el.children).forEach(function(c){if(/^(SCRIPT|STYLE|LINK|TEMPLATE)$/.test(c.tagName))return;var cs=getComputedStyle(c);if(cs.position==='fixed'||cs.display==='none')return;
  var mw=parseFloat(cs.maxWidth),w=c.getBoundingClientRect().width,wrap=(c.tagName==='MAIN'||/(^|\s)(wrap|container|page|content|inner|shell|app)(\s|$)/i.test(c.className));
  if((!isNaN(mw)&&mw<W-1&&w<W-1&&(cs.marginLeft===cs.marginRight))||wrap){c.style.setProperty('max-width','none','important');c.style.setProperty('margin-left','0','important');c.style.setProperty('margin-right','0','important');
   if(wrap){c.style.setProperty('padding-left','0','important');c.style.setProperty('padding-right','0','important')}}
  var vw=document.documentElement.clientWidth,r2=c.getBoundingClientRect();if(r2.width<vw-2&&(parseFloat(cs.marginLeft)<0||parseFloat(cs.marginRight)<0)&&!/(auto|scroll)/.test(getComputedStyle(c.parentElement).overflowX)){c.style.setProperty('margin-left','0','important');c.style.setProperty('margin-right','0','important')}
  if(/^(DIV|MAIN|SECTION|ARTICLE|HEADER|NAV)$/.test(c.tagName)&&d<3)walk(c,d+1)})})(mid,0)}
function place(){['mw-bh','mw-mid','mw-bf'].forEach(function(id){var b=document.getElementById(id);if(!b)return;b.style.transform='none';var W=colW(),
 want=Math.max(16,(document.documentElement.clientWidth-W)/2);b.style.setProperty('width',W+'px','important');var r=b.getBoundingClientRect(),d=Math.round(want-r.left),ay=r.top+(window.scrollY||0),fy=Math.round(ay)-ay;b.style.transform=(d||fy)?'translate('+d+'px,'+fy.toFixed(3)+'px)':'none'})}
/* ly8 R85 (Max Oct 16 2026 23:39 ICT): "Working on" dropdown above Morning Report, only while this board's agent is working. Data: ONE shared file kit/agent-status.json (no-store + cache-bust). */
var ST=K+'agent-status.json';function norm(n){return String(n||'').toLowerCase().replace(/&/g,'and').replace(/\bagent\b/g,'').replace(/[^a-z0-9]+/g,' ').trim()}
function boardAgent(){var e=q('script[data-mw-agent]')||q('[data-mw-agent]');if(e)return e.getAttribute('data-mw-agent');var m=q('meta[name="mw-agent-name"]');if(m)return m.content;
 var c=q('script[src*="mw-chat.js"][data-agent-name]');if(c)return c.getAttribute('data-agent-name');var cc=q('.mw-cc-header[data-cc-name]');if(cc)return cc.dataset.ccName;
 var t=document.title.match(/^\s*(.+?)\s+(Agent\s+)?(Command Center|Board|Dashboard)\b/i);return t?t[1]:''}
function working(wd){var me=norm(boardAgent());if(!me){wd.hidden=true;return}
 function upd(){fetch(ST+'?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){var a=null;((j&&j.agents)||[]).forEach(function(x){if(norm(x.agent)===me)a=x});
  if(a&&a.working){q('.mw-wo-doing',wd).textContent=a.doing||'Working';wd.hidden=false}else{wd.hidden=true;wd.open=false}}).catch(function(){})}
 upd();setInterval(upd,60000);document.addEventListener('visibilitychange',function(){if(!document.hidden)upd()})}
function run(){if(document.body.dataset.mwLayout===V)return;var cc=q('.mw-cc-header');if(!cc)return;document.body.dataset.mwLayout=V;fonts();
 need('mw-layout.css',true);need('deck-shelf.css',true);need('routines-section.css',true);need('mw-back.js',false);/* ly12 R104 history-first back helper */
 var heroes=qa('[data-mw-slot="hero"]');
 var shelf=q('[data-shelf]')||q('[data-launcher]')||slot('shelf');
 var mor=findMorning(),rout=q('[data-routines]')||q('#routines');
 var bh=mk('div','mw-branded-header');bh.id='mw-bh';
 var home=mk('a','mw-apps-home mw-bh-home');home.href=HOME;home.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg><span>Apps Home</span>';
 var ncc=mk('div','mw-bh-cc'),lg=mk('div','mw-bh-logo'),src=q('.mw-cc-logo',cc);
 if(src){var pic=q('img',src);if(pic){var im=mk('img');im.src=pic.currentSrc||pic.src;im.alt=pic.alt||'';lg.appendChild(im)}else{var sv=q('svg',src);if(sv)lg.appendChild(sv.cloneNode(true))}}
 else if(cc.dataset.ccLogo){var im2=mk('img');im2.src=cc.dataset.ccLogo;im2.alt='';lg.appendChild(im2)}
 var tx=mk('div','mw-bh-text'),t0=q('.mw-cc-title',cc)||q('h1',cc),d0=q('.mw-cc-desc',cc)||q('p',cc);
 tx.append(mk('h1','mw-bh-title',t0?t0.textContent.trim():(cc.dataset.ccName||'')+' Command Center'),mk('p','mw-bh-desc',d0?d0.textContent.trim():(cc.dataset.ccDesc||'')));ncc.append(lg,tx,shareBtn());
 /* R106 header action slot (staged): <div data-mw-header-action> (e.g. Household's Add To Home Screen) moves to the top right of the
    Command Center header, next to Share: 44px square light icon button, label only at 700px+. Nothing renders when a board has none. */
 if(R106){var acts=qa('[data-mw-header-action]').filter(function(a){return !a.closest('#mw-bh,#mw-bf')});if(acts.length){var aw=mk('div','mw-bh-actions');acts.forEach(function(a){a.classList.add('mw-bh-action');aw.appendChild(a)});ncc.insertBefore(aw,ncc.lastChild)}}
 var decks=mk('div','mw-bh-decks');if(!shelf){shelf=mk('section');shelf.setAttribute('data-shelf','shelf.json');need('deck-shelf.js',false)}decks.appendChild(shelf);
 var md=mk('details','mw-bh-morning');md.id='mw-morning';var sm=mk('summary');sm.append(mk('span','mw-mr-t','Morning Report'),mk('span','mw-mr-n',''),mk('span','mw-chev'));md.appendChild(sm);var body=mk('div','mw-mr-body');md.appendChild(body);
 if(mor){if(mor.tagName==='DETAILS'){var os=q(':scope>summary',mor);if(os){var st=os.textContent.replace(/\s+/g,' ').replace(MR,'').replace(/^[\s·\-:]+/,'').trim();if(st)body.appendChild(mk('p','mw-mr-sub',st))}
   mor.classList.add('mw-mr-src');[].slice.call(mor.childNodes).forEach(function(n){if(n!==os)body.appendChild(n)});body.appendChild(mor);mor.style.setProperty('display','none','important')}
  else{body.appendChild(mor);mor.hidden=false}}else body.appendChild(mk('p','mw-mr-sub','No Morning Report yet.'));
 var wd=mk('details','mw-bh-working');wd.id='mw-working';wd.hidden=true;var ws=mk('summary');ws.append(mk('span','mw-mr-t','Working On'),mk('span','mw-chev'));wd.appendChild(ws);var wb=mk('div','mw-mr-body');wb.appendChild(mk('p','mw-mr-sub mw-wo-doing',''));wd.appendChild(wb);working(wd);
 /* ly12 R106 (Max Oct 17 2026 19:53 ICT): header = Command Center > decks + counter > (Working On) > Morning Report > To-Do List fold-down
    (closed, same look as Morning Report) > Document Center > divider. To-Do source: [data-mw-slot="todo"], else #todos (Grok Bot). */
 /* R106 is ON from ly13 (projects.js op5 fold-down cleared by Security, e58b17a). */
 var tsrc=R106?(slot('todo')||q('details#todos')||q('#todos')):null,td=null;
 if(tsrc&&!tsrc.closest('#mw-bh,#mw-bf')){td=mk('details','mw-bh-morning mw-bh-todo');td.id='mw-todo';
  /* Max 20:16 ICT: always-open To-Do blocks (ul, section, div, details) are wrapped into a closed fold-down; header row = title + count like Morning Report.
     Title: data-mw-todo-title, else Construction's 'Decisions Needed' (#decisions) keeps its own title, else 'To-Do List'. */
  var tt=tsrc.getAttribute('data-mw-todo-title')||(tsrc.id==='decisions'?'Decisions Needed':'To-Do List');
  var tsm=mk('summary'),tn=mk('span','mw-mr-n','');tsm.append(mk('span','mw-mr-t',tt),tn,mk('span','mw-chev'));td.appendChild(tsm);var tb=mk('div','mw-mr-body');td.appendChild(tb);
  if(tsrc.tagName==='DETAILS'){tsrc.open=true;tsrc.classList.add('mw-todo-src')}tsrc.classList.add('mw-todo');tsrc.hidden=false;
  var th0=q('h2,h3',tsrc);if(th0&&/^\s*(to-?do( list|'?s)?|waiting on max|needs? (you|max)|open items|decisions needed)\s*[\d·\s]*$/i.test(th0.textContent))th0.classList.add('mw-todo-h');tb.appendChild(tsrc);
  /* ly13 count: 1) data-mw-todo-count, 2) the number in the source's own summary/heading (e.g. Grok Bot "To-Do's (87)", Construction "Decisions Needed · 6"),
     3) visible top-level li, 4) .mlist children. Empty source: one plain-text line (textContent), removed again once items arrive. */
  var emp=null,cnt=function(){var L=0,ac=tsrc.getAttribute('data-mw-todo-count'),has=ac!=null&&/^\d+$/.test(ac.trim());if(has)L=+ac.trim();
   if(!has&&!L){var sm0=q(':scope>summary',tsrc)||th0;var mm=sm0&&sm0.textContent.match(/(\d+)/);if(mm)L=+mm[1]}
   if(!has&&!L)L=qa('li',tsrc).filter(function(li){return !li.parentElement.closest('li')&&getComputedStyle(li).display!=='none'}).length;
   if(!has&&!L){var ml=q('.mlist',tsrc)||(tsrc.classList.contains('mlist')?tsrc:null);if(ml)L=[].slice.call(ml.children).filter(function(c){return c.nodeType===1}).length}
   tn.textContent=L?'('+L+')':'';
   var blank=!L&&!tsrc.textContent.trim();if(blank&&!emp){emp=mk('p','mw-mr-sub mw-todo-empty','Nothing waiting on you right now.');tb.appendChild(emp)}else if(!blank&&emp&&tsrc.textContent.trim()){emp.remove();emp=null}};cnt();var tci=0;try{new MutationObserver(function(){clearTimeout(tci);tci=setTimeout(cnt,120)}).observe(tsrc,{childList:true,subtree:true})}catch(_){}}
 var dsrc=R106?(q('#mw-projects')||q('[data-mw-projects]')):null,dw=null;if(dsrc&&!dsrc.closest('#mw-bf')){dw=mk('div','mw-bh-docs');dw.appendChild(dsrc)}
 bh.append(home,ncc,decks,wd,md);if(td)bh.append(td);if(dw)bh.append(dw);bh.append(mk('hr','mw-bh-divider'));
 cc.style.setProperty('display','none','important');cc.setAttribute('aria-hidden','true');
 document.body.insertBefore(bh,document.body.firstChild);
 reportExtras(md,body);stickBar(bh,tx.firstChild.textContent);
 var after=bh;heroes.forEach(function(h){after.after(h);after=h});
 /* ly12: with R106 on, the To-Do List is a header fold-down; until then it stays the first middle section (ly9) */
 var todo=R106?null:slot('todo');if(todo){todo.classList.add('mw-todo');var th=q('h2,h3',todo);if(th&&/waiting on max|needs? (you|max)|to-?do/i.test(th.textContent))th.textContent='To-Do List';after.after(todo);after=todo}
 /* anything else the old header carried (greeting, updated time, buttons) moves to the middle */
 var ex=mk('div','mw-cc-extras');[].slice.call(cc.children).forEach(function(c){if(!c.matches('.mw-cc-logo,.mw-cc-text'))ex.appendChild(c)});
 var otx=q('.mw-cc-text',cc);if(otx)[].slice.call(otx.children).forEach(function(c){if(c!==t0&&c!==d0)ex.appendChild(c)});
 if(ex.children.length){after.after(ex);after=ex}
 var bf=mk('div','mw-branded-footer');bf.id='mw-bf';var rw=mk('div','mw-bf-routines');
 if(!rout){rout=mk('section');rout.setAttribute('data-routines','routines.json');need('routines-section.js',false)}rw.appendChild(rout);
 var sf=mk('div','mw-bf-standard'),ba=mk('a','mw-built');ba.innerHTML=MACHAN;ba.href='https://maxweberman.com';sf.append(ba);
 bf.append(mk('hr','mw-bf-divider'),rw,sf);
 var tail=qa('body>script,body>style,body>template');document.body.appendChild(bf);tail.forEach(function(s){document.body.appendChild(s)});
 /* ly7 (Max Oct 16 2026 21:36 ICT): no stray 'Board · Updated / Add To Home Screen / Share' row under the header. Updated + Add To Home Screen move next to the footer Share; Share is not duplicated. */
 var fx=mk('div','mw-bf-extras');qa('nav.topnav,.mw-cc-extras,.mw-topbar,[data-mw-slot="topbar"]').forEach(function(r){if(r.closest('#mw-bh,#mw-bf'))return;
  qa('button,a',r).forEach(function(b){var k=b.textContent+' '+(b.getAttribute('aria-label')||'')+' '+b.id+' '+b.className;if(/share/i.test(k))b.remove();else if(/a2hs|add to home/i.test(k))fx.appendChild(b)});
  qa('*',r).forEach(function(x){if(!x.children.length&&/^\s*(Last\s+)?Updated\b/i.test(x.textContent)&&!x.closest('.mw-bf-extras'))fx.insertBefore(x,fx.firstChild)});
  if(!qa('button,a,input,img,video,canvas',r).some(function(x){return !/a-o956qercs5ubd57y/.test(x.getAttribute('href')||'')})&&r.textContent.replace(/[\s\u00b7|]+/g,' ').trim().split(' ').length<=3)r.style.setProperty('display','none','important')});
 if(fx.children.length)sf.insertBefore(fx,ba);
 qa('footer,.mw-footer,[data-mw-slot="footer"],[data-mw-slot="footer-pre"]').forEach(function(f){if(f.closest('#mw-bh,#mw-bf'))return;
  qa('a[href*="maxweberman.com"],.mw-machan',f).forEach(function(a){a.remove()});
  qa('*',f).forEach(function(x){if(!x.children.length&&/^\s*Built by (Max Weberman|Machan)\s*$/.test(x.textContent))x.remove()});
  [].slice.call(f.childNodes).forEach(function(n){if(n.nodeType===3)n.textContent=n.textContent.replace(/Built by (Max Weberman|Machan)/,'')});
  qa('button,a',f).forEach(function(b){if(/share/i.test(b.textContent+' '+(b.getAttribute('aria-label')||'')+' '+b.id+' '+b.className))b.remove()});
  f.classList.remove('mw-footer','mw-branded-footer','mw-bf-standard');f.classList.add('mw-old-footer');
  if(!f.textContent.trim()&&!q('img,svg,video,canvas,input',f)&&!q('#toast,.toast',f))f.style.setProperty('display','none','important')});
 qa('a[href*="a-o956qercs5ubd57y"]').forEach(function(a){if(a===home||a.closest('[data-mw-keep-home]'))return;var t=a.textContent.replace(/[\u2190<\s]+/g,' ').trim();if(/^apps home$/i.test(t)||!t)a.remove()});
 qa('.mw-section,.mw-sections>section,.mw-sections>div,.rt-wrap,.routbot,.rt-bottom,header').forEach(function(s){if(s.closest('#mw-bh,#mw-bf'))return;if(!s.textContent.trim()&&!q('img,svg,video,iframe,canvas,button,input',s))s.style.setProperty('display','none','important')});
 /* no doubled dividers: the middle's first/last blocks lose their own top/bottom rules */
 function edge(start,dir){var e=start,n=0;while(e&&n<4){var nx=dir>0?e.nextElementSibling:e.previousElementSibling;while(nx&&(/^(SCRIPT|STYLE|TEMPLATE|LINK)$/.test(nx.tagName)||getComputedStyle(nx).display==='none'||getComputedStyle(nx).position==='fixed'))nx=dir>0?nx.nextElementSibling:nx.previousElementSibling;
  if(!nx)return;var x=nx;for(var d=0;d<4&&x;d++){if(x.tagName==='HR'){x.style.setProperty('display','none','important');break}var cs=getComputedStyle(x);
   if(dir>0&&parseFloat(cs.borderTopWidth)>0)x.style.setProperty('border-top','0','important');if(dir<0&&parseFloat(cs.borderBottomWidth)>0)x.style.setProperty('border-bottom','0','important');
   var ch=[].slice.call(x.children).filter(function(c){var k=getComputedStyle(c);return k.display!=='none'&&k.position!=='fixed'&&!/^(SCRIPT|STYLE)$/.test(c.tagName)});x=dir>0?ch[0]:ch[ch.length-1]}return}}
 edge(after,1);edge(bf,-1);setTimeout(function(){edge(after,1);edge(bf,-1)},2000);
 /* middle content shares the 1100px column with the branded header/footer (Max 14:19) */
 var mid=mk('div','mw-middle');mid.id='mw-mid';bh.after(mid);var nx=mid.nextSibling;
 while(nx&&nx!==bf){var n2=nx.nextSibling;if(nx.nodeType===1){var k=getComputedStyle(nx);if(!/^(SCRIPT|STYLE|LINK|TEMPLATE|NOSCRIPT)$/.test(nx.tagName)&&k.position!=='fixed'&&!nx.matches('.mw-chat-btn,#toast,.toast,[role=dialog]'))mid.appendChild(nx)}else if(nx.nodeType===3&&nx.textContent.trim())mid.appendChild(nx);nx=n2}
 column();setTimeout(column,1500);setTimeout(column,4000);
 var tries=0,iv=setInterval(function(){stdShelfHead(decks);tries++;if((q('.ds-head',decks)&&tries>6)||tries>30){zeroCounter(decks);clearInterval(iv)}},500);
 var sh2=0,ivh=setInterval(function(){stdShelfHead(decks);if(++sh2>20)clearInterval(ivh)},1000);
 place();addEventListener('resize',function(){place();column()});var pn=0,pv=setInterval(function(){place();if(++pn>30)clearInterval(pv)},500);try{new ResizeObserver(function(){place()}).observe(document.getElementById('mw-mid')||document.body)}catch(_){}addEventListener('load',place);setTimeout(place,1500);setTimeout(place,4000);
 document.dispatchEvent(new CustomEvent('mw-layout'));
 /* ly13 R106: kit/projects.js (op5, not edited here) re-mounts #mw-projects as the first child of #mw-mid on start and on every 'mw-layout'
    event. Move that same node back into the header slot (.mw-bh-docs, above the divider). Node move only; projects.js is never re-run. */
 if(R106){var homeDocs=function(){var p=q('#mw-projects')||q('[data-mw-projects]');if(!p||p.closest('#mw-bf'))return;
   if(!dw){dw=mk('div','mw-bh-docs');bh.insertBefore(dw,q(':scope>.mw-bh-divider',bh))}if(p.parentNode!==dw)dw.appendChild(p)};
  /* ly13: the Document Center used to be #mw-mid's first child; now a board block is, and a negative margin-top on it (Construction .wrap)
     would collapse through #mw-mid and slide it under the divider. Zero only NEGATIVE top margins down the first-visible-child chain. */
  var midTop=function(){var e=mid;for(var dd=0;dd<5&&e;dd++){var f=[].slice.call(e.children).filter(function(c){var k=getComputedStyle(c);return k.display!=='none'&&k.position!=='fixed'&&k.position!=='absolute'&&!/^(SCRIPT|STYLE|LINK|TEMPLATE)$/.test(c.tagName)})[0];
   if(!f)return;if(parseFloat(getComputedStyle(f).marginTop)<0)f.style.setProperty('margin-top','0','important');var ek=getComputedStyle(f);if(parseFloat(ek.paddingTop)>0||parseFloat(ek.borderTopWidth)>0)return;e=f}};
  var homeAll=function(){homeDocs();midTop()};
  homeAll();[0,300,1000,2500].forEach(function(t){setTimeout(homeAll,t)});
  try{var dmo=new MutationObserver(homeAll);dmo.observe(mid,{childList:true});dmo.observe(document.body,{childList:true});setTimeout(function(){dmo.disconnect()},15000)}catch(_){}}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.MWLayout={run:run,version:V,machan:MACHAN};})();
