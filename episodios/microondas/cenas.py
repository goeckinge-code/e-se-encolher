"""Cenas 3D de "Como funciona o micro-ondas?" — apresentador: Léo.
Mesma gramática de câmera (blender/camera.py, ESTILO.md). Gancho: 4 batidas de câmera nos primeiros 5 s.
Empilhado na vertical: micro-ondas numa prateleira em cima, Léo embaixo.
"""
import bpy, math, random, os, sys
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "blender"))
from lib import *
from look import *
from camera import Rig, Shot
import scenes as OLD

MZ = 2.15      # base do micro-ondas (prateleira)
MW, MH, MD = 2.4, 1.4, 1.3

def kitchen():
    cube("floor", "#D9B88A", (0, 0, -0.05), (16, 12, 0.1), bevel=0)
    cube("wall", "#BFE3E0", (0, 2.0, 4), (16, 0.15, 8), bevel=0)
    for i in range(-16, 17):
        for j in range(0, 16):
            if (i + j) % 2 == 0: cube(f"tile{i}_{j}", "#AED8D4", (i*0.5, 1.92, 0.25 + j*0.5), (0.48, 0.01, 0.48), bevel=0)
    cube("shelf", "#B8743E", (0, 0.95, MZ - 0.06), (3.2, 1.6, 0.12), bevel=0.02)

def microwave(cutaway=False):
    """devolve dict com partes animáveis. cutaway: sem porta e com a lateral do compartimento aberta."""
    g = empty("mw", (0, 0.95, MZ))
    body = "#F2F2F5"; dark = "#2A2F45"
    cube("mwback", body, (0, MD/2, MH/2), (MW, 0.06, MH), g, bevel=0.03)
    cube("mwtop", body, (0, 0, MH), (MW, MD, 0.08), g, bevel=0.04)
    cube("mwbot", body, (0, 0, 0.02), (MW, MD, 0.08), g, bevel=0.04)
    cube("mwleft", body, (-MW/2, 0, MH/2), (0.08, MD, MH), g, bevel=0.03)
    cube("mwright", body, (MW/2, 0, MH/2), (0.08, MD, MH), g, bevel=0.03)
    cube("mwdiv", body, (MW/2 - 0.62, 0, MH/2), (0.06, MD, MH), g, bevel=0.01)
    cav = cube("mwcav", "#FFE9A8", (-0.31, MD/2 - 0.05, MH/2), (MW - 0.75, 0.02, MH - 0.2), g, bevel=0)   # fundo iluminado
    cube("mwcavfloor", "#F7F1DE", (-0.31, 0, 0.08), (MW - 0.75, MD - 0.1, 0.02), g, bevel=0)
    # painel
    cube("mwpanel", "#DCDDE4", (MW/2 - 0.31, -MD/2 + 0.02, MH/2), (0.56, 0.04, MH - 0.1), g, bevel=0.02)
    cube("mwdisp", "#1E1B2E", (MW/2 - 0.31, -MD/2 - 0.01, MH - 0.25), (0.42, 0.02, 0.18), g, bevel=0.01)
    disp = text3d("mwdispt", "0:30", "#63F28A", (MW/2 - 0.31, -MD/2 - 0.03, MH - 0.25), 0.12, g, extrude=0.002)
    for r in range(3):
        for c in range(3):
            cyl(f"mwbtn{r}{c}", "#FFFFFF", (MW/2 - 0.45 + c*0.14, -MD/2 - 0.01, 0.85 - r*0.17), 0.045, 0.03, g, rot=(math.pi/2, 0, 0), bevel=0.01)
    cube("mwstart", "#4FC08D", (MW/2 - 0.31, -MD/2 - 0.01, 0.2), (0.4, 0.03, 0.12), g, bevel=0.02)
    # porta (dobradiça à esquerda)
    hinge = empty("mwhinge", (-MW/2, -MD/2, 0.05), g)
    door = cube("mwdoor", "#E8E8EE", (0.94, -0.02, MH/2 - 0.05), (1.88, 0.06, MH - 0.12), hinge, bevel=0.03)
    win = cube("mwwin", "#3A3F58", (0.88, -0.06, MH/2 - 0.05), (1.5, 0.02, MH - 0.42), hinge, bevel=0.02)
    cube("mwhandle", "#B8BBC8", (1.78, -0.1, MH/2 - 0.05), (0.06, 0.06, 0.7), hinge, bevel=0.02)
    # prato giratório + tigela de sopa
    plate = empty("mwplate", (-0.31, 0, 0.12), g)
    cyl("plateglass", "#CFE9F2", (0, 0, 0), 0.5, 0.03, plate, bevel=0.01)
    bowl = empty("bowl", (0, 0, 0.02), plate)
    b = sphere("bowlb", "#FF8C42", (0, 0, 0.2), 0.3, (1, 1, 0.75), bowl, sub=1); Leo._cut_upper(Leo, b, 0.2)
    soup = cyl("soup", "#F2B84B", (0, 0, 0.18), 0.27, 0.02, bowl, bevel=0)
    # magnetron no compartimento da direita (visível no corte)
    mag = empty("magnetron", (MW/2 - 0.31, 0.05, 0.75), g)
    cyl("magbody", "#C97B3A", (0, 0, 0), 0.17, 0.32, mag, bevel=0.02)
    for k in range(6): cyl(f"magfin{k}", "#B0B4C0", (0, 0, -0.14 + k*0.055), 0.24, 0.015, mag, bevel=0)
    cyl("magant", "#E0E0E8", (-0.22, 0, 0.05), 0.04, 0.3, mag, rot=(0, math.pi/2, 0), bevel=0)
    glow = sphere("magglow", "#FFB34D", (0, -0.15, 0.0), 0.09, parent=mag, sub=1)
    side = cube("mwsidepanel", body, (MW/2 - 0.31, -MD/2 + 0.06, MH/2), (0.56, 0.04, MH - 0.12), g, bevel=0.02)
    side.hide_render = cutaway
    if cutaway:   # corte: sem porta e sem o painel da frente, para ver o magnetron
        for o in [door, win] + list(hinge.children): o.hide_render = True
        for o in g.children:
            if o.name.startswith(("mwpanel", "mwdisp", "mwbtn", "mwstart")): o.hide_render = True
    return dict(g=g, hinge=hinge, plate=plate, bowl=bowl, soup=soup, mag=mag, glow=glow, disp=disp, side=side, cav=cav)

