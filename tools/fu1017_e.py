"""Follow-ons E (Oct 17 2026): WellNest Tea Energy Line recipe, Grok Bot Follow-Through, Branding Mixed Deck: Up Keep next round."""
import os, json, re
from fu1017_kit import *
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
from team_kit import wrap, shareic
from wn_guard import blocked as wn_blocked
import base64; _ns = dict(globals()); _ns["base64"] = base64; _src = open("tools/build_wn_tea.py").read(); exec(_src[_src.index("_src = open"):_src.index("def head(")], _ns)
wsvg, wlabel, IMGF = _ns["svg"], _ns["label"], _ns["img"]
WN = "WellNest Agent e2806a26-3867-4986-a7ef-46c03abc7f35"
GREEN = "#5E8A3A"; LEMON = "#C9A227"
# ---------- WellNest drawn scenes (same 16,40,208x120 window as the tea deck) ----------
def win(inner): return rect(16, 40, 208, 120, "#F3EEE4", LINE) + inner + t(214, 155, "mockup", 6, "#8A8580", "hind", 400, "end")
def leafpile(cx, cy, n, c, r=5):
    return "".join(f'<ellipse cx="{cx + ((i * 37) % 23) - 11}" cy="{cy + ((i * 17) % 13) - 6}" rx="{r}" ry="{r*.45}" fill="{c}" transform="rotate({(i*47)%180} {cx + ((i * 37) % 23) - 11} {cy + ((i * 17) % 13) - 6})"/>' for i in range(n))
def bowl(cx, cy, w, fill_):
    return f'<path d="M{cx-w/2} {cy} Q{cx} {cy+w*.55} {cx+w/2} {cy} Z" fill="#FFFFFF" stroke="#B9A98C"/>' + fill_
def ratio(herb_share):
    # a blend split into tea leaf (dark) and herbs (green/yellow), drawn as one jar with layers + two bowls
    hl = 90 * herb_share
    s = '<path d="M96 58 H144 Q150 58 150 64 V150 H90 V64 Q90 58 96 58 Z" fill="#E9F0EE" stroke="#9FB2AE"/>' + rect(99, 48, 42, 10, "#3A3A3A")
    s += rect(92, 150 - hl, 56, hl, GREEN + "CC") + rect(92, 60, 56, 90 - hl, "#5B4632") + leafpile(120, 150 - hl / 2, 6, LEMON, 4)
    s += t(170, 80, f"{round(herb_share*100)}% herbs", 10, GREEN, "khand", 700) + t(170, 96, f"{round((1-herb_share)*100)}% oolong", 10, "#5B4632", "khand", 700) + t(170, 112, "by weight", 7, MUTE)
    return win(s)
def gingercut(kick):
    n = 6 if kick else 2
    s = bowl(80, 100, 80, "") + leafpile(80, 92, 10, GREEN, 5) + "".join(f'<circle cx="{60 + (i*13)%40}" cy="{88 + (i*7)%10}" r="5" fill="#E2C48A" stroke="#B48D5F"/>' for i in range(n))
    s += t(140, 84, "Ginger slices:", 9, INK, "hind", 600) + t(140, 104, "a hint" if not kick else "a clear kick", 14, "#B48D5F", "khand", 700) + t(140, 120, f"{n} slices per jar (drawn)", 7, MUTE)
    return win(s)
def moringaform(powder):
    s = bowl(84, 96, 90, "")
    s += (f'<ellipse cx="84" cy="98" rx="34" ry="8" fill="{GREEN}"/>' + "".join(f'<circle cx="{60 + (i*11)%48}" cy="{94 + (i*5)%8}" r="1" fill="#3E6A24"/>' for i in range(20))) if powder else leafpile(84, 92, 14, GREEN, 4)
    s += t(146, 86, "Fine powder" if powder else "Dried leaf flakes", 12, INK, "khand", 700) + t(146, 102, "clouds the cup, strong" if powder else "clear cup, softer", 8, MUTE) + t(146, 114, "green" if powder else "green taste", 8, MUTE)
    return win(s)
