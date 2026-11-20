"""Cenas 3D de "E se você acordasse com um rabo?" — personagem: Bia (blender/personagens.py).
Mesma gramática de câmera do canal (blender/camera.py, ESTILO.md). Cada build_sN devolve (frame, rig).
Bia com s=1 tem ~2,1 de altura (cabeça em z≈1.6). Close: h≈1.9 · médio: 2.6 · corpo inteiro: 3.4.
"""
import bpy, math, random, os, sys
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "blender"))
from lib import *
from look import *
from camera import Rig, Shot
from personagens import BiaCtl
import scenes as OLD

def hearts(n, color="#FF4F7B"):
    return [text3d(f"heart{k}", "♥", color, (0, 0, -50), 0.32, extrude=0.04) for k in range(n)]

def place_hearts(hs, t, base, on, spread=0.6):
    for k, h in enumerate(hs):
        if not on: h.hide_render = True; continue
        u = (t*0.9 + k/len(hs)) % 1
        h.hide_render = False
        h.location = (base[0] + (k - len(hs)/2 + 0.5)*spread*0.5 + math.sin(u*6 + k)*0.08, base[1], base[2] + u*1.1)
        s = 0.6 + 0.6*math.sin(u*math.pi); h.scale = (s, s, s)

def zzz():
    return [text3d(f"z{k}", "Z", "#FFFFFF", (0, 0, -50), 0.16+k*0.07, extrude=0.03) for k in range(3)]

def place_zzz(zs, t, base, on):
    for k, z in enumerate(zs):
        if not on: z.hide_render = True; continue
        u = (t*0.8 + k/3) % 1
        z.hide_render = False
        z.location = (base[0] + 0.15 + u*0.5, base[1], base[2] + u*0.8)

def bang(name, color="#FFD93D"):
    return text3d(name, "!", color, (0, 0, -50), 0.7, extrude=0.05)