def steam(n, seed=1):
    rr = random.Random(seed)
    return [(sphere(f"stm{seed}_{k}", "#FFFFFF", (0, 0, -50), 0.1, sub=1), rr.uniform(-0.15, 0.15), rr.uniform(0, 1)) for k in range(n)]

def place_steam(st, t, base, on, hgt=0.8, sz=0.12):
    for o, dx, ph in st:
        if not on: o.hide_render = True; continue
        u = (t*0.7 + ph) % 1
        o.hide_render = False
        o.location = (base[0] + dx + math.sin(u*6 + ph*9)*0.06, base[1], base[2] + u*hgt)
        s = (sz + u*sz*1.4)/0.1*(1 - u*0.5); o.scale = (s, s, s)

def wave_tube(name, length, amp, lam, color="#FF5A7A", r=0.025, n=80):
    pts = [(-length/2 + length*i/(n-1), 0, amp*math.sin(2*math.pi*(length*i/(n-1))/lam)) for i in range(n)]
    o = poly_tube(name, color, pts, r)
    return o

def droplet(name, loc, s=1.0, color="#4FB3F2"):
    """gotinha de água com carinha"""
    g = empty(name, loc)
    sphere(name+"b", color, (0, 0, 0), 0.3*s, parent=g, sub=1)
    bpy.ops.mesh.primitive_cone_add(radius1=0.22*s, depth=0.32*s, location=(0, 0, 0))
    c = bpy.context.object; c.name = name+"c"; c.parent = g; c.location = (0, 0, 0.3*s); setmat(c, color)
    for sx in (-1, 1):
        sphere(name+f"e{sx}", INKC, (sx*0.1*s, -0.27*s, 0.05*s), 0.04*s, (1, 0.5, 1.3), g, sub=0, seg=10)
    arc_tube(name+"m", INKC, (0, -0.29*s, -0.06*s), 0.06*s, 0.012*s, math.radians(200), math.radians(340), g)
    sphere(name+"sh", "#BFE6FF", (0.1*s, -0.22*s, 0.15*s), 0.06*s, parent=g, sub=0, seg=10)
    return g

