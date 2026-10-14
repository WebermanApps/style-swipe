#!/usr/bin/env python3
"""Build Style Swipe deck org-chart (Oct 14 2026): Org Chart Deck, exactly 20 this-or-that pairs on how Max's agent
organization should look and be shown. Based on the current org chart (ops/apps-home/agents.json: Grok Bot main; Work =
UpKeep, WellNest, Prop, Scout, Construction; Personal = Portfolio, Blueprint, Thai, Blog, Japan Cottage, Miles, Jokes;
AIR = Branding, Research, Coach, Video & Photo, Dump, Legal, Security; UpKeep Content not yet on the chart).
Pattern from build_agent_dashboards_more.py (team_kit.publish, dash_kit). Crisp: every label >= 8 units (floor 7.5).
Submit -> agent 'grok-bot' (ops/submit/inbox/grok-bot via pull.sh grok-bot). Drawn example mockups only."""
import sys, os, re, json; sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, chev, phone
DID = "org-chart"; MIN = 8
B = dict(name="Agent", bg="#FDFBF6", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=6, hw=600)
INK, MUTE, LN = B["ink"], B["mute"], B["line"]; ACC = B["acc"]; WH = "#FFFFFF"
pairs, O, add = deck("oc_", "Org Chart Deck")
ROUTE = []
def P(agent, ask, a, b): ROUTE.append(agent); add(agent, agent, O(*a), O(*b), ask)
def tx(x, y, s, sz=8, c=INK, h=False, w=None, a="start"): return T(B, x, y, s, max(sz, MIN), c, h, w, a)
def share(x, y): return f'<g transform="translate({x},{y}) scale(.5)"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{INK}" stroke-width="2.2"/></g>'
def card(x, y, w, h, edge=None): return R(x, y, w, h, WH, LN, B["r"]) + (R(x, y, 3, h, edge, r=1.5) if edge else "")
def ln(x, y, w, c=MUTE + "77"): return R(x, y, w, 3, c, r=1.5)
def sec(y, s): return tx(14, y, s, 11, INK, True)
def pill(x, y, s, c, solid=False, a="start"):
    w = len(s) * 4.3 + 12; x = x - w if a == "end" else x
    return R(x, y - 9, w, 12, c if solid else c + "1F", r=6) + tx(x + w / 2, y, s, 8, WH if solid else c, w=600, a="middle")
def frame(name, body, c=TERRA):
    s = R(0, 0, W, 32, WH) + L(0, 32, W, 32, LN) + chev(12, 16, MUTE) + tx(18, 19, "Apps Home", 8, MUTE, w=600)
    s += tx(120, 21, name, 12, INK, True, a="middle") + share(212, 9) + D(170, 16, 2.5, c)
    s += body + tx(120, 293, "Built by Max Weberman", 8, "#8A8580", a="middle")
    return phone(B, s)
def rows(y, items, right=None, edge=True, h=22):
    s = ""
    for i, it in enumerate(items):
        yy = y + i * (h + 4); s += card(14, yy, 212, h, ACC[i % 4] if edge else None) + tx(24, yy + h / 2 + 3, it, 8.5, INK, w=600)
        if right: s += tx(218, yy + h / 2 + 3, right[i % len(right)], 8, MUTE, a="end")
    return s
