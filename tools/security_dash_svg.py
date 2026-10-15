"""Security Dashboard Setup Deck card: label + mini dashboard mockup in the kit look (white, #FAF6EE / #e3ddd2, Khand/Hind, square corners)."""
from draft_svg import t, rect
from team_kit import shareic, wrap
INK, MUTE, CREAM, LINE, GREEN, AMBER, RED = "#0A0A0A", "#525252", "#FAF6EE", "#e3ddd2", "#2E7D4F", "#C98A12", "#B3402A"
def R(x, y, w, h, f=CREAM, s=LINE): return rect(x, y, w, h, f, s, 0)
def L(x, y, w, c="#cfc8bb"): return rect(x, y, w, 4, c, "none", 0)
def dot(x, y, c): return f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>'
def body(k, x, y, w, h):
    s = ""
    if k == "status":
        for i, c in enumerate((GREEN, GREEN, AMBER)): s += R(x + i * (w // 3), y, w // 3 - 4, 40) + dot(x + 10 + i * (w // 3), y + 12, c) + L(x + 6 + i * (w // 3), y + 26, 40)
        y += 46
    elif k == "alerts":
        s += R(x, y, w, 22, "#fbeee9", RED) + dot(x + 10, y + 11, RED) + L(x + 20, y + 9, 100, RED); y += 28
    elif k == "todo":
        for i in range(3): s += R(x, y, 10, 10, "#fff") + L(x + 16, y + 3, w - 40); y += 15
        y += 4
    elif k == "banner":
        s += R(x, y, w, 26, "#fbeee9", RED) + L(x + 8, y + 11, w - 60, RED); y += 32
    elif k == "cards":
        for i in range(3): s += R(x, y, w, 20) + dot(x + 10, y + 10, (RED, AMBER, AMBER)[i]) + L(x + 20, y + 8, w - 40); y += 24
    elif k == "lights":
        for i, c in enumerate((GREEN, AMBER, GREEN, RED)): s += dot(x + 6, y + 6, c) + L(x + 16, y + 4, w - 30); y += 14
    elif k == "areas":
        for a in ("PASSWORDS", "BACKUPS", "DEVICES"): s += R(x, y, w, 18) + t(x + 6, y + 13, a, 9, MUTE, "hind", 600) + t(x + w - 8, y + 13, "3/4", 9, INK, "hind", 600, "end"); y += 22
    elif k == "counts":
        for i, (n, lab) in enumerate((("2", "REUSED"), ("1", "WEAK"), ("0", "BREACHED"))): s += R(x + i * (w // 3), y, w // 3 - 4, 44) + t(x + 8 + i * (w // 3), y + 26, n, 22, INK, "khand") + t(x + 8 + i * (w // 3), y + 38, lab, 7, MUTE, "hind", 600)
        y += 50
    elif k == "bar":
        s += R(x, y, w, 14, "#fff") + rect(x, y, int(w * .7), 14, GREEN, "none", 0) + t(x, y + 28, "14 OF 20 ACCOUNTS", 9, MUTE, "hind", 600); y += 36
    elif k == "timeline":
        s += L(x, y + 14, w, LINE)
        for i, c in enumerate((RED, AMBER, GREEN, GREEN)): s += dot(x + 10 + i * (w - 20) // 3, y + 16, c) + L(x + i * (w - 20) // 3, y + 26, 24)
        y += 38
    elif k == "table":
        for i in range(4): s += R(x, y, w, 14, "#fff" if i % 2 else CREAM) + L(x + 6, y + 5, 60) + L(x + w - 50, y + 5, 40); y += 14
        y += 4
    elif k in ("carousel", "thumbs"):
        for i in range(3): s += R(x + i * 68, y, 60, 52) + L(x + i * 68 + 6, y + 40, 40)
        s += dot(x + w // 2 - 8, y + 62, INK) + dot(x + w // 2 + 4, y + 62, LINE); y += 70
    elif k == "page":
        s += R(x, y, w, 60, "#fff") + t(x + 8, y + 18, "WEEKLY REPORT", 11, INK, "khand")
        for i in range(3): s += L(x + 8, y + 28 + i * 9, w - 30)
        y += 66
    elif k == "list":
        for i in range(4): s += R(x, y, 16, 12) + L(x + 22, y + 4, w - 40); y += 16
    elif k == "fold":
        for i, o in enumerate((True, False, False)): s += R(x, y, w, 18) + L(x + 6, y + 7, 80) + t(x + w - 8, y + 13, "-" if o else "+", 11, INK, "hind", 600, "end"); y += 20 + (24 if o else 0)
    elif k == "open":
        for i in range(2): s += R(x, y, w, 40, "#fff") + L(x + 6, y + 8, 80, INK) + L(x + 6, y + 20, w - 20) + L(x + 6, y + 28, w - 40); y += 44
    elif k == "log":
        for i in range(4): s += t(x, y + 9, f"{9-i}:0{i} PM", 8, MUTE, "hind", 600) + L(x + 48, y + 5, w - 60); y += 14
    elif k == "family":
        for n in ("NOZOMI", "MAPLE", "MOM"): s += R(x, y, w, 18) + t(x + 6, y + 13, n, 9, INK, "hind", 600) + dot(x + w - 10, y + 9, GREEN if n != "MOM" else AMBER); y += 22
    elif k == "tabs":
        for i, n in enumerate(("ME", "FAMILY")): s += R(x + i * 60, y, 56, 16, INK if i else "#fff") + t(x + 28 + i * 60, y + 12, n, 8, "#fff" if i else INK, "hind", 600, "middle")
        y += 22
    elif k == "stack":
        for i in range(4): s += R(x + 30, y, w - 60, 16) + L(x + 36, y + 6, 60); y += 19
    elif k == "grid":
        for i in range(4): s += R(x + (i % 2) * (w // 2), y + (i // 2) * 30, w // 2 - 4, 26) + L(x + 6 + (i % 2) * (w // 2), y + 11 + (i // 2) * 30, 50)
        y += 62
    return s, y
def svg(group, label, desc, kinds, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, LINE)
    s += t(16, 26, group.upper(), 10.5, MUTE, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 13, INK, 15)
    y = 54
    for l in wrap(label, 18)[:2]: s += t(16, y, l, 24, INK, "khand"); y += 25
    for l in wrap(desc, 34)[:2]: s += t(16, y, l, 12, MUTE); y += 15
    y += 4; s += R(16, y, 208, 300 - y - 22, "#FFFFFF"); s += R(16, y, 208, 18, CREAM) + t(22, y + 13, "COMMAND CENTER", 10, INK, "khand", 600)
    yy = y + 24
    for k in kinds:
        b, yy = body(k, 22, yy, 196, 0); s += b; yy += 4
    s += t(120, 292, "Built by Max Weberman", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-height:100%;max-width:100%"><clipPath id="c"><rect width="240" height="300"/></clipPath><g clip-path="url(#c)">{s}</g><rect x=".5" y=".5" width="239" height="299" fill="none" stroke="{LINE}"/></svg>'
