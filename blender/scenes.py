"""Cenas 3D do episódio. Cada build_* monta o cenário e devolve frame(t)."""
import bpy, math, random, sys
from mathutils import Vector
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from lib import *
from look import *

def camkeys(cam, t, keys, roll=0.0, shake=0.0):
    """keys: [(t, eye, target, lens)] interpolados com ease"""
    if t <= keys[0][0]: k0 = k1 = keys[0]; u = 0
    elif t >= keys[-1][0]: k0 = k1 = keys[-1]; u = 0
    else:
        for i in range(len(keys)-1):
            if keys[i][0] <= t < keys[i+1][0]:
                k0, k1 = keys[i], keys[i+1]; u = (t-k0[0])/(k1[0]-k0[0]); break
    e = ease(u)
    eye = Vector(k0[1]).lerp(Vector(k1[1]), e); tg = Vector(k0[2]).lerp(Vector(k1[2]), e)
    if shake:
        eye += Vector((math.sin(t*47)*shake, 0, math.cos(t*41)*shake))
    cam.data.lens = lerp(k0[3], k1[3], e)
    look_at(cam, eye, tg, roll)

class Puff:
    def __init__(self, n=8):
        self.o = [sphere(f"puff{i}", "#FFFFFF", (0, 0, -50), 0.2, sub=1) for i in range(n)]
    def at(self, center, R, u):
        for i, o in enumerate(self.o):
            if u <= 0 or u >= 1: o.hide_render = True; continue
            o.hide_render = False
            a = i/len(self.o)*2*math.pi + 0.4
            d = R*(0.3 + 0.9*eout(u)); r = R*0.45*(1-0.7*u)
            o.location = (center[0]+math.cos(a)*d, center[1]-0.3, center[2]+math.sin(a)*d*0.8)
            o.scale = (r/0.2,)*3

