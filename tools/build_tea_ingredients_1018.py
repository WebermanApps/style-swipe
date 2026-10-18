"""Chiang Mai Tea Ingredients Deck (Max asked Oct 18 2026 22:44 ICT; brief from WellNest).
Usage: python3 tools/build_tea_ingredients_1018.py [--pages-only]   (from the repo root).
Same page kit as the Oct 18 night decks (md1018_kit.page from index.template.html, cream background like build_machan_1018.py),
but single cards (deck.cards) with a Like / Pass page block: Hold and Love hidden, Notes kept, Share in the footer.
One card per ingredient, no pick cap (Max approved the exception). Results route to WellNest (submit_agent wellnest)."""
import datetime, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import page, EMOJI
import tea_ingredients_1018 as TI
DID = "wellnest-chiang-mai-tea-ingredients-deck"; NAME = "Chiang Mai Tea Ingredients Deck"; SLUG = "chiang-mai-tea-ingredients"
WN = dict(submit_agent="wellnest", submit_to="WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35")
REQ = "Oct 18 2026 22:44 ICT: Max asked for one Like/Pass swipe card per Chiang Mai tea ingredient (brief from WellNest); no pick cap"
START, END = "<!--mw-likepass-->", "<!--/mw-likepass-->"
LP = START + r"""
<style id="mw-likepass-css">
body.mw-lp #bMaybe,body.mw-lp #bLove,body.mw-lp .stamp.maybe,body.mw-lp .stamp.love{display:none!important}
body.mw-lp #bNo{background:#FFFFFF;color:#9B2C1F;border-color:#9B2C1F}
body.mw-lp #bYes{background:#0B6E4F;color:#FFFFFF;border-color:#0B6E4F}
body.mw-lp .opt .tags .tag{background:#E3F1EA;color:#0B6E4F;border-color:#BFDCCB;font-weight:600}
body.mw-lp.carding .opt .tags{display:flex!important;flex-wrap:wrap;gap:4px;margin-top:2px}
body.mw-lp.carding .opt .tags:empty{display:none!important}
body.mw-lp #controls3{flex-wrap:wrap!important;align-items:stretch}
body.mw-lp.carding .opts.single .opt h3{font-size:22px!important;line-height:1.15}
body.mw-lp.carding .opts.single .opt p{font-size:15px!important;display:block!important}
body.mw-lp #controls3>button{flex:1 1 0!important;min-width:0!important}
body.mw-lp #controls3>#bNo,body.mw-lp #controls3>#bYes{flex:2 1 0!important}
body.mw-lp #controls3>#bU3{flex:0 0 52px!important}
</style>
<script>(()=>{
/* Like / Pass single cards (deck.like_pass): Pass left, Like right; Hold and Love hidden; notes saved with the vote */
const lp=()=>{try{return !!(deck&&single&&deck.like_pass)}catch(e){return false}};
function lpUi(){const on=lp();document.body.classList.toggle('mw-lp',on);if(!on)return;
 const n=document.getElementById('bNo'),y=document.getElementById('bYes');if(n)n.textContent='Pass';if(y)y.textContent='Like';
 try{LBL.no='Pass';LBL.yes='Like'}catch(e){}
 const h=document.querySelector('#card h2');if(h)h.textContent='Like Or Pass?';
 const s=document.querySelector('#card .stamp.yes');if(s)s.textContent='LIKE';
 const hi=document.getElementById('hint');if(hi&&document.body.classList.contains('carding'))hi.textContent='Swipe left = Pass, right = Like. Arrow keys: \u2190 Pass, \u2192 Like. Notes are optional.';
 const e=document.querySelector('#main .end');if(e&&!e.dataset.lp){e.dataset.lp=1;const t=(totals=>totals)(buildResults().totals);
  const h2=e.querySelector('h2');if(h2)h2.textContent='Your Picks';
  const st=e.querySelector('.stats');if(st)st.innerHTML=`<div class="stat"><b style="color:#0B6E4F">${t.yes||0}</b><span>Like</span></div><div class="stat"><b style="color:#A4161A">${t.no||0}</b><span>Pass</span></div>`;
  e.querySelectorAll('.catlist .ans.yes').forEach(a=>a.textContent='LIKE');
  e.querySelectorAll('h3').forEach(x=>{if(/^Tags You /.test(x.textContent)){x.style.display='none';const b=x.nextElementSibling;if(b)b.style.display='none'}});
  e.querySelectorAll('.notes-list .nt').forEach(x=>x.innerHTML=x.innerHTML.replace(/ · yes</,' · Like<').replace(/ · no</,' · Pass<'))}}
window.addEventListener('keydown',e=>{if(!lp())return;const k=e.key;if(k==='m'||k==='l'||k==='ArrowUp'||k==='ArrowDown'){if(e.target&&(e.target.tagName==='TEXTAREA'||e.target.tagName==='SELECT'))return;e.stopImmediatePropagation()}},true);
try{const _sd=setDeck;setDeck=function(){const x=_sd.apply(this,arguments);try{lpUi()}catch(e){}return x}}catch(e){}
try{const _r=render;render=function(){const x=_r.apply(this,arguments);try{lpUi()}catch(e){}return x}}catch(e){}
try{const _se=showEnd;showEnd=function(){const x=_se.apply(this,arguments);try{lpUi()}catch(e){}return x}}catch(e){}
try{const _ss=shareSummary;shareSummary=function(){if(!lp())return _ss.apply(this,arguments);if(!picks.length)return 'Try this deck: Like or Pass.';
 const r=buildResults(),t=r.totals||{},liked=picks.filter(p=>p.answer==='yes').map(p=>p.label).slice(0,8).join(', ');
 return `My picks (${deck.title||deck.date}, ${r.answered}/${items.length}): ${t.yes||0} Like, ${t.no||0} Pass.`+(liked?` Liked: ${liked}.`:'')+((r.notes||[]).length?` Notes: ${r.notes.map(n=>`[${n.label}] ${n.note}`).join(' | ').slice(0,600)}`:'')}}catch(e){}
try{const _sr=submitResults;submitResults=function(){const r=_sr.apply(this,arguments);try{if(lp()&&r){r.mode='like-pass';
 const lab=id=>{const c=items.find(i=>i.id===id);return c?c.option.label:id};const nt=id=>{try{return noteOf(id)||undefined}catch(e){return undefined}};
 r.like=picks.filter(p=>p.answer==='yes').map(p=>({card:lab(p.card_id),note:nt(p.card_id)}));
 r.pass=picks.filter(p=>p.answer==='no').map(p=>({card:lab(p.card_id),note:nt(p.card_id)}))}}catch(e){}return r}}catch(e){}
})();</script>
""" + END
def finish_page(slug):
    """Deck title, light cream background (same as build_machan_1018.finish_page), standard footer kept, Like/Pass block."""
    pg = os.path.join(slug, "index.html"); h = open(pg).read()
    if "const D=" in h: return
    h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
    h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
    assert '<a class="builtby' in h and 'id="shareBtn"' in h and "<!--/mw-r116-->" in h, "standard footer, Share button, r116 block"
    h = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", h, flags=re.S)
    i = h.rindex("</body>"); h = h[:i] + LP + "\n" + h[i:]
    open(pg, "w").write(h)
