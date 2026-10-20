#!/usr/bin/env python3
"""Daily New Ideas deck for Research (R101, Max Oct 17 2026 15:53 ICT). 10 this-or-that picks of things Max could build
or directions to take: spinoffs of what he built + new ideas. Never repeats an idea: queue/new-ideas-history.json records every
idea key shown (and the finish() ledger blocks repeated option ids).
Leads: each run reads /workspace/ops/brand/new-ideas-leads.md (Research); up to 2 unshown lead pairs lead each deck.\nBank = tools/new_ideas_bank.py (hand-drawn) + tools/new_ideas_more.py (compact rows) + queue/new-ideas-generated.json (auto).
AUTO-REFILL: every run checks the unshown count first; under 20 it generates new pairs (project x direction matrix in
new_ideas_gen.py, real claims only, no numbers) into queue/new-ideas-generated.json before picking. Run it alone: new_ideas.py --refill.
Card text: title <=20 chars, description <=28 chars (one line each on a 393px phone); asserted.
Mockups: blocks spread/scaled to fill the 240x300 card; the page pins the picture box to the card's 4:5 shape (no empty band).
Name 'New Ideas: <theme>' (no numbers), random-suffix slug. Page is written UNLOCKED: lock it (lock_pages.py on a temp copy
of only the page) before commit.
R105 (Max Oct 17 2026 19:46 ICT): every pick's ask is 'Research New Ideas Deck: <idea area>, <one plain sentence>' (r105_ask(); caption_rule.guard).
R110 (Max Oct 17 2026 20:20 ICT): a deck that carries any UpKeep / Smart Upkeep idea never carries a Thai one (is_thai(); asserted).
usage: new_ideas.py [--dry] | --refill | --rebuild <deck_id>   (rebuild = same slug and ideas, fresh drawings/text)"""
import sys as _mws,os as _mwo;_mws.path.insert(0,_mwo.path.dirname(_mwo.path.abspath(__file__))+('' if _mwo.path.basename(_mwo.path.dirname(_mwo.path.abspath(__file__)))=='tools' else '/tools'));import mw_machan_pop  # Machan pop-up + cover date (Oct 20 2026 ICT)
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import sys, os, json, string, secrets, datetime, random
from team_kit import deck as kdeck, publish, BLK
from fu1017_kit import card
from agent_links import patch as link_patch
from new_ideas_bank import BANK as BANK1
import new_ideas_more, new_ideas_gen
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
import re as _re, caption_rule
LOC = "Research New Ideas Deck"
_TH = _re.compile(r"thai|thailand|bangkok|chiang mai|isan|siam|amomentinthai", _re.I)
_UK = _re.compile(r"upkeep", _re.I)
def is_thai(e): return bool(_TH.search(json.dumps(e, ensure_ascii=False, default=str)))
def is_upkeep(e): return bool(_UK.search(" ".join(map(str, e[:4]))))
def r105_ask(th, ask):
    """'<exact screen>: <element>, <one sentence>' -> 'Research New Ideas Deck: <idea area>, which series fits the channel next?'"""
    el = _re.sub(r"[,:@]", " ", {"@AMomentInThai": "YouTube channel"}.get(th, th)).strip()
    el = _re.sub(r"\s+", " ", el); s = ask.strip().rstrip(".")
    s = (s[:1].lower() + s[1:]) if s[:1].isupper() and not s.split(" ")[0] in ("Max", "Mom's", "Upkeep", "WellNest", "Style", "Site", "Japan", "Smart") else s
    s = _re.sub(r"\?\s*\((idea only)\)$", r" (\1)?", s)
    out = f"{LOC}: {el}, {s if s.endswith('?') else s + '.'}"
    bad = caption_rule.check(out); assert not bad, (out, bad); return out
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
HIST = "queue/new-ideas-history.json"; GEN = "queue/new-ideas-generated.json"; LOW = 20
hist = json.load(open(HIST)) if os.path.exists(HIST) else {"shown": {}, "decks": []}
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
def compact(i, spec):
    label, desc, tpl, items = spec.split("|"); its = [x for x in items.split(";") if x]; c = ACC[i % 4]
    hd = ("hdr", label, "", c, "logo", label[0])
    if tpl == "list": b = [("cards", [tuple(x.split(":", 1)) for x in its], None, "ic:check")]
    elif tpl == "tiles": b = [("tiles", [(x, ["home", "tag", "check", "star"][j % 4]) for j, x in enumerate(its)], 2, 60)]
    elif tpl == "checks": b = [("checks", its, JUNGLE, 1)]
    elif tpl == "steps": b = [("steps", its, c, 0), ("gap", 10), ("photo", 90, c, "house")]
    elif tpl == "timeline": b = [("timeline", [tuple(x.split(":", 1)) for x in its])]
    elif tpl == "photo": b = [("photo", 130, c, its[1] if len(its) > 1 else "house", its[0])]
    elif tpl == "word": b = [("word", its[0], 38, "#171717", its[1] if len(its) > 1 else "")]
    elif tpl == "chat": b = [("bubble", its[0], False), ("bubble", its[1], True, c)]
    elif tpl == "tags": b = [("tags", its), ("photos", 3, 70)]
    else: raise ValueError(tpl)
    return (label.lower().replace(" ", "-").replace("'", "")[:24], label, desc, c, [hd] + b)