def hbar(x, y, w, f, c): return R(x, y, w, 5, LN, r=2.5) + R(x, y, w * f, 5, c, r=2.5)
def chk(x, y, on, c=JUNGLE): return f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{c if on else "none"}" stroke="{c}"/>'
def btn(x, y, w, s, c, solid=True): return R(x, y, w, 15, c if solid else WH, c, 7.5) + tx(x + w / 2, y + 10.5, s, 8, WH if solid else c, w=600, a="middle")
def thumb(x, y, w, h, c): return R(x, y, w, h, c + "26", r=4) + f'<path d="M{x+w/2-4} {y+h/2-5} L{x+w/2+5} {y+h/2} L{x+w/2-4} {y+h/2+5} Z" fill="{c}"/>'
def tbl(y, heads, xs, data, h=22):
    s = card(14, y, 212, 18 + len(data) * h) + "".join(tx(x, y + 13, hd, 8, MUTE, w=600) for x, hd in zip(xs, heads))
    for i, r in enumerate(data):
        yy = y + 18 + i * h; s += L(20, yy, 220, yy, LN)
        for j, (x, v) in enumerate(zip(xs, r)): s += v if v.startswith("<") else tx(x, yy + 14.5, v, 8.5 if j == 0 else 8, INK if j == 0 else MUTE, w=600 if j == 0 else None)
    return s

GRP = {"Work": TERRA, "Personal": LAGOON, "AIR": JUNGLE}
WORK = ["UpKeep", "WellNest", "Prop", "Scout", "Construction"]
PERS = ["Portfolio", "Blueprint", "Thai", "Blog", "Japan Cottage", "Miles", "Jokes"]
AIR = ["Branding", "Research", "Coach", "Video & Photo", "Dump", "Legal", "Security"]
def node(x, y, w, s, c, h=18, paused=False, solid=False):
    f = c if solid else (WH if not paused else "#F3F1EC")
    return R(x, y, w, h, f, LN if not solid else c, 4) + (R(x, y, 3, h, c, r=1.5) if not solid else "") + tx(x + w / 2, y + h / 2 + 3, s, 8, WH if solid else (MUTE if paused else INK), w=600, a="middle")
def vline(x, y1, y2, c=LN): return L(x, y1, x, y2, c)
def hub(y=44, c=SAFFRON): return node(80, y, 80, "Grok Bot", c, 20, solid=True)
def groups_tree(y, names, sub=None):
    s = hub() + vline(120, 64, y - 8) + L(40, y - 8, 200, y - 8, LN)
    for i, g in enumerate(names):
        x = 40 + i * 80; s += vline(x, y - 8, y) + node(x - 36, y, 72, g, GRP.get(g, LAGOON), 18, solid=True)
        for j, a in enumerate((sub or {}).get(g, [])): s += vline(x, y + 18, y + 24 + j * 22) + node(x - 36, y + 24 + j * 22, 72, a, GRP.get(g, LAGOON), 18)
    return s
