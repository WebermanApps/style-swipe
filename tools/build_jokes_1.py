#!/usr/bin/env python3
"""Build Style Swipe deck jokes-1 (PUBLISHED): Jokes Round 1: Set List, Bit Card, Tag Picks, Set Timer, Joke Page Style, Bit Library, Navigation, New Tag Alerts, Bit Ratings, Open Bits.
Based on the Jokes agent's current work (team-feed, team-sync recaps, latest files; source: /workspace/jokes-dashboard).
Pattern: tools/build_dashboard_2.py + draft_svg.py via tools/personal_kit.py. Example data only. Run from the repo root."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from personal_kit import *
D = Deck("jokes-1", "jk1_", 'Jokes', 'Stand-Up Set', "mic", TERRA)
D.topic("sl", 'Set List', 'Set List', "list", [('Opener', 'Short and quick', '1 Min'), ('Helpless Romantic', 'Closer bit', '3 Min'), ('The Obituary', 'New bit', '2 Min'), ('Wheelchair Line', 'Idea', '1 Min'), ('Tamagotchi', 'Idea', '2 Min')], "corners")
D.topic("bc", 'Bit Card', 'Bit Card', "detail", [('Helpless Romantic', 'Closer with two tag options', '3 Min'), ('Setup', '', ''), ('Turn', '', ''), ('Tag One', '', ''), ('Tag Two', '', '')], "accent")
D.topic("tg", 'Tags', 'Tag Picks', "buttons", [('The Obituary Bit', 'Which tag lands harder?', '2 Tags'), ('Tag One', '', ''), ('Tag Two', '', ''), ('Next Bit', 'Wheelchair Line', 'Idea')], "density")
D.topic("tm", 'Set Timer', 'Set Timer', "chart", [('Set Length, Example', 'Target 10 minutes', '9 Min'), ('Longest Bit', 'Romantic', '3 Min'), ('Open Slots', 'Two', '2')], "accent2")
D.topic("pg", 'Joke Page Style', 'Joke Page Style', "type", [('Tell The Story', 'The obituary bit, new draft', 'New Bit'), ('Length', '2 min', ''), ('Status', 'Draft', '')], "corners")
D.topic("lib", 'Bit Library', 'Bit Library', "tiles", [('Romantic', 'Closer', 'Ready'), ('Obituary', 'New', 'Draft'), ('Wheelchair', 'Idea', 'Idea'), ('Tamagotchi', 'Idea', 'Idea'), ('Housewarming', 'Card lines', 'Done'), ('Opener', 'Short', 'Ready'), ('Airport', 'Old', 'Ready'), ('Gym', 'Old', 'Ready')], "header")
D.topic("nv", 'App Layout', 'Navigation', "nav", [('Set List', 'Tonight', '5'), ('Bits Library', 'All', '12'), ('Tags Picks', 'Open', '2'), ('Ideas Inbox', 'New', '3')], "header2")
D.topic("nt", 'Alerts', 'New Tag Alert', "notice", [('New Tags Ready', 'Two tags for the obituary bit', 'Now'), ('Romantic', 'Closer', 'Ready'), ('Obituary', 'New', 'Draft'), ('Opener', 'Short', 'Ready')], "accent")
D.topic("rt", 'Bit Ratings', 'Bit Ratings', "chart", [('Laughs By Bit, Example', 'Example ratings', '5 Bits'), ('Best', 'Romantic', 'Top'), ('Needs Work', 'Gym', 'Low')], "density")
D.topic("ob", 'Set List', 'Open Bits', "list", [('Wheelchair Line', 'Needs a turn', 'Idea'), ('Tamagotchi', 'Needs a setup', 'Idea'), ('Airport', 'Needs a tag', 'Old'), ('Gym', 'Needs a closer', 'Old'), ('Dating App', 'New idea', 'Idea')], "header")
D.publish_meta('Jokes Round 1: Set List, Bit Card, Tag Picks, Set Timer, Joke Page Style, Bit Library, Navigation, New Tag Alerts, Bit Ratings, Open Bits', ["Jokes: open design, branding, content and app decisions with drawn SVG mockups", "White light mode, Khand/Hind, Title Case, English only, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017", "Example data only"], {"team_feed": "/workspace/ops/team-feed.md", "recaps": "/workspace/ops/team-sync/2026-10-13.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md", "source": '/workspace/jokes-dashboard'}, 37)
