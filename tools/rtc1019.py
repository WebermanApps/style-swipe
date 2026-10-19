"""Tech Certs, Training And Cool Tech follow-up deck (Research spec /workspace/ops/research/2026-10-19-tech-certs-followup-deck.json, Oct 19 2026).
Swatch draws the visuals from each option's visual_brief: light cream #FAF6EE, gold #b08a3e, Khand/Hind, no emoji, TEST / SAMPLE data.
People are illustrated, healthy-looking techs (never real people); badges are plain lagoon pills with words, never real cert logos."""
import json, re
from md1018_kit import make
from mcd1019 import T, R, C, L, INK, MUTE, LINE, WHITE, TERRA, LAGOON, JUNGLE
from draft_svg import screen
CREAM = "#FAF6EE"; GOLD = "#b08a3e"; GREY = "#9A948A"
SPEC = "/workspace/ops/research/2026-10-19-tech-certs-followup-deck.json"
def card(inner, note):
    return screen(f'<g transform="scale(.5)">{R(0,0,480,600,CREAM)}{inner}'
                  f'{R(18,14,120,26,WHITE,"#B9AE9C",4,1.4,chr(39)[:0]+"stroke-dasharray=\"4 3\"")}{T(78,32,"TEST · SAMPLE",12,MUTE,700,"middle")}'
                  f'{R(0,556,480,44,WHITE)}{L(0,556,480,556,"#E8E0D2")}{T(240,584,note,17,INK,600,"middle")}</g>', CREAM)
def tech(cx, cy, s=1, shirt=LAGOON, skin="#E3B48F", hair="#4A3424"):
    """Illustrated healthy tech: round friendly face, rosy cheeks, cap, work shirt. Not a real person."""
    return (f'<g transform="translate({cx},{cy}) scale({s})">' + C(0, 40, 34, shirt) + R(-34, 40, 68, 34, shirt)
            + C(0, 0, 24, skin) + f'<path d="M-24 -4 q24 -30 48 0 v-6 q-24 -22 -48 0z" fill="{hair}"/>' + R(-26, -14, 52, 8, GOLD, rx=4)
            + C(-8, 2, 2.4, INK) + C(8, 2, 2.4, INK) + C(-14, 9, 4, "#F2A08A") + C(14, 9, 4, "#F2A08A")
            + f'<path d="M-7 12 q7 6 14 0" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>' + R(-6, 48, 12, 8, WHITE, rx=2) + "</g>")
def badge(x, y, s, grey=False):
    c = GREY if grey else LAGOON; w = len(s) * 7.2 + 24
    return R(x, y, w, 24, c + "1A", c, 12, 1.3) + C(x + 12, y + 12, 4, c) + T(x + 21, y + 16.5, s, 11.5, c, 600), w
def profile(badges, extra=""):
    g = R(40, 70, 400, 420, WHITE, LINE, 14) + tech(110, 140, 1.1) + T(170, 136, "Tech Dash 1", 24, INK, f="khand") + T(170, 160, "TEST profile  ·  North area", 12, MUTE)
    x, y = 70, 230
    for b in badges:
        grey = b.startswith("~"); s, w = badge(x, y, b.lstrip("~"), grey)
        if x + w > 420: x, y = 70, y + 34; s, w = badge(x, y, b.lstrip("~"), grey)
        g += s; x += w + 10
    g += T(70, y + 52, "Valid until dates shown on tap  ·  SAMPLE", 11, MUTE)
    return g + "".join(R(70, 330 + i * 22, 340 - i * 40, 8, "#EEE7DB", rx=4) for i in range(4)) + extra
CERTS = [("First Aid", .3, .85, 14), ("Lead-Safe", .55, .7, 18), ("OSHA 10", .7, .5, 16), ("Bkgd Check", .2, .95, 12), ("HVAC Core", .85, .35, 24), ("Backflow", .6, .25, 20)]
def bubbles(names):
    g = R(40, 70, 400, 420, WHITE, LINE, 10) + L(80, 440, 80 if names else 80, 100, INK, 1.5) + L(80, 440, 420 if names else 330, 440, INK, 1.5)
    g += T(90, 462, "Skill  →", 12, MUTE, 600) + T(60, 120, "Love", 12, MUTE, 600, extra='transform="rotate(-90 60 120)"')
    xw = 340 if names else 250
    for i, (n, sx, sy, r) in enumerate(CERTS):
        cx, cy = 80 + sx * xw, 440 - sy * 330
        g += C(cx, cy, r, GOLD + "55", GOLD, 1.5) + (T(cx + r + 4, cy + 4, n, 11, INK, 600) if names else T(cx, cy + 4, str(i + 1), 12, INK, 700, "middle"))
    if not names: g += R(340, 110, 90, 200, CREAM, LINE, 6) + "".join(T(350, 132 + i * 30, f"{i+1}  {n}", 10.5, INK, 500) for i, (n, *_) in enumerate(CERTS))
    return g + T(240, 520, "Bubble size = SAMPLE cost", 11, MUTE, 500, "middle")
