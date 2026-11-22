"""Cidade de fundo: calçada da frente (onde os personagens ficam), rua com carros passando,
calçada do outro lado com lojas (toldo, letreiro, vitrine) e prédios atrás.

Layout (eixo y = profundidade, a câmera fica em y negativo olhando para +y):
  y -4..2   calçada/praça da frente  → personagens e objetos da cena
  y  2..9   rua (duas mãos)          → carros passando
  y  9..11  calçada de lá            → postes, árvores, pedestres
  y 11      fachadas das lojas       → toldos, letreiros, vitrines
  y 24+     prédios altos

Uso: anim = cidade.build(x0=0, seed=1, night=False); no frame: anim(t)
"""
import math, random
import kit
from kit import box, cyl, text, empty, show, hexcol

LOJAS = [("PADARIA", "#E9C46A", "#C0392B"), ("FARMÁCIA", "#DFF5E1", "#27AE60"), ("MERCADO", "#F4A261", "#2E86DE"),
         ("CAFÉ", "#D7B49E", "#6D4C41"), ("PIZZARIA", "#F6D6AD", "#E74C3C"), ("ÓTICA", "#CFE3F7", "#34495E"),
         ("SORVETES", "#FFD6E8", "#E84393"), ("LOJA", "#E8DAEF", "#8E44AD"), ("BANCO", "#E5E8E8", "#C0392B"),
         ("ACADEMIA", "#D6EAF8", "#F39C12"), ("LIVROS", "#FDEBD0", "#16A085"), ("CELULARES", "#EAEDED", "#2C3E50")]

def awning(name, x, w, z, c1, c2, y):
    g = empty(name, (x, y - 0.55, z))
    n = max(3, int(w / 0.45))
    for i in range(n):
        o = box(f"{name}_{i}", c1 if i % 2 == 0 else c2, (w / n, 1.1, 0.08), ((i - (n - 1) / 2) * w / n, 0, 0), g, rot=(0.35, 0, 0), bevel=0.0)
    box(name + "_v", c2, (w, 0.05, 0.22), (0, -0.53, -0.28), g, bevel=0.0)
    return g

def shop(i, x, w, y, rnd, night):
    nome, wall, acc = LOJAS[i % len(LOJAS)]
    floors = rnd.choice([1, 2, 2, 3])
    H = 3.2 + floors * 2.6
    n = f"shop{i}"
    box(n + "_w", wall, (w, 0.6, H), (x, y + 0.3, H / 2), bevel=0.04)
    box(n + "_cor", kit._shade(wall, 0.85), (w + 0.05, 0.7, 0.25), (x, y + 0.25, H), bevel=0.03)
    # vitrine + porta
    glass = "#F9E79F" if night else "#A9DCF5"
    box(n + "_vit", "#2C3E50", (w * 0.62, 0.1, 1.7), (x - w * 0.12, y - 0.02, 1.25), bevel=0.03)
    box(n + "_vitg", glass, (w * 0.58, 0.12, 1.55), (x - w * 0.12, y - 0.03, 1.25), bevel=0.02)
    box(n + "_door", kit._shade(acc, 0.8), (0.85, 0.12, 2.1), (x + w * 0.33, y - 0.03, 1.05), bevel=0.03)
    # produtos na vitrine
    for k in range(3):
        box(f"{n}_prod{k}", rnd.choice(["#E74C3C", "#F1C40F", "#3498DB", "#2ECC71", "#9B59B6"]),
            (0.32, 0.2, 0.32 + 0.15 * k), (x - w * 0.3 + k * 0.5, y - 0.12, 0.6 + (0.32 + 0.15 * k) / 2), bevel=0.04)
    # letreiro + toldo
    box(n + "_sign", acc, (w * 0.8, 0.18, 0.65), (x, y - 0.1, 2.75), bevel=0.06)
    text(n + "_st", nome, "#FFFFFF", 0.42 if len(nome) < 9 else 0.34, (x, y - 0.21, 2.75))
    awning(n + "_aw", x - w * 0.12, w * 0.66, 2.3, "#FFFFFF", acc, y)
    # andares de cima
    for f in range(floors):
        z = 4.3 + f * 2.6
        for k in range(max(1, int(w / 1.3))):
            nk = max(1, int(w / 1.3))
            wx = x + (k - (nk - 1) / 2) * 1.3
            box(f"{n}_win{f}{k}", "#EDEDED", (0.85, 0.08, 1.15), (wx, y - 0.02, z), bevel=0.03)
            box(f"{n}_wg{f}{k}", "#F7DC6F" if (night and rnd.random() < 0.7) else "#9AD3F0", (0.72, 0.1, 1.0), (wx, y - 0.03, z), bevel=0.02)
    return H

def tree(name, x, y):
    box(name + "_t", "#7B5B3A", (0.25, 0.25, 1.6), (x, y, 0.8), bevel=0.04)
    box(name + "_l1", "#58B368", (1.3, 1.3, 1.1), (x, y, 2.0), bevel=0.2)
    box(name + "_l2", "#4CA65C", (0.9, 0.9, 0.7), (x + 0.1, y, 2.75), bevel=0.15)

