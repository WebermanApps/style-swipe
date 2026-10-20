"""Deck page in Max's NEW deck style (Max chose it Oct 19 2026 evening): the dadbook layout (pitch-style cover with simple steps, an elegant
card with Both / Neither / Love heart / Notes, subtle top-edge shine and slow sheen, warm glow, clean last page 'Next deck coming shortly.')
in Max's own brand: Khand + Hind (no book serif), cream base, terracotta / lagoon / jungle pops, 'Built by Machan' footer to
maxweberman.com. Team-gated submit: ../submit.js (MWSubmit.send asks for the team password; not edited). Results keep the version-4 pairs
format (choice A / B / both / neither / skip, loveA / loveB) so the pull + stats pipeline reads them unchanged.
Usage (from tools/build_eve_1019.py): write(deck_json_dict, slug, meta) -> path"""
import json, os, html
def _ask(a):
    loc, rest = a.split(":", 1); el, q = rest.split(",", 1); return loc.strip(), el.strip(), q.strip()[:1].upper() + q.strip()[1:]
def write(dj, slug, meta):
    did = dj["date"]; P = []
    for p in dj["pairs"]:
        loc, el, q = _ask(p["ask"])
        P.append({"id": p["id"], "cat": p.get("category") or el, "loc": loc, "q": q,
                  "A": {"l": p["optionA"]["label"], "d": p["optionA"]["desc"], "s": p["optionA"]["visual"]["svg"], "t": p["optionA"].get("tags", [])},
                  "B": {"l": p["optionB"]["label"], "d": p["optionB"]["desc"], "s": p["optionB"]["visual"]["svg"], "t": p["optionB"].get("tags", [])}})
    data = json.dumps({"deck": did, "title": dj["title"], "agent": dj.get("submit_agent", "branding"), "to": dj.get("submit_to", ""), "pairs": P,
                       "kicker": meta["kicker"], "lede": meta["lede"], "em": meta["em"]}, ensure_ascii=False).replace("</", "<\\/")
    t = TPL.replace("__TITLE__", html.escape(dj["title"])).replace("__DATA__", data)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w", encoding="utf-8").write(t); return p
TPL = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="light only"><meta name="theme-color" content="#FAF6EE">
<title>__TITLE__ · Style Swipe</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600;700&family=Khand:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{--paper:#FAF6EE;--card:#FFFEFB;--ink:#1F1B16;--mute:#6B645A;--line:#E6DCCB;--tc:#C1502E;--edge:#8A4A2E;--lag:#05668D;--jun:#0B6E4F;--sans:Hind,system-ui,-apple-system,sans-serif;--lab:Khand,Hind,system-ui,sans-serif}
*{box-sizing:border-box}html,body{margin:0;min-height:100%}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5;-webkit-tap-highlight-color:transparent;
 background-image:radial-gradient(120% 60% at 50% -10%,rgba(193,80,46,.09),transparent 60%),radial-gradient(90% 50% at 85% 110%,rgba(5,102,141,.07),transparent 60%),radial-gradient(70% 40% at 0% 100%,rgba(11,110,79,.06),transparent 60%);background-attachment:fixed}
button{font:inherit;color:inherit}
.app{max-width:620px;margin:0 auto;min-height:100dvh;display:flex;flex-direction:column;padding:calc(env(safe-area-inset-top) + 14px) 16px 0}
@media (min-width:900px){.app{max-width:980px}}
@media (min-width:1600px){.app{max-width:1240px}}@media (min-width:2200px){.app{max-width:1760px}body{font-size:20px}.q{font-size:26px}.opt .ot{font-size:24px}.opt .od{font-size:17px}.chip{min-height:58px;font-size:20px}.lab{font-size:15px}.count{font-size:22px}.hero .lac{max-width:860px;padding:40px 36px 34px}h1{font-size:72px}.lede{font-size:21px}.steps span{font-size:18px}footer{font-size:16px}footer a{font-size:20px}}
.scr{display:none;flex:1;flex-direction:column}.scr.on{display:flex}
@media (prefers-reduced-motion:no-preference){.scr.on{animation:rise .5s cubic-bezier(.2,.8,.2,1) both}}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.lab{font-family:var(--lab);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:13px;color:var(--mute)}
/* subtle shine: top-edge highlight + warm inner glow (Brand Bank) */
.lac{position:relative;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;
 box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 18px 40px -22px rgba(110,62,30,.32),0 2px 6px rgba(110,62,30,.06)}
