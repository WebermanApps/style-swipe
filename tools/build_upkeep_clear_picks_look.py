#!/usr/bin/env python3
"""Oct 15 2026 20:06 ICT: 3 member-app look cards for Clear Picks Deck (based on smartkeep/member-app/polish/after/).
Replaces padding pairs vnx 16/18/19, which go back into banks/src-upkeep-video-next.json (stay queued for the next Video refill)."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import team_kit
from team_kit import deck, LAGOON, SAFFRON, INK, MUTE
from PIL import Image
def b_img(y, name):
    w0, h0 = Image.open(f"img/smartkeep-member/{name}.png").size; h = round(212 * h0 / w0); src = f"img/smartkeep-member/{name}.png"
    return f'<image href="{src}" xlink:href="{src}" x="14" y="{y}" width="212" height="{h}" preserveAspectRatio="xMidYMid meet"/>', h + 6
team_kit.BLK["img"] = b_img
pairs, O, add = deck("clk_", "UpKeep"); HD = ("hdr", "Smart Upkeep", "Member App", SAFFRON, "logo", "S")
dyk = lambda c: [HD, ("lbl", "DID YOU KNOW?", c), ("p", "A spring AC tune-up can catch a weak capacitor before the first heat wave."), ("lbl", "NEXT VISIT", MUTE), ("cards", [("Winter Visit", "Dec 8 to Dec 12, 2026", "")], None, "dot", "line", 34)]
add("Member App Look", "Labels", O("dyk_lagoon", "Lagoon Accent", "\"Did You Know?\" in lagoon, as in the polished app.", "visual", dyk(LAGOON)),
    O("dyk_grey", "Grey Caps", "Same grey caps as Your Plan and Next Visit.", "calm", dyk(MUTE)), "\"Did You Know?\" Label: Lagoon Accent Or Grey Caps Like The Other Labels?")
row = lambda btn: [HD, ("lbl", "ADD-ONS", MUTE), ("cards", [("Exterior Window Washing", "+$19/month", "")], None, "dot", "line", 30), btn, ("cards", [("Chimney Sweep", "+$21/month", "")], None, "dot", "line", 30), btn]
add("Member App Look", "Buttons", O("add_saff", "Saffron", "Filled saffron Add buttons on desktop.", "visual", row(("btn", "Add", "fill", SAFFRON))),
    O("add_lag", "Lagoon Outline", "Quieter lagoon outline Add buttons.", "calm", row(("btn", "Add", "outline", LAGOON))), "Add Buttons On Desktop: Saffron Or A Quieter Lagoon Outline?")
add("Member App Look", "Desktop Backdrop", O("bd_plain", "Plain Light Cream", "Flat cream behind the app frame.", "calm", [("img", "backdrop-plain")]),
    O("bd_tex", "Subtle Texture", "Faint diagonal pattern behind the app frame.", "visual", [("img", "backdrop-texture")]), "Desktop Backdrop Behind The App Frame: Plain Light Cream Or A Subtle Texture?")
src = json.load(open("banks/src-upkeep-clear-picks.json"))["pairs"]
drop = [p for p in src if p["optionA"]["id"].startswith(("vnx_16", "vnx_18", "vnx_19"))]; assert len(drop) == 3
keep = [p for p in src if p not in drop]; new = keep + pairs; assert len(new) == 20
json.dump({"pairs": new}, open("banks/src-upkeep-clear-picks.json", "w"), indent=1, ensure_ascii=False)
v = json.load(open("banks/src-upkeep-video-next.json"))
if not any(p["optionA"]["id"].startswith("vnx_16") for p in v["pairs"]): v["pairs"] += drop
json.dump(v, open("banks/src-upkeep-video-next.json", "w"), indent=1, ensure_ascii=False)
print(len(new), len(v["pairs"]))
