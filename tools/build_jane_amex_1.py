#!/usr/bin/env python3
"""DRAFT Style Swipe deck jane-amex-1: 25 this-or-that pairs for Mom's Amex Offers (Jane's phone; info only, not selling).
Starts from the queued Mom's Amex pairs in queue/blog-topics.md and expands toward big readable, simple, elder-friendly options.
All offers shown are fake examples; no account data. Run from the repo root."""
import sys; sys.path.insert(0, "tools")
from draft_svg import *
DID = "jane-amex-1"; pairs, O, add = mk("ja1_", "Mom's Amex Offers")
OFF = [("Corner Bakery Co.", "$10 Back", "Spend $40 or more", "Oct 30", True), ("Green Leaf Grocery", "$15 Back", "Spend $75 or more", "Nov 12", False),
       ("Sunset Cinema", "$5 Back", "Spend $20 or more", "Oct 20", True), ("Blue Harbor Hotels", "$50 Back", "Spend $250 or more", "Dec 31", False),
       ("Maple Pharmacy", "10% Back", "Up to $20 back", "Nov 5", False), ("Riverside Garden", "$20 Back", "Spend $100 or more", "Nov 30", False)]
def head(big=False, accent=None, sub="Updated Oct 13 · Example Offers"):
    return (t(14, 22, "MAX WEBERMAN", 6, MUTE, "hind", 600, extra='letter-spacing="1.4"') + h1(14, 44 if not big else 46, "Mom's Amex Offers", 20 if big else 17)
            + t(14, 58, sub, 7.5 if big else 6.5, MUTE) + (rect(14, 62, 30, 3, accent) if accent else "") + ln(68))
def tile(x, y, name, s=22, c=INK):
    return rect(x, y, s, s, "#FFFFFF", LINE, 5) + t(x + s / 2, y + s * .72, name[0], s * .62, c, "khand", anchor="middle")
def soon(x, y, mode, big=False):
    if mode == "accent": return tag(x, y, "Ends Soon", TERRA, False, 7 if big else 5.8)
    if mode == "saffron": return tag(x, y, "Ends Soon", SAFFRON, False, 7 if big else 5.8)
    if mode == "lagoon": return tag(x, y, "Ends Soon", LAGOON, False, 7 if big else 5.8)
    return t(x, y + 8, "Ends Soon", 7 if big else 6, INK, "hind", 600)
def tabbar(acc=None, cur=0):
    o = rect(0, 266, W, 34, "#FFFFFF") + ln(266, 0, W)
    for i, (n, k) in enumerate([("For You", "home"), ("Search", "search"), ("Saved", "heart"), ("Share", "phone")]):
        cx = 30 + i * 60; c = (acc or INK) if i == cur else "#A3A3A3"; o += ic(k, cx - 7, 271, 14, c) + t(cx, 294, n.upper(), 5.6, c, "hind", 600, "middle")
        if i == cur: o += rect(cx - 10, 297, 20, 2, acc or INK)
    return o
def rows(size="std", acc=None, soonmode="plain", ni="link", n=5, tabs=True, amt_col=INK):
    big = size == "big"; o = head(big, acc); rh = 52 if big else 40
    for i, (m, a, c, d, s) in enumerate(OFF[:n]):
        y = 74 + i * rh
        if y + rh > 266: break
        o += tile(14, y + 6, m, 26 if big else 22) + t(48, y + 16, m, 9 if big else 7.5, MUTE, "hind", 600) + t(48, y + (36 if big else 30), a, 18 if big else 13, amt_col, "khand")
        o += t(226, y + 16, "Ends " + d, 9 if big else 7, INK if big else MUTE, "hind", 600, "end")
        if s: o += soon(226 - (60 if big else 48), y + (24 if big else 20), soonmode, big)
        o += ln(y + rh - 2)
    return screen(o + (tabbar(acc) if tabs else ""))
def az(open_i=None, size="std", acc=None):
    big = size == "big"; o = head(big, acc); y = 74; srt = sorted(OFF)
    for i, (m, a, c, d, s) in enumerate(srt):
        if y > 250: break
        hh = 30 if big else 26
        o += t(14, y + hh * .64, m, 11 if big else 9.5, INK, "hind", 600) + ic("down" if open_i == i else "chev", 206, y + 4, 16, MUTE)
        if open_i == i:
            o += rect(14, y + hh, 212, 70, SOFT, "none", 6) + t(24, y + hh + 28, a, 22, INK, "khand") + t(24, y + hh + 44, c, 9, INK) + t(24, y + hh + 60, "Ends " + d, 9, INK, "hind", 600); y += 72
        o += ln(y + hh); y += hh + 2
    return screen(o + tabbar(acc))
