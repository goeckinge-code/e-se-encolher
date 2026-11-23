"""Foto de perfil 1080x1080: busto do rei com a tocha, no estilo do vídeo."""
import importlib.util, math, os
import numpy as np
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r", os.path.join(here, "rei_exilado.py"))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

N, K = 120, 2                        # canvas em pixel de arte; zoom do rei
rng = np.random.default_rng(5)
img = np.zeros((N, N, 3), np.float32)
for y in range(N):
    u = y / N
    img[y] = r.c("#0c1a1e") * (1 - u) + r.c("#1c3238") * u
L = np.zeros((N, N, 4), np.float32)   # floresta ao fundo
for x in range(-6, N + 6, 11):
    r.rect(L, x, 30, x + rng.integers(3, 6), N, r.c("#16262a"))
for x in range(-10, N + 10, 13):
    r.blob(L, x, rng.integers(-2, 26), rng.integers(12, 18), [r.c("#0f1d18"), r.c("#16291f"), r.c("#1e3628")])
a = L[..., 3:]
img = img * (1 - a) + L[..., :3] * a

spr, hx, hy, tip = r.king_sprite(0, False, 0.3)
K = 3
spr = spr.repeat(K, 0).repeat(K, 1)
ys, xs = np.nonzero(spr[..., 3] > 0)
ox = int(N / 2 - (hx + 2) * K)        # centraliza a cabeça/tronco no círculo
oy = 20 - ys.min()                    # coroa perto do topo
for y in range(spr.shape[0]):
    for x in range(spr.shape[1]):
        Y, X = oy + y, ox + x
        if 0 <= Y < N and 0 <= X < N and spr[y, x, 3] > 0:
            img[Y, X] = spr[y, x, :3]
tx, ty = ox + tip[0] * K, oy + tip[1] * K

# luz da tocha quantizada com dither + ambiente frio
B = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16
BAY = np.tile(B, (N // 4, N // 4))
YY, XX = np.mgrid[0:N, 0:N]
fall = np.clip(1 - np.hypot(XX - tx, YY - ty) / 95, 0, 1) ** 1.4
img *= r.c("#4a5878") * 0.9 + (np.floor(fall * 5 + BAY) / 5)[..., None] * r.c("#ffb060") * 1.3

# chama da tocha (maior, em blocos de 2)
fire = [r.c("#fff4b0"), r.c("#ffc63a"), r.c("#f07a1e"), r.c("#b8321a")]
for i, hh in zip(range(-4, 5), (2, 5, 9, 13, 16, 12, 8, 4, 2)):
    for k in range(hh):
        x, y = int(tx + i), int(ty - 1 - k)
        if 0 <= x < N and 0 <= y < N:
            img[y, x] = fire[min(3, int(k / hh * 4))]
for _ in range(18):                   # brasas e vaga-lumes
    x, y = rng.integers(0, N), rng.integers(0, N - 10)
    img[y, x] = fire[1] if rng.random() < 0.5 else r.c("#e8ff9a")

out = (np.clip(img, 0, 1) * 255).astype(np.uint8).repeat(9, 0).repeat(9, 1)
Image.fromarray(out).save(os.path.join(here, "perfil_rei.png"))
print("ok")
