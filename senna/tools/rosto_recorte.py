"""Recorte do retrato (céu azul) com bordas de cabelo limpas.

Uso: python3 rosto_recorte.py original.jpg foto_hd.png saida.webp [largura]
1. estima a cor do céu atrás de cada pixel (convolução normalizada a partir do céu certo);
2. alfa = diferença entre a foto e esse céu, refinada com filtro guiado pela própria foto;
3. cor do primeiro plano: F = céu + (foto - céu) / alfa  -> tira o azul dos fios (sem halo);
4. aplica na versão HD (alfa e céu ampliados) e salva WebP com transparência.
"""
import sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi

src, hd, dst = sys.argv[1], sys.argv[2], sys.argv[3]
W_OUT = int(sys.argv[4]) if len(sys.argv) > 4 else 1800

I = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
H, W = I.shape[:2]
key = I[..., 2] - np.maximum(I[..., 0], I[..., 1])
sky = (key > .2) & (I[..., 2] > .45)
sky = ndi.binary_erosion(sky, iterations=3)

# 1) cor do céu em toda a imagem: média ponderada só com pixels de céu
def fill(ch, m, s):
    num = cv2.GaussianBlur(ch * m, (0, 0), s)
    den = cv2.GaussianBlur(m.astype(np.float32), (0, 0), s)
    return num / np.maximum(den, 1e-4)
m = sky.astype(np.float32)
B = np.stack([fill(I[..., c], m, 25) for c in range(3)], -1)
far = cv2.GaussianBlur(m, (0, 0), 25) < 1e-3
if far.any():
    B2 = np.stack([fill(I[..., c], m, 120) for c in range(3)], -1)
    B[far] = B2[far]

# 2) alfa pela distância ao céu (azul pesa mais), com transição suave
d = np.sqrt(((I - B) ** 2 * np.array([.8, 1., 1.4])).sum(-1))
a = np.clip((d - .07) / (.30 - .07), 0, 1)
core = ndi.binary_fill_holes(a > .6)
lab, n = ndi.label(core)
big = np.argmax(ndi.sum(core, lab, range(1, n + 1))) + 1
core = lab == big
a = np.where(ndi.binary_erosion(core, iterations=4), 1.0, a)
a[~ndi.binary_dilation(core, iterations=18)] = 0

def guided(G, p, r, eps):
    """Filtro guiado (He et al.) com guia em tons de cinza."""
    bx = lambda x: cv2.boxFilter(x, -1, (r, r))
    mI, mp = bx(G), bx(p)
    cov = bx(G * p) - mI * mp
    var = bx(G * G) - mI * mI
    A = cov / (var + eps)
    b = mp - A * mI
    return bx(A) * G + bx(b)
g = cv2.cvtColor((I * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
a = np.clip(guided(g, a, 5, 1e-3), 0, 1)
a = np.clip((a - .04) / .92, 0, 1)
# pixels com cara de céu (azul claro) entre os fios: ficam transparentes; o azul-marinho do macacão fica
ss = lambda e0, e1, x: np.clip((x - e0) / (e1 - e0), 0, 1)
skyish = ss(.08, .2, key) * ss(.42, .58, I[..., 2])
a = a * (1 - skyish)

# 4) versão HD
Hd = np.asarray(Image.open(hd).convert("RGB").resize((W_OUT, round(H * W_OUT / W)), Image.LANCZOS)).astype(np.float32) / 255
h2, w2 = Hd.shape[:2]
A2 = np.clip(cv2.resize(a, (w2, h2), interpolation=cv2.INTER_CUBIC), 0, 1)
B2 = cv2.resize(B, (w2, h2), interpolation=cv2.INTER_LINEAR)
# a foto original tem uma moldura fina nas bordas: fora do recorte
bw = max(6, w2 // 150)
A2[:, :bw] = 0; A2[:, -bw:] = 0; A2[:bw, :] = 0; A2[-bw:, :] = 0
# 3) cor do primeiro plano sem o céu misturado
F = B2 + (Hd - B2) / np.maximum(A2, .12)[..., None]
F = np.where((A2 > .985)[..., None], Hd, np.clip(F, 0, 1))
# tira o reflexo azul do céu no cabelo (faixa de até ~60 px da borda): azul nunca passa do vermelho/verde
edge = cv2.dilate((A2 < .99).astype(np.uint8), np.ones((5, 5), np.uint8), iterations=12).astype(bool)
skin = (F[..., 0] > F[..., 2] + .06)  # pele e macacão branco não mudam
cap = np.maximum(F[..., 0], F[..., 1]) * 1.04 + .015
hair = (np.arange(h2) < h2 * .7)[:, None]  # só no cabelo: o azul-marinho do macacão fica
F[..., 2] = np.where(edge & ~skin & hair, np.minimum(F[..., 2], cap), F[..., 2])
out = np.dstack([F, A2]) * 255
Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA").save(dst, quality=88, method=6)
print("ok", w2, h2)
