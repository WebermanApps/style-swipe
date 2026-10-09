#!/usr/bin/env python3
"""
Style Swipe deck generator for Max Weberman.

Usage:
  python3 generate_deck.py                       # deck for today
  python3 generate_deck.py --date 2026-10-10     # deck for a given date
  python3 generate_deck.py --ingest results.json # fold exported swipe results into profile.json
  python3 generate_deck.py --ingest r.json --date 2026-10-10   # ingest, then generate next deck
Options:
  --pairs N        number of pairs (default 50)
  --no-embed       don't rebuild index.html with the new deck embedded
  --force          overwrite an existing deck file for that date
  --seed S         random seed (default: derived from date)
  --allow-repeats  if fresh options run out, top up with previously shown ones

What it does:
  * ALWAYS FRESH: never reuses an option that appeared in any earlier deck. The ledger of
    shown options lives in shown_options.json (merged with every decks/*.json, and it never
    forgets). Each option appears at most once per deck. If the unseen pool runs short, the
    deck is shortened with a warning (or topped up with old options only with --allow-repeats).
    Add new options to POOL / POOL_EXTRA to extend the runway.
  * Reads profile.json (accumulated tag + option stats) and biases toward
    *uncertain* areas: categories / tags with few or split votes get more pairs,
    and pairs are chosen to contrast on uncertain tags. Once a direction is clear
    it adds "refinement" pairs between options that are both on the liked side.
  * Writes decks/YYYY-MM-DD.json and (by default) re-renders index.html from
    index.template.html with the deck embedded (images inlined as data URIs) so
    the HTML stays a single self-contained file.
"""
import argparse, base64, datetime as dt, glob, io, itertools, json, math, os, random, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DECKS = os.path.join(ROOT, "decks")
PROFILE = os.path.join(ROOT, "profile.json")
TEMPLATE = os.path.join(ROOT, "index.template.html")
INDEX = os.path.join(ROOT, "index.html")
CREDITS = os.path.join(ROOT, "img", "credits.json")
SHOWN = os.path.join(ROOT, "shown_options.json")

# ---------------------------------------------------------------------------
# Option pool. Each option: id, label, desc, tags, visual (rendered by the app)
# ---------------------------------------------------------------------------
F = {  # font stacks (Google Fonts loaded by the page when online, fallbacks otherwise)
    "inter": "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif",
    "grotesk": "'Space Grotesk', 'Inter', system-ui, sans-serif",
    "playfair": "'Playfair Display', Georgia, serif",
    "dmserif": "'DM Serif Display', Georgia, serif",
    "fraunces": "'Fraunces', Georgia, serif",
    "lora": "'Lora', Georgia, serif",
    "baskerville": "'Libre Baskerville', Baskerville, Georgia, serif",
    "cormorant": "'Cormorant Garamond', Garamond, Georgia, serif",
    "montserrat": "'Montserrat', 'Helvetica Neue', Arial, sans-serif",
    "worksans": "'Work Sans', 'Helvetica Neue', Arial, sans-serif",
    "oswald": "'Oswald', 'Arial Narrow', Impact, sans-serif",
    "bebas": "'Bebas Neue', 'Arial Narrow', Impact, sans-serif",
    "archivo": "'Archivo Black', 'Arial Black', Impact, sans-serif",
    "plexmono": "'IBM Plex Mono', ui-monospace, Menlo, monospace",
    "prompt": "'Prompt', 'Montserrat', system-ui, sans-serif",
    "sarabun": "'Sarabun', 'Inter', system-ui, sans-serif",
    "caveat": "'Caveat', 'Comic Sans MS', cursive",
}

def ui(i, label, desc, tags, bg, surface, text, accent, radius=12, font="inter", shadow="soft", border="none", muted=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="ui", bg=bg, surface=surface, text=text,
                accent=accent, radius=radius, font=F[font], shadow=shadow, border=border, muted=muted or text))

def pal(i, label, desc, tags, colors):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="palette", colors=colors))

def typ(i, label, desc, tags, head, body, hw=700, upper=False, track="0"):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="type", head=F[head], body=F[body],
                headWeight=hw, upper=upper, tracking=track))

def tone(i, label, desc, tags, s1, s2):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="tone", lines=[s1, s2]))

def img(i, label, desc, tags, key, colors, materials, filt=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="image", key=key, filter=filt,
                colors=colors, materials=materials))

def mood(i, label, desc, tags, colors, materials):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="mood", colors=colors, materials=materials))

def logo(i, label, desc, tags, mark, word, font, fg, bg, shape="none", weight=700, spacing="0.02em", italic=False, upper=True, accent=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="logo", mark=mark, word=word, font=F[font],
                fg=fg, bg=bg, shape=shape, weight=weight, spacing=spacing, italic=italic, upper=upper, accent=accent or fg))

def thumb(i, label, desc, tags, bg, fg, accent, font, layout, text, key=None, filt=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="thumb", bg=bg, fg=fg, accent=accent,
                font=F[font], layout=layout, text=text, key=key, filter=filt))

