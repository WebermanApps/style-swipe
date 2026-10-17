"""Investor Pitch Deck: slide looks and story choices (16:9 slide mockups; every number is a labeled placeholder)."""
import base64, io
from PIL import Image
from uk5_art import *
def _poster():
    im = Image.open("/tmp/su-read/assets/poster-v7-16x9.jpg").convert("RGB").resize((640, 360)); b = io.BytesIO(); im.save(b, "JPEG", quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
POSTER = _poster()
PAIRS = []
def pair(g, ask, a, b): PAIRS.append((g, ask, a, b))
def note(y, lines, c=MUTE):
    return "".join(t(14, y + i * 11, l, 7.5, c) for i, l in enumerate(lines))
def house(x, y, s, c=TERRA, drip=False, ok=False):
    o = f'<path d="M{x} {y+s*.45} L{x+s*.5} {y} L{x+s} {y+s*.45}" fill="none" stroke="{INK}" stroke-width="{s*.05}"/>' + rect(x + s * .12, y + s * .4, s * .76, s * .6, "#FFFFFF", INK, 0, s * .04) + rect(x + s * .42, y + s * .66, s * .18, s * .34, c)
    if drip: o += f'<path d="M{x+s*.25} {y+s*.5} q{s*.05} {s*.1} 0 {s*.14} q-{s*.05} -{s*.04} 0 -{s*.14}" fill="{LAGOON}"/>' + f'<path d="M{x+s*.75} {y+s*.18} l{s*.06} {s*.08}" stroke="{TERRA}" stroke-width="{s*.04}"/>'
    if ok: o += f'<circle cx="{x+s*.95}" cy="{y+s*.1}" r="{s*.13}" fill="{JUNGLE}"/><path d="M{x+s*.89} {y+s*.1} l{s*.05} {s*.05} l{s*.08} -{s*.09}" fill="none" stroke="#FFFFFF" stroke-width="{s*.04}"/>'
    return o
CRM = "#FAF6EE"
# 1 opening hook (lead)
s1a = rect(0, 0, 320, 180, CRM) + t(20, 30, "SMART UPKEEP", 9, TERRA, "hind", 600, extra='letter-spacing="2"') + stitle("It started with a drip.", 20, 62, 22) + ssub("One homeowner's story, told in 3 photos.", 20, 80, 10) + house(228, 88, 72, TERRA, drip=True) + rect(20, 100, 110, 50, "#FFFFFF", LINE) + t(28, 116, "REPAIR BILL", 8, MUTE, "hind", 600) + t(28, 138, "$X,XXX", 18, TERRA, "khand") + t(98, 138, "example", 8, MUTE) + sfoot(1)
s1b = f'<image href="{POSTER}" x="0" y="0" width="320" height="180" preserveAspectRatio="xMidYMid slice"/>' + rect(0, 120, 320, 60, "#FFFFFFE6") + stitle("Your Home, Taken Care Of.", 20, 148, 24) + ssub("Membership home upkeep, Metro Detroit.", 20, 166, 10)
pair("Opening Hook", "Opening Hook: A Homeowner Story Or The Brand Promise Over The Van Shot?",
 ("hook_story", "Homeowner Story", "Open on a drip and a surprise bill, then reveal Smart Upkeep.", "bold",
  card("Opening Hook", TERRA, slide(14, 32, 212, s1a) + deck_strip(14, 166, 212, 6, 0, [(0, "Hook")]) + note(206, ["Slide 1. Placeholder bill amount,", "shown as $X,XXX (example)."]))),
 ("hook_promise", "Brand Promise Over Van Shot", "Open on the site's own headline over the Smart Upkeep van frame.", "premium",
  card("Opening Hook", LAGOON, slide(14, 32, 212, s1b) + deck_strip(14, 166, 212, 6, 0, [(0, "Hook")], LAGOON) + note(206, ["Slide 1. Uses the homepage line", "and the intro video frame."]))))
# 2 problem framing
cal = ""
mon = "JFMAMJJASOND"
for i, m in enumerate(mon):
    x = 20 + i * 24; cal += rect(x, 70, 21, 60, "#FFFFFF", LINE) + t(x + 10.5, 82, m, 9, MUTE, "hind", 600, "middle")
    if i in (2, 3, 8, 9, 11): cal += rect(x + 3, 90, 15, 6, TERRA) + rect(x + 3, 100, 10, 6, LAGOON + "88")
s2a = stitle("Every season has a to-do list.", 20, 36, 20) + ssub("Furnace, AC, gutters, water heater, smoke alarms...", 20, 54) + cal + t(20, 150, "Each bar = one seasonal task (example layout)", 9, MUTE) + sfoot(2)
s2b = rect(0, 0, 160, 180, "#F3EEE6") + rect(160, 0, 160, 180, "#EEF5F1") + t(20, 30, "SKIPPED", 10, TERRA, "hind", 600, extra='letter-spacing="1.5"') + t(180, 30, "CARED FOR", 10, JUNGLE, "hind", 600, extra='letter-spacing="1.5"') + house(35, 50, 90, TERRA, drip=True) + house(195, 50, 90, JUNGLE, ok=True) + t(20, 166, "Small problems grow.", 13, INK, "khand") + t(180, 166, "Caught on a visit.", 13, INK, "khand")
pair("Problem Framing", "Problem Slide: A Year Of Seasonal Tasks, Or A Split Screen Of Skipped Versus Cared For?",
 ("problem_calendar", "Seasonal Task Calendar", "Shows how many jobs a home needs across a year.", "practical",
  card("Problem Framing", TERRA, slide(14, 32, 212, s2a) + note(166, ["Calendar of real tasks from the plans:", "furnace, AC, gutters, water heater."]) + chips(272, ["Concrete"]))),
 ("problem_split", "Skipped Vs Cared For", "One split image: the same house, two outcomes.", "bold",
  card("Problem Framing", JUNGLE, slide(14, 32, 212, s2b) + note(166, ["Split screen, no numbers needed.", "Works in a live pitch."]) + chips(272, ["Emotional"]))))
# 3 traction
s3a = stitle("Traction", 20, 34, 20) + "".join(kpi(20 + i * 98, 52, 90, 56, v, l) for i, (v, l) in enumerate([("XXX", "Members"), ("$XXk", "Monthly revenue"), ("XX%", "Renewals")])) + t(20, 132, "Placeholders until real numbers are in.", 10, MUTE) + ex_tag(300, 150) + sfoot(5)
tl = f'<path d="M30 100 H290" stroke="{INK}" stroke-width="1.5"/>' + "".join(dot(40 + i * 82, 100, 6, TERRA if i < 2 else "#CFC6B4") + t(40 + i * 82, 85, lb, 9, INK, "hind", 600, "middle") + t(40 + i * 82, 122, "Month X", 8, MUTE, "hind", 400, "middle") for i, lb in enumerate(["Site live", "Milestone 2", "Milestone 3", "Milestone 4"]))
s3b = stitle("How far we've come", 20, 34, 20) + tl + ex_tag(300, 150) + sfoot(5)
pair("Traction", "Traction Slide: Three Big Number Tiles Or A Milestone Timeline?",
 ("traction_tiles", "Big Number Tiles", "Three tiles, filled in once real numbers exist.", "bold",
  card("Traction", TERRA, slide(14, 32, 212, s3a) + note(166, ["Tiles stay as XXX placeholders", "until Max has real numbers."]) + chips(272, ["Numbers first"]), example=True)),
 ("traction_timeline", "Milestone Timeline", "Dots for what's done and what's next.", "calm",
  card("Traction", LAGOON, slide(14, 32, 212, s3b) + note(166, ["Only the live site is filled in;", "the rest are placeholders."]) + chips(272, ["Story first"]), example=True)))
# 4 ask
s4a = rect(0, 0, 320, 180, CRM) + t(160, 50, "WE'RE RAISING", 10, MUTE, "hind", 600, "middle", 'letter-spacing="2"') + t(160, 98, "$X.XM", 46, TERRA, "khand", anchor="middle") + "".join(t(160, 124 + i * 14, s, 10, INK, "hind", 400, "middle") for i, s in enumerate(["Techs and vans", "Member growth", "18 months of runway (example)"])) + sfoot(10)
s4b = rect(0, 0, 130, 180, TERRA) + t(18, 40, "THE ASK", 10, "#FFFFFF", "hind", 600, extra='letter-spacing="2"') + t(18, 86, "$X.XM", 36, "#FFFFFF", "khand") + t(18, 106, "placeholder", 9, "#FFFFFFCC") + "".join(dot(150, 40 + i * 40, 5, JUNGLE) + t(162, 44 + i * 40, s, 11, INK, "khand") + t(162, 56 + i * 40, "Milestone (example)", 8, MUTE) for i, s in enumerate(["More techs on the road", "More members", "Break-even"]))
pair("The Ask", "Ask Slide Look: One Bold Centered Number, Or Ask On The Left With Milestones On The Right?",
 ("ask_bold", "One Bold Number", "Big round size in the middle, three uses under it.", "bold",
  card("The Ask", TERRA, slide(14, 32, 212, s4a) + note(166, ["Amount stays $X.XM until Max", "sets the round size."]) + chips(272, ["Simple"]), example=True)),
 ("ask_split", "Ask + Milestones Split", "Ask in a terracotta panel, what it unlocks beside it.", "practical",
  card("The Ask", JUNGLE, slide(14, 32, 212, s4b) + note(166, ["Milestones are placeholders,", "no dates or numbers invented."]) + chips(272, ["Tied to goals"]), example=True)))
# 5 team
def head(x, y, s, c):
    return f'<circle cx="{x}" cy="{y}" r="{s}" fill="{c}22"/><circle cx="{x}" cy="{y-s*.2}" r="{s*.38}" fill="{c}"/><path d="M{x-s*.65} {y+s*.75} Q{x} {y+s*.05} {x+s*.65} {y+s*.75} Z" fill="{c}"/>'
s5a = stitle("The Team", 20, 34, 20) + "".join(head(55 + i * 70, 85, 24, [TERRA, LAGOON, JUNGLE, SAFFRON][i]) + t(55 + i * 70, 128, "Name", 11, INK, "khand", anchor="middle") + t(55 + i * 70, 141, ["Founder", "Role", "Role", "Advisor"][i], 8, MUTE, "hind", 400, "middle") for i in range(4)) + sfoot(9)
s5b = rect(0, 0, 320, 180, CRM) + head(60, 70, 34, TERRA) + t(110, 52, "Max Weberman", 18, INK, "khand") + t(110, 66, "Founder", 10, TERRA, "hind", 600) + "".join(rect(110, 76 + i * 12, [160, 140, 120][i], 4, "#D9D2C6") for i in range(3)) + t(20, 140, "ADVISORS", 8, MUTE, "hind", 600, extra='letter-spacing="1.5"') + "".join(rect(20 + i * 72, 148, 62, 18, "#FFFFFF", LINE) + t(51 + i * 72, 160, "Name", 8, MUTE, "hind", 400, "middle") for i in range(4))
pair("Team Slide", "Team Slide: A Headshot Grid With Roles, Or The Founder Story With An Advisor Row?",
 ("team_grid", "Headshot Grid", "Equal tiles, name and role under each.", "calm",
  card("Team Slide", LAGOON, slide(14, 32, 212, s5a) + note(166, ["Drawn placeholders, swap in real", "headshots and names later."]) + chips(272, ["Team-wide"]))),
 ("team_founder", "Founder Story + Advisors", "Founder up front with a short story, advisors in a row.", "premium",
  card("Team Slide", TERRA, slide(14, 32, 212, s5b) + note(166, ["Story lines are placeholders;", "advisor names left blank."]) + chips(272, ["Founder-led"]))))
# 6 demo placement
pair("Demo Placement", "Product Demo: Right After The Problem, Or Just Before The Ask?",
 ("demo_early", "Right After The Problem", "Slide 3: show the app while the problem is fresh.", "bold",
  card("Demo Placement", TERRA, slide(14, 32, 212, stitle("Demo", 20, 40, 24) + ssub("Live app walk-through, 2 minutes", 20, 58) + rect(120, 72, 80, 96, INK) + rect(124, 78, 72, 84, "#FFFFFF") + "".join(rect(130, 86 + i * 18, 60, 12, [TERRA, LAGOON, JUNGLE, SAFFRON][i] + "33") for i in range(4)))
       + deck_strip(14, 166, 212, 10, 2, [(0, "Hook"), (1, "Problem"), (2, "Demo")]) + note(206, ["Order: Hook, Problem, Demo,", "Solution, Market, Traction, Ask."]))),
 ("demo_late", "Just Before The Ask", "Build the case first, then show it working.", "calm",
  card("Demo Placement", LAGOON, slide(14, 32, 212, stitle("Demo", 20, 40, 24) + ssub("Member app and tech app, side by side", 20, 58) + rect(70, 72, 80, 96, INK) + rect(74, 78, 72, 84, "#FFFFFF") + rect(170, 72, 80, 96, INK) + rect(174, 78, 72, 84, "#FFFFFF") + "".join(rect(80, 86 + i * 18, 60, 12, LAGOON + "33") + rect(180, 86 + i * 18, 60, 12, TERRA + "33") for i in range(4)))
       + deck_strip(14, 166, 212, 10, 8, [(8, "Demo"), (9, "Ask")], LAGOON) + note(206, ["Order: Hook, Problem, Solution,", "Market, Traction, Team, Demo, Ask."]))))
# 7 chart style
vals = [1, 1.4, 2, 2.9, 4, 5.4, 7]
s7a = stitle("Members over time", 20, 30, 16) + axes(30, 46, 260, 100) + line(30, 46, 260, 100, vals, 8, TERRA, 3) + t(292, 46 + 100 - 100 * 7 / 8 - 4, "Plus", 9, TERRA, "hind", 600, "end") + line(30, 46, 260, 100, [.6, .8, 1, 1.3, 1.7, 2.1, 2.6], 8, LAGOON, 2) + t(292, 46 + 100 - 100 * 2.6 / 8 - 4, "Essentials", 9, LAGOON, "hind", 600, "end") + t(20, 166, "Example data", 8, "#7A5A0C", "hind", 600)
s7b = stitle("Members over time", 20, 30, 16) + axes(30, 46, 260, 100) + bars(30, 46, 260, 100, vals, 8, TERRA, 6) + rect(170, 52, 92, 22, "#FFFFFF", TERRA, 0, 1) + t(216, 66, "Callout: what changed", 8.5, INK, "hind", 600, "middle") + t(20, 166, "Example data", 8, "#7A5A0C", "hind", 600)
pair("Chart Style", "Pitch Charts: Clean Lines With Direct Labels, Or Bars With A Callout Box?",
 ("chart_lines", "Clean Lines, Direct Labels", "No legend; labels sit at the end of each line.", "calm",
  card("Chart Style", TERRA, slide(14, 32, 212, s7a) + note(166, ["One accent per line, labels at", "the line ends, no legend box."]) + chips(272, ["Minimal"]), example=True)),
 ("chart_bars", "Bars With A Callout", "Latest bar in terracotta, the rest faded, one callout.", "bold",
  card("Chart Style", SAFFRON, slide(14, 32, 212, s7b) + note(166, ["Highlights one point; the callout", "names the reason."]) + chips(272, ["Points at one thing"]), example=True)))
# 8 slide look
s8a = rect(0, 0, 320, 180, CRM) + rect(20, 22, 30, 4, TERRA) + t(20, 74, "HOMES NEED", 36, INK, "khand") + t(20, 110, "A SCHEDULE.", 36, TERRA, "khand") + ssub("Seasonal visits, a report after each one.", 20, 134, 11) + sfoot(3)
s8b = rect(0, 0, 320, 180, "#FFFFFF") + rect(170, 0, 150, 180, CREAM) + g(198, 40, .42, person(polo=TERRA, hat="cap")) + g(244, 40, .42, person(skin=SKIN[2], hair=HAIR[3], hairstyle="pony", cargo=True)) + t(20, 60, "Homes need", 22, INK, "khand") + t(20, 84, "a schedule.", 22, INK, "khand") + ssub("Seasonal visits, a report", 20, 104, 10) + ssub("after each one.", 20, 117, 10) + sfoot(3)
pair("Slide Look", "Slide Look: Cream Slides With A Huge Headline, Or White Slides With An Illustration Half?",
 ("look_cream", "Cream, Huge Headline", "Type does the work; one terracotta word.", "bold",
  card("Slide Look", TERRA, slide(14, 32, 212, s8a) + slide(14, 158, 102, s8a) + slide(124, 158, 102, s2a) + chips(272, ["Type-led"]))),
 ("look_split", "White + Illustration Half", "Headline left, drawn techs right, same style as the site video.", "calm",
  card("Slide Look", LAGOON, slide(14, 32, 212, s8b) + slide(14, 158, 102, s8b) + slide(124, 158, 102, s5a) + chips(272, ["Picture-led"]))))
# 9 headline style
s9a = t(20, 40, "Every visit ends with a", 18, INK, "khand") + t(20, 60, "written report.", 18, TERRA, "khand") + rect(20, 76, 130, 84, "#FFFFFF", LINE) + "".join(rect(28, 86 + i * 14, [100, 80, 90, 60, 70][i], 5, "#E2DCD0") for i in range(5)) + rect(170, 76, 130, 84, CREAM) + icon("report", 215, 96, 40, TERRA) + sfoot(4)
s9b = t(20, 40, "Product", 22, INK, "khand") + rect(20, 52, 40, 3, TERRA) + rect(20, 76, 130, 84, "#FFFFFF", LINE) + "".join(rect(28, 86 + i * 14, [100, 80, 90, 60, 70][i], 5, "#E2DCD0") for i in range(5)) + rect(170, 76, 130, 84, CREAM) + icon("report", 215, 96, 40, LAGOON) + sfoot(4)
pair("Headlines", "Slide Headlines: Say The Takeaway, Or Just Name The Topic?",
 ("head_takeaway", "Takeaway Headlines", "The title is the point of the slide, e.g. the report after every visit.", "practical",
  card("Headlines", TERRA, slide(14, 32, 212, s9a) + note(166, ["Headlines read like a story if", "you only skim the titles."]) + chips(272, ["Skimmable"]))),
 ("head_topic", "Topic Headlines", "Short labels like Product, Market, Team.", "calm",
  card("Headlines", LAGOON, slide(14, 32, 212, s9b) + note(166, ["Classic pitch titles; the", "speaker supplies the point."]) + chips(272, ["Classic"]))))
# 10 demo format
def mini_app(acc):
    return rect(0, 0, 100, 190, "#FFFFFF") + rect(0, 0, 100, 18, "#FFFFFF") + wordmark(6, 13, 10) + rect(6, 26, 88, 40, CREAM) + t(10, 44, "Next visit", 9, INK, "khand") + t(10, 56, "Fall tune-up", 7.5, MUTE) + "".join(rect(6, 74 + i * 22, 88, 18, "#FFFFFF", LINE) + rect(10, 79 + i * 22, 8, 8, acc) + rect(22, 81 + i * 22, 50, 4, "#D9D2C6") for i in range(5))
s10a = rect(0, 0, 320, 180, CRM) + stitle("See it work", 20, 40, 22) + ssub("Tap points mark each step.", 20, 56) + rect(180, 14, 70, 156, INK) + g(184, 20, .62, mini_app(TERRA)) + "".join(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{TERRA}55" stroke="{TERRA}"/>' + t(cx, cy + 3, str(i + 1), 8, INK, "hind", 700, "middle") for i, (cx, cy) in enumerate([(214, 52), (200, 95), (226, 125)])) + sfoot(6)
s10b = rect(0, 0, 320, 180, INK) + rect(10, 10, 300, 160, "#FFFFFF") + g(110, 12, .82, mini_app(LAGOON)) + f'<circle cx="160" cy="92" r="16" fill="#0A0A0A88"/><path d="M155 84 L168 92 L155 100 Z" fill="#FFFFFF"/>' + rect(10, 160, 300, 10, "#0A0A0A") + rect(10, 163, 110, 4, TERRA)
pair("Demo Format", "Demo On The Slide: A Phone Mockup With Numbered Tap Points, Or A Full-Slide Screen Recording?",
 ("demofmt_phone", "Phone Mockup + Tap Points", "Still frame, numbered taps; works with no Wi-Fi.", "practical",
  card("Demo Format", TERRA, slide(14, 32, 212, s10a) + note(166, ["Safe for a live room and for", "a send-ahead PDF."]) + chips(272, ["No video needed"]))),
 ("demofmt_video", "Full-Slide Recording", "A short screen recording fills the slide.", "bold",
  card("Demo Format", LAGOON, slide(14, 32, 212, s10b) + note(166, ["Feels live; needs the video", "file to play in the room."]) + chips(272, ["Feels real"]))))
