"""Outros personagens do canal, com o mesmo "esqueleto" do Léo (root/hip/torso/head/arm/eyes/mouths/brow),
então funcionam com o mesmo controle de pose (look.LeoCtl) e a mesma câmera.

Bia:  cabelo crespo com dois coques, óculos redondos, moletom roxo, calça verde, tênis laranja.
      Opcional: rabo (episódio "E se você acordasse com um rabo?").
Davi: cabelo loiro espetado, sardas, camiseta listrada vermelha e branca, bermuda laranja, tênis azul.
      (episódio "E se a gravidade sumisse por 10 segundos?")
"""
import bpy, math
from mathutils import Vector
from lib import (sphere, cube, cyl, capsule, torus, arc_tube, poly_tube, empty, link, mat, INKC, Leo,
                 EXPR_EYE, EXPR_MOUTH, EXPR_BROW)
import look

B_SKIN, B_HAIR, B_HOOD, B_HOOD_D, B_PANTS, B_SHOE, B_GLASS = "#8D5A3B", "#2A1A14", "#8E5CD9", "#6B3FB3", "#3FA77A", "#FF8A3D", "#1E1B2E"
TAIL, TAIL_TIP = "#C9783A", "#FFF3E0"

STYLES = {
    "bia":  dict(skin="#8D5A3B", hair="#2A1A14", top="#8E5CD9", top_d="#6B3FB3", pants="#3FA77A", legs="#3FA77A", shoe="#FF8A3D", blush="#C2655A"),
    "davi": dict(skin="#F2C29B", hair="#F5C542", top="#E8453C", top_d="#FFFFFF", pants="#F28C28", legs="#F2C29B", shoe="#3D7BE0", blush="#F08C7E"),
}

