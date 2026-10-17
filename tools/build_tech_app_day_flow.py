#!/usr/bin/env python3
"""Tech App Day Flow Deck (Branding, Oct 17 2026 ICT, for Max via UpKeep's whole-app tech review).
10 this-or-that picks on the tech app layout choices still open after the settled picks (map first, photo before tick,
Home History on the job card, full list then steps, slide to check in, member header system: white + accent pop, logo
centered, no greeting, quick action tiles, shrinks and sticks; tech = lagoon, header = the tech's own profile, house
photos only on job cards). Each option is a drawn tech app phone screen: 240x300 (class tad-d, desktop) and a taller
240x520 screen (class tad-m) under 600px, so the phone shows a real full-width screen. Example data only.
R105 captions ('Tech App <screen>: <element>, <one sentence>') guarded by tools/caption_rule.py.
Page written UNLOCKED: lock before commit.   usage: build_tech_app_day_flow.py [--preview DIR]"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets
from draft_svg import t, rect, dot, ln, ic, INK, MUTE, LINE, TERRA, LAGOON, JUNGLE, SAFFRON, crisp
from team_kit import deck as kdeck, publish, shareic
from uk5_art import mark, wordmark, GREY
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UPKEEP = "UpKeep Agent f0d420ad-d37e-44d3-be6f-053da2b6e24d"
DID = "upkeep-tech-app-day-flow-deck"; NAME = "Tech App Day Flow Deck"; SLUG_KEY = "tech-app-day-flow"
CREAM = "#FAF6EE"; BANDL = "#E2DED7"; X0, SW = 20, 200; XR = X0 + SW; L, R = 28, 212
LT = LAGOON + "14"  # light lagoon tint
TECH, INIT, VAN = "Marco Example", "ME", "Van 4  ·  Oakland County"
STOPS = [("123 Sample Lane", "8:00 to 9:00 AM", "Plus", "8:25"), ("48 Example Court", "9:30 to 10:30 AM", "Complete", "9:48"),
         ("7 Placeholder Road", "11:00 to 12:00", "Plus", "11:26"), ("910 Demo Avenue", "12:30 to 1:30 PM", "Plus", "12:58"),
         ("22 Test Street", "2:00 to 3:00 PM", "Complete", "2:31")]
_n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"

# ---------------- pieces (screen x 20..220) ----------------
def status(y, c=INK):
    return t(28, y + 9, "9:41", 7.5, c, "hind", 600) + rect(200, y + 4, 11, 5.5, "none", c, 1, .8) + rect(201.2, y + 5.2, 7, 3.1, c), 14
def topbar(y, extra=""):
    s = shareic(28, y + 4, INK, 12) + mark(91, y + 10, 7, "#FFFFFF", LAGOON) + wordmark(101, y + 14.5, 12)
    return s + extra, 24
def avatar(cx, cy, r, c=LAGOON, ch=INIT):
    return dot(cx, cy, r, c) + t(cx, cy + r * .36, ch, r * .95, "#FFFFFF", "khand", 700, "middle")
def chip(x, y, txt, c, solid=False, h=14, anchor="start"):
    w = len(txt) * 4.4 + 14
    if anchor == "middle": x = x - w / 2
    return rect(x, y, w, h, c if solid else "#FFFFFF", "none" if solid else c, 7, .9) + t(x + w / 2, y + h * .7, txt, 7.5, "#FFFFFF" if solid else c, "hind", 600, "middle"), w
def profile(y, style="left", today="5 stops today"):
    """Tech's own profile header, white with a lagoon pop (member header system, tech colour)."""
    s = ""
    if style == "left":
        s += avatar(46, y + 18, 18) + t(72, y + 14, TECH, 13.5, INK, "khand", 700) + t(72, y + 26, VAN, 7.5, MUTE)
        g, w = chip(72, y + 31, "TECHNICIAN", LAGOON, True); s += g
        s += t(72 + w + 6, y + 41.5, today, 7.5, LAGOON, "hind", 600); h = 52
    else:
        s += avatar(120, y + 21, 20) + t(120, y + 56, TECH, 13.5, INK, "khand", 700, "middle") + t(120, y + 67, VAN, 7.5, MUTE, anchor="middle")
        g, w = chip(120, y + 72, "TECHNICIAN", LAGOON, True, anchor="middle"); s += g; h = 92
    return s + rect(X0, y + h, SW, 2.5, LAGOON), h + 3
