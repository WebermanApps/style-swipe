"""Farm Basket Deck content (Max asked Oct 18 2026 23:10 ICT; brief from WellNest). Project 4, Farm Basket Subscription.
30 single Like / Pass cards with a drawn SVG and a one-line note. WellNest look: kraft frame, cream #FAF6EE, watercolour wash. English only.
No prices, no farm claims (notes describe the item or idea only)."""
CR = "#FAF6EE"; KRAFT = "#C79E6E"; KRAFT_D = "#A97F52"; INK = "#3A3531"
G, GD, LEAF = "#5E8C3A", "#3F6B2A", "#7FA046"
# (category, label, note, wash colour, glyph, glyph colours, tags)
CARDS = [
 # (a) 14 food cards, 21 items grouped
 ("Vegetables", "Morning Glory", "Quick stir-fry green with hollow, tender stems", "#7FA046", "greens", [G, GD], []),
 ("Vegetables", "Chinese Kale", "Thick, sweet stems for oyster-sauce stir-fries", "#5E8C3A", "greens", ["#4F7F5A", "#2F5A3A"], []),
 ("Vegetables", "Long Beans", "Crunchy raw with nam prik or tossed in a curry", "#6E9A4B", "beans", [G, GD], []),
 ("Vegetables", "Thai Eggplant", "Small round green eggplants for green curry", "#8DB44E", "rounds", ["#7FA650", "#E9F0D8"], []),
 ("Vegetables", "Pumpkin And Cucumber", "A wedge of pumpkin for soup plus cool, crisp cucumbers", "#E8892B", "pumpkin", ["#E08A2E", "#6E9A4B"], []),
 ("Vegetables", "Bamboo Shoots (In Season)", "Fresh shoots for soup or curry, only when in season", "#C9A26A", "bamboo", ["#D9B98F", "#8A9A4E"], ["In season"]),
 ("Vegetables", "Cherry Tomatoes And Sweet Corn", "Snacking tomatoes with a cob or two of sweet corn", "#D9483B", "tomcorn", ["#D9483B", "#E8C23A"], []),
 ("Vegetables", "Shiitake Or Local Mushrooms", "A handful of mushrooms for soups and stir-fries", "#A27B5C", "mush", ["#8A5A3C", "#EADBC4"], []),
 ("Vegetables", "Herb Bundle", "Lemongrass, galangal, kaffir lime and holy basil, tied together", "#A7BF4A", "herbs", ["#A7BF4A", "#4E8B3A"], []),
 ("Fruit", "Banana And Papaya", "A hand of bananas and a ripe papaya for breakfast", "#E8C23A", "banpap", ["#E8C23A", "#E8892B"], []),
 ("Fruit", "Mango And Passion Fruit", "Sweet mangoes plus tangy passion fruit to scoop", "#F0A830", "mangopf", ["#F0A830", "#6A3A5A"], []),
 ("Fruit", "Longan And Lychee", "Small, juicy fruits you peel by hand", "#C9A27A", "bunch", ["#C9A27A", "#D9546A"], []),
 ("Fruit", "Highland Strawberries And Persimmon", "Strawberries and Doi Ang Khang persimmon from the highlands", "#D9546A", "berrypers", ["#D63A4A", "#E8892B"], []),
 ("Fruit", "Avocado And Pomelo Or Tangerine", "Creamy avocado with a pomelo or a few tangerines", "#8DB44E", "avocit", ["#5E7B3A", "#F0A030"], []),
 # (b) 4 farm add-ons, tagged Idea
 ("Farm Add-Ons", "WellNest Roselle Tea Sachet", "A sachet of WellNest Roselle Tea tucked into the basket", "#B3263E", "sachet", ["#B3263E", KRAFT], ["Idea"]),
 ("Farm Add-Ons", "Dried Roselle", "A small bag of dried roselle calyces for tea or syrup", "#B3263E", "roselle", ["#9B1F35", "#B3263E"], ["Idea"]),
 ("Farm Add-Ons", "Farm Eggs (If Available)", "A few eggs added when there are some to spare", "#E8C987", "eggs", ["#F3E6CF", "#C79E6E"], ["Idea"]),
 ("Farm Add-Ons", "Honey Or Herbal Jam", "A small jar of honey or herbal jam", "#E2B23A", "jar", ["#E2A23A", KRAFT], ["Idea"]),
 # (c) 8 packaging
 ("Packaging", "Woven Bamboo Basket", "Light, open-weave bamboo basket with a handle", "#C9A26A", "basket", ["#C9A26A", "#A27B3C"], []),
 ("Packaging", "Rattan Basket", "Sturdy rattan basket with a rounded rim", "#A27B5C", "basket", ["#9C6B42", "#7A4F2E"], []),
 ("Packaging", "Water Hyacinth Basket", "Soft, chunky braided water hyacinth basket", "#B89A6A", "basket", ["#B89A6A", "#8A6E44"], []),
 ("Packaging", "Banana-Leaf Wrap Liner", "Banana leaves lining the basket around the produce", "#5E8C3A", "bleaf", ["#5E8C3A", "#3F6B2A"], []),
 ("Packaging", "Cotton Tote", "A plain cotton tote instead of a basket", "#E6DFD1", "tote", ["#EFE6D2", "#A97F52"], []),
 ("Packaging", "Basket Return-And-Swap", "Hand back last week's basket when the new one arrives", "#6E9A4B", "swap", ["#C9A26A", "#5E8C3A"], []),
 ("Packaging", "Kraft Tag With Recipe Card", "A kraft tag naming the items plus a simple recipe card", "#C79E6E", "tag", [KRAFT, INK], []),
 ("Packaging", "Twine With A Dried Flower", "Natural twine tied with one dried flower", "#C9577A", "twine", ["#C9577A", "#B89A6A"], []),
 # (d) 4 basket formats
 ("Basket Format", "Family Size", "A bigger basket for a family of four or so", "#E8892B", "size", [KRAFT, "4"], []),
 ("Basket Format", "Couple Size", "A smaller basket for two people", "#D2774E", "size", [KRAFT, "2"], []),
 ("Basket Format", "Fruit-Heavy Or Veg-Heavy Mix", "Choose more fruit or more vegetables in the mix", "#A7BF4A", "mix", ["#F0A830", "#5E8C3A"], []),
 ("Basket Format", "Delivery-Day Note Card", "A short note on the delivery day: what is in and how to store it", "#C9A27A", "note", [KRAFT, INK], []),
]
def _blob(cx, cy, rx, ry, c, o=1): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" fill-opacity="{o}"/>'
def _hl(d, w=2): return f'<path d="{d}" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
def _basket(a, b, weave):
    s = f'<path d="M86 62 Q120 14 154 62" stroke="{b}" stroke-width="5" fill="none"/><path d="M74 64 H166 L156 122 H84 Z" fill="{a}"/>'
    if weave == 0:
        s += "".join(f'<path d="M{78+i*11} 66 L{88+i*8} 120" stroke="{b}" stroke-width="2"/>' for i in range(8))
        s += "".join(f'<path d="M{76+j*1.5} {74+j*12} H{164-j*1.5}" stroke="{b}" stroke-width="2" stroke-dasharray="6 5"/>' for j in range(4))
    elif weave == 1:
        s += "".join(f'<path d="M{75+j*1.6} {74+j*11} Q120 {80+j*11} {165-j*1.6} {74+j*11}" stroke="{b}" stroke-width="3" fill="none"/>' for j in range(5))
    else:
        s += "".join(f'<path d="M{76+j*1.6} {72+j*12} H{164-j*1.6}" stroke="{b}" stroke-width="7" stroke-dasharray="9 3" stroke-linecap="round"/>' for j in range(4))
    return s + f'<rect x="72" y="60" width="96" height="8" rx="4" fill="{b}"/>'
