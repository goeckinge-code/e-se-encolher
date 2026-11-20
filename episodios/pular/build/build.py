"""Gera o episódio "E SE o mundo te pagasse pra pular?" (HyperFrames, 9:16, sem voz).
Saída: ../index.html, ../compositions/*.html, ../narracao.txt.   Rode: python3 build/build.py
Estilo: referencias/estilo-cartoon-noturno/ESTILO.md"""
import os, sys, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import chars

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================== roteiro
# cada cena: texto da narração + planos. Um plano começa na legenda que contém a palavra-gatilho.
SCENES = [
    dict(id="c1", rain=True, text="E se o mundo te pagasse pra pular? No meu mundo é assim: pulou, caiu um pix na hora.",
         shots=[(None, "s1_rua"), ("No meu", "s1_cidade"), ("pulou", "s1_pulo"), ("caiu", "s1_celular")]),
    dict(id="c2", rain=True, text="Um real por centímetro. Pulou quarenta, ganhou quarenta. Pulou um metro... cem reais. "
         "Por isso aqui ninguém anda. Todo mundo vai pro trabalho pulando. Elevador? Faliu. "
         "E o homem mais odiado da cidade é o que inventou o teto baixo.",
         shots=[(None, "s2_regua"), ("isso", "s2_trabalho"), ("Elevador", "s2_elevador"), ("homem", "s2_procurado")]),
    dict(id="c3", rain=True, text="Criança pula corda e paga a própria escola. Jogador de vôlei virou bilionário. "
         "E quem tem cama elástica em casa... é tratado como quem tem poço de petróleo. "
         "Todo dia, à meia-noite, acende no céu o Ranking do Pulo. Em primeiro, há trinta anos: o Canguru. "
         "Ninguém sabe a altura do pulo dele... porque ninguém nunca viu ele descer.",
         shots=[(None, "s3_corda"), ("Jogador", "s3_volei"), ("cama", "s3_cama"), ("Todo", "s3_ceu"),
                ("Em primeiro", "s3_ranking"), ("Ninguém", "s3_lenda")]),
    dict(id="c4", rain=True, text="E lá no último lugar... tô eu. Léo. Três centímetros. Três reais por pulo. "
         "Minha vó pulou quarenta anos pra criar a gente. Hoje o joelho dela não deixa nem ela levantar da cadeira. "
         "Então eu decidi: eu ia pular mais alto que todo mundo.",
         shots=[(None, "s4_ultimo"), ("Léo", "s4_leo"), ("centímetros", "s4_pulinho"), ("vó", "s4_vo"),
                ("joelho", "s4_joelho"), ("Então", "s4_decidi")]),
    dict(id="c5", rain=True, text="Primeiro, achei um pula-pula de mola no ferro-velho. Cinquenta centímetros. Cinquenta reais! "
         "Até a mola quebrar... e eu cair de cara na poça.",
         shots=[(None, "s5_ferrovelho"), ("Cinquenta", "s5_pogo"), ("Até", "s5_quebra")]),
    dict(id="c6", rain=True, text="Depois, entrei escondido no circo, de madrugada, e pulei na cama elástica do trapézio. "
         "Doze metros. Mil e duzentos reais por pulo! Só que o dono do circo também tava no ranking... e me jogou na rua.",
         shots=[(None, "s6_lona"), ("e pulei", "s6_cama"), ("Doze", "s6_alto"), ("dono", "s6_dono"), ("jogou", "s6_rua")]),
    dict(id="c7", rain=True, text="Aí eu fiz as contas. O problema não era a minha perna. Era a gravidade. "
         "Na Lua, todo mundo pula seis vezes mais alto. Juntei tudo que eu tinha... "
         "e comprei uma passagem no foguete mais barato do mundo.",
         shots=[(None, "s7_contas"), ("gravidade", "s7_gravidade"), ("Lua", "s7_lua"), ("Juntei", "s7_cofrinho"),
                ("comprei", "s7_foguete")]),
    dict(id="c8", rain=False, text="Pisei na Lua. Dobrei os joelhos. E pulei com toda a força. "
         "O celular não parava: dez mil... cem mil... um milhão... E eu continuei subindo. Subindo. E não desci mais.",
         shots=[(None, "s8_lua"), ("Dobrei", "s8_agacha"), ("E pulei", "s8_salto"), ("celular", "s8_celular"),
                ("continuei", "s8_subindo")]),
    dict(id="c9", rain=False, text="Porque aqui o pulo só termina quando você cai. Eu virei o primeiro do ranking, "
         "ganhando dinheiro a cada segundo, flutuando no espaço. E foi aí que eu vi, flutuando do meu lado... "
         "um velhinho de barba branca, com o celular na mão. O Canguru. Ele sorriu e disse: "
         "Trinta anos, garoto. Trinta anos esperando alguém pra conversar.",
         shots=[(None, "s9_flutua"), ("primeiro", "s9_ranking"), ("foi", "s9_viu"), ("velhinho", "s9_canguru"),
                ("sorriu", "s9_juntos")]),
    dict(id="c10", rain=False, hold=2.8, text="Agora eu sou o mais rico do mundo... e não tenho onde gastar. "
         "Eu volto pra Terra e perco tudo? Ou fico aqui em cima com o Canguru? Comenta aí: voltar ou ficar?",
         shots=[(None, "s10_olha"), ("volto", "s10_escolha")]),
]

# ============================================================== tempos (palavra a palavra)
LEAD, TAIL = 0.25, 0.30
STOP = ".?!"


def word_dur(w):
    core = w.strip(".,?!:")
    d = max(0.24, min(0.56, 0.16 + 0.032 * len(core)))
    if w.endswith("..."):
        d += 0.42
    elif w[-1] in STOP:
        d += 0.28
    elif w[-1] in ",:":
        d += 0.14
    return d


def chunks_of(text):
    """legenda de 1-2 palavras: palavras curtas (<=2 letras) grudam na seguinte"""
    words = text.split()
    out, t, i = [], LEAD, 0
    while i < len(words):
        grp = [words[i]]
        while (len(grp[-1].strip(".,?!:")) <= 2 and grp[-1][-1] not in ".,?!:" and i + 1 < len(words)
               and len(grp) < 2):
            i += 1
            grp.append(words[i])
        d = sum(word_dur(w) for w in grp)
        cap = " ".join(w.strip(".,:") for w in grp).replace("...", "")
        out.append([round(t, 3), round(t + d, 3), cap.upper()])
        t += d
        i += 1
    return out, t


T = 0.0
for sc in SCENES:
    sc["chunks"], end = chunks_of(sc["text"])
    sc["dur"] = round(end + TAIL + sc.get("hold", 0), 3)
    sc["start"] = round(T, 3)
    T += sc["dur"]
TOTAL = round(T, 3)


# ============================================================== plano
class Shot:
    def __init__(self, sc, name, t0, t1, p):
        self.sc, self.name, self.t0, self.t1, self.p = sc, name, t0, t1, p
        self.js = []
        self.focus = (540, 980)
        self.zoom = 0.045          # zoom-in lento por segundo (ESTILO.md: 2-9 %/s)
        self.dy = -40
        self.push = None           # (t, dur, scale, fx, fy): push-in rápido
        self.rain = sc.get("rain", False)
        self.cur = 0
        self.punch = True

    @property
    def d(self):
        return self.t1 - self.t0

    def T(self, needle, after=None):
        """tempo (local da cena) da legenda que contém a palavra"""
        a = self.t0 if after is None else after
        for c in self.sc["chunks"]:
            if c[0] >= a - 1e-6 and needle.upper() in c[2]:
                return c[0]
        raise KeyError(f"{self.name}: '{needle}' não encontrado depois de {a}")

    def __call__(self, s):
        self.js.append(s)


def jt(t):
    return f"{t:.3f}"


# ------------------------------------------------------------------ fundos do Blender
LIGHT = {   # luz de contorno + ambiente dos personagens por cenário
    "rua": ("#b9b4ff", "brightness(.86) saturate(.92)"), "rua_alta": ("#b9b4ff", "brightness(.82) saturate(.9)"),
    "rua_close": ("#ffc98a", "brightness(.9)"), "beco": ("#8f9dff", "brightness(.84) saturate(.9)"),
    "beco_close": ("#8f9dff", "brightness(.86)"), "elevador": ("#dfe8ff", "brightness(.9) saturate(.85)"),
    "escola": ("#c0b0ff", "brightness(.88)"), "quadra": ("#e8eeff", "brightness(1.02)"),
    "quintal": ("#ff6a6a", "brightness(.85)"), "ceu": ("#cfe6ff", "brightness(.8)"), "ceu_lua": ("#fff4d0", "brightness(.6)"),
    "telhado": ("#fff4d0", "brightness(.85)"), "sala": ("#ffc98a", "brightness(.95) sepia(.08)"),
    "ferrovelho": ("#ffb07a", "brightness(.86)"), "circo": ("#ffd08a", "brightness(.88)"),
    "circo_dentro": ("#fff0d0", "brightness(.95)"), "circo_alto": ("#fff0d0", "brightness(.98)"),
    "foguete": ("#e0ecff", "brightness(.88)"), "lua": ("#ffffff", "brightness(1.0)"), "espaco": ("#cfe6ff", "brightness(.95)"),
}


