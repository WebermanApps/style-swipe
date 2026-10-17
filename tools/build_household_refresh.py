#!/usr/bin/env python3
"""Household refresh (Branding, Oct 17 2026): builds the 11 fresh 10-pick Household decks in tools/household_refresh_content.py.
Visuals: real Commons photos (tools/household_refresh_media.py -> img/household/), real CC0 artworks from the Art Institute of Chicago
(tools/build_art_deck.fetch -> img/art/) and clean drawn cards (tools/household_refresh_svg.py). Light only, square corners,
#E3DDD2 borders, Khand + Hind. R105 captions (tools/caption_rule.py), Notes + Share on every pick, submit -> Household.
Deck pages: committed index.template.html + committed agent_links/chat_button blocks (Return/back links go to the Household board).
usage: build_household_refresh.py   -> prints one {deckId, name, slug, url} line per deck; pages are written UNLOCKED, lock before commit."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import media_rule; media_rule.guard()
import os, sys, json, string, secrets, subprocess, types
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from team_kit import deck as kdeck, publish
from draft_svg import TERRA, LAGOON, JUNGLE, SAFFRON
import caption_rule, household_refresh_media as media, household_refresh_svg as S
from household_refresh_content import DECKS
import build_art_deck
def aic(aid):  # build_art_deck.fetch, with a 600px fallback for works whose IIIF image is smaller than 843px (403 otherwise)
    try: return build_art_deck.fetch(aid)
    except Exception:
        _g = build_art_deck.get
        build_art_deck.get = lambda u: _g(u.replace("/full/843,/", "/full/600,/"))
        try: return build_art_deck.fetch(aid)
        finally: build_art_deck.get = _g
from chat_button import patch as chat_patch
def committed(path): return subprocess.run(["git", "show", "HEAD:" + path], capture_output=True, text=True, check=True).stdout
# committed agent_links (another worker may have uncommitted edits in the working tree)
_al = types.ModuleType("agent_links_committed"); _al.__file__ = os.path.join(ROOT, "tools", "agent_links.py")
exec(compile(committed("tools/agent_links.py").split('if __name__ == "__main__":')[0], "agent_links.py", "exec"), _al.__dict__)
TEMPLATE = committed("index.template.html")
ACC = [TERRA, LAGOON, JUNGLE, SAFFRON]
SL = "queue/household-slugs.json"
META = {"submit_agent": "household", "submit_to": "Household Agent", "agent_id": "c59ffdde-28bf-4ad7-8dd8-22f5e941647d", "deck_size": 10,
        "board": "household", "audience": "Max and Nozomi", "caption_rule": "R105", "round": "household-refresh-2026-10-17"}
CSS = (":root{--bg:#FFFFFF;--line:#E3DDD2}html,body{background:#FFFFFF!important}"
       "html body .card.card,html body .opt.opt,html body .vis.vis,html body .stamp.stamp,html body .carding .card{border-radius:0!important}.vis{background:#FAF6EE!important}"
       "body.carding .opt .vis svg,body.carding .opt .vis .v-svg svg,.v-svg svg,.opt .vis svg{width:100%!important;height:auto!important;max-height:none!important;max-width:100%!important;flex:0 0 auto!important}"
       "body.carding .opt .vis{min-height:0;overflow:visible}")
def build(D, photos, k):
    short = "".join(w[0] for w in D["id"].split("-")[1:])[:6]
    pairs, O, add = kdeck(f"hhr{short}_", "Household")
    for i, (g, loc, el, sent, a, b) in enumerate(D["pairs"]):
        acc = ACC[(i + k) % 4]; opts = []
        for key, label, desc, feel, (kind, ref), chips in (a, b):
            cred = None
            if kind == "p":
                c = photos[ref]; svg = S.photo_card(c, label, desc, acc)
                cred = {"title": c["title"][5:], "author": c["author"].split("\n")[0][:80], "license": c["license"], "license_url": c["license_url"], "source": c["source"]}
            elif kind == "a":
                c = aic(ref); svg = S.art_card(c, label, desc, acc)
                cred = {x: c[x] for x in ("title", "artist", "date", "license", "source")}
            else: svg = S.drawn_card(g, label, desc, ref, chips, acc)
            o = O(key, label, desc, feel, svg, tags=[g.lower()])
            if cred: o["credit"] = cred
            opts.append(o)
        add(g, g, opts[0], opts[1], f"{loc}: {el}, {sent}")
    caption_rule.guard(pairs, D["id"]); assert len(pairs) == 10, (D["id"], len(pairs))
    publish(D["id"], D["name"], "Household", pairs, {**META, "brands": [D["brief"], "Household help for Max, Nozomi and Maple. Fresh picks only: nothing repeats an earlier Household deck or the board's Jakarta trip cards."],
            "topic": D["topic"], "tag": D["tag"]}, seed=1017 + k, n=10)
    dj = json.load(open(f"decks/{D['id']}.json")); assert len(dj["pairs"]) == 10
    slugs = json.load(open(SL))
    if D["id"] not in slugs: slugs[D["id"]] = D["id"].replace("household-", "household-", 1) + "-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6)); json.dump(slugs, open(SL, "w"), indent=1)
    slug = slugs[D["id"]]
    head = f'<base href="../">\n<meta name="robots" content="noindex">\n<script>window.DEFAULT_DECK="{D["id"]}"</script>\n<style>{CSS}</style>\n'
    os.makedirs(slug, exist_ok=True); p = os.path.join(slug, "index.html"); open(p, "w").write(TEMPLATE.replace("<head>", "<head>\n" + head, 1))
    _al.patch(p); chat_patch(p); h = open(p).read().replace("mw-chat.js?v=cc9", "mw-chat.js?v=cc11"); open(p, "w").write(h)
    pages = json.load(open("decks/pages.json")); pages[D["id"]] = slug; json.dump(pages, open("decks/pages.json", "w"), indent=1, ensure_ascii=False)
    return {"deckId": D["id"], "name": D["name"], "slug": slug, "url": f"https://webermanapps.github.io/style-swipe/{slug}/", "tag": D["tag"], "topic": D["topic"]}
if __name__ == "__main__":
    photos = media.all_photos(); only = set(sys.argv[1:])
    out = [build(D, photos, k) for k, D in enumerate(DECKS) if not only or D["id"] in only]
    json.dump(out, open("queue/household-refresh-built.json", "w"), indent=1)
    for r in out: print(json.dumps(r))
