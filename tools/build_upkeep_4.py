#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-4: 50 all-new this-or-that pairs, round 4 of the Up Keep / Smart Upkeep home maintenance
membership app (https://webermanapps.github.io/smart-upkeep/). Mock screens are drawn as SVG in Up Keep's own style
(white base, #0A0A0A ink, square black buttons, Khand headings, Hind body, terracotta accent, #E5E0D8 rules) and
rendered through the 'hm' svg renderer. Run from the style-swipe repo root."""
import json, random, re, datetime as dt
DID = "upkeep-4"; LOGOS = "/workspace/brand/smart-upkeep/logos"
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
    return {"id": "uk4_" + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "notes": True, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": bg}}
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
# ===================== upkeep-4 content =====================
from PIL import Image
MOCK = "/workspace/brand/smart-upkeep/mockups"; PRICE = "Membership Starting at $99/Month"; BORD = "#E5E5E5"; NAVY = "#171717"
for _n in ["white_black-logo", "black_white-logo", "terracotta"]:
    Image.open(f"{MOCK}/polo_{_n}.png").convert("RGB").resize((720, 800)).save(f"img/uk4_polo_{_n}.jpg", quality=82)
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
# ---- Group 1: white base and header (pairs 1-4, fixed first) ----
G1 = "White Base & Header"
add(G1, "Up Keep: App On White", O("wh_white_mwhead", "Pure White With A Max Weberman Header", "The app screen on pure white. Header like maxweberman.com: logo left, square outlined Share right, thin grey rule.", ["clear", "system", "readable"], "system", scr(home("multi"))),
    O("wh_cream_now", "The Current Cream Look", "Today's app: warm cream page, cream cards and the prototype pill in the header.", ["warm", "soft", "familiar"], "neighbor", cream_home()), "Pure White Or The Current Cream?")
add(G1, "Up Keep: Accent On White", O("wh_noaccent", "White, No Accent", "Black, grey and white only. No color at all on the screen.", ["clean", "calm", "restrained"], "concierge", scr(home("none"))),
    O("wh_oneaccent", "White, One Small Accent", "Same screen with one short terracotta rule under the headline.", ["clear", "warm", "micro-dose"], "system", scr(home("one"))), "No Color Or One Small Pop?")
add(G1, "Up Keep: Header Buttons", O("wh_head_share", "Header: Share Only", "Logo left and one square outlined Share button right.", ["simple", "clear"], "system", scr(home("one"), head="share")),
    O("wh_head_call", "Header: Call And Share", "Logo left, square outlined Call and Share buttons right.", ["guided", "easy", "human"], "crew", scr(home("one"), head="call")), "One Header Button Or Two?")
add(G1, "Up Keep: Header Logo", O("wh_head_byline", "Header: Logo With 'By Max Weberman'", "Small tracked 'By Max Weberman' under the logo, like the site wordmark.", ["personal", "trust", "warm"], "neighbor", scr(home("one"), head="byline")),
    O("wh_head_center", "Header: Centered Logo", "Logo centered, Share on the right, thin rule under.", ["balanced", "calm"], "concierge", scr(home("one"), head="center")), "Byline Logo Or Centered Logo?")
FIRST = len(pairs)
# ---- Group 2: membership plan cards ----
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
add(G2, "Up Keep: Plan Price", O("pl_price_stack", "Price As A Big $99", "'Membership Starting at' small on top, a big terracotta $99/Month under it.", ["big", "readable", "lively"], "crew", plan("stack")),
    O("pl_price_line", "Price As One Clear Line", "'Membership Starting at $99/Month' as one sentence, same size throughout.", ["clear", "calm", "honest"], "concierge", plan("line")), "How Should The One Price Show?")
add(G2, "Up Keep: What's Included", O("pl_inc_list", "Included As A Check List", "Four rows, each with a small green check.", ["clear", "system", "scannable"], "system", plan("stack", "list")),
    O("pl_inc_grid", "Included As Icon Tiles", "Four small cream tiles, each with a drawn icon in its own color.", ["lively", "visual", "warm"], "neighbor", plan("stack", "grid")), "List Or Icon Tiles For What's Included?")
add(G2, "Up Keep: Plan Year View", O("pl_inc_seasons", "Show The Year As Four Visits", "Spring, Summer, Fall and Winter as a four-step line.", ["guided", "easy", "visual"], "system", plan("line", "seasons")),
    O("pl_inc_list2", "Show The Systems We Cover", "A list of what gets checked, with no season timeline.", ["clear", "thorough"], "crew", plan("line", "list", cancel="tag")), "Seasons Or Systems?")
add(G2, "Up Keep: Plan Button Color", O("pl_cta_terra", "Plan Button In Terracotta", "The one action on the card in solid terracotta.", ["warm", "lively", "guided"], "neighbor", plan("stack", "list", TERRA)),
    O("pl_cta_black", "Plan Button In Black", "Square black button; color stays in the price only.", ["system", "restrained"], "concierge", plan("stack", "list", INK)), "Terracotta Or Black Button?")
add(G2, "Up Keep: Cancel Anytime", O("pl_cancel_under", "'Cancel Anytime' Under The Button", "A small check and 'Cancel Anytime' right below the button.", ["reassuring", "easy"], "neighbor", plan("line", "grid", cancel="under")),
    O("pl_cancel_tag", "'Cancel Anytime' As A Top Tag", "A green 'Cancel Anytime' tag in the card's top corner.", ["clear", "upfront"], "system", plan("line", "grid", cancel="tag")), "Where Does 'Cancel Anytime' Go?")
add(G2, "Up Keep: Card Frame", O("pl_frame_bar", "Card With A Terracotta Top Bar", "White card with a thin terracotta bar across the top.", ["lively", "warm"], "crew", plan("stack", "seasons", frame="bar")),
    O("pl_frame_cream", "Card On A Cream Page", "Plain bordered white card sitting on a cream page.", ["warm", "soft"], "neighbor", plan("stack", "seasons", frame="line", bg=CREAM)), "Top Bar On White Or Card On Cream?")
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
add(G2, "Up Keep: Plan Story", O("pl_story_split", "Side By Side: On Your Own vs With Us", "Two columns comparing doing it yourself with the membership.", ["guided", "clear", "persuasive"], "crew", plan_cmp("split")),
    O("pl_story_list", "One Card: Just What You Get", "A single card listing four promises, no comparison.", ["simple", "calm"], "concierge", plan_cmp("list")), "Compare Or Just List?")
# ---- Group 3: extras / add-on tiles ----
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
add(G3, "Up Keep: Extras Layout", O("ex_grid", "Extras As A Tile Grid", "Six square tiles, two across, each with a drawn icon.", ["visual", "easy", "big"], "neighbor", extras("grid")),
    O("ex_rows", "Extras As Rows With Switches", "One row per extra with an on/off switch.", ["system", "clear", "compact"], "system", extras("rows")), "Tiles Or Switch Rows?")
add(G3, "Up Keep: Extras Picked State", O("ex_sel_check", "Picked: Green Border And Check", "A picked tile gets a jungle border and a check.", ["clear", "calm"], "system", extras("grid", "check", "duo")),
    O("ex_sel_fill", "Picked: Terracotta Tint", "A picked tile gets a light terracotta fill and border.", ["warm", "lively"], "neighbor", extras("grid", "fill", "duo")), "How Should A Picked Extra Look?")
add(G3, "Up Keep: Extras Icons", O("ex_ic_ink", "Black Line Icons", "All icons drawn in thin black line.", ["restrained", "clean"], "concierge", extras("grid", "check", "outline", True, "button")),
    O("ex_ic_color", "Colored Icons", "Each icon tinted in terracotta, lagoon, jungle or saffron.", ["lively", "multi-accent", "warm"], "neighbor", extras("grid", "check", "duo", True, "button")), "Black Or Colored Icons?")
add(G3, "Up Keep: Extras Detail", O("ex_sub_on", "Tile With A Short How-Often Line", "Name plus a small line like 'Spring And Fall'.", ["guided", "clear"], "system", extras("grid", "fill", "outline", True)),
    O("ex_sub_off", "Tile With Name Only", "Just the icon and the name; bigger and quieter.", ["simple", "big"], "concierge", extras("grid", "fill", "outline", False)), "Add The How-Often Line?")
add(G3, "Up Keep: Extras Add Control", O("ex_add_plus", "Round + In The Corner", "A small round plus in each tile's corner.", ["playful", "easy"], "neighbor", extras("grid", "check", "outline", True, "corner")),
    O("ex_add_btn", "Square Add Button", "A small black square ADD button that turns green ADDED.", ["system", "clear"], "crew", extras("grid", "check", "outline", True, "button")), "Plus Or Add Button?")
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
add(G3, "Up Keep: Extras Grouping", O("ex_by_season", "Grouped By Season", "Extras split into Spring And Summer and Fall And Winter.", ["guided", "organized", "system"], "system", extras_season("season")),
    O("ex_big_cards", "Three Big Cards, Then See More", "Three large cards with big icons; the rest behind a link.", ["big", "readable", "easy"], "neighbor", extras_season("big")), "By Season Or Big Cards?")
add(G3, "Up Keep: Extras Page", O("ex_page_white", "Extras On White", "Tile grid on a pure white page.", ["clear", "clean"], "system", extras("grid", "check", "duo", False, "corner")),
    O("ex_page_cream", "Extras On Cream", "Same tiles on a warm cream page.", ["warm", "soft"], "neighbor", extras("grid", "check", "duo", False, "corner", CREAM)), "White Or Cream Page?")
# ---- Group 4: tech profile and license badges ----
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
        return rect(14, 246, 212, 46, "#FFFFFF", JUNGLE, 4, 1.5) + icon("check", 22, 256, 16, "duo", JUNGLE) + t(44, 262, "License Active", 10, INK, "khand") + t(44, 274, "State Of Michigan · Mechanical · #7114203", 6.6, MUTE) + t(44, 284, "Checked Oct 12, 2026", 6.2, MUTE)
    return (rect(0, 0, W, H, INK, extra='opacity=".35"') + rect(0, 120, W, 180, "#FFFFFF", r=14) + rect(108, 128, 24, 3, "#D4D4D4", r=1.5) + dot(120, 166, 24, JUNGLE + "1F") + shield(106, 152, JUNGLE, 1.2)
            + t(120, 210, "License Verified", 16, INK, "khand", anchor="middle") + t(120, 224, "State Of Michigan · Mechanical Contractor", 7.2, MUTE, anchor="middle") + t(120, 236, "License #7114203 · Active", 7.2, INK, anchor="middle") + link(120, 256, "Open State Lookup", LAGOON, "middle") + btn(266, "Done", "outline", h=22, size=8))
add(G4, "Up Keep: Tech Badges", O("tp_chip_black", "Badges As Black Squares", "Certified, Trained, Insured as small black square chips.", ["system", "bold", "clear"], "crew", techprof("black")),
    O("tp_chip_color", "Badges As Colored Outlines", "Each badge outlined in its own color with a light tint.", ["lively", "multi-accent", "warm"], "neighbor", techprof("outline")), "Black Or Colored Badges?")
add(G4, "Up Keep: Verify Control", O("tp_verify_btn", "Verify As A Big Lagoon Button", "Full-width lagoon button with a shield: Tap To Verify License.", ["guided", "big", "trust"], "system", techprof("outline", "button")),
    O("tp_verify_link", "Verify As A Shield Link", "A small shield and an underlined link.", ["quiet", "clean"], "concierge", techprof("outline", "link")), "Button Or Link To Verify?")
add(G4, "Up Keep: After Verify", O("tp_after_inline", "Result Shows Under The Card", "Tapping verify opens a green 'License Active' box in place.", ["easy", "clear", "fast"], "system", techprof("black", "link", sheet=lic_sheet("inline"))),
    O("tp_after_sheet", "Result In A Pop-Up Sheet", "A bottom sheet with a big shield, the state, license number and a link to the state lookup.", ["trust", "thorough", "big"], "crew", techprof("black", "button", sheet=lic_sheet("sheet"))), "In Place Or Pop-Up Sheet?")
add(G4, "Up Keep: Tech Header", O("tp_head_big", "Big Centered Tech Portrait", "Large illustrated portrait centered with name below.", ["human", "warm", "big"], "neighbor", techprof("ribbon", "button", "big")),
    O("tp_head_row", "Small Portrait In A Row", "Small portrait left, name and license line right.", ["compact", "system"], "system", techprof("ribbon", "button", "row")), "Big Portrait Or Compact Row?")
add(G4, "Up Keep: Badge Shape", O("tp_shape_seal", "Badges As Round Seals", "Three round dashed seals with a shield in each.", ["visual", "trust", "lively"], "neighbor", techprof("seal", "button", "row")),
    O("tp_shape_ribbon", "Badges As Ribbon Tabs", "Solid colored tabs with a notched bottom.", ["bold", "playful"], "crew", techprof("ribbon", "link", "row")), "Seals Or Ribbons?")
add(G4, "Up Keep: Tech Detail", O("tp_stats", "Show Years, Visits And Rating", "Three big numbers under the badges.", ["data", "clear", "proof"], "system", techprof("black", "button", "big", "stats")),
    O("tp_quote", "Show A Short Note From The Tech", "A one-line quote from Danny in a cream box.", ["personal", "warm", "human"], "neighbor", techprof("black", "button", "big", "quote")), "Numbers Or A Personal Note?")
def door_card(mode):
    o = lbl(14, 50, "Arriving Today · 9 AM") + h1(14, 70, "Danny Is On The Way", 17)
    if mode == "id":
        o += rect(40, 84, 160, 170, "#FFFFFF", INK, 10, 1.5) + rect(40, 84, 160, 26, INK, r=0) + roof_logo(84, 102, .9, "#FFFFFF", "#BDBDBD") + techface(120, 140, 18) + t(120, 186, "Danny Ruiz", 14, INK, "khand", anchor="middle") + chips(34, 196, "black") + shield(60, 226, LAGOON, .6, False) + link(78, 237, "Tap To Verify License", LAGOON, size=7)
    else:
        o += rect(14, 84, 212, 66, CREAM, "none", 8) + techface(42, 108, 13) + t(66, 108, "Danny Ruiz", 13, INK, "khand") + t(66, 120, "White van, terracotta stripe", 7, MUTE) + van(24, 160, .9) + rect(14, 216, 212, 26, LAGOON) + t(120, 233, "TAP TO VERIFY LICENSE", 8, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
    return scr(o + btn(262, "Call Danny", "outline", h=24, size=8))
add(G4, "Up Keep: Who's At Your Door", O("tp_door_id", "Arrival As A Photo ID Card", "A badge-style ID card with portrait, name and verify link.", ["trust", "bold", "system"], "crew", door_card("id")),
    O("tp_door_van", "Arrival With The Van To Look For", "Tech row, the van drawing and a big verify button.", ["guided", "visual", "easy"], "neighbor", door_card("van")), "ID Card Or Van To Look For?")
# ---- Group 5: yard sign ----
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
add(G5, "Field: Yard Sign Stake", O("ys_stake_h", "Sign On A Wire H-Stake", "The winning white sign on a simple wire stake.", ["simple", "light"], "neighbor", yard("h")),
    O("ys_stake_post", "Sign Hung From A Black Post", "Same sign hanging from a black real-estate style post.", ["premium", "bold"], "concierge", yard("post")), "H-Stake Or Hanging Post?")
add(G5, "Field: Yard Sign Message", O("ys_msg_maint", "'This Home Is Maintained By Smart Upkeep'", "A pride-of-home line, no price.", ["warm", "trust"], "neighbor", yard("h", "maint")),
    O("ys_msg_price", "'Membership Starting at $99/Month'", "The one price, big, in terracotta.", ["clear", "direct"], "crew", yard("h", "price")), "Pride Line Or Price?")
add(G5, "Field: Yard Sign Color Pop", O("ys_bar_terra", "Terracotta Strip Along The Bottom", "A thin terracotta band across the sign's bottom edge.", ["warm", "lively"], "crew", yard("post", "maint", "terra")),
    O("ys_bar_lagoon", "Short Lagoon Rule Under The Logo", "Only a short lagoon line under the logo.", ["restrained", "clean"], "system", yard("post", "maint", "lagoon")), "Bottom Strip Or Small Rule?")
add(G5, "Field: Yard Sign Contact", O("ys_code_url", "Web Address At The Bottom", "Plain smartupkeep.com along the bottom.", ["simple", "readable"], "system", yard("h", "price", "none", "url", "port")),
    O("ys_code_qr", "QR Code At The Bottom", "A small QR code that opens the quote.", ["modern", "easy"], "crew", yard("h", "price", "none", "qr", "port")), "Web Address Or QR?")
add(G5, "Field: Yard Sign Shape", O("ys_shape_land", "Wide Sign", "A wide landscape sign, logo large.", ["big", "readable"], "neighbor", yard("h", "maint", "terra", "url", "land")),
    O("ys_shape_port", "Tall Sign", "A taller, narrower sign with stacked lines.", ["neat", "premium"], "concierge", yard("h", "maint", "terra", "url", "port")), "Wide Or Tall Sign?")
# ---- Group 6: van wrap ----
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
add(G6, "Field: Van Stripe Weight", O("vw_stripe_thin", "Thin Terracotta Pinstripe", "The winning white van with a thin pinstripe.", ["restrained", "premium"], "concierge", van2("thin")),
    O("vw_stripe_thick", "Thick Terracotta Band", "Same van with a bold, wide band.", ["bold", "lively"], "crew", van2("thick")), "Pinstripe Or Bold Band?")
add(G6, "Field: Van Stripe Shape", O("vw_stripe_straight", "Straight Stripe", "A straight stripe end to end.", ["clean", "system"], "system", van2("mid")),
    O("vw_stripe_swoop", "Stripe That Sweeps Up To The Window", "The stripe curves up toward the front window.", ["lively", "motion"], "neighbor", van2("swoop")), "Straight Or Sweep?")
add(G6, "Field: Van Logo Size", O("vw_logo_big", "One Big Side Logo", "A large logo across the side panel.", ["big", "readable"], "crew", van2("mid", "side", "lic")),
    O("vw_logo_door", "Mid Logo Plus Small Door Logo", "Medium side logo and a second small one on the cab door.", ["neat", "detail"], "concierge", van2("mid", "door", "lic")), "One Big Logo Or Two?")
add(G6, "Field: Van Side Line", O("vw_line_phone", "Phone And Web Line", "Phone number and web address under the logo.", ["easy", "clear"], "system", van2("thin", "side", "phone")),
    O("vw_line_price", "'Membership Starting at $99/Month'", "The one price under the logo.", ["direct", "bold"], "crew", van2("thin", "side", "price")), "Contact Or Price On The Van?")
add(G6, "Field: Van Roof Mark", O("vw_roof_on", "Roofline Drawn Above The Stripe", "A terracotta roof shape rising from the stripe, echoing the logo.", ["playful", "brand"], "neighbor", van2("mid", "side", "lic", True)),
    O("vw_roof_off", "Stripe Only", "Just the stripe, no roof shape.", ["clean", "simple"], "system", van2("mid", "side", "lic", False)), "Add The Roofline Mark?")
# ---- Group 7: uniform on people ----
G7 = "Uniform On People"
def polo_img(keys, cap=""):
    n = len(keys); w = W / n; o = rect(0, 0, W, H, "#F2EFEA")
    for i, k in enumerate(keys): o += f'<image href="img/uk4_polo_{k}.jpg" x="{i*w+2}" y="16" width="{w-4}" height="252" preserveAspectRatio="xMidYMid slice"/>'
    return screen(o + (t(120, 290, cap, 9, INK, "khand", anchor="middle") if cap else ""), head=False)
add(G7, "Field: Polo On A Tech", O("un_white_on", "White Polo, Black Logo", "The white polo shown on a tech.", ["clean", "bright", "trust"], "concierge", polo_img(["white_black-logo"], "White Polo")),
    O("un_black_on", "Black Polo, White Logo", "The black polo shown on a tech.", ["bold", "pro", "crew"], "crew", polo_img(["black_white-logo"], "Black Polo")), "White Or Black Polo On A Person?")
add(G7, "Field: Polo Color Pop", O("un_terra_on", "Terracotta Polo, White Logo", "The terracotta polo shown on a tech.", ["warm", "lively", "brand"], "neighbor", polo_img(["terracotta"], "Terracotta Polo")),
    O("un_white_on2", "White Polo To Match The Van", "White polo, matching the white van and sign that won.", ["clean", "system"], "system", polo_img(["white_black-logo"], "White Polo, Matches The Van")), "Terracotta Or White To Match?")
add(G7, "Field: Crew Look", O("un_crew_mixed", "Crew In Mixed Colors", "Three techs: white, black and terracotta polos.", ["lively", "varied"], "neighbor", polo_img(["white_black-logo", "black_white-logo", "terracotta"], "Mixed Crew")),
    O("un_crew_white", "Crew All In White", "Three techs all in the white polo.", ["unified", "clean"], "system", polo_img(["white_black-logo"] * 3, "All White Crew")), "Mixed Or Matching Crew?")
add(G7, "Field: Lead And Crew", O("un_lead_terra", "Lead Tech In Terracotta, Crew In Black", "The lead stands out in terracotta.", ["clear", "guided"], "crew", polo_img(["terracotta", "black_white-logo"], "Lead In Terracotta")),
    O("un_all_black", "Everyone In Black", "All techs in black polos.", ["bold", "pro"], "crew", polo_img(["black_white-logo", "black_white-logo"], "All Black")), "Highlight The Lead Or All The Same?")
# ---- Group 8: lawn quote ----
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
add(G8, "Up Keep: Lawn Quote Order", O("ln_map_first", "Yard Map First, Price Below", "The illustrated satellite outline leads; price sits under it.", ["visual", "proof", "guided"], "system", lawn("map")),
    O("ln_price_first", "Price First, Map Below", "A big $46 Per Cut up top with a small map under it.", ["direct", "big", "clear"], "crew", lawn("price")), "Map First Or Price First?")
add(G8, "Up Keep: Lawn Outline Color", O("ln_line_lagoon", "Outline In Lagoon", "The measured lawn traced in a dashed lagoon line.", ["calm", "info"], "system", lawn("map", LAGOON, "big", "toggle")),
    O("ln_line_terra", "Outline In Terracotta", "The same outline in terracotta.", ["warm", "lively"], "neighbor", lawn("map", TERRA, "big", "toggle")), "Lagoon Or Terracotta Outline?")
add(G8, "Up Keep: Lawn Size", O("ln_num_big", "One Big Square-Foot Number", "6,240 Sq Ft in large type.", ["big", "readable", "simple"], "crew", lawn("map", LAGOON, "big", "chips", False, "none")),
    O("ln_num_zones", "Front And Back Listed", "Map labeled Front and Back with each size listed.", ["thorough", "system"], "system", lawn("map", LAGOON, "zones", "chips", False, "none")), "One Number Or By Zone?")
add(G8, "Up Keep: Lawn Frequency", O("ln_freq_chips", "Pick How Often With Chips", "Weekly, Every Other Week, One Time as chips.", ["guided", "easy"], "system", lawn("map", JUNGLE, "big", "chips")),
    O("ln_freq_toggle", "One Weekly Switch", "Just a Weekly All Season switch.", ["simple", "fast"], "concierge", lawn("map", JUNGLE, "big", "toggle")), "Chips Or One Switch?")
add(G8, "Up Keep: Lawn Edit", O("ln_handles_on", "Show Drag Corners To Adjust", "Round handles on the outline so you can fix it.", ["interactive", "trust"], "system", lawn("price", LAGOON, "big", "chips", True)),
    O("ln_handles_off", "Clean Outline, No Handles", "Just the outline; edit lives behind a link.", ["clean", "calm"], "concierge", lawn("price", LAGOON, "big", "chips", False)), "Show Drag Corners?")
def lawn_steps(mode):
    o = lbl(14, 48, "Lawn Mowing Quote") + h1(14, 66, "Get A Mowing Price", 16)
    if mode == "steps":
        for i, (s, c) in enumerate([("Type Your Address", JUNGLE), ("We Outline Your Lawn", JUNGLE), ("See Your Price", TERRA)]):
            y = 80 + i * 40; o += dot(28, y + 12, 11, c) + t(28, y + 16, str(i + 1), 10, "#FFFFFF", "khand", anchor="middle") + t(48, y + 16, s, 11, INK, "khand") + (f'<line x1="28" y1="{y+24}" x2="28" y2="{y+40}" stroke="{LINE}" stroke-width="2"/>' if i < 2 else "")
        o += field(212, "Address", "1418 Maple Ave, Royal Oak")
    else:
        o += field(78, "Address", "1418 Maple Ave, Royal Oak") + sat(14, 110, 212, 120, LAGOON) + t(120, 246, "Measuring From Above...", 8, LAGOON, "hind", 600, "middle")
    return scr(o + sticky(btn(270, "Measure My Lawn", "fill", INK, h=22, size=8), 264))
add(G8, "Up Keep: Lawn Start", O("ln_start_steps", "Start With Three Numbered Steps", "Shows how it works before the address box.", ["guided", "clear", "easy"], "system", lawn_steps("steps")),
    O("ln_start_map", "Start With The Map Already Drawing", "Address box, then the yard outline drawing in live.", ["visual", "lively"], "neighbor", lawn_steps("map")), "Steps First Or Map First?")
# ---- Group 9: moisture-scan character ----
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
add(G9, "Character: Drawing Style", O("ms_flat", "Flat Filled Character", "Solid shapes: grey uniform, brown skin, dark cap, like the V.2 frames.", ["warm", "friendly", "illustrated"], "neighbor", scan("flat")),
    O("ms_line", "Black Line-Art Character", "Same tech drawn in black line on white with one color stripe.", ["clean", "system", "light"], "system", scan("line", TERRA)), "Filled Or Line-Art Tech?")
add(G9, "Character: Outfit", O("ms_grey_cap", "Grey Uniform, Dark Cap", "The current grey work uniform and dark cap.", ["pro", "calm"], "crew", scan("flat", "#5E6B73", "#2B2B2B", "dash")),
    O("ms_white_terra", "White Polo, Terracotta Cap", "Matches the white polo with a terracotta cap pop.", ["brand", "lively", "warm"], "neighbor", scan("flat", "#F4F4F2", TERRA, "dash")), "Grey Uniform Or White Polo?")
add(G9, "Character: Scan Effect", O("ms_fx_glow", "Soft Lagoon Glow On The Ceiling", "A soft blue glow where the meter finds moisture.", ["visual", "soft"], "concierge", scan("flat", fx="glow")),
    O("ms_fx_beam", "Dashed Scan Line To The Ceiling", "A dashed lagoon line from the meter up to a small ring.", ["clear", "system", "diagram"], "system", scan("flat", fx="beam")), "Glow Or Scan Line?")
add(G9, "Character: Result Tag", O("ms_tag_caught", "Saffron 'Caught Early' Tag", "A saffron tag pops up by the spot.", ["lively", "alert"], "crew", scan("flat", fx="beam", label="caught")),
    O("ms_tag_normal", "Lagoon 'Normal' Tag", "An outlined lagoon tag that reads Normal.", ["calm", "reassuring"], "system", scan("flat", fx="beam", label="normal")), "Show A Catch Or All Clear?")
add(G9, "Character: Setting", O("ms_room", "Full Line-Drawn Room", "Tech in a simple drawn room with couch and lamp.", ["story", "guided"], "neighbor", scan("flat", room="full")),
    O("ms_spot", "Tech On A Cream Spot", "Just the tech on a cream circle under a ceiling line.", ["focused", "big", "simple"], "concierge", scan("flat", room="spot")), "Full Room Or Spot?")

# ---- order: pairs 1-4 (white base + header) fixed first; then no group twice in a row ----
random.seed(44); first = pairs[:FIRST]; rest = pairs[FIRST:]; random.shuffle(rest); seq = rest; order = list(first)
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
        "title": "Up Keep Round 4: White Base, Header, Plan Card, Extras, Tech License, Yard Sign, Van, Uniform On People, Lawn Quote, Moisture-Scan Character", "brands": ["Up Keep / Smart Upkeep: home maintenance membership app (https://webermanapps.github.io/smart-upkeep/)", "Base: white or cream, #0A0A0A ink, square black buttons, Khand/Hind; 2-3 small pops (terracotta = act, lagoon = info, jungle = done, saffron = due soon); no neon, no pastel, not all-beige"],
        "generated_at": now, "builds_on": "upkeep-3 results (32/50; top tags system, clear, warm, simple, lively; notes: drop score screens, show uniforms on people); upkeep-1 top tags clear, system, warm, lively, multi-accent; upkeep-2 top tags clear, system, visual, guided, easy (no upkeep results files in results/)",
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