def serve(iced):
    if iced:
        s = '<path d="M98 56 H142 L136 150 H104 Z" fill="#EAF2E4" stroke="#9FB2AE"/>' + rect(104, 90, 32, 58, "#C9B45A99") + "".join(rect(108 + (i % 2) * 12, 74 + i * 12, 10, 10, "#FFFFFFCC", "#BFD3D9") for i in range(3)) + f'<path d="M132 52 L126 140" stroke="{GREEN}" stroke-width="3"/>'
        lab = ("Iced", "over ice")
    else:
        s = f'<path d="M92 92 H148 Q148 146 120 146 Q92 146 92 92 Z" fill="#FFFFFF" stroke="#B9A98C"/><path d="M148 102 q14 0 12 14 q-2 10 -14 8" fill="none" stroke="#B9A98C" stroke-width="3"/>' + rect(96, 96, 48, 10, "#C9B45A") + "".join(f'<path d="M{108+i*12} 86 q-6 -10 0 -18 q6 -8 0 -16" stroke="#C9BFAE" stroke-width="2" fill="none"/>' for i in range(3))
        lab = ("Hot", "a morning mug")
    return win(s + t(184, 92, lab[0], 16, INK, "khand", 700, "middle") + t(184, 108, lab[1], 7.5, MUTE, "hind", 400, "middle"))
def mypack(kind, name, sub, extra, band=None, extra_c=MUTE):
    s = rect(16, 40, 208, 120, "#F3EEE4", LINE); cx = 120
    if kind == "pouch": s += '<path d="M72 50 H168 L172 156 H68 Z" fill="#C9A274" stroke="#9C7A52"/>' + rect(72, 50, 96, 6, "#B48D5F")
    else: s += rect(72, 58, 96, 96, "#D8D4CC", "#8F8A82") + rect(69, 50, 102, 12, "#BDB8AF", "#8F8A82")
    s += rect(76, 72, 88, 74, "#FAF6EE", "#C9BFAE")
    if band: s += rect(76, 72, 88, 7, band)
    s += t(cx, 96, name, 12, INK, "khand", 600, "middle") + t(cx, 107, sub, 7.5, MUTE, "hind", 500, "middle")
    for i, l in enumerate(extra): s += t(cx, 121 + i * 10, l, 7.5, extra_c, "hind", 600, "middle")
    return s + t(214, 155, "mockup", 6, "#8A8580", "hind", 400, "end")
def bags():
    s = "".join(f'<path d="M{70+i*36} 140 L{86+i*36} 104 L{102+i*36} 140 Z" fill="#F5EFE2" stroke="#B9A98C"/>' + leafpile(86 + i * 36, 128, 4, GREEN, 3) + f'<path d="M{86+i*36} 104 V86" stroke="#B9A98C"/>' + rect(80 + i * 36, 76, 12, 10, GREEN) for i in range(3))
    return win(s + t(200, 96, "Pyramid", 9, INK, "hind", 600, "end") + t(200, 108, "bags", 9, INK, "hind", 600, "end"))
def steeps(two):
    s = ""
    for i in range(2 if two else 1):
        x = 60 + i * 80
        s += f'<path d="M{x} 92 H{x+44} Q{x+44} 136 {x+22} 136 Q{x} 136 {x} 92 Z" fill="#FFFFFF" stroke="#B9A98C"/>' + rect(x + 4, 96, 36, 8, "#C9B45A") + t(x + 22, 80, ["1st steep", "2nd steep"][i], 8, INK, "hind", 600, "middle") + t(x + 22, 150, ["95C, 4 min", "95C, 6 min"][i], 7, MUTE, "hind", 400, "middle")
    if not two: s += t(130, 112, "One cup only", 9, MUTE)
    return win(s)
def W(gi, side, group, label, desc, facts, scene, feel):
    acc = ["#0A0A0A", "#6B6256"][(gi + side) % 2]
    s = rect(0, 0, 240, 300, "#FFFFFF") + rect(0, 0, 240, 5, acc) + t(16, 28, group.upper(), 10.5, acc, "hind", 600, "start", 'letter-spacing="1.2"') + shareic(206, 15, INK, 15)
    s += IMGF(scene[4:]) if scene.startswith("img:") else scene
    y = 186
    for l in wrap(label, 18)[:2]: s += t(16, y, l, 22, INK, "khand"); y += 23
    for l in wrap(desc, 34)[:2]: s += t(16, y, l, 12.5, MUTE); y += 16
    y = max(y + 2, 254); x = 16
    for f in facts[:2]:
        w = min(104, 18 + len(f) * 6.2); s += rect(x, y, w, 22, "#F6F1E8", LINE) + t(x + 8, y + 15, f, 11, INK, "hind", 600); x += w + 6
    s += t(120, 292, "Built by Machan", 8, "#8A8580", "hind", 400, "middle")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" style="max-width:100%;height:auto">{s}<rect x=".5" y=".5" width="239" height="299" fill="none" stroke="#e3ddd2"/></svg>'
