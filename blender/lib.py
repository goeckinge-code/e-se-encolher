"""Blocos de construção em bpy: materiais, primitivas e o personagem Léo em 3D."""
import bpy, math
from mathutils import Vector

def hexcol(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    lin = [((x+0.055)/1.055)**2.4 if x > 0.04045 else x/12.92 for x in c]
    return (*lin, a)

_MATS = {}
def mat(h, rough=0.5):
    if h in _MATS: return _MATS[h]
    m = bpy.data.materials.new(h); m.diffuse_color = hexcol(h); m.roughness = rough; m.metallic = 0
    _MATS[h] = m; return m

def setmat(o, h):
    o.data.materials.clear(); o.data.materials.append(mat(h)); return o

def smooth(o, sub=2):
    for p in o.data.polygons: p.use_smooth = True
    if sub:
        m = o.modifiers.new("s", "SUBSURF"); m.levels = sub; m.render_levels = sub
    return o

def link(o, parent=None, coll=None):
    (coll or bpy.context.scene.collection).objects.link(o)
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; link(e, parent); return e

def _new(op, name, color, loc, parent, sub, **kw):
    op(location=(0, 0, 0), **kw)
    o = bpy.context.object; o.name = name
    bpy.context.scene.collection.objects.unlink(o) if o.name in bpy.context.scene.collection.objects and False else None
    o.location = loc
    if parent: o.parent = parent
    setmat(o, color); smooth(o, sub)
    return o

def sphere(name, color, loc=(0, 0, 0), r=1, scale=(1, 1, 1), parent=None, sub=1, seg=24):
    o = _new(bpy.ops.mesh.primitive_uv_sphere_add, name, color, loc, parent, sub, radius=r, segments=seg, ring_count=seg//2)
    o.scale = scale; return o

def cube(name, color, loc=(0, 0, 0), size=(1, 1, 1), parent=None, bevel=0.05, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    o = bpy.context.object; o.name = name; o.scale = size; o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    setmat(o, color)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        m = o.modifiers.new("b", "BEVEL"); m.width = bevel; m.segments = 4; m.limit_method = 'NONE'
    for p in o.data.polygons: p.use_smooth = True
    return o

def cyl(name, color, loc=(0, 0, 0), r=1, depth=1, parent=None, rot=(0, 0, 0), bevel=0.02, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=(0, 0, 0))
    o = bpy.context.object; o.name = name; o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    setmat(o, color)
    if bevel:
        m = o.modifiers.new("b", "BEVEL"); m.width = bevel; m.segments = 3; m.limit_method = 'ANGLE'
    for p in o.data.polygons: p.use_smooth = True
    return o

def capsule(name, color, a, b, r, parent=None):
    """cápsula entre pontos a e b (coords locais do parent)"""
    a, b = Vector(a), Vector(b); d = b - a
    o = cyl(name, color, loc=(a+b)/2, r=r, depth=d.length, parent=parent, bevel=0)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    for i, p in enumerate((a, b)):
        sphere(f"{name}_cap{i}", color, loc=p, r=r, parent=parent, sub=0, seg=20)
    return o

def torus(name, color, loc, R, r, parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=(0, 0, 0), major_segments=40, minor_segments=12)
    o = bpy.context.object; o.name = name; o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    setmat(o, color)
    for p in o.data.polygons: p.use_smooth = True
    return o

def arc_tube(name, color, center, R, r, a0, a1, parent=None, rot=(0, 0, 0)):
    """arco (sorriso / sobrancelha) feito de curva com bevel"""
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); n = 16; sp.points.add(n-1)
    for i in range(n):
        a = a0 + (a1-a0)*i/(n-1)
        sp.points[i].co = (math.cos(a)*R, 0, math.sin(a)*R, 1)
    o = bpy.data.objects.new(name, cu); o.location = center; o.rotation_euler = rot
    link(o, parent); o.data.materials.append(mat(color)); return o

def poly_tube(name, color, pts, r, parent=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i, p in enumerate(pts): sp.points[i].co = (*p, 1)
    o = bpy.data.objects.new(name, cu); link(o, parent); o.data.materials.append(mat(color)); return o

def text3d(name, txt, color, loc, size=1, parent=None, rot=(math.pi/2, 0, 0), extrude=0.02):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.extrude = extrude; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    o = bpy.data.objects.new(name, cu); o.location = loc; o.rotation_euler = rot; link(o, parent); o.data.materials.append(mat(color)); return o

def key(o, frame, **props):
    for k, v in props.items():
        setattr(o, k, v); o.keyframe_insert(k, frame=frame)

def show_key(o, frame, visible):
    o.hide_render = not visible; o.keyframe_insert("hide_render", frame=frame)
    for fc in (o.animation_data.action.fcurves if hasattr(o.animation_data.action, 'fcurves') else []):
        pass

# ------------------------------------------------------------------ Léo
SKIN, HAIR, CAP, CAP_D, SHIRT, JEANS, LIMB, SHOE, PHONE, INKC = "#E3A97E", "#3B2418", "#E63946", "#B32634", "#FFC93C", "#3D5A99", "#2F3550", "#F7F7F2", "#2EC4B6", "#1E1B2E"

class Leo:
    """Personagem no molde da referência (corpo-pílula, membros finos, cabeça grande), em 3D.
    Unidades: altura total ~2.0. Pés na origem do root. Frente para -Y."""
    def __init__(self, name="leo"):
        n = name
        self.root = empty(n)                      # posição/escala/rotação geral
        self.hip = empty(n+"_hip", (0, 0, 0.5), self.root)   # sobe/desce (respiração)
        hp = self.hip
        # pernas
        for sx in (-1, 1):
            capsule(f"{n}_leg{sx}", "#26324F", (sx*0.09, 0, -0.04), (sx*0.09, 0, -0.44), 0.042, hp)
            s = sphere(f"{n}_shoe{sx}", SHOE, (sx*0.13, -0.05, -0.47), 0.09, (1, 1.35, 0.55), hp, sub=1)
            sphere(f"{n}_sole{sx}", CAP, (sx*0.13, -0.05, -0.505), 0.088, (1.02, 1.37, 0.18), hp, sub=1)
        # corpo pílula: jeans embaixo, camiseta em cima
        self.torso = empty(n+"_torso", (0, 0, 0), hp)
        tz = self.torso
        sphere(n+"_jeans", JEANS, (0, 0, 0.30), 0.25, (1, 0.92, 1.38), tz, sub=2, seg=32)
        self.shirt = sphere(n+"_shirt", SHIRT, (0, 0, 0.30), 0.258, (1, 0.94, 1.39), tz, sub=2, seg=48)
        self._cut_lower(self.shirt, 0.26)
        self.shirt_parts = [self.shirt]
        # raio no peito
        bolt = text3d(n+"_bolt", "⚡", "#E8452C", (0, -0.25, 0.42), 0.0001, tz)
        bolt.hide_render = True
        pts = [(-0.02, 0.55), (0.07, 0.55), (0.02, 0.45), (0.08, 0.45), (-0.05, 0.30), (-0.01, 0.42), (-0.07, 0.42)]
        me = bpy.data.meshes.new(n+"_boltm"); me.from_pydata([(x, 0, z) for x, z in pts], [], [list(range(len(pts)))])
        bo = bpy.data.objects.new(n+"_bolt2", me); link(bo, tz); bo.location = (0, -0.243, -0.02); bo.data.materials.append(mat("#E8452C"))
        sol = bo.modifiers.new("t", "SOLIDIFY"); sol.thickness = 0.02
        # fone no pescoço
        torus(n+"_band", "#3A3A48", (0, 0.0, 0.66), 0.17, 0.025, tz, rot=(math.radians(70), 0, 0))
        for sx in (-1, 1):
            cyl(f"{n}_cup{sx}", PHONE, (sx*0.17, -0.06, 0.64), 0.065, 0.06, tz, rot=(0, math.radians(90), 0), bevel=0.015)
        # braços (pivô no ombro)
        self.arm = {}
        for sx in (-1, 1):
            sh = empty(f"{n}_sh{sx}", (sx*0.23, 0, 0.55), tz)
            sphere(f"{n}_slv{sx}", SHIRT, (0, 0, -0.03), 0.085, (1, 1, 1.1), sh, sub=1)
            capsule(f"{n}_arm{sx}", LIMB, (0, 0, -0.03), (sx*0.06, 0, -0.38), 0.035, sh)
            sphere(f"{n}_hand{sx}", SKIN, (sx*0.06, 0, -0.41), 0.058, parent=sh, sub=1)
            self.arm[sx] = sh
        # cabeça (pivô no pescoço)
        self.head = empty(n+"_head", (0, 0, 0.7), tz)
        hd = self.head
        self.skull = sphere(n+"_skull", SKIN, (0, 0, 0.38), 0.4, parent=hd, sub=2, seg=32)
        sphere(n+"_hairback", HAIR, (0, 0.06, 0.45), 0.405, (1, 1, 0.98), hd, sub=1, seg=32)
        for sx in (-1, 1):
            sphere(f"{n}_ear{sx}", SKIN, (sx*0.39, 0.02, 0.36), 0.07, (0.5, 0.8, 1), hd, sub=1)
            sphere(f"{n}_blush{sx}", "#EE8C83", (sx*0.21, -0.33, 0.29), 0.075, (1, 0.35, 0.6), hd, sub=1)
            sphere(f"{n}_side{sx}", HAIR, (sx*0.36, -0.06, 0.5), 0.09, (0.5, 0.9, 1.3), hd, sub=1)
        # boné virado pra trás
        cap = sphere(n+"_cap", CAP, (0, 0.02, 0.52), 0.43, (1, 1, 0.78), hd, sub=1, seg=32)
        self._cut_lower(cap, 0.52+0.02)
        torus(n+"_capband", CAP_D, (0, 0.02, 0.555), 0.405, 0.03, hd, rot=(0, 0, 0))
        sphere(n+"_capbtn", CAP_D, (0, 0.02, 0.88), 0.045, parent=hd, sub=1)
        bill = cube(n+"_bill", CAP_D, (0.2, 0.44, 0.57), (0.40, 0.34, 0.035), hd, bevel=0.015, rot=(math.radians(-8), 0, math.radians(35)))
        sphere(n+"_tuft", HAIR, (0, -0.37, 0.6), 0.1, (1.1, 0.5, 0.55), hd, sub=1)
        for k in range(5):
            sphere(f"{n}_fr{k}", HAIR, (-0.2+k*0.1, -0.33, 0.53), 0.06, (1, 0.6, 0.8), hd, sub=1)
        # olhos (variações) — objetos com visibilidade animada
        self.eyes = {}; self.mouths = {}
        def grp(nm):
            e = empty(nm, (0, 0, 0), hd); return e
        g = grp(n+"_e_dot")
        for sx in (-1, 1):
            sphere(f"{n}_eye{sx}", INKC, (sx*0.13, -0.375, 0.42), 0.055, (1, 0.5, 1.25), g, sub=1)
            sphere(f"{n}_glint{sx}", "#FFFFFF", (sx*0.13+0.02, -0.405, 0.45), 0.016, parent=g, sub=0, seg=12)
        self.eyes["dot"] = g
        g = grp(n+"_e_shock")
        for sx in (-1, 1):
            sphere(f"{n}_eyew{sx}", "#FFFFFF", (sx*0.14, -0.36, 0.43), 0.1, (1, 0.45, 1.1), g, sub=1)
            sphere(f"{n}_eyep{sx}", INKC, (sx*0.14, -0.405, 0.42), 0.04, (1, 0.5, 1), g, sub=1)
        self.eyes["shock"] = g
        g = grp(n+"_e_happy")
        for sx in (-1, 1):
            arc_tube(f"{n}_eh{sx}", INKC, (sx*0.13, -0.385, 0.39), 0.06, 0.016, math.radians(20), math.radians(160), g, rot=(0, 0, 0))
        self.eyes["happy"] = g
        g = grp(n+"_e_closed")
        for sx in (-1, 1):
            arc_tube(f"{n}_ec{sx}", INKC, (sx*0.13, -0.385, 0.45), 0.06, 0.016, math.radians(200), math.radians(340), g)
        self.eyes["closed"] = g
        g = grp(n+"_e_dizzy")
        for sx in (-1, 1):
            pts = [(sx*0.13+math.cos(k*0.5)*k*0.0028, -0.39, 0.42+math.sin(k*0.5)*k*0.0028) for k in range(36)]
            poly_tube(f"{n}_ed{sx}", INKC, pts, 0.008, g)
        self.eyes["dizzy"] = g
        # sobrancelhas
        self.brow = {}
        for sx in (-1, 1):
            b = empty(f"{n}_brow{sx}", (sx*0.13, -0.37, 0.53), hd)
            cube(f"{n}_browm{sx}", HAIR, (0, 0, 0), (0.13, 0.04, 0.035), b, bevel=0.015)
            self.brow[sx] = b
        # bocas
        g = grp(n+"_m_line"); arc_tube(n+"_ml", INKC, (0, -0.385, 0.29), 0.06, 0.014, math.radians(200), math.radians(340), g); self.mouths["line"] = g
        g = grp(n+"_m_smile")
        s = sphere(n+"_ms", "#8E2430", (0, -0.37, 0.25), 0.09, (1, 0.4, 0.75), g, sub=1); self._cut_upper(s, 0.25)
        self.mouths["smile"] = g
        g = grp(n+"_m_o"); sphere(n+"_mo", "#6B1E2A", (0, -0.385, 0.25), 0.05, (0.9, 0.35, 1.25), g, sub=1); self.mouths["o"] = g
        g = grp(n+"_m_yawn"); sphere(n+"_my", "#6B1E2A", (0, -0.38, 0.24), 0.075, (1, 0.35, 1.3), g, sub=1); self.mouths["yawn"] = g
        g = grp(n+"_m_wavy")
        poly_tube(n+"_mw", INKC, [(-0.07+i*0.0175, -0.39, 0.27+(0.012 if i % 2 else -0.012)) for i in range(9)], 0.012, g); self.mouths["wavy"] = g
        g = grp(n+"_m_teeth"); cube(n+"_mt", "#FFFFFF", (0, -0.385, 0.27), (0.14, 0.03, 0.06), g, bevel=0.02); self.mouths["teeth"] = g
        g = grp(n+"_m_small"); sphere(n+"_msm", INKC, (0, -0.39, 0.27), 0.022, (1, 0.4, 0.8), g, sub=0); self.mouths["small"] = g
        self.all_parts = [o for o in bpy.data.objects if o.name.startswith(n+"_") or o.name == n]

    def _cut_lower(self, o, zcut):
        """remove a metade de baixo (boné) — aplica bisect via bmesh"""
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        local_z = (zcut - o.location.z)/o.scale.z
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, 0, local_z), plane_no=(0, 0, 1), clear_inner=True)
        bm.to_mesh(o.data); bm.free()

    def _cut_upper(self, o, zcut):
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        local_z = (zcut - o.location.z)/o.scale.z
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, 0, local_z), plane_no=(0, 0, 1), clear_outer=True)
        bm.to_mesh(o.data); bm.free()

EXPR_EYE = {"neutral": "dot", "happy": "happy", "worried": "dot", "shock": "shock", "tired": "closed", "sleep": "closed", "dizzy": "dizzy", "strain": "closed"}
EXPR_MOUTH = {"neutral": "line", "happy": "smile", "worried": "wavy", "shock": "o", "tired": "line", "sleep": "small", "dizzy": "wavy", "strain": "teeth"}
EXPR_BROW = {"neutral": (0, 0), "happy": (0.02, 0), "worried": (0.02, 18), "shock": (0.06, 4), "tired": (-0.02, 6), "sleep": (-0.02, 0), "dizzy": (0.03, -12), "strain": (-0.01, -20)}
