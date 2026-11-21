"""Personagens 3D fictícios (corpo de metaballs + esqueleto + roupas + rosto com expressões).

AGENTE: camisa manga longa azul-marinho, colete tático preto "PROTEÇÃO ANIMAL", calça cáqui,
        cinto preto, luvas brancas, sapato preto, cabelo curtinho.
RAPAZ:  sem camisa, bermuda preta estampada, descalço, cabelo cacheado curto.

Convenções do esqueleto (personagem olhando para -Y, lado L = +X):
  braço/perna: fwd = levanta pra frente, out = abre pro lado, tw = gira no eixo do osso
  antebraço/canela: bend = dobra (cotovelo pra frente / joelho pra trás)
  coluna/cabeça: fwd = inclina pra frente, tw = gira (olha pros lados), side = inclina pro lado
"""
import bpy, math, bmesh
from mathutils import Vector, Matrix, Quaternion
import numpy as np
import mat as M

D = math.radians
MB_K = 0.574          # raio da superfície / raio da metaball (limiar 0.6, rigidez 2)

# ----------------------------------------------------------------- esqueleto
def joints(H, bulk):
    s = H/1.75
    J = {
        "pelvis": ((0, 0, .95), (0, 0, 1.05)),
        "spine": ((0, 0, 1.05), (0, 0, 1.25)),
        "chest": ((0, 0, 1.25), (0, .005, 1.46)),
        "neck": ((0, .005, 1.45), (0, -.005, 1.535)),
        "head": ((0, -.005, 1.535), (0, -.005, 1.75)),
    }
    sh = .175 + .012*bulk
    for sd, sx in (("L", 1), ("R", -1)):
        J["shoulder."+sd] = ((sx*.03, 0, 1.425), (sx*sh, .01, 1.44))
        J["upperarm."+sd] = ((sx*sh, .01, 1.44), (sx*(sh+.06), .025, 1.13))
        J["forearm."+sd] = ((sx*(sh+.06), .025, 1.13), (sx*(sh+.09), -.01, .87))
        J["hand."+sd] = ((sx*(sh+.09), -.01, .87), (sx*(sh+.095), -.015, .72))
        J["thigh."+sd] = ((sx*.095, 0, .93), (sx*.10, -.01, .51))
        J["shin."+sd] = ((sx*.10, -.01, .51), (sx*.10, .025, .085))
        J["foot."+sd] = ((sx*.10, .025, .085), (sx*.10, -.13, .025))
    return {k: (Vector(a)*s, Vector(b)*s) for k, (a, b) in J.items()}

PARENT = {"spine": "pelvis", "chest": "spine", "neck": "chest", "head": "neck"}
for _s in "LR":
    PARENT.update({f"shoulder.{_s}": "chest", f"upperarm.{_s}": f"shoulder.{_s}", f"forearm.{_s}": f"upperarm.{_s}",
                   f"hand.{_s}": f"forearm.{_s}", f"thigh.{_s}": "pelvis", f"shin.{_s}": f"thigh.{_s}",
                   f"foot.{_s}": f"shin.{_s}"})

