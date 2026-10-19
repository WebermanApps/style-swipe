"""WellNest ten-pair follow-ups, Oct 19 2026 16:13 ICT (one level past this morning's PowerHaus Can And Base Tea, PowerHaus Can Look,
Tea Theme Blends and Farm Basket Build; none of their pairs repeated). Drawn with wnf1019_draw (480x600 scaled into the kit screen), MOCKUP tagged.
Theme blend cans stay on the WellNest cream and kraft look; PowerHaus keeps its own royal blue spine, arcs and slim can, clearly apart from the Roselle line.
Gentle theme words only, no health claims; no temple, cannabis or hemp imagery."""
from md1018_kit import make
import wnf1019_draw as D
from wnf1019_draw import can, card, surface, blend_card, basket, ROYAL
from wnc1019_draw import R, C, E, T, G, arcs, wn_mark, wn_word, MONO, SCRIPT, HIND, NUN, OSW, CREAM, KRAFT, KRAFT_D, INKW, LOGO, MUTEW
def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
THEMES = [("Relax", "#8C7BB8"), ("Energy", "#E8892B"), ("Calm", "#6E9FB8"), ("Cooldown", "#4FA3A0"), ("Beauty", "#C9577A"),
          ("Hydrate", "#3A8FC9"), ("Vitamin Charge", "#E8B830"), ("Skincare", "#D98C6E"), ("Digestion", "#6E9A3A")]
TC = dict(THEMES)
def wcan(theme, **k):
    """WellNest theme blend can: cream body, kraft lid, theme colour band; not the PowerHaus spine."""
    cfg = dict(finish="cream", label="wrap", pattern=None, main=TC[theme], lid="kraftband", bandw=8, name=theme, nfont="round", lock="small", tag="", tagpos="none")
    cfg.update(k); return cfg
def row(note, cfgs, labels=None, w=110, h=180, extra=""):
    s = surface(); n = len(cfgs); gap = 440 / n
    for i, cf in enumerate(cfgs):
        cx = 20 + gap * (i + .5); s += can(cx, 470, cf, w, h)
        if labels: s += T(cx, 512, labels[i], 13, INKW, MONO, 600)
    return card(s + extra, note)
def one(note, cfg, extra=""):
    return card(surface() + can(240, 470, cfg, 170, 270) + extra, note)
def ing_icons(cx, y, names, r=14):
    s = ""; n = len(names)
    for i, nm in enumerate(names):
        col = D.ICOL.get(nm, "#999"); x = cx + (i - (n - 1) / 2) * (r * 2.6); s += C(x, y, r, col + "33", col, 1.5) + C(x, y, r * .5, col)
    return s