POOL = {
 "App / UI Style": [
  ui("ui_swiss", "Swiss Minimal", "White space, black type, one sharp accent, square corners.", ["minimal","light","modern","technical"], "#ffffff","#ffffff","#111111","#e63312",0,"inter","none","1px solid #111"),
  ui("ui_soft", "Soft Neumorphic", "Pillowy cards, gentle shadows, rounded everything.", ["soft","light","friendly","modern"], "#eef0f4","#eef0f4","#3b4252","#5e81ac",22,"inter","neu"),
  ui("ui_dark_pro", "Dark Pro Dashboard", "Charcoal surfaces, neon-teal data accents, dense info.", ["dark","technical","bold","modern"], "#0f1115","#1a1d24","#e6e8ee","#2dd4bf",10,"grotesk","glow","1px solid #2a2f3a"),
  ui("ui_warm_paper", "Warm Paper", "Cream background, serif headings, ink-brown text.", ["warm","classic","editorial","light"], "#f6f0e4","#fffaf0","#3a2e22","#b5651d",6,"lora","soft","1px solid #e3d6bf"),
  ui("ui_brutal", "Neo-Brutalist", "Thick black borders, hard offset shadows, loud yellow.", ["bold","playful","raw","light"], "#fff8e1","#ffffff","#000000","#ffd400",4,"archivo","hard","3px solid #000"),
  ui("ui_glass", "Glassmorphism", "Frosted translucent panels over a gradient.", ["modern","luxe","cool","vibrant"], "linear-gradient(135deg,#6a5acd,#00b4d8)","rgba(255,255,255,.22)","#ffffff","#ffe066",18,"inter","soft","1px solid rgba(255,255,255,.45)"),
  ui("ui_earthy", "Earthy Craft", "Clay, olive and sand with rounded friendly cards.", ["earthy","warm","natural","friendly"], "#efe6d8","#faf5ec","#3d3a2e","#6b7f3a",14,"worksans","soft"),
  ui("ui_luxe_dark", "Luxe Black & Gold", "Deep black, thin gold lines, spaced serif caps.", ["luxe","dark","classic","formal"], "#0b0b0b","#141414","#f2ead8","#c8a24a",2,"cormorant","none","1px solid #c8a24a"),
  ui("ui_material", "Clean Material", "Google-style cards, blue primary, clear hierarchy.", ["friendly","modern","light","technical"], "#f5f7fb","#ffffff","#1f2937","#2563eb",12,"inter","soft"),
  ui("ui_tropical", "Tropical Fresh", "Lagoon teal, mango accent, airy rounded layout.", ["tropical","vibrant","friendly","light"], "#e9fbf7","#ffffff","#0b3b3a","#ff9f1c",20,"prompt","soft"),
  ui("ui_terminal", "Terminal / Mono", "Monospace everything, green-on-black, no fluff.", ["technical","dark","minimal","raw"], "#050805","#0b120b","#b6f5b6","#39ff14",0,"plexmono","none","1px solid #1f3a1f"),
  ui("ui_blueprint", "Blueprint", "Construction-blueprint blue with white line work.", ["technical","industrial","cool","bold"], "#0b3d91","#0e4aa8","#ffffff","#ffd166",4,"grotesk","none","1px dashed rgba(255,255,255,.6)"),
  ui("ui_editorial", "Magazine Editorial", "Big serif headlines, generous margins, thin rules.", ["editorial","classic","minimal","light"], "#fbfbf8","#fbfbf8","#141414","#8b1e3f",0,"playfair","none","1px solid #ddd"),
  ui("ui_pastel", "Pastel Playful", "Candy pastels, bubbly corners, emoji-friendly.", ["playful","soft","friendly","light"], "#fff0f6","#ffffff","#5a3d5c","#ff7eb6",24,"montserrat","soft"),
 ],
 "Color Palette": [
  pal("pal_teak_jungle", "Teak & Jungle", "Teak brown, jungle green, rice-paper cream.", ["earthy","warm","natural","tropical"], ["#6b4226","#a0522d","#2f5d3a","#8fb08c","#f4ecd8"]),
  pal("pal_mono_ink", "Monochrome Ink", "Black, greys and white. Nothing else.", ["minimal","classic","cool","formal"], ["#0a0a0a","#3a3a3a","#7a7a7a","#c9c9c9","#ffffff"]),
  pal("pal_safety", "Safety & Steel", "Hi-vis orange, steel grey, concrete, asphalt.", ["industrial","bold","technical","construction"], ["#ff6b00","#2b2d31","#6c757d","#cfd4da","#f8f9fa"]),
  pal("pal_sunset_bkk", "Bangkok Sunset", "Coral, magenta, deep violet, warm gold.", ["vibrant","warm","bold","thai"], ["#ff6f59","#e23e7c","#5b2a86","#f7b32b","#fff1e6"]),
  pal("pal_navy_brass", "Navy & Brass", "Trustworthy navy with polished brass and ivory.", ["classic","formal","luxe","trust"], ["#0f2340","#1d3c6e","#b08d57","#e8dcc2","#fbf8f1"]),
  pal("pal_sage", "Sage Calm", "Sage, eucalyptus, oat, soft charcoal.", ["soft","natural","minimal","calm"], ["#9caf88","#c7d3bf","#e9e4d8","#f7f5ef","#3f4540"]),
  pal("pal_lagoon", "Andaman Lagoon", "Turquoise, deep teal, sand and white.", ["tropical","cool","vibrant","fresh"], ["#00a6a6","#05668d","#028090","#f0e6d2","#ffffff"]),
  pal("pal_terracotta", "Terracotta Clay", "Burnt orange, clay, rust and bone.", ["earthy","warm","rustic","natural"], ["#c1502e","#d9825b","#8c3b1f","#e8d5c4","#faf3eb"]),
  pal("pal_black_gold", "Black & Gold", "Jet black, champagne gold, warm white.", ["luxe","dark","bold","formal"], ["#000000","#1c1c1c","#c9a227","#e6cf8b","#faf7f0"]),
  pal("pal_electric", "Electric Tech", "Electric blue, cyan, ultraviolet on near-black.", ["technical","vibrant","dark","modern"], ["#0b0f1a","#1f6feb","#00e5ff","#7c3aed","#e6edf3"]),
  pal("pal_temple", "Temple Red & Gold", "Thai temple lacquer red, gold leaf, emerald.", ["thai","bold","warm","traditional"], ["#a4161a","#d4a017","#0b6e4f","#1b1b1b","#fff4d6"]),
  pal("pal_concrete", "Concrete & Oak", "Raw concrete greys with pale oak and black steel.", ["minimal","industrial","natural","modern"], ["#8d8d8a","#b9b8b3","#dedbd2","#c8a97e","#1f1f1f"]),
  pal("pal_forest", "Deep Forest", "Forest green, moss, bark and mist.", ["natural","dark","calm","earthy"], ["#1b3a2b","#355e3b","#6b8f71","#5c4033","#e8efe9"]),
  pal("pal_pastel", "Pastel Pop", "Peach, lilac, mint, butter yellow.", ["playful","soft","light","friendly"], ["#ffcdb2","#cdb4db","#b9fbc0","#fff3b0","#ffffff"]),
 ],
 "Typography": [
  typ("ty_inter", "Neutral Sans (Inter)", "Clean, invisible, very legible UI type.", ["minimal","modern","technical","neutral"], "inter","inter",700),
  typ("ty_playfair_inter", "Editorial Serif + Sans", "Playfair headlines with Inter body.", ["editorial","classic","luxe","contrast"], "playfair","inter",700),
  typ("ty_bebas", "Tall Condensed Caps", "Bebas Neue headlines, YouTube-thumbnail energy.", ["bold","loud","modern","youtube"], "bebas","worksans",400,True,"0.03em"),
  typ("ty_fraunces", "Soft Warm Serif", "Fraunces: chunky, friendly, a little quirky.", ["warm","friendly","editorial","craft"], "fraunces","lora",700),
  typ("ty_grotesk", "Techy Grotesk", "Space Grotesk: geometric with personality.", ["technical","modern","bold","geometric"], "grotesk","inter",700),
  typ("ty_mono", "Monospace Engineer", "IBM Plex Mono for a builder/engineer feel.", ["technical","raw","minimal","industrial"], "plexmono","plexmono",600),
  typ("ty_cormorant", "High-Contrast Classic", "Cormorant Garamond, spaced caps, refined.", ["luxe","classic","formal","elegant"], "cormorant","cormorant",600,True,"0.12em"),
  typ("ty_archivo", "Heavy Black Sans", "Archivo Black: blunt, solid, confident.", ["bold","industrial","loud","construction"], "archivo","worksans",400,True,"0"),
  typ("ty_montserrat", "Geometric Sans Caps", "Montserrat wide caps: clean corporate.", ["modern","formal","geometric","clean"], "montserrat","montserrat",700,True,"0.08em"),
  typ("ty_baskerville", "Bookish Serif", "Libre Baskerville throughout. Trustworthy, literary.", ["classic","warm","trust","editorial"], "baskerville","baskerville",700),
  typ("ty_prompt", "Thai-Friendly Sans", "Prompt: pairs naturally with Thai script (สวัสดี).", ["thai","friendly","modern","bilingual"], "prompt","sarabun",600),
  typ("ty_hand", "Handwritten Accent", "Caveat script accents over a simple sans.", ["playful","personal","warm","casual"], "caveat","worksans",700),
 ],
 "Business Communication Tone": [
  tone("tn_direct", "Direct & Brief", "Short, no fluff, action first.", ["direct","minimal","efficient"], "Roof repair is booked for Tuesday, 8am.", "Reply YES to confirm or call me with changes."),
  tone("tn_warm", "Warm & Personal", "Friendly, first-name, a bit of heart.", ["warm","friendly","personal"], "Hi Sarah, hope your week's going great!", "Just a heads-up: we'll be by Tuesday morning to take care of that roof."),
  tone("tn_formal", "Formal & Polished", "Corporate-correct, complete sentences.", ["formal","classic","trust"], "Dear Ms. Johnson, we are pleased to confirm your roof repair appointment.", "Our crew will arrive on Tuesday at 8:00 a.m. Please let us know of any access requirements."),
  tone("tn_hype", "High-Energy Creator", "YouTube-style enthusiasm and hooks.", ["bold","playful","youtube","energetic"], "You will NOT believe what we found under this floor 😳", "Stick around to the end, the reveal is wild."),
  tone("tn_expert", "Calm Expert", "Explains the why, measured authority.", ["trust","technical","calm"], "The leak is coming from failed flashing, not the shingles.", "Fixing the flashing now prevents a much larger repair next rainy season."),
  tone("tn_storyteller", "Reflective Storyteller", "Slow, observational, a little poetic.", ["editorial","warm","calm","personal"], "Some mornings in Chiang Mai the mist doesn't lift until nine.", "That's when I like to walk the site and just listen."),
  tone("tn_witty", "Dry Wit", "Understated humor, still professional.", ["playful","direct","personal"], "Good news: the roof is fixed. Bad news: no more indoor waterfall.", "Invoice attached. No charge for the jokes."),
  tone("tn_bilingual", "Bilingual Friendly", "English with natural Thai touches.", ["thai","friendly","warm","bilingual"], "Sawasdee krab! Your unit inspection is all set for Friday.", "Khob khun for your patience. Any questions, just message me."),
  tone("tn_data", "Data-First Report", "Numbers and bullets, minimal adjectives.", ["technical","direct","efficient","minimal"], "Occupancy 94% (+3% MoM). 2 open work orders, both under 48h.", "Next action: renew Unit 4B lease by Oct 30."),
  tone("tn_luxe", "Quiet Luxury Concierge", "Discreet, gracious, premium service.", ["luxe","formal","calm"], "Your residence has been prepared for your arrival.", "Should you require anything at all, I remain at your disposal."),
  tone("tn_coach", "Encouraging Coach", "Supportive, motivating, plain-spoken.", ["friendly","energetic","warm"], "You're closer than you think. Your permit is 80% done.", "Let's knock out the last two documents this week. I've got you."),
  tone("tn_nononsense", "No-Nonsense Contractor", "Plain talk, straight from the job site.", ["direct","industrial","raw","construction"], "Slab's poured. Framing starts Monday if weather holds.", "Need your tile pick by Friday or we slip a week."),
 ],
 "Home / Interior Style": [
  img("hm_japandi", "Japanese Minimal", "Tatami, low furniture, paper and timber calm.", ["minimal","natural","calm","japanese"], "int_japandi", ["#d8c8a8","#8c6e4a","#f2ede3"], ["tatami","paper","pale wood"]),
  img("hm_warm_modern", "Warm Modern Luxe", "Layered lighting, neutral tones, hotel-like comfort.", ["luxe","warm","modern","soft"], "int_boho", ["#e9e1d6","#a68a6d","#4a4038"], ["linen","walnut","brass"]),
  img("hm_cabin", "Rustic Cabin", "Hand-hewn logs, old wood, cosy and lived-in.", ["rustic","warm","craft","traditional"], "int_cabin", ["#7a5230","#c9a77c","#3b2a1a"], ["logs","iron","wool"]),
  img("hm_brutalist", "Brutalist Concrete", "Board-formed concrete, bold geometric mass.", ["industrial","bold","raw","modern"], "int_concrete", ["#8e8e8a","#bdbcb6","#2b2b2b"], ["concrete","glass","steel"]),
  img("hm_brick_loft", "Brick Warehouse Loft", "Converted industrial brick with big steel windows.", ["industrial","rustic","urban","warm"], "int_industrial", ["#9c4a2f","#2e2e2e","#d8c3a5"], ["brick","steel","timber"]),
  img("hm_minimal_white", "Simple White Minimal", "Light, clean, practical. Rental-friendly.", ["minimal","light","practical","modern"], "int_modernkitchen", ["#ffffff","#d9d9d9","#2b2b2b"], ["laminate","matte white","black fixtures"]),
  img("hm_midcentury", "Mid-Century Modern", "Open beams, glass walls, 1960s California.", ["classic","modern","warm","retro"], "int_midcentury", ["#c47a3a","#2f4f4f","#f0e2c8"], ["teak","glass","stone"]),
  img("hm_thai_teak", "Traditional Thai Teak House", "Raised stilts, steep gables, teak panels.", ["thai","traditional","natural","craft"], "int_thai", ["#6b4226","#3b2a1a","#e8dcc2"], ["teak","stilts","palm"]),
  img("hm_tropical_villa", "Tropical Pool Villa", "Open-air sala, pool deck, thatch and timber.", ["tropical","luxe","natural","resort"], "ext_tropical", ["#2fa4a9","#a0522d","#f4ecd8"], ["thatch","teak","stone"]),
  img("hm_glass_box", "Glass-Box Modernist", "Pure lines, floating floors, nature as the wall.", ["minimal","modern","luxe","architectural"], "ext_modern", ["#ffffff","#2f4f2f","#9e9e9e"], ["steel","glass","travertine"]),
  img("hm_craftsman", "Craftsman Bungalow", "Deep porch, tapered columns, honest woodwork.", ["classic","craft","warm","traditional"], "ext_craftsman", ["#5c4a3a","#a39171","#efe6d2"], ["shingle","fir","river rock"]),
  img("hm_spanish", "Spanish Colonial Revival", "Stucco, clay tile, arches and courtyards.", ["warm","classic","rustic","mediterranean"], "ext_spanish", ["#d9b38c","#a0522d","#4b6043"], ["stucco","clay tile","iron"]),
  img("hm_artdeco", "Art Deco Detail", "Geometry, curves, terrazzo and polished metal.", ["luxe","bold","geometric","classic"], "int_artdeco", ["#1b1b1b","#c9a227","#f2efe8"], ["terrazzo","brass","lacquer"]),
  mood("hm_scandi", "Scandinavian Light", "Pale birch, white walls, wool throws, hygge.", ["minimal","light","natural","soft"], ["#f7f5f0","#e3d9c6","#c2a878","#9aa5a0","#3a3a3a"], ["birch","wool","linen","white oak"]),
  mood("hm_coastal", "Coastal Breezy", "Whitewash, rattan, sea-glass blues.", ["light","tropical","calm","natural"], ["#ffffff","#cfe8ef","#7fb7c9","#d8c3a5","#2c5d73"], ["rattan","whitewash","linen","driftwood"]),
  mood("hm_boho", "Bohemian Eclectic", "Plants, layered rugs, macramé, collected treasures.", ["playful","warm","eclectic","natural"], ["#c1502e","#e9c46a","#2a9d8f","#f4a261","#264653"], ["jute","macramé","terracotta","plants"]),
 ],
 "Logo / Mark": [
  logo("lg_monogram_circle", "Circle Monogram", "Single 'W' in a solid circle. Clean, app-icon ready.", ["minimal","modern","geometric","bold"], "W", "Weberman", "montserrat", "#ffffff", "#111111", "circle", 800),
  logo("lg_serif_wordmark", "Serif Wordmark", "Elegant spaced serif name, no symbol.", ["classic","luxe","formal","editorial"], "", "Weberman", "cormorant", "#1b1b1b", "#f7f3ea", "none", 600, "0.25em"),
  logo("lg_construction_badge", "Construction Badge", "Shield badge, heavy caps, 'EST.' energy.", ["industrial","bold","traditional","construction"], "W", "Weberman Co.", "archivo", "#ffffff", "#ff6b00", "shield", 400, "0.04em"),
  logo("lg_lowercase", "Friendly Lowercase", "Rounded lowercase wordmark with a dot accent.", ["friendly","modern","playful","soft"], "", "weberman.", "montserrat", "#2b2d42", "#edf2f4", "none", 800, "-0.02em", False, False, "#ef8354"),
  logo("lg_blueprint", "Blueprint Line Mark", "Outlined 'W' like a technical drawing.", ["technical","minimal","cool","architectural"], "W", "Weberman", "grotesk", "#ffffff", "#0b3d91", "outline", 500, "0.1em"),
  logo("lg_stamp", "Hand Stamp / Seal", "Thai-seal-inspired red square chop.", ["thai","craft","traditional","bold"], "W", "Weberman", "dmserif", "#ffffff", "#a4161a", "square", 400, "0.05em"),
  logo("lg_gold_crest", "Black & Gold Crest", "Gold monogram in thin ring on black.", ["luxe","dark","classic","formal"], "W", "Weberman", "playfair", "#c9a227", "#0b0b0b", "ring", 700, "0.2em"),
  logo("lg_stencil", "Stencil Industrial", "Spray-stencil caps, job-site crates.", ["industrial","raw","bold","construction"], "", "WEBERMAN", "bebas", "#2b2d31", "#ffd400", "none", 400, "0.12em"),
  logo("lg_signature", "Personal Signature", "Hand-signed name, creator/personal brand feel.", ["personal","warm","playful","casual"], "", "Max Weberman", "caveat", "#1b1b1b", "#fffaf0", "none", 700, "0", False, False),
  logo("lg_leaf", "Organic Leaf Mark", "Soft green rounded square with leaf-like 'W'.", ["natural","friendly","soft","tropical"], "W", "Weberman", "fraunces", "#ffffff", "#3a7d44", "rounded", 700, "0.02em"),
  logo("lg_split", "Split Geometric", "Two-tone diagonal square, modern holding-company look.", ["geometric","modern","bold","corporate"], "W", "WEBERMAN GROUP", "grotesk", "#ffffff", "#1d3c6e", "split", 700, "0.12em", False, True, "#b08d57"),
  logo("lg_mono_text", "Mono Terminal Tag", "Code-style handle: >_ weberman", ["technical","minimal","raw","dark"], ">_", "weberman", "plexmono", "#39ff14", "#050805", "none", 600, "0", False, False),
 ],
 "Photography Style": [
  img("ph_golden", "Golden Hour Warm", "Warm, glowing, sun-low tones.", ["warm","vibrant","natural","cinematic"], "base_temple", [], [], "sepia(.35) saturate(1.4) brightness(1.05) contrast(1.05)"),
  img("ph_bw", "Black & White Documentary", "Grainy contrasty monochrome.", ["classic","raw","editorial","minimal"], "base_temple", [], [], "grayscale(1) contrast(1.35)"),
  img("ph_faded", "Faded Film", "Lifted blacks, low contrast, nostalgic.", ["soft","retro","calm","editorial"], "base_temple", [], [], "contrast(.75) brightness(1.12) saturate(.7) sepia(.15)"),
  img("ph_punchy", "Punchy Vivid", "High saturation, YouTube-pop colors.", ["vibrant","bold","youtube","energetic"], "base_temple", [], [], "saturate(1.9) contrast(1.2)"),
  img("ph_cool_teal", "Teal & Cool Cinematic", "Cool shadows, desaturated, moody.", ["cool","cinematic","dark","modern"], "base_temple", [], [], "hue-rotate(-12deg) saturate(.8) brightness(.9) contrast(1.15)"),
  img("ph_natural", "True-To-Life Natural", "Honest color, no grading. What you see.", ["natural","minimal","trust","neutral"], "base_temple", [], [], None),
  img("ph_site_raw", "Gritty Job-Site Raw", "Harsh, desaturated, real work in progress.", ["industrial","raw","construction","direct"], "base_site", [], [], "saturate(.55) contrast(1.3) brightness(.95)"),
  img("ph_site_clean", "Clean Commercial", "Bright, crisp, brochure-ready.", ["light","corporate","clean","trust"], "base_site", [], [], "brightness(1.15) contrast(1.05) saturate(1.1)"),
  img("ph_site_dramatic", "Dramatic Dark Contrast", "Deep shadows, punchy highlights.", ["bold","dark","cinematic","luxe"], "base_site", [], [], "brightness(.75) contrast(1.6) saturate(1.1)"),
  img("ph_site_warm_film", "Warm Film Grain", "Kodak-ish warmth on real work.", ["warm","retro","craft","natural"], "base_site", [], [], "sepia(.4) contrast(1.1) saturate(1.1)"),
 ],
 "Fashion / Personal Look": [
  mood("fs_workwear", "Rugged Workwear", "Canvas jackets, work boots, denim, utility pockets.", ["rugged","industrial","practical","construction"], ["#7a5c3a","#2f3e46","#c2a878","#1b1b1b","#e9e2d0"], ["duck canvas","denim","leather boots"]),
  mood("fs_linen", "Tropical Linen", "Relaxed linen shirts, sandals, light neutrals.", ["tropical","relaxed","natural","light"], ["#f4efe6","#d8c8a8","#9caf88","#c1502e","#ffffff"], ["linen","cotton","leather sandals"]),
  mood("fs_smart_casual", "Smart Casual", "Oxford shirt, chinos, clean sneakers.", ["classic","clean","trust","modern"], ["#1d3c6e","#ffffff","#c8b593","#6c757d","#2b2b2b"], ["oxford cotton","chino","suede"]),
  mood("fs_all_black", "All-Black Minimal", "Black tee, black trousers, one good watch.", ["minimal","dark","modern","bold"], ["#000000","#1c1c1c","#3a3a3a","#c0c0c0","#ffffff"], ["merino","technical cotton","steel watch"]),
  mood("fs_outdoor", "Outdoor Tech", "Performance fabrics, hiking shoes, caps.", ["technical","practical","natural","active"], ["#355e3b","#ff6b00","#2b2d31","#a3b18a","#f8f9fa"], ["ripstop","merino","Gore-Tex"]),
  mood("fs_tailored", "Tailored Sharp", "Unstructured blazer, polo, loafers.", ["formal","luxe","classic","polished"], ["#0f2340","#e8dcc2","#5c4033","#b08d57","#ffffff"], ["wool","silk-knit","leather loafers"]),
  mood("fs_streetwear", "Creator Streetwear", "Graphic tees, overshirts, bold sneakers.", ["playful","bold","youtube","urban"], ["#ff006e","#3a86ff","#ffbe0b","#1b1b1b","#ffffff"], ["heavy cotton","nylon","rubber"]),
  mood("fs_thai_fusion", "Thai Fusion", "Mor hom indigo, local textiles, modern cuts.", ["thai","craft","natural","personal"], ["#1f3b73","#2c2c54","#d4a017","#e8dcc2","#7a5230"], ["indigo cotton","handwoven silk","teak buttons"]),
  mood("fs_heritage", "Heritage Americana", "Flannel, raw denim, leather belt, boots.", ["rustic","classic","warm","traditional"], ["#8c1c13","#1b3a5c","#c19a6b","#3b2a1a","#efe6d2"], ["flannel","selvedge denim","bridle leather"]),
  mood("fs_resort", "Quiet Luxury Resort", "Knit polos, soft trousers, muted tones.", ["luxe","soft","calm","minimal"], ["#e9e1d6","#c8b593","#7d8c7a","#ffffff","#4a4038"], ["cashmere-cotton","knit","suede"]),
 ],
 "YouTube Thumbnail Style": [
  thumb("yt_bigtext", "Big Bold Text", "Huge 2–3 word caption, high contrast.", ["bold","loud","youtube","vibrant"], "#111", "#ffffff", "#ffd400", "bebas", "bigtext", "THAI HOUSE BUILD", "base_temple", "saturate(1.5) contrast(1.2)"),
  thumb("yt_minimal", "Minimal Cinematic", "No text, one striking frame, letterbox bars.", ["minimal","cinematic","editorial","calm"], "#000", "#ffffff", "#ffffff", "inter", "cinematic", "", "base_temple", "contrast(1.1) saturate(.85)"),
  thumb("yt_split", "Before / After Split", "Two halves with arrow. Transformation story.", ["construction","bold","clear","youtube"], "#111", "#ffffff", "#ff6b00", "archivo", "split", "BEFORE → AFTER", "base_site", None),
  thumb("yt_documentary", "Documentary Title Card", "Serif title in lower third, calm and premium.", ["editorial","classic","calm","cinematic"], "#000", "#f2ead8", "#c9a227", "playfair", "lower", "A Moment in Thai", "base_temple", "sepia(.25) contrast(1.05)"),
  thumb("yt_vlog", "Personal Vlog Face", "Big expressive face circle + short caption.", ["personal","playful","friendly","youtube"], "#ff6f59", "#ffffff", "#ffd400", "montserrat", "face", "I MOVED HERE", "base_temple", None),
  thumb("yt_number", "Number / Listicle", "Big number badge, curiosity hook.", ["bold","direct","youtube","clear"], "#0b3d91", "#ffffff", "#ffd166", "archivo", "number", "7", "base_site", "saturate(1.2)"),
  thumb("yt_handwritten", "Handwritten Journal", "Script note over warm photo, diary feel.", ["warm","personal","craft","soft"], "#f6f0e4", "#ffffff", "#ffffff", "caveat", "hand", "rainy season diaries", "base_temple", "sepia(.3) brightness(1.05)"),
  thumb("yt_bilingual", "Bilingual Caption", "English + Thai text stack, local flavour.", ["thai","bilingual","friendly","vibrant"], "#a4161a", "#ffffff", "#d4a017", "prompt", "bilingual", "BUILDING IN THAILAND|สร้างบ้านในไทย", "base_temple", "saturate(1.2)"),
 ],
 "Icon & Illustration Style": [
  mood("ic_line", "Thin Line Icons", "1.5px stroke, outlined, airy.", ["minimal","light","modern","technical"], ["#111111","#ffffff","#e5e5e5"], ["⌂ outline","◯ stroke","△ line"]),
  mood("ic_filled", "Solid Filled Icons", "Chunky filled shapes, high legibility.", ["bold","friendly","clear","modern"], ["#2563eb","#ffffff","#1f2937"], ["■ solid","● fill","▲ bold"]),
  mood("ic_duotone", "Duotone Icons", "Two-tone shapes with soft secondary fill.", ["modern","soft","friendly","vibrant"], ["#7c3aed","#c4b5fd","#ffffff"], ["◐ duo","◑ tone","◒ layer"]),
  mood("ic_handdrawn", "Hand-Drawn Sketch", "Pencil/ink doodles, imperfect and human.", ["craft","personal","warm","playful"], ["#3a2e22","#f6f0e4","#b5651d"], ["✎ sketch","✐ ink","✍ doodle"]),
  mood("ic_isometric", "Isometric 3D", "Little 3D buildings and tools, tech-forward.", ["technical","playful","geometric","construction"], ["#00b4d8","#ffd166","#ef476f","#073b4c"], ["◇ iso","⬡ block","▱ plane"]),
  mood("ic_blueprint", "Blueprint Technical", "Architectural line drawings in white on blue.", ["technical","architectural","cool","industrial"], ["#0b3d91","#ffffff","#ffd166"], ["⊞ plan","⊿ section","⌖ detail"]),
  mood("ic_flat_illus", "Flat Illustration", "Friendly flat people & scenes, corporate-cheerful.", ["friendly","playful","corporate","vibrant"], ["#ff9f1c","#2ec4b6","#e71d36","#011627"], ["☺ people","☀ scene","☂ objects"]),
  mood("ic_thai_ornament", "Thai Ornamental", "Kranok-inspired flourishes as accents.", ["thai","traditional","luxe","craft"], ["#d4a017","#a4161a","#1b1b1b"], ["❦ kranok","✾ lotus","❀ motif"]),
 ],
}

