"""Art helpers for the Oct 17 evening follow-on decks (Job C, Branding): drawn mockups on the uk5/fu1017 card frame.
All numbers are labeled example data. Member App = terracotta, Tech App = lagoon (Max: 'Member orange tech blue')."""
from fu1017_kit import *
from uk5_art import shot as _shot
def member(label, acc, blocks, foot=None, example=True, extra=""):
    extra = f'<g transform="translate(0,16)">{extra}</g>' if extra else ""
    return S(label, acc, blocks, nav=MNAV, on=0, sub="Member App", foot=foot, example=example, extra=extra)
def tech(label, acc, blocks, foot=None, example=True, extra=""):
    extra = f'<g transform="translate(0,16)">{extra}</g>' if extra else ""
    return U(label, acc, [("mh", "Smart Upkeep", "Tech App", LAGOON)] + list(blocks), 30, foot, example, extra, TNAV, 0)
def site(label, acc, blocks, foot=None, example=False, extra=""):
    extra = f'<g transform="translate(0,16)">{extra}</g>' if extra else ""
    return U(label, acc, [("mh", "smartupkeep.ai", "", TERRA)] + list(blocks), 30, foot, example, extra)
def raw(label, acc, svg, example=False): return card(label, acc, svg, example)
def slidecard(label, acc, inner, cap="", example=True):
    s = slide(14, 74, 212, inner) + (t(120, 210, cap, 8.5, MUTE, "hind", 500, "middle") if cap else "")
    return card(label, acc, s, example)
def stx(x, y, s, size=12, c=INK, f="khand", w=700, a="start"): return t(x, y, s, size, c, f, w, a)
def sbars(x, y, vals, c=LAGOON, hi=None, w=14, gap=8, vmax=None):
    vmax = vmax or max(vals); s = ""
    for i, v in enumerate(vals):
        h = 80 * v / vmax; s += rect(x + i * (w + gap), y - h, w, h, (TERRA if i == hi else c))
    return s
def sline(x, y, w, h, vals, c=TERRA, sw=2.5, dash="", vmax=None):
    vmax = vmax or max(vals); pts = " ".join(f"{x + i * w / (len(vals) - 1):.1f},{y - h * v / vmax:.1f}" for i, v in enumerate(vals))
    return f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{sw}" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>'
def pie(cx, cy, r, parts):
    import math as m; s, a0 = "", -m.pi / 2; tot = sum(p for p, _ in parts)
    for p, c in parts:
        a1 = a0 + 2 * m.pi * p / tot; big = 1 if a1 - a0 > m.pi else 0
        s += f'<path d="M{cx} {cy} L{cx + r * m.cos(a0):.1f} {cy + r * m.sin(a0):.1f} A{r} {r} 0 {big} 1 {cx + r * m.cos(a1):.1f} {cy + r * m.sin(a1):.1f} Z" fill="{c}"/>'; a0 = a1
    return s
def crew(label, acc, people, example=False, cap=""):
    s = _shot(14, 32, 212, 236, people) + (t(120, 282, cap, 8, MUTE, "hind", 500, "middle") if cap else "")
    return card(label, acc, s, example)
def P(**k):
    base = dict(polo=TERRA, pants="#3D3A36", shoe="sneaker", logo="left"); base.update(k); return base