def steps(mode, big=True):
    o = head(True)
    if mode == "vague":
        o += rect(14, 80, 212, 60, SOFT, "none", 8) + t(24, 104, "Looks like there's a deal.", 10, INK) + t(24, 120, "Log into Amex to check it out.", 10, INK)
    else:
        o += h1(14, 92, "How To Use An Offer", 15)
        for i, s in enumerate(["Open the Amex app", "Tap Offers, find this store", "Tap Add To Card, then shop"]):
            y = 104 + i * 44; o += dot(30, y + 16, 13, LAGOON if mode == "steps_color" else INK) + t(30, y + 21, str(i + 1), 13, "#FFFFFF", "khand", anchor="middle") + t(52, y + 21, s, 11 if big else 9, INK, "hind", 600)
    return screen(o + tabbar())
def steps_where(mode):
    o = head(True)
    o += tile(14, 80, "Corner Bakery", 30) + t(52, 92, "Corner Bakery Co.", 10, MUTE, "hind", 600) + t(52, 114, "$10 Back", 24, INK, "khand") + t(14, 140, "Spend $40 or more · Ends Oct 30", 9, INK)
    if mode == "inline": o += rect(14, 152, 212, 104, SOFT, "none", 8) + "".join(t(24, 176 + i * 26, f"{i+1}. {s}", 10.5, INK, "hind", 600) for i, s in enumerate(["Open the Amex app", "Tap Offers, find this store", "Tap Add To Card"]))
    else: o += btn(160, "How Do I Use This?", "outline", INK, h=34, size=9) + t(120, 220, "Opens 3 simple steps", 8, MUTE, anchor="middle")
    return screen(o + tabbar())
def card_view(size="std", acc=None, ni="link", detail="short"):
    big = size == "big"; o = head(big, acc); m, a, c, d, s = OFF[0]
    o += rect(14, 76, 212, 182, "#FFFFFF", LINE, 10) + tile(26, 88, m, 34) + t(70, 104, m, 10 if big else 8.5, MUTE, "hind", 600) + t(26, 160, a, 44 if big else 30, INK, "khand")
    o += t(26, 182, c, 11 if big else 8.5, INK) + t(26, 202, "Ends " + d, 12 if big else 8.5, INK, "hind", 600) + soon(150, 192, "accent" if acc else "plain", big)
    if ni == "link": o += t(214, 244, "NOT INTERESTED", 6.5 if not big else 8, MUTE, "hind", 600, "end", 'letter-spacing="1"')
    elif ni == "button": o += rect(26, 222, 188, 26, "#FFFFFF", "#BDB6AA", 0) + t(120, 239, "NOT INTERESTED", 8, INK, "hind", 600, "middle", 'letter-spacing="1"')
    return screen(o + tabbar(acc))
def undo(mode):
    o = head(True) + rows_inner(1)
    if mode == "toast": o += rect(14, 222, 212, 36, INK, "none", 6) + t(26, 244, "Hidden: Sunset Cinema", 9, "#FFFFFF") + ic("undo", 172, 230, 14, "#FFFFFF") + t(206, 244, "UNDO", 8, "#FFFFFF", "hind", 600, "middle")
    elif mode == "bigundo": o += rect(14, 200, 212, 58, "#FFFFFF", INK, 0, 1.5) + t(120, 222, "Sunset Cinema Hidden", 11, INK, "khand", anchor="middle") + rect(70, 230, 100, 22, INK) + ic("undo", 82, 234, 13, "#FFFFFF") + t(130, 245, "UNDO", 8, "#FFFFFF", "hind", 600, "middle")
    elif mode == "none": o += t(120, 236, "Sunset Cinema was hidden.", 8.5, MUTE, anchor="middle")
    elif mode == "confirm": o += rect(0, 0, W, H, INK, extra='opacity=".3"') + rect(24, 96, 192, 120, "#FFFFFF", "none", 10) + t(120, 128, "Hide Sunset Cinema?", 13, INK, "khand", anchor="middle") + t(120, 146, "You can bring it back from Saved.", 8, MUTE, anchor="middle") + rect(36, 168, 80, 30, "#FFFFFF", INK, 0, 1.3) + t(76, 187, "KEEP", 8, INK, "hind", 600, "middle") + rect(124, 168, 80, 30, INK, INK, 0) + t(164, 187, "HIDE", 8, "#FFFFFF", "hind", 600, "middle")
    return screen(o + tabbar())
