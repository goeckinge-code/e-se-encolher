"""Cenas 3D do episódio 2 (cartão clonado). Uma função por plano: monta a cena e devolve
(frame(t), [objetos que as etiquetas seguem]). Tempos das falas vêm de roteiro.py (R.wt).
Aqui o cara de terno é o golpista ("ele") e o espectador é a vítima."""
import math, bpy
import kit
from kit import *
import roteiro as R

BUILD = {}
def shot(f): BUILD[f.__name__] = f; return f

def pushcam(cam, sh, a, b, target):
    def f(t): look(cam, keys(t, [(0, a), (sh["dur"], b)]), target)
    return f

# ------------------------------------------------------------------ objetos deste episódio
def card(name, loc=(0, 0, 0), parent=None, rot=(math.pi / 2, 0, 0), color="#2E86DE", s=1.0, blank=False):
    """Cartão de banco (em pé, de frente para a câmera)."""
    g = empty(name, loc, parent, rot)
    w, h = 0.86 * s, 0.54 * s
    box(name + "_b", "#F4F6F7" if blank else color, (w, h, 0.03 * s), (0, 0, 0), g, bevel=0.03 * s)
    if not blank:
        box(name + "_chip", "#F1C40F", (0.13 * s, 0.1 * s, 0.035 * s), (-0.25 * s, 0.02 * s, 0.0), g, bevel=0.015 * s)
        box(name + "_num", "#FFFFFF", (0.55 * s, 0.035 * s, 0.035 * s), (0.0, -0.12 * s, 0.0), g, bevel=0.005)
        box(name + "_logo", "#E74C3C", (0.1 * s, 0.08 * s, 0.035 * s), (0.31 * s, -0.17 * s, 0.0), g, bevel=0.02 * s)
    box(name + "_tarja", "#1E1E24", (w, 0.1 * s, 0.032 * s), (0, 0.16 * s, -0.001), g, bevel=0.0)
    return g

def atm(name, loc=(0, 0, 0), parent=None):
    """Caixa eletrônico: corpo, tela, teclado, entrada do cartão."""
    g = empty(name, loc, parent)
    box(name + "_body", "#5D6D7E", (1.5, 0.9, 2.3), (0, 0, 1.15), g, bevel=0.06)
    box(name + "_top", "#2E86DE", (1.55, 0.95, 0.4), (0, 0, 2.4), g, bevel=0.06)
    text(name + "_tt", "24H", "#FFFFFF", 0.26, (0, -0.49, 2.4), g)
    box(name + "_scr", "#1B2631", (0.9, 0.06, 0.6), (0, -0.46, 1.75), g, bevel=0.03)
    box(name + "_scr2", "#5DADE2", (0.8, 0.065, 0.5), (0, -0.465, 1.75), g, bevel=0.02)
    box(name + "_shelf", "#85929E", (1.2, 0.5, 0.1), (0, -0.62, 1.1), g, rot=(0.25, 0, 0), bevel=0.03)
    for r in range(4):
        for c in range(3):
            box(f"{name}_k{r}{c}", "#ECF0F1", (0.14, 0.05, 0.1), (-0.17 + c * 0.17, -0.86, 1.2 - r * 0.0 + 0.0), g, bevel=0.02).location.y = -0.7 - r * 0.035
    for r in range(4):
        for c in range(3):
            o = bpy.data.objects[f"{name}_k{r}{c}"]; o.location.z = 1.2 - r * 0.035 + r * 0.0; o.location.x = -0.17 + c * 0.17; o.location.y = -0.62 - r * 0.12
            o.rotation_euler = (0.25, 0, 0); o.location.z = 1.16 + r * -0.03 + 0.06
    box(name + "_slot", "#17202A", (0.36, 0.06, 0.06), (0.45, -0.47, 1.38), g, bevel=0.01)
    return g

