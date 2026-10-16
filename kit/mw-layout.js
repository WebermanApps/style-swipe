/* Board layout kit ly4 (STRICT, Max Oct 16 2026 13:21 + 13:22 ICT, rulebook R79; earlier R76 12:09, Apps Home button R77 12:39).
   BRANDED HEADER and BRANDED FOOTER are built here as body-level blocks, pixel-identical on every agent board, colors included
   (Max's white + light beige). Board CSS cannot restyle them: scoped ids #mw-bh / #mw-bf + !important locks in mw-layout.css.
   BRANDED HEADER (#mw-bh.mw-branded-header): Apps Home button (.mw-bh-home) > Command Center header (.mw-bh-cc: logo, '<Name> Command Center', description)
     > decks shelf + deck counter (.mw-bh-decks; counter shows 0 when no stats) > Morning Report dropdown (.mw-bh-morning, closed by default)
     > divider (.mw-bh-divider: 1px #e3ddd2, full content width, equal spacing).
   MIDDLE: everything else, incl. ALL agent-specific branding (brand colors, special sections, photos, video). [data-mw-slot="hero"] items go first.
   BRANDED FOOTER (#mw-bf.mw-branded-footer): divider (.mw-bf-divider, same as header's) > Routines (.mw-bf-routines) > standard footer (.mw-bf-standard: Share + mark + 'Built by Machan' -> maxweberman.com; ly5 Oct 16 2026, Branding Agent).
   Per-board differences allowed in the header: logo, name, description (plus deck / report / routine content).
   Markers (optional): data-mw-slot="shelf|morning|hero|routines". Old footers are folded into the middle; old Apps Home links removed.
   Agent boards only (Apps Home, deck pages and the share page never load this file).
   Usage: <link rel="stylesheet" href=".../kit/mw-layout.css?v=ly6"><script src=".../kit/mw-layout.js?v=ly6" defer></script> */