def rows_inner(skip):
    o = ""
    for i, (m, a, c, d, s) in enumerate([x for j, x in enumerate(OFF) if j != 2][:3]):
        y = 74 + i * 44; o += tile(14, y + 6, m, 24) + t(46, y + 15, m, 8.5, MUTE, "hind", 600) + t(46, y + 33, a, 15, INK, "khand") + t(226, y + 15, "Ends " + d, 8, INK, "hind", 600, "end") + ln(y + 42)
    return o
def hidden(mode):
    o = head(True) + h1(14, 92, "Hidden Offers", 15)
    for i, (m, a, c, d, s) in enumerate(OFF[2:5]):
        y = 102 + i * 44; o += t(14, y + 18, m, 10, INK, "hind", 600) + t(14, y + 32, a, 9, MUTE)
        o += (rect(152, y + 8, 74, 24, "#FFFFFF", INK, 0, 1.3) + t(189, y + 24, "BRING BACK", 7, INK, "hind", 600, "middle")) if mode == "button" else t(226, y + 24, "BRING BACK", 7, LAGOON, "hind", 600, "end", 'text-decoration="underline"')
        o += ln(y + 42)
    return screen(o + tabbar(cur=2))
def footer(mode):
    o = head(False) + rows_inner(0)
    if mode == "full": o += ln(214, 0, W) + t(120, 232, "Made For Mom By Max", 9, INK, "khand", anchor="middle") + t(120, 246, "Offers change often. Check the Amex app.", 7, MUTE, anchor="middle") + t(120, 258, "Questions? Text Max.", 7, MUTE, anchor="middle")
    elif mode == "small": o += t(120, 250, "Made For Mom By Max", 7, MUTE, anchor="middle")
    elif mode == "call": o += rect(14, 214, 212, 40, SOFT, "none", 8) + ic("phone", 24, 222, 22, INK) + t(54, 232, "Need Help?", 11, INK, "khand") + t(54, 246, "Tap to text Max", 8, MUTE)
    elif mode == "none": pass
    elif mode == "updated": o += t(120, 236, "Offers Last Checked Oct 13", 9, INK, "hind", 600, "middle") + t(120, 250, "Max updates this list each week.", 7.5, MUTE, anchor="middle")
    return screen(o + tabbar())
def tabs_acc(acc, bg_head=False):
    o = rows("std", acc, "accent" if acc == TERRA else ("lagoon" if acc == LAGOON else ("saffron" if acc == SAFFRON else "plain")))
    return o
def search(mode):
    o = head(True) + rect(14, 76, 212, 34, "#FFFFFF", INK, 0, 1.5) + ic("search", 22, 84, 18, MUTE) + t(48, 98, "Type a store name", 10, "#A3A3A3")
    if mode == "chips": o += "".join(rect(14 + i * 72, 120, 68, 26, INK if i == 0 else "#FFFFFF", INK, 0, 1.2) + t(48 + i * 72, 137, s, 8.5, "#FFFFFF" if i == 0 else INK, "hind", 600, "middle") for i, s in enumerate(["All", "Food", "Travel"]))
    else: o += "".join(t(14, 136 + i * 28, s, 11, INK, "hind", 600) + ic("chev", 206, 122 + i * 28, 16, MUTE) + ln(144 + i * 28) for i, s in enumerate(["Food And Groceries", "Travel", "Health"]))
    return screen(o + tabbar(cur=1))
def saved(mode):
    o = head(True) + h1(14, 92, "Saved Offers", 15)
    for i, (m, a, c, d, s) in enumerate(OFF[:3]):
        y = 102 + i * (52 if mode == "big" else 38)
        o += ic("heart", 14, y + 6, 16 if mode != "big" else 20, TERRA) + t(42, y + 18, m, 10 if mode == "big" else 8.5, INK, "hind", 600) + t(42, y + (38 if mode == "big" else 30), a + " · Ends " + d, 11 if mode == "big" else 8, INK if mode == "big" else MUTE, "hind", 600) + ln(y + (50 if mode == "big" else 36))
    return screen(o + tabbar(cur=2))
def contrast(mode):
    o = head(True); m, a, c, d, s = OFF[1]
    col = MUTE if mode == "grey" else INK
    o += t(14, 100, m, 11, col, "hind", 600) + t(14, 140, a, 36, INK, "khand") + t(14, 164, c, 11, col) + t(14, 184, "Ends " + d, 11, col, "hind", 600)
    return screen(o + tabbar())