def bg(name, dark=0.0):
    """fundo renderizado no Blender (assets/plates/<name>.jpg) com sobra para o zoom de câmera;
    também ajusta a luz de contorno/ambiente dos personagens desse plano"""
    rim, amb = LIGHT.get(name, ("#b9b4ff", ""))
    set_rim(rim, amb)
    o = f'<image href="../assets/plates/{name}.jpg" x="-54" y="-96" width="1188" height="2112" preserveAspectRatio="xMidYMid slice"/>'
    if dark:
        o += rect(-300, -300, W + 600, H + 600, "#05030a", extra=f'opacity="{dark}"')
    return o


# ------------------------------------------------------------------ cenários compostos
def city(p, seed, signs, ground=1530, lamps=(160, 900), far=True):
    r = random.Random(seed)
    o = sky(p) + stars(seed, 40, 700)
    if far:
        o += skyline(seed + 1, 760, 180, 420, "#1a1526", lit=.18)
    o += skyline(seed + 2, 1040, 120, 360, "#251e33", lit=.32)
    x = -40
    for i, (name, col, kind) in enumerate(signs):
        w = r.uniform(300, 360)
        o += storefront(p, x, ground - 560, w, 560, name, col, seed=seed + i, kind=kind)
        x += w + 20
    o += street(p, ground)
    for lx in lamps:
        o += lamp(p, lx, ground - 760, ground, side=1 if lx < 540 else -1)
    return o


def brick_wall(x0, y0, x1, y1, base="#4a2e2a", seed=3):
    r = random.Random(seed)
    o = rect(x0, y0, x1 - x0, y1 - y0, base)
    bw, bh = 90, 40
    for j in range(int((y1 - y0) / bh) + 1):
        off = (j % 2) * bw / 2
        for i in range(int((x1 - x0) / bw) + 2):
            c = r.choice(["#5a3631", "#55322d", "#613b34", "#4d2d29"])
            o += rect(x0 + i * bw - off, y0 + j * bh, bw - 6, bh - 6, c, rx=3)
    return o


def room(p, wall="#3a2e4f", seed=5):
    o = rect(-300, -300, W + 600, 1800, wall)
    for i in range(-4, 16):
        o += rect(i * 90, -300, 40, 1800, "#ffffff", extra='opacity=".04"')
    o += rect(-300, 1480, W + 600, 700, "#2a1f2e") + rect(-300, 1480, W + 600, 18, "#1c1420")
    # janela com chuva e luz da rua
    o += rect(640, 380, 330, 430, "#141c33", rx=6, stroke="#22182a", sw=16)
    o += skyline(seed, 820, 60, 300, "#1d2440", lit=.3, x0=650, x1=960)
    o += line("M805,380 L805,810 M640,595 L970,595", "#22182a", 12)
    o += glow(p, 805, 595, 260, "c", .4)
    return o


def earth(cx, cy, r):
    o = circ(cx, cy, r, "#1f5fbf", INK, 8)
    rr = random.Random(9)
    for _ in range(9):
        a = rr.uniform(0, 6.28)
        d = rr.uniform(0, r * .7)
        o += ell(cx + math.cos(a) * d, cy + math.sin(a) * d, rr.uniform(r * .12, r * .3), rr.uniform(r * .08, r * .2),
                 "#3fae5a", extra='opacity=".95"')
    o += circ(cx, cy, r, "none", "#8fd0ff", 14, extra='opacity=".35"')
    o += path(f"M{cx-r*.7},{cy-r*.55} Q{cx-r*.2},{cy-r*.95} {cx+r*.35},{cy-r*.8}", "none", "#ffffff", 10,
              extra='opacity=".35"')
    return o


def moon(cx, cy, r, col="#f1ecd2"):
    o = circ(cx, cy, r, col, INK, 6)
    rr = random.Random(int(r))
    for _ in range(7):
        o += circ(cx + rr.uniform(-r * .6, r * .6), cy + rr.uniform(-r * .6, r * .6), rr.uniform(r * .06, r * .16),
                  "#d9d1ad", extra='opacity=".9"')
    return o


def space(p, seed):
    return rect(-400, -400, W + 800, H + 800, "#07050d") + stars(seed, 220, H + 300) + \
        circ(300, 500, 600, "#3a1f6b", extra=f'opacity=".25" filter="url(#fx-soft)"')


def tent(cx, top, base, w):
    o = ""
    stripes = 8
    for i in range(stripes):
        x0 = cx - w / 2 + i * w / stripes
        x1 = x0 + w / stripes
        o += path(f"M{cx},{top} L{x0},{base} L{x1},{base} Z", "#c8243a" if i % 2 == 0 else "#f3e9dc", INK, 5)
    o += path(f"M{cx-w/2},{base} Q{cx-w/2+60},{base+50} {cx-w/2+w/stripes},{base} " +
              "".join(f"Q{cx-w/2+(k+.5)*w/stripes},{base+50} {cx-w/2+(k+1)*w/stripes},{base} " for k in range(1, stripes)),
              "#c8243a", INK, 5)
    o += line(f"M{cx},{top} L{cx},{top-80}", INK, 8) + path(f"M{cx},{top-80} L{cx+70},{top-62} L{cx},{top-44} Z", "#ffd23a", INK, 4)
    return o


def pogo(id, x, y, s=1.0):
    o = rect(-8, -330, 16, 300, "#9aa3b2", stroke=INK, sw=5)
    o += rect(-70, -320, 140, 20, "#e63946", rx=8, stroke=INK, sw=5)
    o += rect(-40, -100, 80, 18, "#e63946", rx=6, stroke=INK, sw=5)
    o += g("".join(line(f"M-18,{-80+k*14} L18,{-73+k*14}", "#c9ced8", 6) for k in range(5)), id=f"{id}-mola")
    o += rect(-6, -20, 12, 22, "#333", stroke=INK, sw=4)
    return g(g(o, id=id), tr=f"translate({f(x)},{f(y)}) scale({s})")


def splash(id, x, y):
    o = ""
    for k in range(9):
        a = math.pi * (k / 8)
        o += ell(math.cos(a) * -90, -math.sin(a) * 60, 14, 22, "#9fb8ff", INK, 3,
                 extra=f'transform="rotate({-(k/8*180-90):.0f} {math.cos(a)*-90:.0f} {-math.sin(a)*60:.0f})"')
    return g(g(o, id=id, extra='opacity="0"'), tr=f"translate({x},{y})")


# ============================================================== planos
# cada função recebe o Shot S e devolve o SVG (dentro da câmera). S("js") adiciona animação.

def s1_rua(S):
    p = S.p
    o = bg("rua")
    o += person(f"{p}a", "exec", 540, 1610, 1.55, "smile", umbrella=True)
    o += money(f"{p}m", 560, 860, "+R$ 40", 110)
    t = S.T("pular")
    S(f"J('{p}a',{jt(t)},150)")
    S(f"M('{p}m',{jt(t+.3)},1.1)")
    S.focus, S.zoom = (540, 1150), .05
    return o


def s1_cidade(S):
    p = S.p
    o = bg("rua_alta")
    cr, ids = crowd(f"{p}c", 4, 9, 1560, s=(.62, .8), umbrella=.35, briefcase=.3)
    o += cr
    r = random.Random(3)
    for i, pid in enumerate(ids):
        x = 0
        for k in range(3):
            t = S.t0 + .15 + r.uniform(0, .5) + k * .75
            if t < S.t1 - .6:
                S(f"J('{pid}',{jt(t)},{r.randint(120,220)},.26)")
    for i in range(6):
        o += money(f"{p}m{i}", r.uniform(120, 960), r.uniform(900, 1100), f"+R$ {r.choice([30,45,60,80,25,52])}", 64)
        S(f"M('{p}m{i}',{jt(S.t0+.25+i*.28)},.55)")
    S.focus, S.zoom, S.dy = (540, 1200), .03, -60
    return o


def s1_pulo(S):
    p = S.p
    o = bg("rua_close")
    o += person(f"{p}a", "exec", 520, 2050, 2.9, "happy", briefcase=True, pose="up")
    o += money(f"{p}m", 560, 520, "+R$ 40", 150)
    S(f"J('{p}a',{jt(S.t0+.02)},90,.3)")
    S(f"M('{p}m',{jt(S.t0+.25)},.9)")
    S.focus, S.zoom = (540, 900), .07
    return o


