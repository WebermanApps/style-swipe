#!/usr/bin/env python3
"""Advisor Boards follow-up pairs (Oct 15 2026, after Max's 13:52 ICT Advisor Boards Deck submit). 18 fresh pairs that refine his picks
(16:9 thumbs, caption under, expand in place, swipe cards, carousels) for Research, Coach, Legal, Security. The two skips
(legal cost chips, coach thumbnail kind) come back reworded via carry_over (R64), so 18 + 2 = 20. Same look: white + beige,
square corners, Khand/Hind, numbers only on research topic cards. Writes pairs JSON for ready_shelf.py refill/build --source."""
import sys, os, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_advisor_boards.py")).read()
exec(src.split("# ---------------- Research")[0].replace('deck("ab_", "Branding")', 'deck("ab2_", "Branding")'))
exec("#" + src.split("# ---------------- Coach")[1].split("P(\"Coach Suggestions\"")[0])           # CS, NOTES, CF
exec("DOCS" + src.split("DOCS", 1)[1].split("P(\"Legal Documents\"")[0])                 # DOCS, LF, doc
exec("LQ" + src.split("LQ", 1)[1].split("P(\"Legal Questions\"")[0])
exec("AREAS" + src.split("AREAS", 1)[1].split("P(\"Security Areas\"")[0])                # AREAS, SF
exec("CHK" + src.split("CHK", 1)[1].split("P(\"Security Checks\"")[0])
def shield(x, y, c): return f'<path transform="translate({x},{y})" d="M12 2 L22 6 V14 C22 22 16 27 12 29 C8 27 2 22 2 14 V6 Z" fill="none" stroke="{c}" stroke-width="2.2"/>'
def pline(y, frac=.3): return R(14, y, 212, 3, BB) + R(14, y, 212 * frac, 3, INK)
def three(y, sub=True, numc=None, peek=False):
    s = sec(y, "Research Topic Center"); w = 65
    for i in range(3 if not peek else 4):
        x = 14 + i * (w + 8) - (20 if peek else 0)
        s += box(x, y + 6, w, w * 9 / 16 + (44 if sub else 32)) + thumb(x, y + 6, w, w * 9 / 16, i)
        s += tx(x + 4, y + 6 + w * 9 / 16 + 14, f"0{i+1}", 12, (ACC[i % 4] if numc == "acc" else INK), True)
        for k, l_ in enumerate(wrap(TOP[i % 5], 13)[:2]): s += tx(x + 4, y + 6 + w * 9 / 16 + 25 + k * 9, l_, 8, INK, True)
        if sub: s += tx(x + 4, y + 6 + w * 9 / 16 + 44, TSUB[i % 5][:14], 8, MUTE)
    return s
# ---- Research
P("Research Projects", "Potential Project Center: A Swipe Carousel Of Thumbnail Cards, Or Small Thumbnail Rows In A List?",
  ("rp2_car", "Thumbnail Carousel", "Swipe sideways, like the topics.", "swipeable", RS(tbar(94) + proj_car(124, w=110, n=2), rout=262)),
  ("rp2_rows", "Small Thumbnail Rows", "All six down the page, no swiping.", "scannable",
   RS(sec(102, "Potential Project Center") + "".join(box(14, 108 + i * 26, 212, 22) + thumb(16, 110 + i * 26, 32, 18, i + 1) + tx(54, 122 + i * 26, PRJ[i], 9, INK, True) for i in range(6)), rout=270)))
P("Research Topics", "Three Topic Cards Across: Title With A Short Line Under It, Or Title Only?",
  ("rt2_sub", "Title Plus Line", "Says what's inside each topic.", "descriptive", RS(three(102, True) + dots(212), rout=240)),
  ("rt2_title", "Title Only", "Shorter cards, cleaner row.", "clean", RS(three(102, False) + dots(200), rout=240)))
P("Research Topics", "Big Topic Number Colour: Black Like The Text, Or Each Topic In Its Own Accent Colour?",
  ("rt2_numink", "Black Number", "Calm; matches the titles.", "calm", RS(three(102, True) + dots(212), rout=240)),
  ("rt2_numacc", "Accent Colour", "Each topic easy to spot.", "warm", RS(three(102, True, "acc") + dots(212), rout=240)))
