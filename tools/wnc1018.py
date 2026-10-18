"""WellNest collab decks, Oct 18 2026 (Max asked WellNest directly 22:44 ICT; Branding builds). Two this-or-that decks, Notes + Share on
every card, Both / Love / Neither, cream #FAF6EE page, drawn SVG pouch and lockup mockups (wnc1018_draw). English only.
WellNest is slightly dominant: The WellNest leads every lockup and the kraft pouch with its watercolour wash stays the base.
Partner names are set in type in their colours; no partner logo artwork. No 10-pick cap (Max approved): as many cards as needed."""
from md1018_kit import make
import wnc1018_draw as D
TERRA_W = ["#D2774E"]; BLUEGOLD = ["#E9C64A", "#3E6FD0"]
ROYAL, GOLD, NAVY, PALE = "#003CA7", "#F8D858", "#1C2A4A", "#DFECFE"
# ---------------- PowerHaus Pilates Collab Deck ----------------
PH = dict(pk="powerhaus", name="Recover", wash=TERRA_W, wtop=410, seed=3, wcols=["#B3263A", "#D8B47A", "#8FA84A"])
def ph(**k): return dict(PH, **k)
PH_BASE = ["ginger", "lemongrass", "roselle"]
PH_BREW = {None: ("#B8452E", ["Ruby red,", "tart and warming"]), "turmeric": ("#C2602A", ["Deeper amber red,", "earthy warmth"]),
           "galangal": ("#B04F38", ["Ruby red,", "sharper, peppery heat"]), "butterfly pea": ("#8E3A7A", ["Magenta purple,", "roselle shifts the blue"]),
           "mint": ("#B24C34", ["Ruby red,", "cool, fresh finish"])}
def ph_blend(add=None):
    ings = PH_BASE + ([add] if add else []); col, note = PH_BREW[add]
    return D.card_blend(ph(), ings, col, note, add)
