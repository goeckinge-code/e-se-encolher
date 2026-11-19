"""Cenas 3D de "E se você fosse imortal?". Cada build_sN(sc, W) monta o cenário e devolve (frame, rig).

Enquadramento: plano do personagem em y=0, câmera em y=-9 (camera.Rig). Shot(t, cx, cz, h):
centro do quadro (x, z) e altura do quadro h. Léo com s=1 tem ~2.0 de altura (cabeça em z≈1.6).
  corpo inteiro: h≈3.2   médio (cintura pra cima): h≈2.0   close no rosto: h≈1.2
Empilhar na vertical (quadro 9:16): coisa grande em cima, Léo embaixo.
"""
import bpy, math, random, os, sys
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "blender"))
from lib import *
from look import *
from camera import Rig, Shot
import scenes as OLD          # cenários reaproveitáveis do episódio anterior (quarto, Puff)

def stars(n, seed, y=(6, 14), x=(-14, 14), z=(-8, 16), r=(0.02, 0.06), color="#FFFFFF"):
    rr = random.Random(seed)
    return [sphere(f"st{seed}_{k}", color, (rr.uniform(*x), rr.uniform(*y), rr.uniform(*z)), rr.uniform(*r), sub=0, seg=6) for k in range(n)]

def zzz(prefix="z"):
    return [text3d(f"{prefix}{k}", "Z", "#FFFFFF", (0, 0, -50), 0.16+k*0.07, extrude=0.03) for k in range(3)]

def place_zzz(zs, t, base, on):
    for k, z in enumerate(zs):
        if not on: z.hide_render = True; continue
        u = (t*0.8 + k/3) % 1
        z.hide_render = False
        z.location = (base[0] + 0.15 + u*0.5 + math.sin(u*6)*0.06, base[1], base[2] + u*0.9)

def ring_stars(prefix, n=5, r=0.06):
    return [sphere(f"{prefix}{k}", "#FFD93D", (0, 0, -50), r, sub=0, seg=8) for k in range(n)]

def place_ring(objs, t, c, R, on):
    for k, o in enumerate(objs):
        o.hide_render = not on
        a = t*6 + k/len(objs)*2*math.pi
        o.location = (c[0] + math.cos(a)*R, c[1] - 0.2 + math.sin(a)*0.2, c[2] + math.sin(a)*R*0.25)

def sweat_drop(name="sweat"):
    return sphere(name, "#7EC8F2", (0, 0, -50), 0.06, (0.8, 0.5, 1.25), sub=1)

# ================================================================== S0 — o piano
def build_s0(sc, W):
    setup_render("#9FD3F0")
    cube("street", "#7B8494", (0, 1.5, -0.06), (30, 8, 0.1), bevel=0)
    cube("sidewalk", "#D9D2C5", (0, 0.6, 0.0), (30, 3.2, 0.12), bevel=0.02)
    for k in range(-8, 9):
        cube(f"sw{k}", "#C4BCAE", (k*1.2, 0.6, 0.065), (0.04, 3.2, 0.01), bevel=0)
    cube("bldg", "#E8A87C", (0, 2.6, 4.5), (30, 0.4, 9), bevel=0)
    cube("bldgtrim", "#D08A5E", (0, 2.38, 2.7), (30, 0.1, 0.18), bevel=0)
    for i in range(-5, 6):
        for j in range(3):
            cube(f"win{i}{j}", "#FFFFFF", (i*2.1, 2.36, 3.6+j*2.2), (1.1, 0.08, 1.4), bevel=0.03)
            cube(f"wing{i}{j}", "#7FB2E5", (i*2.1, 2.3, 3.6+j*2.2), (0.9, 0.05, 1.2), bevel=0)
    cube("door", "#8E4E2A", (-2.6, 2.36, 1.2), (1.2, 0.1, 2.4), bevel=0.04)
    cyl("pole", "#3E4A5C", (2.6, 0.2, 1.8), 0.06, 3.6, bevel=0.01)
    sphere("lamp", "#FFE9A8", (2.6, 0.2, 3.65), 0.2, sub=1)
    # piano de cauda reto (caixa preta + teclado)
    pn = empty("piano", (0, 0, 20))
    cube("pbody", "#1E1B2E", (0, 0, 0.55), (1.9, 0.9, 1.1), pn, bevel=0.06)
    cube("pkeys", "#FFFFFF", (0, -0.5, 0.75), (1.5, 0.25, 0.08), pn, bevel=0.01)
    for k in range(9):
        cube(f"pblk{k}", "#1E1B2E", (-0.65+k*0.16, -0.55, 0.8), (0.06, 0.14, 0.04), pn, bevel=0)
    for sx in (-1, 1):
        cyl(f"pleg{sx}", "#1E1B2E", (sx*0.8, 0, -0.2), 0.06, 0.5, pn, bevel=0.01)
    cam = camera(40); leo = LeoCtl("leo"); puff = OLD.Puff(9); dz = ring_stars("dz")
    TP, TC, TL, TA, TV = W("piano"), W("cai"), W("levanta"), W("ajeita"), W("escola")
    T_HIT = W("cabeça")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.25, 3.6),
             Shot(TP, 0, 3.0, 6.4, roll=-6),                     # mostra o piano vindo
             Shot(T_HIT + 0.05, 0.1, 0.85, 2.5, kind="cut", shake=0.07),   # pancada: corte seco + tremida
             Shot(TL, 0, 1.4, 2.1, roll=5),                     # close quando ele levanta
             Shot(TV, 1.4, 1.3, 3.8, roll=-5)]                   # abre quando sai andando
    rig = Rig(cam, shots, D, enter=(0, 0.3, 0.5, 8), exit=(1.2, 0.0, -0.35, -7))
    def frame(t):
        # piano cai e acerta em T_HIT
        if t < T_HIT:
            u = (t - TP) / (T_HIT - TP)
            pz = 6.2 - 5.4 * max(0, u)**2 if t > TP else 20
            pn.location = (0, 0.0, pz + 0.0); pn.rotation_euler = (0, 0.15*max(0, u), 0)
        else:
            k = t - T_HIT
            pn.location = (lerp(0, -2.1, eout(k/0.35)), 0.7, max(0, 1.3*math.sin(min(k, 0.35)/0.35*math.pi)) if k < 0.35 else 0)
            pn.rotation_euler = (0, -0.25*math.exp(-k*6)*math.cos(k*20), 0)
        flat = T_HIT <= t < TL
        up = ease((t - TL) / 0.25)
        sz = 0.5 if flat else lerp(0.5, 1.0, back(up)) if t >= TL else 1.0
        x = 0.0 if t < TV else lerp(0, 3.4, ease((t - TV) / 1.3))
        walk = t > TV
        ex = "neutral" if t < TP else "shock" if t < T_HIT else "dizzy" if t < TL + 0.2 else "happy"
        arms = (8, 8)
        if T_HIT - 0.4 < t < T_HIT: arms = (150, 150)
        if TA <= t < TV: arms = (8, (150, 40))            # mão no boné
        if walk: arms = (14 + math.sin(t*12)*10, 14 - math.sin(t*12)*10)
        leo.pose(t, loc=(x, 0, abs(math.sin(t*12))*0.06 if walk else 0), s=1.0, expr=[[0, ex]], arms=arms,
                 look=(0 if not walk else 25, 10 if t < T_HIT and t > TP else 0), tilt=-8 if TA <= t < TV else 0)
        leo.L.root.scale = (1/math.sqrt(sz), 1/math.sqrt(sz), sz) if sz != 1.0 else (1, 1, 1)
        puff.at((0, -0.3, 0.25), 0.38, (t - T_HIT) / 0.55)
        place_ring(dz, t, (0, 0, 1.15 if flat else 2.05), 0.45, T_HIT < t < TA)
        rig.apply(t)
    return frame, rig