def tiles(y):
    s, w = "", 58
    for i, (lab, k) in enumerate((("Start Route", "chev"), ("Van Stock", "tag"), ("Message", "phone"))):
        x = L + i * (w + 5)
        s += rect(x, y, w, 32, "#FFFFFF", LINE, 8, 1) + ic(k, x + w / 2 - 6, y + 4, 12, LAGOON, 2) + t(x + w / 2, y + 27, lab, 7.5, INK, "hind", 600, "middle")
    return s, 38
def label(y, txt, c=MUTE, right=None, rc=LAGOON):
    s = t(L, y + 9, txt.upper(), 7.5, c, "hind", 600, extra='letter-spacing="1"')
    if right: s += t(R, y + 9, right, 7.5, rc, "hind", 600, "end")
    return s, 14
def mapbox(y, h=70, done=0):
    cid = uid("mp"); s = f'<clipPath id="{cid}"><rect x="{L}" y="{y}" width="184" height="{h}" rx="8"/></clipPath><g clip-path="url(#{cid})">'
    s += rect(L, y, 184, h, "#EEF3F0")
    for i in range(1, 5): s += f'<line x1="{L}" y1="{y+h*i/5}" x2="{R}" y2="{y+h*i/5-6}" stroke="#FFFFFF" stroke-width="3"/>'
    for i in range(1, 6): s += f'<line x1="{L+184*i/6}" y1="{y}" x2="{L+184*i/6+8}" y2="{y+h}" stroke="#FFFFFF" stroke-width="3"/>'
    pts = [(L + 30, y + h * .72), (L + 64, y + h * .38), (L + 104, y + h * .55), (L + 140, y + h * .25), (L + 166, y + h * .62)]
    s += '<polyline points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + f'" fill="none" stroke="{LAGOON}" stroke-width="1.6" stroke-dasharray="3 2"/>'
    for i, (a, b) in enumerate(pts):
        c = JUNGLE if i < done else (TERRA if i == done else LAGOON)
        s += dot(a, b, 7, c) + t(a, b + 3, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle")
    return s + "</g>" + rect(L, y, 184, h, "none", LINE, 8, 1), h + 6
def house(x, y, w, h, c=LAGOON, r=6):
    cid = uid("hs"); s = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath><g clip-path="url(#{cid})">'
    s += rect(x, y, w, h, "#DCEAF0") + rect(x, y + h * .78, w, h * .22, "#CFE3C9")
    cx, b, hw = x + w / 2, y + h * .86, min(w * .3, h * .42)
    s += f'<path d="M{cx-hw} {b} V{b-hw*.75} L{cx} {b-hw*1.35} L{cx+hw} {b-hw*.75} V{b} Z" fill="#FFFFFF" stroke="{c}" stroke-width="1.2" stroke-linejoin="round"/>'
    s += f'<path d="M{cx-hw*1.15} {b-hw*.65} L{cx} {b-hw*1.45} L{cx+hw*1.15} {b-hw*.65}" fill="none" stroke="{TERRA}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
    s += rect(cx - hw * .18, b - hw * .5, hw * .36, hw * .5, c + "88")
    return s + "</g>", h
def stop_row(y, i, thumb=True, cur=False):
    a, win, plan, eta = STOPS[i]; h = 34
    s = rect(L, y, 184, h, LT if cur else "#FFFFFF", LAGOON if cur else LINE, 7, 1)
    s += dot(L + 12, y + h / 2, 7, TERRA if cur else LAGOON) + t(L + 12, y + h / 2 + 3, str(i + 1), 7.5, "#FFFFFF", "hind", 700, "middle")
    s += t(L + 24, y + 14, a, 9.5, INK, "khand", 700) + t(L + 24, y + 26, f"{eta}  ·  {plan}", 7.5, MUTE)
    if thumb: s += house(R - 40, y + 4, 34, h - 8, LAGOON, 4)[0]
    return s, h + 5
def watch_chip(x, y): return chip(x, y, "Watch: AC", TERRA)
def jobcard(y, i=0, full=False, slide=True, maxy=999):
    a, win, plan, eta = STOPS[i]; y0 = y; s = ""
    s += house(L, y, 184, 50, LAGOON, 8)[0] + rect(L, y + 34, 184, 16, "#FFFFFFCC") + t(L + 8, y + 46, a, 10, INK, "khand", 700); y += 54
    s += t(L + 8, y + 9, f"STOP {i+1}  ·  NEXT", 7.5, TERRA, "hind", 600, extra='letter-spacing="1"'); y += 13
    g, w = chip(L + 8, y, win, LAGOON); s += g; s += t(L + 14 + w, y + 10, f"{plan} plan", 7.5, MUTE); y += 18
    if not full:
        g, w = watch_chip(L + 8, y); s += g; s += chip(L + 14 + w, y, "5 tasks", JUNGLE)[0]; s += chip(L + 14 + w + 48, y, "Bring 4", MUTE)[0]; y += 18
        s += t(L + 8, y + 9, "Tap to open tasks, bring list, history", 7.5, LAGOON, "hind", 600); y += 14
    else:
        s += t(L + 8, y + 9, "Watch: Central AC, plan replacement", 7.5, TERRA, "hind", 600); y += 13
        s += label(y - 1, "Tasks")[0]; y += 12
        for tk in ("Mold and moisture scan", "Furnace filter, 2 x 20x25x1", "Smoke and CO checks (4)", "Fridge water filter"):
            if y > maxy - 52: break
            s += rect(L + 8, y + 1, 8, 8, "#FFFFFF", "#BDB6AA", 2, 1) + t(L + 21, y + 8.5, tk, 7.5, INK); y += 11
        if y < maxy - 80:
            s += label(y, "Bring")[0]; y += 13
            for tk in ("Gloves x 2", "Shoe covers x 2", "Filter 20x25x1 x 2"):
                if y > maxy - 62: break
                s += t(L + 8, y + 8, "·  " + tk, 7.5, INK); y += 10
        s += t(L + 8, y + 9, "This Home's History", 7.5, LAGOON, "hind", 600, extra='text-decoration="underline"'); y += 13
    if slide:
        s += slider(L + 6, y, 172)[0]; y += 26
    s = rect(L, y0, 184, y - y0 + 4, "#FFFFFF", LINE, 8, 1) + s
    return s, y - y0 + 9
def slider(x, y, w, txt="SLIDE TO CHECK IN"):
    return rect(x, y, w, 22, LT, LAGOON, 11, 1) + dot(x + 11, y + 11, 9, LAGOON) + ic("chev", x + 5, y + 5, 12, "#FFFFFF", 2.4) + t(x + w / 2 + 8, y + 14.5, txt, 7.5, LAGOON, "hind", 700, "middle", 'letter-spacing=".8"'), 22
def navbar(y, style="four"):
    s = rect(X0, y, SW, 34, "#FFFFFF") + ln(y, X0, XR, BANDL)
    if style == "four":
        for i, (lab, k) in enumerate((("Today", "clock"), ("Stop", "home"), ("Van", "tag"), ("Messages", "phone"))):
            cx = X0 + 25 + i * 50; c = LAGOON if i == 0 else MUTE
            s += ic(k, cx - 6, y + 5, 12, c, 2) + t(cx, y + 27, lab, 7.5, c, "hind", 600, "middle")
        s += rect(X0 + 12, y, 26, 2.5, LAGOON)
    else:
        for i, (lab, k) in enumerate((("Today", "clock"), ("Van", "tag"), ("", None), ("Messages", "phone"), ("Profile", "star"))):
            cx = X0 + 20 + i * 40
            if k is None:
                s += dot(cx, y + 6, 17, "#FFFFFF") + dot(cx, y + 6, 15, LAGOON) + ic("home", cx - 7, y - 2, 14, "#FFFFFF", 2.2) + t(cx, y + 30, "Stop 1", 7.5, LAGOON, "hind", 700, "middle"); continue
            c = LAGOON if i == 0 else MUTE
            s += ic(k, cx - 6, y + 5, 12, c, 2) + t(cx, y + 27, lab, 7.5, c, "hind", 600, "middle")
    return s
def skeleton(y, yend):
    s = ""
    while y + 30 < yend:
        s += rect(L, y, 184, 28, "#F6F4F0", "none", 8) + rect(L + 8, y + 8, 70, 5, "#E4DFD7", "none", 3) + rect(L + 8, y + 17, 110, 4, "#ECE8E2", "none", 3); y += 34
    return s
def summary(y, style):
    if style == "stats":
        s, w = "", 43
        for i, (v, l) in enumerate((("5", "stops"), ("28", "miles"), ("8:25", "first stop"), ("3:40", "done by"))):
            x = L + i * (w + 4.3); c = [LAGOON, JUNGLE, TERRA, LAGOON][i]
            s += rect(x, y, w, 34, "#FFFFFF", LINE, 7, 1) + t(x + 6, y + 17, v, 13, c, "khand", 700) + t(x + 6, y + 28, l, 7.5, MUTE)
        return s, 40
    s = t(L, y + 12, "Stop 1 of 5", 12, INK, "khand", 700) + t(R, y + 11, "Next 8:25 AM", 7.5, LAGOON, "hind", 600, "end")
    s += rect(L, y + 17, 184, 6, "#EEEAE4", "none", 3) + rect(L, y + 17, 18, 6, LAGOON, "none", 3)
    for i in range(1, 5): s += rect(L + 184 * i / 5 - .5, y + 17, 1, 6, "#FFFFFF")
    s += t(L, y + 34, "28 miles  ·  done by about 3:40 PM", 7.5, MUTE)
    return s, 40

# ---------------- phone frame + screen composer ----------------
def phone(y, h, inner, bottom=""):
    cid = uid("ph")
    s = rect(15, y - 5, 210, h + 10, INK, "none", 18)
    s += f'<clipPath id="{cid}"><rect x="{X0}" y="{y}" width="{SW}" height="{h}" rx="13"/></clipPath>'
    s += f'<g clip-path="url(#{cid})">' + rect(X0, y, SW, h, "#FFFFFF") + inner + bottom + "</g>" + rect(103, y + 3, 34, 8, INK, "none", 4)
    return s
def build(y, h, parts, nav=None, sticky=None, header=True, hstyle="left", bg="#FFFFFF", today="5 stops today"):
    """parts: list of callables f(y, yend) -> (svg, height). nav/sticky drawn fixed at the bottom."""
    yend = y + h - (34 if nav else 0) - (30 if sticky else 0)
    s = rect(X0, y, SW, h, bg) + status(y)[0]; yy = y + 15
    if header == "slim":  # settled: header shrinks and sticks after scrolling (member + tech)
        s += avatar(38, yy + 12, 10) + t(54, yy + 11, TECH, 11, INK, "khand", 700) + t(54, yy + 21, today, 7.5, LAGOON, "hind", 600)
        s += chip(R - 58, yy + 5, "TECHNICIAN", LAGOON, True)[0]
        s += rect(X0, yy + 26, SW, 2.5, LAGOON); yy += 34
    elif header:
        g, hh = topbar(yy); s += g; yy += hh
        g, hh = profile(yy, hstyle, today); s += g; yy += hh + 6
    for f in parts:
        if yy > yend - 8: break
        g, hh = f(yy, yend); s += g; yy += hh
    bot = ""
    if sticky: bot += rect(X0, yend, SW, 30, "#FFFFFF") + ln(yend, X0, XR, BANDL) + sticky(yend + 4)
    if nav: bot += navbar(y + h - 34, nav)
    return phone(y, h, s, bot)
def frame(lab, body, H):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 {H}" width="240" height="{H}" class="{"tad-d" if H == 300 else "tad-m"}">'
         + rect(0, 0, 240, H, "#FFFFFF") + rect(0, 0, 240, 5, LAGOON) + t(14, 22, lab.upper(), 7.5, LAGOON, "hind", 600, extra='letter-spacing="1.2"'))
    s += rect(152, 13, 74, 12, SAFFRON + "26", SAFFRON, 0, .8) + t(189, 21.6, "EXAMPLE DATA", 7.5, "#7A5A0C", "hind", 600, "middle", 'letter-spacing=".5"')
    return crisp(s + body + t(120, H - 3, "Built by Machan", 7.5, GREY, "hind", 400, "middle") + rect(.5, .5, 239, H - 1, "none", "#D6D0C6") + "</svg>")
