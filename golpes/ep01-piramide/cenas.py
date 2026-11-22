"""Cenas 3D do episódio 1 (pirâmide financeira), tudo numa cidade: calçada na frente, rua com carros,
lojas e prédios atrás (blender/cidade.py). Uma função por plano: monta a cena e devolve
(frame(t), [objetos que as etiquetas seguem]). Tempos das falas vêm de roteiro.py (R.wt)."""
import math, bpy, random
import kit, cidade
from kit import *
import roteiro as R

BUILD = {}
def shot(f): BUILD[f.__name__] = f; return f

def pushcam(cam, sh, a, b, target, target2=None):
    def f(t):
        k = smooth(t / sh["dur"])
        look(cam, vlerp(a, b, k), vlerp(target, target2 or target, k))
    return f

def walk_in(p, t, x0, x1, t0, t1):
    """Personagem entra andando de x0 até x1 entre t0 e t1. Devolve a 'velocidade' do passo (0..1)."""
    k = clamp((t - t0) / (t1 - t0))
    p.root.location.x = lerp(x0, x1, ease_out(k))
    return 1.0 if 0 < k < 0.97 else 0.0

# ------------------------------------------------------------------ peças
def steps(name, levels, w0=1.3, h=0.9, color="#E8B04A", depth=1.0, y0=0.6):
    """Pirâmide de degraus (cada nível mais para a frente). Devolve [(z, [x...], y)]."""
    out, n = [], len(levels)
    for i, k in enumerate(levels):
        lvl = n - 1 - i
        width = k * w0 + 0.5
        d = depth * (i + 1) + 0.3
        z = lvl * h
        box(f"{name}_{i}", color if i % 2 == 0 else kit._shade(color, 0.9), (width, d, h), (0, y0 - d / 2, z + h / 2), bevel=0.05)
        xs = [(j - (k - 1) / 2) * w0 for j in range(k)]
        out.append((z + h, xs, y0 - d + 0.45))
    return out

def mini(name, i, loc, s=1.0):
    """Boneco simplificado (para multidões grandes)."""
    st = kit.CROWD[i % len(kit.CROWD)]
    g = empty(name, loc); g.scale = (s, s, s)
    box(name + "_l", st["pants"], (0.5, 0.26, 0.75), (0, 0, 0.375), g, bevel=0.04)
    box(name + "_t", st["top"], (0.7, 0.38, 0.75), (0, 0, 1.12), g, bevel=0.05)
    box(name + "_h", st["skin"], (0.56, 0.52, 0.54), (0, 0, 1.78), g, bevel=0.05)
    box(name + "_hr", st["hair"], (0.6, 0.56, 0.14), (0, 0.02, 2.06), g, bevel=0.04)
    for sx in (-1, 1): box(f"{name}_e{sx}", "#1E1B2E", (0.07, 0.02, 0.09), (sx * 0.12, -0.265, 1.82), g, bevel=0.01)
    return g

def crowd(prefix, rows, cols, y0, dx=0.9, dy=1.0, s=0.85, seed=0):
    rnd = random.Random(seed); out = []
    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2) * dx + (dx / 2 if r % 2 else 0) + rnd.uniform(-0.12, 0.12)
            g = mini(f"{prefix}{r}_{c}", r * 7 + c, (x, y0 + r * dy, 0), s)
            out.append((g, rnd.uniform(0, 6)))
    return out

def crowd_anim(items, t, amp=0.06):
    for g, ph in items:
        g.location.z = abs(math.sin(t * 5 + ph)) * amp
        g.rotation_euler.z = math.sin(t * 1.5 + ph) * 0.12

def pyramid_people(levels, w0=1.25, h=1.0, color="#E8B04A", hero_top=True):
    tiers = steps("st", levels, w0, h, color)
    ppl, k = [], 0
    for li, (z, xs, y) in enumerate(tiers):
        row = []
        for x in xs:
            if li == 0 and hero_top: p = hero("hero", (x, y, z))
            else: p = person(f"p{k}", k, (x, y, z)); k += 1
            row.append(p)
        ppl.append(row)
    return ppl, tiers