# ================================================================== S0 — acorda com um rabo (noite)
def build_s0(sc, W):
    setup_render("#1F2550")
    cube("floor", "#5A4A7A", (0, 0, -0.05), (14, 12, 0.1), bevel=0)
    cube("wall", "#2E3A78", (0, 2.6, 3), (14, 0.15, 6.2), bevel=0)
    for k in range(-14, 15): cube(f"stripe{k}", "#34418A", (k*0.45, 2.52, 3), (0.18, 0.01, 6.2), bevel=0)
    cube("winframe", "#C9D2F2", (-1.4, 2.48, 3.2), (1.6, 0.12, 1.8), bevel=0.04)
    cube("winsky", "#101640", (-1.4, 2.42, 3.2), (1.4, 0.02, 1.6), bevel=0)
    sphere("moon", "#FFF3B8", (-1.15, 2.4, 3.5), 0.33, (1, 0.05, 1), sub=1)
    sphere("moonbite", "#101640", (-1.0, 2.39, 3.6), 0.3, (1, 0.05, 1), sub=1)
    for k in range(5): sphere(f"wst{k}", "#FFFFFF", (-1.9 + k*0.22, 2.39, 2.7 + (k % 2)*0.5), 0.03, sub=0, seg=6)
    cube("bedframe", "#6B4A8E", (1.4, 0.9, 0.35), (2.2, 3.0, 0.4), bevel=0.05)
    cube("headboard", "#6B4A8E", (1.4, 2.35, 0.95), (2.2, 0.15, 1.6), bevel=0.06)
    cube("mattress", "#E8E4F5", (1.4, 0.9, 0.62), (2.05, 2.8, 0.2), bevel=0.08)
    blanket = cube("blanket", "#FF8FB1", (1.4, 0.2, 0.8), (2.15, 1.7, 0.22), bevel=0.08)
    sphere("pillow", "#FFFFFF", (1.4, 1.9, 0.9), 0.45, (1.5, 0.6, 0.35), sub=2)
    cyl("rug", "#7D5BB0", (0, -0.6, 0.01), 1.6, 0.02, bevel=0.01, verts=64).scale = (1, 0.55, 1)
    cam = camera(40); bia = BiaCtl("bia", tail=True); puff = OLD.Puff(8); zs = zzz(); bg = bang("bang")
    TR, TA, TN = W("rabo"), W("aparece"), W("noite")
    D = sc["dur"]
    shots = [Shot(0, 1.2, 1.2, 3.3),                     # Bia dormindo sentada na cama
             Shot(TR - 0.05, -0.1, 1.0, 2.6, kind="cut", shake=0.06),   # POF! fora da cama, com rabo
             Shot(TA, 0.45, 0.75, 1.5, roll=-6),         # close no rabo
             Shot(W("nada"), -0.05, 1.65, 1.9, roll=5),  # close no rosto em choque
             Shot(TN - 0.05, -0.45, 2.2, 4.4, roll=-5)]   # abre: janela com a lua
    rig = Rig(cam, shots, D, enter=(0, 0.4, 0.5, 7), exit=(0.6, 0.0, -0.4, 7))
    L = bia.L
    def frame(t):
        if t < TR - 0.05:   # dormindo, sentada encostada na cabeceira (pernas somem no colchão)
            bia.pose(t, loc=(1.4, 1.3, 0.25), expr=[[0, "sleep"]], arms=(12, 12), look=(0, 6), tilt=10)
            for o in L.tail: o.hide_render = True
            for c in L.tail_base.children_recursive: c.hide_render = True
            place_zzz(zs, t, (1.6, 0.9, 2.0), True)
        else:
            bia.pose(t, loc=(0, 0, 0), rotz=math.radians(-25 if t < TA + 0.6 else 0),
                     expr=[[0, "shock"], [TN, "worried"]], arms=((150, 20), (150, 20)) if t < TA else (20, 20),
                     look=(-35 if TA <= t < W("nada") else 0, 8 if TA <= t < W("nada") else 0))
            for c in L.tail_base.children_recursive: c.hide_render = False
            grow = back(cl((t - TR + 0.05) / 0.3))
            L.tail_base.scale = (grow,)*3
            L.wag(t, amp=18, speed=7, curl=14)
            place_zzz(zs, t, (0, 0, 0), False)
        blanket.location.z = 0.8
        puff.at((0.2, 0.4, 0.6), 0.45, (t - TR + 0.05) / 0.5)
        bg.location = (0.55, -0.4, 2.15 + math.sin(t*20)*0.03) if TR - 0.05 < t < TA else (0, 0, -50)
        bg.rotation_euler = (math.pi/2, 0, -0.2)
        rig.apply(t)
    return frame, rig

# ================================================================== S1 — balança quando você fica feliz
def build_s1(sc, W):
    setup_render("#F2D0B4")
    clk, rings = OLD.bedroom()
    for o in rings: o.hide_render = True
    ice = empty("ice", (0, 0, -50))
    bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.28, location=(0, 0, 0)); c = bpy.context.object; c.parent = ice; c.rotation_euler = (math.pi, 0, 0); setmat(c, "#E0A15A")
    sphere("scoop1", "#FF9EC4", (0, 0, 0.17), 0.1, parent=ice, sub=1)
    sphere("scoop2", "#FFF1C1", (0, 0, 0.3), 0.09, parent=ice, sub=1)
    hs = hearts(5)
    cam = camera(40); bia = BiaCtl("bia", tail=True)
    TB, TF = W("balança"), W("feliz")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.25, 3.4),
             Shot(TB - 0.05, 0.4, 0.75, 1.6, roll=6),     # close no rabo balançando
             Shot(TF - 0.05, 0, 1.6, 1.95, roll=-5)]      # close no rosto feliz
    rig = Rig(cam, shots, D, enter=(-0.6, 0, 0.45, -7), exit=(0, 0.4, -0.4, -7))
    L = bia.L
    def frame(t):
        happy = t > 0.6
        spin = math.radians(-35) if TB - 0.05 <= t < TF - 0.05 else 0   # vira um pouco para mostrar o rabo
        bia.pose(t, loc=(0, 0, abs(math.sin(t*9))*0.04 if happy else 0), rotz=spin,
                 expr=[[0, "neutral"], [0.6, "happy"]], arms=((30, 60), 12), look=(0, 6), tilt=math.sin(t*4)*5)
        L.wag(t, amp=30 if happy else 6, speed=16 if happy else 3, curl=16)
        bpy.context.view_layer.update()
        ice.location = L.arm[-1].matrix_world @ Vector((-0.06, -0.06, -0.45))
        place_hearts(hs, t, (0.0, -0.4, 2.05), t > TF - 0.2)
        rig.apply(t)
    return frame, rig

