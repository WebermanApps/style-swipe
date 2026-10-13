#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-3: 25 all-new this-or-that pairs, round 3 of the Up Keep / Smart Upkeep home maintenance
membership app (https://webermanapps.github.io/smart-upkeep/). Mock screens are drawn as SVG in Up Keep's own style
(white base, #0A0A0A ink, square black buttons, Khand headings, Hind body, terracotta accent, #E5E0D8 rules) and
rendered through the 'hm' svg renderer. Run from the style-swipe repo root."""
import json, random, re, datetime as dt
DID = "upkeep-3"; LOGOS = "/workspace/brand/smart-upkeep/logos"
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
    return {"id": "uk3_" + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": bg}}
def add(group, cat, a, b, ask, purpose="refine", retest=False):
    pairs.append({"group": group, "category": cat, "app": "Up Keep", "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": retest})
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

# ===================== 1. Tech visit report detail (3) =====================
RP = "Up Keep: Visit Report Detail"
add(GR, RP,
 O("rep_photogrid", "Report Opens On A Photo Grid", "Six photos from the visit in a grid, each with a short caption. Checklist below.", ["visual", "proof", "lively"], "neighbor",
   screen(lbl(14, 48, "Fall visit · Nov 4") + h1(14, 66, "Your Visit Report", 17) + "".join(photo(14 + (i % 3) * 72, 76 + (i // 3) * 66, 68, 50, k, 4, "warm" if i % 2 else "day") + t(14 + (i % 3) * 72, 136 + (i // 3) * 66, c, 6.5, MUTE) for i, (k, c) in enumerate([("label", "Furnace label"), ("tech", "Burner clean"), ("house", "Gutters clear"), ("interior", "Filter swapped"), ("label", "Water heater"), ("house", "Dryer vent")])) + link(14, 222, "See The 11-Point Checklist", LAGOON) + btn(240, "Download PDF", "outline"))),
 O("rep_checkfirst", "Report Opens On The Checklist", "Every check as a row with a done mark; photos open from a camera icon on each row.", ["clear", "system", "thorough"], "system",
   screen(lbl(14, 48, "Fall visit · Nov 4") + h1(14, 66, "Your Visit Report", 17) + "".join(ln(76 + i * 24) + icon("check", 14, 81 + i * 24, 13, "duo", c) + t(34, 91 + i * 24, n, 8.5, INK) + (icon("cam", 208, 81 + i * 24, 13, "outline") if p else "") for i, (n, c, p) in enumerate([("Furnace tune-up", JUNGLE, 1), ("Filter swapped", JUNGLE, 1), ("Gutters cleaned", JUNGLE, 1), ("CO and smoke test", JUNGLE, 0), ("Water heater flush", JUNGLE, 1), ("Dryer vent: watch", SAFFRON, 1)])) + btn(240, "Download PDF", "outline"))),
 "What Should A Visit Report Open On?")
add(GR, RP,
 O("rep_ba_slider", "Before / After As A Drag Slider", "One photo split down the middle; drag the handle to wipe between before and after.", ["interactive", "modern", "visual"], "system",
   screen(h1(14, 56, "Gutters: Before And After", 15) + photo(14, 66, 212, 140, "house", 6, "mute") + photo(120, 66, 106, 140, "house", 0, "day") + f'<line x1="120" y1="66" x2="120" y2="206" stroke="#FFFFFF" stroke-width="3"/>' + dot(120, 136, 10, "#FFFFFF") + t(120, 140, "‹ ›", 9, INK, "hind", 600, "middle") + tag(20, 74, "Before", MUTE, True) + tag(186, 74, "After", JUNGLE, True) + t(14, 226, "Drag to compare · Nov 4", 7.5, MUTE))),
 O("rep_ba_pair", "Before / After Side By Side", "Two photos next to each other with Before and After labels and one line of what changed.", ["clear", "simple", "proof"], "crew",
   screen(h1(14, 56, "Gutters: Before And After", 15) + photo(14, 66, 104, 120, "house", 6, "mute") + photo(122, 66, 104, 120, "house", 6, "day") + lbl(14, 200, "Before") + lbl(122, 200, "After", JUNGLE) + para(14, 220, ["Removed 3 bags of leaves; downspouts", "flow freely again."], 8, INK, 11))),
 "How Should Before And After Photos Show?")
add(GR, RP,
 O("rep_note_top", "Tech's Note Leads The Report", "A short signed note from Danny at the top, then the results.", ["personal", "warm", "human"], "neighbor",
   screen(h1(14, 56, "Fall Visit Report", 17) + rect(14, 66, 212, 92, CREAM, LINE, 6) + face(36, 88, 10) + t(54, 86, "From Danny", 9, INK, "hind", 600) + t(54, 97, "Nov 4 · 92 minutes", 6.8, MUTE) + para(24, 118, ["Everything looks good, Sarah. Your dryer", "vent is getting lint-heavy; I'd clean it", "in spring. Photos below."], 7.8, INK, 11) + rows(170, [("11 checks done", "✓"), ("1 to watch", "Dryer vent")]) + btn(240, "See Photos", "outline"))),
 O("rep_counts_top", "Result Counts Lead The Report", "Three big numbers up top: Done, To Watch, Fix Now. The note sits below.", ["system", "scannable", "data"], "system",
   screen(h1(14, 56, "Fall Visit Report", 17) + "".join(rect(14 + i * 72, 66, 68, 60, "#FFFFFF", LINE, 4) + rect(14 + i * 72, 66, 68, 4, c) + t(48 + i * 72, 102, n, 22, INK, "khand", anchor="middle") + t(48 + i * 72, 118, l, 6.5, MUTE, "hind", 600, "middle") for i, (n, l, c) in enumerate([("11", "DONE", JUNGLE), ("1", "TO WATCH", SAFFRON), ("0", "FIX NOW", TERRA)])) + lbl(14, 146, "Danny's note") + para(14, 160, ["All good. Dryer vent is getting", "lint-heavy; clean it in spring."], 8, INK, 11) + btn(240, "See Photos", "outline"))),
 "What Should Lead A Visit Report?")
# ===================== 2. Home health score explained (3) =====================
HS = "Up Keep: Home Health Score"
add(GH, HS,
 O("hs_factors", "Score With Factor Bars", "The score, then one bar per factor: systems age, visits done, open issues, safety.", ["transparent", "data", "system"], "system",
   screen(h1(14, 56, "Home Health: 88", 17) + t(14, 70, "How we got your score", 7.5, MUTE) + "".join(t(14, 92 + i * 30, n, 8, INK, "hind", 600) + t(226, 92 + i * 30, v, 7.5, MUTE, anchor="end") + rect(14, 97 + i * 30, 212, 5, "#EEEAE4", r=2.5) + rect(14, 97 + i * 30, 212 * f, 5, c, r=2.5) for i, (n, v, f, c) in enumerate([("Visits done", "4 of 4", 1, JUNGLE), ("Safety checks", "All pass", 1, JUNGLE), ("Systems age", "Water heater 9 yrs", .55, SAFFRON), ("Open issues", "1 to watch", .8, LAGOON)])) + link(14, 222, "How To Raise It", TERRA))),
 O("hs_words", "Score In Plain Words", "The score with three sentences: what's good, what's slipping, what to do.", ["plain", "calm", "clear"], "neighbor",
   screen(ring(120, 92, 32, .88, JUNGLE, "") + t(120, 99, "88", 22, INK, "khand", anchor="middle") + h1(120, 150, "Your Home Is In Good Shape", 15, anchor="middle") + "".join(t(20, 174 + i * 22, s, 9, c, "hind", 600) + t(34, 174 + i * 22, l, 8, INK) for i, (s, l, c) in enumerate([("✓", "All four visits done this year", JUNGLE), ("!", "Water heater is 9 years old", SAFFRON), ("→", "Clean the dryer vent in spring", TERRA)])))),
 "How Should The Home Health Score Be Explained?")
add(GH, HS,
 O("hs_trend", "Score Over Time", "A line chart of the score by season, with a dot for each visit.", ["progress", "data", "lively"], "system",
   screen(h1(14, 56, "Home Health", 17) + t(226, 56, "88", 20, JUNGLE, "khand", anchor="end") + rect(14, 68, 212, 110, "#FFFFFF", LINE, 4) + "".join(ln(80 + i * 24, 22, 218) for i in range(4)) + f'<polyline points="30,150 80,132 130,112 180,96 210,90" fill="none" stroke="{LAGOON}" stroke-width="2.2"/>' + "".join(dot(x, y, 3.5, JUNGLE) for x, y in [(30, 150), (80, 132), (130, 112), (180, 96), (210, 90)]) + "".join(t(30 + i * 50, 172, m, 6.5, MUTE, "hind", 600, "middle") for i, m in enumerate(["Fall", "Winter", "Spring", "Summer"])) + t(14, 198, "Up 17 points since you joined", 8.5, INK, "hind", 600) + t(14, 212, "Each dot is a visit", 7, MUTE))),
 O("hs_compare", "Score Next To Similar Homes", "Your score on a scale with the average for 2,000 to 3,000 sq ft homes in Novi.", ["context", "competitive", "clear"], "crew",
   screen(h1(14, 56, "Home Health", 17) + t(14, 70, "Compared with similar Novi homes", 7.5, MUTE) + rect(14, 112, 212, 8, "#EEEAE4", r=4) + rect(14, 112, 150, 8, SAFFRON + "66", r=4) + f'<line x1="146" y1="104" x2="146" y2="128" stroke="{MUTE}" stroke-width="1.5"/>' + t(146, 140, "Avg 71", 7, MUTE, "hind", 600, "middle") + dot(200, 116, 8, JUNGLE) + t(200, 98, "You 88", 8, JUNGLE, "hind", 600, "middle") + rows(160, [("Visits done", "Top 10%"), ("Systems age", "Average"), ("Open issues", "Fewer than most")]))),
 "Score Over Time Or Next To Neighbors?")
add(GH, HS,
 O("hs_badge_dash", "Score As A Small Badge", "The score is a small pill in the dashboard header, tap to open the details.", ["quiet", "compact", "minimal"], "concierge",
   screen(lbl(14, 48, "Hi Sarah") + h1(14, 66, "Welcome Home", 17) + rect(160, 54, 66, 16, JUNGLE + "1F", r=8) + t(193, 65, "HEALTH 88 ›", 6.5, JUNGLE, "hind", 600, "middle") + rect(14, 78, 212, 50, CREAM, LINE, 6) + t(22, 96, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(22, 114, "Tue, Nov 4 · 9 AM", 13, INK, "khand") + rows(140, [("Furnace", "OK"), ("Water heater", "Due Nov"), ("AC unit", "OK")]) + tabbar(0))),
 O("hs_hero_page", "Score Gets Its Own Page", "A full page: big score, a one-line verdict and the three biggest factors.", ["bold", "focused", "system"], "system",
   screen(t(120, 110, "88", 64, INK, "khand", anchor="middle") + t(120, 128, "OUT OF 100 · GOOD", 7, JUNGLE, "hind", 600, "middle", 'letter-spacing="1"') + pbar(140, .88, JUNGLE, 40, 160) + "".join(rect(14 + i * 72, 162, 68, 46, "#FFFFFF", LINE, 4) + t(48 + i * 72, 182, v, 12, INK, "khand", anchor="middle") + t(48 + i * 72, 196, l, 6.3, MUTE, "hind", 600, "middle") for i, (v, l) in enumerate([("4/4", "VISITS"), ("Pass", "SAFETY"), ("9 yrs", "OLDEST")])) + btn(226, "How To Raise It", col=TERRA) + tabbar(0))),
 "How Big Should The Health Score Be?")

# ===================== 3. Lifespan / replacement forecast (2) =====================
FC = "Up Keep: Replacement Forecast"
add(GH, FC,
 O("fc_years", "Forecast As A Year Line", "A line from 2026 to 2036 with each system's likely replacement year pinned on it.", ["visual", "forward", "system"], "system",
   screen(h1(14, 56, "What To Plan For", 17) + f'<line x1="20" y1="120" x2="220" y2="120" stroke="{LINE}" stroke-width="3"/>' + "".join(t(20 + i * 50, 140, str(2026 + int(i * 2.5)), 6.5, MUTE, "hind", 600, "middle") for i in range(5)) + "".join(f'<line x1="{x}" y1="{y+6}" x2="{x}" y2="120" stroke="{c}" stroke-width="1.4"/>' + dot(x, 120, 4.5, c) + t(x, y, n, 7, INK, "hind", 600, "middle") for x, y, n, c in [(52, 88, "Water heater '29", SAFFRON), (120, 102, "AC '31", LAGOON), (180, 82, "Furnace '34", JUNGLE)]) + rows(160, [("Water heater", "~$1,600 · 2029"), ("AC unit", "~$5,800 · 2031"), ("Furnace", "~$4,900 · 2034")]))),
 O("fc_cards", "Forecast As Budget Cards", "One card per system: years left, rough cost, and a 'Get A Quote' link.", ["practical", "clear", "money"], "crew",
   screen(h1(14, 56, "What To Plan For", 17) + "".join(rect(14, 66 + i * 58, 212, 52, "#FFFFFF", LINE, 6) + rect(14, 66 + i * 58, 4, 52, c) + t(26, 84 + i * 58, n, 11, INK, "khand") + t(26, 98 + i * 58, y, 7.5, MUTE) + t(218, 86 + i * 58, p, 13, INK, "khand", anchor="end") + link(218, 108 + i * 58, "Get A Quote", TERRA, "end", 6.5) for i, (n, y, p, c) in enumerate([("Water Heater", "About 3 years left", "$1,600", SAFFRON), ("AC Unit", "About 5 years left", "$5,800", LAGOON), ("Furnace", "About 8 years left", "$4,900", JUNGLE)])))),
 "How Should The Replacement Forecast Look?")
add(GH, FC,
 O("fc_setaside", "Forecast As A Monthly Set-Aside", "Turns the forecast into one number: 'Put away about $96 a month.'", ["simple", "helpful", "money"], "neighbor",
   screen(h1(14, 56, "Plan Ahead", 17) + t(120, 120, "$96", 44, INK, "khand", anchor="middle") + t(120, 138, "a month covers your next 3 replacements", 8, MUTE, anchor="middle") + rows(158, [("Water heater · 2029", "$1,600"), ("AC unit · 2031", "$5,800"), ("Furnace · 2034", "$4,900")]) + btn(240, "Remind Me Monthly", "outline"))),
 O("fc_lifebars", "Forecast As Life-Used Bars", "Each system gets a bar showing how much of its life is used, colored by urgency.", ["visual", "system", "lively"], "system",
   screen(h1(14, 56, "System Life", 17) + "".join(t(14, 84 + i * 36, n, 8.5, INK, "hind", 600) + t(226, 84 + i * 36, y, 7, MUTE, anchor="end") + rect(14, 90 + i * 36, 212, 8, "#EEEAE4", r=4) + rect(14, 90 + i * 36, 212 * f, 8, c, r=4) for i, (n, y, f, c) in enumerate([("Water Heater", "9 of 12 yrs", .75, SAFFRON), ("AC Unit", "10 of 15 yrs", .66, LAGOON), ("Furnace", "7 of 18 yrs", .39, JUNGLE), ("Roof", "6 of 25 yrs", .24, JUNGLE)])) + link(14, 236, "See Replacement Costs", TERRA))),
 "Show A Set-Aside Number Or Life Bars?")

# ===================== 4. Maintenance history timeline (2) =====================
HI = "Up Keep: Maintenance History"
HIST = [("Nov 4, 2026", "Fall visit", "11 checks · 1 to watch", TERRA), ("Aug 5, 2026", "Summer visit", "Dryer vent, GFCIs", JUNGLE), ("May 6, 2026", "Spring visit", "AC tune-up, gutters", JUNGLE), ("Mar 2, 2026", "Recall fix", "Water heater valve", SAFFRON)]
add(GL, HI,
 O("hist_rail", "Vertical Timeline Rail", "A line down the left with a colored dot per event and the newest on top.", ["visual", "story", "lively"], "neighbor",
   screen(h1(14, 56, "Home History", 17) + f'<line x1="22" y1="72" x2="22" y2="250" stroke="{LINE}" stroke-width="2"/>' + "".join(dot(22, 78 + i * 46, 6, c) + t(36, 76 + i * 46, d, 6.8, MUTE, "hind", 600) + t(36, 90 + i * 46, n, 10.5, INK, "khand") + t(36, 101 + i * 46, s, 7, MUTE) for i, (d, n, s, c) in enumerate(HIST)))),
 O("hist_table", "History As A Dated Table", "Plain rows: date, what was done, who did it. Sort and export.", ["clear", "record", "practical"], "system",
   screen(h1(14, 56, "Home History", 17) + link(226, 56, "Export", LAGOON, "end") + lbl(14, 76, "Date") + lbl(80, 76, "Work") + lbl(190, 76, "By") + "".join(ln(82 + i * 26) + t(14, 98 + i * 26, d[:6], 8, MUTE) + t(80, 98 + i * 26, n, 8, INK, "hind", 600) + t(190, 98 + i * 26, "Danny" if i != 3 else "Mike", 8, MUTE) for i, (d, n, s, c) in enumerate(HIST + [("Feb 3, 2026", "Winter visit", "", "")])))),
 "How Should Maintenance History Look?")
add(GL, HI,
 O("hist_chips", "History Filtered By System", "Chips across the top (All, Furnace, Water Heater, AC) filter the list.", ["control", "organized", "system"], "system",
   screen(h1(14, 56, "Home History", 17) + chip(14, 66, "All", True) + chip(44, 66, "Furnace") + chip(92, 66, "Water Heater") + chip(162, 66, "AC") + rows(96, [("Nov 4 · Furnace tune-up", "Danny"), ("Mar 2 · Recall valve swap", "Mike"), ("Oct 8 · Tank flush", "Danny"), ("May 6 · AC tune-up", "Danny"), ("Feb 3 · Burner check", "Danny")], 28))),
 O("hist_byyear", "History Grouped By Year", "Big year headings, with each year's visits as short cards.", ["calm", "story", "warm"], "neighbor",
   screen(t(14, 62, "2026", 22, INK, "khand") + "".join(rect(14, 70 + i * 30, 212, 26, CREAM, LINE, 4) + t(22, 87 + i * 30, n, 8.5, INK, "hind", 600) + t(218, 87 + i * 30, d, 7.5, MUTE, anchor="end") for i, (n, d) in enumerate([("Fall visit", "Nov 4"), ("Summer visit", "Aug 5"), ("Spring visit", "May 6")])) + t(14, 186, "2025", 22, INK, "khand") + rect(14, 194, 212, 26, CREAM, LINE, 4) + t(22, 211, "Joined Up Keep · first visit", 8.5, INK, "hind", 600) + t(218, 211, "Oct 8", 7.5, MUTE, anchor="end"))),
 "Filter By System Or Group By Year?")
# ===================== 5. Document vault (2) =====================
DV = "Up Keep: Document Vault"
add(GL, DV,
 O("doc_folders", "Vault As Three Folders", "Manuals, Receipts and Warranties as three big folder tiles with counts.", ["visual", "organized", "simple"], "neighbor",
   screen(h1(14, 56, "My Documents", 17) + "".join(rect(14, 68 + i * 54, 212, 46, "#FFFFFF", LINE, 6) + f'<path d="M24 {80+i*54} h12 l3 3 h17 v20 h-32 Z" fill="{c}22" stroke="{c}" stroke-width="1.4"/>' + t(66, 92 + i * 54, n, 11, INK, "khand") + t(66, 104 + i * 54, s, 7, MUTE) + t(218, 94 + i * 54, "›", 12, MUTE, anchor="end") for i, (n, s, c) in enumerate([("Manuals", "9 files · from your labels", LAGOON), ("Receipts", "14 files", TERRA), ("Warranties", "5 files · 1 ends soon", JUNGLE)])) + btn(236, "Add A Document", "outline"))),
 O("doc_bysystem", "Vault Sorted By System", "Each system lists its own manual, receipt and warranty in one row.", ["system", "linked", "clear"], "system",
   screen(h1(14, 56, "My Documents", 17) + "".join(ln(66 + i * 44) + icon(k, 14, 74 + i * 44, 18, "outline") + t(40, 85 + i * 44, n, 9, INK, "hind", 600) + tag(40, 92 + i * 44, "Manual", LAGOON) + tag(86, 92 + i * 44, "Receipt", TERRA) + tag(134, 92 + i * 44, "Warranty", JUNGLE if i != 1 else "#A3A3A3") for i, (k, n) in enumerate(SYS3)) + btn(244, "Add A Document", "outline"))),
 "How Should The Document Vault Be Organized?")
add(GL, DV,
 O("doc_snap", "Add A Receipt By Snapping It", "A camera button: snap a paper receipt and we file it under the right system.", ["easy", "modern", "guided"], "system",
   screen(h1(14, 56, "Add A Receipt", 17) + rect(14, 68, 212, 120, "#FFFFFF", "#CFC8BC", 6, 1.3, 'stroke-dasharray="4 3"') + icon("cam", 104, 104, 32, "duo", TERRA) + t(120, 162, "Snap The Receipt", 8.5, INK, "hind", 600, "middle") + t(120, 174, "We'll read the store, date and item", 7, MUTE, anchor="middle") + btn(204, "Open Camera") + link(120, 248, "Upload A File Instead", MUTE, "middle"))),
 O("doc_forward", "Add A Receipt By Forwarding Email", "Shows a personal address: forward any receipt email and it lands in the vault.", ["effortless", "clever", "calm"], "concierge",
   screen(h1(14, 56, "Add A Receipt", 17) + para(14, 74, ["Forward any receipt email to your", "own vault address:"], 8.5, INK, 12) + rect(14, 104, 212, 30, CREAM, LINE, 4) + t(120, 123, "sarah.novi@docs.upkeep.app", 8.5, INK, "hind", 600, "middle") + btn(146, "Copy Address", "outline") + rows(186, [("Home Depot · Oct 2", "Filed: Furnace"), ("Lowe's · Sep 14", "Filed: Water heater")]))),
 "How Should Receipts Get Into The Vault?")

# ===================== 6. Seasonal checklist (2) =====================
SC = "Up Keep: Seasonal Checklist"
add(GG, SC,
 O("seas_boxes", "Checklist With Tick Boxes", "Fall tasks for the homeowner as tick boxes with a progress count.", ["clear", "satisfying", "system"], "system",
   screen(h1(14, 56, "Your Fall Checklist", 17) + t(226, 56, "3 of 6", 8, JUNGLE, "hind", 600, "end") + pbar(64, .5, JUNGLE) + "".join(ln(76 + i * 26) + check_box(14, 83 + i * 26, on) + t(32, 92 + i * 26, n, 8.5, MUTE if on else INK, extra='text-decoration="line-through"' if on else "") for i, (n, on) in enumerate([("Shut off outdoor faucets", True), ("Bring in hoses", True), ("Swap furnace filter", True), ("Test smoke alarms", False), ("Clean dryer lint trap", False), ("Reverse ceiling fans", False)])))),
 O("seas_cards", "Checklist As Swipeable Cards", "One task per card with a picture and 'Done' or 'Later'.", ["playful", "focused", "lively"], "neighbor",
   screen(lbl(14, 50, "Fall checklist · 4 of 6") + rect(22, 64, 196, 160, "#FFFFFF", LINE, 10) + photo(30, 72, 180, 90, "house", 6, "warm") + h1(120, 186, "Shut Off Outdoor Faucets", 13, anchor="middle") + t(120, 200, "2 minutes · before the first freeze", 7, MUTE, anchor="middle") + btn(234, "Later", "outline", w=100) + btn(234, "Done", col=JUNGLE, x=126, w=100))),
 "How Should The Homeowner Checklist Work?")
add(GG, SC,
 O("seas_split", "Split: You Do / We Do", "Two columns: the homeowner's quick jobs and what the tech handles at the visit.", ["clear", "teamwork", "organized"], "system",
   screen(h1(14, 56, "Fall: Who Does What", 15) + lbl(14, 76, "You do", TERRA) + lbl(122, 76, "We do", LAGOON) + f'<line x1="118" y1="68" x2="118" y2="200" stroke="{LINE}"/>' + "".join(t(14, 94 + i * 18, "· " + a, 7.5, INK) + t(122, 94 + i * 18, "· " + b, 7.5, INK) for i, (a, b) in enumerate([("Outdoor faucets", "Furnace tune-up"), ("Bring in hoses", "Gutters"), ("Swap filter", "CO test"), ("Lint trap", "Water heater"), ("Ceiling fans", "Dryer vent")])) + btn(222, "Start My List"))),
 O("seas_one", "One Combined List With Tags", "A single list; each task carries a small 'You' or 'Danny' tag.", ["simple", "compact", "calm"], "concierge",
   screen(h1(14, 56, "Fall Checklist", 17) + "".join(ln(66 + i * 24) + t(14, 81 + i * 24, n, 8.5, INK) + tag(186, 72 + i * 24, w, TERRA if w == "You" else LAGOON) for i, (n, w) in enumerate([("Furnace tune-up", "Danny"), ("Outdoor faucets", "You"), ("Gutters", "Danny"), ("Swap filter", "You"), ("CO test", "Danny"), ("Lint trap", "You")])))),
 "Split Or One List With Tags?")

# ===================== 7. Emergency shutoff guide (2) =====================
ES = "Up Keep: Emergency Shutoff Guide"
add(GG, ES,
 O("shut_photos", "Shutoffs With Photos Of Your Home", "Each shutoff shows the tech's photo of the actual valve in this house and where it is.", ["specific", "reassuring", "visual"], "neighbor",
   screen(h1(14, 56, "Emergency Shutoffs", 17) + "".join(ln(66 + i * 62) + photo(14, 72 + i * 62, 70, 50, k, 4) + t(94, 88 + i * 62, n, 11, INK, "khand") + t(94, 101 + i * 62, w, 7, MUTE) + link(94, 116 + i * 62, "Show Steps", TERRA, size=6.5) for i, (k, n, w) in enumerate([("label", "Main Water", "Basement, behind the furnace"), ("interior", "Gas", "Outside, left of the meter"), ("label", "Electric Panel", "Garage, north wall")])))),
 O("shut_buttons", "Three Big Emergency Buttons", "Water, Gas, Power as three huge buttons; tap one for steps. Call line at the bottom.", ["urgent", "direct", "fast"], "crew",
   screen(h1(14, 56, "Emergency?", 18) + t(14, 70, "Tap what you need to shut off", 7.5, MUTE) + "".join(rect(14, 80 + i * 50, 212, 42, "#FFFFFF", c, 0, 2) + rect(14, 80 + i * 50, 8, 42, c) + t(34, 107 + i * 50, n, 15, INK, "khand") + t(216, 106 + i * 50, "›", 14, c, anchor="end") for i, (n, c) in enumerate([("Water", LAGOON), ("Gas", SAFFRON), ("Power", TERRA)])) + btn(240, "Call Up Keep Now", col=INK))),
 "How Should The Shutoff Guide Open?")
add(GG, ES,
 O("shut_steps", "Shutoff As Numbered Steps", "Big numbered steps with one small picture per step.", ["guided", "calm", "clear"], "system",
   screen(link(14, 48, "← Shutoffs", INK) + h1(14, 72, "Shut Off The Water", 17) + "".join(rect(14, 82 + i * 52, 22, 22, LAGOON) + t(25, 98 + i * 52, str(i + 1), 13, "#FFFFFF", "khand", anchor="middle") + t(44, 92 + i * 52, a, 9, INK, "hind", 600) + t(44, 104 + i * 52, b, 7, MUTE) + photo(178, 80 + i * 52, 48, 40, "label", 4) for i, (a, b) in enumerate([("Go to the basement", "Behind the furnace, low on the wall"), ("Find the red handle", "On the pipe by the meter"), ("Turn it clockwise", "Until it stops, about 4 turns")])))),
 O("shut_print", "Shutoff As A Printable Card", "A one-page card to print and tape by the panel, with a 'Print' button.", ["practical", "offline", "trusty"], "crew",
   screen(h1(14, 56, "Your Shutoff Card", 17) + rect(24, 66, 192, 150, "#FFFFFF", INK, 0, 1.5) + roof_logo(34, 86, .8) + t(206, 84, "48322", 7, MUTE, anchor="end") + "".join(t(34, 108 + i * 30, n, 10, c, "khand") + t(34, 120 + i * 30, w, 7, INK) for i, (n, w, c) in enumerate([("Water", "Basement, behind furnace · red handle", LAGOON), ("Gas", "Outside left of meter · 1/4 turn", SAFFRON), ("Power", "Garage panel · main breaker top", TERRA)])) + btn(230, "Print My Card", "outline"))),
 "Steps On Screen Or A Printable Card?")

# ===================== 8. My tech profile card (2) =====================
MT = "Up Keep: My Tech Profile"
add(GT, MT,
 O("tech_big", "Big Photo Profile", "A large photo of Danny, his name, years with Up Keep and two buttons.", ["personal", "warm", "human"], "neighbor",
   screen(photo(14, 42, 212, 120, "tech", 8, "warm") + h1(14, 184, "Danny Reyes", 18) + t(14, 198, "Your tech since Oct 2025 · 8 years in HVAC", 7.5, MUTE) + tag(14, 206, "EPA Certified", LAGOON) + tag(84, 206, "Background Checked", JUNGLE) + btn(232, "Text Danny", "outline", w=100, size=8) + btn(232, "Call", "outline", x=126, w=100, size=8))),
 O("tech_compact", "Compact ID Card", "A small badge-style card: round photo, name, license number and rating.", ["system", "credible", "compact"], "system",
   screen(h1(14, 56, "My Tech", 17) + rect(14, 66, 212, 96, "#FFFFFF", INK, 6, 1.5) + rect(14, 66, 212, 18, INK, r=0) + t(22, 78, "UP KEEP TECHNICIAN", 6.5, "#FFFFFF", "hind", 600, extra='letter-spacing="1"') + face(46, 114, 14) + t(74, 108, "Danny Reyes", 13, INK, "khand") + t(74, 121, "MI License 71-04429", 7, MUTE) + t(74, 134, "★ 4.9 · 212 visits", 7.5, SAFFRON, "hind", 600) + rows(176, [("Visits at your home", "5"), ("Next visit", "Feb 3")]))),
 "How Should The 'My Tech' Card Look?")
add(GT, MT,
 O("tech_facts", "Tech Card With Fun Facts", "Adds a line about Danny: 'Dad of two, coaches Little League, loves old Fords.'", ["friendly", "human", "warm"], "neighbor",
   screen(face(120, 78, 22) + h1(120, 136, "Meet Danny", 18, anchor="middle") + para(30, 156, ["Dad of two, coaches Little League", "in Novi and restores old Fords.", "Fixing furnaces for 8 years."], 8, INK, 12) + btn(214, "Say Hi To Danny", "outline"))),
 O("tech_skills", "Tech Card With Skills", "Lists Danny's skills and certifications as tags, no personal details.", ["professional", "credible", "clear"], "crew",
   screen(face(120, 78, 22) + h1(120, 136, "Danny Reyes", 18, anchor="middle") + t(120, 150, "Lead technician · Novi", 7.5, MUTE, anchor="middle") + "".join(tag(x, y, s, c) for x, y, s, c in [(30, 166, "HVAC", LAGOON), (66, 166, "Plumbing", LAGOON), (120, 166, "EPA 608", JUNGLE), (170, 166, "Gas Safe", JUNGLE), (60, 184, "Electrical Basics", LAGOON), (146, 184, "CO Testing", JUNGLE)]) + btn(214, "Text Danny", "outline"))),
 "Personal Or Professional Tech Card?")

# ===================== 9. In-app chat vs call (2) =====================
CH = "Up Keep: Contact Options"
add(GT, CH,
 O("con_chatfirst", "Chat Opens First", "Help opens straight into a chat thread with a 'Call' link in the header.", ["modern", "easy", "async"], "system",
   screen(h1(14, 56, "Help", 17) + link(226, 56, "Call", TERRA, "end") + rect(14, 70, 160, 34, "#F2F2F2", r=10) + para(22, 84, ["Hi Sarah, it's Max. What can", "we help with?"], 7.8, INK, 10) + rect(80, 112, 146, 22, LAGOON, r=10) + t(88, 126, "My furnace is making a click", 7.8, "#FFFFFF") + rect(14, 142, 170, 34, "#F2F2F2", r=10) + para(22, 156, ["Thanks! Can you send a short", "video? Danny will take a look."], 7.8, INK, 10) + rect(14, 268, 212, 22, "#FFFFFF", "#D4D4D4", 11) + t(24, 282, "Message", 7.5, "#A3A3A3"))),
 O("con_choice", "Pick: Chat Or Call", "Two big buttons with the wait time for each: 'Chat · replies in 5 min', 'Call · 1 min'.", ["clear", "choice", "honest"], "crew",
   screen(h1(14, 60, "How Can We Help?", 17) + rect(14, 74, 212, 64, "#FFFFFF", LINE, 6) + icon("chat", 24, 92, 28, "duo", LAGOON) + t(62, 102, "Chat With Us", 12, INK, "khand") + t(62, 116, "Replies in about 5 min", 7.5, MUTE) + rect(14, 146, 212, 64, "#FFFFFF", LINE, 6) + icon("phone", 24, 164, 28, "duo", TERRA) + t(62, 174, "Call Us", 12, INK, "khand") + t(62, 188, "Answered in about 1 min", 7.5, MUTE) + t(120, 236, "8 AM to 8 PM · emergencies 24/7", 7, MUTE, anchor="middle"))),
 "How Should Members Reach Us?")
add(GT, CH,
 O("con_fab", "Floating Help Button", "A round chat button floats in the corner of every screen.", ["always-there", "modern", "light"], "system",
   screen(HOMEBODY + f'<circle cx="204" cy="244" r="17" fill="{LAGOON}"/>' + icon("chat", 194, 234, 20, "outline").replace(INK, "#FFFFFF") + tabbar(0))),
 O("con_tab", "Help As Its Own Tab", "A 'Help' tab in the bottom bar with chat, call and FAQs inside.", ["organized", "calm", "clear"], "concierge",
   screen(h1(14, 56, "Help", 17) + rows(66, [("Chat with us", "› 5 min"), ("Call us", "› 1 min"), ("Text Danny", "›"), ("Common questions", "›")], 32) + f'<rect x="0" y="266" width="{W}" height="34" fill="#FFFFFF"/>' + ln(266, 0, W) + "".join(rect(24 + i * 48 - 6, 273, 12, 10, "none", INK if i == 4 else "#A3A3A3", 2, 1.4) + t(24 + i * 48, 293, n, 6, INK if i == 4 else "#A3A3A3", "hind", 600, "middle") for i, n in enumerate(["Home", "Calendar", "Record", "Invite", "Help"])))),
 "Floating Help Button Or A Help Tab?")
# ===================== 10. Invoice / receipt look (2) =====================
IV = "Up Keep: Invoice And Receipt"
add(GBL, IV,
 O("inv_lines", "Itemized Receipt", "Each line item with a price, member discount and a total. Classic and exact.", ["exact", "transparent", "system"], "system",
   screen(roof_logo(14, 52) + t(226, 52, "#UK-10482", 7, MUTE, anchor="end") + h1(14, 76, "Receipt", 17) + t(14, 90, "Nov 4, 2026 · Danny Reyes", 7.5, MUTE) + rows(98, [("Fall visit (Gold)", "Included"), ("Dryer vent clean", "$129.00"), ("Member discount 15%", "−$19.35"), ("Tax", "$6.21")], 22) + f'<line x1="14" y1="190" x2="226" y2="190" stroke="{INK}" stroke-width="1.5"/>' + t(14, 208, "Total", 11, INK, "khand") + t(226, 208, "$115.86", 13, INK, "khand", anchor="end") + tag(14, 220, "Paid · Visa 4242", JUNGLE) + btn(244, "Download PDF", "outline"), head=False)),
 O("inv_summary", "Summary Receipt", "One big total and 'Paid' stamp; line items fold under 'See Details'.", ["simple", "calm", "clean"], "concierge",
   screen(roof_logo(14, 52) + t(120, 120, "$115.86", 34, INK, "khand", anchor="middle") + t(120, 138, "Paid Nov 4 · Visa 4242", 8, MUTE, anchor="middle") + rect(80, 150, 80, 20, "none", JUNGLE, 4, 1.6) + t(120, 164, "PAID", 9, JUNGLE, "hind", 600, "middle", 'letter-spacing="2"') + t(120, 192, "Dryer vent clean · you saved $19.35", 7.5, INK, anchor="middle") + link(120, 214, "See Details", LAGOON, "middle") + btn(240, "Download PDF", "outline"), head=False)),
 "How Should A Receipt Look?")
add(GBL, IV,
 O("inv_savings", "Receipt Shows Member Savings", "A green box: 'You've saved $412 this year' on every receipt.", ["value", "lively", "reassuring"], "neighbor",
   screen(h1(14, 56, "Receipt · Nov 4", 15) + rows(66, [("Dryer vent clean", "$129.00"), ("Member discount", "−$19.35"), ("Total paid", "$115.86")]) + rect(14, 148, 212, 58, JUNGLE + "14", JUNGLE, 6) + t(24, 168, "You've Saved $412 This Year", 12, JUNGLE, "khand") + t(24, 182, "On repairs and add-ons as a Gold member", 7.2, INK) + t(24, 195, "Visits included: 4 of 4 used", 7.2, MUTE))),
 O("inv_plain", "Receipt Without Savings", "Just the work, the price and the payment. No savings pitch.", ["honest", "plain", "direct"], "crew",
   screen(h1(14, 56, "Receipt · Nov 4", 15) + rows(66, [("Dryer vent clean", "$129.00"), ("Member discount", "−$19.35"), ("Total paid", "$115.86"), ("Paid with", "Visa 4242")]) + btn(180, "Download PDF", "outline") + link(120, 228, "Questions About This Bill?", LAGOON, "middle"))),
 "Show Savings On Receipts?")

# ===================== 11. Membership card + renewal (2) =====================
MB = "Up Keep: Membership Card"
add(GBL, MB,
 O("mem_wallet", "Wallet-Style Member Card", "A dark card like a credit card: name, plan, member since, a QR for the tech.", ["premium", "bold", "tangible"], "concierge",
   screen(h1(14, 56, "My Membership", 17) + rect(14, 68, 212, 128, INK, r=10) + roof_logo(26, 92, 1, "#FFFFFF", TERRA) + rect(160, 80, 54, 54, "#FFFFFF", r=4) + qr(164, 84, 46) + t(26, 156, "SARAH MILLER", 9, "#FFFFFF", "hind", 600, extra='letter-spacing="1.5"') + t(26, 172, "Gold · since Oct 2025", 7.5, "#BDBDBD") + rect(26, 178, 30, 3, TERRA) + btn(212, "Add To Apple Wallet", "outline"))),
 O("mem_light", "Light Member Card", "A white card with a terracotta edge, plan, renewal date and what's left this year.", ["clear", "light", "system"], "system",
   screen(h1(14, 56, "My Membership", 17) + rect(14, 68, 212, 128, "#FFFFFF", LINE, 10) + rect(14, 68, 6, 128, TERRA) + t(30, 92, "Gold Membership", 14, INK, "khand") + t(30, 106, "Sarah Miller · since Oct 2025", 7.5, MUTE) + "".join(ln(116 + i * 24, 30, 214) + t(30, 131 + i * 24, a, 8.5, INK) + t(214, 131 + i * 24, b, 7.5, MUTE, anchor="end") for i, (a, b) in enumerate([("Renews", "Oct 8, 2027"), ("Visits left", "3 of 4"), ("Plan", "$232 / month")])) + btn(212, "Manage Plan", "outline"))),
 "How Should The Membership Card Look?")
add(GBL, "Up Keep: Renewal",
 O("renew_auto", "Renewal: Auto-Renews, Heads-Up", "'Renews Oct 8. Nothing to do.' with a summary of the year and a Change link.", ["easy", "calm", "automatic"], "system",
   screen(h1(14, 60, "Your Plan Renews Oct 8", 15) + t(14, 76, "Nothing to do. Here's your year:", 8, MUTE) + "".join(rect(14 + i * 72, 86, 68, 50, CREAM, LINE, 4) + t(48 + i * 72, 110, v, 15, INK, "khand", anchor="middle") + t(48 + i * 72, 126, l, 6.3, MUTE, "hind", 600, "middle") for i, (v, l) in enumerate([("4", "VISITS"), ("38", "CHECKS"), ("$412", "SAVED")])) + rows(150, [("Next year", "$232 / month"), ("Same tech", "Danny")]) + link(14, 222, "Change Or Cancel", LAGOON))),
 O("renew_ask", "Renewal: Ask To Renew", "'Ready for year two?' with a big Renew button and a small 'Not Now'.", ["personal", "warm", "deliberate"], "neighbor",
   screen(gift(96, 54, TERRA, 2) + h1(120, 136, "Ready For Year Two, Sarah?", 16, anchor="middle") + t(120, 152, "4 visits, 38 checks, $412 saved this year", 7.5, MUTE, anchor="middle") + btn(174, "Renew Gold", col=TERRA) + link(120, 222, "Not Now", MUTE, "middle"))),
 "Auto-Renew Notice Or Ask To Renew?")

# ===================== 12. Plan upgrade prompt (2) =====================
UP = "Up Keep: Plan Upgrade Prompt"
add(GBL, UP,
 O("upg_compare", "Upgrade As A Side-By-Side", "Gold vs Platinum columns with what you'd add, and one 'Switch' button.", ["clear", "comparable", "system"], "system",
   screen(h1(14, 56, "Get More With Platinum", 15) + tiercard(14, 70, 104, 130, "Gold", "$232", "/mo", ["4 visits", "Report", "15% off"]) + tiercard(122, 70, 104, 130, "Platinum", "$398", "/mo", ["6 visits", "Report", "25% off", "Windows", "Priority"], True, "You'd Add", acc=LAGOON) + btn(218, "Switch To Platinum"))),
 O("upg_nudge", "Upgrade As A Small Nudge", "A one-line card in the report: 'Add window washing for $19/mo?' with Add.", ["gentle", "contextual", "light"], "neighbor",
   screen(h1(14, 56, "Fall Visit Report", 17) + rows(66, [("11 checks done", "✓"), ("1 to watch", "Dryer vent")]) + rect(14, 130, 212, 54, CREAM, LINE, 6) + photo(22, 138, 38, 38, "house", 4) + t(68, 152, "Windows Looking Dusty?", 10, INK, "khand") + t(68, 165, "Add washing for $19/mo", 7.3, MUTE) + btn(144, "Add", col=TERRA, x=178, w=40, h=20, size=7) + btn(236, "See Photos", "outline"))),
 "Big Comparison Or Small Nudge?")
add(GBL, UP,
 O("upg_value", "Upgrade Leads With Savings", "'Platinum would have saved you $186 this year.' Based on their real bills.", ["data", "persuasive", "personal"], "crew",
   screen(t(120, 104, "$186", 40, JUNGLE, "khand", anchor="middle") + h1(120, 132, "More Saved On Platinum", 15, anchor="middle") + t(120, 148, "Based on your repairs this year", 7.5, MUTE, anchor="middle") + rows(162, [("25% vs 15% off repairs", "+$96"), ("Window washing included", "+$90")]) + btn(222, "See Platinum"))),
 O("upg_perks", "Upgrade Leads With Perks", "Three icons: more visits, priority booking, windows included.", ["visual", "warm", "lively"], "neighbor",
   screen(h1(120, 64, "Platinum Adds", 17, anchor="middle") + "".join(rect(14 + i * 72, 78, 68, 82, "#FFFFFF", LINE, 6) + dot(48 + i * 72, 104, 13, c + "22") + dot(48 + i * 72, 104, 5, c) + t(48 + i * 72, 134, a, 8, INK, "hind", 600, "middle") + t(48 + i * 72, 146, b, 6.5, MUTE, anchor="middle") for i, (a, b, c) in enumerate([("6 Visits", "2 more", TERRA), ("Priority", "First pick", LAGOON), ("Windows", "Twice a year", JUNGLE)])) + t(120, 186, "$166 more a month", 9, INK, "hind", 600, "middle") + btn(222, "See Platinum"))),
 "What Should An Upgrade Prompt Lead With?")

# ===================== 13. Multi-home / landlord view (2) =====================
MH = "Up Keep: Multi-Home View"
HOMES = [("412 Maple St", "Rental · 2 tenants", 92, JUNGLE, "OK"), ("88 Elm Ct", "Rental · vacant", 71, SAFFRON, "2 due"), ("15 Lake Dr", "My home", 88, JUNGLE, "OK")]
add(GLL, MH,
 O("mh_list", "Homes As A List", "One row per property with score, next visit and a status tag.", ["clear", "compact", "system"], "system",
   screen(h1(14, 56, "My Properties", 17) + t(14, 70, "3 homes · 1 needs attention", 7.5, MUTE) + "".join(ln(80 + i * 46) + ring(32, 103 + i * 46, 13, s / 100, c, "") + t(32, 107 + i * 46, str(s), 9, INK, "khand", anchor="middle") + t(54, 99 + i * 46, a, 9, INK, "hind", 600) + t(54, 111 + i * 46, n, 7, MUTE) + tag(180, 96 + i * 46, st, c) for i, (a, n, s, c, st) in enumerate(HOMES)) + btn(236, "Add A Property", "outline"))),
 O("mh_cards", "Homes As Photo Cards", "A photo card per property, swipe sideways between them.", ["visual", "warm", "lively"], "neighbor",
   screen(h1(14, 56, "My Properties", 17) + rect(14, 66, 180, 170, "#FFFFFF", LINE, 8) + photo(22, 74, 164, 90, "house", 6) + t(22, 184, "412 Maple St", 12, INK, "khand") + t(22, 198, "Rental · next visit Nov 6", 7.3, MUTE) + tag(22, 208, "Health 92", JUNGLE) + rect(200, 66, 40, 170, "#FFFFFF", LINE, 8) + photo(206, 74, 40, 90, "house", 6, "warm") + dots(252, 3, 0))),
 "How Should Several Homes Be Shown?")
add(GLL, MH,
 O("mh_switch", "Home Switcher In The Header", "Same single-home app; a dropdown at the top switches between properties.", ["simple", "familiar", "calm"], "concierge",
   screen(rect(14, 40, 140, 22, "#FFFFFF", "#CFC8BC", 0) + t(22, 55, "412 Maple St", 8.5, INK, "hind", 600) + t(146, 55, "▾", 8, MUTE, anchor="end") + h1(14, 84, "Welcome Back", 16) + rect(14, 94, 212, 50, CREAM, LINE, 6) + t(22, 112, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(22, 130, "Thu, Nov 6 · 1 PM", 13, INK, "khand") + rows(154, [("Furnace", "OK"), ("Water heater", "OK"), ("Tenant access", "Confirmed")]) + tabbar(0), head=False)),
 O("mh_rollup", "Portfolio Roll-Up", "One summary for all homes: visits this month, open issues, spend, then a list.", ["data", "control", "pro"], "crew",
   screen(h1(14, 56, "All Properties", 17) + "".join(rect(14 + i * 72, 66, 68, 50, "#FFFFFF", LINE, 4) + rect(14 + i * 72, 66, 68, 3, c) + t(48 + i * 72, 92, v, 14, INK, "khand", anchor="middle") + t(48 + i * 72, 106, l, 6, MUTE, "hind", 600, "middle") for i, (v, l, c) in enumerate([("3", "VISITS NOV", LAGOON), ("2", "OPEN ISSUES", SAFFRON), ("$1.2k", "SPENT YTD", TERRA)])) + rows(128, [(a, st) for a, n, s, c, st in HOMES], 26) + btn(236, "Export For Taxes", "outline"))),
 "Switch Between Homes Or See Them All At Once?")
# ===================== 14. Marketing site hero + sections (2) =====================
MK = "Up Keep: Marketing Site"
add(GMK, MK,
 O("hero_photo", "Hero With A Real Home Photo", "A big photo of a tech at a front door, headline over white space beneath, one button.", ["warm", "human", "trust"], "neighbor",
   screen(photo(0, 32, W, 120, "tech", 0, "warm") + h1(14, 178, "Your Home, Looked After", 18) + para(14, 194, ["Four visits a year from the same tech.", "Metro Detroit · from $99 a month."], 8, MUTE, 11) + btn(230, "See My Price", col=TERRA))),
 O("hero_type", "Hero With Big Type Only", "No photo: a huge Khand headline, a price line and a button on white.", ["bold", "modern", "confident"], "system",
   screen(t(14, 90, "Home Care", 34, INK, "khand") + t(14, 124, "On Schedule.", 34, TERRA, "khand") + para(14, 146, ["Four visits a year, one tech, a written", "report every time. From $99 a month."], 8.5, MUTE, 12) + btn(186, "See My Price") + "".join(tag(14 + i * 72, 226, s, c) for i, (s, c) in enumerate([("Recall Alerts", LAGOON), ("Same Tech", JUNGLE), ("Cancel Anytime", MUTE)])))),
 "Which Marketing Site Hero?")
add(GMK, MK,
 O("sec_icons", "Sections As Icon Rows", "'What you get' as icon rows: a colored icon, a short title and one line.", ["clear", "scannable", "lively"], "system",
   screen(lbl(14, 50, "What you get") + h1(14, 70, "Everything, Every Season", 16) + "".join(ln(80 + i * 40) + icon(k, 14, 88 + i * 40, 22, "duo", c) + t(46, 98 + i * 40, a, 9.5, INK, "hind", 600) + t(46, 110 + i * 40, b, 7, MUTE) for i, (k, a, b, c) in enumerate([("furnace", "Seasonal Tune-Ups", "Furnace, AC, water heater", TERRA), ("check", "A Report Every Visit", "Photos and a checklist", JUNGLE), ("smoke", "Recall Tracking", "We watch your models", LAGOON), ("phone", "One Tech, One Number", "Text Danny anytime", SAFFRON)])))),
 O("sec_story", "Sections As A Story", "Big numbered sections: 1 We Visit, 2 We Report, 3 We Remember, each with a photo.", ["story", "warm", "editorial"], "neighbor",
   screen("".join(t(14, 76 + i * 76, f"0{i+1}", 26, c, "khand") + t(52, 66 + i * 76, a, 13, INK, "khand") + para(52, 80 + i * 76, b, 7.3, MUTE, 10) + photo(168, 46 + i * 76, 58, 58, k, 4) for i, (a, b, k, c) in enumerate([("We Visit", ["Four times a year,", "same tech."], "tech", TERRA), ("We Report", ["Photos and a checklist", "after every visit."], "label", LAGOON), ("We Remember", ["Models, warranties,", "recalls, all saved."], "interior", JUNGLE)])))),
 "How Should Site Sections Be Laid Out?")

# ===================== 15. Social post + yard sign (2) =====================
SP = "Up Keep: Social And Yard Sign"
add(GMK, SP,
 O("soc_tip", "Social Post: Seasonal Tip Card", "A square post: 'Fall Tip #3: Shut off your outdoor faucets' on cream with a small drawing.", ["helpful", "warm", "brand"], "neighbor",
   screen(rect(20, 30, 200, 200, CREAM, LINE, 4) + lbl(34, 54, "Fall tip #3", TERRA) + t(34, 82, "Shut Off Your", 20, INK, "khand") + t(34, 104, "Outdoor Faucets", 20, INK, "khand") + house_ill(66, 112, .6, INK, TERRA, LAGOON + "55") + roof_logo(34, 216, .8) + t(206, 216, "@upkeepdetroit", 7, MUTE, anchor="end") + t(120, 254, "Instagram · 1,240 likes", 7, MUTE, anchor="middle"), head=False)),
 O("soc_ba", "Social Post: Before / After", "A square post split in two: dirty gutter vs clean, with 'Same Day.' in big type.", ["proof", "bold", "lively"], "crew",
   screen(photo(20, 30, 100, 200, "house", 0, "mute") + photo(120, 30, 100, 200, "house", 0, "day") + rect(20, 186, 200, 44, INK) + t(34, 214, "Same Day.", 18, "#FFFFFF", "khand") + roof_logo(150, 214, .7, "#FFFFFF", TERRA) + tag(26, 38, "Before", MUTE, True) + tag(184, 38, "After", JUNGLE, True) + t(120, 254, "Instagram · 1,240 likes", 7, MUTE, anchor="middle"), head=False)),
 "Which Social Post Style?")
add(GMK, SP,
 O("yard_white", "Yard Sign: White With Black Logo", "A white sign, big black logo, a terracotta 'Cared For By' line and a URL.", ["clean", "classy", "readable"], "concierge",
   screen(rect(0, 0, W, H, "#D9E6EE") + rect(0, 220, W, 80, "#9DB58A") + rect(36, 60, 168, 120, "#FFFFFF", "#BDB6AA", 2) + t(120, 88, "CARED FOR BY", 8, TERRA, "hind", 600, "middle", 'letter-spacing="2"') + roof_logo(64, 124, 1.6) + t(120, 160, "upkeep.app", 9, MUTE, anchor="middle") + rect(70, 180, 4, 60, "#6E6E6E") + rect(166, 180, 4, 60, "#6E6E6E"), head=False)),
 O("yard_color", "Yard Sign: Terracotta Field", "A solid terracotta sign with a white logo and a short 'Ask Us About Your Home' line.", ["bold", "visible", "warm"], "neighbor",
   screen(rect(0, 0, W, H, "#D9E6EE") + rect(0, 220, W, 80, "#9DB58A") + rect(36, 60, 168, 120, TERRA, r=2) + roof_logo(64, 110, 1.6, "#FFFFFF", INK) + t(120, 138, "Ask Us About Your Home", 9, "#FFFFFF", "hind", 600, "middle") + t(120, 160, "upkeep.app", 9, "#FFFFFF", anchor="middle") + rect(70, 180, 4, 60, "#6E6E6E") + rect(166, 180, 4, 60, "#6E6E6E"), head=False)),
 "Which Yard Sign?")

# ===================== 16. Truck + uniform branding (2) =====================
TB = "Up Keep: Truck And Uniform"
add(GFB, TB,
 O("truck_stripe", "White Van, Terracotta Stripe", "A white van with a thin terracotta stripe and black logo on the side.", ["clean", "warm", "recognizable"], "neighbor",
   screen(rect(0, 0, W, H, "#EEF0EA") + rect(0, 200, W, 100, "#C9C9C4") + van(30, 130, 1.2) + t(120, 250, "Side view · white with one stripe", 7.5, MUTE, anchor="middle"), head=False)),
 O("truck_black", "White Van, Big Black Logo Only", "No stripe: a large black logo and phone number. Quiet and confident.", ["minimal", "confident", "quiet"], "concierge",
   screen(rect(0, 0, W, H, "#EEF0EA") + rect(0, 200, W, 100, "#C9C9C4") + van(30, 130, 1.2, stripe=None) + t(54, 176, "(248) 555-0190", 8, INK, "hind", 600) + t(120, 250, "Side view · logo and number only", 7.5, MUTE, anchor="middle"), head=False)),
 "Which Van Side?")
def polo(col, logo_c, up_c, collar):
    return (f'<path d="M70 70 L100 56 Q120 70 140 56 L170 70 L196 104 L172 118 L164 106 V240 H76 V106 L68 118 L44 104 Z" fill="{col}" stroke="#6E6E6E" stroke-width="1"/><path d="M100 56 L120 82 L140 56" fill="none" stroke="{collar}" stroke-width="3"/>' + roof_logo(116, 122, .7, logo_c, up_c))
add(GFB, TB,
 O("polo_white", "White Polo, Black Logo", "A white polo with a small black logo on the chest and a terracotta collar tip.", ["clean", "friendly", "light"], "neighbor",
   screen(rect(0, 0, W, H, "#F4F1EA") + polo("#FFFFFF", INK, TERRA, TERRA) + t(120, 268, "Tech polo · white", 7.5, MUTE, anchor="middle"), head=False)),
 O("polo_black", "Black Polo, White Logo", "A black polo with a white logo and a terracotta 'up'.", ["sharp", "pro", "bold"], "crew",
   screen(rect(0, 0, W, H, "#F4F1EA") + polo(INK, "#FFFFFF", TERRA, "#2B2B2B") + t(120, 268, "Tech polo · black", 7.5, MUTE, anchor="middle"), head=False)),
 "Which Tech Polo?")

# ===================== 17. Fridge magnet / sticker on systems (2) =====================
ST = "Up Keep: Magnet And System Sticker"
add(GFB, ST,
 O("stk_round", "Round Sticker With Next Service", "A round sticker on the furnace: logo, 'Next service: Feb', and a number.", ["friendly", "compact", "visual"], "neighbor",
   screen(photo(0, 32, W, 268, "label", 0) + f'<circle cx="120" cy="150" r="66" fill="#FFFFFF" stroke="{TERRA}" stroke-width="5"/>' + roof_logo(90, 130, 1.1) + t(120, 154, "NEXT SERVICE", 6.5, MUTE, "hind", 600, "middle", 'letter-spacing="1"') + t(120, 174, "February", 16, INK, "khand", anchor="middle") + t(120, 192, "(248) 555-0190", 7.5, TERRA, "hind", 600, "middle"), head=False)),
 O("stk_log", "Service Log Sticker", "A rectangular sticker with a small table: date and tech initials for each visit.", ["record", "practical", "system"], "system",
   screen(photo(0, 32, W, 268, "label", 0) + rect(40, 76, 160, 150, "#FFFFFF", INK, 2, 1.5) + rect(40, 76, 160, 22, INK) + roof_logo(50, 92, .8, "#FFFFFF", TERRA) + t(190, 91, "SERVICE LOG", 6, "#FFFFFF", "hind", 600, "end") + "".join(f'<line x1="48" y1="{116+i*20}" x2="192" y2="{116+i*20}" stroke="#BDB6AA"/>' + t(50, 112 + i * 20, d, 8, INK) + t(190, 112 + i * 20, w, 8, MUTE, anchor="end") for i, (d, w) in enumerate([("Oct 8, 2025", "DR"), ("Feb 3, 2026", "DR"), ("Nov 4, 2026", "DR"), ("", ""), ("", "")])), head=False)),
 "Which Sticker On The Furnace?")
add(GFB, ST,
 O("mag_emergency", "Fridge Magnet: Emergency Numbers", "A fridge magnet with the shutoff spots and a 24/7 number.", ["practical", "safety", "useful"], "crew",
   screen(rect(0, 0, W, H, "#E9E7E3") + rect(46, 50, 148, 200, "#FFFFFF", "#BDB6AA", 10) + roof_logo(64, 80, 1) + t(64, 104, "IN AN EMERGENCY", 6.5, TERRA, "hind", 600, extra='letter-spacing="1"') + t(64, 128, "(248) 555-0190", 13, INK, "khand") + "".join(dot(68, 150 + i * 22, 4, c) + t(78, 153 + i * 22, s, 7.3, INK) for i, (s, c) in enumerate([("Water: basement", LAGOON), ("Gas: by the meter", SAFFRON), ("Power: garage", TERRA)])) + t(120, 232, "24/7 for members", 6.5, MUTE, anchor="middle"), head=False)),
 O("mag_calendar", "Fridge Magnet: Year Of Visits", "A magnet showing the four visit months and a QR to the app.", ["planned", "visual", "calm"], "system",
   screen(rect(0, 0, W, H, "#E9E7E3") + rect(46, 50, 148, 200, "#FFFFFF", "#BDB6AA", 10) + roof_logo(64, 80, 1) + t(64, 104, "YOUR VISITS", 6.5, LAGOON, "hind", 600, extra='letter-spacing="1"') + "".join(rect(64 + (i % 2) * 58, 114 + (i // 2) * 34, 52, 28, CREAM, LINE, 4) + t(90 + (i % 2) * 58, 132 + (i // 2) * 34, m, 9, INK, "khand", anchor="middle") for i, m in enumerate(["Feb", "May", "Aug", "Nov"])) + qr(100, 190, 40), head=False)),
 "Which Fridge Magnet?")

# ===================== 18. QR on equipment label (2) =====================
QR = "Up Keep: Equipment QR Label"
add(GFB, QR,
 O("qr_big", "Big QR, Few Words", "A label that is mostly QR code with 'Scan For History' under it.", ["minimal", "modern", "clean"], "concierge",
   screen(photo(0, 32, W, 268, "label", 0) + rect(60, 70, 120, 160, "#FFFFFF", "#9E9E9E", 4) + qr(76, 84, 88) + t(120, 196, "Scan For History", 10, INK, "khand", anchor="middle") + roof_logo(92, 218, .6), head=False)),
 O("qr_info", "Small QR With Key Facts", "A wider label: model, install year, filter size on the left, small QR on the right.", ["useful", "readable", "system"], "system",
   screen(photo(0, 32, W, 268, "label", 0) + rect(20, 100, 200, 100, "#FFFFFF", "#9E9E9E", 4) + rect(20, 100, 200, 16, INK) + roof_logo(28, 112, .55, "#FFFFFF", TERRA) + t(212, 111, "FURNACE", 6, "#FFFFFF", "hind", 600, "end") + "".join(t(28, 134 + i * 14, a, 6.5, MUTE) + t(70, 134 + i * 14, b, 7.5, INK, "hind", 600) for i, (a, b) in enumerate([("Model", "Carrier 59SC5"), ("Installed", "2019"), ("Filter", "16x25x1"), ("Next", "Feb 3")])) + qr(158, 124, 52), head=False)),
 "Which QR Label On Equipment?")
add(GFB, QR,
 O("qr_scan_page", "Scan Opens The System Page", "Scanning the QR opens that system's page right away, with Book A Visit.", ["direct", "fast", "system"], "system",
   screen(lbl(14, 48, "Scanned · furnace") + h1(14, 70, "Carrier 59SC5 Furnace", 15) + t(14, 84, "Installed 2019 · filter 16x25x1", 7.5, MUTE) + rows(94, [("Last service", "Nov 4 · Danny"), ("Next service", "Feb 3"), ("Warranty", "Until 2032"), ("Recalls", "None")]) + btn(206, "Book A Visit", col=TERRA) + btn(238, "Report A Problem", "outline"))),
 O("qr_scan_help", "Scan Opens 'What's Wrong?'", "Scanning opens a quick help menu: Strange Noise, No Heat, Leak, Just Checking.", ["helpful", "guided", "warm"], "neighbor",
   screen(lbl(14, 48, "Scanned · furnace") + h1(14, 70, "What's Going On?", 17) + "".join(rect(14 + (i % 2) * 108, 82 + (i // 2) * 62, 104, 56, "#FFFFFF", LINE, 6) + dot(30 + (i % 2) * 108, 102 + (i // 2) * 62, 6, c) + t(22 + (i % 2) * 108, 126 + (i // 2) * 62, s, 9, INK, "hind", 600) for i, (s, c) in enumerate([("Strange Noise", SAFFRON), ("No Heat", TERRA), ("A Leak", LAGOON), ("Just Checking", JUNGLE)])) + link(120, 222, "Text Danny Instead", LAGOON, "middle"))),
 "What Should Scanning The QR Open?")
# ===================== 19. Onboarding welcome (2) =====================
OB = "Up Keep: Onboarding Welcome"
add(GON, OB,
 O("wel_letter", "Welcome Note From Max", "A short welcome note signed by Max, then 'Meet Your Tech'.", ["personal", "warm", "human"], "neighbor",
   screen(h1(14, 60, "Welcome To Up Keep", 17) + rect(14, 72, 212, 122, CREAM, LINE, 6) + para(24, 92, ["Hi Sarah,", "", "Thanks for trusting us with your home.", "Danny will be your tech; you'll see the", "same face every visit. Text me anytime.", "", "Max, founder"], 8, INK, 12) + btn(208, "Meet Your Tech"))),
 O("wel_checklist", "Welcome Setup Checklist", "A 4-item setup list: Book First Visit, Snap Labels, Add Calendar, Set Reminders.", ["guided", "system", "clear"], "system",
   screen(h1(14, 60, "Let's Get You Set Up", 17) + t(226, 60, "1 of 4", 8, JUNGLE, "hind", 600, "end") + pbar(68, .25, JUNGLE) + "".join(ln(82 + i * 34) + icon("check", 14, 90 + i * 34, 16, "duo", JUNGLE if i == 0 else "#BDB6AA") + t(38, 102 + i * 34, n, 9, MUTE if i == 0 else INK, "hind", 600) + t(226, 102 + i * 34, "" if i == 0 else "›", 10, MUTE, anchor="end") for i, n in enumerate(["Book your first visit", "Snap your equipment labels", "Add visits to your calendar", "Pick your reminders"])) + btn(232, "Snap Labels Next", col=TERRA))),
 "How Should A New Member Be Welcomed?")
add(GON, OB,
 O("wel_tour", "Three-Screen Tour", "Swipe through 3 screens: Your Tech, Your Record, Your Calendar. Skip any time.", ["guided", "visual", "lively"], "neighbor",
   screen(link(226, 48, "Skip", MUTE, "end") + house_ill(30, 70, 1, INK, TERRA, LAGOON + "55", SAFFRON) + h1(120, 206, "Everything About Your Home", 15, anchor="middle") + t(120, 222, "Models, reports and warranties in one place.", 7.5, MUTE, anchor="middle") + dots(240, 3, 1) + btn(258, "Next", h=24))),
 O("wel_straight", "Straight To The Dashboard", "No tour. The dashboard opens with a one-time banner: 'Welcome! Start here.'", ["fast", "minimal", "direct"], "crew",
   screen(rect(14, 40, 212, 30, JUNGLE + "14", JUNGLE, 4) + t(22, 59, "Welcome, Sarah! Start with your first visit.", 7.5, INK, "hind", 600) + t(218, 59, "✕", 8, MUTE, anchor="end") + h1(14, 92, "Welcome Home", 16) + rect(14, 102, 212, 50, CREAM, LINE, 6) + t(22, 120, "NO VISIT BOOKED YET", 6.5, MUTE, "hind", 600) + link(22, 138, "Book Now", TERRA) + rows(162, [("Furnace", "Add label"), ("Water heater", "Add label")]) + tabbar(0), head=False)),
 "Tour First Or Straight In?")

# ===================== 20. Notification preferences (2) =====================
NP = "Up Keep: Notification Preferences"
add(GON, NP,
 O("np_matrix", "Grid: Type By Channel", "Rows of message types, columns for Text, Push and Email, a tick in each cell.", ["control", "detailed", "system"], "system",
   screen(h1(14, 56, "Notifications", 17) + "".join(t(150 + i * 30, 78, c, 6.5, MUTE, "hind", 600, "middle") for i, c in enumerate(["TEXT", "PUSH", "EMAIL"])) + "".join(ln(84 + r * 28) + t(14, 102 + r * 28, n, 8.3, INK) + "".join(check_box(144 + i * 30, 92 + r * 28, v[i], LAGOON) for i in range(3)) for r, (n, v) in enumerate([("Visit reminders", (1, 1, 0)), ("Tech on the way", (1, 1, 0)), ("Reports ready", (0, 1, 1)), ("Recalls", (1, 1, 1)), ("Offers", (0, 0, 1))])))),
 O("np_quiet", "Quiet Hours And One Channel", "Pick one main channel and quiet hours. Everything else follows.", ["simple", "calm", "respectful"], "concierge",
   screen(h1(14, 56, "Notifications", 17) + lbl(14, 80, "Reach me by") + chip(14, 86, "Text", True, LAGOON, 66) + chip(87, 86, "Push", False, LAGOON, 66) + chip(160, 86, "Email", False, LAGOON, 66) + lbl(14, 134, "Quiet hours") + rect(14, 140, 212, 40, CREAM, LINE, 4) + t(24, 164, "9 PM to 8 AM", 12, INK, "khand") + toggle(196, 154, True, JUNGLE) + t(14, 202, "Recalls and emergencies always come through.", 7.3, MUTE))),
 "How Should Notification Settings Work?")
add(GON, NP,
 O("np_preview", "Preferences With Message Previews", "Each toggle shows a preview of the actual message it controls.", ["transparent", "concrete", "clear"], "system",
   screen(h1(14, 56, "Notifications", 17) + "".join(ln(66 + i * 60) + t(14, 84 + i * 60, n, 9, INK, "hind", 600) + toggle(204, 75 + i * 60, on, JUNGLE) + rect(14, 92 + i * 60, 212, 26, "#F5F5F5", r=8) + t(22, 108 + i * 60, p, 7, MUTE) for i, (n, p, on) in enumerate([("Tech On The Way", "\"Danny is 15 minutes away.\"", True), ("Filter Reminders", "\"Time to swap your 16x25x1 filter.\"", True), ("Seasonal Tips", "\"Fall tip: shut off outdoor faucets.\"", False)])))),
 O("np_presets", "Preferences As Presets", "Three presets (Essentials, Balanced, Everything) with a 'Customize' link.", ["easy", "fast", "guided"], "neighbor",
   screen(h1(14, 56, "Notifications", 17) + "".join(rect(14 + i * 72, 68, 68, 100, SEL if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 4, 1.4) + t(48 + i * 72, 92, n, 9, INK, "khand", anchor="middle") + t(48 + i * 72, 112, c, 18, INK, "khand", anchor="middle") + t(48 + i * 72, 122, "a month", 6.5, MUTE, anchor="middle") for i, (n, c) in enumerate([("Essentials", "~2"), ("Balanced", "~5"), ("Everything", "~12")])) + link(14, 192, "Customize", LAGOON) + btn(232, "Save"))),
 "Previews Or Presets?")
# ===================== 21. Deeper multi-accent (6) =====================
CC = "Up Keep: Multi-Accent Color"
def icon_set(cols, title):
    return screen(h1(14, 56, title, 15) + "".join(rect(14 + (i % 2) * 108, 68 + (i // 2) * 84, 104, 78, "#FFFFFF", LINE, 6) + icon(k, 50 + (i % 2) * 108, 78 + (i // 2) * 84, 32, "duo", cols[i % len(cols)]) + t(66 + (i % 2) * 108, 134 + (i // 2) * 84, n, 8.5, INK, "hind", 600, "middle") for i, (k, n) in enumerate(SYS3)) + btn(244, "Book A Visit", col=TERRA))
add(GK, CC, O("mx_icons_role", "System Icons: One Hue Per System", "Furnace terracotta, water lagoon, AC jungle, detectors saffron. Each system keeps its color everywhere.", ["multi-accent", "coded", "lively"], "neighbor", icon_set([TERRA, LAGOON, JUNGLE, SAFFRON], "My Systems")),
            O("mx_icons_one", "System Icons: All Lagoon", "Every system icon in lagoon; terracotta stays only on the button.", ["multi-accent", "calm", "unified"], "system", icon_set([LAGOON], "My Systems")), "Color System Icons By System?")
add(GK, CC, O("mx_ill_trio", "Illustration: Multi-Hue House", "A spot drawing with a terracotta door, lagoon windows, jungle lawn and a saffron sun.", ["multi-accent", "warm", "drawn"], "neighbor",
                 screen(house_ill(30, 50, 1, INK, TERRA, LAGOON, SAFFRON, JUNGLE) + h1(120, 190, "Your Home Is Covered", 16, anchor="middle") + t(120, 206, "Four visits a year, one tech", 7.5, MUTE, anchor="middle") + btn(232, "See My Plan"))),
            O("mx_ill_mono", "Illustration: Ink Plus One Pop", "The same drawing in black line with only a terracotta door.", ["multi-accent", "restrained", "clean"], "concierge",
                 screen(house_ill(30, 50, 1, INK, TERRA, "#FFFFFF", None, LINE) + h1(120, 190, "Your Home Is Covered", 16, anchor="middle") + t(120, 206, "Four visits a year, one tech", 7.5, MUTE, anchor="middle") + btn(232, "See My Plan"))), "How Colorful Should Spot Illustrations Be?")
SPEND = [.5, .3, .8, .45, .2, .65]; MON = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
add(GK, CC, O("mx_chart_multi", "Chart: Bars Colored By Type", "Spending bars stacked by type: visits lagoon, repairs terracotta, add-ons jungle.", ["multi-accent", "data", "lively"], "system",
                 screen(h1(14, 56, "Spending This Year", 15) + "".join(rect(24 + i * 34, 160 - 80 * v, 20, 80 * v * .5, LAGOON) + rect(24 + i * 34, 160 - 80 * v * .5, 20, 80 * v * .3, TERRA) + rect(24 + i * 34, 160 - 80 * v * .2, 20, 80 * v * .2, JUNGLE) + t(34 + i * 34, 174, MON[i], 6.5, MUTE, "hind", 600, "middle") for i, v in enumerate(SPEND)) + "".join(dot(20 + i * 70, 196, 3.5, c) + t(28 + i * 70, 199, n, 7, MUTE) for i, (n, c) in enumerate([("Visits", LAGOON), ("Repairs", TERRA), ("Add-ons", JUNGLE)])) + rows(212, [("Total", "$3,412")]))),
            O("mx_chart_mono", "Chart: One-Color Bars", "Same chart, all bars ink with the current month in terracotta.", ["multi-accent", "clean", "focused"], "concierge",
                 screen(h1(14, 56, "Spending This Year", 15) + bars(24, 80, SPEND, [INK, INK, INK, INK, INK, TERRA], 20, 14, 80, MON) + rows(212, [("Total", "$3,412")]))), "Multi-Color Or One-Color Charts?")
def badges(style):
    o = h1(14, 56, "Your Badges", 17)
    for i, (n, c) in enumerate([("Year One", TERRA), ("All Visits Done", JUNGLE), ("Recall Fixed", LAGOON), ("Filter Pro", SAFFRON), ("Referrer", BERRY), ("Safety Pass", JUNGLE)]):
        cx, cy = 50 + (i % 3) * 70, 96 + (i // 3) * 82
        o += (dot(cx, cy, 22, c) + shield(cx - 10, cy - 11, "#FFFFFF", .85, False) if style == "fill" else dot(cx, cy, 22, c + "1F") + f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{c}" stroke-width="1.5"/>' + shield(cx - 10, cy - 11, c, .85, False)) + t(cx, cy + 36, n, 7, INK, "hind", 600, "middle")
    return screen(o)
add(GK, CC, O("mx_badge_fill", "Badges: Solid Color Discs", "Achievement badges as solid colored discs with white icons.", ["multi-accent", "bold", "playful"], "neighbor", badges("fill")),
            O("mx_badge_tint", "Badges: Tinted With Colored Line", "The same badges as light tints with a colored outline and icon.", ["multi-accent", "soft", "calm"], "system", badges("tint")), "Which Badge Style?")
def donut(cols):
    import math
    o = h1(14, 56, "Where Your Visits Go", 15); a0 = 0; segs = [(.4, "Heating"), (.25, "Water"), (.2, "Cooling"), (.15, "Safety")]
    for i, (f, n) in enumerate(segs):
        a1 = a0 + f * 2 * math.pi; c = cols[i % len(cols)]
        x0, y0, x1, y1 = 120 + 50 * math.sin(a0), 130 - 50 * math.cos(a0), 120 + 50 * math.sin(a1), 130 - 50 * math.cos(a1)
        o += f'<path d="M{x0:.1f} {y0:.1f} A50 50 0 {1 if f>.5 else 0} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{c}" stroke-width="16"/>'
        o += dot(24 + (i % 2) * 108, 208 + (i // 2) * 18, 4, c) + t(34 + (i % 2) * 108, 211 + (i // 2) * 18, f"{n} {int(round(f*100))}%", 7.5, INK); a0 = a1
    return screen(o + t(120, 136, "38", 18, INK, "khand", anchor="middle") + t(120, 148, "CHECKS", 6, MUTE, "hind", 600, "middle"))
add(GK, CC, O("mx_donut_four", "Donut: Four Role Colors", "Terracotta, lagoon, jungle and saffron segments.", ["multi-accent", "lively", "data"], "system", donut([TERRA, LAGOON, JUNGLE, SAFFRON])),
            O("mx_donut_shades", "Donut: Lagoon Shades", "One hue in four shades of lagoon, from deep to light.", ["multi-accent", "calm", "unified"], "concierge", donut([LAGOON, LAG2, "#4F93AE", "#8FBFD0"])), "Four Hues Or One Hue In Shades?")
def status_badges(mode):
    o = h1(14, 56, "Status Badges", 15)
    for i, (n, c) in enumerate([("Done", JUNGLE), ("Due Soon", SAFFRON), ("Book Now", TERRA), ("Info", LAGOON)]):
        y = 76 + i * 34; o += ln(y - 8) + t(14, y + 8, ["Furnace tune-up", "Water heater flush", "Dryer vent", "Recall check"][i], 8.5, INK)
        o += (dot(160, y + 5, 4, c) + t(170, y + 8, n, 8, INK, "hind", 600)) if mode == "dot" else tag(160, y - 1, n, c, True)
    return screen(o + t(14, 226, "Same four colors, different weight", 7, MUTE))
add(GK, CC, O("mx_status_pill", "Status As Solid Pills", "Filled colored pills with white text for every status.", ["multi-accent", "bold", "scannable"], "crew", status_badges("pill")),
            O("mx_status_dot", "Status As Dot + Word", "A small colored dot and a black word; color stays tiny.", ["multi-accent", "micro-dose", "clean"], "system", status_badges("dot")), "How Loud Should Status Badges Be?")

# ===================== 22. Swipe Controls (2) =====================
C = lambda i, l, desc, tags, **k: {"id": "uk3_" + i, "label": l, "desc": desc, "tags": tags, "feeling": None, "visual": {**{"type": "controls", "words": ["This", "Both", "Love", "That"], "icons": ["◀", "⇄", "❤", "▶"], "colors": [LAGOON, JUNGLE, "#E0245E", TERRA], "bg": "#FFFFFF", "font": "Hind", "stampov": "word", "press": None}, **k}}
add(GS, "Swipe Controls", C("sc3_pill_fill", "Filled Pills, Role Colors", "Solid pills in lagoon, jungle, red and terracotta with white words.", ["bold", "multi-accent"], fmt="pill", style="fill", font="Khand", hint="edges"),
    C("sc3_round_fill", "Filled Circles, Role Colors", "Solid round buttons in the four role colors.", ["playful", "lively"], fmt="round", style="fill", hint="edges"), "Which Swipe Controls?")
add(GS, "Swipe Controls", C("sc3_square_ink", "Black Squares, Colored Press", "Black outline squares that fill with their role color when pressed.", ["restrained", "clear"], fmt="square", style="outline", press="fill", colors=[INK, INK, INK, INK], hint="edges"),
    C("sc3_cream_square", "Cream Squares, Colored Words", "Square buttons on cream with each word in its role color.", ["warm", "micro-dose"], fmt="square", style="outline", bg="#FAF6EE", hint="edges"), "Which Swipe Controls?")

# ---- order: open with a dashboard choice; no category twice in a row ----
random.seed(33); first = pairs[:1]; rest = pairs[1:]; random.shuffle(rest); seq = first + rest; order = []
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
assert len(order) == DECK_SIZE, len(order)
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
        "title": "Up Keep Round 3: Reports, Records, Billing, Field Branding And Deeper Color", "brands": ["Up Keep / Smart Upkeep: home maintenance membership app (https://webermanapps.github.io/smart-upkeep/)", "Base: white or cream, #0A0A0A ink, square black buttons, Khand/Hind; 2-3 small pops (terracotta = act, lagoon = info, jungle = done, saffron = due soon); no neon, no pastel, not all-beige"],
        "generated_at": now, "builds_on": "upkeep-1 top tags clear, system, warm, lively, multi-accent; upkeep-2 top tags clear, system, visual, guided, easy (no upkeep results files in results/)",
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

