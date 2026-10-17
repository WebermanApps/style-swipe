"""Employee Attire Deck: technician uniforms (drawn people, faceless, no likenesses)."""
from uk5_art import *
CHAR = "#3A3D42"; KHAKI = "#B9A27F"; NAVYP = "#2F3A4A"
A = dict(); B = dict(skin=SKIN[2], hair=HAIR[3], hairstyle="pony"); C = dict(skin=SKIN[3], hair=HAIR[2], hairstyle="curly"); D = dict(skin=SKIN[4], hair=HAIR[5], hairstyle="bun")
def P(base, **k): d = dict(base); d.update(k); return d
def strip(y, frames, cur=0):
    """carousel thumbnails row + dots: frames = list of (person kwargs, caption)"""
    n = len(frames); w = (212 - (n - 1) * 5) / n; s = ""
    for i, (p, cap) in enumerate(frames):
        s += zoom(14 + i * (w + 5), y, w, 46, p, 44, 1.0, CREAM if i != cur else "#F6E3DA") + t(14 + i * (w + 5) + w / 2, y + 56, cap, 7.5, INK if i == cur else MUTE, "hind", 600, "middle")
    return s + dots_ind(120, y + 66, n, cur)
def split2(y, h, a, b, la, lb, fy=None, sc=None):
    if fy == "detail":
        s = shot(14, y, 104, h, [a]) + zoom(122, y, 104, h, b, 70, 2.4)
    elif fy is None:
        s = shot(14, y, 104, h, [a]) + shot(122, y, 104, h, [b])
    else:
        s = zoom(14, y, 104, h, a, fy, sc) + zoom(122, y, 104, h, b, fy, sc)
    return s + rect(14, y + h - 15, 104, 15, "#FFFFFFE6") + t(66, y + h - 4.5, la, 7.5, INK, "hind", 600, "middle") + rect(122, y + h - 15, 104, 15, "#FFFFFFE6") + t(174, y + h - 4.5, lb, 7.5, INK, "hind", 600, "middle")
def foot(items, c=INK): return chips(272, items, 14, c)

PAIRS = []
def pair(g, ask, a, b): PAIRS.append((g, ask, a, b))

# 1 polo color (lead card)
pair("Polo Color", "Crew Polo: Terracotta Every Day, Or Add A Charcoal Polo For Dirty Jobs?",
 ("terra_every_day", "Terracotta Every Day", "One color for every visit, matches your door pick.", "calm",
  card("Polo Color", TERRA, shot(14, 30, 212, 160, [P(A, hat="cap"), P(B, cargo=True)]) + strip(196, [(A, "Mon"), (B, "Gutters"), (C, "Attic")], 0) + foot(["One color", "Easy to spot"]))),
 ("charcoal_dirty", "Terracotta + Charcoal Work Polo", "Terracotta at the door, charcoal with a terracotta collar on gutter and attic days.", "practical",
  card("Polo Color", CHAR, shot(14, 30, 212, 160, [P(A, hat="cap"), P(B, polo=CHAR, collar=TERRA, cargo=True)]) + strip(196, [(A, "Door"), (P(B, polo=CHAR, collar=TERRA), "Gutters"), (P(C, polo=CHAR, collar=TERRA), "Attic")], 1) + foot(["Hides dirt", "Two polos each"]))))
# 2 logo placement front/back
pair("Logo Placement", "Logo: Small Chest Logo Plus A Big Back Print, Or Chest And Sleeve With A Plain Back?",
 ("chest_back", "Chest Logo + Big Back Print", "Readable from the driveway when the tech walks away.", "bold",
  card("Logo Placement", TERRA, split2(30, 236, P(C), P(C, back=True), "Front", "Back") + foot(["Seen from street"]))),
 ("chest_sleeve", "Chest Logo + Sleeve Mark", "Quieter back, a small mark on the right sleeve.", "calm",
  card("Logo Placement", LAGOON, split2(30, 236, P(C, sleeve_logo=True), P(C, back=True, logo="none"), "Front", "Back (plain)") + foot(["Low-key"]))))
# 3 logo spot close-up
pair("Logo Placement", "Chest Logo Spot: Left Chest Or Centered Under The Collar?",
 ("logo_left", "Left Chest", "Classic polo spot over the heart.", "calm",
  card("Logo Spot", TERRA, zoom(14, 30, 212, 236, P(D, logo="left"), 62, 3.2) + foot(["Classic"]))),
 ("logo_center", "Centered Under The Collar", "Bigger mark, centered, easy to read at the door.", "bold",
  card("Logo Spot", JUNGLE, zoom(14, 30, 212, 236, P(D, logo="center"), 62, 3.2) + foot(["Bolder"]))))
# 4 pants
pair("Work Pants", "Work Pants: Charcoal Straight-Leg Or Khaki Cargo?",
 ("pants_charcoal", "Charcoal Straight-Leg", "Clean, dark, hides basement dust.", "premium",
  card("Work Pants", CHAR, shot(14, 30, 120, 236, [P(B, pants=CHAR)]) + zoom(138, 30, 88, 236, P(B, pants=CHAR), 170, 2.0) + foot(["Clean line"]))),
 ("pants_khaki", "Khaki Cargo", "Side pockets for a meter and a flashlight.", "practical",
  card("Work Pants", SAFFRON, shot(14, 30, 120, 236, [P(B, pants=KHAKI, cargo=True)]) + zoom(138, 30, 88, 236, P(B, pants=KHAKI, cargo=True), 170, 2.0) + foot(["Pockets"]))))
