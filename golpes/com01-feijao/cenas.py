"""Cenas 3D do comercial do Feijão Gerente Ficou Louco, num supermercado (blender/mercado.py).
Uma função por plano: monta a cena e devolve (frame(t), [objetos que as etiquetas seguem])."""
import math, random, bpy
import kit, mercado
from kit import *
import roteiro as R

BUILD = {}
def shot(f): BUILD[f.__name__] = f; return f
P = R.PRODUTO

def pushcam(cam, sh, a, b, target, target2=None, ease=smooth):
    def f(t):
        k = ease(t / sh["dur"])
        look(cam, vlerp(a, b, k), vlerp(target, target2 or target, k))
    return f

def gerente(loc=(0, 0, 0), rotz=0.0):
    """O gerente: o protagonista de terno, com crachá GERENTE."""
    h = hero("hero", loc, rotz)
    box("cracha", "#FFFFFF", (0.2, 0.02, 0.11), (0.2, -0.205, 0.56), h.body, bevel=0.01)
    box("cracha_b", "#C62828", (0.2, 0.022, 0.03), (0.2, -0.207, 0.6), h.body, bevel=0.0)
    text("cracha_t", "GERENTE", "#1E1B2E", 0.035, (0.2, -0.22, 0.545), h.body)
    return h

# ------------------------------------------------------------------ a roda da confusão
RODA = 7
def face_in(a):
    """Rotação para quem está no ângulo `a` da roda olhar para o centro (frente local = -y)."""
    dx, dy = -math.sin(a), -math.cos(a)
    return math.atan2(dx, -dy)

def roda(center=(0, 0), r=1.15, seed=3):
    """Personagens em roda, virados para o centro, disputando o pacote."""
    ppl = []
    for i in range(RODA):
        a = i / RODA * 2 * math.pi + 0.3
        x, y = center[0] + math.sin(a) * r, center[1] + math.cos(a) * r
        rotz = face_in(a)                           # frente (-y local) aponta para o centro
        p = person(f"r{i}", i + seed, (x, y, 0), rotz=rotz)
        ppl.append((p, a))
    return ppl

def briga(ppl, t, k=1.0, center=(0, 0)):
    """Confusão: inclinam para o centro, braços tentando pegar, corpo chacoalhando."""
    for i, (p, a) in enumerate(ppl):
        ph = i * 1.7
        p.pose(t, armL=lerp(0.3, 2.3 + 0.5 * math.sin(t * 7 + ph), k), armR=lerp(0.3, 2.0 + 0.6 * math.sin(t * 7 + ph + 2.4), k),
               armLs=0.15 * k, armRs=0.15 * k, elbL=0.2, elbR=0.25, lean=0.22 * k, bob=2.5, phase=ph,
               head=(0, 0.15 * math.sin(t * 6 + ph) * k, 0))
        p.root.location.z = abs(math.sin(t * 8 + ph)) * 0.08 * k
        p.expr("o" if math.sin(t * 5 + ph) > 0 else "flat", "angry"); p.blink(t, off=ph)

def pack_disputa(pk, t, z0=2.45, center=(0, 0)):
    pk.location = (center[0] + 0.45 * math.sin(t * 2.3), center[1] + 0.35 * math.sin(t * 1.7 + 1), z0 + 0.22 * abs(math.sin(t * 4.5)))
    pk.rotation_euler = (0.3 * math.sin(t * 3.1), 0.4 * math.sin(t * 2.2), 0.9 * math.sin(t * 1.3))

def poeira(name, n=10, center=(0, 0)):
    """Nuvem de poeira de briga de desenho, no pé da roda."""
    items = []
    for i in range(n):
        o = sphere(f"{name}{i}", "#F4F6F7", 0.35, (0, 0, 0), scale=(1, 1, 0.8))
        items.append((o, i / n * 2 * math.pi))
    def anim(t, k=1.0):
        for o, a in items:
            aa = a + t * 2.2
            r = 1.5 + 0.15 * math.sin(t * 6 + a * 3)
            o.location = (center[0] + math.sin(aa) * r, center[1] + math.cos(aa) * r, 0.25 + 0.15 * abs(math.sin(t * 5 + a)))
            s = (0.45 + 0.3 * abs(math.sin(t * 4 + a * 2))) * k
            o.scale = (0.7 * s, 0.7 * s, 0.55 * s)
            o.hide_render = k < 0.05
    return anim

