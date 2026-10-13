#!/usr/bin/env python3
"""Build Style Swipe daily deck "Flat Fee & Lagoon Deck" (slug flat-fee-and-lagoon): 25 pairs built from Max's
daily 2026-10-13 picks (32/50, results/2026-10-13.txt). Copied from build_daily_2026_10_13.py (same helpers + asserts).
Groups: Up Keep features (14), Blog Topics follow-ups (10), Blog Style (4), Color Accents (6), Swipe Controls (3),
Home Guide (4), Variety (9). Refines winners, retests 'both' ties head to head, re-asks key skips in a fresher way.
Rules: maxweberman.com brand (Khand/Hind, light only), micro-dose color, no emoji (drawn SVG icons only), example data only,
Notes + Share on every pair. Smart Upkeep: no byline, no health score / forecast, 'Your Licensed Tech' (no named tech),
only price line 'Membership Starting at $99/Month'. All option ids prefixed ffl_. Run from style-swipe repo root."""
import json, random, datetime as dt, glob, os

DID = "flat-fee-and-lagoon"
NAME = "Flat Fee & Lagoon Deck"
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
    o = {"id": "ffl_" + i, "label": label, "desc": desc, "tags": tags, "visual": visual}
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

# ---------- shared drawing helpers (new for this deck) ----------
PRICE = "Membership Starting at $99/Month"
LT = "Your Licensed Tech"
HOLDTXT = "#8A6400"   # readable saffron-family text on white
def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        tr = (cur + " " + w).strip()
        if len(tr) > n and cur: out.append(cur); cur = w
        else: cur = tr
    if cur: out.append(cur)
    return out
def svgwrap(body, bg="#FFFFFF"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%">'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</g>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
ICONS = {
    "heart": '<path d="M12 20C5 14.5 3 11.5 3 8.5A4.5 4.5 0 0 1 12 6.5A4.5 4.5 0 0 1 21 8.5C21 11.5 19 14.5 12 20Z"/>',
    "check": '<polyline points="5,12.5 10,17 19,7"/>',
    "pass": '<polyline points="14,5 7,12 14,19"/>',
    "hold": '<line x1="9" y1="6" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="18"/>',
    "phone": '<path d="M6 3h4l2 5-3 2a11 11 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><polyline points="14,3 14,7 18,7"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="15" y2="16"/>',
    "drop": '<path d="M12 3C8 9 6 12 6 15a6 6 0 0 0 12 0c0-3-2-6-6-12z"/>',
    "gauge": '<circle cx="12" cy="13" r="8"/><line x1="12" y1="13" x2="16" y2="9"/>',
    "bolt": '<polyline points="13,3 6,14 12,14 11,21 18,10 12,10 13,3"/>',
    "wrench": '<path d="M15 4a5 5 0 0 0-5 6.5L4 16.5 7.5 20l6-6A5 5 0 0 0 20 9l-3 3-3-1-1-3z"/>',
    "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "mail": '<rect x="3" y="6" width="18" height="12" rx="2"/><polyline points="3,7 12,13 21,7"/>',
    "cal": '<rect x="4" y="5" width="16" height="15" rx="2"/><line x1="4" y1="10" x2="20" y2="10"/><line x1="9" y1="3" x2="9" y2="7"/><line x1="15" y1="3" x2="15" y2="7"/>',
    "bell": '<path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4z"/><line x1="10" y1="21" x2="14" y2="21"/>',
    "camera": '<rect x="3" y="7" width="18" height="13" rx="2"/><circle cx="12" cy="13.5" r="3.5"/><path d="M8 7l2-3h4l2 3"/>',
    "pin": '<path d="M12 21s-7-6.5-7-11a7 7 0 0 1 14 0c0 4.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
    "chat": '<path d="M4 5h16v10h-9l-5 4v-4H4z"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M6 10v10h12V10"/>',
    "leaf": '<path d="M5 19C5 10 11 5 20 5c0 9-5 15-14 14z"/><line x1="5" y1="19" x2="13" y2="11"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>',
    "snow": '<line x1="12" y1="3" x2="12" y2="21"/><line x1="4" y1="7.5" x2="20" y2="16.5"/><line x1="4" y1="16.5" x2="20" y2="7.5"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "list": '<line x1="8" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="8" y1="18" x2="20" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
}
def I(kind, x, y, c=INK, s=14, sw=2):
    return (f'<g transform="translate({x},{y}) scale({s/24:.4f})" fill="none" stroke="{c}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>')
def circ(cx, cy, r, fill, stroke="none", sw=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def rbtn(y, s, col=INK, style="fill", x=14, w=212, h=28, size=9):
    """Capsule-pill button (Max picked Full Capsule Pills, 2026-10-13)."""
    bg, fg = (col, "#FFFFFF") if style == "fill" else ("#FFFFFF", col)
    return rect(x, y, w, h, bg, col, h / 2, 1.5) + t(x + w / 2, y + h / 2 + size * .36, s.upper(), size, fg, "hind", 600, "middle", 'letter-spacing="1.1"')

# ========== A. Swipe Controls (3): Pass / Hold / Love / Keep in capsule pills ==========
CTL = [("Pass", TERRA, TERRA, "pass"), ("Hold", SAFFRON, HOLDTXT, "hold"), ("Love", BERRY, BERRY, "heart"), ("Keep", LAGOON, LAGOON, "check")]
def ctl_screen(style="outline", icons=False, stamp=None, caption=""):
    body = rect(0, 0, W, H, "#FAF8F4")
    body += rect(26, 18, 188, 196, "#FFFFFF", LINE, 12) + rect(34, 26, 172, 118, "#E9E2D6", "none", 8)
    body += f'<polyline points="86,104 120,78 154,104" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>' + rect(96, 102, 48, 30, "#FFFFFF", INK, 0, 2)
    body += t(40, 166, "Example Card", 13, INK, "khand") + t(40, 182, "Swipe, or tap a button below.", 8, MUTE)
    if stamp == "word":
        body += f'<g transform="rotate(-12 82 56)">' + rect(46, 42, 74, 28, "#FFFFFFE8", LAGOON, 5, 2.5) + t(83, 62, "KEEP", 16, LAGOON, "khand", anchor="middle") + "</g>"
    elif stamp == "badge":
        body += circ(190, 44, 15, LAGOON) + I("check", 180, 34, "#FFFFFF", 20, 2.6)
    w, gap, y, h = 49, 5.33, 230, 30
    for i, (lab, c, tc, ic) in enumerate(CTL):
        x = 14 + i * (w + gap)
        if style == "outline": bg, st, fg = "#FFFFFF", c, tc
        else: bg, st, fg = c + "26", "none", tc
        body += rect(x, y, w, h, bg, st, h / 2, 1.6)
        if icons:
            body += I(ic, x + 6, y + 9, fg, 12, 2.4) + t(x + 30, y + 18.5, lab.upper(), 7, fg, "hind", 700, "middle", 'letter-spacing=".4"')
        else:
            body += t(x + w / 2, y + 18.5, lab.upper(), 7.6, fg, "hind", 700, "middle", 'letter-spacing=".6"')
    body += t(120, 282, caption, 7.5, MUTE, anchor="middle")
    return svgwrap(body, "#FAF8F4")

add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "Capsule Pills: Outline Or Soft Tint?",
    O("sc_cap_outline", "Outline Capsules", "White pills with a colored ring and word.", ["clear", "light", "calm", "crisp"],
      Vsvg(ctl_screen("outline", caption="Outline capsules")), ),
    O("sc_cap_tint", "Soft Tint Capsules", "Pills filled with a light wash of each color.", ["soft", "friendly", "lively", "warm"],
      Vsvg(ctl_screen("tint", caption="Soft tint capsules"))))
add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "Words Only Or Words With Small Drawn Icons?",
    O("sc_words_icons", "Words With Drawn Icons", "Back arrow, pause bars, heart, check next to each word.", ["guided", "visual", "clear", "friendly"],
      Vsvg(ctl_screen("outline", icons=True, caption="Pass / Hold / Love / Keep with icons"))),
    O("sc_words_only", "Words Only", "Just Pass / Hold / Love / Keep, nothing else.", ["simple", "minimal", "direct", "clear"],
      Vsvg(ctl_screen("outline", icons=False, caption="Pass / Hold / Love / Keep, words only"))), purpose="check")
add("Swipe Controls", "Swipe Controls", "All Swipe Apps", "When You Choose, What Shows On The Card?",
    O("sc_mark_word", "Tilted Word Stamp", "A tilted KEEP or PASS stamp lands on the card.", ["tactile", "lively", "clear", "warm"],
      Vsvg(ctl_screen("outline", stamp="word", caption="Word stamp on the card"))),
    O("sc_mark_badge", "Small Corner Badge", "A round check badge pops in the corner.", ["calm", "modern", "minimal", "clear"],
      Vsvg(ctl_screen("outline", stamp="badge", caption="Corner badge on the card"))), purpose="check")

