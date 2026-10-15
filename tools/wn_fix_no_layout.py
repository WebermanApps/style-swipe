#!/usr/bin/env python3
"""Max rule Oct 15 2026 12:45 ICT: WellNest decks carry no dashboard layout/structure questions (partners swipe them).
Replaces every blocked pair (tools/wn_guard.py) IN PLACE in the unfinished WellNest dashboard decks with dashboard
COLOUR/FONT pairs or non-dashboard WellNest pairs (rentals, classes, wellness, farm, tea, brand). Same deckIds, same pages,
same deck size. Locked brand: nest logo, Cormorant + DM Sans, gold leads, peach accent, sand lines; white deck background."""
import sys, os, json, re, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from wn_series_kit import *
from wn_guard import blocked, RULE
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
FEEL = ["calm", "visual", "focused", "quick", "action"]
WHITE = "#FFFFFF"
def dmock(label, desc, acc=GOLD, bg=RICE_BRAND, ink=INK, line=SAND, hf=SER, bf=SANS, bs=9, hs=12, link=None, it=False, tagc=None, done=None, warn=None, sel=None, icol=None):
    """Same small dashboard mock on both sides; only colour or font changes."""
    s = rect(0, 0, 240, 300, bg) + logo(24, 22, 24) + tf(42, 27, "The WellNest", hs, ink, hf, 600, "start", 'font-style="italic"' if it else "")
    s += f'<line x1="12" y1="42" x2="228" y2="42" stroke="{line}"/>'
    rows = [("Pick the tea label", acc), ("Sauna menu words", done or acc), ("Stay photos", warn or acc)]
    for i, (t, c) in enumerate(rows):
        y = 54 + i * 44
        s += rect(12, y, 216, 36, sel if (sel and i == 0) else WHITE, line, 8) + rect(12, y, 4, 36, c, "none", 2)
        if icol: s += f'<circle cx="32" cy="{y+18}" r="6" fill="none" stroke="{icol}" stroke-width="1.6"/>'
        s += tf(46 if icol else 24, y + 22, t, bs, ink, bf, 500, "start")
        if tagc: s += rect(170, y + 11, 48, 14, tagc + "33", "none", 7) + tf(194, y + 21, "Brand", 7.5, ink, bf, 600)
    if link: s += tf(24, 202, "See all decisions", 9, link, bf, 600, "start", 'text-decoration="underline"')
    if done: s += tf(216, 202, "3 done", 9, done, bf, 600, "end")
    s += rect(84, 210, 72, 20, acc, "none", 10) + tf(120, 224, "Open Deck", 8, WHITE if acc in (FOREST, ROSELLE) else ink, bf, 600)
    s += tf(120, 252, label, 11, INK, SANS, 600) + para(268, desc, 44, 7.5)
    return scr(s, bg)
def fmock(label, desc, fam, size=20, wt=500, sample="Good Morning, The WellNest", body=SANS, bsize=9, thai=None):
    s = rect(0, 0, 240, 300, RICE_BRAND) + logo(120, 44, 44)
    for i, l in enumerate(W(sample, 18)[:2]): s += tf(120, 104 + i * (size + 4), l, size, INK, fam, wt)
    s += para(160, "Three brand picks are waiting. Roselle harvest starts next week.", 36, bsize, MUTE, bsize + 5, fam=body)
    if thai: s += tf(120, 214, thai, 12, INK, body, 500)
    s += tf(120, 252, label, 11, INK, SANS, 600) + para(268, desc, 44, 7.5)
    return scr(s, RICE_BRAND)