def gcards(y, gs, n=3):
    s = ""
    for g, items in gs:
        c = GRP.get(g, MUTE); h = 18 + 16 * ((len(items[:n * 3]) + 1) // 2)
        s += card(14, y, 212, h, c) + tx(24, y + 12, g.upper(), 8, c, w=600)
        for k, a in enumerate(items): s += tx(24 + (k % 2) * 100, y + 27 + (k // 2) * 16, a, 8.5, INK, w=600)
        y += h + 6
    return s
def tiles(y, items, cols=3, h=34):
    s = ""; w = (212 - (cols - 1) * 6) / cols
    for k, (a, c) in enumerate(items):
        x, yy = 14 + (k % cols) * (w + 6), y + (k // cols) * (h + 6)
        s += R(x, yy, w, h, c + "1F", r=6) + D(x + 11, yy + 11, 4, c) + tx(x + 8, yy + h - 8, a, 8, INK, w=600)
    return s
ALLW = [(a, TERRA) for a in WORK]; ALLP = [(a, LAGOON) for a in PERS]; ALLA = [(a, JUNGLE) for a in AIR]
def tabs(y, on="Work", names=("Work", "Personal", "AIR")):
    s = ""; w = 212 / len(names)
    for i, n in enumerate(names):
        x = 14 + i * w; c = GRP.get(n, INK)
        s += (R(x, y, w - 4, 18, c, r=9) + tx(x + w / 2 - 2, y + 12, n, 8, WH, w=600, a="middle")) if n == on else (R(x, y, w - 4, 18, WH, LN, 9) + tx(x + w / 2 - 2, y + 12, n, 8, MUTE, w=600, a="middle"))
    return s

# ===================== Grouping =====================
P("Grouping", "Org Chart Groups: Keep Three Tabs (Work, Personal, AIR) Or One Page With Three Sections?",
  ("tabs3", "Three Tabs", "Work, Personal, AIR as tabs; one group shown at a time.", "focused",
   frame("Org Chart", tabs(44) + rows(70, WORK))),
  ("onepage", "One Page, Three Sections", "All three groups on one scrolling page, a heading each.", "calm",
   frame("Org Chart", gcards(44, [("Work", WORK), ("Personal", PERS), ("AIR", AIR)]))))
P("Grouping", "Where Does Dump Belong: In AIR Or Straight Under Grok Bot?",
  ("dump_air", "Dump In AIR", "Dump stays with the other shared helpers in AIR.", "calm",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"AIR": ["Dump", "Research", "Coach"]}))),
  ("dump_hub", "Dump Under Grok Bot", "Dump sits beside Grok Bot as its inbox, outside the groups.", "focused",
   frame("Org Chart", hub() + L(160, 54, 176, 54, LN) + node(176, 45, 50, "Dump", JUNGLE) + vline(120, 64, 88) + L(40, 88, 200, 88, LN) + "".join(vline(40 + i * 80, 88, 96) + node(4 + i * 80, 96, 72, g, GRP[g], solid=True) for i, g in enumerate(GRP)))))
P("Grouping", "Prop And Construction: Stay In Work Or Get Their Own Property Group?",
  ("prop_work", "Stay In Work", "Prop and Construction stay in Work with UpKeep and WellNest.", "calm",
   frame("Org Chart", gcards(44, [("Work", WORK)]) + gcards(140, [("Personal", PERS)]))),
  ("prop_own", "Own Property Group", "A fourth group: Prop, Construction, Japan Cottage, Blueprint.", "focused",
   frame("Org Chart", gcards(44, [("Work", ["UpKeep", "WellNest", "Scout"]), ("Property", ["Prop", "Construction", "Japan Cottage", "Blueprint"]), ("Personal", ["Portfolio", "Thai", "Blog", "Miles", "Jokes"])]))))
# ===================== Reporting =====================
P("Who Reports To Whom", "Grok Bot As Hub: Every Agent Wired To Grok Bot Or Grok Bot Over Three Group Leads?",
  ("hub_all", "Every Agent To Grok Bot", "One hub; each agent has a direct line to Grok Bot.", "focused",
   frame("Org Chart", hub(130) + "".join(L(120, 140, 120 + 92 * __import__('math').cos(k * 0.449), 140 + 92 * __import__('math').sin(k * 0.449), LN) for k in range(14)) + "".join(node(120 + 92 * __import__('math').cos(k * 0.449) - 26, 140 + 92 * __import__('math').sin(k * 0.449) - 8, 52, a, c, 16) for k, (a, c) in enumerate((ALLW + ALLP[:4] + ALLA[:5])[:14])))),
  ("hub_leads", "Grok Bot Over Group Leads", "Grok Bot over Work, Personal, AIR; agents under each.", "calm",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"Work": ["UpKeep", "WellNest", "Prop"], "Personal": ["Portfolio", "Thai", "Blog"], "AIR": ["Branding", "Research", "Security"]}))))
P("Who Reports To Whom", "Security: Stay Under AIR Or Report Straight To Grok Bot?",
  ("sec_air", "Under AIR", "Security sits in AIR with Legal and Research.", "calm",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"AIR": ["Security", "Legal", "Research"]}))),
  ("sec_hub", "Straight To Grok Bot", "Security reports to Grok Bot directly and watches every group.", "focused",
   frame("Org Chart", hub() + L(80, 54, 64, 54, LN) + node(14, 45, 50, "Security", INK) + groups_tree(96, ["Work", "Personal", "AIR"], {"AIR": ["Legal", "Research"]})[len(hub()):])))