def skimmer(name, loc, parent=None):
    """O 'chupa-cabra': uma peça falsa colada por cima da entrada do cartão."""
    g = empty(name, loc, parent)
    box(name + "_b", "#7F8C8D", (0.5, 0.22, 0.2), (0, 0, 0), g, bevel=0.05)
    box(name + "_s", "#17202A", (0.38, 0.23, 0.05), (0, -0.005, 0), g, bevel=0.01)
    box(name + "_led", "#E74C3C", (0.05, 0.235, 0.05), (0.18, -0.005, 0.06), g, bevel=0.01)
    return g

def spycam(name, loc, parent=None):
    g = empty(name, loc, parent)
    box(name + "_b", "#2C2C2C", (0.5, 0.25, 0.12), (0, 0, 0), g, bevel=0.03)
    cyl(name + "_lens", "#111111", 0.05, 0.06, (0.1, -0.12, -0.03), g, rot=(math.pi / 2, 0, 0))
    rec = box(name + "_rec", "#FF3B30", (0.05, 0.05, 0.05), (-0.15, -0.13, 0.0), g, bevel=0.02)
    return g, rec

def bag(name, loc, color="#E67E22", parent=None):
    g = empty(name, loc, parent)
    box(name + "_b", color, (0.55, 0.3, 0.6), (0, 0, 0.3), g, bevel=0.04)
    box(name + "_h", kit._shade(color, 0.7), (0.3, 0.04, 0.2), (0, 0, 0.68), g, bevel=0.03)
    return g

def street_atm(bg="#F2D7B6"):
    setup("#8FD0F5")
    box("floor", "#D5D8DC", (40, 14, 0.2), (0, 2, -0.1), bevel=0)
    box("wall", "#E8C39E", (40, 0.2, 10), (0, 2.0, 5), bevel=0)
    box("band", "#C0392B", (40, 0.25, 0.5), (0, 1.88, 3.4), bevel=0.02)
    text("bank", "BANCO", "#FFFFFF", 0.38, (0, 1.74, 3.4))

# ======================================================================= GANCHO
@shot
def c01(sh):
    """Começa no cartão da vítima bem de perto: ele passa por um leitor e um clone pula para fora.
    A câmera recua e mostra o golpista rindo com o clone na mão."""
    setup("#6C5CE7"); cyclo("#6C5CE7")
    h = hero("hero", (0.15, 0.4, 0))
    orig = card("orig", (0, 0, 0), color="#2E86DE", s=1.0)
    clone = card("clone", (0, 0, 0), color="#2E86DE", s=1.0)
    clone_tag = empty("clonetag", (0, 0, 0))
    rd = skimmer("reader", (-0.3, -0.8, 1.55)); rd.rotation_euler = (0, 0, math.pi / 2)
    cam = camera(34)
    t_tres = R.wt(sh, "três")
    def f(t):
        h.pose(t, armR=1.25, armL=0.15, bob=2); h.blink(t); h.expr("grin")
        # cartão original desliza pela leitora (0–0.5 s) e sai voando
        k = clamp(t / 0.5)
        orig.location = (-0.3, -0.85, lerp(2.3, 1.55, k)); orig.rotation_euler = (math.pi / 2, 0, 0)
        if t > 0.5:
            orig.location = (lerp(-0.3, -2.6, clamp((t - 0.5) / 0.5)), -0.85, 1.55 + (t - 0.5) * 1.2)
        # o clone surge (pop) e pula para a mão direita do golpista
        pop(clone, t, 0.45, 0.3)
        kk = smooth((t - 0.6) / 0.6)
        hand = h.arms[1].matrix_world.translation if False else None
        clone.location = (lerp(-0.3, 0.65, kk), lerp(-0.85, -0.25, kk), lerp(1.3, 1.75, kk) + math.sin(kk * math.pi) * 0.5)
        clone.rotation_euler = (math.pi / 2, kk * math.pi * 2, 0)
        # câmera: colada no cartão, recua rápido e continua abrindo devagar
        q = 1 - (1 - clamp((t - 0.35) / 0.9)) ** 3
        look(cam, (lerp(-0.3, 0.1, q), lerp(-2.6, -7.2, q) - 0.25 * t, lerp(1.75, 2.4, q)), (lerp(-0.3, 0.15, q), 0, lerp(1.75, 1.5, q)))
    return f, []

