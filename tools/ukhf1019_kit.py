"""Shared drawing kit for the UpKeep board decks of Oct 19 2026 (Branding, Max via UpKeep Develop 12:02-12:07 ICT):
UpKeep Board Header Deck, UpKeep Board Footer Deck, Technicians Board Layout Deck, Tools And Equipment Board Deck.
Laptop-first drawn SVG mockups (1366-wide browser frame, drawn at 452 units), light only: white / warm cream base, thin terracotta,
lagoon and jungle accents, Khand + Hind, the Smart Upkeep 'UP' house mark redrawn as vector (roof chevron + UP).
Folds copy the kit dashboard fold-downs (mw-layout.css details.mw-bh-morning: cream summary bar, 1px line, Khand label, count, chevron).
PRIVACY: invented sample data only, every card tagged SAMPLE (or TEST / SAMPLE); no real names, addresses or phones."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
from mcd1019 import T, R, C, L, chev, chip, INK, MUTE, LINE, CREAM, WHITE, TERRA, LAGOON, JUNGLE, SOFT
from draft_svg import screen
SAFF = "#B7860B"; COAL = "#3F3A33"; RED = "#B42318"
HAZ = {"Gas": TERRA, "Electrical": SAFF, "CO": COAL, "Flooding": LAGOON}
def kw(s, size): return len(s) * size * .45          # Khand width estimate
def hw(s, size): return len(s) * size * .5           # Hind width estimate
def tagS(s="SAMPLE"):
    w = len(s) * 9 + 24
    return R(18, 14, w, 26, WHITE, "#B9AE9C", 4, 1.4, 'stroke-dasharray="4 3"') + T(18 + w / 2, 32, s, 13, MUTE, 700, "middle", extra='letter-spacing="1.5"')
def foot(s): return R(0, 556, 480, 44, WHITE) + L(0, 556, 480, 556, "#E8E0D2") + T(240, 584, s, min(18, 430 / (len(s) * .5)), INK, 600, "middle")
def frame(inner, note, url="members board", tag="SAMPLE"):
    s = R(14, 52, 452, 492, WHITE, "#D3CABB", 10, 1.4) + R(14, 52, 452, 22, SOFT, "none", 10) + R(14, 66, 452, 8, SOFT)
    s += "".join(C(28 + i * 11, 63, 3.2, "#CFC6B6") for i in range(3)) + R(70, 57, 240, 12, WHITE, LINE, 6) + T(78, 66.5, url + ".sample.test", 8, MUTE) + T(458, 66.5, "Laptop 1366 wide", 7.5, MUTE, 500, "end")
    s += f'<g transform="translate(14,74)">{inner}</g>'
    return screen(f'<g transform="scale(.5)">{R(0,0,480,600,CREAM)}{s}{tagS(tag)}{foot(note)}</g>', CREAM)
def mark(x, y, s, tile=True):
    g = R(x, y, s, s, CREAM, LINE, s * .12) if tile else ""
    g += f'<path d="M{x+s*.2:.1f} {y+s*.44:.1f} L{x+s*.5:.1f} {y+s*.18:.1f} L{x+s*.8:.1f} {y+s*.44:.1f}" fill="none" stroke="{TERRA}" stroke-width="{s*.08:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    return g + T(x + s * .5, y + s * .84, "UP", s * .46, "#1F1F1F", f="khand", anchor="middle")
def tri(y, x0=14, x1=438, h=2):
    w = (x1 - x0) / 3; return "".join(R(x0 + i * w, y, w, h, c) for i, c in enumerate((TERRA, LAGOON, JUNGLE)))
def share_ic(x, y, c=INK):
    return f'<path d="M{x+12} {y+5} v10 M{x+8.5} {y+8.5} l3.5 -3.5 l3.5 3.5 M{x+7} {y+12} v6 h10 v-6" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
def warn(x, y, c=TERRA, s=12):
    return f'<path d="M{x+s/2} {y} L{x+s} {y+s*.9} H{x} Z" fill="{c}22" stroke="{c}" stroke-width="1.3" stroke-linejoin="round"/>' + L(x + s / 2, y + s * .34, x + s / 2, y + s * .6, c, 1.4) + C(x + s / 2, y + s * .75, .9, c)
def check(x, y, done=False, c=JUNGLE, s=11):
    g = R(x, y, s, s, c if done else WHITE, c if done else "#B9AE9C", 2, 1.2)
    return g + (f'<path d="M{x+2.5} {y+s/2} l2.5 2.5 l4 -5" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-linecap="round"/>' if done else "")
def checkc(x, y, c=JUNGLE, r=7): return C(x, y, r, c + "1F", c, 1.2) + f'<path d="M{x-3} {y} l2 2.2 l4 -4.4" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
def docic(x, y, c=LAGOON, s=14):
    return f'<path d="M{x} {y} h{s*.62} l{s*.3} {s*.3} v{s*.82} h-{s*.92} z" fill="{WHITE}" stroke="{c}" stroke-width="1.2" stroke-linejoin="round"/>' + L(x + s * .2, y + s * .55, x + s * .72, y + s * .55, c, 1) + L(x + s * .2, y + s * .78, x + s * .6, y + s * .78, c, 1)
def lock(x, y, c=TERRA): return R(x, y + 5, 10, 8, c + "22", c, 1.5, 1.2) + f'<path d="M{x+2.2} {y+5} v-2 a2.8 2.8 0 0 1 5.6 0 v2" fill="none" stroke="{c}" stroke-width="1.2"/>'
def photo(x, y, w, h, c=JUNGLE):
    return R(x, y, w, h, SOFT, LINE, 3) + f'<path d="M{x+w*.15:.1f} {y+h*.85:.1f} l{w*.25:.1f} -{h*.4:.1f} l{w*.18:.1f} {h*.22:.1f} l{w*.14:.1f} -{h*.14:.1f} l{w*.13:.1f} {h*.32:.1f} z" fill="{c}55"/>' + C(x + w * .74, y + h * .3, min(w, h) * .09, TERRA + "77")
def fold(y, title, count=None, open_=False, body=0, right=None, rcol=MUTE, badge=None, x=14, w=424, h=24, size=13.5, bcol=TERRA, edge=None):
    g = R(x, y, w, h + body, WHITE, LINE) + R(x + .5, y + .5, w - 1, h - 1, CREAM)
    if edge: g += R(x, y, 3, h, edge)
    g += T(x + 10, y + h * .7, title, size, INK, f="khand"); tx = x + 10 + kw(title, size) + 5
    if count is not None: g += T(tx, y + h * .68, f"({count})", 9.5, MUTE, 500); tx += 22
    if badge is not None: g += C(tx + 4, y + h / 2, 7.5, bcol) + T(tx + 4, y + h / 2 + 3.3, str(badge), 9, WHITE, 700, "middle"); tx += 18
    if right: g += T(x + w - 26, y + h * .66, right, 9, rcol, 500, "end")
    g += chev(x + w - 13, y + h / 2, INK, True) if not open_ else f'<path d="M{x+w-17} {y+h/2+2} l4 -4 l4 4" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'
    if open_: g += L(x, y + h, x + w, y + h)
    return g
def lab_chip(x, y, s, style="soft", size=8):
    c = {"TEST": MUTE, "Forecast": LAGOON, "Decided": JUNGLE, "Open": SAFF}.get(s, MUTE)
    if style == "caps": w = len(s) * size * .68 + 10; return R(x, y, w, size + 7, WHITE, c, 2, 1) + T(x + w / 2, y + size + 1.5, s.upper(), size - .5, c, 700, "middle", extra='letter-spacing=".8"'), w
    return chip(x, y, s, c, "soft", size)
def bym(y=452, x=226, anchor="middle"):
    return L(14, y - 6, 438, y - 6, LINE) + T(x, y + 8, "Built by Machan", 9, MUTE, 500, anchor)
def stub(y, names=("Members Catalog", "Sign-ups And Renewals", "Member Messages"), stop=426):
    """Faded board sections under the header block, for context only."""
    if stop - y < 40: return ""
    g = L(14, y + 4, 438, y + 4, LINE, 1, 'stroke-dasharray="3 3"') + T(14, y + 18, "BOARD SECTIONS BELOW THE HEADER", 8, MUTE, 700, extra='letter-spacing="1.2"'); yy = y + 26; inner = ""
    for n in names:
        if yy + 24 > stop: break
        inner += fold(yy, n); yy += 30
    return g + f'<g opacity=".45">{inner}</g>'
def mini_header(title, y=0, share=True):
    g = mark(14, y + 6, 26) + T(48, y + 25, title, 16, INK, f="khand") + T(48 + kw(title, 16) + 8, y + 25, "SAMPLE", 8, MUTE, 700, extra='letter-spacing="1"')
    if share: g += R(414, y + 7, 24, 24, WHITE, INK, 0, 1.2) + share_ic(414, y + 7)
    return g + tri(y + 38), 44
def mini_folds(y, items):
    """Header blocks as a compact row of closed folds: (title, count, alert)."""
    w = (424 - 8 * (len(items) - 1)) / len(items); g = ""
    for i, (t_, n, b) in enumerate(items):
        g += fold(y, t_, None if b else n, False, x=14 + i * (w + 8), w=w, h=20, size=10.5, badge=n if b else None)
    return g, 26