WNP = []
def wp(group, ask, a, b, feels=("calm", "practical")):
    gi = len(WNP); WNP.append((group, ask, opt("fuwn_" + a[0], a[1], a[2], feels[0], W(gi, 0, group, a[1], a[2], a[3], a[4], feels[0])), opt("fuwn_" + b[0], b[1], b[2], feels[1], W(gi, 1, group, b[1], b[2], b[3], b[4], feels[1]))))
wp("Energy Line", "Gentle Lift Recipe: Mostly Herbs With A Little Oolong, Or Half Oolong, Half Herbs?",
   ("mostlyherbs", "Mostly Herbs", "About two thirds herbs, a little leaf.", ["Gentlest", "Herb-led"], ratio(.67)),
   ("halfhalf", "Half And Half", "Even split, more tea taste.", ["Balanced", "More leaf"], ratio(.5)))
wp("Energy Line", "You Kept Both Moringa And Ginger: Ginger As A Warm Hint, Or A Clear Spicy Kick?",
   ("gingerhint", "Ginger As A Hint", "Moringa leads, ginger in the finish.", ["Soft", "Green first"], gingercut(False)),
   ("gingerkick", "Ginger Kick", "Ginger you taste from the first sip.", ["Spicy", "Wake-up"], gingercut(True)), ("calm", "bold"))
wp("Energy Line", "Third Herb Next To Lemongrass: Pandan For A Soft Sweet Note, Or Thai Basil For A Fresh Lift?",
   ("pandan", "Pandan Leaf", "Soft, sweet, vanilla-like note.", ["Sweet note", "Very Thai"], "img:pandan"),
   ("thaibasil", "Thai Basil", "Fresh, peppery, bright.", ["Fresh", "Peppery"], "img:thaibasil"), ("calm", "playful"))
wp("Energy Line", "Moringa In The Blend: Dried Leaf Flakes, Or Fine Moringa Powder?",
   ("flakes", "Dried Leaf Flakes", "Clear cup, softer green taste.", ["Clear cup", "Loose leaf"], moringaform(False)),
   ("powder", "Fine Powder", "Cloudy cup, stronger green taste.", ["Strong green", "Cloudy"], moringaform(True)))
wp("Energy Line", "Energy Line Serve: A Hot Morning Mug, Or Iced For Hot Afternoons?",
   ("hot", "Hot Morning Mug", "Steeped hot, sipped slowly.", ["Hot", "Morning"], serve(False)),
   ("iced", "Iced", "Brewed strong, poured over ice.", ["Iced", "Afternoon"], serve(True)), ("calm", "playful"))
wp("Sourcing", "Pack Story, Since You Picked Our Own Farm First: Name Each Source, Or One Line For The Blend?",
   ("namesource", "Name Each Source", "Herbs from our farm; oolong from a named grower.", ["Honest detail", "Story"], mypack("pouch", "Energy Line", "WellNest", ["Herbs: our farm", "Oolong: Thai grower"])),
   ("oneline", "One Line For The Blend", "'Blended at WellNest, Chiang Mai.'", ["Simple", "Short"], mypack("pouch", "Energy Line", "WellNest", ["Blended at WellNest", "Chiang Mai"])), ("premium", "practical"))
wp("Label Info", "Oolong Has Caffeine: A Plain 'Contains Tea Caffeine' Line, Or A Small Leaf Strength Scale?",
   ("cafline", "Plain Caffeine Line", "One clear line on the front.", ["Plain", "Clear"], mypack("tin", "Energy Line", "WellNest", ["Contains tea", "caffeine"], GREEN, "#2E5FA8")),
   ("cafscale", "Leaf Strength Scale", "One to three leaves; Energy shows two.", ["Visual", "Compare lines"], mypack("tin", "Energy Line", "WellNest", ["Strength:", "2 of 3 leaves"], GREEN)))
