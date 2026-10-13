"""Style Swipe fit check: every deck's first card must fit one iPhone screen (WebKit, iPhone UA).
usage: python3 tools/fit_check.py [BASE_URL] [OUTDIR]"""
import json, glob, os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18793/"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "shots/fit")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
SIZES = [(393, 660), (393, 852)]
decks = []
for f in sorted(glob.glob(os.path.join(ROOT, "decks/*.json"))):
    d = os.path.basename(f)[:-5]
    if d == "submit-test": continue
    j = json.load(open(f)); decks.append((d, j))
# the 2 pair decks with the longest labels: also test their longest-label pair
def lablen(p): return max(len(p["optionA"].get("label", "")), len(p["optionB"].get("label", "")))
pairdecks = [(max(lablen(p) for p in j["pairs"]), d, max(range(len(j["pairs"])), key=lambda i: lablen(j["pairs"][i]))) for d, j in decks if j.get("pairs")]
longest = sorted(pairdecks, reverse=True)[:2]
SAMPLES = {"2026-10-13", "flat-fee-and-lagoon", "upkeep-7", "video-v2", longest[0][1], longest[1][1]}
JS = """() => {
 const H = innerHeight, W = innerWidth, bad = [];
 const inside = (el, name) => { if (!el) { bad.push(name + ': missing'); return }
   const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return;
   for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const cs = getComputedStyle(a);
     if (cs.overflowY !== 'visible' || cs.overflowX !== 'visible') { const q = a.getBoundingClientRect();
       if (r.top < q.top - 1 || r.bottom > q.bottom + 1 || r.left < q.left - 1 || r.right > q.right + 1) { bad.push(`${name} clipped by ${a.className || a.tagName}`); break } } }
   if (r.top < -0.5 || r.left < -0.5 || r.bottom > H + 0.5 || r.right > W + 0.5) bad.push(`${name} out [${r.left|0},${r.top|0},${r.right|0},${r.bottom|0}]`) };
 const se = document.scrollingElement;
 if (se.scrollHeight > H + 1) bad.push(`scrollHeight ${se.scrollHeight} > ${H}`);
 const ctl = [...document.querySelectorAll('.controls')].find(c => getComputedStyle(c).display !== 'none');
 if (!ctl) bad.push('no controls'); else ctl.querySelectorAll('button').forEach(b => inside(b, 'btn ' + b.textContent.trim()));
 const card = document.getElementById('card'); if (!card) bad.push('no card');
 inside(card, 'card');
 if (card && card.scrollHeight > card.clientHeight + 1) bad.push(`card overflows ${card.scrollHeight}>${card.clientHeight}`);
 document.querySelectorAll('#card .opt').forEach((o, i) => { if (o.scrollHeight > o.clientHeight + 1) bad.push(`opt${i} overflows ${o.scrollHeight}>${o.clientHeight}`) });
 document.querySelectorAll('#card .opt .vis').forEach((v, i) => { if (v.getBoundingClientRect().height < 90) bad.push(`vis${i} too small ${v.getBoundingClientRect().height|0}px`) });
 document.querySelectorAll('#card .opt h3').forEach((h, i) => inside(h, 'label' + i));
 document.querySelectorAll('#card .opt .vis').forEach((h, i) => inside(h, 'vis' + i));
 inside(document.querySelector('#card .notebtn'), 'notes');
 inside(document.querySelector('.progress'), 'progress');
 return bad }"""
res = []
with sync_playwright() as p:
    br = p.webkit.launch()
    for W, H in SIZES:
        ctx = br.new_context(viewport={"width": W, "height": H}, user_agent=UA, is_mobile=True, has_touch=True, device_scale_factor=2)
        jobs = [(d, None) for d, _ in decks] + [(d, i) for _, d, i in longest]
        for d, i in jobs:
            pg = ctx.new_page()
            if i is not None: pg.add_init_script(f"localStorage.setItem('__fitidx','{i}')")
            pg.goto(f"{BASE}?date={d}", wait_until="load")
            try: pg.wait_for_selector("#card", state="attached", timeout=15000)
            except Exception:
                res.append((W, H, d, ["card never rendered: " + pg.evaluate("()=>document.getElementById('sub').textContent")])); pg.close(); continue
            if i is not None:
                pg.evaluate(f"()=>{{idx={i};render()}}")
            pg.wait_for_timeout(700)
            bad = pg.evaluate(JS)
            tag = d + ("" if i is None else f"-longest{i+1}")
            res.append((W, H, tag, bad))
            if d in SAMPLES or bad or i is not None: pg.screenshot(path=os.path.join(OUT, f"fit-{W}x{H}-{tag}.png"))
            pg.close()
        ctx.close()
    br.close()
ok = [r for r in res if not r[3]]
lines = [f"Style Swipe fit check · base {BASE}", f"{len(ok)}/{len(res)} passed ({len(decks)} decks x {len(SIZES)} sizes + longest-label pairs {[(d,i+1) for _,d,i in longest]})", ""]
lines += [f"{'PASS' if not b else 'FAIL'} {w}x{h} {t}" + ("" if not b else "  " + "; ".join(b)) for w, h, t, b in res]
open(os.path.join(OUT, "summary.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(l for l in lines if not l.startswith("PASS")))
