/* kit/mw-back.js mb1: history-first Back / Return (rulebook R104, Max Oct 17 2026 19:39 ICT; Branding).
   ANY back/return button on a board, app page or deck page takes Max back to exactly where he came from:
     1) browser history: history.back() when there is history (history.length > 1) AND document.referrer is a trusted board page
        (https://webermanapps.github.io/...) other than this page;
     2) else the trusted origin saved for this page: ?from=<board url> (kept in sessionStorage so it survives the password gate,
        reloads and in-page navigation), else a trusted document.referrer;
     3) else the fixed fallback link (default: the Branding board). Never an untrusted URL (no open redirect).
   NOT for the R82 card Back button on deck pages (previous card) and not for the R77 Apps Home house button (a HOME link).
   API (window.mwBack):
     mwBack(fallbackUrl[, {match:url}])      navigate back now. match: only use history/origin when it IS that page, else go to fallback.
     mwBack.target(fallbackUrl)              the URL Return would go to (no history), for href / open-in-new-tab.
     mwBack.origin()                         {url,name} of the trusted origin board, or null.   mwBack.name() -> board name or ''.
     mwBack.withFrom(deckUrl[, fromUrl, name]) deckUrl + from=<this board> (+ from_name) for links that open decks.
     mwBack.trusted(url)                     URL object if trusted, else null.
   Markup (auto-wired, also when added later): <a href="FALLBACK" data-mw-back>Back</a>   (data-mw-back="URL" overrides the fallback)
     data-mw-return         label it "Return to <board name>" (inner .mw-ret-name gets the name; falls back to data-mw-return-default)
     data-mw-back-match     match mode (only go back if the previous page is the link's own target).
   Load: <script src="https://webermanapps.github.io/style-swipe/kit/mw-back.js?v=mb1"></script>  (kit mw-layout.js ly12 loads it on every board). */