# ================================================================== S1 — no começo é incrível
def build_s1(sc, W):
    setup_render("#F2D0B4")
    clk, rings = OLD.bedroom()
    for o in rings: o.hide_render = True
    # TV + videogame à esquerda
    cube("tvstand", "#8E5A34", (-2.6, 0.8, 0.35), (1.6, 0.7, 0.7), bevel=0.04)
    cube("tv", "#1E1B2E", (-2.6, 0.85, 1.35), (1.5, 0.12, 0.95), bevel=0.04)
    scr = cube("tvscr", "#59C3FF", (-2.6, 0.78, 1.35), (1.36, 0.02, 0.82), bevel=0)
    cube("tvhill", "#5FBF5A", (-2.6, 0.765, 1.08), (1.36, 0.01, 0.28), bevel=0)
    hero = cube("tvhero", "#FF5A5F", (-2.9, 0.76, 1.3), (0.12, 0.01, 0.18), bevel=0)
    win = text3d("tvwin", "FIM!", "#FFD93D", (-2.6, 0.75, 1.55), 0.28, extrude=0.01)
    # pilha de livros alta à direita
    rr = random.Random(5); cols = ["#E63946", "#457B9D", "#F4A259", "#2A9D8F", "#8E7DBE", "#FFD93D"]
    for k in range(16):
        cube(f"book{k}", cols[k % 6], (2.4 + rr.uniform(-0.06, 0.06), 0.4, 0.1 + k*0.2), (0.85, 0.6, 0.18), bevel=0.02,
             rot=(0, 0, rr.uniform(-0.1, 0.1)))
    # teclado (piano) na frente do Léo
    kb = empty("kb", (0, -0.55, 0))
    cube("kbtop", "#1E1B2E", (0, 0, 0.85), (1.3, 0.38, 0.12), kb, bevel=0.03)
    cube("kbkeys", "#FFFFFF", (0, -0.08, 0.92), (1.15, 0.18, 0.03), kb, bevel=0)
    for sx in (-1, 1): cube(f"kbleg{sx}", "#3A3A48", (sx*0.5, 0, 0.42), (0.05, 0.05, 0.84), kb, bevel=0)
    notes = [text3d(f"note{k}", "♪", "#1E1B2E", (0, 0, -50), 0.35, extrude=0.03) for k in range(3)]
    cam = camera(40); leo = LeoCtl("leo")
    TJ, TLv, TP = W("jogos"), W("livros"), W("piano")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.3, 3.3),
             Shot(TJ - 0.1, -2.15, 1.35, 3.0, roll=-6),
             Shot(TLv - 0.1, 1.95, 1.75, 3.9, roll=6),
             Shot(TP - 0.1, 0, 1.2, 2.7, roll=-5)]
    rig = Rig(cam, shots, D, enter=(-1.0, 0, 0.45, 7), exit=(0, -0.3, -0.4, 7))
    def frame(t):
        kb.hide_render = False
        for o in kb.children: o.hide_render = t < TP - 0.1
        if t < TJ - 0.1:
            leo.pose(t, loc=(0, 0, 0), expr=[[0, "happy"]], arms=(150 + math.sin(t*8)*15, 150 - math.sin(t*8)*15))
        elif t < TLv - 0.1:     # jogando: de frente pra TV, braços pra frente
            leo.pose(t, loc=(-1.75, -0.6, 0), expr=[[0, "neutral"], [TJ + 0.5, "happy"]], arms=((20, 60), (20, 60)), look=(-30, 0))
        elif t < TP - 0.1:      # lendo: ao lado da pilha, um livro na mão
            leo.pose(t, loc=(1.5, -0.3, 0), expr=[[0, "neutral"], [TLv + 0.5, "happy"]], arms=((10, 70), (10, 70)), look=(0, 14))
        else:                   # tocando piano
            leo.pose(t, loc=(0, 0, 0), expr=[[0, "happy"]], arms=((12, 55 + math.sin(t*20)*8), (12, 55 - math.sin(t*20)*8)), look=(0, 8),
                     tilt=math.sin(t*5)*6)
        hero.location.x = -2.9 + ((t*0.5) % 0.6)
        win.hide_render = not (TJ + 0.6 < t < TLv)
        for k, n in enumerate(notes):
            on = t > TP; u = (t*0.7 + k/3) % 1
            n.hide_render = not on
            n.location = (-0.5 + k*0.5 + math.sin(u*7)*0.1, -0.7, 1.2 + u*1.4); n.rotation_euler = (math.pi/2, 0, math.sin(u*5)*0.4)
        rig.apply(t)
    return frame, rig