def big_pyramid(levels=10, cube=0.6, seed=0, y=0.0):
    rnd = random.Random(seed); objs = []
    cols = [c["top"] for c in kit.CROWD]
    for lv in range(levels):
        n = 1 + lv * 2
        row = []
        for j in range(n):
            x = (j - (n - 1) / 2) * cube * 1.08
            z = (levels - 1 - lv) * cube * 1.5
            row.append(box(f"pp{lv}_{j}", rnd.choice(cols), (cube, cube, cube * 1.3), (x, y, z + cube * 0.65), bevel=0.06))
        objs.append(row)
    return objs

# ======================================================================= GANCHO
@shot
def s01(sh):
    """GANCHO: começa colado no sorriso do golpista e recua rápido, revelando a rua tomada por gente
    (o "um milhão de brasileiros") e dinheiro caindo."""
    city = cidade.build(0, seed=3, cars=False, ped=False)
    coin_stack("pod", 7, (0, -1.0, 0), r=0.75)
    h = hero("hero", (0, -1.0, 0.63))
    cr = crowd("m", 9, 15, 0.4, seed=1)
    rain, ranim = money_rain("rain", 45, (4.5, 2.5, 7), s=0.9)
    rain.location.y = -1.0
    cam = camera(34)
    t_v = R.wt(sh, "você")
    def f(t):
        city(t)
        point = t > t_v - 0.1
        h.pose(t, armL=2.7 if not point else 0.25, armR=2.7 if not point else 1.55, armLs=0.3, armRs=0.3 if not point else 0,
               elbR=0.05 if point else 0.2, elbL=0.2, bob=3); h.blink(t); h.expr("grin")
        crowd_anim(cr, t)
        ranim(t, -2.0)
        k = 1 - (1 - clamp(t / 0.9)) ** 3          # recuo rápido nos primeiros 0,9 s
        d = lerp(1.6, 7.6, k) + 0.3 * t
        z = lerp(2.05, 3.8, k); tz = lerp(2.0, 2.4, k)
        look(cam, (0.0, -1.0 - d, z), (0, 0.4, tz))
    return f, ["hero"]

# ======================================================================= O GOLPE
@shot
def s04(sh):
    city = cidade.build(6, seed=5)
    h = hero("hero", (-0.8, -0.6, 0), rotz=-0.3)
    g = board("chart", (0.9, 0.3, 0), 1.9, 1.8, header="#27AE60", title="LUCRO", legs=True)
    bars = [box(f"bar{i}", "#27AE60", (0.3, 0.06, 0.25 + i * 0.3), (0.35 + i * 0.4, 0.22, 1.2 + (0.25 + i * 0.3) / 2), bevel=0.02) for i in range(4)]
    ar = arrow("arr", (0.15, 0.15, 1.45), 1.4, "#F39C12"); ar.rotation_euler = (0, -0.6, 0)
    cam = camera(34)
    c = pushcam(cam, sh, (0.1, -8.6, 2.8), (0.05, -7.4, 2.6), (0.05, 1.0, 1.7))
    t_p = R.wt(sh, "promete")
    def f(t):
        city(t)
        wk = walk_in(h, t, -2.6, -0.8, 0.0, 0.9)
        h.root.rotation_euler.z = -1.2 if wk else -0.3
        h.pose(t, armR=1.45 if t > t_p else 0.2, armRs=0.35 if t > t_p else 0, elbR=0.1 if t > t_p else 0.35,
               armL=0.1, walk=wk); h.blink(t); h.expr("grin")
        for i, b in enumerate(bars): pop(b, t, t_p + 0.15 * i, 0.3)
        pop(ar, t, t_p + 0.7, 0.35)
        c(t)
    return f, ["hero"]