# ========== B. Color Accents (6): building on lagoon + saffron on white ==========
def capp(cta=LAGOON, due=SAFFRON, due_style="tag", tag_col=INK, tag_solid=True, done=None, link=None,
         header=None, icon_col=None, title="Home"):
    body = lbl(14, 48, "Customer App") + h1(14, 66, title, 16)
    if header: body += rect(14, 72, 36, 3, header, "none", 1.5)
    body += rect(14, 82, 212, 56, "#FFFFFF", LINE, 8)
    x0 = 22
    if icon_col: body += I("cal", 22, 98, icon_col, 18, 1.8); x0 = 48
    body += t(x0, 100, "NEXT VISIT", 6.5, MUTE, "hind", 600, extra='letter-spacing=".8"') + t(x0, 120, "Tue, Nov 4 · 9 AM", 13, INK, "khand")
    if due_style == "tag": body += tag(160, 92, "Due Soon", due, True)
    elif due_style == "underline": body += t(162, 100, "Due Soon", 8, INK, "hind", 600) + rect(162, 103, 38, 2.5, due, "none", 1)
    elif due_style == "dot": body += circ(165, 97, 3.5, due) + t(172, 100, "Due Soon", 8, INK, "hind", 600)
    rows = [("Furnace Filter", "Done", "gauge"), ("Gutters", "Due", "home"), ("Water Heater", "Info", "drop")]
    for i, (nm, st, ic) in enumerate(rows):
        y = 150 + i * 26
        body += ln(y)
        tx = 14
        if icon_col: body += I(ic, 14, y + 6, icon_col, 14, 1.8); tx = 34
        body += t(tx, y + 17, nm, 9.5, INK)
        if done and st == "Done":
            body += I("check", 186, y + 5, done, 14, 2.4) + t(226, y + 16, "Done", 8, done, "hind", 600, "end")
        else:
            body += tag(226 - (len(st) * 4.4 + 10), y + 8, st, tag_col, tag_solid)
    if link: body += t(14, 244, "See full home record", 9, link, "hind", 600, extra='text-decoration="underline"')
    body += rbtn(256, "Book Visit", cta)
    return screen(body, head=False)

COL = [
    ("Which Lagoon For The Main Button?",
     ("col_deep_lagoon", "Deep Lagoon Button, Saffron Due", "Darker lagoon blue button; saffron due tag.", ["clear", "calm", "trust", "modern"], capp(LAGOON, SAFFRON)),
     ("col_bright_teal", "Bright Teal Button, Saffron Due", "Lighter teal button; saffron due tag.", ["fresh", "lively", "clear", "light"], capp(LAG2, SAFFRON)), "refine"),
    ("Status Tags And Button: Which Gets The Color?",
     ("col_blacktags_lagbtn", "Black Tags, Lagoon Button", "Crisp black status chips; color only on the button.", ["crisp", "system", "clear", "focused"], capp(LAGOON, SAFFRON, tag_col=INK)),
     ("col_lagtags_blackbtn", "Lagoon Tags, Black Button", "Lagoon status chips; black main button.", ["clear", "modern", "lively", "calm"], capp(INK, SAFFRON, tag_col=LAGOON)), "refine"),
    ("Add A Third Pop For 'Done'?",
     ("col_three_jungle", "Lagoon + Saffron + Jungle Check", "Jungle green check for finished items.", ["lively", "multi", "clear", "guided"], capp(LAGOON, SAFFRON, done=JUNGLE)),
     ("col_two_only", "Lagoon + Saffron Only", "No third color; done items use black tags.", ["simple", "focused", "calm", "clear"], capp(LAGOON, SAFFRON)), "check"),
    ("How Should Saffron Mark 'Due Soon'?",
     ("col_saff_underline", "Saffron Underline", "Black words with a thin saffron underline.", ["subtle", "crisp", "clear", "light"], capp(LAGOON, SAFFRON, "underline")),
     ("col_saff_dot", "Saffron Dot", "A small saffron dot before black words.", ["calm", "minimal", "clear", "modern"], capp(LAGOON, SAFFRON, "dot")), "refine"),
    ("Terracotta Button Or Lagoon Button?",
     ("col_terra_btn_laglink", "Terracotta Button, Lagoon Link", "Warm main button; lagoon text link.", ["warm", "brand", "lively", "multi"], capp(TERRA, SAFFRON, link=LAGOON)),
     ("col_lag_btn_terralink", "Lagoon Button, Terracotta Link", "Lagoon main button; terracotta text link.", ["clear", "fresh", "multi", "calm"], capp(LAGOON, SAFFRON, link=TERRA)), "check"),
    ("Where Else Can Lagoon Show Up?",
     ("col_lag_header", "Short Lagoon Line Under Titles", "One small lagoon bar under each page title.", ["clean", "editorial", "calm", "clear"], capp(LAGOON, SAFFRON, header=LAGOON)),
     ("col_lag_icons", "Lagoon Line Icons", "Thin lagoon icons next to each row.", ["guided", "visual", "friendly", "clear"], capp(LAGOON, SAFFRON, icon_col=LAGOON)), "refine"),
]
for ask, a, b, purpose in COL:
    add("Color Accents", "Color Accents", "Customer Apps", ask,
        O(a[0], a[1], a[2], a[3], Vsvg(a[4])), O(b[0], b[1], b[2], b[3], Vsvg(b[4])), purpose=purpose)

# ========== C. Up Keep features (14) ==========
def uk(body): return screen(body)
def uk_title(l, h, size=15): return lbl(14, 48, l) + h1(14, 66, h, size)
def checks(y, items, c=JUNGLE, gap=20, size=9):
    return "".join(I("check", 14, y + i * gap - 10, c, 13, 2.4) + t(32, y + i * gap, s, size, INK) for i, s in enumerate(items))

def uk_tiers2(names, lines):
    b = uk_title("Plans", "Pick Your Plan")
    for i, (n, l) in enumerate(zip(names, lines)):
        y = 80 + i * 50; sel = i == 1
        b += rect(14, y, 212, 44, SEL if sel else "#FFFFFF", INK if sel else LINE, 10, 1.5 if sel else 1)
        b += t(26, y + 19, n, 13, INK, "khand") + t(26, y + 33, l, 7.8, MUTE)
        b += circ(208, y + 22, 6, LAGOON if sel else "#FFFFFF", LAGOON if sel else "#BDB6AA", 1.5)
    b += t(120, 244, PRICE, 10, INK, "khand", anchor="middle") + rbtn(256, "Get My Quote", LAGOON)
    return uk(b)
def uk_pricev(kind):
    b = uk_title("Membership", "What You Get")
    b += checks(98, ["Seasonal visits from " + LT, "Home record for every appliance", "Reminders before each visit", "Cancel anytime"])
    if kind == "line":
        b += rect(14, 182, 212, 44, LAGOON + "12", "none", 10) + t(120, 209, PRICE, 11.5, LAGOON, "khand", anchor="middle")
        b += rbtn(256, "Start My Membership", LAGOON)
    else:
        b += rect(14, 182, 212, 44, "#FFFFFF", LINE, 10) + t(120, 201, "Your price comes after a", 8.5, MUTE, anchor="middle") + t(120, 215, "2-minute home quote.", 8.5, MUTE, anchor="middle")
        b += rbtn(256, "Get My Quote", LAGOON)
    return uk(b)
def uk_human2(kind):
    b = uk_title("Text A Human", "Ask About Your Home", 14)
    b += rect(70, 82, 156, 34, "#F2F0EC", "none", 12) + t(80, 103, "Is my sump pump OK?", 9, INK)
    if kind == "tech":
        b += circ(26, 140, 10, LAGOON + "1F") + I("user", 18, 132, LAGOON, 16, 1.8) + t(42, 137, LT.upper(), 6.5, LAGOON, "hind", 600, extra='letter-spacing=".6"')
    else:
        b += circ(26, 140, 10, TERRA + "1F") + I("chat", 18, 132, TERRA, 16, 1.8) + t(42, 137, "MEMBER CARE DESK", 6.5, TERRA, "hind", 600, extra='letter-spacing=".6"')
    b += rect(14, 152, 170, 46, "#FFFFFF", LINE, 12) + para(24, 170, ["I'll check it on your", "Tue, Nov 4 visit."], 9, INK)
    b += t(14, 220, "Replies within 1 business day (example)", 7.5, MUTE)
    b += rbtn(256, "Send A Message", LAGOON)
    return uk(b)
def uk_accent2(cta, tg, name):
    b = uk_title("Home", "Welcome Home", 16)
    b += rect(14, 80, 212, 56, "#FFFFFF", LINE, 10) + t(22, 98, "NEXT VISIT", 6.5, MUTE, "hind", 600) + t(22, 120, "Tue, Nov 4 · 9 AM", 13, INK, "khand")
    b += tag(162, 92, "Due Soon", tg, True)
    for i, (n, ic) in enumerate([("Home Record", "list"), ("Text A Human", "chat"), ("Visits", "cal")]):
        y = 148 + i * 30; b += ln(y) + I(ic, 14, y + 8, cta, 15, 1.8) + t(36, y + 20, n, 9.5, INK)
    b += rbtn(256, "Book A Visit", cta)
    b += t(226, 76, name, 6.5, MUTE, anchor="end")
    return uk(b)
def uk_pay(kind):
    b = uk_title("Billing", "How You Pay", 15)
    if kind == "app":
        b += rect(14, 84, 212, 70, "#FFFFFF", LAGOON, 10, 1.5) + I("card", 24, 98, LAGOON, 22, 1.8)
        b += t(56, 108, "Card On File", 12, INK, "khand") + t(56, 124, "Ending 0000 (example)", 8, MUTE) + t(56, 140, "Charged monthly in the app", 8, MUTE)
        b += checks(182, ["Change card anytime in Settings", "Receipts saved in the app"], LAGOON)
        b += rbtn(256, "Pay In The App", LAGOON)
    else:
        b += rect(14, 84, 212, 70, "#FFFFFF", LINE, 10) + I("mail", 24, 98, INK, 22, 1.8)
        b += t(56, 108, "Pay By Email Link", 12, INK, "khand") + t(56, 124, "Secure link each month", 8, MUTE) + t(56, 140, "No card stored in the app", 8, MUTE)
        b += checks(182, ["Pay from any device", "Receipt sent by email"], JUNGLE)
        b += rbtn(256, "Email Me The Link", INK, "outline")
    return uk(b)
