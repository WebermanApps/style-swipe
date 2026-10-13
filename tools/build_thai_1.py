#!/usr/bin/env python3
"""DRAFT Style Swipe deck thai-1: 50 this-or-that pairs on the look and format of Max's Thai study partner materials
(lessons, flashcards, tone mark display, quiz styles, review schedule screens, audio buttons). English UI labels only;
Thai example words come from /workspace/thai-vocab-ongoing.md, which already shows Thai script. Run from the repo root."""
import sys; sys.path.insert(0, "tools")
from draft_svg import *
DID = "thai-1"; pairs, O, add = mk("th1_", "Thai Study")
WORDS = [("wind", "lom", "ลม", "flat"), ("bitter", "khǒm", "ขม", "rising"), ("open", "bpèrt", "เปิด", "low"), ("stubborn", "dêua", "ดื้อ", "falling"), ("pick up", "ráp", "รับ", "high"), ("fresh", "sòt", "สด", "low")]
CONT = {"flat": "M0 6 H20", "low": "M0 4 Q10 10 20 10", "falling": "M0 2 Q12 0 20 12", "high": "M0 8 Q12 6 20 0", "rising": "M0 8 Q8 12 20 0"}
def hdr(title, sub=""):
    return (t(14, 24, "THAI STUDY", 6.5, MUTE, "hind", 600, extra='letter-spacing="1.6"') + h1(14, 44, title, 17) + (t(14, 56, sub, 7, MUTE) if sub else "") + ln(62))
def contour(x, y, tone, c=LAGOON, s=1): return f'<g transform="translate({x},{y}) scale({s})"><path d="{CONT[tone]}" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/></g>'
def tone_mark(x, y, tone, mode, anchor="start"):
    if mode == "word": return t(x, y, tone.title() + " Tone", 8, MUTE, "hind", 600, anchor)
    if mode == "accent": return t(x, y, tone.title() + " Tone", 8.5, LAGOON, "hind", 600, anchor)
    if mode == "contour": return contour(x - (10 if anchor == "middle" else 0), y - 9, tone)
    if mode == "pill": return tag(x - (24 if anchor == "middle" else 0), y - 8, tone, LAGOON)
    if mode == "both": return contour(x - 32 if anchor == "middle" else x, y - 9, tone) + t(x + (2 if anchor == "middle" else 26), y, tone.title(), 8, LAGOON, "hind", 600)
    return ""
