"""Renderiza uma cena do episódio com o Blender.

Uso (Blender instalado):
  blender -b -P blender/render.py -- s0 seq            # rápido (Workbench, 15fps, 720x1280)
  blender -b -P blender/render.py -- s0 seq --hq       # alta qualidade (Eevee, 30fps, 1080x1920)
  blender -b -P blender/render.py -- s0 still 0.3,0.85 # quadros de teste (fração da cena ou segundos)

Também funciona com o módulo bpy do pip:  python3 blender/render.py -- s0 seq
Cenas: s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 (ver hyperframes/build/build.py → SCENES)
"""
import bpy, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "hyperframes", "build"))
import build as B   # roteiro, tempos de cada fala e cena

args = sys.argv[sys.argv.index('--')+1:]
sid, mode = args[0], args[1]
HQ = "--hq" in args
args = [a for a in args if a != "--hq"]

bpy.ops.wm.read_factory_settings(use_empty=True)
import scenes
sc_ = next(s for s in B.SCENES if s["id"] == sid)
W_ = lambda n: B.wt(sc_, n)
frame = scenes.BUILD[sid](sc_, W_)
scn = bpy.context.scene

def use_eevee():
    """Eevee com contorno (Freestyle) — precisa de GPU para ficar rápido."""
    sh = scn.display.shading
    bg = sh.background_color[:]
    scn.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    scn.eevee.taa_render_samples = 32
    world = bpy.data.worlds.new("w"); scn.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (*bg, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.5; sun.rotation_euler = (0.9, 0.2, 0.6); scn.collection.objects.link(sun)
    scn.render.use_freestyle = True
    scn.render.line_thickness = 1.6
    scn.view_settings.view_transform = 'Standard'

if mode == "still":
    res = 0.5
    os.makedirs(os.path.join(ROOT, "renders", "still"), exist_ok=True)
    scn.render.resolution_x, scn.render.resolution_y = int(1080*res), int(1920*res)
    if HQ: use_eevee()
    for t in [float(x) for x in args[2].split(",")]:
        tt = t*sc_["dur"] if t <= 1.0 else t
        frame(tt)
        scn.render.filepath = os.path.join(ROOT, "renders", "still", f"{sid}_{tt:.2f}.jpg")
        bpy.ops.render.render(write_still=True)
else:
    out = os.path.join(ROOT, "renders", "frames" + ("_hq" if HQ else ""), sid); os.makedirs(out, exist_ok=True)
    if HQ:
        FPS = 30; scn.render.resolution_x, scn.render.resolution_y = 1080, 1920; use_eevee()
    else:
        FPS = 15; scn.render.resolution_x, scn.render.resolution_y = 720, 1280; scn.display.render_aa = '8'
    n = int(round(sc_["dur"]*FPS)); t0 = time.time()
    for f in range(n):
        p = f"{out}/{f:05d}.jpg"
        if os.path.exists(p): continue          # retoma de onde parou
        frame(f/FPS)
        scn.render.filepath = p + ".tmp.jpg"; bpy.ops.render.render(write_still=True); os.replace(p + ".tmp.jpg", p)
    print("DONE", sid, n, round(time.time()-t0, 1))
