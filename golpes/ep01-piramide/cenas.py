"""Cenas 3D do episódio 1 (pirâmide financeira). Uma função por plano: monta a cena e devolve
(frame(t), [objetos que as etiquetas seguem]). Tempos das falas vêm de roteiro.py (R.wt)."""
import math, bpy
import kit
from kit import *
import roteiro as R

BUILD = {}
def shot(f): BUILD[f.__name__] = f; return f

def street(cam_y=-7):
    setup("#8FD0F5")
    box("grass", "#C9E7A0", (40, 6, 0.2), (0, 0.5, -0.1), bevel=0)
    box("road", "#4A4D57", (40, 8, 0.2), (0, -6.5, -0.12), bevel=0)
    box("curb", "#D5D8DC", (40, 0.3, 0.18), (0, -2.45, 0.0), bevel=0.02)
    box("sky", "#8FD0F5", (80, 0.2, 60), (0, 30, 10), bevel=0)
    city("city", y=16)
    house("house", (0, 3.4, 0))

# ======================================================================= GANCHO
@shot
def s01(sh):
    street()
    h = hero("hero", (0, 0.6, 0))
    cam = camera(38)
    t_v = R.wt(sh, "rico")
    def f(t):
        h.pose(t, armR=0.15, armL=0.1); h.blink(t)
        h.expr("grin" if t > t_v else "smile")
        look(cam, keys(t, [(0, (0, -8.5, 2.2)), (sh["dur"], (0, -6.6, 1.9))]), (0, 0.6, 1.25))
    return f, ["hero"]