def receipt(back):
    rows = (("OSHA 10", "$89"), ("Lead-Safe RRP", "$249"), ("First Aid / CPR", "$95"), ("HVAC entry test", "$150"))
    g = R(110, 70, 260, 400, WHITE, LINE, 4) + T(240, 104, "CERT RECEIPT  ·  SAMPLE", 13, MUTE, 700, "middle") + L(130, 116, 350, 116, LINE)
    for i, (a, b) in enumerate(rows): g += T(130, 146 + i * 30, a, 13, INK, 500) + T(350, 146 + i * 30, b, 13, INK, 600, "end")
    g += L(130, 270, 350, 270, INK) + T(130, 294, "Total", 15, INK, f="khand") + T(350, 294, "$583", 15, INK, f="khand", anchor="end") + T(240, 316, "SAMPLE prices, see sources", 10, MUTE, 500, "middle")
    if back:
        g += R(150, 340, 70, 60, WHITE, GOLD, 4, 1.5) + R(150, 340, 70, 16, GOLD) + T(185, 384, "90", 22, INK, f="khand", anchor="middle") + T(185, 396, "days", 9, MUTE, 500, "middle")
        g += f'<g transform="rotate(-10 300 380)">{R(240, 356, 120, 40, "none", JUNGLE, 6, 3)}{T(300, 383, "REIMBURSED", 15, JUNGLE, 700, "middle")}</g>'
    else: g += f'<g transform="rotate(-10 240 380)">{R(150, 352, 180, 46, "none", JUNGLE, 6, 3)}{T(240, 375, "PAID BY", 12, JUNGLE, 700, "middle")}{T(240, 391, "SMART UPKEEP", 13, JUNGLE, 700, "middle")}</g>'
    return g
def gauge(cx, cy, r, frac, col, label):
    import math
    a = math.pi * (1 - frac); x2, y2 = cx + r * math.cos(a), cy - r * math.sin(a)
    return (f'<path d="M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="#EEE7DB" stroke-width="12"/>'
            f'<path d="M{cx-r} {cy} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="12"/>' + T(cx, cy + 24, label, 12, MUTE, 600, "middle"))
def item(name, sub, extra):
    return R(60, 80, 360, 400, WHITE, LINE, 12) + R(90, 110, 300, 130, "#F3EEE4", rx=8) + T(240, 182, "SAMPLE PHOTO", 12, GREY, 700, "middle") + T(90, 276, name, 22, INK, f="khand") + T(90, 298, sub, 12, MUTE) + extra
def calendar(sat):
    g = R(40, 70, 400, 420, WHITE, LINE, 10) + T(60, 100, "Tech Study Month  ·  TEST", 16, INK, f="khand")
    for j, d in enumerate("MTWTFSS"): g += T(78 + j * 52, 126, d, 12, MUTE, 700, "middle")
    for w in range(4):
        for j in range(7):
            x, y = 54 + j * 52, 136 + w * 76; wk = j >= 5
            g += R(x, y, 48, 70, "#F1EEE8" if wk else CREAM, LINE, 4)
            if not wk: g += R(x + 6, y + 30, 36, 8, GOLD + "66", rx=4)
            if sat and j == 5: g += R(x + 4, y + 26, 40, 18, GOLD, rx=9) + T(x + 24, y + 39, "Review", 9, WHITE, 700, "middle")
    return g
def phone(n):
    g = R(150, 60, 180, 430, WHITE, INK, 24, 2) + R(170, 100, 140, 200, CREAM, LINE, 10) + T(240, 160, "QUIZ", 13, GOLD, 700, "middle") + T(240, 196, "Which meter checks", 13, INK, 600, "middle") + T(240, 214, "for CO?", 13, INK, 600, "middle")
    g += R(176, 312, 64, 30, WHITE, LINE, 6) + R(244, 312, 64, 30, WHITE, LINE, 6) + T(208, 332, "A", 13, INK, 600, "middle") + T(276, 332, "B", 13, INK, 600, "middle")
    return g + T(240, 380, f"1 of {n}", 16, INK, f="khand", anchor="middle") + T(240, 402, "about " + ("3" if n == 5 else "6") + " minutes", 11, MUTE, 500, "middle")
def agenda(kind):
    g = R(60, 70, 360, 420, WHITE, LINE, 12)
    if kind == "warm":
        g += T(80, 104, "Tuesday morning  ·  TEST", 16, INK, f="khand") + R(80, 120, 320, 44, GOLD + "22", GOLD, 6) + T(94, 147, "Warm-up: 3 missed cards", 14, INK, 600)
        rows = ("Vans and safety check", "Day two topic", "Ride-along", "Quiz deck")
        for i, r in enumerate(rows): g += T(94, 200 + i * 40, r, 13, INK) + L(80, 212 + i * 40, 400, 212 + i * 40, LINE)
    else:
        g += T(80, 104, "Monday, end of day  ·  TEST", 16, INK, f="khand") + T(240, 190, "8 / 10", 48, INK, f="khand", anchor="middle") + T(240, 214, "quiz score", 12, MUTE, 500, "middle")
        g += R(80, 250, 320, 60, CREAM, GOLD, 8, 1.5) + tech(120, 266, .5) + T(160, 276, "5-minute review with Max", 14, INK, 600) + T(160, 294, "Talk through the 2 misses", 11, MUTE)
    return g + tech(380, 430, .7, JUNGLE, "#C98E66", "#2E2118")