P("Research Topics", "Three Across On A Phone: Exactly Three Cards Fit, Or A Slice Of The Fourth Peeks In?",
  ("rt2_fit", "Exactly Three", "Neat row, dots say there is more.", "tidy", RS(three(102, True) + dots(212), rout=240)),
  ("rt2_peek4", "Fourth Peeks In", "Edge shows you can swipe.", "swipeable", RS(three(102, True, peek=True) + dots(212), rout=240)))
P("Research Topics", "Carousel Position: Small Dots, Or A Thin Line That Fills As You Swipe?",
  ("rt2_dots", "Small Dots", "One dot per topic.", "oriented", RS(three(102) + dots(212), rout=240)),
  ("rt2_line", "Thin Filling Line", "One quiet bar under the row.", "minimal", RS(three(102) + pline(210), rout=240)))
# ---- Coach
def ccar(icon=True, btn2=False, inkicon=False):
    s = sec(84, "Suggestions")
    for i in range(2):
        x = 14 + i * 158; s += box(x, 90, 150, 150)
        if icon:
            s += (thumb(x, 90, 150, 84, i, "icon") if not inkicon else R(x, 90, 150, 84, BG, BB) + f'<g transform="translate({x+56},{110}) scale(1.6)"><path d="M4 12 L12 4 L20 12 M7 10 V20 H17 V10" fill="none" stroke="{INK}" stroke-width="2"/></g>')
        yy = 188 if icon else 110
        s += tx(x + 6, yy, CS[i][0], 10, INK, True) + "".join(tx(x + 6, yy + 13 + k * 10, l_, 8, MUTE) for k, l_ in enumerate(wrap(CS[i][1], 30)[:2]))
        s += box(x + 6, 220, 60, 14, INK, INK) + tx(x + 36, 230, "Approve", 8, WH, w=600, a="middle")
        if btn2: s += box(x + 72, 220, 60, 14) + tx(x + 102, 230, "Not Now", 8, INK, w=600, a="middle")
    return CF(s + dots(250, 3))
P("Coach Suggestions", "Coach Suggestion Card Buttons: Approve Only, Or Approve Plus Not Now?",
  ("cs2_one", "Approve Only", "One clear action; swipe past to skip.", "decisive", ccar()),
  ("cs2_two", "Approve And Not Now", "Say no without leaving it hanging.", "complete", ccar(btn2=True)))
P("Coach Suggestions", "Drawn Icon Colour: Each Lane Has Its Own Accent, Or All Icons In Black Ink?",
  ("cs2_iconacc", "Lane Accent", "Colour hints which lane it's for.", "warm", ccar()),
  ("cs2_iconink", "Black Ink", "Quieter; the words do the work.", "quiet", ccar(inkicon=True)))
P("Coach Notes", "Coaching Note Cards In The Carousel: Drawn Icon On Top, Or Text Only?",
  ("cn2_icon", "Icon On Top", "Same look as suggestions.", "visual",
   CF(sec(84, "Coaching Notes") + "".join(box(14 + i * 118, 90, 110, 110) + thumb(14 + i * 118, 90, 110, 52, i, "icon") + tx(20 + i * 118, 158, NOTES[i], 9, INK, True) + ln(20 + i * 118, 168, 90) + ln(20 + i * 118, 176, 70) for i in range(2)) + dots(212, 3))),
  ("cn2_text", "Text Only", "Shorter cards, more words.", "compact",
   CF(sec(84, "Coaching Notes") + "".join(box(14 + i * 118, 90, 110, 80) + tx(20 + i * 118, 106, NOTES[i], 9.5, INK, True) + "".join(ln(20 + i * 118, 116 + k * 9, 90 - k * 10) for k in range(5)) for i in range(2)) + dots(182, 3))))
# ---- Legal
def lcard(btns, top=True):
    s = box(14, 90, 186, 120) + R(14, 90, 186, 3, RED) + tx(22, 108, "Urgent", 8, RED, w=600)
    s += "".join(tx(22, 126 + k * 12, l_, 10, INK, True) for k, l_ in enumerate(wrap("Send the IG screenshot of The Cocoon renaming to Wellnest?", 32)))
    for j, b in enumerate(btns): s += box(22 + j * 58, 186, 52, 16, INK if j == 0 else WH, INK) + tx(48 + j * 58, 197, b, 8, WH if j == 0 else INK, w=600, a="middle")
    return s + box(206, 98, 30, 104, "#FAFAFA")