class Bia:
    def __init__(self, name="bia", tail=False, style="bia"):
        n = name; S = STYLES[style]; self.style = style
        B_SKIN, B_HAIR, B_HOOD, B_HOOD_D, B_PANTS, B_SHOE = S["skin"], S["hair"], S["top"], S["top_d"], S["pants"], S["shoe"]
        davi = style == "davi"
        self.root = empty(n)
        self.hip = empty(n+"_hip", (0, 0, 0.5), self.root)
        hp = self.hip
        for sx in (-1, 1):
            capsule(f"{n}_leg{sx}", S["legs"], (sx*0.1, 0, 0.0), (sx*0.1, 0, -0.42), 0.04 if davi else 0.055, hp)
            if davi:
                cyl(f"{n}_sock{sx}", "#FFFFFF", (sx*0.1, 0, -0.38), 0.048, 0.08, hp, bevel=0.01)
            sphere(f"{n}_shoe{sx}", B_SHOE, (sx*0.13, -0.05, -0.47), 0.095, (1, 1.4, 0.6), hp, sub=1)
            sphere(f"{n}_sole{sx}", "#FFFFFF", (sx*0.13, -0.05, -0.51), 0.092, (1.02, 1.42, 0.18), hp, sub=1)
        self.torso = empty(n+"_torso", (0, 0, 0), hp)
        tz = self.torso
        sphere(n+"_pants", B_PANTS, (0, 0, 0.30), 0.25, (1, 0.92, 1.38), tz, sub=2, seg=32)
        # moletom: mesmo volume da camiseta do Léo (look.LeoCtl mexe em shirt.scale/location)
        self.shirt = sphere(n+"_shirt", B_HOOD, (0, 0, 0.30), 0.262, (1, 0.94, 1.39), tz, sub=2, seg=48)
        Leo._cut_lower(self, self.shirt, 0.2)
        if davi:   # listras brancas na camiseta + gola
            for k in range(4):
                z = 0.27 + k*0.1
                rr_ = 0.262*math.sqrt(max(0.05, 1 - ((z - 0.30)/(0.262*1.39))**2))
                o = torus(f"{n}_strp{k}", B_HOOD_D, (0, 0, z), rr_*0.985, 0.013, tz); o.scale = (1, 0.94, 1)
            torus(n+"_collar", B_HOOD_D, (0, 0, 0.66), 0.13, 0.03, tz)
        else:
            torus(n+"_hem", B_HOOD_D, (0, 0, 0.215), 0.245, 0.03, tz)
            sphere(n+"_pocket", B_HOOD_D, (0, -0.235, 0.33), 0.12, (1.2, 0.25, 0.55), tz, sub=1)
            sphere(n+"_hood", B_HOOD_D, (0, 0.13, 0.66), 0.2, (1.25, 0.8, 0.55), tz, sub=1)
            for sx in (-1, 1):
                poly_tube(f"{n}_cord{sx}", "#FFFFFF", [(sx*0.06, -0.235, 0.62), (sx*0.07, -0.25, 0.48)], 0.012, tz)
                sphere(f"{n}_cordt{sx}", "#FFFFFF", (sx*0.07, -0.25, 0.47), 0.02, parent=tz, sub=0, seg=10)
        self.arm = {}
        for sx in (-1, 1):
            sh = empty(f"{n}_sh{sx}", (sx*0.23, 0, 0.55), tz)
            sphere(f"{n}_slv{sx}", B_HOOD, (0, 0, -0.03), 0.085, (1, 1, 1.1), sh, sub=1)
            capsule(f"{n}_arm{sx}", B_SKIN if davi else B_HOOD, (0, 0, -0.03), (sx*0.06, 0, -0.34), 0.035 if davi else 0.045, sh)
            sphere(f"{n}_hand{sx}", B_SKIN, (sx*0.06, 0, -0.41), 0.058, parent=sh, sub=1)
            self.arm[sx] = sh
        # cabeça
        self.head = empty(n+"_head", (0, 0, 0.7), tz)
        hd = self.head
        sphere(n+"_skull", B_SKIN, (0, 0, 0.38), 0.4, parent=hd, sub=2, seg=32)
        for sx in (-1, 1):
            sphere(f"{n}_ear{sx}", B_SKIN, (sx*0.39, 0.02, 0.36), 0.07, (0.5, 0.8, 1), hd, sub=1)
            sphere(f"{n}_blush{sx}", S["blush"], (sx*0.22, -0.33, 0.28), 0.07, (1, 0.35, 0.6), hd, sub=1)
        if davi:   # cabelo loiro espetado + sardas
            sphere(n+"_hairback", B_HAIR, (0, 0.08, 0.5), 0.41, (1.02, 1, 0.9), hd, sub=1, seg=32)
            import bpy as _b
            for k in range(9):
                a = -1.1 + k*0.275
                _b.ops.mesh.primitive_cone_add(radius1=0.11, depth=0.32, location=(0, 0, 0))
                c = _b.context.object; c.name = f"{n}_spike{k}"; c.parent = hd
                c.location = (math.sin(a)*0.3, -0.05 + abs(math.sin(a))*0.08, 0.72 + math.cos(a)*0.12)
                c.rotation_euler = (math.radians(-15), a*0.9, 0); mat_ = mat(B_HAIR); c.data.materials.append(mat_)
            for k in range(5):
                sphere(f"{n}_fr{k}", B_HAIR, (-0.2+k*0.1, -0.31, 0.62), 0.07, (1, 0.6, 0.8), hd, sub=1)
            for sx in (-1, 1):
                for k in range(3):
                    sphere(f"{n}_frk{sx}{k}", "#C9805A", (sx*(0.17+k*0.04), -0.385, 0.33+(k % 2)*0.03), 0.012, parent=hd, sub=0, seg=8)
        else:
            sphere(n+"_hairback", B_HAIR, (0, 0.08, 0.46), 0.42, (1.04, 1, 1.0), hd, sub=1, seg=32)
            sphere(n+"_hairtop", B_HAIR, (0, -0.02, 0.62), 0.36, (1.05, 0.95, 0.55), hd, sub=1)
            for sx in (-1, 1):
                sphere(f"{n}_bun{sx}", B_HAIR, (sx*0.36, 0.02, 0.78), 0.17, parent=hd, sub=1)
                torus(f"{n}_tie{sx}", "#FFD93D", (sx*0.31, 0.02, 0.69), 0.08, 0.022, hd, rot=(0, math.radians(sx*40), 0))
                torus(f"{n}_lens{sx}", B_GLASS, (sx*0.14, -0.39, 0.42), 0.095, 0.014, hd, rot=(math.pi/2, 0, 0))
            poly_tube(n+"_bridge", B_GLASS, [(-0.05, -0.4, 0.43), (0.05, -0.4, 0.43)], 0.012, hd)
            for k in range(6):
                sphere(f"{n}_fr{k}", B_HAIR, (-0.25+k*0.1, -0.3, 0.6+0.03*math.sin(k)), 0.07, (1, 0.7, 0.7), hd, sub=1)
        # olhos / bocas / sobrancelhas: mesmos nomes de grupo do Léo
        self.eyes = {}; self.mouths = {}
        def grp(nm): return empty(nm, (0, 0, 0), hd)
        g = grp(n+"_e_dot")
        for sx in (-1, 1):
            sphere(f"{n}_eye{sx}", INKC, (sx*0.14, -0.375, 0.42), 0.05, (1, 0.5, 1.25), g, sub=1)
            sphere(f"{n}_glint{sx}", "#FFFFFF", (sx*0.14+0.02, -0.405, 0.45), 0.015, parent=g, sub=0, seg=12)
        self.eyes["dot"] = g
        g = grp(n+"_e_shock")
        for sx in (-1, 1):
            sphere(f"{n}_eyew{sx}", "#FFFFFF", (sx*0.14, -0.36, 0.43), 0.085, (1, 0.45, 1.1), g, sub=1)
            sphere(f"{n}_eyep{sx}", INKC, (sx*0.14, -0.405, 0.42), 0.035, (1, 0.5, 1), g, sub=1)
        self.eyes["shock"] = g
        g = grp(n+"_e_happy")
        for sx in (-1, 1): arc_tube(f"{n}_eh{sx}", INKC, (sx*0.14, -0.385, 0.39), 0.05, 0.015, math.radians(20), math.radians(160), g)
        self.eyes["happy"] = g
        g = grp(n+"_e_closed")
        for sx in (-1, 1): arc_tube(f"{n}_ec{sx}", INKC, (sx*0.14, -0.385, 0.45), 0.05, 0.015, math.radians(200), math.radians(340), g)
        self.eyes["closed"] = g
        g = grp(n+"_e_dizzy")
        for sx in (-1, 1):
            pts = [(sx*0.14+math.cos(k*0.5)*k*0.0025, -0.39, 0.42+math.sin(k*0.5)*k*0.0025) for k in range(36)]
            poly_tube(f"{n}_ed{sx}", INKC, pts, 0.007, g)
        self.eyes["dizzy"] = g
        self.brow = {}
        for sx in (-1, 1):
            b = empty(f"{n}_brow{sx}", (sx*0.14, -0.37, 0.53), hd)
            cube(f"{n}_browm{sx}", "#B8862A" if davi else B_HAIR, (0, 0, 0), (0.12, 0.04, 0.03), b, bevel=0.014)
            self.brow[sx] = b
        g = grp(n+"_m_line"); arc_tube(n+"_ml", INKC, (0, -0.385, 0.29), 0.05, 0.013, math.radians(200), math.radians(340), g); self.mouths["line"] = g
        g = grp(n+"_m_smile")
        s = sphere(n+"_ms", "#7A1E2B", (0, -0.37, 0.25), 0.085, (1, 0.4, 0.75), g, sub=1); Leo._cut_upper(self, s, 0.25)
        sphere(n+"_tongue", "#E86A7A", (0, -0.38, 0.205), 0.04, (1, 0.4, 0.5), g, sub=1)
        self.mouths["smile"] = g
        g = grp(n+"_m_o"); sphere(n+"_mo", "#6B1E2A", (0, -0.385, 0.25), 0.045, (0.9, 0.35, 1.25), g, sub=1); self.mouths["o"] = g
        g = grp(n+"_m_yawn"); sphere(n+"_my", "#6B1E2A", (0, -0.38, 0.23), 0.085, (1.1, 0.35, 1.3), g, sub=1); self.mouths["yawn"] = g
        g = grp(n+"_m_wavy")
        poly_tube(n+"_mw", INKC, [(-0.06+i*0.015, -0.39, 0.27+(0.01 if i % 2 else -0.01)) for i in range(9)], 0.011, g); self.mouths["wavy"] = g
        g = grp(n+"_m_teeth"); cube(n+"_mt", "#FFFFFF", (0, -0.385, 0.27), (0.13, 0.03, 0.055), g, bevel=0.02); self.mouths["teeth"] = g
        g = grp(n+"_m_small"); sphere(n+"_msm", INKC, (0, -0.39, 0.27), 0.02, (1, 0.4, 0.8), g, sub=0); self.mouths["small"] = g
        # rabo: corrente de 7 segmentos presa atrás do quadril; cada um é filho do anterior (onda de balanço)
        self.tail = []
        if tail:
            par = empty(n+"_tailbase", (0, 0.2, 0.12), hp)
            par.rotation_euler = (math.radians(-60), 0, 0)
            for k in range(7):
                seg = empty(f"{n}_tl{k}", (0, 0, 0.0 if k == 0 else 0.11), par)
                r = 0.055 + 0.012*k if k < 6 else 0.1
                sphere(f"{n}_tls{k}", TAIL_TIP if k >= 5 else TAIL, (0, 0, 0.06), r, (1, 1, 1.3), seg, sub=1)
                self.tail.append(seg); par = seg
            self.tail_base = self.tail[0].parent

    def wag(self, t, amp=25, speed=10, curl=12, lift=0):
        """balança o rabo: amp em graus por segmento, speed em rad/s, curl = curvatura para cima."""
        if not self.tail: return
        self.tail_base.rotation_euler = (math.radians(-60 - lift), 0, 0)
        for k, s in enumerate(self.tail):
            s.rotation_euler = (math.radians(-curl), math.radians(amp*math.sin(t*speed - k*0.7)), 0)

class BiaCtl(look.LeoCtl):
    def __init__(self, name="bia", tail=False, style="bia"):
        self.L = Bia(name, tail, style)

def DaviCtl(name="davi"):
    return BiaCtl(name, False, "davi")

    def pose(self, t, *a, **k):
        super().pose(t, *a, **k)
        L = self.L
        L.shirt.scale = (1, 0.94, 1.39); L.shirt.location.z = 0.30