def off(label, desc, k, acc=None, btn="Book"): return lambda side: r_offer(label, desc, k, acc or (GOLD if side == 0 else PEACH), btn)
def tag(label, desc): return lambda side: r_tag(label, desc, GOLD if side == 0 else PEACH)
def qt(label, desc): return lambda side: r_quote(label, desc, GOLD if side == 0 else PEACH)
def fix(f): return lambda side: f
# ---------- dashboard colour / font pairs ----------
CF = [
 ("Dashboard Colour", "Dashboard Buttons: Gold Or Forest Green?", ("Gold Buttons", "Warm, matches the logo", fix(dmock("Gold Buttons", "Warm, matches the logo", acc=GOLD))), ("Forest Green Buttons", "Deeper, calmer", fix(dmock("Forest Green Buttons", "Deeper, calmer", acc=FOREST)))),
 ("Dashboard Colour", "Dashboard Page Colour: Pale Sand Or Pure White?", ("Pale Sand", "Soft warm page", fix(dmock("Pale Sand", "Soft warm page", bg="#F6EEDC"))), ("Pure White", "Bright and clean", fix(dmock("Pure White", "Bright and clean", bg=WHITE)))),
 ("Dashboard Colour", "New Items Colour: Peach Or Leaf Green?", ("Peach", "Soft peach marks new", fix(dmock("Peach", "Soft peach marks new", acc=PEACH))), ("Leaf Green", "Fresh green marks new", fix(dmock("Leaf Green", "Fresh green marks new", acc=LEAF)))),
 ("Dashboard Colour", "Done Colour: Forest Green Or Gold?", ("Forest Green", "Green for finished", fix(dmock("Forest Green", "Green for finished", done=FOREST))), ("Gold", "Gold for finished", fix(dmock("Gold", "Gold for finished", done=CMG)))),
 ("Dashboard Colour", "Dashboard Text Colour: Warm Brown-Black Or Neutral Charcoal?", ("Warm Brown-Black", "Soft, earthy ink", fix(dmock("Warm Brown-Black", "Soft, earthy ink", ink="#2B2118"))), ("Neutral Charcoal", "Plain dark grey", fix(dmock("Neutral Charcoal", "Plain dark grey", ink="#333333")))),
 ("Dashboard Colour", "Dashboard Lines: Sand Or Pale Grey?", ("Sand Lines", "Warm thin lines", fix(dmock("Sand Lines", "Warm thin lines", line=SAND))), ("Pale Grey Lines", "Neutral thin lines", fix(dmock("Pale Grey Lines", "Neutral thin lines", line="#D9D9D9")))),
 ("Dashboard Colour", "Dashboard Links: Forest Green Or Dark Gold?", ("Forest Green Links", "Green underlined words", fix(dmock("Forest Green Links", "Green underlined words", link=FOREST))), ("Dark Gold Links", "Gold underlined words", fix(dmock("Dark Gold Links", "Gold underlined words", link=CMG)))),
 ("Dashboard Colour", "Needs-Attention Colour: Peach Or Roselle Red?", ("Peach", "Gentle nudge", fix(dmock("Peach", "Gentle nudge", warn=PEACH))), ("Roselle Red", "Stronger nudge", fix(dmock("Roselle Red", "Stronger nudge", warn=ROSELLE)))),
 ("Dashboard Colour", "Selected Item: Pale Gold Or Pale Peach?", ("Pale Gold", "Light gold fill", fix(dmock("Pale Gold", "Light gold fill", sel="#F8EDCF"))), ("Pale Peach", "Light peach fill", fix(dmock("Pale Peach", "Light peach fill", sel="#F5E3D0")))),
 ("Dashboard Colour", "Dashboard Icons: Gold Or Ink?", ("Gold Icons", "Small gold outlines", fix(dmock("Gold Icons", "Small gold outlines", icol=CMG))), ("Ink Icons", "Small dark outlines", fix(dmock("Ink Icons", "Small dark outlines", icol=INK)))),
 ("Dashboard Colour", "Dashboard Tags: Pale Peach Or Pale Leaf Green?", ("Dark On Pale Peach", "Peach tint tags", fix(dmock("Dark On Pale Peach", "Peach tint tags", tagc=PEACH))), ("Dark On Pale Leaf", "Leaf tint tags", fix(dmock("Dark On Pale Leaf", "Leaf tint tags", tagc=LEAF)))),
 ("Dashboard Font", "Dashboard Body Text: DM Sans Or Cormorant?", ("DM Sans", "Clean, easy to read", fix(fmock("DM Sans", "Clean, easy to read", SER, body=SANS))), ("Cormorant", "Matches the name", fix(fmock("Cormorant", "Matches the name", SER, body=SER, bsize=10)))),
 ("Dashboard Font", "Dashboard Numbers: Cormorant Or DM Sans?", ("Cormorant Numbers", "Elegant 3 of 20", fix(fmock("Cormorant Numbers", "Elegant 3 of 20", SER, 26, sample="3 of 20 Answered"))), ("DM Sans Numbers", "Plain 3 of 20", fix(fmock("DM Sans Numbers", "Plain 3 of 20", SANS, 22, 600, sample="3 of 20 Answered")))),
 ("Dashboard Font", "Dashboard Greeting Size: Large Or Moderate?", ("Large", "Big Cormorant greeting", fix(fmock("Large", "Big Cormorant greeting", SER, 26))), ("Moderate", "Smaller, quieter greeting", fix(fmock("Moderate", "Smaller, quieter greeting", SER, 17)))),
 ("Dashboard Font", "Dashboard Name: Upright Or Italic Cormorant?", ("Upright", "Classic and steady", fix(dmock("Upright", "Classic and steady", hs=14))), ("Italic", "Softer, handwritten feel", fix(dmock("Italic", "Softer, handwritten feel", hs=14, it=True)))),
 ("Dashboard Font", "Dashboard Text Size: Standard Or Larger?", ("Standard", "More fits on screen", fix(dmock("Standard", "More fits on screen", bs=9))), ("Larger", "Easier for everyone", fix(dmock("Larger", "Easier for everyone", bs=11)))),
 ("Dashboard Font", "Dashboard Thai Text: Sarabun Or Noto Sans Thai?", ("Sarabun", "Friendly, rounded Thai", fix(fmock("Sarabun", "Friendly, rounded Thai", SER, body="Sarabun, sans-serif", thai="สวัสดีค่ะ ยินดีต้อนรับ"))), ("Noto Sans Thai", "Clean, matches DM Sans", fix(fmock("Noto Sans Thai", "Clean, matches DM Sans", SER, body="'Noto Sans Thai', sans-serif", thai="สวัสดีค่ะ ยินดีต้อนรับ")))),
]
# ---------- non-dashboard WellNest pairs ----------
RENT = [
 ("Rentals", "Bungalow Rental: Nightly Or Three-Night Minimum?", ("Nightly", "Easy short visits", off("Nightly", "Easy short visits", "stay")), ("Three-Night Minimum", "Slower, deeper stays", off("Three-Night Minimum", "Slower, deeper stays", "stay"))),
 ("Rentals", "Arrival Welcome: Roselle Tea Or Herbal Foot Soak?", ("Roselle Tea", "A warm cup on arrival", off("Roselle Tea", "A warm cup on arrival", "tea")), ("Herbal Foot Soak", "Rest tired feet first", off("Herbal Foot Soak", "Rest tired feet first", "drop"))),
 ("Rentals", "Bedding: Natural Linen Or Crisp White Cotton?", ("Natural Linen", "Soft, earthy, relaxed", off("Natural Linen", "Soft, earthy, relaxed", "stay")), ("Crisp White Cotton", "Hotel-fresh and bright", off("Crisp White Cotton", "Hotel-fresh and bright", "stay"))),
 ("Rentals", "Long Stays: Monthly Nomad Rate Or Short Stays Only?", ("Monthly Nomad Rate", "Workers stay a month", off("Monthly Nomad Rate", "Workers stay a month", "cowork")), ("Short Stays Only", "Keep it a getaway", off("Short Stays Only", "Keep it a getaway", "sun"))),
 ("Rentals", "Breakfast: Included In The Stay Or Paid Separately?", ("Included", "Eggs, fruit and tea from the farm", off("Included", "Eggs, fruit and tea from the farm", "food")), ("Paid Separately", "Lower room rate", off("Paid Separately", "Lower room rate", "food"))),
 ("Classes", "First Class To Offer: Tea Blending Or Farm Cooking?", ("Tea Blending", "Mix your own roselle blend", off("Tea Blending", "Mix your own roselle blend", "tea")), ("Farm Cooking", "Cook Thai dishes from the garden", off("Farm Cooking", "Cook Thai dishes from the garden", "food"))),
 ("Classes", "Class Size: Six Guests Or Fifteen Guests?", ("Six Guests", "Close and personal", off("Six Guests", "Close and personal", "people")), ("Fifteen Guests", "Livelier, lower price", off("Fifteen Guests", "Livelier, lower price", "people"))),
 ("Wellness", "Morning Yoga: In The Tea Field Or In The Sala?", ("In The Tea Field", "Open sky, rows of green", off("In The Tea Field", "Open sky, rows of green", "farm")), ("In The Sala", "Shaded, calm, any weather", off("In The Sala", "Shaded, calm, any weather", "sun"))),
 ("Classes", "Kids: Little Farmers Club Or Adults-Only Classes?", ("Little Farmers Club", "Planting and picking for kids", off("Little Farmers Club", "Planting and picking for kids", "flower")), ("Adults Only", "Quiet classes for grown-ups", off("Adults Only", "Quiet classes for grown-ups", "class"))),
 ("Classes", "Class Length: Ninety Minutes Or Half A Day?", ("Ninety Minutes", "Fits any visit", off("Ninety Minutes", "Fits any visit", "class")), ("Half A Day", "Class plus lunch", off("Half A Day", "Class plus lunch", "food"))),
]
FARM = [
 ("Farm", "Farm Walk Finish: Roselle Field Or Herb Garden?", ("Roselle Field", "End among red calyces", off("Roselle Field", "End among red calyces", "flower")), ("Herb Garden", "End among lemongrass and mint", off("Herb Garden", "End among lemongrass and mint", "leaf"))),
 ("Farm", "Farm Animals: A Few Chickens Or Plants Only?", ("A Few Chickens", "Fresh eggs, guests love them", off("A Few Chickens", "Fresh eggs, guests love them", "basket")), ("Plants Only", "Simpler, quieter farm", off("Plants Only", "Simpler, quieter farm", "leaf"))),
 ("Farm", "Pick Your Own: Roselle Picking Or Herb Picking?", ("Roselle Picking", "Seasonal, Nov to Jan", off("Roselle Picking", "Seasonal, Nov to Jan", "basket")), ("Herb Picking", "Open all year", off("Herb Picking", "Open all year", "basket"))),
 ("Tea", "Signature Cup: Hot Roselle Or Iced Roselle With Lime?", ("Hot Roselle", "Warm and calming", off("Hot Roselle", "Warm and calming", "tea", btn="Shop")), ("Iced Roselle With Lime", "Bright, for hot days", off("Iced Roselle With Lime", "Bright, for hot days", "bottle", btn="Shop"))),
 ("Tea", "Tea Tasting: Three Teas Or Five Teas?", ("Three Teas", "Short and focused", off("Three Teas", "Short and focused", "tea")), ("Five Teas", "The full farm line", off("Five Teas", "The full farm line", "tea"))),
 ("Tea", "Tea Sweetener: Wild Honey Or Palm Sugar?", ("Wild Honey", "From nearby hives", off("Wild Honey", "From nearby hives", "jar", btn="Shop")), ("Palm Sugar", "Classic Thai sweetness", off("Palm Sugar", "Classic Thai sweetness", "jar", btn="Shop"))),
 ("Brand", "Brand Feeling: Grounded Farm Or Gentle Retreat?", ("Grounded Farm", "Hands in the soil", tag("Grounded Farm", "Real work, real harvest, honest food")), ("Gentle Retreat", "Rest and slow down", tag("Gentle Retreat", "Quiet mornings, warm tea, rest"))),
 ("Brand", "Brand Promise: Grown Here Or Made With Care?", ("Grown Here", "Everything from our land", qt("Grown Here", "Every cup starts in our own field.")), ("Made With Care", "Small batches by hand", qt("Made With Care", "Picked, dried and packed by hand."))),
 ("Brand", "Staff Wear: Linen Aprons Or Farm Shirts?", ("Linen Aprons", "Natural, tea-house feel", off("Linen Aprons", "Natural, tea-house feel", "hat")), ("Farm Shirts", "Relaxed, working-farm feel", off("Farm Shirts", "Relaxed, working-farm feel", "hat"))),
 ("Wellness", "Sauna Finish: Cold Plunge Or Herbal Steam Towel?", ("Cold Plunge", "Bracing and bright", off("Cold Plunge", "Bracing and bright", "plunge")), ("Herbal Steam Towel", "Warm lemongrass towel", off("Herbal Steam Towel", "Warm lemongrass towel", "sauna"))),
 ("Wellness", "Massage Oil: Lemongrass Or Plai Ginger?", ("Lemongrass", "Fresh and lifting", off("Lemongrass", "Fresh and lifting", "bottle")), ("Plai Ginger", "Warm, for tired muscles", off("Plai Ginger", "Warm, for tired muscles", "bottle"))),
 ("Wellness", "Quiet Hours: Silent Mornings Or Quiet After Dark?", ("Silent Mornings", "No talking until breakfast", off("Silent Mornings", "No talking until breakfast", "sun")), ("Quiet After Dark", "Calm evenings, stars", off("Quiet After Dark", "Calm evenings, stars", "stay"))),
 ("Farm", "Farm Shop Day: Saturday Market Or Open Every Day?", ("Saturday Market", "One busy farm day", off("Saturday Market", "One busy farm day", "bag", btn="Shop")), ("Open Every Day", "Drop in any time", off("Open Every Day", "Drop in any time", "bag", btn="Shop"))),
 ("Tea", "Tea Gift: Tin Of Three Blends Or One Big Pouch?", ("Tin Of Three Blends", "A taste of the line", off("Tin Of Three Blends", "A taste of the line", "gift", btn="Shop")), ("One Big Pouch", "Plenty of a favourite", off("One Big Pouch", "Plenty of a favourite", "bag", btn="Shop"))),
]
WELL = [
 ("Wellness", "Retreat Length: Weekend Or Five Days?", ("Weekend", "Two nights to reset", off("Weekend", "Two nights to reset", "stay")), ("Five Days", "A real break", off("Five Days", "A real break", "stay"))),
 ("Wellness", "Retreat Food: Plant-Based Or Farm Mixed Menu?", ("Plant-Based", "All from the garden", off("Plant-Based", "All from the garden", "food")), ("Farm Mixed Menu", "Garden plus local eggs and fish", off("Farm Mixed Menu", "Garden plus local eggs and fish", "food"))),
 ("Wellness", "Evening Ritual: Sound Bath Or Tea Ceremony?", ("Sound Bath", "Bowls and rest", off("Sound Bath", "Bowls and rest", "class")), ("Tea Ceremony", "Slow roselle pour", off("Tea Ceremony", "Slow roselle pour", "tea"))),
 ("Wellness", "Phones: Phone Basket At Check-In Or Your Choice?", ("Phone Basket", "A true digital rest", off("Phone Basket", "A true digital rest", "basket")), ("Your Choice", "Guests decide", off("Your Choice", "Guests decide", "people"))),
 ("Rentals", "Rent The Whole Farm: Private Events Or Never?", ("Private Events", "Weddings and offsites", off("Private Events", "Weddings and offsites", "people")), ("Never", "Always open to guests", off("Never", "Always open to guests", "farm"))),
 ("Rentals", "Cowork Pass: Day Pass Or Weekly Pass?", ("Day Pass", "Drop in to work", off("Day Pass", "Drop in to work", "cowork")), ("Weekly Pass", "A focused work week", off("Weekly Pass", "A focused work week", "cowork"))),
 ("Classes", "Herbal Class: Make A Balm Or Make A Bath Soak?", ("Make A Balm", "Take home a small tin", off("Make A Balm", "Take home a small tin", "jar")), ("Make A Bath Soak", "Take home a jar of salts", off("Make A Bath Soak", "Take home a jar of salts", "jar"))),
 ("Classes", "Who Teaches: Family Members Or Visiting Teachers?", ("Family Members", "Our own stories", off("Family Members", "Our own stories", "people")), ("Visiting Teachers", "Fresh skills each month", off("Visiting Teachers", "Fresh skills each month", "class"))),
 ("Farm", "Compost Corner: Show Guests Or Keep Behind The Scenes?", ("Show Guests", "Part of the farm story", off("Show Guests", "Part of the farm story", "leaf")), ("Behind The Scenes", "Keep the visit tidy", off("Behind The Scenes", "Keep the visit tidy", "farm"))),
 ("Tea", "Tea Harvest Name: Roselle Season Or Red Harvest?", ("Roselle Season", "Plain and clear", tag("Roselle Season", "Our yearly roselle picking weeks")), ("Red Harvest", "Bold and memorable", tag("Red Harvest", "Our yearly roselle picking weeks"))),
 ("Brand", "Brand Sound: Birdsong Or Soft Guitar For Videos?", ("Birdsong", "Real farm sound", off("Birdsong", "Real farm sound", "sun")), ("Soft Guitar", "Warm, gentle music", off("Soft Guitar", "Warm, gentle music", "camera"))),
 ("Brand", "Guest Keepsake: Pressed Roselle Bookmark Or Seed Packet?", ("Pressed Roselle Bookmark", "A flower to keep", off("Pressed Roselle Bookmark", "A flower to keep", "flower", btn="Shop")), ("Seed Packet", "Grow your own at home", off("Seed Packet", "Grow your own at home", "leaf", btn="Shop"))),
]
PLAN = {
 # wellnest-dashboard-online-1 was submitted (done 2026-10-15 12:45:15 ICT) before this fix, so it is left as completed.
 # "wellnest-dashboard-online-1": dict(name="Dashboard Colours, Rentals And Classes", pool=CF[:9] + RENT, about="Dashboard colour and font only (no layout), plus rentals, classes and wellness"),
 "wellnest-dashboard-online-2": dict(name="Dashboard Fonts, Farm And Tea", pool=CF[9:] + FARM, about="Dashboard colour and font only (no layout), plus farm, tea, brand and wellness"),
 "wellnest-dashboard": dict(name="WellNest Colour, Font And Wellness Deck", pool=CF[1:2] + CF[13:16] + WELL, about="Dashboard colour, font and avatar only (no layout), plus wellness, rentals, classes, farm and tea", ctx=True),
}
KEEP_AVATAR = re.compile(r"Avatar")
def run(did, plan):
    f = f"decks/{did}.json"; d = json.load(open(f)); ps = d["pairs"]; n0 = len(ps)
    have = {p["ask"] for p in ps}
    bad = [i for i, p in enumerate(ps) if blocked(p, True) and not (did == "wellnest-dashboard" and KEEP_AVATAR.search(p["group"]))]
    pool = [x for x in plan["pool"] if x[1] not in have]
    assert len(pool) >= len(bad), (did, len(pool), len(bad))
    removed = [ps[i]["ask"] for i in bad]
    for j, i in enumerate(bad):
        g, ask, a, b = pool[j]; opts = []
        for side, o in enumerate((a, b)):
            oid = f"wnnl_{did.replace('wellnest-', '').replace('-', '')[:10]}_{i}_{side}"
            svg = o[2](side)
            opts.append({"id": oid, "label": o[0], "desc": o[1], "tags": [FEEL[(i * 2 + side) % 5]], "feeling": FEEL[(i * 2 + side) % 5], "notes": True, "share": True,
                         "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": WHITE}})
        ps[i] = {"group": g, "category": g, "app": "WellNest", "ask": ask, "optionA": opts[0], "optionB": opts[1], "purpose": "new", "retest": False,
                 "notes": True, "share": True, "id": f"{did}-nl{i}", "repeat": False}
    assert len(ps) == n0 and not any(blocked(p, True) and not KEEP_AVATAR.search(p["group"]) for p in ps)
    ids = [p["option" + k]["id"] for p in ps for k in "AB"]; assert len(ids) == len(set(ids))
    if plan["name"]: d["title"] = plan["name"]
    g = {}
    for p in ps: g[p["group"]] = g.get(p["group"], 0) + 1
    d["groups"] = g; d["section_counts"] = g
    fc = {}
    for p in ps:
        for k in "AB": fc[p["option" + k]["feeling"]] = fc.get(p["option" + k]["feeling"], 0) + 1
    d["feeling_counts"] = fc
    d["brands"] = [plan["about"]] + d.get("brands", [])[1:]
    d["no_dashboard_layout"] = RULE; d["generated_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    d.pop("rebuilt", None)
    json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
    return {"deck": did, "title": d["title"], "pairs": len(ps), "replaced": len(bad), "removed": removed}
if __name__ == "__main__":
    out = [run(k, v) for k, v in PLAN.items()]
    print(json.dumps(out, indent=1, ensure_ascii=False))