def C(lab, dfull=False, **kw):
    """Same screen at two heights: desktop 240x300 (phone 34..286) and phone-width 240x520 (phone 34..506).
    Desktop shows the slim stuck header (settled scroll behaviour) unless the pick is about the header itself (dfull)."""
    kd = dict(kw)
    if not dfull and kd.get("header", True) is True: kd["header"] = "slim"
    return frame(lab, build(34, 250, **kd), 300) + frame(lab, build(34, 470, **kw), 520)
# part helpers
P_ = lambda fn: fn
def p_label(txt, right=None): return lambda y, e: label(y, txt, right=right)
def p_map(h=70, done=0): return lambda y, e: mapbox(y, h, done)
def p_tiles(): return lambda y, e: tiles(y)
def p_summary(st): return lambda y, e: summary(y, st)
def p_rows(n=5, thumb=True, start=0, cur=True):
    def f(y, e):
        s, yy = "", y
        for i in range(start, n):
            if yy + 34 > e: break
            g, h = stop_row(yy, i, thumb, cur=(cur and i == start)); s += g; yy += h
        return s, yy - y
    return f
def p_job(full=False, slide=True): return lambda y, e: jobcard(y, 0, full, slide, e)
def p_carousel():
    def f(y, e):
        g, h = jobcard(y, 0, False, True, e)
        cid = uid("cr"); peek = f'<clipPath id="{cid}"><rect x="{L}" y="{y}" width="184" height="{h}"/></clipPath>'
        s = f'<g transform="translate(-14,0)">{g}</g>' + peek + f'<g clip-path="url(#{cid})"><g transform="translate(176,0)">{jobcard(y, 1, False, True, e)[0]}</g></g>'
        dots = "".join(dot(120 - 16 + i * 8, y + h + 2, 2.4, LAGOON if i == 0 else "#D6D0C6") for i in range(5))
        return s + dots, h + 10
    return f