def s1_celular(S):
    p = S.p
    S.rain = False
    o = bg("rua_close", .35) + bokeh(p, 5, 10)
    o += phone(f"{p}ph", 540, 1020, 2.0, value="+R$ 40,00", sub="DE: CHÃO", clock="23:47")
    S(f"tl.from('#{p}ph',{{y:'+=260',duration:.35,ease:'power3.out'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 900), .06
    return o


def s2_regua(S):
    p = S.p
    o = bg("beco")
    o += ruler(780, 180, 1560, 5, 6, 20)
    o += plate(540, 170, "1 cm = R$ 1", 72, bg="#0b2414", fg="#3cff5a", border="#3cff5a")
    o += person(f"{p}a", "girl", 470, 1560, 1.6, "happy", pose="peace")
    o += money(f"{p}m1", 470, 640, "+R$ 40", 100)
    o += money(f"{p}m2", 470, 300, "+R$ 100", 110)
    t1 = S.T("quarenta")
    S(f"J('{p}a',{jt(t1)},{240/1.6:.0f},.32)")
    S(f"M('{p}m1',{jt(t1+.32)},.9)")
    t2 = S.T("metro")
    S(f"J('{p}a',{jt(t2)},{600/1.6:.0f},.5)")
    S(f"M('{p}m2',{jt(S.T('cem'))},1.0)")
    S.focus, S.zoom, S.dy = (540, 900), .02, 0
    return o


def s2_trabalho(S):
    p = S.p
    o = bg("rua")
    o += plate(820, 660, "PONTO", 44, bg="#2b55c9")
    cr, ids = crowd(f"{p}c", 9, 7, 1620, s=(.9, 1.05), umbrella=.2, briefcase=.9)
    o += cr
    r = random.Random(5)
    for i, pid in enumerate(ids):
        t = S.t0 + .1 + (i % 3) * .22
        while t < S.t1 - .7:
            S(f"J('{pid}',{jt(t)},{r.randint(160,240)},.3)")
            t += .8 + r.uniform(0, .15)
    for i in range(5):
        o += money(f"{p}m{i}", 140 + i * 200, 760 + (i % 2) * 120, f"+R$ {r.choice([35,48,52,60])}", 70)
        S(f"M('{p}m{i}',{jt(S.t0+.45+i*.35)},.5)")
    S.focus, S.zoom = (540, 1300), .035
    return o


def s2_elevador(S):
    p = S.p
    S.rain = False
    o = bg("elevador")
    o += line("M330,700 L750,1340 M750,700 L330,1340", "#ffd23a", 30) + line("M330,700 L750,1340 M750,700 L330,1340", INK, 5, extra='stroke-dasharray="30 30"')
    stamp = g(rect(-230, -80, 460, 160, "none", rx=14, stroke="#e63946", sw=12) +
              text(0, 52, "FALIU", 150, fill="#e63946", font=FONT_COND),
              id=f"{p}st", extra='opacity="0"')
    o += g(stamp, tr="translate(540,960) rotate(-12)")
    S(f"tl.fromTo('#{p}st',{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.16,ease:'power3.in',transformOrigin:'50% 50%'}},{jt(S.T('Faliu'))})")
    S.focus, S.zoom = (540, 960), .05
    return o


def s2_procurado(S):
    p = S.p
    o = bg("beco_close")
    o += wanted(f"{p}w", 540, 900, "PROCURADO", ("INVENTOR DO", "TETO BAIXO"), 1.55)
    S.focus, S.zoom = (540, 900), .055
    return o


def s3_corda(S):
    p = S.p
    o = bg("escola")
    o += plate(540, 600, "ESCOLA", 80, bg="#2b55c9")
    o += person(f"{p}a", "girl", 540, 1600, 1.7, "happy", pose="fists")
    rope_up = line("M420,1420 Q540,820 660,1420", "#ffffff", 7)
    rope_dn = line("M420,1420 Q540,1700 660,1420", "#ffffff", 7)
    o += g(rope_up, id=f"{p}r1") + g(rope_dn, id=f"{p}r2", extra='opacity="0"')
    r = random.Random(7)
    t, k = S.t0 + .05, 0
    while t < S.t1 - .45:
        S(f"J('{p}a',{jt(t)},70,.17)")
        S(f"tl.set('#{p}r1',{{opacity:0}},{jt(t+.08)});tl.set('#{p}r2',{{opacity:1}},{jt(t+.08)});"
          f"tl.set('#{p}r2',{{opacity:0}},{jt(t+.36)});tl.set('#{p}r1',{{opacity:1}},{jt(t+.36)})")
        t += .44
        k += 1
    for i in range(4):
        o += money(f"{p}m{i}", 330 + (i % 2) * 420, 960 - (i % 2) * 80, "+R$ 12", 70)
        S(f"M('{p}m{i}',{jt(S.t0+.3+i*.44)},.4)")
    st = g(rect(-260, -70, 520, 140, "#0b2414", rx=14, stroke="#3cff5a", sw=8) +
           text(0, 26, "MENSALIDADE PAGA", 56, fill="#3cff5a", font=FONT_COND), id=f"{p}ok", extra='opacity="0"')
    o += g(st, tr="translate(540,420) rotate(-4)")
    S(f"tl.fromTo('#{p}ok',{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.16,ease:'power3.in',transformOrigin:'50% 50%'}},{jt(S.T('escola'))})")
    S.focus, S.zoom = (540, 1100), .04
    return o


def s3_volei(S):
    p = S.p
    S.rain = False
    o = bg("quadra")
    o += person(f"{p}a", "atleta", 540, 1500, 1.5, "determined")
    o += g(circ(0, 0, 38, "#ffe066", INK, 6) + line("M-36,-8 Q0,6 36,-8 M-10,-36 Q4,0 -10,36", INK, 4), id=f"{p}ball",
           extra='transform="translate(700,700)"')
    o += money(f"{p}m", 540, 380, "+R$ 350", 110)
    o += tag(f"{p}tg", 540, 300, "BILIONÁRIO", 60)
    t = S.t0 + .05
    S(f"J('{p}a',{jt(t)},260,.42)")
    S(f"tl.to('#{p}a-armR',{{rotation:-200,duration:.12,svgOrigin:'0 0'}},{jt(t+.4)})")
    S(f"tl.to('#{p}ball',{{x:200,y:1400,duration:.35,ease:'power2.in'}},{jt(t+.5)})")
    S(f"M('{p}m',{jt(t+.55)},.8)")
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('bilionário'))})")
    S.focus, S.zoom = (540, 1000), .05
    return o


def s3_cama(S):
    p = S.p
    o = bg("quintal")
    o += person(f"{p}g1", "guard", 110, 1560, 1.25, "angry", pose="cross")
    o += person(f"{p}g2", "guard", 980, 1560, 1.25, "angry", flip=True, pose="cross")
    o += plate(540, 640, "PROPRIEDADE PRIVADA", 54, bg="#8a1c12", border="#ffd23a")
    S.focus, S.zoom = (540, 1050), .045
    return o


def s3_ceu(S):
    p = S.p
    o = bg("ceu")
    for x, a in ((180, 18), (900, -18), (360, 6), (720, -6)):
        o += g(cone(p, 0, 0, 60, 380, 1500, "c", .45), tr=f"translate({x},1560) rotate({180+a})")
    o += skyline(14, 1400, 150, 520, "#120e1a", lit=.25)
    o += ranking(f"{p}rk", 540, 400, [("1º", "O CANGURU", "R$ 900.000.000", "?"), ("2º", "KÁTIA MOLA", "R$ 48.000.000", "atleta"),
                                      ("3º", "BARÃO PIRUETA", "R$ 12.000.000", "dono")], s=.8, hi=0)
    S(f"tl.from('#{p}rk',{{y:'+=1300',duration:1.3,ease:'power2.out'}},{jt(S.t0+.1)})")
    S.focus, S.zoom, S.dy = (540, 700), .03, 30
    return o


def s3_ranking(S):
    p = S.p
    o = bg("ceu", .45)
    o += ranking(f"{p}rk", 540, 330, [("1º", "O CANGURU", "R$ 900.000.000", "?"), ("2º", "KÁTIA MOLA", "R$ 48.000.000", "atleta"),
                                      ("3º", "BARÃO PIRUETA", "R$ 12.000.000", "dono")], s=1.25, hi=0)
    o += glow(p, 540, 640, 520, "g", .35)
    o += tag(f"{p}tg", 540, 1180, "HÁ 30 ANOS EM 1º", 54)
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('trinta'))})")
    S.focus, S.zoom = (540, 640), .05
    return o


def s3_lenda(S):
    p = S.p
    o = bg("ceu_lua")
    sil = person(f"{p}a", "canguru", 540, 1380, 1.0, "smile")
    o += g(sil, id=f"{p}sil", extra='style="filter:brightness(0)"')
    o += g("".join(ell(x, y, rx, 50, "#2a2440", extra='opacity=".9"') for x, y, rx in ((200, 240, 260), (820, 180, 300), (520, 90, 340))),
           id=f"{p}cl")
    S(f"J('{p}a',{jt(S.t0+.3)},60,.2)")
    S(f"tl.to('#{p}sil',{{y:-1500,scale:.4,duration:{S.d-0.6:.2f},ease:'power1.in',svgOrigin:'540 1380'}},{jt(S.t0+.65)})")
    S.focus, S.zoom = (540, 700), .03
    return o


def s4_ultimo(S):
    p = S.p
    o = bg("ceu", .45)
    o += ranking(f"{p}rk", 540, 300, [("7.999.998º", "SEU JORGE", "R$ 5", None), ("7.999.999º", "TIA NENA", "R$ 4", None),
                                      ("8.000.000º", "LÉO", "R$ 3", "leo")], s=1.25, hi=2)
    S(f"tl.from('#{p}rk',{{y:'-=900',duration:.7,ease:'power3.out'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}rk',{{opacity:1}},{{opacity:.75,duration:.15,repeat:5,yoyo:true}},{jt(S.T('tô'))})")
    S.focus, S.zoom = (540, 880), .06
    return o


