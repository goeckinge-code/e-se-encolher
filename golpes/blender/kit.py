"""Kit 3D da série de golpes: bonecos de blocos, objetos e utilidades de animação (bpy, Workbench).

Eixos: Z para cima, a câmera olha para +Y, os bonecos olham para -Y (para a câmera).
"""
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(os.path.dirname(HERE), "assets", "fonts", "LilitaOne.ttf")

# ------------------------------------------------------------------ cores e materiais
def hexcol(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c], a)

_M = {}
def mat(h):
    if h not in _M:
        m = bpy.data.materials.new(h); m.diffuse_color = hexcol(h); m.roughness = 0.6; _M[h] = m
    return _M[h]

def link(o, parent=None):
    bpy.context.scene.collection.objects.link(o)
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); e.location = loc; e.rotation_euler = rot; return link(e, parent)

_MESH = {}
def _cube_mesh(size, bevel):
    """Malha de bloco no tamanho real com cantos arredondados (bmesh), compartilhada por tamanho."""
    key = (round(size[0], 3), round(size[1], 3), round(size[2], 3), round(bevel, 3))
    if key in _MESH: return _MESH[key]
    import bmesh
    me = bpy.data.meshes.new("cube"); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=bevel, segments=2, affect='EDGES', profile=0.5)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    _MESH[key] = me; return me

def box(name, color, size=(1, 1, 1), loc=(0, 0, 0), parent=None, rot=(0, 0, 0), bevel=0.04):
    """Bloco no tamanho `size` (m), cantos arredondados de `bevel` m."""
    b = min(bevel, min(size) * 0.45)
    o = bpy.data.objects.new(name, _cube_mesh(size, b))
    o.location = loc; o.rotation_euler = rot; o.color = hexcol(color)
    return link(o, parent)

def cyl(name, color, r=0.5, depth=1, loc=(0, 0, 0), parent=None, rot=(0, 0, 0), verts=24):
    key = ("cyl", verts)
    if key not in _MESH:
        import bmesh
        me = bpy.data.meshes.new(f"cyl{verts}"); bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=0.5, radius2=0.5, depth=1.0)
        bm.to_mesh(me); bm.free()
        for p in me.polygons: p.use_smooth = len(p.vertices) == 4
        _MESH[key] = me
    o = bpy.data.objects.new(name, _MESH[key]); o.scale = (2 * r, 2 * r, depth)
    o.location = loc; o.rotation_euler = rot; o.color = hexcol(color)
    return link(o, parent)

def sphere(name, color, r=0.5, loc=(0, 0, 0), parent=None, scale=(1, 1, 1)):
    if "sph" not in _MESH:
        import bmesh
        me = bpy.data.meshes.new("sph"); bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.5)
        bm.to_mesh(me); bm.free()
        for p in me.polygons: p.use_smooth = True
        _MESH["sph"] = me
    o = bpy.data.objects.new(name, _MESH["sph"]); o.scale = (2 * r * scale[0], 2 * r * scale[1], 2 * r * scale[2])
    o.location = loc; o.color = hexcol(color); return link(o, parent)

def text(name, body, color="#1E1B2E", size=0.3, loc=(0, 0, 0), parent=None, rot=(math.pi / 2, 0, 0), depth=0.0, align='CENTER'):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size; cu.extrude = depth
    cu.align_x = align; cu.align_y = 'CENTER'
    if os.path.exists(FONT):
        f = bpy.data.fonts.get("Lilita") or bpy.data.fonts.load(FONT); f.name = "Lilita"; cu.font = f
    o = bpy.data.objects.new(name, cu); o.location = loc; o.rotation_euler = rot; o.color = hexcol(color)
    return link(o, parent)

