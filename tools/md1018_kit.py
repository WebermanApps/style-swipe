"""Morning decks Oct 18 2026 (Branding): shared drawn-mockup helpers + publish/page writer for build_morning_decks_1018.py.
Light only: white base, warm cream bands (#FAF6EE), terracotta / lagoon / jungle accents (saffron sparingly), Khand + Hind. Example data only;
money figures are always labelled SAMPLE placeholders (never real or invented financials). No Thai references in UpKeep items (R110)."""
import json, os, re, string, secrets
from draft_svg import t, rect, ln, dot, screen, esc, ic, tag, INK, MUTE, LINE, SOFT, TERRA, LAGOON, JUNGLE, SAFFRON, W, H
from team_kit import BLK, deck, publish, wrap, photo, shareic, mono, ACC
import caption_rule
from split_deck import theme_name_ok
CREAM = "#FAF6EE"; ORANGE = "#D9772B"; FAINT = "#9A948A"
def chip(x, y, s, c, solid=False, size=7.5):
    w = len(s) * size * .55 + 12
    return rect(x, y, w, size * 2, c if solid else c + "1A", "none" if solid else c + "66", 6, 1) + t(x + w / 2, y + size * 1.4, s, size, "#FFFFFF" if solid else c, "hind", 600, "middle"), w
def S(label, blocks, note=None, right="", bg="#FFFFFF"):
    """One drawn phone screen: cream label band, stacked team_kit blocks, optional terracotta note at the bottom."""
    s = rect(0, 0, W, 26, CREAM) + t(12, 17, label.upper(), 7.5, INK, "hind", 700, extra='letter-spacing="1"') + (t(228, 17, right, 7.5, MUTE, anchor="end") if right else "") + ln(26, 0, W, LINE)
    y = 34
    for b in blocks:
        g, h = BLK[b[0]](y, *b[1:]); s += g; y += h
    if note:
        yn = max(y + 14, 262)
        s += rect(12, yn - 10, 3, 24, TERRA) + t(20, yn, note[0], 8.5, INK, "hind", 600) + (t(20, yn + 12, note[1], 7.8, MUTE) if len(note) > 1 else "")
    return screen(s, bg)
# ---- extra blocks (registered into team_kit BLK so S() can use them) ----
def b_carousel(y, cards, w=150, h=70, dots=True, auto=False, cur=0, peek=True, counter=None, arrows=False, kind=None):
    """Swipe carousel: first card at the margin, next one peeking at the right edge."""
    s = ""
    for i, cd in enumerate(cards[:3]):
        x = 14 + i * (w + 8)
        if x > 240: break
        cd = list(cd); title = cd[0]; sub = cd[1] if len(cd) > 1 else ""; c = cd[2] if len(cd) > 2 else ACC[i % 4]
        s += rect(x, y, w, h, "#FFFFFF", LINE, 10) + rect(x, y, w, 4, c, "none", 2)
        if kind == "photo": s += photo(x + 8, y + 10, w - 16, h - 34, c, ["house", "room", "sun", "leaf"][i % 4])
        s += t(x + 10, y + h - 18 if kind == "photo" else y + 24, title, 9.5, INK, "khand") + (t(x + 10, y + h - 7 if kind == "photo" else y + 37, sub, 7.5, MUTE) if sub else "")
    hh = h + 6
    if arrows:
        s += f'<circle cx="222" cy="{y+h/2}" r="10" fill="#FFFFFF" stroke="{TERRA}" stroke-width="1.3"/>' + ic("chev", 215, y + h / 2 - 7, 14, TERRA, 2)
    if dots:
        n = len(cards); x0 = 120 - (n - 1) * 6
        s += "".join(rect(x0 + i * 12 - (5 if i == cur else 2.5), y + hh + 2, 10 if i == cur else 5, 5, TERRA if i == cur else "#D6D0C6", "none", 2.5) for i in range(n)); hh += 14
    if counter: s += t(226, y + hh + 6, counter, 7.5, MUTE, "hind", 600, "end"); hh += 12
    if auto:
        s += f'<path d="M20 {y+hh+5} a5 5 0 1 1 1.5 3.6" fill="none" stroke="{LAGOON}" stroke-width="1.4"/>' + t(30, y + hh + 9, "Loops on its own", 7.5, LAGOON, "hind", 600); hh += 14
    return s, hh + 4
