#!/usr/bin/env python3
"""Build Style Swipe daily deck 2026-10-13: 25 pairs.
Blog topics (10), blog writing style (6), micro-dose color (7), Up Keep features (12),
swipe controls (3), variety (9), Niko/Vivian function (3). All option ids prefixed d13_.
Run from style-swipe repo root."""
import json, random, datetime as dt, glob, os

DID = "2026-10-13"
INK, MUTE, LINE = "#0A0A0A", "#525252", "#E5E0D8"
CREAM, SEL, W, H = "#FAF6EE", "#F3E8DC", 240, 300
TERRA, LAGOON, LAG2 = "#C1502E", "#05668D", "#00A6A6"
JUNGLE, SAFFRON, BERRY, PERSIM = "#0B6E4F", "#D4A017", "#9B2D5B", "#E4572E"
K = 'font-family="Khand" font-weight="700"'
HD = 'font-family="Hind"'

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def t(x, y, s, size=10, col=INK, f="hind", w=400, anchor="start", extra=""):
    fam = K if f == "khand" else (f'{HD} font-weight="{w}"' if f == "hind" else f'font-family="{f}"')
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {fam} {extra}>{esc(s)}</text>'
def lbl(x, y, s, col=MUTE, size=7): return t(x, y, s.upper(), size, col, "hind", 600, extra='letter-spacing="1"')
def h1(x, y, s, size=20, col=INK, anchor="start"):
    maxw = 212 if anchor == "middle" else 226 - x
    size = min(size, round(maxw / max(len(s) * .47, 1), 1))
    return t(x, y, s, size, col, "khand", anchor=anchor)
def para(x, y, lines, size=8.5, col=MUTE, lh=None):
    lh = lh or size * 1.35
    return "".join(t(x, y + i * lh, l, size, col) for i, l in enumerate(lines))
def rect(x, y, w, h, fill="none", stroke="none", r=0, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def btn(y, s, style="fill", col=INK, x=14, w=212, h=26, size=9):
    bg, fg = (col, "#FFFFFF") if style == "fill" else ("#FFFFFF", col)
    return rect(x, y, w, h, bg, col, 0, 1.5) + t(x + w / 2, y + h / 2 + size * .36, s.upper(), size, fg, "hind", 600, "middle", 'letter-spacing="1.2"')
def ln(y, x1=14, x2=226): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LINE}"/>'
def tag(x, y, s, col, solid=False):
    ww = len(s) * 4.4 + 10
    return rect(x, y, ww, 11, col if solid else col + "1F", "none", 5.5) + t(x + ww / 2, y + 8, s.upper(), 5.8, "#FFFFFF" if solid else col, "hind", 600, "middle", 'letter-spacing=".6"')
def pbar(y, frac, col=INK, x=14, w=212):
    return rect(x, y, w, 4, "#EEEAE4", "none", 2) + rect(x, y, w * frac, 4, col, "none", 2)
def roof_logo(x, y, s=1, c=INK, up=MUTE):
    return (f'<g transform="translate({x},{y}) scale({s})">' + t(0, 0, "smart", 13, c, "khand") + t(29, 0, "up", 13, up, "khand")
            + f'<polyline points="27,-8 35.5,-14 44,-8" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
            + t(44, 0, "keep", 13, c, "khand") + "</g>")
def hdr(right="", c=INK, up=MUTE):
    r = right or (rect(150, 9, 78, 13, "#F5F5F5", LINE, 6.5) + t(189, 18, "PROTOTYPE", 5.5, MUTE, "hind", 600, "middle", 'letter-spacing=".6"'))
    return roof_logo(14, 21, 1, c, up) + r + f'<line x1="0" y1="31" x2="{W}" y2="31" stroke="{LINE}"/>'
def screen(body, bg="#FFFFFF", head=True, right="", hc=INK, up=MUTE):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%">'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{bg}"/>'
            + (hdr(right, hc, up) if head else "") + body
            + f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def icon_chat(x, y, c=LAGOON, s=18):
    return f'<g transform="translate({x},{y}) scale({s/24})"><path d="M4 5 h16 v10 h-9 l-5 4 v-4 h-2 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/></g>'
def warn_tri(x, y, c=PERSIM, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M12 2 L23 21 H1 Z" fill="{c}"/><rect x="11" y="8" width="2" height="7" fill="#FFFFFF"/><circle cx="12" cy="18" r="1.3" fill="#FFFFFF"/></g>'
def check_box(x, y, on, c=JUNGLE):
    return rect(x, y, 11, 11, c if on else "#FFFFFF", c if on else "#BDB6AA", 2, 1.3) + (f'<path d="M{x+2.5} {y+5.5} l2.5 2.5 4 -5" fill="none" stroke="#FFFFFF" stroke-width="1.6"/>' if on else "")
def ring(cx, cy, r, frac, col, label=""):
    import math
    a = 2 * math.pi * frac; x2, y2 = cx + r * math.sin(a), cy - r * math.cos(a)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEAE4" stroke-width="5"/>'
            f'<path d="M{cx} {cy-r} A{r} {r} 0 {1 if frac>.5 else 0} 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
            + t(cx, cy + 4, label, 11, INK, "khand", anchor="middle"))
def mw_hdr(title="maxweberman.com"):
    return (rect(0, 0, W, 36, "#FFFFFF") + t(14, 24, "MAX WEBERMAN", 11, INK, "khand")
            + t(226, 24, "Blog", 8, MUTE, anchor="end") + ln(36, 0, W))

def O(i, label, desc, tags, visual, notes=True):
    o = {"id": "d13_" + i, "label": label, "desc": desc, "tags": tags, "visual": visual}
    if notes: o["notes"] = True
    return o
def Vsvg(svg, bg="#FFFFFF"):
    return {"type": "hm", "m": "svg", "svg": svg, "bg": bg}
def Vctrl(fmt, words, icons, colors, style="outline", bg="#f4f1ea", font="Hind"):
    return {"type": "controls", "fmt": fmt, "words": words, "icons": icons, "colors": colors, "style": style, "bg": bg, "font": font}
def Vtype(head, body, hw=700, upper=False, tracking="0"):
    return {"type": "type", "head": head, "body": body, "headWeight": hw, "upper": upper, "tracking": tracking}
def Vtone(lines, frm="Max → Reader"):
    return {"type": "tone", "lines": lines, "from": frm}
def Vui(bg, surface, text, accent, radius, font, shadow="soft", border="1px solid #E5E0D8", muted=None):
    return {"type": "ui", "bg": bg, "surface": surface, "text": text, "accent": accent, "radius": radius,
            "font": font, "shadow": shadow, "border": border, "muted": muted or text}
def Vmood(key, overlay=None):
    v = {"type": "mood", "key": key}
    if overlay: v["overlay"] = overlay
    return v
def Vpolish(app, c, p):
    return {"type": "polish", "kind": "scr", "app": app, "c": c, "p": p}

def chip_y(x, y, s):
    return rect(x, y, 100, 28, "#FFFFFF", LINE, 14) + t(x + 50, y + 18, s, 9, INK, "hind", 600, "middle")

pairs = []  # list of dicts with group before final id

def add(group, cat, app, ask, a, b, purpose="refine", retest=False):
    pairs.append({"group": group, "category": cat, "app": app, "ask": ask,
                  "optionA": a, "optionB": b, "purpose": purpose, "retest": retest, "notes": True})

