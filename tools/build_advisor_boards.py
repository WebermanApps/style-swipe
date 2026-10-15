#!/usr/bin/env python3
"""Build Style Swipe deck pairs for 'Advisor Boards Deck' (Oct 15 2026, Max 13:45 ICT + update): 20 this-or-that pairs on
thumbnails and carousels for the Research, Coach, Legal and Security boards (ideas sections first). Real board content.
White + light beige, square corners, Khand/Hind, no emoji, labels >= 8 units. Writes pairs JSON for tools/ready_shelf.py build --source.
Submit -> branding."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, phone
B = dict(name="Agent", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=0, hw=600)
INK, MUTE, LN, BG, BB = "#0A0A0A", "#525252", "#E5E5E5", "#FAF6EE", "#E3DDD2"; ACC = B["acc"]; WH = "#FFFFFF"; RED, AMB, GRN = "#B42318", "#B54708", JUNGLE
pairs, O, add = deck("ab_", "Branding")
def P(grp, ask, a, b): add(grp, grp, O(*a), O(*b), ask)
def tx(x, y, s, sz=8, c=INK, h=False, w=None, a="start"): return T(B, x, y, s, max(sz, 8), c, h, w, a)
def box(x, y, w, h, f=WH, s=LN): return R(x, y, w, h, f, s, 0)
def ln(x, y, w): return R(x, y, w, 3, "#52525240")
def thumb(x, y, w, h, i, kind="scene"):
    c = ACC[i % 4]
    if kind == "tile": return R(x, y, w, h, c) + tx(x + w / 2, y + h / 2 + 4, ["R", "P", "S", "D", "C", "H"][i % 6], max(10, h * .4), WH, True, a="middle")
    if kind == "icon":
        k = ["M4 12 L12 4 L20 12 M7 10 V20 H17 V10", "M12 3 L14.5 9 L21 9.5 L16 14 L17.5 20.5 L12 17 L6.5 20.5 L8 14 L3 9.5 L9.5 9 Z", "M4 7 H20 M4 12 H20 M4 17 H14", "M12 4 A8 8 0 1 0 12.01 4 M12 8 V12 L15 14"][i % 4]; s = min(w, h) * .55
        return R(x, y, w, h, BG, BB) + f'<g transform="translate({x+w/2-s/2},{y+h/2-s/2}) scale({s/24})"><path d="{k}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></g>'
    if kind == "photo":
        return R(x, y, w, h, "#8A8580") + f'<path d="M{x} {y+h} L{x+w*.35} {y+h*.45} L{x+w*.6} {y+h*.75} L{x+w*.8} {y+h*.55} L{x+w} {y+h*.8} V{y+h} Z" fill="#3F3B37"/>' + D(x + w * .78, y + h * .28, min(w, h) * .1, "#E8E2D6")
    return R(x, y, w, h, BG, BB) + f'<path d="M{x} {y+h} L{x+w*.35} {y+h*.5} L{x+w*.6} {y+h*.78} L{x+w*.8} {y+h*.6} L{x+w} {y+h*.85} V{y+h} Z" fill="{c}" opacity=".85"/>' + D(x + w * .78, y + h * .3, min(w, h) * .1, c)
def share(x, y): return f'<g transform="translate({x},{y}) scale(.5)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{INK}" stroke-width="2.2"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{INK}" stroke-width="2.2"/></g>'
def frame(board, body, decks=True):
    s = R(0, 0, W, 32, BG) + L(0, 32, W, 32, BB) + tx(12, 19, "Apps Home", 8, MUTE, w=600) + tx(120, 21, board + " Command Center", 11, INK, True, a="middle") + share(212, 9)
    if decks: s += tx(14, 46, "Ready To Swipe", 9, INK, True) + "".join(box(14 + i * 72, 51, 66, 16) + R(14 + i * 72, 51, 66, 2, ACC[i]) + tx(20 + i * 72, 62, ["Layout", "Colour", "Words"][i], 8, INK, w=600) for i in range(3))
    return phone(B, s + body + tx(120, 293, "Built by Max Weberman", 8, "#8A8580", a="middle"))
def sec(y, s, extra=""): return tx(14, y, s, 11, INK, True) + extra
def arrows(y, x1=14, x2=226): return "".join(box(x - 7, y - 7, 14, 14) + tx(x, y + 3, t, 9, INK, w=600, a="middle") for x, t in ((x1 + 7, "<"), (x2 - 7, ">")))
def dots(y, n=5, k=0): return "".join(D(120 - (n - 1) * 4 + j * 8, y, 2.5, INK if j == k else BB) for j in range(n))
TOP = ["Coder's Dictionary", "UpKeep Pricing Forecast", "Founder And App Security", "Agent Dashboard Product", "Smart Upkeep Deep Dive"]
TSUB = ["60 words, 6 categories", "Plus plan, about $228/mo", "12 steps by impact", "What's in it, pricing", "10 new service ideas"]
SHORT = ["Dashboard Setup", "Add-Ons", "QR Stickers", "Daily Ideas", "Checkout", "Offline Info"]
PRJ = ["Sell Your Agent Dashboard", "Membership Add-Ons", "Home Guide QR Stickers", "Daily Ideas App", "Checkout And Selling", "Offline Shutoffs"]
def wrap(s, n):
    out, cur = [], ""
    for w_ in s.split():
        if len(cur) + len(w_) + 1 > n and cur: out.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    return out + [cur]
def tcard(x, y, w, i, title, sub=None, ratio=9/16, cap="under", num=None, kind="scene", lines=2):
    th = w * ratio; s = box(x, y, w, th + (0 if cap == "over" else 14 + 10 * min(lines, len(wrap(title, int(w / 4.6)))) + (10 if sub else 0)))
    s += thumb(x, y, w, th, i, kind)
    if cap == "over":
        s += R(x, y + th - 18, w, 18, "#0A0A0ACC") + tx(x + 5, y + th - 6, wrap(title, int(w / 4.6))[0], 8.5, WH, True)
        if num: s += R(x, y, 18, 12, WH) + tx(x + 9, y + 9, num, 8, INK, True, a="middle")
        return s
    if num: s += R(x, y, 18, 12, WH) + tx(x + 9, y + 9, num, 8, INK, True, a="middle")
    yy = y + th + 11
    for l_ in wrap(title, int(w / 4.6))[:lines]: s += tx(x + 5, yy, l_, 8.5, INK, True); yy += 10
    if sub: s += tx(x + 5, yy, sub, 8, MUTE)
    return s
def rest(y, label="Routines"): return sec(y, label) + box(14, y + 6, 212, 18) + ln(22, y + 14, 120)
def RS(body, rout=262): return frame("Research", box(14, 74, 212, 14, BG, BB) + tx(20, 84, "Morning Report", 8.5, INK, True) + tx(220, 84, "+", 9, INK, a="end") + body + (rest(rout) if rout else ""))
def topics_car(y, w=96, n=3, x0=14, arr=False, dt=True, num=True, ratio=9/16, cap="under", kind="scene"):
    s = sec(y, "Research Topic Center")
    for i in range(n): s += tcard(x0 + i * (w + 8), y + 6, w, i, TOP[i], TSUB[i] if w > 80 else None, ratio, cap, f"0{i+1}" if num else None, kind)
    hh = w * ratio + 44
    if arr: s += arrows(y + 6 + w * ratio / 2)
    if dt: s += dots(y + hh + 12)
    return s
def proj_grid(y, cols=2, n=6, ratio=9/16, cap="under", kind="scene"):
    s = sec(y, "Potential Project Center"); w = (212 - 8 * (cols - 1)) / cols
    for i in range(n): s += tcard(14 + (i % cols) * (w + 8), y + 6 + (i // cols) * (w * ratio + 34), w, i + 1, (SHORT if cols > 2 else PRJ)[i], None, ratio, cap, None, kind, lines=1 if cols > 2 else 2)
    return s
def tbar(y): return box(14, y, 212, 14, BG, BB) + tx(20, y + 10, "Research Topic Center  |  5 topics", 8.5, INK, True) + tx(220, y + 10, "+", 9, INK, a="end")
def proj_car(y, w=96, n=3):
    s = sec(y, "Potential Project Center")
    for i in range(n): s += tcard(14 + i * (w + 8), y + 6, w, i + 1, PRJ[i], None)
    return s + dots(y + w * 9 / 16 + 44, 6)

# ---------------- Research (current: topic carousel 01-05 + project grid of 6 thumbnails)
P("Research Projects", "Potential Project Center: Keep The Grid Of 6 Thumbnail Cards, Or Turn It Into A Swipe Carousel Like Research Topics?",
  ("rp_grid", "Thumbnail Grid", "All 6 projects visible at once, 2 across.", "overview", RS(tbar(94) + proj_grid(124, n=6, cols=3), rout=270)),
  ("rp_car", "Thumbnail Carousel", "Swipe through projects, one row.", "swipeable", RS(tbar(94) + proj_car(124, w=110, n=2), rout=262)))
P("Research Projects", "Project Cards: Big Image Cards, One Per Row, Or Small Thumbnail Rows With The Title Beside?",
  ("rp_big", "Big Image Cards", "A wide 16:9 picture on each project.", "visual", RS(sec(102, "Potential Project Center") + tcard(14, 108, 212, 1, PRJ[0], "Packaged setup for small teams") , rout=0)),
  ("rp_rows", "Small Thumbnail Rows", "Many projects fit on one screen.", "compact",
   RS(sec(102, "Potential Project Center") + "".join(box(14, 108 + i * 30, 212, 26) + thumb(16, 110 + i * 30, 39, 22, i + 1) + tx(62, 120 + i * 30, PRJ[i], 9, INK, True) + tx(62, 130 + i * 30, "Open", 8, LAGOON, w=600) for i in range(5)), rout=262)))
P("Research Topics", "Research Topic Carousel Card Width: One Big Card With The Next Peeking In, Or Three Small Cards Across?",
  ("rt_peek", "One Card, Next Peeks In", "Big picture, clear read; swipe for more.", "focused", RS(topics_car(102, w=176, n=2), rout=0)),
  ("rt_three", "Three Across", "See three topics at a glance.", "glanceable", RS(topics_car(102, w=65, n=3), rout=240)))
P("Research Topics", "Moving Through The Topic Carousel: Left And Right Arrows, Or Swipe Only?",
  ("rt_arr", "Arrows", "Tap arrows; works on laptop too.", "explicit", RS(topics_car(102, w=88, n=2, x0=32, arr=True), rout=240)),
  ("rt_swipe", "Swipe Only", "Cleaner; cards go edge to edge.", "clean", RS(topics_car(102, w=96, n=3), rout=240)))
P("Research Topics", "Under The Topic Carousel: Show Position Dots, Or No Dots?",
  ("rt_dots", "With Dots", "Shows 5 topics and where you are.", "oriented", RS(topics_car(102), rout=240)),
  ("rt_nodots", "No Dots", "The peeking card is hint enough.", "minimal", RS(topics_car(102, dt=False), rout=240)))
P("Research Topics", "Topic Card Number: Small 01-05 Tag On The Thumbnail Corner, Or Big Number Above The Title?",
  ("rn_tag", "Tag On The Thumbnail", "Number sits on the picture.", "tidy", RS(topics_car(102, w=110, n=2), rout=248)),
  ("rn_big", "Big Number Above Title", "Number leads like a chapter.", "editorial",
   RS(sec(102, "Research Topic Center") + "".join(box(14 + i * 118, 108, 110, 100) + thumb(14 + i * 118, 108, 110, 50, i) + tx(19 + i * 118, 176, f"0{i+1}", 18, ACC[i], True) + tx(19 + i * 118, 190, TOP[i], 8.5, INK, True) + tx(19 + i * 118, 201, TSUB[i], 8, MUTE) for i in range(2)) + dots(220), rout=240)))

# ---------------- Coach (suggestions + coaching notes)
CS = [("One Publishing Rule", "Boards ship when the kit says, not before."), ("Stop Repeating Rules", "No echo posts in the team feed."), ("Clear Lanes For Ideas", "One owner per suggestion type.")]
NOTES = ["Evening Report Thrash", "Swipe Counts Flipped", "Kit Rule Timing"]
def CF(body): return frame("Coach", body + rest(262))
P("Coach Suggestions", "Coach Suggestions: A Swipe Carousel Of Cards With A Thumbnail, Or A Stacked List?",
  ("cs_car", "Thumbnail Carousel", "One suggestion per card, swipe for the next.", "swipeable",
   CF(sec(84, "Suggestions") + "".join(box(14 + i * 158, 90, 150, 150) + thumb(14 + i * 158, 90, 150, 84, i) + tx(20 + i * 158, 188, CS[i][0], 10, INK, True) + "".join(tx(20 + i * 158, 201 + k * 10, l_, 8, MUTE) for k, l_ in enumerate(wrap(CS[i][1], 30)[:2])) + tx(20 + i * 158, 232, "Approve", 8.5, JUNGLE, w=600) for i in range(2)) + dots(250, 3))),
  ("cs_list", "Stacked List", "All suggestions visible, read top down.", "scannable",
   CF(sec(84, "Suggestions") + "".join(box(14, 90 + i * 52, 212, 46) + R(14, 90 + i * 52, 3, 46, ACC[i]) + tx(24, 106 + i * 52, CS[i][0], 10, INK, True) + tx(24, 118 + i * 52, CS[i][1], 8, MUTE) + tx(24, 130 + i * 52, "Approve", 8.5, JUNGLE, w=600) for i in range(3)))))
def cthumbs(kind):
    return CF(sec(84, "Suggestions") + "".join(box(14, 90 + i * 52, 212, 46) + thumb(18, 94 + i * 52, 38, 38, i, kind) + tx(64, 108 + i * 52, CS[i][0], 10, INK, True) + tx(64, 121 + i * 52, CS[i][1][:34], 8, MUTE) for i in range(3)))
P("Coach Suggestions", "Thumbnail On Each Coach Suggestion: A Drawn Line Icon, Or A Photo?",
  ("ct_icon", "Drawn Icon", "Simple line drawing on beige.", "clean", cthumbs("icon")),
  ("ct_photo", "Photo", "A small picture per idea.", "warm", cthumbs("photo")))
P("Coach Suggestions", "Or Keep It Simplest: A Drawn Icon, Or A Solid Colour Tile With A Letter?",
  ("ct_icon2", "Drawn Icon", "Line drawing says what the idea is about.", "descriptive", cthumbs("icon")),
  ("ct_tile", "Colour Tile", "One bold block of colour per lane.", "bold", cthumbs("tile")))
P("Coach Notes", "Coaching Notes (01-03): Swipe Carousel Of Short Cards, Or Keep The Numbered List?",
  ("cn_car", "Short Card Carousel", "One note per card, swipe through.", "swipeable",
   CF(sec(84, "Coaching Notes") + "".join(box(14 + i * 118, 90, 110, 110) + thumb(14 + i * 118, 90, 110, 52, i, "icon") + tx(20 + i * 118, 158, NOTES[i], 9, INK, True) + ln(20 + i * 118, 168, 90) + ln(20 + i * 118, 176, 70) for i in range(2)) + dots(212, 3))),
  ("cn_list", "Numbered List", "All three read in one go.", "steady",
   CF(sec(84, "Coaching Notes") + "".join(box(14, 90 + i * 40, 212, 34) + tx(22, 111 + i * 40, f"0{i+1}", 12, ACC[i], True) + tx(44, 104 + i * 40, NOTES[i], 9.5, INK, True) + ln(44, 112 + i * 40, 150) for i in range(3)))))

# ---------------- Legal
DOCS = ["Privacy Policy", "Terms Of Service", "Trademark Search", "Cyber And E&O Quote"]
def LF(body): return frame("Legal", body + rest(262))
def doc(x, y, w, h, i, t):
    return box(x, y, w, h) + R(x + 8, y + 6, w - 16, h - 30, BG, BB) + "".join(R(x + 14, y + 14 + k * 7, (w - 28) * (.9 - k * .15), 2.5, "#52525255") for k in range(4)) + R(x + 8, y + 6, w - 16, 3, ACC[i % 4]) + tx(x + 6, y + h - 10, t, 8.5, INK, True)
P("Legal Documents", "Legal Documents: A Carousel Of Page Thumbnails, Or A Plain List?",
  ("ld_car", "Page Thumbnail Carousel", "See each document's first page.", "visual",
   LF(sec(84, "Documents") + "".join(doc(14 + i * 74, 90, 68, 92, i, DOCS[i].split()[0]) for i in range(3)) + dots(194, 4) + sec(214, "Apps Under Review") + box(14, 220, 212, 18) + tx(22, 232, "Smart Upkeep App", 8.5, INK, True))),
  ("ld_list", "Plain List", "Name, status, open link.", "efficient",
   LF(sec(84, "Documents") + "".join(box(14, 90 + i * 26, 212, 22) + tx(22, 104 + i * 26, DOCS[i], 9, INK, True) + tx(218, 104 + i * 26, ["Draft", "Draft", "Waiting", "Quote"][i], 8, MUTE, a="end") for i in range(4)) + sec(214, "Apps Under Review") + box(14, 220, 212, 18) + tx(22, 232, "Smart Upkeep App", 8.5, INK, True))))
LQ = [("Urgent", "IG screenshot for WellNest attorney"), ("Approve", "Trademark search, $1,700-$3,000"), ("Approve", "Legal and tax budget, about $5,000"), ("Pick", "Cyber and E&O tier, $1M + $1M")]
P("Legal Questions", "Open Legal Questions: Swipe Cards, One Question Each, Or A Checklist You Tick Down?",
  ("lq_card", "Swipe Cards", "One question fills the card with Yes / No.", "focused",
   LF(sec(84, "Open Legal Matters") + box(14, 90, 186, 130) + R(14, 90, 186, 3, RED) + tx(22, 108, "1 of 5  |  Urgent", 8, RED, w=600) + "".join(tx(22, 126 + k * 12, l_, 10, INK, True) for k, l_ in enumerate(wrap("Send the IG screenshot of The Cocoon renaming to Wellnest?", 32))) + box(22, 192, 80, 18, INK, INK) + tx(62, 204, "Yes", 8.5, WH, w=600, a="middle") + box(110, 192, 80, 18) + tx(150, 204, "Ask More", 8.5, INK, w=600, a="middle") + box(206, 98, 30, 114, "#FAFAFA") + dots(234, 5))),
  ("lq_list", "Checklist", "All open questions in one list.", "complete",
   LF(sec(84, "Open Legal Matters") + "".join(box(14, 90 + i * 34, 212, 30) + box(20, 99 + i * 34, 12, 12) + tx(40, 102 + i * 34, LQ[i][0], 8, RED if i == 0 else MUTE, w=600) + tx(40, 113 + i * 34, LQ[i][1], 9, INK, True) for i in range(4)))))
P("Legal Questions", "Each Legal Question Card: Show The Cost And Deadline As Chips, Or Keep It To The Question Text?",
  ("lc_chips", "Cost And Deadline Chips", "Money and date pop out.", "decisive",
   LF(sec(84, "Open Legal Matters") + "".join(box(14, 90 + i * 46, 212, 40) + tx(22, 105 + i * 46, LQ[i + 1][1].split(",")[0], 9.5, INK, True) + box(22, 112 + i * 46, 66, 12, BG, BB) + tx(55, 121 + i * 46, ["$1.7k-$3k", "$5,000", "$1.5k-$3k/yr"][i], 8, INK, w=600, a="middle") + box(94, 112 + i * 46, 56, 12, BG, BB) + tx(122, 121 + i * 46, ["2 weeks", "This week", "Before sale"][i], 8, INK, w=600, a="middle") for i in range(3)))),
  ("lc_text", "Question Text Only", "Plain sentence, details on tap.", "calm",
   LF(sec(84, "Open Legal Matters") + "".join(box(14, 90 + i * 46, 212, 40) + "".join(tx(22, 105 + i * 46 + k * 11, l_, 9, INK, True if k == 0 else False) for k, l_ in enumerate(wrap(["Approve a trademark search plus attorney opinion?", "Approve a legal and tax budget of about $5,000?", "Pick the Standard cyber and E&O tier?"][i], 44)[:2])) for i in range(3)))))

# ---------------- Security
AREAS = [("Code And Repos", "Amber", AMB), ("Passwords And Logins", "Red", RED), ("Financial Accounts", "Amber", AMB), ("Customer Data", "Amber", AMB), ("Legal And IP", "Amber", AMB), ("Shared Computer", "Red", RED)]
def SF(body): return frame("Security", body + rest(262))
P("Security Areas", "Exposure Overview (6 Areas): A Carousel Of Status Thumbnails, Or A List With Red Amber Green Tags?",
  ("sa_car", "Status Thumbnail Carousel", "Big colour tile per area; swipe through.", "visual",
   SF(sec(84, "Exposure Overview") + "".join(box(14 + i * 74, 90, 68, 92) + R(14 + i * 74, 90, 68, 46, AREAS[j][2]) + tx(48 + i * 74, 118, AREAS[j][1], 11, WH, True, a="middle") + "".join(tx(19 + i * 74, 150 + k * 10, l_, 8.5, INK, True) for k, l_ in enumerate(wrap(AREAS[j][0], 13)[:2])) for i, j in enumerate([1, 5, 0])) + dots(194, 6))),
  ("sa_list", "List With Tags", "All six areas, one line each.", "scannable",
   SF(sec(84, "Exposure Overview") + "".join(box(14, 90 + i * 27, 212, 23) + tx(22, 105 + i * 27, AREAS[i][0], 9, INK, True) + box(184, 95 + i * 27, 36, 13, AREAS[i][2] + "1A", AREAS[i][2]) + tx(202, 105 + i * 27, AREAS[i][1], 8, AREAS[i][2], w=600, a="middle") for i in range(6)))))
P("Security Areas", "Status Thumbnail: A Solid Red Amber Green Tile, Or A White Card With A Drawn Shield Icon In The Status Colour?",
  ("st_tile", "Solid Colour Tile", "Status reads from across the room.", "loud",
   SF(sec(84, "Exposure Overview") + "".join(box(14 + (i % 2) * 110, 90 + (i // 2) * 52, 102, 46) + R(14 + (i % 2) * 110, 90 + (i // 2) * 52, 34, 46, AREAS[i][2]) + "".join(tx(54 + (i % 2) * 110, 106 + (i // 2) * 52 + k * 10, l_, 8.5, INK, True) for k, l_ in enumerate(wrap(AREAS[i][0], 11)[:2])) for i in range(6)))),
  ("st_shield", "Shield Icon", "Calmer; colour only on the icon.", "calm",
   SF(sec(84, "Exposure Overview") + "".join(box(14 + (i % 2) * 110, 90 + (i // 2) * 52, 102, 46) + f'<path transform="translate({20+(i%2)*110},{98+(i//2)*52})" d="M12 2 L22 6 V14 C22 22 16 27 12 29 C8 27 2 22 2 14 V6 Z" fill="none" stroke="{AREAS[i][2]}" stroke-width="2.2"/>' + "".join(tx(54 + (i % 2) * 110, 106 + (i // 2) * 52 + k * 10, l_, 8.5, INK, True) for k, l_ in enumerate(wrap(AREAS[i][0], 11)[:2])) for i in range(6)))))
CHK = ["Change 6 passwords", "Turn on 2FA: bank", "Move tax files", "Lock shared computer"]
P("Security Checks", "Open Security Checks: Swipe Cards, One Fix At A Time, Or A Checklist?",
  ("sc_card", "Swipe Cards", "One fix per card with a Done button.", "focused",
   SF(sec(84, "Open Checks") + box(14, 90, 186, 120) + R(14, 90, 186, 3, RED) + thumb(22, 100, 170, 50, 0, "icon") + tx(22, 168, CHK[0], 11, INK, True) + tx(22, 181, "Red  |  Passwords And Logins", 8, RED, w=600) + box(22, 188, 70, 16, INK, INK) + tx(57, 199, "Done", 8.5, WH, w=600, a="middle") + box(206, 98, 30, 104, "#FAFAFA") + dots(222, 4))),
  ("sc_list", "Checklist", "Tick fixes off one by one.", "complete",
   SF(sec(84, "Open Checks") + "".join(box(14, 90 + i * 28, 212, 24) + box(21, 96 + i * 28, 12, 12) + tx(40, 106 + i * 28, CHK[i], 9, INK, True) + tx(218, 106 + i * 28, ["Red", "Amber", "Amber", "Red"][i], 8, [RED, AMB, AMB, RED][i], w=600, a="end") for i in range(4)))))
P("Security Alerts", "Security Alerts (Like A Leaked Key): A Banner Carousel At The Top, Or One Line In The Morning Report?",
  ("sl_ban", "Banner Carousel", "Each alert is its own red card to swipe.", "urgent",
   SF(box(14, 78, 212, 46, "#FEF3F2", RED) + tx(22, 94, "Alert  |  1 of 2", 8, RED, w=600) + tx(22, 108, "Secret found in a public repo", 10, INK, True) + tx(22, 119, "Rotate the token today", 8, MUTE) + dots(132, 2) + sec(152, "Exposure Overview") + "".join(box(14, 158 + i * 26, 212, 22) + tx(22, 173 + i * 26, AREAS[i][0], 9, INK, True) for i in range(3)))),
  ("sl_line", "Line In Morning Report", "Alerts live inside the report.", "quiet",
   SF(box(14, 78, 212, 50, BG, BB) + tx(22, 92, "Morning Report", 9, INK, True) + D(25, 105, 3, RED) + tx(32, 108, "Secret found in a public repo", 8.5, INK) + D(25, 119, 3, AMB) + tx(32, 122, "2FA still unknown on 4 accounts", 8.5, INK) + sec(152, "Exposure Overview") + "".join(box(14, 158 + i * 26, 212, 22) + tx(22, 173 + i * 26, AREAS[i][0], 9, INK, True) for i in range(3)))))

# ---------------- Shared
P("Thumbnails", "Thumbnail Shape On All Four Boards: Wide 16:9, Or Square?",
  ("sh_wide", "Wide 16:9", "Like a video still; titles get more room.", "cinematic", RS(topics_car(102, w=110, n=2), rout=248)),
  ("sh_sq", "Square", "Taller picture, more like an app tile.", "tile", RS(topics_car(102, w=80, n=3, ratio=1), rout=0)))
P("Thumbnails", "Card Title: Caption Under The Thumbnail, Or Overlaid On A Dark Strip At The Bottom Of The Picture?",
  ("sh_under", "Caption Under", "Text on white, easiest to read.", "readable", RS(tbar(94) + proj_grid(124, n=6, cols=3, cap="under"), rout=270)),
  ("sh_over", "Overlaid", "Picture fills the card; shorter cards.", "immersive", RS(tbar(94) + proj_grid(124, n=6, cols=3, cap="over"), rout=262)))
P("Thumbnails", "Tapping A Thumbnail Card: It Expands In Place With The Details, Or Opens Its Own Page?",
  ("sh_exp", "Expand In Place", "Stay on the board; tap again to close.", "quick",
   RS(sec(102, "Potential Project Center") + tcard(14, 108, 212, 1, PRJ[1], None) + "".join(tx(20, 260 + k * 0, "", 8) for k in range(1)) + box(14, 229, 212, 30) + tx(20, 241, "About $61 per member per month", 8.5, INK) + tx(20, 253, "Close", 8.5, LAGOON, w=600), rout=0)),
  ("sh_page", "Open Page", "Full write-up on its own page, Back to return.", "thorough",
   frame("Research", tx(14, 50, "< Back to Research", 8.5, LAGOON, w=600) + tx(14, 70, "Membership Add-Ons", 14, INK, True) + thumb(14, 78, 212, 119, 1) + "".join(ln(14, 210 + k * 10, 200 - k * 20) for k in range(5)), decks=False)))
assert len(pairs) == 20, len(pairs)
json.dump({"pairs": pairs}, open(sys.argv[1] if len(sys.argv) > 1 else "/workspace/scratch/advisor_pairs.json", "w"), ensure_ascii=False)
print("pairs", len(pairs))
