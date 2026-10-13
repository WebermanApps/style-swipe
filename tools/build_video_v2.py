#!/usr/bin/env python3
"""Build Style Swipe deck video-v2: ~26 this-or-that pairs to plan the Smart Upkeep explainer video V.2 before production.
Follows tools/build_upkeep_3.py (hm svg visuals, ledger, no repeats). Frames come from: V.1 video (ffmpeg), V.2 stills from
Video & Photo (/workspace/video/smartkeep-v2/stills), polo mockups, and new V.2-style frames rendered here with playwright
(cream #FAF3EB base, Khand/Hind, 2-3 small pops). Run from the style-swipe repo root."""
import json, os, glob, subprocess, sys, base64, random, datetime as dt
DID = "video-v2"; IMG = "img"; V1 = "/workspace/smartkeep/video/SmartKeep_V1.mp4"; ST = "/workspace/video/smartkeep-v2/stills"
MOCK = "/workspace/brand/smart-upkeep/mockups"; FONTS = "/workspace/smartkeep/video/build"
CREAM = "#FAF3EB"; INK = "#0A0A0A"; MUTE = "#525252"; TERRA = "#C1502E"; LAGOON = "#05668D"; LAG2 = "#00A6A6"; JUNGLE = "#0B6E4F"; SAFFRON = "#D4A017"
PRICE = "Membership Starting at $99/Month"
from PIL import Image, ImageDraw, ImageFilter

def save(im, key, w=1280):
    im = im.convert("RGB"); im = im.resize((w, round(im.height * w / im.width))); im.save(f"{IMG}/vv2_{key}.jpg", quality=84); return key
def still(name, key): return save(Image.open(f"{ST}/{name}.png"), key, 720 if "9x16" in name else 1280)
def v1frame(t, key):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", V1, "-frames:v", "1", "-vf", "scale=1280:-1", f"{IMG}/vv2_{key}.jpg"], check=True); return key

# ---- new V.2-style frames, 1280x720 HTML ----
def logo_svg(c=INK, up="#737373"):
    s = open("/workspace/brand/smart-upkeep/logos/A_original.svg").read().replace('<rect width="1153" height="400" fill="#FFFFFF"/>', "")
    return s.replace("#1F1F1F", c).replace("#737373", up)
LOGO = "data:image/svg+xml;base64," + base64.b64encode(logo_svg().encode()).decode()
CSS = f"""@font-face{{font-family:Khand;src:url(file://{FONTS}/Khand-Bold.woff2);font-weight:700}}@font-face{{font-family:Hind;src:url(file://{FONTS}/Hind-Regular.woff2)}}@font-face{{font-family:Hind;src:url(file://{FONTS}/Hind-SemiBold.woff);font-weight:600}}
*{{box-sizing:border-box}}body{{margin:0;width:1280px;height:720px;background:{CREAM};font-family:Hind;color:{INK};position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.h{{font-family:Khand;font-weight:700;font-size:50px;line-height:1.08}} .s{{font-size:32px;color:{MUTE};margin-top:14px}} .card{{background:#fff;border-radius:14px;box-shadow:0 6px 24px #0001;padding:22px 30px}}
.logo{{background:url({LOGO}) center/contain no-repeat}}"""
FR = {}
import io
_b = io.BytesIO(); Image.open(f"{MOCK}/polo_white_black-logo.png").convert("RGB").resize((880, 760)).save(_b, "JPEG", quality=80)
POLO = "data:image/jpeg;base64," + base64.b64encode(_b.getvalue()).decode()
def F(key, body, css=""): FR[key] = f"<html><head><style>{CSS}{css}</style></head><body>{body}</body></html>"; return key
def render_frames():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 720})
        for k, html in FR.items():
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150); pg.screenshot(path=f"{IMG}/vv2_{k}.jpg", type="jpeg", quality=84)
        b.close()
