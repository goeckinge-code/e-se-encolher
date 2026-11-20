"""Cenas 3D de "E se a gravidade sumisse por 10 segundos?" — protagonista: Davi (blender/personagens.py).
Gramática de câmera do canal (blender/camera.py, ESTILO.md). Cada build_sN devolve (frame, rig).
Davi com s=1 tem ~2,1 de altura. Close: h≈1.9 · médio: 2.6 · corpo inteiro: 3.4. Coisa grande em cima, Davi embaixo.
"""
import bpy, math, random, os, sys
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "blender"))
from lib import *
from look import *
from camera import Rig, Shot
from personagens import DaviCtl
import scenes as OLD

def backyard(fence=True):
    cube("grass", "#6CC36A", (0, 3, -0.05), (30, 14, 0.1), bevel=0)
    for k in range(-8, 9): cube(f"mow{k}", "#62B860", (k*1.6, 3, 0.0), (0.8, 14, 0.01), bevel=0)
    # casa atrás
    cube("house", "#F4E3C1", (0, 4.2, 2.2), (7, 1.6, 4.4), bevel=0.04)
    roof = cube("roof", "#C2523C", (0, 4.2, 4.9), (7.6, 2.2, 0.25), bevel=0.04, rot=(math.radians(-20), 0, 0))
    for x in (-2.2, 2.2):
        cube(f"hwin{x}", "#FFFFFF", (x, 3.38, 2.6), (1.3, 0.06, 1.2), bevel=0.03)
        cube(f"hwing{x}", "#8FC8EE", (x, 3.34, 2.6), (1.1, 0.04, 1.0), bevel=0)
    cube("hdoor", "#4E8FE0", (0, 3.38, 1.05), (1.1, 0.06, 2.1), bevel=0.03)
    if fence:
        for k in range(-12, 13): cube(f"fence{k}", "#FFFFFF", (k*0.45, 2.4, 0.45), (0.14, 0.06, 0.9), bevel=0.02)
        cube("fencebar", "#FFFFFF", (0, 2.42, 0.6), (11, 0.04, 0.08), bevel=0)

def bowl(name="bowl"):
    b = empty(name, (0, 0, -50))
    s = sphere(name+"b", "#4FC3E8", (0, 0, 0), 0.17, (1, 1, 0.6), b, sub=1)
    Leo._cut_upper(Leo, s, 0.0)
    cyl(name+"m", "#FFFFFF", (0, 0, -0.005), 0.15, 0.01, b, bevel=0)
    return b

def zzz():
    return [text3d(f"z{k}", "Z", "#FFFFFF", (0, 0, -50), 0.16+k*0.07, extrude=0.03) for k in range(3)]

def place_zzz(zs, t, base, on):
    for k, z in enumerate(zs):
        if not on: z.hide_render = True; continue
        u = (t*0.8 + k/3) % 1
        z.hide_render = False; z.location = (base[0] + 0.15 + u*0.5, base[1], base[2] + u*0.8)

def floaters(n, seed, kind):
    rr = random.Random(seed); out = []
    for k in range(n):
        if kind == "milk": o = sphere(f"milk{seed}_{k}", "#FFFFFF", (0, 0, -50), rr.uniform(0.04, 0.09), sub=1)
        else: o = torus(f"cer{seed}_{k}", "#F2A541", (0, 0, -50), 0.05, 0.02)
        out.append((o, rr.uniform(-0.7, 0.7), rr.uniform(-0.5, 0.6), rr.uniform(0, 6.28), rr.uniform(0.6, 1.4)))
    return out

def hammock_leo():
    """o vizinho (Léo) dormindo numa rede — grupo que flutua inteiro"""
    g = empty("hammock", (0, 0, -50))
    sphere("hamnet", "#F28C28", (0, 0, 0), 0.9, (1.3, 0.45, 0.22), g, sub=1)
    for sx in (-1, 1): poly_tube(f"hamrope{sx}", "#8E5A34", [(sx*1.1, 0, 0.05), (sx*1.6, 0, 0.35)], 0.02, g)
    leo = LeoCtl("leo"); leo.L.root.parent = g
    return g, leo