# ========== A. Blog Topics (10) ==========
TOPICS = [
    ("flat_fee", "Why I Charge a Flat Fee Instead of a Percentage",
     "One clear number. No surprises when the budget grows."),
    ("clean_job", "What a Clean Jobsite Says About Your Builder",
     "Order on site usually means order in the schedule and the books."),
    ("see_site", "How You Can See Your Jobsite Anytime",
     "Live view and clear updates without calling the superintendent."),
    ("sub_bids", "Real Sub Bids vs. Padded Estimates",
     "How I show real trade numbers next to a padded lump sum."),
    ("value_eng", "Value Engineering Without Cutting Corners",
     "Where we save money without touching structure, waterproofing, or finish quality."),
    ("restaurant", "What Restaurant Owners Should Know Before a Build-Out",
     "Hood, grease, power, and schedule traps that hit restaurants first."),
    ("custom_home", "Planning a Custom Home: The First Five Decisions",
     "Site, footprint, structure, envelope, and budget — in that order."),
    ("change_orders", "How Change Orders Should Work (and Why They Cause Fights)",
     "A plain process for price, time, and sign-off before work moves."),
    ("allowances", "Allowances Explained: Why Your Budget Moves",
     "What an allowance really covers, and how overages get approved."),
    ("pick_builder", "How to Pick a Builder: Questions to Ask Before You Sign",
     "Ten questions that separate a real builder from a sales pitch."),
]

def blog_yes_card(title, pitch):
    # wrap long title
    words = title.split(); lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > 28 and cur: lines.append(cur); cur = w
        else: cur = trial
    if cur: lines.append(cur)
    lines = lines[:4]
    body = mw_hdr()
    body += lbl(14, 54, "Draft Post") + h1(14, 74, "Write This?", 16)
    body += rect(14, 88, 212, 150, "#FFFFFF", LINE, 4)
    body += "".join(t(24, 112 + i * 16, ln_, 11 if i == 0 else 10, INK, "khand" if i == 0 else "hind", 600 if i else 400)
                    for i, ln_ in enumerate(lines))
    body += para(24, 112 + len(lines) * 16 + 8, [pitch[:42], pitch[42:84] if len(pitch) > 42 else ""], 8, MUTE)
    body += tag(24, 220, "Blog", LAGOON) + tag(70, 220, "Yes", JUNGLE, True)
    body += btn(250, "Write This Post", "fill", TERRA)
    return screen(body, head=False)

def blog_not_now():
    body = mw_hdr()
    body += lbl(14, 54, "Hold") + h1(14, 74, "Not Now", 18)
    body += rect(14, 96, 212, 120, "#F5F5F5", LINE, 4)
    body += t(120, 150, "Skip This Topic", 14, MUTE, "khand", anchor="middle")
    body += t(120, 172, "Keep it in the idea list.", 9, MUTE, anchor="middle")
    body += btn(250, "Not Now", "outline", MUTE)
    return screen(body, head=False)

for slug, title, pitch in TOPICS:
    add("Blog Topics", "Blog Topics", "maxweberman.com Blog", "Blog Topic: Write This Post?",
        O(f"blog_yes_{slug}", title, pitch, ["clear", "practical", "direct", "personal"],
          Vsvg(blog_yes_card(title, pitch))),
        O(f"blog_no_{slug}", "Not Now", "Skip this topic for now.", ["calm", "simple", "quiet", "later"],
          Vsvg(blog_not_now())))

# ========== B. Blog Writing Style (6) ==========
# 1 Voice I vs We
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "First Person Or Company Voice?",
    O("blog_voice_i", 'First Person "I"', 'I write as Max: "I charge a flat fee."',
      ["personal", "direct", "clear", "warm"],
      Vtone(["I charge a flat fee instead of a percentage.", "Here is why that protects your budget."], "Max → Reader")),
    O("blog_voice_we", 'Company "We"', 'We write as the firm: "We charge a flat fee."',
      ["formal", "pro", "clear", "calm"],
      Vtone(["We charge a flat fee instead of a percentage.", "Here is why that protects your budget."], "Weberman Construction → Reader")))

# 2 Headings Title Case vs Sentence case
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Which Heading Style For Blog Posts?",
    O("blog_head_title", "Title Case (Tesla Style)", "Capitalize Major Words In Every Heading.",
      ["clear", "strong", "brand", "direct"],
      Vtype("'Khand', sans-serif", "'Hind', sans-serif", 700, False, "0.02em")),
    O("blog_head_sentence", "Sentence case", "Capitalize only the first word, as on maxweberman.com today.",
      ["calm", "simple", "web", "soft"],
      {"type": "type", "head": "'Khand', sans-serif", "body": "'Hind', sans-serif", "headWeight": 600, "upper": False, "tracking": "0",
       "sample": "How change orders should work"}))

# 3 Length short vs long
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Short Punchy Sections Or Longer How-To Depth?",
    O("blog_len_short", "Short Punchy Sections", "Tight blocks, one idea each, easy to skim on a phone.",
      ["clear", "practical", "light", "direct"],
      Vsvg(screen(mw_hdr() + lbl(14, 54, "Post") + h1(14, 72, "Flat Fee, Plain Math", 15)
                  + para(14, 92, ["One number. No percentage creep.", "", "1. Scope locked", "2. Price locked", "3. Changes priced"], 9, INK)
                  + tag(14, 200, "3 Min Read", LAGOON) + btn(250, "Keep Reading", "outline", INK), head=False))),
    O("blog_len_long", "Longer How-To Depth", "Full walkthrough with examples, tables, and caveats.",
      ["thorough", "guided", "pro", "depth"],
      Vsvg(screen(mw_hdr() + lbl(14, 54, "Post") + h1(14, 72, "Flat Fee, Full Guide", 15)
                  + para(14, 90, ["Why percentages fail on custom work,", "how we build the number, what happens", "when scope grows, three job examples,", "and a worksheet you can reuse.", "", "≈ 12 min read · 1,800 words"], 8.5, MUTE)
                  + btn(250, "Keep Reading", "fill", INK), head=False))))

# 4 Structure numbered vs prose
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Numbered Steps Or Flowing Prose?",
    O("blog_struct_steps", "Numbered Steps", "1, 2, 3 checklist style readers can follow.",
      ["clear", "guided", "practical", "system"],
      Vsvg(screen(mw_hdr() + h1(14, 60, "Five Decisions First", 15)
                  + "".join(rect(14, 78 + i * 32, 212, 28, "#FFFFFF", LINE, 2) + t(28, 96 + i * 32, f"{i+1}.  {s}", 10, INK, "hind", 600)
                            for i, s in enumerate(["Pick the site", "Lock the footprint", "Choose structure", "Set the envelope"]))
                  + btn(250, "Next", "fill", TERRA), head=False))),
    O("blog_struct_prose", "Flowing Prose", "Story-style paragraphs without numbered lists.",
      ["warm", "personal", "story", "calm"],
      Vsvg(screen(mw_hdr() + h1(14, 60, "Five Decisions First", 15)
                  + para(14, 88, ["Before finishes or fixtures, the site", "sets the budget. Then the footprint", "locks cost. Structure and envelope", "follow. Only then do finishes matter.", "", "That order keeps change orders rare."], 9.5, INK)
                  + btn(250, "Next", "outline", INK), head=False))))

# 5 Lead photo vs headline
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Photo-Led Post Or Headline And Text First?",
    O("blog_lead_photo", "Photo-Led Post", "Big jobsite photo above the title.",
      ["visual", "warm", "natural", "story"],
      Vsvg(screen(rect(0, 0, W, 130, "#D4C4B0") + rect(30, 40, 100, 60, "#F7F4EE") + rect(40, 70, 20, 30, "#6B4B3A")
                  + t(14, 156, "MAX WEBERMAN", 8, MUTE, "hind", 600, extra='letter-spacing="1"')
                  + h1(14, 178, "A Clean Jobsite", 18) + para(14, 196, ["What order on site tells you", "about the builder behind it."], 9, MUTE)
                  + btn(250, "Read", "fill", INK), head=False))),
    O("blog_lead_text", "Headline And Text First", "Title and dek first; photo lower or aside.",
      ["clear", "direct", "editorial", "simple"],
      Vsvg(screen(mw_hdr() + h1(14, 64, "A Clean Jobsite", 20) + para(14, 88, ["What order on site tells you", "about the builder behind it."], 10, MUTE)
                  + rect(14, 130, 212, 90, "#E8DFD4", LINE, 2) + t(120, 180, "Photo", 10, MUTE, anchor="middle")
                  + btn(250, "Read", "outline", INK), head=False))))