def photo_scan(key, mode):  # photo-real direction: real interior photo with a scan overlay
    im = Image.open(f"{IMG}/int_modernkitchen.jpg").convert("RGB").resize((1280, 720))
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.ellipse((740, 360, 1040, 600), fill=(0, 140, 230, 200)); ov = ov.filter(ImageFilter.GaussianBlur(40)); im = Image.alpha_composite(im.convert("RGBA"), ov)
    d = ImageDraw.Draw(im); d.rectangle((0, 0, 1280, 720), outline=(250, 243, 235), width=0)
    from PIL import ImageFont; fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    d.rounded_rectangle((760, 290, 1150, 350), 10, fill=(255, 255, 255, 240)); d.text((780, 300), "Moisture: Check Here", font=fnt, fill=(5, 102, 141))
    return save(im, key)

def scene(h, s="", extra="", css=""): return f'{extra}<div class="h">{h}</div>' + (f'<div class="s">{s}</div>' if s else "")
# text size: same beat at V.1 sizes vs ~7% of frame height
F("txt_v1", scene("A Whole-Home Moisture Scan", "On every visit, in every room."), ".h{font-size:38px}.s{font-size:17px}")
F("txt_sup_big", scene("A Whole-Home Moisture Scan", "On every visit, in every room."), ".h{font-size:52px}.s{font-size:34px}")
F("rf_short", scene("An Honest Refund If You Cancel", "No runaround.", f'<div class="card" style="font-size:34px;margin-bottom:30px">✓ Cancel anytime</div>'))
F("txt_7", scene("A Trained Smart Upkeep Tech", "Every tech carries a license you can check."), ".h{font-size:56px}.s{font-size:34px}")
# headline wording per beat
def hl(key, h, s, pop): return F(key, f'<div style="width:90px;height:8px;background:{pop};margin-bottom:26px;border-radius:4px"></div>' + scene(h, s))
hl("hw_tech_a", "Trained Techs. Licenses You Can Check.", "The tech at your door is trained and verified.", LAGOON)
hl("hw_tech_b", "Know Exactly Who's At Your Door", "Tap their profile to verify the license.", LAGOON)
hl("hw_scan_a", "A Moisture Scan Every Visit", "Whole home, every time.", LAG2)
hl("hw_scan_b", "Hidden Leaks, Caught Early", "We scan the whole home for moisture each visit.", LAG2)
hl("hw_ref_a", "An Honest Refund If You Cancel", "No runaround.", JUNGLE)
hl("hw_ref_b", "Cancel Anytime. Get A Fair Refund.", "Simple and honest.", JUNGLE)
# caught early check styles
F("ce_stamp", scene("Caught Early", "", f'<div style="width:220px;height:220px;border:10px solid {JUNGLE};border-radius:50%;display:flex;align-items:center;justify-content:center;transform:rotate(-8deg);margin-bottom:30px;font-family:Khand;font-weight:700;font-size:44px;color:{JUNGLE}">CAUGHT<br>EARLY</div>'), ".h{display:none}")
F("ce_chip", f'<div class="card" style="display:flex;align-items:center;gap:22px;padding:26px 40px"><div style="width:72px;height:72px;border-radius:50%;background:{JUNGLE};color:#fff;font-size:48px;line-height:72px">✓</div><div style="text-align:left"><div class="h" style="font-size:52px">Caught Early</div><div style="font-size:30px;color:{MUTE}">Behind the water heater</div></div></div>')
# license badge
F("lic_seal", f'<div style="width:260px;height:260px;border-radius:50%;border:8px solid {LAGOON};display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff"><div style="font-size:90px;color:{LAGOON};line-height:1">✓</div><div class="h" style="font-size:40px">License Verified</div></div><div class="s">Seal on every tech profile</div>')
# refund visual
F("ref_receipt", f'<div class="card" style="width:560px;text-align:left;font-size:32px"><div class="h" style="font-size:44px">Your Refund</div><div style="display:flex;justify-content:space-between;margin-top:12px"><span>Months left</span><b>Refunded</b></div><div style="margin-top:20px;display:inline-block;border:5px solid {JUNGLE};color:{JUNGLE};font-family:Khand;font-weight:700;font-size:44px;padding:2px 20px;transform:rotate(-4deg)">REFUNDED</div></div><div class="s">An honest refund if you cancel</div>')
# logo placement
F("logo_bug", f'<div class="logo" style="position:absolute;right:40px;top:30px;width:220px;height:76px"></div>' + scene("Do You Change Your Air Filters?", "") )
F("logo_endbig", f'<div class="logo" style="width:620px;height:215px"></div><div class="h" style="font-size:52px">{PRICE}</div>')
F("logo_endsmall", f'<div class="logo" style="width:260px;height:90px;margin-bottom:16px"></div><div class="h" style="font-size:66px">{PRICE}</div>')
# end card layouts
F("end_split", f'<div style="display:flex;width:1280px;height:720px"><div style="flex:1;background:url({POLO}) center/cover"></div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:60px;text-align:left"><div class="logo" style="width:360px;height:125px;background-position:left"></div><div class="h" style="font-size:52px;margin-top:10px">Membership Starting at <span style="color:{TERRA}">$99</span>/Month</div></div></div>')
F("end_band", f'<div class="logo" style="width:480px;height:166px"></div><div style="position:absolute;bottom:0;left:0;right:0;height:170px;background:#fff;border-top:6px solid {TERRA};display:flex;align-items:center;justify-content:center"><div class="h" style="font-size:56px">{PRICE}</div></div>', "body{justify-content:flex-start;padding-top:150px}")
# color amount
F("col_one", scene("A Moisture Scan Every Visit", "Hidden leaks, caught early.", f'<div style="width:120px;height:120px;border-radius:50%;background:{LAGOON}22;border:6px solid {LAGOON};margin-bottom:30px"></div>'))
F("col_three", scene("A Moisture Scan Every Visit", "Hidden leaks, caught early.", f'<div style="display:flex;gap:30px;margin-bottom:30px"><div style="width:100px;height:100px;border-radius:50%;background:{LAGOON}"></div><div style="width:100px;height:100px;border-radius:50%;background:{JUNGLE}"></div><div style="width:100px;height:100px;border-radius:50%;background:{SAFFRON}"></div></div>').replace("Caught Early", f'<span style="color:{TERRA}">Caught Early</span>'))
# motion
def strip(key, cells):
    return F(key, '<div style="display:flex;gap:24px">' + "".join(f'<div class="card" style="width:380px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px"><div style="font-size:24px;color:{MUTE}">{a}</div><div style="margin-top:14px">{b}</div></div>' for a, b in cells) + "</div>")