wp("Label Look", "Energy Line Colour: Leaf Green Band, Or Lemongrass Yellow Band?",
   ("bandgreen", "Leaf Green Band", "Green for moringa and leaf.", ["Green", "Fresh"], mypack("tin", "Energy Line", "WellNest", ["moringa, lemongrass,", "ginger"], GREEN)),
   ("bandyellow", "Lemongrass Yellow Band", "Sunny yellow, a morning feel.", ["Yellow", "Sunny"], mypack("tin", "Energy Line", "WellNest", ["moringa, lemongrass,", "ginger"], LEMON)), ("calm", "bold"))
wp("Container", "Energy Line Format: Loose Leaf In A Tin, Or Pyramid Bags?",
   ("loosetin", "Loose Leaf Tin", "Scoop it; shows the whole leaves.", ["Loose", "Refillable"], mypack("tin", "Energy Line", "Loose leaf", ["about 20 cups", "(example)"], GREEN)),
   ("pyramid", "Pyramid Bags", "One bag, one mug; easy at work.", ["Quick", "On the go"], bags()), ("premium", "practical"))
wp("Label Info", "Brew Guide: One Steep, Or Say The Oolong Can Be Steeped Twice?",
   ("onesteep", "One Steep", "Simple: one cup per serve.", ["Simple", "One cup"], steeps(False)),
   ("twosteeps", "Steep It Twice", "Second cup from the same leaves.", ["Better value", "Tea habit"], steeps(True)))
for g_, ask, a, b in WNP:
    assert not wn_blocked({"ask": ask, "optionA": {"label": a[1], "desc": a[2]}, "optionB": {"label": b[1], "desc": b[2]}, "group": g_}, False), ask
# ---------- Grok Bot Follow-Through ----------
GB = LAGOON
def gh(y=30, sub="Promise list"):
    return f'<circle cx="25" cy="{y+12}" r="10" fill="{GB}"/>' + t(25, y + 16, "G", 11, "#FFFFFF", "khand", 700, "middle") + t(40, y + 11, "Grok Bot", 11, INK, "khand", 700) + t(40, y + 21, sub, 7.5, MUTE) + shareic(208, y + 5) + ln(y + 28)
def prow(y, txt, due, c=INK, tag_=None, agent=None, pct=None):
    s = rect(14, y, 212, 38, "#FFFFFF", LINE, 6) + t(22, y + 16, txt, 10, INK, "hind", 600) + t(22, y + 30, due, 8.5, c)
    if agent: s += rect(218 - len(agent) * 4.6 - 8, y + 8, len(agent) * 4.6 + 8, 12, SOFT, "none", 6) + t(218 - len(agent) * 2.3 - 4, y + 15, agent, 7, INK, "hind", 600, "middle")
    if tag_: s += tag_
    if pct is not None: s += rect(120, y + 26, 98, 4, LINE, "none", 2) + rect(120, y + 26, 98 * pct, 4, GB, "none", 2)
    return s
def late_tag(x, y, style):
    if style == "red": return rect(x, y, 30, 12, TERRA) + t(x + 15, y + 9, "LATE", 7, "#FFFFFF", "hind", 600, "middle")
    return dot(x + 4, y + 6, 3.5, SAFFRON) + t(x + 10, y + 9, "late 2h", 7, "#7A5A0C", "hind", 600)
def chatb(y, txt, me=False, w=150, h=None):
    lines = wrap(txt, 30); h = h or 14 + len(lines) * 12; x = 226 - w if me else 14
    return rect(x, y, w, h, "#FFFFFF" if not me else GB + "18", LINE, 8) + "".join(t(x + 8, y + 16 + i * 12, l, 9, INK) for i, l in enumerate(lines)), h
def G_(label, body, foot=None, example=True, sub="Promise list", acc=GB):
    return card(label, acc, gh(30, sub) + body + (chips(274, foot) if foot else ""), example)
GBP = []
def gp(group, ask, a, b): GBP.append((group, ask, a, b))
def plist(dfmt):
    rows = [("Send Report Center fix", "18:00 ICT", "in 3h"), ("Phone home round two", "Tomorrow 10:00 ICT", "in 22h"), ("WellNest Energy tin draft", "Mon 09:00 ICT", "in 2d")]
    return "".join(prow(66 + i * 46, r[0], ("Due " + r[1]) if dfmt == "clock" else ("Due " + r[2]), INK) for i, r in enumerate(rows))
