"""Monta o atlas de vistas do capacete (3x3) a partir da folha de fotos de referência.

Uso: python3 capacete_atlas.py folha_hd.png ../assets/img/capacete-vistas.webp [LADO_CELULA]
A folha original tem 1536x1024; as caixas abaixo estão nessas coordenadas e são
escaladas para a versão ampliada (tools/super_resolucao.py). Cada caixa envolve o
capacete inteiro; o shader (assets/js/capacete3d.js) encaixa a projeção do molde 3D
exatamente nessa caixa. A ordem precisa bater com CAPACETE_VISTAS no JS.
"""
import sys
from PIL import Image

VISTAS = [  # (nome, ângulo, caixa x0, y0, x1, y1 na folha 1536x1024)
    ("frente", 0, (52, 20, 412, 386)),
    ("3/4 esquerda", -28, (478, 20, 870, 388)),
    ("lateral esquerda", -74, (885, 25, 1250, 376)),
    ("traseira esquerda", -142, (792, 403, 1142, 706)),
    ("traseira", 180, (1278, 38, 1532, 326)),
    ("traseira direita", 160, (1186, 416, 1500, 701)),
    ("lateral direita", 62, (790, 735, 1150, 1024)),
    ("3/4 direita", 30, (30, 740, 368, 1024)),
    ("topo", None, (55, 405, 402, 724)),
]
src, dst = sys.argv[1], sys.argv[2]
C = int(sys.argv[3]) if len(sys.argv) > 3 else 768
im = Image.open(src).convert("RGB")
k = im.width / 1536
atlas = Image.new("RGB", (C * 3, C * 3))
for i, (nome, _, (x0, y0, x1, y1)) in enumerate(VISTAS):
    cell = im.crop((round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k))).resize((C, C), Image.LANCZOS)
    atlas.paste(cell, ((i % 3) * C, (i // 3) * C))
atlas.save(dst, quality=86, method=6)
print("ok", atlas.size)