def lamp(name, x, y, night):
    box(name + "_p", "#5D6D7E", (0.12, 0.12, 4.2), (x, y, 2.1), bevel=0.02)
    box(name + "_a", "#5D6D7E", (0.7, 0.1, 0.1), (x - 0.3, y, 4.15), bevel=0.02)
    box(name + "_l", "#FFF6C8" if night else "#ECF0F1", (0.35, 0.25, 0.15), (x - 0.6, y, 4.05), bevel=0.04)

def bench(name, x, y):
    box(name + "_s", "#A0522D", (1.4, 0.45, 0.08), (x, y, 0.45), bevel=0.02)
    box(name + "_b", "#A0522D", (1.4, 0.08, 0.4), (x, y + 0.2, 0.75), bevel=0.02)
    for sx in (-1, 1): box(f"{name}_l{sx}", "#2C3E50", (0.08, 0.4, 0.45), (x + sx * 0.6, y, 0.22), bevel=0.01)

CAR_COLORS = ["#E74C3C", "#3498DB", "#F1C40F", "#ECF0F1", "#2ECC71", "#9B59B6", "#E67E22", "#34495E"]

def build(x0=0.0, seed=1, night=False, ped=True, near=True, span=14.0, cars=True):
    """Monta a cidade em volta de x0. Devolve anim(t) que move carros e pedestres."""
    rnd = random.Random(seed)
    sky = "#1E2A4A" if night else "#8FD0F5"
    kit.setup(sky)
    asphalt = "#3D4049" if not night else "#2B2E37"
    # chão
    box("near_walk", "#C9C3B8" if not night else "#8C8A86", (80, 7.0, 0.3), (x0, -1.5, -0.15), bevel=0)
    box("curb1", "#E5E2DC", (80, 0.3, 0.32), (x0, 2.0, -0.14), bevel=0.02)
    box("road", asphalt, (80, 7.0, 0.2), (x0, 5.5, -0.2), bevel=0)
    for k in range(-10, 11):
        box(f"lane{k}", "#F4D03F", (1.6, 0.15, 0.02), (x0 + k * 3.6, 5.5, -0.09), bevel=0)
    for k in range(8):   # faixa de pedestres
        box(f"zebra{k}", "#F2F3F4", (0.5, 6.4, 0.02), (x0 - 5.5 + k * 0.9, 5.5, -0.09), bevel=0)
    box("curb2", "#E5E2DC", (80, 0.3, 0.32), (x0, 9.0, -0.14), bevel=0.02)
    box("far_walk", "#D5CEC4" if not night else "#8C8A86", (80, 2.0, 0.3), (x0, 10.0, -0.15), bevel=0)
    # lojas
    x = x0 - span - 2
    i = rnd.randrange(len(LOJAS))
    while x < x0 + span + 2:
        w = rnd.uniform(3.4, 4.6)
        shop(i, x + w / 2, w, 11.0, rnd, night)
        x += w + 0.05; i += 1
    # prédios altos ao fundo
    kit.city("bg", y=24, seed=seed)
    kit.bpy.data.objects["bg"].location.x = x0
    box("sky", sky, (200, 0.2, 120), (x0, 40, 30), bevel=0)
    # postes, árvores, bancos
    for k in range(-3, 4):
        lamp(f"lampF{k}", x0 + k * 6.0 + 1.5, 9.6, night)
        tree(f"treeF{k}", x0 + k * 6.0 - 1.5, 9.8)
    if near:
        for k in (-1, 1):
            lamp(f"lampN{k}", x0 + k * 4.2, 1.6, night)
    # carros nas duas mãos
    cars = []
    for k in range(4 if cars else 0):
        lane = 4.0 if k % 2 == 0 else 7.0
        d = 1 if k % 2 == 0 else -1
        c = kit.car(f"car{k}", (0, lane, 0), color=CAR_COLORS[(k + seed) % len(CAR_COLORS)], rotz=0 if d > 0 else math.pi)
        c.scale = (0.85, 0.85, 0.85)
        cars.append((c, d, rnd.uniform(5.0, 8.0), rnd.uniform(0, 40)))
    # pedestres do outro lado
    peds = []
    if ped:
        for k in range(3):
            d = 1 if k % 2 == 0 else -1
            p = kit.person(f"ped{k}", k + seed, (0, 9.7 + 0.3 * (k % 2), 0), rotz=-math.pi / 2 if d > 0 else math.pi / 2)
            peds.append((p, d, rnd.uniform(1.0, 1.5), rnd.uniform(0, 30)))
    if night:   # escurece o cenário (não os personagens, criados depois); janelas e luzes continuam acesas
        lit = ("_wg", "_vitg", "_l", "lane", "zebra", "_st", "_tt")
        for o in kit.bpy.data.objects:
            if o.type in ("MESH", "FONT") and not o.name.startswith(("car", "ped")):
                c = o.color
                bright = any(k in o.name for k in lit) and (c[0] + c[1] > 1.0 or o.type == "FONT")
                f = 1.0 if bright else 0.42
                o.color = (c[0] * f, c[1] * f, c[2] * f * 1.15, 1)
    L = 2 * span + 8
    def anim(t):
        for c, d, v, off in cars:
            c.location.x = x0 + ((off + v * t) % L - L / 2) * d
        for p, d, v, off in peds:
            p.root.location.x = x0 + ((off + v * t) % L - L / 2) * d
            p.pose(t, walk=1.0, bob=0.5, phase=off)
            p.blink(t, off=off)
    return anim
