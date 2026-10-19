"""Art Taste Deck (Max Oct 19 2026 10:58 PM ICT, directly: 'show me a swipe deck with art. lets start to figure out what kind of art i like.').
20 this-or-that pairs of REAL artworks (tools/art_taste_content.py), open-access / public-domain / freely licensed images only, resized to
<=1200px and stored next to the page (<slug>/img/), credits in <slug>/credits.json and on every card. Page: tools/art_taste_page.py
(Max deck style). Team-gated submit via ../submit.js as agent 'branding'.
Usage (repo root): python3 tools/build_art_taste_1019.py <img_dir> <lic.json>"""
import json, os, re, sys, shutil, secrets, string, datetime
sys.path.insert(0, os.path.dirname(__file__))
import art_taste_content as C, art_taste_page as PG
DID, NAME = "branding-art-taste-deck", "Art Taste Deck"
TO = "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78"
NUMW = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty)\b|\d", re.I)
BAD = re.compile(r"cannabis|hemp|marijuana|weed|buddha|temple|shrine|altar", re.I)
US_ONLY = {"hopper", "okeeffe"}  # public domain in the US (published before 1931); artist died less than 70 years ago
NOTE = {"livia": "cropped to remove the museum rail", "zacharevic": "photo of a public mural; mural by Ernest Zacharevic",
        "benjarong": "museum photo", "dolphins": "museum photo", "adams": "US federal government work (Mural Project, 1941-42)"}
def main(img_dir, lic_path):
    L = json.load(open(lic_path)); assert not NUMW.search(NAME)
    pages = json.load(open("decks/pages.json"))
    slug = pages.get(DID) or "art-taste-deck-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    os.makedirs(f"{slug}/img", exist_ok=True); art = {}; credits = []
    for k, x in C.W.items():
        l = L[k]; shutil.copyfile(os.path.join(img_dir, k + ".jpg"), f"{slug}/img/{k}.jpg")
        lic = l["license"]
        if lic == "Public domain": lic = "Public domain in the US" if k in US_ONLY else "Public domain"
        if lic.startswith("CC BY"): lic += ", photo " + l["photo_credit"].split(" · ")[0]
        from PIL import Image
        w, h = Image.open(f"{slug}/img/{k}.jpg").size
        art[k] = dict(x, w=w, h=h, source=l["source"], source_name="Wikimedia Commons", license=lic)
        credits.append({"key": k, "file": f"img/{k}.jpg", "title": x["title"], "artist": x["artist"], "year": x["year"], "holder": x["holder"],
                        "source_url": l["source"], "license": lic, "license_url": l.get("license_url") or "https://commons.wikimedia.org/wiki/Commons:Reusing_PD_files",
                        "commons_credit": l["photo_credit"], "downloaded_from": l["image"], "note": NOTE.get(k, ""), "size": [w, h], "bytes": os.path.getsize(f"{slug}/img/{k}.jpg")})
    pairs = []
    for i, (cat, q, a, b) in enumerate(C.PAIRS, 1):
        mk = lambda key, s: {"id": f"{DID}_{i:02d}{s}_{key}", "art": key, "label": C.W[key]["title"], "artist": C.W[key]["artist"], "year": C.W[key]["year"],
                             "desc": C.W[key]["what"], "tags": C.W[key]["tags"], "image": f"{slug}/img/{key}.jpg"}
        pairs.append({"id": f"{DID}-{i:02d}", "group": cat, "category": cat, "ask": q, "notes": True, "share": True, "optionA": mk(a, "a"), "optionB": mk(b, "b")})
    blob = json.dumps(pairs, ensure_ascii=False); assert not BAD.search(blob), BAD.search(blob)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(timespec="seconds")
    dj = {"date": DID, "version": 1, "format": "pairs", "kind": "art-taste", "english_only": False, "light_only": True, "title": NAME,
          "generated_at": now, "status": "published", "submit_agent": "branding", "submit_to": TO, "board": "branding-djqmb410", "audience": "Max",
          "requested": True, "request": "Max Oct 19 2026 10:58 PM ICT: 'show me a swipe deck with art. lets start to figure out what kind of art i like.'",
          "deck_size": len(pairs), "built_by": "Branding (Swatch)", "deck_style": "max-deck (dadbook layout in Max's brand)", "page": slug + "/",
          "real_art_only": True, "results_tags": "each option carries tags [style, era, mood]; results carry artA / artB with the same fields",
          "credits": slug + "/credits.json", "sources": {"builder": "tools/build_art_taste_1019.py", "content": "tools/art_taste_content.py", "page": "tools/art_taste_page.py"},
          "notes": True, "share": True, "pairs": pairs}
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    json.dump({"deck": DID, "title": NAME, "note": "Every image is public domain, CC0 or freely licensed; source page and license per file. Images resized to at most 1200px (JPEG q80).",
               "images": credits}, open(f"{slug}/credits.json", "w"), indent=1, ensure_ascii=False)
    PG.write(dj, slug, dict(art=art, kicker="Art Taste Deck", h1="What art do you love?", em="art",
             lede="Real artworks from Hokusai to a Penang street mural. Pick what pulls you in, and the next deck narrows it down.",
             strip=["hokusai", "klimt", "rousseau", "yoshida", "sorolla", "korin"]))
    pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False); open("decks/pages.json", "a").write("\n")
    sz = json.load(open("decks/sizes.json")); sz[DID] = len(pairs); json.dump(sz, open("decks/sizes.json", "w"), indent=1, ensure_ascii=False); open("decks/sizes.json", "a").write("\n")
    print(DID, f"https://webermanapps.github.io/style-swipe/{slug}/", len(pairs))
if __name__ == "__main__": main(*sys.argv[1:3])