.lac::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.95),transparent);pointer-events:none;z-index:2}
.lac::after{content:"";position:absolute;inset:0 0 auto 0;height:36%;background:linear-gradient(180deg,rgba(255,246,230,.5),rgba(255,246,230,0));pointer-events:none;z-index:0}.lac>*{position:relative;z-index:1}
.sheen{position:relative;overflow:hidden}
.sheen::after{content:"";position:absolute;top:0;bottom:0;left:-60%;width:40%;background:linear-gradient(100deg,transparent,rgba(255,250,235,.4),transparent);transform:skewX(-18deg);pointer-events:none;opacity:0}
@media (hover:hover) and (prefers-reduced-motion:no-preference){.sheen:hover::after{animation:sweep 1.6s ease-out}}
@media (prefers-reduced-motion:no-preference){.sheen.tap::after{animation:sweep 1.4s ease-out}}
@keyframes sweep{0%{left:-60%;opacity:1}100%{left:130%;opacity:1}}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:52px;padding:0 26px;border-radius:999px;border:1px solid var(--edge);background:var(--tc);color:#FFF8F0;font-family:var(--lab);font-weight:600;font-size:19px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;
 box-shadow:0 1px 0 rgba(255,255,255,.35) inset,0 10px 22px -12px rgba(138,74,46,.7);touch-action:manipulation}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line);box-shadow:0 1px 0 #fff inset}