def s4_leo(S):
    p = S.p
    o = bg("beco")
    o += person(f"{p}a", "leo", 520, 1620, 2.1, "sad")
    o += tag(f"{p}tg", 520, 680, "LÉO", 64)
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('Léo'))})")
    S.focus, S.zoom = (520, 1000), .06
    return o


def s4_pulinho(S):
    p = S.p
    o = bg("beco")
    o += ruler(820, 1080, 1560, 1, 16, 5)
    o += person(f"{p}a", "leo", 520, 1600, 1.9, "sad", alt=("neutral",))
    o += money(f"{p}m", 560, 700, "+R$ 3", 90)
    t = S.t0 + .1
    S(f"J('{p}a',{jt(t)},{48/1.9:.0f},.14)")
    S(f"M('{p}m',{jt(t+.3)},.9)")
    t2 = S.T("reais")
    S(f"J('{p}a',{jt(t2)},{48/1.9:.0f},.14)")
    S.focus, S.zoom = (620, 1300), .05
    return o


def s4_vo(S):
    p = S.p
    S.rain = False
    o = bg("sala")
    o += rect(80, 420, 300, 260, "#6b4a24", stroke=INK, sw=8) + rect(100, 440, 260, 220, "#d9c8a0")
    o += person(f"{p}f", "vo", 230, 640, .45, "happy")
    o += text(230, 650, "1985", 30, fill="#5a3a1c", font=FONT_COND)
    o += glow(p, 540, 900, 600, "", .25)
    # poltrona: encosto atrás da vó, assento e braços na frente
    o += path("M190,1180 Q190,1040 290,1040 L650,1040 Q750,1040 750,1180 L750,1560 L190,1560 Z", "#7a2f3a", INK, 8)
    o += person(f"{p}a", "vo", 470, 1560, 1.8, "sad")
    o += rect(230, 1290, 480, 270, "#8b3a46", rx=26, stroke=INK, sw=8)              # assento cobre as pernas
    o += rect(150, 1210, 120, 350, "#8b3a46", rx=30, stroke=INK, sw=8) + rect(670, 1210, 120, 350, "#8b3a46", rx=30, stroke=INK, sw=8)
    o += rect(310, 1250, 330, 90, "#5b3d8a", rx=30, stroke=INK, sw=6)               # colo
    o += rect(540, 1262, 110, 66, "#f4f4f4", rx=20, stroke=INK, sw=5)               # joelho enfaixado
    o += line("M555,1280 L635,1310 M555,1310 L635,1280", "#c9ccd6", 4)
    # mesinha com a conta
    o += rect(780, 1300, 260, 24, "#6b4423", stroke=INK, sw=5) + rect(880, 1320, 40, 240, "#6b4423", stroke=INK, sw=5)
    o += g(rect(-90, -60, 180, 120, "#fff", rx=4, stroke=INK, sw=4) + text(0, -20, "CONTA DE LUZ", 24, fill=INK) +
           text(0, 34, "ATRASADA", 40, fill="#e63946"), tr="translate(910,1240) rotate(-8)")
    o += tag(f"{p}tg", 470, 800, "VÓ DALVA", 64)
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.t0+.15)})")
    S.focus, S.zoom = (470, 1050), .045
    return o


def s4_joelho(S):
    p = S.p
    S.rain = False
    o = bg("sala", .2) + bokeh(p, 7, 8, cols=("#ffd36b", "#ff9f6b"))
    o += person(f"{p}a", "vo", 540, 2350, 3.9, "sad")
    o += path("M100,1640 Q100,1500 220,1500 L860,1500 Q980,1500 980,1640 L980,2100 L100,2100 Z", "#7a2f3a", INK, 10)
    o += circ(700, 640, 10, "#9fd3ff", extra='opacity=".9"')
    S(f"tl.fromTo('#{p}a-head',{{rotation:0}},{{rotation:-5,duration:{S.d:.2f},ease:'sine.inOut',svgOrigin:'0 0'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p} circle[r=\"10\"]',{{y:0,opacity:0}},{{y:90,opacity:1,duration:.8}},{jt(S.t0+.6)})")
    S.focus, S.zoom = (540, 1000), .05
    return o


def s4_decidi(S):
    p = S.p
    o = bg("beco_close")
    o += person(f"{p}a", "leo", 540, 2420, 4.2, "sad", alt=("determined",))
    t = S.T("decidi")
    S(f"F('{p}a','sad','determined',{jt(t)});PZ('{p}a','fists',{jt(t)},.3)")
    S.push = (t, .9, 1.35, 540, 900)
    S.focus, S.zoom = (540, 900), .03
    return o


def s5_ferrovelho(S):
    p = S.p
    o = bg("ferrovelho")
    o += person(f"{p}a", "leo", 480, 1600, 1.9, "neutral", alt=("happy",))
    o += pogo(f"{p}pg", 720, 1600, 1.6)
    S(f"tl.from('#{p}pg',{{y:300,rotation:30,duration:.5,ease:'back.out(2)',transformOrigin:'50% 50%'}},{jt(S.t0+.2)})")
    S(f"F('{p}a','neutral','happy',{jt(S.T('pula-pula'))});PZ('{p}a','thumbs',{jt(S.T('pula-pula'))})")
    S.focus, S.zoom = (560, 1200), .05
    return o


def s5_pogo(S):
    p = S.p
    o = bg("ferrovelho")
    o += g(pogo(f"{p}pg", 540, 1620, 1.7) + person(f"{p}a", "leo", 540, 1440, 1.6, "happy"), id=f"{p}grp")
    o += money(f"{p}m", 540, 560, "+R$ 50", 110)
    t, k = S.t0 + .05, 0
    while t < S.t1 - .5:
        S(f"tl.to('#{p}grp',{{y:-300,duration:.28,ease:'power2.out'}},{jt(t)});tl.to('#{p}grp',{{y:0,duration:.28,ease:'power2.in'}},{jt(t+.28)})")
        S(f"tl.to('#{p}a-armL',{{rotation:40,duration:.1,transformOrigin:'50% 50%'}},{jt(t)});tl.to('#{p}a-armR',{{rotation:-40,duration:.1,svgOrigin:'0 0'}},{jt(t)})")
        if k < 3:
            S(f"M('{p}m',{jt(t+.2)},.3)")
        t += .62
        k += 1
    S.focus, S.zoom = (540, 1100), .05
    return o


def s5_quebra(S):
    p = S.p
    o = bg("ferrovelho")
    o += ell(640, 1590, 300, 50, "#4b5a8a", extra='opacity=".8"') + ell(640, 1590, 240, 30, "#7f93c9", extra='opacity=".5"')
    o += pogo(f"{p}pg", 300, 1600, 1.5)
    o += person(f"{p}a", "leo", 300, 1420, 1.5, "happy", alt=("shock",))
    o += g(line("M0,0 l30,-60 l20,40 l30,-70", "#c9ccd6", 8), id=f"{p}sp", extra='opacity="0" transform="translate(290,1520)"')
    o += splash(f"{p}spl", 640, 1580)
    tq = S.T("quebrar")
    S(f"tl.set('#{p}sp',{{opacity:1}},{jt(tq)});tl.to('#{p}sp',{{x:-200,y:-300,rotation:-200,duration:.6,svgOrigin:'40 -30'}},{jt(tq)})")
    S(f"F('{p}a','happy','shock',{jt(tq)})")
    S(f"tl.to('#{p}a-j',{{x:'+=230',y:'+=130',rotation:100,duration:.7,ease:'power1.in',transformOrigin:'50% 50%'}},{jt(tq+.1)})")
    S(f"tl.to('#{p}pg',{{rotation:-80,duration:.5,transformOrigin:'50% 50%'}},{jt(tq+.1)})")
    tp = S.T("poça")
    S(f"tl.fromTo('#{p}spl',{{opacity:1,scale:.3}},{{opacity:0,scale:1.4,duration:.5,ease:'power2.out',transformOrigin:'50% 50%'}},{jt(tp)})")
    S.focus, S.zoom = (600, 1400), .06
    return o