def p_skel(): return lambda y, e: (skeleton(y, e), e - y)
def p_raw(fn): return fn

# ---------------- the 10 picks ----------------
P = []
def pick(group, ask, a, b): P.append((group, ask, a, b))
pick("Profile Header", "Tech App Today: Profile header, should the tech's headshot sit left of the name or centered above it?",
     ("hdr_left", "Headshot Left Of Name", "Compact row, more of the day shows", "practical", C("Profile Header", dfull=True, parts=[p_tiles(), p_label("Today's route"), p_map(60), p_rows(3)], nav="four")),
     ("hdr_center", "Centered Headshot", "Profile card feel, name centered", "premium", C("Profile Header", dfull=True, hstyle="center", parts=[p_tiles(), p_label("Today's route"), p_map(60), p_rows(3)], nav="four")))
pick("Day Summary", "Tech App Today: Day summary, does the top of the day show four quick numbers or one progress bar?",
     ("sum_stats", "Four Quick Numbers", "Stops, miles, first stop, done by", "practical", C("Day Summary", parts=[p_summary("stats"), p_map(64), p_rows(3)], nav="four")),
     ("sum_bar", "One Progress Bar", "Stop 1 of 5 with a filling bar", "calm", C("Day Summary", parts=[p_summary("bar"), p_map(64), p_rows(3)], nav="four")))
