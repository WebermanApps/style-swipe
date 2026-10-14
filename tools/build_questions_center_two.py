#!/usr/bin/env python3
"""Build Style Swipe deck questions-center-two: Questions Center Deck Two (Oct 14 2026, after Max's 19:53 results).
Cards 1-3 re-ask skips 06 / 13 / 14 in clearer words (R64/C10); the rest are new open questions; settled picks are drawn as the base
(card each, all on one page, urgency pills sorted first, days left, one count line, buttons + text, Ask for more detail, + Note, Submit bar + Send).
Helpers reused from build_questions_center.py. Submit -> agent 'grok-bot'."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
_s = open(os.path.join(os.path.dirname(__file__), "build_questions_center.py")).read()
exec(_s[_s.index("from team_kit"):_s.index("# 1 layout")].replace('"Evening Report"', '"Morning Report"'))
DID = "questions-center-two"
pairs, O, add = deck("qc2_", "Grok Bot")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
REL = {"Today": "Due today", "Oct 15": "Due tomorrow", "Oct 17": "In 3 days", "Oct 30": "In 16 days", "": ""}
def q2(y, q, h=54, more="link", send=True, due="all", ans="both", note=True, folded=False):
    ag, txt, urg, d, c = q
    s = card(B, 14, y, 212, h) + T(B, 22, y + 12, ag.upper(), 7.5, M, w=600) + pill(170 if urg != "Urgent" else 164, y + 4, urg, c, urg == "Urgent")[0]
    dl = REL.get(d, d)
    if dl and (due == "all" or (due == "close" and urg == "Urgent")): s += T(B, 150, y + 12, dl, 7.5, TERRA if urg == "Urgent" else M, a="end")
    s += T(B, 22, y + 24, fit(txt, 46), 8.5, INK, w=600)
    s += btn(22, y + 29, 34, "Yes") + btn(60, y + 29, 34, "No", False) + R(98, y + 29, 120, 15, B["soft"], B["line"], 4) + T(B, 103, y + 39.5, "Or type...", 7.5, M)
    if more == "link": s += T(B, 22, y + h - 2, "Ask for more detail", 7.5, LAGOON, w=600)
    elif more == "btn": s += R(22, y + h - 11, 82, 12, "#FFFFFF", LAGOON, 6) + T(B, 63, y + h - 2.5, "Ask for more detail", 7.5, LAGOON, w=600, a="middle")
    if note: s += T(B, 160, y + h - 2, "+ Note", 7.5, LAGOON, w=600, a="end")
    if send: s += T(B, 218, y + h - 2, "Send", 7.5, JUNGLE, w=600, a="end")
    return s
def stack2(y0, qs, h=54, gap=6, **k):
    s = ""
    for i, q in enumerate(qs):
        y = y0 + i * (h + gap)
        if y + h > 256: break
        s += q2(y, q, h, **k)
    return s
def cnt(y=76, txt="6 open, 3 urgent"): return T(B, 14, y, txt, 8.5, INK, w=600)
def bar(): return R(14, 264, 212, 16, INK, r=5) + T(B, 120, 275, "SUBMIT ANSWERS", 7.5, "#FFFFFF", w=600, a="middle", ex='letter-spacing="1"')
def scr2(body): return scr(body + bar())
def base(**k): return scr2(cnt() + stack2(82, QS[:4], **k))
# 1 skip 06
def feed(show):
    s = cnt() + q2(82, QS[1]) + R(14, 140, 212, 13, "#E3F1EA", r=4) + T(B, 20, 149.5, "Answered: Single", 7.5, JUNGLE, w=600)
    s += T(B, 14, 172, "TEAM FEED", 7.5, M, w=600, ex='letter-spacing="1"') + card(B, 14, 178, 212, 32)
    s += T(B, 22, 192, "Max decided: Sal files Single" if show else "Nothing posted: only Portfolio needed this", 8, INK if show else M, w=600)
    s += T(B, 22, 204, "Seen by Portfolio, Prop, Grok Bot" if show else "Posted only when another agent needs it", 7.5, M)
    return scr2(s)
P("Answer Sharing", "After You Answer: Post Your Answer To The Team Feed Too, Or Only Post It When Another Agent Needs It?",
  ("sh_feed", "Always Post To Team Feed", "Every answer also shows in the Team Feed so all agents see it.", "open", feed(True)),
  ("sh_need", "Only When Another Agent Needs It", "The asking agent gets it; the Team Feed only when another agent's work depends on it.", "focused", feed(False)))
# 2 skip 13
def groups(folded):
    s = cnt()
    if folded:
        for i, (n, c, k) in enumerate([("Urgent", TERRA, 3), ("Soon", SAFFRON, 2), ("Later", LAGOON, 1)]):
            y = 82 + i * 30; s += card(B, 14, y, 212, 24) + T(B, 24, y + 15, n, 9, c, True) + T(B, 196, y + 15, f"{k} questions", 7.5, M, a="end") + chev(214, y + 12, M)
        s += T(B, 14, 186, "Tap a group to open it", 7.5, M)
    else: s += T(B, 14, 92, "URGENT", 7.5, TERRA, w=600) + stack2(96, QS[:3])
    return scr2(s)
P("Grouping", "Urgent, Soon, Later: Show Only The Group Names With A Count Until You Tap, Or Show Every Question Straight Away?",
  ("gr_fold", "Group Names With Counts", "Three short rows; tap one to see its questions.", "calm", groups(True)),
  ("gr_open", "Every Question Straight Away", "All question cards visible, urgent first.", "quick", groups(False)))
# 3 skip 14
P("Due Dates", "Due Dates On The Cards: On Every Question That Has One, Or Only On Questions Due In The Next 2 Days?",
  ("dd_all", "Every Question With A Date", "Due today, tomorrow, in 16 days all shown.", "informative", base(due="all")),
  ("dd_close", "Only Due In The Next 2 Days", "Far-off dates hidden until they get close.", "calm", base(due="close")))
P("Ask For Detail", "'Ask For More Detail': A Small Text Link Or An Outlined Button?",
  ("am_link", "Small Text Link", "Quiet link under the answer row.", "calm", base(more="link")),
  ("am_btn", "Outlined Button", "Easier to spot and tap.", "clear", base(more="btn")))
def asked(inline):
    s = cnt() + q2(82, QS[0], more=None)
    if inline: s += R(22, 134, 196, 22, "#EEF5F9", LAGOON, 5) + T(B, 28, 147.5, "Asked Miles for more detail. Waiting...", 7.5, LAGOON, w=600)
    else: s += R(14, 134, 212, 30, "#FFFFFF", B["line"], 6) + T(B, 22, 146, "What else do you need to know?", 7.5, M) + R(22, 150, 150, 11, B["soft"], B["line"], 3) + btn(178, 148, 40, "Ask")
    return scr2(s + stack2(176, QS[1:3]))
P("Ask For Detail", "Tapping 'Ask For More Detail': Sends Right Away, Or Opens A Box To Say What You Need?",
  ("ad_now", "Sends Right Away", "One tap; the agent replies with more detail.", "quick", asked(True)),
  ("ad_box", "Box To Say What You Need", "Type what is unclear, then Ask.", "precise", asked(False)))
def waiting(where):
    s = cnt()
    if where == "card": s += q2(82, QS[0], more=None) + R(150, 84, 0, 0) + R(110, 84, 50, 11, "#EEF5F9", r=5) + T(B, 135, 92, "Detail asked", 7.5, LAGOON, w=600, a="middle") + stack2(140, QS[1:3])
    else: s += stack2(82, QS[1:3]) + T(B, 14, 200, "WAITING FOR DETAIL", 7.5, LAGOON, w=600, ex='letter-spacing="1"') + card(B, 14, 206, 212, 26) + T(B, 22, 222, "Miles: password gate question", 8, INK)
    return scr2(s)
P("Ask For Detail", "While You Wait For Detail: The Question Stays In Place With A Tag, Or Moves To A 'Waiting For Detail' List?",
  ("wd_place", "Stays In Place", "A small 'Detail asked' tag on the card.", "steady", waiting("card")),
  ("wd_list", "Moves To Waiting List", "Out of the way until the agent replies.", "tidy", waiting("list")))
P("Send Buttons", "With Both A Submit Bar And A Send On Each Card: Send Label In Green Text Or A Small Outlined Button?",
  ("sb_text", "Green Text", "Light; the Submit bar stays the main action.", "calm", base()),
  ("sb_btn", "Small Outlined Button", "Each card can clearly be sent alone.", "action",
   scr2(cnt() + "".join(q2(82 + i * 60, q, send=False) + R(186, 82 + i * 60 + 41, 34, 11, "#FFFFFF", JUNGLE, 5) + T(B, 203, 82 + i * 60 + 49.5, "Send", 7.5, JUNGLE, w=600, a="middle") for i, q in enumerate(QS[:3])))))
P("Typed Answers", "Typed Answer Box: One Line That Grows, Or A Taller Box From The Start?",
  ("ta_line", "One Line That Grows", "Compact until you type.", "compact", base()),
  ("ta_tall", "Taller Box", "Room for a longer answer.", "roomy",
   scr2(cnt() + "".join(card(B, 14, 82 + i * 86, 212, 78) + T(B, 22, 94 + i * 86, q[0].upper(), 7.5, M, w=600) + pill(164 if q[2] == "Urgent" else 170, 86 + i * 86, q[2], q[4], q[2] == "Urgent")[0] + T(B, 22, 106 + i * 86, fit(q[1], 46), 8.5, INK, w=600) + btn(22, 111 + i * 86, 34, "Yes") + btn(60, 111 + i * 86, 34, "No", False) + R(22, 130 + i * 86, 196, 24, B["soft"], B["line"], 4) + T(B, 27, 141 + i * 86, "Type your answer", 7.5, M) for i, q in enumerate(QS[:2])))))
P("Empty State", "When There Are No Questions: A Calm 'All answered' Line Or Hide The Section?",
  ("es_line", "Calm Line", "'All answered. Nothing waiting on you.'", "calm", scr(head() + card(B, 14, 70, 212, 30) + T(B, 24, 89, "All answered. Nothing waiting on you.", 8.5, M) + FOOT)),
  ("es_hide", "Hide The Section", "Next section moves up.", "minimal", scr(head() + T(B, 14, 82, "Open Items", 11, INK, True) + card(B, 14, 90, 212, 24) + card(B, 14, 118, 212, 24) + FOOT)))
def newbadge(on):
    s = cnt() + q2(82, QS[3]) + (R(120, 84, 30, 11, JUNGLE, r=5.5) + T(B, 135, 92, "New", 7.5, "#FFFFFF", w=600, a="middle") if on else "") + stack2(140, QS[4:6])
    return scr2(s)
P("New Questions", "A Question That Just Arrived: Green 'New' Badge Or No Badge?",
  ("nq_badge", "Green New Badge", "Until you have seen it.", "clear", newbadge(True)),
  ("nq_none", "No Badge", "Order already shows what matters.", "calm", newbadge(False)))
def agentrow(style):
    q = QS[1]; s = cnt() + card(B, 14, 82, 212, 50)
    if style == "caps": s += T(B, 22, 94, "PORTFOLIO", 7.5, M, w=600)
    else: s += D(26, 91, 5, LAGOON) + T(B, 26, 93.5, "P", 7.5, "#FFFFFF", w=700, a="middle") + T(B, 36, 94, "Portfolio", 8, INK, w=600)
    s += T(B, 22, 106, q[1], 8.5, INK, w=600) + btn(22, 111, 34, "MFS") + btn(60, 111, 40, "Single", False) + pill(164, 86, "Urgent", TERRA, True)[0]
    return scr2(s + stack2(140, QS[2:4]))
P("Agent Name", "Which Agent Is Asking: Small Grey Capitals Or A Coloured Initial Plus Name?",
  ("an_caps", "Small Grey Capitals", "PORTFOLIO above the question.", "quiet", agentrow("caps")),
  ("an_init", "Coloured Initial Plus Name", "Easier to scan by agent.", "visual", agentrow("init")))
def snooze(on):
    s = cnt() + q2(82, QS[4], more=None) + (T(B, 22, 130, "Later today", 7.5, M, w=600) + T(B, 80, 130, "Tomorrow", 7.5, M, w=600) if on else "") + stack2(146, QS[2:4])
    return scr2(s)
P("Not Now", "A Question You Cannot Answer Yet: 'Remind Me Tomorrow' Option, Or Just Leave It?",
  ("nn_snooze", "Remind Me Option", "Hide it until later today or tomorrow.", "relief", snooze(True)),
  ("nn_leave", "Just Leave It", "It stays where it is.", "simple", snooze(False)))
P("Order", "Within Each Urgency: Soonest Due First, Or Oldest Question First?",
  ("or_due", "Soonest Due First", "Due today before due tomorrow.", "focused", base()),
  ("or_old", "Oldest Question First", "Questions waiting longest come first.", "fair",
   scr2(cnt() + "".join(q2(82 + i * 60, q) + T(B, 218, 82 + i * 60 + 12, ["Asked 3 days ago", "Asked yesterday", "Asked today"][i], 7.5, M, a="end") for i, q in enumerate([QS[2], QS[0], QS[1]])))))
def count(kind):
    t = {"open": "6 open, 3 urgent", "today": "6 open, 3 urgent, 2 answered today"}[kind]
    return scr2(cnt(txt=t) + stack2(82, QS[:4]))
P("Counts", "Count Line: '6 open, 3 urgent' Or Add '2 answered today'?",
  ("cl_open", "Open And Urgent Only", "Shorter.", "quick", count("open")),
  ("cl_today", "Add Answered Today", "Shows progress too.", "motivating", count("today")))
P("Big Screen", "On A Big Screen: One Centred Column At Reading Width, Or The Column Fills The Width?",
  ("bw_read", "Reading Width", "Narrow centred column, wide margins.", "calm", desk_col(True) if False else scr(head() + R(0, 64, 240, 200, B["soft"]) + "".join(q2(64 + 10 + i * 58, q) for i, q in enumerate(QS[:3])).replace('x="14"', 'x="34"') + FOOT)),
  ("bw_full", "Fills The Width", "Cards stretch edge to edge.", "bold", scr(head() + "".join(q2(70 + i * 58, q) for i, q in enumerate(QS[:3])) + FOOT)))
P("Answered Today", "Answered Questions After Submit: Gone Completely, Or A Small 'Answered today (3)' Link?",
  ("at_gone", "Gone Completely", "Only open questions stay.", "clean", base()),
  ("at_link", "Answered Today Link", "Tap to look back at today's answers.", "reassuring", scr2(cnt() + stack2(82, QS[:3]) + T(B, 14, 258, "Answered today (3)", 7.5, LAGOON, w=600))))
P("Other Boards", "Legal, Research And Coach: Exactly The Same Look, Or Each Keeps Its Own Accent Colour?",
  ("ob_same", "Exactly The Same", "One Questions Center everywhere.", "consistent", base()),
  ("ob_accent", "Own Accent Colour", "Same layout, the board's accent on buttons.", "personal",
   base().replace(JUNGLE, "#8A5BB5")))
def words(alt):
    qs = [(a, t, {"Urgent": "Today", "Soon": "This Week", "Later": "Anytime"}[u] if alt else u, d, c) for a, t, u, d, c in QS[:4]]
    return scr2(cnt(txt="6 open, 3 today" if alt else "6 open, 3 urgent") + "".join(q2(82 + i * 60, q).replace(f">{q[2]}<", f">{q[2]}<") for i, q in enumerate(qs)))
P("Urgency", "Urgency Words: Urgent, Soon, Later Or Today, This Week, Anytime?",
  ("uw_urg", "Urgent, Soon, Later", "How pressing it is.", "direct", words(False)),
  ("uw_time", "Today, This Week, Anytime", "When it needs an answer.", "practical", words(True)))
def big(on):
    s = cnt()
    for i, q in enumerate(QS[:3]):
        y = 82 + i * 62; s += card(B, 14, y, 212, 56) + T(B, 22, y + 12, q[0].upper(), 7.5, M, w=600) + pill(164 if q[2] == "Urgent" else 170, y + 4, q[2], q[4], q[2] == "Urgent")[0]
        s += T(B, 22, y + (28 if on else 24), fit(q[1], 34 if on else 46), 11 if on else 8.5, INK, True if on else False, w=None if on else 600)
        s += btn(22, y + 36, 34, "Yes") + btn(60, y + 36, 34, "No", False) + T(B, 22, y + 54, "Ask for more detail", 7.5, LAGOON, w=600)
    return scr2(s)
P("Question Text", "Question Wording Size: Same As Other Card Text, Or Larger Headline?",
  ("qt_same", "Same Size", "More questions fit on screen.", "compact", big(False)),
  ("qt_big", "Larger Headline", "Question reads first.", "bold", big(True)))
def wide(on):
    s = cnt()
    for i, q in enumerate(QS[:3]):
        y = 82 + i * 60; s += card(B, 14, y, 212, 54) + T(B, 22, y + 12, q[0].upper(), 7.5, M, w=600) + T(B, 22, y + 24, fit(q[1], 46), 8.5, INK, w=600)
        s += (btn(22, y + 29, 96, "Yes") + btn(122, y + 29, 96, "No", False) if on else btn(22, y + 29, 34, "Yes") + btn(60, y + 29, 34, "No", False)) + T(B, 22, y + 52, "Ask for more detail", 7.5, LAGOON, w=600)
    return scr2(s)
P("Phone Buttons", "On Phone: Yes / No Buttons Split The Full Width, Or Small Buttons On The Left?",
  ("pb_full", "Full Width", "Big tap targets.", "easy", wide(True)),
  ("pb_small", "Small On The Left", "Room for the text box beside them.", "compact", wide(False)))
N = len(pairs); assert N == 20, N
cnt_ = {}
for p in pairs: cnt_[p["group"]] = cnt_.get(p["group"], 0) + 1
publish(DID, "Questions Center Deck Two", "Grok Bot", pairs,
        {"brands": ["Questions Center Deck Two: skips 06/13/14 re-asked first in clearer words, then new open questions; settled picks drawn as the base"],
         "submit_agent": "grok-bot", "submit_to": "Grok Bot (ops/submit/inbox/grok-bot)", "section_counts": cnt_, "deck_size": N, "carried": 3, "topic": "questions-center",
         "follows": {"deck": "questions-center", "submission": "cc7fec14", "answered": 17, "total": 20},
         "sources": {"results": "/workspace/style-swipe/results/questions-center.txt", "rulebook": "/workspace/ops/brand/dashboard-rulebook.md Questions Center spec"}}, seed=2006, n=N, first=3)
