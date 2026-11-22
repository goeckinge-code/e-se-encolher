"""Monta o vídeo final de um episódio: quadros do Blender + legendas karaokê, títulos, números,
etiquetas que seguem objetos, X vermelho, transições em chicote e efeitos sonoros.

Uso: python3 golpes/montar.py ep01-piramide [--de 0 --ate 10] [--still 12.3,40]
Precisa de: Pillow, numpy, ffmpeg. Saída: golpes/renders/<ep>/<ep>.mp4 (sem voz) e sfx.wav
"""
import os, sys, json, math, subprocess, wave, struct, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "assets", "fonts")
EP = sys.argv[1]
sys.path.insert(0, os.path.join(ROOT, EP))
import roteiro as R

W, H, FPS = R.W, R.H, R.FPS
OUT = os.path.join(ROOT, "renders", EP)
INK = (30, 27, 46)
YEL = (255, 214, 64)
COL = {"g": (88, 214, 102), "r": (255, 82, 82), "w": (255, 255, 255)}

def font(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)
F_CAP = font("LilitaOne.ttf", 96)
F_TIT = font("LilitaOne.ttf", 150)
F_BIG = font("LilitaOne.ttf", 120)
F_PILL = font("Nunito-Black.ttf", 46)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def back(x, s=2.2):
    x = clamp(x) - 1; return 1 + x * x * ((s + 1) * x + s)

# ------------------------------------------------------------------ peças de texto (com cache)
_cache = {}
def outlined(txt, fnt, fill, stroke=INK, sw=10, shadow=8, grad=None):
    """Texto com contorno grosso e sombra embaixo. grad=(cor_topo, cor_base) pinta em degradê."""
    key = (txt, id(fnt), fill, stroke, sw, shadow, grad)
    if key in _cache: return _cache[key]
    l, t, r, b = fnt.getbbox(txt, stroke_width=sw)
    w, h = r - l + 4, b - t + shadow + 4
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    if shadow:
        d.text((2 - l, 2 - t + shadow), txt, font=fnt, fill=stroke + (255,), stroke_width=sw, stroke_fill=stroke + (255,))
    d.text((2 - l, 2 - t), txt, font=fnt, fill=fill + (255,), stroke_width=sw, stroke_fill=stroke + (255,))
    if grad:
        mask = Image.new("L", (w, h)); ImageDraw.Draw(mask).text((2 - l, 2 - t), txt, font=fnt, fill=255)
        g = Image.new("RGBA", (w, h)); gd = ImageDraw.Draw(g)
        for y in range(h):
            k = clamp((y - 0.15 * h) / (0.7 * h))
            gd.line([(0, y), (w, y)], fill=tuple(int(a + (bb - a) * k) for a, bb in zip(grad[0], grad[1])) + (255,))
        im.paste(g, (0, 0), mask)
    _cache[key] = im; return im

def caption_img(words, active):
    """Duas palavras lado a lado; a palavra falada fica amarela."""
    parts = [outlined(w.upper().strip(",.:"), F_CAP, YEL if i == active else (255, 255, 255)) for i, w in enumerate(words)]
    gap = 22
    w = sum(p.width for p in parts) + gap * (len(parts) - 1); h = max(p.height for p in parts)
    im = Image.new("RGBA", (w, h)); x = 0
    for p in parts: im.alpha_composite(p, (x, h - p.height)); x += p.width + gap
    return im

