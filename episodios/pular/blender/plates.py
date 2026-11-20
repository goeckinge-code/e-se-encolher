"""Cenários (fundos) do episódio renderizados no Blender/Eevee com luz realista:
contraluz, névoa volumétrica, neon com bloom, asfalto molhado com reflexo.
Uso: blender -b -P blender/plates.py -- <nome> [--preview]
Saída: assets/plates/<nome>.jpg (1080x1920)"""
import bpy, bmesh, math, random, sys, os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "plates")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
NAME = argv[0] if argv else "rua"
PREVIEW = "--preview" in argv


# ------------------------------------------------------------------ base
def hexc(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.render.resolution_percentage = 40 if PREVIEW else 75
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 92
    e = sc.eevee
    e.taa_render_samples = 12 if PREVIEW else 24
    e.use_bloom = True
    e.bloom_threshold, e.bloom_intensity, e.bloom_radius = 0.9, 0.12, 6.5
    e.use_ssr = True
    e.use_ssr_refraction = False
    e.ssr_quality, e.ssr_thickness = 0.5, 0.4
    e.use_gtao = True
    e.gtao_distance = 1.2
    e.use_volumetric_lights = True
    e.volumetric_start, e.volumetric_end = 0.5, 80
    e.volumetric_tile_size = "4"
    e.volumetric_samples = 64
    e.use_soft_shadows = True
    e.shadow_cube_size, e.shadow_cascade_size = "1024", "2048"
    sc.view_settings.view_transform = "Filmic"
    sc.view_settings.look = "Medium High Contrast"
    sc.view_settings.exposure = 0.0
    return sc


def mat(name, col, rough=.6, metal=0., emit=None, estr=0., alpha=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(col)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = hexc(emit)
        b.inputs["Emission Strength"].default_value = estr
    return m


def tmat(name, col, col2, rough=(.5, .8), scale=6., bump=.25, metal=0.):
    """material com variação de cor/rugosidade (sujeira) e relevo, coordenadas do objeto"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = hexc(col)
    cr.color_ramp.elements[1].color = hexc(col2)
    cr.color_ramp.elements[0].position = .35
    cr.color_ramp.elements[1].position = .7
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = rough
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = bump
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Metallic"].default_value = metal
    return m


def sky_plane(loc, size, top="#120c22", mid="#3a2a5e", bot="#c47a5a", estr=1.0):
    """céu com degradê emissivo (contraluz / poluição luminosa no horizonte)"""
    m = bpy.data.materials.new("ceu")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = estr
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = hexc(bot)
    cr.color_ramp.elements[1].color = hexc(top)
    e = cr.color_ramp.elements.new(.35)
    e.color = hexc(mid)
    nt.links.new(sep.outputs["Y"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    plane("ceu", m, loc, size, rot=(math.pi / 2, 0, 0))


def obj(mesh_op, name, m, **kw):
    mesh_op(**kw)
    o = bpy.context.active_object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o


def box(name, m, loc, size, rot=(0, 0, 0)):
    o = obj(bpy.ops.mesh.primitive_cube_add, name, m, location=loc, rotation=rot)
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def plane(name, m, loc, size, rot=(0, 0, 0)):
    o = obj(bpy.ops.mesh.primitive_plane_add, name, m, location=loc, rotation=rot)
    o.scale = (size[0] / 2, size[1] / 2, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def cyl(name, m, loc, r, d, rot=(0, 0, 0), v=24):
    return obj(bpy.ops.mesh.primitive_cylinder_add, name, m, location=loc, radius=r, depth=d, rotation=rot, vertices=v)


def text(name, s, m, loc, size, rot=(math.pi / 2, 0, 0), extrude=.03, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.body = s
    o.data.size = size
    o.data.extrude = extrude
    o.data.align_x = align
    o.data.align_y = "CENTER"
    fnt = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if os.path.exists(fnt):
        o.data.font = bpy.data.fonts.load(fnt)
    o.data.materials.append(m)
    return o


def world(top="#0b0814", fog=.035, fog_col="#7d6aa6", strength=1.0):
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    bg.inputs["Color"].default_value = hexc(top)
    bg.inputs["Strength"].default_value = strength
    if fog:
        vs = nt.nodes.new("ShaderNodeVolumePrincipled")
        vs.inputs["Density"].default_value = fog
        vs.inputs["Color"].default_value = hexc(fog_col)
        vs.inputs["Anisotropy"].default_value = 0.55
        nt.links.new(vs.outputs[0], nt.nodes["World Output"].inputs["Volume"])


def light(kind, loc, energy, col="#ffffff", rot=(0, 0, 0), size=.2, spot=None, blend=.4, shadow=True):
    ld = bpy.data.lights.new("L", kind)
    ld.energy = energy
    ld.color = hexc(col)[:3]
    if hasattr(ld, "shadow_soft_size"):
        ld.shadow_soft_size = size
    if kind == "SPOT" and spot:
        ld.spot_size = math.radians(spot)
        ld.spot_blend = blend
    if kind == "AREA":
        ld.size = size
    ld.use_shadow = shadow
    o = bpy.data.objects.new("L", ld)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    return o


def camera(loc, target, lens=28, dof=None, fstop=2.8):
    cd = bpy.data.cameras.new("cam")
    cd.lens = lens
    cd.sensor_fit = "VERTICAL"
    cd.sensor_height = 36
    c = bpy.data.objects.new("cam", cd)
    bpy.context.collection.objects.link(c)
    c.location = loc
    d = Vector(target) - Vector(loc)
    c.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = c
    if dof:
        cd.dof.use_dof = True
        cd.dof.focus_distance = dof
        cd.dof.aperture_fstop = fstop
    return c


def windows_facade(name, x0, x1, z0, z1, y, rnd, lit=.35, wcol=("#ffcf6e", "#ffe2a3", "#ff9d4d", "#cfe7ff"), wall="#2a2235"):
    """fachada com janelas acesas (emissivas) e apagadas"""
    box(name, mat(name + "w", wall, .85), ((x0 + x1) / 2, y + .5, (z0 + z1) / 2), (x1 - x0, 1, z1 - z0))
    dark = mat(name + "d", "#120f18", .2)
    lits = [mat(name + f"l{i}", "#000000", .4, emit=c, estr=rnd.uniform(3, 7)) for i, c in enumerate(wcol)]
    cols = max(2, int((x1 - x0) / 1.6))
    rows = max(1, int((z1 - z0) / 2.2))
    for i in range(cols):
        for j in range(rows):
            wx = x0 + (i + .5) * (x1 - x0) / cols
            wz = z0 + 1.0 + j * 2.2
            if wz > z1 - .8:
                continue
            m = rnd.choice(lits) if rnd.random() < lit else dark
            plane(name + "win", m, (wx, y - .01, wz), (.8, 1.2), rot=(math.pi / 2, 0, 0))


def rain_streaks(rnd, n=0):
    pass  # a chuva é feita no HyperFrames (anima por cima)


# ------------------------------------------------------------------ cenários
def plate_rua(variant=0, signs=(("PADARIA", "#ff3f9e"), ("FARMÁCIA", "#2bff6a"), ("LANCHES", "#38d9ff"), ("BAR", "#ffb02e"))):
    """rua comprida em diagonal; lojas do lado esquerdo-fundo, câmera na calçada olhando a rua"""
    reset()
    rnd = random.Random(7 + variant)
    world("#07050c", fog=.05, fog_col="#9d8cc7", strength=.5)
    sky_plane((0, 70, 18), (140, 60), estr=1.4)
    asphalt = tmat("asf", "#0e0c12", "#1d1a22", rough=(.18, .6), scale=3, bump=.05)
    plane("rua", asphalt, (0, 20, 0), (80, 80))
    side = tmat("calc", "#28232c", "#3a343e", rough=(.15, .6), scale=4, bump=.06)
    # calçada ao longo do eixo Y (rua vai para o fundo)
    box("calcada", side, (-3.0, 20, .09), (4.4, 70, .18))
    box("guia", tmat("guia", "#4a4452", "#5c5560"), (-.8, 20, .09), (.2, 70, .2))
    box("calcada2", side, (6.3, 20, .09), (3.0, 70, .18))
    puddle = mat("poca", "#07060a", .0, metal=.1)
    for _ in range(16):
        plane("poca", puddle, (rnd.uniform(-4.5, 4.5), rnd.uniform(-2, 30), .006), (rnd.uniform(.8, 3.2), rnd.uniform(.5, 1.6)))
    # faixa amarela central
    for k in range(14):
        plane("faixa", mat("fx", "#c9a640", .5), (2.4, -2 + k * 4, .004), (.12, 1.8))
    wall_cols = [("#3a2a2f", "#4e3a3c"), ("#2a2f3a", "#3a4150"), ("#3a3428", "#4f4636"), ("#2f2638", "#43374f")]
    def shops(xface, side_sign, y0, y1, signs, seed):
        r = random.Random(seed)
        y = y0
        i = 0
        while y < y1:
            w = r.uniform(4.2, 5.6)
            nm, col = signs[i % len(signs)]
            wc = r.choice(wall_cols)
            # bloco do prédio (térreo + andares)
            hgt = r.uniform(9, 16)
            box(f"pr{seed}{i}", tmat(f"pw{seed}{i}", wc[0], wc[1], scale=2.5, bump=.4), (xface - side_sign * 3, y + w / 2, hgt / 2), (6, w - .05, hgt))
            glass = mat(f"vit{seed}{i}", "#000000", .3, emit=r.choice(["#ffb860", "#ffd08a", "#ff9e57"]), estr=r.uniform(1.6, 2.6))
            plane(f"vitrine{i}", glass, (xface + side_sign * .01, y + w / 2, 1.5), (w - 1.0, 2.3), rot=(math.pi / 2, 0, math.pi / 2))
            for k in range(3):
                box(f"prat{i}{k}", mat(f"prm{i}{k}", "#2a170c", .7), (xface + side_sign * .05, y + w / 2, .7 + k * .7), (.06, w - 1.2, .06))
                for q in range(int((w - 1.4) / .35)):
                    if r.random() < .7:
                        box("prod", mat(f"pd{i}{k}{q}", r.choice(["#c23b2b", "#2b6bc2", "#e0c040", "#3aa04a", "#e8e8e8"]), .5),
                            (xface + side_sign * .12, y + .9 + q * .35, .82 + k * .7), (.12, .22, .22))
            box(f"toldo{i}", tmat(f"td{seed}{i}", r.choice(["#6a1a24", "#1a3d6a", "#24502a"]), "#2a1012", scale=8),
                (xface + side_sign * .55, y + w / 2, 2.95), (1.1, w - .2, .1), rot=(0, side_sign * math.radians(16), 0))
            text(f"letreiro{i}", nm, mat(f"neon{seed}{i}", "#000000", .3, emit=col, estr=14),
                 (xface + side_sign * .06, y + w / 2, 3.75), .95, rot=(math.pi / 2, 0, side_sign * math.pi / 2))
            light("POINT", (xface + side_sign * .9, y + w / 2, 3.6), 45, col, size=.4)
            light("AREA", (xface + side_sign * .7, y + w / 2, 1.5), 140, "#ffbf75", rot=(0, side_sign * math.radians(90), 0), size=w * .6)
            # janelas dos andares
            dark = mat("jd", "#0d0b12", .15)
            for fl in range(int((hgt - 4.6) / 2.3)):
                for q in range(int(w / 1.5)):
                    lit = r.random() < .35
                    m = mat(f"jl{seed}{i}{fl}{q}", "#000000", .3, emit=r.choice(["#ffcf6e", "#ffe2a3", "#ffa860", "#bcd7ff"]), estr=r.uniform(1.2, 3)) if lit else dark
                    plane("jan", m, (xface + side_sign * .01, y + .75 + q * 1.5, 5.6 + fl * 2.3), (.75, 1.1), rot=(math.pi / 2, 0, math.pi / 2))
            y += w
            i += 1
    shops(-5.2, 1, -4, 40, signs, 3)
    shops(7.8, -1, 4, 50, (("HOTEL", "#ff4fd0"), ("BAR", "#ffb02e"), ("CAFÉ", "#38d9ff")), 9)
    # skyline ao fundo
    for k in range(12):
        bx = -30 + k * 6 + rnd.uniform(-2, 2)
        bh = rnd.uniform(18, 40)
        box(f"sk{k}", tmat(f"skm{k}", "#120e1a", "#1b1624", scale=1), (bx, 58 + rnd.uniform(0, 6), bh / 2), (rnd.uniform(4, 6), 4, bh))
        for q in range(25):
            if rnd.random() < .5:
                plane("skj", mat(f"skl{k}{q}", "#000000", .4, emit=rnd.choice(["#ffcf6e", "#bcd7ff"]), estr=rnd.uniform(1, 2.5)),
                      (bx + rnd.uniform(-1.8, 1.8), 55.9 + rnd.uniform(0, 6), rnd.uniform(2, bh - 1)), (.5, .7), rot=(math.pi / 2, 0, 0))
    # postes
    pole = mat("poste", "#1b1820", .4, metal=.7)
    for py in (9, 23, 37):
        for px, sg in ((-1.2, 1), (6.0, -1)):
            if px > 0 and py == 3:
                continue
            cyl("poste", pole, (px, py, 3.3), .1, 6.6)
            box("braco", pole, (px + sg * .7, py, 6.5), (1.4, .1, .1))
            lx = px + sg * 1.3
            box("lamp", mat("lampada", "#000000", .3, emit="#ffe3a8", estr=30), (lx, py, 6.42), (.55, .28, .08))
            light("SPOT", (lx, py, 6.3), 2200, "#ffcf8a", spot=70, blend=.7, size=.3)
    # contraluz forte no fim da rua + lua de fundo
    light("AREA", (2, 62, 6), 15000, "#b9a8ff", rot=(math.radians(-95), 0, 0), size=40)
    light("SUN", (0, 0, 20), .15, "#6f63b0", rot=(math.radians(55), 0, math.radians(210)))
    # fios
    wire = mat("fio", "#050407", .5)
    for z, yy in ((8.0, 10), (8.4, 10.5), (7.6, 22)):
        bpy.ops.curve.primitive_bezier_curve_add(location=(2, yy, z), rotation=(0, 0, math.radians(8)))
        c = bpy.context.active_object
        c.data.bevel_depth = .018
        c.scale = (12, 1, 1)
        c.data.materials.append(wire)
    camera((-1.6, -6.5, 1.5), (0.4, 14, 3.4), lens=24, dof=8, fstop=5)



# ------------------------------------------------------------------ peças reutilizáveis
def brick_mat(name, c1="#5a2f28", c2="#6e3a2f", mortar="#2a2222", scale=6.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Color1"].default_value = hexc(c1)
    br.inputs["Color2"].default_value = hexc(c2)
    br.inputs["Mortar"].default_value = hexc(mortar)
    br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = .015
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 3
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMixRGB")
    mix.blend_type = "MULTIPLY"
    mix.inputs["Fac"].default_value = .6
    nt.links.new(br.outputs["Color"], mix.inputs["Color1"])
    nt.links.new(nz.outputs["Color"], mix.inputs["Color2"])
    nt.links.new(mix.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = .5
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = .75
    return m


def star_world(density=900, strength=1.0, base="#020106", nebula="#1a0f33"):
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vo = nt.nodes.new("ShaderNodeTexVoronoi")
    vo.inputs["Scale"].default_value = density
    nt.links.new(tc.outputs["Generated"], vo.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = .0
    cr.color_ramp.elements[0].color = (6, 6, 7, 1)
    cr.color_ramp.elements[1].position = .035
    cr.color_ramp.elements[1].color = hexc(base)
    nt.links.new(vo.outputs["Distance"], cr.inputs["Fac"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.5
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    cr2 = nt.nodes.new("ShaderNodeValToRGB")
    cr2.color_ramp.elements[0].color = hexc(base)
    cr2.color_ramp.elements[1].color = hexc(nebula)
    cr2.color_ramp.elements[0].position = .45
    nt.links.new(nz.outputs["Fac"], cr2.inputs["Fac"])
    add = nt.nodes.new("ShaderNodeMixRGB")
    add.blend_type = "ADD"
    add.inputs["Fac"].default_value = 1
    nt.links.new(cr.outputs["Color"], add.inputs["Color1"])
    nt.links.new(cr2.outputs["Color"], add.inputs["Color2"])
    nt.links.new(add.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength


def lamp_post(x, y, sg=1, energy=2200, col="#ffcf8a", h=6.6):
    pole = mat("poste", "#1b1820", .4, metal=.7)
    cyl("poste", pole, (x, y, h / 2), .1, h)
    box("braco", pole, (x + sg * .7, y, h - .1), (1.4, .1, .1))
    lx = x + sg * 1.3
    box("lamp", mat("lampada", "#000000", .3, emit="#ffe3a8", estr=30), (lx, y, h - .18), (.55, .28, .08))
    light("SPOT", (lx, y, h - .3), energy, col, spot=70, blend=.7, size=.3)


def lit_windows(rnd, x0, x1, z0, z1, y, face="-y", p=.35, w=.75, h=1.1, dx=1.5, dz=2.3, cols=("#ffcf6e", "#ffe2a3", "#ffa860", "#bcd7ff")):
    dark = mat("jd", "#0d0b12", .15)
    x = x0
    while x < x1:
        z = z0
        while z < z1:
            m = mat("jl", "#000000", .3, emit=rnd.choice(cols), estr=rnd.uniform(1.2, 3)) if rnd.random() < p else dark
            plane("jan", m, (x, y, z), (w, h), rot=(math.pi / 2, 0, 0))
            z += dz
        x += dx


def ground(col="#14111a", col2="#221d28", rough=(.18, .6), size=80, loc=(0, 20, 0)):
    plane("chao", tmat("chao", col, col2, rough=rough, scale=3, bump=.05), loc, (size, size))


def skyline_far(rnd, y=55, n=12, x0=-30, x1=40, h=(14, 36), p=.5):
    for k in range(n):
        bx = x0 + (x1 - x0) * k / n + rnd.uniform(-2, 2)
        bh = rnd.uniform(*h)
        bw = rnd.uniform(4, 6)
        box(f"sk{k}", tmat(f"skm{k}", "#120e1a", "#1b1624", scale=1), (bx, y + rnd.uniform(0, 6), bh / 2), (bw, 4, bh))
        lit_windows(rnd, bx - bw / 2 + .6, bx + bw / 2 - .4, 2, bh - 1, y + rnd.uniform(0, 6) - 2.05, p=p * .6, w=.5, h=.7, dx=1.0, dz=1.6)


# ------------------------------------------------------------------ outros cenários
def plate_rua_alta():
    plate_rua(1)
    cam = bpy.context.scene.camera
    cam.location = (2.0, -9, 6.5)
    d = Vector((2.0, 16, 1.5)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.data.dof.use_dof = False


def plate_rua_close():
    plate_rua(2)
    cam = bpy.context.scene.camera
    cam.location = (-0.6, -2.5, 1.5)
    d = Vector((-3.5, 6, 2.2)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 45
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 1.0
    cam.data.dof.aperture_fstop = 1.4


def plate_beco(close=False):
    reset()
    rnd = random.Random(21)
    world("#06040a", fog=.06, fog_col="#8f7fb8", strength=.4)
    ground("#100d14", "#201a24", rough=(.08, .5))
    wall = brick_mat("tijolo", "#4f2a25", "#643429", "#231c1f", scale=5)
    box("muro", wall, (0, 4, 6), (30, .6, 12))
    box("cano", mat("cano", "#3a3d44", .35, metal=.8), (-2.6, 3.62, 5), (.18, .18, 10))
    box("lixeira", tmat("lix", "#24452a", "#1a2f1e", scale=4), (-3.6, 3.1, .55), (1.1, .9, 1.1))
    box("caixa", tmat("cx", "#5a4228", "#3a2a18", scale=5), (3.9, 3.2, .4), (.9, .8, .8))
    box("arandela", mat("arand", "#000000", .3, emit="#ffd28a", estr=35), (1.6, 3.55, 4.6), (.5, .3, .2))
    light("SPOT", (1.6, 3.3, 4.45), 1600, "#ffc77a", rot=(math.radians(15), 0, 0), spot=95, blend=.8, size=.3)
    light("AREA", (-12, -2, 6), 2600, "#7f8dff", rot=(0, math.radians(-70), 0), size=8)   # contraluz azul vindo da esquerda
    light("AREA", (0, -8, 3), 120, "#6a5a9a", rot=(math.radians(90), 0, 0), size=12)
    puddle = mat("poca", "#07060a", .0, metal=.1)
    for _ in range(6):
        plane("poca", puddle, (rnd.uniform(-4, 4), rnd.uniform(-2, 3), .006), (rnd.uniform(.6, 2), rnd.uniform(.3, .9)))
    if close:
        camera((0, -2.2, 1.6), (0, 4, 2.0), lens=40, dof=1.2, fstop=1.6)
    else:
        camera((0, -6.5, 1.4), (0, 4, 2.6), lens=26, dof=8, fstop=6)


def plate_elevador():
    reset()
    world("#050407", fog=.025, fog_col="#9a9ab0", strength=.3)
    floor = mat("piso", "#2a2a30", .25)
    nt = floor.node_tree
    ck = nt.nodes.new("ShaderNodeTexChecker")
    ck.inputs["Color1"].default_value = hexc("#2c2a30")
    ck.inputs["Color2"].default_value = hexc("#1a181d")
    ck.inputs["Scale"].default_value = 12
    nt.links.new(nt.nodes.new("ShaderNodeTexCoord").outputs["Object"], ck.inputs["Vector"])
    nt.links.new(ck.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    plane("piso", floor, (0, 0, 0), (20, 20))
    walls = tmat("parede", "#3d3644", "#2a2530", scale=3, bump=.15)
    box("fundo", walls, (0, 3.2, 3), (14, .3, 6))
    box("esq", walls, (-3.6, 0, 3), (.3, 12, 6))
    box("dir", walls, (3.6, 0, 3), (.3, 12, 6))
    box("teto", walls, (0, 0, 5.2), (8, 12, .2))
    metal = tmat("aco", "#8d929c", "#6b707a", rough=(.2, .4), scale=20, bump=.05, metal=.9)
    box("moldura", mat("mold", "#4a4452", .4, metal=.6), (0, 3.0, 1.55), (2.8, .1, 3.1))
    box("portaE", metal, (-.66, 2.94, 1.45), (1.28, .06, 2.85))
    box("portaD", metal, (.66, 2.94, 1.45), (1.28, .06, 2.85))
    box("painel", mat("pain", "#000000", .3, emit="#ff4040", estr=4), (0, 2.96, 3.25), (.5, .04, .2))
    box("luminaria", mat("fluor", "#000000", .2, emit="#dfe8ff", estr=12), (0, 1.0, 5.05), (2.2, .3, .06))
    light("AREA", (0, 1.0, 5.0), 700, "#dfe8ff", rot=(0, 0, 0), size=2)
    light("AREA", (0, -6, 2), 150, "#ffb070", rot=(math.radians(90), 0, 0), size=4)
    camera((0, -5.2, 1.5), (0, 3, 1.9), lens=26, dof=8, fstop=8)


def plate_escola():
    reset()
    rnd = random.Random(31)
    world("#06040c", fog=.04, fog_col="#7f78b0", strength=.5)
    sky_plane((0, 70, 18), (140, 60), estr=1.0, bot="#5a3d6e")
    ground("#141118", "#221c26")
    fac = tmat("escola", "#5a4a6a", "#4a3c58", scale=2, bump=.2)
    box("predio", fac, (0, 12, 6), (22, 3, 12))
    box("telhado", mat("tel", "#2a2030", .7), (0, 12, 12.3), (23, 3.6, .6))
    for k in range(3):
        for i in range(7):
            lit = rnd.random() < .7
            m = mat("sala", "#000000", .3, emit=rnd.choice(["#fff1c9", "#ffe0a0", "#e8f0ff"]), estr=rnd.uniform(2, 4)) if lit else mat("sd", "#0d0b12", .2)
            plane("janela", m, (-9 + i * 3, 10.45, 2.2 + k * 3.3), (1.9, 1.7), rot=(math.pi / 2, 0, 0))
    box("portao", mat("port", "#1a1820", .4, metal=.7), (0, 10.4, 1.4), (3.2, .1, 2.8))
    for x in (-6, 6):
        cyl("tronco", mat("tr", "#1a1210", .8), (x, 6, 1.6), .2, 3.2)
        obj(bpy.ops.mesh.primitive_ico_sphere_add, "copa", tmat("copa", "#0f1f14", "#16301c", scale=4, bump=.6), location=(x, 6, 4.2), radius=2.0, subdivisions=3)
    lamp_post(6.5, 2, -1)
    light("AREA", (0, 30, 8), 9000, "#b0a0ff", rot=(math.radians(-95), 0, 0), size=30)
    camera((0, -7, 1.3), (0, 10, 5.2), lens=24, dof=10, fstop=6)


def plate_quadra():
    reset()
    world("#040306", fog=.05, fog_col="#c8d4ff", strength=.2)
    floor = tmat("madeira", "#a8642c", "#8a4e20", rough=(.15, .35), scale=1.5, bump=.05)
    plane("quadra", floor, (0, 5, 0), (40, 40))
    for x in (-5, 5):
        plane("linha", mat("ln", "#f2f2f2", .4), (x, 6, .003), (.1, 30))
    plane("linha2", mat("ln2", "#f2f2f2", .4), (0, 6, .003), (10, .1))
    box("rede", mat("rede", "#e8e8e8", .5, emit="#ffffff", estr=.3), (0, 6, 2.35), (10, .03, 1.0))
    for x in (-5.2, 5.2):
        cyl("poste", mat("pr", "#888c96", .3, metal=.8), (x, 6, 1.45), .07, 2.9)
    box("arquib", tmat("arq", "#1a1820", "#24222a", scale=3), (0, 22, 3), (40, 6, 6), rot=(math.radians(-25), 0, 0))
    for x in (-8, 8):
        light("SPOT", (x, 8, 14), 30000, "#e8eeff", rot=(math.radians(-25), math.radians(-20 if x > 0 else 20), 0), spot=40, blend=.4, size=.5)
        box("refletor", mat("rf", "#000000", .3, emit="#ffffff", estr=60), (x, 8.3, 14.2), (1.2, .2, .6))
    camera((0, -7.5, 1.6), (0, 6, 3.4), lens=24, dof=9, fstop=6)


def plate_quintal():
    reset()
    rnd = random.Random(41)
    world("#05040a", fog=.04, fog_col="#7f78b0", strength=.4)
    sky_plane((0, 70, 18), (140, 60), estr=1.0)
    ground("#0f1a10", "#18261a", rough=(.5, .9))
    box("casa", brick_mat("casa", "#4a3a3a", "#5a4444", "#2a2222", 4), (-6, 9, 3.5), (8, 6, 7))
    plane("janela", mat("jc", "#000000", .3, emit="#ffd08a", estr=3), (-4.5, 5.96, 3.5), (1.6, 1.4), rot=(math.pi / 2, 0, 0))
    for i in range(30):    # cerca de madeira
        box("tabua", tmat("tb", "#3a2a1a", "#2a1c10", scale=6), (-2 + i * .5, 14, 1.0), (.4, .08, 2.0 + rnd.uniform(-.1, .1)))
    skyline_far(rnd, y=40, n=10, x0=-20, x1=30, h=(8, 20))
    # cama elástica + jaula
    cyl("cama", mat("lona", "#1a1d3a", .4), (2.2, 4, .75), 1.8, .08, v=48)
    obj(bpy.ops.mesh.primitive_torus_add, "aro", mat("aro", "#2a5ad0", .4), location=(2.2, 4, .78), major_radius=1.85, minor_radius=.08)
    for k in range(16):
        a = k / 16 * 2 * math.pi
        cyl("grade", mat("grade", "#9aa0aa", .3, metal=.8), (2.2 + 2.0 * math.cos(a), 4 + 2.0 * math.sin(a), 1.6), .03, 3.2)
    for k in range(4):     # lasers
        box("laser", mat("las", "#000000", .2, emit="#ff1a1a", estr=40), (2.2, 4 - 2.1, .8 + k * .55), (4.2, .02, .02), rot=(0, 0, math.radians(k * 6 - 9)))
    light("POINT", (2.2, 2, 1.6), 120, "#ff2a2a", size=.5)
    lamp_post(6.5, 1.5, -1, energy=1800)
    light("AREA", (0, 30, 8), 7000, "#a0a8ff", rot=(math.radians(-95), 0, 0), size=30)
    camera((2.2, -5.5, 1.7), (2.2, 6, 1.8), lens=26, dof=7, fstop=6)


def plate_ceu(moon=True, beams=True, roof=False, big_moon=False):
    reset()
    rnd = random.Random(51)
    world("#05040b", fog=.02, fog_col="#8f84c8", strength=.4)
    sky_plane((0, 120, 40), (300, 160), estr=1.2, mid="#2a1f48", bot="#7a4a6a")
    skyline_far(rnd, y=60, n=14, x0=-40, x1=40, h=(10, 40), p=.6)
    if moon:
        r = 9 if big_moon else 3
        mo = obj(bpy.ops.mesh.primitive_uv_sphere_add, "lua", tmat("lua", "#f4efd8", "#c9c2a2", scale=4, bump=.3), location=(6 if not big_moon else 0, 110, 45 if not big_moon else 30), radius=r)
        mo.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = hexc("#fff4d0")
        mo.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.5
    if beams:
        for x, a in ((-14, 18), (14, -18), (-5, 6), (5, -6)):
            light("SPOT", (x, 45, 0), 90000, "#cfe6ff", rot=(math.radians(-a * .2), math.radians(a), 0), spot=6, blend=.2, size=.4)
    if roof:
        box("telhado", tmat("teto", "#1a1520", "#241e2a", scale=3), (0, 2, -.1), (30, 14, .2))
        box("caixa", tmat("cxa", "#2a2430", "#1a1520", scale=3), (4, 4, 1.4), (2, 2, 2.8))
        box("mureta", tmat("mur", "#2a2430", "#1a1520", scale=3), (0, 8.5, .4), (30, .3, .8))
        light("AREA", (-4, -3, 4), 300, "#ffb070", rot=(math.radians(60), 0, 0), size=3)
        camera((0, -6, 1.6), (0, 60, 18 if big_moon else 12), lens=26)
    else:
        camera((0, -2, 1.6), (0, 60, 22), lens=24)


def plate_sala():
    reset()
    rnd = random.Random(61)
    world("#050407", fog=.02, fog_col="#c0a080", strength=.3)
    wall = bpy.data.materials.new("papel")
    wall.use_nodes = True
    nt = wall.node_tree
    wv = nt.nodes.new("ShaderNodeTexWave")
    wv.inputs["Scale"].default_value = 3
    wv.wave_type = "BANDS"
    wv.bands_direction = "X"
    nt.links.new(nt.nodes.new("ShaderNodeTexCoord").outputs["Object"], wv.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = hexc("#3e2f52")
    cr.color_ramp.elements[1].color = hexc("#4a3a60")
    nt.links.new(wv.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = .8
    box("parede", wall, (0, 3, 3), (14, .2, 6))
    box("rodape", mat("rod", "#2a1c14", .5), (0, 2.88, .12), (14, .05, .24))
    plane("piso", tmat("taco", "#4a2c18", "#3a2010", rough=(.3, .6), scale=2), (0, 0, 0), (20, 20))
    plane("tapete", tmat("tap", "#6a2430", "#4a1820", rough=(.8, .95), scale=8), (0, 1, .005), (5, 3))
    # janela com cidade chuvosa
    box("caixilho", mat("cx", "#20161a", .6), (2.6, 2.86, 3.0), (2.4, .1, 2.8))
    plane("vidro", mat("vid", "#000000", .1, emit="#1a2440", estr=1.5), (2.6, 2.8, 3.0), (2.1, 2.5), rot=(math.pi / 2, 0, 0))
    for _ in range(40):
        plane("luzcid", mat("lc", "#000000", .3, emit=rnd.choice(["#ffcf6e", "#bcd7ff", "#ff8fa0"]), estr=rnd.uniform(2, 6)),
              (2.6 + rnd.uniform(-1, 1), 2.79, 2.0 + rnd.uniform(0, 1.6)), (.06, .09), rot=(math.pi / 2, 0, 0))
    box("cruz", mat("cz", "#20161a", .6), (2.6, 2.78, 3.0), (2.1, .04, .08))
    box("cruz2", mat("cz2", "#20161a", .6), (2.6, 2.78, 3.0), (.08, .04, 2.5))
    # abajur quente
    cyl("abajur", mat("ab", "#000000", .4, emit="#ffcf8a", estr=6), (-3.2, 2.4, 1.9), .4, .5, v=24)
    cyl("pe", mat("pe", "#2a1c14", .5), (-3.2, 2.4, .85), .05, 1.7)
    light("POINT", (-3.2, 2.2, 1.9), 400, "#ffb26a", size=.4)
    light("AREA", (2.6, 3.5, 3), 300, "#8090ff", rot=(math.radians(-90), 0, 0), size=2)
    light("AREA", (0, -4, 4), 60, "#ffd0a0", rot=(math.radians(70), 0, 0), size=6)
    camera((0, -4.5, 1.5), (0, 3, 1.9), lens=24, dof=5.5, fstop=4)


def plate_ferrovelho():
    reset()
    rnd = random.Random(71)
    world("#05040a", fog=.05, fog_col="#a08c90", strength=.4)
    sky_plane((0, 70, 18), (140, 60), estr=1.0, bot="#8a4a3a")
    ground("#17130f", "#241c16", rough=(.4, .9))
    junk = [tmat(f"j{k}", c1, c2, rough=(.3, .8), scale=5, bump=.4, metal=.5) for k, (c1, c2) in
            enumerate([("#4a2a1c", "#2a1810"), ("#3a3e44", "#22252a"), ("#5a1e1e", "#2a1212"), ("#2a3a2a", "#1a241a")])]
    for k in range(40):
        x, y = rnd.uniform(-10, 10), rnd.uniform(4, 16)
        if abs(x) < 2.5 and y < 7:
            continue
        sz = (rnd.uniform(.6, 2.4), rnd.uniform(.6, 2.4), rnd.uniform(.4, 1.6))
        box("sucata", rnd.choice(junk), (x, y, sz[2] / 2 + rnd.uniform(0, 1.5)), sz, rot=(rnd.uniform(-.4, .4), rnd.uniform(-.4, .4), rnd.uniform(0, 3)))
    for k in range(14):
        obj(bpy.ops.mesh.primitive_torus_add, "pneu", mat("pn", "#0f0e10", .8), location=(rnd.uniform(-8, 8), rnd.uniform(3, 12), rnd.uniform(.2, 1.5)),
            rotation=(rnd.uniform(0, 3), rnd.uniform(0, 3), 0), major_radius=.45, minor_radius=.18)
    text("placa", "FERRO-VELHO", mat("neonfv", "#000000", .3, emit="#ff7a2a", estr=18), (0, 14, 6), 1.2)
    light("POINT", (0, 13, 6), 400, "#ff7a2a", size=1)
    lamp_post(-3.5, 2, 1, energy=2400)
    light("AREA", (0, 40, 6), 9000, "#ffa080", rot=(math.radians(-95), 0, 0), size=30)
    camera((0, -6, 1.5), (0, 8, 3.0), lens=24, dof=7, fstop=6)


def stripe_mat(name, c1="#b81f34", c2="#efe6d8", n=16):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    gr = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], gr.inputs[0])
    at = nt.nodes.new("ShaderNodeMath")
    at.operation = "ARCTAN2"
    nt.links.new(gr.outputs["Y"], at.inputs[0])
    nt.links.new(gr.outputs["X"], at.inputs[1])
    mu = nt.nodes.new("ShaderNodeMath")
    mu.operation = "MULTIPLY"
    mu.inputs[1].default_value = n / 2
    nt.links.new(at.outputs[0], mu.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath")
    sn.operation = "SINE"
    nt.links.new(mu.outputs[0], sn.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath")
    gt.operation = "GREATER_THAN"
    nt.links.new(sn.outputs[0], gt.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixRGB")
    mx.inputs["Color1"].default_value = hexc(c1)
    mx.inputs["Color2"].default_value = hexc(c2)
    nt.links.new(gt.outputs[0], mx.inputs["Fac"])
    nt.links.new(mx.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = .7
    return m


def plate_circo_ext():
    reset()
    rnd = random.Random(81)
    world("#05040a", fog=.04, fog_col="#9080b0", strength=.4)
    sky_plane((0, 70, 18), (140, 60), estr=1.1)
    ground("#101a10", "#18241a", rough=(.5, .9))
    lona = stripe_mat("lona")
    obj(bpy.ops.mesh.primitive_cylinder_add, "parede", lona, location=(0, 12, 2.5), radius=7, depth=5, vertices=64)
    obj(bpy.ops.mesh.primitive_cone_add, "teto", lona, location=(0, 12, 8), radius1=7.6, radius2=.2, depth=6, vertices=64)
    plane("entrada", mat("ent", "#000000", .3, emit="#ffb860", estr=4), (0, 4.98, 1.8), (2.4, 3.4), rot=(math.pi / 2, 0, 0))
    light("SPOT", (0, 5.5, 2), 900, "#ffb860", rot=(math.radians(100), 0, 0), spot=80, blend=.8)
    for k in range(26):   # varal de luzes
        a = math.pi * (k / 25)
        x = -7.4 * math.cos(a)
        z = 5.2 + 3.0 * math.sin(a)
        obj(bpy.ops.mesh.primitive_uv_sphere_add, "lampada", mat("lp", "#000000", .3, emit="#ffe08a", estr=40), location=(x, 4.6, z), radius=.09)
    text("placacirco", "CIRCO", mat("nc", "#000000", .3, emit="#ff3060", estr=18), (0, 4.9, 4.6), 1.0)
    light("POINT", (0, 4.5, 4.6), 200, "#ff3060", size=.5)
    light("AREA", (0, 40, 8), 9000, "#a090ff", rot=(math.radians(-95), 0, 0), size=30)
    skyline_far(rnd, y=45, n=10, x0=-25, x1=25, h=(6, 16))
    camera((-1.5, -5.5, 1.4), (0, 10, 5.0), lens=22, dof=8, fstop=6)


def plate_circo_int(high=False):
    reset()
    world("#030205", fog=.06, fog_col="#ffd9b0", strength=.2)
    lona = stripe_mat("lonai", "#5a1020", "#2a1218", n=24)
    obj(bpy.ops.mesh.primitive_cylinder_add, "parede", lona, location=(0, 0, 4), radius=14, depth=8, vertices=64)
    obj(bpy.ops.mesh.primitive_cone_add, "teto", lona, location=(0, 0, 13), radius1=14.5, radius2=.3, depth=10, vertices=64)
    plane("picadeiro", tmat("serragem", "#6a4426", "#4a2e18", rough=(.8, 1), scale=4), (0, 0, .01), (40, 40))
    cyl("anel", mat("anel", "#b81f34", .5), (0, 3, .2), 5.2, .4, v=64)
    cyl("anel2", mat("anel2", "#2a1218", .7), (0, 3, .22), 4.9, .42, v=64)
    cyl("cama", mat("lona2", "#1a1d3a", .4), (0, 3, .75), 1.8, .08, v=48)
    obj(bpy.ops.mesh.primitive_torus_add, "aro", mat("aro", "#2a5ad0", .4), location=(0, 3, .78), major_radius=1.85, minor_radius=.08)
    box("trapezio", mat("trap", "#c9a24a", .3, metal=.8), (0, 3, 11), (2.2, .08, .08))
    for x in (-1.1, 1.1):
        box("corda", mat("cor", "#d8d0c0", .6), (x, 3, 13), (.03, .03, 4))
    light("SPOT", (0, 3, 17), 60000, "#fff0d0", spot=18, blend=.3, size=.3)
    for x, a in ((-8, 30), (8, -30)):
        light("SPOT", (x, -4, 10), 15000, "#ff8a5a", rot=(math.radians(45), math.radians(a), 0), spot=14, blend=.3)
    if high:
        camera((0, -9, 8.5), (0, 3, 9.5), lens=26)
    else:
        camera((0, -8, 1.6), (0, 3, 4.5), lens=24, dof=11, fstop=8)


def plate_foguete():
    reset()
    rnd = random.Random(91)
    world("#04030a", fog=.03, fog_col="#9090c0", strength=.4)
    sky_plane((0, 90, 25), (200, 90), estr=1.0)
    ground("#1a1820", "#24222a", rough=(.4, .8))
    body = tmat("fog", "#e9e6ef", "#c9c6d4", rough=(.25, .4), scale=8, bump=.1, metal=.3)
    cyl("corpo", body, (0, 8, 5), 1.0, 8, v=48)
    obj(bpy.ops.mesh.primitive_cone_add, "bico", mat("bico", "#c8243a", .4), location=(0, 8, 10.4), radius1=1.0, radius2=0, depth=2.8, vertices=48)
    for a in (0, 120, 240):
        r = math.radians(a)
        box("aleta", mat("al", "#c8243a", .4), (math.cos(r) * 1.2, 8 + math.sin(r) * 1.2, 1.6), (.12, 1.2, 2.2), rot=(0, 0, r))
    obj(bpy.ops.mesh.primitive_cylinder_add, "janela", mat("jv", "#000000", .1, emit="#8fd8ff", estr=3), location=(0, 7.02, 7.2), radius=.35, depth=.1, rotation=(math.pi / 2, 0, 0))
    for k in range(4):   # fitas remendando
        box("fita", mat("ft", "#b9b6aa", .6), (rnd.uniform(-.3, .3), 6.98, 3.5 + k * 1.1), (.9, .05, .18), rot=(0, rnd.uniform(-.6, .6), 0))
    for k in range(12):   # torre de serviço
        box("torre", mat("tr", "#5b5f6b", .4, metal=.8), (2.6, 8, .5 + k * 1.0), (.1, 1.4, .1))
        box("travessa", mat("tv", "#5b5f6b", .4, metal=.8), (2.6, 8, .5 + k * 1.0), (.1, .1, 1.0), rot=(math.radians(45), 0, 0))
    for x in (-8, 8):
        light("SPOT", (x, 2, .5), 12000, "#e0ecff", rot=(math.radians(70), math.radians(-25 if x > 0 else 25), 0), spot=20, blend=.4)
    mo = obj(bpy.ops.mesh.primitive_uv_sphere_add, "lua", mat("lua", "#f4efd8", .8, emit="#fff4d0", estr=2.5), location=(14, 80, 40), radius=4)
    camera((0, -7, 1.5), (0, 8, 6.0), lens=24, dof=14, fstop=8)


def planet(name, loc, r, sea="#1f5fbf", land="#3fae5a", atm="#8fd0ff"):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 6
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = hexc(sea)
    cr.color_ramp.elements[1].color = hexc(land)
    cr.color_ramp.elements[0].position = .52
    cr.color_ramp.elements[1].position = .56
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = .5
    obj(bpy.ops.mesh.primitive_uv_sphere_add, name, m, location=loc, radius=r, segments=96, ring_count=48)
    bpy.ops.object.shade_smooth()
    # atmosfera
    a = bpy.data.materials.new(name + "atm")
    a.use_nodes = True
    a.blend_method = "BLEND"
    nt = a.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = .35
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = hexc(atm)
    em.inputs["Strength"].default_value = 3
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lw.outputs["Facing"], mx.inputs["Fac"])
    nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    obj(bpy.ops.mesh.primitive_uv_sphere_add, name + "a", a, location=loc, radius=r * 1.04, segments=96, ring_count=48)
    bpy.ops.object.shade_smooth()


def plate_lua_chao():
    reset()
    star_world()
    bpy.context.scene.eevee.use_volumetric_lights = False
    pl = obj(bpy.ops.mesh.primitive_grid_add, "chao", tmat("regolito", "#9a97a6", "#6f6c7a", rough=(.8, 1), scale=2, bump=.6),
             location=(0, 10, 0), x_subdivisions=160, y_subdivisions=160, size=60)
    tex = bpy.data.textures.new("crat", "VORONOI")
    tex.noise_scale = 2.2
    md = pl.modifiers.new("d", "DISPLACE")
    md.texture = tex
    md.strength = .7
    md.texture_coords = "GLOBAL"
    planet("terra", (-9, 60, 22), 6)
    light("SUN", (0, 0, 10), 4.5, "#fff6e8", rot=(math.radians(70), 0, math.radians(-60)))
    camera((0, -6, 1.7), (0, 10, 2.8), lens=24)


def plate_espaco(earth_r=26, cam_z=0):
    reset()
    star_world(1100)
    bpy.context.scene.eevee.use_volumetric_lights = False
    planet("terra", (0, 40, -32 + cam_z), earth_r)
    light("SUN", (0, 0, 10), 4.0, "#fff6e8", rot=(math.radians(40), math.radians(30), math.radians(-40)))
    camera((0, -10, 0), (0, 40, 2), lens=30)


PLATES = {
    "rua": lambda: plate_rua(0),
    "rua_alta": plate_rua_alta,
    "rua_close": plate_rua_close,
    "beco": lambda: plate_beco(False),
    "beco_close": lambda: plate_beco(True),
    "elevador": plate_elevador,
    "escola": plate_escola,
    "quadra": plate_quadra,
    "quintal": plate_quintal,
    "ceu": lambda: plate_ceu(True, True),
    "ceu_lua": lambda: plate_ceu(True, False, roof=True, big_moon=True),
    "telhado": lambda: plate_ceu(True, False, roof=True),
    "sala": plate_sala,
    "ferrovelho": plate_ferrovelho,
    "circo": plate_circo_ext,
    "circo_dentro": lambda: plate_circo_int(False),
    "circo_alto": lambda: plate_circo_int(True),
    "foguete": plate_foguete,
    "lua": plate_lua_chao,
    "espaco": plate_espaco,
}

def render(name):
    os.makedirs(OUT, exist_ok=True)
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(OUT, name + (".preview" if PREVIEW else "") + ".jpg")
    bpy.ops.render.render(write_still=True)
    print("SALVO", sc.render.filepath)



if __name__ == "__main__":
    PLATES[NAME]()
    render(NAME)
