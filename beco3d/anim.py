"""Coreografia dos 30 segundos: 8 planos, poses, expressões e câmera.

Tudo é função do tempo t (segundos): `frame(t)` posiciona personagens e câmera.
Tempos e enquadramentos baseados nos primeiros 30s do vídeo de referência.
"""
import bpy, math
from mathutils import Vector, Matrix
import pessoas as PS

D = math.radians
FPS = 24
DUR = 30.0

# ------------------------------------------------------------------ utilidades
def ss(x):  # smoothstep
    x = max(0.0, min(1.0, x)); return x*x*(3 - 2*x)

def lerp(a, b, t): return a + (b - a)*t

def blend(p1, p2, a):
    out = {}
    for k in set(p1) | set(p2):
        d1, d2 = p1.get(k, {}), p2.get(k, {})
        out[k] = {q: lerp(d1.get(q, 0), d2.get(q, 0), a) for q in set(d1) | set(d2)}
    return out

def add(*ps):
    out = {}
    for p in ps:
        for k, d in p.items():
            o = out.setdefault(k, {})
            for q, v in d.items(): o[q] = o.get(q, 0) + v
    return out

def scale(p, f): return {k: {q: v*f for q, v in d.items()} for k, d in p.items()}

def track(keys, t):
    """keys: [(t, valor)] com valor numérico, tupla ou dict de pose; interpolação suave."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            a = ss((t - t0)/max(1e-6, t1 - t0))
            if isinstance(v0, dict): return blend(v0, v1, a)
            if isinstance(v0, (tuple, list)): return tuple(lerp(x, y, a) for x, y in zip(v0, v1))
            return lerp(v0, v1, a)
    return keys[-1][1]

def lin_track(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            a = (t - t0)/max(1e-6, t1 - t0)
            return tuple(lerp(x, y, a) for x, y in zip(v0, v1))
    return keys[-1][1]

def wob(t, f, seed=0.0):
    return (math.sin(t*f*6.283 + seed) + .5*math.sin(t*f*2.7*6.283 + seed*1.7) + .25*math.sin(t*f*5.3*6.283 + seed*3.1))/1.75

def floor_z(x, y):
    """Altura do chão (escada contínua para o quadril)."""
    if .1 <= x <= 1.7 and .9 <= y < 3.3: return min(1.6, max(0, (y - .9)/.30*.20 + .1))
    if .1 <= x <= 4.3 and 3.3 <= y <= 4.8: return 1.6
    if x < .2 and 2.0 <= y <= 4.8: return .45
    return 0.0

# ------------------------------------------------------------------ biblioteca de poses
def P(**kw):
    """P(upperarm_L=dict(...)) -> {'upperarm.L': {...}}"""
    return {k.replace("_L", ".L").replace("_R", ".R"): v for k, v in kw.items()}

REST = P(upperarm_L=dict(out=4, fwd=3), upperarm_R=dict(out=4, fwd=3), forearm_L=dict(bend=12), forearm_R=dict(bend=12),
         hand_L=dict(tw=0), hand_R=dict(tw=0))

def walk(phase, amp=1.0, stairs=0.0):
    """Ciclo de caminhada; phase em ciclos. stairs=1 sobe escada (passos altos)."""
    s = math.sin(phase*6.283); c = math.cos(phase*6.283)
    A = 24*amp + 18*stairs
    kneeL = max(0, -c)*(38*amp + 40*stairs) + 6
    kneeR = max(0, c)*(38*amp + 40*stairs) + 6
    return P(thigh_L=dict(fwd=A*s + 12*stairs), thigh_R=dict(fwd=-A*s + 12*stairs),
             shin_L=dict(bend=kneeL), shin_R=dict(bend=kneeR),
             foot_L=dict(down=-6*s*amp), foot_R=dict(down=6*s*amp),
             upperarm_L=dict(fwd=-16*s*amp), upperarm_R=dict(fwd=16*s*amp),
             forearm_L=dict(bend=10 + 8*amp), forearm_R=dict(bend=10 + 8*amp),
             pelvis=dict(tw=5*s*amp), chest=dict(tw=-6*s*amp, fwd=4 + 8*stairs))

def bob(phase, amp=1.0):
    return -abs(math.sin(phase*6.283))*.025*amp + .012*amp

# agente
AG_TALK = P(upperarm_L=dict(fwd=28, out=14), forearm_L=dict(bend=75), hand_L=dict(tw=-40),
            upperarm_R=dict(fwd=34, out=12), forearm_R=dict(bend=70), hand_R=dict(tw=40), chest=dict(fwd=4))
AG_POINT = P(upperarm_R=dict(fwd=78, out=38, tw=-10), forearm_R=dict(bend=6), hand_R=dict(fwd=-8),
             upperarm_L=dict(fwd=8, out=6), forearm_L=dict(bend=35), chest=dict(tw=-12), head=dict(tw=-28))
AG_REACH = P(upperarm_R=dict(fwd=62, out=4), forearm_R=dict(bend=28), upperarm_L=dict(fwd=46, out=-6), forearm_L=dict(bend=48),
             chest=dict(fwd=12), spine=dict(fwd=6))
AG_HOLD = P(upperarm_R=dict(fwd=72, out=14), forearm_R=dict(bend=40), upperarm_L=dict(fwd=58, out=-14), forearm_L=dict(bend=62),
            chest=dict(fwd=16, tw=8), spine=dict(fwd=8), thigh_L=dict(fwd=34), shin_L=dict(bend=38), thigh_R=dict(fwd=-8), shin_R=dict(bend=12))
AG_HAND_BACK = P(upperarm_L=dict(fwd=44, out=-10), forearm_L=dict(bend=30), hand_L=dict(fwd=-30),
                 upperarm_R=dict(fwd=10, out=6), forearm_R=dict(bend=30), chest=dict(fwd=4))
AG_LOOK_UP = P(head=dict(fwd=-16, tw=-10), neck=dict(fwd=-6))

# rapaz
RA_SIT = P(thigh_L=dict(fwd=82, out=10), thigh_R=dict(fwd=82, out=14), shin_L=dict(bend=74), shin_R=dict(bend=88),
           upperarm_L=dict(fwd=-12, out=22), forearm_L=dict(bend=8), upperarm_R=dict(fwd=-10, out=24), forearm_R=dict(bend=8),
           chest=dict(fwd=10), spine=dict(fwd=6))
RA_DEFEND = P(upperarm_L=dict(fwd=118, out=26), forearm_L=dict(bend=118, tw=-20),
              upperarm_R=dict(fwd=40, out=20), forearm_R=dict(bend=92),
              spine=dict(fwd=-6, side=8), chest=dict(fwd=-8, tw=-22), head=dict(tw=28, fwd=10, side=-8),
              thigh_L=dict(fwd=26, out=8), shin_L=dict(bend=40), thigh_R=dict(fwd=8, out=10), shin_R=dict(bend=30))
RA_PULL = P(upperarm_L=dict(fwd=60, out=34), forearm_L=dict(bend=60), upperarm_R=dict(fwd=-20, out=24), forearm_R=dict(bend=40),
            spine=dict(fwd=-10, side=-6), chest=dict(tw=18), head=dict(tw=-20), thigh_L=dict(fwd=20), shin_L=dict(bend=25),
            thigh_R=dict(fwd=-12), shin_R=dict(bend=10))
RA_CHEST = P(upperarm_R=dict(fwd=34, out=-14), forearm_R=dict(bend=126, tw=30), hand_R=dict(fwd=10),
             upperarm_L=dict(fwd=24, out=26), forearm_L=dict(bend=58, tw=50), hand_L=dict(tw=-60),
             spine=dict(fwd=-4), head=dict(fwd=-6))
RA_SHRUG = P(upperarm_L=dict(fwd=30, out=30), forearm_L=dict(bend=64, tw=60), hand_L=dict(tw=-70),
             upperarm_R=dict(fwd=26, out=26), forearm_R=dict(bend=60, tw=60), hand_R=dict(tw=-70),
             shoulder_L=dict(up=10), shoulder_R=dict(up=10), head=dict(fwd=-4))
RA_POINT_BACK = P(upperarm_R=dict(fwd=58, out=28), forearm_R=dict(bend=34), hand_R=dict(fwd=-10),
                  upperarm_L=dict(fwd=18, out=14), forearm_L=dict(bend=50), chest=dict(tw=20), head=dict(tw=34))
RA_ARMS_CHEST = P(upperarm_L=dict(fwd=30, out=-8), forearm_L=dict(bend=110), upperarm_R=dict(fwd=30, out=-8), forearm_R=dict(bend=110))

# ------------------------------------------------------------------ câmera
class Cam:
    def __init__(self, scene):
        self.ob = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
        scene.collection.objects.link(self.ob); scene.camera = self.ob
        self.ob.data.sensor_width = 36
        self.ob.data.clip_start = .05

    def set(self, loc, target, lens=26, t=0.0, shake=1.0, roll=0.0):
        loc = Vector(loc); target = Vector(target)
        # tremido de câmera na mão (sutil)
        sh = Vector((wob(t, .35, 1), wob(t, .3, 2), wob(t, .4, 3)))*.012*shake
        loc = loc + sh
        target = target + Vector((wob(t, .25, 4), 0, wob(t, .28, 5)))*.02*shake
        d = (target - loc).normalized()
        q = d.to_track_quat('-Z', 'Y')
        self.ob.matrix_world = Matrix.Translation(loc) @ q.to_matrix().to_4x4() @ Matrix.Rotation(D(roll + 1.2*wob(t, .2, 6)*shake), 4, 'Z')
        self.ob.data.lens = lens

# ------------------------------------------------------------------ fala / piscar
def talk(t, amount=1.0, seed=0.0):
    v = .5 + .5*math.sin(t*11 + seed) * math.sin(t*3.1 + seed*2)
    return max(0, v)*.55*amount

def blink(t, period=3.1, seed=0.0):
    x = (t + seed) % period
    return -1.0 if x < .12 else 0.0

# ------------------------------------------------------------------ planos
SHOTS = []
def shot(t0, t1):
    def deco(fn): SHOTS.append((t0, t1, fn)); return fn
    return deco

FAR = (40, 40, 0, 0)

@shot(0.0, 3.2)
def s1(t, A, R, cam):
    """Beco: o agente vem andando na direção da câmera, falando e gesticulando; olha para trás/cima no fim."""
    y = lerp(-1.6, -4.6, t/3.2); ph = t*1.0
    A.place(.45, y, bob(ph), 0)
    g = track([(0, scale(AG_TALK, .3)), (.8, AG_TALK), (1.6, scale(AG_TALK, .6)), (2.3, AG_TALK), (3.2, scale(AG_TALK, .4))], t)
    look = track([(0, {}), (2.3, {}), (2.9, AG_LOOK_UP)], t)
    gest = P(forearm_L=dict(bend=14*math.sin(t*5)), forearm_R=dict(bend=18*math.sin(t*4.3 + 1)))
    A.pose(add(walk(ph, .8), g, look, gest, P(head=dict(tw=8*math.sin(t*1.3)))))
    A.face(brow=.2, frown=.5, mouth=talk(t, 1.1), eyes=blink(t))
    A.fingers("L", .25, spread=.6); A.fingers("R", .25, spread=.6)
    R.place(*FAR)
    cy = lerp(-6.2, -7.4, t/3.2)
    cam.set((.55, cy, 1.5), (.45, y + .2, 1.45), 26, t)

@shot(3.2, 6.5)
def s2(t, A, R, cam):
    """Pé da escada: o rapaz sentado no corrimão; o agente chega por trás e começa a subir."""
    lt = t - 3.2
    p0, p1 = Vector((.75, -1.2)), Vector((.95, 1.15))
    a = min(1, lt/3.0); pos = p0.lerp(p1, a); ph = lt*1.05
    on_st = ss((pos.y - .8)/.5)
    A.place(pos.x, pos.y, floor_z(pos.x, pos.y)*on_st + bob(ph), 180)
    A.pose(add(walk(ph, .85, on_st), track([(0, {}), (1.0, AG_LOOK_UP), (2.0, {})], lt),
               P(upperarm_R=dict(out=6), forearm_R=dict(bend=10))))
    A.face(frown=.6, mouth=talk(lt, .7, 1), eyes=blink(lt, 2.7))
    A.fingers("L", .4); A.fingers("R", .4)
    # rapaz sentado no corrimão do meio (y=1.5 -> topo ~ z 1.3), olhando o agente chegar
    R.place(1.5, 1.55, .38, -90)
    R.pose(add(RA_SIT, P(head=dict(tw=track([(0, -10), (1.5, 25), (3.3, 40)], lt), fwd=-6)), P(chest=dict(tw=10))))
    R.face(brow=track([(0, 0), (1.8, .7)], lt), eyes=-1 if blink(lt, 3.5) < 0 else track([(0, 0), (1.8, .6)], lt),
           mouth=track([(0, 0), (2.4, .25)], lt))
    R.fingers("L", .55); R.fingers("R", .55)
    cl = Vector(lin_track([(0, (.55, -3.4, 1.65)), (3.3, (.75, -1.3, 1.75))], lt))
    tg = Vector(lin_track([(0, (.9, 1.6, 1.35)), (3.3, (1.1, 2.0, 1.45))], lt))
    cam.set(cl, tg, 24, t)

@shot(6.5, 12.0)
def s3(t, A, R, cam):
    """Confronto na escada: o agente segura o braço, o rapaz se protege e puxa o braço."""
    lt = t - 6.5
    ay = track([(0, 1.0), (1.4, 1.35), (3.8, 1.45), (5.5, 1.7)], lt)
    A.place(.95, ay, floor_z(.95, ay), 180)
    ap = track([(0, scale(walk(.25, .6, 1), 1)), (1.0, AG_REACH), (2.2, AG_HOLD), (3.6, AG_HOLD), (4.4, add(AG_HOLD, P(chest=dict(tw=-10)))), (5.5, AG_HOLD)], lt)
    A.pose(add(ap, P(head=dict(fwd=-8, tw=6*math.sin(lt*2)))))
    A.face(frown=.8, brow=-.2, mouth=talk(lt, .9, 2), eyes=blink(lt, 2.9))
    A.fingers("L", track([(0, .3), (1.8, .75)], lt)); A.fingers("R", track([(0, .3), (1.8, .7)], lt))
    ry = track([(0, 1.85), (2.0, 1.95), (3.5, 2.15), (5.5, 2.05)], lt)
    rh = track([(0, 160), (1.6, 150), (3.0, 120), (4.5, 150), (5.5, 170)], lt)
    R.place(track([(0, .95), (2.5, 1.15), (5.5, 1.05)], lt), ry, floor_z(1.0, ry) - track([(0, 0), (2.0, .08), (3.5, .05)], lt), rh)
    rp = track([(0, REST), (1.2, scale(RA_PULL, .5)), (2.2, RA_DEFEND), (3.4, RA_DEFEND), (4.3, RA_PULL), (5.5, scale(RA_DEFEND, .8))], lt)
    R.pose(add(rp, P(spine=dict(side=5*math.sin(lt*3)))))
    R.face(brow=.8, frown=.4, eyes=.8, mouth=track([(0, .2), (2.0, .7), (3.0, .4), (4.0, .8), (5.5, .5)], lt) + .15*math.sin(lt*9))
    R.fingers("L", .6, spread=.4); R.fingers("R", .7)
    # câmera baixa atrás do agente (mostra "PROTEÇÃO ANIMAL"), orbitando para a direita
    ang = track([(0, -62), (5.5, -30)], lt)
    rad = track([(0, 2.1), (5.5, 1.8)], lt)
    ctr = Vector((.95, 1.6, 1.0))
    cl = ctr + Vector((math.sin(D(ang))*rad, -math.cos(D(ang))*rad, track([(0, .75), (5.5, .95)], lt)))
    cam.set(cl, Vector((1.0, 1.8, 1.5)), 22, t, 1.3)

@shot(12.0, 15.0)
def s4(t, A, R, cam):
    """O rapaz desce a escada rápido, olhando para trás; o agente vem atrás. Câmera acompanha (pan rápido)."""
    lt = t - 12.0
    ry = track([(0, 2.7), (2.4, .2), (3.0, -.4)], lt); ph = lt*1.6
    R.place(1.0, ry, floor_z(1.0, ry) + bob(ph, .6), track([(0, 10), (1.5, -5), (3.0, -25)], lt))
    R.pose(add(walk(ph, .9), P(head=dict(tw=track([(0, 55), (1.4, 10), (2.2, 50), (3.0, 0)], lt)), chest=dict(tw=14)),
               P(upperarm_L=dict(out=18), upperarm_R=dict(out=18))))
    R.face(brow=.6, eyes=.5, mouth=talk(lt, 1.2, 3))
    R.fingers("L", .4); R.fingers("R", .4)
    ay = track([(0, 3.6), (1.0, 3.2), (3.0, 1.4)], lt); pha = lt*1.3
    A.place(1.0, ay, floor_z(1.0, ay) + bob(pha), 0)
    A.pose(add(walk(pha, .8), P(head=dict(fwd=10)), track([(0, {}), (2.0, AG_TALK)], lt)))
    A.face(frown=.7, mouth=talk(lt, 1, 4), eyes=blink(lt, 2.5))
    A.fingers("L", .3); A.fingers("R", .3)
    # câmera no largo, à esquerda; pan acompanha o rapaz
    cl = Vector(lin_track([(0, (-.9, -.9, 1.55)), (3.0, (-1.1, -1.8, 1.5))], lt))
    tgt = Vector((1.0, ry, floor_z(1.0, ry) + 1.35))
    whip = track([(0, Vector((1.4, 3.6, 3.0))), (.45, tgt), (3.0, tgt)], lt)
    cam.set(cl, Vector(whip), 24, t, 1.4)

@shot(15.0, 18.0)
def s5(t, A, R, cam):
    """Beco: o rapaz de costas para a câmera; o agente de frente explicando com as mãos."""
    lt = t - 15.0
    R.place(.55, -3.0, 0, 30)
    R.pose(add(RA_ARMS_CHEST if lt < 1.4 else blend(RA_ARMS_CHEST, RA_SHRUG, ss((lt - 1.4)/.6)), P(head=dict(tw=-6, fwd=-4))))
    R.face(brow=.5, eyes=.3, mouth=talk(lt, .6, 5))
    R.fingers("L", .5); R.fingers("R", .5)
    A.place(-.45, -4.3, 0, 155)
    A.pose(add(AG_TALK, P(upperarm_L=dict(fwd=10*math.sin(lt*3.2)), upperarm_R=dict(fwd=12*math.sin(lt*2.7 + 1)),
                         forearm_L=dict(bend=15*math.sin(lt*4)), head=dict(tw=5*math.sin(lt*1.5), fwd=4))))
    A.face(frown=.5, brow=.3*math.sin(lt*2), mouth=talk(lt, 1.2, 6), eyes=blink(lt, 2.6))
    A.fingers("L", .15, spread=1); A.fingers("R", .15, spread=1)
    cl = Vector(lin_track([(0, (1.05, -1.5, 1.62)), (3.0, (.95, -1.85, 1.6))], lt))
    cam.set(cl, (-.2, -3.9, 1.35), 28, t)

@shot(18.0, 22.0)
def s6(t, A, R, cam):
    """O rapaz com a mão no peito, espantado; o agente atrás aponta para o fim do beco."""
    lt = t - 18.0
    R.place(.0, -3.6, 0, -8)
    R.pose(add(track([(0, RA_SHRUG), (.7, RA_CHEST), (4.0, RA_CHEST)], lt), P(head=dict(tw=-8 + 6*math.sin(lt*1.3), side=4))))
    R.face(brow=1.0, eyes=.9, mouth=track([(0, .3), (.8, .9), (2.4, .6), (3.0, .95), (4, .7)], lt), smile=0)
    R.fingers("L", .2, spread=1); R.fingers("R", .1, spread=.3)
    A.place(.65, -2.75, 0, -20)
    A.pose(track([(0, AG_TALK), (.9, AG_POINT), (4.0, AG_POINT)], lt))
    A.face(brow=.4, mouth=talk(lt, 1.0, 7)*.8 + .1, smile=.6, eyes=blink(lt, 2.4))
    A.fingers("R", point=True); A.fingers("L", .3)
    cl = Vector(lin_track([(0, (-.1, -5.6, 1.5)), (4.0, (-.05, -5.0, 1.52))], lt))
    cam.set(cl, (.2, -3.2, 1.38), 26, t)

@shot(22.0, 24.5)
def s7(t, A, R, cam):
    """Close no rosto do rapaz: boca aberta, olhos arregalados, mão espalmada."""
    lt = t - 22.0
    R.place(.0, -3.6, 0, -12)
    R.pose(add(P(upperarm_L=dict(fwd=46, out=30), forearm_L=dict(bend=40, tw=70), hand_L=dict(tw=-70)),
               P(upperarm_R=dict(fwd=6, out=8), forearm_R=dict(bend=20)),
               P(head=dict(tw=track([(0, 8), (1.2, -6), (2.5, 4)], lt), fwd=-6, side=5))))
    R.face(brow=1.0, frown=0, eyes=1.0, mouth=.85 + .1*math.sin(lt*6))
    R.fingers("L", .1, spread=1); R.fingers("R", .3)
    A.place(.9, -2.4, 0, -40)
    A.pose(AG_POINT); A.face(); A.fingers("R", point=True)
    hc = Vector((.0, -3.6, 1.58))
    cl = Vector(lin_track([(0, (-.18, -4.75, 1.58)), (2.5, (-.14, -4.55, 1.56))], lt))
    cam.set(cl, hc + Vector((.02, 0, -.12)), 32, t, .8, roll=-3)

@shot(24.5, 30.0)
def s8(t, A, R, cam):
    """Pé da escada, perto da mureta com corrimão azul: o rapaz gesticula, o agente com a mão nas costas dele."""
    lt = t - 24.5
    R.place(-.95, 1.2, 0, track([(0, 15), (2.0, -15), (3.5, 5), (5.5, -10)], lt))
    rp = track([(0, RA_POINT_BACK), (1.6, RA_SHRUG), (2.8, RA_POINT_BACK), (4.2, RA_SHRUG), (5.5, RA_CHEST)], lt)
    R.pose(add(rp, P(head=dict(tw=track([(0, 35), (1.6, -5), (2.8, 35), (4.2, -10)], lt), fwd=-4))))
    R.face(brow=.9, eyes=.7, mouth=talk(lt, 1.6, 8) + .15)
    R.fingers("L", .2, spread=.8); R.fingers("R", .15, spread=.6)
    A.place(-.45, 1.55, 0, -25)
    A.pose(add(AG_HAND_BACK, P(head=dict(tw=-10, fwd=6))))
    A.face(frown=.4, mouth=talk(lt, .5, 9), eyes=blink(lt, 2.8))
    A.fingers("L", .1, spread=.5); A.fingers("R", .3)
    ang = track([(0, 8), (5.5, 30)], lt)
    ctr = Vector((-.75, 1.35, 1.2))
    rad = track([(0, 2.6), (5.5, 2.2)], lt)
    cl = ctr + Vector((math.sin(D(ang))*rad, -math.cos(D(ang))*rad, .35))
    cam.set(cl, ctr + Vector((0, 0, .25)), 24, t)

# ------------------------------------------------------------------ montagem
class Filme:
    def __init__(self, scene):
        self.A = PS.Pessoa(PS.AGENTE)
        self.R = PS.Pessoa(PS.RAPAZ)
        self.cam = Cam(scene)

    def frame(self, t):
        for t0, t1, fn in SHOTS:
            if t0 <= t < t1 or (t1 == DUR and t >= t1):
                fn(t, self.A, self.R, self.cam); break
        bpy.context.view_layer.update()

def shot_at(t):
    for i, (t0, t1, fn) in enumerate(SHOTS):
        if t0 <= t < t1: return i + 1, fn.__doc__.strip().split("\n")[0]
    return len(SHOTS), SHOTS[-1][2].__doc__