def make_armature(name, J):
    arm = bpy.data.armatures.new(name); ob = bpy.data.objects.new(name, arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    for bn, (h, t) in J.items():
        eb = arm.edit_bones.new(bn); eb.head, eb.tail = h, t
        y = (t - h).normalized()
        if bn.startswith("shoulder"):
            eb.align_roll(Vector((0, 0, 1)))
        else:
            z = Vector((1, 0, 0)).cross(y)
            eb.align_roll(z.normalized())
    for bn, p in PARENT.items():
        arm.edit_bones[bn].parent = arm.edit_bones[p]
        arm.edit_bones[bn].use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in ob.pose.bones: pb.rotation_mode = 'XYZ'
    return ob

# ----------------------------------------------------------------- corpo (metaballs)
def _mb_object(name, elems, res=0.012):
    mb = bpy.data.metaballs.new(name); mb.threshold = 0.6; mb.resolution = res; mb.render_resolution = res
    for e in elems:
        kind = e[0]
        if kind == "ball":
            _, c, r = e; el = mb.elements.new(type='BALL'); el.co = c; el.radius = r/MB_K
        elif kind == "ell":
            _, c, sz = e; el = mb.elements.new(type='ELLIPSOID'); el.co = c
            r = max(sz); el.radius = r/MB_K; el.size_x, el.size_y, el.size_z = sz[0]/r, sz[1]/r, sz[2]/r
        elif kind == "cap":
            _, a, b, r = e; a, b = Vector(a), Vector(b); d = b - a
            el = mb.elements.new(type='CAPSULE'); el.co = (a+b)/2; el.radius = r/MB_K; el.size_x = d.length/2
            el.rotation = d.normalized().to_track_quat('X', 'Z')
        el.stiffness = 2.0
    ob = bpy.data.objects.new(name, mb); bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bpy.data.objects.remove(ob); bpy.data.metaballs.remove(mb)
    mo = bpy.data.objects.new(name + "_m", me); bpy.context.scene.collection.objects.link(mo)
    for p in me.polygons: p.use_smooth = True
    return mo

def _limb_caps(a, b, r0, r1, n=3):
    out = []
    for i in range(n):
        p0 = a.lerp(b, i/n); p1 = a.lerp(b, (i+1)/n)
        out.append(("cap", p0, p1, r0 + (r1-r0)*(i+.5)/n))
    return out

def body_parts(J, H, bulk, belly):
    s = H/1.75
    v = lambda x, y, z: Vector((x, y, z))*s
    w = 1 + .1*bulk
    torso = [
        ("ell", v(0, .005, .96), (.155*w, .105*w, .11)),                # quadril
        ("ell", v(0, -.004 - .02*belly, 1.10), (.135*w, (.095+.03*belly)*w, .11)),  # barriga
        ("ell", v(0, .0, 1.30), (.165*w, .105*w, .14)),                 # peito
        ("ell", v(0, -.022, 1.33), (.13*w, .06*w, .07)),                # peitoral
        ("cap", v(-.16*w, .01, 1.415), v(.16*w, .01, 1.415), .062*w),    # ombros
        ("cap", v(0, .005, 1.40), v(0, -.004, 1.56), .05),               # pescoço
        ("ell", v(.085, .0, .89), (.075*w, .085*w, .08)), ("ell", v(-.085, .0, .89), (.075*w, .085*w, .08)),
        ("ell", v(0, .05, .93), (.13*w, .07, .09)),                     # bumbum
    ]
    parts = {"torso": torso}
    for sd in "LR":
        ua, fa, ha = J["upperarm."+sd], J["forearm."+sd], J["hand."+sd]
        parts["arm."+sd] = [("cap", ua[0], ua[1].lerp(ua[0], .05), .043*w*s), ("cap", fa[0], fa[1], .034*w*s),
                            ("ball", ua[0] + v(0, 0, -.02), .05*w*s), ("ball", fa[1].lerp(fa[0], .2), .03*s)]
        th, sh = J["thigh."+sd], J["shin."+sd]
        parts["leg."+sd] = [("cap", th[0] + v(0, 0, .02), th[0].lerp(th[1], .55), .072*w*s),
                            ("cap", th[0].lerp(th[1], .5), th[1], .057*w*s),
                            ("cap", sh[0], sh[0].lerp(sh[1], .5), .048*w*s),
                            ("cap", sh[0].lerp(sh[1], .5), sh[1], .036*s)]
    return parts

def _seg_dist(P, a, b):
    ab = b - a; t = np.clip(((P - a) @ ab)/(ab @ ab), 0, 1)
    return np.linalg.norm(P - (a + t[:, None]*ab), axis=1)

ALLOW = {
    "torso": ["pelvis", "spine", "chest", "neck", "shoulder.L", "shoulder.R", "thigh.L", "thigh.R", "head"],
    "arm.L": ["upperarm.L", "forearm.L", "shoulder.L", "hand.L"],
    "arm.R": ["upperarm.R", "forearm.R", "shoulder.R", "hand.R"],
    "leg.L": ["thigh.L", "shin.L", "pelvis", "foot.L"],
    "leg.R": ["thigh.R", "shin.R", "pelvis", "foot.R"],
}
BONE_R = {"pelvis": .13, "spine": .12, "chest": .14, "neck": .05, "head": .09, "shoulder.L": .07, "shoulder.R": .07,
          "upperarm.L": .045, "upperarm.R": .045, "forearm.L": .035, "forearm.R": .035, "hand.L": .03, "hand.R": .03,
          "thigh.L": .07, "thigh.R": .07, "shin.L": .045, "shin.R": .045, "foot.L": .04, "foot.R": .04}

def skin_weights(ob, J, allowed, H):
    s = H/1.75
    P = np.array([v.co[:] for v in ob.data.vertices])
    ds = []
    for bn in allowed:
        a, b = np.array(J[bn][0][:]), np.array(J[bn][1][:])
        d = _seg_dist(P, a, b) - BONE_R[bn]*s*.8
        if bn == "head": d[P[:, 2] < 1.565*s] = 9
        if bn.startswith("thigh") and "torso" in ob.name: d = d + .03*s
        if bn == "pelvis" and "leg" in ob.name: d[P[:, 2] < .86*s] = 9
        if bn.startswith("hand"): d[np.linalg.norm(P - np.array(J[bn][0][:]), axis=1) > .05*s] = 9
        if bn.startswith("foot"): d[P[:, 2] > .12*s] = 9
        ds.append(np.maximum(d, .002))
    ds = np.array(ds)
    w = 1/ds**5; w /= w.sum(0)
    for i, bn in enumerate(allowed):
        vg = ob.vertex_groups.new(name=bn)
        idx = np.nonzero(w[i] > .01)[0]
        for j in idx: vg.add([int(j)], float(w[i][j]), 'REPLACE')

def bind(ob, arm):
    ob.parent = arm
    m = ob.modifiers.new("arm", 'ARMATURE'); m.object = arm

def bone_parent(ob, arm, bone):
    """Prende um objeto rígido a um osso mantendo a posição de repouso."""
    ob.parent = arm; ob.parent_type = 'BONE'; ob.parent_bone = bone
    pb = arm.pose.bones[bone]
    # matriz do osso em repouso (cauda), o objeto foi criado em coords do mundo/armature
    bm = arm.data.bones[bone].matrix_local
    tail = Matrix.Translation(arm.data.bones[bone].tail_local - arm.data.bones[bone].head_local)
    ob.matrix_parent_inverse = (Matrix.Translation(arm.data.bones[bone].tail_local) @ bm.to_3x3().to_4x4()).inverted()

def setm(ob, m):
    ob.data.materials.clear(); ob.data.materials.append(m); return ob

def assign_by(ob, mats, fn):
    """fn(center_world_rest) -> índice do material"""
    ob.data.materials.clear()
    for m in mats: ob.data.materials.append(m)
    for p in ob.data.polygons: p.material_index = fn(p.center)

def shell(src, name, keep, off, mat_, solid=0.0):
    """Roupa folgada: cópia da região do corpo deslocada pela normal (herda os pesos)."""
    me = src.data.copy(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for vg in src.vertex_groups: ob.vertex_groups.new(name=vg.name)
    # copia pesos
    for v in me.vertices: pass
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(f.calc_center_median())], context='FACES')
    bm.to_mesh(me); bm.free()
    setm(ob, mat_)
    d = ob.modifiers.new("off", 'DISPLACE'); d.strength = off; d.mid_level = 0; d.direction = 'NORMAL'
    if solid:
        so = ob.modifiers.new("sol", 'SOLIDIFY'); so.thickness = solid; so.offset = -1
    return ob