# 6 Tone advice vs story
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Direct Advice Or Story From The Jobsite?",
    O("blog_tone_advice", "Direct Advice", "Do this. Skip that. Plain instruction.",
      ["direct", "practical", "clear", "strong"],
      Vtone(["Ask for the allowance list before you sign.", "If it is vague, the budget will move."], "Advice")),
    O("blog_tone_story", "Story From The Jobsite", "A real scene first, then the lesson.",
      ["warm", "personal", "story", "natural"],
      Vtone(["Tuesday, 6 AM: the tile crate arrived two sizes off.", "Here is how we fixed the allowance without a fight."], "From The Jobsite")))

# ========== C. Micro-dose color (7) ==========
def color_screen(kind, accent, accent2=None, accent3=None):
    """Phone mock: white base with accent pops vs earthy/bw."""
    body = lbl(14, 48, "Customer App") + h1(14, 66, "Home Dashboard", 16)
    if kind == "one":
        body += rect(14, 80, 212, 56, "#FFFFFF", LINE, 6) + t(22, 100, "NEXT VISIT", 6.5, MUTE, "hind", 600)
        body += t(22, 118, "Tue, Nov 4 · 9 AM", 13, INK, "khand")
        body += tag(150, 96, "Due", accent, True)
        body += btn(250, "Book Visit", "fill", accent)
        body += t(14, 160, "One accent: button + due tag", 8, MUTE)
    elif kind == "two":
        body += rect(14, 80, 212, 56, "#FFFFFF", LINE, 6) + t(22, 100, "NEXT VISIT", 6.5, MUTE, "hind", 600)
        body += t(22, 118, "Tue, Nov 4 · 9 AM", 13, INK, "khand")
        body += tag(150, 96, "Info", accent) + tag(14, 150, "On Track", accent2 or JUNGLE, True)
        body += pbar(175, 0.65, accent)
        body += btn(250, "Continue", "fill", accent)
        body += t(14, 200, "Two accents: act + status", 8, MUTE)
    elif kind == "three":
        body += ring(70, 140, 36, 0.72, accent, "72%")
        body += tag(120, 100, "Act", accent, True)
        body += tag(120, 120, "Info", accent2 or LAGOON)
        body += tag(120, 140, "Done", accent3 or JUNGLE, True)
        body += btn(250, "See Plan", "fill", accent)
        body += t(14, 200, "Three small pops spread", 8, MUTE)
    elif kind == "earthy":
        body += rect(14, 80, 212, 56, "#EDE6DC", "#D4C4B0", 6) + t(22, 100, "NEXT VISIT", 6.5, "#7A6A58", "hind", 600)
        body += t(22, 118, "Tue, Nov 4 · 9 AM", 13, "#4A3F35", "khand")
        body += btn(250, "Book Visit", "fill", "#8B6914")
        body += t(14, 160, "All-earthy, no clear pop", 8, MUTE)
    elif kind == "bw":
        body += rect(14, 80, 212, 56, "#FFFFFF", "#111", 0) + t(22, 100, "NEXT VISIT", 6.5, MUTE, "hind", 600)
        body += t(22, 118, "Tue, Nov 4 · 9 AM", 13, INK, "khand")
        body += btn(250, "Book Visit", "fill", INK)
        body += t(14, 160, "Plain black and white", 8, MUTE)
    elif kind == "link":
        body += para(14, 90, ["Your furnace filter is due.", "Size: 16×25×1"], 10, INK)
        body += t(14, 140, "Order filter →", 11, accent, "hind", 600, extra='text-decoration="underline"')
        body += btn(250, "Open Record", "outline", INK)
        body += t(14, 170, "Accent only on the link", 8, MUTE)
    elif kind == "ring":
        body += ring(120, 150, 48, 0.4, accent, "Due")
        body += btn(250, "Schedule", "outline", accent)
        body += t(14, 220, "Accent on progress ring", 8, MUTE)
    return screen(body)

COLOR_PAIRS = [
    ("col_lagoon_one", "Lagoon Button And Tag", "White base, one lagoon pop on CTA and due tag.",
     ["clear", "fresh", "modern", "light"], color_screen("one", LAGOON),
     "col_earthy_all", "All-Earthy Dashboard", "Beige card, brown button, no clear color pop.",
     ["earthy", "warm", "soft", "quiet"], color_screen("earthy", "#8B6914")),
    ("col_persim_two", "Persimmon Plus Jungle", "Act in persimmon, status in jungle.",
     ["lively", "clear", "warm", "multi"], color_screen("two", PERSIM, JUNGLE),
     "col_bw_plain", "Plain Black And White", "Ink and white only, no accent.",
     ["minimal", "stark", "simple", "cold"], color_screen("bw", INK)),
    ("col_jungle_ring", "Jungle Progress Ring", "White base, jungle ring as the only pop.",
     ["calm", "clear", "natural", "focused"], color_screen("ring", JUNGLE),
     "col_saffron_one", "Saffron Due Tag And Button", "One saffron accent for due actions.",
     ["warm", "clear", "alert", "light"], color_screen("one", SAFFRON)),
    ("col_berry_link", "Berry Text Link", "Neutral screen, berry underline link only.",
     ["subtle", "editorial", "clear", "quiet"], color_screen("link", BERRY),
     "col_terra_one", "Terracotta CTA Only", "White base, terracotta fill button.",
     ["warm", "brand", "direct", "light"], color_screen("one", TERRA)),
    ("col_three_spread", "Three Micro Pops", "Terracotta act, lagoon info, jungle done.",
     ["lively", "multi", "clear", "system"], color_screen("three", TERRA, LAGOON, JUNGLE),
     "col_one_only", "Single Lagoon Pop", "Same layout with only lagoon.",
     ["simple", "focused", "calm", "clear"], color_screen("one", LAGOON)),
    ("col_lag2_two", "Teal Lagoon Plus Saffron", "Info teal and due saffron on white.",
     ["fresh", "multi", "clear", "modern"], color_screen("two", LAG2, SAFFRON),
     "col_earthy_soft", "Soft Earthy No Pop", "Cream and taupe only.",
     ["earthy", "soft", "home", "quiet"], color_screen("earthy", "#A08968")),
    ("col_persim_ring", "Persimmon Ring And Outline", "Progress ring and outline button in persimmon.",
     ["warm", "focused", "clear", "bold"], color_screen("ring", PERSIM),
     "col_bw_tags", "Black Tags On White", "Status as black chips, no hue.",
     ["minimal", "stark", "system", "cold"], color_screen("bw", INK)),
]
for a_id, a_lab, a_desc, a_tags, a_svg, b_id, b_lab, b_desc, b_tags, b_svg in COLOR_PAIRS:
    add("Color Accents", "Color Accents", "Customer Apps", "Which Color Accent Approach?",
        O(a_id, a_lab, a_desc, a_tags, Vsvg(a_svg)),
        O(b_id, b_lab, b_desc, b_tags, Vsvg(b_svg)))