def cenario(with_roda=True):
    city = mercado.build(seed=2, produto=P)
    mercado.pallet("pal", (0, 2.6, 0), produto=P)
    sign = empty("oferta", (1.7, 2.3, 0))
    box("of_p", "#7F8C8D", (0.06, 0.06, 1.9), (0, 0, 0.95), sign, bevel=0.01)
    box("of_b", "#E53935", (1.1, 0.08, 0.7), (0, 0, 2.1), sign, bevel=0.06)
    text("of_t", "OFERTA", "#FFFFFF", 0.26, (0, -0.06, 2.2), sign)
    if P.get("preco"): text("of_pr", P["preco"], "#FFD23F", 0.2, (0, -0.06, 1.95), sign)
    out = {"city": city}
    if with_roda:
        out["roda"] = roda()
        out["pack"] = mercado.pacote("pack", (0, 0, 2.4), produto=P)
        out["poeira"] = poeira("dust")
    return out

# ======================================================================= 1. A DISPUTA
@shot
def f01(sh):
    S = cenario()
    cam = camera(32)
    def f(t):
        briga(S["roda"], t); pack_disputa(S["pack"], t); S["poeira"](t)
        k = 1 - (1 - clamp(t / sh["dur"])) ** 2.2        # começa de longe e entra na confusão
        look(cam, vlerp((0, -17, 6.5), (0.3, -6.0, 3.2), k), vlerp((0, 3, 2.0), (0, 0, 1.9), k))
    return f, ["pack"]

# ======================================================================= 2. ENTRA O GERENTE
@shot
def f02(sh):
    S = cenario()
    h = gerente((-3.2, -2.6, 0))
    cam = camera(32)
    c = pushcam(cam, sh, (-0.3, -8.4, 2.5), (-0.5, -7.3, 2.4), (-0.4, -1.0, 1.75))
    def f(t):
        briga(S["roda"], t); pack_disputa(S["pack"], t); S["poeira"](t, 0.6)
        k = clamp(t / 1.1)
        h.root.location.x = lerp(-3.2, -0.6, ease_out(k))
        wk = 1.0 if k < 0.95 else 0.0
        h.root.rotation_euler.z = lerp(-1.57, -0.1, smooth((t - 0.8) / 0.4))
        talking = h.talk(t, sh["words"])
        gest = t > R.wt(sh, "Baixou")
        h.pose(t, walk=wk, armR=1.2 if gest else 0.2, armRs=0.6 if gest else 0, elbR=0.5,
               armL=2.6 if t > R.wt(sh, "graça!") - 0.2 else 0.2, armLs=0.5, elbL=0.3, bob=2)
        h.blink(t)
        c(t)
    return f, ["hero"]

@shot
def f03(sh):
    S = cenario()
    h = gerente((-0.6, -2.6, 0), rotz=-0.1)
    cam = camera(34)
    c = pushcam(cam, sh, (-0.5, -6.6, 2.3), (-0.6, -5.6, 2.2), (-0.6, -2.0, 1.85))
    t_g, t_q = R.wt(sh, "gostoso,"), R.wt(sh, "qualidade")
    def f(t):
        briga(S["roda"], t); pack_disputa(S["pack"], t); S["poeira"](t)
        h.talk(t, sh["words"])
        thumbs = t > t_q
        h.pose(t, armR=1.6 if thumbs else (0.9 if t > t_g else 0.3), armRs=0.2, elbR=1.4 if thumbs else 0.6,
               armL=0.9 + 0.2 * math.sin(t * 3), armLs=0.4, elbL=0.8, bob=2,
               head=(0, 0, 0.25 if t < t_g else 0))       # olha para a roda, depois para a câmera
        h.blink(t)
        c(t)
    return f, ["hero"]

