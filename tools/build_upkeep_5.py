#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-5 (DRAFT, unpublished): 50 all-new this-or-that pairs, round 5 of the Up Keep / Smart Upkeep home maintenance
membership app (https://webermanapps.github.io/smart-upkeep/). Mock screens are drawn as SVG in Up Keep's own style
(white base, #0A0A0A ink, square black buttons, Khand headings, Hind body, terracotta accent, #E5E0D8 rules) and
rendered through the 'hm' svg renderer. Run from the style-swipe repo root."""
import json, random, re, datetime as dt
DID = "upkeep-5"; LOGOS = "/workspace/brand/smart-upkeep/logos"
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
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%">'
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

def tiercard(x, y, w, h, name, price, per, feats, hi=False, badge=None, col=INK, acc=TERRA):
    s = rect(x, y, w, h, SEL if hi else "#FFFFFF", INK if hi else LINE, 4, 1.5 if hi else 1)
    if badge: s += rect(x + 8, y - 6, len(badge) * 4.3 + 10, 12, acc, r=6) + t(x + 13 + len(badge) * 2.15, y + 2, badge.upper(), 5.8, "#FFFFFF", "hind", 600, "middle")
    s += h1(x + 8, y + 22, name, 14) + t(x + 8, y + 40, price, 15, INK, "khand") + t(x + 8 + len(price) * 6.4, y + 40, per, 7, MUTE)
    return s + "".join(t(x + 8, y + 54 + i * 11, "✓ " + f, 7, MUTE) for i, f in enumerate(feats))

# ---- extra helpers for round 2 ----
def ln(y, x1=14, x2=226): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LINE}"/>'
def dot(cx, cy, r, c): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
def face(cx, cy, r=14): return dot(cx, cy, r, "#C79B7B") + f'<path d="M{cx-r*.9} {cy+r*1.6} Q{cx} {cy+r*.6} {cx+r*.9} {cy+r*1.6}" fill="#3E4A52"/>'
def bell(x, y, c=INK, s=1): return f'<g transform="translate({x},{y}) scale({s})"><path d="M2 14 h16 l-2 -3 v-5 a6 6 0 0 0 -12 0 v5 Z" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/><circle cx="10" cy="17" r="2" fill="{c}"/></g>'
def shield(x, y, c, s=1, fill=True): return f'<g transform="translate({x},{y}) scale({s})"><path d="M12 2 L21 5 V11 Q21 18 12 22 Q3 18 3 11 V5 Z" fill="{c if fill else "none"}" stroke="{c}" stroke-width="1.6"/><path d="M8 12 l3 3 5 -6" fill="none" stroke="{"#FFFFFF" if fill else c}" stroke-width="2" stroke-linecap="round"/></g>'
def warn(x, y, c, s=1): return f'<g transform="translate({x},{y}) scale({s})"><path d="M12 2 L23 21 H1 Z" fill="{c}"/><rect x="11" y="8" width="2" height="7" fill="#FFFFFF"/><circle cx="12" cy="18" r="1.3" fill="#FFFFFF"/></g>'
def gift(x, y, c, s=1): return f'<g transform="translate({x},{y}) scale({s})"><rect x="3" y="9" width="18" height="12" fill="none" stroke="{c}" stroke-width="1.6"/><rect x="2" y="6" width="20" height="4" fill="{c}"/><line x1="12" y1="6" x2="12" y2="21" stroke="{c}" stroke-width="1.6"/><path d="M12 6 q-6 -6 -6 0 M12 6 q6 -6 6 0" fill="none" stroke="{c}" stroke-width="1.6"/></g>'
def phone_frame(body, bg="#EEF3F6"):  # lock screen style for notifications
    return screen(f'<rect width="{W}" height="{H}" fill="{bg}"/>' + t(120, 44, "9:41", 26, INK, "khand", anchor="middle") + t(120, 58, "Tuesday, November 4", 7.5, MUTE, anchor="middle") + body, head=False)
def notif(y, title, body_lines, app="UP KEEP", accent=TERRA, h=None, extra=""):
    h = h or 30 + 11 * len(body_lines)
    return (rect(12, y, 216, h, "#FFFFFF", "none", 12, 1, 'opacity=".97"') + rect(20, y + 8, 14, 14, "#FFFFFF", LINE, 3) + f'<polyline points="{22},{y+18} {27},{y+12} {32},{y+18}" fill="none" stroke="{accent}" stroke-width="1.6"/>'
            + t(40, y + 18, app, 6.5, MUTE, "hind", 600, extra='letter-spacing=".8"') + t(220, y + 18, "now", 6.5, MUTE, anchor="end")
            + t(20, y + 34, title, 8.5, INK, "hind", 600) + "".join(t(20, y + 45 + i * 11, l, 7.8, MUTE) for i, l in enumerate(body_lines)) + extra)
def sms(lines, sender="Up Keep", tint="#E9E9EB"):
    s = rect(0, 0, W, 40, "#F7F7F7") + dot(120, 16, 9, "#C9C9C9") + t(120, 34, sender, 7, INK, "hind", 600, "middle") + ln(40, 0, W)
    y = 56
    for l in lines:
        hh = 12 + 10.5 * len(l); s += rect(14, y, 180, hh, tint, r=10) + "".join(t(22, y + 14 + i * 10.5, x, 7.8, INK) for i, x in enumerate(l)); y += hh + 8
    return screen(s + rect(14, 268, 212, 20, "#FFFFFF", "#D4D4D4", 10) + t(24, 281, "Text Message", 7, "#A3A3A3"), head=False)
def chip(x, y, s, on=False, col=INK, w=None):
    w = w or len(s) * 4.6 + 14
    return rect(x, y, w, 20, col if on else "#FFFFFF", col if on else "#CFC8BC", 0, 1.3) + t(x + w / 2, y + 13, s, 7.5, "#FFFFFF" if on else INK, "hind", 600, "middle")
def tabbar(cur=0, col=INK):
    s = f'<rect x="0" y="266" width="{W}" height="34" fill="#FFFFFF"/>' + ln(266, 0, W)
    for i, n in enumerate(["Home", "Calendar", "Record", "Invite"]):
        cx = 30 + i * 60; c = col if i == cur else "#A3A3A3"; s += rect(cx - 6, 273, 12, 10, "none", c, 2, 1.4) + t(cx, 293, n, 6, c, "hind", 600, "middle")
    return s

pairs = []
def O(i, label, desc, tags, feel, svg, bg="#F7F4EF"):
    return {"id": "uk5_" + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "notes": True, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": bg}}
def add(group, cat, a, b, ask, purpose="refine", retest=False):
    pairs.append({"group": group, "category": cat, "app": "Up Keep", "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": retest, "notes": True})
# Round-3 default: white base, black ink, 2-3 small pops: terracotta = act, lagoon = info, jungle = done, saffron = due soon
SYS = [("furnace", "Furnace", "Carrier 59SC5", "OK", JUNGLE), ("water", "Water Heater", "Rheem XG50T", "Due Nov", SAFFRON), ("ac", "AC Unit", "Trane XR14", "OK", JUNGLE), ("smoke", "Smoke Detectors", "6 of 6", "OK", JUNGLE)]
HOMEBODY = lbl(14, 48, "Hi Sarah") + h1(14, 66, "Welcome Home", 17) + rect(14, 76, 212, 56, CREAM, LINE, 6) + t(22, 96, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(22, 114, "Tue, Nov 4 · 9 AM", 13, INK, "khand") + "".join(ln(142 + i * 22) + t(14, 157 + i * 22, n, 8.5, INK) + tag(176, 148 + i * 22, st, c) for i, (_, n, _, st, c) in enumerate(SYS[:4]))
# ---- extra helpers for round 3 ----
def qr(x, y, s=40, c=INK):
    random.seed(int(x * 7 + y)); n = 11; u = s / n; o = ""
    for i in range(n):
        for j in range(n):
            if (i < 3 and j < 3) or (i < 3 and j > 7) or (i > 7 and j < 3): continue
            if random.random() < .5: o += rect(x + i * u, y + j * u, u, u, c)
    for a, b in [(0, 0), (8, 0), (0, 8)]: o += rect(x + a * u, y + b * u, 3 * u, 3 * u, "none", c, 0, u * .6) + rect(x + (a + 1) * u, y + (b + 1) * u, u, u, c)
    return o
def van(x, y, s=1, body="#FFFFFF", stripe=TERRA, logo=INK):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0 20 V6 Q0 0 6 0 H120 L150 18 V48 H0 Z" fill="{body}" stroke="#6E6E6E" stroke-width="1.2"/><path d="M122 4 L144 18 H122 Z" fill="#B8CCD8"/>'
            + (rect(0, 34, 150, 6, stripe) if stripe else "") + f'<circle cx="32" cy="48" r="9" fill="#2B2B2B"/><circle cx="118" cy="48" r="9" fill="#2B2B2B"/></g>' + roof_logo(x + 16 * s, y + 24 * s, s * 1.4, logo, stripe or MUTE))
def bars(x, y, vals, cols, w=16, gap=10, hmax=60, labels=None):
    o = ""
    for i, v in enumerate(vals):
        c = cols[i % len(cols)]; hh = hmax * v; o += rect(x + i * (w + gap), y + hmax - hh, w, hh, c, r=2)
        if labels: o += t(x + i * (w + gap) + w / 2, y + hmax + 11, labels[i], 6.5, MUTE, "hind", 600, "middle")
    return o
def check_box(x, y, on, c=JUNGLE): return rect(x, y, 11, 11, c if on else "#FFFFFF", c if on else "#BDB6AA", 2, 1.3) + (f'<path d="M{x+2.5} {y+5.5} l2.5 2.5 4 -5" fill="none" stroke="#FFFFFF" stroke-width="1.6"/>' if on else "")
def rows(y, items, dy=24, x=14, right_col=MUTE):
    return "".join(ln(y + i * dy) + t(x, y + 15 + i * dy, a, 8.5, INK) + t(226, y + 15 + i * dy, b, 7.5, right_col, anchor="end") for i, (a, b) in enumerate(items))
def house_ill(x, y, s, roof, door, win, sun=None, ground="#9DB58A"):
    return (f'<g transform="translate({x},{y}) scale({s})">' + (f'<circle cx="150" cy="20" r="12" fill="{sun}"/>' if sun else "") + f'<rect x="0" y="96" width="180" height="8" fill="{ground}"/><path d="M26 54 L90 10 L154 54 Z" fill="{roof}"/>'
            + f'<rect x="36" y="54" width="108" height="42" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/><rect x="80" y="66" width="20" height="30" fill="{door}"/><rect x="48" y="62" width="20" height="16" fill="{win}"/><rect x="112" y="62" width="20" height="16" fill="{win}"/></g>')
SYS3 = [("furnace", "Furnace"), ("water", "Water Heater"), ("ac", "AC Unit"), ("smoke", "Smoke Detectors")]
GR, GH, GL, GG, GT, GBL, GLL, GMK, GFB, GON = ("Visit Report", "Home Health & Forecast", "History & Documents", "Homeowner Guides", "My Tech & Contact",
    "Billing & Membership", "Multi-Home View", "Marketing & Social", "Field Branding & Labels", "Onboarding & Settings")
GK, GS = "Multi-Accent Color", "Swipe Controls"
# ---- helpers carried over from upkeep-4 ----
from PIL import Image
MOCK = "/workspace/brand/smart-upkeep/mockups"
PRICE = "Membership Starting at $99/Month"
BORD = "#E5E5E5"
NAVY = "#171717"
def sq_btn(x, y, s, w=None, h=18, col=NAVY, ic=None):
    w = w or len(s) * 5.2 + 16 + (12 if ic else 0)
    return rect(x, y, w, h, "#FFFFFF", col, 0, 2) + (ic(x + 6, y + 4) if ic else "") + t(x + w / 2 + (6 if ic else 0), y + h / 2 + 2.6, s.upper(), 7, col, "khand", extra='letter-spacing="1"')
def share_ic(x, y): return f'<g transform="translate({x},{y})"><path d="M5 1 V7 M2 3.5 L5 .5 L8 3.5 M1 6 V10 H9 V6" fill="none" stroke="{NAVY}" stroke-width="1.3"/></g>'
def call_ic(x, y): return icon("phone", x, y - 1, 11, "outline")
def mwhdr(v="share", bg="#FFFFFF"):
    o = rect(0, 0, W, 34, bg)
    if v == "center": o += roof_logo(92, 22, 1, INK, MUTE) + sq_btn(186, 8, "Share", 44)
    elif v == "byline": o += roof_logo(14, 19, 1, INK, MUTE) + t(14, 28, "BY MAX WEBERMAN", 5.2, MUTE, "khand", extra='letter-spacing="1.4"') + sq_btn(172, 8, "Share", 54, ic=share_ic)
    elif v == "call": o += roof_logo(14, 22, 1, INK, MUTE) + sq_btn(120, 8, "Call", 48, ic=call_ic) + sq_btn(172, 8, "Share", 54, ic=share_ic)
    else: o += roof_logo(14, 22, 1, INK, MUTE) + sq_btn(172, 8, "Share", 54, ic=share_ic)
    return o + f'<line x1="0" y1="34" x2="{W}" y2="34" stroke="{BORD}"/>'
def scr(body, bg="#FFFFFF", head="share"):
    return screen((mwhdr(head, bg) if head else "") + body, bg, head=False)
def home(acc="multi", bg="#FFFFFF", card="#FFFFFF"):
    eb = LAGOON if acc == "multi" else MUTE
    o = t(14, 52, "HOME MAINTENANCE MEMBERSHIP", 6.2, eb, "hind", 600, extra='letter-spacing="1.4"') + h1(14, 76, "Your Home, Taken Care Of.", 21)
    if acc in ("multi", "one"): o += rect(14, 83, 34, 3, TERRA)
    o += para(14, 100, ["One membership for the upkeep your home", "needs all year, done by licensed techs."], 8.2, MUTE, 11)
    o += btn(124, "Get Started", "fill", INK, h=30, size=10)
    rowsd = [("water", "When Did You Last Flush The Water Heater?", LAGOON), ("check", "A Simple List We Handle For You", JUNGLE), ("cam", "Photos From Every Visit", TERRA)]
    for i, (k, s, c) in enumerate(rowsd):
        y = 166 + i * 40; o += rect(14, y, 212, 34, card, LINE, 6) + icon(k, 22, y + 8, 18, "duo" if acc == "multi" else "outline", c if acc == "multi" else INK) + t(48, y + 21, s, 8, INK, "khand")
    return o
def cream_home():
    return screen(home("multi", CREAM, "#FFFDF8"), CREAM, head=True)
G1 = "White Base & Header"
FIRST = len(pairs)
G2 = "Membership Plan Card"
INC = [("furnace", "Furnace And AC Tune-Ups"), ("water", "Water Heater Flush"), ("smoke", "Smoke And CO Checks"), ("cam", "Photo Report Every Visit")]
def plan(price="stack", inc="list", cta=INK, cancel="under", frame="bar", bg="#FFFFFF"):
    o = h1(14, 56, "Your Membership", 18)
    o += rect(14, 66, 212, 200, "#FFFFFF" if bg == CREAM else "#FFFFFF", LINE if frame != "bar" else LINE, 6) + (rect(14, 66, 212, 4, TERRA) if frame == "bar" else "")
    if cancel == "tag": o += tag(22, 76, "Cancel Anytime", JUNGLE)
    py = 96 if cancel == "tag" else 84
    if price == "stack":
        o += t(120, py + 4, "MEMBERSHIP STARTING AT", 6.5, MUTE, "hind", 600, "middle", 'letter-spacing="1.2"') + t(108, py + 32, "$99", 30, TERRA, "khand", anchor="middle") + t(140, py + 32, "/Month", 10, INK, "khand", anchor="middle")
        y = py + 46
    else:
        o += t(120, py + 10, PRICE, 11.5, INK, "khand", anchor="middle"); y = py + 26
    o += ln(y, 22, 218); y += 8
    if inc == "list":
        for i, (k, s) in enumerate(INC): o += icon("check", 24, y + i * 20, 12, "duo", JUNGLE) + t(42, y + 10 + i * 20, s, 8.2, INK)
        y += 82
    elif inc == "grid":
        for i, (k, s) in enumerate(INC):
            x0 = 22 + (i % 2) * 100; y0 = y + (i // 2) * 38
            o += rect(x0, y0, 96, 34, CREAM, "none", 4) + icon(k, x0 + 6, y0 + 8, 16, "duo", [TERRA, LAGOON, JUNGLE, SAFFRON][i]) + t(x0 + 27, y0 + 15, s.split(" ")[0], 7.5, INK, "khand") + t(x0 + 27, y0 + 25, " ".join(s.split(" ")[1:3]), 6.3, MUTE)
        y += 80
    else:
        for i, s in enumerate(["Spring", "Summer", "Fall", "Winter"]):
            cx = 40 + i * 54; o += dot(cx, y + 14, 9, [JUNGLE, SAFFRON, TERRA, LAGOON][i] + "26") + t(cx, y + 17, str(i + 1), 8, [JUNGLE, SAFFRON, TERRA, LAGOON][i], "khand", anchor="middle") + t(cx, y + 36, s, 7, INK, "hind", 600, "middle")
            if i < 3: o += f'<line x1="{cx+11}" y1="{y+14}" x2="{cx+43}" y2="{y+14}" stroke="{LINE}" stroke-width="1.5"/>'
        o += t(120, y + 54, "Four Visits A Year, We Book Them", 7.5, MUTE, anchor="middle"); y += 66
    o += btn(min(y + 4, 230), "Get My Personal Price", "fill", cta, x=22, w=196, h=26, size=8.5)
    if cancel == "under": o += icon("check", 84, 262 - 2, 10, "duo", JUNGLE) + t(98, 267 - 1, "Cancel Anytime", 7.5, INK, "hind", 600)
    return scr(o, bg)
def plan_cmp(mode):
    o = h1(14, 56, "One Membership", 18) + t(14, 72, "Built around your home, not a tier.", 8, MUTE)
    if mode == "split":
        o += rect(14, 84, 104, 150, CREAM, LINE, 6) + rect(122, 84, 104, 150, "#FFFFFF", INK, 6, 1.5) + t(66, 102, "ON YOUR OWN", 6.5, MUTE, "hind", 600, "middle") + t(174, 102, "WITH SMART UPKEEP", 6.5, TERRA, "hind", 600, "middle")
        for i, (a, b) in enumerate([("You Remember", "We Book It"), ("You Find A Pro", "Same Tech"), ("No Record", "Photo Report"), ("Surprise Bills", "One Monthly Price")]):
            o += t(66, 126 + i * 26, a, 8, MUTE, anchor="middle") + t(174, 126 + i * 26, b, 8.5, INK, "khand", anchor="middle")
    else:
        o += rect(14, 84, 212, 150, "#FFFFFF", LINE, 6)
        for i, s in enumerate(["We Book Every Visit", "The Same Licensed Tech", "Photo Report Every Visit", "One Monthly Price"]): o += icon("check", 24, 98 + i * 32, 14, "duo", JUNGLE) + t(46, 109 + i * 32, s, 10, INK, "khand")
    return scr(o + t(120, 252, PRICE, 10.5, INK, "khand", anchor="middle") + t(120, 266, "Cancel Anytime", 7.5, JUNGLE, "hind", 600, "middle") + btn(272, "See My Price", "fill", INK, h=22, size=8))
G3 = "Extras & Add-Ons"
def aic(k, x, y, s=18, c=INK, duo=False):
    f = c + "33" if duo else "none"; st = c if duo else INK; g = f'<g transform="translate({x},{y}) scale({s/24})" fill="none" stroke="{st}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    P = {"gutter": f'<path d="M2 7 H22 L20 12 H4 Z" fill="{f}"/><path d="M18 12 V21"/><path d="M8 15 q1 2 0 3"/>',
         "vent": f'<circle cx="12" cy="12" r="9" fill="{f}"/><path d="M7 9 H17 M7 12 H17 M7 15 H17"/>',
         "lawn": f'<path d="M2 21 H22" /><path d="M5 21 L6 13 M9 21 L9 10 M13 21 L14 12 M17 21 L18 9" /><circle cx="18" cy="6" r="2.5" fill="{f}"/>',
         "snow": f'<path d="M12 3 V21 M4 7.5 L20 16.5 M20 7.5 L4 16.5"/><circle cx="12" cy="12" r="2.5" fill="{f}"/>',
         "window": f'<rect x="4" y="3" width="16" height="18" fill="{f}"/><path d="M12 3 V21 M4 12 H20"/>',
         "wash": f'<path d="M3 10 H11 L14 7 V13 L11 10" fill="{f}"/><path d="M15 6 l5 -2 M15 10 h6 M15 14 l5 2"/>'}
    return g + P[k] + "</g>"
EX = [("gutter", "Gutter Cleaning", "Spring And Fall"), ("vent", "Dryer Vent Clean", "Once A Year"), ("lawn", "Lawn Mowing", "Weekly In Season"), ("snow", "Snow Clearing", "Every Storm"), ("window", "Window Washing", "Inside And Out"), ("wash", "Power Washing", "Siding And Deck")]
ECOL = [LAGOON, TERRA, JUNGLE, LAGOON, SAFFRON, TERRA]
def extras(layout="grid", sel="check", ic="outline", sub=True, add_ui="corner", bg="#FFFFFF"):
    o = h1(14, 56, "Add Extras", 18) + t(14, 70, "Tap to add to your plan.", 7.8, MUTE)
    on = {0, 2}
    for i, (k, n, s) in enumerate(EX):
        c = ECOL[i]; duo = ic == "duo"; picked = i in on
        if layout == "grid":
            x = 14 + (i % 2) * 108; y = 80 + (i // 2) * 62; w, h = 104, 56
            bc, sw = ((JUNGLE, 2) if sel == "check" else (TERRA, 2)) if picked else (LINE, 1)
            fill = (TERRA + "14") if (picked and sel == "fill") else "#FFFFFF"
            o += rect(x, y, w, h, fill, bc, 8, sw) + aic(k, x + 8, y + 8, 20, c if duo else INK, duo) + t(x + 8, y + 40, n, 8.6, INK, "khand") + (t(x + 8, y + 50, s, 6.4, MUTE) if sub else "")
            if add_ui == "corner": o += (icon("check", x + w - 20, y + 6, 14, "duo", JUNGLE) if picked and sel == "check" else (dot(x + w - 13, y + 13, 7, TERRA) + t(x + w - 13, y + 16.5, "+" if not picked else "-", 10, "#FFFFFF", "khand", anchor="middle") if sel == "fill" or not picked else ""))
            if add_ui == "corner" and not picked and sel == "check": o += rect(x + w - 20, y + 6, 14, 14, "#FFFFFF", "#BDB6AA", 7, 1.3) + t(x + w - 13, y + 17, "+", 10, MUTE, "khand", anchor="middle")
            if add_ui == "button": o += rect(x + w - 34, y + 34, 28, 14, INK if not picked else JUNGLE, "none", 0) + t(x + w - 20, y + 44, "ADDED" if picked else "ADD", 5.6, "#FFFFFF", "hind", 600, "middle")
        else:
            y = 80 + i * 30; o += ln(y) + aic(k, 16, y + 5, 18, c if duo else INK, duo) + t(42, y + 15, n, 9, INK, "khand") + (t(42, y + 25, s, 6.4, MUTE) if sub else "") + toggle(202, y + 9, picked, JUNGLE)
    return scr(o + sticky(btn(266, "2 Extras Added · Continue", "fill", INK, h=24, size=8)), bg)
def extras_season(mode):
    o = h1(14, 56, "Add Extras", 18)
    if mode == "season":
        y = 70
        for sname, items, c in [("Spring And Summer", [0, 2, 5], JUNGLE), ("Fall And Winter", [1, 3, 4], LAGOON)]:
            o += lbl(14, y + 8, sname, c); y += 14
            for j, i in enumerate(items): o += rect(14 + j * 72, y, 68, 66, "#FFFFFF", LINE, 8) + aic(EX[i][0], 36 + j * 72, y + 10, 24, c, True) + t(48 + j * 72, y + 52, EX[i][1].split(" ")[0], 8, INK, "khand", anchor="middle")
            y += 78
    else:
        for i, (k, n, s) in enumerate(EX[:3]):
            y = 70 + i * 62; o += rect(14, y, 212, 56, "#FFFFFF", LINE, 8) + dot(42, y + 28, 18, ECOL[i] + "1F") + aic(k, 30, y + 16, 24, ECOL[i], True) + t(70, y + 26, n, 11, INK, "khand") + t(70, y + 40, s, 7.5, MUTE) + rect(184, y + 19, 32, 18, INK, "none", 0) + t(200, y + 31, "ADD", 6.5, "#FFFFFF", "hind", 600, "middle")
        o += link(14, 268, "See 3 More Extras", LAGOON)
    return scr(o)
G4 = "Tech Profile & License"
def techface(cx, cy, r, cap=INK):
    return dot(cx, cy + r * 1.9, r * 1.35, "#5E6B73") + dot(cx, cy, r, "#B07D5B") + f'<path d="M{cx-r} {cy-r*.25} Q{cx} {cy-r*1.5} {cx+r} {cy-r*.25} Z" fill="{cap}"/>' + rect(cx - r * .2, cy - r * .5, r * 1.5, r * .22, cap)
def chips(x, y, style):
    o = ""; xx = x
    for n, c in [("Certified", LAGOON), ("Trained", JUNGLE), ("Insured", TERRA)]:
        w = len(n) * 5 + 14
        if style == "black": o += rect(xx, y, w, 15, INK) + t(xx + w / 2, y + 10.5, n.upper(), 6.3, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
        elif style == "outline": o += rect(xx, y, w, 15, c + "14", c, 0, 1.2) + t(xx + w / 2, y + 10.5, n.upper(), 6.3, c, "hind", 600, "middle", 'letter-spacing="1"')
        elif style == "seal":
            cx = xx + 22; o += dot(cx, y + 18, 17, c + "1F") + f'<circle cx="{cx}" cy="{y+18}" r="17" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="2 2"/>' + shield(cx - 8, y + 9, c, .7) + t(cx, y + 46, n, 7, INK, "hind", 600, "middle"); w = 52
        else:
            o += f'<path d="M{xx} {y} H{xx+w} V{y+15} L{xx+w/2} {y+21} L{xx} {y+15} Z" fill="{c}"/>' + t(xx + w / 2, y + 10.5, n.upper(), 6.3, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
        xx += w + 6
    return o
def techprof(ch="black", verify="button", head="big", extra="stats", sheet=None):
    o = ""
    if head == "big": o += techface(120, 74, 20) + t(120, 124, "Danny Ruiz", 17, INK, "khand", anchor="middle") + t(120, 136, "Your Tech · Licensed Mechanical Contractor", 7, MUTE, anchor="middle"); y = 146; cx = 120
    else: o += lbl(14, 50, "Your Tech") + techface(34, 72, 13) + t(56, 70, "Danny Ruiz", 15, INK, "khand") + t(56, 82, "Licensed Mechanical Contractor", 7, MUTE); y = 98; cx = None
    wtot = {"black": 172, "outline": 172, "seal": 168, "ribbon": 172}[ch]
    o += chips((W - wtot) / 2 if cx else 14, y, ch); y += 54 if ch == "seal" else 28
    if extra == "stats":
        for i, (n, l) in enumerate([("9", "Years"), ("1,240", "Visits"), ("4.9", "Rating")]): o += t(48 + i * 72, y + 16, n, 15, INK, "khand", anchor="middle") + t(48 + i * 72, y + 26, l.upper(), 5.8, MUTE, "hind", 600, "middle")
        y += 36
    else:
        o += rect(14, y, 212, 34, CREAM, "none", 6) + para(22, y + 14, ["\"I'll be the one at your door every visit.", "Ask me anything.\""], 7.6, INK, 10); y += 42
    if verify == "button": o += rect(14, y, 212, 26, LAGOON) + shield(54, y + 5, "#FFFFFF", .65, False) + t(124, y + 17, "TAP TO VERIFY LICENSE", 8, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
    else: o += shield(14, y + 2, LAGOON, .65, False) + link(34, y + 15, "Tap To Verify License", LAGOON, size=8)
    if sheet: o += sheet
    return scr(o)
def lic_sheet(mode):
    if mode == "inline":
        return rect(14, 246, 212, 46, "#FFFFFF", JUNGLE, 4, 1.5) + icon("check", 22, 256, 16, "duo", JUNGLE) + t(44, 262, "License Active", 10, INK, "khand") + t(44, 274, "State Of Michigan · Mechanical", 6.6, MUTE) + t(44, 284, "Checked Oct 12, 2026", 6.2, MUTE)
    return (rect(0, 0, W, H, INK, extra='opacity=".35"') + rect(0, 120, W, 180, "#FFFFFF", r=14) + rect(108, 128, 24, 3, "#D4D4D4", r=1.5) + dot(120, 166, 24, JUNGLE + "1F") + shield(106, 152, JUNGLE, 1.2)
            + t(120, 210, "License Verified", 16, INK, "khand", anchor="middle") + t(120, 224, "State Of Michigan · Mechanical Contractor", 7.2, MUTE, anchor="middle") + t(120, 236, "License Active", 7.2, INK, anchor="middle") + link(120, 256, "Open State Lookup", LAGOON, "middle") + btn(266, "Done", "outline", h=22, size=8))
def door_card(mode):
    o = lbl(14, 50, "Arriving Today · 9 AM") + h1(14, 70, "Danny Is On The Way", 17)
    if mode == "id":
        o += rect(40, 84, 160, 170, "#FFFFFF", INK, 10, 1.5) + rect(40, 84, 160, 26, INK, r=0) + roof_logo(84, 102, .9, "#FFFFFF", "#BDBDBD") + techface(120, 140, 18) + t(120, 186, "Danny Ruiz", 14, INK, "khand", anchor="middle") + chips(34, 196, "black") + shield(60, 226, LAGOON, .6, False) + link(78, 237, "Tap To Verify License", LAGOON, size=7)
    else:
        o += rect(14, 84, 212, 66, CREAM, "none", 8) + techface(42, 108, 13) + t(66, 108, "Danny Ruiz", 13, INK, "khand") + t(66, 120, "White van, terracotta stripe", 7, MUTE) + van(24, 160, .9) + rect(14, 216, 212, 26, LAGOON) + t(120, 233, "TAP TO VERIFY LICENSE", 8, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
    return scr(o + btn(262, "Call Danny", "outline", h=24, size=8))
G5 = "Yard Sign"
def yard(stake="h", msg="maint", bar="terra", code="url", shape="land"):
    o = rect(0, 0, W, H, "#DCEAF0") + rect(0, 200, W, 100, "#9DB58A") + house_ill(150, 70, .55, "#5B5550", "#6B4B3A", "#B8CCD8") + dot(30, 196, 22, "#7E9C6B")
    sw, sh = (176, 108) if shape == "land" else (124, 146)
    x, y = 120 - sw / 2, 206 - sh - 4
    if stake == "h": o += rect(x + 24, y + sh, 3, 50, "#6E6E6E") + rect(x + sw - 27, y + sh, 3, 50, "#6E6E6E")
    else: o += rect(x - 8, y - 10, 3, sh + 64, "#2B2B2B") + rect(x - 8, y - 10, sw + 16, 3, "#2B2B2B") + f'<line x1="{x+20}" y1="{y-7}" x2="{x+20}" y2="{y}" stroke="#2B2B2B"/><line x1="{x+sw-20}" y1="{y-7}" x2="{x+sw-20}" y2="{y}" stroke="#2B2B2B"/>'
    o += rect(x, y, sw, sh, "#FFFFFF", "#BDBDBD", 2) + roof_logo(x + sw / 2 - 34 * (1.1 if shape == "land" else 1), y + 28, 1.1 if shape == "land" else 1, INK, MUTE)
    cy = y + 44
    if msg == "maint": o += t(x + sw / 2, cy, "THIS HOME IS MAINTAINED BY", 5.6, MUTE, "hind", 600, "middle", 'letter-spacing="1"') + t(x + sw / 2, cy + 13, "Smart Upkeep Members", 10, INK, "khand", anchor="middle")
    else: o += t(x + sw / 2, cy + 2, "Membership Starting at", 8, INK, "khand", anchor="middle") + t(x + sw / 2, cy + 18, "$99/Month", 15, TERRA if bar != "lagoon" else LAGOON, "khand", anchor="middle")
    if code == "qr": o += qr(x + sw / 2 - 11, y + sh - 34, 22) if shape != "land" else qr(x + sw - 28, y + sh - 28, 20)
    else: o += t(x + sw / 2, y + sh - 12, "smartupkeep.com", 7.5, INK, "hind", 600, "middle")
    if bar == "terra": o += rect(x, y + sh - 6, sw, 6, TERRA)
    elif bar == "lagoon": o += rect(x + sw / 2 - 18, y + 34, 36, 2.5, LAGOON)
    return screen(o, head=False)
G6 = "Van Wrap"
def van2(stripe="mid", logo="side", line="phone", roof=False, sc=TERRA):
    o = rect(0, 0, W, H, "#F2F1EE") + rect(0, 214, W, 86, "#C9C6C0") + h1(14, 44, "Van Side", 13, MUTE)
    x, y = 14, 96
    o += f'<path d="M{x} {y+110} V{y+14} Q{x} {y} {x+14} {y} H{x+150} L{x+206} {y+52} V{y+110} Z" fill="#FFFFFF" stroke="#6E6E6E" stroke-width="1.2"/><path d="M{x+154} {y+8} L{x+196} {y+50} H{x+154} Z" fill="#B8CCD8"/><line x1="{x+150}" y1="{y+8}" x2="{x+150}" y2="{y+110}" stroke="#BDBDBD"/>'
    if stripe == "thin": o += rect(x, y + 86, 206, 4, sc)
    elif stripe == "thick": o += rect(x, y + 80, 206, 16, sc)
    elif stripe == "swoop": o += f'<path d="M{x} {y+96} L{x+120} {y+96} Q{x+150} {y+96} {x+170} {y+60} L{x+178} {y+60} Q{x+158} {y+104} {x+120} {y+104} L{x} {y+104} Z" fill="{sc}"/>'
    else: o += rect(x, y + 84, 206, 8, sc)
    if roof: o += f'<polyline points="{x+20},{y+86} {x+75},{y+70} {x+130},{y+86}" fill="none" stroke="{sc}" stroke-width="3"/>'
    if logo == "side": o += roof_logo(x + 22, y + 48, 1.9, INK, MUTE)
    else: o += roof_logo(x + 158, y + 76, .7, INK, MUTE) + roof_logo(x + 18, y + 40, 1.2, INK, MUTE)
    if line == "phone": o += t(x + 22, y + 70, "(313) 555-0142 · smartupkeep.com", 7.5, INK, "hind", 600)
    elif line == "lic": o += icon("check", x + 22, y + 60, 11, "duo", JUNGLE) + t(x + 36, y + 69, "Licensed & Insured Home Techs", 7.8, INK, "hind", 600)
    else: o += t(x + 22, y + 70, PRICE, 8, INK, "khand")
    o += dot(x + 44, y + 110, 15, "#2B2B2B") + dot(x + 44, y + 110, 6, "#9E9E9E") + dot(x + 168, y + 110, 15, "#2B2B2B") + dot(x + 168, y + 110, 6, "#9E9E9E")
    return screen(o, head=False)
G7 = "Uniform On People"
def polo_img(keys, cap=""):
    n = len(keys); w = W / n; o = rect(0, 0, W, H, "#F2EFEA")
    for i, k in enumerate(keys): o += f'<image href="img/uk4_polo_{k}.jpg" x="{i*w+2}" y="16" width="{w-4}" height="252" preserveAspectRatio="xMidYMid slice"/>'
    return screen(o + (t(120, 290, cap, 9, INK, "khand", anchor="middle") if cap else ""), head=False)
G8 = "Lawn Quote"
def sat(x, y, w, h, col=LAGOON, handles=False, zones=False):
    o = f'<defs><clipPath id="s{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/></clipPath></defs><g clip-path="url(#s{x}{y})">' + rect(x, y, w, h, "#B9C99F")
    o += rect(x, y + h * .78, w, h * .22, "#D8D4CC") + rect(x + w * .62, y + h * .35, w * .14, h * .45, "#E3DED5")
    o += rect(x + w * .3, y + h * .3, w * .3, h * .26, "#8F8780") + f'<path d="M{x+w*.3} {y+h*.43} H{x+w*.6}" stroke="#7A736C"/>'
    for cx, cy, r in [(.1, .15, .1), (.88, .2, .09), (.15, .65, .07), (.86, .62, .08)]: o += dot(x + w * cx, y + h * cy, h * r, "#7E9C6B")
    pts = [(.05, .04), (.95, .04), (.95, .76), (.05, .76)]
    P = " ".join(f"{x+w*a:.1f},{y+h*b:.1f}" for a, b in pts)
    o += f'<polygon points="{P}" fill="{col}22" stroke="{col}" stroke-width="2" stroke-dasharray="5 3"/>'
    if handles: o += "".join(f'<circle cx="{x+w*a}" cy="{y+h*b}" r="4" fill="#FFFFFF" stroke="{col}" stroke-width="2"/>' for a, b in pts)
    if zones: o += f'<line x1="{x+w*.05}" y1="{y+h*.3}" x2="{x+w*.95}" y2="{y+h*.3}" stroke="{col}" stroke-width="1.5"/>' + tag(x + 8, y + 10, "Back 4,140", col, True) + tag(x + 8, y + h * .6, "Front 2,100", col, True)
    return o + "</g>"
def lawn(order="map", col=LAGOON, num="big", freq="chips", handles=False, extra="season"):
    o = lbl(14, 48, "Lawn Mowing Quote") + h1(14, 66, "We Measured Your Yard", 16)
    if order == "map":
        o += sat(14, 74, 212, 120, col, handles, num == "zones"); y = 204
        if num == "big": o += t(14, y + 18, "6,240", 22, INK, "khand") + t(76, y + 18, "Sq Ft Of Lawn", 8.5, MUTE); y += 28
        else: o += rows(y - 6, [("Front Lawn", "2,100 Sq Ft"), ("Back Lawn", "4,140 Sq Ft")], 18); y += 32
    else:
        o += rect(14, 74, 212, 64, CREAM, "none", 6) + t(22, 108, "$46", 30, TERRA, "khand") + t(74, 100, "Per Cut", 10, INK, "khand") + t(74, 112, "6,240 Sq Ft Measured", 7, MUTE) + sat(14, 146, 212, 70, col, handles, False); y = 226
    if freq == "chips": o += chip(14, y, "Weekly", True, JUNGLE, 60) + chip(78, y, "Every Other Week", False, INK, 82) + chip(164, y, "One Time", False, INK, 62)
    else: o += t(14, y + 13, "Weekly All Season", 8.5, INK, "hind", 600) + toggle(204, y + 4, True, JUNGLE)
    y += 28
    if order == "map": o += t(14, y + 14, "$46", 18, TERRA, "khand") + t(44, y + 14, "Per Cut" + (" · 26 Cuts April To October" if extra == "season" else ""), 7.5, MUTE)
    if handles: o += t(226, 210 if order == "map" else 230, "DRAG CORNERS TO FIX", 5.6, col, "hind", 600, "end")
    return scr(o + sticky(btn(270, "Add Mowing To My Plan", "fill", INK, h=22, size=8), 264))
def lawn_steps(mode):
    o = lbl(14, 48, "Lawn Mowing Quote") + h1(14, 66, "Get A Mowing Price", 16)
    if mode == "steps":
        for i, (s, c) in enumerate([("Type Your Address", JUNGLE), ("We Outline Your Lawn", JUNGLE), ("See Your Price", TERRA)]):
            y = 80 + i * 40; o += dot(28, y + 12, 11, c) + t(28, y + 16, str(i + 1), 10, "#FFFFFF", "khand", anchor="middle") + t(48, y + 16, s, 11, INK, "khand") + (f'<line x1="28" y1="{y+24}" x2="28" y2="{y+40}" stroke="{LINE}" stroke-width="2"/>' if i < 2 else "")
        o += field(212, "Address", "1418 Maple Ave, Royal Oak")
    else:
        o += field(78, "Address", "1418 Maple Ave, Royal Oak") + sat(14, 110, 212, 120, LAGOON) + t(120, 246, "Measuring From Above...", 8, LAGOON, "hind", 600, "middle")
    return scr(o + sticky(btn(270, "Measure My Lawn", "fill", INK, h=22, size=8), 264))
G9 = "Moisture-Scan Character"
def scan_tech(x, y, s=1, style="flat", shirt="#5E6B73", cap="#2B2B2B"):
    lw = 'stroke="#0A0A0A" stroke-width="1.6"' if style == "line" else 'stroke="none"'
    sk = "#FFFFFF" if style == "line" else "#8A5A3C"; sh = "#FFFFFF" if style == "line" else shirt; pn = "#FFFFFF" if style == "line" else "#3E4A52"
    acc = shirt if style == "line" else "#FFFFFF"
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-9" y="38" width="7" height="34" fill="{pn}" {lw}/><rect x="2" y="38" width="7" height="34" fill="{pn}" {lw}/>'
            f'<path d="M-13 6 Q-13 0 -6 0 H6 Q13 0 13 6 V40 H-13 Z" fill="{sh}" {lw}/>' + (rect(-13, 30, 26, 3, acc) if style == "line" else "") +
            f'<rect x="4" y="8" width="5" height="6" fill="{acc}" />'
            f'<path d="M-13 8 L-22 30 L-16 32 L-9 16" fill="{sh}" {lw}/><rect x="-24" y="30" width="9" height="11" fill="#2B2B2B"/>'
            f'<path d="M13 8 L20 -6 L15 -8 L10 4" fill="{sh}" {lw}/>'
            f'<rect x="15" y="-24" width="9" height="17" rx="2" fill="#2B2B2B"/><rect x="17" y="-21" width="5" height="6" fill="#8FD0E0"/>'
            f'<circle cx="0" cy="-10" r="9" fill="{sk}" {lw}/><path d="M-10 -12 Q0 -24 10 -12 Z" fill="{cap}" {lw}/><rect x="0" y="-14" width="14" height="3" fill="{cap}"/></g>')
def scan(style="flat", shirt="#5E6B73", cap="#2B2B2B", fx="glow", label="caught", room="full", bg="#FFFFFF"):
    o = rect(0, 0, W, H, bg) + h1(14, 36, "A Moisture Scan Every Visit", 15)
    cy = 60
    if room == "full":
        o += f'<rect x="8" y="{cy}" width="224" height="190" fill="none" stroke="{INK}" stroke-width="1.5"/>' + f'<line x1="8" y1="{cy+170}" x2="232" y2="{cy+170}" stroke="{INK}" stroke-width="1.5"/>'
        o += f'<path d="M20 {cy+170} V{cy+140} H70 V{cy+170}" fill="none" stroke="{INK}" stroke-width="1.4"/><line x1="200" y1="{cy+170}" x2="200" y2="{cy+110}" stroke="{INK}" stroke-width="1.4"/><path d="M190 {cy+110} H210 L206 {cy+100} H194 Z" fill="none" stroke="{INK}" stroke-width="1.4"/>'
        tx, ty = 130, cy + 98
    else:
        o += dot(120, 168, 82, CREAM) + f'<line x1="40" y1="{cy+12}" x2="200" y2="{cy+12}" stroke="{INK}" stroke-width="1.5"/>'; tx, ty = 116, cy + 110
    ceil = cy + (0 if room == "full" else 12)
    mx = tx + 19
    if fx == "glow": o += f'<defs><radialGradient id="gl"><stop offset="0" stop-color="{LAGOON}" stop-opacity=".55"/><stop offset="1" stop-color="{LAGOON}" stop-opacity="0"/></radialGradient></defs><ellipse cx="{mx}" cy="{ceil+4}" rx="34" ry="18" fill="url(#gl)"/>'
    else: o += f'<line x1="{mx}" y1="{ty-24}" x2="{mx}" y2="{ceil+2}" stroke="{LAGOON}" stroke-width="1.5" stroke-dasharray="3 3"/>' + f'<ellipse cx="{mx}" cy="{ceil+3}" rx="12" ry="3" fill="none" stroke="{LAGOON}" stroke-width="1.5"/>'
    o += scan_tech(tx, ty, 1.15, style, shirt, cap)
    if label == "caught": o += rect(mx - 66, ceil + 14, 54, 15, SAFFRON, r=2) + t(mx - 39, ceil + 24.5, "Caught Early", 7, INK, "hind", 600, "middle")
    else: o += rect(mx - 64, ceil + 14, 44, 15, "#FFFFFF", LAGOON, 2, 1.2) + t(mx - 42, ceil + 24.5, "Normal", 7, LAGOON, "hind", 600, "middle")
    o += icon("check", 54, 270, 13, "duo", JUNGLE) + t(72, 280, "Saved To Your Home Record", 8.5, INK, "khand")
    return screen(o, head=False)
# ===================== upkeep-5 content (DRAFT) =====================
def card(x, y, w, h, mode="border", fill="#FFFFFF"):
    if mode == "shadow": return rect(x, y + 2, w, h, "#0A0A0A", r=8, extra='opacity=".06"') + rect(x, y, w, h, fill, "none", 8)
    return rect(x, y, w, h, fill, LINE, 8)
def wc_screen(bg, cardbg, mode="border", hero=False, headbg=None):
    o = ""
    if hero: o += rect(0, 34, W, 70, CREAM) + f'<line x1="0" y1="104" x2="{W}" y2="104" stroke="{LINE}"/>'
    o += lbl(14, 52, "Hi Sarah") + h1(14, 72, "Your Home", 19) + rect(14, 79, 34, 3, TERRA)
    for i, (k, n, st, c) in enumerate([("furnace", "Furnace", "Checked Nov 4", JUNGLE), ("water", "Water Heater", "Flush Due Nov", SAFFRON), ("ac", "AC Unit", "Checked Jun 2", JUNGLE), ("smoke", "Smoke Detectors", "6 Of 6 Working", JUNGLE)]):
        y = 116 + i * 40; o += card(14, y, 212, 34, mode, cardbg) + icon(k, 22, y + 8, 18, "duo", c) + t(48, y + 16, n, 9.5, INK, "khand") + t(48, y + 27, st, 7, MUTE) + dot(214, y + 17, 3.5, c)
    return screen(mwhdr("share", headbg or bg) + o + btn(276 - 8, "Ask Anything", "outline", h=22, size=8), bg, head=False)
GA = "White Base Follow-Ups"
add(GA, "White Base: Card Edges", O("wc_w_border", "White Base: Cards With Thin Borders", "White page, white cards outlined in a thin warm grey line.", ["clear", "system", "crisp"], "system", wc_screen("#FFFFFF", "#FFFFFF", "border")),
    O("wc_w_shadow", "White Base: Cards With A Soft Shadow", "White page, borderless cards lifted by a faint shadow.", ["soft", "modern"], "concierge", wc_screen("#FFFFFF", "#FFFFFF", "shadow")), "On White: Borders Or Shadows?")
add(GA, "White Base: Warm Touch", O("wc_w_creamband", "White Base: One Cream Band Up Top", "White page with a thin cream band behind the greeting only.", ["warm", "balanced"], "neighbor", wc_screen("#FFFFFF", "#FFFFFF", "border", True)),
    O("wc_w_creamcards", "White Base: Cream Cards On White", "White page; the cards themselves are cream.", ["warm", "lively"], "neighbor", wc_screen("#FFFFFF", CREAM, "border")), "On White: Cream Band Or Cream Cards?")
def wc2(status="tag", greet="big", icons="duo"):
    o = ""
    if greet == "big": o += h1(14, 64, "Hi Sarah", 24) + t(14, 80, "Your Home Is In Good Shape", 10, INK, "khand"); y0 = 92
    else: o += lbl(14, 52, "Hi Sarah") + h1(14, 70, "Your Home", 16); y0 = 82
    for i, (k, n, st, c) in enumerate([("furnace", "Furnace", "Checked", JUNGLE), ("water", "Water Heater", "Due Soon", SAFFRON), ("ac", "AC Unit", "Checked", JUNGLE), ("smoke", "Smoke Detectors", "All Working", JUNGLE)]):
        y = y0 + i * 40; o += card(14, y, 212, 34, "border") + (icon(k, 22, y + 8, 18, "duo", c) if icons == "duo" else icon(k, 22, y + 8, 18, "outline", INK)) + t(48, y + 21, n, 10, INK, "khand")
        o += tag(222 - len(st) * 4.4 - 10, y + 12, st, c, solid=False) if status == "tag" else dot(214, y + 17, 3.5, c)
    return screen(mwhdr("byline", "#FFFFFF") + o + btn(268, "Ask Anything", "outline", h=22, size=8), "#FFFFFF", head=False)
add(GA, "White Base: Status Marks", O("wc_w_stat_tag", "Status As Small Colored Tags", "Each system row ends in a word tag: Checked, Due Soon.", ["lively", "readable", "visual"], "neighbor", wc2("tag")),
    O("wc_w_stat_dot", "Status As One Colored Dot", "Each row ends in a small colored dot only.", ["minimal", "quiet"], "system", wc2("dot")), "Tags Or Dots For Status?")
add(GA, "White Base: Greeting Size", O("wc_w_greet_big", "Big Friendly Greeting", "A large 'Hi Sarah' with a plain one-line status.", ["big", "neighbor", "readable"], "neighbor", wc2("tag", "big")),
    O("wc_w_greet_small", "Small Label Greeting", "A small caps 'Hi Sarah' over a short title.", ["compact", "system"], "system", wc2("tag", "small")), "Big Or Small Greeting?")
add(GA, "White Base: Row Icons", O("wc_w_ic_color", "Colored Drawn Icons", "Each system icon tinted in its status color.", ["visual", "lively"], "neighbor", wc2("tag", "big", "duo")),
    O("wc_w_ic_black", "Black Line Icons", "All icons in thin black line.", ["restrained", "system"], "system", wc2("tag", "big", "line")), "Colored Or Black Icons?")
FIRST = len(pairs)
# ---- onboarding photo steps ----
GB = "Onboarding Photo Steps"
def snap(mode="auto", guide="frame", prog="dots", example=False, skip="link"):
    o = (dots(48, 5, 1, JUNGLE) if prog == "dots" else pbar(44, .4, JUNGLE) + t(226, 56, "Step 2 Of 5", 6.5, MUTE, anchor="end")) + h1(14, 74, "Snap The Water Heater Label", 15)
    if example: o += photo(14, 82, 64, 50, "label", 4) + t(84, 98, "Like This:", 8, INK, "hind", 600) + para(84, 110, ["The sticker with model", "and serial numbers."], 7, MUTE, 9); y = 140
    else: y = 84
    o += rect(14, y, 212, 110, "#2B2B2B", r=8) + photo(44, y + 16, 152, 78, "label", 2)
    if guide == "frame": o += "".join(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>' for d in [f"M40 {y+24} V{y+12} H52", f"M188 {y+12} H200 V{y+24}", f"M40 {y+86} V{y+98} H52", f"M188 {y+98} H200 V{y+86}"])
    else: o += rect(20, y + 92, 200, 14, "#0A0A0A", r=3, extra='opacity=".6"') + t(120, y + 102, "Fill The Frame · No Glare · Hold Steady", 6.5, "#FFFFFF", "hind", 600, "middle")
    y += 118
    if mode == "auto" and y < 250: o += rect(14, y, 212, 34, JUNGLE + "14", JUNGLE, 6) + t(22, y + 14, "Rheem XG50T · Serial 0423B11", 8.5, INK, "hind", 600) + link(22, y + 26, "Looks Right", JUNGLE) + link(100, y + 26, "Fix It", TERRA)
    elif y < 250: o += field(y + 8, "Model", "") 
    o += sticky(btn(266, "Take Photo", "fill", INK, h=24, size=8) if skip == "none" else btn(264, "Take Photo", "fill", INK, x=14, w=130, h=24, size=8) + link(186, 280, "Skip For Now" if skip == "link" else "Tech Will Do It", LAGOON, "middle"))
    return scr(o)
add(GB, "Up Keep: Label Photo", O("ob_auto_fill", "Photo Auto-Fills Model And Serial", "After the photo: 'Rheem XG50T' with Looks Right or Fix It.", ["easy", "guided", "fast"], "system", snap("auto")),
    O("ob_type_in", "Photo, Then Type The Model", "Photo is saved; you type the model yourself.", ["simple", "control"], "crew", snap("manual")), "Auto-Fill Or Type It?")
add(GB, "Up Keep: Camera Guide", O("ob_guide_frame", "White Corner Guides On The Camera", "Four corner marks show where the label goes.", ["visual", "clear"], "system", snap("auto", "frame")),
    O("ob_guide_tips", "One Line Of Tips On The Camera", "A dark strip: Fill The Frame, No Glare, Hold Steady.", ["guided", "readable"], "neighbor", snap("auto", "tips")), "Corner Guides Or Tip Line?")
add(GB, "Up Keep: Photo Progress", O("ob_prog_dots", "Progress As Five Dots", "Five step dots across the top.", ["calm", "simple"], "concierge", snap("auto", "frame", "dots")),
    O("ob_prog_bar", "Progress Bar With 'Step 2 Of 5'", "A green bar and the step count.", ["clear", "guided"], "system", snap("auto", "frame", "bar")), "Dots Or Bar With Count?")
add(GB, "Up Keep: Photo Example", O("ob_example_on", "Show An Example Photo First", "A small drawn example of the label above the camera.", ["guided", "easy"], "neighbor", snap("manual", "frame", "bar", True)),
    O("ob_example_off", "Camera Only, Bigger", "No example; the camera box is bigger.", ["big", "fast"], "crew", snap("manual", "frame", "bar", False)), "Show An Example?")
add(GB, "Up Keep: Photo Skip", O("ob_skip_later", "'Skip For Now' Link", "A link to skip and add the photo later.", ["easy", "forgiving"], "neighbor", snap("auto", "tips", "dots", False, "link")),
    O("ob_skip_tech", "'Tech Will Do It' Link", "The skip link says the tech will take it on the first visit.", ["reassuring", "human"], "crew", snap("auto", "tips", "dots", False, "tech")), "How Should Skip Read?")
def photo_list(mode):
    o = h1(14, 56, "Photos Of Your Home", 16) + t(14, 70, "Five quick photos so your tech comes ready.", 7.5, MUTE)
    items = [("Water Heater Label", 1), ("Furnace Label", 1), ("AC Unit", 0), ("Electric Panel", 0), ("Main Water Shutoff", 0)]
    if mode == "list":
        for i, (n, d) in enumerate(items): y = 80 + i * 34; o += ln(y) + (photo(14, y + 4, 34, 26, "label", 3) if d else rect(14, y + 4, 34, 26, "#FFFFFF", "#BDB6AA", 3, extra='stroke-dasharray="3 2"') + icon("cam", 22, y + 8, 18, "outline")) + t(56, y + 21, n, 9, INK, "khand") + (icon("check", 210, y + 10, 14, "duo", JUNGLE) if d else link(226, y + 21, "Add", TERRA, "end"))
    else:
        for i, (n, d) in enumerate(items[:4]): x = 14 + (i % 2) * 108; y = 80 + (i // 2) * 88; o += (photo(x, y, 104, 64, "label", 6) if d else rect(x, y, 104, 64, CREAM, "#BDB6AA", 6, extra='stroke-dasharray="4 3"') + icon("cam", x + 42, y + 20, 22, "outline")) + t(x, y + 76, n, 8, INK, "khand")
    return scr(o + sticky(btn(266, "2 Of 5 Done · Continue", "fill", INK, h=24, size=8)))
add(GB, "Up Keep: Photo Checklist", O("ob_list_rows", "All Photos As A Checklist", "Five rows; done ones show a thumbnail and check.", ["system", "clear"], "system", photo_list("list")),
    O("ob_list_grid", "Photos As Big Empty Frames", "A grid of big dashed frames to fill in.", ["visual", "big", "lively"], "neighbor", photo_list("grid")), "Checklist Or Frame Grid?")
# ---- visit log ----
GC = "Visit Log"
VIS = [("Nov 4", "Fall Visit", "11 Checks · 1 To Watch", SAFFRON), ("Jun 2", "Summer Visit", "9 Checks · All Good", JUNGLE), ("Mar 10", "Spring Visit", "10 Checks · All Good", JUNGLE), ("Dec 1", "Winter Visit", "8 Checks · 1 Fixed", LAGOON)]
def vlog(mode="list", thumbs=False, filt=False, year=False):
    o = h1(14, 56, "Visit Log", 18); y = 66
    if filt: o += "".join(chip(14 + i * 58, y, s, i == 0, INK, 54) for i, s in enumerate(["All", "Visits", "Repairs", "Notes"])); y += 28
    if year: o += lbl(14, y + 8, "2026", TERRA); y += 14
    for d, n, s, c in VIS:
        if mode == "list":
            o += ln(y) + t(14, y + 18, d, 9, INK, "khand") + (photo(52, y + 5, 30, 22, "house", 3) if thumbs else "") + t(90 if thumbs else 56, y + 15, n, 9, INK, "khand") + t(90 if thumbs else 56, y + 26, s, 7, MUTE) + dot(220, y + 16, 3.5, c); y += 34
        else:
            o += dot(24, y + 14, 5, c) + (f'<line x1="24" y1="{y+19}" x2="24" y2="{y+44}" stroke="{LINE}" stroke-width="2"/>') + t(38, y + 12, d.upper(), 6.5, MUTE, "hind", 600) + t(38, y + 24, n, 10, INK, "khand") + t(38, y + 34, s, 7, MUTE) + (photo(178, y + 4, 48, 32, "house", 4) if thumbs else ""); y += 44
    return scr(o)
add(GC, "Up Keep: Visit Log Layout", O("vl_list", "Visit Log As A Plain List", "Date, visit and result on each row.", ["clear", "compact", "system"], "system", vlog("list")),
    O("vl_timeline", "Visit Log As A Timeline", "Colored dots on a vertical line.", ["visual", "guided"], "neighbor", vlog("timeline")), "List Or Timeline?")
add(GC, "Up Keep: Visit Log Photos", O("vl_thumbs_on", "Each Visit Shows A Photo", "A small drawn photo on every visit.", ["visual", "proof"], "neighbor", vlog("timeline", True)),
    O("vl_thumbs_off", "Text Only, Photos Inside", "No thumbnails; photos open with the visit.", ["clean", "fast"], "concierge", vlog("timeline", False)), "Thumbnails Or Text?")
def vdetail(mode):
    o = lbl(14, 50, "Nov 4 · 92 Minutes · Danny") + h1(14, 70, "Fall Visit", 18)
    if mode == "sum":
        o += "".join(rect(14 + i * 72, 80, 68, 50, "#FFFFFF", LINE, 6) + rect(14 + i * 72, 80, 68, 3, c) + t(48 + i * 72, 108, n, 18, INK, "khand", anchor="middle") + t(48 + i * 72, 122, l, 6, MUTE, "hind", 600, "middle") for i, (n, l, c) in enumerate([("11", "DONE", JUNGLE), ("1", "TO WATCH", SAFFRON), ("0", "FIX NOW", TERRA)]))
        o += rows(140, [("Filter Swapped", "Done"), ("Water Heater Flush", "Done"), ("Dryer Vent", "Watch")], 24)
    else:
        o += "".join(ln(80 + i * 26) + icon("check", 14, 85 + i * 26, 14, "duo", c) + t(34, 96 + i * 26, n, 9, INK) for i, (n, c) in enumerate([("Furnace Tune-Up", JUNGLE), ("Filter Swapped", JUNGLE), ("Water Heater Flush", JUNGLE), ("Moisture Scan: Normal", LAGOON), ("Dryer Vent: Watch", SAFFRON), ("Smoke And CO Test", JUNGLE)]))
    return scr(o + btn(262, "Download Proof Pack", "outline", h=24, size=8))
add(GC, "Up Keep: Visit Detail", O("vl_det_sum", "Visit Opens On Three Counts", "Done, To Watch, Fix Now, then the main rows.", ["scannable", "data"], "system", vdetail("sum")),
    O("vl_det_check", "Visit Opens On The Full Checklist", "Every check as a row with a small icon.", ["thorough", "clear"], "crew", vdetail("check")), "Counts Or Full Checklist?")
def vnote(mode):
    o = h1(14, 56, "Add A Note", 17) + t(14, 70, "Your own note on the Nov 4 visit.", 7.5, MUTE)
    if mode == "text": o += rect(14, 80, 212, 90, "#FFFFFF", "#CFC8BC", 0) + t(22, 96, "Basement smelled musty again after rain.", 8, INK)
    else: o += rect(14, 80, 212, 90, CREAM, "none", 8) + dot(120, 116, 18, TERRA) + rect(116, 106, 8, 14, "#FFFFFF", r=4) + t(120, 154, "Hold To Talk", 9, INK, "khand", anchor="middle")
    return scr(o + lbl(14, 190, "Tag It") + "".join(chip(14 + i * 70, 196, s, i == 1, LAGOON, 66) for i, s in enumerate(["Question", "Watch", "Done"])) + btn(262, "Save Note", "fill", INK, h=24, size=8))
add(GC, "Up Keep: Member Note", O("vl_note_type", "Type A Note", "A plain text box.", ["simple", "clear"], "system", vnote("text")),
    O("vl_note_voice", "Hold To Talk A Note", "A big terracotta mic button; it writes it down.", ["easy", "big", "lively"], "neighbor", vnote("voice")), "Type Or Talk?")
# ---- Home Record ----
GD = "Home Record"
EQ = [("furnace", "Furnace", "Carrier 59SC5 · 2014", JUNGLE), ("water", "Water Heater", "Rheem XG50T · 2019", SAFFRON), ("ac", "AC Unit", "Trane XR14 · 2016", JUNGLE), ("smoke", "Smoke Detectors", "6 Units · 2022", JUNGLE)]
def hrec(mode="list", tabs=False):
    o = lbl(14, 50, "1418 Maple Ave") + h1(14, 70, "Home Record", 18); y = 80
    if tabs: o += "".join(t(14 + i * 56, y + 10, s, 8.5, INK if i == 0 else MUTE, "hind", 600) + (rect(14 + i * 56, y + 15, 40, 2, TERRA) if i == 0 else "") for i, s in enumerate(["Equipment", "Readings", "Photos", "Files"])) + ln(y + 18, 0, W); y += 26
    for i, (k, n, s, c) in enumerate(EQ):
        if mode == "list": o += ln(y) + icon(k, 14, y + 8, 18, "duo", c) + t(40, y + 16, n, 9.5, INK, "khand") + t(40, y + 27, s, 7, MUTE) + t(226, y + 20, "›", 12, MUTE, anchor="end"); y += 36
        else: x = 14 + (i % 2) * 108; yy = y + (i // 2) * 76; o += rect(x, yy, 104, 70, "#FFFFFF", LINE, 8) + photo(x + 6, yy + 6, 92, 34, "label", 4) + t(x + 8, yy + 52, n, 9, INK, "khand") + t(x + 8, yy + 63, s.split(" · ")[1], 6.5, MUTE)
    return scr(o + btn(262, "Download Proof Pack", "outline", h=24, size=8))
add(GD, "Up Keep: Home Record Layout", O("hr_list", "Equipment As Icon Rows", "One row per system with model and year.", ["system", "compact"], "system", hrec("list")),
    O("hr_cards", "Equipment As Photo Cards", "Two-across cards with the label photo.", ["visual", "proof"], "neighbor", hrec("cards")), "Rows Or Photo Cards?")
add(GD, "Up Keep: Home Record Sections", O("hr_tabs", "Tabs: Equipment, Readings, Photos, Files", "Four tabs under the title.", ["organized", "system"], "system", hrec("list", True)),
    O("hr_onepage", "One Long Page, No Tabs", "Everything on one scroll.", ["simple", "easy"], "neighbor", hrec("list", False)), "Tabs Or One Page?")
def readings(mode):
    o = lbl(14, 50, "Water Heater · Rheem XG50T") + h1(14, 70, "Readings", 18)
    R = [("Nov 4", "Normal", JUNGLE), ("Jun 2", "Normal", JUNGLE), ("Mar 10", "A Bit High", SAFFRON), ("Dec 1", "Normal", JUNGLE)]
    if mode == "table": o += rows(80, [(f"{d}", s) for d, s, c in R], 26) + "".join(dot(160, 95 + i * 26, 3.5, c) for i, (_, _, c) in enumerate(R))
    else: o += "".join(rect(14 + i * 54, 84, 48, 60, c + "14", c, 6) + t(38 + i * 54, 108, s.split()[0] if s == "Normal" else "High", 9, c, "khand", anchor="middle") + t(38 + i * 54, 134, d, 7, MUTE, "hind", 600, "middle") for i, (d, s, c) in enumerate(reversed(R)))
    return scr(o + lbl(14, 200, "Moisture Scan") + t(14, 216, "Normal at every visit this year.", 8.5, INK) + btn(262, "See All Readings", "outline", h=24, size=8))
add(GD, "Up Keep: Readings", O("hr_read_table", "Readings As A Plain Table", "Date and result rows with a color dot.", ["clear", "system"], "system", readings("table")),
    O("hr_read_tiles", "Readings As Color Tiles", "One tinted tile per visit, oldest to newest.", ["visual", "lively"], "neighbor", readings("tiles")), "Table Or Tiles?")
def recall(mode):
    o = h1(14, 56, "Recall Check", 17) + t(14, 70, "We check your equipment against recall lists.", 7.5, MUTE)
    if mode == "clear": o += rect(14, 82, 212, 70, JUNGLE + "12", JUNGLE, 8) + icon("check", 26, 98, 24, "duo", JUNGLE) + t(60, 112, "No Recalls Found", 13, INK, "khand") + t(60, 126, "4 items checked Oct 12", 7.5, MUTE)
    else: o += "".join(ln(82 + i * 30) + icon(k, 14, 88 + i * 30, 18, "outline") + t(40, 101 + i * 30, n, 9, INK, "khand") + tag(176, 92 + i * 30, "No Recall", JUNGLE) for i, (k, n, _, _) in enumerate(EQ))
    return scr(o + t(14, 236, "Last checked Oct 12, 2026", 7, MUTE) + btn(262, "Check Again", "outline", h=24, size=8))
add(GD, "Up Keep: Recall Check", O("hr_recall_one", "One Big 'No Recalls Found' Box", "A single green all-clear box.", ["reassuring", "big", "easy"], "neighbor", recall("clear")),
    O("hr_recall_rows", "Recall Status Per Item", "Each item with its own No Recall tag.", ["thorough", "system"], "system", recall("rows")), "One All-Clear Or Per Item?")
def handoff(mode):
    o = h1(14, 56, "Selling Your Home?", 17) + para(14, 72, ["Hand your Home Record to the buyer:", "every visit, photo and reading."], 8, MUTE, 11)
    if mode == "steps": o += "".join(dot(28, 112 + i * 36, 10, c) + t(28, 116 + i * 36, str(i + 1), 9, "#FFFFFF", "khand", anchor="middle") + t(46, 116 + i * 36, s, 10, INK, "khand") for i, (s, c) in enumerate([("Enter The Buyer's Email", JUNGLE), ("We Send The Record", LAGOON), ("They Can Keep The Plan", TERRA)]))
    else: o += rect(30, 100, 180, 110, "#FFFFFF", INK, 6, 1.5) + roof_logo(80, 122, 1) + t(120, 146, "Home Record", 15, INK, "khand", anchor="middle") + t(120, 160, "1418 Maple Ave · 4 Years", 7.5, MUTE, anchor="middle") + t(120, 182, "16 Visits · 212 Photos · 48 Readings", 7.5, INK, "hind", 600, "middle")
    return scr(o + btn(262, "Send To Buyer", "fill", INK, h=24, size=8))
add(GD, "Up Keep: Home Record Handoff", O("hr_hand_steps", "Handoff As Three Steps", "Numbered steps for sending the record.", ["guided", "clear"], "system", handoff("steps")),
    O("hr_hand_cover", "Handoff As A Record Cover", "A cover card with the totals, like a certificate.", ["proud", "premium"], "concierge", handoff("cover")), "Steps Or Cover Card?")
def proof(mode):
    o = h1(14, 56, "Proof Pack", 17) + t(14, 70, "A visit record for warranty claims.", 7.5, MUTE)
    if mode == "doc": o += rect(44, 82, 152, 160, "#FFFFFF", "#BDB6AA", 2) + roof_logo(56, 102, .8) + "".join(rect(56, 116 + i * 12, [120, 90, 110, 70, 100, 80, 115][i], 4, "#D6D0C6") for i in range(7)) + photo(56, 204, 60, 30, "label", 2) + photo(122, 204, 60, 30, "tech", 2)
    else: o += rows(80, [("Visit Dates", "16"), ("Photos", "212"), ("Readings", "48"), ("Tech Licenses", "2")], 26) + t(14, 200, "PDF · 4.2 MB", 7.5, MUTE)
    return scr(o + btn(262, "Download PDF", "fill", INK, h=24, size=8))
add(GD, "Up Keep: Proof Pack", O("hr_proof_doc", "Proof Pack Shown As The Document", "A drawn page preview of the PDF.", ["visual", "proof"], "crew", proof("doc")),
    O("hr_proof_list", "Proof Pack As What's Inside", "Rows listing what the PDF contains.", ["clear", "system"], "system", proof("list")), "Page Preview Or Contents List?")
# ---- Ask Anything thread ----
GE = "Ask Anything Thread"
def thread(me=LAGOON, them="#F1EEE9", avatar=True, photo_on=True, quick=False, bg="#FFFFFF"):
    o = lbl(14, 50, "Ask Anything") + t(14, 64, "Danny usually replies within an hour.", 7, MUTE)
    y = 76
    def bub(y, lines, mine):
        w = max(len(l) for l in lines) * 4.1 + 18; h = 10 + len(lines) * 10; x = 226 - w if mine else (36 if avatar else 14)
        return rect(x, y, w, h, me if mine else them, r=10) + "".join(t(x + 9, y + 14 + i * 10, l, 7.6, "#FFFFFF" if mine else INK) for i, l in enumerate(lines)), h
    s, h = bub(y, ["There's a drip under the water", "heater. Should I worry?"], True); o += s; y += h + 8
    if photo_on: o += photo(130, y, 96, 60, "label", 8); y += 68
    s, h = bub(y, ["Thanks for the photo. That's the", "relief valve; it's normal after a", "flush. I'll check it Nov 4."], False); o += s + (techface(22, y + 12, 7) if avatar else ""); y += h + 8
    if quick: o += "".join(chip(14 + i * 72, 228, q, False, LAGOON, 68) for i, q in enumerate(["Book A Visit", "Send Photo", "Call Danny"]))
    return screen(mwhdr("call", bg) + o + rect(14, 262, 180, 26, "#FFFFFF", "#CFC8BC", 13) + t(26, 278, "Ask Anything", 8, "#A3A3A3") + dot(212, 275, 12, INK) + f'<path d="M207 275 H217 M213 271 L217 275 L213 279" stroke="#FFFFFF" stroke-width="1.6" fill="none"/>', bg, head=False)
add(GE, "Up Keep: Thread Bubbles", O("aa_me_lagoon", "My Bubbles In Lagoon", "Your messages in lagoon, tech in light grey.", ["calm", "info", "clear"], "system", thread(LAGOON)),
    O("aa_me_ink", "My Bubbles In Black", "Your messages in black, tech in light grey.", ["bold", "restrained"], "crew", thread(INK)), "Lagoon Or Black Bubbles?")
add(GE, "Up Keep: Thread Face", O("aa_avatar_on", "Tech Face Beside Replies", "A small drawn face next to Danny's replies.", ["human", "warm"], "neighbor", thread(LAGOON, avatar=True)),
    O("aa_avatar_off", "No Faces, Just Bubbles", "Cleaner thread with no avatars.", ["clean", "simple"], "concierge", thread(LAGOON, avatar=False)), "Show The Tech's Face?")
add(GE, "Up Keep: Thread Shortcuts", O("aa_quick_on", "Shortcut Chips Above The Box", "Book A Visit, Send Photo, Call Danny.", ["guided", "easy"], "system", thread(LAGOON, quick=True)),
    O("aa_quick_off", "Just The Text Box", "No shortcuts; type anything.", ["simple", "open"], "concierge", thread(LAGOON, quick=False)), "Add Shortcut Chips?")
def ask_empty(mode):
    o = h1(14, 58, "Ask Anything", 20) + t(14, 74, "About your home. A real tech answers.", 8, MUTE)
    if mode == "examples": o += "".join(rect(14, 88 + i * 34, 212, 28, LAGOON + "1F", r=10) + t(24, 106 + i * 34, q, 8.5, LAGOON, "hind", 600) for i, q in enumerate(["Is This Noise Normal?", "Which Filter Size Do I Buy?", "Can You Look At This Leak?", "When Is My Next Visit?"]))
    else: o += dot(120, 140, 40, CREAM) + techface(120, 132, 16) + t(120, 200, "Danny Ruiz, Your Tech", 11, INK, "khand", anchor="middle") + t(120, 214, "Licensed · Replies Within An Hour", 7.5, MUTE, anchor="middle")
    return scr(o + rect(14, 262, 212, 26, "#FFFFFF", "#CFC8BC", 13) + t(26, 278, "Type Or Send A Photo", 8, "#A3A3A3"))
add(GE, "Up Keep: Thread Start", O("aa_start_examples", "Start With Example Questions", "Four tappable sample questions.", ["guided", "easy"], "system", ask_empty("examples")),
    O("aa_start_tech", "Start With Your Tech's Face", "A big drawn portrait of who will answer.", ["human", "trust", "big"], "neighbor", ask_empty("tech")), "Examples Or Tech Face?")
# ---- reminder notifications ----
GF = "Reminder Notifications"
def remind(style="plain", act="buttons", when="day"):
    title = "Visit Tomorrow, 9 AM" if when == "day" else "Visit In 1 Hour"
    body = ["Danny is coming for your fall visit.", "Clear a path to the furnace."]
    if style == "plain": o = notif(90, title, body)
    else: o = notif(90, title, body, accent=TERRA, extra=dot(208, 108, 10, TERRA + "26") + icon("furnace", 200, 100, 16, "duo", TERRA))
    if act == "buttons": o += rect(14, 172, 104, 24, "#FFFFFF", r=8) + t(66, 188, "Confirm", 8.5, JUNGLE, "hind", 600, "middle") + rect(122, 172, 104, 24, "#FFFFFF", r=8) + t(174, 188, "Reschedule", 8.5, LAGOON, "hind", 600, "middle")
    return phone_frame(o)
add(GF, "Up Keep: Reminder Look", O("rm_plain", "Plain Text Reminder", "Standard notification, title and two lines.", ["clear", "simple"], "system", remind("plain")),
    O("rm_icon", "Reminder With A Small Drawn Icon", "Same notification with a terracotta furnace icon.", ["visual", "lively"], "neighbor", remind("icon")), "Plain Or With Icon?")
add(GF, "Up Keep: Reminder Actions", O("rm_act_on", "Confirm And Reschedule Buttons", "Two buttons right on the notification.", ["easy", "fast", "guided"], "system", remind("icon", "buttons")),
    O("rm_act_off", "Tap To Open The App", "No buttons; tapping opens the visit.", ["simple", "clean"], "concierge", remind("icon", "none")), "Buttons Or Just Tap?")
add(GF, "Up Keep: Reminder Timing", O("rm_day", "Remind The Day Before", "One reminder the day before.", ["calm", "planned"], "concierge", remind("plain", "buttons", "day")),
    O("rm_hour", "Remind One Hour Before", "One reminder an hour before arrival.", ["timely", "direct"], "crew", remind("plain", "buttons", "hour")), "Day Before Or Hour Before?")
def filt_rem(mode):
    if mode == "push": return phone_frame(notif(90, "Time To Change Your Filter", ["Size 16x25x1. Tap to see how,", "or add it to your next visit."], accent=SAFFRON))
    return sms([["Smart Upkeep: Time to change your", "furnace filter (16x25x1). Reply", "ADD to have Danny bring one Nov 4."], ["ADD"]], "Smart Upkeep")
add(GF, "Up Keep: DIY Reminder Channel", O("rm_push", "Filter Reminder As An App Alert", "A push alert with the filter size.", ["system", "quiet"], "system", filt_rem("push")),
    O("rm_text", "Filter Reminder As A Text", "A text you can answer with ADD.", ["easy", "human"], "neighbor", filt_rem("sms")), "App Alert Or Text?")
def cal(mode):
    o = h1(14, 56, "You're All Set", 18) + t(14, 72, "Four visits booked for the year.", 8, MUTE)
    S = [("Mar 10", "Spring", JUNGLE), ("Jun 2", "Summer", SAFFRON), ("Sep 8", "Fall", TERRA), ("Dec 1", "Winter", LAGOON)]
    if mode == "button": o += rows(82, [(f"{s} Visit", d) for d, s, c in S], 26) + btn(196, "Add My Visits To Calendar", "fill", INK, h=26, size=8)
    else: o += "".join(rect(14 + (i % 2) * 108, 84 + (i // 2) * 64, 104, 58, "#FFFFFF", LINE, 6) + rect(14 + (i % 2) * 108, 84 + (i // 2) * 64, 104, 14, c, r=0) + t(66 + (i % 2) * 108, 94 + (i // 2) * 64, s.upper(), 6.5, "#FFFFFF", "hind", 600, "middle") + t(66 + (i % 2) * 108, 124 + (i // 2) * 64, d, 15, INK, "khand", anchor="middle") for i, (d, s, c) in enumerate(S)) + link(14, 228, "Add All To Calendar", LAGOON)
    return scr(o)
add(GF, "Up Keep: Add To Calendar", O("rm_cal_btn", "Big 'Add My Visits To Calendar' Button", "A list of four dates and one big button.", ["guided", "big"], "system", cal("button")),
    O("rm_cal_tiles", "Four Calendar Tiles And A Link", "Color-topped date tiles with a small link.", ["visual", "lively"], "neighbor", cal("tiles")), "Big Button Or Calendar Tiles?")
def cancel_note(mode):
    o = h1(14, 56, "Cancel Anytime", 18)
    if mode == "plain": o += para(14, 76, ["Give us 3 days' notice before your next", "billing date and you won't be charged."], 8.5, INK, 12) + btn(130, "Cancel My Membership", "outline", TERRA, h=26, size=8)
    else: o += "".join(dot(28, 92 + i * 34, 9, c) + t(28, 95.5 + i * 34, str(i + 1), 8, "#FFFFFF", "khand", anchor="middle") + t(44, 96 + i * 34, s, 9.5, INK, "khand") for i, (s, c) in enumerate([("Tap Cancel 3 Days Before Billing", INK), ("We Confirm By Email", INK), ("Your Home Record Stays Yours", JUNGLE)])) + btn(200, "Cancel My Membership", "outline", TERRA, h=26, size=8)
    return scr(o)
# ---- tech app ----
GG = "Tech App"
def tday(mode="list", map_on=False):
    o = lbl(14, 50, "Tue, Nov 4 · Danny") + h1(14, 70, "Today: 4 Visits", 18); y = 80
    if map_on: o += rect(14, y, 212, 70, "#E8E4DC", r=6) + f'<path d="M30 {y+50} L80 {y+20} L140 {y+44} L200 {y+16}" fill="none" stroke="{LAGOON}" stroke-width="2"/>' + "".join(dot(x, yy, 5, c) for x, yy, c in [(30, y + 50, JUNGLE), (80, y + 20, TERRA), (140, y + 44, INK), (200, y + 16, INK)]); y += 78
    for i, (tm, a, s, c) in enumerate([("8:00", "1418 Maple Ave", "Done", JUNGLE), ("10:30", "22 Elm St", "Next", TERRA), ("1:00", "905 Oak Ct", "", MUTE), ("3:30", "71 Birch Rd", "", MUTE)][: 3 if map_on else 4]):
        o += ln(y) + t(14, y + 18, tm, 10, INK, "khand") + t(54, y + 15, a, 9, INK, "khand") + t(54, y + 26, "Fall Visit · 90 Min", 7, MUTE) + (tag(186, y + 10, s, c, s == "Next") if s else ""); y += 34
    return scr(o + btn(262, "Start Next Visit", "fill", TERRA, h=24, size=8), head="share")
add(GG, "Tech App: Day View", O("ta_day_list", "Day As A Stop List", "Times and addresses, the next one tagged.", ["clear", "system", "compact"], "crew", tday("list")),
    O("ta_day_map", "Day With A Route Map On Top", "A small drawn route map above the stops.", ["visual", "guided"], "system", tday("list", True)), "List Or Map On Top?")
def tcheck(mode):
    o = lbl(14, 50, "22 Elm St · Step 4 Of 11") + pbar(56, 4 / 11, JUNGLE) + h1(14, 82, "Water Heater Flush", 16)
    if mode == "one": o += photo(14, 92, 212, 100, "label", 6) + chip(14, 202, "Done", True, JUNGLE, 66) + chip(86, 202, "Watch", False, INK, 66) + chip(158, 202, "Fix Now", False, INK, 68) + icon("cam", 14, 232, 18, "outline") + t(38, 245, "Add Photo", 8.5, INK, "hind", 600)
    else: o += "".join(ln(92 + i * 26) + check_box(14, 99 + i * 26, i < 2) + t(32, 109 + i * 26, s, 8.5, INK) + icon("cam", 208, 97 + i * 26, 14, "outline") for i, s in enumerate(["Shut Off Gas And Water", "Drain Tank", "Check Relief Valve", "Refill And Relight", "Moisture Scan Around Base", "Photo Of Label"]))
    return scr(o + btn(262, "Next Step", "fill", INK, h=24, size=8))
add(GG, "Tech App: Checklist", O("ta_chk_one", "One Step Per Screen", "Big photo and Done / Watch / Fix Now.", ["big", "guided", "focused"], "crew", tcheck("one")),
    O("ta_chk_list", "All Steps In One List", "Checkboxes with a camera on each row.", ["fast", "system"], "system", tcheck("list")), "One Step Or Full List?")
def tarrive(mode):
    o = h1(14, 56, "Arriving At 22 Elm St", 15)
    if mode == "auto": o += rect(14, 66, 212, 60, LAGOON + "14", LAGOON, 6) + t(22, 86, "Member Gets: 'Danny Is 5 Minutes Away'", 8, INK, "hind", 600) + t(22, 100, "Sent automatically with your photo", 7, MUTE) + toggle(196, 104, True, LAGOON)
    else: o += btn(70, "Text: I'm On My Way", "fill", LAGOON, h=30, size=9) + btn(108, "Text: I'm Here", "outline", LAGOON, h=30, size=9)
    return scr(o + lbl(14, 160, "Member Notes") + para(14, 174, ["Dog in back yard. Use side door.", "Ask about basement smell."], 8.5, INK, 12) + btn(262, "Start Visit", "fill", TERRA, h=24, size=8))
add(GG, "Tech App: Arrival Text", O("ta_arr_auto", "Arrival Text Goes Out On Its Own", "An auto 5-minutes-away text, with a switch.", ["easy", "system"], "system", tarrive("auto")),
    O("ta_arr_tap", "Tech Taps To Send Arrival Text", "Two big buttons: On My Way, I'm Here.", ["human", "control"], "crew", tarrive("tap")), "Automatic Or Tap To Send?")
def tbrand(mode):
    bg, acc = (("#FFFFFF", LAGOON) if mode == "white" else (CREAM, TERRA))
    o = lbl(14, 50, "Tue, Nov 4 · Danny") + h1(14, 70, "Today: 4 Visits", 18) + rect(14, 77, 34, 3, acc)
    for i, (tm, a, st) in enumerate([("8:00", "1418 Maple Ave", "Done"), ("10:30", "22 Elm St", "Next"), ("1:00", "905 Oak Ct", ""), ("3:30", "71 Birch Rd", "")]):
        y = 88 + i * 40; o += rect(14, y, 212, 34, "#FFFFFF", LINE, 6) + t(22, y + 21, tm, 10, INK, "khand") + t(62, y + 15, a, 9, INK, "khand") + t(62, y + 26, "Fall Visit · 90 Min", 7, MUTE) + (tag(180, y + 11, st, acc if st == "Next" else JUNGLE, st == "Next") if st else "")
    return scr(o + btn(262, "Start Next Visit", "fill", acc, h=24, size=8), bg)
def tfinish(mode):
    o = h1(14, 56, "Finish Visit", 18) + rows(66, [("Checks Done", "11"), ("To Watch", "1"), ("Photos", "14")], 24)
    if mode == "sign": o += lbl(14, 150, "Member Sign-Off") + rect(14, 156, 212, 60, "#FFFFFF", "#CFC8BC") + f'<path d="M30 196 q20 -26 40 -4 t40 -6 t40 2" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    else: o += lbl(14, 150, "Note To Member") + rect(14, 156, 212, 60, CREAM, "none", 6) + para(22, 172, ["All good, Sarah. Dryer vent is", "getting lint-heavy; clean in spring."], 8, INK, 11)
    return scr(o + btn(262, "Send Report", "fill", JUNGLE, h=24, size=8))
add(GG, "Tech App: Finish", O("ta_fin_sign", "Finish With A Member Signature", "Member signs on the tech's phone.", ["formal", "proof"], "crew", tfinish("sign")),
    O("ta_fin_note", "Finish With A Short Tech Note", "Tech types a two-line note instead.", ["human", "warm", "fast"], "neighbor", tfinish("note")), "Signature Or Note?")
def tparts(mode):
    o = h1(14, 56, "Van Parts For Today", 16)
    P = [("Filter 16x25x1", 3, JUNGLE), ("Smoke Battery 9V", 6, JUNGLE), ("Relief Valve", 0, TERRA), ("Dryer Vent Brush", 1, JUNGLE)]
    if mode == "list": o += "".join(ln(66 + i * 28) + t(14, 84 + i * 28, n, 9, INK) + t(200, 84 + i * 28, str(q), 10, c, "khand", anchor="end") + (tag(204, 76 + i * 28, "Out", TERRA, True) if q == 0 else "") for i, (n, q, c) in enumerate(P))
    else: o += "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 70, 104, 64, c + "12", c, 6) + t(66 + (i % 2) * 108, 100 + (i // 2) * 70, str(q), 22, c, "khand", anchor="middle") + t(66 + (i % 2) * 108, 120 + (i // 2) * 70, n, 7, INK, "hind", 600, "middle") for i, (n, q, c) in enumerate(P))
    return scr(o + btn(262, "Order Missing Parts", "outline", h=24, size=8))
# ---- email & receipt ----
GH = "Email & Receipt"
def mail(kind="report", head="logo", hero="none", btnc=INK, bg="#FFFFFF"):
    o = rect(0, 0, W, 34, "#F7F7F7") + t(14, 15, "From: Smart Upkeep", 7, INK, "hind", 600) + t(14, 26, "Your Fall Visit Report" if kind == "report" else "Receipt: November Membership", 7, MUTE) + ln(34, 0, W)
    o += rect(14, 42, 212, 250, bg, LINE, 0)
    y = 48
    if head == "logo": o += roof_logo(84, y + 18, 1) + ln(y + 28, 24, 216); y += 36
    elif head == "bar": o += rect(14, y - 6, 212, 30, INK) + roof_logo(26, y + 13, .9, "#FFFFFF", "#BDBDBD"); y += 32
    else: o += roof_logo(24, y + 16, .9) + t(216, y + 14, "BY MAX WEBERMAN", 5.2, MUTE, "khand", "end", 'letter-spacing="1.4"') + ln(y + 24, 24, 216); y += 32
    if hero == "photo": o += photo(24, y, 192, 60, "house", 4); y += 66
    elif hero == "icon": o += dot(120, y + 22, 20, JUNGLE + "1F") + icon("check", 108, y + 10, 24, "duo", JUNGLE); y += 50
    if kind == "report":
        o += h1(24, y + 16, "Your Fall Visit Is Done", 14) + para(24, y + 30, ["Hi Sarah, Danny finished 11 checks.", "One thing to watch: the dryer vent."], 7.6, INK, 10); y += 56
    else:
        o += h1(24, y + 16, "Thanks, Sarah", 14) + rows(y + 22, [("Membership, November", "$99.00"), ("Gutter Cleaning", "Included"), ("Paid · Visa 4242", "$99.00")], 18).replace('x1="14"', 'x1="24"').replace('x2="226"', 'x2="216"').replace('x="226"', 'x="216"').replace('x="14"', 'x="24"'); y += 80
    o += btn(y, "See The Report" if kind == "report" else "View Receipt", "fill", btnc, x=24, w=192, h=22, size=7.5)
    o += t(120, 284, "Cancel Anytime · smartupkeep.com", 6, MUTE, anchor="middle")
    return screen(o, "#F7F7F7" if bg == "#FFFFFF" else "#EFEAE2", head=False)
add(GH, "Email: Top Image", O("em_hero_photo", "Visit Email Opens With A Drawn House", "An illustrated house picture up top.", ["warm", "visual"], "neighbor", mail("report", "logo", "photo")),
    O("em_hero_check", "Visit Email Opens With A Green Check", "A big drawn check instead of a picture.", ["clear", "simple"], "system", mail("report", "logo", "icon")), "House Picture Or Check?")
add(GH, "Email: Button Color", O("em_btn_ink", "Email Button In Black", "Square black button.", ["system", "restrained"], "system", mail("report", "byline", "icon", INK)),
    O("em_btn_terra", "Email Button In Terracotta", "Square terracotta button.", ["warm", "lively"], "neighbor", mail("report", "byline", "icon", TERRA)), "Black Or Terracotta Button?")
def rcpt_doc(mode):
    o = roof_logo(14, 24, 1) + t(226, 22, "RECEIPT", 7, MUTE, "hind", 600, "end", 'letter-spacing="1.4"') + ln(32, 0, W) + h1(14, 58, "November 2026", 16) + t(14, 72, "1418 Maple Ave · Paid Nov 1", 7.5, MUTE)
    if mode == "big": o += t(14, 118, "$99.00", 34, INK, "khand") + tag(130, 104, "Paid", JUNGLE, True) + rows(130, [("Membership", "$99.00"), ("Gutter Cleaning", "Included")], 24)
    else: o += rows(84, [("Membership", "$99.00"), ("Gutter Cleaning", "Included"), ("Tax", "$0.00")], 22) + f'<line x1="14" y1="156" x2="226" y2="156" stroke="{INK}" stroke-width="1.5"/>' + t(14, 174, "Total Paid", 10, INK, "khand") + t(226, 174, "$99.00", 12, INK, "khand", anchor="end")
    return screen(o + t(14, 232, "Cancel Anytime.", 7.5, MUTE) + btn(262, "Download PDF", "outline", h=24, size=8), head=False)
add(GH, "Receipt: Layout", O("em_rdoc_big", "Receipt Leads With A Big Total", "Large $99.00 and a green Paid tag first.", ["big", "readable"], "crew", rcpt_doc("big")),
    O("em_rdoc_ledger", "Receipt As A Classic Ledger", "Line items, a rule, then Total Paid.", ["system", "familiar"], "system", rcpt_doc("ledger")), "Big Total Or Ledger?")
def failcard(mode):
    o = h1(14, 56, "Your Card Didn't Go Through", 15)
    if mode == "calm": o += para(14, 74, ["No problem. Your visits stay booked.", "Update your card by Nov 8."], 8.5, INK, 12) + btn(110, "Update Card", "fill", INK, h=26, size=8.5)
    else: o += rect(14, 66, 212, 40, SAFFRON + "1F", SAFFRON, 6) + warn(22, 76, SAFFRON, .8) + t(46, 85, "Payment Needed By Nov 8", 9.5, INK, "khand") + t(46, 97, "Visits pause after that date.", 7, MUTE) + btn(118, "Update Card", "fill", TERRA, h=26, size=8.5)
    return scr(o + link(14, 170, "Text Danny Instead", LAGOON))
add(GH, "Email: Failed Card", O("em_fail_calm", "Failed Card: Calm, Visits Stay Booked", "Plain reassuring text and a black button.", ["calm", "reassuring"], "neighbor", failcard("calm")),
    O("em_fail_alert", "Failed Card: Saffron Alert Box", "A saffron box with the deadline and terracotta button.", ["clear", "urgent"], "system", failcard("alert")), "Calm Or Alert?")
# ---- funnel open decisions ----
GI = "Sign-Up Funnel Decisions"
def zipwait(mode):
    o = dots(48, 6, 0, JUNGLE) + h1(14, 74, "What's Your ZIP?", 18) + field(84, "ZIP Code", "49503")
    if mode == "wait": o += rect(14, 120, 212, 92, CREAM, "none", 8) + t(22, 140, "Not In Your Area Yet", 12, INK, "khand") + t(22, 154, "Want a heads-up when we are?", 8, MUTE) + field(162, "Email", "sarah@email.com", 22, 196) + btn(220, "Tell Me When", "fill", INK, h=24, size=8)
    else: o += rect(14, 120, 212, 40, SAFFRON + "1F", SAFFRON, 6) + t(22, 138, "We Serve Metro Detroit For Now", 9, INK, "khand") + t(22, 150, "You can still look around.", 7, MUTE) + btn(230, "Continue Anyway", "outline", h=24, size=8)
    return scr(o)
add(GI, "Funnel: Out-Of-Area ZIP", O("fn_zip_wait", "Out Of Area: Join The Waitlist", "An email box: 'Tell Me When'.", ["helpful", "guided"], "neighbor", zipwait("wait")),
    O("fn_zip_note", "Out Of Area: Note, Keep Going", "A saffron note and Continue Anyway.", ["open", "simple"], "system", zipwait("note")), "Waitlist Or Keep Going?")
def vidhero(mode):
    if mode == "modal": return screen(home("one") + rect(0, 0, W, H, INK, extra='opacity=".55"') + rect(14, 90, 212, 120, "#1F1F1F", r=8) + dot(120, 150, 18, "#FFFFFF") + f'<path d="M115 141 L129 150 L115 159 Z" fill="{INK}"/>' + t(120, 196, "Watch The 60s Video", 9, "#FFFFFF", "khand", anchor="middle"), head=False)
    return scr(home("one").replace("Get Started", "Get Started") + rect(14, 160, 0, 0) + "", head="share").replace("</g><rect x=\".5\"", rect(10, 244, 220, 40, "#FFFFFF") + rect(14, 246, 212, 34, "#FFFFFF", LINE, 6) + rect(18, 250, 46, 26, "#1F1F1F", r=4) + dot(41, 263, 7, "#FFFFFF") + f'<path d="M39 259 L45 263 L39 267 Z" fill="{INK}"/>' + t(72, 260, "Watch The 60s Video", 9, INK, "khand") + t(72, 271, "Plays only if you tap", 6.8, MUTE) + "</g><rect x=\".5\"", 1)
add(GI, "Funnel: Explainer Video", O("fn_vid_poster", "Small Video Poster In The Hero", "A small 'Watch 60s Video' thumbnail; nothing pops up.", ["calm", "easy"], "system", vidhero("poster")),
    O("fn_vid_modal", "Video Opens Over The Page", "The video pops up over the home page on arrival.", ["bold", "story"], "crew", vidhero("modal")), "Small Poster Or Pop-Up Video?")
def trust(mode):
    o = h1(14, 56, "Why Neighbors Trust Us", 15)
    if mode == "facts": o += "".join(ln(66 + i * 34) + shield(14, 72 + i * 34, c, .8, False) + t(40, 84 + i * 34, a, 9.5, INK, "khand") + t(40, 95 + i * 34, b, 7, MUTE) for i, (a, b, c) in enumerate([("Michigan Licensed", "Tap To Verify License", LAGOON), ("Insured", "$2M General Liability", JUNGLE), ("Background Checked", "Re-Checked Every Year", TERRA), ("How We Vet", "Required Certs For Every Tech", SAFFRON)]))
    else: o += "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 76, 104, 70, c + "12", c, 8) + shield(54 + (i % 2) * 108, 74 + (i // 2) * 76, c, 1, True) + t(66 + (i % 2) * 108, 120 + (i // 2) * 76, a, 9, INK, "khand", anchor="middle") for i, (a, c) in enumerate([("Licensed", LAGOON), ("Insured", JUNGLE), ("Background Checked", TERRA), ("Vetted", SAFFRON)]))
    return scr(o + btn(262, "Tap To Verify License", "fill", LAGOON, h=24, size=8))
add(GI, "Funnel: Trust Signals", O("fn_trust_facts", "Trust As Fact Rows With Details", "License number, insurer amount, yearly re-check.", ["thorough", "trust", "clear"], "system", trust("facts")),
    O("fn_trust_tiles", "Trust As Four Shield Tiles", "Four colored tiles, one word each.", ["visual", "lively", "big"], "neighbor", trust("tiles")), "Detailed Rows Or Shield Tiles?")
def pay(mode):
    o = dots(48, 6, 5, JUNGLE) + h1(14, 74, "Start Your Membership", 16) + t(14, 90, PRICE, 10, INK, "khand")
    if mode == "later": o += rect(14, 102, 212, 70, JUNGLE + "12", JUNGLE, 8) + t(22, 122, "Reserve Your Spot Today", 11, INK, "khand") + para(22, 136, ["Pay after your first visit.", "Card saved, not charged yet."], 7.8, MUTE, 11) + btn(190, "Reserve My Spot", "fill", JUNGLE, h=26, size=8.5)
    else: o += field(106, "Card Number", "4242 4242 4242 4242") + field(140, "Expires", "08 / 29", 14, 100) + field(140, "CVC", "123", 126, 100) + btn(190, "Pay $99 And Start", "fill", INK, h=26, size=8.5)
    return scr(o + icon("check", 84, 228, 10, "duo", JUNGLE) + t(98, 236, "Cancel Anytime", 7.5, INK, "hind", 600))
add(GI, "Funnel: Payment Step", O("fn_pay_later", "Reserve Now, Pay After First Visit", "Card saved, charged after the first visit.", ["reassuring", "easy"], "neighbor", pay("later")),
    O("fn_pay_now", "Pay Now To Start", "Card form and 'Pay $99 And Start'.", ["direct", "clear"], "crew", pay("now")), "Pay Later Or Pay Now?")
def signopt(mode):
    o = h1(14, 56, "One Last Thing", 17)
    if mode == "toggle": o += rect(14, 66, 212, 64, "#FFFFFF", LINE, 8) + t(22, 86, "Put A Yard Sign Out?", 11, INK, "khand") + para(22, 100, ["We'll swap your smoke and CO", "batteries on us."], 7.6, MUTE, 10) + toggle(194, 80, True, JUNGLE)
    else: o += yard("h", "maint", "terra").split('<g clip-path="url(#c)">')[1].rsplit("</g>", 1)[0].replace('<rect width="240" height="300"', '<rect width="0" height="0"', 1) if False else rect(14, 66, 212, 120, "#DCEAF0", r=8) + rect(14, 150, 212, 36, "#9DB58A") + rect(70, 92, 100, 54, "#FFFFFF", "#BDBDBD") + roof_logo(86, 116, .9) + rect(70, 140, 100, 4, TERRA) + rect(90, 146, 2, 20, "#6E6E6E") + rect(148, 146, 2, 20, "#6E6E6E") + t(14, 204, "Put A Yard Sign Out? Battery Swap On Us.", 8.5, INK, "khand") + chip(14, 214, "Yes, Please", True, JUNGLE, 100) + chip(120, 214, "No Thanks", False, INK, 100)
    return scr(o + btn(262, "Finish Sign-Up", "fill", INK, h=24, size=8))
add(GI, "Funnel: Yard Sign Opt-In", O("fn_sign_toggle", "Yard Sign Ask As A Switch", "A switch row with the battery-swap perk.", ["simple", "quiet"], "system", signopt("toggle")),
    O("fn_sign_picture", "Yard Sign Ask With A Drawing", "A drawn sign on a lawn with Yes / No chips.", ["visual", "lively"], "neighbor", signopt("picture")), "Switch Or Picture?")
# ---- re-asks of upkeep-4 skips (fresh forms) + third directions for the two NEITHERs ----
GR = "Re-Asks In New Forms"
def fig(x, y, s=1, shirt="#F4F4F2", cap="#2B2B2B", collar=None, style="flat", mark=True):
    o = scan_tech(x, y, s, style, shirt, cap)
    if collar: o += f'<g transform="translate({x},{y}) scale({s})"><path d="M-8 0 L0 8 L8 0 Z" fill="{collar}"/><rect x="-13" y="36" width="26" height="4" fill="{collar}"/></g>'
    if mark and style == "flat": o += f'<g transform="translate({x},{y}) scale({s})"><polyline points="-8,16 -4.5,13 -1,16" fill="none" stroke="{INK if shirt in ("#F4F4F2", "#FFFFFF") else "#FFFFFF"}" stroke-width="1.3"/></g>'
    return o
def cancel_spot(mode):
    o = h1(14, 58, "Membership", 18) + rect(14, 70, 212, 120, "#FFFFFF", LINE, 6) + rect(14, 70, 212, 4, TERRA)
    o += t(120, 96, "MEMBERSHIP STARTING AT", 6.5, MUTE, "hind", 600, "middle", 'letter-spacing="1.2"') + t(108, 132, "$99", 34, TERRA, "khand", anchor="middle") + t(142, 132, "/Month", 10, INK, "khand", anchor="middle")
    for i, (k, s) in enumerate(INC[:2]): o += icon("check", 30, 146 + i * 18, 11, "duo", JUNGLE) + t(46, 155 + i * 18, s, 8, INK)
    if mode == "banner":
        o += rect(14, 200, 212, 30, JUNGLE + "14", "none", 6) + icon("check", 24, 207, 16, "duo", JUNGLE) + t(46, 219, "Cancel Anytime", 11, INK, "khand") + t(46, 227, "No contract. Stop with one tap.", 6.5, MUTE)
        o += btn(240, "Get My Personal Price", "fill", INK, h=28)
    else:
        o += btn(214, "Get My Personal Price", "fill", INK, h=34) + t(120, 260, "Cancel Anytime · No Contract", 7.5, MUTE, "hind", 600, "middle")
    return scr(o)
def char_card(style):
    o = rect(14, 44, 212, 186, CREAM if False else "#FFFFFF", LINE, 8) + house_ill(130, 70, .5, "#5B5550", "#6B4B3A", "#B8CCD8") + f'<line x1="22" y1="206" x2="218" y2="206" stroke="{INK if style=="line" else "#9DB58A"}" stroke-width="{1.5 if style=="line" else 6}"/>'
    o += fig(70, 140, 1.1, "#5E6B73", "#2B2B2B", style=style, mark=False) if style == "flat" else scan_tech(70, 140, 1.1, "line", TERRA)
    o += h1(14, 252, "Your Tech Is On The Way", 15) + t(14, 266, "Arriving Tue 9 AM. Look for the white van.", 7.5, MUTE)
    return scr(o)
def door_fig(shirt):
    o = rect(0, 34, W, 266, "#FFFFFF") + rect(132, 70, 80, 170, "#F7F4EE", "#BDB6AA", 2) + rect(146, 90, 52, 150, "#6B4B3A") + dot(190, 168, 2.5, "#E8C77A") + rect(0, 240, W, 60, "#E8E2D8")
    o += fig(86, 168, 1.35, shirt, "#2B2B2B")
    o += h1(14, 64, "At Your Door", 16) + t(14, 268, "Polo: " + ("Terracotta" if shirt == TERRA else "White, black logo"), 9, INK, "khand")
    return scr(o)
def crew(kind):
    o = h1(14, 62, "The Up Keep Crew", 17) + rect(0, 220, W, 80, "#EFEBE4")
    looks = {"mixed": [("#F4F4F2", "#2B2B2B", None), ("#5E6B73", "#2B2B2B", None), (TERRA, "#2B2B2B", None)],
             "white": [("#F4F4F2", "#2B2B2B", None)] * 3,
             "collar": [("#F4F4F2", "#2B2B2B", TERRA)] * 3,
             "grey": [("#5E6B73", "#2B2B2B", None)] * 3}[kind]
    for i, (sh, cp, col) in enumerate(looks): o += fig(52 + i * 68, 150, 1.05, sh, cp, col)
    cap = {"mixed": "Mixed: White, Grey, Terracotta", "white": "Everyone In White Polos", "collar": "White With Terracotta Collar", "grey": "Grey Uniform, Dark Cap"}[kind]
    return scr(o + t(120, 262, cap, 11, INK, "khand", anchor="middle"))
def street_van(th):
    o = rect(0, 34, W, 150, "#DCEAF0") + house_ill(120, 60, .6, "#5B5550", "#6B4B3A", "#B8CCD8") + rect(0, 184, W, 116, "#C9C6C0") + rect(0, 184, W, 10, "#9DB58A")
    x, y, sc = 30, 196, .86
    o += f'<g transform="translate({x},{y}) scale({sc})"><path d="M0 70 V10 Q0 0 10 0 H140 L196 40 V70 Z" fill="#FFFFFF" stroke="#6E6E6E" stroke-width="1.2"/><path d="M144 6 L186 38 H144 Z" fill="#B8CCD8"/>'
    a, b = (58, 62) if th == "thin" else (50, 66)
    o += f'<path d="M0 {a} H110 Q132 {a} 146 38 L154 38 Q138 {b} 112 {b} H0 Z" fill="{TERRA}"/>' if th == "thin" else f'<path d="M0 {a} H104 Q128 {a} 142 38 L158 38 Q142 {b} 110 {b} H0 Z" fill="{TERRA}"/>'
    o += '<circle cx="36" cy="70" r="12" fill="#2B2B2B"/><circle cx="160" cy="70" r="12" fill="#2B2B2B"/></g>' + roof_logo(x + 16, y + 34, 1.3, INK, MUTE)
    return scr(o + t(120, 288, ("Thin" if th == "thin" else "Thick") + " Sweep Stripe", 10, INK, "khand", anchor="middle"))
def lic_only(line):
    o = techface(120, 78, 22) + t(120, 130, "Your Licensed Tech", 15, INK, "khand", anchor="middle")
    o += rect(40, 142, 160, 52, "#FFFFFF", JUNGLE, 8, 1.5) + shield(52, 154, JUNGLE, 1.1) + t(86, 166, "License Active", 12, INK, "khand") + t(86, 180, "State Mechanical License", 7, MUTE)
    if line: o += rect(14, 204, 212, 30, SAFFRON + "1F", "none", 6) + icon("check", 22, 211, 16, "duo", JUNGLE) + t(44, 224, "Tech May Change, Always Licensed", 9.5, INK, "khand")
    o += rect(14, 244 if line else 214, 212, 28, LAGOON) + shield(50, 248 if line else 218, "#FFFFFF", .7, False) + t(124, (262 if line else 232), "TAP TO VERIFY LICENSE", 8, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
    return scr(o)
add(GR, "Re-Ask: Cancel Anytime Placement", O("ra_cancel_banner", "Cancel Anytime As A Green Banner", "A soft green strip with a check above the button.", ["visual", "reassuring", "big"], "neighbor", cancel_spot("banner")),
    O("ra_cancel_under", "Cancel Anytime As Small Text Under The Button", "One grey line under a big black button.", ["simple", "quiet"], "system", cancel_spot("under")), "Where Does Cancel Anytime Go?", retest=True)
add(GR, "Re-Ask: Character Drawing Style", O("ra_char_flat", "Flat Filled Tech On The Arrival Card", "Solid shapes on the 'On The Way' card.", ["lively", "visual", "neighbor"], "neighbor", char_card("flat")),
    O("ra_char_line", "Black Line-Art Tech On The Arrival Card", "Same card, tech drawn in black line.", ["simple", "readable"], "system", char_card("line")), "Filled Or Line-Art Tech, On A Real Screen?", retest=True)
add(GR, "Re-Ask: Polo Color At The Door", O("ra_door_terra", "Terracotta Polo At The Door", "The tech at your front door in terracotta.", ["lively", "visual"], "neighbor", door_fig(TERRA)),
    O("ra_door_white", "White Polo At The Door", "The tech at your front door in white with a black mark.", ["simple", "readable"], "neighbor", door_fig("#F4F4F2")), "Terracotta Or White Polo, Seen At The Door?", retest=True)
add(GR, "Re-Ask: Crew Outfits", O("ra_crew_mixed", "Crew In Mixed Outfits", "White, grey and terracotta on three techs.", ["lively", "neighbor", "visual"], "neighbor", crew("mixed")),
    O("ra_crew_white", "Whole Crew In White", "All three techs in white polos.", ["simple", "unified"], "system", crew("white")), "Mixed Or Matching Crew?", retest=True)
add(GR, "Re-Ask: Van Stripe Weight", O("ra_van_thin", "Thin Sweep Stripe, Parked Out Front", "The sweeping stripe, thin, seen from the street.", ["simple", "light"], "system", street_van("thin")),
    O("ra_van_thick", "Thick Sweep Stripe, Parked Out Front", "The sweeping stripe, thick, seen from the street.", ["big", "visual", "lively"], "neighbor", street_van("thick")), "Thin Or Thick Stripe From The Curb?", retest=True)
add(GR, "New Direction: Tech Detail", O("ra_tech_lic_only", "License Only", "Face, 'Your Licensed Tech', license badge and Verify. No stats, no note.", ["simple", "readable", "big"], "neighbor", lic_only(False)),
    O("ra_tech_lic_line", "License Plus 'Tech May Change, Always Licensed'", "Same card with one plain line about the tech changing.", ["honest", "readable", "guided"], "neighbor", lic_only(True)), "License Only, Or Add The Always-Licensed Line?")
add(GR, "New Direction: Crew Uniform", O("ra_crew_collar", "White Polo With A Terracotta Collar", "White polos with a small terracotta collar and hem.", ["lively", "neighbor", "visual"], "neighbor", crew("collar")),
    O("ra_crew_grey", "Grey Uniform, Dark Cap", "The grey work uniform with a dark cap on the whole crew.", ["pro", "readable"], "system", crew("grey")), "White With Terracotta Collar Or Grey Uniform?")

# ---- order: pairs 1-5 (white base follow-ups) fixed first; then no group twice in a row ----
random.seed(55); first = pairs[:FIRST]; rest = pairs[FIRST:]; random.shuffle(rest); seq = rest; order = list(first)
while seq:
    k = next((i for i, p in enumerate(seq) if not order or p["group"] != order[-1]["group"]), 0); order.append(seq.pop(k))
for i, p in enumerate(order, 1):
    p.update(id=f"{DID}-{i:02d}", repeat=False)
alloc, feel, groups = {}, {}, {}
for p in order:
    alloc[p["category"]] = alloc.get(p["category"], 0) + 1; groups[p["group"]] = groups.get(p["group"], 0) + 1
    for s in "AB":
        f = p["option" + s].get("feeling")
        if f: feel[f] = feel.get(f, 0) + 1
ids = [p["option" + s]["id"] for p in order for s in "AB"]
assert len(order) == 50, len(order)
assert len(ids) == len(set(ids)), "duplicate option id"
ledger = json.load(open("shown_options.json"))
shown = {k for k, v in ledger.get("options", {}).items() if v != [DID]}
import glob, os
for fp in glob.glob("decks/*.json"):
    if os.path.basename(fp) == f"{DID}.json": continue
    for pp in json.load(open(fp)).get("pairs", []):
        for s in "AB":
            o = pp.get("option" + s) or {}
            if o.get("id"): shown.add(o["id"])
rep = [i for i in ids if i in shown]; assert not rep, f"repeats: {rep}"
assert all(p["option" + s]["tags"] for p in order for s in "AB")
now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
deck = {"date": DID, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True,
        "title": "Up Keep Round 5: White Base Follow-Ups, Re-Asks, Photo Onboarding, Visit Log, Home Record, Ask Anything, Reminders, Tech App, Email And Receipts", "brands": ["Up Keep / Smart Upkeep: home maintenance membership app (https://webermanapps.github.io/smart-upkeep/)", "Base: white, #0A0A0A ink, square black buttons, Khand/Hind; 2-3 small pops (terracotta = act, lagoon = info, jungle = done, saffron = due soon); no neon, no pastel, not all-beige"],
        "generated_at": now, "builds_on": "upkeep-4 results (45/50; white won; top tags lively, neighbor, big, visual, readable, easy, simple, guided; avoided concierge, bold, thorough, crew, calm, clean; skipped 17, 26, 27, 49, 50 re-asked here; NEITHERs 36 tech detail and 47 get third directions); upkeep-3 results (32/50; top tags system, clear, warm, simple, lively; notes: drop score screens, show uniforms on people); upkeep-1 top tags clear, system, warm, lively, multi-accent; upkeep-2 top tags clear, system, visual, guided, easy (no upkeep results files in results/)",
        "feelings": {"neighbor": "Trusted neighbor", "system": "Calm organized system", "concierge": "Quiet premium concierge", "crew": "No-nonsense pro crew"},
        "feeling_counts": feel, "allocation": alloc, "groups": groups, "apps": {"Up Keep": len(order)},
        "pair_mix": {"refine": sum(p["purpose"] == "refine" for p in order), "check": sum(p["purpose"] == "check" for p in order), "retest": sum(p["retest"] for p in order)},
        "sources": {"app": "https://webermanapps.github.io/smart-upkeep/", "app_source": "/workspace/smartkeep/funnel-app/", "ideas": "/workspace/smartkeep/ideas/2026-10-12.md", "brand": "/workspace/ops/brand/maxweberman-brand.md"},
        "freshness": {"option_slots": len(ids), "never_shown_before": len(ids), "share": 1.0}, "warnings": [], "pairs": order}
json.dump(deck, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
# ledger: add this deck's option ids under DID (idempotent)
opts = ledger["options"]
for k in [k for k, v in opts.items() if v == [DID]]: del opts[k]
for i in ids: opts[i] = [DID]
ledger["options"] = dict(sorted(opts.items())); ledger["shown_count"] = len(opts); ledger["updated"] = now
json.dump(ledger, open("shown_options.json", "w"), indent=1)
print(len(order), "pairs", groups)

