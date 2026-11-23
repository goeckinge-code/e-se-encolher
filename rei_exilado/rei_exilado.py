"""O Rei Exilado — teste de animação em pixel art com rolagem lateral (v2).

A arte é desenhada em 320x180 ("pixel de arte"). A composição roda numa grade
3x mais fina (960x540) para a câmera e o rei deslizarem em sub-pixel, sem
tremer, e no fim tudo é ampliado 2x para 1920x1080, sem suavização.
Camadas com paralaxe, luz quantizada com dither, lago com correnteza,
reflexo e peixes pulando. O rei é um esqueleto 2D (coxa, canela, braço)
redesenhado a cada quadro, então a caminhada é contínua.

Uso: python3 rei_exilado/rei_exilado.py  ->  rei_exilado/rei_exilado.mp4
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 320, 180       # grade da arte
S = 3                 # sub-pixel da composição
FW, FH = W * S, H * S
UP = 2                # ampliação final -> 1920x1080
FPS = 30
DUR = 18.0
GROUND = 118
BANK = 132
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rei_exilado.mp4")
rng = np.random.default_rng(7)


def c(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


# ---------------------------------------------------------------- primitivas (arte)
def layer(width):
    return np.zeros((H, width, 4), np.float32)


def px(L, x, y, col):
    x, y = int(x), int(y)
    if 0 <= y < L.shape[0] and 0 <= x < L.shape[1]:
        L[y, x, :3] = col
        L[y, x, 3] = 1


def rect(L, x0, y0, x1, y1, col):
    x0, x1 = max(0, int(x0)), min(L.shape[1], int(x1))
    y0, y1 = max(0, int(y0)), min(L.shape[0], int(y1))
    if x0 < x1 and y0 < y1:
        L[y0:y1, x0:x1, :3] = col
        L[y0:y1, x0:x1, 3] = 1


def blob(L, cx, cy, r, ramp, rough=0.35):
    for y in range(int(cy - r - 2), int(cy + r + 2)):
        for x in range(int(cx - r - 2), int(cx + r + 2)):
            dx, dy = (x - cx) / r, (y - cy) / r
            d = math.hypot(dx, dy) + rng.uniform(-rough, rough) * 0.3
            if d < 1:
                s = (-dy * 0.6 + (1 - d) * 0.5) + rng.uniform(-0.25, 0.25)
                i = int(np.clip((s + 0.3) / 1.3 * len(ramp), 0, len(ramp) - 1))
                px(L, x, y, ramp[i])


def fern(L, x, y, size, cols):
    """Samambaia: leque de folhas curvas saindo do chão."""
    for a in np.linspace(-75, 75, rng.integers(5, 8)):
        ang = math.radians(a + rng.uniform(-8, 8))
        ln = size * rng.uniform(0.7, 1.0)
        for k in range(int(ln)):
            u = k / ln
            xx = x + math.sin(ang) * k
            yy = y - math.cos(ang) * k * (1 - u * 0.6) + u * u * 3
            px(L, xx, yy, cols[min(len(cols) - 1, int(u * len(cols)))])


def bricks(L, x0, y0, x1, y1, base, mortar, bw=6, bh=3):
    for y in range(y0, y1):
        row = (y - y0) // bh
        for x in range(x0, x1):
            if (y - y0) % bh == bh - 1 or (x - x0 + (row % 2) * (bw // 2)) % bw == 0:
                px(L, x, y, mortar)
            else:
                px(L, x, y, base * rng.uniform(0.85, 1.12))


# ---------------------------------------------------------------- movimento
WALK_END = 15.5
SPEED = 21


def king_x(t):
    if t < 0.8:
        return 60 + SPEED * t * t / 1.6
    if t < WALK_END - 1.2:
        return 60 + SPEED * (t - 0.4)
    u = min(1.0, (t - (WALK_END - 1.2)) / 1.2)
    return 60 + SPEED * (WALK_END - 1.6) + SPEED * 1.2 * (u - u * u / 2)


MAXCAM = int(king_x(DUR) - 130) + 4


def cam_x(t):
    # câmera alisada: acompanha o rei com atraso suave
    x = king_x(t) - 130
    if x > 10:
        return x
    return (x + 10) ** 2 / 40 if x > -10 else 0.0


def lw(f):
    return W + int(f * MAXCAM) + 10


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


def build_far():
    L = layer(lw(0.12))
    ramp = [c("#122228"), c("#182c33"), c("#203a44")]
    x = 0
    while x < L.shape[1]:
        rect(L, x, 25, x + rng.integers(2, 4), GROUND, c("#1b3038"))
        x += rng.integers(5, 11)
    for x in range(-10, L.shape[1] + 10, 9):
        blob(L, x + rng.integers(-4, 4), rng.integers(4, 34), rng.integers(12, 20), ramp)
    rect(L, 0, 0, L.shape[1], 8, ramp[0])
    for x in range(0, L.shape[1], 10):
        blob(L, x, 108 + rng.integers(-3, 3), rng.integers(8, 13), [c("#16292e"), c("#1c3238")])
    rect(L, 0, 104, L.shape[1], GROUND, c("#18292e"))
    return L


def build_far2():
    L = layer(lw(0.28))
    ramp = [c("#101e19"), c("#152820"), c("#1c3528")]
    x = 3
    while x < L.shape[1]:
        tw = rng.integers(3, 6)
        rect(L, x, 15, x + tw, GROUND, c("#1a231f"))
        for y in range(20, GROUND, 4):
            px(L, x + rng.integers(0, tw), y, c("#232e28"))
        x += rng.integers(13, 24)
    for x in range(-10, L.shape[1] + 10, 12):
        blob(L, x + rng.integers(-5, 5), rng.integers(0, 28), rng.integers(11, 18), ramp)
    for x in range(0, L.shape[1], 14):
        blob(L, x + rng.integers(-5, 5), GROUND - rng.integers(3, 9), rng.integers(6, 11), ramp)
    return L


def build_mid():
    L = layer(lw(0.5))
    ramp = [c("#0e1c14"), c("#162b1c"), c("#203d27"), c("#2c5232")]
    bark, barkl = c("#22201a"), c("#363024")
    x = 6
    while x < L.shape[1]:
        tw = rng.integers(5, 11)
        rect(L, x, 18, x + tw, GROUND, bark)
        for y in range(22, GROUND, 3):
            px(L, x + rng.integers(0, tw), y, barkl)
        rect(L, x - 3, GROUND - 3, x + tw + 3, GROUND, bark)
        rect(L, x - 1, GROUND - 6, x + tw + 1, GROUND - 3, bark)
        for side in (-1, 1):                                    # galhos
            by = rng.integers(30, 60)
            for k in range(rng.integers(6, 12)):
                px(L, x + (tw if side > 0 else 0) + side * k, by - k // 2, bark)
        for _ in range(6):
            blob(L, x + tw / 2 + rng.integers(-20, 20), rng.integers(-2, 34), rng.integers(10, 18), ramp)
        for _ in range(rng.integers(1, 4)):                     # cipós
            vx, vl = x + tw / 2 + rng.integers(-14, 14), rng.integers(10, 30)
            for k in range(vl):
                px(L, vx + round(math.sin(k * 0.3)), 30 + k, ramp[2])
        x += rng.integers(22, 38)
    return L


def build_bush():
    L = layer(lw(0.78))
    ramp = [c("#13261a"), c("#1d3a24"), c("#2a5530"), c("#3f7340")]
    fcols = [c("#1d3a24"), c("#2a5530"), c("#3f7340")]
    x = 0
    while x < L.shape[1]:
        for _ in range(rng.integers(2, 5)):
            blob(L, x + rng.integers(-10, 10), GROUND - rng.integers(4, 14), rng.integers(6, 13), ramp)
        fern(L, x + rng.integers(-6, 12), GROUND, rng.integers(9, 15), fcols)
        x += rng.integers(12, 26)
    return L


def build_front():                     # samambaias à frente do rei (1.2)
    L = layer(lw(1.2))
    cols = [c("#0b160d"), c("#102014"), c("#16301b")]
    x = 30
    while x < L.shape[1]:
        for _ in range(rng.integers(1, 3)):
            fern(L, x + rng.integers(-5, 5), GROUND + 4, rng.integers(7, 11), cols)
        x += rng.integers(45, 90)
    return L


EMIT = []      # chamas fixas: (x_mundo, y, tamanho)
LIGHTS = []    # (x_mundo, y, raio, cor, intensidade)
CAMP = 440     # acampamento


def build_ground():
    L = layer(lw(1.0))
    Wl = L.shape[1]
    bricks(L, 0, GROUND + 1, Wl, BANK, c("#3e3a33"), c("#211d19"), 7, 4)
    g = [c("#1f3a1c"), c("#2f5526"), c("#46742f")]
    rect(L, 0, GROUND - 1, Wl, GROUND + 2, g[1])
    for x in range(Wl):
        for k in range(rng.integers(0, 4)):
            px(L, x, GROUND - 1 - k, g[min(2, k)])
        if rng.random() < 0.3:
            px(L, x, GROUND + 2, g[0])
    # ---- castelo em chamas
    stone, mort = c("#55535a"), c("#2a282d")
    bricks(L, 14, 30, 104, GROUND, stone, mort)
    bricks(L, 0, 10, 30, GROUND, stone * 1.05, mort)
    for bx in range(0, 30, 6):
        rect(L, bx, 5, bx + 4, 10, stone)
    for bx in range(30, 104, 7):
        rect(L, bx, 25, bx + 4, 30, stone)
    dark = c("#120d0c")
    rect(L, 44, 74, 76, GROUND, dark)
    for y in range(64, 74):
        w = int(16 * math.sqrt(max(0, 1 - ((y - 74) / 10) ** 2)))
        rect(L, 60 - w, y, 60 + w, y + 1, dark)
    for gx in range(46, 76, 4):
        rect(L, gx, 64, gx + 1, 86 + (gx * 7) % 11, c("#3b3634"))
    for wx, wy in [(10, 26), (10, 52), (32, 44), (88, 44), (66, 40)]:
        rect(L, wx, wy, wx + 5, wy + 9, dark)
        EMIT.append((wx + 2.5, wy + 8, 3))
    for fx, fy, s in [(8, 5, 7), (40, 25, 5), (84, 25, 8), (22, 5, 5)]:
        EMIT.append((fx, fy, s))
    LIGHTS.extend([(16, 20, 75, c("#ff6a2a"), 1.0), (60, 45, 85, c("#ff7a30"), 0.9),
                   (86, 30, 65, c("#ff5520"), 0.8)])
    # ---- estandarte caído
    rect(L, 140, 100, 141, GROUND, c("#4a3a28"))
    for y in range(100, 110):
        rect(L, 141, y, 141 + (9 - (y - 100) // 2) - (y % 3), y + 1, c("#7a1a28"))
    # ---- santuário em ruínas
    pal, pdk = c("#8a877c"), c("#4a4841")
    for x0 in (216, 262):
        bricks(L, x0, 72, x0 + 11, GROUND, pal, pdk, 5, 5)
        rect(L, x0 - 2, 68, x0 + 13, 72, pal * 1.1)
        rect(L, x0 - 1, GROUND - 4, x0 + 12, GROUND, pal * 0.9)
        for ry in (82, 94):
            rect(L, x0 + 3, ry, x0 + 8, ry + 1, pdk)
            rect(L, x0 + 3, ry + 3, x0 + 8, ry + 4, pdk)
            rect(L, x0 + 3, ry, x0 + 4, ry + 4, pdk)
        rect(L, x0 + 1, 64, x0 + 10, 68, c("#3a3028"))
        EMIT.append((x0 + 5.5, 63, 6))
        LIGHTS.append((x0 + 5.5, 62, 80, c("#ffa040"), 1.1))
    bricks(L, 212, 56, 238, 62, pal, pdk, 6, 3)
    for fx, fy in [(250, 114), (254, 116), (247, 116)]:
        rect(L, fx, fy, fx + 4, fy + 3, pal * 0.8)
    st = c("#6f6d66")
    rect(L, 237, 106, 255, GROUND, st)
    rect(L, 241, 80, 251, 106, st)
    rect(L, 243, 71, 250, 80, st)
    rect(L, 236, 85, 243, 102, st * 0.8)
    rect(L, 252, 60, 253, 98, st * 0.9)
    for _ in range(50):
        px(L, rng.integers(235, 257), rng.integers(76, GROUND), c("#3c6a32"))
    # ---- carroça abandonada
    wood = c("#5a3f26")
    cx0 = 300
    rect(L, cx0, 100, cx0 + 30, 110, wood)
    for xx in range(cx0, cx0 + 30, 5):
        rect(L, xx, 100, xx + 1, 110, wood * 0.7)
    rect(L, cx0 + 30, 106, cx0 + 46, 107, wood)
    for a in range(0, 360, 10):
        if 200 < a < 280:
            continue
        r = math.radians(a)
        px(L, cx0 + 8 + 7 * math.cos(r), 111 + 7 * math.sin(r), wood * 0.8)
    rect(L, cx0 + 18, 113, cx0 + 27, GROUND, wood * 0.6)
    # ---- placa
    rect(L, 372, 92, 374, GROUND, wood)
    rect(L, 362, 93, 386, 98, wood * 1.2)
    rect(L, 364, 100, 381, 105, wood * 1.1)
    # ---- acampamento: estranho encapuzado, fogueira, barraca
    tent = c("#6b5a3a")
    for y in range(86, GROUND):
        w = (y - 86) * 0.9
        rect(L, CAMP + 52 - w, y, CAMP + 52 + w, y + 1, tent * (0.75 if y % 4 == 0 else 1))
    rect(L, CAMP + 49, 100, CAMP + 55, GROUND, c("#1c1510"))
    rect(L, CAMP + 14, GROUND - 2, CAMP + 30, GROUND, c("#3a2a1a"))
    EMIT.append((CAMP + 22, GROUND - 3, 9))
    LIGHTS.append((CAMP + 22, GROUND - 9, 95, c("#ffb050"), 1.3))
    cloak = c("#2c2e3a")
    rect(L, CAMP - 6, 100, CAMP + 7, GROUND, cloak)
    rect(L, CAMP - 4, 92, CAMP + 5, 101, cloak)
    rect(L, CAMP + 2, 95, CAMP + 5, 98, c("#1a1214"))
    return L


# ---------------------------------------------------------------- o rei (esqueleto)
KC = {k: tuple(int(v * 255) for v in c(h)) + (255,) for k, h in {
    "crown": "#f2c84b", "crownd": "#b88a2a", "gem": "#d0283a", "skin": "#d29a74",
    "hair": "#5a3a28", "eye": "#1a1010", "tunic": "#d8d0c0", "tunicd": "#a09684",
    "belt": "#6a4a1e", "cape": "#2b4fa8", "caped": "#18306e", "pants": "#3b3040",
    "boot": "#2a1e18", "torch": "#6b4a2a"}.items()}


def dim(col, f):
    return tuple(int(v * f) for v in col[:3]) + (255,)


def king_sprite(q, moving, t):
    """Desenha o rei (virado para a direita) em pixel de arte. q = fase da passada."""
    SW, SH = 48, 60
    im = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    TH, SHN = 9.0, 8.5                     # coxa, canela

    def leg(qq):
        if moving:
            a = math.radians(27 * math.sin(qq))
            flex = math.radians(6 + 50 * max(0.0, math.cos(qq)) ** 1.4)
        else:
            a, flex = math.radians(4 * math.sin(qq)), math.radians(4)
        kx, ky = TH * math.sin(a), TH * math.cos(a)
        sa = a - flex
        return (kx, ky), (kx + SHN * math.sin(sa), ky + SHN * math.cos(sa))

    legs = [leg(q), leg(q + math.pi)]       # [frente, trás]
    drop = max(f[1] for _, f in legs)
    hx, hy = 20.0, SH - 2 - drop            # quadril: pé mais baixo encosta no chão
    lean = math.radians(5)
    sx, sy = hx + 13 * math.sin(lean), hy - 13 * math.cos(lean)

    def P(o, p):
        return (o[0] + p[0], o[1] + p[1])

    def draw_leg(lg, f):
        (k, ft) = lg
        kn, fo = P((hx, hy), k), P((hx, hy), ft)
        d.line([(hx, hy), kn], fill=dim(KC["pants"], f), width=3)
        d.line([kn, fo], fill=dim(KC["pants"], f), width=3)
        mid = ((kn[0] + fo[0] * 2) / 3, (kn[1] + fo[1] * 2) / 3)
        d.line([mid, fo], fill=dim(KC["boot"], f), width=3)
        d.line([fo, (fo[0] + 3, fo[1])], fill=dim(KC["boot"], f), width=2)

    sw = math.sin(q) if moving else 0.15 * math.sin(t * 1.5)
    # braço de trás (balança oposto à perna da frente)
    ub = math.radians(-26 * sw)
    el = (sx - 1 + 6 * math.sin(ub), sy + 1 + 6 * math.cos(ub))
    fa = ub + math.radians(25)
    hd = (el[0] + 5.5 * math.sin(fa), el[1] + 5.5 * math.cos(fa))
    d.line([(sx - 1, sy + 1), el], fill=dim(KC["tunic"], 0.6), width=3)
    d.line([el, hd], fill=dim(KC["tunic"], 0.6), width=2)
    d.point([hd], fill=dim(KC["skin"], 0.6))
    draw_leg(legs[1], 0.62)
    # capa (atrás do corpo, ondulando)
    wv = math.sin(t * 5.0) * 1.2
    tr = 3 if moving else 1
    cape = [(sx + 1, sy - 1), (sx - 4, sy), (hx - 6 - tr + wv * 0.5, hy - 2),
            (hx - 7 - tr + wv, hy + 7), (hx - 3 - tr * 0.5 - wv * 0.5, hy + 9), (hx + 1, hy + 5)]
    d.polygon(cape, fill=KC["cape"])
    d.line([(sx - 3, sy + 2), (hx - 5 - tr + wv * 0.7, hy + 6)], fill=KC["caped"], width=1)
    d.line([cape[2], cape[3]], fill=KC["caped"], width=1)
    draw_leg(legs[0], 1.0)
    # tronco e túnica
    torso = [(sx - 3, sy), (sx + 3, sy), (hx + 4, hy + 1), (hx + 4, hy + 5), (hx - 4, hy + 5), (hx - 4, hy + 1)]
    d.polygon(torso, fill=KC["tunic"])
    d.line([(hx - 3, hy + 4), (hx + 3, hy + 4)], fill=KC["tunicd"], width=1)
    d.line([(sx - 2, sy + 1), (hx - 3, hy)], fill=KC["tunicd"], width=1)
    d.line([(hx - 4, hy - 1), (hx + 4, hy - 1)], fill=KC["belt"], width=2)
    d.point([(hx + 1, hy - 1)], fill=KC["crown"])
    # cabeça
    nx, ny = sx + 1, sy - 1
    d.rectangle([nx - 2, ny - 6, nx + 3, ny], fill=KC["skin"])
    d.rectangle([nx - 2, ny - 6, nx - 1, ny - 1], fill=KC["hair"])          # cabelo atrás
    d.rectangle([nx - 2, ny - 6, nx + 3, ny - 6], fill=KC["hair"])
    d.rectangle([nx, ny - 1, nx + 3, ny], fill=KC["hair"])                  # barba
    d.point([(nx + 2, ny - 4)], fill=KC["eye"])
    d.rectangle([nx - 2, ny - 8, nx + 3, ny - 7], fill=KC["crown"])        # coroa
    d.point([(nx - 2, ny - 9), (nx + 1, ny - 9), (nx + 3, ny - 9)], fill=KC["crown"])
    d.point([(nx + 1, ny - 7)], fill=KC["gem"])
    d.line([(nx - 2, ny - 7), (nx + 3, ny - 7)], fill=KC["crownd"], width=1)
    # braço da frente segurando a tocha
    bob = 0.5 * math.sin(2 * q) if moving else 0
    sh = (sx + 1, sy + 1)
    el = (sh[0] + 3, sh[1] + 5 + bob)
    hd = (el[0] + 4, el[1] - 2 + bob)
    d.line([sh, el], fill=KC["tunic"], width=3)
    d.line([el, hd], fill=KC["tunic"], width=2)
    tip = (hd[0] + 2, hd[1] - 7)
    d.line([(hd[0] - 0.5, hd[1] + 2), tip], fill=KC["torch"], width=1)
    d.point([hd], fill=KC["skin"])
    arr = np.asarray(im).astype(np.float32) / 255
    return arr, hx, tip


# ---------------------------------------------------------------- desenho em sub-pixel
def block(img, fx, fy, col, alpha=1.0):
    """Um pixel de arte (SxS) numa posição fina qualquer."""
    fx, fy = int(round(fx)), int(round(fy))
    if -S < fx < FW and -S < fy < FH:
        y0, y1, x0, x1 = max(0, fy), min(FH, fy + S), max(0, fx), min(FW, fx + S)
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - alpha) + col * alpha


FIRE = [c("#fff4b0"), c("#ffc63a"), c("#f07a1e"), c("#b8321a")]
FIRE_HZ = 9           # o fogo muda de forma 9x por segundo (antes: a cada quadro)


def fire(img, ax, ay, s, t, seed):
    """Chama em coordenadas de arte (float) -> grade fina."""
    step = int(t * FIRE_HZ)
    u = t * FIRE_HZ - step
    ra = np.random.default_rng(step * 131 + seed)
    rb = np.random.default_rng((step + 1) * 131 + seed)
    for i in range(-(s // 2), s - s // 2):
        hmax = s * (1.6 - abs(i) / max(1, s) * 1.6)
        ha, hb = hmax * ra.uniform(0.5, 1.1), hmax * rb.uniform(0.5, 1.1)
        h = int(max(1, ha * (1 - u) + hb * u))       # interpola entre formas
        for k in range(h):
            block(img, (ax + i) * S, (ay - k) * S, FIRE[min(3, int(k / h * 4))])


# ---------------------------------------------------------------- texto
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CAPTIONS = [(0.6, 4.2, "O castelo caiu."),
            (4.8, 8.6, "Expulso do próprio reino,"),
            (9.2, 12.8, "o rei vaga pela floresta..."),
            (13.4, 16.0, "...em busca de um novo lar.")]


def text_mask(txt, size, cy):
    im = Image.new("L", (FW, FH), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    f = ImageFont.truetype(FONT, size)
    d.text(((FW - d.textlength(txt, font=f)) / 2, cy), txt, font=f, fill=255)
    m = np.array(im) > 127
    o = m.copy()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1), (0, 2)]:
        o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return m, o


TXT = [(a, b, text_mask(s, 24, 40)) for a, b, s in CAPTIONS]
TITLE = text_mask("O REI EXILADO", 56, 200)
SUB = text_mask("capítulo I", 22, 270)

# ---------------------------------------------------------------- lago
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16
BAY = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:BANK, :W]
YY, XX = np.mgrid[0:BANK, 0:W].astype(np.float32)
AMBIENT = c("#4a5878") * 0.85
STREAKS = [(rng.uniform(0, 900), rng.integers(BANK + 2, H), rng.integers(3, 10), rng.uniform(3, 7))
           for _ in range(110)]
LEAVES = [(rng.uniform(0, 900), rng.integers(BANK + 6, H - 4), rng.uniform(4, 8)) for _ in range(9)]


def fish_jumps():
    out, t = [], 1.6
    r = np.random.default_rng(3)
    while t < DUR - 1.5:
        out.append((t, king_x(t) + r.uniform(30, 160), r.uniform(144, 168), r.choice([-1, 1])))
        t += r.uniform(1.8, 3.0)
    return out


JUMPS = fish_jumps()
JUMP_T = 0.85


def draw_water_life(img, t, cam):
    # correnteza: riscos de luz que escorrem para a esquerda; os de perto andam mais rápido
    for wx, row, ln, spd in STREAKS:
        depth = 1 + (row - BANK) / (H - BANK) * 0.35
        sx = ((wx - cam * depth - t * spd) % (W + 60)) - 30
        a = 0.25 + 0.2 * math.sin(t * 1.7 + wx)
        if a > 0.15:
            x0, x1 = int(max(0, sx * S)), int(min(FW, (sx + ln) * S))
            if x0 < x1:
                img[row * S:row * S + S, x0:x1] += c("#3c4c58") * a
    # folhas boiando
    for wx, row, spd in LEAVES:
        sx = ((wx - cam * 1.1 - t * spd) % (W + 40)) - 20
        bob = 0.4 * math.sin(t * 2 + wx)
        for i, col in enumerate((c("#4a5a2a"), c("#6a6a30"), c("#4a5a2a"))):
            block(img, (sx + i) * S, (row + bob) * S, col * 0.7)
    # peixes
    for t0, wx, wy, dr in JUMPS:
        age = t - t0
        if -0.1 < age < JUMP_T + 1.0:
            sx = wx - cam
            for ring_t, rx in ((age, sx), (age - JUMP_T, sx + dr * 16)):
                if 0 < ring_t < 1.0:                           # anéis na água
                    rr = 2 + ring_t * 13
                    al = (1 - ring_t) * 0.8
                    for ang in np.linspace(0, 2 * math.pi, int(10 + rr * 3), endpoint=False):
                        block(img, (rx + rr * math.cos(ang)) * S, (wy + rr * 0.22 * math.sin(ang)) * S,
                              c("#9ab0bc"), al)
            if 0 <= age <= JUMP_T:
                u = age / JUMP_T
                fx, fy = sx + dr * 16 * u, wy - 13 * math.sin(math.pi * u)
                vx, vy = dr * 16, -13 * math.pi * math.cos(math.pi * u)
                n = math.hypot(vx, vy)
                ux, uy = vx / n, vy / n
                for i in range(-3, 4):                         # corpo segue a direção do salto
                    col = c("#b8c8d0") if i > -2 else c("#7a8c96")
                    block(img, (fx + ux * i) * S, (fy + uy * i) * S, col)
                    if -2 < i < 3:
                        block(img, (fx + ux * i - uy) * S, (fy + uy * i + ux * 0.6) * S, c("#5a6c78"))
                tx, ty = fx - ux * 4, fy - uy * 4               # cauda
                block(img, (tx - uy) * S, (ty + ux) * S, c("#7a8c96"))
                block(img, (tx + uy) * S, (ty - ux) * S, c("#7a8c96"))
                if u < 0.35 or u > 0.65:                       # gotas
                    for k in range(3):
                        block(img, (fx - ux * 2 + (k - 1) * 2) * S, (fy + 2 + k % 2) * S, c("#c8dce4"), 0.7)


# ---------------------------------------------------------------- render
def up3(a):
    return a.repeat(S, 0).repeat(S, 1)


def main():
    sky = up3(build_sky())
    layers = [(build_far(), 0.12, 0.12), (build_far2(), 0.28, 0.3), (build_mid(), 0.5, 0.45),
              (build_bush(), 0.78, 0.8), (build_ground(), 1.0, 1.0)]
    front = up3(build_front())
    layers = [(up3(L), f, wv) for L, f, wv in layers]
    flies = [(rng.uniform(0, 700), rng.uniform(55, 115), rng.uniform(0, 6.28)) for _ in range(36)]

    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{FW * UP}x{FH * UP}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", OUT],
                          stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for fi in range(n):
        t = fi / FPS
        cam = cam_x(t)
        img = sky.copy()
        wgt = np.full((FH, FW), 0.1, np.float32)

        def over(L, f, wv):
            nonlocal img, wgt
            o = int(round(cam * f * S))
            cr = L[:, o:o + FW]
            a = cr[..., 3:4]
            img = img * (1 - a) + cr[..., :3] * a
            wgt = np.where(a[..., 0] > 0, wv, wgt)

        for L, f, wv in layers:
            over(L, f, wv)

        # ---- rei
        kx = king_x(t)
        moving = t < WALK_END - 0.05
        q = 2 * math.pi * (kx - 60) / 30.0
        spr, hx, tip = king_sprite(q, moving, t)
        sp = up3(spr)
        ox = int(round((kx - cam - hx) * S))
        oy = (GROUND + 1) * S - sp.shape[0]
        x0, x1 = max(0, ox), min(FW, ox + sp.shape[1])
        a = sp[:, x0 - ox:x1 - ox, 3:4]
        img[oy:oy + sp.shape[0], x0:x1] = img[oy:oy + sp.shape[0], x0:x1] * (1 - a) + sp[:, x0 - ox:x1 - ox, :3] * a
        wgt[oy:oy + sp.shape[0], x0:x1] = np.where(a[..., 0] > 0, 1.0, wgt[oy:oy + sp.shape[0], x0:x1])
        tax = kx - cam - hx + tip[0]                               # ponta da tocha (arte)
        tay = GROUND + 1 - spr.shape[0] + tip[1]
        over(front, 1.2, 0.9)

        # ---- luz
        fl = 1 + 0.06 * math.sin(t * 9) + 0.04 * math.sin(t * 15.3)
        lights = [(tax, tay, 95 * fl, c("#ffb060"), 1.35)]
        for lx, ly, r, col, inten in LIGHTS:
            sx = lx - cam
            if -r < sx < W + r:
                lights.append((sx, ly, r * (1 + 0.05 * math.sin(t * 6 + lx)), col, inten))
        Lm = np.zeros((BANK, W, 3), np.float32)
        for sx, sy, r, col, inten in lights:
            dd = np.sqrt((XX - sx) ** 2 + ((YY - sy) * 1.15) ** 2)
            fall = np.clip(1 - dd / r, 0, 1) ** 1.6
            Lm += (np.floor(fall * 5 + BAY) / 5)[..., None] * col * inten
        dawn = max(0, (t - 12) / 6) * 0.25
        img[:BANK * S] *= AMBIENT * (1 + dawn) + wgt[:BANK * S, :, None] * up3(Lm)

        # ---- emissivos
        for k, (ex, ey, s) in enumerate(EMIT):
            if -10 < ex - cam < W + 10:
                fire(img, ex - cam, ey, s, t, k)
        fire(img, tax, tay - 0.5, 3, t, 99)
        r2 = np.random.default_rng(int(t * 12))
        if cam < 130:                                              # brasas
            for _ in range(16):
                base, rise = r2.uniform(0, 104), r2.uniform(0, 1)
                ey = 30 - rise * 30 - (t * 12 % 1) * 3
                block(img, (base - cam + math.sin(rise * 6) * 2) * S, ey * S, FIRE[r2.integers(1, 3)])
        for fx, fy, ph in flies:                                   # vaga-lumes
            sx = fx - cam * 0.9 + 6 * math.sin(t * 0.8 + ph)
            sy = fy + 4 * math.sin(t * 1.3 + ph * 2)
            if 1 <= sx < W - 1 and 1 <= sy < BANK - 1 and math.sin(t * 2 + ph * 3) > -0.3:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    block(img, (sx + dx) * S, (sy + dy) * S, c("#9ab84a"), 0.5)
                block(img, sx * S, sy * S, c("#e8ff9a"))

        # ---- lago: reflexo ondulado que corre
        B = BANK * S
        for k in range(FH - B):
            kk = k / S
            off = int(round(math.sin(kk * 0.8 + t * 2.2) * (0.6 + kk * 0.1) * S
                            + math.sin(kk * 0.23 - t * 1.1) * S))
            img[B + k] = np.roll(img[B - 1 - k], off, 0) * c("#4a6478") * (0.75 - kk * 0.006)
        img[B:B + S] *= 0.4
        draw_water_life(img, t, cam)

        # ---- fade, texto, saída
        fade = min(1, t / 1.0) * min(1, (DUR - t) / 1.2)
        out = np.clip(img * fade, 0, 1)

        def put(mask, al):
            m, o = mask
            out[o] = out[o] * (1 - al) + np.array([20, 14, 12]) / 255 * al
            out[m] = out[m] * (1 - al) + np.array([240, 228, 196]) / 255 * al
        for a0, b0, mk in TXT:
            if a0 <= t <= b0:
                put(mk, min(1, (t - a0) / 0.4, (b0 - t) / 0.4))
        if t > 15.8:
            al = min(1, (t - 15.8) / 0.8, (DUR - t) / 0.6)
            put(TITLE, al)
            put(SUB, al)
        big = (out * 255).astype(np.uint8).repeat(UP, 0).repeat(UP, 1)
        ff.stdin.write(big.tobytes())
        if fi in (60, 230, 420, 500):
            Image.fromarray(big).save(OUT.replace(".mp4", f"_f{fi:03d}.png"))
    ff.stdin.close()
    ff.wait()
    print("ok", OUT)


if __name__ == "__main__":
    main()