gp("Promise List", "Promise List Due Times: The Clock Time In ICT, Or A Countdown Like 'In 3h'?",
   opt("fugb_clock", "Clock Time", "'Due 18:00 ICT' on every row.", "practical", G_("Due Times", plist("clock"), ["Exact"])),
   opt("fugb_countdown", "Countdown", "'Due in 3h' so urgency is obvious.", "bold", G_("Due Times", plist("count"), ["Urgency"])))
def bygroup(agent_first):
    if not agent_first: return plist("clock")
    s = ""; y = 64
    for ag, items in [("UpKeep", ["Phone home round two"]), ("Branding", ["Report Center fix", "Mixed deck round two"])]:
        s += t(14, y + 11, ag.upper(), 8.5, GB, "hind", 600, extra='letter-spacing="1"'); y += 14
        for it in items: s += prow(y, it, "Due 18:00 ICT"); y += 44
    return s
gp("Promise List", "Promise List Order: Soonest Due First, Or Grouped By Agent?",
   opt("fugb_soonest", "Soonest Due First", "One list; top row is what's next.", "practical", G_("List Order", bygroup(False), ["Next up"])),
   opt("fugb_byagent", "Grouped By Agent", "See each agent's open promises.", "calm", G_("List Order", bygroup(True), ["Who owes what"])))
def donemsg(proof):
    a, h = chatb(70, "Done: Phone home round two is live.", False, 190)
    s = a
    if proof: s += rect(14, 70 + h + 8, 190, 90, "#FFFFFF", LINE, 8) + photo(22, 70 + h + 16, 80, 74, LAGOON, "house", 4) + t(112, 70 + h + 44, "Screenshot + link", 10, INK, "hind", 600) + t(112, 70 + h + 60, "tap to open", 9, GB)
    return s
gp("Confirming Done", "Done Confirmations: One Line, Or One Line Plus A Screenshot And Link?",
   opt("fugb_doneline", "One Line", "'Done: X is live.' Nothing else.", "calm", G_("Done Message", donemsg(False), ["Short"], sub="Chat")),
   opt("fugb_doneproof", "Line + Proof", "Screenshot and link under the line.", "practical", G_("Done Message", donemsg(True), ["Check it yourself"], sub="Chat")))
def bars_(by):
    rows = [("Smart Upkeep app", .7), ("WellNest teas", .4), ("Investor pitch", .2)] if by == "project" else [("UpKeep Agent", .6), ("Branding Agent", .8), ("WellNest Agent", .5)]
    return "".join(t(14, 82 + i * 44, r[0], 10.5, INK, "hind", 600) + t(226, 82 + i * 44, f"{round(r[1]*100)}%", 10, MUTE, "hind", 600, "end") + rect(14, 90 + i * 44, 212, 10, LINE, "none", 5) + rect(14, 90 + i * 44, 212 * r[1], 10, GB, "none", 5) for i, r in enumerate(rows))
gp("Progress", "Percent-Done Bars: One Bar Per Project, Or One Bar Per Agent?",
   opt("fugb_barproj", "Per Project", "How far each thing you asked for is.", "practical", G_("Progress Bars", bars_("project"), ["By project"], sub="Weekly")),
   opt("fugb_baragent", "Per Agent", "How far each agent is on its list.", "calm", G_("Progress Bars", bars_("agent"), ["By agent"], sub="Weekly")))
gp("Late Items", "Late Flag Look: A Red 'LATE' Tag, Or An Amber Dot With How Late?",
   opt("fugb_latered", "Red 'LATE' Tag", "Impossible to miss.", "bold", G_("Late Flag", prow(66, "Report Center fix", "Due 12:00 ICT", tag_=late_tag(188, 74, "red")) + prow(112, "Mixed deck round two", "Due 18:00 ICT") + prow(158, "Energy tin draft", "Due Mon 09:00 ICT"), ["Loud"])),
   opt("fugb_lateamber", "Amber Dot + Time", "'late 2h' in amber; calmer.", "calm", G_("Late Flag", prow(66, "Report Center fix", "Due 12:00 ICT", tag_=late_tag(180, 74, "amber")) + prow(112, "Mixed deck round two", "Due 18:00 ICT") + prow(158, "Energy tin draft", "Due Mon 09:00 ICT"), ["Calm"])))