# ================================================================== S2 — escola: o rabo não mente
def build_s2(sc, W):
    setup_render("#BFD8C8")
    cube("floor", "#C9A06A", (0, 0, -0.05), (16, 12, 0.1), bevel=0)
    cube("wall", "#BFD8C8", (0, 3.0, 4), (16, 0.15, 8), bevel=0)
    cube("board", "#2F5D4A", (0, 2.9, 2.9), (4.4, 0.08, 1.8), bevel=0.03)
    cube("boardframe", "#8E5A34", (0, 2.95, 2.9), (4.6, 0.06, 2.0), bevel=0.02)
    text3d("chalk", "2 + 2 = ?", "#FFFFFF", (-0.5, 2.84, 3.2), 0.35, extrude=0.005)
    # carteiras: Léo (o crush) atrás, Bia na frente
    for x, y in ((0.9, 1.3), (-0.4, -0.3)):
        cube(f"desk{x}", "#E2B66F", (x, y - 0.45, 0.9), (1.0, 0.6, 0.08), bevel=0.02)
        for sx in (-1, 1): cube(f"dl{x}{sx}", "#5B5F66", (x + sx*0.42, y - 0.45, 0.45), (0.05, 0.05, 0.9), bevel=0)
    leo = LeoCtl("leo")
    # colegas olhando (cabeças nas laterais)
    kids = []
    for i, (x, col) in enumerate([(-2.2, "#E3A97E"), (2.4, "#B0784F")]):
        g = empty(f"kid{i}", (x, 0.8, 0))
        sphere(f"kb{i}", "#4FA3D9" if i else "#F4A259", (0, 0, 0.75), 0.32, (1, 0.9, 1.5), g, sub=1)
        sphere(f"kh{i}", col, (0, 0, 1.45), 0.36, parent=g, sub=1)
        sphere(f"khr{i}", "#3B2418", (0, 0.06, 1.6), 0.36, (1, 1, 0.7), g, sub=1)
        for sx in (-1, 1): sphere(f"ke{i}{sx}", INKC, (sx*0.12 + (0.08 if i == 0 else -0.08), -0.34, 1.48), 0.045, (1, 0.5, 1.2), g, sub=1)
        kids.append(g)
    hs = hearts(6)
    cam = camera(40); bia = BiaCtl("bia", tail=True)
    TE, TD, TG, TM = W("escola"), W("descobre"), W("gosta"), W("mentir")
    D = sc["dur"]
    shots = [Shot(0, 0.2, 2.0, 4.6),                       # sala
             Shot(TD - 0.05, -0.1, 1.3, 2.8, roll=-6),      # Bia olhando o Léo
             Shot(TG - 0.05, -0.05, 0.8, 1.8, roll=6),      # rabo enlouquecido + corações
             Shot(W("rabo") - 0.05, 0.9, 1.9, 2.2, roll=-5),  # Léo sem entender
             Shot(TM - 0.05, -0.4, 1.6, 1.9, kind="cut")]  # close: Bia com vergonha
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, -7), exit=(0.8, 0, -0.4, 7))
    L = bia.L
    def frame(t):
        crazy = t > TG - 0.1
        bia.pose(t, loc=(-0.4, -0.3, 0), rotz=math.radians(-150 if TD - 0.05 <= t < TM - 0.05 else 0),
                 expr=[[0, "neutral"], [TD, "happy"], [TM, "worried"]], arms=(12, 12) if t < TM else ((40, 80), (40, 80)), look=(0, 0))
        L.wag(t, amp=40 if crazy else 8, speed=24 if crazy else 4, curl=18)
        leo.pose(t, loc=(0.9, 1.3, 0), expr=[[0, "neutral"], [TG + 0.4, "shock"]], arms=(10, 10), look=(-15, 0))
        for i, k in enumerate(kids):
            k.location.x = (-2.2 if i == 0 else 2.4) + (0.35*ease((t - TG)/0.4)*(1 if i == 0 else -1))
        bpy.context.view_layer.update()
        base = L.tail_base.matrix_world @ Vector((0, 0, 0.6))
        place_hearts(hs, t, (base.x, base.y - 0.6, base.z + 0.4), crazy and t < TM - 0.05, spread=0.9)
        rig.apply(t)
    return frame, rig

