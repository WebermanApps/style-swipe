#!/usr/bin/env python3
"""Oct 16 2026 (Max): Phone Home Top Section Deck, 20 this-or-that pairs for the smartupkeep.ai home hero ON A PHONE.
Baseline = Hero C (smart-upkeep 8a4e623): h1, lead, 16:9 video teaser (poster, 0.6s loop, warm filter) in cream #FBF6EE card
with terracotta outlines, price pill, full-width Get Started; trust chips (Certified Techs, Honest Refund, Report Every Visit,
Metro Detroit) in the row below. Each option = drawn 393px phone frame. Kit copied from build_upkeep_trust_tags.py (89aed43)."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, json, string, secrets
from html import escape
from team_kit import deck, publish
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CR, INK, MU, TD, LN = "#FBF6EE", "#1A1A1A", "#3D3D3D", "#C1502E", "#E5E0D8"
W, VH = 393, 760  # phone viewport (below status bar), tab bar at bottom
CHIPS = [("Certified Techs", "#C1502E1C", "#A8432A"), ("Honest Refund", "#05668D1A", "#05668D"), ("Report Every Visit", "#D4A01726", "#7A5A0E"), ("Metro Detroit", "#0B6E4F1A", "#0B6E4F")]
def T(x, y, s, fs, fam="Hind", wt=400, fill=INK, anchor="start", ls=0):
    return f'<text x="{x}" y="{y}" font-family="{fam},sans-serif" font-weight="{wt}" font-size="{fs}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{escape(s)}</text>'
def video(x, y, w, h, play="auto", dark=False):
    s = f'<g><clipPath id="vc{x}{y}{w}{h}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/></clipPath><g clip-path="url(#vc{x}{y}{w}{h})">'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFDF9"/>'
    gy = y + h * .72
    s += f'<rect x="{x}" y="{gy}" width="{w}" height="{h-(gy-y)}" fill="#F3EBDD"/>'
    s += T(x + w*.05, y + h*.36, "Introducing", min(16, w*.045), "Khand", 700) + T(x + w*.05, y + h*.36 + min(18, w*.05), "Smart Upkeep", min(16, w*.045), "Khand", 700, TD)
    vx, vy, vw = x + w*.42, gy - w*.15, w*.36  # van
    s += f'<rect x="{vx}" y="{vy}" width="{vw*.72}" height="{w*.13}" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/><path d="M{vx+vw*.72} {vy+w*.04} h{vw*.18} l{vw*.1} {w*.05} v{w*.04} h-{vw*.28}z" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    s += f'<path d="M{vx} {vy+w*.1} h{vw}" stroke="{TD}" stroke-width="3"/><circle cx="{vx+vw*.18}" cy="{gy}" r="{w*.022}" fill="{INK}"/><circle cx="{vx+vw*.82}" cy="{gy}" r="{w*.022}" fill="{INK}"/>'
    tx = x + w*.88; s += f'<circle cx="{tx}" cy="{gy-w*.11}" r="{w*.018}" fill="#7A4E2E"/><rect x="{tx-w*.022}" y="{gy-w*.09}" width="{w*.044}" height="{w*.09}" rx="3" fill="#8A8A8A"/>'
    if dark: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#shade)"/>'
    s += '</g></g>'
    if play == "poster":
        s += f'<circle cx="{x+w/2}" cy="{y+h/2}" r="26" fill="#FFFFFFE6" stroke="{TD}" stroke-width="2"/><path d="M{x+w/2-7} {y+h/2-11} l19 11 -19 11z" fill="{TD}"/>'
        s += f'<rect x="{x+w-46}" y="{y+h-26}" width="38" height="18" rx="2" fill="#1A1A1ACC"/>' + T(x+w-27, y+h-13, "0:50", 11, wt=600, fill="#fff", anchor="middle")
    else:
        s += f'<circle cx="{x+20}" cy="{y+h-20}" r="8" fill="none" stroke="{INK}" stroke-width="1.5"/><path d="M{x+17} {y+h-24} l7 4 -7 4z" fill="{INK}"/>'
        s += f'<rect x="{x+w-46}" y="{y+h-26}" width="38" height="18" rx="2" fill="#1A1A1ACC"/>' + T(x+w-27, y+h-13, "0:50", 11, wt=600, fill="#fff", anchor="middle")
    return s
def chiprow(y, mode, x0=16):
    s, x = "", x0
    if mode == "scroll":
        for t, bg, fg in CHIPS:
            w = len(t) * 7.1 + 22; s += f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="{bg}"/>' + T(x + 11, y + 20, t, 13, wt=600, fill=fg); x += w + 8
        return s + f'<rect x="{W-40}" y="{y}" width="40" height="30" fill="url(#fadeR)"/>', 42
    rows = 0; yy = y
    for t, bg, fg in CHIPS:
        w = len(t) * 7.1 + 22
        if x + w > W - 16: x, yy = x0, yy + 38
        s += f'<rect x="{x}" y="{yy}" width="{w}" height="30" rx="15" fill="{bg}"/>' + T(x + 11, yy + 20, t, 13, wt=600, fill=fg); x += w + 8
    return s, yy - y + 42
def phone(o):
    g = {"tight": .7, "normal": 1, "airy": 1.35}[o.get("density", "normal")]
    out, y = "", 0
    logo = o.get("logo", "md"); hb = {"sm": 44, "md": 62, "lg": 84}[logo]; lf = {"sm": 18, "md": 24, "lg": 32}[logo]
    out += f'<rect x="0" y="0" width="{W}" height="{hb}" fill="#fff"/>'
    lx = W/2 if o.get("logo_pos", "center") == "center" else 16; an = "middle" if lx == W/2 else "start"
    out += f'<text x="{lx}" y="{hb/2+lf*.35}" font-family="Khand,sans-serif" font-weight="700" font-size="{lf}" text-anchor="{an}"><tspan fill="{INK}">smart</tspan><tspan fill="{TD}">up</tspan><tspan fill="{INK}">keep</tspan></text>'
    if o.get("hdr_call"): out += f'<rect x="{W-104}" y="{hb/2-16}" width="88" height="32" fill="none" stroke="{TD}" stroke-width="1.5"/>' + T(W-60, hb/2+5, "CALL US", 13, "Khand", 700, TD, "middle", 1)
    else: out += f'<rect x="{W-96}" y="{hb/2-17}" width="80" height="34" fill="#fff" stroke="{INK}" stroke-width="1.5"/>' + T(W-56, hb/2+5, "SHARE", 13, "Khand", 700, INK, "middle", 1.5)
    y = hb + 8 * g
    card = o.get("card", True); pad = 16 if card else 0; cx, cw = 14 if card else 0, W - 28 if card else W
    cy0 = y; body = ""; iy = y + (22 * g if card else 14 * g); ix = cx + 16 if card else 16; iw = cw - 32 if card else W - 32
    hs = o.get("h1", 34); lines = o.get("lines", ["Your Home, Taken", "Care Of."])
    def vid(yy):
        r = o.get("ratio", 16/9); full = o.get("bleed", False)
        vx, vw = (0, W) if full else (ix, iw); vh = vw / r
        return video(vx, yy, vw, vh, o.get("play", "auto"), o.get("overlay", False)), vh
    def heads(yy, fill=INK, sub=MU):
        b = ""
        for l in lines: yy += hs * 1.02; b += T(ix, yy, l, hs, "Khand", 700, fill)
        lead = o.get("lead", ["Catch small problems before they\u2019re big", "ones."])
        if lead:
            yy += 8 * g
            for l in lead: yy += 22; b += T(ix, yy, l, 16.5, fill=sub)
        return b, yy
    if o.get("overlay"):
        vb, vh = vid(iy if not o.get("bleed") else y); vy = iy if not o.get("bleed") else y
        body += vb; hb2, _ = heads(vy + vh - 20 - len(lines) * hs * 1.02 - (len(o.get("lead") or []) * 22 + (8 if o.get("lead") else 0)), "#fff", "#FFFFFFE0"); body += hb2; iy = vy + vh + 18 * g
    else:
        order = o.get("order", "text")
        if order == "video":
            vb, vh = vid(iy if not o.get("bleed") else y); body += vb; iy = (iy if not o.get("bleed") else y) + vh + 6 * g
            hb2, iy = heads(iy); body += hb2; iy += 18 * g
        else:
            hb2, iy = heads(iy); body += hb2; iy += 24 * g
            vb, vh = vid(iy); body += vb; iy += vh + 24 * g
    if o.get("price", True):
        pt = "MEMBERSHIP STARTING AT $99/MONTH"; pw = len(pt) * 8 + 20
        body += f'<rect x="{ix}" y="{iy}" width="{pw}" height="32" fill="#fff" stroke="{TD}" stroke-width="1.2"/>' + T(ix + 10, iy + 21, pt, 13, "Khand", 700, INK, ls=.6); iy += 32 + 16 * g
    cta = o.get("cta", "full"); ct = o.get("cta_text", "GET STARTED").upper(); call = o.get("call")
    def btn(x, yy, w, t, solid=True):
        return (f'<rect x="{x}" y="{yy}" width="{w}" height="48" rx="4" fill="{TD if solid else "#fff"}" stroke="{TD}" stroke-width="1.5"/>' + T(x + w/2, yy + 30, t, 15, "Khand", 700, "#fff" if solid else TD, "middle", 2))
    if cta in ("full", "inline"):
        if call == "pair": w2 = (iw - 10) / 2; body += btn(ix, iy, w2, ct) + btn(ix + w2 + 10, iy, w2, "CALL US", False)
        elif call == "only": body += btn(ix, iy, iw, "CALL US")
        else: body += btn(ix, iy, iw if cta == "full" else len(ct) * 10 + 48, ct)
        iy += 48 + (10 * g)
        if o.get("ghost"): body += T(ix + iw/2, iy + 16, o["ghost"], 14, wt=600, fill=TD, anchor="middle"); iy += 26
    if o.get("chips") in ("scroll", "wrap") and o.get("chips_in", True):
        iy += 8 * g; cs, ch = chiprow(iy, o["chips"], ix); body += cs; iy += ch
    iy += (6 * g if card else 0)
    if card: out += f'<rect x="{cx}" y="{cy0}" width="{cw}" height="{iy - cy0 + 10}" fill="{CR}" stroke="#E8DCCB"/><rect x="{cx}" y="{cy0}" width="{cw}" height="3" fill="{TD}"/>'
    elif not o.get("bleed"): out += f'<rect x="0" y="{cy0}" width="{W}" height="{iy - cy0 + 10}" fill="{CR}"/>'
    else: out += f'<rect x="0" y="{cy0}" width="{W}" height="{iy - cy0 + 10}" fill="{CR}"/>'
    out += body; y = iy + 30
    if o.get("chips", "below") == "below":
        out += T(16, y + 6, "Why Trust Us", 22, "Khand", 700) + T(W-16, y + 6, "HOW WE VET", 13, "Khand", 700, TD, "end", 1.5); cs, ch = chiprow(y + 20, "scroll"); out += cs; y += 20 + ch + 24
    out += T(16, y + 6, "Plans", 22, "Khand", 700) + T(W-16, y + 6, "FREE QUOTE IN MINUTES", 13, "Khand", 700, INK, "end", 1.5)
    out += f'<rect x="34" y="{y+28}" width="325" height="220" rx="10" fill="#fff" stroke="#05668D" stroke-width="2"/>' + T(52, y + 64, "MOST POPULAR", 12, wt=600) + T(52, y + 92, "Plus", 22, "Khand", 700)
    tb = VH - 62
    if cta == "sticky":
        tb -= 70; out += f'<rect x="0" y="{tb}" width="{W}" height="70" fill="#fff" stroke="{LN}"/>'
        if call == "pair": out += btn(16, tb + 11, 230, ct) + btn(256, tb + 11, 121, "CALL", False)
        else: out += btn(16, tb + 11, W - 32, ct)
        tb += 70
    out += f'<rect x="0" y="{tb}" width="{W}" height="62" fill="#fff" stroke="{LN}"/><rect x="0" y="{tb}" width="78" height="2" fill="{TD}"/>'
    for i, n in enumerate(["Home", "Plans", "\u00c0 La Carte", "My Home", "Account"]):
        out += f'<rect x="{39+i*78.6-8}" y="{tb+12}" width="16" height="16" rx="3" fill="none" stroke="{TD if i==0 else INK}" stroke-width="1.5"/>' + T(39 + i * 78.6, tb + 46, n, 12, fill=TD if i == 0 else INK, anchor="middle")
    defs = f'<defs><linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="{CR if o.get("chips")=="scroll" else "#fff"}"/></linearGradient><linearGradient id="shade" x1="0" x2="0" y1="0" y2="1"><stop offset=".25" stop-color="#1A1A1A" stop-opacity="0"/><stop offset="1" stop-color="#1A1A1A" stop-opacity=".78"/></linearGradient><clipPath id="scr"><rect x="12" y="36" width="{W}" height="{VH}"/></clipPath></defs>'
    frame = f'<rect x="1" y="1" width="{W+22}" height="{VH+66}" rx="44" fill="#1A1A1A"/><rect x="12" y="12" width="{W}" height="{VH+42}" rx="34" fill="#fff"/>' + T(46, 30, "9:41", 13, wt=600) + f'<rect x="{12+W/2-50}" y="16" width="100" height="22" rx="11" fill="#1A1A1A"/><rect x="{W-30}" y="20" width="24" height="11" rx="3" fill="none" stroke="{INK}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W+24} {VH+68}" style="width:100%;height:auto;display:block">{defs}{frame}<g clip-path="url(#scr)"><g transform="translate(12 36)">{out}</g></g><rect x="{12+W/2-60}" y="{VH+30}" width="120" height="5" rx="2.5" fill="#1A1A1A"/></svg>'
NOW = {}
pairs, O, add = deck("phh_", "UpKeep")
def P(g, ask, a, b): add(g, g, *[O(x[0], x[1], x[2], x[3], phone(x[4])) for x in (a, b)], ask)
NOWD = ("now", "Hero C (Now)", "Live phone hero: text, 16:9 video in cream card, price pill, full-width Get Started.", "familiar", NOW)
def now(i): return (f"now{i}",) + NOWD[1:]
P("Video", "Video Shape: 16:9 Or 4:5?", now(1), ("v45", "4:5 Video", "Taller video fills more of the phone screen; CTA drops lower.", "immersive", {"ratio": 4/5}))
P("Video", "Video: Inside The Card Or Full-Bleed Edge To Edge?", now(2), ("bleed", "Full-Bleed Video On Top", "Video runs edge to edge under the header, text below.", "bold", {"card": False, "bleed": True, "order": "video"}))
P("Video", "Video Size: Square 1:1 Or Tall 9:16 Teaser?", ("v11", "Square 1:1 Video", "Square video, middle ground.", "balanced", {"ratio": 1}), ("v916", "Tall 9:16 Video", "Phone-shaped video; text and CTA fall below the fold.", "cinematic", {"ratio": 9/16, "order": "video", "lines": ["Your Home, Taken Care Of."], "h1": 28}))
P("Order", "Order: Headline First Or Video First?", now(3), ("vfirst", "Video First", "Video at the top of the card, headline under it.", "visual", {"order": "video"}))
P("Order", "Text Below The Video Or Over It?", ("below", "Text Below Video", "Video first, clean headline underneath.", "clean", {"order": "video"}), ("over", "Text Over Video", "Headline sits on the video with a dark fade.", "dramatic", {"overlay": True, "ratio": 4/5, "lines": ["Your Home,", "Taken Care Of."]}))
P("Headline", "Headline Size: 34px Or 44px?", now(4), ("h44", "Big 44px Headline", "Bigger, louder headline; pushes the video down.", "loud", {"h1": 44, "lines": ["Your Home,", "Taken Care Of."]}))
P("Headline", "Line Breaks: 'Your Home, Taken / Care Of.' Or 'Your Home, / Taken Care Of.'?", now(5), ("brk", "Break After 'Your Home,'", "Splits the line at the comma.", "rhythmic", {"lines": ["Your Home,", "Taken Care Of."]}))
P("Headline", "Headline: Two Lines At 34px Or One Line At 26px?", now(6), ("h26", "One Line, 26px", "Smaller headline fits one line; more room for the video.", "quiet", {"h1": 26, "lines": ["Your Home, Taken Care Of."]}))
P("Subhead", "Subhead: Keep It Or Drop It?", now(7), ("nolead", "No Subhead", "Headline straight into the video. Tighter top.", "minimal", {"lead": None}))
P("Subhead", "Subhead: Short Or Longer?", ("short", "Short Subhead", "'Catch small problems early.'", "punchy", {"lead": ["Catch small problems early."]}), ("long", "Longer Subhead", "Adds seasonal visits and a report after every visit (both on the site).", "informative", {"lead": ["Catch small problems before they\u2019re big", "ones. Seasonal visits and a written report", "after every visit."]}))
P("CTA", "Get Started: In-Flow Or Sticky Bottom Bar?", now(8), ("sticky", "Sticky Bottom Bar", "Get Started stays pinned above the tabs while you scroll.", "always-there", {"cta": "sticky"}))
P("CTA", "CTA Width: Full-Width Or Inline Button?", now(9), ("inline", "Inline Button", "Shorter button, left-aligned with the text.", "light", {"cta": "inline"}))
P("CTA", "CTA Words: 'Get Started' Or 'Free Quote In Minutes'?", now(10), ("quote", "Free Quote In Minutes", "Same words the site uses on Plans.", "low-pressure", {"cta_text": "Free Quote in Minutes"}))
P("Call", "Tap-To-Call Or Get Started?", ("gs", "Get Started Only", "One clear action (now).", "focused", {}), ("pair", "Get Started + Call Us", "Two buttons side by side. Site lists no phone number yet; needs Max's number.", "personal", {"call": "pair"}))
P("Call", "Header: Share Button Or Call Us Button?", now(11), ("hcall", "Call Us In Header", "Swap Share for a Call Us button. Needs Max's phone number.", "reachable", {"hdr_call": True}))
P("Trust", "Trust Chips: Next Row Down Or Inside The Hero?", now(12), ("chipin", "Chips Inside Hero (Scroll Row)", "Chips under Get Started, swipe sideways.", "reassuring", {"chips": "scroll"}))
P("Trust", "Chips In Hero: Scroll Row Or Wrap Onto Two Lines?", ("cscroll", "Scroll Row", "One line, swipe for more.", "neat", {"chips": "scroll"}), ("cwrap", "Wrap Onto Two Lines", "All four visible at once.", "complete", {"chips": "wrap"}))
P("Header", "Logo Bar: Medium Or Slim?", now(13), ("slim", "Slim Header, Small Logo", "44px bar, logo left. More hero above the fold.", "compact", {"logo": "sm", "logo_pos": "left"}))
P("Video", "Video: Autoplay Teaser Or Poster With Play Button?", ("auto", "Autoplay Teaser (Now)", "Muted loop from 0.6s, small play mark.", "alive", {}), ("poster", "Poster + Big Play Button", "Still poster; tap to play.", "calm", {"play": "poster"}))
P("Density", "Spacing: Roomy Or Tight?", ("airy", "Roomy", "More air between pieces; less fits above the fold.", "premium", {"density": "airy"}), ("tight", "Tight", "Less space; price and Get Started higher up.", "efficient", {"density": "tight", "price": True}))
assert len(pairs) == 20, len(pairs)
did, NAME = "upkeep-phone-home-top-section-deck", "Phone Home Top Section Deck"
order = [p["ask"] for p in pairs]
publish(did, NAME, "UpKeep", pairs, {"brands": ["Smart Upkeep home page hero on a phone: video size and crop, headline, subhead, CTA, call, trust chips, header, density"], "submit_agent": "upkeep", "topic": did, "deck_size": 20, "board": "upkeep", "audience": "Max", "requested": True}, seed=8410, n=20)
dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"])); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 20
SL = "queue/upkeep-phone-hero-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
if did not in slugs: slugs[did] = "phone-home-top-section-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]
FIX = ".v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important}body.carding .opt .vis{min-height:0;overflow:visible}"
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hind:wght@400;600&family=Khand:wght@700&display=swap">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
sz = json.load(open("decks/sizes.json")); sz[did] = 20; json.dump(dict(sorted(sz.items())), open("decks/sizes.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