# ================================================================== S2 — 150 anos
def living(wall="#C9B8E8", stripe="#BBA8DE"):
    cube("floor", "#C98A4B", (0, 0, -0.05), (16, 12, 0.1), bevel=0)
    for k in range(-8, 9): cube(f"plank{k}", "#B97A3E", (k*0.9, 0, 0.0), (0.03, 12, 0.012), bevel=0)
    cube("wall", wall, (0, 2.6, 4), (16, 0.15, 8.2), bevel=0)
    for k in range(-17, 18): cube(f"stripe{k}", stripe, (k*0.45, 2.52, 4), (0.16, 0.01, 8.2), bevel=0)
    cube("base", "#FFFFFF", (0, 2.5, 0.08), (16, 0.06, 0.16), bevel=0.01)
    cyl("rug", "#E86A5B", (0, -0.4, 0.01), 2.3, 0.02, bevel=0.01, verts=64).scale = (1, 0.55, 1)

def sofa(x=0, color="#D88C3A", dark="#B8702A"):
    cube("sofaback", color, (x, 1.7, 1.0), (3.4, 0.6, 1.5), bevel=0.2)
    cube("sofaseat", dark, (x, 1.05, 0.4), (3.2, 1.3, 0.55), bevel=0.15)
    cube("sofacush", color, (x, 1.0, 0.75), (3.0, 1.2, 0.25), bevel=0.12)
    for sx in (-1, 1): cube(f"sofaarm{sx}", color, (x + sx*1.75, 1.15, 0.75), (0.45, 1.6, 1.05), bevel=0.18)

def friend(name, x, z, color, hair):
    g = empty(name, (x, 2.33, z))
    sphere(name+"h", "#E3A97E", (0, 0, 0.18), 0.15, (1, 0.4, 1), g, sub=1)
    sphere(name+"hr", hair, (0, 0.02, 0.27), 0.15, (1, 0.4, 0.6), g, sub=1)
    sphere(name+"b", color, (0, 0, -0.12), 0.13, (1, 0.4, 1.3), g, sub=1)
    for sx in (-1, 1): sphere(name+f"e{sx}", INKC, (sx*0.05, -0.06, 0.2), 0.018, sub=0, parent=g, seg=8)
    arc_tube(name+"m", INKC, (0, -0.065, 0.13), 0.04, 0.008, math.radians(200), math.radians(340), g)
    return g

