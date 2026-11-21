import bpy, sys, os, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
bpy.ops.wm.read_factory_settings(use_empty=True)
import cenario as C
sc = bpy.context.scene
t=time.time(); C.build(); C.sky_and_sun(sc); print("build", time.time()-t)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 432, 768
sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -1.0
out = sys.argv[-1]
views = {"beco": ((0, -9, 1.6), (88, 0, 0), 24), "escada": ((.6, -2.2, 1.5), (85, 0, 8), 24),
         "patio": ((-1.2, -1.0, 1.5), (86, 0, -15), 24), "contra": ((.9, 3.0, 2.6), (80, 0, 180), 22)}
for k, (loc, rot, lens) in views.items():
    cam.location = loc; cam.rotation_euler = [math.radians(a) for a in rot]; cam.data.lens = lens
    sc.render.filepath = f"{out}_{k}.png"; t = time.time(); bpy.ops.render.render(write_still=True); print(k, time.time()-t)