def T_POWERHAUS():
    pairs, P = make("wph18_", "WellNest")
    L = "PowerHaus Collab Pouch"
    # names
    P("Name", L, "Tea name", "which name should lead the pouch for the PowerHaus collab tea?",
      ("recover", "Recover", "The draft name, plain and warm after class.", "calm", D.card_full(ph(name="Recover"))),
      ("reform", "Reform", "Nods to the reformer, a little sportier.", "focused", D.card_full(ph(name="Reform"))))
    P("Name", L, "Tea name", "which of these two names fits a tea for after a reformer class better?",
      ("coreset", "Core Reset", "The core is the Pilates centre, reset says rest.", "focused", D.card_full(ph(name="Core Reset"))),
      ("postclass", "Post-Class", "Says exactly when to drink it.", "practical", D.card_full(ph(name="Post-Class"))))
    P("Name", L, "Tea name", "should the tea be called Lengthen or keep the draft name Recover?",
      ("lengthen", "Lengthen", "Pilates language, long and calm.", "calm", D.card_full(ph(name="Lengthen"))),
      ("recover2", "Recover", "The draft name stays.", "warm", D.card_full(ph(name="Recover"))))
    # blend
    for k, add, d in (("turm", "turmeric", "Adds earthy warmth and a deeper colour."), ("gal", "galangal", "Adds a sharper, peppery ginger note."),
                      ("pea", "butterfly pea", "Turns the cup magenta purple with the roselle."), ("mint", "mint", "Adds a cool, fresh finish.")):
        P("Blend", L, "Blend", f"should the draft ginger, lemongrass and roselle blend stay as it is or add {add}?",
          ("base" + k, "Keep The Draft Blend", "Ginger, lemongrass and roselle, ruby red cup.", "calm", ph_blend()),
          (k, f"Add {add.title()}", d, "bold" if add == "butterfly pea" else "warm", ph_blend(add)))
    # colour accents
    P("Colour", L, "Accent colour", "should our kraft and cream pouch carry a royal blue or a gold accent from PowerHaus?",
      ("blue", "Royal Blue Accent", "Blue band, rule and partner name in royal blue.", "focused", D.card_full(ph(accent=ROYAL, pcol=ROYAL))),
      ("gold", "Gold Accent", "Soft gold band and rule, partner name in navy.", "warm", D.card_full(ph(accent=GOLD, pcol=NAVY))))
    P("Colour", L, "Accent amount", "should the PowerHaus colour show only in the partner name or also as a band across the top of the label?",
      ("nameonly", "Name Only", "Royal blue only in the PowerHaus name.", "calm", D.card_full(ph(pcol=ROYAL))),
      ("band", "Name And Top Band", "A royal blue band tops the label too.", "bold", D.card_full(ph(accent=ROYAL, pcol=ROYAL))))
    # wash
    P("Wash", L, "Watercolour wash", "should the label keep the warm terracotta wash or switch to a blue and gold wash in PowerHaus colours?",
      ("terra", "Terracotta Wash", "The draft wash, warm and earthy.", "warm", D.card_full(ph(pcol=ROYAL))),
      ("bluegold", "Blue And Gold Wash", "Gold rising into royal blue, sportier.", "bold", D.card_full(ph(wash=BLUEGOLD, pcol=ROYAL))))
    P("Wash", L, "Wash height", "should the wash stay at the draft height or rise higher up the label?",
      ("wlow", "Draft Height", "More cream, the name reads first.", "calm", D.card_full(ph(pcol=ROYAL))),
      ("whigh", "Taller Wash", "More colour on the shelf.", "bold", D.card_full(ph(pcol=ROYAL, wtop=330))))
    # lockup
    Z = "The WellNest stays first and larger"
    P("Lockup", L, "Lockup order", "should the co-brand sit as our circle mark with a for PowerHaus line under the name or as one line at the top?",
      ("draft", "Circle Mark, For Line", "Our circle mark, then for PowerHaus Pilates.", "calm", D.card_zoom(ph(pcol=ROYAL), Z)),
      ("line", "One Line At The Top", "The WellNest × PowerHaus Pilates.", "focused", D.card_zoom(ph(lock="line", conn="x", lk=.62, pcol=ROYAL), Z)))
    P("Lockup", L, "Partner name size", "how big should the PowerHaus name be next to The WellNest?",
      ("half", "Half Size", "PowerHaus at about half our height.", "calm", D.card_zoom(ph(lock="stack", conn="with", lk=.5, pcol=ROYAL), "PowerHaus at about half our size")),
      ("three", "Three Quarters", "PowerHaus closer in size, still second.", "focused", D.card_zoom(ph(lock="stack", conn="with", lk=.75, pcol=ROYAL), "PowerHaus at about three quarters")))
    P("Lockup", L, "Joining word", "which small word should join The WellNest and PowerHaus in the lockup?",
      ("with", "With", "The WellNest with PowerHaus Pilates.", "warm", D.card_zoom(ph(lock="stack", conn="with", lk=.6, pcol=ROYAL), Z)),
      ("x", "Times Sign", "The WellNest × PowerHaus Pilates.", "bold", D.card_zoom(ph(lock="stack", conn="x", lk=.6, pcol=ROYAL), Z)))
    # pouch styling
    P("Pouch", L, "Name type", "should the tea name stay in our typewriter face or be set bold in PowerHaus blue?",
      ("mono", "Our Typewriter Face", "Matches every WellNest pouch.", "calm", D.card_full(ph(pcol=ROYAL))),
      ("bold", "Bold In PowerHaus Blue", "A rounded bold name in royal blue.", "bold", D.card_full(ph(pcol=ROYAL, title_font="partner"))))
    P("Pouch", L, "Window", "should the pouch stay plain kraft or show a small window with the blend inside?",
      ("plain", "Plain Kraft", "As drafted, no window.", "calm", D.card_full(ph(pcol=ROYAL))),
      ("window", "Small Window", "A pill window shows the roselle and ginger.", "practical", D.card_full(ph(pcol=ROYAL, window=True))))
    P("Pouch", L, "Label edge", "should the cream label stay clean or get a thin gold keyline like the PowerHaus gold?",
      ("clean", "Clean Label", "Plain cream, the wash does the work.", "calm", D.card_full(ph(pcol=ROYAL))),
      ("foil", "Thin Gold Keyline", "A fine gold line frames the label.", "warm", D.card_full(ph(pcol=ROYAL, foil=True))))
    # taglines
    P("Tagline", L, "Tagline", "which line should sit under the name to tie recovery to movement?",
      ("t1", "Move well, steep well", "Move well. Steep well. Recover well.", "warm", D.card_full(ph(pcol=ROYAL, tag="Move well. Steep well. Recover well."))),
      ("t2", "The cup after the class", "The cup after the class.", "calm", D.card_full(ph(pcol=ROYAL, tag="The cup after the class."))))
    P("Tagline", L, "Tagline", "which of these two lines says recovery is part of the practice better?",
      ("t3", "Reformer to kettle", "From the reformer to the kettle.", "playful", D.card_full(ph(pcol=ROYAL, tag="From the reformer to the kettle."))),
      ("t4", "Recovery is movement too", "Recovery is part of the movement.", "focused", D.card_full(ph(pcol=ROYAL, tag="Recovery is part of the movement."))))
    P("Tagline", L, "Tagline", "should the pouch use our own new line or the PowerHaus line Pilates for every body, every goal?",
      ("t5", "Stretch it out, steep it in", "Stretch it out. Steep it in.", "playful", D.card_full(ph(pcol=ROYAL, tag="Stretch it out. Steep it in."))),
      ("t6", "Their line: every body", "Pilates for every body, every goal.", "warm", D.card_full(ph(pcol=ROYAL, tag="Pilates for every body, every goal."))))
    return pairs