H = lambda o, x="", s=1: f'<div class="h" style="font-size:40px;opacity:{o};transform:translateX({x}px) scale({s})">Caught Early</div>'
strip("mo_slide", [("0.0 s", H(.2, -60)), ("0.3 s", H(.7, -20)), ("0.6 s", H(1))])
strip("mo_pop", [("0.0 s", H(.3, 0, .7)), ("0.2 s", H(1, 0, 1.08)), ("0.35 s", H(1))])
strip("tr_fade", [("Scene A", H(1)), ("Cross-fade", H(.4) + f'<div class="h" style="font-size:40px;opacity:.4;color:{MUTE}">Trained Techs</div>'), ("Scene B", f'<div class="h" style="font-size:40px">Trained Techs</div>')])
strip("tr_wipe", [("Scene A", H(1)), ("Bar wipes across", f'<div style="width:300px;height:180px;background:linear-gradient(90deg,{TERRA} 0 40%,transparent 40%)"></div>'), ("Scene B", f'<div class="h" style="font-size:40px">Trained Techs</div>')])

def svgimg(key, w=1280, h=720):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><image href="img/vv2_{key}.jpg" width="{w}" height="{h}"/></svg>'
pairs = []
def O(i, label, desc, tags, key, w=1280, h=720):
    return {"id": "vv2_" + i, "label": label, "desc": desc, "tags": tags, "feeling": None, "notes": True, "visual": {"type": "hm", "m": "svg", "svg": svgimg(key, w, h), "bg": CREAM}}