# ---- Expanded pool (added 2026-10-09) ----
F.update({
    "kanit": "'Kanit', 'Prompt', system-ui, sans-serif",
    "mitr": "'Mitr', 'Prompt', system-ui, sans-serif",
    "chakra": "'Chakra Petch', 'Space Grotesk', system-ui, sans-serif",
    "pridi": "'Pridi', 'Lora', Georgia, serif",
    "notoserifjp": "'Noto Serif JP', 'Hiragino Mincho ProN', Georgia, serif",
    "notosansjp": "'Noto Sans JP', 'Hiragino Sans', system-ui, sans-serif",
    "dmsans": "'DM Sans', 'Inter', system-ui, sans-serif",
    "syne": "'Syne', 'Space Grotesk', system-ui, sans-serif",
    "anton": "'Anton', 'Bebas Neue', Impact, sans-serif",
    "nunito": "'Nunito', 'Inter', system-ui, sans-serif",
    "outfit": "'Outfit', 'Inter', system-ui, sans-serif",
    "spacemono": "'Space Mono', ui-monospace, Menlo, monospace",
    "manrope": "'Manrope', 'Inter', system-ui, sans-serif",
})

def tone2(i, label, desc, tags, s1, s2, frm="Tagline"):
    o = tone(i, label, desc, tags, s1, s2); o["visual"]["from"] = frm; return o

def hero(i, label, desc, tags, bg, fg, accent, font, layout, head, sub, cta, key=None, filt=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="hero", bg=bg, fg=fg, accent=accent,
                font=F[font], layout=layout, head=head, sub=sub, cta=cta, key=key, filter=filt))

def post(i, label, desc, tags, bg, fg, accent, font, layout, text, key=None, filt=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="post", bg=bg, fg=fg, accent=accent,
                font=F[font], layout=layout, text=text, key=key, filter=filt))

def pace(i, label, desc, tags, cuts, colors, notes):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="pace", cuts=cuts, colors=colors, notes=notes))

def merch(i, label, desc, tags, item, base, ink, mark, font, accent=None):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=dict(type="merch", item=item, base=base, ink=ink,
                mark=mark, font=F[font], accent=accent or ink))