def mesh_obj(name, verts, faces, mat_=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    if mat_: setm(ob, mat_)
    return ob

def prim(kind, name, mat_, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), sub=1, **kw):
    if kind == "sphere": bpy.ops.mesh.primitive_uv_sphere_add(segments=kw.get("seg", 24), ring_count=kw.get("rings", 12), radius=1)
    elif kind == "ico": bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=kw.get("subd", 2), radius=1)
    elif kind == "cube": bpy.ops.mesh.primitive_cube_add(size=2)
    elif kind == "cyl": bpy.ops.mesh.primitive_cylinder_add(vertices=kw.get("verts", 24), radius=1, depth=2)
    elif kind == "torus": bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=kw.get("minor", .1), major_segments=kw.get("maj", 32), minor_segments=8)
    ob = bpy.context.object; ob.name = name
    ob.location, ob.scale, ob.rotation_euler = loc, scale, rot
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for p in ob.data.polygons: p.use_smooth = True
    if sub:
        m = ob.modifiers.new("s", 'SUBSURF'); m.levels = sub; m.render_levels = sub
    if mat_: setm(ob, mat_)
    return ob

# ----------------------------------------------------------------- cabeça e rosto
def build_head(P, spec):
    """Cabeça em coordenadas do mundo (repouso). Retorna dict de partes do rosto."""
    s = spec["H"]/1.75
    hc = Vector((0, -.012, 1.64))*s     # centro da cabeça
    skin = P["skin"]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=1)
    hd = bpy.context.object; hd.name = spec["name"] + "_cabeca"
    for vtx in hd.data.vertices:
        x, y, z = vtx.co
        # crânio: largura 15cm, profundidade 19cm, altura 23cm
        sx, sy, sz = .074, .098, .108
        if z < 0:                          # mandíbula estreita até o queixo
            k = min(1, -z)
            x *= 1 - .30*k**1.6
            y *= 1 - .18*k
            if y < 0: y *= 1 - .05*k
        if y < 0:                          # rosto mais plano
            y *= .86 + .1*abs(z)
        if y > 0 and z < -.2:              # nuca
            y *= .85
        if y < -.5 and -.05 < z < .35:     # testa/sobrancelha
            y -= .03*max(0, 1-abs(z-.15)/.2)
        if y < -.4 and -.45 < z < -.1:     # bochechas
            x *= 1.03
        vtx.co = (x*sx*spec.get("headw", 1), y*sy, z*sz)
    hd.location = hc
    bpy.ops.object.transform_apply(location=True)
    for p in hd.data.polygons: p.use_smooth = True
    m = hd.modifiers.new("s", 'SUBSURF'); m.levels = 1; m.render_levels = 1
    setm(hd, skin)
    F = {"head": hd}
    fy = hc.y - .081*s               # plano do rosto
    # nariz
    nz = hc.z - .02*s
    nose = prim("sphere", spec["name"]+"_nariz", skin, loc=(0, fy - .012*s, nz), scale=(.012*spec.get("nosew", 1)*s, .016*s, .026*s), seg=16, rings=10)
    for vtx in nose.data.vertices:
        if vtx.co.z > nz:             # ponte fina
            k = (vtx.co.z - nz)/(.03*s); vtx.co.x *= 1 - .55*k
        if vtx.co.y < fy - .012*s: vtx.co.y -= .004*s
    tip = prim("sphere", spec["name"]+"_narina", skin, loc=(0, fy - .016*s, nz - .02*s), scale=(.017*spec.get("nosew", 1)*s, .01*s, .009*s), seg=16, rings=8)
    F["nose"] = [nose, tip]
    # olhos
    eye_w = P["eye"]
    F["eyes"], F["lids"], F["brows"] = [], [], []
    for sd, sx in (("L", 1), ("R", -1)):
        ec = Vector((sx*.031*s, fy + .010*s, hc.z + .022*s))
        eb = prim("sphere", f"{spec['name']}_olho.{sd}", eye_w, loc=ec, scale=(.0125*s,)*3, sub=0, seg=24, rings=16)
        iris = prim("sphere", f"{spec['name']}_iris.{sd}", P["iris"], loc=ec + Vector((0, -.0105*s, 0)), scale=(.0062*s, .0028*s, .0062*s), sub=0, seg=16, rings=8)
        pup = prim("sphere", f"{spec['name']}_pupila.{sd}", P["pupil"], loc=ec + Vector((0, -.0122*s, 0)), scale=(.003*s, .0015*s, .003*s), sub=0, seg=12, rings=6)
        F["eyes"] += [eb, iris, pup]
        # pálpebras: casca de esfera (metade de cima), girada para abrir/fechar
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=.0138*s)
        lid = bpy.context.object; lid.name = f"{spec['name']}_palpebra.{sd}"
        bm = bmesh.new(); bm.from_mesh(lid.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -.001*s], context='VERTS'); bm.to_mesh(lid.data); bm.free()
        so = lid.modifiers.new("so", 'SOLIDIFY'); so.thickness = .0015*s
        for p in lid.data.polygons: p.use_smooth = True
        lid.location = ec; setm(lid, skin)
        lid.rotation_mode = 'XYZ'
        F["lids"].append(lid)
        # sobrancelha
        br = prim("cyl", f"{spec['name']}_sobrancelha.{sd}", P["hair"], loc=(0, 0, 0), scale=(.0045*s, .0045*s, .017*s), rot=(0, D(90), 0), verts=10)
        br.location = ec + Vector((sx*.002*s, -.006*s, .021*s))
        br.rotation_euler = (0, 0, 0)
        br.rotation_mode = 'XYZ'
        F["brows"].append(br)
        # orelha
        prim("sphere", f"{spec['name']}_orelha.{sd}", skin, loc=(sx*.073*s, hc.y + .008*s, hc.z + .005*s), scale=(.012*s, .02*s, .032*s), rot=(D(-8), 0, sx*D(-12)), seg=16, rings=10)
    # boca: cavidade escura + lábios
    mz = hc.z - .055*s
    F["mouth_c"] = Vector((0, fy - .004*s, mz))
    cav = prim("sphere", spec["name"]+"_boca", P["mouthin"], loc=(0, 0, 0), scale=(.021*s, .008*s, .006*s), seg=20, rings=10, sub=0)
    cav.location = F["mouth_c"]
    teeth = prim("cube", spec["name"]+"_dentes", P["teeth"], loc=(0, 0, 0), scale=(.016*s, .004*s, .0035*s), sub=1)
    teeth.location = F["mouth_c"] + Vector((0, .0015*s, .0035*s))
    lu = prim("cyl", spec["name"]+"_labio_sup", P["lip"], loc=(0, 0, 0), scale=(.0026*s, .0026*s, .02*s), rot=(0, D(90), 0), verts=12)
    ll = prim("cyl", spec["name"]+"_labio_inf", P["lip"], loc=(0, 0, 0), scale=(.0032*s, .0032*s, .018*s), rot=(0, D(90), 0), verts=12)
    lu.location = F["mouth_c"] + Vector((0, -.001*s, .003*s)); ll.location = F["mouth_c"] + Vector((0, -.001*s, -.0035*s))
    F["mouth"] = {"cav": cav, "teeth": teeth, "lu": lu, "ll": ll}
    # queixo/mandíbula: a parte de baixo do rosto desce com a boca aberta — usamos um "queixo" separado
    chin = prim("sphere", spec["name"]+"_queixo", skin, loc=(0, fy + .02*s, hc.z - .088*s), scale=(.024*s, .014*s, .012*s), seg=16, rings=10)
    F["chin"] = chin
    chin.hide_render = True
    F["rest"] = {o.name: o.location.copy() for o in [lu, ll, cav, teeth, chin] + F["brows"]}
    F["hc"] = hc; F["s"] = s
    return F