def S(i, label, desc, tags, bpm, words, color):
    return {"id": "vv2_" + i, "label": label, "desc": desc, "tags": tags, "feeling": None, "notes": True, "visual": {"type": "sound", "bpm": bpm, "words": words, "color": color, "bg": CREAM}}
def add(group, ask, a, b): pairs.append({"group": group, "category": "Smart Upkeep Video V.2: " + group, "app": "Smart Upkeep Video V.2", "ask": ask, "optionA": a, "optionB": b, "purpose": "refine", "retest": False, "notes": True})

if "--skip-frames" not in sys.argv:
    for k in ["beat1_open", "beat2_hook", "beat7_tech_tech_A", "beat7_tech_tech_B", "beat8_scan_scan_A", "beat8_scan_scan_B", "beat9_refund", "beat10_end_end_A", "beat10_end_end_B", "beat1_open_text_B", "beat2_hook_text_B", "beat8_scan_text_B", "beat9_refund_text_B", "beat10_end", "beat10_end_9x16",
              "beat4_life_color_A", "beat4_life_color_B", "beat7_tech"]: still(k, k.lower())
    v1frame(2.5, "v1_hook"); v1frame(57, "v1_licensed")
    save(Image.open(f"{MOCK}/polo_white_black-logo.png"), "polo_white"); save(Image.open(f"{MOCK}/polo_terracotta.png"), "polo_terra")
    photo_scan("scan_photo", 0); render_frames()

G = dict(T="Text Size", W="Headline Wording", O="Opening Hook", M="Moisture Scan", K="Tech Look", L="License Badge", R="Refund Promise", G="Logo", E="End Card", C="Color Amount", N="Motion", U="Music", F="Format")
add(G["T"], "How Big Should On-Screen Text Be?", O("txt_v1_frame", "V.1 Size (Real V.1 Frame)", "A real V.1 frame: headline about 6% of frame height, checklist text near 1.5%.", ["v1", "small"], "v1_licensed"),
    O("txt_7_frame", "Bigger: Key Line About 7% Of Height", "Same tech beat rebuilt: headline about 7-8% of frame height, support line about 4.5%.", ["big", "readable"], "txt_7"))
add(G["T"], "How Big Should Support Lines Be?", O("txt_v1_sup", "V.1 Support Size", "Support line at V.1 size (about 2.4% of height), headline about 5%.", ["v1", "small"], "txt_v1"),
    O("txt_sup_big", "Bigger Support Line (About 4.5%)", "Same scene; headline about 7%, support line about 4.5% of height.", ["big", "readable"], "txt_sup_big"))
