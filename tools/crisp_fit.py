#!/usr/bin/env python3
"""Crisp pass step 2 (Oct 14 2026): after crisp_decks.py raised mockup text, render every SVG in Chromium (page fonts loaded) and
step any raised label back down (never below its original size) until it no longer collides with other text, leaves a box it sat in,
or leaves the screen. usage: crisp_fit.py <orig_decks_dir> <deck_id> [...]   (needs a local server on 18793 serving this repo)"""
import json, os, re, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ORIG = sys.argv[1]
FS = re.compile(r'(<text\b[^>]*?font-size=")([\d.]+)(")')
JS = r"""([o,n])=>{const h=document.getElementById('cfit');
const mk=s=>{const d=document.createElement('div');d.style.cssText='width:960px;position:absolute;left:0;top:0';d.innerHTML=s;h.appendChild(d);const v=d.querySelector('svg');v.setAttribute('width','960');v.removeAttribute('height');v.style.cssText='width:960px;height:auto';return v};
const so=mk(o),sn=mk(n);const T0=[...so.querySelectorAll('text')],T1=[...sn.querySelectorAll('text')];if(T0.length!==T1.length)return null;
const R0=[...so.querySelectorAll('rect')].map(r=>r.getBoundingClientRect()),R1=[...sn.querySelectorAll('rect')].map(r=>r.getBoundingClientRect());
const bb=t=>t.getBoundingClientRect(),X=(a,b,p=1)=>a.width&&b.width&&a.left<b.right-p&&b.left<a.right-p&&a.top<b.bottom-p&&b.top<a.bottom-p;
const inside=(a,r,p=.5)=>a.left>=r.left-p&&a.right<=r.right+p&&a.top>=r.top-p&&a.bottom<=r.bottom+p;
const B0=T0.map(bb),svr=sn.getBoundingClientRect();
const boxes=B0.map(b=>R0.map((r,j)=>r.width<svr.width*.95&&inside(b,r)?j:-1).filter(j=>j>=0));
const bad=i=>{const b=bb(T1[i]);if(!b.width)return false;if(b.left<svr.left-1||b.right>svr.right+1)return true;
 for(let j=0;j<T1.length;j++){if(j===i)continue;if(X(b,bb(T1[j]))&&!X(B0[i],B0[j]))return true}
 for(const j of boxes[i])if(!inside(b,R1[j],2))return true;return false};
const out=[];for(let pass=0;pass<3;pass++)for(let i=0;i<T1.length;i++){const s0=parseFloat(T0[i].getAttribute('font-size')),s=parseFloat(T1[i].getAttribute('font-size'));
 if(!(s>s0))continue;let c=s;while(c>s0&&bad(i)){c=Math.max(s0,+(c-.25).toFixed(2));T1[i].setAttribute('font-size',c)}}
const res=T1.map(t=>t.getAttribute('font-size'));h.innerHTML='';return res}"""
def walk(o, oo, f):
    if isinstance(o, dict): return {k: walk(v, oo.get(k) if isinstance(oo, dict) else None, f) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, oo[i] if isinstance(oo, list) and i < len(oo) else None, f) for i, v in enumerate(o)]
    if isinstance(o, str) and o.lstrip().startswith("<svg") and isinstance(oo, str) and oo != o: return f(oo, o)
    return o
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("http://127.0.0.1:18793/agent-dashboards-ndeqtp/"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.createElement('div');d.id='cfit';d.style.cssText='position:fixed;left:-5000px;top:0';document.body.appendChild(d);return document.fonts.ready.then(()=>1)}")
    for did in sys.argv[2:]:
        pth = os.path.join(ROOT, "decks", did + ".json"); raw = open(pth).read(); d = json.loads(raw); od = json.load(open(os.path.join(ORIG, did + ".json")))
        st = {"svg": 0, "stepped": 0}
        def fit(o, n):
            sizes = pg.evaluate(JS, [o, n]); st["svg"] += 1
            if sizes is None: return n
            it = iter(sizes); cur = [m.group(2) for m in FS.finditer(n)]
            if len(cur) != len(sizes): return n
            st["stepped"] += sum(1 for a, c in zip(cur, sizes) if c is not None and float(a) != float(c))
            return FS.sub(lambda m: m.group(1) + f"{float(next(it) or m.group(2)):g}" + m.group(3), n)
        nd = walk(d, od, fit)
        ln = raw.split("\n")[1] if "\n" in raw.strip() else ""; ind = (len(ln) - len(ln.lstrip(" "))) if ln else None
        open(pth, "w").write(json.dumps(nd, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else "")); print(did, st, flush=True)
    b.close()