# ================================================================== S3 — a porta do ônibus
def build_s3(sc, W):
    setup_render("#9FD3F0")
    cube("street", "#7B8494", (0, 2, -0.06), (30, 10, 0.1), bevel=0)
    cube("curb", "#D9D2C5", (0, -0.4, 0.0), (30, 2.0, 0.12), bevel=0.02)
    # ônibus atrás (em cima no quadro)
    cube("bus", "#FFC72C", (0.6, 1.6, 1.9), (9, 2.2, 3.2), bevel=0.25)
    cube("busstripe", "#1E1B2E", (0.6, 0.49, 1.15), (9, 0.04, 0.12), bevel=0)
    for i in range(4):
        cube(f"bw{i}", "#7FB2E5", (-2.6 + i*1.5, 0.48, 2.65), (1.2, 0.04, 0.9), bevel=0.05)
    heads = []
    for i in range(4):
        h = sphere(f"ph{i}", ["#E3A97E", "#8D5A3B", "#F2C9A0", "#B0784F"][i], (-2.6 + i*1.5, 0.7, 2.5), 0.3, sub=1)
        heads.append(h)
    for sx in (-1, 1): cyl(f"wheel{sx}", "#2A2A35", (0.6 + sx*3.2, 0.45, 0.45), 0.5, 0.3, rot=(math.pi/2, 0, 0), bevel=0.03)
    cube("doorway", "#2A2F45", (2.8, 0.5, 1.25), (1.4, 0.06, 2.5), bevel=0)
    doorL = cube("doorL", "#E8EEF8", (2.45, 0.42, 1.25), (0.68, 0.06, 2.4), bevel=0.03)
    doorR = cube("doorR", "#E8EEF8", (3.15, 0.42, 1.25), (0.68, 0.06, 2.4), bevel=0.03)
    sign = text3d("sign", "ESCOLA", "#FFFFFF", (2.8, 0.45, 2.75), 0.22, extrude=0.01)
    cam = camera(40); bia = BiaCtl("bia", tail=True); bg = bang("bang", "#FF4F4F"); stars_ = [sphere(f"ow{k}", "#FFD93D", (0, 0, -50), 0.06, sub=0, seg=8) for k in range(6)]
    TF, TO, TG = W("fecha"), W("inteiro") - 0.5, W("grito")
    T_HIT = W("dele")
    D = sc["dur"]
    shots = [Shot(0, 1.8, 1.7, 4.4),                        # Bia subindo no ônibus
             Shot(TF - 0.05, 3.0, 1.0, 2.0, roll=6),        # porta fechando no rabo
             Shot(T_HIT, 3.0, 1.0, 2.0, kind="cut", shake=0.08),
             Shot(TO - 0.05, 2.75, 1.65, 1.9, roll=-6),     # close no grito
             Shot(TG - 0.1, 1.5, 2.2, 5.0, roll=5)]         # abre: o ônibus inteiro olhando
    rig = Rig(cam, shots, D, enter=(-0.8, 0.0, 0.45, 7), exit=(0, 0.6, -0.45, -8))
    L = bia.L
    def frame(t):
        # Bia de pé no degrau, de frente; o rabo sai pela porta (aponta para +x)
        bia.pose(t, loc=(2.55, 0.3, 0.12), expr=[[0, "happy"], [T_HIT, "shock"], [TO, "strain"]],
                 mouth=[[0, None], [TO, "yawn"]], arms=(12, 12) if t < T_HIT else (155, 155), look=(0, -8 if t > TO else 0))
        L.tail_base.rotation_euler = (0, math.radians(80), 0)
        stuck = t >= T_HIT
        for k, s in enumerate(L.tail):
            s.rotation_euler = (0, math.radians(4 if stuck else 12*math.sin(t*6 - k)), math.radians(math.sin(t*40)*6 if stuck and k > 3 else 0))
        u = ease((t - TF) / (T_HIT - TF))
        doorL.location.x = lerp(1.9, 2.45, u); doorR.location.x = lerp(3.7, 3.15, u)
        doorL.scale.x = 1; doorR.scale.x = 1
        bg.location = (2.95, -0.2, 2.25 + math.sin(t*25)*0.04) if t > TO - 0.05 else (0, 0, -50)
        bg.rotation_euler = (math.pi/2, 0, 0.15)
        for k, s in enumerate(stars_):
            a = t*7 + k/6*2*math.pi
            s.location = (3.25 + math.cos(a)*0.25, 0.1, 1.0 + math.sin(a)*0.12) if T_HIT < t < TO else (0, 0, -50)
        for i, h in enumerate(heads):
            h.location.y = lerp(0.7, 0.45, ease((t - TG + 0.3)/0.3))
        rig.apply(t)
    return frame, rig

