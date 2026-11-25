"""Supermercado de fundo + embalagem do feijão.

Layout (a câmera fica em y negativo olhando para +y):
  y -6..4   área aberta com piso quadriculado → ação (palete de promoção no centro)
  x ±4.6    gôndolas laterais formando corredores que vão para o fundo
  y 7       gôndolas do fundo, de frente para a câmera
  topo      luzes, faixas de OFERTA, bandeirinhas

Uso: anim = mercado.build(seed=1); pacote("pack", ...); no frame: anim(t)
"""
import math, random
import kit
from kit import box, cyl, sphere, text, empty, show

PROD_COLORS = ["#E74C3C", "#F1C40F", "#3498DB", "#2ECC71", "#9B59B6", "#E67E22", "#1ABC9C", "#ECF0F1", "#C0392B", "#2980B9"]

# ------------------------------------------------------------------ embalagem
def pacote(name, loc=(0, 0, 0), parent=None, s=1.0, rot=(0, 0, 0), produto=None):
    """Pacote de feijão (frente para -y): saco vermelho, faixa amarela com a marca, 'FEIJÃO' e janela com grãos."""
    P = produto or {"marca": "FEIJÃO GALANTE", "produto": "FEIJÃO", "peso": ""}
    g = empty(name, loc, parent, rot); g.scale = (s, s, s)
    W_, D_, H_ = 0.44, 0.14, 0.62
    box(name + "_bag", "#C62828", (W_, D_, H_), (0, 0, H_ / 2), g, bevel=0.06)
    box(name + "_seal", "#8E1B1B", (W_ + 0.01, D_ * 0.6, 0.05), (0, 0, H_ - 0.03), g, bevel=0.015)
    y = -D_ / 2 - 0.005
    # faixa da marca
    box(name + "_band", "#FFD23F", (W_ - 0.04, 0.012, 0.17), (0, y, H_ - 0.16), g, bevel=0.01)
    marca = P["marca"].split()
    l1 = " ".join(marca[:1]); l2 = " ".join(marca[1:])
    text(name + "_m1", l1, "#8E1B1B", 0.06, (0, y - 0.01, H_ - 0.125), g)
    text(name + "_m2", l2, "#8E1B1B", 0.05, (0, y - 0.01, H_ - 0.19), g)
    # nome do produto
    text(name + "_p", P["produto"], "#FFFFFF", 0.1, (0, y - 0.01, H_ - 0.31), g)
    # janela com os grãos
    box(name + "_win", "#F5E6CC", (0.28, 0.012, 0.15), (0, y, 0.14), g, bevel=0.03)
    rnd = random.Random(5)
    for i in range(14):
        sphere(f"{name}_gr{i}", rnd.choice(["#5D2E1F", "#6E3B26", "#4A2418"]), 0.022,
               (rnd.uniform(-0.11, 0.11), y - 0.012, rnd.uniform(0.09, 0.19)), g, scale=(1.3, 0.6, 0.9))
    if P.get("peso"):
        text(name + "_w", P["peso"], "#FFFFFF", 0.05, (0.13, y - 0.01, 0.04), g)
    return g

# ------------------------------------------------------------------ peças do mercado
def gondola(name, x, y, w=3.0, h=2.6, rotz=0.0, rnd=None, depth=0.7):
    """Prateleira cheia de produtos (frente para -y no espaço local)."""
    rnd = rnd or random.Random(1)
    g = empty(name, (x, y, 0), rot=(0, 0, rotz))
    box(name + "_back", "#DADFE1", (w, 0.12, h), (0, depth / 2 - 0.06, h / 2), g, bevel=0.02)
    box(name + "_top", "#E74C3C", (w + 0.05, depth, 0.28), (0, 0, h + 0.14), g, bevel=0.04)
    box(name + "_base", "#7F8C8D", (w, depth, 0.15), (0, 0, 0.075), g, bevel=0.02)
    nshelf = 4
    for k in range(nshelf):
        z = 0.15 + k * (h - 0.25) / nshelf
        box(f"{name}_sh{k}", "#BDC3C7", (w, depth, 0.05), (0, 0, z), g, bevel=0.01)
        box(f"{name}_tag{k}", "#FFD23F", (w, 0.02, 0.07), (0, -depth / 2 - 0.01, z + 0.0), g, bevel=0.0)
        x0 = -w / 2 + 0.12
        while x0 < w / 2 - 0.15:
            kind = rnd.random()
            col = rnd.choice(PROD_COLORS)
            if kind < 0.45:
                pw, ph = rnd.uniform(0.16, 0.26), rnd.uniform(0.25, 0.42)
                box(f"{name}_p{k}_{x0:.2f}", col, (pw, 0.2, ph), (x0 + pw / 2, -0.05, z + 0.025 + ph / 2), g, bevel=0.02)
            elif kind < 0.75:
                pw = rnd.uniform(0.1, 0.14); ph = rnd.uniform(0.22, 0.4)
                cyl(f"{name}_p{k}_{x0:.2f}", col, pw / 2, ph, (x0 + pw / 2, -0.05, z + 0.025 + ph / 2), g, verts=12)
                pw += 0.02
            else:
                pw, ph = 0.2, 0.3
                box(f"{name}_p{k}_{x0:.2f}", "#C62828", (pw, 0.12, ph), (x0 + pw / 2, -0.05, z + 0.025 + ph / 2), g, bevel=0.03)
            x0 += pw + 0.03
    return g

