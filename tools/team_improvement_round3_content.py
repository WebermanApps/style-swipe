"""Team Improvement Deck, round three (Branding, Oct 17 2026). 10 picks (R86/R88).
Sources: Brand scan 2026-10-16 items 6, 10, 11 (left over from round two); round-one cards that were never published
(14 Handoffs, 19 Saving Work; 03 Team View left out: dashboard layout, R83); the round-two skip (Font Questions) re-asked reworded;
and follow-ups that Max's round-two picks opened (split naming, button corners, caption band, mockup style).
No dashboard-layout questions (R83). Copy follows R89: short title + one-line description.
Each pair: (group, ask, A, B); option = (label, desc, fact1, fact2, drawing kind)."""
def P(g, ask, a, b): return (g, ask, a, b)
NAME = "Team Improvement Deck"
ABOUT = "Broad improvements to how the Grok Bot team works: round three, the last brand-scan items, two never-asked team questions and follow-ups to round two"
ROUND = "three"; PREV = "team-improvement-deck-deck-look-round"; PREFIX = "teamimp3_"
SOURCES = ("ops/team-sync/handoffs/team-improvement-sources-2026-10-16.md (Brand scan items 6, 10, 11; round-one unpublished cards 14, 19) "
           "+ round-two skip re-asked (Font Questions) + round-two follow-ups (R89)")
CSS = "*{border-radius:0!important}.card,.opt,.vis{border-radius:10px!important}"  # R89: deck cards 10px, rest square
PAIRS = [
P("Decks", "Comparing Fonts, Asked Again: Draw The Mockup In The Font Itself Or Keep House Fonts With A Label?",
  ("Draw In The Font", "The picture is set in the font being compared.", "True look", "Exact", "font_real"),
  ("House Fonts + Label", "Khand and Hind in the picture, font name below.", "Consistent", "Simpler", "font_named")),
P("Decks", "Numbered Decks (Thai Ready 1-4 And 55 More): Rename By Theme Or Keep Numbers Hidden In The Link?",
  ("Rename By Theme", "New theme names in titles and links; old links redirect.", "Clear links", "One-time work", "names_rename")
  , ("Keep Numbers Hidden", "Titles stay descriptive; numbers only in the link.", "No churn", "Links stay", "names_hidden")),
P("Decks", "Standalone Decks Like Inbox Keep-Or-Delete: Shared Pair Layout Or Their Own Keep/Delete Cards?",
  ("Shared Pair Layout", "Same this-or-that layout and buttons as every deck.", "One way", "Same counts", "standalone_pair"),
  ("Own Keep/Delete Cards", "One card at a time with Keep and Delete buttons.", "Fast triage", "Fits inbox", "standalone_single")),
P("Decks", "Audio Cards In Video Decks: Mix Them Into The Video Decks Or Give Audio Its Own Deck?",
  ("Mix Into Video Decks", "Music and voice cards sit between the video cards.", "One deck", "In context", "audio_mix"),
  ("Own Audio Deck", "A separate deck for music, voice and sound picks.", "Focused", "Easy to compare", "audio_own")),
P("Team", "Handoffs Between Agents: Done Quietly Or One Line In The Team Feed?",
  ("Done Quietly", "Agents pass work along without posting anything.", "Less noise", "Calm", "handoff_silent"),
  ("One Line In The Feed", "Each handoff adds one short line to the Team Feed.", "Traceable", "Easy to check", "handoff_feed")),
P("Team", "Saving Results: Push To GitHub Right Away Or Also Keep A Daily Dropbox Copy?",
  ("Push Right Away", "Results go to GitHub as soon as they are applied.", "Simple", "One place", "save_push"),
  ("Also Daily Dropbox", "Push right away, plus one Dropbox copy each day.", "Extra backup", "Safer", "save_dropbox")),
P("Decks", "Splitting Big Decks Into 10s: Name Each Part By Its Theme Or Keep One Name With Part One, Part Two?",
  ("Name By Theme", "Each part named for what is in it.", "Clear", "Easy to find", "split_theme"),
  ("Part One, Part Two", "Same deck name, parts in order.", "Keeps the set", "Simple", "split_part")),
P("Deck Look", "With 10px Deck Cards: Round The Vote Buttons Too Or Keep The Buttons Square?",
  ("Round Buttons Too", "Vote buttons get the same soft 10px corners.", "Matches cards", "Soft", "btn_round"),
  ("Keep Buttons Square", "Cards soft, buttons stay sharp and square.", "Crisp", "Matches boards", "btn_square")),
P("Deck Look", "Caption Panel Under Deck Pictures On A White Page: Light Cream Band Or White With A Thin Line?",
  ("Light Cream Band", "Caption sits on a small cream band under the picture.", "Warm", "Sets it apart", "cap_cream"),
  ("White With A Line", "All white, a thin grey line above the caption.", "Clean", "Crisp", "cap_white")),
P("Deck Look", "Drawn Mockups For Text Topics: Brand Colour Drawings Or Grey Sketch Lines?",
  ("Brand Colour", "Small drawings in terracotta, lagoon and jungle.", "Lively", "On brand", "mock_color"),
  ("Grey Sketch", "Simple grey line drawings, colour only on the pick.", "Calm", "Quiet", "mock_grey")),
]
assert len(PAIRS) == 10

