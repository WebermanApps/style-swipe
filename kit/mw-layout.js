/* Uniform board layout (Max, Oct 16 2026 12:09 ICT, rulebook R76; kit ly1). Applies to EVERY agent board + Apps Home, no exceptions.
   BRANDED HEADER (.mw-branded-header parts): 1) Command Center header (.mw-cc-header)  2) deck shelf + deck counter ([data-shelf] / .ds-sec)  3) Morning Report, collapsible, CLOSED by default.
   MIDDLE: everything else (optional [data-mw-slot="hero"] goes first, e.g. WellNest hero video).
   BRANDED FOOTER (.mw-branded-footer parts): 1) Routines ([data-routines] / #routines)  2) standard footer: Share + "Built by Max Weberman" -> https://maxweberman.com.
   Explicit markers win over detection: data-mw-slot="header|shelf|counter|morning|hero|routines|footer-pre|footer". Opt out of the Morning Report wrap: data-mw-keep. Several hero slots keep DOM order. footer-pre = extra standard-footer parts (e.g. a share bar) placed after Routines, before the footer.
   Usage: <link rel="stylesheet" href=".../kit/mw-layout.css?v=ly1"><script src=".../kit/mw-layout.js?v=ly1" defer></script> */
(function(){
var q=function(s,r){return (r||document).querySelector(s)};
var slot=function(n){return q('[data-mw-slot="'+n+'"]')};
var MR=/^\s*morning report/i;
function findMorning(){var e=slot('morning')||q('details.mw-morning')||q('#morning')||q('[aria-label="Morning Report"]');if(e)return e;
 var ds=document.querySelectorAll('details');for(var i=0;i<ds.length;i++){var s=ds[i].querySelector(':scope>summary');if(s&&MR.test(s.textContent)&&!ds[i].closest('details details, .mw-cc-header, nav'))return ds[i];}
 var hs=document.querySelectorAll('h1,h2,h3,.rk,.rhd,.rh,.eyebrow,.mrt,b,span');
 for(var j=0;j<hs.length;j++){var h=hs[j];if(!MR.test(h.textContent)||h.closest('a,nav,.mw-cc-header,[data-routines],#routines,footer,.ds-sec,script'))continue;
  var c=h.closest('section,article,details,.card,.report');if(c&&c!==document.body&&c.tagName!=='MAIN')return c;}
 return null}
function lca(a,b){if(!a)return b&&b.parentElement;if(!b)return a.parentElement;var p=a.parentElement;while(p&&!p.contains(b))p=p.parentElement;return p||document.body}
function lastEl(p){var c=p.lastElementChild;while(c&&/^(SCRIPT|STYLE|TEMPLATE)$/.test(c.tagName))c=c.previousElementSibling;return c}
function firstEl(p){var c=p.firstElementChild;while(c&&/^(SCRIPT|STYLE|TEMPLATE)$/.test(c.tagName))c=c.nextElementSibling;return c}
function climbAfter(e,col){while(e.parentElement&&e.parentElement!==col&&e.parentElement!==document.body&&(lastEl(e.parentElement)===e||e.parentElement.tagName==='HEADER'))e=e.parentElement;return e}
function climbBefore(e,col){while(e.parentElement&&e.parentElement!==col&&firstEl(e.parentElement)===e&&e.parentElement!==document.body)e=e.parentElement;return e}
function wrapMorning(m){if(m.hasAttribute('data-mw-keep'))return m;
 if(m.tagName==='DETAILS'){m.classList.add('mw-morning-own');m.open=false;m.removeAttribute('open');m.classList.add('mw-morning');return m}
 var d=document.createElement('details');d.className='mw-morning';var s=document.createElement('summary');s.textContent='Morning Report';d.appendChild(s);
 m.parentNode.insertBefore(d,m);d.appendChild(m);return d}
function share(){var u=location.href.split('#')[0],t=document.title;if(navigator.share){navigator.share({title:t,url:u}).catch(function(){});return}
 try{navigator.clipboard.writeText(u)}catch(_){}var b=q('.mw-std-share');if(b){b.textContent='Link copied';setTimeout(function(){b.textContent='Share'},1600)}}
function stdFooter(f,col){var made=false;if(!f){f=document.createElement('footer');f.className='mw-footer';(col||document.body).appendChild(f);made=true}
 f.classList.add('mw-footer');f.setAttribute('data-mw-slot','footer');
 var bar=q('.mw-footer-bar',f);if(!bar){bar=document.createElement('div');bar.className='mw-footer-bar';var fw=f.querySelector(':scope>.wrap');(fw||f).appendChild(bar)}
 if(!q('a[href*="maxweberman.com"]',f)){var lf=[].slice.call(f.querySelectorAll('*')).filter(function(x){return !x.children.length&&x.textContent.trim()==='Built by Max Weberman'})[0];
  if(lf){var la=document.createElement('a');la.href='https://maxweberman.com';la.textContent='Built by Max Weberman';la.style.color='inherit';lf.textContent='';lf.appendChild(la)}}
 if(!q('a[href*="maxweberman.com"]',f)){var a=document.createElement('a');a.href='https://maxweberman.com';a.textContent='Built by Max Weberman';
  var old=[].slice.call(f.childNodes).filter(function(n){return n.nodeType===3&&/Built by Max Weberman/.test(n.textContent)});old.forEach(function(n){n.textContent=n.textContent.replace('Built by Max Weberman','')});bar.appendChild(a)}
 var hasShare=[].slice.call(f.querySelectorAll('button,a')).concat([].slice.call(document.querySelectorAll('[data-mw-slot="footer-pre"] button'))).some(function(x){return /share/i.test(x.textContent+' '+(x.getAttribute('aria-label')||'')+' '+x.className)});
 if(!hasShare){var b=document.createElement('button');b.type='button';b.className='mw-btn mw-std-share';b.textContent='Share';b.addEventListener('click',share);bar.insertBefore(b,bar.firstChild)}
 return f}
function run(){if(document.body.dataset.mwLayout)return;var hdr=slot('header')||q('.mw-cc-header');if(!hdr)return;document.body.dataset.mwLayout='ly1';
 var shelf=slot('shelf')||q('[data-shelf]')||q('[data-launcher]')||q('.ds-sec'),rout=slot('routines')||q('[data-routines]')||q('#routines'),
  foot=slot('footer')||q('.mw-footer')||(function(){var fs=document.querySelectorAll('footer');return fs.length?fs[fs.length-1]:null})(),
  mor=findMorning(),heroes=[].slice.call(document.querySelectorAll('[data-mw-slot="hero"]'));
 if(foot&&foot.contains(hdr))foot=null;
 var col=lca(hdr,foot||rout);if(col&&col.contains&&!col.contains(hdr))col=hdr.parentElement;
 var at=climbAfter(hdr,col);
 hdr.classList.add('mw-branded-header','mw-bh-cc');var mw=mor&&wrapMorning(mor);if(shelf)shelf.classList.add('mw-branded-header','mw-bh-decks');if(mw)mw.classList.add('mw-branded-header','mw-bh-morning');
 [shelf,slot('counter'),mw].concat(heroes).forEach(function(e){if(!e||e.contains(hdr))return;at.after(e);at=e});
 foot=stdFooter(foot,col);
 var b=climbBefore(foot,col);if(rout&&!foot.contains(rout)){var blk=rout;while(blk.parentElement&&blk.parentElement!==col&&blk.parentElement!==document.body)blk=blk.parentElement;
  if(blk!==rout&&(blk.compareDocumentPosition(b)&4)){rout.parentElement.appendChild(rout);}else b.before(rout)}else if(rout&&foot.contains(rout)&&rout.parentElement===foot)foot.insertBefore(rout,foot.firstChild);
 document.querySelectorAll('[data-mw-slot="footer-pre"]').forEach(function(e){b.before(e)});
 if(rout)rout.classList.add('mw-routines-slot','mw-branded-footer','mw-bf-routines');foot.classList.add('mw-branded-footer','mw-bf-standard');
 document.dispatchEvent(new CustomEvent('mw-layout'))}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.MWLayout={run:run};})();