POOL_EXTRA = {
 "App / UI Style": [
  ui("ui_rice_paper", "Rice Paper Thai", "Cream paper tones, Kanit headings, teak-brown accents.", ["thai","warm","light","natural"], "#f7f1e3","#fffaf0","#3b2a1a","#8b5a2b",10,"kanit","soft","1px solid #eadfc8"),
  ui("ui_jobsite", "Job-Site Tablet", "Huge touch targets, hi-vis orange on concrete grey. Works with gloves on.", ["industrial","direct","practical","light"], "#d9dcd6","#f4f4f1","#1f1f1f","#ff6b00",6,"archivo","hard","2px solid #1f1f1f"),
  ui("ui_bento", "Bento Grid", "Modular tiles of different sizes, tidy Japanese-box layout.", ["japanese","minimal","modern","light"], "#f2f0eb","#ffffff","#222222","#d1495b",16,"dmsans","soft","1px solid #e4e1da"),
  ui("ui_sunlit_linen", "Sunlit Linen", "Off-white linen texture, sage accent, airy spacing.", ["natural","light","calm","soft"], "#f6f3ec","#fbfaf6","#3f4540","#7d9a6f",14,"outfit","soft"),
  ui("ui_kraft", "Kraft Cardboard", "Brown kraft background, stamped black type, no gloss.", ["craft","rustic","warm","raw"], "#c8a97e","#d8bf96","#1b1b1b","#1b1b1b",2,"spacemono","none","2px solid #1b1b1b"),
  ui("ui_bilingual_dash", "Bilingual Dashboard", "Every label in English and Thai, Sarabun body, calm teal.", ["bilingual","thai","practical","friendly"], "#eef6f5","#ffffff","#16302e","#139a8f",12,"sarabun","soft"),
  ui("ui_clinic_mint", "Clinical Mint", "Mint and white, very clean, hospital-grade calm.", ["light","cool","clean","trust"], "#f0faf6","#ffffff","#12372a","#2bb673",10,"manrope","soft","1px solid #d6efe4"),
  ui("ui_y2k", "Y2K Chrome", "Chrome gradients, bubbly buttons, retro-futurist.", ["playful","retro","vibrant","bold"], "linear-gradient(135deg,#d7e1ec,#a6b3c4,#f0f4f8)","rgba(255,255,255,.7)","#1a1a40","#8a2be2",20,"syne","soft","1px solid #fff"),
  ui("ui_bauhaus", "Bauhaus Color Blocks", "Primary red, blue, yellow blocks on a strict grid.", ["bold","geometric","vibrant","playful"], "#f4f1e8","#ffffff","#111111","#1d4ed8",0,"outfit","hard","2px solid #111"),
  ui("ui_monsoon", "Monsoon Slate", "Slate blue-grey with rain-teal highlights.", ["cool","calm","natural","modern"], "#dfe6ea","#f3f6f8","#253237","#3d8a99",12,"inter","soft"),
  ui("ui_chalkboard", "Chalkboard Sketch", "Deep-green board, handwritten labels, chalky lines.", ["playful","craft","dark","personal"], "#24382f","#2e463b","#f0f0e8","#f9e79f",8,"caveat","none","1px dashed rgba(255,255,255,.5)"),
  ui("ui_dune", "Desert Dune Gradient", "Peach-to-sand gradient, soft rounded white cards.", ["warm","soft","light","modern"], "linear-gradient(160deg,#ffd8b8,#f6e7d0)","rgba(255,255,255,.85)","#4a3426","#e07a3f",18,"nunito","soft"),
 ],
 "Color Palette": [
  pal("pal_mango_sticky", "Mango Sticky Rice", "Mango yellow, coconut cream, pandan green, palm-sugar brown.", ["thai","warm","tropical","playful"], ["#f6b93b","#fff5e1","#3c8d2f","#6b4226","#ffffff"]),
  pal("pal_tuk_tuk", "Tuk-Tuk Neon", "Cyan, hot pink, taxi yellow on black.", ["bangkok","vibrant","bold","urban"], ["#00a8e8","#ff006e","#ffd60a","#1b1b1b","#ffffff"]),
  pal("pal_rebar", "Rebar & Rust", "Oxide rust, burnt orange, steel grey, cement.", ["industrial","raw","warm","construction"], ["#8b3a1a","#b5651d","#4a4a48","#a9a9a2","#e8e4dc"]),
  pal("pal_coconut", "Coconut Husk", "Coconut milk, husk tan, shell brown, palm green.", ["natural","light","tropical","warm"], ["#f7f1e3","#c8a97e","#6b4f2a","#3e5641","#ffffff"]),
  pal("pal_monsoon_sky", "Monsoon Sky", "Storm slate, rain blue, mist, cloud white.", ["cool","calm","natural","soft"], ["#253237","#5c6b73","#9db4c0","#c2dfe3","#e0fbfc"]),
  pal("pal_jasmine", "Jasmine Rice", "Near-white, rice cream, straw, soft leaf.", ["light","minimal","natural","soft"], ["#fffdf7","#f3ead3","#d9cba3","#a3b18a","#4a4a3a"]),
  pal("pal_lotus", "Lotus Pond", "Lotus pink, deep rose, pad green, lime, pond-white.", ["thai","natural","soft","playful"], ["#f4a6b7","#e56b8a","#3a7d44","#a7c957","#f7f7f2"]),
  pal("pal_mohom", "Mor Hom Indigo", "Indigo farmer's shirt blue, faded denim, cotton, teak.", ["thai","craft","cool","natural"], ["#1f3b73","#3e5c99","#a8b8d8","#f3efe6","#b5651d"]),
  pal("pal_laterite", "Laterite Earth", "Red laterite, ochre, rice-field green, wheat, soil.", ["earthy","warm","rustic","natural"], ["#a0522d","#cd853f","#6b8e23","#f5deb3","#3b2a1a"]),
  pal("pal_galvanized", "Galvanized Steel", "Zinc greys with one caution-yellow accent.", ["industrial","cool","technical","light"], ["#2f3a40","#9aa5ab","#c5ccd0","#e9ecee","#f2a900"]),
  pal("pal_papaya", "Green Papaya", "Papaya green, lime, ripe orange, cream, leaf shadow.", ["tropical","vibrant","fresh","natural"], ["#83b735","#c6e377","#ff8c42","#fff4e0","#2d4a22"]),
  pal("pal_sakura", "Sakura Dusk", "Cherry blossom pinks fading into evening blue.", ["japanese","soft","calm","light"], ["#f8c8d8","#e4a3b8","#6d597a","#355070","#fdf6f0"]),
  pal("pal_nordic_frost", "Nordic Frost", "Ice white, frost blue, fjord grey.", ["cool","minimal","light","calm"], ["#ffffff","#eef3f7","#cad8e4","#8aa4bd","#34495e"]),
  pal("pal_chili_lime", "Chili & Lime", "Bird's-eye chili red, orange, lime, deep navy.", ["bold","vibrant","playful","thai"], ["#d62828","#f77f00","#fcbf49","#a4c639","#003049"]),
  pal("pal_khaki_field", "Field Khaki", "Khaki, olive drab, canvas, charcoal.", ["practical","earthy","rugged","natural"], ["#c3b091","#8a7f5a","#4b5320","#e8e2d0","#2b2b2b"]),
 ],
 "Typography": [
  typ("ty_kanit", "Kanit Bold Thai Sans", "Kanit headings: the modern Bangkok signage look, great with Thai script.", ["thai","bold","modern","bilingual"], "kanit","sarabun",700),
  typ("ty_chakra", "Chakra Petch Techno", "Angular Thai-designed sans, engineering edge.", ["technical","thai","bold","industrial"], "chakra","inter",700,True,"0.04em"),
  typ("ty_pridi", "Pridi Thai Serif", "Soft Thai-friendly serif for storytelling.", ["thai","warm","editorial","calm"], "pridi","sarabun",600),
  typ("ty_dmsans", "DM Sans Friendly Geometric", "Low-contrast geometric sans, approachable.", ["friendly","modern","light","clean"], "dmsans","dmsans",700),
  typ("ty_syne", "Syne Art-School", "Wide, quirky display face with gallery energy.", ["bold","playful","editorial","experimental"], "syne","inter",800),
  typ("ty_anton", "Anton Poster", "Tall heavy poster caps. Reads from across a job site.", ["loud","bold","industrial","direct"], "anton","worksans",400,True,"0.02em"),
  typ("ty_nunito", "Nunito Rounded", "Rounded terminals, soft and kind.", ["friendly","soft","playful","light"], "nunito","nunito",800),
  typ("ty_notoserifjp", "Noto Serif JP Calm", "Japanese Mincho-style serif, quiet and literary.", ["japanese","calm","editorial","minimal"], "notoserifjp","notosansjp",600),
  typ("ty_outfit", "Outfit Clean Geometric", "Crisp modern geometric, startup-clean.", ["modern","minimal","light","friendly"], "outfit","outfit",700),
  typ("ty_spacemono", "Space Mono Retro-Tech", "Quirky monospace with a 70s-computer feel.", ["technical","retro","raw","playful"], "spacemono","inter",700),
  typ("ty_manrope", "Manrope Practical Sans", "Neutral, efficient, slightly technical.", ["practical","modern","neutral","direct"], "manrope","manrope",800),
  typ("ty_mitr", "Mitr Rounded Thai", "Rounded Thai sans, friendly and bilingual-ready.", ["thai","friendly","playful","bilingual"], "mitr","sarabun",500),
 ],
 "Business Communication Tone": [
  tone("tn_site_update", "Site Update Bullets", "Checklist-style status, zero padding.", ["direct","practical","construction","efficient"], "Today: footing rebar inspected ✓. Pour Thursday 7am.", "Photos attached. Nothing needed from you."),
  tone("tn_neighborly", "Neighborly Landlord", "Casual, considerate, like a good neighbor.", ["warm","friendly","personal","casual"], "Hey Tom, quick one: water's off 10 to noon tomorrow for a pipe fix.", "Sorry for the hassle, I'll text when it's back on."),
  tone("tn_transparent", "Radically Transparent", "Bad news first, with the plan attached.", ["trust","direct","honest","calm"], "Honest update: we're 4 days behind because of the rain.", "Here's the new schedule. Cost to you: nothing."),
  tone("tn_teacher", "Patient Teacher", "Uses analogies, explains the why.", ["calm","technical","friendly","educational"], "Think of the vapor barrier as a raincoat for your walls.", "In Bangkok's humidity, it's the difference between 5 years and 30."),
  tone("tn_two_word", "Two-Word SMS", "As short as humanly possible.", ["minimal","direct","efficient","raw"], "Done. ✓", "Invoice sent."),
  tone("tn_thai_polite", "Polite Thai-English", "Thai politeness particles, gentle and respectful.", ["thai","bilingual","warm","polite"], "Khun Somchai krab, the contract is ready for your review.", "Please take your time. Happy to explain anything krab."),
  tone("tn_explorer", "Curious Explorer", "Wonder-driven, adventurous, first person.", ["playful","energetic","personal","adventurous"], "Took a wrong turn outside Nan and found the best khao soi of my life.", "Then I found the guy who built the restaurant. By hand."),
  tone("tn_plain_quote", "Plain-Number Quote", "Price and timeline, no adjectives.", ["direct","technical","trust","efficient"], "Kitchen remodel: 380,000 THB, 6 weeks.", "Price is fixed unless the scope changes."),
  tone("tn_humble", "Humble Builder", "Small-crew pride, quiet confidence.", ["warm","craft","calm","personal"], "We're a small crew, and we like it that way.", "Every joint gets the same care, whether you see it or not."),
  tone("tn_bold_promise", "Bold Guarantee", "Confident promise, high stakes.", ["bold","direct","energetic","confident"], "On time, or the last week is free.", "That's how sure we are."),
  tone("tn_gentle", "Gentle Reminder", "Soft, empathetic nudges.", ["soft","friendly","calm","warm"], "Just a gentle nudge: rent is due on the 5th.", "If anything's tight this month, let's talk."),
 ],
 "Home / Interior Style": [
  mood("hm_thai_pavilion", "Modern Thai Pavilion", "Steep gables, open sala, teak screens, modern glass.", ["thai","tropical","natural","modern"], ["#6b4226","#c8a97e","#f4ecd8","#3e5641","#ffffff"], ["teak screens","open sala","clay roof tiles"]),
  mood("hm_shophouse", "Bangkok Shophouse Reno", "Narrow old shophouse, exposed brick, steel stairs, plants.", ["industrial","bangkok","urban","warm"], ["#9c4a2f","#2e2e2e","#d8c3a5","#5a7d4f","#f2efe8"], ["old brick","black steel","terrazzo"]),
  mood("hm_lime_plaster", "Earth & Lime Plaster", "Hand-troweled walls, rounded edges, warm limewash.", ["natural","warm","craft","calm"], ["#e8dccb","#c9b49a","#a68a6d","#f6f1ea","#6b5b4b"], ["limewash","clay","linen"]),
  mood("hm_wabi", "Wabi-Sabi", "Imperfect, aged, quiet beauty.", ["japanese","natural","calm","raw"], ["#d6cfc4","#a39b8b","#6e6658","#3e3a33","#f2eee8"], ["aged wood","stoneware","washi"]),
  mood("hm_stilt", "Raised Stilt House", "Lifted off the ground for breeze and floods, shaded underneath.", ["tropical","thai","natural","light"], ["#8c6e4a","#d8c8a8","#4e7d4a","#f7f3ea","#2b2b2b"], ["stilts","louvers","hammock space"]),
  mood("hm_bamboo", "Bamboo Architecture", "Curving bamboo structure, thatch, open air.", ["natural","craft","tropical","organic"], ["#c9b26b","#8a7a3c","#4e5d2c","#f1ead1","#3b2f1e"], ["bamboo","alang-alang thatch","rattan"]),
  mood("hm_container", "Shipping-Container Home", "Corten boxes, big glazing, efficient.", ["industrial","raw","practical","modern"], ["#a0522d","#2f3e46","#c5ccd0","#f4f4f1","#ff6b00"], ["corrugated steel","plywood","glass"]),
  mood("hm_rammed_earth", "Rammed Earth Modern", "Layered earth walls, flat roofs, warm and solid.", ["earthy","natural","modern","warm"], ["#b9825a","#d4a373","#8c5a3c","#efe1cf","#3d3a2e"], ["rammed earth","concrete","oak"]),
  mood("hm_white_courtyard", "White Courtyard House", "Whitewashed walls around a planted courtyard.", ["light","minimal","calm","mediterranean"], ["#ffffff","#f1ece2","#9caf88","#c1502e","#4a4a4a"], ["whitewash","terracotta","olive tree"]),
  mood("hm_aframe", "A-Frame Cabin", "Steep triangle roof, loft bed, woodstove.", ["rustic","cozy","natural","playful"], ["#5c4033","#a0784e","#2f4f2f","#efe6d8","#c1502e"], ["cedar","wool","cast iron"]),
  mood("hm_tropical_colonial", "Tropical Colonial Veranda", "Wraparound veranda, shutters, ceiling fans.", ["classic","tropical","warm","formal"], ["#ffffff","#2f5d3a","#c8a97e","#1b1b1b","#e9e1d6"], ["shutters","rattan","marble"]),
  mood("hm_maximalist", "Maximalist Pattern", "Clashing prints, bold color, more is more.", ["bold","playful","vibrant","eclectic"], ["#e63946","#f4a261","#2a9d8f","#7b2cbf","#ffbe0b"], ["wallpaper","velvet","patterned tile"]),
 ],
 "Logo / Mark": [
  logo("lg_roofline", "Roofline Mark", "'W' tucked under a simple roof peak.", ["construction","friendly","modern","clean"], "W", "Weberman", "montserrat", "#b5651d", "#fbf6ee", "house", 800),
  logo("lg_bilingual_word", "Bilingual Wordmark", "English name with Thai script beneath.", ["thai","bilingual","modern","friendly"], "", "Weberman|เวเบอร์แมน", "kanit", "#1b1b1b", "#f4ecd8", "bilingual", 600, "0.04em", False, False, "#8b5a2b"),
  logo("lg_hex_bolt", "Hex Bolt Mark", "'W' inside a hex nut. Engineering through and through.", ["industrial","technical","bold","construction"], "W", "Weberman", "chakra", "#2f3a40", "#e9ecee", "hex", 700, "0.08em"),
  logo("lg_palm_line", "Palm Line Mark", "Thin green outlined 'W' like a palm frond sketch.", ["natural","tropical","minimal","light"], "W", "Weberman", "outfit", "#3a7d44", "#f6f3ec", "outline", 500, "0.12em"),
  logo("lg_travel_badge", "Round Travel Badge", "'A Moment In Thai' in a round souvenir badge.", ["personal","playful","retro","travel"], "AMIT", "A Moment In Thai", "bebas", "#f4ecd8", "#c1502e", "ring", 400, "0.1em"),
  logo("lg_mincho", "Mincho Brush Mark", "Japanese-serif 'W' in a vermillion square.", ["japanese","craft","calm","minimal"], "W", "Weberman", "notoserifjp", "#ffffff", "#d1495b", "square", 600, "0.2em"),
  logo("lg_underline", "Underlined Wordmark", "Plain bold name with one thick underline. Says what it is.", ["direct","minimal","practical","modern"], "", "WEBERMAN", "manrope", "#111111", "#ffffff", "underline", 800, "0.06em", False, True, "#ff6b00"),
  logo("lg_chakra_tech", "Techno Thai Mark", "Angular Chakra Petch caps with a cut corner.", ["technical","thai","bold","modern"], "W", "WEBERMAN", "chakra", "#ffffff", "#139a8f", "split", 700, "0.1em", False, True, "#0b3b3a"),
  logo("lg_kraft_ring", "Kraft Rubber Stamp", "Inky ring stamp on kraft paper.", ["craft","rustic","warm","raw"], "W", "Weberman · Built By Hand", "spacemono", "#1b1b1b", "#c8a97e", "ring", 700, "0.06em"),
  logo("lg_moment_dot", "A Moment Dot", "Lowercase handle with a sunset dot.", ["friendly","minimal","light","personal"], "", "a moment in thai.", "dmsans", "#2b2b2b", "#fff8f0", "none", 700, "-0.01em", False, False, "#f77f00"),
  logo("lg_mw", "MW Ligature", "M and W joined in one rounded tile.", ["modern","personal","geometric","clean"], "MW", "Max Weberman", "outfit", "#ffffff", "#2f5d3a", "rounded", 800, "0.04em"),
  logo("lg_sunrise", "Sunrise Arc", "Half sun rising behind the name.", ["warm","tropical","friendly","light"], "", "Weberman", "nunito", "#4a3426", "#fff4e6", "sun", 800, "0.02em", False, False, "#f6b93b"),
 ],
 "Photography Style": [
  img("ph_airy", "Bright & Airy", "Lifted exposure, soft contrast, breezy.", ["light","soft","natural","fresh"], "ext_tropical", [], [], "brightness(1.2) contrast(.88) saturate(.9)"),
  img("ph_tropical_pop", "Tropical Saturated", "Juicy greens and turquoise water.", ["tropical","vibrant","warm","bold"], "ext_tropical", [], [], "saturate(1.6) contrast(1.08) hue-rotate(-6deg)"),
  img("ph_matte_earth", "Matte Earth Tones", "Muted, earthy, slightly warm matte finish.", ["earthy","natural","calm","warm"], "ext_tropical", [], [], "sepia(.3) saturate(.8) contrast(.9) brightness(1.03)"),
  img("ph_cross", "Cross-Processed", "Shifted colors, retro lab mistake look.", ["retro","playful","bold","experimental"], "base_temple", [], [], "hue-rotate(25deg) saturate(1.4) contrast(1.2)"),
  img("ph_infrared", "Pink Infrared", "Surreal false-color foliage.", ["experimental","playful","vibrant","surreal"], "base_temple", [], [], "hue-rotate(160deg) saturate(1.3)"),
  img("ph_overcast", "Soft Overcast", "Flat gentle light, low saturation, quiet.", ["calm","soft","japanese","natural"], "int_japandi", [], [], "brightness(1.1) contrast(.85) saturate(.75)"),
  img("ph_archive", "Archival Sepia", "Old-print sepia, history-book feel.", ["classic","retro","thai","craft"], "int_thai", [], [], "sepia(.9) contrast(1.1)"),
  img("ph_highkey", "High-Key White", "Overexposed whites, minimal shadows.", ["light","minimal","clean","modern"], "ext_modern", [], [], "brightness(1.35) contrast(.85) saturate(.9)"),
  img("ph_low_sun", "Low Sun, Long Shadows", "Warm raking light on real work.", ["warm","cinematic","industrial","natural"], "base_site", [], [], "sepia(.25) saturate(1.3) contrast(1.25) brightness(.95)"),
  img("ph_honest_doc", "Honest Interior Doc", "Neutral, slightly muted, journalistic.", ["natural","trust","editorial","raw"], "int_cabin", [], [], "saturate(.85) contrast(1.05)"),
 ],
 "Fashion / Personal Look": [
  mood("fs_fisherman", "Fisherman Pants & Tee", "Wrap fisherman pants, plain tee, flip-flops.", ["thai","relaxed","tropical","natural"], ["#2f4858","#f2efe8","#c8a97e","#6b8f71","#1b1b1b"], ["cotton wrap pants","plain tee","flip-flops"]),
  mood("fs_linen_jacket", "Linen Shirt-Jacket", "Light linen overshirt over a tee, rolled sleeves.", ["natural","practical","light","warm"], ["#e9e2d0","#c3b091","#8a7f5a","#ffffff","#3b2a1a"], ["linen overshirt","tee","canvas sneakers"]),
  mood("fs_noragi", "Japanese Workwear", "Indigo noragi jacket, wide trousers, tabi-style shoes.", ["japanese","craft","natural","calm"], ["#1f3b73","#2c2c54","#e8dcc2","#5c4033","#f7f5ef"], ["sashiko indigo","hemp","tabi"]),
  mood("fs_gorpcore", "Gorpcore Trail", "Fleece, trail runners, bright technical accents.", ["technical","active","playful","outdoor"], ["#ff8c42","#3a86ff","#2b2d31","#a3b18a","#f8f9fa"], ["fleece","ripstop","trail runners"]),
  mood("fs_white_tee", "White Tee & Jeans Uniform", "Same outfit daily. Zero decisions.", ["minimal","light","practical","direct"], ["#ffffff","#3e5c99","#1b1b1b","#e5e5e5","#c8a97e"], ["heavy white tee","straight jeans","white sneakers"]),
  mood("fs_site_polo", "Smart Site Polo", "Branded polo, work pants, hi-vis accents, boots.", ["construction","practical","direct","industrial"], ["#2b2d31","#ff6b00","#c5ccd0","#ffffff","#6c757d"], ["piqué polo","stretch work pants","safety boots"]),
  mood("fs_surf", "Surf Casual", "Boardshorts, faded tees, sun-bleached colors.", ["tropical","relaxed","playful","light"], ["#00a6a6","#f0e6d2","#ff9f1c","#ffffff","#05668d"], ["boardshorts","slub cotton","sandals"]),
  mood("fs_knit", "Earthy Knitwear", "Chunky knits in oat, rust and moss.", ["warm","soft","natural","craft"], ["#e8dcc6","#b5651d","#6b7f3a","#5c4033","#f7f3ea"], ["wool knit","cord","suede boots"]),
  mood("fs_tonal_khaki", "Tonal Khaki", "Head-to-toe sand and khaki tones.", ["earthy","minimal","practical","natural"], ["#c3b091","#d8c8a8","#a39171","#efe6d2","#5c4a3a"], ["twill","canvas","suede"]),
  mood("fs_camp_collar", "Retro Camp Collar", "Printed camp-collar shirts, loose fit.", ["playful","retro","tropical","vibrant"], ["#f77f00","#2a9d8f","#e9c46a","#264653","#fff8e7"], ["rayon print","pleated trousers","loafers"]),
  mood("fs_athleisure", "Clean Athleisure", "Technical joggers, performance tee, minimal sneakers.", ["modern","active","minimal","light"], ["#f1f3f5","#adb5bd","#343a40","#ffffff","#4dabf7"], ["tech jersey","joggers","knit runners"]),
 ],
 "YouTube Thumbnail Style": [
  thumb("yt_question", "Question Hook", "One big provocative question.", ["direct","bold","youtube","curious"], "#111", "#ffffff", "#f6b93b", "kanit", "bigtext", "WHY BUILD HERE?", "ext_tropical", "saturate(1.3) contrast(1.1)"),
  thumb("yt_pin", "Map Pin Travel", "Location pin and place name over scenery.", ["tropical","travel","friendly","light"], "#139a8f", "#ffffff", "#ff6f59", "dmsans", "pin", "Nan Province", "base_temple", "brightness(1.08)"),
  thumb("yt_clean_white", "Clean White Caption", "Small, clean caption on a white tab.", ["minimal","light","calm","editorial"], "#ffffff", "#111111", "#111111", "dmsans", "tab", "Building a teak house", "int_thai", "sepia(.2)"),
  thumb("yt_progress", "Build Progress Bar", "Day counter with progress bar.", ["construction","direct","clear","practical"], "#111", "#ffffff", "#ff6b00", "anton", "progress", "DAY 47 / 120", "base_site", "saturate(1.1)"),
  thumb("yt_price", "Price Tag Reveal", "Sticker price tag in baht.", ["direct","bold","thai","youtube"], "#d62828", "#ffffff", "#ffd60a", "kanit", "price", "฿2.9M", "ext_tropical", "saturate(1.2)"),
  thumb("yt_duo", "Reaction Duo", "Two faces reacting plus a short line.", ["playful","personal","energetic","youtube"], "#3a86ff", "#ffffff", "#ffbe0b", "nunito", "face", "WE DID IT", "ext_modern", None),
  thumb("yt_film_frame", "Warm Film Frame", "Letterboxed warm frame, no text.", ["cinematic","warm","calm","natural"], "#000", "#ffffff", "#ffffff", "inter", "cinematic", "", "ext_tropical", "sepia(.35) saturate(1.2)"),
  thumb("yt_arrows", "Red Circles & Arrows", "Classic red circle highlighting a detail.", ["loud","playful","youtube","bold"], "#111", "#ffffff", "#ff1f1f", "anton", "arrows", "LOOK AT THIS", "base_site", "contrast(1.15)"),
  thumb("yt_th_vs_jp", "Thailand Vs Japan Split", "Two-country comparison split.", ["bold","comparison","bilingual","travel"], "#111", "#ffffff", "#d1495b", "kanit", "split", "THAI vs JAPAN", "int_japandi", None),
 ],
 "Icon & Illustration Style": [
  mood("ic_thai_line", "Thai-Motif Line Icons", "Thin line icons with a subtle kranok curl.", ["thai","minimal","craft","light"], ["#ffffff","#8b5a2b","#f4ecd8"], ["⌂ curl","❧ leaf","☸ wheel"]),
  mood("ic_sticker", "Die-Cut Stickers", "Thick white outline sticker icons.", ["playful","bold","vibrant","friendly"], ["#ff006e","#ffbe0b","#3a86ff","#ffffff"], ["★ sticker","♥ badge","⚑ flag"]),
  mood("ic_stamp", "Rubber Stamp Icons", "Inky, slightly misregistered stamp marks.", ["craft","rustic","raw","warm"], ["#c8a97e","#1b1b1b","#a4161a"], ["✪ stamp","✚ mark","✔ ink"]),
  mood("ic_pixel", "Pixel 8-Bit", "Chunky pixel-art icons.", ["retro","playful","technical","bold"], ["#1b1b1b","#39ff14","#ff006e","#00e5ff"], ["▦ pixel","▩ tile","▣ block"]),
  mood("ic_clay", "Soft 3D Clay", "Puffy pastel 3D icons.", ["soft","friendly","playful","modern"], ["#ffcdb2","#b5e48c","#a2d2ff","#ffffff"], ["● puff","◆ clay","▲ soft"]),
  mood("ic_construction_glyph", "Monoline Construction Glyphs", "Hard-hat, level, trowel in one consistent stroke.", ["industrial","technical","minimal","construction"], ["#2b2d31","#ff6b00","#f8f9fa"], ["⚒ tools","⛏ dig","⚙ gear"]),
  mood("ic_watercolor", "Watercolor Spots", "Loose watercolor blobs behind simple icons.", ["soft","natural","craft","warm"], ["#a3c4bc","#f2c6b4","#e9e4d8","#6b8f71"], ["❀ wash","☁ bleed","✿ bloom"]),
  mood("ic_emoji", "Native Emoji Only", "Just use emoji. Universal and zero effort.", ["friendly","practical","casual","playful"], ["#ffd60a","#ffffff","#2b2b2b"], ["🏠 home","🔧 fix","🌴 trip"]),
  mood("ic_mon", "Japanese Mon Crests", "Circular family-crest style icons.", ["japanese","geometric","craft","classic"], ["#1b1b1b","#ffffff","#d1495b"], ["◎ crest","❁ mon","⊛ seal"]),
 ],
}

