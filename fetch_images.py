"""Fetch freely-licensed images from Wikimedia Commons into img/ with credits.json."""
import json, os, re, urllib.request, urllib.parse
UA = {"User-Agent": "StyleSwipe/1.0 (personal project; max)"}
Q = {
 "int_scandi": "Scandinavian interior living room",
 "int_japandi": "Japanese minimalist interior wood",
 "int_midcentury": "mid-century modern living room",
 "int_industrial": "industrial loft interior brick",
 "int_mediterranean": "Mediterranean house interior",
 "int_tropical": "tropical modern villa pool",
 "int_farmhouse": "farmhouse kitchen interior",
 "int_concrete": "exposed concrete interior architecture",
 "int_thai": "traditional Thai house teak",
 "int_boho": "bohemian interior plants",
 "int_artdeco": "Art Deco interior",
 "int_modernkitchen": "modern kitchen interior white",
 "int_cabin": "log cabin interior",
 "int_coastal": "beach house interior",
 "ext_modern": "modern house exterior architecture",
 "ext_craftsman": "craftsman bungalow house",
 "ext_spanish": "Spanish colonial revival house",
 "ext_tropical": "Bali villa architecture",
 "base_street": "Bangkok street market",
 "base_site": "construction site building workers",
 "base_temple": "Wat Arun Bangkok",
}
API = "https://commons.wikimedia.org/w/api.php?"
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
credits = {}
os.makedirs("img", exist_ok=True)
for key, q in Q.items():
    params = dict(action="query", format="json", generator="search", gsrsearch=f"{q} filetype:bitmap",
                  gsrnamespace=6, gsrlimit=8, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=720)
    try:
        data = json.loads(get(API + urllib.parse.urlencode(params)))
        pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        ok = False
        for p in pages:
            ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
            lic = md.get("LicenseShortName", {}).get("value", "")
            if ii.get("width", 0) < 600 or ii.get("width",0) < ii.get("height",0): continue
            if not re.search(r"CC|Public domain|PD", lic, re.I): continue
            raw = get(ii["thumburl"])
            fn = f"img/{key}.jpg"; open(fn, "wb").write(raw)
            artist = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
            credits[key] = {"file": fn, "title": p["title"], "license": lic, "artist": artist, "source": ii["descriptionurl"]}
            print("OK", key, p["title"], lic); ok = True; break
        if not ok: print("MISS", key)
    except Exception as e:
        print("ERR", key, e)
json.dump(credits, open("img/credits.json", "w"), indent=1)
