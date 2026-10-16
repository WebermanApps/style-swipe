/* mw-chat cc8 (R74). Usage:
   <script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc8" data-agent-id="<uuid>" data-agent-name="Coach Agent" defer></script>
   or <meta name="mw-agent-id" content="<uuid>"> (+ optional <meta name="mw-agent-name">), or data-agent="<slug>" from the registry below,
   or call MWChat.mount({agent:'<slug>'}) / MWChat.mount({id,name}) later (deck pages). Opens grokbot://app/v1/agent?id=<id>. */
(function(){
var REG={'grok-bot':['24ff6404-25b2-46a1-8487-b99d3c7c7b06','Grok Bot'],'household':['c59ffdde-28bf-4ad7-8dd8-22f5e941647d','Household'],'email-sorting':['d31d8de8-a97a-4bc3-823f-e4946a383e87','Email Sorting'],'branding':['3fac5054-3a3d-49b1-af61-59883f7fdc78','Branding Agent'],'upkeep':['f0d420ad-d37e-44d3-be6f-053da2b6e24d','UpKeep Agent'],'blog':['57b6fc9e-e2fc-45ba-b28e-73f066c4b0fa','Blog Agent'],'coach':['758a3343-fff3-4093-9169-81f79ffdc3ef','Coach Agent'],'jokes':['0f68b81e-50fc-455c-b558-a13f7cd796aa','Jokes Agent'],'legal':['55ae1827-d0b6-4a4a-98f1-551dc6f0ef3a','Legal Agent'],'portfolio':['cbf1a856-abbb-410a-99a0-cb65d213fc21','Portfolio Agent'],'prop':['f466837e-6ecd-4c83-9ac9-5f031aa92add','Prop Agent'],'research':['6efe5de2-9a20-43d9-a1eb-068e645ed407','Research Agent'],'security':['d47b42b5-3764-4c66-9360-3d4c931d0483','Security Agent'],'video-photo':['eca52f98-7367-4a43-9b92-47366636826e','Video & Photo Agent']};
var me=document.currentScript,base=(me&&me.src||'').replace(/mw-chat\.js(\?.*)?$/,''),ver=((me&&me.src||'').match(/\?v=([^&]+)/)||[])[1]||'cc8';
var AVOID='#share,.shic,.mw-share,footer,.mw-footer,#routines,.mw-sec-routines,[data-routines],[data-mw-chat-avoid]';
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
function place(){if(!btn)return;btn.classList.remove('mw-chat-dock');btn.style.top='';var r=btn.getBoundingClientRect(),pad={left:r.left-6,right:r.right+6,top:r.top-6,bottom:r.bottom+6},bad=false;
 document.querySelectorAll(AVOID).forEach(function(el){if(bad||el===btn)return;var q=el.getBoundingClientRect();if(q.width&&q.height&&hit(pad,q))bad=true});
 if(bad){var h=Math.max(document.documentElement.scrollHeight,document.body.scrollHeight);btn.classList.add('mw-chat-dock');btn.style.top=(h-44-16)+'px'}}
function mount(o){var c=resolve(o);if(!c)return;cfg=c;css();if(!btn){btn=document.createElement('a');btn.className='mw-chat-btn mw-hover';btn.href=url();btn.addEventListener('click',open);
 btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true"><path d="M4 5h16v11H10l-4 3.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/></svg>';
 document.body.appendChild(btn);document.body.classList.add('mw-chat-on');var t;function q(){cancelAnimationFrame(t);t=requestAnimationFrame(place)}
 addEventListener('scroll',q,{passive:true});addEventListener('resize',q);new MutationObserver(q).observe(document.body,{childList:true,subtree:true});setTimeout(place,300);setTimeout(place,1500)}
 btn.href=url();btn.setAttribute('aria-label','Chat with '+cfg.name);btn.title='Chat with '+cfg.name;btn.setAttribute('data-agent-id',cfg.id);place()}
window.MWChat={mount:mount,registry:REG};
function auto(){var d=me&&me.dataset||{};var o={id:d.agentId||meta('mw-agent-id'),name:d.agentName||meta('mw-agent-name'),agent:d.agent||meta('mw-agent')};if(o.id||o.agent)mount(o)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',auto);else auto();
})();
