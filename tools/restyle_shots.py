"""usage: restyle_shots.py <tag> [base]  -> shots/restyle/<tag>-<page>-393x852.png (+ fit check at 393x660, 1470, 2560)"""
import sys
from playwright.sync_api import sync_playwright
tag = sys.argv[1]; base = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:18793/"
PAGES = ["folio-dashboard-kuijvp", "upkeep-board-vh7w9l", "deck-board-h0dwt3", "wellnest-brand-r2-qlpkxs3t"]
with sync_playwright() as p:
    b = p.chromium.launch()
    for pg_ in PAGES:
        for w, h in [(393, 852), (393, 660), (1470, 956), (2560, 1440)]:
            pg = b.new_page(viewport={"width": w, "height": h}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(base + pg_ + "/", wait_until="domcontentloaded"); pg.wait_for_timeout(1200)
            if (w, h) == (393, 852): pg.screenshot(path=f"shots/restyle/{tag}-{pg_}-393x852.png")
            r = pg.evaluate("()=>{const se=document.scrollingElement;const c=document.querySelector('.controls');const cr=c?c.getBoundingClientRect():null;return [se.scrollHeight,se.scrollWidth,getComputedStyle(document.body).backgroundColor,cr?Math.round(cr.bottom):null]}")
            ok = r[0] <= h + 1 and r[1] <= w + 1 and (r[3] is None or r[3] <= h + 1)
            print(tag, pg_, f"{w}x{h}", "FIT" if ok else "OVERFLOW", r, errs[:1])
    b.close()