def pill_img(label, dot):
    key = ("pill", label, dot)
    if key in _cache: return _cache[key]
    l, t, r, b = F_PILL.getbbox(label)
    tw, th = r - l, b - t
    pad, dr = 26, 13
    w, h = tw + pad * 2 + dr * 2 + 14, 84
    im = Image.new("RGBA", (w + 8, h + 10))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 8, w + 4, h + 8), h // 2, fill=(0, 0, 0, 60))
    d.rounded_rectangle((0, 0, w, h), h // 2, fill=(255, 255, 255, 255), outline=INK + (255,), width=4)
    rgb = tuple(int(dot.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    d.ellipse((pad - 4, h / 2 - dr, pad - 4 + dr * 2, h / 2 + dr), fill=rgb + (255,))
    d.text((pad + dr * 2 + 8 - l, (h - th) / 2 - t), label, font=F_PILL, fill=INK + (255,))
    _cache[key] = im; return im

def x_img():
    if "x" in _cache: return _cache["x"]
    s = 150; im = Image.new("RGBA", (s + 10, s + 10)); d = ImageDraw.Draw(im)
    d.ellipse((6, 10, s + 6, s + 10), fill=(0, 0, 0, 70))
    d.ellipse((0, 0, s, s), fill=(232, 52, 64, 255), outline=(255, 255, 255, 255), width=9)
    m = 44
    for a, b in (((m, m), (s - m, s - m)), ((s - m, m), (m, s - m))):
        d.line([a, b], fill=(255, 255, 255, 255), width=20)
    _cache["x"] = im; return im

def scaled(im, k):
    if abs(k - 1) < 0.01: return im
    k = max(0.02, k)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)

def place(base, im, cx, cy, k=1.0, alpha=1.0):
    im = scaled(im, k)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def title_img(txt):
    lines = txt.split("\n")
    parts = [outlined(l, F_TIT, (255, 214, 64), stroke=(74, 36, 10), sw=12, shadow=12,
                      grad=((255, 236, 120), (255, 172, 20))) for l in lines]
    w = max(p.width for p in parts); h = sum(p.height for p in parts) - 18 * (len(parts) - 1)
    im = Image.new("RGBA", (w, h)); y = 0
    for p in parts: im.alpha_composite(p, ((w - p.width) // 2, y)); y += p.height - 18
    if im.width > W - 80: im = scaled(im, (W - 80) / im.width)
    return im

def fmt(n): return f"{n:,}".replace(",", ".")

# ------------------------------------------------------------------ eventos de som
SFX = []   # (tempo, tipo)

def frame_for(t_global):
    """Qual plano e qual quadro dele."""
    for sh in R.SHOTS:
        s0 = sh["start"]; n = sh["frames"]
        if t_global < s0 + n / FPS - 1e-6: return sh, int(round((t_global - s0) * FPS))
    sh = R.SHOTS[-1]; return sh, sh["frames"] - 1

_anch = {}
def anchors(sh):
    if sh["id"] not in _anch:
        p = os.path.join(OUT, "frames", sh["id"], "anchors.json")
        _anch[sh["id"]] = json.load(open(p)) if os.path.exists(p) else {}
    return _anch[sh["id"]]

def compose(sh, f):
    t = f / FPS
    p = os.path.join(OUT, "frames", sh["id"], f"{min(f, sh['frames'] - 1):05d}.jpg")
    if os.path.exists(p): base = Image.open(p).convert("RGB")
    else: base = Image.new("RGB", (W, H), (60, 60, 70))
    if base.size != (W, H): base = base.resize((W, H), Image.LANCZOS)
    base = ImageEnhance.Color(base).enhance(1.1)
    # chicote: desfoque horizontal forte nos 4 primeiros quadros
    if sh.get("whip") and f < 4:
        k = (4 - f) / 4
        arr = np.asarray(base).astype(np.float32); acc = np.zeros_like(arr); n = 9
        for i in range(n):
            acc += np.roll(arr, int((i - n / 2) * 26 * k + 120 * k), axis=1)
        base = Image.fromarray((acc / n).astype(np.uint8))
    # gancho: flash branco de impacto nos primeiros quadros do vídeo
    if sh is R.SHOTS[0] and f < 5:
        base = Image.blend(base, Image.new("RGB", (W, H), (255, 255, 255)), (5 - f) / 6)
    im = base.convert("RGBA")
    def wt(word): return R.wt(sh, word)
    # números grandes (com contador opcional no s18)
    for txt, word, col, y in sh.get("big", []):
        t0 = wt(word)
        if sh.get("count") and txt.startswith("10 BILH"):
            ta = wt(sh["count"][0])
            if ta <= t < t0:
                k = clamp((t - ta) / (t0 - ta)); lvl = 1 + int(k * 9)
                c = outlined(fmt(10 ** lvl), F_BIG, (255, 255, 255))
                place(im, c, W / 2, H * y, 1.0)
                lab = outlined(f"PESSOAS NO NÍVEL {lvl}", F_PILL, (255, 255, 255), sw=6, shadow=4)
                place(im, lab, W / 2, H * y + 100)
        if t >= t0:
            k = back((t - t0) / 0.25) * (1.6 if sh is R.SHOTS[0] else 1.0)   # no gancho o número é maior
            place(im, outlined(txt, F_BIG, COL[col]), W / 2, H * y, k)
    # título de capítulo
    if sh.get("title"):
        txt, word = sh["title"]; t0 = wt(word)
        if t >= t0: place(im, title_img(txt), W / 2, H * 0.17, back((t - t0) / 0.3))
    # etiquetas que seguem objetos
    an = anchors(sh).get(str(min(f, sh["frames"] - 1)), {})
    for label, obj, word, dot in sh.get("pills", []):
        t0 = wt(word)
        if t < t0: continue
        pos = an.get(obj)
        if obj == "card" or not pos: x, y = W * 0.62, H * 0.3
        else: x, y = pos[0] * W, pos[1] * H - 70
        pi = pill_img(label, dot)
        x = min(max(x, pi.width / 2 + 30), W - pi.width / 2 - 30); y = min(max(y, 330), H - 520)
        place(im, pi, x, y, back((t - t0) / 0.25))
    # X vermelho
    if sh.get("x") and t >= wt(sh["x"]):
        place(im, x_img(), 170, 300, back((t - wt(sh["x"])) / 0.25))
    # legenda (2 palavras; a falada em amarelo)
    groups = R.captions(sh)
    for gi, (a, b, ws) in enumerate(groups):
        nxt = groups[gi + 1][0] if gi + 1 < len(groups) else sh["dur"] + 1
        if a <= t < nxt or (gi == 0 and t < a):
            active = 0 if len(ws) == 1 or t < ws[1][0] else 1
            place(im, caption_img([w for _, _, w in ws], active), W / 2, H * sh.get("cap", 0.68))
            break
    return im.convert("RGB")

def collect_sfx():
    for sh in R.SHOTS:
        s0 = sh["start"]
        if sh.get("whip"): SFX.append((s0, "whoosh"))
        for _, word, *_ in sh.get("big", []): SFX.append((s0 + R.wt(sh, word), "pop"))
        for _, _, word, _ in sh.get("pills", []): SFX.append((s0 + R.wt(sh, word), "plin"))
        if sh.get("title"): SFX.append((s0 + R.wt(sh, sh["title"][1]), "boom"))
        if sh.get("x"): SFX.append((s0 + R.wt(sh, sh["x"]), "buzz"))
        if sh is R.SHOTS[0]: SFX.extend([(0.0, "boom"), (0.03, "whoosh"), (0.25, "fanfare")])
        if sh["id"] == "s24": SFX.append((s0 + R.wt(sh, "bloquear"), "clang"))

# ------------------------------------------------------------------ síntese dos efeitos (sem arquivos externos)
SR = 48000
def env(n, a=0.005, d=0.15):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)

def synth(kind):
    rnd = np.random.default_rng(len(kind))
    if kind == "pop":
        n = int(0.18 * SR); t = np.arange(n) / SR
        f = 380 + 900 * np.exp(-t * 30); return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.05)
    if kind == "plin":
        n = int(0.35 * SR); t = np.arange(n) / SR
        return 0.28 * (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2093 * t)) * env(n, 0.002, 0.09)
    if kind == "boom":
        n = int(0.6 * SR); t = np.arange(n) / SR
        f = 60 + 140 * np.exp(-t * 12)
        s = 0.7 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.22)
        return s + 0.2 * rnd.standard_normal(n) * env(n, 0.001, 0.03)
    if kind == "buzz":
        n = int(0.4 * SR); t = np.arange(n) / SR
        sq = np.sign(np.sin(2 * np.pi * 150 * t)) + np.sign(np.sin(2 * np.pi * 156 * t))
        return 0.13 * sq * env(n, 0.005, 0.25) * (t < 0.32)
    if kind == "whoosh":
        n = int(0.4 * SR); noise = rnd.standard_normal(n)
        k = np.hanning(n); out = np.convolve(noise, np.ones(30) / 30, "same") * k
        return 0.6 * out / (np.abs(out).max() + 1e-9) * 0.7
    if kind == "clang":
        n = int(0.9 * SR); t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * t) / (i + 1) for i, f in enumerate((220, 563, 921, 1340)))
        return 0.35 * s * env(n, 0.001, 0.25)
    if kind == "fanfare":
        out = np.zeros(int(1.2 * SR))
        for i, f in enumerate((523, 659, 784, 1047)):
            n = int(0.5 * SR); t = np.arange(n) / SR; st = int(i * 0.12 * SR)
            out[st:st + n] += 0.18 * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(n, 0.005, 0.3)
        return out
    return np.zeros(10)

