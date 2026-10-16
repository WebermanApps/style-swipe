#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-2: 25 all-new this-or-that pairs, round 2 of the Up Keep / Smart Upkeep home maintenance
membership app (https://webermanapps.github.io/smart-upkeep/). Mock screens are drawn as SVG in Up Keep's own style
(white base, #0A0A0A ink, square black buttons, Khand headings, Hind body, terracotta accent, #E5E0D8 rules) and
rendered through the 'hm' svg renderer. Run from the style-swipe repo root."""
import json, random, re, datetime as dt
DID = "upkeep-2"; LOGOS = "/workspace/brand/smart-upkeep/logos"
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
    return {"id": "uk2_" + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": bg}}
def add(group, cat, a, b, ask, purpose="refine", retest=False):
    pairs.append({"group": group, "category": cat, "app": "Up Keep", "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": retest})
GD, GC, GA, GB, GF, GP, GE, GM, GK, GV, GS = ("Member Dashboard", "Calendar & Reminders", "Recall & Warranty", "Booking & Tech Arrival", "Funnel Screens", "Payment & Add-Ons",
    "Empty States", "Messages & Referral", "Multi-Accent Color", "Voice & Microcopy", "Swipe Controls")
# Round-2 default: white base, black ink, 2-3 small pops: terracotta = act, lagoon = info, jungle = done, saffron = due soon
SYS = [("furnace", "Furnace", "Carrier 59SC5", "OK", JUNGLE), ("water", "Water Heater", "Rheem XG50T", "Due Nov", SAFFRON), ("ac", "AC Unit", "Trane XR14", "OK", JUNGLE), ("smoke", "Smoke Detectors", "6 of 6", "OK", JUNGLE)]

# ===================== 1. Member dashboard + home record (3) =====================
D = "Up Keep: Member Dashboard"
add(GD, D,
 O("dash_visitfirst", "Next Visit Card Leads", "After sign-up the dashboard opens on the next visit: date, tech, a reschedule link. Systems sit below.", ["clear", "guided", "warm"], "neighbor",
   screen(lbl(14, 48, "Hi Sarah") + h1(14, 66, "Welcome Home", 17) + rect(14, 76, 212, 78, CREAM, LINE, 6) + rect(14, 76, 4, 78, TERRA) + face(44, 104, 12) + t(66, 96, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(66, 112, "Tue, Nov 4 · 9 AM", 13, INK, "khand") + t(66, 124, "Danny, your tech", 7.5, MUTE) + link(66, 144, "Reschedule", LAGOON)
          + "".join(ln(166 + i * 22) + t(14, 181 + i * 22, n, 8.5, INK) + tag(176, 172 + i * 22, st, c) for i, (_, n, _, st, c) in enumerate(SYS[:4])) + tabbar(0))),
 O("dash_scorefirst", "Home Health Score Leads", "A big score ring opens the dashboard, with counts of what's done, due and urgent.", ["system", "data", "lively"], "system",
   screen(lbl(14, 48, "Hi Sarah") + ring(60, 98, 32, .88, JUNGLE, "") + t(60, 104, "88", 20, INK, "khand", anchor="middle") + t(60, 144, "HOME HEALTH", 6, MUTE, "hind", 600, "middle")
          + "".join(dot(112, 80 + i * 20, 4, c) + t(122, 83 + i * 20, s, 8.5, INK) for i, (s, c) in enumerate([("9 systems OK", JUNGLE), ("2 due this month", SAFFRON), ("0 urgent", TERRA)]))
          + rect(14, 158, 212, 30, "#FFFFFF", LINE, 4) + t(22, 177, "Next visit · Tue, Nov 4 · 9 AM", 8, INK, "hind", 600) + t(218, 177, "›", 10, MUTE, anchor="end") + btn(200, "See My Home Record", "outline") + tabbar(0))),
 "What Should The Dashboard Open On?")
add(GD, "Up Keep: Home Record",
 O("rec_tiles", "Systems As Tiles", "A 2x2 grid of systems, each tile with an icon and a colored status dot.", ["visual", "lively", "organized"], "neighbor",
   screen(h1(14, 54, "My Home Record", 17) + "".join(rect(14 + (i % 2) * 108, 64 + (i // 2) * 86, 104, 80, "#FFFFFF", LINE, 6) + icon(k, 22 + (i % 2) * 108, 72 + (i // 2) * 86, 22, "duo", c) + dot(108 + (i % 2) * 108, 74 + (i // 2) * 86, 4, c) + t(22 + (i % 2) * 108, 116 + (i // 2) * 86, n, 9, INK, "hind", 600) + t(22 + (i % 2) * 108, 128 + (i // 2) * 86, m, 6.8, MUTE) + t(22 + (i % 2) * 108, 138 + (i // 2) * 86, st, 6.8, c, "hind", 600) for i, (k, n, m, st, c) in enumerate(SYS)) + tabbar(2))),
 O("rec_rows", "Systems As A List", "One row per system with model, last service and a status tag on the right.", ["clear", "compact", "system"], "system",
   screen(h1(14, 54, "My Home Record", 17) + t(14, 70, "11 systems · updated Oct 8", 7.5, MUTE) + "".join(ln(80 + i * 40) + icon(k, 14, 88 + i * 40, 20, "outline") + t(44, 98 + i * 40, n, 9, INK, "hind", 600) + t(44, 109 + i * 40, m + " · serviced Oct 8", 6.8, MUTE) + tag(180, 92 + i * 40, st, c) for i, (k, n, m, st, c) in enumerate(SYS)) + tabbar(2))),
 "How Should The Home Record List Systems?")
add(GD, "Up Keep: System Detail",
 O("sys_history", "System Page: Service History", "Tap a system to see its photo, model and a dated list of every visit.", ["transparent", "record", "calm"], "concierge",
   screen(link(14, 48, "← Home Record", INK) + photo(14, 56, 212, 70, "label", 6) + h1(14, 146, "Water Heater", 17) + t(14, 160, "Rheem XG50T · 50 gal · installed 2017", 7.5, MUTE)
          + "".join(ln(170 + i * 24) + t(14, 185 + i * 24, d, 8, MUTE) + t(70, 185 + i * 24, n, 8, INK) for i, (d, n) in enumerate([("Oct 8", "Flushed, anode checked"), ("Apr 2", "Flushed"), ("Oct 3", "Installed in Record")])) + link(14, 256, "Download All Reports", TERRA))),
 O("sys_health", "System Page: Age And Health Bar", "The same page leads with an age bar: 9 of about 12 years used, plus what to plan for.", ["practical", "forward", "lively"], "system",
   screen(link(14, 48, "← Home Record", INK) + h1(14, 72, "Water Heater", 17) + t(14, 86, "Rheem XG50T · 50 gal", 7.5, MUTE) + lbl(14, 108, "Life used") + rect(14, 114, 212, 10, "#EEEAE4", r=5) + rect(14, 114, 159, 10, SAFFRON, r=5) + t(14, 138, "9 of about 12 years", 9, INK, "hind", 600)
          + rect(14, 150, 212, 50, CREAM, LINE, 4) + t(22, 166, "Plan Ahead", 10, INK, "khand") + para(22, 178, ["Budget about $1,600 for a new tank", "in 2029. We'll remind you."], 7.5, MUTE, 10) + tag(14, 212, "Flushed Oct 8", JUNGLE) + tag(84, 212, "No Recalls", LAGOON) + btn(240, "Book A Check"))),
 "What Should A System Page Lead With?")

# ===================== 2. Calendar + reminders (3) =====================
add(GC, "Up Keep: Maintenance Calendar",
 O("cal_month", "Month Grid", "A month calendar with colored dots on visit and reminder days. Tap a day for details.", ["visual", "system", "planned"], "system",
   screen(h1(14, 54, "November", 17) + t(226, 54, "‹  ›", 10, INK, anchor="end") + "".join(t(25 + i * 30, 72, d, 6.5, MUTE, "hind", 600, "middle") for i, d in enumerate("SMTWTFS"))
          + "".join(t(25 + ((n + 5) % 7) * 30, 90 + ((n + 5) // 7) * 24, str(n + 1), 8, INK, anchor="middle") + (dot(25 + ((n + 5) % 7) * 30, 95 + ((n + 5) // 7) * 24, 2.5, {3: TERRA, 9: SAFFRON, 20: LAGOON}[n]) if n in (3, 9, 20) else "") for n in range(30))
          + ln(222) + dot(18, 236, 3, TERRA) + t(26, 239, "Visit", 7, MUTE) + dot(64, 236, 3, SAFFRON) + t(72, 239, "Filter", 7, MUTE) + dot(108, 236, 3, LAGOON) + t(116, 239, "Tip", 7, MUTE) + tabbar(1))),
 O("cal_agenda", "Agenda List", "The next things in date order: visit, filter swap, seasonal tip. No grid.", ["clear", "simple", "practical"], "crew",
   screen(h1(14, 54, "Coming Up", 17) + "".join(ln(66 + i * 44) + rect(14, 74 + i * 44, 32, 30, CREAM, LINE, 4) + t(30, 86 + i * 44, m, 6, MUTE, "hind", 600, "middle") + t(30, 100 + i * 44, d, 12, INK, "khand", anchor="middle") + t(56, 88 + i * 44, n, 9, INK, "hind", 600) + t(56, 100 + i * 44, s, 7, MUTE) + dot(220, 89 + i * 44, 3.5, c) for i, (m, d, n, s, c) in enumerate([("NOV", "4", "Fall Visit With Danny", "9 to 11 AM · furnace, gutters", TERRA), ("NOV", "10", "Swap Furnace Filter", "16x25x1 · in your garage", SAFFRON), ("NOV", "21", "Winterize Hose Bibs", "2-minute tip", LAGOON), ("FEB", "3", "Winter Visit", "Not booked yet", "#A3A3A3")])) + tabbar(1))),
 "How Should The Maintenance Calendar Look?")
add(GC, "Up Keep: Calendar",
 O("cal_seasons", "Four Season Cards", "The year as four cards: Fall, Winter, Spring, Summer, each with what gets done.", ["seasonal", "warm", "clear"], "neighbor",
   screen(h1(14, 54, "Your Year Of Care", 17) + "".join(rect(14 + (i % 2) * 108, 64 + (i // 2) * 96, 104, 90, "#FFFFFF", LINE, 6) + rect(14 + (i % 2) * 108, 64 + (i // 2) * 96, 104, 5, c) + t(22 + (i % 2) * 108, 86 + (i // 2) * 96, s, 12, INK, "khand") + t(22 + (i % 2) * 108, 98 + (i // 2) * 96, d, 6.8, MUTE) + para(22 + (i % 2) * 108, 114 + (i // 2) * 96, w, 6.8, INK, 10) for i, (s, d, w, c) in enumerate([("Fall", "Nov 4 · booked", ["Furnace tune-up", "Gutters", "CO test"], TERRA), ("Winter", "Feb 3", ["Water heater", "Sump pump", "Detectors"], LAGOON), ("Spring", "May 5", ["AC tune-up", "Gutters", "Irrigation"], JUNGLE), ("Summer", "Aug 4", ["Dryer vent", "Caulk check", "GFCIs"], SAFFRON)])))),
 O("cal_timeline", "One Year Timeline", "A single line across the year with visit markers and a 'You Are Here' pin.", ["minimal", "system", "modern"], "concierge",
   screen(h1(14, 54, "Your Year Of Care", 17) + f'<line x1="24" y1="110" x2="216" y2="110" stroke="{LINE}" stroke-width="3"/><line x1="24" y1="110" x2="58" y2="110" stroke="{INK}" stroke-width="3"/>' + rect(46, 78, 24, 13, INK, r=3) + t(58, 87, "NOW", 6, "#FFFFFF", "hind", 600, "middle")
          + "".join(dot(x, 110, 6, c) + t(x, 130, m, 7, INK, "hind", 600, "middle") for x, m, c in [(64, "Nov", TERRA), (112, "Feb", LAGOON), (160, "May", JUNGLE), (208, "Aug", SAFFRON)])
          + "".join(ln(150 + i * 24) + t(14, 165 + i * 24, n, 8.5, INK) + t(226, 165 + i * 24, d, 8, MUTE, anchor="end") for i, (n, d) in enumerate([("Fall visit", "Nov 4 · booked"), ("Winter visit", "Feb 3"), ("Spring visit", "May 5"), ("Summer visit", "Aug 4")])))),
 "Season Cards Or A Timeline?")
add(GC, "Up Keep: Reminder Settings",
 O("rem_toggles", "Reminder Toggles By Type", "A row per reminder (visit day-before, filter swaps, seasonal tips, recalls) with its own switch.", ["control", "system", "detailed"], "system",
   screen(h1(14, 54, "Reminders", 17) + "".join(ln(66 + i * 34) + t(14, 84 + i * 34, n, 9, INK, "hind", 600) + t(14, 95 + i * 34, d, 6.8, MUTE) + toggle(202, 78 + i * 34, on, JUNGLE) for i, (n, d, on) in enumerate([("Day Before A Visit", "Text at 6 PM", True), ("Filter Swaps", "Every 90 days", True), ("Seasonal Tips", "4 a year", False), ("Recall Alerts", "Always on", True)])) + lbl(14, 216, "Send by") + chip(14, 222, "Text", True) + chip(58, 222, "Push") + chip(104, 222, "Email"))),
 O("rem_level", "One Simple Choice", "Pick how much you hear from us: Just Visits, Visits And Tips, or Everything.", ["simple", "calm", "guided"], "concierge",
   screen(h1(14, 54, "How Often Should We Remind You?", 15) + "".join(rect(14, 68 + i * 50, 212, 44, SEL if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 0, 1.4) + t(24, 86 + i * 50, n, 10, INK, "khand") + t(24, 100 + i * 50, d, 7, MUTE) + (t(216, 92 + i * 50, "✓", 11, INK, anchor="end") if i == 1 else "") for i, (n, d) in enumerate([("Just Visits", "A text the day before"), ("Visits And Tips", "Plus 4 seasonal tips a year"), ("Everything", "Plus filter swaps and reports")])) + btn(232, "Save"))),
 "How Should Reminders Be Set?")

HOMEBODY = lbl(14, 48, "Hi Sarah") + h1(14, 66, "Welcome Home", 17) + rect(14, 76, 212, 56, CREAM, LINE, 6) + t(22, 96, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(22, 114, "Tue, Nov 4 · 9 AM", 13, INK, "khand") + "".join(ln(142 + i * 22) + t(14, 157 + i * 22, n, 8.5, INK) + tag(176, 148 + i * 22, st, c) for i, (_, n, _, st, c) in enumerate(SYS[:4]))
add(GD, "Up Keep: App Navigation",
 O("nav_tabs", "Bottom Tab Bar", "Four tabs at the bottom: Home, Calendar, Record, Invite. Always one tap away.", ["app-like", "system", "clear"], "system", screen(HOMEBODY + tabbar(0))),
 O("nav_menu", "Menu Button In The Header", "No tab bar. A menu icon at the top right opens the same four pages.", ["minimal", "clean", "quiet"], "concierge",
   screen(HOMEBODY, right="".join(f'<line x1="206" y1="{12+i*5}" x2="224" y2="{12+i*5}" stroke="{INK}" stroke-width="1.6"/>' for i in range(3)))),
 "How Should Members Get Around The App?")
add(GC, "Up Keep: Calendar Sync",
 O("sync_each", "Add Each Visit To Calendar", "An 'Add To Calendar' button on every booked visit.", ["control", "simple", "clear"], "crew",
   screen(h1(14, 54, "Fall Visit", 17) + t(14, 70, "Tue, Nov 4 · 9 to 11 AM · Danny", 8, MUTE) + "".join(t(14, 92 + i * 13, "✓ " + l, 8, INK) for i, l in enumerate(["Furnace tune-up", "Gutter clean", "Smoke and CO test"])) + btn(150, "Add To Calendar", "outline") + btn(184, "Reschedule", "outline", col=MUTE))),
 O("sync_all", "Sync The Whole Schedule", "One switch: 'Keep my calendar in sync.' Every visit and change shows up on its own.", ["system", "automatic", "lively"], "system",
   screen(h1(14, 54, "Calendar Sync", 17) + rect(14, 66, 212, 50, CREAM, LINE, 6) + t(22, 86, "Keep My Calendar In Sync", 10, INK, "khand") + t(22, 100, "Visits, changes and filter swaps", 7, MUTE) + toggle(196, 84, True, JUNGLE)
          + "".join(chip(14 + i * 72, 128, n, i == 0, LAGOON, 66) for i, n in enumerate(["Google", "Apple", "Outlook"])) + "".join(ln(166 + i * 22) + dot(18, 177 + i * 22, 3, c) + t(28, 180 + i * 22, n, 8, INK) for i, (n, c) in enumerate([("Nov 4 · Fall visit", TERRA), ("Nov 10 · Filter swap", SAFFRON), ("Feb 3 · Winter visit", TERRA)])))),
 "Add Visits One By One Or Sync Them All?")

# ===================== 3. Recall + warranty (4) =====================
add(GA, "Up Keep: Recall Alert",
 O("recall_banner", "Recall As A Dashboard Banner", "A saffron banner on the dashboard. Tap for the fix. The rest of the page stays normal.", ["calm", "contained", "clear"], "system",
   screen(rect(14, 42, 212, 50, "#FFF6DD", SAFFRON, 4) + warn(22, 52, SAFFRON, .9) + t(48, 60, "Recall On Your Water Heater", 9.5, INK, "khand") + t(48, 72, "Rheem XG50T · free fix · no cost to you", 7, MUTE) + link(48, 84, "See What To Do", INK)
          + h1(14, 116, "Welcome Home", 16) + "".join(ln(126 + i * 22) + t(14, 141 + i * 22, n, 8.5, INK) + tag(176, 132 + i * 22, st if n != "Water Heater" else "Recall", c if n != "Water Heater" else SAFFRON) for i, (_, n, _, st, c) in enumerate(SYS)) + tabbar(0))),
 O("recall_full", "Recall As A Full Screen", "A full page: what's wrong, is it safe, and one button to book the free fix.", ["urgent", "direct", "safety"], "crew",
   screen(warn(102, 44, TERRA, 1.5) + h1(120, 98, "Your Water Heater Is Recalled", 17, anchor="middle") + t(120, 112, "Rheem XG50T · serial 0423-B", 7.5, MUTE, anchor="middle")
          + "".join(ln(124 + i * 26) + t(14, 140 + i * 26, l, 7.5, MUTE) + t(226, 140 + i * 26, v, 8, INK, "hind", 600, "end") for i, (l, v) in enumerate([("Problem", "Gas valve can stick"), ("Is it safe?", "Yes, for now"), ("Cost to you", "$0")])) + btn(212, "Book The Free Fix", col=TERRA) + link(120, 256, "Remind Me Tomorrow", MUTE, "middle"))),
 "How Should A Recall Alert Show?")
add(GA, "Up Keep: Recall Alert",
 O("recall_steps", "Recall Fix As 3 Steps", "Numbered steps with a progress line: We Found It, Parts Ordered, Danny Installs.", ["guided", "system", "reassuring"], "system",
   screen(h1(14, 56, "Recall Fix: Water Heater", 15) + f'<line x1="26" y1="76" x2="26" y2="196" stroke="{LINE}" stroke-width="2"/><line x1="26" y1="76" x2="26" y2="136" stroke="{JUNGLE}" stroke-width="2"/>'
          + "".join(dot(26, 80 + i * 56, 8, c) + t(26, 84 + i * 56, str(i + 1), 8, "#FFFFFF", "hind", 600, "middle") + t(44, 84 + i * 56, n, 10, INK, "khand") + t(44, 96 + i * 56, d, 7, MUTE) for i, (n, d, c) in enumerate([("We Found It", "Oct 12 · from your label photo", JUNGLE), ("Parts Ordered", "Arriving Oct 20", JUNGLE), ("Danny Installs", "Book a 30-minute slot", "#BDB6AA")])) + btn(230, "Pick A Time", col=TERRA))),
 O("recall_letter", "Recall Fix As A Note From Max", "A short first-person note explaining the recall and that we'll handle it.", ["personal", "warm", "calm"], "neighbor",
   screen(h1(14, 56, "About Your Water Heater", 15) + rect(14, 66, 212, 136, CREAM, LINE, 6) + para(24, 86, ["Hi Sarah,", "", "Rheem recalled your water heater's gas", "valve. It's safe to use, and the fix is", "free. Danny will swap the part on a", "30-minute visit.", "", "Max"], 8, INK, 12) + btn(214, "Pick A Time") + link(120, 258, "Questions? Text Max", LAGOON, "middle"))),
 "How Should The Recall Fix Be Explained?")
add(GA, "Up Keep: Warranty Check",
 O("war_bars", "Warranty As Time Bars", "Each system shows a bar of warranty time left, colored green, saffron or grey.", ["visual", "system", "lively"], "system",
   screen(h1(14, 54, "Warranty Check", 17) + t(14, 68, "From your label photos", 7.5, MUTE) + "".join(ln(78 + i * 42) + t(14, 96 + i * 42, n, 9, INK, "hind", 600) + t(226, 96 + i * 42, l, 7.5, c if c != "#BDB6AA" else MUTE, "hind", 600, "end") + rect(14, 102 + i * 42, 212, 6, "#EEEAE4", r=3) + rect(14, 102 + i * 42, 212 * f, 6, c, r=3) for i, (n, l, f, c) in enumerate([("Furnace", "6 yrs left", .6, JUNGLE), ("AC Unit", "8 months left", .1, SAFFRON), ("Water Heater", "Expired", 0, "#BDB6AA"), ("Dishwasher", "3 yrs left", .5, JUNGLE)])))),
 O("war_cards", "Warranty As Covered / Not Covered", "Two simple groups: Covered and Not Covered, with end dates.", ["simple", "clear", "direct"], "crew",
   screen(h1(14, 54, "Warranty Check", 17) + shield(14, 64, JUNGLE, .7) + t(36, 78, "COVERED", 7, JUNGLE, "hind", 600, extra='letter-spacing="1"') + "".join(ln(86 + i * 22) + t(14, 101 + i * 22, n, 8.5, INK) + t(226, 101 + i * 22, d, 7.5, MUTE, anchor="end") for i, (n, d) in enumerate([("Furnace", "Until 2032"), ("Dishwasher", "Until 2029"), ("AC Unit", "Until Jun 2027")]))
          + shield(14, 158, "#A3A3A3", .7, False) + t(36, 172, "NOT COVERED", 7, MUTE, "hind", 600, extra='letter-spacing="1"') + ln(180) + t(14, 195, "Water Heater", 8.5, INK) + t(226, 195, "Ended 2023", 7.5, MUTE, anchor="end") + btn(222, "Add A Receipt", "outline"))),
 "How Should Warranty Status Show?")
add(GA, "Up Keep: Warranty Check",
 O("war_lookup", "Lookup Form First", "Type brand and model, tap Check. Results appear under it.", ["practical", "fast", "tool"], "crew",
   screen(h1(14, 56, "Check A Warranty", 17) + field(70, "Brand", "Trane") + field(100, "Model", "XR14") + btn(136, "Check") + rect(14, 172, 212, 44, "#FFFFFF", LINE, 4) + rect(14, 172, 4, 44, SAFFRON) + t(26, 190, "Covered Until Jun 2027", 10, INK, "khand") + t(26, 204, "Parts only · 8 months left", 7.5, MUTE))),
 O("war_snap", "Snap The Label First", "A camera button leads. We read the label and fill in the warranty for them.", ["easy", "modern", "guided"], "system",
   screen(h1(14, 56, "Check A Warranty", 17) + para(14, 72, ["Snap the sticker on the unit.", "We'll read it and look it up."]) + rect(14, 96, 212, 110, "#FFFFFF", "#CFC8BC", 6, 1.3, 'stroke-dasharray="4 3"') + icon("cam", 104, 128, 32, "duo", LAGOON) + t(120, 186, "Tap To Snap A Label", 8, INK, "hind", 600, "middle") + btn(220, "Open Camera") + link(120, 264, "Type It Instead", MUTE, "middle"))),
 "How Should A Warranty Check Start?")

# ===================== 4. Label snap result (3) =====================
LS = "Up Keep: Label-Snap Result"
add(GF, LS,
 O("snap_fields", "Read-Back As Fields", "Brand, model and serial shown as filled fields they can edit, under the photo.", ["clear", "editable", "system"], "system",
   screen(photo(14, 42, 212, 66, "label", 6) + tag(20, 48, "Read In 2 Sec", JUNGLE, True) + field(124, "Brand", "Rheem") + field(154, "Model", "XG50T06EC36U1") + field(184, "Serial", "0423B12345") + btn(222, "Looks Right") + link(120, 264, "Retake Photo", MUTE, "middle"))),
 O("snap_card", "Read-Back As A Product Card", "One card: 'Rheem 50-Gallon Gas Water Heater, 2017' with age and recall status chips.", ["friendly", "visual", "lively"], "neighbor",
   screen(t(14, 52, "We Found It", 17, INK, "khand") + rect(14, 62, 212, 130, "#FFFFFF", LINE, 8) + photo(22, 70, 64, 64, "label", 6) + t(94, 84, "Rheem", 8, MUTE) + t(94, 100, "50-Gal Gas", 12, INK, "khand") + t(94, 114, "Water Heater", 12, INK, "khand") + t(94, 128, "Made 2017", 7.5, MUTE)
          + tag(22, 146, "9 Years Old", SAFFRON) + tag(88, 146, "No Recalls", JUNGLE) + tag(150, 146, "Warranty Ended", "#737373") + t(22, 180, "Model XG50T · Serial 0423B…", 7, MUTE) + btn(206, "Looks Right") + btn(238, "Fix It", "outline"))),
 "How Should The Label Read-Back Look?")
add(GF, LS,
 O("snap_conf_two", "Two Buttons: Looks Right / Fix It", "Two clear buttons under the result.", ["direct", "clear", "fast"], "crew",
   screen(photo(14, 42, 212, 90, "label", 6) + h1(14, 154, "Rheem XG50T", 18) + t(14, 168, "Serial 0423B12345 · made 2017", 7.5, MUTE) + btn(186, "Looks Right", col=JUNGLE) + btn(220, "Fix It", "outline"))),
 O("snap_conf_tap", "Tap Any Line To Fix", "No Fix button. Each line has a small pencil; one Save at the bottom.", ["minimal", "flexible", "calm"], "concierge",
   screen(photo(14, 42, 212, 90, "label", 6) + "".join(ln(140 + i * 26) + t(14, 155 + i * 26, l, 7, MUTE) + t(70, 155 + i * 26, v, 8.5, INK, "hind", 600) + t(226, 155 + i * 26, "✎", 9, LAGOON, anchor="end") for i, (l, v) in enumerate([("Brand", "Rheem"), ("Model", "XG50T"), ("Serial", "0423B12345")])) + btn(230, "Save"))),
 "How Should They Confirm The Label?")
add(GF, LS,
 O("snap_multi", "All Labels In One Summary", "After several snaps, one list of everything read, each with a check.", ["organized", "summary", "system"], "system",
   screen(h1(14, 56, "4 Labels Read", 17) + "".join(ln(66 + i * 34) + photo(14, 72 + i * 34, 28, 22, "label", 3) + t(50, 84 + i * 34, n, 8.5, INK, "hind", 600) + t(50, 95 + i * 34, m, 6.8, MUTE) + icon("check", 206, 76 + i * 34, 16, "duo", JUNGLE) for i, (n, m) in enumerate([("Water Heater", "Rheem XG50T"), ("Furnace", "Carrier 59SC5"), ("AC Unit", "Trane XR14"), ("Panel", "Square D QO")])) + btn(216, "Get My Final Price", col=TERRA))),
 O("snap_each", "One Result Per Snap", "Each photo gets its own result screen right away, then Next Label.", ["focused", "step", "clear"], "neighbor",
   screen(lbl(14, 50, "Label 2 of 4") + pbar(56, .5) + photo(14, 68, 212, 90, "label", 6) + h1(14, 180, "Carrier 59SC5 Furnace", 16) + t(14, 194, "Made 2019 · 7 years old", 7.5, MUTE) + tag(14, 202, "No Recalls", JUNGLE) + btn(226, "Next Label"))),
 "One Summary Or One Result At A Time?")

# ===================== 5. Booking + rescheduling (3) =====================
BK = "Up Keep: Booking A Visit"
add(GB, BK,
 O("book_chips", "Day Strip And Time Chips", "Swipe a strip of days, then tap a time window chip.", ["fast", "modern", "lively"], "neighbor",
   screen(h1(14, 54, "Book Your Fall Visit", 16) + "".join(rect(14 + i * 43, 64, 39, 44, INK if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 4) + t(33 + i * 43, 80, d, 6.5, "#FFFFFF" if i == 1 else MUTE, "hind", 600, "middle") + t(33 + i * 43, 98, n, 13, "#FFFFFF" if i == 1 else INK, "khand", anchor="middle") for i, (d, n) in enumerate([("MON", "3"), ("TUE", "4"), ("WED", "5"), ("THU", "6"), ("FRI", "7")]))
          + lbl(14, 128, "Tue, Nov 4") + chip(14, 136, "8 to 10 AM") + chip(84, 136, "9 to 11 AM", True, TERRA) + chip(154, 136, "1 to 3 PM") + chip(14, 162, "3 to 5 PM") + t(14, 200, "Danny · about 90 minutes", 7.5, MUTE) + btn(230, "Book Tue 9 To 11 AM"))),
 O("book_list", "Plain List Of Open Slots", "The next six open times as rows. Tap one.", ["simple", "clear", "practical"], "crew",
   screen(h1(14, 54, "Book Your Fall Visit", 16) + t(14, 68, "Next open times with Danny", 7.5, MUTE) + "".join(ln(78 + i * 26) + t(14, 95 + i * 26, d, 8.5, INK, "hind", 600 if i == 1 else 400) + t(226, 95 + i * 26, "✓" if i == 1 else "›", 9, TERRA if i == 1 else MUTE, anchor="end") for i, d in enumerate(["Mon, Nov 3 · 1 to 3 PM", "Tue, Nov 4 · 9 to 11 AM", "Tue, Nov 4 · 3 to 5 PM", "Wed, Nov 5 · 8 to 10 AM", "Thu, Nov 6 · 1 to 3 PM", "Fri, Nov 7 · 9 to 11 AM"])) + btn(240, "Book This Time"))),
 "How Should Booking A Visit Work?")
add(GB, "Up Keep: Rescheduling",
 O("resch_sheet", "Reschedule In A Bottom Sheet", "Tap Reschedule and a sheet slides up over the dashboard with 3 new times.", ["quick", "modern", "light"], "system",
   screen(h1(14, 56, "Welcome Home", 16) + rect(14, 66, 212, 60, CREAM, LINE, 6) + t(22, 86, "Tue, Nov 4 · 9 AM", 12, INK, "khand") + rect(0, 32, W, H, INK, extra='opacity=".25"') + rect(0, 124, W, 180, "#FFFFFF", r=12) + rect(108, 130, 24, 3, "#D4D4D4", r=1.5) + h1(14, 154, "Move Your Visit", 14)
          + "".join(rect(14, 164 + i * 28, 212, 22, SEL if i == 0 else "#FFFFFF", INK if i == 0 else LINE, 0, 1.3) + t(24, 179 + i * 28, s, 8, INK) for i, s in enumerate(["Wed, Nov 5 · 9 to 11 AM", "Thu, Nov 6 · 1 to 3 PM", "Mon, Nov 10 · 9 to 11 AM"])) + btn(258, "Move It", col=TERRA, h=22))),
 O("resch_page", "Reschedule On Its Own Page", "A full page with the current time crossed out and a new calendar picker.", ["clear", "deliberate", "calm"], "concierge",
   screen(link(14, 48, "← Back", INK) + h1(14, 72, "Move Your Visit", 17) + rect(14, 82, 212, 30, "#F5F5F5", LINE, 4) + t(22, 101, "Tue, Nov 4 · 9 AM", 9, MUTE, extra='text-decoration="line-through"') + t(218, 101, "CURRENT", 6, MUTE, "hind", 600, "end")
          + lbl(14, 130, "Pick a new day") + "".join(rect(14 + (i % 4) * 54, 136 + (i // 4) * 32, 50, 26, INK if i == 2 else "#FFFFFF", INK if i == 2 else LINE, 0) + t(39 + (i % 4) * 54, 153 + (i // 4) * 32, d, 7.5, "#FFFFFF" if i == 2 else INK, "hind", 600, "middle") for i, d in enumerate(["Mon 3", "Wed 5", "Thu 6", "Fri 7", "Mon 10", "Tue 11", "Wed 12", "Thu 13"])) + chip(14, 210, "9 to 11 AM", True) + chip(84, 210, "1 to 3 PM") + btn(244, "Confirm New Time"))),
 "Where Should Rescheduling Happen?")
add(GB, BK,
 O("book_windows", "2-Hour Arrival Windows", "Times shown as windows: '9 to 11 AM'. Honest about traffic.", ["honest", "realistic", "practical"], "crew",
   screen(h1(14, 54, "Pick A Time", 17) + "".join(rect(14, 66 + i * 34, 212, 28, SEL if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 0, 1.3) + t(24, 84 + i * 34, s, 9, INK, "hind", 600) + t(216, 84 + i * 34, n, 7, MUTE, anchor="end") for i, (s, n) in enumerate([("8 to 10 AM", "Morning"), ("9 to 11 AM", "Morning"), ("1 to 3 PM", "Afternoon"), ("3 to 5 PM", "Afternoon")])) + t(14, 218, "Danny texts 30 minutes before he arrives.", 7.5, MUTE) + btn(236, "Book 9 To 11 AM"))),
 O("book_exact", "Exact Start Times", "Times shown as exact starts: '9:00 AM'. Feels precise.", ["precise", "premium", "confident"], "concierge",
   screen(h1(14, 54, "Pick A Time", 17) + "".join(chip(14 + (i % 3) * 72, 68 + (i // 3) * 30, s, i == 1, INK, 66) for i, s in enumerate(["8:00 AM", "9:00 AM", "10:30 AM", "1:00 PM", "2:30 PM", "4:00 PM"])) + t(14, 150, "Danny arrives on time or your next visit is free.", 7.5, MUTE) + btn(236, "Book 9:00 AM"))),
 "Arrival Windows Or Exact Times?")

# ===================== 6. Tech arrival (2) =====================
TA = "Up Keep: Tech Arrival"
add(GB, TA,
 O("arr_push", "Lock-Screen Push With Photo", "'Danny is 15 minutes away' with his photo and a gray van line.", ["personal", "warm", "human"], "neighbor",
   phone_frame(notif(80, "Danny Is 15 Minutes Away", ["Gray Up Keep van · plate EKT 4421", "He'll ring the bell when he arrives."], extra=face(206, 116, 10)) + notif(160, "Tip: Clear A Path To The Furnace", ["Danny will need about 3 feet around it."], accent=LAGOON))),
 O("arr_map", "Live Map With ETA", "Opens to a small map, a moving van dot and a big ETA number.", ["live", "system", "modern"], "system",
   screen(f'<rect x="0" y="32" width="{W}" height="140" fill="#EEF0EA"/>' + "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#FFFFFF" stroke-width="7"/>' for a, b, c, d in [(0, 80, 240, 100), (60, 32, 90, 172), (150, 32, 170, 172), (0, 140, 240, 130)])
          + f'<path d="M78 120 L160 110 L165 70" fill="none" stroke="{LAGOON}" stroke-width="3" stroke-dasharray="5 3"/>' + dot(78, 120, 7, LAGOON) + dot(165, 70, 7, TERRA) + rect(160, 54, 10, 8, "#FFFFFF", r=1)
          + t(14, 200, "15", 34, INK, "khand") + t(52, 200, "min away", 9, MUTE) + face(200, 190, 12) + t(14, 218, "Danny · gray Up Keep van", 7.5, MUTE) + btn(234, "Text Danny", "outline", w=100, size=8) + btn(234, "Call", "outline", x=126, w=100, size=8))),
 "How Should The Tech Arrival Notice Look?")
add(GB, TA,
 O("arr_stage", "Arrival Steps Bar", "A 4-step bar: Booked, On The Way, Here, Report Ready, with the current step lit.", ["system", "clear", "lively"], "system",
   screen(h1(14, 56, "Today's Visit", 17) + "".join(dot(30 + i * 60, 82, 7, c) + t(30 + i * 60, 104, n, 6.5, INK if i <= 1 else MUTE, "hind", 600, "middle") for i, (n, c) in enumerate([("Booked", JUNGLE), ("On The Way", LAGOON), ("Here", "#D4D4D4"), ("Report", "#D4D4D4")])) + f'<line x1="37" y1="82" x2="83" y2="82" stroke="{JUNGLE}" stroke-width="2"/><line x1="97" y1="82" x2="203" y2="82" stroke="#D4D4D4" stroke-width="2"/>'
          + rect(14, 122, 212, 60, CREAM, LINE, 6) + face(42, 146, 12) + t(64, 144, "Danny Is On The Way", 11, INK, "khand") + t(64, 158, "Arriving 9:15 to 9:25 AM", 7.5, MUTE) + btn(198, "Text Danny", "outline"))),
 O("arr_simple", "One Big Status Line", "Just one sentence, big: 'Danny arrives around 9:20.' and a Text button.", ["minimal", "calm", "direct"], "concierge",
   screen(face(120, 92, 22) + h1(120, 158, "Danny Arrives Around 9:20", 18, anchor="middle") + t(120, 174, "Gray Up Keep van · about 90 minutes", 7.5, MUTE, anchor="middle") + btn(200, "Text Danny"))),
 "How Much Detail On Arrival Day?")

# ===================== 7. 4-step overview + Learn More + ZIP/sq ft (7) =====================
STEPS = [("Answer A Few Questions", "7 quick taps"), ("Take Some Photos", "Optional · final price"), ("Review Your Membership", "Gold or Platinum"), ("Sign Up", "Pick a payment plan")]
add(GF, "Up Keep: 4-Step Overview",
 O("ov_numbers", "Big Numbered Rows", "Four rows with big Khand numbers in a colored square each.", ["clear", "lively", "multi-accent"], "neighbor",
   screen(lbl(14, 50, "How it works") + h1(14, 70, "Four Quick Steps", 18) + "".join(ln(82 + i * 40) + rect(14, 90 + i * 40, 26, 26, c) + t(27, 109 + i * 40, str(i + 1), 15, "#FFFFFF", "khand", anchor="middle") + t(50, 101 + i * 40, n, 9.5, INK, "hind", 600) + t(50, 112 + i * 40, d, 7, MUTE) for i, ((n, d), c) in enumerate(zip(STEPS, [TERRA, LAGOON, JUNGLE, INK]))) + btn(250, "Continue To Step 1"))),
 O("ov_stepper", "Horizontal Stepper", "Four connected circles across the top, then the first step in detail.", ["system", "compact", "modern"], "system",
   screen(lbl(14, 50, "How it works") + h1(14, 70, "Four Quick Steps", 18) + f'<line x1="36" y1="94" x2="204" y2="94" stroke="{LINE}" stroke-width="2"/>' + "".join(dot(36 + i * 56, 94, 10, INK if i == 0 else "#FFFFFF") + f'<circle cx="{36+i*56}" cy="94" r="10" fill="none" stroke="{INK}" stroke-width="1.4"/>' + t(36 + i * 56, 98, str(i + 1), 9, "#FFFFFF" if i == 0 else INK, "khand", anchor="middle") + t(36 + i * 56, 118, n.split()[0], 6.5, MUTE, "hind", 600, "middle") for i, (n, _) in enumerate(STEPS))
          + rect(14, 134, 212, 80, CREAM, LINE, 6) + t(24, 156, "Step 1: Answer A Few Questions", 11, INK, "khand") + para(24, 172, ["ZIP, home size and your systems.", "About 2 minutes. Tap Unsure anytime."], 7.5, MUTE, 11) + btn(234, "Start Step 1"))),
 "How Should The 4-Step Overview Look?")
add(GF, "Up Keep: 4-Step Overview",
 O("ov_time", "Each Step Shows Its Time", "'2 min', '3 min', '1 min', '1 min' on the right of each step, plus a total.", ["transparent", "reassuring", "specific"], "system",
   screen(h1(14, 56, "Four Quick Steps", 18) + t(226, 56, "≈ 7 MIN", 7, LAGOON, "hind", 600, "end") + "".join(ln(68 + i * 36) + t(14, 90 + i * 36, f"{i+1}. {n}", 9, INK, "hind", 600) + t(226, 90 + i * 36, m, 7.5, MUTE, anchor="end") for i, ((n, _), m) in enumerate(zip(STEPS, ["2 min", "3 min", "1 min", "1 min"]))) + btn(226, "Continue To Step 1"))),
 O("ov_notime", "Steps Without Times", "Just the four steps and what each does. No minutes.", ["clean", "calm", "minimal"], "concierge",
   screen(h1(14, 56, "Four Quick Steps", 18) + "".join(ln(68 + i * 36) + t(14, 88 + i * 36, f"{i+1}. {n}", 9, INK, "hind", 600) + t(14, 98 + i * 36, d, 7, MUTE) for i, (n, d) in enumerate(STEPS)) + btn(226, "Continue To Step 1"))),
 "Show How Long Each Step Takes?")
ACC = ["What's Included", "How It Works", "Recall Tracking", "Service Area: Metro Detroit", "FAQ"]
add(GF, "Up Keep: Learn More",
 O("acc_plus", "Plus / Minus Rows", "Plain rows with + and −. One section open shows a short checklist.", ["minimal", "classic", "clear"], "concierge",
   screen(lbl(14, 50, "Learn more") + "".join(ln(58 + i * 26 + (64 if i > 0 else 0)) + t(14, 75 + i * 26 + (64 if i > 0 else 0), n, 9, INK, "hind", 600) + t(226, 75 + i * 26 + (64 if i > 0 else 0), "−" if i == 0 else "+", 12, INK, anchor="end") for i, n in enumerate(ACC)) + para(14, 92, ["✓ Fall furnace and spring AC tune-ups", "✓ Water heater flush", "✓ Gutters, dryer vent, detectors", "✓ A written report every visit"], 7.5, MUTE, 12))),
 O("acc_icons", "Icon Cards That Expand", "Each section is a small card with a colored icon; tap to expand.", ["visual", "lively", "multi-accent"], "neighbor",
   screen(lbl(14, 50, "Learn more") + "".join(rect(14, 58 + i * 40 + (54 if i > 0 else 0), 212, 34 + (54 if i == 0 else 0), "#FFFFFF", LINE, 6) + rect(22, 66 + i * 40 + (54 if i > 0 else 0), 18, 18, c + "22", r=4) + dot(31, 75 + i * 40 + (54 if i > 0 else 0), 4, c) + t(48, 79 + i * 40 + (54 if i > 0 else 0), n, 9, INK, "hind", 600) + t(218, 79 + i * 40 + (54 if i > 0 else 0), "▴" if i == 0 else "▾", 8, MUTE, anchor="end") for i, (n, c) in enumerate(zip(ACC, [TERRA, LAGOON, SAFFRON, JUNGLE, BERRY]))) + para(48, 98, ["Tune-ups, water heater flush, gutters,", "dryer vent, detectors and a report", "after every visit."], 7.2, MUTE, 11))),
 "How Should Learn More Look?")
add(GF, "Up Keep: ZIP Question",
 O("zip_big", "One Big ZIP Box", "A large single box with big digits and the service area in small text.", ["focused", "clear", "simple"], "system",
   screen(link(14, 50, "← Back", INK) + pbar(60, .14) + lbl(14, 84, "Question 1 of 7") + h1(14, 106, "What's Your ZIP Code?", 19) + rect(14, 120, 212, 46, "#FFFFFF", INK, 0, 1.8) + t(120, 152, "4 8 3 2 2", 22, INK, "khand", anchor="middle") + tag(14, 176, "✓ We Serve Novi", JUNGLE) + t(14, 204, "Wayne, Oakland and Macomb counties", 7, MUTE) + btn(232, "Next"))),
 O("zip_map", "ZIP With A Service Map", "A small map of metro Detroit shades the service area and drops a pin on their ZIP.", ["visual", "local", "reassuring"], "neighbor",
   screen(link(14, 50, "← Back", INK) + pbar(60, .14) + h1(14, 88, "What's Your ZIP Code?", 19) + field(98, "ZIP or address", "48322") + rect(14, 132, 212, 86, "#EEF0EA", LINE, 6) + f'<path d="M40 150 L120 140 L190 158 L196 200 L110 210 L46 196 Z" fill="{LAGOON}" opacity=".18" stroke="{LAGOON}" stroke-width="1.2"/>' + dot(98, 172, 5, TERRA) + t(108, 175, "Novi", 7, INK, "hind", 600) + btn(232, "Next"))),
 "How Should The ZIP Question Look?")
add(GF, "Up Keep: Home Size Question",
 O("sqft_chips", "Size As Range Buttons", "Six tappable ranges, like the live app: 'Under 2,000', '2,000 to 3,000'…", ["easy", "fast", "clear"], "crew",
   screen(lbl(14, 52, "Question 2 of 7") + h1(14, 74, "About How Big Is Your Home?", 16) + "".join(rect(14 + (i % 2) * 108, 88 + (i // 2) * 36, 104, 30, SEL if i == 1 else "#FFFFFF", INK if i == 1 else LINE, 0, 1.3) + t(66 + (i % 2) * 108, 107 + (i // 2) * 36, s, 7.8, INK, "hind", 600, "middle") for i, s in enumerate(["Under 2,000", "2,000 to 3,000", "3,000 to 4,000", "4,000 to 5,000", "5,000 to 6,000", "Not Sure"])) + btn(232, "Next"))),
 O("sqft_slider", "Size As A Slider", "Drag a slider; the number and a little house grow as they go.", ["playful", "tactile", "lively"], "neighbor",
   screen(lbl(14, 52, "Question 2 of 7") + h1(14, 74, "About How Big Is Your Home?", 16) + f'<g transform="translate(60,70) scale(.5)">' + f'<path d="M50 120 L120 62 L190 120" fill="none" stroke="{INK}" stroke-width="3"/><rect x="66" y="118" width="108" height="56" fill="{SEL}" stroke="{INK}" stroke-width="3"/></g>' + t(120, 186, "2,400 sq ft", 20, INK, "khand", anchor="middle")
          + rect(14, 198, 212, 6, "#EEEAE4", r=3) + rect(14, 198, 80, 6, TERRA, r=3) + f'<circle cx="94" cy="201" r="9" fill="#FFFFFF" stroke="{TERRA}" stroke-width="2"/>' + t(14, 220, "1,000", 6.5, MUTE) + t(226, 220, "6,000+", 6.5, MUTE, anchor="end") + btn(240, "Next"))),
 "How Should Home Size Be Asked?")
add(GF, "Up Keep: ZIP Question",
 O("zip_waitlist", "Out Of Area: Join The Waitlist", "'We're not in 90210 yet.' with an email box to hear when we are.", ["honest", "helpful", "warm"], "neighbor",
   screen(link(14, 50, "← Back", INK) + h1(14, 82, "We're Not In 90210 Yet", 18) + para(14, 98, ["We serve metro Detroit today. Want a", "heads-up when we come to you?"]) + field(126, "Email", "sarah@email.com") + btn(166, "Tell Me When") + link(120, 214, "Try Another ZIP", LAGOON, "middle"))),
 O("zip_continue", "Out Of Area: Estimate Anyway", "A saffron warning line, then they can still see a sample estimate.", ["flexible", "direct", "practical"], "crew",
   screen(link(14, 50, "← Back", INK) + h1(14, 82, "What's Your ZIP Code?", 18) + field(92, "ZIP or address", "90210") + rect(14, 126, 212, 34, "#FFF6DD", SAFFRON, 0) + t(22, 141, "90210 is outside metro Detroit.", 7.8, INK, "hind", 600) + t(22, 153, "You can still see a sample estimate.", 7.3, MUTE) + btn(176, "See A Sample Estimate"))),
 "What Happens Outside The Service Area?")

# ===================== 8. Add-on detail + payment plan (5) =====================
add(GP, "Up Keep: Add-On Detail",
 O("addon_photo", "Add-On Detail With A Photo", "Tap Window Washing: a photo, what's done, how often and the price.", ["visual", "clear", "warm"], "neighbor",
   screen(link(14, 48, "← Add-Ons", INK) + photo(14, 56, 212, 80, "house", 6) + h1(14, 158, "Exterior Window Washing", 15) + t(14, 172, "Outside glass, once or twice a year", 7.5, MUTE) + t(14, 198, "$19", 22, INK, "khand") + t(40, 198, "/ month · about $225 a year", 8, MUTE) + btn(214, "Add To My Plan", col=TERRA) + t(120, 256, "Done by a vetted partner, scheduled by us", 6.8, MUTE, anchor="middle"))),
 O("addon_facts", "Add-On Detail As Facts", "No photo: a short fact table (how often, who does it, time, price).", ["practical", "factual", "system"], "system",
   screen(link(14, 48, "← Add-Ons", INK) + h1(14, 74, "Exterior Window Washing", 15) + "".join(ln(86 + i * 26) + t(14, 103 + i * 26, l, 7.5, MUTE) + t(226, 103 + i * 26, v, 8, INK, "hind", 600, "end") for i, (l, v) in enumerate([("How often", "1 to 2 times a year"), ("Who", "Vetted partner"), ("Time", "About 2 hours"), ("Price", "$150 to $302 a year")])) + btn(214, "Add To My Plan", col=TERRA))),
 "How Should An Add-On Detail Look?")
add(GP, "Up Keep: Add-On Detail",
 O("addon_range", "Price As A Range", "'$150 to $302 a year' with a note that the final price comes after a look.", ["honest", "transparent", "careful"], "crew",
   screen(h1(14, 56, "Chimney Sweep", 17) + t(14, 92, "$129 – $381", 26, INK, "khand") + t(14, 106, "per sweep · set after we see it", 7.5, MUTE) + ln(118) + para(14, 134, ["Wood-burning chimney clean and a", "Level 1 safety check."], 8, INK, 12) + btn(214, "Add To My Plan"))),
 O("addon_mid", "Price As One Number", "'$21 / month' with the range tucked under a small 'Why?' link.", ["simple", "clear", "friendly"], "neighbor",
   screen(h1(14, 56, "Chimney Sweep", 17) + t(14, 92, "$21", 26, INK, "khand") + t(52, 92, "/ month", 9, MUTE) + link(14, 108, "Why This Price?", LAGOON) + ln(118) + para(14, 134, ["Wood-burning chimney clean and a", "Level 1 safety check."], 8, INK, 12) + btn(214, "Add To My Plan"))),
 "Range Or One Number?")
add(GP, "Up Keep: Payment Plan",
 O("pay_cards", "Stacked Plan Cards", "Three stacked cards: Monthly, Quarterly, Yearly (10% off), with the selected one outlined.", ["clear", "comparable", "system"], "system",
   screen(h1(14, 54, "How Do You Want To Pay?", 15) + "".join(rect(14, 64 + i * 50, 212, 44, SEL if i == 0 else "#FFFFFF", INK if i == 0 else LINE, 0, 1.4) + f'<circle cx="28" cy="{86+i*50}" r="6" fill="{"#FFFFFF"}" stroke="{INK}" stroke-width="1.4"/>' + (dot(28, 86 + i * 50, 3, INK) if i == 0 else "") + t(42, 83 + i * 50, n, 9.5, INK, "hind", 600) + t(42, 95 + i * 50, d, 7, MUTE) + t(216, 89 + i * 50, p, 11, INK, "khand", anchor="end") for i, (n, d, p) in enumerate([("Monthly", "Cancel anytime", "$232/mo"), ("Quarterly", "4 payments a year", "$695"), ("Yearly", "Save 10%", "$2,502")])) + tag(150, 164, "Save $278", JUNGLE, True) + btn(230, "Continue"))),
 O("pay_toggle", "Segmented Toggle", "A three-way switch at the top changes the one big price below.", ["compact", "modern", "lively"], "neighbor",
   screen(h1(14, 54, "How Do You Want To Pay?", 15) + rect(14, 66, 212, 26, "#F5F5F5", LINE, 0) + rect(16, 68, 69, 22, INK) + "".join(t(50 + i * 71, 82, n, 7.5, "#FFFFFF" if i == 0 else INK, "hind", 600, "middle") for i, n in enumerate(["Monthly", "Quarterly", "Yearly −10%"]))
          + t(120, 140, "$232", 40, INK, "khand", anchor="middle") + t(120, 156, "per month · cancel anytime", 8, MUTE, anchor="middle") + t(120, 176, "$2,780 a year in total", 7.5, MUTE, anchor="middle") + btn(230, "Continue"))),
 "How Should The Payment Plan Be Picked?")
add(GP, "Up Keep: Payment Plan",
 O("pay_reserve", "Reserve Now, Pay After First Visit", "Leads with 'Reserve My Spot, $0 Today'. Card details come after Danny's first visit.", ["low-risk", "trust", "warm"], "neighbor",
   screen(h1(14, 56, "Reserve Your Spot", 17) + t(14, 92, "$0 Today", 26, JUNGLE, "khand") + para(14, 108, ["Pay after Danny's first visit, once you've", "seen the report. Then $232 a month."]) + "".join(t(14, 146 + i * 13, "✓ " + l, 8, INK) for i, l in enumerate(["No card needed now", "Cancel before the visit, no charge", "Final price set on site"])) + btn(200, "Reserve My Spot", col=TERRA))),
 O("pay_now", "Pay Now With Card", "Standard checkout: card fields and 'Start Membership'. Secure badge below.", ["standard", "direct", "committed"], "crew",
   screen(h1(14, 56, "Payment", 17) + t(14, 72, "Gold · $232 a month · first charge today", 7.5, MUTE) + field(84, "Card number", "4242 4242 4242 4242") + field(114, "Expiry", "08 / 29", w=100) + field(114, "CVC", "123", x=126, w=100) + btn(158, "Start Membership") + shield(80, 196, LAGOON, .5) + t(96, 205, "Secure checkout by Stripe", 7, MUTE))),
 "Pay Now Or Pay After The First Visit?")

# ===================== 9. Empty states (2) =====================
add(GE, "Up Keep: Empty States",
 O("empty_draw", "Empty Report: Small Drawing", "No reports yet: a simple line house with a terracotta door and 'Your first report lands Nov 4'.", ["friendly", "warm", "drawn"], "neighbor",
   screen(h1(14, 54, "Visit Reports", 17) + f'<g transform="translate(60,60) scale(.5)"><path d="M50 120 L120 62 L190 120" fill="none" stroke="{INK}" stroke-width="3"/><path d="M64 112 V170 H176 V112" fill="none" stroke="{INK}" stroke-width="3"/><rect x="108" y="132" width="24" height="38" fill="{TERRA}"/></g>' + h1(120, 172, "No Reports Yet", 16, anchor="middle") + t(120, 188, "Your first report lands after Nov 4.", 8, MUTE, anchor="middle") + btn(210, "See A Sample Report", "outline") + tabbar(2))),
 O("empty_check", "Empty Report: What Happens Next", "No drawing: a 3-item checklist of what happens before the first report.", ["system", "useful", "clear"], "system",
   screen(h1(14, 54, "Visit Reports", 17) + rect(14, 66, 212, 120, CREAM, LINE, 6) + t(24, 88, "Your First Report Is On Its Way", 11, INK, "khand") + "".join(icon("check", 24, 98 + i * 26, 16, "duo", c) + t(46, 110 + i * 26, n, 8, INK if c != "#BDB6AA" else MUTE) for i, (n, c) in enumerate([("Membership started", JUNGLE), ("Visit booked · Nov 4", JUNGLE), ("Danny visits, report follows", "#BDB6AA")])) + link(14, 206, "See A Sample Report", LAGOON) + tabbar(2))),
 "How Should An Empty Page Look?")
add(GE, "Up Keep: Empty States",
 O("empty_cal_cta", "Empty Calendar: One Big Button", "No visits booked yet: a short line and one 'Book Your First Visit' button.", ["direct", "focused", "simple"], "crew",
   screen(h1(14, 54, "Calendar", 17) + icon("check", 100, 88, 40, "outline") + h1(120, 160, "Nothing Booked Yet", 16, anchor="middle") + t(120, 176, "Pick a time and we'll handle the rest.", 8, MUTE, anchor="middle") + btn(196, "Book Your First Visit", col=TERRA) + tabbar(1))),
 O("empty_cal_ghost", "Empty Calendar: Ghost Schedule", "Shows the four seasons faded, with 'Book' on the first one.", ["preview", "planned", "system"], "system",
   screen(h1(14, 54, "Calendar", 17) + "".join(rect(14, 66 + i * 46, 212, 40, "#FFFFFF", LINE, 4, 1, 'stroke-dasharray="3 2"' if i else "") + t(24, 90 + i * 46, s, 10, INK if i == 0 else "#A3A3A3", "khand") + (btn(76 + i * 46, "Book", col=TERRA, x=160, w=58, h=20, size=7) if i == 0 else t(216, 90 + i * 46, "Not yet", 7, "#A3A3A3", anchor="end")) for i, s in enumerate(["Fall Visit", "Winter Visit", "Spring Visit", "Summer Visit"])) + tabbar(1))),
 "How Should An Empty Calendar Look?")

# ===================== 10. Push / SMS wording + referral (4) =====================
add(GM, "Up Keep: Reminder Text",
 O("sms_short", "Short Text Reminder", "'Up Keep: Danny visits tomorrow 9-11 AM. Reply C to confirm, R to reschedule.'", ["short", "efficient", "system"], "system",
   sms([["Up Keep: Danny visits tomorrow,", "Tue 9-11 AM. Reply C to confirm", "or R to reschedule."]])),
 O("sms_friendly", "Friendly Text Reminder", "'Hi Sarah, it's Max at Up Keep. Danny's coming tomorrow between 9 and 11…'", ["warm", "personal", "neighborly"], "neighbor",
   sms([["Hi Sarah, it's Max at Up Keep.", "Danny's coming tomorrow between", "9 and 11 AM for your fall visit."], ["Need a different time? Just reply", "and we'll sort it out."]])),
 "Which Reminder Text?")
add(GM, "Up Keep: Push Reminder",
 O("push_task", "Push: The Task", "'Time To Swap Your Furnace Filter' + size and where it is.", ["useful", "direct", "clear"], "crew",
   phone_frame(notif(84, "Time To Swap Your Furnace Filter", ["16x25x1 · it's in your garage, top shelf.", "Takes 2 minutes."], accent=SAFFRON))),
 O("push_why", "Push: The Reason", "'A Clean Filter Cuts Your Heating Bill' + one tap to mark it done.", ["benefit", "friendly", "lively"], "neighbor",
   phone_frame(notif(84, "A Clean Filter Cuts Your Heating Bill", ["Your 90-day swap is due. Tap when done", "and we'll log it in your Home Record."], accent=JUNGLE))),
 "Which Push Reminder Wording?")
add(GM, "Up Keep: Referral",
 O("ref_card", "Referral As A Big Card", "'Give A Month, Get A Month' with a code and one Share button.", ["bold", "simple", "warm"], "neighbor",
   screen(rect(14, 44, 212, 140, CREAM, LINE, 8) + gift(104, 56, TERRA, 1.4) + h1(120, 112, "Give A Month, Get A Month", 15, anchor="middle") + t(120, 126, "When a neighbor joins, you both get", 7.5, MUTE, anchor="middle") + t(120, 136, "one month free.", 7.5, MUTE, anchor="middle") + rect(54, 146, 132, 24, "#FFFFFF", INK, 0, 1.3, 'stroke-dasharray="3 2"') + t(120, 162, "SARAH-NOVI", 10, INK, "khand", anchor="middle") + btn(198, "Share My Link") + tabbar(3))),
 O("ref_contacts", "Referral With Neighbor Tracker", "A share row plus a list of who you've invited and who joined.", ["system", "tracking", "lively"], "system",
   screen(h1(14, 54, "Invite Neighbors", 17) + t(14, 68, "You both get a month free.", 7.5, MUTE) + btn(78, "Text", "outline", w=66, size=8) + btn(78, "Email", "outline", x=87, w=66, size=8) + btn(78, "Copy Link", "outline", x=160, w=66, size=8)
          + lbl(14, 126, "Your invites") + "".join(ln(132 + i * 26) + t(14, 148 + i * 26, n, 8.5, INK) + tag(170, 139 + i * 26, s, c) for i, (n, s, c) in enumerate([("Mike R.", "Joined", JUNGLE), ("The Patels", "Invited", LAGOON), ("Jen K.", "Invited", LAGOON)])) + t(14, 228, "1 free month earned", 8, JUNGLE, "hind", 600) + tabbar(3))),
 "How Should The Referral Screen Look?")
add(GM, "Up Keep: Referral",
 O("ref_month", "Reward: A Free Month", "'You both get a month free.'", ["simple", "generous", "clear"], "neighbor",
   screen(gift(96, 60, TERRA, 2) + h1(120, 142, "You Both Get A Month Free", 16, anchor="middle") + t(120, 158, "When a neighbor joins Up Keep", 8, MUTE, anchor="middle") + btn(190, "Invite A Neighbor"))),
 O("ref_dollars", "Reward: Dollar Credit", "'$100 off for you, $100 off for them.'", ["concrete", "money", "direct"], "crew",
   screen(t(120, 112, "$100 + $100", 34, INK, "khand", anchor="middle") + h1(120, 142, "For You And Your Neighbor", 16, anchor="middle") + t(120, 158, "Credit when they join Up Keep", 8, MUTE, anchor="middle") + btn(190, "Invite A Neighbor"))),
 "Which Referral Reward?")

# ===================== 11. Multi-accent color combos (8) =====================
def combo(btnc, info, ok, base="#FFFFFF", warnc=None, iconc=None):
    """Member dashboard with each role colored: button, info (links/ring/next-visit stripe), ok tags, optional due tag."""
    warnc = warnc or ok
    s = lbl(14, 48, "Hi Sarah") + h1(14, 66, "Your Home Is In Good Shape", 15) + rect(14, 76, 212, 70, "#FFFFFF" if base != "#FFFFFF" else CREAM, LINE, 6) + rect(14, 76, 4, 70, info)
    s += ring(52, 111, 20, .88, info, "88") + t(84, 100, "Next visit", 7, MUTE) + t(84, 116, "Tue, Nov 4 · 9 AM", 12, INK, "khand") + link(84, 134, "Reschedule", info)
    for i, (n, st, c) in enumerate([("Furnace", "Done", ok), ("Water heater", "Due Nov", warnc), ("Gutters", "Done", ok), ("Smoke detectors", "Done", ok)]):
        y = 156 + i * 22; s += ln(y) + (icon("check", 14, y + 4, 13, "duo", iconc) if iconc else "") + t(14 + (18 if iconc else 0), y + 15, n, 8.5, INK) + tag(176, y + 6, st, c)
    return screen(s + btn(250, "Book A Visit", col=btnc), base, up=btnc)
CC = "Up Keep: Multi-Accent Color"
add(GK, CC, O("cc_tl_j", "Terracotta Button + Lagoon Info + Jungle Done", "Three jobs, three hues: act, inform, all good.", ["lively", "coded", "multi-accent", "warm"], "system", combo(TERRA, LAGOON, JUNGLE)),
            O("cc_tl", "Terracotta Button + Lagoon For Everything Else", "Two hues only. Lagoon covers info and done.", ["balanced", "calm", "multi-accent"], "concierge", combo(TERRA, LAGOON, LAGOON)), "Three Hues Or Two?")
add(GK, CC, O("cc_lag_btn", "Lagoon Button, Terracotta Links", "Swap roles: cool blue main button, warm terracotta links and ring.", ["cool", "trust", "multi-accent"], "system", combo(LAGOON, TERRA, JUNGLE, base=CREAM)),
            O("cc_terra_btn", "Terracotta Button, Lagoon Links", "Warm main button, cool links and ring.", ["warm", "inviting", "multi-accent"], "neighbor", combo(TERRA, LAGOON, JUNGLE, base=CREAM)), "Which Hue On The Main Button?")
add(GK, CC, O("cc_saffron_due", "Saffron For 'Due Soon'", "Done tags jungle green, due-soon tags saffron. A traffic-light feel without red.", ["coded", "clear", "multi-accent"], "system", combo(INK, LAGOON, JUNGLE, warnc=SAFFRON)),
            O("cc_terra_due", "Terracotta For 'Due Soon'", "Due-soon tags in terracotta instead: warmer, a bit more urgent.", ["warm", "urgent", "multi-accent"], "crew", combo(INK, LAGOON, JUNGLE, warnc=TERRA)), "What Color Means 'Due Soon'?")
add(GK, CC, O("cc_black_btn", "Black Button, Color Only In Status", "Main button stays black; the hues live only in ring, links and tags.", ["restrained", "brand", "multi-accent"], "concierge", combo(INK, LAGOON, JUNGLE, warnc=SAFFRON)),
            O("cc_color_btn", "Colored Button Plus Status Colors", "Terracotta main button on top of the same status colors.", ["lively", "bold", "multi-accent"], "neighbor", combo(TERRA, LAGOON, JUNGLE, warnc=SAFFRON)), "Black Main Button Or Colored?")
add(GK, CC, O("cc_berry_trio", "Berry + Lagoon + Jungle", "Deep berry button with lagoon info and jungle done.", ["rich", "distinctive", "multi-accent"], "concierge", combo(BERRY, LAGOON, JUNGLE)),
            O("cc_persim_trio", "Persimmon + Lagoon + Jungle", "Brighter persimmon button with the same lagoon and jungle.", ["energetic", "bright", "multi-accent"], "neighbor", combo(PERSIM, LAGOON, JUNGLE)), "Which Warm Main Button In A Trio?")
add(GK, CC, O("cc_cream_trio", "Trio On Cream", "Terracotta, lagoon, jungle on warm cream #FAF6EE.", ["warm", "soft", "multi-accent", "cream-base"], "neighbor", combo(TERRA, LAGOON, JUNGLE, base=CREAM, warnc=SAFFRON)),
            O("cc_white_trio", "Trio On White", "The same three hues on pure white.", ["crisp", "clear", "multi-accent", "white-base"], "system", combo(TERRA, LAGOON, JUNGLE, warnc=SAFFRON)), "Cream Or White Under Three Pops?")
add(GK, CC, O("cc_icons_on", "Colored Check Icons In Lists", "Small duotone check icons in jungle beside every system row.", ["lively", "visual", "multi-accent"], "neighbor", combo(TERRA, LAGOON, JUNGLE, warnc=SAFFRON, iconc=JUNGLE)),
            O("cc_icons_off", "Color Only In The Tags", "Rows stay plain text; color sits only in the tags on the right.", ["clean", "calm", "multi-accent"], "system", combo(TERRA, LAGOON, JUNGLE, warnc=SAFFRON)), "Add Colored Icons To Lists?")
add(GK, CC, O("cc_deep_lag", "Deep Lagoon Info (#05668D)", "Black button; deep lagoon on the ring, links and Done tags, saffron for due.", ["serious", "trust", "multi-accent"], "system", combo(INK, LAGOON, LAGOON, warnc=SAFFRON)),
            O("cc_teal_info", "Bright Lagoon Info (#00A6A6)", "The same screen with the brighter teal lagoon.", ["fresh", "lively", "multi-accent"], "neighbor", combo(INK, LAG2, LAG2, warnc=SAFFRON)), "Which Lagoon For Info?")

# ===================== 12. Voice & microcopy (4) =====================
def micro(head, lines, cta, sub=None):
    return screen(icon("check", 96, 52, 48, "duo", JUNGLE) + h1(120, 128, head, 18, anchor="middle") + "".join(t(120, 146 + i * 12, l, 8, MUTE, anchor="middle") for i, l in enumerate(lines)) + btn(196, cta) + (link(120, 244, sub, LAGOON, "middle") if sub else ""))
VO = "Up Keep: Microcopy"
add(GV, VO, O("mc_booked_plain", "Booked: 'Visit Booked.'", "Plain confirmation with the facts.", ["plain", "factual", "short"], "system", micro("Visit Booked.", ["Tue, Nov 4 · 9 to 11 AM · Danny"], "Done")),
            O("mc_booked_warm", "Booked: 'You're All Set, Sarah.'", "Warm, names the person and the tech.", ["warm", "personal", "friendly"], "neighbor", micro("You're All Set, Sarah.", ["Danny will see you Tuesday", "between 9 and 11 AM."], "Sounds Good")), "Which Booking Confirmation?")
add(GV, VO, O("mc_err_plain", "Error: 'That ZIP Doesn't Look Right.'", "Short, says what to fix.", ["direct", "clear", "short"], "crew",
                 screen(h1(14, 82, "What's Your ZIP Code?", 18) + rect(14, 96, 212, 26, "#FFFFFF", TERRA, 0, 1.6) + t(22, 113, "4832", 10, INK) + t(14, 136, "That ZIP doesn't look right. Use 5 digits.", 7.5, TERRA, "hind", 600) + btn(160, "Next"))),
            O("mc_err_kind", "Error: 'Hmm, We Need 5 Digits.'", "Softer, a little human.", ["friendly", "gentle", "human"], "neighbor",
                 screen(h1(14, 82, "What's Your ZIP Code?", 18) + rect(14, 96, 212, 26, "#FFFFFF", SAFFRON, 0, 1.6) + t(22, 113, "4832", 10, INK) + t(14, 136, "Hmm, we need all 5 digits. Or tap Unsure.", 7.5, INK) + btn(160, "Next"))), "Which Error Wording?")
add(GV, VO, O("mc_done_title", "Report Push: 'Your Fall Report Is Ready'", "States the thing.", ["clear", "system", "factual"], "system", phone_frame(notif(84, "Your Fall Report Is Ready", ["11 checks done · 1 to watch: dryer vent."], accent=LAGOON))),
            O("mc_done_story", "Report Push: 'Danny Finished Up. All Good.'", "Tells it like a neighbor would.", ["human", "warm", "short"], "neighbor", phone_frame(notif(84, "Danny Finished Up. All Good.", ["One small thing: the dryer vent. Details", "and photos are in your report."], accent=JUNGLE))), "Which Report-Ready Wording?")
add(GV, VO, O("mc_cancel_soft", "Cancel Screen: 'Sorry To See You Go.'", "Soft goodbye with a pause option.", ["kind", "warm", "retention"], "neighbor",
                 screen(h1(14, 70, "Sorry To See You Go", 18) + para(14, 86, ["Before you cancel: you can pause for up", "to 3 months instead. No charge."]) + btn(116, "Pause Instead", col=LAGOON) + btn(150, "Cancel Membership", "outline"))),
            O("mc_cancel_plain", "Cancel Screen: 'Cancel Membership'", "Plain and quick. Shows the refund, one button.", ["honest", "fast", "respectful"], "crew",
                 screen(h1(14, 70, "Cancel Membership", 18) + para(14, 86, ["Unused visits are refunded: $464.", "Your Home Record stays yours."]) + btn(116, "Cancel Membership") + link(120, 166, "Keep My Membership", INK, "middle"))), "Which Cancel Screen Voice?")

# ===================== 13. Swipe Controls (2) =====================
C = lambda i, l, desc, tags, **k: {"id": "uk2_" + i, "label": l, "desc": desc, "tags": tags, "feeling": None, "visual": {"type": "controls", "words": ["This", "Both", "Love", "That"], "icons": ["◀", "⇄", "❤", "▶"], "colors": [LAGOON, JUNGLE, "#E0245E", TERRA], "bg": "#FFFFFF", "font": "Hind", "stampov": "word", "press": None, **k}}
add(GS, "Swipe Controls", C("sc_trio_square", "Square Outline, Three Pops", "Square outline buttons: lagoon This, jungle Both, red Love, terracotta That.", ["multi-accent", "clear"], fmt="square", style="outline", press="fill", hint="edges"),
    C("sc_trio_fill", "Square Filled, Three Pops", "The same colors as solid filled squares with white text.", ["bold", "lively"], fmt="square", style="fill", font="Khand", hint="edges"), "Which Swipe Controls?")
add(GS, "Swipe Controls", C("sc_cream_pill", "Cream Pills With Colored Icons", "Cream pills, black words, a small colored icon in each.", ["warm", "micro-dose"], fmt="pill", style="outline", bg="#FAF6EE", hint="edges"),
    C("sc_white_round", "White Round With Colored Ring", "Round white buttons with a colored ring that fills on press.", ["clean", "playful"], fmt="round", style="outline", press="fill", hint="edges"), "Which Swipe Controls?")

# ---- order: open with a dashboard choice; no category twice in a row ----
random.seed(22); first = pairs[:1]; rest = pairs[1:]; random.shuffle(rest); seq = first + rest; order = []
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
        "title": "Up Keep Round 2: Member App, Booking, Alerts And Color Pops", "brands": ["Up Keep / Smart Upkeep: home maintenance membership app (https://webermanapps.github.io/smart-upkeep/)", "Base: white or cream, #0A0A0A ink, square black buttons, Khand/Hind; 2-3 small pops (terracotta = act, lagoon = info, jungle = done, saffron = due soon); no neon, no pastel, not all-beige"],
        "generated_at": now, "builds_on": "upkeep-1 answers (31 of 50): top tags clear, system, warm, lively, multi-accent",
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