@shot
def f04(sh):
    S = cenario()
    big = mercado.pacote("bigpack", (0.55, -3.0, 0.0), s=3.2, produto=P)
    pot = empty("pot", (-0.85, -3.6, 0))
    cyl("pot_b", "#5D6D7E", 0.45, 0.55, (0, 0, 0.75), pot)
    cyl("pot_i", "#4A2418", 0.4, 0.56, (0, 0, 0.77), pot)
    box("pot_st", "#7F8C8D", (1.1, 1.1, 0.5), (0, 0, 0.25), pot, bevel=0.06)
    for sx in (-1, 1): box(f"pot_h{sx}", "#34495E", (0.18, 0.08, 0.08), (sx * 0.52, 0, 0.95), pot, bevel=0.02)
    steam = [sphere(f"st{i}", "#FFFFFF", 0.12, (0, 0, 0)) for i in range(6)]
    beans = [sphere(f"bean{i}", "#5D2E1F", 0.05, (0, 0, 0), scale=(1.3, 0.8, 0.9)) for i in range(18)]
    h = gerente((-1.5, -2.2, 0), rotz=-0.35)
    empty("b1", (0.55, -3.3, 2.4)); empty("b2", (-0.85, -3.6, 1.6)); empty("b3", (0.55, -3.3, 1.2))
    cam = camera(32)
    c = pushcam(cam, sh, (0.0, -10.0, 2.9), (0.0, -8.9, 2.7), (-0.1, -2.6, 1.6))
    t_g, t_s, t_r = R.wt(sh, "Grãos"), R.wt(sh, "sabor"), R.wt(sh, "rendimento")
    def f(t):
        briga(S["roda"], t); pack_disputa(S["pack"], t); S["poeira"](t)
        big.rotation_euler.z = 0.25 * math.sin(t * 1.1)
        pop(big, t, 0.05, 0.4)
        h.talk(t, sh["words"])
        h.pose(t, armR=1.3, armRs=0.7, elbR=0.1, armL=0.3, bob=2); h.blink(t)
        for i, b in enumerate(beans):          # grãos pulando do pacote para a panela
            k = ((t - t_g - i * 0.09) % 1.0)
            b.location = (lerp(0.3, -0.85, k), lerp(-3.2, -3.6, k), 2.2 + math.sin(k * math.pi) * 0.9 - k * 1.2)
            b.rotation_euler = (k * 8, k * 5, 0); b.hide_render = t < t_g + i * 0.09
        for i, s_ in enumerate(steam):
            k = ((t * 0.6 + i / 6) % 1.0)
            s_.location = (-0.85 + 0.15 * math.sin(t * 2 + i), -3.6, 1.15 + k * 1.3)
            sc = 0.12 + 0.12 * k; s_.scale = (2 * sc,) * 3; s_.hide_render = t < t_r - 0.3
        c(t)
    return f, ["b1", "b2", "b3"]

# ======================================================================= 3. OLHA A CONFUSÃO
@shot
def f05(sh):
    S = cenario()
    h = gerente((-1.55, -2.5, 0), rotz=0.35)
    cam = camera(32)
    c = pushcam(cam, sh, (-1.2, -8.6, 2.6), (-0.4, -5.6, 2.4), (-0.4, -0.6, 1.8), (0.0, 0.0, 1.9))
    t_o = R.wt(sh, "Olha")
    def f(t):
        briga(S["roda"], t); pack_disputa(S["pack"], t); S["poeira"](t)
        h.talk(t, sh["words"])
        h.pose(t, armR=1.35, armRs=1.0, elbR=0.05, armL=0.2, bob=2, head=(0, 0, 0.35 if int(t * 1.2) % 2 else 0)); h.blink(t)
        c(t)
    return f, ["hero"]

