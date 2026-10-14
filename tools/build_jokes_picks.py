#!/usr/bin/env python3
"""Build a Jokes 20-card Style Swipe deck (R66): 4 categories x 5 pairs = 20.
Usage (repo root): python3 tools/build_jokes_picks.py <deck-id> "<Deck Name>" [seed]
Refill (R66): after each Jokes submit, run again with a new descriptive id (e.g. jokes-picks-round-two) and seed,
then set it as `ready` in /workspace/jokes-dashboard/launcher.json and run ./update.sh.
Neutral data only: bit titles, statuses and one-line premise labels. No joke text."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from personal_kit import *
did, name = sys.argv[1], sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 41
D = Deck(did, "jkp" + str(seed) + "_", 'Jokes', 'Stand-Up Set', "mic", TERRA)
D.topic("db", 'Dashboard Deck', 'Dashboard Deck', "tiles", [('Bits', 'In progress', '8'), ('Punched Up', 'Ready', '2'), ('Raw Notes', 'Needs work', '6'), ('Ideas', 'New', '10'), ('Routines', 'Reports', '2'), ('Decks', 'Open', '1')], "header")
D.topic("pg", 'Joke Page Style', 'Joke Page Style', "type", [('Bit Title', 'Neutral title only', 'Raw'), ('Length', '2 Min', ''), ('Status', 'Raw Notes', '')], "corners")
D.topic("sl", 'Set List and Bit Tools', 'Set List and Bit Tools', "list", [('Opener', 'Short', '1 Min'), ('Line-Cutting Bit', 'Raw Notes', '2 Min'), ('Pride Bit', 'Raw Notes', '2 Min'), ('Chivalry Bit', 'Raw Notes', '2 Min'), ('Closer', 'Punched Up', '3 Min')], "accent")
D.topic("pp", 'Premise Picks', 'Premise Picks', "list", [('Thai Tones', 'Language', 'Idea'), ('AI Team', 'Tech', 'Idea'), ('Quick Look', 'Work', 'Idea'), ('Mango Camera', 'Creator Life', 'Idea'), ('Basically Local', 'Living Abroad', 'Idea')], "density")
D.publish_meta(name, ["Jokes R66 deck: Dashboard Deck, Joke Page Style, Set List and Bit Tools, Premise Picks", "White light mode, Khand/Hind, Title Case, English only, no emoji", "Example data only, neutral titles"], {"source": '/workspace/jokes-dashboard'}, seed)