def hair_cap(P, spec, F, style):
    s = F["s"]; hc = F["hc"]
    hd = F["head"]
    me = hd.data.copy(); cap = bpy.data.objects.new(spec["name"]+"_cabelo", me); bpy.context.scene.collection.objects.link(cap)
    bm = bmesh.new(); bm.from_mesh(me)
    def keep(c):
        rel = c - hc
        if rel.z < -.005*s: return False
        if rel.y < -.05*s and rel.z < .055*s: return False      # linha do cabelo na testa
        if abs(rel.x) > .06*s and rel.z < .02*s and rel.y < .03*s: return False   # costeleta
        return True
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(f.calc_center_median())], context='FACES')
    bm.to_mesh(me); bm.free()
    cap.modifiers.clear()
    d = cap.modifiers.new("d", 'DISPLACE'); d.direction = 'NORMAL'; d.mid_level = 0
    d.strength = .0025*s if style == "curto" else .006*s
    sm = cap.modifiers.new("s", 'SUBSURF'); sm.levels = 1; sm.render_levels = 1
    setm(cap, P["hair"])
    parts = [cap]
    if style == "cacheado":
        # cachos: muitas bolinhas espalhadas na calota (cabelo curto-médio, nada de black power)
        rng = np.random.default_rng(7)
        verts = [v.co.copy() for v in me.vertices]
        pts = [verts[i] for i in rng.choice(len(verts), min(420, len(verts)), replace=False)]
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1)
        proto = bpy.context.object
        bm2 = bmesh.new()
        for p in pts:
            n = (p - hc).normalized()
            r = (.009 + .004*rng.random())*s
            c = p + n*(.004*s + .006*s*rng.random())
            mtx = Matrix.Translation(c) @ Matrix.Diagonal((r, r, r*1.3, 1))
            tmp = bmesh.new(); tmp.from_mesh(proto.data); tmp.transform(mtx)
            tmp_me = bpy.data.meshes.new("t"); tmp.to_mesh(tmp_me); tmp.free(); bm2.from_mesh(tmp_me); bpy.data.meshes.remove(tmp_me)
        bpy.data.objects.remove(proto)
        me2 = bpy.data.meshes.new(spec["name"]+"_cachos"); bm2.to_mesh(me2); bm2.free()
        cur = bpy.data.objects.new(spec["name"]+"_cachos", me2); bpy.context.scene.collection.objects.link(cur)
        for p in me2.polygons: p.use_smooth = True
        sm = cur.modifiers.new("s", 'SUBSURF'); sm.levels = 1; sm.render_levels = 1
        setm(cur, P["hair"]); parts.append(cur)
    return parts

