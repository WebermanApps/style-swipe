#!/usr/bin/env python3
"""
Style Swipe deck generator for Max Weberman.

Usage:
  python3 generate_deck.py                       # deck for today
  python3 generate_deck.py --date 2026-10-10     # deck for a given date
  python3 generate_deck.py --ingest results.json # fold exported swipe results into profile.json
  python3 generate_deck.py --ingest r.json --date 2026-10-10   # ingest, then generate next deck
Options:
  --pairs N        number of pairs (default 25)
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

# ---------------------------------------------------------------------------
# 2026-10-10 additions: work-focused categories (SiteAgent AI construction startup, this week's Short,
# channel trailer, tenant/lender/partner messages, the Japanese-modern dream home, the Japan akiya hunt).
# ---------------------------------------------------------------------------
POOL_2026_10_10 = {
 "SiteAgent Brand Marks": [
  logo("sa_hex_bolt", "Hex Bolt Mark", "Bolt-head hexagon with an S, hi-vis orange on charcoal.", ["industrial","bold","construction","technical"], "S", "SiteAgent", "archivo", "#ff6b00", "#1f1f1f", "hex", 800, "0.02em", False, False),
  logo("sa_chat_bubble", "Chat Bubble Mark", "Leaf-shaped speech bubble: an assistant you talk to.", ["friendly","modern","technical","soft"], "S", "SiteAgent", "manrope", "#139a8f", "#f4fbfa", "rounded", 800, "0.01em", False, False),
  logo("sa_blueprint_outline", "Blueprint Outline", "Outlined letter on graph lines, white on blueprint blue.", ["technical","cool","construction","minimal"], "S", "SiteAgent", "grotesk", "#ffffff", "#0b3d91", "outline", 700, "0.04em"),
  logo("sa_bilingual_lockup", "Bilingual Lockup", "English name over Thai, one rule between.", ["bilingual","thai","friendly","clear"], "", "SiteAgent|ผู้ช่วยไซต์งาน AI", "kanit", "#16302e", "#ffffff", "bilingual", 700, "0.02em", False, False, "#139a8f"),
  logo("sa_lowercase_dot", "Lowercase With Dot", "Quiet lowercase wordmark, one orange period.", ["minimal","modern","calm","clean"], "", "siteagent.", "dmsans", "#1b1b1b", "#f6f3ec", "none", 700, "-0.01em", False, False, "#ff6b00"),
  logo("sa_level_underline", "Spirit-Level Underline", "Tall condensed caps sitting on a lime level bar.", ["bold","practical","construction","direct"], "", "SITEAGENT", "oswald", "#1f1f1f", "#f4f4f1", "underline", 700, "0.06em", False, True, "#a4c639"),
  logo("sa_terminal", "Terminal Snake Case", "site_agent in mono, green on black, for the tech crowd.", ["technical","dark","raw","minimal"], "", "site_agent", "plexmono", "#39ff14", "#050805", "none", 600, "0", False, False),
  logo("sa_sunrise", "Sunrise Over Site", "Half sun rising behind the name: early-start energy.", ["warm","tropical","friendly","thai"], "", "SiteAgent", "prompt", "#3b2a1a", "#fff5e1", "sun", 700, "0.01em", False, False, "#f7a325"),
  logo("sa_split_square", "Diagonal Split Tile", "SA on a two-tone diagonal tile, like a caution plate.", ["bold","geometric","modern","construction"], "SA", "SiteAgent", "montserrat", "#1f1f1f", "#ffffff", "split", 800, "0.02em", False, False, "#ffb703"),
  logo("sa_ring_seal", "Inspector's Ring Seal", "SA inside a double ring, like an approval stamp.", ["trust","craft","classic","earthy"], "SA", "SiteAgent", "fraunces", "#3a2e22", "#f4ecd8", "ring", 700, "0.03em", False, False),
  logo("sa_foreman_hand", "Foreman's Handwriting", "Marker-on-plywood script. Human, not corporate.", ["personal","playful","craft","casual"], "", "SiteAgent", "caveat", "#1b1b1b", "#e9d8b4", "none", 700, "0", False, False),
  logo("sa_safety_shield", "Safety Shield", "Black shield, yellow SA: safety first, literally.", ["construction","trust","bold","traditional"], "SA", "SiteAgent", "anton", "#ffd60a", "#111111", "shield", 400, "0.04em"),
 ],
 "SiteAgent Pitch Page": [
  hero("sa_hero_bilingual", "Bilingual Hero", "English headline with Thai right under it, EN/TH toggle.", ["bilingual","thai","friendly","light"], "#eef6f5", "#16302e", "#139a8f", "kanit", "bilingual", "The AI Site Assistant|ผู้ช่วยไซต์งาน AI สำหรับผู้รับเหมา", "", "Try A Demo"),
  hero("sa_hero_chat", "Ask-Your-Site Chat Box", "The hero is a chat box, like talking to a foreman.", ["modern","friendly","technical","clean"], "#f7f8fa", "#1f2937", "#139a8f", "manrope", "chat", "Ask Your Site Anything", "Daily reports, safety briefs, and client updates.", "Ask"),
  hero("sa_hero_blueprint", "Blueprint Grid", "Graph-paper blue with a floor-plan sketch.", ["technical","construction","cool","bold"], "#0b3d91", "#ffffff", "#ffd166", "grotesk", "blueprint", "Every Site, One Daily Report", "Photos in, report out, in Thai and English.", "See A Sample"),
  hero("sa_hero_bigtype", "Giant Promise", "One huge line and nothing else.", ["bold","direct","minimal","modern"], "#ffffff", "#111111", "#ff6b00", "anton", "bigtype", "FEWER SURPRISES ON SITE.", "", "Book A Pilot"),
  hero("sa_hero_photo", "Real Site Photo", "Full-bleed job-site photo with headline overlay.", ["cinematic","natural","construction","bold"], "#000", "#ffffff", "#ffb703", "kanit", "fullbleed", "Built For Thai Builders", "An AI assistant that lives on your site.", "Get Early Access", "base_site"),
  hero("sa_hero_cards", "Three Feature Cards", "Headline plus three simple feature tiles.", ["practical","clear","friendly","light"], "#f4f4f1", "#1f1f1f", "#ff6b00", "dmsans", "cards", "What SiteAgent Does For You", "Site Report|Safety Brief|Client Update", "Start"),
  hero("sa_hero_trust", "Builder-To-Builder Trust", "Centered promise with a trust line and logo strip.", ["trust","classic","calm","personal"], "#fbfaf6", "#1b1b1b", "#8b5a2b", "lora", "trust", "Made By A Builder, For Builders", "From someone who runs real jobs", "Talk To Max"),
  hero("sa_hero_map", "Sites On A Map", "Map with site pins beside a short pitch.", ["practical","technical","modern","clear"], "#ffffff", "#16302e", "#139a8f", "inter", "map", "All Your Sites, One Screen", "Progress, photos, and issues by location.", "View Demo"),
  hero("sa_hero_illus", "Friendly Illustration", "Soft sun-and-mountain illustration, warm colors.", ["friendly","warm","playful","soft"], "#ffd8b8", "#4a3426", "#e07a3f", "nunito", "illus", "Your Site, Explained Simply", "No training needed. Just send photos.", "Try It Free"),
  hero("sa_hero_video", "Play-The-Demo Video", "Big site photo with a play button: watch a day on site.", ["storytelling","cinematic","youtube","natural"], "#000", "#ffffff", "#a4c639", "outfit", "video", "See A Day On Site In 60 Seconds", "Watch how one report gets made.", "", "base_site"),
  hero("sa_hero_form", "Pilot Sign-Up Form", "Headline left, three-field pilot form right.", ["direct","practical","construction","clear"], "#f4f4f1", "#1f1f1f", "#ffb703", "manrope", "form", "Book A Pilot For Your Crew", "Set up in one afternoon.", "Book Pilot"),
  hero("sa_hero_magazine", "Magazine Cover", "Editorial cover look: 'The New Foreman'.", ["editorial","bold","cinematic","modern"], "#000", "#ffffff", "#ff6b00", "playfair", "magazine", "THE NEW FOREMAN", "AI for Southeast Asian job sites", "", "base_site", "contrast(1.1)"),
 ],
 "SiteAgent Product Voice": [
  tone2("sa_v_checklist", "Checklist Direct", "Facts and fixes, nothing else.", ["direct","efficient","practical","minimal"], "Rebar check on Level 2: 3 items open.", "Fix before the pour: spacing, ties, cover.", "SiteAgent → Foreman"),
  tone2("sa_v_coach", "Friendly Coach", "Encouraging first, then the ask.", ["friendly","warm","personal","soft"], "Morning, team! Great progress yesterday.", "Two quick safety things before the crew starts.", "SiteAgent → Foreman"),
  tone2("sa_v_bilingual", "Bilingual Line-By-Line", "Every alert in English, then Thai.", ["bilingual","thai","direct","clear"], "Pour moved to 2pm because of rain.", "เทปูนเลื่อนเป็นบ่ายสองโมงเพราะฝนตก", "SiteAgent → Crew"),
  tone2("sa_v_formal", "Formal Report", "Reads like an official document.", ["formal","trust","classic","calm"], "Daily Site Report, October 10.", "Work is on schedule. No incidents were recorded.", "SiteAgent → Owner"),
  tone2("sa_v_emoji", "Emoji Casual", "Chatty, celebratory, LINE-app vibe.", ["playful","casual","friendly","vibrant"], "✅ Slab poured! 🎉", "Next up: keep it wet for 7 days 💧", "SiteAgent → Crew"),
  tone2("sa_v_data", "Numbers First", "A dashboard in one line.", ["technical","minimal","efficient","modern"], "Crew 14 · Rain 0 mm · Progress 62%", "Roofing is 1 day behind plan.", "SiteAgent → Owner"),
  tone2("sa_v_stop", "Stop-Work Urgent", "Caps, short, impossible to ignore.", ["bold","direct","construction","loud"], "STOP: no harness on the east scaffold.", "Photo attached. Fix it and reply DONE.", "SiteAgent → Foreman"),
  tone2("sa_v_heads_up", "Calm Heads-Up", "Gentle suggestion, not an order.", ["calm","soft","friendly","polite"], "Heads up: rain is likely after 3pm.", "It might be worth covering the rebar before lunch.", "SiteAgent → Foreman"),
  tone2("sa_v_story", "Homeowner Story", "Turns progress into a little story for the client.", ["storytelling","warm","personal","natural"], "Your kitchen walls went up today.", "Here's the view from where your sink will be.", "SiteAgent → Homeowner"),
  tone2("sa_v_thanks", "Polite Thank-You", "Thai-style courtesy before business.", ["polite","warm","calm","thai"], "Thank you, team. Today went smoothly.", "Tomorrow's plan is attached. Please check it when you have a moment.", "SiteAgent → Crew"),
 ],
 "Shorts Cover Styles": [
  thumb("sh_bigtext_bowl", "Big Bold Caption", "Two-tone giant words, food-spot energy.", ["bold","loud","youtube","vibrant"], "#1b4332", "#ffffff", "#a4c639", "bebas", "bigtext", "BUILD YOUR BOWL"),
  thumb("sh_bilingual_spot", "Bilingual Label Stack", "English line over a Thai line, sticker style.", ["bilingual","thai","friendly","clear"], "#ffffff", "#1b1b1b", "#f6b93b", "kanit", "bilingual", "Fresh Lunch Spot|ร้านสลัดสดใหม่"),
  thumb("sh_hand_note", "Handwritten Note", "Tilted handwriting, like a diary entry.", ["personal","casual","warm","craft"], "#c8a97e", "#ffffff", "#ffffff", "caveat", "hand", "my new lunch spot"),
  thumb("sh_price_tag", "Price-Tag Sticker", "Rotated sticker asking the value question.", ["playful","bold","youtube","practical"], "#2d4a22", "#ffffff", "#ffd60a", "archivo", "price", "WORTH IT?"),
  thumb("sh_pin_place", "Map Pin Place", "Location pin with a short place line.", ["travel","natural","friendly","clean"], "#3e5641", "#ffffff", "#ff8c42", "outfit", "pin", "Found: Healthy Lunch"),
  thumb("sh_lower_third", "Lower-Third Title", "Quiet title in the lower third with a thin accent line.", ["editorial","calm","minimal","natural"], "#5a7d4f", "#ffffff", "#f6b93b", "dmsans", "lower", "Fresh, Fast, Local"),
  thumb("sh_face_react", "Reaction Face", "Big surprised face plus caption.", ["loud","youtube","energetic","playful"], "#ff8c42", "#ffffff", "#ffd60a", "anton", "face", "DIDN'T EXPECT THIS"),
  thumb("sh_journal_tab", "Journal Tab", "Small label tab, like a page in a daily journal.", ["minimal","personal","calm","light"], "#fff5e1", "#3b2a1a", "#3b2a1a", "mitr", "tab", "Daily Journal · Lunch"),
  thumb("sh_arrows", "Circle And Arrow", "Red-circle-and-arrow callout.", ["bold","playful","youtube","loud"], "#264653", "#ffffff", "#ff3b30", "oswald", "arrows", "LOOK AT THIS"),
  thumb("sh_soft_big", "Soft Big Caption", "Big words but in calm pastel greens.", ["soft","light","natural","friendly"], "#c6e377", "#1b4332", "#ffffff", "nunito", "bigtext", "GREEN AND GOOD"),
 ],
 "Channel Trailer Pacing": [
  pace("ct_montage", "30-Second Montage", "Fast cuts of the best family moments, music-driven.", ["energetic","storytelling","bold","youtube"], [1,1,2,1,1,2,1,1,2,1,1,2], ["#f7a325","#e23e7c"], ["~1.3s shots","music-led","no talking"]),
  pace("ct_talk_camera", "Talk-To-Camera Intro", "You on camera saying who you are and why to subscribe.", ["personal","direct","honest","trust"], [10,4,6,8], ["#1d3c6e","#f4ecd8"], ["you on camera","b-roll inserts","clear ask"]),
  pace("ct_day_arc", "Morning-To-Night Arc", "One day in Thailand, from coffee to sunset.", ["storytelling","calm","natural","warm"], [3,3,4,3,5,4], ["#ffd8b8","#3e5641"], ["one day","time-of-day arc","soft music"]),
  pace("ct_chapters", "Title-Card Chapters", "Bold text cards: Family · Building · Thailand.", ["clear","editorial","minimal","modern"], [2,5,2,5,2,5], ["#111111","#ffffff"], ["text cards","3 chapters","even rhythm"]),
  pace("ct_family_open", "Slow Family Open", "Starts on a quiet family moment, holds it.", ["warm","personal","calm","soft"], [8,6,8], ["#c8a97e","#8fb08c"], ["long holds","natural sound","gentle music"]),
  pace("ct_hook_question", "Hook Question Open", "Opens on a question, then answers it fast.", ["bold","youtube","energetic","direct"], [1,2,1,2,8], ["#ff006e","#ffd60a"], ["question hook","quick payoff","subscribe card"]),
  pace("ct_bilingual_subs", "Bilingual Subtitles Throughout", "Even pacing with English and Thai captions on everything.", ["bilingual","thai","friendly","clear"], [4,4,4,4,4], ["#139a8f","#ffffff"], ["EN + TH captions","steady cuts","voiceover"]),
  pace("ct_one_take", "One-Take Walk", "A single unbroken walk-and-talk shot.", ["raw","honest","cinematic","personal"], [30], ["#4a4a48","#d9cba3"], ["single take","handheld","no edits"]),
 ],
 "Tenant & Partner Messages": [
  tone2("tm_receipt_brief", "Receipt: Brief", "One line, done.", ["direct","efficient","minimal","clear"], "Your October rent receipt is attached.", "Thanks for paying on time.", "Max → Tenant"),
  tone2("tm_receipt_warm", "Receipt: Warm", "Friendly, with an open door.", ["warm","friendly","personal","soft"], "Hi! Your October receipt is attached.", "Really appreciate you both. Let me know if the house needs anything.", "Max → Tenant"),
  tone2("tm_receipt_formal", "Receipt: Formal", "Letter-style and complete.", ["formal","classic","trust","polite"], "Please find attached your rent receipt for October 2026.", "Kindly keep it for your records.", "Max → Tenant"),
  tone2("tm_visit_options", "Visit: Two Options", "Offer two times, let them pick.", ["direct","practical","friendly","efficient"], "Could I stop by for a quick visit this week?", "Would Tuesday 5pm or Saturday 10am work better?", "Max → Tenant"),
  tone2("tm_visit_why", "Visit: Explain Why", "Say what and how long before asking when.", ["honest","clear","personal","polite"], "I'd like to swap out the old mirror and check a couple small things.", "It should take about 20 minutes. What time suits you?", "Max → Tenant"),
  tone2("tm_bundle_list", "Bundled List", "Several asks in one numbered text.", ["efficient","minimal","direct","practical"], "Two quick things:", "1) Mirror pickup before the 16th. 2) A visit window, your pick.", "Max → Tenant"),
  tone2("tm_lender_formal", "Lender: Formal", "Clean and official for a bank or insurer.", ["formal","polite","trust","calm"], "Hello, please find the evidence of insurance for the loan attached.", "Let me know if you need anything else from me.", "Max → Lender"),
  tone2("tm_lender_casual", "Lender: Casual", "Relaxed, even with a bank.", ["casual","friendly","light","personal"], "Hi! Sending over the insurance proof you asked for.", "Shout if anything's missing.", "Max → Lender"),
  tone2("tm_partner_direct", "Partner: Straight To Numbers", "Recap, then a deadline.", ["direct","trust","practical","clear"], "Quick recap of where we stand. The numbers are below.", "Can we lock the last open points this week?", "Max → Partner"),
  tone2("tm_partner_warm", "Partner: Relationship First", "Thanks first, details later, in person.", ["warm","personal","calm","friendly"], "Thanks again for being part of this.", "When you have 15 minutes, I'd love to walk through the last details together.", "Max → Partner"),
 ],
 "Dream Home Finishes": [
  mood("dh_engawa_teak", "Engawa In Teak", "Oiled teak veranda, paper screens, river stones.", ["japanese","natural","warm","craft"], ["#8b5a2b","#c19a6b","#f4ecd8","#3e5641","#2b2b2b"], ["teak decking","shoji screens","river stone"]),
  mood("dh_engawa_composite", "Engawa In Grey Composite", "Low-maintenance grey decking with slim steel posts.", ["modern","practical","cool","minimal"], ["#6b6e70","#a9a9a2","#e9ecee","#2f3a40","#7d9a6f"], ["composite deck","steel posts","gravel"]),
  mood("dh_shou_sugi", "Charred Timber Outside", "Black charred cladding outside, warm wood inside.", ["japanese","dark","craft","bold"], ["#1b1b1b","#3a2e22","#c8a97e","#f2f0eb","#5a7d4f"], ["charred cedar","white plaster","bronze"]),
  mood("dh_lime_teak", "Lime Plaster And Teak", "Soft white plaster walls with teak and clay tile.", ["light","natural","thai","warm"], ["#f6f3ec","#e8e2d0","#8b5a2b","#a3b18a","#3f4540"], ["lime plaster","teak","clay tile"]),
  mood("dh_wellness_hinoki", "Wellness Wing: Hinoki Spa", "Hinoki tub, slate floor, steam and silence.", ["japanese","calm","natural","minimal"], ["#e9d8b4","#c9b38a","#8e8e8a","#f7f5ef","#3f4540"], ["hinoki wood","slate","pebble floor"]),
  mood("dh_wellness_resort", "Wellness Wing: Jungle Resort", "Open-air shower, terrazzo, ferns, rattan.", ["tropical","resort","natural","light"], ["#2f5d3a","#8fb08c","#d9cba3","#ffffff","#6b4226"], ["terrazzo","rattan","open shower","ferns"]),
  mood("dh_music_walnut", "Music Office: Walnut Acoustic", "Walnut slat walls, wool felt, warm lamps.", ["warm","craft","personal","calm"], ["#5c3d2e","#a47551","#d8c3a5","#2b2b2b","#b5651d"], ["walnut slats","wool felt","cork"]),
  mood("dh_music_studio", "Music Office: Raw Studio", "Concrete, steel shelving, gear on display.", ["industrial","technical","raw","modern"], ["#2b2d31","#6c757d","#cfd4da","#ff6b00","#f8f9fa"], ["acoustic panels","concrete","steel shelving"]),
  mood("dh_kitchen_concrete", "Kitchen: Concrete And Oak", "Polished concrete counters, white oak, brass tap.", ["modern","industrial","minimal","light"], ["#bdbcb6","#8e8e8a","#d9c3a0","#f2f0eb","#3a3a3a"], ["polished concrete","white oak","brass tap"]),
  mood("dh_kitchen_tile", "Kitchen: Handmade Tile", "Glossy handmade tile, teak shelves, a pop of mango.", ["craft","warm","playful","natural"], ["#3e7c8c","#e9e4d8","#8b5a2b","#f6b93b","#ffffff"], ["zellige tile","teak","open shelving"]),
  mood("dh_pool_slate", "Plunge Pool: Dark Slate", "Dark stone pool that mirrors the mountains.", ["dark","calm","luxe","natural"], ["#253237","#3d5a61","#9aa5ab","#e0e0d8","#5a7d4f"], ["dark slate","infinity edge","bamboo"]),
  mood("dh_pool_mosaic", "Plunge Pool: Turquoise Mosaic", "Bright mosaic pool, sandstone edge, frangipani.", ["tropical","vibrant","light","playful"], ["#00a6a6","#7fd1c7","#f0e6d2","#ffffff","#c1502e"], ["turquoise mosaic","sandstone","frangipani"]),
 ],
 "Japan Cottage Makeover": [
  mood("jc_keep_old", "Keep The Old Bones", "Dark beams, tatami, paper doors, barely touched.", ["traditional","rustic","japanese","calm"], ["#3a2e22","#6b4f2a","#d9cba3","#f3ead3","#2b2b2b"], ["old beams","tatami","fusuma doors"]),
  mood("jc_white_gut", "Bright White Refresh", "White walls, birch floors, everything light.", ["minimal","light","modern","clean"], ["#ffffff","#f2f0eb","#e3d9c6","#c2a878","#3a3a3a"], ["white paint","birch","linen"]),
  mood("jc_kominka_cafe", "Old-House Cafe Vibe", "Warm wood, plants, vintage lamps, a little retro.", ["warm","craft","retro","personal"], ["#8b5a2b","#d8c3a5","#3e5641","#f6b93b","#2b2b2b"], ["vintage lamps","plants","worn wood"]),
  mood("jc_beam_loft", "Beams And Steel Loft", "Open it up to the rafters, add black steel.", ["industrial","raw","modern","bold"], ["#2b2b2b","#5a4632","#a9a9a2","#e8e4dc","#b5651d"], ["exposed rafters","black steel","concrete floor"]),
  mood("jc_family_tough", "Family-Tough Practical", "Durable floors, lots of storage, kid-proof.", ["practical","friendly","light","natural"], ["#e9e4d8","#c8a97e","#7d9a6f","#ffffff","#4a4a3a"], ["vinyl plank","built-in storage","washable paint"]),
  mood("jc_guesthouse", "Rental-Ready Guesthouse", "Simple, clean, photographs well for bookings.", ["clean","practical","modern","calm"], ["#f7f5ef","#d9d4c7","#9aa5a0","#3f4540","#c19a6b"], ["simple furniture","good lighting","neutral textiles"]),
  mood("jc_thai_fusion", "Thai-Japanese Fusion", "Rattan and teak brought into a Japanese house.", ["thai","tropical","warm","japanese"], ["#8b5a2b","#c8a97e","#2f5d3a","#f4ecd8","#c1502e"], ["rattan","teak","indigo textiles"]),
  mood("jc_wabi_clay", "Wabi-Sabi Clay", "Clay walls, imperfect pottery, quiet earth tones.", ["earthy","calm","natural","craft"], ["#a47551","#c9b38a","#e8dcc2","#6b6e70","#3a2e22"], ["clay plaster","handmade pottery","stone"]),
 ],
}
for _cat, _opts in POOL_2026_10_10.items():
    POOL.setdefault(_cat, []).extend(_opts)

# ---------------------------------------------------------------------------
# 2026-10-10 (round 2) additions: deeper refinement inside Max's liked space (warm, light, modern,
# industrial, construction, clear, bilingual, friendly, rustic, natural) for SiteAgent + SMART visa,
# the Japanese-modern dream home, the Japan akiya, @AMomentInThai Shorts, and tenant/lender messages.
# A few disliked directions (playful, vibrant, luxe, editorial, japanese+minimal, dark) are kept as checks.
# ---------------------------------------------------------------------------
POOL_2026_10_10C = {
 "SiteAgent Brand Marks": [
  logo("sa2_roof_s", "Roof-Peak S", "An S tucked under a simple roof line, warm terracotta.", ["construction","warm","friendly","clear"], "S", "SiteAgent", "montserrat", "#c1502e", "#fbf6ee", "house", 800, "0.01em", False, False),
  logo("sa2_hex_light", "Light Hex Nut", "Steel-grey hex on off-white: industrial but light.", ["industrial","light","modern","construction"], "S", "SiteAgent", "chakra", "#4a4a48", "#f4f4f1", "hex", 700, "0.04em", False, False),
  logo("sa2_bilingual_kanit", "Kanit Bilingual Stack", "Bold Kanit English over Thai, teal rule.", ["bilingual","thai","modern","clear"], "", "SiteAgent|ไซต์เอเจนต์", "kanit", "#1b1b1b", "#f6f3ec", "bilingual", 700, "0.02em", False, False, "#139a8f"),
  logo("sa2_tape_measure", "Tape-Measure Underline", "Clean name on a yellow tape-measure bar.", ["construction","clear","friendly","practical"], "", "SiteAgent", "manrope", "#1f1f1f", "#ffffff", "underline", 800, "0.01em", False, False, "#ffc300"),
  logo("sa2_rounded_tile", "Rounded App Tile", "Soft-cornered SA app icon in clay orange.", ["modern","friendly","warm","clean"], "SA", "SiteAgent", "outfit", "#d9693b", "#fff8f0", "rounded", 800, "0.02em", False, False),
  logo("sa2_kraft_stamp", "Kraft Site Stamp", "Ink ring stamp on kraft: approved on site.", ["rustic","craft","construction","warm"], "SA", "SiteAgent · Approved", "spacemono", "#1b1b1b", "#c8a97e", "ring", 700, "0.05em"),
  logo("sa2_blueprint_light", "Light Blueprint Line", "Blue outline letter on pale graph paper.", ["technical","light","clear","construction"], "S", "SiteAgent", "grotesk", "#0b3d91", "#eef3f9", "outline", 600, "0.06em"),
  logo("sa2_sun_teal", "Morning Shift Arc", "Teal half-sun behind the name: early starts.", ["warm","friendly","natural","light"], "", "SiteAgent", "nunito", "#16302e", "#f4fbfa", "sun", 800, "0.01em", False, False, "#7fd1c7"),
  logo("sa2_wood_circle", "Timber Circle", "Oiled-wood brown circle mark, natural feel.", ["natural","rustic","warm","modern"], "S", "SiteAgent", "fraunces", "#8b5a2b", "#f7f1e3", "circle", 700, "0.02em", False, False),
  logo("sa2_split_steel", "Steel & Safety Split", "Diagonal steel-grey and safety-orange tile.", ["industrial","construction","modern","bold"], "SA", "SITEAGENT", "oswald", "#2f3a40", "#f4f4f1", "split", 700, "0.08em", False, True, "#ff6b00"),
  logo("sa2_neon_play", "Neon Pop Bubble", "Hot-pink bubble icon. (Playful/vibrant check.)", ["playful","vibrant","bold","youtube"], "S", "SiteAgent", "syne", "#ff006e", "#fff0f6", "circle", 800, "0", False, False),
  logo("sa2_gold_luxe", "Gold Serif Crest", "Gold ring on black, serif caps. (Luxe/dark check.)", ["luxe","dark","classic","formal"], "SA", "SITEAGENT", "cormorant", "#c9a227", "#0b0b0b", "ring", 600, "0.2em"),
 ],
 "SiteAgent Pitch Page": [
  hero("sa2_hero_photo_light", "Bright Site Photo", "Airy daylight site photo, short promise, orange button.", ["construction","light","natural","clear"], "#000", "#ffffff", "#ff8c42", "dmsans", "fullbleed", "Site Reports In Two Minutes", "Photos in, Thai and English report out.", "Book A Pilot", "base_site", "brightness(1.15) saturate(.9)"),
  hero("sa2_hero_bilingual_warm", "Warm Bilingual Hero", "Cream background, Kanit headline, Thai under it.", ["bilingual","warm","thai","friendly"], "#fff8f0", "#3b2a1a", "#d9693b", "kanit", "bilingual", "Your AI Site Assistant|ผู้ช่วยงานก่อสร้างของคุณ", "SiteAgent", "Try It"),
  hero("sa2_hero_cards_steel", "Steel Feature Cards", "Three cards on concrete grey: Report, Safety, Client.", ["industrial","clear","modern","practical"], "#e9ecee", "#1f1f1f", "#ff6b00", "manrope", "cards", "One Assistant For Every Site", "Report|Safety|Client", ""),
  hero("sa2_hero_split_portrait", "Founder Split", "Max on the right, builder-to-builder promise left.", ["personal","friendly","trust","warm"], "#f6f3ec", "#3b2a1a", "#8b5a2b", "outfit", "split", "Built By A Builder", "I run real sites. SiteAgent is what I wanted.", "Talk To Max", "base_site"),
  hero("sa2_hero_form_light", "Light Pilot Form", "White page, form right, nothing else to read.", ["clear","light","direct","modern"], "#ffffff", "#1b1b1b", "#139a8f", "dmsans", "form", "Start A Free Pilot", "Set up in one afternoon.", "Start"),
  hero("sa2_hero_blueprint_light", "Pale Blueprint", "Light-blue graph paper, sketch plan, dark text.", ["technical","construction","light","clear"], "#dce8f5", "#0b3d91", "#ff8c42", "grotesk", "blueprint", "Every Site, One Clear Report", "Structural · Safety · Progress", "See Sample"),
  hero("sa2_hero_map_thai", "Thai Sites Map", "Map with pins across Thailand and a site list.", ["practical","clear","thai","modern"], "#f4fbfa", "#16302e", "#139a8f", "sarabun", "map", "All Your Sites", "Bangkok · Chiang Mai · Phuket", "Open Dashboard"),
  hero("sa2_hero_chat_warm", "Warm Chat Hero", "Chat box on cream: 'Ask your site anything'.", ["friendly","warm","modern","clear"], "#fbf6ee", "#3b2a1a", "#d9693b", "nunito", "chat", "Ask Your Site Anything", "In English or Thai.", "Ask"),
  hero("sa2_hero_trust_numbers", "Pilot Results Strip", "Headline plus three pilot numbers.", ["trust","clear","construction","direct"], "#ffffff", "#1f1f1f", "#2bb673", "manrope", "trust", "Pilots Saved 6 Hours A Week", "★★★★★ from Thai foremen", "Read Case Study"),
  hero("sa2_hero_bigtype_warm", "Warm Giant Line", "Huge headline on sand, one orange rule.", ["bold","warm","direct","modern"], "#f6e7d0", "#3b2a1a", "#d9693b", "anton", "bigtype", "LESS PAPER. MORE BUILDING.", "", "Book Demo"),
  hero("sa2_hero_dark_video", "Dark Cinematic Demo", "Black page, moody demo video. (Dark check.)", ["dark","cinematic","bold","modern"], "#0b0b0b", "#ffffff", "#2dd4bf", "inter", "video", "The Future Of The Job Site", "90-second film", "Play", "base_site", "brightness(.55)"),
  hero("sa2_hero_vibrant_illus", "Candy Gradient Illustration", "Bright pink-purple gradient. (Vibrant/playful check.)", ["vibrant","playful","friendly","bold"], "linear-gradient(135deg,#ff7eb6,#7c3aed)", "#ffffff", "#ffe066", "syne", "illus", "Sites, But Fun", "AI for builders", "Let's Go"),
 ],
 "SiteAgent Product Voice": [
  tone2("sa2_v_morning_brief", "Morning Brief, Bilingual", "Three lines, EN then TH, sent at 7am.", ["bilingual","clear","construction","friendly"], "Today: formwork L3, rebar delivery 10am, rain after 4.", "วันนี้: แบบหล่อชั้น 3, เหล็กมาส่ง 10 โมง, ฝนหลัง 4 โมง", "SiteAgent → Crew"),
  tone2("sa2_v_plain_owner", "Plain Owner Update", "Plain words, one photo, no jargon.", ["clear","warm","friendly","natural"], "Your roof frame is up. It's level and on schedule.", "Next week we start the tiles.", "SiteAgent → Homeowner"),
  tone2("sa2_v_foreman_peer", "Foreman-To-Foreman", "Talks like a seasoned site boss.", ["direct","construction","rustic","practical"], "Mesh on the east slab is sitting on the dirt.", "Chair it up before the pour. 20 minutes, tops.", "SiteAgent → Foreman"),
  tone2("sa2_v_safety_kind", "Kind Safety Reminder", "Firm on safety, warm in tone.", ["friendly","construction","warm","clear"], "Quick one: two guys on the scaffold without harnesses.", "Let's get them clipped in before break. Thanks, team.", "SiteAgent → Foreman"),
  tone2("sa2_v_summary_numbers", "Week In Numbers", "Numbers with one plain-English line.", ["clear","modern","direct","practical"], "Week 6: 71% done (+9). 0 incidents. 2 open issues.", "Biggest risk: window delivery next Tuesday.", "SiteAgent → Owner"),
  tone2("sa2_v_thai_polite", "Polite Thai Partner", "Krab-polite, respectful to subcontractors.", ["thai","bilingual","warm","friendly"], "Khun Somsak krab, the tile delivery is confirmed for Friday.", "Please let me know if your team needs anything krab.", "SiteAgent → Subcontractor"),
  tone2("sa2_v_lender_ready", "Lender-Ready Progress", "Structured draw-request style progress note.", ["trust","clear","modern","construction"], "Milestone 3 (structure) complete. Photos and inspection attached.", "Requesting draw #3 per schedule.", "SiteAgent → Lender"),
  tone2("sa2_v_quick_fix", "Problem + Fix", "Every issue arrives with a suggested fix.", ["direct","practical","friendly","clear"], "Drain on the north side is pooling.", "Suggested fix: add 2% fall and a gravel trench. Approve?", "SiteAgent → Foreman"),
  tone2("sa2_v_rustic_humor", "Dry Site Humor", "A bit of site banter, still useful.", ["rustic","casual","warm","direct"], "The cement mixer is back from vacation.", "Pour's on for 7am. Bring coffee.", "SiteAgent → Crew"),
  tone2("sa2_v_visual_first", "Photo-First Caption", "Short caption under a marked-up photo.", ["clear","modern","natural","practical"], "📷 Crack at column C4, hairline, 0.2 mm.", "Monitor only. Re-check in 7 days.", "SiteAgent → Engineer"),
  tone2("sa2_v_hype", "Hype Announcer", "All caps celebration. (Playful/vibrant check.)", ["playful","vibrant","loud","energetic"], "LET'S GOOO! SLAB DAY! 🔥🔥", "Crew is CRUSHING it today!!", "SiteAgent → Crew"),
  tone2("sa2_v_luxe_concierge", "Concierge Formal", "Five-star hotel register. (Luxe/formal check.)", ["luxe","formal","calm","classic"], "Good morning. Your residence progresses gracefully.", "Should you wish, a private site viewing can be arranged.", "SiteAgent → Owner"),
 ],
 "SMART Visa Pitch Deck": [
  hero("sv_title_bilingual", "Bilingual Title Slide", "Name, one-line pitch, EN/TH.", ["bilingual","clear","thai","modern"], "#ffffff", "#16302e", "#139a8f", "kanit", "bilingual", "SiteAgent|AI สำหรับงานก่อสร้างไทย", "SMART Visa application · 2026", ""),
  hero("sv_problem_bigtype", "Problem In One Line", "Giant statement of the problem.", ["direct","bold","clear","construction"], "#f4f4f1", "#1f1f1f", "#ff6b00", "anton", "bigtype", "THAI SITES LOSE 1 DAY A WEEK TO PAPER.", "", ""),
  hero("sv_market_map", "Market Map Slide", "Thailand map with site density and numbers.", ["clear","technical","modern","thai"], "#f4fbfa", "#16302e", "#139a8f", "sarabun", "map", "Market: 90,000 Active Sites", "Bangkok · EEC · North · South", ""),
  hero("sv_product_cards", "Product In Three Cards", "Capture, Report, Act.", ["clear","modern","friendly","practical"], "#ffffff", "#1f2937", "#2563eb", "dmsans", "cards", "How SiteAgent Works", "Capture|Report|Act", ""),
  hero("sv_founder", "Founder Credibility", "Max's photo, years building, why him.", ["personal","trust","warm","construction"], "#fbf6ee", "#3b2a1a", "#8b5a2b", "outfit", "split", "Founder: Max Weberman", "US contractor (LLC) · building in Thailand", "", "base_site"),
  hero("sv_traction_numbers", "Traction Numbers", "Pilots, hours saved, sites live.", ["trust","clear","direct","modern"], "#ffffff", "#0f2340", "#2bb673", "manrope", "trust", "3 Pilots · 14 Sites · 6 h/week Saved", "Letters of intent attached", ""),
  hero("sv_blueprint_tech", "Tech Architecture Slide", "Blueprint-style system diagram.", ["technical","construction","clear","industrial"], "#0b3d91", "#ffffff", "#ffd166", "chakra", "blueprint", "Technology & IP", "On-device vision · Thai NLP · Offline-first", ""),
  hero("sv_jobs_thai", "Thai Jobs Impact", "How many Thai jobs and skills it creates.", ["thai","warm","clear","trust"], "#fff8f0", "#3b2a1a", "#d9693b", "kanit", "center", "12 Thai Hires In 24 Months", "Engineering · Support · Field trainers", ""),
  hero("sv_warm_photo", "Warm Site Photo Cover", "Golden-hour site photo as cover slide.", ["warm","natural","construction","storytelling"], "#000", "#ffffff", "#f6b93b", "dmsans", "fullbleed", "Building Thailand, Smarter", "SMART Visa · Startup category", "", "base_site", "sepia(.3) saturate(1.2)"),
  hero("sv_ask_form", "The Ask Slide", "Clear ask: visa, funding, partners.", ["direct","clear","practical","modern"], "#f4f4f1", "#1f1f1f", "#139a8f", "manrope", "form", "What We Need", "SMART Visa · 5M THB seed · 2 pilot partners", ""),
  hero("sv_editorial_cover", "Magazine-Style Cover", "Big serif masthead cover. (Editorial check.)", ["editorial","classic","bold","formal"], "#000", "#ffffff", "#d62828", "playfair", "magazine", "THE NEW FOREMAN", "A SiteAgent story", "", "base_site", "contrast(1.1)"),
  hero("sv_dark_luxe", "Black & Gold Deck", "Black slides, gold lines. (Dark/luxe check.)", ["dark","luxe","formal","classic"], "#0b0b0b", "#f2ead8", "#c9a227", "cormorant", "center", "SiteAgent Holdings", "Confidential", ""),
 ],
 "SiteAgent App Screens": [
  ui("sa2_ui_light_teal", "Light Teal Field App", "White cards, teal actions, big touch targets.", ["light","clear","modern","friendly"], "#f4fbfa","#ffffff","#16302e","#139a8f",14,"dmsans","soft","1px solid #d7ebe8"),
  ui("sa2_ui_concrete_orange", "Concrete & Orange", "Concrete grey surfaces, safety-orange buttons.", ["industrial","construction","clear","modern"], "#e9ecee","#f8f9fa","#1f1f1f","#ff6b00",8,"manrope","soft","1px solid #cfd4da"),
  ui("sa2_ui_warm_sand", "Warm Sand", "Sand and clay tones, rounded, homey.", ["warm","friendly","natural","light"], "#f6efe4","#fffaf3","#3b2a1a","#d9693b",16,"nunito","soft"),
  ui("sa2_ui_bilingual", "Bilingual Labels", "Every label in English and Thai, Sarabun body.", ["bilingual","thai","clear","practical"], "#ffffff","#f7f8fa","#1f2937","#2563eb",10,"sarabun","soft","1px solid #e5e7eb"),
  ui("sa2_ui_kraft", "Kraft Clipboard", "Clipboard-and-kraft look, stamped type.", ["rustic","craft","construction","warm"], "#d8bf96","#efe1c6","#1b1b1b","#8b3a1a",4,"spacemono","none","2px solid #1b1b1b"),
  ui("sa2_ui_glove", "Glove-Friendly Big Buttons", "Huge buttons, high contrast, works with gloves.", ["construction","clear","direct","practical"], "#ffffff","#ffffff","#111111","#ffc300",6,"archivo","hard","2px solid #111"),
  ui("sa2_ui_timber", "Timber & Cream", "Cream app with oak-brown accents.", ["natural","warm","modern","rustic"], "#f7f1e3","#fffaf0","#3b2a1a","#8b5a2b",12,"outfit","soft","1px solid #eadfc8"),
  ui("sa2_ui_blueprint_light", "Pale Blueprint App", "Light blueprint blue with white cards.", ["technical","light","construction","clear"], "#dce8f5","#ffffff","#0b3d91","#ff8c42",8,"grotesk","soft","1px dashed #9db4d8"),
  ui("sa2_ui_line_green", "LINE-Style Chat Green", "Familiar chat-app green, friendly bubbles.", ["friendly","thai","modern","clear"], "#f2f7f2","#ffffff","#1b1b1b","#06c755",18,"prompt","soft"),
  ui("sa2_ui_steel_minimal", "Steel Minimal", "Cool steel greys, thin lines, very calm.", ["industrial","modern","minimal","light"], "#f1f3f5","#ffffff","#212529","#495057",4,"inter","none","1px solid #dee2e6"),
  ui("sa2_ui_dark_ops", "Dark Ops Dashboard", "Night-mode command center. (Dark check.)", ["dark","technical","bold","modern"], "#0f1115","#1a1d24","#e6e8ee","#ff6b00",10,"grotesk","glow","1px solid #2a2f3a"),
  ui("sa2_ui_candy", "Candy Gradient App", "Pink-violet gradient, bubbly. (Playful/vibrant check.)", ["playful","vibrant","soft","bold"], "linear-gradient(135deg,#ff7eb6,#7c3aed)","rgba(255,255,255,.85)","#2b1b3a","#ff006e",22,"syne","soft"),
 ],
 "Tenant & Partner Messages": [
  tone2("tm2_rent_bilingual", "Rent Reminder, Bilingual", "Friendly reminder in English and Thai.", ["bilingual","friendly","clear","warm"], "Hi Ploy, rent for November is due on the 5th.", "ค่าเช่าเดือนพฤศจิกายนครบกำหนดวันที่ 5 นะครับ ขอบคุณครับ", "Max → Tenant"),
  tone2("tm2_repair_eta", "Repair With ETA", "Exact time, who's coming, what to expect.", ["clear","direct","friendly","practical"], "Aircon tech Khun Lek is coming Tue 10-11am.", "About 30 minutes. No need to be home if the key box is OK.", "Max → Tenant"),
  tone2("tm2_move_in", "Warm Move-In Welcome", "Welcome note with the three things that matter.", ["warm","friendly","natural","clear"], "Welcome home! WiFi, trash day and my number are on the fridge.", "Message me anytime, I usually reply within the hour.", "Max → Tenant"),
  tone2("tm2_rent_rise", "Rent Increase, Plain & Fair", "Explains the why, gives time, offers options.", ["clear","trust","warm","direct"], "Next year's rent goes up 3%, from 12,000 to 12,360 THB.", "Costs went up 6%; I kept it at half. Happy to chat.", "Max → Tenant"),
  tone2("tm2_late_firm", "Late Payment, Firm & Kind", "Firm deadline, open door.", ["direct","clear","friendly","trust"], "Rent is 7 days late now. I need it by Friday.", "If something's going on, tell me and we'll make a plan.", "Max → Tenant"),
  tone2("tm2_inspection", "Inspection Notice", "Advance notice, purpose, duration.", ["clear","practical","polite","friendly"], "Quick heads-up: yearly safety check on Sat 9am, about 20 min.", "Smoke alarms, water heater, breaker panel. Thanks!", "Max → Tenant"),
  tone2("tm2_lender_monthly", "Lender Monthly Snapshot", "Occupancy, collections, issues in four lines.", ["clear","trust","modern","direct"], "October: 96% occupied, 100% collected, NOI 184k THB.", "One roof repair (38k) done and paid from reserve.", "Max → Lender"),
  tone2("tm2_lender_draw", "Construction Draw Request", "Milestone, proof, amount, date.", ["construction","clear","trust","practical"], "Draw #4 request: framing complete, inspection passed 10/8.", "Amount 1.2M THB per schedule. Photos and invoices attached.", "Max → Lender"),
  tone2("tm2_lender_bad_news", "Lender: Delay, Owned Early", "Bad news first, cause, new date, cost.", ["trust","direct","clear","calm"], "Heads-up: completion moves from Dec 15 to Jan 10.", "Cause: window supplier. No budget impact; plan attached.", "Max → Lender"),
  tone2("tm2_partner_casual", "Partner: Quick & Friendly", "Short, friendly, still has the numbers.", ["friendly","casual","clear","warm"], "Good news: unit 3 rented at 14k, two weeks early.", "Want to grab coffee Friday and plan unit 4?", "Max → Partner"),
  tone2("tm2_emoji_landlord", "Emoji-Heavy Landlord", "Very chatty with emoji. (Playful check.)", ["playful","vibrant","casual","friendly"], "Rent day tomorrow!! 🏠💸🎉", "You're the best tenants ever 🙌✨", "Max → Tenant"),
  tone2("tm2_formal_notice", "Formal Legal Notice", "Formal letter register. (Formal/classic check.)", ["formal","classic","trust","calm"], "Dear Tenant, please be advised that the rental rate will be adjusted.", "This notice is provided in accordance with Clause 7 of your lease.", "Max → Tenant"),
 ],
 "Dream Home Finishes": [
  mood("dh2_oak_plaster", "White Oak & Warm Plaster", "Light oak floors, warm-white plaster, linen.", ["warm","light","natural","modern"], ["#f4efe6","#e3d4bc","#c8a97e","#9caf88","#3f4540"], ["white oak","warm plaster","linen"]),
  mood("dh2_teak_concrete", "Teak & Polished Concrete", "Teak doors and ceilings over polished concrete floors.", ["industrial","warm","modern","natural"], ["#8b5a2b","#bdbcb6","#e8e4dc","#3a3a3a","#c19a6b"], ["teak","polished concrete","black steel"]),
  mood("dh2_cedar_steel", "Cedar & Black Steel Windows", "Cedar cladding with slim black steel frames.", ["industrial","natural","modern","rustic"], ["#a0784e","#2b2b2b","#e8dcc6","#6b8f71","#f7f3ea"], ["cedar","steel windows","stone"]),
  mood("dh2_clay_tile_roof", "Clay Tile Roof, Deep Eaves", "Thai-Japanese deep eaves with clay tiles.", ["warm","rustic","thai","natural"], ["#a0522d","#c1502e","#e8dcc2","#5c4033","#4e7d4a"], ["clay roof tiles","deep eaves","teak brackets"]),
  mood("dh2_engawa_light", "Light-Oak Engawa", "Pale oak veranda with sliding glass, garden view.", ["light","natural","modern","calm"], ["#e3d9c6","#c2a878","#ffffff","#7d9a6f","#3a3a3a"], ["light oak deck","sliding glass","moss garden"]),
  mood("dh2_reclaimed", "Reclaimed Timber Beams", "Old teak beams reused in a modern frame.", ["rustic","craft","warm","construction"], ["#6b4226","#3b2a1a","#d8c3a5","#f4ecd8","#8a7f5a"], ["reclaimed teak","iron straps","lime wash"]),
  mood("dh2_terrazzo_light", "Light Terrazzo & Rattan", "Pale terrazzo floors, rattan furniture, palms.", ["light","tropical","natural","modern"], ["#f2efe8","#d9d4c7","#c8a97e","#5a7d4f","#ffffff"], ["terrazzo","rattan","palms"]),
  mood("dh2_kitchen_oak_steel", "Kitchen: Oak & Stainless", "Oak fronts, stainless counters, open shelves.", ["industrial","modern","warm","clear"], ["#c8a97e","#c0c4c8","#f4f4f1","#2b2b2b","#9caf88"], ["oak fronts","stainless top","open shelving"]),
  mood("dh2_bath_stone", "Bath: Warm Stone & Plants", "Travertine, wood slats, a big window to plants.", ["natural","warm","calm","light"], ["#e8dcc6","#c9b49a","#7d9a6f","#ffffff","#5c4033"], ["travertine","wood slats","indoor plants"]),
  mood("dh2_studio_brick", "Music Studio: Brick & Oak", "Brick wall, oak floor, warm lamps, gear wall.", ["industrial","warm","rustic","personal"], ["#9c4a2f","#c8a97e","#2e2e2e","#f2efe8","#b5651d"], ["old brick","oak","pegboard gear wall"]),
  mood("dh2_courtyard", "Inner Courtyard Garden", "Open courtyard with a maple, stone path, rain chain.", ["natural","calm","light","modern"], ["#5a7d4f","#d9cba3","#f7f5ef","#8e8e8a","#c1502e"], ["courtyard","stone path","rain chain"]),
  mood("dh2_carport_workshop", "Carport + Workshop Wing", "Steel carport with a tool workshop behind.", ["construction","industrial","practical","rustic"], ["#2f3a40","#c5ccd0","#a0784e","#f4f4f1","#ff6b00"], ["steel carport","workbench","tool wall"]),
  mood("dh2_ma_minimal", "Pure Ma Minimalism", "Empty rooms, white walls, single object. (Japanese-minimal check.)", ["japanese","minimal","calm","light"], ["#ffffff","#f2f0eb","#d9d4c7","#2b2b2b","#e8e4dc"], ["empty space","white walls","one vase"]),
  mood("dh2_dark_onyx", "Onyx & Brass Luxe", "Black marble, brass, moody lights. (Luxe/dark check.)", ["luxe","dark","bold","formal"], ["#0b0b0b","#2b2b2b","#c9a227","#5c4033","#efe6d2"], ["black onyx","brass","velvet"]),
 ],
 "Japan Cottage Makeover": [
  mood("jc2_warm_wood_refresh", "Warm Wood Refresh", "Sand the old cedar, keep it warm, add soft lighting.", ["warm","natural","rustic","light"], ["#c8a97e","#e8dcc6","#8b5a2b","#f7f3ea","#3b2a1a"], ["sanded cedar","paper lamps","linen"]),
  mood("jc2_modern_kitchen_insert", "Modern Kitchen In Old Shell", "New stainless/oak kitchen inside the old frame.", ["modern","industrial","warm","practical"], ["#c0c4c8","#c8a97e","#3a2e22","#f4f4f1","#7d9a6f"], ["stainless counter","oak fronts","old beams"]),
  mood("jc2_insulated_cozy", "Insulated & Cozy", "Double glazing, wood stove, wool rugs: winter-proof.", ["warm","practical","rustic","natural"], ["#8c3b1f","#d8c3a5","#5c4033","#efe6d2","#2b2b2b"], ["wood stove","double glazing","wool"]),
  mood("jc2_doma_workshop", "Doma Workshop Entry", "Earth-floor entry turned into a tool workshop.", ["construction","rustic","craft","practical"], ["#8e8e8a","#a0784e","#3a2e22","#e8e4dc","#ff6b00"], ["earthen floor","workbench","tool wall"]),
  mood("jc2_engawa_cafe", "Engawa Coffee Corner", "Sunny veranda bench with a little coffee bar.", ["warm","friendly","natural","light"], ["#c19a6b","#f4ecd8","#6f4e37","#9caf88","#ffffff"], ["veranda bench","pour-over","garden view"]),
  mood("jc2_guest_suite_clean", "Clean Guest Suite", "Simple bed, good light, bookable photos.", ["clean","light","modern","practical"], ["#f7f5ef","#e3d9c6","#9aa5a0","#c19a6b","#3f4540"], ["platform bed","linen","task light"]),
  mood("jc2_steel_beam_open", "Open Plan With Steel Beam", "Remove a wall, add a black steel beam, open it up.", ["industrial","construction","modern","clear"], ["#2b2b2b","#c8a97e","#e8e4dc","#6b6e70","#ffffff"], ["steel beam","open plan","exposed joists"]),
  mood("jc2_garden_veg", "Vegetable Garden Yard", "Raised beds, compost, a small greenhouse.", ["natural","rustic","practical","friendly"], ["#4e7d4a","#8a7f5a","#c8a97e","#f2efe8","#c1502e"], ["raised beds","greenhouse","compost"]),
  mood("jc2_thai_textiles", "Thai Textiles Warm-Up", "Indigo and handwoven Thai fabrics in a Japanese house.", ["thai","warm","craft","natural"], ["#1f3b73","#d4a017","#e8dcc2","#8b5a2b","#f7f3ea"], ["indigo","handwoven cotton","teak"]),
  mood("jc2_bilingual_signage", "Bilingual House Signage", "Small EN/JP/TH wooden signs for guests.", ["bilingual","friendly","craft","clear"], ["#c8a97e","#3b2a1a","#f4ecd8","#7d9a6f","#ffffff"], ["burned wood signs","3 languages","house manual"]),
  mood("jc2_solar_practical", "Solar + Rain Tank", "Solar roof and rainwater tank, off-grid-ish.", ["practical","modern","natural","construction"], ["#2f3a40","#7d9a6f","#e9ecee","#c8a97e","#ffffff"], ["solar panels","rain tank","LED"]),
  mood("jc2_rustic_barn", "Barn-Style Rustic", "Big doors, raw wood, farmhouse sink.", ["rustic","warm","natural","craft"], ["#7a5230","#c9a77c","#efe6d2","#3b2a1a","#6b7f3a"], ["barn doors","raw wood","farmhouse sink"]),
  mood("jc2_zen_minimal", "Zen Minimal Strip-Back", "Remove everything, white and tatami only. (Japanese-minimal check.)", ["japanese","minimal","calm","light"], ["#ffffff","#e3d9c6","#d8c8a8","#2b2b2b","#f2ede3"], ["tatami","white walls","nothing else"]),
  mood("jc2_pop_colour", "Colour-Pop Retro Makeover", "Bright Showa-retro colors. (Vibrant/playful check.)", ["vibrant","playful","retro","bold"], ["#d1495b","#edae49","#00798c","#f2efe8","#30638e"], ["retro tiles","color doors","neon sign"]),
 ],
 "Akiya Garden & Exterior": [
  mood("ak_cedar_fence", "Cedar Fence & Gravel", "Simple cedar fence, gravel paths, a few maples.", ["natural","rustic","calm","warm"], ["#a0784e","#bdbcb6","#4e7d4a","#f2efe8","#3b2a1a"], ["cedar fence","gravel","maple"]),
  mood("ak_repaint_light", "Light Repaint", "Pale grey siding, white trim, bright and fresh.", ["light","clean","modern","practical"], ["#e9ecee","#ffffff","#9aa5ab","#c8a97e","#3a3a3a"], ["siding paint","white trim","new gutters"]),
  mood("ak_steel_roof", "Galvalume Roof Swap", "Replace old tiles with a standing-seam metal roof.", ["industrial","practical","construction","modern"], ["#9aa5ab","#c5ccd0","#2f3a40","#e9ecee","#c19a6b"], ["standing seam","galvalume","new flashing"]),
  mood("ak_wood_deck", "Big Timber Deck", "Wide wood deck off the living room.", ["warm","natural","friendly","rustic"], ["#c19a6b","#8b5a2b","#4e7d4a","#f7f3ea","#2b2b2b"], ["timber deck","outdoor table","string lights"]),
  mood("ak_carport_solar", "Solar Carport", "Steel carport with solar panels on top.", ["modern","practical","industrial","clear"], ["#2f3a40","#4dabf7","#e9ecee","#c5ccd0","#ffffff"], ["steel frame","solar panels","EV charger"]),
  mood("ak_wild_garden", "Wild Meadow Garden", "Let it go natural: grasses, wildflowers, a bench.", ["natural","rustic","calm","warm"], ["#83b735","#c6e377","#f6b93b","#8a7f5a","#f2efe8"], ["grasses","wildflowers","bench"]),
  mood("ak_tropical_twist", "Tropical Plant Twist", "Hardy palms and bananas in a Japanese yard.", ["tropical","natural","warm","friendly"], ["#2f5d3a","#83b735","#c8a97e","#f4ecd8","#c1502e"], ["hardy palms","banana plants","stone lantern"]),
  mood("ak_workshop_shed", "Workshop Shed", "Small timber shed for tools and projects.", ["construction","rustic","practical","craft"], ["#8b5a2b","#c8a97e","#2b2b2b","#f2efe8","#ff6b00"], ["timber shed","workbench","pegboard"]),
  mood("ak_stone_wall", "Old Stone Wall Restored", "Repoint the old stone retaining wall, add moss.", ["rustic","natural","craft","construction"], ["#8e8e8a","#6e6658","#4e7d4a","#e9e4d8","#3b2a1a"], ["dry stone","lime mortar","moss"]),
  mood("ak_entry_canopy", "Steel & Cedar Entry Canopy", "New entry canopy in black steel with cedar soffit.", ["industrial","modern","warm","construction"], ["#2b2b2b","#a0784e","#e8e4dc","#7d9a6f","#ffffff"], ["steel canopy","cedar soffit","stone step"]),
  mood("ak_bilingual_gate", "Bilingual Name Gate", "Wooden gate with a small EN/JP house name plate.", ["bilingual","friendly","natural","craft"], ["#c8a97e","#3b2a1a","#f4ecd8","#5a7d4f","#ffffff"], ["timber gate","name plate","lantern"]),
  mood("ak_fire_pit", "Gravel Fire-Pit Corner", "Steel fire pit, benches, string lights.", ["warm","friendly","rustic","natural"], ["#8c3b1f","#bdbcb6","#c8a97e","#2b2b2b","#f6b93b"], ["steel fire pit","timber benches","string lights"]),
  mood("ak_charred_black", "All-Black Charred Exterior", "Fully charred cladding, black on black. (Dark check.)", ["dark","japanese","bold","minimal"], ["#1b1b1b","#2b2b2b","#3a3a3a","#8e8e8a","#f2f0eb"], ["yakisugi","black roof","black fence"]),
  mood("ak_zen_gravel", "Strict Zen Gravel Garden", "Raked gravel, one stone. (Japanese-minimal check.)", ["japanese","minimal","calm","light"], ["#e9e4d8","#a39b8b","#3a5a40","#6e6658","#f7f5ef"], ["raked gravel","single stone","moss"]),
 ],
 "Shorts Cover Styles": [
  thumb("sh2_bilingual_warm", "Warm Bilingual Stack", "Warm photo, EN line over TH line.", ["bilingual","warm","clear","friendly"], "#3b2a1a", "#ffffff", "#f6b93b", "kanit", "bilingual", "Building In Thailand|สร้างบ้านในไทย", "base_site", "sepia(.25) saturate(1.1)"),
  thumb("sh2_progress_day", "Day Counter", "Build-day counter with progress bar.", ["construction","clear","direct","modern"], "#111", "#ffffff", "#ff8c42", "anton", "progress", "DAY 12 / 90", "base_site", None),
  thumb("sh2_clean_tab", "Clean White Tab", "Small clean label on a bright photo.", ["clean","light","natural","modern"], "#ffffff", "#1b1b1b", "#1b1b1b", "dmsans", "tab", "Teak vs concrete?", "ext_tropical", "brightness(1.1)"),
  thumb("sh2_pin_akiya", "Akiya Pin", "Map pin over an old Japanese house.", ["natural","friendly","clear","travel"], "#3e5641", "#ffffff", "#ff8c42", "outfit", "pin", "¥1M Japan house?", "int_japandi", "brightness(1.05)"),
  thumb("sh2_split_before", "Before / After Split", "Clean split, orange label.", ["construction","clear","bold","direct"], "#111", "#ffffff", "#ff6b00", "archivo", "split", "BEFORE → AFTER", "int_cabin", None),
  thumb("sh2_question_warm", "Warm Question Hook", "One question, warm tones.", ["warm","direct","clear","friendly"], "#3b2a1a", "#ffffff", "#f6b93b", "kanit", "bigtext", "WORTH BUILDING HERE?", "ext_tropical", "sepia(.2)"),
  thumb("sh2_hand_rustic", "Rustic Handwritten", "Handwriting on a warm wood photo.", ["rustic","personal","warm","natural"], "#c8a97e", "#ffffff", "#ffffff", "caveat", "hand", "fixing the old beams", "int_cabin", "sepia(.3)"),
  thumb("sh2_price_baht", "Baht Price Sticker", "Price sticker, clear and direct.", ["direct","clear","thai","construction"], "#2f3a40", "#ffffff", "#ffc300", "kanit", "price", "฿380K", "base_site", None),
  thumb("sh2_lower_industrial", "Industrial Lower Third", "Steel-grey lower third, orange rule.", ["industrial","clear","modern","construction"], "#2f3a40", "#ffffff", "#ff6b00", "manrope", "lower", "Steel Frame, Day 3", "base_site", "saturate(.8)"),
  thumb("sh2_number_tips", "Number Tips", "Big number badge: 3 tips.", ["clear","friendly","practical","bold"], "#139a8f", "#ffffff", "#ffd166", "archivo", "number", "3", "base_site", None),
  thumb("sh2_neon_arrows", "Neon Circles & Arrows", "Loud red circles. (Playful/vibrant check.)", ["playful","vibrant","loud","youtube"], "#111", "#ffffff", "#ff1f1f", "anton", "arrows", "NO WAY!!", "base_temple", "saturate(1.6)"),
  thumb("sh2_cinematic_dark", "Dark Cinematic Bars", "Moody letterbox, no text. (Dark/editorial check.)", ["dark","cinematic","editorial","calm"], "#000", "#ffffff", "#ffffff", "inter", "cinematic", "", "base_temple", "brightness(.6) contrast(1.2)"),
 ],
 "Shorts Pacing & Captions": [
  pace("sp2_hook_build", "Hook + Build Steps", "1s hook, then 5 quick steps, end on the result.", ["clear","direct","construction","modern"], [1,2,2,2,2,2,3], ["#ff6b00","#2f3a40"], ["1s hook","step captions","result last"]),
  pace("sp2_bilingual_caps", "Bilingual Captions Always", "EN on top, TH under, every line.", ["bilingual","clear","friendly","thai"], [2,3,2,3,2,3], ["#139a8f","#f6b93b"], ["EN + TH captions","medium pace","clean font"]),
  pace("sp2_warm_story", "Warm Mini-Story", "Slow open, 3 beats, warm music.", ["warm","natural","storytelling","personal"], [4,3,3,4,5], ["#d9693b","#f6e7d0"], ["slow open","acoustic","3 beats"]),
  pace("sp2_timelapse_loop", "Timelapse Loop", "Build timelapse that loops seamlessly.", ["construction","modern","clear","industrial"], [3,3,3,3,3], ["#2f3a40","#ffc300"], ["timelapse","seamless loop","no talking"]),
  pace("sp2_talk_to_cam", "Talk-To-Camera Tips", "Face to camera, jump cuts, text keywords.", ["friendly","direct","clear","personal"], [2,1,2,1,2,1,2], ["#2563eb","#e5e7eb"], ["face cam","keyword text","jump cuts"]),
  pace("sp2_asmr_site", "Site ASMR", "Natural tool sounds, close-ups, no music.", ["natural","rustic","construction","calm"], [4,5,4,5], ["#8b5a2b","#d8c3a5"], ["tool sounds","macro","no music"]),
  pace("sp2_before_after_snap", "Before/After Snap", "Hold before, beat drop, snap to after.", ["clear","construction","bold","modern"], [6,1,8], ["#6c757d","#ff8c42"], ["beat drop","snap cut","hold after"]),
  pace("sp2_walkthrough", "One-Take Walkthrough", "Gimbal walk-through, captions name each room.", ["natural","clear","modern","warm"], [15], ["#7d9a6f","#f4ecd8"], ["one take","room labels","gimbal"]),
  pace("sp2_qa_reply", "Reply-To-Comment", "Shows a viewer comment, then answers fast.", ["friendly","clear","direct","personal"], [2,3,3,3], ["#06c755","#ffffff"], ["comment sticker","quick answer","CTA end"]),
  pace("sp2_cost_breakdown", "Cost Breakdown", "Numbers pop on screen as items appear.", ["clear","direct","construction","practical"], [2,2,2,2,2,3], ["#2bb673","#1f1f1f"], ["number pops","baht totals","receipt end"]),
  pace("sp2_three_lang", "Three-Language Caption Pop", "EN, TH, JP captions pop in turn for the akiya series.", ["bilingual","clear","friendly","modern"], [2,2,2,2,2,2], ["#139a8f","#d9693b"], ["EN/TH/JP","caption pops","steady pace"]),
  pace("sp2_tenant_tip", "Landlord Tip In 20s", "Problem, fix, result, in three beats.", ["clear","practical","friendly","direct"], [3,4,4,3], ["#2bb673","#f4f4f1"], ["3 beats","on-screen tip","calm music"]),
  pace("sp2_hyper", "Hyper Meme Edit", "Zooms, sound effects, flashing text. (Playful/vibrant check.)", ["playful","vibrant","loud","energetic"], [1,1,1,1,1,1,1,1,1,1], ["#ff006e","#ffbe0b"], ["zoom punches","SFX","flashing text"]),
  pace("sp2_moody_film", "Moody Film Essay", "Slow, dark grade, voiceover. (Dark/editorial check.)", ["dark","editorial","cinematic","calm"], [8,9,7], ["#1b1b1b","#5b2a86"], ["dark grade","VO essay","slow"]),
 ],
 "Investor & Lender Messages": [
  tone2("il_onepager", "One-Page Summary", "Everything a lender needs on one page.", ["clear","trust","modern","direct"], "Project: 4-unit rental, Chiang Mai. Cost 9.8M, value 14M.", "Ask: 6.5M THB, 7 years. DSCR 1.4.", "Max → Lender"),
  tone2("il_story_numbers", "Story, Then Numbers", "Why first, then the numbers.", ["warm","storytelling","clear","trust"], "Young families here can't find decent rentals.", "We build 4 units at 12k/month, 95% expected occupancy.", "Max → Investor"),
  tone2("il_bilingual_bank", "Bilingual Bank Note", "English summary, Thai line for the Thai bank.", ["bilingual","thai","clear","trust"], "Attached: updated budget and permit approval.", "แนบงบประมาณและใบอนุญาตก่อสร้างฉบับล่าสุดครับ", "Max → Bank"),
  tone2("il_risk_upfront", "Risks Up Front", "Names the top risks and the mitigations.", ["trust","direct","clear","construction"], "Top risk: rainy-season delays. Buffer: 6 weeks in schedule.", "Second: material prices. Locked 70% of steel already.", "Max → Investor"),
  tone2("il_quarterly_friendly", "Friendly Quarterly Update", "Warm opener, 3 bullets, photo.", ["friendly","warm","clear","natural"], "Hi all, quick Q3 update with a photo from site.", "On budget, 2 weeks ahead, units pre-leased: 3 of 4.", "Max → Investors"),
  tone2("il_builder_cred", "Builder Credibility", "Leans on hands-on construction experience.", ["construction","trust","rustic","direct"], "I've built and managed rentals for years, I'm on site daily.", "That's why my cost estimates hold.", "Max → Lender"),
  tone2("il_follow_up", "Polite Follow-Up", "Gentle nudge with a deadline.", ["friendly","clear","polite","direct"], "Just following up on the term sheet from last week.", "Could we confirm by Friday so we keep the pour date?", "Max → Lender"),
  tone2("il_thanks_close", "Closing Thank-You", "Thanks + what happens next.", ["warm","friendly","trust","clear"], "Thank you for closing this so smoothly.", "First draw request goes in next Monday, with photos.", "Max → Lender"),
  tone2("il_data_table", "Data-Table Style", "Mostly numbers, one line of context.", ["modern","clear","technical","direct"], "LTC 66% · DSCR 1.42 · IRR 14.8% · Payback 6.1 yrs", "Assumes 12k rent, 5% vacancy, 3% annual increase.", "Max → Investor"),
  tone2("il_casual_text", "Casual Text Message", "Short, informal, for a lender he knows well.", ["casual","friendly","direct","natural"], "Permit's approved 🎉", "Sending the paperwork tonight.", "Max → Lender"),
  tone2("il_hype_pitch", "Big Hype Pitch", "Superlatives and exclamation marks. (Playful/vibrant check.)", ["playful","vibrant","bold","energetic"], "This is THE deal of the year!!", "Massive upside, can't-miss returns 🚀", "Max → Investor"),
  tone2("il_banker_formal", "Formal Banker Letter", "Old-school formal letter. (Formal/luxe check.)", ["formal","classic","luxe","calm"], "Dear Sir, I respectfully submit the enclosed proposal for your esteemed consideration.", "I remain at your disposal for any further particulars.", "Max → Bank"),
 ],
}
for _cat, _opts in POOL_2026_10_10C.items():
    POOL.setdefault(_cat, []).extend(_opts)
CATEGORY_WEIGHT_EXTRA_10C = {"SMART Visa Pitch Deck": 1.0, "SiteAgent App Screens": 1.0, "Shorts Pacing & Captions": 0.9,
                             "Akiya Garden & Exterior": 0.9, "Investor & Lender Messages": 1.0}


CATEGORY_WEIGHT = {  # base share of the deck
    "App / UI Style": 1.0, "Color Palette": 1.1, "Typography": 1.0, "Business Communication Tone": 1.1,
    "Home / Interior Style": 1.0, "Logo / Mark": 1.0, "Photography Style": 0.8, "Fashion / Personal Look": 0.8,
    "YouTube Thumbnail Style": 0.8, "Icon & Illustration Style": 0.6,
    "Brand Voice & Taglines": 1.1, "Social Post Layouts": 0.9, "Video Editing & Pacing": 0.9,
    "Website Hero Sections": 0.9, "Packaging & Merch": 0.8, "Workspace": 0.8, "Cars & Gear": 0.7,
    "Food Styling": 0.7, "Music & Mood": 0.8, "Bangkok Vs Japan Aesthetics": 0.9,
}

CATEGORY_WEIGHT.update(CATEGORY_WEIGHT_EXTRA_10C)

# ---------------------------------------------------------------------------
# 2026-10-10 (round 3) "variety" additions: 17 brand-new categories and 9 new card formats
# (full-bleed photo, word-only, quick-fire mini, motion, sound, Thai type, texture, light, cover, sign).
# ~70% of each category sits inside Max's liked space; ~30% are deliberate contrasts.
# ---------------------------------------------------------------------------
F.update({
    "baijam": "'Bai Jamjuree', 'Kanit', system-ui, sans-serif",
    "plexthai": "'IBM Plex Sans Thai', 'Sarabun', system-ui, sans-serif",
    "notoserifthai": "'Noto Serif Thai', 'Pridi', Georgia, serif",
    "notosansthai": "'Noto Sans Thai', 'Sarabun', system-ui, sans-serif",
    "taviraj": "'Taviraj', 'Pridi', Georgia, serif",
    "trirong": "'Trirong', 'Pridi', Georgia, serif",
    "athiti": "'Athiti', 'Prompt', system-ui, sans-serif",
    "krub": "'Krub', 'Kanit', system-ui, sans-serif",
    "k2d": "'K2D', 'Kanit', system-ui, sans-serif",
    "niramit": "'Niramit', 'Sarabun', system-ui, sans-serif",
    "charm": "'Charm', 'Pridi', cursive",
    "chonburi": "'Chonburi', 'Kanit', serif",
    "itim": "'Itim', 'Mitr', cursive",
    "sriracha": "'Sriracha', 'Mitr', cursive",
    "mali": "'Mali', 'Mitr', system-ui, sans-serif",
    "charmonman": "'Charmonman', 'Pridi', cursive",
})

def _o(i, label, desc, tags, **visual):
    return dict(id=i, label=label, desc=desc, tags=tags, visual=visual)
def bleed(i, label, desc, tags, key, caption="", filt=None):
    return _o(i, label, desc, tags, type="bleed", key=key, caption=caption or label, filter=filt)
def word(i, label, desc, tags, w, sub, bg, fg, font="inter"):
    return _o(i, label, desc, tags, type="word", word=w, sub=sub, bg=bg, fg=fg, font=F[font])
def mini(i, label, desc, tags, icon, items, bg, fg="#1b1b1b"):
    return _o(i, label, desc, tags, type="mini", icon=icon, items=items, bg=bg, fg=fg)
def motion(i, label, desc, tags, kind, easing, dur, color, bg="#f4f4f1"):
    return _o(i, label, desc, tags, type="motion", kind=kind, easing=easing, dur=dur, color=color, bg=bg)
def sound(i, label, desc, tags, bpm, color, words, bg="#14161a"):
    return _o(i, label, desc, tags, type="sound", bpm=bpm, color=color, words=words, bg=bg)
def thaitype(i, label, desc, tags, font, weight=400, sample="บ้านไม้สักริมน้ำ", bg="#faf8f3", fg="#1b1b1b"):
    return _o(i, label, desc, tags, type="thaitype", font=F[font], weight=weight, sample=sample, bg=bg, fg=fg)
def texture(i, label, desc, tags, css, note=""):
    return _o(i, label, desc, tags, type="texture", css=css, note=note)
def light(i, label, desc, tags, css, kelvin):
    return _o(i, label, desc, tags, type="light", css=css, kelvin=kelvin)
def cover(i, label, desc, tags, bg, fg, accent, font, layout, title, sub, key=None, filt=None):
    return _o(i, label, desc, tags, type="cover", bg=bg, fg=fg, accent=accent, font=F[font], layout=layout,
              title=title, sub=sub, key=key, filter=filt)
def sign(i, label, desc, tags, bg, fg, accent, font, shape, text, sub=""):
    return _o(i, label, desc, tags, type="sign", bg=bg, fg=fg, accent=accent, font=F[font], shape=shape, text=text, sub=sub)

POOL_2026_10_10D = {
 "Travel & Hotel Vibes": [
  bleed("tv_beach_barefoot", "Barefoot Beach Bungalow", "Simple hut, sand floor, hammock, no shoes for a week.", ["natural","tropical","rustic","light"], "tr_beach_bungalow", "Koh Lanta, no shoes"),
  bleed("tv_heritage_boutique", "Heritage Boutique Hotel", "Restored colonial house, teak floors, ceiling fans.", ["warm","classic","natural","craft"], "tr_boutique_lobby", "Luang Prabang heritage"),
  bleed("tv_glamping", "Glamping Tent", "Canvas tent, real bed, stone wall, forest outside.", ["natural","rustic","warm","friendly"], "tr_glamping", "Canvas + real bed"),
  bleed("tv_timber_lodge", "Big Timber Lodge", "Massive beams, stone fireplace, communal tables.", ["rustic","warm","craft","construction"], "tr_mountain_lodge", "Timber + stone"),
  bleed("tv_desert_camp", "Desert Bedouin Camp", "Tents under red cliffs, stars, total silence.", ["natural","adventurous","warm","raw"], "tr_desert_camp", "Wadi Rum"),
  bleed("tv_sleeper_train", "Overnight Sleeper Train", "Bunk, window, rattle: the journey is the hotel.", ["practical","adventurous","rustic","clear"], "tr_sleeper_train", "Bunk with a view"),
  bleed("tv_pool_villa", "Private Pool Villa", "Thatched sala, plunge pool, outdoor shower.", ["tropical","warm","natural","resort"], "ext_tropical", "Sala + pool"),
  bleed("tv_tatami_inn", "Tatami Inn", "Futon on tatami, paper doors, onsen down the hall.", ["japanese","calm","natural","minimal"], "int_japandi", "Futon night"),
  bleed("tv_glass_retreat", "Glass Forest Retreat", "Glass walls, trees on every side.", ["modern","light","natural","minimal"], "ext_modern", "Trees on all sides"),
  bleed("tv_icon_resort", "Mega-Resort Skyline", "Rooftop infinity pool, big-city icon hotel.", ["luxe","vibrant","bold","urban"], "tr_treehouse", "Rooftop infinity pool"),
  bleed("tv_temple_stay", "Temple-Town Guesthouse", "Small family guesthouse near the temple, bikes at the door.", ["thai","friendly","warm","natural"], "base_temple", "Bikes at the door"),
  mood("tv_city_neon_capsule", "Neon Capsule Hotel", "Pod beds, LED strips, city at 2am.", ["dark","vibrant","technical","urban"], ["#0b0f1a","#7c3aed","#00e5ff","#ff006e","#2b2b2b"], ["pod beds","LED strips","2am city"]),
 ],
 "Café & Coffee Shop Design": [
  bleed("cf_bamboo_garden", "Bamboo Garden Café", "Bamboo seating under trees, blossoms beyond the rail.", ["natural","tropical","warm","friendly"], "cf_garden", "Shade + bamboo"),
  bleed("cf_roaster_showpiece", "Vintage Roaster Showpiece", "Old cast-iron roaster as the centerpiece, wood and brick.", ["rustic","craft","warm","industrial"], "cf_industrial", "Cast-iron roaster"),
  bleed("cf_street_cart", "Street Coffee Cart", "Coffee on wheels, cups for 20 baht.", ["practical","friendly","raw","clear"], "cf_kiosk", "Coffee on wheels"),
  bleed("cf_craft_roastery", "Working Roastery", "Aprons, sacks, roasting drum: you watch it happen.", ["industrial","craft","construction","warm"], "cf_roastery", "Watch it roast"),
  mood("cf_white_tile", "White-Tile Minimal Café", "White tile, one pale wood bar, nothing on the walls.", ["japanese","minimal","light","calm"], ["#ffffff","#f2f0eb","#d9c3a0","#e5e5e5","#2b2b2b"], ["white tile","pale wood","no decor"]),
  mood("cf_shophouse", "Shophouse Café", "Old Thai shophouse, terrazzo floor, plants on the stairs.", ["thai","warm","rustic","natural"], ["#e9c46a","#5a7d4f","#9c4a2f","#d8c3a5","#f2efe8"], ["terrazzo","old shutters","plants"]),
  mood("cf_concrete_block", "Concrete Block Café", "Raw concrete counter, steel stools, big window.", ["industrial","modern","construction","clear"], ["#bdbcb6","#8e8e8a","#2b2b2b","#f2f0eb","#c8a97e"], ["poured concrete","steel stools","big glass"]),
  mood("cf_farm_bakery", "Farmhouse Bakery Café", "Long wood tables, bread on display, flour in the air.", ["rustic","warm","friendly","natural"], ["#c9a77c","#f4ecd8","#7a5230","#efe6d2","#6b7f3a"], ["long tables","bread shelves","linen"]),
  mood("cf_neon_night", "Neon Night Café", "Dark room, pink neon sign, late-night playlist.", ["dark","vibrant","playful","urban"], ["#1a1a40","#ff006e","#7c3aed","#00e5ff","#2b2b2b"], ["neon sign","dark walls","vinyl"]),
  mood("cf_library", "Library Café", "Bookshelves to the ceiling, armchairs, quiet hours.", ["warm","classic","calm","editorial"], ["#5c4033","#a47551","#efe6d2","#1b3a2b","#c9a227"], ["bookshelves","armchairs","green lamps"]),
 ],
 "Signage & Wayfinding": [
  sign("sg_steel_plate", "Laser-Cut Steel Plate", "Raw steel sign, cut-out letters, rusting slowly.", ["industrial","rustic","construction","modern"], "#6b4f3a", "#f2efe8", "#b5651d", "grotesk", "plate", "SITE OFFICE", "→ 50 m"),
  sign("sg_painted_wood", "Hand-Painted Wood Board", "Brush-painted letters on a reclaimed board.", ["rustic","craft","warm","friendly"], "#c8a97e", "#3b2a1a", "#c1502e", "caveat", "board", "Fresh Coffee", "open 7-4"),
  sign("sg_bilingual_blade", "Bilingual Blade Sign", "Projecting sign, English and Thai, lit at night.", ["bilingual","thai","clear","friendly"], "#ffffff", "#16302e", "#139a8f", "kanit", "blade", "Reception", "แผนกต้อนรับ"),
  sign("sg_hi_vis", "Hi-Vis Site Board", "Yellow-black safety board, huge type.", ["construction","clear","direct","industrial"], "#ffd400", "#111111", "#111111", "archivo", "plate", "HARD HATS", "beyond this point"),
  sign("sg_pictogram", "Pictogram Only", "Icons, arrows, no words. Universal.", ["clear","modern","minimal","practical"], "#1d4ed8", "#ffffff", "#ffffff", "inter", "picto", "🚻 ↗  🅿 ←", ""),
  sign("sg_wood_burned", "Burned Timber Plaque", "Letters branded into cedar.", ["natural","craft","rustic","warm"], "#a0784e", "#2b1d12", "#2b1d12", "fraunces", "board", "Garden House", "est. 2026"),
  sign("sg_enamel", "Enamel Street Plate", "Blue-white enamel, rounded corners, old-school.", ["classic","clear","friendly","retro"], "#1f3b73", "#ffffff", "#ffffff", "montserrat", "enamel", "Soi Weberman", "ซอย"),
  sign("sg_floor_graphic", "Painted Floor Lines", "Wayfinding painted on the floor in colored lanes.", ["modern","clear","playful","industrial"], "#d9dcd6", "#1f1f1f", "#ff6b00", "manrope", "floor", "Workshop", "Office · Store"),
  sign("sg_neon_script", "Neon Script Sign", "Pink neon script on black brick.", ["vibrant","playful","dark","urban"], "#141414", "#ff7eb6", "#ff006e", "caveat", "neon", "good vibes", ""),
  sign("sg_gold_leaf", "Gold-Leaf Window Lettering", "Gilded serif on glass, tailor-shop style.", ["luxe","classic","formal","editorial"], "#1b1b1b", "#d4af37", "#d4af37", "cormorant", "glass", "WEBERMAN & CO.", "Builders since 2026"),
 ],
 "Uniforms & Workwear": [
  mood("uw_canvas_chore", "Canvas Chore Coat Crew", "Duck-canvas chore coats with a small chest logo.", ["rustic","construction","warm","practical"], ["#a07040","#2f3e46","#e8dcc2","#1b1b1b","#c1502e"], ["duck canvas","chest patch","brass snaps"]),
  mood("uw_hivis_modern", "Modern Hi-Vis Kit", "Slim hi-vis polos, grey pants, clean logo.", ["construction","modern","clear","industrial"], ["#ff6b00","#2b2d31","#c5ccd0","#ffffff","#ffd400"], ["hi-vis polo","stretch pants","reflective tape"]),
  mood("uw_linen_hospitality", "Linen Hospitality Uniform", "Sand linen shirts and aprons for guests.", ["natural","light","warm","friendly"], ["#e9e2d0","#c3b091","#ffffff","#7d9a6f","#3b2a1a"], ["linen shirt","waxed apron","sandals"]),
  mood("uw_indigo_mohom", "Indigo Mor Hom Crew", "Thai farmer-indigo work shirts as uniform.", ["thai","natural","craft","bilingual"], ["#1f3b73","#3e5c99","#f3efe6","#b5651d","#ffffff"], ["mor hom indigo","cotton","embroidered name"]),
  mood("uw_coverall", "Grey Coveralls", "One-piece grey coveralls, name tape, orange stitch.", ["industrial","practical","clear","construction"], ["#6c757d","#2b2d31","#ff6b00","#e9ecee","#ffffff"], ["coverall","name tape","knee pads"]),
  mood("uw_olive_utility", "Olive Utility Set", "Olive ripstop shirt and cargo pants.", ["natural","practical","rustic","modern"], ["#4b5320","#8a7f5a","#e8e2d0","#2b2b2b","#c3b091"], ["ripstop","cargo pockets","boots"]),
  mood("uw_white_tee_logo", "White Tee + Cap", "Plain white tee, navy cap, small logo. That's it.", ["clear","light","friendly","minimal"], ["#ffffff","#1d3c6e","#e5e5e5","#c8a97e","#2b2b2b"], ["white tee","navy cap","small logo"]),
  mood("uw_black_tech", "All-Black Tech Uniform", "Black technical shell and pants, black boots.", ["dark","technical","modern","bold"], ["#0b0b0b","#1c1c1c","#3a3a3a","#c0c0c0","#ff6b00"], ["tech shell","black boots","tonal logo"]),
  mood("uw_colorblock", "Bright Color-Block Crew", "Primary-color panels so every crew member pops on camera.", ["vibrant","playful","bold","youtube"], ["#e63946","#ffbe0b","#3a86ff","#ffffff","#1b1b1b"], ["color-block","bold logo","sneakers"]),
  mood("uw_tailored_site", "Tailored Site Manager", "Blazer over a polo, chinos, clean boots.", ["formal","classic","trust","luxe"], ["#0f2340","#e8dcc2","#5c4033","#ffffff","#b08d57"], ["blazer","polo","leather boots"]),
 ],
 "Book & Magazine Covers": [
  cover("bk_photo_band", "Photo + Bold Band", "Full photo, one bold title band.", ["clear","modern","construction","bold"], "#111", "#ffffff", "#ff6b00", "anton", "band", "BUILT IN THAILAND", "A field guide", "base_site"),
  cover("bk_kraft_field", "Kraft Field Guide", "Kraft paper, stamped title, small drawing.", ["rustic","craft","natural","warm"], "#c8a97e", "#1b1b1b", "#8b3a1a", "spacemono", "stamp", "Tropical Building", "Notes from the site"),
  cover("bk_bilingual_type", "Bilingual Type Cover", "Type-only, English and Thai stacked.", ["bilingual","thai","clear","modern"], "#fff8f0", "#3b2a1a", "#d9693b", "kanit", "type", "Home|บ้าน", "Max Weberman"),
  cover("bk_blueprint", "Blueprint Cover", "Floor plan line art on blue.", ["technical","construction","clear","industrial"], "#0b3d91", "#ffffff", "#ffd166", "grotesk", "plan", "THE TEAK HOUSE", "Plans + process"),
  cover("bk_warm_photo", "Warm Photo, Small Title", "Golden photo, tiny serif title.", ["warm","natural","calm","light"], "#000", "#ffffff", "#f6b93b", "lora", "small", "A Moment In Thai", "Stories", "ext_tropical", "sepia(.3)"),
  cover("bk_swiss_grid", "Swiss Grid Cover", "Strict grid, big number, red accent.", ["modern","clear","minimal","bold"], "#f4f1e8", "#111111", "#e63312", "inter", "grid", "07", "Building Better"),
  cover("bk_illustrated", "Illustrated Picture-Book", "Soft illustration, rounded title.", ["friendly","warm","playful","soft"], "#ffd8b8", "#4a3426", "#e07a3f", "nunito", "illus", "Our House", "For little builders"),
  cover("bk_luxury_coffee", "Coffee-Table Luxe", "Black linen, gold foil serif.", ["luxe","dark","formal","classic"], "#141414", "#c9a227", "#c9a227", "cormorant", "foil", "RESIDENCES", "Volume I"),
  cover("bk_magazine_editorial", "Glossy Magazine", "Masthead, cover lines, portrait photo.", ["editorial","bold","vibrant","cinematic"], "#000", "#ffffff", "#ff006e", "playfair", "mag", "BUILDER", "The tropical issue", "base_temple", "saturate(1.4)"),
  cover("bk_zine", "Photocopied Zine", "Black-and-white collage, taped letters.", ["raw","playful","craft","retro"], "#f2efe8", "#111111", "#111111", "anton", "zine", "SITE LIFE", "issue #1", "base_site", "grayscale(1) contrast(1.6)"),
 ],
 "Textures & Materials": [
  texture("tx_board_concrete", "Board-Formed Concrete", "Wood-grain imprint in grey concrete.", ["industrial","modern","construction","raw"], "repeating-linear-gradient(0deg,#a9a9a2 0 14px,#9a9a93 14px 15px,#b3b3ac 15px 30px),#a9a9a2", "concrete"),
  texture("tx_teak_grain", "Oiled Teak Grain", "Warm golden-brown wood grain.", ["warm","natural","craft","rustic"], "repeating-linear-gradient(95deg,#8b5a2b 0 6px,#9c6a37 6px 9px,#7a4d23 9px 16px)", "teak"),
  texture("tx_lime_plaster", "Lime Plaster", "Soft cloudy off-white wall.", ["light","natural","calm","warm"], "radial-gradient(circle at 30% 30%,#f7f3ea,#e8e0d0 60%,#efe7d8)", "lime"),
  texture("tx_corrugated", "Corrugated Steel", "Ribbed galvanized metal.", ["industrial","construction","practical","clear"], "repeating-linear-gradient(90deg,#c5ccd0 0 6px,#9aa5ab 6px 10px,#e9ecee 10px 14px)", "zinc"),
  texture("tx_rattan", "Woven Rattan", "Cane weave, light and airy.", ["natural","tropical","craft","light"], "repeating-linear-gradient(45deg,#d9b77e 0 4px,transparent 4px 8px),repeating-linear-gradient(-45deg,#c79d5d 0 4px,#f1e2c4 4px 8px)", "rattan"),
  texture("tx_brick", "Old Red Brick", "Running-bond brick with grey mortar.", ["rustic","industrial","warm","construction"], "linear-gradient(#cfc9bf 2px,transparent 2px) 0 0/40px 16px,linear-gradient(90deg,#cfc9bf 2px,transparent 2px) 0 0/40px 32px,linear-gradient(90deg,#cfc9bf 2px,transparent 2px) 20px 16px/40px 32px,#9c4a2f", "brick"),
  texture("tx_terrazzo", "Terrazzo Chips", "Speckled stone chips in cream.", ["modern","light","friendly","thai"], "radial-gradient(circle at 20% 30%,#c1502e 3px,transparent 4px),radial-gradient(circle at 70% 60%,#5a7d4f 4px,transparent 5px),radial-gradient(circle at 40% 80%,#8e8e8a 3px,transparent 4px),radial-gradient(circle at 85% 20%,#d4a017 2px,transparent 3px),#efe9de", "terrazzo"),
  texture("tx_linen", "Natural Linen", "Fine crosshatch fabric in oat.", ["natural","light","soft","warm"], "repeating-linear-gradient(0deg,#e9e2d0 0 1px,#ded5bf 1px 2px),repeating-linear-gradient(90deg,rgba(0,0,0,.03) 0 1px,transparent 1px 3px),#e9e2d0", "linen"),
  texture("tx_rammed_earth", "Rammed Earth Layers", "Striped earth bands in ochre and clay.", ["earthy","natural","modern","rustic"], "repeating-linear-gradient(0deg,#b9825a 0 9px,#c99668 9px 15px,#a87250 15px 22px,#d4a373 22px 28px)", "earth"),
  texture("tx_black_marble", "Black Marble", "Polished black stone with white veins.", ["luxe","dark","formal","bold"], "linear-gradient(115deg,transparent 45%,rgba(255,255,255,.5) 46%,transparent 48%),linear-gradient(160deg,transparent 60%,rgba(255,255,255,.3) 61%,transparent 62%),#141414", "marble"),
  texture("tx_neon_acrylic", "Neon Acrylic", "Glossy fluorescent plastic.", ["vibrant","playful","modern","bold"], "linear-gradient(135deg,#ff006e,#ffbe0b 50%,#3a86ff)", "acrylic"),
  texture("tx_charred_wood", "Charred Timber", "Black alligator-cracked wood.", ["dark","japanese","craft","raw"], "repeating-linear-gradient(0deg,#1b1b1b 0 10px,#2b2b2b 10px 11px),repeating-linear-gradient(90deg,transparent 0 18px,#000 18px 19px)", "yakisugi"),
 ],
 "Lighting Moods": [
  light("lt_golden_hour", "Golden-Hour Glow", "Low warm sun through the windows.", ["warm","natural","light","calm"], "linear-gradient(160deg,#ffcf8a,#f6a65d 45%,#6b4226)", "2700K sunset"),
  light("lt_daylight_clear", "Bright Clear Daylight", "Even, cool-white daylight. Everything visible.", ["light","clear","modern","practical"], "linear-gradient(180deg,#ffffff,#eef3f7 70%,#d9e2ea)", "5000K daylight"),
  light("lt_edison_warm", "Edison Bulb Warmth", "Bare filament bulbs over a workbench.", ["warm","industrial","rustic","craft"], "radial-gradient(circle at 30% 25%,#ffd27a 0 8%,transparent 30%),radial-gradient(circle at 70% 25%,#ffd27a 0 8%,transparent 30%),linear-gradient(#3b2a1a,#1f1610)", "2200K filament"),
  light("lt_paper_lantern", "Paper Lantern Diffuse", "Soft round glow, no hard shadows.", ["soft","warm","natural","friendly"], "radial-gradient(circle at 50% 40%,#fff3d6 0 20%,#f1d9a8 40%,#8c6e4a 90%)", "2700K diffused"),
  light("lt_workshop_led", "Workshop LED Strips", "Bright linear LEDs, shadow-free bench.", ["industrial","clear","construction","modern"], "linear-gradient(180deg,#ffffff 0 6%,#e9ecee 6% 10%,#ffffff 10% 16%,#cfd4da 16% 100%)", "4000K task"),
  light("lt_candle", "Candlelit Evening", "Flickering low light, warm pockets.", ["warm","calm","rustic","soft"], "radial-gradient(circle at 50% 70%,#ffb347 0 6%,#a0522d 25%,#1b1208 70%)", "1800K candle"),
  light("lt_overcast_skylight", "Overcast Skylight", "Grey-soft top light, calm and flat.", ["calm","light","natural","clear"], "linear-gradient(180deg,#e9ecef,#d7dbe0 60%,#c2c8ce)", "6500K overcast"),
  light("lt_moody_spot", "Moody Spotlights", "Dark room, a few dramatic pools of light.", ["dark","cinematic","luxe","bold"], "radial-gradient(circle at 30% 40%,#f5d48a 0 10%,transparent 25%),radial-gradient(circle at 75% 55%,#f5d48a 0 8%,transparent 22%),#0b0b0b", "2700K accent"),
  light("lt_rgb_gamer", "RGB Color Wash", "Purple-teal LED wash.", ["vibrant","playful","technical","dark"], "linear-gradient(135deg,#7c3aed,#00e5ff 55%,#ff006e)", "RGB"),
  light("lt_moon_garden", "Moonlit Garden", "Cool blue night with low path lights.", ["calm","natural","cool","dark"], "radial-gradient(circle at 80% 15%,#e0fbfc 0 6%,transparent 18%),linear-gradient(#1b2a3a,#253237 60%,#2f5d3a)", "4100K path"),
 ],
 "Outdoor Spaces & Gardens": [
  bleed("gd_tropical_path", "Tropical Garden Path", "Palms, ferns and a shaded gravel path.", ["tropical","natural","warm","calm"], "gd_tropical", "Shade + ferns"),
  bleed("gd_kitchen_beds", "Raised Kitchen Beds", "Timber raised beds, greenhouse, real food.", ["practical","natural","rustic","construction"], "gd_vegetable", "Grow your own"),
  bleed("gd_cottage_border", "Cottage Flower Border", "Overflowing flowers by a white house.", ["natural","friendly","warm","light"], "gd_cottage", "Flowers everywhere"),
  bleed("gd_wild_meadow", "Wildflower Meadow", "Let it grow: grasses and wildflowers.", ["natural","rustic","light","calm"], "gd_meadow", "Let it grow"),
  bleed("gd_rooftop_green", "Rooftop Garden Terrace", "Planters, shade sails, city around.", ["modern","natural","urban","friendly"], "gd_rooftop", "Green roof"),
  bleed("gd_courtyard_fountain", "Formal Courtyard Fountain", "Clipped hedges, fountain, symmetry.", ["classic","formal","calm","luxe"], "gd_courtyard", "Symmetry"),
  bleed("gd_japanese_pond", "Japanese Pond Garden", "Moss, maples, lantern, waterfall.", ["japanese","calm","natural","craft"], "gd_japanese", "Moss + water"),
  bleed("gd_cactus_dry", "Dry Cactus Garden", "Sand, rocks, cacti: almost no watering.", ["practical","bold","natural","playful"], "gd_xeriscape", "No watering"),
  mood("gd_outdoor_kitchen", "Outdoor Kitchen & BBQ Deck", "Concrete counter, grill, long table under a pergola.", ["industrial","warm","friendly","construction"], ["#bdbcb6","#8b5a2b","#2b2b2b","#f2efe8","#c1502e"], ["concrete counter","grill","pergola"]),
  mood("gd_play_lawn", "Family Play Lawn", "Soft lawn, shade tree, swing, sandbox.", ["friendly","natural","light","warm"], ["#83b735","#c6e377","#c8a97e","#ffffff","#f6b93b"], ["lawn","tree swing","sandbox"]),
 ],
 "Thai Script Typefaces": [
  thaitype("th_baijam", "Bai Jamjuree", "Loopless modern Thai, clean and technical.", ["modern","clear","technical","thai"], "baijam", 600),
  thaitype("th_plex", "IBM Plex Sans Thai", "Engineered and neutral, very legible.", ["clear","modern","technical","practical"], "plexthai", 500),
  thaitype("th_noto_sans", "Noto Sans Thai", "Classic looped Thai, friendly and readable.", ["clear","friendly","bilingual","practical"], "notosansthai", 500),
  thaitype("th_noto_serif", "Noto Serif Thai", "Traditional looped serif for long reading.", ["classic","calm","editorial","thai"], "notoserifthai", 500),
  thaitype("th_taviraj", "Taviraj", "Elegant high-contrast serif, magazine-like.", ["editorial","luxe","classic","formal"], "taviraj", 500),
  thaitype("th_trirong", "Trirong", "Bookish serif, warm and traditional.", ["warm","classic","craft","thai"], "trirong", 500),
  thaitype("th_athiti", "Athiti", "Soft loopless sans, light and airy.", ["light","friendly","modern","soft"], "athiti", 600),
  thaitype("th_krub", "Krub", "Squarish, sturdy, a little industrial.", ["industrial","modern","clear","construction"], "krub", 600),
  thaitype("th_k2d", "K2D", "Rounded geometric, friendly signage feel.", ["friendly","modern","clear","warm"], "k2d", 600),
  thaitype("th_niramit", "Niramit", "Calligraphic-touch sans, gentle and warm.", ["warm","natural","friendly","craft"], "niramit", 500),
  thaitype("th_chonburi", "Chonburi", "Heavy poster display with thick-thin strokes.", ["bold","vibrant","retro","playful"], "chonburi", 400, "ร้านกาแฟสด"),
  thaitype("th_charm", "Charm", "Brush-script Thai, ceremonial.", ["luxe","classic","formal","craft"], "charm", 700),
  thaitype("th_itim", "Itim", "Hand-drawn marker Thai, casual.", ["playful","friendly","casual","personal"], "itim", 400, "วันนี้ไปไซต์งาน"),
  thaitype("th_mali", "Mali", "Rounded, cheerful, kids-book friendly.", ["friendly","soft","playful","warm"], "mali", 600, "ห้องของลูกสาว"),
 ],
 "Motion & Animation Styles": [
  motion("mo_ease_slide", "Smooth Ease Slide", "Elements glide in and settle, no fuss.", ["modern","clear","calm","light"], "slide", "cubic-bezier(.22,1,.36,1)", 1.4, "#139a8f"),
  motion("mo_snappy", "Snappy & Quick", "Fast, crisp, gets out of the way.", ["clear","direct","modern","practical"], "slide", "cubic-bezier(.4,0,.2,1)", .6, "#ff6b00"),
  motion("mo_soft_fade", "Soft Fade", "Gentle opacity fades, very calm.", ["soft","calm","natural","light"], "fade", "ease-in-out", 2.0, "#c8a97e"),
  motion("mo_mechanical", "Mechanical Steps", "Stepped motion like a machine or crane.", ["industrial","construction","technical","bold"], "slide", "steps(5,end)", 1.5, "#2f3a40"),
  motion("mo_handdrawn", "Hand-Drawn Wiggle", "Boiling line wiggle, stop-motion feel.", ["craft","warm","friendly","rustic"], "wiggle", "steps(3,end)", .5, "#8b5a2b"),
  motion("mo_grow", "Organic Grow", "Things grow from the center like a plant.", ["natural","warm","soft","friendly"], "scale", "cubic-bezier(.34,1.3,.64,1)", 1.6, "#5a7d4f"),
  motion("mo_typewriter", "Typewriter Text", "Letters type on one by one.", ["clear","retro","direct","editorial"], "type", "steps(14,end)", 2.2, "#1b1b1b"),
  motion("mo_bouncy", "Bouncy Cartoon", "Squash-and-stretch bounces everywhere.", ["playful","vibrant","friendly","bold"], "bounce", "cubic-bezier(.5,-0.5,.5,1.5)", .8, "#ff006e"),
  motion("mo_cinematic_slow", "Slow Cinematic Push", "Slow zoom and long dissolves.", ["cinematic","dark","luxe","calm"], "zoom", "linear", 4.0, "#c9a227", "#141414"),
  motion("mo_glitch", "Glitch / Digital", "Jitters, RGB splits, techy.", ["technical","vibrant","dark","bold"], "glitch", "steps(2,end)", .4, "#00e5ff", "#0b0f1a"),
 ],
 "Emoji & Sticker Styles": [
  mini("em_classic_native", "Native Emoji", "Plain phone emoji, nothing custom.", ["clear","friendly","practical","casual"], "👍", ["universal","zero effort","LINE-ready"], "#fff8e1"),
  mini("em_line_stickers", "LINE-Style Stickers", "Big expressive character stickers for chats.", ["friendly","thai","playful","warm"], "🐻", ["character","big reactions","Thai chat"], "#e8f8ee"),
  mini("em_construction_set", "Construction Sticker Set", "Hard hats, cones, thumbs-up crew.", ["construction","friendly","clear","industrial"], "👷", ["hard hat","cone","done ✓"], "#fff3d6"),
  mini("em_handdrawn", "Hand-Drawn Doodles", "Pen-doodle stickers, wobbly lines.", ["craft","warm","personal","rustic"], "✍️", ["doodle","ink","wobbly"], "#f6f0e4"),
  mini("em_bilingual_words", "Bilingual Word Stickers", "Short words: OK / โอเค, Thanks / ขอบคุณ.", ["bilingual","thai","clear","friendly"], "💬", ["OK / โอเค","ขอบคุณ","สู้ๆ"], "#e6f3f1"),
  mini("em_minimal_mono", "Mono Line Icons", "Single-color line icons instead of emoji.", ["minimal","modern","clear","light"], "◯", ["line only","one color","calm"], "#f4f4f1"),
  mini("em_baby_cute", "Baby & Family Stickers", "Soft pastel baby, bottle, sleepy moon.", ["soft","friendly","warm","personal"], "👶", ["sleepy moon","bottle","first steps"], "#fdf0f3"),
  mini("em_meme_reaction", "Meme Reaction Faces", "Loud meme faces and caps text.", ["playful","vibrant","loud","youtube"], "😱", ["NO WAY","bruh","caps text"], "#ffe5ec"),
  mini("em_3d_glossy", "3D Glossy Emoji", "Shiny 3D-rendered icons.", ["vibrant","modern","bold","playful"], "💎", ["glossy","3D","gradients"], "#ede7ff"),
  mini("em_dark_neon", "Dark Neon Stickers", "Neon outlines on black.", ["dark","vibrant","urban","bold"], "⚡", ["neon","black","glow"], "#1a1a2e", "#f0f0f0"),
 ],
 "Event & Party Styling": [
  mood("ev_site_bbq", "Topping-Out BBQ", "Celebrate the roof going up: grill, crew, cold drinks.", ["construction","friendly","warm","rustic"], ["#2b2d31","#ff6b00","#c8a97e","#f2efe8","#83b735"], ["grill","plywood tables","crew photo"]),
  mood("ev_garden_lanterns", "Garden Lantern Dinner", "Long table under lanterns and string lights.", ["warm","natural","friendly","light"], ["#f6b93b","#5a7d4f","#f4ecd8","#8b5a2b","#ffffff"], ["string lights","long table","lanterns"]),
  mood("ev_thai_housewarming", "Thai Housewarming (Khuen Baan Mai)", "Monks' blessing, marigolds, family feast.", ["thai","warm","natural","friendly"], ["#f6a21a","#ffffff","#d4a017","#3c8d2f","#c1502e"], ["marigolds","white string","family feast"]),
  mood("ev_open_house", "Clean Open House", "Bright, simple, plans on easels, coffee bar.", ["clear","light","modern","practical"], ["#ffffff","#f4f4f1","#139a8f","#c8a97e","#2b2b2b"], ["easels","coffee bar","name tags"]),
  mood("ev_rustic_barn", "Rustic Barn Party", "Hay bales, wood crates, acoustic band.", ["rustic","warm","natural","craft"], ["#a0784e","#e9c46a","#6b4226","#efe6d2","#3b2a1a"], ["wood crates","hay","acoustic"]),
  mood("ev_baby_first_birthday", "Soft First Birthday", "Pastel balloons, picnic blankets, cake smash.", ["soft","friendly","warm","light"], ["#f8c8d8","#fff3b0","#cfe8ef","#ffffff","#c8a97e"], ["pastel balloons","picnic","cake smash"]),
  mood("ev_industrial_launch", "Warehouse Product Launch", "Concrete floor, steel stage, big screen.", ["industrial","modern","bold","technical"], ["#2b2b2b","#bdbcb6","#ff6b00","#ffffff","#6c757d"], ["steel stage","big screen","concrete"]),
  mood("ev_black_tie", "Black-Tie Gala", "Black, gold, crystal, string quartet.", ["luxe","formal","dark","classic"], ["#0b0b0b","#c9a227","#ffffff","#3a3a3a","#efe6d2"], ["black tie","gold","crystal"]),
  mood("ev_neon_rave", "Neon Rooftop Party", "UV paint, DJ, neon everything.", ["vibrant","playful","dark","urban"], ["#ff006e","#00e5ff","#7c3aed","#ffbe0b","#0b0f1a"], ["UV paint","DJ","neon"]),
  mood("ev_beach_bonfire", "Beach Bonfire", "Driftwood, bonfire, guitar, mats on sand.", ["natural","tropical","rustic","warm"], ["#f6b93b","#c1502e","#f0e6d2","#05668d","#3b2a1a"], ["bonfire","driftwood","mats"]),
 ],
 "Watches & EDC": [
  mini("ed_field_watch", "Field Watch", "Simple, legible, canvas strap.", ["practical","rustic","clear","natural"], "⌚", ["38 mm","canvas strap","lume"], "#e8e2d0"),
  mini("ed_digital_tough", "Tough Digital", "Shock-proof digital, does everything.", ["practical","industrial","construction","clear"], "⏱", ["shockproof","solar","alarm"], "#e9ecee"),
  mini("ed_smartwatch", "Smartwatch", "Notifications, calls, fitness on the wrist.", ["modern","technical","practical","clear"], "📟", ["notifications","GPS","health"], "#eef3f7"),
  mini("ed_dress_gold", "Gold Dress Watch", "Thin gold case, leather strap.", ["luxe","formal","classic","editorial"], "🕰", ["gold","thin","leather"], "#1b1b1b", "#d4af37"),
  mini("ed_dive_steel", "Steel Dive Watch", "Rotating bezel, steel bracelet.", ["bold","modern","industrial","classic"], "🌊", ["200 m","steel","bezel"], "#dfe6ea"),
  mini("ed_multitool", "Multi-Tool + Tape", "Multi-tool, 5 m tape, pencil.", ["construction","practical","rustic","industrial"], "🛠", ["multi-tool","5 m tape","carpenter pencil"], "#fff3d6"),
  mini("ed_minimal_carry", "Minimal Carry", "Phone, slim wallet, one key. Done.", ["minimal","clear","modern","light"], "🔑", ["slim wallet","one key","phone"], "#f4f4f1"),
  mini("ed_creator_kit", "Creator Pocket Kit", "Pocket camera, lav mic, power bank.", ["technical","friendly","modern","youtube"], "🎥", ["pocket cam","lav mic","power bank"], "#e6f3f1"),
  mini("ed_leather_notebook", "Leather Notebook & Pen", "Worn leather notebook, brass pen.", ["craft","warm","rustic","classic"], "📓", ["leather","brass pen","sketches"], "#efe1c6"),
  mini("ed_neon_gadgets", "Colorful Gadgets", "Translucent neon tech toys.", ["vibrant","playful","technical","bold"], "🎮", ["translucent","neon","fidget"], "#ffe5ec"),
 ],
 "Kids' Room & Nursery": [
  mood("kd_warm_wood", "Warm Wood Nursery", "Solid wood crib, oat linen, soft rug.", ["warm","natural","soft","craft"], ["#c8a97e","#efe6d8","#8b5a2b","#ffffff","#9caf88"], ["wood crib","oat linen","wool rug"]),
  mood("kd_light_airy", "Light & Airy", "White walls, sheer curtains, pale oak.", ["light","calm","natural","soft"], ["#ffffff","#f6f3ec","#e3d9c6","#cfe8ef","#c2a878"], ["sheer curtains","pale oak","white"]),
  mood("kd_jungle_mural", "Jungle Mural Room", "Hand-painted palms and animals on one wall.", ["tropical","friendly","natural","warm"], ["#2f5d3a","#83b735","#f6b93b","#f4ecd8","#c1502e"], ["mural","palms","animals"]),
  mood("kd_thai_textile", "Thai Textile Nursery", "Handwoven cotton, indigo, little elephant motifs.", ["thai","craft","warm","bilingual"], ["#1f3b73","#d4a017","#f3efe6","#c1502e","#ffffff"], ["indigo cotton","elephant motif","bilingual books"]),
  mood("kd_montessori", "Montessori Low Room", "Floor bed, low shelves, everything reachable.", ["practical","natural","clear","calm"], ["#e9e4d8","#c8a97e","#9caf88","#ffffff","#5c4033"], ["floor bed","low shelves","open toys"]),
  mood("kd_builder_play", "Little Builder Corner", "Wooden blocks, tool bench, kid hard hat.", ["construction","friendly","warm","playful"], ["#ffc300","#c8a97e","#ff6b00","#ffffff","#2b2b2b"], ["wood blocks","tool bench","kid hard hat"]),
  mood("kd_sage_cloud", "Sage & Cloud", "Sage walls, cloud shelf, soft lamp.", ["soft","calm","natural","modern"], ["#9caf88","#c7d3bf","#ffffff","#e9e4d8","#c8a97e"], ["sage paint","cloud shelf","soft lamp"]),
  mood("kd_reading_nook", "Reading Nook", "Window seat, cushions, bookshelf wall.", ["warm","friendly","craft","light"], ["#f6e7d0","#c8a97e","#7d9a6f","#ffffff","#c1502e"], ["window seat","cushions","book wall"]),
  mood("kd_rainbow_bright", "Rainbow Bright", "Primary colors, rainbow rug, toys everywhere.", ["vibrant","playful","bold","friendly"], ["#e63946","#ffbe0b","#3a86ff","#2ec4b6","#ffffff"], ["rainbow rug","primary colors","toys"]),
  mood("kd_princess_luxe", "Princess Luxe", "Canopy bed, pink velvet, gold mirror.", ["luxe","playful","soft","classic"], ["#f8c8d8","#e4a3b8","#d4af37","#ffffff","#cdb4db"], ["canopy","velvet","gold mirror"]),
  mood("kd_scandi_mono", "Monochrome Scandi", "Black-and-white prints, grey felt.", ["minimal","modern","calm","cool"], ["#ffffff","#2b2b2b","#c9c9c9","#e5e5e5","#7a7a7a"], ["B&W prints","felt","grey"]),
  mood("kd_dark_moody", "Moody Dark Nursery", "Deep navy walls, brass, starry ceiling.", ["dark","calm","luxe","bold"], ["#0f2340","#1d3c6e","#c9a227","#e8dcc2","#ffffff"], ["navy walls","star ceiling","brass"]),
 ],
 "Podcast & Audio Branding": [
  sound("pd_acoustic_intro", "Acoustic Guitar Intro", "5-second fingerpicked sting, warm room tone.", ["warm","natural","craft","friendly"], 92, "#c8a97e", ["fingerpicked","5 s sting","room tone"]),
  sound("pd_site_foley", "Job-Site Sound Logo", "Hammer-hit + drill whirr as the audio logo.", ["construction","industrial","clear","rustic"], 120, "#ff6b00", ["hammer hit","drill whirr","2 s"]),
  sound("pd_bilingual_host", "Bilingual Host Hello", "'Hello / สวัสดีครับ' spoken over a soft pad.", ["bilingual","thai","friendly","clear"], 80, "#139a8f", ["spoken hello","EN/TH","soft pad"]),
  sound("pd_khaen_loop", "Khaen Loop", "Isan mouth-organ loop, modern beat under it.", ["thai","warm","natural","friendly"], 100, "#d4a017", ["khaen","light beat","Isan"]),
  sound("pd_lofi_bed", "Lo-Fi Music Bed", "Dusty beat under the whole episode.", ["calm","soft","modern","personal"], 78, "#cdb4db", ["vinyl crackle","78 BPM","bed"]),
  sound("pd_clean_chime", "Clean Two-Note Chime", "Simple bright two-note brand chime.", ["clear","modern","light","minimal"], 60, "#4dabf7", ["two notes","bright","1 s"]),
  sound("pd_nature_bed", "Nature Ambience", "Rain, birds, cicadas under the voice.", ["natural","calm","tropical","light"], 50, "#5a7d4f", ["rain","birds","cicadas"]),
  sound("pd_news_drums", "Big News Drums", "Dramatic newsroom drums and brass.", ["bold","formal","cinematic","editorial"], 128, "#d62828", ["timpani","brass","newsroom"]),
  sound("pd_synth_dark", "Dark Synth Drone", "Low synth drone, thriller vibe.", ["dark","cinematic","technical","bold"], 70, "#7c3aed", ["drone","sub bass","thriller"]),
  sound("pd_ukulele_happy", "Happy Ukulele", "Bouncy ukulele and whistles.", ["playful","vibrant","friendly","light"], 140, "#ffbe0b", ["ukulele","whistle","claps"]),
 ],
 "This Or That: Words": [
  word("wd_build", "Build", "Making something real.", ["construction","clear","direct","industrial"], "BUILD", "make it real", "#2f3a40", "#ffffff", "anton"),
  word("wd_craft", "Craft", "Doing it slowly and well.", ["craft","rustic","warm","natural"], "Craft", "slow and right", "#c8a97e", "#3b2a1a", "fraunces"),
  word("wd_home", "Home", "Belonging, family, rest.", ["warm","friendly","natural","light"], "home", "where it starts", "#fff8f0", "#3b2a1a", "nunito"),
  word("wd_sabai", "Sabai", "Thai for easy, comfortable, at ease.", ["thai","calm","bilingual","warm"], "สบาย", "sabai · at ease", "#f4ecd8", "#6b4226", "kanit"),
  word("wd_honest", "Honest", "Straight talk, no surprises.", ["clear","direct","trust","friendly"], "Honest.", "no surprises", "#ffffff", "#1b1b1b", "manrope"),
  word("wd_sturdy", "Sturdy", "Built to take a beating.", ["industrial","construction","practical","rustic"], "STURDY", "takes a beating", "#6c757d", "#ffffff", "archivo"),
  word("wd_bright", "Bright", "Light-filled, open, optimistic.", ["light","modern","friendly","clear"], "bright", "open + optimistic", "#fff3b0", "#3b2a1a", "outfit"),
  word("wd_grounded", "Grounded", "Earthy, steady, close to nature.", ["natural","rustic","calm","warm"], "grounded", "earth + steady", "#5a4632", "#efe6d2", "lora"),
  word("wd_together", "Together", "Community, crew, family.", ["friendly","warm","bilingual","personal"], "Together", "ด้วยกัน", "#139a8f", "#ffffff", "prompt"),
  word("wd_quiet", "Quiet", "Low noise, stillness, restraint.", ["japanese","minimal","calm","light"], "quiet", "", "#ffffff", "#9a9a9a", "notoserifjp"),
  word("wd_iconic", "Iconic", "Head-turning, status, stand-out.", ["luxe","bold","editorial","formal"], "ICONIC", "", "#0b0b0b", "#d4af37", "playfair"),
  word("wd_wild", "Wild", "Loud, colorful, unpredictable.", ["vibrant","playful","bold","energetic"], "WILD!", "", "#ff006e", "#ffe066", "syne"),
  word("wd_mysterious", "Mysterious", "Shadowy, moody, withheld.", ["dark","cinematic","editorial","calm"], "mysterious", "", "#141414", "#9aa3b2", "cormorant"),
  word("wd_useful", "Useful", "Function first, every time.", ["practical","clear","modern","industrial"], "useful", "function first", "#e9ecee", "#1f1f1f", "plexmono"),
 ],
 "Quick-Fire Picks": [
  mini("qf_morning", "Early Mornings", "Up at 5:30, site by 7.", ["construction","natural","clear","practical"], "🌅", ["5:30 alarm","coffee","site by 7"], "#fff1e6"),
  mini("qf_late_nights", "Late Nights", "Best ideas after 10pm.", ["dark","cinematic","personal","calm"], "🌙", ["10pm ideas","quiet","screens"], "#1a1a2e", "#f0f0f0"),
  mini("qf_pickup", "Pickup Truck", "Bed full of tools, mud on the tires.", ["construction","rustic","practical","industrial"], "🛻", ["tools","mud","tow"], "#e9ecee"),
  mini("qf_scooter", "Scooter", "Weaving through Bangkok traffic.", ["thai","friendly","practical","urban"], "🛵", ["125cc","basket","fast"], "#e6f3f1"),
  mini("qf_mountains", "Mountains", "Cool air, forests, fog.", ["natural","calm","rustic","light"], "⛰", ["fog","pine","cool air"], "#e9efe9"),
  mini("qf_beach", "Beach", "Sand, salt, sun.", ["tropical","light","natural","warm"], "🏝", ["sand","salt","sun"], "#e0fbfc"),
  mini("qf_cook_home", "Cook At Home", "Big pot, family table.", ["warm","friendly","natural","practical"], "🍲", ["family table","big pot","leftovers"], "#fff5e1"),
  mini("qf_street_food", "Street Food", "Plastic stool, wok fire.", ["thai","raw","friendly","warm"], "🍜", ["wok hei","plastic stool","40 baht"], "#fff1e6"),
  mini("qf_vinyl", "Vinyl Records", "Physical music, slow listening.", ["warm","craft","retro","personal"], "💿", ["crate digging","slow","warm sound"], "#efe1c6"),
  mini("qf_streaming", "Streaming Playlists", "Infinite music, zero friction.", ["modern","clear","practical","technical"], "🎧", ["playlists","shuffle","everywhere"], "#eef3f7"),
  mini("qf_fine_dining", "Tasting Menu", "12 tiny courses, wine pairing.", ["luxe","formal","editorial","calm"], "🍷", ["12 courses","pairing","tweezers"], "#1b1b1b", "#d4af37"),
  mini("qf_theme_park", "Theme Park Day", "Rides, crowds, sugar, noise.", ["vibrant","playful","loud","energetic"], "🎢", ["rides","crowds","sugar"], "#ffe5ec"),
 ],
}
for _cat, _opts in POOL_2026_10_10D.items():
    POOL.setdefault(_cat, []).extend(_opts)
CATEGORY_WEIGHT.update({c: 1.0 for c in POOL_2026_10_10D})

# ---- Swipe Controls (Oct 10, 2026): Max brands the swipe bar itself --------------------------------
SC_WORDS = {
    "nmly":  (["No", "Maybe", "Love", "Yes"], ["✕", "?", "❤", "✓"]),
    "nhoy":  (["Nope", "Hmm", "Obsessed", "Yep"], ["✕", "〜", "★", "✓"]),
    "psfk":  (["Pass", "Save", "Fire", "Keep"], ["✕", "⌑", "🔥", "✓"]),
    "thai":  (["ไม่", "อาจจะ", "รัก", "ใช่"], ["✕", "?", "❤", "✓"]),
    "smwy":  (["Skip", "Meh", "Wow", "Yes"], ["»", "–", "!", "✓"]),
    "tbt":   (["This", "Both", "That"], ["◀", "⇄", "▶"]),
    "emoji": (["", "", "", ""], ["👎", "🤔", "😍", "👍"]),
}
SC_PAL = {
    "brand":  ["#A4161A", "#D4A017", "#E0245E", "#0B6E4F"],
    "warm":   ["#C1502E", "#D4A017", "#E0245E", "#05668D"],
    "mono":   ["#1b1b1b", "#1b1b1b", "#1b1b1b", "#1b1b1b"],
    "monol":  ["#f4f1ea", "#f4f1ea", "#f4f1ea", "#f4f1ea"],
    "pastel": ["#f4a6a6", "#f6d58e", "#f7a1c4", "#9fd8b5"],
    "neon":   ["#ff3b5c", "#ffd23f", "#ff2e88", "#2bff88"],
    "tropic": ["#ef6f3c", "#f2c14e", "#e84a7f", "#2a9d8f"],
    "earth":  ["#8a5a44", "#b08d57", "#b5523b", "#5a7d4f"],
}
def ctl(i, label, desc, tags, fmt, words, pal, style, bg="#f4f1ea", font="Hind"):
    w, ic = SC_WORDS[words]
    cols = SC_PAL[pal]
    if len(w) == 3: cols = [cols[0], cols[3], cols[2]] if words == "tbt" else cols[:3]
    return {"id": i, "label": label, "desc": desc, "tags": tags,
            "visual": {"type": "controls", "fmt": fmt, "words": w, "icons": ic, "colors": cols, "style": style, "bg": bg, "font": font}}

POOL_SWIPE = {"Swipe Controls": [
    ctl("sc_round_brand", "Round Color Icons", "Four round icon buttons in brand colors, labels under.", ["clear", "warm", "modern", "friendly"], "round", "nmly", "brand", "filled"),
    ctl("sc_round_outline", "Round Outline Icons", "Thin outlined circles, color only on the icon.", ["minimal", "light", "clear", "modern"], "round", "nmly", "brand", "outline"),
    ctl("sc_round_mono", "Round Mono Icons", "Black circles, white icons. No color at all.", ["minimal", "monochrome", "industrial", "bold"], "round", "nmly", "mono", "filled"),
    ctl("sc_round_emoji", "Emoji Bubbles", "Emoji-only round buttons, no words.", ["playful", "friendly", "casual", "vibrant"], "round", "emoji", "pastel", "filled"),
    ctl("sc_round_haptic", "Haptic Press Circles", "Round buttons that squash on press like a phone tap.", ["modern", "playful", "warm", "tactile"], "round", "nhoy", "tropic", "haptic"),
    ctl("sc_round_glow", "Neon Glow Circles", "Dark bar, glowing neon ring buttons (deliberate dark test).", ["dark", "vibrant", "bold", "tech"], "round", "smwy", "neon", "glow", "#121212"),
    ctl("sc_round_thai", "Thai Round Icons", "Round icons with Thai labels: ไม่ / อาจจะ / รัก / ใช่.", ["thai", "bilingual", "warm", "friendly"], "round", "thai", "warm", "filled", "#f4f1ea", "Kanit"),
    ctl("sc_pill_brand", "Filled Pills", "Four filled pill buttons with words.", ["clear", "warm", "friendly", "modern"], "pill", "nmly", "brand", "filled"),
    ctl("sc_pill_outline", "Outline Pills", "Outlined pills, colored text, airy.", ["minimal", "light", "clear", "calm"], "pill", "nmly", "warm", "outline"),
    ctl("sc_pill_slang", "Slang Pills", "Nope / Hmm / Obsessed / Yep in chunky pills.", ["playful", "casual", "youtube", "bold"], "pill", "nhoy", "tropic", "filled"),
    ctl("sc_pill_pass", "Pass / Save / Fire / Keep", "Collector vocabulary on rounded pills.", ["playful", "creator", "bold", "modern"], "pill", "psfk", "warm", "filled"),
    ctl("sc_pill_thai", "Thai Pills", "Thai-only pill buttons in Kanit.", ["thai", "bilingual", "clear", "friendly"], "pill", "thai", "tropic", "filled", "#fff8ee", "Kanit"),
    ctl("sc_pill_mono", "Monochrome Pills", "Black outline pills, uppercase, wide tracking (site style).", ["minimal", "monochrome", "formal", "clear"], "pill", "nmly", "mono", "outline", "#ffffff", "Khand"),
    ctl("sc_pill_earth", "Earthy Pills", "Clay, ochre and moss pills.", ["natural", "rustic", "warm", "craft"], "pill", "smwy", "earth", "filled"),
    ctl("sc_pill_glow", "Glow Pills", "Pills that glow on press on a dark bar (deliberate dark test).", ["dark", "vibrant", "tech", "bold"], "pill", "nhoy", "neon", "glow", "#141414"),
    ctl("sc_seg_brand", "Segmented Bar", "One bar split into four colored segments.", ["clear", "modern", "warm", "practical"], "segmented", "nmly", "brand", "filled"),
    ctl("sc_seg_mono", "Mono Segmented Bar", "iOS-style segmented control, gray with a sliding white thumb.", ["minimal", "monochrome", "calm", "modern"], "segmented", "nmly", "mono", "slide", "#e9e9e9"),
    ctl("sc_seg_thai", "Thai Segmented Bar", "Segmented bar with Thai words.", ["thai", "bilingual", "clear", "modern"], "segmented", "thai", "brand", "filled", "#f4f1ea", "Kanit"),
    ctl("sc_seg_tbt", "This / Both / That Bar", "Three-way segmented bar for A vs B cards.", ["clear", "modern", "direct", "practical"], "segmented", "tbt", "warm", "slide"),
    ctl("sc_seg_emoji", "Emoji Segments", "Emoji-only segmented strip.", ["playful", "casual", "friendly", "vibrant"], "segmented", "emoji", "pastel", "filled"),
    ctl("sc_slider_brand", "Swipe Slider", "A single slider: drag from No to Yes, Love at the far end.", ["modern", "tactile", "clear", "warm"], "slider", "nmly", "brand", "slide"),
    ctl("sc_slider_mono", "Mono Slider", "Thin gray track, black knob gliding across.", ["minimal", "monochrome", "calm", "light"], "slider", "smwy", "mono", "slide", "#ffffff"),
    ctl("sc_slider_tbt", "This-That Slider", "Knob slides between This and That; middle is Both.", ["direct", "clear", "modern", "practical"], "slider", "tbt", "warm", "slide"),
    ctl("sc_dial", "Rating Dial", "A half-circle dial: needle swings from No to Love.", ["industrial", "technical", "bold", "tactile"], "dial", "nmly", "brand", "slide", "#f4f1ea"),
    ctl("sc_dial_thai", "Thai Gauge Dial", "Gauge dial with Thai words around the arc.", ["thai", "industrial", "playful", "bold"], "dial", "thai", "tropic", "slide", "#f4f1ea", "Kanit"),
    ctl("sc_rail_brand", "Side Rail (Right)", "Vertical stack on the right edge, TikTok-style.", ["modern", "youtube", "creator", "vibrant"], "rail", "nmly", "brand", "filled", "#f4f1ea"),
    ctl("sc_rail_emoji", "Emoji Side Rail", "Emoji rail with counts, like a Shorts screen.", ["playful", "youtube", "creator", "casual"], "rail", "emoji", "pastel", "haptic", "#fff8ee"),
    ctl("sc_rail_mono", "Mono Side Rail", "White outline icons on a photo, no fills.", ["minimal", "monochrome", "modern", "calm"], "rail", "nmly", "monol", "outline", "#f4f1ea"),
    ctl("sc_gesture_arrows", "Gesture Hints Only", "No buttons: faint ← No · Yes → arrows and a moving thumb.", ["minimal", "modern", "calm", "light"], "gesture", "nmly", "brand", "slide"),
    ctl("sc_gesture_thai", "Thai Gesture Hints", "Swipe hints in Thai only: ← ไม่ · ใช่ →.", ["thai", "minimal", "calm", "bilingual"], "gesture", "thai", "warm", "slide", "#f4f1ea", "Kanit"),
    ctl("sc_gesture_tbt", "This ← → That Hint", "Just a hand hint between This and That.", ["minimal", "direct", "clear", "light"], "gesture", "tbt", "warm", "slide"),
    ctl("sc_thumb_brand", "Big Thumb Pads", "Two big pads at thumb height (No / Yes), small Maybe and Love between.", ["practical", "bold", "clear", "warm"], "thumb", "nmly", "brand", "haptic"),
    ctl("sc_thumb_psfk", "Pass / Keep Pads", "Huge Pass and Keep pads, Save and Fire as chips.", ["bold", "practical", "creator", "playful"], "thumb", "psfk", "tropic", "haptic"),
    ctl("sc_thumb_mono", "Mono Thumb Pads", "Heavy black pads, white words, workboot-tough.", ["industrial", "bold", "monochrome", "construction"], "thumb", "smwy", "mono", "filled", "#d9d4c7", "Khand"),
    ctl("sc_thumb_thai", "Thai Thumb Pads", "Big Thai pads: ไม่ and ใช่.", ["thai", "bold", "practical", "friendly"], "thumb", "thai", "brand", "haptic", "#f4f1ea", "Kanit"),
    ctl("sc_stamp_brand", "Rubber Stamps", "Buttons drawn as tilted rubber stamps.", ["rustic", "craft", "playful", "warm"], "stamp", "nmly", "brand", "outline", "#efe6d2"),
    ctl("sc_stamp_inspect", "Inspection Stamps", "PASS / SAVE / FIRE / KEEP as site-inspection stamps.", ["construction", "industrial", "rustic", "bold"], "stamp", "psfk", "earth", "outline", "#e8e0cc", "Khand"),
    ctl("sc_stamp_thai", "Thai Hanko Stamps", "Red seal stamps with Thai words.", ["thai", "craft", "traditional", "warm"], "stamp", "thai", "brand", "filled", "#f6efe2", "Kanit"),
    ctl("sc_stamp_slang", "Sticker Stamps", "Nope / Yep as die-cut stickers.", ["playful", "vibrant", "casual", "youtube"], "stamp", "nhoy", "neon", "filled", "#fff6e5"),
    ctl("sc_square_khand", "Square Uppercase Buttons", "Square outlined buttons, uppercase Khand (maxweberman.com style).", ["minimal", "formal", "clear", "monochrome"], "square", "nmly", "mono", "outline", "#ffffff", "Khand"),
    ctl("sc_square_color", "Square Color Blocks", "Flat square color blocks, no radius.", ["bold", "industrial", "modern", "clear"], "square", "smwy", "warm", "filled", "#ffffff", "Khand"),
    ctl("sc_square_haptic", "Square Haptic Keys", "Chunky keyboard-key buttons that press down.", ["tactile", "industrial", "playful", "bold"], "square", "nmly", "earth", "haptic", "#d8d2c4"),
    ctl("sc_emoji_float", "Floating Emoji", "Emoji float up from the bar on tap, like live reactions.", ["playful", "vibrant", "youtube", "friendly"], "round", "emoji", "tropic", "float", "#fff8ee"),
    ctl("sc_bilingual_pill", "Bilingual Pills", "Each pill shows English over Thai.", ["bilingual", "thai", "clear", "friendly"], "pill", "nmly", "brand", "bilingual"),
    ctl("sc_tbt_round", "This / Both / That Circles", "Three round buttons for pair cards.", ["clear", "friendly", "warm", "modern"], "round", "tbt", "warm", "filled"),
    ctl("sc_tbt_glow", "This / That Glow", "Glowing This and That buttons on a dark bar (deliberate dark test).", ["dark", "tech", "vibrant", "bold"], "pill", "tbt", "neon", "glow", "#121212"),
]}
POOL.update(POOL_SWIPE)

# ---- Polish deck (2026-10-10g): mini-mocks of polish choices for Max's real apps -------------------
TERRA, LAGOON, JUNGLE = "#C1502E", "#05668D", "#0B6E4F"
APPS = {
 "hg":  {"name": "Home Guide", "title": "Your Home Guide", "sub": "Moschouris Residence · For Niko and Vivian", "cta": "Call Max", "item": "Maintenance Schedule", "mark": "HG", "img": "ext_craftsman"},
 "fq":  {"name": "Finish Questions", "title": "Finish Questions", "sub": "19 questions in 15 stops", "cta": "Start", "item": "Kitchen: cabinet pulls?", "mark": "FQ", "img": "int_modernkitchen"},
 "sw":  {"name": "Site Walk", "title": "Site Walk", "sub": "Moschouris house · 7 stops", "cta": "Finish & Share", "item": "Stop 1: Mechanical Room", "mark": "SW", "img": "base_site"},
 "rp":  {"name": "Room Photos", "title": "Room Photos", "sub": "Pick the photos you took of each room", "cta": "Add Photos", "item": "Living Area 004", "mark": "RP", "img": "int_concrete"},
 "jao": {"name": "Jane's Amex Offers", "title": "Jane's Amex Offers", "sub": "Updated Oct 10 · 4 offers", "cta": "Add to Card", "item": "Macy's · +5 Miles", "mark": "JA", "img": "tr_boutique_lobby"},
 "jsq": {"name": "Jane's Shopping Quiz", "title": "Which Brands Do You Love?", "sub": "50 brands · 2 minutes", "cta": "Start", "item": "Saks Fifth Avenue", "mark": "JQ", "img": "tr_boutique_lobby"},
 "jhc": {"name": "Japan House Crew", "title": "Japan House Crew", "sub": "Swipe countryside houses together", "cta": "Join the Crew", "item": "Farmhouse, Nagano · $26K", "mark": "JH", "img": "gd_japanese"},
 "ak":  {"name": "Akiya Swipe", "title": "Akiya Keep or Toss", "sub": "199 cheap houses in Japan", "cta": "Keep", "item": "Old Kominka, Okayama · $18K", "mark": "AK", "img": "int_japandi"},
 "sa":  {"name": "SiteAgent Pitch", "title": "The AI Site Assistant for Builders", "sub": "Seven agents. One assistant. Zero extra admin.", "cta": "Book a Demo", "item": "Daily Report ready to approve", "mark": "SA", "img": "base_site"},
 "wr":  {"name": "Weberman Residence", "title": "Weberman Residence", "sub": "Spatial Study · 5,272 sf courtyard house", "cta": "Walk Through", "item": "103 Living + Conversation Pit", "mark": "WR", "img": "gd_courtyard"},
 "bs":  {"name": "Blueprint Swipe", "title": "Pick a Room", "sub": "Find your dream home taste", "cta": "Start Swiping", "item": "Office and Music Studio", "mark": "BS", "img": "int_cabin"},
 "br":  {"name": "Brief", "title": "Morning Brief", "sub": "Saturday, Oct 10 · 3 items need you", "cta": "Sync", "item": "Steadily EOI ready to send", "mark": "B", "img": "int_japandi"},
}
def pz(kind, app, i, label, desc, tags, **p):
    c = APPS[app]
    return {"id": f"pz_{kind}_{i}", "label": label, "desc": desc, "tags": tags, "app": c["name"],
            "visual": {"type": "polish", "kind": kind, "app": c["name"], "c": c, "p": p}}

# Each entry: (app, optionA, optionB). Checks carry a disliked tag (playful, vibrant, bold, formal, luxe, editorial, geometric).
PZ = {}
def add(cat, pairs): PZ[cat] = pairs

add("App Icon & Favicon", [
 ("hg", pz("icon","hg",1,"Black Square, Khand Initials","Square black tile, white HG in Khand.",["modern","clear","minimal","direct"],shape="square",bg="#171717",fg="#fff",mark="HG"),
        pz("icon","hg",2,"Cream Tile, Terracotta House","Cream rounded tile with a terracotta roof line.",["warm","natural","friendly","craft"],shape="squircle",bg="#FAF3EB",fg=TERRA,mark="⌂",line=True)),
 ("sw", pz("icon","sw",3,"Lagoon Circle, White Check","Round lagoon icon with a check mark.",["clear","modern","light","practical"],shape="round",bg=LAGOON,fg="#fff",mark="✓"),
        pz("icon","sw",4,"Outlined Square, Black SW","White tile, thin black border, SW.",["minimal","light","clear","modern"],shape="square",bg="#fff",fg="#171717",mark="SW",border=True)),
 ("ak", pz("icon","ak",5,"Jungle Tile, Leaf Mark","Green squircle with a small leaf.",["natural","warm","soft","friendly"],shape="squircle",bg=JUNGLE,fg="#fff",mark="❦"),
        pz("icon","ak",6,"Neon Gradient Tile","Bright pink-orange gradient, bold AK.",["vibrant","playful","bold","loud"],shape="squircle",bg="linear-gradient(135deg,#ff2e88,#ffb800)",fg="#fff",mark="AK")),
 ("sa", pz("icon","sa",7,"Hard-Hat Badge","Terracotta circle, white SA, hard-hat line.",["construction","warm","bold","clear"],shape="round",bg=TERRA,fg="#fff",mark="SA",line=True),
        pz("icon","sa",8,"Grey Blueprint Grid","Light grey tile with grid lines and SA.",["construction","technical","light","modern"],shape="square",bg="#EDEDED",fg="#171717",mark="SA",grid=True)),
 ("br", pz("icon","br",9,"Single Letter B","Black B on white, nothing else.",["minimal","direct","clear","modern"],shape="squircle",bg="#fff",fg="#171717",mark="B",border=True),
        pz("icon","br",10,"Sunrise Bar","Cream tile, lagoon B, thin terracotta sunrise bar.",["warm","personal","soft","light"],shape="squircle",bg="#FFFDF7",fg=LAGOON,mark="B",bar=TERRA)),
])
add("Splash & Loading", [
 ("hg", pz("splash","hg",1,"Wordmark Fade-In","MAX WEBERMAN fades in, then the guide.",["minimal","modern","clear","calm"],style="wordmark"),
        pz("splash","hg",2,"Photo + Thin Progress Bar","House photo with a thin lagoon progress bar.",["warm","natural","personal","light"],style="photo",accent=LAGOON)),
 ("fq", pz("splash","fq",3,"Skeleton Cards","Grey placeholder cards shimmer while loading.",["modern","clear","practical","light"],style="skeleton"),
        pz("splash","fq",4,"Spinner Only","A centered spinner, nothing else.",["minimal","plain","practical","calm"],style="spinner")),
 ("jhc", pz("splash","jhc",5,"Three Bouncing Dots","Terracotta dots bounce under the name.",["friendly","warm","soft","playful"],style="dots",accent=TERRA),
         pz("splash","jhc",6,"House Outline Draws Itself","A line drawing of a house draws in.",["craft","natural","warm","personal"],style="draw",accent=JUNGLE)),
 ("sa", pz("splash","sa",7,"Blueprint Grid Build","Grid lines draw, then the logo drops in.",["construction","technical","modern","clear"],style="grid",accent=LAGOON),
        pz("splash","sa",8,"Big Bold Count-Up","Huge 0→100% counter in black.",["bold","loud","modern","direct"],style="count")),
 ("wr", pz("splash","wr",9,"Soft Cream Wash","Cream background warms in with the title.",["soft","warm","calm","light"],style="wash",accent=TERRA),
        pz("splash","wr",10,"Bar Under Wordmark","Wordmark with a jungle bar filling under it.",["clear","modern","natural","direct"],style="bar",accent=JUNGLE)),
])
add("Header & Navigation", [
 ("hg", pz("header","hg",1,"Wordmark Left, Share Right","MAX WEBERMAN left, square SHARE right, thin rule.",["clear","modern","minimal","direct"],layout="left",border="line"),
        pz("header","hg",2,"Centered Title, Back Arrow","Centered title, back arrow left, soft shadow.",["friendly","soft","clear","light"],layout="center",border="shadow")),
 ("sw", pz("header","sw",3,"Stop Counter Header","Title with 'Stop 2 of 7' and a jungle progress line.",["practical","clear","construction","modern"],layout="progress",accent=JUNGLE),
        pz("header","sw",4,"Tabs Under Title","Title with Stops / Notes / Photos tabs.",["practical","clear","modern","light"],layout="tabs",accent=LAGOON)),
 ("jao", pz("header","jao",5,"Small Caps Kicker","Small grey kicker over a big Khand title.",["editorial","formal","minimal","clear"],layout="stacked"),
         pz("header","jao",6,"Friendly Greeting","'Hi Jane' with the date underneath.",["personal","friendly","warm","soft"],layout="greet",accent=TERRA)),
 ("jhc", pz("header","jhc",7,"Bottom Tab Bar","Swipe · Matches · Map · Group tabs at the bottom.",["practical","clear","modern","friendly"],layout="bottomtabs",accent=TERRA),
         pz("header","jhc",8,"Hamburger Menu","Title with a menu icon; nav hidden.",["minimal","clear","calm","modern"],layout="burger")),
 ("bs", pz("header","bs",9,"Accent Underline Title","Title with a short terracotta underline.",["warm","clear","craft","modern"],layout="underline",accent=TERRA),
        pz("header","bs",10,"Breadcrumb Header","Rooms › Office and Music Studio breadcrumb.",["clear","practical","light","technical"],layout="crumb")),
])
add("Button Styles", [
 ("hg", pz("button","hg",1,"Square Outline Uppercase","Square, 2px black outline, uppercase (site style).",["minimal","clear","modern","direct"],radius=0,fill="outline",color="#171717",case="upper"),
        pz("button","hg",2,"Filled Terracotta Pill","Rounded terracotta pill, white text.",["warm","friendly","soft","clear"],radius=99,fill="solid",color=TERRA,case="title")),
 ("fq", pz("button","fq",3,"Big Full-Width Black","Full-width black bar button, 52px.",["direct","bold","clear","practical"],radius=6,fill="solid",color="#171717",case="upper",full=True),
        pz("button","fq",4,"Tinted Lagoon Block","Light lagoon tint, lagoon text.",["soft","light","clear","modern"],radius=10,fill="tint",color=LAGOON,case="title",full=True)),
 ("jao", pz("button","jao",5,"Ghost Text Button With Arrow","No box, underlined text and an arrow.",["minimal","light","calm","clear"],radius=0,fill="ghost",color="#171717",case="upper",arrow=True),
         pz("button","jao",6,"Gold Luxe Button","Black button, gold serif-ish caps.",["luxe","formal","dark","editorial"],radius=2,fill="solid",color="#171717",text="#C9A54A",case="upper")),
 ("sa", pz("button","sa",7,"Jungle Solid With Icon","Jungle green, calendar icon, Book a Demo.",["natural","clear","direct","modern"],radius=8,fill="solid",color=JUNGLE,case="title",icon="▦"),
        pz("button","sa",8,"Outline + Solid Pair","Primary solid black plus secondary outline.",["clear","modern","practical","minimal"],radius=4,fill="pair",color="#171717",case="upper")),
 ("jsq", pz("button","jsq",9,"Soft Shadow Rounded","White rounded button lifted by a soft shadow.",["soft","friendly","light","modern"],radius=14,fill="shadow",color="#171717",case="title"),
         pz("button","jsq",10,"Chunky 3D Press","Thick bottom edge, presses down.",["playful","bold","tactile","vibrant"],radius=10,fill="3d",color=TERRA,case="upper")),
])
add("Card Styles", [
 ("ak", pz("card","ak",1,"Photo Top, Rounded 16","Big photo, rounded 16px card, soft shadow.",["soft","natural","warm","modern"],radius=16,img="top",shadow="soft",border=False),
        pz("card","ak",2,"Photo Left, Square Corners","Square card, photo on the left, hairline border.",["minimal","clear","modern","practical"],radius=0,img="left",shadow="none",border=True)),
 ("hg", pz("card","hg",3,"Icon Row Cards","Small icon, title, chevron; light grey border.",["clear","practical","light","friendly"],radius=12,img="icon",shadow="none",border=True),
        pz("card","hg",4,"Accent Edge Cards","Terracotta left edge, cream fill.",["warm","craft","clear","soft"],radius=8,img="none",accent=TERRA,fill="#FFFDF7",border=False)),
 ("rp", pz("card","rp",5,"Photo Grid Tiles","Three-up square photo tiles per room.",["natural","modern","clear","light"],radius=6,img="grid",border=False),
        pz("card","rp",6,"List With Count Badge","Room name with a lagoon photo-count badge.",["clear","practical","minimal","modern"],radius=10,img="badge",accent=LAGOON,border=True)),
 ("jhc", pz("card","jhc",7,"Full-Bleed Photo Card","Photo fills the card, white text on a fade.",["natural","warm","personal","modern"],radius=18,img="bleed"),
         pz("card","jhc",8,"Polaroid Card","White frame, handwritten-style caption.",["playful","personal","craft","warm"],radius=2,img="polaroid")),
 ("br", pz("card","br",9,"Flat Grey Panels","Flat F5F5F5 panels, no border, no shadow.",["minimal","calm","light","modern"],radius=10,img="none",fill="#F5F5F5",border=False),
        pz("card","br",10,"Bold Color Blocks","Each section in a saturated color block.",["vibrant","bold","playful","loud"],radius=12,img="none",fill="#FFB800",border=False,loud=True)),
])
add("Empty States", [
 ("rp", pz("empty","rp",1,"Camera Icon + One Line","Grey camera icon: 'No photos yet. Add the first one.'",["clear","minimal","friendly","light"],art="icon",icon="📷",copy="No photos yet. Add the first one."),
        pz("empty","rp",2,"Line Drawing Of The Room","Thin line sketch of a room with an Add Photos button.",["craft","warm","personal","natural"],art="sketch",copy="This room is waiting for photos.")),
 ("jao", pz("empty","jao",3,"Plain Text Only","'No offers today. Check back tomorrow.'",["minimal","direct","plain","calm"],art="none",copy="No offers today. Check back tomorrow."),
         pz("empty","jao",4,"Friendly Note From Max","'Nothing new yet, Jane. I'll update this soon. – Max'",["personal","warm","friendly","soft"],art="note",copy="Nothing new yet, Jane. I'll update this soon. – Max")),
 ("br", pz("empty","br",5,"Sun Icon, All Clear","Small sun icon: 'All clear this morning.'",["warm","light","soft","friendly"],art="icon",icon="☀",copy="All clear this morning."),
        pz("empty","br",6,"Big Zero","A huge 0 in Khand: 'items need you'.",["bold","direct","modern","clear"],art="zero",copy="items need you")),
 ("jhc", pz("empty","jhc",7,"Photo Of A Quiet Village","Soft photo: 'No matches yet. Keep swiping.'",["natural","warm","calm","personal"],art="photo",copy="No matches yet. Keep swiping."),
         pz("empty","jhc",8,"Cartoon Mascot","A cartoon house waving: 'No matches yet!'",["playful","cute","vibrant","casual"],art="emoji",icon="🏠👋",copy="No matches yet!")),
 ("fq", pz("empty","fq",9,"Checklist All Done","Green check: 'All 19 answered. Thank you.'",["clear","friendly","natural","direct"],art="icon",icon="✓",copy="All 19 answered. Thank you.",accent=JUNGLE),
        pz("empty","fq",10,"Progress Ring Empty","Grey ring at 0/19 with 'Start with the kitchen.'",["practical","modern","clear","light"],art="ring",copy="Start with the kitchen.")),
])
add("Hover & Micro-Interactions", [
 ("hg", pz("micro","hg",1,"Lift + Soft Shadow","Card lifts 2px with a soft shadow.",["soft","modern","light","clear"],effect="lift"),
        pz("micro","hg",2,"Underline Slides In","Link underline grows from left to right.",["minimal","clear","modern","calm"],effect="underline")),
 ("sa", pz("micro","sa",3,"Arrow Nudge","Button arrow nudges right on hover.",["direct","modern","clear","friendly"],effect="nudge"),
        pz("micro","sa",4,"Fill Sweep","Outline button fills black from the left.",["bold","modern","direct","clear"],effect="fill")),
 ("jsq", pz("micro","jsq",5,"Squash Press","Button squashes like a phone tap.",["tactile","friendly","playful","warm"],effect="press"),
         pz("micro","jsq",6,"Gentle Scale 1.03","Button grows 3%, nothing else (brand .mw-hover).",["minimal","soft","modern","calm"],effect="scale")),
 ("wr", pz("micro","wr",7,"Room Tile Tilt","Room tile tilts slightly toward the cursor.",["playful","modern","geometric","bold"],effect="tilt"),
        pz("micro","wr",8,"Photo Zoom On Hover","Room photo zooms 5% inside its frame.",["natural","warm","soft","modern"],effect="zoom")),
 ("bs", pz("micro","bs",9,"Color Wash On Hover","Card background warms to cream.",["warm","soft","light","calm"],effect="wash"),
        pz("micro","bs",10,"Icon Spin","The room icon spins a quarter turn.",["playful","casual","friendly","vibrant"],effect="spin")),
])
add("Screen Transitions", [
 ("sw", pz("trans","sw",1,"Slide Left Like Pages","Next stop slides in from the right.",["clear","modern","practical","calm"],t="slide"),
        pz("trans","sw",2,"Quick Fade","Screens cross-fade in 150ms.",["minimal","soft","calm","light"],t="fade")),
 ("fq", pz("trans","fq",3,"Card Stack Peel","Each question peels off a stack.",["tactile","friendly","modern","warm"],t="stack"),
        pz("trans","fq",4,"Scale Up From Tap","New screen grows out of the tapped row.",["modern","clear","soft","light"],t="scale")),
 ("jhc", pz("trans","jhc",5,"Bouncy Spring","Screens spring in with a bounce.",["playful","vibrant","bold","casual"],t="bounce"),
         pz("trans","jhc",6,"Slide Up Sheet","Details slide up as a bottom sheet.",["clear","modern","practical","soft"],t="sheet")),
 ("wr", pz("trans","wr",7,"Camera Fly-Through","Plan zooms into the room like a camera move.",["modern","technical","natural","bold"],t="zoom"),
        pz("trans","wr",8,"Curtain Wipe","A cream panel wipes across between rooms.",["warm","craft","calm","soft"],t="curtain")),
 ("br", pz("trans","br",9,"No Animation","Instant swap. Fastest possible.",["direct","minimal","practical","plain"],t="none"),
        pz("trans","br",10,"Sections Fade Up In Order","Each section fades up one after another.",["soft","modern","calm","light"],t="stagger")),
])
add("Typography Scale", [
 ("hg", pz("type","hg",1,"Big Khand Title, Small Hind","Large tight Khand headings, 15px Hind body.",["modern","bold","clear","construction"],h=30,body=13,weight=700,case="title"),
        pz("type","hg",2,"Moderate Scale","Calm 22px headings, 15px body, more air.",["calm","soft","clear","light"],h=22,body=13,weight=600,case="title")),
 ("sa", pz("type","sa",3,"Uppercase Tracked Labels","Uppercase labels with wide tracking above titles.",["formal","clear","modern","minimal"],h=24,body=12,weight=700,case="title",kicker=True),
        pz("type","sa",4,"Huge Hero Number","One giant number leads: '6 voice notes → 1 log'.",["bold","direct","construction","modern"],h=40,body=12,weight=700,case="title",number=True)),
 ("jao", pz("type","jao",5,"Readable Large Body","17px body for easy reading on a phone.",["friendly","clear","practical","soft"],h=22,body=15,weight=600,case="title"),
         pz("type","jao",6,"Editorial Serif Mix","Serif headline over sans body, magazine feel.",["editorial","luxe","formal","classic"],h=24,body=12,weight=600,case="title",serif=True)),
 ("bs", pz("type","bs",7,"All Caps Khand Titles","Every heading uppercase Khand.",["bold","construction","direct","modern"],h=26,body=12,weight=700,case="upper"),
        pz("type","bs",8,"Title Case Khand","Title Case Khand, normal tracking.",["clear","modern","warm","friendly"],h=26,body=12,weight=700,case="title")),
 ("fq", pz("type","fq",9,"Question As Headline","The question itself is the big headline.",["direct","clear","practical","modern"],h=24,body=12,weight=700,case="title",question=True),
        pz("type","fq",10,"Small Header, Big Answers","Small question text, large answer buttons.",["practical","friendly","clear","light"],h=15,body=14,weight=600,case="title",answers=True)),
])
add("Spacing & Density", [
 ("sw", pz("density","sw",1,"Airy Rows","Generous 16px padding, few rows per screen.",["calm","light","soft","modern"],pad=12,rows=4),
        pz("density","sw",2,"Compact Checklist","Tight 8px rows, more stops visible.",["practical","clear","construction","direct"],pad=5,rows=7)),
 ("rp", pz("density","rp",3,"Comfortable List","Medium spacing with dividers.",["clear","practical","light","friendly"],pad=8,rows=5,divider=True),
        pz("density","rp",4,"Spacious Cards","Each room a separate airy card.",["soft","modern","light","calm"],pad=10,rows=3,cards=True)),
 ("br", pz("density","br",5,"Dense Dashboard","Many small rows, like a cockpit.",["technical","practical","bold","modern"],pad=4,rows=8),
        pz("density","br",6,"One Thing Per Row","Big rows, one item each.",["calm","clear","direct","soft"],pad=11,rows=3)),
 ("jao", pz("density","jao",7,"Two-Column Grid","Offers in a 2-up grid.",["modern","clear","light","practical"],pad=6,rows=6,grid=True),
         pz("density","jao",8,"Single Column Feed","One offer per row, full width.",["clear","friendly","calm","direct"],pad=9,rows=4)),
 ("hg", pz("density","hg",9,"Generous Margins","Wide side margins, narrow column.",["calm","soft","light","editorial"],pad=10,rows=4,margin=22),
        pz("density","hg",10,"Edge To Edge","Content runs to the screen edges.",["modern","direct","practical","bold"],pad=8,rows=5,margin=2)),
])
add("Accent Color Usage", [
 ("hg", pz("accent","hg",1,"Monochrome Only","Black, white and grey. No accent at all.",["minimal","clear","modern","formal"],mode="none"),
        pz("accent","hg",2,"Terracotta On The Main Button Only","One terracotta call button; rest grey.",["warm","clear","direct","minimal"],mode="cta",color=TERRA)),
 ("sa", pz("accent","sa",3,"Lagoon Links And Icons","Lagoon for links and small icons.",["clear","modern","light","calm"],mode="links",color=LAGOON),
        pz("accent","sa",4,"Jungle Status Dots","Jungle green only for done and ready states.",["natural","practical","clear","construction"],mode="status",color=JUNGLE)),
 ("jhc", pz("accent","jhc",5,"Cream + Terracotta Warmth","Cream background, terracotta headings.",["warm","natural","soft","personal"],mode="warm",color=TERRA),
         pz("accent","jhc",6,"All Three Accents","Terracotta, lagoon and jungle on different tabs.",["vibrant","playful","bold","friendly"],mode="all")),
 ("br", pz("accent","br",7,"Thin Accent Rule","A thin lagoon line under each section title.",["minimal","clear","modern","calm"],mode="rule",color=LAGOON),
        pz("accent","br",8,"Tinted Section Backgrounds","Each section in a pale accent tint.",["soft","warm","light","friendly"],mode="tint")),
 ("fq", pz("accent","fq",9,"Selected Answer In Jungle","Only the picked answer turns jungle green.",["clear","natural","direct","modern"],mode="selected",color=JUNGLE),
        pz("accent","fq",10,"Progress Bar In Terracotta","Terracotta progress bar is the only color.",["warm","clear","practical","minimal"],mode="progress",color=TERRA)),
])
add("Imagery Treatment", [
 ("ak", pz("image","ak",1,"Natural, Rounded 12","True-color photo, rounded 12px corners.",["natural","warm","soft","modern"],key="int_japandi",frame="round",filt="none"),
        pz("image","ak",2,"Warm Film Grade","Slightly warm, softer contrast photo.",["warm","natural","personal","soft"],key="int_japandi",frame="round",filt="sepia(.25) saturate(1.1) contrast(.95)")),
 ("hg", pz("image","hg",3,"Full-Bleed Hero","Photo runs edge to edge under the title.",["natural","modern","bold","personal"],key="ext_craftsman",frame="bleed",filt="none"),
        pz("image","hg",4,"Square Crop With Caption","Square crop, small grey caption below.",["clear","minimal","practical","light"],key="ext_craftsman",frame="square",filt="none",caption="Front elevation, Oct 2026")),
 ("sa", pz("image","sa",5,"Site Photo, Black And White","Construction site in black and white.",["construction","formal","editorial","minimal"],key="base_site",frame="square",filt="grayscale(1) contrast(1.1)"),
        pz("image","sa",6,"Site Photo, True Color","Construction site in natural color.",["construction","natural","warm","clear"],key="base_site",frame="round",filt="none")),
 ("wr", pz("image","wr",7,"Circle Crops","Room photos in small circles.",["friendly","soft","playful","light"],key="gd_courtyard",frame="circle",filt="none"),
        pz("image","wr",8,"Wide Panorama Strip","Wide 3:1 strip across the screen.",["natural","modern","calm","clear"],key="gd_courtyard",frame="strip",filt="none")),
 ("bs", pz("image","bs",9,"Light Duotone","Photos washed to cream and lagoon.",["soft","modern","geometric","editorial"],key="int_cabin",frame="round",filt="grayscale(1) sepia(.3) hue-rotate(160deg) saturate(.6) brightness(1.1)"),
        pz("image","bs",10,"Bright And Airy","Lifted exposure, light and clean.",["light","natural","soft","warm"],key="int_cabin",frame="round",filt="brightness(1.12) saturate(.95)")),
])
add("Share Preview (OG Card)", [
 ("hg", pz("og","hg",1,"Photo Left, Title Right","House photo left, title and site right.",["clear","natural","modern","practical"],layout="left"),
        pz("og","hg",2,"Big Khand Title On White","Huge black title, small wordmark, no photo.",["minimal","bold","direct","modern"],layout="text")),
 ("sa", pz("og","sa",3,"Photo With Dark-Free Fade","Site photo, light fade, black title.",["construction","natural","light","clear"],layout="bleed"),
        pz("og","sa",4,"Split With Terracotta Panel","Photo half, terracotta panel with the claim.",["warm","bold","construction","modern"],layout="split",accent=TERRA)),
 ("jhc", pz("og","jhc",5,"Personal Invite","'Max invited you to Japan House Crew' with house photo.",["personal","friendly","warm","natural"],layout="invite"),
         pz("og","jhc",6,"Collage Of Four Houses","Four house photos in a grid with the name.",["natural","playful","warm","casual"],layout="collage")),
 ("jsq", pz("og","jsq",7,"Question As Title","'Which brands do you love?' in big type.",["direct","clear","friendly","modern"],layout="question"),
         pz("og","jsq",8,"Luxe Black And Gold","Black card, gold serif title.",["luxe","formal","dark","editorial"],layout="luxe")),
 ("wr", pz("og","wr",9,"Floor Plan Thumbnail","Plan drawing with the house name.",["technical","construction","modern","clear"],layout="plan"),
        pz("og","wr",10,"Courtyard Photo, Wordmark Corner","Photo with a small MAX WEBERMAN corner mark.",["natural","personal","calm","warm"],layout="corner")),
])
add("Onboarding First Screen", [
 ("jhc", pz("onboard","jhc",1,"One Sentence + Start","'Swipe houses with your crew.' and a Start button.",["direct","clear","minimal","friendly"],layout="single"),
         pz("onboard","jhc",2,"Three Steps With Icons","Swipe · Match · Visit, three icon steps.",["clear","practical","friendly","modern"],layout="steps")),
 ("fq", pz("onboard","fq",3,"Letter From Max","'Hi Niko and Vivian, a few quick questions…' – Max.",["personal","warm","friendly","soft"],layout="letter"),
        pz("onboard","fq",4,"Checklist Preview","Shows the 15 stops as a checklist.",["practical","clear","construction","direct"],layout="checklist")),
 ("ak", pz("onboard","ak",5,"Photo Hero + Gesture Hint","House photo, faint swipe hint arrows.",["natural","warm","modern","calm"],layout="photo"),
        pz("onboard","ak",6,"Animated Tutorial Card","A demo card swipes itself to teach you.",["playful","modern","friendly","tactile"],layout="demo")),
 ("jsq", pz("onboard","jsq",7,"Hi Jane","'Hi Jane! 50 brands, 2 minutes.' Start button.",["personal","friendly","warm","direct"],layout="greet"),
         pz("onboard","jsq",8,"Formal Instructions","Numbered rules in small text.",["formal","practical","plain","clear"],layout="rules")),
 ("sa", pz("onboard","sa",9,"Problem First","'Sites run on chat threads, paper and memory.'",["direct","construction","bold","clear"],layout="problem"),
        pz("onboard","sa",10,"Demo Video Frame","Play button over a site video still.",["modern","construction","natural","clear"],layout="video")),
])
add("Success & Confirmation", [
 ("fq", pz("success","fq",1,"Check Draws In","Jungle check mark draws, 'Sent to Max.'",["clear","natural","friendly","modern"],style="check",copy="Sent to Max."),
        pz("success","fq",2,"Stamp: Done","A terracotta DONE stamp thumps down.",["craft","warm","construction","bold"],style="stamp",copy="DONE")),
 ("sw", pz("success","sw",3,"Toast At The Bottom","Small toast: 'Stop 3 saved'.",["minimal","clear","calm","practical"],style="toast",copy="Stop 3 saved"),
        pz("success","sw",4,"Full Screen Thank You","Full screen: 'Walk complete. Thank you!'",["personal","warm","friendly","soft"],style="full",copy="Walk complete. Thank you!")),
 ("jsq", pz("success","jsq",5,"Confetti Burst","Confetti bursts over 'All done!'",["playful","vibrant","bold","casual"],style="confetti",copy="All done!"),
         pz("success","jsq",6,"Heart Pulse","A red heart pulses once: 'Thanks, Jane.'",["personal","warm","friendly","soft"],style="heart",copy="Thanks, Jane.")),
 ("rp", pz("success","rp",7,"Progress Ring Completes","Ring fills to 100%: 'All rooms done.'",["clear","modern","practical","light"],style="ring",copy="All rooms done."),
        pz("success","rp",8,"Green Banner","Jungle banner across the top: 'Uploaded.'",["direct","clear","natural","practical"],style="banner",copy="Uploaded.")),
 ("jao", pz("success","jao",9,"Check + Next Step","'Added. Open Amex to use it.'",["clear","direct","practical","friendly"],style="next",copy="Added. Open Amex to use it."),
         pz("success","jao",10,"Signature Thank You","'Enjoy, Jane. – Max' with a small signature line.",["personal","warm","craft","soft"],style="sign",copy="Enjoy, Jane.")),
])
add("Error States", [
 ("rp", pz("error","rp",1,"Inline Under The Field","Small terracotta text under the upload box.",["clear","minimal","calm","practical"],style="inline",copy="That photo is too big. Try one under 20 MB."),
        pz("error","rp",2,"Friendly Card With Retry","Card: 'Upload didn't go through. Try again?'",["friendly","warm","soft","clear"],style="card",copy="Upload didn't go through. Try again?")),
 ("br", pz("error","br",3,"Top Banner","Thin banner: 'Not connected to Dropbox.'",["direct","clear","practical","modern"],style="banner",copy="Not connected to Dropbox."),
        pz("error","br",4,"Blunt Red Alert","Bright red box, ERROR in caps.",["bold","loud","formal","vibrant"],style="alert",copy="ERROR: SYNC FAILED")),
 ("jhc", pz("error","jhc",5,"Explain + Fix","'Open the full group link you were sent (ends in ?g=…).'",["clear","friendly","practical","direct"],style="explain",copy="Open the full group link you were sent. It ends in ?g=…"),
         pz("error","jhc",6,"Lock Icon Screen","Big lock icon with one line.",["minimal","clear","calm","modern"],style="lock",copy="Group link needed.")),
 ("sw", pz("error","sw",7,"Offline Toast","'Offline. Your notes are saved on this phone.'",["calm","practical","clear","soft"],style="toast",copy="Offline. Notes saved on this phone."),
        pz("error","sw",8,"Warning Strip, Amber","Amber strip with dark text.",["clear","practical","construction","direct"],style="strip",copy="2 stops still need a photo.")),
 ("fq", pz("error","fq",9,"Gentle Nudge","Unanswered question gets a soft terracotta outline.",["soft","warm","clear","friendly"],style="nudge",copy="Pick one, or tap Not Sure."),
        pz("error","fq",10,"Shake + Message","The answer box shakes once.",["playful","tactile","direct","modern"],style="shake",copy="Pick an answer first.")),
])
add("Footer", [
 ("hg", pz("footer","hg",1,"Wordmark + Phone Button","MAX WEBERMAN and a Call Max square button.",["clear","direct","personal","modern"],style="contact"),
        pz("footer","hg",2,"Tiny Grey Credit","'Made by Max Weberman' in small grey.",["minimal","calm","light","plain"],style="credit")),
 ("sa", pz("footer","sa",3,"Links Row","Product · Pricing · Contact links in a row.",["clear","practical","modern","minimal"],style="links"),
        pz("footer","sa",4,"Cream Block With Email","Cream footer block with an email line.",["warm","soft","clear","friendly"],style="cream")),
 ("jao", pz("footer","jao",5,"Updated Date Stamp","'Updated Oct 10, 2026' only.",["minimal","practical","direct","clear"],style="date"),
         pz("footer","jao",6,"Share + Signature","Share button and '– Max' side by side.",["personal","friendly","warm","clear"],style="share")),
 ("wr", pz("footer","wr",7,"Drawing Title Block","Architect-style title block: sheet, scale, date.",["technical","construction","craft","formal"],style="titleblock"),
        pz("footer","wr",8,"Thin Rule + Wordmark","A hairline and the wordmark, centered.",["minimal","modern","calm","light"],style="rule")),
 ("bs", pz("footer","bs",9,"Progress Saved Note","'Progress saves on this device.' plus Share.",["practical","clear","friendly","light"],style="saved"),
        pz("footer","bs",10,"Big Bold Wordmark","Huge MAX WEBERMAN across the bottom.",["bold","editorial","modern","loud"],style="big")),
])
add("Share Message Copy", [
 ("jhc", pz("msg","jhc",1,"Short And Direct","'Join my Japan house crew: [link]'",["direct","clear","casual","friendly"],text="Join my Japan house crew: webermanapps.github.io/japan-house-crew"),
         pz("msg","jhc",2,"Warm Invite","'Found some great old houses in Japan. Swipe with me? [link]'",["warm","personal","friendly","soft"],text="Found some great old houses in Japan. Want to swipe through them with me? webermanapps.github.io/japan-house-crew")),
 ("fq", pz("msg","fq",3,"Task-Focused","'19 quick questions about your finishes, about 10 minutes: [link]'",["practical","direct","clear","construction"],text="19 quick questions about your finishes, about 10 minutes: webermanapps.github.io/finish-questions"),
        pz("msg","fq",4,"Personal From Max","'Hi Niko and Vivian, this helps me order the right finishes. Thanks! – Max'",["personal","warm","friendly","craft"],text="Hi Niko and Vivian, this helps me order the right finishes for your house. Thanks! – Max webermanapps.github.io/finish-questions")),
 ("jsq", pz("msg","jsq",5,"Playful Emoji","'🛍️ Quick quiz for you, Jane! 😍 [link]'",["playful","vibrant","casual","cute"],text="🛍️ Quick quiz for you, Jane! Which brands do you love? 😍 webermanapps.github.io/amex-brand-swipe"),
         pz("msg","jsq",6,"Plain And Kind","'Jane, a 2-minute quiz so I can find you better offers.'",["friendly","clear","personal","soft"],text="Jane, here's a 2-minute quiz so I can find you better Amex offers: webermanapps.github.io/amex-brand-swipe")),
 ("sa", pz("msg","sa",7,"One-Line Pitch","'SiteAgent: one AI assistant for your whole site. Preview: [link]'",["direct","clear","construction","modern"],text="SiteAgent: one AI assistant for your whole site. Partner preview: webermanapps.github.io/ai-construction-pitch"),
        pz("msg","sa",8,"Formal Introduction","'Dear partner, please find attached our proposal…'",["formal","classic","practical","editorial"],text="Dear partner, please find our proposal for SiteAgent at the link below. Kind regards, Max Weberman")),
 ("wr", pz("msg","wr",9,"Show-And-Tell","'Here's the house I'm designing. Walk through it in 3D: [link]'",["personal","warm","natural","friendly"],text="Here's the house I'm designing. You can walk through it in 3D: webermanapps.github.io/weberman-residence"),
        pz("msg","wr",10,"Just The Link","Only the link, no text.",["minimal","direct","plain","clear"],text="webermanapps.github.io/weberman-residence")),
])
add("From Max Sign-Off", [
 ("hg", pz("sign","hg",1,"– Max","A simple dash and first name.",["personal","direct","minimal","warm"],style="dash"),
        pz("sign","hg",2,"Small Photo + Name","Small round photo placeholder and 'Max Weberman, builder'.",["personal","friendly","warm","clear"],style="avatar")),
 ("fq", pz("sign","fq",3,"Handwritten-Style Line","Italic 'Thanks, Max' with a pen-stroke underline.",["personal","craft","warm","soft"],style="pen"),
        pz("sign","fq",4,"Initials Stamp","A small MW stamp in terracotta.",["craft","construction","warm","modern"],style="stamp")),
 ("jao", pz("sign","jao",5,"Made For Jane","'Made for Jane by Max' at the top.",["personal","warm","friendly","soft"],style="madefor"),
         pz("sign","jao",6,"Corporate Footer","'© 2026 Max Weberman. All rights reserved.'",["formal","plain","classic","minimal"],style="legal")),
 ("sa", pz("sign","sa",7,"Founder Note","'I built SiteAgent after 10 years on site. – Max, founder'",["personal","construction","direct","warm"],style="founder"),
        pz("sign","sa",8,"Team Sign-Off","'– The SiteAgent team'",["clear","modern","formal","practical"],style="team")),
 ("br", pz("sign","br",9,"Good Morning, Max","Greeting at the top: 'Good morning, Max.'",["personal","warm","soft","friendly"],style="greet"),
        pz("sign","br",10,"No Personal Touch","Just the date. No greeting.",["minimal","direct","plain","practical"],style="none")),
])

# ~15% checks: only these options keep the directions Max has rejected; incidental tags elsewhere are softened
PZ_CHECKS = {"pz_icon_6", "pz_button_6", "pz_button_10", "pz_card_10", "pz_empty_8", "pz_micro_7", "pz_trans_5",
             "pz_type_6", "pz_accent_6", "pz_og_8", "pz_error_4", "pz_msg_5", "pz_msg_8", "pz_success_5"}
_SOFTEN = {"bold": "strong", "formal": "tidy", "editorial": "refined", "playful": "lively", "geometric": "precise",
           "loud": "punchy", "classic": "traditional", "vibrant": "colorful", "luxe": "premium", "dark": "contrast", "cute": "sweet"}
for _lst in PZ.values():
    for _app, _a, _b in _lst:
        for _o in (_a, _b):
            if _o["id"] not in PZ_CHECKS:
                _o["tags"] = list(dict.fromkeys(_SOFTEN.get(t, t) for t in _o["tags"]))
POOL.update({cat: [o for _, a, b in pairs for o in (a, b)] for cat, pairs in PZ.items()})
CATEGORY_WEIGHT.update({cat: 1.0 for cat in PZ})
CATEGORY_WEIGHT.update({"Swipe Controls": 1.0})
SWIPE_CONTROLS = "Swipe Controls"
SC_TH = {"No": "ไม่", "Maybe": "อาจจะ", "Love": "รัก", "Yes": "ใช่"}
for _o in POOL_SWIPE["Swipe Controls"]:
    if _o["visual"]["style"] == "bilingual":
        _o["visual"]["sub"] = [SC_TH.get(w, "") for w in _o["visual"]["words"]]

# Loose "family" of each category so the deck order can avoid putting similar things back-to-back.
CATEGORY_GROUP = {
    "work": ["SiteAgent Brand Marks", "SiteAgent Pitch Page", "SiteAgent Product Voice", "SiteAgent App Screens", "SMART Visa Pitch Deck"],
    "homes": ["Home / Interior Style", "Dream Home Finishes", "Japan Cottage Makeover", "Akiya Garden & Exterior", "Outdoor Spaces & Gardens",
              "Kids' Room & Nursery", "Café & Coffee Shop Design", "Workspace", "Textures & Materials", "Lighting Moods", "Travel & Hotel Vibes"],
    "type": ["Typography", "Thai Script Typefaces", "Logo / Mark", "Signage & Wayfinding", "Book & Magazine Covers"],
    "media": ["YouTube Thumbnail Style", "Shorts Cover Styles", "Shorts Pacing & Captions", "Video Editing & Pacing", "Motion & Animation Styles",
              "Podcast & Audio Branding", "Social Post Layouts", "Channel Trailer Pacing", "Music & Mood"],
    "words": ["Business Communication Tone", "Brand Voice & Taglines", "Tenant & Partner Messages", "Investor & Lender Messages", "This Or That: Words"],
    "things": ["Fashion / Personal Look", "Uniforms & Workwear", "Watches & EDC", "Cars & Gear", "Packaging & Merch", "Emoji & Sticker Styles",
               "Quick-Fire Picks", "Event & Party Styling", "Food Styling"],
}
GROUP_OF = {c: g for g, cs in CATEGORY_GROUP.items() for c in cs}
GROUP_OF.setdefault("Swipe Controls", "Swipe Controls")
for _c in PZ: GROUP_OF.setdefault(_c, _c)

# ---- Niko & Vivian deck (2026-10-11b): visual AND functional choices for the apps Max built for his clients ----
# Home Guide (Moschouris Residence), Finish Questions, Site Walk and Room Photos, mocked with each app's real
# room names, questions, checklist items and buttons (no links, no contact details). Plus retests of the
# app-polish-spec 'Topics To Retest' and 4 Swipe Controls pairs inside Max's current lean. Light mode only.
NVAPPS = {
 "hg": {"name": "Home Guide", "title": "Your Home Guide", "sub": "Moschouris Residence", "cta": "Call Max", "item": "Maintenance Schedule", "mark": "HG", "img": "ext_craftsman"},
 "fq": {"name": "Finish Questions", "title": "Finish Questions", "sub": "19 questions in 15 rooms", "cta": "Send Answers", "item": "Mud room floor tile?", "mark": "FQ", "img": "int_modernkitchen"},
 "sw": {"name": "Site Walk", "title": "Moschouris Site Walk", "sub": "7 stops · Basement to Exterior", "cta": "Finish and Share", "item": "Stop 1: Basement Mechanical Room", "mark": "SW", "img": "base_site"},
 "rp": {"name": "Room Photos", "title": "Room Photos", "sub": "Moschouris room photos", "cta": "Add Photos", "item": "Living Area 004", "mark": "RP", "img": "tr_boutique_lobby"},
 "sa": {"name": "SiteAgent Pitch", "title": "The AI Site Assistant for Builders", "sub": "Seven agents. One assistant. Zero extra admin.", "cta": "Book a Demo", "item": "Daily Report ready to approve", "mark": "SA", "img": "base_site"},
}
def nv(kind, app, i, label, desc, tags, **p):
    c = NVAPPS[app]
    return {"id": f"nv_{kind}_{i}", "label": label, "desc": desc, "tags": tags, "app": c["name"],
            "visual": {"type": "polish", "kind": kind, "app": c["name"], "c": c, "p": p}}

HG_AZ = ["1/2 Bath", "Coatroom", "Dining Room", "Foyer", "Gallery", "Greatroom", "Kitchen", "Lanai", "Mud Room", "Office"]
HG_LEVELS = [["Basement", ["Gym", "Mech Room"]], ["First Floor", ["Foyer", "Kitchen"]], ["Second Floor", ["Shoe Den"]]]
HG_MAINT = ["Furnace 1 Humidifier", "Sump Pump 1", "Water Filter System", "ERV System", "Water Heater 1", "Irrigation Controller"]
HG_SECTIONS = ["Emergencies", "Who to Call", "Maintenance Schedule", "Warranties", "Shutoffs & Key Locations", "Home Systems & Equipment"]
FQ_ROOMS = ["Foyer 110", "Mud Room 116", "Half Bath 115", "Laundry 203", "Bedroom 201", "Bathroom 204", "Closet 209"]
FQ_AZ = ["Bathroom 204", "Bedroom 201", "Bedroom 206", "Closet 209", "Foyer 110", "Gym 012", "Half Bath 115", "Laundry 203", "Living Area 004", "Mud Room 116"]
FQ_WALK = [["Basement", ["Living Area 004", "Gym 012"]], ["First Floor", ["Foyer 110", "Mud Room 116"]], ["Second Floor", ["Laundry 203"]]]
SW_ITEMS = ["Water Filter System", "Sump Pump 1 (Check)", "ERV System", "Furnace 1 Humidifier", "Water Heater 1 (Rinnai)", "Electrical Panels (2)"]
SW_STOPS = ["Basement Mechanical Room", "Unfinished Basement Area", "Finished Basement Area", "Main Level", "Master Suite", "Upper Level", "Exterior"]
RP_AZ = [["Bathroom 005", 3], ["Family Suite 002", 6], ["Gym 012", 0], ["Kitchen 006", 8], ["Living Area 004", 4], ["Mud Room 116", 0]]
RP_LEVELS = [["Basement", 14], ["First Floor", 22], ["Second Floor", 18]]
SLABS = [["Carrara Fina quartz", "linear-gradient(135deg,#f4f4f2 0,#e6e6e3 40%,#cfd0cf 42%,#f1f1ef 46%,#e9e9e6 100%)"],
         ["Calacatta Vivo quartz", "linear-gradient(120deg,#fbf8f2 0,#f1e9da 35%,#c9a978 37%,#f6f0e4 40%,#efe6d4 100%)"],
         ["Mystery White marble", "linear-gradient(150deg,#f2f2f2 0,#d9dbdc 30%,#9aa0a4 31%,#e3e4e5 36%,#f0f0f0 100%)"],
         ["Porcelain slab", "linear-gradient(135deg,#f3efe8,#e7e1d6)"]]

NV = []   # (category, app key, option A, option B)
def nvadd(cat, app, a, b): NV.append((cat, app, a, b))

# --- Home Guide (Moschouris Residence) ---
nvadd("List Sorting", "hg",
 nv("sort", "hg", 1, "A–Z Rooms, Sort Chips On Top", "Rooms A to Z by default. Chips switch to By Level or By Trade.", ["clear", "direct", "practical", "modern"],
    mode="az", chips=["A–Z", "By Level", "By Trade"], items=HG_AZ, head="Finishes by Room"),
 nv("sort", "hg", 2, "Grouped By Level, A–Z Inside", "Basement, First Floor, Second Floor headers, rooms A to Z under each.", ["practical", "clear", "architectural", "friendly"],
    mode="level", chips=["A–Z", "By Level", "By Trade"], groups=HG_LEVELS, head="Finishes by Room"))
nvadd("Condensed Lists", "hg",
 nv("rows", "hg", 1, "Tap A Row, It Expands In Place", "One compact row per task. The tapped row opens right there.", ["practical", "clear", "minimal", "direct"],
    mode="expand", items=HG_MAINT, open=0, detail=["Replace the pad", "Every fall · Mech Room"], head="Maintenance Schedule"),
 nv("rows", "hg", 2, "Tap A Row, Details Slide Up", "Same compact rows. Details open in a bottom sheet over the list.", ["clear", "modern", "soft", "tactile"],
    mode="sheet", items=HG_MAINT, open=0, detail=["Replace the pad", "Every fall · Mech Room"], head="Maintenance Schedule"))
nvadd("Condensed Lists", "hg",
 nv("rows", "hg", 3, "Expand All And Collapse All Buttons", "Rows can all open at once. Two small buttons open or close everything.", ["practical", "direct", "clear", "efficient"],
    mode="toggle", items=HG_SECTIONS[1:5], details=["Plumber · Electrician · HVAC", "6 tasks this fall", "Appliances · Roof · Windows", "Water · Gas · Power"], head="Good to Know"),
 nv("rows", "hg", 4, "Only One Row Open At A Time", "Opening a row closes the last one, so the list stays short.", ["minimal", "tidy", "clear", "calm"],
    mode="onlyone", items=HG_SECTIONS[1:6], open=4, detail=["Furnace 1 · Water Heater 1", "Sump Pump 1 · ERV System"], head="Good to Know"))
nvadd("Notifications", "hg",
 nv("notify", "hg", 1, "Add All To My Calendar", "One tap puts every maintenance task in their phone calendar.", ["practical", "calm", "clear", "personal"],
    mode="calendar", events=[["Oct 15", "Change furnace filters"], ["Nov 1", "Test sump pumps"], ["Nov 20", "Shut off irrigation"]]),
 nv("notify", "hg", 2, "Remind Me: A Push From The App", "The guide pings them on the day, with the task and how long it takes.", ["direct", "modern", "practical", "friendly"],
    mode="push", copy="Time to test Sump Pump 1. Takes about 2 minutes."))
nvadd("Navigation", "hg",
 nv("nav", "hg", 1, "Floor Plan First", "Opens on the floor plan. Tap a room to see its finishes.", ["architectural", "tactile", "modern", "natural"],
    mode="plan", head="First Floor", rooms=["Kitchen", "Pantry", "Greatroom", "Lanai", "Foyer", "Mud Room"], toggle=["Floor Plan", "Room List"]),
 nv("nav", "hg", 2, "Room List First", "Opens on a list of rooms. The floor plan is one tap away.", ["clear", "practical", "direct", "minimal"],
    mode="list", head="First Floor", rooms=["Dining Room", "Foyer", "Greatroom", "Kitchen", "Lanai", "Mud Room"], toggle=["Room List", "Floor Plan"]))
nvadd("Feature Options", "hg",
 nv("feature", "hg", 1, "Offline Copy On Their Phones", "The whole guide saves on the phone and works with no signal.", ["practical", "calm", "clear", "honest"],
    mode="offline", copy="Saved on this phone. Works with no signal.", head="Your Home Guide"),
 nv("feature", "hg", 2, "Live Updates From Max", "Max can add or fix things and they see it right away.", ["personal", "modern", "friendly", "direct"],
    mode="live", copy="New: warranty info for the Kitchen Cooktop", stamp="Updated by Max · 2 hours ago", head="Your Home Guide"))
nvadd("Feature Options", "hg",
 nv("feature", "hg", 3, "Emergencies Pinned On Top", "A red-outlined Emergencies card always sits above every section.", ["direct", "practical", "clear", "construction"],
    mode="pin", items=HG_SECTIONS[1:5], copy="Emergencies: water, gas and power shutoffs"),
 nv("feature", "hg", 4, "Search Bar On Top", "Type what you need and jump straight to it.", ["modern", "clear", "practical", "minimal"],
    mode="search", query="water shut", results=["Water Shutoff for Niko", "Shutoffs & Key Locations", "Water Filter System"]))
nvadd("App Icon & Favicon", "hg",
 nv("icon", "hg", 11, "White Tile, Black HG, Faint Grid", "The interim rule: white tile, thin black border, Khand initials, faint grid.", ["minimal", "clear", "technical", "light"],
    shape="square", bg="#fff", fg="#171717", mark="HG", border=True, grid=True),
 nv("icon", "hg", 12, "Light Grey Tile, Roofline Over HG", "#EDEDED tile with a thin black roof line above the initials.", ["architectural", "clear", "warm", "personal"],
    shape="square", bg="#EDEDED", fg="#171717", mark="HG", roof=True))
nvadd("Imagery Treatment", "hg",
 nv("image", "hg", 11, "Full-Width Photo, Rounded 14", "True-color room photo across the screen, 14px corners.", ["natural", "clear", "honest", "modern"],
    key="int_modernkitchen", frame="round", filt="none", room="Kitchen"),
 nv("image", "hg", 12, "Photo With A Caption Line", "True-color square crop with a small grey caption under it.", ["clear", "practical", "tidy", "light"],
    key="int_modernkitchen", frame="square", filt="none", caption="Kitchen · First Floor · Oct 2026", room="Kitchen"))
nvadd("From Max Sign-Off", "hg",
 nv("signoff", "hg", 1, "Note From Max At The Top", "A short plain note above the sections, signed – Max.", ["personal", "warm", "friendly", "direct"],
    mode="top", copy="Niko and Vivian, everything about your house is in here. Call me anytime."),
 nv("signoff", "hg", 2, "Name And Call Max In The Footer", "No note on top. The footer says who built it, with a Call Max button.", ["clear", "direct", "practical", "personal"],
    mode="footer", copy="Built by Max Weberman"))
nvadd("Header & Navigation", "hg",
 nv("hdr", "hg", 1, "Wordmark Left, Share Right, Thin Rule", "The spec header: MAX WEBERMAN, square SHARE, 1px grey rule.", ["light", "clear", "minimal", "modern"],
    mode="rule"),
 nv("hdr", "hg", 2, "Gold Monogram Crest Header", "Centered serif MR monogram in gold over the title.", ["luxe", "formal", "classic", "elegant"],
    mode="crest"))
nvadd("Onboarding First Screen", "hg",
 nv("onb", "hg", 1, "Welcome Note, Then Start", "'Welcome home, Niko and Vivian.' One line and a Start button.", ["personal", "warm", "friendly", "clear"],
    mode="welcome", copy="Welcome home, Niko and Vivian.", sub2="Shutoffs, contacts and upkeep for your house."),
 nv("onb", "hg", 2, "Numbered Instructions Page", "A formal page of numbered rules before the guide.", ["formal", "plain", "practical", "traditional"],
    mode="rules", items=["This guide is provided for reference only.", "Consult the Documents Index for warranties.", "Contact the listed trades for service.", "Retain this guide for your records."]))

# --- Finish Questions ---
nvadd("Navigation", "fq",
 nv("nav", "fq", 3, "One Question Per Screen", "Big question, answer buttons, Next. Nothing else on screen.", ["clear", "direct", "calm", "practical"],
    mode="onepage", room="Mud Room 116", step="6 of 19", q="Mud room floor tile?", answers=["Cala Vi. Calacatta 24x24", "Jem Aria Gold 24x48", "Hardwood (no tile)"]),
 nv("nav", "fq", 4, "All Questions In One Scroll", "Every room and question on one page, grouped by room.", ["practical", "efficient", "clear", "modern"],
    mode="scroll", qs=[["Mud Room 116", "Mud room floor tile?"], ["Half Bath 115", "Vanity top here?"], ["Bedroom 201", "Carpet in this room?"]]))
nvadd("Checklists", "fq",
 nv("check", "fq", 1, "Room Chips Turn Green When Done", "Each room is a chip. Answered rooms turn jungle with a check.", ["clear", "natural", "practical", "modern"],
    mode="chips", items=FQ_ROOMS, done=3),
 nv("check", "fq", 2, "Progress Ring: 7 Of 19", "One ring shows how many questions are answered.", ["clear", "modern", "calm", "practical"],
    mode="ring", done=7, total=19, next="Next: Laundry 203"))
nvadd("Answer Style", "fq",
 nv("answer", "fq", 1, "Photo Answer Tiles", "Each answer is a tile with a picture of the material.", ["natural", "tactile", "friendly", "clear"],
    mode="tiles", q="Shower wall slab material?", answers=SLABS),
 nv("answer", "fq", 2, "Text Answer Blocks", "Full-width tinted lagoon blocks with the product names.", ["clear", "practical", "direct", "minimal"],
    mode="text", q="Shower wall slab material?", answers=[s[0] for s in SLABS]))
nvadd("Feature Options", "fq",
 nv("feature", "fq", 5, "Not Sure? Snap A Photo", "Next to Not Sure, a camera button: take a photo and Max checks it.", ["practical", "friendly", "tactile", "personal"],
    mode="notsure-photo", q="Penny tile on shower floor and main floor?", copy="Snap the floor and I'll check it."),
 nv("feature", "fq", 6, "Not Sure? Leave Max A Note", "Next to Not Sure, a short note box for what they remember.", ["personal", "warm", "friendly", "calm"],
    mode="notsure-note", q="Penny tile on shower floor and main floor?", copy="I think it's the white one from the showroom…"))
nvadd("Share Message Copy", "fq",
 nv("msg2", "fq", 1, "Plain Sentence, Then The Link", "Hi Niko and Vivian, here are the finish questions for your house.", ["personal", "clear", "friendly", "direct"],
    text="Hi Niko and Vivian, here are the finish questions for your house.", card="Finish Questions · 19 questions"),
 nv("msg2", "fq", 2, "Count And Time, Then The Link", "19 questions, about 10 minutes. Answer what you know.", ["practical", "direct", "clear", "construction"],
    text="19 finish questions for the house, about 10 minutes. Answer what you know.", card="Finish Questions · 19 questions"))
nvadd("Screen Transitions", "fq",
 nv("trans", "fq", 11, "Next Question Slides In", "The next question slides in from the right, like turning a page.", ["clear", "modern", "practical", "direct"], t="slide", next="Half Bath 115: Vanity top here?"),
 nv("trans", "fq", 12, "Next Question Rises As A Sheet", "Each question slides up from the bottom as a sheet.", ["soft", "modern", "clear", "tactile"], t="sheet", next="Half Bath 115: Vanity top here?"))
nvadd("Success & Confirmation", "fq",
 nv("done", "fq", 1, "Check Plus What Happens Next", "Check draws in: 'Sent to Max.' and what he will do with it.", ["clear", "friendly", "direct", "personal"],
    mode="next", copy="Sent to Max.", sub2="He will confirm your finishes this week."),
 nv("done", "fq", 2, "Summary Of Your Answers", "A short list of every answer they gave, with a check on top.", ["practical", "clear", "honest", "calm"],
    mode="summary", rows=[["Mud Room 116", "Cala Vi. Calacatta 24x24"], ["Bedroom 201", "Bixley Premium, Grounded"], ["Closet 209", "Duchateau Savanna hardwood"], ["Bathroom 204", "Not sure"]]))
nvadd("Checklists", "fq",
 nv("check", "fq", 3, "Room List With Jungle Checks", "When all 19 are done, every room shows a quiet jungle check.", ["clear", "natural", "calm", "practical"],
    mode="alldone", items=FQ_ROOMS[:6]),
 nv("check", "fq", 4, "Confetti At 19 Of 19", "Bright confetti bursts when the last answer goes in.", ["playful", "vibrant", "loud", "casual"],
    mode="confetti"))
nvadd("List Sorting", "fq",
 nv("sort", "fq", 3, "Walk Order, Room By Room", "Rooms in the order you walk the house, level by level.", ["practical", "construction", "clear", "natural"],
    mode="walk", groups=FQ_WALK, chips=["Walk Order", "A–Z"], head="Rooms"),
 nv("sort", "fq", 4, "A–Z Rooms With Sort Chips", "Rooms A to Z by default, with a chip for walk order.", ["clear", "direct", "practical", "modern"],
    mode="az", items=FQ_AZ, chips=["A–Z", "Walk Order"], head="Rooms"))
nvadd("From Max Sign-Off", "fq",
 nv("signoff", "fq", 3, "Thanks Line Under Send", "Under the Send Answers button: 'Thanks, Niko and Vivian. – Max'", ["personal", "warm", "direct", "friendly"],
    mode="under", copy="Thanks, Niko and Vivian. – Max"),
 nv("signoff", "fq", 4, "Why It Matters, From Max", "First screen: 'I need these to order the right replacements. – Max'", ["personal", "practical", "clear", "honest"],
    mode="why", copy="I need these to order the right replacements later. – Max"))
nvadd("Typography Scale", "fq",
 nv("qtype", "fq", 1, "Khand Question, Hind Answers", "Tight Khand question, plain Hind answer buttons.", ["clear", "modern", "direct", "friendly"], serif=False),
 nv("qtype", "fq", 2, "Serif Question, Magazine Style", "A large serif italic question like a magazine page.", ["editorial", "classic", "refined", "soft"], serif=True))

# --- Site Walk ---
nvadd("Checklists", "sw",
 nv("check", "sw", 5, "Tap The Row To Check It Off", "The whole row is the button. Done rows turn jungle.", ["practical", "clear", "direct", "modern"],
    mode="tap", items=SW_ITEMS[:5], done=2, head="Stop 1: Mechanical Room"),
 nv("check", "sw", 6, "Checkbox Plus A Photo Slot", "Each item has a checkbox and a small photo slot to fill.", ["practical", "construction", "clear", "honest"],
    mode="photo", items=SW_ITEMS[:5], done=2, head="Stop 1: Mechanical Room"))
nvadd("Photo Handling", "sw",
 nv("photo", "sw", 1, "Photo Markup: Draw On It", "Circle and arrow right on the photo to show the spot.", ["tactile", "construction", "practical", "direct"],
    mode="markup", eq="heater", room="Water Heater 1", copy="Label here"),
 nv("photo", "sw", 2, "Photo Notes: Type Under It", "A short note under each photo, no drawing.", ["clear", "calm", "practical", "honest"],
    mode="notes", eq="heater", room="Water Heater 1", copy="Rinnai. New label photo. Gas line on the left."))
nvadd("Navigation", "sw",
 nv("nav", "sw", 5, "Big Next Stop Button", "One wide Next Stop button at the bottom of each stop.", ["direct", "clear", "practical", "calm"],
    mode="nextbtn", stop=2, stops=SW_STOPS),
 nv("nav", "sw", 6, "Stop Dots To Jump Around", "Numbered dots 1 to 7 on top. Tap any stop, done ones are green.", ["modern", "clear", "tactile", "practical"],
    mode="dots", stop=2, stops=SW_STOPS))
nvadd("Feature Options", "sw",
 nv("feature", "sw", 7, "Offline Mode: Saves On The Phone", "No signal in the basement? Notes and photos save on the phone.", ["practical", "calm", "honest", "construction"],
    mode="offline", copy="No signal down here. Notes and photos are saved on this phone.", head="Stop 2: Unfinished Basement"),
 nv("feature", "sw", 8, "Live Sync To Max", "Every check and photo reaches Max as soon as it is taken.", ["modern", "direct", "personal", "friendly"],
    mode="live", copy="Sump Pump 1 (Check) · photo sent", stamp="Synced to Max · just now", head="Stop 2: Unfinished Basement"))
nvadd("Feature Options", "sw",
 nv("feature", "sw", 9, "Voice Note Per Item", "Hold the mic and talk. The app types it out.", ["direct", "tactile", "personal", "modern"],
    mode="voice", item="Furnace 1 Humidifier", copy="Pad looks fine, water line is dry."),
 nv("feature", "sw", 10, "Typed Note Per Item", "A small text box under each item.", ["clear", "calm", "practical", "honest"],
    mode="typed", item="Furnace 1 Humidifier", copy="Pad looks fine, water line is dry."))
nvadd("Condensed Lists", "sw",
 nv("rows", "sw", 5, "Compact Equipment Rows That Expand", "One line per item. Tap to see the model and notes.", ["practical", "clear", "minimal", "direct"],
    mode="expand", items=SW_ITEMS, open=4, detail=["Rinnai · new label photo", "Check the gas valve"], head="Stop 1: Mechanical Room"),
 nv("rows", "sw", 6, "Equipment Cards With A Photo", "Each item is a card with a photo and its name.", ["natural", "friendly", "clear", "tactile"],
    mode="cards", items=SW_ITEMS[:3], eqs=["filter", "pump", "erv"], head="Stop 1: Mechanical Room"))
nvadd("Notifications", "sw",
 nv("notify", "sw", 3, "Text Max When The Walk Is Done", "Max gets a short text with the stop and photo count.", ["direct", "personal", "casual", "practical"],
    mode="sms", copy="Niko finished the site walk: 7 of 7 stops, 23 photos."),
 nv("notify", "sw", 4, "Email Summary With Photos", "An email with every stop, note and photo thumbnail.", ["clear", "practical", "calm", "honest"],
    mode="email", subject="Moschouris site walk · 7 stops, 23 photos", eqs=["heater", "filter", "pump"]))
nvadd("Share & Sign-Off", "sw",
 nv("sharef", "sw", 1, "Finish And Share: One PDF Report", "Finish makes one tidy PDF with every stop and photo.", ["practical", "clear", "construction", "tidy"],
    mode="pdf"),
 nv("sharef", "sw", 2, "Finish And Share: A Link", "Finish sends a link to the photos and notes, nothing to download.", ["modern", "direct", "clear", "friendly"],
    mode="link"))
nvadd("App Icon & Favicon", "sw",
 nv("icon", "sw", 13, "Outlined Square, Jungle Check Dot", "White tile, 2px black border, SW, small jungle check in the corner.", ["clear", "natural", "practical", "modern"],
    shape="square", bg="#fff", fg="#171717", mark="SW", border=True, dot="#0B6E4F"),
 nv("icon", "sw", 14, "Outlined Square, Faint Grid", "White tile, 2px black border, SW over a faint grid.", ["technical", "construction", "minimal", "clear"],
    shape="square", bg="#fff", fg="#171717", mark="SW", border=True, grid=True))
nvadd("Checklists", "sw",
 nv("check", "sw", 7, "Stop Rows With A Jungle Done Dot", "Plain rows; a small jungle dot marks each finished stop.", ["clear", "calm", "natural", "practical"],
    mode="dots", items=SW_STOPS[:6], done=3),
 nv("check", "sw", 8, "Bold Color Stop Tiles", "Each stop is a big saturated color tile.", ["vibrant", "loud", "bold", "lively"],
    mode="tiles", items=SW_STOPS[:6]))
nvadd("Feature Options", "sw",
 nv("feature", "sw", 11, "Simple Stop 3 Of 7 Progress", "Just the stop count and a thin jungle line.", ["clear", "calm", "practical", "minimal"],
    mode="progress", stop=3, total=7, head="Stop 3: Finished Basement"),
 nv("feature", "sw", 12, "Points And Badges For Each Stop", "+50 points per stop and a badge at the end.", ["playful", "loud", "vibrant", "casual"],
    mode="points", head="Stop 3: Finished Basement"))

# --- Room Photos ---
nvadd("Photo Handling", "rp",
 nv("photo", "rp", 3, "Three-Up Grid Per Room", "Square thumbnails, three across, under each room name.", ["clear", "practical", "modern", "natural"],
    mode="grid", room="Living Area 004", keys=["tr_boutique_lobby"] * 6),
 nv("photo", "rp", 4, "Swipeable Carousel Per Room", "One big photo per room; swipe through, dots show how many.", ["natural", "personal", "tactile", "modern"],
    mode="carousel", room="Living Area 004", key="tr_boutique_lobby", n=4))
nvadd("Photo Handling", "rp",
 nv("photo", "rp", 5, "Shrink Photos Before Upload", "Photos are resized on the phone so they upload fast.", ["practical", "clear", "efficient", "direct"],
    mode="shrink", copy="12 photos · 48 MB → 9 MB"),
 nv("photo", "rp", 6, "Keep Full-Size Originals", "Every photo goes up at full quality, even if it is slower.", ["honest", "practical", "natural", "calm"],
    mode="full", copy="12 photos · 48 MB · full quality"))
nvadd("List Sorting", "rp",
 nv("sort", "rp", 5, "Rooms A–Z With Photo Counts", "A to Z by default, each room with its photo count.", ["clear", "direct", "practical", "minimal"],
    mode="azcount", rooms=RP_AZ, chips=["A–Z", "Level", "Needs Photos"], head="All Rooms", nosub=True),
 nv("sort", "rp", 6, "Rooms Missing Photos First", "Rooms with no photos float to the top under 'Needs Photos'.", ["practical", "direct", "construction", "clear"],
    mode="need", rooms=RP_AZ, chips=["A–Z", "Level", "Needs Photos"], head="All Rooms", nosub=True))
nvadd("Feature Options", "rp",
 nv("feature", "rp", 13, "Camera Opens Right Away", "Add Photos jumps straight to the camera.", ["direct", "tactile", "practical", "modern"],
    mode="camera", item="Kitchen 006"),
 nv("feature", "rp", 14, "Pick From The Photo Library", "Add Photos opens their library to pick photos they already took.", ["calm", "practical", "friendly", "clear"],
    mode="library", item="Kitchen 006", keys=["int_modernkitchen", "tr_boutique_lobby", "int_boho", "int_midcentury", "tr_glamping", "ext_craftsman"]))
nvadd("Navigation", "rp",
 nv("nav", "rp", 7, "Tap A Room On The Floor Plan", "Floor plan with photo counts; tap a room to add photos.", ["architectural", "tactile", "natural", "modern"],
    mode="plan", head="Basement", rooms=["Gym 012", "Wine 008", "Living Area 004", "Bathroom 005", "Family Suite 002", "Mech Room"], counts=[0, 2, 4, 3, 6, 1], toggle=["Floor Plan", "Room List"]),
 nv("nav", "rp", 8, "Room List By Level", "Levels as headers, rooms listed under each.", ["clear", "practical", "direct", "calm"],
    mode="levellist", groups=[["Basement", ["Bathroom 005", "Family Suite 002", "Gym 012", "Living Area 004"]], ["First Floor", ["Kitchen 006", "Mud Room 116"]]]))
nvadd("Condensed Lists", "rp",
 nv("rows", "rp", 7, "Room Rows With A Thumbnail Strip", "Each row shows the first few photos as tiny thumbnails.", ["natural", "clear", "friendly", "practical"],
    mode="thumbs", rooms=RP_AZ[:4], keys=["tr_boutique_lobby", "int_boho", "int_modernkitchen", "int_midcentury"]),
 nv("rows", "rp", 8, "Room Rows With A Count Badge", "Each row shows only a lagoon badge with the photo count.", ["minimal", "clear", "practical", "direct"],
    mode="badges", rooms=RP_AZ[:6]))
nvadd("Share & Sign-Off", "rp",
 nv("sharef", "rp", 3, "Share By Level", "One Share button per level, with its photo count.", ["practical", "clear", "tidy", "construction"],
    mode="levels", levels=RP_LEVELS),
 nv("sharef", "rp", 4, "Share All Photos At Once", "One big Share All button for every room.", ["direct", "clear", "minimal", "modern"],
    mode="all", total=54))
nvadd("Imagery Treatment", "rp",
 nv("image", "rp", 13, "True Color, No Filter", "Photos exactly as taken, 12px corners.", ["natural", "honest", "clear", "modern"],
    key="tr_boutique_lobby", frame="round", filt="none", room="Living Area 004"),
 nv("image", "rp", 14, "Bright Lift (+15% Exposure)", "Photos brightened a little so dim rooms read clearly.", ["light", "soft", "warm", "natural"],
    key="tr_boutique_lobby", frame="round", filt="brightness(1.15) saturate(.95)", room="Living Area 004"))
nvadd("Share Message Copy", "rp",
 nv("msg2", "rp", 3, "Plain: Every Room, Sorted By Level", "Here are the room photos, sorted by level.", ["clear", "practical", "direct", "friendly"],
    text="Here are the room photos, sorted by level.", card="Room Photos · 54 photos"),
 nv("msg2", "rp", 4, "Personal Note From Max", "Niko, here are today's photos. Every room is in there. – Max", ["personal", "warm", "friendly", "casual"],
    text="Niko, here are today's photos. Every room is in there. – Max", card="Room Photos · 54 photos"))
nvadd("Photo Handling", "rp",
 nv("photo", "rp", 7, "Clean Grid With Room Labels", "Straight square tiles, room name above each set.", ["clear", "natural", "calm", "practical"],
    mode="grid", room="Kitchen 006", keys=["int_modernkitchen"] * 6),
 nv("photo", "rp", 8, "Vintage Film Frames", "Photos in sepia film-strip frames with sprocket holes.", ["retro", "editorial", "warm", "craft"],
    mode="film", room="Kitchen 006", key="int_modernkitchen"))
nvadd("Empty States", "rp",
 nv("empty2", "rp", 1, "Camera Icon And One Line", "Grey camera in a circle: 'No photos yet. Add the first one.'", ["clear", "friendly", "minimal", "direct"],
    mode="icon", copy="No photos yet. Add the first one.", item="Gym 012"),
 nv("empty2", "rp", 2, "Cartoon Camera Mascot", "A waving cartoon camera: 'Say cheese!'.", ["playful", "cute", "vibrant", "casual"],
    mode="mascot", copy="Say cheese! No photos yet.", item="Gym 012"))

# --- SiteAgent share card (retest) ---
nvadd("Share Preview (OG Card)", "sa",
 nv("og2", "sa", 1, "Site Photo Left, Claim Right", "Site photo on the left, Khand claim and grey subline on the right.", ["construction", "clear", "natural", "practical"],
    mode="left"),
 nv("og2", "sa", 2, "Light Grid Card, Big Claim", "Light grey blueprint grid, big Khand claim, small wordmark.", ["construction", "technical", "direct", "modern"],
    mode="grid"))

# --- Swipe Controls: refine inside the lean (earthy round or pill, gesture hint visible, stamp on swipe) ---
SC_WORDS["tblt"] = (["This", "Both", "Love", "That"], ["◀", "⇄", "❤", "▶"])
SC_PAL["earth4"] = ["#3F6E7D", "#5A7D4F", "#B5523B", "#A0703C"]   # dusty lagoon, moss, clay, ochre
def ctl2(i, label, desc, tags, fmt, style, hint="above", stampov="word", press=None, bg="#FAF3EB"):
    o = ctl(i, label, desc, tags, fmt, "tblt", "earth4", style, bg)
    o["visual"].update({"hint": hint, "stampov": stampov, "press": press})
    return o
NV_SC = [
 (ctl2("sc_nv_round_filled", "Earthy Round Buttons, Filled", "Filled clay, moss, ochre circles; hint above; stamp on swipe.", ["warm", "natural", "clear", "colorful"], "round", "filled"),
  ctl2("sc_nv_round_outline", "Earthy Round Buttons, Outline", "Same circles as outlines, color on the ring and icon only.", ["light", "natural", "minimal", "clear"], "round", "outline")),
 (ctl2("sc_nv_pill_filled", "Earthy Pills, Filled", "Filled earthy pills with words; hint above; stamp on swipe.", ["warm", "clear", "friendly", "natural"], "pill", "filled"),
  ctl2("sc_nv_pill_fillpress", "Earthy Pills, Outline Until Pressed", "Outline pills that fill with color when tapped.", ["light", "tactile", "clear", "natural"], "pill", "outline", press="fill")),
 (ctl2("sc_nv_hint_above", "Hint Line Above The Buttons", "'← This · That →' sits just above the round buttons.", ["clear", "minimal", "practical", "light"], "round", "outline", hint="above"),
  ctl2("sc_nv_hint_card", "Hint Arrows On The Card Edges", "Faint ← and → arrows sit on the card's left and right edges.", ["minimal", "light", "modern", "calm"], "round", "outline", hint="edges")),
 (ctl2("sc_nv_stamp_word", "Stamp: Word In Khand Caps", "Swiping shows a tilted outline stamp: THIS or THAT.", ["construction", "craft", "clear", "warm"], "pill", "outline", stampov="word"),
  ctl2("sc_nv_stamp_icon", "Stamp: Check Icon Plus Word", "Swiping shows a round stamp with a check over the word.", ["clear", "friendly", "natural", "craft"], "pill", "outline", stampov="icon")),
]
for _a, _b in NV_SC: POOL[SWIPE_CONTROLS].extend([_a, _b])

for _cat, _app, _a, _b in NV:
    POOL.setdefault(_cat, []).extend([_a, _b])
    CATEGORY_WEIGHT.setdefault(_cat, 1.0)
    GROUP_OF.setdefault(_cat, _cat)
NV_RETEST = {"App Icon & Favicon", "Imagery Treatment", "Share Message Copy", "From Max Sign-Off", "Screen Transitions", "Share Preview (OG Card)"}
NV_ASK = {"Feature Options": "Which Should {app} Do?", "Navigation": "Which Works Better For {app}?", "List Sorting": "Which Works Better For {app}?",
          "Condensed Lists": "Which Works Better For {app}?", "Checklists": "Which Works Better For {app}?", "Notifications": "Which Should {app} Do?",
          "Photo Handling": "Which Works Better For {app}?", "Share & Sign-Off": "Which Should {app} Do?", "Answer Style": "Which Works Better For {app}?"}


# ---- Niko & Vivian deck, round 2 (2026-10-12b): look AND function for the same four client apps ----
# Retests the 10 pairs Max skipped in 2026-10-11b (as fresh, sharper options), the app-polish-spec retest topics
# (icon, imagery, share copy, sign-off, transitions, SiteAgent share card), plus new function questions:
# warranties, shutoffs, who to call, task tracking, install card, edit-after-send, reminders, resume, problem flags,
# viewer, before/after, upload progress, select and download. Most screens use the generic 'scr' composer. Light mode only.
def nv2(kind, app, slug, label, desc, tags, **p):
    c = NVAPPS[app]
    return {"id": f"nv2_{app}_{slug}", "label": label, "desc": desc, "tags": tags, "app": c["name"],
            "visual": {"type": "polish", "kind": kind, "app": c["name"], "c": c, "p": p}}
def scr(app, slug, label, desc, tags, blocks, **p): return nv2("scr", app, slug, label, desc, tags, blocks=blocks, **p)

NV2 = []   # (category, app key, option A, option B, retest?)
def nv2add(cat, app, a, b, retest=False): NV2.append((cat, app, a, b, retest))
FQ_SWATCH = ["#ECEBE8", "#F3ECDD", "#DDDFE0", "#EDE7DC"]

# --- Retests of the 10 pairs skipped in deck 2026-10-11b ---
nv2add("Feature Options", "fq",
 scr("fq", "notsure_both", "Not Sure: Add A Photo Or A Note", "Tapping Not Sure shows two small buttons. They pick either one, or neither.", ["practical", "friendly", "personal", "clear"],
     [["q", "Penny tile on shower floor and main floor?", 13], ["ans", ['Carrara Catalina 1" penny', "Aquarius White penny"], None], ["ans", ["Not Sure"], 0], ["btns", ["📷 Add Photo", "✎ Add Note"]], ["small", "Optional. Max can check it for you."]], head="Bathroom 204", sub=""),
 scr("fq", "notsure_mark", "Not Sure: Just Mark It, Max Follows Up", "Not Sure is one tap. No photo or note. Max sorts it out later.", ["direct", "calm", "clear", "personal"],
     [["q", "Penny tile on shower floor and main floor?", 13], ["ans", ['Carrara Catalina 1" penny', "Aquarius White penny"], None], ["ans", ["Not Sure"], 0], ["small", "Got it. Max will look at this one with you."], ["spacer"], ["btn", "Next →", "full"]], head="Bathroom 204", sub=""), True)
nv2add("Navigation", "sw",
 scr("sw", "next_only", "One Big Next Stop Button", "Only the next stop. The stop count sits above, and there's nothing else to tap.", ["direct", "clear", "calm", "practical"],
     [["progress", 2, 7, "Stop 2"], ["q", "Unfinished Basement Area", 13], ["ph", 4], ["spacer"], ["btn", "Next Stop →", "full"]], sub=""),
 scr("sw", "next_dots", "Next Stop Button Plus Stop Dots", "The same button at the bottom, plus dots 1 to 7 on top to jump back.", ["practical", "clear", "tactile", "modern"],
     [["chips", ["✓ 1", "2", "3", "4", "5", "6", "7"], 1], ["q", "Unfinished Basement Area", 13], ["ph", 3], ["spacer"], ["btn", "Next Stop →", "full"]], sub=""), True)
nv2add("Feature Options", "hg",
 scr("hg", "pin_and_search", "Emergencies Pinned, Search Under It", "Both: a red-outlined Emergencies card on top, and a search bar right below.", ["practical", "clear", "direct", "construction"],
     [["pin", "Water, gas and power shutoffs"], ["search", ""], ["row", "Who to Call"], ["row", "Maintenance Schedule"], ["row", "Warranties"]]),
 scr("hg", "search_only", "Search On Top, Emergencies In The List", "One search bar. Emergencies is the first row, styled like the rest.", ["minimal", "clear", "modern", "calm"],
     [["search", ""], ["row", "Emergencies", "›", "b"], ["row", "Who to Call"], ["row", "Maintenance Schedule"], ["row", "Warranties"], ["row", "Shutoffs & Key Locations"]]), True)
nv2add("Answer Style", "fq",
 scr("fq", "ans_tiles", "Material Photo Tiles, Name Underneath", "Two-up tiles with a picture of each material and its name under it.", ["natural", "tactile", "clear", "friendly"],
     [["q", "Shower wall slab material?", 13], ["tilesans", SLABS, 1, 34]], head="Bathroom 204", sub=""),
 scr("fq", "ans_swatch", "Text Rows With A Small Swatch", "Full-width rows with the product name and a small color chip on the left.", ["clear", "practical", "direct", "minimal"],
     [["q", "Shower wall slab material?", 13], ["ans", [s[0] for s in SLABS], 1, "swatch", FQ_SWATCH]], head="Bathroom 204", sub=""), True)
nvadd_msg = [
 nv2("msg2", "fq", "msg_warm_count", "Hi, Count And Time, Then The Link", "A greeting plus how many questions and how long they take.", ["personal", "clear", "friendly", "practical"],
     text="Hi Niko and Vivian, 19 quick finish questions for the house, about 10 minutes. Answer what you know.", card="Finish Questions · 19 questions"),
 nv2("msg2", "fq", "msg_short", "One Short Line, Then The Link", "Just: Finish questions for the house. About 10 minutes.", ["direct", "minimal", "clear", "calm"],
     text="Finish questions for the house. About 10 minutes.", card="Finish Questions · 19 questions")]
nv2add("Share Message Copy", "fq", *nvadd_msg, True)
nv2add("App Icon & Favicon", "sw",
 nv2("icon", "sw", "icon_roof", "Light Grey Tile, Roofline Over SW", "Matches the Home Guide icon: light grey tile, thin black roof line above SW.", ["architectural", "clear", "personal", "light"],
     shape="square", bg="#EDEDED", fg="#171717", mark="SW", roof=True),
 nv2("icon", "sw", "icon_white_dot", "White Tile, Thin Border, Jungle Dot", "White tile, 1px border, SW in Khand, small jungle check in the corner.", ["clear", "natural", "minimal", "light"],
     shape="square", bg="#fff", fg="#171717", mark="SW", border=True, dot="#0B6E4F"), True)
nv2add("Feature Options", "sw",
 scr("sw", "offline_queue", "Saves On The Phone, Sends When Back Online", "A quiet line says what's waiting. It sends on its own when signal returns.", ["practical", "calm", "honest", "clear"],
     [["strip", "No signal. 3 photos are waiting to send.", "grey", "⤓"], ["row", "Sump Pump 1 (Check)", "boxon"], ["row", "ERV System", "boxon"], ["row", "Furnace 1 Humidifier", "box"], ["row", "Water Heater 1 (Rinnai)", "box"], ["small", "Everything is saved on this phone."]], head="Stop 2: Unfinished Basement", sub=""),
 scr("sw", "live_line", "Live Status Line: Sent To Max", "A small line under the header shows each check and photo reaching Max.", ["modern", "direct", "personal", "clear"],
     [["strip", "Sent to Max · just now", "ok", "●"], ["row", "Sump Pump 1 (Check)", "boxon"], ["row", "ERV System", "boxon"], ["row", "Furnace 1 Humidifier", "box"], ["row", "Water Heater 1 (Rinnai)", "box"], ["small", "Max sees each photo as you take it."]], head="Stop 2: Unfinished Basement", sub=""), True)
nv2add("Feature Options", "rp",
 scr("rp", "add_ask", "Add Photos Asks: Camera Or Library", "One tap opens a small sheet with Take Photos and Choose From Library.", ["clear", "practical", "friendly", "calm"],
     [["row", "Kitchen 006", "badge:8"], ["row", "Living Area 004", "badge:4"], ["row", "Mud Room 116", "badge:0"], ["sheet", "Add Photos to Mud Room 116", [], ["📷 Take Photos", "▦ Choose From Library"], "first"]], sub=""),
 scr("rp", "add_camera_lib", "Camera Opens, Library Button In The Corner", "Straight to the camera, with a small Library button bottom-left.", ["direct", "tactile", "practical", "modern"],
     [["photo", "int_modernkitchen", 128, "Mud Room 116"], ["btns", ["▦ Library", "◉ Shoot", "Done"]]], head="Add Photos", sub=""), True)
nv2add("Share Preview (OG Card)", "sa",
 nv2("og", "sa", "og_bleed", "Site Photo, Claim On A Light Fade", "Full site photo with the Khand claim on a white fade at the bottom.", ["construction", "natural", "clear", "modern"], layout="bleed"),
 nv2("og", "sa", "og_text", "Clean White Card, Big Claim, Wordmark", "No photo. Big Khand claim and the small MAX WEBERMAN wordmark.", ["clear", "direct", "minimal", "light"], layout="text"), True)

# --- Home Guide (Moschouris Residence) ---
nv2add("List Sorting", "hg",
 nv("sort", "hg", 21, "Warranties: Ending Soonest First", "Warranties that run out soonest float to the top.", ["practical", "direct", "clear", "honest"],
    mode="level", chips=["Ending Soon", "By System", "A–Z"], groups=[["Ending Soon", ["Water Heater 1 (Rinnai)"]], ["Later", ["Furnace 1", "Kitchen Appliances", "Roof", "Windows"]]], head="Warranties"),
 nv("sort", "hg", 22, "Warranties: Grouped By System", "Heating, Water, Kitchen, Exterior, with each warranty under its system.", ["clear", "practical", "calm", "architectural"],
    mode="level", chips=["Ending Soon", "By System", "A–Z"], groups=[["Heating", ["Furnace 1"]], ["Water", ["Water Heater 1 (Rinnai)", "Sump Pump 1"]], ["Exterior", ["Roof", "Windows"]]], head="Warranties"))
nv2add("Feature Options", "hg",
 scr("hg", "shutoff_photo", "Shutoff With A Photo Of The Valve", "Each shutoff shows where it is, with a photo and a marked spot.", ["practical", "clear", "natural", "honest"],
     [["photo", "eq:filter", 92, "Main water valve"], ["txt", "Mech Room, by the water filter system.", 10], ["small", "Turn the handle a quarter turn to close."]], head="Water Shutoff", sub="Shutoffs & Key Locations"),
 scr("hg", "shutoff_steps", "Shutoff As Three Short Steps", "Numbered steps in big type, no photo.", ["direct", "clear", "calm", "practical"],
     [["q", "1. Go to the Mech Room.", 13], ["q", "2. Find the main water valve by the filter.", 13], ["q", "3. Turn the handle a quarter turn.", 13], ["small", "Then call the plumber from Who to Call."]], head="Water Shutoff", sub="Shutoffs & Key Locations"))
nv2add("Condensed Lists", "hg",
 scr("hg", "call_trade", "Who To Call: One Row Per Trade, Call Button", "Plumber, Electrician, HVAC, each with a small Call button.", ["direct", "practical", "clear", "construction"],
     [["row", "Plumber", "chip:Call"], ["row", "Electrician", "chip:Call"], ["row", "HVAC", "chip:Call"], ["row", "Water Heater (Rinnai)", "chip:Call"], ["row", "Builder: Max", "chip:Call"]], head="Who to Call", sub=""),
 scr("hg", "call_system", "Who To Call: Listed Under Each System", "Open a system, like Water Heater 1, and its service contact is right there.", ["practical", "clear", "calm", "architectural"],
     [["rowx", "Water Heater 1 (Rinnai)", ["Service: Rinnai dealer", "Call · Model and serial"]], ["row", "Furnace 1"], ["row", "Sump Pump 1"], ["row", "ERV System"], ["row", "Irrigation Controller"]], head="Home Systems & Equipment", sub=""))
nv2add("Checklists", "hg",
 scr("hg", "task_done", "Tap A Task To Mark It Done", "Each task gets a box. Tapping it saves the date it was done.", ["practical", "clear", "honest", "tactile"],
     [["row", "Change furnace filters", "grey:Done Oct 3", "mute"], ["row", "Test Sump Pump 1", "box"], ["row", "Replace humidifier pad", "box"], ["row", "Shut off irrigation", "box"], ["small", "1 of 4 done this fall"]], head="Maintenance Schedule", sub="Fall"),
 scr("hg", "task_list", "Just The List, No Tracking", "The schedule is a reference list. Nothing to check off.", ["minimal", "calm", "clear", "direct"],
     [["row", "Change furnace filters", "grey:Every 3 months"], ["row", "Test Sump Pump 1", "grey:Every fall"], ["row", "Replace humidifier pad", "grey:Every fall"], ["row", "Shut off irrigation", "grey:Before frost"]], head="Maintenance Schedule", sub="Fall"))
nv2add("Onboarding First Screen", "hg",
 scr("hg", "install_card", "Keep This Guide On Your Phone Card", "Right after sign-in, a small card offers Add to Home Screen once.", ["practical", "friendly", "clear", "personal"],
     [["install", "Keep this guide on your phone", "One tap from your home screen, like an app."], ["row", "Emergencies"], ["row", "Who to Call"], ["row", "Maintenance Schedule"]]),
 scr("hg", "install_footer", "Small Add To Home Screen Tip In The Footer", "No popup. A one-line tip sits in the footer, always there.", ["minimal", "calm", "clear", "light"],
     [["row", "Emergencies"], ["row", "Who to Call"], ["row", "Maintenance Schedule"], ["row", "Warranties"], ["spacer"], ["small", "Tip: add this guide to your home screen."], ["small", "Built by Max Weberman"]]))
nv2add("Feature Options", "hg",
 scr("hg", "pw_remember", "Password Once, Remember This Phone", "They type the password once. A box keeps the phone signed in.", ["practical", "friendly", "calm", "clear"],
     [["q", "Welcome back.", 16], ["input", "••••", 16], ["row", "Remember this phone", "boxon", "b"], ["btn", "Open the Guide", "full", "solid"]], sub=""),
 scr("hg", "pw_every", "Password Every Time", "The guide always asks for the password. Nothing is kept on the phone.", ["honest", "clear", "direct", "construction"],
     [["q", "Enter the password.", 16], ["input", "••••", 16], ["small", "For privacy, this guide asks every time."], ["btn", "Open the Guide", "full", "solid"]], sub=""))
nv2add("Condensed Lists", "hg",
 scr("hg", "eq_labelphoto", "Equipment: Label Photo Plus Model And Serial", "The equipment page shows a photo of the label, then the numbers.", ["practical", "honest", "natural", "clear"],
     [["photo", "eq:heater", 70, "Label photo"], ["kv", [["Model", "Rinnai tankless"], ["Location", "Mech Room"]]]], head="Water Heater 1", sub="Home Systems & Equipment"),
 scr("hg", "eq_copy", "Equipment: Model And Serial With Copy Buttons", "No photo. The model and serial each have a Copy button for calls.", ["direct", "clear", "minimal", "practical"],
     [["kv", [["Model", "Rinnai tankless"], ["Serial", "On label"], ["Location", "Mech Room"]], True], ["small", "Copy the numbers when you call for service."]], head="Water Heater 1", sub="Home Systems & Equipment"))
nv2add("Layout", "hg",
 scr("hg", "rows_icons", "Calm Rows With Small Line Icons", "White rows, a thin line icon on each, one accent only.", ["clear", "calm", "minimal", "light"],
     [["row", "🚨  Emergencies"], ["row", "☎  Who to Call"], ["row", "▦  Maintenance Schedule"], ["row", "✓  Warranties"], ["row", "⌂  Shutoffs & Key Locations"]], hdr="mw"),
 scr("hg", "tiles_bright", "Big Bright Section Tiles", "Every section is a big saturated color tile.", ["vibrant", "loud", "playful", "bold"],
     [["tiles", ["Emergencies", "Who to Call", "Maintenance", "Warranties", "Shutoffs", "Equipment"]]], hdr="mw"))

# --- Finish Questions ---
nv2add("Feature Options", "fq",
 scr("fq", "edit_until", "Change Answers Until Max Confirms", "After sending, answers stay editable until Max marks them confirmed.", ["friendly", "practical", "calm", "honest"],
     [["banner", "Sent to Max. You can still change answers until he confirms.", "ok", "✓"], ["row", "Mud Room 116", "chip:Edit"], ["row", "Bedroom 201", "chip:Edit"], ["row", "Bathroom 204", "chip:Edit"]], sub="All 19 answered"),
 scr("fq", "lock_sent", "Answers Lock Once Sent", "Once sent, the answers are final. Changes go through Max.", ["direct", "clear", "honest", "construction"],
     [["banner", "Sent to Max. To change an answer, text Max.", "grey", "🔒"], ["row", "Mud Room 116", "tick"], ["row", "Bedroom 201", "tick"], ["row", "Bathroom 204", "tick"]], sub="All 19 answered"))
nv2add("Notifications", "fq",
 scr("fq", "remind_text", "A Gentle Text If It Sits For 3 Days", "If answers aren't sent after 3 days, they get one short reminder text.", ["practical", "friendly", "personal", "direct"],
     [["spacer"], ["small", "Text Message · Thursday 10:02 AM"], ["bubble", "Hi Niko and Vivian, 12 of 19 finish questions are done. The rest take about 4 minutes.", "in", True], ["small", "Sent once. No more reminders after this."]], nohead=True),
 scr("fq", "remind_none", "No Reminders, Max Follows Up Himself", "The app never nudges. Max checks in when he needs the answers.", ["calm", "personal", "honest", "clear"],
     [["progress", 12, 19, "Answered"], ["note", "No rush. I'll check in with you before I order anything.", "– Max"], ["row", "Laundry 203", "odot"], ["row", "Bedroom 206", "odot"]], sub=""))
nv2add("Feature Options", "fq",
 scr("fq", "save_auto", "Saves As You Go, Picks Up Where You Left Off", "Every answer saves on its own. Opening it again starts at the next question.", ["practical", "calm", "clear", "friendly"],
     [["banner", "Welcome back. You're on question 8 of 19.", "info"], ["q", "Laundry 203: Floor tile?", 14], ["ans", ["Jem Aria Gold 24x48", "Same as Mud Room", "Not Sure"], None], ["small", "Answers save on this phone as you go."]], sub=""),
 scr("fq", "save_room", "Save Button At The End Of Each Room", "A Save Room button at the bottom of each room. Nothing saves until it is tapped.", ["direct", "clear", "honest", "construction"],
     [["q", "Laundry 203: Floor tile?", 14], ["ans", ["Jem Aria Gold 24x48", "Same as Mud Room", "Not Sure"], 0], ["spacer"], ["btn", "Save Laundry 203", "full", "solid"]], sub=""))
nv2add("Feature Options", "fq",
 scr("fq", "two_answer", "Niko And Vivian Each Answer, Then Compare", "Each answers on their own phone. Different answers show up side by side.", ["personal", "friendly", "practical", "clear"],
     [["q", "Mud room floor tile?", 13], ["kv", [["Niko", "Cala Vi. Calacatta 24x24"], ["Vivian", "Jem Aria Gold 24x48"]]], ["banner", "You picked different tiles. Pick one together?", "clay"], ["btns", ["Use Niko's", "Use Vivian's"]]], sub="Mud Room 116"),
 scr("fq", "one_shared", "One Shared Set Of Answers", "One link, one set of answers. Whoever answers, it counts for both.", ["clear", "direct", "calm", "minimal"],
     [["q", "Mud room floor tile?", 13], ["ans", ["Cala Vi. Calacatta 24x24", "Jem Aria Gold 24x48", "Hardwood (no tile)"], 0], ["small", "Answered by Vivian · shared with Niko"]], sub="Mud Room 116"))
nv2add("Question Context", "fq",
 scr("fq", "ctx_photo", "Show A Photo Of The Room", "Each question has a small photo of that room on top.", ["natural", "clear", "friendly", "tactile"],
     [["photo", "int_concrete", 62, "Mud Room 116"], ["q", "Mud room floor tile?", 13], ["ans", ["Cala Vi. Calacatta 24x24", "Jem Aria Gold 24x48"], None]], sub=""),
 scr("fq", "ctx_plan", "Show Where It Is On The Plan", "A tiny floor plan with the room shaded.", ["architectural", "clear", "practical", "construction"],
     [["plan", ["Kitchen", "Greatroom", "Foyer", "Mud Room", "Half Bath"], 3, 58], ["q", "Mud room floor tile?", 13], ["ans", ["Cala Vi. Calacatta 24x24", "Jem Aria Gold 24x48"], None]], sub=""))
nv2add("Answer Style", "fq",
 scr("fq", "sel_fill", "Picked Answer Fills Jungle", "The picked answer turns solid jungle green with white text.", ["clear", "natural", "direct", "modern"],
     [["q", "Vanity top here?", 14], ["ans", ["Carrara Fina quartz", "Calacatta Vivo quartz", "Not Sure"], 1]], head="Half Bath 115", sub=""),
 scr("fq", "sel_check", "Picked Answer Gets An Outline And A Check", "White rows. The picked one gets a jungle outline and a check on the right.", ["light", "clear", "calm", "minimal"],
     [["q", "Vanity top here?", 14], ["ans", ["Carrara Fina quartz", "Calacatta Vivo quartz", "Not Sure"], 1, "check"]], head="Half Bath 115", sub=""))
nv2add("Error States", "fq",
 nv2("error", "fq", "err_card", "Couldn't Send: Saved, Try Again", "A calm card says the answers are safe on the phone, with Try Again.", ["calm", "clear", "honest", "friendly"],
     style="card", copy="Couldn't send just now. Your answers are saved on this phone."),
 scr("fq", "err_banner", "Couldn't Send: Red Banner On Top", "A thin red banner across the top, with the screen still usable.", ["direct", "clear", "practical", "honest"],
     [["strip", "Not sent. No connection. Trying again.", "err", "⚠"], ["row", "Mud Room 116", "tick"], ["row", "Bedroom 201", "tick"], ["row", "Bathroom 204", "tick"], ["btn", "Send Answers", "full", "solid"]], sub="All 19 answered"))
nv2add("Answer Style", "fq",
 scr("fq", "ans_emoji", "Fun Emoji Answer Buttons", "Each answer is a candy-colored pill with an emoji.", ["playful", "vibrant", "casual", "loud"],
     [["q", "Carpet in this room?", 14], ["ans", ["Bixley Premium, Grounded", "Hardwood instead", "Not Sure"], None, "emoji"]], head="Bedroom 201", sub=""),
 scr("fq", "ans_text", "Calm Text Answer Buttons", "Tinted lagoon rows with the product names.", ["clear", "calm", "direct", "practical"],
     [["q", "Carpet in this room?", 14], ["ans", ["Bixley Premium, Grounded", "Hardwood instead", "Not Sure"], None]], head="Bedroom 201", sub=""))
nv2add("Onboarding First Screen", "fq",
 scr("fq", "onb_time", "Welcome Note With How Long It Takes", "Welcome line, '19 questions, about 10 minutes', then Start.", ["personal", "clear", "friendly", "practical"],
     [["spacer"], ["q", "Hi Niko and Vivian.", 18], ["txt", "19 questions, about 10 minutes. Answer what you know.", 10.5], ["btn", "Start"], ["spacer"]], sub=""),
 scr("fq", "onb_cover", "Formal Cover Page With Project Number", "A serif cover page: project number, revision and date, then Begin.", ["formal", "traditional", "classic", "corporate"],
     [["spacer"], ["serif", "MOSCHOURIS RESIDENCE", 13, "letter-spacing:.14em"], ["serif", "Finish Selection Questionnaire · Rev. 2", 10, "font-style:italic"], ["serif", "Project No. 2026-114 · October 12, 2026", 9, "color:#737373"], ["btn", "Begin"], ["spacer"]], sub="", bg="#FFFDF7"))

# --- Site Walk ---
nv2add("Feature Options", "sw",
 scr("sw", "resume_banner", "Pick Up At The Stop You Left", "Opening it again shows one line: Continue at Stop 3.", ["practical", "clear", "direct", "calm"],
     [["banner", "Welcome back. Continue at Stop 3: Finished Basement Area.", "info"], ["btn", "Continue →", "full", "solid"], ["link", "See all stops"]], sub="2 of 7 stops done"),
 scr("sw", "resume_list", "Start Screen Lists Every Stop With Status", "Opening it again shows all 7 stops with done dots. Tap any one.", ["clear", "practical", "calm", "natural"],
     [["row", "1. Basement Mechanical Room", "dot"], ["row", "2. Unfinished Basement Area", "dot"], ["row", "3. Finished Basement Area", "odot", "b"], ["row", "4. Main Level", "odot"], ["row", "5. Master Suite", "odot"], ["row", "6. Upper Level", "odot"]], sub="2 of 7 stops done"))
nv2add("Checklists", "sw",
 scr("sw", "notfound_note", "Can't Find It? Mark Not Found With A Note", "Each item has a Not Found choice that asks for one line about it.", ["practical", "honest", "clear", "construction"],
     [["row", "ERV System", "boxon"], ["rowx", "Electrical Panels (2)", ["Not found · 'Only saw one panel by the stairs.'"]], ["row", "Water Heater 1 (Rinnai)", "box"]], head="Stop 1: Mechanical Room", sub=""),
 scr("sw", "notfound_skip", "Skip The Item, It Is Flagged For Max", "Skip moves on. Skipped items show as a list for Max at the end.", ["direct", "calm", "clear", "minimal"],
     [["row", "ERV System", "boxon"], ["row", "Electrical Panels (2)", "clay:Skipped"], ["row", "Water Heater 1 (Rinnai)", "box"], ["spacer"], ["small", "1 skipped item goes to Max with the walk."]], head="Stop 1: Mechanical Room", sub=""))
nv2add("Photo Handling", "sw",
 scr("sw", "photo_required", "Photo Required To Check It Off", "The checkbox stays locked until a photo is added.", ["practical", "honest", "construction", "direct"],
     [["photo", "eq:pump", 84, "Sump Pump 1 (Check)"], ["btn", "📷 Add Photo to Check Off", "full"], ["small", "A photo is needed for this item."]], head="Stop 2: Unfinished Basement", sub=""),
 scr("sw", "photo_optional", "Photo Optional, Check Anytime", "They can check it off right away. The photo slot is there if they want it.", ["calm", "friendly", "clear", "practical"],
     [["row", "Sump Pump 1 (Check)", "boxon", "b"], ["thumbs", ["eq:pump"], 3, 40], ["small", "Add a photo if you like."]], head="Stop 2: Unfinished Basement", sub=""))
nv2add("Imagery Treatment", "sw",
 scr("sw", "img_caption", "True-Color Photo, Caption Below", "The photo as taken, 10px corners, a small grey caption under it.", ["natural", "honest", "clear", "light"],
     [["photo", "eq:heater", 110], ["cap", "Water Heater 1 (Rinnai) · Stop 1 · Oct 12"]], head="Stop 1: Mechanical Room", sub=""),
 scr("sw", "img_tag", "Photo With A White Name Tag On It", "The same photo with a small white tag in the corner naming the item.", ["clear", "practical", "modern", "construction"],
     [["photo", "eq:heater", 120, "Water Heater 1 (Rinnai)"]], head="Stop 1: Mechanical Room", sub=""), True)
nv2add("Screen Transitions", "sw",
 nv2("trans", "sw", "tr_slide", "Next Stop Slides In From The Right", "Like turning a page, one stop to the next.", ["clear", "modern", "practical", "direct"], t="slide", next="Stop 3: Finished Basement Area"),
 nv2("trans", "sw", "tr_bounce", "Next Stop Bounces In With A Zoom", "A springy zoom-and-bounce between stops.", ["playful", "energetic", "lively", "casual"], t="bounce", next="Stop 3: Finished Basement Area"), True)
nv2add("Success & Confirmation", "sw",
 scr("sw", "done_next", "Walk Done: Check And What Max Does Next", "A check draws in. One line on what Max does with it.", ["clear", "friendly", "personal", "direct"],
     [["spacer"], ["check", 46], ["big", "Walk done. Sent to Max.", 15, "He'll go through the photos and text you this week."], ["spacer"]], sub=""),
 scr("sw", "done_summary", "Walk Done: Stop-By-Stop Summary", "A list of the 7 stops with photo counts, and anything skipped.", ["practical", "clear", "honest", "calm"],
     [["row", "1. Basement Mechanical Room", "badge:6"], ["row", "2. Unfinished Basement Area", "badge:4"], ["row", "3. Finished Basement Area", "badge:3"], ["row", "4. Main Level", "badge:5"], ["row", "Skipped", "clay:1 item"], ["btn", "Finish and Share", "full"]], sub="7 of 7 stops · 23 photos"))
nv2add("Feature Options", "sw",
 scr("sw", "flag_outline", "Problem? Flag Turns The Item Terracotta", "A small Flag button outlines the item in terracotta for Max.", ["clear", "practical", "construction", "calm"],
     [["row", "Water Filter System", "boxon"], ["row", "Sump Pump 1", "clay:⚑ Flagged", "clay"], ["row", "ERV System", "box"], ["small", "Flagged: 'Pump hums but doesn't start.'"]], head="Stop 2: Unfinished Basement", sub=""),
 scr("sw", "flag_alarm", "Problem? Big Flashing Red Alert", "A flashing red banner fills the top of the screen.", ["loud", "vibrant", "bold", "energetic"],
     [["alert", "⚠ PROBLEM FOUND!"], ["row", "Water Filter System", "boxon"], ["row", "Sump Pump 1 (Check)", "box"], ["row", "ERV System", "box"]], head="Stop 2: Unfinished Basement", sub=""))
nv2add("From Max Sign-Off", "sw",
 scr("sw", "so_thanks", "Thank-You Line From Max On Finish", "Above Finish and Share: 'Thanks for walking the house. – Max'", ["personal", "friendly", "direct", "clear"],
     [["spacer"], ["note", "Thanks for walking the house with me.", "– Max"], ["btn", "Finish and Share", "full", "solid"], ["spacer"]], sub="7 of 7 stops done"),
 scr("sw", "so_none", "No Note, Just Finish And Share", "The last screen is only the summary line and the button.", ["minimal", "clear", "direct", "calm"],
     [["spacer"], ["big", "7 of 7 stops done", 18, "23 photos · 14 notes"], ["btn", "Finish and Share", "full", "solid"], ["spacer"]], sub=""), True)

# --- Room Photos ---
nv2add("Photo Handling", "rp",
 scr("rp", "view_full", "Tap A Photo: Full Screen, Swipe Through", "Opens big on cream, with arrows and swipe to the next one.", ["natural", "tactile", "clear", "modern"],
     [["viewer", "int_modernkitchen", "Kitchen 006", "3 of 8"]], nohead=True),
 scr("rp", "view_zoom", "Tap A Photo: Zooms In Place", "The photo grows right where it is. Pinch for more.", ["direct", "tactile", "practical", "minimal"],
     [["zoom", "int_modernkitchen", 120], ["cap", "Kitchen 006 · 3 of 8"]], head="Kitchen 006", sub=""))
nv2add("Imagery Treatment", "rp",
 scr("rp", "img_date", "Small Date Under Each Photo", "A quiet grey date line under every photo.", ["clear", "honest", "practical", "light"],
     [["photo", "tr_boutique_lobby", 112, None, "f:brightness(1.15) saturate(.95)"], ["cap", "Living Area 004 · Oct 12, 2026"]], head="Living Area 004", sub=""),
 scr("rp", "img_stamp", "Orange Film-Camera Date Stamp", "A glowing orange '26 10 12 stamp in the corner, like an old camera.", ["retro", "warm", "casual", "craft"],
     [["datestamp", "tr_boutique_lobby", 118]], head="Living Area 004", sub="", ), True)
nv2add("Feature Options", "rp",
 scr("rp", "upl_each", "Upload: A Bar For Each Photo", "Every photo shows its own small progress bar.", ["practical", "clear", "honest", "tactile"],
     [["upl", "int_modernkitchen", "IMG_2041.jpg", 100], ["upl", "int_modernkitchen", "IMG_2042.jpg", 100], ["upl", "int_modernkitchen", "IMG_2043.jpg", 64], ["upl", "int_modernkitchen", "IMG_2044.jpg", 20], ["upl", "int_modernkitchen", "IMG_2045.jpg", 0]], head="Adding to Kitchen 006", sub=""),
 scr("rp", "upl_one", "Upload: One Overall Line", "One line: 'Adding 5 photos', with a single bar.", ["minimal", "calm", "clear", "direct"],
     [["thumbs", ["int_modernkitchen"] * 3, 3, 36], ["big", "Adding 5 photos", 15], ["progress", 3, 5, "Kitchen 006", True], ["small", "You can keep using the app."]], head="Adding to Kitchen 006", sub=""))
nv2add("Success & Confirmation", "rp",
 scr("rp", "ok_toast", "Quiet Toast: 5 Photos Added", "A small jungle toast at the bottom. The room list stays on screen.", ["calm", "clear", "minimal", "natural"],
     [["row", "Kitchen 006", "badge:13"], ["row", "Living Area 004", "badge:4"], ["row", "Mud Room 116", "badge:0"], ["toast", "✓ 5 photos added to Kitchen 006", "ok"]], sub=""),
 scr("rp", "ok_screen", "Check Screen With The New Photos", "A full screen with a check, the count and the new thumbnails.", ["clear", "friendly", "personal", "direct"],
     [["check", 40], ["big", "5 photos added", 15, "Kitchen 006"], ["thumbs", ["int_modernkitchen"] * 3, 3, 32], ["btn", "Done", "full"]], nohead=True))
nv2add("Feature Options", "rp",
 scr("rp", "ba_slider", "Before And After: Drag A Slider", "One photo, drag the line to compare before and after.", ["tactile", "modern", "natural", "clear"],
     [["slider", "int_midcentury", 118], ["cap", "Drag to compare"]], head="Living Area 004", sub="Before and After"),
 scr("rp", "ba_side", "Before And After: Side By Side", "Two photos next to each other, labeled.", ["clear", "practical", "honest", "calm"],
     [["sbs", "int_midcentury", 110], ["cap", "Same angle, Oct 2026"]], head="Living Area 004", sub="Before and After"))
nv2add("App Icon & Favicon", "rp",
 nv2("icon", "rp", "icon_roof", "Light Grey Tile, Roofline Over RP", "Same family as Home Guide: light grey tile with a thin roof line.", ["architectural", "clear", "personal", "light"],
     shape="square", bg="#EDEDED", fg="#171717", mark="RP", roof=True),
 nv2("icon", "rp", "icon_grid", "White Tile, Black RP, Faint Grid", "White tile, thin black border, Khand initials over a faint grid.", ["minimal", "clear", "technical", "light"],
     shape="square", bg="#fff", fg="#171717", mark="RP", border=True, grid=True), True)
nv2add("From Max Sign-Off", "rp",
 scr("rp", "so_footer", "Footer: Built By Max Weberman, Call Max", "The standard footer line with a small Call Max button.", ["clear", "direct", "personal", "practical"],
     [["row", "Kitchen 006", "badge:8"], ["row", "Living Area 004", "badge:4"], ["row", "Family Suite 002", "badge:6"], ["spacer"], ["small", "Built by Max Weberman"], ["btn", "📞 Call Max"]], sub=""),
 scr("rp", "so_title", "Line Under The Title: Photos From Max", "Under the title: 'Photos from Max, October 2026.' Nothing in the footer.", ["personal", "friendly", "calm", "light"],
     [["row", "Kitchen 006", "badge:8"], ["row", "Living Area 004", "badge:4"], ["row", "Family Suite 002", "badge:6"], ["row", "Bathroom 005", "badge:3"]], sub="Photos from Max, October 2026"), True)
nv2add("Feature Options", "rp",
 scr("rp", "sel_long", "Long-Press A Photo To Select Several", "Press and hold one photo, then tap others to pick them.", ["tactile", "modern", "direct", "practical"],
     [["small", "Hold a photo to select"], ["thumbs", ["int_modernkitchen"] * 6, 3, 38, ["sel", "sel", "unsel", "unsel", "sel", "unsel"]], ["btns", ["Share 3", "Download 3"]]], head="Kitchen 006", sub=""),
 scr("rp", "sel_button", "A Select Button Up Top", "Tap Select, then tap photos. Easy to find, one extra tap.", ["clear", "practical", "calm", "friendly"],
     [["chips", ["Select", "All Photos"], 0], ["thumbs", ["int_modernkitchen"] * 6, 3, 38, ["sel", "sel", "unsel", "unsel", "sel", "unsel"]], ["btns", ["Share 3", "Download 3"]]], head="Kitchen 006", sub=""))
nv2add("Photo Handling", "rp",
 scr("rp", "frame_clean", "Clean Photos, 10px Corners", "True photos, rounded a little, nothing on top.", ["natural", "clear", "calm", "light"],
     [["photo", "int_modernkitchen", 120]], head="Kitchen 006", sub="8 photos"),
 scr("rp", "frame_sticker", "Sticker Frames And Stars", "Candy-striped frames with star and house stickers.", ["playful", "vibrant", "cute", "loud"],
     [["sticker", "int_modernkitchen", 112]], head="Kitchen 006", sub="8 photos"))
nv2add("Share & Sign-Off", "rp",
 scr("rp", "dl_zip", "Download Everything As One File", "One button saves every photo in one zip file, sorted by room.", ["practical", "clear", "direct", "construction"],
     [["spacer"], ["big", "54 photos, 15 rooms", 16, "One zip file · folders by room"], ["btn", "⤓ Download All", "full", "solid"], ["spacer"]], sub=""),
 scr("rp", "dl_each", "Save Photos To The Phone, Room By Room", "Each room has a Save button that puts its photos in the phone's library.", ["friendly", "practical", "calm", "personal"],
     [["row", "Kitchen 006", "chip:Save 8"], ["row", "Living Area 004", "chip:Save 4"], ["row", "Family Suite 002", "chip:Save 6"], ["row", "Bathroom 005", "chip:Save 3"], ["small", "Saves to Photos on this phone."]], sub=""))

nv2add("Empty States", "hg",
 scr("hg", "empty_soon", "Empty Section Says: Max Is Adding This", "Sections without info yet show one line, so they know it's coming.", ["honest", "personal", "clear", "calm"],
     [["row", "Water Heater 1 (Rinnai)", "grey:Ends early Nov"], ["row", "Furnace 1", "›"], ["rowx", "Roof", ["Max is adding this warranty."]], ["row", "Windows", "›"]], head="Warranties", sub=""),
 scr("hg", "empty_hide", "Hide Sections Until They Have Info", "Empty sections don't show at all. The list only has what's ready.", ["minimal", "clear", "direct", "light"],
     [["row", "Water Heater 1 (Rinnai)", "grey:Ends early Nov"], ["row", "Furnace 1", "›"], ["row", "Windows", "›"], ["small", "More warranties appear here as Max adds them."]], head="Warranties", sub=""))
nv2add("Share & Sign-Off", "fq",
 scr("fq", "share_pdf", "After Sending: Save A Copy As A PDF", "The done screen offers a PDF of their answers to keep.", ["practical", "clear", "honest", "construction"],
     [["check", 38], ["big", "Sent to Max.", 15], ["btn", "⤓ Save a Copy (PDF)", "full"], ["small", "19 answers · 15 rooms"]], nohead=True),
 scr("fq", "share_none", "After Sending: Nothing Else To Do", "The done screen just closes. Max has the answers.", ["minimal", "calm", "direct", "clear"],
     [["spacer"], ["check", 44], ["big", "Sent to Max.", 16, "That's it. You're done."], ["spacer"]], nohead=True))
nv2add("Onboarding First Screen", "sw",
 scr("sw", "onb_intro", "Short Intro: 7 Stops, About 30 Minutes", "One screen with the stop count, the time, and Start the Walk.", ["clear", "friendly", "practical", "personal"],
     [["spacer"], ["q", "Moschouris Site Walk", 18], ["txt", "7 stops, Basement to Exterior. About 30 minutes. Bring your phone charged.", 10.5], ["btn", "Start the Walk", "", "solid"], ["spacer"]], nohead=True),
 scr("sw", "onb_straight", "Straight Into Stop 1", "No intro. The app opens on Stop 1 with the first item.", ["direct", "minimal", "practical", "clear"],
     [["progress", 1, 7, "Stop 1"], ["q", "Basement Mechanical Room", 13], ["row", "Water Filter System", "box"], ["row", "Sump Pump 1 (Check)", "box"], ["row", "ERV System", "box"], ["row", "Furnace 1 Humidifier", "box"]], sub=""))

# --- Swipe Controls: inside the lean (earthy, outline until pressed, edge arrows); stamp retest ---
SC_PAL["earth4s"] = ["#6E97A4", "#86A27A", "#C98270", "#BF9767"]   # the same earthy four, one step softer
def ctl3(i, label, desc, tags, fmt, pal="earth4", hint="edges", stampov="word", press="fill", style="outline", bg="#FAF3EB"):
    o = ctl(i, label, desc, tags, fmt, "tblt", pal, style, bg)
    o["visual"].update({"hint": hint, "stampov": stampov, "press": press})
    return o
NV2_SC = [
 (ctl3("sc_nv2_stamp_word", "Stamp: THIS Or THAT In Khand Caps", "Round outline buttons and edge arrows. Swiping shows a tilted word stamp.", ["clear", "craft", "construction", "natural"], "round", stampov="word"),
  ctl3("sc_nv2_stamp_icon", "Stamp: Round Check Over The Word", "Same buttons. Swiping shows a round stamp with a check over the word.", ["clear", "friendly", "natural", "craft"], "round", stampov="icon")),
 (ctl3("sc_nv2_round_press", "Round Outline Buttons, Fill On Press", "Earthy circles with icons and small words under them.", ["light", "natural", "tactile", "clear"], "round"),
  ctl3("sc_nv2_pill_press", "Pill Outline Buttons, Fill On Press", "Earthy pills with the words inside.", ["light", "natural", "clear", "friendly"], "pill")),
 (ctl3("sc_nv2_tone_deep", "Earthy Tones, As They Are", "Dusty lagoon, moss, clay and ochre at full depth.", ["natural", "clear", "warm", "light"], "pill"),
  ctl3("sc_nv2_tone_soft", "Earthy Tones, One Step Softer", "The same four colors, a little lighter and quieter.", ["soft", "light", "natural", "calm"], "pill", pal="earth4s")),
]
for _a, _b in NV2_SC: POOL[SWIPE_CONTROLS].extend([_a, _b])
for _cat, _app, _a, _b, _r in NV2:
    POOL.setdefault(_cat, []).extend([_a, _b])
    CATEGORY_WEIGHT.setdefault(_cat, 1.0)
    GROUP_OF.setdefault(_cat, _cat)
NV_ASK.update({"Layout": "Which Works Better For {app}?", "Question Context": "Which Works Better For {app}?", "Error States": "Which Is Sharper For {app}?",
               "Success & Confirmation": "Which Is Sharper For {app}?", "Onboarding First Screen": "Which Is Sharper For {app}?"})


# Categories whose pairs must contrast on a tag: one option carries tag X, the other tag Y.
PAIR_RULES = {"Bangkok Vs Japan Aesthetics": ("bangkok", "japan")}

# ---------------------------------------------------------------------------
def deck_options(deck):
    """Every option in a deck, for both formats: v2 pairs (optionA/optionB) and v3 single cards (option)."""
    for p in deck.get("pairs", []):
        for o in ("optionA", "optionB"):
            if o in p: yield p[o]
    for c in deck.get("cards", []):
        if "option" in c: yield c["option"]

# ---- English-only rule (Max, Oct 10, 2026) ------------------------------------------------------
# The brand is English only for now. Options that show Thai or Japanese script, bilingual wordmarks or
# copy, EN/TH layouts or language toggles are never put in a deck. Place-based looks (Bangkok, Japan,
# Isan...) are fine when their text is English.
import re as _re_lang
_SCRIPT_RX = _re_lang.compile("[\u0E00-\u0E7F\u3040-\u30FF\u3400-\u9FFF\uFF66-\uFF9F]")
_LANG_TEXT_RX = _re_lang.compile(r"EN\s*/\s*TH|TH\s*/\s*EN|EN\s*\|\s*TH|bilingual|two languages|three languages|language toggle|lang(uage)? switch", _re_lang.I)
NON_ENGLISH_TAGS = {"bilingual", "thai-script", "japanese-script", "multilingual"}
IGNORED_TAGS = {"bilingual", "thai", "thai-script", "japanese-script", "multilingual"}   # history kept, no longer scored

def non_english_reasons(opt):
    """Why an option breaks the English-only rule ([] if it is fine)."""
    blob = json.dumps(opt, ensure_ascii=False); v = opt.get("visual", {}); why = []
    if _SCRIPT_RX.search(blob): why.append("Thai/Japanese script")
    if NON_ENGLISH_TAGS & set(opt.get("tags", [])): why.append("bilingual tag")
    if v.get("type") == "thaitype" or "bilingual" in (v.get("layout"), v.get("shape"), v.get("style")): why.append("bilingual/Thai layout")
    if _LANG_TEXT_RX.search(blob): why.append("bilingual copy or language toggle")
    return why

def english_only(opt): return not non_english_reasons(opt)

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
    if tag in IGNORED_TAGS: return 0.0, 0.0   # English-only: 'bilingual' is no longer a direction
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

def allocate(profile, total, caps, focus=None):
    """Split `total` pairs across categories by weight x uncertainty (x focus boost), never exceeding caps[cat]."""
    focus = focus or {}
    raw = {c: CATEGORY_WEIGHT.get(c, 0.8) * focus.get(c, 1.0) * (0.5 + category_uncertainty(profile, c)) for c in POOL}
    alloc = {c: 0 for c in POOL}
    total = min(total, sum(caps.values()))
    for c in sorted(POOL, key=lambda c: -raw[c]):      # everyone with room gets at least 1
        if sum(alloc.values()) < total and caps[c] > 0: alloc[c] = 1
    while sum(alloc.values()) < total:                  # then fill by largest deficit vs. ideal share
        s = sum(raw[c] for c in POOL if alloc[c] < caps[c])
        c = max((c for c in POOL if alloc[c] < caps[c]), key=lambda c: total * raw[c] / s - alloc[c])
        alloc[c] += 1
    return alloc

def allocate_mixed(profile, total, caps, focus, focus_share, max_per, rng):
    """Variety mode: ~focus_share of pairs from focus categories, the rest spread over everything else.
    No category gets more than max_per pairs. Weights get a little jitter so decks differ day to day."""
    focus = focus or {}
    capm = {c: min(caps[c], max_per) for c in POOL}
    alloc = {c: 0 for c in POOL}
    w = {c: CATEGORY_WEIGHT.get(c, 0.8) * (0.5 + category_uncertainty(profile, c)) * (0.75 + 0.5 * rng.random()) for c in POOL}
    def fill(cats, n):
        cats = [c for c in cats if capm[c] > alloc[c]]
        start = sum(alloc[c] for c in cats)
        while n > 0 and cats:
            room = [c for c in cats if alloc[c] < capm[c]]
            if not room: break
            sw = sum(w[c] for c in room)
            target = start + n
            c = max(room, key=lambda c: target * w[c] / sw - alloc[c])
            alloc[c] += 1; n -= 1
        return n
    fcats = [c for c in POOL if c in focus]
    ocats = [c for c in POOL if c not in focus]
    nf = round(total * focus_share) if fcats else 0
    left = fill(fcats, nf)
    left = fill(ocats, total - nf + left)
    if left: fill(fcats, left)        # variety pool ran dry: hand the rest back to focus
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
        for o in deck_options(load_json(p, {})):
            out.setdefault(o["id"], set()).add(date)
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

def swipe_controls_unclear(profile, min_answered=16, max_uncertainty=0.35):
    """Keep 2-4 Swipe Controls pairs in every deck until Max has answered enough of them and the
    category's tags show a clear lean."""
    st = profile.get("categories", {}).get(SWIPE_CONTROLS, {})
    return st.get("answered", 0) < min_answered or category_uncertainty(profile, SWIPE_CONTROLS) > max_uncertainty