# ========== D. Up Keep features (12) ==========
def uk_tiers(names):
    # names: list of (name, price, badge?)
    body = lbl(14, 48, "Plans") + h1(14, 66, "Pick Your Plan", 16)
    for i, (n, p, badge) in enumerate(names):
        x = 14 + i * 72
        body += rect(x, 84, 68, 130, SEL if badge else "#FFFFFF", INK if badge else LINE, 4, 1.5 if badge else 1)
        if badge: body += tag(x + 8, 78, badge, TERRA, True)
        body += t(x + 8, 110, n, 11, INK, "khand")
        body += t(x + 8, 130, p, 12, INK, "khand")
        body += para(x + 6, 148, ["2 visits", "Filters", "Reports"][:3], 7, MUTE, 11)
    body += btn(250, "Continue", "fill", INK)
    return screen(body)

def uk_price(monthly_first):
    body = lbl(14, 48, "Gold Plan") + h1(14, 66, "Your Price", 16)
    if monthly_first:
        body += t(14, 110, "$240", 36, INK, "khand") + t(100, 110, "/mo", 14, MUTE)
        body += t(14, 132, "$2,880 / year · Draft Price", 9, MUTE)
        body += tag(14, 150, "Draft Price", SAFFRON)
    else:
        body += t(14, 110, "$2,880", 36, INK, "khand") + t(130, 110, "/yr", 14, MUTE)
        body += t(14, 132, "$240 / month · Draft Price", 9, MUTE)
        body += tag(14, 150, "Draft Price", SAFFRON)
    body += btn(250, "Lock Founding Price", "fill", TERRA)
    return screen(body)

def uk_ask(ai_first):
    body = lbl(14, 48, "Ask Anything") + h1(14, 66, "Furnace Filter Size?", 14)
    if ai_first:
        body += rect(14, 88, 212, 70, LAGOON + "14", "none", 6)
        body += t(22, 110, "AI Answer", 7, LAGOON, "hind", 600)
        body += para(22, 126, ["Your Carrier uses 16×25×1.", "Last changed Oct 2."], 9, INK)
        body += btn(180, "Text A Human", "outline", INK)
        body += btn(220, "Looks Right", "fill", JUNGLE)
    else:
        body += rect(14, 88, 212, 70, "#FFFFFF", LINE, 6)
        body += icon_chat(22, 100, TERRA, 22)
        body += t(52, 112, "Text A Human First", 11, INK, "khand")
        body += para(52, 128, ["Danny usually replies", "within 1 hour."], 8, MUTE)
        body += btn(180, "Send To Team", "fill", TERRA)
        body += btn(220, "Try AI Answer", "outline", LAGOON)
    return screen(body)

def uk_urgent(fullscreen):
    if fullscreen:
        body = warn_tri(96, 50, PERSIM, 2.2)
        body += h1(120, 130, "Leave The Home", 18, PERSIM, "middle")
        body += para(30, 150, ["Gas smell, CO alarm, flooding,", "or sparking: call 911 or your", "utility before any form."], 9.5, INK)
        body += btn(220, "I Called 911", "fill", PERSIM)
        body += btn(258, "Back", "outline", MUTE)
        return screen(body, head=False, bg="#FFF8F5")
    body = lbl(14, 48, "Request Service") + h1(14, 66, "What Is Wrong?", 15)
    body += rect(14, 84, 212, 50, PERSIM + "18", "none", 4) + warn_tri(22, 92, PERSIM, 1.1)
    body += para(52, 100, ["Safety first: leave the home", "and call 911 if needed."], 8.5, INK)
    body += "".join(rect(14, 150 + i * 28, 212, 24, "#FFFFFF", LINE, 2) + t(24, 166 + i * 28, s, 9, INK)
                    for i, s in enumerate(["Gas smell", "Flooding", "Other issue"]))
    return screen(body)

def uk_waitlist(style):
    body = lbl(14, 48, "Out Of Area") + h1(14, 66, "Not In Metro Detroit Yet", 14)
    if style == "warm":
        body += rect(14, 90, 212, 100, CREAM, LINE, 6)
        body += para(24, 112, ["We are opening Wayne, Oakland,", "and Macomb first.", "", "Join the waitlist and we will", "email you when we reach you."], 9, INK)
        body += btn(220, "Join The Waitlist", "fill", LAGOON)
    else:
        body += para(14, 100, ["Your ZIP is outside our", "beta area."], 11, INK)
        body += rect(14, 140, 212, 40, "#FFFFFF", LINE, 0)
        body += t(24, 164, "you@email.com", 10, "#A3A3A3")
        body += btn(220, "Notify Me", "outline", INK)
    return screen(body)

def uk_photo_label(auto):
    body = lbl(14, 48, "Add Appliance") + h1(14, 66, "Rating Plate", 15)
    body += rect(14, 84, 212, 70, "#D9D4CB", "none", 4)
    body += rect(60, 96, 120, 46, "#F7F7F2", "#9E9E9E", 2)
    if auto:
        body += tag(14, 164, "Auto-Filled — Confirm", JUNGLE, True)
        body += para(14, 186, ["Brand: Carrier", "Model: 59SC5A", "Serial: 4910A228"], 9, INK)
        body += btn(250, "Looks Right", "fill", JUNGLE)
    else:
        body += para(14, 170, ["Enter fields manually first.", "Photo is optional backup."], 9, MUTE)
        for i, (lab, val) in enumerate([("Brand", ""), ("Model", ""), ("Serial", "")]):
            body += t(14, 210 + i * 18, lab + ": ________", 8.5, MUTE)
        body += btn(270, "Save", "fill", INK)
    return screen(body)

def uk_remind(channel):
    body = lbl(14, 48, "Reminders") + h1(14, 66, "How Should We Nudge?", 14)
    if channel == "email":
        body += rect(14, 90, 212, 80, "#FFFFFF", LAGOON, 4, 1.5)
        body += t(24, 112, "Email Primary", 12, INK, "khand")
        body += para(24, 130, ["3 days before each visit.", "SMS only as a backup."], 9, MUTE)
        body += check_box(24, 190, True, LAGOON) + t(42, 200, "Email on", 9, INK)
        body += check_box(24, 212, False) + t(42, 222, "SMS backup", 9, MUTE)
    else:
        body += rect(14, 90, 212, 80, "#FFFFFF", TERRA, 4, 1.5)
        body += t(24, 112, "SMS Primary", 12, INK, "khand")
        body += para(24, 130, ["Text 3 days before.", "Email is the weekly digest."], 9, MUTE)
        body += check_box(24, 190, True, TERRA) + t(42, 200, "SMS on", 9, INK)
        body += check_box(24, 212, False) + t(42, 222, "Email digest", 9, MUTE)
    body += btn(250, "Save Preferences", "fill", INK)
    return screen(body)