def load_bank():
    rows = [(k, th, kd, ask, compact(0, a), compact(1, b)) for k, th, kd, ask, a, b in new_ideas_more.R]
    gen = json.load(open(GEN)) if os.path.exists(GEN) else []
    rows += [(k, th, kd, ask, compact(0, a), compact(1, b)) for k, th, kd, ask, a, b in gen]
    return list(BANK1) + rows
def refill(bank):
    fresh = [e for e in bank if e[0] not in hist["shown"]]
    if len(fresh) >= LOW: return bank
    gen = json.load(open(GEN)) if os.path.exists(GEN) else []
    have = {e[0] for e in bank}; add = [r for r in new_ideas_gen.generate() if r[0] not in have][:max(0, 60 - len(fresh))]
    if not add: sys.exit(f"bank low ({len(fresh)} unshown) and generator exhausted: add rows to tools/new_ideas_more.py or directions to new_ideas_gen.py")
    json.dump(gen + add, open(GEN, "w"), indent=1, ensure_ascii=False); print(f"refilled bank: +{len(add)} generated pairs", file=sys.stderr)
    return load_bank()
from uk5_art import GREY
from draft_svg import t as _t, rect as _r, crisp as _crisp
def frame(label, acc, body, H):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 {H}" width="240" height="{H}" class="{"ni-d" if H == 300 else "ni-m"}">'
         + _r(0, 0, 240, H, "#FFFFFF") + _r(0, 0, 240, 5, acc) + _t(14, 22, label.upper(), 7.5, acc, "hind", 600, extra='letter-spacing="1.2"'))
    return _crisp(s + body + _t(120, H - 3, "Built by Machan", 7.5, GREY, "hind", 400, "middle") + _r(.5, .5, 239, H - 1, "none", "#D6D0C6") + "</svg>")
def layout(blocks, top, avail):
    """Lay blocks out like at(), then scale (to width) and spread them (gap capped, centered) to fill top..top+avail."""
    y, parts = top, []
    for b in blocks:
        gg, h = BLK[b[0]](y, *b[1:]); parts.append((gg, y, h)); y += h
    total = y - top; sc = min(avail / total, 1.08) if total else 1
    gap = min(18, (avail - total * sc) / max(1, len(parts) - 1)) if len(parts) > 1 else 0
    pad = (avail - total * sc - gap * (len(parts) - 1)) / 2
    body = ""
    for i, (gg, y0, h) in enumerate(parts):
        ny = top + pad + (y0 - top) * sc + gap * i
        body += f'<g transform="translate({120 - 120 * sc:.2f},{ny - y0 * sc:.2f}) scale({sc:.4f})">{gg}</g>'
    return body
