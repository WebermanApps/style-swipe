"""Tools And Equipment Board Deck (Oct 19 2026, Max via UpKeep Develop 12:07 ICT): the board's own sections Tech Tool Bag,
Van Inventory Tracking and Ordering. Fields, layout and what each tracks. Every item is labelled TEST, Forecast or Decided.
The final tool list, van setup and suppliers are OPEN: shown as Open placeholders, generic category names only, no real tools,
brands or suppliers. Ordering never buys anything without Max's approval, and every ordering mockup shows that step.
18 this-or-that pairs, SAMPLE data only."""
from md1018_kit import make
from ukhf1019_kit import *
from ukhf1019_tech import TECH
BAG = [("Hand tools", "Good", "Oct 19", 0, "TEST"), ("Meters and testers", "Good", "Oct 18", 1, "TEST"), ("Safety gear", "Worn", "Oct 12", 7, "Forecast"),
       ("Ladders and access", "Good", "Oct 19", 0, "Decided"), ("Power tools", "Replace", "Oct 2", 17, "TEST")]
VAN = [("Filters", 3, 4, 10, "TEST"), ("Fasteners", 22, 10, 30, "TEST"), ("Sealants and tape", 2, 3, 8, "Forecast"),
       ("Plumbing parts", 7, 5, 12, "TEST"), ("Electrical parts", 4, 4, 10, "Decided"), ("Cleaning supplies", 9, 4, 10, "TEST")]
ORD = [("Filters restock", "Van 1", "Requested", "TEST"), ("Sealants and tape", "Van 2", "Needs Max's approval", "TEST"),
       ("Safety gear refresh", "Tech Dash 3", "Approved", "Forecast"), ("Fasteners", "Van 3", "Ordered", "TEST"), ("Cleaning supplies", "Van 1", "Received", "Decided")]
STEPS = ["Requested", "Needs Max's approval", "Approved", "Ordered", "Received"]
STC = {"Requested": LAGOON, "Needs Max's approval": TERRA, "Approved": JUNGLE, "Ordered": SAFF, "Received": MUTE}
CONC = {"Good": JUNGLE, "Worn": SAFF, "Replace": TERRA}
def openph(x, y, w, s="Open: final tool list", h=18):
    return R(x, y, w, h, WHITE, SAFF, 3, 1.1, 'stroke-dasharray="4 3"') + T(x + 8, y + h * .68, s, 8.5, SAFF, 700)
def cond(x, y, c, style="word"):
    if style == "word": return chip(x, y - 10, c, CONC[c], "soft", 7.5)[0]
    k = {"Good": 3, "Worn": 2, "Replace": 1}[c]
    return "".join(R(x + i * 9, y - 8, 7, 8, CONC[c] if i < k else "#E2DACB", rx=1.5) for i in range(3)) + T(x + 30, y, c, 8, INK, 500)
def lastc(x, y, d, n, style="date"):
    if style == "date": return T(x, y, d, 8.5, INK, 500)
    c = JUNGLE if n <= 3 else (SAFF if n <= 10 else TERRA)
    return chip(x, y - 10, ("Today" if n == 0 else f"{n} days ago"), c, "soft", 7.5)[0]
def bag_rows(y, o, rows=BAG, x0=24, w=404):
    full = o.get("fields", "full") == "full"; g = ""; yy = y
    if full: g += R(x0, yy, w, 16, SOFT) + "".join(T(xx, yy + 11, s, 7, MUTE, 700, extra='letter-spacing=".6"') for xx, s in ((x0 + 22, "CATEGORY"), (x0 + 170, "CONDITION"), (x0 + 250, "LAST CHECKED"), (x0 + 330, "LABEL"))); yy += 16
    for nm, c, d, n, lab in rows:
        g += check(x0 + 4, yy + 4, c == "Good") + T(x0 + 22, yy + 13, nm, 9.5, INK, 600) + cond(x0 + 170, yy + 13, c, o.get("cond", "word"))
        if full: g += lastc(x0 + 250, yy + 13, d, n, o.get("last", "date")) + (lab_chip(x0 + 330, yy + 3, lab, "soft", 7)[0] if o.get("lab", "end") == "end" else "")
        else: g += lab_chip(x0 + w - 50, yy + 3, lab, "soft", 7)[0]
        if o.get("lab") == "left": g = g  # left labels drawn by caller
        g += L(x0, yy + 19, x0 + w, yy + 19); yy += 20
    if o.get("ph", "row") == "row": g += openph(x0, yy + 3, w, "Open: final tool list per bag (not decided yet)"); yy += 24
    return g, yy - y