def uk_scan(kind):
    b = uk_title("Add Appliance", "Rating Label", 15)
    if kind == "app":
        b += rect(14, 80, 212, 110, "#2A2A2A10", "none", 10)
        for (x, y, dx, dy) in [(40, 92, 1, 1), (200, 92, -1, 1), (40, 178, 1, -1), (200, 178, -1, -1)]:
            b += f'<path d="M{x} {y+dy*14} V{y} H{x+dx*14}" fill="none" stroke="{LAGOON}" stroke-width="2.4" stroke-linecap="round"/>'
        b += rect(66, 108, 108, 54, "#F7F7F2", "#9E9E9E", 2) + "".join(rect(76, 118 + j * 10, 70 - j * 12, 4, "#C9C3B8") for j in range(4))
        b += t(14, 212, "Point your camera at the label.", 9, INK) + t(14, 226, "We fill in brand, model and serial.", 8, MUTE)
        b += rbtn(256, "Scan The Label", LAGOON)
    else:
        b += circ(40, 112, 18, LAGOON + "1F") + I("user", 28, 100, LAGOON, 24, 1.8)
        b += t(66, 108, LT, 12, INK, "khand") + t(66, 122, "scans every label at your", 8.5, MUTE) + t(66, 134, "first visit. Nothing to do.", 8.5, MUTE)
        b += rect(14, 160, 212, 40, "#FFFFFF", LINE, 10) + I("cal", 24, 170, INK, 18, 1.8) + t(50, 184, "First visit: Tue, Nov 4 (example)", 9, INK)
        b += rbtn(256, "Got It", INK, "outline")
    return uk(b)
def uk_pause2(kind):
    if kind == "pause":
        b = uk_title("Membership", "Pause Your Membership", 14)
        b += para(14, 90, ["Away for a while? Pause up to", "2 months a year. No visits, no charge."], 9, INK)
        for i, s in enumerate(["1 Month", "2 Months"]):
            x = 14 + i * 108; on = i == 0
            b += rect(x, 124, 104, 34, LAGOON + "14" if on else "#FFFFFF", LAGOON if on else LINE, 17, 1.5) + t(x + 52, 145, s, 10, LAGOON if on else INK, "hind", 600, "middle")
        b += t(14, 186, "Resumes automatically.", 8, MUTE)
        b += rbtn(256, "Pause Membership", LAGOON)
    else:
        b = uk_title("Membership", "Skip Your Next Visit", 14)
        b += para(14, 90, ["Busy season? Skip one visit.", "Your membership keeps going."], 9, INK)
        b += rect(14, 124, 212, 50, "#FFFFFF", LINE, 10) + I("cal", 24, 137, INK, 20, 1.8) + t(52, 146, "Next visit moves to", 8.5, MUTE) + t(52, 161, "the following season", 10, INK, "khand")
        b += t(14, 196, "No pause option.", 8, MUTE)
        b += rbtn(256, "Skip This Visit", INK, "outline")
    return uk(b)
def uk_stack(kind):
    b = uk_title("Offers", "Your Offers", 15)
    rows = [("Welcome Offer", "Applied at sign-up"), ("Referral Credit", "Friend joined (example)")]
    for i, (n, s) in enumerate(rows):
        y = 84 + i * 58
        on = kind == "stack" or i == 0
        b += rect(14, y, 212, 50, "#FFFFFF" if on else "#F5F3EF", LAGOON if on else LINE, 10, 1.5 if on else 1)
        b += t(26, y + 22, n, 12, INK if on else MUTE, "khand") + t(26, y + 37, s, 8, MUTE)
        b += (I("check", 196, y + 15, JUNGLE, 18, 2.4) if on else t(214, y + 30, "Can't combine", 7.5, MUTE, anchor="end"))
    b += t(14, 222, "Both offers apply together." if kind == "stack" else "One offer at a time.", 9, INK, "hind", 600)
    b += rbtn(256, "Continue", LAGOON)
    return uk(b)
def uk_remind2(kind):
    b = uk_title("Reminders", "Before Each Visit", 15)
    if kind == "text":
        b += rect(14, 84, 190, 60, "#F2F0EC", "none", 14) + para(24, 104, ["Smart UpKeep: your visit is", "Tue, Nov 4 at 9 AM.", "Reply C to confirm."], 9, INK, 13)
        b += rect(14, 156, 130, 30, "#FFFFFF", LAGOON, 15, 1.5) + I("cal", 24, 163, LAGOON, 15, 1.8) + t(44, 175, "Add To Calendar", 9, LAGOON, "hind", 600)
        b += t(14, 212, "Text 3 days before, with a calendar invite.", 8, MUTE)
    else:
        b += rect(14, 84, 212, 46, "#FFFFFF", LINE, 12) + I("bell", 24, 96, LAGOON, 18, 1.8) + t(50, 103, "Visit Tue, Nov 4 at 9 AM", 9.5, INK, "hind", 600) + t(50, 117, "App notification", 7.5, MUTE)
        b += rect(14, 140, 212, 46, "#FFFFFF", LINE, 12) + I("mail", 24, 152, INK, 18, 1.8) + t(50, 159, "Weekly Recap Email", 9.5, INK, "hind", 600) + t(50, 173, "Upcoming visits and tasks", 7.5, MUTE)
        b += t(14, 212, "App notification, then an email recap.", 8, MUTE)
    b += rbtn(256, "Save", INK)
    return uk(b)
def uk_found2(kind):
    b = uk_title("Membership", "Your Plan", 16)
    b += rect(14, 82, 212, 120, "#FFFFFF", LINE, 12)
    if kind == "tag": b += tag(26, 94, "Founding Member", SAFFRON, True)
    else: b += tag(26, 94, "Welcome Offer", LAGOON)
    b += t(26, 130, PRICE, 11.5, INK, "khand") + checks(156, ["Seasonal visits", "Home record"], JUNGLE)
    if kind == "tag": b += t(14, 222, "Founding members keep this rate for 12 months.", 7.8, MUTE)
    else: b += t(14, 222, "No founding badge; welcome offer only.", 7.8, MUTE)
    b += rbtn(256, "Start My Membership", LAGOON)
    return uk(b)