pick("Stops", "Tech App Today: Stop list, are the day's stops a short list under the map or one swipeable card at a time?",
     ("stops_list", "Short List Under Map", "All stops as slim rows", "practical", C("Stops", parts=[p_label("Today's route", "5 stops"), p_map(70), p_rows(5)], nav="four")),
     ("stops_carousel", "Swipe One Card At A Time", "Next stop big, swipe for the rest", "bold", C("Stops", parts=[p_label("Today's route", "1 of 5"), p_map(70), p_carousel()], nav="four")))
pick("Job Card", "Tech App Today: Job card, does each stop open as a short summary or show the full task and bring list?",
     ("job_short", "Short Summary Card", "Address, window, tap to open", "calm", C("Job Card", header=False, parts=[p_label("Stop 1 of 5"), p_job(False), p_rows(5, True, 1, False)], nav="four")),
     ("job_full", "Full Card Open", "Tasks and bring list on the card", "practical", C("Job Card", header=False, parts=[p_label("Stop 1 of 5"), p_job(True), p_rows(5, True, 1, False)], nav="four")))
pick("Navigation Bar", "Tech App Today: Navigation bar, is it four plain tabs or tabs with a raised Current Stop button in the middle?",
     ("nav_four", "Four Plain Tabs", "Today, Stop, Van, Messages", "calm", C("Navigation Bar", parts=[p_summary("bar"), p_map(64), p_rows(3)], nav="four")),
     ("nav_center", "Raised Current Stop", "Middle button jumps to your stop", "bold", C("Navigation Bar", parts=[p_summary("bar"), p_map(64), p_rows(3)], nav="center")))