# ------------------------------------------------------------------ cena / luz / câmera
def setup(bg="#BFE8DA", aa='8'):
    s = bpy.context.scene
    s.render.engine = 'BLENDER_WORKBENCH'
    d = s.display; sh = d.shading
    # Luz plana (cores exatas) + sombreado nas bordas (cavity) + sombra suave: visual de brinquedo
    sh.light = 'FLAT'; sh.color_type = 'OBJECT'
    sh.show_shadows = True; sh.shadow_intensity = 0.25
    sh.show_cavity = True; sh.cavity_type = 'BOTH'
    sh.cavity_ridge_factor = 0.5; sh.cavity_valley_factor = 1.0
    sh.curvature_ridge_factor = 0.5; sh.curvature_valley_factor = 0.5
    sh.show_specular_highlight = False
    sh.background_type = 'VIEWPORT'; sh.background_color = hexcol(bg)[:3]
    d.light_direction = (-0.45, -0.55, 0.75); d.shadow_shift = 0.05; d.shadow_focus = 0.25
    d.render_aa = aa
    s.view_settings.view_transform = 'Standard'
    w = s.world or bpy.data.worlds.new("w"); s.world = w; w.color = hexcol(bg)[:3]
    return s

def camera(lens=40):
    c = bpy.data.cameras.new("cam"); c.lens = lens; c.sensor_fit = 'VERTICAL'; c.sensor_height = 24
    o = bpy.data.objects.new("cam", c); link(o); bpy.context.scene.camera = o
    return o

def look(cam, pos, target, roll=0.0):
    cam.location = Vector(pos)
    d = Vector(target) - Vector(pos)
    q = d.to_track_quat('-Z', 'Y'); cam.rotation_euler = q.to_euler()
    cam.rotation_euler.rotate_axis('Z', roll)

def room(floor="#E6D3C3", wall="#8FC9B0", depth=6, width=14, wall_h=9, base=None):
    """Chão + parede de fundo (+ rodapé)."""
    box("floor", floor, (width, 14, 0.2), (0, 2, -0.1), bevel=0)
    box("wall", wall, (width, 0.2, wall_h), (0, depth, wall_h / 2), bevel=0)
    if base: box("base", base, (width, 0.24, 0.22), (0, depth - 0.12, 0.11), bevel=0.01)

def cyclo(color, w=120):
    """Fundo infinito de uma cor só (chão e parede da mesma cor)."""
    box("floor", color, (w, 120, 0.2), (0, 30, -0.1), bevel=0)
    box("wall", color, (w, 0.2, 80), (0, 40, 40), bevel=0)
    bpy.context.scene.world.color = hexcol(color)[:3]

# ------------------------------------------------------------------ animação
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x, s=1.9):
    x = clamp(x); x -= 1; return 1 + x * x * ((s + 1) * x + s)
def lerp(a, b, k): return a + (b - a) * k
def vlerp(a, b, k): return tuple(lerp(x, y, k) for x, y in zip(a, b))
def ramp(t, t0, d): return clamp((t - t0) / d) if d > 0 else float(t >= t0)

def pop(o, t, t0, d=0.28, base=None):
    """Aparece crescendo com um quique em t0. Antes de t0 fica escondido."""
    base = base or o.get("_base")
    if base is None: base = tuple(o.scale); o["_base"] = base
    k = back(ramp(t, t0, d)) if t >= t0 else 0
    o.scale = tuple(max(1e-4, b * k) for b in base)
    o.hide_render = t < t0

def show(o, on):
    o.hide_render = not on
    for c in o.children_recursive: c.hide_render = not on

def keys(t, pts):
    """Interpola [(tempo, valor_tuple), ...] com smoothstep."""
    if t <= pts[0][0]: return pts[0][1]
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        if t <= t1: return vlerp(a, b, smooth((t - t0) / (t1 - t0)))
    return pts[-1][1]

# ------------------------------------------------------------------ boneco de blocos
SKINS = ["#F1C7A5", "#D9A07A", "#B97A54", "#8A5A3C", "#F5D0B5"]