def is_check(profile, opt, threshold=-0.35):
    """An option that carries a tag Max has clearly rejected (used sparingly as a re-test)."""
    return any(tag_pref(profile, t)[0] <= threshold for t in opt["tags"])

def build_deck(date, n_pairs, seed=None, allow_repeats=False, focus=None, focus_note=None, check_share=0.12,
               max_per=None, focus_share=None):
    rng = random.Random(seed if seed is not None else date)
    profile = load_json(PROFILE, empty_profile())
    # Most pairs refine inside the liked space; only a small budget re-tests disliked directions,
    # always as disliked-vs-liked (never two disliked options against each other).
    check_budget = [max(2, round(n_pairs * check_share))]
    seen = seen_pairs(exclude_date=date)
    shown = shown_options(exclude_date=date)
    avail = {c: [o for o in opts if o["id"] not in shown and english_only(o)] for c, opts in POOL.items()}
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
    mixed = max_per is not None
    if mixed:
        alloc = allocate_mixed(profile, n_pairs, caps, focus, focus_share if focus_share is not None else 0.3, max_per, rng)
    else:
        alloc = allocate(profile, n_pairs, caps, focus)
    sc = SWIPE_CONTROLS
    if swipe_controls_unclear(profile) and caps.get(sc, 0) >= 2:
        want = min(caps[sc], max(2, min(4, alloc.get(sc, 0) or 3)))
        alloc[sc] = alloc.get(sc, 0)
        while alloc[sc] < want:       # take slots from the biggest other categories
            big = max((c for c in alloc if c != sc and alloc[c] > 0), key=lambda c: alloc[c])
            alloc[big] -= 1; alloc[sc] += 1
        while alloc[sc] > 4:
            small = min((c for c in POOL if c != sc and caps[c] > alloc.get(c, 0)), key=lambda c: alloc.get(c, 0))
            alloc[sc] -= 1; alloc[small] = alloc.get(small, 0) + 1
    pairs = []
    def pick(cat, opts, k, used):
        cands = list(itertools.combinations(opts, 2))
        if cat in PAIR_RULES:
            x, y = PAIR_RULES[cat]
            cands = [(a, b) for a, b in cands if (x in a["tags"] and y in b["tags"]) or (y in a["tags"] and x in b["tags"])]
        cands = [ab for ab in cands if pair_key(ab[0]["id"], ab[1]["id"]) not in seen]
        def score(ab):
            checks = is_check(profile, ab[0]) + is_check(profile, ab[1])
            return pair_priority(profile, ab[0], ab[1], rng) + (1.0 if checks == 0 else 0.0)
        cands.sort(key=lambda ab: -score(ab))
        chosen = []
        for a, b in cands:                     # each option at most once per deck
            if len(chosen) >= k: break
            if a["id"] in used or b["id"] in used: continue
            checks = is_check(profile, a) + is_check(profile, b)
            if checks == 2: continue
            if checks == 1:
                if check_budget[0] <= 0: continue
                check_budget[0] -= 1
            chosen.append((a, b)); used.update((a["id"], b["id"]))
        return chosen
    used = set()
    if mixed:
        def has_both(c):
            return any(is_check(profile, o) for o in avail[c]) and any(not is_check(profile, o) for o in avail[c])
        slots = [c for c in alloc for _ in range(alloc[c])]
        rng.shuffle(slots)
        n_chk = round(n_pairs * check_share)
        k_chk = {c: 0 for c in alloc}
        for c in slots:
            if n_chk <= 0: break
            if has_both(c) and k_chk[c] < alloc[c] and k_chk[c] < 2:
                k_chk[c] += 1; n_chk -= 1
        def pick_quota(cat, k_ref, k_ck):
            opts = avail[cat]
            cands = [ab for ab in itertools.combinations(opts, 2) if pair_key(ab[0]["id"], ab[1]["id"]) not in seen]
            if cat in PAIR_RULES:
                x, y = PAIR_RULES[cat]
                cands = [(a, b) for a, b in cands if (x in a["tags"] and y in b["tags"]) or (y in a["tags"] and x in b["tags"])]
            cands.sort(key=lambda ab: -pair_priority(profile, ab[0], ab[1], rng))
            out, need = [], k_ref + k_ck
            # phases: fill the check quota, then the refine quota, then any shortfall (refine first)
            for phase in ("check", "refine", "extra-refine", "extra-check"):
                for a, b in cands:
                    if len(out) >= need: break
                    if a["id"] in used or b["id"] in used: continue
                    ck = is_check(profile, a) + is_check(profile, b)
                    if ck == 2: continue
                    if phase == "check" and not (ck == 1 and k_ck > 0): continue
                    if phase == "refine" and not (ck == 0 and k_ref > 0): continue
                    if phase == "extra-refine" and ck != 0: continue
                    if phase == "extra-check" and ck != 1: continue
                    out.append((a, b, "check" if ck else "refine")); used.update((a["id"], b["id"]))
                    if phase == "check": k_ck -= 1
                    if phase == "refine": k_ref -= 1
            return out
        for cat in [c for c in alloc if alloc[c]]:
            for a, b, purpose in pick_quota(cat, alloc[cat] - k_chk[cat], k_chk[cat]):
                if rng.random() < 0.5: a, b = b, a
                pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": False, "purpose": purpose})
        for c in alloc: alloc[c] = sum(p["category"] == c for p in pairs)
        # top up any shortfall from categories that still have room under the cap
        for _ in range(3):
            if len(pairs) >= n_pairs: break
            for cat in sorted(POOL, key=lambda c: (c in (focus or {}), alloc[c])):   # variety first, emptiest first
                if len(pairs) >= n_pairs: break
                if alloc[cat] >= max_per: continue
                n_ck = sum(p["purpose"] == "check" for p in pairs)
                want_ck = 1 if n_ck < round(n_pairs * check_share) else 0
                for a, b, purpose in pick_quota(cat, 1 - want_ck, want_ck):
                    if rng.random() < 0.5: a, b = b, a
                    pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": False, "purpose": purpose})
                    alloc[cat] += 1
    order = [] if mixed else [c for c in alloc if alloc[c]]
    rng.shuffle(order)
    for cat in order:
        k = alloc[cat]
        got = pick(cat, avail[cat], k, used)
        if len(got) < k:   # not enough refine-able pairs here; re-offer the shortfall to other categories
            alloc[cat] = len(got)
        for a, b in got:
            if rng.random() < 0.5: a, b = b, a
            purpose = "check" if (is_check(profile, a) or is_check(profile, b)) else "refine"
            pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": False, "purpose": purpose})
    for cat in sorted(order, key=lambda c: -(focus or {}).get(c, 1.0)):   # top up any shortfall
        need = n_pairs - len(pairs)
        if need <= 0: break
        for a, b in pick(cat, avail[cat], need, used):
            alloc[cat] += 1
            purpose = "check" if (is_check(profile, a) or is_check(profile, b)) else "refine"
            pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": False, "purpose": purpose})
    if allow_repeats and len(pairs) < n_pairs:     # explicit opt-in only
        for cat in sorted(POOL, key=lambda c: -CATEGORY_WEIGHT.get(c, 0.8)):
            need = n_pairs - len(pairs)
            if need <= 0: break
            for a, b in pick(cat, [o for o in POOL[cat] if english_only(o)], min(need, 2), used):
                pairs.append({"category": cat, "optionA": a, "optionB": b, "repeat": True})
    rng.shuffle(pairs)
    if mixed:   # greedy order: never the same category twice in a row, and avoid the same family back-to-back
        rest, seq = pairs[:], []
        while rest:
            last = seq[-1]["category"] if seq else None
            lg = GROUP_OF.get(last, last)
            nxt = (next((p for p in rest if p["category"] != last and GROUP_OF.get(p["category"], p["category"]) != lg), None)
                   or next((p for p in rest if p["category"] != last), None) or rest[0])
            rest.remove(nxt); seq.append(nxt)
        pairs = seq
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
            "focus": {"categories": sorted(focus or {}), "note": focus_note or ""},
            "pair_mix": {"refine": sum(p.get("purpose") == "refine" for p in pairs), "check": sum(p.get("purpose") == "check" for p in pairs)},
            "freshness": {"option_slots": len(opt_ids), "never_shown_before": fresh,
                          "share": round(fresh / max(1, len(opt_ids)), 3)},
            "warnings": warnings, "pairs": pairs,
            "image_credits": load_json(CREDITS, {})}