def bag_table(y, o):
    g = T(24, y + 10, "TECH DASH 1  ·  BAG CHECKLIST  ·  SAMPLE", 7.5, MUTE, 700, extra='letter-spacing="1"')
    if o.get("ph") == "banner": g += openph(24, y + 16, 404, "Open: the final tool list is not decided; categories only for now", 20); y += 24
    b, h = bag_rows(y + 16, o); return g + b, h + 18 + (24 if o.get("ph") == "banner" else 0)
def bag_techcar(y, o):
    g = ""; w = 196
    for i, (nm, c, van, area) in enumerate(TECH[:2]):
        x = 36 + i * (w + 8); g += R(x, y, w, 150, WHITE, LINE, 6) + R(x, y, w, 3, c) + T(x + 8, y + 17, nm + " bag", 11.5, INK, f="khand") + T(x + w - 8, y + 17, "4 of 5 good", 8, JUNGLE, 600, "end")
        yy = y + 26
        for nm2, cnd, d, n, lab in BAG:
            g += check(x + 8, yy + 2, cnd == "Good") + T(x + 23, yy + 11, nm2, 8.5, INK, 600) + cond(x + 98, yy + 11, cnd, "word") + lab_chip(x + 146, yy + 2, lab, "soft", 6)[0]; yy += 18
        g += openph(x + 8, yy + 2, w - 16, "Open: final tool list", 16)
    g += R(14, y, 20, 150, WHITE) + f'<path d="M28 {y+71} l-4 4 l4 4" fill="none" stroke="{INK}" stroke-width="1.5"/>' + C(26, y + 75, 9, "none", LINE)
    g += C(430, y + 75, 9, WHITE, INK) + chev(430, y + 75, INK, False) + "".join(R(206 + i * 12, y + 156, 8 if i == 0 else 5, 4, TERRA if i == 0 else "#D6D0C6", rx=2) for i in range(3))
    return g, 166
CATS = [("Hand tools", "5 of 5 checked", "TEST"), ("Meters and testers", "2 of 3 checked", "TEST"), ("Safety gear", "1 worn", "Forecast"), ("Ladders and access", "All good", "Decided"), ("Power tools", "1 to replace", "TEST")]
def cat_carousel(y, cats=CATS, title="BAG CATEGORIES"):
    g = T(24, y + 10, title + "  ·  SAMPLE", 7.5, MUTE, 700, extra='letter-spacing="1"'); x = 40
    for nm, sm, lab in cats[:4]:
        g += R(x, y + 18, 118, 74, WHITE, LINE, 6) + R(x, y + 18, 118, 3, LAGOON) + R(x + 8, y + 28, 28, 22, CREAM, LINE, 3) + T(x + 44, y + 42, nm, 9.5, INK, f="khand")
        g += T(x + 8, y + 66, sm, 8.5, INK, 500) + lab_chip(x + 8, y + 72, lab, "soft", 7)[0]; x += 124
    g += R(430, y + 16, 22, 80, WHITE) + R(14, y + 16, 24, 80, WHITE) + C(26, y + 55, 9, WHITE, LINE) + f'<path d="M28 {y+51} l-4 4 l4 4" fill="none" stroke="{INK}" stroke-width="1.5"/>' + C(430, y + 55, 9, WHITE, INK) + chev(430, y + 55, INK, False)
    g += "".join(R(206 + i * 12, y + 98, 8 if i == 0 else 5, 4, TERRA if i == 0 else "#D6D0C6", rx=2) for i in range(3))
    return g, 108