class Person:
    """Boneco de blocos (~2,05 m). Partes com pivô: hip, legL/R, armL/R, head.
    style: dict(skin, top, pants, shoes, hair, hair_style, suit, tie, old)."""
    def __init__(self, name, loc=(0, 0, 0), rotz=0.0, **style):
        st = dict(skin="#F1C7A5", top="#3C6E71", pants="#3B3F4C", shoes="#1E1E24", hair="#4A3020",
                  hair_style="short", suit=False, tie="#D63031", old=False, scale=1.0)
        st.update(style); self.st = st; self.name = name
        self.root = empty(name, loc, rot=(0, 0, rotz)); self.root.scale = (st["scale"],) * 3
        r = self.root
        self.hip = empty(name + "_hip", (0, 0, 0.78), r)
        self.legs = []
        for i, x in enumerate((-0.15, 0.15)):
            p = empty(f"{name}_leg{i}", (x, 0, 0), self.hip)
            box(f"{name}_legm{i}", st["pants"], (0.25, 0.27, 0.74), (0, 0, -0.37), p)
            box(f"{name}_shoe{i}", st["shoes"], (0.27, 0.36, 0.13), (0, -0.04, -0.72), p, bevel=0.04)
            self.legs.append(p)
        self.body = empty(name + "_body", (0, 0, 0), self.hip)
        b = self.body
        box(name + "_torso", st["top"], (0.7, 0.38, 0.74), (0, 0, 0.37), b, bevel=0.05)
        if st["suit"]:
            box(name + "_shirt", "#F4F4F4", (0.2, 0.02, 0.4), (0, -0.19, 0.53), b, bevel=0.005)
            box(name + "_tie", st["tie"], (0.09, 0.03, 0.36), (0, -0.2, 0.5), b, bevel=0.01)
            box(name + "_knot", st["tie"], (0.11, 0.035, 0.07), (0, -0.205, 0.69), b, bevel=0.01)
            for sx in (-1, 1):
                box(f"{name}_lapel{sx}", _shade(st["top"], 0.8), (0.07, 0.02, 0.36), (sx * 0.14, -0.195, 0.52), b,
                    rot=(0, sx * 0.35, 0), bevel=0.005)
            box(name + "_btn", "#1E1E24", (0.05, 0.02, 0.05), (0, -0.195, 0.24), b, bevel=0.01)
        self.arms = []
        for i, x in enumerate((-0.44, 0.44)):
            p = empty(f"{name}_arm{i}", (x, 0, 0.68), b)
            box(f"{name}_armm{i}", st["top"], (0.2, 0.24, 0.6), (0, 0, -0.27), p)
            box(f"{name}_hand{i}", st["skin"], (0.18, 0.21, 0.17), (0, 0, -0.64), p, bevel=0.04)
            self.arms.append(p)
        self.head = empty(name + "_head", (0, 0, 0.76), b)
        h = self.head
        box(name + "_headm", st["skin"], (0.6, 0.56, 0.58), (0, 0, 0.3), h, bevel=0.05)
        self._face(st)
        self._hair(st)
        self.anchor = empty(name + "_top", (0, 0, 0.78 + 0.76 + 0.72), r)   # ponto acima da cabeça (etiquetas)
        self.anchor.name = name
        self.root.name = name + "_root"
        self.expr("smile")

    def _face(self, st):
        n, h, y = self.name, self.head, -0.285
        self.eyes = [box(f"{n}_eye{i}", "#1E1B2E", (0.075, 0.02, 0.1), (x, y, 0.34), h, bevel=0.015) for i, x in enumerate((-0.13, 0.13))]
        self.brows = [box(f"{n}_brow{i}", _shade(st["hair"], 0.8) if not st["old"] else "#9A9A9A", (0.14, 0.02, 0.035),
                          (x, y, 0.45), h, bevel=0.01) for i, x in enumerate((-0.13, 0.13))]
        self.nose = box(n + "_nose", _shade(st["skin"], 0.9), (0.07, 0.05, 0.09), (0, y - 0.02, 0.26), h, bevel=0.02)
        self.mouths = {}
        mc = "#6B2A2A"
        g = empty(n + "_m_smile", (0, y, 0.14), h)
        box(n + "_ms1", mc, (0.16, 0.02, 0.035), (0, 0, 0), g, bevel=0.01)
        box(n + "_ms2", mc, (0.035, 0.02, 0.05), (-0.08, 0, 0.025), g, bevel=0.01)
        box(n + "_ms3", mc, (0.035, 0.02, 0.05), (0.08, 0, 0.025), g, bevel=0.01)
        self.mouths["smile"] = g
        g = empty(n + "_m_grin", (0, y, 0.13), h)
        box(n + "_mg1", mc, (0.2, 0.02, 0.09), (0, 0, 0), g, bevel=0.02)
        box(n + "_mg2", "#FFFFFF", (0.16, 0.025, 0.03), (0, -0.002, 0.02), g, bevel=0.005)
        self.mouths["grin"] = g
        g = empty(n + "_m_sad", (0, y, 0.12), h)
        box(n + "_md1", mc, (0.16, 0.02, 0.035), (0, 0, 0.03), g, bevel=0.01)
        box(n + "_md2", mc, (0.035, 0.02, 0.05), (-0.08, 0, 0.0), g, bevel=0.01)
        box(n + "_md3", mc, (0.035, 0.02, 0.05), (0.08, 0, 0.0), g, bevel=0.01)
        self.mouths["sad"] = g
        g = empty(n + "_m_o", (0, y, 0.13), h)
        box(n + "_mo1", mc, (0.09, 0.02, 0.11), (0, 0, 0), g, bevel=0.02)
        self.mouths["o"] = g
        g = empty(n + "_m_flat", (0, y, 0.14), h)
        box(n + "_mf1", mc, (0.15, 0.02, 0.03), (0, 0, 0), g, bevel=0.01)
        self.mouths["flat"] = g

    def _hair(self, st):
        n, h, c, hs = self.name, self.head, st["hair"], st["hair_style"]
        if hs == "short":      # cabelinho normal, com risca de lado e topete pequeno
            box(n + "_hair1", c, (0.64, 0.6, 0.13), (0, 0.01, 0.62), h, bevel=0.04)
            box(n + "_hair2", c, (0.64, 0.14, 0.42), (0, 0.24, 0.42), h, bevel=0.03)
            box(n + "_hair3", c, (0.08, 0.5, 0.22), (-0.31, 0.04, 0.5), h, bevel=0.02)
            box(n + "_hair4", c, (0.08, 0.5, 0.22), (0.31, 0.04, 0.5), h, bevel=0.02)
            box(n + "_hair5", c, (0.4, 0.14, 0.1), (0.1, -0.25, 0.62), h, rot=(0, -0.12, 0), bevel=0.03)
            box(n + "_hair6", c, (0.24, 0.14, 0.08), (-0.18, -0.25, 0.59), h, bevel=0.03)
        elif hs == "old":      # careca em cima, cabelo branco dos lados
            for sx in (-1, 1):
                box(f"{n}_ohair{sx}", c, (0.08, 0.44, 0.24), (sx * 0.31, 0.06, 0.38), h, bevel=0.03)
            box(n + "_ohairb", c, (0.6, 0.08, 0.26), (0, 0.29, 0.36), h, bevel=0.03)
        elif hs == "long":
            box(n + "_lhair1", c, (0.66, 0.62, 0.14), (0, 0.01, 0.62), h, bevel=0.05)
            box(n + "_lhair2", c, (0.68, 0.2, 0.7), (0, 0.24, 0.28), h, bevel=0.04)
            for sx in (-1, 1):
                box(f"{n}_lhs{sx}", c, (0.1, 0.4, 0.62), (sx * 0.33, 0.06, 0.3), h, bevel=0.03)
            box(n + "_lfr", c, (0.5, 0.12, 0.12), (0, -0.26, 0.6), h, bevel=0.03)
        elif hs == "cap":
            box(n + "_cap1", c, (0.66, 0.62, 0.2), (0, 0.0, 0.66), h, bevel=0.06)
            box(n + "_cap2", c, (0.5, 0.3, 0.05), (0, -0.4, 0.58), h, bevel=0.02)
        elif hs == "police":
            box(n + "_pcap1", "#22313F", (0.66, 0.64, 0.18), (0, 0.0, 0.67), h, bevel=0.05)
            box(n + "_pcap2", "#111820", (0.54, 0.26, 0.05), (0, -0.4, 0.6), h, bevel=0.02)
            box(n + "_pcap3", "#F1C40F", (0.12, 0.03, 0.1), (0, -0.33, 0.68), h, bevel=0.02)
        elif hs == "bald":
            pass

    def expr(self, name, brows=None):
        for k, g in self.mouths.items(): show(g, k == name)
        b = brows or {"sad": "sad", "o": "up", "grin": "up"}.get(name, "flat")
        for i, br in enumerate(self.brows):
            sx = -1 if i == 0 else 1
            br.rotation_euler = (0, {"sad": sx * 0.35, "angry": -sx * 0.35, "up": 0, "flat": 0}[b], 0)
            br.location.z = 0.47 if b == "up" else 0.45

    def pose(self, t, armL=0.0, armR=0.0, armLs=0.0, armRs=0.0, head=(0, 0, 0), bob=1.0, walk=0.0, phase=0.0):
        """armX: rotação para a frente (rad); armXs: abrir para o lado; walk: velocidade do passo."""
        w = math.sin(t * 9 + phase) * 0.55 * walk
        self.legs[0].rotation_euler.x = w; self.legs[1].rotation_euler.x = -w
        self.arms[0].rotation_euler = (-armL - w * 0.8, -armLs, 0)
        self.arms[1].rotation_euler = (-armR + w * 0.8, armRs, 0)
        self.body.location.z = abs(math.sin(t * 9 + phase)) * 0.05 * walk + math.sin(t * 2.6 + phase) * 0.012 * bob
        self.head.rotation_euler = head

    def blink(self, t, every=3.1, off=0.0):
        k = ((t + off) % every) < 0.09
        for e in self.eyes: e.scale.z = 0.15 if k else 1.0

