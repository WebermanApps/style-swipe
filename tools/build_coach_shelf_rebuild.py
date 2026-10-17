#!/usr/bin/env python3
"""Coach shelf rebuild (Branding, Oct 17 2026 ICT; Coach's ask relayed by Grok Bot). No results submitted for any of the three decks.
1) Rule Cleanup: Buttons, Names & Caps -> "Rule Cleanup: Names, Labels & Sources" (same deck id + URL): drops Love Button (settled R82/R89:
   Love kept), Sticky Header (R87), Locked Pages Rule (R119 wrote it into the rulebook) and Shelf Cap (R86/R97); adds 4 open rulebook items.
2) Rule Cleanup: Files, Copies & Retests (same id + URL): drops Questionnaire Size ('must be 20', settled by R86/R87); adds Rulebook Copy.
3) Dashboard Layout Deck (20 picks, mostly about sections removed Oct 16) is retired (unlisted, status retired, replaced_by) and replaced by
   "Header And Footer Details": 10 open questions on the R76/R79/R87/R106 branded header and footer. No Share-placement questions
   (waiting on Max), nothing from the open Main Dashboard Rules / All Boards Rules decks (S1-S18), nothing a rule already settles.
Kept picks keep their option ids, svgs and order; new picks get drawn mockups (R89). R105 captions, light only, Khand/Hind, no Thai."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from team_kit import *
from caption_rule import guard
from split_deck import theme_name_ok
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREAM = "#FAF6EE"; DIV = "#d9d1c3"; FAINT = "#9A948A"

# ---------- shared drawing ----------
def head_doc(y, title, sub):
    return t(14, y + 22, title, 14, INK, "khand") + t(14, y + 34, sub, 7.5, MUTE) + ln(y + 42), 50
def rule_row(y, code, text, c=INK, tagtxt="", tagc=TERRA, strike=False, fill="#FFFFFF"):
    s = rect(14, y, 212, 30, fill, LINE, 4) + t(22, y + 19, code, 9.5, c, "khand")
    s += t(56, y + 19, text, 7.5, FAINT if strike else INK, "hind", 500, extra='text-decoration="line-through"' if strike else "")
    if tagtxt: w = len(tagtxt) * 5.8 * .76 + 10; s += tag(218 - w, y + 9.5, tagtxt, tagc)
    return s, 36
def doc(title, sub, rows, note=None, bg="#FFFFFF"):
    blocks = [("raw",) + head_doc(0, title, sub)]
    y = 50
    for r in rows:
        g, h = rule_row(y, *r); blocks.append(("raw", g, h)); y += h
    if note: blocks += [("gap", 4), ("banner", note[0], note[1], note[2])]
    return render(blocks, bg)
def home_btn(y):
    return rect(14, y, 64, 18, "#FFFFFF", INK, 0, 1) + ic("home", 18, y + 3, 12, INK, 2) + t(33, y + 12.5, "APPS HOME", 7.5, INK, "khand"), 24
def cc(y, title, lines=None, size=13):
    lines = lines or [title]; s = mono(14, y + 4, "C", TERRA, 22)
    for i, l in enumerate(lines): s += t(42, y + 15 + i * (size + 1), l, size, INK, "khand")
    yy = y + 15 + (len(lines) - 1) * (size + 1)
    s += t(42, yy + 11, "Coaching and team habits", 7.5, MUTE) + shareic(208, y + 6)
    return s, yy - y + 20
def deckcard(x, y, name, new=True, w=64, ask=False):
    if ask:
        return rect(x, y, w, 58, "#FFFFFF", "#BDB6AA", 10, 1, 'stroke-dasharray="3 2"') + t(x + w / 2, y + 26, "+", 14, TERRA, "khand", anchor="middle") + t(x + w / 2, y + 42, "Ask For A Deck", 7.5, INK, "hind", 600, "middle")
    s = rect(x, y, w, 58, "#FFFFFF", LINE, 10) + rect(x, y, w, 22, CREAM, "none", 10) + rect(x, y + 12, w, 10, CREAM)
    s += t(x + 6, y + 36, name, 7.5, INK, "khand") + t(x + 6, y + 47, "10 picks", 7.5, MUTE)
    if new: s += rect(x + w - 26, y + 46, 22, 9, CREAM, "none") + t(x + w - 15, y + 53, "NEW", 7.5, TERRA, "khand", anchor="middle")
    return s
def shelf(y, names=("Rule Cleanup", "Team Ideas", "Habits"), ask=False):
    s = t(14, y + 9, "READY TO SWIPE", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"')
    for i, n in enumerate(names): s += deckcard(14 + i * 72, y + 14, n)
    if ask: s += deckcard(14 + len(names) * 72, y + 14, "", ask=True)
    return s, 80
def counter(y, txt, link=False):
    s = t(14, y + 11, txt, 8.5, INK, "hind", 600)
    if link: s += t(226, y + 11, "Deck Building", 7.5, LAGOON, "hind", 600, "end", 'text-decoration="underline"')
    return s, 18
def fold(y, title, count="", right=None, opened=None):
    s = rect(14, y, 212, 30, "#FFFFFF", LINE, 0) + t(24, y + 19, title + (f" ({count})" if count != "" else ""), 10, INK, "khand")
    if right: w = len(right) * 5.8 * .76 + 10; s += tag(192 - w, y + 10, right, TERRA)
    s += ic("down", 200, y + 7, 16, INK, 2); h = 36
    if opened:
        g, hh = opened(y + 30); s += g; h = 30 + hh + 6
    return s, h
def divider(y): return f'<line x1="14" y1="{y+6}" x2="226" y2="{y+6}" stroke="{DIV}"/>', 12
def machan(x, y, s=12):
    return (f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{s/2}" fill="{TERRA}"/><circle cx="{x+s/2}" cy="{y+s*.58}" r="{s*.32}" fill="#F6E7D3"/>'
            f'<circle cx="{x+s*.4}" cy="{y+s*.55}" r="{s*.06}" fill="{LAGOON}"/><circle cx="{x+s*.6}" cy="{y+s*.55}" r="{s*.06}" fill="{LAGOON}"/>'
            f'<path d="M{x+s/2} {y} q{s*.12} {-s*.3} {s*.3} {-s*.3}" stroke="{JUNGLE}" stroke-width="1.4" fill="none"/>')
def credit(y, label=""):
    s = machan(80, y + 4) + t(98, y + 14, "Built by Machan", 9, INK, "khand")
    if label: s += t(120, y + 30, label, 7.5, MUTE, anchor="middle")
    return s, 40 if label else 24
def note(y, a, b):
    return rect(14, y, 212, 34, CREAM, "none") + t(22, y + 14, a, 8.5, INK, "khand") + t(22, y + 26, b, 7.5, MUTE), 40
R = lambda f: ("raw",) + f
def header_screen(parts, nt=None):
    blocks = [R(home_btn(10))]; y = 34
    for p in parts:
        g, h = p(y); blocks.append(("raw", g, h)); y += h
    if nt: g, h = note(y + 2, *nt); blocks.append(("raw", g, h + 2))
    return render([("gap", 10)] + blocks)
def footer_screen(parts, nt=None):
    blocks = [("raw", t(14, 22, "Coach Command Center  ·  middle sections", 7.5, FAINT) + rect(14, 30, 212, 70, SOFT, "none"), 104)]; y = 104
    g, h = divider(y); blocks.append(("raw", g, h)); y += h
    for p in parts:
        g, h = p(y); blocks.append(("raw", g, h)); y += h
    if nt: g, h = note(y + 4, *nt); blocks.append(("raw", g, h + 4))
    return render(blocks)

def p_rows(rows):
    def f(y):
        s = ""
        for i, (a, b) in enumerate(rows): s += t(24, y + 14 + i * 16, a, 8, INK, "hind", 500) + t(216, y + 14 + i * 16, b, 7.5, MUTE, "hind", 400, "end")
        return s, len(rows) * 16 + 4
    return f
def headlines(stack):
    def f(y):
        if stack:
            s = ""
            for i, (a, b) in enumerate([("Leads up", "Three new member calls"), ("Late", "Blog draft moved"), ("Done", "Deck counts posted")]):
                yy = y + 6 + i * 30; s += rect(24, yy, 192, 26, "#FFFFFF", LINE) + rect(24, yy, 3, 26, ACC[i]) + t(32, yy + 11, a, 8.5, INK, "khand") + t(32, yy + 21, b, 7.5, MUTE)
            return s, 96
        s = ""
        for i, (a, b) in enumerate([("Leads up", "Three new calls"), ("Late", "Blog draft"), ("Done", "Counts posted")]):
            x = 24 + i * 96; s += rect(x, y + 6, 88, 44, "#FFFFFF", LINE) + rect(x, y + 6, 88, 3, ACC[i]) + t(x + 6, y + 24, a, 8.5, INK, "khand") + t(x + 6, y + 36, b, 7.5, MUTE)
        s += b_dots(y + 54, 3, 0)[0].replace('cx="106"', 'cx="106"')
        return s, 74
    return f

# ---------- deck 1 and 2: rule cleanup (kept picks + new) ----------
def rebuild(did, title, drop, new_pairs, meta_note):
    """In-place rebuild (same deck id, URL and kept options), like the R86 split / R105 retrofit: the kept options already sit in the
    ledger under the unlisted parent deck, so draft_svg.finish's repeat check can't take them; new options get the same check by hand."""
    import glob, datetime as dt
    old = json.load(open(f"decks/{did}.json"))
    kept = [p for p in old["pairs"] if p["category"] not in drop]
    assert len(kept) == len(old["pairs"]) - len(drop), [p["category"] for p in old["pairs"]]
    pairs = kept + new_pairs; assert len(pairs) == 10, len(pairs); guard(pairs, did); assert theme_name_ok(title), title
    led = json.load(open("shown_options.json")); shown = set(led["options"])
    for fp in glob.glob("decks/*.json"):
        for pp in json.load(open(fp)).get("pairs", []):
            for x in "AB": shown.add((pp.get("option" + x) or {}).get("id"))
    ids = [p["option" + x]["id"] for p in new_pairs for x in "AB"]
    assert len(ids) == len(set(ids)) and not [i for i in ids if i in shown], "repeated option ids"
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    for i, p in enumerate(pairs, 1):
        p.update(id=f"{did}-{i:02d}", repeat=False, notes=True, share=True)
        for x in "AB": p["option" + x]["notes"] = True; p["option" + x]["share"] = True
    for p in new_pairs: p["generated"] = "2026-10-17"
    feel, groups = {}, {}
    for p in pairs:
        groups[p["group"]] = groups.get(p["group"], 0) + 1
        for x in "AB": f = p["option" + x]["feeling"]; feel[f] = feel.get(f, 0) + 1
    old.update(previous_title=old["title"], title=title, generated_at=now, status="published", deck_size=10, groups=groups, feeling_counts=feel,
               apps={"Coach": 10}, notes=True, share=True, caption_rule="R105", rebuilt="2026-10-17: " + meta_note,
               rebuilt_sources={"rulebook": "/workspace/ops/brand/dashboard-rulebook.md", "review": "/workspace/ops/brand/dashboard-review-2026-10-17.md",
                                "builder": "tools/build_coach_shelf_rebuild.py"},
               freshness={"option_slots": 20, "never_shown_before": len(ids), "share": round(len(ids) / 20, 2),
                          "note": f"{len(kept)} picks kept from the R86 split (same options), {len(new_pairs)} new"})
    old["pairs"] = pairs
    json.dump(old, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    for i in ids: led["options"][i] = [did]
    led["options"] = dict(sorted(led["options"].items())); led["shown_count"] = len(led["options"]); led["updated"] = now
    json.dump(led, open("shown_options.json", "w"), indent=1, ensure_ascii=False)
    print(did, title, [p["category"] for p in pairs])

A_ID = "rule-cleanup-rule-cleanup-deck-love-button-sticky-header"
pa, O, add = deck("bkco_rc1017a_", "Coach")
add("Rule Cleanup", "Repeated Numbers",
    O("01a", "Give It A New Number", "The Apps Home button rule moves to the next free number.", "focused",
      doc("Dashboard Rulebook", "Rules in force, newest last", [("R76", "Branded header and footer"), ("R77", "Requested Decks section"), ("R120", "Apps Home button", JUNGLE, "NEW NUMBER", JUNGLE), ("R78", "Compact Routines")], ("One number, one rule", JUNGLE, "check"))),
    O("01b", "Keep It With A Letter", "It stays next to its twin as R77b.", "calm",
      doc("Dashboard Rulebook", "Rules in force, newest last", [("R76", "Branded header and footer"), ("R77", "Requested Decks section"), ("R77b", "Apps Home button", LAGOON, "LETTER", LAGOON), ("R78", "Compact Routines")], ("Old links to R77 still work", LAGOON, "check"))),
    "Dashboard Rulebook: Repeated rule numbers, two different rules are both called R77 so should the second one get a new number or keep R77 with a letter?")
add("Rule Cleanup", "Relayed Rules",
    O("02a", "In Force On Relay", "A rule passed on by Grok Bot, Legal or UpKeep counts the moment it arrives.", "focused",
      doc("Dashboard Rulebook", "Rules passed on by other agents", [("R110", "via Legal and Grok Bot", INK, "IN FORCE", JUNGLE), ("R118", "via UpKeep", INK, "IN FORCE", JUNGLE), ("R119", "via Security", INK, "IN FORCE", JUNGLE)], ("Agents act on it straight away", JUNGLE, "check"))),
    O("02b", "Wait For Max's Okay", "It is written down but waits for one tap from Max before it counts.", "calm",
      doc("Dashboard Rulebook", "Rules passed on by other agents", [("R110", "via Legal and Grok Bot", INK, "WAITING", SAFFRON), ("R118", "via UpKeep", INK, "WAITING", SAFFRON), ("R119", "via Security", INK, "WAITING", SAFFRON)], ("Max confirms each one once", SAFFRON, "clock"))),
    "Dashboard Rulebook: Relayed rules, should a rule another agent passes on count right away or wait until Max confirms it?")
add("Rule Cleanup", "Staged Rules",
    O("03a", "With The Rest, Tagged", "Staged rules stay in number order with a Staged tag.", "calm",
      doc("Dashboard Rulebook", "All rules, in number order", [("R105", "Card caption rule"), ("R106", "Branded header order", INK, "STAGED", SAFFRON), ("R107", "Refresh deck"), ("R109", "Quick note", INK, "STAGED", SAFFRON)])),
    O("03b", "Own Staged List", "Rules waiting on Security move to a Staged list at the end.", "focused",
      doc("Dashboard Rulebook", "In force", [("R105", "Card caption rule"), ("R107", "Refresh deck")], ("Staged: R106 header order, R109 note", SAFFRON, "clock"))),
    "Dashboard Rulebook: Staged rules, should rules that wait on Security sit in number order with a Staged tag or move to their own list?")
add("Rule Cleanup", "Lost Early Rules",
    O("04a", "Rebuild From Results", "Branding rebuilds R1 to R65 from old deck results and commits.", "focused",
      doc("Dashboard Rulebook", "Early rules lost in the Oct 16 restore", [("R1", "Rebuilt from deck results", INK, "CHECK", LAGOON), ("R12", "Rebuilt from deck results", INK, "CHECK", LAGOON), ("R64", "Skipped cards come back", INK, "KEPT", JUNGLE)], ("Max checks each rebuilt rule", LAGOON, "search"))),
    O("04b", "Start From Today", "Drop the missing numbers; today's rules are the full list.", "calm",
      doc("Dashboard Rulebook", "Early rules lost in the Oct 16 restore", [("R1", "Not rebuilt", FAINT, "", TERRA, True), ("R12", "Not rebuilt", FAINT, "", TERRA, True), ("R66", "Ready Deck Shelf", INK, "IN FORCE", JUNGLE)], ("Only what the team does now counts", JUNGLE, "check"))),
    "Dashboard Rulebook: Lost early rules, should the missing R1 to R65 be rebuilt from old deck results or left out with today's rules as the full list?")
rebuild(A_ID, "Rule Cleanup: Names, Labels & Sources", {"Love Button", "Sticky Header", "Locked Pages Rule", "Shelf Cap"}, pa,
        "dropped Love Button (R82/R89 keep Love), Sticky Header (R87), Locked Pages Rule (R119) and Shelf Cap (R86/R97); added Repeated Numbers, Relayed Rules, Staged Rules, Lost Early Rules")

B_ID = "rule-cleanup-rule-cleanup-deck-questionnaire-size"
pb, O, add = deck("bkco_rc1017b_", "Coach")
add("Rule Cleanup", "Rulebook Copy",
    O("01a", "Commit A Copy", "Every rulebook change is also committed to the Branding repo.", "focused",
      doc("Branding Repo", "rules/dashboard-rulebook.md", [("Oct 17", "R119 cleanup permission", INK, "SAVED", JUNGLE), ("Oct 17", "R118 Extras ideas", INK, "SAVED", JUNGLE), ("Oct 17", "R117 UpKeep video", INK, "SAVED", JUNGLE)], ("A restore can never lose it again", JUNGLE, "check"))),
    O("01b", "Box Only (As Now)", "The rulebook lives only on the shared box, as it does now.", "calm",
      doc("Shared Box", "ops/brand/dashboard-rulebook.md", [("Oct 16", "Rebuilt after the box restore", INK, "ONE COPY", SAFFRON), ("R1", "Early rules not recovered", FAINT, "", TERRA, True)], ("One file, nothing to keep in step", SAFFRON, "clock"))),
    "Dashboard Rulebook: Safe copy, should every rulebook change also be committed to the Branding repo or should it stay only on the shared box?")
rebuild(B_ID, "Rule Cleanup: Files, Copies & Retests", {"Questionnaire Size"}, pb,
        "dropped Questionnaire Size ('must be 20', settled by R86 10 picks and R87 questions one at a time in chat); added Rulebook Copy")

# ---------- deck 3: Header And Footer Details (replaces Dashboard Layout Deck) ----------
C_ID = "dashboard-layout-header-and-footer-details"; C_NAME = "Header And Footer Details"; OLD_C = "dashboard-layout-dashboard-layout-deck"
pc, O, add = deck("bkhf_", "Coach")
G = "Header And Footer"
add(G, "Long Board Names",
    O("01a", "Wrap To Two Lines", "The full name wraps at the same size.", "calm",
      header_screen([lambda y: cc(y, "", ["Video And Photo Studio", "Command Center"])], ("Same size on every board", "Two lines at most on a 393 phone"))),
    O("01b", "Shrink To One Line", "The name gets smaller until it fits one line.", "focused",
      header_screen([lambda y: cc(y, "Video And Photo Studio Command Center", None, 9.5)], ("One line on every board", "Long names use smaller type"))),
    "Agent Board Header: Long board names, on a phone should a long Command Center name wrap to a second line or shrink to fit on one?")
add(G, "Deck Counter Wording",
    O("02a", "Today And All Time", "Two numbers: decks done today and all time.", "focused",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y), lambda y: counter(y, "2 decks today  ·  41 all time")], ("Shows today's pace", "Finished decks keep counting (R96)"))),
    O("02b", "One All-Time Total", "Just the total number of decks finished.", "calm",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y), lambda y: counter(y, "41 decks done")], ("One plain number", "Finished decks keep counting (R96)"))),
    "Agent Board Header: Deck counter, should it read decks done today and all time or one all-time total?")
add(G, "Deck Counter Tap",
    O("03a", "Opens Deck Building", "Tapping the counter opens the Deck Building page.", "focused",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y), lambda y: counter(y, "41 decks done", True)], ("A link to every deck and result", "Same tab, Return brings you back"))),
    O("03b", "Just A Number", "The counter is plain text and does nothing when tapped.", "calm",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y), lambda y: counter(y, "41 decks done")], ("Nothing to tap by mistake", "Deck Building stays on its own board"))),
    "Agent Board Header: Deck counter tap, should tapping the counter open the Deck Building page or stay plain text?")
add(G, "Open Shelf Slots",
    O("04a", "Show Fewer Decks", "The shelf simply ends after the last ready deck.", "calm",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y, ("Rule Cleanup", "Team Ideas"))], ("Two decks, nothing else", "The queue is empty"))),
    O("04b", "Ask For A Deck Card", "A last dashed card lets Max ask for a new deck.", "playful",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: shelf(y, ("Rule Cleanup", "Team Ideas"), True)], ("A dashed card fills the gap", "Tap it to ask Branding for a deck"))),
    "Agent Board Header: Open shelf slots, when the ready queue is empty should the shelf just show fewer decks or end with an Ask For A Deck card?")
add(G, "Late Tag Spot",
    O("05a", "On The Closed Row", "The Late tag shows on the Morning Report row while it is closed.", "focused",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: counter(y, "41 decks done"), lambda y: fold(y, "Morning Report", 3, "LATE 12 MIN")], ("Seen without opening it", "Fold stays closed by default"))),
    O("05b", "Inside Only", "The row stays clean; the tag shows once it is opened.", "calm",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: counter(y, "41 decks done"), lambda y: fold(y, "Morning Report", 3)], ("Same row on every board", "Late tag waits inside"))),
    "Agent Board Header: Late tag, should the Late N min tag show on the closed Morning Report row or only once it is opened?")
add(G, "Before It Posts",
    O("06a", "Yesterday, Tagged", "Yesterday's report stays, with a small Yesterday tag.", "calm",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: fold(y, "Morning Report", 3, "YESTERDAY", p_rows([("Leads up", "Fri"), ("Blog draft moved", "Fri"), ("Deck counts posted", "Fri")]))], ("Something to read at any hour", "Replaced at 4:47 AM"))),
    O("06b", "Posts At 4:47 AM", "One short line says when today's report arrives.", "focused",
      header_screen([lambda y: cc(y, "Coach Command Center"), lambda y: fold(y, "Morning Report", 0, None, p_rows([("Today's report posts at 4:47 AM", "")]))], ("Never shows old news", "One line until it posts"))),
    "Agent Board Header: Morning Report before it posts, should the fold show yesterday's report with a Yesterday tag or one line saying when today's arrives?")
add(G, "Headlines On A Phone",
    O("07a", "Stacked", "The three headline cards sit one under another.", "calm",
      header_screen([lambda y: fold(y, "Morning Report", 3, None, headlines(True))], ("All three seen at once", "Taller fold"))),
    O("07b", "One Swipe Row", "The three cards sit side by side and swipe.", "playful",
      header_screen([lambda y: fold(y, "Morning Report", 3, None, headlines(False))], ("Shorter fold", "Swipe for the next headline"))),
    "Agent Board Header: Morning Report headlines, on a phone should the three headline cards stack or sit in one swipe row?")
add(G, "No Routines Yet",
    O("08a", "Hide The Section", "A board with no routines shows no Routines fold at all.", "calm",
      footer_screen([credit], ("Footer is just the credit", "Routines appear once one exists"))),
    O("08b", "Routines (0) With A Line", "The closed fold shows a zero and one line inside.", "focused",
      footer_screen([lambda y: fold(y, "Routines", 0, None, p_rows([("No routines yet", "")])), credit], ("Same footer on every board", "Says plainly there are none"))),
    "Agent Board Footer: Boards with no routines, should the Routines fold be hidden or show Routines (0) with one plain line?")
add(G, "Single Group Label",
    O("09a", "Keep The Label", "Daily And Beyond shows even when it is the only group.", "calm",
      footer_screen([lambda y: fold(y, "Routines", 2, None, p_rows([("DAILY AND BEYOND", ""), ("Morning Report", "4:47 AM Daily"), ("Weekly review", "9:17 AM Thu")])), credit], ("Same look as boards with two groups", ""))),
    O("09b", "Hide It", "With one group the rows start straight away.", "focused",
      footer_screen([lambda y: fold(y, "Routines", 2, None, p_rows([("Morning Report", "4:47 AM Daily"), ("Weekly review", "9:17 AM Thu")])), credit], ("One line shorter", "Label shows again with two groups"))),
    "Agent Board Footer: Routine group label, when a board has only one group should the Daily And Beyond label still show or be hidden?")
add(G, "Credit Link Tab",
    O("10a", "Same Tab", "Built by Machan opens maxweberman.com in the same tab.", "calm",
      footer_screen([lambda y: fold(y, "Routines", 4), lambda y: credit(y, "Opens here; Back returns to the board")], ("Like every other board link", "R104 Back brings you home"))),
    O("10b", "New Tab", "Built by Machan opens maxweberman.com in a new tab.", "focused",
      footer_screen([lambda y: fold(y, "Routines", 4), lambda y: credit(y, "Opens in a new tab; the board stays open")], ("The board never leaves the screen", "Close the tab to come back"))),
    "Agent Board Footer: Built by Machan link, should maxweberman.com open in the same tab or in a new tab?")
assert len(pc) == 10 and theme_name_ok(C_NAME); guard(pc, C_ID)
txt = json.dumps(pa + pb + pc).lower()
assert "thai" not in txt and "share placement" not in txt
assert not re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", json.dumps(pa + pb + pc, ensure_ascii=False)), "emoji"
order = [p["ask"] for p in pc]
publish(C_ID, C_NAME, "Coach", pc, {"brands": ["Open questions on the branded header (Command Center header, decks and counter, Morning Report fold) and branded footer (Routines, Built by Machan) that no rule settles yet. Share placement is left out (waiting on Max). Nothing from Main Dashboard Rules or All Boards Rules.",
        "Max's standard look: white and light beige, Khand and Hind, light mode only."],
        "submit_agent": "coach", "topic": "dashboard-layout", "shelf": True, "deck_size": 10, "board": "coach", "caption_rule": "R105",
        "replaces": OLD_C, "request": "Coach via Grok Bot, Oct 17 2026: retire or rebuild Dashboard Layout Deck around the current branded header and footer; keep Share placement out.",
        "sources": {"rulebook": "/workspace/ops/brand/dashboard-rulebook.md (R72, R76, R79, R85, R87, R96, R97, R104, R106)", "review": "/workspace/ops/brand/dashboard-review-2026-10-17.md (S20; S1-S18 left to the open decks)", "builder": "tools/build_coach_shelf_rebuild.py"}}, seed=10178, n=10, first=0)
dj = json.load(open(f"decks/{C_ID}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{C_ID}-{i:02d}"
json.dump(dj, open(f"decks/{C_ID}.json", "w"), indent=1, ensure_ascii=False)
# retire the old 20-pick deck (normal path: unlisted + status retired + replaced_by; file, page and ledger kept)
od = json.load(open(f"decks/{OLD_C}.json"))
od.update(unlisted=True, status="retired", shelf=False, replaced_by=C_ID, retired_at="2026-10-17",
          retired_note="R86 10 picks + most cards asked about sections removed Oct 16 (Brand Guide Summary, Recent Work, Stat Strip, Layout Standards, Apps); replaced by Header And Footer Details. No results were submitted.")
json.dump(od, open(f"decks/{OLD_C}.json", "w"), indent=1, ensure_ascii=False)
led = json.load(open("shown_options.json")); json.dump(led, open("shown_options.json", "w"), indent=1, ensure_ascii=False)
from write_sizes import main as write_sizes; write_sizes()
from ready_shelf import write_page
print("page", write_page(C_ID))