def music(total):
    """Batida leve e contínua (o vídeo nunca fica em silêncio). 120 bpm, kick + hat + baixo."""
    n = int(total * SR); out = np.zeros(n); beat = 60 / 120
    kick = synth("boom")[: int(0.25 * SR)] * 0.5
    t = np.arange(int(0.06 * SR)) / SR
    hat = np.random.default_rng(1).standard_normal(len(t)) * np.exp(-t * 80) * 0.06
    bassnotes = [55, 55, 65.4, 49]
    i = 0; tt = 0.0
    while tt < total:
        s = int(tt * SR)
        if i % 2 == 0: out[s:s + len(kick)] += kick[: max(0, n - s)]
        h0 = int((tt + beat / 2) * SR); out[h0:h0 + len(hat)] += hat[: max(0, n - h0)]
        bn = int(beat * SR); tb = np.arange(bn) / SR
        f = bassnotes[(i // 4) % 4]
        b = 0.09 * np.sin(2 * np.pi * f * tb) * np.exp(-tb * 3)
        out[s:s + bn] += b[: max(0, n - s)]
        i += 1; tt += beat
    return out

def write_audio(path, total):
    mix = music(total)
    for t0, kind in SFX:
        s = synth(kind); i = int(t0 * SR); j = min(len(mix), i + len(s))
        if i < len(mix): mix[i:j] += s[: j - i]
    mix = mix / max(1.0, np.abs(mix).max() / 0.89)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ------------------------------------------------------------------ principal
if __name__ == "__main__":
    args = sys.argv[2:]
    if "--still" in args:
        os.makedirs(os.path.join(OUT, "check"), exist_ok=True)
        for x in args[args.index("--still") + 1].split(","):
            sh, f = frame_for(float(x)); compose(sh, f).save(os.path.join(OUT, "check", f"c_{float(x):06.2f}.jpg"), quality=88)
        sys.exit()
    total_frames = sum(sh["frames"] for sh in R.SHOTS)
    a = int(float(args[args.index("--de") + 1]) * FPS) if "--de" in args else 0
    b = int(float(args[args.index("--ate") + 1]) * FPS) if "--ate" in args else total_frames
    collect_sfx()
    wav = os.path.join(OUT, "sfx.wav"); write_audio(wav, total_frames / FPS)
    mp4 = os.path.join(OUT, f"{EP}.mp4" if (a, b) == (0, total_frames) else f"{EP}_trecho.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-ss", str(a / FPS), "-i", wav, "-map", "0:v", "-map", "1:a", "-shortest",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    starts = []
    for sh in R.SHOTS:
        for f in range(sh["frames"]): starts.append((sh, f))
    for g in range(a, b):
        sh, f = starts[g]
        ff.stdin.write(compose(sh, f).tobytes())
        if g % 150 == 0: print("quadro", g, "/", b, flush=True)
    ff.stdin.close(); ff.wait()
    print("OK", mp4)
