"""O Rei Exilado — capítulo 2: o encapuzado (25s). Resultado da votação do cap. 1: B.

Reaproveita cenário, rei, cavalo, fogo e lago de rei_exilado.py.
O encapuzado acorda na fogueira, guia o rei a pé com uma lanterna de luz azul,
passando por pedras com runas e túmulos, até um portal em ruínas onde está o
estandarte do lobo, de quem tomou o castelo.

Uso: python3 rei_exilado/cap2.py  ->  rei_exilado/cap2.mp4
"""
import importlib.util
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r", os.path.join(HERE, "rei_exilado.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
c, S, W, H, FW, FH, UP, FPS = r.c, r.S, r.W, r.H, r.FW, r.FH, r.UP, r.FPS
GROUND, BANK, block, up3 = r.GROUND, r.BANK, r.block, r.up3
DUR = 25.0
OUT = os.path.join(HERE, "cap2.mp4")
rng = np.random.default_rng(21)

# ---------------------------------------------------------------- roteiro de movimento
HX0 = 60                  # cavalo com o rei, parado na fogueira
SX0 = 108                 # encapuzado sentado/parado
RUIN = 640                # portal em ruínas
SSTOP = RUIN - 30
WAKE, GO, STOP = 3.0, 5.0, 20.8
REVEAL = 20.6
CARD_T = 22.2


def trap(t, t0, t1, x0, x1, acc=1.2, dec=1.6):
    if t <= t0:
        return x0
    T, TT = min(t, t1) - t0, t1 - t0
    v = (x1 - x0) / (TT - (acc + dec) / 2)
    if T < acc:
        return x0 + v * T * T / (2 * acc)
    d1 = v * acc / 2
    if T < TT - dec:
        return x0 + d1 + v * (T - acc)
    u = T - (TT - dec)
    return x0 + d1 + v * (TT - dec - acc) + v * (u - u * u / (2 * dec))


def stranger_x(t):
    return trap(t, GO, STOP, SX0, SSTOP)


def horse_x(t):
    return trap(t, GO + 0.8, STOP + 0.6, HX0, SSTOP - 52)


def focus_x(t):
    return (horse_x(t) + stranger_x(t)) / 2


def cam_x(t):
    x = focus_x(t) - 150
    if x > 10:
        return x
    return (x + 10) ** 2 / 40 if x > -10 else 0.0


r.MAXCAM = int(focus_x(DUR) - 150) + 6

# ---------------------------------------------------------------- cenário do cap. 2
EMIT, LIGHTS, RUNES = [], [], []      # RUNES: (x, y, peso no clímax)


