"""Renderiza uma cena de "Como funciona o micro-ondas?".

  python3 episodios/microondas/render.py -- s0 seq          # 30fps, 720x1280 (Workbench)
  python3 episodios/microondas/render.py -- s0 seq --hq     # 30fps, 1080x1920
  python3 episodios/microondas/render.py -- s0 still 0.2,0.5,3.1   # quadros de teste (fração da cena ou segundos)
(ou: blender -b -P episodios/microondas/render.py -- s0 seq)

Desfoque de movimento: nos whips (quando o quadro muda rápido) cada quadro é a média de vários subquadros,
como o borrão da referência. Quadros parados são renderizados uma vez só.
"""
import bpy, sys, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import roteiro as R

args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
HQ = "--hq" in args
args = [a for a in args if a != "--hq"]
sid, mode = args[0], args[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
import cenas
sc_ = next(s for s in R.SCENES if s["id"] == sid)
frame, rig = cenas.BUILD[sid](sc_, lambda n, end=False: R.wt(sc_, n, end))
scn = bpy.context.scene
FPS = 30
AA = '8' if HQ else '5'   # 16 amostras custa 2x e quase não muda nada em 720p
OUT = os.path.join(HERE, "renders")

def render_to(path):
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)

def render_blur(t, path, tmp):
    """média de subquadros quando a câmera está em movimento rápido (obturador de meio quadro)."""
    v = rig.speed(t)
    n = 1 if v < 0.012 else 3 if v < 0.04 else 5 if v < 0.1 else 7
    if n == 1:
        scn.display.render_aa = AA; frame(t); render_to(path); return 1
    scn.display.render_aa = 'FXAA'      # a média dos subquadros já suaviza as bordas
    acc = None
    for k in range(n):
        frame(t + (k/(n-1) - 0.5) * (0.5/FPS))
        render_to(tmp)
        import cv2
        im = cv2.imread(tmp).astype(np.float32)
        acc = im if acc is None else acc + im
    import cv2
    cv2.imwrite(path, (acc/n).clip(0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
    return n

if mode == "still":
    os.makedirs(os.path.join(OUT, "still"), exist_ok=True)
    scn.render.resolution_x, scn.render.resolution_y = 540, 960
    for x in args[2].split(","):
        t = float(x); tt = t*sc_["dur"] if t <= 1.0 else t
        p = os.path.join(OUT, "still", f"{sid}_{tt:05.2f}.jpg")
        render_blur(tt, p, p + ".tmp.jpg")
else:
    out = os.path.join(OUT, "frames" + ("_hq" if HQ else ""), sid); os.makedirs(out, exist_ok=True)
    scn.render.resolution_x, scn.render.resolution_y = (1080, 1920) if HQ else (720, 1280)
    n = int(round(sc_["dur"]*FPS)); t0 = time.time(); subs = 0
    for f in range(n):
        p = f"{out}/{f:05d}.jpg"
        if os.path.exists(p): continue          # retoma de onde parou
        subs += render_blur(f/FPS, p + ".part.jpg", p + ".tmp.jpg"); os.replace(p + ".part.jpg", p)
    print("DONE", sid, n, "quadros", subs, "renders", round(time.time()-t0, 1), "s")
