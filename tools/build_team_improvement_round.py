#!/usr/bin/env python3
"""Branding: next round of the permanent Team Improvement Deck (R75, R88: 10 picks per round; Oct 17 2026).
Reuses the round-one drawing kit from build_team_improvement_deck.py (svg/thumb), adds deck-look drawings.
New deck id per round so answers never mix; same name; submit_agent branding; chat to Branding; Machan footer from the template.
usage: build_team_improvement_round.py <deck_id>   (prints slug + url; page written UNLOCKED, lock before commit)"""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, re, string, secrets
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
src = open("tools/build_team_improvement_deck.py").read(); ns = {"__file__": os.path.abspath("tools/build_team_improvement_deck.py"), "__name__": "ti_lib"}
exec(src[:src.index('SL = "queue/team-improvement-slugs.json"')], ns); os.chdir(ROOT)
rect, t, X, Y, W, H, INK, MUTE, LINE, BEI, W_ = (ns[k] for k in ("rect", "t", "X", "Y", "W", "H", "INK", "MUTE", "LINE", "BEI", "W_"))
old_thumb = ns["thumb"]
def card(x, y, w, h, fill=W_, stroke=LINE, r=0): return rect(x, y, w, h, fill, stroke, r)
def thumb(k, a):
    cx = X + W / 2
    if k in ("bg_white", "bg_cream"):
        bg = W_ if k == "bg_white" else BEI
        return rect(X, Y, W, H, bg, LINE) + card(cx - 44, Y + 12, 88, 80) + rect(cx - 36, Y + 20, 72, 40, a) + rect(cx - 36, Y + 68, 50, 6, INK) + rect(cx - 36, Y + 80, 64, 4, MUTE)
    if k in ("corner_sq", "corner_rd"):
        r = 0 if k == "corner_sq" else 10
        return rect(X, Y, W, H, BEI, LINE) + card(cx - 80, Y + 14, 72, 76, W_, INK, r) + card(cx + 8, Y + 14, 72, 76, W_, INK, r) + rect(cx - 72, Y + 22, 56, 34, a, "none", max(r - 4, 0)) + rect(cx + 16, Y + 22, 56, 34, a, "none", max(r - 4, 0))
    if k in ("votes_a", "votes_b"):
        labs = ["THIS", "BOTH", "LOVE", "THAT", "NEITHER"] if k == "votes_a" else ["NO", "MAYBE", "LOVE", "YES", "SKIP"]
        s = rect(X, Y, W, H, BEI, LINE) + card(cx - 50, Y + 8, 100, 48) + rect(cx - 44, Y + 14, 88, 28, a)
        for i, l in enumerate(labs):
            x = X + 6 + i * 40; s += rect(x, Y + 66, 36, 26, a if l == "LOVE" else W_, INK) + t(x + 18, Y + 83, l, 6.8 if len(l) > 5 else 7.5, W_ if l == "LOVE" else INK, "hind", 700, "middle")
        return s
    if k == "split":
        return rect(X, Y, W, H, BEI, LINE) + card(X + 12, Y + 10, 88, 84) + card(X + 108, Y + 10, 88, 84) + rect(X + 18, Y + 16, 76, 50, a) + rect(X + 114, Y + 16, 76, 50, LINE) + rect(X + 18, Y + 74, 50, 5, INK) + rect(X + 114, Y + 74, 50, 5, INK)
    if k == "mockup":
        return rect(X, Y, W, H, BEI, LINE) + card(cx - 70, Y + 8, 140, 88) + rect(cx - 62, Y + 16, 124, 12, a) + "".join(card(cx - 62 + i * 42, Y + 34, 38, 30) for i in range(3)) + rect(cx - 62, Y + 72, 90, 5, MUTE) + rect(cx - 62, Y + 82, 60, 5, MUTE)
    if k == "textcard":
        return rect(X, Y, W, H, W_, LINE) + t(cx, Y + 48, "Go Through", 20, INK, "khand", 700, "middle") + t(cx, Y + 72, "Old Emails?", 20, INK, "khand", 700, "middle") + rect(cx - 30, Y + 84, 60, 4, a)
    if k == "splitdeck":
        s = rect(X, Y, W, H, BEI, LINE) + card(X + 14, Y + 20, 60, 64, W_, INK) + t(X + 44, Y + 57, "24", 16, INK, "khand", 700, "middle")
        s += f'<polygon points="{X+84},{Y+48} {X+100},{Y+52} {X+84},{Y+56}" fill="{a}"/>'
        return s + card(X + 110, Y + 12, 40, 40, W_, a) + t(X + 130, Y + 38, "10", 13, INK, "khand", 700, "middle") + card(X + 156, Y + 12, 40, 40, W_, a) + t(X + 176, Y + 38, "10", 13, INK, "khand", 700, "middle") + card(X + 133, Y + 58, 40, 40, W_, a) + t(X + 153, Y + 84, "4", 13, INK, "khand", 700, "middle")
    if k == "archive":
        return rect(X, Y, W, H, BEI, LINE) + rect(cx - 50, Y + 34, 100, 58, W_, INK, 0, 2) + rect(cx - 56, Y + 22, 112, 14, a) + rect(cx - 16, Y + 50, 32, 6, INK) + card(cx - 30, Y + 8, 40, 18, W_, INK)
    if k == "font_real":
        return rect(X, Y, W, H, W_, LINE) + f'<text x="{cx}" y="{Y+52}" font-size="24" font-family="Georgia,serif" font-style="italic" fill="{INK}" text-anchor="middle">Calm Morning</text>' + f'<text x="{cx}" y="{Y+82}" font-size="15" font-family="Courier New,monospace" fill="{MUTE}" text-anchor="middle">Calm Morning</text>'
    if k == "font_named":
        return rect(X, Y, W, H, W_, LINE) + t(cx, Y + 48, "Calm Morning", 24, INK, "khand", 700, "middle") + rect(cx - 50, Y + 64, 100, 22, BEI, LINE) + t(cx, Y + 79, "Font: Cormorant", 10, INK, "hind", 600, "middle")
    if k == "scale_up":
        return rect(X, Y, W, H, BEI, LINE) + card(X + 8, Y + 6, W - 16, H - 12, W_, INK) + rect(X + 16, Y + 14, W - 32, 18, a) + "".join(rect(X + 16, Y + 40 + i * 14, W - 32 - i * 30, 7, LINE) for i in range(4))
    if k == "small_cap":
        return rect(X, Y, W, H, BEI, LINE) + card(cx - 30, Y + 10, 60, 54, W_, INK) + rect(cx - 24, Y + 16, 48, 10, a) + "".join(rect(cx - 24, Y + 32 + i * 8, 40 - i * 8, 4, LINE) for i in range(3)) + rect(cx - 60, Y + 74, 120, 6, INK) + rect(cx - 44, Y + 86, 88, 4, MUTE)
    if k in ("line1", "line2"):
        s = rect(X, Y, W, H, W_, LINE) + rect(X + 14, Y + 12, W - 28, 36, a)
        s += t(X + 14, Y + 70, "Morning Report Cards", 15, INK, "khand", 700)
        if k == "line2": s += t(X + 14, Y + 88, "Three short cards with the top news.", 10.5, MUTE)
        return s
    return old_thumb(k, a)
