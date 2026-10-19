"""WellNest collab look decks, Oct 19 2026 (Max asked directly 9:37 ICT: 'please add more decks for powerhaus and buds station. but please create
new designs that still have our brand but have more differences than our roselle line.'). Branding builds; drawn mockups in wnc1019_draw.
Two this-or-that decks, 20 pairs each, Notes + Share on every card. Each partner is its own co-branded sub-line, not a Roselle recolour:
  PowerHaus Studio Line: slim tins / box pouch / bottle, sash, spine or wrap labels, condensed caps, spring + arc patterns, blue-led palettes.
  Buds Station Lounge Line: round tins / jars / pillow packs, cloud, badge or ticket labels, rounded type, clouds, dots, paws, a sleepy cat.
WellNest DNA everywhere: circle + script mark, cream, mono small print, a kraft cue. All design questions (no deck or layout questions).
No prices, no health claims, no invented partner facts; every card is tagged MOCKUP. English only, light only."""
from md1018_kit import make
import wnc1019_draw as D
PH = dict(pal="bluegold", arch="sash", pattern="springs", type="condensed", lid="dip", finish="matte")
def ph(**k): return dict(PH, **k)
def T_POWERHAUS():
    pairs, P = make("wph19_", "WellNest"); L = "PowerHaus Studio Line"
    c = lambda body, note: D.card(body, note)
    P("Container", L, "Hero container", "which shape should replace the Roselle-style pouch?",
      ("tin", "Slim Tall Tin", "A tall cylinder tin that stands like a water bottle.", "focused", c(D.ph_hero(ph(), "tin"), "Slim tall tin")),
      ("box", "Box Pouch With Gusset", "A flat-bottom pouch printed edge to edge, no cream patch.", "practical", c(D.ph_hero(ph(), "pouch"), "Box pouch, full print")))
    P("Label", L, "Label shape", "a diagonal sash or a vertical colour spine?",
      ("sash", "Diagonal Sash", "A blue band cuts across the front like a stretch.", "bold", c(D.ph_hero(ph(arch="sash"), "tin"), "Diagonal sash")),
      ("spine", "Vertical Spine", "A blue strip down the side carries the PowerHaus name.", "focused", c(D.ph_hero(ph(arch="spine"), "tin"), "Vertical colour spine")))
    P("Label", L, "Label coverage", "should the label be a full wrap band or a solid colour face?",
      ("wrap", "Wrap Band", "Patterned body with a white band around the middle.", "calm", c(D.ph_hero(ph(arch="wrap"), "tin"), "Patterned wrap with band")),
      ("block", "Solid Colour Face", "The whole front in royal blue with white type.", "bold", c(D.ph_hero(ph(arch="block"), "tin"), "Solid blue face")))
    P("Pattern", L, "Pattern", "which pattern feels more like a reformer class?",
      ("springs", "Spring Coils", "Rows of coils, a nod to reformer springs.", "playful", c(D.ph_hero(ph(arch="wrap", pattern="springs"), "tin"), "Spring coils")),
      ("arcs", "Sweeping Arcs", "Long arcs like a reaching, lengthening move.", "calm", c(D.ph_hero(ph(arch="wrap", pattern="arcs"), "tin"), "Sweeping arcs")))
    P("Pattern", L, "Pattern energy", "should the pattern be a quiet dot grid or bold chevrons?",
      ("dots", "Quiet Dot Grid", "Small even dots, clean and calm.", "calm", c(D.ph_hero(ph(arch="wrap", pattern="dots"), "tin"), "Dot grid")),
      ("chev", "Bold Chevrons", "Stacked chevrons that point up, more energy.", "bold", c(D.ph_hero(ph(arch="wrap", pattern="chevron"), "tin"), "Chevrons")))
    P("Colour", L, "Accent palette", "royal blue with gold or navy with lime?",
      ("bg", "Royal Blue And Gold", "From the PowerHaus logo colours.", "warm", c(D.ph_hero(ph(pal="bluegold"), "tin"), "Royal blue + gold")),
      ("nl", "Navy And Lime", "Navy with the lime accent from their site.", "bold", c(D.ph_hero(ph(pal="navylime"), "tin"), "Navy + lime")))
    P("Colour", L, "Lighter palette", "sky blue or white with blue type?",
      ("sky", "Sky Blue", "A brighter, softer blue sash.", "playful", c(D.ph_hero(ph(pal="skyblue"), "tin"), "Sky blue")),
      ("white", "White With Blue Type", "Mostly white, blue only in the type and sash.", "calm", c(D.ph_hero(ph(pal="whiteblue", pattern="dots"), "tin"), "White + blue type")))
    P("Type", L, "Tea name type", "tall condensed caps or rounded lowercase?",
      ("cond", "Tall Condensed Caps", "Sporty, like a studio timetable.", "focused", c(D.ph_hero(ph(type="condensed"), "tin"), "RECOVER in condensed caps")),
      ("round", "Rounded Lowercase", "Friendly and heavy, softer voice.", "warm", c(D.ph_hero(ph(type="rounded"), "tin"), "recover in rounded lowercase")))
    P("Finish", L, "Tin finish", "should the tin be matte white or a brushed metal look?",
      ("matte", "Matte White", "Soft matte white body, blue print.", "calm", c(D.ph_hero(ph(finish="matte"), "tin"), "Matte white tin")),
      ("metal", "Brushed Metal", "Bare metal look with the print on top.", "bold", c(D.ph_hero(ph(finish="metal"), "tin"), "Brushed metal tin")))
    P("Lid", L, "Lid", "solid blue or kraft with a blue band?",
      ("dip", "Blue Dipped Lid", "A solid blue cap, all studio.", "bold", c(D.ph_hero(ph(lid="dip"), "tin"), "Blue lid")),
      ("kraft", "Kraft Lid, Blue Band", "Our kraft colour on top, tied to the WellNest line.", "warm", c(D.ph_hero(ph(lid="kraft"), "tin"), "Kraft lid + blue band")))
    P("Single serve", L, "Grab-and-go format", "which single-serve format fits a gym bag better?",
      ("sticks", "Stick Pack Box", "Slim stick packs in a small carton.", "practical", c(D.ph_hero(ph(), "sticks"), "Stick pack box")),
      ("sachet", "Sachets In A Flat Tin", "Pyramid sachets in a flat, pocket tin.", "calm", c(D.ph_hero(ph(), "sachet"), "Pyramid sachets, flat tin")))
    P("Iced bottle", L, "Iced tea bottle", "clear with a wrap label or frosted with a neck tag?",
      ("clear", "Clear Bottle, Wrap Label", "The ruby tea shows through, label wraps round.", "bold", c(D.ph_hero(ph(bottle="clear"), "bottle"), "Clear bottle, wrap label")),
      ("frost", "Frosted Bottle, Neck Tag", "Soft frosted glass, kraft tag at the neck.", "calm", c(D.ph_hero(ph(bottle="frost"), "bottle"), "Frosted bottle, kraft tag")))
    P("In studio", L, "Front desk display", "how should tins sit at the studio front desk?",
      ("crate", "Wooden Crate", "A small maple crate with a blue band.", "warm", c(D.ph_scene(ph(), "crate"), "Front desk crate, studio mockup")),
      ("cubby", "Wall Cubbies", "Tins in the cubbies like props on a shelf.", "focused", c(D.ph_scene(ph(), "cubby"), "Wall cubbies, studio mockup")))
    P("In studio", L, "After-class tea", "how should tea be offered after a class?",
      ("disp", "Self-Serve Dispenser", "A blue-topped dispenser with paper cups.", "practical", c(D.ph_scene(ph(), "dispenser"), "Self-serve dispenser")),
      ("tray", "Poured Glasses On A Tray", "Glasses poured and waiting on a maple tray.", "warm", c(D.ph_scene(ph(), "tray"), "Poured tray")))
    P("Retail shelf", L, "Shelf display", "one row on a blue strip or a small pyramid?",
      ("row", "One Row, Blue Strip", "Neat row with a blue shelf strip below.", "focused", c(D.ph_scene(ph(), "shelfrow"), "Row with shelf strip")),
      ("pyr", "Small Pyramid Stack", "Shorter tins stacked in a pyramid.", "playful", c(D.ph_scene(ph(), "pyramid"), "Pyramid stack")))
    P("Menu card", L, "Menu card", "should the drinks menu be a desk tent card or a dark wall board?",
      ("tent", "Desk Tent Card", "White tent card with a blue header.", "calm", c(D.ph_menu(ph(), "tent"), "Desk tent card")),
      ("board", "Navy Wall Board", "A navy board with gold spring line.", "bold", c(D.ph_menu(ph(), "board"), "Navy wall board")))
    P("Merch", L, "Drinkware", "which piece of drinkware should carry the co-brand?",
      ("tumb", "Insulated Tumbler", "Blue tumbler with gold arcs.", "bold", c(D.ph_merch(ph(), "tumbler"), "Tumbler")),
      ("mug", "Enamel Mug", "White enamel mug, blue rim, our circle mark.", "warm", c(D.ph_merch(ph(), "mug"), "Enamel mug")))
    P("Merch", L, "Small merch", "should the small merch be a mat towel or a canvas tote?",
      ("towel", "Mat Towel", "Pale blue towel with a stitched band.", "practical", c(D.ph_merch(ph(), "towel"), "Mat towel")),
      ("tote", "Canvas Tote", "Cream tote with a blue spine strip.", "calm", c(D.ph_merch(ph(), "tote"), "Canvas tote")))
    P("Co-brand", L, "Co-brand badge", "a round seal or a side-by-side bar?",
      ("seal", "Round Seal", "Our mark over PowerHaus Pilates in a ring.", "calm", c(D.ph_badge(ph(), "seal"), "Round seal")),
      ("bar", "Side-By-Side Bar", "Our mark, a gold rule, then PowerHaus Pilates.", "focused", c(D.ph_badge(ph(), "bar"), "Side-by-side bar")))
    P("Back panel", L, "Back panel", "an info grid or a class timeline?",
      ("grid", "Info Grid", "Six tidy boxes, details to be filled in.", "practical", c(D.ph_back(ph(), "grid"), "Info grid, details TBC")),
      ("time", "Class Timeline", "Before class, after class, at home.", "playful", c(D.ph_back(ph(), "time"), "Timeline back panel")))
    return pairs