@shot
def s07(sh):
    """Os NOVOS embaixo, na frente; o dinheiro sobe até os PRIMEIROS, num palco atrás."""
    city = cidade.build(-6, seed=7)
    box("stage", "#B9A7E0", (3.6, 1.7, 1.5), (0, 0.9, 0.75), bevel=0.06)
    box("stage_t", "#9B86D3", (3.7, 1.8, 0.12), (0, 0.9, 1.52), bevel=0.04)
    old = [person(f"o{i}", i + 5, (-0.85 + i * 1.7, 0.9, 1.58)) for i in range(2)]
    h = hero("hero", (0, 1.1, 1.58))
    box("chest", "#8B5E3C", (1.0, 0.8, 0.7), (0, -1.0, 0.35), bevel=0.06)
    box("chestl", "#F1C40F", (0.22, 0.82, 0.18), (0, -1.0, 0.5), bevel=0.03)
    new = [person(f"n{i}", i + 1, (-1.15 + i * 1.15, -2.3, 0)) for i in range(3)]
    empty("new", (0, -2.3, 2.5)); empty("old", (0, 0.9, 4.2))
    a1 = arrow("a1", (0.0, -0.4, 1.1), 1.2, "#2ECC71"); a1.rotation_euler = (0, -1.2, 0)
    bills = [bill(f"b{i}", s=0.9) for i in range(6)]
    cam = camera(32)
    c = pushcam(cam, sh, (0, -11.2, 6.2), (0, -10.0, 5.6), (0, 0.0, 2.4))
    t_p, t_n = R.wt(sh, "primeiros"), R.wt(sh, "entrou")
    def f(t):
        city(t)
        h.pose(t, armL=0.7, armR=0.7, armLs=0.3, armRs=0.3, bob=2); h.blink(t); h.expr("grin")
        for i, p in enumerate(new):
            give = t > t_n - 0.3 + i * 0.12
            p.pose(t, armR=1.3 if give else 0.2, elbR=0.1 if give else 0.35, phase=i); p.expr("smile"); p.blink(t, off=i)
        for i, p in enumerate(old):
            up = t > t_p + 0.6
            p.pose(t, armL=2.6 if up else 0.3, armR=2.6 if up else 0.3, phase=i, bob=2)
            p.expr("grin" if up else "smile"); p.blink(t, off=i * 2)
        for i, b in enumerate(bills):
            k = ((t - 0.3 - i * 0.35) % 2.1) / 2.1
            x0 = (i % 3 - 1) * 1.15; x1 = -0.85 if i % 2 else 0.85
            b.location = (lerp(x0, x1, k), lerp(-2.3, 0.7, k), lerp(1.4, 3.6, k) + math.sin(k * math.pi) * 0.8)
            b.rotation_euler = (0, k * 6, 0); show(b, t > 0.3 + i * 0.35)
        pop(a1, t, t_p)
        c(t)
    return f, ["old", "new"]

@shot
def s10(sh):
    city = cidade.build(3, seed=11)
    ppl, tiers = pyramid_people([1, 2, 3], w0=1.1)
    empty("bonus", (0, tiers[0][2], tiers[0][0] + 2.6))
    coins = [coin(f"c{i}", r=0.18) for i in range(6)]
    cam = camera(32)
    c = pushcam(cam, sh, (0, -12.0, 5.9), (0, -10.8, 5.5), (0, -0.4, 3.6))
    t_b = R.wt(sh, "bônus")
    def f(t):
        city(t)
        for li, row in enumerate(ppl):
            for j, p in enumerate(row):
                pop(p.root, t, 0.05 + (len(ppl) - 1 - li) * 0.35 + j * 0.06, 0.3)
                up = li == 0 and t > t_b
                p.pose(t, armL=2.5 if up else 0.1, armR=2.5 if up else 0.1, phase=j + li, bob=1.5)
                p.expr("grin" if li == 0 else "smile"); p.blink(t, off=j + li)
        for i, cn in enumerate(coins):
            k = ((t - t_b - i * 0.25) % 1.2) / 1.2
            x0 = tiers[-1][1][i % 3]; z0 = tiers[-1][0] + 1.6; y0 = tiers[-1][2] - 0.3
            cn.location = (lerp(x0, 0, k), lerp(y0, tiers[0][2] - 0.3, k), lerp(z0, tiers[0][0] + 1.6, k) + math.sin(k * math.pi) * 0.6)
            cn.rotation_euler = (math.pi / 2, 0, t * 6)
            show(cn, t > t_b + i * 0.25)
        c(t)
    return f, ["bonus"]

