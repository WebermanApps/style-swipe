#!/usr/bin/env python3
"""Build one deck of the WellNest 25-deck series. usage: build_wn_series.py <deckId>   (e.g. wellnest-brand-look-1)
Deck id == Submit deck value == deck-queue.json deckId. Standalone page <slug>/index.html with white background,
wn-deck-done localStorage on real submit, Back link -> wellnest-dashboard/?done=<deckId>. Submit -> agent 'wellnest'."""
import sys, os, json, random, string, re
sys.path.insert(0, os.path.dirname(__file__))
from wn_series_content import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATID = {"Brand Look": "brand-look", "Voice & Story": "voice-story", "Experiences & Tours": "experiences-tours", "Products & Tea": "products-tea", "Dashboard & Online": "dashboard-online"}
SLUGS = os.path.join(ROOT, "queue", "wn-series-slugs.json")
slugs = json.load(open(SLUGS)) if os.path.exists(SLUGS) else {}
FEEL = ["calm", "visual", "focused", "quick", "action"]
def render(o, dk, side, i):
    label, desc = o[0], o[1]; kind = dk; arg = {}
    if len(o) >= 3:
        if isinstance(o[2], str) and len(o) == 3 and o[2] not in ("av", "pk", "ph", "dash", "pal", "ty", "tag", "quote", "offer", "ig", "web"): arg = {"k": o[2]}
        else: kind = o[2]; arg = o[3] if len(o) > 3 else {}
    acc = arg.get("acc", GOLD if side == 0 else PEACH)
    if kind == "tag": return r_tag(label, desc, acc)
    if kind == "quote": return r_quote(label, desc, acc)
    if kind == "offer": return r_offer(label, desc, arg.get("k", "leaf"), acc, arg.get("btn", "Shop" if "products" in CUR else "Book"))
    if kind == "ig": return r_ig(label, desc, arg.get("k", "leaf"), acc)
    if kind == "web": return r_web(label, desc, arg.get("k", "sun"), acc)
    if kind == "pal": a = dict(arg); cols = a.pop("cols", [GOLD, PEACH]); return r_pal(label, desc, cols, **a)
    if kind == "av": a = dict(arg); return r_av(label, desc, a.pop("k"), **a)
    if kind == "dash": a = dict(arg); return r_dash(label, desc, a.pop("blocks"), **a)
    if kind == "ty": a = dict(arg); return r_ty(label, desc, a.pop("sample"), **a)
    if kind == "pk": a = dict(arg); return pouch(**a)
    if kind == "ph": a = dict(arg); return ph(**a)
    raise ValueError(kind)
def slug_for(did, base):
    if did not in slugs:
        slugs[did] = "wellnest-" + base + "-" + "".join(__import__("secrets").choice(string.ascii_lowercase + string.digits) for _ in range(6))
        json.dump(slugs, open(SLUGS, "w"), indent=1)
    return slugs[did]
def page(did, slug):
    HEAD = f'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="{did}"</script>
