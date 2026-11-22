"""Renderiza um plano do episódio (Workbench) e grava a posição na tela dos objetos com etiqueta.

Uso:
  python golpes/blender/render.py -- ep01-piramide s01 still 0.2,0.8   # quadros de teste em renders/still
  python golpes/blender/render.py -- ep01-piramide s01 seq [--res 0.667]
(python = Python com o módulo bpy; ou: blender -b -P golpes/blender/render.py -- ...)
"""
import bpy, sys, os, json, time, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
GOLPES = os.path.dirname(HERE)
args = sys.argv[sys.argv.index('--') + 1:]
ep, sid, mode = args[0], args[1], args[2]
RES = float(args[args.index("--res") + 1]) if "--res" in args else 1.0
EPD = os.path.join(GOLPES, ep)
sys.path.insert(0, HERE); sys.path.insert(0, EPD)

bpy.ops.wm.read_factory_settings(use_empty=True)
import roteiro as R, cenas
sh = R.shot(sid)
frame, anchors = cenas.BUILD[sid](sh)
scn = bpy.context.scene
scn.render.resolution_x, scn.render.resolution_y = int(R.W * RES), int(R.H * RES)
scn.render.image_settings.file_format = 'JPEG'; scn.render.image_settings.quality = 92
OUT = os.path.join(GOLPES, "renders", ep)

if mode == "still":
    os.makedirs(os.path.join(OUT, "still"), exist_ok=True)
    scn.render.resolution_x, scn.render.resolution_y = 540, 960
    for x in args[3].split(","):
        t = float(x) * sh["dur"] if float(x) <= 1 else float(x)
        frame(t)
        scn.render.filepath = os.path.join(OUT, "still", f"{sid}_{t:05.2f}.jpg")
        bpy.ops.render.render(write_still=True)
elif mode == "anchors":      # só recalcula onde ficam as etiquetas, sem renderizar
    out = os.path.join(OUT, "frames", sid); meta = {}
    for f in range(sh["frames"]):
        frame(f / R.FPS); meta[f] = {a: cenas.kit.project(a) for a in anchors}
    json.dump(meta, open(os.path.join(out, "anchors.json"), "w")); print("ANCHORS", sid)
else:
    out = os.path.join(OUT, "frames", sid); os.makedirs(out, exist_ok=True)
    meta, t0 = {}, time.time()
    for f in range(sh["frames"]):
        t = f / R.FPS
        frame(t)
        p = f"{out}/{f:05d}.jpg"
        if not os.path.exists(p):
            scn.render.filepath = p + ".tmp.jpg"; bpy.ops.render.render(write_still=True); os.replace(p + ".tmp.jpg", p)
        meta[f] = {a: cenas.kit.project(a) for a in anchors}
    json.dump(meta, open(os.path.join(out, "anchors.json"), "w"))
    print("DONE", sid, sh["frames"], round(time.time() - t0, 1), "s")