def fill_card(label, acc, blocks):
    """Two drawings: 240x300 for wider screens, 240x520 for phones (the phone picture box is tall), so the drawing fills
    the picture box either way. Phone version = the screen on top + a 1.35x close-up of its main content below."""
    d = frame(label, acc, layout(blocks, 32, 254), 300)
    head, rest = blocks[:1], blocks[1:] or blocks
    zoom, zy = "", 4
    for b in rest:
        gg, h = BLK[b[0]](zy, *b[1:]); zoom += gg; zy += h
    m_body = layout(blocks, 32, 254) + _r(14, 296, 212, 1, "#E3DDD2") + _t(14, 312, "CLOSE-UP", 7, GREY, "hind", 600, extra='letter-spacing="1.2"')
    m_body += f'<clipPath id="z{abs(hash(label + str(blocks))) % 10**8}"><rect x="0" y="318" width="240" height="190"/></clipPath>'
    cid = f"z{abs(hash(label + str(blocks))) % 10**8}"
    m_body += f'<g clip-path="url(#{cid})"><g transform="translate(-5,318) scale(1.35)">{zoom}</g></g>'
    return d + frame(label, acc, m_body, 540)
LEADF = "/workspace/ops/brand/new-ideas-leads.md"
def read_leads():
    """Each run: read the Research leads file. Mapped leads (new_ideas_more.LEADS) are already bank rows; a new unmapped
    lead becomes an auto pair (lead vs park it) in queue/new-ideas-generated.json and is reported so a better pair can be written."""
    if not os.path.exists(LEADF): return []
    import re
    leads = [l[2:].strip() for l in open(LEADF) if l.startswith("- ")]
    gen = json.load(open(GEN)) if os.path.exists(GEN) else []; have = {r[0] for r in gen}; keys = []
    for l in leads:
        k = next((v for p_, v in new_ideas_more.LEADS.items() if l.startswith(p_)), None)
        if not k:
            k = "lead-auto-" + re.sub(r"[^a-z]+", "-", l.lower())[:30].strip("-")
            if k not in have:
                words = re.sub(r"[^A-Za-z ]", "", l).split()[:3]; lab = " ".join(w.capitalize() for w in words)[:20]
                desc = ""
                for w in l.split():
                    if len(desc) + len(w) + 1 > 28: break
                    desc = (desc + " " + w).strip()
                gen.append((k, "Research Leads", "new", "Worth exploring this lead?", f"{lab}|{desc.rstrip('.,:;')}|photo|Research lead;house",
                            "Park It For Later|Keep it on the list|checks|Saved;Revisit later"))
                json.dump(gen, open(GEN, "w"), indent=1, ensure_ascii=False); print("new lead auto-paired:", k, file=sys.stderr)
        keys.append(k)
    return keys
lead_keys = read_leads()
bank = load_bank()
dry = "--dry" in sys.argv
if "--refill" in sys.argv: bank = refill(bank); print(len(bank), "pairs,", len([e for e in bank if e[0] not in hist["shown"]]), "unshown"); sys.exit()
rebuild = sys.argv[sys.argv.index("--rebuild") + 1] if "--rebuild" in sys.argv else None
byk = {e[0]: e for e in bank}
if rebuild:
    old = json.load(open(f"decks/{rebuild}.json")); pick = [byk[k] for k in old["idea_keys"]]
    did = rebuild; slug = json.load(open("decks/pages.json"))[did]; name = old["title"]; theme = old["theme"]
    tw = [x.strip() for x in theme.replace("&", ",").split(",")]
else:
    bank = refill(bank)
    fresh = [e for e in bank if e[0] not in hist["shown"]]
    rng = random.Random(); rng.shuffle(fresh); pick, seen = [], set()
    for e in [e for e in fresh if e[0] in lead_keys][:2]: pick.append(e); seen.add(e[1])
    for e in sorted(fresh, key=lambda e: e[2] != "new"):
        if e[1] not in seen and len(pick) < 10: pick.append(e); seen.add(e[1])
    for e in fresh:
        if len(pick) < 10 and e not in pick: pick.append(e)
    if any(is_upkeep(e) for e in pick):  # R110: UpKeep and Thai never in the same deck
        pick = [e for e in pick if not is_thai(e)]
        for e in [e for e in fresh if not is_thai(e) and e not in pick]:
            if len(pick) >= 10: break
            if e[1] not in {x[1] for x in pick} or len(pick) >= 8: pick.append(e)
    sp = [e[1] for e in pick if e[2] == "spinoff"]; nw = [e[1] for e in pick if e[2] != "spinoff"]
    themes = []
    for th in sp[:2] + nw[:1] + sp[2:] + nw[1:]:
        if th not in themes: themes.append(th)
    def short(th): return {"@AMomentInThai": "YouTube", "Smart Upkeep": "Upkeep", "Weberman Construction": "Construction"}.get(th, th)
    tw = [short(x) for x in themes[:3]]
    theme = f"{tw[0]}, {tw[1]} & {tw[2]}"; name = f"New Ideas: {theme}"
    tslug = "-".join("".join(c for c in w.lower() if c.isalnum() or c == " ").replace(" ", "-") for w in tw)
    suf = "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
    did = f"new-ideas-{tslug}-{suf}"; slug = did