P("Who Reports To Whom", "Legal: Shared Helper In AIR Or Placed With The Work Agents?",
  ("legal_air", "Shared Helper In AIR", "Legal serves every group from AIR.", "calm",
   frame("Org Chart", gcards(44, [("AIR", ["Legal", "Security", "Research", "Branding"])]) + tx(14, 140, "Serves: Work, Personal", 8.5, MUTE))),
  ("legal_work", "With The Work Agents", "Legal sits in Work next to Prop, Construction and UpKeep.", "focused",
   frame("Org Chart", gcards(44, [("Work", WORK + ["Legal"])]) + gcards(140, [("AIR", ["Branding", "Research", "Coach", "Security"])]))))
P("Who Reports To Whom", "Show Hand-Offs Between Agents (For Example Branding To WellNest) Or Only Reporting Lines?",
  ("lines_only", "Only Reporting Lines", "Clean tree: who reports to whom, nothing else.", "calm",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"Work": ["WellNest"], "AIR": ["Branding"]}))),
  ("handoffs", "Show Hand-Offs Too", "Dashed lines for regular hand-offs between agents.", "focused",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"Work": ["WellNest"], "AIR": ["Branding"]}) + f'<path d="M164 129 Q120 150 76 129" fill="none" stroke="{SAFFRON}" stroke-width="1.4" stroke-dasharray="3 2"/>' + tx(120, 160, "Hand-off", 8, SAFFRON, w=600, a="middle"))))
# ===================== Display =====================
P("Display Style", "Org Chart Look: A Tree With Lines Or Group Cards?",
  ("disp_tree", "Tree With Lines", "Boxes joined by lines, Grok Bot at the top.", "focused",
   frame("Org Chart", groups_tree(96, ["Work", "Personal", "AIR"], {"Work": ["UpKeep", "Prop"], "Personal": ["Thai", "Blog"], "AIR": ["Legal", "Coach"]}))),
  ("disp_cards", "Group Cards", "One white card per group listing its agents.", "calm",
   frame("Org Chart", gcards(44, [("Work", WORK), ("Personal", PERS), ("AIR", AIR)]))))
P("Display Style", "Agents Shown As Group Cards Or As Coloured Tiles?",
  ("disp_cards2", "Group Cards", "Names listed inside a white card per group.", "calm",
   frame("Org Chart", gcards(44, [("Work", WORK), ("AIR", AIR)]))),
  ("disp_tiles", "Coloured Tiles", "Each agent its own tile, coloured by group.", "visual",
   frame("Org Chart", tiles(44, ALLW + ALLA[:7], 3))))
P("Display Style", "Org Chart On Phone: All Groups Open Or Folded With A Count?",
  ("ph_open", "All Groups Open", "Every agent visible; longer page.", "calm",
   frame("Org Chart", gcards(44, [("Work", WORK), ("Personal", PERS), ("AIR", AIR)]))),
  ("ph_fold", "Folded With A Count", "Tap a group to open it; counts shown.", "focused",
   frame("Org Chart", hub() + "".join(card(14, 76 + i * 30, 212, 24, c) + tx(24, 92 + i * 30, g, 9, INK, True) + tx(196, 92 + i * 30, str(n), 8.5, MUTE, a="end") + chev(210, 89 + i * 30, MUTE) for i, (g, c, n) in enumerate([("Work", TERRA, 5), ("Personal", LAGOON, 7), ("AIR", JUNGLE, 7)])))))
