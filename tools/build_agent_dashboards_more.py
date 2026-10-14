#!/usr/bin/env python3
"""Build Style Swipe deck agent-dashboards-more (Oct 14 2026): Agent Dashboards Deck Two, 20 this-or-that pairs on
boards that got few or no pairs last time (UpKeep internal board, Deck Building, Branding, Legal, Blog, Dump, Japan
Cottage, Video & Photo, Jokes, Miles, WellNest, Portfolio) plus cross-dashboard Routines (R65) presentation.
Uses each board's live sections (checked Oct 14). Skips everything settled in dashboard-rulebook.md (R1-R65), and every
pair in agent-dashboards, folio/upkeep/deck-board (+Details) and rulebook-tiebreak decks. No live/customer apps.
Pattern copied from build_agent_dashboards.py (team_kit.publish, dash_kit). Crisp text: every full-scale label >= 8
viewBox units (mockups are vector SVG, so they render sharp at 2x/3x). Routing:
/workspace/ops/brand/agent-dashboards-more-routing.md. Submit -> agent 'branding'. Drawn example mockups only."""
import sys, os, re, json; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON, W
from dash_kit import R, T, L, D, chev, phone
DID = "agent-dashboards-more"; MIN = 8
B = dict(name="Agent", bg="#FDFBF6", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F3ECDD", acc=[TERRA, LAGOON, JUNGLE, SAFFRON],
         head="Khand, sans-serif", body="Hind, sans-serif", r=6, hw=600)
INK, MUTE, LN = B["ink"], B["mute"], B["line"]; ACC = B["acc"]; WH = "#FFFFFF"
pairs, O, add = deck("am_", "Agent Dashboards Deck Two")
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

