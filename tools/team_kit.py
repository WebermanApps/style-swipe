"""Block-based drawn SVG mockup kit for the per-agent team decks (upkeep-7, prop-1, construction-1, scout-1, wellnest-1).
Built on draft_svg (white base, Khand/Hind, small accents #C1502E #05668D #0B6E4F #D4A017). Example data only.
A screen is a list of blocks stacked top to bottom; each block is a tuple (kind, *args)."""
import json, os, math
from draft_svg import *
from draft_svg import finish as _finish
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
def shareic(x, y, c=INK, s=13):
    return f'<g transform="translate({x},{y}) scale({s/24})"><path d="M12 3 V15 M7 8 L12 3 L17 8" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12 V20 H19 V12" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/></g>'
def mono(x, y, ch, c, s=22, fill=True):
    return (f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{s/2}" fill="{c if fill else "#FFFFFF"}" stroke="{c}" stroke-width="1.6"/>'
            + t(x + s / 2, y + s * .7, ch, s * .55, "#FFFFFF" if fill else c, "khand", anchor="middle"))
def photo(x, y, w, h, c=LAGOON, kind="house", r=6):
    s = rect(x, y, w, h, c + "1A", "none", r)
    if kind == "house":
        cx, b = x + w / 2, y + h * .82; hw = min(w, h) * .38
        s += f'<path d="M{cx-hw} {b} V{b-hw*.9} L{cx} {b-hw*1.6} L{cx+hw} {b-hw*.9} V{b} Z" fill="#FFFFFF" stroke="{c}" stroke-width="1.4" stroke-linejoin="round"/>' + rect(cx - hw * .2, b - hw * .6, hw * .4, hw * .6, c + "55")
    elif kind == "sun":
        s += f'<circle cx="{x+w*.72}" cy="{y+h*.3}" r="{min(w,h)*.12}" fill="{SAFFRON}88"/><path d="M{x} {y+h*.85} Q{x+w*.3} {y+h*.5} {x+w*.55} {y+h*.7} T{x+w} {y+h*.6} V{y+h} H{x} Z" fill="{c}55"/>'
    elif kind == "person":
        s += f'<circle cx="{x+w/2}" cy="{y+h*.4}" r="{min(w,h)*.17}" fill="{c}66"/><path d="M{x+w*.22} {y+h} Q{x+w/2} {y+h*.5} {x+w*.78} {y+h} Z" fill="{c}66"/>'
    elif kind == "leaf":
        s += f'<path d="M{x+w*.3} {y+h*.8} Q{x+w*.2} {y+h*.25} {x+w*.75} {y+h*.2} Q{x+w*.8} {y+h*.75} {x+w*.3} {y+h*.8} Z M{x+w*.3} {y+h*.8} L{x+w*.62} {y+h*.36}" fill="{c}44" stroke="{c}" stroke-width="1.2"/>'
    elif kind == "room":
        s += f'<path d="M{x} {y+h*.7} H{x+w} M{x+w*.3} {y} V{y+h*.7}" stroke="{c}66" stroke-width="1.2"/>' + rect(x + w * .45, y + h * .45, w * .35, h * .25, c + "44", "none", 3) + rect(x + w * .08, y + h * .2, w * .15, h * .3, "#FFFFFF", c + "88", 2)
    return s
def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n and cur: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    return lines + ([cur] if cur else [])

def render(blocks, bg="#FFFFFF"):
    """Stack blocks; returns full SVG screen."""
    s, y = "", 0
    for b in blocks:
        k, a = b[0], b[1:]
        g, h = BLK[k](y, *a); s += g; y += h
    return screen(s, bg)

def b_hdr(y, title, sub="", c=INK, style="plain", ch=None):
    ch = ch or title[0]
    if style == "band":
        return rect(0, y, W, 46, c) + mono(14, y + 12, ch, c, 22, False) + _ht(y, title, sub, "#FFFFFF", c, True), 52
    if style == "center":
        return t(120, y + 24, title, 15, INK, "khand", anchor="middle") + t(120, y + 35, sub, 6.5, MUTE, anchor="middle") + shareic(212, y + 12) + ln(y + 44), 50
    if style == "logo":
        return mono(14, y + 12, ch, c, 22) + _ht(y, title, sub, INK, c, False) + ln(y + 44), 50
    if style == "bar":
        return rect(0, y, W, 4, c) + _ht(y + 2, title, sub, INK, c, False, x=14) + ln(y + 46), 52
    return _ht(y, title, sub, INK, c, False, x=14) + ln(y + 44), 50
