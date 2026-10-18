#!/usr/bin/env python3
"""UpKeep Full Review decks (Branding, Oct 17 2026 ICT). Max 21:43 ICT: "review all of upkeeps pages/apps and find some things
you think we might need to work on and make fresh decks." Built from ops/brand/upkeep-full-review-2026-10-17.md (screens shot from
the box working copy, smart-upkeep 319e011, and the board's tool pages). Four decks, one theme each (R113), 10 picks each:
  Site: Trust And Launch Dates | Operator Console: Alerts And Test Data | Member App: Account And Empty States |
  Planning Tools: Brand Colours And Layout
Option A = what the code shows now, Option B = one improvement drawn on the same screen. Copy and colours come from the code
(app.js, member/, console/, board funnel/, website-diagram/, info-flow/, value-estimator/). Names, addresses and numbers are
example or TEST data. R105 captions guarded by caption_rule. No Thai references (R110), no emoji, light mode only.
Not re-asked (Job 6 888e752 + queued decks): member header, Did You Know, visit history, open items, trust tags, sign-up form
errors, forecast, pitch, attire, video pop-up, console layout/KPI/member table/phone/map/calendar, Face ID and sign-in link.
Pages written UNLOCKED: lock before commit.   usage: build_upkeep_full_review.py [--preview DIR] [--only KEY]"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets, re
from draft_svg import t, rect, dot, ln, ic, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON, crisp
from team_kit import deck as kdeck, publish, shareic
from uk5_art import mark, wordmark, GREY
import caption_rule
from split_deck import theme_name_ok
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
CREAM = "#FAF6EE"; RED = "#b91c1c"; TEAL = "#0F7C7A"; TERRA2 = "#C8643F"; GOLD = "#D4A017"; GD = "#B97F00"; MUST = "#8a6510"
_n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"
def grad(x, y, w, h, r=0, op=""):
    g = uid("bl")
    return (f'<defs><linearGradient id="{g}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{LAGOON}{op}"/>'
            f'<stop offset="1" stop-color="{TERRA}{op}"/></linearGradient></defs>' + rect(x, y, w, h, f"url(#{g})", "none", r))
def chip(x, y, txt, c, solid=False, h=13, tc=None, fill="#FFFFFF"):
    w = len(txt) * 4.3 + 12
    return rect(x, y, w, h, c if solid else fill, "none" if solid else c, 6.5, .9) + t(x + w / 2, y + h * .7, txt, 7.5, tc or ("#FFFFFF" if solid else c), "hind", 600, "middle"), w
def btn(x, y, w, txt, c=TERRA, solid=True, h=20, tc=None):
    return rect(x, y, w, h, c if solid else "#FFFFFF", "none" if solid else c, 3, 1) + t(x + w / 2, y + h * .66, txt, 7.5, tc or ("#FFFFFF" if solid else c), "hind", 700, "middle", 'letter-spacing=".8"')
def lbl(x, y, s, c=MUTE): return t(x, y, s.upper(), 7.5, c, "hind", 600, extra='letter-spacing="1"')
def row(x, y, w, title, sub="", k=None, c=INK, chev=True, h=26, kc=LAGOON):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 6, 1)
    tx = x + 8
    if k: s += ic(k, x + 7, y + h / 2 - 6, 12, kc, 1.8); tx = x + 25
    s += t(tx, y + (11 if sub else h / 2 + 3), title, 8.5, c, "khand", 700)
    if sub: s += t(tx, y + 21, sub, 7.5, MUTE)
    if chev: s += t(x + w - 8, y + h / 2 + 3, "›", 9, LAGOON, "hind", 600, "end")
    return s
def skel(x, y, w, h): return rect(x, y, w, h, "#EFEBE4", "none", 4)

# ---------------- frames ----------------
def frame(lab, body, accent=TERRA, data="EXAMPLE DATA", H=300):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 {H}" width="240" height="{H}">' + rect(0, 0, 240, H, "#FFFFFF"))
    s += (grad(0, 0, 240, 5) if accent == "blend" else rect(0, 0, 240, 5, accent))
    s += t(12, 21, lab.upper(), 7.5, LAGOON if accent == "blend" else accent, "hind", 600, extra='letter-spacing="1.1"')
    if data:
        w = len(data) * 4.6 + 12
        s += rect(228 - w, 12, w, 12, SAFFRON + "26", SAFFRON, 0, .8) + t(228 - w / 2, 20.6, data, 7.5, "#7A5A0C", "hind", 600, "middle", 'letter-spacing=".5"')
    return crisp(s + body + t(120, H - 3, "Built by Machan", 7.5, GREY, "hind", 400, "middle") + rect(.5, .5, 239, H - 1, "none", "#D6D0C6") + "</svg>")
def phone(inner, bg="#FFFFFF", y=32, h=256):
    cid = uid("ph")
    return (rect(15, y - 4, 210, h + 8, INK, "none", 16) + f'<clipPath id="{cid}"><rect x="20" y="{y}" width="200" height="{h}" rx="12"/></clipPath>'
            + f'<g clip-path="url(#{cid})">' + rect(20, y, 200, h, bg) + inner + "</g>" + rect(104, y - 3, 32, 2.4, "#3a3a3a", "none", 1.2))
def desk(inner, bg="#FFFFFF", y=32, h=250):
    cid = uid("dk")
    return (rect(6, y, 228, h, "#FFFFFF", "#CFC8BC", 6, 1) + rect(6, y, 228, 12, "#F1EEE8", "none", 6) + rect(6, y + 6, 228, 6, "#F1EEE8")
            + dot(13, y + 6, 2, "#E2B4A5") + dot(20, y + 6, 2, "#E7D6A2") + dot(27, y + 6, 2, "#B9D3C4")
            + f'<clipPath id="{cid}"><rect x="7" y="{y+12}" width="226" height="{h-13}"/></clipPath><g clip-path="url(#{cid})">' + rect(7, y + 12, 226, h - 13, bg) + inner + "</g>")

# ================= SITE pieces (smart-upkeep app.js home) =================
def site_head(y, contact=False, desktop=False, links=False):
    if desktop:
        if links:
            s = rect(7, y, 226, 18, "#FFFFFF") + wordmark(14, y + 13, 11, INK, TERRA) + shareic(220, y + 4, INK, 9)
            s += f'<line x1="7" y1="{y+18}" x2="233" y2="{y+18}" stroke="{TERRA}" stroke-dasharray="3 2"/>'
            xs = 84
            for w in ("Plans", "A La Carte", "My Home"):
                s += t(xs, y + 12, w, 7.5, INK, "hind", 600); xs += len(w) * 3.9 + 10
            s += rect(194, y + 4, 22, 11, TERRA, "none", 2) + t(205, y + 11.8, "Quote", 7.5, "#FFFFFF", "hind", 700, "middle")
            return s, 19
        s = rect(7, y, 226, 18, "#FFFFFF") + wordmark(120, y + 13, 11, INK, TERRA, "middle") + shareic(220, y + 4, INK, 9)
        s += f'<line x1="7" y1="{y+18}" x2="233" y2="{y+18}" stroke="{TERRA}" stroke-dasharray="3 2"/>'
        return s, 19
    s = rect(20, y, 200, 24, "#FFFFFF") + wordmark(120, y + 16, 13, INK, TERRA, "middle") + shareic(200, y + 5, INK, 11)
    if contact:
        s += rect(26, y + 5, 40, 14, "#FFFFFF", TERRA, 7, .9) + ic("phone", 29, y + 6, 11, TERRA, 1.6) + t(53, y + 15, "Text Us", 7.5, TERRA, "hind", 700, "middle")
    return s, 24
def site_hero(y, cta="FREE QUOTE IN MINUTES", dates=False):
    s = rect(20, y, 200, 120, "#FBF4EC")
    s += t(30, y + 26, "Your Home,", 17, INK, "khand", 700) + t(30, y + 44, "Taken Care Of.", 17, INK, "khand", 700)
    s += t(30, y + 58, "Catch small problems early.", 8, MUTE)
    s += btn(30, y + 66, 116, cta)
    if dates:
        s += rect(30, y + 92, 180, 18, "#FFFFFF", LINE, 4) + ic("cal", 34, y + 95, 11, TERRA, 1.6)
        s += t(49, y + 104, "Sign-ups open Dec 1 · Visits start Jan 2027", 7.5, INK, "hind", 600)
    else:
        for i, (c, w) in enumerate(((TERRA, "Cancel Anytime"), (LAGOON, "Certified Techs"))):
            s += chip(30 + i * 78, y + 94, w, c)[0]
    return s, 122
def plan_card(x, y, name, price, visits, edge=LAGOON, w=92, h=86, pop=False):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 6, 1) + rect(x, y, w, 3, edge, "none", 1.5)
    if pop: s += rect(x + 6, y + 8, 58, 10, "#FFFFFF", INK, 0, .7) + t(x + 35, y + 15.5, "MOST POPULAR", 7.5, INK, "hind", 600, "middle")
    s += t(x + 6, y + 32, name, 11, INK, "khand", 700) + t(x + 6, y + 50, "From", 7.5, MUTE) + t(x + 24, y + 52, price, 15, INK, "khand", 700) + t(x + 26 + len(price) * 6.4, y + 52, "/Mo", 7.5, MUTE)
    s += t(x + 6, y + 64, f"VISITS PER YEAR: {visits}", 7.5, MUTE, "hind", 600)
    s += t(x + 6, y + 78, "And More", 7.5, LAGOON, "hind", 600, extra='text-decoration="underline"')
    return s
def site_plans(y, edge=LAGOON, head_link="FREE QUOTE IN MINUTES"):
    s = t(28, y + 12, "Plans", 12, INK, "khand", 700) + (t(212, y + 11, head_link, 7.5, INK, "hind", 700, "end", 'letter-spacing=".8"') if head_link else "")
    s += plan_card(28, y + 20, "Essentials", "$99", 2, edge) + plan_card(126, y + 20, "Plus", "$164", 4, edge, pop=True)
    return s, 112
def site_nav(y):
    s = rect(20, y, 200, 30, "#FFFFFF") + ln(y, 20, 220)
    for i, (lab, k) in enumerate((("Home", "home"), ("Plans", "star"), ("A La Carte", "tag"), ("My Home", "card"), ("Account", "heart"))):
        cx = 40 + i * 40; c = TERRA if i == 0 else MUTE
        s += ic(k, cx - 5, y + 4, 10, c, 1.6) + t(cx, y + 25, lab, 7.5, c, "hind", 600, "middle")
    return s
def site_details(y):
    s = t(28, y + 11, "Details", 11, INK, "khand", 700)
    for i, w in enumerate(("What's Included", "Shop A La Carte", "Refund Promise", "FAQ")):
        s += rect(28, y + 17 + i * 19, 184, 17, "#FFFFFF", LINE, 0, 1) + t(36, y + 28 + i * 19, w, 8, INK, "khand", 700) + ic("down", 198, y + 20 + i * 19, 10, LAGOON, 1.6)
    return s, 96
def featured(y):
    return rect(28, y, 184, 30, "#FFFFFF", LINE, 6, 1) + rect(28, y, 3, 30, TERRA) + t(38, y + 11, "FEATURED SERVICE", 7.5, LAGOON, "hind", 600) + t(38, y + 23, "Custom Grass Cutting", 8.5, INK, "khand", 700) + dot(202, y + 15, 6, TERRA), 34
def footer_full(y):
    s = rect(20, y, 200, 120, CREAM) + ln(y, 20, 220, "#E9DFD0") + wordmark(30, y + 18, 12, INK, TERRA)
    s += t(30, y + 30, "Owned and run in Metro Detroit", 7.5, MUTE)
    for i, (k, w) in enumerate((("phone", "Text or call (555) 010-0000"), ("mic", "hello@example.com"), ("home", "Wayne · Oakland · Macomb"))):
        s += ic(k, 30, y + 37 + i * 14, 10, TERRA, 1.6) + t(45, y + 46 + i * 14, w, 7.5, INK, "hind", 500)
    for i, w in enumerate(("FAQ", "Cancel Membership", "Privacy", "Terms")):
        s += t(30 + [0, 22, 104, 142][i], y + 96, w, 7.5, LAGOON, "hind", 600, extra='text-decoration="underline"')
    s += t(30, y + 110, "Example contact details", 7.5, GREY)
    return s, 120

# ================= site picks =================
def S_footer(full):
    y = 32; s = ""
    g, h = site_head(y); s += g; y += h
    g, h = site_details(y + 4); s += g; y += h + 6
    g, h = featured(y); s += g; y += h + 4
    if full: s += footer_full(y)[0]
    else: s += rect(20, y, 200, 120, "#FFFFFF") + t(120, y + 50, "(page ends here)", 7.5, GREY, "hind", 400, "middle")
    s += site_nav(258)
    return frame("Home: bottom of page", phone(s))
def S_dates(on):
    y = 32; s = ""; g, h = site_head(y); s += g; y += h
    g, h = site_hero(y, dates=on); s += g; y += h + 4
    s += site_plans(y)[0] + site_nav(258)
    return frame("Home: hero", phone(s))
def S_cta(one):
    lab_p = "GET MY FREE QUOTE" if one else "FREE QUOTE IN MINUTES"
    y = 32; s = ""; g, h = site_head(y); s += g; y += h
    g, h = site_hero(y, cta=lab_p); s += g; y += h
    s += t(28, y + 14, "Plans", 12, INK, "khand", 700) + t(212, y + 13, lab_p, 7.5, INK, "hind", 700, "end", 'letter-spacing=".8"')
    s += rect(28, y + 22, 184, 60, "#FFFFFF", LINE, 6, 1) + t(36, y + 36, "Quote: Chapter 1 of 3", 9, INK, "khand", 700) + t(36, y + 48, "How big is your home?", 7.5, MUTE)
    s += t(120, y + 74, "Get My Free Quote · Tailored To Your Home" if one else "Free Offer in Minutes · Tailored to Your Home", 7.5, MUTE, "hind", 500, "middle")
    s += rect(20, 258, 200, 30, "#FFFFFF") + ln(258, 20, 220) + btn(30, 263, 180, "GET MY FREE QUOTE" if one else "GET STARTED")
    return frame("Home: main button", phone(s))
def S_desknav(top):
    y = 44; s = ""; g, h = site_head(y, desktop=True, links=top); s += g; y += h + 6
    s += rect(14, y, 212, 66, "#FBF4EC", "none", 2) + t(22, y + 20, "Your Home, Taken Care Of.", 14, INK, "khand", 700) + t(22, y + 33, "Catch small problems before they're big ones.", 7.5, MUTE)
    s += btn(22, y + 41, 70, "GET STARTED", h=16); y += 74
    s += t(14, y + 9, "Plans", 10, INK, "khand", 700)
    for i, (n, p) in enumerate((("Essentials", "$99"), ("Plus", "$164"), ("Complete", "$312"))):
        x = 14 + i * 72
        s += rect(x, y + 14, 66, 70, "#FFFFFF", LINE, 4) + rect(x, y + 14, 66, 2.5, LAGOON) + t(x + 5, y + 30, n, 9, INK, "khand", 700) + t(x + 5, y + 46, "From " + p + "/Mo", 7.5, INK, "hind", 600) + t(x + 5, y + 58, "Visits a year", 7.5, MUTE)
    if not top:
        bx = 62; by = y + 46
        s += rect(bx, by, 116, 26, "#FFFFFF", LINE, 2, 1) + rect(bx, by, 22, 2, TERRA)
        for i, w in enumerate(("Home", "Plans", "A La C.", "My Home", "Acct")):
            s += t(bx + 11 + i * 23.5, by + 18, w, 7.5, TERRA if i == 0 else MUTE, "hind", 600, "middle")
    return frame("Home at 1280: navigation", desk(s, y=32, h=240))
def S_edge(c):
    y = 32; s = ""; g, h = site_head(y); s += g; y += h + 4
    g, h = site_plans(y, edge=c); s += g; y += h
    s += t(28, y + 12, "What We Take Care Of", 10, INK, "khand", 700) + rect(28, y + 18, 120, 40, "#FFFFFF", LINE, 6) + t(36, y + 32, "Water", 8.5, LAGOON, "khand", 700) + t(36, y + 46, "Water Heater", 7.5, INK)
    s += site_nav(258)
    return frame("Home: plan cards", phone(s))
def S_owner(on):
    y = 32; s = ""; g, h = site_head(y); s += g; y += h + 4
    s += t(28, y + 11, "Why Trust Us", 11, INK, "khand", 700) + t(212, y + 10, "HOW WE VET", 7.5, INK, "hind", 700, "end")
    s += chip(28, y + 18, "Home Reports", TERRA)[0] + chip(96, y + 18, "Licensed & Insured", LAGOON)[0]; y += 38
    if on:
        s += rect(28, y, 184, 62, CREAM, "none", 8) + dot(50, y + 24, 15, TERRA) + t(50, y + 29, "MW", 11, "#FFFFFF", "khand", 700, "middle")
        s += t(72, y + 17, "Owned And Run Locally", 10, INK, "khand", 700) + t(72, y + 29, "Max Weberman, founder", 7.5, MUTE)
        s += t(72, y + 41, "Questions go to a real person,", 7.5, INK) + t(72, y + 51, "not a call centre.", 7.5, INK)
        y += 68
    g, h = site_details(y); s += g
    s += site_nav(258)
    return frame("Home: who is behind it", phone(s))
def S_sample(on):
    y = 32; s = ""; g, h = site_head(y); s += g; y += h
    g, h = site_hero(y); s += g; y += h + 2
    if on:
        s += rect(28, y, 184, 44, "#FFFFFF", LINE, 6, 1) + rect(34, y + 6, 24, 32, CREAM, LINE, 2) + ln(y + 14, 38, 54) + ln(y + 20, 38, 54) + ln(y + 26, 38, 50)
        s += t(66, y + 17, "See A Sample Home Report", 9, INK, "khand", 700) + t(66, y + 29, "What you get after every visit", 7.5, MUTE) + t(204, y + 25, "›", 10, LAGOON, "hind", 600, "end")
        y += 50
    s += site_plans(y)[0] + site_nav(258)
    return frame("Home: proof before sign-up", phone(s))
def S_cancel(fixed):
    y = 32; s = ""
    g, h = site_head(y); s += g; y += h + 4
    w = 184 if fixed else 226
    s += rect(28, y, w, 8 + (166 if fixed else 110), "#FFFFFF", LINE, 0, 1)
    s += t(36, y + 20, "Cancel Membership", 14, INK, "khand", 700)
    s += t(36, y + 34, "No fee, no phone call needed. Your refund is", 7.5, INK) + t(36, y + 44, "what you prepaid minus services already done.", 7.5, INK)
    s += lbl(36, y + 60, "Email on your membership") + rect(36, y + 64, w - 16, 18, "#FFFFFF", "#CFC6B4")
    if fixed:
        s += lbl(36, y + 98, "What happens next")
        for i, w2 in enumerate(("We email your refund math today", "Visits stop on your end date", "Refund lands in 5 to 10 days")):
            s += dot(41, y + 108 + i * 13, 4.5, TERRA) + t(41, y + 110.5 + i * 13, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle") + t(50, y + 111 + i * 13, w2, 7.5, INK)
        s += btn(36, y + 148, 168, "CANCEL MY MEMBERSHIP")
    else:
        s += btn(36, y + 88, w - 16, "CANCEL MY MEMBERSHIP")
        s += t(36, y + 130, "Page is 488px wide on a 393 phone:", 7.5, RED, "hind", 600) + t(36, y + 140, "it scrolls sideways.", 7.5, RED, "hind", 600)
    return frame("Cancel Membership page", phone(s))
def S_faq(new):
    y = 32; s = ""
    s += rect(20, y, 200, 24, "#FFFFFF") + rect(26, y + 5, 34, 14, "#F3F1EC", LINE, 7) + t(43, y + 15, "Back", 7.5, INK, "hind", 600, "middle"); y += 26
    s += t(28, y + 16, "Frequently Asked Questions", 13, INK, "khand", 700); y += 24
    if new:
        s += rect(28, y, 184, 18, "#FFFFFF", "#CFC6B4", 9) + ic("search", 33, y + 3, 11, MUTE, 1.6) + t(48, y + 12, "Search questions", 7.5, MUTE); y += 24
        s += lbl(28, y + 8, "Top questions"); y += 12
        for q in ("When do visits start?", "Can I cancel anytime?", "Which areas do you serve?"):
            s += rect(28, y, 184, 18, "#FFFFFF", LINE) + t(34, y + 12, q, 8, INK, "khand", 700) + ic("down", 198, y + 3, 10, LAGOON, 1.6); y += 20
        s += rect(28, y + 4, 184, 30, CREAM, "none", 6) + t(36, y + 17, "Still have a question?", 8.5, INK, "khand", 700) + t(36, y + 28, "Text the team, we reply the same day.", 7.5, MUTE)
    else:
        s += t(28, y + 10, "Heating, Cooling and Furnace Filters", 9, INK, "khand", 700); y += 14
        for q in ("How often should I change my furnace filter?", "How often does a furnace need a tune-up?", "How often should my AC be serviced?"):
            s += t(32, y + 9, q, 7.5, LAGOON, "hind", 600); y += 13
        for c in ("Safety Checks", "Water, Gutters and Michigan Winters", "Plans and Visits", "Our Techs and Service Area", "Billing, Cancel and Moving"):
            s += rect(28, y + 2, 184, 16, "#FFFFFF", LINE) + t(34, y + 13, c, 8, INK, "khand", 700); y += 18
    s += rect(20, 258, 200, 30, "#FFFFFF") + ln(258, 20, 220) + btn(30, 263, 180, "GET STARTED")
    return frame("FAQ page", phone(s))
def S_contact(on):
    y = 32; s = ""; g, h = site_head(y, contact=on); s += g; y += h
    g, h = site_hero(y); s += g; y += h + 4
    s += site_plans(y)[0] + site_nav(258)
    return frame("Home: header", phone(s))

# ================= CONSOLE pieces (console/index.html) =================
def con_head(y, test="three", banner=False):
    s = rect(7, y, 226, 16, "#FFFFFF") + wordmark(120, y + 12, 10, INK, TERRA, "middle") + shareic(220, y + 3, INK, 9) + grad(7, y + 16, 226, 1.6)
    y += 20
    s += t(14, y + 14, "Operator Console", 15, INK, "khand", 700)
    s += t(14, y + 26, "Everything members, techs and the site send in.", 7.5, MUTE)
    b = y + 31
    if test == "three":
        s += rect(14, b, 34, 14, "#FFFFFF", INK, 3) + t(31, b + 9.5, "Refresh", 7.5, INK, "hind", 600, "middle")
        s += rect(52, b, 66, 14, "#FFFFFF", INK, 3) + t(85, b + 9.5, "Load Test Data", 7.5, INK, "hind", 600, "middle")
        s += rect(122, b, 98, 14, "#FFFFFF", INK, 3) + t(171, b + 9.5, "Clear Live Test Events", 7.5, INK, "hind", 600, "middle")
    else:
        s += rect(14, b, 34, 14, "#FFFFFF", INK, 3) + t(31, b + 9.5, "Refresh", 7.5, INK, "hind", 600, "middle")
        s += rect(52, b, 40, 14, "#FFFFFF", LINE, 3) + t(67, b + 9.5, "Test", 7.5, MUTE, "hind", 600, "middle") + ic("down", 79, b + 2.5, 9, MUTE, 1.5)
    y += 49
    if banner:
        s += rect(7, y, 226, 14, SAFFRON + "22") + rect(7, y, 3, 14, SAFFRON) + t(14, y + 10, "TEST DATA: every row below is sample data", 7.5, "#5C4408", "hind", 600); y += 18
    return s, y
ALERTS = [("Safety Escalation", "Casey Test · Gas smell", "12m ago", "9:32 PM", "safety"),
          ("Visit Request", "Finley Sample · Dripping under kitchen sink", "20m ago", "9:24 PM", "info"),
          ("Moisture Reading: Wet", "Avery Example · Basement corner 24%", "40m ago", "9:04 PM", "watch"),
          ("Missed Check-In", "Gray Example · Sam Demo", "55m ago", "8:49 PM", "watch"),
          ("Failed Payment", "Emery Mock · Card declined", "3h ago", "6:44 PM", "bill")]
SEV = {"safety": (RED, "Safety"), "watch": (TERRA, "Watch"), "bill": (MUST, "Billing"), "info": (LAGOON, "Info")}
def alerts(y, sev=False, actions=False, tags=True, clock=False, n=5):
    s = rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Live Alerts", 11, INK, "khand", 700) + dot(206, y + 9, 6, RED) + t(206, y + 12, str(n), 7.5, "#FFFFFF", "hind", 700, "middle")
    y += 20
    items = ALERTS[:n]
    if sev: items = sorted(items, key=lambda a: ["safety", "watch", "bill", "info"].index(a[4]))
    for ti, sub, ago, clk, kind in items:
        c = SEV[kind][0] if sev else RED
        h = 40 if actions else 28
        s += rect(10, y, 220, h, "#FFFFFF", LINE) + rect(14, y + 3, 2.5, h - 6, c if sev else (TERRA2 if kind != "watch" else "#2E6F86")) + dot(22, y + 10, 2.6, c)
        s += t(28, y + 12, ti, 8.5, INK, "khand", 700)
        x2 = 28 + len(ti) * 4.3 + 4
        if sev: s += chip(x2, y + 4, SEV[kind][1], c, h=11)[0]
        elif tags: s += chip(x2, y + 4, "SAMPLE", MUTE, h=11)[0]
        s += t(28, y + 23, sub, 7.5, MUTE)
        s += t(224, y + 12, (clk + " · " + ago) if clock else ago, 7.5, MUTE, "hind", 400, "end")
        if actions:
            for i, w in enumerate(("Acknowledge", "Assign", "Resolve")):
                bx = 28 + [0, 56, 92][i]; bw = [52, 32, 36][i]
                s += rect(bx, y + 27, bw, 11, "#FFFFFF" if i < 2 else JUNGLE, LINE if i < 2 else "none", 3) + t(bx + bw / 2, y + 35, w, 7.5, INK if i < 2 else "#FFFFFF", "hind", 600, "middle")
        y += h
    return s, y
def C_frame(lab, body): return frame(lab, desk(body, y=30, h=258), "blend", "TEST DATA")
def C_sev(on):
    s, y = con_head(42); g, y = alerts(y + 2, sev=on); return C_frame("Console: Live Alerts", s + g)
def C_actions(on):
    s, y = con_head(42); g, y = alerts(y + 2, actions=on, n=4); return C_frame("Console: alert actions", s + g)
def C_dupes(once):
    s, y = con_head(42); y += 2
    s += rect(10, y, 108, 16, "#FFFFFF", LINE, 4) + t(16, y + 11, "Live Alerts", 9, INK, "khand", 700)
    s += rect(122, y, 108, 16, "#FFFFFF", LINE, 4) + t(128, y + 11, "Requests And Bookings", 9, INK, "khand", 700)
    yy = y + 18
    def item(x, y, hl=True):
        return rect(x, y, 108, 26, "#FFF4EF" if hl else "#FFFFFF", TERRA if hl else LINE, 3) + t(x + 5, y + 10, "Visit Request", 8, INK, "khand", 700) + t(x + 5, y + 20, "Finley Sample · kitchen sink", 7.5, MUTE)
    if once:
        s += item(10, yy) + rect(122, yy, 108, 26, "#FFFFFF", LINE, 3) + t(127, yy + 10, "Add-On Order", 8, INK, "khand", 700) + t(127, yy + 20, "Jordan Sample", 7.5, MUTE)
        s += rect(10, yy + 30, 108, 14, "#FFFFFF", LINE, 3) + t(15, yy + 40, "Also in Requests ›", 7.5, LAGOON, "hind", 600)
    else:
        s += item(10, yy) + item(122, yy)
    yy += 52
    s += rect(10, yy, 220, 16, "#FFFFFF", LINE, 4) + t(16, yy + 11, "Activity Feed", 9, INK, "khand", 700); yy += 18
    if not once: s += item(10, yy)
    for i, (a, b) in enumerate((("Add-On Click", "site"), ("Quote Generated", "site"), ("Site Visit", "site"))):
        ry = yy + (28 if not once else 0) + i * 18
        s += rect(10, ry, 220, 16, "#FFFFFF", LINE) + t(16, ry + 11, a, 8, INK, "khand", 700) + t(224, ry + 11, b, 7.5, MUTE, "hind", 400, "end")
    if not once: s += t(120, 270, "Same request shows 3 times", 7.5, RED, "hind", 600, "middle")
    return C_frame("Console: repeated items", s)
def C_tags(banner):
    s, y = con_head(42, banner=banner); g, y = alerts(y + 2, tags=not banner, n=4); return C_frame("Console: sample tags", s + g)
def C_testbtn(menu):
    s, y = con_head(42, test="menu" if menu else "three")
    for i, (v, l) in enumerate((("5", "Live Alerts"), ("5", "Visits Today"), ("3", "Open Requests"))):
        s += rect(10 + i * 75, y + 4, 70, 30, "#FFFFFF", RED if i == 0 else LINE, 5) + t(16 + i * 75, y + 20, v, 13, RED if i == 0 else INK, "khand", 700) + t(16 + i * 75, y + 30, l, 7.5, MUTE)
    g, _ = alerts(y + 40, n=3); s += g
    if menu:
        s += rect(52, 125, 100, 50, "#FFFFFF", LINE, 4, 1) + t(58, 138, "Load Test Data", 7.5, INK, "hind", 600) + t(58, 152, "Clear Live Test Events", 7.5, INK, "hind", 600) + t(58, 167, "Test data is on", 7.5, JUNGLE, "hind", 600)
    return C_frame("Console: header buttons", s)
def C_empty(calm):
    s, y = con_head(42); y += 2
    s += rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Live Alerts", 11, INK, "khand", 700) + t(206, y + 13, "0", 8, MUTE, "hind", 700, "middle"); y += 22
    if calm:
        s += rect(10, y, 220, 58, CREAM, "none", 8) + ic("check", 22, y + 14, 22, JUNGLE, 2.2)
        s += t(52, y + 24, "All Clear", 13, INK, "khand", 700) + t(52, y + 36, "No alerts right now. Last one closed 8:49 PM.", 7.5, MUTE) + t(52, y + 48, "Next visit 9:00 AM · Alex Sample", 7.5, LAGOON, "hind", 600)
    else:
        s += rect(10, y, 220, 58, "#FFFFFF", LINE)
    y += 64
    s += rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Today", 11, INK, "khand", 700) + ic("down", 210, y + 4, 10, INK, 1.6)
    return C_frame("Console: no alerts", s)
def C_launch(on):
    s, y = con_head(42); y += 2
    if on:
        s += rect(10, y, 220, 60, "#FFFFFF", LINE, 6) + grad(10, y, 220, 3, 0)
        s += t(18, y + 16, "Launch Readiness", 11, INK, "khand", 700) + chip(180, y + 6, "TEST", SAFFRON, tc="#7A5A0C")[0]
        for i, (v, l, c) in enumerate((("45 days", "to sign-ups, Dec 1", TERRA), ("76 days", "to first visits, Jan 1", LAGOON), ("12", "waitlist homes", JUNGLE))):
            x = 18 + i * 72
            s += t(x, y + 36, v, 12, c, "khand", 700) + t(x, y + 48, l, 7.5, MUTE)
        y += 66
    for i, (v, l) in enumerate((("5", "Live Alerts"), ("5", "Visits Today"), ("6", "Active Members"))):
        s += rect(10 + i * 74, y, 70, 30, "#FFFFFF", RED if i == 0 else LINE, 5) + t(16 + i * 74, y + 16, v, 13, RED if i == 0 else INK, "khand", 700) + t(16 + i * 74, y + 26, l, 7.5, MUTE)
    g, _ = alerts(y + 36, n=3 if on else 5); s += g
    return C_frame("Console: top of page", s)
def C_zips(grouped):
    s, y = con_head(42); y += 2
    s += rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Sales Funnel", 11, INK, "khand", 700); y += 22
    for i, (v, l) in enumerate((("8", "Site Visits"), ("4", "Quotes Started"), ("1", "Sign-Ups"))):
        s += t(18 + i * 72, y + 14, v, 13, INK, "khand", 700) + t(18 + i * 72, y + 24, l, 7.5, MUTE)
    y += 32
    s += lbl(18, y + 8, "Waitlist ZIPs"); y += 14
    if grouped:
        for i, (z, n, w) in enumerate((("48170", 2, 80), ("48197", 1, 40), ("48105", 1, 40))):
            s += t(18, y + 10 + i * 16, z, 8.5, INK, "khand", 700) + rect(52, y + 3 + i * 16, w, 8, LAGOON + "33", LAGOON, 3, .6) + t(58 + w, y + 10 + i * 16, f"{n} home" + ("s" if n > 1 else ""), 7.5, MUTE)
        s += t(18, y + 58, "Outside Wayne, Oakland and Macomb", 7.5, MUTE)
    else:
        for i, z in enumerate(("48170", "48197", "48105", "48170")):
            s += t(18, y + 10 + i * 13, z, 8.5, INK, "hind", 500)
        s += t(60, y + 49, "48170 is listed twice", 7.5, RED, "hind", 600)
    return C_frame("Console: Sales Funnel", s)
def C_place(muted):
    s, y = con_head(42); y += 2
    s += rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Revenue And Billing", 11, INK, "khand", 700); y += 22
    tiles = [("$1,150", "MRR, active members (TEST)", True), ("Placeholder", "Prepaid Balance", False), ("1", "Refunds Due (TEST)", True), ("1", "Failed Cards (TEST)", True)]
    def tile(x, yy, v, l, real, need):
        r = rect(x, yy, 108, 36, "#F6F4F0" if (muted and not real) else "#FFFFFF", LINE, 5)
        if muted and not real: return r + t(x + 7, yy + 16, "Not connected yet", 8.5, MUTE, "khand", 700) + t(x + 7, yy + 29, need, 7.5, MUTE)
        return r + t(x + 7, yy + 18, v, 13, INK, "khand", 700) + t(x + 7, yy + 29, l, 7.5, MUTE)
    for i, (v, l, real) in enumerate(tiles):
        s += tile(10 + (i % 2) * 112, y + (i // 2) * 40, v, l, real, "Prepaid Balance, needs billing")
    y += 86
    s += rect(10, y, 220, 18, "#FFFFFF", LINE, 6) + t(18, y + 13, "Metrics", 11, INK, "khand", 700); y += 22
    s += tile(10, y, "20 min", "Avg Response (TEST)", True, "") + tile(122, y, "Placeholder", "NPS And Reviews", False, "NPS, starts after visits")
    return C_frame("Console: Revenue And Metrics", s)
def C_time(clock):
    s, y = con_head(42); g, y = alerts(y + 2, clock=clock, n=5); return C_frame("Console: alert times", s + g)

# ================= MEMBER pieces (member/index.html) =================
def m_head(y, test="pill"):
    s = ""
    if test == "pill":
        s += rect(20, y, 200, 14, CREAM) + rect(30, y + 1.5, 180, 11, "#FFFFFF", RED, 5.5, .8) + t(120, y + 9.6, "Client 1 · Test Data · fake person, real address", 7.5, RED, "hind", 600, "middle"); y += 14
    s += rect(20, y, 200, 22, "#FFFFFF") + shareic(28, y + 5, INK, 11) + wordmark(120, y + 15, 11, INK, GREY, "middle") + dot(206, y + 11, 8, TERRA) + t(206, y + 14.5, "A", 9, "#FFFFFF", "khand", 700, "middle")
    if test == "chip": s += rect(160, y + 6, 26, 10, "#F1EEE8", "none", 5) + t(173, y + 13.5, "TEST", 7.5, MUTE, "hind", 600, "middle")
    s += rect(20, y + 22, 200, 2, TERRA)
    return s, y + 24
def m_nav(cur=0):
    y = 258; s = rect(20, y, 200, 30, "#FFFFFF") + ln(y, 20, 220)
    for i, (lab, k) in enumerate((("Home", "home"), ("Visits", "cal"), ("Record", "card"), ("Plan", "tag"), ("More", "star"))):
        cx = 40 + i * 40; c = TERRA if i == cur else MUTE
        s += ic(k, cx - 5, y + 4, 10, c, 1.6) + t(cx, y + 25, lab, 7.5, c, "hind", 600, "middle")
    return s
def m_house(y, h=46):
    cid = uid("mh")
    s = f'<clipPath id="{cid}"><rect x="20" y="{y}" width="200" height="{h}"/></clipPath><g clip-path="url(#{cid})">' + rect(20, y, 200, h, "#CFE0E8") + rect(20, y + h * .7, 200, h * .3, "#B9D2A8")
    s += rect(70, y + h * .3, 100, h * .5, "#B8654A") + f'<path d="M64 {y+h*.32} L120 {y+4} L176 {y+h*.32} Z" fill="#6E5E55"/>' + rect(134, y + h * .5, 30, h * .3, "#F2EFEA")
    s += "</g>" + rect(20, y + h - 15, 200, 15, "#00000070") + t(28, y + h - 4, "5439 Example Village Drive", 9, "#FFFFFF", "khand", 700)
    return s, h
def m_title(y):
    return t(28, y + 16, "Alina Example", 13, INK, "khand", 700) + chip(106, y + 6, "Plus", TERRA, True)[0], 22
def m_actions(y):
    s = ""
    for i, w in enumerate(("Book", "Message Tech", "My Add-Ons")):
        x = 26 + i * 64
        s += rect(x, y, 60, 16, "#FFFFFF", TERRA, 8, .9) + t(x + 30, y + 11, w, 7.5, INK, "hind", 600, "middle")
    return s, 20
def m_page(parts, cur=0, test="pill", bg=CREAM):
    y = 32; s = ""; g, y = m_head(y, test); s += g; y += 2
    for f in parts:
        g, h = f(y); s += g; y += h
    return phone(s + m_nav(cur), bg)
def M_more(full):
    def body(y):
        s = lbl(28, y + 12, "Account") + rect(26, y + 16, 2, 14, INK) + t(32, y + 28, "More", 14, INK, "khand", 700); y += 34
        if not full:
            return s + row(28, y, 184, "Profile", "Address, contact, notifications, Refer", "heart", h=30), 200
        groups = [("Account", [("Profile", "Address and contact", "heart"), ("Notifications", "Visit reminders, reports", "clock")]),
                  ("Help", [("Message The Team", "Same-day reply", "phone"), ("Refer A Neighbor", "1 month free each", "star")]),
                  ("", [("Sign Out", "", "x")])]
        for g, rows in groups:
            if g: s += lbl(28, y + 8, g); y += 11
            for ti, sub, k in rows:
                s += row(28, y, 184, ti, sub, k, h=24 if sub else 18, chev=bool(sub)); y += (26 if sub else 20)
        return s, 200
    return frame("Member app: More tab", m_page([body], cur=4))
def M_cancel(on):
    def body(y):
        s = lbl(28, y + 12, "Membership") + t(28, y + 28, "Plan & Billing", 14, INK, "khand", 700); y += 34
        s += rect(28, y, 184, 50, "#FFFFFF", LINE, 6) + lbl(36, y + 12, "Current plan") + t(36, y + 26, "Plus · 4 Visits a Year", 10, INK, "khand", 700) + t(36, y + 38, "Annual · renews Jan 2028 (example)", 7.5, MUTE); y += 56
        s += rect(28, y, 184, 34, "#FFFFFF", LINE, 6) + lbl(36, y + 12, "Payment") + t(36, y + 26, "Card ending 0000 (example)", 8, INK); y += 40
        s += row(28, y, 184, "Pause My Plan", "", "clock", h=18); y += 22
        if on:
            s += t(28, y + 18, "Cancel Membership", 8, MUTE, "hind", 600, extra='text-decoration="underline"') + t(28, y + 29, "One step, online, no call needed", 7.5, GREY)
        return s, 200
    return frame("Member app: Plan & Billing", m_page([body], cur=3))
def M_first(new):
    def body(y):
        g, h = m_house(y); s = g; y += h + 2
        s += m_title(y)[0]; y += 22
        s += m_actions(y)[0]; y += 22
        s += rect(26, y, 188, 92, "#FFFFFF", LINE, 8)
        if not new:
            s += lbl(34, y + 12, "Next visit") + t(34, y + 26, "Winter Visit", 11, INK, "khand", 700)
            s += t(34, y + 39, "Monday, Feb 15, 2027, 8:00 to 9:00 AM", 7.5, INK, "hind", 600) + dot(44, y + 60, 10, TERRA) + t(44, y + 63.5, "DW", 8, "#FFFFFF", "khand", 700, "middle")
            s += lbl(60, y + 55, "Who's coming") + t(60, y + 67, "Dana", 9, INK, "khand", 700) + chip(34, y + 74, "EPA 608", TERRA)[0] + chip(80, y + 74, "OSHA 10", TERRA)[0]
        else:
            s += rect(26, y, 3, 92, TERRA) + lbl(34, y + 12, "Welcome to Smart Upkeep") + t(34, y + 26, "Your First Visit: January 2027", 11, INK, "khand", 700)
            s += t(34, y + 38, "We email your day and window 2 weeks before.", 7.5, MUTE)
            for i, (w, ok) in enumerate((("Plan chosen and paid", True), ("Add photos of your equipment", False), ("Tell us how to get in", False))):
                yy = y + 48 + i * 13
                s += (rect(34, yy, 9, 9, JUNGLE, "none", 2) if ok else rect(34, yy, 9, 9, "#FFFFFF", "#BDB6AA", 2, 1)) + t(48, yy + 7.5, w, 7.5, MUTE if ok else INK, "hind", 500)
        return s, 200
    return frame("Member app: Home", m_page([body]))
def M_record(new):
    def body(y):
        s = lbl(28, y + 12, "Home record") + t(28, y + 28, "Your Appliances", 14, INK, "khand", 700); y += 34
        if not new:
            for ti, sub, note in (("Gas Furnace · Trane", "Installed 2016 · Checked Oct 2026", "Condition: Fair"), ("Central AC · Goodman", "Installed 2008 · Checked Oct 2026", "Plan Replacement"), ("Water Heater · Navien", "Installed 2012 · Checked Oct 2026", "Condition: Fair")):
                s += rect(28, y, 184, 40, "#FFFFFF", LINE, 6) + t(36, y + 13, ti, 9, INK, "khand", 700) + t(36, y + 24, sub, 7.5, MUTE) + t(36, y + 35, note, 7.5, TERRA if "Plan" in note else MUTE, "hind", 600); y += 44
            s += t(28, y + 10, "Checked Oct 2026 is before visits start", 7.5, RED, "hind", 600)
        else:
            s += rect(28, y, 184, 88, CREAM, "#EFE3D3", 8) + ic("card", 108, y + 8, 24, TERRA, 1.8)
            s += t(120, y + 46, "Your Record Starts At Your First Visit", 9.5, INK, "khand", 700, "middle") + t(120, y + 58, "Your tech logs every appliance in January.", 7.5, MUTE, anchor="middle")
            s += btn(66, y + 66, 108, "ADD PHOTOS NOW", TERRA, False, h=15); y += 94
            s += lbl(28, y + 8, "What we will log") + t(28, y + 20, "Furnace · AC · Water heater · Detectors", 7.5, INK)
        return s, 200
    return frame("Member app: Record", m_page([body], cur=2))
def M_signin(err):
    s = rect(20, 32, 200, 256, CREAM) + rect(30, 56, 180, 200, "#FFFFFF", "#e6dfd1")
    s += chip(40, 66, "Prototype, sample data", MUTE)[0] + t(40, 96, "Member Sign In", 16, INK, "khand", 700)
    s += t(40, 112, "Email", 7.5, INK, "hind", 600) + rect(40, 116, 160, 20, "#fffdf8", RED if err else "#cfc6b4", 0, 1.2 if err else 1)
    if err: s += t(40, 146, "Enter the email on your membership.", 7.5, RED, "hind", 600)
    yy = 156 if err else 148
    s += t(40, yy, "Password", 7.5, INK, "hind", 600) + rect(40, yy + 4, 160, 20, "#fffdf8", RED if err else "#cfc6b4", 0, 1.2 if err else 1)
    if err: s += t(40, yy + 34, "Enter your password.", 7.5, RED, "hind", 600)
    b = yy + (40 if err else 32)
    s += rect(40, b, 160, 20, INK) + t(120, b + 13, "SIGN IN", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    s += t(120, b + 32, "Forgot password?", 7.5, LAGOON, "hind", 600, "middle")
    if not err: s += t(120, 246, "Empty fields sign in with no message", 7.5, RED, "hind", 600, "middle")
    return frame("Member app: Sign In", phone(s, CREAM))
def M_loading(sk):
    def body(y):
        if not sk: return rect(20, y, 200, 220, CREAM) + t(120, y + 100, "(blank while loading)", 7.5, GREY, "hind", 400, "middle"), 200
        s = skel(20, y, 200, 46) + skel(28, y + 52, 110, 12) + skel(28, y + 72, 56, 14) + skel(90, y + 72, 56, 14) + skel(152, y + 72, 56, 14)
        s += rect(26, y + 94, 188, 70, "#FFFFFF", LINE, 8) + skel(34, y + 104, 50, 7) + skel(34, y + 118, 120, 10) + skel(34, y + 136, 150, 7) + skel(34, y + 148, 90, 7)
        return s, 200
    return frame("Member app: Home loading", m_page([body]))
def M_offline(on):
    def body(y):
        s = ""
        if on:
            s += rect(20, y, 200, 24, SAFFRON + "22") + rect(20, y, 3, 24, SAFFRON) + ic("clock", 26, y + 6, 11, "#7A5A0C", 1.6)
            s += t(41, y + 10, "Can't reach Smart Upkeep right now.", 7.5, "#5C4408", "hind", 600) + t(41, y + 20, "Showing what was saved at 8:12 AM.", 7.5, "#5C4408"); y += 26
        g, h = m_house(y, 40); s += g; y += h + 2
        s += m_title(y)[0]; y += 22
        s += rect(26, y, 188, 60, "#FFFFFF", LINE, 8) + lbl(34, y + 12, "Next visit") + t(34, y + 26, "Winter Visit", 11, INK, "khand", 700) + t(34, y + 39, "Window Jan 12 to Feb 26, 2027", 7.5, INK)
        s += t(34, y + 52, "Requests send when you are back online" if on else "Request A Visit fails with no message", 7.5, MUTE if on else RED, "hind", 600)
        return s, 200
    return frame("Member app: no connection", m_page([body]))
def M_payfail(on):
    def body(y):
        g, h = m_house(y, 40); s = g; y += h + 2
        s += m_title(y)[0]; y += 22
        if on:
            s += rect(26, y, 188, 40, "#FFF4EF", TERRA, 6, 1) + t(34, y + 15, "Your card was declined", 9, INK, "khand", 700) + t(34, y + 28, "Update it by Jan 5 to keep your visit.", 7.5, MUTE)
            s += btn(156, y + 10, 52, "UPDATE", h=16); y += 46
        s += m_actions(y)[0]; y += 22
        s += rect(26, y, 188, 54, "#FFFFFF", LINE, 8) + lbl(34, y + 12, "Your plan") + t(34, y + 36, "4", 18, TERRA, "khand", 700) + t(50, y + 28, "Visits A Year", 9, INK, "khand", 700) + t(50, y + 40, "Plus · Quarterly Care", 7.5, MUTE)
        if not on: s += t(34, y + 68, "A failed card only shows in the console", 7.5, RED, "hind", 600)
        return s, 200
    return frame("Member app: payment problem", m_page([body]))
def M_testlabel(chipmode):
    def body(y):
        g, h = m_house(y); s = g; y += h + 2
        s += m_title(y)[0]; y += 22
        s += m_actions(y)[0]; y += 22
        s += rect(26, y, 188, 60, "#FFFFFF", LINE, 8) + lbl(34, y + 12, "Next visit") + t(34, y + 26, "Winter Visit", 11, INK, "khand", 700) + t(34, y + 39, "Monday, Feb 15, 2027, 8:00 to 9:00 AM", 7.5, INK, "hind", 600)
        return s, 200
    return frame("Member app: test data label", m_page([body], test="chip" if chipmode else "pill"))
def M_desk(two):
    s = rect(7, 44, 226, 236, CREAM)
    def col(x, y, w):
        r = rect(x, y, w, 30, "#CFE0E8") + rect(x, y + 20, w, 10, "#00000070") + t(x + 4, y + 28, "5439 Example Village Dr", 7.5, "#FFFFFF", "khand", 700)
        r += t(x + 4, y + 44, "Alina Example", 10, INK, "khand", 700) + rect(x + 4, y + 50, w - 8, 12, "#FFFFFF", TERRA, 6, .8) + t(x + w / 2, y + 58.5, "Book · Message · Add-Ons", 7.5, INK, "hind", 600, "middle")
        return r
    if not two:
        s += rect(76, 48, 88, 230, "#FFFFFF", LINE, 8) + col(76, 56, 88)
        s += rect(80, 124, 80, 50, "#FFFFFF", LINE, 4) + t(84, 136, "NEXT VISIT", 7.5, MUTE, "hind", 600) + t(84, 148, "Winter Visit", 8, INK, "khand", 700)
        s += t(120, 268, "1280: phone column, empty sides", 7.5, RED, "hind", 600, "middle")
    else:
        s += rect(24, 48, 192, 230, "#FFFFFF", LINE, 8) + col(28, 56, 104)
        s += rect(138, 56, 74, 60, "#FFFFFF", LINE, 4) + t(142, 68, "NEXT VISIT", 7.5, MUTE, "hind", 600) + t(142, 80, "Winter Visit", 9, INK, "khand", 700) + t(142, 92, "Feb 15, 8 to 9 AM", 7.5, INK)
        s += rect(138, 120, 74, 50, "#FFFFFF", LINE, 4) + t(142, 132, "OPEN ITEMS", 7.5, MUTE, "hind", 600) + t(142, 144, "Central AC", 8.5, INK, "khand", 700) + chip(142, 150, "Watch", MUST, h=11)[0]
        s += rect(28, 124, 104, 46, "#FFFFFF", LINE, 4) + t(32, 136, "YOUR PLAN", 7.5, MUTE, "hind", 600) + t(32, 156, "4", 14, TERRA, "khand", 700) + t(44, 152, "Visits A Year", 8, INK, "khand", 700)
        for i, w in enumerate(("Home", "Visits", "Record", "Plan", "More")):
            s += t(40 + i * 40, 268, w, 7.5, TERRA if i == 0 else MUTE, "hind", 600, "middle")
    return frame("Member app at 1280", desk(s, CREAM, y=32, h=252))

# ================= PLANNING TOOLS pieces (board funnel/, website-diagram/, info-flow/, value-estimator/) =================
def tool_head(y, title, sub, eyebrow, new=False, aligned=False):
    s = ""
    if new:
        s += rect(7, y, 226, 16, "#FFFFFF") + t(14, y + 11, "‹ Command Center", 7.5, INK, "hind", 600) + wordmark(120, y + 12, 9, INK, TERRA, "middle") + grad(7, y + 16, 226, 1.6); y += 22
    else:
        s += rect(36, y + 2, 92, 14, "#FFFFFF", LINE, 7) + t(82, y + 12, "‹ UpKeep Command Center", 7.5, INK, "hind", 600, "middle"); y += 20
    s += t(36, y + 6, eyebrow, 7.5, LAGOON if new else GD, "hind", 700, extra='letter-spacing="1"') + t(36, y + 22, title, 15, INK, "khand", 700)
    s += t(36 if (aligned or new) else 12, y + 33, sub, 7.5, MUTE)
    return s, y + 38
def T_frame(lab, body): return frame(lab, desk(body, "#FDFBF6", y=30, h=258), "blend", None)
COLS_OLD = [("Member", TEAL), ("Company / Console", GD), ("Tech", TERRA2)]
def T_flow(new):
    s, y = tool_head(42, "Information Flow Map", "What each action triggers across the apps, and back.", "SMART UPKEEP · DRAFT", False, True)
    xs = [12, 86, 160]
    for i, (n, c) in enumerate(COLS_OLD):
        if new: s += grad(xs[i], y, 68, 14, 4) if i == 1 else rect(xs[i], y, 68, 14, TERRA if i == 0 else LAGOON, "none", 4)
        else: s += rect(xs[i], y, 68, 14, c, "none", 4)
        s += t(xs[i] + 34, y + 10, n, 7.5, "#FFFFFF", "khand", 700, "middle")
    y += 20
    for k, (st, a, b, cc) in enumerate((("Get A Quote", "Quote Started", "Funnel Counts", None), ("Accept A Plan", "Sign Up + Pay", "New Sign-Up", "Visit Routed"), ("Request A Visit", "Request A Visit", "Requests List", "On Today's List"))):
        s += rect(10, y, 220, 50, "#FFFFFF", LINE, 4) + dot(18, y + 9, 5, INK) + t(18, y + 11.5, str(k + 1), 7.5, "#FFFFFF", "hind", 700, "middle") + t(27, y + 12, st, 9, INK, "khand", 700)
        bc = [TERRA if new else TEAL, LAGOON if new else GD]
        for j, w in enumerate((a, b, cc)):
            if not w: continue
            x = xs[j]
            if j == 2: s += rect(x, y + 18, 68, 26, "#F3F1EC", "#9AA1A5", 4, 1, 'stroke-dasharray="3 2"')
            elif j == 1 and new: s += grad(x - .8, y + 17.2, 69.6, 27.6, 4) + rect(x + .6, y + 18.6, 66.8, 24.8, "#FFFFFF", "none", 3.4)
            else: s += rect(x, y + 18, 68, 26, "#FFFFFF", bc[j], 4, 1.2)
            s += t(x + 4, y + 29, w[:20], 7.5, INK, "hind", 600) + t(x + 4, y + 39, "PLANNED" if j == 2 else "LIVE", 7.5, MUTE if j == 2 else JUNGLE, "hind", 600)
        y += 54
    return T_frame("Information Flow Map", s)
def T_accent(new):
    s, y = tool_head(42, "Value Estimator", "An estimate, not an appraisal.", "SMART UPKEEP · ESTIMATES", False, True)
    for i, w in enumerate(("Base At Launch", "Pre-Launch", "100 Homes")):
        x = 14 + i * 64
        if i == 0: s += (grad(x, y, 60, 15, 3) if new else rect(x, y, 60, 15, GOLD, "none", 3)) + t(x + 30, y + 10.5, w, 7.5, "#FFFFFF" if new else INK, "hind", 700, "middle")
        else: s += rect(x, y, 60, 15, "#FFFFFF", LINE, 3) + t(x + 30, y + 10.5, w, 7.5, INK, "hind", 600, "middle")
    y += 22
    for i, (n, v, f) in enumerate((("Member Homes", "31", .1), ("Monthly Churn (%)", "2.7", .3))):
        s += rect(14, y, 100, 40, "#FFFFFF", LINE, 4) + t(20, y + 12, n, 7.5, INK, "hind", 600) + t(108, y + 12, v, 8, INK, "hind", 600, "end")
        s += rect(20, y + 26, 88, 4, "#3a3a3a", "none", 2) + dot(20 + 88 * f, y + 28, 4, LAGOON if new else GD); y += 44
    s += rect(122, y - 88, 104, 84, "#FFFFFF", LINE, 4) + t(130, y - 72, "LIKELY", 7.5, MUTE, "hind", 600) + t(130, y - 52, "$128k", 15, TERRA if new else GD, "khand", 700) + t(130, y - 36, "Example estimate", 7.5, MUTE)
    return T_frame("Tool pages: accent colour", s)
def T_align(fixed):
    s, y = tool_head(42, "Funnel", "The six-stage smartupkeep.ai funnel as it works on the site.", "SMART UPKEEP · LIVE SITE", False, fixed)
    s += rect(36, y, 168, 120, "#FFFFFF", LINE, 4)
    for i, w in enumerate(("Marketing", "Video / Catch", "Home Page", "Info Gather")):
        x = 42 + i * 8
        s += rect(x, y + 6 + i * 24, 156 - i * 16, 20, GOLD if i % 2 == 0 else "#E8B942", "none", 3) + dot(x + 9, y + 16 + i * 24, 6, TEAL) + t(x + 9, y + 19 + i * 24, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle") + t(x + 19, y + 19 + i * 24, w, 7.5, INK, "hind", 600)
    if not fixed: s += f'<line x1="12" y1="{y-8}" x2="12" y2="{y+130}" stroke="{RED}" stroke-dasharray="2 2"/><line x1="36" y1="{y-8}" x2="36" y2="{y+130}" stroke="{RED}" stroke-dasharray="2 2"/>' + t(14, y + 140, "intro starts left of the card", 7.5, RED, "hind", 600)
    return T_frame("Tool pages at 1280: intro line", s)
def T_bars(new, zeros=False, which="bars"):
    s, y = tool_head(42, "Funnel", "The six-stage smartupkeep.ai funnel. Tap a stage.", "SMART UPKEEP · LIVE SITE", False, True)
    s += rect(14, y, 212, 150, "#FFFFFF", LINE, 4)
    for i, w in enumerate(("Marketing", "Video / Catch", "Home Page", "Info Gather", "Price Offer", "Make The Sale")):
        x = 20 + i * 9; bw = 200 - i * 18; yy = y + 6 + i * 22
        if which == "bars" and new:
            s += grad(x, yy, bw, 18, 3, ["", "E6", "CC", "B3", "99", "80"][i]) + dot(x + 9, yy + 9, 6, "#FFFFFF") + t(x + 9, yy + 12, str(i + 1), 7.5, INK, "hind", 700, "middle") + t(x + 19, yy + 12, w, 7.5, "#FFFFFF", "hind", 700)
        else:
            s += rect(x, yy, bw, 18, GOLD if i % 2 == 0 else "#E8B942", "none", 3) + dot(x + 9, yy + 9, 6, TEAL) + t(x + 9, yy + 12, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle") + t(x + 19, yy + 12, w, 7.5, INK, "hind", 600)
        if zeros: s += rect(x + bw - 18, yy + 3, 14, 12, "#FFFFFF", "none", 3) + t(x + bw - 11, yy + 12, "0", 8, INK, "khand", 700, "middle")
    msg = "TEST zeros · counts start Dec 1, 2026" if zeros else "Tap a stage. Counts start at launch."
    s += t(20, y + 144, msg, 7.5, "#7A5A0C" if zeros else MUTE, "hind", 600 if zeros else 400)
    return T_frame("Funnel: " + ("stage bars" if which == "bars" else "before launch"), s)
def pill(x, y, w, c=GOLD, new=False):
    ww = len(w) * 4.1 + 12
    s = rect(x, y, ww, 14, "#FFFFFF", c, 7, 1) + t(x + ww / 2, y + 10, w, 7.5, INK, "hind", 600, "middle")
    if new: s += rect(x + ww - 8, y - 6, 20, 9, JUNGLE, "none", 4) + t(x + ww + 2, y + 1, "NEW", 7.5, "#FFFFFF", "hind", 700, "middle")
    return s, ww
def T_diagram(more=False, colour=False):
    s, y = tool_head(42, "Website Diagram", "Every smartupkeep.ai page, screen and app. Tap one.", "SMART UPKEEP · LIVE SITE", False, True)
    s += rect(10, y, 220, 184, "#FFFFFF", LINE, 4)
    SC = TERRA if colour else GOLD
    yy = y + 10
    for line in (("Home", "Video (V7)", "Welcome Offer", "FAQ"), ("Get Started", "Your Price Is Ready"), ("Price Offer", "Waitlist (Out Of Area)"), ("Sign Up", "Secure Payment", "Welcome")):
        x = 16
        for w in line: g, ww = pill(x, yy, w, SC); s += g; x += ww + 5
        yy += 20
    if more:
        for line in (("Cancel Membership", "In-Person Form"), ("Lawn Quote",)):
            x = 16
            for w in line: g, ww = pill(x, yy, w, SC, new=True); s += g; x += ww + 16
            yy += 20
    s += ln(yy, 16, 224, "#EFE3C8") + t(16, yy + 10, "Apps (behind the gate)", 7.5, MUTE); yy += 16
    apps = [("Member App", TERRA if colour else GOLD), ("Tech App", LAGOON if colour else GOLD), ("Operator Console", None)]
    if more: apps = [("Member App + Client 1-3", GOLD), ("Tech App + Tech Dash 1-3", GOLD), ("Operator Console", None)]
    x = 16
    for w, c in apps:
        ww = len(w) * 4.1 + 12
        if x + ww > 226: x = 16; yy += 20
        if c is None and colour:
            s += grad(x - 1, yy - 1, ww + 2, 16, 8) + rect(x, yy, ww, 14, "#FFFFFF", "none", 7) + t(x + ww / 2, yy + 10, w, 7.5, INK, "hind", 600, "middle")
        else:
            s += pill(x, yy, w, c or GOLD, new=more and "1-3" in w)[0]
        x += ww + (14 if more else 5)
    if colour:
        yy += 26; s += dot(20, yy, 3, TERRA) + t(26, yy + 3, "Member", 7.5, MUTE) + dot(64, yy, 3, LAGOON) + t(70, yy + 3, "Tech", 7.5, MUTE) + grad(96, yy - 3, 12, 6, 3) + t(112, yy + 3, "Owner and console", 7.5, MUTE)
    return T_frame("Website Diagram: " + ("pages" if more else "pill colours"), s)
def T_value(new):
    s, y = tool_head(42, "Value Estimator", "What the business could be worth.", "SMART UPKEEP · ESTIMATES", False, True)
    s += rect(14, y, 212, 112, "#FFFFFF", LINE, 4)
    for i, (l, v) in enumerate((("LOW", "$38k"), ("LIKELY", "$128k"), ("HIGH", "$160k"))):
        x = 22 + i * 66
        s += t(x, y + 16, l, 7.5, MUTE, "hind", 600) + t(x, y + 36, v, 18 if i == 1 else 13, ((TERRA if new else GD) if i == 1 else INK), "khand", 700)
    if new: s += chip(22, y + 49, "Example estimate · TEST inputs", SAFFRON, tc="#7A5A0C")[0] + grad(22, y + 64, 196, 2, 1)
    s += t(22, y + 80, "Implied ARR $65k · Profit $5,375 (TEST)" if new else "Implied ARR $65k · Profit $5,375", 7.5, INK, "hind", 600) + t(22, y + 94, "31 homes x ($168 + $7 add-ons) x 12", 7.5, MUTE)
    if not new: s += t(22, y + 107, "No label marks these as test inputs", 7.5, RED, "hind", 600)
    return T_frame("Value Estimator: result", s)
def T_planned(new):
    s, y = tool_head(42, "Information Flow Map", "Live, sample-only and planned steps.", "SMART UPKEEP · DRAFT", False, True)
    for k, (st, a, b, cc) in enumerate((("Accept A Plan", "Sign Up + Pay", "New Sign-Up", "Visit Routed"), ("Request A Visit", "Request A Visit", "Requests List", "On Today's List"), ("Visit Report", "Report In Record", "Visit Reports", "Report Sent"))):
        s += rect(10, y, 220, 50, "#FFFFFF", LINE, 4) + t(18, y + 12, st, 9, INK, "khand", 700)
        for j, w in enumerate((a, b, cc)):
            x = [12, 86, 160][j]
            if j == 2 and k < 2:
                if new: s += rect(x, y + 18, 68, 26, "#FFFFFF", LAGOON, 4, 1, 'stroke-dasharray="4 2"') + t(x + 4, y + 29, w, 7.5, INK, "hind", 600) + chip(x + 4, y + 32, "Planned · Jan", LAGOON, h=10)[0]
                else: s += rect(x, y + 18, 68, 26, "#F3F1EC", "#9AA1A5", 4, 1, 'stroke-dasharray="3 2"') + t(x + 4, y + 29, w, 7.5, MUTE, "hind", 600) + t(x + 4, y + 39, "PLANNED", 7.5, MUTE, "hind", 600)
            else:
                c = [TEAL, GD, TERRA2][j]
                s += rect(x, y + 18, 68, 26, "#FFFFFF", c, 4, 1.2) + t(x + 4, y + 29, w, 7.5, INK, "hind", 600) + t(x + 4, y + 39, "LIVE", 7.5, JUNGLE, "hind", 600)
        y += 54
    return T_frame("Information Flow Map: planned steps", s)
def T_header(new):
    s, y = tool_head(42, "Website Diagram", "Every smartupkeep.ai page, screen and app.", "SMART UPKEEP · LIVE SITE", new, True)
    s += rect(10, y, 220, 130, "#FFFFFF", LINE, 4)
    yy = y + 10
    for line in (("Password Gate",), ("Home", "Video (V7)", "FAQ"), ("Get Started",), ("Your Price Is Ready",)):
        tot = sum(len(w) * 4.1 + 12 for w in line) + 5 * (len(line) - 1); x = 120 - tot / 2
        for w in line: g, ww = pill(x, yy, w); s += g; x += ww + 5
        s += t(120, yy + 22, "↓", 7.5, MUTE, "hind", 400, "middle"); yy += 28
    return T_frame("Tool pages: top of page", s)

# ================= decks =================
FEEL = {"calm", "bold", "practical", "playful", "premium"}
DECKS = {}
def D(key, did, name, tag, blurb, topic, note, picks, applies):
    DECKS[key] = dict(did=did, name=name, tag=tag, blurb=blurb, topic=topic, note=note, picks=picks, applies=applies)
SITE = "Smart Upkeep Site"
D("site", "upkeep-site-trust-and-launch-dates-deck", "Site: Trust And Launch Dates", "Home Page", "10 cards: site trust, launch dates and sign-up path",
  "site-trust-and-launch-dates", "Trust and conversion gaps on smartupkeep.ai before sign-ups open Dec 1 2026.", [
  ("Footer", f"{SITE} Home: Footer, the page ends with an empty footer now, so should it end with contact, service area and policy links?",
   ("ft_empty", "Empty Footer (Now)", "Page ends after Featured Service", "calm", S_footer(False)),
   ("ft_full", "Contact Footer", "Text, call, email, area, policy links", "practical", S_footer(True))),
  ("Launch Dates", f"{SITE} Home Hero: Launch dates, should the hero say sign-ups open Dec 1 and visits start in January 2027?",
   ("dt_none", "No Dates (Now)", "Trust chips under the button", "calm", S_dates(False)),
   ("dt_line", "Dates Line Under Button", "Sign-ups Dec 1, visits Jan 2027", "practical", S_dates(True))),
  ("Main Button", f"{SITE} Home: Main button wording, should hero, plans and bottom bar use one label instead of three?",
   ("cta_mixed", "Three Labels (Now)", "Free Quote, Get Started, Free Offer", "calm", S_cta(False)),
   ("cta_one", "One Label Everywhere", "Get My Free Quote on every button", "bold", S_cta(True))),
  ("Desktop Navigation", f"{SITE} Home At 1280: Navigation, should the phone tab bar floating over the plan cards become links in the header?",
   ("nav_float", "Floating Tab Bar (Now)", "Phone bar sits over plan prices", "calm", S_desknav(False)),
   ("nav_head", "Links In The Header", "Plans, A La Carte, My Home, Quote", "practical", S_desknav(True))),
  ("Plan Card Edge", f"{SITE} Home Plans: Plan card top edge, should the plan cards keep the lagoon edge or take the member terracotta?",
   ("edge_lagoon", "Lagoon Edge (Now)", "Blue top edge on every plan", "calm", S_edge(LAGOON)),
   ("edge_terra", "Terracotta Edge", "Member colour, lagoon stays for links", "bold", S_edge(TERRA))),
  ("Who Is Behind It", f"{SITE} Home: Owner card, should a short owned-and-run-locally card with the founder sit under Why Trust Us?",
   ("own_none", "No Owner Card (Now)", "Trust chips, then Details", "calm", S_owner(False)),
   ("own_card", "Owned And Run Locally", "Founder initials, real person line", "premium", S_owner(True))),
  ("Sample Report", f"{SITE} Home: Sample Home Report, should the home page link to a sample report before anyone signs up?",
   ("rep_none", "No Sample (Now)", "Hero goes straight to plans", "calm", S_sample(False)),
   ("rep_link", "See A Sample Report", "Small card under the hero", "practical", S_sample(True))),
  ("Cancel Page", f"{SITE} Cancel Membership Page: Layout, the page scrolls sideways on a phone now, so should it fit and show what happens next?",
   ("cx_now", "Wide Form (Now)", "Scrolls sideways at 393", "calm", S_cancel(False)),
   ("cx_fit", "Fitted With Next Steps", "Refund email, end date, timing", "practical", S_cancel(True))),
  ("FAQ Page", f"{SITE} FAQ Page: Opening view, should it open on a search box and the top three questions with a text-the-team line?",
   ("faq_now", "Category List (Now)", "First category open, rest folded", "calm", S_faq(False)),
   ("faq_new", "Search And Top Questions", "Launch, cancel, area, then help", "practical", S_faq(True))),
  ("Header Contact", f"{SITE} Home Header: Contact button, should a small Text Us button sit at the left of the header across from Share?",
   ("hc_none", "Share Only (Now)", "Logo centered, Share at right", "calm", S_contact(False)),
   ("hc_text", "Text Us At Left", "One tap to reach the team", "practical", S_contact(True))),
 ], ["smartupkeep.ai home", "/#cancel", "/faq/", "desktop 1280"])
CON = "Operator Console"
D("console", "upkeep-operator-console-alerts-and-test-data-deck", "Operator Console: Alerts And Test Data", "Operator Console", "10 cards: console alerts, test data and launch view",
  "operator-console-alerts-and-test-data", "Alert handling and test data noise in the Operator Console (/console/); layout picks stay in the queued Operator Console Deck.", [
  ("Alert Severity", f"{CON} Live Alerts: Severity, should a gas smell look different from a declined card instead of every alert in the same red?",
   ("sev_same", "Same Red For All (Now)", "Every alert gets one red dot", "calm", C_sev(False)),
   ("sev_rank", "Ranked By Severity", "Safety red first, billing mustard", "practical", C_sev(True))),
  ("Alert Actions", f"{CON} Live Alerts: Actions, should each alert carry Acknowledge, Assign and Resolve buttons?",
   ("act_none", "No Actions (Now)", "Alerts stay until data changes", "calm", C_actions(False)),
   ("act_three", "Acknowledge, Assign, Resolve", "Three small buttons per alert", "practical", C_actions(True))),
  ("Repeated Items", f"{CON} Sections: Repeated items, should one request live in one section with an also-in link instead of showing three times?",
   ("dup_all", "In Every Section (Now)", "Alerts, Requests and Feed", "calm", C_dupes(False)),
   ("dup_once", "Once, With Also-In Link", "One home for each item", "practical", C_dupes(True))),
  ("Sample Tags", f"{CON} Rows: Sample tags, should one test data banner replace the SAMPLE chip on every row?",
   ("tag_rows", "Chip On Every Row (Now)", "About 60 SAMPLE chips", "calm", C_tags(False)),
   ("tag_banner", "One Test Data Banner", "Rows stay clean", "practical", C_tags(True))),
  ("Test Buttons", f"{CON} Header: Test buttons, should Load Test Data and Clear Live Test Events move into one small Test menu?",
   ("tb_three", "Three Buttons (Now)", "Beside Refresh at the top", "calm", C_testbtn(False)),
   ("tb_menu", "Refresh Plus Test Menu", "Test tools one tap away", "practical", C_testbtn(True))),
  ("No Alerts", f"{CON} Live Alerts: Empty state, when there are no alerts should the panel show a calm All Clear card?",
   ("emp_blank", "Blank Panel (Now)", "Count reads 0, list is empty", "calm", C_empty(False)),
   ("emp_clear", "All Clear Card", "Last closed alert and next visit", "calm", C_empty(True))),
  ("Launch Readiness", f"{CON} Top Of Page: Launch readiness, should a card count down to sign-ups on Dec 1 and first visits on Jan 1?",
   ("lr_none", "KPI Row Only (Now)", "Alerts, visits, members", "calm", C_launch(False)),
   ("lr_card", "Launch Readiness Card", "Days to Dec 1 and Jan 1, TEST", "bold", C_launch(True))),
  ("Waitlist ZIPs", f"{CON} Sales Funnel: Waitlist ZIPs, should the ZIP list group repeats into one row per ZIP with a count?",
   ("zip_list", "Plain List (Now)", "48170 shows twice", "calm", C_zips(False)),
   ("zip_count", "One Row Per ZIP", "Small bar and home count", "practical", C_zips(True))),
  ("Not Yet Connected", f"{CON} Revenue And Metrics: Placeholder tiles, should tiles with no data say not connected yet instead of the word Placeholder?",
   ("ph_word", "Placeholder Word (Now)", "Reads like a real value", "calm", C_place(False)),
   ("ph_muted", "Muted Not Connected Yet", "Grey tile says what it needs", "practical", C_place(True))),
  ("Alert Times", f"{CON} Live Alerts: Times, should each alert show the clock time next to how long ago it came in?",
   ("tm_ago", "Minutes Ago Only (Now)", "12m ago, 3h ago", "calm", C_time(False)),
   ("tm_clock", "Clock Time Plus Ago", "9:32 PM, 12m ago", "practical", C_time(True))),
 ], ["operator console (/console/)"])
MEM = "UpKeep Member App"
D("member", "upkeep-member-app-account-and-empty-states-deck", "Member App: Account And Empty States", "Member App", "10 cards: account menu, first month and problem states",
  "member-app-account-and-empty-states", "Member app states nobody has seen yet: the month before the first visit, errors, loading and the account menu.", [
  ("More Tab", f"{MEM} More: Account menu, the tab has one Profile row now, so should it list account, help and sign out in groups?",
   ("more_one", "One Profile Row (Now)", "Everything sits inside Profile", "calm", M_more(False)),
   ("more_full", "Grouped Account List", "Notifications, help, refer, sign out", "practical", M_more(True))),
  ("Cancel Link", f"{MEM} Plan & Billing: Cancel link, should the one-step online cancel be a quiet link at the bottom of Plan & Billing?",
   ("cl_none", "No Cancel In App (Now)", "Cancel lives only on the site", "calm", M_cancel(False)),
   ("cl_link", "Quiet Link At The Bottom", "Under Pause My Plan", "practical", M_cancel(True))),
  ("Before First Visit", f"{MEM} Home: Before the first visit, should a December sign-up see a welcome card with three getting-ready steps?",
   ("fv_now", "Next Visit Card (Now)", "Built for long-time members", "calm", M_first(False)),
   ("fv_new", "Welcome And Get Ready", "First visit in January, 3 steps", "bold", M_first(True))),
  ("Empty Record", f"{MEM} Record: Before the first visit, should the record say it starts at the first visit and offer adding photos now?",
   ("rec_now", "Appliance List (Now)", "Shows checks dated Oct 2026", "calm", M_record(False)),
   ("rec_new", "Starts At First Visit", "Add equipment photos now", "practical", M_record(True))),
  ("Sign-In Errors", f"{MEM} Sign In: Errors, should empty or wrong fields show a short red line under each box?",
   ("si_none", "No Message (Now)", "Empty fields still sign in", "calm", M_signin(False)),
   ("si_err", "Red Line Under Each Box", "Says what to fix", "practical", M_signin(True))),
  ("Loading", f"{MEM} Home: Loading, should Home show grey placeholder shapes while it loads instead of a blank screen?",
   ("ld_blank", "Blank While Loading (Now)", "Cream screen until ready", "calm", M_loading(False)),
   ("ld_skel", "Grey Placeholder Shapes", "Layout shows at once", "calm", M_loading(True))),
  ("No Connection", f"{MEM} Home: No connection, should a mustard banner say it is showing saved info when the app can't connect?",
   ("off_none", "Nothing Shown (Now)", "Requests fail with no message", "calm", M_offline(False)),
   ("off_banner", "Saved Info Banner", "Requests send when back online", "practical", M_offline(True))),
  ("Payment Problem", f"{MEM} Home: Declined card, should a declined card show a terracotta notice with Update on Home?",
   ("pay_none", "Console Only (Now)", "Member never sees it in the app", "calm", M_payfail(False)),
   ("pay_banner", "Notice With Update", "Date to fix it by, one button", "practical", M_payfail(True))),
  ("Test Data Label", f"{MEM} Header: Test data label, should the red pill above the header become a small grey TEST chip?",
   ("tl_pill", "Red Pill Above (Now)", "Full test line on every tab", "calm", M_testlabel(False)),
   ("tl_chip", "Small Grey TEST Chip", "Header stays as picked", "calm", M_testlabel(True))),
  ("Desktop View", f"{MEM} Home At 1280: Desktop view, should Home use two columns inside the frame instead of one phone column?",
   ("dk_one", "Phone Column (Now)", "Empty cream on both sides", "calm", M_desk(False)),
   ("dk_two", "Two Columns Above 900px", "Next visit and open items at right", "premium", M_desk(True))),
 ], ["member app (member/, Client 1-3)"])
BRD = "UpKeep Board"
D("tools", "upkeep-planning-tools-brand-colours-and-layout-deck", "Planning Tools: Brand Colours And Layout", "Planning Tools", "10 cards: funnel, diagram, flow map and estimator look",
  "planning-tools-brand-colours-and-layout", "Brand drift on the board's planning tools (Funnel, Website Diagram, Information Flow Map, Value Estimator).", [
  ("Flow Map Colours", f"{BRD} Information Flow Map: Column colours, Member is teal and Tech terracotta now, so should Member take terracotta, Tech lagoon and Console the blend?",
   ("ifc_now", "Teal, Gold, Terra (Now)", "Member teal, Tech terracotta", "calm", T_flow(False)),
   ("ifc_brand", "Terracotta, Blend, Lagoon", "Matches member and tech apps", "bold", T_flow(True))),
  ("Accent Colour", f"{BRD} Value Estimator: Accent colour, should the gold buttons and sliders take the lagoon-to-terracotta blend?",
   ("acc_gold", "Gold Accent (Now)", "Gold buttons and slider dots", "calm", T_accent(False)),
   ("acc_blend", "Owner Blend", "Lagoon to terracotta, like Console", "premium", T_accent(True))),
  ("Intro Line", f"{BRD} Funnel At 1280: Intro line, should the line under the title start at the card's edge instead of hanging out to the left?",
   ("al_hang", "Hangs Left (Now)", "Starts left of the card", "calm", T_align(False)),
   ("al_fix", "Lined Up With The Card", "Title, line and card share an edge", "calm", T_align(True))),
  ("Funnel Bars", f"{BRD} Funnel: Stage bars, should the six bars fade through the blend instead of alternating two golds?",
   ("fb_gold", "Two Golds (Now)", "Teal number dots on gold", "calm", T_bars(False)),
   ("fb_blend", "One Blend, Fading", "White number dots, white labels", "bold", T_bars(True))),
  ("Before Launch", f"{BRD} Funnel: Before launch, should each stage show a TEST zero and the Dec 1 start instead of no numbers?",
   ("bl_none", "No Numbers (Now)", "Counts start at launch", "calm", T_bars(False, False, "zeros")),
   ("bl_zero", "TEST Zeros And Start Date", "Zero per stage, Dec 1 note", "practical", T_bars(False, True, "zeros"))),
  ("Diagram Pages", f"{BRD} Website Diagram: Missing pages, should it add Cancel Membership, the In-Person Form, Lawn Quote and the Client and Tech Dash views?",
   ("dp_now", "Current Pages (Now)", "Misses five newer pages", "calm", T_diagram(False, False)),
   ("dp_new", "Newer Pages Added", "Marked New until reviewed", "practical", T_diagram(True, False))),
  ("Diagram Colours", f"{BRD} Website Diagram: Pill colours, should each pill take the colour of who uses it instead of all gold?",
   ("dc_gold", "All Gold (Now)", "Every pill outlined gold", "calm", T_diagram(False, False)),
   ("dc_who", "Coloured By Who Uses It", "Member terracotta, tech lagoon", "bold", T_diagram(False, True))),
  ("Estimate Label", f"{BRD} Value Estimator: Result label, should the likely value carry an example estimate and TEST inputs chip?",
   ("ve_gold", "Big Gold Number (Now)", "Reads like a real valuation", "calm", T_value(False)),
   ("ve_label", "Example Estimate Chip", "Blend rule, test inputs marked", "practical", T_value(True))),
  ("Planned Steps", f"{BRD} Information Flow Map: Planned steps, should planned boxes show a lagoon dashed edge with a target month instead of grey?",
   ("ps_grey", "Grey Dashed (Now)", "Planned looks switched off", "calm", T_planned(False)),
   ("ps_lagoon", "Lagoon Dashed, Target Month", "Planned, with a Jan chip", "practical", T_planned(True))),
  ("Page Top", f"{BRD} Tool Pages: Top of page, should the floating back pill become a slim header with logo and the blend rule like the board?",
   ("pt_pill", "Back Pill (Now)", "Floating pill, gold eyebrow", "calm", T_header(False)),
   ("pt_head", "Slim Board Header", "Back, logo, blend rule", "premium", T_header(True))),
 ], ["board funnel/", "website-diagram/", "info-flow/", "value-estimator/"])

# ================= EXTRAS IDEAS (Max 22:11 ICT standing rule via UpKeep: decks propose NEW add-ons for the Extras list) =================
# Card = the live Shop A La Carte Extras grid (app.js extrasEntry: .xt-grid 4 across, .xt-tile white with border, icon over label,
# .xt-tile.cur lagoon edge, tap opens the renderAddonList detail with desc + price). Icons are the site's own (icons.js -> uk_extras_icons.json).
# Existing tiles (pricing-config.js addons after Max removed pool, snow, handyman, pest, backflow) are drawn plain; the idea is the
# highlighted 8th tile with a NEW chip and its open detail. Prices are examples only.
XICO = json.load(open("tools/uk_extras_icons.json"))
def suico(name, x, y, size):
    b = XICO.get(name) or XICO["wrench"]
    b = b.replace('class="f-t', f'fill="{TERRA}" class="f-t').replace('class="f-l', f'fill="{LAGOON}" class="f-l').replace('class="f-s', f'fill="{SAFFRON}" class="f-s').replace('class="f-j', f'stroke="{JUNGLE}" class="f-j')
    k = size / 48
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})" fill="none" stroke="#1f1b17" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{b}</g>'
LIVE_X = [("window", "Exterior Window Washing"), ("brush", "Carpet Cleaning"), ("spray", "Pressure Washing"), ("brush", "Deck Sealing"),
          ("chimney", "Chimney Sweep"), ("duct", "Air Duct Cleaning"), ("lights", "Christmas Lights")]
def tile_lab(x, cx, y, lab, c=INK):
    words, lines, cur = lab.split(), [], ""
    for w in words:
        if len(cur + " " + w) > 11 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(t(cx, y + i * 8.4, l, 7.5, c, "hind", 500, "middle") for i, l in enumerate(lines[:3]))
def X_card(ico, name, desc, price, unit="one time"):
    y = 32; s = rect(20, y, 200, 256, "#FAF3EB")
    s += rect(20, y + 14, 200, 242, "#FFFFFF", "none", 10) + t(28, y + 32, "Shop À La Carte", 13, INK, "khand", 700) + t(210, y + 31, "×", 12, INK, "hind", 400, "end")
    s += t(28, y + 43, "Optional services for any membership.", 7.5, MUTE) + t(28, y + 52, "Tap a tile for details and price.", 7.5, MUTE)
    gy = y + 58; w = 45; hgt = 52
    items = LIVE_X + [(ico, name)]
    for i, (ic_, lab) in enumerate(items):
        cx0 = 26 + (i % 4) * (w + 2); yy = gy + (i // 4) * (hgt + 2); new = i == 7
        s += rect(cx0, yy, w, hgt, "#FFFFFF", LAGOON if new else "#E4D6C4", 0, 1.6 if new else 1)
        s += suico(ic_, cx0 + w / 2 - 10, yy + 4, 20) + tile_lab(cx0, cx0 + w / 2, yy + 33, lab, INK if new else "#3a3a3a")
        if new: s += rect(cx0 + w - 20, yy - 5, 22, 9, JUNGLE, "none", 4) + t(cx0 + w - 9, yy + 1.5, "NEW", 7.5, "#FFFFFF", "hind", 700, "middle")
    dy = gy + 2 * (hgt + 2) + 4
    s += rect(26, dy, 188, 74, "#FFFFFF", "#E4D6C4", 0, 1) + suico(ico, 32, dy + 6, 22)
    s += t(60, dy + 15, name, 9.5, INK, "khand", 700)
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        if len(cur + " " + wd) > 36 and cur: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur)
    for i, l in enumerate(lines[:3]): s += t(60, dy + 27 + i * 9.5, l, 7.5, MUTE)
    s += t(60, dy + 63, f"Example ${price} · {unit}", 8, INK, "hind", 700)
    s += rect(170, dy + 53, 38, 15, TERRA, "none", 3) + t(189, dy + 63.5, "ADD", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return frame("Shop À La Carte: new extra", phone(s), TERRA, "EXAMPLE PRICE")
XP = [
 ("Water Protection", ("leak", "Water Leak Sensor Setup", "Leak sensors under sinks, by the water heater and washer, linked to your phone.", "149", "meter"),
                      ("sumpbk", "Sump Pump Battery Backup", "A battery backup pump that keeps the basement dry when the power goes out.", "650", "shield")),
 ("Gutters", ("guards", "Gutter Guard Install", "Mesh guards on every gutter so leaves stay out between cleanings.", "1,200", "gutter"),
             ("dsext", "Downspout Extensions", "Extensions and splash blocks that carry roof water away from the foundation.", "120", "gutter")),
 ("Driveway", ("sealcoat", "Driveway Sealcoating", "Clean and sealcoat an asphalt driveway before winter salt and freeze.", "300", "brush"),
              ("crack", "Concrete Crack Filling", "Fill cracks in walks, steps and the garage floor before water gets in.", "175", "wrench")),
 ("Deep Cleaning", ("grout", "Tile And Grout Cleaning", "Deep clean and reseal grout in kitchens and bathrooms.", "250", "brush"),
                   ("upholst", "Upholstery Cleaning", "Steam clean sofas and chairs, pairs with carpet cleaning.", "150", "spray")),
 ("Kitchen", ("dispose", "Garbage Disposal Clean", "Clean, deodorize and check the disposal for leaks and jams.", "85", "wrench"),
             ("hood", "Range Hood Filter Degrease", "Degrease or replace range hood filters so the fan pulls smoke out.", "75", "duct")),
 ("Bathrooms", ("tune", "Faucet And Toilet Tune-Up", "Fix running toilets and drips, swap flappers and aerators.", "140", "wrench"),
               ("bathfan", "Bath Fan Clean And Check", "Clean bathroom exhaust fans and check they vent outside.", "95", "duct")),
 ("Smart Home", ("thermo", "Smart Thermostat Install", "Install and set up a smart thermostat you buy or we bring.", "175", "clock"),
                ("bell", "Video Doorbell Install", "Mount and connect a video doorbell, device not included.", "125", "camera")),
 ("Home Safety", ("grab", "Grab Bar Install", "Two grab bars anchored in studs in the tub, shower or by the toilet.", "150", "shield"),
                 ("ext", "Fire Extinguisher Service", "Check, tag and place kitchen and garage fire extinguishers.", "60", "detector")),
 ("Basement", ("wells", "Window Well Covers", "Clear covers on basement window wells to keep out rain, snow and leaves.", "350", "window"),
              ("dehum", "Basement Dehumidifier Setup", "Set up a dehumidifier with a drain line so the basement stays dry.", "225", "meter")),
 ("Appliances", ("hoses", "Washer Hose Upgrade", "Swap rubber washer hoses for braided steel ones that resist bursting.", "90", "dryer"),
                ("cfan", "Ceiling Fan Clean And Balance", "Clean blades, tighten mounts and stop the wobble on ceiling fans.", "80", "ac")),
]
EXTRAS_REMOVED = ("pool", "snow", "handyman", "pest", "backflow")
_DNP = json.load(open("queue/extras-do-not-propose.json"))  # do-not-propose ledger (R118 removed + every Extras "neither"); never propose these
EXTRAS_NEVER = {x["name"].lower() for x in _DNP["removed_by_max"] + _DNP["rejected"]}
XSHORT = {'Water Leak Sensor Setup': 'Phone alerts for leaks at sinks, heater', 'Sump Pump Battery Backup': 'Keeps the sump pumping in an outage', 'Gutter Guard Install': 'Mesh guards keep leaves out of gutters', 'Downspout Extensions': 'Carries roof water away from the house', 'Driveway Sealcoating': 'Seals asphalt before winter salt', 'Concrete Crack Filling': 'Fills cracks in walks, steps, garage', 'Tile And Grout Cleaning': 'Deep clean and reseal tile grout', 'Upholstery Cleaning': 'Steam clean sofas and chairs', 'Garbage Disposal Clean': 'Clean, deodorize, check for leaks', 'Range Hood Filter Degrease': 'Degrease or swap range hood filters', 'Faucet And Toilet Tune-Up': 'Fix drips and running toilets', 'Bath Fan Clean And Check': 'Clean fans, check they vent outside', 'Smart Thermostat Install': 'Install and set up a smart thermostat', 'Video Doorbell Install': 'Mount and connect a video doorbell', 'Grab Bar Install': 'Two grab bars anchored in studs', 'Fire Extinguisher Service': 'Check, tag and place extinguishers', 'Window Well Covers': 'Clear covers keep wells dry and clean', 'Basement Dehumidifier Setup': 'Dehumidifier with a drain line', 'Washer Hose Upgrade': 'Braided steel hoses that resist bursts', 'Ceiling Fan Clean And Balance': 'Clean blades, tighten, stop the wobble'}
def extras_picks():
    out = []
    for grp, a, b in XP:
        ask = f"Website: Extras, which new {grp.lower()} add-on should join the Extras list, {a[1]} or {b[1]}?"
        oa = (a[0], a[1], XSHORT[a[1]], "practical", X_card(a[4], a[1], a[2], a[3]))
        ob = (b[0], b[1], XSHORT[b[1]], "practical", X_card(b[4], b[1], b[2], b[3]))
        out.append((grp, ask, oa, ob))
    return out
D("extras", "upkeep-extras-ideas-deck", "Extras Ideas Deck", "Extras", "10 cards: new add-on ideas for the Extras list",
  "extras-ideas", "New add-on ideas for the smartupkeep.ai Extras list (Max 22:11 ICT standing rule). Each pick pairs two ideas not on the list today.", extras_picks(),
  ["smartupkeep.ai Shop À La Carte extras grid (pricing-config.js addons)"])
BUILD = ["site", "console", "member", "extras"]   # Planning Tools deck kept in code, not built (Extras Ideas Deck took its slot, Max 22:11 ICT)

def build(key):
    dd = DECKS[key]; DID, NAME = dd["did"], dd["name"]
    assert theme_name_ok(NAME) and not re.search(r"\d", NAME), "R113"
    assert len(dd["picks"]) == 10
    pairs, O, add = kdeck(key[:3] + "fr_", "UpKeep")
    for grp, ask, a, b in dd["picks"]:
        if key != "extras": assert not caption_rule.check(ask), (ask, caption_rule.check(ask))
        else: assert ask.startswith("Website: Extras, ") and ask.count("?") == 1
        for o in (a, b): assert len(o[1]) <= 30 and len(o[2]) <= 40 and o[3] in FEEL, o[:3]
        oa, ob = [O(o[0], o[1], o[2], o[3], o[4], tags=[grp, key]) for o in (a, b)]
        add(grp, grp, oa, ob, ask)
    txt = json.dumps(pairs).lower(); assert "thai" not in txt, "R110"
    meta = {"brands": [dd["note"] + " Option A is what the code shows now (smart-upkeep 319e011 and the board pages), Option B one improvement on the same screen.",
                       "Smart Upkeep brand: white or warm cream, member terracotta #C1502E, tech lagoon #05668D, owner and console lagoon-to-terracotta blend, Khand and Hind, light mode only."],
            "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": dd["topic"], "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True, "caption_rule": "R105" if key != "extras" else "Max 22:11 ICT: captions start with 'Website: Extras, ...'",
            "request": "Max Oct 17 2026 21:43 ICT: 'can you please review all of upkeeps pages/apps and find some things you think we might need to work on and make fresh decks.'",
            "applies_to": dd["applies"], "design_input": "ops/brand/upkeep-full-review-2026-10-17.md",
            "example_data": "All names, addresses, contact details and numbers are example or TEST data.",
            "not_reasked": "Job 6 follow-ups (style-swipe 888e752), queued Operator Console Deck layout picks, video pop-up, Face ID and sign-in link picks",
            "sources": {"content": "tools/build_upkeep_full_review.py", "screens": "/workspace/shots/upkeep-full-review/"}}
    publish(DID, NAME, "UpKeep", pairs, meta, seed=10175, n=10, first=10)
    dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == 10
    order = [p["ask"] for p in pairs]; dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
    for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{DID}-{i:02d}"
    json.dump(dj, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
    if key != "extras": caption_rule.guard(dj["pairs"], DID)
    from agent_links import patch as link_patch
    from chat_button import patch as chat_patch
    pages = json.load(open("decks/pages.json"))
    slug = pages.get(DID) or dd["topic"] + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
           "body.carding .opt .vis{min-height:0;overflow:visible}")
    HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{DID}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    return {"id": DID, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "total": 10, "topic": dd["topic"], "added": dj["generated_at"],
            "tag": dd["tag"], "blurb": dd["blurb"], "slug": slug, "pairs": [f'{q["optionA"]["label"]} vs {q["optionB"]["label"]}' for q in dj["pairs"]]}
if "--preview" in sys.argv:
    d = sys.argv[sys.argv.index("--preview") + 1]; os.makedirs(d, exist_ok=True)
    for key, dd in DECKS.items():
        h = "<html><head><link href='https://fonts.googleapis.com/css2?family=Khand:wght@700&family=Hind:wght@400;500;600;700&display=swap' rel='stylesheet'></head><body style='margin:0;background:#fff;display:grid;grid-template-columns:repeat(4,250px);gap:6px'>"
        for g, ask, a, b in dd["picks"]:
            for o in (a, b): h += f"<div style='width:250px;font:11px Hind'>{o[4]}<b>{o[1]}</b></div>"
        open(os.path.join(d, f"preview-{key}.html"), "w").write(h + "</body></html>")
    print("preview", d); sys.exit()
keys = [sys.argv[sys.argv.index("--only") + 1]] if "--only" in sys.argv else BUILD
out = [build(k) for k in keys]
json.dump(out, open("/tmp/ukr_decks.json", "w"), indent=1)
print(json.dumps(out, indent=1, ensure_ascii=False))
