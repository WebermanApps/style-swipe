#!/usr/bin/env python3
"""Member Profile Header Deck (Branding, for Max Oct 17 2026 18:56 ICT: "i want to establish a branded header/top portion for the
technicians app that will be similar for the member app. please send me a swipe deck for the header/top portion of the member
profile on upkeep"). 10 this-or-that picks; each card is a drawn phone top (member profile, Smart Upkeep member app) at full card
scale. The winner becomes the shared header system for the member AND technician apps (pick 10 shows both side by side).
Brand from smartkeep/funnel-app/member: white base, #EFEDE9 band, terracotta/lagoon/jungle pops, Khand/Hind, roof mark + smartupkeep.
Trust badges: approved set only. No home health score (Max dropped it). Add-ons = one 'My Add-Ons' list. Names/addresses are fake.
Same template/kit as build_followups_1017.py (R89 look, header Share, Notes, This/Both/Love/That/Neither). Page written UNLOCKED:
lock before commit.  usage: build_member_profile_header.py [--preview DIR]"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets
from draft_svg import t, rect, dot, ln, ic, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import deck as kdeck, publish, shareic
from uk5_art import card, mark, wordmark, GREY
from draft_svg import crisp
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
BAND = "#EFEDE9"; BANDL = "#E2DED7"; X0, SW = 20, 200; XR = X0 + SW
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
DID = "upkeep-member-profile-header-deck"; NAME = "Member Profile Header Deck"; SLUG_KEY = "member-profile-header"
NAME_F, NAME_L, ADDR, CITY = "Sarah", "Sample", "123 Sample Lane", "Exampleville"
TECH = "Marco (sample)"
_n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"

# ---------------- pieces (screen x 20..220, drawn at card scale) ----------------
def status(y, c=INK):
    return t(28, y + 9, "9:41", 7.5, c, "hind", 600) + rect(200, y + 4, 11, 5.5, "none", c, 1, .8) + rect(201.2, y + 5.2, 7, 3.1, c), 14
def logo(y, where="corner", c=TERRA, share=True):
    s = ""
    if where == "corner": s += mark(31, y + 10, 7.5, "#FFFFFF", c) + wordmark(42, y + 14.5, 12.5)
    elif where == "center": s += mark(89, y + 10, 7.5, "#FFFFFF", c) + wordmark(100, y + 14.5, 12.5)
    if share: s += shareic(201, y + 3.5, INK, 13)
    return s, 24
def avatar(cx, cy, r, c=TERRA, ch="S"):
    return dot(cx, cy, r, c) + t(cx, cy + r * .42, ch, r * 1.15, "#FFFFFF", "khand", 700, "middle")
def houseic(x, y, s, c=LAGOON, fill=True):
    return (rect(x, y, s, s, c + "1A" if fill else "#FFFFFF", "none" if fill else c, 4, 1)
            + f'<path d="M{x+s*.2} {y+s*.8} V{y+s*.48} L{x+s*.5} {y+s*.22} L{x+s*.8} {y+s*.48} V{y+s*.8} Z" fill="#FFFFFF" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"/>'
            + rect(x + s * .42, y + s * .58, s * .16, s * .22, c))
def who(y, mode="avatar", c=TERRA, big=False):
    if mode == "avatar":
        r = 17 if big else 14
        return (avatar(28 + r, y + r + 1, r, c) + t(36 + 2 * r, y + r - 1, f"{NAME_F} {NAME_L}", 13.5 if big else 12.5, INK, "khand", 700)
                + t(36 + 2 * r, y + r + 10, f"{ADDR}, {CITY}", 7.5, MUTE)), 2 * r + 8
    s = houseic(28, y, 32, LAGOON) + t(68, y + 14, ADDR, 13.5, INK, "khand", 700) + t(68, y + 26, f"{NAME_F}'s home  ·  {CITY}", 7.5, MUTE)
    return s, 40
def greet(y, on=True, size=16):
    return (t(28, y + size, f"Good morning, {NAME_F}", size, INK, "khand", 700), size + 8) if on else ("", 0)
def chip(x, y, txt, c, solid=False, h=15):
    w = len(txt) * 4.3 + 14
    return rect(x, y, w, h, c if solid else "#FFFFFF", "none" if solid else c, 8, .9) + t(x + w / 2, y + h * .69, txt, 7.5, "#FFFFFF" if solid else c, "hind", 600, "middle"), w
def plan(x, y, c=TERRA): return chip(x, y, "PLUS PLAN", c, True)
def info_row(y, kind, txt, c=INK, x=28):
    k = {"visit": "cal", "tech": "phone", "plan": "star"}[kind]
    if kind == "tech": g = avatar(x + 6, y + 6, 6, JUNGLE, "M")
    else: g = ic(k, x, y, 12, c, 2)
    return g + t(x + 17, y + 9.5, txt, 8, INK, "hind", 500), 17
BADGES = ["Certified Techs", "Licensed & Insured", "Background-Checked Yearly", "Moisture Scan Every Visit", "Cancel Anytime", "Home Reports"]
def tick(x, y, c): return f'<path d="M{x} {y} l2.6 2.6 l5 -5.4" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
def badge_row(y, c=JUNGLE, items=BADGES[:3]):
    x, s = 28, ""
    for b in items:
        w = len(b) * 4.25 + 24
        s += rect(x, y, w, 17, c + "12", c + "55", 8.5, .8) + tick(x + 7, y + 8.8, c) + t(x + 18, y + 11.6, b, 7.5, c, "hind", 600)
        x += w + 5
    return s, 24
def trust_line(y, c=JUNGLE):
    return tick(28, y + 7, c) + t(39, y + 9.8, "Licensed & Insured  ·  Certified Techs", 7.5, MUTE, "hind", 600), 16
def actions(y, c=LAGOON):
    s, w = "", 60
    items = [("Book", "cal"), ("Message Tech", "phone"), ("My Add-Ons", "tag")]
    for i, (lab, k) in enumerate(items):
        x = 28 + i * (w + 4)
        s += rect(x, y, w, 34, "#FFFFFF", LINE, 8, 1) + ic(k, x + w / 2 - 6, y + 5, 12, c, 2) + t(x + w / 2, y + 28, lab, 7.5, INK, "hind", 600, "middle")
    return s, 42
def skeleton(y, h_end=300):
    s = t(28, y + 12, "MY HOME", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"')
    yy = y + 18
    while yy < h_end:
        s += rect(28, yy, 184, 34, "#F6F4F0", "none", 8) + rect(36, yy + 9, 70, 6, "#E4DFD7", "none", 3) + rect(36, yy + 20, 110, 5, "#ECE8E2", "none", 3)
        yy += 42
    return s
def hero(y, h=104, c=LAGOON):
    cid = uid("hc")
    s = f'<clipPath id="{cid}"><rect x="{X0}" y="{y}" width="{SW}" height="{h}"/></clipPath><g clip-path="url(#{cid})">'
    s += rect(X0, y, SW, h, "#DCEAF0") + dot(186, y + 50, 8, SAFFRON + "AA") + rect(X0, y + h - 18, SW, 18, "#CFE3C9")
    cx, b = 120, y + h - 12
    s += f'<path d="M{cx-34} {b} V{b-26} L{cx} {b-50} L{cx+34} {b-26} V{b} Z" fill="#FFFFFF" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/>'
    s += f'<path d="M{cx-40} {b-22} L{cx} {b-54} L{cx+40} {b-22}" fill="none" stroke="{TERRA}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
    s += rect(cx - 6, b - 16, 12, 16, c + "88") + rect(cx - 25, b - 21, 11, 9, c + "33", c, 0, .8) + rect(cx + 14, b - 21, 11, 9, c + "33", c, 0, .8)
    s += rect(X0, y, SW, 42, "#FFFFFFCC") + "</g>"
    return s, h
def phone_strip(y, h, inner, label=None, fade=True):
    """Phone top cropped at y+h: dark bezel, screen x 20..220, white fade at the cut."""
    cid = uid("ps")
    s = rect(15, y - 5, 210, h + 5, INK, "none", 18) + rect(15, y + h - 20, 210, 20, INK)
    s += f'<clipPath id="{cid}"><rect x="{X0}" y="{y}" width="{SW}" height="{h}" rx="13"/></clipPath>'
    s += f'<g clip-path="url(#{cid})">' + rect(X0, y, SW, h, "#FFFFFF") + inner + "</g>" + rect(103, y + 3, 34, 8, INK, "none", 4)
    if fade:
        s += f'<defs><linearGradient id="{cid}f" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient></defs>'
        s += rect(10, y + h - 26, 220, 27, f"url(#{cid}f)")
    if label: s += t(28, y - 9, label.upper(), 7.5, MUTE, "hind", 600, extra='letter-spacing="1"')
    return s

# ---------------- one header system: a dict of choices -> drawn screen ----------------
BASE = dict(layout="standard", logo="corner", who="avatar", greet=False, info=("plan", "visit"), badges=None, actions=False,
            band=False, acc=TERRA, logo_c=TERRA, collapsed=False, app="member")
def screen(y, **kw):
    o = dict(BASE, **kw); acc = o["acc"]; s = ""; y0 = y
    if o["collapsed"]:  # slim sticky bar after scrolling
        s += rect(X0, y, SW, 50, BAND if o["band"] else "#FFFFFF") + status(y)[0]
        s += avatar(36, y + 30, 9, acc) + t(51, y + 34, f"{NAME_F} {NAME_L}", 11, INK, "khand", 700) + plan(150, y + 23, acc)[0] + ln(y + 50, X0, XR, BANDL)
        return s + skeleton(y + 54), y + 50
    if o["layout"] == "none_scrolled":  # header scrolled away: content only
        return status(y)[0] + skeleton(y + 14), y
    if o["layout"] == "hero":
        g, h = hero(y, 104); s += g; s += status(y)[0]; s += logo(y + 15, o["logo"], o["logo_c"])[0]; y += h + 8
        s += avatar(45, y + 15, 17, acc) + t(70, y + 13, f"{NAME_F} {NAME_L}", 13.5, INK, "khand", 700) + t(70, y + 25, f"{ADDR}, {CITY}", 7.5, MUTE); y += 40
        g, w = plan(28, y, acc); s += g; s += ic("cal", 28 + w + 8, y + 1.5, 12, INK, 2) + t(28 + w + 24, y + 11, "Next visit Tue, Nov 3", 8, INK, "hind", 500); y += 24
        return s + ln(y, X0, XR, BANDL) + skeleton(y + 6), y
    if o["layout"] == "compact":
        s += status(y)[0]; y += 16
        s += avatar(36, y + 13, 10, acc) + t(52, y + 13, f"{NAME_F} {NAME_L}", 12, INK, "khand", 700) + t(52, y + 23, "Next visit Tue, Nov 3", 7.5, MUTE)
        s += plan(146, y + 6, acc)[0] + shareic(201, y + 6, INK, 12); y += 30
        return s + ln(y, X0, XR, BANDL) + skeleton(y + 8), y
    hdr_bg = BAND if o["band"] else "#FFFFFF"
    s += status(y)[0]; y += 16
    if o["logo"] != "none": g, h = logo(y, o["logo"], o["logo_c"]); s += g; y += h + 4
    if o["greet"]: g, h = greet(y); s += g; y += h
    g, h = who(y, o["who"], acc, big=not o["greet"]); s += g; y += h
    info = o["info"]
    if "plan" in info and "visit" in info and "tech" not in info:
        g, w = plan(28, y, acc); s += g; s += ic("cal", 28 + w + 8, y + 1.5, 12, INK, 2) + t(28 + w + 24, y + 11, "Next visit Tue, Nov 3", 8, INK, "hind", 500); y += 22
    elif "tech" in info:
        g, w = plan(28, y, acc); s += g; y += 21
        for k, txt in (("visit", "Next visit  Tue, Nov 3  ·  9-11 AM"), ("tech", f"Your tech  {TECH}")):
            if k in info: g, h = info_row(y, k, txt, acc); s += g; y += h
        y += 3
    elif info == ("plan",):
        g, w = plan(28, y, acc); s += g; y += 22
    if o["badges"] == "row": g, h = badge_row(y, JUNGLE if acc == TERRA else acc); s += g; y += h
    elif o["badges"] == "line": g, h = trust_line(y); s += g; y += h
    if o["actions"]: g, h = actions(y + 2, LAGOON if acc == TERRA else acc); s += g; y += h + 2
    y += 4
    if hdr_bg != "#FFFFFF": s = rect(X0, y0, SW, y - y0, hdr_bg) + s
    if o.get("rule"): s += rect(X0, y - 1, SW, 3, acc)
    return s + ln(y, X0, XR, BANDL) + skeleton(y + 8), y
MH = 520  # phone-width picture box is tall: a 240x520 drawing (class mph-m) replaces the 240x300 one (mph-d) under 600px
def closeup(y, inner_at0, hh):
    """1.15x close-up of the header (screen drawn at y=0, rows 0..hh) placed at card y."""
    cid = uid("cu"); sc = 1.15
    return (t(14, y - 6, "CLOSE-UP", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"') + rect(4.5, y - .5, 231, hh * sc + 1, "#FFFFFF", LINE, 6, 1)
            + f'<clipPath id="{cid}"><rect x="5" y="{y}" width="230" height="{hh*sc:.1f}" rx="6"/></clipPath>'
            + f'<g clip-path="url(#{cid})"><g transform="translate(-18,{y}) scale({sc})">{inner_at0}</g></g>')
def full(**kw):
    d = phone_strip(34, 252, screen(34, **kw)[0])
    inner0, hy = screen(0, **kw); hh = min(hy + 2, 196)
    m = phone_strip(34, 252, screen(34, **kw)[0]) + closeup(306, inner0, hh)
    return d, m
def stack(la, ka, lb, kb, ha=118, hb=118):
    d = phone_strip(44, ha, screen(44, **ka)[0], la) + phone_strip(44 + ha + 22, hb, screen(44 + ha + 22, **kb)[0], lb)
    m = phone_strip(44, 230, screen(44, **ka)[0], la) + phone_strip(296, 210, screen(296, **kb)[0], lb)
    return d, m
def tech_screen(y, mode):
    """Technician app header. 'same' = same system as member (status, logo, avatar+name, chip, rows); 'own' = route band."""
    s = status(y)[0]; y0 = y; y += 16
    if mode == "same":
        s += logo(y, "corner", TERRA)[0]; y += 28
        s += avatar(42, y + 14, 14, LAGOON, "M") + t(64, y + 13, "Marco Example", 12.5, INK, "khand", 700) + t(64, y + 24, "Technician  ·  Van 4", 7.5, MUTE); y += 36
        g, w = chip(28, y, "TECHNICIAN", LAGOON, True); s += g; s += ic("cal", 28 + w + 8, y + 1.5, 12, INK, 2) + t(28 + w + 24, y + 11, "Today  5 visits", 8, INK, "hind", 500)
        return s
    s = rect(X0, y0, SW, 96, LAGOON) + status(y0, "#FFFFFF")[0]
    s += t(28, y + 14, "TODAY'S ROUTE", 7.5, "#FFFFFF", "hind", 600, extra='letter-spacing="1"') + t(28, y + 36, "5 Stops  ·  Van 4", 17, "#FFFFFF", "khand", 700)
    s += rect(28, y + 46, 184, 4, "#FFFFFF55", "none", 2) + rect(28, y + 46, 74, 4, "#FFFFFF", "none", 2) + t(28, y + 64, "Next: 123 Sample Lane  9:00 AM", 8, "#FFFFFF", "hind", 600)
    return s

# ---------------- the 10 picks ----------------
def frame(label, acc, body, H):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 {H}" width="240" height="{H}" class="{"mph-d" if H == 300 else "mph-m"}">'
         + rect(0, 0, 240, H, "#FFFFFF") + rect(0, 0, 240, 5, acc) + t(14, 22, label.upper(), 7.5, acc, "hind", 600, extra='letter-spacing="1.2"'))
    s += rect(152, 13, 74, 12, SAFFRON + "26", SAFFRON, 0, .8) + t(189, 21.6, "EXAMPLE DATA", 7.5, "#7A5A0C", "hind", 600, "middle", 'letter-spacing=".5"')
    return crisp(s + body + t(120, H - 3, "Built by Machan", 7.5, GREY, "hind", 400, "middle") + rect(.5, .5, 239, H - 1, "none", "#D6D0C6") + "</svg>")
def C(label, acc, body):
    d, m = body; return frame(label, acc, d, 300) + frame(label, acc, m, MH)
P = []
def pick(group, ask, a, b): P.append((group, ask, a, b))
pick("Layout", "Top of the profile: a home photo hero, or a compact name bar?",
     ("lay_hero", "Home Photo Hero", "Your house up top, name below", "premium", C("Layout", TERRA, full(layout="hero"))),
     ("lay_bar", "Compact Name Bar", "One slim row, more room below", "practical", C("Layout", TERRA, full(layout="compact"))))
pick("Identity", "Lead with the member, or with the house?",
     ("id_member", "Member Initials First", "Avatar and name lead", "calm", C("Identity", LAGOON, full(who="avatar", logo="none"))),
     ("id_house", "House And Address First", "The home leads, name second", "practical", C("Identity", LAGOON, full(who="house", logo="none"))))
pick("Info Shown", "How much membership info sits in the header?",
     ("info_full", "Plan, Visit And Tech", "Plan, next visit and your tech", "practical", C("Info Shown", JUNGLE, full(info=("plan", "visit", "tech")))),
     ("info_min", "Just The Plan Badge", "Only the plan; the rest below", "calm", C("Info Shown", JUNGLE, full(info=("plan",)))))
pick("Trust Badges", "Trust badges in the header: a chip row, or one quiet line?",
     ("tr_row", "Badge Chip Row", "Swipeable approved badges", "bold", C("Trust Badges", JUNGLE, full(badges="row", info=("plan",)))),
     ("tr_line", "One Quiet Trust Line", "Two badges as a single line", "calm", C("Trust Badges", JUNGLE, full(badges="line", info=("plan",)))))
pick("Logo", "Where does the Smart Upkeep mark sit?",
     ("logo_corner", "Logo In The Corner", "Mark top left, share top right", "practical", C("Logo", TERRA, full(logo="corner"))),
     ("logo_center", "Logo Centered", "Mark centered across the top", "premium", C("Logo", TERRA, full(logo="center"))))
pick("Greeting", "Say hello, or go straight to the name?",
     ("gr_on", "Good Morning, Sarah", "A warm time-of-day hello", "playful", C("Greeting", SAFFRON, full(greet=True))),
     ("gr_off", "No Greeting", "Name and plan, nothing extra", "calm", C("Greeting", SAFFRON, full(greet=False))))
pick("Quick Actions", "Quick action buttons under the name?",
     ("qa_on", "Quick Action Buttons", "Book, Message Tech, My Add-Ons", "practical", C("Quick Actions", LAGOON, full(actions=True))),
     ("qa_off", "No Quick Actions", "A clean header, actions below", "calm", C("Quick Actions", LAGOON, full(actions=False, info=("plan", "visit", "tech")))))
pick("Color", "Which color treatment for the header?",
     ("col_white", "White, Terracotta Pop", "Pure white with terracotta", "bold", C("Color", TERRA, full(acc=TERRA, logo_c=TERRA, rule=True, badges="line", info=("plan", "visit")))),
     ("col_band", "Soft Band, Lagoon Pop", "Light grey band, lagoon accents", "calm", C("Color", LAGOON, full(acc=LAGOON, logo_c=LAGOON, band=True, badges="line", info=("plan", "visit")))))
pick("On Scroll", "When the member scrolls, does the header shrink and stick, or scroll away?",
     ("sc_stick", "Shrinks And Sticks", "Slim bar stays on top", "practical", C("On Scroll", LAGOON, stack("At the top", {}, "After scrolling: slim bar stays", dict(collapsed=True), 128, 104))),
     ("sc_static", "Scrolls Away", "Header leaves with the page", "calm", C("On Scroll", LAGOON, stack("At the top", {}, "After scrolling: header gone", dict(layout="none_scrolled"), 128, 104))))
def tech_pair(mode):
    d = (phone_strip(44, 118, screen(44, info=("plan", "visit"))[0], "Member app")
         + phone_strip(184, 102, tech_screen(184, mode) + skeleton(184 + 100), "Technician app"))
    m = (phone_strip(44, 225, screen(44, info=("plan", "visit"))[0], "Member app")
         + phone_strip(296, 210, tech_screen(296, mode) + skeleton(296 + 100), "Technician app"))
    return d, m
pick("Tech App", "Same header for the tech app?",
     ("tech_same", "Same Header, Both Apps", "One system; tech swaps the details", "practical", C("Tech App", TERRA, tech_pair("same"))),
     ("tech_own", "Tech Gets Its Own", "A route-first band for techs", "bold", C("Tech App", TERRA, tech_pair("own"))))

FEEL = {"calm", "bold", "practical", "playful", "premium"}
if "--preview" in sys.argv:
    d = sys.argv[sys.argv.index("--preview") + 1]; os.makedirs(d, exist_ok=True)
    h = "<html><body style='margin:0;background:#fff;display:grid;grid-template-columns:repeat(4,360px);gap:10px;font-family:Hind'>"
    for g, ask, a, b in P:
        for o in (a, b): h += f"<div><div style='width:170px;display:inline-block;vertical-align:top'>{o[4].split('</svg>')[0]}</svg></div><div style='width:170px;display:inline-block'>{o[4].split('</svg>')[1]}</svg></div><b>{o[1]}</b></div>"
    open(os.path.join(d, "preview.html"), "w").write(h + "</body></html>"); print("preview", d); sys.exit()
assert len(P) == 10
pairs, O, add = kdeck("mph_", "UpKeep")
for grp, ask, a, b in P:
    for o in (a, b): assert len(o[1]) <= 24 and len(o[2]) <= 34 and o[3] in FEEL, o[:3]
    oa, ob = [O(o[0], o[1], o[2], o[3], o[4], tags=[grp, "member-app", "tech-app"]) for o in (a, b)]
    add(grp, grp, oa, ob, ask)
REQ = ('Max Oct 17 2026 18:56 ICT: "i want to establish a branded header/top portion for the technicians app that will be similar '
       'for the member app. please send me a swipe deck for the header/top portion of the member profile on upkeep"')
meta = {"brands": ["Smart Upkeep brand: white base, light grey band, terracotta, lagoon and jungle accents, Khand and Hind, light mode only. Trust badges: approved set only. No home health score."],
        "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": SLUG_KEY, "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True,
        "request": REQ, "applies_to": ["member app profile header", "technician app header"],
        "example_data": "Sarah Sample, 123 Sample Lane, Exampleville, Marco and all dates are placeholders.",
        "sources": {"content": "tools/build_member_profile_header.py", "brand": "smartkeep/funnel-app/member/index.html"}}
publish(DID, NAME, "UpKeep", pairs, meta, seed=1017, n=10, first=10)  # keep the drafted order: layout first, tech-app last
dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == 10
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or SLUG_KEY + "-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns)
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{DID}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}body.carding .opt .vis .v-svg svg{{min-height:0!important}}html body .vis svg.mph-m{{display:none!important}}@media(max-width:600px){{html body .vis svg.mph-d{{display:none!important}}html body .vis svg.mph-m{{display:block!important}}}}</style>
    {ns["SHARE"]}'''
from agent_links import patch as link_patch
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1).replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11")
os.makedirs(slug, exist_ok=True); pth = os.path.join(slug, "index.html"); open(pth, "w").write(s); link_patch(pth)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
rec = {"id": DID, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "total": 10, "topic": SLUG_KEY, "added": dj["generated_at"],
       "tag": "Max's Picks", "blurb": "10 cards, requested by Max", "requested": True,
       "pairs": [f'{p["optionA"]["label"]} vs {p["optionB"]["label"]}' for p in dj["pairs"]]}
print(json.dumps(rec, indent=1, ensure_ascii=False))