def cat_folds(y, cats=CATS, open_first=True):
    g = ""; yy = y
    for i, (nm, sm, lab) in enumerate(cats):
        if i == 0 and open_first:
            rows = [r for r in BAG if r[0] == nm] + [("Open item slot", "Good", "Oct 19", 0, "TEST")]
            b, h = bag_rows(yy + 24, {"fields": "lean", "ph": None}, rows[:1], 30, 392)
            g += fold(yy, nm, None, True, h + 30, right=sm + "  ·  " + lab, rcol=INK, x=24, w=404, h=22, size=11.5) + b + openph(30, yy + 26 + h, 392, "Open: items in this category", 16); yy += h + 58
        else: g += fold(yy, nm, None, False, right=sm + "  ·  " + lab, x=24, w=404, h=22, size=11.5); yy += 26
    return g, yy - y
def van_table(y, o, rows=VAN):
    g = R(24, y, 404, 16, SOFT) + "".join(T(xx, y + 11, s, 7, MUTE, 700, extra='letter-spacing=".6"') for xx, s in ((30, "CATEGORY"), (150, "IN VAN"), (200, "MIN"), (240, "PAR"), (290, "STOCK"), (380, "LABEL"))); yy = y + 16
    for nm, st, mn, par, lab in rows:
        low = st < mn; at = st == mn
        if low and o.get("low", "tint") == "tint": g += R(24, yy, 404, 20, TERRA + "10") + R(24, yy, 3, 20, TERRA)
        g += T(30, yy + 13, nm, 9.5, INK, 600)
        if o.get("view", "num") == "num":
            g += T(150, yy + 13, str(st), 10, TERRA if low else INK, 700) + T(200, yy + 13, str(mn), 9, MUTE) + T(240, yy + 13, str(par), 9, MUTE)
        else:
            bx, bw = 150, 200; g += R(bx, yy + 7, bw, 7, "#EEE8DE", rx=3) + R(bx, yy + 7, bw * min(st / par, 1), 7, TERRA if low else (SAFF if at else JUNGLE), rx=3)
            g += L(bx + bw * mn / par, yy + 4, bx + bw * mn / par, yy + 17, INK, 1.4) + T(bx + bw + 4, yy + 14, f"{st}/{par}", 8, INK, 600)
        if o.get("view", "num") == "num":
            if low: g += (chip(290, yy + 3, "Low", TERRA, "solid", 7.5)[0] if o.get("low", "tint") == "tint" else warn(290, yy + 4, TERRA, 11) + T(304, yy + 13, "Below min", 8.5, TERRA, 700))
            elif at: g += chip(290, yy + 3, "At min", SAFF, "soft", 7.5)[0]
            else: g += chip(290, yy + 3, "OK", JUNGLE, "dot", 8)[0]
        g += lab_chip(380, yy + 3, lab, "soft", 7)[0] + L(24, yy + 20, 428, yy + 20); yy += 20
    if o.get("view") == "bar": g += T(150, yy + 11, "Bar = stock against par  ·  black tick = min", 7.5, MUTE)
    yy += 14
    g += openph(24, yy, 404, "Open: van setup and final stock list (categories only for now)"); yy += 22
    return g, yy - y
def van_car(y, o):
    g = ""; w = 196
    for i, (nm, c, van, area) in enumerate(TECH[:2]):
        x = 36 + i * (w + 8); g += R(x, y, w, 150, WHITE, LINE, 6) + R(x, y, w, 3, c) + T(x + 8, y + 17, f"{van}  ·  {nm}", 11, INK, f="khand") + chip(x + w - 52, y + 6, "2 low" if i == 0 else "OK", TERRA if i == 0 else JUNGLE, "soft", 7.5)[0]; yy = y + 26
        for nm2, st, mn, par, lab in VAN:
            low = st < mn and i == 0; g += T(x + 8, yy + 11, nm2, 8.5, INK, 600) + R(x + 100, yy + 5, 60, 6, "#EEE8DE", rx=3) + R(x + 100, yy + 5, 60 * min((st if i == 0 else par - 1) / par, 1), 6, TERRA if low else JUNGLE, rx=3) + T(x + w - 8, yy + 11, f"{st if i == 0 else par-1}/{par}", 8, TERRA if low else INK, 600, "end"); yy += 17
        g += openph(x + 8, yy + 4, w - 16, "Open: van setup", 16)
    g += R(14, y, 20, 150, WHITE) + C(26, y + 75, 9, WHITE, LINE) + f'<path d="M28 {y+71} l-4 4 l4 4" fill="none" stroke="{INK}" stroke-width="1.5"/>' + C(430, y + 75, 9, WHITE, INK) + chev(430, y + 75, INK, False)
    return g + "".join(R(206 + i * 12, y + 156, 8 if i == 0 else 5, 4, TERRA if i == 0 else "#D6D0C6", rx=2) for i in range(3)), 166