# ================================================================== S4 — gol de rabo
def build_s4(sc, W):
    setup_render("#8FD0F5")
    cube("field", "#4FA84F", (0, 4, -0.05), (30, 16, 0.1), bevel=0)
    for k in range(-6, 7): cube(f"mow{k}", "#5CB85C", (k*1.6, 4, 0.0), (0.8, 16, 0.01), bevel=0)
    cube("line", "#FFFFFF", (0, 3.0, 0.01), (30, 0.08, 0.01), bevel=0)
    # gol em cima no quadro (atrás)
    g = empty("goal", (0, 5.0, 0))
    for sx in (-1, 1): cyl(f"post{sx}", "#FFFFFF", (sx*1.8, 0, 1.1), 0.07, 2.2, g, bevel=0.01)
    cyl("bar", "#FFFFFF", (0, 0, 2.2), 0.07, 3.7, g, rot=(0, math.pi/2, 0), bevel=0.01)
    cube("net", "#DDE8EE", (0, 0.6, 1.1), (3.6, 0.04, 2.2), g, bevel=0)
    for k in range(9): cube(f"netv{k}", "#B8C6CF", (-1.6 + k*0.4, 0.57, 1.1), (0.02, 0.02, 2.2), g, bevel=0)
    for k in range(5): cube(f"neth{k}", "#B8C6CF", (0, 0.57, 0.2 + k*0.45), (3.6, 0.02, 0.02), g, bevel=0)
    ball = empty("ball", (0, 0, -50))
    sphere("ballw", "#FFFFFF", (0, 0, 0), 0.18, parent=ball, sub=1)
    for k in range(5): sphere(f"ballp{k}", "#1E1B2E", (math.cos(k*1.25)*0.13, -0.1, math.sin(k*1.25)*0.13), 0.06, (1, 0.5, 1), ball, sub=0, seg=10)
    conf = [cube(f"cf{k}", ["#FF4F7B", "#FFD93D", "#4FC08D", "#7FB2FF"][k % 4], (0, 0, -50), (0.08, 0.02, 0.12), bevel=0) for k in range(24)]
    cam = camera(40); bia = BiaCtl("bia", tail=True)
    TL, TG, TH = W("lenda"), W("gol"), W("história")
    D = sc["dur"]
    rr = random.Random(3); cdat = [(rr.uniform(-2, 2), rr.uniform(-1, 1), rr.uniform(2, 4), rr.uniform(0, 6)) for _ in conf]
    shots = [Shot(0, 0, 1.6, 4.4),
             Shot(TL - 0.05, 0.3, 0.6, 1.7, roll=-6),       # rabo chutando
             Shot(TG + 0.15, 0, 2.6, 4.4, roll=6),           # bola entrando no gol
             Shot(TH - 0.1, 0, 1.6, 1.95, roll=-5)]          # close comemorando
    rig = Rig(cam, shots, D, enter=(0.6, 0, 0.45, -7), exit=(0, 0.5, -0.4, 7))
    L = bia.L
    T_KICK = TL + 0.35
    def frame(t):
        spin = ease((t - TL + 0.1) / 0.45) * 2*math.pi if t < T_KICK + 0.3 else 0
        win = t > TG + 0.5
        bia.pose(t, loc=(0, 0.2, 0), rotz=spin, expr=[[0, "strain"], [T_KICK, "shock"], [TG + 0.5, "happy"]],
                 arms=((150, 20), (150, 20)) if win else ((60, 0), (60, 0)), look=(0, -10 if TG < t < TH else 0))
        L.wag(t, amp=40 if win else 12, speed=18 if win else 6, curl=10)
        # bola: parada ao lado, sai voando no chute e entra no gol
        if t < T_KICK:
            ball.location = (0.55, -0.1, 0.18)
        else:
            u = cl((t - T_KICK) / 0.7)
            ball.location = (lerp(0.55, 0.6, u), lerp(-0.1, 5.2, u), 0.18 + 2.2*math.sin(u*math.pi*0.9))
        ball.rotation_euler = (t*12, t*5, 0)
        for (x, y, h, ph), c in zip(cdat, conf):
            k = t - TG - 0.6
            if k < 0: c.location = (0, 0, -50); continue
            c.location = (x + math.sin(k*3 + ph)*0.2, 0.5 + y, 3.6 - (k*1.4 + ph*0.1) % 3.6)
            c.rotation_euler = (k*5 + ph, k*3, ph)
        rig.apply(t)
    return frame, rig

