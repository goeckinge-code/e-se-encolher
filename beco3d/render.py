"""Renderiza a animação de 30s do beco (Cycles na CPU).

Uso (de dentro da pasta do projeto):
  python3 beco3d/render.py -- still 1.5,5,9          # quadros de teste (segundos) em renders/beco/still/
  python3 beco3d/render.py -- seq                    # todos os quadros (24fps) em renders/beco/frames/
  python3 beco3d/render.py -- seq 0 240              # só um intervalo de quadros (para dividir o trabalho)
Opções: --hq (1080x1920, mais amostras)   --samples N
Também roda no Blender:  blender -b -P beco3d/render.py -- seq
"""
import bpy, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ["still", "1"]
HQ = "--hq" in args
SAMPLES = int(args[args.index("--samples")+1]) if "--samples" in args else (64 if HQ else 20)
args = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i-1] != "--samples")]
mode = args[0]

bpy.ops.wm.read_factory_settings(use_empty=True)
import cenario as C, anim as AN
sc = bpy.context.scene
C.build(); C.sky_and_sun(sc)
F = AN.Filme(sc)

sc.render.engine = 'CYCLES'
cy = sc.cycles
cy.device = 'CPU'; cy.samples = SAMPLES; cy.use_adaptive_sampling = True; cy.adaptive_threshold = .03
cy.use_denoising = True
try: cy.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 2; cy.transparent_max_bounces = 4
cy.caustics_reflective = cy.caustics_refractive = False
cy.blur_glossy = 1.0
sc.render.resolution_x, sc.render.resolution_y = (1080, 1920) if HQ else (540, 960)
sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -.4
try: sc.view_settings.look = 'AgX - Punchy'
except Exception: pass
sc.render.image_settings.file_format = 'PNG'
sc.render.use_persistent_data = True
# leve desfoque de movimento: parece filmado
sc.render.fps = AN.FPS

if mode == "still":
    out = os.path.join(ROOT, "renders", "beco", "still"); os.makedirs(out, exist_ok=True)
    for t in [float(x) for x in args[1].split(",")]:
        F.frame(t)
        sc.render.filepath = os.path.join(out, f"t{t:05.2f}.png")
        t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f"STILL {t:.2f}s plano {AN.shot_at(t)[0]} em {time.time()-t0:.1f}s", flush=True)
else:
    out = os.path.join(ROOT, "renders", "beco", "frames" + ("_hq" if HQ else "")); os.makedirs(out, exist_ok=True)
    n = int(AN.DUR*AN.FPS)
    a = int(args[1]) if len(args) > 1 else 0; b = int(args[2]) if len(args) > 2 else n
    t0 = time.time(); done = 0
    for f in range(a, min(b, n)):
        p = f"{out}/{f:05d}.png"
        if os.path.exists(p): continue          # retoma de onde parou
        F.frame(f/AN.FPS)
        sc.render.filepath = p[:-4] + ".tmp.png"; bpy.ops.render.render(write_still=True); os.replace(p[:-4] + ".tmp.png", p)
        done += 1
        print(f"FRAME {f} ({done}) {(time.time()-t0)/done:.1f}s/q", flush=True)
    print("DONE", a, b, round(time.time()-t0, 1))