def order_cards(cards):
    """Greedy order: never the same category twice in a row, avoid the same family back-to-back."""
    rest, seq = cards[:], []
    while rest:
        last = seq[-1]["category"] if seq else None
        lg = GROUP_OF.get(last, last)
        nxt = (next((c for c in rest if c["category"] != last and GROUP_OF.get(c["category"], c["category"]) != lg), None)
               or next((c for c in rest if c["category"] != last), None) or rest[0])
        rest.remove(nxt); seq.append(nxt)
    return seq

def build_single_deck(date, n_cards, seed=None, allow_repeats=False, focus=None, focus_note=None, check_share=0.24,
                      max_per=None, focus_share=None):
    """v3 deck: n_cards single-option cards (answer No / Maybe / Love / Yes).
    Reuses the pair selector (same rules: unseen only, variety mix, focus share, refine vs check),
    asking for n_cards/2 pairs and splitting each pair into two cards. In a check pair one option is
    'check' (likely disliked) and the other 'refine' (likely liked); max_per counts cards."""
    pd = build_deck(date, (n_cards + 1) // 2, seed, allow_repeats, focus, focus_note, check_share,
                    None if max_per is None else max(1, max_per // 2), focus_share)
    profile = load_json(PROFILE, empty_profile())
    rng = random.Random(f"{seed if seed is not None else date}-cards")
    cards = []
    for p in pd["pairs"]:
        for o in (p["optionA"], p["optionB"]):
            cards.append({"category": p["category"], "option": o, "repeat": p.get("repeat", False),
                          "purpose": "check" if is_check(profile, o) else "refine"})
    rng.shuffle(cards)
    cards = [{"id": f"{date}-{i:02d}", **c} for i, c in enumerate(order_cards(cards)[:n_cards], 1)]
    shown = shown_options(exclude_date=date)
    fresh = sum(c["option"]["id"] not in shown for c in cards)
    alloc = {}
    for c in cards: alloc[c["category"]] = alloc.get(c["category"], 0) + 1
    deck = {k: v for k, v in pd.items() if k not in ("pairs", "pair_mix", "allocation", "freshness")}
    deck.update({"version": 3, "format": "single", "deck_size": len(cards),
                 "answers": {"love": 2, "yes": 1, "maybe": 0, "no": -1},
                 "allocation": alloc,
                 "card_mix": {"refine": sum(c["purpose"] == "refine" for c in cards), "check": sum(c["purpose"] == "check" for c in cards)},
                 "freshness": {"option_slots": len(cards), "never_shown_before": fresh, "share": round(fresh / max(1, len(cards)), 3)},
                 "cards": cards, "image_credits": pd["image_credits"]})
    return deck

def convert_pair_deck(src_id, new_id, n_cards=25):
    """Turn an existing pair deck into a single-card deck. The deck keeps ALL of the source options
    as a reserve (A sides first, then B sides, same order); the app drops options from pairs Max
    already answered in the source deck on that device and shows the first n_cards of the rest."""
    src = load_json(os.path.join(DECKS, f"{src_id}.json"), None)
    if not src or "pairs" not in src: sys.exit(f"No pair deck {src_id}")
    profile = load_json(PROFILE, empty_profile())
    cards = []
    for side in ("optionA", "optionB"):
        for p in src["pairs"]:
            o = p[side]
            cards.append({"id": f"{new_id}-{len(cards)+1:03d}", "category": p["category"], "option": o,
                          "source_pair": p["id"], "purpose": "check" if is_check(profile, o) else "refine"})
    deck = {k: v for k, v in src.items() if k not in ("pairs", "pair_mix", "freshness")}
    deck.update({"date": new_id, "version": 3, "format": "single", "deck_size": n_cards, "source_deck": src_id,
                 "converted_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                 "note": f"Single-card version of {src_id}. {n_cards} cards shown, drawn from the {len(cards)} source options, skipping pairs already answered in {src_id}.",
                 "answers": {"love": 2, "yes": 1, "maybe": 0, "no": -1},
                 "card_mix_first_n": {"refine": sum(c["purpose"] == "refine" for c in cards[:n_cards]), "check": sum(c["purpose"] == "check" for c in cards[:n_cards])},
                 "cards": cards})
    return deck

SC_POLISH_PAIRS = [("sc_round_outline", "sc_round_haptic"), ("sc_gesture_tbt", "sc_slider_tbt"), ("sc_stamp_brand", "sc_square_khand"),
                   ("sc_pill_brand", "sc_seg_brand"), ("sc_rail_mono", "sc_pill_earth")]

def build_polish_deck(date, seed=None):
    """Polish deck: 95 this-or-that pairs of polish choices for Max's real apps (PZ) + 5 Swipe Controls pairs.
    Every pair is labelled with the app it applies to. All options must be unseen and English-only."""
    rng = random.Random(seed if seed is not None else date)
    profile = load_json(PROFILE, empty_profile())
    shown = shown_options(exclude_date=date)
    sc = {o["id"]: o for o in POOL[SWIPE_CONTROLS]}
    pairs = []
    for cat, lst in PZ.items():
        for app, a, b in lst:
            if rng.random() < 0.5: a, b = b, a
            pairs.append({"category": cat, "app": APPS[app]["name"], "optionA": a, "optionB": b})
    for x, y in SC_POLISH_PAIRS:
        a, b = sc[x], sc[y]
        if rng.random() < 0.5: a, b = b, a
        pairs.append({"category": SWIPE_CONTROLS, "app": "All Swipe Apps", "optionA": a, "optionB": b})
    for p in pairs:
        for o in (p["optionA"], p["optionB"]):
            assert o["id"] not in shown, f"{o['id']} already shown"
            assert english_only(o), f"{o['id']} is not English-only"
        p["repeat"] = False
        p["purpose"] = "check" if (is_check(profile, p["optionA"]) or is_check(profile, p["optionB"])) else "refine"
    rng.shuffle(pairs)
    # spread: never the same category or the same app back to back; Swipe Controls spaced out
    rest, seq = pairs[:], []
    while rest:
        last = seq[-1] if seq else {"category": None, "app": None}
        since_sc = next((i for i, q in enumerate(reversed(seq)) if q["category"] == SWIPE_CONTROLS), 99)
        ok = lambda q: q["category"] != last["category"] and q["app"] != last["app"] and (q["category"] != SWIPE_CONTROLS or since_sc >= 14)
        nxt = next((q for q in rest if ok(q)), None) or next((q for q in rest if q["category"] != last["category"]), None) or rest[0]
        rest.remove(nxt); seq.append(nxt)
    pairs = [{"id": f"{date}-{i:03d}", **p} for i, p in enumerate(seq, 1)]
    alloc = {}
    for p in pairs: alloc[p["category"]] = alloc.get(p["category"], 0) + 1
    apps = {}
    for p in pairs: apps[p["app"]] = apps.get(p["app"], 0) + 1
    ids = [p[o]["id"] for p in pairs for o in ("optionA", "optionB")]
    return {"date": date, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True,
            "title": "Polish Picks For Max's Apps",
            "brands": ["maxweberman.com base: Khand/Hind, black/white/grey + terracotta, lagoon, jungle"],
            "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "allocation": alloc, "apps": apps,
            "focus": {"categories": sorted(PZ), "note": "Polish deck: choices that make Max's shareable apps look sharp, mocked with each app's real name and content."},
            "pair_mix": {"refine": sum(p["purpose"] == "refine" for p in pairs), "check": sum(p["purpose"] == "check" for p in pairs)},
            "freshness": {"option_slots": len(ids), "never_shown_before": sum(i not in shown for i in ids), "share": 1.0},
            "warnings": [], "pairs": pairs, "image_credits": load_json(CREDITS, {})}

def build_nv_deck(date, seed=None, nvlist=None, sclist=None, title="Niko And Vivian's Apps: Look And Function", note=None):
    """Niko & Vivian deck (first built 2026-10-11b): 45 hand-paired visual + functional choices for Home Guide,
    Finish Questions, Site Walk and Room Photos (incl. app-polish-spec retests), 1 SiteAgent share-card retest
    and 4 Swipe Controls pairs. Every option must be unseen, English-only and light-mode."""
    rng = random.Random(seed if seed is not None else date)
    profile = load_json(PROFILE, empty_profile())
    shown = shown_options(exclude_date=date)
    pairs = []
    for item in (nvlist if nvlist is not None else NV):
        cat, app, a, b = item[:4]
        rt = item[4] if len(item) > 4 else cat in NV_RETEST
        if rng.random() < 0.5: a, b = b, a
        nm = NVAPPS[app]["name"]
        pairs.append({"category": cat, "app": nm, "ask": NV_ASK.get(cat, "Which Is Sharper For {app}?").format(app=nm),
                      "retest": rt, "optionA": a, "optionB": b})
    for a, b in (sclist if sclist is not None else NV_SC):
        if rng.random() < 0.5: a, b = b, a
        pairs.append({"category": SWIPE_CONTROLS, "app": "All Swipe Apps", "ask": "Which Swipe Controls Feel More Like You?",
                      "retest": False, "optionA": a, "optionB": b})
    seen_ids = set()
    for p in pairs:
        for o in (p["optionA"], p["optionB"]):
            assert o["id"] not in shown, f"{o['id']} already shown"
            assert o["id"] not in seen_ids, f"{o['id']} twice in this deck"
            assert english_only(o), f"{o['id']} is not English-only: {non_english_reasons(o)}"
            seen_ids.add(o["id"])
        p["repeat"] = False
        ck = is_check(profile, p["optionA"]) + is_check(profile, p["optionB"])
        assert ck < 2, f"two disliked options in one pair: {p['optionA']['id']} / {p['optionB']['id']}"
        p["purpose"] = "check" if ck else "refine"
    rng.shuffle(pairs)
    rest, seq = pairs[:], []
    while rest:   # never the same category or app back to back; Swipe Controls spaced out
        last = seq[-1] if seq else {"category": None, "app": None}
        since_sc = next((i for i, q in enumerate(reversed(seq)) if q["category"] == SWIPE_CONTROLS), 99)
        since_ck = next((i for i, q in enumerate(reversed(seq)) if q["purpose"] == "check"), 99)
        ok = lambda q: (q["category"] != last["category"] and q["app"] != last["app"]
                        and (q["category"] != SWIPE_CONTROLS or since_sc >= 10) and (q["purpose"] != "check" or since_ck >= 3))
        nxt = (next((q for q in rest if ok(q)), None) or next((q for q in rest if q["category"] != last["category"] and q["app"] != last["app"]), None)
               or next((q for q in rest if q["category"] != last["category"]), None) or rest[0])
        rest.remove(nxt); seq.append(nxt)
    pairs = [{"id": f"{date}-{i:02d}", **p} for i, p in enumerate(seq, 1)]
    alloc, apps = {}, {}
    for p in pairs:
        alloc[p["category"]] = alloc.get(p["category"], 0) + 1
        apps[p["app"]] = apps.get(p["app"], 0) + 1
    ids = [p[o]["id"] for p in pairs for o in ("optionA", "optionB")]
    return {"date": date, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True,
            "title": title,
            "brands": ["maxweberman.com base: Khand/Hind, black/white/grey + terracotta, lagoon, jungle"],
            "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "allocation": alloc, "apps": apps,
            "focus": {"categories": sorted({c for c, *_ in (nvlist if nvlist is not None else NV)}), "note": note or "Standing focus (from Oct 11, 2026): visual and functional choices for Niko and Vivian's apps (Home Guide, Finish Questions, Site Walk, Room Photos), mocked with each app's real rooms, questions and checklist items; plus app-polish-spec retests and Swipe Controls."},
            "retests": sorted({p["category"] for p in pairs if p["retest"]}),
            "pair_mix": {"refine": sum(p["purpose"] == "refine" for p in pairs), "check": sum(p["purpose"] == "check" for p in pairs)},
            "freshness": {"option_slots": len(ids), "never_shown_before": sum(i not in shown for i in ids), "share": round(sum(i not in shown for i in ids) / len(ids), 3)},
            "warnings": [], "pairs": pairs, "image_credits": load_json(CREDITS, {})}

NV2_NOTE = ("Niko and Vivian's apps, round 2 (Oct 12, 2026): retests of the 10 pairs skipped in 2026-10-11b as sharper options, the app-polish-spec retests "
            "(icon, imagery, share copy, sign-off, transitions, SiteAgent share card), and new function choices: warranties, shutoffs, who to call, task tracking, "
            "install card, password, edit after sending, reminders, resume, problem flags, photo viewer, before and after, uploads, select and download. Plus 3 Swipe Controls pairs.")
POLISH_SETS = {"2026-10-10g": lambda date, seed: build_polish_deck(date, seed), "nv": lambda date, seed: build_nv_deck(date, seed),
               "nv2": lambda date, seed: build_nv_deck(date, seed, NV2, NV2_SC, "Niko And Vivian's Apps, Round 2: Look And Function", NV2_NOTE)}
def polish_set_unseen(name, date):
    shown = shown_options(exclude_date=date)
    if name == "nv": ids = [o["id"] for _, _, a, b in NV for o in (a, b)] + [o["id"] for a, b in NV_SC for o in (a, b)]
    elif name == "nv2": ids = [o["id"] for _, _, a, b, _ in NV2 for o in (a, b)] + [o["id"] for a, b in NV2_SC for o in (a, b)]
    else: ids = [o["id"] for lst in PZ.values() for _, a, b in lst for o in (a, b)]
    return not any(i in shown for i in ids)

SINGLE_SCORE = {"love": 2, "yes": 1, "maybe": 0, "no": -1}

# ---------------------------------------------------------------------------
NOTES = os.path.join(ROOT, "results", "notes.json")   # private (results/ is gitignored); never published

def save_notes(res):
    """Notes on Votes: store every note from a results export in results/notes.json and print the new or changed ones."""
    deck = res.get("deck") or "?"
    found = list(res.get("notes") or [])
    seen_ids = {n.get("pair_id") or n.get("card_id") for n in found}
    for p in res.get("picks", []):                      # older exports: notes only inside picks
        pid = p.get("pair_id") or p.get("card_id")
        if p.get("note") and pid not in seen_ids:
            lab = p.get("label") or f"{p.get('labelA')} vs {p.get('labelB')}"
            found.append({"pair_id" if "pair_id" in p else "card_id": pid, "category": p.get("category"), "label": lab,
                          "answer": p.get("choice") or p.get("answer"), "note": p["note"], "at": p.get("at")})
    if not found:
        print("Notes: none in this export."); return
    os.makedirs(os.path.dirname(NOTES), exist_ok=True)
    store = load_json(NOTES, {"note": "Private Style Swipe vote notes from Max. Not published.", "decks": {}})
    d = store.setdefault("decks", {}).setdefault(deck, {})
    new = []
    for n in found:
        key = n.get("pair_id") or n.get("card_id")
        if d.get(key, {}).get("note") != n.get("note"): new.append(n)
        d[key] = {k: v for k, v in n.items() if v is not None}
    store["updated"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(NOTES, "w") as f: json.dump(store, f, indent=1, ensure_ascii=False)
    print(f"Notes: {len(found)} in export, {len(new)} new or changed (saved to {NOTES}).")
    for n in new:
        print(f"  NOTE [{deck} {n.get('pair_id') or n.get('card_id')}] {n.get('category')}: {n.get('label')} -> {n.get('answer')}\n    \"{n.get('note')}\"")

def parse_results_text(txt):
    """Results from the app: a plain JSON export, or shared text (summary line, then the JSON, then maybe a URL)."""
    txt = txt.strip()
    try: return json.loads(txt)
    except ValueError: pass
    dec = json.JSONDecoder()
    for i, ch in enumerate(txt):
        if ch != "{": continue
        try:
            obj, _ = dec.raw_decode(txt[i:])
        except ValueError: continue
        if isinstance(obj, dict) and "picks" in obj: return obj
    return None

def enrich_compact(res):
    """Shared (compact) results carry only ids, choice/answer and note; fill labels, option ids, tags and
    category from the deck file so the rest of ingest works unchanged."""
    deck = load_json(os.path.join(DECKS, f"{res.get('deck')}.json"), None)
    if not deck: return res
    pairs = {p["id"]: p for p in deck.get("pairs", [])}
    cards = {c["id"]: c for c in deck.get("cards", [])}
    for p in res.get("picks", []):
        if "pair_id" in p and p["pair_id"] in pairs and "optionA" not in p:
            d = pairs[p["pair_id"]]; A, B = d["optionA"], d["optionB"]
            p.update({"category": d["category"], "optionA": A["id"], "optionB": B["id"], "labelA": A.get("label"),
                      "labelB": B.get("label"), "tagsA": A.get("tags", []), "tagsB": B.get("tags", [])})
        elif "card_id" in p and p["card_id"] in cards and "option_id" not in p:
            c = cards[p["card_id"]]; o = c["option"]
            p.update({"category": c["category"], "option_id": o["id"], "label": o.get("label"), "tags": o.get("tags", [])})
    return res

def ingest(results_path):
    try: res = parse_results_text(open(results_path, encoding="utf-8").read())
    except OSError: res = None
    if not res: sys.exit(f"Could not read results JSON: {results_path}")
    res = enrich_compact(res)
    profile = load_json(PROFILE, empty_profile())
    deck_date = res.get("deck")
    save_notes(res)
    if deck_date in profile["decks_ingested"]:
        print(f"Deck {deck_date} already ingested; skipping (delete it from profile.decks_ingested to redo).")
        return
    def bump(d, key, field, amt=1):
        if d is profile["tags"] and key in IGNORED_TAGS: return   # English-only: stop scoring these
        d.setdefault(key, {}).setdefault(field, 0); d[key][field] += amt
    for p in res.get("picks", []):
        if "answer" in p:          # v3 single-card pick: Love +2, Yes +1, Maybe 0 (still shown), No -1
            ans, cat = p.get("answer"), p.get("category")
            if ans not in SINGLE_SCORE: continue
            sc, oid, tags = SINGLE_SCORE[ans], p.get("option_id"), set(p.get("tags", []))
            bump(profile["categories"], cat, "answered"); bump(profile["categories"], cat, ans)
            bump(profile["options"], oid, "shown")
            for t in tags: bump(profile["tags"], t, "shown")
            if sc > 0:
                bump(profile["options"], oid, "wins", sc)
                for t in tags: bump(profile["tags"], t, "wins", sc)
            elif sc < 0:
                bump(profile["options"], oid, "losses", -sc)
                for t in tags: bump(profile["tags"], t, "losses", -sc)
            if ans == "love": bump(profile["options"], oid, "loves")
            continue
        choice, cat = p.get("choice"), p.get("category")
        if choice == "skip": continue
        if res.get("version", 1) >= 4 and choice in ("both", "loveA", "loveB", "neither"):
            # v4 pairs: Both +1 each, Love +2 to the loved option (the other counts as a normal loss), Neither -1 each
            bump(profile["categories"], cat, "answered"); bump(profile["categories"], cat, choice)
            sides = {"A": (p.get("optionA"), set(p.get("tagsA", []))), "B": (p.get("optionB"), set(p.get("tagsB", [])))}
            for oid, tags in sides.values():
                bump(profile["options"], oid, "shown")
                for t in tags: bump(profile["tags"], t, "shown")
            def give(side, amt):
                oid, tags = sides[side]
                field = "wins" if amt > 0 else "losses"
                bump(profile["options"], oid, field, abs(amt))
                for t in tags: bump(profile["tags"], t, field, abs(amt))
            if choice == "both": give("A", 1); give("B", 1)
            elif choice == "neither": give("A", -1); give("B", -1)
            else:
                win = choice[-1]; lose = "B" if win == "A" else "A"
                give(win, 2); bump(profile["options"], sides[win][0], "loves")
                bump(profile["options"], sides[lose][0], "losses")
                for t in sides[lose][1] - sides[win][1]: bump(profile["tags"], t, "losses")
            continue
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
    ranked = sorted(((t, v) for t, v in profile["tags"].items() if t not in IGNORED_TAGS), key=lambda kv: -(kv[1].get("wins", 0) - kv[1].get("losses", 0)))
    profile["top_tags"] = [t for t, _ in ranked[:12]]
    profile["bottom_tags"] = [t for t, _ in ranked[-8:]]
    with open(PROFILE, "w") as f: json.dump(profile, f, indent=1)
    print(f"Ingested {len(res.get('picks', []))} picks from deck {deck_date}. Top tags: {', '.join(profile['top_tags'][:8])}")

# ---------------------------------------------------------------------------
def inline_images(deck):
    """Return a copy of the deck with image keys mapped to small data URIs (for a self-contained HTML)."""
    imgs = {}
    keys = set()
    for o in deck_options(deck):
        v = o["visual"]; keys |= {v.get("key"), (v.get("p") or {}).get("key"), (v.get("c") or {}).get("img")}
        keys |= set((v.get("p") or {}).get("keys") or [])
        if v.get("type") == "polish" and (v.get("p") or {}).get("layout") == "collage": keys |= {"gd_japanese", "int_japandi", "gd_cottage", "int_cabin"}
    keys -= {None}
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

def inline_audio(deck):
    """Render (or reuse) a real MP3 clip for every sound option in the deck; return {option_id: data URI}."""
    out = {}
    try:
        import audio_synth
    except Exception as e:
        print("WARNING: audio clips not generated:", e); return out
    for o in deck_options(deck):
        if o["visual"].get("type") == "sound":
            path = audio_synth.render(o)
            out[o["id"]] = "data:audio/mpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()
    return out

def render_index(deck):
    if not os.path.exists(TEMPLATE):
        print("No index.template.html; skipping HTML render."); return
    html = open(TEMPLATE).read()
    payload = json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")
    imgs = json.dumps(inline_images(deck)).replace("</", "<\\/")
    auds = json.dumps(inline_audio(deck))
    html = html.replace("/*__DECK_JSON__*/null", payload).replace("/*__IMAGES_JSON__*/{}", imgs).replace("/*__AUDIO_JSON__*/{}", auds)
    with open(INDEX, "w") as f: f.write(html)
    print(f"Rendered {INDEX} ({os.path.getsize(INDEX)//1024} KB) with deck {deck['date']} embedded")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="YYYY-MM-DD (default: today, local time)")
    ap.add_argument("--pairs", type=int, default=20, help="deck size, max 20 (Oct 14 2026 rule: never more than 20; shorter is fine)")
    ap.add_argument("--format", choices=["pairs", "single"], default="pairs", help="A-vs-B pairs (default: This / That / Both / Love / Neither) or single-option cards (No/Maybe/Love/Yes)")
    ap.add_argument("--polish", action="store_true", help="build a hand-paired app-polish deck: the newest unseen set (Niko & Vivian apps: 45 + 1 retest + 4 Swipe Controls = 50 pairs; or the 10-10g set: 95 + 5)")
    ap.add_argument("--polish-set", choices=["nv2", "nv", "2026-10-10g"], help="with --polish: which hand-paired set (default: newest set that is still unseen; 'nv' = Niko & Vivian apps, 50 pairs)")
    ap.add_argument("--convert-from", help="build this deck id as a single-card version of an existing pair deck (e.g. 2026-10-10d)")
    ap.add_argument("--ingest", help="results JSON exported from the app")
    ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--seed")
    ap.add_argument("--focus", help="comma-separated category names to boost (x3) for this deck, i.e. what Max is working on now")
    ap.add_argument("--focus-note", help="one-line note on why these categories are in focus (saved in the deck)")
    ap.add_argument("--max-per-category", type=int, help="variety mode: cap pairs per category (e.g. 4)")
    ap.add_argument("--focus-share", type=float, help="variety mode: share of pairs from --focus categories (default 0.3)")
    ap.add_argument("--check-share", type=float, default=0.12, help="share of pairs that re-test disliked directions (default 0.12)")
    ap.add_argument("--allow-repeats", action="store_true", help="if the fresh pool runs out, top up with previously shown options")
    a = ap.parse_args()
    if a.pairs > 20: print(f"WARNING: --pairs {a.pairs} > 20; decks never exceed 20 pairs. Using 20."); a.pairs = 20
    os.makedirs(DECKS, exist_ok=True)
    if not os.path.exists(PROFILE):
        with open(PROFILE, "w") as f: json.dump(empty_profile(), f, indent=1)
    if a.ingest:
        ingest(a.ingest)
        if not a.date: return
    if a.date:
        date = a.date
    else:   # today; if a deck for today already exists, use the next free suffix (2026-10-10b, c, ...)
        base = dt.date.today().isoformat(); date = base
        for suf in "bcdefghij":
            if not os.path.exists(os.path.join(DECKS, f"{date}.json")): break
            date = base + suf
    import re as _re
    if not _re.fullmatch(r"\d{4}-\d{2}-\d{2}[a-z]?", date): sys.exit(f"Bad deck id: {date}")
    dt.date.fromisoformat(date[:10])
    focus = {}
    for c in (a.focus or "").split(","):
        c = c.strip()
        if not c: continue
        if c not in POOL: sys.exit(f"Unknown focus category: {c!r}. Known: {', '.join(POOL)}")
        focus[c] = 3.0
    out = os.path.join(DECKS, f"{date}.json")
    if os.path.exists(out) and not a.force:
        print(f"{out} exists (use --force to regenerate). Re-rendering HTML from it.")
        deck = load_json(out, None)
    else:
        if a.polish:
            # newest polish set whose options are all still unseen (Niko & Vivian set first, then the 10-10g set)
            name = a.polish_set or next((n for n in ("nv2", "nv", "2026-10-10g") if polish_set_unseen(n, date)), None)
            if not name: sys.exit("Every polish set has already been shown. Add a new NV/PZ block to generate_deck.py.")
            deck = POLISH_SETS[name](date, a.seed)
        elif a.convert_from:
            deck = convert_pair_deck(a.convert_from, date, a.pairs)
            print(f"Wrote {out}: {deck['deck_size']} cards from {len(deck['cards'])} options of {a.convert_from}")
        elif a.format == "pairs":
            deck = build_deck(date, a.pairs, a.seed, a.allow_repeats, focus, a.focus_note, a.check_share,
                              a.max_per_category, a.focus_share)
        else:
            deck = build_single_deck(date, a.pairs, a.seed, a.allow_repeats, focus, a.focus_note,
                                     a.check_share if a.check_share != 0.12 else 0.24, a.max_per_category, a.focus_share)
        with open(out, "w") as f: json.dump(deck, f, indent=1, ensure_ascii=False)
        if not a.convert_from:
            fr = deck["freshness"]
            print(f"Wrote {out}: {len(deck.get('cards', deck.get('pairs')))} {deck.get('format', 'pair')} items; {fr['never_shown_before']}/{fr['option_slots']} option slots never shown before ({fr['share']:.0%}).")
            print(f"Allocation: {deck['allocation']}")
    led = save_shown()
    print(f"shown_options.json: {led['shown_count']} shown, {led['unseen_remaining']} of {led['pool_size']} still unseen")
    if not a.no_embed: render_index(deck)

if __name__ == "__main__":
    main()