# ----------------------------------------------------------------- mãos e pés
def build_hand(P, spec, J, sd, mat_):
    s = spec["H"]/1.75
    h0, h1 = J["hand."+sd]
    sx = 1 if sd == "L" else -1
    d = (h1 - h0).normalized()
    # palma em coords locais simples: depois rotacionamos para o eixo do osso
    objs = []
    palm = prim("cube", f"{spec['name']}_palma.{sd}", mat_, scale=(.012*s, .042*s, .040*s), sub=2)
    palm.location = (0, 0, -.045*s)
    fingers = []
    for i, (off, ln) in enumerate(((-.03, .036), (-.01, .042), (.01, .040), (.029, .032))):
        f = prim("cyl", f"{spec['name']}_dedo{i}.{sd}", mat_, scale=(.0085*s, .0085*s, ln*s/2), verts=10, sub=1)
        # pivô no nó do dedo
        for v in f.data.vertices: v.co.z -= ln*s/2
        f.location = (0, off*s*sx*-1 if False else off*s, -.082*s)
        f.rotation_mode = 'XYZ'
        fingers.append(f)
    th = prim("cyl", f"{spec['name']}_polegar.{sd}", mat_, scale=(.0105*s, .0105*s, .019*s), verts=10, sub=1)
    for v in th.data.vertices: v.co.z -= .019*s
    th.location = (-.004*s, -.03*s, -.035*s); th.rotation_mode = 'XYZ'
    th.rotation_euler = (D(-35), 0, 0)
    root = bpy.data.objects.new(f"{spec['name']}_mao.{sd}", None); bpy.context.scene.collection.objects.link(root)
    for o in [palm, th] + fingers: o.parent = root
    # orientação: Z local da mão ao longo de -d (dedos para baixo), Y local = frente (-Y do mundo) => polegar à frente
    zax = -d; yax = Vector((0, -1, 0)); xax = yax.cross(zax).normalized(); yax = zax.cross(xax).normalized()
    rot = Matrix((xax, yax, zax)).transposed().to_4x4()
    if sd == "R": rot = rot @ Matrix.Scale(-1, 4, Vector((1, 0, 0)))
    root.matrix_world = Matrix.Translation(h0) @ rot
    return {"root": root, "fingers": fingers, "thumb": th, "palm": palm}