def uk_season2(kind):
    if kind == "month":
        b = uk_title("This Month", "November", 16)
        for i, (s, done) in enumerate([("Swap furnace filter", True), ("Clean gutters", False), ("Shut off outdoor taps", False)]):
            y = 84 + i * 40
            b += rect(14, y, 212, 34, "#FFFFFF", LINE, 10) + check_box(24, y + 11, done, JUNGLE) + t(44, y + 21, s, 9.5, INK if not done else MUTE)
        b += t(14, 222, "Only this month's 3 tasks.", 8, MUTE)
        b += rbtn(256, "See Next Month", INK, "outline")
    else:
        b = uk_title("Your Year", "Seasonal Plan", 16)
        seas = [("Winter", "snow", LAGOON, "D J F"), ("Spring", "leaf", JUNGLE, "M A M"), ("Summer", "sun", SAFFRON, "J J A"), ("Fall", "leaf", TERRA, "S O N")]
        for i, (n, ic, c, m) in enumerate(seas):
            x = 14 + (i % 2) * 108; y = 82 + (i // 2) * 70
            b += rect(x, y, 104, 62, "#FFFFFF", LINE, 10) + I(ic, x + 10, y + 10, c, 18, 1.8) + t(x + 34, y + 24, n, 11, INK, "khand") + t(x + 10, y + 50, m + "  ·  4 tasks", 7.5, MUTE)
        b += t(14, 236, "The whole year at a glance.", 8, MUTE)
        b += rbtn(256, "Open Month", INK, "outline")
    return uk(b)
def uk_ai2(kind):
    b = uk_title("Ask Anything", "Furnace Filter Size?", 14)
    b += rect(14, 82, 212, 82, LAGOON + "12", "none", 12) + t(24, 100, "AI ANSWER", 6.5, LAGOON, "hind", 600, extra='letter-spacing=".8"')
    b += para(24, 118, ["Your furnace uses a 16x25x1 filter.", "Last changed Oct 2 (example)."], 9, INK)
    if kind == "source":
        b += I("doc", 24, 142, MUTE, 13, 1.8) + t(42, 152, "From your home record · Furnace", 7.5, MUTE)
    else:
        b += rect(24, 140, 150, 16, "#FFFFFF", JUNGLE, 8, 1.2) + I("check", 30, 142, JUNGLE, 12, 2.4) + t(46, 151, "Checked by " + LT, 7.2, JUNGLE, "hind", 600)
    b += rbtn(186, "Text A Human", INK, "outline") + rbtn(224, "Looks Right", LAGOON)
    return uk(b)
def uk_appl2(kind):
    b = uk_title("Home Record", "Appliances", 16)
    items = [("Furnace", "gauge", "8 yrs"), ("Water Heater", "drop", "5 yrs"), ("Central AC", "snow", "8 yrs"), ("Electrical Panel", "bolt", "20 yrs")]
    if kind == "rows":
        for i, (n, ic, a) in enumerate(items):
            y = 80 + i * 36; b += ln(y) + t(14, y + 23, n, 10, INK) + t(226, y + 23, a, 9, MUTE, anchor="end")
        b += t(14, 238, "Rows with age, oldest flagged in the list.", 7.5, MUTE)
    else:
        for i, (n, ic, a) in enumerate(items):
            x = 14 + (i % 2) * 108; y = 80 + (i // 2) * 76
            b += rect(x, y, 104, 68, "#FFFFFF", LINE, 10) + I(ic, x + 10, y + 10, LAGOON, 20, 1.8) + t(x + 10, y + 48, n, 9.5, INK, "khand") + t(x + 10, y + 60, a, 7.5, MUTE)
    b += rbtn(256, "Add Appliance", INK)
    return uk(b)
def uk_wait2(kind):
    b = uk_title("Out Of Area", "We're Not There Yet", 14)
    b += rect(14, 80, 212, 140, CREAM, LINE, 12)
    if kind == "map":
        b += f'<path d="M40 110 Q80 92 120 104 T200 100 L196 170 Q150 184 110 172 T44 176 Z" fill="#FFFFFF" stroke="{LINE}"/>'
        b += circ(96, 138, 22, LAGOON + "22") + I("pin", 86, 124, LAGOON, 20, 1.8) + I("pin", 154, 126, MUTE, 14, 1.6)
        b += t(26, 204, "We start near you next (example).", 9, INK)
    else:
        b += t(120, 132, "128", 34, LAGOON, "khand", anchor="middle") + t(120, 152, "neighbors in your ZIP are waiting", 9, INK, anchor="middle")
        b += t(120, 168, "(example number)", 7.5, MUTE, anchor="middle") + t(120, 200, "More sign-ups bring us sooner.", 8.5, MUTE, anchor="middle")
    b += rbtn(256, "Join The Waitlist", LAGOON)
    return uk(b)

UK = [
    ("Tier Names", "Plain Names: Short Or With 'Home'?",
     ("uk_tier_short", "Essentials / Plus / Complete", "Your pick, with one line on who each plan fits.", ["clear", "simple", "direct", "practical"],
      uk_tiers2(["Essentials", "Plus", "Complete"], ["Core seasonal care", "Adds gutters and filters", "Everything, whole home"])),
     ("uk_tier_home", "Home Essentials / Home Plus / Home Complete", "Same names with 'Home' in front.", ["guided", "home", "clear", "warm"],
      uk_tiers2(["Home Essentials", "Home Plus", "Home Complete"], ["Core seasonal care", "Adds gutters and filters", "Everything, whole home"])), "refine"),
    ("Price Display", "Show The Starting Price Or Quote First?",
     ("uk_price_line", "Starting Price On The Plan Page", "One line: " + PRICE + ".", ["clear", "honest", "direct", "simple"], uk_pricev("line")),
     ("uk_price_quote", "Price After The Quote", "No number until the 2-minute home quote.", ["guided", "calm", "personal", "careful"], uk_pricev("quote")), "check"),
    ("Text A Human", "Who Answers Text A Human?",
     ("uk_human_tech", LT + " Answers", "Your own licensed tech replies.", ["personal", "trust", "warm", "neighbor"], uk_human2("tech")),
     ("uk_human_desk", "Member Care Desk Answers", "A support desk replies, then loops in the tech.", ["system", "fast", "clear", "pro"], uk_human2("desk")), "refine"),
    ("Accent Color", "Which Accent Pair For The App?",
     ("uk_acc_lagsaff", "Lagoon + Saffron", "Lagoon buttons and icons; saffron due tag.", ["fresh", "clear", "modern", "multi"], uk_accent2(LAGOON, SAFFRON, "Lagoon + Saffron")),
     ("uk_acc_terralag", "Terracotta + Lagoon", "Terracotta buttons and icons; lagoon tag.", ["warm", "brand", "lively", "multi"], uk_accent2(TERRA, LAGOON, "Terracotta + Lagoon")), "refine"),
    ("In-App Payment", "Pay In The App Or By Email Link?",
     ("uk_pay_app", "Pay In The App", "Card on file, charged monthly, receipts in the app.", ["easy", "modern", "fast", "system"], uk_pay("app")),
     ("uk_pay_link", "Pay By Email Link", "A secure link each month; no card stored.", ["careful", "simple", "calm", "trust"], uk_pay("link")), "refine"),
    ("Label Capture", "Who Captures Appliance Labels?",
     ("uk_scan_app", "Member Scans In The App", "Camera frame; we fill brand, model and serial.", ["fast", "modern", "easy", "visual"], uk_scan("app")),
     ("uk_scan_tech", LT + " Scans At First Visit", "Nothing for the member to do.", ["personal", "calm", "trust", "simple"], uk_scan("tech")), "refine"),
    ("Pause Policy", "Pause The Membership Or Skip A Visit?",
     ("uk_pause_months", "Pause Up To 2 Months A Year", "No visits and no charge while paused.", ["flexible", "friendly", "clear", "calm"], uk_pause2("pause")),
     ("uk_pause_skip", "Skip A Visit, No Pause", "Billing keeps going; the visit moves a season.", ["simple", "direct", "system", "clear"], uk_pause2("skip")), "refine"),
    ("Offer Stacking", "Can Offers Stack?",
     ("uk_stack_one", "One Offer At A Time", "Welcome offer or referral credit, not both.", ["simple", "clear", "careful", "direct"], uk_stack("one")),
     ("uk_stack_both", "Welcome + Referral Stack", "Both apply together.", ["generous", "friendly", "warm", "lively"], uk_stack("stack")), "refine"),
    ("Reminders", "How Should Visit Reminders Arrive?",
     ("uk_rem_textcal", "Text With A Calendar Invite", "Text 3 days before, Add To Calendar button.", ["direct", "fast", "personal", "practical"], uk_remind2("text")),
     ("uk_rem_pushmail", "App Notification + Email Recap", "Push notice, then a weekly email recap.", ["calm", "system", "thorough", "quiet"], uk_remind2("push")), "check"),
    ("Founding Badge", "Founding Member Tag Or None?",
     ("uk_found_tag", "Founding Member Tag", "Small saffron tag on the plan card.", ["warm", "clear", "special", "light"], uk_found2("tag")),
     ("uk_found_none", "No Badge, Welcome Offer Only", "Only the lagoon welcome offer tag.", ["simple", "calm", "minimal", "clear"], uk_found2("none")), "check"),
    ("Seasonal Plan", "This Month's Tasks Or The Whole Year?",
     ("uk_season_month", "This Month's 3 Tasks", "Short checklist for the current month.", ["simple", "focused", "calm", "clear"], uk_season2("month")),
     ("uk_season_year", "Four Seasons At A Glance", "Year view in four season tiles.", ["guided", "system", "visual", "thorough"], uk_season2("year")), "check"),
    ("Ask Anything", "AI Answer: Show The Source Or A Tech Check?",
     ("uk_ai_source", "Source From Your Home Record", "Small line showing where the answer came from.", ["clear", "honest", "system", "calm"], uk_ai2("source")),
     ("uk_ai_techcheck", "Checked By " + LT, "Green badge when your tech has confirmed it.", ["trust", "personal", "clear", "warm"], uk_ai2("tech")), "refine"),
    ("Home Record", "Appliances: Rows Or Tiles?",
     ("uk_appl_rows", "Appliance Rows With Age", "Simple list: name and age.", ["simple", "clear", "practical", "system"], uk_appl2("rows")),
     ("uk_appl_tiles", "Appliance Tiles With Icons", "Two-by-two tiles with drawn lagoon icons.", ["visual", "friendly", "guided", "modern"], uk_appl2("tiles")), "refine"),
    ("Out Of Area", "Warm Waitlist: Map Or Neighbor Count?",
     ("uk_wait_map", "Waitlist With A Small Map", "Cream card with a pin near the member.", ["warm", "visual", "calm", "neighbor"], uk_wait2("map")),
     ("uk_wait_count", "Waitlist With A Neighbor Count", "How many nearby are waiting (example number).", ["social", "lively", "clear", "warm"], uk_wait2("count")), "refine"),
]
for cat, ask, a, b, purpose in UK:
    add("Up Keep", f"Up Keep: {cat}", "Up Keep", ask,
        O(a[0], a[1], a[2], a[3], Vsvg(a[4])), O(b[0], b[1], b[2], b[3], Vsvg(b[4])), purpose=purpose)

# ========== D. Blog Topics follow-ups (10) ==========
def blog_title(title, dek, kicker="Post Title"):
    lines = wrap(title, 26)[:4]
    b = mw_hdr() + lbl(14, 56, kicker)
    b += "".join(t(14, 80 + i * 19, l, 15, INK, "khand") for i, l in enumerate(lines))
    y = 80 + len(lines) * 19 + 6
    b += para(14, y, wrap(dek, 42)[:3], 8.5, MUTE)
    b += tag(14, 226, "Blog", LAGOON) + tag(60, 226, "Draft", SAFFRON, True)
    b += rbtn(256, "Use This", INK)
    return screen(b, head=False)
def blog_angle(head, kind, items, note=""):
    b = mw_hdr() + lbl(14, 54, "Angle") + h1(14, 74, head, 15)
    if kind == "steps":
        for i, s in enumerate(items):
            y = 88 + i * 30
            b += circ(24, y + 12, 9, LAGOON + "1F") + t(24, y + 15.5, str(i + 1), 9, LAGOON, "khand", anchor="middle") + t(40, y + 16, s, 9.5, INK)
    elif kind == "table":
        b += t(14, 98, "TRADE", 6.5, MUTE, "hind", 600) + t(160, 98, "REAL BID", 6.5, MUTE, "hind", 600, "end") + t(226, 98, "PADDED", 6.5, MUTE, "hind", 600, "end")
        for i, (a, r, p) in enumerate(items):
            y = 104 + i * 26
            b += ln(y) + t(14, y + 17, a, 9.5, INK) + t(160, y + 17, r, 9.5, JUNGLE, "hind", 600, "end") + t(226, y + 17, p, 9.5, MUTE, "hind", 400, "end")
    elif kind == "flags":
        for i, s in enumerate(items):
            y = 88 + i * 30
            b += rect(14, y, 212, 24, "#FFFFFF", LINE, 12) + circ(28, y + 12, 4, PERSIM) + t(40, y + 16, s, 9, INK)
    elif kind == "check":
        for i, s in enumerate(items):
            y = 88 + i * 28
            b += check_box(14, y + 4, False, LAGOON) + t(34, y + 13, s, 9.5, INK)
    elif kind == "weeks":
        for i, (wk, s) in enumerate(items):
            y = 88 + i * 30
            b += rect(14, y, 46, 22, LAGOON + "14", "none", 11) + t(37, y + 15, wk, 8, LAGOON, "hind", 600, "middle") + t(68, y + 15, s, 9.5, INK)
    if note: b += t(14, 240, note, 7.5, MUTE)
    b += rbtn(256, "Use This Angle", INK)
    return screen(b, head=False)
def blog_lead(kind, title):
    b = rect(0, 0, W, 156, "#EFE9DF")
    if kind == "clipboard":
        b += rect(78, 22, 84, 116, "#FFFFFF", INK, 4, 1.6) + rect(102, 16, 36, 12, INK, "none", 3) + "".join(rect(90, 44 + j * 14, 60 - (j % 2) * 18, 4, "#C9C3B8") for j in range(5)) + rect(90, 118, 40, 8, LAGOON + "55", "none", 2)
        b += rect(0, 140, W, 16, "#D8CDBE")
    elif kind == "number":
        b = rect(0, 0, W, 156, "#FFFFFF") + t(120, 92, "One Price", 32, INK, "khand", anchor="middle") + rect(70, 104, 100, 3, SAFFRON, "none", 1.5) + t(120, 126, "Not a percentage", 10, MUTE, anchor="middle")
    elif kind == "drawing":
        b += "".join(f'<line x1="{x}" y1="10" x2="{x}" y2="146" stroke="#05668D22"/>' for x in range(10, W, 16))
        b += rect(40, 34, 160, 90, "none", INK, 0, 1.6) + rect(40, 34, 70, 50, "none", INK, 0, 1.2) + f'<path d="M120 60 q20 -18 40 0 t40 0" fill="none" stroke="{TERRA}" stroke-width="2.4"/>' + circ(150, 96, 14, "none", TERRA, 2.4)
    elif kind == "form":
        b += rect(60, 18, 120, 124, "#FFFFFF", LINE, 4) + t(72, 40, "CHANGE ORDER #3", 7, INK, "hind", 700) + "".join(rect(72, 52 + j * 14, 90, 4, "#C9C3B8") for j in range(4))
        b += t(72, 124, "Approved", 9, JUNGLE, "khand") + f'<path d="M110 124 q10 -12 20 0 t20 -4" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    elif kind == "lot":
        b = rect(0, 0, W, 156, "#DCEAF0") + rect(0, 96, W, 60, "#C9D6B4") + "".join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+20}" stroke="#6B4B3A" stroke-width="2"/>' + rect(x - 1, y, 6, 4, PERSIM) for x, y in [(60, 96), (180, 96), (40, 124), (200, 124)])
        b += f'<polyline points="62,100 182,100 202,128 42,128 62,100" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 3"/>'
    elif kind == "frame":
        b = rect(0, 0, W, 156, "#F4E2C6") + rect(0, 128, W, 28, "#D9C9A8") + f'<polyline points="50,128 50,70 120,30 190,70 190,128" fill="none" stroke="#8A6A4A" stroke-width="2"/>'
        b += "".join(f'<line x1="{x}" y1="{70 if x in (50, 190) else 40 + abs(120 - x) * .57}" x2="{x}" y2="128" stroke="#8A6A4A" stroke-width="1.4"/>' for x in range(62, 190, 12))
    b += t(14, 178, "MAX WEBERMAN", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"')
    b += "".join(t(14, 198 + i * 18, l, 14, INK, "khand") for i, l in enumerate(wrap(title, 30)[:2]))
    b += rbtn(256, "Use This Image", INK, "outline")
    return svgwrap(b)
def blog_yes2(title, pitch):
    lines = wrap(title, 26)[:4]
    b = mw_hdr() + lbl(14, 56, "New Topic") + h1(14, 76, "Write This?", 16)
    b += rect(14, 88, 212, 150, "#FFFFFF", LINE, 10)
    b += "".join(t(24, 112 + i * 17, l, 12, INK, "khand") for i, l in enumerate(lines))
    b += para(24, 112 + len(lines) * 17 + 8, wrap(pitch, 40)[:3], 8, MUTE)
    b += tag(24, 220, "Blog", LAGOON)
    b += rbtn(256, "Write This Post", TERRA)
    return screen(b, head=False)
def blog_notnow2():
    b = mw_hdr() + lbl(14, 56, "Hold") + h1(14, 76, "Not Now", 18)
    b += rect(14, 96, 212, 120, "#F7F5F1", LINE, 10) + I("hold", 108, 120, MUTE, 24, 2.2)
    b += t(120, 172, "Keep it in the idea list.", 9, MUTE, anchor="middle")
    b += rbtn(256, "Not Now", MUTE, "outline")
    return screen(b, head=False)

BT = [
    ("Flat Fee Post: Which Title?",
     ("blog_ff_t_vs", "Flat Fee vs. Percentage: What It Means for Your Budget", "Comparison title; plain math up front.", ["clear", "practical", "direct", "guided"],
      blog_title("Flat Fee vs. Percentage: What It Means for Your Budget", "Side-by-side math on a sample custom home.")),
     ("blog_ff_t_why", "Why I Charge a Flat Fee (and What It Saves You)", "First-person title with the payoff.", ["personal", "direct", "warm", "clear"],
      blog_title("Why I Charge a Flat Fee (and What It Saves You)", "My reason, then what it means for your budget.")), "refine"),
    ("Sub Bids Post: Which Angle?",
     ("blog_sb_a_table", "Show A Real Bid Sheet", "Example trades with real bid vs. padded number.", ["clear", "honest", "system", "visual"],
      blog_angle("Real Bids, Side by Side", "table", [("Framing", "$48,200", "$56,000"), ("Electrical", "$21,900", "$27,500"), ("HVAC", "$18,400", "$23,000"), ("Drywall", "$12,600", "$16,000")], "Example numbers only")),
     ("blog_sb_a_signs", "5 Signs Of A Padded Estimate", "Numbered warning signs readers can check.", ["guided", "practical", "direct", "clear"],
      blog_angle("5 Signs of a Padded Estimate", "steps", ["One lump sum, no trades", "No sub names or dates", "Big round numbers", "Vague allowances", "No bid copies shared"])), "refine"),
    ("Change Orders Post: Which Title?",
     ("blog_co_t_how", "How Change Orders Should Work", "Short, plain, process title.", ["simple", "clear", "direct", "calm"],
      blog_title("How Change Orders Should Work", "Price, time, and sign-off before any work moves.")),
     ("blog_co_t_steps", "Change Orders Without the Fight: A 4-Step Process", "Promise plus numbered process.", ["guided", "practical", "clear", "system"],
      blog_title("Change Orders Without the Fight: A 4-Step Process", "The four steps I use on every job.")), "refine"),
    ("Pick A Builder Post: Which Angle?",
     ("blog_pb_a_check", "10-Question Checklist", "A checklist readers can print and bring.", ["guided", "practical", "clear", "system"],
      blog_angle("Ask These Before You Sign", "check", ["Can I see real sub bids?", "Who runs my site daily?", "How are changes priced?", "What does the warranty cover?", "Can I call 3 past clients?"], "Printable checklist")),
     ("blog_pb_a_flags", "Red Flags Before You Sign", "The warning signs that end the meeting.", ["direct", "strong", "clear", "practical"],
      blog_angle("Red Flags Before You Sign", "flags", ["No written schedule", "Deposit over 10% up front", "Allowances with no detail", "No license or insurance shown", "Pressure to sign today"])), "refine"),
    ("Custom Home Post: Which Angle?",
     ("blog_ch_a_order", "The Five Decisions, In Order", "Numbered order: site to budget.", ["guided", "clear", "system", "practical"],
      blog_angle("The First Five Decisions", "steps", ["Site and soil", "Footprint and size", "Structure", "Envelope", "Budget lock"])),
     ("blog_ch_a_weeks", "Your First Month, Week By Week", "What happens in weeks 1 to 4.", ["guided", "story", "practical", "warm"],
      blog_angle("Your First Month", "weeks", [("Week 1", "Walk the site, set budget"), ("Week 2", "Footprint and survey"), ("Week 3", "Structure options"), ("Week 4", "Envelope and lock")])), "refine"),
    ("Flat Fee Post: Which Lead Image?",
     ("blog_ff_img_clip", "Contract On A Clipboard", "Drawn clipboard on site, one highlighted line.", ["warm", "real", "story", "natural"], blog_lead("clipboard", "Why I Charge a Flat Fee")),
     ("blog_ff_img_num", "Simple Type Graphic", "'One Price' with a saffron underline.", ["clear", "direct", "brand", "simple"], blog_lead("number", "Why I Charge a Flat Fee")), "refine"),
    ("Change Orders Post: Which Lead Image?",
     ("blog_co_img_draw", "Marked-Up Drawing", "Plan sheet with a terracotta change circled.", ["visual", "real", "clear", "story"], blog_lead("drawing", "How Change Orders Should Work")),
     ("blog_co_img_form", "Signed Change Order Form", "Form with Approved and a signature.", ["clear", "practical", "trust", "system"], blog_lead("form", "How Change Orders Should Work")), "refine"),
    ("Custom Home Post: Which Lead Image?",
     ("blog_ch_img_lot", "Empty Lot With Stakes", "Day one: grass, sky, survey stakes.", ["natural", "light", "story", "calm"], blog_lead("lot", "Planning a Custom Home")),
     ("blog_ch_img_frame", "Framing At Golden Hour", "The house taking shape in warm light.", ["warm", "visual", "story", "natural"], blog_lead("frame", "Planning a Custom Home")), "refine"),
]
for ask, a, b, purpose in BT:
    add("Blog Topics", "Blog Topics", "maxweberman.com Blog", ask,
        O(a[0], a[1], a[2], a[3], Vsvg(a[4])), O(b[0], b[1], b[2], b[3], Vsvg(b[4])), purpose=purpose)
for slug, title, pitch in [
    ("punch", "Punch Lists: How a Good Builder Finishes a Job", "What a clean close-out looks like, item by item."),
    ("schedule", "What a Real Construction Schedule Looks Like", "Dates, trades, and float, and how to read one."),
]:
    add("Blog Topics", "Blog Topics", "maxweberman.com Blog", "New Topic: Write This Post?",
        O(f"blog_new_{slug}", title, pitch, ["clear", "practical", "direct", "guided"], Vsvg(blog_yes2(title, pitch))),
        O(f"blog_new_{slug}_no", "Not Now", "Keep it in the idea list.", ["calm", "simple", "quiet", "later"], Vsvg(blog_notnow2())), purpose="new")

# ========== E. Blog Style (4) ==========
def post_mock(order):
    if order == "photo":
        b = rect(0, 0, W, 128, "#DCEAF0") + rect(0, 86, W, 42, "#C9D6B4") + rect(84, 52, 72, 40, "#FFFFFF", INK, 0, 1.4) + f'<polyline points="78,54 120,28 162,54" fill="none" stroke="{INK}" stroke-width="1.8"/>'
        b += t(14, 150, "MAX WEBERMAN", 7.5, MUTE, "hind", 600, extra='letter-spacing="1"') + h1(14, 172, "Planning a Custom Home", 16)
        b += para(14, 190, ["The first five decisions, in order."], 9, MUTE)
    else:
        b = rect(0, 0, W, 36, "#FFFFFF") + t(14, 24, "MAX WEBERMAN", 11, INK, "khand") + ln(36, 0, W)
        b += h1(14, 66, "Planning a Custom Home", 18) + para(14, 86, ["The first five decisions, in order."], 9.5, MUTE)
        b += rect(14, 104, 212, 96, "#DCEAF0", "none", 8) + rect(14, 166, 212, 34, "#C9D6B4", "none", 0) + rect(92, 136, 56, 30, "#FFFFFF", INK, 0, 1.4) + f'<polyline points="86,138 120,118 154,138" fill="none" stroke="{INK}" stroke-width="1.8"/>'
    b += rbtn(256, "Read", INK, "outline")
    return svgwrap(b)
def heads_mock(case):
    hs = ["The First Five Decisions", "Why Order Matters", "What It Costs To Skip A Step"] if case == "title" else ["The first five decisions", "Why order matters", "What it costs to skip a step"]
    b = mw_hdr()
    for i, hh in enumerate(hs):
        y = 64 + i * 62
        b += t(14, y, hh, 14, INK, "khand") + para(14, y + 16, ["Before finishes or fixtures, the site", "sets the budget. Then the footprint."], 8.5, MUTE)
    b += rbtn(256, "Keep Reading", INK, "outline")
    return screen(b, head=False)
def steps_mock(kind):
    b = mw_hdr() + h1(14, 62, "Change Orders in 4 Steps", 15)
    steps = ["Write the change", "Price it in writing", "Agree on time added", "Sign before work"]
    if kind == "check":
        for i, s in enumerate(steps):
            y = 78 + i * 34
            b += rect(14, y, 212, 28, "#FFFFFF", LINE, 8) + t(24, y + 18, f"{i+1}.", 10, LAGOON, "khand") + t(40, y + 18, s, 9.5, INK) + check_box(204, y + 8, i == 0, JUNGLE)
    else:
        exs = ["Swap tile in the main bath", "+$1,850, sub quote attached", "+2 days to tile schedule", "Owner signs in the app"]
        for i, (s, e) in enumerate(zip(steps, exs)):
            y = 80 + i * 40
            b += t(14, y + 10, f"{i+1}. {s}", 10, INK, "hind", 600) + t(26, y + 25, "Example: " + e, 8, MUTE)
    b += rbtn(256, "Keep Reading", INK, "outline")
    return screen(b, head=False)
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Head To Head: Photo First Or Headline First?",
    O("blog_lead_photo2", "Photo First, Then Headline", "Big photo on top, title under it.", ["visual", "warm", "story", "natural"], Vsvg(post_mock("photo"))),
    O("blog_lead_head2", "Headline First, Then Photo", "Title and summary on top, photo below.", ["clear", "direct", "editorial", "simple"], Vsvg(post_mock("head"))), purpose="retest", retest=True)
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Whose Voice In Advice Posts?",
    O("blog_voice_max2", "Max Speaking", "'I tell every client to ask for the bid sheet.'", ["personal", "direct", "warm", "clear"],
      Vtone(["I tell every client to ask for the real bid sheet.", "If a builder won't share it, keep looking."], "Max → Reader")),
    O("blog_voice_firm2", "The Firm Speaking", "'At Weberman Construction, we share every bid.'", ["pro", "calm", "formal", "clear"],
      Vtone(["At Weberman Construction, we share every sub bid.", "Ask any builder you meet for the same."], "Weberman Construction → Reader")), purpose="check")
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Section Headings: Which Case Reads Better?",
    O("blog_case_title2", "Title Case Headings", "Every Major Word Capitalized.", ["clear", "strong", "brand", "direct"], Vsvg(heads_mock("title"))),
    O("blog_case_sent2", "Sentence case headings", "Only the first word capitalized.", ["calm", "simple", "soft", "web"], Vsvg(heads_mock("sentence"))), purpose="check")