POOL_EXTRA.update({
 "Brand Voice & Taglines": [
  tone2("bv_built_to_last", "Built To Last", "Classic durability promise.", ["direct","trust","construction","classic"], "Built to last.", "Weberman Construction · Thailand"),
  tone2("bv_one_moment", "One Moment At A Time", "Slow, personal channel voice.", ["calm","personal","warm","editorial"], "One moment at a time.", "Slow travel and honest building in Thailand."),
  tone2("bv_no_surprises", "No Surprises", "Reliability as the whole brand.", ["direct","trust","practical","minimal"], "No surprises. Just good buildings.", "Fixed prices. Real schedules. Straight answers."),
  tone2("bv_sabai", "Live Sabai", "Thai ease and comfort as the promise.", ["thai","warm","relaxed","bilingual"], "Live sabai.", "Homes that feel like a deep breath."),
  tone2("bv_monsoon", "Built For The Monsoon", "Climate-specific technical pride.", ["tropical","technical","bold","practical"], "Built for the monsoon.", "Tested every rainy season since day one."),
  tone2("bv_real_hands", "Real Hands, Real Wood", "Craft and authenticity.", ["craft","natural","warm","raw"], "Real hands. Real wood. Real homes.", "Nothing flat-packed about it."),
  tone2("bv_human_landlord", "The Landlord Who Answers", "Funny-true property-management promise.", ["friendly","direct","playful","personal"], "A landlord who actually answers.", "Usually within the hour."),
  tone2("bv_build_better_th", "Build Better / สร้างดีกว่า", "Bilingual two-word line.", ["bilingual","thai","modern","direct"], "Build better.", "สร้างดีกว่า"),
  tone2("bv_inside_out", "Open To Air, Closed To Rain", "Tropical-architecture poetry.", ["tropical","natural","editorial","calm"], "Open to the air. Closed to the rain.", "Tropical homes, properly engineered."),
  tone2("bv_every_baht", "Every Baht Accounted For", "Transparency as the hook.", ["trust","direct","technical","thai"], "Every baht, accounted for.", "Line-item quotes. Photo-logged progress."),
  tone2("bv_stay_curious", "Stay Curious, Build Anyway", "Adventurous creator energy.", ["playful","personal","energetic","adventurous"], "Stay curious. Build anyway.", "New episode every Friday."),
  tone2("bv_quiet_work", "The Work Does The Talking", "Understated confidence.", ["calm","minimal","confident","craft"], "We don't shout. The work does.", ""),
  tone2("bv_ground_up", "From The Ground Up", "Foundation-first, traditional.", ["classic","construction","trust","formal"], "From the ground up, since day one.", "Weberman Construction LLC"),
  tone2("bv_local_roots", "Local Roots, Global Standards", "Thai crew, international spec.", ["thai","trust","formal","bilingual"], "Local roots. Global standards.", "Thai craftsmanship, international building codes."),
  tone2("bv_heart_hammer", "Heart & Hammer", "Warm, playful two-noun brand line.", ["warm","playful","craft","friendly"], "Heart & hammer.", "Homes built by people who care."),
  tone2("bv_less_better", "Less, But Better", "Minimalist manifesto.", ["minimal","calm","modern","direct"], "Less, but better.", "Fewer projects. Done right."),
  tone2("bv_build_adventure", "Build The Adventure", "High-energy YouTube tagline.", ["energetic","bold","youtube","adventurous"], "Build the adventure.", "Subscribe and come along."),
  tone2("bv_home_base", "Your Home Base In Thailand", "Welcoming, practical rental promise.", ["friendly","thai","practical","warm"], "Your home base in Thailand.", "Furnished, fixed fast, and fairly priced."),
 ],
 "Social Post Layouts": [
  post("sp_quote", "Big Quote Card", "One strong line, huge type, logo in the corner.", ["editorial","direct","minimal","bold"], "#f4ecd8", "#1b1b1b", "#b5651d", "playfair", "quote", "Measure twice, pour once."),
  post("sp_carousel", "Swipe Carousel Cover", "Numbered hook that begs a swipe.", ["friendly","practical","youtube","clear"], "#139a8f", "#ffffff", "#ffd60a", "kanit", "carousel", "5 Things I Wish I Knew Before Building In Thailand"),
  post("sp_photo_bar", "Photo + Thin Caption Bar", "Full photo, slim caption strip.", ["minimal","natural","light","editorial"], "#ffffff", "#1b1b1b", "#1b1b1b", "dmsans", "photo", "Teak, rain, and patience.", "int_thai", "sepia(.2)"),
  post("sp_before_after", "Before / After Slider", "Diagonal split with labels.", ["construction","clear","bold","direct"], "#111", "#ffffff", "#ff6b00", "anton", "beforeafter", "BEFORE|AFTER", "base_site"),
  post("sp_stat", "Big Stat", "One huge number, one small caption.", ["direct","technical","minimal","bold"], "#0f2340", "#ffffff", "#2dd4bf", "manrope", "stat", "94%|occupancy this quarter"),
  post("sp_checklist", "Checklist Card", "Ticked list, practical and saveable.", ["practical","friendly","clear","light"], "#fffaf0", "#1b1b1b", "#2bb673", "dmsans", "checklist", "Rainy-Season Prep|Clear gutters|Seal windows|Check drainage|Trim trees"),
  post("sp_meme", "Builder Meme", "Top caption over a site photo.", ["playful","casual","raw","personal"], "#111", "#ffffff", "#ffffff", "anton", "meme", "WHEN THE CLIENT SAYS 'SMALL CHANGE'", "base_site"),
  post("sp_grid", "3×3 Grid Tile", "One tile of a profile-wide puzzle grid.", ["editorial","bold","geometric","modern"], "#f2f0eb", "#222", "#d1495b", "syne", "grid", "WEBERMAN"),
  post("sp_bilingual", "Bilingual Caption Card", "English headline, Thai sub-line.", ["thai","bilingual","friendly","vibrant"], "#a4161a", "#ffffff", "#d4a017", "kanit", "bilingual", "New Listing|ห้องว่างพร้อมเข้าอยู่"),
  post("sp_receipt", "Receipt Breakdown", "Itemized cost like a receipt.", ["trust","direct","playful","technical"], "#ffffff", "#1b1b1b", "#d62828", "spacemono", "receipt", "Bathroom Reno|Tiles 42,000|Plumbing 18,500|Labor 36,000|TOTAL 96,500 THB"),
  post("sp_tip", "Sticky-Note Tip", "Tip of the day on a yellow sticky note.", ["friendly","craft","playful","practical"], "#e9ecef", "#1b1b1b", "#fff3b0", "caveat", "tip", "Tip: pour concrete in the morning in April. Trust me."),
  post("sp_polaroid", "Polaroid Snapshot", "Instant-photo frame with handwriting.", ["retro","warm","personal","craft"], "#d8c3a5", "#1b1b1b", "#ffffff", "caveat", "polaroid", "first sunrise on site", "ext_tropical", "sepia(.3)"),
  post("sp_type_only", "Type-Only Minimal", "Small type, lots of space.", ["minimal","calm","light","editorial"], "#ffffff", "#1b1b1b", "#1b1b1b", "inter", "minimal", "Slow is smooth. Smooth is fast."),
  post("sp_collage", "Scrapbook Collage", "Taped photos, scribbles, stickers.", ["playful","craft","warm","personal"], "#f6f0e4", "#1b1b1b", "#e56b8a", "caveat", "collage", "week 12 on site", "base_temple"),
  post("sp_poll", "This-Or-That Poll", "Two-option vote card.", ["playful","friendly","interactive","bold"], "#fff0f6", "#1b1b1b", "#ff006e", "nunito", "poll", "Teak|Concrete"),
  post("sp_map", "Map Pin Post", "Pinned location with a route line.", ["tropical","travel","thai","friendly"], "#e9fbf7", "#0b3b3a", "#ff6f59", "dmsans", "map", "Chiang Mai → Pai"),
 ],
 "Video Editing & Pacing": [
  pace("vp_jump", "Fast Jump-Cuts", "Under 1s per shot, punch-ins, no pauses.", ["energetic","youtube","bold","direct"], [1,1,1,1,1,1,1,1,1,1,1,1], ["#ff006e","#3a86ff"], ["0.8s avg shot","jump cuts","punch-in zooms"]),
  pace("vp_slow_cinema", "Slow Cinema", "Long held shots, ambient sound, room to breathe.", ["calm","cinematic","editorial","natural"], [8,11,7,12], ["#3e5641","#8fb08c"], ["6-12s shots","ambient audio","no music"]),
  pace("vp_doc", "Documentary Interview", "Talking head with b-roll cutaways.", ["trust","editorial","calm","personal"], [5,2,2,6,2,3,5], ["#1d3c6e","#b08d57"], ["interview A-roll","b-roll cutaways","lower thirds"]),
  pace("vp_timelapse", "Timelapse Build Montage", "Months of construction in 60 seconds.", ["construction","energetic","practical","bold"], [2,2,2,2,2,2,2,2], ["#ff6b00","#2b2d31"], ["timelapse","beat-synced","day counter"]),
  pace("vp_asmr", "ASMR Craft Close-Ups", "Macro shots, tool sounds up, no talking.", ["craft","calm","natural","raw"], [4,5,4,6,5], ["#8b5a2b","#d8c8a8"], ["macro lens","foley up","no voiceover"]),
  pace("vp_walk_talk", "Walk-And-Talk Vlog", "Handheld, one long ramble with light trims.", ["personal","friendly","casual","raw"], [9,3,10,4,8], ["#139a8f","#ffd166"], ["handheld","natural light","light trims"]),
  pace("vp_music_montage", "Music-Driven Montage", "Cuts land on the beat; music leads.", ["vibrant","energetic","cinematic","tropical"], [2,2,1,2,2,1,2,3], ["#f77f00","#2a9d8f"], ["cut on beat","120 BPM","speed ramps"]),
  pace("vp_tutorial", "Step-By-Step Tutorial", "Numbered chapters, on-screen labels, clear.", ["practical","direct","technical","educational"], [4,4,4,4,4,4], ["#2563eb","#e5e7eb"], ["chapters","on-screen steps","zoom callouts"]),
  pace("vp_one_take", "One Continuous Take", "No cuts. Real time. Gimbal walk-through.", ["raw","cinematic","minimal","honest"], [30], ["#1b1b1b","#c5ccd0"], ["single take","gimbal","house tour"]),
  pace("vp_split", "Split-Screen Compare", "Side-by-side shots for comparison.", ["clear","technical","bold","comparison"], [3,3,3,3,3], ["#d1495b","#00a6a6"], ["split screen","synced action","labels"]),
  pace("vp_vhs", "VHS Home-Video", "Tracking lines, date stamp, nostalgic.", ["retro","playful","warm","personal"], [3,5,2,4,3], ["#7b2cbf","#f9e79f"], ["VHS grain","date stamp","4:3 crop"]),
  pace("vp_shorts", "Vertical Shorts (30s)", "Hook in 1s, text on screen, loopable.", ["energetic","direct","youtube","mobile"], [1,2,1,2,1,2,1], ["#ff1f1f","#1b1b1b"], ["9:16","hook in 1s","captions always"]),
  pace("vp_three_act", "Three-Act Story", "Setup, struggle, payoff with music swell.", ["cinematic","warm","editorial","story"], [6,4,3,2,2,5,8], ["#5b2a86","#f7b32b"], ["story arc","music swell","slow open"]),
  pace("vp_bilingual_subs", "Burned-In Bilingual Subs", "Medium pace with English + Thai subtitles.", ["bilingual","thai","friendly","practical"], [4,3,4,3,4], ["#a4161a","#d4a017"], ["EN + TH subs","medium pace","subtitle styling"]),
  pace("vp_natural_sound", "No Talking, Natural Sound", "Birds, rain, tools. Let the place speak.", ["natural","calm","minimal","tropical"], [7,6,9,8], ["#2f5d3a","#c2dfe3"], ["nat sound","no VO","long fades"]),
  pace("vp_drone", "Drone Reveal Heavy", "Big aerial reveals between sections.", ["bold","cinematic","tropical","dramatic"], [6,2,2,7,2,2,6], ["#05668d","#f0e6d2"], ["aerial reveals","orbit shots","wide-tight-wide"]),
 ],
 "Website Hero Sections": [
  hero("wh_fullbleed", "Full-Bleed Photo", "Edge-to-edge photo with headline overlay.", ["tropical","natural","cinematic","bold"], "#000", "#ffffff", "#f6b93b", "kanit", "fullbleed", "Tropical Homes, Built Right", "Design-build across Thailand", "See Projects", "ext_tropical"),
  hero("wh_split_form", "Split With Quote Form", "Headline left, quote request form right.", ["practical","direct","construction","clear"], "#f4f4f1", "#1f1f1f", "#ff6b00", "manrope", "form", "Get A Fixed-Price Quote", "Reply within 24 hours", "Request Quote"),
  hero("wh_bigtype", "Giant Type Only", "Massive headline, nothing else.", ["bold","minimal","direct","modern"], "#ffffff", "#111111", "#ff6b00", "anton", "bigtype", "WE BUILD.", "", "Talk To Us"),
  hero("wh_video", "Video Background", "Looping site footage with play button.", ["cinematic","dark","bold","modern"], "#0b0b0b", "#ffffff", "#2dd4bf", "inter", "video", "Watch A House Get Built", "12-minute documentary", "Play", "base_site", "brightness(.6)"),
  hero("wh_cards", "Service Cards Up Top", "Three service cards right under a short headline.", ["practical","clear","friendly","corporate"], "#f5f7fb", "#1f2937", "#2563eb", "dmsans", "cards", "What Do You Need?", "Build|Renovate|Rent", ""),
  hero("wh_bilingual", "Bilingual Toggle Hero", "EN / TH toggle front and center.", ["bilingual","thai","friendly","light"], "#fffaf0", "#3b2a1a", "#8b5a2b", "kanit", "bilingual", "Homes For Life|บ้านสำหรับชีวิต", "Weberman Construction", "Contact"),
  hero("wh_center_min", "Centered Minimal", "One line, one button, lots of white.", ["minimal","light","calm","modern"], "#ffffff", "#1b1b1b", "#1b1b1b", "outfit", "center", "Thoughtful Homes In Thailand", "", "Start A Project"),
  hero("wh_portfolio", "Portfolio Grid Hero", "Project photo grid is the hero.", ["editorial","craft","visual","natural"], "#f2f0eb", "#222", "#d1495b", "dmsans", "grid", "Recent Work", "", "", "int_thai"),
  hero("wh_personal", "Personal Intro + Portrait", "Hi, I'm Max. Founder-led and human.", ["personal","friendly","warm","trust"], "#fff4e6", "#4a3426", "#e07a3f", "nunito", "split", "Hi, I'm Max.", "I build homes and film the journey.", "Watch The Channel", "base_temple"),
  hero("wh_trust", "Reviews & Trust Badges", "Stars, client logos, years in business.", ["trust","corporate","formal","clear"], "#ffffff", "#0f2340", "#b08d57", "inter", "trust", "Trusted By 120+ Owners", "★★★★★ 4.9 average", "Read Reviews"),
  hero("wh_map", "Map + Listings", "Rental map with available units.", ["practical","technical","clear","modern"], "#eef6f5", "#16302e", "#139a8f", "sarabun", "map", "Available Units", "Bangkok · Chiang Mai · Hua Hin", "Browse"),
  hero("wh_blueprint", "Blueprint Hero", "Plan drawing behind the headline.", ["technical","industrial","cool","architectural"], "#0b3d91", "#ffffff", "#ffd166", "chakra", "blueprint", "Engineered For The Tropics", "Structural · Architectural · Build", "View Plans"),
  hero("wh_warm_gradient", "Warm Gradient + Illustration", "Sunset gradient, friendly illustration.", ["warm","friendly","playful","tropical"], "linear-gradient(135deg,#ffd8b8,#ff9f6e)", "#4a3426", "#ffffff", "nunito", "illus", "Find Your Place In The Sun", "Rentals and builds", "Explore"),
  hero("wh_dark_luxe", "Dark Luxe Hero", "Black, gold rule, serif.", ["luxe","dark","formal","classic"], "#0b0b0b", "#f2ead8", "#c9a227", "cormorant", "center", "Residences Of Distinction", "By appointment", "Enquire"),
  hero("wh_magazine", "Magazine Cover Hero", "Masthead and cover lines on a photo.", ["editorial","classic","bold","storytelling"], "#000", "#ffffff", "#d62828", "playfair", "magazine", "A MOMENT IN THAI", "Issue 12 · The Teak House", "Read", "int_thai", "sepia(.3)"),
  hero("wh_chat", "Chat-First AI Hero", "A chat box is the hero: ask the agent anything.", ["technical","friendly","modern","practical"], "#f5f7fb", "#1f2937", "#7c3aed", "inter", "chat", "Ask Weberman AI", "Quotes, schedules, rentals: 24/7", "Ask"),
 ],
})