def build_s2(sc, W):
    setup_render("#C9B8E8")
    living(); sofa()
    # foto dos amigos na parede (em cima — empilhado na vertical)
    cube("frame", "#7A4A2A", (0, 2.42, 3.25), (2.0, 0.08, 1.4), bevel=0.04)
    cube("photo", "#FFF3D6", (0, 2.37, 3.25), (1.75, 0.02, 1.15), bevel=0)
    for i, (c, h) in enumerate([("#E63946", "#3B2418"), ("#2A9D8F", "#D9A441"), ("#FFC93C", "#3B2418"), ("#457B9D", "#1E1B2E")]):
        friend(f"fr{i}", -0.6 + i*0.4, 3.2, c, h)
    # mesa de centro + bolo 150
    cube("table", "#8E5A34", (0, -0.9, 0.42), (1.8, 0.9, 0.12), bevel=0.03)
    for sx in (-1, 1):
        for sy in (-1, 1): cube(f"tl{sx}{sy}", "#6E4224", (sx*0.75, -0.9+sy*0.32, 0.18), (0.08, 0.08, 0.36), bevel=0)
    cake = empty("cake", (0, -0.9, 0.48))
    cyl("cake1", "#F6B8C8", (0, 0, 0.18), 0.48, 0.36, cake, bevel=0.04)
    cyl("cakeicing", "#FFFFFF", (0, 0, 0.37), 0.5, 0.06, cake, bevel=0.03)
    text3d("c150", "150", "#E63946", (0, -0.5, 0.18), 0.28, cake, extrude=0.03)
    flames = []
    for k in range(7):
        a = k/7*2*math.pi
        cyl(f"cand{k}", "#7FB2FF", (math.cos(a)*0.32, math.sin(a)*0.25, 0.5), 0.025, 0.22, cake, bevel=0)
        flames.append(sphere(f"fl{k}", "#FFB703", (math.cos(a)*0.32, math.sin(a)*0.25, 0.66), 0.04, (1, 1, 1.6), cake, sub=1))
    hat = empty("hat", (0, 0, 0))
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.45, location=(0, 0, 0)); c = bpy.context.object; c.parent = hat; setmat(c, "#4FC08D")
    sphere("hatpom", "#FFD93D", (0, 0, 0.25), 0.06, parent=hat, sub=1)
    cam = camera(40); leo = LeoCtl("leo")
    TV, TA, TT = W("velha"), W("amigos"), W("tempo")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.0, 2.0),                    # abre no bolo
             Shot(W("você") - 0.05, 0, 1.4, 2.9, roll=6),
             Shot(TV, 0, 1.7, 1.95, roll=-4),        # close: "a mais velha do mundo"
             Shot(TA - 0.05, 0, 3.15, 1.9, roll=6),   # foto dos amigos
             Shot(TT - 0.1, 0, 1.65, 1.9, roll=-5)]    # close triste
    rig = Rig(cam, shots, D, enter=(0.8, 0.4, 0.5, -8), exit=(0, 0.5, -0.4, 6))
    def frame(t):
        leo.pose(t, loc=(0, 0.45, 0.25), expr=[[0, "happy"], [TA, "worried"]], arms=(14, 14), look=(0, 0 if t < TA else 10))
        hp = leo.L.head.matrix_world @ Vector((0, 0, 0.9))
        bpy.context.view_layer.update()
        hat.location = leo.L.head.matrix_world @ Vector((0.05, 0.0, 0.92)); hat.rotation_euler = (0, 0.25, 0)
        for k, f in enumerate(flames): f.scale = (1, 1, 1.6 + math.sin(t*14 + k)*0.3)
        rig.apply(t)
    return frame, rig

# ================================================================== S3 — a cidade virou floresta
def tree(name, x, y, h, r, rr):
    cyl(name+"t", "#7A4A2A", (x, y, h/2), 0.12*r, h, bevel=0.01)
    for k in range(4):
        sphere(name+f"c{k}", rr.choice(["#3E9B4F", "#4FB25E", "#2F8A45"]), (x + rr.uniform(-0.4, 0.4)*r, y, h + rr.uniform(-0.1, 0.5)*r), (0.55 + rr.uniform(0, 0.3))*r, sub=1)

def build_s3(sc, W):
    setup_render("#BFE6C4")
    cube("ground", "#5DA55A", (0, 2, -0.05), (30, 14, 0.1), bevel=0)
    rr = random.Random(3)
    # prédios em ruína, cobertos de mato (atrás, em cima no quadro)
    for i, (x, h) in enumerate([(-3.2, 6.5), (-1.0, 8.5), (1.6, 7.2), (3.8, 5.6)]):
        cube(f"ruin{i}", "#9AA0A8", (x, 4.5, h/2), (1.8, 1.4, h), bevel=0.05, rot=(0, rr.uniform(-0.06, 0.06), 0))
        for j in range(int(h/1.2)):
            cube(f"rw{i}{j}", "#4A5058", (x - 0.4, 3.78, 0.9 + j*1.2), (0.45, 0.05, 0.6), bevel=0)
            cube(f"rw2{i}{j}", "#4A5058", (x + 0.4, 3.78, 0.9 + j*1.2), (0.45, 0.05, 0.6), bevel=0)
        for j in range(7):
            sphere(f"vine{i}{j}", rr.choice(["#3E9B4F", "#4FB25E"]), (x + rr.uniform(-0.9, 0.9), 3.7, rr.uniform(0.3, h)), rr.uniform(0.25, 0.5), (1, 0.4, 1), sub=1)
        sphere(f"top{i}", "#3E9B4F", (x, 4.5, h + 0.1), 0.9, (1.1, 0.8, 0.45), sub=1)
    for k in range(9):
        tree(f"tr{k}", rr.uniform(-5, 5), rr.uniform(1.4, 3.0), rr.uniform(2.0, 3.6), rr.uniform(0.8, 1.3), rr)
    for k in range(18):
        sphere(f"bush{k}", rr.choice(["#3E9B4F", "#4FB25E", "#6CC56A"]), (rr.uniform(-6, 6), rr.uniform(0.6, 1.4), 0.1), rr.uniform(0.3, 0.6), (1, 0.7, 0.7), sub=1)
    # placa velha caída "WI-FI GRÁTIS"
    sg = empty("sign", (-1.6, 0.3, 0))
    cyl("signp", "#5B5F66", (0, 0, 0.7), 0.04, 1.4, sg, bevel=0)
    cube("signb", "#2E6FB7", (0, -0.02, 1.35), (1.2, 0.06, 0.5), sg, bevel=0.03)
    text3d("signt", "WI-FI", "#FFFFFF", (0, -0.07, 1.35), 0.26, sg, extrude=0.01)
    sg.rotation_euler = (0, 0.25, 0)
    # celular na mão do Léo
    ph = cube("phone", "#1E1B2E", (0, 0, -50), (0.16, 0.03, 0.28), bevel=0.02)
    nos = text3d("nosig", "✕", "#E63946", (0, 0, -50), 0.16, extrude=0.01)
    cam = camera(40); leo = LeoCtl("leo")
    TF, TN, TI = W("floresta"), W("ninguém"), W("internet")
    D = sc["dur"]
    shots = [Shot(0, 0, 3.4, 7.5, push=0.07),
             Shot(TF - 0.05, -0.4, 1.4, 3.6, roll=-6),
             Shot(TN, 0.25, 1.6, 2.4, roll=5),
             Shot(TI, 0.2, 1.7, 1.8, kind="cut")]
    rig = Rig(cam, shots, D, enter=(0, 0.6, 0.45, 7), exit=(-0.8, 0, -0.4, -6))
    def frame(t):
        up = t > TN - 0.1
        arms = (10, (150, 30)) if up else (10, 10)
        leo.pose(t, loc=(0.2, 0, 0), expr=[[0, "neutral"], [TN, "worried"], [TI, "shock"]], arms=arms, look=(10 if up else 0, -12 if up else 0))
        bpy.context.view_layer.update()
        hand = leo.L.arm[1].matrix_world @ Vector((0.06, -0.05, -0.43))
        ph.location = hand if up else (0, 0, -50)
        nos.location = (hand.x, hand.y - 0.05, hand.z + 0.3 + math.sin(t*8)*0.02) if up else (0, 0, -50)
        rig.apply(t)
    return frame, rig

