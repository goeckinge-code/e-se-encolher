"""Capacete de Ayrton Senna em Blender (bpy), exportado como malha leve para o site.

Uso (Blender como módulo Python 3.11, ou `blender -b -P capacete.py --`):
    python capacete.py SAIDA_DIR [--render]
Gera SAIDA_DIR/capacete3d.bin (+ .json com o layout) e, com --render, uma prévia em Cycles.

Modelo: casco alongado com queixeira (capacete fechado), abertura da viseira recortada,
viseira separada um pouco maior que o casco, aro do pescoço. A pintura vem em cores por
vértice: amarelo, faixa verde e faixa azul contornando a viseira, como no capacete real.
Eixos de exportação (three.js): y para cima, z para a frente, x para a direita.
"""
import json, math, os, sys
import bpy, bmesh
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
OUT = args[0] if args else "."
RENDER = "--render" in args
os.makedirs(OUT, exist_ok=True)

YELLOW = (0.96, 0.76, 0.02)
GREEN = (0.02, 0.48, 0.20)
BLUE = (0.05, 0.16, 0.48)
WHITE = (0.95, 0.95, 0.93)
NAVY = (0.03, 0.05, 0.14)
VISOR = (0.05, 0.06, 0.07)

bpy.ops.wm.read_factory_settings(use_empty=True)


def shell_shape(v):
    """Esfera -> casco: alonga para a frente/trás, achata dos lados e desce a queixeira."""
    x, y, z = v.x, v.y, v.z
    f = -y  # f = frente
    x *= 0.9
    f *= 1.06 if f > 0 else 1.14
    z *= 1.02
    if z < 0:  # parte de baixo: a frente desce e avança (queixeira); a nuca abre um pouco
        k = max(0.0, f) ** 1.2
        f += 0.24 * k * (-z)
        z *= 1.0 + 0.20 * k
        x *= 1.0 + 0.05 * (-z) * (1.0 - k)
    return Vector((x, -f, z))