# ================================================================== S5 — escolha
def build_s5(sc, W):
    setup_render("#2A2F5E")
    cube("floor", "#3B3F7A", (0, 0, -0.05), (14, 12, 0.1), bevel=0)
    spot = sphere("spot", "#3E4590", (0, 2.0, 1.2), 1.8, (1, 0.05, 1), sub=1)
    q = text3d("q", "?", "#FFD93D", (0.75, -0.2, 2.1), 0.5, extrude=0.04)
    cam = camera(40); bia = BiaCtl("bia", tail=True)
    D = sc["dur"]
    shots = [Shot(0, 0, 1.75, 3.6, push=0.035)]            # Bia embaixo, card de escolha em cima
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, 7), exit=(0, 0, 0, 0), exit_t=0.01)
    L = bia.L
    def frame(t):
        bia.pose(t, loc=(0, 0, 0), rotz=math.radians(-20), expr=[[0, "neutral"], [W("Comenta"), "happy"]],
                 arms=(10, (40, 90)), look=(-8, -6), tilt=8)
        L.wag(t, amp=22, speed=9, curl=14)
        q.location.z = 2.1 + math.sin(t*4)*0.06; q.rotation_euler = (math.pi/2, 0, math.sin(t*3)*0.2)
        rig.apply(t)
    return frame, rig

BUILD = {f"s{i}": globals()[f"build_s{i}"] for i in range(6)}
