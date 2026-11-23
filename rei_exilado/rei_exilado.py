"""O Rei Exilado — teste de animação em pixel art com rolagem lateral.

Tudo é desenhado em baixa resolução (320x180) e ampliado 6x sem suavização
para 1920x1080. Camadas com paralaxe, luz pontual quantizada com dither
(tocha do rei, braseiros, incêndio do castelo) e reflexo na água.

Uso: python3 rei_exilado/rei_exilado.py  ->  rei_exilado/rei_exilado.mp4
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 320, 180
SCALE = 6
FPS = 24
DUR = 18.0
GROUND = 118          # linha do chão (pés do rei)
BANK = 132            # início da água
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rei_exilado.mp4")
rng = np.random.default_rng(7)


def c(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


# ---------------------------------------------------------------- primitivas
def layer(width):
    return np.zeros((H, width, 4), np.float32)


def px(L, x, y, col):
    if 0 <= y < L.shape[0] and 0 <= x < L.shape[1]:
        L[y, x, :3] = col
        L[y, x, 3] = 1


def rect(L, x0, y0, x1, y1, col):
    x0, x1 = max(0, x0), min(L.shape[1], x1)
    y0, y1 = max(0, y0), min(L.shape[0], y1)
    if x0 < x1 and y0 < y1:
        L[y0:y1, x0:x1, :3] = col
        L[y0:y1, x0:x1, 3] = 1


def blob(L, cx, cy, r, ramp, rough=0.35):
    """Copa/arbusto: círculo irregular, mais claro em cima (luz da lua)."""
    for y in range(int(cy - r - 2), int(cy + r + 2)):
        for x in range(int(cx - r - 2), int(cx + r + 2)):
            dx, dy = (x - cx) / r, (y - cy) / r
            d = math.hypot(dx, dy) + rng.uniform(-rough, rough) * 0.3
            if d < 1:
                s = (-dy * 0.6 + (1 - d) * 0.5) + rng.uniform(-0.25, 0.25)
                i = int(np.clip((s + 0.3) / 1.3 * len(ramp), 0, len(ramp) - 1))
                px(L, x, y, ramp[i])


def bricks(L, x0, y0, x1, y1, base, mortar, bw=6, bh=3):
    for y in range(y0, y1):
        row = (y - y0) // bh
        for x in range(x0, x1):
            if (y - y0) % bh == bh - 1 or (x - x0 + (row % 2) * (bw // 2)) % bw == 0:
                px(L, x, y, mortar)
            else:
                px(L, x, y, base * rng.uniform(0.85, 1.12))


# ---------------------------------------------------------------- roteiro
WALK_END = 15.5
SPEED = 24


def king_x(t):
    s = min(t, WALK_END)
    x = 60 + SPEED * s
    if t > WALK_END - 1.0:            # desacelera antes de parar
        u = min(1, (t - (WALK_END - 1.0)) / 1.0)
        x = 60 + SPEED * (WALK_END - 1.0) + SPEED * (u - u * u / 2)
    if t < 0.6:
        x = 60 + SPEED * t * t / 1.2
    return x


MAXCAM = int(king_x(DUR) - 130) + 4


def cam_x(t):
    return max(0.0, king_x(t) - 130)


def lw(f):
    return W + int(f * MAXCAM) + 8


# ---------------------------------------------------------------- cenário
def build_sky():
    sky = np.zeros((H, W, 3), np.float32)
    top, mid = c("#0a1318"), c("#4a6e7c")
    for y in range(H):
        u = min(1, y / 95)
        sky[y] = top * (1 - u) + mid * u
    for _ in range(40):
        sky[rng.integers(0, 45), rng.integers(0, W)] = c("#9fb8c4")
    return sky


def build_far():                       # floresta distante (paralaxe 0.15)
    L = layer(lw(0.15))
    ramp = [c("#13242a"), c("#1a2f35"), c("#23404a")]
    x = 0
    while x < L.shape[1]:
        tw = rng.integers(2, 5)
        rect(L, x, 30, x + tw, GROUND, c("#1b3038"))
        x += rng.integers(9, 20)
    for x in range(-10, L.shape[1] + 10, 14):
        blob(L, x + rng.integers(-4, 4), rng.integers(8, 34), rng.integers(12, 20), ramp)
    rect(L, 0, 0, L.shape[1], 10, ramp[0])
    rect(L, 0, 96, L.shape[1], GROUND, c("#1d353b"))
    return L


def build_mid():                       # árvores do meio (0.45)
    L = layer(lw(0.45))
    ramp = [c("#0e1c14"), c("#162b1c"), c("#203d27"), c("#2c5232")]
    x = 6
    while x < L.shape[1]:
        tw = rng.integers(4, 9)
        bark = c("#22201a")
        rect(L, x, 20, x + tw, GROUND, bark)
        for y in range(24, GROUND, 3):         # textura de casca
            px(L, x + rng.integers(0, tw), y, c("#363024"))
        rect(L, x - 2, GROUND - 3, x + tw + 2, GROUND, bark)   # raízes
        for _ in range(4):
            blob(L, x + tw / 2 + rng.integers(-16, 16), rng.integers(0, 30), rng.integers(10, 17), ramp)
        x += rng.integers(30, 52)
    return L


def build_bush():                      # arbustos (0.75)
    L = layer(lw(0.75))
    ramp = [c("#13261a"), c("#1d3a24"), c("#2a5530"), c("#3f7340")]
    x = 0
    while x < L.shape[1]:
        for _ in range(rng.integers(2, 4)):
            blob(L, x + rng.integers(-8, 8), GROUND - rng.integers(4, 12), rng.integers(6, 12), ramp)
        x += rng.integers(22, 48)
    return L


EMIT = []      # (x_mundo, y, tamanho) chamas fixas no cenário
LIGHTS = []    # (x_mundo, y, raio, cor, intensidade)


def build_ground():                    # plano do rei (1.0)
    L = layer(lw(1.0))
    Wl = L.shape[1]
    # muro de pedra da margem
    bricks(L, 0, GROUND + 1, Wl, BANK, c("#3e3a33"), c("#211d19"), 7, 4)
    # grama com tufos
    g = [c("#1f3a1c"), c("#2f5526"), c("#46742f")]
    rect(L, 0, GROUND - 1, Wl, GROUND + 2, g[1])
    for x in range(Wl):
        h = rng.integers(0, 4)
        for k in range(h):
            px(L, x, GROUND - 1 - k, g[min(2, k)])
        if rng.random() < 0.3:
            px(L, x, GROUND + 2, g[0])        # musgo escorrendo
    # ---- castelo em chamas (início)
    stone, mort = c("#55535a"), c("#2a282d")
    bricks(L, 14, 40, 100, GROUND, stone, mort)
    bricks(L, 2, 22, 30, GROUND, stone * 1.05, mort)           # torre
    for bx in range(2, 30, 6):
        rect(L, bx, 17, bx + 4, 22, stone)
    for bx in range(30, 100, 7):
        rect(L, bx, 35, bx + 4, 40, stone)
    rect(L, 46, 84, 72, GROUND, c("#120d0c"))                  # portão
    for y in range(78, 84):
        w = int(13 * math.sqrt(1 - ((y - 84) / 7) ** 2))
        rect(L, 59 - w, y, 59 + w, y + 1, c("#120d0c"))
    for gx in range(48, 72, 4):                                # grade quebrada
        rect(L, gx, 78, gx + 1, 96 + (gx * 7) % 9, c("#3b3634"))
    for wx, wy in [(12, 36), (12, 60), (30, 56), (84, 56), (64, 50)]:
        rect(L, wx, wy, wx + 4, wy + 7, c("#120d0c"))
        EMIT.append((wx + 2, wy + 6, 3))
    for fx, fy, s in [(10, 17, 6), (40, 35, 5), (80, 35, 7), (24, 17, 4)]:
        EMIT.append((fx, fy, s))
    LIGHTS.extend([(16, 30, 70, c("#ff6a2a"), 1.0), (60, 50, 80, c("#ff7a30"), 0.9), (84, 40, 60, c("#ff5520"), 0.8)])
    # ---- estandarte caído
    rect(L, 130, 104, 131, GROUND, c("#4a3a28"))
    for y in range(104, 112):
        rect(L, 131, y, 131 + (8 - (y - 104) // 2) - (y % 3), y + 1, c("#7a1a28"))
    # ---- santuário em ruínas com braseiros
    pal, dark = c("#8a877c"), c("#4a4841")
    for x0 in (226, 262):
        bricks(L, x0, 80, x0 + 10, GROUND, pal, dark, 5, 5)
        rect(L, x0 - 2, 76, x0 + 12, 80, pal * 1.1)
        rect(L, x0 - 1, GROUND - 4, x0 + 11, GROUND, pal * 0.9)
        for ry in (88, 98):                                     # runas entalhadas
            rect(L, x0 + 3, ry, x0 + 7, ry + 1, dark)
            rect(L, x0 + 3, ry + 3, x0 + 7, ry + 4, dark)
            rect(L, x0 + 3, ry, x0 + 4, ry + 4, dark)
        rect(L, x0 + 1, 72, x0 + 9, 76, c("#3a3028"))           # braseiro
        EMIT.append((x0 + 5, 71, 6))
        LIGHTS.append((x0 + 5, 70, 75, c("#ffa040"), 1.1))
    bricks(L, 222, 66, 246, 72, pal, dark, 6, 3)               # arco partido
    for (fx, fy) in [(250, 114), (254, 116), (247, 116)]:       # escombros
        rect(L, fx, fy, fx + 4, fy + 3, pal * 0.8)
    # estátua (figura original: guardião com escudo)
    st = c("#6f6d66")
    rect(L, 240, 108, 254, GROUND, st)
    rect(L, 244, 86, 251, 108, st)
    rect(L, 245, 79, 250, 86, st)
    rect(L, 239, 90, 245, 104, st * 0.8)                       # escudo
    rect(L, 251, 70, 252, 100, st * 0.9)                       # lança
    for _ in range(40):                                        # musgo/heras
        px(L, rng.integers(238, 256), rng.integers(84, GROUND), c("#3c6a32"))
    # ---- carroça abandonada
    wood = c("#5a3f26")
    rect(L, 318, 102, 346, 111, wood)
    for xx in range(318, 346, 5):
        rect(L, xx, 102, xx + 1, 111, wood * 0.7)
    rect(L, 346, 108, 362, 109, wood)
    for a in range(0, 360, 12):                                # roda quebrada
        if 200 < a < 280:
            continue
        r = math.radians(a)
        px(L, int(326 + 6 * math.cos(r)), int(112 + 6 * math.sin(r)), wood * 0.8)
    rect(L, 336, 114, 344, 118, wood * 0.6)
    # ---- placa
    rect(L, 412, 96, 414, GROUND, wood)
    rect(L, 404, 97, 424, 101, wood * 1.2)
    rect(L, 406, 103, 420, 107, wood * 1.1)
    # ---- acampamento: barraca, fogueira e um estranho encapuzado
    tent = c("#6b5a3a")
    for y in range(92, GROUND):
        w = (y - 92) * 0.9
        rect(L, int(560 - w), y, int(560 + w), y + 1, tent * (0.75 if y % 4 == 0 else 1))
    rect(L, 558, 104, 562, GROUND, c("#1c1510"))
    rect(L, 526, GROUND - 2, 540, GROUND, c("#3a2a1a"))        # lenha
    EMIT.append((533, GROUND - 3, 8))
    LIGHTS.append((533, GROUND - 8, 90, c("#ffb050"), 1.3))
    cloak = c("#2c2e3a")
    rect(L, 510, 104, 520, GROUND, cloak)                       # sentado
    rect(L, 511, 98, 518, 105, cloak)
    rect(L, 516, 101, 518, 103, c("#1a1214"))                   # rosto na sombra
    return L


# ---------------------------------------------------------------- o rei
PAL = {"Y": "#f2c84b", "y": "#b88a2a", "S": "#d29a74", "s": "#3a2418", "H": "#5a3a28",
       "W": "#d8d0c0", "w": "#958b7a", "R": "#2b4fa8", "r": "#18306e", "B": "#2e2420",
       "b": "#6a4a1e", "T": "#6b4a2a"}
PAL = {k: c(v) for k, v in PAL.items()}
TOP = ["....Y.Y.Y...",
       "....YYYYY...",
       "....HSSSS...",
       "....HSSsS...",
       "...RHHHSS...",
       "..RRWWWWS.T.",
       ".RRRWWWWSST.",
       ".RRrWWWW..T.",
       "RRrrWbbW..T.",
       "RRrrWWWW....",
       "RRrrWwwW....",
       "RrrrWwwW...."]
TOP_B = TOP[:8] + [".RrrWbbW..T.", "RRrrWWWW....", ".RrrWwwW....", "RRrrWwwW...."]
LEGS = [["RRr.B..B....", "Rr..B...B...", "r..B....B...", "...B.....B..", "..BB.....BB."],
        ["RRr..BB.....", "Rr...BB.....", "r....BB.....", ".....BB.....", ".....BBB...."]]
IDLE = ["Rrr..B.B....", "Rr...B.B....", "r....B.B....", ".....B.B....", "....BB.BB..."]


def draw_king(img, w, sx, t, moving, dist):
    if moving:
        f = int(dist / 5) % 4
        rows = (TOP if f < 2 else TOP_B) + LEGS[f % 2]
        bob = 1 if f % 2 else 0
    else:
        rows = (TOP if int(t * 2) % 2 else TOP_B) + IDLE
        bob = 0
    y0 = GROUND - len(rows) + 1 - bob
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                x, y = int(sx) + i, y0 + j
                if 0 <= x < W and 0 <= y < H:
                    img[y, x] = PAL[ch]
                    w[y, x] = 1
    return int(sx) + 10, y0 + 4          # ponta da tocha


# ---------------------------------------------------------------- fogo
FIRE = [c("#fff4b0"), c("#ffc63a"), c("#f07a1e"), c("#b8321a")]


def fire(img, x, y, s, t, seed):
    r = np.random.default_rng(int(t * FPS) * 131 + seed)
    for i in range(-(s // 2), s - s // 2):
        hmax = s * (1.6 - abs(i) / max(1, s) * 1.6)
        h = int(max(1, hmax * r.uniform(0.5, 1.1)))
        for k in range(h):
            col = FIRE[min(3, int(k / h * 4))]
            xx, yy = x + i, y - k
            if 0 <= xx < W and 0 <= yy < H:
                img[yy, xx] = col


# ---------------------------------------------------------------- texto
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CAPTIONS = [(0.6, 4.2, "O castelo caiu."),
            (4.8, 8.6, "Expulso do próprio reino,"),
            (9.2, 12.8, "o rei vaga pela floresta..."),
            (13.4, 16.0, "...em busca de um novo lar.")]


def text_mask(txt, size, cy):
    cw, ch = 960, 540
    im = Image.new("L", (cw, ch), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"                  # sem antialias: borda de pixel
    f = ImageFont.truetype(FONT, size)
    bw = d.textlength(txt, font=f)
    d.text(((cw - bw) / 2, cy), txt, font=f, fill=255)
    m = np.array(im) > 127
    o = m.copy()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1), (0, 2)]:
        o |= np.roll(np.roll(m, dy, 0), dx, 1)
    up = lambda a: a.repeat(2, 0).repeat(2, 1)
    return up(m), up(o)


TXT = [(a, b, text_mask(s, 24, 40)) for a, b, s in CAPTIONS]
TITLE = text_mask("O REI EXILADO", 56, 200)
SUB = text_mask("capítulo I", 22, 270)

# ---------------------------------------------------------------- render
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16
BAY = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]
YY, XX = np.mgrid[0:BANK, 0:W].astype(np.float32)
AMBIENT = c("#4a5878") * 0.85


def main():
    sky = build_sky()
    layers = [(build_far(), 0.15, 0.2), (build_mid(), 0.45, 0.45), (build_bush(), 0.75, 0.8),
              (build_ground(), 1.0, 1.0)]
    flies = [(rng.uniform(0, 700), rng.uniform(60, 115), rng.uniform(0, 6.28)) for _ in range(30)]
    drops = [(rng.uniform(0, 700), rng.integers(BANK + 3, H), rng.integers(2, 7)) for _ in range(60)]

    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W * SCALE}x{H * SCALE}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", OUT],
                          stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for fi in range(n):
        t = fi / FPS
        cam = cam_x(t)
        img = sky.copy()
        wgt = np.full((H, W), 0.12, np.float32)
        for L, f, wv in layers:
            o = int(round(cam * f))
            cr = L[:, o:o + W]
            a = cr[..., 3:4]
            img = img * (1 - a) + cr[..., :3] * a
            wgt = np.where(a[..., 0] > 0, wv, wgt)
        kx = king_x(t)
        moving = t < WALK_END
        tx, ty = draw_king(img, wgt, kx - cam, t, moving, kx - 60)

        # ---- luz: ambiente frio da noite + pontos quentes quantizados
        fl = 1 + 0.08 * math.sin(t * 23) + 0.05 * math.sin(t * 41)
        lights = [(tx, ty, 78 * fl, c("#ffb060"), 1.15)]
        for lx, ly, r, col, inten in LIGHTS:
            sx = lx - cam
            if -r < sx < W + r:
                lights.append((sx, ly, r * (1 + 0.06 * math.sin(t * 17 + lx)), col, inten))
        Lm = np.zeros((BANK, W, 3), np.float32)
        for sx, sy, r, col, inten in lights:
            d = np.sqrt((XX - sx) ** 2 + ((YY - sy) * 1.15) ** 2)
            fall = np.clip(1 - d / r, 0, 1) ** 1.6
            q = np.floor(fall * 5 + BAY[:BANK]) / 5          # bandas com dither
            Lm += q[..., None] * col * inten
        dawn = max(0, (t - 12) / 6) * 0.25                     # céu clareia no fim
        shade = AMBIENT * (1 + dawn) + wgt[:BANK, :, None] * Lm
        img[:BANK] *= shade

        # ---- emissivos (não recebem sombra)
        for k, (ex, ey, s) in enumerate(EMIT):
            sx = int(ex - cam)
            if -10 < sx < W + 10:
                fire(img, sx, ey, s, t, k)
        fire(img, int(tx), ty - 1, 3, t, 99)
        r2 = np.random.default_rng(fi)
        if cam < 120:                                          # brasas do castelo
            for _ in range(14):
                ex = int(r2.uniform(5, 100) - cam)
                ey = int(40 - r2.uniform(0, 40))
                if 0 <= ex < W and 0 <= ey < H:
                    img[ey, ex] = FIRE[r2.integers(1, 3)]
        for fx, fy, ph in flies:                               # vaga-lumes
            sx = int(fx - cam * 0.9 + 6 * math.sin(t * 0.8 + ph))
            sy = int(fy + 4 * math.sin(t * 1.3 + ph * 2))
            if 1 <= sx < W - 1 and 1 <= sy < BANK and math.sin(t * 2 + ph * 3) > -0.3:
                img[sy, sx] = c("#e8ff9a")
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    img[sy + dy, sx + dx] = img[sy + dy, sx + dx] * 0.5 + c("#9ab84a") * 0.5

        # ---- água: reflexo espelhado com ondulação
        for k in range(H - BANK):
            src = BANK - 1 - k
            off = int(round(math.sin(k * 0.9 + t * 3.0) * (0.5 + k * 0.06)))
            img[BANK + k] = np.roll(img[src], off, 0) * c("#4a6478") * (0.75 - k * 0.006)
        img[BANK] *= 0.4
        for dx0, dy, ln in drops:                              # riscos de luz na água
            sx = int((dx0 - cam + t * 4) % (W + 40)) - 20
            if math.sin(t * 2 + dx0) > 0:
                img[dy, max(0, sx):max(0, min(W, sx + ln))] += c("#3c4c58") * 0.6

        # ---- fade e vinheta
        fade = min(1, t / 1.0) * min(1, (DUR - t) / 1.2)
        img = np.clip(img * fade, 0, 1)
        big = (img * 255).astype(np.uint8).repeat(SCALE, 0).repeat(SCALE, 1)

        # ---- legendas
        def put(mask, alpha):
            m, o = mask
            fg = big.astype(np.float32)
            fg[o] = fg[o] * (1 - alpha) + np.array([20, 14, 12]) * alpha
            fg[m] = fg[m] * (1 - alpha) + np.array([240, 228, 196]) * alpha
            return fg.astype(np.uint8)
        for a, b, mk in TXT:
            if a <= t <= b:
                al = min(1, (t - a) / 0.4, (b - t) / 0.4)
                big = put(mk, al)
        if t > 15.8:
            al = min(1, (t - 15.8) / 0.8, (DUR - t) / 0.6)
            big = put(TITLE, al)
            big = put(SUB, al)
        ff.stdin.write(big.tobytes())
        if fi in (30, 60, 170, 300, 410):
            Image.fromarray(big).save(OUT.replace(".mp4", f"_f{fi:03d}.png"))
    ff.stdin.close()
    ff.wait()
    print("ok", OUT)


if __name__ == "__main__":
    main()