add("Blog Style", "Blog Writing Style", "maxweberman.com Blog", "Numbered Steps: Checklist Or Example Under Each?",
    O("blog_steps_check", "Steps With Check Boxes", "Each step in a box readers can tick.", ["guided", "practical", "system", "clear"], Vsvg(steps_mock("check"))),
    O("blog_steps_example", "Steps With An Example Under Each", "A real-world example line under every step.", ["thorough", "practical", "clear", "depth"], Vsvg(steps_mock("example"))))

# ========== F. Home Guide + Finish Questions (4) — Construction; Home Guide is customer-facing ==========
def hg(app_name, body):
    head = rect(0, 0, W, 36, "#FFFFFF") + t(14, 24, app_name.upper(), 10, INK, "khand") + ln(36, 0, W)
    return svgwrap(head + body)
def hg_war(kind):
    b = h1(14, 62, "Warranties", 16)
    for i, (n, d, c, solid) in enumerate([("Roof · Example Brand", "Ends 2034", JUNGLE, False), ("Water Heater", "Ends In 60 Days", SAFFRON, True)]):
        y = 76 + i * 78
        b += rect(14, y, 212, 70, "#FFFFFF", LINE, 10) + t(24, y + 20, n, 11, INK, "khand") + tag(24, y + 28, d, c, solid)
        if kind == "call":
            b += rect(24, y + 46, 96, 18, "#FFFFFF", LAGOON, 9, 1.3) + I("phone", 30, y + 49, LAGOON, 12, 1.8) + t(46, y + 58.5, "Call To Claim", 7.5, LAGOON, "hind", 600)
        else:
            b += I("doc", 24, y + 46, LAGOON, 14, 1.8) + t(42, y + 57, "Open Warranty PDF", 8, LAGOON, "hind", 600, extra='text-decoration="underline"')
    b += rbtn(256, "Add Warranty", INK, "outline")
    return hg("Home Guide", b)
