#!/usr/bin/env python3
"""Household refresh (Branding, Oct 17 2026): photos for the Household board decks.
Real place and dish photos from Wikimedia Commons (free licences only: CC0 / PD / CC BY / CC BY-SA), picked by hand per option
(queue/household-refresh-photos.json: key -> exact Commons file title), saved as 640px WebP in img/household/ with credits in
img/household/credits.json (title, author, licence, licence url, source page). Idempotent: existing files are kept."""
import json, os, re, html, io, urllib.request, urllib.parse
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UA = {"User-Agent": "StyleSwipe/1.0 (maxweberman.com; household decks)"}
OK = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [1-4]\.[05])", re.I)
D = "img/household"; CR = D + "/credits.json"
def api(**p):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**p, "format": "json"})
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
def fetch(key, title, cred):
    f = f"{D}/{key}.webp"
    if key in cred and os.path.exists(f): return cred[key]
    d = api(action="query", titles=title, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=640)
    p = next(iter(d["query"]["pages"].values())); ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
    lic = (m.get("LicenseShortName") or {}).get("value", ""); assert OK.match(lic), (title, lic)
    raw = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=90).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((640, 640)); im.save(f, "WEBP", quality=76, method=6)
    art = html.unescape(re.sub(r"<[^>]+>", "", (m.get("Artist") or {}).get("value", ""))).strip() or "Unknown"
    cred[key] = {"file": f, "w": im.width, "h": im.height, "title": title, "author": art[:80], "license": lic,
                 "license_url": (m.get("LicenseUrl") or {}).get("value", ""), "source": ii["descriptionurl"]}
    return cred[key]
def all_photos():
    os.makedirs(D, exist_ok=True); cred = json.load(open(CR)) if os.path.exists(CR) else {}
    for k, t in json.load(open("queue/household-refresh-photos.json")).items(): fetch(k, t, cred)
    json.dump(cred, open(CR, "w"), indent=1, ensure_ascii=False); return cred
if __name__ == "__main__":
    c = all_photos(); print(len(c), "photos;", sum(os.path.getsize(v["file"]) for v in c.values()) // 1024, "KB")