add(G["W"], "Headline For The Tech Beat?", O("hw_tech_a", "Trained Techs. Licenses You Can Check.", "States both facts plainly.", ["direct", "proof"], "hw_tech_a"), O("hw_tech_b", "Know Exactly Who's At Your Door", "Leads with the homeowner's feeling.", ["warm", "human"], "hw_tech_b"))
add(G["W"], "Headline For The Moisture Scan Beat?", O("hw_scan_a", "A Moisture Scan Every Visit", "Says what we do.", ["plain", "service"], "hw_scan_a"), O("hw_scan_b", "Hidden Leaks, Caught Early", "Says what you get.", ["benefit", "punchy"], "hw_scan_b"))
add(G["W"], "Headline For The Refund Beat?", O("hw_ref_a", "An Honest Refund If You Cancel", "Calm and direct.", ["honest", "plain"], "hw_ref_a"), O("hw_ref_b", "Cancel Anytime. Get A Fair Refund.", "Two short sentences.", ["punchy", "freedom"], "hw_ref_b"))
add(G["O"], "How Should V.2 Open?", O("op_logo", "Logo First (V.2 Still)", "Open on the Smart Upkeep logo for about 2 seconds, then the hook.", ["brand", "calm"], "beat1_open_text_b"), O("op_question", "Question First (V.2 Still)", "Cold open on 'Do You Change Your Air Filters?'; logo comes later.", ["hook", "fast"], "beat2_hook_text_b"))
add(G["O"], "Which Hook Question?", O("op_v1q", "V.1 Hook: Water Heater (Real V.1 Frame)", "Keep V.1's 'When Was The Last Time You Flushed Your Water Heater?'", ["v1", "familiar"], "v1_hook"), O("op_v2q", "V.2 Hook: Air Filters (V.2 Still)", "New, shorter question with bigger type.", ["new", "short"], "beat2_hook"))
add(G["M"], "Which Moisture Scan Look?", O("ms_meter", "Room Map With Readings (V.2 Still)", "Floor plan with Dry / Normal readings and one 'Check Here' spot, like meter readings.", ["data", "clear"], "beat8_scan_scan_a"), O("ms_thermal", "Thermal Spot (V.2 Still)", "Thermal-camera style patch behind the water heater with a 'Check Here' tag.", ["visual", "thermal"], "beat8_scan_scan_b"))
add(G["M"], "Illustrated Or Photo-Real Scan?", O("ms_illus", "Illustrated", "Flat drawing that matches the rest of the video.", ["illustrated", "consistent"], "beat8_scan_text_b"), O("ms_photo", "Photo-Real", "A real room photo with a blue moisture spot overlay. Stand-in photo; final would be shot.", ["photo", "real"], "scan_photo"))
add(G["M"], "Which 'Caught Early' Check?", O("ce_stamp", "Round Stamp", "A tilted jungle-green stamp lands on the spot.", ["bold", "stamp"], "ce_stamp"), O("ce_chip", "Check Chip", "A white card with a green check and where it was found.", ["clean", "calm"], "ce_chip"))
add(G["K"], "How Should The Tech Appear?", O("tk_illus", "Illustrated Tech (V.2 Still)", "Drawn tech beside the verify card.", ["illustrated", "consistent"], "beat7_tech_tech_a"), O("tk_polo", "Real Person In The Polo", "Mockup: white polo with the Smart Upkeep logo on a real person.", ["photo", "real"], "polo_white"))
add(G["K"], "Van Or Polo For The Tech Beat?", O("tk_van", "Branded Van (V.2 Still)", "A Smart Upkeep van beside the verify card.", ["vehicle", "brand"], "beat7_tech_tech_b"), O("tk_terra", "Terracotta Polo", "Mockup: terracotta polo with a white logo on a real person.", ["photo", "warm"], "polo_terra"))
add(G["L"], "Which License Verify Badge?", O("lb_card", "Profile Card With Tap To Verify (V.2 Still)", "Certified / Trained tags, a 'Tap To Verify License' button and 'License Verified'.", ["detailed", "app"], "beat7_tech"), O("lb_seal", "Big Round Seal", "One large lagoon seal: 'License Verified'.", ["simple", "bold"], "lic_seal"))
add(G["R"], "Which Refund Visual?", O("rf_list", "Itemized List (V.2 Still)", "A short card with three refund lines.", ["clear", "itemized"], "beat9_refund"), O("rf_stamp", "Refunded Stamp", "A receipt card with a green 'Refunded' stamp.", ["visual", "stamp"], "ref_receipt"))
add(G["R"], "Refund Line Under The Headline?", O("rf_w_short", "Short Line: 'No Runaround.'", "Headline plus two words.", ["short", "plain"], "rf_short"), O("rf_w_items", "Itemized Lines (V.2 Still)", "Three short lines on a card. Check the wording against the real refund policy first.", ["detailed", "clear"], "beat9_refund_text_b"))
add(G["G"], "Logo At The Open?", O("lg_open_big", "Big Centered Logo (V.2 Still)", "Logo alone, large, then the hook.", ["brand", "bold"], "beat1_open"), O("lg_open_bug", "Small Corner Logo", "Hook plays at once; small logo sits top right.", ["fast", "quiet"], "logo_bug"))
add(G["G"], "Logo Size At The End?", O("lg_end_big", "Big Logo, Price Below", "Logo about half the frame width.", ["brand", "bold"], "logo_endbig"), O("lg_end_small", "Small Logo, Big Price", "The price line is the hero.", ["offer", "direct"], "logo_endsmall"))
add(G["E"], "Which End Card Layout?", O("ec_stack", "Stacked (V.2 Still)", "Logo over the price line, centered.", ["simple", "centered"], "beat10_end_end_a"), O("ec_side", "Side By Side (V.2 Still)", "Logo left, price right.", ["wide", "modern"], "beat10_end_end_b"))
add(G["E"], "Which End Card Layout?", O("ec_split", "Split With Tech Photo", "Polo photo left, logo and price right.", ["human", "photo"], "end_split"), O("ec_band", "Logo With White Price Band", "Logo up top; price in a white band with a terracotta rule.", ["clean", "bold"], "end_band"))
add(G["C"], "How Much Color In A Scene?", O("co_one", "One Pop", "One lagoon accent in the scene; everything else ink on cream.", ["restrained", "calm"], "col_one"), O("co_three", "Three Pops", "Lagoon, jungle and saffron marks plus a terracotta word.", ["lively", "multi-accent"], "col_three"))
add(G["C"], "Color In Busy Scenes?", O("co_mute", "Mostly Gray (V.2 Still)", "Calendar blocks in gray with a few green.", ["calm", "muted"], "beat4_life_color_a"), O("co_mix", "Mixed Accents (V.2 Still)", "Calendar blocks in jungle, lagoon and saffron.", ["lively", "multi-accent"], "beat4_life_color_b"))
add(G["N"], "How Should Text Come In?", O("mn_slide", "Calm Slide", "Text slides in about 60px and fades up over 0.6 s.", ["calm", "smooth"], "mo_slide"), O("mn_pop", "Gentle Pop", "Text scales from 70% with a small overshoot over 0.35 s.", ["lively", "playful"], "mo_pop"))
add(G["N"], "Which Scene Transition?", O("mn_fade", "Soft Cross-Fade", "Scenes melt into each other over about 0.4 s.", ["calm", "soft"], "tr_fade"), O("mn_wipe", "Accent Bar Wipe", "A terracotta bar sweeps across and reveals the next scene.", ["energetic", "brand"], "tr_wipe"))
add(G["U"], "Which Music Mood?", S("mu_acoustic", "Warm Acoustic Guitar", "Fingerpicked guitar, about 92 BPM, warm and homey.", ["warm", "craft"], 92, ["guitar", "warm", "92 bpm"], TERRA),
    S("mu_piano", "Light Upbeat Piano", "Bright piano chords, about 112 BPM, light and optimistic.", ["bright", "upbeat"], 112, ["piano", "light", "112 bpm"], LAGOON))