# ===== A. Theme Blend Can Labels =====
def T_CANS():
    pairs, P = make("wnthcan19_", "WellNest"); L = "WellNest Theme Blend Can"
    P("Name", L, "Theme name type", "on the cream theme cans, should the theme name be rounded sans or our script?",
      o("round", "Rounded Sans", "Relax in soft rounded letters.", "friendly", row("Rounded sans", [wcan(t) for t in ("Relax", "Energy", "Calm")])),
      o("script", "WellNest Script", "Relax handwritten, like the logo.", "warm", row("Script", [wcan(t, nfont="script") for t in ("Relax", "Energy", "Calm")])))
    P("Colour", L, "Theme colour use", "should each theme colour fill the whole can around a cream label or show only as a small dot by the name?",
      o("can", "Theme Colour Can", "Can in the theme colour, cream label band.", "bold", row("Colour can", [wcan(t, finish="matte", body=TC[t]) for t in ("Cooldown", "Beauty", "Hydrate")])),
      o("dot", "Small Colour Dot", "Cream can, a dot of theme colour.", "quiet", row("Colour dot", [wcan(t, label="none") for t in ("Cooldown", "Beauty", "Hydrate")],
        extra="".join(C(20 + 440 / 3 * (i + .5), 470 - 180 * .62 + 16, 6, TC[t]) for i, t in enumerate(("Cooldown", "Beauty", "Hydrate"))))))
    P("Ingredients", L, "Ingredients on the front", "should the front show the three or four ingredients as small icons or as one word line?",
      o("icons", "Ingredient Icons", "Little coloured rounds for each herb.", "visual", one("Icons", wcan("Relax"), ing_icons(240, 432, ["Chrysanthemum", "Holy basil", "Longan"]))),
      o("words", "One Word Line", "Chrysanthemum  ·  Holy basil  ·  Longan.", "clear", one("Words", wcan("Relax"), T(240, 432, "Chrysanthemum · Holy basil · Longan", 8.5, INKW, MONO, 500))))
    P("Base tea", L, "Base tea marker", "should the base tea show as a small chip or be part of the blend name?",
      o("chip", "Small Base Chip", "A kraft chip: on oolong.", "tidy", one("Base chip", wcan("Energy"), R(190, 384, 100, 26, CREAM, KRAFT_D, 13, 1.4) + T(240, 402, "on oolong", 13, INKW, MONO, 600))),
      o("name", "Base In The Name", "Oolong Energy as the name.", "direct", one("Base in name", wcan("Energy", name="Oolong Energy"))))
    P("Hierarchy", L, "Theme word or blend name", "should the theme word be the biggest thing on the can or a small word over a blend name?",
      o("theme", "Big Theme Word", "CALM large, nothing else competes.", "simple", one("Theme first", wcan("Calm"))),
      o("blend", "Blend Name, Small Theme", "Jasmine Evening big, calm small above.", "storied", one("Blend first", wcan("Calm", name="Jasmine Evening"), T(240, 300, "CALM", 12, TC["Calm"], MONO, 600, extra='letter-spacing="3"'))))
    P("Range", L, "Shelf order", "for the nine cans on a shelf, should they run as a colour spectrum or in mood groups?",
      o("spec", "Colour Spectrum", "Warm to cool, like a rainbow.", "striking", row("Spectrum", [wcan(t) for t in ("Energy", "Vitamin Charge", "Beauty", "Calm", "Hydrate")], w=72, h=130)),
      o("mood", "Mood Groups", "Wind-down cans together, lift cans together.", "useful", row("Mood groups", [wcan(t) for t in ("Relax", "Calm", "Cooldown", "Energy", "Vitamin Charge")], ["wind", "down", "", "lift", ""], w=72, h=130)))
    P("Lid", L, "Lid band", "should the kraft lid carry a thin band in the theme colour or stay plain kraft?",
      o("band", "Theme Colour Band", "Theme shows from above too.", "coded", one("Lid band", wcan("Digestion", bandw=12))),
      o("plain", "Plain Kraft Lid", "Lids all match; colour stays on the body.", "calm", one("Plain lid", wcan("Digestion", lid="tall", bandw=0))))
    P("Copy", L, "Mood line", "should each can carry one gentle mood line or no line at all?",
      o("line", "One Gentle Line", "For slow evenings, under the name.", "warm", one("Mood line", wcan("Relax", tag="for slow evenings", tagpos="under"))),
      o("none", "No Line", "Name and ingredients only.", "clean", one("No line", wcan("Relax"))))
    back = lambda kind: card(surface() + R(110, 120, 260, 330, CREAM, "#D9CDB8", 12) + T(240, 160, "BACK OF CAN", 12, MUTEW, MONO, 600, extra='letter-spacing="2"')
                             + ("".join(C(160 + i * 80, 230, 26, "#FFFFFF", KRAFT_D, 2) + T(160 + i * 80, 236, s, 13, INKW, MONO, 600) + T(160 + i * 80, 282, l, 12, MUTEW, HIND) for i, (s, l) in enumerate((("85°", "water"), ("4 m", "steep"), ("2 g", "per cup"))))
                                if kind == "guide" else T(240, 220, "Picked in the hills near", 15, INKW, HIND) + T(240, 244, "Chiang Mai, dried slowly,", 15, INKW, HIND) + T(240, 268, "blended in small batches.", 15, INKW, HIND))
                             + wn_word(240, 420, 22, LOGO), "Brew guide" if kind == "guide" else "Herb story")
    P("Back", L, "Back of the can", "should the back lead with a three-icon brew guide or a short story of the herbs?",
      o("guide", "Brew Guide Icons", "Water, steep time, amount.", "practical", back("guide")),
      o("story", "Herb Story", "Where it grew and how it was dried.", "warm", back("story")))
    P("Caffeine", L, "Caffeine marker", "should cans show a simple caffeine-free mark or a light, medium, none scale?",
      o("mark", "Caffeine-Free Mark", "Only on the cans without tea leaf.", "simple", one("Caffeine-free mark", wcan("Cooldown"), R(180, 384, 120, 24, "#FFFFFF", KRAFT_D, 12, 1.2) + T(240, 401, "caffeine-free", 12, INKW, MONO, 600))),
      o("scale", "Three-Dot Scale", "Every can shows its caffeine level.", "informative", one("Caffeine scale", wcan("Energy"), "".join(C(222 + i * 18, 398, 6, "#E8892B" if i < 2 else "#E6DFD1") for i in range(3)) + T(240, 424, "caffeine", 11, MUTEW, MONO))))
    return pairs