def dates(mode):
    o = head(True)
    for i, (m, a, c, d, s) in enumerate(OFF[:4]):
        y = 76 + i * 46; o += t(14, y + 18, m, 9.5, INK, "hind", 600) + t(14, y + 36, a, 15, INK, "khand")
        if mode == "full": o += t(226, y + 28, ["Thursday, Oct 30", "Wednesday, Nov 12", "Monday, Oct 20", "Wednesday, Dec 31"][i], 8.5, INK, "hind", 600, "end")
        elif mode == "days": o += t(226, y + 28, ["17 Days Left", "30 Days Left", "7 Days Left", "79 Days Left"][i], 9, TERRA if i == 2 else INK, "hind", 600, "end")
        else: o += t(226, y + 28, "Ends " + d, 9, INK, "hind", 600, "end")
        o += ln(y + 44)
    return screen(o + tabbar())
def sections(mode):
    o = head(True)
    if mode == "one":
        o += lbl(14, 84, "All Offers · A To Z") + "".join(t(14, 106 + i * 26, m, 11, INK, "hind", 600) + t(226, 106 + i * 26, a, 11, INK, "khand", anchor="end") + ln(114 + i * 26) for i, (m, a, c, d, s) in enumerate(sorted(OFF)))
    else:
        o += lbl(14, 84, "Your Stores") + "".join(t(14, 104 + i * 24, m, 10.5, INK, "hind", 600) + t(226, 104 + i * 24, a, 10.5, INK, "khand", anchor="end") for i, (m, a, c, d, s) in enumerate(OFF[:2]))
        o += lbl(14, 168, "Everything Else") + "".join(t(14, 188 + i * 24, m, 10.5, INK, "hind", 600) + t(226, 188 + i * 24, a, 10.5, INK, "khand", anchor="end") for i, (m, a, c, d, s) in enumerate(OFF[2:5]))
    return screen(o + tabbar())
def welcome(mode):
    o = t(14, 22, "MAX WEBERMAN", 6, MUTE, "hind", 600, extra='letter-spacing="1.4"')
    if mode == "hello": o += h1(14, 60, "Hi Mom", 30) + t(14, 82, "Here are this week's Amex offers.", 10, INK) + t(14, 98, "6 Example Offers · Updated Oct 13", 8, MUTE)
    else: o += h1(14, 48, "Mom's Amex Offers", 17) + t(14, 62, "Updated Oct 13 · Example Offers", 7, MUTE)
    o += ln(110 if mode == "hello" else 70) + "".join(t(14, (132 if mode == "hello" else 92) + i * 28, m, 11, INK, "hind", 600) + t(226, (132 if mode == "hello" else 92) + i * 28, a, 12, INK, "khand", anchor="end") for i, (m, a, c, d, s) in enumerate(OFF[:4]))
    return screen(o + tabbar())

