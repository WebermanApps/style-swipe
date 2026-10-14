"""usage: shot_page.py <slug>  -> shots/fit/<slug>-393x852.png, -1470x956.png, plus card dump of all pairs at 393"""
import sys
from playwright.sync_api import sync_playwright
slug = sys.argv[1]; base = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:18793/"
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(393, 852), (1470, 956)]:
        pg = b.new_page(viewport={"width": w, "height": h}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(base + slug + "/"); pg.wait_for_timeout(1500)
        pg.screenshot(path=f"shots/fit/{slug}-{w}x{h}.png")
        info = pg.evaluate("()=>({sh:document.scrollingElement.scrollHeight,sw:document.scrollingElement.scrollWidth,title:document.title,txt:document.body.innerText.slice(0,400)})")
        print(w, info, errs)
    b.close()
