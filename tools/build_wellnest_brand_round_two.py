#!/usr/bin/env python3
"""Build Style Swipe deck wellnest-brand-round-two: WellNest Brand Deck Round Two (Oct 14 2026).
After Round One (192/200, sub 35a22b29): new taglines + story angles (no global-family, no founder-story framings),
retests of every Neither/skip card (except the two rejected framing pairs and the two founder-voice pairs),
retests of the three tensions (logo on posts, Thai in captions, gold vs green). Built in the picked direction:
real nest logo, Cormorant + DM Sans, rice-white base, gold leading, peach accent. Submit -> agent 'wellnest'."""
import sys, os, json, copy
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
_src = open(os.path.join(os.path.dirname(__file__), "build_wellnest_brand.py")).read()
exec(_src[_src.index("FOREST, DEEP"):_src.index("# ---------- 1")])   # shared colours, logo(), icon(), tf(), scr()
DID = "wellnest-brand-round-two"
pairs, O, add = deck("wn2_", "WellNest")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def P(group, a, b, ask=None, purpose="new"):
    add(group, group, O(*a), O(*b), ask or f"{a[1]} Or {b[1]}?", purpose)

def tag(line, sub="", acc=GOLD):
    s = rect(0, 0, 240, 300, RICE) + logo(120, 74, 100)
    words = line.split(); half = (len(words) + 1) // 2
    l1, l2 = " ".join(words[:half]), " ".join(words[half:])
    s += tf(120, 168, l1, 22, INK, SER, 500) + tf(120, 196, l2, 22, INK, SER, 500)
    s += f'<line x1="96" y1="214" x2="144" y2="214" stroke="{acc}" stroke-width="2"/>'
    s += tf(120, 240, "THE WELLNEST", 8, MUTE, SANS, 500, extra='letter-spacing="2"')
    if sub: s += tf(120, 262, sub, 8, MUTE, SANS, 400)
    return scr(s, RICE)

def story(title, line, k, acc=GOLD):
    s = rect(0, 0, 240, 300, RICE) + rect(18, 22, 204, 150, "#FFFFFF", SAND, 12)
    s += f'<circle cx="120" cy="97" r="44" fill="none" stroke="{acc}" stroke-width="2"/>' + icon(k, 96, 73, 48, acc, 1.5)
    s += tf(120, 204, title, 18, INK, SER, 600) + tf(120, 226, line, 9, MUTE, SANS, 400)
    s += rect(84, 246, 72, 22, PEACH, "none", 11) + tf(120, 261, "Read The Story", 8, "#FFFFFF", SANS, 600)
    return scr(s, RICE)

def ig(logo_on=False, cap1="Roselle drying in the sun.", cap2=""):
    s = rect(0, 0, 240, 300, RICE) + rect(24, 30, 192, 170, ROSELLE + "22", "none", 8)
    for i in range(6):
        s += f'<circle cx="{58+i*25}" cy="{110+(i%2)*18}" r="10" fill="{ROSELLE}" opacity=".8"/>'
    if logo_on: s += rect(176, 160, 34, 34, "#FFFFFF", "none", 17) + logo(193, 177, 30)
    s += tf(28, 224, cap1, 10, INK, SANS, 400, "start")
    if cap2: s += f'<text x="28" y="242" font-size="10" fill="{MUTE}" font-family="Noto Sans Thai, sans-serif" text-anchor="start">{esc(cap2)}</text>'
    return scr(s, RICE)

def lead(main, second, name):
    s = rect(0, 0, 240, 300, RICE) + logo(120, 62, 80)
    s += tf(120, 134, "Farm Life, Open To All", 18, INK, SER, 500)
    s += rect(60, 152, 120, 30, main, "none", 15) + tf(120, 171, "Book A Farm Day", 9, "#FFFFFF" if main != GOLD else INK, SANS, 600)
    for i, c in enumerate([main, main, second, PEACH]):
        s += rect(42 + i * 40, 206, 36, 36, c, "none", 6)
    s += tf(120, 266, name, 8, MUTE, SANS, 400)
    return scr(s, RICE)

# ---------- New Taglines (12 pairs counted as 6) ----------
G = "New Taglines"
for (ia, la, da, fa), (ib, lb, db, fb) in [
 (("tg2_home", "Slow Down, You're Home", "Gentle welcome.", "calm"), ("tg2_rest", "Rest Grows Here", "Rest as a crop.", "calm")),
 (("tg2_poured", "Grown Slowly, Poured Warmly", "Tea-first.", "visual"), ("tg2_steeped", "Steeped In San Sai", "Place-first.", "focused")),
 (("tg2_wings", "Come Rest Your Wings", "Nest image, poetic.", "visual"), ("tg2_tea_nest", "Every Nest Needs Tea", "Light humour.", "quick")),
 (("tg2_dawn", "Picked At Dawn, Sipped At Dusk", "A whole farm day.", "visual"), ("tg2_softer", "Where The Day Grows Softer", "Mood-first.", "calm")),
 (("tg2_soil", "Good Soil, Good Rest", "Organic and rest.", "focused"), ("tg2_air", "Farm Air Is Free", "Light humour.", "quick")),
 (("tg2_exhale", "A Farm To Exhale In", "Wellness-first.", "calm"), ("tg2_rooted", "Rooted In Chiang Mai", "Place-first.", "focused")),
]: P(G, (ia, la, da, fa, tag(la)), (ib, lb, db, fb, tag(lb, acc=PEACH)))