# ===================== UpKeep (internal board only) =====================
P("UpKeep", "UpKeep Board Deadlines: Next Three With Days Left Or A Month Strip?",
  ("uk_next", "Next Three, Days Left", "Three closest deadlines as rows, days left on the right.", "focused",
   frame("UpKeep", sec(54, "Deadlines") + rows(62, ["Example deadline one", "Example deadline two", "Example deadline three"], ["3 days", "9 days", "21 days"]) + sec(160, "Current Status") + rows(168, ["Example status row"]), LAGOON)),
  ("uk_strip", "Month Strip", "Four weeks across, a dot on each deadline day; tap a dot for details.", "visual",
   frame("UpKeep", sec(54, "Deadlines") + card(14, 62, 212, 84) + "".join(tx(30 + i * 30, 78, d, 8, MUTE, w=600, a="middle") for i, d in enumerate("MTWTFSS")) + "".join(D(30 + (i % 7) * 30, 92 + (i // 7) * 14, 3.5 if i in (3, 10, 25) else 1.6, LAGOON if i in (3, 10, 25) else LN) for i in range(28)) + sec(166, "Current Status") + rows(174, ["Example status row"]), LAGOON)))
P("UpKeep", "UpKeep Board Current Status: Row Per Area With A Coloured Dot Or One Plain Sentence?",
  ("uk_dots", "Row Per Area, Coloured Dot", "Site, Video, Legal, Sign-Ups: green, amber or red dot each.", "focused",
   frame("UpKeep", sec(54, "Current Status") + "".join(card(14, 62 + i * 26, 212, 22) + D(26, 73 + i * 26, 4, c) + tx(36, 76 + i * 26, n, 8.5, INK, w=600) + tx(218, 76 + i * 26, t, 8, MUTE, a="end") for i, (n, c, t) in enumerate([("Site", JUNGLE, "On track"), ("Video", JUNGLE, "On track"), ("Legal", SAFFRON, "Waiting"), ("Sign-Ups", TERRA, "Blocked")])) + sec(186, "Links") + rows(194, ["Example link"]), LAGOON)),
  ("uk_sent", "One Plain Sentence", "A short written status, updated with each report.", "calm",
   frame("UpKeep", sec(54, "Current Status") + card(14, 62, 212, 62) + tx(24, 80, "Example: site and video on track;", 8.5, INK) + tx(24, 94, "legal waiting on Max; sign-ups", 8.5, INK) + tx(24, 108, "blocked until terms are signed.", 8.5, INK) + sec(146, "Links") + rows(154, ["Example link"]), LAGOON)))
# ===================== Deck Building =====================
P("Deck Building", "Deck Building Requests From Agents: Cards With Build / Not Now Or Plain Rows?",
  ("db_req_btn", "Cards With Build / Not Now", "Each request shows who asked and two buttons.", "warm",
   frame("Deck Building", sec(54, "Requests From Agents") + "".join(card(14, 62 + i * 56, 212, 50) + tx(24, 78 + i * 56, f"Example Request {i+1}", 9.5, INK, True) + tx(216, 78 + i * 56, ["From Legal", "From Blog"][i], 8, MUTE, a="end") + btn(24, 88 + i * 56, 54, "Build", JUNGLE) + btn(84, 88 + i * 56, 60, "Not Now", INK, False) for i in range(2)), TERRA)),
  ("db_req_rows", "Plain Rows", "One row per request, agent on the right, tap to open.", "focused",
   frame("Deck Building", sec(54, "Requests From Agents") + rows(62, ["Example request one", "Example request two", "Example request three"], ["Legal", "Blog", "Miles"], edge=False), TERRA)))
P("Deck Building", "Deck Building Results In: Top Picks As Words Or As Small Pictures?",
  ("db_res_words", "Top Picks As Words", "Three winning picks written out, link to full results.", "focused",
   frame("Deck Building", sec(54, "Results In") + card(14, 62, 212, 104) + tx(24, 80, "Example Deck, 19 of 20", 10, INK, True) + "".join(tx(24, 98 + i * 16, f"{i+1}.", 8.5, TERRA, w=600) + tx(36, 98 + i * 16, t, 8.5, INK) for i, t in enumerate(["Example pick one", "Example pick two", "Example pick three"])) + tx(24, 156, "See All Results", 8.5, LAGOON, w=600), TERRA)),
  ("db_res_pics", "Top Picks As Small Pictures", "The three winning mockups as small thumbnails.", "visual",
   frame("Deck Building", sec(54, "Results In") + card(14, 62, 212, 120) + tx(24, 80, "Example Deck, 19 of 20", 10, INK, True) + "".join(R(24 + i * 66, 90, 58, 66, ACC[i] + "1F", LN, 4) + R(30 + i * 66, 98, 46, 6, ACC[i], r=2) + ln(30 + i * 66, 112, 40) + ln(30 + i * 66, 120, 30) + tx(53 + i * 66, 150, f"Pick {i+1}", 8, INK, w=600, a="middle") for i in range(3)) + tx(24, 174, "See All Results", 8.5, LAGOON, w=600), TERRA)))
# ===================== Branding =====================
P("Branding", "Branding Accent Colors: Big Swatches Or Chips With The Hex Code?",
  ("br_swatch", "Big Swatches", "Four large colour blocks with the name under each.", "visual",
   frame("Branding", sec(54, "Accent Colors") + "".join(R(14 + i * 54, 62, 50, 60, c, r=6) + tx(39 + i * 54, 136, n, 8, INK, w=600, a="middle") for i, (c, n) in enumerate(zip(ACC, ["Terracotta", "Lagoon", "Jungle", "Saffron"]))) + sec(166, "Brand Files") + rows(174, ["Example file"]), TERRA)),
  ("br_chips", "Chips With Hex Code", "A row per colour: dot, name, hex, where it is used.", "focused",
   frame("Branding", sec(54, "Accent Colors") + "".join(card(14, 62 + i * 24, 212, 20) + D(26, 72 + i * 24, 5, c) + tx(36, 75 + i * 24, n, 8.5, INK, w=600) + tx(110, 75 + i * 24, hx, 8, MUTE) + tx(218, 75 + i * 24, u, 8, MUTE, a="end") for i, (c, n, hx, u) in enumerate(zip(ACC, ["Terracotta", "Lagoon", "Jungle", "Saffron"], ["#C1502E", "#05668D", "#0B6E4F", "#D4A017"], ["Actions", "Links", "Done", "Reports"]))) + sec(178, "Brand Files") + rows(186, ["Example file"]), TERRA)))
P("Branding", "Branding Brand Files: Picture Grid Or File Rows?",
  ("br_grid", "Picture Grid", "Each logo or mark as a picture tile, name under it.", "visual",
   frame("Branding", sec(54, "Brand Files") + "".join(R(14 + (i % 3) * 72, 62 + (i // 3) * 64, 68, 58, WH, LN, 6) + D(48 + (i % 3) * 72, 84 + (i // 3) * 64, 11, ACC[i % 4] + "55") + tx(48 + (i % 3) * 72, 112 + (i // 3) * 64, ["Logo", "Mark", "Icon", "Fonts", "Colors", "Footer"][i], 8, INK, w=600, a="middle") for i in range(6)) + sec(206, "UpKeep Marks") + rows(214, ["Example mark"]), TERRA)),
  ("br_rows", "File Rows", "One row per file: name, type, last changed.", "focused",
   frame("Branding", sec(54, "Brand Files") + rows(62, ["Logo", "Mark", "Icon", "Fonts", "Footer"], ["SVG", "SVG", "PNG", "CSS", "HTML"], edge=False) + sec(198, "UpKeep Marks") + rows(206, ["Example mark"]), TERRA)))
# ===================== Legal =====================
P("Legal", "Legal Open Matters: One List With A Status Tag Or Grouped By Status?",
  ("lg_tag", "One List, Status Tag", "Every matter on one list, a coloured tag on each.", "focused",
   frame("Legal", sec(54, "Open Legal Matters") + "".join(card(14, 62 + i * 26, 212, 22) + tx(24, 76 + i * 26, n, 8.5, INK, w=600) + pill(218, 76 + i * 26, t, c, a="end") for i, (n, t, c) in enumerate([("Example matter one", "Waiting", TERRA), ("Example matter two", "Drafted", LAGOON), ("Example matter three", "Review", SAFFRON), ("Example matter four", "Ready", JUNGLE), ("Example matter five", "Waiting", TERRA)])), INK)),
  ("lg_grp", "Grouped By Status", "Waiting On Max, With Attorney, Drafted: each a small group.", "calm",
   frame("Legal", "".join(tx(14, y, h, 8, c, w=600) + "".join(card(14, y + 6 + j * 24, 212, 20, c) + tx(24, y + 19 + j * 24, f"Example matter", 8.5, INK, w=600) for j in range(n)) for y, h, c, n in [(52, "WAITING ON MAX", TERRA, 2), (118, "WITH ATTORNEY", SAFFRON, 1), (160, "DRAFTED", LAGOON, 2)]), INK)))
P("Legal", "Legal Matter Risk: A Word Tag Or A Three-Step Meter?",
  ("lg_word", "Word Tag", "Low, Medium or High written in a small tag.", "focused",
   frame("Legal", sec(54, "Open Legal Matters") + "".join(card(14, 62 + i * 40, 212, 34) + tx(24, 76 + i * 40, "Example matter", 9, INK, True) + tx(24, 89 + i * 40, "Example next step", 8, MUTE) + pill(218, 80 + i * 40, r, c, a="end") for i, (r, c) in enumerate([("High", TERRA), ("Medium", SAFFRON), ("Low", JUNGLE)])), INK)),
  ("lg_meter", "Three-Step Meter", "Three small bars fill up with the risk level.", "visual",
   frame("Legal", sec(54, "Open Legal Matters") + "".join(card(14, 62 + i * 40, 212, 34) + tx(24, 76 + i * 40, "Example matter", 9, INK, True) + tx(24, 89 + i * 40, "Example next step", 8, MUTE) + "".join(R(176 + k * 14, 74 + i * 40, 11, 8, (c if k < n else LN), r=2) for k in range(3)) for i, (n, c) in enumerate([(3, TERRA), (2, SAFFRON), (1, JUNGLE)])), INK)))
# ===================== Blog =====================
P("Blog", "Blog Posts: Separate Sections Or One Stage Strip (Draft, Rewrite, Ready)?",
  ("bl_secs", "Separate Sections", "Rewrites / Ready To Publish, then New Drafts, as now.", "calm",
   frame("Blog", sec(54, "Ready To Publish") + rows(62, ["Example post title", "Example post title"]) + sec(126, "New Drafts") + rows(134, ["Example post title", "Example post title", "Example post title"]), SAFFRON)),
  ("bl_strip", "One Stage Strip", "Tabs with counts: Draft, Rewrite, Ready; one list below.", "focused",
   frame("Blog", "".join(R(14 + i * 72, 46, 68, 30, (SAFFRON + "26" if i == 2 else WH), (SAFFRON if i == 2 else LN), 6) + tx(48 + i * 72, 59, n, 8.5, INK, w=600, a="middle") + tx(48 + i * 72, 71, c, 8, MUTE, a="middle") for i, (n, c) in enumerate([("Draft", "10"), ("Rewrite", "3"), ("Ready", "1")])) + rows(88, ["Example post title", "Example post title", "Example post title"]), SAFFRON)))
P("Blog", "Blog Drafts: Title Rows Or Cards With The First Line?",
  ("bl_title", "Title Rows", "Title only, status on the right, tap to read.", "focused",
   frame("Blog", sec(54, "New Drafts") + rows(62, ["Example post title one", "Example post title two", "Example post title three", "Example post title four", "Example post title five"], ["Draft"], edge=False), SAFFRON)),
  ("bl_first", "Cards With First Line", "Title plus the opening line of the post.", "warm",
   frame("Blog", sec(54, "New Drafts") + "".join(card(14, 62 + i * 52, 212, 46) + tx(24, 78 + i * 52, f"Example Post Title {i+1}", 9.5, INK, True) + tx(24, 92 + i * 52, "Example: the first line of the post,", 8, MUTE) + tx(24, 102 + i * 52, "cut off after two lines...", 8, MUTE) for i in range(3)), SAFFRON)))
# ===================== Dump =====================
P("Dump", "Dump Open Items: Priority Tabs Or One List With P Tags?",
  ("dp_tabs", "Priority Tabs", "P0 / P1 / P2 tabs with counts; one list at a time.", "focused",
   frame("Dump", "".join(R(14 + i * 72, 44, 68, 20, (TERRA if i == 0 else WH), (TERRA if i == 0 else LN), 10) + tx(48 + i * 72, 57.5, n, 8.5, WH if i == 0 else INK, w=600, a="middle") for i, n in enumerate(["P0  2", "P1  2", "P2  17"])) + rows(76, ["Example urgent item", "Example urgent item"]) + sec(148, "Handed Off") + rows(156, ["Example item"]), TERRA)),
  ("dp_tags", "One List With P Tags", "All items together, highest priority first, tag on each.", "calm",
   frame("Dump", sec(54, "Open Items") + "".join(card(14, 62 + i * 26, 212, 22) + pill(22, 76 + i * 26, p, c, True) + tx(52, 76 + i * 26, "Example item", 8.5, INK, w=600) for i, (p, c) in enumerate([("P0", TERRA), ("P0", TERRA), ("P1", SAFFRON), ("P1", SAFFRON), ("P2", MUTE)])) + tx(14, 198, "See All 21", 8.5, LAGOON, w=600), TERRA)))
P("Dump", "Dump Handed Off: Grouped Under Each Agent Or An Agent Chip On Each Row?",
  ("dp_grp", "Grouped Under Each Agent", "Agent name as a small heading, its items under it.", "calm",
   frame("Dump", sec(54, "Handed Off") + "".join(tx(14, y, n, 8, c, w=600) + rows(y + 6, ["Example item"] * k) for y, n, c, k in [(72, "PROP", JUNGLE, 2), (138, "CONSTRUCTION", TERRA, 2), (204, "WELLNEST", SAFFRON, 1)]), TERRA)),
  ("dp_chip", "Agent Chip On Each Row", "Newest first; a coloured agent chip leads each row.", "focused",
   frame("Dump", sec(54, "Handed Off") + "".join(card(14, 62 + i * 26, 212, 22) + pill(22, 76 + i * 26, n, c) + tx(26 + len(n) * 4.3 + 14, 76 + i * 26, "Example item", 8.5, INK, w=600) for i, (n, c) in enumerate([("Prop", JUNGLE), ("Construction", TERRA), ("WellNest", SAFFRON), ("Prop", JUNGLE), ("Scout", LAGOON)])), TERRA)))
# ===================== Japan Cottage =====================
P("Japan Cottage", "Japan Cottage Status: Listing Count Tiles Or The Newest Listing Card?",
  ("jc_count", "Listing Count Tiles", "Akiya and other sources as count tiles, new today marked.", "focused",
   frame("Japan Cottage", sec(54, "Status") + "".join(card(14 + i * 72, 62, 68, 56) + tx(48 + i * 72, 92, v, 16, INK, True, a="middle") + tx(48 + i * 72, 108, n, 8, MUTE, a="middle") for i, (v, n) in enumerate([("199", "Akiya"), ("12", "New Today"), ("4", "Saved")])) + sec(140, "Recent Work") + rows(148, ["Example item", "Example item"]), JUNGLE)),
  ("jc_new", "Newest Listing Card", "Newest listing with a drawn house picture, price and town.", "warm",
   frame("Japan Cottage", sec(54, "Status") + card(14, 62, 212, 100, JUNGLE) + R(24, 70, 70, 84, JUNGLE + "1F", r=4) + f'<path d="M36 128 L59 104 L82 128 Z M42 128 V146 H76 V128" fill="none" stroke="{JUNGLE}" stroke-width="1.6"/>' + tx(104, 86, "NEWEST", 8, JUNGLE, w=600) + tx(104, 104, "Example Town", 10, INK, True) + tx(104, 120, "Example price", 8.5, MUTE) + tx(104, 146, "Open Swipe", 8.5, LAGOON, w=600) + sec(184, "Recent Work") + rows(192, ["Example item"]), JUNGLE)))
# ===================== Video & Photo =====================
P("Video & Photo", "Video & Photo Current Work: Picture Cards Or Rows With A Stage Tag?",
  ("vp_pic", "Picture Cards", "Each project as a card with a frame from the video.", "visual",
   frame("Video & Photo", sec(54, "Current Work") + "".join(card(14 + (i % 2) * 109, 62 + (i // 2) * 84, 103, 78) + thumb(20 + (i % 2) * 109, 68 + (i // 2) * 84, 91, 46, ACC[i]) + tx(20 + (i % 2) * 109, 130 + (i // 2) * 84, f"Example Project {i+1}", 8.5, INK, w=600) for i in range(4)), LAGOON)),
  ("vp_stage", "Rows With A Stage Tag", "Project name, stage tag: Script, Edit, Review, Published.", "focused",
   frame("Video & Photo", sec(54, "Current Work") + "".join(card(14, 62 + i * 26, 212, 22) + tx(24, 76 + i * 26, f"Example project {i+1}", 8.5, INK, w=600) + pill(218, 76 + i * 26, s, c, a="end") for i, (s, c) in enumerate([("Edit", LAGOON), ("Review", SAFFRON), ("Script", MUTE), ("Published", JUNGLE), ("Edit", LAGOON)])), LAGOON)))
# ===================== Jokes =====================
P("Jokes", "Jokes Bits In Progress: Index Cards Or Rows With A Draft Count?",
  ("jk_idx", "Index Cards", "Each bit as a small card showing its premise.", "warm",
   frame("Jokes", sec(54, "Bits In Progress") + "".join(card(14 + (i % 2) * 109, 62 + (i // 2) * 66, 103, 60, ACC[i]) + tx(22 + (i % 2) * 109, 80 + (i // 2) * 66, f"Example Bit {i+1}", 9.5, INK, True) + tx(22 + (i % 2) * 109, 95 + (i // 2) * 66, "Example premise", 8, MUTE) + tx(22 + (i % 2) * 109, 107 + (i // 2) * 66, "line here", 8, MUTE) for i in range(4)), SAFFRON)),
  ("jk_rows", "Rows With A Draft Count", "Bit name and how many drafts so far.", "focused",
   frame("Jokes", sec(54, "Bits In Progress") + rows(62, ["Example bit one", "Example bit two", "Example bit three", "Example bit four"], ["Draft 3", "Draft 1", "Draft 2", "Draft 5"]) + sec(176, "Recently Done") + rows(184, ["Example bit"]), SAFFRON)))
# ===================== Miles =====================
P("Miles Agent", "Miles Open Items: Grouped By Waiting, Watching, Done Or One List With Tags?",
  ("mi_grp", "Grouped By Status", "Waiting On Max first, then Watching, then Done.", "calm",
   frame("Miles", "".join(tx(14, y, h, 8, c, w=600) + rows(y + 6, ["Example item"] * n) for y, h, c, n in [(52, "WAITING ON MAX", TERRA, 2), (118, "WATCHING", LAGOON, 1), (160, "DONE", JUNGLE, 1)]), LAGOON)),
  ("mi_tags", "One List With Tags", "All open items together, a status tag on each.", "focused",
   frame("Miles", sec(54, "Open Items") + "".join(card(14, 62 + i * 26, 212, 22) + tx(24, 76 + i * 26, "Example item", 8.5, INK, w=600) + pill(218, 76 + i * 26, s, c, a="end") for i, (s, c) in enumerate([("Waiting", TERRA), ("Waiting", TERRA), ("Today", SAFFRON), ("Watching", LAGOON), ("Done", JUNGLE)])), LAGOON)))
# ===================== WellNest =====================
P("WellNest", "WellNest Add To Home Screen: Steps Card On The Board Or A Small Help Link?",
  ("wn_steps", "Steps Card On The Board", "Three drawn steps always shown on the dashboard.", "warm",
   frame("WellNest", sec(54, "Add To Home Screen") + card(14, 62, 212, 84) + "".join(D(30, 80 + i * 22, 7, SAFFRON + "33") + tx(30, 83 + i * 22, str(i + 1), 8, INK, w=600, a="middle") + tx(44, 83 + i * 22, s, 8.5, INK) for i, s in enumerate(["Tap Share in the browser", "Choose Add To Home Screen", "Tap Add"])) + sec(168, "Open Items") + rows(176, ["Example item", "Example item"]), SAFFRON)),
  ("wn_link", "Small Help Link", "One line near the bottom; steps open on tap.", "calm",
   frame("WellNest", sec(54, "Open Items") + rows(62, ["Example item", "Example item", "Example item"]) + sec(152, "Apps And Links") + rows(160, ["Example app"]) + tx(14, 212, "How To Add To Home Screen", 8.5, LAGOON, w=600) + chev(140, 209, LAGOON), SAFFRON)))
# ===================== Portfolio =====================
P("Portfolio", "Portfolio Open Items: Newest First Or Grouped By Area (Tax, Rental, Insurance)?",
  ("pf_new", "Newest First", "One list, newest change at the top, status on the right.", "focused",
   frame("Portfolio", sec(54, "Open Items") + rows(62, ["Example item one", "Example item two", "Example item three", "Example item four"], ["In progress"], edge=False), TERRA)),
  ("pf_area", "Grouped By Area", "Small headings: Tax, Rental, Insurance; items under each.", "calm",
   frame("Portfolio", "".join(tx(14, y, h, 8, c, w=600) + rows(y + 6, ["Example item"] * n, edge=False) for y, h, c, n in [(52, "TAX", TERRA, 1), (92, "RENTAL", LAGOON, 2), (158, "INSURANCE", JUNGLE, 1)]), TERRA)))
# ===================== Routines (cross-dashboard, R65) =====================
P("All Dashboards (Routines, R65)", "Routines Section Look: A Card Per Group Or One Table With Group Lines?",
  ("rt_cards", "A Card Per Group", "Reports, Daily, Weekly each in its own white card.", "calm",
   frame("Routines", sec(54, "Routines") + "".join(card(14, y, 212, 14 + n * 18, c) + tx(24, y + 12, g, 8, c, w=600) + "".join(tx(24, y + 27 + j * 18, "Example routine", 8.5, INK, w=600) + tx(218, y + 27 + j * 18, "Ran 5:00 AM", 8, MUTE, a="end") for j in range(n)) for y, g, c, n in [(62, "REPORTS", SAFFRON, 2), (122, "DAILY", LAGOON, 2), (182, "WEEKLY", JUNGLE, 1)]), LAGOON)),
  ("rt_table", "One Table, Group Lines", "One table: name, when, last run; thin group lines.", "focused",
   frame("Routines", sec(54, "Routines") + tbl(62, ["NAME", "WHEN", "LAST RUN"], [24, 118, 172], [["REPORTS"] + ["", ""], ["Example routine", "4:47 AM", "5:00 AM"], ["Example routine", "6:00 PM", "Yesterday"], ["DAILY", "", ""], ["Example routine", "8:03 AM", "8:05 AM"], ["WEEKLY", "", ""], ["Example routine", "Sundays", "Oct 11"]], h=20), LAGOON)))
P("All Dashboards (Routines, R65)", "Routines On Phone: All Groups Open Or Only Reports Open, Rest Folded?",
  ("rt_open", "All Groups Open", "Every routine shown; the section is longer.", "calm",
   frame("Routines", sec(54, "Routines") + "".join(tx(14, y, g, 8, c, w=600) + rows(y + 6, ["Example routine"] * n, ["On"], edge=False, h=20) for y, g, c, n in [(72, "REPORTS", SAFFRON, 2), (130, "DAILY", LAGOON, 2), (188, "WEEKLY", JUNGLE, 2)]), LAGOON)),
  ("rt_fold", "Reports Open, Rest Folded", "Reports shown; Daily, Weekly, Monthly fold with a count.", "focused",
   frame("Routines", sec(54, "Routines") + tx(14, 72, "REPORTS", 8, SAFFRON, w=600) + rows(78, ["Morning Report", "Evening Report"], ["On"], edge=False, h=20) + "".join(card(14, 132 + i * 26, 212, 22) + tx(24, 146 + i * 26, g, 8.5, INK, w=600) + tx(196, 146 + i * 26, n, 8, MUTE, a="end") + chev(210, 143 + i * 26, MUTE) for i, (g, n) in enumerate([("Daily", "3"), ("Weekly", "2"), ("Monthly", "1")])), LAGOON)))
N = len(pairs); assert N == 20, N
# crisp check: no full-scale text under MIN
for p in pairs:
    for o in (p["optionA"], p["optionB"]):
        small = [float(v) for v in re.findall(r'font-size="([\d.]+)"', o["visual"]["svg"]) if float(v) < MIN]
        assert not small, (o["id"], small)
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Agent Dashboards Deck Two", "Agent Dashboards Deck Two", pairs,
        {"brands": ["Agent Dashboards Deck Two: board-specific layout choices for UpKeep (internal board), Deck Building, Branding, Legal, Blog, Dump, Japan Cottage, Video & Photo, Jokes, Miles, WellNest, Portfolio, plus the Routines section (R65)",
                    "Cream #FDFBF6 page, white cards, Khand/Hind, terracotta/lagoon/jungle/saffron accents; skips everything settled in the Dashboard Rulebook (R1-R65) and earlier board decks; text at least 8 units, vector mockups"],
         "submit_agent": "branding", "submit_to": "Branding Agent", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "routing": "/workspace/ops/brand/agent-dashboards-more-routing.md"},
        seed=1416, n=N)
d = json.load(open(f"decks/{DID}.json"))
json.dump([{"n": i + 1, "ask": p["ask"], "group": p.get("group"), "a": [p["optionA"]["id"], p["optionA"]["label"]], "b": [p["optionB"]["id"], p["optionB"]["label"]]} for i, p in enumerate(d["pairs"])], open("/tmp/am_route.json", "w"))