# ===== B. Base Tea Taste Pairings =====
def T_BASE():
    pairs, P = make("wnbase19_", "WellNest"); L = "WellNest Base Tea"; B = blend_card
    P("Oolong", L, "Oolong style", "for blends on oolong, should the oolong be light and floral or deeper and roasted?",
      o("light", "Light Floral Oolong", "Bright, orchid-like, pale cup.", "fresh", B("Light floral", "Oolong", "Light oolong", ["Jasmine", "Ginger"], "bright and floral")),
      o("roast", "Roasted Oolong", "Toasty, nutty, amber cup.", "cosy", B("Roasted", "Oolong", "Roasted oolong", ["Longan", "Ginger"], "toasty and warm")))
    P("Green tea", L, "Green tea style", "should the green tea base taste fresh and grassy or carry a jasmine scent?",
      o("grass", "Fresh And Grassy", "Clean green tea, herbs lead the scent.", "clean", B("Grassy green", "Green tea", "Green tea", ["Lemongrass", "Mint"], "fresh and green")),
      o("jas", "Jasmine-Scented", "Green tea already holding jasmine.", "fragrant", B("Jasmine green", "Green tea", "Jasmine green", ["Jasmine", "Mint"], "soft and fragrant")))
    P("White tea", L, "White tea style", "should the white tea be delicate silver tips or fuller white peony?",
      o("silver", "Delicate Silver Tips", "Very light, honeyed.", "delicate", B("Silver tips", "White tea", "Silver tips", ["Chrysanthemum", "Jasmine"], "light and honeyed")),
      o("peony", "Fuller White Peony", "More body, holds herbs better.", "rounded", B("White peony", "White tea", "White peony", ["Chrysanthemum", "Jasmine"], "fuller and soft")))
    P("Oolong", L, "Sweet note on oolong", "for a sweet note on oolong, should it come from longan or mango?",
      o("longan", "Longan", "Deep, caramel-like sweetness.", "mellow", B("Longan", "Oolong", "Oolong", ["Longan", "Lemongrass"], "mellow and sweet")),
      o("mango", "Mango", "Bright tropical sweetness.", "sunny", B("Mango", "Oolong", "Oolong", ["Mango", "Lemongrass"], "sunny and sweet")))
    P("Green tea", L, "Citrus note on green", "for a citrus lift on green tea, should it be kaffir lime or orange peel?",
      o("kaffir", "Kaffir Lime", "Sharp, leafy, very local.", "zesty", B("Kaffir lime", "Green tea", "Green tea", ["Kaffir lime", "Lemongrass"], "zesty and green")),
      o("orange", "Orange Peel (New)", "Softer, sweeter citrus; new, not in your ingredients deck.", "gentle", B("Orange peel", "Green tea", "Green tea", ["Orange peel", "Lemongrass"], "soft citrus")))
    P("White tea", L, "Flower on white", "for a flower on white tea, should it be osmanthus or jasmine?",
      o("osm", "Osmanthus (New)", "Apricot-like, golden; new, not in your ingredients deck.", "golden", B("Osmanthus", "White tea", "White tea", ["Osmanthus", "Chrysanthemum"], "golden and light")),
      o("jas", "Jasmine", "From your liked list, perfumed.", "fragrant", B("Jasmine", "White tea", "White tea", ["Jasmine", "Chrysanthemum"], "soft and floral")))
    P("Oolong", L, "Warm spice on oolong", "for warmth on oolong, should it be ginger or lemongrass?",
      o("ginger", "Ginger", "Gentle heat at the finish.", "warming", B("Ginger", "Oolong", "Oolong", ["Ginger", "Kaffir lime"], "gentle heat")),
      o("lg", "Lemongrass", "Light, lemony lift.", "bright", B("Lemongrass", "Oolong", "Oolong", ["Lemongrass", "Kaffir lime"], "light lift")))
    P("Ratio", L, "Herbs per base", "should each base carry two herbs so the tea shows or three so the herbs lead?",
      o("two", "Two Herbs", "The tea taste stays clear.", "tea-led", B("Two herbs", "Green tea", "Green tea", ["Jasmine", "Mint"], "tea first")),
      o("three", "Three Herbs", "Rounder, more herbal cup.", "herb-led", B("Three herbs", "Green tea", "Green tea", ["Jasmine", "Mint", "Lemongrass"], "herbs first")))
    P("Brewing", L, "Iced pairing", "for an iced serve, should it be iced oolong with mint or iced green tea with lemongrass?",
      o("oolong", "Iced Oolong And Mint", "Toasty and cool.", "rounded", B("Iced oolong", "Iced", "Oolong", ["Mint", "Longan"], "toasty and cool")),
      o("green", "Iced Green And Lemongrass", "Crisp and light.", "crisp", B("Iced green", "Iced", "Green tea", ["Lemongrass", "Kaffir lime"], "crisp and light")))
    P("Brewing", L, "Hot or cold brew", "should the herb-led blends be sold as hot steep first or cold brew first?",
      o("hot", "Hot Steep First", "Kettle, cup, a few minutes.", "classic", B("Hot steep", "Hot steep", "White tea", ["Chrysanthemum", "Jasmine"], "warm cup")),
      o("cold", "Cold Brew First", "Jar in the fridge overnight.", "easy", B("Cold brew", "Cold brew", "Green tea", ["Butterfly pea", "Lemongrass"], "slow and cool")))
    return pairs

