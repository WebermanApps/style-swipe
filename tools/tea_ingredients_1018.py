"""Chiang Mai Tea Ingredients Deck content (Max asked Oct 18 2026 22:44 ICT; brief from WellNest).
One single card per ingredient, Like or Pass + optional Notes. Light cream only, English only.
Drawn colour-swatch illustrations only (no photos, no people). STAR = already in WellNest teas ("In our teas" tag)."""
CR = "#FAF6EE"; BORD = "#E6DFD1"
# (category, name, flavor note, swatch colour, in our teas)
ING = [
 ("Tea Bases", "Assam Tea Leaf (Miang)", "Brisk, malty, gently astringent", "#5E7B3A", True),
 ("Tea Bases", "Oolong (Doi Mae Salong)", "Floral, toasty, honeyed finish", "#A27B3C", True),
 ("Tea Bases", "Mulberry Leaf", "Soft, grassy, lightly sweet", "#6E9A4B", True),
 ("Tea Bases", "Moringa Leaf", "Green, earthy, spinach-like", "#7FA046", True),
 ("Tea Bases", "Guava Leaf", "Woody, tannic, faintly fruity", "#8A9A4E", False),
 ("Tea Bases", "Pandan Leaf", "Sweet, grassy, vanilla-like", "#3E9B5A", True),
 ("Tea Bases", "Gotu Kola", "Fresh, bitter-green, celery-like", "#4F8A4A", False),
 ("Flowers", "Roselle", "Tart, cranberry-bright, ruby red", "#B3263E", True),
 ("Flowers", "Butterfly Pea", "Mild, earthy, brews deep blue", "#3A4FB8", True),
 ("Flowers", "Chrysanthemum", "Mellow, honeyed, softly floral", "#E2B23A", True),
 ("Flowers", "Jasmine", "Sweet, heady, perfumed", "#D8C98E", False),
 ("Flowers", "Marigold / Calendula", "Earthy, peppery, saffron-hued", "#E8892B", False),
 ("Flowers", "Lotus Petal And Stamen", "Delicate, nutty, faintly sweet", "#E59AAE", False),
 ("Flowers", "Safflower", "Earthy, lightly bitter, golden", "#E0702A", False),
 ("Flowers", "Highland Rose", "Fragrant, soft, gently sweet", "#C9577A", False),
 ("Roots And Spices", "Ginger", "Hot, zesty, warming", "#C99A4B", True),
 ("Roots And Spices", "Galangal", "Sharp, piney, warming", "#C9A27A", False),
 ("Roots And Spices", "Turmeric", "Earthy, peppery, golden", "#D89A1E", False),
 ("Roots And Spices", "Fingerroot (Krachai)", "Earthy, camphor-cool, mildly spicy", "#B88A55", False),
 ("Roots And Spices", "Black Ginger (Krachai Dam)", "Bitter, earthy, deep and woody", "#4B2E5A", False),
 ("Citrus And Herbs", "Lemongrass", "Bright, lemony, clean", "#A7BF4A", True),
 ("Citrus And Herbs", "Kaffir Lime Leaf / Peel", "Zesty, floral citrus, aromatic", "#4E8B3A", True),
 ("Citrus And Herbs", "Thai Basil", "Sweet anise, licorice, peppery", "#5B7F3E", True),
 ("Citrus And Herbs", "Holy Basil", "Clove-spicy, peppery, warming", "#6B8F4A", False),
 ("Citrus And Herbs", "Peppermint / Spearmint", "Cool, fresh, sweet", "#3FA37A", False),
 ("Citrus And Herbs", "Lemon Basil", "Lemony, light, sweet-herbal", "#8DB44E", False),
 ("Fruit", "Dried Longan", "Smoky, caramel-sweet, raisiny", "#8A5A2E", False),
 ("Fruit", "Lychee", "Floral, juicy, rose-sweet", "#D9546A", False),
 ("Fruit", "Mango / Mango Leaf", "Tropical, sweet, lightly resinous", "#F0A830", False),
 ("Fruit", "Tamarind", "Sour-sweet, tangy, date-like", "#7A4A2A", False),
 ("Fruit", "Bael Fruit (Matoom)", "Mellow, caramel, marmalade-like", "#C7893A", False),
 ("Fruit", "Mak Kiang", "Tart, berry-sweet, deep purple", "#5A2A55", False),
 ("Fruit", "Coffee Cherry Husk (Cascara)", "Fruity, hibiscus-tart, honeyed", "#9B3A2A", False),
]
def glyph(cat, c):
    """Simple drawn shape per category, centred at (120, 78) on a 240 x 150 cream card."""
    if cat == "Tea Bases":
        return (f'<path d="M120 30C92 46 84 90 120 126C156 90 148 46 120 30Z" fill="{c}"/>'
                f'<path d="M120 40V122M120 66l-14-10M120 66l14-10M120 88l-16-11M120 88l16-11" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if cat == "Citrus And Herbs":
        return (f'<path d="M94 116C94 84 110 52 138 32C146 62 136 100 94 116Z" fill="{c}"/>'
                f'<path d="M150 116C150 92 140 70 122 56C114 80 122 104 150 116Z" fill="{c}" fill-opacity=".7"/>'
                f'<path d="M96 114C110 90 122 66 136 38" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if cat == "Flowers":
        p = "".join(f'<ellipse cx="120" cy="56" rx="15" ry="24" fill="{c}" transform="rotate({a} 120 80)"/>' for a in range(0, 360, 60))
        return p + '<circle cx="120" cy="80" r="11" fill="#FAF6EE"/><circle cx="120" cy="80" r="6" fill="' + c + '" fill-opacity=".55"/>'
    if cat == "Roots And Spices":
        return (f'<path d="M78 92C78 74 96 70 108 76C112 60 132 58 140 72C154 64 170 76 164 92C176 100 166 118 150 112C142 124 120 124 112 112C96 120 74 110 78 92Z" fill="{c}"/>'
                f'<path d="M96 96q10-6 22 0M132 90q10-6 20 2" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # Fruit
    return (f'<circle cx="120" cy="84" r="36" fill="{c}"/><path d="M120 48q2-12 12-16" stroke="#5E7B3A" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<path d="M126 44c8-8 20-8 26-2-8 8-18 8-26 2z" fill="#6E9A4B"/><path d="M100 70q6-10 16-12" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="3" fill="none" stroke-linecap="round"/>')
def svg(cat, c, star):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 150" width="240" height="150" style="max-width:100%;height:auto">'
         f'<rect x=".5" y=".5" width="239" height="149" rx="10" fill="{CR}" stroke="{BORD}"/>'
         f'<circle cx="120" cy="78" r="58" fill="{c}" fill-opacity=".12"/>' + glyph(cat, c))
    # small colour swatch chip, bottom left
    s += f'<rect x="12" y="122" width="16" height="16" rx="4" fill="{c}"/>'
    return s + '</svg>'