# ================================================================== S0 — você sai do chão
def build_s0(sc, W):
    setup_render("#9FD8F7")
    backyard()
    bw = bowl()
    cam = camera(40); davi = DaviCtl()
    TG, TP, TC = W("gravidade"), W("No primeiro"), W("chão")
    T_UP = W("segundo")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.3, 3.5),                      # Davi tomando café no quintal
             Shot(TG - 0.05, 0, 3.0, 6.0, roll=-6),     # céu: "a gravidade sumisse"
             Shot(TP - 0.05, 0, 0.6, 2.0, roll=6),      # close nos pés saindo do chão
             Shot(TC - 0.1, 0, 2.4, 2.2, roll=-5)]     # close no rosto, já no ar
    rig = Rig(cam, shots, D, enter=(0, 0.4, 0.5, 7), exit=(0, 0.8, -0.4, -7))
    L = davi.L
    def frame(t):
        up = max(0.0, t - T_UP)
        z = 0.35*up**1.3
        flail = t > T_UP
        davi.pose(t, loc=(0, 0, z), rotx=math.sin(t*1.7)*0.08*flail, roty=math.sin(t*1.3)*0.12*flail,
                  expr=[[0, "happy"], [TG + 0.3, "neutral"], [T_UP + 0.1, "shock"]],
                  arms=((30, 60), 12) if not flail else (110 + math.sin(t*9)*25, 110 - math.sin(t*9)*25), look=(0, 6 if not flail else -10))
        bpy.context.view_layer.update()
        if not flail:
            bw.location = L.arm[-1].matrix_world @ Vector((-0.06, -0.12, -0.45)); bw.rotation_euler = (0, 0, 0)
        else:   # a tigela escapa da mão e sobe girando
            bw.location = (-0.4 - up*0.3, -0.3, 1.0 + z + up*0.4); bw.rotation_euler = (up*2, up*1.3, 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S1 — bolhas de leite
def build_s1(sc, W):
    setup_render("#9FD8F7")
    backyard()
    bw = bowl()
    milk = floaters(16, 1, "milk"); cer = floaters(12, 2, "cer")
    cam = camera(40); davi = DaviCtl()
    TL, TB, TV = W("o leite"), W("bolhas"), W("voando")
    D = sc["dur"]
    Z = 1.6   # Davi flutuando acima da cerca
    shots = [Shot(0, 0, Z + 1.0, 3.6),
             Shot(TL - 0.05, -0.35, Z + 1.35, 1.8, roll=6),   # tigela virando no ar
             Shot(TB - 0.05, 0, Z + 1.5, 2.2, roll=-5),       # bolhas em volta do rosto
             Shot(TV - 0.05, 0, Z + 1.55, 1.7, kind="cut")]   # boca aberta pegando uma bolha
    rig = Rig(cam, shots, D, enter=(0, -0.6, 0.5, -7), exit=(0.7, 0, -0.4, 7))
    def frame(t):
        davi.pose(t, loc=(0, 0, Z + math.sin(t*1.5)*0.08), roty=math.sin(t*1.1)*0.1,
                  expr=[[0, "neutral"], [TB, "happy"], [TV, "shock"]], mouth=[[0, None], [TV, "o"]],
                  arms=((60, 40), (60, 40)), look=(0, -8))
        k = cl((t - TL + 0.3) / 1.0)
        bw.location = (-0.45, -0.35, Z + 1.3 + math.sin(t*2)*0.05); bw.rotation_euler = (math.pi*ease(k), t*0.6, 0)
        for (o, x, z, ph, sp) in milk + cer:
            on = t > TL + 0.1
            o.hide_render = not on
            spread = ease((t - TL - 0.1) / 1.2)
            o.location = (-0.45 + (x + math.sin(t*sp + ph)*0.08 + 0.45)*spread, -0.45 + math.cos(ph)*0.15,
                          Z + 1.3 + (z + math.cos(t*sp*0.8 + ph)*0.08)*spread)
            o.rotation_euler = (t*sp, ph, t)
        rig.apply(t)
    return frame, rig

# ================================================================== S2 — o vizinho na rede
def build_s2(sc, W):
    setup_render("#8FD0F5")
    backyard()
    ham, leo = hammock_leo(); zs = zzz()
    cam = camera(40); davi = DaviCtl()
    TV, TF, TD = W("o vizinho"), W("flutuando"), W("dormindo")
    D = sc["dur"]
    Z = 2.4
    shots = [Shot(0, 0, Z + 1.2, 3.6),
             Shot(TV - 0.05, 0.2, Z + 2.2, 4.0, roll=-6),   # rede passando em cima
             Shot(TD - 0.05, 0.0, Z + 3.0, 2.4, roll=5),   # close no Léo dormindo
             Shot(W("na rede") + 0.05, 0, Z + 1.55, 1.9, roll=-5)]   # Davi sem acreditar
    rig = Rig(cam, shots, D, enter=(0.7, 0, 0.45, 7), exit=(0, 0.8, -0.45, -7))
    def frame(t):
        davi.pose(t, loc=(0, 0, Z + math.sin(t*1.5)*0.08), roty=math.sin(t*1.1)*0.1,
                  expr=[[0, "happy"], [TV + 0.3, "shock"], [W("na rede") + 0.05, "worried"]], arms=(50, 50), look=(0, -12 if t > TV else 0))
        x = lerp(-2.4, 1.6, cl((t - TV + 0.6) / 3.8))
        ham.location = (x, 0.2, Z + 2.85 + math.sin(t*1.3)*0.06); ham.rotation_euler = (0, math.sin(t*0.9)*0.08, 0)
        leo.pose(t, loc=(1.0, -0.55, 0.15), roty=math.radians(-90), expr=[[0, "sleep"]], arms=(10, 10), look=(0, 0))
        bpy.context.view_layer.update()
        hp = leo.L.head.matrix_world @ Vector((0, 0, 0.4))
        place_zzz(zs, t, (hp.x, hp.y - 0.4, hp.z), True)
        rig.apply(t)
    return frame, rig

# ================================================================== S3 — acima dos telhados
def build_s3(sc, W):
    setup_render("#7CC4F2")
    rr = random.Random(4)
    # bairro lá embaixo (empilhado: Davi em cima no céu, casas embaixo)
    cube("ground", "#6CC36A", (0, 6, -6.05), (60, 30, 0.1), bevel=0)
    for i in range(-5, 6):
        x = i*2.2; h = rr.uniform(1.6, 2.6); c = rr.choice(["#F4E3C1", "#FFD3B0", "#CFE3F7", "#E6D3F5"])
        cube(f"h{i}", c, (x, 6 + rr.uniform(-1, 1), -6 + h/2), (1.8, 1.8, h), bevel=0.04)
        cube(f"r{i}", rr.choice(["#C2523C", "#8E5A34", "#4E6FB0"]), (x, 6, -6 + h + 0.2), (2.0, 2.0, 0.4), bevel=0.05)
    cl_ = []
    for k in range(6):
        g = empty(f"cloud{k}", (rr.uniform(-4, 4), rr.uniform(2, 5), rr.uniform(1.0, 5.0)))
        for j in range(4): sphere(f"cl{k}{j}", "#FFFFFF", (j*0.45 - 0.7, 0, math.sin(j)*0.15), 0.42 + (j % 2)*0.12, (1, 0.6, 0.8), g, sub=1)
        cl_.append(g)
    cam = camera(40); davi = DaviCtl(); bird = text3d("bird", "v", "#1E1B2E", (0, 0, -50), 0.4, extrude=0.02)
    TT, TL, TVo = W("telhados"), W("E lembra"), W("volta")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.4, 4.0),
             Shot(TT - 0.1, 0, -1.5, 10.0, roll=-6),        # abre: o bairro lá embaixo
             Shot(TL - 0.05, 0, 1.6, 2.4, roll=6),          # volta pro Davi
             Shot(TVo - 0.05, 0, 1.75, 1.8, kind="cut", shake=0.05)]   # close: percebe
    rig = Rig(cam, shots, D, enter=(0, -0.8, 0.5, -8), exit=(0, -1.5, -0.3, 6), exit_t=0.25)
    def frame(t):
        davi.pose(t, loc=(0, 0, math.sin(t*1.4)*0.1), rotz=math.sin(t*0.5)*0.2, roty=math.sin(t*0.8)*0.15,
                  expr=[[0, "happy"], [TL + 0.3, "neutral"], [TVo, "shock"]],
                  arms=((150, 20), (150, 20)) if t < TL else (60, 60), look=(0, 0 if t < TVo else 15))
        for k, g in enumerate(cl_): g.location.x += 0.0; g.location.x = ((k*1.7 + t*0.25) % 9) - 4.5
        bird.location = (lerp(-3, 3, (t*0.25) % 1), 1.0, 2.6 + math.sin(t*6)*0.05); bird.rotation_euler = (math.pi/2, 0, 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S4 — ela volta: piscina
def build_s4(sc, W):
    setup_render("#8FD0F5")
    backyard(fence=False)
    cube("deck", "#E8D3A8", (0, 0.4, -0.02), (6, 3.4, 0.1), bevel=0.02)
    cube("poolwall", "#FFFFFF", (0, 0.4, 0.15), (3.6, 2.4, 0.4), bevel=0.06)
    water = cube("water", "#3FB6E8", (0, 0.4, 0.32), (3.3, 2.1, 0.08), bevel=0.02)
    splash = [sphere(f"sp{k}", "#BFEAFF", (0, 0, -50), 0.12, sub=1) for k in range(14)]
    rings = [torus(f"wr{k}", "#E8F8FF", (0, 0, -50), 0.4, 0.03) for k in range(3)]
    boia = torus("boia", "#FF5A7A", (0, 0, -50), 0.34, 0.11)
    cam = camera(40); davi = DaviCtl()
    TD, TVo, TS = W("dez"), W("volta"), W("só")
    T_HIT = TS + 0.15
    TA = W("Ainda")
    D = sc["dur"]
    rr = random.Random(9); sd = [(rr.uniform(0, 6.28), rr.uniform(1.5, 3.0), rr.uniform(0.8, 1.6)) for _ in splash]
    shots = [Shot(0, 0, 4.6, 3.0),                           # lá em cima, parado no ar
             Shot(TVo - 0.05, 0, 3.4, 4.2, roll=-6),         # começa a cair
             Shot(T_HIT - 0.12, 0, 0.9, 4.2, kind="slow", dur=0.5),   # câmera desce junto
             Shot(T_HIT + 0.02, 0, 0.9, 3.6, kind="cut", shake=0.09),  # TCHIBUM
             Shot(TA - 0.05, 0, 0.8, 1.8, roll=5)]           # close: cabeça pra fora d'água
    rig = Rig(cam, shots, D, enter=(0, 1.2, 0.5, 7), exit=(0, 0, -0.45, -7))
    def frame(t):
        if t < TVo:
            z = 3.6 + math.sin(t*1.4)*0.08; ex = "happy" if t < TD + 0.3 else "shock"
        elif t < T_HIT:
            u = (t - TVo) / (T_HIT - TVo); z = lerp(3.6, -0.6, u*u); ex = "shock"
        else:
            k = t - T_HIT; z = -1.05 + 0.25*eout(cl((k - 0.4)/0.5)) + math.sin(t*3)*0.03; ex = "dizzy" if k < 1.0 else "happy"
        falling = TVo <= t < T_HIT
        davi.pose(t, loc=(0, 0.3, z), expr=[[0, ex]], arms=(165, 165) if falling else (70 + math.sin(t*5)*10, 70 - math.sin(t*5)*10),
                  look=(0, -15 if falling else 0), mouth=[[0, None], [TVo, "yawn"], [T_HIT, None]])
        k = t - T_HIT
        for (ph, sp, hgt), s in zip(sd, splash):
            if 0 <= k < 0.9:
                s.location = (math.cos(ph)*sp*k, 0.1 + math.sin(ph)*0.3, 0.4 + hgt*3*k - 5*k*k); s.hide_render = s.location.z < 0.3
            else: s.hide_render = True
        for i, r in enumerate(rings):
            u = (k - i*0.25) / 1.2
            r.location = (0, 0.3, 0.37) if 0 < u < 1 else (0, 0, -50); r.scale = (1 + u*2.5, 1 + u*1.2, 1)
        boia.location = (0.75, 0.15, 0.4 + math.sin(t*3)*0.02) if k > 0.3 else (0, 0, -50)
        rig.apply(t)
    return frame, rig

# ================================================================== S5 — escolha
def build_s5(sc, W):
    setup_render("#8FD0F5")
    backyard(fence=False)
    cube("deck", "#E8D3A8", (0, 0.4, -0.02), (6, 3.4, 0.1), bevel=0.02)
    cube("poolwall", "#FFFFFF", (0, 0.4, 0.15), (3.6, 2.4, 0.4), bevel=0.06)
    cube("water", "#3FB6E8", (0, 0.4, 0.32), (3.3, 2.1, 0.08), bevel=0.02)
    boia = torus("boia", "#FF5A7A", (0, 0.3, 0.42), 0.36, 0.12)
    q = text3d("q", "?", "#FFD93D", (0.65, -0.3, 1.25), 0.45, extrude=0.04)
    cam = camera(40); davi = DaviCtl()
    D = sc["dur"]
    shots = [Shot(0, 0, 1.3, 3.0, push=0.035)]          # Davi embaixo, card em cima
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, 7), exit=(0, 0, 0, 0), exit_t=0.01)
    def frame(t):
        davi.pose(t, loc=(0, 0.3, -0.8 + math.sin(t*2)*0.03), expr=[[0, "neutral"], [W("Comenta"), "happy"]],
                  arms=(55, (40, 100)), look=(-8, -6), tilt=8)
        boia.location.z = 0.42 + math.sin(t*2)*0.03
        q.location.z = 1.25 + math.sin(t*4)*0.06; q.rotation_euler = (math.pi/2, 0, math.sin(t*3)*0.2)
        rig.apply(t)
    return frame, rig

BUILD = {f"s{i}": globals()[f"build_s{i}"] for i in range(6)}
