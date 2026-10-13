#!/usr/bin/env python3
"""Build Style Swipe deck thai-2 (PUBLISHED): Thai Round 2: Quiz Answers, Daily Tip, Known Words, Progress, Word Card, Audio Controls, Home, Navigation, Bring Back, Vocab Check.
Based on the Thai Study agent's current work (team-feed, team-sync recaps, latest files; source: decks/thai-1.json).
Pattern: tools/build_dashboard_2.py + draft_svg.py via tools/personal_kit.py. Example data only. Run from the repo root."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from personal_kit import *
D = Deck("thai-2", "th2_", 'Thai Study', '94 Active Words', "speaker", JUNGLE)
D.topic("qa", 'Quiz', 'Quiz Answers', "list", [('Water', 'Naam', 'A'), ('Rice', 'Khao', 'B'), ('Thank You', 'Khop Khun', 'C'), ('Hello', 'Sawatdee', 'D'), ('Delicious', 'Aroi', 'E')], "corners")
D.topic("tip", 'Daily Tip', 'Daily Tip Card', "type", [('Do You Have...?', 'Say it as Mii ... Mai', 'Daily Tip'), ('Example', 'Mii naam mai', ''), ('Meaning', 'Do you have water?', '')], "accent")
D.topic("kw", 'Known Words', 'Known Words Archive', "list", [('Hello', 'Known since Oct 12', 'Back'), ('Water', 'Known since Oct 12', 'Back'), ('Rice', 'Known since Oct 12', 'Back'), ('Market', 'Known since Oct 12', 'Back'), ('Friend', 'Known since Oct 12', 'Back')], "density")
D.topic("prog", 'Progress', 'Progress', "chart", [('Words Learned', 'Example week', '62'), ('Due Today', 'Review', '12'), ('Known', 'Archived', '32')], "accent2")
D.topic("wc", 'Word Card', 'Word Card', "detail", [('Aroi', 'Delicious, said with a rising tone', 'Tone: Low'), ('Hear It', '', ''), ('Slow Replay', '', ''), ('Say It Back', '', ''), ('Use It In A Line', '', '')], "corners")
D.topic("aud", 'Audio', 'Audio Controls', "buttons", [('Khop Khun', 'Thank you', 'Audio'), ('Play', '', ''), ('Slow', '', ''), ('Next Word', 'Due today', '12 left')], "accent")
D.topic("home", 'Home', 'Study Home', "tiles", [('Quiz', '94 active words', 'Start'), ('Flashcards', 'Due today', '12'), ('Vocab Check', 'Sort words', 'New'), ('Known Words', 'Archive', '32'), ('Daily Tip', 'Today', '1'), ('Tones', 'Guide', '5'), ('Letters', 'Practice', '44'), ('Listen', 'Audio only', 'Go')], "density")
D.topic("nav", 'Navigation', 'Navigation', "nav", [('Quiz Words', 'Practice', '94'), ('Cards Review', 'Due', '12'), ('Check Words', 'Sort', 'New'), ('Known Words', 'Archive', '32')], "header")
D.topic("bb", 'Known Words', 'Bring Back Message', "notice", [('Word Brought Back', 'Water is in the quiz again', 'Now'), ('Rice', 'Known', 'Back'), ('Market', 'Known', 'Back'), ('Friend', 'Known', 'Back')], "header2")
D.topic("vc", 'Vocab Check', 'Vocab Check Buttons', "buttons", [('Hello', 'Do you know this word?', 'Check'), ('I Know It', '', ''), ('Still Learning', '', ''), ('Progress', 'Word 14 of 30', '14/30')], "corners")
D.publish_meta('Thai Round 2: Quiz Answers, Daily Tip, Known Words, Progress, Word Card, Audio Controls, Home, Navigation, Bring Back, Vocab Check', ["Thai Study: open design, branding, content and app decisions with drawn SVG mockups", "White light mode, Khand/Hind, Title Case, English only, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017", "Example data only"], {"team_feed": "/workspace/ops/team-feed.md", "recaps": "/workspace/ops/team-sync/2026-10-13.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md", "source": 'decks/thai-1.json'}, 32, based_on="thai-1")
