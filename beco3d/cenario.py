"""Cenário realista: beco de comunidade com escadaria de concreto e corrimão azul.

Eixos: Z para cima. O beco corre ao longo de Y (y<0); no fim dele (y 0..5) há um largo com a
escadaria subindo em +Y até um patamar na frente da casa amarela "34", e um segundo lance
subindo em +X encostado na fachada. À esquerda da escada, um patamar baixo com mureta e
corrimão azul na frente de uma casa com janela gradeada (cena final).
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix
import numpy as np
import mat as M

D = math.radians
COL = None

def _link(ob):
    (COL or bpy.context.scene.collection).objects.link(ob); return ob

def box(name, m, lo, hi, bevel=0.0, seg=2):
    lo, hi = Vector(lo), Vector(hi); c = (lo+hi)/2; h = (hi-lo)/2
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=2)
    for v in bm.verts: v.co = Vector((v.co.x*h.x + c.x, v.co.y*h.y + c.y, v.co.z*h.z + c.z))
    bm.to_mesh(me); bm.free()
    ob = _link(bpy.data.objects.new(name, me))
    if m: ob.data.materials.append(m)
    if bevel:
        b = ob.modifiers.new("b", 'BEVEL'); b.width = bevel; b.segments = seg; b.limit_method = 'ANGLE'
        for p in me.polygons: p.use_smooth = False
    return ob

def tube(name, m, a, b, r=0.022, verts=12):
    a, b = Vector(a), Vector(b); d = b - a
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=d.length)
    rot = d.normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bm.transform(Matrix.Translation((a+b)/2) @ rot)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = _link(bpy.data.objects.new(name, me)); ob.data.materials.append(m); return ob

def join(objs, name):
    if not objs: return None
    ctx = bpy.context
    for o in ctx.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    ctx.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); objs[0].name = name; return objs[0]

# ------------------------------------------------------------------ peças
def window(name, center, normal, w, h, kind="grade", frame="#e8e6df", depth=.12):
    """Janela na parede. normal = direção para fora da parede (ex.: (0,-1,0))."""
    parts = []
    white = M.paint("grade_branca", frame, .45, chip=.25)
    dark = M.plain("vao_escuro", "#151515", .9)
    glass = M.glass()
    # coordenadas locais: largura em X, altura em Z, para fora em -Y
    loc = []
    loc.append(box(name+"_vidro", glass if kind != "veneziana" else dark, (-w/2, -.012, -h/2), (w/2, -.004, h/2)))
    t = .035
    for (a, b) in [((-w/2-t, -.02, h/2), (w/2+t, .01, h/2+t)), ((-w/2-t, -.02, -h/2-t), (w/2+t, .01, -h/2)),
                   ((-w/2-t, -.02, -h/2), (-w/2, .01, h/2)), ((w/2, -.02, -h/2), (w/2+t, .01, h/2))]:
        loc.append(box(name+"_mold", white, a, b))
    loc.append(box(name+"_peitoril", M.concrete("peitoril", "#b8b3a6"), (-w/2-.06, -.07, -h/2-.05), (w/2+.06, .02, -h/2)))
    if kind == "grade":
        n = max(3, int(w/.11)); m_ = max(3, int(h/.11))
        for i in range(n+1):
            x = -w/2 + w*i/n
            loc.append(tube(name+"_gv", white, (x, -.05, -h/2), (x, -.05, h/2), .008, 6))
        for j in range(m_+1):
            z = -h/2 + h*j/m_
            loc.append(tube(name+"_gh", white, (-w/2, -.05, z), (w/2, -.05, z), .008, 6))
    elif kind == "veneziana":
        n = int(h/.045)
        for j in range(n):
            z = -h/2 + (j+.5)*h/n
            loc.append(box(name+"_ripa", white, (-w/2, -.02 + .012*(j % 2), z-.02), (w/2, .02, z+.02)))
    elif kind == "portao":
        loc.append(box(name+"_porta", M.paint("porta_azul", "#3b5f7a", .5, chip=.4), (-w/2, -.03, -h/2), (w/2, -.013, h/2)))
        n = max(3, int(w/.1))
        for i in range(n+1):
            x = -w/2 + w*i/n
            loc.append(tube(name+"_gv", white, (x, -.06, -h/2), (x, -.06, h/2), .009, 6))
        for z in (-h/2+.05, 0, h/2-.05):
            loc.append(tube(name+"_gh", white, (-w/2, -.06, z), (w/2, -.06, z), .012, 6))
    elif kind == "porta":
        loc.append(box(name+"_porta", M.paint("porta_azul", "#3b5f7a", .5, chip=.4), (-w/2, -.035, -h/2), (w/2, -.013, h/2)))
        loc.append(box(name+"_macaneta", M.plain("metal", "#9a968e", .3, 1.0), (w/2-.12, -.06, -.05), (w/2-.07, -.035, .0)))
    ob = join(loc, name)
    n = Vector(normal).normalized()
    ang = math.atan2(n.x, -n.y)
    ob.matrix_world = Matrix.Translation(center) @ Matrix.Rotation(ang, 4, 'Z')
    return ob

def meter_box(name, center, normal):
    gray = M.paint("caixa_luz", "#b9bdb5", .5, chip=.2)
    parts = [box(name, gray, (-.16, -.12, -.2), (.16, 0, .2), .01),
             box(name+"_visor", M.glass("visor"), (-.08, -.125, -.02), (.08, -.11, .1))]
    ob = join(parts, name)
    n = Vector(normal).normalized(); ob.matrix_world = Matrix.Translation(center) @ Matrix.Rotation(math.atan2(n.x, -n.y), 4, 'Z')
    return ob

def plant(name, base, size=1.0, pot="#3a2a22"):
    parts = []
    p = box(name+"_vaso", M.plain("vaso_"+pot, pot, .7), (-.11*size, -.11*size, 0), (.11*size, .11*size, .22*size), .02)
    parts.append(p)
    leaf = M.plain("folha", "#3d5f2a", .55)
    rng = np.random.default_rng(abs(hash(name)) % 1000)
    for i in range(int(14*size)+4):
        a = rng.random()*6.28; r = rng.random()*.12*size; hgt = .25 + rng.random()*.45*size
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
        o = bpy.context.object
        o.scale = (.03*size, .09*size*(.6+rng.random()), .012)
        o.rotation_euler = (rng.random()*1.2, rng.random()*1.2, a)
        o.location = (math.cos(a)*r, math.sin(a)*r, .2*size + hgt*.6)
        o.data.materials.append(leaf); parts.append(o)
        st = tube(name+"_caule", leaf, (0, 0, .2*size), o.location, .004, 5); parts.append(st)
    ob = join(parts, name); ob.location = base; return ob

def wall_block(name, m, lo, hi, base_mat=None, base_h=0.0):
    o = [box(name, m, lo, hi)]
    if base_mat and base_h:
        lo2 = Vector(lo) - Vector((.015, .015, 0)); hi2 = Vector((hi[0]+.015, hi[1]+.015, lo[2] + base_h))
        o.append(box(name+"_rodape", base_mat, lo2, hi2))
    return o

def wires(name, pts_pairs, sag=.35):
    m = M.plain("fio", "#151515", .6)
    for i, (a, b) in enumerate(pts_pairs):
        a, b = Vector(a), Vector(b)
        cu = bpy.data.curves.new(f"{name}{i}", 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = .006; cu.bevel_resolution = 1
        sp = cu.splines.new('POLY'); n = 16; sp.points.add(n-1)
        for k in range(n):
            t = k/(n-1); p = a.lerp(b, t); p.z -= sag*4*t*(1-t)
            sp.points[k].co = (*p, 1)
        ob = _link(bpy.data.objects.new(f"{name}{i}", cu)); ob.data.materials.append(m)

def stairs(name, x0, x1, y0, z0, n, run, rise, axis="y", sign=1):
    """Lance de escada maciço. axis: direção de subida."""
    con = M.concrete("degrau", "#a19d93", 1.3)
    out = []
    for i in range(n):
        if axis == "y":
            ya = y0 + sign*i*run; yb = ya + sign*run
            lo = (x0, min(ya, yb), 0); hi = (x1, max(ya, yb), z0 + (i+1)*rise)
        else:
            xa = x0 + sign*i*run; xb = xa + sign*run
            lo = (min(xa, xb), y0[0], 0); hi = (max(xa, xb), y0[1], z0 + (i+1)*rise)
        o = box(f"{name}_{i}", con, lo, hi, .012, 2); out.append(o)
    return join(out, name)

def rail_line(name, a, b, post_every=1.0, h=.9, r=.022):
    blue = M.paint("corrimao_azul", "#2c6aa3", .4, chip=.5)
    a, b = Vector(a), Vector(b)
    parts = [tube(name, blue, a + Vector((0, 0, h)), b + Vector((0, 0, h)), r)]
    parts.append(tube(name+"_m", blue, a + Vector((0, 0, h*.5)), b + Vector((0, 0, h*.5)), r*.8))
    L = (b - a).length; n = max(1, int(round(L/post_every)))
    for i in range(n+1):
        p = a.lerp(b, i/n)
        parts.append(tube(name+"_p", blue, p, p + Vector((0, 0, h)), r))
    return join(parts, name)

# ------------------------------------------------------------------ cenário
def build():
    global COL
    COL = bpy.data.collections.new("cenario"); bpy.context.scene.collection.children.link(COL)
    mint = M.plaster("verde_claro", "#a8d6c6", stain=.45, scale=.9)
    yellow = M.plaster("amarelo", "#e8dca3", stain=.6, scale=.8)
    cream = M.plaster("creme", "#e4e0d2", stain=.55)
    gray = M.plaster("cinza_manchado", "#b4b2a8", dirt="#5d5b52", stain=.75, scale=1.1)
    teal = M.plaster("azul_piscina", "#3c9eb0", stain=.35)
    brick = M.plaster("tijolo", "#a8705a", dirt="#6b4636", stain=.6, scale=2.5)
    pink = M.plaster("rosa", "#d9b7a7", stain=.5)
    con = M.concrete("chao", "#b3ada0", .9)
    caco = M.mosaic()
    walls = []

    # chão
    walls.append(box("chao", con, (-8, -14, -.2), (8, 16, 0)))
    # ---------------- beco (y < 0)
    walls += wall_block("parede_esq", mint, (-2.6, -14, 0), (-1.35, .2, 6.2), caco, .95)
    walls += wall_block("parede_dir", gray, (1.35, -14, 0), (2.6, -.4, 5.5))
    box("pilar_dir", cream, (1.2, -1.0, 0), (1.55, -.4, 3.0), .01)
    box("degrau_porta", con, (-1.35, -6.2, 0), (-1.05, -5.0, .14), .01)
    window("jan_esq1", Vector((-1.35, -3.6, 1.7)), (1, 0, 0), .9, 1.0, "veneziana")
    window("jan_esq2", Vector((-1.35, -3.6, 4.4)), (1, 0, 0), .9, 1.0, "grade")
    window("porta_esq", Vector((-1.35, -5.6, 1.05)), (1, 0, 0), .8, 2.1, "porta")
    window("jan_esq3", Vector((-1.35, -9.0, 1.7)), (1, 0, 0), .9, 1.1, "grade")
    window("jan_dir1", Vector((1.35, -6.5, 2.0)), (-1, 0, 0), .7, .9, "veneziana", frame="#d9d4c5")
    window("jan_dir2", Vector((1.35, -6.5, 4.4)), (-1, 0, 0), .7, .9, "grade")
    meter_box("luz1", Vector((1.35, -3.0, 1.5)), (-1, 0, 0))
    tube("cano1", M.plain("pvc", "#dcdcd6", .4), (1.33, -2.2, 0), (1.33, -2.2, 5.4), .025)
    tube("cano2", M.plain("pvc", "#dcdcd6", .4), (-1.33, -7.4, 0), (-1.33, -7.4, 6.1), .03)
    plant("planta_beco", (-1.1, -1.6, 0), 1.1)
    # mancha escura de chão molhado / sarjeta
    box("canaleta", M.plain("canaleta", "#55534e", .3), (1.0, -14, -.001), (1.35, 0, .004))

    # ---------------- largo e escadaria (y >= 0)
    # 1º lance: sobe em +Y, x 0.2..1.6, 8 degraus (0.30 x 0.20) até z=1.6 em y=3.4
    stairs("escada1", .2, 1.6, .9, 0, 8, .30, .20, "y", 1)
    box("patamar", M.concrete("degrau", "#a19d93", 1.3), (.2, 3.3, 0), (4.2, 4.8, 1.6), .012)
    # 2º lance: sobe em +X a partir do patamar, encostado na fachada (y 3.9..4.8)
    s2 = []
    for i in range(6):
        s2.append(box(f"escada2_{i}", M.concrete("degrau", "#a19d93", 1.3), (1.9 + i*.3, 3.9, 1.6), (4.2, 4.8, 1.6 + (i+1)*.2), .012))
    join(s2, "escada2")
    # parede lateral à direita do 1º lance (mureta que acompanha a escada)
    box("mureta_dir", gray, (1.6, .2, 0), (1.85, 3.3, 1.0), .01)
    for i, (y, sz) in enumerate(((.6, 1.0), (1.6, .8), (2.6, 1.2))):
        plant(f"vaso_mureta{i}", (1.72, y, 1.0), sz*.8, pot=("#3a2a22", "#7a2f22", "#2d2d2d")[i])
    # casa amarela "34" atrás do patamar
    walls.append(box("casa34", yellow, (-.6, 4.8, 0), (5.0, 9.0, 7.0)))
    box("casa34_laje", M.concrete("laje", "#c9c5b8"), (-.7, 4.6, 3.55), (5.1, 4.8, 3.7), .01)
    window("casa34_porta", Vector((.9, 4.8, 2.65)), (0, -1, 0), .85, 2.1, "porta")
    window("casa34_jan", Vector((-.1 + .0, 4.8, 2.2)), (0, -1, 0), .5, .7, "grade")
    window("casa34_jan2", Vector((2.6, 4.8, 5.3)), (0, -1, 0), 1.1, 1.0, "grade")
    window("casa34_jan3", Vector((.6, 4.8, 5.3)), (0, -1, 0), .9, 1.0, "veneziana")
    num = bpy.data.curves.new("num34", 'FONT'); num.body = "34"; num.size = .22; num.extrude = .005; num.align_x = 'CENTER'
    try: num.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    except Exception: pass
    no = _link(bpy.data.objects.new("num34", num)); no.data.materials.append(M.plain("tinta_num", "#6a6550", .8))
    no.location = (2.2, 4.79, 3.0); no.rotation_euler = (D(90), 0, 0)
    meter_box("luz34a", Vector((-.25, 4.8, 3.0)), (0, -1, 0))
    meter_box("luz34b", Vector((.15, 4.8, 3.0)), (0, -1, 0))
    tube("cano34", M.plain("pvc", "#dcdcd6", .4), (4.4, 4.77, 1.6), (4.4, 4.77, 6.9), .03)
    plant("vaso_patamar", (3.9, 3.55, 1.6), 1.0, "#2d2d2d")
    # corrimões azuis do 1º lance (dos dois lados) e do patamar
    rail_line("corr_esq", (.22, .9, 0), (.22, 3.3, 1.6), .8)
    rail_line("corr_meio", (1.55, .9, 0), (1.55, 3.3, 1.6), .8)
    rail_line("corr_pat", (.22, 3.3, 1.6), (.22, 4.75, 1.6), .7)
    rail_line("corr_esc2", (1.9, 3.88, 1.6), (4.2, 3.88, 2.8), .8)
    # patamar baixo à esquerda com mureta + corrimão (cena final)
    box("patio", con, (-4.5, 2.0, 0), (.2, 4.8, .45), .01)
    box("patio_degrau", con, (-1.6, 1.65, 0), (-.6, 2.0, .22), .01)
    rail_line("corr_patio_a", (-4.4, 2.0, .45), (-1.65, 2.0, .45), .9)
    rail_line("corr_patio_b", (-.55, 2.0, .45), (.18, 2.0, .45), .7)
    # casa creme com janela gradeada e grade na porta (à esquerda)
    walls.append(box("casa_esq", cream, (-6.0, 4.8, 0), (-.6, 9.0, 6.5)))
    window("casa_esq_jan", Vector((-2.4, 4.8, 1.75)), (0, -1, 0), 1.4, 1.3, "grade")
    window("casa_esq_porta", Vector((-4.0, 4.8, 1.5)), (0, -1, 0), .9, 2.1, "portao")
    window("casa_esq_jan2", Vector((-3.0, 4.8, 4.6)), (0, -1, 0), 1.2, 1.1, "grade")
    meter_box("luzesq", Vector((-1.2, 4.8, 1.6)), (0, -1, 0))
    for i, x in enumerate((-3.3, -1.0)):
        plant(f"vaso_patio{i}", (x, 4.45, .45), .9)
    # lado esquerdo do largo fecha com a parede verde até o patio
    walls.append(box("parede_largo_esq", mint, (-6.0, -.4, 0), (-1.35, .2, 6.2)))
    # lado direito: casa cinza alta
    walls.append(box("casa_dir", gray, (1.85, -.4, 0), (5.5, 3.3, 7.5)))
    window("casa_dir_jan", Vector((1.85, 1.9, 4.5)), (-1, 0, 0), .8, 1.0, "grade")
    # ---------------- fundo: prédios mais altos, azul, tijolo, rosa
    box("fundo_azul", teal, (-1.0, 9.0, 0), (3.0, 12.0, 11.0))
    box("fundo_tijolo", brick, (3.0, 9.0, 0), (7.0, 13.0, 9.5))
    box("fundo_rosa", pink, (-6.0, 9.0, 0), (-1.0, 12.0, 9.0))
    for i, (x, z) in enumerate(((.0, 8.0), (1.8, 8.0), (.0, 10.0), (1.8, 10.0))):
        window(f"fundo_azul_j{i}", Vector((x, 9.0, z)), (0, -1, 0), .9, 1.0, "grade")
    for i, (x, z) in enumerate(((4.2, 7.8), (5.8, 7.8))):
        window(f"fundo_tij_j{i}", Vector((x, 9.0, z)), (0, -1, 0), .8, .9, "grade", frame="#cfc7b6")
    for i, (x, z) in enumerate(((-4.5, 7.6), (-2.5, 7.6))):
        window(f"fundo_rosa_j{i}", Vector((x, 9.0, z)), (0, -1, 0), .9, 1.0, "veneziana")
    # prédios atrás da câmera no beco (para os contraplanos)
    box("fundo_beco", pink, (-3, -16, 0), (3, -14, 8))
    window("fundo_beco_j", Vector((0, -14, 2.0)), (0, 1, 0), 1.0, 1.1, "grade")
    # fios cruzando o céu
    wires("fio", [((-1.35, -10, 5.6), (1.35, -6, 5.2)), ((-1.35, -4, 5.8), (1.35, -1, 5.0)), ((-1.35, -2, 5.5), (2.0, 4.8, 6.6)),
                  ((-1.3, .5, 6.0), (2.5, 9.0, 8.0)), ((1.35, -8, 5.0), (-1.35, -12, 5.6)), ((-1.0, 9.0, 9.0), (1.85, 2.0, 6.8))], .4)
    return COL

def sky_and_sun(scene, sun_elev=70, sun_rot=200, strength=.34, sun_energy=5.0):
    w = bpy.data.worlds.new("ceu"); scene.world = w; w.use_nodes = True
    nt = w.node_tree; sky = nt.nodes.new("ShaderNodeTexSky")
    try: sky.sky_type = 'NISHITA'
    except Exception: pass
    try:
        sky.sun_elevation = D(sun_elev); sky.sun_rotation = D(sun_rot); sky.sun_disc = False
        sky.air_density = 1.2; sky.dust_density = 1.5
    except Exception: pass
    nt.links.new(sky.outputs[0], nt.nodes["Background"].inputs[0])
    nt.nodes["Background"].inputs[1].default_value = strength
    sun = bpy.data.objects.new("sol", bpy.data.lights.new("sol", 'SUN'))
    sun.data.energy = sun_energy; sun.data.angle = D(.8); sun.data.color = (1, .93, .84)
    # o sol vem da direção (sun_rot, sun_elev); a luz aponta no sentido oposto
    sun.rotation_euler = (D(90 - sun_elev), 0, D(sun_rot + 90))
    scene.collection.objects.link(sun)
    return sun
