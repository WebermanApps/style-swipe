"""WellNest follow-up decks from Max's Oct 19 2026 results (Branding builds; drawn mockups in wnf1019_draw). 20 this-or-that pairs each:
  PowerHaus Can And Base Tea (from PowerHaus Pilates Collab results + notes: base tea first then herbs; a can, not a pouch)
  PowerHaus Can Look (from PowerHaus Collab Look results: winners applied to cans; fresh palettes, name type, co-brand badge, drinkware)
  Tea Theme Blends (from Chiang Mai Tea Ingredients likes + note: best 3-4 matches per theme, which base goes with which herb)
  Farm Basket Build (from Farm Basket results, all 30 yes: full baskets, sizes, liner + tag combos, note card)
Ingredient notes use common, modest associations only (no medical or health claims). No prices. No temple or cannabis imagery."""
from md1018_kit import make
import wnf1019_draw as D
R_ = D.ROYAL
# ---------------- PowerHaus Can And Base Tea ----------------
PC = dict(label="none", pattern=None, lid="plain", finish="matte", lock="line", conn="with", nfont="mono", tagpos="under")  # Name Only accent, Clean Label, line lockup, 'with', typewriter
def pc(**k): return dict(PC, **k)
def T_CAN():
    pairs, P = make("wnfc19_", "WellNest"); L = "PowerHaus Can"; B = D.blend_card; cc = D.can_card
    P("Base tea", L, "Reform base tea", "should the Reform blend start from green tea or oolong?",
      ("green", "Green Tea Base", "Fresh and grassy, a bright after-class cup.", "fresh", B("Green tea base", "Reform", "Green tea", ["Lemongrass", "Ginger", "Mint"], "Bright and brisk")),
      ("oolong", "Oolong Base", "Rounder and toasty, a fuller cup.", "warm", B("Oolong base", "Reform", "Oolong", ["Ginger", "Lemongrass", "Orange peel"], "Round and toasty")))
    P("Herb pairing", L, "Reform herbs on green tea", "which herbs suit Reform on a green tea base?",
      ("lgm", "Lemongrass, Ginger, Mint", "Zesty and cooling together.", "fresh", B("Lemongrass, ginger, mint", "Reform", "Green tea", ["Lemongrass", "Ginger", "Mint"], "Zesty and cool")),
      ("klb", "Kaffir Lime, Lemon Basil, Ginger", "Citrus-leaf brightness with warmth.", "bold", B("Kaffir lime, lemon basil, ginger", "Reform", "Green tea", ["Kaffir lime", "Lemon basil", "Ginger"], "Citrus and warmth")))
    P("Herb pairing", L, "Reform herbs on oolong", "which herbs suit Reform on an oolong base?",
      ("gop", "Ginger And Orange Peel (New)", "Warm and sweet-citrus over toasty oolong; orange peel is new.", "warm", B("Ginger, orange peel", "Reform", "Oolong", ["Ginger", "Orange peel", "Lemongrass"], "Warm citrus")),
      ("tbm", "Thai Basil And Mint", "Herbal and fresh over the roast.", "fresh", B("Thai basil, mint", "Reform", "Oolong", ["Thai basil", "Mint", "Ginger"], "Herbal and fresh")))
    P("Base tea", L, "Core Reset base tea", "should Core Reset start from white tea or oolong?",
      ("white", "White Tea Base", "Soft, light and delicate.", "calm", B("White tea base", "Core Reset", "White tea", ["Chrysanthemum", "Jasmine", "Longan"], "Soft and light")),
      ("oolong", "Oolong Base", "A little deeper, still smooth.", "warm", B("Oolong base", "Core Reset", "Oolong", ["Holy basil", "Longan", "Ginger"], "Smooth and deeper")))
    P("Herb pairing", L, "Core Reset herbs on white tea", "which herbs and flowers suit Core Reset on white tea?",
      ("cj", "Chrysanthemum And Jasmine", "Two classic white-tea flowers.", "calm", B("Chrysanthemum, jasmine", "Core Reset", "White tea", ["Chrysanthemum", "Jasmine", "Longan"], "Floral and soft")),
      ("hl", "Holy Basil And Lemongrass", "Herby with a clean citrus line.", "fresh", B("Holy basil, lemongrass", "Core Reset", "White tea", ["Holy basil", "Lemongrass", "Mint"], "Herby and clean")))
    P("Herb pairing", L, "Core Reset herbs on oolong", "which herbs suit Core Reset on oolong?",
      ("hl", "Holy Basil And Longan", "Herbal with a gentle dried-fruit sweetness.", "calm", B("Holy basil, longan", "Core Reset", "Oolong", ["Holy basil", "Longan", "Chrysanthemum"], "Herbal and sweet")),
      ("og", "Osmanthus (New) And Ginger", "Apricot-like flower with soft warmth; osmanthus is new.", "warm", B("Osmanthus, ginger", "Core Reset", "Oolong", ["Osmanthus", "Ginger", "Longan"], "Floral warmth")))
    P("Base tea", L, "Lengthen base tea", "should Lengthen start from green tea or white tea?",
      ("green", "Green Tea Base", "Clean and lively.", "fresh", B("Green tea base", "Lengthen", "Green tea", ["Jasmine", "Mint", "Lemongrass"], "Clean and lively")),
      ("white", "White Tea Base", "Airy and gentle.", "calm", B("White tea base", "Lengthen", "White tea", ["Chrysanthemum", "Butterfly pea", "Lemongrass"], "Airy and gentle")))
    P("Herb pairing", L, "Lengthen herbs on green tea", "which herbs suit Lengthen on green tea?",
      ("jm", "Jasmine And Mint", "Fragrant and cool, very classic.", "calm", B("Jasmine, mint", "Lengthen", "Green tea", ["Jasmine", "Mint", "Lemon basil"], "Fragrant and cool")),
      ("bpl", "Butterfly Pea And Lemongrass", "Deep blue cup with citrus notes.", "playful", B("Butterfly pea, lemongrass", "Lengthen", "Green tea", ["Butterfly pea", "Lemongrass", "Mint"], "Blue and citrus")))
    P("Herb pairing", L, "Lengthen herbs on white tea", "which herbs suit Lengthen on white tea?",
      ("cbp", "Chrysanthemum And Butterfly Pea", "Gold flower, blue tint, very gentle.", "calm", B("Chrysanthemum, butterfly pea", "Lengthen", "White tea", ["Chrysanthemum", "Butterfly pea", "Lemongrass"], "Gentle and floral")),
      ("jm", "Jasmine And Mint", "Soft floral with a cool finish.", "fresh", B("Jasmine, mint", "Lengthen", "White tea", ["Jasmine", "Mint", "Lemon basil"], "Floral and cool")))
    P("Base tea", L, "Tea strength", "should each blend be mostly tea with herbs or mostly herbs on a lighter tea base?",
      ("tea", "Tea-Led Blend", "Base tea is the main taste, herbs support it.", "focused", cc("Tea-led blend", pc(name="Reform", tag="Tea-led, herbs support"))),
      ("herb", "Herb-Led Blend", "Herbs lead, a lighter tea base underneath.", "calm", cc("Herb-led blend", pc(name="Reform", tag="Herb-led, light tea base"))))
    P("Can", L, "Can shape", "should the can be tall and slim or short and wide?",
      ("tall", "Tall And Slim", "Stands like a studio water bottle.", "focused", cc("Tall and slim", pc(name="Reform"), w=130)),
      ("short", "Short And Wide", "A sturdy caddy that sits low.", "calm", D.card(D.surface() + D.can(240, 470, pc(name="Reform"), 210, 190), "Short and wide")))
    P("Can", L, "Can size", "should the range come as one full can or a full can plus a mini travel can?",
      ("full", "One Full Can", "One size for the studio shelf.", "practical", cc("One full can", pc(name="Core Reset"))),
      ("mini", "Full Can Plus Mini", "A small can for the class bag too.", "playful", D.card(D.surface() + D.can(190, 470, pc(name="Core Reset"), 150, 240) + D.can(345, 470, pc(name="Core Reset", tag=""), 90, 130), "Full can plus mini")))
    P("Finish", L, "Can finish", "should the can be matte white or soft cream?",
      ("white", "Matte White", "Crisp studio white.", "focused", cc("Matte white", pc(name="Lengthen"))),
      ("cream", "Soft Cream", "WellNest cream, warmer.", "warm", cc("Soft cream", pc(name="Lengthen", finish="cream"))))
    P("Finish", L, "Can wrap", "should the can wear a kraft paper wrap or show brushed metal?",
      ("kraft", "Kraft Paper Wrap", "The WellNest kraft cue on a can.", "warm", cc("Kraft paper wrap", pc(name="Lengthen", finish="kraft"))),
      ("metal", "Brushed Metal", "Bare tin with printed type.", "bold", cc("Brushed metal", pc(name="Lengthen", finish="brushed"))))
    P("Lid", L, "Lid style", "should the can close with a deep kraft lid or a flat pull-tab top?",
      ("kraft", "Deep Kraft Lid With Band", "Slip-on kraft lid with a thin royal band.", "warm", cc("Kraft lid with band", pc(name="Reform", lid="kraftband"))),
      ("pull", "Pull-Tab Seal Top", "A sealed top with a pull ring.", "practical", cc("Pull-tab top", pc(name="Reform", lid="pull"))))
    P("Lid", L, "Lid colour", "should the lid match the can or be royal blue?",
      ("match", "Lid Matches The Can", "One calm colour top to bottom.", "calm", cc("Matching lid", pc(name="Core Reset", lid="plain"))),
      ("blue", "Royal Blue Lid", "The only blue on the can besides the name.", "bold", cc("Royal blue lid", pc(name="Core Reset", lid="slip"))))
    P("Label layout", L, "Lockup placement", "should the one-line lockup sit on a white band or straight on the can?",
      ("band", "On A White Band", "A wrap band frames the lockup and name.", "focused", cc("Lockup on a band", pc(name="Reform", label="wrap", finish="cream"))),
      ("open", "Straight On The Can", "Type printed on the open body.", "calm", cc("Lockup on the can", pc(name="Reform"))))
    P("Label layout", L, "Blend name size", "should the blend name be the biggest thing on the can or sit quietly under the lockup?",
      ("big", "Big Blend Name", "The name leads in large typewriter caps.", "bold", cc("Big blend name", pc(name="Reform", lock="small"))),
      ("quiet", "Quiet Blend Name", "Lockup leads, name below it.", "calm", cc("Quiet blend name", pc(name="Reform"))))
    P("Tagline", L, "Tagline placement", "should the tagline sit under the blend name or run in a band at the base?",
      ("under", "Under The Name", "Small italic line under the name.", "calm", cc("Tagline under name", pc(name="Lengthen", tag="Recovery is movement too"))),
      ("base", "Band At The Base", "A royal band around the bottom.", "bold", cc("Tagline base band", pc(name="Lengthen", tag="Recovery is movement too", tagpos="base"))))
    P("Tagline", L, "Tagline on the lid", "should the tagline also go on the lid band or stay off the lid?",
      ("lid", "On The Lid Band", "The cup after the class, read from above.", "playful", cc("Tagline on lid band", pc(name="Core Reset", lid="kraftband", bandw=16, tagpos="lid"))),
      ("off", "Lid Stays Plain", "Only the band colour on the lid.", "calm", cc("Plain lid band", pc(name="Core Reset", lid="kraftband"))))
    return pairs