add(G["U"], "How Should The Music End?", S("mu_sting", "Soft Two-Note Chime On The Logo", "A small chime as the end card lands.", ["clean", "sting"], 60, ["chime", "end", "1 s"], JUNGLE),
    S("mu_resolve", "No Sting, Music Resolves", "The track simply resolves on a soft chord.", ["calm", "soft"], 70, ["chord", "resolve", "soft"], SAFFRON))
add(G["F"], "Which Format Leads?", O("fm_169", "16:9 Leads (V.2 Still)", "Built wide for the site and YouTube; 9:16 cut made after.", ["wide", "web"], "beat10_end"), O("fm_916", "9:16 Leads (V.2 Still)", "Built tall for Reels and Shorts; 16:9 cut made after.", ["vertical", "social"], "beat10_end_9x16", 720, 1280))

# audio clips
sys.path.insert(0, "."); import audio_synth as A, numpy as np
def piano(bpm):
    out = np.zeros(int(A.SR * 4)); beat = 60 / bpm
    for k, ch in enumerate([[60, 64, 67], [65, 69, 72], [67, 71, 74], [64, 67, 72]] * 2):
        for m in ch:
            f = A.note(m); tt = A.t(1.2); s = sum(np.sin(2 * np.pi * f * h * tt) / h ** 1.5 for h in (1, 2, 3, 4)) * np.exp(-3 * tt); A.place(out, s * .25, k * beat)
    return out