def sphere(name, radius, seg=(120, 88)):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg[0], v_segments=seg[1], radius=radius)
    for v in bm.verts:
        v.co = shell_shape(v.co)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def rounded_box(name, w, h, r, depth, z0, f0):
    """Cortador da viseira: retângulo arredondado (largura w, altura h) extrudado para a frente."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    pts = []
    for cx, cz, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(13):
            a = math.radians(a0 + k * 7.5)
            pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    back = [bm.verts.new((x, -f0, z + z0)) for x, z in pts]
    front = [bm.verts.new((x, -(f0 + depth), z + z0)) for x, z in pts]
    n = len(pts)
    for i in range(n):
        bm.faces.new((back[i], back[(i + 1) % n], front[(i + 1) % n], front[i]))
    bm.faces.new(back[::-1])
    bm.faces.new(front)
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def neck_cutter():
    """Cubo inclinado: o corte da base fica mais baixo na frente (queixo) e mais alto na nuca."""
    me = bpy.data.meshes.new("pescoco")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=4.0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("pescoco", me)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(22), 0, 0)
    ob.location = (0, 0, -0.66 - 2.0 / math.cos(math.radians(22)))
    return ob


def apply_all(ob):
    bpy.context.view_layer.objects.active = ob
    for m in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


def boolean(ob, cutter, op):
    m = ob.modifiers.new("b", "BOOLEAN")
    m.operation = op
    m.object = cutter
    m.solver = "EXACT"


cut_v = rounded_box("corte_viseira", 1.46, 0.52, 0.2, 3.0, -0.12, 0.15)
cut_n = neck_cutter()

shell = sphere("casco", 1.0)
sol = shell.modifiers.new("s", "SOLIDIFY")
sol.thickness = 0.05
sol.offset = -1
boolean(shell, cut_v, "DIFFERENCE")
boolean(shell, cut_n, "DIFFERENCE")
apply_all(shell)

visor = sphere("viseira", 1.028)
cut_v2 = rounded_box("corte_viseira2", 1.50, 0.56, 0.22, 3.0, -0.12, 0.15)
sol2 = visor.modifiers.new("s", "SOLIDIFY")
sol2.thickness = 0.012
boolean(visor, cut_v2, "INTERSECT")
apply_all(visor)

for ob in (cut_v, cut_v2, cut_n):
    bpy.data.objects.remove(ob)
for ob in (shell, visor):
    for p in ob.data.polygons:
        p.use_smooth = True


def livery(x, f, z):
    """Mesma pintura do shader do site (para a prévia do Blender)."""
    ang = math.atan2(x, f)
    side = min(1.0, abs(ang) / 1.25)
    top = 0.14 - 0.05 * side ** 2
    front = f > 0.2 and abs(ang) < 1.05
    if front and top - 0.005 < z < top + 0.05:
        return NAVY
    if top + 0.05 < z < top + 0.07 or top + 0.15 < z < top + 0.17:
        return WHITE
    if top + 0.07 <= z <= top + 0.15:
        return GREEN
    if not front and top - 0.12 <= z <= top - 0.02:
        return BLUE
    return YELLOW


def paint(ob, fn):
    me = ob.data
    col = me.color_attributes.new("cor", "FLOAT_COLOR", "POINT")
    for i, v in enumerate(me.vertices):
        c = fn(v.co.x, -v.co.y, v.co.z)
        col.data[i].color = (*[cc ** 2.2 for cc in c], 1.0)


paint(shell, livery)
paint(visor, lambda *a: VISOR)


def export(obs, path):
    """Malha triangulada: Float32 (posição, normal) + Uint16 (índices), eixos do three.js.
    A pintura é calculada no shader do site a partir da posição, então não vai cor."""
    import struct
    parts, blob = [], bytearray()
    for ob in obs:
        dg = bpy.context.evaluated_depsgraph_get()
        me = ob.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        P, N = [], []
        for v in me.vertices:
            P += [v.co.x, v.co.z, -v.co.y]
            N += [v.normal.x, v.normal.z, -v.normal.y]
        I = [i for t in me.loop_triangles for i in t.vertices]
        part = {"name": ob.name, "count": len(me.vertices), "index": len(I)}
        assert len(me.vertices) < 65536
        for key, arr, fmt in (("pos", P, "f"), ("nor", N, "f"), ("idx", I, "H")):
            while len(blob) % 4:
                blob.append(0)
            part[key] = len(blob)
            blob += struct.pack(f"<{len(arr)}{fmt}", *arr)
        parts.append(part)
    open(path + ".bin", "wb").write(blob)
    json.dump({"parts": parts}, open(path + ".json", "w"))
    print("export", path, len(blob) // 1024, "KB", [(p["name"], p["count"]) for p in parts])


export([shell, visor], os.path.join(OUT, "capacete3d"))

if RENDER:
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 24
    sc.cycles.device = "CPU"
    sc.render.resolution_x = sc.render.resolution_y = 640
    for ob, rough, metal in ((shell, 0.18, 0.0), (visor, 0.05, 0.6)):
        m = bpy.data.materials.new(ob.name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        a = m.node_tree.nodes.new("ShaderNodeVertexColor")
        a.layer_name = "cor"
        m.node_tree.links.new(a.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
        ob.data.materials.append(m)
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.88, 0.83, 1)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    for i, (yaw, name) in enumerate(((35, "34"), (90, "lado"), (0, "frente"))):
        r = math.radians(yaw)
        cam.location = (4.6 * math.sin(r), -4.6 * math.cos(r), 0.5)
        cam.rotation_euler = (math.radians(84), 0, r)
        L = bpy.data.objects.get("sol") or bpy.data.objects.new("sol", bpy.data.lights.new("sol", "SUN"))
        if not L.users_collection:
            sc.collection.objects.link(L)
        L.rotation_euler = (math.radians(40), 0, math.radians(30))
        L.data.energy = 3
        sc.render.filepath = os.path.join(OUT, f"previa_{name}.png")
        bpy.ops.render.render(write_still=True)