# ======================================================================= COMO FUNCIONA
@shot
def c02(sh):
    street_atm()
    a = atm("atm", (0, 1.0, 0))
    sk = skimmer("skim", (0, 0, 0))
    h = hero("hero", (1.0, -0.3, 0), rotz=0.9)
    cam = camera(32); c = pushcam(cam, sh, (-0.3, -6.6, 2.5), (-0.2, -5.7, 2.3), (0.4, 0.5, 1.4))
    t_c = R.wt(sh, "cola")
    slot = (0.45, 0.48, 1.38)
    def f(t):
        k = smooth(ramp(t, t_c - 0.1, 0.8))
        sk.location = (lerp(1.0, slot[0], k), lerp(-0.5, slot[1] - 0.02, k), lerp(1.35, slot[2], k))
        h.pose(t, armR=1.5 if k < 1 else 0.3, armRs=-0.3, armL=0.15); h.blink(t); h.expr("grin")
        h.head.rotation_euler = (0, 0, 0.3 * math.sin(t * 3) if t > t_c + 1.0 else 0)
        c(t)
    return f, ["skim"]

@shot
def c03(sh):
    street_atm()
    a = atm("atm", (0, 1.0, 0))
    skimmer("skim", (0.45, 0.46, 1.38))
    v = person("vit", 5, (-0.35, -0.45, 0), rotz=math.pi + 0.35)
    cd = card("vcard", (0, 0, 0), s=0.5)
    bits = [card(f"bit{i}", s=0.18, color="#5DADE2") for i in range(6)]
    cam = camera(34); c = pushcam(cam, sh, (1.7, -5.4, 2.8), (1.5, -4.7, 2.6), (0.4, 0.4, 1.6))
    t_p, t_cp = R.wt(sh, "passa"), R.wt(sh, "copiada.")
    def f(t):
        v.pose(t, armR=1.3 if t > t_p - 0.3 else 0.2, armL=0.1)
        k = smooth(ramp(t, t_p, 0.6))
        cd.location = (0.45, lerp(-0.2, 0.44, k), 1.4); cd.rotation_euler = (0, 0, math.pi / 2)
        show(cd, t > t_p - 0.3)
        for i, b in enumerate(bits):
            kk = ((t - t_p - 0.4 - i * 0.18) % 1.3) / 1.3
            b.location = (0.45 + kk * 1.6, 0.2 - kk * 0.4, 1.45 + kk * 1.9); b.rotation_euler = (math.pi / 2, kk * 4, 0)
            show(b, t > t_p + 0.4 + i * 0.18)
        c(t)
    return f, ["atm"]

@shot
def c04(sh):
    street_atm()
    a = atm("atm", (0, 1.0, 0))
    cam_, rec = spycam("spycam", (0.0, 0.6, 2.18))
    arm = empty("hand", (0.0, 0.05, 1.32))
    box("hand_m", "#D9A07A", (0.2, 0.3, 0.14), (0, 0, 0), arm, bevel=0.04)
    box("hand_f", "#D9A07A", (0.06, 0.18, 0.06), (0.02, 0.18, -0.03), arm, bevel=0.02)
    box("sleeve", "#A07856", (0.26, 0.6, 0.24), (0, -0.4, 0.02), arm, bevel=0.05)
    cam = camera(30); c = pushcam(cam, sh, (-0.9, -3.4, 2.4), (-0.75, -2.8, 2.25), (0.0, 0.6, 1.75))
    t_c = R.wt(sh, "câmera")
    def f(t):
        arm.location = (-0.17 + 0.17 * (int(t * 4) % 3), 0.05 + 0.02 * math.sin(t * 20), 1.32 + 0.03 * abs(math.sin(t * 12)))
        rec.hide_render = (int(t * 3) % 2) == 1
        pop(cam_, t, t_c - 0.2, 0.3)
        c(t)
    return f, ["spycam"]