def hg_shut(kind):
    b = h1(14, 62, "Shutoffs", 16)
    if kind == "system":
        groups = [("Water", "drop", LAGOON, [("Main Water", "Basement")]), ("Gas", "gauge", SAFFRON, [("Gas Meter", "Exterior, East")]), ("Power", "bolt", TERRA, [("Main Panel", "Garage")])]
    else:
        groups = [("Basement", "home", INK, [("Main Water", "North wall")]), ("Garage", "home", INK, [("Main Panel", "Left of door")]), ("Exterior", "home", INK, [("Gas Meter", "East side")])]
    y = 76
    for g, ic, c, rows in groups:
        b += I(ic, 14, y, c, 14, 1.9) + t(34, y + 11, g.upper(), 7, MUTE, "hind", 600, extra='letter-spacing="1"')
        for n, r in rows:
            b += ln(y + 18) + t(14, y + 38, n, 11, INK, "khand") + t(226, y + 38, r, 8.5, MUTE, anchor="end")
        y += 56
    b += rbtn(256, "Edit", INK, "outline")
    return hg("Home Guide", b)
def fq_skip2(kind):
    b = lbl(14, 54, "Question 7 of 20") + pbar(60, .35, LAGOON) + h1(14, 88, "Kitchen Backsplash", 15) + para(14, 106, ["Brand and color still open."], 9.5, MUTE)
    if kind == "end":
        b += rect(14, 128, 212, 50, LAGOON + "10", "none", 10) + I("list", 24, 141, LAGOON, 18, 1.8) + para(50, 148, ["Skipped questions come back", "at the end."], 8.5, INK)
    else:
        b += rect(14, 128, 212, 50, "#FFFFFF", LINE, 10) + I("hold", 24, 141, SAFFRON, 18, 2) + para(50, 148, ["Skipped questions go to a", "Later list you open anytime."], 8.5, INK)
        b += rect(150, 40, 76, 20, SAFFRON + "26", "none", 10) + t(188, 54, "Later (3)", 8, HOLDTXT, "hind", 600, "middle")
    b += rbtn(214, "Answer", INK) + rbtn(252, "Skip", MUTE, "outline")
    return hg("Finish Questions", b)
def hg_contacts(kind):
    b = h1(14, 62, "Who To Call", 16)
    rows = [("Plumber", "drop", "(555) 010-0141"), ("Electrician", "bolt", "(555) 010-0172"), ("Heating And Cooling", "gauge", "(555) 010-0118")]
    for i, (n, ic, ph) in enumerate(rows):
        if kind == "list":
            y = 76 + i * 44
            b += ln(y) + t(14, y + 20, n, 11, INK, "khand") + t(14, y + 34, ph + " (example)", 8, MUTE) + circ(212, y + 22, 12, LAGOON + "14") + I("phone", 205, y + 15, LAGOON, 14, 1.8)
        else:
            y = 74 + i * 56
            b += rect(14, y, 212, 50, "#FFFFFF", LINE, 10) + circ(36, y + 25, 14, LAGOON + "14") + I(ic, 27, y + 16, LAGOON, 18, 1.8)
            b += t(58, y + 22, n, 11, INK, "khand") + t(58, y + 36, ph + " (example)", 8, MUTE)
    b += rbtn(256, "Add Contact", INK, "outline")
    return hg("Home Guide", b)