@shot
def s02(sh):
    street()
    h = hero("hero", (-0.9, -0.9, 0), rotz=-0.35)
    fr = [person(f"f{i}", i, (-0.9 + (i % 4) * 0.75 + (0.35 if (i // 4) % 2 else 0), 0.3 + (i // 4) * 0.9, 0), rotz=0.15) for i in range(10)]
    cam = camera(32)
    t_f, t_m = R.wt(sh, "amigos"), R.wt(sh, "mil")
    def f(t):
        h.pose(t, armR=1.3 if t > t_m else 0.2, armL=0.1); h.blink(t); h.expr("grin")
        for i, p in enumerate(fr):
            pop(p.root, t, 0.1 + i * 0.09, 0.25)
            p.pose(t, phase=i); p.blink(t, off=i * 0.37); p.expr("smile")
        look(cam, keys(t, [(0, (0.3, -9.6, 4.4)), (sh["dur"], (0.2, -8.4, 4.0))]), (0.2, 0.4, 1.2))
    return f, ["f2", "hero"]

@shot
def s03(sh):
    street()
    h = hero("hero", (-0.8, -0.9, 0), rotz=-0.3)
    fr = [person(f"f{i}", i, (-0.6 + (i % 3) * 0.85 + (0.4 if (i // 3) % 2 else 0), 0.4 + (i // 3) * 0.9, 0), rotz=0.25) for i in range(7)]
    cam = camera(34)
    t_q = R.wt(sh, "ganho")
    def f(t):
        h.pose(t, armR=0.2); h.blink(t); h.expr("o" if t > t_q + 0.2 else "smile")
        for i, p in enumerate(fr):
            cross = t > 0.3 + i * 0.05
            p.pose(t, armL=1.4 if cross else 0, armR=1.4 if cross else 0, armLs=-0.5 if cross else 0, armRs=-0.5 if cross else 0, phase=i)
            p.expr("flat", "angry"); p.blink(t, off=i * 0.3)
            p.head.rotation_euler = (0, 0.12 * math.sin(i), 0)
        look(cam, keys(t, [(0, (0.2, -8.6, 3.6)), (sh["dur"], (0.1, -7.4, 3.2))]), (0.1, 0.3, 1.3))
    return f, ["hero"]

# ======================================================================= helpers de cenário
def office(wall="#7CC6A4", floor="#E3CDB6"):
    setup("#7CC6A4")
    room(floor, wall, depth=3.5, base="#6B4F3A")
    for x in (-2.5, 2.5): box(f"lamp{x}", "#FFFFFF", (1.8, 0.4, 0.08), (x, 1.5, 4.6), bevel=0.02)
    box("window", "#EDEDED", (1.6, 0.1, 1.3), (3.0, 3.38, 2.4), bevel=0.03)
    box("windowg", "#A9DCF5", (1.4, 0.12, 1.1), (3.0, 3.36, 2.4), bevel=0.02)

def pushcam(cam, sh, a, b, target, lens=None):
    def f(t): look(cam, keys(t, [(0, a), (sh["dur"], b)]), target)
    return f

def steps(name, levels, w0=1.3, h=0.9, color="#E8B04A", depth=1.0):
    """Pirâmide de degraus (cada nível mais para a frente). levels = pessoas por nível, de cima para baixo.
    Devolve [(z, [x...], y)] com a altura do piso, as posições x e o y onde as pessoas ficam."""
    out, n = [], len(levels)
    for i, k in enumerate(levels):
        lvl = n - 1 - i
        width = k * w0 + 0.5
        d = depth * (i + 1) + 0.3
        z = lvl * h
        box(f"{name}_{i}", color if i % 2 == 0 else kit._shade(color, 0.9), (width, d, h), (0, 0.6 - d / 2, z + h / 2), bevel=0.05)
        xs = [(j - (k - 1) / 2) * w0 for j in range(k)]
        out.append((z + h, xs, 0.6 - d + 0.45))
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

# ======================================================================= DEGRAU 1
@shot
def s04(sh):
    office()
    h = hero("hero", (-0.85, 0.4, 0), rotz=-0.3)
    g = board("chart", (0.75, 2.0, 0), 1.9, 1.8, header="#27AE60", title="LUCRO", legs=True)
    bars = [box(f"bar{i}", "#27AE60", (0.3, 0.06, 0.25 + i * 0.3), (0.2 + i * 0.4, 1.92, 1.2 + (0.25 + i * 0.3) / 2), bevel=0.02) for i in range(4)]
    ar = arrow("arr", (0.0, 1.85, 1.45), 1.4, "#F39C12"); ar.rotation_euler = (0, -0.6, 0)
    cam = camera(34); c = pushcam(cam, sh, (0, -7.4, 2.4), (0, -6.3, 2.2), (0, 1.0, 1.5))
    t_p = R.wt(sh, "promete")
    def f(t):
        h.pose(t, armR=1.5 if t > t_p else 0.3, armRs=0.3 if t > t_p else 0, armL=0.1); h.blink(t); h.expr("grin")
        for i, b in enumerate(bars): pop(b, t, t_p + 0.15 * i, 0.3)
        pop(ar, t, t_p + 0.7, 0.35)
        c(t)
    return f, ["hero"]

@shot
def s05(sh):
    setup("#BFE8DA"); cyclo("#BFE8DA")
    h = hero("hero", (-0.9, -0.2, 0), rotz=-0.3)
    st = [coin_stack(f"cs{i}", 3 + i * 5, (0.0 + i * 0.6, 0.9 + i * 0.25, 0), r=0.26) for i in range(4)]
    cam = camera(34); c = pushcam(cam, sh, (0, -8.6, 2.6), (0, -7.4, 2.4), (0.1, 0.5, 1.5))
    def f(t):
        h.pose(t, armR=0.9, armRs=0.6, armL=0.1); h.blink(t); h.expr("grin")
        for i, s_ in enumerate(st):
            for j, cc in enumerate(s_.children):
                cc.hide_render = t < 0.1 + i * 0.12 + j * 0.03
        c(t)
    return f, ["hero"]

# ======================================================================= DEGRAU 2
@shot
def s06(sh):
    office()
    h = hero("hero", (-0.75, 0.1, 0), rotz=-0.35)
    sf = safe("safe", (0.75, 1.0, 0), "#8C969E")
    hinge = bpy.data.objects[sf["hinge"]]
    cam = camera(34); c = pushcam(cam, sh, (0, -7.8, 2.5), (0.05, -6.6, 2.3), (0.05, 0.6, 1.3))
    t_t = R.wt(sh, "tirar")
    def f(t):
        hinge.rotation_euler.z = -1.9 * smooth(ramp(t, 0.2, 0.6))
        scratch = t > t_t
        h.pose(t, armL=2.6 if scratch else 0.1, armLs=-0.3 if scratch else 0, armR=0.2,
               head=(0, 0.15 * math.sin(t * 6) if scratch else 0, 0)); h.blink(t)
        h.expr("o" if t > 0.6 else "smile")
        c(t)
    return f, ["safe", "hero"]

def ponzi_set(sh, wide=False):
    """Vertical: os NOVOS embaixo, na frente; o dinheiro sobe até os PRIMEIROS, num palco atrás."""
    setup("#D9CCF2"); cyclo("#D9CCF2")
    box("stage", "#B9A7E0", (3.4, 1.6, 1.6), (0, 2.2, 0.8), bevel=0.06)
    old = [person(f"o{i}", i + 5, (-0.8 + i * 1.6, 2.2, 1.6)) for i in range(2)]
    h = hero("hero", (0, 2.4, 1.6))
    chest = box("chest", "#8B5E3C", (1.0, 0.8, 0.7), (0, 0.3, 0.35), bevel=0.06)
    box("chestl", "#F1C40F", (0.22, 0.82, 0.18), (0, 0.3, 0.5), bevel=0.03)
    new = [person(f"n{i}", i + 1, (-1.1 + i * 1.1, -0.9, 0), rotz=0.0) for i in range(3)]
    empty("new", (0, -0.9, 2.5)); empty("old", (0, 2.2, 4.3))
    a1 = arrow("a1", (0.0, 0.9, 1.1), 1.2, "#2ECC71"); a1.rotation_euler = (0, -1.2, 0)
    bills = [bill(f"b{i}", s=0.9) for i in range(6)]
    return h, new, old, bills, (a1,)

@shot
def s07(sh):
    h, new, old, bills, ars = ponzi_set(sh)
    cam = camera(32); c = pushcam(cam, sh, (0, -9.4, 6.2), (0, -8.3, 5.6), (0, 0.8, 2.0))
    t_p, t_n = R.wt(sh, "primeiros"), R.wt(sh, "entrou")
    def f(t):
        h.pose(t, armL=0.6, armR=0.6); h.blink(t); h.expr("grin")
        for i, p in enumerate(new):
            p.pose(t, armR=1.2 if t > t_n - 0.3 else 0.2, phase=i); p.expr("smile"); p.blink(t, off=i)
        for i, p in enumerate(old):
            up = t > t_p + 0.6
            p.pose(t, armL=2.6 if up else 0.3, armR=2.6 if up else 0.3, phase=i)
            p.expr("grin" if up else "smile"); p.blink(t, off=i * 2)
        for i, b in enumerate(bills):
            k = ((t - 0.3 - i * 0.35) % 2.1) / 2.1
            x0 = (i % 3 - 1) * 1.1; x1 = -0.8 if i % 2 else 0.8
            b.location = (lerp(x0, x1, k), lerp(-0.9, 2.0, k), lerp(1.4, 3.4, k) + math.sin(k * math.pi) * 0.8)
            b.rotation_euler = (0, k * 6, 0); show(b, t > 0.3 + i * 0.35)
        pop(ars[0], t, t_p)
        c(t)
    return f, ["old", "new"]

@shot
def s08(sh):
    h, new, old, bills, ars = ponzi_set(sh)
    cam = camera(30); c = pushcam(cam, sh, (0, -11.4, 7.0), (0, -10.4, 6.4), (0, 0.8, 2.0))
    def f(t):
        h.pose(t, armLs=1.2, armRs=1.2, armL=0.2, armR=0.2); h.blink(t); h.expr("grin")
        for i, p in enumerate(new + old): p.pose(t, phase=i); p.expr("smile"); p.blink(t, off=i)
        for i, b in enumerate(bills):
            k = ((t + i * 0.35) % 2.1) / 2.1
            x0 = (i % 3 - 1) * 1.1; x1 = -0.8 if i % 2 else 0.8
            b.location = (lerp(x0, x1, k), lerp(-0.9, 2.0, k), lerp(1.4, 3.4, k) + math.sin(k * math.pi) * 0.8)
            b.rotation_euler = (0, k * 6, 0)
        c(t)
    return f, []

# ======================================================================= DEGRAU 3
@shot
def s09(sh):
    office(wall="#E9B9A8", floor="#D8C7B8")
    h = hero("hero", (0.9, -0.6, 0), rotz=0.25)
    for i in range(5):
        y = 0.0 + i * 0.7
        for x in (-1.0, -0.1):
            cyl(f"post{i}{x}", "#BDC3C7", 0.06, 1.0, (x, y, 0.5)); cyl(f"postb{i}{x}", "#7F8C8D", 0.2, 0.06, (x, y, 0.03))
            if i < 4: box(f"rope{i}{x}", "#C0392B", (0.05, 0.66, 0.05), (x, y + 0.35, 0.92), bevel=0.01)
    empty("queue", (-0.55, 1.4, 1.7))
    cam = camera(34); c = pushcam(cam, sh, (-0.1, -7.6, 3.2), (-0.1, -6.5, 2.9), (0.0, 0.6, 1.1))
    def f(t):
        h.pose(t, armL=0.2, armR=0.2, head=(0, 0, 0.5 * math.sin(t * 2.2))); h.blink(t); h.expr("o")
        c(t)
    return f, ["queue", "hero"]

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

@shot
def s10(sh):
    setup("#FBE7A1"); cyclo("#FBE7A1")
    ppl, tiers = pyramid_people([1, 2, 3], w0=1.1)
    empty("bonus", (0, tiers[0][2], tiers[0][0] + 2.6))
    coins = [coin(f"c{i}", r=0.18) for i in range(6)]
    cam = camera(32); c = pushcam(cam, sh, (0, -10.5, 5.0), (0, -9.4, 4.6), (0, -0.6, 2.0))
    t_b = R.wt(sh, "bônus")
    def f(t):
        for li, row in enumerate(ppl):
            for j, p in enumerate(row):
                pop(p.root, t, 0.05 + (len(ppl) - 1 - li) * 0.35 + j * 0.06, 0.3)
                p.pose(t, armL=2.5 if (li == 0 and t > t_b) else 0.1, armR=2.5 if (li == 0 and t > t_b) else 0.1, phase=j + li)
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
def s11(sh):
    setup("#FBE7A1"); cyclo("#FBE7A1")
    ppl, tiers = pyramid_people([1, 2, 3, 4], w0=1.0)
    cam = camera(30); c = pushcam(cam, sh, (0, -14.0, 6.4), (0, -12.6, 6.0), (0, -1.0, 2.6))
    def f(t):
        for li, row in enumerate(ppl):
            for j, p in enumerate(row):
                p.pose(t, armL=2.6 if li == 0 else 0.1, armR=2.6 if li == 0 else 0.1, phase=j + li)
                p.expr("grin" if li == 0 else "smile"); p.blink(t, off=j + li)
        c(t)
    return f, []

# ======================================================================= DEGRAU 4
@shot
def s12(sh):
    street()
    h = hero("hero", (0, -0.9, 0))
    ps = [person(f"p{i}", i, (-1.2 + (i % 3) * 1.2 + (0.6 if i >= 3 else 0), 0.4 + (i // 3) * 0.9, 0)) for i in range(5)]
    cam = camera(34); c = pushcam(cam, sh, (0, -7.6, 3.0), (0, -6.4, 2.7), (0, 0.0, 1.4))
    def f(t):
        h.pose(t, armL=0.2, armR=0.2); h.blink(t); h.expr("o" if t > 0.8 else "smile")
        for i, p in enumerate(ps):
            p.pose(t, phase=i, head=(0, 0, (-1 if p.root.location.x > 0 else 1) * 0.25))
            p.expr("flat", "angry"); p.blink(t, off=i * 0.5)
            for e in p.eyes: e.scale.z = 0.4
        c(t)
    return f, ["hero"]

@shot
def s13(sh):
    street()
    h = hero("hero", (-0.7, -1.0, 0), rotz=-0.2)
    cr = car("car", (0.6, 1.0, 0), rotz=0.5)
    ph = phone("phone", (0, 0, 0))
    bag = box("bag", "#2E86DE", (0.6, 0.35, 0.8), (-1.5, -0.4, 0.45), bevel=0.06)
    cam = camera(34); c = pushcam(cam, sh, (0, -8.4, 3.0), (-0.1, -7.2, 2.8), (-0.1, 0.0, 1.4))
    t_c, t_v, t_s = R.wt(sh, "carro"), R.wt(sh, "viagem"), R.wt(sh, "saque.")
    ph.parent = h.arms[1]; ph.location = (0, -0.14, -0.85); ph.rotation_euler = (math.pi, 0, 0)
    def f(t):
        up = t > t_s - 0.4
        h.pose(t, armR=2.8 if up else 0.4, armL=0.2); h.blink(t); h.expr("grin")
        show(ph, up)
        pop(cr, t, t_c - 0.1, 0.3); pop(bag, t, t_v, 0.25)
        c(t)
    return f, ["car", "phone"]

@shot
def s14(sh):
    setup("#F6C6D6"); cyclo("#F6C6D6")
    big = empty("bigphone", (0.3, 1.6, 0))
    box("bp_b", "#1E1E24", (2.4, 0.2, 4.4), (0, 0, 2.5), big, bevel=0.2)
    box("bp_s", "#FDFEFE", (2.1, 0.22, 3.8), (0, -0.01, 2.55), big, bevel=0.06)
    box("bp_h", "#2E86DE", (2.1, 0.24, 0.4), (0, -0.02, 4.25), big, bevel=0.04)
    text("bp_t", "@RICO.FACIL", "#FFFFFF", 0.22, (0, -0.15, 4.25), big)
    car("pcar", (0.3, 1.2, 2.3), rotz=0.3).scale = (0.42, 0.42, 0.42)
    text("bp_l", "R$ 50 MIL HOJE!", "#27AE60", 0.24, (0, -0.15, 1.6), big)
    hearts = [box(f"heart{i}", "#E74C3C", (0.28, 0.1, 0.28), (-0.9 + (i % 2) * 2.4, 0.9, 1.4 + (i // 2) * 1.2), rot=(0, 0.785, 0), bevel=0.06) for i in range(6)]
    h = hero("hero", (-0.9, -0.4, 0), rotz=-0.3)
    cam = camera(32); c = pushcam(cam, sh, (0, -10, 3.0), (0, -8.8, 2.9), (0.1, 1.0, 2.3))
    def f(t):
        h.pose(t, armR=1.4, armRs=0.4); h.blink(t); h.expr("grin")
        for i, hh in enumerate(hearts):
            pop(hh, t, 0.2 + i * 0.18, 0.25); hh.location.z = 1.4 + (i // 2) * 1.2 + 0.1 * math.sin(t * 3 + i)
        c(t)
    return f, []

# ======================================================================= DEGRAU 5
@shot
def s15(sh):
    office(wall="#A9C6E8", floor="#D9D4CC")
    h = hero("hero", (-0.75, 0.2, 0), rotz=-0.5)
    cop = person("cop", 0, (0.8, 0.0, 0), rotz=0.5, top="#24476B", pants="#1C2E45", hair_style="police", skin=kit.SKINS[2])
    box("clip", "#8B5E3C", (0.45, 0.05, 0.6), (0, -0.14, -0.7), cop.arms[0], bevel=0.02)
    box("clipp", "#FFFFFF", (0.38, 0.06, 0.48), (0, -0.15, -0.72), cop.arms[0], bevel=0.01)
    cam = camera(34); c = pushcam(cam, sh, (0, -7.6, 2.5), (0, -6.4, 2.3), (0, 0.3, 1.4))
    t_q = R.wt(sh, "vende?")
    def f(t):
        h.pose(t, armL=0.2, armR=0.2); h.blink(t); h.expr("o" if t > 0.6 else "smile")
        cop.pose(t, armL=1.3, armR=0.2 if t < t_q - 0.5 else 1.0, armRs=0 if t < t_q - 0.5 else 0.4); cop.blink(t, off=1)
        cop.expr("flat", "angry")
        c(t)
    return f, ["cop", "hero"]

@shot
def s16(sh):
    setup("#C7E6F7"); cyclo("#C7E6F7")
    table("tbl", (0.35, 0.8, 0), 2.4, 1.0, 0.85)
    cn = coin("coin", (-0.4, 0.8, 1.27), r=0.3)
    text("coin_t", "B", "#B9770E", 0.34, (0, 0, -0.04), cn, rot=(0, 0, 0))
    bk = book("book", (0.35, 0.8, 0.9))
    os_ = ostrich("ostrich", (1.05, 0.8, 0.9), rotz=0.3); os_.scale = (0.6, 0.6, 0.6)
    h = hero("hero", (-0.9, -0.6, 0), rotz=-0.4)
    cam = camera(32); c = pushcam(cam, sh, (0, -8.6, 2.9), (0.1, -7.4, 2.7), (0.2, 0.4, 1.5))
    t_c, t_k, t_a = R.wt(sh, "criptomoeda"), R.wt(sh, "curso"), R.wt(sh, "avestruz.")
    def f(t):
        h.pose(t, armR=1.4, armRs=0.6); h.blink(t); h.expr("grin")
        pop(cn, t, t_c - 0.1); pop(bk, t, t_k - 0.1); pop(os_, t, t_a - 0.15, 0.35)
        cn.rotation_euler = (math.pi / 2, 0, 0.35 * math.sin(t * 2))
        c(t)
    return f, ["coin", "book", "ostrich"]

@shot
def s17(sh):
    setup("#C7E6F7"); cyclo("#C7E6F7")
    fac = empty("fac", (0, 1.0, 0))
    box("fac_w", "#F5E6C8", (4.4, 0.12, 3.2), (0, 0, 1.6), fac, bevel=0.03)
    box("fac_s", "#E74C3C", (3.6, 0.2, 0.7), (0, -0.1, 2.9), fac, bevel=0.05)
    text("fac_t", "INVEST MAX", "#FFFFFF", 0.42, (0, -0.22, 2.9), fac)
    box("fac_d", "#2B2F33", (1.0, 0.14, 1.9), (0, -0.02, 0.95), fac, bevel=0.03)
    for x in (-1.5, 1.5):
        box(f"fac_win{x}", "#9AD3F0", (0.9, 0.14, 0.8), (x, -0.02, 1.5), fac, bevel=0.03)
        box(f"prop{x}", "#A0522D", (0.12, 0.12, 3.4), (x, 0.9, 1.4), fac, rot=(0.45, 0, 0), bevel=0.02)
    box("bucket", "#95A5A6", (0.35, 0.35, 0.35), (1.0, 1.4, 0.18), bevel=0.05)
    h = hero("hero", (-2.6, -0.3, 0), rotz=-0.2)
    cam = camera(32)
    def f(t):
        h.pose(t, armR=0.3); h.blink(t); h.expr("grin")
        a = lerp(-0.15, 0.95, smooth(ramp(t, 0.0, sh["dur"])))
        r = 10.0
        look(cam, (math.sin(a) * r, 1.0 - math.cos(a) * r, 3.0), (0, 1.0, 1.6))
    return f, []

# ======================================================================= VIRADA
def big_pyramid(levels=10, cube=0.32, seed=0):
    import random
    rnd = random.Random(seed); objs = []
    cols = [c["top"] for c in kit.CROWD]
    for lv in range(levels):
        n = 1 + lv * 2
        row = []
        for j in range(n):
            x = (j - (n - 1) / 2) * cube * 1.08
            z = (levels - 1 - lv) * cube * 1.5
            o = box(f"pp{lv}_{j}", rnd.choice(cols), (cube, cube, cube * 1.3), (x, 0, z + cube * 0.65), bevel=0.04)
            row.append(o)
        objs.append(row)
    return objs

@shot
def s18(sh):
    setup("#1F2A44"); cyclo("#1F2A44")
    L = 10
    objs = big_pyramid(L)
    cam = camera(32)
    t_tr, t_b = R.wt(sh, "traz"), R.wt(sh, "bilhões")
    def f(t):
        k = clamp((t - t_tr + 0.3) / (t_b - t_tr + 0.3))
        shown = 1 + int(k * (L - 1) + 0.0001) if t > t_tr - 0.3 else 1
        for lv, row in enumerate(objs):
            for o in row: o.hide_render = lv >= shown
        top_z = (L - 1) * 0.32 * 1.5 + 0.6
        frac = shown / L
        cz = top_z - frac * top_z / 2
        dist = 4 + frac * 9
        look(cam, (0, -dist, cz + 0.6), (0, 0, cz))
    return f, []

@shot
def s19(sh):
    setup("#1F2A44"); cyclo("#1F2A44")
    big_pyramid(10)
    globe("earth", (0, -1.5, 0.6), 0.6)
    cam = camera(30); c = pushcam(cam, sh, (0, -16, 4.0), (0, -14.2, 3.6), (0, 0, 2.4))
    gl = bpy.data.objects["earth"]
    def f(t):
        gl.rotation_euler.z = t * 0.6
        c(t)
    return f, []

@shot
def s20(sh):
    office(wall="#3B4A6B", floor="#2D3550")
    table("tbl", (0, 0.4, 0), 2.2, 1.1, 0.9)
    lp, lid = laptop("laptop", (0, 0.3, 0.95), screen="#C0392B")
    lid.rotation_euler.x = 0.25
    lid.location.y = 0.52
    text("lp_t1", "SAQUE", "#FFFFFF", 0.2, (0, -0.05, 0.66), lid)
    text("lp_t2", "BLOQUEADO", "#FFFFFF", 0.2, (0, -0.05, 0.42), lid)
    ps = [person(f"p{i}", i, (-1.0 + i * 1.0, 1.6 + (i % 2) * 0.3, 0)) for i in range(3)]
    cam = camera(34); c = pushcam(cam, sh, (0, -6.4, 2.8), (0, -5.3, 2.5), (0, 0.8, 1.6))
    t_s = R.wt(sh, "saques")
    def f(t):
        lid.rotation_euler.x = 0.25
        for i, p in enumerate(ps):
            mad = t > t_s
            p.pose(t, armL=2.8 if mad else 0.2, armR=2.8 if mad else 0.2, phase=i)
            p.expr("sad" if mad else "o"); p.blink(t, off=i)
        c(t)
    return f, ["laptop"]

@shot
def s21(sh):
    setup("#B7B9C4"); cyclo("#B7B9C4")
    ppl, tiers = pyramid_people([1, 2, 3], w0=1.1, color="#9EA3B0")
    h = ppl[0][0]
    bag = box("bag", "#27AE60", (0.5, 0.4, 0.55), (0, -0.05, -0.78), h.arms[1], bevel=0.12)
    bills = [bill(f"b{i}", s=0.8) for i in range(8)]
    cam = camera(32); c = pushcam(cam, sh, (0, -10.5, 5.0), (0, -9.4, 4.6), (0, -0.6, 2.0))
    t_p = R.wt(sh, "perde")
    def f(t):
        for li, row in enumerate(ppl):
            for j, p in enumerate(row):
                low = li == len(ppl) - 1
                p.pose(t, phase=j + li, armL=2.4 if (low and t > t_p) else 0.1, armR=2.4 if (low and t > t_p) else 0.1)
                p.expr("grin" if li == 0 else ("sad" if low else "flat")); p.blink(t, off=j)
        h.pose(t, armR=0.5, armL=2.6)
        for i, b in enumerate(bills):
            k = ((t + i * 0.3) % 1.6) / 1.6
            x0 = tiers[-1][1][i % 3]; z0 = tiers[-1][0] + 1.4; y0 = tiers[-1][2] - 0.4
            b.location = (lerp(x0, 0.4, k), lerp(y0, tiers[0][2] - 0.4, k), lerp(z0, tiers[0][0] + 1.0, k) + math.sin(k * math.pi) * 1.0)
            b.rotation_euler = (0, k * 7, 0)
        c(t)
    return f, []

# ======================================================================= IRONIA + FATO REAL
@shot
def s22(sh):
    setup("#F7C548"); cyclo("#F7C548")
    for i in range(14):
        x = (i % 7 - 3) * 1.2 + (0.4 if i >= 7 else 0); y = 1.5 + (i // 7) * 2.2
        coin_stack(f"cs{i}", 8 + (i * 7) % 12, (x, y, 0), r=0.45)
    coin_stack("pod", 6, (0, 0, 0), r=0.8)
    h = hero("hero", (0, 0, 0.55))
    conf, canim = confetti("conf", 110, (4, 2, 6))
    cam = camera(34); c = pushcam(cam, sh, (0, -7.8, 2.8), (0, -6.0, 2.4), (0, 0.5, 1.9))
    def f(t):
        h.pose(t, armL=2.7, armR=2.7, armLs=0.4, armRs=0.4, bob=3); h.blink(t); h.expr("grin")
        canim(t, 0.0)
        c(t)
    return f, []

@shot
def s23(sh):
    setup("#2C2F3A"); cyclo("#2C2F3A")
    h = hero("hero", (0, 0.4, 0))
    bars = empty("bars", (0, -0.4, 0))
    for i in range(9): cyl(f"bar{i}", "#9AA3AD", 0.06, 3.6, ((i - 4) * 0.42, 0, 1.8), bars)
    box("bart", "#7F8C8D", (3.9, 0.2, 0.2), (0, 0, 3.6), bars, bevel=0.03)
    box("barm", "#7F8C8D", (3.9, 0.16, 0.14), (0, 0, 1.9), bars, bevel=0.03)
    cam = camera(36); c = pushcam(cam, sh, (0, -7.0, 2.2), (0, -5.6, 2.0), (0, 0.4, 1.4))
    t_c = R.wt(sh, "crime")
    def f(t):
        bars.location.z = 5 * (1 - ease_out(ramp(t, t_c - 0.15, 0.25)))
        h.pose(t, armL=0.1, armR=0.1); h.blink(t); h.expr("sad" if t > t_c else "o")
        c(t)
    return f, []

@shot
def s24(sh):
    setup("#E9E4D8"); cyclo("#E9E4D8")
    k = 0
    for r in range(7):
        for cidx in range(11):
            mini(f"m{k}", k * 7 + r, ((cidx - 5) * 0.9 + (0.45 if r % 2 else 0), 1.0 + r * 1.0, 0), 0.85); k += 1
    gav = empty("gavel", (2.6, -1.2, 2.0))
    box("gv_h", "#6E4426", (0.9, 0.45, 0.45), (0, 0, 0.0), gav, bevel=0.08)
    box("gv_s", "#8B5E3C", (0.12, 0.12, 1.3), (0.0, 0, -0.65), gav, rot=(0, 0, 0), bevel=0.03)
    cam = camera(34); c = pushcam(cam, sh, (0, -9.0, 5.2), (0, -7.6, 4.6), (0, 2.2, 1.0))
    t_b = R.wt(sh, "bloquear")
    def f(t):
        gav.rotation_euler.y = -0.9 + 1.4 * back(ramp(t, t_b - 0.1, 0.18)) if t > t_b - 0.1 else -0.9
        show(gav, t > t_b - 0.6)
        c(t)
    return f, []

@shot
def s25(sh):
    setup("#BFE8DA"); cyclo("#BFE8DA")
    g = board("rule", (0.55, 1.2, 0), 2.2, 2.5, header="#E74C3C", title="REGRA SIMPLES",
              lines=["O LUCRO VEM", "DE QUEM", "ENTRA DEPOIS?", "!= PIRÂMIDE"], tsize=0.22, lsize=0.27)
    h = hero("hero", (-1.0, -0.3, 0), rotz=-0.3)
    cam = camera(32); c = pushcam(cam, sh, (0, -8.6, 2.9), (0.1, -7.6, 2.7), (0.1, 0.6, 1.9))
    def f(t):
        h.pose(t, armR=1.5, armRs=0.4); h.blink(t); h.expr("smile")
        c(t)
    return f, []

@shot
def s26(sh):
    setup("#F7C548"); cyclo("#F7C548")
    g = board("card", (0.55, 1.2, 0), 2.2, 2.4, header="#2E86DE", title="PROPOSTA",
              lines=["LUCRO GARANTIDO", "CHAME UM AMIGO", "!VOCÊ ENTRARIA?"], tsize=0.22, lsize=0.24)
    h = hero("hero", (-1.0, -0.3, 0), rotz=-0.3)
    cam = camera(32); c = pushcam(cam, sh, (0, -8.6, 2.9), (0.1, -7.8, 2.7), (0.1, 0.6, 1.9))
    def f(t):
        h.pose(t, armR=1.5, armRs=0.4); h.blink(t); h.expr("grin")
        c(t)
    return f, ["card"]

