#!/usr/bin/env python3
"""Build Style Swipe deck scout-1 (PUBLISHED): 25 pairs for the Scout agent (YouTube Shorts channel about daily life in
Thailand). Based on the Oct 13 team-sync recap (post package workflow, publish-time test, competitor title finding, 30-day
plan, Style C thumbnails, Thumbnail Taste app) and Scout's dashboard. Example numbers only.
Pattern: tools/build_dashboard_2.py + draft_svg.py via team_kit.py. Run from repo root."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from team_kit import *
DID = "scout-1"; pairs, O, add = deck("sc1_", "Scout")
def pr(G, ask, fn, a, b): add(G, G, O(a[0], a[1], a[2], a[3], fn(a[4])), O(b[0], b[1], b[2], b[3], fn(b[4])), ask)
HS = ("hdr", "Scout", "Shorts · Example Data", TERRA, "logo", "S")

G = "Thumbnail Text"
def th(k):
    m = {"block": ("block", TERRA), "outline": ("outline", INK), "bottom": ("bottom", INK), "top": ("top", TERRA), "lagoon": ("block", LAGOON), "jungle": ("block", JUNGLE), "none": ("none", INK), "two": ("block", SAFFRON)}
    st, c = m[k]; txt = {"none": "", "two": "Rain Day"}.get(k, "Rainy Season Market")
    return [("gap", 30), ("thumb", txt, c, st, "person"), ("p", "Short · 0:42", 46, MUTE, True)]
pr(G, "Color Blocks Or Outlined Words?", th, ("th_block", "Words On Terracotta Blocks", "Style C blocks, bottom left.", "visual", "block"), ("th_outline", "White Words, Black Outline", "Classic outlined text on top.", "action", "outline"))
pr(G, "White Strip Or Top Words?", th, ("th_bottom", "White Strip At Bottom", "Calm caption strip.", "calm", "bottom"), ("th_top", "Big Words Across The Top", "Terracotta words with a white edge.", "action", "top"))
pr(G, "Lagoon Or Jungle Blocks?", th, ("th_lagoon", "Lagoon Blocks", "Cool blue behind the words.", "calm", "lagoon"), ("th_jungle", "Jungle Blocks", "Deep green behind the words.", "visual", "jungle"))
pr(G, "No Words Or Two Words?", th, ("th_notext", "Photo Only, No Words", "Let the frame speak.", "calm", "none"), ("th_twoword", "Two Words Only", "Saffron block, very short.", "quick", "two"))

G = "Title Style"
def ti(k):
    T = {"specific": "I Paid 40 Baht For This Breakfast", "vague": "A Normal Morning Here", "question": "Would You Eat This At 6 AM?", "number": "3 Things I Buy Every Week", "place": "Night Market, Chiang Mai", "feeling": "The Quietest Morning All Year", "short": "Rain Day", "long": "What A Rainy Monday Looks Like When You Live In Thailand"}[k]
    return [HS, ("lbl", "Title Preview"), ("raw", photo(14, 80, 212, 120, LAGOON, "sun") + t(14, 216, "", 1), 128), ("h", T, 14), ("p", "Example Channel · 1.2K views", 46)]
pr(G, "Specific Or Mood Title?", ti, ("ti_specific", "Specific Detail Title", "Price, thing, place.", "focused", "specific"), ("ti_vague", "Soft Mood Title", "A gentle, open line.", "calm", "vague"))
pr(G, "Question Or Number Title?", ti, ("ti_question", "Question Title", "Asks the viewer.", "action", "question"), ("ti_number", "Number Title", "3 things, 5 spots.", "focused", "number"))
pr(G, "Place Name Or Feeling?", ti, ("ti_place", "Place Name Title", "Where it happens.", "focused", "place"), ("ti_feeling", "Feeling Title", "How it felt.", "calm", "feeling"))
pr(G, "Two Words Or Full Sentence?", ti, ("ti_short", "Two-Word Title", "Very short.", "quick", "short"), ("ti_long", "Full Sentence Title", "Says the whole story.", "focused", "long"))

G = "Post Package Card"
def pk(k):
    rows = [("Title", "Rainy Season Market"), ("Post Time", "7 PM ICT Thu"), ("Hashtags", "4"), ("Thumbnail", "Style C")]
    if k == "table": return [HS, ("h", "Ready To Post", 16), ("table", rows, True), ("btn", "Copy All", "fill", INK)]
    if k == "cards": return [HS, ("h", "Ready To Post", 16), ("cards", [(a, b, "COPY") for a, b in rows], None, "dot", "line", 30)]
    if k == "thumbfirst": return [HS, ("raw", photo(14, 56, 70, 100, LAGOON, "person") + rect(14, 120, 50, 14, TERRA) + t(18, 131, "MARKET", 9, "#FFFFFF", "khand") + t(92, 72, "Rainy Season Market", 11, INK, "khand") + t(92, 84, "7 PM ICT Thu", 7, MUTE) + tag(92, 90, "Ready", JUNGLE), 108), ("btn", "Copy All", "fill", INK)]
    if k == "textfirst": return [HS, ("h", "Rainy Season Market", 16), ("p", "Description, hashtags and settings below. Thumbnail attached."), ("cards", [("Thumbnail", "Style C · attached", "", "ic:star")])]
    if k == "steps": return [HS, ("steps", ["Title", "Thumb", "Text", "Post"], TERRA, 1), ("cards", rows[:2])]
    if k == "check": return [HS, ("h", "Before You Post", 15), ("checks", ["Title pasted", "Thumbnail set", "Description pasted", "Scheduled 7 PM"], JUNGLE, 1)]
    if k == "chat": return [HS, ("bubble", "Package ready for Rainy Season Market."), ("bubble", "Title, thumb, text and time below. Tap to copy each."), ("bubble", "Thanks", True)]
    return [HS, ("h", "Ready To Post", 16), ("tiles", [("Title", "tag"), ("Thumb", "star"), ("Text", "card"), ("Time", "clock")], 2, 54)]
pr(G, "Table Or Copy Cards?", pk, ("pk_table", "One Table, Copy All", "Everything in rows.", "quick", "table"), ("pk_cards", "Copy Link On Each Row", "Copy one piece at a time.", "focused", "cards"))
pr(G, "Thumbnail First Or Title First?", pk, ("pk_thumb", "Thumbnail Leads", "See the thumb first.", "visual", "thumbfirst"), ("pk_text", "Title Leads", "Words first.", "focused", "textfirst"))
pr(G, "Steps Or Checklist?", pk, ("pk_steps", "Four Posting Steps", "Title, Thumb, Text, Post.", "focused", "steps"), ("pk_check", "Before-You-Post Checklist", "Tick as you go.", "action", "check"))
pr(G, "Chat Message Or Tiles?", pk, ("pk_chat", "Arrives As Chat", "Package in bubbles.", "calm", "chat"), ("pk_tiles", "Four Tiles", "Tap each piece.", "visual", "tiles"))

G = "Publish Time Test"
def pt(k):
    if k == "bars": return [HS, ("lbl", "Avg Views In 24h · Sample"), ("bars", [.6, .9, .4], TERRA, ["7 PM", "9 PM", "8 AM"]), ("p", "4 Shorts per slot so far.")]
    if k == "table": return [HS, ("lbl", "Avg Views In 24h · Sample"), ("table", [("7 PM", "1.4K"), ("9 PM", "2.1K"), ("8 AM", "0.9K")], True)]
    if k == "winner": return [HS, ("lbl", "Leading So Far"), ("word", "9 PM", 40, JUNGLE, "Ahead By 50% · Sample"), ("p", "Too early to call. 8 more Shorts to go.", 46, MUTE, True)]
    if k == "even": return [HS, ("lbl", "Test Progress"), ("bar", .33, LAGOON, "4 Of 12 Shorts", "33%"), ("p", "No winner shown until all 12 are in.")]
    if k == "cal": return [HS, ("lbl", "Next Posts"), ("cal", (15, 16, 17, 22, 23, 24), TERRA)]
    if k == "list": return [HS, ("lbl", "Next Posts"), ("cards", [("Thu", "7 PM ICT"), ("Fri", "9 PM ICT"), ("Sat", "8 AM ICT")], None, "ic:clock")]
    if k == "line": return [HS, ("lbl", "Views Over 7 Days · Sample"), ("line", [.1, .7, .85, .9, .92, .93, .95], TERRA)]
    return [HS, ("lbl", "Views At Check Points · Sample"), ("stats", [("1.4K", "24h"), ("1.8K", "72h"), ("2.0K", "7d")])]
pr(G, "Bars Or Table?", pt, ("pt_bars", "Bar Per Time Slot", "Visual compare.", "visual", "bars"), ("pt_table", "Shaded Table", "Exact numbers.", "focused", "table"))
pr(G, "Show A Leader Or Wait?", pt, ("pt_leader", "Show The Leader Now", "Big leading slot.", "action", "winner"), ("pt_wait", "Progress Only, No Leader", "Wait for all 12.", "calm", "even"))
pr(G, "Calendar Or Next Three?", pt, ("pt_cal", "Calendar Of Post Days", "Marked days.", "visual", "cal"), ("pt_next3", "Next Three Posts", "Day and time rows.", "quick", "list"))
pr(G, "Line Or Check-Point Boxes?", pt, ("pt_line", "Seven-Day Line", "Shows the day-one jump.", "visual", "line"), ("pt_boxes", "24h, 72h, 7d Boxes", "Three numbers.", "focused", "stats"))

G = "Short Ideas Board"
def ib(k):
    I = [("Rainy Season Market", "Script ready"), ("Morning Temple Walk", "Needs frames"), ("Scooter Rental Day", "Idea")]
    if k == "rows": return [HS, ("h", "15 Short Ideas", 15), ("cards", I, None, "num")]
    if k == "kanban": return [HS, ("raw", "".join(rect(14 + i * 72, 56, 66, 190, SOFT, "none", 6) + lbl(20 + i * 72, 70, n, ACC[i], 6) + "".join(rect(18 + i * 72, 78 + j * 30, 58, 24, "#FFFFFF", LINE, 4) for j in range(3 - i)) for i, n in enumerate(["Idea", "Script", "Filmed"])), 200)]
    if k == "thumbs": return [HS, ("photos", 3, 90, ["sun", "leaf", "person"]), ("p", "Each idea with a sample frame.")]
    if k == "text": return [HS, ("cards", I, TERRA, "dot", "line", 30)]
    if k == "vote": return [HS, ("cards", [(a, b, "tag:Yes?") for a, b in I], TERRA)]
    if k == "rank": return [HS, ("cards", [(a, b, f"#{i+1}") for i, (a, b) in enumerate(I)], LAGOON)]
    if k == "week": return [HS, ("lbl", "This Week"), ("cards", I[:2], TERRA), ("lbl", "Next Week"), ("cards", I[2:], LAGOON)]
    return [HS, ("cards", I, None), ("btn", "See All 15", "link", TERRA)]
pr(G, "List Or Board Columns?", ib, ("ib_rows", "Numbered List", "One row per idea.", "focused", "rows"), ("ib_board", "Idea, Script, Filmed Columns", "Board view.", "visual", "kanban"))
pr(G, "Frames Or Words?", ib, ("ib_frames", "Sample Frame Per Idea", "Picture grid.", "visual", "thumbs"), ("ib_words", "Words Only", "Titles and status.", "quick", "text"))
pr(G, "Vote Or Ranked?", ib, ("ib_vote", "Yes? Tag To Vote", "You approve each.", "action", "vote"), ("ib_rank", "Scout Ranks Them", "Rank number on each.", "focused", "rank"))
pr(G, "By Week Or Top Three?", ib, ("ib_week", "Grouped By Week", "This week, next week.", "focused", "week"), ("ib_top", "Top Three Plus Link", "Short and focused.", "calm", "top"))

G = "Description Template"
def ds(k):
    if k == "short": return [HS, ("lbl", "Description"), ("p", "A rainy morning at the local market. Follow for daily life in Thailand.", 44, INK)]
    if k == "story": return [HS, ("lbl", "Description"), ("p", "Every Thursday the market fills before 6 AM. Today the rain came early, and the noodle stall still had a line. Follow for more small moments.", 44, INK)]
    if k == "tagsend": return [HS, ("lbl", "Description"), ("p", "A rainy morning at the market.", 44, INK), ("tags", ["Thailand", "Chiang Mai", "Daily Life"])]
    if k == "tagsnone": return [HS, ("lbl", "Description"), ("p", "A rainy morning at the market.", 44, INK), ("p", "No hashtags. Title carries it.", 44)]
    if k == "link": return [HS, ("lbl", "Description"), ("p", "A rainy morning at the market.", 44, INK), ("cards", [("More Shorts", "Playlist link", "", "ic:play")], LAGOON, "ic:play")]
    if k == "nolink": return [HS, ("lbl", "Description"), ("p", "A rainy morning at the market. Follow for more.", 44, INK)]
    if k == "pin": return [HS, ("lbl", "Pinned Comment"), ("bubble", "What should I film next week? Market or temple?")]
    return [HS, ("lbl", "Pinned Comment"), ("p", "None. Leave comments open.", 44)]
pr(G, "One Line Or Short Story?", ds, ("ds_short", "One-Line Description", "Short and plain.", "quick", "short"), ("ds_story", "Three-Line Story", "Tells a bit more.", "calm", "story"))
pr(G, "Hashtags Or None?", ds, ("ds_tags", "Three Hashtags At End", "Place and topic.", "focused", "tagsend"), ("ds_notags", "No Hashtags", "Clean text.", "calm", "tagsnone"))
pr(G, "Playlist Link Or Not?", ds, ("ds_link", "Playlist Link Card", "Send viewers on.", "action", "link"), ("ds_nolink", "No Link", "Just the text.", "calm", "nolink"))
pr(G, "Pinned Question Or No Pin?", ds, ("ds_pin", "Pinned Question", "Ask what to film next.", "action", "pin"), ("ds_nopin", "No Pinned Comment", "Comments stay open.", "calm", "nopin"))

G = "Channel Stats Card"
def cs(k):
    if k == "big": return [HS, ("word", "1.4K", 44, TERRA, "Subscribers · Sample"), ("stats", [("23", "Shorts"), ("97%", "Day-One Views")], "plain")]
    if k == "boxes": return [HS, ("stats", [("1.4K", "Subs"), ("23", "Shorts"), ("97%", "Day One")], "tint")]
    if k == "line": return [HS, ("lbl", "Subscribers · Sample"), ("line", [.2, .3, .35, .5, .6, .8, .9], JUNGLE)]
    if k == "bars": return [HS, ("lbl", "Subscribers · Sample"), ("bars", [.2, .3, .35, .5, .6, .8, .9], JUNGLE)]
    if k == "organic": return [HS, ("lbl", "Where Subs Came From · Sample"), ("bar", .6, JUNGLE, "Organic", "60%"), ("bar", .4, SAFFRON, "Ads", "40%")]
    if k == "blank": return [HS, ("banner", "Need Studio Export To Split Subs", SAFFRON, "clock"), ("stats", [("1.4K", "Subs"), ("?", "Organic")])]
    if k == "goal": return [HS, ("ring", .47, TERRA, "47%", "Of Watch-Hour Goal · Sample")]
    return [HS, ("bar", .47, TERRA, "Watch-Hour Goal · Sample", "47%"), ("cards", [("Next Short", "Thu 7 PM")])]
pr(G, "Big Number Or Three Boxes?", cs, ("cs_big", "One Big Number", "Subscribers first.", "visual", "big"), ("cs_boxes", "Three Tinted Boxes", "Subs, Shorts, Day One.", "focused", "boxes"))
pr(G, "Line Or Bars Over Time?", cs, ("cs_line", "Growth Line", "Smooth trend.", "calm", "line"), ("cs_bars", "Weekly Bars", "Step by step.", "visual", "bars"))
pr(G, "Show Split Or Ask For Data?", cs, ("cs_split", "Organic Vs Ads Bars", "When data is in.", "focused", "organic"), ("cs_ask", "Banner Asking For Export", "Until data arrives.", "action", "blank"))
pr(G, "Ring Or Bar For Goal?", cs, ("cs_ring", "Goal Ring", "Big percent ring.", "visual", "goal"), ("cs_goalbar", "Goal Bar Plus Next Short", "Bar and next post.", "quick", "goalbar"))

G = "Opening Frame Text"
def of(k):
    T = {"hook": "WAIT FOR IT", "place": "CHIANG MAI, 6 AM", "q": "WHAT'S 40 BAHT GET YOU?", "none": "", "sub": "", "big": ""}
    if k in ("hook", "place", "q", "none"):
        return [("gap", 30), ("thumb", T[k].title() if T[k] else "", TERRA, "outline" if T[k] else "none", "sun"), ("p", "First Second Of The Short", 46, MUTE, True)]
    st = {"subs": ("bottom", "Captions Along The Bottom"), "bigc": ("outline", "Big Word Captions Mid")}[k]
    return [("gap", 30), ("thumb", "So the rain came early", TERRA, st[0], "person"), ("p", st[1], 46, MUTE, True)]
pr(G, "Hook Or Place Name?", of, ("of_hook", "Hook Words", "Wait For It.", "action", "hook"), ("of_place", "Place And Time", "Chiang Mai, 6 AM.", "calm", "place"))
pr(G, "Question Or Clean Frame?", of, ("of_q", "Question On Frame", "Pulls curiosity.", "action", "q"), ("of_clean", "No Text, Just The Shot", "Let it play.", "calm", "none"))
pr(G, "Bottom Captions Or Big Mid Captions?", of, ("of_subs", "Small Bottom Captions", "Easy to read, calm.", "calm", "subs"), ("of_bigc", "Big Outlined Captions", "Bold mid-screen words.", "visual", "bigc"))

G = "Waiting On Max"
def wm(k):
    I = [("Send Studio Export", "90 days"), ("Pause Ad Campaigns?", "Yes or no"), ("New Frames: Two Shorts", "Thumbnails")]
    if k == "cards": return [HS, ("lbl", "Waiting On You"), ("cards", I, TERRA, "num")]
    if k == "yesno": return [HS, ("lbl", "Waiting On You"), ("raw", "".join(rect(14, 82 + i * 54, 212, 48, "#FFFFFF", LINE, 8) + t(24, 98 + i * 54, n, 10, INK, "khand") + t(24, 108 + i * 54, h, 6.5, MUTE) + btn(112 + i * 54, "Do It", "fill", INK, 150, 32, 14, 6) + btn(112 + i * 54, "Later", "line", INK, 188, 32, 14, 6) for i, (n, h) in enumerate(I)), 170)]
    if k == "one": return [HS, ("lbl", "One Thing Today"), ("h", "Send The Studio Export", 18), ("p", "Unlocks the organic vs ads split."), ("btn", "How To Export", "fill", TERRA)]
    return [HS, ("stats", [("3", "Waiting"), ("1", "Blocking")], "tint"), ("cards", I, TERRA)]
pr(G, "List Or Buttons On Each?", wm, ("wm_list", "Numbered List", "Tap to open.", "calm", "cards"), ("wm_btns", "Do It And Later Buttons", "Answer on the card.", "action", "yesno"))
pr(G, "One Thing Or Counts First?", wm, ("wm_one", "One Thing Today", "Biggest blocker only.", "focused", "one"), ("wm_counts", "Counts Then List", "Waiting and blocking.", "visual", "count"))

G = "Thumbnail Taste Results"
def tt(k):
    if k == "grid": return [HS, ("h", "Your Picks", 15), ("raw", "".join(photo(14 + (i % 3) * 72, 76 + (i // 3) * 80, 66, 74, ACC[i % 4], ["person", "sun", "leaf"][i % 3]) + (rect(14 + (i % 3) * 72, 76 + (i // 3) * 80, 66, 74, "none", JUNGLE, 6, 2.5) if i in (0, 4) else "") for i in range(6)), 166)]
    if k == "tags": return [HS, ("h", "What You Like", 15), ("tags", ["Faces", "Few Words", "Terracotta", "Bright", "Close Up"]), ("bar", .7, JUNGLE, "Faces", "70%"), ("bar", .55, LAGOON, "Few Words", "55%")]
    if k == "ab": return [HS, ("raw", photo(14, 60, 103, 150, TERRA, "person") + photo(123, 60, 103, 150, LAGOON, "sun") + btn(218, "This", "fill", INK, 14, 103, 24, 8) + btn(218, "This", "fill", INK, 123, 103, 24, 8), 190)]
    return [("gap", 30), ("thumb", "Rain Market", TERRA, "block"), ("btn2", "Like", "Skip")]
pr(G, "Picks Grid Or Taste Tags?", tt, ("tt_grid", "Grid With Picks Ringed", "See what you chose.", "visual", "grid"), ("tt_tags", "Taste Tags And Bars", "What the picks add up to.", "focused", "tags"))
pr(G, "Two-Up Or One At A Time?", tt, ("tt_ab", "Two Thumbnails Side By Side", "Pick the better one.", "quick", "ab"), ("tt_one", "One At A Time, Like Or Skip", "Judge each alone.", "calm", "one"))

G = "Channel Banner And Avatar"
def cb(k):
    if k in ("photo", "word", "line", "solid"):
        top = {"photo": photo(0, 0, W, 90, LAGOON, "sun", 0), "word": rect(0, 0, W, 90, "#FFFFFF") + t(120, 52, "A Moment In Thailand", 18, INK, "khand", anchor="middle") + ln(89, 0, W),
               "line": rect(0, 0, W, 90, "#FFFFFF") + photo(0, 0, W, 90, TERRA, "leaf", 0), "solid": rect(0, 0, W, 90, TERRA) + t(120, 52, "Daily Life, Short And Real", 14, "#FFFFFF", "khand", anchor="middle")}[k]
        return [("raw", top + f'<circle cx="44" cy="100" r="22" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>' + photo(26, 82, 36, 36, LAGOON, "person", 18) + t(74, 112, "A Moment In Thailand", 11, INK, "khand") + t(74, 123, "Example Handle · 1.4K Subs", 6.5, MUTE), 140), ("photos", 3, 90, ["person", "sun", "leaf"])]
    ch = {"face": ("person", ""), "mono": (None, "M")}[k]
    return [("gap", 40), ("raw", (photo(70, 40, 100, 100, LAGOON, "person", 50) if ch[0] else f'<circle cx="120" cy="90" r="50" fill="{TERRA}"/>' + t(120, 112, "M", 60, "#FFFFFF", "khand", anchor="middle")) + t(120, 170, "Small Size:", 7, MUTE, anchor="middle") + (photo(108, 180, 24, 24, LAGOON, "person", 12) if ch[0] else f'<circle cx="120" cy="192" r="12" fill="{TERRA}"/>' + t(120, 198, "M", 14, "#FFFFFF", "khand", anchor="middle")), 200)]
pr(G, "Photo Banner Or Name Banner?", cb, ("cb_photo", "Wide Photo Banner", "A calm landscape.", "visual", "photo"), ("cb_word", "Channel Name On White", "Clean wordmark.", "calm", "word"))
pr(G, "Leaf Drawing Or Terracotta Band?", cb, ("cb_leaf", "Drawn Leaf Banner", "Soft drawn art.", "calm", "line"), ("cb_solid", "Terracotta Band With Line", "Bold brand color.", "visual", "solid"))
pr(G, "Face Or Letter Avatar?", cb, ("cb_face", "Face Avatar", "Personal and warm.", "visual", "face"), ("cb_letter", "Letter Avatar", "Clean brand mark.", "focused", "mono"))

G = "Series Names"
def sn(k):
    N = {"day": ("A Day In", "A Day In Chiang Mai #4"), "price": ("What It Costs", "What It Costs: Breakfast"), "morning": ("6 AM Club", "6 AM Club: Market"), "plain": ("No Series", "Rainy Season Market"),
         "num": ("Numbered", "Thailand Moment 24"), "loc": ("By Place", "Chiang Dao: Morning Fog")}[k]
    return [HS, ("lbl", "Series: " + N[0]), ("raw", photo(66, 90, 108, 150, LAGOON, "person", 8) + rect(74, 200, 92, 30, "#FFFFFFEE", "none", 4) + t(120, 219, N[1][:22], 8.5, INK, "khand", anchor="middle"), 160), ("p", N[1], 40, INK, True)]
pr(G, "A Day In Or What It Costs?", sn, ("sn_dayin", "A Day In Series", "Place-based episodes.", "calm", "day"), ("sn_costs", "What It Costs Series", "Price hook each time.", "action", "price"))
pr(G, "6 AM Club Or No Series?", sn, ("sn_6am", "6 AM Club Series", "Early mornings only.", "visual", "morning"), ("sn_none", "No Series Names", "Each Short stands alone.", "calm", "plain"))
pr(G, "Numbered Or By Place?", sn, ("sn_num", "Numbered Moments", "Moment 24, 25, 26.", "focused", "num"), ("sn_place", "Named By Place", "Place, then the scene.", "visual", "loc"))

G = "Scout Dashboard"
def sd(k):
    if k == "gallery": return [HS, ("lbl", "Latest Thumbnails"), ("photos", 3, 90, ["person", "sun", "leaf"]), ("cards", [("Next Short", "Thu 7 PM")])]
    if k == "stats": return [HS, ("stats", [("1.4K", "Subs"), ("23", "Shorts"), ("3", "Waiting")], "tint"), ("cards", [("Next Short", "Thu 7 PM")])]
    if k == "next": return [HS, ("lbl", "Next Short"), ("h", "Thu 7 PM · Rain Market", 16), ("bar", .75, JUNGLE, "Package Ready", "3/4")]
    if k == "plan": return [HS, ("lbl", "30-Day Plan"), ("bar", .2, TERRA, "3 Of 15 Shorts", "20%"), ("cards", [("This Week", "3 scripted")], TERRA)]
    if k == "band": return [("hdr", "Scout", "Shorts · Example Data", TERRA, "band", "S"), ("cards", [("Next Short", "Thu 7 PM"), ("Waiting On You", "3")])]
    return [("hdr", "Scout", "Shorts · Example Data", TERRA, "bar", "S"), ("cards", [("Next Short", "Thu 7 PM"), ("Waiting On You", "3")])]
pr(G, "Thumbnails Or Stats First?", sd, ("sd_gallery", "Thumbnail Gallery First", "See the look.", "visual", "gallery"), ("sd_stats", "Stat Boxes First", "Numbers up top.", "focused", "stats"))
pr(G, "Next Short Or 30-Day Plan?", sd, ("sd_next", "Next Short Leads", "What posts next.", "action", "next"), ("sd_plan", "30-Day Plan Leads", "Progress on the plan.", "focused", "plan"))
pr(G, "Color Band Or Thin Top Line?", sd, ("sd_band", "Terracotta Header Band", "Strong header.", "visual", "band"), ("sd_line", "Thin Top Line", "White header, thin line.", "calm", "line"))

G = "Playlist Covers"
def pc(k):
    if k == "photo": return [HS, ("raw", "".join(photo(14 + (i % 2) * 108, 60 + (i // 2) * 104, 104, 96, ACC[i], ["sun", "person", "leaf", "house"][i]) + rect(14 + (i % 2) * 108, 136 + (i // 2) * 104, 104, 20, "#FFFFFFEE") + t(20 + (i % 2) * 108, 150 + (i // 2) * 104, ["Markets", "Mornings", "Nature", "Home"][i], 9, INK, "khand") for i in range(4)), 210)]
    if k == "color": return [HS, ("tiles", [("Markets", "tag"), ("Mornings", "clock"), ("Nature", "star"), ("Home", "home")], 2, 96, "solid")]
    if k == "list": return [HS, ("cards", [("Markets", "8 Shorts"), ("Mornings", "6 Shorts"), ("Nature", "5 Shorts"), ("Home", "4 Shorts")], None, "ic:play")]
    return [HS, ("raw", "".join(photo(14, 60 + i * 50, 70, 44, ACC[i], ["sun", "person", "leaf"][i]) + t(92, 80 + i * 50, ["Markets", "Mornings", "Nature"][i], 11, INK, "khand") + t(92, 92 + i * 50, "Example count", 6.5, MUTE) for i in range(3)), 160)]
pr(G, "Photo Covers Or Color Covers?", pc, ("pc_photo", "Photo Covers With Label", "Each playlist a photo.", "visual", "photo"), ("pc_color", "Solid Color Covers", "Brand color blocks.", "visual", "color"))
pr(G, "Icon Rows Or Photo Rows?", pc, ("pc_rows", "Icon Rows With Counts", "Clean list.", "quick", "list"), ("pc_photorows", "Photo Rows", "Small photo per playlist.", "calm", "rows"))

G = "Upload Settings Card"
def us(k):
    R = [("Visibility", "Scheduled"), ("Made For Kids", "No"), ("Category", "Travel"), ("Comments", "On")]
    if k == "toggles": return [HS, ("h", "Upload Settings", 15), ("toggles", [("Scheduled", True), ("Made For Kids", False), ("Comments On", True), ("Remix Allowed", True)])]
    if k == "table": return [HS, ("h", "Upload Settings", 15), ("table", R, True)]
    if k == "diff": return [HS, ("h", "Same As Last Time", 15), ("p", "Only one change: post time is 9 PM for the test."), ("cards", [("Post Time", "9 PM ICT", "tag:Changed")], SAFFRON)]
    return [HS, ("h", "Upload Settings", 15), ("cards", [(a, b) for a, b in R], None, "dot", "line", 28)]
pr(G, "Toggles Or Table?", us, ("us_toggles", "Toggle Rows", "Looks like YouTube.", "visual", "toggles"), ("us_table", "Plain Table", "Read and copy.", "focused", "table"))
pr(G, "Only Changes Or Full List?", us, ("us_diff", "Only What Changed", "Same as last time, plus one change.", "quick", "diff"), ("us_full", "Full List Every Time", "All settings each post.", "calm", "full"))

G = "Hashtag Sets"
def hs(k):
    if k == "chips": return [HS, ("lbl", "Hashtags"), ("tags", ["Thailand", "Chiang Mai", "Daily Life", "Expat"], True)]
    if k == "text": return [HS, ("lbl", "Hashtags"), ("p", "#Thailand #ChiangMai #DailyLife #Expat", 40, LAGOON)]
    if k == "three": return [HS, ("lbl", "Three Fixed Tags"), ("tags", ["Thailand", "Chiang Mai", "Shorts"])]
    return [HS, ("lbl", "Tags Picked Per Short"), ("tags", ["Market", "Rain", "Street Food", "Morning", "Noodles"])]
pr(G, "Chips Or Plain Text?", hs, ("hs_chips", "Solid Color Chips", "Easy to scan.", "visual", "chips"), ("hs_text", "Plain Text Line", "Copy-ready.", "quick", "text"))
pr(G, "Same Three Or Per Short?", hs, ("hs_fixed", "Same Three Every Time", "Simple and steady.", "calm", "three"), ("hs_per", "Picked Per Short", "Matches the topic.", "focused", "per"))

publish(DID, "Scout Round 1: Thumbnail Text, Title Style, Post Package, Publish Time Test, Short Ideas Board, Description Template, Channel Stats, Opening Frame Text, Waiting On Max, Thumbnail Taste Results, Channel Banner, Series Names, Scout Dashboard, Playlist Covers, Upload Settings, Hashtag Sets", "Scout", pairs,
        {"brands": ["Scout (YouTube Shorts on daily life in Thailand), example numbers only", "White light mode, Khand/Hind, Title Case, no emoji, accents only #C1502E #05668D #0B6E4F #D4A017"],
         "feelings": {"visual": "Visual", "focused": "Focused", "quick": "Quick", "action": "Action-first", "calm": "Calm"},
         "sources": {"team_sync": "/workspace/ops/team-sync/2026-10-13.md", "feed": "/workspace/ops/team-feed.md", "chart": "/workspace/ops/team-sync/reorg-chart-2026-10-13.md"}}, seed=33)