P("Legal Questions", "Legal Question Card Buttons: Yes And Ask More, Or Yes, No And Later?",
  ("lq2_two", "Yes And Ask More", "Two buttons; questions go to Legal.", "focused", LF(sec(84, "Open Legal Matters") + lcard(["Yes", "Ask More"]) + dots(226, 5))),
  ("lq2_three", "Yes, No, Later", "Every answer has a button.", "complete", LF(sec(84, "Open Legal Matters") + lcard(["Yes", "No", "Later"]) + dots(226, 5))))
P("Legal Questions", "Legal Board Order: Question Cards First, Documents Under Them, Or Documents First?",
  ("lo2_q", "Questions First", "What needs you leads the board.", "urgent",
   LF(sec(84, "Open Legal Matters") + box(14, 90, 212, 60) + R(14, 90, 212, 3, RED) + tx(22, 108, "Send the IG screenshot?", 10, INK, True) + sec(170, "Documents") + "".join(box(14, 176 + i * 22, 212, 18) + tx(22, 188 + i * 22, DOCS[i], 8.5, INK, True) for i in range(3)))),
  ("lo2_d", "Documents First", "Reference on top, questions below.", "steady",
   LF(sec(84, "Documents") + "".join(box(14, 90 + i * 22, 212, 18) + tx(22, 102 + i * 22, DOCS[i], 8.5, INK, True) for i in range(3)) + sec(170, "Open Legal Matters") + box(14, 176, 212, 60) + R(14, 176, 212, 3, RED) + tx(22, 194, "Send the IG screenshot?", 10, INK, True))))
P("Legal Documents", "Document List Status: A Word Tag On The Right, Or A Small Coloured Dot Before The Name?",
  ("ld2_tag", "Word Tag", "Draft, Waiting, Quote spelled out.", "explicit",
   LF(sec(84, "Documents") + "".join(box(14, 90 + i * 26, 212, 22) + tx(22, 104 + i * 26, DOCS[i], 9, INK, True) + box(176, 95 + i * 26, 44, 12, BG, BB) + tx(198, 104 + i * 26, ["Draft", "Draft", "Waiting", "Quote"][i], 8, INK, w=600, a="middle") for i in range(4)))),
  ("ld2_dot", "Coloured Dot", "Quieter; colour shows the state.", "quiet",
   LF(sec(84, "Documents") + "".join(box(14, 90 + i * 26, 212, 22) + D(24, 101 + i * 26, 3, [AMB, AMB, LAGOON, JUNGLE][i]) + tx(32, 104 + i * 26, DOCS[i], 9, INK, True) for i in range(4)))))
