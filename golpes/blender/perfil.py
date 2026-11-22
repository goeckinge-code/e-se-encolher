"""Foto de perfil do protagonista (o cara de terno). Quadrada, com o rosto no centro para o corte redondo.

Uso: python golpes/blender/perfil.py   (python com o módulo bpy)
Saída: golpes/assets/perfil/perfil_<cor>.png (1440x1440)
"""
import bpy, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(os.path.dirname(HERE), "assets", "perfil")
os.makedirs(OUT, exist_ok=True)

VARIANTES = {"amarelo": "#F7C548", "azul": "#5DADE2", "verde": "#58C98B"}

for nome, cor in VARIANTES.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import importlib, kit; importlib.reload(kit)
    from kit import *
    setup(cor); cyclo(cor)
    for o in ("floor", "wall"): bpy.data.objects.remove(bpy.data.objects[o])   # fundo liso (só a cor do mundo)
    h = hero("hero", (0, 0, 0), rotz=-0.28)
    h.pose(0.0, armR=0.12, armRs=0.05, armL=0.12, armLs=0.05, bob=0, head=(0.04, 0, 0.12))
    h.expr("smile")
    for e in h.eyes: e.scale.z = 1.0
    # notas e moedas flutuando atrás, nos cantos (ficam fora do rosto)
    for i, (x, z, r) in enumerate([(-0.85, 2.65, 0.5), (0.72, 2.75, -0.6), (-0.9, 1.6, 1.2), (0.8, 1.65, -1.1)]):
        if i % 2: coin(f"c{i}", (x, 1.4, z), r=0.2, rot=(math.pi / 2, 0, r))
        else: bill(f"b{i}", (x, 1.4, z), rot=(0.3, r, 0.4), s=0.9)
    cam = camera(55)
    look(cam, (0.5, -4.4, 2.3), (0.02, 0, 2.02))
    s = bpy.context.scene
    s.render.resolution_x = s.render.resolution_y = 1440
    s.display.render_aa = '16'
    s.render.image_settings.file_format = 'PNG'
    s.render.filepath = os.path.join(OUT, f"perfil_{nome}.png")
    bpy.ops.render.render(write_still=True)
    print("OK", s.render.filepath)