@shot
def c05(sh):
    setup("#E3D6F5"); cyclo("#E3D6F5")
    table("tbl", (0, 0.6, 0), 2.4, 1.0, 0.85)
    lp, lid = laptop("laptop", (-0.6, 0.65, 0.9), screen="#2ECC71"); lp.scale = (0.7, 0.7, 0.7)
    lid.rotation_euler.x = 0.2
    wr = empty("writer", (0.3, 0.55, 0.9))
    box("wr_b", "#34495E", (0.7, 0.45, 0.22), (0, 0, 0.11), wr, bevel=0.05)
    box("wr_s", "#17202A", (0.6, 0.06, 0.05), (0, 0, 0.23), wr, bevel=0.01)
    blank = card("blank", s=0.55, blank=True)
    done = card("done", s=0.55, color="#2E86DE")
    h = hero("hero", (0.95, 1.45, 0), rotz=0.25)
    cam = camera(32); c = pushcam(cam, sh, (0, -6.8, 3.0), (0, -5.8, 2.8), (0.15, 0.6, 1.5))
    t_g, t_b = R.wt(sh, "grava"), R.wt(sh, "branco,")
    def f(t):
        h.pose(t, armL=0.9, armR=0.9); h.blink(t); h.expr("grin")
        k = smooth(ramp(t, t_g - 0.2, 0.6))
        y = lerp(-0.3, 0.55, k)
        for cd in (blank, done):
            cd.location = (0.3, y, 1.25 + (1 - k) * 0.5); cd.rotation_euler = (math.pi / 2, 0, 0)
        out = smooth(ramp(t, t_b + 0.1, 0.5))
        sw = t > t_b
        show(blank, not sw); show(done, sw)
        if sw: done.location = (0.3, lerp(0.55, -0.4, out), 1.25 + out * 0.9); done.rotation_euler = (math.pi / 2, 0, out * 0.3)
        c(t)
    return f, []

@shot
def c06(sh):
    setup("#FFD6A5"); cyclo("#FFD6A5")
    h = hero("hero", (0, 0.2, 0))
    bags = [bag(f"bag{i}", (-1.1 + i * 0.7, -0.4 + (i % 2) * 0.5, 0), col) for i, col in enumerate(["#E74C3C", "#9B59B6", "#16A085", "#F39C12"])]
    rain, ranim = money_rain("rain", 26, (2.2, 1.5, 5.0), s=0.8)
    cd = card("ccard", s=0.4); cd.parent = h.arms[1]; cd.location = (0, -0.15, -0.85)
    cam = camera(32); c = pushcam(cam, sh, (0, -6.8, 2.6), (0, -5.8, 2.4), (0, 0.2, 1.5))
    t_c, t_s = R.wt(sh, "compras"), R.wt(sh, "saques")
    def f(t):
        h.pose(t, armR=2.6, armL=0.3 if t < t_s else 2.4, bob=2); h.blink(t); h.expr("grin")
        for i, b in enumerate(bags): pop(b, t, t_c - 0.1 + i * 0.12, 0.25)
        ranim(t, t_s - 2.0); show(rain, t > t_s)
        for o in rain.children_recursive: o.hide_render = o.hide_render or t < t_s
        c(t)
    return f, ["hero"]

# ======================================================================= VIRADA + PROTEÇÃO
@shot
def c07(sh):
    setup("#BFE8DA"); cyclo("#BFE8DA")
    big = card("big", (0, 0.6, 2.0), s=3.0, color="#2E86DE")
    shield = empty("shield", (0, -0.2, 2.05))
    box("sh_b", "#27AE60", (1.0, 0.15, 1.15), (0, 0, 0), shield, bevel=0.3)
    box("sh_c", "#FFFFFF", (0.14, 0.17, 0.55), (0, 0, 0), shield, bevel=0.04)
    box("sh_c2", "#FFFFFF", (0.55, 0.17, 0.14), (0, 0, 0.05), shield, bevel=0.04)
    sk = skimmer("skim", (0, 0, 0))
    cam = camera(32); c = pushcam(cam, sh, (0, -7.2, 2.4), (0, -6.2, 2.3), (0, 0.4, 1.9))
    t_ch, t_cp = R.wt(sh, "chip"), R.wt(sh, "copiar.")
    def f(t):
        big.rotation_euler = (math.pi / 2, 0, 0.15 * math.sin(t * 1.5))
        pop(shield, t, t_ch + 0.6, 0.35)
        k = ramp(t, t_cp - 0.9, 0.9)
        bounce = math.sin(clamp(k) * math.pi) * 0.25
        sk.location = (lerp(2.4, 0.75, smooth(k)) + (0.3 if t > t_cp else 0) * (t - t_cp) * 3, -0.4, 1.4 + bounce)
        sk.rotation_euler = (0, 0, (t - t_cp) * 6 if t > t_cp else 0)
        c(t)
    return f, []

