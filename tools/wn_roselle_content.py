"""Roselle Packaging Polish Deck (Max via WellNest, Oct 16 2026 21:44 ICT). Polish, not redesign, of the real WellNest roselle pouch
(Instagram story photos May 16 2024, cropped to img/wn-roselle/ref-front.jpg, ref-back.jpg): kraft stand-up pouch, cream label with a pink
watercolour wash at the bottom, circular WellNest script logo top right, 'ROSELLE' typewriter serif + 'organic herbal tea' italic, claims line,
info block on the wash, NET WT bottom right. Back: farm story, www.thewellnest.organic, About The Farm, certified organic + handmade icons, Directions.
Each option = (label, desc, fact1, fact2, view, overrides). view: front | back | tag. Overrides change ONE detail from CURRENT."""
CURRENT = dict(pink="#D9637A", fade="brush", washh=0.36, logo="tr", logos=1.0, titlew=400, thai=False, tagline="refreshing tarty sweet",
               claims="aid digestion | promote heart health | boost immunity", claimsz=4.2, window=False, seal="notch", sheen=False,
               weight="corner", qr="none", backlayout="stack", icons="line", tag="kraft")
PAIRS = [
("Pink Wash", "Pink Shade: Today's Dusty Rose Or A Softer Blush?", ("Dusty Rose", "Today's pink, kept as is.", "Today", "Warm", "front", {}), ("Softer Blush", "A lighter, paler pink.", "Lighter", "Soft", "front", {"pink": "#EBA3B1"})),
("Pink Wash", "Pink Shade: Dusty Rose Or Deeper Roselle Red?", ("Dusty Rose", "Today's pink.", "Today", "Warm", "front", {}), ("Roselle Red", "Closer to the brewed tea colour.", "Deeper", "Tea colour", "front", {"pink": "#B8324A"})),
("Pink Wash", "Wash Edge: Brushy Watercolour Or Smooth Fade?", ("Brushy Edge", "Today's hand-painted edge.", "Today", "Handmade", "front", {}), ("Smooth Fade", "Pink melts into cream.", "Smooth", "Soft", "front", {"fade": "smooth"})),
("Pink Wash", "Wash Height: Bottom Third Or Up To Half?", ("Bottom Third", "Today's height.", "Today", "More cream", "front", {}), ("Up To Half", "More pink on the shelf.", "More pink", "Bolder", "front", {"washh": 0.5})),
("Logo", "Logo Size: Today's Size Or A Little Bigger?", ("Today's Size", "Small ring top right.", "Today", "Quiet", "front", {}), ("A Little Bigger", "Ring about a third larger.", "Bigger", "Easier to see", "front", {"logos": 1.35})),
("Logo", "Logo Placement: Top Right Or Top Centre?", ("Top Right", "Where it sits today.", "Today", "Offset", "front", {}), ("Top Centre", "Centred above the name.", "Centred", "Balanced", "front", {"logo": "tc"})),
("Title", "Title Weight: Regular Typewriter Or Bold?", ("Regular", "Today's light typewriter ROSELLE.", "Today", "Light", "front", {}), ("Bold", "Same font, heavier.", "Bolder", "Reads far", "front", {"titlew": 700})),
("Title", "Thai Name: Leave Off Or Add กระเจี๊ยบ?", ("Leave Off", "English only, as today.", "Today", "Clean", "front", {}), ("Add Thai Name", "Small Thai name under ROSELLE.", "Bilingual", "Local", "front", {"thai": True})),
("Words", "Tagline: 'Refreshing Tarty Sweet' Or 'Tart, Bright, Gently Sweet'?", ("Refreshing Tarty Sweet", "Today's wording.", "Today", "Playful", "front", {}), ("Tart, Bright, Gently Sweet", "Same idea, smoother words.", "Smoother", "Clear", "front", {"tagline": "tart, bright, gently sweet"})),
("Words", "Claims Text Size: Today's Small Size Or Slightly Larger?", ("Today's Size", "Small claims line.", "Today", "Subtle", "front", {}), ("Slightly Larger", "Easier to read.", "Readable", "Clear", "front", {"claimsz": 5.4})),
("Words", "Claims Line: Three Claims Or Two Shorter Ones?", ("Three Claims", "Digestion, heart, immunity.", "Today", "Full", "front", {}), ("Two Claims", "Aid digestion, caffeine free.", "Shorter", "Calmer", "front", {"claims": "aid digestion | caffeine free"})),
("Back Panel", "Back Layout: Stacked Sections Or Two Columns Below The Story?", ("Stacked", "Story, farm, icons, directions in one column.", "Today", "Simple", "back", {}), ("Two Columns", "Farm and Directions side by side.", "Compact", "Tidy", "back", {"backlayout": "cols"})),
("Back Panel", "Back Icons: Thin Line Or Filled Pink?", ("Thin Line", "Today's line icons.", "Today", "Light", "back", {}), ("Filled Pink", "Icons in the wash pink.", "Colour", "Matches front", "back", {"icons": "pink"})),
("Pouch", "Window: No Window Or Small Window Showing Calyces?", ("No Window", "Plain kraft, as today.", "Today", "Clean", "front", {}), ("Small Window", "See the dried roselle.", "See inside", "Real", "front", {"window": True})),
("Pouch", "Top Of Pouch: Tear Notch Only Or Sticker Seal?", ("Tear Notch", "Today's zip and notch.", "Today", "Simple", "front", {}), ("Sticker Seal", "Small round seal over the top.", "Sealed", "Gift feel", "front", {"seal": "sticker"})),
("Pouch", "Kraft Finish: Matte Or Slight Sheen?", ("Matte Kraft", "Today's paper feel.", "Today", "Natural", "front", {}), ("Slight Sheen", "Soft gloss catches light.", "Polished", "Premium", "front", {"sheen": True})),
("Pouch", "Weight Callout: Small Corner Text Or Clear Badge?", ("Small Corner", "NET WT in the corner, as today.", "Today", "Quiet", "front", {}), ("Clear Badge", "100 g in a small circle.", "Clear", "Easy to spot", "front", {"weight": "badge"})),
("Back Panel", "QR Code: Next To Directions Or Next To The Website?", ("Next To Directions", "Scan for brewing video.", "Brewing", "Bottom", "back", {"qr": "dir"}), ("Next To Website", "Scan for the farm story.", "Story", "Top", "back", {"qr": "web"})),
("Shelf Tag", "Shelf Tag: Kraft With Pink Wash Or Plain Cream?", ("Kraft With Pink Wash", "Matches the pouch.", "Matching", "Warm", "tag", {}), ("Plain Cream", "Quiet cream tag.", "Quiet", "Clean", "tag", {"tag": "cream"})),
("Shelf Tag", "Shelf Tag Line: Name And Weight Or Add Farm Line?", ("Name And Weight", "Roselle, organic herbal tea, 100 g.", "Short", "Clear", "tag", {}), ("Add Farm Line", "Adds 'From Kraingan Farm, Chiang Mai'.", "Story", "Local", "tag", {"tag": "farm"})),
]
assert len(PAIRS) == 20