def wifi(name):
    g = empty(name, (0, 0, -50))
    sphere(name+"d", "#4FC08D", (0, 0, 0), 0.07, parent=g, sub=0, seg=12)
    for k in range(3):
        arc_tube(name+f"a{k}", "#4FC08D", (0, 0, 0.0), 0.18 + k*0.15, 0.035, math.radians(45), math.radians(135), g)
    return g

# ================================================================== S0 — GANCHO
def build_s0(sc, W):
    setup_render("#BFE3E0")
    kitchen(); M = microwave()
    st = steam(6, 1)
    hot = text3d("hotlines", "~ ~ ~", "#FF5A3D", (0, 0, -50), 0.3, extrude=0.02)
    drop = droplet("hookdrop", (0, 0, -50), 1.0)
    cam = camera(40); leo = LeoCtl("leo")
    TF, TS, TSg = W("fogo"), W("Sabe"), W("O segredo")
    D = sc["dur"]
    bowlc = (-0.31, 0.6, MZ + 0.35)
    shots = [Shot(0.0, -0.1, 2.05, 2.5, shake=0.07, push=0.10),           # 1ª imagem: Léo em choque + porta abrindo (tremida)
             Shot(TF - 0.12, -0.31, MZ + 0.5, 1.4, roll=-7),               # a sopa fumegando (sem fogo!)
             Shot(TS - 0.05, 0.1, 1.7, 1.55, roll=6),                      # "Sabe como?" close
             Shot(TSg - 0.05, -0.31, MZ + 0.6, 1.0, roll=-7)]              # mergulha na sopa: a gotinha
    rig = Rig(cam, shots, D, enter=(0, 0, 0.0, 0), enter_t=0.01, exit=(0, 0, -0.55, 8))
    def frame(t):
        M["hinge"].rotation_euler = (0, 0, -math.radians(105)*eout(t/0.35))     # porta escancara no 1º quadro
        place_steam(st, t, (bowlc[0], 0.45, bowlc[2]), True, 0.7, 0.07)
        leo.pose(t, loc=(0, -0.6, 0), expr=[[0, "shock"], [TS, "neutral"], [TSg, "happy"]],
                 arms=((150, 20), (150, 20)) if t < TS else (10, (30, 120)), look=(0, -12 if t < TS else 0), tilt=8 if TS < t < TSg else 0)
        k = t - TSg
        drop.location = (bowlc[0], 0.35, bowlc[2] - 0.1 + 0.45*back(cl(k/0.35))) if k > 0 else (0, 0, -50)
        drop.rotation_euler = (0, math.sin(t*40)*0.15 if k > 0.4 else 0, 0)
        drop.scale = (0.55,)*3
        rig.apply(t)
    return frame, rig