# ================================================================== S4 — os continentes se juntam
def build_s4(sc, W):
    setup_render("#141A3D")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.25
    stars(90, 4)
    R = 2.4; C0 = Vector((0, 0.6, -R + 0.02))
    sphere("planet", "#3D8BD9", tuple(C0), R, sub=2, seg=48)
    sphere("atmo", "#7FC4FF", tuple(C0 + Vector((0, 0.3, 0))), R*1.04, (1, 0.05, 1), sub=1)
    # continentes: manchas no hemisfério de frente, que deslizam para o centro
    conts = []
    rr = random.Random(8)
    for i, (a0, color) in enumerate([(-1.2, "#5FBF5A"), (1.1, "#7AC96A"), (-0.55, "#4FAF4F"), (0.6, "#6DBE5E")]):
        g = empty(f"cont{i}", tuple(C0))
        for k in range(5):
            sphere(f"cb{i}{k}", color, (rr.uniform(-0.25, 0.25), -R*0.98, rr.uniform(-0.25, 0.25)), rr.uniform(0.28, 0.42), (1, 0.18, 1), g, sub=1)
        conts.append((g, a0, 0.7 + i*0.15))
    flag_br = empty("fbr", (0, 0, -50)); flag_af = empty("faf", (0, 0, -50))
    for f, col in ((flag_br, "#2EA44F"), (flag_af, "#E9A23B")):
        cyl(f.name+"p", "#FFFFFF", (0, 0, 0.35), 0.02, 0.7, f, bevel=0)
        cube(f.name+"f", col, (0.17, 0, 0.6), (0.32, 0.02, 0.22), f, bevel=0)
    tbr = text3d("tbr", "BRASIL", "#FFFFFF", (0, 0, -50), 0.2, extrude=0.01)
    taf = text3d("taf", "ÁFRICA", "#FFFFFF", (0, 0, -50), 0.2, extrude=0.01)
    cam = camera(40); leo = LeoCtl("leo")
    TJ, TA, TB, TAf = W("juntam"), W("pé"), W("Brasil"), W("África")
    D = sc["dur"]
    shots = [Shot(0, 0, -0.4, 6.8, push=0.05),
             Shot(TJ, 0, -0.1, 5.4, kind="slow", dur=0.6),
             Shot(TA - 0.05, 0, 1.2, 2.6, roll=-6),
             Shot(TAf - 0.1, 0, 0.9, 3.4, roll=5)]
    rig = Rig(cam, shots, D, enter=(0, -0.8, 0.5, -7), exit=(0, 0.6, -0.4, 7))
    def frame(t):
        m = ease((t - TJ + 0.6) / 1.6)
        for g, a0, sp in conts:
            a = lerp(a0, a0*0.18, m)
            g.rotation_euler = (0, a, 0)
        walk = t > TA - 0.1
        leo.pose(t, loc=(0, 0, abs(math.sin(t*10))*0.05 if walk else 0), expr=[[0, "neutral"], [TJ, "shock"], [TA, "happy"]],
                 arms=((14 + math.sin(t*10)*14, 14 - math.sin(t*10)*14) if walk else (10, 10)), look=(20 if walk else 0, 0))
        on = t > TB - 0.15
        flag_br.location = (-0.75, 0.1, -0.05) if on else (0, 0, -50); flag_br.rotation_euler = (0, -0.35, 0)
        flag_af.location = (0.75, 0.1, -0.05) if t > TAf - 0.15 else (0, 0, -50); flag_af.rotation_euler = (0, 0.35, 0)
        tbr.location = (-0.75, -0.1, 0.9) if on else (0, 0, -50)
        taf.location = (0.8, -0.1, 0.9) if t > TAf - 0.15 else (0, 0, -50)
        rig.apply(t)
    return frame, rig

