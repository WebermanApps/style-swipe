"""Mix mode + missing-deck fallback check. usage: python3 tools/mix_check.py [BASE] [OUTDIR]"""
import sys, os
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18793/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "shots/fit"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
ok = True
with sync_playwright() as p:
    b = p.webkit.launch()
    for H in (852, 660):
        c = b.new_context(viewport={"width": 393, "height": H}, user_agent=UA, is_mobile=True, has_touch=True, device_scale_factor=2)
        pg = c.new_page(); pg.goto(BASE + "?mix=upkeep,thai&n=25"); pg.wait_for_selector("#card", state="attached", timeout=15000); pg.wait_for_timeout(700)
        r = pg.evaluate("""()=>{const banks={};items.forEach(p=>banks[p.bank]=(banks[p.bank]||0)+1);
          const f=document.querySelector('footer');const vis=el=>el&&el.getClientRects().length>0&&getComputedStyle(el).display!=='none';
          return {id:deck.date,name:deck.name,sub:document.getElementById('sub').textContent,n:items.length,banks,
            footer:vis(f),byline:[...document.querySelectorAll('body *')].filter(e=>vis(e)&&/upkeep/i.test(e.childNodes.length===1&&e.firstChild.nodeType===3?e.textContent:'')&&/by/i.test(e.textContent)).map(e=>e.textContent.trim()).slice(0,3),
            scroll:document.scrollingElement.scrollHeight,ih:innerHeight}}""")
        print(H, r)
        good = r["n"] == 25 and set(r["banks"]) == {"upkeep", "thai"} and abs(r["banks"]["upkeep"] - r["banks"]["thai"]) <= 1 and not r["footer"] and not r["byline"] and r["scroll"] <= r["ih"] + 1 and r["name"].startswith("Mixed Deck:")
        ok &= good; pg.screenshot(path=os.path.join(OUT, f"mix-393x{H}-upkeep-thai.png"))
        c.close()
    c = b.new_context(viewport={"width": 393, "height": 852}, user_agent=UA, is_mobile=True)
    pg = c.new_page(); pg.goto(BASE + "?date=upkeep-99"); pg.wait_for_timeout(2500)
    t = pg.evaluate("document.getElementById('main').innerText"); g = "Play From Bank" in t; print("fallback:", g, t[:160].replace("\n", " | ")); ok &= g
    pg.screenshot(path=os.path.join(OUT, "missing-deck-fallback-393x852.png"))
    b.close()
print("MIX CHECK", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
