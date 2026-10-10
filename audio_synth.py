"""Generate short, real audio clips for Style Swipe "sound" cards (podcast / audio branding).

Each sound option gets a ~3-5 s clip rendered with numpy (plus espeak-ng for spoken lines when
available), encoded to MP3 with ffmpeg, saved under audio/<option_id>.mp3. Clips are played with
plain <audio> elements on the page (not WebAudio), so they work after a tap on iOS Safari/Android.
"""
import os, shutil, subprocess, tempfile, wave
import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(ROOT, "audio")

def t(sec): return np.arange(int(SR * sec)) / SR
def env(n, a=0.005, r=0.3):
    x = np.ones(n); na, nr = int(SR * a), min(n, int(SR * r))
    if na: x[:na] = np.linspace(0, 1, na)
    if nr: x[-nr:] *= np.linspace(1, 0, nr)
    return x
def note(f): return 440.0 * 2 ** ((f - 69) / 12)
def place(buf, sig, at):
    i = int(SR * at); j = min(len(buf), i + len(sig)); buf[i:j] += sig[: j - i]
def pluck(freq, dur=1.5, bright=0.5):
    n = int(SR * dur); p = max(2, int(SR / freq)); rng = np.random.default_rng(int(freq))
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = (bright * buf[i % p] + (1 - bright) * buf[(i + 1) % p]) * 0.996 if i >= p else buf[i % p]
    return out * env(n, 0.001, 0.2)
def sine(freq, dur, decay=3.0):
    tt = t(dur); return np.sin(2 * np.pi * freq * tt) * np.exp(-decay * tt)
def bell(freq, dur=1.6):
    tt = t(dur)
    return (np.sin(2*np.pi*freq*tt) + .4*np.sin(2*np.pi*freq*2.76*tt)*np.exp(-4*tt) + .2*np.sin(2*np.pi*freq*5.4*tt)*np.exp(-7*tt)) * np.exp(-2.2*tt)
def saw(freq, dur):
    tt = t(dur); return 2 * ((tt * freq) % 1) - 1
def lowpass(x, a=0.05):
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y
def noise(dur, seed=0): return np.random.default_rng(seed).uniform(-1, 1, int(SR * dur))
def kick(dur=0.35):
    tt = t(dur); f = 120 * np.exp(-18 * tt) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-9 * tt)
def pad(freqs, dur, a=0.6):
    tt = t(dur); x = sum(np.sin(2*np.pi*f*tt) + .3*np.sin(2*np.pi*f*2.003*tt) for f in freqs)
    return x / len(freqs) * env(len(tt), a, 0.8)