# ---------------------------------------------------------------- quarto
def bedroom(empty_room=False):
    cube("floor", "#C98A4B", (0, 0, -0.05), (14, 12, 0.1), bevel=0)
    for k in range(-6, 7):
        cube(f"plank{k}", "#B97A3E", (k*0.9, 0, 0.0), (0.03, 12, 0.012), bevel=0)
    cube("wall", "#F2D0B4", (0, 2.6, 3), (14, 0.15, 6.2), bevel=0)
    for k in range(-14, 15):
        cube(f"stripe{k}", "#EDC2A2", (k*0.45, 2.52, 3), (0.18, 0.01, 6.2), bevel=0)
    cube("wallL", "#EBC7AA", (-4.2, 0, 3), (0.15, 12, 6.2), bevel=0)
    cube("base", "#FFFFFF", (0, 2.5, 0.08), (14, 0.06, 0.16), bevel=0.01)
    # janela com nascer do sol
    cube("winframe", "#FFFFFF", (-1.7, 2.48, 2.9), (1.7, 0.12, 2.1), bevel=0.04)
    cube("winsky", "#FFB27A", (-1.7, 2.42, 3.25), (1.45, 0.02, 1.2), bevel=0)
    cube("winsky2", "#FFD9A0", (-1.7, 2.42, 2.35), (1.45, 0.02, 0.7), bevel=0)
    sphere("sun", "#FFF3C4", (-1.55, 2.41, 2.75), 0.32, (1, 0.05, 1), sub=1)
    cube("winbarV", "#FFFFFF", (-1.7, 2.4, 2.9), (0.07, 0.05, 1.9), bevel=0.01)
    cube("winbarH", "#FFFFFF", (-1.7, 2.4, 2.9), (1.5, 0.05, 0.07), bevel=0.01)
    cube("sill", "#FFFFFF", (-1.7, 2.3, 1.82), (1.95, 0.35, 0.09), bevel=0.02)
    cyl("plantpot", "#E86A5B", (-1.1, 2.25, 1.98), 0.13, 0.22, bevel=0.02)
    for k in range(4):
        sphere(f"leaf{k}", "#5FAF57", (-1.1+math.cos(k*1.6)*0.09, 2.22, 2.2+k*0.05), 0.11, (0.7, 0.5, 1.2), sub=1)
    # pôster de foguete
    cube("poster", "#3B3F7A", (1.3, 2.5, 3.2), (1.1, 0.03, 1.45), bevel=0.01)
    for k in range(6):
        sphere(f"star{k}", "#FFD93D", (0.95+(k % 3)*0.35, 2.47, 3.6+(k//3)*0.32-0.15*(k % 2)), 0.05, sub=0, seg=8)
    sphere("rocket", "#FFFFFF", (1.3, 2.46, 3.0), 0.14, (1, 0.4, 2.2), sub=1)
    sphere("rwin", "#4FC3E8", (1.3, 2.4, 3.1), 0.06, (1, 0.4, 1), sub=1)
    # cama
    cube("bedframe", "#9A5B2E", (2.3, 0.9, 0.35), (2.2, 3.2, 0.4), bevel=0.05)
    cube("headboard", "#9A5B2E", (2.3, 2.45, 0.9), (2.2, 0.15, 1.5), bevel=0.06)
    cube("mattress", "#FFFFFF", (2.3, 0.9, 0.62), (2.05, 3.0, 0.2), bevel=0.08)
    cube("blanket", "#4E8FE0", (2.3, 0.45, 0.72), (2.15, 2.2, 0.16), bevel=0.08)
    pil = sphere("pillow", "#FFFFFF", (2.3, 2.0, 0.85), 0.45, (1.6, 0.6, 0.35), sub=2)
    # criado-mudo + despertador
    cube("stand", "#B8743E", (-2.6, 1.8, 0.45), (0.9, 0.8, 0.9), bevel=0.04)
    cube("drawer", "#C98A4B", (-2.6, 1.39, 0.5), (0.7, 0.03, 0.3), bevel=0.02)
    sphere("knob", "#FFD93D", (-2.6, 1.36, 0.5), 0.04, sub=0, seg=10)
    clk = empty("clock", (-2.6, 1.8, 1.17))
    cyl("clkbody", "#2EC4B6", (0, 0, 0), 0.24, 0.16, clk, rot=(math.pi/2, 0, 0), bevel=0.03)
    cyl("clkface", "#FFFFFF", (0, -0.085, 0), 0.18, 0.02, clk, rot=(math.pi/2, 0, 0), bevel=0)
    for sx in (-1, 1):
        sphere(f"bell{sx}", "#FFD93D", (sx*0.15, 0, 0.22), 0.09, (1, 1, 0.7), clk, sub=1)
        capsule(f"clkleg{sx}", INKC, (sx*0.12, 0, -0.18), (sx*0.17, 0, -0.27), 0.02, clk)
    cube("hand1", INKC, (0, -0.1, 0.05), (0.02, 0.01, 0.11), clk, bevel=0)
    cube("hand2", INKC, (0.04, -0.1, 0), (0.09, 0.01, 0.02), clk, bevel=0)
    rings = []
    for k in range(3):
        for sx in (-1, 1):
            a = math.radians(30 + k*22)
            o = capsule(f"ring{k}{sx}", INKC, (sx*math.cos(a)*0.34, -0.05, math.sin(a)*0.34), (sx*math.cos(a)*0.46, -0.05, math.sin(a)*0.46), 0.015, clk)
            rings += [o] + [c for c in clk.children if c.name.startswith(f"ring{k}{sx}_cap")]
    # tapete
    cyl("rug", "#E86A5B", (0, -0.2, 0.01), 1.9, 0.02, bevel=0.01, verts=64).scale = (1, 0.6, 1)
    cyl("rug2", "#F4A259", (0, -0.2, 0.025), 1.4, 0.02, bevel=0.01, verts=64).scale = (1, 0.6, 1)
    return clk, rings

# ---------------------------------------------------------------- S0
def build_s0(sc_, W_):
    setup_render("#F2D0B4")
    clk, rings = bedroom(); cam = camera(40); leo = LeoCtl("leo"); puff = Puff()
    TM = W_("metade")
    def frame(t):
        ring = t < TM
        clk.rotation_euler = (0, math.sin(t*60)*0.06 if ring else 0, math.sin(t*55)*0.04 if ring else 0)
        for o in rings: o.hide_render = not ring
        s = lerp(1.0, 0.5, ease((t-TM)/0.28))
        yawn = 0.45 < t < 1.5
        if t < TM:
            st = ease((t-0.45)/0.3) - ease((t-1.2)/0.3)
            arms = (lerp(8, 160, st), lerp(8, 160, st))
        else:
            arms = (lerp(8, 165, eout((t-TM)/0.2)), lerp(8, 158, eout((t-TM-0.05)/0.2)))
        leo.pose(t, loc=(0, 0, 0), s=s, expr=[[0, "tired"], [TM+0.12, "shock"]], mouth=[[0, None], [0.45, "yawn"], [1.5, None]],
                 arms=arms, look=(0, 6 if t > TM else -4))
        puff.at((0, 0, 1.1*s+0.4), 0.9, (t-TM)/0.6)
        camkeys(cam, t, [(0, (0.6, -6.2, 1.5), (0, 0, 1.15), 38), (TM, (0.4, -5.6, 1.45), (0, 0, 1.1), 40),
                         (TM+0.9, (0.25, -3.2, 0.85), (0, 0, 0.62), 42), (sc_["dur"], (0.2, -3.0, 0.82), (0, 0, 0.6), 42)])
    return frame

# ---------------------------------------------------------------- S1 (roupa sobrando)
def build_s1(sc_, W_):
    setup_render("#F2D0B4")
    clk, rings = bedroom(); cam = camera(40); leo = LeoCtl("leo")
    for o in rings: o.hide_render = True
    TR, TI = W_("roupa"), W_("inteira")
    sw = sphere("sweat", "#7EC8F2", (0, 0, 0), 0.05, (0.8, 0.5, 1.2), sub=1)
    def frame(t):
        arms = (8, 150+math.sin(t*12)*20) if t > TR else (8, 8)
        leo.pose(t, loc=(0, 0, 0), s=0.5, big=True, expr=[[0, "neutral"], [0.9, "worried"]], arms=arms, look=(0, 8), tilt=-4)
        sw.hide_render = t < TR
        sw.location = (0.22, -0.2, 1.0 - ((t*0.4) % 0.15))
        keys = [(0, (0.5, -3.4, 0.85), (0, 0, 0.6), 40), (TI-0.05, (0.3, -3.0, 0.8), (0, 0, 0.58), 40),
                (TI+0.25, (0.12, -1.7, 0.86), (0, 0, 0.78), 42), (sc_["dur"], (0.1, -1.6, 0.86), (0, 0, 0.78), 42)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S2 (gato)
def build_s2(sc_, W_):
    setup_render("#7487C2")
    cube("floor", "#B65A3C", (0, 0, -0.05), (14, 14, 0.1), bevel=0)
    for k in range(-8, 9): cube(f"rugl{k}", "#A44E33", (k*0.6, 0, 0.002), (0.25, 14, 0.01), bevel=0)
    cube("wall", "#6E82BC", (0, 4, 3), (14, 0.15, 6.2), bevel=0)
    cube("sofa", "#C0473F", (-2.6, 2.6, 0.8), (3.4, 1.4, 1.6), bevel=0.25)
    cube("sofa2", "#D85A50", (-2.6, 1.6, 0.6), (3.4, 1.4, 0.9), bevel=0.25)
    cam = camera(36); leo = LeoCtl("leo")
    # gato agachado (loaf) com rabo
    cat = empty("cat", (0.75, 1.0, 0)); cat.scale = (1.3, 1.3, 1.3)
    sphere("catbody", "#F2973A", (0.35, 0.5, 0.55), 0.7, (1.0, 1.35, 0.8), cat, sub=2)
    head = empty("cathead", (0, -0.45, 0.85), cat)
    sphere("catskull", "#F2973A", (0, 0, 0), 0.62, (1.12, 0.95, 0.92), head, sub=2)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(radius1=0.24, depth=0.42, location=(0, 0, 0))
        e = bpy.context.object; e.name = f"ear{sx}"; e.parent = head; e.location = (sx*0.42, 0.05, 0.55); e.rotation_euler = (0, sx*-0.35, 0); setmat(e, "#F2973A"); smooth(e, 1)
        sphere(f"earin{sx}", "#F7B3B8", (sx*0.41, -0.07, 0.5), 0.12, (0.8, 0.3, 1.2), head, sub=1)
        sphere(f"cateye{sx}", "#C9E35A", (sx*0.27, -0.52, 0.12), 0.17, (1, 0.45, 1.1), head, sub=1)
        sphere(f"catpup{sx}", INKC, (sx*0.27, -0.6, 0.12), 0.12, (1, 0.3, 1.25), head, sub=1)
        sphere(f"catgl{sx}", "#FFFFFF", (sx*0.27+0.06, -0.64, 0.2), 0.035, sub=0, parent=head)
        for k in range(3):
            capsule(f"wh{sx}{k}", INKC, (sx*0.35, -0.55, -0.1-k*0.06), (sx*0.85, -0.6, -0.05-k*0.1), 0.008, head)
    sphere("muzzle", "#FFF1DE", (0, -0.5, -0.15), 0.25, (1.3, 0.6, 0.8), head, sub=1)
    sphere("catnose", "#F27C8A", (0, -0.65, -0.03), 0.06, (1.2, 0.6, 0.8), head, sub=1)
    for k in range(3): cube(f"stripe{k}", "#C96E1E", (-0.18+k*0.18, -0.2, 0.5), (0.07, 0.4, 0.06), head, bevel=0.02)
    for sx in (-1, 1): sphere(f"paw{sx}", "#FFF1DE", (sx*0.35, -0.6, 0.1), 0.17, (1, 1.4, 0.6), cat, sub=1)
    tail = [empty(f"tail{i}", (0, 0, 0), cat) for i in range(1)]
    tailo = poly_tube("tailc", "#F2973A", [(0.9, 1.0, 0.3), (1.3, 1.1, 0.5), (1.5, 1.0, 0.9), (1.4, 0.9, 1.3)], 0.09, cat)
    pupils = [o for o in bpy.data.objects if o.name.startswith("catpup")]
    TG, TO, TD = W_("gato"), W_("olhar"), W_("diferente")
    sw = sphere("sweat", "#7EC8F2", (0, 0, 0), 0.05, (0.8, 0.5, 1.2), sub=1)
    def frame(t):
        head.rotation_euler = (0, math.sin(t*1.4)*0.04, -0.35 + ease((t-TG)/0.5)*0.15)
        cat.location.z = -0.08*ease((t-TO)/0.5)          # abaixa para o bote
        cat.rotation_euler = (0, 0, math.sin(t*0.8)*0.03)
        dil = lerp(1.0, 1.8, ease((t-TO)/0.4))          # pupila dilata (modo caça)
        for p in pupils: p.scale = (dil, 0.3, 1.25*min(dil, 1.4))
        tailo.rotation_euler = (0, math.sin(t*5)*0.12*(1+ease((t-TO)/0.4)*2), 0)
        arms = (lerp(8, 165, eout((t-TD-0.15)/0.2)), lerp(8, 158, eout((t-TD-0.2)/0.2))) if t > TD+0.15 else (8, 8)
        leo.pose(t, loc=(-0.5, -0.6, 0), s=0.8, rotz=0.4, expr=[[0, "neutral"], [TG, "worried"], [TD+0.15, "shock"]], arms=arms, look=(20, 8))
        sw.hide_render = t < TG; sw.location = (-0.45, -0.95, 1.55 - ((t*0.4) % 0.15))
        keys = [(0, (-0.1, -6.4, 1.3), (0.05, 0.3, 1.05), 34), (TD+0.35, (-0.05, -5.8, 1.25), (0.05, 0.3, 1.05), 34),
                (TD+0.7, (-1.3, -3.4, 1.4), (-0.6, -0.5, 1.25), 40), (sc_["dur"], (-1.35, -3.25, 1.4), (-0.6, -0.5, 1.25), 40)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S3 (caixa de fósforo)
def build_s3(sc_, W_):
    setup_render("#3A3358")
    cube("table", "#A0623A", (0, 0, -0.1), (16, 14, 0.2), bevel=0)
    for k in range(-8, 9): cube(f"grain{k}", "#93582F", (0, k*0.8, 0.002), (16, 0.04, 0.01), bevel=0)
    # caneca gigante e lápis
    cyl("mug", "#F4F1EA", (-2.4, 2.6, 2.0), 1.6, 4.0, bevel=0.1, verts=64)
    cyl("mugband", "#E63946", (-2.4, 2.6, 2.7), 1.62, 0.5, bevel=0, verts=64)
    torus("mughandle", "#F4F1EA", (-0.75, 2.6, 2.0), 0.9, 0.22, rot=(math.pi/2, 0, 0))
    pen = empty("pencil", (1.5, 2.2, 0.25)); pen.rotation_euler = (0, math.pi/2, 0.25)
    cyl("penb", "#FFC93C", (0, 0, 0), 0.25, 5, pen, bevel=0.02, verts=6)
    bpy.ops.mesh.primitive_cone_add(radius1=0.25, depth=0.6, vertices=6, location=(0, 0, 2.8)); c = bpy.context.object; c.parent = pen; setmat(c, "#F3D19A")
    cyl("eraser", "#F28B8B", (0, 0, -2.65), 0.25, 0.4, pen, bevel=0.03, verts=6)
    # caixa de fósforo (gaveta aberta) — Léo deitado dentro
    box = empty("box", (0, 0, 0))
    cube("shell", "#3D5BD9", (0, 0.9, 0.45), (2.6, 1.6, 0.9), box, bevel=0.03)
    cube("label", "#FFE9B8", (0, 0.09, 0.45), (1.6, 0.02, 0.4), box, bevel=0.01)
    cube("strip", "#6F3B22", (0, 0.9, 0.91), (2.6, 1.6, 0.02), box, bevel=0) if False else None
    cube("drawer_bot", "#E9D5AE", (0, -0.9, 0.05), (2.5, 1.5, 0.1), box, bevel=0.01)
    for sx in (-1, 1): cube(f"drawer_side{sx}", "#E9D5AE", (sx*1.22, -0.9, 0.3), (0.06, 1.5, 0.5), box, bevel=0.01)
    cube("drawer_front", "#D9363E", (0, -1.62, 0.3), (2.5, 0.06, 0.55), box, bevel=0.01)
    text3d("txt", "FÓSFOROS", "#FFE9B8", (0, -1.66, 0.3), 0.28, box, extrude=0.01)
    for k in range(3):
        m = empty(f"match{k}", (1.8+k*0.35, -1.2+k*0.2, 0.06)); m.rotation_euler = (0, math.pi/2, 0.4+k*0.2)
        cyl(f"stick{k}", "#F3D19A", (0, 0, 0), 0.05, 1.6, m, bevel=0.01, verts=8)
        sphere(f"tip{k}", "#C0392B", (0, 0, 0.82), 0.09, (1, 1, 1.3), m, sub=1)
    pil = sphere("tpil", "#FFFFFF", (-0.85, -0.9, 0.2), 0.2, (1, 1.3, 0.45), sub=1)
    blanket = cube("tblanket", "#F28B8B", (0.25, -0.9, 0.32), (1.5, 1.3, 0.12), bevel=0.05)
    for k in range(5): sphere(f"dot{k}", "#FFFFFF", (-0.3+k*0.28, -1.0+(k % 2)*0.35, 0.39), 0.06, (1, 1, 0.3), sub=0)
    cam = camera(40); leo = LeoCtl("leo")
    zz = [text3d(f"z{k}", "Z", "#FFFFFF", (0, 0, 0), 0.18+k*0.06, extrude=0.02) for k in range(3)]
    TF = W_("fósforo")
    def frame(t):
        leo.pose(t, loc=(0.3, -0.9, 0.3), s=0.62, rotx=-math.pi/2, rotz=math.pi/2, expr=[[0, "sleep"], [TF+0.2, "neutral"]],
                 mouth=[[0, None], [TF+0.2, "line"]], arms=(8, 8), look=(0, -10))
        for k, z in enumerate(zz):
            ph = (t*0.6 + k*0.33) % 1
            z.location = (-0.55+ph*0.35+k*0.08, -1.3, 0.6+ph*0.6+k*0.1); z.hide_render = t > TF
            z.rotation_euler = (math.pi/2, 0, 0.3)
        keys = [(0, (1.2, -5.5, 3.4), (0, -0.5, 0.4), 34), (TF+0.2, (0.9, -4.8, 3.0), (0, -0.6, 0.4), 36),
                (TF+0.5, (-0.4, -2.3, 1.4), (-0.75, -0.9, 0.45), 42), (sc_["dur"], (-0.45, -2.2, 1.35), (-0.75, -0.9, 0.45), 42)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S4 (formiga)
def build_s4(sc_, W_):
    setup_render("#CDEBF2")
    cube("soil", "#8A5A3C", (0, 0, -0.1), (30, 30, 0.2), bevel=0)
    r = random.Random(3)
    for k in range(70):
        sphere(f"peb{k}", r.choice(["#7A4C30", "#9C6A48", "#6B4129"]), (r.uniform(-6, 6), r.uniform(-3, 8), 0.0), r.uniform(0.05, 0.22), (1, 1, 0.5), sub=1, seg=10)
    blades = []
    for k in range(14):
        x = -5 + k*0.8 + r.uniform(-0.2, 0.2); y = r.uniform(2, 6)
        cu_pts = [(x, y, 0), (x+0.1, y, 2.5), (x+0.4, y, 5), (x+0.9, y, 7.5)]
        b = poly_tube(f"blade{k}", r.choice(["#7CC46A", "#5FAF57", "#8FD27A"]), cu_pts, 0.18)
        b.data.bevel_depth = 0.0; b.data.extrude = 0.0
        b.data.bevel_depth = 0.22; b.scale = (1, 0.35, 1)
        blades.append(b)
    sugar = cube("sugarL", "#FFFFFF", (0.35, -0.3, 0.38), (0.75, 0.75, 0.75), bevel=0.06, rot=(0, 0, 0.3))
    for k in range(6): sphere(f"sp{k}", "#E1E9F5", (0.35+r.uniform(-0.3, 0.3), -0.69, 0.38+r.uniform(-0.3, 0.3)), 0.05, (1, 0.3, 1), sub=0)
    # formiga
    ant = empty("ant", (0, 0, 0))
    sphere("abdomen", "#5A2E1C", (0.75, 0, 0.55), 0.5, (1.3, 0.95, 0.9), ant, sub=2)
    sphere("thorax", "#6E3A24", (0.0, 0, 0.6), 0.3, (1.3, 0.85, 0.85), ant, sub=2)
    ahead = sphere("ahead", "#6E3A24", (-0.55, 0, 0.75), 0.33, (1, 0.95, 0.9), ant, sub=2)
    for sy in (-1, 1):
        sphere(f"aeye{sy}", "#FFFFFF", (-0.75, sy*0.17, 0.85), 0.09, (0.6, 1, 1), ant, sub=1)
        sphere(f"apup{sy}", INKC, (-0.8, sy*0.17, 0.85), 0.05, (0.5, 1, 1), ant, sub=1)
        poly_tube(f"ant_an{sy}", INKC, [(-0.65, sy*0.12, 1.0), (-0.85, sy*0.25, 1.45), (-1.2, sy*0.35, 1.5)], 0.025, ant)
    legs = []
    for i, lx in enumerate((-0.25, 0.0, 0.25)):
        for sy in (-1, 1):
            g = empty(f"ant_leg{i}{sy}", (lx, sy*0.2, 0.55), ant)
            poly_tube(f"ant_lt{i}{sy}", INKC, [(0, 0, 0), (0, sy*0.45, 0.15), (0, sy*0.7, -0.55)], 0.035, g)
            legs.append((g, i, sy))
    crumb = empty("crumb", (0, 0, 1.3), ant)
    sphere("crumbm", "#D9A35B", (0, 0, 0), 0.45, (1.2, 1, 0.8), crumb, sub=2)
    for k in range(6): sphere(f"cr{k}", "#B9823E", (r.uniform(-0.3, 0.3), -0.35, r.uniform(-0.2, 0.2)), 0.05, sub=0, parent=crumb)
    cam = camera(36); leo = LeoCtl("leo")
    sw = sphere("sweat", "#7EC8F2", (0, 0, 0), 0.05, (0.8, 0.5, 1.2), sub=1)
    TA, TF = W_("formiga"), W_("forte")
    def frame(t):
        ax = lerp(3.0, 0.5, ease(t/(TA+1.0))) - max(0, t-TF-0.3)*1.6
        ant.location = (ax, 1.6, 0.0); ant.rotation_euler = (0, 0, math.pi); ant.scale = (0.85, 0.85, 0.85)
        for g, i, sy in legs:
            g.rotation_euler = (math.sin(t*14+i*2+(sy > 0)*math.pi)*0.35, 0, 0)
        crumb.location.z = 1.35 + math.sin(t*14)*0.03
        jit = math.sin(t*40)*0.01
        leo.pose(t, loc=(-0.45+jit, -0.3, 0), s=1.0, rotz=0.9, fwd=14, expr=[[0, "strain"], [TF+0.1, "worried"]],
                 arms=((25, 75), (25, 75)), look=(0, -6 if t < TF else 10), tilt=0)
        sw.hide_render = False; sw.location = (-0.75, -0.6, 1.95-((t*0.5) % 0.2))
        keys = [(0, (0.3, -7.6, 2.1), (0.1, 0.6, 1.25), 30), (TF, (0.2, -7.0, 2.0), (0.1, 0.6, 1.25), 30),
                (TF+0.3, (-0.3, -4.6, 1.7), (-0.25, 0.2, 1.3), 34), (sc_["dur"], (-0.3, -4.4, 1.7), (-0.25, 0.2, 1.3), 34)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S5 (ácaro)
def build_s5(sc_, W_):
    setup_render("#3A2D47")
    r = random.Random(11)
    dust = []
    for k in range(70):
        o = sphere(f"dust{k}", r.choice(["#E9D9C0", "#CDBBA0", "#BFA3C9"]), (r.uniform(-6, 6), r.uniform(1, 9), r.uniform(-2, 7)), r.uniform(0.04, 0.15), sub=1, seg=16)
        dust.append((o, o.location.copy(), r.uniform(0.05, 0.3), r.uniform(0, 6)))
    for k in range(3):
        pts = [(r.uniform(-5, 5), r.uniform(5, 9), r.uniform(-1, 6)) for _ in range(4)]
        poly_tube(f"fiber{k}", "#5E4F78", pts, 0.08)
    mite = empty("mite", (0, 0, 0))
    sphere("mbody", "#EED8B6", (0, 0, 0), 1.1, (1.25, 1.0, 0.75), mite, sub=2)
    sphere("mshine", "#FFFFFF", (-0.3, -0.6, 0.45), 0.35, (1.2, 0.5, 0.4), mite, sub=1)
    mhead = sphere("mhead", "#D9B98F", (-1.35, 0, 0.05), 0.42, (1, 0.9, 0.8), mite, sub=2)
    for sy in (-1, 1):
        sphere(f"meye{sy}", "#FFFFFF", (-1.55, sy*0.2, 0.25), 0.12, sub=1, parent=mite)
        sphere(f"mpup{sy}", INKC, (-1.65, sy*0.2, 0.25), 0.06, sub=1, parent=mite)
    mand = []
    for sy in (-1, 1):
        g = empty(f"mand{sy}", (-1.7, sy*0.12, -0.05), mite)
        poly_tube(f"mandt{sy}", "#5B4630", [(0, 0, 0), (-0.25, sy*0.08, 0), (-0.35, -sy*0.05, 0)], 0.04, g); mand.append((g, sy))
    mlegs = []
    for k in range(4):
        for sy in (-1, 1):
            g = empty(f"mleg{k}{sy}", (-0.6+k*0.4, sy*0.85, -0.2), mite)
            poly_tube(f"mlt{k}{sy}", "#E7CDA8", [(0, 0, 0), (0, sy*0.55, 0.25), (-0.1, sy*0.9, -0.55)], 0.07, g); mlegs.append((g, k, sy))
    for k in range(14):
        a = k/14*2*math.pi
        poly_tube(f"hair{k}", "#B49A78", [(math.cos(a)*1.3, math.sin(a)*1.05, 0.2), (math.cos(a)*1.75, math.sin(a)*1.45, 0.6)], 0.015, mite)
    cam = camera(36); leo = LeoCtl("leo")
    TM, TMO = W_("ácaro"), W_("monstro")
    def frame(t):
        for o, p0, sp, ph in dust:
            o.location = (p0.x + math.sin(t*0.5+ph)*0.2, p0.y, p0.z + ((t*sp + ph) % 1)*0.0 + math.sin(t*0.7+ph)*0.15)
        mx = lerp(5.5, 1.9, ease((t-TM+0.3)/1.0))
        mite.location = (lerp(5.0, 0.7, ease((t-TM+0.3)/1.0)), 1.8, 3.3+math.sin(t*2)*0.12); mite.rotation_euler = (0.35, 0.1, math.pi + 0.5); mite.scale = (0.75, 0.75, 0.75)
        for g, k, sy in mlegs: g.rotation_euler = (math.sin(t*8+k+sy)*0.25, 0, 0)
        for g, sy in mand: g.rotation_euler = (0, 0, sy*math.sin(t*10)*0.35)
        arms = (80, 80) if t < TM else (lerp(80, 165, eout((t-TM-0.2)/0.2)), lerp(80, 160, eout((t-TM-0.25)/0.2)))
        leo.pose(t, loc=(-0.25, -0.3, 0.2+math.sin(t*1.7)*0.12), s=1.0, rotz=0.3, roty=math.sin(t*0.8)*0.12, expr=[[0, "worried"], [TM+0.2, "shock"]], arms=arms, look=(-10, 10))
        keys = [(0, (0.1, -7.8, 2.0), (0.1, 0.6, 2.0), 30), (TMO+0.1, (0.1, -7.2, 2.0), (0.1, 0.6, 2.0), 30),
                (TMO+0.4, (-0.1, -6.0, 1.8), (0.1, 0.5, 1.9), 32), (sc_["dur"], (-0.1, -5.8, 1.8), (0.1, 0.5, 1.9), 32)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S6 (bactéria / gota)
def bacterium(name, color, loc, rot, s=1.0):
    g = empty(name, loc); g.rotation_euler = rot; g.scale = (s, s, s)
    capsule(name+"_b", color, (-0.9, 0, 0), (0.9, 0, 0), 0.45, g)
    for k in range(6): sphere(f"{name}_sp{k}", "#FFFFFF", (-0.6+k*0.25, -0.38, 0.1*(k % 2)), 0.07, (1, 0.4, 1), g, sub=0)
    for sy in (-1, 1):
        sphere(f"{name}_e{sy}", "#FFFFFF", (0.95, -0.25, sy*0.15+0.05), 0.09, sub=1, parent=g)
        sphere(f"{name}_p{sy}", INKC, (1.0, -0.32, sy*0.15+0.05), 0.045, sub=0, parent=g)
    fl = poly_tube(name+"_fl", INKC, [(-1.3-k*0.15, 0, 0) for k in range(14)], 0.03, g)
    return g, fl

def wiggle(fl, t, ph=0):
    sp = fl.data.splines[0]
    for k, p in enumerate(sp.points):
        p.co = (-1.3-k*0.15, 0, math.sin(k*0.6-t*12+ph)*0.15, 1)

def build_s6(sc_, W_):
    setup_render("#2F86C9")
    r = random.Random(5)
    bubs = []
    for k in range(30):
        o = sphere(f"bub{k}", "#BFE9FF", (r.uniform(-6, 6), r.uniform(1.5, 9), r.uniform(-3, 7)), r.uniform(0.05, 0.18), sub=2, seg=16)
        sphere(f"bubg{k}", "#FFFFFF", (0, 0, 0), 0.07, (1, 1, 1), o, sub=1, seg=12).location = (-0.03, -0.12, 0.05)
        bubs.append((o, o.location.copy(), r.uniform(0.4, 1.0)))
    for k in range(5):
        cube(f"ray{k}", "#5FB4E8", (-4+k*2.2, 7, 5), (0.6, 0.05, 14), bevel=0, rot=(0, 0.35, 0))
    bA, fA = bacterium("bA", "#7DDB6A", (2.4, 2.5, 3.6), (0.2, 0.3, 2.9), 1.1)
    bB, fB = bacterium("bB", "#B48CF0", (-2.6, 1.5, -0.6), (0.3, -0.2, 0.4), 1.0)
    bC, fC = bacterium("bC", "#FFB36B", (2.6, 0.5, -0.4), (0, 0.5, 2.4), 0.9)
    cam = camera(36); leo = LeoCtl("leo")
    TG = W_("oceano")
    def frame(t):
        for o, p0, sp in bubs: o.location = (p0.x + math.sin(t*2+p0.y)*0.08, p0.y, (p0.z + t*sp + 3) % 10 - 3)
        bA.location.x = 2.4 - t*0.15; bB.location.x = -2.6 + t*0.12; bC.location.z = -0.4 + t*0.1
        wiggle(fA, t); wiggle(fB, t, 1); wiggle(fC, t, 2)
        arms = (95+math.sin(t*6)*40, 95+math.sin(t*6+1)*40)
        leo.pose(t, loc=(0, 0, 0.6+math.sin(t*2)*0.12), s=1.0, rotz=-0.2, roty=math.sin(t*1.3)*0.1, expr=[[0, "shock"], [TG+0.3, "worried"]],
                 mouth=[[0, None], [1.2, "small"], [TG+0.3, None]], arms=arms, look=(0, 6))
        keys = [(0, (0.4, -5.6, 1.9), (0, 0.2, 1.6), 36), (TG+0.1, (0.3, -6.2, 1.9), (0, 0.2, 1.6), 36),
                (TG+0.8, (0.2, -9.8, 2.6), (0, 0.5, 1.9), 34), (sc_["dur"], (0.2, -10.2, 2.6), (0, 0.5, 1.9), 34)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S7 (vírus)
def build_s7(sc_, W_):
    setup_render("#4E2160")
    big, fbig = bacterium("big", "#5FAF57", (0, 9, 6.5), (0.1, 0, 0.1), 5.0)
    vir = empty("virus", (0, 0, 0)); spin = empty("vspin", (0, 0, 0), vir)
    sphere("vcore", "#D9367A", (0, 0, 0), 0.9, sub=2, parent=spin)
    rr_ = random.Random(2)
    for k in range(26):
        z = 1 - 2*(k+0.5)/26; rad = math.sqrt(1-z*z); a = k*2.399
        d = Vector((math.cos(a)*rad, math.sin(a)*rad, z))
        capsule(f"spk{k}", "#F27CA6", tuple(d*0.85), tuple(d*1.3), 0.05, spin)
        sphere(f"spkb{k}", "#FFC93C", tuple(d*1.36), 0.11, parent=spin, sub=1, seg=12)
    for k in range(9):
        sphere(f"vsp{k}", "#A8205A", (rr_.uniform(-0.5, 0.5), -0.75, rr_.uniform(-0.5, 0.5)), 0.12, (1, 0.4, 1), spin, sub=0)
    for sx in (-1, 1):
        sphere(f"veye{sx}", "#FFFFFF", (sx*0.3, -0.84, 0.15), 0.18, (1, 0.4, 1), vir, sub=1)
        sphere(f"vpup{sx}", INKC, (sx*0.3-0.05, -0.92, 0.14), 0.08, (1, 0.4, 1), vir, sub=1)
        b = cube(f"vbrow{sx}", INKC, (sx*0.3, -0.88, 0.42), (0.3, 0.04, 0.06), vir, bevel=0.01, rot=(0, sx*0.35, 0))
    arc_tube("vmouth", INKC, (0, -0.9, -0.38), 0.18, 0.03, math.radians(20), math.radians(160), vir)
    cam = camera(36); leo = LeoCtl("leo")
    q = empty("q", (0, 0, 0))
    star = sphere("qstar", "#FFD93D", (0, 0, 0), 0.32, (1, 0.25, 1), q, sub=1)
    text3d("qtxt", "?", "#4A63E7", (0, -0.1, -0.12), 0.5, q, extrude=0.03)
    TV = W_("vírus")
    def frame(t):
        vx = lerp(6.0, 1.5, eout((t-TV+0.2)/0.9))
        vir.location = (lerp(5.0, 0.55, eout((t-TV+0.2)/0.9)), 1.2, 3.1+math.sin(t*1.5)*0.1); spin.rotation_euler = (t*0.3, t*0.5, 0)
        vir.rotation_euler = (0, 0, 0.25)
        wiggle(fbig, t)
        arms = (8, 8) if t < TV+0.2 else (lerp(8, 85, eout((t-TV-0.2)/0.2)), lerp(8, 160, eout((t-TV-0.25)/0.2)))
        leo.pose(t, loc=(-0.35, -0.3, 0), s=1.0, rotz=0.25, expr=[[0, "neutral"], [TV+0.2, "shock"]], arms=arms, look=(10, 14))
        q.hide_render = t < TV+0.5
        for c in q.children: c.hide_render = t < TV+0.5
        qs = back((t-TV-0.5)/0.3)
        q.location = (-0.75, -0.6, 2.45); q.scale = (qs, qs, qs); q.rotation_euler = (0, math.sin(t*6)*0.15, 0)
        keys = [(0, (0.1, -7.8, 2.0), (0.1, 0.5, 2.0), 30), (TV+0.9, (0.1, -7.3, 2.0), (0.1, 0.5, 2.0), 30),
                (TV+1.2, (-0.1, -6.2, 1.9), (0.0, 0.4, 1.95), 32), (sc_["dur"], (-0.1, -6.0, 1.9), (0.0, 0.4, 1.95), 32)]
        camkeys(cam, t, keys)
    return frame

# ---------------------------------------------------------------- S8 (átomo)
def build_s8(sc_, W_):
    setup_render("#140F33")
    sc = bpy.context.scene; sc.display.shading.shadow_intensity = 0.2
    r = random.Random(9)
    for k in range(80):
        sphere(f"st{k}", "#FFFFFF", (r.uniform(-12, 12), r.uniform(8, 14), r.uniform(-6, 14)), r.uniform(0.02, 0.06), sub=0, seg=6)
    nuc = empty("nuc", (0, 2.0, 3.4))
    rr_ = random.Random(2)
    for k in range(14):
        v = Vector((rr_.uniform(-1, 1), rr_.uniform(-1, 1), rr_.uniform(-1, 1))).normalized()*rr_.uniform(0, 0.35)
        sphere(f"nu{k}", "#E84A5F" if k % 2 else "#4A7BE8", tuple(v), 0.28, parent=nuc, sub=1, seg=16)
    orbits = [(0.0, 2.8, 0.9, 1.6), (1.05, 2.8, 0.9, -1.25), (2.1, 2.8, 0.9, 1.9)]
    els = []
    for i, (rot, a, b, sp) in enumerate(orbits):
        o = torus(f"orb{i}", "#8FD8FF", (0, 2.0, 3.4), 1.0, 0.012, rot=(math.pi/2, rot, 0)); o.scale = (a, b, 1)
        e = sphere(f"el{i}", "#B8F6FF", (0, 0, 0), 0.16, sub=1)
        trail = [sphere(f"tr{i}{k}", "#6FE8FF", (0, 0, 0), 0.13-k*0.012, sub=0, seg=10) for k in range(8)]
        els.append((rot, a, b, sp, e, trail))
    fly = sphere("fly", "#B8F6FF", (0, 0, 0), 0.2, sub=1)
    lines = [cube(f"spd{k}", "#8FD8FF", (0, 0, 0), (1.4, 0.02, 0.03), bevel=0) for k in range(6)]
    cam = camera(34); leo = LeoCtl("leo")
    TE = W_("Elétrons")
    def P(rot, a, b, th):
        x0, z0 = math.cos(th)*a, math.sin(th)*b
        # elipse no plano XZ (y=2), rotacionada em torno de Y
        return Vector((x0*math.cos(rot) + z0*math.sin(rot), 2.0 - 0.0, 3.4 - x0*math.sin(rot) + z0*math.cos(rot)))
    def frame(t):
        nuc.rotation_euler = (t*0.4, t*0.3, 0)
        nuc.location = (math.sin(t*20)*0.01, 2.0, 3.4)
        for rot, a, b, sp, e, trail in els:
            th = t*sp*2.2
            e.location = P(rot, a, b, th)
            for k, tr in enumerate(trail): tr.location = P(rot, a, b, th - (k+1)*0.07*math.copysign(1, sp))
        on = t > TE
        ph = ((t-TE)*0.9) % 1
        fly.hide_render = not on; fly.location = (lerp(-4, 4, ph), -0.6, 1.55+math.sin(ph*6)*0.1)
        for k, l in enumerate(lines):
            l.hide_render = not on; p = (t*3+k*0.17) % 1
            l.location = (lerp(-4, 4, p), -0.3-k*0.05, 0.8+k*0.25)
        leo.pose(t, loc=(0, 0, 0), s=1.0, expr=[[0, "shock"], [TE+0.6, "dizzy"]], arms=(85+math.sin(t*9)*8, 85+math.sin(t*9+2)*8),
                 tilt=math.sin(t*9)*6 if on else 0, look=(0, 10))
        keys = [(0, (0.0, -7.5, 2.8), (0, 1.0, 2.2), 32), (TE+0.9, (0.0, -7.0, 2.6), (0, 1.0, 2.0), 32),
                (TE+1.2, (0.1, -4.2, 1.6), (0, 0, 1.4), 36), (sc_["dur"], (0.1, -4.0, 1.6), (0, 0, 1.4), 36)]
        camkeys(cam, t, keys, shake=0.03 if on else 0)
    return frame

# ---------------------------------------------------------------- S9 (vazio)
def build_s9(sc_, W_):
    setup_render("#0A0818")
    r = random.Random(4)
    for k in range(120):
        sphere(f"st{k}", "#FFFFFF", (r.uniform(-12, 12), r.uniform(4, 16), r.uniform(-8, 12)), r.uniform(0.015, 0.05), sub=0, seg=6)
    halo = sphere("halo", "#FFE58A", (0, 0.8, 1), 1.0, (1, 0.05, 1), sub=1)
    cam = camera(36); leo = LeoCtl("leo")
    TE = W_("existe")
    def frame(t):
        k = ease(t/(TE+0.5)); s = lerp(1.0, 0.03, k)
        leo.pose(t, loc=(0, 0, lerp(0, 1.4, k)), s=s, expr=[[0, "worried"], [0.9, "shock"]], arms=(85+math.sin(t*4)*10, 85+math.sin(t*4+1)*10), look=(0, 10))
        hs = 0.45*s + 0.06; halo.scale = (hs, 0.05, hs); halo.location = (0, 0.6, lerp(0, 1.4, k)+1.0*s)
        camkeys(cam, t, [(0, (0, -6.5, 1.3), (0, 0, 1.1), 36), (sc_["dur"], (0, -5.6, 1.5), (0, 0, 1.45), 40)])
    return frame

# ---------------------------------------------------------------- S10 (volta ao quarto)
def build_s10(sc_, W_):
    setup_render("#F2D0B4")
    clk, rings = bedroom(); cam = camera(36)
    dot = sphere("dot", "#FFE066", (2.3, 1.62, 1.02), 0.05, sub=1)
    halo = sphere("dothalo", "#FFF3B0", (2.3, 1.64, 1.02), 0.12, (1, 0.2, 1), sub=1)
    tag = text3d("tag", "VOCÊ", "#FFFFFF", (2.3, 1.4, 1.6), 0.32, extrude=0.03)
    arrow = empty("arrow", (2.3, 1.4, 1.3))
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.18, location=(0, 0, 0)); c = bpy.context.object; c.parent = arrow; c.rotation_euler = (math.pi, 0, 0); setmat(c, "#FFFFFF")
    def frame(t):
        clk.rotation_euler = (0, math.sin(t*60)*0.06, math.sin(t*55)*0.04)
        tag.location.z = 1.62 + math.sin(t*5)*0.05; arrow.location.z = 1.33 + math.sin(t*5)*0.05
        hs = 1 + math.sin(t*6)*0.2; halo.scale = (hs, 0.2, hs)
        camkeys(cam, t, [(0, (1.5, -6.4, 2.3), (1.4, 0.9, 1.5), 30), (sc_["dur"], (1.55, -5.9, 2.25), (1.45, 0.9, 1.5), 31)])
    return frame

BUILD = dict(s0=build_s0, s1=build_s1, s2=build_s2, s3=build_s3, s4=build_s4, s5=build_s5, s6=build_s6,
             s7=build_s7, s8=build_s8, s9=build_s9, s10=build_s10)