def build():
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    cards = []
    for i, (cat, nm, note, col, star) in enumerate(TI.ING, 1):
        oid = "cmtea18_" + re.sub(r"[^a-z0-9]+", "_", nm.lower()).strip("_")
        cards.append({"id": f"{DID}-{i:02d}", "category": cat, "group": cat, "app": "WellNest", "notes": True, "share": True,
                      "in_our_teas": star,
                      "option": {"id": oid, "label": nm, "desc": note, "tags": ["In our teas"] if star else [], "feeling": "calm",
                                 "notes": True, "share": True, "visual": {"type": "hm", "m": "svg", "svg": TI.svg(cat, col, star)}}})
    d = {"date": DID, "version": 3, "owner": "Max Weberman", "format": "single", "like_pass": True, "english_only": True, "light_only": True,
         "title": NAME, "name": NAME, "generated_at": now, "status": "published", "cards": cards, "deck_size": len(cards), "no_cap": True,
         "cap_note": "Max approved an exception to the 10-pick cap: one card per ingredient", "share": True, "notes": True,
         **WN, "row": "nozomi", "project": "Chiang Mai Tea Ingredients", "requested": True, "request": REQ, "log_only": True,
         "groups": {}, "apps": {"WellNest": len(cards)}, "built_by": "Branding", "built_at_note": "Oct 18 2026 22:44 ICT request",
         "brands": ["Chiang Mai tea ingredients for WellNest teas; In our teas = already in a WellNest tea", "Drawn colour swatches only, no photos, no people"],
         "sources": {"content": "tools/tea_ingredients_1018.py", "builder": "tools/build_tea_ingredients_1018.py"}}
    for c in cards: d["groups"][c["category"]] = d["groups"].get(c["category"], 0) + 1
    assert not EMOJI.search(json.dumps(d, ensure_ascii=False)), "emoji"
    json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    so = json.load(open("shown_options.json"))
    for c in cards: so["options"].setdefault(c["option"]["id"], []).append(DID)
    so["shown_count"] = so.get("shown_count", 0) + len(cards); so["updated"] = now
    json.dump(so, open("shown_options.json", "w"), indent=1, ensure_ascii=False)
    from write_sizes import main as write_sizes; write_sizes()
    return len(cards)
if __name__ == "__main__":
    n = None if "--pages-only" in sys.argv else build()
    slug, url = page(DID, SLUG); finish_page(slug)
    print(DID, slug, url, n)
