"""Deixa uma foto em HD sem o aspecto "de cera": super-resolução (Real-ESRGAN, ver
super_resolucao.py) misturada com a ampliação clássica da foto original, para manter
o grão e a textura da pele.

Uso: python3 hd.py PESOS.pth entrada.jpg saida.webp LARGURA [mistura=0.6] [qualidade=84]
  mistura = peso da super-resolução (0..1). Rostos: 0.55–0.65. Objetos e carros: 0.8–1.
"""
import os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import super_resolucao as sr

pesos, src, dst, largura = sys.argv[1:5]
mix = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
q = int(sys.argv[6]) if len(sys.argv) > 6 else 84
largura = int(largura)

sr.W.update({k: v.astype(np.float32) for k, v in sr.load_pth(pesos).items()})
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(np.float32) / 255
fn = sr.run if "conv_first.weight" in sr.W else sr.run_compact
up = np.clip(sr.tiled(a, fn), 0, 1)
up = Image.fromarray((up * 255 + 0.5).astype(np.uint8))
alto = round(im.height * largura / im.width)
up = up.resize((largura, alto), Image.LANCZOS)
base = im.resize((largura, alto), Image.LANCZOS)
out = Image.blend(base, up, mix)
out.save(dst, quality=q, method=6) if dst.endswith(".webp") else out.save(dst)
print("ok", dst, out.size)
