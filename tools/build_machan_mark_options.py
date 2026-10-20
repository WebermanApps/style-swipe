#!/usr/bin/env python3
"""Oct 16 2026 (Max): Machan Mark Options Deck, 11 pairs (Max asked for 11, overrides 20). 22 variations of
/workspace/ops/brand/machan-mark.svg; each card shows the mark large AND at real 22px beside 'Built by Machan'.
Chat to Branding, submit_agent branding. Slug: descriptive + random letters (queue/machan-mark-slugs.json)."""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets
from team_kit import deck, publish
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
TC, LB, JG, JG2, CR, BL, INK, MU = "#C8643F", "#2E6F86", "#3F7D58", "#5E9A6E", "#FAF6EE", "#E9B9A3", "#0A0A0A", "#6B6560"
SAF = "#D4A017"
def mark(shape="round", expr="smile", sprout="two", style="fill", body=TC, eye=LB, acc=None, mono=False, cheek=BL):
    """24x24 mark, returns inner SVG elements."""
    s = ""
    # sprout
    if sprout == "two": s += f'<path d="M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z" fill="{JG}"/><path d="M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z" fill="{JG2}"/>'
    elif sprout == "one": s += f'<path d="M12 5.4C12.3 3 14 1.6 16.4 1.8c-.2 2.2-1.9 3.6-4.4 3.6z" fill="{JG}"/><path d="M12 5.6V3.8" stroke="{JG}" stroke-width=".9" stroke-linecap="round"/>'
    elif sprout == "curl": s += f'<path d="M12 5.6c0-2 1-3.4 2.6-3.4 1.2 0 1.8 1 1.2 1.8-.5.6-1.4.4-1.4-.3" fill="none" stroke="{JG}" stroke-width="1.2" stroke-linecap="round"/><path d="M12 4.6C11 3.2 9.6 2.9 8.6 3.4c.6 1.3 1.9 1.8 3.4 1.2z" fill="{JG2}"/>'
    # body
    sw = 1.6
    if shape == "round": b = '<rect x="3.5" y="5.5" width="17" height="16" rx="7"{a}/>'
    elif shape == "square": b = '<rect x="3.5" y="5.5" width="17" height="16" rx="3.2"{a}/>'
    else: b = '<path d="M12 5.2L20.5 11.2V19.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2V11.2Z"{a}/>'
    s += b.format(a=f' fill="{body}"' if style == "fill" else f' fill="#FFFFFF" stroke="{body}" stroke-width="{sw}" stroke-linejoin="round"')
    if mono:
        return s + f'<text x="12" y="19.2" text-anchor="middle" font-family="Khand,sans-serif" font-weight="700" font-size="11" fill="{CR if style=="fill" else body}">M</text>'
    face = '<rect x="5.5" y="9.5" width="13" height="10" rx="{r}" fill="{c}"/>'.format(r=1.6 if shape != "round" else 5, c=CR)
    if style == "fill": s += face
    # accessory
    if acc == "hat": s += f'<path d="M8 6.6h8l-1-2.6H9z" fill="{LB}"/><rect x="6.8" y="6.2" width="10.4" height="1.2" rx=".6" fill="{INK}"/>'
    if acc == "band": s += f'<rect x="4.2" y="8" width="15.6" height="1.6" fill="{SAF}"/>'
    # eyes
    if expr == "sleepy": s += f'<path d="M8.4 13.6q1.2 .9 2.4 0M13.2 13.6q1.2 .9 2.4 0" fill="none" stroke="{eye}" stroke-width="1.1" stroke-linecap="round"/>'
    elif expr == "wink": s += f'<circle cx="9.6" cy="13.3" r="1.35" fill="{eye}"/><path d="M13.2 13.5q1.2-.9 2.4 0" fill="none" stroke="{eye}" stroke-width="1.1" stroke-linecap="round"/>'
    else: s += f'<circle cx="9.6" cy="13.3" r="1.35" fill="{eye}"/><circle cx="14.4" cy="13.3" r="1.35" fill="{eye}"/>'
    # mouth
    if expr == "grin": s += f'<path d="M10.2 15.7h3.6q-.3 1.9-1.8 1.9t-1.8-1.9z" fill="{TC if body == TC else body}"/>'
    else: s += f'<path d="M10.6 16.1q1.4 1.1 2.8 0" fill="none" stroke="{body}" stroke-width="1.1" stroke-linecap="round"/>'
    if cheek: s += f'<circle cx="7.6" cy="15.6" r=".9" fill="{cheek}"/><circle cx="16.4" cy="15.6" r=".9" fill="{cheek}"/>'
    return s
def card(m, word="plain", label=""):
    g = lambda x, y, sz: f'<g transform="translate({x},{y}) scale({sz/24})">{m}</g>'
    s = '<rect width="240" height="300" fill="#FFFFFF"/><rect x="0" y="0" width="240" height="196" fill="#FAF6EE"/>' + g(52, 24, 136)
    s += '<line x1="16" y1="214" x2="224" y2="214" stroke="#e3ddd2"/><text x="16" y="232" font-family="Hind,sans-serif" font-size="9" font-weight="600" fill="#8A8580" letter-spacing="1">REAL SIZE, 22PX</text>'
    if word == "plain": s += g(16, 246, 22) + f'<text x="44" y="262" font-family="Hind,sans-serif" font-size="14" fill="{MU}">Built by Machan</text>'
    elif word == "bold": s += g(16, 246, 22) + f'<text x="44" y="262" font-family="Hind,sans-serif" font-size="14" fill="{MU}">Built by <tspan font-family="Khand,sans-serif" font-weight="700" font-size="16" fill="{INK}">Machan</tspan></text>'
    elif word == "after": s += f'<text x="16" y="262" font-family="Hind,sans-serif" font-size="14" fill="{MU}">Built by Machan</text>' + g(124, 246, 22)
    elif word == "pill": s += f'<rect x="12" y="242" width="140" height="30" rx="15" fill="#FAF6EE" stroke="#e3ddd2"/>' + g(18, 246, 22) + f'<text x="46" y="262" font-family="Hind,sans-serif" font-size="14" fill="{MU}">Built by Machan</text>'
    elif word == "stack": s += g(16, 246, 22) + f'<text x="44" y="255" font-family="Hind,sans-serif" font-size="9" fill="{MU}">Built by</text><text x="44" y="270" font-family="Khand,sans-serif" font-weight="700" font-size="15" fill="{INK}">MACHAN</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" style="width:100%;height:auto;display:block">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>'
