"""Machan decks Oct 18 2026 (Max asked 22:04 ICT: "lets do a few swipes on machan and the origin story", "make 2 of them").
Two this-or-that decks, 10 picks each, Notes on every card, light only (cream), Khand headings + Hind body, phone-first.
Deck 1 (Look And Personality): drawn SVG mockups of the v3 wink mark (assets/machan-mark-v3-wink.svg, persimmon) in its real
footer context. Deck 2 (Origin Story): mini card mockups of the actual story text from /workspace/machan/brand-story.md and the
story carousel. Uses only the five real pieces of lore already in the story; no new facts. Palette: terracotta #C1502E,
lagoon #05668D, jungle #0B6E4F, cream #FAF6EE. Picks are logged only, never implemented automatically."""
from md1018_kit import *
from draft_svg import crisp
from team_kit import wrap
CR = "#FAF6EE"; BORD = "#E6DFD1"; HEAD = "#2A1D15"; LEAD = "#5A4636"; GREY = "#8A8A8A"
PERSIMMON = "#D9772B"; LEAF1 = "#0B6E4F"; LEAF2 = "#3E8E68"; BLUSH = "#EBB49C"; SEED = "#8A5A3C"
_n = [0]
def uid(p): _n[0] += 1; return f"{p}{_n[0]}"
MARK = dict(cap="two", eyes="wink", blush=True, finish="arc", body=TERRA, dy=0)
def mark(x, y, size, **o):
    """The v3 Machan mark (48-unit grid) at (x, y), size px wide. Options: cap two|three|calyx, eyes wink|open,
    blush, finish flat|soft, body colour, dy (small vertical hop for the bounce frames)."""
    o = dict(MARK, **o); b = o["body"]; s = ""
    if o["cap"] in ("two", "three"):
        s += f'<path d="M24 11.6V9.4" stroke="{LEAF1}" stroke-width="1.6" stroke-linecap="round"/>'
        s += f'<path d="M24 10.2C22.6 6 19 3.8 15 4.4c.7 4 4 6.4 9 5.8z" fill="{LEAF1}"/><path d="M24 10.2C25.4 6 29 3.8 33 4.4c-.7 4-4 6.4-9 5.8z" fill="{LEAF2}"/>'
        if o["cap"] == "three": s += f'<path d="M24 10.4C22.2 7.6 22.4 4.4 24 1.8c1.6 2.6 1.8 5.8 0 8.6z" fill="#2F7F5B"/>'
    s += f'<rect x="7" y="11" width="34" height="32" rx="14" fill="{b}"/>'
    if o["finish"] == "arc": s += '<path d="M14.5 16.6c2.4-2 5.6-3 9.5-3" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="1.6" stroke-linecap="round"/>'
    if o["finish"] == "soft":
        g = uid("hl")
        s += (f'<defs><radialGradient id="{g}" cx=".32" cy=".22" r=".7"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".22"/>'
              f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs><rect x="7" y="11" width="34" height="32" rx="14" fill="url(#{g})"/>'
              '<path d="M14.5 16.6c2.4-2 5.6-3 9.5-3" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.6" stroke-linecap="round"/>')
    if o["cap"] == "calyx":
        s += (f'<path d="M24 7.4Q25.8 10.6 34.5 12.3Q26 13.9 24 16.6Q22 13.9 13.5 12.3Q22.2 10.6 24 7.4Z" fill="{LEAF1}"/>'
              f'<path d="M24 12.3L24 6" stroke="{LEAF1}" stroke-width="1.8" stroke-linecap="round"/><circle cx="24" cy="12.3" r="1.6" fill="{LEAF2}"/>')
    s += '<rect x="11" y="18.5" width="26" height="20" rx="10" fill="#FAF6EE"/>'
    s += '<circle cx="19.2" cy="27" r="2.6" fill="#05668D"/><circle cx="19.9" cy="26.2" r=".8" fill="#fff"/>'
    if o["eyes"] == "wink": s += '<path d="M26.1 26.6q2.7 2.4 5.4 0" fill="none" stroke="#05668D" stroke-width="1.9" stroke-linecap="round"/>'
    else: s += '<circle cx="28.8" cy="27" r="2.6" fill="#05668D"/><circle cx="29.5" cy="26.2" r=".8" fill="#fff"/>'
    s += f'<path d="M21.2 32.4q2.8 2.2 5.6 0" fill="none" stroke="{b}" stroke-width="1.9" stroke-linecap="round"/>'
    if o["blush"]: s += f'<circle cx="15.2" cy="31.6" r="1.8" fill="{BLUSH}"/><circle cx="32.8" cy="31.6" r="1.8" fill="{BLUSH}"/>'
    return f'<g transform="translate({x:.2f},{y + o["dy"]:.2f}) scale({size / 48:.4f})">{s}</g>'
