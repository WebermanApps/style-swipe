#!/usr/bin/env python3
"""Art Deck (Household board): downloads real CC0 artworks from the Art Institute of Chicago API into img/art/ (credits in img/art/credits.json),
then publishes a 20-pair image deck with the same page pattern as build_household.py (white, beige accents, Khand/Hind, Notes + Share)."""
import sys, os, json, re, string, secrets, urllib.request, html
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck as kdeck, publish
from agent_links import patch as link_patch
from art_content import NAME, PAIRS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UA = {"User-Agent": "StyleSwipe/1.0 (maxweberman.com)", "AIC-User-Agent": "StyleSwipe (maxweberman.com)"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
os.makedirs("img/art", exist_ok=True); CR = "img/art/credits.json"; cred = json.load(open(CR)) if os.path.exists(CR) else {}
def fetch(aid):
    k = f"aic_{aid}"
    if k in cred and os.path.exists(cred[k]["file"]): return cred[k]
    d = json.loads(get(f"https://api.artic.edu/api/v1/artworks/{aid}?fields=id,title,artist_title,artist_display,date_display,medium_display,image_id,is_public_domain,thumbnail"))["data"]
    assert d["is_public_domain"] and d["image_id"], aid
    f = f"img/art/{k}.jpg"; open(f, "wb").write(get(f"https://www.artic.edu/iiif/2/{d['image_id']}/full/843,/0/default.jpg"))
    from PIL import Image; w, h = Image.open(f).size
    cred[k] = {"file": f, "w": w, "h": h, "title": d["title"], "artist": d["artist_title"] or (d["artist_display"] or "").split("\n")[0], "date": d["date_display"],
               "medium": d["medium_display"], "license": "CC0 (Art Institute of Chicago Open Access, public domain)", "source": f"https://www.artic.edu/artworks/{aid}"}
    json.dump(cred, open(CR, "w"), indent=1, ensure_ascii=False); return cred[k]
E2 = html.escape
def svg(c, label):
    W, H = 240, 300; bw, bh = 224, 222; s = c["w"] / c["h"]
    iw, ih = (bw, bw / s) if s > bw / bh else (bh * s, bh); x, y = 8 + (bw - iw) / 2, 8 + (bh - ih) / 2
    t = lambda x, y, txt, sz, col, fam, wt=600: f'<text x="{x}" y="{y}" font-size="{sz}" fill="{col}" text-anchor="middle" font-family="{fam}, sans-serif" font-weight="{wt}">{E2(txt)}</text>'
    by = (c["artist"] or "Unknown") + (", " + c["date"] if c["date"] else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">'
            f'<rect width="{W}" height="{H}" fill="#FFFFFF"/><rect x="8" y="8" width="{bw}" height="{bh}" rx="8" fill="#FAF6EE" stroke="#E3DDD2"/>'
            f'<image href="{c["file"]}" xlink:href="{c["file"]}" x="{x:.1f}" y="{y:.1f}" width="{iw:.1f}" height="{ih:.1f}" preserveAspectRatio="xMidYMid meet"/>'
            + t(120, 252, label[:34], 15, "#0A0A0A", "Khand") + t(120, 268, by[:46], 9.5, "#525252", "Hind", 500)
            + t(120, 286, "Art Institute of Chicago, CC0  ·  Built by Max Weberman", 7.5, "#8A8580", "Hind", 400)
            + f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
if __name__ == "__main__":
    did = "household-art-deck"; SL = "queue/household-slugs.json"; slugs = json.load(open(SL))
    pairs, O, add = kdeck("hhart_", "Household"); FEEL = ["classic", "bold", "calm", "playful", "premium"]
    for gi, (g, ask, ia, la, ib, lb) in enumerate(PAIRS):
        opts = []
        for side, (aid, lab) in enumerate(((ia, la), (ib, lb))):
            c = fetch(aid); desc = f'{c["artist"] or "Unknown"}, {c["date"]}. {c["medium"] or ""}'.strip()
            o = O(f"aic{aid}", lab, desc[:120], FEEL[(gi + side) % 5], svg(c, lab), tags=["art", g.lower()])
            o["credit"] = {k: c[k] for k in ("title", "artist", "date", "license", "source")}; opts.append(o)
        add(g, g, opts[0], opts[1], ask)
    publish(did, NAME, "Household", pairs, {"brands": ["Permanent deck of real public-domain artworks across painting, photography, sculpture, illustration, prints, styles and eras", "Images: Art Institute of Chicago Open Access (CC0); credits in img/art/credits.json"],
            "submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d",
            "deck_size": 20, "board": "household", "permanent": True, "audience": "Max and Nozomi"}, seed=5300, n=20)
    assert len(json.load(open(f"decks/{did}.json"))["pairs"]) == 20
    if did not in slugs: slugs[did] = "household-art-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[did]; HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}</style>\n'
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)); link_patch(p)
    pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"deckId": did, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