def reason(expand):
    s = prow(66, "Report Center fix", "New: 18:00 ICT (was 12:00)", TERRA)
    if expand: s += rect(14, 108, 212, 26, SOFT, "none", 6) + t(22, 125, "Why: waiting on the submit key.", 9, INK)
    else: s += t(22, 124, "Why? Tap to read", 9.5, GB, "hind", 600)
    return s + prow(144, "Mixed deck round two", "Due 18:00 ICT")
gp("Missed Deadlines", "The Short Reason For A Missed Date: Always Shown Under It, Or Behind A 'Why' Tap?",
   opt("fugb_whyshown", "Always Shown", "Reason sits right under the new date.", "practical", G_("Missed Date", reason(True), ["No tap"])),
   opt("fugb_whytap", "Behind 'Why'", "List stays short; tap to read.", "calm", G_("Missed Date", reason(False), ["Tidy"])))
def wrapup(by):
    s = t(14, 76, "This week", 14, INK, "khand", 700); y = 86
    groups = [("Smart Upkeep app", ["Phone home live", "Trust tags v2"]), ("WellNest", ["Beauty Line deck"])] if by == "project" else [("UpKeep Agent", ["Phone home live", "Trust tags v2"]), ("Branding Agent", ["Mixed deck round two"])]
    for gname, items in groups:
        s += t(14, y + 12, gname, 10.5, GB, "hind", 600); y += 20
        for it in items:
            s += dot(20, y + 6, 3, JUNGLE) + t(30, y + 10, it, 10, INK); y += 18
            if by == "project": s += t(226, y - 8, "UpKeep" if "WellNest" not in gname else "WellNest", 8.5, MUTE, "hind", 600, "end")
        y += 10
    return s
gp("Weekly Wrap-Up", "Weekly Wrap-Up (You Want Agents Named And The Team Too): Group By Project With Names, Or Group By Agent?",
   opt("fuwg_proj", "By Project, Names Beside", "What shipped per project, who on the right.", "practical", G_("Wrap-Up", wrapup("project"), ["Project first"], sub="Weekly wrap-up")),
   opt("fuwg_agent", "By Agent", "Each agent's list under its name.", "calm", G_("Wrap-Up", wrapup("agent"), ["Credit first"], sub="Weekly wrap-up")))
def review(day):
    s = rect(14, 66, 212, 130, "#FFFFFF", LINE, 10) + t(24, 88, "Weekly Review Deck", 14, INK, "khand", 700) + t(24, 104, f"{day}, 10 picks", 9, MUTE)
    s += rect(24, 114, 92, 70, GB + "18", LINE, 6) + rect(124, 114, 92, 70, TERRA + "18", LINE, 6) + t(70, 153, "This", 11, INK, "hind", 600, "middle") + t(170, 153, "That", 11, INK, "hind", 600, "middle")
    return s + chatb(206, f"Your weekly review is ready ({day}).", False, 200)[0]
gp("Weekly Review", "Weekly Review Swipe Deck: Ready Friday Evening, Or Monday Morning?",
   opt("fugb_fri", "Friday Evening", "Look back while the week is fresh.", "calm", G_("Review Deck", review("Friday 18:00 ICT"), sub="Weekly review")),
   opt("fugb_mon", "Monday Morning", "Set the week ahead with it.", "practical", G_("Review Deck", review("Monday 08:00 ICT"), sub="Weekly review")))
def brief(top):
    secs = [("Waiting on you", ["Ask slide amount?", "Rain jacket color?"], TERRA), ("Done", ["Phone home live"], JUNGLE), ("Next", ["Trust tags v2"], GB)]
    if not top: secs = secs[1:] + secs[:1]
    s = t(14, 76, "Morning brief", 14, INK, "khand", 700); y = 88
    for nm, items, c in secs:
        s += rect(14, y, 3, 16 + len(items) * 17, c) + t(22, y + 11, nm.upper(), 8.5, c, "hind", 600, extra='letter-spacing="1"'); y += 18
        for it in items: s += t(22, y + 11, it, 10, INK); y += 17
        y += 10
    return s
gp("Re-Asking", "Questions You Haven't Answered: At The Top Of The Next Brief, Or In A 'Waiting On You' Section At The End?",
   opt("fugb_qtop", "Top Of The Brief", "First thing you see each morning.", "bold", G_("Re-Ask Spot", brief(True), ["First"], sub="Morning brief")),
   opt("fugb_qend", "Section At The End", "News first, questions last.", "calm", G_("Re-Ask Spot", brief(False), ["Last"], sub="Morning brief")))
