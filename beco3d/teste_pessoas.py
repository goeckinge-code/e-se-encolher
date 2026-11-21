"""Teste: os dois personagens lado a lado sob o sol."""
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
bpy.ops.wm.read_factory_settings(use_empty=True)
import pessoas as PS, mat as M
sc = bpy.context.scene
a = PS.Pessoa(PS.AGENTE); r = PS.Pessoa(PS.RAPAZ)
a.place(-.45, 0, 0, 0); r.place(.45, 0, 0, 0)
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if "pose" in args:
    a.pose({"upperarm.R": dict(fwd=80, out=10), "forearm.R": dict(bend=5), "head": dict(tw=-20), "upperarm.L": dict(fwd=30, out=20), "forearm.L": dict(bend=70)})
    a.fingers("R", point=True); a.fingers("L", .2, spread=1)
    a.face(brow=.6, mouth=.5)
    r.pose({"upperarm.R": dict(fwd=30, out=20), "forearm.R": dict(bend=110), "upperarm.L": dict(fwd=20, out=35), "forearm.L": dict(bend=40), "head": dict(tw=15)})
    r.fingers("L", .1, spread=1); r.face(brow=1, eyes=1, mouth=.8)
else:
    for p in (a, r): p.face(); p.fingers("L", .3); p.fingers("R", .3)
fl = bpy.data.objects.new("chao", bpy.data.meshes.new("chao")); sc.collection.objects.link(fl)
fl.data.from_pydata([(-5,-5,0),(5,-5,0),(5,5,0),(-5,5,0)],[],[(0,1,2,3)]); fl.data.materials.append(M.concrete())
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
sky = w.node_tree.nodes.new("ShaderNodeTexSky")
w.node_tree.links.new(sky.outputs[0], w.node_tree.nodes["Background"].inputs[0])
try: sky.sky_type = 'NISHITA'
except Exception: pass
sky.sun_elevation = math.radians(55); sky.sun_rotation = math.radians(200)
w.node_tree.nodes["Background"].inputs[1].default_value = .25
sun = bpy.data.objects.new("sol", bpy.data.lights.new("sol", 'SUN')); sun.data.energy = 3.2; sun.data.angle = math.radians(1)
sun.rotation_euler = (math.radians(35), 0, math.radians(200)); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 35
view = args[0] if args and args[0] in ("front","back","face","faceR","hand") else "front"
if view == "front": cam.location = (0, -4.2, 1.1); cam.rotation_euler = (math.radians(88), 0, 0)
elif view == "back": cam.location = (0, 4.2, 1.2); cam.rotation_euler = (math.radians(88), 0, math.radians(180))
elif view == "face": cam.location = (-.45, -.7, 1.62); cam.rotation_euler = (math.radians(90), 0, 0); cam.data.lens = 50
elif view == "faceR": cam.location = (.45, -.7, 1.58); cam.rotation_euler = (math.radians(90), 0, 0); cam.data.lens = 50
if view == "hand": cam.location = (-.9, -.9, .85); cam.rotation_euler = (math.radians(90), 0, math.radians(-30)); cam.data.lens = 60
sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 540, 960
sc.view_settings.view_transform = 'AgX'; 
try: sc.view_settings.look = 'AgX - Punchy'
except Exception as e: print('LOOK', e)
sc.view_settings.exposure = -1.0
sc.render.filepath = os.path.join(sys.argv[-1])
bpy.ops.render.render(write_still=True)