def s6_lona(S):
    p = S.p
    o = bg("circo")
    o += person(f"{p}a", "leo", 140, 1560, 1.35, "determined", pose="crouch")
    S(f"tl.fromTo('#{p}a-j',{{x:0}},{{x:270,duration:{S.d-.2:.2f},ease:'none'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}a-legL',{{rotation:-20}},{{rotation:20,duration:.25,repeat:{int(S.d/.25)},yoyo:true,svgOrigin:'0 0'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}a-legR',{{rotation:20}},{{rotation:-20,duration:.25,repeat:{int(S.d/.25)},yoyo:true,svgOrigin:'0 0'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 1200), .04
    return o


def s6_cama(S):
    p = S.p
    S.rain = False
    o = bg("circo_dentro")
    o += person(f"{p}a", "leo", 540, 1450, 1.2, "happy")
    o += money(f"{p}m", 540, 380, "+R$ 1.200", 110)
    t = S.t0 + .1
    while t < S.t1 - .9:
        S(f"J('{p}a',{jt(t)},{900/1.2:.0f},.55)")
        S(f"M('{p}m',{jt(t+.55)},.5)")
        t += 1.3
    S.focus, S.zoom, S.dy = (540, 900), .02, 0
    return o


def s6_alto(S):
    p = S.p
    S.rain = False
    o = bg("circo_alto")
    o += rect(120, 300, 20, 1600, "#ffd23a") + "".join(line(f"M120,{300+k*130} l40,0", INK, 5) for k in range(13))
    o += text(240, 330, "12 m", 90, fill="#ffd23a", font=FONT_COND, stroke=INK, sw=12)
    o += person(f"{p}a", "leo", 540, 1080, 1.7, "happy")
    for i in range(3):
        o += money(f"{p}m{i}", (250, 840, 830)[i], (900, 760, 1040)[i], "+R$ 1.200", 86)
        S(f"M('{p}m{i}',{jt(S.T('Mil')+i*.35)},.6)")
    S(f"tl.fromTo('#{p}a-j',{{y:200}},{{y:-40,duration:.6,ease:'power2.out'}},{jt(S.t0)});tl.to('#{p}a-j',{{y:900,duration:.9,ease:'power2.in'}},{jt(S.t1-1.0)})")
    S(f"tl.set('#{p}a-armL',{{rotation:150,svgOrigin:'0 0'}},{jt(S.t0)});tl.set('#{p}a-armR',{{rotation:-150,svgOrigin:'0 0'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 800), .05
    return o


def s6_dono(S):
    p = S.p
    S.rain = False
    o = bg("circo_dentro", .25) + bokeh(p, 9, 10, cols=("#ffd36b", "#ff9a5a"))
    o += person(f"{p}a", "dono", 540, 2250, 3.4, "angry", pose="hips")
    o += tag(f"{p}tg", 540, 430, "BARÃO PIRUETA", 60)
    badge = g(rect(-200, -60, 400, 110, "#0b2414", rx=12, stroke="#3cff5a", sw=6) +
              text(0, 26, "3º NO RANKING", 56, fill="#3cff5a", font=FONT_COND), id=f"{p}bd", extra='opacity="0"')
    o += g(badge, tr="translate(820,560) rotate(6)")
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.t0+.1)})")
    S(f"tl.fromTo('#{p}bd',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('ranking'))})")
    S.focus, S.zoom = (540, 800), .06
    return o


def s6_rua(S):
    p = S.p
    o = bg("rua")
    o += person(f"{p}a", "leo", 260, 1640, 1.5, "shock", pose="fall")
    o += splash(f"{p}spl", 760, 1640)
    t = S.t0 + .1
    S(f"tl.fromTo('#{p}a-j',{{x:-260,y:-330,rotation:-60}},{{x:330,y:0,rotation:80,duration:.75,ease:'power1.in',transformOrigin:'50% 50%'}},{jt(t)})")
    S(f"tl.fromTo('#{p}spl',{{opacity:1,scale:.3}},{{opacity:0,scale:1.4,duration:.5,transformOrigin:'50% 50%'}},{jt(t+.75)})")
    S.focus, S.zoom = (600, 1300), .05
    return o


def s7_contas(S):
    p = S.p
    S.rain = False
    o = bg("sala")
    o += rect(80, 300, 520, 640, "#1f3a2c", rx=8, stroke="#6b4423", sw=16)   # quadro
    for i, (t_, y) in enumerate((("R$ 1 = 1 cm", 400), ("EU = 3 cm", 500), ("3 cm = R$ 3", 600), ("PRECISO: +ALTO", 720))):
        o += g(text(110, y, t_, 52, fill="#f4f1e6", font=FONT_COND, anchor="start"), id=f"{p}l{i}", extra='opacity="0"')
        S(f"tl.to('#{p}l{i}',{{opacity:1,duration:.15}},{jt(S.t0+.15+i*.45)})")
    o += line("M140,760 L520,760", "#ffd23a", 8)
    o += person(f"{p}a", "leo", 760, 1600, 1.8, "neutral", alt=("determined",), pose="point")
    S(f"F('{p}a','neutral','determined',{jt(S.T('perna'))});PZ('{p}a','chin',{jt(S.T('perna'))})")
    S.focus, S.zoom = (480, 900), .05
    return o


def s7_gravidade(S):
    p = S.p
    S.rain = False
    o = bg("sala", .55) + bokeh(p, 10, 8, cols=("#a77bff", "#ff4fa3"))
    o += g(text(540, 420, "GRAVIDADE", 150, fill="#ff4fa3", font=FONT_COND, stroke=INK, sw=14), id=f"{p}gt")
    for x in (240, 540, 840):
        o += g(path(f"M{x-40},560 L{x+40},560 L{x+40},760 L{x+80},760 L{x},860 L{x-80},760 L{x-40},760 Z", "#ff4fa3", INK, 6),
               id=f"{p}ar{x}")
        S(f"tl.fromTo('#{p}ar{x}',{{y:-30}},{{y:30,duration:.3,repeat:{int(S.d/.3)},yoyo:true}},{jt(S.t0)})")
    o += person(f"{p}a", "leo", 540, 1580, 1.6, "angry", pose="shrug")
    S(f"tl.fromTo('#{p}a-j',{{scaleY:1}},{{scaleY:.78,scaleX:1.12,duration:.35,ease:'power2.in',transformOrigin:'50% 50%'}},{jt(S.t0+.1)})")
    S(f"tl.fromTo('#{p}gt',{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:.2,ease:'power3.in',transformOrigin:'50% 50%'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 1000), .05
    return o


def s7_lua(S):
    p = S.p
    o = bg("telhado")
    o += g(text(620, 680, "x6", 150, fill="#3cff5a", font=FONT_COND, stroke=INK, sw=14), id=f"{p}x6", extra='opacity="0"')
    o += person(f"{p}a", "leo", 380, 1620, 1.6, "happy", flip=False)
    S(f"tl.to('#{p}a-head',{{rotation:-12,duration:.4,transformOrigin:'50% 50%'}},{jt(S.t0+.1)})")
    S(f"PZ('{p}a','pointup',{jt(S.T('Lua'))})")
    S(f"tl.fromTo('#{p}x6',{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.25,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('seis'))})")
    S.focus, S.zoom = (540, 700), .04
    return o


def s7_cofrinho(S):
    p = S.p
    S.rain = False
    o = bg("sala") + bokeh(p, 11, 6, cols=("#ffd36b",))
    o += rect(-300, 1300, W + 600, 40, "#6b4423") + rect(-300, 1340, W + 600, 700, "#4a2f1a")
    pig = (ell(0, 0, 180, 140, "#ff8fb8", INK, 8) + circ(150, -20, 60, "#ff8fb8", INK, 7) + ell(190, -10, 22, 18, "#ff6f9f", INK, 4) +
           circ(140, -50, 9, INK) + path("M-60,-140 L-10,-140 L-20,-120 L-50,-120 Z", INK) +
           "".join(rect(x, 110, 40, 70, "#ff8fb8", rx=8, stroke=INK, sw=6) for x in (-130, -40, 40, 100)))
    o += g(g(pig, id=f"{p}pig"), tr="translate(400,1130)")
    for k in range(10):
        o += g(ell(0, 0, 32, 32, "#ffd23a", INK, 5) + text(0, 12, "$", 34, fill="#b8860b"), id=f"{p}c{k}",
               extra=f'opacity="0" transform="translate({400+(k-5)*40},1150)"')
    o += phone(f"{p}ph", 820, 1080, 1.1, title="SALDO", value="R$ 4.312,00", sub="TUDO QUE EU TENHO", clock="02:10")
    tq = S.T("tinha")
    S(f"tl.to('#{p}pig',{{rotation:8,duration:.06,repeat:5,yoyo:true,transformOrigin:'50% 50%'}},{jt(tq-.4)})")
    S(f"tl.to('#{p}pig',{{opacity:0,scale:1.3,duration:.12,transformOrigin:'50% 50%'}},{jt(tq)})")
    for k in range(10):
        S(f"tl.fromTo('#{p}c{k}',{{opacity:1,y:0}},{{y:{random.Random(k).randint(80,220)},x:'+={(k-5)*30}',duration:.45,ease:'bounce.out'}},{jt(tq)})")
    S.focus, S.zoom = (560, 1100), .05
    return o


def s7_foguete(S):
    p = S.p
    o = bg("foguete")
    o += tag(f"{p}tg", 540, 290, "PROMOÇÃO: SÓ IDA", 60)
    o += person(f"{p}a", "leo", 260, 1640, 1.1, "happy", pose="thumbs")
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('barato'))})")
    S.focus, S.zoom = (540, 900), .04
    return o


def moon_ground(p, y=1450):
    o = path(f"M-300,{y} Q200,{y-60} 540,{y-20} Q900,{y+20} 1400,{y-40} L1400,2200 L-300,2200 Z", "#a9a6b5", INK, 8)
    r = random.Random(y)
    for _ in range(10):
        x, yy = r.uniform(0, W), r.uniform(y + 60, H + 100)
        o += ell(x, yy, r.uniform(60, 150), r.uniform(14, 34), "#8b8899", INK, 4)
    return o


