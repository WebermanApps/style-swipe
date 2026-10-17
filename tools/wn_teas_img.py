"""Card images for the WellNest Teas refresh decks (R107, Oct 17 2026). Built directly on the WellNest mockups (Max 20:09 ICT):
option A = the mockup as drafted (pouch-*.jpg, or mockup-*.jpg with a side tag), option B = the same image with ONE small edit
(wash recolour, name or line re-set in the label's typewriter face, partner-name line, logo size, brushy edge, window, badge,
ingredient tag swap). Sources copied into each deck's own folder img/wn-teas-<tea>/src/; outputs img/wn-teas-<tea>/<pick>-<a|b>.jpg.
Ingredient photos: img/wn-tea/*.jpg (Wikimedia Commons, img/wn-tea/credits.json). Dried roselle: WellNest board product-roselle-dried.jpg.
Never writes under files/ or projects/."""
import os, shutil, colorsys, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/workspace/wellnest/teas"
DRIED = "/workspace/scratch/op-rollout/wellnest-dashboard/product-roselle-dried.jpg"
GF = "/usr/share/fonts/truetype/sand-box/google"
CP = {"regular": f"{GF}/Courier Prime/CourierPrime-Regular.ttf", "bold": f"{GF}/Courier Prime/CourierPrime-Bold.ttf", "light": "/usr/share/fonts/opentype/urw-base35/NimbusMonoPS-Regular.otf"}
HIND = {"r": f"{GF}/Hind/Hind-Regular.ttf", "sb": f"{GF}/Hind/Hind-SemiBold.ttf"}
KHAND = f"{GF}/Khand/Khand-SemiBold.ttf"
INKC = (58, 53, 49)
# label geometry on pouch-<tea>.jpg (589x720), measured on a 25 px grid; text bands from dark-pixel rows
GEO = {"calm": dict(L=106, R=488, T=201, B=652, title=(358, 422), sub=(445, 463), t="CALM", s="herbal tea"),
       "energy": dict(L=98, R=492, T=247, B=668, title=(373, 416), sub=(438, 465), t="ENERGY", s="oolong & herbs"),
       "beauty": dict(L=115, R=475, T=184, B=620, title=(364, 399), sub=(426, 440), t="BEAUTY", s="roselle herbal tea"),
       "powerhaus": dict(L=108, R=478, T=197, B=636, title=(384, 429), sub=(453, 470), t="RECOVER", s="for PowerHaus Pilates"),
       "vanni": dict(L=101, R=483, T=184, B=628, title=(379, 410), sub=(435, 449), t="SOFT BLUE", s="for Vanni Pilates"),
       "buds": dict(L=104, R=481, T=219, B=668, title=(410, 443), sub=(465, 478), t="UNWIND", s="for The Buds Station"),
       "roselle-refresh": dict(L=127, R=460, T=191, B=628, title=(377, 405), sub=(427, 440), tag=(468, 483), t="ROSELLE", s="organic herbal tea",
                               tg="tart, bright, gently sweet", logo=(292, 208, 452, 348))}
for _k, _g in GEO.items(): _g["key"] = _k
CROPS = {"full": (40, 160, 550, 626), "top": (127, 190, 460, 494), "title": (127, 300, 460, 604), "pouch": (0, 92, 589, 630), "low": (127, 400, 460, 704)}
MOCK_CROP = (470, 0, 1258, 720)
def font(p, s): return ImageFont.truetype(p, int(round(s)))
def arr(im): return np.asarray(im.convert("RGB")).astype(np.float32)
def img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def erase(a, x0, y0, x1, y1, seed=1):
    """fill a box with a vertical blend of the rows just above and below (paper texture kept with light noise)"""
    top = a[max(y0 - 4, 0):y0 - 1, x0:x1].mean(0); bot = a[y1 + 1:y1 + 4, x0:x1].mean(0)
    h = y1 - y0; t = np.linspace(0, 1, h)[:, None, None]
    fill = top[None] * (1 - t) + bot[None] * t
    rng = np.random.default_rng(seed); fill += rng.normal(0, 1.6, fill.shape)
    a[y0:y1, x0:x1] = fill; return a
def dark_extent(a, y0, y1, L, R):
    g = a[y0:y1, L + 4:R - 4].max(2); cols = np.where((g < 120).sum(0) > 0)[0]
    return L + 4 + cols.min(), L + 4 + cols.max()