# ---------------- PowerHaus Can Look ----------------
LK = dict(label="spine", pattern="arcs", finish="matte", lid="kraftband", lock="line", conn="with", nfont="mono", tagpos="none", tag="")
def lk(**k): return dict(LK, **k)
PALS = {"cobaltsand": ("#2347A8", "#D9C4A0"), "slatecoral": ("#4A6A8A", "#E07A5F"), "tealcream": ("#1F6F78", "#F2E6CF"), "inkpeach": ("#1E2F5C", "#F2B38B"),
        "skykraft": ("#4F86C6", "#C79E6E"), "bluetint": ("#3A5FB8", "#BCD0EE")}
def pal(k): return dict(main=PALS[k][0], acc=PALS[k][1])
def T_LOOK():
    pairs, P = make("wnfl19_", "WellNest"); L = "PowerHaus Can Look"; cc = D.can_card; row = D.can_row
    P("Label", L, "Spine or wrap band on a can", "which of your two label winners works better on a can?",
      ("spine", "Vertical Spine", "A blue strip down the side with PowerHaus.", "focused", cc("Vertical spine", lk(name="Reform"))),
      ("wrap", "Wrap Band", "Arcs on the body, a white band in the middle.", "calm", cc("Wrap band", lk(name="Reform", label="wrap"))))
    P("Pattern", L, "Arc coverage", "should the sweeping arcs cover the whole can or just the lower third?",
      ("full", "Arcs All Over", "Arcs wrap the whole body.", "bold", cc("Arcs all over", lk(name="Core Reset", label="full"))),
      ("low", "Arcs Low", "Arcs rise from the base only.", "subtle", cc("Arcs low", lk(name="Core Reset"))))
    P("Lid", L, "Kraft lid band width", "should the blue band on the kraft lid be thin or wide?",
      ("thin", "Thin Band", "A fine royal line on kraft.", "subtle", cc("Thin band", lk(name="Lengthen", bandw=6))),
      ("wide", "Wide Band", "A bold band most of the lid.", "bold", cc("Wide band", lk(name="Lengthen", bandw=20))))
    P("Colour", L, "Fresh palette", "cobalt with sand or slate blue with coral?",
      ("cs", "Cobalt And Sand", "Deep cobalt with a warm sand partner.", "warm", cc("Cobalt + sand", lk(name="Reform", **pal("cobaltsand")))),
      ("sc", "Slate Blue And Coral", "Muted slate with a coral pop.", "playful", cc("Slate + coral", lk(name="Reform", badge="ribbon", **pal("slatecoral")))))
    P("Colour", L, "Fresh palette", "deep teal with cream or ink blue with peach?",
      ("tc", "Deep Teal And Cream", "Calm teal, very studio.", "calm", cc("Teal + cream", lk(name="Core Reset", **pal("tealcream")))),
      ("ip", "Ink Blue And Peach", "Near-navy with a soft peach.", "warm", cc("Ink + peach", lk(name="Core Reset", badge="ribbon", **pal("inkpeach")))))
    P("Colour", L, "Range colours", "should the three cans share one blue or each get its own shade?",
      ("one", "One Blue For All", "Same blue; names tell them apart.", "focused", row("One blue", [lk(name="Reform"), lk(name="Core Reset"), lk(name="Lengthen")])),
      ("three", "A Shade Per Blend", "Cobalt, teal and sky blue.", "playful", row("A shade per blend", [lk(name="Reform", **pal("cobaltsand")), lk(name="Core Reset", **pal("tealcream")), lk(name="Lengthen", **pal("skykraft"))])))
    P("Name type", L, "Blend name type", "should blend names be rounded sans or small serif caps?",
      ("round", "Rounded Sans", "Soft, friendly and modern.", "friendly", cc("Rounded sans", lk(name="Lengthen", nfont="round"))),
      ("serif", "Serif Caps", "Quiet and refined.", "calm", cc("Serif caps", lk(name="Lengthen", nfont="serif"))))
    P("Name type", L, "Blend name type", "should blend names be wide spaced caps or our script?",
      ("wide", "Wide Spaced Caps", "Airy, stretched like a long move.", "focused", cc("Wide spaced caps", lk(name="Reform", nfont="wide"))),
      ("script", "WellNest Script", "Hand-written, matching our mark.", "warm", cc("WellNest script", lk(name="Reform", nfont="script"))))
    P("Co-brand", L, "Co-brand badge", "should the co-brand badge be a round seal or a hanging ribbon tab?",
      ("seal", "Round Seal", "A small circle seal near the top.", "focused", cc("Round seal", lk(name="Core Reset", badge="seal"))),
      ("ribbon", "Ribbon Tab", "A short ribbon tab off the rim.", "playful", cc("Ribbon tab", lk(name="Core Reset", badge="ribbon", acc="#C79E6E"))))
    P("Co-brand", L, "Badge placement", "should the badge go on the lid top or as a small stamp near the base?",
      ("lid", "Sticker On The Lid", "Seen from above on the shelf.", "playful", cc("Lid sticker", lk(name="Lengthen", badge="sticker"))),
      ("stamp", "Stamp Near The Base", "A quiet studio stamp.", "subtle", cc("Base stamp", lk(name="Lengthen", badge="stamp"))))
    P("Can", L, "Can proportion", "should the look go on a tall slim can or a classic caddy?",
      ("slim", "Tall Slim Can", "Long lines, like the arcs.", "focused", cc("Tall slim", lk(name="Reform"), w=130)),
      ("caddy", "Classic Caddy", "Wider, a little more traditional.", "calm", D.card(D.surface() + D.can(240, 470, lk(name="Reform"), 200, 200), "Classic caddy")))
    P("Can", L, "Matte white or kraft body", "should the body stay matte white or go kraft under the spine?",
      ("white", "Matte White Body", "Your matte white winner.", "focused", cc("Matte white", lk(name="Core Reset"))),
      ("kraft", "Kraft Body", "Kraft can, white lid band.", "warm", cc("Kraft body", lk(name="Core Reset", finish="kraft"))))
    def drink(kind, note, col=R_):
        s = D.surface()
        if kind == "glass": s += D.R(190, 250, 100, 210, "#EAF2FA", "#9FB6CF", 10, 2) + D.arcs(190, 300, 290, 460, col, 3, 3, .7) + D.T(240, 290, "The WellNest", 16, D.INKW, D.SCRIPT, 700)
        if kind == "cup": s += f'<path d="M180 330 h120 l-10 120 q-2 12 -14 12 h-72 q-12 0 -14 -12 z" fill="#FBFBF8" stroke="#BDB3A3" stroke-width="2"/>' + D.R(196, 330, 14, 132, col) + D.T(254, 400, "The WellNest", 15, D.INKW, D.SCRIPT, 700)
        if kind == "bottle": s += D.R(205, 220, 70, 240, "#E3E7EA", "#9AA0A6", 26, 2) + D.R(220, 196, 40, 30, "#C79E6E", rx=6) + D.R(205, 300, 70, 40, col) + D.T(240, 326, "WN + PH", 12, "#FFFFFF", D.OSW, 700)
        if kind == "nohandle": s += f'<path d="M195 360 q0 100 45 100 q45 0 45 -100 z" fill="{D.CREAM}" stroke="#BDB3A3" stroke-width="2"/>' + D.arcs(198, 380, 282, 450, col, 3, 2.4, .7)
        return D.card(s + D.can(380, 470, lk(name="Reform", tag=""), 80, 120), note)
    P("Drinkware", L, "After-class drinkware", "should the studio cup be a clear glass tumbler or a white cup with a blue spine?",
      ("glass", "Glass Tumbler With Arcs", "Clear glass, printed arcs.", "fresh", drink("glass", "Glass tumbler")),
      ("cup", "Cup With Blue Spine", "Matte white cup echoing the can.", "focused", drink("cup", "Cup with spine")))
    P("Drinkware", L, "Take-away drinkware", "should members take a steel bottle or a small handle-less cup?",
      ("bottle", "Steel Bottle", "Kraft cap, blue band.", "practical", drink("bottle", "Steel bottle")),
      ("nohandle", "Handle-Less Cup", "Cream ceramic with arcs.", "calm", drink("nohandle", "Handle-less cup")))
    def flat(kind, note):
        s = D.surface() + D.R(110, 330, 260, 110, "#FBFBF8", "#BDB3A3", 12, 2) + D.R(110, 330, 260, 22, D.KRAFT, rx=10)
        s += (D.R(130, 352, 20, 88, R_) if kind == "spine" else D.arcs(110, 360, 370, 440, R_, 4, 3, .75)) + D.T(250, 400, "The WellNest with PowerHaus Pilates", 13, D.INKW, D.MONO, 500) + D.T(250, 420, "SACHETS", 13, R_, D.OSW, 600, extra='letter-spacing="4"')
        return D.card(s + D.can(410, 470, lk(name="Reform", tag=""), 60, 100), note)
    P("Range", L, "Sachet flat tin", "should the flat sachet tin carry the spine or the arcs?",
      ("spine", "Flat Tin With Spine", "Same blue spine as the can.", "focused", flat("spine", "Flat tin, spine")),
      ("arcs", "Flat Tin With Arcs", "Arcs across the lid.", "calm", flat("arcs", "Flat tin, arcs")))
    def bottle(kind, note):
        s = D.surface() + D.R(200, 220, 80, 250, "#EEF2F4", "#B9C3CA", 20, 2) + D.R(222, 180, 36, 44, "#D9DCDF", rx=4)
        s += f'<path d="M240 226 l40 30 v40 h-36 z" fill="{D.CREAM}" stroke="#A97F52"/>' + (D.R(244, 262, 6, 32, R_) if kind == "spine" else D.arcs(244, 262, 280, 296, R_, 2, 2, .8))
        return D.card(s + D.T(240, 380, "The WellNest", 16, D.INKW, D.SCRIPT, 700) + D.can(390, 470, lk(name="Reform", tag=""), 70, 110), note)
    P("Range", L, "Frosted bottle neck tag", "should the bottle's neck tag carry the spine or the arcs?",
      ("spine", "Tag With Spine", "Matches the spine can.", "focused", bottle("spine", "Neck tag, spine")),
      ("arcs", "Tag With Arcs", "Matches the wrap can.", "calm", bottle("arcs", "Neck tag, arcs")))
    def crate(kind, note):
        s = D.surface() + D.R(70, 360, 340, 110, "#C9A26A", "#A27B3C", 4, 2) + "".join(D.R(70, 368 + i * 34, 340, 4, "#A27B3C") for i in range(3))
        s += "".join(D.can(130 + i * 110, 380, lk(name=["Reform", "Core Reset", "Lengthen"][i], tag=""), 80, 120) for i in range(3))
        s += D.R(70, 430, 340, 24, R_) + D.T(240, 447, "THE WELLNEST WITH POWERHAUS PILATES", 11, "#FFFFFF", D.OSW, 600) if kind == "strip" else D.T(240, 450, "THE WELLNEST", 18, "#7A5A2E", D.MONO, 700, extra='letter-spacing="4"')
        return D.card(s, note)
    P("In studio", L, "Wooden crate display", "should the can crate front have a blue strip or a stamped name?",
      ("strip", "Blue Strip Front", "Your one-row blue strip on the crate.", "bold", crate("strip", "Blue strip")),
      ("stamp", "Stamped Name", "Burned-in look, quieter.", "warm", crate("stamp", "Stamped name")))
    def menu(kind, note):
        s = D.surface() + D.R(120, 70, 240, 380, "#FFFFFF", "#D9CDB8", 6, 1.5) + D.T(240, 110, "AFTER CLASS", 15, R_, D.OSW, 600, extra='letter-spacing="4"')
        if kind == "cans":
            for i, n in enumerate(["Reform", "Core Reset", "Lengthen"]): s += D.can(170, 200 + i * 90, lk(name=n, tag=""), 40, 60) + D.T(200, 180 + i * 90, n, 15, D.INKW, D.MONO, 600, "start")
        else:
            s += D.R(150, 140, 3, 270, R_)
            for i, (t, n) in enumerate([("Before", "Water"), ("After class", "Reform"), ("Cool down", "Core Reset"), ("Evening", "Lengthen")]): s += D.C(151, 160 + i * 70, 7, R_) + D.T(170, 158 + i * 70, t, 12, D.MUTEW, D.MONO, 400, "start") + D.T(170, 178 + i * 70, n, 16, D.INKW, D.MONO, 600, "start")
        return D.card(s + D.T(240, 436, "The WellNest", 16, D.INKW, D.SCRIPT, 700), note)
    P("Menu card", L, "Menu card", "should the studio menu show the three cans or your class timeline?",
      ("cans", "Menu With Cans", "Each blend beside its can.", "friendly", menu("cans", "Menu with cans")),
      ("tl", "Class Timeline Menu", "Which blend fits each moment.", "focused", menu("tl", "Class timeline menu")))
    def shelf(kind, note):
        s = D.surface() + D.R(30, 400, 420, 16, "#E2D6C0") + D.R(30, 416, 420, 30, R_ if kind != "cream" else "#FFFFFF", "#00000022")
        if kind == "arcs": s += D.arcs(30, 418, 450, 446, "#FFFFFF", 3, 2, .6)
        s += D.T(240, 436, "THE WELLNEST WITH POWERHAUS PILATES", 12, "#FFFFFF", D.OSW, 600, extra='letter-spacing="2"')
        s += "".join(D.can(80 + i * 80, 398, lk(name=["Reform", "Core Reset", "Lengthen"][i % 3], tag=""), 60, 100) for i in range(5))
        return D.card(s, note)
    P("Retail shelf", L, "Blue shelf strip", "should the one-row blue strip be plain or carry faint arcs?",
      ("plain", "Plain Blue Strip", "Solid blue with white caps.", "focused", shelf("plain", "Plain strip")),
      ("arcs", "Strip With Faint Arcs", "Arcs echo the cans.", "calm", shelf("arcs", "Strip with arcs")))
    P("Label", L, "Wrap band colour", "should the wrap band be bright white or WellNest cream?",
      ("white", "White Band", "Crisp against the arcs.", "focused", cc("White band", lk(name="Lengthen", label="wrap"))),
      ("cream", "Cream Band", "Warmer, more WellNest.", "warm", cc("Cream band", lk(name="Lengthen", label="wrap", finish="cream"))))
    return pairs
