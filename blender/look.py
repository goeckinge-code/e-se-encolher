"""Configuração de render (Workbench estilizado) + controle do Léo por quadro."""
import bpy, math
from mathutils import Vector
from lib import Leo, EXPR_EYE, EXPR_MOUTH, EXPR_BROW, hexcol

W, H, FPS = 1080, 1920, 30

def setup_render(bg="#F3D6BF", res=1.0, aa="16"):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.resolution_x, sc.render.resolution_y = int(W*res), int(H*res)
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 93
    sh = sc.display.shading
    sh.light = 'STUDIO'
    try: sh.studio_light = 'paint.sl'
    except Exception: pass
    sh.color_type = 'MATERIAL'
    sh.show_shadows = True; sh.shadow_intensity = 0.45
    sh.show_cavity = True; sh.cavity_type = 'BOTH'
    sh.cavity_ridge_factor = 0.6; sh.cavity_valley_factor = 1.0
    sh.curvature_ridge_factor = 0.5; sh.curvature_valley_factor = 0.7
    sh.show_object_outline = True; sh.object_outline_color = hexcol("#1E1B2E")[:3]
    sh.show_specular_highlight = True
    sc.display.light_direction = (0.45, -0.55, 0.7)
    sc.display.shadow_shift = 0.08; sc.display.shadow_focus = 0.9
    sc.display.render_aa = aa
    sh.background_type = 'VIEWPORT'; sh.background_color = hexcol(bg)[:3]
    sc.view_settings.view_transform = 'Standard'
    return sc

def camera(lens=50):
    cd = bpy.data.cameras.new("cam"); cd.lens = lens; cd.sensor_fit = 'VERTICAL'
    cam = bpy.data.objects.new("cam", cd); bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam

def look_at(cam, eye, target, roll=0.0):
    cam.location = Vector(eye)
    d = Vector(target) - Vector(eye)
    q = d.to_track_quat('-Z', 'Y')
    cam.rotation_mode = 'QUATERNION'
    from mathutils import Quaternion
    cam.rotation_quaternion = q @ Quaternion((0, 0, 1), roll)

def at(keys, t):
    v = keys[0][1]
    for k in keys:
        if t >= k[0]: v = k[1]
    return v

def last_change(keys, t):
    c = -9
    for k in keys:
        if t >= k[0]: c = k[0]
    return c

def cl(x, a=0, b=1): return max(a, min(b, x))
def ease(u): u = cl(u); return u*u*(3-2*u)
def eout(u): u = cl(u); return 1-(1-u)**3
def back(u): u = cl(u); c = 1.7; return 1+(c+1)*(u-1)**3+c*(u-1)**2
def lerp(a, b, u): return a+(b-a)*u

class LeoCtl:
    def __init__(self, name="leo"):
        self.L = Leo(name)

    def pose(self, t, loc=(0, 0, 0), s=1.0, rotz=0.0, roty=0.0, rotx=0.0, expr=(("neutral"),), mouth=None,
             arms=(8, 8), tilt=0.0, seed=0.0, look=(0, 0), fwd=0.0, big=False):
        L = self.L
        if isinstance(expr, str): expr = [[0, expr]]
        ex = at(expr, t); ch = t - last_change(expr, t)
        sq = 1 - 0.1*math.sin(math.pi*ch/0.3) if ch < 0.3 else 1
        L.root.location = loc; L.root.scale = (s, s, s)
        L.root.rotation_euler = (rotx, roty, rotz)
        b = 1 + 0.016*math.sin(t*3.1 + seed)
        L.torso.scale = (1/math.sqrt(b), 1/math.sqrt(b), b)
        L.hip.location.z = 0.5
        L.shirt.scale = (1.55, 1.5, 2.0) if big else (1, 0.94, 1.39)
        L.shirt.location.z = 0.18 if big else 0.30
        for o in bpy.data.objects:
            if o.name.startswith(L.root.name+"_slv"):
                o.scale = (1.9, 1.9, 2.6) if big else (1, 1, 1.1)
                o.location.z = -0.16 if big else -0.03
        L.torso.rotation_euler = (math.radians(fwd), 0, 0)
        L.head.rotation_euler = (math.radians(look[1] + math.sin(t*1.9+seed)*1.5), math.radians(tilt + math.sin(t*1.3+seed)*2.0), math.radians(look[0]))
        L.head.scale = (2-sq, 2-sq, sq)
        # braços: ângulo 0 = para baixo, 90 = para o lado, 170 = para cima ; negativo = para frente/dentro
        for sx, a in ((-1, arms[0]), (1, arms[1])):
            if isinstance(a, tuple):   # (lado, frente)
                side, front = a
            else:
                side, front = a, 0
            L.arm[sx].rotation_euler = (math.radians(-front), math.radians(-sx*side), 0)
        eye = EXPR_EYE[ex]
        blink = ((t + seed) % 3.3) < 0.12 and eye == "dot"
        for k, g in L.eyes.items():
            vis = (k == eye and not blink) or (blink and k == "closed")
            for o in g.children_recursive: o.hide_render = not vis
        m = (at(mouth, t) if mouth else None) or EXPR_MOUTH[ex]
        for k, g in L.mouths.items():
            for o in g.children_recursive: o.hide_render = (k != m)
        dz, rot = EXPR_BROW[ex]
        for sx in (-1, 1):
            br = L.brow[sx]; br.location.z = 0.53 + dz; br.rotation_euler = (0, math.radians(sx*rot), 0)
