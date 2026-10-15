#!/usr/bin/env python3
"""Oct 15 2026 19:39 ICT: UpKeep's new pairs (smartkeep/decks/new-pairs-video.md, new-pairs-order-form.md) -> source banks for
Video and Order Form refills (carried skips go first via ready_shelf), plus Clear Picks Deck (App Design + Plans clashes re-asked
head to head, padded with UpKeep's leftover new pairs). Writes banks/src-upkeep-{video-next,order-form-next,clear-picks}.json."""
import sys, os, re, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from team_kit import deck, TERRA, LAGOON, JUNGLE, SAFFRON, INK
def asks(f): return [re.sub(r"^\d+\.\s*", "", l).strip() for l in open(f) if re.match(r"^\d+\.", l)]
def split(q):
    g, rest = q.split(":", 1) if ":" in q else ("", q); rest = rest.strip().rstrip("?")
    a, b = re.split(r"\s+Or\s+", rest, 1); return g.strip(), a.strip(), b.strip()
def sid(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:14]
play = lambda c=SAFFRON: ("raw", f'<rect x="14" y="0" width="212" height="118" rx="8" fill="{c}22"/><circle cx="120" cy="59" r="20" fill="{c}"/><path d="M114 49 L130 59 L114 69 Z" fill="#fff"/>', 126)
def vis(kind, g, lab, c):
    if kind == "video": return [("hdr", "Smart Upkeep", "Video", SAFFRON, "logo", "S"), play(c), ("word", lab[:28], 18, INK, g[:30])]
    return [("hdr", "Smart Upkeep", "Order Form", SAFFRON, "logo", "S"), ("lbl", g.upper()[:30]), ("cards", [(lab[:30], "", "")], c, "dot", "line", 40), ("btn", "Join Plus", "fill", SAFFRON)]
def from_md(f, prefix, kind, group):
    pairs, O, add = deck(prefix, "UpKeep")
    for i, q in enumerate(asks(f), 1):
        g, a, b = split(q)
        add(group, group, O(f"{i:02d}a_{sid(a)}", a, g, "calm", vis(kind, g, a, LAGOON)), O(f"{i:02d}b_{sid(b)}", b, g, "focused", vis(kind, g, b, TERRA)), q)
    assert len(pairs) == 20, (f, len(pairs)); return pairs
vp = from_md("/workspace/smartkeep/decks/new-pairs-video.md", "vnx_", "video", "Video")
op = from_md("/workspace/smartkeep/decks/new-pairs-order-form.md", "ofx_", "form", "Order Form")
VID, ORD = vp[:15], op[:19]   # 5 + 15 and 1 + 19 with the carried skips
cp, O, add = deck("clr_", "UpKeep")
HD = {"Centered Header": ("hdr", "Smart Upkeep", "Home Record", SAFFRON, "center"), "Color Band Header": ("hdr", "Smart Upkeep", "Home Record", LAGOON, "band"),
      "Big Title Header": ("word", "Home Record", 30, INK, ""), "Plain Header": ("hdr", "Smart Upkeep", "Home Record", INK, "plain")}
body = [("cards", [("Gas Furnace", "Tuned Sep 2026", ""), ("Central AC", "Tuned Apr 2026", "")], None, "dot", "line", 30)]
hs = list(HD)
for i, (a, b) in enumerate([(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]):
    A, B = hs[a], hs[b]
    add("Clear Picks", "Header Style", O(f"hd{i}a_{sid(A)}", A.replace(" Header", ""), "App header, head to head.", "calm", [HD[A]] + body),
        O(f"hd{i}b_{sid(B)}", B.replace(" Header", ""), "App header, head to head.", "focused", [HD[B]] + body), f"App Header, Head To Head: {A.replace(' Header','')} Or {B.replace(' Header','')}?")
HL = {"Label Plus Headline": [("lbl", "YOUR APPLIANCES"), ("word", "Home Record", 22, INK, "")], "Big Headline": [("word", "Home Record", 30, INK, "")],
      "Tinted Title Box": [("banner", "Home Record", SAFFRON, "home")], "Side Rule Headline": [("hdr", "Home Record", "", TERRA, "bar")]}
for i, (A, B) in enumerate([("Label Plus Headline", "Big Headline"), ("Tinted Title Box", "Side Rule Headline"), ("Label Plus Headline", "Tinted Title Box")]):
    add("Clear Picks", "Headline Style", O(f"hl{i}a_{sid(A)}", A, "Section headline.", "calm", HL[A] + body), O(f"hl{i}b_{sid(B)}", B, "Section headline.", "focused", HL[B] + body), f"Section Headline, Head To Head: {A} Or {B}?")
MN = {"Top Pill Tabs": [("tabs", ["Appliances", "Scan", "Recalls"], "pill")] + body, "Bottom Tabs": [("word", "Home Record", 20, INK, "")] + body + [("nav",)],
      "Side Menu": [("cards", [("Appliances", "", ""), ("Moisture Scan", "", ""), ("Recalls", "", ""), ("Proof Pack", "", "")], LAGOON, "dot", "line", 26)],
      "Swipe Pages": body + [("dots", 4, 1, INK)]}
for i, (A, B) in enumerate([("Top Pill Tabs", "Bottom Tabs"), ("Side Menu", "Swipe Pages"), ("Top Pill Tabs", "Side Menu")]):
    add("Clear Picks", "Menu Type", O(f"mn{i}a_{sid(A)}", A, "How you move between sections.", "calm", MN[A]), O(f"mn{i}b_{sid(B)}", B, "How you move between sections.", "focused", MN[B]), f"Menu Type, Head To Head: {A} Or {B}?")
add("Clear Picks", "Member Home", O("mh_big", "Big House Picture", "Picture fills the top of member Home.", "visual", [("photo", 130, LAGOON, "house", "Your Home")]),
    O("mh_banner", "Small Banner", "Thin picture strip, plan and visit below.", "calm", [("photo", 46, LAGOON, "house", ""), ("cards", [("Next Visit", "Winter Visit", "")], None, "dot", "line", 30)]),
    "Member Home, Pick One: Big House Picture Or Small Banner?")
add("Clear Picks", "Add-Ons", O("ao_under", "Under The Plans", "Add-ons listed below the plan cards.", "calm", [("cards", [("Plus", "Most Popular", "")], SAFFRON, "dot", "line", 34), ("cards", [("Chimney Sweep", "", "+$/month")], None, "dot", "line", 28)]),
    O("ao_step", "Separate Step", "Pick a plan, then a step just for add-ons.", "focused", [("steps", ["Plan", "Add-Ons", "Details", "Pay"], TERRA, 2), ("cards", [("Chimney Sweep", "", "+$/month")], None, "dot", "line", 28)]),
    "Add-Ons, Pick One: Under The Plans Or A Separate Step?")
CLR = cp + vp[15:] + op[19:]
assert len(CLR) == 20, len(CLR)
for n, ps in (("upkeep-video-next", VID), ("upkeep-order-form-next", ORD), ("upkeep-clear-picks", CLR)):
    json.dump({"pairs": ps}, open(f"banks/src-{n}.json", "w"), indent=1, ensure_ascii=False); print(n, len(ps))