# ================================================================== S1 — magnetron e ondas
def build_s1(sc, W):
    setup_render("#BFE3E0")
    kitchen(); M = microwave(cutaway=True)
    waves = [wave_tube(f"wv{k}", 1.4, 0.06, 0.28, "#FF5A7A") for k in range(3)]
    wf = wifi("wifi")
    cam = camera(40); leo = LeoCtl("leo")
    TM, TO, TW = W("magnetron"), W("ondas"), W("wi-fi")
    D = sc["dur"]
    magw = Vector((MW/2 - 0.31, 0.95, MZ + 0.75))
    shots = [Shot(0, 0, MZ + 0.2, 3.4),
             Shot(TM - 0.05, magw.x, magw.z, 1.2, roll=6),          # close no magnetron
             Shot(TO - 0.05, -0.2, MZ + 0.7, 2.2, roll=-6),        # ondas atravessando
             Shot(TW - 0.05, 0, 1.75, 2.1, roll=5)]                # Léo + wi-fi
    rig = Rig(cam, shots, D, enter=(0.5, 0.4, 0.5, 7), exit=(-0.4, 0.3, -0.45, -7))
    def frame(t):
        on = t > TM
        M["glow"].scale = (1 + 0.4*math.sin(t*20)*on,)*3
        for k, w in enumerate(waves):
            w.hide_render = not (t > TO - 0.3)
            ph = (t*0.9) % 0.28
            w.location = (-0.35 + ph, 0.55 + k*0.15, MZ + 0.45 + k*0.28)
        leo.pose(t, loc=(0, -0.6, 0), expr=[[0, "neutral"], [TM, "happy"], [TO, "shock"], [TW, "happy"]],
                 arms=(10, (150, 10)) if t < TW else ((40, 40), (160, 10)), look=(20, -14) if t < TW else (0, 0))
        wf.location = (0.62, -0.9, 2.15 + math.sin(t*4)*0.04) if t > TW - 0.1 else (0, 0, -50)
        wf.rotation_euler = (math.pi/2, 0, 0); s = back(cl((t - TW + 0.1)/0.3)); wf.scale = (s, s, s)
        rig.apply(t)
    return frame, rig