def EXTRA_THUMBS(k, a, h):
    rect, t, X, Y, W, H, INK, MUTE, LINE, BEI, W_, card = (h[x] for x in ("rect", "t", "X", "Y", "W", "H", "INK", "MUTE", "LINE", "BEI", "W_", "card"))
    cx = X + W / 2
    def chip(x, y, w, txt, fill=W_, col=INK, r=0): return rect(x, y, w, 20, fill, INK, r) + t(x + w / 2, y + 14, txt, 8.5, col, "hind", 700, "middle")
    if k in ("names_rename", "names_hidden"):
        s = rect(X, Y, W, H, W_, LINE)
        if k == "names_rename":
            s += t(X + 14, Y + 26, "thai-ready-1", 10, MUTE, "hind", 400) + f'<line x1="{X+14}" y1="{Y+23}" x2="{X+80}" y2="{Y+23}" stroke="{a}" stroke-width="2"/>'
            s += t(X + 14, Y + 46, "thai-tones-and-greetings", 10, INK, "hind", 700) + rect(X + 14, Y + 58, W - 28, 30, BEI, LINE) + t(X + 22, Y + 78, "Tones And Greetings", 13, INK, "khand", 700)
        else:
            s += t(X + 14, Y + 26, "link: thai-ready-1", 10, MUTE, "hind", 400) + rect(X + 14, Y + 40, W - 28, 44, BEI, LINE) + t(X + 22, Y + 68, "Tones And Greetings", 15, INK, "khand", 700) + rect(X + 14, Y + 90, 60, 4, a)
        return s
    if k == "standalone_pair":
        return rect(X, Y, W, H, BEI, LINE) + card(X + 12, Y + 8, 88, 62) + card(X + 108, Y + 8, 88, 62) + rect(X + 18, Y + 14, 76, 24, a) + rect(X + 114, Y + 14, 76, 24, LINE) + "".join(chip(X + 10 + i * 48, Y + 78, 44, l) for i, l in enumerate(["THIS", "BOTH", "THAT", "SKIP"]))
    if k == "standalone_single":
        return rect(X, Y, W, H, BEI, LINE) + card(cx - 60, Y + 8, 120, 62) + t(cx - 50, Y + 26, "From: Newsletter", 9, MUTE) + rect(cx - 50, Y + 34, 100, 6, INK) + rect(cx - 50, Y + 46, 80, 5, LINE) + chip(cx - 60, Y + 78, 56, "KEEP", W_) + chip(cx + 4, Y + 78, 56, "DELETE", a, W_)
    if k in ("audio_mix", "audio_own"):
        s = rect(X, Y, W, H, BEI, LINE)
        def film(x): return card(x, Y + 16, 40, 52, W_, INK) + rect(x + 6, Y + 22, 28, 22, LINE) + f'<polygon points="{x+16},{Y+28} {x+26},{Y+33} {x+16},{Y+38}" fill="{INK}"/>'
        def note(x, c): return card(x, Y + 16, 40, 52, W_, c) + f'<circle cx="{x+16}" cy="{Y+50}" r="5" fill="{c}"/><rect x="{x+20}" y="{Y+26}" width="2.5" height="24" fill="{c}"/>'
        if k == "audio_mix": return s + film(X + 10) + note(X + 60, a) + film(X + 110) + note(X + 160, a) + t(cx, Y + 90, "Video Deck", 11, INK, "khand", 700, "middle")
        return s + film(X + 14) + film(X + 58) + rect(cx, Y + 10, 1, 84, LINE) + note(X + 120, a) + note(X + 164, a) + t(X + 56, Y + 90, "Video", 11, INK, "khand", 700, "middle") + t(X + 162, Y + 90, "Audio", 11, INK, "khand", 700, "middle")
    if k in ("handoff_silent", "handoff_feed"):
        s = rect(X, Y, W, H, W_, LINE) + card(X + 12, Y + 12, 52, 30, BEI, INK) + t(X + 38, Y + 31, "Blog", 10, INK, "khand", 700, "middle") + card(X + 144, Y + 12, 52, 30, BEI, INK) + t(X + 170, Y + 31, "Build", 10, INK, "khand", 700, "middle")
        s += f'<line x1="{X+68}" y1="{Y+27}" x2="{X+138}" y2="{Y+27}" stroke="{a}" stroke-width="2"/><polygon points="{X+138},{Y+22} {X+144},{Y+27} {X+138},{Y+32}" fill="{a}"/>'
        if k == "handoff_feed": s += rect(X + 12, Y + 56, W - 24, 36, BEI, LINE) + t(X + 20, Y + 70, "TEAM FEED", 7.5, a, "hind", 700) + t(X + 20, Y + 85, "Blog passed the bids post to Build", 9.5, INK)
        else: s += t(cx, Y + 78, "nothing posted", 10, MUTE, "hind", 400, "middle")
        return s
    if k in ("save_push", "save_dropbox"):
        s = rect(X, Y, W, H, W_, LINE) + card(X + 12, Y + 30, 52, 44, BEI, INK) + t(X + 38, Y + 56, "Results", 10, INK, "khand", 700, "middle")
        s += f'<line x1="{X+68}" y1="{Y+44}" x2="{X+110}" y2="{Y+30}" stroke="{a}" stroke-width="2"/>' + card(X + 112, Y + 14, 84, 30, W_, INK) + t(X + 154, Y + 33, "GitHub", 11, INK, "khand", 700, "middle")
        if k == "save_dropbox": s += f'<line x1="{X+68}" y1="{Y+60}" x2="{X+110}" y2="{Y+74}" stroke="{a}" stroke-width="2" stroke-dasharray="4 3"/>' + card(X + 112, Y + 60, 84, 30, W_, a) + t(X + 154, Y + 79, "Dropbox, daily", 10, INK, "khand", 700, "middle")
        return s
    if k in ("split_theme", "split_part"):
        n1, n2 = ("Calm Line", "Beauty Line") if k == "split_theme" else ("Part One", "Part Two")
        s = rect(X, Y, W, H, BEI, LINE) + card(X + 12, Y + 30, 52, 44, W_, INK) + t(X + 38, Y + 56, "Tea", 12, INK, "khand", 700, "middle")
        s += f'<polygon points="{X+70},{Y+48} {X+84},{Y+52} {X+70},{Y+56}" fill="{a}"/>'
        return s + card(X + 92, Y + 12, 104, 36, W_, a) + t(X + 144, Y + 35, n1, 11, INK, "khand", 700, "middle") + card(X + 92, Y + 56, 104, 36, W_, a) + t(X + 144, Y + 79, n2, 11, INK, "khand", 700, "middle")
    if k in ("btn_round", "btn_square"):
        r = 10 if k == "btn_round" else 0
        s = rect(X, Y, W, H, W_, LINE) + rect(cx - 70, Y + 8, 140, 56, W_, INK, 10) + rect(cx - 62, Y + 16, 124, 32, a, "none", 6)
        for i, l in enumerate(["THIS", "BOTH", "LOVE", "THAT"]): s += rect(X + 14 + i * 46, Y + 72, 42, 24, W_, INK, r) + t(X + 35 + i * 46, Y + 88, l, 8, INK, "hind", 700, "middle")
        return s
    if k in ("cap_cream", "cap_white"):
        s = rect(X, Y, W, H, W_, LINE) + rect(X + 14, Y + 8, W - 28, 56, a)
        if k == "cap_cream": s += rect(X + 14, Y + 64, W - 28, 32, BEI)
        else: s += f'<line x1="{X+14}" y1="{Y+70}" x2="{X+W-14}" y2="{Y+70}" stroke="{LINE}" stroke-width="1.5"/>'
        return s + t(X + 22, Y + 86, "Roselle With Butterfly Pea", 11, INK, "khand", 700)
    if k in ("mock_color", "mock_grey"):
        c1, c2, c3 = ("#C1502E", "#05668D", "#0B6E4F") if k == "mock_color" else ("#BDBDBD", "#BDBDBD", a)
        s = rect(X, Y, W, H, W_, LINE) + rect(cx - 70, Y + 8, 140, 88, W_, INK, 0, 1.5)
        s += rect(cx - 62, Y + 16, 124, 14, c1) + rect(cx - 62, Y + 38, 58, 30, "none", c2, 0, 2) + rect(cx + 4, Y + 38, 58, 30, "none", c2, 0, 2) + rect(cx - 62, Y + 76, 70, 12, c3)
        return s
    return None