def uk_calendar(dense):
    body = lbl(14, 48, "Michigan Plan") + h1(14, 66, "12-Month Calendar", 15)
    months = ["N", "D", "J", "F", "M", "A"]
    tasks_busy = [3, 2, 4, 3, 2, 3]
    tasks_sparse = [1, 1, 2, 1, 1, 1]
    tasks = tasks_busy if dense else tasks_sparse
    for i, m in enumerate(months):
        x = 14 + (i % 3) * 72; y = 90 + (i // 3) * 70
        body += rect(x, y, 66, 60, "#FFFFFF", LINE, 4)
        body += t(x + 8, y + 16, m, 10, INK, "khand")
        for j in range(tasks[i]):
            body += rect(x + 8 + j * 12, y + 28, 10, 10, TERRA if dense else LAGOON, "none", 2)
        body += t(x + 8, y + 52, f"{tasks[i]} tasks", 7, MUTE)
    body += t(14, 240, "Busy seasonal plan" if dense else "Sparse seasonal plan", 8, MUTE)
    return screen(body)

def uk_warranty(chip):
    body = lbl(14, 48, "Home") + h1(14, 66, "Welcome Home", 16)
    body += rect(14, 80, 212, 50, CREAM, LINE, 6) + t(22, 100, "NEXT VISIT", 6.5, MUTE, "hind", 600)
    body += t(22, 118, "Tue, Nov 4 · 9 AM", 12, INK, "khand")
    if chip:
        body += tag(14, 144, "Warranty Ends In 48 Days", SAFFRON, True)
        body += t(14, 170, "Water Heater · A.O. Smith", 9, MUTE)
    else:
        body += ln(148) + t(14, 168, "Systems", 10, INK, "khand")
        body += t(14, 190, "Water Heater — warranty in list →", 9, MUTE)
    body += btn(250, "Open Record", "outline", INK)
    return screen(body)

def uk_founding(prom):
    body = lbl(14, 48, "Founding Member") + h1(14, 66, "Price Lock", 16)
    if prom:
        body += rect(14, 88, 212, 90, TERRA, "none", 6)
        body += t(24, 118, "PRICE LOCKED", 14, "#FFFFFF", "khand")
        body += t(24, 140, "12 Months", 22, "#FFFFFF", "khand")
        body += t(24, 162, "Gold · $240/mo draft", 9, "#FFFFFF")
    else:
        body += rect(14, 88, 212, 90, "#FFFFFF", LINE, 6)
        body += tag(24, 104, "Price Locked 12 Mo", MUTE)
        body += t(24, 140, "Gold · $240/mo draft", 14, INK, "khand")
        body += t(24, 160, "Quiet badge under the price.", 9, MUTE)
    body += btn(250, "Continue", "fill", INK)
    return screen(body)

def uk_share(style):
    body = lbl(14, 48, "Share") + h1(14, 66, "Send This Screen", 15)
    body += para(14, 90, ["Fixed share control at the", "bottom of every page."], 10, MUTE)
    if style == "square":
        body += rect(90, 160, 60, 60, "#FFFFFF", INK, 0, 2)
        body += t(120, 195, "SHARE", 10, INK, "hind", 600, "middle", 'letter-spacing="1"')
        body += t(120, 240, "Outlined square brand", 8, MUTE, anchor="middle")
    else:
        body += rect(70, 170, 100, 36, "#FFFFFF", LAGOON, 18, 1.5)
        body += t(120, 193, "Share", 12, LAGOON, "hind", 600, "middle")
        body += t(120, 240, "Softer pill", 8, MUTE, anchor="middle")
    return screen(body)

def uk_record(rooms_first):
    body = lbl(14, 48, "Home Record") + h1(14, 66, "Michigan Residence", 15)
    if rooms_first:
        items = [("Kitchen", "4 finishes"), ("Basement", "Furnace + WH"), ("Garage", "Panel"), ("Yard", "Gutters")]
        body += t(14, 90, "Rooms First", 9, LAGOON, "hind", 600)
    else:
        items = [("Furnace", "Carrier 59SC5"), ("Water Heater", "Rheem XG50"), ("AC", "Trane XR14"), ("Panel", "Square D 200A")]
        body += t(14, 90, "Appliances First", 9, TERRA, "hind", 600)
    for i, (a, b) in enumerate(items):
        body += ln(104 + i * 28) + t(14, 122 + i * 28, a, 10, INK) + t(226, 122 + i * 28, b, 8, MUTE, anchor="end")
    body += btn(250, "Add", "fill", INK)
    return screen(body)

UK = [
    ("Tier Names", "Silver/Gold/Platinum Or Essentials/Plus/Complete?",
     O("uk_tier_metal", "Silver / Gold / Platinum", "Metal names from pricing-48322.",
       ["clear", "classic", "premium", "simple"], Vsvg(uk_tiers([("Silver", "$90/mo", None), ("Gold", "$240", "Rec"), ("Plat", "$420", None)]))),
     O("uk_tier_plain", "Essentials / Plus / Complete", "Plain GTM plan names.",
       ["clear", "practical", "direct", "simple"], Vsvg(uk_tiers([("Essentials", "$90/mo", None), ("Plus", "$240", "Rec"), ("Complete", "$420", None)])))),
    ("Price Display", "Monthly-First Or Annual-First Price?",
     O("uk_price_mo", "Monthly First (Draft)", "Big monthly number, annual under it, Draft tag.",
       ["clear", "practical", "light", "direct"], Vsvg(uk_price(True))),
     O("uk_price_yr", "Annual First (Draft)", "Big annual number, monthly under it, Draft tag.",
       ["clear", "honest", "strong", "direct"], Vsvg(uk_price(False)))),
    ("Ask Anything", "AI Answer First Or Text A Human First?",
     O("uk_ask_ai", "AI Answer First", "Home-record AI reply on top; Text A Human second.",
       ["fast", "modern", "clear", "system"], Vsvg(uk_ask(True))),
     O("uk_ask_human", "Text A Human First", "Human path on top; AI as optional.",
       ["personal", "warm", "trust", "neighbor"], Vsvg(uk_ask(False)))),
    ("Urgent Safety", "Full-Screen Block Or Inline Warning?",
     O("uk_urg_full", "Full-Screen Safety Block", "Blocks the form until they confirm calling out.",
       ["safe", "strong", "clear", "direct"], Vsvg(uk_urgent(True))),
     O("uk_urg_inline", "Inline Warning On The Form", "Red banner above the issue list.",
       ["calm", "guided", "clear", "light"], Vsvg(uk_urgent(False)))),
    ("Out Of Area", "Which Waitlist Message Style?",
     O("uk_wait_warm", "Warm Waitlist Card", "Cream card explaining metro Detroit first.",
       ["warm", "friendly", "clear", "neighbor"], Vsvg(uk_waitlist("warm"))),
     O("uk_wait_plain", "Plain Notify Form", "Short ZIP message and email field.",
       ["simple", "direct", "minimal", "system"], Vsvg(uk_waitlist("plain")))),
    ("Photo Label", "Auto-Fill Confirm Or Manual Fields First?",
     O("uk_photo_auto", "Auto-Fill, Then Confirm", "AI fills brand/model/serial; member confirms.",
       ["fast", "modern", "easy", "clear"], Vsvg(uk_photo_label(True))),
     O("uk_photo_manual", "Manual Fields First", "Type fields; photo is optional backup.",
       ["control", "simple", "careful", "clear"], Vsvg(uk_photo_label(False)))),
    ("Reminders", "Email Or SMS As The Primary Reminder?",
     O("uk_rem_email", "Email Primary", "Email 3 days before; SMS backup only.",
       ["calm", "pro", "clear", "quiet"], Vsvg(uk_remind("email"))),
     O("uk_rem_sms", "SMS Primary", "Text 3 days before; email as digest.",
       ["direct", "fast", "personal", "clear"], Vsvg(uk_remind("sms")))),
    ("Calendar Density", "Busy Or Sparse Michigan Seasonal Plan?",
     O("uk_cal_busy", "Busy Seasonal Plan", "More Michigan tasks per month on the grid.",
       ["thorough", "guided", "system", "busy"], Vsvg(uk_calendar(True))),
     O("uk_cal_sparse", "Sparse Seasonal Plan", "Fewer, higher-signal tasks per month.",
       ["calm", "simple", "clear", "light"], Vsvg(uk_calendar(False)))),
    ("Warranty Expiry", "Home-Screen Chip Or List-Only?",
     O("uk_war_chip", "Home-Screen Warranty Chip", "Expiring warranty as a saffron chip on Home.",
       ["clear", "alert", "guided", "visual"], Vsvg(uk_warranty(True))),
     O("uk_war_list", "List-Only Warranty", "Warranty stays inside the record list.",
       ["quiet", "simple", "calm", "minimal"], Vsvg(uk_warranty(False)))),
    ("Founding Badge", "Prominent Or Quiet Price-Lock Badge?",
     O("uk_found_big", "Prominent Price-Lock Banner", "Full terracotta lock card.",
       ["bold", "clear", "warm", "strong"], Vsvg(uk_founding(True))),
     O("uk_found_quiet", "Quiet Price-Lock Chip", "Small muted chip under the price.",
       ["quiet", "minimal", "calm", "soft"], Vsvg(uk_founding(False)))),
    ("Share Button", "Outlined Square Brand Or Softer Pill?",
     O("uk_share_sq", "Outlined Square Share", "Brand square control at the bottom.",
       ["brand", "clear", "strong", "system"], Vsvg(uk_share("square"))),
     O("uk_share_pill", "Softer Pill Share", "Rounded pill with lagoon outline.",
       ["soft", "friendly", "light", "calm"], Vsvg(uk_share("pill")))),
    ("Home Record", "Rooms-First Or Appliances-First?",
     O("uk_rec_rooms", "Rooms First", "Kitchen, basement, garage as the top list.",
       ["guided", "home", "clear", "warm"], Vsvg(uk_record(True))),
     O("uk_rec_appl", "Appliances First", "Furnace, water heater, AC as the top list.",
       ["practical", "system", "clear", "direct"], Vsvg(uk_record(False)))),
]
for cat, ask, a, b in UK:
    add("Up Keep", cat if cat.startswith("Up Keep") else f"Up Keep: {cat}", "Up Keep", ask, a, b)

# ========== E. Swipe Controls (3) — fresh never-shown ==========
add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "Which Control Words Feel Right?",
    O("sc_words_passhold", "Pass / Hold / Love / Keep", "Plain verbs, no slang fire words.",
      ["clear", "direct", "practical", "calm"],
      Vctrl("pill", ["Pass", "Hold", "Love", "Keep"], ["«", "–", "♥", "✓"],
            [TERRA, SAFFRON, BERRY, LAGOON], "outline", "#ffffff", "Hind")),
    O("sc_words_leftright", "Left / Maybe / Love / Right", "Direction words matched to swipe sides.",
      ["clear", "guided", "simple", "modern"],
      Vctrl("pill", ["Left", "Maybe", "Love", "Right"], ["◀", "?", "♥", "▶"],
            [TERRA, SAFFRON, BERRY, JUNGLE], "filled", "#f4f1ea", "Khand")))