def speak(text, voice="en", speed=150):
    """espeak-ng TTS -> float array at SR (None if espeak-ng is missing)."""
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe: return None
    with tempfile.TemporaryDirectory() as d:
        raw = os.path.join(d, "s.wav"); res = os.path.join(d, "r.wav")
        subprocess.run([exe, "-v", voice, "-s", str(speed), "-w", raw, text], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ar", str(SR), "-ac", "1", res], check=True)
        with wave.open(res) as w:
            return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768

# ---- recipes ---------------------------------------------------------------
def r_acoustic(bpm):
    out = np.zeros(int(SR * 4)); beat = 60 / bpm / 2
    for k, m in enumerate([52, 59, 64, 67, 71, 67, 64, 59, 55, 62, 67, 71]):
        place(out, pluck(note(m), 1.6, 0.5) * 0.5, k * beat)
    return out
def r_ukulele(bpm):
    out = np.zeros(int(SR * 3.5)); beat = 60 / bpm
    for k in range(8):
        for j, m in enumerate([67, 72, 76, 79] if k % 2 == 0 else [65, 69, 72, 77]):
            place(out, pluck(note(m), 0.6, 0.3) * 0.3, k * beat / 2 + j * 0.012)
    tt = t(0.6); whistle = np.sin(2*np.pi*(note(84) + 30*np.sin(2*np.pi*6*tt))*tt) * env(len(tt), 0.05, 0.2) * 0.25
    for k, at in enumerate([1.6, 2.2]): place(out, whistle, at)
    return out
def r_site_foley(bpm):
    out = np.zeros(int(SR * 3.2))
    for at in (0.1, 0.5, 0.9):     # hammer: thump + sharp noise click
        place(out, kick(0.25) * 0.9, at); place(out, noise(0.05, int(at*10)) * np.exp(-60 * t(0.05)) * 0.8, at)
    tt = t(1.4); f = 180 + 520 * np.minimum(1, tt / 0.3)     # drill spin-up whine
    drill = (np.sign(np.sin(2*np.pi*np.cumsum(f)/SR)) * 0.25 + noise(1.4, 3) * 0.15) * env(len(tt), 0.05, 0.3)
    place(out, lowpass(drill, 0.25), 1.5)
    return out
def r_bilingual_host(bpm):
    out = np.zeros(int(SR * 4.5)); place(out, pad([note(57), note(64), note(69)], 4.5, 0.8) * 0.18, 0)
    en = speak("Hello, and welcome.", "en-us", 150); th = speak("สวัสดีครับ", "th", 130)
    if en is not None: place(out, en * 0.9, 0.4)
    if th is not None: place(out, th * 0.9, 2.2)
    if en is None and th is None:   # no TTS available: two-note "hel-lo" motif instead
        place(out, bell(note(76)) * 0.5, 0.5); place(out, bell(note(72)) * 0.5, 0.9)
    return out
def r_khaen(bpm):
    out = np.zeros(int(SR * 4)); beat = 60 / bpm
    drone = sum(lowpass(saw(note(m), 4), 0.12) for m in (57, 64)) * 0.18 * env(int(SR*4), 0.2, 0.5)
    out += drone
    mel = [69, 72, 74, 76, 74, 72, 69, 67]
    for k, m in enumerate(mel):
        s = lowpass(saw(note(m), beat * 0.9), 0.15) * env(int(SR*beat*0.9), 0.02, 0.08) * 0.35
        place(out, s, k * beat * 0.5)
    for k in range(int(4 / beat)):
        place(out, kick(0.3) * 0.5, k * beat)
        place(out, noise(0.04, k) * np.exp(-80*t(0.04)) * 0.25, k * beat + beat / 2)
    return out
def r_lofi(bpm):
    dur = 4.5; out = np.zeros(int(SR * dur)); beat = 60 / bpm
    out += lowpass(pad([note(m) for m in (57, 60, 64, 67)], dur, 0.3), 0.08) * 0.5
    for k in range(int(dur / beat)):
        place(out, kick(0.35) * 0.7, k * beat)
        if k % 2: place(out, lowpass(noise(0.12, k), 0.4) * np.exp(-25*t(0.12)) * 0.45, k * beat)
    crackle = np.zeros(len(out)); rng = np.random.default_rng(7)
    crackle[rng.integers(0, len(out), 120)] = rng.uniform(-0.4, 0.4, 120)
    return out + crackle
def r_chime(bpm):
    out = np.zeros(int(SR * 2.4)); place(out, bell(note(79), 1.8) * 0.6, 0.05); place(out, bell(note(86), 1.8) * 0.6, 0.45)
    return out
def r_nature(bpm):
    dur = 4.5; rain = lowpass(noise(dur, 11), 0.35) * 0.35
    out = rain.copy()
    for k, at in enumerate([0.4, 0.55, 1.6, 1.75, 1.9, 3.1, 3.25]):   # bird chirps
        tt = t(0.09); f = 3200 + 1400 * np.sin(np.pi * tt / 0.09)
        place(out, np.sin(2*np.pi*np.cumsum(f)/SR) * env(len(tt), 0.005, 0.03) * 0.35, at)
    tt = t(dur); cic = np.sin(2*np.pi*4800*tt) * (0.5 + 0.5*np.sign(np.sin(2*np.pi*35*tt))) * 0.06
    return out + cic * env(len(tt), 1.0, 1.0)
def r_news(bpm):
    out = np.zeros(int(SR * 3.5)); beat = 60 / bpm
    for k in range(6): place(out, sine(note(41 + (k % 2) * 5), 0.6, 5) * 0.8, k * beat / 2)
    br = sum(lowpass(saw(note(m), 1.4), 0.2) for m in (60, 64, 67, 72)) / 4 * env(int(SR*1.4), 0.03, 0.4) * 0.7
    place(out, br, 6 * beat / 2)
    return out
def r_dark_synth(bpm):
    dur = 4.5; tt = t(dur)
    x = sum(lowpass(saw(note(33) * d, dur), 0.03) for d in (1, 1.006, 0.994)) / 3
    x *= (0.6 + 0.4 * np.sin(2*np.pi*0.5*tt)); sub = np.sin(2*np.pi*note(33)/2*tt) * 0.5
    return (x + sub) * env(len(tt), 0.8, 1.0)

RECIPES = {
    "pd_acoustic_intro": r_acoustic, "pd_site_foley": r_site_foley, "pd_bilingual_host": r_bilingual_host,
    "pd_khaen_loop": r_khaen, "pd_lofi_bed": r_lofi, "pd_clean_chime": r_chime, "pd_nature_bed": r_nature,
    "pd_news_drums": r_news, "pd_synth_dark": r_dark_synth, "pd_ukulele_happy": r_ukulele,
}
def recipe_for(opt):
    if opt["id"] in RECIPES: return RECIPES[opt["id"]]
    tags = set(opt.get("tags", []))      # sensible defaults for future sound options
    if tags & {"construction", "industrial"}: return r_site_foley
    if tags & {"dark", "cinematic"}: return r_dark_synth
    if tags & {"natural", "tropical"}: return r_nature
    if tags & {"playful", "vibrant"}: return r_ukulele
    if tags & {"thai"}: return r_khaen
    if tags & {"calm", "soft"}: return r_lofi
    if tags & {"warm", "craft"}: return r_acoustic
    return r_chime

def render(opt, force=False):
    """Make audio/<id>.mp3 for a sound option (cached). Returns the path."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    path = os.path.join(AUDIO_DIR, f"{opt['id']}.mp3")
    if os.path.exists(path) and not force: return path
    x = recipe_for(opt)(opt["visual"].get("bpm", 90))
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    fade = int(SR * 0.05); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "96k", path], check=True)
    return path