def _ht(y, title, sub, fg, c, band, x=42):
    s = t(x, y + 22, title, 13, fg, "khand") + (t(x, y + 33, sub, 6.5, "#FFFFFFCC" if band else MUTE) if sub else "")
    return s + shareic(208, y + 15, fg)
def b_gap(y, h=8): return "", h
def b_lbl(y, s, c=MUTE): return lbl(14, y + 10, s, c), 16
def b_h(y, s, size=18, c=INK, center=False):
    return h1(120 if center else 14, y + size, s, size, c, "middle" if center else "start"), size + 8
def b_p(y, s, n=46, c=MUTE, center=False):
    ls = wrap(s, n); return "".join(t(120 if center else 14, y + 9 + i * 10, l, 7.5, c, anchor="middle" if center else "start") for i, l in enumerate(ls)), len(ls) * 10 + 4
def b_card(y, title, sub="", c=TERRA, right="", mark="dot", h=34, edge="line"):
    s = rect(14, y, 212, h, "#FFFFFF" if edge != "tint" else c + "12", LINE if edge == "line" else "none", 7)
    if edge == "left": s += rect(14, y, 4, h, c, "none", 2)
    if mark == "dot": s += dot(26, y + h / 2, 3.5, c); x = 36
    elif mark == "none": x = 24
    elif mark.startswith("ic:"): s += rect(22, y + h / 2 - 10, 20, 20, c + "1F", "none", 5) + ic(mark[3:], 25, y + h / 2 - 7, 14, c, 2); x = 50
    else: s += mono(22, y + h / 2 - 9, mark, c, 18); x = 46
    s += t(x, y + h / 2 - (1 if sub else -3), title, 9.5, INK, "khand") + (t(x, y + h / 2 + 9, sub, 6.5, MUTE) if sub else "")
    if right.startswith("tag:"): s += _rtag(y + h / 2 - 5.5, right[4:], c)
    elif right: s += t(218, y + h / 2 + 3, right, 7.5, c, "hind", 600, "end")
    return s, h + 6
def _rtag(y, s, c):
    w = len(s) * 5.8 * .76 + 10; return tag(218 - w, y, s, c)
def b_cards(y, items, c=None, mark="dot", edge="line", h=34):
    s, hh = "", 0
    for i, it in enumerate(items):
        it = list(it) + [""] * (3 - len(it)); cc = c or ACC[i % 4]
        g, d = b_card(y + hh, it[0], it[1], cc, it[2], mark if mark != "num" else str(i + 1), h, edge); s += g; hh += d
    return s, hh