ns["thumb"] = thumb
svg, kdeck, publish = ns["svg"], ns["kdeck"], ns["publish"]
from team_improvement_round_content import NAME, ABOUT, PAIRS
from agent_links import patch as link_patch
from chat_button import patch as chat_patch
did = sys.argv[1]
acc = [ns["TERRA"], ns["LAGOON"], ns["JUNGLE"], ns["SAFFRON"]]
FEEL = ["practical", "bold", "calm", "playful", "premium"]
pairs, O, add = kdeck("teamimp2_", "Grok Bot Team")
for gi, (g, ask, a, b) in enumerate(PAIRS):
    opts = []
    for side, o in enumerate((a, b)):
        oid = re.sub(r"[^a-z0-9]+", "_", o[0].lower())[:24] + f"_{gi}{side}"
        opts.append(O(oid, o[0], o[1], FEEL[(gi * 2 + side) % 5], svg(g, o[0], o[1], o[2:4], o[4], acc[(gi + side * 2) % 4])))
    add(g, g, opts[0], opts[1], ask)
publish(did, NAME, "Grok Bot Team", pairs, {"brands": [ABOUT, "Permanent Branding deck (R75): forward Max's 'ask Branding' dislikes here."],
        "submit_agent": "branding", "submit_to": "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "topic": "team-improvement",
        "deck_size": 10, "board": "branding", "audience": "Max", "permanent": True, "round": "two", "previous_round": "team-improvement-deck",
        "sources": "ops/team-sync/handoffs/team-improvement-sources-2026-10-16.md (Brand scan 2026-10-16 items 1-5, 7-9, 12) + re-asked skip (Idea Card)"}, seed=7600, n=10)
order = [p[1] for p in PAIRS]; dj = json.load(open(f"decks/{did}.json")); dj["pairs"].sort(key=lambda p: order.index(p["ask"]))
for i, p in enumerate(dj["pairs"], 1): p["id"] = f"{did}-{i:02d}"
json.dump(dj, open(f"decks/{did}.json", "w"), indent=1, ensure_ascii=False); assert len(dj["pairs"]) == 10, len(dj["pairs"])
SL = "queue/team-improvement-slugs.json"; slugs = json.load(open(SL)) if os.path.exists(SL) else {}
if did not in slugs: slugs[did] = "team-improvement-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
slug = slugs[did]
_i = src.index("FIX = ("); exec(src[_i:src.index("\n", src.index('overflow:visible}")', _i))], ns); FIX = ns["FIX"]
HEAD = f'''<base href="../">
<meta name="robots" content="noindex">
<script>window.DEFAULT_DECK="{did}"</script>
<style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}{FIX}</style>
'''
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1)
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p); chat_patch(p)
h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({"deckId": did, "name": NAME, "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/"}))