POOL_EXTRA.update({
 "Packaging & Merch": [
  merch("pm_kraft_box", "Kraft Box + Ink Stamp", "Recycled kraft box, one-color stamped mark.", ["craft","rustic","natural","raw"], "box", "#c8a97e", "#1b1b1b", "W", "spacemono"),
  merch("pm_hivis_tee", "Hi-Vis Crew Tee", "Safety-orange tee, big back print.", ["industrial","construction","bold","practical"], "tee", "#ff6b00", "#1b1b1b", "WEBERMAN", "anton"),
  merch("pm_minimal_tee", "Tiny Chest Logo Tee", "Off-white tee, small chest mark.", ["minimal","light","modern","clean"], "tee", "#f6f3ec", "#1b1b1b", "w.", "dmsans"),
  merch("pm_trucker", "Trucker Cap Patch", "Mesh trucker with woven patch.", ["rugged","playful","retro","casual"], "cap", "#2f4858", "#f4ecd8", "W", "bebas", "#c1502e"),
  merch("pm_enamel_mug", "Enamel Camp Mug", "Speckled enamel, rim stripe.", ["rustic","outdoor","warm","craft"], "mug", "#f2efe8", "#1f3b73", "W", "fraunces"),
  merch("pm_bilingual_tote", "Bilingual Tote", "Canvas tote with EN/TH type.", ["thai","bilingual","practical","natural"], "tote", "#efe6d2", "#3b2a1a", "สวัสดี|HELLO", "kanit"),
  merch("pm_sticker_pack", "Sticker Pack", "Bright die-cut stickers for laptops and crates.", ["playful","vibrant","friendly","youtube"], "sticker", "#ffbe0b", "#1b1b1b", "AMIT", "nunito", "#ff006e"),
  merch("pm_letterpress", "Letterpress Business Card", "Deep impression, cotton stock.", ["craft","classic","tactile","formal"], "card", "#f7f3ea", "#1b1b1b", "Max Weberman", "baskerville"),
  merch("pm_matte_black", "Matte Black Box", "Soft-touch black box, foil mark.", ["luxe","dark","minimal","formal"], "box", "#141414", "#c9a227", "W", "cormorant"),
  merch("pm_indigo_hoodie", "Indigo-Dyed Hoodie", "Hand-dyed indigo with tonal print.", ["craft","thai","natural","cool"], "hoodie", "#1f3b73", "#a8b8d8", "W", "fraunces"),
  merch("pm_neon_sticker", "Neon Bangkok Sticker", "Hot-pink and cyan street sticker.", ["bangkok","vibrant","urban","bold"], "sticker", "#1b1b1b", "#00e5ff", "BKK", "anton", "#ff006e"),
  merch("pm_tool_roll", "Waxed Canvas Tool Roll", "Olive waxed canvas, leather ties.", ["industrial","craft","practical","rugged"], "tote", "#5a5f3a", "#e8dcc2", "W·M", "spacemono"),
  merch("pm_coconut_cup", "Coconut-Shell Cup", "Polished coconut shell with burned mark.", ["tropical","natural","playful","craft"], "mug", "#6b4f2a", "#f4ecd8", "W", "caveat"),
  merch("pm_white_card", "Clean White Business Card", "Bright white, one accent edge.", ["minimal","modern","light","clean"], "card", "#ffffff", "#1b1b1b", "WEBERMAN", "outfit", "#139a8f"),
  merch("pm_bottle", "Steel Water Bottle", "Powder-coated steel bottle.", ["practical","modern","active","minimal"], "bottle", "#7d9a6f", "#ffffff", "W", "outfit"),
  merch("pm_hard_hat", "Branded Hard Hat", "White hard hat with crew logo.", ["construction","industrial","bold","practical"], "hat", "#ffffff", "#ff6b00", "W", "anton"),
 ],
 "Workspace": [
  mood("ws_site_office", "Site Office Container", "Converted container, plan table, whiteboard.", ["industrial","practical","raw","construction"], ["#2f3e46","#ff6b00","#c5ccd0","#f4f4f1","#a0522d"], ["container","plan rack","whiteboard"]),
  mood("ws_white_desk", "Minimal White Desk", "One laptop, one lamp, nothing else.", ["minimal","light","calm","modern"], ["#ffffff","#f1f1ef","#d9d9d9","#2b2b2b","#c8a97e"], ["white oak","laptop","task lamp"]),
  mood("ws_teak_studio", "Teak Studio", "Solid teak desk, rattan chair, jungle view.", ["warm","natural","thai","craft"], ["#6b4226","#c8a97e","#3e5641","#f4ecd8","#1b1b1b"], ["teak slab","rattan","linen blinds"]),
  mood("ws_cafe", "Café Nomad", "Corner table, flat white, headphones.", ["personal","casual","warm","urban"], ["#6f4e37","#d8c3a5","#2b2b2b","#f2efe8","#9caf88"], ["espresso","headphones","notebook"]),
  mood("ws_garden_sala", "Garden Sala Office", "Open-air pavilion desk among plants.", ["tropical","natural","light","calm"], ["#2f5d3a","#8fb08c","#c8a97e","#f7f3ea","#ffffff"], ["open sala","ceiling fan","plants"]),
  mood("ws_command", "Multi-Monitor Command Center", "Three screens, RGB glow, dashboards.", ["technical","dark","bold","modern"], ["#0b0f1a","#1f6feb","#00e5ff","#7c3aed","#e6edf3"], ["3 monitors","LED strip","mech keyboard"]),
  mood("ws_woodshop", "Woodshop Bench", "Workbench, pegboard, sawdust.", ["craft","rustic","practical","raw"], ["#a0784e","#5c4033","#e8dcc2","#2b2b2b","#ff6b00"], ["pegboard","hand planes","sawdust"]),
  mood("ws_tatami_desk", "Floor Desk On Tatami", "Low desk, cushion, shoji light.", ["japanese","calm","minimal","natural"], ["#d8c8a8","#8c6e4a","#f2ede3","#3b3b3b","#9caf88"], ["tatami","zabuton","shoji"]),
  mood("ws_jungle", "Jungle Office", "Plants everywhere, humid and green.", ["natural","tropical","playful","fresh"], ["#1b3a2b","#355e3b","#83b735","#f4efe6","#c1502e"], ["monstera","hanging pots","terracotta"]),
  mood("ws_edit_bay", "Video Editing Bay", "Dark room, color-accurate monitor, speakers.", ["technical","cinematic","dark","focused"], ["#121212","#2b2b2b","#5b2a86","#f7b32b","#e6e6e6"], ["reference monitor","studio monitors","blackout"]),
  mood("ws_standing_loft", "Standing Desk Loft", "Steel-frame standing desk in a brick loft.", ["industrial","modern","active","warm"], ["#9c4a2f","#2e2e2e","#d8c3a5","#f2efe8","#c8a97e"], ["standing desk","brick","Edison bulbs"]),
  mood("ws_vintage_study", "Vintage Study", "Leather chair, bookshelves, green lamp.", ["classic","warm","formal","dark"], ["#3b2a1a","#5c4033","#1b3a2b","#c9a227","#efe6d2"], ["leather","walnut","banker's lamp"]),
  mood("ws_van", "Van Office", "Laptop on a fold-down table, door open to the coast.", ["rugged","outdoor","personal","adventurous"], ["#5a7d4f","#e9e2d0","#c19a6b","#2f4858","#ffffff"], ["fold-down desk","solar panel","Starlink"]),
  mood("ws_coworking", "Bright Coworking", "Shared tables, big windows, community buzz.", ["friendly","modern","light","social"], ["#ffffff","#f5f7fb","#2563eb","#ffd166","#1f2937"], ["shared tables","phone booths","plants"]),
  mood("ws_drafting", "Drafting Table", "Tilted board, parallel rule, pencils.", ["technical","craft","classic","architectural"], ["#f4f1e8","#0b3d91","#8b5a2b","#2b2b2b","#ffd166"], ["parallel rule","trace paper","pencils"]),
  mood("ws_rooftop", "Bangkok Rooftop Desk", "Laptop on a rooftop at golden hour, skyline behind.", ["bangkok","urban","warm","personal"], ["#ff6f59","#f7b32b","#5b2a86","#2b2b2b","#fff1e6"], ["skyline","string lights","outdoor table"]),
 ],
 "Cars & Gear": [
  mood("cg_pickup", "Pickup Workhorse", "Double-cab diesel pickup, ladder rack.", ["practical","rugged","construction","direct"], ["#f2f2f2","#2b2d31","#9aa5ab","#ff6b00","#1b1b1b"], ["double cab","ladder rack","tow hitch"]),
  mood("cg_land_cruiser", "Vintage Land Cruiser", "Old 4x4 restored with care.", ["retro","rugged","adventurous","craft"], ["#c3b091","#4b5320","#efe6d2","#2b2b2b","#a0522d"], ["steel bumpers","roof rack","snorkel"]),
  mood("cg_scooter", "Scooter Life", "Thai-everyday automatic scooter.", ["thai","practical","playful","urban"], ["#d62828","#ffffff","#2b2b2b","#fcbf49","#c5ccd0"], ["125cc","basket","helmet"]),
  mood("cg_ev", "Minimal EV", "Quiet electric car, clean dashboard.", ["modern","technical","minimal","light"], ["#ffffff","#e9ecef","#adb5bd","#212529","#4dabf7"], ["EV","glass roof","single screen"]),
  mood("cg_cafe_racer", "Café Racer Motorbike", "Custom vintage-style motorcycle.", ["craft","retro","bold","personal"], ["#1b1b1b","#8c1c13","#c19a6b","#c0c0c0","#efe6d2"], ["clip-ons","leather seat","chrome"]),
  mood("cg_adv_bike", "Adventure Touring Bike", "Panniers, crash bars, mountain passes.", ["adventurous","technical","rugged","outdoor"], ["#ff8c42","#2b2d31","#a3b18a","#f8f9fa","#3a86ff"], ["panniers","crash bars","GPS"]),
  mood("cg_camper", "Camper Van", "Pop-top van, slow travel.", ["personal","relaxed","outdoor","natural"], ["#9caf88","#f4efe6","#c8a97e","#2f4858","#ffffff"], ["pop-top","awning","bed"]),
  mood("cg_luxury_suv", "Luxury SUV", "Black premium SUV, leather interior.", ["luxe","formal","dark","classic"], ["#0b0b0b","#3a3a3a","#c9a227","#efe6d2","#ffffff"], ["leather","chrome","tinted glass"]),
  mood("cg_gravel_bike", "Steel Gravel Bike", "Simple steel bike for dirt roads.", ["natural","active","minimal","outdoor"], ["#355e3b","#c8a97e","#2b2b2b","#f2efe8","#b5651d"], ["steel frame","wide tires","frame bag"]),
  mood("cg_tuktuk", "Custom Tuk-Tuk", "Branded tuk-tuk for shoots and promos.", ["bangkok","playful","vibrant","bold"], ["#00a8e8","#ff006e","#ffd60a","#1b1b1b","#ffffff"], ["3 wheels","neon trim","sound system"]),
  mood("cg_cinema_rig", "Cinema Camera Rig", "Full-frame cinema camera, cage, matte box.", ["technical","cinematic","bold","pro"], ["#1b1b1b","#3a3a3a","#d62828","#c0c0c0","#ffffff"], ["cinema camera","matte box","follow focus"]),
  mood("cg_pocket", "Pocket Vlog Kit", "Tiny gimbal camera and a lav mic.", ["minimal","practical","personal","light"], ["#2b2b2b","#e9ecef","#ffffff","#adb5bd","#ff6f59"], ["pocket gimbal","wireless lav","phone"]),
  mood("cg_cordless", "Pro Cordless Tool Kit", "One battery platform, every tool.", ["industrial","practical","construction","bold"], ["#ffd400","#1b1b1b","#6c757d","#ffffff","#ff6b00"], ["drill","impact driver","track saw"]),
  mood("cg_film_camera", "Film Camera Kit", "Mechanical film body, prime lens, rolls of Portra.", ["retro","craft","warm","personal"], ["#c0c0c0","#1b1b1b","#f2c6b4","#d4a017","#efe6d2"], ["35mm body","50mm prime","Portra 400"]),
  mood("cg_drone", "Drone Kit", "Compact drone, ND filters, spare batteries.", ["technical","bold","cinematic","modern"], ["#e9ecef","#2b2b2b","#00a6a6","#ffffff","#ff6b00"], ["drone","ND filters","controller"]),
  mood("cg_field_watch", "Field Watch", "Simple, legible, tough watch.", ["classic","rugged","practical","minimal"], ["#4b5320","#efe6d2","#2b2b2b","#c0c0c0","#c19a6b"], ["canvas strap","steel case","luminous dial"]),
 ],
})