def b_btn(y, s, style="fill", c=INK, h=26):
    if style == "pill": return rect(14, y, 212, h, c, "none", h / 2) + t(120, y + h / 2 + 3.3, s.upper(), 9, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1.2"'), h + 8
    if style == "link": return t(120, y + 12, s.upper(), 8, c, "hind", 600, "middle", 'letter-spacing="1" text-decoration="underline"'), 20
    return btn(y, s, style, c, h=h), h + 8
def b_btn2(y, a, b, c=INK):
    return btn(y, a, "fill", c, 14, 103, 24, 7.5) + btn(y, b, "line", c, 123, 103, 24, 7.5), 32
def b_photo(y, h=90, c=LAGOON, kind="house", cap=""):
    s = photo(14, y, 212, h, c, kind)
    if cap: s += rect(14, y + h - 18, 212, 18, "#FFFFFFDD") + t(22, y + h - 6, cap, 7.5, INK, "hind", 600)
    return s, h + 8
def b_photos(y, n=3, h=56, kinds=None, cols=None):
    w = (212 - (n - 1) * 6) / n; kinds = kinds or ["house", "room", "sun", "leaf", "person"]
    return "".join(photo(14 + i * (w + 6), y, w, h, (cols or ACC)[i % 4], kinds[i % len(kinds)]) for i in range(n)), h + 8
def b_stats(y, items, style="box"):
    n = len(items); w = (212 - (n - 1) * 6) / n; s = ""
    for i, (v, l) in enumerate(items):
        x = 14 + i * (w + 6); c = ACC[i % 4]
        if style == "box": s += rect(x, y, w, 46, "#FFFFFF", LINE, 7) + t(x + 8, y + 26, v, 17, c, "khand") + t(x + 8, y + 38, l, 6.3, MUTE)
        elif style == "tint": s += rect(x, y, w, 46, c + "14", "none", 7) + t(x + w / 2, y + 26, v, 17, c, "khand", anchor="middle") + t(x + w / 2, y + 38, l, 6.3, INK, anchor="middle")
        else: s += t(x, y + 24, v, 22, INK, "khand") + rect(x, y + 30, 18, 2.5, c) + t(x, y + 42, l, 6.3, MUTE)
    return s, 54
def b_bars(y, vals, c=LAGOON, labels=None, h=60):
    n = len(vals); bw = 212 / n; s = ln(y + h, 14, 226)
    for i, v in enumerate(vals):
        s += rect(14 + i * bw + 3, y + h - h * v, bw - 6, h * v, c if i == n - 1 else c + "55", "none", 2)
        if labels: s += t(14 + i * bw + bw / 2, y + h + 9, labels[i], 6, MUTE, anchor="middle")
    return s, h + (16 if labels else 8)
def b_line(y, vals, c=JUNGLE, h=56):
    n = len(vals); pts = " ".join(f"{14+i*212/(n-1):.1f},{y+h-h*v:.1f}" for i, v in enumerate(vals))
    return rect(14, y, 212, h, SOFT, "none", 6) + f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>' + dot(226, y + h - h * vals[-1], 3, c), h + 8
def b_tiles(y, items, cols=2, h=64, style="line"):
    w = (212 - (cols - 1) * 8) / cols; s = ""; rows = math.ceil(len(items) / cols)
    for i, (n, k) in enumerate(items):
        x, yy = 14 + (i % cols) * (w + 8), y + (i // cols) * (h + 8); c = ACC[i % 4]
        if style == "solid": s += rect(x, yy, w, h, c, "none", 9) + ic(k, x + 10, yy + 10, 18, "#FFFFFF", 2.2) + t(x + 10, yy + h - 10, n, 10, "#FFFFFF", "khand")
        else: s += rect(x, yy, w, h, "#FFFFFF", LINE, 9) + rect(x + 10, yy + 10, 24, 24, c + "1F", "none", 6) + ic(k, x + 14, yy + 14, 16, c, 2.2) + t(x + 10, yy + h - 10, n, 10, INK, "khand")
    return s, rows * (h + 8)
def b_checks(y, items, c=JUNGLE, done=2):
    s = ""
    for i, it in enumerate(items):
        yy = y + i * 22; ok = i < done
        s += (rect(14, yy + 2, 12, 12, c, "none", 3) + f'<path d="M17 {yy+8} l2.5 2.5 4.5 -5" fill="none" stroke="#FFFFFF" stroke-width="1.8"/>' if ok else rect(14, yy + 2, 12, 12, "#FFFFFF", "#BDB6AA", 3, 1.2))
        s += t(34, yy + 11.5, it, 8.5, MUTE if ok else INK, "hind", 500) + ln(yy + 19, 34, 226)
    return s, len(items) * 22 + 6
def b_tags(y, items, solid=False):
    s, x, yy = "", 14, y
    for i, it in enumerate(items):
        w = len(it) * 5.8 * .76 + 10
        if x + w > 226: x, yy = 14, yy + 16
        s += tag(x, yy, it, ACC[i % 4], solid); x += w + 6
    return s, yy - y + 20
def b_dots(y, n=5, cur=1, c=INK):
    x0 = 120 - (n - 1) * 7; return "".join(f'<circle cx="{x0+i*14}" cy="{y+6}" r="3" fill="{c if i<=cur else "#D6D0C6"}"/>' for i in range(n)), 16
def b_steps(y, items, c=TERRA, cur=1):
    n = len(items); w = 212 / n; s = ln(y + 10, 14 + w / 2, 226 - w / 2, "#D6D0C6")
    for i, it in enumerate(items):
        cx = 14 + w * i + w / 2; on = i <= cur
        s += f'<circle cx="{cx}" cy="{y+10}" r="7" fill="{c if on else "#FFFFFF"}" stroke="{c if on else "#BDB6AA"}" stroke-width="1.4"/>' + t(cx, y + 13, str(i + 1), 7, "#FFFFFF" if on else MUTE, "hind", 700, "middle") + t(cx, y + 28, it, 6.3, INK if on else MUTE, "hind", 600, "middle")
    return s, 36
def b_bar(y, frac, c=JUNGLE, label="", right=""):
    s = (t(14, y + 8, label, 7.5, INK, "hind", 600) if label else "") + (t(226, y + 8, right, 7.5, c, "hind", 600, "end") if right else "")
    o = 13 if (label or right) else 0
    return s + rect(14, y + o, 212, 6, "#EEEAE4", "none", 3) + rect(14, y + o, 212 * frac, 6, c, "none", 3), o + 14
def b_ring(y, frac, c=JUNGLE, big="", sub=""):
    cx, cy, r = 120, y + 42, 34; a = 2 * math.pi * frac; x2, y2 = cx + r * math.sin(a), cy - r * math.cos(a)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEAE4" stroke-width="7"/><path d="M{cx} {cy-r} A{r} {r} 0 {1 if frac>.5 else 0} 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
            + t(cx, cy + 6, big, 20, INK, "khand", anchor="middle") + t(cx, cy + 16, sub, 6.3, MUTE, anchor="middle")), 92
def b_table(y, rows, zebra=False):
    s = ""
    for i, (k, v) in enumerate(rows):
        yy = y + i * 18
        if zebra and i % 2 == 0: s += rect(14, yy, 212, 18, SOFT)
        s += t(20, yy + 12, k, 7.8, MUTE) + t(220, yy + 12, v, 7.8, INK, "hind", 600, "end") + ("" if zebra else ln(yy + 18))
    return s, len(rows) * 18 + 8
def b_input(y, ph, c=TERRA, k="mic"):
    return rect(14, y, 212, 28, "#FFFFFF", INK, 6, 1.2) + ic(k, 22, y + 6, 16, c, 2) + t(44, y + 18, ph, 8, "#9A948A"), 36
def b_toggles(y, items):
    s = ""
    for i, (n, on) in enumerate(items):
        yy = y + i * 26; c = JUNGLE if on else "#D6D0C6"
        s += t(14, yy + 15, n, 8.5, INK, "hind", 500) + rect(196, yy + 5, 28, 15, c, "none", 7.5) + dot(196 + (20 if on else 8), yy + 12.5, 5.5, "#FFFFFF") + ln(yy + 24)
    return s, len(items) * 26 + 4
def b_timeline(y, items):
    s = f'<line x1="22" y1="{y+6}" x2="22" y2="{y+len(items)*30-12}" stroke="#D6D0C6" stroke-width="1.5"/>'
    for i, (a, b) in enumerate(items):
        yy = y + i * 30; s += dot(22, yy + 8, 4.5, ACC[i % 4]) + t(34, yy + 11, a, 9, INK, "khand") + t(34, yy + 21, b, 6.5, MUTE)
    return s, len(items) * 30 + 2
def b_bubble(y, s, me=False, c=LAGOON):
    ls = wrap(s, 34); h = len(ls) * 10 + 10; w = max(len(l) for l in ls) * 4.2 + 18; x = 226 - w if me else 14
    return rect(x, y, w, h, c if me else SOFT, "none", 9) + "".join(t(x + 9, y + 13 + i * 10, l, 7.5, "#FFFFFF" if me else INK) for i, l in enumerate(ls)), h + 6
def b_banner(y, s, c=SAFFRON, k="clock"):
    return rect(14, y, 212, 26, c + "1A", "none", 6) + rect(14, y, 3, 26, c) + ic(k, 22, y + 6, 14, c, 2) + t(42, y + 16.5, s, 8, INK, "hind", 600), 32
def b_swatch(y, cols, names=None):
    n = len(cols); w = (212 - (n - 1) * 6) / n
    return "".join(rect(14 + i * (w + 6), y, w, 40, c, LINE if c.upper() in ("#FFFFFF", "#F7F4EF", "#F5F3EF") else "none", 6) + (t(14 + i * (w + 6), y + 50, names[i], 6.3, MUTE) if names else "") for i, c in enumerate(cols)), 58 if names else 48
def b_word(y, s, size=26, c=INK, sub="", center=True, f="khand", spacing=0):
    x = 120 if center else 14; a = "middle" if center else "start"
    s1 = t(x, y + size, s, size, c, f, 700, a, f'letter-spacing="{spacing}"' if spacing else "")
    return s1 + (lbl(x, y + size + 14, sub, MUTE, 6.5, a) if sub else ""), size + (24 if sub else 10)
def b_thumb(y, text, c=TERRA, style="block", kind="person"):
    x, w, h = 66, 108, 150; s = photo(x, y, w, h, LAGOON, kind, 8)
    ls = wrap(text, 11)
    if style == "block": s += "".join(rect(x + 8, y + 90 + i * 20, len(l) * 7.2 + 8, 18, c) + t(x + 12, y + 104 + i * 20, l.upper(), 13, "#FFFFFF", "khand") for i, l in enumerate(ls))
    elif style == "outline": s += "".join(t(x + w / 2, y + 30 + i * 18, l.upper(), 16, "#FFFFFF", "khand", anchor="middle", extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"') for i, l in enumerate(ls))
    elif style == "bottom": s += rect(x, y + h - 44, w, 44, "#FFFFFFEE") + "".join(t(x + 8, y + h - 28 + i * 14, l, 12, INK, "khand") for i, l in enumerate(ls[:2]))
    elif style == "none": pass
    else: s += "".join(t(x + 8, y + 22 + i * 16, l.upper(), 14, c, "khand", extra='stroke="#FFFFFF" stroke-width="2.5" paint-order="stroke"') for i, l in enumerate(ls))
    return s + rect(x, y, w, h, "none", "#D6D0C6", 8), h + 8
def b_tabs(y, names, style="pill"):
    n = len(names); w = 212 / n; s = ""
    if style == "pill": s += rect(14, y, 212, 22, SOFT, "none", 11) + rect(16, y + 2, w - 4, 18, "#FFFFFF", LINE, 9)
    else: s += ln(y + 22) + rect(22, y + 20, w - 16, 2.5, TERRA)
    return s + "".join(t(14 + w * i + w / 2, y + 14.5, nm, 8, INK if i == 0 else MUTE, "khand", anchor="middle") for i, nm in enumerate(names)), 30
def b_map(y, h=90):
    s = rect(14, y, 212, h, SOFT, "none", 8) + "".join(f'<line x1="{14+i*42}" y1="{y}" x2="{14+i*42+20}" y2="{y+h}" stroke="#E5E0D8" stroke-width="5"/>' for i in range(1, 5))
    s += f'<path d="M30 {y+h-16} Q90 {y+20} 150 {y+h*.55} T210 {y+18}" fill="none" stroke="{LAGOON}" stroke-width="2.5" stroke-dasharray="5 3"/>'
    return s + dot(30, y + h - 16, 5, TERRA) + dot(210, y + 18, 5, JUNGLE), h + 8
def b_sheet(y, title, rows, c=INK):
    s = rect(0, y, W, H - y, "#0A0A0A33") + rect(0, y + 20, W, H - y, "#FFFFFF", "none", 14) + rect(104, y + 28, 32, 4, "#D6D0C6", "none", 2) + t(14, y + 52, title, 13, INK, "khand")
    g, h = b_checks(y + 62, rows, JUNGLE, 0); return s + g, H - y
def b_raw(y, svg, h): return svg, h
def b_cal(y, marks=(3, 9, 16, 23), c=TERRA):
    s = "".join(t(14 + i * 30.3 + 15, y + 8, d, 6, MUTE, "hind", 600, "middle") for i, d in enumerate("MTWTFSS"))
    for d in range(28):
        x, yy = 14 + (d % 7) * 30.3, y + 14 + (d // 7) * 20
        on = d + 1 in marks; s += (rect(x + 5, yy, 20, 16, c, "none", 4) if on else "") + t(x + 15, yy + 11, str(d + 1), 7, "#FFFFFF" if on else INK, "hind", 600, "middle")
    return s, 100
def b_nav(y, items=(("Home", "home"), ("Visits", "cal"), ("Notes", "star"), ("Share", "tag"))):
    yy = H - 40; s = ln(yy) + "".join(ic(k, 14 + i * 53 + 18, yy + 6, 15, INK if i == 0 else MUTE, 1.8) + t(14 + i * 53 + 26, yy + 31, n, 6, INK if i == 0 else MUTE, "hind", 600, "middle") for i, (n, k) in enumerate(items))
    return s, 0
BLK = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}

def deck(prefix, app):
    pairs = []
    def O(i, label, desc, feel, blocks, tags=()):
        svg = blocks if isinstance(blocks, str) else render(blocks)
        return {"id": prefix + i, "label": label, "desc": desc, "tags": list(dict.fromkeys(list(tags) + [feel])), "feeling": feel, "notes": True, "share": True,
                "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": "#FFFFFF"}}
    def add(group, cat, a, b, ask, purpose="new"):
        pairs.append({"group": group, "category": cat, "app": app, "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": False, "notes": True, "share": True})
    return pairs, O, add
def publish(did, title, app, pairs, meta, seed, n=None, first=0):
    _finish(did, title, app, pairs, first, meta, seed=seed, n=n)  # first = carried pairs kept at the front  # n overrides the 25-pair trim (only when Max asks for a bigger deck)
    d = json.load(open(f"decks/{did}.json")); d.pop("draft", None); d["status"] = "published"; d["share"] = True; d["notes"] = True
    for pp in d["pairs"]: pp["notes"] = True; pp["share"] = True
    txt = json.dumps(d, ensure_ascii=False)
    import re
    bad = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", txt); assert not bad, bad
    json.dump(d, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    try:
        from write_sizes import main as write_sizes
        write_sizes()
    except Exception as e:
        print("write_sizes:", e)