G1, G2, G3, G4, G5, G6, G7, G8 = "List Layout", "How To Use An Offer", "Bigger Dates And Amounts", "Not Interested And Undo", "Footer", "Gentle Accent", "Offer Detail", "Home And Finding Things"
add(G1, "List: Layout", O("ls_rows", "Long Rows, One Under Another", "Every offer as a row: store, amount, end date.", ["simple", "readable", "overview"], "plain", rows("big")), O("ls_az", "A To Z List, Tap To Open", "Store names A to Z; tap one to see the deal.", ["simple", "tidy", "easy"], "plain", az(1, "big")), "Long Rows Or A To Z Tap-To-Open?")
add(G1, "List: A To Z Open State", O("ls_az_open", "A To Z With One Store Open", "The tapped store opens with a big amount.", ["guided", "big"], "warm", az(2, "big")), O("ls_az_closed", "A To Z All Closed", "Just store names until she taps.", ["calm", "minimal"], "plain", az(None, "big")), "Show One Open Or All Closed?")
add(G1, "List: Row Height", O("ls_rows_tall", "Tall Rows, Fewer On Screen", "Bigger rows, about 4 on screen.", ["big", "readable"], "warm", rows("big")), O("ls_rows_short", "Short Rows, More On Screen", "Smaller rows, about 5 on screen.", ["compact", "overview"], "plain", rows("std")), "Tall Or Short Rows?")
add(G1, "List: Sections", O("ls_sec_one", "One A To Z List", "Every offer in one list.", ["simple", "easy"], "plain", sections("one")), O("ls_sec_two", "Your Stores, Then Everything Else", "Two plain sections.", ["guided", "personal"], "warm", sections("two")), "One List Or Two Sections?")
add(G1, "List: Card Or Row", O("ls_one_card", "One Big Offer Card", "One offer fills the screen.", ["big", "focused"], "warm", card_view("big")), O("ls_list_rows", "A Plain List Of Rows", "Several offers at once.", ["overview", "simple"], "plain", rows("big", None, "plain", "link", 4)), "One Card Or A List?")
add(G1, "List: Store Initial", O("ls_tile_on", "Store Initial Tile On Each Row", "A big letter tile next to each store.", ["visual", "easy"], "warm", rows("big")), O("ls_tile_az", "Names Only, No Tiles", "A To Z names with no tile.", ["minimal", "clean"], "plain", az(None, "std")), "Letter Tiles Or Names Only?")
add(G2, "Steps: Wording", O("st_vague", "Short 'Log Into Amex' Line", "One line telling her to log into Amex.", ["short", "quiet"], "plain", steps("vague")), O("st_three", "3 Plain Numbered Steps", "Open the app, tap Offers, tap Add To Card.", ["guided", "readable", "easy"], "warm", steps("steps")), "One Line Or 3 Steps?", "check")
add(G2, "Steps: Number Color", O("st_ink", "Black Step Numbers", "Steps in black circles.", ["calm", "plain"], "plain", steps("steps")), O("st_lagoon", "Lagoon Step Numbers", "Steps in soft lagoon circles.", ["gentle", "visual"], "warm", steps("steps_color")), "Black Or Lagoon Numbers?")
add(G2, "Steps: Where They Go", O("st_inline", "Steps Under Every Offer", "The 3 steps show on each offer.", ["guided", "easy"], "warm", steps_where("inline")), O("st_button", "'How Do I Use This?' Button", "One button opens the steps.", ["simple", "clean"], "plain", steps_where("button")), "Steps Always Shown Or Behind A Button?")
add(G2, "Steps: Text Size", O("st_big", "Big Step Text", "Steps at large size.", ["big", "readable"], "warm", steps("steps", True)), O("st_std", "Standard Step Text", "Steps at normal size.", ["compact", "plain"], "plain", steps("steps", False)), "How Big Are The Steps?")
add(G2, "Steps: Steps Color On Big", O("st_lag_big", "Big Steps In Lagoon", "Large text, lagoon numbers.", ["big", "gentle"], "warm", steps("steps_color", True)), O("st_lag_std", "Standard Steps In Lagoon", "Normal text, lagoon numbers.", ["compact", "gentle"], "plain", steps("steps_color", False)), "Big Or Standard With Lagoon?")
add(G3, "Size: Amounts", O("sz_big", "Bigger Amounts And Dates", "$10 Back at large size, dates in black.", ["big", "readable"], "warm", rows("big")), O("sz_std", "Current Text Size", "Today's sizes.", ["compact", "familiar"], "plain", rows("std")), "Bigger Or Current Size?", "check")
add(G3, "Size: Date Style", O("sz_date_full", "Full Day And Date", "'Thursday, Oct 30'.", ["clear", "readable"], "warm", dates("full")), O("sz_date_days", "Days Left", "'7 Days Left', the soonest in terracotta.", ["urgent", "easy"], "plain", dates("days")), "Full Date Or Days Left?")
add(G3, "Size: Date Short", O("sz_date_ends", "'Ends Oct 30'", "Short date in bold black.", ["simple", "short"], "plain", dates("ends")), O("sz_date_full2", "'Thursday, Oct 30' On The Card", "Full date on one big card.", ["readable", "big"], "warm", card_view("big")), "Short Date Or Full Date?")
add(G3, "Size: Text Color", O("sz_dark", "All Text In Dark Black", "Store, terms and date in near-black.", ["readable", "high-contrast"], "warm", contrast("dark")), O("sz_grey", "Grey Details, Black Amount", "Details in grey, amount in black.", ["soft", "layered"], "plain", contrast("grey")), "All Dark Or Grey Details?")
add(G3, "Size: Card Amount", O("sz_card_big", "Huge Amount On The Card", "Amount at 44 pt.", ["big", "readable"], "warm", card_view("big")), O("sz_card_std", "Normal Amount On The Card", "Amount at 30 pt.", ["balanced", "plain"], "plain", card_view("std")), "How Big Is The Amount?")
add(G3, "Size: Header", O("sz_head_big", "Bigger Header Text", "Larger title and updated line.", ["readable", "big"], "warm", rows("big", None, "plain", "link", 4)), O("sz_head_std", "Small Header Text", "Smaller title area, more room for offers.", ["compact", "efficient"], "plain", rows("std", None, "plain", "link", 4, True)), "Big Or Small Header?")
add(G3, "Size: Saved List", O("sz_saved_big", "Big Saved List", "Large saved rows with amount and date.", ["big", "readable"], "warm", saved("big")), O("sz_saved_std", "Compact Saved List", "Smaller saved rows.", ["compact", "overview"], "plain", saved("std")), "Big Or Compact Saved List?")
add(G4, "Not Interested: Undo", O("ni_undo", "Not Interested With Undo", "A dark bar: 'Hidden: Sunset Cinema · Undo'.", ["forgiving", "easy"], "warm", undo("toast")), O("ni_noundo", "Not Interested Without Undo", "A small line saying it was hidden.", ["simple", "final"], "plain", undo("none")), "Undo Or No Undo?", "check")
add(G4, "Not Interested: Undo Size", O("ni_undo_big", "Big Undo Box", "A boxed message with a big Undo button.", ["big", "forgiving"], "warm", undo("bigundo")), O("ni_undo_toast", "Small Undo Bar", "A slim dark bar with Undo.", ["light", "quick"], "plain", undo("toast")), "Big Undo Box Or Small Bar?")
add(G4, "Not Interested: Ask First", O("ni_confirm", "Ask 'Hide This?' First", "A Keep / Hide question before hiding.", ["safe", "guided"], "warm", undo("confirm")), O("ni_direct", "Hide Right Away With Undo", "Hides at once, Undo shows after.", ["fast", "forgiving"], "plain", undo("toast")), "Ask First Or Hide With Undo?")
add(G4, "Not Interested: Button", O("ni_link", "Small 'Not Interested' Text", "Grey caps text at the bottom of the card.", ["quiet", "clean"], "plain", card_view("big", None, "link")), O("ni_button", "Outlined 'Not Interested' Button", "A full-width outlined button.", ["clear", "big"], "warm", card_view("big", None, "button")), "Small Text Or Button?")
add(G4, "Not Interested: Bring Back", O("ni_back_btn", "'Bring Back' Buttons", "Outlined buttons on hidden offers.", ["clear", "big"], "warm", hidden("button")), O("ni_back_link", "'Bring Back' Links", "Small lagoon links.", ["light", "quiet"], "plain", hidden("link")), "Buttons Or Links To Bring Back?")
add(G4, "Not Interested: Hide Option", O("ni_none_card", "No Not Interested At All", "Cards with no hide option.", ["simple", "calm"], "plain", card_view("big", None, "none")), O("ni_link_card", "Keep A Small Not Interested", "Small hide text stays.", ["control", "quiet"], "plain", card_view("std", None, "link")), "Keep Not Interested?")
add(G5, "Footer: Add One?", O("ft_full", "Footer: 'Made For Mom By Max' Plus Help", "Three short lines at the bottom.", ["warm", "personal", "reassuring"], "warm", footer("full")), O("ft_none", "No Footer", "Offers end, nothing below.", ["clean", "minimal"], "plain", footer("none")), "Footer Or No Footer?", "check")
add(G5, "Footer: Size", O("ft_small", "One Small Line", "'Made For Mom By Max' in grey.", ["quiet", "simple"], "plain", footer("small")), O("ft_full2", "Three Lines With A Rule", "Title, note and help line.", ["warm", "guided"], "warm", footer("full")), "One Line Or Three?")
add(G5, "Footer: Help", O("ft_call", "'Need Help? Text Max' Box", "A soft box with a phone icon.", ["helpful", "big", "personal"], "warm", footer("call")), O("ft_updated", "'Offers Last Checked' Line", "When the list was checked.", ["clear", "trust"], "plain", footer("updated")), "Help Box Or Last Checked?")
add(G5, "Footer: Help Or Nothing", O("ft_call2", "Help Box At The Bottom", "Text Max box only.", ["helpful", "warm"], "warm", footer("call")), O("ft_small2", "Small Credit Line Only", "Just a small credit line.", ["minimal", "quiet"], "plain", footer("small")), "Help Box Or Credit Line?")
add(G5, "Footer: Checked Or Credit", O("ft_upd2", "Last Checked Date", "'Offers Last Checked Oct 13'.", ["clear", "reassuring"], "plain", footer("updated")), O("ft_none2", "Nothing At The Bottom", "No footer at all.", ["clean", "minimal"], "plain", footer("none")), "Last Checked Line Or Nothing?")
add(G6, "Accent: Tabs And Ends Soon", O("ac_terra", "Gentle Terracotta Accent", "Active tab and Ends Soon tag in soft terracotta.", ["warm", "gentle", "visual"], "warm", tabs_acc(TERRA)), O("ac_plain", "Plain Black And White", "No accent color.", ["calm", "plain"], "plain", tabs_acc(None)), "Gentle Accent Or Plain?", "check")
add(G6, "Accent: Which Color", O("ac_lagoon", "Gentle Lagoon Accent", "Tab and tag in lagoon blue.", ["calm", "gentle"], "plain", tabs_acc(LAGOON)), O("ac_terra2", "Gentle Terracotta Accent", "Tab and tag in terracotta.", ["warm", "lively"], "warm", rows("std", TERRA, "accent", n=4)), "Lagoon Or Terracotta?")
add(G6, "Accent: Saffron", O("ac_saffron", "Saffron Ends Soon Only", "Only the Ends Soon tag in saffron.", ["warm", "alert"], "warm", rows("std", None, "saffron")), O("ac_lag_soon", "Lagoon Ends Soon Only", "Only the Ends Soon tag in lagoon.", ["calm", "clear"], "plain", rows("std", None, "lagoon")), "Saffron Or Lagoon Tag?")
add(G6, "Accent: Amount Color", O("ac_amt_ink", "Amounts In Black", "Dollar amounts stay black.", ["readable", "calm"], "plain", rows("big", TERRA, "accent")), O("ac_amt_jungle", "Amounts In Green", "Dollar amounts in jungle green.", ["visual", "money"], "warm", rows("big", TERRA, "accent", amt_col=JUNGLE)), "Black Or Green Amounts?")
add(G6, "Accent: Header Rule", O("ac_rule_on", "Small Color Line Under The Title", "A short terracotta rule under the header.", ["warm", "branded"], "warm", rows("big", TERRA, "accent", n=4)), O("ac_rule_off", "No Color Line", "Plain header.", ["clean", "plain"], "plain", rows("big", None, "accent", n=4)), "Color Line Under Title?")
add(G6, "Accent: Ends Soon Tag", O("ac_soon_tag", "Ends Soon As A Soft Tag", "A soft terracotta tag.", ["visual", "gentle"], "warm", rows("big", None, "accent", n=4)), O("ac_soon_text", "Ends Soon As Bold Text", "Bold black words, no tag.", ["plain", "readable"], "plain", rows("big", None, "plain", n=4)), "Tag Or Bold Text?")
add(G6, "Accent: Tab Bar", O("ac_tab_lagoon", "Lagoon Active Tab", "Active tab and underline in lagoon.", ["calm", "clear"], "plain", rows("std", LAGOON, "plain", n=4)), O("ac_tab_ink", "Black Active Tab", "Active tab in black.", ["plain", "classic"], "plain", rows("std", None, "plain", n=4)), "Lagoon Or Black Tab?")
add(G7, "Detail: Card Accent", O("dt_card_terra", "Big Card With Terracotta Ends Soon", "One big card with a soft tag.", ["warm", "big"], "warm", card_view("big", TERRA)), O("dt_card_plain", "Big Card, No Color", "One big card in black and white.", ["plain", "readable"], "plain", card_view("big", None)), "Accent On The Big Card?")
add(G7, "Detail: Steps Placement", O("dt_steps_inline2", "Steps Inside The Offer", "The 3 steps right under the amount.", ["guided", "easy"], "warm", steps_where("inline")), O("dt_steps_page", "Steps On Their Own Page", "A separate 'How To Use' page.", ["clean", "focused"], "plain", steps("steps")), "Steps In The Offer Or A Separate Page?")
add(G7, "Detail: Contrast", O("dt_dark2", "Everything Dark", "All details in black.", ["readable", "high-contrast"], "warm", contrast("dark")), O("dt_card_std2", "Standard Card", "The current card size.", ["familiar", "compact"], "plain", card_view("std", None, "none")), "Dark Details Or Standard Card?")
add(G7, "Detail: Date Emphasis", O("dt_days_left", "Days Left Up Front", "Days left on every row.", ["urgent", "clear"], "plain", dates("days")), O("dt_full_date", "Full Date On Every Row", "Full day and date.", ["calm", "readable"], "warm", dates("full")), "Days Left Or Full Date?")
add(G7, "Detail: One Or All", O("dt_az_open3", "Tap To Open, One At A Time", "A To Z with one opened store.", ["focused", "easy"], "warm", az(0, "big", TERRA)), O("dt_rows_all", "Everything Shown At Once", "All rows with full info.", ["overview", "plain"], "plain", rows("big", TERRA, "accent")), "One At A Time Or All At Once?")
add(G8, "Home: Greeting", O("hm_hello", "'Hi Mom' Greeting", "A big hello, then the offers.", ["warm", "personal", "big"], "warm", welcome("hello")), O("hm_title", "Title Only", "Just 'Mom's Amex Offers'.", ["plain", "compact"], "plain", welcome("title")), "Hi Mom Or Just A Title?")
add(G8, "Search: Filters", O("hm_search_chips", "Search With Three Big Chips", "All, Food, Travel chips.", ["easy", "big"], "warm", search("chips")), O("hm_search_rows", "Search With Category Rows", "Tap a category row.", ["clear", "readable"], "plain", search("rows")), "Chips Or Category Rows?")
add(G8, "Saved: Hearts", O("hm_saved_big", "Saved List With Big Rows", "Hearts, store and amount at large size.", ["big", "warm"], "warm", saved("big")), O("hm_hidden_links", "Hidden List With Links", "Hidden offers with Bring Back links.", ["control", "quiet"], "plain", hidden("link")), "Show Saved Or Hidden First In The Saved Tab?")
add(G8, "Home: Tab Count", O("hm_tabs_four", "Four Tabs At The Bottom", "For You, Search, Saved, Share.", ["familiar", "complete"], "plain", rows("std", None, "plain", n=4)), O("hm_no_tabs", "No Tab Bar, Just The List", "One scrolling list, no tabs.", ["simple", "minimal"], "warm", rows("std", None, "plain", n=5, tabs=False)), "Tabs Or No Tabs?")
add(G8, "Home: Hello Size", O("hm_hello_big", "Big 'Hi Mom' With A List", "Greeting plus four rows.", ["warm", "big"], "warm", welcome("hello")), O("hm_list_big", "Straight To A Big List", "No greeting; big rows start right away.", ["fast", "readable"], "plain", rows("big", None, "plain", n=4)), "Greeting Or Straight To The List?")
add(G8, "Search: Box", O("hm_search_only", "One Big Search Box", "Search box with category rows under it.", ["easy", "readable"], "warm", search("rows")), O("hm_az_list", "No Search, Just A To Z", "An A To Z list instead of search.", ["simple", "calm"], "plain", az(None, "big")), "Search Or A To Z?")
add(G2, "Steps: First Step Wording", O("st_inline_big", "Steps Under The Offer, Big Text", "The 3 steps in large text on the offer.", ["big", "guided"], "warm", steps_where("inline")), O("st_vague2", "Keep The One-Line Hint", "One plain 'log into Amex' line.", ["short", "plain"], "plain", steps("vague")), "Steps On The Offer Or One Line?")
add(G1, "List: A To Z Accent", O("ls_az_terra", "A To Z With A Terracotta Tab", "A To Z list, active tab in terracotta.", ["warm", "gentle"], "warm", az(3, "big", TERRA)), O("ls_az_lagoon", "A To Z With A Lagoon Tab", "A To Z list, active tab in lagoon.", ["calm", "gentle"], "plain", az(3, "big", LAGOON)), "Terracotta Or Lagoon On A To Z?")
add(G7, "Detail: Not Interested On Big Card", O("dt_ni_btn_terra", "Big Card With A Not Interested Button", "Big card, outlined hide button, terracotta tag.", ["clear", "big"], "warm", card_view("big", TERRA, "button")), O("dt_ni_none_terra", "Big Card With No Hide Option", "Big card, no hide option at all.", ["simple", "calm"], "plain", card_view("big", TERRA, "none")), "Hide Button Or None On The Big Card?")
finish(DID, "Mom's Amex Offers Round 1: List Layout, 3 Plain Steps, Bigger Dates And Amounts, Undo, Footer, Gentle Accent", "Mom's Amex Offers", pairs, 0,
       {"brands": ["Mom's Amex Offers: an info-only app on Jane's phone, not a sales page", "White base, near-black ink, Khand/Hind, big readable type, one gentle accent at most"],
        "feelings": {"warm": "Warm and personal", "plain": "Plain and calm"},
        "sources": {"app": "/workspace/amex/offers-app/", "review": "/workspace/ops/reviews/janes-amex/", "queue": "/workspace/style-swipe/queue/blog-topics.md (Mom's Amex section)"},
        "content_note": "All offers are fake examples (Corner Bakery Co., Green Leaf Grocery, etc.); no account data."}, seed=11)