def glyph(kind, c, i):
    a, b = c[0], c[1]
    if kind == "greens":
        return "".join(f'<path d="M{120+dx} 128 C{110+dx} 100 {96+dx*2} 66 {104+dx*2} 34 C{124+dx*2} 50 {130+dx} 96 {120+dx} 128Z" fill="{a if k%2 else b}"/>' for k, dx in enumerate((-22, -8, 6, 20))) + _hl("M118 126 V60")
    if kind == "beans":
        return "".join(f'<path d="M{60+k*8} {40+k*14} C120 {20+k*14} 150 {110+k*6} 186 {96+k*8}" stroke="{a if k%2 else b}" stroke-width="7" fill="none" stroke-linecap="round"/>' for k in range(4))
    if kind == "rounds":
        return "".join(_blob(x, y, 22, 20, a) + f'<path d="M{x-8} {y-18} q8-10 16 0" fill="{G}"/>' + _blob(x - 6, y - 4, 6, 4, b, .7) for x, y in ((96, 92), (140, 92), (118, 60)))
    if kind == "pumpkin":
        return (_blob(100, 88, 38, 30, a) + f'<path d="M100 60 V116 M82 64 Q76 88 82 112 M118 64 Q124 88 118 112" stroke="#B8651E" stroke-width="2" fill="none"/><path d="M98 58 q2-10 10-12" stroke="{GD}" stroke-width="4" fill="none"/>'
                + f'<rect x="138" y="54" width="22" height="70" rx="11" fill="{b}" transform="rotate(18 149 89)"/>' + _hl("M144 64 l6 50", 2))
    if kind == "bamboo":
        return f'<path d="M100 128 L118 30 L138 128 Z" fill="{a}"/><path d="M106 100 H132 M110 76 H128 M114 54 H124" stroke="#A97F52" stroke-width="2"/><path d="M118 32 q-14-4-20 8 M120 34 q14-6 22 4" stroke="{b}" stroke-width="4" fill="none"/>'
    if kind == "tomcorn":
        return ("".join(_blob(x, y, 14, 13, a) + f'<path d="M{x-5} {y-12} l5 4 5-4" stroke="{G}" stroke-width="2.5" fill="none"/>' for x, y in ((78, 98), (104, 108), (90, 76)))
                + f'<path d="M140 128 C126 100 132 54 152 34 C170 54 172 100 160 128Z" fill="{b}"/><path d="M146 128 C140 100 142 70 150 50 M138 128 C120 110 124 80 130 64" stroke="{G}" stroke-width="5" fill="none"/>'
                + "".join(f'<circle cx="{150+(k%2)*6}" cy="{50+k*8}" r="2.6" fill="#F6E7A0"/>' for k in range(9)))
    if kind == "mush":
        return "".join(f'<path d="M{x-28*s} {y} Q{x} {y-44*s} {x+28*s} {y} Z" fill="{a}"/><rect x="{x-7*s}" y="{y}" width="{14*s}" height="{30*s}" rx="5" fill="{b}"/>' for x, y, s in ((100, 84, 1), (146, 96, .75)))
    if kind == "herbs":
        return (f'<path d="M96 128 L112 34 M104 128 L118 30 M112 128 L122 36" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'
                + _blob(140, 112, 16, 10, "#D9C29A") + f'<path d="M130 58 q22-18 34 6 q-18 16-34-6z" fill="{b}"/><path d="M150 82 q14-12 24 2 q-12 12-24-2z" fill="#6B8F4A"/>'
                + '<path d="M92 92 q26 6 40 0" stroke="#B89A6A" stroke-width="3" fill="none"/>')
    if kind == "banpap":
        return (f'<path d="M64 70 Q90 120 128 88 Q96 104 72 62Z" fill="{a}"/><path d="M70 60 Q100 118 136 76 Q100 96 78 56Z" fill="{a}" fill-opacity=".85"/>'
                + _blob(160, 92, 22, 32, b) + _blob(160, 96, 10, 18, "#F6C08A") + "".join(f'<circle cx="{156+(k%2)*8}" cy="{86+k*5}" r="2" fill="#2A2A2A"/>' for k in range(5)))
    if kind == "mangopf":
        return (f'<path d="M80 60 C120 40 136 100 104 120 C76 136 56 90 80 60Z" fill="{a}"/>' + _hl("M82 72 q10-10 20-8", 3)
                + _blob(156, 90, 26, 26, b) + _blob(156, 90, 18, 18, "#E8C23A") + "".join(f'<circle cx="{150+(k%3)*6}" cy="{84+(k//3)*7}" r="2" fill="#2A2A2A"/>' for k in range(6)))
    if kind == "bunch":
        pts = [(100, 60), (88, 76), (110, 78), (96, 94), (118, 96), (106, 112)]
        return (f'<path d="M104 30 L100 58" stroke="{GD}" stroke-width="3"/>' + "".join(_blob(x, y, 11, 11, a) for x, y in pts)
                + "".join(_blob(x + 50, y + 4, 11, 12, b) + f'<circle cx="{x+47}" cy="{y}" r="2" fill="#FFFFFF" fill-opacity=".5"/>' for x, y in pts[:4]))
    if kind == "berrypers":
        return ("".join(f'<path d="M{x} {y+18} C{x-16} {y} {x-12} {y-12} {x} {y-10} C{x+12} {y-12} {x+16} {y} {x} {y+18}Z" fill="{a}"/><path d="M{x-8} {y-10} l8 4 8-4" stroke="{G}" stroke-width="3" fill="none"/>' for x, y in ((82, 84), (108, 100)))
                + _blob(156, 88, 28, 24, b) + f'<path d="M144 66 q12-10 24 0 l-12 6z" fill="{GD}"/>')
    if kind == "avocit":
        return (f'<path d="M92 40 C120 40 124 84 116 108 C108 132 76 132 68 108 C60 84 64 40 92 40Z" fill="{a}"/>' + _blob(92, 100, 14, 16, "#D8E39A") + _blob(92, 102, 7, 8, "#8A5A2E")
                + _blob(156, 90, 30, 30, b) + f'<path d="M156 60 V120 M126 90 H186 M135 69 L177 111 M177 69 L135 111" stroke="#F6C770" stroke-width="2"/>')
    if kind == "sachet":
        return f'<rect x="92" y="40" width="56" height="78" rx="4" fill="#FFFFFF" stroke="{b}" stroke-width="2"/><rect x="92" y="88" width="56" height="30" fill="{a}" fill-opacity=".75"/><text x="120" y="66" font-size="9" text-anchor="middle" fill="{INK}" font-family="Caveat, cursive" font-weight="700">The WellNest</text><text x="120" y="80" font-size="7" text-anchor="middle" fill="{INK}" font-family="Hind, sans-serif">Roselle Tea</text><path d="M120 40 V24" stroke="{b}" stroke-width="1.5"/><rect x="112" y="16" width="16" height="10" fill="{b}"/>'
    if kind == "roselle":
        return "".join(f'<path d="M{x} {y+16} C{x-16} {y+6} {x-14} {y-12} {x} {y-18} C{x+14} {y-12} {x+16} {y+6} {x} {y+16}Z" fill="{a if k%2 else b}"/><path d="M{x} {y-14} V{y+12}" stroke="#E8798A" stroke-width="1.5"/>' for k, (x, y) in enumerate(((96, 84), (122, 72), (146, 88), (118, 104))))
    if kind == "eggs":
        return f'<path d="M70 104 H170 L160 124 H80 Z" fill="{b}"/>' + "".join(_blob(x, 92, 15, 20, a) + _blob(x - 4, 84, 4, 6, "#FFFFFF", .7) for x in (92, 120, 148))
    if kind == "jar":
        return f'<rect x="96" y="46" width="48" height="74" rx="10" fill="{a}"/><rect x="92" y="36" width="56" height="14" rx="3" fill="{b}"/><rect x="104" y="72" width="32" height="24" rx="3" fill="{CR}"/><path d="M110 84 h20" stroke="{INK}" stroke-width="1.5"/>' + _hl("M104 56 V110", 3)
    if kind == "basket":
        return _basket(a, b, {"#C9A26A": 0, "#9C6B42": 1}.get(a, 2))
    if kind == "bleaf":
        return _basket("#C9A26A", "#A27B3C", 0) + f'<path d="M66 70 C90 30 130 40 120 66Z M174 70 C150 30 110 40 120 66Z" fill="{a}"/><path d="M70 68 L118 58 M170 68 L122 58" stroke="{b}" stroke-width="2"/>'
    if kind == "tote":
        return f'<path d="M98 60 Q98 26 120 26 Q142 26 142 60" stroke="{b}" stroke-width="5" fill="none"/><rect x="82" y="58" width="76" height="68" rx="4" fill="{a}" stroke="{b}" stroke-width="1.5"/><text x="120" y="98" font-size="12" text-anchor="middle" fill="{INK}" font-family="Caveat, cursive" font-weight="700">The WellNest</text>'
    if kind == "swap":
        return (f'<g transform="translate(-36 10) scale(.7) translate(50 20)">{_basket(a, "#A27B3C", 0)}</g><g transform="translate(36 10) scale(.7) translate(50 20)">{_basket(a, "#A27B3C", 0)}</g>'
                + f'<path d="M104 48 Q120 32 136 48" stroke="{b}" stroke-width="4" fill="none"/><path d="M132 40 l6 9 -10 1z" fill="{b}"/><path d="M136 128 Q120 142 104 128" stroke="{b}" stroke-width="4" fill="none"/><path d="M108 136 l-6-9 10-1z" fill="{b}"/>')
    if kind == "tag":
        return (f'<path d="M70 50 H130 L146 72 L130 94 H70 Z" fill="{a}"/><circle cx="132" cy="72" r="4" fill="{CR}"/><path d="M80 64 h38 M80 74 h30 M80 84 h34" stroke="{b}" stroke-width="2"/>'
                + f'<rect x="120" y="70" width="58" height="56" rx="3" fill="#FFFFFF" stroke="#E6DFD1" transform="rotate(6 149 98)"/><text x="150" y="92" font-size="9" text-anchor="middle" fill="{b}" font-family="Caveat, cursive" font-weight="700" transform="rotate(6 149 98)">Recipe</text><path d="M132 100 h34 M132 108 h28 M132 116 h30" stroke="#C9C2B6" stroke-width="1.5" transform="rotate(6 149 98)"/>')
    if kind == "twine":
        return (f'<rect x="70" y="60" width="100" height="62" rx="4" fill="#E9D9BC"/><path d="M70 90 H170 M120 60 V122" stroke="{b}" stroke-width="3"/><path d="M120 90 q-20-22-30-6 q10 10 30 6 q20-22 30-6 q-10 10-30 6" stroke="{b}" stroke-width="3" fill="none"/>'
                + f'<path d="M124 88 L150 50" stroke="#6E7A3A" stroke-width="2"/>' + "".join(f'<ellipse cx="150" cy="44" rx="4" ry="8" fill="{a}" transform="rotate({r} 150 50)"/>' for r in range(0, 360, 72)))
    if kind == "size":
        n = int(b); s = _basket(a, "#A27B3C", 0) if n == 4 else f'<g transform="translate(24 24) scale(.8)">{_basket(a, "#A27B3C", 0)}</g>'
        people = "".join(f'<circle cx="{40+k*14}" cy="104" r="5" fill="{INK}" fill-opacity=".7"/><path d="M{33+k*14} 126 q7-16 14 0z" fill="{INK}" fill-opacity=".7"/>' for k in range(n))
        return s + people
    if kind == "mix":
        return (f'<path d="M120 36 A50 50 0 0 1 120 136 Z" fill="{b}"/><path d="M120 36 A50 50 0 0 0 120 136 Z" fill="{a}"/><path d="M120 30 V142" stroke="{CR}" stroke-width="3"/>'
                + '<text x="96" y="92" font-size="10" text-anchor="middle" fill="#FFFFFF" font-family="Hind, sans-serif" font-weight="700">Fruit</text><text x="144" y="92" font-size="10" text-anchor="middle" fill="#FFFFFF" font-family="Hind, sans-serif" font-weight="700">Veg</text>')
    if kind == "note":
        return (f'<rect x="76" y="36" width="88" height="92" rx="4" fill="#FFFFFF" stroke="{a}" stroke-width="2"/><text x="120" y="56" font-size="11" text-anchor="middle" fill="{b}" font-family="Caveat, cursive" font-weight="700">Delivery Day</text>'
                + "".join(f'<rect x="86" y="{66+k*14}" width="8" height="8" rx="2" fill="none" stroke="{a}" stroke-width="1.5"/><path d="M100 {70+k*14} h{50-k*6}" stroke="#C9C2B6" stroke-width="2"/>' for k in range(4)))
    raise KeyError(kind)
def svg(i, cat, wash, kind, cols, tags):
    fid = f"fbw{i}"
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 150" width="240" height="150" style="max-width:100%;height:auto">'
         f'<defs><filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.06" numOctaves="3" seed="{i}"/>'
         f'<feDisplacementMap in="SourceGraphic" scale="14"/><feGaussianBlur stdDeviation="1.2"/></filter></defs>'
         f'<rect x="0" y="0" width="240" height="150" rx="12" fill="{KRAFT}"/><rect x="6" y="6" width="228" height="138" rx="8" fill="{CR}"/>'
         f'<g filter="url(#{fid})" opacity=".55"><ellipse cx="120" cy="84" rx="82" ry="46" fill="{wash}" fill-opacity=".35"/><ellipse cx="104" cy="96" rx="60" ry="30" fill="{wash}" fill-opacity=".3"/></g>')
    s += glyph(kind, cols, i)
    s += f'<text x="16" y="134" font-size="9" fill="{KRAFT_D}" font-family="Caveat, cursive" font-weight="700">The WellNest</text>'
    return s + '</svg>'