@shot
def f06(sh):
    """Eles percebem o gesto, congelam, olham... e pulam para trás correndo, de um jeito exagerado."""
    S = cenario()
    h = gerente((-1.55, -2.5, 0), rotz=0.35)
    cam = camera(32)
    c = pushcam(cam, sh, (0.0, -9.6, 3.4), (0.0, -9.0, 3.3), (0.0, 0.0, 1.5))
    t_fz, t_go = 0.25, 0.95
    pk = S["pack"]
    def f(t):
        S["poeira"](t, k=clamp(1 - t / 0.4))
        for i, (p, a) in enumerate(S["roda"]):
            if t < t_fz:
                briga([(p, a)], t)
                continue
            if t < t_go:                         # congela e olha para o gerente, chocado
                p.pose(t, armL=1.8, armR=1.6, elbL=0.2, elbR=0.2, lean=-0.05, bob=0, head=(0.1, 0, 0.5))
                p.expr("o", "up")
                for e in p.eyes: e.scale = (1.4, 1, 1.5)
                continue
            k = clamp((t - t_go) / 1.2)
            x0, y0 = math.sin(a) * 1.15, math.cos(a) * 1.15
            x1, y1 = FORA[i]
            e = ease_out(k)                      # salto para trás e corrida para as bordas
            p.root.location = (lerp(x0, x1 * 1.15, e), lerp(y0, y1 + 0.3, e), max(0, math.sin(clamp(k * 2.5) * math.pi) * 0.6))
            p.root.rotation_euler.z = lerp(face_in(a), face_to(x0, y0, x1 * 3, y1 * 3), smooth(k * 3))   # vira para onde corre
            p.pose(t, walk=1.8, armL=2.8, armR=2.8, armLs=0.6, armRs=0.6, bob=0)
            p.expr("o", "up")
        # o pacote cai no chão quando largam
        if t < t_fz: pack_disputa(pk, t)
        else:
            k = clamp((t - t_go) / 0.5)
            pk.location = (0, 0, 2.45 * (1 - k * k) if k < 1 else 0)
            pk.rotation_euler = (0, 0, (1 - k) * 2.0)
            if k >= 1: pk.location.z = abs(math.sin(clamp((t - t_go - 0.5) / 0.3) * math.pi)) * 0.15
        h.pose(t, armR=1.35 if t < t_go + 0.4 else 0.3, armRs=1.0 if t < t_go + 0.4 else 0.1, elbR=0.05, bob=1.5); h.expr("grin"); h.blink(t)
        c(t)
    return f, []

# ======================================================================= 4. O GERENTE PEGA O PACOTE
FORA = [(-3.0, -0.2), (-3.3, 1.6), (-2.0, 3.4), (-0.4, 4.4), (2.0, 3.4), (3.3, 1.6), (3.0, -0.2)]
def face_to(x, y, tx=0.0, ty=0.0):
    dx, dy = tx - x, ty - y
    return math.atan2(dx, -dy)

def fora(S):
    """Personagens já afastados, nas bordas e no fundo, olhando com inveja."""
    for i, (p, a) in enumerate(S["roda"]):
        x, y = FORA[i]
        p.root.location = (x, y, 0)
        p.root.rotation_euler.z = face_to(x, y)

@shot
def f07(sh):
    S = cenario()
    fora(S)
    h = gerente((-1.55, -2.5, 0), rotz=0.35)
    pk = S["pack"]; pk.location = (0, 0, 0)
    conf, canim = confetti("conf", 90, (3, 2, 5))
    cam = camera(30)
    t_walk, t_pick, t_up = 0.0, 1.2, 1.7
    def f(t):
        S["poeira"](t, k=0)
        for i, (p, a) in enumerate(S["roda"]):
            p.pose(t, armL=0.4, armR=0.4, elbL=1.0, elbR=1.0, bob=1, phase=i); p.expr("sad", "sad"); p.blink(t, off=i)
        k = clamp((t - t_walk) / t_pick)
        hx, hy = lerp(-1.55, -0.05, smooth(k)), lerp(-2.5, -0.55, smooth(k))
        h.root.location = (hx, hy, 0)
        h.root.rotation_euler.z = lerp(0.6, 0.0, smooth((t - 0.9) / 0.4))
        if t < t_pick:
            h.pose(t, walk=1.0, bob=1); h.expr("grin")
        elif t < t_up:                            # abaixa e pega
            h.pose(t, armL=0.9, armR=0.9, elbL=0.2, elbR=0.2, lean=0.5, bob=0); h.expr("grin")
        else:                                     # ergue acima da cabeça, como um troféu
            h.pose(t, armL=2.95, armR=2.95, armLs=0.15, armRs=0.15, elbL=0.15, elbR=0.15, bob=3); h.expr("grin")
        h.blink(t)
        if t < t_pick + 0.2:
            pk.location = (0, 0, 0); pk.rotation_euler = (0, 0, 0)
        else:
            u = smooth((t - t_pick - 0.2) / 0.5)
            pk.location = (hx, hy - 0.08, lerp(0.6, 2.12, u)); pk.rotation_euler = (0, 0, 0)
        canim(t, t_up)
        # câmera acompanha o gerente e termina baixa, olhando para cima (herói)
        q = smooth(t / sh["dur"])
        look(cam, vlerp((-0.8, -8.0, 2.6), (0.0, -5.4, 0.9), q), vlerp((-0.8, -1.0, 1.5), (0.0, -0.5, 2.2), q))
    return f, []