# ================================================================== S2 — gotinhas chacoalhando
def build_s2(sc, W):
    setup_render("#FFD48A")
    # macro: superfície da sopa
    cube("soupsurf", "#F2B84B", (0, 0.5, -0.05), (12, 8, 0.1), bevel=0)
    for k in range(14):
        rr = random.Random(k); sphere(f"bub{k}", "#F7CF73", (rr.uniform(-3, 3), rr.uniform(0, 2), 0.02), rr.uniform(0.08, 0.2), (1, 1, 0.3), sub=1)
    drops = [droplet(f"d{k}", (x, y, 0.55 + z), 1.0) for k, (x, y, z) in enumerate([(-0.75, 0.2, 0.2), (0.75, 0.3, 0.0), (0, 0.1, 0.9), (-0.4, 0.6, 1.7), (0.5, 0.5, 1.6)])]
    waves = [wave_tube(f"w{k}", 6.0, 0.18, 0.7, "#FF5A7A", r=0.04) for k in range(3)]
    lines = [cube(f"sh{k}", "#1E1B2E", (0, 0, -50), (0.03, 0.01, 0.16), bevel=0) for k in range(10)]
    cam = camera(40)
    TA, TQ, TC, TP = W("água"), W("Quando"), W("chacoalhar"), W("parar")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.4, 3.4),
             Shot(TA - 0.05, -0.75, 0.75, 1.3, roll=-6),        # close numa gotinha
             Shot(TQ - 0.05, 0, 1.35, 3.6, roll=6),              # ondas chegando
             Shot(TC - 0.05, 0.0, 1.45, 1.4, kind="cut", shake=0.05)]   # chacoalho no close
    rig = Rig(cam, shots, D, enter=(0, -0.6, 0.6, -8), exit=(0, 0.4, -0.45, 7))
    rr = random.Random(5); ph = [rr.uniform(0, 6) for _ in drops]
    def frame(t):
        hit = t > TQ + 0.4
        amp = 0.0 if not hit else 0.06 if t < TC else 0.1
        for d, p in zip(drops, ph):
            base = d.get("base") or tuple(d.location); d["base"] = base
            d.location = (base[0] + math.sin(t*55 + p)*amp, base[1], base[2] + math.cos(t*47 + p)*amp + math.sin(t*1.5 + p)*0.05)
            d.rotation_euler = (0, math.sin(t*50 + p)*amp*3, 0)
        for k, w in enumerate(waves):
            on = t > TQ - 0.2
            w.hide_render = not on
            x = lerp(-6, 0, eout(cl((t - TQ + 0.2)/0.8))) + ((t*1.2) % 0.7)
            w.location = (x, -0.3, 0.6 + k*0.75)
        for k, l in enumerate(lines):
            d = drops[k % len(drops)]; on = t > TC
            l.location = (d.location.x + (0.42 if k < 5 else -0.42), d.location.y - 0.3, d.location.z + 0.05*(k % 3)) if on else (0, 0, -50)
            l.rotation_euler = (0, math.radians(20 if k < 5 else -20), 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S3 — esfregar as mãos
def build_s3(sc, W):
    setup_render("#9FC7E8")
    cube("ground", "#EEF4FA", (0, 0, -0.05), (16, 12, 0.1), bevel=0)
    snow = [sphere(f"sn{k}", "#FFFFFF", (0, 0, -50), 0.04, sub=0, seg=8) for k in range(40)]
    heat = [wave_tube(f"ht{k}", 0.5, 0.04, 0.16, "#FF6A3D", r=0.018, n=30) for k in range(3)]
    for h in heat: h.rotation_euler = (0, math.pi/2, 0)
    scarf = torus("scarf", "#E63946", (0, 0, -50), 0.16, 0.05)
    drops = [droplet(f"hd{k}", (0, 0, -50), 0.5, "#FF7A5A") for k in range(2)]
    cam = camera(40); leo = LeoCtl("leo")
    TE, TI, TF = W("esquenta"), W("esfregar"), W("frio")
    D = sc["dur"]
    rr = random.Random(2); sd = [(rr.uniform(-1.5, 1.5), rr.uniform(0, 4), rr.uniform(0.3, 0.6)) for _ in snow]
    shots = [Shot(0, 0, 2.1, 2.4),                                  # gotinhas vermelhas com vapor
             Shot(TI - 0.05, 0, 1.25, 1.4, roll=-6),                # close nas mãos esfregando
             Shot(TF - 0.05, 0, 1.6, 2.0, roll=5)]                  # rosto feliz e quentinho
    rig = Rig(cam, shots, D, enter=(0.6, 0, 0.5, 7), exit=(0, -0.4, -0.45, -7))
    def frame(t):
        rub = t > TI - 0.2
        leo.pose(t, loc=(0, 0, 0), expr=[[0, "tired"], [TI + 0.6, "happy"]],
                 arms=((25, 75 + math.sin(t*30)*10), (25, 75 - math.sin(t*30)*10)) if rub else ((20, 60), (20, 60)), look=(0, 10))
        bpy.context.view_layer.update()
        n = leo.L.head.matrix_world @ Vector((0, 0, -0.05))
        scarf.location = n; scarf.scale = (1.1, 1, 0.8)
        hand = (leo.L.arm[-1].matrix_world @ Vector((-0.06, 0, -0.41)) + leo.L.arm[1].matrix_world @ Vector((0.06, 0, -0.41))) / 2
        for k, h in enumerate(heat):
            u = (t*1.2 + k/3) % 1
            h.hide_render = not (t > TI + 0.3)
            h.location = (hand.x - 0.28 + k*0.28, hand.y - 0.25, hand.z + 0.05 + u*0.25); h.scale = (0.7, 0.7, 0.7)
        for (x, ph, sp), s in zip(sd, snow):
            s.location = (x, -0.8, 3.2 - ((t*sp + ph) % 4))
        for k, d in enumerate(drops):    # abertura: duas gotinhas já quentes (ligação com a cena anterior)
            on = t < TI - 0.05
            d.location = (-0.35 + k*0.7, -0.9, 2.15 + math.sin(t*40 + k)*0.04) if on else (0, 0, -50)
        rig.apply(t)
    return frame, rig

# ================================================================== S4 — o prato gira
def build_s4(sc, W):
    setup_render("#BFE3E0")
    kitchen(); M = microwave()
    M["hinge"].rotation_euler = (0, 0, -math.radians(105))
    # metades quente/fria da comida (aparecem no "senão")
    hot = sphere("hothalf", "#FF4F3D", (0, 0, -50), 0.27, (1, 1, 0.08), sub=1)
    cold = sphere("coldhalf", "#7FC4FF", (0, 0, -50), 0.27, (1, 1, 0.08), sub=1)
    Leo._cut_upper(Leo, hot, 0.0); Leo._cut_upper(Leo, cold, 0.0)
    st = steam(6, 4); ice = [cube(f"ice{k}", "#E4F6FF", (0, 0, -50), (0.08, 0.08, 0.08), bevel=0.015) for k in range(3)]
    arrow = text3d("arrow", "↻", "#1E1B2E", (0, 0, -50), 0.45, extrude=0.03)
    cam = camera(40); leo = LeoCtl("leo")
    TG, TS, TP, TGe = W("gira"), W("Senão"), W("pela"), W("gelado")
    D = sc["dur"]
    pw = Vector((-0.31, 0.95, MZ + 0.12))
    shots = [Shot(0, -0.1, MZ + 0.3, 2.6),
             Shot(TG - 0.05, pw.x, pw.z + 0.25, 1.3, roll=6),        # prato girando
             Shot(TS - 0.05, pw.x, pw.z + 0.25, 1.15, kind="cut"),   # para: metade quente, metade fria
             Shot(TP - 0.05, 0.1, 1.65, 1.9, roll=-6),               # Léo queimando a boca
             Shot(TGe - 0.05, 0.1, 1.65, 1.9, kind="cut", shake=0.04)]   # ... e tremendo de frio
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, -7), exit=(0, 0.3, -0.45, 7))
    def frame(t):
        spinning = t < TS - 0.05
        M["plate"].rotation_euler = (0, 0, t*2.2 if spinning else (TS - 0.05)*2.2)
        M["plate"].rotation_euler.x = 0
        split = not spinning
        c = M["g"].matrix_world @ Vector((-0.31, 0, 0.12 + 0.02 + 0.2))
        for o, dx in ((hot, -0.135), (cold, 0.135)):
            o.location = (c.x + dx, c.y, c.z + 0.005) if split else (0, 0, -50)
            o.scale = (0.5, 1, 0.08)
        place_steam(st, t, (c.x - 0.15, c.y - 0.2, c.z), split, 0.6, 0.06)
        for k, i in enumerate(ice):
            i.location = (c.x + 0.08 + k*0.07, c.y - 0.15, c.z + 0.05) if split else (0, 0, -50); i.rotation_euler = (k, k*0.5, 0)
        arrow.location = (pw.x, 0.3, pw.z + 0.75) if TG - 0.1 < t < TS - 0.05 else (0, 0, -50)
        arrow.rotation_euler = (math.pi/2, 0, -t*3)
        ex = "happy" if t < TS else "strain" if t < TP + 0.1 else "shock" if t < TGe else "worried"
        leo.pose(t, loc=(0, -0.6, 0), expr=[[0, ex]], mouth=[[0, None], [TP, "yawn"], [TGe, "wavy"]],
                 arms=((150, 20), (150, 20)) if TP <= t < TGe else ((30, 60), (30, 60)) if t >= TGe else (10, 10),
                 tilt=math.sin(t*45)*4 if t >= TGe else 0, look=(0, -10 if t < TS else 0))
        rig.apply(t)
    return frame, rig

