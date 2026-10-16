#!/usr/bin/env python3
"""Oct 16 2026 (Max): Home Page Trust Tags Deck, 20 this-or-that pairs for the trust chip row on smartupkeep.ai.
Current chips (smart-upkeep app.js `trust`): Certified Techs, Honest Refund, Report Every Visit, Metro Detroit.
Each card = drawn hero mockup (cream, Khand/Hind, terracotta CTA) with the chip row in site chip tints (t0-t3).
Options marked (*) in desc rest on claims the site does not make yet -> need Max's fact check.
Chat to UpKeep, submit_agent upkeep. Slug: descriptive + random letters (queue/upkeep-trust-tags-slugs.json)."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets
from html import escape
from team_kit import deck, publish
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CR, INK, MU, TD = "#FAF6EE", "#0A0A0A", "#6B6560", "#A8432A"
TINT = [("#C1502E1C", TD), ("#05668D1A", "#05668D"), ("#D4A01726", "#7A5A0E"), ("#0B6E4F1A", "#0B6E4F")]
ICON = {"shield": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z" fill="none" stroke="{c}" stroke-width="2"/>',
 "refund": '<path d="M4 12a8 8 0 1 0 3-6.2M4 4v4h4" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
 "clip": '<rect x="6" y="4" width="12" height="17" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M9 10h6M9 14h6" stroke="{c}" stroke-width="2"/>',
 "house": '<path d="M4 11l8-7 8 7v9H4z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
 "check": '<path d="M5 12l5 5 9-10" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>',
 "cal": '<rect x="4" y="5" width="16" height="15" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M4 10h16" stroke="{c}" stroke-width="2"/>',
 "tag": '<path d="M4 4h8l8 8-8 8-8-8z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="8.5" cy="8.5" r="1.5" fill="{c}"/>',
 "pin": '<path d="M12 21s-6-6-6-11a6 6 0 0 1 12 0c0 5-6 11-6 11z" fill="none" stroke="{c}" stroke-width="2"/>'}
def tw(s, fs): return len(s) * fs * .52
def chips(tags, style, y0):
    out, x, y, fs = "", 14, y0, 9
    if style == "grid":
        n = len(tags); w = (212 - (n - 1) * 5) / n
        for i, (t, ic) in enumerate(tags):
            bg, fg = TINT[i % 4]; cx = 14 + i * (w + 5)
            out += f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="44" rx="7" fill="{bg}"/><g transform="translate({cx + w/2 - 7:.1f},{y + 5}) scale(.58)">{ICON[ic].format(c=fg)}</g>'
            words = t.split(); lines = [" ".join(words[:len(words)//2 or 1]), " ".join(words[len(words)//2 or 1:])] if len(t) > 11 else [t]
            for j, ln in enumerate(lines):
                out += f'<text x="{cx + w/2:.1f}" y="{y + 28 + j*9}" font-family="Hind,sans-serif" font-weight="600" font-size="7.6" fill="{fg}" text-anchor="middle">{escape(ln)}</text>'
        return out
    for i, (t, ic) in enumerate(tags):
        bg, fg = TINT[i % 4]
        w = tw(t, fs) + (30 if style != "text" else 18)
        if x + w > 226: x, y = 14, y + 26
        if style == "outline": out += f'<rect x="{x}" y="{y}" width="{w:.1f}" height="21" rx="10.5" fill="#FFFFFF" stroke="{TD}" stroke-width="1"/>'; fg = TD
        elif style == "solid": out += f'<rect x="{x}" y="{y}" width="{w:.1f}" height="21" rx="10.5" fill="{TD}"/>'; fg = "#FFFFFF"
        elif style == "text": fg = INK
        else: out += f'<rect x="{x}" y="{y}" width="{w:.1f}" height="21" rx="10.5" fill="{bg}"/>'
        if style == "text": out += f'<g transform="translate({x},{y + 4}) scale(.55)">{ICON["check"].format(c=TD)}</g>'; tx = x + 16
        else: out += f'<g transform="translate({x + 8},{y + 4}) scale(.55)">{ICON[ic].format(c=fg)}</g>'; tx = x + 23
        out += f'<text x="{tx:.1f}" y="{y + 14}" font-family="Hind,sans-serif" font-weight="600" font-size="{fs}" fill="{fg}">{escape(t)}</text>'
        x += w + 6
    return out
def hero(tags, style="pill", head="Why Trust Us"):
    s = f'<rect width="240" height="300" fill="{CR}"/>'
    s += f'<rect x="0" y="0" width="240" height="34" fill="#FFFFFF"/><circle cx="24" cy="17" r="9" fill="{TD}"/><text x="24" y="21" font-family="Khand,sans-serif" font-weight="700" font-size="11" fill="#FFF" text-anchor="middle">S</text><text x="39" y="21.5" font-family="Khand,sans-serif" font-weight="700" font-size="13" fill="{INK}">Smart Upkeep</text><line x1="0" y1="34" x2="240" y2="34" stroke="#E5E0D8"/>'
    s += f'<rect x="14" y="44" width="212" height="52" rx="8" fill="#05668D22"/><path d="M104 88 V74 L120 62 L136 74 V88 Z" fill="none" stroke="#05668D" stroke-width="2.4" stroke-linejoin="round"/><circle cx="210" cy="86" r="7" fill="#FFFFFFCC"/><path d="M208 83 L213 86 L208 89Z" fill="{INK}"/>'
    s += f'<text x="14" y="120" font-family="Khand,sans-serif" font-weight="700" font-size="21" fill="{INK}">Your Home, Taken Care Of.</text>'
    s += f'<text x="14" y="135" font-family="Hind,sans-serif" font-size="9.5" fill="{MU}">Catch small problems before they&#8217;re big ones.</text>'
    s += f'<text x="14" y="148" font-family="Hind,sans-serif" font-weight="600" font-size="8.5" fill="{TD}">Membership Starting at $99/Month</text>'
    s += f'<rect x="14" y="155" width="212" height="24" rx="12" fill="{TD}"/><text x="120" y="171" font-family="Khand,sans-serif" font-weight="700" font-size="12" fill="#FFF" text-anchor="middle">Get Started</text>'
    s += f'<text x="14" y="200" font-family="Khand,sans-serif" font-weight="700" font-size="12" fill="{INK}">{escape(head)}</text><text x="226" y="200" font-family="Hind,sans-serif" font-weight="600" font-size="8" fill="{TD}" text-anchor="end">How We Vet</text>'
    s += chips(tags, style, 208)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" style="width:100%;height:auto;display:block">{s}<rect x=".5" y=".5" width="239" height="299" rx="2" fill="none" stroke="#E5E0D8"/></svg>'
CT, HR, RV, MD = ("Certified Techs", "shield"), ("Honest Refund", "refund"), ("Report Every Visit", "clip"), ("Metro Detroit", "house")
CUR = [CT, HR, RV, MD]
pairs, O, add = deck("ttg_", "UpKeep")
def P(g, ask, a, b):
    add(g, g, *[O(o[0], o[1], o[2], o[3], hero(o[4], *(o[5:] or []))) for o in (a, b)], ask)
P("Current Vs New", "Keep 'Certified Techs' Or Say 'Insured And Background-Checked'?",
  ("cur_ct", "Certified Techs (Now)", "Today's first chip.", "familiar", CUR),
  ("ins_bg", "Insured And Background-Checked", "Spells out what 'certified' means (site already says both).", "specific", [("Insured, Background-Checked", "shield"), HR, RV, MD]))
P("Wording", "Refund Chip: 'Honest Refund' Or 'Cancel Anytime, No Fee'?",
  ("w_honest", "Honest Refund (Now)", "Current wording.", "warm", CUR),
  ("w_cancel", "Cancel Anytime, No Fee", "Same promise the FAQ makes, in plain words.", "plain", [CT, ("Cancel Anytime, No Fee", "refund"), RV, MD]))
P("Wording", "Refund Chip: 'Honest Refund' Or 'Money-Back Promise'?",
  ("w_honest2", "Honest Refund (Now)", "Current wording.", "warm", CUR),
  ("w_moneyback", "Money-Back Promise", "(*) Sounds like a full refund; site refunds prepaid minus work done. Needs Max's OK.", "bold", [CT, ("Money-Back Promise", "refund"), RV, MD]))
P("Wording", "Report Chip: 'Report Every Visit' Or 'Photo Report Every Visit'?",
  ("w_rep", "Report Every Visit (Now)", "Current wording.", "plain", CUR),
  ("w_photo", "Photo Report Every Visit", "Adds photos, which the site already promises.", "visual", [CT, HR, ("Photo Report Every Visit", "clip"), MD]))
P("Current Vs New", "Fourth Chip: 'Metro Detroit' Or 'Wayne, Oakland, Macomb'?",
  ("cur_md", "Metro Detroit (Now)", "Short area name.", "simple", CUR),
  ("counties", "Wayne, Oakland, Macomb", "Names the three counties the site lists.", "specific", [CT, HR, RV, ("Wayne, Oakland, Macomb", "pin")]))
P("Wording", "Local Chip: 'Metro Detroit' Or 'Local Detroit Team'?",
  ("w_md", "Metro Detroit (Now)", "Where we work.", "simple", CUR),
  ("w_local", "Local Detroit Team", "(*) Implies techs are local staff. Needs Max's OK.", "warm", [CT, HR, RV, ("Local Detroit Team", "pin")]))
P("Theme", "Record Chip: 'Report Every Visit' Or 'Home Record Kept'?",
  ("t_rep", "Report Every Visit (Now)", "About each visit.", "practical", CUR),
  ("t_record", "Home Record Kept", "About the lasting record of your home (site has Home Record).", "lasting", [CT, HR, ("Home Record Kept", "clip"), MD]))
P("Theme", "Pricing Theme: 'One Monthly Price' Or 'No Surprise Fees'?",
  ("t_monthly", "One Monthly Price", "(*) Site says 'Starting at $99/Month'; confirm price is set for the term.", "calm", [CT, ("One Monthly Price", "tag"), RV, MD]),
  ("t_nosurprise", "No Surprise Fees", "(*) Needs Max's OK: add-ons and repairs may cost extra.", "reassuring", [CT, ("No Surprise Fees", "tag"), RV, MD]))
P("Theme", "Swap In Speed: 'Same-Week Visits' Or Keep 'Metro Detroit'?",
  ("t_sameweek", "Same-Week Visits", "(*) Not on the site today. Needs Max's OK.", "quick", [CT, HR, RV, ("Same-Week Visits", "cal")]),
  ("t_keepmd", "Metro Detroit (Now)", "Keep the area chip.", "simple", CUR))
P("Theme", "Seasonal Rhythm: 'Visits Every Season' Or 'Scheduled For You'?",
  ("t_season", "Visits Every Season", "Fall, winter, spring, summer visits.", "steady", [CT, HR, ("Visits Every Season", "cal"), MD]),
  ("t_sched", "Scheduled For You", "We book the visits; you don't have to remember.", "easy", [CT, HR, ("Scheduled For You", "cal"), MD]))
P("Theme", "Vetting Chip: 'Background-Checked Yearly' Or 'License Checked'?",
  ("t_bg", "Background-Checked Yearly", "Site says background checked yearly.", "safe", [("Background-Checked Yearly", "shield"), HR, RV, MD]),
  ("t_lic", "License Checked", "Site says state license checked (avoid 'Licensed in Michigan' unless confirmed).", "official", [("License Checked", "shield"), HR, RV, MD]))
P("Theme", "Protection Chip: 'Insured Techs' Or 'Moisture Scan Every Visit'?",
  ("t_ins", "Insured Techs", "Short, plain safety claim.", "safe", [("Insured Techs", "shield"), HR, RV, MD]),
  ("t_moist", "Moisture Scan Every Visit", "Proof of care: the whole-home mold and moisture scan.", "thorough", [CT, HR, ("Moisture Scan Every Visit", "check"), MD]))
P("Count", "How Many Chips: 3 Or 4?",
  ("c3", "3 Chips", "Drop the area chip; calmer row.", "minimal", [CT, HR, RV]),
  ("c4", "4 Chips (Now)", "Today's row.", "complete", CUR))
P("Count", "How Many Chips: 4 Or 5?",
  ("c4b", "4 Chips (Now)", "Today's row.", "balanced", CUR),
  ("c5", "5 Chips", "Adds 'Cancel Anytime' as its own chip.", "thorough", [CT, HR, RV, MD, ("Cancel Anytime", "refund")]))
P("Style", "Chip Style: Soft Tints Or Terracotta Outline?",
  ("s_tint", "Soft Tints (Now)", "Four gentle brand tints.", "friendly", CUR, "pill"),
  ("s_outline", "Terracotta Outline", "All chips one color, outline only.", "tidy", CUR, "outline"))
P("Style", "Chip Style: Solid Terracotta Or Checkmark Text?",
  ("s_solid", "Solid Terracotta", "Bold filled chips.", "bold", CUR, "solid"),
  ("s_text", "Checkmark Text", "No chips; a check before each line.", "quiet", CUR, "text"))
P("Style", "Chip Shape: Pills Or Badge Tiles (Phone Style)?",
  ("s_pill", "Pills (Now)", "Rounded pills that wrap.", "light", CUR, "pill"),
  ("s_grid", "Badge Tiles", "Four even tiles, icon over text.", "structured", CUR, "grid"))
P("Heading", "Row Heading: 'Why Trust Us' Or 'Our Promise'?",
  ("h_why", "Why Trust Us (Now)", "Current heading.", "direct", CUR, "pill", "Why Trust Us"),
  ("h_promise", "Our Promise", "Softer, promise-style heading.", "warm", CUR, "pill", "Our Promise"))
P("Mix", "Whole Row: Today's Four Or A People-First Row?",
  ("m_now", "Today's Four", "Certified, Refund, Report, Metro Detroit.", "familiar", CUR),
  ("m_people", "People-First Row", "Background-checked, insured, same tech each visit (*) needs Max's OK.", "personal", [("Background-Checked", "shield"), ("Insured", "shield"), ("Same Tech Each Visit", "house"), HR]))
P("Mix", "Whole Row: Proof-First Or Promise-First?",
  ("m_proof", "Proof-First", "Report, Home Record, moisture scan, insured.", "practical", [("Photo Report", "clip"), ("Home Record Kept", "clip"), ("Moisture Scan", "check"), ("Insured Techs", "shield")]),
  ("m_promise", "Promise-First", "Cancel anytime, honest refund, vetted techs, local.", "reassuring", [("Cancel Anytime", "refund"), HR, ("Vetted Techs", "shield"), MD]))
assert len(pairs) == 20, len(pairs)
did, NAME = "upkeep-home-page-trust-tags-deck", "Home Page Trust Tags Deck"
order = [p["ask"] for p in pairs]
publish(did, NAME, "UpKeep", pairs, {"brands": ["Smart Upkeep home page hero trust chips: wording, themes, count, style"], "submit_agent": "upkeep", "topic": did, "deck_size": 20, "board": "upkeep", "audience": "Max", "requested": True}, seed=8400, n=20)
dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"])); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 20
SL = "queue/upkeep-trust-tags-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
if did not in slugs: slugs[did] = "home-page-trust-tags-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]
FIX = ".v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important}body.carding .opt .vis{min-height:0;overflow:visible}"
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hind:wght@400;600&family=Khand:wght@700&display=swap">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
sz = json.load(open("decks/sizes.json")); sz[did] = 20; json.dump(dict(sorted(sz.items())), open("decks/sizes.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