def T(x, y, s, size, col=INK, fam="hind", w=400, anchor="start", extra=""):
    return t(x, y, s, size, col, fam, w, anchor, extra)
PAIR_H = [0]
def frame(body, Hh, label, note, sub=None):
    Hh = max(Hh, PAIR_H[0])
    """One card: white top strip with label + MOCKUP chip, body, terracotta note line at the bottom."""
    i = uid("r")
    top = rect(0, 0, W, 24, "#FFFFFF") + T(12, 16, label.upper(), 7.5, INK, w=700, extra='letter-spacing=".8"') + ln(24, 0, W, LINE)
    top += rect(190, 6, 38, 13, "#FFFFFF", SAFFRON, 3, 1, 'stroke-dasharray="3 2"') + T(209, 15.5, "MOCKUP", 6, "#8A6510", w=700, anchor="middle", extra='letter-spacing=".5"')
    yn = Hh - 30
    nt = ln(yn - 10, 0, W, LINE) + rect(12, yn - 4, 3, 24, TERRA) + T(20, yn + 6, note[0], 8.5, INK, w=600) + T(20, yn + 18, note[1], 7.8, MUTE)
    return crisp(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="max-width:100%;height:auto">'
                 f'<clipPath id="{i}"><rect width="{W}" height="{Hh}" rx="14"/></clipPath><g clip-path="url(#{i})"><rect width="{W}" height="{Hh}" fill="{CR}"/>'
                 + body + top + nt + f'</g><rect x=".5" y=".5" width="{W-1}" height="{Hh-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def footer_strip(y, mk, text="Built by Machan", tag=None, label="FOOTER, REAL SIZE"):
    """The page footer as it sits under every project: mark at 22 px + 'Built by Machan' in grey Hind 11 px."""
    h = 46 if tag else 34
    s = T(14, y - 5, label, 6.5, FAINT, w=700, extra='letter-spacing=".8"')
    s += rect(10, y, 220, h, "#FFFFFF", BORD, 8, 1)
    tw = len(text) * 5.3; x0 = 120 - (22 + 6 + tw) / 2
    s += mark(x0, y + 5, 22, **mk) + T(x0 + 28, y + 20, text, 11, GREY, w=400)
    if tag: s += T(120, y + 38, tag, 8, TERRA, w=600, anchor="middle")
    return s, h
def look_card(mk, note, big=124, tag=None, extra=""):
    """Deck 1 standard card: big mark on cream, then the real-size footer under it."""
    body = mark(120 - big / 2, 32, big, **mk) + extra
    f, h = footer_strip(178, mk, tag=tag)
    body += f
    return frame(body, 178 + h + 54, "Machan mark", note)
# ---------- Deck 1 drawings that are not the standard card ----------
def hover_card(mode, note):
    """Three frames left to right: rest, cursor over the footer, rest again."""
    body = rect(0, 24, W, 196, CR) + T(14, 44, "FOOTER ON HOVER, 3 FRAMES", 6.5, FAINT, w=700, extra='letter-spacing=".8"')
    for i, (lab, x) in enumerate((("Rest", 18), ("Hover", 90), ("After", 162))):
        hov = i == 1; body += rect(x, 54, 60, 92, "#FFFFFF", TERRA if hov else BORD, 8, 1.4 if hov else 1)
        if mode == "wink": mk = dict(eyes="wink" if hov else "open"); dy = 0
        else: mk = dict(eyes="wink"); dy = -5 if hov else 0
        body += mark(x + 10, 66, 40, dy=dy, **mk)
        if mode == "bounce" and hov:
            body += f'<ellipse cx="{x+30}" cy="113" rx="12" ry="2" fill="#2A1D15" fill-opacity=".12"/>' + "".join(f'<path d="M{x+8+k*4} {74+k*6} h-5" stroke="{TERRA}" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round"/>' for k in range(3))
        else: body += f'<ellipse cx="{x+30}" cy="113" rx="14" ry="2" fill="#2A1D15" fill-opacity=".08"/>'
        body += T(x + 30, 128, "Built by Machan", 7.5, GREY, anchor="middle") + T(x + 30, 160, lab.upper(), 7, TERRA if hov else MUTE, w=700, anchor="middle", extra='letter-spacing=".8"')
        if i < 2: body += f'<path d="M{x+63} 100 l7 0 m-3 -3 l3 3 l-3 3" fill="none" stroke="{FAINT}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
    body += f'<path d="M{90+42} 96 l0 12 l3 -3 l3 6 l2 -1 l-3 -6 l4 0 z" fill="#FFFFFF" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"/>'
    body += T(120, 184, "Wink, then eyes open again" if mode == "wink" else "A 2 px hop, then settles back", 8.5, LEAD, w=500, anchor="middle")
    return frame(body, 250, "Machan footer", note)
def seed_glyph(cx, cy, k=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({k})"><ellipse cx="0" cy="0" rx="6" ry="8.5" fill="{SEED}"/><ellipse cx="0" cy="0" rx="4.3" ry="6.8" fill="#F3E6D2"/>'
            f'<ellipse cx="0" cy="-2.4" rx="2" ry="2.6" fill="{SEED}" fill-opacity=".85"/><path d="M0 0 V5" stroke="{SEED}" stroke-opacity=".85" stroke-width="1.3" stroke-linecap="round"/></g>')
def leaf_glyph(cx, cy, k=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({k})"><path d="M-8 4 C-6 -4 2 -8 9 -6 C8 1 1 6 -8 4 Z" fill="{LEAF1}"/>'
            f'<path d="M-6 3 C-1 0 3 -3 7 -5" fill="none" stroke="#FFFFFF" stroke-opacity=".5" stroke-width=".9" stroke-linecap="round"/></g>')
def divider_card(kind, note):
    body = rect(0, 24, W, 200, CR) + rect(14, 38, 212, 172, "#FFFFFF", BORD, 10)
    body += T(28, 62, "What we built", 15, HEAD, "khand") + "".join(rect(28, 72 + i * 10, w, 4, "#E9E2D6", "none", 2) for i, w in enumerate((176, 150, 164)))
    y = 124
    body += ln(y, 28, 104, "#E2D8C8") + ln(y, 136, 212, "#E2D8C8") + (seed_glyph(120, y, 1.15) if kind == "seed" else leaf_glyph(120, y, 1.2))
    body += T(28, 156, "What comes next", 15, HEAD, "khand") + "".join(rect(28, 166 + i * 10, w, 4, "#E9E2D6", "none", 2) for i, w in enumerate((168, 140, 120)))
    body += T(14, 222, "SECTION DIVIDER, ZOOMED", 6.5, FAINT, w=700, extra='letter-spacing=".8"')
    lab = "Seed with the spoon inside" if kind == "seed" else "One small green leaf"
    body += rect(14, 230, 212, 26, "#FFFFFF", BORD, 6) + (seed_glyph(32, 243, .9) if kind == "seed" else leaf_glyph(32, 243, .9)) + T(46, 247, lab, 8.5, LEAD, w=500)
    return frame(body, 316, "Machan divider", note)
def empty_card(kind, note):
    body = rect(0, 24, W, 230, CR) + rect(14, 38, 212, 200, "#FFFFFF", BORD, 10) + T(28, 60, "Your projects", 14, HEAD, "khand") + ln(68, 28, 212, "#EEE7DB")
    if kind == "sapling":
        body += f'<ellipse cx="120" cy="160" rx="34" ry="6" fill="#E9DCC8"/><path d="M120 160 C120 146 119 134 120 122" stroke="{LEAF1}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
        body += f'<path d="M120 136 C112 128 102 128 97 132 C102 140 112 142 120 136 Z" fill="{LEAF2}"/><path d="M120 126 C128 116 139 115 144 119 C139 128 128 131 120 126 Z" fill="{LEAF1}"/>'
        body += T(120, 190, "Nothing here yet.", 11, HEAD, w=600, anchor="middle") + T(120, 205, "Made to keep growing.", 8.5, TERRA, w=600, anchor="middle")
    else:
        body += rect(60, 100, 120, 60, "none", "#D9D1C3", 8, 1.2, 'stroke-dasharray="4 3"') + T(120, 134, "No projects", 8.5, FAINT, anchor="middle")
        body += T(120, 190, "Nothing here yet.", 11, HEAD, w=600, anchor="middle")
    body += mark(28, 216, 14) + T(46, 226, "Built by Machan", 7.5, GREY)
    return frame(body, 296, "Machan empty state", note)
import re as _re2
def _h(svg): return float(_re2.search(r'viewBox="0 0 240 ([\d.]+)"', svg).group(1))
def equal(P0):
    """Wrap make()'s P: option svgs are callables; both sides are drawn at one shared height so they line up."""
    def P(group, loc, el, sentence, a, b):
        PAIR_H[0] = 0; ha, hb = _h(a[4]()), _h(b[4]()); PAIR_H[0] = max(ha, hb)
        sa, sb = a[4](), b[4](); PAIR_H[0] = 0
        P0(group, loc, el, sentence, a[:4] + (sa,), b[:4] + (sb,))
    return P
def T_LOOK():
    pairs, P = make("machlook18_", "Branding"); P = equal(P)
    def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
    M = "Machan Mark Mockup"; F = "Machan Footer Mockup"
    P("Cap", M, "Leaf cap", "should Machan wear the two leaves he has today or a fuller cap of three leaves?",
      o("two", "Two Leaves", "Today's cap: two green leaves on a short stem.", "calm", lambda: look_card(dict(cap="two"), ("Today's mark", "Simple and light at 22 px"))),
      o("three", "Three Leaves", "A third, taller leaf in the middle of the cap.", "lively", lambda: look_card(dict(cap="three"), ("Fuller, more like a sprout", "A touch busier when small"))))
    P("Face", F, "Default face", "in the footer should Machan rest with his wink or with both eyes open?",
      o("wink", "Wink At Rest", "The v3 wink is always on in the footer.", "playful", lambda: look_card(dict(eyes="wink"), ("The wink is the signature", "Same as today"))),
      o("open", "Both Eyes Open", "Two round lagoon eyes; no wink at rest.", "friendly", lambda: look_card(dict(eyes="open"), ("Friendly and plain", "Wink saved for a moment"))))
    P("Face", M, "Blush cheeks", "should Machan keep the soft blush on his cheeks or drop it for a cleaner face?",
      o("blush", "Blush Cheeks", "Two soft pink dots under the eyes, as today.", "warm", lambda: look_card(dict(blush=True), ("Warm and a little shy", "Same as today"))),
      o("noblush", "No Blush", "Cream face with eyes and smile only.", "minimal", lambda: look_card(dict(blush=False), ("Cleaner at small sizes", "Less cute, more crisp"))))
    P("Cap", M, "Persimmon cap", "now that Machan is a persimmon should the leaves become a four-sepal persimmon calyx or stay as leaves?",
      o("calyx", "Persimmon Calyx", "A flat four-sepal star on top, like a real persimmon.", "natural", lambda: look_card(dict(cap="calyx"), ("Reads as a persimmon", "Lower, flatter top"))),
      o("leaves", "Keep The Leaves", "Two leaves on a stem, as today.", "playful", lambda: look_card(dict(cap="two"), ("Known shape", "Sprout-like and friendly"))))
    P("Finish", M, "Colour finish", "should the body be flat colour or keep a soft highlight on the top left?",
      o("flat", "Flat Colour", "One solid terracotta, no shine.", "minimal", lambda: look_card(dict(finish="flat"), ("Crisp, sticker-like", "Prints cleanly"))),
      o("soft", "Soft Highlight", "A faint glow and shine stroke on the top left.", "polished", lambda: look_card(dict(finish="soft"), ("A little round and ripe", "Close to today's shine"))))
    P("Footer", F, "Footer tagline", "should a small tagline sit under Built by Machan or should the footer stay one line?",
      o("tag", "Tagline Under The Mark", "Adds the wish line under it in small terracotta.", "warm", lambda: look_card(dict(), ("A small good-luck sign-off", "Footer grows a line"), tag="May all things go as you wish.")),
      o("notag", "No Tagline", "Just the mark and Built by Machan, as today.", "calm", lambda: look_card(dict(), ("Quiet, one line", "Same as today"))))
    P("Motion", F, "Hover motion", "when someone points at the footer should Machan wink or do a tiny bounce?",
      o("wink", "Wink On Hover", "Eyes open at rest; he winks while you hover.", "playful", lambda: hover_card("wink", ("The wink becomes a reward", "Needs eyes open at rest"))),
      o("bounce", "Tiny Bounce", "Keeps the wink; hops 2 px and settles.", "lively", lambda: hover_card("bounce", ("Wink stays the signature", "Small, quick motion"))))
    P("Colour", M, "Body colour", "should Machan's body move to a brighter persimmon orange or stay brand terracotta?",
      o("orange", "Persimmon Orange", "A warmer, brighter orange (#D9772B).", "fresh", lambda: look_card(dict(body=PERSIMMON), ("More like the real fruit", "Steps off the brand red"))),
      o("terra", "Terracotta", "Brand terracotta #C1502E, as today.", "calm", lambda: look_card(dict(body=TERRA), ("Matches every board", "Same as today"))))
    P("Glyphs", "Machan Divider Mockup", "Divider glyph", "between page sections should the small divider be a persimmon seed with its spoon or a single leaf?",
      o("seed", "Seed-Spoon Divider", "A split persimmon seed with the spoon inside.", "editorial", lambda: divider_card("seed", ("Nods to the seed forecast", "Needs a closer look to read"))),
      o("leaf", "Leaf Divider", "One small green leaf from Machan's cap.", "natural", lambda: divider_card("leaf", ("Reads at a glance", "Matches the cap"))))
    P("Empty", "Machan Empty State Mockup", "Empty list", "when a list has nothing in it yet should it show a small sapling or a plain empty box?",
      o("sapling", "Sapling Empty State", "A tiny sapling plus Made to keep growing.", "warm", lambda: empty_card("sapling", ("Hopeful, on story", "A little more to draw"))),
      o("plain", "Plain Empty State", "A dashed box and Nothing here yet.", "practical", lambda: empty_card("plain", ("Clear and quiet", "No story in it"))))
    return pairs
# ---------- Deck 2: story text cards ----------
def slide(kicker, head, body, foot=None, pos=None, glyph=None, mk=True, card_note=None, foot_col=TERRA, size=24, bw=44):
    """A mini carousel slide drawn inside the card: kicker, Khand headline lines, Hind body, terracotta foot line, dots."""
    s = rect(0, 24, W, 400, CR) + rect(14, 36, 212, 0, "none")
    y = 60
    inner = T(28, y, kicker.upper(), 7.5, TERRA, w=700, extra='letter-spacing="1"')
    if glyph: inner += T(212, y + 2, glyph, 11, TERRA, w=600, anchor="end")
    y += 8
    for l in head: y += size * .95; inner += T(28, y, l, size, HEAD, "khand")
    y += 16
    for l in wrap(body, bw): inner += T(28, y, l, 8.5, LEAD); y += 12.5
    if foot:
        y += 6
        for l in wrap(foot, bw - 2): inner += T(28, y, l, 8.5, foot_col, w=600); y += 12.5
    y += 8
    if mk: inner += mark(28, y, 18) + T(50, y + 12, "Built by Machan", 7.5, GREY); y += 26
    if pos: n, i = pos; x0 = 120 - (n - 1) * 5; inner += "".join(rect(x0 + k * 10 - (5 if k == i else 2.5), y, 10 if k == i else 5, 5, TERRA if k == i else "#D6D0C6", "none", 2.5) for k in range(n)); y += 12
    hh = y + 8
    s += rect(14, 36, 212, hh - 36, "#FFFFFF", BORD, 12) + inner
    return s, hh
def story_card(label, note, *a, **k):
    body, hh = slide(*a, **k)
    return frame(body, hh + 52, label, note)
TALE = "The Tiger and the Dried Persimmon"
def T_STORY():
    pairs, P = make("machstory18_", "Branding"); P = equal(P)
    def o(k, label, desc, feel, svg): return (k, label, desc, feel, svg)
    C = "Machan Story Carousel Mockup"; I = "Machan Story Intro Card Mockup"; G = "Machan Signature Card Mockup"
    SC = "Story card"
    P("Lore", C, "Lead lore", "right after the intro should the story open on Fruit of the gods or on May all things go as you wish?",
      o("gods", "Fruit Of The Gods First", "Slide 01 is the Diospyros name story.", "playful",
        lambda: story_card(SC, ("Opens on the name", "Light, a bit grand"), "01 The name", ["Fruit of", "the gods."],
                   "The persimmon genus is Diospyros, from Greek. It's often translated as \"fruit of the gods\" or \"divine fruit.\"",
                   "Machan doesn't let it go to his head. Mostly.", pos=(7, 1))),
      o("wish", "The Wish First", "Slide 01 is the Chinese good-luck wish.", "warm",
        lambda: story_card(SC, ("Opens on a wish for the reader", "Warm and lucky"), "01 The wish", ["May all things go", "as you wish."],
                   "In Chinese, persimmon (柿, shì) sounds like 事, \"matters.\" Two persimmons stand for 事事如意, a good-luck motif all over New Year art.",
                   "Every project Machan signs carries a little of that wish.", pos=(7, 1), glyph="事事如意")))
    P("Tone", I, "Tone", "should the story read playful and a little cheeky or warm and earnest?",
      o("playful", "Playful", "Cheeky lines, the wink does the talking.", "playful",
        lambda: story_card(SC, ("Fun, a bit smug", "Matches the wink"), "Meet the mascot", ["Machan is a", "persimmon."],
                   "Round, terracotta, slightly smug. One bright eye, one caught mid-wink. Fruit of the gods, and he doesn't let it go to his head. Mostly.",
                   None, pos=(7, 0))),
      o("earnest", "Warm And Earnest", "Plain, kind lines about what he stands for.", "warm",
        lambda: story_card(SC, ("Sincere, says what he means", "Less joking"), "Meet the mascot", ["Machan is a", "persimmon."],
                   "A small, round mark at the bottom of every project. He stands for good luck, a little nerve, thinking ahead and work that keeps growing.",
                   None, pos=(7, 0))))
    P("Taglines", G, "Lead tagline", "should the main tagline be May all things go as you wish or Small fruit, big nerve?",
      o("wish", "May All Things Go As You Wish", "The good-luck wish as the main line.", "warm",
        lambda: story_card(SC, ("A wish for the reader", "Soft and generous"), "The signature", ["Built by", "Machan."], "May all things go as you wish.", None, mk=False, size=26)),
      o("nerve", "Small Fruit. Big Nerve.", "The tiger lore as the main line.", "bold",
        lambda: story_card(SC, ("Short and punchy", "About courage"), "The signature", ["Built by", "Machan."], "Small fruit. Big nerve.", None, mk=False, size=26)))
    P("Taglines", G, "Second tagline", "for the second line should Machan use Fruit of the gods, wink included or Read the seed, build for the season?",
      o("wink", "Fruit Of The Gods. Wink Included.", "Name lore plus the wink.", "playful",
        lambda: story_card(SC, ("Funny, ties to the mark", "Leans on the wink"), "The signature", ["Built by", "Machan."], "Fruit of the gods. Wink included.", None, mk=False, size=26)),
      o("seed", "Read The Seed", "Read the seed. Build for the season. The forecast as a promise.", "practical",
        lambda: story_card(SC, ("Says he thinks ahead", "Needs the forecast story"), "The signature", ["Built by", "Machan."], "Read the seed. Build for the season.", None, mk=False, size=26)))
    P("Tiger", C, "Tiger slide", "since the tiger slide reads weakest should it lead with the folk tale or lead with Small fruit, big nerve?",
      o("tale", "Tale First", "Headline The tiger ran, then the tale, then the line.", "playful",
        lambda: story_card(SC, ("Story pulls you in", "Punchline last"), "03 The nerve", ["The tiger", "ran."],
                   f"In the Korean folk tale \"{TALE},\" a tiger hears a mother quiet her crying baby with a gotgam, a dried persimmon. It decides the persimmon must be scarier than a tiger, and flees.",
                   "Small fruit. Big nerve.", pos=(7, 3))),
      o("line", "Line First", "The tagline is the headline; the tale told short.", "bold",
        lambda: story_card(SC, ("Point lands first", "Tale as the proof"), "03 The nerve", ["Small fruit.", "Big nerve."],
                   f"In the Korean folk tale \"{TALE},\" a tiger runs from a gotgam, a dried persimmon, sure it must be scarier than a tiger.",
                   "Machan doesn't back away from hard problems.", pos=(7, 3))))
    P("Footer", "Machan Footer Tooltip Mockup", "Footer blurb", "when someone taps Built by Machan should the blurb be the full About line or one short tagline?",
      o("full", "Full About Line", "The persimmon, fruit of the gods, lucky mascot line.", "warm", lambda: blurb_card("full", ("Tells the whole idea", "Longer to read"))),
      o("short", "One Short Line", "Built by Machan. May all things go as you wish.", "minimal", lambda: blurb_card("short", ("Quick and light", "Story left to the carousel"))))
    P("Naming", I, "Naming", "should the story say Max Weberman by name or stay just Machan?",
      o("max", "Names Max", "He signs off on everything Max Weberman builds.", "warm",
        lambda: story_card(SC, ("Clear whose mascot he is", "Same as today"), "Meet the mascot", ["Machan is a", "persimmon."],
                   "Round, terracotta, two green leaves, one bright eye and one mid-wink. He signs off on everything Max Weberman builds.", None, pos=(7, 0))),
      o("machan", "Just Machan", "He signs off on everything built here.", "calm",
        lambda: story_card(SC, ("Machan stands on his own", "Works on any project"), "Meet the mascot", ["Machan is a", "persimmon."],
                   "Round, terracotta, two green leaves, one bright eye and one mid-wink. He signs off on everything built here.", None, pos=(7, 0))))
    P("Format", "Machan Story Page Mockup", "Story format", "should the story stay a seven-slide carousel or fold into one single card?",
      o("carousel", "Seven-Slide Carousel", "One lore per slide, swipe through, dots below.", "lively", lambda: carousel_card(("One idea at a time", "Same as today"))),
      o("single", "One Single Card", "All five lore lines on one card, one line each.", "practical", lambda: single_card(("All of it in one look", "Less room for each story"))))
    P("Roots", C, "Nagasaki tree", "should the story keep the Nagasaki survivor tree slide or stay lighter and end on the seed forecast?",
      o("keep", "Keep The Nagasaki Tree", "Slide 05: the survivor tree and its saplings.", "warm",
        lambda: story_card(SC, ("The deepest root of the story", "A heavier moment"), "05 The roots", ["Made to keep", "growing."],
                   "A persimmon tree in Nagasaki survived the 1945 atomic bombing. Through the Kaki Tree Project, its saplings are planted around the world as a symbol of peace.",
                   "Under the wink, Machan is about things that last.", pos=(7, 5))),
      o("light", "Keep It Lighter", "Drop slide 05; the forecast is the last lore.", "playful",
        lambda: story_card(SC, ("Stays playful start to end", "Six slides"), "04 The forecast", ["Reads what's", "coming."],
                   "Ozark and US folk weather lore says to split a persimmon seed. A spoon means heavy snow, a knife means bitter, cutting cold, and a fork means a mild winter.",
                   "Machan looks a little way down the road before anything gets built.", pos=(6, 4))))
    P("Close", G, "Closing taglines", "should the last slide list all five taglines or end on just one?",
      o("all", "All Five Taglines", "Every tagline listed under Built by Machan.", "editorial", lambda: close_card("all", ("Shows the whole set", "Busier ending"))),
      o("one", "Just One", "Built by Machan. and one line under it.", "minimal", lambda: close_card("one", ("Clean, memorable end", "Others live elsewhere"))))
    return pairs
ABOUT = "Machan is a persimmon, the \"fruit of the gods,\" and Max Weberman's lucky mascot, here to sign off on everything Max builds, with a wink."
def blurb_card(kind, note):
    body = rect(0, 24, W, 260, CR) + rect(14, 38, 212, 70, "#FFFFFF", BORD, 10) + "".join(rect(28, 52 + i * 11, w, 4, "#E9E2D6", "none", 2) for i, w in enumerate((176, 150, 164, 120)))
    lines = wrap(ABOUT, 40) if kind == "full" else ["Built by Machan.", "May all things go as you wish."]
    bh = 22 + len(lines) * 12.5; by = 124
    body += rect(22, by, 196, bh, HEAD, "none", 8) + f'<path d="M114 {by+bh} l6 7 l6 -7 z" fill="{HEAD}"/>'
    for i, l in enumerate(lines): body += T(34, by + 18 + i * 12.5, l, 8.5, "#FAF6EE", w=600 if (kind == "short" and i == 0) else 400)
    fy = by + bh + 14
    body += rect(10, fy, 220, 34, "#FFFFFF", BORD, 8) + mark(78, fy + 6, 22) + T(106, fy + 21, "Built by Machan", 11, GREY)
    body += f'<path d="M150 {fy+14} l0 12 l3 -3 l3 6 l2 -1 l-3 -6 l4 0 z" fill="#FFFFFF" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"/>'
    return frame(body, fy + 34 + 62, "Machan footer", note)
def carousel_card(note):
    body = rect(0, 24, W, 260, CR) + T(14, 44, "MACHAN: A PERSIMMON STORY", 7, MUTE, w=700, extra='letter-spacing=".8"') + T(226, 44, "02 / 07", 7.5, MUTE, w=600, anchor="end")
    body += rect(14, 54, 176, 170, "#FFFFFF", BORD, 12) + T(26, 76, "01 THE NAME", 7.5, TERRA, w=700, extra='letter-spacing="1"') + T(26, 100, "Fruit of", 22, HEAD, "khand") + T(26, 121, "the gods.", 22, HEAD, "khand")
    for i, l in enumerate(wrap("The persimmon genus is Diospyros, from Greek, often translated as \"fruit of the gods.\"", 32)): body += T(26, 140 + i * 12, l, 8.5, LEAD)
    body += mark(26, 190, 18) + T(48, 202, "Built by Machan", 7.5, GREY)
    body += rect(198, 54, 176, 170, "#FFFFFF", BORD, 12) + T(210, 76, "02 THE WISH", 7.5, TERRA, w=700) + T(210, 100, "May all", 22, HEAD, "khand")
    x0 = 120 - 6 * 5; body += "".join(rect(x0 + k * 10 - (5 if k == 1 else 2.5), 236, 10 if k == 1 else 5, 5, TERRA if k == 1 else "#D6D0C6", "none", 2.5) for k in range(7))
    body += T(120, 262, "Swipe for the next story", 8, MUTE, anchor="middle")
    return frame(body, 330, "Machan story page", note)
def single_card(note):
    rows = [("Fruit of the gods.", "Diospyros, the divine fruit."), ("May all things go as you wish.", "事事如意, the good-luck pun."),
            ("Braver than he looks.", "The tiger who ran from a gotgam."), ("Reads what's coming.", "Spoon, knife or fork in the seed."), ("Made to keep growing.", "The Nagasaki tree and its saplings.")]
    body = rect(0, 24, W, 300, CR) + rect(14, 36, 212, 258, "#FFFFFF", BORD, 12) + T(28, 60, "Machan is a persimmon.", 17, HEAD, "khand")
    y = 74
    for h, s in rows:
        body += rect(28, y, 3, 26, TERRA) + T(38, y + 10, h, 9, HEAD, w=600) + T(38, y + 22, s, 8, MUTE); y += 34
    body += mark(28, y + 4, 18) + T(50, y + 16, "Built by Machan", 7.5, GREY)
    return frame(body, 352, "Machan story page", note)
TAGS = ["May all things go as you wish.", "Small fruit. Big nerve.", "Fruit of the gods. Wink included.", "Read the seed. Build for the season.", "Made to keep growing."]
def close_card(kind, note):
    body = rect(0, 24, W, 300, CR); y = 60
    inner = T(28, y, "THE SIGNATURE", 7.5, TERRA, w=700, extra='letter-spacing="1"') + mark(170, 46, 42)
    inner += T(28, y + 26, "Built by", 26, HEAD, "khand") + T(28, y + 51, "Machan.", 26, HEAD, "khand"); y += 70
    if kind == "all":
        for l in wrap("Lucky, brave, thinks ahead, built to last. A little divine, a lot playful, with a wink.", 40): inner += T(28, y, l, 8.5, LEAD); y += 12.5
        y += 6
        for s in TAGS: inner += rect(28, y - 9, 3, 12, TERRA) + T(36, y, s, 8.5, HEAD, w=600); y += 16
    else:
        y += 6; inner += T(28, y + 4, TAGS[0], 12, TERRA, w=600); y += 26
    y += 8; x0 = 90; inner += "".join(rect(x0 + k * 10 - (5 if k == 6 else 2.5), y, 10 if k == 6 else 5, 5, TERRA if k == 6 else "#D6D0C6", "none", 2.5) for k in range(7)); y += 14
    body += rect(14, 36, 212, y - 36, "#FFFFFF", BORD, 12) + inner
    return frame(body, y + 54, "Machan signature card", note)
