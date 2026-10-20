"""Art Taste Deck page (Max Oct 19 2026 10:58 PM ICT: 'show me a swipe deck with art. lets start to figure out what kind of art i like.').
The Max deck style (tools/eve1019_page.py TPL: dadbook layout in Max's brand, Khand + Hind, cream, terracotta / lagoon / jungle pops,
subtle shine and glow, Both / Neither / Love / Notes, 'Next deck coming shortly.', then (Max Oct 19 2026 11:27 PM ICT) footer 'Built by Machan' -> the Machan story page) patched so
the ART is the hero (pairs side by side from 700px up; on phones side by side unless both images are wide landscapes, then stacked): each option is a large framed artwork (img/<key>.jpg next to the page) with title, artist, year, a one-line
'what it is', three tags (style, era, mood) and a small image credit (source link + license). Team-gated submit via ../submit.js (unchanged).
Results: version-4 pairs format plus artA / artB {key,title,artist,year,style,era,mood} so follow-up decks can narrow by tag.
Usage: write(deck_json_dict, slug, meta) -> path   (meta: kicker, lede, em, h1, strip, art{key:{...}})"""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import json, os, html
from eve1019_page import TPL as BASE
def _patch(T):
    def rep(a, b):
        nonlocal T
        assert T.count(a) == 1, (a[:70], T.count(a)); T = T.replace(a, b)
    rep("@media (min-width:900px){.app{max-width:980px}}", "@media (min-width:900px){.app{max-width:1180px}}")
    rep("@media (min-width:1600px){.app{max-width:1240px}}@media (min-width:2200px){.app{max-width:1760px}",
        "@media (min-width:1600px){.app{max-width:1500px}}@media (min-width:2200px){.app{max-width:2300px}")
    rep("h1{font-size:72px}.lede{font-size:21px}", "h1{font-size:72px}.lede{font-size:21px}.opt .oa{font-size:18px}.opt .tg i{font-size:14px}.opt .cr{font-size:13px}.strip img{height:150px;max-width:260px}")
    rep(".opt svg{display:block;width:100%;height:auto}", """.opt .pk{display:block;width:100%;border:0;padding:0;margin:0;background:none;text-align:left;cursor:pointer;position:relative;color:inherit;font:inherit}
.frame{display:flex;align-items:center;justify-content:center;height:min(42vh,400px);padding:10px;background:radial-gradient(120% 90% at 50% 0%,#FFFDF8,#F2EADC)}
.frame img{display:block;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 8px 14px rgba(70,40,15,.22))}
@media (max-width:699px){.frame{height:auto;min-height:160px}.frame img{width:auto;max-width:100%;height:auto;max-height:52vh}}
@media (min-width:700px){.frame{height:min(56vh,620px);padding:14px}}
@media (min-width:1600px){.frame{height:min(62vh,880px);padding:18px}}
@media (min-width:2200px){.frame{height:min(64vh,1080px);padding:22px}}
.opt .oa{display:block;font-size:14.5px;color:var(--edge);font-weight:600;margin-top:1px}
.opt .tg{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}.opt .tg i{font-style:normal;font-size:11.5px;letter-spacing:.04em;padding:2px 8px;border-radius:999px;border:1px solid var(--line);background:#FBF6EC;color:#5A5047}
.opt .tg i:nth-child(1){border-color:rgba(5,102,141,.3);color:var(--lag)}.opt .tg i:nth-child(3){border-color:rgba(11,110,79,.3);color:var(--jun)}
.opt .cr{margin:0;padding:0 12px 10px 50px;font-size:10.5px;line-height:1.35;color:#8A8177}.opt .cr a{color:#7A6F64}
.strip{display:flex;gap:8px;justify-content:center;margin:2px 0 18px;overflow:hidden}.strip img{flex:1 1 0;min-width:0;max-width:150px;height:74px;object-fit:cover;border-radius:6px;box-shadow:0 6px 14px -8px rgba(70,40,15,.5);border:1px solid rgba(255,255,255,.8)}
@media (max-width:420px){.strip img:nth-child(n+5){display:none}}""")
    rep('   <ol class="steps">', '   <div class="strip" id="strip" aria-hidden="true"></div>\n   <ol class="steps">')
    rep("<strong>Swipe these ten pairs.</strong> Tap the one you like, or swipe toward it. Both, Neither and a Love heart are there too.",
        "<strong>Swipe twenty pairs of real art.</strong> Tap the one that pulls you in, or swipe toward it. Both, Neither, a Love heart and Notes are there too.")
    rep("<strong>Send your picks.</strong> They go to Swatch, who builds them into the boards.", "<strong>Send your picks.</strong> They go to Swatch, tagged by style, era and mood.")
    rep("<strong>The next deck follows</strong>, one notch further.", "<strong>The next deck narrows it down</strong> to the styles you love.")
    a = T.index("function opt(o,side){"); b = T.index("\nfunction render(){")
    T = T[:a] + """function opt(o,side){return `<div class="opt" data-side="${side}"><button class="pk sheen" aria-label="${side}: ${esc(o.l)}, ${esc(o.ar)}, ${esc(o.y)}"><span class="tick">${TICK}</span><span class="heart">${HEART}</span><span class="frame"><img src="img/${o.k}.jpg" width="${o.w}" height="${o.h}" alt="${esc(o.l)}, ${esc(o.ar)}, ${esc(o.y)}" decoding="async"></span><span class="ol"><span class="k">${side}</span><span><span class="ot">${esc(o.l)}</span><span class="oa">${esc(o.ar)} · ${esc(o.y)}</span><span class="od">${esc(o.d)}</span><span class="tg">${o.t.map(x=>`<i>${esc(x)}</i>`).join('')}</span></span></span></button><p class="cr">Image: <a href="${esc(o.cu)}" target="_blank" rel="noopener">${esc(o.cs)}</a> · ${esc(o.lic)} · ${esc(o.ho)}</p></div>`}
function preload(k){const p=D.pairs[k];if(!p)return;[p.A,p.B].forEach(o=>{const i=new Image();i.src='img/'+o.k+'.jpg'})}""" + T[b:]
    rep("""$('card').querySelectorAll('.opt').forEach(b=>{const s=b.dataset.side,on=a.c===s||a.c==='both';b.classList.toggle('sel',on);b.classList.toggle('dim',!!a.c&&!on);b.classList.toggle('loved',!!a.l&&on);b.setAttribute('aria-pressed',on);b.onclick=()=>{if(window._sw){window._sw=false;return}b.classList.add('tap');pick(s)}});""",
        """$('card').querySelectorAll('.opt').forEach(b=>{const s=b.dataset.side,on=a.c===s||a.c==='both',k=b.querySelector('.pk');b.classList.toggle('sel',on);b.classList.toggle('dim',!!a.c&&!on);b.classList.toggle('loved',!!a.l&&on);k.setAttribute('aria-pressed',on);k.onclick=()=>{if(window._sw){window._sw=false;return}k.classList.add('tap');pick(s)}});preload(S.i+1);""")
    rep("if(e.target.closest('textarea,summary,.chip'))return;", "if(e.target.closest('textarea,summary,.chip,.cr'))return;")
    rep("o={pair_id:p.id,choice:choiceOf(a),category:p.cat,labelA:p.A.l,labelB:p.B.l,tagsA:p.A.t,tagsB:p.B.t};",
        "art=x=>({key:x.k,title:x.l,artist:x.ar,year:x.y,style:x.t[0],era:x.t[1],mood:x.t[2]}),o={pair_id:p.id,choice:choiceOf(a),category:p.cat,question:p.q,labelA:p.A.l+' ('+p.A.ar+')',labelB:p.B.l+' ('+p.B.ar+')',tagsA:p.A.t,tagsB:p.B.t,artA:art(p.A),artB:art(p.B)};")
    rep("style:'max-deck',owner", "style:'max-deck',kind:'art-taste',owner")
    rep("$('kicker').textContent=D.kicker;$('lede').textContent=D.lede;",
        "$('kicker').textContent=D.kicker;$('lede').textContent=D.lede;$('strip').innerHTML=(D.strip||[]).map(k=>`<img src=\"img/${k}.jpg\" alt=\"\">`).join('');")
    rep("(()=>{const t=D.title,e=D.em", "(()=>{const t=D.h1||D.title,e=D.em")
    rep("</style></head>", """@media (min-width:1600px){.hero .lac{max-width:980px}.strip img{height:150px;max-width:240px}}
@media (min-width:2200px){.hero .lac{max-width:1360px;padding:56px 60px 50px}h1{font-size:108px}.lede{font-size:27px}.strip{gap:14px;margin-bottom:26px}.strip img{height:260px;max-width:420px;border-radius:10px}.steps span{font-size:21px}.steps b{width:40px;height:40px;font-size:22px}.hero .btn{min-height:66px;font-size:25px;padding:0 44px}.lab{font-size:17px}.endc h2{font-size:72px}.endc p{font-size:26px}.tri i{width:52px;height:4px}}
</style></head>""")
    rep('<footer><a href="https://maxweberman.com"><span>Built by Machan</span></a></footer>',
        '<footer><a href="https://webermanapps.github.io/style-swipe/machan-story-awczm5/"><span>Built by Machan</span></a></footer>')
    rep('<div class="pair" id="pair">', '<div class="pair${(p.A.w/p.A.h>1.15&&p.B.w/p.B.h>1.15)?\' wide\':\' duo\'}" id="pair">')
    rep("</style></head>", """@media (max-width:699px){.pair.duo{grid-template-columns:1fr 1fr;gap:8px}.pair.duo .frame{padding:6px;min-height:120px}.pair.duo .frame img{max-height:44vh}
.pair.duo .opt .ol{display:block;padding:8px 8px 10px}.pair.duo .opt .k{float:left;margin:0 6px 2px 0;width:22px;height:22px;font-size:13px}.pair.duo .opt .ot{font-size:16px}.pair.duo .opt .oa,.pair.duo .opt .od{font-size:12.5px;line-height:1.35}
.pair.duo .opt .tg{gap:3px}.pair.duo .opt .tg i{font-size:10px;padding:1px 6px}.pair.duo .opt .cr{padding:0 8px 8px;font-size:9.5px}.pair.duo .tick{width:24px;height:24px;top:6px;right:6px}}
</style></head>""")
    rep("<p>Thank you, Max.</p>", "<p>Thank you, Max. Your picks shape the next one.</p>")
    return T
TPL = _patch(BASE)
def write(dj, slug, meta):
    A = meta["art"]; P = []
    def side(o):
        x = A[o["art"]]
        return {"k": x["k"], "l": x["title"], "ar": x["artist"], "y": x["year"], "d": x["what"], "t": x["tags"], "w": x["w"], "h": x["h"],
                "cu": x["source"], "cs": x["source_name"], "lic": x["license"], "ho": x["holder"]}
    for p in dj["pairs"]:
        P.append({"id": p["id"], "cat": p["category"], "loc": "Art Taste", "q": p["ask"], "A": side(p["optionA"]), "B": side(p["optionB"])})
    data = json.dumps({"deck": dj["date"], "title": dj["title"], "h1": meta["h1"], "agent": dj.get("submit_agent", "branding"), "to": dj.get("submit_to", ""),
                       "pairs": P, "kicker": meta["kicker"], "lede": meta["lede"], "em": meta["em"], "strip": meta["strip"]}, ensure_ascii=False).replace("</", "<\\/")
    t = TPL.replace("__TITLE__", html.escape(dj["title"])).replace("__DATA__", data)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w", encoding="utf-8").write(t); return p