# ---------------- Tea Theme Blends ----------------
LIKED = {"Assam Miang", "Oolong", "Mulberry leaf", "Moringa", "Guava leaf", "Gotu kola", "Roselle", "Butterfly pea", "Chrysanthemum", "Jasmine", "Ginger",
         "Lemongrass", "Kaffir lime", "Thai basil", "Holy basil", "Lemon basil", "Mint", "Longan", "Mango", "Tamarind"}
THEMES = [  # theme, mood line, (A base, A herbs, A label), (B base, B herbs, B label) x2
 ("Relax", "An evening cup to wind down", [
   (("Mulberry leaf", ["Chrysanthemum", "Holy basil", "Longan"]), ("Oolong", ["Jasmine", "Holy basil", "Longan"])),
   (("Guava leaf", ["Chrysanthemum", "Jasmine", "Longan"]), ("Mulberry leaf", ["Holy basil", "Lemon basil", "Mint"]))]),
 ("Energy", "A brisk morning or pre-class cup", [
   (("Assam Miang", ["Ginger", "Lemongrass", "Kaffir lime"]), ("Oolong", ["Moringa", "Mint", "Lemongrass"])),
   (("Assam Miang", ["Moringa", "Ginger", "Mango"]), ("Oolong", ["Ginger", "Thai basil", "Kaffir lime"]))]),
 ("Calm", "A steady, soft daytime cup", [
   (("Oolong", ["Jasmine", "Chrysanthemum", "Lemon basil"]), ("Mulberry leaf", ["Holy basil", "Butterfly pea", "Lemongrass"])),
   (("Guava leaf", ["Gotu kola", "Holy basil", "Mint"]), ("Mulberry leaf", ["Gotu kola", "Jasmine", "Chrysanthemum"]))]),
 ("Cooldown", "A cooling cup for hot afternoons", [
   (("Mulberry leaf", ["Chrysanthemum", "Mint", "Butterfly pea"]), ("Guava leaf", ["Roselle", "Lemongrass", "Mint"])),
   (("Oolong", ["Mint", "Kaffir lime", "Lemon basil"]), ("Mulberry leaf", ["Butterfly pea", "Lemongrass", "Lemon basil", "Mint"]))]),
 ("Beauty", "A bright, colourful cup", [
   (("Mulberry leaf", ["Roselle", "Butterfly pea", "Gotu kola"]), ("Oolong", ["Jasmine", "Roselle", "Mango"])),
   (("Guava leaf", ["Roselle", "Longan", "Mint"]), ("Mulberry leaf", ["Butterfly pea", "Chrysanthemum", "Jasmine"]))]),
 ("Hydrate", "An easy iced cup to sip all day", [
   (("Mulberry leaf", ["Lemongrass", "Mango", "Mint"]), ("Guava leaf", ["Roselle", "Kaffir lime", "Longan"])),
   (("Oolong", ["Mango", "Lemongrass", "Lemon basil"]), ("Mulberry leaf", ["Roselle", "Mint", "Lemongrass"]))]),
 ("Vitamins", "Fruity, leafy picks often chosen for vitamin-themed blends", [
   (("Guava leaf", ["Moringa", "Roselle", "Kaffir lime"]), ("Mulberry leaf", ["Moringa", "Mango", "Tamarind"])),
   (("Assam Miang", ["Moringa", "Ginger", "Roselle"]), ("Guava leaf", ["Mango", "Roselle", "Lemongrass"]))]),
 ("Skincare", "Herbs often picked for skin-themed blends", [
   (("Guava leaf", ["Gotu kola", "Moringa", "Mint"]), ("Oolong", ["Gotu kola", "Chrysanthemum", "Jasmine"])),
   (("Mulberry leaf", ["Gotu kola", "Roselle", "Lemongrass"]), ("Guava leaf", ["Butterfly pea", "Gotu kola", "Mango"]))]),
 ("Digestion", "An after-meal cup", [
   (("Oolong", ["Ginger", "Mint", "Lemongrass"]), ("Mulberry leaf", ["Ginger", "Tamarind", "Thai basil"])),
   (("Assam Miang", ["Ginger", "Kaffir lime", "Thai basil"]), ("Guava leaf", ["Mint", "Tamarind", "Lemon basil"]))]),
]
def lab(base, herbs):
    s = ", ".join(herbs); return s if len(s) <= 34 else ", ".join(h.split()[0] for h in herbs)[:34]