POOL_EXTRA.update({
 "Food Styling": [
  mood("fd_street_steam", "Street-Market Steam", "Woks, steam, fluorescent light, motion.", ["bangkok","vibrant","raw","energetic"], ["#d62828","#f77f00","#2b2b2b","#fcbf49","#f2efe8"], ["wok hei","plastic stools","neon"]),
  mood("fd_banana_leaf", "Banana-Leaf Plating", "Food on fresh banana leaves, top-down.", ["thai","natural","tropical","craft"], ["#3c8d2f","#83b735","#f6b93b","#fff5e1","#6b4226"], ["banana leaf","rattan tray","herbs"]),
  mood("fd_fine_dining", "Fine-Dining Minimal", "Tiny portions, tweezers, big white plates.", ["luxe","minimal","formal","modern"], ["#ffffff","#f1f1ef","#2b2b2b","#c9a227","#9caf88"], ["porcelain","microgreens","tweezers"]),
  mood("fd_rustic_table", "Rustic Wooden Table", "Old wood, linen napkins, crumbs left in.", ["rustic","warm","natural","craft"], ["#7a5230","#c9a77c","#efe6d2","#6b7f3a","#3b2a1a"], ["reclaimed wood","linen","cast iron"]),
  mood("fd_flatlay", "Bright Overhead Flat-Lay", "Clean top-down, bright colors, crisp shadows.", ["light","vibrant","modern","clean"], ["#ffffff","#ff8c42","#83b735","#ffd60a","#e56b8a"], ["overhead","white marble","hard light"]),
  mood("fd_dark_moody", "Dark & Moody Food", "Black backdrop, single window light.", ["dark","cinematic","luxe","dramatic"], ["#141414","#2b2b2b","#8c3b1f","#c9a227","#efe6d2"], ["slate","side light","deep shadow"]),
  mood("fd_bento", "Bento Precision", "Neat compartments, careful arrangement.", ["japanese","minimal","calm","precise"], ["#1b1b1b","#d1495b","#f2ede3","#9caf88","#f6b93b"], ["lacquer box","rice","pickles"]),
  mood("fd_family_feast", "Family-Style Feast", "Many shared dishes, hands reaching in.", ["warm","friendly","thai","social"], ["#c1502e","#f6b93b","#3c8d2f","#fff5e1","#6b4226"], ["shared plates","sticky rice baskets","laughter"]),
  mood("fd_fruit_cart", "Tropical Fruit Cart", "Glass cart of mango, papaya, watermelon on ice.", ["tropical","vibrant","playful","fresh"], ["#ff8c42","#f4a6b7","#83b735","#ffd60a","#e0fbfc"], ["ice","glass cart","fruit"]),
  mood("fd_coffee", "Slow Coffee Ritual", "Pour-over, ceramic cups, morning light.", ["calm","craft","natural","minimal"], ["#6f4e37","#d8c3a5","#f2efe8","#3b3b3b","#9caf88"], ["pour-over","stoneware","morning light"]),
  mood("fd_site_bbq", "Job-Site Lunch BBQ", "Grill on a tailgate, crew lunch.", ["industrial","casual","raw","social"], ["#2b2d31","#ff6b00","#8b3a1a","#c5ccd0","#f6b93b"], ["tailgate","charcoal","paper plates"]),
  mood("fd_mortar", "Mortar & Pestle Process", "Som tam being pounded, process shots.", ["craft","thai","raw","energetic"], ["#6b4226","#d62828","#83b735","#fff5e1","#3b2a1a"], ["clay mortar","chili","lime"]),
  mood("fd_pastel_cafe", "Pastel Café", "Soft pinks, latte art, cute desserts.", ["soft","playful","light","sweet"], ["#ffcdb2","#f8c8d8","#fff3b0","#ffffff","#cdb4db"], ["latte art","pastel plates","dessert"]),
  mood("fd_noodle_macro", "Macro Noodle Close-Up", "Steam, chopsticks lifting noodles, glossy broth.", ["bold","cinematic","warm","appetizing"], ["#c1502e","#f6b93b","#3b2a1a","#fff5e1","#83b735"], ["macro","chopstick lift","steam"]),
  mood("fd_izakaya", "Izakaya Warmth", "Lantern light, skewers, beer glasses.", ["japanese","warm","dark","social"], ["#8c1c13","#f7b32b","#2b2b2b","#efe6d2","#5c4033"], ["paper lantern","yakitori","counter seats"]),
  mood("fd_fresh_bowl", "Fresh Clean Bowl", "Grain bowl, bright greens, healthy.", ["light","fresh","minimal","natural"], ["#a7c957","#ffffff","#f6b93b","#e56b8a","#f2efe8"], ["grain bowl","greens","sesame"]),
 ],
 "Music & Mood": [
  mood("mm_lofi", "Lo-Fi Chill", "Dusty beats, vinyl crackle, study vibes.", ["calm","soft","personal","retro"], ["#cdb4db","#ffcdb2","#6d597a","#355070","#fdf6f0"], ["78 BPM","vinyl crackle","Rhodes"]),
  mood("mm_molam", "Molam / Luk Thung Groove", "Isan khaen, phin and twangy country-funk.", ["thai","playful","warm","energetic"], ["#d4a017","#a4161a","#0b6e4f","#fff4d6","#1b1b1b"], ["khaen","phin","Isan groove"]),
  mood("mm_ambient", "Ambient Drone", "Washes of sound, no beat.", ["calm","minimal","cinematic","spacious"], ["#c2dfe3","#9db4c0","#5c6b73","#253237","#e0fbfc"], ["no beat","pads","reverb"]),
  mood("mm_acoustic", "Acoustic Folk", "Fingerpicked guitar, warm and human.", ["warm","natural","craft","personal"], ["#c8a97e","#6b4226","#9caf88","#f4ecd8","#3b2a1a"], ["acoustic guitar","harmonica","100 BPM"]),
  mood("mm_indie", "Indie Rock Energy", "Driving guitars, real drums.", ["energetic","raw","bold","youtube"], ["#d62828","#1b1b1b","#f2efe8","#fcbf49","#3a86ff"], ["electric guitar","live drums","140 BPM"]),
  mood("mm_strings", "Cinematic Strings", "Swelling orchestral strings.", ["cinematic","editorial","formal","dramatic"], ["#1d3c6e","#b08d57","#e8dcc2","#0f2340","#fbf8f1"], ["strings","swell","piano"]),
  mood("mm_citypop", "Japanese City Pop", "80s Tokyo night-drive funk.", ["japanese","retro","playful","urban"], ["#ff7eb6","#7c3aed","#00e5ff","#ffd166","#1a1a40"], ["slap bass","synth brass","night drive"]),
  mood("mm_tropical_house", "Tropical House", "Marimba, steel drums, sunny four-on-the-floor.", ["tropical","vibrant","light","energetic"], ["#00a6a6","#ff9f1c","#ffd60a","#ffffff","#2ec4b6"], ["marimba","115 BPM","pan flute"]),
  mood("mm_jazz", "Late-Night Jazz", "Smoky trio, brushes on snare.", ["luxe","dark","classic","calm"], ["#141414","#3b2a1a","#c9a227","#8c1c13","#efe6d2"], ["upright bass","brushes","saxophone"]),
  mood("mm_field", "Field Recordings Only", "Birds, rain, cicadas, tools. No music.", ["natural","minimal","raw","calm"], ["#2f5d3a","#8fb08c","#c2dfe3","#f7f3ea","#5c4033"], ["cicadas","rain","birdsong"]),
  mood("mm_synthwave", "Synthwave", "Neon arpeggios, retro-futurist.", ["retro","dark","bold","cinematic"], ["#1a1a40","#ff006e","#7c3aed","#00e5ff","#ffbe0b"], ["arpeggios","gated drums","neon"]),
  mood("mm_boombap", "Boom-Bap Hip-Hop", "Head-nod beats, sampled loops.", ["direct","urban","bold","confident"], ["#1b1b1b","#fcbf49","#d62828","#f2efe8","#3a3a3a"], ["90 BPM","samples","scratches"]),
  mood("mm_thai_funk", "Thai Funk / Phin Psych", "60s-70s Thai psych-funk revival.", ["thai","vibrant","retro","energetic"], ["#f77f00","#d62828","#2a9d8f","#e9c46a","#264653"], ["phin","fuzz guitar","congas"]),
  mood("mm_piano", "Solo Piano", "Gentle neo-classical piano.", ["calm","soft","classic","minimal"], ["#f7f5ef","#2b2b2b","#c8b593","#e9e4d8","#6d597a"], ["felt piano","sparse","60 BPM"]),
  mood("mm_work_rhythm", "Work-Rhythm Percussion", "Hammers, saws and drums turned into beats.", ["industrial","energetic","raw","construction"], ["#2b2d31","#ff6b00","#c5ccd0","#8b3a1a","#f8f9fa"], ["found sound","stomp","claps"]),
  mood("mm_reggae", "Island Reggae", "Laid-back offbeat, beach afternoons.", ["tropical","relaxed","warm","playful"], ["#2f9e44","#ffd43b","#e03131","#f4efe6","#1b1b1b"], ["offbeat skank","bass","75 BPM"]),
 ],
 "Bangkok Vs Japan Aesthetics": [
  mood("bj_bkk_yaowarat", "Bangkok: Yaowarat Neon", "Chinatown neon signs, red and gold, night crowds.", ["bangkok","vibrant","bold","urban"], ["#d62828","#fcbf49","#1b1b1b","#00a8e8","#fff1e6"], ["neon signs","gold shops","street food"]),
  mood("bj_bkk_market", "Bangkok: Wet-Market Chaos", "Tarps, crates, colors stacked on colors.", ["bangkok","raw","vibrant","energetic"], ["#00a8e8","#ff006e","#83b735","#f6b93b","#6c757d"], ["blue tarps","plastic crates","hanging bulbs"]),
  mood("bj_bkk_temple", "Bangkok: Temple Gold & Mosaic", "Glass mosaic, gold leaf, layered roofs.", ["bangkok","thai","traditional","bold"], ["#d4a017","#a4161a","#0b6e4f","#1f3b73","#fff4d6"], ["gold leaf","glass mosaic","naga roofs"]),
  mood("bj_bkk_shophouse", "Bangkok: Old Shophouse Patina", "Peeling paint, rolling shutters, potted plants.", ["bangkok","rustic","warm","urban"], ["#e9c46a","#5a7d4f","#9c4a2f","#d8c3a5","#2b2b2b"], ["roller shutters","patina","potted plants"]),
  mood("bj_bkk_khlong", "Bangkok: Khlong Canal Life", "Wooden houses on stilts over canals, long-tail boats.", ["bangkok","natural","craft","tropical"], ["#5c4033","#2f5d3a","#7a9e9f","#f4ecd8","#c1502e"], ["stilt houses","long-tail boats","canal"]),
  mood("bj_bkk_rooftop", "Bangkok: Rooftop Skyline", "Glass towers, sunset haze, rooftop bars.", ["bangkok","modern","urban","warm"], ["#ff6f59","#5b2a86","#f7b32b","#2b2b2b","#fff1e6"], ["skyline","haze","rooftop"]),
  mood("bj_bkk_signs", "Bangkok: Hand-Painted Signs", "Hand-lettered shop signs in bold Thai script.", ["bangkok","craft","playful","bilingual"], ["#d62828","#ffffff","#1f3b73","#fcbf49","#2b2b2b"], ["hand lettering","enamel paint","Thai script"]),
  mood("bj_bkk_modernism", "Bangkok: Tropical Modernism", "60s concrete brise-soleil and breeze blocks.", ["bangkok","modern","tropical","architectural"], ["#e8e4dc","#a9a9a2","#2f5d3a","#c1502e","#4a4a48"], ["breeze blocks","brise-soleil","terrazzo"]),
  mood("bj_jp_machiya", "Japan: Kyoto Machiya Calm", "Wooden lattice townhouses, quiet lanes.", ["japan","calm","craft","natural"], ["#5c4033","#d8c8a8","#2b2b2b","#f2ede3","#9caf88"], ["koshi lattice","noren","stone path"]),
  mood("bj_jp_shinjuku", "Japan: Shinjuku Neon", "Dense vertical neon signage, rain on asphalt.", ["japan","vibrant","urban","dark"], ["#1a1a40","#ff006e","#00e5ff","#ffbe0b","#7c3aed"], ["vertical signs","wet asphalt","izakaya alleys"]),
  mood("bj_jp_muji", "Japan: Muji Utility Minimal", "Undyed, unbranded, perfectly useful.", ["japan","minimal","light","practical"], ["#f7f5ef","#e3d9c6","#a39b8b","#ffffff","#7f2e2e"], ["undyed cotton","PP boxes","oak"]),
  mood("bj_jp_ryokan", "Japan: Ryokan & Onsen", "Cedar bath, yukata, garden view.", ["japan","calm","luxe","natural"], ["#8c6e4a","#d8c8a8","#2f4f2f","#f2ede3","#3b3b3b"], ["hinoki bath","yukata","tatami"]),
  mood("bj_jp_shotengai", "Japan: Shōtengai Retro", "Covered shopping arcades, Showa-era signage.", ["japan","retro","playful","warm"], ["#d1495b","#edae49","#00798c","#f2efe8","#30638e"], ["arcade roof","Showa signs","kissaten"]),
  mood("bj_jp_zen", "Japan: Zen Garden Order", "Raked gravel, moss, a single stone.", ["japan","minimal","calm","natural"], ["#e9e4d8","#a39b8b","#3a5a40","#6e6658","#f7f5ef"], ["raked gravel","moss","stone"]),
  mood("bj_jp_konbini", "Japan: Konbini Pop", "Bright packaging, perfect shelves, cute mascots.", ["japan","playful","vibrant","light"], ["#ffffff","#2a9d8f","#e63946","#ffbe0b","#3a86ff"], ["onigiri","mascots","fluorescent"]),
  mood("bj_jp_ando", "Japan: Concrete Ando Modern", "Smooth concrete, light slots, silence.", ["japan","minimal","modern","industrial"], ["#bdbcb6","#8e8e8a","#2b2b2b","#f2f0eb","#5a7d4f"], ["form-tie concrete","light slot","water"]),
 ],
})