def van_folds(y, o):
    g = ""; yy = y
    for i, (nm, c, van, area) in enumerate(TECH):
        if i == 0:
            b, h = van_table(yy + 26, {"view": "num"}, VAN[:4]); g += fold(yy, f"{van}  ·  {nm}", None, True, h + 6, right="2 below min  ·  1 at min  ·  TEST", rcol=TERRA, x=24, w=404, h=22, size=11.5) + b; yy += h + 34
        else: g += fold(yy, f"{van}  ·  {nm}", None, False, right=("All at or above min  ·  TEST" if i == 1 else "1 below min  ·  Forecast"), x=24, w=404, h=22, size=11.5); yy += 26
    return g, yy - y
VCATS = [("Filters", "1 below min", "TEST"), ("Fasteners", "All good", "TEST"), ("Sealants and tape", "1 below min", "Forecast"), ("Plumbing parts", "All good", "TEST"), ("Electrical parts", "At min", "Decided")]
def van_chips(y, o):
    g = ""; x = 24
    for i, s in enumerate(["All categories", "Filters", "Fasteners", "Sealants and tape", "Plumbing parts"]):
        gg, w = chip(x, y, s, LAGOON if i == 0 else MUTE, "solid" if i == 0 else "outline", 8); g += gg; x += w + 5
    b, h = van_table(y + 24, {"view": "num"}, VAN[:5]); return g + b, h + 24
def approval_banner(y):
    return R(24, y, 404, 22, TERRA + "12", TERRA + "77", 3) + lock(32, y + 4) + T(48, y + 15, "Nothing is bought without Max's approval. Approve happens here, then the order is placed.", 8.5, TERRA, 700), 28
def stchip(x, y, s, style="word"):
    if style == "word": return chip(x, y - 10, s, STC[s], "solid" if s == "Needs Max's approval" else "soft", 7.5)[0]
    k = STEPS.index(s); g = ""
    for i in range(5): g += C(x + 5 + i * 16, y - 4, 4, STC[STEPS[i]] if i <= k else WHITE, STC[STEPS[i]] if i <= k else "#CFC6B6", 1.2) + (L(x + 9 + i * 16, y - 4, x + 17 + i * 16, y - 4, "#CFC6B6") if i < 4 else "")
    return g + T(x + 84, y, {"Needs Max's approval": "Max to approve"}.get(s, s), 7.5, STC[s], 700)
def ord_table(y, o):
    g = ""
    if o.get("banner", True): b, h = approval_banner(y); g += b; y += h
    g += R(24, y, 404, 16, SOFT) + "".join(T(xx, y + 11, s, 7, MUTE, 700, extra='letter-spacing=".6"') for xx, s in ((30, "REQUEST"), (130, "FOR"), (190, "STATUS"), (318, "SUPPLIER"), (356, "COST"), (388, "LABEL"))); yy = y + 16
    for nm, fr, st, lab in ORD:
        need = st == "Needs Max's approval"
        if need: g += R(24, yy, 404, 22, TERRA + "0D") + R(24, yy, 3, 22, TERRA)
        g += T(30, yy + 14, nm, 9, INK, 600) + T(130, yy + 14, fr, 8.5, MUTE) + stchip(190, yy + 14, st, o.get("status", "word"))
        if o.get("sup", "inline") == "inline": g += T(318, yy + 14, "Open", 8.5, SAFF, 700) + T(356, yy + 14, "Open", 8.5, SAFF, 700)
        else: g += T(318, yy + 14, "-", 8.5, MUTE) + T(356, yy + 14, "-", 8.5, MUTE)
        g += lab_chip(388, yy + 4, lab, "soft", 6.5)[0] + L(24, yy + 22, 428, yy + 22); yy += 22
    if o.get("sup") == "fold":
        g += fold(yy + 6, "Supplier And Cost (Open)", None, False, right="Placeholders until suppliers are chosen", x=24, w=404, h=22, size=11); yy += 30
    return g, yy - y + 4 + (28 if o.get("banner", True) else 0)
