import json,sys
from playwright.sync_api import sync_playwright
d=json.load(open(f"decks/{sys.argv[1]}.json"))
h="<html><body style='margin:0;background:#eee;display:flex;flex-wrap:wrap;gap:4px'>"+"".join(f"<div style='width:240px'>{p[o]['visual']['svg']}<div style='font:9px sans-serif'>{i+1}{o[-1]} {p[o]['label']}</div></div>" for i,p in enumerate(d['pairs']) for o in ('optionA','optionB'))+"</body></html>"
open("/tmp/c.html","w").write(h.replace('href="img/','href="file:///workspace/style-swipe/img/'))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1990,"height":800});pg.goto("file:///tmp/c.html");pg.wait_for_timeout(800);pg.screenshot(path=f"/tmp/{sys.argv[1]}-contact.png",full_page=True);b.close()