def _shade(h, f):
    h = h.lstrip('#'); c = [min(255, int(int(h[i:i + 2], 16) * f)) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(c)

def hero(name="hero", loc=(0, 0, 0), rotz=0.0):
    """Protagonista: terno cinza-grafite, gravata vermelha, cabelo castanho curto."""
    return Person(name, loc, rotz, suit=True, top="#465066", pants="#465066", tie="#D63031",
                  hair="#5A3A22", hair_style="short", skin="#F1C7A5")

CROWD = [dict(top="#E67E22", pants="#34495E", hair="#2C1B10", skin=SKINS[0]),
         dict(top="#27AE60", pants="#5D6D7E", hair="#1E1E1E", skin=SKINS[2], hair_style="long"),
         dict(top="#8E44AD", pants="#2C3E50", hair="#D9C38A", skin=SKINS[4], hair_style="long"),
         dict(top="#2980B9", pants="#7F8C8D", hair="#111111", skin=SKINS[3], hair_style="cap"),
         dict(top="#C0392B", pants="#34495E", hair="#6E4B2A", skin=SKINS[1]),
         dict(top="#A07856", pants="#4E3B2E", hair="#EDEDED", skin=SKINS[0], hair_style="old", old=True),
         dict(top="#16A085", pants="#2C3E50", hair="#3B2A1E", skin=SKINS[2]),
         dict(top="#F1C40F", pants="#566573", hair="#151515", skin=SKINS[3], hair_style="long"),
         dict(top="#D35400", pants="#3E4A59", hair="#EDEDED", skin=SKINS[1], hair_style="old", old=True),
         dict(top="#5DADE2", pants="#2E4053", hair="#4A3020", skin=SKINS[0], hair_style="cap")]

def person(name, i, loc=(0, 0, 0), rotz=0.0, **kw):
    st = dict(CROWD[i % len(CROWD)]); st.update(kw); return Person(name, loc, rotz, **st)

# ------------------------------------------------------------------ objetos
def bill(name, loc=(0, 0, 0), parent=None, rot=(0, 0, 0), s=1.0):
    """Maço de notas verde com faixa branca."""
    g = empty(name, loc, parent, rot)
    box(name + "_b", "#3FAE5A", (0.42 * s, 0.22 * s, 0.1 * s), (0, 0, 0), g, bevel=0.01)
    box(name + "_f", "#EAF6E9", (0.08 * s, 0.23 * s, 0.105 * s), (0, 0, 0), g, bevel=0.005)
    return g

def coin(name, loc=(0, 0, 0), parent=None, r=0.25, rot=(math.pi / 2, 0, 0)):
    g = empty(name, loc, parent, rot)
    cyl(name + "_c", "#F5B82E", r, 0.07, (0, 0, 0), g, verts=28)
    cyl(name + "_i", "#FFD45C", r * 0.72, 0.075, (0, 0, 0), g, verts=28)
    return g

def coin_stack(name, n, loc, parent=None, r=0.3):
    g = empty(name, loc, parent)
    for i in range(n):
        cyl(f"{name}_{i}", "#F5B82E" if i % 2 else "#E9A824", r, 0.09, (0.01 * math.sin(i * 1.7), 0.01 * math.cos(i), 0.045 + i * 0.09), g, verts=24)
    return g

def safe(name, loc=(0, 0, 0), color="#7F8C8D", open_=0.0, parent=None, empty_=True):
    g = empty(name, loc, parent)
    box(name + "_body", color, (1.1, 1.0, 1.2), (0, 0, 0.6), g, bevel=0.06)
    box(name + "_in", "#2B2F33", (0.9, 0.05, 1.0), (0, -0.48, 0.6), g, bevel=0.01)
    hinge = empty(name + "_hinge", (-0.5, -0.52, 0.6), g)
    door = empty(name + "_door", (0, 0, 0), hinge)
    box(name + "_dm", _shade(color, 1.1), (1.0, 0.08, 1.1), (0.5, 0, 0), door, bevel=0.03)
    cyl(name + "_dial", "#2B2F33", 0.16, 0.06, (0.5, -0.05, 0.1), door, rot=(math.pi / 2, 0, 0))
    hinge.rotation_euler.z = -open_ * 1.9
    g["hinge"] = hinge.name
    return g

def board(name, loc, w=2.4, h=1.6, parent=None, header="#2E86DE", title="", lines=(), tsize=0.2, lsize=0.17, legs=True):
    """Cartão/placa branca com barra colorida no topo (estilo tela de app)."""
    g = empty(name, loc, parent)
    if legs:
        for sx in (-1, 1): box(f"{name}_leg{sx}", "#6B4F3A", (0.06, 0.06, 1.0), (sx * (w / 2 - 0.2), 0.05, 0.5), g, bevel=0.01)
    z0 = 1.0 if legs else 0
    box(name + "_card", "#FFFFFF", (w, 0.08, h), (0, 0, z0 + h / 2), g, bevel=0.03)
    box(name + "_head", header, (w, 0.1, 0.34), (0, -0.01, z0 + h - 0.17), g, bevel=0.03)
    if title: text(name + "_t", title, "#FFFFFF", tsize, (0, -0.08, z0 + h - 0.17), g)
    for i, ln in enumerate(lines):
        col = "#D63031" if ln.startswith("!") else "#1E1B2E"
        text(f"{name}_l{i}", ln.lstrip("!"), col, lsize, (0, -0.06, z0 + h - 0.55 - i * lsize * 1.35), g)
    return g

def arrow(name, loc, length=1.2, color="#F5C518", parent=None, rotz=0.0):
    g = empty(name, loc, parent, (0, 0, rotz))
    box(name + "_s", color, (length, 0.18, 0.12), (length / 2, 0, 0), g, bevel=0.03)
    o = cyl(name + "_h", color, 0.28, 0.12, (length + 0.15, 0, 0), g, verts=3)
    o.rotation_euler = (0, 0, 0)
    return g

def house(name, loc, color="#F2C46B", roof="#C0392B", parent=None):
    g = empty(name, loc, parent)
    box(name + "_w", color, (6, 0.4, 3.2), (0, 0, 1.6), g, bevel=0.03)
    box(name + "_r", roof, (6.4, 0.7, 0.35), (0, -0.1, 3.3), g, bevel=0.05)
    box(name + "_door", "#7A4B2E", (1.0, 0.1, 2.0), (-1.2, -0.22, 1.0), g, bevel=0.03)
    for x in (0.8, 2.3):
        box(f"{name}_win{x}", "#EDEDED", (1.1, 0.1, 1.0), (x, -0.22, 1.8), g, bevel=0.03)
        box(f"{name}_wg{x}", "#9AD3F0", (0.95, 0.12, 0.85), (x, -0.23, 1.8), g, bevel=0.02)
    return g

def city(name, y=14, n=9, seed=3, parent=None, sky=None):
    import random
    rnd = random.Random(seed); g = empty(name, (0, y, 0), parent)
    x = -14
    cols = ["#C9CDD6", "#B8C2CF", "#D8CFC4", "#AEB7C2", "#CFC6D8"]
    while x < 14:
        w = rnd.uniform(1.8, 3.2); hgt = rnd.uniform(4, 10); c = rnd.choice(cols); yb = rnd.uniform(0, 2)
        box(f"{name}_{x:.1f}", c, (w, 1.5, hgt), (x + w / 2, yb, hgt / 2), g, bevel=0.03)
        nk = int((w - 0.3) / 0.7)
        for r in range(int((hgt - 0.6) / 1.1)):
            for k in range(nk):
                box(f"{name}_{x:.1f}_{r}_{k}", "#F7E08A", (0.32, 0.05, 0.42),
                    (x + w / 2 + (k - (nk - 1) / 2) * 0.7, yb - 0.76, 0.9 + r * 1.1), g, bevel=0.0)
        x += w + rnd.uniform(0.1, 0.6)
    return g

def car(name, loc, color="#D62828", parent=None, rotz=0.0):
    g = empty(name, loc, parent, (0, 0, rotz))
    box(name + "_b", color, (3.4, 1.5, 0.6), (0, 0, 0.6), g, bevel=0.15)
    box(name + "_t", color, (1.7, 1.3, 0.5), (-0.2, 0, 1.1), g, bevel=0.15)
    box(name + "_gl", "#2B3A4A", (1.5, 1.32, 0.38), (-0.2, 0, 1.12), g, bevel=0.1)
    for x in (-1.1, 1.1):
        for y in (-0.75, 0.75):
            cyl(f"{name}_wh{x}{y}", "#1E1E24", 0.36, 0.28, (x, y, 0.36), g, rot=(math.pi / 2, 0, 0))
            cyl(f"{name}_rim{x}{y}", "#BDC3C7", 0.18, 0.3, (x, y, 0.36), g, rot=(math.pi / 2, 0, 0))
    box(name + "_lt", "#FFF3B0", (0.06, 0.3, 0.14), (1.71, -0.45, 0.72), g, bevel=0.02)
    box(name + "_lt2", "#FFF3B0", (0.06, 0.3, 0.14), (1.71, 0.45, 0.72), g, bevel=0.02)
    return g

def phone(name, loc, parent=None, rot=(0, 0, 0), screen="#5DADE2"):
    g = empty(name, loc, parent, rot)
    box(name + "_b", "#1E1E24", (0.34, 0.05, 0.62), (0, 0, 0), g, bevel=0.03)
    box(name + "_s", screen, (0.29, 0.055, 0.52), (0, -0.002, 0.01), g, bevel=0.01)
    return g

def laptop(name, loc, parent=None, screen="#ECF0F1"):
    g = empty(name, loc, parent)
    box(name + "_base", "#95A5A6", (1.6, 1.1, 0.08), (0, 0, 0.04), g, bevel=0.02)
    lid = empty(name + "_lid", (0, 0.52, 0.08), g, (-0.25, 0, 0))
    box(name + "_lidm", "#7F8C8D", (1.6, 0.06, 1.05), (0, 0, 0.52), lid, bevel=0.03)
    box(name + "_scr", screen, (1.45, 0.07, 0.9), (0, -0.01, 0.53), lid, bevel=0.01)
    return g, lid

def table(name, loc, w=2.4, d=1.0, h=0.9, color="#8B5E3C", parent=None):
    g = empty(name, loc, parent)
    box(name + "_top", color, (w, d, 0.1), (0, 0, h), g, bevel=0.03)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{name}_l{sx}{sy}", _shade(color, 0.8), (0.1, 0.1, h), (sx * (w / 2 - 0.1), sy * (d / 2 - 0.1), h / 2), g, bevel=0.01)
    return g

def book(name, loc, parent=None, color="#8E44AD"):
    g = empty(name, loc, parent)
    box(name + "_c", color, (0.6, 0.18, 0.8), (0, 0, 0.4), g, bevel=0.03)
    box(name + "_p", "#FDFEFE", (0.54, 0.16, 0.74), (0.04, 0.02, 0.4), g, bevel=0.02)
    return g

def ostrich(name, loc, parent=None, rotz=0.0):
    g = empty(name, loc, parent, (0, 0, rotz))
    for sx in (-1, 1):
        box(f"{name}_leg{sx}", "#E8B48A", (0.07, 0.07, 0.9), (sx * 0.15, 0, 0.45), g, bevel=0.02)
        box(f"{name}_ft{sx}", "#E8B48A", (0.12, 0.2, 0.05), (sx * 0.15, -0.06, 0.03), g, bevel=0.02)
    box(name + "_body", "#2C2C2C", (0.7, 1.0, 0.6), (0, 0.05, 1.15), g, bevel=0.2)
    box(name + "_tail", "#F4F4F4", (0.5, 0.25, 0.3), (0, 0.6, 1.3), g, bevel=0.1)
    box(name + "_neck", "#E8B48A", (0.1, 0.1, 0.9), (0, -0.38, 1.75), g, bevel=0.04)
    box(name + "_head", "#E8B48A", (0.2, 0.26, 0.18), (0, -0.44, 2.22), g, bevel=0.06)
    box(name + "_beak", "#F0A040", (0.12, 0.18, 0.06), (0, -0.62, 2.2), g, bevel=0.02)
    for sx in (-1, 1): box(f"{name}_eye{sx}", "#111111", (0.03, 0.05, 0.05), (sx * 0.1, -0.5, 2.26), g, bevel=0.01)
    return g

def globe(name, loc, r=1.0, parent=None):
    g = empty(name, loc, parent)
    sphere(name + "_sea", "#3E8EDE", r, (0, 0, 0), g)
    import random
    rnd = random.Random(7)
    for i in range(26):
        th, ph = rnd.uniform(0, 2 * math.pi), rnd.uniform(-1.1, 1.1)
        p = Vector((math.cos(ph) * math.cos(th), math.cos(ph) * math.sin(th), math.sin(ph))) * r * 0.97
        s = rnd.uniform(0.25, 0.5) * r
        o = box(f"{name}_land{i}", "#5DBB63", (s, s * 0.8, 0.12 * r), tuple(p), g, bevel=0.03)
        o.rotation_euler = Vector((0, 0, 1)).rotation_difference(p.normalized()).to_euler()
    return g

def confetti(name, n=120, area=(6, 4, 9), seed=1, parent=None):
    import random
    rnd = random.Random(seed); g = empty(name, (0, 0, 0), parent); items = []
    cols = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#FFFFFF", "#E67E22"]
    for i in range(n):
        o = box(f"{name}_{i}", rnd.choice(cols), (0.09, 0.02, 0.14), (0, 0, 0), g, bevel=0)
        items.append((o, rnd.uniform(-area[0], area[0]), rnd.uniform(-area[1], area[1]), rnd.uniform(0, area[2]),
                      rnd.uniform(0.6, 1.4), rnd.uniform(0, 6)))
    def anim(t, t0):
        for o, x, y, z, sp, ph in items:
            k = max(0, t - t0)
            o.location = (x + math.sin(k * 2 + ph) * 0.3, y, area[2] + z - k * 2.4 * sp)
            o.rotation_euler = (k * 4 * sp + ph, k * 3 + ph, ph)
            o.hide_render = t < t0
    return g, anim

def money_rain(name, n=40, area=(5, 3, 8), seed=2, parent=None, s=0.8):
    import random
    rnd = random.Random(seed); g = empty(name, (0, 0, 0), parent); items = []
    for i in range(n):
        o = bill(f"{name}_{i}", s=s, parent=g)
        items.append((o, rnd.uniform(-area[0], area[0]), rnd.uniform(-area[1], area[1]), rnd.uniform(0, area[2]),
                      rnd.uniform(0.7, 1.3), rnd.uniform(0, 6)))
    def anim(t, t0, up=False):
        for o, x, y, z, sp, ph in items:
            k = max(0, t - t0)
            zz = (z + k * 3 * sp) if up else (area[2] + z - k * 2.2 * sp)
            o.location = (x + math.sin(k * 1.5 + ph) * 0.4, y, zz)
            o.rotation_euler = (k * 2 * sp + ph, k * 1.4 + ph, ph)
            show(o, t >= t0)
    return g, anim

# ------------------------------------------------------------------ projeção (etiquetas que seguem objetos)
def project(obj_name, scene=None):
    from bpy_extras.object_utils import world_to_camera_view
    s = scene or bpy.context.scene
    o = bpy.data.objects.get(obj_name)
    if o is None: return None
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    p = world_to_camera_view(s, s.camera, o.matrix_world.translation)
    return (round(p.x, 4), round(1 - p.y, 4), round(p.z, 3))