def s8_lua(S):
    p = S.p
    o = bg("lua")
    o += person(f"{p}a", "leo", 520, 1620, 1.6, "happy", helmet=True, pose="wave")
    o += g(ell(0, 0, 40, 14, "#6f6c7d"), id=f"{p}pe", extra='opacity="0" transform="translate(500,1640)"')
    S(f"tl.fromTo('#{p}a-j',{{y:-120}},{{y:0,duration:.6,ease:'power2.in'}},{jt(S.t0)})")
    S(f"tl.to('#{p}pe',{{opacity:1,duration:.1}},{jt(S.t0+.6)})")
    S.focus, S.zoom = (520, 1200), .05
    return o


def s8_agacha(S):
    p = S.p
    o = bg("lua")
    o += person(f"{p}a", "leo", 540, 2050, 3.0, "determined", helmet=True, pose="crouch")
    S(f"tl.to('#{p}a-j',{{scaleY:.82,duration:.6,ease:'power2.out',transformOrigin:'50% 50%'}},{jt(S.t0+.1)})")
    S.focus, S.zoom = (540, 1000), .06
    return o


def s8_salto(S):
    p = S.p
    o = bg("lua")
    o += g("".join(circ(540 + math.cos(a) * 140, 1520, 40, "#c9c6d4", INK, 4) for a in (0, 1, 2, 3, 4, 5)), id=f"{p}dust",
           extra='opacity="0"')
    o += person(f"{p}a", "leo", 540, 1560, 1.6, "determined", helmet=True)
    t = S.T("pulei")
    S(f"tl.to('#{p}a-j',{{scaleY:.8,duration:.15,svgOrigin:'0 0'}},{jt(t-.15)})")
    S(f"tl.to('#{p}a-j',{{scaleY:1.1,y:-1400,duration:1.1,ease:'power2.in'}},{jt(t)})")
    S(f"tl.set('#{p}a-armL',{{rotation:160,svgOrigin:'0 0'}},{jt(t)});tl.set('#{p}a-armR',{{rotation:-160,svgOrigin:'0 0'}},{jt(t)})")
    S(f"tl.fromTo('#{p}dust',{{opacity:1,scale:.5}},{{opacity:0,scale:1.8,duration:.6,transformOrigin:'50% 50%'}},{jt(t)})")
    S.push = (max(S.t0 + .05, t - .75), .6, 1.3, 540, 1050)
    S.focus, S.zoom = (540, 1200), .03
    return o


def s8_celular(S):
    p = S.p
    o = bg("espaco", .3) + bokeh(p, 12, 8, cols=("#3cff5a", "#39e5ff"))
    o += phone(f"{p}ph", 540, 1000, 2.0, title="PIX RECEBIDO", value="", sub="DE: A LUA", clock="03:33")
    vals = [("dez mil", "+R$ 10.000"), ("cem mil", "+R$ 100.000"), ("milhão", "+R$ 1.000.000")]
    for i, (nd, v) in enumerate(vals):
        o += g(text(540, 940, v, 92, fill="#18a64a", font=FONT_COND), id=f"{p}v{i}", extra='opacity="0"')
        t = S.T(nd.split()[0] if i < 2 else "milhão")
        S(f"tl.set('#{p}v{i}',{{opacity:1}},{jt(t)})")
        if i:
            S(f"tl.set('#{p}v{i-1}',{{opacity:0}},{jt(t)})")
        S(f"tl.fromTo('#{p}ph',{{x:-12}},{{x:12,duration:.05,repeat:5,yoyo:true}},{jt(t)})")
    S.focus, S.zoom = (540, 950), .07
    return o


