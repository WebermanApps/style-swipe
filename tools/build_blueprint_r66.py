#!/usr/bin/env python3
"""Build a Blueprint 20-card Style Swipe deck (R66): exactly 4 topics × 5 pairs = 20.

Categories (launcher.json): rooms | materials | exterior | systems | style
Usage (from style-swipe root):
  python3 tools/build_blueprint_r66.py <deck-id> "<Deck Name>" [seed] [cat,cat,...]
Refill after submit / after deck-request:
  python3 tools/build_blueprint_r66.py blueprint-r66-<stamp> "Blueprint: …" <seed> rooms,materials
  then set ready in /workspace/blueprint-dashboard/launcher.json (see tools/blueprint_r66_ready.py).
Skipped cards: reword in the next run (R64); unanswered come first when you pass --carry ids.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from personal_kit import *

TOPICS = {
  "rooms": [
    ("kit", "Rooms", "Kitchen Layout", "tiles",
     [('Island', 'One long island', 'Open'), ('Two Islands', 'Prep + seating', 'Open'), ('Galley', 'Two runs', 'Compact'),
      ('L-Shape', 'Corner work', 'Open'), ('U-Shape', 'Wrap around', 'Open'), ('Herb Nook', 'Garden window', 'Open')], "corners"),
    ("liv", "Rooms", "Living Room", "tiles",
     [('Conversation Pit', 'Sunken seats', 'Open'), ('Open Plan', 'To kitchen', 'Open'), ('Tatami Bay', 'Quiet room', 'Open'),
      ('Fireplace Wall', 'Stone face', 'Open'), ('TV Wall', 'Hidden panel', 'Open')], "header"),
    ("ste", "Rooms", "Master Suite", "detail",
     [('Bed Wall', 'Oak headboard', 'Open'), ('Dressing', 'Walk-in', 'Open'), ('View Window', 'Garden', 'Open'),
      ('Reading Nook', 'Window seat', 'Open'), ('Door To Bath', 'Pocket', 'Open')], "header2"),
    ("gym", "Rooms", "Gym And Wellness", "list",
     [('Training Floor', 'Rubber zone', 'Open'), ('Cadillac', 'Pilates', 'Open'), ('Sauna', 'Hinoki', 'Open'),
      ('Cold Plunge', 'Zellige', 'Open'), ('Steam', 'Wet room', 'Open')], "density"),
  ],
  "materials": [
    ("wd", "Materials", "Wood And Stone", "swatch",
     [('Rift Oak', 'Straight grain', '#C8A47C'), ('Teak', 'Deep warm', '#A87849'), ('Hinoki', 'Pale cypress', '#E2CBA0'),
      ('Honed Limestone', 'Soft matte', '#DCD6CC'), ('Quartzite', 'Kitchen top', '#D8D2C8')], "corners"),
    ("tl", "Materials", "Tile And Texture", "swatch",
     [('Zellige', 'Handmade glaze', '#9BB7A8'), ('Large Format', 'Big stone tile', '#DCD6CC'),
      ('Terracotta', 'Warm floor', '#C47A4A'), ('Fluted Plaster', 'Wall rhythm', '#E9E4DA'), ('Lime Plaster', 'Soft white', '#F5F1E8')], "accent"),
    ("hw", "Materials", "Hardware And Light", "list",
     [('Brushed Stainless', 'Faucet + pulls', 'Open'), ('Matte Black', 'Levers', 'Open'), ('Unlacquered Brass', 'Warm metal', 'Open'),
      ('Linear Pendant', 'Island light', 'Open'), ('Path Lights', 'Garden', 'Open')], "density"),
    ("dr", "Materials", "Doors And Windows", "detail",
     [('Front Door', 'Solid oak', 'Open'), ('Lift And Slide', 'To pergola', 'Open'), ('Black Frame', 'Windows', 'Open'),
      ('Interior Door', 'Flush oak', 'Open'), ('Shoji Screen', 'Light filter', 'Open')], "header"),
  ],
  "exterior": [
    ("ent", "Exterior", "Entry And Face", "tiles",
     [('Street Gate', 'Wood + steel', 'Open'), ('Front Path', 'Stone', 'Open'), ('Deep Eave', 'Shade', 'Open'),
      ('Carport', 'Open side', 'Open'), ('Mail Nook', 'Wall slot', 'Open')], "corners"),
    ("ct", "Exterior", "Courtyard", "tiles",
     [('Engawa', 'Wood deck', 'Open'), ('Planted Court', 'Maples', 'Open'), ('Gravel Band', 'Drain', 'Open'),
      ('Water Basin', 'Still pool', 'Open'), ('Lanterns', 'Path', 'Open')], "header"),
    ("pl", "Exterior", "Pool And Garden", "list",
     [('Salt Pool', '34 × 12', 'Open'), ('Pool Deck', 'Stone', 'Open'), ('Vegetable Beds', 'Drip lines', 'Open'),
      ('Orchard', 'Fruit trees', 'Open'), ('Sprint Lane', 'Lawn', 'Open')], "density"),
    ("rf", "Exterior", "Roof And Walls", "swatch",
     [('Metal Roof', 'Standing seam', '#8A9096'), ('Lime Plaster', 'White wall', '#F5F1E8'),
      ('Board Form', 'Concrete base', '#B8B5AE'), ('Wood Soffit', 'Under eave', '#C8A47C'), ('Stone Base', 'Low wall', '#DCD6CC')], "accent"),
  ],
  "systems": [
    ("wtr", "Systems", "Water Systems", "list",
     [('Rain Cisterns', '80 m³', 'Set'), ('Well Treat', 'Full train', 'Set'), ('Mains Backup', 'Air gap + RPZ', 'Set'),
      ('Hot Water', 'Heat pump 300 L', 'Open'), ('Irrigation', 'Purple pipe', 'Open')], "density"),
    ("nrg", "Systems", "Energy", "chart",
     [('Solar', 'Example week', '20 kWp'), ('Battery', 'Example', '30 kWh'), ('Grid Use', 'Example', 'Low'),
      ('EV Ready', 'Carport', 'Open'), ('Monitor', 'Panel app', 'Open')], "accent2"),
    ("cl", "Systems", "Climate", "list",
     [('ERV', 'Fresh air', 'Open'), ('Heat Pump', 'Air handler', 'Open'), ('Ceiling Fans', 'Quiet', 'Open'),
      ('Floor Heat', 'Bath zones', 'Open'), ('Shade', 'Deep eaves', 'Set')], "corners"),
    ("str", "Systems", "Structure", "list",
     [('Steel Stud', 'Walls', 'Set'), ('Fiber Cement', 'Board', 'Set'), ('Lime Plaster', 'Finish', 'Set'),
      ('Engineer Check', 'Stud sizing', 'Open'), ('Roof Frame', 'Metal', 'Set')], "header"),
  ],
  "style": [
    ("ov", "Style", "Overall Look", "tiles",
     [('Japanese Modern', 'Warm timber', 'Open'), ('Quiet Luxury', 'Soft stone', 'Open'), ('Tropical Modern', 'Deep eave', 'Open'),
      ('Courtyard House', 'Inward', 'Open'), ('Minimal Warm', 'Few materials', 'Open')], "corners"),
    ("tb", "Style", "Tie-Breakers", "buttons",
     [('Engawa Surface', 'Flagstone or wood', 'Open'), ('Yes', '', ''), ('Not Yet', '', ''),
      ('Next: Island Edge', 'Stone or wood', 'Queued')], "corners"),
    ("tot", "Style", "This Or That", "list",
     [('Door Hardware', 'Round 3', 'Open'), ('Dining Table', 'Round 3', 'Open'), ('Exterior Lights', 'Round 3', 'Open'),
      ('Wall Texture', 'On request', 'Open'), ('Accent Plaster', 'On request', 'Open')], "density"),
    ("ui", "Style", "App And Deck Feel", "tiles",
     [('Plain Title', 'No house banner', 'Set'), ('Water Diagram', 'Plus item list', 'Set'),
      ('Deck Groups', 'Rooms · Materials · Style', 'Set'), ('Open A New Deck', '20 cards', 'Set'),
      ('Progress Rows', 'Compact', 'Set')], "header"),
  ],
}

def pick_topics(cats):
  cats = [c for c in cats if c in TOPICS] or list(TOPICS)
  # Exactly 4 topics for 20 pairs
  pool = []
  i = 0
  while len(pool) < 4:
    c = cats[i % len(cats)]
    opts = TOPICS[c]
    pool.append(opts[(i // len(cats)) % len(opts)])
    i += 1
    if i > 40: break
  # dedupe by key
  seen, out = set(), []
  for t in pool:
    if t[0] in seen: continue
    seen.add(t[0]); out.append(t)
    if len(out) == 4: break
  while len(out) < 4:
    for c in TOPICS:
      for t in TOPICS[c]:
        if t[0] not in seen:
          seen.add(t[0]); out.append(t)
          if len(out) == 4: break
      if len(out) == 4: break
  return out[:4]

def main():
  args = sys.argv[1:]
  if len(args) < 2:
    sys.exit(__doc__)
  did, name = args[0], args[1]
  seed = int(args[2]) if len(args) > 2 and args[2].isdigit() else 14
  cats = (args[3] if len(args) > 3 else "rooms,materials,exterior,systems,style").split(",")
  cats = [c.strip() for c in cats if c.strip()]
  D = Deck(did, "bpr66_", "Weberman Residence", "Dream Home · 20", "house", LAGOON)
  topics = pick_topics(cats)
  for key, group, cat, body, items, fin in topics:
    D.topic(key, group, cat, body, items, fin)
  assert len(D.pairs) == 20, len(D.pairs)
  D.publish_meta(
    name,
    ["Blueprint R66: 20-card deck split across " + ", ".join(cats),
     "White light mode, Khand/Hind, Title Case, English only, no emoji",
     "Example data only; unanswered return and skips reworded on refill (R61/R64)"],
    {"launcher": "/workspace/blueprint-dashboard/launcher.json", "categories": cats},
    seed,
  )
  print(f"built decks/{did}.json with {len(D.pairs)} pairs; cats={cats}")

if __name__ == "__main__":
  main()