def b_pills(y, items, cols=None, fade=False, size=7.5, gap=6, x0=14):
    """One row of pill tags that runs off the edge (a looping strip) with optional soft edge fade."""
    s, x = "", x0
    for i, it in enumerate(items):
        c = (cols or [INK])[i % len(cols or [INK])]
        g, w = chip(x, y, it, c, False, size); s += g; x += w + gap
    if fade:
        s += (f'<defs><linearGradient id="fl{y}" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
              f'<linearGradient id="fr{y}" x1="1" x2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient></defs>'
              f'<rect x="0" y="{y-2}" width="22" height="{size*2+4}" fill="url(#fl{y})"/><rect x="218" y="{y-2}" width="22" height="{size*2+4}" fill="url(#fr{y})"/>')
    return s, size * 2 + 8
def b_note(y, a, b="", c=TERRA):
    return rect(14, y, 212, 34 if b else 22, CREAM, "none", 6) + rect(14, y, 3, 34 if b else 22, c) + t(22, y + 14, a, 8.5, INK, "hind", 600) + (t(22, y + 26, b, 7.5, MUTE) if b else ""), (40 if b else 28)
def b_kv(y, rows, c=INK):
    s = ""
    for i, (k, v, *cc) in enumerate(rows):
        yy = y + i * 20; col = cc[0] if cc else c
        s += t(14, yy + 13, k, 8.5, INK, "hind", 500) + t(226, yy + 13, v, 8.5, col, "hind", 700, "end") + ln(yy + 19)
    return s, len(rows) * 20 + 6
def b_reading(y, val, word, c, sub=""):
    s = rect(14, y, 120, 34, "#FFFFFF", c, 6, 1.4) + t(24, y + 23, val, 15, INK, "khand") + t(124, y + 22, "%", 9, MUTE, "hind", 600, "end")
    g, w = chip(142, y + 9, word, c, True, 8); s += g
    if sub: s += t(14, y + 46, sub, 7.5, MUTE)
    return s, 52 if sub else 42
def b_desk(y, inner, h=150):
    """A small desktop browser frame (1280 wide) with inner blocks scaled down."""
    s = rect(10, y, 220, h, "#FFFFFF", "#D6D0C6", 6) + rect(10, y, 220, 12, SOFT, "none", 6) + "".join(dot(18 + i * 7, y + 6, 2, "#C9C2B6") for i in range(3))
    return s + f'<g transform="translate(14,{y+16})">{inner}</g>', h + 8
def b_scale(y, frac, labels=("Dry", "Watch", "Wet"), cols=(JUNGLE, SAFFRON, TERRA)):
    s = ""; w = 212 / 3
    for i in range(3): s += rect(14 + i * w, y, w - 2, 8, cols[i] + "55", "none", 2) + t(14 + i * w + w / 2, y + 20, labels[i], 7.5, cols[i], "hind", 600, "middle")
    s += f'<path d="M{14+212*frac-5} {y-6} h10 l-5 6 z" fill="{INK}"/>'
    return s, 28
def b_gauge(y, frac, label="", c=TERRA):
    import math
    cx, cy, r = 120, y + 50, 40; a = math.pi * (1 - frac); x2, y2 = cx + r * math.cos(a), cy - r * math.sin(a)
    s = f'<path d="M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="#EEEAE4" stroke-width="9"/><path d="M{cx-r} {cy} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{c}" stroke-width="9"/>'
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx+(r-14)*math.cos(a):.1f}" y2="{cy-(r-14)*math.sin(a):.1f}" stroke="{INK}" stroke-width="2"/>' + dot(cx, cy, 3, INK)
    return s + (t(cx, cy + 16, label, 8.5, INK, "khand", anchor="middle") if label else ""), 72
def b_blobs(y, items, h=110, axes=("Repair", "Prevent", "One trade", "Whole home"), labels="inside"):
    s = rect(14, y, 212, h, SOFT, "none", 6) + f'<line x1="120" y1="{y+6}" x2="120" y2="{y+h-6}" stroke="#D6D0C6"/><line x1="20" y1="{y+h/2}" x2="220" y2="{y+h/2}" stroke="#D6D0C6"/>'
    s += t(20, y + h / 2 - 3, axes[0], 6.8, MUTE) + t(220, y + h / 2 - 3, axes[1], 6.8, MUTE, anchor="end") + t(124, y + h - 8, axes[2], 6.8, MUTE) + t(124, y + 13, axes[3], 6.8, MUTE)
    for (nm, fx, fy, r, c) in items:
        cx, cy = 14 + 212 * fx, y + h * fy
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{c}33" stroke="{c}" stroke-width="1.2"/>'
        s += t(cx, cy + 3, nm, 7.5, INK, "hind", 600, "middle") if labels == "inside" else t(cx + r + 3, cy + 3, nm, 7.5, INK, "hind", 600)
    return s, h + 8