def build_foot(P, spec, J, sd, shoe):
    s = spec["H"]/1.75
    a, b = J["foot."+sd]
    if shoe:
        f = prim("cube", f"{spec['name']}_sapato.{sd}", P["shoe"], scale=(.05*s, .135*s, .045*s), sub=2)
        f.location = ((a.x+b.x)/2, (a.y+b.y)/2 - .01*s, .045*s)
        sole = prim("cube", f"{spec['name']}_sola.{sd}", P["sole"], scale=(.052*s, .14*s, .012*s), sub=1)
        sole.location = (f.location.x, f.location.y, .012*s)
        return [f, sole]
    f = prim("sphere", f"{spec['name']}_pe.{sd}", P["skin"], scale=(.045*s, .12*s, .035*s), seg=20, rings=10)
    for v in f.data.vertices:
        if v.co.y > 0: v.co.z *= 1.4               # calcanhar mais alto
        if v.co.z < 0: v.co.z *= .5                 # sola plana
    f.location = ((a.x+b.x)/2, (a.y+b.y)/2 - .015*s, .035*s)
    toes = []
    for i in range(5):
        tx = (a.x + (.02 - .011*i)*s*(1 if sd == "L" else -1))
        t = prim("sphere", f"{spec['name']}_dedopé{i}.{sd}", P["skin"], loc=(tx, b.y - .02*s + .005*i*s, .018*s), scale=(.009*s - .0008*i*s,)*3, seg=10, rings=6, sub=0)
        toes.append(t)
    return [f] + toes

# ----------------------------------------------------------------- colete
def text_obj(name, txt, size, mat_, extrude=.0015):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.space_line = .9
    try:
        cu.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    except Exception: pass
    ob = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(ob)
    setm(ob, mat_); return ob

def build_vest(P, spec, torso, J):
    s = spec["H"]/1.75
    keep = lambda c: 1.02*s < c.z < 1.455*s and not (abs(c.x) > .12*s and c.z > 1.36*s) and not (abs(c.x) < .07*s and c.y < -.02*s and c.z > 1.40*s)
    v = shell(torso, spec["name"]+"_colete", keep, .03*s, P["vest"], solid=.012*s)
    sm = v.modifiers.new("s", 'SUBSURF'); sm.levels = 1; sm.render_levels = 1
    # alças por cima dos ombros
    straps = []
    for sx in (1, -1):
        st = prim("cube", spec["name"]+"_alca", P["vest"], scale=(.035*s, .12*s, .012*s), sub=1)
        st.location = (sx*.085*s, .0, 1.468*s)
        straps.append(st)
    # placa traseira + etiqueta com texto
    back_y = .118*s*(1+.1*spec["bulk"])
    patch = prim("cube", spec["name"]+"_etiqueta", P["patch"], scale=(.11*s, .004*s, .05*s), sub=0)
    patch.location = (0, back_y + .03*s, 1.32*s)
    border = prim("cube", spec["name"]+"_borda", P["white"], scale=(.114*s, .003*s, .054*s), sub=0)
    border.location = (0, back_y + .028*s, 1.32*s)
    t = text_obj(spec["name"]+"_texto", "PROTEÇÃO\nANIMAL", .042*s, P["white"])
    t.location = (0, back_y + .0352*s, 1.32*s); t.rotation_euler = (D(90), 0, D(180))
    # frente: etiqueta pequena sem texto + bolsos
    front = []
    for sx in (1, -1):
        pk = prim("cube", spec["name"]+"_bolso", P["vest"], scale=(.045*s, .012*s, .05*s), sub=0)
        bv = pk.modifiers.new("b", "BEVEL"); bv.width = .006*s; bv.segments = 2
        pk.location = (sx*.07*s, -(back_y - .005*s) - .03*s, 1.12*s)
        front.append(pk)
    fp = prim("cube", spec["name"]+"_etiqueta_frente", P["patch"], scale=(.05*s, .003*s, .022*s), sub=0)
    fp.location = (.0, -(back_y) - .033*s, 1.27*s)
    front.append(fp)
    return [v], straps + [patch, border, t] + front

# ----------------------------------------------------------------- montagem
PALETTE = {
    "agente": dict(skin="#4e3122", shirt="#1b2030", pants="#a48d69", hair="#0b0807"),
    "rapaz": dict(skin="#8d5d3f", hair="#1a110c"),
}

