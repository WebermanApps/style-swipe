"""Team Improvement Deck, round four (Branding, Oct 17 2026 21:xx ICT). 10 picks (R86/R88), team-wide workflow + deck/dashboard look.
Follow-ups to round three (R112-R116 applied): feed line format, skip handling, Your Picks summary, New badge, notes, swipe hints,
progress, deck thumbnails, status colours, done confirmations. Not asked: font comparison (skipped twice, dropped), saving results
(on hold until Max answers 'Which is safer?'), dashboard layout (R83). No UpKeep/Thai pairing (R110). R105 captions.
Each pair: (group, ask, A, B); option = (label, desc, fact1, fact2, drawing kind)."""
def P(g, ask, a, b): return (g, ask, a, b)
NAME = "Team Improvement Deck"
ABOUT = "Broad improvements to how the Grok Bot team works: round four, team workflow and the deck and board look"
ROUND = "four"; PREV = "team-improvement-deck-round-three"; PREFIX = "teamimp4_"
SOURCES = ("Round three results (R112-R116, Oct 17 2026 20:52 ICT) follow-ups + Brand scan 2026-10-16 look notes; "
           "01 fonts dropped, 06 saving results on hold, 02/10 not re-asked this round")
CSS = ".card,.opt,.vis{border-radius:10px!important}"  # R89 + R116: 10px deck cards, round vote buttons come from the template
PAIRS = [
P("Workflow", "Team Feed: Handoff line, plain words only or a small from-to tag with the two agent names?",
  ("Plain Words", "One sentence: who passed what to whom, plus the link.", "Quiet", "Reads fast", "feed_plain"),
  ("From-To Tag", "Two small agent tags with an arrow, then the line.", "Scannable", "Clear owners", "feed_tag")),
P("Workflow", "Team Workflow: Skipped picks, re-ask them as they are next round or have the agent reword them first?",
  ("Re-Ask As Is", "The same card comes back in the next round.", "Simple", "No delay", "skip_same"),
  ("Reword First", "The agent rewrites the card before it comes back.", "Clearer", "Fewer skips", "skip_reword")),
P("Workflow", "Team Workflow: Done confirmation, one line in chat or a short Done card on the agent board?",
  ("Line In Chat", "The agent replies with one line when the job is done.", "Fast", "In the thread", "done_chat"),
  ("Done Card On Board", "A small Done card with what changed and a link.", "Easy to find", "Lasting", "done_card")),
P("Deck Look", "Deck Page: Progress, a thin bar along the top or ten small dots that fill in?",
  ("Thin Bar", "One slim green bar that grows as you answer.", "Calm", "Minimal", "prog_bar"),
  ("Ten Dots", "One dot per pick, filled when answered.", "Exact", "Shows skips", "prog_dots")),
P("Deck Look", "Deck Page: Swipe hint, arrows on the first card only or a small hint line on every card?",
  ("First Card Only", "Left and right arrows show once, then go away.", "Clean", "Learn once", "hint_first"),
  ("Hint Line Every Card", "A short line under each card: left This, right That.", "Always there", "No guessing", "hint_line")),
P("Deck Look", "Deck Page: Your Picks summary, picture tiles for each pick or a short text list?",
  ("Picture Tiles", "A grid of the chosen pictures with their labels.", "Visual", "Easy recall", "sum_tiles"),
  ("Short Text List", "One line per pick: question and choice.", "Compact", "Quick to scan", "sum_list")),
P("Deck Look", "Deck Page: Notes, a pencil button on each card or a note box always open under the card?",
  ("Pencil Button", "Tap the pencil to open a note box when needed.", "Tidy", "Optional", "note_btn"),
  ("Always Open Box", "A short note box sits under every card.", "Inviting", "One tap less", "note_box")),
P("Board Look", "Branding Board: New badge, a small green pill or a single green dot on the deck card?",
  ("Green Pill", "A small rounded pill that says New.", "Clear", "Readable", "new_pill"),
  ("Green Dot", "A single dot in the corner, no word.", "Subtle", "Quiet", "new_dot")),
P("Board Look", "Deck Building Page: Deck card picture, the first pick's mockup or a plain colour block per agent?",
  ("First Pick Mockup", "The card shows a small picture from the deck.", "Preview", "Inviting", "thumb_pick"),
  ("Agent Colour Block", "A flat block in the agent's colour with its icon.", "Consistent", "Calm", "thumb_color")),
P("Board Look", "Agent Boards: Status colours, green amber red dots or one accent colour with a word?",
  ("Green Amber Red", "Traffic-light dots for on track, waiting and stuck.", "At a glance", "Familiar", "stat_traffic"),
  ("Accent + Word", "One brand colour and a short word like Waiting.", "On brand", "Calmer", "stat_word")),
]
assert len(PAIRS) == 10