def cart(name, loc, rotz=0.0, color="#2E86DE"):
    g = empty(name, loc, rot=(0, 0, rotz))
    box(name + "_b", color, (0.9, 0.6, 0.5), (0, 0, 0.75), g, bevel=0.06)
    box(name + "_i", kit._shade(color, 0.7), (0.8, 0.5, 0.45), (0, 0, 0.8), g, bevel=0.04)
    box(name + "_h", "#7F8C8D", (0.08, 0.6, 0.08), (-0.55, 0, 1.15), g, bevel=0.02)
    box(name + "_f", "#7F8C8D", (0.06, 0.06, 0.5), (-0.5, 0, 0.9), g, bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(f"{name}_w{sx}{sy}", "#1E1E24", 0.08, 0.06, (sx * 0.35, sy * 0.22, 0.08), g, rot=(math.pi / 2, 0, 0), verts=12)
    box(name + "_leg", "#7F8C8D", (0.7, 0.4, 0.05), (0, 0, 0.2), g, bevel=0.01)
    return g

def pallet(name, loc, n=(4, 3, 3), produto=None):
    """Palete de promoção com pilha de pacotes + placa OFERTA."""
    g = empty(name, loc)
    box(name + "_wood", "#B07D4F", (2.2, 1.4, 0.2), (0, 0, 0.1), g, bevel=0.03)
    packs = []
    for lz in range(n[2]):
        for ix in range(n[0]):
            for iy in range(n[1]):
                if lz == n[2] - 1 and iy == 0 and ix in (1, 2): continue    # espaço do pacote disputado
                p = caixa(f"{name}_pk{lz}{ix}{iy}", ((ix - (n[0] - 1) / 2) * 0.5, (iy - (n[1] - 1) / 2) * 0.42 + 0.1, 0.2 + lz * 0.55 * 0.8),
                          g, s=0.8)
                packs.append(p)
    return g, packs

def build(seed=1, produto=None):
    rnd = random.Random(seed)
    kit.setup("#F4F1EA")
    # piso quadriculado + paredes
    box("floor", "#ECE8E1", (40, 40, 0.2), (0, 6, -0.1), bevel=0)
    for i in range(-10, 11):
        for j in range(-6, 16):
            if (i + j) % 2 == 0:
                box(f"tile{i}_{j}", "#D8D2C6", (0.98, 0.98, 0.02), (i * 1.0, j * 1.0, 0.005), bevel=0)
    box("backwall", "#F6E3B4", (40, 0.2, 12), (0, 12.5, 6), bevel=0)
    box("ceil", "#FAFAFA", (40, 30, 0.2), (0, 6, 6.6), bevel=0)
    for j in range(-2, 6):
        for i in (-3, 0, 3):
            box(f"light{i}_{j}", "#FFFFFF", (2.2, 0.35, 0.08), (i, j * 2.2, 6.45), bevel=0.02)
            box(f"lightf{i}_{j}", "#D5D8DC", (2.3, 0.45, 0.04), (i, j * 2.2, 6.5), bevel=0.0)
    # faixas e bandeirinhas
    box("banner", "#E53935", (6.0, 0.15, 0.9), (0, 11.8, 4.9), bevel=0.06)
    text("banner_t", "SUPER OFERTAS", "#FFFFFF", 0.62, (0, 11.68, 4.9))
    for k in range(-14, 15):
        o = box(f"flag{k}", ["#E74C3C", "#F1C40F", "#2E86DE", "#2ECC71"][k % 4], (0.35, 0.03, 0.4), (k * 0.45, 3.0, 5.6 - 0.12 * math.cos(k * 0.25)),
                rot=(0, math.pi / 4, 0), bevel=0)
    # gôndolas: fundo e corredores laterais
    for k in range(-2, 3):
        gondola(f"gb{k}", k * 3.2, 9.5, 3.1, 2.8, rnd=rnd)
    for side in (-1, 1):
        for k in range(3):
            gondola(f"gs{side}{k}", side * 5.2, 1.5 + k * 3.2, 3.1, 2.6, rotz=-side * math.pi / 2, rnd=rnd)
    for k in range(3):
        box(f"pend{k}", ["#2E86DE", "#27AE60", "#E67E22"][k], (1.6, 0.1, 0.5), (-5.2 + 0.0, 1.5 + k * 3.2, 4.0), rot=(0, 0, math.pi / 2), bevel=0.04)
    cart("cart1", (-3.6, 5.6, 0), rotz=0.4)
    cart("cart2", (3.7, -1.4, 0), rotz=2.6, color="#E74C3C")
    def anim(t):
        pass
    return anim

# ------------------------------------------------------------------ embalagem real (arte do cliente nas 6 faces)
import os, bpy, bmesh
GALANTE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "galante")
_GMATS = {}
def _face_mat(face):
    if face in _GMATS: return _GMATS[face]
    m = bpy.data.materials.new("galante_" + face); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get("Principled BSDF")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(GALANTE, face + ".png"), check_existing=True)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.nodes.active = tex
    _GMATS[face] = m; return m

