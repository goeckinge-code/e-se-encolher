"""Alfa do carro em HD (sobre a saída 4x da super-resolução).

- silhueta automática: tudo que não é fundo branco ligado às bordas;
- tomada de ar: onde o branco do carro encontra o fundo branco a borda some, então ela
  é desenhada como vetor (medida na foto original: de (364,477) a (494,520));
- assoalho: cada coluna entre as rodas é preenchida até a faixa escura da base.
Uso: python3 alfa_carro_hd.py car_x4.png carro.webp [alfa_base.webp]
  alfa_base: alfa já existente na mesma resolução (o corpo branco do carro some no fundo
  branco da versão HD; a base anterior, feita sobre a foto 3x, separa melhor).
"""
import sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.uint8)
H, W = im.shape[:2]
K = 4
X = lambda x: (x - 118) * K  # foto original -> 4x
Y = lambda y: (y - 466) * K
lum = im.astype(int).mean(-1)

# 1) silhueta automática (ou a base informada)
if len(sys.argv) > 3:
    base = np.asarray(Image.open(sys.argv[3]).getchannel("A")).astype(np.float32) / 255
    car = base > 0.5
else:
  bright = (lum >= 244).astype(np.uint8)
  dark = cv2.morphologyEx(1 - bright, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
  lab, n = ndi.label(1 - dark)
  border = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
  car = ndi.binary_fill_holes(~np.isin(lab, list(border)))

# 2) tomada de ar vetorial: acima da linha de recorte (y < 514) entre x 360 e 506
air = np.zeros((H, W), np.uint8)
poly = [(360, 515), (361, 479), (364, 476.5), (430, 497.5), (494, 519.5), (506, 522), (506, 515)]
cv2.fillPoly(air, [np.array([(X(x), Y(y)) for x, y in poly], np.int32)], 1)
zone = np.zeros((H, W), bool)
zone[:Y(515), X(359):X(506)] = True
car = np.where(zone, air > 0, car)

# 3) rodas inteiras e assoalho até a faixa escura
yy, xx = np.mgrid[0:H, 0:W]
for cx, cy, r in ((305, 247, 99), (1205, 238, 101)):  # rodas (coordenadas 3x do recorte antigo)
    car |= (xx - cx * 4 / 3) ** 2 + (yy - cy * 4 / 3) ** 2 <= (r * 4 / 3) ** 2
y0, y1 = Y(548), Y(573)
for x in range(X(126), X(560)):
    col = lum[y0:y1, x]
    d = np.nonzero(col < 150)[0]
    if len(d) and car[y0 - 4, x]:
        car[y0:y0 + d.max() + 1, x] = True
wheels = np.zeros((H, W), bool)
for cx, cy, r in ((305, 247, 99), (1205, 238, 101)):
    wheels |= (xx - cx * 4 / 3) ** 2 + (yy - cy * 4 / 3) ** 2 <= (r * 4 / 3) ** 2
car[Y(573):] &= wheels[Y(573):]  # nada abaixo do assoalho além dos pneus (a sombra do chão fica no CSS)
car = ndi.binary_opening(car, iterations=2)
lab2, n2 = ndi.label(car)
sizes = ndi.sum(car, lab2, range(1, n2 + 1))
car = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s > 4000])

a = cv2.GaussianBlur(car.astype(np.float32), (0, 0), 1.1)
a = np.clip((a - 0.5) * 1.6 + 0.5, 0, 1)
# halo branco: na borda, pixels quase brancos perdem um pouco de alfa
er = cv2.erode(a, np.ones((5, 5), np.uint8))
wt = np.clip((lum - 225) / 25, 0, 1)
a = a * (1 - wt) + np.minimum(a, er) * wt
Image.fromarray(np.dstack([im, (a * 255).astype(np.uint8)]), "RGBA").save(dst, quality=90, method=6)
print("ok", W, H)