def b_sample(y, s="SAMPLE NUMBERS, NOT REAL"):
    w = len(s) * 4.4 + 14
    return rect(120 - w / 2, y, w, 14, "#FFFFFF", SAFFRON, 3, 1, 'stroke-dasharray="3 2"') + t(120, y + 10, s, 7.5, "#8a6510", "hind", 700, "middle", 'letter-spacing=".6"'), 20
from team_kit import b_card as _b_card
def b_cards(y, items, c=None, mark="dot", edge="line", h=34):
    """team_kit b_cards, but c may also be a list of colours (one per row). Process-local override."""
    s, hh = "", 0
    for i, it in enumerate(items):
        it = list(it) + [""] * (3 - len(it)); cc = (c[i % len(c)] if isinstance(c, (list, tuple)) else c) or ACC[i % 4]
        g, d = _b_card(y + hh, it[0], it[1], cc, it[2], mark if mark != "num" else str(i + 1), h, edge); s += g; hh += d
    return s, hh
def b_cdots(y, n=4, cur=0, auto=False):
    x0 = 120 - (n - 1) * 6; s = "".join(rect(x0 + i * 12 - (5 if i == cur else 2.5), y + 2, 10 if i == cur else 5, 5, TERRA if i == cur else "#D6D0C6", "none", 2.5) for i in range(n)); h = 14
    if auto: s += f'<path d="M20 {y+h+5} a5 5 0 1 1 1.5 3.6" fill="none" stroke="{LAGOON}" stroke-width="1.4"/>' + t(34, y + h + 9, "Loops on its own", 7.5, LAGOON, "hind", 600); h += 14
    return s, h + 4
def b_raw(y, svg, h):
    """Raw svg drawn from y=0, moved to the block's place (team_kit b_raw does not translate)."""
    return f'<g transform="translate(0,{y})">{svg}</g>', h
for _k, _v in list(globals().items()):
    if _k.startswith("b_"): BLK[_k[2:]] = _v
# ---- deck building ----
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
def make(prefix, app):
    pairs, O, add = deck(prefix, app); n = [0]
    def P(group, loc, el, sentence, a, b, purpose="new"):
        """a/b = (key, label, desc, feeling, svg). Caption is R105: '<loc>: <el>, <sentence>'."""
        n[0] += 1; k = f"{n[0]:02d}"; ask = f"{loc}: {el}, {sentence}"
        bad = caption_rule.check(ask); assert not bad, (ask, bad)
        for x in (a, b): assert len(x[1]) <= 34 and len(x[2]) <= 72, x[:3]
        add(group, el[0].upper() + el[1:], O(k + a[0], a[1], a[2], a[3], a[4]), O(k + b[0], b[1], b[2], b[3], b[4]), ask, purpose=purpose)
    return pairs, P
def page(did, slug_base):
    from agent_links import patch as link_patch
    from chat_button import patch as chat_patch
    pages = json.load(open("decks/pages.json"))
    slug = pages.get(did) or slug_base + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    FIX = ("body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
           "body.carding .opt .vis{min-height:0;overflow:visible}")
    HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
    s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
    pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    return slug, f"https://webermanapps.github.io/style-swipe/{slug}/"
def ship(did, name, app, pairs, meta, seed, slug_base, upkeep=False):
    assert len(pairs) == 10, (did, len(pairs)); assert theme_name_ok(name) and not re.search(r"\d", name), name
    caption_rule.guard(pairs, did)
    txt = json.dumps(pairs, ensure_ascii=False)
    assert not EMOJI.search(txt), "emoji"
    if upkeep: assert not re.search(r"thai|thailand", txt, re.I), "R110"
    order = [p["ask"] for p in pairs]
    publish(did, name, app, pairs, dict(meta, deck_size=10, caption_rule="R105", notes=True, built_by="Branding", built_at_note="Morning decks Oct 18 2026 (daily work report 2026-10-17, rules 3 and 5)",
            sources={"report": "/workspace/ops/brand/daily-work-report/2026-10-17.md", "rulebook": "/workspace/ops/brand/dashboard-rulebook.md", "builder": "tools/build_morning_decks_1018.py"}), seed=seed, n=10, first=0)
    dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
    for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
    json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False)
    slug, url = page(did, slug_base)
    return {"id": did, "name": name, "url": url, "slug": slug, "titles": [p["ask"] for p in dj["pairs"]]}