def T_TEA():
    pairs, P = make("wnft19_", "WellNest"); L = "Tea Theme Blends"; B = D.blend_card
    for theme, mood, prs in THEMES:
        for j, ((ba, ha), (bb, hb)) in enumerate(prs):
            assert {ba, bb, *ha, *hb} <= LIKED, (theme, ha, hb); assert 3 <= len(ha) <= 4 and 3 <= len(hb) <= 4
            el = f"{theme} blend" if j == 0 else f"{theme} alternate blend"
            P(theme, L, el, f"which three or four ingredient match fits the {theme.lower()} theme better?",
              (f"{theme[:3].lower()}{j}a", lab(ba, ha), f"On {ba.lower()}: {', '.join(h.lower() for h in ha)}.", "calm", B(f"{ba} base", theme, ba, ha, mood)),
              (f"{theme[:3].lower()}{j}b", lab(bb, hb), f"On {bb.lower()}: {', '.join(h.lower() for h in hb)}.", "fresh", B(f"{bb} base", theme, bb, hb, mood)))
    P("Base tea", L, "Caffeine-free base", "which leaf should be the everyday caffeine-free base?",
      ("mul", "Mulberry Leaf", "Mild, grassy, an easy base for flowers.", "calm", B("Mulberry leaf base", "Herbal base", "Mulberry leaf", ["Chrysanthemum", "Butterfly pea", "Lemongrass"], "Mild and grassy")),
      ("gua", "Guava Leaf", "Slightly fruity, good with roselle and citrus.", "fresh", B("Guava leaf base", "Herbal base", "Guava leaf", ["Roselle", "Kaffir lime", "Mint"], "Lightly fruity")))
    P("Base tea", L, "Tea base for ginger and citrus", "should ginger and lemongrass blends sit on Assam Miang or oolong?",
      ("assam", "Assam Miang", "Malty and strong, holds up to ginger.", "bold", B("Assam Miang base", "Tea base", "Assam Miang", ["Ginger", "Lemongrass", "Kaffir lime"], "Malty and brisk")),
      ("oolong", "Oolong", "Smoother, lets the citrus show.", "calm", B("Oolong base", "Tea base", "Oolong", ["Ginger", "Lemongrass", "Kaffir lime"], "Smooth and citrusy")))
    return pairs
