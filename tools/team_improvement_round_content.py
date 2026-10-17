"""Team Improvement Deck, next round (Branding, Oct 17 2026). 10 picks (R86/R88; R75 said 20).
Sources: ops/team-sync/handoffs/team-improvement-sources-2026-10-16.md incl. '## Brand scan 2026-10-16' (scan items 1-5, 7-9, 12),
plus the one card Max skipped in round 1 (Idea Card), re-asked reworded (R64 / R87 skipped cards).
Each pair: (group, ask, A, B); option = (label, desc, fact1, fact2, drawing kind)."""
def P(g, ask, a, b): return (g, ask, a, b)
NAME = "Team Improvement Deck"
ABOUT = "Broad improvements to how the Grok Bot team works: round two, mostly deck look from the Oct 16 brand scan, plus one re-asked card"
PAIRS = [
P("Boards", "Idea Cards, Asked Again: Just A Big Picture Or A Picture With Approve And Not Now?",
  ("Just A Big Picture", "Tap the picture to open the idea; nothing else on the card.", "Clean", "Visual", "bigpic"),
  ("Picture With Buttons", "Picture plus Approve and Not Now right under it.", "Act fast", "One tap", "picbtn")),
P("Deck Look", "Deck Page Background: Pure White Or Soft Cream?",
  ("Pure White", "White page, cream only for small bands.", "Crisp", "Max standard", "bg_white"),
  ("Soft Cream", "The whole page in light cream #FAF6EE.", "Warm", "Softer", "bg_cream")),
P("Deck Look", "Deck Card Corners: Square Or Softly Rounded?",
  ("Square Corners", "Sharp corners like the rest of the boards.", "Matches boards", "Clean", "corner_sq"),
  ("Softly Rounded", "Small 10px corners like Ready To Swipe cards.", "Friendly", "Card feel", "corner_rd")),
P("Decks", "Vote Buttons: Keep This, Both, Love, That, Neither Or Switch To No, Maybe, Love, Yes?",
  ("Keep This / That", "This, Both, Love, That, Neither, Skip.", "Familiar", "Pairs", "votes_a"),
  ("No / Maybe / Yes", "No, Maybe, Love, Yes, plus Skip.", "Plain words", "Guide style", "votes_b")),
P("Decks", "Topics With Several Views: A Swipe Carousel Card Or One Split-Screen Pair?",
  ("Carousel Card", "Swipe sideways through 3 views on one card.", "More views", "Phone friendly", "carousel"),
  ("Split-Screen Pair", "Two views side by side, nothing hidden.", "See both", "Simple", "split")),
P("Decks", "Text-Only Topics: Add Simple Drawn Mockups Or Keep Fast Text Cards?",
  ("Drawn Mockups", "A small drawing for every card, even to-do items.", "Visual", "Slower to build", "mockup"),
  ("Fast Text Cards", "Big clear words only, quick to swipe.", "Fast", "No clutter", "textcard")),
P("Decks", "Odd-Size Old Decks: Split Into 10-Pick Decks Or Archive Them?",
  ("Split Into 10s", "Cut each into 10-pick decks by theme.", "Nothing lost", "More decks", "splitdeck"),
  ("Archive Them", "Move them off the shelves into an archive.", "Tidy shelves", "Can come back", "archive")),
P("Decks", "Font Questions: Show The Real Font In The Picture Or Keep Khand And Hind And Name It?",
  ("Show Real Font", "The mockup uses the font being compared.", "True look", "Exact", "font_real"),
  ("Name The Font", "Mockup stays in Khand/Hind; font named below.", "Consistent", "Simpler", "font_named")),
P("Decks", "Small Mockups On A Phone: Scale Up To Fill The Card Or Keep Small With A Caption?",
  ("Scale Up", "The mockup grows to fill the picture box.", "Easy to see", "Big", "scale_up"),
  ("Small With Caption", "Real-size mockup with a caption below it.", "True size", "Calm", "small_cap")),
P("Decks", "Long Card Text: One Line Only Or Up To Two Lines?",
  ("One Line Only", "Every option fits on one line.", "Fast read", "Short", "line1"),
  ("Up To Two Lines", "A short title plus a one-line description.", "More context", "Clear", "line2")),
]
assert len(PAIRS) == 10