@shot
def c08(sh):
    street_atm()
    a = atm("atm", (0, 1.0, 0))
    v = person("vit", 6, (-0.1, -0.35, 0), rotz=math.pi)
    hand = empty("hand", (0.0, 0.26, 1.42))
    box("hand_m", "#B97A54", (0.42, 0.3, 0.08), (0, 0, 0), hand, rot=(0.25, 0, 0), bevel=0.03)
    ph = phone("phone", (0, 0, 0), screen="#27AE60"); ph.scale = (1.6, 1.6, 1.6)
    cam = camera(32); c = pushcam(cam, sh, (1.8, -5.8, 3.0), (1.6, -5.0, 2.8), (0.2, 0.2, 1.8))
    t_c, t_a = R.wt(sh, "cubra"), R.wt(sh, "alerta")
    def f(t):
        v.pose(t, armL=1.5 if t > t_c - 0.2 else 0.1, armR=0.2 if t < t_a - 0.3 else 2.0)
        hand.hide_render = t < t_c - 0.1
        ph.location = (0.55, -0.9, 2.75 + 0.05 * math.sin(t * 4)); ph.rotation_euler = (0, 0, -0.2)
        pop(ph, t, t_a - 0.2, 0.3)
        c(t)
    return f, ["hand", "phone"]

@shot
def c09(sh):
    setup("#F6C6D6"); cyclo("#F6C6D6")
    g = board("alert", (0, 1.0, 0), 2.3, 2.6, header="#E74C3C", title="BANCO",
              lines=["COMPRA DE", "R$ 4.800", "FOI VOCÊ?", "!BLOQUEAR"], tsize=0.24, lsize=0.3, legs=False)
    g.location.z = 0.3
    btn = box("btn", "#E74C3C", (1.4, 0.12, 0.38), (0, 0.9, 0.85), bevel=0.08)
    text("btn_t", "BLOQUEAR", "#FFFFFF", 0.22, (0, 0.82, 0.85))
    v = person("vit", 2, (-1.05, -0.4, 0), rotz=-0.4)
    cam = camera(32); c = pushcam(cam, sh, (0, -7.4, 2.4), (0, -6.4, 2.3), (0, 0.6, 1.7))
    t_b = R.wt(sh, "Bloqueie")
    def f(t):
        press = t > t_b
        v.pose(t, armR=1.4 if press else 0.3, armRs=0.4 if press else 0); v.expr("o" if t < t_b else "smile"); v.blink(t)
        btn.location.y = 0.9 + (0.05 if (press and t < t_b + 0.25) else 0)
        c(t)
    return f, []

@shot
def c10(sh):
    setup("#F7C548"); cyclo("#F7C548")
    g = board("card", (0.55, 1.2, 0), 2.2, 2.3, header="#2E86DE", title="PERGUNTA",
              lines=["VOCÊ JÁ TEVE", "O CARTÃO", "!CLONADO?"], tsize=0.22, lsize=0.28)
    h = hero("hero", (-1.0, -0.3, 0), rotz=-0.3)
    cd = card("hcard", s=0.4); cd.parent = h.arms[0]; cd.location = (0, -0.15, -0.85)
    cam = camera(32); c = pushcam(cam, sh, (0, -8.6, 2.9), (0.1, -7.8, 2.7), (0.1, 0.6, 1.9))
    def f(t):
        h.pose(t, armR=1.5, armRs=0.4, armL=0.6); h.blink(t); h.expr("grin")
        c(t)
    return f, ["card"]