def laptop(kind):
    g = R(60, 100, 360, 230, INK, rx=10) + R(70, 110, 340, 210, WHITE) + f'<path d="M30 330 h420 l-20 24 h-380z" fill="#CFC6B6"/>'
    if kind == "slides":
        g += R(90, 124, 300, 150, CREAM, LINE) + T(110, 160, "Day two: Safety first", 18, INK, f="khand") + "".join(R(110, 180 + i * 18, 220 - i * 30, 8, "#E2D8C8", rx=4) for i in range(4))
        g += R(90, 282, 300, 30, "#F3EEE4") + T(100, 301, "Speaker notes: mention the CO meter demo", 10, MUTE)
    else:
        g += R(80, 120, 160, 190, CREAM, LINE) + T(90, 140, "Research dashboard", 11, INK, 700) + "".join(R(90, 152 + i * 26, 140, 18, WHITE, LINE, 3) for i in range(5))
        g += R(248, 120, 152, 190, CREAM, LINE) + T(258, 140, "TEST app screen", 11, INK, 700) + R(268, 156, 112, 140, WHITE, INK, 10, 1.2)
    return g + tech(240, 420, .8) + T(240, 500, "Max presents on the laptop  ·  TEST", 11, MUTE, 500, "middle")
DRAW = {
 "fu19_01num": lambda: card(bubbles(False), "Numbers with a key"), "fu19_01name": lambda: card(bubbles(True), "Names on bubbles"),
 "fu19_02co": lambda: card(receipt(False), "Company pays up front"), "fu19_02back": lambda: card(receipt(True), "Paid back after 90 days"),
 "fu19_03four": lambda: card(profile(["First Aid", "Lead-Safe", "OSHA 10", "Background Checked"]), "All four badges"),
 "fu19_03two": lambda: card(profile(["First Aid", "Background Checked"], T(70, 300, "More (2) >", 12, LAGOON, 600)), "Two plus More"),
 "fu19_04hide": lambda: card(profile(["First Aid", "OSHA 10", "Background Checked"]), "Expired badge hidden"),
 "fu19_04grey": lambda: card(profile(["First Aid", "OSHA 10", "Background Checked", "~Lead-Safe: Renewing"]), "Grey Renewing badge"),
 "fu19_05box": lambda: card(item("Thermal Camera", "Wow and difficulty  ·  SAMPLE", gauge(170, 380, 50, .9, GOLD, "Wow") + "".join(R(260 + i * 28, 360, 22, 22, INK if i < 2 else WHITE, INK, 3, 1.3) for i in range(5)) + T(318, 404, "Difficulty", 12, MUTE, 600, "middle")), "Five boxes"),
 "fu19_05gauge": lambda: card(item("Thermal Camera", "Wow and effort  ·  SAMPLE", gauge(170, 380, 50, .9, GOLD, "Wow") + gauge(320, 380, 50, .4, INK, "Effort")), "Second gauge"),
 "fu19_06thermal": lambda: card(item("Thermal Camera", "#1 by wow  ·  $529 SAMPLE  ·  easy setup", R(90, 330, 110, 32, JUNGLE, rx=16) + T(145, 351, "Buy now", 13, WHITE, 700, "middle") + tech(360, 380, .7)), "Thermal camera now"),
 "fu19_06glasses": lambda: card(item("Smart Glasses", "#2 by wow  ·  from $379 SAMPLE  ·  harder", R(90, 330, 130, 32, GOLD, rx=16) + T(155, 351, "Pilot: 1 tech", 13, WHITE, 700, "middle") + T(90, 392, "Members asked for consent first", 11, MUTE) + tech(360, 380, .7)), "Glasses pilot first"),
 "fu19_07free": lambda: card(calendar(False), "Weekends free"), "fu19_07sat": lambda: card(calendar(True), "Light Saturday review"),
 "fu19_08five": lambda: card(phone(5), "Five-card quiz"), "fu19_08ten": lambda: card(phone(10), "Ten-card quiz"),
 "fu19_09warm": lambda: card(agenda("warm"), "Next morning warm-up"), "fu19_09max": lambda: card(agenda("max"), "Review with Max"),
 "fu19_10slides": lambda: card(laptop("slides"), "Slides with notes"), "fu19_10live": lambda: card(laptop("live"), "Live walk-through"),
}
def T_RTC():
    spec = json.load(open(SPEC)); pairs, P = make("rtcfu19_", "Research")
    for p in spec["pairs"]:
        m = re.match(r"^([^:]+): ([^,]+), (.+)$", p["ask"]); loc, el, sent = m.groups()
        a, b = p["optionA"], p["optionB"]
        P(p["group"], loc, el, sent, (a["id"][5:], a["label"], a["desc"], a["feeling"], DRAW[a["id"]]()), (b["id"][5:], b["label"], b["desc"], b["feeling"], DRAW[b["id"]]()))
    return pairs
