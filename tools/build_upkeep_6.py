#!/usr/bin/env python3
"""Build Style Swipe deck upkeep-6 (PUBLISHED): 50 Up Keep pairs built on Max's upkeep-5 picks (reconstructed in
/workspace/smartkeep/branding/upkeep-5-picks.md). Mix: 9 follow-ups that lean into his picks, 9 skipped pairs re-asked in new
forms (van stripe: medium settled, test medium vs medium + saffron pinline), and 32 pairs across 8 new areas (dashboard, plan
change, neighbor referral, seasonal checklist, tech photo capture, operator console, empty and success states, QR landing page).
Rules: white light mode, Khand/Hind, Title Case, no byline, no AI / health score / tier names, only price 'Membership Starting at
$99/Month', only refund line 'Cancel Anytime', 'Your Licensed Tech' (no named tech, no license numbers).
Reuses the upkeep-5 drawing helpers. Run from the style-swipe repo root."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "build_upkeep_5.py")).read().split("\n# ---- order:")[0]
exec(compile(src, "uk5_helpers", "exec"))
import draft_svg
_icon = icon
def icon(k, x, y, s=18, style="outline", c=TERRA):
    try: return _icon(k, x, y, s, style, c)
    except KeyError: return draft_svg.ic(k, x, y, s, c if style == "duo" else INK)
DID = "upkeep-6"; pairs = []
def O(i, label, desc, tags, feel, svg):
    return {"id": "uk6_" + i, "label": label, "desc": desc, "tags": list(dict.fromkeys(tags + [feel])), "feeling": feel, "notes": True, "visual": {"type": "hm", "m": "svg", "svg": svg, "bg": "#F7F4EF"}}
def add(group, cat, a, b, ask, purpose="refine"):
    pairs.append({"group": group, "category": cat, "app": "Up Keep", "ask": ask, "optionA": a, "optionB": b, "purpose": purpose, "retest": purpose == "reask", "notes": True, "share": True})
LT = "Your Licensed Tech"

# ================= Building On Your Picks =================
G = "Building On Your Picks"
def dash_cards(edge="border", band=True):
    o = (rect(0, 35, W, 52, CREAM) if band else "") + lbl(14, 52, "Hi Sarah") + h1(14, 76, "Welcome Home", 22)
    for i, (k, n, st, c) in enumerate([("furnace", "Furnace", "Checked", JUNGLE), ("water", "Water Heater", "Due Soon", SAFFRON), ("ac", "AC Unit", "Checked", JUNGLE), ("smoke", "Smoke Detectors", "Checked", JUNGLE)]):
        y = 98 + i * 40
        o += rect(14, y, 212, 34, "#FFFFFF", LINE if edge == "border" else "none", 6, 1, '' if edge == "border" else 'style="filter:drop-shadow(0 1px 2px #0002)"') + icon(k, 22, y + 8, 18, "duo", c) + t(48, y + 21, n, 9.5, INK, "khand") + tag(170, y + 12, st, c)
    return o
add(G, "Dashboard Cards", O("pk_band_full", "Cream Band With Big Greeting And Bordered Cards", "Your picks together: cream band, big greeting, thin-border cards, colored icons.", ["system", "neighbor", "visual"], "neighbor", scr(dash_cards())),
    O("pk_band_off", "Same, But No Cream Band", "Your picks on pure white, no band.", ["system", "simple"], "system", scr(dash_cards(band=False))), "Keep The Cream Band?")
def photo_step(guide="corner", ex=True, dotsn=True):
    o = (dots(48, 5, 1, INK) if dotsn else "") + h1(14, 72, "Snap The Water Heater Label", 15)
    if ex: o += rect(14, 80, 60, 40, CREAM, LINE, 4) + photo(18, 84, 52, 32, "label", 3) + t(80, 100, "Like This", 8, MUTE)
    y = 128 if ex else 84; o += rect(14, y, 212, 120, "#2B2B2B", r=6) + photo(54, y + 20, 132, 80, "label", 3)
    if guide == "corner": o += "".join(f'<path d="M{x} {yy+(12 if sy>0 else -12)} V{yy} H{x+(12 if sx>0 else -12)}" stroke="#FFFFFF" stroke-width="2.5" fill="none"/>' for x, yy, sx, sy in [(44, y + 12, 1, 1), (196, y + 12, -1, 1), (44, y + 108, 1, -1), (196, y + 108, -1, -1)])
    else: o += rect(44, y + 12, 152, 96, "none", TERRA, 4, 2)
    return scr(o + btn(262, "Take Photo", "fill", INK, h=24, size=8.5))
add(G, "Photo Guide Color", O("pk_guide_white", "White Corner Guides", "Your corner-guide pick, in white.", ["system", "visual"], "system", photo_step("corner")),
    O("pk_guide_terra", "Full Terracotta Frame", "One thin terracotta box instead of corners.", ["lively", "visual"], "neighbor", photo_step("frame")), "Corners Or A Full Frame?")
def remind_ic(btns=2, col=TERRA):
    body = notif(120, "Your Visit Is Tomorrow, 9 AM", ["Your Licensed Tech will text when on the way."], accent=col)
    if btns == 2: body += rect(20, 178, 100, 22, "#FFFFFF", INK, 0, 1.4) + t(70, 193, "CONFIRM", 7, INK, "hind", 600, "middle") + rect(124, 178, 100, 22, "#FFFFFF", LINE, 0, 1.4) + t(174, 193, "RESCHEDULE", 7, MUTE, "hind", 600, "middle")
    else: body += rect(20, 178, 204, 22, INK) + t(122, 193, "CONFIRM", 7, "#FFFFFF", "hind", 600, "middle")
    return phone_frame(body)
add(G, "Reminder Buttons", O("pk_rem_two", "Confirm And Reschedule", "Your day-before reminder with both buttons.", ["system", "neighbor"], "system", remind_ic(2)),
    O("pk_rem_one", "Confirm Only, Reschedule Inside", "One black Confirm button.", ["simple", "system"], "system", remind_ic(1)), "Two Buttons Or One?")
def mail2(head="check", btnc=TERRA):
    o = rect(0, 0, W, H, "#F5F5F5") + rect(14, 18, 212, 266, "#FFFFFF", LINE, 4) + roof_logo(24, 38, .9, INK, MUTE)
    o += (dot(120, 78, 20, JUNGLE + "22") + icon("check", 106, 64, 28, "duo", JUNGLE)) if head == "check" else (dot(120, 78, 20, LAGOON + "22") + icon("cam", 106, 64, 28, "duo", LAGOON))
    o += t(120, 120, "Your Fall Visit Is Done", 14, INK, "khand", anchor="middle") + para(30, 138, ["Your Licensed Tech finished 11 checks.", "One thing to watch: the dryer vent."], 8, MUTE, 11)
    o += rows(170, [("Checks Done", "11"), ("To Watch", "1"), ("Fix Now", "0")], 18) + btn(238, "See The Full Report", "fill", btnc, x=30, w=180, h=24, size=8)
    return screen(o, head=False)
add(G, "Visit Email", O("pk_mail_check", "Green Check, Terracotta Button", "Your two email picks together.", ["lively", "system"], "neighbor", mail2()),
    O("pk_mail_cam", "Lagoon Photo Icon, Terracotta Button", "Leads with 'photos inside' instead of the check.", ["visual", "lively"], "neighbor", mail2("cam")), "Check Or Photo Icon Up Top?")
def receipt(mode):
    o = h1(14, 56, "Receipt", 18) + t(14, 70, "October 1, 2026", 7.5, MUTE)
    o += rows(80, [("Membership", "Monthly"), ("Visits Booked", "4 A Year"), ("Paid With", "Visa 4242")], 22)
    o += ln(152) + t(14, 170, "Monthly Membership", 11, INK, "khand")
    if mode == "tag": o += tag(14, 182, "Paid", JUNGLE, True)
    else: o += rect(14, 182, 212, 24, JUNGLE + "14", "none", 4) + icon("check", 20, 186, 14, "duo", JUNGLE) + t(40, 197, "Paid, Thank You", 8.5, INK, "hind", 600)
    return scr(o + t(120, 240, PRICE, 9.5, INK, "khand", anchor="middle") + t(120, 254, "Cancel Anytime", 7.5, JUNGLE, "hind", 600, "middle"))
add(G, "Ledger Receipt", O("pk_rc_tag", "Ledger With A Small Paid Tag", "Your ledger pick with a solid green tag.", ["system", "simple"], "system", receipt("tag")),
    O("pk_rc_strip", "Ledger With A Green Paid Strip", "A soft green line, 'Paid, Thank You'.", ["neighbor", "visual"], "neighbor", receipt("strip")), "Tag Or Strip?")
def recall_rows(icons):
    o = h1(14, 56, "Recall Check", 18) + t(14, 70, "Checked Oct 12, 2026", 7.5, MUTE)
    for i, (k, n) in enumerate([("furnace", "Furnace"), ("water", "Water Heater"), ("ac", "AC Unit"), ("smoke", "Smoke Detectors")]):
        y = 82 + i * 34; o += ln(y) + (icon(k, 14, y + 8, 18, "duo", LAGOON) if icons else "") + t(40 if icons else 14, y + 21, n, 10, INK, "khand") + tag(150, y + 12, "No Recall", JUNGLE)
    return scr(o)
add(G, "Recall Per Item", O("pk_rec_ic", "Per Item With Icons", "Your per-item pick with system icons.", ["visual", "system"], "system", recall_rows(True)),
    O("pk_rec_plain", "Per Item, Text Only", "Same rows, no icons.", ["simple", "system"], "system", recall_rows(False)), "With Icons Or Text Only?")
def daymap(stops):
    o = lbl(14, 48, "Tech App · Today") + h1(14, 66, "4 Stops", 16) + rect(14, 74, 212, 90, "#E8EEE6", r=6)
    o += f'<path d="M30 150 Q70 90 110 120 T200 90" fill="none" stroke="{LAGOON}" stroke-width="2.5"/>' + "".join(dot(x, y, 6, c) + t(x, y + 3, str(i + 1), 7, "#FFFFFF", "khand", anchor="middle") for i, (x, y, c) in enumerate([(30, 150, JUNGLE), (90, 112, TERRA), (150, 112, INK), (200, 90, INK)]))
    if stops == "rows": o += rows(172, [("9:00 · 1418 Maple Ave", "Done"), ("11:00 · 22 Oak St", "Next"), ("1:30 · 80 Elm Rd", ""), ("3:30 · 5 Pine Ct", "")], 22)
    else: o += rect(14, 172, 212, 60, "#FFFFFF", TERRA, 6, 1.5) + lbl(22, 188, "Next Stop", TERRA) + t(22, 206, "11:00 · 22 Oak St", 11, INK, "khand") + btn(240, "Start Drive", "fill", INK, h=22, size=8)
    return scr(o)
add(G, "Map Day", O("pk_map_rows", "Map With The Full Stop List", "Your map pick with all stops below.", ["system", "visual"], "system", daymap("rows")),
    O("pk_map_next", "Map With Only The Next Stop", "One big Next Stop card.", ["lively", "visual"], "neighbor", daymap("next")), "All Stops Or Next Only?")
def door_polo(collar):
    o = rect(0, 35, W, H, "#DCEAF0") + rect(60, 70, 120, 200, "#FFFFFF", "#BDBDBD") + rect(70, 80, 100, 190, "#6B4B3A")
    o += dot(120, 130, 16, "#B07D5B") + f'<path d="M92 270 V182 Q92 160 120 160 Q148 160 148 182 V270 Z" fill="{"#FFFFFF" if collar else TERRA}" stroke="#BDBDBD"/>'
    if collar: o += f'<path d="M108 160 L120 176 L132 160" fill="none" stroke="{TERRA}" stroke-width="4"/>' + rect(92, 262, 56, 6, TERRA)
    return scr(o + t(120, 290, LT, 10, INK, "khand", anchor="middle"))
add(G, "Polo At The Door", O("pk_polo_terra", "Terracotta Polo At The Door", "Your door pick.", ["lively", "neighbor"], "neighbor", door_polo(False)),
    O("pk_polo_collar", "White Polo, Terracotta Collar, At The Door", "Your crew-collar pick, seen at the door.", ["neighbor", "visual"], "neighbor", door_polo(True)), "Full Terracotta Or Collar Only?")
def note_both(mode):
    o = h1(14, 56, "Add A Note For Your Tech", 15) + rect(14, 66, 212, 90, "#FFFFFF", "#CFC8BC") + t(22, 84, "The upstairs vent rattles at night.", 8.5, INK)
    if mode == "side": o += rect(14, 164, 160, 26, INK) + t(94, 181, "SEND NOTE", 8, "#FFFFFF", "hind", 600, "middle") + rect(180, 164, 46, 26, "#FFFFFF", TERRA, 0, 1.5) + icon("chat", 192, 168, 18, "outline")
    else: o += rect(14, 164, 212, 26, INK) + t(120, 181, "SEND NOTE", 8, "#FFFFFF", "hind", 600, "middle") + link(120, 210, "Or Hold To Talk", TERRA, "middle")
    return scr(o)
add(G, "Type Or Talk", O("pk_note_side", "Type Box With A Talk Button Beside Send", "You picked both; both on one row.", ["system", "visual"], "system", note_both("side")),
    O("pk_note_link", "Type Box, 'Or Hold To Talk' Link Below", "Typing first, talking as a link.", ["simple", "neighbor"], "neighbor", note_both("link")), "Talk As A Button Or A Link?")

# ================= Skipped, Asked A New Way =================
G = "Skipped, Asked A New Way"
def stat_mark(kind):
    o = h1(14, 56, "Your Systems", 18)
    for i, (n, st, c) in enumerate([("Furnace", "Checked", JUNGLE), ("Water Heater", "Due Soon", SAFFRON), ("AC Unit", "Checked", JUNGLE), ("Dryer Vent", "Fix Now", TERRA)]):
        y = 70 + i * 40; o += rect(14, y, 212, 34, "#FFFFFF", LINE, 6)
        if kind == "bar": o += rect(14, y, 5, 34, c, r=0) + t(28, y + 21, n, 10, INK, "khand") + t(218, y + 21, st, 7.5, c, "hind", 600, "end")
        else: o += t(22, y + 21, n, 10, INK, "khand") + dot(204, y + 17, 9, c + "22") + (icon("check", 196, y + 9, 16, "duo", c) if st == "Checked" else t(204, y + 21, "!", 10, c, "khand", anchor="middle"))
    return scr(o)
add(G, "Status Mark", O("rs_stat_bar", "Status As A Color Edge Plus A Word", "Left color edge on each card, status word at right.", ["system", "visual"], "system", stat_mark("bar")),
    O("rs_stat_icon", "Status As A Small Round Icon", "A check or ! in a soft colored circle.", ["visual", "lively"], "neighbor", stat_mark("icon")), "Color Edge Or Round Icon?", "reask")
def ask2(kind):
    o = h1(14, 56, "Ask Anything", 18) + t(14, 70, "Your Licensed Tech replies within a day.", 7.5, MUTE)
    o += rect(96, 84, 130, 34, LAGOON, r=10) + para(104, 98, ["Is it normal for the furnace", "to click twice?"], 7.6, "#FFFFFF", 10)
    o += rect(14, 126, 140, 34, "#EEEEEE", r=10) + para(22, 140, ["Yes, that is the igniter.", "We'll check it at your visit."], 7.6, INK, 10)
    if kind == "plus": o += rect(14, 262, 26, 22, "#FFFFFF", INK, 0, 1.3) + t(27, 277, "+", 12, INK, "khand", anchor="middle") + rect(44, 262, 182, 22, "#FFFFFF", "#CFC8BC", 11) + t(54, 276, "Type A Question", 7.5, "#A3A3A3")
    else: o += rect(14, 238, 212, 20, CREAM, r=4) + t(120, 251, "Try: Send Photo  ·  Book A Visit", 7.5, MUTE, "hind", 600, "middle") + rect(14, 262, 212, 22, "#FFFFFF", "#CFC8BC", 11) + t(24, 276, "Type A Question", 7.5, "#A3A3A3")
    return scr(o)
add(G, "Thread Shortcuts", O("rs_ask_plus", "A '+' Button For Photo And Booking", "Shortcuts tucked behind one plus.", ["simple", "system"], "system", ask2("plus")),
    O("rs_ask_hint", "One Hint Line Above The Box", "'Try: Send Photo · Book A Visit'.", ["neighbor", "visual"], "neighbor", ask2("hint")), "Plus Button Or Hint Line?", "reask")
def pay2(kind):
    o = h1(14, 56, "Start Your Membership", 16) + t(120, 84, PRICE, 11, INK, "khand", anchor="middle")
    if kind == "trial": o += rect(14, 98, 212, 60, CREAM, LINE, 6) + icon("cal", 22, 110, 18, "duo", LAGOON) + t(48, 120, "First Charge After Your First Visit", 9, INK, "khand") + t(48, 134, "We save your card today.", 7.5, MUTE)
    else: o += rect(14, 98, 212, 60, "#FFFFFF", LINE, 6) + icon("check", 22, 110, 18, "duo", JUNGLE) + t(48, 120, "Your First Visit Gets Booked Now", 9, INK, "khand") + t(48, 134, "Pay today, pick your date next.", 7.5, MUTE)
    return scr(o + field(170, "Card", "Visa 4242") + btn(222, "Reserve My Spot" if kind == "trial" else "Pay And Book", "fill", INK, h=26, size=8.5) + t(120, 266, "Cancel Anytime", 7.5, JUNGLE, "hind", 600, "middle"))
add(G, "Payment Timing", O("rs_pay_after", "Lead With 'First Charge After Your First Visit'", "Card saved now, a lagoon note on timing.", ["neighbor", "system"], "neighbor", pay2("trial")),
    O("rs_pay_book", "Lead With 'Your First Visit Gets Booked Now'", "Pay today, framed as booking right away.", ["system", "lively"], "system", pay2("now")), "Pay Later Or Book Now Framing?", "reask")
def proof2(kind):
    o = h1(14, 56, "Home Record For Buyers", 15)
    if kind == "share": o += rect(14, 66, 212, 120, CREAM, LINE, 6) + t(120, 100, "Send Your Home Record", 12, INK, "khand", anchor="middle") + t(120, 116, "Every visit, photo and receipt in one file.", 7.5, MUTE, anchor="middle") + btn(140, "Share Link", "fill", INK, x=40, w=160, h=24, size=8)
    else: o += "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 60, 104, 54, "#FFFFFF", LINE, 6) + t(22 + (i % 2) * 108, 90 + (i // 2) * 60, n, 16, c, "khand") + t(22 + (i % 2) * 108, 104 + (i // 2) * 60, l, 7, MUTE) for i, (n, l, c) in enumerate([("12", "Visits", LAGOON), ("86", "Photos", TERRA), ("4", "Systems", JUNGLE), ("9", "Receipts", SAFFRON)]))
    return scr(o + btn(262, "Make Proof Pack", "outline", h=22, size=8))
add(G, "Proof Pack", O("rs_proof_share", "Proof Pack As One Share Card", "One cream card, one Share Link button.", ["simple", "neighbor"], "neighbor", proof2("share")),
    O("rs_proof_counts", "Proof Pack As Four Counts", "Visits, photos, systems, receipts as colored numbers.", ["visual", "system"], "system", proof2("counts")), "Share Card Or Counts?", "reask")
def vlog2(kind):
    o = h1(14, 56, "Visit Log", 18)
    data = [("Oct 4", "Fall Visit", JUNGLE), ("Jul 9", "Summer Visit", JUNGLE), ("Apr 2", "Spring Visit", SAFFRON), ("Jan 8", "Winter Visit", JUNGLE)]
    if kind == "cards": o += "".join(rect(14 + (i % 2) * 108, 66 + (i // 2) * 74, 104, 68, "#FFFFFF", LINE, 6) + rect(14 + (i % 2) * 108, 66 + (i // 2) * 74, 104, 4, c) + t(22 + (i % 2) * 108, 92 + (i // 2) * 74, s, 10, INK, "khand") + t(22 + (i % 2) * 108, 106 + (i // 2) * 74, d, 7.5, MUTE) for i, (d, s, c) in enumerate(data))
    else: o += "".join(t(14, 84 + i * 44, d.split()[0].upper(), 6.5, MUTE, "hind", 600) + t(14, 98 + i * 44, d.split()[1], 14, INK, "khand") + t(52, 92 + i * 44, s, 10, INK, "khand") + dot(216, 90 + i * 44, 4, c) + ln(108 + i * 44) for i, (d, s, c) in enumerate(data))
    return scr(o)
add(G, "Visit Log Layout", O("rs_log_cards", "Visit Log As Season Cards", "Two-by-two cards, a color top edge each.", ["visual", "lively"], "neighbor", vlog2("cards")),
    O("rs_log_cal", "Visit Log With Big Date Numbers", "Month and day on the left, visit on the right.", ["system", "simple"], "system", vlog2("date")), "Season Cards Or Big Dates?", "reask")
def filt(kind):
    if kind == "email":
        o = rect(0, 0, W, H, "#F5F5F5") + rect(14, 30, 212, 200, "#FFFFFF", LINE, 4) + roof_logo(24, 52, .9) + t(24, 82, "Time To Change Your Filter", 13, INK, "khand") + t(24, 98, "Size 16 x 25 x 1. Takes two minutes.", 8, MUTE) + btn(116, "Show Me How", "fill", TERRA, x=24, w=192, h=24, size=8)
        return screen(o, head=False)
    return phone_frame(notif(110, "Filter Day", ["Size 16 x 25 x 1. Tap to see how."], accent=LAGOON) + notif(180, "Done? Tap To Check It Off", ["We'll remind you in 90 days."], accent=JUNGLE))
add(G, "Filter Reminder", O("rs_filt_email", "Filter Reminder As An Email With A How-To", "One email with the size and a terracotta button.", ["system", "visual"], "system", filt("email")),
    O("rs_filt_pair", "Two Alerts: Reminder, Then Check-Off", "An app alert, then a follow-up to mark it done.", ["system", "lively"], "neighbor", filt("pair")), "Email Or Two Alerts?", "reask")
def zip2(kind):
    o = h1(14, 56, "We're Not In 48301 Yet", 15)
    if kind == "map": o += rect(14, 68, 212, 110, "#E8EEE6", r=6) + f'<circle cx="100" cy="120" r="40" fill="{JUNGLE}22" stroke="{JUNGLE}" stroke-dasharray="4 3"/>' + dot(180, 100, 5, TERRA) + t(180, 92, "You", 7, TERRA, "hind", 600, "middle") + t(14, 196, "We're growing toward you.", 8.5, MUTE)
    else: o += rect(14, 68, 212, 60, CREAM, LINE, 6) + t(22, 92, "Neighbors Asking: 14", 13, INK, "khand") + t(22, 108, "We open where enough homes ask.", 7.5, MUTE) + t(14, 150, "Add your home to the list.", 8.5, MUTE)
    return scr(o + field(206, "Email") + btn(250, "Tell Me When", "fill", INK, h=24, size=8))
add(G, "Out Of Area", O("rs_zip_map", "Out Of Area With A Service Map", "A map showing where we are now.", ["visual", "system"], "system", zip2("map")),
    O("rs_zip_count", "Out Of Area With 'Neighbors Asking' Count", "A count of nearby homes on the list.", ["neighbor", "lively"], "neighbor", zip2("count")), "Map Or Neighbor Count?", "reask")
def cal2(kind):
    o = h1(14, 56, "Your Year Of Visits", 16)
    vis = [("Jan 8", "Winter", LAGOON), ("Apr 2", "Spring", JUNGLE), ("Jul 9", "Summer", SAFFRON), ("Oct 4", "Fall", TERRA)]
    if kind == "rows": o += "".join(rect(14, 68 + i * 38, 212, 32, "#FFFFFF", LINE, 6) + rect(14, 68 + i * 38, 4, 32, c) + t(26, 88 + i * 38, f"{s} · {d}", 10, INK, "khand") + icon("cal", 200, 74 + i * 38, 16, "outline") for i, (d, s, c) in enumerate(vis))
    else: o += rect(14, 68, 212, 130, "#FFFFFF", LINE, 6) + "".join(t(26 + (i % 6) * 34, 88 + (i // 6) * 50, m, 7, MUTE, "hind", 600) + (dot(34 + (i % 6) * 34, 104 + (i // 6) * 50, 6, vis[[0, 3, 6, 9].index(i)][2]) if i in (0, 3, 6, 9) else "") for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]))
    return scr(o + btn(240, "Sync To My Calendar", "fill", INK, h=24, size=8))
add(G, "Calendar Add", O("rs_cal_rows", "Four Visit Rows, One Sync Button", "Each visit a row with its own calendar icon.", ["system", "simple"], "system", cal2("rows")),
    O("rs_cal_year", "Year Grid With Colored Visit Dots", "Twelve months, four colored dots.", ["visual", "lively"], "neighbor", cal2("year")), "Rows Or Year Grid?", "reask")
def van_pin(pin):
    o = rect(0, 34, W, 150, "#DCEAF0") + house_ill(120, 60, .6, "#5B5550", "#6B4B3A", "#B8CCD8") + rect(0, 184, W, 116, "#C9C6C0") + rect(0, 184, W, 10, "#9DB58A")
    x, y, sc = 30, 196, .86; a, b = 54, 64
    o += f'<g transform="translate({x},{y}) scale({sc})"><path d="M0 70 V10 Q0 0 10 0 H140 L196 40 V70 Z" fill="#FFFFFF" stroke="#6E6E6E" stroke-width="1.2"/><path d="M144 6 L186 38 H144 Z" fill="#B8CCD8"/>'
    o += f'<path d="M0 {a} H107 Q130 {a} 144 38 L156 38 Q140 {b} 111 {b} H0 Z" fill="{TERRA}"/>'
    if pin: o += f'<path d="M0 {b+3} H111 Q142 {b+3} 158 38 L161 38 Q144 {b+6} 112 {b+6} H0 Z" fill="{SAFFRON}"/>'
    o += '<circle cx="36" cy="70" r="12" fill="#2B2B2B"/><circle cx="160" cy="70" r="12" fill="#2B2B2B"/></g>' + roof_logo(x + 16, y + 34, 1.3, INK, MUTE)
    return scr(o + t(120, 288, "Medium Sweep Stripe" + (" Plus Saffron Pinline" if pin else ""), 10, INK, "khand", anchor="middle"))
add(G, "Van Stripe", O("rs_van_med", "Medium Sweep Stripe", "Medium is settled ('in between'); terracotta only.", ["system", "simple"], "system", van_pin(False)),
    O("rs_van_pin", "Medium Sweep Stripe Plus A Saffron Pinline", "Same stripe with a thin saffron line under it.", ["lively", "visual"], "neighbor", van_pin(True)), "Medium Alone Or With A Saffron Pinline?", "reask")

# ================= New Areas =================
def dash(kind):
    o = lbl(14, 50, "Hi Sarah") + h1(14, 72, "Welcome Home", 20)
    if kind == "next": o += rect(14, 82, 212, 70, CREAM, LINE, 6) + lbl(22, 100, "Next Visit", LAGOON) + t(22, 122, "Tue, Nov 4 · 9 AM", 15, INK, "khand") + t(22, 138, LT + " will text when on the way.", 7, MUTE)
    elif kind == "todo": o += rect(14, 82, 212, 70, "#FFFFFF", SAFFRON, 6, 1.5) + lbl(22, 100, "One Thing For You", SAFFRON) + t(22, 122, "Change The Furnace Filter", 13, INK, "khand") + link(22, 140, "Show Me How", TERRA)
    elif kind == "grid": o += "".join(rect(14 + (i % 2) * 108, 82 + (i // 2) * 52, 104, 46, "#FFFFFF", LINE, 6) + icon(k, 22 + (i % 2) * 108, 92 + (i // 2) * 52, 16, "duo", c) + t(44 + (i % 2) * 108, 104 + (i // 2) * 52, n, 9, INK, "khand") for i, (k, n, c) in enumerate([("cal" if False else "check", "Visits", JUNGLE), ("cam", "Photos", TERRA), ("chat", "Ask", LAGOON), ("water", "Systems", SAFFRON)]))
    else: o += rows(82, [("Next Visit", "Nov 4"), ("Last Visit", "Oct 4"), ("Open Items", "1"), ("Photos", "86")], 22)
    return o
G = "Dashboard"
add(G, "Dashboard Top Card", O("db_next", "Top Card: Next Visit", "Cream card with the next visit date.", ["system", "neighbor"], "neighbor", scr(dash("next") + rows(170, [("Furnace", "Checked"), ("Water Heater", "Due Soon"), ("AC Unit", "Checked")], 26))),
    O("db_todo", "Top Card: One Thing For You", "Saffron-edged card with your one to-do.", ["lively", "visual"], "neighbor", scr(dash("todo") + rows(170, [("Furnace", "Checked"), ("Water Heater", "Due Soon"), ("AC Unit", "Checked")], 26))), "Next Visit Or Your To-Do First?", "new")
add(G, "Dashboard Body", O("db_grid", "Four Colored Shortcut Tiles", "Visits, Photos, Ask, Systems.", ["visual", "lively"], "neighbor", scr(dash("grid") + tabbar(0))),
    O("db_rows", "Plain Summary Rows", "Next, last, open items, photos.", ["system", "simple"], "system", scr(dash("rows") + tabbar(0))), "Tiles Or Rows?", "new")
def dash_tech(kind):
    o = dash("next")
    if kind == "card": o += rect(14, 162, 212, 52, "#FFFFFF", LINE, 6) + techface(38, 184, 11) + t(58, 184, LT, 10, INK, "khand") + t(58, 197, "Licensed And Insured", 7, MUTE) + sq_btn(180, 178, "Call", 38)
    else: o += btn(166, "Call", "outline", INK, x=14, w=103, h=24, size=8) + btn(166, "Message", "outline", INK, x=123, w=103, h=24, size=8)
    return scr(o + tabbar(0))
add(G, "Dashboard Tech", O("db_tech_card", "Tech Card On The Dashboard", "A small face card for Your Licensed Tech.", ["neighbor", "visual"], "neighbor", dash_tech("card")),
    O("db_tech_btns", "Just Call And Message Buttons", "Two buttons, no face.", ["system", "simple"], "system", dash_tech("btns")), "Tech Card Or Two Buttons?", "new")
def dash_season(kind):
    o = dash("next") + lbl(14, 172, "Fall Progress")
    if kind == "bar": o += pbar(180, .6, JUNGLE) + t(14, 198, "6 Of 10 Fall Checks Done", 8, MUTE)
    else: o += "".join(dot(26 + i * 21, 188, 7, JUNGLE if i < 6 else "#EEEAE4") for i in range(10)) + t(14, 210, "6 Of 10 Fall Checks Done", 8, MUTE)
    return scr(o + tabbar(0))
add(G, "Dashboard Progress", O("db_prog_bar", "Season Progress As A Bar", "One green bar.", ["system", "simple"], "system", dash_season("bar")),
    O("db_prog_dots", "Season Progress As Ten Dots", "One dot per check.", ["visual", "lively"], "neighbor", dash_season("dots")), "Bar Or Dots?", "new")

G = "Plan Change"
def pc(kind):
    o = h1(14, 56, "Change My Plan", 18) + t(14, 70, PRICE, 9, INK, "khand")
    if kind == "list": o += rows(82, [("Add Extras", ""), ("Pause Visits", ""), ("Move To A New Home", ""), ("Cancel Membership", "")], 30) + "".join(icon("chev", 210, 92 + i * 30, 12, "outline") if False else t(222, 98 + i * 30, ">", 10, MUTE, "khand", anchor="end") for i in range(4))
    else: o += "".join(rect(14 + (i % 2) * 108, 82 + (i // 2) * 70, 104, 64, "#FFFFFF", LINE, 6) + aic(k, 22 + (i % 2) * 108, 90 + (i // 2) * 70, 20, c, True) + t(22 + (i % 2) * 108, 130 + (i // 2) * 70, n, 9.5, INK, "khand") for i, (k, n, c) in enumerate([("gutter", "Add Extras", JUNGLE), ("snow", "Pause Visits", LAGOON), ("window", "Move Homes", SAFFRON), ("vent", "Cancel", TERRA)]))
    return scr(o + t(120, 262, "Cancel Anytime", 7.5, JUNGLE, "hind", 600, "middle"))
add(G, "Plan Change Menu", O("pc_list", "Plan Options As A Plain List", "Four rows with arrows.", ["system", "simple"], "system", pc("list")),
    O("pc_tiles", "Plan Options As Icon Tiles", "Four tiles with colored drawn icons.", ["visual", "lively"], "neighbor", pc("tiles")), "List Or Tiles?", "new")
def pause(kind):
    o = h1(14, 56, "Pause Visits", 18) + t(14, 70, "Your membership stays, visits wait.", 7.5, MUTE)
    if kind == "chips": o += chip(14, 84, "1 Month", False, INK, 66) + chip(86, 84, "3 Months", True, LAGOON, 70) + chip(162, 84, "6 Months", False, INK, 64)
    else: o += rect(14, 84, 212, 90, "#FFFFFF", LINE, 6) + t(22, 102, "Resume On", 7, MUTE, "hind", 600) + t(22, 124, "Feb 1, 2027", 16, INK, "khand") + icon("cal", 196, 100, 18, "duo", LAGOON)
    return scr(o + btn(240, "Pause My Visits", "fill", INK, h=24, size=8))
add(G, "Pause Length", O("pc_pause_chips", "Pause By Picking 1, 3 Or 6 Months", "Three chips.", ["simple", "system"], "system", pause("chips")),
    O("pc_pause_date", "Pause Until A Date", "Pick the resume date.", ["system", "visual"], "neighbor", pause("date")), "Chips Or A Date?", "new")
def cancel_flow(kind):
    o = h1(14, 56, "Cancel Membership", 17)
    if kind == "pause": o += rect(14, 70, 212, 64, CREAM, LINE, 6) + t(22, 92, "Want A Break Instead?", 12, INK, "khand") + t(22, 108, "Pause visits and keep your record.", 7.5, MUTE) + link(22, 124, "Pause Instead", LAGOON)
    else: o += rect(14, 70, 212, 64, "#FFFFFF", LINE, 6) + t(22, 92, "Your Home Record Stays Yours", 12, INK, "khand") + t(22, 108, "Download it any time after you leave.", 7.5, MUTE)
    return scr(o + t(120, 168, "Cancel Anytime", 9, JUNGLE, "khand", anchor="middle") + btn(190, "Cancel Membership", "outline", TERRA, h=24, size=8) + btn(222, "Keep My Membership", "fill", INK, h=24, size=8))
add(G, "Cancel Screen", O("pc_can_pause", "Cancel Offers 'Pause Instead'", "A cream card suggesting a pause.", ["neighbor", "system"], "neighbor", cancel_flow("pause")),
    O("pc_can_record", "Cancel Promises 'Your Record Stays Yours'", "Plain reassurance, no offer.", ["system", "simple"], "system", cancel_flow("record")), "Pause Offer Or Record Promise?", "new")
def pc_done(kind):
    o = (dot(120, 90, 26, JUNGLE + "22") + icon("check", 102, 72, 36, "duo", JUNGLE)) if kind == "check" else rect(14, 50, 212, 80, CREAM, r=6) + icon("cal", 30, 66, 26, "duo", LAGOON)
    o += t(120, 150, "Extras Added", 17, INK, "khand", anchor="middle") + t(120, 166, "Gutter cleaning starts at your spring visit.", 7.5, MUTE, anchor="middle")
    return scr(o + btn(240, "Back Home", "fill", INK, h=24, size=8))
add(G, "Plan Change Done", O("pc_done_check", "Done Screen With A Big Green Check", "Simple confirmation.", ["system", "lively"], "system", pc_done("check")),
    O("pc_done_cal", "Done Screen With A Calendar Card", "Shows when the change starts.", ["visual", "neighbor"], "neighbor", pc_done("cal")), "Check Or Calendar?", "new")

G = "Neighbor Referral"
def ref(kind):
    o = h1(14, 56, "Invite A Neighbor", 18)
    if kind == "house": o += house_ill(30, 66, 1, "#5B5550", "#6B4B3A", "#B8CCD8", SAFFRON) + gift(186, 70, TERRA, 1.3)
    else: o += rect(14, 66, 212, 100, "#FFFFFF", LINE, 6) + qr(30, 80, 70) + t(112, 104, "Show This Code", 11, INK, "khand") + t(112, 120, "Your neighbor scans", 7.5, MUTE) + t(112, 132, "and joins in a minute.", 7.5, MUTE)
    return scr(o + t(14, 192, "You Both Get A Free Gutter Cleaning", 11, INK, "khand") + btn(212, "Send Invite Link", "fill", INK, h=24, size=8) + tabbar(3))
add(G, "Referral Hero", O("rf_house", "Referral With A Drawn House And Gift", "Warm picture up top.", ["neighbor", "visual"], "neighbor", ref("house")),
    O("rf_qr", "Referral With A Big QR Code", "Show the code at the fence.", ["system", "visual"], "system", ref("qr")), "Drawing Or QR Code?", "new")
def ref_track(kind):
    o = h1(14, 56, "Your Invites", 18)
    if kind == "rows": o += rows(70, [("Mike On Oak St", "Joined"), ("The Lees", "Invited"), ("Ana P.", "Invited")], 28)
    else: o += rect(14, 70, 212, 90, "#E8EEE6", r=6) + house_ill(26, 84, .35, "#5B5550", "#6B4B3A", "#B8CCD8") + house_ill(90, 84, .35, "#5B5550", JUNGLE, "#B8CCD8") + house_ill(154, 84, .35, "#5B5550", "#6B4B3A", "#B8CCD8") + tag(98, 146, "Joined", JUNGLE, True)
    return scr(o + t(14, 190, "1 Free Gutter Cleaning Earned", 10, JUNGLE, "khand") + tabbar(3))
add(G, "Referral Tracking", O("rf_rows", "Invites As A Status List", "Name and Joined / Invited.", ["system", "simple"], "system", ref_track("rows")),
    O("rf_street", "Invites As Houses On Your Street", "Joined homes get a green door.", ["neighbor", "lively"], "neighbor", ref_track("street")), "List Or Street View?", "new")
def ref_sms(kind):
    if kind == "warm": return sms([["Hey! We use Up Keep for the house.", "Your Licensed Tech comes 4x a year."], ["Membership Starting at $99/Month.", "Cancel Anytime. smartupkeep.com/i/sarah"]], "Mike")
    return sms([["Sarah invited you to Up Keep."], ["Home maintenance, done for you.", "smartupkeep.com/i/sarah"]], "Mike")
add(G, "Referral Text", O("rf_sms_warm", "Invite Text In Your Own Voice", "Two friendly bubbles with the price line.", ["neighbor", "lively"], "neighbor", ref_sms("warm")),
    O("rf_sms_short", "Short Invite Text", "One line and the link.", ["system", "simple"], "system", ref_sms("short")), "Personal Or Short Text?", "new")
def ref_card(kind):
    o = rect(0, 0, W, H, "#F2EFEA") + rect(30, 60, 180, 120, "#FFFFFF", "#BDBDBD") + roof_logo(44, 84, 1)
    o += t(44, 112, "Your Neighbor Sarah", 8, MUTE) + t(44, 130, "Thinks You'd Like Up Keep", 12, INK, "khand") + (rect(30, 174, 180, 6, TERRA) if kind == "strip" else "") + qr(166, 130, 32)
    if kind == "door": o += rect(100, 20, 40, 44, "none", "#6E6E6E", 20, 3)
    return screen(o + t(120, 210, "Door Hanger" if kind == "door" else "Mailbox Card", 10, INK, "khand", anchor="middle"), head=False)
add(G, "Referral Print", O("rf_card", "Printed Mailbox Card With A Terracotta Strip", "A postcard you drop off.", ["visual", "neighbor"], "neighbor", ref_card("strip")),
    O("rf_hanger", "Door Hanger", "Hangs on a neighbor's knob.", ["lively", "neighbor"], "neighbor", ref_card("door")), "Card Or Door Hanger?", "new")

G = "Seasonal Checklist"
def season(kind):
    o = h1(14, 56, "Fall Checklist", 18) + t(14, 70, "Your Licensed Tech covers most of it.", 7.5, MUTE)
    items = [("Furnace Tune-Up", True, "Us"), ("Gutter Check", True, "Us"), ("Change Filter", False, "You"), ("Test Smoke Alarms", False, "Us"), ("Shut Outdoor Taps", False, "You")]
    if kind == "split":
        o += lbl(14, 88, "We Do", JUNGLE) + "".join(check_box(14, 96 + i * 20, d) + t(32, 105 + i * 20, n, 8.5, INK) for i, (n, d, w) in enumerate([x for x in items if x[2] == "Us"]))
        o += lbl(14, 168, "You Do", SAFFRON) + "".join(check_box(14, 176 + i * 20, d, SAFFRON) + t(32, 185 + i * 20, n, 8.5, INK) for i, (n, d, w) in enumerate([x for x in items if x[2] == "You"]))
    else: o += "".join(ln(80 + i * 28) + check_box(14, 88 + i * 28, d) + t(32, 97 + i * 28, n, 8.5, INK) + tag(188, 88 + i * 28, w, JUNGLE if w == "Us" else SAFFRON) for i, (n, d, w) in enumerate(items))
    return scr(o)
add(G, "Checklist Grouping", O("sc_split", "Checklist Split: We Do, You Do", "Two labeled groups.", ["system", "visual"], "system", season("split")),
    O("sc_tags", "One List With Us / You Tags", "Single list, small colored tags.", ["lively", "visual"], "neighbor", season("tags")), "Split Or Tagged?", "new")
def season_nav(kind):
    o = h1(14, 56, "Seasonal Checklist", 16)
    s = [("Winter", LAGOON), ("Spring", JUNGLE), ("Summer", SAFFRON), ("Fall", TERRA)]
    if kind == "tabs": o += "".join(t(40 + i * 54, 82, n, 9, c if n == "Fall" else MUTE, "khand", anchor="middle") for i, (n, c) in enumerate(s)) + rect(176, 86, 46, 3, TERRA) + ln(89)
    else: o += "".join(rect(14 + i * 54, 70, 50, 34, c + ("33" if n == "Fall" else "14"), c if n == "Fall" else "none", 4, 1.5) + t(39 + i * 54, 91, n, 9, INK, "khand", anchor="middle") for i, (n, c) in enumerate(s))
    return scr(o + rows(112, [("Furnace Tune-Up", "Done"), ("Gutter Check", "Done"), ("Change Filter", "Due"), ("Shut Outdoor Taps", "Due")], 26))
add(G, "Season Switcher", O("sc_tabs", "Seasons As Text Tabs", "Underline marks the season.", ["system", "simple"], "system", season_nav("tabs")),
    O("sc_blocks", "Seasons As Color Blocks", "Four tinted blocks, each its season color.", ["visual", "lively"], "neighbor", season_nav("blocks")), "Tabs Or Color Blocks?", "new")
def season_item(kind):
    o = h1(14, 56, "Shut Outdoor Taps", 16) + tag(14, 64, "You Do", SAFFRON)
    if kind == "steps": o += "".join(dot(24, 100 + i * 34, 9, LAGOON) + t(24, 104 + i * 34, str(i + 1), 9, "#FFFFFF", "khand", anchor="middle") + t(40, 104 + i * 34, s, 9, INK, "khand") for i, s in enumerate(["Find The Inside Valve", "Turn It Off", "Open The Outside Tap To Drain"]))
    else: o += photo(14, 84, 212, 110, "interior", 6) + t(14, 212, "Turn the inside valve, then drain the tap.", 8, MUTE)
    return scr(o + btn(250, "Mark Done", "fill", JUNGLE, h=24, size=8))
add(G, "How-To Item", O("sc_steps", "How-To As Numbered Steps", "Three lagoon numbered steps.", ["system", "visual"], "system", season_item("steps")),
    O("sc_photo", "How-To As One Photo And A Line", "A picture, one sentence.", ["visual", "neighbor"], "neighbor", season_item("photo")), "Steps Or Photo?", "new")
def season_done(kind):
    o = h1(14, 56, "Fall Checklist", 18)
    if kind == "ring": o += ring(120, 130, 46, .8, JUNGLE, "8 Of 10")
    else: o += t(14, 100, "8 Of 10 Done", 22, JUNGLE, "khand") + pbar(110, .8, JUNGLE) + t(14, 134, "2 left, both for You.", 8, MUTE)
    return scr(o + btn(240, "See What's Left", "outline", h=24, size=8))
add(G, "Checklist Progress", O("sc_ring", "Progress As A Green Ring", "8 of 10 in a ring.", ["visual", "lively"], "neighbor", season_done("ring")),
    O("sc_num", "Progress As A Big Number And Bar", "Number first, thin bar.", ["system", "simple"], "system", season_done("num")), "Ring Or Number And Bar?", "new")

G = "Tech Photo Capture"
def cap(kind):
    o = rect(0, 0, W, H, "#1E1E1E") + photo(14, 40, 212, 170, "tech" if kind != "label" else "label", 6)
    o += rect(0, 0, W, 30, "#FFFFFF") + t(14, 20, "Furnace · Before", 9, INK, "khand") + tag(180, 10, "2 Of 6", LAGOON)
    if kind == "chips": o += rect(0, 220, W, 80, "#FFFFFF") + chip(14, 230, "Done", True, JUNGLE, 60) + chip(80, 230, "Watch", False, INK, 60) + chip(146, 230, "Fix Now", False, INK, 66) + dot(120, 278, 12, TERRA)
    else: o += rect(0, 220, W, 80, "#FFFFFF") + t(14, 240, "Tap To Add A Note", 8, MUTE) + dot(120, 274, 14, "#FFFFFF") + f'<circle cx="120" cy="274" r="14" fill="none" stroke="{INK}" stroke-width="3"/>'
    return screen(o, head=False)
add(G, "Capture Screen", O("tp_chips", "Shutter With Done / Watch / Fix Now Chips", "Rate the item right on the camera.", ["system", "visual"], "system", cap("chips")),
    O("tp_plain", "Plain Shutter, Rate After", "Camera first, rating on the next screen.", ["simple", "system"], "system", cap("plain")), "Rate On Camera Or After?", "new")
def ba(kind):
    o = lbl(14, 48, "Before And After") + h1(14, 66, "Dryer Vent", 16)
    if kind == "side": o += photo(14, 76, 104, 120, "mute", 4, "mute") + photo(122, 76, 104, 120, "house", 4) + tag(20, 82, "Before", SAFFRON, True) + tag(128, 82, "After", JUNGLE, True)
    else: o += photo(14, 76, 212, 120, "house", 4) + f'<line x1="120" y1="76" x2="120" y2="196" stroke="#FFFFFF" stroke-width="3"/>' + dot(120, 136, 9, "#FFFFFF") + t(120, 140, "<>", 8, INK, "khand", anchor="middle")
    return scr(o + btn(240, "Save Pair", "fill", INK, h=24, size=8))
add(G, "Before And After", O("tp_side", "Before And After Side By Side", "Two photos with saffron and green tags.", ["visual", "system"], "system", ba("side")),
    O("tp_slider", "Before And After Slider", "One photo, drag the line.", ["lively", "visual"], "neighbor", ba("slider")), "Side By Side Or Slider?", "new")
def queue(kind):
    o = lbl(14, 48, "Photos For This Visit") + h1(14, 66, "6 Of 11 Taken", 16) + pbar(74, 6 / 11, LAGOON)
    if kind == "grid": o += "".join((photo(14 + (i % 3) * 72, 88 + (i // 3) * 64, 68, 58, "tech", 4) if i < 6 else rect(14 + (i % 3) * 72, 88 + (i // 3) * 64, 68, 58, "#FFFFFF", "#CFC8BC", 4, 1, 'stroke-dasharray="3 3"') + icon("cam", 38 + (i % 3) * 72, 106 + (i // 3) * 64, 20, "outline")) for i in range(9))
    else: o += "".join(ln(88 + i * 28) + check_box(14, 96 + i * 28, i < 2) + t(32, 105 + i * 28, n, 8.5, INK) + icon("cam", 204, 94 + i * 28, 14, "outline") for i, n in enumerate(["Furnace Label", "Filter", "Water Heater", "Smoke Alarms", "Dryer Vent", "Sump Pump"]))
    return scr(o)
add(G, "Shot List", O("tp_grid", "Shot List As A Photo Grid", "Taken photos and dashed empty slots.", ["visual", "system"], "system", queue("grid")),
    O("tp_list", "Shot List As Checklist Rows", "One row per required photo.", ["system", "simple"], "system", queue("list")), "Grid Or Rows?", "new")
def markup(kind):
    o = rect(0, 0, W, H, "#1E1E1E") + photo(14, 40, 212, 180, "tech", 6) + rect(0, 0, W, 30, "#FFFFFF") + t(14, 20, "Mark The Problem", 9, INK, "khand")
    if kind == "circle": o += f'<circle cx="150" cy="110" r="26" fill="none" stroke="{TERRA}" stroke-width="3"/>'
    else: o += f'<path d="M80 170 L134 118" stroke="{SAFFRON}" stroke-width="4"/><path d="M134 118 l-12 2 l8 8 Z" fill="{SAFFRON}"/>' + rect(40, 172, 90, 18, SAFFRON, r=3) + t(85, 184, "Rust Here", 8, INK, "hind", 600, "middle")
    return screen(o + rect(0, 228, W, 72, "#FFFFFF") + btn(250, "Attach To Report", "fill", INK, h=24, size=8), head=False)
add(G, "Photo Markup", O("tp_circle", "Markup With A Terracotta Circle", "Circle the spot.", ["system", "visual"], "system", markup("circle")),
    O("tp_arrow", "Markup With A Saffron Arrow And Label", "Arrow plus a short word.", ["lively", "visual"], "neighbor", markup("arrow")), "Circle Or Arrow And Label?", "new")

G = "Operator Console"
def op(kind):
    o = rect(0, 0, W, 30, "#FFFFFF") + roof_logo(14, 20, .8) + t(226, 20, "Operator", 7, MUTE, "hind", 600, "end") + ln(30, 0, W)
    if kind == "board":
        for j, (n, c) in enumerate([("Today", LAGOON), ("Late", TERRA), ("Done", JUNGLE)]):
            x = 8 + j * 76; o += lbl(x, 48, n, c) + "".join(rect(x, 56 + i * 44, 72, 38, "#FFFFFF", LINE, 4) + rect(x, 56 + i * 44, 3, 38, c) + t(x + 8, 72 + i * 44, ["Maple Ave", "Oak St", "Elm Rd"][i], 7.5, INK, "khand") + t(x + 8, 84 + i * 44, ["9:00", "11:00", "1:30"][i], 6.5, MUTE) for i in range(3 - j))
    else: o += t(14, 50, "Visits Today", 11, INK, "khand") + "".join(ln(58 + i * 26) + t(14, 74 + i * 26, a, 8, INK) + t(140, 74 + i * 26, b, 7.5, MUTE) + tag(188, 64 + i * 26, s, c) for i, (a, b, s, c) in enumerate([("1418 Maple Ave", "9:00", "Done", JUNGLE), ("22 Oak St", "11:00", "Late", TERRA), ("80 Elm Rd", "1:30", "Today", LAGOON), ("5 Pine Ct", "3:30", "Today", LAGOON)]))
    return screen(o, head=False)
add(G, "Console Day View", O("op_board", "Visits As A Board: Today, Late, Done", "Three columns of cards.", ["visual", "system"], "system", op("board")),
    O("op_table", "Visits As A Table With Status Tags", "Rows with colored tags.", ["system", "simple"], "system", op("table")), "Board Or Table?", "new")
def op_kpi(kind):
    o = rect(0, 0, W, 30, "#FFFFFF") + roof_logo(14, 20, .8) + ln(30, 0, W) + t(14, 50, "This Week", 11, INK, "khand")
    k = [("38", "Visits", LAGOON), ("3", "Fix Now", TERRA), ("12", "Watch", SAFFRON), ("214", "Members", JUNGLE)]
    if kind == "tiles": o += "".join(rect(14 + (i % 2) * 108, 60 + (i // 2) * 60, 104, 54, "#FFFFFF", LINE, 6) + t(22 + (i % 2) * 108, 88 + (i // 2) * 60, n, 20, c, "khand") + t(22 + (i % 2) * 108, 102 + (i // 2) * 60, l, 7, MUTE) for i, (n, l, c) in enumerate(k))
    else: o += bars(30, 70, [.5, .7, .6, .9, .8], [LAGOON], 24, 14, 80, ["M", "T", "W", "T", "F"]) + t(14, 190, "38 Visits · 3 Fix Now · 12 Watch", 8.5, INK, "hind", 600)
    return screen(o, head=False)
add(G, "Console Numbers", O("op_tiles", "Week As Four Colored Number Tiles", "Visits, Fix Now, Watch, Members.", ["visual", "lively"], "neighbor", op_kpi("tiles")),
    O("op_chart", "Week As A Bar Chart", "Visits per day plus one summary line.", ["system", "visual"], "system", op_kpi("chart")), "Tiles Or Chart?", "new")
def op_assign(kind):
    o = rect(0, 0, W, 30, "#FFFFFF") + roof_logo(14, 20, .8) + ln(30, 0, W) + t(14, 50, "Assign Visit · 22 Oak St", 10, INK, "khand")
    if kind == "drag": o += rect(14, 60, 212, 30, CREAM, TERRA, 4, 1.5, 'stroke-dasharray="4 3"') + t(120, 79, "Drag A Tech Here", 8, TERRA, "hind", 600, "middle") + "".join(rect(14, 100 + i * 36, 212, 30, "#FFFFFF", LINE, 4) + techface(30, 113 + i * 36, 8) + t(46, 119 + i * 36, f"Licensed Tech {i+1}", 9, INK, "khand") + t(218, 119 + i * 36, f"{3-i} Stops", 7, MUTE, anchor="end") for i in range(3))
    else: o += field(60, "Tech", "Licensed Tech 2 · 2 Stops") + field(96, "Time", "11:00 AM") + btn(140, "Assign", "fill", INK, h=24, size=8)
    return screen(o, head=False)
add(G, "Console Assign", O("op_drag", "Assign By Dragging A Tech Card", "Drop zone plus tech cards with load.", ["visual", "system"], "system", op_assign("drag")),
    O("op_form", "Assign With Two Dropdowns", "Tech and time, one button.", ["system", "simple"], "system", op_assign("form")), "Drag Or Dropdowns?", "new")
def op_alert(kind):
    o = rect(0, 0, W, 30, "#FFFFFF") + roof_logo(14, 20, .8) + ln(30, 0, W)
    if kind == "banner": o += rect(0, 30, W, 30, TERRA + "1F") + warn(10, 36, TERRA, .7) + t(32, 50, "3 Fix Now Items Need A Call Today", 8.5, INK, "hind", 600)
    else: o += bell(206, 6, TERRA) + dot(222, 8, 5, TERRA) + t(222, 10, "3", 6, "#FFFFFF", "hind", 600, "middle")
    return screen(o + t(14, 82, "Visits Today", 11, INK, "khand") + rows(90, [("1418 Maple Ave", "Done"), ("22 Oak St", "Late"), ("80 Elm Rd", "1:30")], 24), head=False)
add(G, "Console Alerts", O("op_banner", "Urgent Items As A Terracotta Banner", "Strip across the top.", ["lively", "visual"], "neighbor", op_alert("banner")),
    O("op_bell", "Urgent Items Behind A Bell Badge", "Count on a bell.", ["system", "simple"], "system", op_alert("bell")), "Banner Or Bell?", "new")

G = "Empty And Success States"
def empty(kind):
    o = h1(14, 56, "Visit Log", 18)
    if kind == "ill": o += house_ill(30, 80, 1, "#5B5550", "#6B4B3A", "#B8CCD8", SAFFRON) + t(120, 210, "Your First Visit Will Show Here", 11, INK, "khand", anchor="middle")
    else: o += rect(14, 80, 212, 110, "#FFFFFF", "#CFC8BC", 6, 1, 'stroke-dasharray="4 3"') + icon("cal", 108, 112, 24, "outline") + t(120, 160, "No Visits Yet", 11, INK, "khand", anchor="middle")
    return scr(o + t(120, 226, "First visit: Tue, Nov 4 · 9 AM", 8, MUTE, anchor="middle") + btn(244, "Add To Calendar", "outline", h=22, size=8))
add(G, "Empty Visit Log", O("es_ill", "Empty State With A Drawn House", "Warm illustration and a line.", ["neighbor", "visual"], "neighbor", empty("ill")),
    O("es_dash", "Empty State With A Dashed Box", "Plain dashed placeholder.", ["system", "simple"], "system", empty("dash")), "Drawing Or Dashed Box?", "new")
def success(kind):
    if kind == "confetti": o = "".join(rect(20 + (k * 37) % 200, 40 + (k * 23) % 90, 5, 9, [TERRA, LAGOON, JUNGLE, SAFFRON][k % 4], extra=f'transform="rotate({k*29} {22+(k*37)%200} {44+(k*23)%90})"') for k in range(26)) + dot(120, 120, 26, JUNGLE) + icon("check", 102, 102, 36, "outline", "#FFFFFF").replace(INK, "#FFFFFF")
    else: o = dot(120, 110, 30, JUNGLE + "22") + icon("check", 100, 90, 40, "duo", JUNGLE)
    return scr(o + t(120, 176, "Welcome To Up Keep", 17, INK, "khand", anchor="middle") + t(120, 192, "Your first visit is booked.", 8, MUTE, anchor="middle") + btn(240, "See My Home", "fill", INK, h=24, size=8))
add(G, "Sign-Up Success", O("es_confetti", "Success With Four-Color Confetti", "Small pops of all four colors.", ["lively", "visual"], "neighbor", success("confetti")),
    O("es_check", "Success With One Green Check", "Calm single check.", ["system", "simple"], "system", success("check")), "Confetti Or Check?", "new")
def empty_ask(kind):
    o = h1(14, 56, "Ask Anything", 18)
    if kind == "tech": o += techface(120, 100, 20) + t(120, 204, LT, 13, INK, "khand", anchor="middle") + t(120, 220, "Ask me anything about your home.", 8, MUTE, anchor="middle")
    else: o += "".join(rect(14, 76 + i * 30, 212, 24, "#FFFFFF", LINE, 12) + t(24, 92 + i * 30, q, 8, INK) for i, q in enumerate(["Why does my furnace click?", "How often should I flush?", "Is this leak urgent?"]))
    return scr(o + rect(14, 262, 212, 22, "#FFFFFF", "#CFC8BC", 11) + t(24, 276, "Type A Question", 7.5, "#A3A3A3"))
add(G, "Empty Ask Screen", O("es_ask_tech", "Empty Ask With Your Licensed Tech", "Face and one line.", ["neighbor", "visual"], "neighbor", empty_ask("tech")),
    O("es_ask_q", "Empty Ask With Three Sample Questions", "Tap a question to start.", ["system", "visual"], "system", empty_ask("q")), "Tech Or Samples?", "new")
def visit_done(kind):
    o = (rect(0, 35, W, 120, JUNGLE + "14") if kind == "band" else "") + dot(120, 86, 22, JUNGLE) + icon("check", 104, 70, 32, "outline").replace(INK, "#FFFFFF")
    o += t(120, 134, "Fall Visit Done", 17, INK, "khand", anchor="middle") + rows(162, [("Checks Done", "11"), ("To Watch", "1"), ("Fix Now", "0")], 22)
    return scr(o + btn(250, "See Photos", "fill", INK, h=24, size=8))
add(G, "Visit Done State", O("es_vd_band", "Visit Done With A Soft Green Band", "Green tint behind the check.", ["lively", "visual"], "neighbor", visit_done("band")),
    O("es_vd_white", "Visit Done On Plain White", "Check on white.", ["system", "simple"], "system", visit_done("white")), "Green Band Or White?", "new")

G = "QR Landing Page"
def qrl(kind):
    o = (rect(0, 35, W, 30, LAGOON + "14") + qr(14, 40, 20) + t(42, 54, "You Scanned The Yard Sign On Maple Ave", 7.5, INK, "hind", 600)) if kind == "ctx" else ""
    y = 86 if kind == "ctx" else 56
    o += h1(14, y, "Your Home, Taken Care Of.", 20) + rect(14, y + 8, 34, 3, TERRA) + para(14, y + 26, ["Four visits a year by Your Licensed Tech."], 8.2, MUTE)
    o += t(14, y + 58, PRICE, 11, INK, "khand") + t(14, y + 72, "Cancel Anytime", 7.5, JUNGLE, "hind", 600)
    return scr(o + field(196, "ZIP Code", "48067") + btn(236, "Check My Address", "fill", INK, h=26, size=8.5))
add(G, "QR Landing Top", O("ql_ctx", "Landing Says Where You Scanned", "A lagoon strip: 'You Scanned The Yard Sign On Maple Ave'.", ["neighbor", "system"], "neighbor", qrl("ctx")),
    O("ql_plain", "Landing Starts With The Headline", "Same page, no scan note.", ["system", "simple"], "system", qrl("plain")), "Scan Note Or Straight In?", "new")
def qrl_proof(kind):
    o = h1(14, 56, "Your Neighbors Use Up Keep", 15)
    if kind == "map": o += rect(14, 66, 212, 110, "#E8EEE6", r=6) + "".join(dot(30 + (k * 41) % 190, 76 + (k * 29) % 90, 4, JUNGLE) for k in range(14)) + dot(120, 120, 6, TERRA)
    else: o += rect(14, 66, 212, 60, CREAM, LINE, 6) + t(22, 96, "23 Homes On Your Street", 14, INK, "khand") + t(22, 112, "Within half a mile of this sign.", 7.5, MUTE)
    return scr(o + t(14, 200, PRICE, 10, INK, "khand") + t(14, 214, "Cancel Anytime", 7.5, JUNGLE, "hind", 600) + btn(236, "Get Started", "fill", INK, h=26, size=8.5))
add(G, "QR Neighbor Proof", O("ql_map", "Neighbor Proof As A Dot Map", "Green dots for member homes nearby.", ["neighbor", "visual"], "neighbor", qrl_proof("map")),
    O("ql_count", "Neighbor Proof As One Number", "'23 Homes On Your Street'.", ["system", "neighbor"], "system", qrl_proof("count")), "Dot Map Or Number?", "new")
def qrl_cta(kind):
    o = h1(14, 56, "Get Started", 18) + t(14, 72, PRICE, 10, INK, "khand")
    if kind == "call": o += btn(90, "Check My Address", "fill", INK, h=26, size=8.5) + btn(122, "Call Us", "outline", INK, h=26, size=8.5)
    else: o += field(88, "ZIP Code", "48067") + btn(126, "Check My Address", "fill", INK, h=26, size=8.5)
    return scr(o + t(120, 176, "Cancel Anytime", 7.5, JUNGLE, "hind", 600, "middle"))
add(G, "QR Action", O("ql_call", "Two Buttons: Check Address, Call Us", "Black and outlined buttons.", ["system", "neighbor"], "system", qrl_cta("call")),
    O("ql_zip", "ZIP Box Right On The Page", "Type ZIP, one button.", ["system", "simple"], "system", qrl_cta("zip")), "Two Buttons Or ZIP Box?", "new")
def qrl_vid(kind):
    o = h1(14, 56, "See A Visit In 60 Seconds", 15)
    if kind == "poster": o += photo(14, 66, 212, 120, "tech", 6) + dot(120, 126, 18, "#FFFFFFDD") + f'<path d="M114 116 L130 126 L114 136 Z" fill="{TERRA}"/>'
    else: o += "".join(rect(14, 66 + i * 40, 212, 34, "#FFFFFF", LINE, 6) + icon(k, 22, 74 + i * 40, 18, "duo", c) + t(48, 87 + i * 40, s, 9.5, INK, "khand") for i, (k, s, c) in enumerate([("cal", "We Book Your Visit", LAGOON), ("check", "Your Licensed Tech Checks 11 Things", JUNGLE), ("cam", "You Get Photos", TERRA)]))
    return scr(o + btn(236, "Get Started", "fill", INK, h=26, size=8.5))
add(G, "QR Explainer", O("ql_video", "Short Video Poster", "A tap-to-play visit video.", ["visual", "lively"], "neighbor", qrl_vid("poster")),
    O("ql_steps", "Three Icon Steps", "Book, Check, Photos.", ["system", "visual"], "system", qrl_vid("steps")), "Video Or Steps?", "new")

# ---- rule checks ----
blob = json.dumps(pairs).lower()
for bad in ["by max weberman", "built by max", " ai ", "health score", "danny", "basic", "premium", "license #", "lic #", "refund", "money back", "emoji"]:
    assert bad not in blob, bad
import re
prices = set(re.findall(r"\$\d+[^<\"]{0,12}", json.dumps(pairs)))
assert all(p.startswith("$99") for p in prices), prices
draft_svg.finish(DID, "Up Keep Round 6: Building On Your Picks, Skipped Pairs Asked Anew (Van Stripe Medium vs Saffron Pinline), Dashboard, Plan Change, Neighbor Referral, Seasonal Checklist, Tech Photo Capture, Operator Console, Empty And Success States, QR Landing Page", "Up Keep", pairs, 0,
    {"builds_on": "upkeep-5 picks (reconstructed: /workspace/smartkeep/branding/upkeep-5-picks.md)",
     "brands": ["Up Keep / Smart Upkeep: white light mode, Khand/Hind, small pops of #C1502E, #05668D, #0B6E4F, #D4A017"],
     "feelings": {"system": "Clear system", "neighbor": "Friendly neighbor"},
     "sources": {"previous_deck": "decks/upkeep-5.json", "picks": "/workspace/smartkeep/branding/upkeep-5-picks.md"}}, seed=66)
d = json.load(open(f"decks/{DID}.json")); d.pop("draft", None); d["status"] = "published"
json.dump(d, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