<style>:root{{--bg:#FDFBF6}}html,body{{background:#FDFBF6!important}}</style>
<script>(function(){{var ID="{did}",DONE="https://webermanapps.github.io/wellnest-dashboard/?done="+ID;
function mark(){{try{{var a=JSON.parse(localStorage.getItem("wn-deck-done")||"[]");if(!Array.isArray(a))a=[];if(a.indexOf(ID)<0)a.push(ID);localStorage.setItem("wn-deck-done",JSON.stringify(a))}}catch(e){{}}}}
var f=window.fetch;window.fetch=function(u,o){{var p=f.apply(this,arguments);try{{if(o&&o.method==="POST"&&o.body){{var b=JSON.parse(o.body);if(b&&b.deck===ID&&b.agent==="wellnest"&&!b.test&&!b.partial)p.then(function(){{mark()}},function(){{}})}}}}catch(e){{}}return p}};
function fix(){{document.querySelectorAll('a[href*="branding-djqmb410/decks"]').forEach(function(a){{a.href=DONE;a.removeAttribute("target")}})}}
new MutationObserver(fix).observe(document.documentElement,{{childList:true,subtree:true}});document.addEventListener("DOMContentLoaded",fix)}})();</script>
'''
    s = open(os.path.join(ROOT, "index.template.html")).read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True); open(os.path.join(ROOT, slug, "index.html"), "w").write(s)
did = sys.argv[1]; CUR = did
os.chdir(ROOT)
if did == "wellnest-dashboard-online-1":
    d = json.load(open("decks/wellnest-dashboard.json")); d["date"] = did; d["title"] = "Dashboard: WellNest Dashboard Look"
    d["submit_agent"] = "wellnest"; d["note_series"] = "Copy of wellnest-dashboard under the series deckId so Submit matches deck-queue.json"
    for p in d["pairs"]:
        for k in ("optionA", "optionB"): p[k]["visual"]["bg"] = "#FFFFFF"
    json.dump(d, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    from write_sizes import main as ws; ws()
    slug = slug_for(did, "dash-look"); page(did, slug); print(json.dumps({"deckId": did, "name": d["title"], "slug": slug, "n": len(d["pairs"])})); sys.exit()
spec = next(x for x in D if f"wellnest-{CATID[x['cat']]}-{x['order']}" == did)
pairs, O, add = deck("wx" + str(abs(hash(did)) % 997) + "_", "WellNest") if False else __import__("team_kit").deck(did.replace("wellnest-", "").replace("-", "")[:10] + "_", "WellNest")
n = 0
for gi, (g, ask, a, b) in enumerate(spec["pairs"]):
    opts = []
    for side, o in enumerate((a, b)):
        n += 1; oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{n}"
        opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], render(o, spec["dk"], side, gi)))
    add(g, g, opts[0], opts[1], ask)

# ---- Round Two fold-in (Oct 14, 13:40): Max dropped the 61-pair Round Two; its key retests move into the 20-card series ----
R1 = json.load(open(os.path.join(ROOT, "decks/wellnest-brand.json"))); R2 = json.load(open(os.path.join(ROOT, "decks/wellnest-brand-round-two.json")))
def _r2(prefix): return [p for p in R2["pairs"] if p["optionA"]["id"].startswith(prefix)]
def _r1(pid): return [p for p in R1["pairs"] if p["id"] == pid]
FOLD = {
 "wellnest-voice-story-1": (_r2("wn2_tg2_") + _r1("wellnest-brand-138"),
   ["Wellness Words: Rest, Warm, Slow Or Wellness Words: Reset, Recharge?", "Rest Grows Wild Here Or Sip Slowly?", "The Farm Is The Spa Or Farm, Steam, Rest?", "Homegrown Calm Or Warmth, Grown Daily?", "Find Your Nest In San Sai Or Find Your Nest, Pour Your Tea?", "Rest Is A Farm Skill, Learn It Or Sun-Dried, Hand-Picked, Home?", "Come As Guests, Leave Rested Or Come As Guests, Leave As Family?"]),
 "wellnest-voice-story-2": (_r2("wn2_sa2_") + _r1("wellnest-brand-151"),
   ["Why A Nest: Shelter Or Why A Nest: Gathering?", "Why San Sai: Soil And Water Or Why San Sai: Family Roots?", "Neighbours Who Help Or Guests Who Return?", "Seasons As Chapters Or Plants As Chapters?", "Founders Shown Together Or Family Shown, Founders Quiet?", "Story Video: Two Minutes Or Story Video: Ten Short Reels?", "Story Ends With An Invitation Or Story Ends With A Recipe?"]),
 "wellnest-voice-story-3": ([p for p in R2["pairs"] if p["optionA"]["id"] in ("wn2_tn_logo_small", "wn2_tn_cap_en")] + _r1("wellnest-brand-114") + _r1("wellnest-brand-118"),
   ["Polls In Stories Or Farm Diary Stories?", "Hashtags: Three Local Or No Hashtags?", "Caption Line Breaks Or Single Paragraph?", "Weather Notes Or No Weather Notes?"]),
 "wellnest-brand-look-1": ([p for p in R2["pairs"] if p["optionA"]["id"] == "wn2_tn_gold_lead"], ["Section Tint: Pale Gold Or Pale Peach?"]),
 "wellnest-brand-look-4": (_r1("wellnest-brand-41") + _r1("wellnest-brand-124") + _r1("wellnest-brand-136") + _r1("wellnest-brand-187"),
   ["Animals: Chickens And Ducks Or Plants Only?", "Shadows: Soft Or Strong?", "Rainy Season: Show Rain Or Avoid?", "Text On Photos: Never Or Short Title?"]),
}
if did in FOLD:
    src, drop = FOLD[did]; before = len(pairs)
    keep = [p for p in pairs if p["ask"] not in drop]; assert before - len(keep) == len(drop), (did, before - len(keep), len(drop))
    pairs[:] = keep
    for p in src:
        a, b = json.loads(json.dumps(p["optionA"])), json.loads(json.dumps(p["optionB"]))
        for o in (a, b): o["id"] = "rt_" + o["id"]; o["notes"] = True; o["share"] = True
        add("Round Two Retest: " + p["group"].replace("Retest: ", ""), "Round Two Retest", a, b, p["ask"], "retest"); pairs[-1]["retest"] = True
    assert len(pairs) <= 20, (did, len(pairs)); print("folded", did, "+", len(src), "-", len(drop), "=", len(pairs))
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(did, spec["name"], "WellNest", pairs,
        {"brands": [spec["about"], "Locked WellNest brand: original nest logo, Cormorant + DM Sans, gold leads, peach accent, sand lines; white deck background; drawn SVGs, sample content only"],
         "submit_agent": "wellnest", "submit_to": "WellNest Agent", "section_counts": cnt, "deck_size": len(pairs), "series": {"category": spec["cat"], "order": spec["order"]},
         "sources": {"rules": "/workspace/wellnest/brand-rules.md", "results": "/workspace/wellnest/deck-results/", "queue": "/workspace/wellnest/deck-queue.json"}},
        seed=3000 + n, n=len(pairs))
dj = json.load(open(f"decks/{did}.json"))
for p in dj["pairs"]:
    for k in ("optionA", "optionB"): p[k]["visual"]["bg"] = "#FFFFFF"
json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
slug = slug_for(did, spec["slug"]); page(did, slug)
print(json.dumps({"deckId": did, "name": spec["name"], "slug": slug, "n": len(pairs)}))