# ================================================================== S5 — nada de metal: faísca
def build_s5(sc, W):
    setup_render("#BFE3E0")
    kitchen(); M = microwave()
    M["hinge"].rotation_euler = (0, 0, -math.radians(105))
    M["bowl"].hide_render = True
    for c in M["bowl"].children_recursive: c.hide_render = True
    fork = empty("fork", (0, -0.1, 0.25), M["plate"])
    cube("forkh", "#C9CDD8", (0, 0.15, 0), (0.09, 0.6, 0.05), fork, bevel=0.015)
    cube("forkb", "#C9CDD8", (0, -0.17, 0), (0.2, 0.08, 0.05), fork, bevel=0.015)
    for k in range(4): cube(f"fork{k}", "#C9CDD8", (-0.075 + k*0.05, -0.32, 0), (0.025, 0.26, 0.04), fork, bevel=0.008)
    fork.rotation_euler = (math.radians(-65), 0, 0.3)
    sparks = [cube(f"spk{k}", "#FFE14D", (0, 0, -50), (0.04, 0.01, 0.28), bevel=0) for k in range(22)]
    flash = sphere("flash", "#FFF6B0", (0, 0, -50), 0.32, (1, 0.1, 1), sub=1)
    warn = text3d("warn", "!", "#E63946", (0, 0, -50), 0.6, extrude=0.05)
    cam = camera(40); leo = LeoCtl("leo")
    TG, TB, TF = W("garfo"), W("batem"), W("faísca")
    D = sc["dur"]
    pw = Vector((-0.31, 0.95, MZ + 0.2))
    shots = [Shot(0, 0, 1.9, 3.2),
             Shot(TG - 0.05, pw.x, pw.z + 0.35, 1.3, roll=-6),        # close no garfo no prato
             Shot(TB + 0.1, pw.x, pw.z + 0.4, 1.6, kind="cut", shake=0.08),   # faíscas!
             Shot(TF - 0.05, 0.05, 1.65, 1.9, roll=6, shake=0.04)]   # Léo apavorado
    rig = Rig(cam, shots, D, enter=(0.6, 0.3, 0.5, -7), exit=(0, 0.4, -0.45, 7))
    rr = random.Random(7); sd = [(rr.uniform(0, 6.28), rr.uniform(0.15, 0.45), rr.uniform(0, 1)) for _ in sparks]
    def frame(t):
        M["plate"].rotation_euler = (0, 0, 0)
        on = t > TB + 0.1
        bpy.context.view_layer.update()
        tip = M["plate"].matrix_world @ Vector((0.0, -0.3, 0.55))
        for (a, r, ph), sp in zip(sd, sparks):
            if not on: sp.location = (0, 0, -50); continue
            u = (t*5 + ph) % 1
            sp.location = (tip.x + math.cos(a)*r*u*2.0, tip.y - 0.3, tip.z + math.sin(a)*r*u*2.0)
            sp.rotation_euler = (0, -a + math.pi/2, 0); sp.scale = (1, 1, 1 - u)
        fl = on and (int(t*12) % 2 == 0)
        flash.location = (tip.x, tip.y - 0.25, tip.z + 0.1) if fl else (0, 0, -50)
        warn.location = (0.62, -0.9, 2.0 + math.sin(t*20)*0.03) if t > TF - 0.1 else (0, 0, -50)
        warn.rotation_euler = (math.pi/2, 0, 0.1)
        leo.pose(t, loc=(0, -0.6, 0), expr=[[0, "neutral"], [TG, "worried"], [TB + 0.1, "shock"]],
                 arms=((160, 15), (160, 15)) if on else (10, (40, 60)), look=(0, -12 if t < TF else 0),
                 tilt=math.sin(t*30)*3 if on else 0)
        rig.apply(t)
    return frame, rig

# ================================================================== S6 — escolha
def build_s6(sc, W):
    setup_render("#BFE3E0")
    kitchen(); M = microwave()
    q = text3d("q", "?", "#FFD93D", (0.75, -0.9, 1.95), 0.45, extrude=0.04)
    cam = camera(40); leo = LeoCtl("leo")
    D = sc["dur"]
    shots = [Shot(0, 0, 1.75, 3.6, push=0.035)]
    rig = Rig(cam, shots, D, enter=(0, 0.5, 0.5, 7), exit=(0, 0, 0, 0), exit_t=0.01)
    def frame(t):
        leo.pose(t, loc=(0, -0.6, 0), expr=[[0, "neutral"], [W("Comenta"), "happy"]], arms=(10, (40, 90)), look=(-8, -6), tilt=8)
        q.location.z = 1.95 + math.sin(t*4)*0.06; q.rotation_euler = (math.pi/2, 0, math.sin(t*3)*0.2)
        rig.apply(t)
    return frame, rig

BUILD = {f"s{i}": globals()[f"build_s{i}"] for i in range(7)}
