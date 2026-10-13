"""Small SVG helpers shared by the thai-1 and jane-amex-1 draft deck builders (white base, Khand/Hind, 1-2 accent pops)."""
import json, datetime as dt, glob, os
INK = "#0A0A0A"; MUTE = "#525252"; LINE = "#E5E0D8"; SOFT = "#F5F3EF"; W, H = 240, 300
TERRA = "#C1502E"; LAGOON = "#05668D"; JUNGLE = "#0B6E4F"; SAFFRON = "#D4A017"
THAI = 'font-family="Noto Sans Thai Looped, Sarabun, Noto Sans Thai, sans-serif" font-weight="600"'
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def t(x, y, s, size=10, col=INK, f="hind", w=400, anchor="start", extra=""):
    fam = {"khand": 'font-family="Khand" font-weight="700"', "thai": THAI}.get(f, f'font-family="Hind" font-weight="{w}"')
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}" {fam} {extra}>{esc(s)}</text>'
def h1(x, y, s, size=18, col=INK, anchor="start"):
    maxw = 212 if anchor == "middle" else 226 - x; size = min(size, round(maxw / (max(len(s), 1) * .47), 1)); return t(x, y, s, size, col, "khand", anchor=anchor)
def lbl(x, y, s, col=MUTE, size=7, anchor="start"): return t(x, y, s.upper(), size, col, "hind", 600, anchor, 'letter-spacing="1"')
def rect(x, y, w, h, fill="none", stroke="none", r=0, sw=1, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def ln(y, x1=14, x2=226, c=LINE): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}"/>'
def dot(cx, cy, r, c): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
def btn(y, s, style="fill", col=INK, x=14, w=212, h=26, size=9):
    bg, fg = (col, "#FFFFFF") if style == "fill" else ("#FFFFFF", col)
    return rect(x, y, w, h, bg, col, 0, 1.5) + t(x + w / 2, y + h / 2 + size * .36, s.upper(), size, fg, "hind", 600, "middle", 'letter-spacing="1.2"')
def tag(x, y, s, col, solid=False, size=5.8):
    w = len(s) * size * .76 + 10
    return rect(x, y, w, size * 1.9, col if solid else col + "1F", "none", size) + t(x + w / 2, y + size * 1.38, s.upper(), size, "#FFFFFF" if solid else col, "hind", 600, "middle", 'letter-spacing=".6"')
def screen(body, bg="#FFFFFF"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="max-height:100%;max-width:100%">'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath><g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{bg}"/>' + body + f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#D6D0C6"/></svg>')
# small drawn icons (24-unit grid)
def ic(kind, x, y, s=16, c=INK, sw=1.8):
    P = {"speaker": f'<path d="M4 9 H8 L13 5 V19 L8 15 H4 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/><path d="M16 9 Q18 12 16 15 M18.5 6.5 Q22.5 12 18.5 17.5" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
         "slow": f'<path d="M3 16 Q4 9 11 9 Q17 9 18 16 Z" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="20" cy="13" r="2.2" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M6 16 v3 M15 16 v3" stroke="{c}" stroke-width="{sw}"/>',
         "check": f'<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M7 12.5 l3.5 3.5 6.5 -7" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
         "x": f'<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M8 8 L16 16 M16 8 L8 16" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
         "play": f'<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M10 8 L16 12 L10 16 Z" fill="{c}"/>',
         "cal": f'<rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M3 10 H21 M8 3 V7 M16 3 V7" stroke="{c}" stroke-width="{sw}"/>',
         "undo": f'<path d="M9 7 L4 12 L9 17" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 12 H15 Q20 12 20 17" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
         "heart": f'<path d="M12 20 L4 12 Q1 8 4.5 5 Q8 3 12 7 Q16 3 19.5 5 Q23 8 20 12 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
         "card": f'<rect x="2" y="5" width="20" height="14" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M2 10 H22" stroke="{c}" stroke-width="{sw}"/>',
         "phone": f'<rect x="6" y="2" width="12" height="20" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/><circle cx="12" cy="18" r="1" fill="{c}"/>',
         "tag": f'<path d="M3 12 V4 H11 L21 14 L13 22 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/><circle cx="7.5" cy="8.5" r="1.6" fill="{c}"/>',
         "clock": f'<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M12 6 V12 L16 14" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>',
         "chev": f'<path d="M9 5 L16 12 L9 19" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>',
         "down": f'<path d="M5 9 L12 16 L19 9" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>',
         "star": f'<path d="M12 3 L14.6 9 L21 9.5 L16 13.6 L17.6 20 L12 16.5 L6.4 20 L8 13.6 L3 9.5 L9.4 9 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
         "mic": f'<rect x="9" y="3" width="6" height="11" rx="3" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M5 11 Q5 18 12 18 Q19 18 19 11 M12 18 V21" fill="none" stroke="{c}" stroke-width="{sw}"/>',
         "home": f'<path d="M3 11 L12 4 L21 11 V20 H3 Z" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>',
         "search": f'<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="M15.5 15.5 L21 21" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>'}
    return f'<g transform="translate({x},{y}) scale({s/24})">{P[kind]}</g>'
def finish(did, title, app, pairs, first_fixed, extra_meta, seed=7):
    import random
    random.seed(seed); first = pairs[:first_fixed]; seq = pairs[first_fixed:]; random.shuffle(seq); order = list(first)
    while seq:
        k = next((i for i, p in enumerate(seq) if not order or p["group"] != order[-1]["group"]), 0); order.append(seq.pop(k))
    for i, p in enumerate(order, 1): p.update(id=f"{did}-{i:02d}", repeat=False)
    ids = [p["option" + s]["id"] for p in order for s in "AB"]
    assert len(order) == 50, len(order); assert len(ids) == len(set(ids)), "duplicate option id"
    ledger = json.load(open("shown_options.json")); shown = {k for k, v in ledger["options"].items() if v != [did]}
    for fp in glob.glob("decks/*.json"):
        if os.path.basename(fp) == f"{did}.json": continue
        for pp in json.load(open(fp)).get("pairs", []):
            for s in "AB":
                o = pp.get("option" + s) or {}
                if o.get("id"): shown.add(o["id"])
    rep = [i for i in ids if i in shown]; assert not rep, f"repeats: {rep}"
    groups, feel = {}, {}
    for p in order:
        groups[p["group"]] = groups.get(p["group"], 0) + 1
        for s in "AB": f = p["option" + s]["feeling"]; feel[f] = feel.get(f, 0) + 1
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    deck = {"date": did, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True, "title": title,
            "generated_at": now, "draft": True, "status": "draft-unpublished", "feeling_counts": feel, "groups": groups, "apps": {app: len(order)},
            "freshness": {"option_slots": len(ids), "never_shown_before": len(ids), "share": 1.0}, "warnings": [], **extra_meta, "pairs": order}
    json.dump(deck, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    opts = ledger["options"]
    for k in [k for k, v in opts.items() if v == [did]]: del opts[k]
    for i in ids: opts[i] = [did]
    ledger["options"] = dict(sorted(opts.items())); ledger["shown_count"] = len(opts); ledger["updated"] = now
    json.dump(ledger, open("shown_options.json", "w"), indent=1)
    print(did, len(order), "pairs", groups)
def mk(prefix, app):
    pairs = []
    def O(i, label, desc, tags, feel, svg): return {"id": prefix + i, "label": label, "desc": desc, "tags": tags + [feel], "feeling": feel, "notes": True, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": "#F7F4EF"}}
    def add(group, cat, a, b, ask, purpose="refine"): pairs.append({"group": group, "category": cat, "app": app, "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": False, "notes": True})
    return pairs, O, add