# ======================================================================= 5. FINAL
@shot
def f08(sh):
    S = cenario()
    fora(S)
    h = gerente((0, -0.6, 0))
    pk = S["pack"]
    pk.location = (0.22, -1.0, 1.0); pk.rotation_euler = (0, 0, -0.15)     # segura o pacote na frente do peito
    cam = camera(34)
    c = pushcam(cam, sh, (0.15, -5.4, 2.1), (0.2, -4.4, 2.0), (0.15, -0.6, 1.75))
    t_f = R.wt(sh, "Consegui")
    def f(t):
        S["poeira"](t, k=0)
        for i, (p, a) in enumerate(S["roda"]):
            p.pose(t, armL=0.4, armR=0.4, elbL=1.0, elbR=1.0, bob=1, phase=i); p.expr("sad", "sad"); p.blink(t, off=i)
        h.talk(t, sh["words"])
        h.pose(t, armR=0.9, armRs=0.0, elbR=1.1, armL=2.7 if t < t_f else 0.9, elbL=0.3 if t < t_f else 1.1, armLs=0.3 if t < t_f else 0.0, bob=2.5)
        pk.location.z = 1.0 + 0.03 * math.sin(t * 2.6)
        h.blink(t)
        c(t)
    return f, ["hero"]

@shot
def f09(sh):
    """Close cinematográfico da embalagem: pacote gigante girando num pedestal, raios de luz e confete."""
    S = cenario(with_roda=False)
    ped = cyl("ped", "#C62828", 1.25, 0.5, (0, -1.0, 0.25), verts=40)
    cyl("ped2", "#FFD23F", 1.32, 0.12, (0, -1.0, 0.52), verts=40)
    big = mercado.pacote("bigpack", (0, -1.0, 0.58), s=4.2, produto=P)
    rays = empty("rays", (0, 0.2, 1.9))
    for i in range(12):
        box(f"ray{i}", "#FFE082" if i % 2 else "#FFF3C4", (0.35, 0.05, 6.0), (0, 0, 0), rays, rot=(0, i * math.pi / 12, 0), bevel=0)
    beans = [sphere(f"bn{i}", random.Random(i).choice(["#5D2E1F", "#6E3B26"]), 0.08,
                    (math.sin(i * 0.9) * (1.5 + (i % 3) * 0.2), -1.4 + math.cos(i * 0.9) * 0.6, 0.05), scale=(1.3, 0.8, 0.8)) for i in range(26)]
    side = [mercado.pacote(f"sp{i}", ((-1) ** i * (1.7 + (i // 2) * 0.55), -0.6 + (i // 2) * 0.3, 0), s=1.4, produto=P,
                           rot=(0, 0, (-1) ** i * 0.3)) for i in range(4)]
    conf, canim = confetti("conf", 80, (3, 1.5, 6))
    cam = camera(36)
    def f(t):
        rays.rotation_euler.y = t * 0.25
        big.rotation_euler.z = 0.35 * math.sin(t * 0.9)
        big.location.z = 0.58 + 0.05 * math.sin(t * 2)
        canim(t, 0.0)
        q = smooth(t / sh["dur"])
        look(cam, vlerp((0.9, -10.2, 2.3), (0.0, -8.4, 2.1), q), (0, -1.0, 2.0 + 0.1 * q))
    return f, []