HGP = [
    ("Home Guide: Warranty Card", "Home Guide", "Warranty Cards: Call Button Or Document Link?",
     ("hg_war_call", "Card With Call To Claim", "End date chip plus a tap-to-call pill.", ["guided", "practical", "clear", "action"], hg_war("call")),
     ("hg_war_doc", "Card With Warranty PDF Link", "End date chip plus a link to the document.", ["calm", "simple", "clear", "record"], hg_war("doc"))),
    ("Home Guide: Shutoff List", "Home Guide", "Shutoff List: Group By System Or By Room?",
     ("hg_shut_system", "Grouped By System", "Water, gas, power, each with a drawn icon.", ["clear", "guided", "safe", "system"], hg_shut("system")),
     ("hg_shut_room", "Grouped By Room", "Basement, garage, exterior.", ["simple", "home", "calm", "clear"], hg_shut("room"))),
    ("Finish Questions: After A Skip", "Finish Questions", "Skipped Questions: Back At The End Or A Later List?",
     ("fq_skip_end", "Skipped Come Back At The End", "Same flow; skipped ones return last.", ["simple", "guided", "calm", "clear"], fq_skip2("end")),
     ("fq_skip_later", "Skipped Go To A Later List", "A Later tab you open whenever.", ["flexible", "control", "clear", "light"], fq_skip2("later"))),
    ("Home Guide: Contacts", "Home Guide", "Who To Call: Text List Or Cards With Icons?",
     ("hg_ct_list", "Text List With Call Button", "Trade, number, round call button.", ["simple", "fast", "minimal", "clear"], hg_contacts("list")),
     ("hg_ct_cards", "Cards With Trade Icons", "Each trade as a card with a drawn icon.", ["visual", "friendly", "guided", "clear"], hg_contacts("cards"))),
]
for cat, app, ask, a, b in HGP:
    add("Home Guide", cat, app, ask, O(a[0], a[1], a[2], a[3], Vsvg(a[4])), O(b[0], b[1], b[2], b[3], Vsvg(b[4])))

# ========== G. Variety (9) ==========
def scene(sky, ground, extra, title, sub, tg, tgc):
    b = rect(0, 0, W, 170, sky) + rect(0, 130, W, 40, ground) + extra
    b += h1(14, 200, title, 16) + para(14, 218, [sub], 9, MUTE) + tag(14, 236, tg, tgc)
    return svgwrap(b, "#FFFFFF")
def cafe2(kind):
    if kind == "window":
        ex = rect(30, 26, 120, 90, "#FFFFFF", "#D6D0C6", 0, 3) + f'<line x1="90" y1="26" x2="90" y2="116" stroke="#D6D0C6" stroke-width="3"/>' + rect(20, 116, 200, 10, "#C8A57E") + rect(160, 96, 16, 20, LAGOON, "none", 2) + rect(170, 102, 12, 8, "none", LAGOON, 4, 2)
        return scene("#F7F4EE", "#E8DFD4", ex, "Bright Corner Window Seat", "Morning sun, white oak counter.", "Cafe", LAGOON)
    ex = circ(50, 70, 36, "#8DB580") + circ(190, 64, 40, "#7FA872") + rect(80, 104, 80, 6, "#C8A57E") + rect(116, 110, 8, 26, "#8A6A4A") + rect(150, 112, 18, 18, TERRA, "none", 2)
    return scene("#E6EFE4", "#D9CDB8", ex, "Garden Patio Shade Table", "Tree shade, terracotta pots.", "Cafe", TERRA)
def travel2(kind):
    if kind == "coast":
        ex = rect(0, 104, W, 26, "#9CC7D8") + rect(40, 70, 50, 40, "#FFFFFF") + rect(96, 60, 40, 50, "#F7F4EE") + rect(142, 76, 46, 34, "#FFFFFF") + f'<polyline points="40,70 65,56 90,70" fill="#E4572E55"/>'
        return scene("#CFE3EE", "#EFE6D6", ex, "Harbor Walk, Quiet Coast Town", "Low white houses, slow mornings.", "Travel", LAGOON)
    ex = f'<path d="M0 130 L60 70 L120 100 L180 60 L240 110 V130 Z" fill="#D9C2A0"/>' + rect(96, 84, 48, 46, "#EADBC4") + rect(112, 104, 14, 26, "#8A6A4A") + f'<polyline points="90,86 120,68 150,86" fill="#C1502E55"/>'
    return scene("#F2DCC4", "#CDB89A", ex, "Stone Lane, Hill Town", "Warm stone, first light.", "Travel", TERRA)
def plant2(kind):
    if kind == "tall":
        ex = rect(104, 108, 32, 24, TERRA, "none", 3) + f'<path d="M120 108 C112 80 100 60 108 36 M120 108 C126 76 140 58 132 30" stroke="{JUNGLE}" stroke-width="3" fill="none"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="7" fill="{JUNGLE}" transform="rotate({r} {x} {y})"/>' for x, y, r in [(104, 50, -30), (136, 44, 30), (110, 72, -20), (134, 70, 25), (116, 90, -10)])
        return scene("#FAF6EE", "#EFE6D6", ex, "One Tall Plant In A Corner", "A single green statement.", "Plants", JUNGLE)
    ex = "".join(rect(x, 110, 28, 22, c, "none", 3) + circ(x + 14, 96, 16, g) for x, c, g in [(60, "#D4C4B0", JUNGLE), (106, TERRA, "#3E8E6E"), (152, "#FFFFFF", JUNGLE)])
    return scene("#FAF6EE", "#EFE6D6", ex, "Cluster Of Three Small Pots", "Mixed greens on one shelf.", "Plants", JUNGLE)
def table2(kind):
    if kind == "out":
        ex = f'<path d="M10 30 Q120 60 230 30" stroke="#8A6A4A" fill="none"/>' + "".join(circ(x, 30 + 30 * (1 - ((x - 120) / 110) ** 2) * .5 + 6, 4, SAFFRON) for x in range(30, 220, 24)) + rect(30, 100, 180, 10, "#C8A57E") + "".join(circ(x, 96, 8, "#F3ECE1", LINE) for x in (60, 100, 140, 180))
        return scene("#E8EEF2", "#D9CDB8", ex, "Shared Table Outdoors", "String lights, long wood table.", "Food", SAFFRON)
    ex = rect(20, 30, 200, 60, "#FFFFFF", "#E5E0D8") + rect(40, 40, 50, 40, "#CFE3EE") + rect(30, 100, 180, 10, "#C8A57E") + "".join(circ(x, 96, 8, "#F3ECE1", LINE) for x in (60, 100, 140, 180))
    return scene("#F7F4EE", "#E8DFD4", ex, "Shared Table, Bright Kitchen", "Family bowls by a big window.", "Food", LAGOON)
def watch2(col, name):
    b = circ(120, 112, 70, "none", INK, 3) + circ(120, 112, 60, "#FFFFFF") + "".join(f'<line x1="{120 + 52 * __import__("math").sin(a * 0.5236):.1f}" y1="{112 - 52 * __import__("math").cos(a * 0.5236):.1f}" x2="{120 + 58 * __import__("math").sin(a * 0.5236):.1f}" y2="{112 - 58 * __import__("math").cos(a * 0.5236):.1f}" stroke="{INK}" stroke-width="1.6"/>' for a in range(12))
    b += f'<line x1="120" y1="112" x2="120" y2="72" stroke="{INK}" stroke-width="2.6"/><line x1="120" y1="112" x2="150" y2="112" stroke="{INK}" stroke-width="2.6"/><line x1="120" y1="126" x2="120" y2="58" stroke="{col}" stroke-width="1.4"/>' + circ(120, 112, 3, col)
    b += t(120, 214, name, 14, INK, "khand", anchor="middle") + t(120, 232, "White dial, one colored second hand", 8.5, MUTE, anchor="middle")
    return svgwrap(b)
def cover2(kind):
    b = rect(0, 0, W, H, "#F4F1EA") + rect(50, 20, 140, 200, "#FFFFFF", LINE)
    b += rect(50, 20, 140, 200, "#DCEAF0") + rect(50, 150, 140, 70, "#C9D6B4") + rect(96, 110, 48, 40, "#FFFFFF", INK, 0, 1.4) + f'<polyline points="90,112 120,90 150,112" fill="none" stroke="{INK}" stroke-width="1.8"/>'
    if kind == "band":
        b += rect(50, 186, 140, 34, "#FFFFFF") + t(60, 208, "THE JOBSITE", 12, INK, "khand")
    else:
        b += t(60, 46, "THE", 12, INK, "khand") + t(60, 62, "JOBSITE", 16, INK, "khand")
    b += t(14, 246, "Title In A White Band At The Bottom" if kind == "band" else "Title Over The Photo, Top Left", 11, INK, "khand") + t(14, 262, "Photo-led cover", 8.5, MUTE)
    return svgwrap(b)
def texture2(kind):
    if kind == "linen":
        b = rect(0, 0, W, H, "#FBF7EF") + "".join(f'<path d="M{x} 0 Q{x+8} 110 {x} 220" stroke="#E6DCCB" stroke-width="10" fill="none" opacity=".7"/>' for x in range(20, W, 26))
        b += rect(0, 0, 70, 220, "#FFF6DA88")
        t1, t2 = "Linen Curtain In Sun", "Light through a loose weave."
    else:
        b = rect(0, 0, W, H, "#EFE7DA") + f'<path d="M0 0 L120 0 L60 220 L0 220 Z" fill="#00000010"/>' + "".join(circ(x, y, 1, "#00000014") for x in range(10, W, 17) for y in range(10, 220, 19))
        t1, t2 = "Plaster Wall With Soft Shadow", "Matte mineral wall, slow shade."
    b += rect(0, 220, W, 80, "#FFFFFFE6") + h1(14, 250, t1, 15) + t(14, 270, t2, 9, MUTE)
    return svgwrap(b)