def credits(chips_):
    s = t(14, 76, "Shipped today", 14, INK, "khand", 700)
    rows = [("Phone home hero live", "UpKeep"), ("Mixed deck round two", "Branding"), ("Energy Line deck", "WellNest")]
    for i, (r, a) in enumerate(rows):
        y = 88 + i * 34; s += t(14, y + 14, r, 10, INK, "hind", 600)
        if chips_: s += rect(226 - len(a) * 5.4 - 12, y + 3, len(a) * 5.4 + 12, 16, SOFT, "none", 8) + t(226 - len(a) * 2.7 - 6, y + 14, a, 8.5, INK, "hind", 600, "middle")
        s += ln(y + 24)
    if not chips_: s += rect(14, 196, 212, 28, SOFT, "none", 6) + t(22, 214, "Who did what: UpKeep, Branding, WellNest", 9, INK)
    return s
gp("Credits", "Naming Agents In Reports: A Small Name Chip On Each Line, Or One 'Who Did What' Line At The Bottom?",
   opt("fugb_chips", "Chip On Each Line", "Who did each thing, right there.", "practical", G_("Agent Credit", credits(True), ["Per line"], sub="Daily report")),
   opt("fugb_footer", "'Who Did What' Line", "Lines read as the team; credit below.", "calm", G_("Agent Credit", credits(False), ["Team voice"], sub="Daily report")))
# ---------- Branding: Mixed Deck: Up Keep, next round (static from banks/upkeep.json) ----------
BANK = {p["id"]: p for p in json.load(open("banks/upkeep.json"))["pairs"]}
MIX, MIX_IDS = [], []
def mx(bid, ask, la, da, lb, db, feels=("practical", "calm")):
    p = BANK[bid]; k = bid.split("-")[-1]
    MIX.append((p["group"], ask, opt(f"fumix_{k}a", la, da, feels[0], p["optionA"]["visual"]["svg"]), opt(f"fumix_{k}b", lb, db, feels[1], p["optionB"]["visual"]["svg"]))); MIX_IDS.append(bid)
mx("upkeep-bank-103", "Re-Ask, Open Items List: Cards With A Colored Left Edge, Or Simple Divider Lines?", "Colored Edge Cards", "Each item a rounded card with a color edge.", "Simple Divider Lines", "Plain rows split by thin lines, square look.")
mx("upkeep-bank-112", "Re-Ask, Crew Picture: One Tech In A Polo, Or Two Techs In Tees?", "One Tech In A Polo", "A single tech, plain header above.", "Two Techs In Tees", "Two people, color band header.")
mx("upkeep-bank-126", "Re-Ask, Open Item Details: Sections That Fold Open, Or A Picture Above Each Item?", "Fold-Open Sections", "Tap a row to open it; terracotta accent.", "Picture Above Each Item", "Photo first, words under; lagoon accent.")
mx("upkeep-bank-092", "Re-Ask, Lawn Add-On Card: A Grid Of Small Icons, Or One Feature With A List?", "Small Icon Grid", "What's included as little icons; jungle accent.", "One Feature + A List", "One big feature, list under; saffron accent.")
mx("upkeep-bank-134", "Plan Cards: A Ring Showing Visits Used, Or One Big Number?", "Ring Of Visits Used", "Ring fills as visits happen; jungle accent.", "One Big Number", "Big visit count; saffron accent.", ("calm", "bold"))
mx("upkeep-bank-115", "Crew Picture, Again: One Tech In A Zip Jacket, Or A Crew Of Three?", "One Tech, Zip Jacket", "Single tech in the cold-weather layer.", "Crew Of Three", "Three techs together, color band header.")
mx("upkeep-bank-098", "Lawn Add-On Action: A Simple Text Link, Or A Bar Stuck To The Bottom?", "Simple Text Link", "Quiet link under the add-on.", "Bottom Bar", "Add button pinned to the bottom, color header.", ("calm", "bold"))
mx("upkeep-bank-086", "Licensed Tech Card: Photo Above The Name, Or Photo Beside It?", "Photo Above", "Big tech photo on top; jungle accent.", "Photo Beside", "Small photo next to the name; saffron accent.")
mx("upkeep-bank-127", "Open Item Buttons: Square Corners, Or Round Pill Buttons?", "Square Buttons", "Sharp, square buttons; jungle accent.", "Pill Buttons", "Round-ended buttons; saffron accent.", ("practical", "playful"))
mx("upkeep-bank-081", "Licensed Tech Card Details: Dotted Rows, Or Cards With A Colored Edge?", "Dotted Rows", "Details as rows with dots; terracotta.", "Color Edge Cards", "Each detail a card with a lagoon edge.")
def DD(id, name, slug_key, prefix, app, agent, submit_to, board, follows, about, summary, tag, pairs, reasked=(), inbox="", brands=(), **kw):
    d = dict(id=id, name=name, slug_key=slug_key, prefix=prefix, app=app, agent=agent, submit_to=submit_to, board=board, topic=slug_key, follows=follows, about=about,
             summary=summary, tag=tag, pairs=pairs, reasked=list(reasked), agent_inbox=inbox, brands=list(brands)); d.update(kw); return d
