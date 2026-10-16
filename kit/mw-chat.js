/* mw-chat cc11 (R74; cc11: also lifts above fixed tab bars/tap targets; cc10: lifts above fixed footers/bars in app layouts; cc9: cc9: hides while a row arrow (.arr / [data-mw-chat-hide]) is under it; more agents in registry). Usage:
   <script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc11" data-agent-id="<uuid>" data-agent-name="Coach Agent" defer></script>
   or <meta name="mw-agent-id" content="<uuid>"> (+ optional <meta name="mw-agent-name">), or data-agent="<slug>" from the registry below,
   or call MWChat.mount({agent:'<slug>'}) / MWChat.mount({id,name}) later (deck pages). Opens grokbot://app/v1/agent?id=<id>. */
(function(){
var REG={'grok-bot':['24ff6404-25b2-46a1-8487-b99d3c7c7b06','Grok Bot'],'household':['c59ffdde-28bf-4ad7-8dd8-22f5e941647d','Household'],'email-sorting':['d31d8de8-a97a-4bc3-823f-e4946a383e87','Email Sorting'],'branding':['3fac5054-3a3d-49b1-af61-59883f7fdc78','Branding Agent'],'blueprint':['5b23bb2f-ffc9-4b61-b04c-43a3943eac12','Blueprint Agent'],'construction':['f159ad69-43eb-47d6-87f5-2b637892edd2','Construction Agent'],'miles':['c4b349b2-05c3-4b7a-8dce-effcd2fbf58a','Miles Agent'],'thai':['7b552e05-d400-4d4b-897d-1b30381b6dda','Thai Agent'],'wellnest':['e2806a26-3867-4986-a7ef-46c03abc7f35','WellNest Agent'],'scout':['b0693910-5aaa-446b-b2ed-62026a073082','Scout Agent'],'japan-cottage':['a9f4c34c-b9eb-4c38-8554-3e1091ceb7b5','Japan Cottage Agent'],'upkeep':['f0d420ad-d37e-44d3-be6f-053da2b6e24d','UpKeep Agent'],'blog':['57b6fc9e-e2fc-45ba-b28e-73f066c4b0fa','Blog Agent'],'coach':['758a3343-fff3-4093-9169-81f79ffdc3ef','Coach Agent'],'jokes':['0f68b81e-50fc-455c-b558-a13f7cd796aa','Jokes Agent'],'legal':['55ae1827-d0b6-4a4a-98f1-551dc6f0ef3a','Legal Agent'],'portfolio':['cbf1a856-abbb-410a-99a0-cb65d213fc21','Portfolio Agent'],'prop':['f466837e-6ecd-4c83-9ac9-5f031aa92add','Prop Agent'],'research':['6efe5de2-9a20-43d9-a1eb-068e645ed407','Research Agent'],'security':['d47b42b5-3764-4c66-9360-3d4c931d0483','Security Agent'],'video-photo':['eca52f98-7367-4a43-9b92-47366636826e','Video & Photo Agent']};
var me=document.currentScript,base=(me&&me.src||'').replace(/mw-chat\.js(\?.*)?$/,''),ver=((me&&me.src||'').match(/\?v=([^&]+)/)||[])[1]||'cc11';
var AVOID='#share,.shic,.mw-share,footer,.mw-footer,#routines,.mw-sec-routines,[data-routines],[data-mw-chat-avoid]';
var HIDE='.arr,[data-mw-chat-hide]';
var btn,note,cfg;
function meta(n){var m=document.querySelector('meta[name="'+n+'"]');return m&&m.content}
function resolve(o){o=o||{};var id=o.id,name=o.name,s=o.agent;if(!id&&s&&REG[s]){id=REG[s][0];name=name||REG[s][1]}return id?{id:id,name:name||'your agent'}:null}
function css(){if(document.getElementById('mw-chat-css'))return;var l=document.createElement('link');l.id='mw-chat-css';l.rel='stylesheet';l.href=base+'mw-chat.css?v='+ver;document.head.appendChild(l)}
function url(){return 'grokbot://app/v1/agent?id='+encodeURIComponent(cfg.id)}
function showNote(){if(note)note.remove();note=document.createElement('div');note.className='mw-chat-note';note.setAttribute('role','status');note.textContent='Open this in the Grok Bot app to chat with '+cfg.name+'.';var s=document.createElement('small');s.textContent='Tap to close';note.appendChild(s);note.onclick=function(){note.remove();note=null};document.body.appendChild(note)}
function open(e){e.preventDefault();var left=false;function gone(){if(document.visibilityState==='hidden')left=true}function bl(){left=true}
 document.addEventListener('visibilitychange',gone);window.addEventListener('blur',bl);window.addEventListener('pagehide',bl);
 try{location.href=url()}catch(_){}
 setTimeout(function(){document.removeEventListener('visibilitychange',gone);window.removeEventListener('blur',bl);window.removeEventListener('pagehide',bl);if(!left&&document.visibilityState==='visible')showNote()},1200)}
function hit(a,b){return a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top}
function fixedish(el){for(;el&&el!==document.body;el=el.parentElement){var p=getComputedStyle(el).position;if(p==='fixed'||p==='sticky')return true}return false}
var TAP='a,button,input,select,textarea,[role=button],.arr';
function hits(sel,big){var r=btn.getBoundingClientRect(),pad={left:r.left-6,right:r.right+6,top:r.top-6,bottom:r.bottom+6},out=[];
 document.querySelectorAll(sel).forEach(function(el){if(el===btn||btn.contains(el))return;var q=el.getBoundingClientRect();if(!q.width||!q.height)return;if(big&&(q.height>innerHeight*.6))return;if(hit(pad,q))out.push(el)});return out}
function place(){if(!btn)return;btn.classList.remove('mw-chat-dock','mw-chat-hidden');btn.style.top='';btn.style.bottom='';
 var bad=hits(AVOID).concat(hits(TAP,true).filter(fixedish));if(!bad.length){if(hits(HIDE).length)btn.classList.add('mw-chat-hidden');return}
 var noScroll=document.scrollingElement.scrollHeight<=innerHeight+4;
 if(noScroll||bad.some(fixedish)){ /* fixed bars (app layouts): lift the button above them and any tap targets */
  for(var i=0;i<10;i++){var h=hits(AVOID).concat(hits(TAP,true));if(!h.length)return;var top=Math.min.apply(null,h.map(function(e){return e.getBoundingClientRect().top}));
   var b=innerHeight-top+8;if(b>innerHeight*.6){btn.classList.add('mw-chat-hidden');return}btn.style.bottom=b+'px'}return}
 var H=Math.max(document.documentElement.scrollHeight,document.body.scrollHeight);btn.classList.add('mw-chat-dock');btn.style.top=(H-44-16)+'px'}
function mount(o){var c=resolve(o);if(!c)return;cfg=c;css();if(!btn){btn=document.createElement('a');btn.className='mw-chat-btn mw-hover';btn.href=url();btn.addEventListener('click',open);
 btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true"><path d="M4 5h16v11H10l-4 3.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/></svg>';
 document.body.appendChild(btn);document.body.classList.add('mw-chat-on');var t;function q(){cancelAnimationFrame(t);t=requestAnimationFrame(place)}
 addEventListener('scroll',q,{passive:true});addEventListener('resize',q);new MutationObserver(q).observe(document.body,{childList:true,subtree:true});setTimeout(place,300);setTimeout(place,1500)}
 btn.href=url();btn.setAttribute('aria-label','Chat with '+cfg.name);btn.title='Chat with '+cfg.name;btn.setAttribute('data-agent-id',cfg.id);place()}
window.MWChat={mount:mount,registry:REG};
function auto(){var d=me&&me.dataset||{};var o={id:d.agentId||meta('mw-agent-id'),name:d.agentName||meta('mw-agent-name'),agent:d.agent||meta('mw-agent')};if(o.id||o.agent)mount(o)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',auto);else auto();
})();