# ===== C. PowerHaus Pilates Studio Display =====
PH = dict(main=ROYAL, label="spine", pattern="arcs", lid="kraftband", nfont="mono", lock="line", tagpos="none", tag="")
NAMES = ("Reform", "Core Reset", "Lengthen")
def ph(n, **k): return dict(PH, name=n, **k)
def studio(note, inner, wall="#F4F6FA"):
    return card(R(0, 0, 480, 600, wall) + R(0, 430, 480, 170, "#E9E4DA") + inner, note, wall)
def counter(y=430): return R(40, y, 400, 16, "#C9A26A") + R(40, y + 16, 400, 110, "#E9DCC8")
def T_STUDIO():
    pairs, P = make("phstudio19_", "WellNest"); L = "PowerHaus Studio Display"
    pouch = R(170, 190, 140, 240, "#FBFBF8", "#00000022", 6) + f'<path d="M170 190 l20 -20 h100 l20 20" fill="#EFEFEA" stroke="#00000022"/>' + R(186, 190, 22, 240, ROYAL) + T(255, 300, "The WellNest", 16, INKW, SCRIPT, 700) + T(255, 318, "with", 9, MUTEW, MONO) + T(255, 336, "PowerHaus Pilates", 11, ROYAL, NUN, 800) + T(255, 370, "REFORM", 14, INKW, MONO, 600, extra='letter-spacing="3"')
    P("Container", L, "Can or pouch", "your Collab Look pick was the box pouch but your note says can not pouch, so which should PowerHaus come in?",
      o("can", "Can", "Matte white can, kraft lid, blue spine; your note.", "solid", studio("Can", counter() + can(240, 430, ph("Reform"), 140, 230))),
      o("pouch", "Box Pouch With Gusset", "Stand-up pouch with the spine; your look pick.", "light", studio("Box pouch", counter() + pouch)))
    P("Placement", L, "Display spot", "should the PowerHaus cans live on the front desk counter or on a wall shelf by the mats?",
      o("desk", "Front Desk Counter", "Seen at check-in and checkout.", "welcoming", studio("Front desk", counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)) + T(240, 520, "FRONT DESK", 14, INKW, MONO, 600))),
      o("wall", "Wall Shelf By The Mats", "Seen while class is ending.", "in-the-moment", studio("Wall shelf", R(60, 300, 360, 10, "#C9A26A") + "".join(can(150 + i * 90, 300, ph(n), 70, 110) for i, n in enumerate(NAMES)) + R(60, 440, 360, 30, "#8FA8D8", rx=6) + T(240, 520, "BY THE MATS", 14, INKW, MONO, 600))))
    P("Arrangement", L, "Can arrangement", "should the cans stack in a small pyramid or stand in one tidy line?",
      o("pyr", "Small Pyramid", "Three below, two, one on top.", "abundant", studio("Pyramid", counter() + "".join(can(150 + i * 90, 430, ph(NAMES[i]), 70, 100) for i in range(3)) + "".join(can(195 + i * 90, 316, ph(NAMES[i + 1]), 70, 100) for i in range(2)) + can(240, 202, ph("Reform"), 70, 100))),
      o("line", "One Tidy Line", "All three side by side, labels facing out.", "calm", studio("Line", counter() + "".join(can(110 + i * 65, 430, ph(NAMES[i % 3]), 56, 110) for i in range(5)))))
    disp = lambda kind: (("".join(R(120 + i * 90, 260, 60, 150, "#FFFFFF66", "#9AA9C9", 8, 2) + R(124 + i * 90, 320, 52, 86, ["#C9A26A", "#B7C46A", "#E9E2C8"][i] + "AA", rx=6) + R(144 + i * 90, 410, 12, 20, "#9AA0A6") for i in range(3)))
                         if kind == "jar" else R(150, 330, 80, 90, "#FFFFFF", INKW, 10, 2) + f'<path d="M230 350 q30 10 0 40" stroke="{INKW}" stroke-width="3" fill="none"/>' + "".join(R(260 + i * 34, 390, 26, 34, "#FFFFFF", "#9AA9C9", 4, 1.5) for i in range(4)))
    P("Tasting", L, "Tasting station", "should after-class tasting pour from glass dispensers or from a kettle into small cups?",
      o("jar", "Glass Dispensers", "Three iced blends, help yourself.", "cool", studio("Dispensers", counter() + disp("jar"))),
      o("kettle", "Kettle And Cups", "Warm pour, a little ritual.", "warm", studio("Kettle", counter() + disp("kettle"))))
    P("Signage", L, "Shelf talker", "should each can get a small tent card or should one strip sign explain all three?",
      o("tent", "Tent Card Per Can", "Name and one line in front of each can.", "guided", studio("Tent cards", counter() + "".join(can(150 + i * 90, 400, ph(n), 66, 100) + f'<path d="M{122+i*90} 430 l28 -30 l28 30 z" fill="#FFFFFF" stroke="{ROYAL}"/>' for i, n in enumerate(NAMES)))),
      o("strip", "One Strip Sign", "A blue strip along the counter edge.", "clean", studio("Strip sign", counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)) + R(40, 446, 400, 22, ROYAL) + T(240, 462, "THE CUP AFTER THE CLASS", 12, "#FFFFFF", MONO, 600, extra='letter-spacing="2"'))))
    P("Tasting", L, "Sample cups", "should samples go in small paper cups with the blue spine or small glass cups?",
      o("paper", "Paper Cups With Spine", "Take one, toss it, see the brand.", "easy", studio("Paper cups", counter() + "".join(f'<path d="M{110+i*60} 360 h40 l-6 70 h-28 z" fill="#FFFFFF" stroke="#C9CDD1"/>' + R(116 + i * 60, 362, 6, 66, ROYAL) for i in range(5)))),
      o("glass", "Small Glass Cups", "Washable, the tea colour shows.", "premium", studio("Glass cups", counter() + "".join(R(110 + i * 60, 370, 40, 60, "#FFFFFF88", "#9AA9C9", 4, 1.5) + R(113 + i * 60, 392, 34, 36, ["#C9A26A", "#B7C46A", "#E9E2C8"][i % 3] + "CC", rx=3) for i in range(5)))))
    P("Signage", L, "Class pairing sign", "should a sign pair each blend with a class or simply list the three blends?",
      o("pair", "Blend Per Class", "Reformer: Reform  ·  Mat: Core Reset  ·  Stretch: Lengthen.", "matched", studio("Class pairing", R(110, 90, 260, 220, "#FFFFFF", ROYAL, 8, 2) + "".join(T(240, 140 + i * 50, f"{c}  →  {n}", 15, INKW, MONO, 600) for i, (c, n) in enumerate((("Reformer", "Reform"), ("Mat", "Core Reset"), ("Stretch", "Lengthen")))) + counter())),
      o("list", "Just The Three Blends", "Names and one taste word each.", "simple", studio("Blend list", R(110, 90, 260, 220, "#FFFFFF", ROYAL, 8, 2) + "".join(T(240, 140 + i * 50, n.upper(), 16, ROYAL, MONO, 600, extra='letter-spacing="3"') for i, n in enumerate(NAMES)) + counter())))
    P("Mood", L, "Display lighting", "should the display get a warm spotlight or sit in natural window light?",
      o("spot", "Warm Spotlight", "A soft pool of light on the cans.", "dramatic", studio("Spotlight", f'<path d="M240 40 L120 430 H360 Z" fill="#FFE9B0" opacity=".45"/>' + counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)), "#E9ECF2")),
      o("window", "Natural Window Light", "Bright, airy, morning class feel.", "airy", studio("Window light", R(320, 60, 120, 200, "#FFFFFF", "#C9CDD1", 4, 3) + L2(380) + counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)))))
    bag = lambda kind: studio("Kraft bag" if kind == "kraft" else "White bag", R(170, 180, 140, 230, KRAFT if kind == "kraft" else "#FFFFFF", "#00000022", 4) + (R(186, 180, 22, 230, ROYAL) if kind == "kraft" else arcs(170, 300, 310, 410, ROYAL, 4, 3, .8)) + f'<path d="M205 180 q35 -60 70 0" stroke="{INKW}" stroke-width="4" fill="none"/>' + T(255, 290, "PowerHaus", 16, INKW if kind == "kraft" else ROYAL, NUN, 800))
    P("Take-home", L, "Take-home bag", "should cans go home in a kraft bag with the blue spine or a white bag with the arcs?",
      o("kraft", "Kraft Bag, Blue Spine", "Matches the kraft lid.", "earthy", bag("kraft")),
      o("white", "White Bag, Arcs", "Matches the matte white can.", "fresh", bag("white")))
    P("Backdrop", L, "Display backdrop", "behind the display, should there be a blue arcs panel or a plain white wall with the lockup?",
      o("arcs", "Blue Arcs Panel", "Big sweeping arcs behind the cans.", "branded", studio("Arcs panel", R(80, 60, 320, 330, "#EEF2FA") + arcs(80, 120, 400, 390, ROYAL, 6, 4, .8) + counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)))),
      o("wall", "White Wall, Lockup", "The WellNest with PowerHaus Pilates, painted small.", "quiet", studio("Lockup wall", T(240, 140, "The WellNest", 30, INKW, SCRIPT, 700) + T(240, 166, "with", 12, MUTEW, MONO) + T(240, 192, "PowerHaus Pilates", 18, ROYAL, NUN, 800) + counter() + "".join(can(150 + i * 90, 430, ph(n), 70, 110) for i, n in enumerate(NAMES)), "#FFFFFF")))
    return pairs