DECKS = [
 DD("wellnest-tea-blends-energy-line-recipe", "Tea Blends: Energy Line Recipe", "wellnest-tea-energy-line-recipe", "fuwn_", "WellNest", "wellnest", WN, "wellnest",
    "wellnest-tea-blend-ingredients-calm-line-digestion-line",
    "Follow-on to Tea Blends: Energy Line & Line Purposes (10/10, 08:15 ICT): lemongrass, moringa, gentle lift, local oolong and both moringa + ginger picked, own farm first. Now the recipe: ratio, ginger level, third herb, moringa form, serve, pack story, caffeine line, colour, format, brew guide.",
    "Energy Line recipe and pack: leaf-to-herb ratio, ginger level, pandan vs Thai basil, moringa form, hot vs iced, source wording, caffeine line, band colour, tin vs bags, steeps.",
    "Tea Blends", WNP, [], "wellnest/wellnest-tea-blend-ingredients-calm-line-digestion-line-20261017-0815-*.json",
    ["WellNest teas: herbal and tea-leaf blends only. No cannabis or hemp; no health claims on cards. Source wording on packs is a draft until the farm confirms what it grows (oolong comes from a grower)."],
    head_extra="wellnest"),
 DD("follow-through-promise-list-and-reports", "Follow-Through: Promise List And Reports", "follow-through-promise-list", "fugb_", "Grok Bot", "grok-bot", "Grok Bot", "grok-bot",
    "follow-through-reporting-habits-promises",
    "Follow-on to Follow-Through: Habits & Promises (10/10, 12:20 ICT): tracked promise list, confirm done, percent bars, explain misses, flag late, weekly wrap-up, swipe-deck review, re-ask next day, name agents and team. Drawn Grok Bot screens.",
    "Promise list due format and order, done-message proof, progress bars by project or agent, late flag look, missed-date reason, wrap-up grouping, review day, re-ask spot, agent credits.",
    "Follow-Through", GBP, [], "grok-bot/follow-through-reporting-habits-promises-20261017-1220-*.json",
    ["How Grok Bot runs Max's agent team as CEO. Example rows and times only."]),
 DD("mixed-deck-up-keep-round-two", "Mixed Deck: Up Keep, Round Two", "mixed-deck-up-keep-round-two", "fumix_", "Smart Upkeep", "branding", "Branding Agent 3fac5054-3a3d-49b1-af61-59883f7fdc78", "branding",
    "mix-upkeep-2026-10-17",
    "Follow-on to Mixed Deck: Up Keep (6/10, 10:24 ICT): his four skips re-asked in new words (open items edge cards, crew picture, fold-open details, lawn add-on card), plus six unseen Up Keep bank pairs (plan ring, crew of three, lawn action, tech card photo, buttons, tech details).",
    "Four skipped mix pairs re-asked in plain words, plus six unseen Up Keep bank pairs: plan ring vs number, crew picture, lawn add-on action, tech card photo, buttons, tech details.",
    "Mixed Deck", MIX, ["upkeep-bank-103", "upkeep-bank-112", "upkeep-bank-126", "upkeep-bank-092"], "branding/mix-*-20261017-1024-*.json",
    ["Smart Upkeep bank visuals (banks/upkeep.json), example data only. Lawn add-on shown whole, never split into steps."], bank_ids=MIX_IDS),
]