add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "Which Button Shape For Swipe Controls?",
    O("sc_shape_softrect", "Soft Rectangle Keys", "Slightly rounded rectangles, brand colors.",
      ["soft", "modern", "clear", "light"],
      Vctrl("square", ["No", "Maybe", "Love", "Yes"], ["✕", "?", "♥", "✓"],
            [TERRA, SAFFRON, BERRY, LAGOON], "filled", "#ffffff", "Hind")),
    O("sc_shape_capsule", "Full Capsule Pills", "Fully rounded capsules, outline style.",
      ["soft", "friendly", "calm", "light"],
      Vctrl("pill", ["No", "Maybe", "Love", "Yes"], ["✕", "?", "♥", "✓"],
            [TERRA, SAFFRON, BERRY, LAGOON], "outline", "#faf6ee", "Hind")))

add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "Which Stamp Style For A Choice?",
    O("sc_stamp_inkcircle", "Ink Circle Stamp", "Round ink stamp with the word inside.",
      ["tactile", "clear", "warm", "brand"],
      Vctrl("stamp", ["No", "Maybe", "Love", "Yes"], ["✕", "·", "♥", "✓"],
            [INK, MUTE, BERRY, JUNGLE], "outline", "#f4f1ea", "Khand")),
    O("sc_stamp_ticket", "Ticket Stub Stamp", "Small ticket-stub shape for each pick.",
      ["playful", "visual", "clear", "light"],
      Vctrl("stamp", ["Skip", "Hold", "Love", "Pick"], ["»", "–", "♥", "✓"],
            [TERRA, SAFFRON, BERRY, LAGOON], "filled", "#ffffff", "Hind")))

