"""Follow-on decks kit (Branding, Oct 17 2026, Max: 'if i swiped on anything today, make sure a new deck is built with the same type of content').
Full-card drawn mockups (uk5_art card frame: accent bar, label, Built by Machan) with team_kit blocks drawn at full scale (mockups fill the card),
SPLIT() for multi-view topics (two phone views side by side + a full-size detail strip), people/slides/charts from uk5_art.
All numbers are labeled example data or placeholders. Option = (key, label, desc, feel, svg)."""
import math
from draft_svg import t, rect, dot, ln, esc, ic, btn, tag, lbl, crisp, INK, MUTE, LINE, SOFT, TERRA, LAGOON, JUNGLE, SAFFRON
from team_kit import BLK, wrap, mono, photo, shareic
from uk5_art import card, chips, chip, slide, stitle, ssub, sfoot, phone, browser, line, bars, axes, kpi, spark, area, wordmark, mark, person, shot, zoom, icon, ex_tag, deck_strip, CREAM, GREY, DEEP, SKIN, HAIR, g
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
def at(blocks, y=30):
    s = ""
    for b in blocks:
        f = BLK[b[0]]; gg, h = f(y, *b[1:]); s += gg; y += h
    return s
def navbar(y, items, on=0, c=INK):
    n = len(items); w = 212 / n; s = ln(y) 
    for i, (nm, k) in enumerate(items):
        col = c if i == on else MUTE
        s += ic(k, 14 + i * w + w / 2 - 7, y + 5, 14, col, 1.8) + t(14 + i * w + w / 2, y + 28, nm, 7.5, col, "hind", 600, "middle")
    return s
MNAV = (("Home", "home"), ("Record", "tag"), ("Visits", "cal"), ("Profile", "star"))
TNAV = (("Today", "home"), ("Reports", "star"), ("Van", "tag"), ("Profile", "cal"))
def U(label, acc, blocks, y=30, foot=None, example=False, extra="", nav=None, nav_on=0):
    body = at(blocks, y) + extra
    if nav: body += navbar(246, nav, nav_on)
    if foot: body += chips(274, foot)
    return card(label, acc, body, example)
def mini(blocks, app="Smart Upkeep", sub="Member App", c=TERRA, nav=None, hstyle="logo"):
    s = rect(0, 0, 240, 300, "#FFFFFF") + at([("hdr", app, sub, c, hstyle, app[0])] + list(blocks), 0)
    if nav: s += navbar(258, nav)
    return s
def SPLIT(label, acc, L, R, la, lb, detail=None, foot=None, example=False, appL=("Smart Upkeep", "Member App"), appR=("Smart Upkeep", "Member App"), navL=None, navR=None, rawL=None, rawR=None):
    """Two phone views side by side (nothing hidden), captions, then an optional full-size detail strip (blocks) from y=206."""
    w = 100; sc = w / 240
    iL = rawL if rawL is not None else mini(L, *appL, nav=navL)
    iR = rawR if rawR is not None else mini(R, *appR, nav=navR)
    s = phone(18, 40, w, 300, iL, sc) + phone(122, 40, w, 300, iR, sc)
    s += t(68, 186, la, 9.5, INK, "khand", 700, "middle") + t(172, 186, lb, 9.5, INK, "khand", 700, "middle")
    if detail: s += at(detail, 196)
    if foot: s += chips(274, foot)
    return card(label, acc, s, example)
def opt(key, label, desc, feel, svg): return (key, label, desc, feel, svg)
def b_mh(y, app="Smart Upkeep", sub="", c=TERRA):
    s = rect(14, y, 212, 24, "#FFFFFF") + mark(26, y + 12, 6, "#FFFFFF", c) + t(36, y + 16, app, 10.5, INK, "khand", 700)
    if sub: s += t(36 + len(app) * 5.2 + 4, y + 16, sub, 7.5, MUTE)
    return s + shareic(208, y + 5.5) + ln(y + 24), 28
BLK["mh"] = b_mh
def b_tx(y, s, size=9, c=INK, f="khand", w=700): return t(14, y + size, s, size, c, f, w), size + 6
BLK["tx"] = b_tx
def b_row(y, k, v, c=INK):
    return t(14, y + 11, k, 8.5, INK, "hind", 500) + t(226, y + 11, v, 8, c, "hind", 600, "end") + ln(y + 17), 20
BLK["row"] = b_row
def S(label, acc, blocks, nav=None, on=0, sub="Member App", foot=None, example=False, extra=""):
    return U(label, acc, [("mh", "Smart Upkeep", sub)] + list(blocks), 30, foot, example, extra, nav, on)