@shot
def s13(sh):
    city = cidade.build(-3, seed=13)
    h = hero("hero", (-0.7, -1.0, 0), rotz=-0.2)
    cr = car("car", (0.7, 3.0, 0), rotz=0.0, color="#D62828")       # importado, estacionando na rua
    ph = phone("phone", (0, 0, 0)); ph.parent = h.hands[1]; ph.location = (0, -0.14, -0.05); ph.rotation_euler = (math.pi, 0, 0)
    cam = camera(34)
    c = pushcam(cam, sh, (0.2, -8.8, 3.0), (0.0, -7.6, 2.8), (0.0, 1.0, 1.5))
    t_c, t_s = R.wt(sh, "carro"), R.wt(sh, "ninguém")
    def f(t):
        city(t)
        up = t > t_s - 0.2
        show_off = t_c < t < t_s
        h.pose(t, armR=2.7 if up else 0.4, elbR=0.6 if up else 0.35, armL=0.9 if show_off else 0.2,
               armLs=0.9 if show_off else 0, elbL=0.1); h.blink(t); h.expr("grin")
        show(ph, up)
        cr.location.x = lerp(6.0, 0.7, ease_out(ramp(t, t_c - 0.6, 0.8)))     # o carro chega e estaciona
        c(t)
    return f, ["car"]

# ======================================================================= A CONTA NÃO FECHA
@shot
def s18(sh):
    city = cidade.build(0, seed=17, night=True, ped=False)
    L = 10
    objs = big_pyramid(L, cube=0.6, y=-0.5)
    cam = camera(32)
    t_tr, t_b = R.wt(sh, "décimo"), R.wt(sh, "bilhões")
    top_z = (L - 1) * 0.6 * 1.5 + 1.2
    state = {"f": 0.1}
    def f(t):
        city(t)
        k = clamp((t - t_tr + 0.3) / (t_b - t_tr + 0.3))
        shown = 1 + int(k * (L - 1) + 0.0001) if t > t_tr - 0.3 else 1
        for lv, row in enumerate(objs):
            for o in row: o.hide_render = lv >= shown
        frac = max(0.1, lerp(1 / L, 1.0, smooth(k)) if t > t_tr - 0.3 else 0.1)   # câmera abre suave
        cz = top_z - frac * top_z / 2
        dist = 6 + frac * 16
        look(cam, (0, -0.5 - dist, cz + 1.0), (0, 2.0, cz))
    return f, []

@shot
def s19(sh):
    city = cidade.build(0, seed=17, night=True, ped=False)
    big_pyramid(10, cube=0.6, y=-0.5)
    globe("earth", (0, -4.6, 0.9), 0.9)
    cam = camera(30)
    c = pushcam(cam, sh, (0, -25, 6.0), (0, -22.5, 5.4), (0, 0, 4.4))
    gl = bpy.data.objects["earth"]
    def f(t):
        city(t)
        gl.rotation_euler.z = t * 0.6
        c(t)
    return f, []

@shot
def s20(sh):
    city = cidade.build(4, seed=19, night=True)
    table("tbl", (0, -0.6, 0), 2.2, 1.1, 0.9, color="#6D4C41")
    lp, lid = laptop("laptop", (0, -0.7, 0.95), screen="#C0392B")
    lid.rotation_euler.x = 0.25; lid.location.y = 0.52
    text("lp_t1", "SAQUE", "#FFFFFF", 0.2, (0, -0.05, 0.66), lid)
    text("lp_t2", "BLOQUEADO", "#FFFFFF", 0.2, (0, -0.05, 0.42), lid)
    ps = [person(f"p{i}", i, (-1.0 + i * 1.0, 0.5 + (i % 2) * 0.3, 0)) for i in range(3)]
    cam = camera(34)
    c = pushcam(cam, sh, (0, -7.6, 2.9), (0, -6.6, 2.6), (0, 0.4, 1.7))
    t_s = R.wt(sh, "saques")
    def f(t):
        city(t)
        for i, p in enumerate(ps):
            mad = t > t_s + i * 0.08
            p.pose(t, armL=2.8 if mad else 0.2, armR=2.8 if mad else 0.2, elbL=1.2 if mad else 0.35, elbR=1.2 if mad else 0.35, phase=i)
            p.expr("sad" if mad else "o"); p.blink(t, off=i)
        c(t)
    return f, ["laptop"]