def resolve(bpm):
    out = np.zeros(int(A.SR * 3)); A.place(out, A.pad([A.note(m) for m in (55, 60, 64, 67)], 2.8) * .5, 0); return out
A.RECIPES.update({"vv2_mu_acoustic": A.r_acoustic, "vv2_mu_piano": piano, "vv2_mu_sting": A.r_chime, "vv2_mu_resolve": resolve})
for p in pairs:
    for s in "AB":
        o = p["option" + s]
        if o["visual"]["type"] == "sound": A.render(o)

for i, p in enumerate(pairs, 1): p.update(id=f"{DID}-{i:02d}", repeat=False)
ids = [p["option" + s]["id"] for p in pairs for s in "AB"]
assert len(ids) == len(set(ids)), "duplicate option id"
for p in pairs:
    for s in "AB":
        v = p["option" + s]["visual"]
        if v["type"] == "hm": k = v["svg"].split("img/")[1].split('"')[0]; assert os.path.exists(f"{IMG}/{k}"), k
ledger = json.load(open("shown_options.json")); shown = {k for k, v in ledger.get("options", {}).items() if v != [DID]}
for fp in glob.glob("decks/*.json"):
    if os.path.basename(fp) == f"{DID}.json": continue
    for pp in json.load(open(fp)).get("pairs", []):
        for s in "AB":
            o = pp.get("option" + s) or {}
            if o.get("id"): shown.add(o["id"])
vis = [p["option" + x]["visual"].get("svg") for p in pairs for x in "AB" if p["option" + x]["visual"]["type"] == "hm"]
assert len(vis) == len(set(vis)), "repeated visual"
rep = [i for i in ids if i in shown]; assert not rep, f"repeats: {rep}"
txt = json.dumps(pairs).lower()
for bad in [" ai ", "health score", "forecast", "smartkeep", "silver", "gold", "platinum", "a la carte"]: assert bad not in txt, bad
from trim_deck import DECK_SIZE, select, save_overflow  # decks are 25 pairs; extras go to banks/overflow
pairs, _cut = select(pairs, DECK_SIZE); save_overflow(DID, _cut)
ids = [p["option" + s]["id"] for p in pairs for s in "AB"]
groups = {}
for p in pairs: groups[p["group"]] = groups.get(p["group"], 0) + 1
now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
deck = {"date": DID, "version": 4, "owner": "Max Weberman", "format": "pairs", "english_only": True, "light_only": True, "notes": True,
        "title": "Smart Upkeep Explainer Video V.2: Plan Before Production",
        "brands": ["Smart Upkeep explainer video V.2: at most 45 s; only price 'Membership Starting at $99/Month'; beats: trained techs with verifiable licenses, whole-home moisture scan every visit, honest refund if you cancel",
                   "Light mode, cream #FAF3EB or white base, Khand/Hind, Title Case, 2-3 small pops of terracotta, lagoon, jungle, saffron; bigger text than V.1; new music"],
        "generated_at": now, "groups": groups, "allocation": {p["category"]: 1 for p in pairs}, "apps": {"Smart Upkeep Video V.2": len(pairs)},
        "sources": {"v1_video": V1, "v1_build": "/workspace/smartkeep/video/build/index3.html", "v2_stills": ST, "mockups": MOCK, "logos": "/workspace/brand/smart-upkeep/logos"},
        "freshness": {"option_slots": len(ids), "never_shown_before": len(ids), "share": 1.0}, "warnings": [], "pairs": pairs}
json.dump(deck, open(f"decks/{DID}.json", "w"), indent=1, ensure_ascii=False)
opts = ledger["options"]
for k in [k for k, v in opts.items() if v == [DID]]: del opts[k]
for i in ids: opts[i] = [DID]
ledger["options"] = dict(sorted(opts.items())); ledger["shown_count"] = len(opts); ledger["updated"] = now
json.dump(ledger, open("shown_options.json", "w"), indent=1)
print(len(pairs), "pairs", groups)