for _cat, _opts in POOL_EXTRA.items():
    POOL.setdefault(_cat, []).extend(_opts)

CATEGORY_WEIGHT = {  # base share of the deck
    "App / UI Style": 1.0, "Color Palette": 1.1, "Typography": 1.0, "Business Communication Tone": 1.1,
    "Home / Interior Style": 1.0, "Logo / Mark": 1.0, "Photography Style": 0.8, "Fashion / Personal Look": 0.8,
    "YouTube Thumbnail Style": 0.8, "Icon & Illustration Style": 0.6,
    "Brand Voice & Taglines": 1.1, "Social Post Layouts": 0.9, "Video Editing & Pacing": 0.9,
    "Website Hero Sections": 0.9, "Packaging & Merch": 0.8, "Workspace": 0.8, "Cars & Gear": 0.7,
    "Food Styling": 0.7, "Music & Mood": 0.8, "Bangkok Vs Japan Aesthetics": 0.9,
}

# Categories whose pairs must contrast on a tag: one option carries tag X, the other tag Y.
PAIR_RULES = {"Bangkok Vs Japan Aesthetics": ("bangkok", "japan")}

# ---------------------------------------------------------------------------
def load_json(path, default):
    try:
        with open(path) as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def empty_profile():
    return {"version": 1, "updated": None, "decks_ingested": [], "tags": {}, "options": {}, "categories": {}}

def pair_key(a, b):
    return "|".join(sorted([a, b]))

def seen_pairs(exclude_date=None):
    seen = set()
    for p in glob.glob(os.path.join(DECKS, "*.json")):
        if exclude_date and os.path.basename(p) == f"{exclude_date}.json": continue
        d = load_json(p, {})
        for pr in d.get("pairs", []):
            seen.add(pair_key(pr["optionA"]["id"], pr["optionB"]["id"]))
    return seen

def tag_pref(profile, tag):
    """Returns (preference in [-1,1], uncertainty in [0,1])."""
    t = profile["tags"].get(tag)
    if not t: return 0.0, 1.0
    w, l, n = t.get("wins", 0), t.get("losses", 0), t.get("shown", 0)
    pref = (w - l) / (w + l + 2)          # smoothed
    conf = min(1.0, n / 8) * abs(pref)    # needs exposure AND a clear lean
    return pref, 1.0 - conf

def option_score(profile, opt):
    return sum(tag_pref(profile, t)[0] for t in opt["tags"]) / max(1, len(opt["tags"]))

def category_uncertainty(profile, cat):
    c = profile["categories"].get(cat, {})
    answered = c.get("answered", 0)
    tags = {t for o in POOL[cat] for t in o["tags"]}
    tag_unc = sum(tag_pref(profile, t)[1] for t in tags) / len(tags)
    exposure_unc = 1.0 / (1 + answered / 10)
    neither_rate = c.get("neither", 0) / max(1, answered)   # lots of "neither" => keep exploring
    return 0.5 * tag_unc + 0.35 * exposure_unc + 0.15 * min(1, neither_rate * 2)

def allocate(profile, total, caps):
    """Split `total` pairs across categories by weight x uncertainty, never exceeding caps[cat]."""
    raw = {c: CATEGORY_WEIGHT.get(c, 0.8) * (0.5 + category_uncertainty(profile, c)) for c in POOL}
    alloc = {c: 0 for c in POOL}
    total = min(total, sum(caps.values()))
    for c in sorted(POOL, key=lambda c: -raw[c]):      # everyone with room gets at least 1
        if sum(alloc.values()) < total and caps[c] > 0: alloc[c] = 1
    while sum(alloc.values()) < total:                  # then fill by largest deficit vs. ideal share
        s = sum(raw[c] for c in POOL if alloc[c] < caps[c])
        c = max((c for c in POOL if alloc[c] < caps[c]), key=lambda c: total * raw[c] / s - alloc[c])
        alloc[c] += 1
    return alloc

def pair_priority(profile, a, b, rng):
    """Higher = more informative. Contrast on uncertain tags; plus refinement among liked options."""
    diff = set(a["tags"]) ^ set(b["tags"])
    contrast = sum(tag_pref(profile, t)[1] for t in diff) / 4.0
    sa, sb = option_score(profile, a), option_score(profile, b)
    refine = 0.6 if (sa > 0.15 and sb > 0.15) else 0.0      # both liked -> fine-tune
    both_disliked = -0.8 if (sa < -0.25 and sb < -0.25) else 0.0
    oa = profile["options"].get(a["id"], {}).get("shown", 0)
    ob = profile["options"].get(b["id"], {}).get("shown", 0)
    novelty = 0.5 / (1 + oa) + 0.5 / (1 + ob)
    return contrast + refine + both_disliked + novelty + rng.random() * 0.6

def shown_options(exclude_date=None):
    """option id -> set of deck dates it appeared in. Union of shown_options.json and every decks/*.json,
    ignoring `exclude_date` (the deck being (re)generated)."""
    out = {k: set(v) for k, v in load_json(SHOWN, {}).get("options", {}).items()}
    for p in glob.glob(os.path.join(DECKS, "*.json")):
        date = os.path.basename(p)[:-5]
        for pr in load_json(p, {}).get("pairs", []):
            for o in ("optionA", "optionB"):
                out.setdefault(pr[o]["id"], set()).add(date)
    if exclude_date:
        for k in list(out):
            out[k].discard(exclude_date)
            if not out[k]: del out[k]
    return out

def save_shown():
    """Persist the ever-shown ledger (never forgets, even if a deck file is deleted)."""
    shown = shown_options()
    all_ids = {o["id"] for opts in POOL.values() for o in opts}
    remaining = {c: sum(o["id"] not in shown for o in opts) for c, opts in POOL.items()}
    data = {"updated": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "note": "Options already shown in a deck. generate_deck.py never reuses these.",
            "shown_count": len(shown), "pool_size": len(all_ids), "unseen_remaining": len(all_ids - set(shown)),
            "unseen_by_category": remaining,
            "options": {k: sorted(v) for k, v in sorted(shown.items())}}
    with open(SHOWN, "w") as f: json.dump(data, f, indent=1)
    return data

def build_deck(date, n_pairs, seed=None, allow_repeats=False):
    rng = random.Random(seed if seed is not None else date)
    profile = load_json(PROFILE, empty_profile())
    seen = seen_pairs(exclude_date=date)
    shown = shown_options(exclude_date=date)
    avail = {c: [o for o in opts if o["id"] not in shown] for c, opts in POOL.items()}
    def cap(c, opts):
        if c in PAIR_RULES:
            x, y = PAIR_RULES[c]
            return min(sum(x in o["tags"] for o in opts), sum(y in o["tags"] for o in opts))
        return len(opts) // 2
    caps = {c: cap(c, avail[c]) for c in POOL}
    warnings = []
    if sum(caps.values()) < n_pairs:
        msg = (f"Only {sum(caps.values())} fresh pairs left in the pool (wanted {n_pairs}). "
               "Add more options to POOL" + (", topping up with previously shown options." if allow_repeats else "; deck will be shorter."))
        print("WARNING:", msg); warnings.append(msg)
    alloc = allocate(profile, n_pairs, caps)
    pairs = []
    def pick(cat, opts, k, used):
        cands = list(itertools.combinations(opts, 2))
        if cat in PAIR_RULES:
            x, y = PAIR_RULES[cat]
            cands = [(a, b) for a, b in cands if (x in a["tags"] and y in b["tags"]) or (y in a["tags"] and x in b["tags"])]
        cands = [ab for ab in cands if pair_key(ab[0]["id"], ab[1]["id"]) not in seen]
        cands.sort(key=lambda ab: -pair_priority(profile, ab[0], ab[1], rng))
        chosen = []
        for a, b in cands:                     # each option at most once per deck
            if len(chosen) >= k: break
            if a["id"] in used or b["id"] in used: continue
            chosen.append((a, b)); used.update((a["id"], b["id"]))
        return chosen
    used = set()
    for cat, k in alloc.items():
        for a, b in pick(cat, avail[cat], k, used):
            if rng.random() < 0.5: a, b = b, a
            pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": False})
    if allow_repeats and len(pairs) < n_pairs:     # explicit opt-in only
        for cat in sorted(POOL, key=lambda c: -CATEGORY_WEIGHT.get(c, 0.8)):
            need = n_pairs - len(pairs)
            if need <= 0: break
            for a, b in pick(cat, POOL[cat], min(need, 2), used):
                pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": True})
    rng.shuffle(pairs)
    for i in range(1, len(pairs)):              # avoid back-to-back same category
        if pairs[i]["category"] == pairs[i-1]["category"]:
            for j in range(i + 1, len(pairs)):
                if pairs[j]["category"] != pairs[i-1]["category"]:
                    pairs[i], pairs[j] = pairs[j], pairs[i]; break
    pairs = [{"id": f"{date}-{i:02d}", **p} for i, p in enumerate(pairs, 1)]
    opt_ids = [p[o]["id"] for p in pairs for o in ("optionA", "optionB")]
    fresh = sum(oid not in shown for oid in opt_ids)
    return {"date": date, "version": 2, "owner": "Max Weberman",
            "brands": ["YouTube @AMomentInThai", "Weberman Construction LLC", "Property Management", "AI Agents"],
            "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "allocation": {c: n for c, n in alloc.items() if n},
            "freshness": {"option_slots": len(opt_ids), "never_shown_before": fresh,
                          "share": round(fresh / max(1, len(opt_ids)), 3)},
            "warnings": warnings, "pairs": pairs,
            "image_credits": load_json(CREDITS, {})}

# ---------------------------------------------------------------------------
def ingest(results_path):
    res = load_json(results_path, None)
    if not res: sys.exit(f"Could not read results JSON: {results_path}")
    profile = load_json(PROFILE, empty_profile())
    deck_date = res.get("deck")
    if deck_date in profile["decks_ingested"]:
        print(f"Deck {deck_date} already ingested; skipping (delete it from profile.decks_ingested to redo).")
        return
    def bump(d, key, field, amt=1):
        d.setdefault(key, {}).setdefault(field, 0); d[key][field] += amt
    for p in res.get("picks", []):
        choice, cat = p.get("choice"), p.get("category")
        if choice == "skip": continue
        bump(profile["categories"], cat, "answered")
        a_tags, b_tags = p.get("tagsA", []), p.get("tagsB", [])
        for t in set(a_tags) | set(b_tags): bump(profile["tags"], t, "shown")
        for oid in (p.get("optionA"), p.get("optionB")): bump(profile["options"], oid, "shown")
        if choice in ("A", "B"):
            win, lose = (a_tags, b_tags) if choice == "A" else (b_tags, a_tags)
            wid, lid = (p["optionA"], p["optionB"]) if choice == "A" else (p["optionB"], p["optionA"])
            for t in set(win) - set(lose): bump(profile["tags"], t, "wins")
            for t in set(lose) - set(win): bump(profile["tags"], t, "losses")
            bump(profile["options"], wid, "wins"); bump(profile["options"], lid, "losses")
        elif choice == "neither":
            bump(profile["categories"], cat, "neither")
            for t in set(a_tags) | set(b_tags): bump(profile["tags"], t, "losses", 0.5)
            for oid in (p.get("optionA"), p.get("optionB")): bump(profile["options"], oid, "losses", 0.5)
    profile["decks_ingested"].append(deck_date)
    profile["updated"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    # convenience view: top tags
    ranked = sorted(profile["tags"].items(), key=lambda kv: -(kv[1].get("wins", 0) - kv[1].get("losses", 0)))
    profile["top_tags"] = [t for t, _ in ranked[:12]]
    profile["bottom_tags"] = [t for t, _ in ranked[-8:]]
    with open(PROFILE, "w") as f: json.dump(profile, f, indent=1)
    print(f"Ingested {len(res.get('picks', []))} picks from deck {deck_date}. Top tags: {', '.join(profile['top_tags'][:8])}")

# ---------------------------------------------------------------------------
def inline_images(deck):
    """Return a copy of the deck with image keys mapped to small data URIs (for a self-contained HTML)."""
    imgs = {}
    keys = {p[o]["visual"].get("key") for p in deck["pairs"] for o in ("optionA", "optionB")} - {None}
    try:
        from PIL import Image
    except ImportError:
        Image = None
    for k in sorted(keys):
        path = os.path.join(ROOT, "img", f"{k}.jpg")
        if not os.path.exists(path): continue
        if Image:
            im = Image.open(path).convert("RGB"); im.thumbnail((560, 420))
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=72, optimize=True); data = buf.getvalue()
        else:
            data = open(path, "rb").read()
        imgs[k] = "data:image/jpeg;base64," + base64.b64encode(data).decode()
    return imgs

def render_index(deck):
    if not os.path.exists(TEMPLATE):
        print("No index.template.html; skipping HTML render."); return
    html = open(TEMPLATE).read()
    payload = json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")
    imgs = json.dumps(inline_images(deck)).replace("</", "<\\/")
    html = html.replace("/*__DECK_JSON__*/null", payload).replace("/*__IMAGES_JSON__*/{}", imgs)
    with open(INDEX, "w") as f: f.write(html)
    print(f"Rendered {INDEX} ({os.path.getsize(INDEX)//1024} KB) with deck {deck['date']} embedded")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="YYYY-MM-DD (default: today, local time)")
    ap.add_argument("--pairs", type=int, default=50)
    ap.add_argument("--ingest", help="results JSON exported from the app")
    ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--seed")
    ap.add_argument("--allow-repeats", action="store_true", help="if the fresh pool runs out, top up with previously shown options")
    a = ap.parse_args()
    os.makedirs(DECKS, exist_ok=True)
    if not os.path.exists(PROFILE):
        with open(PROFILE, "w") as f: json.dump(empty_profile(), f, indent=1)
    if a.ingest:
        ingest(a.ingest)
        if not a.date: return
    date = a.date or dt.date.today().isoformat()
    dt.date.fromisoformat(date)
    out = os.path.join(DECKS, f"{date}.json")
    if os.path.exists(out) and not a.force:
        print(f"{out} exists (use --force to regenerate). Re-rendering HTML from it.")
        deck = load_json(out, None)
    else:
        deck = build_deck(date, a.pairs, a.seed, a.allow_repeats)
        with open(out, "w") as f: json.dump(deck, f, indent=1, ensure_ascii=False)
        fr = deck["freshness"]
        print(f"Wrote {out}: {len(deck['pairs'])} pairs; {fr['never_shown_before']}/{fr['option_slots']} option slots never shown before ({fr['share']:.0%}).")
        print(f"Allocation: {deck['allocation']}")
    led = save_shown()
    print(f"shown_options.json: {led['shown_count']} shown, {led['unseen_remaining']} of {led['pool_size']} still unseen")
    if not a.no_embed: render_index(deck)

if __name__ == "__main__":
    main()
