"""Gramática de câmera do canal "E SE…" (medida quadro a quadro no vídeo de referência, ver ESTILO.md).

A câmera nunca para:
  * HOLD  — entre uma batida e outra, zoom lento e contínuo para dentro (~6% de escala por segundo),
            com um balanço mínimo (±0,25° de rotação, deriva de poucos pixels).
  * WHIP  — na troca de batida, um movimento rápido de 0,25–0,4 s: zoom/pan com aceleração e freio fortes,
            um "tranco" de rotação de 3–8° que volta a zero e desfoque de movimento (render.py faz os subquadros).
  * SHAKE — impactos: tremida que decai em ~0,4 s.
  * ENTRADA/SAÍDA de cena — a cena começa terminando um whip (vem rodada e mais aberta) e termina começando
            outro na mesma direção, então o corte some dentro do borrão.

O enquadramento é dado no plano do personagem: centro (x, z) e altura do quadro h (unidades do Blender).
A câmera fica num ponto fixo por cena e só muda a distância focal — é zoom de verdade, como na referência
(que é 2D e escala a imagem), sem paralaxe estranha.
"""
import math
from mathutils import Vector, Quaternion

PUSH = 0.06        # zoom contínuo por segundo durante o hold
WHIP = 0.32        # duração padrão do whip (s)
SENSOR = 36.0      # mm (sensor_fit vertical em look.camera)

def _cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def _smooth(u):     # ease-in-out forte (quíntico): acelera e freia como na referência
    u = _cl(u); return u*u*u*(u*(u*6-15)+10)

class Shot:
    """Uma batida de câmera: a partir de t, enquadrar (cx, cz) com altura h.
    kind: 'whip' (padrão), 'cut' (troca seca), 'slow' (transição suave de dur s).
    roll: tranco de rotação do whip (graus, sinal = direção). push: zoom/s durante o hold."""
    def __init__(self, t, cx, cz, h, kind="whip", dur=None, roll=None, push=PUSH, shake=0.0):
        self.t, self.c, self.h = t, Vector((cx, cz)), h
        self.kind, self.dur, self.roll, self.push, self.shake = kind, dur, roll, push, shake

class Rig:
    """eye: posição fixa da câmera. plane_y: profundidade do plano do personagem.
    shots: lista de Shot em ordem. enter/exit: (dx, dz, dzoom, roll) do whip de entrada/saída da cena."""
    def __init__(self, cam, shots, dur, eye_y=-9.0, plane_y=0.0, enter=(0.0, 0.0, 0.35, 6.0), exit=(0.0, 0.0, -0.4, -6.0),
                 enter_t=0.22, exit_t=0.2, seed=0.0):
        self.cam, self.shots, self.dur = cam, shots, dur
        self.eye_y, self.plane_y = eye_y, plane_y
        self.enter, self.exit, self.enter_t, self.exit_t, self.seed = enter, exit, enter_t, exit_t, seed
        self.impacts = []     # (t, força)
        for s in shots:
            if s.shake: self.impacts.append((s.t, s.shake))

    def impact(self, t, amp=0.06):
        self.impacts.append((t, amp)); return self

    # estado (centro, altura, roll) no tempo t — sem balanço nem tremida
    def state(self, t):
        sh = self.shots
        # hold do shot i, com push acumulado
        def held(i, tt):
            s = sh[i]; return s.c.copy(), s.h * (1 - s.push) ** max(0.0, tt - s.t), 0.0
        i = 0
        for k, s in enumerate(sh):
            if t >= s.t: i = k
        c, h, r = held(i, t)
        # whip para o próximo shot começa antes de next.t e termina em next.t
        if i + 1 < len(sh):
            nx = sh[i+1]
            d = nx.dur or (WHIP if nx.kind == "whip" else 0.9 if nx.kind == "slow" else 0)
            if d and t > nx.t - d:
                u = (t - (nx.t - d)) / d
                c0, h0, _ = held(i, nx.t - d)
                e = _smooth(u)
                c = c0.lerp(nx.c, e)
                h = math.exp(math.log(h0) + (math.log(nx.h) - math.log(h0)) * e)
                if nx.kind == "whip":
                    # zoom "respira" para fora no meio do whip (como a referência) e roda e volta
                    h *= 1 + 0.18 * math.sin(math.pi * u)
                    ro = nx.roll if nx.roll is not None else (5.0 if (i % 2) else -5.0)
                    r = ro * math.sin(math.pi * u)
        return c, h, r

    def pose(self, t):
        c, h, r = self.state(t)
        # entrada de cena: termina um whip
        if t < self.enter_t:
            u = 1 - _smooth(t / self.enter_t)
            dx, dz, dzm, ro = self.enter
            c = c + Vector((dx, dz)) * u; h *= 1 + dzm * u; r += ro * u
        # saída de cena: começa um whip
        if t > self.dur - self.exit_t:
            u = _smooth((t - (self.dur - self.exit_t)) / self.exit_t)
            u = u * u
            dx, dz, dzm, ro = self.exit
            c = c + Vector((dx, dz)) * u; h *= max(0.2, 1 + dzm * u); r += ro * u
        # balanço mínimo (respiração de câmera de mão)
        s = self.seed
        c = c + Vector((math.sin(t*0.9+s)*0.004*h, math.sin(t*1.3+s*2)*0.004*h))
        r += math.sin(t*0.7+s)*0.25
        # tremida de impacto
        for ti, amp in self.impacts:
            k = t - ti
            if 0 <= k < 0.45:
                dec = (1 - k/0.45) ** 2
                c = c + Vector((math.sin(k*73)*amp*h*dec, math.cos(k*61)*amp*h*dec))
                r += math.sin(k*57)*amp*40*dec
        return c, h, r

    def apply(self, t):
        c, h, r = self.pose(t)
        cam = self.cam
        eye = Vector((c.x, self.eye_y, c.y))
        dist = self.plane_y - self.eye_y
        cam.location = eye
        cam.rotation_mode = 'QUATERNION'
        q = Vector((0, 1, 0)).to_track_quat('-Z', 'Y')
        cam.rotation_quaternion = q @ Quaternion((0, 0, 1), math.radians(r))
        cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = SENSOR
        cam.data.lens = SENSOR * dist / h
        return h

    def speed(self, t, dt=1/30):
        """quanto o quadro muda entre t-dt/2 e t+dt/2 (fração da tela) — usado para ligar o desfoque."""
        c0, h0, r0 = self.pose(t - dt/2); c1, h1, r1 = self.pose(t + dt/2)
        return abs(math.log(h1/h0)) + (c1 - c0).length / h0 + abs(r1 - r0) / 30