def light2(kind):
    if kind == "morning":
        b = rect(0, 0, W, H, "#FAF6EE") + rect(60, 20, 120, 110, "#DCEAF0", "#FFFFFF", 0, 4) + f'<path d="M60 130 L20 220 H200 L180 130 Z" fill="#FFF3D6"/>'
        t1, t2 = "Morning Window Light", "Cool sky, a warm patch on the floor."
    else:
        b = rect(0, 0, W, H, "#F3ECE1") + f'<line x1="120" y1="0" x2="120" y2="60" stroke="{INK}"/>' + f'<path d="M96 60 H144 L132 80 H108 Z" fill="{INK}"/>' + f'<path d="M108 80 L60 170 H180 L132 80 Z" fill="#F7D98A66"/>' + rect(50, 170, 140, 10, "#C8A57E")
        t1, t2 = "Evening Pendant Over The Table", "One warm pool of light."
    b += h1(14, 246, t1, 15) + t(14, 266, t2, 9, MUTE)
    return svgwrap(b)
def bag2(kind):
    b = rect(0, 0, W, H, "#FFFFFF")
    c, st = ("#E8DEC8", "#B8A888") if kind == "canvas" else ("#9A6A44", "#6E4A2E")
    b += rect(40, 80, 160, 100, c, st, 16, 2) + f'<path d="M84 80 Q84 40 120 40 Q156 40 156 80" fill="none" stroke="{st}" stroke-width="6"/>' + rect(40, 120, 160, 6, LAGOON if kind == "canvas" else "#6E4A2E")
    b += h1(14, 222, "Canvas Weekend Bag" if kind == "canvas" else "Leather Weekend Bag", 16) + t(14, 242, "Light, washable, lagoon stripe." if kind == "canvas" else "Warm brown, ages with use.", 9, MUTE)
    return svgwrap(b)

VAR = [
    ("Cafés", "Head To Head: Which Cafe Today?",
     ("var_cafe_window", "Bright Corner Window Seat", "White oak, morning sun, lagoon cup.", ["light", "natural", "calm", "clear"], cafe2("window")),
     ("var_cafe_patio", "Garden Patio Shade Table", "Tree shade and terracotta pots.", ["natural", "warm", "outdoor", "lively"], cafe2("patio")), "retest"),
    ("Travel & Hotel Vibes", "Head To Head: Which Trip Next?",
     ("var_tv_harbor", "Quiet Coast Town", "Harbor walk, low white houses.", ["light", "calm", "travel", "fresh"], travel2("coast")),
     ("var_tv_stone", "Hill Town Morning", "Stone lanes in first light.", ["warm", "natural", "travel", "quiet"], travel2("hill")), "retest"),
    ("Plants & Greenery", "Head To Head: One Plant Or A Cluster?",
     ("var_pl_tall", "One Tall Plant", "Single statement green in a corner.", ["simple", "focused", "natural", "calm"], plant2("tall")),
     ("var_pl_three", "Cluster Of Three Pots", "Mixed greens on one shelf.", ["lively", "natural", "warm", "home"], plant2("three")), "retest"),
    ("Food & Table", "Shared Table: Outdoors Or Bright Kitchen?",
     ("var_fd_outdoor", "Shared Table Outdoors", "Long table under string lights.", ["warm", "outdoor", "lively", "friendly"], table2("out")),
     ("var_fd_kitchen", "Shared Table, Bright Kitchen", "Family bowls by a big window.", ["light", "home", "calm", "natural"], table2("in")), "refine"),
    ("Watches & EDC", "Dress Watch: Which Second Hand?",
     ("var_wa_lagoon", "Lagoon Second Hand", "White dial, one lagoon hand.", ["clear", "fresh", "calm", "modern"], watch2(LAGOON, "Lagoon Second")),
     ("var_wa_saffron", "Saffron Second Hand", "White dial, one saffron hand.", ["warm", "lively", "clear", "light"], watch2(SAFFRON, "Saffron Second")), "refine"),
    ("Book & Magazine Covers", "Photo Cover: Where Does The Title Go?",
     ("var_bk_band", "Title In A Bottom Band", "Photo on top, white band with the title.", ["clear", "calm", "editorial", "light"], cover2("band")),
     ("var_bk_topleft", "Title Over The Photo", "Title set on the photo, top left.", ["visual", "bold", "story", "modern"], cover2("top")), "refine"),
    ("Textures & Materials", "Which Surface Feels Like Home?",
     ("var_tx_linen2", "Linen Curtain In Sun", "Light through a loose weave.", ["light", "soft", "natural", "calm"], texture2("linen")),
     ("var_tx_plaster2", "Plaster Wall With Shadow", "Matte mineral wall, slow shade.", ["warm", "quiet", "natural", "home"], texture2("plaster")), "check"),
    ("Lighting Moods", "Morning Light Or Evening Pendant?",
     ("var_lt_morning", "Morning Window Light", "Cool sky, warm patch on the floor.", ["light", "fresh", "natural", "clear"], light2("morning")),
     ("var_lt_pendant", "Evening Pendant", "One warm pool of light over the table.", ["warm", "cozy", "quiet", "home"], light2("evening")), "check"),
    ("Bags & Gear", "Which Weekend Bag?",
     ("var_bag_canvas", "Canvas Weekend Bag", "Light canvas, small lagoon stripe.", ["light", "practical", "casual", "fresh"], bag2("canvas")),
     ("var_bag_leather", "Leather Weekend Bag", "Warm brown leather.", ["warm", "classic", "natural", "rich"], bag2("leather")), "new"),
]
for cat, ask, a, b, purpose in VAR:
    add("Variety", cat, "Style Profile", ask, O(a[0], a[1], a[2], a[3], Vsvg(a[4])), O(b[0], b[1], b[2], b[3], Vsvg(b[4])),
        purpose=purpose, retest=(purpose == "retest"))

# ---- rule checks ----
import re
for p in pairs:
    for s in "AB": p["option" + s]["share"] = True; p["option" + s]["notes"] = True
    p["share"] = True; p["notes"] = True
uk_txt = re.sub(r"<[^>]+>", " ", json.dumps([p for p in pairs if p["group"] == "Up Keep"], ensure_ascii=False))
for bad in [r"Built by", r"By Max", r"Max Weberman", r"Health Score", r"Forecast", r"Danny", r"License #", r"Lic\.? ?#"]:
    m = re.search(bad, uk_txt, re.I); assert not m, (bad, uk_txt[max(0, m.start() - 60):m.end() + 60])
assert not re.search(r"\$\s?\d+(?!/Month)", uk_txt.replace(PRICE, "")), "stray Up Keep price"
all_txt = json.dumps(pairs, ensure_ascii=False)
emo = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2194-\u21FF]", all_txt); assert not emo, emo
assert "#0A0A0A\"" not in json.dumps([p["optionA"]["visual"].get("bg") for p in pairs])  # light backgrounds only

# ---- order: shuffle with no same group twice in a row ----
random.seed(1014)
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

alloc, groups, apps = {}, {}, {}
for p in order:
    alloc[p["category"]] = alloc.get(p["category"], 0) + 1
    groups[p["group"]] = groups.get(p["group"], 0) + 1
    apps[p["app"]] = apps.get(p["app"], 0) + 1
ids = [p["option" + s]["id"] for p in order for s in "AB"]
assert len(order) == DECK_SIZE, len(order)
assert len(ids) == len(set(ids)), "duplicate option id"
assert all(order[i]["group"] != order[i + 1]["group"] for i in range(49)), "same group twice in a row"
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
assert 10 <= groups["Up Keep"] <= 15
now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
deck = {
    "date": DID,
    "name": NAME,
    "version": 4,
    "owner": "Max Weberman",
    "format": "pairs",
    "english_only": True,
    "light_only": True,
    "status": "published",
    "notes": True,
    "share": True,
    "title": NAME + ": Blog Follow-Ups, Lagoon + Saffron Color, Up Keep Decisions, Home Guide, Variety, Swipe Controls",
    "brands": [
        "maxweberman.com base: Khand/Hind, light only, English only, capsule-pill buttons",
        "Micro-dose color: white base, lagoon + saffron pops, crisp black tags (no neon, no pastel, not all-beige)",
        "Smart UpKeep: no byline, no health score/forecast, 'Your Licensed Tech', only price 'Membership Starting at $99/Month'",
        "Home Guide is customer-facing: picks go to Construction, Max approves before publish",
    ],
    "generated_at": now,
    "builds_on": "Daily 2026-10-13 picks (32/50): refine winners, retest the 4 'both' ties, re-ask key skips; UpKeep open questions (tier names, price display, Text A Human, accent, payment, label capture, pause, stacking)",
    "sources": {"results": "results/2026-10-13.txt", "prior_deck": "decks/2026-10-13.json",
                "handoffs": ["/workspace/smartkeep/branding/daily-2026-10-13-picks.md", "/workspace/blog/branding/style-swipe-2026-10-13-picks.md", "/workspace/ops/construction/branding/home-guide-picks-2026-10-13.md"]},
    "allocation": alloc,
    "groups": groups,
    "apps": apps,
    "pair_mix": {
        "refine": sum(p["purpose"] == "refine" for p in order),
        "check": sum(p["purpose"] == "check" for p in order),
        "new": sum(p["purpose"] == "new" for p in order),
        "retest": sum(bool(p["retest"]) for p in order),
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
print("pair_mix", deck["pair_mix"])
print("apps", apps)