def build_ground2():
    L = r.layer(r.lw(1.0))
    Wl = L.shape[1]
    r.bricks(L, 0, GROUND + 1, Wl, BANK, c("#3e3a33"), c("#211d19"), 7, 4)
    g = [c("#1f3a1c"), c("#2f5526"), c("#46742f")]
    r.rect(L, 0, GROUND - 1, Wl, GROUND + 2, g[1])
    for x in range(Wl):
        for k in range(rng.integers(0, 4)):
            r.px(L, x, GROUND - 1 - k, g[min(2, k)])
    # acampamento (mesmo do cap. 1)
    tent = c("#6b5a3a")
    for y in range(86, GROUND):
        w = (y - 86) * 0.9
        r.rect(L, SX0 + 44 - w, y, SX0 + 44 + w, y + 1, tent * (0.75 if y % 4 == 0 else 1))
    r.rect(L, SX0 + 41, 100, SX0 + 47, GROUND, c("#1c1510"))
    r.rect(L, SX0 + 12, GROUND - 2, SX0 + 26, GROUND, c("#3a2a1a"))
    EMIT.append((SX0 + 19, GROUND - 3, 8))
    LIGHTS.append((SX0 + 19, GROUND - 9, 90, c("#ffb050"), 1.2))
    # pedras eretas com runas
    st = c("#5e5c58")
    for x0, h in [(225, 26), (246, 34), (300, 30), (318, 22)]:
        r.rect(L, x0, GROUND - h, x0 + 8, GROUND, st)
        r.rect(L, x0 + 1, GROUND - h - 2, x0 + 7, GROUND - h, st * 0.9)
        for _ in range(25):
            r.px(L, x0 + rng.integers(0, 8), GROUND - rng.integers(0, h), c("#3c6a32"))
        for k in range(2):
            RUNES.append((x0 + 4, GROUND - h + 6 + k * 8, 0.0))
    # túmulos e cruzes tortas
    wood = c("#4a3a28")
    for i, x0 in enumerate(range(372, 440, 16)):
        lean = (i % 3) - 1
        r.rect(L, x0, GROUND - 14, x0 + 2, GROUND, wood)
        for k in range(6):
            r.px(L, x0 - 3 + k, GROUND - 10 + (lean * k) // 3, wood)
        r.rect(L, x0 - 4, GROUND - 2, x0 + 6, GROUND, c("#3a3024"))
    # estátua sem cabeça
    r.rect(L, 476, 92, 486, GROUND, c("#6f6d66"))
    r.rect(L, 472, GROUND - 6, 490, GROUND, c("#6f6d66") * 0.85)
    r.rect(L, 486, 96, 491, 100, c("#6f6d66"))
    r.rect(L, 493, GROUND - 4, 498, GROUND, c("#6f6d66") * 0.8)          # a cabeça caída
    # muro antigo
    r.bricks(L, 535, 96, 575, GROUND, c("#4e4c50"), c("#262428"), 6, 3)
    for k in range(20):
        r.rect(L, 535 + k * 2, 90 + (k * 7) % 8, 537 + k * 2, 96, c("#4e4c50"))
    # portal em ruínas
    pal, pdk = c("#7a776e"), c("#3e3c36")
    for x0 in (RUIN, RUIN + 52):
        r.bricks(L, x0, 50, x0 + 14, GROUND, pal, pdk, 7, 5)
        r.rect(L, x0 - 2, GROUND - 5, x0 + 16, GROUND, pal * 0.85)
        for k in range(5):
            RUNES.append((x0 + 7, 60 + k * 11, 1.0))
    r.bricks(L, RUIN - 4, 42, RUIN + 70, 50, pal * 1.05, pdk, 8, 4)
    for k in range(8):                                                   # lintel partido
        r.rect(L, RUIN + 50 + k * 3, 36 + (k * 5) % 6, RUIN + 53 + k * 3, 42, pal)
    r.rect(L, RUIN + 14, 50, RUIN + 52, GROUND, c("#0b0d12"))             # escuridão do portal
    RUNES.append((RUIN + 33, 46, 1.0))
    # estandarte do usurpador: lobo prateado sobre negro
    BX = RUIN + 26
    r.rect(L, BX, 58, BX + 1, GROUND, c("#4a3a28"))
    r.rect(L, BX + 1, 60, BX + 14, 82, c("#16141a"))
    for k in range(4):
        r.rect(L, BX + 1 + k * 3, 82, BX + 3 + k * 3, 84 + (k % 2) * 2, c("#16141a"))
    wolf = ["..#....#.", "..##..##.", "..######.", ".##.##.#.", ".#######.", "..#####..", "...###...", "....#...."]
    for j, row in enumerate(wolf):
        for i, ch in enumerate(row):
            if ch == "#":
                r.px(L, BX + 3 + i, 64 + j, c("#b8bcc4"))
    for _ in range(80):
        r.px(L, RUIN + rng.integers(-2, 68), rng.integers(44, GROUND), c("#3c6a32"))
    return L


# ---------------------------------------------------------------- o encapuzado
def hooded_sprite(q, moving, t, raise_u=0.0):
    SW, SH = 40, 56
    im = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    TH, SHN = 8.5, 8.0

    def leg(qq):
        if moving:
            a = math.radians(25 * math.sin(qq))
            flex = math.radians(6 + 45 * max(0.0, math.cos(qq)) ** 1.4)
        else:
            a, flex = math.radians(4 * math.sin(qq)), math.radians(4)
        kx, ky = TH * math.sin(a), TH * math.cos(a)
        return (kx, ky), (kx + SHN * math.sin(a - flex), ky + SHN * math.cos(a - flex))

    legs = [leg(q), leg(q + math.pi)]
    hx, hy = 18.0, SH - 2 - max(f[1] for _, f in legs)
    sx, sy = hx + 1.5, hy - 13
    cloak, cloakd, pants = (44, 46, 58, 255), (30, 31, 42, 255), (28, 24, 30, 255)
    for (k, f), dimf in ((legs[1], 0.7), (legs[0], 1.0)):
        col = tuple(int(v * dimf) for v in pants[:3]) + (255,)
        kn, fo = (hx + k[0], hy + k[1]), (hx + f[0], hy + f[1])
        d.line([(hx, hy), kn], fill=col, width=3)
        d.line([kn, fo], fill=col, width=3)
        d.line([fo, (fo[0] + 2.5, fo[1])], fill=(20, 16, 14, 255), width=2)
    wv = math.sin(t * 4.0) * (1.4 if moving else 0.6)
    d.polygon([(sx - 3, sy - 1), (sx + 3, sy - 1), (hx + 5, hy + 6), (hx + 2, hy + 9),
               (hx - 4, hy + 9), (hx - 7 - wv, hy + 8)], fill=cloak)
    d.line([(sx - 1, sy + 1), (hx - 3 - wv * 0.5, hy + 8)], fill=cloakd, width=1)
    d.line([(sx + 1, sy + 2), (hx + 1, hy + 8)], fill=cloakd, width=1)
    d.ellipse([sx - 3, sy - 10, sx + 4, sy + 1], fill=cloakd)                 # capuz
    d.polygon([(sx - 3, sy - 6), (sx - 6, sy - 3), (sx - 2, sy - 1)], fill=cloakd)
    d.rectangle([sx + 1, sy - 6, sx + 3, sy - 2], fill=(10, 8, 12, 255))       # rosto na sombra
    eye = (sx + 2.5, sy - 4.5)
    # braço com a lanterna (sobe no clímax)
    sh = (sx + 1, sy + 1)
    bob = 0.5 * math.sin(2 * q) if moving else 0
    hand = (sh[0] + 5 + 2 * raise_u, sh[1] + 6 - 13 * raise_u + bob)
    el = (sh[0] + 2 + raise_u, sh[1] + 5 - 4 * raise_u)
    d.line([sh, el, hand], fill=cloak, width=2)
    d.line([hand, (hand[0], hand[1] + 1)], fill=(60, 56, 50, 255), width=1)
    d.rectangle([hand[0] - 1, hand[1] + 1, hand[0] + 1, hand[1] + 4], fill=(40, 36, 32, 255))
    lamp = (hand[0], hand[1] + 2.5)
    arr = np.asarray(im).astype(np.float32) / 255
    return arr, hx, lamp, eye


def flip(spr, hx, *pts):
    w = spr.shape[1]
    return (spr[:, ::-1], w - 1 - hx) + tuple((w - 1 - p[0], p[1]) for p in pts)


# ---------------------------------------------------------------- textos
TM = r.text_mask
INTRO1 = [TM("VOCÊS ESCOLHERAM:  B", 44, 175), TM("cada comentário decide a série", 24, 248)]
INTRO2 = [TM("O REI EXILADO", 56, 175), TM("capítulo 2  -  o encapuzado", 24, 250)]
CARD = [TM("COMENTE  A  ou  B", 46, 150),
        TM("A  -  Confiar no encapuzado", 26, 232),
        TM("B  -  Fugir dele durante a noite", 26, 278),
        TM("os comentários decidem o capítulo 3", 18, 336)]
CYAN = c("#8fe6ff")


def jumps():
    out, t = [], 2.0
    g = np.random.default_rng(9)
    while t < DUR - 1.5:
        out.append((t, focus_x(t) + g.uniform(-60, 140), g.uniform(144, 168), g.choice([-1, 1])))
        t += g.uniform(2.0, 3.2)
    return out


r.JUMPS = jumps()


# ---------------------------------------------------------------- render
def main():
    sky = up3(r.build_sky())
    layers = [(r.build_far(), 0.12, 0.12), (r.build_far2(), 0.28, 0.3), (r.build_mid(), 0.5, 0.45),
              (r.build_bush(), 0.78, 0.8), (build_ground2(), 1.0, 1.0)]
    r.FAR_EMIT.clear()                       # a vila do cap. 1 fica para trás
    front = up3(r.build_front())
    layers = [(up3(L), f, wv) for L, f, wv in layers]
    flies = [(rng.uniform(0, 650), rng.uniform(55, 115), rng.uniform(0, 6.28)) for _ in range(36)]

    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{FW * UP}x{FH * UP}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", OUT],
                          stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
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

        def paste(spr, ax, ay):
            sp = up3(spr)
            ox, oy = int(round(ax * S)), int(round(ay * S))
            x0, x1 = max(0, ox), min(FW, ox + sp.shape[1])
            if x0 >= x1:
                return
            a = sp[:, x0 - ox:x1 - ox, 3:4]
            sl = (slice(oy, oy + sp.shape[0]), slice(x0, x1))
            img[sl] = img[sl] * (1 - a) + sp[:, x0 - ox:x1 - ox, :3] * a
            wgt[sl] = np.where(a[..., 0] > 0, 1.0, wgt[sl])

        for L, f, wv in layers:
            over(L, f, wv)

        # ---- encapuzado: parado olhando o rei, vira e guia
        sxw = stranger_x(t)
        smov = GO + 0.05 < t < STOP - 0.05
        ru = min(1.0, max(0.0, (t - REVEAL) / 0.8))
        sspr, shx, lamp, eye = hooded_sprite(2 * math.pi * (sxw - SX0) / 28.0, smov, t, ru)
        if t < GO - 0.3:
            sspr, shx, lamp, eye = flip(sspr, shx, lamp, eye)
        stop_ = GROUND + 1 - sspr.shape[0]
        sleft = sxw - shx
        paste(sspr, sleft - cam, stop_)

        # ---- cavalo e rei montado
        hxw = horse_x(t)
        hmov = GO + 0.85 < t < STOP + 0.55
        hq = 2 * math.pi * (hxw - HX0) / 36.0
        hspr, hax, saddle = r.horse_sprite(hq, hmov, 0.0, t)
        htop = GROUND + 1 - hspr.shape[0]
        paste(hspr, hxw - cam - hax, htop)
        kspr, khx, khy, tip = r.king_sprite(hq, True, t, ride=True)
        kl = hxw - hax + saddle[0] - khx
        kt = htop + saddle[1] + 1 - khy
        paste(kspr, kl - cam, kt)
        tax, tay = kl - cam + tip[0], kt + tip[1]
        over(front, 1.2, 0.9)

        # ---- luz: tocha quente do rei, lanterna fria do encapuzado, runas
        lit = min(1.0, max(0.0, (t - 1.0) / 2.0))                 # lanterna acende ao acordar
        glow = 0.35 + 0.65 * ru
        fl = 1 + 0.06 * math.sin(t * 9) + 0.04 * math.sin(t * 15.3)
        lx, ly = sleft - cam + lamp[0], stop_ + lamp[1]
        lights = [(tax, tay, 95 * fl, c("#ffb060"), 1.3),
                  (lx, ly, 75 * (1 + 0.5 * ru), CYAN, 0.9 * lit * (1 + 0.6 * ru))]
        for ex, ey, rr, col, inten in LIGHTS:
            if -rr < ex - cam < W + rr:
                lights.append((ex - cam, ey, rr * (1 + 0.05 * math.sin(t * 6 + ex)), col, inten))
        for k, (rx, ry, wgt_r) in enumerate(RUNES[::2]):
            pul = 0.5 + 0.5 * math.sin(t * 2 + k)
            if -40 < rx - cam < W + 40:
                lights.append((rx - cam, ry, 32 + 30 * wgt_r * ru, CYAN, (0.25 + 0.5 * wgt_r * glow) * (0.7 + 0.3 * pul)))
        Lm = np.zeros((BANK, W, 3), np.float32)
        for lsx, lsy, rr, col, inten in lights:
            dd = np.sqrt((r.XX - lsx) ** 2 + ((r.YY - lsy) * 1.15) ** 2)
            fall = np.clip(1 - dd / rr, 0, 1) ** 1.6
            Lm += (np.floor(fall * 5 + r.BAY) / 5)[..., None] * col * inten
        img[:BANK * S] *= r.AMBIENT * 0.92 + wgt[:BANK * S, :, None] * up3(Lm)

        # ---- emissivos
        for k, (ex, ey, s) in enumerate(EMIT):
            if -10 < ex - cam < W + 10:
                r.fire(img, ex - cam, ey, s, t, k)
        r.fire(img, tax, tay - 0.5, 3, t, 99)
        if lit > 0:
            block(img, lx * S, ly * S, c("#e8fbff"), lit)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                block(img, (lx + dx) * S, (ly + dy) * S, CYAN, 0.6 * lit)
        eg = 0.55 + 0.45 * math.sin(t * 3)
        block(img, (sleft - cam + eye[0]) * S, (stop_ + eye[1]) * S, c("#c8f0ff"), eg)
        for k, (rx, ry, wgt_r) in enumerate(RUNES):
            a = (0.45 + 0.35 * math.sin(t * 2.2 + k * 0.9)) * (0.6 + 0.4 * wgt_r * glow + 0.4 * ru)
            block(img, (rx - cam) * S, ry * S, CYAN, min(1, a))
            block(img, (rx - cam) * S, (ry + 1) * S, CYAN * 0.7, min(1, a * 0.7))
        for fx, fy, ph in flies:
            fsx = fx - cam * 0.9 + 6 * math.sin(t * 0.8 + ph)
            fsy = fy + 4 * math.sin(t * 1.3 + ph * 2)
            if 1 <= fsx < W - 1 and 1 <= fsy < BANK - 1 and math.sin(t * 2 + ph * 3) > -0.3:
                block(img, fsx * S, fsy * S, c("#e8ff9a"))

        # ---- lago
        B = BANK * S
        for k in range(FH - B):
            kk = k / S
            off = int(round(math.sin(kk * 0.8 + t * 2.2) * (0.6 + kk * 0.1) * S
                            + math.sin(kk * 0.23 - t * 1.1) * S))
            img[B + k] = np.roll(img[B - 1 - k], off, 0) * c("#4a6478") * (0.75 - kk * 0.006)
        img[B:B + S] *= 0.4
        r.draw_water_life(img, t, cam)

        # ---- textos
        out = np.clip(img * min(1, t / 0.8), 0, 1)

        def put(mask, al):
            m, o = mask
            out[o] = out[o] * (1 - al) + np.array([20, 14, 12]) / 255 * al
            out[m] = out[m] * (1 - al) + np.array([240, 228, 196]) / 255 * al

        for t0, t1, masks in ((0.3, 2.9, INTRO1), (3.1, 5.6, INTRO2)):
            if t0 < t < t1:
                al = min(1, (t - t0) / 0.5, (t1 - t) / 0.5)
                out[120:310] *= 1 - 0.4 * al
                for mk in masks:
                    put(mk, al)
        if t > CARD_T:
            al = min(1, (t - CARD_T) / 0.6)
            out[100:380] *= 1 - 0.55 * al
            for i, mk in enumerate(CARD):
                put(mk, max(0, min(1, (t - CARD_T - i * 0.35) / 0.5)))
        big = (out * 255).astype(np.uint8).repeat(UP, 0).repeat(UP, 1)
        ff.stdin.write(big.tobytes())
        if fi in (45, 200, 380, 560, 640, 740):
            Image.fromarray(big).save(OUT.replace(".mp4", f"_f{fi:03d}.png"))
    ff.stdin.close()
    ff.wait()
    print("ok", OUT)


if __name__ == "__main__":
    main()