BS = dict(pal="pinkbutter", label="cloud", pattern="clouds", type="bubbly", lid="plain", finish="matte")
def bs(**k): return dict(BS, **k)
def T_BUDS():
    pairs, P = make("wbs19_", "WellNest"); L = "Buds Station Lounge Line"
    c = lambda body, note: D.card(body, note, "#FFFBF8")
    P("Container", L, "Hero container", "which shape should replace the Roselle-style pouch?",
      ("tin", "Short Round Tin", "A squat, toy-like round tin.", "playful", c(D.bs_hero(bs(), "tin"), "Short round tin")),
      ("jar", "Jar With Cloud Lid", "A glass jar with a cloud on the lid.", "warm", c(D.bs_hero(bs(label="badge"), "jar"), "Jar with cloud lid")))
    P("Label", L, "Label shape", "should the front label be a cloud die-cut or a round badge?",
      ("cloud", "Cloud Die-Cut", "A cloud-shaped white label.", "playful", c(D.bs_hero(bs(label="cloud"), "tin"), "Cloud label")),
      ("badge", "Round Badge", "A round badge with a stitched ring.", "calm", c(D.bs_hero(bs(label="badge"), "tin"), "Round badge")))
    P("Pattern", L, "Pattern", "which all-over pattern should wrap the tin?",
      ("clouds", "Puffy Clouds", "Clouds, like the lounge ceiling.", "calm", c(D.bs_hero(bs(pattern="clouds"), "tin"), "Puffy clouds")),
      ("dots", "Dots And Sparkles", "Butter dots with small white sparkles.", "playful", c(D.bs_hero(bs(pattern="dots"), "tin"), "Dots and sparkles")))
    P("Pattern", L, "Second pattern", "should a second tin wear paw prints or soft stripes?",
      ("paws", "Paw Prints", "A trail of small cat paws.", "playful", c(D.bs_hero(bs(pattern="paws", label="badge"), "tin"), "Paw prints")),
      ("stripes", "Soft Stripes", "Pink and butter bands, like an awning.", "warm", c(D.bs_hero(bs(pattern="stripes", label="badge"), "tin"), "Soft stripes")))
    P("Colour", L, "Accent palette", "pink with butter or coral with powder blue?",
      ("pb", "Pink And Butter", "The shop's pink with its butter awning.", "warm", c(D.bs_hero(bs(pal="pinkbutter"), "tin"), "Pink + butter")),
      ("cp", "Coral And Powder Blue", "Coral counter tones with a dusty powder blue.", "calm", c(D.bs_hero(bs(pal="coralpowder"), "tin"), "Coral + powder blue")))
    P("Colour", L, "Colour layout", "a two-tone split or an evening fade?",
      ("split", "Two-Tone Split", "Light top, pink bottom, clean line between.", "focused", c(D.bs_hero(bs(split=True, pattern="dots", label="badge"), "tin"), "Two-tone split")),
      ("grad", "Evening Fade", "Soft fade from cream to butter to pink.", "calm", c(D.bs_hero(bs(grad=True, pattern=None, label="badge"), "tin"), "Evening fade")))
    P("Type", L, "Tea name type", "bubbly lowercase or retro shadow caps?",
      ("bub", "Bubbly Lowercase", "Rounded, hand-drawn feel.", "playful", c(D.bs_hero(bs(type="bubbly", label="badge"), "tin"), "unwind in bubbly lowercase")),
      ("retro", "Retro Shadow Caps", "Soft serif caps with a butter drop shadow.", "warm", c(D.bs_hero(bs(type="retro", label="badge"), "tin"), "UNWIND in retro caps")))
    P("Mascot", L, "Sleepy cat", "should a small sleepy cat curl up at the bottom of the tin?",
      ("cat", "Add The Sleepy Cat", "A curled white cat by the label.", "playful", c(D.bs_hero(bs(cat=True, label="badge"), "tin"), "With a sleepy cat")),
      ("nocat", "No Cat", "Pattern and label only.", "calm", c(D.bs_hero(bs(label="badge"), "tin"), "No cat")))
    P("Pouch", L, "Pouch style", "a pillow pack or a ribbon-tied bag?",
      ("pillow", "Pillow Pack", "Soft pillow pack with crimped top.", "playful", c(D.bs_hero(bs(label="badge"), "pillow"), "Pillow pack")),
      ("bag", "Ribbon-Tied Bag", "Flat-bottom bag with a kraft top and pink bow.", "warm", c(D.bs_hero(bs(label="badge", pattern="dots"), "bag"), "Ribbon-tied bag")))
    P("Finish", L, "Tin finish", "should the tin feel soft-touch matte or glossy like candy?",
      ("matte", "Soft-Touch Matte", "Velvety pastel, no shine.", "calm", c(D.bs_hero(bs(finish="matte", label="badge"), "tin"), "Soft-touch matte")),
      ("gloss", "Candy Gloss", "Bright shine like a sweet wrapper.", "playful", c(D.bs_hero(bs(finish="gloss", label="badge"), "tin"), "Candy gloss")))
    P("Lid", L, "Lid", "should the lid have a scalloped edge or a cloud knob on top?",
      ("scal", "Scalloped Edge", "A butter lid with a wavy edge.", "playful", c(D.bs_hero(bs(lid="scallop", label="badge"), "tin"), "Scalloped lid")),
      ("cloud", "Cloud Knob", "A white lid with a little cloud on top.", "warm", c(D.bs_hero(bs(lid="cloud", label="badge"), "tin"), "Cloud knob lid")))
    P("Iced drink", L, "Iced serve", "a cup with a cloud sticker or a swing-top bottle?",
      ("cup", "Iced Cup, Cloud Sticker", "A clear cup with a dome lid and cloud sticker.", "playful", c(D.bs_iced(bs(), "cup"), "Iced cup")),
      ("bottle", "Swing-Top Bottle", "A glass bottle with a round badge label.", "warm", c(D.bs_iced(bs(), "bottle"), "Swing-top bottle")))
    P("In shop", L, "Counter display", "how should the tea sit in the shop?",
      ("counter", "Counter Tray Of Tins", "Mini tins in a tray on the pink counter.", "warm", c(D.bs_scene(bs(label="badge"), "counter"), "Counter tray, shop mockup")),
      ("rail", "Hanging Pouch Rail", "Pillow packs clipped to a rail.", "playful", c(D.bs_scene(bs(), "rail"), "Pouch rail, shop mockup")))
    P("In shop", L, "Lounge serving", "how should tea be served to people hanging out?",
      ("bench", "Tray On The Bench", "Pot and glass on a tray on the pink bench.", "calm", c(D.bs_scene(bs(), "bench"), "Tray on the bench")),
      ("jars", "Self-Scoop Jars", "Three jars on a ledge to scoop from.", "practical", c(D.bs_scene(bs(), "jars"), "Self-scoop jars")))
    P("Menu card", L, "Menu card", "should the tea menu be a round coaster or a folded postcard?",
      ("coaster", "Round Coaster Menu", "Doubles as a coaster under the glass.", "playful", c(D.bs_menu(bs(), "coaster"), "Coaster menu")),
      ("post", "Folded Postcard", "A small folded card with a cloud cover.", "calm", c(D.bs_menu(bs(), "post"), "Postcard menu")))
    P("Merch", L, "Lounge merch", "a pink cloud mug or a sleepy cat tote?",
      ("mug", "Pink Enamel Mug", "Pink mug with a white cloud and the tea name.", "warm", c(D.bs_merch(bs(), "mug"), "Pink enamel mug")),
      ("tote", "Cat And Clouds Tote", "Pink tote, clouds and the sleepy cat.", "playful", c(D.bs_merch(bs(), "tote"), "Cat and clouds tote")))
    P("Merch", L, "Small merch", "a sticker sheet or enamel pins?",
      ("stick", "Sticker Sheet", "Cloud, cat, star and our circle mark.", "playful", c(D.bs_merch(bs(), "stickers"), "Sticker sheet")),
      ("pin", "Enamel Pins", "A cat pin and a cloud pin.", "warm", c(D.bs_merch(bs(), "pin"), "Enamel pins")))
    P("Gift", L, "Gift set", "should the gift be a lift-off box set or a mini tin trio?",
      ("box", "Lift-Off Box Set", "Tin, mug and stickers in a cloud box.", "warm", c(D.bs_merch(bs(), "shoebox"), "Lift-off gift box")),
      ("trio", "Mini Tin Trio", "Three small tins in three palettes.", "playful", c(D.bs_merch(bs(label="badge"), "trio"), "Mini tin trio")))
    P("Co-brand", L, "Co-brand badge", "a speech bubble or a ticket stub?",
      ("bubble", "Speech Bubble", "Our mark says hello with The Buds Station.", "playful", c(D.bs_badge(bs(), "bubble"), "Speech bubble")),
      ("ticket", "Ticket Stub", "Our mark, a perforation, then the tea.", "calm", c(D.bs_badge(bs(), "ticket"), "Ticket stub")))
    P("Back panel", L, "Back panel", "a little comic or a tick list?",
      ("comic", "Four-Panel Comic", "Scoop, steep, sip, stay a while.", "playful", c(D.bs_back(bs(), "comic"), "Comic steps")),
      ("list", "Tick List", "Plain rows, details to be filled in.", "practical", c(D.bs_back(bs(), "list"), "Tick list, details TBC")))
    return pairs