def ord_lanes(y, o):
    g = ""
    if o.get("banner", True): b, h = approval_banner(y); g += b; y += h
    w = 78
    for i, s in enumerate(STEPS):
        x = 24 + i * (w + 3.5); c = STC[s]; g += R(x, y, w, 150, CREAM if s != "Needs Max's approval" else TERRA + "10", LINE if s != "Needs Max's approval" else TERRA, 4, 1.1) + R(x, y, w, 3, c)
        g += T(x + 6, y + 15, s if len(s) < 14 else "Needs Max's", 8.5, c, 700) + (T(x + 6, y + 25, "approval", 8.5, c, 700) if len(s) >= 14 else "")
        for nm, fr, st, lab in [r for r in ORD if r[2] == s]:
            g += R(x + 4, y + 32, w - 8, 56, WHITE, LINE, 4) + T(x + 9, y + 46, nm[:15], 8, INK, 600) + T(x + 9, y + 58, fr, 7.5, MUTE) + lab_chip(x + 9, y + 64, lab, "soft", 6.5)[0]
            if s == "Needs Max's approval": g += lock(x + w - 20, y + 66)
    return g, 158 + (28 if o.get("banner", True) else 0)
def approve_card(y):
    g = R(24, y, 404, 92, WHITE, TERRA, 6, 1.4) + R(24, y, 404, 22, TERRA + "14", rx=6) + T(34, y + 15, "NEEDS MAX'S APPROVAL  ·  SAMPLE", 9.5, TERRA, f="khand", extra='letter-spacing="1.2"')
    g += T(34, y + 38, "Sealants and tape for Van 2  ·  qty Open  ·  supplier Open  ·  cost Open", 9, INK, 600) + T(34, y + 52, "Why: below min (2 of min 3)  ·  requested by Tools Agent  ·  TEST", 8.5, MUTE)
    g += R(34, y + 62, 92, 22, JUNGLE, rx=3) + T(80, y + 77, "Approve (Max only)", 8.5, WHITE, 700, "middle") + R(132, y + 62, 60, 22, WHITE, MUTE, 3) + T(162, y + 77, "Decline", 8.5, INK, 600, "middle")
    g += T(418, y + 77, "No order is placed until approved", 8, TERRA, 600, "end")
    return g, 100
def ord_approve(y, o):
    if o.get("ap") == "card":
        b, h = approve_card(y); g = b; yy = y + h
        for nm, fr, st, lab in ORD:
            if st == "Needs Max's approval": continue
            g += T(30, yy + 13, nm, 9, INK, 600) + T(130, yy + 13, fr, 8.5, MUTE) + stchip(190, yy + 13, st) + lab_chip(390, yy + 3, lab, "soft", 7)[0] + L(24, yy + 19, 428, yy + 19); yy += 20
        return g, yy - y + 4
    return ord_table(y, {"banner": True})
def ord_form(y, o):
    if o.get("form") == "quick":
        g = R(24, y, 330, 24, WHITE, "#CFC6B6", 12) + T(36, y + 16, "Add a request: category, van or tech, why", 9, MUTE) + R(360, y, 68, 24, LAGOON, rx=12) + T(394, y + 16, "Request", 9.5, WHITE, 700, "middle")
        g += T(24, y + 38, "Goes in as Requested, then waits for Max's approval. Supplier and cost stay Open.", 8.5, MUTE); b, h = ord_table(y + 46, {"banner": False}); return g + b, h + 46
    g = R(24, y, 404, 120, WHITE, LINE, 6) + T(34, y + 16, "NEW ORDER REQUEST  ·  SAMPLE", 8.5, MUTE, 700, extra='letter-spacing="1"')
    F = [("Category", "Sealants and tape", 34, 30), ("For van or tech", "Van 2", 230, 30), ("Quantity", "Open", 34, 62), ("Why", "Below min", 230, 62), ("Supplier", "Open", 34, 94), ("Cost", "Open", 230, 94)]
    for k, v, x, yy in F:
        op = v == "Open"; g += T(x, y + yy - 2, k, 7.5, MUTE, 600) + R(x, y + yy + 2, 184, 18, WHITE, SAFF if op else "#CFC6B6", 3, 1, 'stroke-dasharray="3 2"' if op else "") + T(x + 6, y + yy + 15, v, 9, SAFF if op else INK, 700 if op else 500)
    g += R(24, y + 126, 404, 22, TERRA + "10", rx=3) + lock(32, y + 130) + T(48, y + 141, "Submit sends it to Max for approval. Nothing is bought until he approves.", 8.5, TERRA, 700)
    return g, 154