(function(w,d){if(w.mwBack&&w.mwBack.VERSION)return;
var V='mb1',HOSTS=['webermanapps.github.io'],FB='https://webermanapps.github.io/branding-djqmb410/',SK='mwBack:'+location.pathname;
var B='https://webermanapps.github.io/';
var NAMES=[['branding-djqmb410/decks/','Deck Building'],['branding-djqmb410/','Branding'],['a-o956qercs5ubd57y/','Apps Home'],['upkeep-cc-d36d3521/','UpKeep'],
 ['wellnest-dashboard/','WellNest'],['grokbot-cc-7b9szx1e/','Grok Bot'],['blog-dashboard/','Blog'],['blueprint-dashboard/','Blueprint'],['coach-dashboard/','Coach'],
 ['cd-4thwrkpz54/','Construction'],['dump-dashboard/','Dump'],['jc-cc-e034959dac7d/','Japan Cottage'],['jokes-cc-5a640f18188c/','Jokes'],['legal-0a84f667080d/','Legal'],
 ['portfolio-dashboard/','Portfolio'],['prop-dashboard/','Prop'],['rd-3k3k8jcaqb/','Research'],['scout-dashboard/','Scout'],['security-07940c684c/','Security'],
 ['thai-vocab-quiz/dashboard/','Thai'],['thai-vocab-quiz/','Thai Quiz'],['video-photo-dashboard-70m4sfrw/','Video & Photo'],['miles-dashboard/','Miles'],
 ['household-dashboard/','Household'],['style-swipe/','Style Swipe']];
function trusted(u){if(!u)return null;try{var x=new URL(u,location.href);if(x.protocol!=='https:'||HOSTS.indexOf(x.hostname)<0||x.username||x.password)return null;return x}catch(e){return null}}
function page(x){return x.origin+x.pathname.replace(/index\.html$/,'')}
function self(){return page(new URL(location.href))}
function notSelf(x){return x&&page(x)!==self()?x:null}
function clean(n){return String(n||'').replace(/[^\w &'\u00b7.-]/g,'').replace(/\s+/g,' ').trim().slice(0,40)}
function nameFor(u){var x=trusted(u);if(!x)return '';var p=x.href.slice(B.length).split(/[?#]/)[0],best='',bl=-1;
 NAMES.forEach(function(n){if(p.indexOf(n[0])===0&&n[0].length>bl){best=n[1];bl=n[0].length}});return best}
var SS={get:function(){try{return JSON.parse(sessionStorage.getItem(SK)||'null')}catch(e){return null}},set:function(v){try{sessionStorage.setItem(SK,JSON.stringify(v))}catch(e){}}};
function origin(){var q=new URLSearchParams(location.search),f=notSelf(trusted(q.get('from')));
 if(f){var o={url:f.href,name:clean(q.get('from_name'))||nameFor(f.href)};SS.set(o);return o}
 var s=SS.get();if(s&&notSelf(trusted(s.url)))return {url:trusted(s.url).href,name:clean(s.name)||nameFor(s.url)};
 var r=notSelf(trusted(d.referrer));if(r){var o2={url:r.href,name:nameFor(r.href)};SS.set(o2);return o2}return null}
function samePage(a,b){var x=trusted(a),y=trusted(b);return !!(x&&y&&page(x)===page(y))}
function target(fb,o){o=o||{};var g=origin(),f=trusted(fb)||trusted(FB);if(o.match)return g&&samePage(g.url,o.match)?g.url:(trusted(o.match)||f).href;return g?g.url:f.href}
function go(fb,o){o=o||{};var r=notSelf(trusted(d.referrer)),t=target(fb,o);
 if(w.history.length>1&&r&&(!o.match||samePage(r.href,o.match))){var left=false;w.addEventListener('pagehide',function(){left=true},{once:true});
  try{w.history.back()}catch(e){}setTimeout(function(){if(!left&&!d.hidden)location.assign(t)},800);return}
 location.assign(t)}
function withFrom(u,from,name){try{var x=new URL(u,location.href);if(!trusted(x.href))return u;var f=trusted(from||location.href);if(!f)return u;
 x.searchParams.set('from',page(f));var n=clean(name||'');if(n)x.searchParams.set('from_name',n);return x.href}catch(e){return u}}
function fbOf(a){return a.getAttribute('data-mw-back')||a.getAttribute('href')||FB}
function label(a){if(!a.hasAttribute('data-mw-return'))return;var g=origin(),n=(g&&g.name)||a.getAttribute('data-mw-return-default')||nameFor(fbOf(a))||'Board';
 var s=a.querySelector('.mw-ret-name');if(s){if(s.textContent!==n)s.textContent=n}a.setAttribute('aria-label','Return to '+n);a.title='Return to '+n}
function wire(a){if(!a||a.__mwb)return;a.__mwb=1;if(!a.hasAttribute('data-mw-back-match')){var t=target(fbOf(a));if(a.tagName==='A'&&a.getAttribute('href')!==t&&!a.hasAttribute('data-mw-keep-href'))a.setAttribute('href',t)}label(a)}
function scan(){var L=d.querySelectorAll('[data-mw-back]');for(var i=0;i<L.length;i++){wire(L[i]);label(L[i])}}
d.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('[data-mw-back]');if(!a||e.defaultPrevented)return;
 if(e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();var fb=a.getAttribute('data-mw-back')||a.getAttribute('data-mw-fallback')||FB;
 if(a.hasAttribute('data-mw-back-match'))go(fb,{match:a.getAttribute('data-mw-back-match')||fb});else go(fb)},false);
var api=function(fb,o){go(fb,o)};api.VERSION=V;api.go=go;api.target=target;api.origin=origin;api.name=function(){var g=origin();return g?g.name:''};
api.withFrom=withFrom;api.trusted=trusted;api.nameFor=nameFor;api.scan=scan;w.mwBack=api;
origin();
function boot(){scan();var t=0;try{new MutationObserver(function(){if(t)return;t=setTimeout(function(){t=0;scan()},80)}).observe(d.documentElement,{childList:true,subtree:true})}catch(e){}}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',boot);else boot();
})(window,document);