# 5 hats
pair("Hats", "Hat: Terracotta Cap Or White Cap With A Terracotta Mark?",
 ("cap_terra", "Terracotta Cap", "Matches the polo head to toe.", "bold",
  card("Hats", TERRA, shot(14, 30, 120, 236, [P(A, hat="cap", hatc=TERRA)]) + zoom(138, 30, 88, 236, P(A, hat="cap", hatc=TERRA), 22, 2.6) + foot(["All terracotta"]))),
 ("cap_white", "White Cap, Terracotta Mark", "Lighter look, cooler in summer sun.", "calm",
  card("Hats", LAGOON, shot(14, 30, 120, 236, [P(A, hat="cap", hatc="#FFFFFF")]) + zoom(138, 30, 88, 236, P(A, hat="cap", hatc="#FFFFFF"), 22, 2.6) + foot(["Lighter"]))))
# 6 name patch
def namezoom(p, kind):
    s = zoom(14, 30, 212, 236, p, 66, 3.4)
    if kind == "patch": s += rect(30, 196, 110, 30, "#FFFFFF", TERRA, 0, 1.2) + t(85, 216, "SAM", 13, INK, "khand", anchor="middle") + f'<path d="M85 196 L70 160" stroke="{TERRA}" stroke-width="1"/>'
    else: s += rect(110, 196, 104, 30, "#FFFFFF", LINE, 0, 1) + t(162, 210, "SAM", 11, INK, "khand", anchor="middle") + t(162, 221, "Smart Upkeep Tech", 7.5, MUTE, "hind", 400, "middle")
    return s
pair("Name Patch", "Name: Embroidered Oval Patch Or Printed First Name Under The Logo?",
 ("name_patch", "Embroidered Oval Patch", "Classic service-shirt patch with the first name.", "playful",
  card("Name Patch", TERRA, namezoom(P(C, patch="patch"), "patch") + foot(["Classic"]))),
 ("name_printed", "Printed Name Under Logo", "Name and role printed small under the chest logo.", "premium",
  card("Name Patch", LAGOON, namezoom(P(C, patch="printed"), "printed") + foot(["Cleaner"]))))
# 7 shoes
pair("Shoes", "Shoes: Brown Leather Work Boots Or Dark Athletic Work Shoes?",
 ("shoe_boot", "Brown Work Boots", "Sturdy for roofs, gutters and yards.", "practical",
  card("Shoes", "#6B4A2E", shot(14, 30, 100, 236, [P(D, shoe="boot")]) + zoom(118, 30, 108, 236, P(D, shoe="boot"), 222, 3.0) + foot(["Sturdy"]))),
 ("shoe_athletic", "Athletic Work Shoes", "Lighter for a full day of indoor visits.", "calm",
  card("Shoes", INK, shot(14, 30, 100, 236, [P(D, shoe="athletic")]) + zoom(118, 30, 108, 236, P(D, shoe="athletic"), 222, 3.0) + foot(["Lighter"]))))
# 8 winter layer (carousel)
def wcar(p, title, cur_cap):
    return shot(14, 30, 212, 160, [p]) + strip(196, [(p, "Front"), (P(p, hat="beanie", hatc=TERRA), "With beanie"), (P(p, layer=None, hat=None), "Indoors")], 0)
pair("Seasonal Layers", "Winter Layer: Charcoal Softshell Over The Polo Or A Terracotta Quarter-Zip?",
 ("winter_softshell", "Charcoal Softshell", "Polo collar and logo still show at the door.", "premium",
  card("Winter Layer", CHAR, wcar(P(A, layer="softshell", layerc=CHAR), "", "") + foot(["Polo shows"]))),
 ("winter_qzip", "Terracotta Quarter-Zip", "Warm pullover in the brand color.", "bold",
  card("Winter Layer", TERRA, wcar(P(A, layer="quarterzip", layerc=TERRA), "", "") + foot(["Brand color"]))))
# 9 fall / rain layer
pair("Seasonal Layers", "Spring And Fall Layer: Lagoon Rain Shell Or Charcoal Vest?",
 ("rain_shell", "Lagoon Rain Shell", "Hood for storm checks and gutter days.", "practical",
  card("Rain Layer", LAGOON, split2(30, 236, P(B, layer="rain", layerc=LAGOON), P(B, layer="rain", layerc=LAGOON), "Full", "Detail", "detail") + foot(["For rain"]))),
 ("vest", "Charcoal Vest", "Keeps arms free, polo still on show.", "calm",
  card("Vest Layer", CHAR, split2(30, 236, P(B, layer="vest", layerc=CHAR), P(B, layer="vest", layerc=CHAR, back=False), "Full", "Detail", "detail") + foot(["Arms free"]))))
# 10 indoor shoe covers
pair("Shoes", "Indoors: Blue Disposable Shoe Covers Or Terracotta Reusable Covers?",
 ("covers_blue", "Blue Disposable Covers", "Fresh pair at every door.", "practical",
  card("Shoe Covers", LAGOON, shot(14, 30, 100, 236, [P(C, covers="#7DB7DA")]) + zoom(118, 30, 108, 236, P(C, covers="#7DB7DA"), 228, 3.0) + foot(["Fresh pair"]))),
 ("covers_terra", "Terracotta Reusable Covers", "Branded covers that match the polo.", "bold",
  card("Shoe Covers", TERRA, shot(14, 30, 100, 236, [P(C, covers=TERRA)]) + zoom(118, 30, 108, 236, P(C, covers=TERRA), 228, 3.0) + foot(["On brand"]))))