# ---------- New Story Angles (6) ----------
G = "New Story Angles"
for (ia, la, da, fa, ka), (ib, lb, db, fb, kb) in [
 (("sa2_notebook", "Mae Noy's Tea Notebook", "Her notes, her blends.", "calm", "class"), ("sa2_kidsq", "Kids' Farm Questions", "Kids ask, the farm answers.", "quick", "people")),
 (("sa2_nospray", "Why We Never Spray", "Organic, plainly told.", "focused", "leaf"), ("sa2_thisweek", "What Grows This Week", "A weekly farm note.", "quick", "farm")),
 (("sa2_dawn", "The Nest At Dawn", "First light on the farm.", "visual", "sun"), ("sa2_sauna", "A Sauna Hour Diary", "One hour, minute by minute.", "calm", "sauna")),
 (("sa2_lessons", "Little Farm Lessons", "One small skill a week.", "action", "basket"), ("sa2_recipes", "Recipes From The Rows", "Cook what we pick.", "action", "food")),
 (("sa2_herbs", "Meet The Herbs", "One plant per story.", "visual", "flower"), ("sa2_onecup", "One Cup, Three Ways", "Hot, iced, punch.", "quick", "tea")),
 (("sa2_built", "How The Nest Was Built", "Barn, sauna, stays.", "focused", "stay"), ("sa2_guestday", "A Guest's First Day", "Arrive to sunset.", "visual", "camera")),
]: P(G, (ia, la, da, fa, story(la, da, ka)), (ib, lb, db, fb, story(lb, db, kb, PEACH)))

# ---------- Tensions (3) ----------
G = "Tensions To Settle"
P(G, ("tn_logo_small", "Small Nest Logo On Posts", "A small logo in the corner.", "visual", ig(True)),
     ("tn_logo_none", "No Logo On Posts", "Photo and caption only.", "calm", ig(False)), "Logo On Posts: Small Logo Or None?", "retest")
P(G, ("tn_cap_en", "English Captions Only", "Plain English.", "focused", ig(False, "Roselle drying in the sun.")),
     ("tn_cap_thai", "English With A Thai Word", "A Thai word now and then.", "visual", ig(False, "Roselle drying in the sun.", "แดดดี ชอบมาก")), "Captions: English Only Or A Thai Word?", "retest")
P(G, ("tn_gold_lead", "Gold Leads", "Gold buttons, peach accent.", "visual", lead(GOLD, PEACH, "Gold, peach, on rice-white")),
     ("tn_green_lead", "Deep Green Leads", "Green buttons, peach accent.", "focused", lead(DEEP, PEACH, "Deep green, peach, on rice-white")), "Lead Colour: Gold Or Deep Green?", "retest")

# ---------- Retests of Round One Neither / skip cards ----------
R1 = json.load(open(os.path.join(ROOT, "decks/wellnest-brand.json")))
RES = json.load(open(os.path.join(ROOT, "results/wellnest-brand.json")))
ch = {p["pair_id"]: p["choice"] for p in RES["picks"]}
DROP = {"wnr_tg_hub", "wnr_sa_corp", "wnr_sa_letter", "wnr_sa_i"}   # rejected global-family / founder framings: not re-asked
for p in R1["pairs"]:
    if ch.get(p["id"]) not in ("neither", "skip"): continue
    if p["optionA"]["id"] in DROP: continue
    a, b = copy.deepcopy(p["optionA"]), copy.deepcopy(p["optionB"])
    for o in (a, b): o["id"] = "wn2_rt_" + o["id"][4:]
    g = "Retest: " + p["group"]
    add(g, g, a, b, p["ask"], "retest")
for p in pairs:
    if p["purpose"] == "retest": p["retest"] = True

cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
N = len(pairs); print("pairs built:", N, cnt)
publish(DID, "WellNest Brand Deck Round Two", "WellNest", pairs,
        {"brands": ["The WellNest Round Two: new taglines and story angles, Round One Neither/skip retests, three tension retests",
                    "Picked direction: original nest logo, Cormorant + DM Sans, rice-white base, gold leads, peach accent; drawn SVGs, no emoji, Thai only in Thai options"],
         "submit_agent": "wellnest", "submit_to": "WellNest Agent", "section_counts": cnt, "deck_size": N,
         "trim_override": f"{N} pairs: long WellNest deck OK per Max",
         "follows": {"deck": "wellnest-brand", "submission": "35a22b29-9181-4001-8a9d-fa0919bbb203", "answered": 192, "total": 200},
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"results": "/workspace/wellnest/deck-results/2026-10-14-wellnest-brand-deck.md", "rules": "/workspace/wellnest/brand-rules.md"}},
        seed=2027, n=N)