def EXTRA_THUMBS(k, a, h):
    rect, t, X, Y, W, H, INK, MUTE, LINE, BEI, W_, card = (h[x] for x in ("rect", "t", "X", "Y", "W", "H", "INK", "MUTE", "LINE", "BEI", "W_", "card"))
    cx = X + W / 2; G = "#0B6E4F"
    def chip(x, y, w, txt, fill=W_, col=INK, r=10): return rect(x, y, w, 20, fill, INK, r) + t(x + w / 2, y + 14, txt, 8.5, col, "hind", 700, "middle")
    def phone(inner):  # small deck page frame
        return rect(X, Y, W, H, BEI, LINE) + rect(cx - 52, Y + 4, 104, H - 8, W_, INK, 10) + inner
    def mini(y, hh=40):  # a 10px deck card with picture
        return rect(cx - 44, y, 88, hh, W_, LINE, 10) + rect(cx - 38, y + 6, 76, hh - 18, a, "none", 6)
    if k in ("feed_plain", "feed_tag"):
        s = rect(X, Y, W, H, W_, LINE) + t(X + 12, Y + 18, "TEAM FEED", 8, a, "hind", 700)
        for i in range(3):
            y = Y + 28 + i * 24; s += rect(X + 10, y, W - 20, 20, BEI, LINE)
            if k == "feed_plain": s += t(X + 16, y + 14, ["Blog passed the bids post to Build", "Coach passed 3 ideas to Branding", "Security passed a fix to Branding"][i], 8.5, INK)
            else:
                s += chip(X + 14, y, 40, ["Blog", "Coach", "Security"][i], W_, INK) + t(X + 62, y + 14, "\u2192", 10, a, "hind", 700) + chip(X + 72, y, 46, ["Build", "Branding", "Branding"][i], a, W_)
                s += t(X + 124, y + 14, ["bids post", "3 ideas", "kit fix"][i], 8.5, MUTE)
        return s
    if k in ("skip_same", "skip_reword"):
        s = rect(X, Y, W, H, BEI, LINE) + card(X + 10, Y + 14, 84, 66, W_, INK, 10) + t(X + 52, Y + 34, "SKIPPED", 8, MUTE, "hind", 700, "middle") + t(X + 52, Y + 54, "Old wording", 9, INK, "hind", 600, "middle")
        s += f'<polygon points="{X+100},{Y+44} {X+112},{Y+48} {X+100},{Y+52}" fill="{a}"/>' + card(X + 118, Y + 14, 80, 66, W_, a, 10) + t(X + 158, Y + 34, "NEXT ROUND", 8, a, "hind", 700, "middle")
        s += t(X + 158, Y + 54, "Old wording" if k == "skip_same" else "New wording", 9, INK, "hind", 600, "middle")
        if k == "skip_reword": s += rect(X + 126, Y + 60, 64, 4, a)
        return s
    if k == "done_chat":
        return rect(X, Y, W, H, W_, LINE) + rect(X + 12, Y + 12, 120, 22, BEI, LINE, 10) + t(X + 20, Y + 27, "Max: please fix the deck", 8.5, INK) + rect(X + 70, Y + 44, 126, 22, G, "none", 10) + t(X + 78, Y + 59, "Done: deck fixed, link", 8.5, W_, "hind", 600)
    if k == "done_card":
        return rect(X, Y, W, H, BEI, LINE) + rect(X + 20, Y + 10, W - 40, H - 20, W_, INK, 10) + chip(X + 30, Y + 18, 44, "DONE", G, W_) + t(X + 30, Y + 56, "Deck fixed", 13, INK, "khand", 700) + t(X + 30, Y + 72, "Round buttons, cream band", 8.5, MUTE) + t(X + 30, Y + 86, "Open link", 8.5, a, "hind", 700)
    if k in ("prog_bar", "prog_dots"):
        s = phone("")
        if k == "prog_bar": s += rect(cx - 44, Y + 12, 88, 4, LINE, "none", 2) + rect(cx - 44, Y + 12, 52, 4, G, "none", 2)
        else: s += "".join(f'<circle cx="{cx-40+i*8.9:.1f}" cy="{Y+14}" r="3" fill="{G if i<6 else W_}" stroke="{G if i<6 else LINE}"/>' for i in range(10))
        return s + mini(Y + 24, 52) + chip(cx - 44, Y + 80, 40, "THIS") + chip(cx + 4, Y + 80, 40, "THAT")
    if k in ("hint_first", "hint_line"):
        s = phone(mini(Y + 12, 56))
        if k == "hint_first": s += t(cx - 50, Y + 46, "\u2190", 18, a, "hind", 700) + t(cx + 38, Y + 46, "\u2192", 18, a, "hind", 700) + t(cx, Y + 82, "first card only", 8, MUTE, "hind", 400, "middle")
        else: s += t(cx, Y + 80, "\u2190 This   That \u2192", 8.5, INK, "hind", 600, "middle") + rect(cx - 30, Y + 86, 60, 3, a)
        return s
    if k == "sum_tiles":
        s = rect(X, Y, W, H, W_, LINE) + t(X + 12, Y + 18, "Your Picks (6)", 11, INK, "khand", 700)
        for i in range(6):
            x = X + 12 + (i % 3) * 64; y = Y + 26 + (i // 3) * 38; s += rect(x, y, 58, 34, W_, LINE, 8) + rect(x + 4, y + 4, 50, 18, a if i % 2 == 0 else LINE, "none", 4) + rect(x + 4, y + 26, 34, 4, INK)
        return s
    if k == "sum_list":
        s = rect(X, Y, W, H, W_, LINE) + t(X + 12, Y + 18, "Your Picks (6)", 11, INK, "khand", 700)
        for i in range(6): y = Y + 30 + i * 12; s += rect(X + 12, y, 90 - (i % 3) * 14, 4, MUTE) + rect(X + 140, y, 44, 4, a)
        return s
    if k in ("note_btn", "note_box"):
        s = phone(mini(Y + 10, 44))
        if k == "note_btn": s += rect(cx + 18, Y + 58, 26, 20, W_, INK, 10) + f'<path d="M{cx+25},{Y+74} l2,-6 l8,-8 l4,4 l-8,8 z" fill="none" stroke="{INK}" stroke-width="1.5"/>' + t(cx - 44, Y + 72, "Add Note", 8.5, MUTE)
        else: s += rect(cx - 44, Y + 58, 88, 30, W_, INK, 6) + t(cx - 38, Y + 72, "Note (optional)", 8, MUTE)
        return s
    if k in ("new_pill", "new_dot"):
        s = rect(X, Y, W, H, BEI, LINE)
        for i in range(2):
            x = X + 14 + i * 98; s += rect(x, Y + 12, 84, 80, W_, INK, 10) + rect(x + 8, Y + 20, 68, 36, a if i == 0 else LINE, "none", 6) + rect(x + 8, Y + 64, 52, 6, INK) + rect(x + 8, Y + 76, 36, 4, MUTE)
            if i == 0: s += (rect(x + 46, Y + 16, 34, 16, G, "none", 8) + t(x + 63, Y + 27, "NEW", 8, W_, "hind", 700, "middle")) if k == "new_pill" else f'<circle cx="{x+74}" cy="{Y+20}" r="5" fill="{G}"/>'
        return s
    if k in ("thumb_pick", "thumb_color"):
        s = rect(X, Y, W, H, W_, LINE)
        for i, col in enumerate([a, "#05668D", "#C1502E"]):
            x = X + 10 + i * 66; s += rect(x, Y + 10, 58, 84, W_, INK, 10)
            if k == "thumb_pick": s += rect(x + 5, Y + 15, 48, 40, BEI, LINE, 6) + rect(x + 10, Y + 20, 18, 30, col, "none", 3) + rect(x + 30, Y + 20, 18, 30, LINE, "none", 3)
            else: s += rect(x + 5, Y + 15, 48, 40, col, "none", 6) + f'<circle cx="{x+29}" cy="{Y+35}" r="9" fill="{W_}"/>'
            s += rect(x + 6, Y + 64, 40, 5, INK) + rect(x + 6, Y + 76, 28, 4, MUTE)
        return s
    if k in ("stat_traffic", "stat_word"):
        s = rect(X, Y, W, H, W_, LINE)
        for i, (nm, c, w) in enumerate([("Blog", G, "On track"), ("Coach", "#D9A21B", "Waiting"), ("Build", "#B5373A", "Stuck")]):
            y = Y + 12 + i * 28; s += rect(X + 10, y, W - 20, 24, BEI, LINE, 8) + t(X + 34, y + 16, nm, 10, INK, "khand", 700)
            if k == "stat_traffic": s += f'<circle cx="{X+22}" cy="{y+12}" r="5" fill="{c}"/>'
            else: s += f'<circle cx="{X+22}" cy="{y+12}" r="5" fill="{a}"/>' + t(X + W - 18, y + 16, w, 9, a, "hind", 700, "end")
        return s
    return None
