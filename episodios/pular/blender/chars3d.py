"""Personagens autorais modelados no Blender e renderizados como PEÇAS de recorte (cut-out):
cabeça (uma imagem por expressão + piscada), tronco, braço, antebraço, 5 mãos, coxa, canela+tênis.
O HyperFrames monta as peças no esqueleto articulado (build/chars.py) e anima.

Uso:  blender -b -P blender/chars3d.py -- <personagem|all> [--test]
Saída: assets/chars/<personagem>/<peça>.png  (fundo transparente)

Coordenadas do "rig" (as mesmas do build): x para a direita, y para BAIXO, pés em y=0, 1 unidade = 1 px na escala 1.
Ombro (±38,-282) · cotovelo -216 · punho -158 · quadril (±16,-170) · joelho -86 · pescoço -296 · cabeça ~ -362.
Só o lado ESQUERDO da tela é modelado; o direito é espelhado no HyperFrames."""
import bpy, math, sys, os, random
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
WHO = argv[0] if argv else "leo"
TEST = "--test" in argv
U = 0.01

EXPRS = ["neutral", "happy", "sad", "shock", "determined", "angry", "smile"]
HANDS = ["open", "fist", "point", "thumb", "peace"]
JOINT = {"head": (0, -296), "torso": (0, 0), "arm": (-38, -282), "fore": (-38, -216), "hand": (-38, -158),
         "thigh": (-16, -170), "shin": (-16, -86)}
BOX = {"head": (-140, 140, -320, 150), "torso": (-100, 100, -340, -30), "arm": (-34, 34, -30, 86),
       "fore": (-30, 30, -18, 74), "hand": (-44, 44, -38, 74), "thigh": (-36, 36, -20, 100), "shin": (-60, 60, -18, 104)}
K = {"head": 3.2, "torso": 3, "arm": 3, "fore": 3, "hand": 3, "thigh": 3, "shin": 3}