# ---------------- Buds Station Collab Deck ----------------
OCHRE = ["#D2A548"]; SAFF_LAT = ["#C88E43", "#B8653F"]; PINK_CORAL = ["#E59A8F", "#CA5970"]
BS = dict(pk="buds", name="Unwind", wash=OCHRE, wtop=410, seed=9, mcol="#594A44", wcols=["#E3B53B", "#3F8A4A", "#8FA84A"])
def bs(**k): return dict(BS, **k)
BS_BASE = ["chrysanthemum", "pandan", "lemongrass"]
BS_BREW = {None: ("#CDB45A", ["Pale gold,", "soft and floral"]), "holy basil": ("#B9A34E", ["Gold green,", "gently peppery"]),
           "lotus": ("#D9C38A", ["Pale gold,", "light and floral"]), "dried longan": ("#B98A45", ["Warm amber,", "naturally sweet"])}
def bs_blend(add=None):
    ings = BS_BASE + ([add] if add else []); col, note = BS_BREW[add]
    return D.card_blend(bs(), ings, col, note, add)
def T_BUDS():
    pairs, P = make("wbs18_", "WellNest")
    L = "Buds Station Collab Pouch"
    P("Name", L, "Tea name", "which name should lead the pouch for the Buds Station collab tea?",
      ("unwind", "Unwind", "The draft name, simple and calm.", "calm", D.card_full(bs(name="Unwind"))),
      ("slow", "Slow Afternoon", "A time of day, warm and unhurried.", "warm", D.card_full(bs(name="Slow Afternoon"))))
    P("Name", L, "Tea name", "which of these two neighbourhood names fits the pouch better?",
      ("spires", "Seven Spires", "From the seven spires nearby, kept abstract.", "focused", D.card_full(bs(name="Seven Spires"))),
      ("grove", "Bodhi Grove", "From the 1455 bodhi grove, quiet and green.", "calm", D.card_full(bs(name="Bodhi Grove"))))
    P("Name", L, "Tea name", "should the tea be called Photharam Blend after the road or keep the draft name Unwind?",
      ("photharam", "Photharam Blend", "Named for Photharam Road, a local address.", "practical", D.card_full(bs(name="Photharam Blend"))),
      ("unwind2", "Unwind", "The draft name stays.", "calm", D.card_full(bs(name="Unwind"))))
    for k, add, d in (("basil", "holy basil", "Adds a gentle peppery, herbal note."), ("lotus", "lotus", "Adds a light, floral softness."),
                      ("longan", "dried longan", "Adds a natural, caramel sweetness.")):
        P("Blend", L, "Blend", f"should the draft chrysanthemum, pandan and lemongrass blend stay as it is or add {add}?",
          ("base" + k, "Keep The Draft Blend", "Chrysanthemum, pandan, lemongrass, pale gold cup.", "calm", bs_blend()),
          (k, f"Add {add.title()}", d, "warm", bs_blend(add)))
    P("Wash", L, "Watercolour wash", "should the label take a saffron and laterite wash or a pink and coral wash?",
      ("saffron", "Saffron And Laterite", "Saffron rising into old brick, from the temple walls.", "warm", D.card_full(bs(wash=SAFF_LAT))),
      ("pink", "Pink And Coral", "The shop's pink and coral, brighter.", "playful", D.card_full(bs(wash=PINK_CORAL))))
    P("Wash", L, "Wash against the draft", "should the label keep the draft soft ochre wash or move to saffron and laterite?",
      ("ochre", "Draft Ochre Wash", "Soft golden ochre, as drafted.", "calm", D.card_full(bs())),
      ("saffron2", "Saffron And Laterite", "Deeper, earthier, more of the neighbourhood.", "warm", D.card_full(bs(wash=SAFF_LAT))))
    P("Motif", L, "Small motif", "should the label carry an abstract seven-line spire motif or a single bodhi leaf?",
      ("spire", "Seven-Line Spire Motif", "Seven fine lines, tallest in the middle, abstract.", "focused", D.card_full(bs(motif="spire7", wash=SAFF_LAT))),
      ("bodhi", "Bodhi Leaf", "One smooth heart-shaped leaf with its long tip.", "calm", D.card_full(bs(motif="bodhi", wash=SAFF_LAT))))
    P("Motif", L, "Motif size", "should the motif sit small by our mark or run large and faint behind the name?",
      ("msmall", "Small, By Our Mark", "A quiet detail beside the circle mark.", "calm", D.card_full(bs(motif="spire7", wash=SAFF_LAT))),
      ("mbig", "Large And Faint", "A faint watermark behind the whole label.", "bold", D.card_full(bs(motif="spire7", mpos="big", wash=SAFF_LAT))))
    Z = "The WellNest stays first and larger"
    P("Lockup", L, "Lockup order", "should the co-brand sit as our circle mark with a for line under the name or as one line at the top?",
      ("draft", "Circle Mark, For Line", "Our circle mark, then for The Buds Station.", "calm", D.card_zoom(bs(), Z)),
      ("line", "One Line At The Top", "The WellNest × The Buds Station.", "focused", D.card_zoom(bs(lock="line", conn="x", lk=.55), Z)))
    P("Lockup", L, "Partner name size", "how big should The Buds Station name be next to The WellNest?",
      ("half", "Half Size", "The partner name at about half our height.", "calm", D.card_zoom(bs(lock="stack", conn="with", lk=.5), "Partner name at about half our size")),
      ("three", "Three Quarters", "Closer in size, still second.", "focused", D.card_zoom(bs(lock="stack", conn="with", lk=.75), "Partner name at about three quarters")))
    P("Lockup", L, "Partner name place", "should The Buds Station name sit on the front of the pouch or only on the back panel?",
      ("front", "On The Front", "For The Buds Station under the name.", "warm", D.card_full(bs())),
      ("back", "Back Panel Only", "Front is WellNest only, partner named on the back.", "calm",
       D.card_back(bs(lock="front-only"), [("Made with", "t"), ("", "partner"), ("Photharam Road,", "t"), ("Chiang Mai", "t")])))
    P("Pouch", L, "Partner name colour", "should the partner name be set in the shop pink or in a warm temple brown?",
      ("pinkname", "Shop Pink", "The Buds Station in its pink.", "playful", D.card_full(bs(wash=SAFF_LAT))),
      ("brownname", "Warm Brown", "The Buds Station in old brick brown.", "calm", D.card_full(bs(wash=SAFF_LAT, pcol="#594A44"))))
    P("Pouch", L, "Label texture", "should the cream label stay clean or carry a faint weathered stucco speckle?",
      ("clean", "Clean Label", "Plain cream, as drafted.", "calm", D.card_full(bs(wash=SAFF_LAT))),
      ("stucco", "Stucco Speckle", "A faint speckle like weathered stucco.", "warm", D.card_full(bs(wash=SAFF_LAT, texture="stucco"))))
    P("Pouch", L, "Brick band", "should the wash end softly or sit on a faint laterite brick band at the bottom?",
      ("soft", "Soft Wash Only", "The wash fades out at the bottom edge.", "calm", D.card_full(bs(wash=SAFF_LAT))),
      ("brick", "Faint Brick Band", "A low band of laterite brick texture.", "warm", D.card_full(bs(wash=SAFF_LAT, texture="brick"))))
    P("Pouch", L, "Accent colour", "should the pouch take a dusty teal or a butter yellow accent from the shop?",
      ("teal", "Dusty Teal Accent", "A dusty teal band and rule.", "calm", D.card_full(bs(accent="#6A8288"))),
      ("butter", "Butter Yellow Accent", "A butter yellow band and rule.", "warm", D.card_full(bs(accent="#D9C184"))))
    P("Tagline", L, "Tagline", "which line should sit under the name?",
      ("t1", "Slow afternoons, steeped", "Slow afternoons, steeped.", "calm", D.card_full(bs(wash=SAFF_LAT, tag="Slow afternoons, steeped."))),
      ("t2", "Steep slowly, stay a while", "Steep slowly. Stay a while.", "warm", D.card_full(bs(wash=SAFF_LAT, tag="Steep slowly. Stay a while."))))
    P("Tagline", L, "Tagline", "which of these two lines feels more like the neighbourhood?",
      ("t3", "Old brick, warm light", "Old brick, warm light, one good cup.", "warm", D.card_full(bs(wash=SAFF_LAT, tag="Old brick, warm light, one good cup."))),
      ("t4", "A quiet cup from Photharam", "A quiet cup from Photharam Road.", "calm", D.card_full(bs(wash=SAFF_LAT, tag="A quiet cup from Photharam Road."))))
    P("Tagline", L, "Tagline", "should the pouch carry a tagline at all or leave the name to speak?",
      ("t5", "Brewed for slow afternoons", "Brewed for the long, slow afternoon.", "calm", D.card_full(bs(wash=SAFF_LAT, tag="Brewed for the long, slow afternoon."))),
      ("t6", "No Tagline", "Name and partner line only.", "practical", D.card_full(bs(wash=SAFF_LAT))))
    return pairs