# ---------------- Farm Basket Build ----------------
VEG = ["Morning Glory", "Chinese Kale", "Long Beans", "Thai Eggplant", "Pumpkin And Cucumber", "Herb Bundle", "Cherry Tomatoes And Sweet Corn"]
FRUIT = ["Banana And Papaya", "Mango And Passion Fruit", "Longan And Lychee", "Highland Strawberries And Persimmon", "Avocado And Pomelo Or Tangerine"]
def T_FARM():
    pairs, P = make("wnfb19_", "WellNest"); L = "Farm Basket"; bc = D.basket_card; nc = D.note_card
    P("Full basket", L, "Weekly family basket", "should the family basket lean on vegetables or fruit?",
      ("veg", "Veg-Heavy Family Basket", "Greens, beans, eggplant, herbs, one fruit.", "practical", bc("Veg-heavy", "bamboo", VEG[:5] + ["Mango And Passion Fruit"])),
      ("fruit", "Fruit-Heavy Family Basket", "Mango, longan, banana, berries, some greens.", "playful", bc("Fruit-heavy", "bamboo", FRUIT + ["Morning Glory"])))
    P("Full basket", L, "Couple basket mix", "should the couple basket be greens and herbs or fruit and add-ons?",
      ("greens", "Greens And Herbs", "A cook-at-home basket for two.", "practical", bc("Greens and herbs", "hyacinth", ["Chinese Kale", "Herb Bundle", "Long Beans", "Shiitake Or Local Mushrooms"])),
      ("treats", "Fruit And Add-Ons", "Fruit, roselle tea and a jar of honey.", "warm", bc("Fruit and add-ons", "hyacinth", ["Mango And Passion Fruit", "Longan And Lychee", "WellNest Roselle Tea Sachet", "Honey Or Herbal Jam"])))
    P("Full basket", L, "Add-on corner", "which add-ons should crown the basket?",
      ("tea", "Roselle Tea And Honey", "WellNest sachet plus a small honey jar.", "warm", bc("Tea and honey", "rattan", ["Morning Glory", "WellNest Roselle Tea Sachet", "Honey Or Herbal Jam", "Banana And Papaya", "Long Beans"])),
      ("eggs", "Farm Eggs And Dried Roselle", "Eggs when there are some, plus roselle.", "practical", bc("Eggs and roselle", "rattan", ["Morning Glory", "Farm Eggs (If Available)", "Dried Roselle", "Banana And Papaya", "Long Beans"])))
    P("Full basket", L, "Seasonal special", "which seasonal basket should come first?",
      ("rainy", "Bamboo Shoots And Mushrooms", "A rainy-season soup basket.", "calm", bc("Rainy-season basket", "bamboo", ["Bamboo Shoots (In Season)", "Shiitake Or Local Mushrooms", "Herb Bundle", "Pumpkin And Cucumber"])),
      ("cool", "Strawberries And Persimmon", "A cool-season highland basket.", "playful", bc("Cool-season basket", "bamboo", ["Highland Strawberries And Persimmon", "Avocado And Pomelo Or Tangerine", "Chinese Kale", "Longan And Lychee"])))
    P("Full basket", L, "Meal theme", "should a themed basket be breakfast or a stir-fry night?",
      ("bfast", "Breakfast Basket", "Fruit, eggs, honey and tea.", "warm", bc("Breakfast", "rattan", ["Banana And Papaya", "Farm Eggs (If Available)", "Honey Or Herbal Jam", "WellNest Roselle Tea Sachet", "Mango And Passion Fruit"])),
      ("stir", "Stir-Fry Basket", "Greens, beans, mushrooms and herbs.", "practical", bc("Stir-fry night", "rattan", ["Morning Glory", "Chinese Kale", "Long Beans", "Shiitake Or Local Mushrooms", "Herb Bundle"])))
    P("Full basket", L, "Fruit mix", "tropical fruit mix or citrus and avocado?",
      ("trop", "Tropical Mix", "Mango, papaya, longan.", "playful", bc("Tropical mix", "hyacinth", ["Mango And Passion Fruit", "Banana And Papaya", "Longan And Lychee"])),
      ("cit", "Citrus And Avocado", "Pomelo or tangerine with avocado.", "fresh", bc("Citrus and avocado", "hyacinth", ["Avocado And Pomelo Or Tangerine", "Highland Strawberries And Persimmon", "Longan And Lychee"])))
    P("Basket", L, "Family basket weave", "should the family basket be woven bamboo or rattan?",
      ("bam", "Woven Bamboo", "Light open weave.", "calm", bc("Bamboo", "bamboo", VEG[:3] + FRUIT[:2])),
      ("rat", "Rattan", "Sturdier, rounded rim.", "warm", bc("Rattan", "rattan", VEG[:3] + FRUIT[:2])))
    P("Basket", L, "Couple basket carrier", "should the couple basket be water hyacinth or a cotton tote?",
      ("hy", "Water Hyacinth Basket", "Soft, chunky braid.", "warm", bc("Water hyacinth", "hyacinth", ["Morning Glory", "Mango And Passion Fruit", "Longan And Lychee"])),
      ("tote", "Cotton Tote", "Easy to carry and fold.", "practical", bc("Cotton tote", "bamboo", ["Morning Glory", "Mango And Passion Fruit", "Longan And Lychee"], tote=True)))
    def sizes(note, k1, k2, kind):
        s = D.R(0, 0, 480, 600, "#FAF6EE") + D.R(0, 440, 480, 160, "#EFE6D6") + D.basket(150, 360, k1, kind, VEG[:3] + FRUIT[:2]) + D.basket(360, 380, k2, kind, VEG[:2] + FRUIT[:1])
        s += D.T(150, 470, "Family", 15, D.INKW, D.MONO, 600) + D.T(360, 470, "Couple", 15, D.INKW, D.MONO, 600)
        return D.card(s, note, "#FAF6EE")
    P("Size", L, "Size gap", "should family and couple baskets differ a lot or a little in size?",
      ("big", "Clear Size Gap", "Family is about twice the couple basket.", "practical", sizes("Clear size gap", .7, .42, "bamboo")),
      ("small", "Small Size Gap", "Same basket, a bit less inside.", "calm", sizes("Small size gap", .62, .55, "bamboo")))
    P("Size", L, "Same basket for both sizes", "should both sizes use the same basket style?",
      ("same", "Same Style, Two Sizes", "Bamboo for both.", "calm", sizes("Same style", .65, .48, "bamboo")),
      ("diff", "Different Basket Per Size", "Rattan family, hyacinth couple.", "playful", D.card(D.R(0, 0, 480, 600, "#FAF6EE") + D.R(0, 440, 480, 160, "#EFE6D6") + D.basket(150, 360, .65, "rattan", VEG[:3] + FRUIT[:2]) + D.basket(360, 380, .48, "hyacinth", VEG[:2] + FRUIT[:1]), "Different per size", "#FAF6EE")))
    P("Liner and tag", L, "Liner and tag combo", "banana-leaf liner with a kraft tag or cloth liner with a recipe card?",
      ("bk", "Banana Liner And Kraft Tag", "Fresh green liner, kraft name tag.", "warm", bc("Banana + kraft tag", "rattan", VEG[:3] + FRUIT[:2], liner="banana", tag="kraft")),
      ("cr", "Cloth Liner And Recipe Card", "Cream cloth, recipe card tucked in.", "calm", bc("Cloth + recipe card", "rattan", VEG[:3] + FRUIT[:2], liner="cloth", tag="card")))
    P("Liner and tag", L, "Liner with twine", "paper liner with twine or banana-leaf liner with twine?",
      ("pt", "Paper Liner And Twine", "Kraft paper, twine and one dried flower.", "calm", bc("Paper + twine", "bamboo", VEG[:3] + FRUIT[:2], liner="paper", twine=True)),
      ("bt", "Banana Liner And Twine", "Leaf liner, twine and one dried flower.", "warm", bc("Banana + twine", "bamboo", VEG[:3] + FRUIT[:2], liner="banana", twine=True)))
    P("Liner and tag", L, "Tag set", "kraft tag with twine or just the recipe card?",
      ("kt", "Kraft Tag And Twine", "Name tag tied on with a flower.", "warm", bc("Kraft tag + twine", "hyacinth", FRUIT[:3], tag="kraft", twine=True)),
      ("rc", "Recipe Card Only", "One card, nothing tied on.", "calm", bc("Recipe card only", "hyacinth", FRUIT[:3], tag="card")))
    P("Liner and tag", L, "Full dress", "should the basket wear everything or keep it simple?",
      ("all", "Liner, Tag, Card And Twine", "The full gift look.", "warm", bc("Everything", "rattan", VEG[:3] + FRUIT[:2], liner="banana", tag="kraft", twine=True)),
      ("simple", "Liner Only", "Produce speaks for itself.", "calm", bc("Liner only", "rattan", VEG[:3] + FRUIT[:2], liner="cloth")))
    P("Liner and tag", L, "Liner for fruit baskets", "should fruit-heavy baskets use cloth or paper liners?",
      ("cloth", "Cloth Liner", "Soft for ripe fruit.", "calm", bc("Cloth liner", "bamboo", FRUIT, liner="cloth")),
      ("paper", "Paper Liner", "Simple and compostable.", "practical", bc("Paper liner", "bamboo", FRUIT, liner="paper")))
    P("Note card", L, "Note card header", "should the note card open with our script mark or a kraft band?",
      ("script", "Script Mark Header", "WellNest circle and Delivery Day.", "warm", nc("Script header", dict(head="script", list="check"))),
      ("band", "Kraft Band Header", "This week's basket on a kraft band.", "focused", nc("Kraft band header", dict(head="band", list="check"))))
    P("Note card", L, "Item list style", "should the items be a checklist or a simple dotted list?",
      ("check", "Checklist", "Tick off what you used.", "practical", nc("Checklist", dict(head="script", list="check"))),
      ("dots", "Dotted List", "Calm and simple.", "calm", nc("Dotted list", dict(head="script", list="dots"))))
    P("Note card", L, "Storage tips", "should each item show where to store it?",
      ("store", "Storage Tip Per Item", "Fridge, counter or jar of water.", "practical", nc("With storage tips", dict(head="script", list="dots", store=True))),
      ("none", "Items Only", "Just what is inside.", "calm", nc("Items only", dict(head="script", list="dots"))))
    P("Note card", L, "Card extra", "should the bottom of the card hold a recipe or a little fruit border?",
      ("recipe", "Recipe Of The Week", "One easy dish from the basket.", "warm", nc("Recipe of the week", dict(head="band", list="dots", recipe=True))),
      ("art", "Fruit Dot Border", "A row of painted fruit dots.", "playful", nc("Fruit dot border", dict(head="band", list="dots", art=True))))
    P("Note card", L, "Card fullness", "full card or minimal card?",
      ("full", "Full Card", "List, storage tips and a recipe.", "practical", nc("Full card", dict(head="script", list="check", store=True, recipe=True))),
      ("min", "Minimal Card", "Header and items only.", "calm", nc("Minimal card", dict(head="band", list="dots"))))
    return pairs