def stick(y): return slider(L, y, 184, "SLIDE TO CHECK IN  ·  STOP 1")[0]
pick("Check In", "Tech App Today: Check-in slider, does it sit inside each job card or stay pinned at the bottom for the next stop?",
     ("ci_card", "Inside Each Job Card", "Slide on the card you are reading", "practical", C("Check In", header=False, parts=[p_label("Stop 1 of 5"), p_job(False, True), p_rows(5, True, 1, False)], nav="four")),
     ("ci_sticky", "Pinned At The Bottom", "One slider for the next stop", "bold", C("Check In", header=False, parts=[p_label("Stop 1 of 5"), p_job(False, False), p_rows(5, True, 1, False)], nav="four", sticky=stick)))
# photo capture: after the shutter
def walk_head(y, e, step="Step 3 of 9"):
    s = t(L, y + 9, "123 SAMPLE LANE  ·  WALKTHROUGH", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"') + t(L, y + 26, "Furnace Filter", 15, INK, "khand", 700) + t(R, y + 24, step, 7.5, LAGOON, "hind", 600, "end")
    return s + rect(L, y + 31, 184, 4, "#EEEAE4", "none", 2) + rect(L, y + 31, 61, 4, LAGOON, "none", 2), 42
def photo_confirm(y, e):
    s = rect(L, y, 184, 150, "#1F1F1F", "none", 8) + house(L + 8, y + 8, 168, 108, LAGOON, 4)[0]
    s += t(L + 92, y + 64, "Before photo", 9, "#FFFFFF", "khand", 700, "middle")
    s += rect(L + 8, y + 122, 80, 22, "#FFFFFF", "none", 11) + t(L + 48, y + 136.5, "RETAKE", 7.5, INK, "hind", 700, "middle", 'letter-spacing=".8"')
    s += rect(L + 96, y + 122, 80, 22, LAGOON, "none", 11) + t(L + 136, y + 136.5, "USE PHOTO", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return s, 156
def photo_instant(y, e):
    s = rect(L, y, 184, 66, "#FFFFFF", LINE, 8, 1) + house(L + 8, y + 8, 60, 50, LAGOON, 4)[0] + ic("check", L + 56, y + 10, 10, JUNGLE, 2.2)
    s += t(L + 76, y + 22, "Before photo saved", 9.5, INK, "khand", 700) + t(L + 76, y + 34, "Step can start now", 7.5, MUTE)
    s += rect(L + 76, y + 40, 48, 18, "#FFFFFF", LAGOON, 9, 1) + t(L + 100, y + 52, "UNDO", 7.5, LAGOON, "hind", 700, "middle")
    y2 = y + 72
    s += label(y2, "Step tasks")[0]
    for i, tk in enumerate(("Pull old filter", "Note size and date", "Fit new filter, arrow up")):
        s += rect(L, y2 + 16 + i * 14, 9, 9, "#FFFFFF", "#BDB6AA", 2, 1) + t(L + 14, y2 + 24 + i * 14, tk, 7.5, INK)
    s += rect(L, y2 + 64, 184, 22, LAGOON, "none", 11) + t(120, y2 + 78.5, "START STEP", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return s, 160
pick("Photo Capture", "Tech App Walkthrough: Photo capture, after the shutter does the tech confirm the shot or does it save at once with an undo?",
     ("ph_confirm", "Confirm Each Shot", "Retake or Use Photo, then go on", "calm", C("Photo Capture", header=False, parts=[walk_head, photo_confirm, p_skel()])),
     ("ph_instant", "Saves At Once, Undo", "No extra tap, undo if blurry", "practical", C("Photo Capture", header=False, parts=[walk_head, photo_instant, p_skel()])))
# end of day
def eod_summary(y, e):
    s = t(L, y + 14, "Day Done", 16, INK, "khand", 700) + t(L, y + 26, "Mon, Feb 15  ·  5 of 5 stops", 7.5, MUTE); y2 = y + 34
    g, _ = summary(y2, "stats"); s += g
    s += rect(L, y2 + 44, 184, 40, LT, "none", 8) + t(L + 8, y2 + 58, "5 reports sent to members", 8, INK, "hind", 600) + t(L + 8, y2 + 72, "42 photos  ·  2 rechecks set", 7.5, MUTE)
    s += rect(L, y2 + 92, 184, 22, LAGOON, "none", 11) + t(120, y2 + 106.5, "CHECK OUT FOR THE DAY", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return s, y2 + 120 - y
def eod_list(y, e):
    s = t(L, y + 14, "Before You Head Home", 16, INK, "khand", 700) + t(L, y + 26, "3 of 4 done", 7.5, MUTE); y2 = y + 34
    for i, (tk, ok) in enumerate((("All 5 reports sent", True), ("Van stock counted", True), ("Restock request sent", True), ("Van locked and parked", False))):
        yy = y2 + i * 22
        s += (rect(L, yy + 3, 12, 12, JUNGLE, "none", 3) + f'<path d="M{L+3} {yy+9} l2.5 2.5 4.5 -5" fill="none" stroke="#FFFFFF" stroke-width="1.8"/>' if ok else rect(L, yy + 3, 12, 12, "#FFFFFF", "#BDB6AA", 3, 1.2))
        s += t(L + 20, yy + 12.5, tk, 8.5, MUTE if ok else INK, "hind", 500) + ln(yy + 19, L + 20, R)
    s += rect(L, y2 + 94, 184, 22, LAGOON + "55", "none", 11) + t(120, y2 + 108.5, "CHECK OUT FOR THE DAY", 7.5, "#FFFFFF", "hind", 700, "middle", 'letter-spacing=".8"')
    return s, y2 + 122 - y
pick("End Of Day", "Tech App Wrap-Up: End of day, does the day close with a summary of numbers or a short checklist to tick?",
     ("eod_sum", "Summary Of The Day", "Stops, reports, photos at a glance", "premium", C("End Of Day", parts=[eod_summary, p_skel()], nav="four")),
     ("eod_list", "Short Checklist", "Tick the last jobs, then check out", "practical", C("End Of Day", parts=[eod_list, p_skel()], nav="four")))
# offline
def off_banner(y, e):
    return rect(X0, y - 6, SW, 26, SAFFRON + "22") + rect(X0, y - 6, 3, 26, SAFFRON) + ic("clock", L, y - 1, 12, "#7A5A0C", 2) + t(L + 17, y + 6, "Offline. 3 photos saved on this phone.", 7.5, "#5C4408", "hind", 600) + t(L + 17, y + 16, "They send when signal is back.", 7.5, "#5C4408"), 26
def off_chip(y, e):
    g, w = chip(L, y, "Offline  ·  3 waiting", SAFFRON); return g.replace(f'fill="{SAFFRON}" text-anchor', 'fill="#7A5A0C" text-anchor'), 20
pick("Offline", "Tech App Today: Offline status, is no signal shown as a full-width banner or a small chip under the header?",
     ("off_banner", "Full-Width Banner", "Hard to miss, says what is saved", "bold", C("Offline", parts=[off_banner, p_summary("bar"), p_map(60, 2), p_rows(5, True, 2)], nav="four")),
     ("off_chip", "Small Status Chip", "Quiet, tap it for details", "calm", C("Offline", parts=[off_chip, p_summary("bar"), p_map(60, 2), p_rows(5, True, 2)], nav="four")))
# empty day
def empty_calm(y, e):
    s = rect(L, y, 184, 96, CREAM, "none", 10) + ic("cal", 108, y + 14, 24, LAGOON, 1.8)
    s += t(120, y + 54, "No Stops Today", 14, INK, "khand", 700, "middle") + t(120, y + 66, "Your next route is Tue, Feb 16", 7.5, MUTE, anchor="middle") + t(120, y + 78, "4 stops  ·  first at 8:00 AM", 7.5, LAGOON, "hind", 600, "middle")
    return s, 104
def empty_tasks(y, e):
    s = t(L, y + 12, "No Stops Today", 13, INK, "khand", 700) + t(R, y + 11, "Next route Tue", 7.5, LAGOON, "hind", 600, "end"); y2 = y + 18
    s += label(y2, "Good use of today")[0]
    for i, (tk, sub, k) in enumerate((("Count van stock", "12 items to check", "tag"), ("Finish a training video", "Moisture scan basics", "play"), ("Renew OSHA 10", "Due in 30 days", "star"))):
        yy = y2 + 16 + i * 32
        s += rect(L, yy, 184, 28, "#FFFFFF", LINE, 7, 1) + rect(L + 6, yy + 5, 18, 18, LAGOON + "1F", "none", 5) + ic(k, L + 9, yy + 8, 12, LAGOON, 2)
        s += t(L + 30, yy + 12, tk, 9, INK, "khand", 700) + t(L + 30, yy + 23, sub, 7.5, MUTE)
    return s, 16 + 3 * 32 + 22
pick("Empty Day", "Tech App Today: Empty day, when there are no stops does the screen stay calm or offer useful tasks?",
     ("empty_calm", "Calm, Shows Next Route", "One card with the next route day", "calm", C("Empty Day", today="No stops today", parts=[p_tiles(), empty_calm, p_skel()], nav="four")),
     ("empty_tasks", "Offers Useful Tasks", "Van count, training, cert renewals", "practical", C("Empty Day", today="No stops today", parts=[p_tiles(), empty_tasks, p_skel()], nav="four")))

FEEL = {"calm", "bold", "practical", "playful", "premium"}
if "--preview" in sys.argv:
    d = sys.argv[sys.argv.index("--preview") + 1]; os.makedirs(d, exist_ok=True)
    h = "<html><body style='margin:0;background:#fff;display:grid;grid-template-columns:repeat(4,250px 250px);gap:6px;font-family:Hind'>"
    for g, ask, a, b in P:
        for o in (a, b):
            d1, m1 = o[4].split("</svg>")[:2]
            h += f"<div style='width:250px'>{d1}</svg><b>{o[1]}</b></div><div style='width:250px'>{m1}</svg></div>"
    open(os.path.join(d, "preview.html"), "w").write(h + "</body></html>"); print("preview", d); sys.exit()
assert len(P) == 10
import caption_rule
pairs, O, add = kdeck("tad_", "UpKeep")
for grp, ask, a, b in P:
    assert not caption_rule.check(ask), (ask, caption_rule.check(ask))
    for o in (a, b): assert len(o[1]) <= 24 and len(o[2]) <= 34 and o[3] in FEEL, o[:3]
    oa, ob = [O(o[0], o[1], o[2], o[3], o[4], tags=[grp, "tech-app"]) for o in (a, b)]
    add(grp, grp, oa, ob, ask)
REQ = ("Max Oct 17 2026 ICT: UpKeep reviews and remakes the whole Smart Upkeep technician app (tech/?dash=1-3); Branding gives design input "
       "and a deck on the layout choices still open.")
meta = {"brands": ["Smart Upkeep brand: white or warm cream base, terracotta, lagoon and jungle pops (tech app = lagoon), Khand and Hind, light mode only, 44px tap targets. Header = the tech's own profile; house photos only on job cards."],
        "submit_agent": "upkeep", "submit_to": UPKEEP, "topic": SLUG_KEY, "deck_size": 10, "board": "upkeep", "audience": "Max", "requested": True,
        "request": REQ, "applies_to": ["technician app (tech/)"], "follow_on_of": ["upkeep-member-profile-header-deck", "upkeep-technician-page-walkthrough-and-check-in-deck", "upkeep-technician-page-deck-checklist-today"],
        "not_reasked": ["map first", "photo before tick", "Home History on the job card", "full list then steps", "slide to check in", "member header system (white + accent, logo centered, no greeting, quick action tiles, shrinks and sticks)"],
        "example_data": "Marco Example, 123 Sample Lane and all addresses, times and counts are placeholders.",
        "design_input": "ops/brand/tech-app-review.md",
        "sources": {"content": "tools/build_tech_app_day_flow.py", "review": "smartkeep/updates-oct17/tech-review/"}}
publish(DID, NAME, "UpKeep", pairs, meta, seed=1017, n=10, first=10)  # drafted order kept
dj = json.load(open(f"decks/{DID}.json")); assert len(dj["pairs"]) == 10
caption_rule.guard(dj["pairs"], DID)
pages = json.load(open("decks/pages.json"))
slug = pages.get(DID) or SLUG_KEY + "-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns)
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{DID}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}body.carding .opt .vis .v-svg svg{{min-height:0!important}}html body .vis svg.tad-m{{display:none!important}}@media(max-width:600px){{html body .vis svg.tad-d{{display:none!important}}html body .vis svg.tad-m{{display:block!important}}}}</style>
    {ns["SHARE"]}'''
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); pth = os.path.join(slug, "index.html"); open(pth, "w").write(s); link_patch(pth); chat_patch(pth)
h = open(pth).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(pth, "w").write(h)
pages[DID] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
rec = {"id": DID, "name": NAME, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "total": 10, "topic": SLUG_KEY, "added": dj["generated_at"],
       "tag": "Technician", "blurb": "10 cards: tech app layout picks still open", "requested": True, "refill": True,
       "pairs": [f'{p["optionA"]["label"]} vs {p["optionB"]["label"]}' for p in dj["pairs"]]}
print(json.dumps(rec, indent=1, ensure_ascii=False))
