"""usage: crisp_shots.py <tag> [slug...] -> shots/crisp/<tag>/<slug>-<w>x<h>@2x.png; prints scroll/overflow + min rendered SVG text px"""
import sys, os, json
from playwright.sync_api import sync_playwright
tag = sys.argv[1]; slugs = sys.argv[2:]; base = os.environ.get("BASE", "http://127.0.0.1:18794/")
out = f"shots/crisp/{tag}"; os.makedirs(out, exist_ok=True)
JS = """()=>{const se=document.scrollingElement;let mn=99,svgs=0,over=0;
document.querySelectorAll('.card:not([style*="opacity: 0"]) .v-svg svg').forEach(s=>{svgs++;const r=s.getBoundingClientRect(),vb=s.viewBox.baseVal;const k=r.width/(vb.width||r.width);
 s.querySelectorAll('text').forEach(t=>{let f=parseFloat(t.getAttribute('font-size')||'0');let p=t.parentElement,m=1;while(p&&p!==s){const tr=p.getAttribute&&p.getAttribute('transform');const mm=tr&&tr.match(/scale\\(([\\d.]+)/);if(mm)m*=parseFloat(mm[1]);p=p.parentElement}
 if(f)mn=Math.min(mn,f*m*k)})});
document.querySelectorAll('.opt').forEach(o=>{if(o.scrollHeight>o.clientHeight+2)over++});
return {sh:se.scrollHeight,ch:se.clientHeight,sw:se.scrollWidth,cw:se.clientWidth,svgs,minTextPx:+mn.toFixed(1),optOverflow:over}}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for slug in slugs:
        for w, h in [(393, 852), (1470, 956), (2560, 1440)]:
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(base + slug + "/"); pg.wait_for_timeout(1800)
            pg.screenshot(path=f"{out}/{slug}-{w}x{h}@2x.png")
            print(slug, w, json.dumps(pg.evaluate(JS)), errs[:2], flush=True); pg.close()
    b.close()