def low_to_order(y, o):
    if o.get("flow") == "btn":
        g = ""; yy = y
        for nm, st, mn, par, lab in VAN[:4]:
            low = st < mn; g += (R(24, yy, 404, 24, TERRA + "0D") if low else "") + T(30, yy + 15, nm, 9.5, INK, 600) + T(160, yy + 15, f"{st} in van  ·  min {mn}  ·  par {par}", 8.5, TERRA if low else MUTE, 600 if low else 400)
            if low: g += R(330, yy + 3, 92, 18, WHITE, LAGOON, 9, 1.2) + T(376, yy + 15.5, "Request order", 8.5, LAGOON, 700, "middle")
            g += L(24, yy + 24, 428, yy + 24); yy += 24
        g += T(24, yy + 14, "Request order adds a line to Ordering as Requested; Max approves before anything is bought.", 8, MUTE); return g, yy - y + 22
    b, h = approval_banner(y); g = b; yy = y + h + 2
    g += T(24, yy + 10, "DRAFTED BY THE TOOLS AGENT FROM LOW STOCK  ·  TEST", 7.5, MUTE, 700, extra='letter-spacing="1"'); yy += 16
    for nm, st, mn, par, lab in [v for v in VAN if v[1] < v[2]]:
        g += R(24, yy, 404, 30, WHITE, TERRA + "88", 4) + lock(32, yy + 8) + T(48, yy + 13, f"{nm}  ·  Van 1  ·  top up to par {par}", 9, INK, 600) + T(48, yy + 25, f"{st} in van, min {mn}  ·  supplier Open  ·  cost Open", 8, MUTE) + stchip(318, yy + 19, "Needs Max's approval")
        yy += 36
    return g, yy - y
SECS = [("bag", "Tech Tool Bag", "3 bags  ·  1 item worn  ·  1 to replace"), ("van", "Van Inventory Tracking", "3 vans  ·  2 below min"), ("ord", "Ordering", "5 requests  ·  1 needs Max's approval")]
def board(open_=None, body=None, tiles=False, o=None):
    g, y = mini_header("Tools And Equipment Command Center")
    s, h = mini_folds(y, [("Emergency Alerts", 0, False), ("To-Do List", 2, False), ("Documents Center", 1, False)]); g += s; y += h
    if tiles:
        for i, (big, sm, c) in enumerate((("1 worn", "Tech Tool Bag", SAFF), ("2 low", "Van Inventory", TERRA), ("1 waiting", "Max's approval", TERRA))):
            x = 14 + i * 144; g += R(x, y, 136, 46, CREAM, LINE, 6) + T(x + 10, y + 24, big, 17, c, f="khand") + T(x + 10, y + 38, sm, 8.5, MUTE, 600)
        y += 54
    for key, title, summ in SECS:
        if key == open_:
            b, bh = body(y + 30, o or {}); g += fold(y, title, None, True, bh + 10, right=summ, rcol=INK) + b; y += bh + 40
        else: g += fold(y, title, None, False, right=summ); y += 30
    g += fold(min(max(y, 410), 420), "Ping Record", 3, False, right="In the branded footer", h=20, size=11)
    return g + bym(452)
