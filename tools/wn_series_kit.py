"""Shared renderers for the WellNest 25-deck series (Oct 14 2026). Locked brand: nest logo, Cormorant + DM Sans, rice-white, gold leads, peach accent, sand lines."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
_src = open(os.path.join(os.path.dirname(__file__), "build_wellnest_brand.py")).read()
exec(_src[_src.index("FOREST, DEEP"):_src.index("# ---------- 1")])
_s2 = _src[_src.index("def pouch("):_src.index("TAG = ")]; exec(_s2)
_s3 = _src[_src.index("def ph("):_src.index("for a, b in [", _src.index("def ph("))]; exec(_s3)
CMG = "#B8902F"
RICE_BRAND = RICE; RICE = "#FFFFFF"   # Max Oct 14: deck backgrounds plain white
def W(s, n): return wrap(s, n)
def para(y, s, n=34, size=9, col=MUTE, lh=13, x=120, anchor="middle", fam=None):
    return "".join(tf(x, y + i * lh, l, size, col, fam or SANS, 400, anchor) for i, l in enumerate(W(s, n)[:4]))
def head2(y, s, size=20, n=20, col=INK):
    ls = W(s, n)[:3]; return "".join(tf(120, y + i * (size + 4), l, size, col, SER, 500) for i, l in enumerate(ls)), len(ls) * (size + 4)
def r_tag(label, desc, acc):
    s = rect(0, 0, 240, 300, RICE) + logo(120, 70, 90); h, hh = head2(160, label, 22, 18)
    s += h + f'<line x1="96" y1="{160+hh}" x2="144" y2="{160+hh}" stroke="{acc}" stroke-width="2"/>'
    s += para(180 + hh, desc, 36, 8.5)
    return scr(s, RICE)
def r_offer(label, desc, k, acc, btn="Learn More"):
    s = rect(0, 0, 240, 300, RICE) + rect(18, 20, 204, 128, "#FFFFFF", SAND, 12)
    s += f'<circle cx="120" cy="84" r="40" fill="none" stroke="{acc}" stroke-width="2"/>' + icon(k or "leaf", 96, 60, 48, acc, 1.5)
    h, hh = head2(178, label, 18, 22); s += h + para(184 + hh, desc, 38, 8.5)
    s += rect(80, 262, 80, 22, PEACH if acc != PEACH else GOLD, "none", 11) + tf(120, 277, btn, 8, "#FFFFFF" if acc != PEACH else INK, SANS, 600)
    return scr(s, RICE)
def r_quote(label, desc, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + tf(36, 70, "\u201C", 60, acc, SER, 400, "start")
    h, hh = head2(110, label, 19, 20); s += h + f'<line x1="100" y1="{112+hh}" x2="140" y2="{112+hh}" stroke="{SAND}" stroke-width="1.5"/>'
    s += para(132 + hh, desc, 36, 9, MUTE, 13, fam=SER) + logo(120, 262, 34)
    return scr(s, "#FFFFFF")
def r_ig(label, desc, k, acc):
    s = rect(0, 0, 240, 300, "#FFFFFF") + logo(26, 20, 22) + tf(42, 24, "thewellnest", 8.5, INK, SANS, 600, "start")
    s += rect(0, 36, 240, 170, acc + "2A") + icon(k or "leaf", 90, 90, 60, acc, 1.4)
    s += tf(12, 224, label, 11, INK, SANS, 600, "start") + para(240, desc, 44, 8.5, MUTE, 12, 12, "start")
    return scr(s, "#FFFFFF")
def r_web(label, desc, k, acc):
    s = rect(0, 0, 240, 300, RICE) + logo(22, 18, 20) + tf(36, 22, "The WellNest", 9, INK, SER, 600, "start")
    s += "".join(rect(150 + i * 22, 16, 14, 3, MUTE + "88", "none", 1.5) for i in range(3))
    s += rect(12, 38, 216, 110, acc + "30", "none", 10) + icon(k or "sun", 96, 66, 48, acc, 1.4)
    h, hh = head2(178, label, 18, 22); s += h + para(184 + hh, desc, 40, 8.5)
    s += rect(70, 262, 100, 22, GOLD, "none", 11) + tf(120, 277, "Plan Your Visit", 8, INK, SANS, 600)
    return scr(s, RICE)
def r_pal(label, desc, cols, btn=GOLD, txt=INK, btxt=None):
    s = rect(0, 0, 240, 300, RICE) + logo(120, 52, 64) + tf(120, 116, "Farm Life, Open To All", 17, txt, SER, 500)
    s += rect(66, 130, 108, 28, btn, "none", 14) + tf(120, 148, "Book A Farm Day", 8.5, btxt or ("#FFFFFF" if btn not in (GOLD, SAND, PEACH, RICE) else INK), SANS, 600)
    for i, c in enumerate(cols): s += rect(120 - len(cols) * 20 + i * 40 + 2, 176, 36, 36, c, SAND, 6)
    s += tf(120, 238, label, 11, INK, SANS, 600) + para(254, desc, 40, 8)
    return scr(s, RICE)
def avimg(k, cx, cy, d, tile=None, ring=None):
    s = ""
    if tile: s += rect(cx - d / 2, cy - d / 2, d, d, tile, SAND + "66", d * .22)
    if ring: s += f'<circle cx="{cx}" cy="{cy}" r="{d/2}" fill="none" stroke="{ring}" stroke-width="{max(1,d/30)}"/>'
    return s + f'<image href="img/wellnest-avatar/opt{k}.png" x="{cx-d/2}" y="{cy-d/2}" width="{d}" height="{d}" preserveAspectRatio="xMidYMid meet" style="mix-blend-mode:multiply"/>'
def r_av(label, desc, k, tile=None, bg=RICE, ring=None, mode="sizes"):
    s = rect(0, 0, 240, 300, bg)
    if mode == "profile":
        s += rect(0, 0, 240, 300, "#FFFFFF") + avimg(k, 50, 56, 64, tile, ring) + tf(96, 46, "thewellnest", 11, INK, SANS, 600, "start") + tf(96, 62, "Organic farm, San Sai", 8, MUTE, SANS, 400, "start")
        for i in range(9): s += rect(4 + (i % 3) * 78, 100 + (i // 3) * 62, 76, 60, [ROSELLE, FOREST, GOLD, PEACH, PEA, LEAF][i % 6] + "55")
    else:
        s += avimg(k, 120, 84, 110, tile, ring) + T_(label)
        for i, d in enumerate([48, 32, 20, 14]): s += avimg(k, 46 + i * 50, 248, d, tile, ring)
        s += tf(120, 286, desc, 7.5, MUTE)
        return scr(s, bg)
    s += tf(120, 288, desc, 7.5, MUTE)
    return scr(s, "#FFFFFF")
def T_(label): return tf(120, 170, label, 15, INK, SER, 600) + f'<line x1="24" y1="196" x2="216" y2="196" stroke="{SAND}"/>' + tf(24, 212, "SMALL SIZES", 6, MUTE, SANS, 600, "start", 'letter-spacing="1.2"')
def r_dash(label, desc, blocks, acc=GOLD, card="line", dense=False):
    s = rect(0, 0, 240, 300, RICE) + logo(24, 22, 24) + tf(42, 27, "The WellNest", 12, INK, SER, 600, "start") + f'<line x1="12" y1="42" x2="228" y2="42" stroke="{SAND}"/>'
    y = 52; hgt = 26 if dense else 36
    for b in blocks:
        if y > 240: break
        if card == "shadow": s += rect(14, y + 2, 212, hgt, "#00000010", "none", 8)
        s += rect(12, y, 216, hgt, "#FFFFFF" if card != "flat" else acc + "22", SAND if card == "line" else "none", 8)
        s += rect(12, y, 4, hgt, acc, "none", 2) + tf(24, y + hgt / 2 + 3, b, 9, INK, SANS, 500, "start") + tf(216, y + hgt / 2 + 3, ">", 9, MUTE, SANS, 400, "end")
        y += hgt + (5 if dense else 8)
    s += tf(120, 266, label, 11, INK, SANS, 600) + para(282, desc, 44, 7.5)
    return scr(s, RICE)
def r_ty(label, desc, sample, hs=26, hw=400, italic=False, caps=False, ls=0, body="Sun-dried roselle, picked by hand on our family farm in San Sai."):
    s = rect(0, 0, 240, 300, RICE)
    ex = (' font-style="italic"' if italic else "") + (f' letter-spacing="{ls}"' if ls else "")
    smp = sample.upper() if caps else sample
    for i, l in enumerate(W(smp, 16)[:3]): s += tf(120, 80 + i * (hs + 4), l, hs, INK, SER, hw, "middle", ex)
    s += para(180, body, 36, 9, MUTE, 14)
    s += tf(120, 252, label, 11, INK, SANS, 600) + para(268, desc, 40, 8)
    return scr(s, RICE)