P("Display Style", "Each Agent Box Shows: Name Only Or Name With A Status Dot And Last Activity?",
  ("box_name", "Name Only", "Just the agent name; quiet and simple.", "calm",
   frame("Org Chart", rows(44, ["UpKeep", "WellNest", "Prop", "Construction", "Scout"], edge=True))),
  ("box_status", "Name, Dot, Last Activity", "Green or grey dot and when it last shipped.", "focused",
   frame("Org Chart", "".join(card(14, 44 + i * 26, 212, 22) + D(26, 55 + i * 26, 3, c) + tx(36, 58 + i * 26, a, 8.5, INK, w=600) + tx(218, 58 + i * 26, t, 8, MUTE, a="end") for i, (a, c, t) in enumerate([("UpKeep", JUNGLE, "14:35"), ("WellNest", JUNGLE, "13:10"), ("Prop", JUNGLE, "Yesterday"), ("Construction", JUNGLE, "Oct 12"), ("Scout", "#BDB6AA", "Paused")])))))
# ===================== Where on Apps Home =====================
P("Where It Lives", "On Apps Home: Org Chart At The Top Or As Its Own Team Tab?",
  ("ah_top", "At The Top", "A small chart above the Work, Personal, AIR tabs.", "visual",
   frame("Apps Home", card(14, 44, 212, 70) + hub(52) + "".join(node(24 + i * 66, 86, 60, g, GRP[g], 16, solid=True) for i, g in enumerate(GRP)) + tabs(124) + rows(150, WORK[:3]))),
  ("ah_tab", "Own Team Tab", "A fourth tab, Team, holds the org chart.", "calm",
   frame("Apps Home", tabs(44, "Team", ("Work", "Personal", "AIR", "Team")) + groups_tree(110, ["Work", "Personal", "AIR"])[0:0] + gcards(70, [("Work", WORK), ("AIR", AIR)]))))
P("Where It Lives", "Apps Home Link: A Small Org Chart Link Or Grok Bot Card Opens The Chart?",
  ("ah_link", "Small Link At The Bottom", "One line, View Org Chart, near the footer.", "calm",
   frame("Apps Home", tabs(44) + rows(70, WORK) + tx(14, 220, "View Org Chart", 8.5, LAGOON, w=600) + chev(84, 217, LAGOON))),
  ("ah_card", "Grok Bot Card Opens It", "Tap the Grok Bot card at the top to see the chart.", "focused",
   frame("Apps Home", card(14, 44, 212, 40, SAFFRON) + tx(24, 62, "Grok Bot", 11, INK, True) + tx(24, 76, "Team Org Chart", 8, MUTE) + chev(212, 64, MUTE) + tabs(94) + rows(120, WORK[:4]))))
# ===================== Naming =====================
P("Naming", "Agent Names: Short (Branding, Miles) Or With Agent (Branding Agent, Miles Agent)?",
  ("nm_short", "Short Names", "Branding, Miles, Research: no Agent word.", "calm",
   frame("Org Chart", rows(44, ["Branding", "Miles", "Research", "Coach", "Legal"]))),
  ("nm_agent", "With Agent", "Branding Agent, Miles Agent, Research Agent.", "focused",
   frame("Org Chart", rows(44, ["Branding Agent", "Miles Agent", "Research Agent", "Coach Agent", "Legal Agent"]))))
P("Naming", "Third Group Name: AIR Or AI Resources?",
  ("nm_air", "AIR", "Short tab name; fits the phone tab bar.", "focused",
   frame("Org Chart", tabs(44) + rows(70, AIR[:5]))),
  ("nm_air_long", "AI Resources", "Spelled out, like the Dropbox folder 03 AI Resources.", "calm",
   frame("Org Chart", tabs(44, "AI Resources", ("Work", "Personal", "AI Resources")) + rows(70, AIR[:5]))))
# ===================== Merge / add =====================
P("Merge Or Add", "UpKeep Content: Its Own Agent Box Or Folded Into UpKeep?",
  ("uc_own", "Own Box In Work", "UpKeep Content added to Work beside UpKeep.", "focused",
   frame("Org Chart", gcards(44, [("Work", WORK + ["UpKeep Content"])]))),
  ("uc_sub", "Under UpKeep", "Shown as a small sub-box under UpKeep.", "calm",
   frame("Org Chart", node(60, 44, 120, "UpKeep", TERRA, 20, solid=True) + vline(120, 64, 80) + node(70, 80, 100, "UpKeep Content", TERRA) + gcards(116, [("Work", ["WellNest", "Prop", "Scout", "Construction"])]))))