pairs, O, add = deck("mmo_", "Branding")
def P(g, ask, a, b):
    add(g, g, *[O(o[0], o[1], o[2], o[3], card(mark(**o[4]), o[5] if len(o) > 5 else "plain")) for o in (a, b)], ask)
P("Expression", "Expression: Soft Smile Or Wink?",
  ("ex_smile", "Soft Smile", "The first-pass face: two eyes, small smile.", "friendly", {}),
  ("ex_wink", "Wink", "One eye winks, a bit cheeky.", "playful", dict(expr="wink")))
P("Expression", "Expression: Sleepy Calm Or Big Grin?",
  ("ex_sleepy", "Sleepy Calm", "Closed happy eyes, very calm.", "calm", dict(expr="sleepy")),
  ("ex_grin", "Big Grin", "Open grin, more energy.", "bold", dict(expr="grin")))
P("Sprout", "Sprout: Single Leaf Or Curly Tendril?",
  ("sp_one", "Single Leaf", "One leaf on a short stem.", "clean", dict(sprout="one")),
  ("sp_curl", "Curly Tendril", "A curl plus a small leaf.", "playful", dict(sprout="curl")))
P("Face Shape", "Face Shape: Soft Square Or House-Roof Top?",
  ("fs_square", "Soft Square", "Rounded square, sturdier feel.", "practical", dict(shape="square")),
  ("fs_roof", "House-Roof Top", "Pointed roof top, a nod to building homes.", "warm", dict(shape="roof")))
P("Color Pop", "Color Pop: Lagoon Blue Body Or Jungle Green Body?",
  ("cp_lagoon", "Lagoon Blue Body", "Blue body, terracotta eyes.", "fresh", dict(body=LB, eye=TC)),
  ("cp_jungle", "Jungle Green Body", "Green body, blue eyes.", "natural", dict(body=JG, eye=LB)))
P("Line Weight", "Line Weight: Filled Or Outline?",
  ("lw_fill_sq", "Filled", "Solid terracotta, round face, wink.", "bold", dict(expr="wink", sprout="one")),
  ("lw_outline", "Outline", "Terracotta outline on white, lighter.", "minimal", dict(style="outline", expr="smile")))
P("Accessory", "Accessory: Tiny Hat Or Headband?",
  ("ac_hat", "Tiny Hat", "Small lagoon-blue cap.", "playful", dict(acc="hat", sprout="none")),
  ("ac_band", "Headband", "Saffron headband across the brow.", "sporty", dict(acc="band")))
P("Monogram", "Mascot Face Or Plain Monogram M?",
  ("mo_face", "Mascot Face", "Roof-top face with grin.", "friendly", dict(shape="roof", expr="grin", sprout="one")),
  ("mo_m", "Monogram M", "No face, a Khand M on terracotta.", "formal", dict(mono=True)))
P("Wordmark", "Wordmark: Plain Text Or Bold Khand 'Machan'?",
  ("wm_plain", "Plain Text", "Mark, then 'Built by Machan' in Hind.", "calm", dict(sprout="curl"), "plain"),
  ("wm_bold", "Bold Machan", "'Machan' in bold Khand, darker.", "bold", dict(sprout="curl"), "bold"))
P("Wordmark", "Wordmark Layout: Mark After The Text Or In A Soft Pill?",
  ("wm_after", "Mark After Text", "'Built by Machan' then the mark.", "quiet", dict(expr="sleepy", shape="square"), "after"),
  ("wm_pill", "Soft Pill", "Mark and text in a cream pill.", "polished", dict(expr="sleepy", shape="square"), "pill"))
P("Wordmark", "Wordmark: Stacked MACHAN Or Outline Mark With Plain Text?",
  ("wm_stack", "Stacked", "Small 'Built by' over MACHAN in caps.", "editorial", dict(shape="roof", body=LB, eye=TC), "stack"),
  ("wm_outline", "Outline Mark", "Outline sleepy mark, plain text.", "minimal", dict(style="outline", expr="sleepy", sprout="curl"), "plain"))
assert len(pairs) == 11
did, NAME = "machan-mark-options-deck", "Machan Mark Options Deck"
order = [p["ask"] for p in pairs]
publish(did, NAME, "Branding", pairs, {"brands": ["Machan mark (footer mascot) options, 22 variations"], "submit_agent": "branding", "topic": did, "deck_size": 11, "board": "branding", "audience": "Max", "requested": True}, seed=8300, n=11)
dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"])); json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 11
SL = "queue/machan-mark-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
if did not in slugs: slugs[did] = "machan-mark-options-" + "".join(secrets.choice(string.ascii_lowercase) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]
FIX = ".v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important}body.carding .opt .vis{min-height:0;overflow:visible}"
HEAD = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{did}"</script>\n<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}{FIX}</style>\n'
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