.btn:focus-visible,.chip:focus-visible,.opt:focus-visible,.iconb:focus-visible{outline:2px solid var(--lag);outline-offset:3px}
.tri{display:flex;justify-content:center;gap:6px;margin:4px 0 10px}.tri i{display:block;width:34px;height:3px;border-radius:2px;background:var(--tc)}.tri i:nth-child(2){background:var(--lag)}.tri i:nth-child(3){background:var(--jun)}
/* cover */
.hero{flex:1;display:flex;flex-direction:column;justify-content:center;padding:10px 0 18px}
.hero .lac{padding:28px 22px 24px;text-align:center;max-width:620px;margin:0 auto;width:100%}
h1{font-family:var(--lab);font-weight:700;font-size:clamp(36px,10vw,54px);line-height:1;margin:6px 0 10px;letter-spacing:.005em}
h1 em{font-style:normal;color:var(--tc)}
.lede{font-size:18px;color:#4F453D;margin:0 0 18px}
.steps{list-style:none;margin:0 0 20px;padding:0;text-align:left;display:grid;gap:10px}
.steps li{display:flex;gap:12px;align-items:flex-start;padding:10px 12px;border-radius:12px;background:rgba(250,246,238,.85);border:1px solid var(--line)}
.steps b{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-family:var(--lab);font-size:18px;color:#fff;background:var(--tc);box-shadow:0 1px 0 rgba(255,255,255,.4) inset}
.steps li:nth-child(2) b{background:var(--lag)}.steps li:nth-child(3) b{background:var(--jun)}
.steps span{font-size:15.5px;line-height:1.4}.steps strong{font-weight:600}
/* deck */
.top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.prog{flex:1;height:4px;border-radius:4px;background:var(--line);overflow:hidden}.prog i{display:block;height:100%;background:linear-gradient(90deg,var(--jun),var(--lag),var(--tc));width:0;transition:width .35s ease}
.count{font-family:var(--lab);font-weight:600;font-size:19px;color:var(--mute);min-width:56px;text-align:right}
.iconb{width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--card);display:grid;place-items:center;cursor:pointer}
.card{padding:16px 14px 16px;touch-action:pan-y;user-select:none;-webkit-user-select:none}
@media (prefers-reduced-motion:no-preference){.card{transition:transform .28s cubic-bezier(.2,.8,.2,1),opacity .28s ease}}
.topic{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:2px;text-align:center}
.topic .lab{color:var(--lag)}.topic .cat{color:var(--tc)}
.q{font-size:19px;line-height:1.35;text-align:center;margin:4px auto 14px;color:#3A312B;max-width:46em;font-weight:500}
.pair{display:grid;grid-template-columns:1fr;gap:14px}
@media (min-width:700px){.pair{grid-template-columns:1fr 1fr}}
.opt{position:relative;display:block;width:100%;border:1px solid var(--line);padding:0;background:#fff;cursor:pointer;text-align:left;border-radius:14px;overflow:hidden;
 box-shadow:0 10px 22px -16px rgba(60,30,10,.45);transition:transform .25s ease,opacity .25s ease,filter .25s ease,box-shadow .25s ease}
.opt svg{display:block;width:100%;height:auto}
.opt .ol{display:flex;gap:10px;align-items:flex-start;padding:10px 12px 12px;border-top:1px solid var(--line)}
.opt .k{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-family:var(--lab);font-weight:700;font-size:16px;color:#fff;background:var(--lag)}
.opt[data-side=B] .k{background:var(--jun)}
.opt .ot{font-family:var(--lab);font-weight:600;font-size:19px;line-height:1.1;display:block}.opt .od{font-size:14.5px;color:#4F453D;display:block;margin-top:2px}
.opt.sel{box-shadow:0 0 0 3px var(--paper),0 0 0 5px var(--tc),0 16px 30px -16px rgba(193,80,46,.6);transform:translateY(-3px)}
.opt.sel::before{content:"";position:absolute;inset:0;background:radial-gradient(80% 60% at 50% 0%,rgba(193,80,46,.10),transparent 70%);pointer-events:none;z-index:1}
.opt.dim{opacity:.55;filter:saturate(.7)}@media (hover:hover){.opt:not(.sel):hover{transform:translateY(-2px)}}
.tick{position:absolute;top:10px;right:10px;width:30px;height:30px;border-radius:50%;background:var(--tc);color:#fff;display:none;place-items:center;z-index:2;box-shadow:0 4px 10px rgba(110,62,30,.35)}
.opt.sel .tick{display:grid}.opt .heart{position:absolute;top:10px;left:10px;color:var(--tc);display:none;z-index:2}.opt.loved .heart{display:block}
.acts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:16px auto 0;max-width:520px}
.chip{position:relative;overflow:hidden;min-height:48px;transition:background .2s ease,color .2s ease,border-color .2s ease;border-radius:999px;border:1px solid var(--line);background:linear-gradient(180deg,#FFFFFF,#FBF5EA);font-family:var(--lab);font-weight:600;font-size:17px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 1px 0 #fff inset;touch-action:manipulation}
.chip.on{border-color:var(--edge);background:var(--tc);color:#FFF8F0}
.chip.love.on{background:#fff;color:var(--tc);border-color:var(--tc)}
.chip svg{width:18px;height:18px}
.hint{text-align:center;font-size:13.5px;color:var(--mute);margin:10px 0 0}
details.notes{margin:12px auto 0;border-top:1px dashed var(--line);padding-top:8px;max-width:720px}
details.notes summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:44px;font-size:15px;color:#4F453D}
details.notes summary::-webkit-details-marker{display:none}
details.notes summary .sm{font-size:13px;color:var(--mute);max-width:60%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
details.notes textarea{width:100%;min-height:84px;border:1px solid var(--line);border-radius:12px;padding:10px 12px;font:16px/1.45 var(--sans);background:#FFFEFB;color:var(--ink);resize:vertical}
details.notes textarea:focus{outline:2px solid rgba(5,102,141,.35);border-color:var(--lag)}
.saved{font-size:12.5px;color:var(--jun);min-height:1.2em;margin-top:4px}
.nav{display:flex;justify-content:space-between;align-items:center;margin-top:12px;gap:10px}
/* send */
.sum{padding:20px 18px;max-width:720px;margin:0 auto;width:100%}
.sum h2,.endc h2{font-family:var(--lab);font-weight:700;font-size:36px;line-height:1.05;margin:4px 0 6px;text-align:center}
.sum p.c{text-align:center;color:#4F453D;margin:0 0 14px}
.list{list-style:none;padding:0;margin:0 0 16px;max-height:44vh;overflow:auto;border-top:1px solid var(--line)}
.list li{display:flex;gap:10px;padding:9px 2px;border-bottom:1px solid var(--line);font-size:15px;line-height:1.35}
.list li .n{font-family:var(--lab);font-weight:600;color:var(--lag);min-width:22px}
.list li i{color:var(--mute);font-style:normal}.list li .h{color:var(--tc);margin-left:auto}
.stack{display:grid;gap:10px}.msg{text-align:center;font-size:14px;color:var(--mute);min-height:1.3em;display:flex;align-items:center;justify-content:center;gap:8px}
/* Machan bounces on loaders (standing rule) */
.mcl{display:none;width:22px;height:22px}.msg.busy .mcl{display:block}
@media (prefers-reduced-motion:no-preference){.msg.busy .mcl{animation:hop .7s cubic-bezier(.3,.7,.4,1) infinite alternate}}
@keyframes hop{from{transform:translateY(0)}to{transform:translateY(-7px)}}
/* end */
.endc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 10px}
.endc p{font-size:18px;color:#4F453D;margin:6px 0 0}
footer{text-align:center;padding:22px 0 calc(env(safe-area-inset-bottom) + 18px);font-size:14px;color:var(--mute)}
footer a{display:inline-flex;align-items:center;min-height:44px;color:var(--edge);text-decoration:none;font-family:var(--lab);font-weight:600;font-size:17px;letter-spacing:.06em}
footer a span{border-bottom:1px solid rgba(138,74,46,.35)}footer a:hover{color:var(--tc)}
</style></head><body>
<div class="app">
 <section class="scr on" id="s-cover" aria-label="Cover">
  <div class="hero"><div class="lac sheen" id="coverCard">
   <div class="lab" id="kicker"></div>
   <h1 id="h1"></h1>
   <div class="tri" aria-hidden="true"><i></i><i></i><i></i></div>
   <p class="lede" id="lede"></p>
   <ol class="steps">
    <li><b>1</b><span><strong>Swipe these ten pairs.</strong> Tap the one you like, or swipe toward it. Both, Neither and a Love heart are there too.</span></li>
    <li><b>2</b><span><strong>Send your picks.</strong> They go to Swatch, who builds them into the boards.</span></li>
    <li><b>3</b><span><strong>The next deck follows</strong>, one notch further.</span></li>
   </ol>
   <button class="btn sheen" id="begin">Begin <span aria-hidden="true">→</span></button>
   <p class="hint" id="resume" hidden></p>
  </div></div>
 </section>
 <section class="scr" id="s-deck" aria-label="Pairs">
  <div class="top"><button class="iconb" id="home" aria-label="Back to cover"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg></button><div class="prog"><i id="bar"></i></div><div class="count" id="count"></div></div>
  <div class="lac card" id="card"></div>
  <div class="nav"><button class="btn ghost" id="prev">← Back</button><button class="btn ghost" id="next">Skip →</button></div>
 </section>
 <section class="scr" id="s-send" aria-label="Send your picks">
  <div class="lac sum">
   <h2>Good picks.</h2>
   <div class="tri" aria-hidden="true"><i></i><i></i><i></i></div>
   <p class="c">Here is your list. Send it and Swatch builds it in.</p>
   <ul class="list" id="list"></ul>
   <div class="stack">
    <button class="btn sheen" id="send">Send my picks</button>
    <div class="msg" id="msg" role="status" aria-live="polite"><svg class="mcl" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z" fill="#3F7D58"/><path d="M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z" fill="#5E9A6E"/><rect x="3.5" y="5.5" width="17" height="16" rx="7" fill="#C8643F"/><rect x="5.5" y="9" width="13" height="10" rx="5" fill="#FAF6EE"/><circle cx="9.6" cy="13.3" r="1.35" fill="#2E6F86"/><circle cx="14.4" cy="13.3" r="1.35" fill="#2E6F86"/><path d="M10.6 16.1q1.4 1.1 2.8 0" fill="none" stroke="#C8643F" stroke-width="1.1" stroke-linecap="round"/></svg><span id="msgt"></span></div>
    <button class="btn ghost" id="copy">Copy my picks</button>
    <button class="btn ghost" id="toEnd">Finish</button>
    <button class="btn ghost" id="review" style="border:0">← Review my picks</button>
   </div>
  </div>
 </section>
 <section class="scr" id="s-end" aria-label="Done">
  <div class="endc"><div class="tri" aria-hidden="true"><i></i><i></i><i></i></div><h2>Next deck coming shortly.</h2><p>Thank you, Max.</p></div>
 </section>
 <footer><a href="https://maxweberman.com"><span>Built by Machan</span></a></footer>
</div>
<script src="../submit.js?v=gr2"></script>
<script>
const D=__DATA__;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,N=D.pairs.length,KEY='mwdeck:'+D.deck+':v1';
let S={i:0,a:{}};try{S=Object.assign(S,JSON.parse(localStorage.getItem(KEY)||'{}'))}catch(_){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(_){}};
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
$('kicker').textContent=D.kicker;$('lede').textContent=D.lede;
(()=>{const t=D.title,e=D.em&&t.indexOf(D.em)>=0?D.em:'';const h=$('h1');if(!e){h.textContent=t;return}const i=t.indexOf(e);h.append(t.slice(0,i));const m=document.createElement('em');m.textContent=e;h.append(m,t.slice(i+e.length))})();
function show(id){document.querySelectorAll('.scr').forEach(s=>s.classList.toggle('on',s.id===id));scrollTo({top:0,behavior:RM?'auto':'smooth'});history.replaceState(null,'','#'+id.slice(2)+(id==='s-deck'?'-'+(S.i+1):''))}
const HEART='<svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.2 5.3 3.1 1.7-1.9 3.2-3.1 5.3-3.1 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21z"/></svg>';
const TICK='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
function opt(o,side){return `<button class="opt sheen" data-side="${side}" aria-label="${side}: ${esc(o.l)}"><span class="tick">${TICK}</span><span class="heart">${HEART}</span>${o.s}<span class="ol"><span class="k">${side}</span><span><span class="ot">${esc(o.l)}</span><span class="od">${esc(o.d)}</span></span></span></button>`}
function render(){const p=D.pairs[S.i],a=S.a[S.i]||{};
 $('count').textContent=(S.i+1)+' / '+N;$('bar').style.width=(answered()/N*100)+'%';
 $('card').innerHTML=`<div class="topic"><span class="lab">${esc(p.loc)}</span><span class="lab" aria-hidden="true">·</span><span class="lab cat">${esc(p.cat)}</span></div><p class="q">${esc(p.q)}</p>
 <div class="pair" id="pair">${opt(p.A,'A')}${opt(p.B,'B')}</div>
 <div class="acts"><button class="chip sheen" data-c="both">Both</button><button class="chip love sheen" data-love aria-pressed="false">${HEART}Love</button><button class="chip sheen" data-c="neither">Neither</button></div>
 <p class="hint">Tap one, or swipe left for A and right for B. <span style="white-space:nowrap">Love = really want this.</span></p>
 <details class="notes"${a.n?' open':''}><summary><span style="white-space:nowrap">✎ Add a note</span><span class="sm">${esc(a.n||'')}</span></summary><textarea id="note" placeholder="Anything at all: what to change, what you'd rather see." aria-label="Note for this pair">${esc(a.n||'')}</textarea><div class="saved" id="saved"></div></details>`;
 $('card').querySelectorAll('.opt').forEach(b=>{const s=b.dataset.side,on=a.c===s||a.c==='both';b.classList.toggle('sel',on);b.classList.toggle('dim',!!a.c&&!on);b.classList.toggle('loved',!!a.l&&on);b.setAttribute('aria-pressed',on);b.onclick=()=>{if(window._sw){window._sw=false;return}b.classList.add('tap');pick(s)}});
 $('card').querySelectorAll('.chip[data-c]').forEach(b=>{b.classList.toggle('on',a.c===b.dataset.c);b.setAttribute('aria-pressed',a.c===b.dataset.c);b.onclick=()=>pick(b.dataset.c)});
 const lv=$('card').querySelector('[data-love]');lv.classList.toggle('on',!!a.l);lv.setAttribute('aria-pressed',!!a.l);lv.onclick=()=>{const x=S.a[S.i]||(S.a[S.i]={});x.l=!x.l;save();render()};
 let t;$('note').oninput=e=>{const x=S.a[S.i]||(S.a[S.i]={});x.n=e.target.value;x.at=new Date().toISOString();save();$('card').querySelector('.sm').textContent=x.n;clearTimeout(t);$('saved').textContent='Saved';t=setTimeout(()=>$('saved').textContent='',1400)};
 $('prev').style.visibility=S.i===0?'hidden':'visible';$('next').textContent=a.c?(S.i===N-1?'Finish →':'Next →'):(S.i===N-1?'Skip and finish →':'Skip →')}
let adv;function pick(c){const x=S.a[S.i]||(S.a[S.i]={});x.c=(x.c===c&&c!=='A'&&c!=='B')?undefined:c;save();render();clearTimeout(adv);
 if(x.c&&!$('card').querySelector('details').open)adv=setTimeout(()=>go(1),RM?250:560)}
function go(d){clearTimeout(adv);const n=S.i+d;if(n>=N){toSend();return}if(n<0)return;const card=$('card');if(!RM){card.style.opacity=0;card.style.transform=`translateX(${d>0?-24:24}px)`}
 setTimeout(()=>{S.i=n;save();render();location.hash='deck-'+(S.i+1);if(!RM){card.style.transform=`translateX(${d>0?24:-24}px)`;requestAnimationFrame(()=>{card.style.opacity=1;card.style.transform=''})}},RM?0:160)}
(()=>{const el=$('card');let x0=null,y0=0,dx=0;el.addEventListener('pointerdown',e=>{if(e.target.closest('textarea,summary,.chip'))return;x0=e.clientX;y0=e.clientY;dx=0},{passive:true});
 el.addEventListener('pointermove',e=>{if(x0==null)return;dx=e.clientX-x0;if(Math.abs(dx)>Math.abs(e.clientY-y0)&&!RM)el.style.transform=`translateX(${dx*.35}px) rotate(${dx*.02}deg)`},{passive:true});
 const end=()=>{if(x0==null)return;el.style.transform='';if(Math.abs(dx)>70){window._sw=true;setTimeout(()=>window._sw=false,400);pick(dx<0?'A':'B')}else if(Math.abs(dx)>8){window._sw=true;setTimeout(()=>window._sw=false,400)}x0=null};el.addEventListener('pointerup',end);el.addEventListener('pointercancel',()=>{x0=null;el.style.transform=''})})();
addEventListener('keydown',e=>{if(!$('s-deck').classList.contains('on')||e.target.tagName==='TEXTAREA')return;if(e.key==='ArrowLeft')pick('A');if(e.key==='ArrowRight')pick('B');if(e.key==='ArrowDown')pick('neither');if(e.key==='ArrowUp')pick('both')});
$('prev').onclick=()=>go(-1);$('next').onclick=()=>go(1);$('home').onclick=()=>show('s-cover');
function answered(){return Object.keys(S.a).filter(k=>S.a[k]&&S.a[k].c).length}
function startAt(){for(let k=0;k<N;k++)if(!(S.a[k]&&S.a[k].c))return k;return N-1}
$('begin').onclick=()=>{S.i=answered()?startAt():0;save();render();show('s-deck')};
if(answered()){$('resume').hidden=false;$('resume').textContent=answered()+' of '+N+' picked. Tap Begin to carry on.'}
function label(k){const p=D.pairs[k],a=S.a[k]||{};if(!a.c)return null;return a.c==='A'?p.A.l:a.c==='B'?p.B.l:a.c==='both'?p.A.l+' + '+p.B.l:'Neither'}
function choiceOf(a){if(!a||!a.c)return 'skip';if(a.l&&(a.c==='A'||a.c==='B'))return 'love'+a.c;return a.c}
function results(){const picks=D.pairs.map((p,k)=>{const a=S.a[k]||{},o={pair_id:p.id,choice:choiceOf(a),category:p.cat,labelA:p.A.l,labelB:p.B.l,tagsA:p.A.t,tagsB:p.B.t};if(a.l)o.love=true;if(a.n)o.note=a.n;return o});
 const un=picks.filter(x=>x.choice==='skip').map(x=>x.pair_id);
 return {app:'style-swipe',version:4,format:'pairs',style:'max-deck',owner:'Max Weberman',deck:D.deck,answered:answered(),total:N,picks,unanswered:[],skipped:un,partial:false,to:D.to,agent:D.agent,exported_at:new Date().toISOString()}}
function notesText(){return D.pairs.map((p,k)=>{const a=S.a[k]||{};return a.n?JSON.stringify({pair_id:p.id,category:p.cat,label:p.A.l+' vs '+p.B.l,answer:choiceOf(a),note:a.n,at:a.at||new Date().toISOString()}):null}).filter(Boolean).join('\n')}
function toSend(){$('list').innerHTML=D.pairs.map((p,k)=>{const a=S.a[k]||{},l=label(k);return `<li><span class="n">${k+1}</span><span>${esc(p.cat)}: ${l?esc(l):'<i>Skipped</i>'}${a.n?`<br><i>“${esc(a.n)}”</i>`:''}</span>${a.l?'<span class="h" aria-label="Loved">♥</span>':''}</li>`}).join('');show('s-send')}
function picksText(){return D.title+': my picks\n'+D.pairs.map((p,k)=>{const a=S.a[k]||{},l=label(k);return (k+1)+'. '+p.cat+': '+(l||'Skipped')+(a.l?' (Love)':'')+(a.n?' ('+a.n+')':'')}).join('\n')}
function busy(on,t){const m=$('msg');m.classList.toggle('busy',!!on);$('msgt').textContent=t||''}
$('send').onclick=async()=>{const b=$('send');b.disabled=true;b.textContent='Sending…';busy(true,'Sending…');
 let ok=false;const slow=setTimeout(()=>busy(true,'Still sending… give it a moment.'),6000);
 try{ok=window.MWSubmit?await MWSubmit.send({agent:D.agent,app:'style-swipe',deck:D.deck,results:results(),notes:notesText(),partial:false,answered:answered(),total:N,unanswered:N-answered()}):false}catch(_){}clearTimeout(slow);
 b.disabled=false;if(ok){b.textContent='Sent ✓';busy(false,'Sent. Swatch has your picks.');setTimeout(()=>show('s-end'),1400)}
 else{b.textContent='Send my picks';busy(false,window.MWSubmit&&MWSubmit.blocked?'Not sent: the team password is needed to send.':'Saved here and will retry. You can also copy your picks.')}};
$('copy').onclick=async()=>{const t=picksText();try{await navigator.clipboard.writeText(t);busy(false,'Copied.')}catch(_){busy(false,'Copy did not work here.')}};
$('toEnd').onclick=()=>show('s-end');$('review').onclick=()=>{S.i=0;render();show('s-deck')};
addEventListener('hashchange',()=>{const h=location.hash.slice(1),m=h.match(/^deck-(\d+)$/),on=id=>$(id).classList.contains('on');if(m){const k=Math.min(N-1,Math.max(0,+m[1]-1));if(k!==S.i||!on('s-deck')){S.i=k;save();render();if(!on('s-deck'))show('s-deck')}}else if(h==='send'&&!on('s-send'))toSend();else if(h==='end'&&!on('s-end'))show('s-end');else if((h===''||h==='cover')&&!on('s-cover'))show('s-cover')});
(function(){const h=location.hash.slice(1),m=h.match(/^deck-(\d+)$/);if(m){S.i=Math.min(N-1,Math.max(0,+m[1]-1));render();show('s-deck')}else if(h==='send')toSend();else if(h==='end')show('s-end');else render()})();
</script>
<!--mw-pairfit v1--><style id="mw-pairfit">/* mw-pairfit v1 (Max, Oct 19 2026 11:26 PM ICT): a pair sits side by side from 700px up; under 700px it stays side by side unless BOTH options are landscape (aspect > 1.2), then it stacks. */
@media (min-width:700px){.pair,.opts:not(.single){grid-template-columns:1fr 1fr!important}}
@media (max-width:699.98px){.pair{grid-template-columns:1fr 1fr!important;gap:8px!important}.pair.mw-pair-wide,.pair.wide{grid-template-columns:1fr!important;gap:14px!important}
.opts.mw-pair-wide{grid-template-columns:1fr!important;grid-template-rows:minmax(0,1fr) minmax(0,1fr)!important}}
</style><script id="mw-pairfit-js">/* mw-pairfit v1: reads each option's aspect from data-aspect, else from its visual (.stage / .vis): a card with its own text uses its CSS aspect-ratio (none = not landscape);
 otherwise the main <img> natural size, <video> size, <canvas> size, or <svg> viewBox (an <svg> whose <image> fills 30%+ of it uses that image's width/height attributes). Read-only: it loads nothing, fetches nothing and only toggles one class. */
(function(){var R=1.2,SEL='.pair,.opts:not(.single)',q=0;
function num(v){if(!v)return 0;var m=String(v).split(/[\/:x]/),a=parseFloat(m[0]),b=m.length>1?parseFloat(m[1]):1;return a>0&&b>0?a/b:0}
function txt(v){var w=document.createTreeWalker(v,NodeFilter.SHOW_TEXT,null),n;while((n=w.nextNode()))if(n.nodeValue.trim()&&!(n.parentElement&&n.parentElement.closest('svg,script,style')))return true;return false}
function ar(o){var d=o.hasAttribute('data-aspect')?o:o.querySelector('[data-aspect]');if(d){var x=num(d.getAttribute('data-aspect'));if(x)return x}
 var v=o.querySelector('.stage,.vis'),L;
 if(v){if(txt(v)){var c=v.firstElementChild;return c?num(getComputedStyle(c).aspectRatio.replace('auto','').trim()):0}L=v.querySelectorAll('img,video,canvas,svg')}
 else L=o.querySelectorAll('img,video,canvas,svg');
 var best=null,ba=0;[].forEach.call(L,function(e){if(e.closest('.tick,.heart,.side,.k,.ol,.ic'))return;if(e.tagName.toLowerCase()==='svg'&&e.parentElement&&e.parentElement.closest('svg'))return;var r=e.getBoundingClientRect(),a=r.width*r.height;if(a>ba){ba=a;best=e}});
 if(!best||ba<1500)return 0;var t=best.tagName.toLowerCase();
 if(t==='img')return best.naturalWidth&&best.naturalHeight?best.naturalWidth/best.naturalHeight:0;
 if(t==='video')return best.videoWidth&&best.videoHeight?best.videoWidth/best.videoHeight:num(best.getAttribute('width')+'/'+best.getAttribute('height'));
 if(t==='canvas')return best.width&&best.height?best.width/best.height:0;
 var vb=best.viewBox&&best.viewBox.baseVal,sw=vb&&vb.width?vb.width:parseFloat(best.getAttribute('width')),sh=vb&&vb.height?vb.height:parseFloat(best.getAttribute('height')),im=null,ia=0;
 [].forEach.call(best.querySelectorAll('image'),function(i){var w=parseFloat(i.getAttribute('width')),h=parseFloat(i.getAttribute('height'));if(w>0&&h>0&&w*h>ia){ia=w*h;im=w/h}});
 if(im&&sw&&sh&&ia>=.3*sw*sh)return im;return sw>0&&sh>0?sw/sh:0}
function fit(p){var o=[].filter.call(p.children,function(c){return c.classList.contains('opt')});var w=o.length===2&&ar(o[0])>R&&ar(o[1])>R;if(p.classList.contains('mw-pair-wide')!==w)p.classList.toggle('mw-pair-wide',w)}
function all(){q=0;[].forEach.call(document.querySelectorAll(SEL),fit)}
function soon(){if(!q)q=requestAnimationFrame(all)}
document.addEventListener('load',function(e){var t=e.target;if(t&&(t.tagName==='IMG'||t.tagName==='image')&&t.closest&&t.closest(SEL))soon()},true);
document.addEventListener('loadedmetadata',function(e){if(e.target&&e.target.closest&&e.target.closest(SEL))soon()},true);
new MutationObserver(soon).observe(document.documentElement,{childList:true,subtree:true});soon()})();
</script><!--/mw-pairfit-->
</body></html>'''
