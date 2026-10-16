"""Card SVG shared with build_wn_business.py (copied so other boards render identically)."""
from draft_svg import t, rect
from team_kit import shareic, wrap
BG, INK, MUTE, LINE = "#FFFFFF", "#0A0A0A", "#525252", "#E5E0D8"
def svg(group, label, desc, facts, acc):
    s = rect(0, 0, 240, 300, BG) + rect(0, 0, 240, 5, acc)
    s += t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    y = 70
    for l in wrap(label, 15)[:3]: s += t(16, y, l, 28, INK, "khand"); y += 30
    y += 4; s += rect(16, y, 36, 3, acc, "none", 1.5); y += 22
    for l in wrap(desc, 28)[:3]: s += t(16, y, l, 14, MUTE); y += 18
    y = max(y + 6, 200)
    for f in facts[:2]:
        s += rect(16, y, 208, 32, "#FFFFFF", LINE, 8) + f'<circle cx="30" cy="{y+16}" r="4" fill="{acc}"/>' + t(42, y + 21, f, 13.5, INK, "hind", 600); y += 36
    s += t(120, 290, "Built by Max Weberman", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto"><clipPath id="c"><rect width="240" height="300" rx="14"/></clipPath><g clip-path="url(#c)">{s}</g><rect x=".5" y=".5" width="239" height="299" rx="14" fill="none" stroke="#D6D0C6"/></svg>'