P("Merge Or Add", "Video & Photo And Branding: Keep Two Agents Or Merge Into One Creative Agent?",
  ("vp_two", "Keep Two", "Branding for look and words; Video & Photo for media.", "calm",
   frame("Org Chart", gcards(44, [("AIR", AIR)]))),
  ("vp_one", "Merge Into Creative", "One Creative agent covers brand, video and photo.", "focused",
   frame("Org Chart", gcards(44, [("AIR", ["Creative", "Research", "Coach", "Dump", "Legal", "Security"])]))))
P("Merge Or Add", "Blog And Jokes: Keep Separate Or Merge Into One Writing Agent?",
  ("bj_two", "Keep Separate", "Blog and Jokes stay two Personal agents.", "calm",
   frame("Org Chart", gcards(44, [("Personal", PERS)]))),
  ("bj_one", "One Writing Agent", "A Writing agent with Blog and Jokes as sections.", "focused",
   frame("Org Chart", gcards(44, [("Personal", ["Portfolio", "Blueprint", "Thai", "Writing", "Japan Cottage", "Miles"])]))))
# ===================== Paused =====================
P("Paused Agents", "Paused Scout And Japan Cottage: Greyed In Place Or Moved To A Paused Group?",
  ("pz_grey", "Greyed In Place", "Stay in their group, grey with a Paused tag.", "calm",
   frame("Org Chart", "".join(node(14, 44 + i * 24, 212, a, TERRA, 20, paused=(a == "Scout")) for i, a in enumerate(WORK)) + pill(218, 122, "Paused", MUTE, a="end"))),
  ("pz_group", "Paused Group", "A grey Paused group at the bottom.", "focused",
   frame("Org Chart", gcards(44, [("Work", ["UpKeep", "WellNest", "Prop", "Construction"])]) + gcards(108, [("Paused", ["Scout", "Japan Cottage"])]))))
P("Paused Agents", "Paused Agents On Apps Home: Hidden Or Shown With A Resume Note?",
  ("pz_hide", "Hidden", "Paused agents leave Apps Home until resumed.", "focused",
   frame("Apps Home", tabs(44) + rows(70, ["UpKeep", "WellNest", "Prop", "Construction"]))),
  ("pz_note", "Shown With A Resume Note", "Kept at the end, grey, with what restarts them.", "calm",
   frame("Apps Home", tabs(44) + rows(70, ["UpKeep", "WellNest", "Prop", "Construction"]) + card(14, 174, 212, 30) + tx(24, 187, "Scout", 8.5, MUTE, w=600) + tx(24, 199, "Paused. Resumes when Max asks.", 8, MUTE))))
N = len(pairs); assert N == 20, N
for p in pairs:
    for o in (p["optionA"], p["optionB"]):
        small = [float(v) for v in re.findall(r'font-size="([\d.]+)"', o["visual"]["svg"]) if float(v) < MIN]
        assert not small, (o["id"], small)
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Org Chart Deck", "Org Chart Deck", pairs,
        {"brands": ["Org Chart Deck: how the agent organization should look and be shown (groups Work/Personal/AIR, reporting to Grok Bot, display style, place on Apps Home, naming, merges and additions, paused agents)",
                    "Cream #FDFBF6 page, white cards, Khand/Hind; based on the current Apps Home org chart; text at least 8 units, vector mockups"],
         "submit_agent": "grok-bot", "submit_to": "Grok Bot", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True},
        seed=1447, n=N, first=0)
d = json.load(open(f"decks/{DID}.json")); print(len(d["pairs"]))
for i, p in enumerate(d["pairs"]): print(i + 1, p["group"], "|", p["ask"])