# ================================================================== S5 — os oceanos evaporam
def build_s5(sc, W):
    setup_render("#FFC879")
    cube("sand", "#F2D29B", (0, 0, -0.05), (30, 6, 0.1), bevel=0)
    sea = cube("sea", "#2FA7C9", (0, 4.5, -0.1), (30, 6, 0.1), bevel=0)
    cube("shore", "#FFFFFF", (0, 1.5, 0.0), (30, 0.12, 0.02), bevel=0)
    sun = sphere("sun", "#FFFBE6", (1.8, 12, 7.5), 1.6, (1, 0.1, 1), sub=1)
    halo = sphere("sunhalo", "#FFE9A6", (1.8, 12.2, 7.5), 2.4, (1, 0.05, 1), sub=1)
    rock = sphere("rock", "#7E7A8C", (0.2, 0.3, 0.15), 0.8, (1.3, 0.9, 0.55), sub=2)
    steam = []
    rr = random.Random(6)
    for k in range(9):
        col = [sphere(f"stm{k}{j}", "#FFFFFF", (0, 0, -50), 0.3, sub=1) for j in range(5)]
        steam.append((rr.uniform(-4, 4), rr.uniform(2.5, 5.5), rr.uniform(0, 1), col))
    bottle = empty("bottle", (0, 0, -50))
    cyl("btl", "#FF8C42", (0, 0, 0), 0.12, 0.42, bottle, bevel=0.03)
    cyl("btlcap", "#FFFFFF", (0, 0, 0.26), 0.07, 0.1, bottle, bevel=0.01)
    text3d("btlt", "1000", "#FFFFFF", (0, -0.13, 0.0), 0.09, bottle, extrude=0.005)
    sw = [sweat_drop(f"sw{k}") for k in range(3)]
    cam = camera(40); leo = LeoCtl("leo")
    TF, TE, TP = W("forte"), W("evaporam"), W("protetor")
    D = sc["dur"]
    shots = [Shot(0, 0.8, 3.0, 6.4),
             Shot(TF - 0.1, 0.3, 1.7, 2.9, roll=5),
             Shot(TE - 0.1, 0, 2.2, 5.0, roll=-6),
             Shot(TP - 0.05, 0.25, 1.9, 2.1, roll=5)]
    rig = Rig(cam, shots, D, enter=(0, 0.8, 0.5, 8), exit=(-1.0, 0, -0.4, -6))
    def frame(t):
        hot = ease((t - TF) / 2.5)
        sea.scale.z = 1; sea.location.z = lerp(-0.1, -0.4, ease((t - TE) / 1.5))
        halo.scale = (1 + hot*0.4 + math.sin(t*4)*0.03,)*1 + (0.05, 1 + hot*0.4 + math.sin(t*4)*0.03)
        for x, y, ph, col in steam:
            on = t > TE - 0.3
            for j, s in enumerate(col):
                u = (t*0.6 + ph + j/5) % 1
                s.hide_render = not on
                s.location = (x + math.sin(u*5 + j)*0.15, y, -0.1 + u*3.2); r = 0.2 + u*0.45
                s.scale = (r/0.3,)*3
        hand = t > TP - 0.1
        leo.pose(t, loc=(0.2, 0.2, 0.55), expr=[[0, "neutral"], [TF, "tired"], [TE, "shock"], [TP, "worried"]],
                 arms=(10, ((60, 70) if hand else 10)), look=(0, 0))
        bpy.context.view_layer.update()
        h = leo.L.arm[1].matrix_world @ Vector((0.06, -0.08, -0.43))
        bottle.location = h if hand else (0, 0, -50); bottle.rotation_euler = (0, -0.5 if hand else 0, 0)
        head = leo.L.head.matrix_world @ Vector((0, 0, 0.4))
        for k, s in enumerate(sw):
            on = t > TF + 0.3; u = (t*1.3 + k/3) % 1
            s.hide_render = not on
            s.location = (head.x + (-0.4 if k % 2 else 0.42), head.y - 0.3, head.z + 0.25 - u*0.5)
        rig.apply(t)
    return frame, rig

# ================================================================== S6 — o Sol engole a Terra
def build_s6(sc, W):
    setup_render("#120A1E")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.2
    stars(110, 6)
    sun = sphere("redsun", "#FF5A2A", (-1.2, 10, 6.5), 3.0, (1, 0.25, 1), sub=2, seg=48)
    glow = sphere("redglow", "#B83A2A", (-1.2, 10.5, 6.5), 4.0, (1, 0.05, 1), sub=1)
    earth = empty("earth", (2.2, 6, 5.2))
    sphere("earthb", "#3D8BD9", (0, 0, 0), 0.32, parent=earth, sub=1)
    sphere("earthg", "#5FBF5A", (0.08, -0.22, 0.08), 0.17, (1, 0.5, 0.9), earth, sub=1)
    burst = [sphere(f"bu{k}", "#FFD166", (0, 0, -50), 0.1, sub=0, seg=8) for k in range(8)]
    cam = camera(40); leo = LeoCtl("leo")
    TG, TE, TB = W("gigante"), W("engole"), W("boiando")
    D = sc["dur"]
    shots = [Shot(0, 0.3, 4.4, 7.0, push=0.05),
             Shot(TG - 0.1, 0, 4.8, 8.6, roll=-5),
             Shot(TE + 0.25, 1.5, 4.5, 3.2, roll=6, shake=0.06),
             Shot(TB - 0.1, 0, 1.0, 2.4, roll=-6)]
    rig = Rig(cam, shots, D, enter=(0, -0.8, 0.5, -7), exit=(0, 0, -0.45, 8))
    def frame(t):
        g = ease((t - TG + 0.2) / 1.0)
        s = lerp(0.8, 1.35, g)
        sun.scale = (s, 0.25, s); glow.scale = (s*1.1 + math.sin(t*3)*0.03, 0.05, s*1.1 + math.sin(t*3)*0.03)
        sw = ease((t - TE) / 0.5)
        earth.location = (lerp(2.2, 1.6, sw), lerp(6, 9.5, sw), 5.2)
        earth.scale = (1 - sw*0.9,)*3
        for k, b in enumerate(burst):
            u = (t - TE - 0.45) / 0.5
            b.hide_render = not (0 < u < 1)
            a = k/8*2*math.pi
            b.location = (1.6 + math.cos(a)*u*0.9, 6.0, 5.2 + math.sin(a)*u*0.9)
        leo.pose(t, loc=(math.sin(t*0.8)*0.15, 0, 0.1 + math.sin(t*1.4)*0.12), rotz=0, roty=math.sin(t*0.9)*0.35 + t*0.08,
                 expr=[[0, "shock"], [TB, "worried"]], arms=(90 + math.sin(t*3)*15, 90 - math.sin(t*3)*15), look=(0, -15 if t < TB else 0))
        rig.apply(t)
    return frame, rig