class Pessoa:
    def __init__(self, spec):
        self.spec = spec; name = spec["name"]; H = spec["H"]
        J = joints(H, spec["bulk"]); self.J = J
        P = {
            "skin": M.skin(name+"_pele", spec["skin"]),
            "hair": M.hair(name+"_cab", spec["hair"]),
            "eye": M.plain("olho_branco", "#e9e4dc", .15),
            "iris": M.plain("iris", "#2b1a10", .1),
            "pupil": M.plain("pupila", "#050505", .05),
            "mouthin": M.plain("boca_dentro", "#3a1412", .6),
            "teeth": M.plain("dentes", "#e8e2d2", .3),
            "lip": M.skin(name+"_labio", spec["lip"]),
            "shoe": M.plain("sapato", "#121212", .35),
            "sole": M.plain("sola", "#1e1e1e", .8),
            "vest": M.fabric("colete", "#121318", .9, 120),
            "patch": M.plain("etiqueta", "#0e0e10", .7),
            "white": M.plain("branco", "#e8e8e6", .5),
        }
        self.P = P
        arm = make_armature(name, J); self.arm = arm
        parts = body_parts(J, H, spec["bulk"], spec.get("belly", 0))
        meshes = {}
        for k, elems in parts.items():
            o = _mb_object(f"{name}_{k}", elems, .011*H/1.75)
            skin_weights(o, J, ALLOW[k], H); meshes[k] = o
        self.meshes = meshes
        objs_bind, objs_rigid = list(meshes.values()), []
        if spec["kind"] == "agente":
            shirt = M.fabric("camisa", spec["shirt"], .85, 260); pants = M.fabric("calca", spec["pants"], .9, 300)
            s = H/1.75
            assign_by(meshes["torso"], [shirt, pants, P["skin"]], lambda c: 2 if c.z > 1.50*s else (1 if c.z < 1.0*s else 0))
            for sd in "LR":
                assign_by(meshes["arm."+sd], [shirt, P["skin"]], lambda c: 0)
                assign_by(meshes["leg."+sd], [pants], lambda c: 0)
            # pernas da calça mais folgadas
            for sd in "LR":
                objs_bind.append(shell(meshes["leg."+sd], f"{name}_calca.{sd}", lambda c: c.z > .07*s, .012*s, pants))
            objs_bind.append(shell(meshes["torso"], f"{name}_calca_q", lambda c: .80*s < c.z < 1.0*s, .016*s, pants))
            vb, vr = build_vest(P, spec, meshes["torso"], J)
            objs_bind += vb; objs_rigid += [(o, "chest") for o in vr]
            belt = prim("torus", name+"_cinto", M.plain("cinto", "#0c0c0c", .4), scale=(.16*s*(1+.1*spec["bulk"]), .115*s*(1+.1*spec["bulk"]), 1.0), minor=.12, sub=1)
            belt.scale = (1, 1, .22); belt.location = (0, .0, .995*s)
            buckle = prim("cube", name+"_fivela", M.plain("fivela", "#8d8a83", .3, 1.0), scale=(.022*s, .004*s, .015*s), sub=0)
            buckle.location = (0, -.122*s*(1+.1*spec["bulk"]), .995*s)
            objs_rigid += [(belt, "pelvis"), (buckle, "pelvis")]
            collar = prim("torus", name+"_gola", shirt, scale=(.056*s, .056*s, 1), minor=.16, sub=1)
            collar.scale = (1, 1, .3); collar.location = (0, .0, 1.475*s)
            objs_rigid.append((collar, "neck"))
            hand_mat = M.plain("luva", "#f0f0ee", .55)
        else:
            s = H/1.75
            shorts = M.fabric("bermuda", "#101012", .75, 260, print_col="#26272a", print_scale=13)
            assign_by(meshes["torso"], [P["skin"]], lambda c: 0)
            for sd in "LR":
                assign_by(meshes["arm."+sd], [P["skin"]], lambda c: 0)
                assign_by(meshes["leg."+sd], [P["skin"]], lambda c: 0)
                objs_bind.append(shell(meshes["leg."+sd], f"{name}_bermuda.{sd}", lambda c: c.z > .56*s, .022*s, shorts))
            objs_bind.append(shell(meshes["torso"], f"{name}_bermuda_q", lambda c: c.z < 1.03*s, .02*s, shorts))
            band = prim("torus", name+"_cos", shorts, scale=(.155*s, .108*s, 1), minor=.1, sub=1)
            band.scale = (1, 1, .25); band.location = (0, .004*s, 1.03*s)
            objs_rigid.append((band, "pelvis"))
            hand_mat = P["skin"]
        for o in objs_bind:
            bind(o, arm)
        # cabeça (rígida no osso da cabeça)
        F = build_head(P, spec); self.F = F
        hair = hair_cap(P, spec, F, spec["hairstyle"])
        head_objs = [o for o in bpy.context.scene.collection.objects if o.name.startswith(name + "_") and o.parent is None
                     and o.type == 'MESH' and o not in objs_bind and o not in [x for x, _ in objs_rigid]
                     and o.name not in [m.name for m in meshes.values()]]
        self.hands = {}
        for sd in "LR":
            self.hands[sd] = build_hand(P, spec, J, sd, hand_mat)
            objs_rigid.append((self.hands[sd]["root"], "hand."+sd))
            for o in build_foot(P, spec, J, sd, spec["kind"] == "agente"):
                objs_rigid.append((o, "foot."+sd))
        for o in head_objs:
            objs_rigid.append((o, "head"))
        for o, b in objs_rigid:
            mw = o.matrix_world.copy()
            o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = b
            bpy.context.view_layer.update()
            o.matrix_world = mw
        bpy.context.view_layer.update()
        # guarda posições de repouso (locais) das partes do rosto
        self.face_rest = {o.name: (o.location.copy(), o.rotation_euler.copy(), o.scale.copy())
                          for o in F["brows"] + F["lids"] + [F["chin"]] + list(F["mouth"].values())}
        self.finger_rest = {f.name: f.rotation_euler.copy() for sd in "LR" for f in self.hands[sd]["fingers"] + [self.hands[sd]["thumb"]]}

    # ---------------------------------------------------------- pose
    def pose(self, p):
        """p: dict osso -> dict(fwd,out,tw,bend,side). Lado R é espelhado automaticamente."""
        for pb in self.arm.pose.bones:
            pb.rotation_euler = (0, 0, 0)
        for key, v in p.items():
            if key.startswith("_"): continue
            pb = self.arm.pose.bones[key]
            sd = -1 if key.endswith(".R") else 1
            b = key.split(".")[0]
            g = lambda k: D(v.get(k, 0))
            if b in ("upperarm", "thigh"):
                pb.rotation_euler = (-g("fwd"), sd*g("tw"), -sd*g("out"))
            elif b in ("forearm",):
                pb.rotation_euler = (-g("bend"), sd*g("tw"), -sd*g("out"))
            elif b in ("shin",):
                pb.rotation_euler = (g("bend"), sd*g("tw"), 0)
            elif b in ("hand",):
                pb.rotation_euler = (-g("fwd"), sd*g("tw"), -sd*g("out"))
            elif b in ("foot",):
                pb.rotation_euler = (g("down"), 0, 0)
            elif b == "shoulder":
                pb.rotation_euler = (g("up"), 0, -sd*g("fwd"))
            else:   # pelvis, spine, chest, neck, head
                pb.rotation_euler = (g("fwd"), g("tw"), -g("side"))

    def place(self, x, y, z, heading_deg):
        self.arm.location = (x, y, z); self.arm.rotation_euler = (0, 0, D(heading_deg))

    def face(self, brow=0.0, frown=0.0, eyes=0.0, mouth=0.0, smile=0.0):
        """brow: -1..1 (abaixa/levanta), frown: 0..1 (franze), eyes: -1 fechado .. 1 arregalado, mouth: 0..1 abertura."""
        s = self.F["s"]
        R = self.arm.data.bones["head"].matrix_local.to_3x3().inverted()
        W = lambda x, y, z: R @ Vector((x, y, z))
        def rot(o, rest, axis, ang):
            o.rotation_euler = (rest.to_matrix() @ Matrix.Rotation(ang, 3, axis)).to_euler('XYZ', rest)
        for i, br in enumerate(self.F["brows"]):
            loc, r0, sc = self.face_rest[br.name]
            sx = 1 if i == 0 else -1
            br.location = loc + W(-sx*.002*s*frown, 0, .006*s*brow - .003*s*frown)
            rot(br, r0, 'Y', sx*D(16*frown - 7*brow))
        for lid in self.F["lids"]:
            loc, r0, sc = self.face_rest[lid.name]
            a = -32 - 28*max(0, eyes) + 122*max(0, -eyes)
            rot(lid, r0, 'X', D(a))
        op = mouth
        for nm, o in self.F["mouth"].items():
            loc, r0, sc = self.face_rest[o.name]
            if nm == "ll": o.location = loc + W(0, 0, -.017*s*op)
            elif nm == "lu": o.location = loc + W(0, 0, .002*s*op)
            elif nm == "cav":
                o.location = loc + W(0, 0, -.008*s*op)
                o.scale = (sc.x*(1 + .2*smile - .2*op), sc.y, sc.z*(1 + 2.6*op))
            elif nm == "teeth": o.location = loc + W(0, 0, .001*s*op)
        cl, cr, cs = self.face_rest[self.F["chin"].name]
        self.F["chin"].location = cl + W(0, 0, -.015*s*op)

    def fingers(self, sd, curl=0.3, point=False, spread=0.0):
        h = self.hands[sd]
        for i, f in enumerate(h["fingers"]):
            c = curl if not (point and i == 0 and False) else 0
            if point and i == 0: c = 0.0          # indicador (i==0 fica do lado do polegar)
            elif point: c = 1.0
            f.rotation_euler = (D((i-1.5)*6*spread), D(95*c), 0)
        h["thumb"].rotation_euler = (D(-35), D(45*(curl if not point else .8)), 0)


AGENTE = dict(name="agente", kind="agente", H=1.76, bulk=1.0, belly=0.3, skin="#4b2f20", lip="#3d2219",
              shirt="#1b2030", pants="#a48d69", hair="#0b0807", hairstyle="curto", headw=1.02, nosew=1.15)
RAPAZ = dict(name="rapaz", kind="rapaz", H=1.71, bulk=-0.6, belly=0.0, skin="#8a5a3c", lip="#6e3e2c",
             hair="#1a110c", hairstyle="cacheado", headw=.97, nosew=1.0)