def L2(x): return f'<line x1="{x}" y1="60" x2="{x}" y2="260" stroke="#C9CDD1" stroke-width="3"/><line x1="320" y1="160" x2="440" y2="160" stroke="#C9CDD1" stroke-width="3"/>' + f'<path d="M320 260 L200 430 H440 L440 260 Z" fill="#FFF8E0" opacity=".5"/>'

# ===== D. Farm Basket Gift Presentation =====
GIFT = ["Mango And Passion Fruit", "Longan And Lychee", "WellNest Roselle Tea Sachet", "Honey Or Herbal Jam", "Herb Bundle"]
def gb(note, extra_back="", extra_front="", kind="bamboo", items=GIFT, **k):
    s = R(0, 0, 480, 600, "#FAF6EE") + R(0, 440, 480, 160, "#EFE6D6") + extra_back + basket(240, 330, 1.1, kind, items, **k) + extra_front + wn_word(80, 540, 20, LOGO)
    return card(s, note, "#FAF6EE")
def bow(col, x=240, y=250): return f'<path d="M{x} {y} q-40 -30 -40 0 q0 30 40 0 q40 -30 40 0 q0 30 -40 0" fill="{col}"/><path d="M{x} {y} l-16 40 M{x} {y} l16 40" stroke="{col}" stroke-width="5"/>' + C(x, y, 7, col)
def T_GIFT():
    pairs, P = make("wngift19_", "WellNest"); L = "Farm Basket Gift"
    P("Wrap", L, "Gift wrap", "for gifting, should the basket be wrapped in a knotted cloth or stay open with a bow?",
      o("cloth", "Knotted Cloth Wrap", "A cotton cloth tied on top, no plastic.", "thoughtful", gb("Cloth wrap", extra_front=f'<path d="M110 340 Q240 140 370 340 Z" fill="#E9DDC8" stroke="#CDBA9A" stroke-width="2"/>' + C(240, 200, 18, "#E9DDC8", "#CDBA9A", 2))),
      o("open", "Open With A Bow", "Fruit on show, a bow on the handle.", "generous", gb("Open with bow", extra_front=bow("#5E8C3A", 240, 210))))
    P("Ribbon", L, "Ribbon", "should the bow be natural twine or a cotton ribbon in WellNest green?",
      o("twine", "Natural Twine Bow", "Rustic, matches the kraft tag.", "rustic", gb("Twine", extra_front=bow("#B89A6A", 240, 210))),
      o("green", "WellNest Green Ribbon", "Soft cotton, a pop of brand colour.", "branded", gb("Green ribbon", extra_front=bow("#5E8C3A", 240, 210))))
    tagc = lambda kind: R(300, 380, 130, 80, "#FFFFFF", KRAFT_D, 4, 1.5) + (T(365, 418, "For you, with love", 18, INKW, SCRIPT, 700) if kind == "hand" else T(365, 414, "A GIFT FROM", 10, MUTEW, MONO, 600) + T(365, 438, "The WellNest", 18, INKW, SCRIPT, 700))
    P("Message", L, "Gift tag message", "should the gift tag carry a handwritten-look note or a printed A gift from line?",
      o("hand", "Handwritten Look", "For you, with love, in script.", "personal", gb("Handwritten", extra_front=tagc("hand"))),
      o("print", "Printed Gift Line", "A GIFT FROM above our script mark.", "tidy", gb("Printed", extra_front=tagc("print"))))
    P("Card", L, "Gift card placement", "should the gift card tuck in at the front or hang from the handle?",
      o("front", "Tucked In Front", "Peeks out between the fruit.", "neat", gb("Tucked in", extra_front=R(200, 260, 80, 60, "#FFFFFF", KRAFT_D, 3, 1.5) + T(240, 296, "To you", 16, INKW, SCRIPT, 700))),
      o("handle", "Hung From The Handle", "Swings on twine at the top.", "charming", gb("On the handle", extra_front=f'<path d="M300 190 v40" stroke="#B89A6A" stroke-width="2"/>' + R(270, 230, 70, 50, "#FFFFFF", KRAFT_D, 3, 1.5) + T(305, 262, "To you", 15, INKW, SCRIPT, 700))))
    P("Filler", L, "Basket filler", "under the fruit, should the filler be kraft paper shred or dried banana leaf?",
      o("shred", "Kraft Paper Shred", "Soft and springy.", "classic", gb("Paper shred", extra_front="".join(f'<path d="M{150+i*12} 330 q6 -12 12 0" stroke="{KRAFT_D}" stroke-width="2" fill="none"/>' for i in range(16)))),
      o("leaf", "Dried Banana Leaf", "Earthy, farm-like.", "earthy", gb("Banana leaf", liner="banana")))
    P("Add-on", L, "Gift add-on", "should a gift basket add a WellNest tea can or a small jar of honey?",
      o("can", "WellNest Tea Can", "One cream theme can tucked in.", "signature", gb("Tea can", extra_front=can(330, 400, dict(finish="cream", label="wrap", pattern=None, main="#8C7BB8", lid="kraftband", bandw=8, name="Relax", nfont="round", lock="small", tag="", tagpos="none"), 60, 90))),
      o("honey", "Small Honey Jar", "A golden jar with a kraft lid.", "sweet", gb("Honey jar", extra_front=R(306, 330, 50, 64, "#E8B830CC", "#A27B3C", 8, 1.5) + R(304, 320, 54, 14, KRAFT, rx=3))))
    P("Carry", L, "Carry box", "for delivery, should the gift ride in a kraft carry box or be handed over as is?",
      o("box", "Kraft Carry Box", "Open-top box with a handle cut-out.", "protected", gb("Carry box", extra_front=R(100, 300, 280, 140, KRAFT, KRAFT_D, 4, 2) + R(210, 312, 60, 14, "#00000022", rx=7) + T(240, 400, "The WellNest", 26, INKW, SCRIPT, 700))),
      o("asis", "Handed Over As Is", "The basket is the wrapping.", "simple", gb("As is")))
    P("Size", L, "Gift size", "should the gift basket be its own small size or the same as the couple basket?",
      o("small", "Small Gift Size", "A smaller, tighter gift basket.", "giftable", card(R(0, 0, 480, 600, "#FAF6EE") + R(0, 440, 480, 160, "#EFE6D6") + basket(240, 360, .8, "hyacinth", GIFT[:4]) + wn_word(80, 540, 20, LOGO), "Small gift", "#FAF6EE")),
      o("couple", "Same As Couple Basket", "One less size to make.", "practical", gb("Couple size", kind="hyacinth")))
    P("Seal", L, "Seal sticker", "should the wrap or tag get a round WellNest seal sticker?",
      o("seal", "Round WellNest Seal", "Circle mark seals the tag.", "finished", gb("Seal", extra_front=tagc("print") + wn_mark(430, 384, 18))),
      o("none", "No Sticker", "The tag alone is enough.", "minimal", gb("No seal", extra_front=tagc("print"))))
    inside = lambda kind: card(R(0, 0, 480, 600, "#FAF6EE") + R(90, 70, 300, 400, "#FFFFFF", "#D9CDB8", 6, 1.5) + wn_mark(240, 130, 30)
                               + (T(240, 210, "From", 14, MUTEW, MONO, 600) + R(150, 230, 180, 2, "#C9C2B6") + T(240, 290, "To", 14, MUTEW, MONO, 600) + R(150, 310, 180, 2, "#C9C2B6") if kind == "from"
                                  else T(240, 200, "From our farm", 24, INKW, SCRIPT, 700) + "".join(R(130, 230 + i * 22, 220 - (i % 2) * 40, 4, "#E2D8C8", rx=2) for i in range(6))), "From and to" if kind == "from" else "Farm story", "#FAF6EE")
    P("Card", L, "Inside the gift card", "should the gift card inside hold From and To lines or a short story of the farm?",
      o("from", "From And To Lines", "Space for the giver to write.", "personal", inside("from")),
      o("story", "Farm Story", "A few lines about where it grew.", "storied", inside("story")))
    return pairs
