"""Materiais procedurais (Cycles) para o beco: reboco manchado, concreto, tecido, pele."""
import bpy

def hexcol(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    return (*[((x+0.055)/1.055)**2.4 if x > 0.04045 else x/12.92 for x in c], a)

_cache = {}

def _base(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf

def _tex_coord(nt, mapping_scale=1.0, obj=True):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (mapping_scale,)*3
    nt.links.new(tc.outputs["Object" if obj else "Generated"], mp.inputs["Vector"])
    return mp.outputs["Vector"]

def _noise(nt, vec, scale, detail=8, rough=0.6):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"]); return n

def _ramp(nt, inp, stops):
    r = nt.nodes.new("ShaderNodeValToRGB"); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = stops[0][0], stops[0][1]
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], stops[-1][1]
    for p, c in stops[1:-1]:
        e = cr.elements.new(p); e.color = c
    nt.links.new(inp, r.inputs["Fac"]); return r

def _bump(nt, bsdf, height, strength=0.3, dist=0.02):
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = strength
    b.inputs["Distance"].default_value = dist
    nt.links.new(height, b.inputs["Height"]); nt.links.new(b.outputs["Normal"], bsdf.inputs["Normal"])
    return b

def mix_col(nt, fac, a, b):
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'
    nt.links.new(fac, mx.inputs[0])
    for i, v in ((6, a), (7, b)):
        if isinstance(v, tuple): mx.inputs[i].default_value = v
        else: nt.links.new(v, mx.inputs[i])
    return mx.outputs[2]

def plaster(name, color, dirt="#6b6650", stain=0.55, scale=1.0, rough=0.9):
    """Parede de reboco pintado, com manchas de umidade escorrendo e sujeira perto do chão."""
    key = ("pl", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, scale)
    # manchas grandes (umidade) — esticadas na vertical para parecer escorrido
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(vec, sep.inputs[0])
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    mulz = nt.nodes.new("ShaderNodeMath"); mulz.operation = 'MULTIPLY'; mulz.inputs[1].default_value = 0.25
    nt.links.new(sep.outputs[2], mulz.inputs[0])
    nt.links.new(sep.outputs[0], comb.inputs[0]); nt.links.new(sep.outputs[1], comb.inputs[1]); nt.links.new(mulz.outputs[0], comb.inputs[2])
    n1 = _noise(nt, comb.outputs[0], 1.6, 10, 0.65)
    # sujeira perto do chão (gradiente em Z)
    grad = nt.nodes.new("ShaderNodeMapRange"); grad.inputs[1].default_value = 0.0; grad.inputs[2].default_value = 1.3
    grad.inputs[3].default_value = 1.0; grad.inputs[4].default_value = 0.0
    nt.links.new(sep.outputs[2], grad.inputs[0])
    add = nt.nodes.new("ShaderNodeMath"); add.operation = 'ADD'
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.4
    nt.links.new(grad.outputs[0], mul.inputs[0])
    nt.links.new(n1.outputs["Fac"], add.inputs[0]); nt.links.new(mul.outputs[0], add.inputs[1])
    r = _ramp(nt, add.outputs[0], [(0.5, (1, 1, 1, 1)), (0.5 + 0.35*(1-stain) + 0.25, (0, 0, 0, 1))])
    inv = nt.nodes.new("ShaderNodeInvert"); nt.links.new(r.outputs[0], inv.inputs[1])
    col = mix_col(nt, inv.outputs[0], hexcol(color), hexcol(dirt))
    # variação fina de cor
    n2 = _noise(nt, vec, 18, 6, 0.5)
    ov = nt.nodes.new("ShaderNodeMix"); ov.data_type = 'RGBA'; ov.blend_type = 'OVERLAY'; ov.inputs[0].default_value = 0.18
    nt.links.new(col, ov.inputs[6]); nt.links.new(n2.outputs["Color"], ov.inputs[7])
    nt.links.new(ov.outputs[2], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    n3 = _noise(nt, vec, 60, 4, 0.7)
    _bump(nt, bsdf, n3.outputs["Fac"], 0.25, 0.01)
    _cache[key] = m; return m

def concrete(name="concreto", color="#9a968c", scale=1.0):
    key = ("cc", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, scale)
    n1 = _noise(nt, vec, 2.2, 10, 0.6)
    n2 = _noise(nt, vec, 30, 6, 0.6)
    r = _ramp(nt, n1.outputs["Fac"], [(0.3, hexcol("#8a857b")), (0.5, hexcol(color)), (0.72, hexcol("#c4bfb3"))])
    ov = nt.nodes.new("ShaderNodeMix"); ov.data_type = 'RGBA'; ov.blend_type = 'OVERLAY'; ov.inputs[0].default_value = 0.35
    nt.links.new(r.outputs[0], ov.inputs[6]); nt.links.new(n2.outputs["Color"], ov.inputs[7])
    nt.links.new(ov.outputs[2], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.85
    _bump(nt, bsdf, n2.outputs["Fac"], 0.35, 0.01)
    _cache[key] = m; return m

def mosaic(name="caco"):
    """Revestimento de caco de cerâmica/pedra (rodapé das casas): células de Voronoi com rejunte."""
    key = ("mo", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, 1.0)
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs["Scale"].default_value = 9
    nt.links.new(vec, vo.inputs["Vector"])
    vc = nt.nodes.new("ShaderNodeTexVoronoi"); vc.inputs["Scale"].default_value = 9
    nt.links.new(vec, vc.inputs["Vector"])
    edge = _ramp(nt, vo.outputs["Distance"], [(0.0, (0, 0, 0, 1)), (0.04, (1, 1, 1, 1))])
    tone = _ramp(nt, vc.outputs["Color"], [(0.0, hexcol("#cfcac0")), (0.5, hexcol("#ebe7df")), (1.0, hexcol("#a9a49a"))])
    col = mix_col(nt, edge.outputs[0], hexcol("#5e5a52"), tone.outputs[0])
    nt.links.new(col, bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.35
    _bump(nt, bsdf, edge.outputs[0], 0.6, 0.01)
    _cache[key] = m; return m

def paint(name, color, rough=0.35, metallic=0.0, chip=0.0):
    """Tinta lisa (corrimão azul, grades brancas); chip = descascado."""
    key = ("pa", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    if chip > 0:
        vec = _tex_coord(nt, 1.0)
        n = _noise(nt, vec, 14, 8, 0.7)
        r = _ramp(nt, n.outputs["Fac"], [(0.62 - chip*0.2, (0, 0, 0, 1)), (0.66 - chip*0.2, (1, 1, 1, 1))])
        col = mix_col(nt, r.outputs[0], hexcol(color), hexcol("#5b4a3a"))
        nt.links.new(col, bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = hexcol(color)
    bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metallic
    _cache[key] = m; return m

def fabric(name, color, rough=0.85, scale=220, print_col=None, print_scale=7):
    """Tecido: trama fina no relevo; print_col adiciona estampa (bermuda)."""
    key = ("fa", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, 1.0)
    w = nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value = scale; w.inputs["Distortion"].default_value = 2
    nt.links.new(vec, w.inputs["Vector"])
    n = _noise(nt, vec, 9, 6, 0.6)
    base = hexcol(color)
    if print_col:
        vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = 'SMOOTH_F1' if hasattr(vo, 'feature') else 'F1'
        vo.inputs["Scale"].default_value = print_scale
        nt.links.new(vec, vo.inputs["Vector"])
        vo2 = nt.nodes.new("ShaderNodeTexVoronoi"); vo2.feature = 'DISTANCE_TO_EDGE'; vo2.inputs["Scale"].default_value = print_scale
        nt.links.new(vec, vo2.inputs["Vector"])
        r = _ramp(nt, vo2.outputs["Distance"], [(0.0, (1, 1, 1, 1)), (0.035, (0, 0, 0, 1))])
        col = mix_col(nt, r.outputs[0], base, hexcol(print_col))
    else:
        col = mix_col(nt, n.outputs["Fac"], hexcol(color), tuple(c*0.8 for c in base[:3]) + (1,))
    nt.links.new(col, bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    add = nt.nodes.new("ShaderNodeMath"); add.operation = 'ADD'
    nt.links.new(w.outputs["Fac"], add.inputs[0]); nt.links.new(n.outputs["Fac"], add.inputs[1])
    _bump(nt, bsdf, add.outputs[0], 0.25, 0.004)
    _cache[key] = m; return m

def skin(name, color, rough=0.5):
    key = ("sk", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, 1.0)
    n = _noise(nt, vec, 40, 6, 0.6)
    n2 = _noise(nt, vec, 4, 4, 0.5)
    base = hexcol(color)
    col = mix_col(nt, n2.outputs["Fac"], tuple(c*0.82 for c in base[:3]) + (1,), tuple(min(1, c*1.12) for c in base[:3]) + (1,))
    nt.links.new(col, bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.12
        bsdf.inputs["Subsurface Radius"].default_value = (0.9, 0.4, 0.25)
        bsdf.inputs["Subsurface Scale"].default_value = 0.01
    if "Specular IOR Level" in bsdf.inputs: bsdf.inputs["Specular IOR Level"].default_value = 0.45
    _bump(nt, bsdf, n.outputs["Fac"], 0.12, 0.002)
    _cache[key] = m; return m

def plain(name, color, rough=0.5, metallic=0.0, emit=0.0, alpha=1.0):
    key = ("pn", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    bsdf.inputs["Base Color"].default_value = hexcol(color)
    bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metallic
    if emit:
        bsdf.inputs["Emission Color"].default_value = hexcol(color); bsdf.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        bsdf.inputs["Alpha"].default_value = alpha
    _cache[key] = m; return m

def glass(name="vidro"):
    key = ("gl", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    bsdf.inputs["Base Color"].default_value = hexcol("#4a5a60")
    bsdf.inputs["Roughness"].default_value = 0.05; bsdf.inputs["Metallic"].default_value = 0.6
    _cache[key] = m; return m

def hair(name, color="#120d0a", scale=300):
    key = ("hr", name)
    if key in _cache: return _cache[key]
    m, nt, bsdf = _base(name)
    vec = _tex_coord(nt, 1.0)
    n = _noise(nt, vec, scale, 4, 0.8)
    bsdf.inputs["Base Color"].default_value = hexcol(color)
    bsdf.inputs["Roughness"].default_value = 0.7
    _bump(nt, bsdf, n.outputs["Fac"], 0.8, 0.004)
    _cache[key] = m; return m