assert not (any(is_upkeep(e) for e in pick) and any(is_thai(e) for e in pick)), "R110: UpKeep and Thai in one deck"
if dry: print(name, [p[0] for p in pick], len(bank), "pairs in bank"); sys.exit()
pairs, O, add = kdeck("ni-", "Research")
for key, th, kind, ask, a, b in pick:
    opts = []
    for o in (a, b):
        assert len(o[1]) <= 20 and len(o[2]) <= 28, o[:3]
        opts.append(O(f"{key}-{o[0]}", o[1], o[2], "practical", fill_card(th, o[3], o[4]), tags=[th, kind]))
    add(th, th, opts[0], opts[1], r105_ask(th, ask))
caption_rule.guard(pairs, "new-ideas")
assert not (any(is_upkeep(e) for e in pick) and any(is_thai(e) for e in pick)), "R110: UpKeep and Thai in one deck"
meta = {"brands": ["Research"], "submit_agent": "research", "topic": "new-ideas", "deck_size": 10, "board": "research", "audience": "Max",
        "rule": "R101 Daily New Ideas deck", "signoff": {k: v for k, v in new_ideas_more.SIGNOFF.items() if k in [p[0] for p in pick]}, "idea_keys": [p[0] for p in pick], "theme": theme,
        "claims": "Real claims only; no market numbers.", "sources": {"bank": "tools/new_ideas_bank.py", "history": HIST,
        "steer": ["research-dashboard topics.json decisions", "ops/agent-activity/preferences-log.md", "ops/submit/inbox/**"]}}
publish(did, name, "Research", pairs, meta, seed=secrets.randbelow(10**6), n=10)
dj = json.load(open(f"decks/{did}.json")); assert len(dj["pairs"]) == 10
src = open("tools/build_upkeep_five_decks.py").read(); ns = {}; exec(src[src.index("SHARE = ("):src.index("FEEL = {")], ns)
HEAD = f'''<base href="../">
    <meta name="robots" content="noindex">
    <script>window.DEFAULT_DECK="{did}"</script>
    <style>:root{{--bg:#FFFFFF}}html,body{{background:#FFFFFF!important}}*{{border-radius:0!important}}.card,.opt,.vis{{border-radius:10px!important}}body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}}body.carding .opt .vis{{min-height:0;overflow:visible}}body.carding .opt .vis .v-svg svg{{min-height:0!important}}html body .vis svg.ni-m{{display:none!important}}@media(max-width:600px){{html body .vis svg.ni-d{{display:none!important}}html body .vis svg.ni-m{{display:block!important}}}}</style>
    {ns["SHARE"]}'''
s = open("index.template.html").read().replace("<head>", "<head>\n" + HEAD, 1).replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11")
os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(s); link_patch(p)
pages = json.load(open("decks/pages.json")); pages[did] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
now = dj["generated_at"]
for e in pick: hist["shown"][e[0]] = {"deck": did, "at": hist["shown"].get(e[0], {}).get("at", now), "A": e[4][1], "B": e[5][1]}
if not any(d["id"] == did for d in hist["decks"]): hist["decks"].append({"id": did, "name": name, "slug": slug, "at": now})
json.dump(hist, open(HIST, "w"), indent=1, ensure_ascii=False)
rec = {"id": did, "name": name, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "total": 10, "topic": "new-ideas", "added": now,
       "tag": "New Ideas", "blurb": "10 idea picks: " + ", ".join(tw), "pairs": [f'{p["optionA"]["label"]} vs {p["optionB"]["label"]}' for p in dj["pairs"]]}
print(json.dumps(rec, indent=1, ensure_ascii=False))