def hexc(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


def mixhex(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{int(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def P(x, y, d=0.0):
    """rig (x, y para baixo, profundidade d para a câmera) -> mundo do Blender"""
    return Vector((x * U, -d * U, -y * U))


# ------------------------------------------------------------------ cena
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.eevee.taa_render_samples = 16
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0
    def L(loc, e, col, rot, size=4):
        ld = bpy.data.lights.new("L", "AREA")
        ld.energy, ld.size, ld.use_shadow = e, size, False
        ld.color = hexc(col)[:3]
        o = bpy.data.objects.new("L", ld)
        sc.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = rot
    L((-4, -6, 7), 1400, "#fff4e6", (math.radians(50), 0, math.radians(-30)))   # principal (frente-esquerda-alto)
    L((5, -5, 3), 300, "#b8c4ff", (math.radians(70), 0, math.radians(40)))      # preenchimento frio
    cam = bpy.data.cameras.new("cam")
    cam.type = "ORTHO"
    co = bpy.data.objects.new("cam", cam)
    sc.collection.objects.link(co)
    co.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = co


OUTLINE = None


def outline_mat():
    global OUTLINE
    if OUTLINE:
        return OUTLINE
    m = bpy.data.materials.new("contorno")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = hexc("#0d0a10")
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    m.use_backface_culling = True
    OUTLINE = m
    return m


MATS = {}


def toon(base, shade=None, rim=True, flat=False):
    """cel shading: 2 tons (luz/sombra chapados) + brilho + luz de contorno"""
    key = (base, shade, rim, flat)
    if key in MATS:
        return MATS[key]
    shade = shade or mixhex(mixhex(base, "#000000", .38), "#3a1e5c", .22)
    hi = mixhex(base, "#ffffff", .22)
    m = bpy.data.materials.new("toon")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission")
    if flat:
        em.inputs["Color"].default_value = hexc(base)
    else:
        df = nt.nodes.new("ShaderNodeBsdfDiffuse")
        s2r = nt.nodes.new("ShaderNodeShaderToRGB")
        nt.links.new(df.outputs[0], s2r.inputs[0])
        cr = nt.nodes.new("ShaderNodeValToRGB")
        cr.color_ramp.interpolation = "CONSTANT"
        cr.color_ramp.elements[0].color = hexc(shade)
        cr.color_ramp.elements[1].position = .3
        cr.color_ramp.elements[1].color = hexc(base)
        e3 = cr.color_ramp.elements.new(.92)
        e3.color = hexc(hi)
        nt.links.new(s2r.outputs["Color"], cr.inputs["Fac"])
        out = cr.outputs["Color"]
        if rim:
            lw = nt.nodes.new("ShaderNodeLayerWeight")
            lw.inputs["Blend"].default_value = .45
            rr = nt.nodes.new("ShaderNodeValToRGB")
            rr.color_ramp.interpolation = "CONSTANT"
            rr.color_ramp.elements[0].color = (0, 0, 0, 1)
            rr.color_ramp.elements[1].position = .72
            rr.color_ramp.elements[1].color = (.35, .4, .55, 1)
            nt.links.new(lw.outputs["Facing"], rr.inputs["Fac"])
            add = nt.nodes.new("ShaderNodeMixRGB")
            add.blend_type = "ADD"
            add.inputs["Fac"].default_value = 1
            nt.links.new(out, add.inputs[1])
            nt.links.new(rr.outputs["Color"], add.inputs[2])
            out = add.outputs[0]
        nt.links.new(out, em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    MATS[key] = m
    return m


def finish(o, m, part, expr=None, hand=None, line=True, sub=1, lw=3.2):
    o.data.materials.clear()
    o.data.materials.append(m)
    if sub:
        md = o.modifiers.new("s", "SUBSURF")
        md.levels = md.render_levels = sub
    if line:
        o.data.materials.append(outline_mat())
        md = o.modifiers.new("o", "SOLIDIFY")
        md.thickness = lw * U
        md.offset = 1
        md.use_flip_normals = True
        md.material_offset = 1
    o["part"] = part
    if expr:
        o["expr"] = expr
    if hand:
        o["hand"] = hand
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def sph(part, m, x, y, d, r, sc=(1, 1, 1), rot=(0, 0, 0), **kw):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r * U, location=P(x, y, d), segments=24, ring_count=16)
    o = bpy.context.active_object
    o.scale = (sc[0], sc[2], sc[1])          # sc = (largura x, altura y, profundidade)
    o.rotation_euler = (math.radians(rot[0]), math.radians(rot[2]), math.radians(rot[1]))
    return finish(o, m, part, sub=kw.pop("sub", 0), **kw)


def cap(part, m, a, b, r1, r2=None, d=0, **kw):
    """cápsula afunilada entre dois pontos do rig"""
    r2 = r1 if r2 is None else r2
    A, B = P(a[0], a[1], d), P(b[0], b[1], d)
    v = B - A
    L = v.length
    bpy.ops.mesh.primitive_cone_add(radius1=r1 * U, radius2=r2 * U, depth=L, location=(A + B) / 2, vertices=20)
    o = bpy.context.active_object
    o.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    objs = [o]
    for c, r in ((A, r1), (B, r2)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * U, location=c, segments=20, ring_count=12)
        objs.append(bpy.context.active_object)
    bpy.ops.object.select_all(action="DESELECT")
    for x in objs:
        x.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.join()
    return finish(o, m, part, sub=kw.pop("sub", 0), **kw)


def blob(part, m, x0, x1, y0, y1, d0, d1, taper=0.0, **kw):
    """caixa arredondada (subdividida) para troncos, roupas, sapatos; taper estreita a base"""
    bpy.ops.mesh.primitive_cube_add(location=P((x0 + x1) / 2, (y0 + y1) / 2, (d0 + d1) / 2))
    o = bpy.context.active_object
    o.scale = ((x1 - x0) / 2 * U, (d1 - d0) / 2 * U, (y1 - y0) / 2 * U)
    bpy.ops.object.transform_apply(scale=True)
    if taper:
        for v in o.data.vertices:
            if v.co.z < 0:
                v.co.x *= (1 - taper)
    md = o.modifiers.new("b", "BEVEL")
    md.width = min(x1 - x0, y1 - y0, d1 - d0) * .32 * U
    md.segments = 4
    return finish(o, m, part, sub=kw.pop("sub", 1), **kw)


def tube(part, m, pts, r, d=0, cyclic=False, **kw):
    """linha 3D (sobrancelhas, boca, cílios) — pontos no rig"""
    cu = bpy.data.curves.new("c", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r * U
    cu.bevel_resolution = 3
    sp = cu.splines.new("NURBS")
    sp.points.add(len(pts) - 1)
    for i, (x, y) in enumerate(pts):
        v = P(x, y, d)
        sp.points[i].co = (v.x, v.y, v.z, 1)
    sp.use_endpoint_u = True
    sp.order_u = min(3, len(pts))
    sp.use_cyclic_u = cyclic
    o = bpy.data.objects.new("t", cu)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.active_object
    return finish(o, m, part, line=kw.pop("line", False), sub=0, **kw)


# ------------------------------------------------------------------ rosto
INK = "#140d12"


def eyes(C, expr):
    """olhos grandes cartoon por expressão (objetos marcados com expr)"""
    hx, hy, fd = C["eye_x"], C["eye_y"], C["face_d"]
    white = toon("#ffffff", "#d9dcef", rim=False)
    iris = toon(C["iris"], mixhex(C["iris"], "#000000", .5), rim=False)
    black = toon("#06040a", flat=True)
    shine = toon("#ffffff", flat=True)
    skin = toon(C["skin"])
    for side in (-1, 1):
        ex = side * hx
        if expr == "happy":
            tube("head", toon(INK, flat=True), [(ex - 14, hy + 3), (ex, hy - 10), (ex + 14, hy + 3)], 3.2, d=fd + 6, expr=expr)
            continue
        big = expr == "shock"
        sph("head", white, ex, hy, fd, 18 if big else 16, sc=(1, 1.22, .45), expr=expr, lw=2.2)
        ir = 8 if big else 11
        sph("head", iris, ex - side * 1.5, hy + 3, fd + 5, ir, sc=(1, 1.08, .35), expr=expr, line=False)
        sph("head", black, ex - side * 1.5, hy + 3, fd + 7, ir * .55, sc=(1, 1.08, .3), expr=expr, line=False)
        sph("head", shine, ex + 3, hy - 3, fd + 9, 3.6, sc=(1, 1, .3), expr=expr, line=False)
        sph("head", shine, ex - 4, hy + 8, fd + 9, 1.7, sc=(1, 1, .3), expr=expr, line=False)
        if expr in ("sad", "determined", "angry"):
            tilt = (14 if expr == "sad" else -12) * side
            sph("head", skin, ex, hy - 17, fd + 4, 19, sc=(1.1, .55, .5), rot=(0, 0, tilt), expr=expr, lw=2.2)
        tube("head", toon(INK, flat=True), [(ex - 17, hy - 6), (ex - 4, hy - 20), (ex + 12, hy - 18), (ex + side * 22, hy - 14)],
             2.8, d=fd + 9, expr=expr)


def brows(C, expr):
    m = toon(C.get("brow", C["hair"]), flat=True)
    bx, by, fd = C["eye_x"], C["eye_y"] - 30, C["face_d"] + 2
    for side in (-1, 1):
        o = {"angry": (6, 10), "determined": (2, 8), "sad": (-4, -10), "shock": (-12, -2)}.get(expr, (-6, 0))
        inner, outer = o[1], o[0]
        if expr == "sad":
            inner, outer = -8, 4
        tube("head", m, [(side * (bx + 14), by + outer), (side * bx, by - 4 + min(inner, outer)), (side * (bx - 14), by + inner)],
             4.2, d=fd, expr=expr)


def mouth(C, expr):
    my, fd = C["eye_y"] + 42, C["face_d"] - 4
    ink = toon(INK, flat=True)
    dark = toon("#4a0c16", flat=True)
    tongue = toon("#e2556a", flat=True)
    teeth = toon("#ffffff", flat=True)
    if expr == "happy":
        sph("head", dark, 0, my + 4, fd, 17, sc=(1.1, .8, .3), expr=expr, lw=2.5)
        sph("head", tongue, 0, my + 11, fd + 3, 9, sc=(1, .55, .25), expr=expr, line=False)
        sph("head", teeth, 0, my - 4, fd + 4, 13, sc=(1.1, .25, .2), expr=expr, line=False)
    elif expr == "shock":
        sph("head", dark, 0, my + 4, fd, 10, sc=(1, 1.3, .3), expr=expr, lw=2.5)
        sph("head", tongue, 0, my + 10, fd + 3, 6, sc=(1, .6, .25), expr=expr, line=False)
    elif expr == "angry":
        sph("head", dark, 0, my + 4, fd, 15, sc=(1, .45, .3), expr=expr, lw=2.5)
        sph("head", teeth, 0, my + 2, fd + 3, 12, sc=(1, .2, .2), expr=expr, line=False)
    else:
        pts = {"smile": [(-15, my - 2), (0, my + 8), (15, my - 2)], "sad": [(-12, my + 6), (0, my - 2), (12, my + 6)],
               "determined": [(-12, my + 2), (0, my), (12, my + 3)]}.get(expr, [(-10, my + 1), (0, my + 3), (10, my + 1)])
        tube("head", ink, pts, 3, d=fd + 4, expr=expr)


def blink_lids(C):
    skin = toon(C["skin"])
    for side in (-1, 1):
        sph("blink", skin, side * C["eye_x"], C["eye_y"], C["face_d"] + 6, 19, sc=(1.05, 1.25, .45), lw=2.2)
        tube("blink", toon(INK, flat=True), [(side * C["eye_x"] - 15, C["eye_y"] + 4), (side * C["eye_x"], C["eye_y"] + 8),
                                             (side * C["eye_x"] + 15, C["eye_y"] + 4)], 2.8, d=C["face_d"] + 14)


# ------------------------------------------------------------------ peças comuns
def head_base(C):
    hy = -362
    skin = toon(C["skin"])
    sph("head", skin, 0, hy, 0, 62, sc=(1, 1.08, .95), sub=0)
    for side in (-1, 1):
        sph("head", skin, side * 60, hy + 6, -6, 13, sc=(.7, 1.1, .6))
    sph("head", toon(mixhex(C["skin"], "#a04040", .15)), 3, hy + 18, 58, 7, sc=(1, .9, .8), lw=2.2)   # nariz
    # bochechas rosadas
    for side in (-1, 1):
        sph("head", toon(mixhex(C["skin"], "#ff6060", .35), rim=False), side * 34, hy + 22, 50, 10, sc=(1.3, .7, .2), line=False)
    for e in EXPRS:
        eyes(C, e)
        brows(C, e)
        mouth(C, e)
    blink_lids(C)


def limbs(C):
    skin = toon(C["skin"])
    top = toon(C["top"])
    sl = C.get("sleeve", "short")
    # braço (ombro -282 -> cotovelo -216)
    cap("arm", top if sl == "long" else skin, (-38, -284), (-38, -214), 11 if sl == "long" else 9, 10 if sl == "long" else 8)
    if sl == "short":
        cap("arm", top, (-38, -288), (-38, -250), 15, 14)
    cap("fore", top if sl == "long" else skin, (-38, -218), (-38, -164), 10 if sl == "long" else 8, 9 if sl == "long" else 7)
    if sl == "long":
        cap("fore", toon(C.get("cuff", mixhex(C["top"], "#000000", .25))), (-38, -172), (-38, -160), 11, 11)
    if C.get("wrist"):
        cap("fore", toon(C["wrist"]), (-38, -176), (-38, -168), 9, 9)
    # perna (quadril -170 -> joelho -86 -> pé)
    leg_m = toon(C["legs"]) if C.get("legs") else skin
    cap("thigh", leg_m, (-16, -172), (-16, -84), 14, 12)
    if C.get("shorts"):
        cap("thigh", toon(C["shorts"]), (-16, -176), (-16, -128), 19, 17)
    cap("shin", leg_m, (-16, -88), (-16, -16), 12, 10)
    if C.get("sock"):
        cap("shin", toon(C["sock"]), (-16, -44), (-16, -14), 11.5, 11)
        if C.get("sock_stripe"):
            cap("shin", toon(C["sock_stripe"]), (-16, -38), (-16, -32), 12.2, 12.2, line=False)
    if C.get("kneepad"):
        sph("shin", toon(C["kneepad"]), -16, -82, 6, 15, sc=(1, 1.1, .8))
    if C.get("brace"):
        cap("shin", toon(C["brace"]), (-16, -92), (-16, -70), 14, 14)
    shoe(C)


def shoe(C):
    col = C["shoe"]
    if C.get("spring_boots"):
        blob("shin", toon(col), -46, 6, -30, -4, -16, 22)
        for k in range(4):
            tube("shin", toon("#cfd4dc"), [(-36, -2 + k * 4), (-2, -4 + k * 4), (-36, -6 + k * 4)], 2.2, d=4, line=True)
        return
    if C.get("slipper"):
        blob("shin", toon(col), -48, 8, -16, 0, -16, 26)
        return
    blob("shin", toon(col), -50, 8, -26, -2, -18, 26)
    blob("shin", toon("#f2efe6"), -54, 10, -8, 2, -20, 28)                     # sola
    sph("shin", toon("#f2efe6"), -40, -14, 16, 11, sc=(1, .8, .6))              # biqueira
    for k in range(3):
        tube("shin", toon("#ffffff", flat=True), [(-26 + k * 8, -24), (-20 + k * 8, -18)], 1.6, d=26)
    if C.get("tape"):
        blob("shin", toon("#b9bcc4"), -30, -6, -22, -10, -20, 28, line=False)


def hands(C):
    skin = toon(C["skin"])
    wx, wy = -38, -158
    for h in HANDS:
        if h == "open":
            sph("hand", skin, wx, wy + 16, 0, 13, sc=(1, 1.15, .55), hand=h)
            for i, fx in enumerate((-9, -3, 3, 9)):
                cap("hand", skin, (wx + fx, wy + 22), (wx + fx * 1.5, wy + 40 + (i in (1, 2)) * 4), 4, 3.5, hand=h)
            cap("hand", skin, (wx + 9, wy + 10), (wx + 20, wy + 22), 4.5, 4, hand=h)
        else:
            sph("hand", skin, wx, wy + 18, 0, 14, sc=(1, 1.1, .8), hand=h)
            for fx in (-8, -2.5, 3, 8.5):
                sph("hand", skin, wx + fx, wy + 30, 6, 4.8, sc=(1, 1, 1), hand=h, lw=2)
            if h == "point":
                cap("hand", skin, (wx - 3, wy + 28), (wx - 3, wy + 56), 4.6, 4, hand=h)
            if h == "peace":
                cap("hand", skin, (wx - 5, wy + 28), (wx - 10, wy + 56), 4.4, 4, hand=h)
                cap("hand", skin, (wx + 3, wy + 28), (wx + 8, wy + 56), 4.4, 4, hand=h)
            if h == "thumb":
                cap("hand", skin, (wx + 9, wy + 26), (wx + 7, wy + 52), 5, 4.5, hand=h)
            else:
                cap("hand", skin, (wx + 11, wy + 10), (wx + 6, wy + 26), 5, 4.5, hand=h)


# ------------------------------------------------------------------ elenco
def leo():
    C = dict(skin="#8d5a3b", hair="#1b120d", iris="#4a2a12", top="#1f8f8f", sleeve="long", cuff="#1a6f6f",
             shorts="#8a7a52", sock="#e8e2d0", sock_stripe="#d83a3a", shoe="#9aa0aa", tape=True, eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    hair = toon(C["hair"])
    for (x, y, r) in ((0, hy - 70, 48), (-42, hy - 56, 36), (42, hy - 56, 36), (-26, hy - 86, 34), (26, hy - 86, 34),
                      (-56, hy - 26, 26), (56, hy - 26, 26), (0, hy - 96, 30)):
        sph("head", hair, x, y, -10, r, sc=(1, .9, .9))
    blob("head", toon("#ff7a1a"), -64, 64, hy - 52, hy - 38, -40, 62, sub=1)            # faixa de suor laranja
    # tronco: moletom largão + capuz + bolso + remendo de moeda + bermuda
    blob("torso", toon(C["top"]), -46, 46, -294, -150, -26, 30, taper=.08)
    blob("torso", toon("#1a7777"), -36, 36, -306, -282, -34, 4)                          # capuz dobrado
    blob("torso", toon("#1a7777"), -28, 28, -200, -168, 20, 34, line=True)              # bolso canguru
    sph("torso", toon("#f2c33a"), 22, -250, 32, 11, sc=(1, 1, .3), lw=2.4)              # remendo: moeda
    tube("torso", toon("#c99a1f", flat=True), [(18, -255), (22, -245), (26, -255)], 1.6, d=36)
    blob("torso", toon(C["shorts"]), -40, 40, -168, -128, -24, 26)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)                          # pescoço
    tube("torso", toon("#e8e2d0", flat=True), [(-6, -280), (-8, -246)], 1.6, d=34)        # cordão do capuz
    tube("torso", toon("#e8e2d0", flat=True), [(6, -280), (8, -246)], 1.6, d=34)
    limbs(C)
    hands(C)


def vo():
    C = dict(skin="#e2b28e", hair="#d9d9e0", brow="#bdbdc8", iris="#4a5a6a", top="#d9a23a", sleeve="long", cuff="#b9861f",
             legs="#e2b28e", brace="#3a4a8a", shoe="#ff9db8", slipper=True, eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    hair = toon(C["hair"])
    sph("head", hair, 0, hy - 50, -6, 60, sc=(1.05, .75, .95))
    sph("head", hair, 0, hy - 104, -14, 30)                                                 # coque
    cap("head", toon("#e8b92e"), (-18, hy - 120), (22, hy - 96), 3, 3)                     # lápis no coque
    for side in (-1, 1):   # óculos redondos
        tube("head", toon("#6a4a2a", flat=True), [(side * 24 + 21 * math.cos(a), hy + 2 + 21 * math.sin(a)) for a in
                                                  [i / 12 * 2 * math.pi for i in range(13)]], 2.6, d=66)
    tube("head", toon("#6a4a2a", flat=True), [(-3, hy), (3, hy)], 2.6, d=66)
    tube("head", toon("#9a8a6a", flat=True), [(-44, hy + 6), (-30, hy + 60), (30, hy + 60), (44, hy + 6)], 1.2, d=40)   # cordinha
    blob("torso", toon("#9b7ab8"), -44, 44, -290, -40, -24, 26, taper=-.25)               # vestido lilás
    blob("torso", toon(C["top"]), -48, 48, -296, -170, -28, 32, taper=-.05)              # cardigã mostarda
    for k in range(4):
        sph("torso", toon("#7a4a1a"), 0, -276 + k * 28, 33, 4.5, sc=(1, 1, .5), lw=2)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)
    limbs(C)
    hands(C)


def canguru():
    C = dict(skin="#e8c09c", hair="#f4f4f6", brow="#f4f4f6", iris="#3a5a7a", top="#5b2a86", sleeve="long", cuff="#e8b92e",
             legs="#5b2a86", shoe="#cfd4dc", spring_boots=True, eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    white = toon(C["hair"])
    for side in (-1, 1):
        sph("head", white, side * 56, hy - 12, -8, 24, sc=(.8, 1.2, .9))
    sph("head", white, 0, hy + 70, 30, 46, sc=(1, 1.9, .5))                                # barba longa
    sph("head", white, 0, hy + 34, 54, 22, sc=(1.6, .5, .4), lw=2.4)                       # bigode
    blob("head", toon("#e8b92e"), -64, 64, hy - 48, hy - 34, -40, 62)                      # faixa dourada de campeão
    blob("torso", toon(C["top"]), -46, 46, -294, -150, -26, 30, taper=.05)
    for side in (-1, 1):
        blob("torso", toon(C["cuff"]), side * 46 - 4, side * 46 + 4, -292, -152, -10, 32, line=False)
    sph("torso", toon("#e8b92e"), 0, -236, 32, 20, sc=(1, 1, .3), lw=2.6)                  # medalhão "1"
    tube("torso", toon("#5b2a86", flat=True), [(-3, -246), (3, -252), (3, -222)], 2.6, d=38)
    blob("torso", toon(C["legs"]), -40, 40, -168, -128, -24, 26)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)
    limbs(C)
    hands(C)


def exec_():
    C = dict(skin="#c99470", hair="#1c120c", iris="#3a2414", top="#4b5160", sleeve="long", cuff="#ffffff", legs="#3f4452",
             shoe="#1a1418", eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    hair = toon(C["hair"])
    sph("head", hair, 0, hy - 44, -2, 62, sc=(1.02, .62, .98))
    sph("head", hair, -24, hy - 50, 30, 30, sc=(1.6, .5, .7))                               # topete lateral
    blob("torso", toon(C["top"]), -48, 48, -294, -148, -26, 30, taper=.06)
    blob("torso", toon("#ffffff"), -14, 14, -296, -240, 24, 34, line=False)                # camisa
    cap("torso", toon("#c0182a"), (0, -290), (0, -220), 5, 7, d=38)                          # gravata
    blob("torso", toon(C["legs"]), -40, 40, -160, -128, -24, 26)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)
    limbs(C)
    hands(C)


def bia():
    C = dict(skin="#a86c48", hair="#2a1408", iris="#3a1e0c", top="#f4f4f6", sleeve="short", legs="#a86c48", sock="#ffffff",
             shoe="#141018", eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    hair = toon(C["hair"])
    sph("head", hair, 0, hy - 40, -4, 64, sc=(1.02, .7, 1))
    for side in (-1, 1):     # tranças
        for k in range(4):
            sph("head", hair, side * 64, hy + 10 + k * 22, -6, 13 - k, sc=(1, 1.1, .9))
        sph("head", toon("#ffd23a"), side * 64, hy + 96, -6, 7)
    blob("torso", toon(C["top"]), -42, 42, -294, -186, -24, 28)
    blob("torso", toon("#1f2e6a"), -50, 50, -192, -112, -28, 30, taper=-.3)                # saia azul-marinho
    blob("torso", toon("#1f2e6a"), -12, 12, -296, -280, 26, 32, line=False)                # gola
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)
    limbs(C)
    hands(C)


def katia():
    C = dict(skin="#6e4430", hair="#120a06", iris="#2a1408", top="#1fb35a", sleeve="none", legs="#6e4430", shorts="#1a2a5a",
             kneepad="#1a1a1a", sock="#ffffff", shoe="#ffffff", eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    hair = toon(C["hair"])
    sph("head", hair, 0, hy - 42, -6, 62, sc=(1.02, .66, .98))
    sph("head", hair, 34, hy - 92, -24, 24, sc=(1, 1.4, .9))                                # rabo de cavalo alto
    sph("head", hair, 56, hy - 60, -30, 18, sc=(1, 1.8, .8))
    blob("torso", toon(C["top"]), -42, 42, -294, -150, -24, 28, taper=.08)
    for side in (-1, 1):
        blob("torso", toon("#ffd23a"), side * 42 - 5, side * 42 + 5, -292, -152, -10, 30, line=False)
    tube("torso", toon("#ffffff", flat=True), [(-10, -262), (10, -262), (10, -222)], 4, d=34)   # número 7
    tube("torso", toon("#e8b92e"), [(-26, -296), (0, -258), (26, -296)], 2, d=32)          # cordão da medalha
    sph("torso", toon("#ffd23a"), 0, -252, 34, 12, sc=(1, 1, .3), lw=2.4)
    blob("torso", toon(C["shorts"]), -40, 40, -166, -130, -24, 26)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 11, 12)
    limbs(C)
    hands(C)


def barao():
    C = dict(skin="#e6b089", hair="#3a2414", iris="#3a2414", top="#b81f34", sleeve="long", cuff="#e8b92e", legs="#2a2232",
             shoe="#141018", eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    sph("head", toon("#3a2414"), 0, hy + 30, 58, 16, sc=(2.8, .6, .4), lw=2.4)               # bigode
    for side in (-1, 1):
        tube("head", toon("#3a2414"), [(side * 30, hy + 30), (side * 50, hy + 20), (side * 52, hy + 8), (side * 44, hy + 6)], 4, d=58)
    hat = toon("#1c1620")
    blob("head", hat, -84, 84, hy - 64, hy - 50, -50, 70)                                   # aba
    blob("head", hat, -50, 50, hy - 170, hy - 58, -30, 50, taper=-.08)                       # copa
    blob("head", toon("#e8b92e"), -52, 52, hy - 86, hy - 70, -32, 52)
    for k in range(5):                                                                     # mola em cima da cartola
        tube("head", toon("#cfd4dc"), [(-16, hy - 172 - k * 10), (16, hy - 176 - k * 10), (-16, hy - 180 - k * 10)], 2.6, d=10)
    sph("head", toon("#d8262c"), 0, hy - 228, 10, 10)
    blob("torso", toon(C["top"]), -60, 60, -294, -146, -34, 40, taper=-.12)                # casaca (gordinho)
    blob("torso", toon("#f2efe6"), -22, 22, -296, -170, 36, 44, line=False)                # colete
    for k in range(4):
        sph("torso", toon("#e8b92e"), 12, -276 + k * 28, 46, 5, sc=(1, 1, .5), lw=2)
    blob("torso", toon(C["legs"]), -44, 44, -160, -128, -26, 28)
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 12, 13)
    limbs(C)
    hands(C)


def seguranca():
    C = dict(skin="#5a3a28", hair="#0d0a08", iris="#100806", top="#1a1a20", sleeve="long", cuff="#101014", legs="#1a1a20",
             shoe="#0a0a0c", eye_x=24, eye_y=-360, face_d=52)
    head_base(C)
    hy = -362
    sph("head", toon("#0d0a08"), 0, hy - 46, -2, 60, sc=(1, .5, .95))
    blob("head", toon("#08080c"), -50, 50, hy - 14, hy + 12, 50, 70, line=True)               # óculos escuros
    blob("torso", toon(C["top"]), -56, 56, -298, -110, -30, 34, taper=-.06)                 # capa de chuva
    blob("torso", toon("#101014"), -44, 44, -308, -286, -36, 6)                              # capuz caído
    tube("torso", toon("#f0c040", flat=True), [(-30, -250), (30, -250)], 3, d=36)            # faixa refletiva
    cap("torso", toon(C["skin"]), (0, -306), (0, -288), 13, 14)
    limbs(C)
    hands(C)


CAST = {"leo": leo, "vo": vo, "canguru": canguru, "exec": exec_, "bia": bia, "katia": katia, "barao": barao, "seguranca": seguranca}


# ------------------------------------------------------------------ render das peças
def render_part(name, part, out, expr=None, hand=None):
    sc = bpy.context.scene
    for o in sc.objects:
        if o.type in ("LIGHT", "CAMERA"):
            continue
        show = o.get("part") == part
        if show and part == "head":
            e = o.get("expr")
            show = (e is None) or (e == expr)
        if show and part == "hand":
            show = o.get("hand") == hand
        o.hide_render = not show
    jx, jy = JOINT[part if part != "blink" else "head"]
    x0, x1, y0, y1 = BOX[part if part != "blink" else "head"]
    k = K[part if part != "blink" else "head"] * (.5 if TEST else 1)
    w, h = x1 - x0, y1 - y0
    cam = sc.camera
    cam.data.ortho_scale = max(w, h) * U
    cam.location = (jx + (x0 + x1) / 2) * U, -10, -(jy + (y0 + y1) / 2) * U
    sc.render.resolution_x, sc.render.resolution_y = int(w * k), int(h * k)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


def build(name):
    reset()
    global OUTLINE
    OUTLINE = None
    MATS.clear()
    CAST[name]()
    d = os.path.join(ROOT, "assets", "chars", name)
    os.makedirs(d, exist_ok=True)
    jobs = [("head", e, None, f"head_{e}") for e in EXPRS] + [("blink", None, None, "blink")]
    jobs += [(p, None, None, p) for p in ("torso", "arm", "fore", "thigh", "shin")]
    jobs += [("hand", None, h, f"hand_{h}") for h in HANDS]
    for part, e, h, fn in jobs:
        if TEST and fn not in ("head_neutral", "torso", "arm", "fore", "thigh", "shin", "hand_open"):
            continue
        render_part(name, part, os.path.join(d, fn + ".png"), expr=e, hand=h)
    print("PRONTO", name)


if __name__ == "__main__":
    for n in (CAST if WHO == "all" else [WHO]):
        build(n)
