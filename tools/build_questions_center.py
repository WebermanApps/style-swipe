#!/usr/bin/env python3
"""Build Style Swipe deck questions-center: Questions Center Deck (Oct 14 2026). 20 pairs on how the Questions Center should look and work
(Grok Bot Command Center, just below the Evening Report dropdown; same format reused for Legal, Research, Coach).
Sample content: /workspace/ops/grokbot/decisions-2026-10-14.md. Submit -> agent 'grok-bot'."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
from dash_kit import *
DID = "questions-center"
B = dict(name="Command Center", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("qc_", "Grok Bot")
M = B["mute"]; INK = B["ink"]
QS = [("Miles", "Undo the password gate on Mom's Amex apps?", "Urgent", "Today", TERRA),
      ("Portfolio", "Sal: file MFS or Single?", "Urgent", "Oct 15", TERRA),
      ("Construction", "Push redaction on the Walk-Through app?", "Urgent", "Today", TERRA),
      ("Grok Bot", "Security under AIR or straight to Grok Bot?", "Soon", "Oct 17", SAFFRON),
      ("Prop", "Mellow Wood rent: $3,500 or $3,600?", "Soon", "Oct 30", SAFFRON),
      ("UpKeep", "7 or 8 progress segments?", "Later", "", LAGOON)]
def fit(s, n):
    return s if len(s) <= n else s[:n - 1].rstrip() + "..."
SHARE = lambda x=210, y=12: f'<g transform="translate({x},{y}) scale(.6)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{INK}" stroke-width="2.2"/></g>'
FOOT = L(14, 284, 226, 284, B["line"]) + T(B, 120, 295, "Built by Machan", 7.5, M, a="middle")
def head(sub="Command Center"):
    s = T(B, 14, 26, "Questions For Max", 16, None, True) + T(B, 14, 38, sub, 7.5, M) + SHARE()
    s += R(14, 44, 212, 16, "#FFFFFF", B["line"], 6) + T(B, 22, 55, "Evening Report", 7.5, INK, w=600) + chev(216, 52, M)
    return s
def pill(x, y, txt, c, solid=False):
    w = len(txt) * 4.4 + 10
    return R(x, y, w, 12, c if solid else "#FFFFFF", c, 6) + T(B, x + w / 2, y + 8.6, txt, 7.5, "#FFFFFF" if solid else c, w=600, a="middle"), w
def btn(x, y, w, txt, solid=True, c=JUNGLE):
    return R(x, y, w, 15, c if solid else "#FFFFFF", c, 5) + T(B, x + w / 2, y + 10.5, txt, 7.5, "#FFFFFF" if solid else c, w=600, a="middle")
def qcard(y, q, h=44, badge="pill", due=True, ans="buttons", note=False, edge=False):
    ag, txt, urg, d, c = q
    s = card(B, 14, y, 212, h) + (R(14, y, 3, h, c, r=1.5) if edge else "")
    s += T(B, 22, y + 12, ag.upper(), 7.5, M, w=600)
    if badge == "pill": p, w = pill(170 if urg != "Urgent" else 164, y + 4, urg, c, urg == "Urgent"); s += p
    elif badge == "dot": s += D(216, y + 9, 3.5, c)
    if due and d: s += T(B, 216 if badge != "pill" else 150, y + 12, "Due " + d, 7.5, TERRA if urg == "Urgent" else M, a="end")
    s += T(B, 22, y + 24, fit(txt, 46), 8.5, INK, w=600)
    if ans == "buttons": s += btn(22, y + h - 18, 44, "Yes") + btn(70, y + h - 18, 44, "No", False)
    elif ans == "text": s += R(22, y + h - 18, 196, 14, B["soft"], B["line"], 4) + T(B, 27, y + h - 8, "Type your answer", 7.5, M)
    elif ans == "both": s += btn(22, y + h - 18, 40, "Yes") + btn(66, y + h - 18, 40, "No", False) + R(110, y + h - 18, 108, 15, B["soft"], B["line"], 4) + T(B, 115, y + h - 8, "Or type...", 7.5, M)
    if note: s += T(B, 218, y + h - 7, "+ Note", 7.5, LAGOON, w=600, a="end")
    return s
def stackq(y0, qs, h=44, gap=6, **k):
    s = ""
    for i, q in enumerate(qs):
        y = y0 + i * (h + gap)
        if y + h > 280: break
        s += qcard(y, q, h, **k)
    return s
def submitbar(y=262, n=6):
    return R(14, y, 212, 18, INK, r=5) + T(B, 120, y + 12.5, f"SUBMIT ANSWERS (2 OF {n})", 7.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1"')
def scr(body, bg="#FFFFFF"): return screen(head() + body + FOOT, bg)
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
def grouphdr(y, txt, c, n):
    return T(B, 14, y, txt.upper(), 7.5, c, w=600, ex='letter-spacing="1"') + T(B, 226, y, str(n), 7.5, M, a="end")

# 1 layout: cards vs list
def listview(qs):
    s = ""
    for i, q in enumerate(qs):
        y = 68 + i * 30; s += L(14, y + 28, 226, y + 28, B["line"]) + D(18, y + 12, 3, q[4]) + T(B, 26, y + 10, q[0].upper(), 7.5, M, w=600) + T(B, 26, y + 22, fit(q[1], 44), 8, INK) + chev(220, y + 14, M)
    return s
P("Layout", "Questions Center: A Card For Each Question Or A Compact List?",
  ("lay_cards", "A Card Each", "Each question is its own white card with answer buttons right on it.", "visual", scr(stackq(68, QS[:4]))),
  ("lay_list", "Compact List", "One line per question; tap a row to open and answer.", "quick", scr(listview(QS))))
# 2 layout: one-at-a-time vs all
def single():
    q = QS[0]; s = T(B, 14, 76, "Question 1 of 6", 7.5, M) + R(14, 80, 212, 3, B["soft"], r=1.5) + R(14, 80, 35, 3, JUNGLE, r=1.5)
    s += card(B, 14, 92, 212, 150) + T(B, 26, 110, q[0].upper(), 7.5, M, w=600) + pill(178, 101, "Urgent", TERRA, True)[0]
    s += T(B, 26, 132, "Undo the password gate on", 12, INK, True) + T(B, 26, 148, "Mom's 2 live Amex apps?", 12, INK, True) + T(B, 26, 166, "Due today. Pushed in 8422814, 64a81b4.", 7.5, M)
    s += btn(26, 196, 90, "Yes, Undo") + btn(124, 196, 90, "No, Keep", False) + T(B, 26, 228, "Skip for now", 7.5, LAGOON, w=600) + T(B, 214, 228, "+ Note", 7.5, LAGOON, w=600, a="end")
    return s
P("Layout", "Answering: One Question At A Time Or All On One Page?",
  ("one_at", "One At A Time", "Big single question, answer, the next one slides in.", "focused", scr(single())),
  ("all_page", "All On One Page", "Scroll and answer in any order.", "quick", scr(stackq(68, QS[:4]))))
# 3 grouping by agent vs urgency
def byagent():
    s = grouphdr(76, "Portfolio", INK, 2) + qcard(80, QS[1], 40) + grouphdr(134, "Construction", INK, 1) + qcard(138, QS[2], 40) + grouphdr(192, "Prop", INK, 1) + qcard(196, QS[4], 40)
    return s
def byurg():
    return grouphdr(76, "Urgent", TERRA, 3) + qcard(80, QS[0], 40, edge=True) + qcard(124, QS[1], 40, edge=True) + grouphdr(178, "Soon", SAFFRON, 2) + qcard(182, QS[3], 40, edge=True) + qcard(226, QS[4], 40, edge=True)
P("Grouping", "Group The Questions By Agent Or By Urgency?",
  ("grp_agent", "By Agent", "Each agent's questions together under its name.", "calm", scr(byagent())),
  ("grp_urg", "By Urgency", "Urgent first, then Soon, then Later, agent shown on each card.", "action", scr(byurg())))
# 4 grouping inside: collapsed groups vs open
def collapsed():
    s = ""
    for i, (n, c, k) in enumerate([("Urgent", TERRA, 3), ("Portfolio", INK, 9), ("Legal", INK, 21), ("UpKeep", INK, 8), ("Prop", INK, 7), ("security", INK, 6)]):
        y = 68 + i * 30; s += card(B, 14, y, 212, 24) + T(B, 24, y + 15, n, 9, c, True) + pill(180, y + 6, str(k), c if c != INK else LAGOON, c == TERRA)[0] + chev(216, y + 12, M)
    return s
P("Grouping", "Groups: Folded Shut With Counts Or Everything Open?",
  ("grp_fold", "Folded With Counts", "Tap a group to open it; only Urgent opens by itself.", "calm", scr(collapsed())),
  ("grp_open", "Everything Open", "All questions visible, long scroll.", "quick", scr(byagent())))
# 5 answer type buttons vs text
P("Answer Types", "Answer With Quick Buttons Or Typed Text?",
  ("ans_btn", "Quick Buttons", "Yes / No or the two choices as buttons.", "quick", scr(stackq(68, QS[:4], ans="buttons"))),
  ("ans_txt", "Typed Text", "A short text box under every question.", "focused", scr(stackq(68, QS[:4], ans="text"))))
# 6 both vs per question
P("Answer Types", "Buttons Plus A Text Box On Every Question, Or Only Where Needed?",
  ("ans_both", "Both On Every Question", "Buttons and an Or type box on every card.", "action", scr(stackq(68, QS[:4], ans="both"))),
  ("ans_need", "Only Where Needed", "Agent picks: buttons for choices, text box for open questions.", "calm",
   scr(qcard(68, QS[0]) + qcard(118, QS[1], ans="text") + qcard(168, QS[3]) + qcard(218, QS[4], ans="text"))))
# 7 choice labels: yes/no vs real options
def realopt(y, q, a, b):
    return card(B, 14, y, 212, 44) + T(B, 22, y + 12, q[0].upper(), 7.5, M, w=600) + T(B, 22, y + 24, fit(q[1], 46), 8.5, INK, w=600) + btn(22, y + 26, 94, a, False, LAGOON) + btn(122, y + 26, 94, b, False, LAGOON)
P("Answer Types", "Choice Buttons: Plain Yes / No Or The Real Options Spelled Out?",
  ("opt_yn", "Plain Yes / No", "Short and the same on every card.", "quick", scr(stackq(68, QS[1:5]))),
  ("opt_real", "Real Options", "Buttons say the actual choices, e.g. MFS / Single.", "focused",
   scr(realopt(68, QS[1], "MFS", "Single") + realopt(118, QS[4], "$3,500", "$3,600") + realopt(168, QS[3], "Under AIR", "To Grok Bot") + realopt(218, QS[5], "7 Segments", "8 Segments"))))
# 8 after answer: hide on submit vs hide right away
def answered(hide):
    s = qcard(68, QS[0], ans=None) + R(22, 98, 60, 13, "#E3F1EA", r=4) + T(B, 52, 107, "Answered Yes", 7.5, JUNGLE, w=600, a="middle")
    s += qcard(118, QS[1], ans=None) + R(22, 148, 70, 13, "#E3F1EA", r=4) + T(B, 57, 157, "Answered Single", 7.5, JUNGLE, w=600, a="middle")
    s += qcard(168, QS[2]) + qcard(218, QS[3]) + submitbar(266)
    return s
def gone():
    return T(B, 14, 76, "2 answers sent. 4 left.", 7.5, JUNGLE, w=600) + stackq(82, QS[2:6])
P("After Answering", "After You Answer: Stay Ticked Until Submit, Or Vanish Right Away?",
  ("aft_submit", "Ticked Until Submit", "Answered cards show your pick, then hide when you press Submit.", "calm", scr(answered(True))),
  ("aft_now", "Vanish Right Away", "Each answer sends and the card disappears at once.", "quick", scr(gone())))
# 9 submit bar sticky vs per-card send
def percard():
    s = ""
    for i, q in enumerate(QS[:4]):
        y = 68 + i * 50; s += qcard(y, q, ans="buttons") + btn(176, y + 26, 42, "Send", True, INK)
    return s
P("After Answering", "Sending: One Submit Bar For All, Or A Send Button On Each Card?",
  ("snd_bar", "One Submit Bar", "Answer several, press Submit once; works anytime, even half done.", "calm", scr(stackq(68, QS[:4]) + submitbar(266))),
  ("snd_card", "Send On Each Card", "Each card sends on its own.", "action", scr(percard())))
# 10 urgency badges
P("Urgency", "Urgency: Word Pill Or A Coloured Edge?",
  ("urg_pill", "Word Pill", "Urgent / Soon / Later pill top right.", "focused", scr(stackq(68, QS[:4], badge="pill"))),
  ("urg_edge", "Coloured Edge", "Terracotta, saffron or lagoon strip down the left side.", "calm", scr(stackq(68, QS[:4], badge=None, edge=True))))
# 11 urgent banner vs inline
def banner():
    return R(14, 68, 212, 40, "#FBEDE8", TERRA, 8) + T(B, 24, 84, "3 URGENT", 9, TERRA, True) + T(B, 24, 98, "Miles, Portfolio, Construction need you today", 7.5, INK) + stackq(116, QS[:3], badge=None, edge=True)
P("Urgency", "Urgent Questions: A Red Banner On Top Or Just Sorted First?",
  ("urg_ban", "Banner On Top", "A terracotta box counts urgent questions above the rest.", "action", scr(banner())),
  ("urg_sort", "Just Sorted First", "No banner; urgent cards are simply first.", "calm", scr(stackq(68, QS[:4], badge="pill"))))
# 12 due dates
P("Due Dates", "Due Dates: Shown On Every Card Or Only When Close?",
  ("due_all", "On Every Card", "Each card with a date shows Due date.", "focused", scr(stackq(68, QS[1:5]))),
  ("due_close", "Only When Close", "Only within 2 days, in terracotta.", "calm", scr(qcard(68, QS[1]) + qcard(118, QS[2]) + qcard(168, QS[3], due=False) + qcard(218, QS[4], due=False))))
# 13 due format
def duefmt(rel):
    s = ""
    for i, q in enumerate(QS[1:5]):
        y = 68 + i * 50; s += qcard(y, (q[0], q[1], q[2], "", q[4]), ans="buttons")
        lab = ["Due tomorrow", "Due today", "In 3 days", "In 16 days"][i] if rel else ["Due Oct 15", "Due Oct 14", "Due Oct 17", "Due Oct 30"][i]
        s += T(B, 218, y + 38, lab, 7.5, TERRA if i < 2 else M, w=600, a="end")
    return s
P("Due Dates", "Dates As Days Left Or As The Calendar Date?",
  ("due_rel", "Days Left", "Due today, tomorrow, in 3 days.", "quick", scr(duefmt(True))),
  ("due_abs", "Calendar Date", "Due Oct 15, Oct 30.", "focused", scr(duefmt(False))))
# 14 notes
def noteopen():
    return qcard(68, QS[1]) + R(22, 116, 196, 30, B["soft"], B["line"], 4) + T(B, 27, 128, "Note: check 2025 extension first", 7.5, INK) + qcard(154, QS[3]) + qcard(204, QS[4])
P("Notes", "Notes: A Small + Note Link Or An Open Note Box On Each Card?",
  ("note_link", "Small + Note Link", "Tap + Note to add a few words.", "calm", scr(stackq(68, QS[:4], note=True))),
  ("note_box", "Note Box Open", "A note box shows under the question.", "focused", scr(noteopen())))
# 15 context: show source line vs not
def ctx(show):
    s = ""
    for i, (q, src) in enumerate(zip(QS[:4], ["Commits 8422814, 64a81b4", "Tax deadline Oct 15", "Public page shows address", "Org chart deck"])):
        h = 54 if show else 44; y = 68 + i * (h + 6)
        if y + h > 280: break
        s += qcard(y, q, h) + (T(B, 22, y + 34, src, 7.5, M) if show else "")
    return s
P("Notes", "Show A Line Of Background Under Each Question?",
  ("ctx_yes", "Background Line", "One grey line: why the agent is asking.", "focused", scr(ctx(True))),
  ("ctx_no", "Question Only", "Just the question; tap for detail.", "quick", scr(ctx(False))))
# 16 how answer returns
def ret(feed):
    s = stackq(68, QS[2:4]) + T(B, 14, 180, "SENT TO AGENTS", 7.5, M, w=600, ex='letter-spacing="1"')
    rows = [("Miles", "Yes, undo", "Received 19:31"), ("Portfolio", "Single", "Received 19:32")]
    for i, (a, v, t) in enumerate(rows):
        y = 186 + i * 30
        s += card(B, 14, y, 212, 26) + T(B, 24, y + 11, a.upper(), 7.5, M, w=600) + T(B, 24, y + 21, v, 8, INK) + T(B, 216, y + 16, t if feed else "Sent", 7.5, JUNGLE, w=600, a="end")
    return s
P("Answer Return", "After Submit: Show Each Agent Got Your Answer, Or Just A Sent Message?",
  ("ret_recv", "Show Received", "A Sent To Agents list ticks Received when the agent picks it up.", "focused", scr(ret(True))),
  ("ret_sent", "Just Sent", "A short 'Sent' and the cards go away.", "quick", scr(stackq(68, QS[2:4]) + R(14, 186, 212, 24, "#E3F1EA", r=6) + T(B, 120, 201, "2 answers sent", 8.5, JUNGLE, w=600, a="middle"))))
# 17 return route: to agent inbox vs also in team feed
def route(feed):
    s = R(14, 72, 212, 64, "#FFFFFF", B["line"], 8) + T(B, 24, 88, "Your answer goes to", 7.5, M) + T(B, 24, 104, "Portfolio inbox", 11, INK, True) + T(B, 24, 120, "ops/submit/inbox/portfolio", 7.5, M)
    if feed: s += R(14, 144, 212, 52, "#FFFFFF", B["line"], 8) + T(B, 24, 160, "And the Team Feed", 7.5, M) + T(B, 24, 176, "Max answered: Single", 10, INK, True)
    return s
P("Answer Return", "Answers Go Only To The Agent, Or Also Show In The Team Feed?",
  ("rt_agent", "Only The Agent", "Private: straight to that agent's inbox.", "calm", scr(route(False))),
  ("rt_feed", "Agent And Team Feed", "Other agents can see the decision too.", "visual", scr(route(True))))
# 18 phone vs desktop
def desk2():
    s = T(B, 14, 76, "Big screen: two columns", 7.5, M)
    for i, q in enumerate(QS[:6]):
        x = 14 + (i % 2) * 108; y = 82 + (i // 2) * 62
        s += card(B, x, y, 104, 56) + T(B, x + 6, y + 12, q[0].upper(), 7.5, M, w=600) + D(x + 96, y + 9, 3, q[4]) + T(B, x + 6, y + 24, fit(q[1], 21), 7.5, INK, w=600) + btn(x + 6, y + 36, 42, "Yes") + btn(x + 52, y + 36, 42, "No", False)
    return s
P("Phone And Desktop", "On A Big Screen: Two Columns Of Cards Or One Centred Column?",
  ("pd_two", "Two Columns", "More questions visible at once on desktop.", "visual", scr(desk2())),
  ("pd_one", "One Centred Column", "Same single column as phone, centred.", "calm", scr(stackq(68, QS[:4]))))
# 19 phone: full page vs sheet
def sheet():
    return R(0, 0, 240, 300, "#0A0A0A22") + R(0, 120, 240, 180, "#FFFFFF", B["line"], 14) + R(108, 126, 24, 3, B["line"], r=1.5) + qcard(138, QS[0]) + qcard(188, QS[1])
P("Phone And Desktop", "On Phone: Questions Inside The Page Or A Slide-Up Sheet?",
  ("ph_page", "Inside The Page", "Questions sit in the page under Evening Report.", "calm", scr(stackq(68, QS[:4]))),
  ("ph_sheet", "Slide-Up Sheet", "Tap Questions, a sheet slides up over the page.", "focused", screen(head() + R(14, 68, 212, 24, "#FFFFFF", B["line"], 6) + T(B, 24, 83, "Questions (6)", 9, INK, True) + sheet())))
# 20 counts
def counts(kind):
    if kind == "stats":
        s = ""
        for i, (n, l, c) in enumerate([("6", "Open", INK), ("3", "Urgent", TERRA), ("2", "Due Today", SAFFRON)]):
            x = 14 + i * 72; s += card(B, x, 68, 68, 36) + T(B, x + 8, 88, n, 14, c, True) + T(B, x + 8, 99, l, 7.5, M)
        return s + stackq(112, QS[:3])
    return T(B, 14, 76, "6 open, 3 urgent", 8.5, INK, w=600) + stackq(84, QS[:4])
P("Counts", "Counts: Three Stat Boxes Or One Line Of Text?",
  ("cnt_box", "Three Stat Boxes", "Open, Urgent, Due Today as small boxes.", "visual", scr(counts("stats"))),
  ("cnt_line", "One Line", "'6 open, 3 urgent' above the cards.", "quick", scr(counts("line"))))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Questions Center Deck", "Grok Bot", pairs,
        {"brands": ["Questions Center on the Grok Bot Command Center, below Evening Report; format reused for Legal, Research, Coach"],
         "submit_agent": "grok-bot", "submit_to": "Grok Bot (ops/submit/inbox/grok-bot)", "section_counts": cnt, "deck_size": N,
         "sources": {"sample": "/workspace/ops/grokbot/decisions-2026-10-14.md"}}, seed=1414, n=N)