# ========== F1. Variety (9) — light/natural/warm ==========
def cafe_card(name, notes_line, accent):
    body = rect(0, 0, W, H, "#FFFFFF") + rect(0, 0, W, 110, "#E8DFD4")
    body += rect(20, 30, 80, 60, "#F7F4EE") + rect(110, 40, 100, 40, accent + "33")
    body += h1(14, 140, name, 16) + para(14, 160, [notes_line, "Natural light, quiet seats."], 9, MUTE)
    body += tag(14, 210, "Cafe", accent) + tag(70, 210, "Warm", TERRA)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def texture_card(label, fill, pattern="lines"):
    body = rect(0, 0, W, H, fill)
    if pattern == "lines":
        body += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#00000018" stroke-width="1"/>' for y in range(20, H, 12))
    elif pattern == "dots":
        body += "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#00000022"/>' for x in range(12, W, 14) for y in range(12, H, 14))
    elif pattern == "weave":
        body += "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#00000014" stroke-width="3"/>' for x in range(8, W, 10))
    body += rect(0, 220, W, 80, "#FFFFFFCC") + h1(14, 250, label, 16) + t(14, 272, "Material sample", 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def travel_card(place, sky, tip):
    body = rect(0, 0, W, 160, sky) + rect(0, 140, W, 160, "#F7F4EE")
    body += rect(40, 80, 160, 70, "#FFFFFF") + rect(100, 100, 20, 50, "#6B4B3A")  # simple building
    body += h1(14, 190, place, 16) + para(14, 210, [tip], 9, MUTE)
    body += tag(14, 250, "Travel", LAGOON)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def nursery_card(style):
    body = rect(0, 0, W, H, "#FAF6EE")
    if style == "natural":
        body += rect(20, 40, 200, 120, "#E5EDE4") + rect(50, 80, 60, 50, "#F7F4EE") + rect(130, 70, 50, 60, "#D4C4B0")
        body += h1(14, 200, "Natural Nursery", 16) + para(14, 220, ["Wood crib, linen, soft green."], 9, MUTE)
    else:
        body += rect(20, 40, 200, 120, "#F3ECE1") + rect(40, 70, 160, 20, "#FFFFFF") + rect(40, 100, 100, 40, "#E8DFD4")
        body += h1(14, 200, "Warm Cream Nursery", 16) + para(14, 220, ["Cream walls, oak, quiet textiles."], 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def watch_card(style):
    body = rect(0, 0, W, H, "#FFFFFF")
    body += f'<circle cx="120" cy="120" r="70" fill="none" stroke="{INK}" stroke-width="3"/>'
    if style == "field":
        body += f'<circle cx="120" cy="120" r="58" fill="#F4F1EA"/><circle cx="120" cy="120" r="4" fill="{INK}"/>'
        body += t(120, 210, "Field Watch", 14, INK, "khand", anchor="middle")
        body += t(120, 230, "Cream dial, clean marks", 9, MUTE, anchor="middle")
    else:
        body += f'<circle cx="120" cy="120" r="58" fill="#FFFFFF"/><rect x="118" y="70" width="4" height="30" fill="{TERRA}"/>'
        body += t(120, 210, "Dress Watch", 14, INK, "khand", anchor="middle")
        body += t(120, 230, "White dial, terracotta second", 9, MUTE, anchor="middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

add("Variety", "Cafés", "Style Profile", "Which Cafe Mood Fits?",
    O("var_cafe_light", "Bright Corner Cafe", "White walls, wood, lagoon cup accent.",
      ["light", "natural", "warm", "calm"], Vsvg(cafe_card("Bright Corner", "White oak and morning light.", LAGOON))),
    O("var_cafe_garden", "Garden Patio Cafe", "Greenery edge, terracotta planter pop.",
      ["natural", "warm", "outdoor", "calm"], Vsvg(cafe_card("Garden Patio", "Shade trees and quiet tables.", TERRA))))

add("Variety", "Textures & Materials", "Style Profile", "Which Material Feels Better?",
    O("var_tx_linen", "Natural Linen", "Open weave, warm off-white.",
      ["natural", "light", "soft", "calm"], Vsvg(texture_card("Natural Linen", "#F3ECE1", "weave"))),
    O("var_tx_plaster", "Warm Lime Plaster", "Soft mineral wall, cream tone.",
      ["natural", "warm", "quiet", "home"], Vsvg(texture_card("Warm Lime Plaster", "#EDE6DC", "dots"))))

add("Variety", "Travel & Hotel Vibes", "Style Profile", "Which Travel Mood?",
    O("var_tv_coast", "Quiet Coast Town", "Soft blue sky, white building, calm stay.",
      ["light", "calm", "natural", "travel"], Vsvg(travel_card("Quiet Coast", "#CFE3EE", "Walkable, bright, low-key."))),
    O("var_tv_hill", "Hill Town Morning", "Warm sky, stone, early light.",
      ["warm", "natural", "travel", "quiet"], Vsvg(travel_card("Hill Town", "#F2D9BF", "Stone streets, slow coffee."))))

add("Variety", "Kids' Room & Nursery", "Style Profile", "Which Nursery Direction?",
    O("var_kd_natural", "Natural Nursery", "Wood, linen, soft green — no loud color.",
      ["natural", "calm", "light", "warm"], Vsvg(nursery_card("natural"))),
    O("var_kd_cream", "Warm Cream Nursery", "Cream walls, oak, quiet textiles.",
      ["warm", "soft", "light", "home"], Vsvg(nursery_card("cream"))))

add("Variety", "Watches & EDC", "Style Profile", "Which Watch Direction?",
    O("var_wa_field", "Field Watch, Cream Dial", "Practical marks, light dial.",
      ["practical", "clear", "light", "calm"], Vsvg(watch_card("field"))),
    O("var_wa_dress", "Dress Watch, Terracotta Second", "White dial, one micro-dose hand.",
      ["clear", "warm", "simple", "modern"], Vsvg(watch_card("dress"))))


def light_card(style):
    if style == "day":
        body = rect(0, 0, W, H, "#F7F4EE") + rect(0, 0, W, 100, "#CFE3EE")
        body += rect(30, 80, 180, 100, "#FFFFFF") + rect(50, 100, 40, 60, "#E8DFD4")
        body += h1(14, 220, "Daylight Room", 16, INK) + para(14, 242, ["Soft sky light, pale walls."], 9, MUTE)
    else:
        body = rect(0, 0, W, H, "#F3ECE1") + f'<ellipse cx="120" cy="90" rx="55" ry="24" fill="{SAFFRON}33"/>'
        body += f'<circle cx="120" cy="110" r="18" fill="{SAFFRON}"/>' + rect(114, 128, 12, 40, "#6B4B3A")
        body += h1(14, 220, "Warm Lamp Glow", 16, INK) + para(14, 242, ["Evening pool of warm light."], 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def food_card(style):
    body = rect(0, 0, W, H, "#FFFFFF")
    if style == "simple":
        body += f'<ellipse cx="120" cy="120" rx="70" ry="50" fill="#F3ECE1" stroke="{LINE}"/>'
        body += f'<circle cx="100" cy="110" r="12" fill="{JUNGLE}"/><circle cx="130" cy="115" r="10" fill="{TERRA}"/>'
        body += h1(14, 210, "Simple Plate", 16) + para(14, 232, ["Few ingredients, clear colors."], 9, MUTE)
    else:
        body += rect(40, 50, 160, 120, "#EDE6DC") + rect(60, 70, 120, 80, "#F7F4EE")
        body += tag(70, 100, "Shared", TERRA, True)
        body += h1(14, 210, "Shared Table", 16) + para(14, 232, ["Family-style bowls, warm wood."], 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def plant_card(style):
    body = rect(0, 0, W, H, "#FAF6EE")
    if style == "one":
        body += f'<rect x="100" y="160" width="40" height="30" fill="{TERRA}"/>'
        body += f'<ellipse cx="120" cy="120" rx="40" ry="50" fill="{JUNGLE}"/>'
        body += h1(14, 220, "One Tall Plant", 16) + para(14, 242, ["Single statement green."], 9, MUTE)
    else:
        for i, x in enumerate([50, 100, 150]):
            body += f'<rect x="{x}" y="150" width="28" height="22" fill="#D4C4B0"/>'
            body += f'<ellipse cx="{x+14}" cy="120" rx="22" ry="28" fill="{JUNGLE if i!=1 else LAG2}"/>'
        body += h1(14, 220, "Small Plant Cluster", 16) + para(14, 242, ["Three pots, mixed greens."], 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

def book_card(style):
    body = rect(0, 0, W, H, "#FFFFFF")
    if style == "photo":
        body += rect(50, 30, 140, 180, "#E8DFD4") + rect(60, 40, 120, 90, "#CFE3EE")
        body += h1(60, 160, "Jobsite", 14) + para(60, 178, ["Photo-led cover"], 8, MUTE)
        body += t(14, 240, "Photo Cover", 14, INK, "khand") + t(14, 260, "Big image, short title", 9, MUTE)
    else:
        body += rect(50, 30, 140, 180, INK) + t(120, 110, "FLAT", 18, "#FFFFFF", "khand", anchor="middle")
        body += t(120, 135, "FEE", 18, "#FFFFFF", "khand", anchor="middle")
        body += t(14, 240, "Type Cover", 14, INK, "khand") + t(14, 260, "Bold words, no photo", 9, MUTE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)">{body}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

add("Variety", "Lighting Moods", "Style Profile", "Which Lighting Mood?",
    O("var_lt_day", "Daylight Room", "Soft sky light and pale walls.",
      ["light", "natural", "calm", "clear"], Vsvg(light_card("day"))),
    O("var_lt_lamp", "Warm Lamp Glow", "Evening pool of warm light.",
      ["warm", "cozy", "quiet", "home"], Vsvg(light_card("lamp"))))

add("Variety", "Food & Table", "Style Profile", "Which Table Style?",
    O("var_fd_simple", "Simple Plate", "Few ingredients, clear colors.",
      ["simple", "clear", "light", "practical"], Vsvg(food_card("simple"))),
    O("var_fd_shared", "Shared Table", "Family-style bowls on warm wood.",
      ["warm", "friendly", "natural", "home"], Vsvg(food_card("shared"))))

add("Variety", "Plants & Greenery", "Style Profile", "Which Plant Setup?",
    O("var_pl_one", "One Tall Plant", "Single statement green in terracotta.",
      ["simple", "natural", "calm", "focused"], Vsvg(plant_card("one"))),
    O("var_pl_cluster", "Small Plant Cluster", "Three pots, mixed greens.",
      ["lively", "natural", "warm", "home"], Vsvg(plant_card("cluster"))))

add("Variety", "Book & Magazine Covers", "Style Profile", "Which Cover Direction?",
    O("var_bk_photo", "Photo-Led Cover", "Big jobsite photo, short title.",
      ["visual", "story", "warm", "clear"], Vsvg(book_card("photo"))),
    O("var_bk_type", "Type-Led Cover", "Bold words on ink, no photo.",
      ["strong", "direct", "clear", "brand"], Vsvg(book_card("type"))))


# ========== F2. Niko & Vivian function (3) ==========
def nv_screen(app_name, title, body_svg):
    head = rect(0, 0, W, 36, "#FFFFFF") + t(14, 24, app_name.upper(), 10, INK, "khand") + ln(36, 0, W)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="#FFFFFF"/>{head}{body_svg}</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>'

# Warranty list layout — Home Guide
add("Niko Vivian", "Warranty List", "Home Guide", "How Should Warranties List On Home Guide?",
    O("nv_war_cards", "Warranty Cards With Dates", "Each warranty as a card with end date and status chip.",
      ["clear", "guided", "visual", "practical"],
      Vsvg(nv_screen("Home Guide", "Warranties",
                     h1(14, 60, "Warranties", 16)
                     + rect(14, 78, 212, 50, "#FFFFFF", LINE, 4) + t(24, 98, "Roof · Owens Corning", 10, INK) + tag(24, 108, "Ends 2034", JUNGLE)
                     + rect(14, 138, 212, 50, "#FFFFFF", LINE, 4) + t(24, 158, "Water Heater", 10, INK) + tag(24, 168, "Ends In 60 Days", SAFFRON, True)
                     + btn(250, "Add Warranty", "outline", INK)))),
    O("nv_war_table", "Compact Date Table", "One tight table: item, start, end.",
      ["simple", "system", "dense", "clear"],
      Vsvg(nv_screen("Home Guide", "Warranties",
                     h1(14, 60, "Warranties", 16)
                     + lbl(14, 80, "Item") + lbl(120, 80, "End")
                     + "".join(ln(90 + i * 28) + t(14, 108 + i * 28, a, 9, INK) + t(226, 108 + i * 28, b, 9, MUTE, anchor="end")
                               for i, (a, b) in enumerate([("Roof", "2034"), ("Water Heater", "2027"), ("HVAC", "2029"), ("Windows", "2031")]))
                     + btn(250, "Add", "fill", INK)))))

# Shutoff labeling — Home Guide / Site Walk
add("Niko Vivian", "Shutoff Labels", "Home Guide", "How Should Water And Gas Shutoffs Be Labeled?",
    O("nv_shut_photo", "Photo Plus Big Label", "Photo of the valve with a large name tag.",
      ["clear", "visual", "guided", "safe"],
      Vsvg(nv_screen("Home Guide", "Shutoffs",
                     h1(14, 60, "Main Water Shutoff", 14)
                     + rect(14, 78, 212, 100, "#DCE9F0", "none", 4) + rect(90, 110, 60, 40, "#8A8A8A", INK, 2)
                     + tag(14, 190, "Basement · North Wall", LAGOON, True)
                     + btn(250, "Show Gas Next", "fill", TERRA)))),
    O("nv_shut_list", "Text List With Room Only", "Name and room in a simple list, no photo.",
      ["simple", "fast", "minimal", "clear"],
      Vsvg(nv_screen("Home Guide", "Shutoffs",
                     h1(14, 60, "Shutoffs", 16)
                     + "".join(ln(80 + i * 36) + t(14, 102 + i * 36, a, 11, INK, "khand") + t(226, 102 + i * 36, b, 9, MUTE, anchor="end")
                               for i, (a, b) in enumerate([("Main Water", "Basement"), ("Gas Meter", "Exterior"), ("HVAC Power", "Utility")]))
                     + btn(250, "Edit", "outline", INK)))))

# Finish question skip reason — Finish Questions
add("Niko Vivian", "Finish Skip Reason", "Finish Questions", "When Skipping A Finish Question, Ask Why?",
    O("nv_skip_reason", "Ask For A Skip Reason", "Optional chips: Later, N/A, Need Sample, Other + notes.",
      ["guided", "thorough", "clear", "practical"],
      Vsvg(nv_screen("Finish Questions", "Skip",
                     h1(14, 60, "Skip This Question?", 14)
                     + para(14, 84, ["Kitchen backsplash brand"], 9, MUTE)
                     + "".join(chip_y(14 + (i % 2) * 110, 110 + (i // 2) * 36, s) for i, s in enumerate(["Later", "N/A", "Need Sample", "Other"]))
                     + btn(250, "Skip With Reason", "fill", LAGOON)))),
    O("nv_skip_plain", "Skip With No Reason", "One Skip button; no why step.",
      ["simple", "fast", "light", "calm"],
      Vsvg(nv_screen("Finish Questions", "Skip",
                     h1(14, 60, "Kitchen Backsplash", 14)
                     + para(14, 90, ["Brand and color still open."], 10, MUTE)
                     + btn(200, "Answer", "fill", INK)
                     + btn(240, "Skip", "outline", MUTE)))))

# ---- order: shuffle with no same group twice in a row ----
random.seed(1310)
seq = list(pairs)
random.shuffle(seq)
order = []
while seq:
    k = next((i for i, p in enumerate(seq) if not order or p["group"] != order[-1]["group"]), 0)
    order.append(seq.pop(k))
from trim_deck import DECK_SIZE, select, save_overflow  # decks are 25 pairs; extras go to banks/overflow
order, _cut = select(order, DECK_SIZE); save_overflow(DID, _cut)
for i, p in enumerate(order, 1):
    p.update(id=f"{DID}-{i:02d}", repeat=False)

alloc, groups = {}, {}
for p in order:
    alloc[p["category"]] = alloc.get(p["category"], 0) + 1
    groups[p["group"]] = groups.get(p["group"], 0) + 1
apps = {}
for p in order:
    apps[p["app"]] = apps.get(p["app"], 0) + 1
ids = [p["option" + s]["id"] for p in order for s in "AB"]
assert len(order) == DECK_SIZE, len(order)
assert len(ids) == len(set(ids)), "duplicate option id"
ledger = json.load(open("shown_options.json"))
shown = {k for k, v in ledger.get("options", {}).items() if v != [DID]}
for fp in glob.glob("decks/*.json"):
    if os.path.basename(fp) == f"{DID}.json":
        continue
    for pp in json.load(open(fp)).get("pairs", []):
        for s in "AB":
            o = pp.get("option" + s) or {}
            if o.get("id"):
                shown.add(o["id"])
rep = [i for i in ids if i in shown]
assert not rep, f"repeats: {rep}"
assert all(p["option" + s]["tags"] for p in order for s in "AB")
now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
deck = {
    "date": DID,
    "version": 4,
    "owner": "Max Weberman",
    "format": "pairs",
    "english_only": True,
    "light_only": True,
    "title": "Daily 2026-10-13: Blog Topics, Writing Style, Micro-Dose Color, Up Keep Features, Variety, Swipe Controls",
    "brands": [
        "maxweberman.com base: Khand/Hind, light only, English only",
        "Micro-dose color: white/neutral base with small clear pops (no neon, no pastel, not all-beige)",
        "Up Keep / Smart Upkeep feature this-or-that block",
    ],
    "generated_at": now,
    "builds_on": "Queue blog topics + writing style; color accent one-time; standing Up Keep features; variety + swipe controls; Niko/Vivian function",
    "allocation": alloc,
    "groups": groups,
    "apps": apps,
    "pair_mix": {
        "refine": sum(p["purpose"] == "refine" for p in order),
        "check": sum(p["purpose"] == "check" for p in order),
        "retest": sum(p["retest"] for p in order),
    },
    "freshness": {"option_slots": len(ids), "never_shown_before": len(ids), "share": 1.0},
    "warnings": [],
    "pairs": order,
}
json.dump(deck, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
opts = ledger["options"]
for k in [k for k, v in opts.items() if v == [DID]]:
    del opts[k]
for i in ids:
    opts[i] = [DID]
ledger["options"] = dict(sorted(opts.items()))
ledger["shown_count"] = len(opts)
ledger["updated"] = now
json.dump(ledger, open("shown_options.json", "w"), indent=1)
print(len(order), "pairs")
print("groups", groups)
print("allocation", alloc)
print("apps", apps)
