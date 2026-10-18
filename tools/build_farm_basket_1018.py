"""Farm Basket Deck (Max asked Oct 18 2026 23:10 ICT; brief from WellNest). Project 4, Farm Basket Subscription.
Usage: python3 tools/build_farm_basket_1018.py [--pages-only]   (from the repo root).
Same Like / Pass single-card pattern as build_tea_ingredients_1018.py (its LP block: Hold and Love hidden, Notes saved with the vote,
Share in the standard footer, results route to WellNest). WellNest collab look: kraft frame, cream #FAF6EE, watercolour wash. Light only."""
import datetime, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from md1018_kit import page, EMOJI
from build_tea_ingredients_1018 import LP, START, END, WN
import farm_basket_1018 as FB
DID = "wellnest-farm-basket-deck"; NAME = "Farm Basket Deck"; SLUG = "farm-basket"
REQ = "Oct 18 2026 23:10 ICT: Max asked (brief from WellNest) for one Like/Pass deck for Project 4, Farm Basket Subscription: 14 food, 4 add-on ideas, 8 packaging, 4 basket formats"
def finish_page(slug):
    pg = os.path.join(slug, "index.html"); h = open(pg).read()
    if "const D=" in h: return
    h = re.sub(r"<title>[^<]*</title>", f"<title>{NAME} · Style Swipe</title>", h, count=1)
    h = h.replace("<style>:root{--bg:#FFFFFF}html,body{background:#FFFFFF!important}", "<style>:root{--bg:#FAF6EE!important}:root,:root body{background:#FAF6EE!important}", 1)
    assert '<a class="builtby' in h and 'id="shareBtn"' in h and "<!--/mw-r116-->" in h, "standard footer, Share button, r116 block"
    h = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", h, flags=re.S)
    i = h.rindex("</body>"); h = h[:i] + LP + "\n" + h[i:]
    open(pg, "w").write(h)
def build():
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds"); cards = []
    for i, (cat, nm, note, wash, kind, cols, tags) in enumerate(FB.CARDS, 1):
        oid = "fbasket18_" + re.sub(r"[^a-z0-9]+", "_", nm.lower()).strip("_")
        cards.append({"id": f"{DID}-{i:02d}", "category": cat, "group": cat, "app": "WellNest", "notes": True, "share": True,
                      "option": {"id": oid, "label": nm, "desc": note, "tags": tags, "feeling": "calm", "notes": True, "share": True,
                                 "visual": {"type": "hm", "m": "svg", "svg": FB.svg(i, cat, wash, kind, cols, tags)}}})
    assert len(cards) == 30
    d = {"date": DID, "version": 3, "owner": "Max Weberman", "format": "single", "like_pass": True, "english_only": True, "light_only": True,
         "title": NAME, "name": NAME, "generated_at": now, "status": "published", "cards": cards, "deck_size": len(cards), "no_cap": True,
         "share": True, "notes": True, **WN, "row": "nozomi", "project": "Project 4, Farm Basket Subscription", "requested": True, "request": REQ,
         "log_only": True, "groups": {}, "apps": {"WellNest": len(cards)}, "built_by": "Branding", "built_at_note": "Oct 18 2026 23:10 ICT request",
         "brands": ["WellNest look: kraft, cream #FAF6EE, watercolour wash", "Drawn SVGs only, no photos, no people; no prices, no farm claims"],
         "sources": {"content": "tools/farm_basket_1018.py", "builder": "tools/build_farm_basket_1018.py"}}
    for c in cards: d["groups"][c["category"]] = d["groups"].get(c["category"], 0) + 1
    assert not EMOJI.search(json.dumps(d, ensure_ascii=False)), "emoji"
    assert not re.search(r"(฿|baht|\$|\bTHB\b|organic|certified|pesticide)", json.dumps([c["option"]["label"] + c["option"]["desc"] for c in cards]), re.I)
    json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    so = json.load(open("shown_options.json"))
    for c in cards: so["options"].setdefault(c["option"]["id"], []).append(DID)
    so["shown_count"] = so.get("shown_count", 0) + len(cards); so["updated"] = now
    json.dump(so, open("shown_options.json", "w"), indent=1, ensure_ascii=False)
    from write_sizes import main as write_sizes; write_sizes()
    return len(cards)
if __name__ == "__main__":
    n = None if "--pages-only" in sys.argv else build()
    slug, url = page(DID, SLUG); finish_page(slug)
    print(DID, slug, url, n)