def speaker_btn(x, y, style="round", c=INK, label="Play"):
    if style == "round": return dot(x + 14, y + 14, 14, c) + ic("speaker", x + 6, y + 6, 16, "#FFFFFF")
    if style == "outline": return rect(x, y, 28, 28, "#FFFFFF", c, 14, 1.5) + ic("speaker", x + 6, y + 6, 16, c)
    if style == "square": return rect(x, y, 84, 28, c, c, 0) + ic("speaker", x + 8, y + 6, 16, "#FFFFFF") + t(x + 52, y + 18, label.upper(), 7.5, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1"')
    if style == "wide": return rect(14, y, 212, 34, c, c, 0) + ic("speaker", 70, y + 8, 18, "#FFFFFF") + t(130, y + 21, label.upper(), 9, "#FFFFFF", "hind", 600, "middle", 'letter-spacing="1.2"')
    if style == "inline": return ic("speaker", x, y, 14, c)
    return ""
# ---- lessons ----
def lesson(layout="card", size="big", rom="under", tm="word", audio="round"):
    o = hdr("Lesson 4: Everyday Words", "6 Words · About 5 Minutes")
    if layout == "card":
        e, r, th, tn = WORDS[0]; ts = 54 if size == "big" else 36
        o += rect(14, 74, 212, 168, "#FFFFFF", LINE, 10) + t(120, 140, th, ts, INK, "thai", anchor="middle")
        if rom == "under": o += t(120, 168, r, 14, INK, "khand", anchor="middle") + t(120, 184, e.title(), 9, MUTE, anchor="middle")
        else: o += t(120, 172, e.title(), 12, INK, "khand", anchor="middle")
        o += tone_mark(120, 204, tn, tm, "middle") + speaker_btn(106, 210, audio) + t(120, 262, "1 Of 6", 7, MUTE, anchor="middle") + btn(268, "Next Word", "fill", INK, h=24, size=8)
    elif layout == "rows":
        for i, (e, r, th, tn) in enumerate(WORDS[:5]):
            y = 70 + i * 38; o += ln(y + 34) + t(14, y + 24, th, 18 if size == "big" else 14, INK, "thai") + t(84, y + 16, r, 10, INK, "khand") + t(84, y + 28, e.title(), 7.5, MUTE) + tone_mark(150, y + 24, tn, tm) + speaker_btn(198, y + 6, "outline" if audio == "round" else audio)
        o += btn(268, "Start Practice", "fill", INK, h=24, size=8)
    elif layout == "sentence":
        o += rect(14, 74, 212, 90, SOFT, "none", 8) + t(120, 112, "เปิด ประตู", 28, INK, "thai", anchor="middle") + t(120, 136, "bpèrt bpra-dtuu", 11, INK, "khand", anchor="middle") + t(120, 152, "Open The Door", 8, MUTE, anchor="middle")
        o += lbl(14, 184, "New Word In This Line") + t(14, 208, "เปิด", 20, LAGOON, "thai") + t(60, 204, "bpèrt · Open", 10, INK, "khand") + tone_mark(60, 218, "low", tm) + speaker_btn(196, 190, "outline") + btn(268, "Next Line", "fill", INK, h=24, size=8)
    elif layout == "steps":
        for i, (s, d) in enumerate([("Look", "See the word"), ("Listen", "Hear it twice"), ("Say It", "Repeat out loud"), ("Check", "Quick quiz")]):
            y = 76 + i * 44; c = LAGOON if i == 1 else (JUNGLE if i == 0 else "#BDB6AA")
            o += dot(30, y + 14, 12, c if i < 2 else "#FFFFFF") + f'<circle cx="30" cy="{y+14}" r="12" fill="none" stroke="{c}" stroke-width="1.5"/>' + t(30, y + 18, str(i + 1), 10, "#FFFFFF" if i < 2 else MUTE, "khand", anchor="middle") + t(52, y + 14, s, 12, INK, "khand") + t(52, y + 26, d, 7.5, MUTE)
            if i < 3: o += f'<line x1="30" y1="{y+27}" x2="30" y2="{y+46}" stroke="{LINE}" stroke-width="1.5"/>'
        o += btn(268, "Continue: Listen", "fill", INK, h=24, size=8)
    return screen(o)
def lesson_intro(mode):
    o = hdr("Today's Lesson")
    if mode == "list":
        o += t(14, 86, "You Will Learn", 11, INK, "khand") + "".join(t(14, 106 + i * 18, f"{th}  {r}  ·  {e.title()}", 9, INK, "hind") for i, (e, r, th, _) in enumerate(WORDS[:5]))
    else:
        o += rect(14, 74, 212, 120, SOFT, "none", 10) + t(120, 130, "6", 54, LAGOON, "khand", anchor="middle") + t(120, 152, "New Words", 13, INK, "khand", anchor="middle") + t(120, 170, "About 5 Minutes", 8, MUTE, anchor="middle")
    return screen(o + btn(262, "Start Lesson", "fill", INK, h=28))
def lesson_end(mode):
    o = hdr("Lesson Done")
    if mode == "big":
        o += ic("check", 90, 86, 60, JUNGLE, 1.6) + t(120, 178, "6 Of 6 Words", 20, INK, "khand", anchor="middle") + t(120, 196, "Next review: Tomorrow", 9, MUTE, anchor="middle")
    else:
        o += "".join(t(14, 90 + i * 22, f"{th}  {r}", 10, INK) + (ic("check", 206, 78 + i * 22, 14, JUNGLE) if i != 2 else ic("x", 206, 78 + i * 22, 14, TERRA)) + ln(96 + i * 22) for i, (e, r, th, _) in enumerate(WORDS))
        o += t(14, 238, "5 Right · 1 To Review", 10, INK, "khand")
    return screen(o + btn(262, "Back To Lessons", "outline", INK, h=26))
# ---- flashcards ----
def flash(side="front", front="thai", rom=True, flip="tap", deck="single", known="buttons"):
    o = hdr("Flashcards", "Word 3 Of 20")
    e, r, th, tn = WORDS[1]
    if deck == "stack": o += rect(30, 86, 180, 156, "#FFFFFF", LINE, 10) + rect(22, 80, 196, 160, "#FFFFFF", LINE, 10)
    o += rect(14, 74, 212, 162, "#FFFFFF", "#CFC8BC" if deck == "single" else LINE, 10, 1.2)
    if side == "front":
        if front == "thai": o += t(120, 160, th, 60, INK, "thai", anchor="middle") + (t(120, 188, r, 13, MUTE, "khand", anchor="middle") if rom else "")
        else: o += t(120, 156, e.title(), 30, INK, "khand", anchor="middle")
        o += (t(120, 222, "Tap To Flip", 7.5, MUTE, anchor="middle") if flip == "tap" else rect(80, 208, 80, 20, "#FFFFFF", INK, 0) + t(120, 221, "SHOW ANSWER", 6.8, INK, "hind", 600, "middle"))
    else:
        o += t(120, 128, th, 34, INK, "thai", anchor="middle") + t(120, 156, r, 14, INK, "khand", anchor="middle") + t(120, 176, e.title(), 11, MUTE, anchor="middle") + tone_mark(120, 200, tn, "both", "middle") + speaker_btn(106, 206, "outline")
    if known == "buttons": o += rect(14, 252, 102, 32, "#FFFFFF", TERRA, 0, 1.5) + t(65, 272, "STILL LEARNING", 7.5, TERRA, "hind", 600, "middle") + rect(124, 252, 102, 32, JUNGLE, JUNGLE, 0) + t(175, 272, "I KNOW IT", 7.5, "#FFFFFF", "hind", 600, "middle")
    elif known == "swipe": o += ic("chev", 196, 258, 20, JUNGLE) + f'<g transform="translate(44,278) scale(-1,1)">{ic("chev", 0, -20, 20, TERRA)}</g>' + t(120, 272, "Swipe Right If You Know It", 8, MUTE, anchor="middle")
    elif known == "three": o += "".join(rect(14 + i * 72, 252, 68, 32, "#FFFFFF" if i < 2 else JUNGLE, [TERRA, SAFFRON, JUNGLE][i], 0, 1.5) + t(48 + i * 72, 272, s.upper(), 7, [TERRA, INK, "#FFFFFF"][i], "hind", 600, "middle") for i, s in enumerate(["Again", "Hard", "Easy"]))
    return screen(o)
def flash_grid(mode):
    o = hdr("My Word Deck", "94 Words")
    if mode == "grid":
        for i, (e, r, th, _) in enumerate(WORDS):
            x = 14 + (i % 2) * 108; y = 72 + (i // 2) * 64; o += rect(x, y, 104, 58, "#FFFFFF", LINE, 8) + t(x + 52, y + 30, th, 20, INK, "thai", anchor="middle") + t(x + 52, y + 48, r, 9, MUTE, "khand", anchor="middle")
    else:
        for i, (e, r, th, _) in enumerate(WORDS):
            y = 72 + i * 32; o += t(14, y + 20, th, 15, INK, "thai") + t(80, y + 18, r + " · " + e.title(), 8.5, INK) + ic("chev", 208, y + 6, 14, MUTE) + ln(y + 30)
    return screen(o + btn(272, "Study All", "fill", INK, h=22, size=8))
# ---- tone marks ----
def tone_screen(mode, big=False):
    o = hdr("Tone Guide", "How Each Word Sounds")
    for i, (e, r, th, tn) in enumerate(WORDS[:5]):
        y = 72 + i * 40; o += t(14, y + 26, th, 22 if big else 16, INK, "thai") + t(84, y + 18, r, 11, INK, "khand") + t(84, y + 30, e.title(), 7.5, MUTE) + tone_mark(160, y + 24, tn, mode) + ln(y + 38)
    return screen(o)
def tone_key(mode):
    o = hdr("The Five Tones")
    for i, tn in enumerate(["flat", "low", "falling", "high", "rising"]):
        y = 76 + i * 36
        if mode == "contour": o += contour(20, y + 4, tn, LAGOON, 1.4) + t(62, y + 16, tn.title(), 13, INK, "khand") + t(130, y + 16, ["lom", "sòt", "dêua", "ráp", "khǒm"][i], 10, MUTE, "khand")
        else: o += rect(14, y, 212, 30, SOFT, "none", 6) + t(24, y + 20, tn.title(), 13, INK, "khand") + t(100, y + 20, ["no mark", "à", "â", "á", "ǎ"][i], 11, LAGOON, "hind", 600) + t(160, y + 20, ["lom", "sòt", "dêua", "ráp", "khǒm"][i], 10, MUTE, "khand")
    return screen(o)
def tone_rom(mode):
    o = hdr("Pronunciation")
    e, r, th, tn = WORDS[3]
    o += t(120, 140, th, 54, INK, "thai", anchor="middle")
    if mode == "marks": o += t(120, 180, "dêua", 22, INK, "khand", anchor="middle") + t(120, 198, "Falling Tone", 9, LAGOON, "hind", 600, "middle")
    else: o += t(120, 180, "deua", 22, INK, "khand", anchor="middle") + contour(108, 188, tn, LAGOON, 1.2) + t(120, 216, "Falling", 9, LAGOON, "hind", 600, "middle")
    return screen(o + speaker_btn(106, 232, "round"))
# ---- quiz ----
def quiz(mode="mc", state="ask", fb="color", prog="bar", audio=False):
    o = t(14, 24, "QUIZ · 4 OF 10", 6.5, MUTE, "hind", 600, extra='letter-spacing="1.6"')
    o += (rect(14, 32, 212, 4, "#EEEAE4", r=2) + rect(14, 32, 85, 4, LAGOON, r=2)) if prog == "bar" else "".join(dot(26 + i * 21, 34, 4, LAGOON if i < 4 else "#E5E0D8") for i in range(10))
    e, r, th, tn = WORDS[2]
    if mode == "mc":
        o += t(120, 98, th, 44, INK, "thai", anchor="middle") + (speaker_btn(106, 108, "outline") if audio else "") + t(120, 150, "What Does It Mean?", 10, INK, "khand", anchor="middle")
        for i, a in enumerate(["Open", "Close", "Cut", "Fill"]):
            y = 160 + i * 32; good = state == "answered" and i == 0; bad = state == "answered" and i == 2
            col = (JUNGLE if good else TERRA if bad else LINE) if fb == "color" else (INK if good or bad else LINE)
            o += rect(14, y, 212, 26, (JUNGLE + "14" if good else TERRA + "12" if bad else "#FFFFFF") if fb == "color" else "#FFFFFF", col, 0, 1.5 if good or bad else 1) + t(28, y + 17, a, 10, INK, "hind", 600)
            if good: o += ic("check", 200, y + 5, 16, JUNGLE if fb == "color" else INK)
            if bad: o += ic("x", 200, y + 5, 16, TERRA if fb == "color" else INK)
    elif mode == "listen":
        o += speaker_btn(0, 70, "wide", LAGOON, "Play The Word") + t(120, 136, "Which Word Did You Hear?", 10, INK, "khand", anchor="middle")
        for i, (_, rr, tt, _) in enumerate(WORDS[:4]):
            x = 14 + (i % 2) * 108; y = 148 + (i // 2) * 60; o += rect(x, y, 104, 54, "#FFFFFF", LINE, 0) + t(x + 52, y + 30, tt, 22, INK, "thai", anchor="middle") + t(x + 52, y + 46, rr, 8, MUTE, "khand", anchor="middle")
    elif mode == "type":
        o += t(120, 100, "Open", 30, INK, "khand", anchor="middle") + t(120, 120, "Type It In Romanized Letters", 8, MUTE, anchor="middle") + rect(14, 140, 212, 36, "#FFFFFF", INK, 0, 1.5) + t(24, 164, "bpert", 14, INK, "khand") + btn(190, "Check", "fill", INK, h=28)
    elif mode == "match":
        for i, (ee, rr, tt, _) in enumerate(WORDS[:4]):
            y = 70 + i * 44; o += rect(14, y, 96, 36, "#FFFFFF", LAGOON if i == 1 else LINE, 0, 1.5 if i == 1 else 1) + t(62, y + 24, tt, 18, INK, "thai", anchor="middle")
            o += rect(130, y, 96, 36, "#FFFFFF", LINE, 0) + t(178, y + 22, ["Bitter", "Open", "Wind", "Stubborn"][i], 10, INK, "hind", 600, "middle")
        o += t(120, 262, "Tap A Thai Word, Then Its Meaning", 8, MUTE, anchor="middle")
    elif mode == "tf":
        o += t(120, 110, th, 44, INK, "thai", anchor="middle") + t(120, 150, "Means \"Close\"", 16, INK, "khand", anchor="middle")
        o += rect(14, 190, 102, 60, "#FFFFFF", TERRA, 0, 1.5) + t(65, 226, "FALSE", 12, TERRA, "hind", 600, "middle") + rect(124, 190, 102, 60, "#FFFFFF", JUNGLE, 0, 1.5) + t(175, 226, "TRUE", 12, JUNGLE, "hind", 600, "middle")
    return screen(o)
def quiz_result(mode):
    o = hdr("Quiz Done")
    if mode == "score": o += t(120, 140, "8/10", 54, INK, "khand", anchor="middle") + t(120, 164, "Nice Work", 12, JUNGLE, "khand", anchor="middle")
    else: o += t(14, 86, "Review These 2", 12, INK, "khand") + "".join(rect(14, 96 + i * 46, 212, 40, "#FFFFFF", LINE, 6) + t(24, 122 + i * 46, tt, 18, INK, "thai") + t(84, 114 + i * 46, rr, 10, INK, "khand") + t(84, 126 + i * 46, ee.title(), 7.5, MUTE) + speaker_btn(190, 102 + i * 46, "outline") for i, (ee, rr, tt, _) in enumerate(WORDS[2:4]))
    return screen(o + btn(262, "Practice Again", "fill", INK, h=26))
# ---- review schedule ----
def review(mode="count", accent=LAGOON):
    o = hdr("Review", "Spaced Repetition")
    if mode == "count": o += rect(14, 74, 212, 110, SOFT, "none", 10) + t(120, 138, "12", 56, accent, "khand", anchor="middle") + t(120, 162, "Words Due Today", 12, INK, "khand", anchor="middle") + btn(196, "Start Review", "fill", INK, h=30)
    elif mode == "week":
        for i, (d, n) in enumerate(zip(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], [12, 8, 15, 5, 9, 3, 6])):
            x = 18 + i * 30; hh = n * 6; o += rect(x, 170 - hh, 20, hh, accent if i == 0 else "#D9D4CB", r=2) + t(x + 10, 184, d, 7, MUTE, "hind", 600, "middle") + t(x + 10, 166 - hh, str(n), 7, INK, "hind", 600, "middle")
        o += t(14, 210, "12 Due Today", 14, INK, "khand") + btn(222, "Start Review", "fill", INK, h=28)
    elif mode == "buckets":
        for i, (s, n, c) in enumerate([("Due Today", 12, accent), ("Tomorrow", 8, MUTE), ("This Week", 21, MUTE), ("Known", 32, JUNGLE)]):
            y = 74 + i * 42; o += rect(14, y, 212, 36, "#FFFFFF", LINE, 6) + t(26, y + 23, s, 12, INK, "khand") + t(212, y + 24, str(n), 16, c, "khand", anchor="end")
        o += btn(250, "Start Review", "fill", INK, h=28)
    elif mode == "calendar":
        o += lbl(14, 80, "October 2026")
        for d in range(28):
            x = 18 + (d % 7) * 30; y = 90 + (d // 7) * 30; due = d in (12, 13, 15, 18, 20, 24)
            o += rect(x, y, 26, 26, (accent + "22" if due else "#FFFFFF"), accent if d == 12 else LINE, 4, 1.5 if d == 12 else 1) + t(x + 13, y + 17, str(d + 1), 8, INK, "hind", 600, "middle")
        o += t(14, 230, "Today: 12 Words Due", 12, INK, "khand") + btn(242, "Start Review", "fill", INK, h=28)
    elif mode == "streak":
        o += t(14, 96, "5 Day Streak", 22, INK, "khand") + "".join(dot(30 + i * 30, 120, 10, accent if i < 5 else "#E5E0D8") + t(30 + i * 30, 142, "MTWTFSS"[i], 7, MUTE, "hind", 600, "middle") for i in range(7)) + t(14, 180, "12 Words Due Today", 12, INK, "khand") + btn(196, "Keep It Going", "fill", INK, h=30)
    return screen(o)
def remind_card(mode):
    o = rect(0, 0, W, H, "#EEF3F6") + t(120, 50, "9:41", 26, INK, "khand", anchor="middle")
    o += rect(12, 76, 216, 66 if mode == "word" else 50, "#FFFFFF", "none", 12) + t(22, 94, "THAI STUDY", 6.5, MUTE, "hind", 600, extra='letter-spacing=".8"')
    if mode == "word": o += t(22, 112, "Word Of The Day: ลม (lom)", 9, INK, "hind", 600) + t(22, 126, "Wind. Tap to hear it and review 12 more.", 7.5, MUTE)
    else: o += t(22, 112, "12 words are ready to review", 9, INK, "hind", 600) + t(22, 124, "About 4 minutes.", 7.5, MUTE)
    return screen(o, "#EEF3F6")
# ---- audio ----
def audio_screen(style="round", slow="text", wave=False, auto=False, place="under"):
    o = hdr("Listen")
    e, r, th, tn = WORDS[4]
    o += t(120, 130, th, 54, INK, "thai", anchor="middle") + t(120, 160, r, 14, INK, "khand", anchor="middle")
    y = 180 if place == "under" else 74
    if place == "corner": o += speaker_btn(190, 74, "outline")
    elif style == "round": o += speaker_btn(98, y, "round", LAGOON) + dot(120, y + 14, 22, "none")
    elif style == "square": o += speaker_btn(78, y, "square", INK)
    elif style == "wide": o += speaker_btn(0, y, "wide", LAGOON, "Play")
    if wave: o += "".join(rect(40 + i * 8, 236 - h / 2, 4, h, LAGOON + "66", r=2) for i, h in enumerate([6, 12, 20, 28, 18, 24, 10, 16, 26, 14, 8, 18, 22, 10, 6, 12, 8, 4, 6, 4]))
    if slow == "text": o += link_b(120, 270 if not wave else 284, "Play Slowly")
    elif slow == "icon": o += rect(84, 256, 72, 26, "#FFFFFF", INK, 0, 1.3) + ic("slow", 92, 258, 20, INK) + t(134, 273, "SLOW", 7.5, INK, "hind", 600, "middle")
    elif slow == "speed": o += "".join(rect(48 + i * 50, 256, 44, 24, INK if i == 2 else "#FFFFFF", INK, 0, 1.2) + t(70 + i * 50, 272, s, 8, "#FFFFFF" if i == 2 else INK, "hind", 600, "middle") for i, s in enumerate(["0.5x", "0.75x", "1x"]))
    if auto: o += rect(14, 66, 212, 0) + t(226, 56, "Auto-Play On", 7, JUNGLE, "hind", 600, "end")
    return screen(o)
def link_b(x, y, s, col=LAGOON): return t(x, y, s.upper(), 8, col, "hind", 600, "middle", 'letter-spacing="1" text-decoration="underline"')
def record(mode):
    o = hdr("Say It Out Loud")
    o += t(120, 130, "ขม", 54, INK, "thai", anchor="middle") + t(120, 160, "khǒm", 14, INK, "khand", anchor="middle")
    if mode == "compare": o += speaker_btn(40, 186, "square", INK, "Thai") + rect(124, 186, 84, 28, TERRA, TERRA, 0) + ic("mic", 132, 192, 16, "#FFFFFF") + t(174, 204, "ME", 7.5, "#FFFFFF", "hind", 600, "middle")
    else: o += dot(120, 214, 26, TERRA) + ic("mic", 106, 200, 28, "#FFFFFF") + t(120, 260, "Hold To Record", 8, MUTE, anchor="middle")
    return screen(o)
# ---- progress / known words / frame ----
def known(mode):
    o = hdr("Known Words", "32 Words")
    if mode == "chips":
        for i, (ee, rr, tt, _) in enumerate(WORDS * 2):
            x = 14 + (i % 3) * 72; y = 74 + (i // 3) * 40; o += rect(x, y, 68, 34, JUNGLE + "12", JUNGLE, 6, 1) + t(x + 34, y + 22, tt, 14, INK, "thai", anchor="middle")
    else:
        for i, (ee, rr, tt, _) in enumerate(WORDS):
            y = 72 + i * 30; o += ic("check", 14, y + 6, 14, JUNGLE) + t(36, y + 18, tt + "  " + rr, 9.5, INK) + t(226, y + 18, "BRING BACK", 6.5, LAGOON, "hind", 600, "end") + ln(y + 28)
    return screen(o + btn(272, "Share My List", "outline", INK, h=22, size=8))
def prog(mode):
    o = hdr("My Progress")
    if mode == "ring":
        import math
        a = 2 * math.pi * .34; o += f'<circle cx="120" cy="140" r="50" fill="none" stroke="#EEEAE4" stroke-width="10"/><path d="M120 90 A50 50 0 0 1 {120+50*math.sin(a):.1f} {140-50*math.cos(a):.1f}" fill="none" stroke="{JUNGLE}" stroke-width="10" stroke-linecap="round"/>' + t(120, 148, "32", 26, INK, "khand", anchor="middle") + t(120, 214, "32 Known · 94 Active", 11, INK, "khand", anchor="middle")
    else: o += "".join(t(14, 98 + i * 46, s, 12, INK, "khand") + rect(14, 106 + i * 46, 212, 8, "#EEEAE4", r=4) + rect(14, 106 + i * 46, 212 * f, 8, c, r=4) + t(226, 98 + i * 46, n, 10, INK, "khand", anchor="end") for i, (s, f, n, c) in enumerate([("Known", .34, "32", JUNGLE), ("Learning", .5, "47", LAGOON), ("New", .16, "15", "#BDB6AA")]))
    return screen(o)
def frame(mode):
    o = hdr("Thai Study")
    items = [("Lessons", "home"), ("Flashcards", "card"), ("Quiz", "check"), ("Review", "cal")]
    if mode == "tiles":
        for i, (s, k) in enumerate(items):
            x = 14 + (i % 2) * 108; y = 74 + (i // 2) * 96; o += rect(x, y, 104, 88, "#FFFFFF", LINE, 10) + ic(k, x + 36, y + 16, 32, LAGOON if i == 3 else INK) + t(x + 52, y + 72, s, 12, INK, "khand", anchor="middle")
    else:
        for i, (s, k) in enumerate(items):
            y = 74 + i * 46; o += ic(k, 14, y + 8, 22, LAGOON if i == 3 else INK) + t(48, y + 24, s, 14, INK, "khand") + ic("chev", 206, y + 10, 16, MUTE) + ln(y + 42)
    return screen(o + t(120, 286, "12 Words Due Today", 8, LAGOON, "hind", 600, "middle"))

G1, G2, G3, G4, G5, G6, G7 = "Lessons", "Flashcards", "Tone Marks", "Quiz Styles", "Review Schedule", "Audio Buttons", "Progress And Home"
add(G1, "Lesson: Layout", O("ls_card", "One Word Per Card", "A big Thai word, romanized under it, then Next.", ["big", "focused", "readable"], "calm", lesson("card")), O("ls_rows", "All Words In A List", "Six rows with Thai, romanized, meaning and play.", ["compact", "overview"], "school", lesson("rows")), "One Word At A Time Or The Whole List?")
add(G1, "Lesson: Thai Size", O("ls_big", "Huge Thai Letters", "Thai word fills the card.", ["big", "readable"], "calm", lesson("card", "big")), O("ls_med", "Medium Thai Letters", "Thai word at a normal heading size.", ["balanced", "simple"], "school", lesson("card", "med")), "How Big Is The Thai?")
add(G1, "Lesson: Meaning", O("ls_rom_under", "Romanized Plus Meaning", "Romanized line and the English meaning under the Thai.", ["guided", "easy"], "calm", lesson("card", "big", "under")), O("ls_rom_none", "Meaning Only", "Only the English meaning under the Thai.", ["simple", "challenge"], "school", lesson("card", "big", "none")), "Show Romanized In Lessons?")
add(G1, "Lesson: Format", O("ls_sentence", "Learn Inside A Short Line", "A two-word line, then the new word pulled out.", ["story", "context"], "playful", lesson("sentence")), O("ls_steps", "Four Clear Steps", "Look, Listen, Say It, Check, as a step list.", ["guided", "clear"], "school", lesson("steps")), "Sentence First Or Steps?")
add(G1, "Lesson: Start Screen", O("ls_intro_list", "Start With The Word List", "Shows every word you'll learn.", ["clear", "overview"], "school", lesson_intro("list")), O("ls_intro_big", "Start With One Big Number", "A big '6 New Words' and the time it takes.", ["big", "simple"], "calm", lesson_intro("big")), "How Does A Lesson Start?")
add(G1, "Lesson: End Screen", O("ls_end_big", "Big Check And Next Review", "One large check and when to come back.", ["big", "reassuring"], "calm", lesson_end("big")), O("ls_end_list", "Word-By-Word Result", "Each word with a check or cross.", ["detailed", "clear"], "school", lesson_end("list")), "How Does A Lesson End?")
add(G1, "Lesson: Row Audio", O("ls_rows_round", "Outline Play Circles On Rows", "Round outlined speaker on each row.", ["light", "clean"], "calm", lesson("rows", "big", "under", "word", "round")), O("ls_rows_inline", "Small Speaker Icon On Rows", "A small speaker icon only.", ["minimal", "compact"], "school", lesson("rows", "big", "under", "word", "inline")), "Row Play Button Style?")
add(G2, "Flashcard: Front", O("fc_front_thai", "Thai On The Front", "Thai word and romanized up front.", ["challenge", "readable"], "school", flash("front", "thai")), O("fc_front_eng", "English On The Front", "English word up front, recall the Thai.", ["recall", "simple"], "school", flash("front", "eng")), "Which Side Faces You First?")
add(G2, "Flashcard: Romanized Hint", O("fc_rom_on", "Romanized Hint Shown", "Romanized under the Thai on the front.", ["easy", "guided"], "calm", flash("front", "thai", True)), O("fc_rom_off", "Thai Only On Front", "No hint until you flip.", ["challenge", "focused"], "school", flash("front", "thai", False)), "Show The Hint On The Front?")
add(G2, "Flashcard: Flip", O("fc_flip_tap", "Tap Anywhere To Flip", "Small 'Tap To Flip' text.", ["quick", "light"], "playful", flash("front", flip="tap")), O("fc_flip_btn", "Show Answer Button", "An outlined Show Answer button.", ["clear", "guided"], "school", flash("front", flip="button")), "How Do You Flip?")
add(G2, "Flashcard: Rating", O("fc_known_two", "Two Buttons: Still Learning, I Know It", "Terracotta outline and solid green.", ["simple", "big"], "calm", flash("back", known="buttons")), O("fc_known_three", "Three Buttons: Again, Hard, Easy", "Classic spaced-repetition rating.", ["control", "detailed"], "school", flash("back", known="three")), "Two Or Three Ratings?")
add(G2, "Flashcard: Gesture", O("fc_buttons", "Rate With Buttons", "Two buttons under the card.", ["clear", "readable"], "school", flash("back", known="buttons")), O("fc_swipe", "Rate By Swiping", "Swipe right if you know it.", ["playful", "quick"], "playful", flash("back", known="swipe")), "Buttons Or Swipe?")
add(G2, "Flashcard: Pile", O("fc_single", "One Card", "A single card on white.", ["clean", "focused"], "calm", flash("front", deck="single")), O("fc_stack", "Card Stack", "Cards peek out behind like a real pile.", ["playful", "visual"], "playful", flash("front", deck="stack")), "Single Card Or Stack?")
add(G2, "Flashcard: Deck View", O("fc_grid", "Word Deck As Tiles", "Two-column tiles with Thai and romanized.", ["visual", "big"], "playful", flash_grid("grid")), O("fc_list", "Word Deck As A List", "One line per word.", ["compact", "clear"], "school", flash_grid("list")), "Tiles Or List For Your Words?")
add(G3, "Tone: Display", O("tn_word", "Tone As A Grey Word", "'Falling Tone' in small grey text.", ["quiet", "simple"], "calm", tone_screen("word")), O("tn_contour", "Tone As A Drawn Pitch Line", "A small lagoon line that rises or falls.", ["visual", "clear"], "playful", tone_screen("contour")), "Words Or Drawn Lines For Tones?")
add(G3, "Tone: Color", O("tn_accent", "Tone Name In Lagoon", "The tone name in the one accent color.", ["clear", "visual"], "school", tone_screen("accent")), O("tn_pill", "Tone In A Small Pill", "A soft lagoon pill tag.", ["tidy", "visual"], "school", tone_screen("pill")), "Plain Accent Text Or Pill?")
add(G3, "Tone: Combo", O("tn_both", "Pitch Line Plus Name", "Drawn line and the tone name together.", ["guided", "clear"], "school", tone_screen("both")), O("tn_contour_only", "Pitch Line Only", "Just the drawn line, nothing else.", ["minimal", "visual"], "calm", tone_screen("contour", True)), "Line With Name Or Line Alone?")
add(G3, "Tone: Key Page", O("tn_key_contour", "Tone Key As Pitch Lines", "Five drawn lines with an example each.", ["visual", "easy"], "playful", tone_key("contour")), O("tn_key_marks", "Tone Key As Romanized Marks", "Five rows showing the accent mark used.", ["system", "detailed"], "school", tone_key("marks")), "How Is The Tone Key Shown?")
add(G3, "Tone: Romanized", O("tn_rom_marks", "Romanized With Accent Marks", "dêua, with the mark showing the tone.", ["compact", "school"], "school", tone_rom("marks")), O("tn_rom_line", "Plain Romanized Plus Pitch Line", "deua, with a drawn falling line.", ["visual", "easy"], "playful", tone_rom("line")), "Accent Marks Or Plain Letters Plus A Line?")
add(G3, "Tone: Big View", O("tn_big_thai", "Bigger Thai In The Tone Guide", "Larger Thai next to each tone.", ["big", "readable"], "calm", tone_screen("both", True)), O("tn_small_thai", "Standard Thai In The Tone Guide", "Normal Thai size.", ["compact", "simple"], "school", tone_screen("both", False)), "Tone Guide Thai Size?")
add(G3, "Tone: Quiz Hint", O("tn_hint_word", "Lesson Rows Show Tone Words", "Lesson rows show the tone as a word.", ["clear", "readable"], "school", lesson("rows", "big", "under", "word")), O("tn_hint_line", "Lesson Rows Show Pitch Lines", "Lesson rows show a drawn line.", ["visual", "lively"], "playful", lesson("rows", "big", "under", "contour")), "Tones In Lesson Rows?")
add(G4, "Quiz: Type", O("qz_mc", "Pick The Meaning", "Thai word with four answer buttons.", ["easy", "clear"], "school", quiz("mc")), O("qz_listen", "Listen And Pick The Word", "Play the sound, pick from four Thai tiles.", ["audio", "challenge"], "playful", quiz("listen")), "Read Or Listen Quiz?")
add(G4, "Quiz: Recall", O("qz_type", "Type The Romanized Word", "See English, type the sound.", ["challenge", "active"], "school", quiz("type")), O("qz_match", "Match Pairs", "Tap a Thai word, then its meaning.", ["playful", "visual"], "playful", quiz("match")), "Typing Or Matching?")
add(G4, "Quiz: Quick Mode", O("qz_tf", "True Or False", "Two big buttons.", ["big", "fast"], "playful", quiz("tf")), O("qz_mc_audio", "Pick The Meaning With Audio", "Four answers plus a play button.", ["guided", "audio"], "school", quiz("mc", audio=True)), "Fast True/False Or Full Choice?")
add(G4, "Quiz: Feedback", O("qz_fb_color", "Green And Terracotta Feedback", "Right answer green, wrong one terracotta.", ["clear", "visual"], "school", quiz("mc", "answered", "color")), O("qz_fb_ink", "Black Feedback Only", "Check and cross in black.", ["calm", "minimal"], "calm", quiz("mc", "answered", "ink")), "Colored Or Black Feedback?")
add(G4, "Quiz: Progress", O("qz_prog_bar", "Progress Bar", "A thin lagoon bar on top.", ["clean", "simple"], "calm", quiz("mc", prog="bar")), O("qz_prog_dots", "Ten Dots", "One dot per question.", ["visual", "playful"], "playful", quiz("mc", prog="dots")), "Bar Or Dots?")
add(G4, "Quiz: Result", O("qz_res_score", "Big Score", "A huge 8/10.", ["big", "simple"], "playful", quiz_result("score")), O("qz_res_review", "Words To Review", "The missed words with play buttons.", ["guided", "useful"], "school", quiz_result("review")), "Score Or Missed Words?")
add(G4, "Quiz: Answer Layout", O("qz_listen_grid", "Answers As Thai Tiles", "Four Thai tiles in a grid.", ["visual", "big"], "playful", quiz("listen", prog="dots")), O("qz_answer_rows", "Answers As Rows", "Four stacked answer rows.", ["clear", "readable"], "school", quiz("mc", prog="dots")), "Tiles Or Rows For Answers?")
add(G5, "Review: Home", O("rv_count", "One Big Due Number", "A big '12 Words Due Today'.", ["big", "simple"], "calm", review("count")), O("rv_week", "Week Bar Chart", "Due words per day for the week.", ["visual", "planned"], "school", review("week")), "Big Number Or Week Chart?")
add(G5, "Review: Breakdown", O("rv_buckets", "Due, Tomorrow, This Week, Known", "Four rows with counts.", ["clear", "system"], "school", review("buckets")), O("rv_calendar", "Month Calendar", "Due days tinted lagoon.", ["visual", "planned"], "school", review("calendar")), "Rows Or Calendar?")
add(G5, "Review: Motivation", O("rv_streak", "Streak Dots", "A 5-day streak with week dots.", ["lively", "habit"], "playful", review("streak")), O("rv_count_jungle", "Due Count In Green", "Big due number, no streak.", ["calm", "simple"], "calm", review("count", JUNGLE)), "Streak Or Just The Count?")
add(G5, "Review: Accent", O("rv_week_lagoon", "Week Chart In Lagoon", "Today's bar in lagoon.", ["calm", "clear"], "school", review("week", LAGOON)), O("rv_week_saffron", "Week Chart In Saffron", "Today's bar in saffron.", ["warm", "lively"], "playful", review("week", SAFFRON)), "Lagoon Or Saffron Highlight?")
add(G5, "Review: Reminder", O("rv_rem_word", "Reminder Shows A Word", "'Word Of The Day: ลม (lom)'.", ["playful", "visual"], "playful", remind_card("word")), O("rv_rem_count", "Reminder Shows A Count", "'12 words are ready to review'.", ["simple", "clear"], "calm", remind_card("count")), "What Does The Reminder Say?")
add(G5, "Review: Calendar Accent", O("rv_cal_terra", "Calendar Due Days In Terracotta", "Due days tinted terracotta.", ["warm", "lively"], "playful", review("calendar", TERRA)), O("rv_cal_jungle", "Calendar Due Days In Green", "Due days tinted jungle green.", ["calm", "natural"], "calm", review("calendar", JUNGLE)), "Calendar Tint?")
add(G5, "Review: Buckets Accent", O("rv_buck_saffron", "Due Count In Saffron", "Due Today number in saffron.", ["warm", "alert"], "playful", review("buckets", SAFFRON)), O("rv_buck_lagoon", "Due Count In Lagoon", "Due Today number in lagoon.", ["calm", "clear"], "calm", review("buckets", LAGOON)), "Due Count Color?")
add(G6, "Audio: Main Button", O("au_round", "Round Lagoon Play Button", "A round lagoon speaker button.", ["friendly", "visual"], "playful", audio_screen("round")), O("au_square", "Square Black Play Button", "Square black button with 'Play'.", ["clear", "brand"], "school", audio_screen("square")), "Round Or Square Play?")
add(G6, "Audio: Size", O("au_wide", "Full-Width Play Bar", "A wide lagoon bar under the word.", ["big", "easy"], "calm", audio_screen("wide")), O("au_corner", "Small Speaker In The Corner", "A small outline speaker top right.", ["minimal", "quiet"], "calm", audio_screen("round", place="corner")), "Big Bar Or Corner Speaker?")
add(G6, "Audio: Slow Replay", O("au_slow_text", "'Play Slowly' Link", "An underlined text link.", ["simple", "quiet"], "calm", audio_screen("round", "text")), O("au_slow_icon", "Drawn Slow Icon Button", "A small drawn turtle outline with 'Slow'.", ["playful", "visual"], "playful", audio_screen("round", "icon")), "How Is Slow Replay Shown?")
add(G6, "Audio: Speed", O("au_speed_chips", "Speed Chips: 0.5x, 0.75x, 1x", "Three speed chips.", ["control", "clear"], "school", audio_screen("square", "speed")), O("au_slow_one", "One Slow Button", "Just one Slow button.", ["simple", "easy"], "calm", audio_screen("square", "icon")), "Speed Choices Or One Slow?")
add(G6, "Audio: Waveform", O("au_wave_on", "Show A Sound Wave", "A soft lagoon wave under the button.", ["visual", "lively"], "playful", audio_screen("round", "text", True)), O("au_wave_off", "No Sound Wave", "Just the button.", ["clean", "minimal"], "calm", audio_screen("round", "text", False)), "Show The Sound Wave?")
add(G6, "Audio: Auto-Play", O("au_auto_on", "Auto-Play Each Word", "Word plays when it shows; small green note.", ["easy", "guided"], "calm", audio_screen("wide", "text", False, True)), O("au_auto_off", "Tap To Play", "Nothing plays until you tap.", ["quiet", "control"], "school", audio_screen("wide", "text", False, False)), "Auto-Play Or Tap?")
add(G6, "Audio: Say It Back", O("au_rec_hold", "Big Hold-To-Record Button", "One big terracotta mic button.", ["big", "active"], "playful", record("hold")), O("au_rec_compare", "Thai Vs Me Buttons", "Play the Thai, then play your own try.", ["guided", "compare"], "school", record("compare")), "How Do You Practice Saying It?")
add(G7, "Known Words: View", O("kw_chips", "Known Words As Green Tiles", "Thai words in soft green tiles.", ["visual", "proud"], "playful", known("chips")), O("kw_list", "Known Words As A List", "Rows with a Bring Back link.", ["clear", "control"], "school", known("list")), "Tiles Or List?")
add(G7, "Progress: View", O("pg_ring", "One Progress Ring", "A ring with 32 known.", ["big", "simple"], "calm", prog("ring")), O("pg_bars", "Three Progress Bars", "Known, Learning, New bars.", ["detailed", "clear"], "school", prog("bars")), "Ring Or Bars?")
add(G7, "Home: Layout", O("hm_tiles", "Home As Four Big Tiles", "Lessons, Flashcards, Quiz, Review tiles.", ["big", "visual"], "playful", frame("tiles")), O("hm_rows", "Home As Four Rows", "Icon rows with arrows.", ["compact", "clear"], "school", frame("rows")), "Tiles Or Rows On Home?")
add(G7, "Flashcard: Deck Style", O("fc_grid_big", "Flashcard Back With Pitch Line", "Back side shows the drawn tone and play.", ["visual", "guided"], "playful", flash("back", known="swipe")), O("fc_back_three", "Flashcard Back With Ratings", "Back side with Again, Hard, Easy.", ["control", "system"], "school", flash("back", known="three")), "Swipe Or Rate On The Back?")
add(G1, "Lesson: Tone In A Sentence", O("ls_sent_line", "Sentence Lesson With A Pitch Line", "The new word's tone as a drawn line.", ["visual", "guided"], "playful", lesson("sentence", tm="contour")), O("ls_sent_pill", "Sentence Lesson With A Tone Pill", "The tone as a small lagoon pill.", ["tidy", "clear"], "school", lesson("sentence", tm="pill")), "Line Or Pill In Sentence Lessons?")
add(G5, "Review: Streak Color", O("rv_streak_saffron", "Streak Dots In Saffron", "Warm saffron streak dots.", ["warm", "lively"], "playful", review("streak", SAFFRON)), O("rv_streak_jungle", "Streak Dots In Green", "Jungle green streak dots.", ["calm", "natural"], "calm", review("streak", JUNGLE)), "Streak Color?")
add(G3, "Tone: Big Guide Style", O("tn_big_pill", "Big Thai With Tone Pills", "Large Thai and a lagoon pill per word.", ["big", "visual"], "playful", tone_screen("pill", True)), O("tn_big_word", "Big Thai With Grey Tone Words", "Large Thai and a quiet grey tone word.", ["big", "quiet"], "calm", tone_screen("word", True)), "Pills Or Grey Words With Big Thai?")
add(G6, "Audio: Slow With Big Bar", O("au_wide_speed", "Big Play Bar Plus Speed Chips", "Wide play bar and 0.5x / 0.75x / 1x.", ["big", "control"], "school", audio_screen("wide", "speed")), O("au_wide_slow", "Big Play Bar Plus One Slow Button", "Wide play bar and one drawn Slow button.", ["big", "simple"], "calm", audio_screen("wide", "icon")), "Speed Chips Or Slow Button Under A Big Bar?")
finish(DID, "Thai Study Round 1: Lessons, Flashcards, Tone Marks, Quiz Styles, Review Schedule, Audio Buttons", "Thai Study", pairs, 0,
       {"brands": ["Max's Thai study partner materials (Thai Vocab Quiz https://webermanapps.github.io/thai-vocab-quiz/, flashcards, study sheet)", "White base, Khand/Hind for UI, Thai lesson words in Noto Sans Thai Looped/Sarabun, 1-2 accent pops (lagoon, jungle, terracotta, saffron)"],
        "feelings": {"calm": "Calm and readable", "school": "Organized school-style", "playful": "Light and playful"},
        "sources": {"words": "/workspace/thai-vocab-ongoing.md", "quiz": "/workspace/thai-vocab-quiz/", "team_feed": "/workspace/ops/team-feed.md"},
        "content_note": "UI labels English only; Thai words are lesson content taken from the existing study sheet."})
