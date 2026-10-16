#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-1: 25 this-or-that pairs centered on the Up Keep / Smart Upkeep home maintenance
membership app (https://webermanapps.github.io/smart-upkeep/). Mock screens are drawn as SVG in Up Keep's own style
(white base, #0A0A0A ink, square black buttons, Khand headings, Hind body, terracotta accent, #E5E0D8 rules) and
rendered through the 'hm' svg renderer. Run from the style-swipe repo root."""
import json, random, re, datetime as dt
DID = "upkeep-1"; LOGOS = "/workspace/brand/smart-upkeep/logos"
INK = "#0A0A0A"; MUTE = "#525252"; LINE = "#E5E0D8"; CREAM = "#FAF6EE"; SEL = "#F3E8DC"; W, H = 240, 300
TERRA = "#C1502E"; LAGOON = "#05668D"; LAG2 = "#00A6A6"; JUNGLE = "#0B6E4F"; SAFFRON = "#D4A017"; BERRY = "#9B2D5B"; PERSIM = "#E4572E"; TEAL = "#4F8A8B"
K = 'font-family="Khand" font-weight="700"'; HD = 'font-family="Hind"'
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def t(x, y, s, size=10, col=INK, f="hind", w=400, anchor="start", extra=""):
    fam = K if f == "khand" else (f'{HD} font-weight="{w}"' if f == "hind" else f'font-family="{f}"')
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {fam} {extra}>{esc(s)}</text>'
def lbl(x, y, s, col=MUTE, size=7): return t(x, y, s.upper(), size, col, "hind", 600, extra='letter-spacing="1"')
def h1(x, y, s, size=20, col=INK, anchor="start"):
    maxw = 212 if anchor == "middle" else 226 - x; size = min(size, round(maxw / (len(s) * .47), 1))
    return t(x, y, s, size, col, "khand", anchor=anchor)
def para(x, y, lines, size=8.5, col=MUTE, lh=None):
    lh = lh or size * 1.35; return "".join(t(x, y + i * lh, l, size, col) for i, l in enumerate(lines))
def rect(x, y, w, h, fill="none", stroke="none", r=0, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def btn(y, s, style="fill", col=INK, x=14, w=212, h=26, size=9):
    bg, fg = (col, "#FFFFFF") if style == "fill" else ("#FFFFFF", col)
    return rect(x, y, w, h, bg, col, 0, 1.5) + t(x + w / 2, y + h / 2 + size * .36, s.upper(), size, fg, "hind", 600, "middle", 'letter-spacing="1.2"')
def link(x, y, s, col=TERRA, anchor="start", size=7.5):
    return t(x, y, s.upper(), size, col, "hind", 600, anchor, 'letter-spacing="1" text-decoration="underline"')
def roof_logo(x, y, s=1, c=INK, up=MUTE):
    return (f'<g transform="translate({x},{y}) scale({s})">' + t(0, 0, "smart", 13, c, "khand") + t(29, 0, "up", 13, up, "khand")
            + f'<polyline points="27,-8 35.5,-14 44,-8" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' + t(44, 0, "keep", 13, c, "khand") + "</g>")
def hdr(right="", c=INK, up=MUTE):
    r = right or (rect(150, 9, 78, 13, "#F5F5F5", LINE, 6.5) + t(189, 18, "PROTOTYPE PRICING", 5.5, MUTE, "hind", 600, "middle", 'letter-spacing=".6"'))
    return roof_logo(14, 21, 1, c, up) + r + f'<line x1="0" y1="31" x2="{W}" y2="31" stroke="{LINE}"/>'
def screen(body, bg="#FFFFFF", head=True, right="", hc=INK, up=MUTE):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-width:100%;height:auto">'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{bg}"/>'
            + (hdr(right, hc, up) if head else "") + body + f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
def pbar(y, frac, col=INK, x=14, w=212): return rect(x, y, w, 4, "#EEEAE4", "none", 2) + rect(x, y, w * frac, 4, col, "none", 2)
def dots(y, n, cur, col=INK, cx=W / 2):
    x0 = cx - (n - 1) * 7; return "".join(f'<circle cx="{x0+i*14}" cy="{y}" r="{4 if i==cur else 3}" fill="{col if i<=cur else "#FFFFFF"}" stroke="{col if i<=cur else "#BDB6AA"}" stroke-width="1.2"/>' for i in range(n))
def field(y, label, val="", x=14, w=212):
    return lbl(x, y, label) + rect(x, y + 4, w, 20, "#FFFFFF", "#CFC8BC", 0) + t(x + 6, y + 17, val, 8.5, INK if val else "#A3A3A3")
def toggle(x, y, on, col=TERRA):
    return rect(x, y, 22, 12, col if on else "#D4D4D4", "none", 6) + f'<circle cx="{x+(16 if on else 6)}" cy="{y+6}" r="4.5" fill="#FFFFFF"/>'
def photo(x, y, w, h, kind="house", r=6, tone="day"):
    sky = {"day": ("#CFE3EE", "#F4F1EA"), "warm": ("#F2D9BF", "#FBF2E6"), "mute": ("#DCDCD8", "#F2F1EE")}[tone]
    gid = f"g{abs(hash((x, y, w, h, kind, tone))) % 99999}"
    s = f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset="1" stop-color="{sky[1]}"/></linearGradient><clipPath id="k{gid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath></defs><g clip-path="url(#k{gid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/>'
    if kind == "house":
        bx, by, bw = x + w * .22, y + h * .42, w * .56
        s += f'<rect x="{x}" y="{y+h*.8}" width="{w}" height="{h*.2}" fill="#9DB58A"/><path d="M{bx-6} {by} L{bx+bw/2} {y+h*.16} L{bx+bw+6} {by} Z" fill="#5B5550"/><rect x="{bx}" y="{by}" width="{bw}" height="{h*.4}" fill="#F7F4EE"/><rect x="{bx+bw*.42}" y="{by+h*.16}" width="{bw*.16}" height="{h*.24}" fill="#6B4B3A"/><rect x="{bx+bw*.1}" y="{by+h*.1}" width="{bw*.2}" height="{h*.12}" fill="#B8CCD8"/><rect x="{bx+bw*.7}" y="{by+h*.1}" width="{bw*.2}" height="{h*.12}" fill="#B8CCD8"/><circle cx="{x+w*.1}" cy="{y+h*.7}" r="{h*.14}" fill="#7E9C6B"/><circle cx="{x+w*.9}" cy="{y+h*.68}" r="{h*.16}" fill="#7E9C6B"/>'
    elif kind == "tech":
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#E8E2D8"/><rect x="{x+w*.52}" y="{y+h*.12}" width="{w*.3}" height="{h*.8}" rx="6" fill="#F8F8F6" stroke="#BDB6AA"/><rect x="{x+w*.58}" y="{y+h*.3}" width="{w*.18}" height="{h*.08}" fill="#8A8A8A"/><circle cx="{x+w*.3}" cy="{y+h*.34}" r="{h*.13}" fill="#C79B7B"/><path d="M{x+w*.1} {y+h} Q{x+w*.12} {y+h*.5} {x+w*.3} {y+h*.5} Q{x+w*.48} {y+h*.5} {x+w*.5} {y+h} Z" fill="#3E4A52"/><path d="M{x+w*.4} {y+h*.7} L{x+w*.6} {y+h*.36}" stroke="#7A7A7A" stroke-width="4" stroke-linecap="round"/>'
    elif kind == "interior":
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F3ECE1"/><rect x="{x}" y="{y+h*.75}" width="{w}" height="{h*.25}" fill="#C9A882"/><rect x="{x+w*.1}" y="{y+h*.15}" width="{w*.3}" height="{h*.4}" fill="#DCE9F0" stroke="#FFFFFF" stroke-width="3"/><rect x="{x+w*.5}" y="{y+h*.5}" width="{w*.4}" height="{h*.25}" rx="4" fill="#8C9A8A"/><circle cx="{x+w*.8}" cy="{y+h*.3}" r="{h*.07}" fill="#E8C77A"/>'
    elif kind == "label":
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#D9D4CB"/><rect x="{x+w*.2}" y="{y+h*.2}" width="{w*.6}" height="{h*.6}" rx="3" fill="#F7F7F2" stroke="#9E9E9E"/>' + "".join(f'<rect x="{x+w*.26}" y="{y+h*(.3+i*.1)}" width="{w*(.48 if i%2 else .34)}" height="{h*.04}" fill="#6E6E6E"/>' for i in range(5))
    return s + "</g>"
def icon(kind, x, y, s=18, style="outline", c=TERRA):
    sw = 1.8; g = f'<g transform="translate({x},{y}) scale({s/24})">'
    fill = c + "33" if style == "duo" else "none"; st = c if style == "duo" else INK
    P = {"furnace": f'<rect x="5" y="3" width="14" height="18" rx="2" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><path d="M9 14 q3 -6 3 -2 q3 -3 3 2 q-3 4 -6 0" fill="{c if style=="duo" else "none"}" stroke="{st}" stroke-width="{sw*.8}"/>',
         "water": f'<rect x="7" y="2" width="10" height="20" rx="5" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><path d="M12 9 q-3 4 0 6 q3 -2 0 -6" fill="{c if style=="duo" else "none"}" stroke="{st}" stroke-width="{sw*.8}"/>',
         "ac": f'<rect x="3" y="6" width="18" height="12" rx="2" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><circle cx="12" cy="12" r="3.5" fill="none" stroke="{st}" stroke-width="{sw*.8}"/>',
         "smoke": f'<circle cx="12" cy="12" r="9" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><circle cx="12" cy="12" r="2.5" fill="{c if style=="duo" else st}"/>',
         "phone": f'<path d="M6 3 h4 l2 5 -3 2 q2 4 5 5 l2 -3 5 2 v4 q0 2 -2 2 Q5 19 4 5 q0 -2 2 -2Z" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>',
         "chat": f'<path d="M4 5 h16 v10 h-9 l-5 4 v-4 h-2 Z" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round"/>',
         "check": f'<circle cx="12" cy="12" r="10" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><path d="M7 12.5 l3.5 3.5 6.5 -7" fill="none" stroke="{c if style=="duo" else st}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
         "cam": f'<rect x="3" y="7" width="18" height="13" rx="2" fill="{fill}" stroke="{st}" stroke-width="{sw}"/><circle cx="12" cy="13.5" r="3.5" fill="none" stroke="{st}" stroke-width="{sw}"/><path d="M8 7 l1.5 -3 h5 l1.5 3" fill="none" stroke="{st}" stroke-width="{sw}"/>'}
    return g + P[kind] + "</g>"
def ring(cx, cy, r, frac, col, label=""):
    import math
    a = 2 * math.pi * frac; x2, y2 = cx + r * math.sin(a), cy - r * math.cos(a)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEAE4" stroke-width="5"/><path d="M{cx} {cy-r} A{r} {r} 0 {1 if frac>.5 else 0} 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>' + t(cx, cy + 4, label, 11, INK, "khand", anchor="middle"))
def tag(x, y, s, col, solid=False):
    w = len(s) * 4.4 + 10
    return rect(x, y, w, 11, col if solid else col + "1F", "none", 5.5) + t(x + w / 2, y + 8, s.upper(), 5.8, "#FFFFFF" if solid else col, "hind", 600, "middle", 'letter-spacing=".6"')
def sticky(content, y=258): return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="#FFFFFF"/><line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{LINE}"/><rect x="0" y="{y-6}" width="{W}" height="6" fill="#0A0A0A" opacity=".04"/>' + content

pairs = []
def O(i, label, desc, tags, feel, svg, bg="#F7F4EF"):
    return {"id": "uk1_" + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": bg}}
def add(group, cat, a, b, ask, purpose="refine", retest=False):
    pairs.append({"group": group, "category": cat, "app": "Up Keep", "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": retest})
G1, G2, G3, G4, G5, G6, G7 = "Open Choices", "Micro-Dose Color", "Retest", "Voice & Headlines", "Logo", "Photos, Screens & Email", "Swipe Controls"

# ===================== 1. Up Keep's open choices (16) =====================
add(G1, "Up Keep: Intro Video",
 O("video_autoplay", "Video Autoplays As An Overlay", "The explainer starts on its own, muted with captions, over the page. Skip in the corner.", ["bold", "modern", "direct"], "system",
   screen(photo(0, 32, W, 190, "house", 0) + rect(0, 32, W, 190, "#0A0A0A", extra='opacity=".28"') + rect(176, 42, 52, 15, "#FFFFFF", r=7.5) + t(202, 52, "SKIP ›", 6.5, INK, "hind", 600, "middle")
          + rect(14, 180, 160, 26, "#0A0A0A", r=3, extra='opacity=".7"') + t(20, 191, "Every system in your house,", 7.5, "#FFFFFF") + t(20, 201, "checked on schedule.", 7.5, "#FFFFFF")
          + rect(14, 216, 212, 3, "#FFFFFF", extra='opacity=".5"') + rect(14, 216, 70, 3, TERRA) + t(20, 236, "🔇 Tap for sound", 7.5, MUTE) + btn(254, "Get My Estimate"))),
 O("video_tap", "Tap-To-Play Hero", "A still photo with a play button. Nothing moves until they tap.", ["calm", "clear", "minimal"], "concierge",
   screen(photo(14, 42, 212, 120, "house") + f'<circle cx="120" cy="102" r="17" fill="#FFFFFF" opacity=".92"/><path d="M115 93 L128 102 L115 111 Z" fill="{INK}"/>' + t(120, 154, "WATCH · 0:48", 6.5, "#FFFFFF", "hind", 600, "middle")
          + h1(14, 190, "Your House, Checked Every Season") + para(14, 206, ["Licensed techs, a set schedule and a photo", "report after every visit."]) + btn(240, "Get My Estimate"))),
 "How Should The Intro Video Start?")
add(G1, "Up Keep: Questions",
 O("q_one", "One Question Per Screen", "Big single question, one input, Next. A thin bar shows how far along.", ["clear", "calm", "focused"], "system",
   screen(link(14, 50, "← Back", INK) + pbar(60, .2) + lbl(14, 82, "Question 1 of 5") + h1(14, 104, "What's Your ZIP Code?", 21) + para(14, 120, ["We only serve homes we can reach fast."]) + rect(14, 132, 212, 30, "#FFFFFF", "#0A0A0A", 0, 1.5) + t(22, 151, "48322", 12, INK) + btn(176, "Next"))),
 O("q_form", "One Short Form", "All five questions on one page. Fill it in and press one button.", ["direct", "efficient", "practical"], "crew",
   screen(h1(14, 56, "Tell Us About Your Home", 18) + field(70, "ZIP code", "48322") + field(100, "Home size", "2,400 sq ft") + field(130, "Furnaces", "1") + field(160, "Water heaters", "1 tank") + field(190, "AC units", "") + btn(226, "See My Estimate"))),
 "Which Question Flow?")
def tiercard(x, y, w, h, name, price, per, feats, hi=False, badge=None, col=INK, acc=TERRA):
    s = rect(x, y, w, h, SEL if hi else "#FFFFFF", INK if hi else LINE, 4, 1.5 if hi else 1)
    if badge: s += rect(x + 8, y - 6, len(badge) * 4.3 + 10, 12, acc, r=6) + t(x + 13 + len(badge) * 2.15, y + 2, badge.upper(), 5.8, "#FFFFFF", "hind", 600, "middle")
    s += h1(x + 8, y + 22, name, 14) + t(x + 8, y + 40, price, 15, INK, "khand") + t(x + 8 + len(price) * 6.4, y + 40, per, 7, MUTE)
    return s + "".join(t(x + 8, y + 54 + i * 11, "✓ " + f, 7, MUTE) for i, f in enumerate(feats))
add(G1, "Up Keep: Plan Names",
 O("names_metal", "Gold And Platinum", "Classic tier names. Easy to rank, a bit like a credit card.", ["classic", "premium", "clear"], "concierge",
   screen(h1(14, 56, "Pick Your Plan", 19) + tiercard(14, 70, 102, 120, "Gold", "$2,780", "/yr", ["4 visits", "Filters", "Report"], True) + tiercard(124, 70, 102, 120, "Platinum", "$3,940", "/yr", ["6 visits", "Gutters", "Priority"]) + btn(208, "Continue With Gold"))),
 O("names_care", "Quarterly Care And Monthly Care", "Names that say what you get: how often we come.", ["plain-spoken", "honest", "clear"], "neighbor",
   screen(h1(14, 56, "Pick Your Plan", 19) + tiercard(14, 70, 102, 120, "Quarterly Care", "$2,780", "/yr", ["4 visits", "Filters", "Report"], True) + tiercard(124, 70, 102, 120, "Monthly Care", "$3,940", "/yr", ["12 visits", "Gutters", "Priority"]) + btn(208, "Continue With Quarterly"))),
 "Which Plan Names?")
add(G1, "Up Keep: Plan Layout",
 O("tiers_side", "Plans Side By Side", "Both plans in two columns so they compare at a glance.", ["organized", "clear", "transparent"], "system",
   screen(h1(14, 56, "Compare Plans", 19) + tiercard(14, 70, 102, 140, "Gold", "$232", "/mo", ["4 visits", "Filters", "Report", "Recalls"], True) + tiercard(124, 70, 102, 140, "Platinum", "$328", "/mo", ["6 visits", "Gutters", "Priority", "Recalls"]) + btn(226, "Continue"))),
 O("tiers_rec", "Recommended Plan First", "One big card for the plan that fits their house. Others sit behind a link.", ["guided", "calm", "focused"], "concierge",
   screen(lbl(14, 52, "Best fit for your home") + tiercard(14, 62, 212, 130, "Gold", "$232", "/mo", ["4 seasonal visits", "Filters, flushes, detectors", "Photo report after each visit"], True, "Recommended") + btn(206, "Continue With Gold") + link(120, 250, "See Other Plans", INK, "middle"))),
 "How Should Plans Be Laid Out?")
add(G1, "Up Keep: Price Display",
 O("price_month", "Monthly Price Big", "'$232 / month' leads. The yearly total sits small underneath.", ["friendly", "approachable", "clear"], "neighbor",
   screen(lbl(14, 56, "Gold plan") + t(14, 100, "$232", 44, INK, "khand") + t(98, 100, "/ month", 11, MUTE) + t(14, 116, "$2,780 billed yearly, or pay monthly", 8, MUTE) + f'<line x1="14" y1="130" x2="226" y2="130" stroke="{LINE}"/>' + para(14, 146, ["✓ 4 seasonal visits", "✓ Filters, flushes, detectors", "✓ Photo report every visit"], 8.5, INK, 13) + btn(200, "Start Gold"))),
 O("price_year", "Annual Price Big", "'$2,780 / year' leads. Monthly is the small line.", ["honest", "transparent", "direct"], "crew",
   screen(lbl(14, 56, "Gold plan") + t(14, 100, "$2,780", 44, INK, "khand") + t(124, 100, "/ year", 11, MUTE) + t(14, 116, "About $232 a month", 8, MUTE) + f'<line x1="14" y1="130" x2="226" y2="130" stroke="{LINE}"/>' + para(14, 146, ["✓ 4 seasonal visits", "✓ Filters, flushes, detectors", "✓ Photo report every visit"], 8.5, INK, 13) + btn(200, "Start Gold"))),
 "Which Price Should Be Big?")
ADDS = [("Gutter Cleaning", "+$18/mo"), ("Dryer Vent", "+$6/mo"), ("Sump Pump Test", "+$5/mo"), ("Window Wash", "+$22/mo")]
add(G1, "Up Keep: Add-Ons",
 O("addons_toggle", "Add-Ons As Toggle Rows", "A plain list with a switch on each row.", ["minimal", "efficient", "organized"], "system",
   screen(h1(14, 56, "Add Anything Else?", 18) + "".join(f'<line x1="14" y1="{70+i*34}" x2="226" y2="{70+i*34}" stroke="{LINE}"/>' + t(14, 88 + i * 34, n, 9.5, INK, "hind", 600) + t(14, 98 + i * 34, p, 7, MUTE) + toggle(202, 82 + i * 34, i == 0) for i, (n, p) in enumerate(ADDS)) + btn(226, "Continue"))),
 O("addons_cards", "Add-Ons As Picture Cards", "Two-by-two cards with a small picture. Tap a card to add it.", ["visual", "tactile", "friendly"], "neighbor",
   screen(h1(14, 56, "Add Anything Else?", 18) + "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 76, 104, 70, SEL if i == 0 else "#FFFFFF", INK if i == 0 else LINE, 4, 1.3) + photo(19 + (i % 2) * 108, 71 + (i // 2) * 76, 94, 34, ["house", "interior", "tech", "house"][i], 3, ["day", "warm", "mute", "day"][i]) + t(20 + (i % 2) * 108, 118 + (i // 2) * 76, n, 7.5, INK, "hind", 600) + t(20 + (i % 2) * 108, 129 + (i // 2) * 76, p, 6.5, MUTE) for i, (n, p) in enumerate(ADDS)) + btn(226, "Continue"))),
 "How Should Add-Ons Look?")
add(G1, "Up Keep: Price Details",
 O("detail_modal", "Details In A Pop-Up", "'See What's Included' opens a sheet over the page.", ["focused", "clean", "modern"], "system",
   screen(tiercard(14, 46, 212, 90, "Gold", "$232", "/mo", ["4 seasonal visits"], True) + rect(0, 32, W, H, INK, extra='opacity=".25"') + rect(0, 128, W, 180, "#FFFFFF", r=12) + rect(108, 134, 24, 3, "#D4D4D4", r=1.5) + h1(14, 158, "What's In Gold", 15) + t(222, 156, "✕", 10, INK, anchor="end")
          + "".join(t(14, 176 + i * 12, l, 7.5, MUTE) + t(226, 176 + i * 12, v, 7.5, INK, anchor="end") for i, (l, v) in enumerate([("Furnace tune-up ×2", "$420"), ("Water heater flush", "$210"), ("Filters ×4", "$160"), ("Detectors, GFCIs", "$140"), ("Your price", "$2,780")])) + btn(250, "Got It"))),
 O("detail_inline", "Details Expand In Place", "The card grows to show the breakdown. No pop-up.", ["transparent", "calm", "practical"], "crew",
   screen(rect(14, 42, 212, 200, SEL, INK, 4, 1.5) + h1(22, 64, "Gold", 14) + t(22, 82, "$232", 15, INK, "khand") + t(48, 82, "/mo", 7, MUTE) + t(218, 64, "HIDE ▴", 6.5, TERRA, "hind", 600, "end") + f'<line x1="22" y1="94" x2="218" y2="94" stroke="{LINE}"/>'
          + "".join(t(22, 110 + i * 13, l, 7.5, MUTE) + t(218, 110 + i * 13, v, 7.5, INK, anchor="end") for i, (l, v) in enumerate([("Furnace tune-up ×2", "$420"), ("Water heater flush", "$210"), ("Filters ×4", "$160"), ("Detectors, GFCIs", "$140"), ("AC check", "$180"), ("Your price", "$2,780")])) + btn(254, "Continue With Gold"))),
 "Where Should Price Details Open?")
add(G1, "Up Keep: Equipment Photos",
 O("cam_guided", "Guided Camera", "The camera opens with a frame and one instruction at a time.", ["guided", "modern", "focused"], "system",
   screen(photo(0, 32, W, 210, "label", 0) + "".join(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="3"/>' for d in ["M40 70 v-14 h14", "M200 70 v-14 h-14", "M40 200 v14 h14", "M200 200 v14 h-14"]) + rect(30, 222, 180, 16, "#0A0A0A", r=8, extra='opacity=".7"') + t(120, 233, "Point at the water heater label", 7.5, "#FFFFFF", anchor="middle")
          + t(14, 262, "Step 2 of 4", 7, MUTE) + f'<circle cx="120" cy="270" r="16" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="120" cy="270" r="11" fill="{INK}"/>', bg="#FFFFFF")),
 O("cam_grid", "Upload Grid", "Six labelled tiles. Tap any tile to snap or pick a photo.", ["flexible", "organized", "practical"], "crew",
   screen(h1(14, 56, "Add Photos Of Your Equipment", 15) + "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 58, 104, 52, "#FFFFFF" if i > 1 else "#FFFFFF", LINE, 4, 1, 'stroke-dasharray="3 2"' if i > 1 else "") + (photo(15 + (i % 2) * 108, 67 + (i // 2) * 58, 102, 36, "label" if i == 0 else "tech", 3) if i < 2 else t(66 + (i % 2) * 108, 96 + (i // 2) * 58, "+", 16, MUTE, anchor="middle")) + t(20 + (i % 2) * 108, 113 + (i // 2) * 58, n, 7, INK, "hind", 600) for i, n in enumerate(["Water Heater Label", "Furnace", "AC Unit", "Electric Panel", "Sump Pump", "Other"])) + btn(250, "Upload 2 Photos"))),
 "How Should Photo Upload Work?")
add(G1, "Up Keep: Signature",
 O("sig_drawn", "Draw Your Signature", "Sign with a finger in a box, like at a store counter.", ["personal", "tactile", "formal"], "concierge",
   screen(h1(14, 56, "Sign Your Agreement", 18) + para(14, 72, ["Gold plan · $232 a month · cancel anytime"]) + lbl(14, 100, "Sign below") + rect(14, 106, 212, 80, "#FFFFFF", "#CFC8BC") + f'<path d="M30 160 c10 -30 18 -30 16 0 c-2 18 14 -26 22 -12 c6 10 10 4 16 -6 c4 12 10 14 20 2 c8 -10 14 6 26 -2 c10 -6 30 -4 60 -8" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>' + f'<line x1="24" y1="172" x2="216" y2="172" stroke="{LINE}"/>' + link(222, 198, "Clear", MUTE, "end") + btn(220, "Sign And Continue"))),
 O("sig_typed", "Type Your Name", "Type your full name. It shows in a script face as your signature.", ["fast", "practical", "clear"], "system",
   screen(h1(14, 56, "Sign Your Agreement", 18) + para(14, 72, ["Gold plan · $232 a month · cancel anytime"]) + field(100, "Full name", "Sarah Whitman") + lbl(14, 146, "Your signature") + rect(14, 152, 212, 40, CREAM, LINE) + t(24, 180, "Sarah Whitman", 20, INK, "Caveat") + t(14, 206, "☑ I agree that typing my name is my signature.", 7, MUTE) + btn(220, "Sign And Continue"))),
 "How Should They Sign?")
add(G1, "Up Keep: Most Popular Badge",
 O("pop_gold", "Most Popular On Gold", "The badge sits on the cheaper plan most people pick.", ["safe", "approachable", "guided"], "neighbor",
   screen(h1(14, 56, "Pick Your Plan", 19) + tiercard(14, 76, 102, 120, "Gold", "$232", "/mo", ["4 visits", "Filters", "Report"], True, "Most Popular") + tiercard(124, 76, 102, 120, "Platinum", "$328", "/mo", ["6 visits", "Gutters", "Priority"]) + btn(214, "Continue"))),
 O("pop_plat", "Most Popular On Platinum", "The badge nudges toward the bigger plan.", ["premium", "bold", "upsell"], "concierge",
   screen(h1(14, 56, "Pick Your Plan", 19) + tiercard(14, 76, 102, 120, "Gold", "$232", "/mo", ["4 visits", "Filters", "Report"]) + tiercard(124, 76, 102, 120, "Platinum", "$328", "/mo", ["6 visits", "Gutters", "Priority"], True, "Most Popular") + btn(214, "Continue"))),
 "Where Does Most Popular Go?")
EST = h1(14, 56, "Your Estimate", 19) + t(14, 92, "$232", 32, INK, "khand") + t(76, 92, "/ month · Gold", 9, MUTE) + "".join(f'<line x1="14" y1="{106+i*20}" x2="226" y2="{106+i*20}" stroke="{LINE}"/>' + t(14, 120 + i * 20, l, 8, INK) + t(226, 120 + i * 20, v, 8, MUTE, anchor="end") for i, (l, v) in enumerate([("Furnace ×1", "Included"), ("Water heater, tank", "Included"), ("AC ×1", "Included"), ("Smoke detectors ×6", "Included")]))
add(G1, "Up Keep: Main Button",
 O("cta_sticky", "Sticky Bottom Button", "The main button stays pinned at the bottom while they scroll.", ["persistent", "modern", "efficient"], "system",
   screen(EST + sticky(btn(266, "Start Gold"), 256))),
 O("cta_inline", "Buttons In The Flow", "Buttons sit right after the content, like the live app.", ["calm", "classic", "clear"], "concierge",
   screen(EST + btn(196, "Start Gold") + btn(228, "Add Photos For A Final Price", "outline"))),
 "Sticky Button Or In The Flow?")
add(G1, "Up Keep: Icons",
 O("icons_outline", "Outline Icons", "Thin black line icons, like the rest of the type.", ["minimal", "clean", "classic"], "concierge",
   screen(h1(14, 56, "Your Home Record", 18) + "".join(f'<line x1="14" y1="{68+i*40}" x2="226" y2="{68+i*40}" stroke="{LINE}"/>' + icon(k, 16, 76 + i * 40, 22, "outline") + t(48, 86 + i * 40, n, 9.5, INK, "hind", 600) + t(48, 97 + i * 40, d, 7, MUTE) for i, (k, n, d) in enumerate([("furnace", "Furnace", "Carrier 59SC5 · checked Sep 14"), ("water", "Water Heater", "Rheem XG50T · flushed Sep 14"), ("ac", "AC Unit", "Trane XR14 · due Apr"), ("smoke", "Smoke Detectors", "6 of 6 tested")])))),
 O("icons_duo", "Filled Duotone Icons", "Icons with a soft fill and a terracotta line.", ["friendly", "warm", "visual"], "neighbor",
   screen(h1(14, 56, "Your Home Record", 18) + "".join(f'<line x1="14" y1="{68+i*40}" x2="226" y2="{68+i*40}" stroke="{LINE}"/>' + icon(k, 16, 76 + i * 40, 22, "duo") + t(48, 86 + i * 40, n, 9.5, INK, "hind", 600) + t(48, 97 + i * 40, d, 7, MUTE) for i, (k, n, d) in enumerate([("furnace", "Furnace", "Carrier 59SC5 · checked Sep 14"), ("water", "Water Heater", "Rheem XG50T · flushed Sep 14"), ("ac", "AC Unit", "Trane XR14 · due Apr"), ("smoke", "Smoke Detectors", "6 of 6 tested")])))),
 "Which Icon Style?")
QBODY = lbl(14, 98, "Question 3 of 5") + h1(14, 120, "How Many Water Heaters?", 19) + "".join(rect(14, 132 + i * 30, 212, 24, SEL if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 0, 1.3) + t(24, 148 + i * 30, s, 9, INK) for i, s in enumerate(["None", "1 tank", "1 tankless", "2 or more"])) + btn(260, "Next")
add(G1, "Up Keep: Progress",
 O("prog_bar", "Progress Bar", "A thin bar fills as they go.", ["minimal", "clear", "modern"], "system", screen(link(14, 50, "← Back", INK) + pbar(64, .6) + QBODY)),
 O("prog_dots", "Step Dots", "Five dots; filled dots are done.", ["friendly", "clear", "countable"], "neighbor", screen(link(14, 50, "← Back", INK) + dots(70, 5, 2) + QBODY)),
 "Progress Bar Or Step Dots?")
add(G1, "Up Keep: Estimate Notice",
 O("notice_banner", "Notice As A Banner", "A cream banner on top: 'This is an estimate. Final price after your first visit.'", ["transparent", "honest", "upfront"], "crew",
   screen(rect(0, 32, W, 30, CREAM) + rect(0, 32, 3, 30, TERRA) + t(12, 45, "This is an estimate.", 8, INK, "hind", 600) + t(12, 56, "Final price is set at your first visit.", 7.5, MUTE) + f'<g transform="translate(0,14)">{EST}</g>' + btn(220, "Start Gold"))),
 O("notice_foot", "Notice As A Footnote", "A small line under the price with an asterisk.", ["calm", "clean", "minimal"], "concierge",
   screen(EST.replace(">$232<", ">$232*<") + t(14, 206, "*Estimate. Final price is set at your first visit.", 6.8, MUTE) + btn(220, "Start Gold"))),
 "How Should The Estimate Notice Show?")
CALLR = rect(156, 8, 72, 16, "#FFFFFF", INK, 0, 1.2) + icon("phone", 160, 10, 12, "outline") + t(196, 19, "CALL / TEXT", 6, INK, "hind", 600, "middle")
add(G1, "Up Keep: Call / Text Button",
 O("call_header", "Call / Text In The Header", "Always at the top right, on every screen.", ["accessible", "direct", "personal"], "crew",
   screen(EST + btn(206, "Start Gold"), right=CALLR)),
 O("call_float", "Floating Call / Text Button", "A round button in the bottom corner that opens Call or Text.", ["modern", "accessible", "friendly"], "neighbor",
   screen(EST + btn(206, "Start Gold") + f'<circle cx="204" cy="266" r="17" fill="{INK}"/>' + icon("chat", 194, 256, 20, "outline").replace(f'stroke="{INK}"', 'stroke="#FFFFFF"'))),
 "Where Should Call / Text Live?")
add(G1, "Up Keep: Call / Text Button",
 O("call_footer", "Call / Text Beside The Main Button", "In the sticky footer, a small Call button next to Start.", ["efficient", "practical", "direct"], "crew",
   screen(EST + sticky(btn(266, "Start Gold", x=14, w=160) + rect(180, 266, 46, 26, "#FFFFFF", INK, 0, 1.5) + icon("phone", 196, 272, 14, "outline"), 256))),
 O("call_card", "Call / Text Card Under The Estimate", "A short card: 'Questions? Call or text Max.' with two buttons.", ["personal", "warm", "trustworthy"], "neighbor",
   screen(EST + rect(14, 196, 212, 58, CREAM, LINE, 4) + t(24, 214, "Questions? Call Or Text Max.", 10, INK, "khand") + btn(222, "Call", "outline", x=24, w=92, h=22, size=8) + btn(222, "Text", "outline", x=124, w=92, h=22, size=8) + btn(264, "Start Gold"))),
 "Which Call / Text Spot?")

# ===================== 2. Micro-dose color (9) =====================
def dash(accs, base="#FFFFFF", spread=1, beige=False):
    a = accs[0]; b = accs[1] if len(accs) > 1 else a; c = accs[2] if len(accs) > 2 else b
    ink = "#4A4036" if beige else INK; card = "#EFE6D8" if beige else ("#FFFFFF" if base != "#FFFFFF" else CREAM)
    s = lbl(14, 50, "Hi Sarah") + h1(14, 70, "Your Home Is In Good Shape", 15, ink)
    s += rect(14, 80, 212, 74, card, LINE, 6) + ring(52, 117, 22, .86, (b if spread >= 2 else "#BDB6AA") if not beige else "#A8957C", "92") + t(84, 104, "Next visit", 7, MUTE) + t(84, 120, "Tue, Nov 4 · 9 AM", 12, ink, "khand") + t(84, 133, "Danny, your tech", 7.5, MUTE) + (tag(84, 138, "Confirmed", c, False) if spread >= 3 else "")
    for i, (n, st) in enumerate([("Furnace filter", "Done"), ("Water heater flush", "Done"), ("Gutters", "Due Nov")]):
        y = 168 + i * 24; s += f'<line x1="14" y1="{y}" x2="226" y2="{y}" stroke="{LINE}"/>' + t(14, y + 15, n, 8.5, ink) + (tag(176, y + 6, st, c if (spread >= 3 and st == "Done") else ("#737373"), False) if not beige else tag(176, y + 6, st, "#8C7A64"))
    s += btn(250, "Book A Visit", col=("#8C7A64" if beige else a))
    return screen(s, base, hc=ink, up=("#8C7A64" if beige else a))
CO = "Up Keep: Micro-Dose Color"
add(G2, CO, O("cd_terra", "Terracotta Pop", "White base, one terracotta button (#C1502E). Everything else black and grey.", ["warm", "earthy-pop", "one-accent"], "neighbor", dash([TERRA])),
            O("cd_lagoon", "Lagoon Pop", "Same screen, one lagoon blue button (#05668D).", ["cool", "trustworthy", "one-accent"], "system", dash([LAGOON])), "Which Single Accent?")
add(G2, CO, O("cd_jungle", "Jungle Pop", "One jungle green button (#0B6E4F): reads as 'all good'.", ["natural", "calm", "one-accent"], "crew", dash([JUNGLE])),
            O("cd_saffron", "Saffron Pop", "One saffron button (#D4A017): sunny, attention-getting.", ["sunny", "warm", "one-accent"], "neighbor", dash([SAFFRON])), "Which Single Accent?")
add(G2, CO, O("cd_berry", "Berry Pop", "One deep berry button (#9B2D5B).", ["rich", "distinctive", "one-accent"], "concierge", dash([BERRY])),
            O("cd_persim", "Persimmon Pop", "One persimmon button (#E4572E): brighter than terracotta.", ["energetic", "warm", "one-accent"], "neighbor", dash([PERSIM])), "Which Single Accent?")
add(G2, CO, O("cd_lag_deep", "Deep Lagoon", "Darker lagoon #05668D.", ["cool", "serious", "one-accent"], "system", dash([LAGOON])),
            O("cd_lag_bright", "Bright Lagoon", "Brighter lagoon teal #00A6A6.", ["fresh", "friendly", "one-accent"], "neighbor", dash([LAG2])), "Which Lagoon?")
add(G2, CO, O("cd_one", "One Accent Only", "Color only on the main button. Ring and tags stay grey.", ["minimal", "restrained", "one-accent"], "concierge", dash([TERRA], spread=1)),
            O("cd_spread", "Accent Spread In 3 Spots", "Same terracotta on the button, the progress ring and the Done tags.", ["lively", "coded", "multi-accent"], "neighbor", dash([TERRA], spread=3)), "One Spot Or Spread Around?")
add(G2, CO, O("cd_duo", "Two Colors: Terracotta + Lagoon", "Terracotta button; lagoon ring and tags.", ["balanced", "lively", "multi-accent"], "system", dash([TERRA, LAGOON, LAGOON], spread=3)),
            O("cd_trio", "Three Colors: Terracotta, Jungle, Saffron", "Terracotta button, saffron ring, jungle Done tags.", ["playful", "coded", "multi-accent"], "neighbor", dash([TERRA, SAFFRON, JUNGLE], spread=3)), "Two Colors Or Three?")
add(G2, CO, O("cd_white_pop", "White Base, Small Pops (Check)", "Max's new rule: white base, clear small accents.", ["clean", "crisp", "multi-accent"], "system", dash([LAGOON, LAGOON, JUNGLE], spread=3)),
            O("cd_beige", "All Beige, No Pops (Check)", "Warm beige everything, muted brown button.", ["earthy", "muted", "all-beige"], "neighbor", dash([TERRA], base="#F3ECE1", beige=True)), "Pops Or All Beige?", "check")
add(G2, CO, O("cd_base_white", "Pure White Base", "Pops of jungle green on #FFFFFF.", ["crisp", "clean", "white-base"], "system", dash([JUNGLE], spread=3)),
            O("cd_base_cream", "Warm Cream Base", "The same pops on cream #FAF6EE.", ["warm", "soft", "cream-base"], "neighbor", dash([JUNGLE], base=CREAM, spread=3)), "White Or Cream Base?")
def visit_card(where, col):
    s = h1(14, 56, "Visit Report · Oct 8", 16) + ring(196, 52, 14, .9, col if where == "ring" else "#BDB6AA", "")
    for i, (n, st) in enumerate([("Furnace filter swapped", "Done"), ("Water heater flushed", "Done"), ("Smoke detectors", "6 of 6"), ("Dryer vent", "Needs Clean")]):
        y = 74 + i * 30; s += f'<line x1="14" y1="{y}" x2="226" y2="{y}" stroke="{LINE}"/>' + t(14, y + 18, n, 8.5, INK) + tag(166, y + 10, st, (col if where == "tags" else "#737373") if st != "Needs Clean" else (col if where == "tags" else "#737373"), where == "tags" and st == "Needs Clean")
    return screen(s + photo(14, 200, 100, 46, "tech") + photo(126, 200, 100, 46, "label") + link(14, 266, "Download PDF", col if where != "tags" else INK))
add(G2, CO, O("cd_on_ring", "Color On The Score Ring And Link", "The accent marks the score and the link; tags stay grey.", ["calm", "restrained", "one-accent"], "concierge", visit_card("ring", LAGOON)),
            O("cd_on_tags", "Color On The Status Tags", "The accent marks Done tags, and solid for anything that needs action.", ["clear", "coded", "one-accent"], "system", visit_card("tags", LAGOON)), "Where Should The Pop Go?")

# ===================== 3. Retests (2) =====================
HOME = h1(14, 56, "Your Home Record", 18) + "".join(f'<line x1="14" y1="{68+i*30}" x2="226" y2="{68+i*30}" stroke="{LINE}"/>' + t(14, 87 + i * 30, n, 9, INK) + t(226, 87 + i * 30, "›", 11, MUTE, anchor="end") for i, n in enumerate(["Maintenance Schedule", "Shutoffs & Key Locations", "Visit Reports"]))
add(G3, "Up Keep: Install Prompt",
 O("install_card", "Install Card After Booking", "Right after the first visit is booked: a card offering 'Add Up Keep to your home screen'.", ["helpful", "proactive", "app-like"], "system",
   screen(HOME + rect(14, 170, 212, 76, "#FFFFFF", INK, 6, 1.3) + rect(24, 182, 30, 30, "#FFFFFF", LINE, 7) + roof_logo(26, 200, .38) + t(62, 192, "Add Up Keep To Your Home Screen", 9.5, INK, "khand") + para(62, 204, ["Open your schedule and shutoffs in one", "tap, even with no signal."], 7, MUTE, 9) + btn(222, "Add To Home Screen", x=24, w=130, h=18, size=7) + link(162, 234, "Not Now", MUTE))),
 O("install_menu", "Quiet Install Link In The Menu", "No prompt. 'Install App' sits as a row in the menu for anyone who wants it.", ["quiet", "respectful", "minimal"], "concierge",
   screen(HOME + f'<line x1="14" y1="158" x2="226" y2="158" stroke="{LINE}"/>' + t(14, 177, "Install App", 9, MUTE) + t(226, 177, "⤓", 10, MUTE, anchor="end"))),
 "Install Prompt (Retest)", retest=True)
SHUT = [("Water Main", "Basement, north wall, red handle"), ("Gas Shutoff", "Outside, left of meter"), ("Electric Panel", "Garage, behind the door")]
add(G3, "Up Keep: Offline Shutoffs",
 O("offline_saved", "Shutoffs Saved For Offline", "A 'Works without signal' badge. The page is stored on the phone.", ["reliable", "safety", "practical"], "crew",
   screen(h1(14, 56, "Shutoffs", 18) + tag(160, 47, "Works Offline", JUNGLE) + "".join(rect(14, 68 + i * 54, 212, 48, "#FFFFFF", LINE, 4) + photo(18, 72 + i * 54, 40, 40, "label", 3) + t(66, 86 + i * 54, n, 10, INK, "khand") + t(66, 98 + i * 54, d, 7, MUTE) for i, (n, d) in enumerate(SHUT)) + t(14, 248, "✓ Saved on this phone · updated Oct 8", 7, JUNGLE))),
 O("offline_online", "Shutoffs Load Online Only", "Same page, always fresh, but it needs a connection.", ["simple", "current", "minimal"], "system",
   screen(h1(14, 56, "Shutoffs", 18) + "".join(rect(14, 68 + i * 54, 212, 48, "#FFFFFF", LINE, 4) + photo(18, 72 + i * 54, 40, 40, "label", 3) + t(66, 86 + i * 54, n, 10, INK, "khand") + t(66, 98 + i * 54, d, 7, MUTE) for i, (n, d) in enumerate(SHUT)) + t(14, 248, "Needs an internet connection", 7, MUTE))),
 "Offline Shutoffs (Retest)", retest=True)

# ===================== 4. Voice & headlines (7) =====================
def hero(head, sub, cta="Get My Estimate", lines2=None):
    hl = head if isinstance(head, list) else [head]
    s = photo(14, 42, 212, 96, "house") + "".join(h1(14, 164 + i * 22, l, 21) for i, l in enumerate(hl))
    y = 164 + len(hl) * 22; s += para(14, y, sub, 8.5, MUTE, 12) + btn(y + len(sub) * 12 + 10, cta)
    return screen(s)
VO = "Up Keep: Headline & Voice"
add(G4, VO, O("hl_handled", "Your House, Handled.", "Short and calm. Promise first.", ["calm", "confident", "short"], "concierge", hero("Your House, Handled.", ["Seasonal visits, a set price and a photo", "report after every one."])),
            O("hl_never", "Never Miss Home Maintenance Again.", "Names the problem the homeowner has.", ["direct", "problem-first", "clear"], "crew", hero(["Never Miss Home", "Maintenance Again."], ["We keep the schedule. You keep living."])), "Which Headline?")
add(G4, VO, O("hl_small", "Small Visits. No Big Surprises.", "Light, reassuring rhythm.", ["friendly", "reassuring", "short"], "neighbor", hero(["Small Visits.", "No Big Surprises."], ["A quick check each season so the big", "things never catch you off guard."])),
            O("hl_8000", "Catch The $8,000 Problem While It's An $80 Fix.", "Money-first, concrete.", ["concrete", "money", "urgent"], "crew", hero(["Catch The $8,000 Problem", "While It's An $80 Fix."], ["Leaks, rust and worn parts, found early."])), "Which Headline?")
add(G4, VO, O("tone_max", "Neighbor Tone: 'Hi, I'm Max.'", "First person, from Max.", ["personal", "warm", "neighborly"], "neighbor", hero("Hi, I'm Max.", ["My crew looks after your house like it's", "our own, every season, same faces."], "Meet The Crew")),
            O("tone_pro", "Pro Tone: Facts In A Row", "Short, factual lines. No 'I'.", ["professional", "factual", "direct"], "crew", hero("Licensed. Scheduled. Reported.", ["Licensed techs. Set visits. A photo", "report after every one."], "See Plans")), "Which Voice?")
add(G4, VO, O("cta_price", "Button: 'See My Price'", "Three words, low effort.", ["short", "direct", "low-pressure"], "crew", hero("Your House, Checked Every Season", ["Answer five quick questions."], "See My Price")),
            O("cta_2min", "Button: 'Get My Estimate In 2 Minutes'", "Sets the time it takes.", ["specific", "reassuring", "clear"], "system", hero("Your House, Checked Every Season", ["Answer five quick questions."], "Get My Estimate In 2 Minutes")), "Which Button Text?")
add(G4, VO, O("sub_flat", "Subline: 'One Flat Yearly Price. Cancel Anytime.'", "Leads with terms and safety.", ["transparent", "safe", "honest"], "concierge", hero("Your House, Handled.", ["One flat yearly price. Cancel anytime."])),
            O("sub_from", "Subline: 'Plans From $232 A Month.'", "Leads with a number.", ["concrete", "money", "direct"], "crew", hero("Your House, Handled.", ["Plans from $232 a month."])), "Which Subline?")
add(G4, VO, O("hl_boring", "Up Keep Takes Care Of The Boring, Important Stuff.", "Wry and plain.", ["wry", "friendly", "plain-spoken"], "neighbor", hero(["We Handle The Boring,", "Important Stuff."], ["Filters, flushes, detectors and gutters."])),
            O("hl_protect", "Protect The Biggest Thing You Own.", "Serious, value-focused.", ["serious", "protective", "premium"], "concierge", hero(["Protect The Biggest", "Thing You Own."], ["Care that keeps your home's value up."])), "Which Headline?")
add(G4, VO, O("proof_tech", "Proof Line: 'Same Tech Every Visit.'", "Trust through a familiar face.", ["personal", "trust", "consistent"], "neighbor", hero("Your House, Handled.", ["Same tech every visit. Danny knows", "your house."], "Meet Danny")),
            O("proof_photo", "Proof Line: 'Photos Of Everything We Check.'", "Trust through evidence.", ["transparent", "evidence", "organized"], "system", hero("Your House, Handled.", ["Photos of everything we check, in", "your Home Record."], "See A Sample Report")), "Which Proof Line?")

# ===================== 5. Logo (4) using the house-spells-UP files =====================
def logo_inner(name, recolor=None):
    s = open(f"{LOGOS}/{name}.svg").read()
    if recolor: s = s.replace(TEAL, recolor)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1); body = s[s.index(">") + 1:-6]
    body = re.sub(r'^<rect width="[\d.]+" height="[\d.]+" fill="#FFFFFF"/>', "", body)
    return body, [float(v) for v in vb.split()]
def nest(name, x, y, w, recolor=None):
    body, (_, _, vw, vh) = logo_inner(name, recolor); h = w * vh / vw
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="0 0 {vw} {vh}">{body}</svg>', h
def logo_hdr_screen(name, recolor=None):
    lg, h = nest(name, 8, 8, 120, recolor)
    return screen(lg + f'<line x1="0" y1="{h+14:.0f}" x2="{W}" y2="{h+14:.0f}" stroke="{LINE}"/>' + h1(14, 90, "Your House, Handled.", 20) + para(14, 106, ["Seasonal visits and a photo report."]) + btn(124, "Get My Estimate"), head=False)
def splash(name, recolor=None, bg="#FFFFFF"):
    lg, h = nest(name, 30, 110, 180, recolor)
    return screen(lg + t(120, 250, "Loading your Home Record…", 7.5, MUTE, anchor="middle"), bg=bg, head=False)
def homescreen(icon_name, scale):
    body, (_, _, vw, vh) = logo_inner(icon_name)
    apps = "".join(rect(24 + (i % 4) * 50, 60 + (i // 4) * 62, 42, 42, c, r=10) for i, c in enumerate(["#D8D8D8", "#CFE3F7", "#F8D9C4", "#DDEDD5", "#E9E4F5", "#F5E9C8", "#E0E0E0"]))
    x, y = 24 + 3 * 50, 60 + 62
    ic = rect(x, y, 42, 42, "#FFFFFF", LINE, 10) + f'<svg x="{x+21-21*scale:.1f}" y="{y+21-21*scale:.1f}" width="{42*scale:.1f}" height="{42*scale:.1f}" viewBox="0 0 {vw} {vh}">{body.replace("rx=\"22\"", "rx=\"0\"")}</svg>'
    return screen(f'<rect width="{W}" height="{H}" fill="#EEF3F6"/>' + t(120, 30, "9:41", 9, INK, "hind", 600, "middle") + apps + ic + t(x + 21, y + 52, "Up Keep", 6.5, INK, anchor="middle") + rect(14, 230, 212, 48, "#FFFFFFAA", r=16), head=False)
LO = "Up Keep: Logo"
add(G5, LO, O("lg_hdr_outline", "Outline House In The App Header", "SMART [UP] KEEP with the outline house, at real header size.", ["light", "clean", "outline"], "system", logo_hdr_screen("up_outline")),
            O("lg_hdr_solid", "Solid House In The App Header", "The solid teal house with U and P cut out, at header size.", ["bold", "solid", "friendly"], "neighbor", logo_hdr_screen("up_solid")), "Outline Or Solid In The App?")
add(G5, LO, O("lg_splash_roof", "Color On The Roof Only (Splash)", "Loading screen: only the roof in color.", ["restrained", "clean", "minimal"], "concierge", splash("up_acc_house")),
            O("lg_splash_whole", "Whole Mark In Color (Splash)", "Loading screen: roof, U and P in color.", ["bold", "friendly", "visible"], "neighbor", splash("up_acc_whole")), "Where Does The Logo Color Go?")
add(G5, LO, O("lg_icon_big", "App Icon: Mark Fills The Tile", "The house-UP is big inside the icon tile.", ["bold", "legible", "solid"], "crew", homescreen("up_icon_app_outline", 1.25)),
            O("lg_icon_small", "App Icon: Mark With Breathing Room", "The house-UP sits smaller with white space around it.", ["calm", "airy", "premium-quiet"], "concierge", homescreen("up_icon_app_outline", .85)), "How Big In The App Icon?")
add(G5, LO, O("lg_teal", "Logo Roof In Its Own Teal", "Keeps the logo's muted teal while the app's buttons stay black and terracotta.", ["calm", "cool", "consistent"], "system", logo_hdr_screen("up_teal")),
            O("lg_terra", "Logo Roof In App Terracotta", "Recolors the roof to match the app's terracotta links.", ["warm", "matched", "cohesive"], "neighbor", logo_hdr_screen("up_teal", TERRA)), "Teal Logo Or Matched To The App?")

# ===================== 6. Photos, screens & email (10) =====================
PH = "Up Keep: Hero Photo"
add(G6, PH, O("ph_house", "Hero Photo: The House", "A bright, daylight photo of a well-kept house.", ["bright", "aspirational", "calm"], "concierge", screen(photo(0, 32, W, 150, "house", 0) + h1(14, 210, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))),
            O("ph_tech", "Hero Photo: A Tech At Work", "A close shot of a tech checking the water heater.", ["real", "hands-on", "trustworthy"], "crew", screen(photo(0, 32, W, 150, "tech", 0) + h1(14, 210, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))), "Which Hero Photo?")
add(G6, PH, O("ph_warm", "Warm, Lived-In Interior", "A sunny living room: what the homeowner gets to enjoy.", ["warm", "lifestyle", "soft"], "neighbor", screen(photo(0, 32, W, 150, "interior", 0, "warm") + h1(14, 210, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))),
            O("ph_cool", "Clean, Muted Exterior", "A cooler, muted exterior shot, editorial feel.", ["muted", "editorial", "quiet"], "concierge", screen(photo(0, 32, W, 150, "house", 0, "mute") + h1(14, 210, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))), "Which Photo Mood?")
LINEHOUSE = f'<g fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"><path d="M50 120 L120 62 L190 120"/><path d="M62 110 V170 H178 V110"/><rect x="108" y="132" width="24" height="38"/><rect x="76" y="124" width="22" height="18"/><rect x="142" y="124" width="22" height="18"/><path d="M155 80 V64 H167 V90"/></g><circle cx="120" cy="152" r="3" fill="{TERRA}"/>'
FLATHOUSE = f'<rect x="20" y="170" width="200" height="10" fill="#E8E0D2"/><path d="M50 120 L120 62 L190 120 Z" fill="{TERRA}"/><rect x="62" y="118" width="116" height="52" fill="#F3E8DC"/><rect x="108" y="132" width="24" height="38" fill="{INK}"/><rect x="76" y="126" width="22" height="16" fill="#CFE3EE"/><rect x="142" y="126" width="22" height="16" fill="#CFE3EE"/>'
add(G6, "Up Keep: Illustration Or Photo",
 O("il_line", "Line Illustration", "A simple black line drawing of a house, one terracotta dot.", ["minimal", "drawn", "clean"], "system", screen(f'<g transform="translate(0,-20)">{LINEHOUSE}</g>' + h1(14, 196, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))),
 O("il_photo", "Real Photo", "A real photo of a home in the same spot.", ["real", "warm", "credible"], "neighbor", screen(photo(14, 42, 212, 130, "house") + h1(14, 196, "Your House, Handled.", 20) + btn(228, "Get My Estimate"))), "Illustration Or Photo?")
add(G6, "Up Keep: Illustration Style",
 O("il_line2", "Line Drawing Style", "Thin black lines, mostly white.", ["minimal", "light", "outline"], "concierge", screen(f'<g transform="translate(0,-20)">{LINEHOUSE}</g>' + h1(14, 196, "Every Season, Covered", 18) + para(14, 212, ["Spring, summer, fall and winter visits."]))),
 O("il_flat", "Flat Color Style", "Simple shapes with a terracotta roof and cream walls.", ["friendly", "warm", "flat"], "neighbor", screen(f'<g transform="translate(0,-20)">{FLATHOUSE}</g>' + h1(14, 196, "Every Season, Covered", 18) + para(14, 212, ["Spring, summer, fall and winter visits."]))), "Which Illustration Style?")
CF = "Up Keep: Confirmation"
add(G6, CF, O("cf_check", "Big Check And Summary", "A large check, 'You're In', and a plain summary list.", ["clear", "calm", "simple"], "system",
   screen(icon("check", 96, 50, 48, "duo", JUNGLE) + h1(120, 124, "You're In, Sarah.", 21, anchor="middle") + "".join(f'<line x1="14" y1="{140+i*22}" x2="226" y2="{140+i*22}" stroke="{LINE}"/>' + t(14, 155 + i * 22, l, 8, MUTE) + t(226, 155 + i * 22, v, 8, INK, anchor="end") for i, (l, v) in enumerate([("Plan", "Gold"), ("First visit", "Tue, Nov 4 · 9 AM"), ("Price", "$232 / month")])) + btn(222, "Go To My Home Record"))),
            O("cf_tech", "Meet Your Tech", "'Danny will see you Tuesday' with his photo and Add to Calendar.", ["personal", "warm", "human"], "neighbor",
   screen(h1(14, 58, "You're In, Sarah.", 21) + rect(14, 72, 212, 92, CREAM, LINE, 6) + f'<circle cx="46" cy="104" r="20" fill="#C79B7B"/>' + t(76, 98, "Danny will see you", 8, MUTE) + t(76, 114, "Tue, Nov 4 · 9 AM", 13, INK, "khand") + t(76, 126, "Licensed tech, 11 years", 7, MUTE) + btn(136, "Add To Calendar", "outline", x=24, w=192, h=20, size=7.5) + btn(180, "Go To My Home Record"))), "Which Confirmation?")
def email(kind):
    if kind == "letter":
        s = rect(0, 0, W, 34, "#F5F5F5") + t(14, 14, "From: Max Weberman", 7, MUTE) + t(14, 26, "Welcome to Up Keep, Sarah", 8, INK, "hind", 600)
        s += para(14, 56, ["Hi Sarah,", "", "Thanks for joining. Danny will be at your", "house Tuesday, Nov 4 at 9 AM. He'll check", "the furnace, flush the water heater and test", "every smoke detector.", "", "Questions? Just reply. It comes to me.", "", "Max"], 8.5, INK, 13) + t(14, 200, "Max Weberman", 18, INK, "Caveat")
        return screen(s, head=False)
    s = rect(0, 0, W, 34, "#F5F5F5") + t(14, 14, "From: Up Keep", 7, MUTE) + t(14, 26, "Welcome to Up Keep, Sarah", 8, INK, "hind", 600) + roof_logo(84, 60, 1)
    s += f'<line x1="14" y1="72" x2="226" y2="72" stroke="{LINE}"/>' + h1(120, 98, "Welcome Home, Sarah", 19, anchor="middle") + rect(14, 110, 212, 60, CREAM, LINE, 6) + t(24, 128, "FIRST VISIT", 6.5, MUTE, "hind", 600) + t(24, 146, "Tue, Nov 4 · 9 AM", 14, INK, "khand") + t(24, 160, "Danny, your tech", 7.5, MUTE)
    s += "".join(t(14, 190 + i * 13, "✓ " + l, 8, INK) for i, l in enumerate(["Furnace check", "Water heater flush", "Smoke detector test"])) + btn(234, "Open My Home Record", col=TERRA)
    return screen(s, head=False)
add(G6, "Up Keep: Welcome Email", O("em_letter", "Plain Letter From Max", "Reads like a personal email. No graphics.", ["personal", "plain", "warm"], "neighbor", email("letter")),
            O("em_card", "Designed Card Email", "Logo, a visit card, a checklist and one button.", ["organized", "branded", "clear"], "system", email("card")), "Which Welcome Email?")
def report(kind):
    if kind == "check":
        s = h1(14, 56, "Visit Report · Oct 8", 16) + "".join(f'<line x1="14" y1="{66+i*28}" x2="226" y2="{66+i*28}" stroke="{LINE}"/>' + icon("check", 14, 72 + i * 28, 14, "duo", JUNGLE) + t(36, 83 + i * 28, n, 8.5, INK) + photo(190, 69 + i * 28, 36, 22, "label" if i % 2 else "tech", 3) for i, n in enumerate(["Furnace filter swapped", "Water heater flushed", "Smoke detectors tested", "AC coils rinsed", "Sump pump tested"]))
        return screen(s + link(14, 222, "Download PDF", INK) + btn(240, "Book Next Visit"))
    s = h1(14, 56, "Visit Report · Oct 8", 16) + ring(60, 112, 34, .92, JUNGLE, "") + t(60, 116, "92", 22, INK, "khand", anchor="middle") + t(60, 160, "HOME HEALTH", 6.5, MUTE, "hind", 600, "middle") + t(110, 94, "11 checks done", 9, INK, "hind", 600) + t(110, 108, "1 to watch: dryer vent", 8, MUTE) + t(110, 122, "0 urgent", 8, MUTE)
    s += rect(14, 176, 212, 40, CREAM, LINE, 4) + t(22, 192, "Danny's Note", 9.5, INK, "khand") + t(22, 206, "All good. Dryer vent needs a clean next time.", 7, MUTE)
    return screen(s + btn(240, "See All 11 Checks"))
add(G6, "Up Keep: Visit Report", O("vr_check", "Checklist With Photos", "Every item with a check and a photo beside it.", ["detailed", "evidence", "organized"], "crew", report("check")),
            O("vr_score", "Home Health Score Summary", "One score ring, a short summary and the tech's note.", ["summary", "calm", "modern"], "concierge", report("score")), "Which Visit Report?")
def report2(kind):
    if kind == "timeline":
        s = h1(14, 56, "Oct 8 Visit", 16) + f'<line x1="22" y1="66" x2="22" y2="250" stroke="{LINE}" stroke-width="2"/>'
        for i, (tm, n, k) in enumerate([("9:04", "Furnace filter swapped", "tech"), ("9:21", "Water heater flushed", "label"), ("9:40", "Detectors tested", "interior")]):
            y = 70 + i * 60; s += f'<circle cx="22" cy="{y+6}" r="4" fill="{INK}"/>' + t(32, y + 9, tm + " · " + n, 8, INK, "hind", 600) + photo(32, y + 14, 120, 38, k, 4)
        return screen(s)
    s = h1(14, 56, "Oct 8 Visit", 16) + rect(14, 66, 212, 16, "#F5F5F5") + t(20, 77, "SYSTEM", 6.5, MUTE, "hind", 600) + t(130, 77, "STATUS", 6.5, MUTE, "hind", 600) + t(220, 77, "PHOTO", 6.5, MUTE, "hind", 600, "end")
    s += "".join(f'<line x1="14" y1="{82+i*24}" x2="226" y2="{82+i*24}" stroke="{LINE}"/>' + t(20, 98 + i * 24, n, 8, INK) + t(130, 98 + i * 24, st, 8, MUTE) + t(220, 98 + i * 24, "View", 7.5, INK, "hind", 600, "end", 'text-decoration="underline"') for i, (n, st) in enumerate([("Furnace", "Filter swapped"), ("Water heater", "Flushed"), ("AC", "Coils rinsed"), ("Detectors", "6 of 6 OK"), ("Dryer vent", "Watch"), ("Sump pump", "OK")]))
    return screen(s)
add(G6, "Up Keep: Visit Report", O("vr_timeline", "Photo Timeline", "The visit in order, with a big photo for each step.", ["visual", "story", "transparent"], "neighbor", report2("timeline")),
            O("vr_table", "Table By System", "One row per system: status and a photo link.", ["organized", "compact", "efficient"], "system", report2("table")), "Which Report Layout?")

def inbox(subj, prev):
    rows=[("Up Keep", subj, prev, True), ("Hardware Co.", "Fall sale: 20% off", "Rakes, filters and more", False), ("City Water", "Your October bill", "Amount due $64.20", False)]
    s=rect(0,0,W,34,"#F5F5F5")+t(14,22,"Inbox",12,INK,"khand")
    for i,(fr,sj,pv,new) in enumerate(rows):
        y=40+i*48; s+=f'<line x1="0" y1="{y+46}" x2="{W}" y2="{y+46}" stroke="{LINE}"/>'+(f'<circle cx="8" cy="{y+12}" r="3" fill="{LAGOON}"/>' if new else "")+t(16,y+14,fr,8.5,INK,"hind",600 if new else 400)+t(16,y+27,sj,8.5,INK,"hind",600 if new else 400)+t(16,y+39,pv,7.5,MUTE)
    return screen(s,head=False)
add(G6, "Up Keep: Welcome Email", O("em_subj_welcome", "Subject: 'Welcome To Up Keep, Sarah'", "Classic welcome subject line in the inbox.", ["classic", "warm", "clear"], "concierge", inbox("Welcome To Up Keep, Sarah", "Your first visit is Tue, Nov 4 at 9 AM")),
            O("em_subj_danny", "Subject: 'Danny's Coming Tuesday At 9'", "Leads with the visit and the tech's name.", ["personal", "specific", "useful"], "neighbor", inbox("Danny's Coming Tuesday At 9", "Here's what he'll check at your house")), "Which Welcome Subject Line?")
def confirm2(kind):
    s=icon("check",14,44,26,"duo",JUNGLE)+h1(48,64,"You're In, Sarah.",19)
    if kind=="cal":
        s+=lbl(14,92,"Your visit schedule")+"".join(f'<line x1="14" y1="{100+i*26}" x2="226" y2="{100+i*26}" stroke="{LINE}"/>'+t(14,117+i*26,sn,9,INK,"hind",600)+t(226,117+i*26,d,8,MUTE,anchor="end") for i,(sn,d) in enumerate([("Fall","Tue, Nov 4"),("Winter","Feb 3"),("Spring","May 5"),("Summer","Aug 4")]))
        return screen(s+btn(216,"Add All 4 Visits To Calendar")+link(120,262,"Go To My Home Record",INK,"middle"))
    s+=para(14,92,["Want your partner to get visit reminders","and reports too?"],8.5,INK,12)+field(124,"Their phone or email","")+btn(164,"Invite To Up Keep","outline")+btn(216,"Go To My Home Record")
    return screen(s)
add(G6, "Up Keep: Confirmation", O("cf_cal", "Confirmation: Add All Visits To Calendar", "Shows the 4 seasonal dates with one calendar button.", ["organized", "practical", "planned"], "system", confirm2("cal")),
            O("cf_invite", "Confirmation: Invite Your Household", "Offers to add a partner for reminders and reports.", ["shared", "friendly", "family"], "neighbor", confirm2("invite")), "What Comes After Sign-Up?")

# ===================== 7. Swipe Controls (2) =====================
EARTH = ["#3F6E7D", "#5A7D4F", "#B5523B", "#A0703C"]
C = lambda i, l, desc, tags, **k: {"id": "uk1_" + i, "label": l, "desc": desc, "tags": tags, "feeling": None, "visual": {"type": "controls", "words": ["This", "Both", "Love", "That"], "icons": ["◀", "⇄", "❤", "▶"], "colors": EARTH, "bg": "#FFFFFF", "font": "Hind", "stampov": "word", "press": None, **k}}
add(G7, "Swipe Controls", C("sc_terra_square", "Terracotta Square Outline", "Square outline buttons in Up Keep terracotta.", ["warm", "clear"], fmt="square", style="outline", press="fill", colors=[TERRA] * 4, hint="edges"),
    C("sc_black_square", "Black Square Filled", "Square, filled black like the app's main buttons.", ["bold", "direct"], fmt="square", style="fill", colors=[INK] * 4, font="Khand", hint="edges"), "Which Swipe Controls?")
add(G7, "Swipe Controls", C("sc_micro_pill", "White Pills, One Color Each", "White pills with a small colored icon each (lagoon, jungle, berry, saffron).", ["micro-dose", "friendly"], fmt="pill", style="outline", colors=[LAGOON, JUNGLE, BERRY, SAFFRON], hint="edges"),
    C("sc_mono_round", "Grey Round, Color On Press", "Grey round buttons that fill with terracotta only when pressed.", ["minimal", "calm"], fmt="round", style="outline", press="fill", colors=["#737373"] * 4, hint="edges"), "Which Swipe Controls?")

# ---- order: open with an Up Keep choice; no category twice in a row ----
random.seed(12); first = pairs[:1]; rest = pairs[1:]; random.shuffle(rest); seq = first + rest; order = []
while seq:
    k = next((i for i, p in enumerate(seq) if not order or p["category"] != order[-1]["category"]), 0); order.append(seq.pop(k))
from trim_deck import DECK_SIZE, select, save_overflow  # decks are 25 pairs; extras go to banks/overflow
order, _cut = select(order, DECK_SIZE); save_overflow(DID, _cut)
for i, p in enumerate(order, 1):
    p.update(id=f"{DID}-{i:02d}", repeat=False)
alloc, feel, groups = {}, {}, {}
for p in order:
    alloc[p["category"]] = alloc.get(p["category"], 0) + 1; groups[p["group"]] = groups.get(p["group"], 0) + 1
    for s in "AB":
        f = p["option" + s].get("feeling")
        if f: feel[f] = feel.get(f, 0) + 1
ids = [p["option" + s]["id"] for p in order for s in "AB"]
assert len(ids) == len(set(ids)), "duplicate option id"
shown = set(json.load(open("shown_options.json")).get("options", {}))
import glob, os
for fp in glob.glob("decks/*.json"):
    if os.path.basename(fp) == f"{DID}.json": continue
    for pp in json.load(open(fp)).get("pairs", []):
        for s in "AB":
            o = pp.get("option" + s) or {}
            if o.get("id"): shown.add(o["id"])
rep = [i for i in ids if i in shown]; assert not rep, f"repeats: {rep}"
assert all(p["option" + s]["tags"] for p in order for s in "AB")
deck = {"date": DID, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True,
        "title": "Up Keep: App Choices, Color, Voice And Logo", "brands": ["Up Keep / Smart Upkeep: home maintenance membership app (https://webermanapps.github.io/smart-upkeep/)", "Base: white or cream, #0A0A0A ink, square black buttons, Khand/Hind; micro-dose accents (terracotta, lagoon, jungle, saffron, berry, persimmon)"],
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "feelings": {"neighbor": "Trusted neighbor", "system": "Calm organized system", "concierge": "Quiet premium concierge", "crew": "No-nonsense pro crew"},
        "feeling_counts": feel, "allocation": alloc, "groups": groups, "apps": {"Up Keep": len(order)},
        "pair_mix": {"refine": sum(p["purpose"] == "refine" for p in order), "check": sum(p["purpose"] == "check" for p in order), "retest": sum(p["retest"] for p in order)},
        "sources": {"app": "https://webermanapps.github.io/smart-upkeep/", "ideas": "/workspace/smartkeep/ideas/2026-10-12.md", "queue": "queue/blog-topics.md#Up Keep Pair List", "logos": LOGOS},
        "freshness": {"option_slots": len(ids), "never_shown_before": len(ids), "share": 1.0}, "warnings": [], "pairs": order}
json.dump(deck, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
print(len(order), "pairs", groups)