# ---- Security
def shields(word=True, order=(0, 1, 2, 3, 4, 5)):
    s = sec(84, "Exposure Overview")
    for n, i in enumerate(order):
        x, y = 14 + (n % 2) * 110, 90 + (n // 2) * 52
        s += box(x, y, 102, 46) + shield(x + 6, y + 8, AREAS[i][2]) + "".join(tx(x + 40, y + 16 + k * 10, l_, 8.5, INK, True) for k, l_ in enumerate(wrap(AREAS[i][0], 11)[:2]))
        if word: s += tx(x + 40, y + 40, AREAS[i][1], 8, AREAS[i][2], w=600)
    return SF(s)
P("Security Areas", "Shield Cards: Status Word Under The Name, Or Just The Coloured Shield?",
  ("sa2_word", "Status Word", "Red or Amber written out too.", "explicit", shields(True)),
  ("sa2_icon", "Shield Only", "Colour says it; less text.", "minimal", shields(False)))
P("Security Areas", "Exposure Cards Order: Worst First, Or Always The Same Order?",
  ("sa2_worst", "Worst First", "Red areas jump to the front.", "urgent", shields(True, (1, 5, 0, 2, 3, 4))),
  ("sa2_fixed", "Same Order", "Each area keeps its spot.", "steady", shields(True)))
def scard(swipe=False):
    s = sec(84, "Open Checks") + box(14, 90, 186, 120) + R(14, 90, 186, 3, RED) + thumb(22, 100, 170, 50, 0, "icon") + tx(22, 168, CHK[0], 11, INK, True) + tx(22, 181, "Red  |  Passwords And Logins", 8, RED, w=600)
    s += (tx(22, 200, "Swipe right when done  >", 8.5, LAGOON, w=600) if swipe else box(22, 188, 70, 16, INK, INK) + tx(57, 199, "Done", 8.5, WH, w=600, a="middle"))
    return SF(s + box(206, 98, 30, 104, "#FAFAFA") + dots(222, 4))
P("Security Checks", "Marking A Security Fix Done: Tap A Done Button, Or Swipe The Card Right?",
  ("sc2_btn", "Done Button", "Clear, hard to do by accident.", "explicit", scard()),
  ("sc2_swipe", "Swipe Right", "Fast; same gesture as decks.", "quick", scard(True)))
def alert(style):
    if style == "fill": a = box(14, 78, 212, 46, "#FEF3F2", RED)
    else: a = box(14, 78, 212, 46) + R(14, 78, 212, 3, RED)
    return SF(a + tx(22, 94, "Alert", 8, RED, w=600) + tx(22, 108, "Secret found in a public repo", 10, INK, True) + tx(22, 119, "Rotate the token today", 8, MUTE) + dots(132, 2) + sec(152, "Exposure Overview") + "".join(box(14, 158 + i * 26, 212, 22) + tx(22, 173 + i * 26, AREAS[i][0], 9, INK, True) for i in range(3)))
P("Security Alerts", "Alert Banner Look: Light Red Card With A Red Outline, Or White Card With A Red Top Bar?",
  ("sl2_fill", "Light Red Card", "Can't miss it.", "loud", alert("fill")),
  ("sl2_bar", "White With Red Bar", "Matches the other cards.", "calm", alert("bar")))
# ---- Shared
def expd(close):
    s = sec(102, "Potential Project Center") + tcard(14, 108, 212, 1, PRJ[1], None) + box(14, 229, 212, 30, BG, BB) + tx(20, 241, "About $61 per member per month", 8.5, INK)
    s += tx(20, 253, "Close", 8.5, LAGOON, w=600) if close else tx(20, 253, "Tap the card to close", 8, MUTE)
    return RS(s, rout=0)
P("Thumbnails", "Expanded Card: Show A Close Link, Or Just Tap The Card Again To Close?",
  ("sh2_close", "Close Link", "Obvious way back.", "explicit", expd(True)),
  ("sh2_tap", "Tap Again", "No extra words on the card.", "minimal", expd(False)))
def ccap(sub):
    return RS(sec(102, "Potential Project Center") + "".join(tcard(14 + i * 110, 108, 102, i + 1, PRJ[i], "Ready to sell" if sub else None) for i in range(2)) + dots(190, 6), rout=240)
P("Thumbnails", "Caption Under Each Thumbnail: Title Only, Or Title Plus A Short Grey Line?",
  ("sh2_t", "Title Only", "Shortest cards.", "clean", ccap(False)),
  ("sh2_ts", "Title Plus Line", "A hint of what's inside.", "descriptive", ccap(True)))
def exp2(push):
    s = sec(102, "Potential Project Center") + tcard(14, 108, 212, 1, PRJ[1], None) + box(14, 229, 212, 22, BG, BB) + tx(20, 243, "About $61 per member per month", 8.5, INK)
    s += (box(14, 256, 212, 18) + tx(20, 268, PRJ[2], 8.5, INK, True)) if push else (box(14, 256, 212, 18) + tx(20, 268, "Expanded cards close others", 8, MUTE))
    return RS(s, rout=0)
P("Thumbnails", "Opening One Card: Others Stay Open Too, Or Opening One Closes The Rest?",
  ("sh2_many", "Many Open", "Compare two at once.", "thorough", exp2(True)),
  ("sh2_one", "One At A Time", "Board stays short and tidy.", "tidy", exp2(False)))
assert len(pairs) == 18, len(pairs)
json.dump({"pairs": pairs}, open(sys.argv[1] if len(sys.argv) > 1 else "/workspace/style-swipe/banks/advisor-boards-two-pairs.json", "w"), ensure_ascii=False)
print("pairs", len(pairs))