def tracked(draw, x, y, text, f, fill, track):
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill); x += f.getlength(ch) + track
def tw(text, f, track): return sum(f.getlength(c) for c in text) + track * (len(text) - 1)
def set_line(im, g, band, old, new, weight="regular", maxw=None, seed=3):
    """erase a text band and set new text in Courier Prime at the same cap height, tracking and centre"""
    a = arr(im); y0, y1 = band; x0, x1 = dark_extent(a, y0, y1, g["L"], g["R"]); cx = (x0 + x1) / 2
    caps = old.upper() == old
    probe = font(CP[weight], 100); bb = probe.getbbox("H" if caps else "x")
    ref_h = (bb[3] - bb[1]); size = 100 * (y1 - y0) / ref_h if caps else 100 * (y1 - y0) / (probe.getbbox("hg")[3] - probe.getbbox("hg")[1])
    f = font(CP[weight], size); track = ((x1 - x0) - tw(old, f, 0)) / max(len(old) - 1, 1)
    track = max(track, 0)
    a = erase(a, g["L"] + 6, y0 - 7, g["R"] - 6, y1 + 7, seed); im = img(a); d = ImageDraw.Draw(im)
    maxw = maxw or (g["R"] - g["L"] - 44)
    while tw(new, f, track) > maxw and size > 8: size *= 0.95; f = font(CP[weight], size); track *= 0.95
    w = tw(new, f, track); top = f.getbbox("H" if caps else "h")[1]
    tracked(d, cx - w / 2, y0 - top - (0 if caps else 0), new, f, INKC, track)
    return im
def _hsv(reg):
    import matplotlib.colors as mc
    return mc.rgb_to_hsv(np.clip(reg, 0, 1))
def wash_hue(reg):
    h = _hsv(reg); m = (reg.max(2) - reg.min(2)) > 0.18
    hh = h[..., 0][m] * 2 * np.pi; return (np.degrees(np.arctan2(np.sin(hh).mean(), np.cos(hh).mean())) % 360)
WASH_HUE = {"calm": 312, "energy": 60, "beauty": 355, "powerhaus": 22, "vanni": 228, "buds": 38, "roselle-refresh": 5}
CREAM_HUE = 35
def hdist(h, ref): return np.abs(((h - ref) + 180) % 360 - 180)
def wash_alpha(reg, g):
    """0..1 wash coverage: strong colour (sat) OR the wash's own hue far from the cream paper hue"""
    h = _hsv(reg)[..., 0] * 360; sat = reg.max(2) - reg.min(2); wh = WASH_HUE[g["key"]]
    a_sat = np.clip((sat - 0.16) / 0.12, 0, 1)
    a_hue = (np.clip((30 - hdist(h, wh)) / 12, 0, 1) * np.clip((hdist(h, CREAM_HUE) - 18) / 10, 0, 1) * np.clip((sat - 0.025) / 0.04, 0, 1))
    return np.clip(np.maximum(a_sat, a_hue), 0, 1)
def recolour(im, g, hue, ks, kv, y_from=None):
    import matplotlib.colors as mc
    a = arr(im); x0, x1, y0, y1 = g["L"] + 6, g["R"] - 6, g["T"] + 5, g["B"] - 5
    reg = a[y0:y1, x0:x1] / 255.0; sat = reg.max(2) - reg.min(2)
    hsv = _hsv(reg); alpha = wash_alpha(reg, g)
    new = hsv.copy(); new[..., 0] = (hue % 360) / 360.0
    new[..., 1] = np.clip(hsv[..., 1] * ks, 0, 1); new[..., 2] = np.clip(hsv[..., 2] * kv, 0, 1)
    rgb = mc.hsv_to_rgb(new); out = reg * (1 - alpha[..., None]) + rgb * alpha[..., None]
    a[y0:y1, x0:x1] = out * 255; return img(a)
