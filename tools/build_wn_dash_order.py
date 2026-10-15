#!/usr/bin/env python3
"""Rebuild WellNest 'Dashboard & Online' decks 1-2 IN PLACE (same deckIds + page slugs) for Max's new WellNest dashboard order
(Oct 14 2026 20:04 ICT), top to bottom: big header banner (newest site-plan render + logo), Swipe Decks, Dropbox upload link,
Open Projects, Team Chat. 20 pairs each. Locked WellNest brand in the mockups (nest logo, Cormorant + DM Sans, gold, peach, sand).
usage: build_wn_dash_order.py   (builds both). Submit -> agent 'wellnest'."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
sys.exit("Retired Oct 15 2026 (Max 12:45 ICT): WellNest decks carry no dashboard layout/structure questions. These decks are now built by tools/wn_fix_no_layout.py; see tools/wn_guard.py.")
from wn_series_kit import *
_ws = open(os.path.join(os.path.dirname(__file__), "build_wn_series.py")).read()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
_ns = {"os": os, "ROOT": ROOT}; exec(_ws[_ws.index("def page("):_ws.index("did = sys.argv[1]")], _ns); wn_page = _ns["page"]
OK = "#267D58"
def T(x, y, s, size=8, col=INK, fam=SANS, wt=400, a="start"): return tf(x, y, s, max(size, 7.5), col, fam, wt, a)
def render_art(x, y, w, h, style="plan", colour=True, labels=False, north=False, crop=False):
    g = GOLD if colour else "none"; gr = "#CFE3C4" if colour else "none"; st = "#7A6A4F"
    s = rect(x, y, w, h, "#F4EBD6" if colour else "#FFFFFF", SAND if not colour else "none", 0)
    sx, sy = (1.35, 1.35) if crop else (1, 1); cx, cy = x + w / 2, y + h / 2
    inner = ""
    if style == "plan":
        inner += rect(cx - 70, cy - 26, 52, 30, gr, st, 3) + rect(cx - 12, cy - 22, 30, 22, g, st, 3) + rect(cx + 24, cy - 26, 44, 18, "#E8C9A9" if colour else "none", st, 3)
        inner += f'<ellipse cx="{cx+42}" cy="{cy+14}" rx="18" ry="9" fill="{"#BFD9E6" if colour else "none"}" stroke="{st}"/>' + f'<path d="M{cx-80} {cy+20} Q{cx-20} {cy+6} {cx+20} {cy+22}" fill="none" stroke="{st}" stroke-dasharray="3 2"/>'
        inner += "".join(f'<circle cx="{cx-60+i*14}" cy="{cy+24}" r="4" fill="{"#8DB57A" if colour else "none"}" stroke="{st}"/>' for i in range(5))
        if labels: inner += T(cx - 66, cy - 8, "Tea Field", 7.5, INK, wt=600) + T(cx - 10, cy - 8, "Nest", 7.5, INK, wt=600) + T(cx + 27, cy - 14, "Sauna", 7.5, INK, wt=600)
    else:  # 3d bird's-eye
        for i, (dx, dy, ww, c) in enumerate([(-60, -6, 40, gr), (-14, -14, 34, g), (26, -4, 38, "#E8C9A9")]):
            c = c if colour else "none"
            inner += f'<path d="M{cx+dx} {cy+dy} l{ww/2} -10 l{ww/2} 10 l-{ww/2} 10 Z" fill="{c}" stroke="{st}"/><path d="M{cx+dx} {cy+dy} v12 l{ww/2} 10 v-12 M{cx+dx+ww} {cy+dy} v12 l-{ww/2} 10" fill="none" stroke="{st}"/>'
        inner += "".join(f'<circle cx="{cx-70+i*20}" cy="{cy+26}" r="5" fill="{"#8DB57A" if colour else "none"}" stroke="{st}"/>' for i in range(8))
    if crop: inner = f'<g transform="translate({cx},{cy}) scale({sx}) translate({-cx},{-cy})">{inner}</g>'
    s += f'<clipPath id="ra{int(x)}{int(y)}{int(w)}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#ra{int(x)}{int(y)}{int(w)})">{inner}</g>'
    if north: s += f'<path d="M{x+w-14} {y+16} l4 -9 l4 9 l-4 -3 Z" fill="{INK}"/>' + T(x + w - 10, y + 24, "N", 7.5, INK, a="middle") + rect(x + 8, y + h - 9, 30, 2, INK) + T(x + 42, y + h - 6, "20 m", 7.5, INK)
    return s
def banner(y, h=78, style="plan", logo_pos="tl", badge=True, title="over", cap=False, newpill=False, overlay=False, colour=True, labels=False, north=False, card=False, crop=False, border=False, bg="#FFFFFF", split=False):
    x, w = (12, 216) if card else (0, 240)
    s = rect(0, y, 240, h + (18 if title == "below" else 0), bg)
    if split:
        s += render_art(12, y + 4, 120, h - 8, style, colour, labels, north) + logo(160, y + 26, 30) + T(178, y + 30, "The", 9, INK, SER, 600) + T(140, y + 52, "WellNest", 15, INK, SER, 600)
        return s, h
    s += render_art(x, y, w, h, style, colour, labels, north, crop)
    if card or border: s += rect(x, y, w, h, "none", SAND, 8 if card else 0, 1.2)
    if overlay: s += f'<defs><linearGradient id="ov" x1="0" y1="0" x2="0" y2="1"><stop offset=".45" stop-color="{GOLD}" stop-opacity="0"/><stop offset="1" stop-color="{GOLD}" stop-opacity=".75"/></linearGradient></defs>' + rect(x, y, w, h, "url(#ov)")
    lx, ly = {"tl": (x + 22, y + 20), "c": (120, y + h / 2), "br": (x + w - 22, y + h - 20)}[logo_pos]
    if badge: s += f'<circle cx="{lx}" cy="{ly}" r="15" fill="#FFFFFF" stroke="{SAND}"/>'
    s += logo(lx, ly, 22)
    if title == "over": s += T(lx + 20 if logo_pos == "tl" else 120, ly + 4 if logo_pos == "tl" else y + h - 8, "The WellNest", 12, INK, SER, 600, "start" if logo_pos == "tl" else "middle")
    if title == "below": s += T(14, y + h + 13, "The WellNest", 12, INK, SER, 600)
    if cap: s += T(x + w - 6, y + h - 5, "Site plan, Oct 14 render", 7.5, INK, a="end")
    if newpill: s += rect(x + w - 62, y + 7, 54, 13, OK, r=6.5) + T(x + w - 35, y + 16.5, "New render", 7.5, "#FFFFFF", wt=600, a="middle")
    return s, h + (18 if title == "below" else 0)
def sec(y, s, serif=True): return T(14, y, s if serif else s.upper(), 11 if serif else 8, INK, SER if serif else SANS, 600)
def decks(y, n=2.5, thumb=False, tag=GOLD, cont="label", serif=True):
    s = sec(y + 10, "Swipe Decks", serif); w = 216 / n - 6
    for i in range(3):
        x = 12 + i * (w + 6); c = [GOLD, PEACH, OK][i]
        s += rect(x, y + 16, w, 46, "#FFFFFF", (OK if (i == 0 and cont == "outline") else SAND), 7, 1.4 if (i == 0 and cont == "outline") else 1)
        if thumb: s += render_art(x + 1, y + 17, w - 2, 16, "plan") + T(x + 6, y + 44, ["Brand Look", "Tea Line", "Tours"][i], 8, INK, wt=600)
        else: s += rect(x, y + 16, w, 3, c, r=1.5) + T(x + 6, y + 32, ["Brand Look", "Tea Line", "Tours"][i], 8.5, INK, wt=600)
        s += rect(x + 6, y + (48 if not thumb else 47), 30, 0, "none") + T(x + 6, y + 57, ("Continue" if i == 0 else "Start"), 7.5, OK, wt=600) if not thumb else T(x + 6, y + 57, ("Continue" if i == 0 else "Start"), 7.5, OK, wt=600)
        if not thumb: s += rect(x + w - 34, y + 36, 28, 11, (tag if i else tag) + "33", r=5.5) + T(x + w - 20, y + 44, ["Brand", "Tea", "Tours"][i], 7.5, INK, a="middle")
    return s, 66
def upload(y, style="button", words="Upload To Dropbox", last=False, icon="cloud"):
    ic = (f'<path d="M{24} {y+14} h10 a5 5 0 0 0 -2 -9 a6 6 0 0 0 -11 2 a4 4 0 0 0 3 7" fill="none" stroke="{INK if style!="button" else "#FFFFFF"}" stroke-width="1.4"/>' if icon == "cloud"
          else f'<path d="M{28} {y+5} v10 M{23} {y+10} h10" stroke="{INK if style!="button" else "#FFFFFF"}" stroke-width="1.6"/>')
    if style == "button": s = rect(12, y, 216, 22, GOLD, r=11) + ic + T(120, y + 14.5, words, 9, INK, wt=600, a="middle")
    else: s = rect(12, y, 216, 22, "#FFFFFF", SAND, 7) + ic + T(42, y + 14.5, words, 8.5, INK, wt=600) + T(218, y + 14.5, ">", 9, MUTE, a="end")
    h = 26
    if last: s += T(14, y + 32, "Last upload: 6 photos, today 14:20", 7.5, MUTE); h = 36
    return s, h
PROJ = [("Sauna House", "Roof framing", .6, "Build"), ("Tea Shop Shelf", "Pick wood", .3, "Shop"), ("Guest Signs", "Thai wording", .8, "Farm")]
def projects(y, style="cards", nxt=True, top3=True, thumb=False, group=False, serif=True):
    s = sec(y + 10, "Open Projects", serif) + (T(226, y + 10, "All 7", 8, OK, wt=600, a="end") if top3 else ""); yy = y + 16
    items = PROJ if top3 else PROJ + [("Pond Edge", "Stones", .2, "Farm")]
    if group: s += T(14, yy + 8, "BUILD", 7.5, MUTE, wt=600); yy += 10
    for i, (n, st, f, ar) in enumerate(items):
        if style == "cards":
            s += rect(12, yy, 216, 20, "#FFFFFF", SAND, 6) + (render_art(14, yy + 2, 24, 16, "plan") if thumb else "")
            tx = 44 if thumb else 20; s += T(tx, yy + 13, n, 8.5, INK, wt=600)
            s += (T(tx + 66, yy + 13, st, 7.5, MUTE) if nxt else rect(160, yy + 5, 40, 11, PEACH + "44", r=5.5) + T(180, yy + 13, "Open", 7.5, INK, a="middle"))
            s += rect(196 if nxt else 206, yy + 9, 26 if nxt else 16, 3, SAND, r=1.5) + rect(196 if nxt else 206, yy + 9, (26 if nxt else 16) * f, 3, OK, r=1.5); yy += 23
        else:
            s += T(20, yy + 10, n, 8.5, INK) + (T(220, yy + 10, st, 7.5, MUTE, a="end") if nxt else "") + f'<line x1="14" y1="{yy+15}" x2="226" y2="{yy+15}" stroke="{SAND}"/>'; yy += 16
        if group and i == 0: s += T(14, yy + 8, "SHOP AND FARM", 7.5, MUTE, wt=600); yy += 10
    return s, yy - y + 2
def chat(y, style="inline", inp=True, avatars=True, unread="dot", serif=True):
    s = sec(y + 10, "Team Chat", serif)
    s += (f'<circle cx="{88 if serif else 66}" cy="{y+6}" r="5" fill="{GOLD}"/>' + T(88 if serif else 66, y + 8.5, "2", 7.5, INK, wt=600, a="middle")) if unread == "dot" else T(80, y + 10, "2 new", 8, INK, wt=700)
    yy = y + 16
    if style == "inline":
        for i, (who, m) in enumerate([("Noi", "Roof sheets arrive Friday"), ("Max", "Great, photos please")]):
            x = 12 if i == 0 else 60
            if avatars: s += f'<circle cx="{x+7}" cy="{yy+8}" r="6" fill="{[PEACH, GOLD][i]}"/>' + T(x + 7, yy + 10.5, who[0], 7.5, INK, wt=700, a="middle")
            s += rect(x + (16 if avatars else 0), yy, 150, 16, "#FFFFFF" if i == 0 else GOLD + "33", SAND, 8) + T(x + (22 if avatars else 6), yy + 11, ("" if avatars else who + ": ") + m, 7.5, INK); yy += 19
        if inp: s += rect(12, yy + 2, 216, 16, "#FFFFFF", SAND, 8) + T(20, yy + 13, "Message the team", 7.5, MUTE); yy += 20
    else:
        s += rect(12, yy, 216, 22, "#FFFFFF", SAND, 11) + T(24, yy + 14.5, "Noi: Roof sheets arrive Friday", 8, INK) + T(218, yy + 14.5, "Open", 8, OK, wt=600, a="end"); yy += 26
    return s, yy - y
ORDER = ["banner", "decks", "upload", "projects", "chat"]
def page(label, desc, B={}, D={}, U={}, P={}, C={}, wide=None, gap=6, cards_gap=False, serif=True):
    s = rect(0, 0, 240, 300, RICE); y = 0
    for part in ORDER:
        if part == "banner": g, h = banner(y, **B)
        elif part == "decks": g, h = decks(y, serif=serif, **D)
        elif part == "upload": g, h = upload(y, **U)
        elif part == "projects": g, h = projects(y, serif=serif, **P)
        else: g, h = chat(y, serif=serif, **C)
        if y > 252: break
        s += (rect(6, y - 2, 228, h + 2, "#FFFFFF", SAND, 8) if cards_gap and part != "banner" else "") + g + (f'<line x1="12" y1="{y+h+gap/2}" x2="228" y2="{y+h+gap/2}" stroke="{SAND}"/>' if not cards_gap and part != "banner" and part != "chat" else "")
        y += h + gap + (4 if cards_gap else 0)
    s = f'<clipPath id="pg"><rect width="240" height="262"/></clipPath><g clip-path="url(#pg)">{s}</g>' + rect(0, 262, 240, 38, "#FFFFFF") + f'<line x1="0" y1="262" x2="240" y2="262" stroke="{SAND}"/>'
    s += T(120, 277, label, 10, INK, wt=600, a="middle") + T(120, 291, desc, 7.5, MUTE, a="middle")
    return scr(s, RICE)
def desk(label, desc, side):
    s = rect(0, 0, 240, 300, RICE) + rect(6, 30, 228, 150, "#1A1A1A", r=6) + rect(10, 34, 220, 138, "#FFFFFF", r=3)
    g, _ = banner(0, 40, crop=True); s += f'<g transform="translate(10,34) scale({220/240})">{g}</g>'
    if side:
        g1, _ = decks(0, n=3.2); g2, _ = upload(0, style="row")
        s += f'<g transform="translate(12,74) scale(.5)">{g1}</g><g transform="translate(122,80) scale(.45)">{g2}</g>'
        g3, _ = projects(0); s += f'<g transform="translate(12,112) scale(.5)">{g3}</g>'
    else:
        for i, f in enumerate([lambda: decks(0, n=4.5), lambda: upload(0, style="row"), lambda: projects(0)]):
            g, _ = f(); s += f'<g transform="translate(14,{74+i*30}) scale(.92,.42)">{g}</g>'
    s += rect(100, 180, 40, 12, "#1A1A1A") + rect(80, 192, 80, 4, "#1A1A1A", r=2) + T(120, 18, "On A Laptop", 11, INK, SER, 600, "middle")
    s += T(120, 236, label, 10, INK, wt=600, a="middle") + para(252, desc, 44, 7.5)
    return scr(s, RICE)
FEEL = ["calm", "visual", "focused", "quick", "action"]
def build(did, name, spec, about):
    pairs, O, add = deck(did.replace("wellnest-", "wn").replace("-", "")[:12] + "o_", "WellNest")
    for gi, (g, ask, a, b) in enumerate(spec):
        o = [O(f"{g.lower().replace(' ', '')[:10]}_{gi}_{k}", x[0], x[1], FEEL[(gi * 2 + k) % 5], x[2]) for k, x in enumerate((a, b))]
        add(g, g, o[0], o[1], ask)
    assert len(pairs) == 20, (did, len(pairs))
    cnt = {}
    for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
    publish(did, name, "WellNest", pairs, {"brands": [about, "Locked WellNest brand: original nest logo, Cormorant + DM Sans, gold leads, peach accent, sand lines; white deck background; drawn SVGs, sample content only"],
            "submit_agent": "wellnest", "submit_to": "WellNest Agent", "section_counts": cnt, "deck_size": 20, "series": {"category": "Dashboard & Online", "order": int(did[-1])},
            "rebuilt": "2026-10-14 20:04 ICT in place for Max's new WellNest dashboard order (banner, Swipe Decks, Dropbox upload, Open Projects, Team Chat)",
            "sources": {"queue": "/workspace/wellnest/deck-queue.json", "dashboard": "/workspace/wellnest/dashboard/index.html"}}, seed=2004 + int(did[-1]), n=20)
    dj = json.load(open(f"decks/{did}.json"))
    for p in dj["pairs"]:
        for k in ("optionA", "optionB"): p[k]["visual"]["bg"] = "#FFFFFF"
    json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    slug = json.load(open("queue/wn-series-slugs.json"))[did]; wn_page(did, slug); return slug
P_ = page
def thumbs(n, row, sq=False):
    lab = (f"{n} {'Square' if sq else 'Wide'} Thumbnails" if row else "All Renders Link")
    s = rect(0, 0, 240, 300, RICE); g, h = banner(0, 70); s += g; y = h + 4
    if row:
        w = (216 - (n - 1) * 5) / n; hh = w if sq else w * .5
        for i in range(n): s += render_art(12 + i * (w + 5), y, w, hh, ["plan", "3d"][i % 2]) + rect(12 + i * (w + 5), y, w, hh, "none", SAND, 4)
        s += T(14, y + hh + 10, "Older renders", 7.5, MUTE); y += hh + 16
    else: s += T(226, y + 8, "All renders (6) >", 8, OK, wt=600, a="end"); y += 14
    g, h = decks(y); s += g; y += h + 4; g, h = upload(y); s += g
    s = f'<clipPath id="pg"><rect width="240" height="262"/></clipPath><g clip-path="url(#pg)">{s}</g>' + rect(0, 262, 240, 38, "#FFFFFF") + f'<line x1="0" y1="262" x2="240" y2="262" stroke="{SAND}"/>'
    return scr(s + T(120, 280, lab, 10, INK, wt=600, a="middle"), RICE)
def tap(gallery):
    s = rect(0, 0, 240, 300, "#1A1A1A") + render_art(0, 70, 240, 130, "plan", labels=True) + T(226, 24, "Close", 9, "#FFFFFF", wt=600, a="end")
    if gallery: s += "".join(rect(84 + i * 12, 214, 7, 7, "#FFFFFF" if i == 0 else "#777777", r=3.5) for i in range(6)) + T(120, 50, "Render 1 of 6, Oct 14", 9, "#FFFFFF", a="middle")
    else: s += T(120, 50, "Newest render, pinch to zoom", 9, "#FFFFFF", a="middle")
    return scr(s + rect(0, 262, 240, 38, "#FFFFFF") + T(120, 280, "Render Gallery" if gallery else "Full-Screen Render", 10, INK, wt=600, a="middle"), "#1A1A1A")
def splitdesk(split):
    s = rect(0, 0, 240, 300, RICE) + rect(6, 30, 228, 150, "#1A1A1A", r=6) + rect(10, 34, 220, 138, "#FFFFFF", r=3)
    g, _ = banner(0, 64, split=split); s += f'<g transform="translate(10,34) scale({220/240})">{g}</g>'
    g, _ = decks(0, n=4.5); s += f'<g transform="translate(14,100) scale(.9)">{g}</g>'
    s += rect(100, 180, 40, 12, "#1A1A1A") + rect(80, 192, 80, 4, "#1A1A1A", r=2) + T(120, 18, "On A Laptop", 11, INK, SER, 600, "middle")
    return scr(s + T(120, 236, "Render Left, Logo Right" if split else "Full-Width Render", 10, INK, wt=600, a="middle"), RICE)
def Q2(g, ask, a, b):
    def fx(o):
        if not isinstance(o[2], dict): return o
        k = dict(o[2]); k.setdefault("B", {}); k["B"] = {"h": 36, "title": "over", **k["B"]}
        if g in ("Team Chat", "Sections"): k.setdefault("P", {}); k["P"] = {"style": "list", **k["P"]}; k.setdefault("D", {}); k["U"] = {**k.get("U", {})}
        return (o[0], o[1], k)
    return Q(g, ask, fx(a), fx(b))
def Q(g, ask, a, b): return (g, ask, (a[0], a[1], P_(a[0], a[1], **a[2])) if isinstance(a[2], dict) else a, (b[0], b[1], P_(b[0], b[1], **b[2])) if isinstance(b[2], dict) else b)
S1 = [
 Q("Render Style", "Header Render: Top-Down Site Plan Or Bird's-Eye 3D View?", ("Top-Down Site Plan", "Flat plan, every area in place", {"B": {"style": "plan"}}), ("Bird's-Eye 3D", "Buildings drawn in 3D from above", {"B": {"style": "3d"}})),
 Q("Render Style", "Render Colour: Soft Colour Fill Or Clean Line Drawing?", ("Soft Colour Fill", "Fields, roofs and pond in colour", {}), ("Clean Line Drawing", "Architect-style lines, no fill", {"B": {"colour": False}})),
 Q("Banner Size", "Header Banner: Tall Hero Or Short Strip?", ("Tall Hero", "Render fills the top of the phone", {"B": {"h": 120}}), ("Short Strip", "Thin banner, decks show sooner", {"B": {"h": 54}})),
 Q("Banner Size", "Render: Edge To Edge Or Inside A Rounded Card?", ("Edge To Edge", "Render runs to the screen edges", {}), ("Rounded Card", "Render sits in a card with margins", {"B": {"card": True}})),
 Q("Logo Placement", "Logo: Top Left Over The Render Or Centred On It?", ("Top Left", "Logo and name in the corner", {}), ("Centred", "Logo in the middle, name underneath", {"B": {"logo_pos": "c"}})),
 Q("Logo Placement", "Logo On The Render: White Circle Badge Or Plain?", ("White Circle Badge", "Logo sits on a small white circle", {}), ("Plain Logo", "Logo straight on the render", {"B": {"badge": False}})),
 Q("Logo Placement", "Name 'The WellNest': On The Render Or Below It?", ("On The Render", "Name beside the logo on the image", {}), ("Below The Render", "Clean image, name on the page under it", {"B": {"title": "below"}})),
 Q("Render Details", "Small Caption 'Site plan, Oct 14 render': Show Or Leave Off?", ("Show Caption", "Says which render this is", {"B": {"cap": True}}), ("No Caption", "Just the image", {})),
 Q("Render Details", "When A New Render Arrives: Green 'New render' Pill Or Nothing?", ("New Render Pill", "Pill until you have seen it", {"B": {"newpill": True}}), ("Nothing", "Banner just updates quietly", {})),
 Q("Render Details", "Site Plan: Area Names On The Plan Or Unlabelled?", ("Area Names", "Tea Field, Nest, Sauna written on it", {"B": {"labels": True, "h": 96}}), ("Unlabelled", "Picture only, no words", {"B": {"h": 96}})),
 Q("Render Details", "North Arrow And Scale Bar: Show Or Hide?", ("Show Them", "Small N arrow and 20 m bar", {"B": {"north": True}}), ("Hide Them", "Cleaner banner", {})),
 Q("Render Details", "Banner Overlay: Soft Gold Fade At The Bottom Or None?", ("Gold Fade", "Warm fade into the page", {"B": {"overlay": True}}), ("No Overlay", "Render shown as drawn", {})),
 ("Thumbnails", "Older Renders: Thumbnail Row Under The Banner Or Behind An 'All renders' Link?", ("Thumbnail Row", "3 small older renders under the banner", thumbs(3, True)), ("All Renders Link", "One small link opens the gallery", thumbs(0, False))),
 ("Thumbnails", "Render Thumbnails: Square Or Wide?", ("Square", "Small square crops", thumbs(4, True, sq=True)), ("Wide", "Wide crops, whole plan shows", thumbs(3, True))),
 ("Thumbnails", "How Many Older Renders: 3 Or 5?", ("Three", "Only the latest three", thumbs(3, True)), ("Five", "Five smaller thumbnails", thumbs(5, True))),
 ("Thumbnails", "Tap The Banner: Full-Screen Render Or Render Gallery?", ("Full-Screen Render", "Pinch to zoom the newest render", tap(False)), ("Render Gallery", "Swipe through every render", tap(True))),
 Q("Phone Crop", "On Phone: Crop To The Middle Of The Plan Or Show The Whole Plan?", ("Crop To Middle", "Bigger, edges cut off", {"B": {"crop": True}}), ("Whole Plan", "Everything fits, smaller", {})),
 Q("Frame", "Render Edge: Thin Sand Border Or No Border?", ("Thin Sand Border", "Fine line frames the render", {"B": {"border": True, "card": True}}), ("No Border", "Render meets the page", {"B": {"card": True}})),
 ("Big Screen", "On A Laptop: Render Left With Logo Right, Or Full-Width Render?", ("Render Left, Logo Right", "Split banner", splitdesk(True)), ("Full-Width Render", "Wide image across the top", splitdesk(False))),
 Q("Header Colour", "Behind The Name: Warm Rice Cream Or Plain White?", ("Warm Rice Cream", "Header strip in brand cream", {"B": {"title": "below", "bg": RICE_BRAND}}), ("Plain White", "Same white as the page", {"B": {"title": "below"}})),
]
S2 = [
 Q2("Swipe Decks", "Deck Cards: Small Render Thumbnail Or Colour Stripe Only?", ("Render Thumbnail", "Tiny picture on each deck", {"D": {"thumb": True}}), ("Colour Stripe Only", "Thin stripe, title and tag", {})),
 Q2("Swipe Decks", "Deck Tag Colour: Gold Or Peach?", ("Gold Tags", "Tags in soft gold", {}), ("Peach Tags", "Tags in soft peach", {"D": {"tag": PEACH}})),
 Q2("Swipe Decks", "Carousel On Phone: 2.5 Decks Visible Or 1.5 Bigger Decks?", ("2.5 Visible", "Smaller cards, more at once", {}), ("1.5 Bigger", "Bigger cards, one and a half", {"D": {"n": 1.5}})),
 Q2("Swipe Decks", "A Started Deck: Green Outline Or Just The 'Continue' Word?", ("Green Outline", "Started deck stands out", {"D": {"cont": "outline"}}), ("Continue Word Only", "Same card, label says Continue", {})),
 Q2("Upload Link", "Dropbox Upload: Big Gold Button Or Quiet Row With Arrow?", ("Big Gold Button", "Easy to spot and tap", {}), ("Quiet Row", "Same look as other rows", {"U": {"style": "row"}})),
 Q2("Upload Link", "Upload Wording: 'Upload To Dropbox' Or 'Add Photos And Files'?", ("Upload To Dropbox", "Says where files go", {}), ("Add Photos And Files", "Says what you do", {"U": {"words": "Add Photos And Files"}})),
 Q2("Upload Link", "Under The Upload Link: 'Last upload' Line Or Nothing?", ("Last Upload Line", "Shows when you last sent files", {"U": {"last": True}}), ("Nothing", "Just the link", {})),
 Q2("Upload Link", "Upload Icon: Cloud Or Plus?", ("Cloud", "Cloud outline", {"U": {"style": "row"}}), ("Plus", "Simple plus sign", {"U": {"style": "row", "icon": "plus"}})),
 Q2("Open Projects", "Open Projects: Cards With Progress Or A Simple List?", ("Cards With Progress", "Each project a card with a bar", {}), ("Simple List", "One line each", {"P": {"style": "list"}})),
 Q2("Open Projects", "Each Project: Next Step Written Or Just An Open Pill?", ("Next Step", "e.g. Roof framing", {}), ("Open Pill", "Status only", {"P": {"nxt": False}})),
 Q2("Open Projects", "How Many Projects: Top 3 With 'All 7' Or Every Project?", ("Top 3 + All Link", "Short section", {}), ("Every Project", "Longer, nothing hidden", {"P": {"top3": False}})),
 Q2("Open Projects", "Project Thumbnail: Small Render Crop Or None?", ("Small Render Crop", "Picture of where it is", {"P": {"thumb": True}}), ("None", "Words only", {})),
 Q2("Open Projects", "Group Projects By Area Or One List?", ("By Area", "Build, Shop and Farm headings", {"P": {"group": True}}), ("One List", "Newest first", {})),
 Q2("Team Chat", "Team Chat: Last Messages Shown Or One 'Open' Bar?", ("Last Messages", "See the latest two inline", {}), ("One Open Bar", "Latest line, tap to open", {"C": {"style": "bar"}})),
 Q2("Team Chat", "Message Box: Always Showing Or Tap To Open?", ("Always Showing", "Type right away", {}), ("Tap To Open", "Shorter section", {"C": {"inp": False}})),
 Q2("Team Chat", "Who Wrote It: Coloured Initial Circles Or Names Only?", ("Initial Circles", "N, M in small circles", {}), ("Names Only", "Noi: ...", {"C": {"avatars": False}})),
 Q2("Team Chat", "Unread Messages: Gold Count Dot Or '2 new' In Bold?", ("Gold Count Dot", "Small dot with the number", {}), ("2 New In Bold", "Words beside the title", {"C": {"unread": "text"}})),
 Q2("Sections", "Section Titles: Cormorant Serif Or Small DM Sans Capitals?", ("Cormorant Serif", "Matches the brand name", {}), ("DM Sans Capitals", "Small, spaced, quieter", {"serif": False})),
 Q2("Sections", "Between Sections: Thin Sand Lines Or Separate White Cards?", ("Thin Sand Lines", "One flowing page", {}), ("Separate Cards", "Each section in its own card", {"cards_gap": True})),
 ("Big Screen", "On A Laptop: Decks And Upload Side By Side, Or Everything Stacked?", ("Side By Side", "Uses the wide screen", desk("Side By Side", "Decks left, upload right", True)), ("Stacked", "Same order as the phone", desk("Stacked", "Same order as the phone", False))),
]
if __name__ == "__main__":
    out = {}
    out["wellnest-dashboard-online-1"] = build("wellnest-dashboard-online-1", "Dashboard: Header, Render And Logo", S1, "Header banner with the newest site-plan render + logo: render style, logo placement, thumbnails and render options (new dashboard order, Max 20:04)")
    out["wellnest-dashboard-online-2"] = build("wellnest-dashboard-online-2", "Dashboard: Decks, Upload, Projects And Chat", S2, "Swipe Decks carousel, Dropbox upload link, Open Projects and Team Chat (new dashboard order, Max 20:04)")
    print(json.dumps(out))