def s8_subindo(S):
    p = S.p
    o = bg("espaco")
    o += g(moon(540, 1900, 700), id=f"{p}mn")
    o += g("".join(line(f"M{x},{y} l0,{L}", "#ffffff", 3, extra='opacity=".5"') for x, y, L in
                   [(random.Random(i).uniform(0, W), random.Random(i + 50).uniform(0, H), 160) for i in range(30)]), id=f"{p}st")
    o += person(f"{p}a", "leo", 540, 1050, 1.3, "happy", helmet=True, pose="up")
    S(f"tl.set('#{p}a-armL',{{rotation:160,transformOrigin:'50% 50%'}},{jt(S.t0)});tl.set('#{p}a-armR',{{rotation:-160,svgOrigin:'0 0'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}mn',{{scale:1}},{{scale:.15,duration:{S.d:.2f},ease:'power1.out',transformOrigin:'50% 50%'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}st',{{y:-400}},{{y:400,duration:.5,ease:'none',repeat:{int(S.d/.5)}}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 900), .02
    return o


def s9_flutua(S):
    p = S.p
    o = bg("espaco")
    o += g(person(f"{p}a", "leo", 540, 1150, 1.6, "happy", helmet=True, pose="float"), id=f"{p}fl")
    S(f"tl.fromTo('#{p}fl',{{rotation:-8}},{{rotation:14,duration:{S.d:.2f},ease:'sine.inOut',svgOrigin:'540 950'}},{jt(S.t0)})")
    r = random.Random(2)
    k = 0
    t = S.t0 + .2
    while t < S.t1 - .6:
        o += money(f"{p}m{k}", r.uniform(220, 860), r.uniform(300, 600), f"+R$ {r.choice(['1.000','2.500','5.000','10.000'])}", 70)
        S(f"M('{p}m{k}',{jt(t)},.45)")
        t += .55
        k += 1
    S.focus, S.zoom = (540, 900), .04
    return o


def s9_ranking(S):
    p = S.p
    o = bg("espaco")
    o += ranking(f"{p}rk", 540, 340, [("1º", "LÉO", "R$ 900.000.001", "leo"), ("2º", "O CANGURU", "R$ 900.000.000", "?"),
                                      ("3º", "KÁTIA MOLA", "R$ 48.000.000", "atleta")], s=1.25, hi=0)
    S(f"tl.from('#{p}rk',{{scale:1.6,opacity:0,duration:.3,ease:'power3.out',transformOrigin:'50% 0%'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 700), .05
    return o


def s9_viu(S):
    p = S.p
    o = bg("espaco", .2)
    o += person(f"{p}a", "leo", 540, 2350, 4.0, "happy", helmet=True, alt=("shock",))
    S(f"F('{p}a','happy','shock',{jt(S.T('vi'))})")
    S(f"tl.to('#{p}a-head',{{rotation:10,duration:.3,transformOrigin:'50% 50%'}},{jt(S.T('vi'))})")
    S.focus, S.zoom = (540, 900), .06
    return o


def s9_canguru(S):
    p = S.p
    o = bg("espaco", .2)
    o += g(person(f"{p}a", "canguru", 540, 1650, 2.2, "smile") +
           g(phone(f"{p}ph", 0, 0, .35, title="PIX RECEBIDO", value="+R$ 5.000", hand=False), tr="translate(640,1150) rotate(10)"),
           id=f"{p}fl")
    o += tag(f"{p}tg", 540, 400, "O CANGURU", 70)
    S(f"PZ('{p}a','phone',{jt(S.t0)},0)")
    S(f"tl.fromTo('#{p}fl',{{y:30,rotation:-4}},{{y:-30,rotation:4,duration:{S.d:.2f},ease:'sine.inOut',svgOrigin:'540 1100'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}tg',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(3)',transformOrigin:'50% 50%'}},{jt(S.T('Canguru'))})")
    S.focus, S.zoom = (540, 1000), .045
    return o


def s9_juntos(S):
    p = S.p
    o = bg("espaco")
    # empilhado na vertical: Canguru em cima, Léo embaixo
    o += g(person(f"{p}c", "canguru", 400, 1060, 1.3, "smile", alt=("happy",), pose="wave"), id=f"{p}fc")
    o += g(person(f"{p}a", "leo", 660, 1560, 1.4, "shock", helmet=True, alt=("neutral",), pose="float"), id=f"{p}fa")
    bal = g(path("M-330,-110 L330,-110 Q360,-110 360,-80 L360,60 Q360,90 330,90 L-90,90 L-150,150 L-140,90 L-330,90 Q-360,90 -360,60 L-360,-80 Q-360,-110 -330,-110 Z",
                 "#ffffff", INK, 7) + text(0, -12, "TRINTA ANOS,", 62, fill=INK) + text(0, 62, "GAROTO.", 62, fill=INK),
            id=f"{p}bal", extra='opacity="0"')
    o += g(bal, tr="translate(600,330)")
    S(f"F('{p}c','smile','happy',{jt(S.T('sorriu'))})")
    S(f"tl.fromTo('#{p}bal',{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.22,ease:'back.out(2.5)',transformOrigin:'20% 100%'}},{jt(S.T('Trinta'))})")
    S(f"F('{p}a','shock','neutral',{jt(S.T('esperando'))});PZ('{p}a','shrug',{jt(S.T('esperando'))})")
    S(f"tl.fromTo('#{p}fc',{{y:-20}},{{y:20,duration:1.6,repeat:{int(S.d/1.6)},yoyo:true,ease:'sine.inOut'}},{jt(S.t0)})")
    S(f"tl.fromTo('#{p}fa',{{y:20}},{{y:-20,duration:1.4,repeat:{int(S.d/1.4)},yoyo:true,ease:'sine.inOut'}},{jt(S.t0)})")
    S.focus, S.zoom = (540, 1000), .025
    return o


def s10_olha(S):
    p = S.p
    o = bg("espaco")
    o += person(f"{p}a", "leo", 540, 2050, 3.2, "sad", helmet=True)
    r = random.Random(4)
    for k in range(8):
        o += g(rect(-60, -30, 120, 60, "#3cae5a", rx=6, stroke=INK, sw=4) + text(0, 14, "$", 40, fill="#0b4a1c"),
               id=f"{p}n{k}", extra=f'transform="translate({r.uniform(80,1000):.0f},{r.uniform(200,900):.0f}) rotate({r.uniform(-40,40):.0f})"')
        S(f"tl.to('#{p}n{k}',{{rotation:'+={r.choice([-1,1])*90}',y:'+={r.randint(-80,80)}',duration:{S.d:.2f},ease:'none'}},{jt(S.t0)})")
    S(f"tl.to('#{p}a-head',{{rotation:8,duration:.6,transformOrigin:'50% 50%'}},{jt(S.t0+.3)})")
    S.focus, S.zoom = (540, 900), .04
    return o


def s10_escolha(S):
    p = S.p
    o = bg("espaco", .2)
    o += person(f"{p}c", "canguru", 300, 1560, .9, "smile", pose="wave")
    o += person(f"{p}a", "leo", 780, 1600, .9, "neutral", helmet=True, pose="chin")
    card = (text(540, 330, "E AGORA?", 120, fill="#ffd23a", font=FONT_COND, stroke=INK, sw=18) +
            g(rect(-230, -170, 460, 340, "#2b55c9", rx=36, stroke=INK, sw=8) +
              text(0, -30, "VOLTAR", 92, fill="#fff", font=FONT_COND, stroke=INK, sw=10) +
              text(0, 60, "PRA TERRA", 54, fill="#cfe0ff", font=FONT_COND), id=f"{p}oa", extra='transform="translate(290,640)"') +
            g(rect(-230, -170, 460, 340, "#ffd23a", rx=36, stroke=INK, sw=8) +
              text(0, -30, "FICAR", 92, fill=INK, font=FONT_COND) +
              text(0, 60, "NO ESPAÇO", 54, fill="#5a3a00", font=FONT_COND), id=f"{p}ob", extra='transform="translate(790,640)"') +
            text(540, 960, "COMENTA AÍ", 84, fill="#fff", font=FONT_COND, stroke=INK, sw=14))
    o += g(card, id=f"{p}card", extra='opacity="0"')
    S(f"tl.fromTo('#{p}card',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:'back.out(1.8)',transformOrigin:'50% 50%'}},{jt(S.t0+.1)})")
    S(f"tl.fromTo('#{p}oa',{{rotation:-4}},{{rotation:4,duration:.6,repeat:{int(S.d/.6)},yoyo:true,ease:'sine.inOut',transformOrigin:'50% 50%'}},{jt(S.t0+.3)})")
    S(f"tl.fromTo('#{p}ob',{{rotation:4}},{{rotation:-4,duration:.6,repeat:{int(S.d/.6)},yoyo:true,ease:'sine.inOut',transformOrigin:'50% 50%'}},{jt(S.t0+.3)})")
    S.focus, S.zoom = (540, 900), .015
    return o


# ============================================================== montagem
FONTFACE = """@font-face{font-family:OSans;src:url(../assets/fonts/OpenSans-ExtraBold.woff2) format('woff2');font-weight:800}
@font-face{font-family:Oswald;src:url(../assets/fonts/Oswald-Bold.woff2) format('woff2');font-weight:700}
@font-face{font-family:Nunito;src:url(../assets/fonts/Nunito-Black.woff2) format('woff2');font-weight:900}"""

JS_HELPERS = """
const POSES={
 rest:{aL:[8,-14],aR:[-8,14],lL:[3,-3],lR:[-3,3],h:['fist','fist']},
 umbrella:{aL:[8,-14],aR:[-10,100],lL:[3,-3],lR:[-3,3],h:['open','fist']},
 up:{aL:[160,12],aR:[-160,-12],lL:[6,-4],lR:[-6,4],h:['open','open']},
 thumbs:{aL:[8,-14],aR:[-35,-115],lL:[3,-3],lR:[-3,3],h:['open','thumb']},
 cross:{aL:[-14,-100],aR:[14,100],lL:[4,-3],lR:[-4,3],h:['fist','fist']},
 chin:{aL:[-14,-96],aR:[22,150],lL:[3,-3],lR:[-3,3],h:['fist','fist']},
 point:{aL:[8,-14],aR:[-82,-6],lL:[3,-3],lR:[-3,3],h:['open','point']},
 pointup:{aL:[8,-14],aR:[-150,-18],lL:[3,-3],lR:[-3,3],h:['open','point']},
 hips:{aL:[38,-80],aR:[-38,80],lL:[8,-4],lR:[-8,4],h:['fist','fist']},
 wave:{aL:[8,-14],aR:[-125,-35],lL:[3,-3],lR:[-3,3],h:['open','open']},
 peace:{aL:[30,-70],aR:[-125,-30],lL:[3,-3],lR:[-3,3],h:['fist','peace']},
 shrug:{aL:[50,-112],aR:[-50,112],lL:[3,-3],lR:[-3,3],h:['open','open']},
 fists:{aL:[14,-70],aR:[-14,70],lL:[8,-4],lR:[-8,4],h:['fist','fist']},
 phone:{aL:[8,-14],aR:[6,118],lL:[3,-3],lR:[-3,3],h:['open','fist']},
 crouch:{aL:[30,-40],aR:[-30,40],lL:[24,-24],lR:[-24,24],h:['fist','fist']},
 float:{aL:[70,-30],aR:[-70,30],lL:[14,-30],lR:[-10,24],h:['open','open']},
 fall:{aL:[150,-40],aR:[-120,30],lL:[30,-16],lR:[-18,30],h:['open','open']},
};
const CUR={};const HS=['open','fist','point','thumb','peace'];
const RO={svgOrigin:'0 0',smoothOrigin:false};
function PZ(p,name,t,d){d=(d===undefined)?.25:d;const P=POSES[name];const s='#'+p;CUR[p]=name;
 const set=(sel,v)=>{ if(d>0) tl.to(sel,Object.assign({rotation:v,duration:d,ease:'power2.inOut'},RO),t); else tl.set(sel,Object.assign({rotation:v},RO),t);};
 set(s+'-armL',P.aL[0]);set(s+'-armL2',P.aL[1]);set(s+'-armR',P.aR[0]);set(s+'-armR2',P.aR[1]);
 set(s+'-legL',P.lL[0]);set(s+'-legL2',P.lL[1]);set(s+'-legR',P.lR[0]);set(s+'-legR2',P.lR[1]);
 ['L','R'].forEach((k,i)=>HS.forEach(h=>tl.set(s+'-h'+k+'-'+h,{opacity:h===P.h[i]?1:0},t+d*.5)));}
function J(p,t,h,up){up=up||Math.max(.22,Math.sqrt(h)/42);const j='#'+p+'-j',a='#'+p+'-armL',b='#'+p+'-armR';
 const P=POSES[CUR[p]||'rest'];
 tl.to(j,Object.assign({scaleY:.86,duration:.07},RO),t);
 tl.to(['#'+p+'-legL2','#'+p+'-legR2'],{rotation:(i)=>i?28:-28,duration:.07,svgOrigin:'0 0',smoothOrigin:false},t);
 tl.to(j,Object.assign({scaleY:1.05,y:-h,duration:up,ease:'power2.out'},RO),t+.07);
 tl.to(['#'+p+'-legL2','#'+p+'-legR2'],{rotation:(i)=>i?-10:10,duration:up*.6,svgOrigin:'0 0',smoothOrigin:false},t+.07);
 tl.to(a,Object.assign({rotation:150,duration:.14},RO),t+.05);tl.to(b,Object.assign({rotation:-150,duration:.14},RO),t+.05);
 tl.to(j,Object.assign({scaleY:1,y:0,duration:up,ease:'power2.in'},RO),t+.07+up);
 tl.to(a,Object.assign({rotation:P.aL[0],duration:.18},RO),t+.07+up*1.3);tl.to(b,Object.assign({rotation:P.aR[0],duration:.18},RO),t+.07+up*1.3);
 tl.to(['#'+p+'-legL2','#'+p+'-legR2'],{rotation:(i)=>i?P.lR[1]:P.lL[1],duration:.2,svgOrigin:'0 0',smoothOrigin:false},t+.07+2*up);
 tl.to(j,Object.assign({scaleY:.9,duration:.05},RO),t+.07+2*up);tl.to(j,Object.assign({scaleY:1,duration:.1},RO),t+.12+2*up);}
function IDLE(p,t0,t1,ph,blink){const n=(per)=>Math.max(1,Math.floor((t1-t0)/per));
 tl.fromTo('#'+p+'-br',{scaleY:1},Object.assign({scaleY:1.016,duration:1.3,repeat:n(1.3),yoyo:true,ease:'sine.inOut',immediateRender:false},RO),t0+ph*.5);
 tl.fromTo('#'+p+'-hb',{rotation:-2.2},Object.assign({rotation:2.2,duration:1.7,repeat:n(1.7),yoyo:true,ease:'sine.inOut',immediateRender:false},RO),t0+ph);
 tl.fromTo(['#'+p+'-wL','#'+p+'-wR'],{rotation:-5},Object.assign({rotation:5,duration:1.1,repeat:n(1.1),yoyo:true,ease:'sine.inOut',immediateRender:false},RO),t0+ph*.7);
 if(blink){for(let t=t0+.6+ph;t<t1-.2;t+=2.6+ph){tl.set('#'+p+'-blink',{opacity:1},t);tl.set('#'+p+'-blink',{opacity:0},t+.09);}}}
function M(id,t,hold){const s='#'+id;
 tl.fromTo(s,{opacity:0,scale:.5,y:0},{opacity:1,scale:1.15,duration:.12,ease:'back.out(3)',transformOrigin:'50% 50%',immediateRender:false},t);
 tl.to(s,{scale:1,duration:.08,transformOrigin:'50% 50%'},t+.12);
 tl.to(s,{y:-80,opacity:0,duration:.35,ease:'power1.in'},t+.2+hold);}
function F(p,a,b,t){tl.set('#'+p+'-fx-'+a,{opacity:0},t);tl.set('#'+p+'-fx-'+b,{opacity:1},t);}
"""


def build_scene(sc):
    c = sc["chunks"]
    cur = 0
    starts = []
    for needle, fn in sc["shots"]:
        if needle is None:
            starts.append((0.0, fn))
            continue
        while needle.upper() not in c[cur][2]:
            cur += 1
            if cur >= len(c):
                raise KeyError(f"{sc['id']}: gatilho '{needle}' não achado")
        starts.append((c[cur][0], fn))
    shots = []
    for i, (t0, fn) in enumerate(starts):
        t1 = starts[i + 1][0] if i + 1 < len(starts) else sc["dur"]
        S = Shot(sc, fn, t0, t1, f"{sc['id']}{chr(97+i)}")
        chars.CREATED.clear()
        S.svg = globals()[fn](S)
        S.people = list(chars.CREATED)
        shots.append(S)
    p = sc["id"]
    D = sc["dur"]
    svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">', defs(p)]
    js = [f"const tl=gsap.timeline({{paused:true}});", JS_HELPERS]
    for S in shots:
        svg.append(f'<g id="{S.p}" style="visibility:hidden"><g id="{S.p}-cam">{S.svg}</g></g>')
        js.append(f"tl.set('#{S.p}',{{visibility:'visible'}},{jt(S.t0)});")
        if S is not shots[-1]:
            js.append(f"tl.set('#{S.p}',{{visibility:'hidden'}},{jt(S.t1)});")
        fx, fy = S.focus
        z = lambda tt: 1 + S.zoom * (tt - S.t0)
        if sc.get("rain"):
            js.append(f"tl.set('#{p}-rain',{{visibility:'{'visible' if S.rain else 'hidden'}'}},{jt(S.t0)});")
        cam = f"'#{S.p}-cam'"
        if S.push:
            t, d, zs, px, py = S.push
            js.append(f"tl.fromTo({cam},{{scale:1,y:0}},{{scale:{z(t):.4f},duration:{max(.01,t-S.t0):.3f},ease:'none',svgOrigin:'{fx} {fy}'}},{jt(S.t0)});")
            js.append(f"tl.to({cam},{{scale:{zs*z(t):.4f},duration:{d:.3f},ease:'power2.inOut',svgOrigin:'{px} {py}'}},{jt(t)});")
        elif S.d > 3.4 and S.punch:
            # corte "punch-in" no meio do plano (ritmo do estilo: corte a cada ~2 s)
            m = S.t0 + S.d * .5
            js.append(f"tl.fromTo({cam},{{scale:1,y:0}},{{scale:{z(m):.4f},y:{S.dy/2:.1f},duration:{m-S.t0:.3f},ease:'none',svgOrigin:'{fx} {fy}'}},{jt(S.t0)});")
            js.append(f"tl.fromTo({cam},{{scale:{z(m)*1.22:.4f},y:{S.dy/2:.1f}}},{{scale:{z(S.t1)*1.22:.4f},y:{S.dy},duration:{S.t1-m:.3f},ease:'none',svgOrigin:'{fx} {fy}',immediateRender:false}},{jt(m)});")
        else:
            js.append(f"tl.fromTo({cam},{{scale:1,y:0}},{{scale:{z(S.t1):.4f},y:{S.dy},duration:{S.d:.3f},ease:'none',svgOrigin:'{fx} {fy}'}},{jt(S.t0)});")
        rr = random.Random(S.p)
        for k, (pid, pose) in enumerate(S.people):
            js.append(f"PZ('{pid}','{pose}',{jt(S.t0)},0);")
            js.append(f"IDLE('{pid}',{jt(S.t0)},{jt(S.t1)},{rr.uniform(0,.8):.2f},{'true' if k < 4 else 'false'});")
        js.extend(x + ";" for x in S.js)
    if sc.get("rain"):
        svg.append(rain(p, hash(p) % 100, D))
        js.append(f"tl.fromTo('#{p}-rain',{{y:-600}},{{y:0,duration:.5,ease:'none',repeat:{int(D/.5)}}},0);")
    svg.append("</svg>")
    js.append(f"tl.set({{}},{{}},{D:.3f});")
    js.append(f'window.__timelines["{p}"]=tl;')
    js = [x.replace("transformOrigin:", "smoothOrigin:false,transformOrigin:") for x in js]
    js = [x if "-cam" in x else x.replace("svgOrigin:", "smoothOrigin:false,svgOrigin:") for x in js]
    html = f"""<template>
<style>{FONTFACE}
#root{{position:absolute;inset:0;overflow:hidden;background:#0d0912}}
#root svg{{position:absolute;left:0;top:0}}
</style>
<div id="root" data-composition-id="{p}" data-width="{W}" data-height="{H}">
{''.join(svg)}
</div>
<script>
{chr(10).join(js)}
</script></template>"""
    open(os.path.join(ROOT, "compositions", f"{p}.html"), "w").write(html)
    return shots


def build_captions():
    rows = []
    k = 0
    for sc in SCENES:
        for a, b, txt in sc["chunks"]:
            st = sc["start"] + a
            en = sc["start"] + b
            rows.append(f'<div id="cap-{k}" class="clip cap" data-start="{st:.3f}" data-duration="{en-st:.3f}">'
                        f'<span class="w">{txt}</span></div>')
            k += 1
    html = f"""<template>
<style>{FONTFACE}
#root{{position:absolute;inset:0;pointer-events:none}}
.cap{{position:absolute;left:0;top:1335px;width:100%;text-align:center}}
.w{{display:inline-block;font-family:OSans;font-weight:800;font-size:60px;line-height:1.2;color:#fff;
  -webkit-text-stroke:7px #141018;paint-order:stroke fill;text-shadow:0 5px 12px rgba(0,0,0,.65);letter-spacing:.5px}}
</style>
<div id="root" data-composition-id="legendas" data-width="{W}" data-height="{H}">
{chr(10).join(rows)}
</div>
<script>window.__timelines["legendas"]=gsap.timeline({{paused:true}}).set({{}},{{}},{TOTAL:.3f});</script></template>"""
    open(os.path.join(ROOT, "compositions", "legendas.html"), "w").write(html)


def build_index():
    rows = []
    for i, sc in enumerate(SCENES):
        rows.append(f'<div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
                    f'data-start="{sc["start"]:.3f}" data-duration="{sc["dur"]:.3f}" data-track-index="0" '
                    f'data-width="{W}" data-height="{H}" style="z-index:1"></div>')
    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="assets/lib/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
#vinheta{{position:absolute;inset:0;z-index:5;pointer-events:none;
 background:radial-gradient(ellipse 85% 70% at 50% 45%,rgba(0,0,0,0) 55%,rgba(5,3,10,.72) 100%),
 linear-gradient(180deg,rgba(0,0,0,0) 62%,rgba(6,4,12,.55) 80%,rgba(6,4,12,.75) 100%)}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}">
{chr(10).join(rows)}
<div id="vinheta"></div>
<div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:6"></div>
</div><script>window.__timelines["main"]=gsap.timeline({{paused:true}}).set({{}},{{}},{TOTAL:.3f});</script></body></html>"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)


def build_narration(all_shots):
    out = ["E SE o mundo te pagasse pra pular?  (narração com tempos — vídeo sem voz)",
           f"Duração total: {TOTAL:.1f} s · 1080x1920 · 30 fps", ""]
    for sc, shots in zip(SCENES, all_shots):
        out.append(f"[{sc['start']:6.2f} – {sc['start']+sc['dur']:6.2f}]  {sc['text']}")
        for a, b, txt in sc["chunks"]:
            out.append(f"      {sc['start']+a:6.2f}  {txt}")
        out.append("")
    out.append("Planos (corte seco):")
    for sc, shots in zip(SCENES, all_shots):
        for S in shots:
            out.append(f"  {sc['start']+S.t0:6.2f}  {S.name}")
    open(os.path.join(ROOT, "narracao.txt"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    all_shots = [build_scene(sc) for sc in SCENES]
    build_captions()
    build_index()
    build_narration(all_shots)
    n = sum(len(s) for s in all_shots)
    print(f"ok: {len(SCENES)} cenas, {n} planos, {TOTAL:.2f} s (média {TOTAL/n:.2f} s por plano)")
    for sc in SCENES:
        print(f"  {sc['id']:4s} {sc['start']:7.2f} +{sc['dur']:.2f}")