(function(){
var V='ly6',MACHAN="<span class=\"mw-machan\" style=\"display:inline-flex;align-items:center;gap:6px;vertical-align:middle;white-space:nowrap\"><svg class=\"mw-machan-mark\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" aria-hidden=\"true\" focusable=\"false\" style=\"display:block;flex:none;width:22px;height:22px\"><path d=\"M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z\" fill=\"#3F7D58\"/><path d=\"M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z\" fill=\"#5E9A6E\"/><rect x=\"3.5\" y=\"5.5\" width=\"17\" height=\"16\" rx=\"7\" fill=\"#C8643F\"/><rect x=\"5.5\" y=\"9\" width=\"13\" height=\"10\" rx=\"5\" fill=\"#FAF6EE\"/><circle cx=\"9.6\" cy=\"13.3\" r=\"1.35\" fill=\"#2E6F86\"/><circle cx=\"14.4\" cy=\"13.3\" r=\"1.35\" fill=\"#2E6F86\"/><path d=\"M10.6 16.1q1.4 1.1 2.8 0\" fill=\"none\" stroke=\"#C8643F\" stroke-width=\"1.1\" stroke-linecap=\"round\"/><circle cx=\"7.6\" cy=\"15.6\" r=\".9\" fill=\"#E9B9A3\"/><circle cx=\"16.4\" cy=\"15.6\" r=\".9\" fill=\"#E9B9A3\"/></svg>Built by Machan</span>",K='https://webermanapps.github.io/style-swipe/kit/',HOME='https://webermanapps.github.io/a-o956qercs5ubd57y/';
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
 try{navigator.clipboard.writeText(u)}catch(_){}var b=q('#mw-bf .mw-std-share');if(b){b.textContent='Link copied';setTimeout(function(){b.textContent='Share'},1600)}}
function zeroCounter(sh){var head=q('.ds-head',sh);if(!head)return;var st=q('.ds-stats',head);if(!st){st=mk('div','ds-stats');head.appendChild(st)}
 if(st.hidden||!st.children.length){st.textContent='';[['0','decks today'],['0','decks all-time']].forEach(function(p){var s=mk('span','ds-stat');s.append(mk('b','',p[0]),mk('span','',p[1]));st.appendChild(s)});st.hidden=false}}
function stdShelfHead(sh){var h=q('.ds-head h2',sh);if(h&&h.textContent!=='Ready To Swipe')h.textContent='Ready To Swipe'}
function column(){var mid=document.getElementById('mw-mid');if(!mid)return;var W=Math.min(1100,document.documentElement.clientWidth-32);
 (function walk(el,d){[].slice.call(el.children).forEach(function(c){if(/^(SCRIPT|STYLE|LINK|TEMPLATE)$/.test(c.tagName))return;var cs=getComputedStyle(c);if(cs.position==='fixed'||cs.display==='none')return;
  var mw=parseFloat(cs.maxWidth),w=c.getBoundingClientRect().width,wrap=(c.tagName==='MAIN'||/(^|\s)(wrap|container|page|content|inner|shell|app)(\s|$)/i.test(c.className));
  if((!isNaN(mw)&&mw<W-1&&w<W-1&&(cs.marginLeft===cs.marginRight))||wrap){c.style.setProperty('max-width','none','important');c.style.setProperty('margin-left','0','important');c.style.setProperty('margin-right','0','important');
   if(wrap){c.style.setProperty('padding-left','0','important');c.style.setProperty('padding-right','0','important')}}
  var vw=document.documentElement.clientWidth,r2=c.getBoundingClientRect();if(r2.width<vw-2&&(parseFloat(cs.marginLeft)<0||parseFloat(cs.marginRight)<0)&&!/(auto|scroll)/.test(getComputedStyle(c.parentElement).overflowX)){c.style.setProperty('margin-left','0','important');c.style.setProperty('margin-right','0','important')}
  if(/^(DIV|MAIN|SECTION|ARTICLE|HEADER|NAV)$/.test(c.tagName)&&d<3)walk(c,d+1)})})(mid,0)}
function place(){['mw-bh','mw-mid','mw-bf'].forEach(function(id){var b=document.getElementById(id);if(!b)return;b.style.transform='none';var W=Math.min(1100,document.documentElement.clientWidth-32),
 want=Math.max(16,(document.documentElement.clientWidth-W)/2);b.style.setProperty('width',W+'px','important');var r=b.getBoundingClientRect(),d=Math.round(want-r.left),ay=r.top+(window.scrollY||0),fy=Math.round(ay)-ay;b.style.transform=(d||fy)?'translate('+d+'px,'+fy.toFixed(3)+'px)':'none'})}
function run(){if(document.body.dataset.mwLayout===V)return;var cc=q('.mw-cc-header');if(!cc)return;document.body.dataset.mwLayout=V;fonts();
 need('mw-layout.css',true);need('deck-shelf.css',true);need('routines-section.css',true);
 var heroes=qa('[data-mw-slot="hero"]');
 var shelf=q('[data-shelf]')||q('[data-launcher]')||slot('shelf');
 var mor=findMorning(),rout=q('[data-routines]')||q('#routines');
 var bh=mk('div','mw-branded-header');bh.id='mw-bh';
 var home=mk('a','mw-apps-home mw-bh-home');home.href=HOME;home.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg><span>Apps Home</span>';
 var ncc=mk('div','mw-bh-cc'),lg=mk('div','mw-bh-logo'),src=q('.mw-cc-logo',cc);
 if(src){var pic=q('img',src);if(pic){var im=mk('img');im.src=pic.currentSrc||pic.src;im.alt=pic.alt||'';lg.appendChild(im)}else{var sv=q('svg',src);if(sv)lg.appendChild(sv.cloneNode(true))}}
 else if(cc.dataset.ccLogo){var im2=mk('img');im2.src=cc.dataset.ccLogo;im2.alt='';lg.appendChild(im2)}
 var tx=mk('div','mw-bh-text'),t0=q('.mw-cc-title',cc)||q('h1',cc),d0=q('.mw-cc-desc',cc)||q('p',cc);
 tx.append(mk('h1','mw-bh-title',t0?t0.textContent.trim():(cc.dataset.ccName||'')+' Command Center'),mk('p','mw-bh-desc',d0?d0.textContent.trim():(cc.dataset.ccDesc||'')));ncc.append(lg,tx);
 var decks=mk('div','mw-bh-decks');if(!shelf){shelf=mk('section');shelf.setAttribute('data-shelf','shelf.json');need('deck-shelf.js',false)}decks.appendChild(shelf);
 var md=mk('details','mw-bh-morning');md.id='mw-morning';var sm=mk('summary');sm.append(mk('span','mw-mr-t','Morning Report'),mk('span','mw-chev'));md.appendChild(sm);var body=mk('div','mw-mr-body');md.appendChild(body);
 if(mor){if(mor.tagName==='DETAILS'){var os=q(':scope>summary',mor);if(os){var st=os.textContent.replace(/\s+/g,' ').replace(MR,'').replace(/^[\s·\-:]+/,'').trim();if(st)body.appendChild(mk('p','mw-mr-sub',st))}
   mor.classList.add('mw-mr-src');[].slice.call(mor.childNodes).forEach(function(n){if(n!==os)body.appendChild(n)});body.appendChild(mor);mor.style.setProperty('display','none','important')}
  else{body.appendChild(mor);mor.hidden=false}}else body.appendChild(mk('p','mw-mr-sub','No Morning Report yet.'));
 bh.append(home,ncc,decks,md,mk('hr','mw-bh-divider'));
 cc.style.setProperty('display','none','important');cc.setAttribute('aria-hidden','true');
 document.body.insertBefore(bh,document.body.firstChild);
 var after=bh;heroes.forEach(function(h){after.after(h);after=h});
 /* anything else the old header carried (greeting, updated time, buttons) moves to the middle */
 var ex=mk('div','mw-cc-extras');[].slice.call(cc.children).forEach(function(c){if(!c.matches('.mw-cc-logo,.mw-cc-text'))ex.appendChild(c)});
 var otx=q('.mw-cc-text',cc);if(otx)[].slice.call(otx.children).forEach(function(c){if(c!==t0&&c!==d0)ex.appendChild(c)});
 if(ex.children.length){after.after(ex);after=ex}
 var bf=mk('div','mw-branded-footer');bf.id='mw-bf';var rw=mk('div','mw-bf-routines');
 if(!rout){rout=mk('section');rout.setAttribute('data-routines','routines.json');need('routines-section.js',false)}rw.appendChild(rout);
 var sf=mk('div','mw-bf-standard'),sb=mk('button','mw-std-share','Share');sb.type='button';sb.addEventListener('click',share);var ba=mk('a','mw-built');ba.innerHTML=MACHAN;ba.href='https://maxweberman.com';sf.append(sb,ba);
 bf.append(mk('hr','mw-bf-divider'),rw,sf);
 var tail=qa('body>script,body>style,body>template');document.body.appendChild(bf);tail.forEach(function(s){document.body.appendChild(s)});
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
 document.dispatchEvent(new CustomEvent('mw-layout'))}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.MWLayout={run:run,version:V,machan:MACHAN};})();
