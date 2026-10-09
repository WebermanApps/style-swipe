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

What it does:
  * Picks 50 A/B pairs from the option pool below, never repeating a pair that
    appears in any existing decks/*.json (falls back to repeats only if a
    category's pool is exhausted).
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

CATEGORY_WEIGHT = {  # base share of the deck
    "App / UI Style": 1.0, "Color Palette": 1.1, "Typography": 1.0, "Business Communication Tone": 1.1,
    "Home / Interior Style": 1.0, "Logo / Mark": 1.0, "Photography Style": 0.8, "Fashion / Personal Look": 0.8,
    "YouTube Thumbnail Style": 0.8, "Icon & Illustration Style": 0.6,
}

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

def allocate(profile, total, rng):
    raw = {c: CATEGORY_WEIGHT[c] * (0.5 + category_uncertainty(profile, c)) for c in POOL}
    s = sum(raw.values())
    alloc = {c: max(2, int(round(total * v / s))) for c, v in raw.items()}
    cats = sorted(POOL, key=lambda c: -raw[c])
    i = 0
    while sum(alloc.values()) != total:   # fix rounding
        c = cats[i % len(cats)]
        if sum(alloc.values()) > total and alloc[c] > 2: alloc[c] -= 1
        elif sum(alloc.values()) < total: alloc[c] += 1
        i += 1
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

def build_deck(date, n_pairs, seed=None):
    rng = random.Random(seed if seed is not None else date)
    profile = load_json(PROFILE, empty_profile())
    seen = seen_pairs(exclude_date=date)
    alloc = allocate(profile, n_pairs, rng)
    pairs, used_opts = [], {}
    for cat, k in alloc.items():
        opts = POOL[cat]
        cands = [(a, b) for a, b in itertools.combinations(opts, 2)]
        fresh = [c for c in cands if pair_key(c[0]["id"], c[1]["id"]) not in seen]
        pool = fresh if len(fresh) >= k else fresh + [c for c in cands if c not in fresh]
        scored = sorted(pool, key=lambda ab: -pair_priority(profile, ab[0], ab[1], rng))
        chosen, count = [], {}
        for a, b in scored:   # spread options: each option at most ~2x per day
            if count.get(a["id"], 0) >= 2 or count.get(b["id"], 0) >= 2: continue
            chosen.append((a, b)); count[a["id"]] = count.get(a["id"], 0) + 1; count[b["id"]] = count.get(b["id"], 0) + 1
            if len(chosen) == k: break
        for a, b in scored:   # top up if spread rule was too strict
            if len(chosen) >= k: break
            if (a, b) not in chosen: chosen.append((a, b))
        for a, b in chosen:
            if rng.random() < 0.5: a, b = b, a
            pairs.append({"category": cat, "optionA": a, "optionB": b,
                          "repeat": pair_key(a["id"], b["id"]) in seen})
    rng.shuffle(pairs)
    # avoid long runs of the same category
    for i in range(1, len(pairs)):
        if pairs[i]["category"] == pairs[i-1]["category"]:
            for j in range(i + 1, len(pairs)):
                if pairs[j]["category"] != pairs[i-1]["category"]:
                    pairs[i], pairs[j] = pairs[j], pairs[i]; break
    for i, p in enumerate(pairs, 1):
        p["id"] = f"{date}-{i:02d}"
        pairs[i-1] = {"id": p["id"], **{k: v for k, v in p.items() if k != "id"}}
    return {"date": date, "version": 1, "owner": "Max Weberman",
            "brands": ["YouTube @AMomentInThai", "Weberman Construction LLC", "Property Management", "AI Agents"],
            "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "allocation": alloc, "pairs": pairs,
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
        deck = build_deck(date, a.pairs, a.seed)
        with open(out, "w") as f: json.dump(deck, f, indent=1, ensure_ascii=False)
        reps = sum(p["repeat"] for p in deck["pairs"])
        print(f"Wrote {out}: {len(deck['pairs'])} pairs, {reps} repeats. Allocation: {deck['allocation']}")
    if not a.no_embed: render_index(deck)

if __name__ == "__main__":
    main()