def T_TOOLS():
    pairs, P = make("uktb19_", "UpKeep"); F = lambda s, n: frame(s, n, "tools-equipment board", "TEST  ·  SAMPLE"); LOC = "Tools And Equipment Board"
    P("Board", LOC, "Board overview", "should the three sections open as folds with one-line summaries or add count tiles above them?",
      ("folds", "Folds With Summaries", "Tech Tool Bag, Van Inventory, Ordering, a line each.", "calm", F(board(), "Folds only")),
      ("tiles", "Count Tiles Above", "Worn, low and waiting-for-Max tiles on top.", "glanceable", F(board(tiles=True), "Count tiles")))
    P("Tech Tool Bag", LOC, "Bag layout", "should the tool bags be one checklist per tech or a carousel with a card per tech?",
      ("table", "Checklist Per Tech", "One bag at a time as a checklist table.", "focused", F(board("bag", bag_table), "Checklist table")),
      ("car", "Carousel, Card Per Tech", "Slide between Tech Dash 1-3 bag cards.", "visual", F(board("bag", bag_techcar), "Tech carousel")))
    P("Tech Tool Bag", LOC, "Bag categories", "should tool categories be a carousel of cards or dropdowns with a one-line summary each?",
      ("car", "Category Carousel", "Hand tools, meters, safety gear, ladders as cards.", "visual", F(board("bag", lambda y, o: cat_carousel(y)), "Category carousel")),
      ("folds", "Dropdown Per Category", "Each category a fold with its summary line.", "tidy", F(board("bag", lambda y, o: cat_folds(y)), "Category dropdowns")))
    P("Tech Tool Bag", LOC, "Bag fields", "should each bag row show just the item and condition or also last checked and a label?",
      ("lean", "Item And Condition", "Check, category, condition and label.", "calm", F(board("bag", bag_table, o={"fields": "lean"}), "Lean row")),
      ("full", "Plus Last Checked", "Adds a last checked column and a label column.", "complete", F(board("bag", bag_table, o={"fields": "full"}), "Full row")))
    P("Tech Tool Bag", LOC, "Condition display", "should condition be a Good, Worn or Replace word chip or a three-block meter?",
      ("word", "Word Chip", "Green Good, gold Worn, terracotta Replace.", "clear", F(board("bag", bag_table, o={"cond": "word"}), "Word chip")),
      ("meter", "Three-Block Meter", "Three small blocks fill with condition.", "visual", F(board("bag", bag_table, o={"cond": "meter"}), "Block meter")))
    P("Tech Tool Bag", LOC, "Last checked", "should last checked show the date or a days-ago chip that turns terracotta when overdue?",
      ("date", "Plain Date", "Oct 19, Oct 12, Oct 2.", "precise", F(board("bag", bag_table, o={"last": "date"}), "Date")),
      ("ago", "Days-Ago Chip", "Today, 7 days ago, 17 days ago in warning colours.", "glanceable", F(board("bag", bag_table, o={"last": "ago"}), "Days-ago chip")))
    P("Tech Tool Bag", LOC, "Open placeholder", "while the tool list is undecided, should Open show as a dashed row in the list or a banner on top?",
      ("row", "Dashed Open Row", "A dashed gold row at the end of the list.", "subtle", F(board("bag", bag_table, o={"ph": "row"}), "Open row")),
      ("banner", "Open Banner On Top", "A dashed gold banner over the list.", "clear", F(board("bag", bag_table, o={"ph": "banner"}), "Open banner")))
    P("Van Inventory", LOC, "Stock levels", "should van stock show numbers with min and par columns or bars against par with a min tick?",
      ("num", "Numbers, Min, Par", "In van, min and par as numbers.", "precise", F(board("van", van_table, o={"view": "num"}), "Numbers")),
      ("bar", "Bars Against Par", "A bar to par with a tick at min.", "visual", F(board("van", van_table, o={"view": "bar"}), "Bars")))
    P("Van Inventory", LOC, "Van grouping", "should each van be a card in a carousel or a dropdown with a one-line summary?",
      ("car", "Van Carousel", "Slide between Van 1-3 cards with stock bars.", "visual", F(board("van", van_car), "Van carousel")),
      ("folds", "Dropdown Per Van", "Each van a fold, 2 below min on the line.", "tidy", F(board("van", van_folds), "Van dropdowns")))
    P("Van Inventory", LOC, "Low-stock flag", "should low stock be a tinted row with a Low chip or a warning sign with Below min?",
      ("tint", "Tinted Row, Low Chip", "Terracotta tint and edge, solid Low chip.", "bold", F(board("van", van_table, o={"low": "tint"}), "Tinted row")),
      ("icon", "Warning Sign, Below Min", "No tint, a small warning and Below min.", "subtle", F(board("van", van_table, o={"low": "icon"}), "Warning sign")))
    P("Van Inventory", LOC, "Van categories", "should van stock categories be a carousel of cards or filter chips over one list?",
      ("car", "Category Carousel", "Filters, fasteners, sealants as cards.", "visual", F(board("van", lambda y, o: cat_carousel(y, VCATS, "VAN 1 CATEGORIES")), "Category carousel")),
      ("chips", "Filter Chips Over List", "Chips narrow the van stock table.", "quick", F(board("van", van_chips), "Filter chips")))
    P("Ordering", LOC, "Order list", "should order requests be a table with a status column or lanes for each status?",
      ("table", "Table With Status", "One row per request, status in a column.", "compact", F(board("ord", ord_table), "Table")),
      ("lanes", "Status Lanes", "Requested to Received as five lanes.", "visual", F(board("ord", ord_lanes), "Lanes")))
    P("Ordering", LOC, "Order status", "should order status be a coloured word chip or a five-step tracker?",
      ("word", "Word Chip", "Requested, Needs Max's approval, Approved, Ordered, Received.", "simple", F(board("ord", ord_table, o={"status": "word"}), "Word chip")),
      ("steps", "Five-Step Tracker", "Five dots fill as the order moves along.", "guided", F(board("ord", ord_table, o={"status": "steps"}), "Step tracker")))
    P("Ordering", LOC, "Max approval step", "should the approval step be an Approve card for Max on top or a locked row under a banner?",
      ("card", "Approve Card On Top", "A terracotta card with Approve (Max only) and Decline.", "clear", F(board("ord", ord_approve, o={"ap": "card"}), "Approve card")),
      ("lock", "Locked Row And Banner", "A lock on the row and a no-buy banner above.", "calm", F(board("ord", ord_approve, o={"ap": "lock"}), "Locked row")))
    P("Ordering", LOC, "Supplier and cost", "should supplier and cost be Open placeholders in each row or tucked into one Open fold?",
      ("inline", "Open In Each Row", "Supplier Open and Cost Open on every request.", "honest", F(board("ord", ord_table, o={"sup": "inline"}), "Open in rows")),
      ("fold", "One Open Fold", "Rows stay clean, one Supplier and Cost fold.", "tidy", F(board("ord", ord_table, o={"sup": "fold"}), "Open fold")))
    P("Ordering", LOC, "New request", "should a new order request be a short form or a one-line quick add?",
      ("form", "Short Form", "Category, van or tech, quantity, why, supplier, cost.", "complete", F(board("ord", ord_form, o={"form": "form"}), "Short form")),
      ("quick", "One-Line Quick Add", "Type it in one line, the rest stays Open.", "fast", F(board("ord", ord_form, o={"form": "quick"}), "Quick add")))
    P("Ordering", LOC, "Low stock to order", "should low stock get a Request order button or auto-drafted requests waiting for Max?",
      ("btn", "Request Order Button", "A button on each low row adds a request.", "manual", F(board("van", low_to_order, o={"flow": "btn"}), "Request button")),
      ("auto", "Drafted, Waiting For Max", "The agent drafts the request; it waits, locked, for Max.", "assisted", F(board("ord", low_to_order, o={"flow": "auto"}), "Drafted requests")))
    P("Labels", LOC, "Item labels", "should the TEST, Forecast and Decided label be a soft pill or an outlined capital tag?",
      ("soft", "Soft Pill", "Pale grey, lagoon or jungle pill.", "friendly", F(board("van", van_table, o={}), "Soft pill")),
      ("caps", "Outlined Capital Tag", "A boxed capital stamp.", "formal", board_caps()))
    return pairs
def board_caps():
    import ukhf1019_kit as K
    old = K.lab_chip
    def caps(x, y, s, style="soft", size=8): return old(x, y, s, "caps", size)
    globals()["lab_chip"] = caps
    try: return frame(board("van", van_table, o={}), "Outlined tag", "tools-equipment board", "TEST  ·  SAMPLE")
    finally: globals()["lab_chip"] = old