def caixa(name, loc=(0, 0, 0), parent=None, s=1.0, rot=(0, 0, 0), W_=0.40, H_=0.55, D_=0.28):
    """Caixa do Feijão Galante (frente para -y), com a arte de cada face. Origem na base."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    x, y, z = W_ / 2, D_ / 2, H_
    V = lambda a, b, c: bm.verts.new((a, b, c))
    # (face, 4 vértices em ordem anti-horária vista de fora, começando no canto inferior esquerdo da arte)
    faces = {
        "frente":   [(-x, -y, 0), (x, -y, 0), (x, -y, z), (-x, -y, z)],
        "costas":   [(x, y, 0), (-x, y, 0), (-x, y, z), (x, y, z)],
        "direita":  [(x, -y, 0), (x, y, 0), (x, y, z), (x, -y, z)],
        "esquerda": [(-x, y, 0), (-x, -y, 0), (-x, -y, z), (-x, y, z)],
        "topo":     [(-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)],
        "base":     [(-x, y, 0), (x, y, 0), (x, -y, 0), (-x, -y, 0)],
    }
    order = list(faces)
    for f in order: me.materials.append(_face_mat(f))
    for i, f in enumerate(order):
        fc = bm.faces.new([V(*p) for p in faces[f]]); fc.material_index = i
        for lp, (u, v) in zip(fc.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]): lp[uv].uv = (u, v)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; o.rotation_euler = rot; o.scale = (s, s, s)
    o.color = kit.hexcol("#1E4FC2")
    return kit.link(o, parent)

def usar_texturas():
    """Liga as texturas no Workbench. Objetos sem material ganham um material com a sua cor de objeto."""
    sc = bpy.context.scene
    cache = {}
    for o in bpy.data.objects:
        if o.type not in ("MESH", "FONT") or o.name.startswith("galante") : continue
        if o.type == "MESH" and len(o.data.materials) and o.data.materials[0] and o.data.materials[0].name.startswith("galante_"): continue
        key = tuple(round(c, 4) for c in o.color[:3])
        if key not in cache:
            m = bpy.data.materials.new("c%d" % len(cache)); m.diffuse_color = (*key, 1); cache[key] = m
        o.data.materials.clear() if o.type == "MESH" and o.data.users == 1 else None
        if o.type == "MESH" and o.data.users > 1:
            o.data = o.data.copy(); o.data.materials.clear()
        o.data.materials.append(cache[key]) if not len(o.data.materials) else None
        o.data.materials[0] = cache[key]
    sc.display.shading.color_type = 'TEXTURE'