# ================================================================== S7 — a última estrela se apaga
def build_s7(sc, W):
    setup_render("#0B0A1C")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.2
    st = stars(140, 7)
    last = sphere("last", "#FFE58A", (0.6, 8, 5.4), 0.35, sub=1)
    lhalo = sphere("lhalo", "#FFD166", (0.6, 8.2, 5.4), 0.7, (1, 0.05, 1), sub=1)
    ast = sphere("ast", "#6E6A7C", (0, 0.2, -0.15), 0.85, (1.4, 1, 0.55), sub=2)
    for k in range(5):
        a = k*1.3
        sphere(f"crater{k}", "#5A566A", (math.cos(a)*0.7, -0.35, 0.05 + math.sin(a)*0.12), 0.12, (1, 0.4, 0.6), sub=1)
    lant = empty("lant", (0, 0, -50))
    cyl("lantb", "#FFD93D", (0, 0, 0), 0.06, 0.3, lant, rot=(math.pi/2, 0, 0), bevel=0.01)
    bpy.ops.mesh.primitive_cone_add(radius1=0.32, radius2=0.05, depth=1.3, location=(0, 0, 0)); beam = bpy.context.object
    beam.parent = lant; beam.location = (0, 0, 0.8); setmat(beam, "#FFF6C8")
    cam = camera(40); leo = LeoCtl("leo")
    TU, TA, TL, TE = W("última"), W("apaga"), W("lanterna"), W("esperando")
    D = sc["dur"]
    shots = [Shot(0, 0, 3.0, 6.6, push=0.05),
             Shot(TU - 0.05, 0.6, 5.3, 2.0, roll=-5),
             Shot(TL - 0.1, 0.25, 1.5, 3.1, roll=6),
             Shot(TE - 0.05, 0.1, 1.75, 2.0, roll=-4)]
    rig = Rig(cam, shots, D, enter=(0, 0.8, 0.5, 7), exit=(0, 0, -0.5, -7))
    rr = random.Random(1); offs = [rr.uniform(0.0, TU) for _ in st]
    def frame(t):
        for o, toff in zip(st, offs): o.hide_render = t > toff
        k = cl((t - TA) / 0.6)
        sz = lerp(1, 0.05, ease(k)) * (1 + 0.15*math.sin(t*30)*(1 - k))
        last.scale = (sz,)*3; last.hide_render = k >= 1
        lhalo.scale = (sz, 0.05, sz); lhalo.hide_render = k >= 1
        hold = t > TL - 0.15
        leo.pose(t, loc=(0, 0, 0.32), expr=[[0, "neutral"], [TA, "shock"], [TL, "neutral"], [TE, "tired"]],
                 arms=(10, ((40, 60) if hold else 10)), look=(0, -18 if TU < t < TL else 0))
        bpy.context.view_layer.update()
        h = leo.L.arm[1].matrix_world @ Vector((0.06, -0.08, -0.43))
        lant.location = h if hold else (0, 0, -50)
        lant.rotation_euler = (0, math.radians(40 + math.sin(t*1.5)*15), 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S8 — buracos negros somem
def build_s8(sc, W):
    setup_render("#090818")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.2
    stars(40, 8, r=(0.015, 0.03))
    holes = []
    for i, (x, z, r) in enumerate([(-1.4, 5.0, 0.7), (1.3, 5.6, 0.95), (0.2, 4.0, 0.5)]):
        g = empty(f"bh{i}", (x, 4, z))
        sphere(f"bhc{i}", "#000000", (0, 0, 0), r, parent=g, sub=1)
        o = torus(f"bhr{i}", "#FF8A3D", (0, 0, 0), r*1.35, r*0.09, g, rot=(math.radians(75), 0, math.radians(15)))
        sphere(f"bhg{i}", "#5A2A1A", (0, 0.4, 0), r*1.5, (1, 0.05, 1), g, sub=1)
        holes.append((g, i))
    num = text3d("num", "1 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000",
                 "#FFFFFF", (0, 0, -50), 0.42, extrude=0.02)
    num.data.align_x = 'LEFT'
    zs = zzz()
    cam = camera(40); leo = LeoCtl("leo")
    TS, TN, TZ = W("somem"), W("número"), W("zeros")
    D = sc["dur"]
    shots = [Shot(0, 0, 3.6, 6.2, push=0.05),
             Shot(TS - 0.1, 0, 4.9, 4.0, roll=-6),
             Shot(TN - 0.1, 0, 3.0, 4.6, roll=5),
             Shot(TZ - 0.05, 0, 1.55, 2.0, kind="cut", shake=0.04)]
    rig = Rig(cam, shots, D, enter=(0, 0.8, 0.5, -7), exit=(0, 0, -0.5, 8))
    def frame(t):
        for g, i in holes:
            k = cl((t - TS - i*0.25) / 0.7)
            s = lerp(1, 0.0, ease(k)) * (1 + 0.08*math.sin(t*20 + i)*(k > 0))
            g.scale = (max(s, 0.001),)*3; g.hide_render = k >= 1
            for c in g.children: c.hide_render = k >= 1
            g.rotation_euler = (0, 0, t*0.2*(i + 1))
        on = t > TN - 0.2
        num.location = (lerp(-2.0, -14.0, cl((t - TN)/2.6)), -0.5, 2.9) if on else (0, 0, -50)
        num.rotation_euler = (math.pi/2, 0, 0)
        sleep = t < TZ
        leo.pose(t, loc=(0, 0, 0.1 + math.sin(t*1.2)*0.08), roty=math.sin(t*0.7)*0.15, expr=[[0, "sleep"], [TZ, "shock"]],
                 arms=(30, 30) if sleep else (150, 150), look=(0, 8 if sleep else -6))
        place_zzz(zs, t, (0.25, -0.3, 2.0), sleep)
        rig.apply(t)
    return frame, rig

# ================================================================== S9 — no escuro, pra sempre
def build_s9(sc, W):
    setup_render("#05040C")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.15
    spot = sphere("spot", "#1C1A3A", (0, 1.5, 1.0), 1.6, (1, 0.05, 1), sub=1)
    clk = empty("clock", (0, 0, -50))
    cyl("clkbody", "#2EC4B6", (0, 0, 0), 0.24, 0.16, clk, rot=(math.pi/2, 0, 0), bevel=0.03)
    cyl("clkface", "#FFFFFF", (0, -0.085, 0), 0.18, 0.02, clk, rot=(math.pi/2, 0, 0), bevel=0)
    for sx in (-1, 1): sphere(f"bell{sx}", "#FFD93D", (sx*0.15, 0, 0.22), 0.09, (1, 1, 0.7), clk, sub=1)
    cube("ch1", INKC, (0, -0.1, 0.05), (0.02, 0.01, 0.11), clk, bevel=0)
    cube("ch2", INKC, (0.04, -0.1, 0), (0.09, 0.01, 0.02), clk, bevel=0)
    xs = [cube(f"x{k}", "#E63946", (0, 0, -50), (0.7, 0.04, 0.08), bevel=0.02) for k in range(2)]
    cam = camera(40); leo = LeoCtl("leo")
    TS, TPm, TC = W("sobra"), W("Pelo"), W("acorda")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.2, 7.5, push=0.04),
             Shot(TS, 0, 1.2, 3.4, kind="slow", dur=1.4, push=0.07),
             Shot(TPm - 0.05, 0, 1.6, 2.1, roll=6),
             Shot(TC - 0.1, 0.35, 2.4, 2.4, roll=-5)]
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.6, 6), exit=(0, 0, -0.5, -7))
    def frame(t):
        leo.pose(t, loc=(0, 0, 0), expr=[[0, "neutral"], [W("sempre"), "tired"], [TPm, "happy"]],
                 arms=(10, 10) if t < TPm else (150, 150), look=(0, 0 if t < TC else -10))
        spot.scale = (1 + math.sin(t*2)*0.03, 0.05, 1 + math.sin(t*2)*0.03)
        on = t > TC - 0.15
        clk.location = (0.35 + (t - TC)*0.2, -0.2, 2.6 + (t - TC)*0.15) if on else (0, 0, -50)
        clk.rotation_euler = (0, math.sin(t*40)*0.08, 0)
        for k, x in enumerate(xs):
            x.location = (clk.location.x, -0.4, clk.location.z) if t > TC + 0.25 else (0, 0, -50)
            x.rotation_euler = (0, math.radians(45 if k else -45), 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S10 — escolha
def build_s10(sc, W):
    setup_render("#0B0A1C")
    sc_ = bpy.context.scene; sc_.display.shading.shadow_intensity = 0.2
    stars(60, 10, r=(0.015, 0.04))
    spot = sphere("spot", "#262350", (0, 1.5, 0.9), 1.5, (1, 0.05, 1), sub=1)
    q = text3d("q", "?", "#FFD93D", (0.7, -0.2, 2.0), 0.5, extrude=0.04)
    cam = camera(40); leo = LeoCtl("leo")
    D = sc["dur"]
    shots = [Shot(0, 0, 0.95, 3.0, push=0.035)]
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, -7), exit=(0, 0, 0, 0), exit_t=0.01)
    def frame(t):
        leo.pose(t, loc=(0, 0, 0), expr=[[0, "neutral"]], arms=(10, (40, 90)), look=(-8, -6), tilt=8)
        q.location.z = 2.0 + math.sin(t*4)*0.06; q.rotation_euler = (math.pi/2, 0, math.sin(t*3)*0.2)
        rig.apply(t)
    return frame, rig

BUILD = {f"s{i}": globals()[f"build_s{i}"] for i in range(11)}