@shot
def s21(sh):
    city = cidade.build(-4, seed=23)
    ppl, tiers = pyramid_people([1, 2, 3], w0=1.1, color="#9EA3B0")
    h = ppl[0][0]
    box("bag", "#27AE60", (0.5, 0.4, 0.55), (0, -0.05, -0.2), h.hands[1], bevel=0.12)
    bills = [bill(f"b{i}", s=0.8) for i in range(8)]
    cam = camera(32)
    c = pushcam(cam, sh, (0, -12.0, 5.9), (0, -10.8, 5.5), (0, -0.4, 3.6))
    t_p = R.wt(sh, "perde")
    def f(t):
        city(t)
        for li, row in enumerate(ppl):
            for j, p in enumerate(row):
                if li == 0: continue
                low = li == len(ppl) - 1
                mad = low and t > t_p + j * 0.06
                p.pose(t, phase=j + li, armL=2.4 if mad else 0.1, armR=2.4 if mad else 0.1, elbL=1.1 if mad else 0.35, elbR=1.1 if mad else 0.35)
                p.expr("sad" if low else "flat"); p.blink(t, off=j)
        h.pose(t, armR=0.5, armL=2.6, bob=2); h.expr("grin"); h.blink(t)
        for i, b in enumerate(bills):
            k = ((t + i * 0.3) % 1.6) / 1.6
            x0 = tiers[-1][1][i % 3]; z0 = tiers[-1][0] + 1.4; y0 = tiers[-1][2] - 0.4
            b.location = (lerp(x0, 0.4, k), lerp(y0, tiers[0][2] - 0.4, k), lerp(z0, tiers[0][0] + 1.0, k) + math.sin(k * math.pi) * 1.0)
            b.rotation_euler = (0, k * 7, 0)
        c(t)
    return f, []

# ======================================================================= FATO REAL + PERGUNTA
@shot
def s24(sh):
    city = cidade.build(0, seed=29, cars=False, ped=False)
    cr = crowd("m", 8, 13, -1.5, seed=4)
    gav = empty("gavel", (2.0, -4.0, 2.4))
    box("gv_h", "#6E4426", (0.9, 0.45, 0.45), (0, 0, 0.0), gav, bevel=0.08)
    box("gv_s", "#8B5E3C", (0.12, 0.12, 1.3), (0.0, 0, -0.65), gav, bevel=0.03)
    cam = camera(34)
    c = pushcam(cam, sh, (0, -10.5, 6.0), (0, -9.0, 5.3), (0, 1.5, 1.5))
    t_b = R.wt(sh, "bloquear")
    def f(t):
        city(t)
        crowd_anim(cr, t, amp=0.03 if t < t_b else 0.0)
        gav.rotation_euler.y = -0.9 + 1.4 * back(ramp(t, t_b - 0.1, 0.18)) if t > t_b - 0.1 else -0.9
        show(gav, t > t_b - 0.6)
        c(t)
    return f, []

@shot
def s26(sh):
    city = cidade.build(8, seed=31)
    board("card", (0.55, 0.2, 0), 2.2, 2.4, header="#2E86DE", title="PROPOSTA",
          lines=["LUCRO GARANTIDO", "CHAME UM AMIGO", "!VOCÊ ENTRARIA?"], tsize=0.22, lsize=0.24)
    h = hero("hero", (-1.0, -1.2, 0), rotz=-0.3)
    cam = camera(32)
    c = pushcam(cam, sh, (0, -9.6, 3.0), (0.1, -8.6, 2.8), (0.1, 0.6, 2.0))
    def f(t):
        city(t)
        h.pose(t, armR=1.45, armRs=0.4, elbR=0.1, armL=0.2 + 0.25 * max(0, math.sin(t * 3)), bob=1.5); h.blink(t); h.expr("grin")
        c(t)
    return f, ["card"]