def wash_top(g): return (g.get("tag") or g["sub"])[1] + 6
def cream_row(o, g, x0, x1):
    r0, r1 = g["title"][0] - 40, g["title"][0] - 10
    c = np.median(o[r0:r1, x0:x1], 0); k = 15
    return np.stack([np.convolve(np.pad(c[:, i], k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid") for i in range(3)], 1)
def height(im, g, dy):
    """dy<0: fade the top of the wash back into cream so it sits lower; dy>0: stretch the wash band upward (text rows kept)"""
    o = arr(im); a = o.copy(); x0, x1 = g["L"] + 5, g["R"] - 5; y0 = wash_top(g) - 4; y1 = g["B"] - 4; H = y1 - y0
    cream = cream_row(o, g, x0, x1)[None]
    if dy < 0:
        x0, x1 = g["L"] + 1, g["R"] - 1; cream = cream_row(o, g, x0, x1)[None]; y0 = g["title"][1] + 3
        ys = np.arange(y0, y1)[:, None, None]; d = -dy + (wash_top(g) - 4 - y0)
        f = np.clip((ys - (y0 + d * 0.9)) / (d * 0.9), 0, 1)
        reg = o[y0:y1, x0:x1]; lum = reg.mean(2, keepdims=True); cl = cream.mean(2, keepdims=True)
        paper = cream * np.clip((lum + (cl - lum) * 0.55) / cl, 0, 1.2)
        out = paper * (1 - f) + reg * f; txt = reg.max(2, keepdims=True) < 170
        a[y0:y1, x0:x1] = np.where(txt, reg, out)
        return img(a)
    nh = H + dy; band = o[y0:y1, x0:x1]
    nb = arr(img(band).resize((x1 - x0, nh), Image.LANCZOS)) / 255.0
    al = wash_alpha(nb, g)[..., None]; top = y1 - nh
    a[top:y1, x0:x1] = a[top:y1, x0:x1] * (1 - al) + nb * 255 * al
    t0 = g["title"][0] - 8; t1 = wash_top(g)
    keep = o[t0:t1, x0:x1].max(2, keepdims=True) < 165
    a[t0:t1, x0:x1] = np.where(keep, o[t0:t1, x0:x1], a[t0:t1, x0:x1])
    return img(a)
def brushy(im, g):
    a = arr(im); x0, x1, y0, y1 = g["L"] + 5, g["R"] - 5, wash_top(g) + 4, g["B"] - 4
    reg = a[y0:y1, x0:x1]; sat = (reg.max(2) - reg.min(2)) / 255.0
    rng = np.random.default_rng(11); n = np.asarray(Image.fromarray((rng.random(((y1 - y0) // 3 + 1, (x1 - x0) // 3 + 1)) * 255).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BICUBIC)) / 255.0
    cream = np.median(a[wash_top(g) - 4:wash_top(g), x0:x1].reshape(-1, 3), 0)
    w = wash_alpha(reg / 255.0, g); base = np.clip(w, 0.15, 1)[..., None]; full = cream + (reg - cream) / base
    al = np.clip((w + (n - 0.5) * 0.35 - 0.45) * 9, 0, 1)[..., None]
    a[y0:y1, x0:x1] = cream * (1 - al) + np.clip(full * 0.9 + cream * 0.1, 0, 255) * al; return img(a)
def logo(im, g, k):
    a = arr(im); x0, y0, x1, y1 = g["logo"]; patch = img(a[y0:y1, x0:x1]); pa = arr(patch) / 255.0
    m = np.clip(((pa.max(2) - pa.min(2)) - 0.06) / 0.10 + (0.80 - pa.max(2)) / 0.25, 0, 1)
    a = erase(a, x0, y0, x1, y1, 9); w, h = x1 - x0, y1 - y0; nw, nh = int(w * k), int(h * k)
    sp = patch.resize((nw, nh), Image.LANCZOS); sm = Image.fromarray((m * 255).astype(np.uint8)).resize((nw, nh), Image.LANCZOS)
    im2 = img(a); cx, cy = (x0 + x1) // 2 + int(w * (1 - k) / 2 * 0.6), (y0 + y1) // 2
    im2.paste(sp, (cx - nw // 2, cy - nh // 2), sm); return im2
def over(im, g, text):
    d = ImageDraw.Draw(im); f = font(HIND["sb"], 15); track = 3.2; w = tw(text, f, track)
    a = arr(im); x0, x1 = dark_extent(a, *g["title"], g["L"], g["R"]); cx = (x0 + x1) / 2
    tracked(d, cx - w / 2, g["title"][0] - 34, text, f, INKC, track); return im
def line(im, g, text):
    d = ImageDraw.Draw(im); f = font(CP["regular"], 15); w = tw(text, f, 0.5)
    tracked(d, (g["L"] + g["R"]) / 2 - w / 2, g["sub"][1] + 12, text, f, INKC, 0.5); return im
def window(im):
    d = Image.open(DRIED).convert("RGB"); W, H = 120, 62; x, y = 236, 112
    s = min(d.width / W, d.height / H); c = d.crop((int((d.width - W * s) / 2), int((d.height - H * s) / 2), int((d.width + W * s) / 2), int((d.height + H * s) / 2))).resize((W, H), Image.LANCZOS)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), 10, fill=255)
    gl = Image.new("RGB", (W, H), (255, 255, 255)); c = Image.blend(c, gl, 0.12)
    im.paste(c, (x, y), m); ImageDraw.Draw(im).rounded_rectangle((x, y, x + W - 1, y + H - 1), 10, outline=(160, 128, 92), width=2); return im
def weight(im, g, kind):
    d = ImageDraw.Draw(im); R, B = g["R"], g["B"]
    if kind == "corner":
        f = font(CP["regular"], 12); d.text((R - 14 - f.getlength("NET WT"), B - 26), "NET WT", font=f, fill=(96, 70, 74))
    else:
        cx, cy, r = R - 42, B - 44, 28; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(250, 246, 238), outline=(176, 96, 110), width=2)
        f = font(CP["bold"], 12); [d.text((cx - f.getlength(t) / 2, cy + dy), t, font=f, fill=(96, 60, 66)) for t, dy in (("NET", -14), ("WT", 1))]
    return im
def claims(im, k):
    a = arr(im); x0, y0, x1, y1 = 74, 540, 482, 598; band = img(a[y0:y1, x0:x1]); ba = arr(band) / 255.0
    m = np.clip((0.62 - ba.max(2)) / 0.22, 0, 1); nw, nh = int((x1 - x0) * k), int((y1 - y0) * k)
    a = erase(a, x0, y0 - 2, min(x1 + 40, 598), y1 + 2, 13); im2 = img(a)
    im2.paste(band.resize((nw, nh), Image.LANCZOS), (x0 - 4, y0 - int((nh - (y1 - y0)) / 2)), Image.fromarray((m * 255).astype(np.uint8)).resize((nw, nh), Image.LANCZOS))
    return im2
def pinkicons(im):
    a = arr(im); pts = [(80, 312), (150, 320), (62, 377), (110, 397), (172, 400)]
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; mask = np.zeros(a.shape[:2], bool)
    for (cx, cy) in pts: mask |= (xx - cx) ** 2 + (yy - cy) ** 2 < 17 ** 2
    bg = np.asarray(img(a).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    ink = (bg.mean(2) - a.mean(2) > 18) & mask
    ink = np.asarray(Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
    a[ink] = np.array([206, 104, 122], np.float32); return img(a)
def tag_panel(im, spec):
    """cream side tag on the mockup's white space: head, small ingredient photo, rows (name + % bar) or lines"""
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = 418, 70, 774, 650
    d.rectangle((x0, y0, x1, y1), fill=(250, 246, 238), outline=(227, 221, 210), width=2)
    fh = font(KHAND, 46); d.text((x0 + 20, y0 + 10), spec["head"].upper(), font=fh, fill=(10, 10, 10))
    y = y0 + 76
    if spec.get("photo"):
        p = Image.open(os.path.join(ROOT, "img/wn-tea", spec["photo"] + ".jpg")).convert("RGB"); W, H = x1 - x0 - 36, 150
        s = min(p.width / W, p.height / H); p = p.crop((int((p.width - W * s) / 2), int((p.height - H * s) / 2), int((p.width + W * s) / 2), int((p.height + H * s) / 2))).resize((W, H), Image.LANCZOS)
        im.paste(p, (x0 + 18, y)); d.rectangle((x0 + 18, y, x0 + 18 + W, y + H), outline=(227, 221, 210), width=1); y += H + 16
    if spec.get("rows"):
        hi = spec.get("hi"); fr, fb = font(HIND["r"], 31), font(HIND["sb"], 31); fp = font(KHAND, 36)
        for i, (nm, pct) in enumerate(spec["rows"]):
            on = hi == "all" or hi == i; f = fb if on else fr; col = (10, 10, 10) if on else (107, 101, 96)
            words, lines = nm.split(), [""]
            for w_ in words:
                if f.getlength((lines[-1] + " " + w_).strip()) > (x1 - x0 - 120): lines.append(w_)
                else: lines[-1] = (lines[-1] + " " + w_).strip()
            for ln in lines: d.text((x0 + 18, y), ln, font=f, fill=col); y += 34
            d.text((x1 - 18 - fp.getlength(f"{pct}%"), y - 40), f"{pct}%", font=fp, fill=col)
            bw = (x1 - x0 - 36) * pct / 100; d.rectangle((x0 + 18, y + 2, x1 - 18, y + 10), fill=(238, 234, 228))
            d.rectangle((x0 + 18, y + 2, x0 + 18 + bw, y + 10), fill=(10, 10, 10) if on else (170, 162, 152)); y += 30
    for ln in spec.get("lines") or []:
        f = font(CP["bold"], 30); d.text((x0 + 18, y), ln, font=f, fill=INKC); y += 40
    return im
def cup_panel(im, photo, name):
    d = ImageDraw.Draw(im); p = Image.open(os.path.join(ROOT, "img/wn-tea", photo + ".jpg")).convert("RGB")
    D = 300; s = min(p.width, p.height); p = p.crop(((p.width - s) // 2, (p.height - s) // 2, (p.width + s) // 2, (p.height + s) // 2)).resize((D, D), Image.LANCZOS)
    m = Image.new("L", (D, D), 0); ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255); cx, cy = 596, 320
    im.paste(p, (cx - D // 2, cy - D // 2), m); d.ellipse((cx - D // 2, cy - D // 2, cx + D // 2, cy + D // 2), outline=(227, 221, 210), width=3)
    f = font(KHAND, 44); t = ("CUP: " + name).upper(); d.text((cx - f.getlength(t) / 2, cy + D // 2 + 16), t, font=f, fill=(10, 10, 10)); return im
def render(spec, out_dir, name):
    """spec -> jpg path (relative to ROOT); sources are copied into out_dir/src first"""
    os.makedirs(os.path.join(out_dir, "src"), exist_ok=True)
    def src(fn, from_=SRC):
        dst = os.path.join(out_dir, "src", os.path.basename(fn))
        if not os.path.exists(dst): shutil.copy2(os.path.join(from_, fn) if not os.path.isabs(fn) else fn, dst)
        return dst
    b = spec["base"]
    if b == "pouch":
        g = GEO[spec["tea"]]; im = Image.open(src(f"pouch-{spec['tea']}.jpg")).convert("RGB")
        for op in spec["ops"]:
            k = op[0]
            if k == "title": im = set_line(im, g, g["title"], g["t"], op[1], op[2] if len(op) > 2 else "regular")
            elif k == "sub": im = set_line(im, g, g["sub"], g["s"], op[1])
            elif k == "tag": im = set_line(im, g, g["tag"], g["tg"], op[1])
            elif k == "wash": im = recolour(im, g, op[1], op[2], op[3], wash_top(g) - 2)
            elif k == "height": im = height(im, g, op[1])
            elif k == "brushy": im = brushy(im, g)
            elif k == "logo": im = logo(im, g, op[1])
            elif k == "over": im = over(im, g, op[1])
            elif k == "line": im = line(im, g, op[1])
            elif k == "window": src(DRIED); im = window(im)
            elif k == "weight": im = weight(im, g, op[1])
        im = im.crop(CROPS[spec.get("crop", "full")])
    elif b == "mock":
        im = Image.open(src(f"mockup-{spec['tea']}.jpg")).convert("RGB").crop(MOCK_CROP)
        if spec.get("tag"): im = tag_panel(im, spec["tag"])
        if spec.get("cup"): im = cup_panel(im, spec["cup"], spec["cupname"])
        im = im.resize((624, 570), Image.LANCZOS)
    elif b == "photo":
        if spec["src"] == "current":
            im = Image.open(src("current-roselle.jpg")).convert("RGB")
            for op in spec["ops"]:
                if op[0] == "claims": im = claims(im, op[1])
            im = im.crop((20, 300, 600, 830 if False else 799)).resize((560, 480), Image.LANCZOS) if False else im.crop((40, 288, 600, 799))
        else:
            im = Image.open(src(os.path.join(ROOT, "img/wn-roselle/ref-back.jpg"))).convert("RGB")
            for op in spec["ops"]:
                if op[0] == "pinkicons": im = pinkicons(im)
            im = im.crop((30, 208, 292, 447)).resize((524, 478), Image.LANCZOS)
    p = os.path.join(out_dir, name + ".jpg"); im.save(p, "JPEG", quality=82, optimize=True, progressive=True)
    return os.path.relpath(p, ROOT), im.size
