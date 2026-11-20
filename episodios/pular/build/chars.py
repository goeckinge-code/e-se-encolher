"""Personagens v3 — cartoon articulado (referência do dono do canal): contorno preto grosso,
cabeça grande, olhos grandes com brilho, tênis grandões; corpo de recorte com articulações.

Rig (pés em 0,0; cada articulação gira em torno da própria origem local):
  {p}            posição/escala no quadro
  {p}-j          pulo/esmagar (origem nos pés)
  {p}-br         respiração (idle)
  {p}-legL/R     quadril  > {p}-legL2/R2 joelho
  {p}-armL/R     ombro    > {p}-armL2/R2 cotovelo > {p}-handL/R punho (mãos trocáveis {p}-hL-<forma>)
  {p}-head       pescoço  ; rostos {p}-fx-<expressão> ; olhos .eyes (piscar)
"""
from lib import g, path, circ, ell, rect, line, text, f, FONT_COND

OUTL = "#0b0a0e"
RIM = "#a9c4ff"
AMB = ""
HIP, SH, NECK = -170, -284, -296
CREATED = []          # personagens criados no plano atual: (id, pose) — o build adiciona idle/pose


def set_rim(c, amb=None):
    global RIM, AMB
    RIM = c
    if amb is not None:
        AMB = amb


def char_defs():
    return """
<linearGradient id="fx-cel"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".64" stop-color="#000" stop-opacity="0"/>
<stop offset=".65" stop-color="#1a0a20" stop-opacity=".26"/><stop offset="1" stop-color="#1a0a20" stop-opacity=".34"/></linearGradient>
<radialGradient id="fx-headc" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/>
<stop offset=".74" stop-color="#3a0a1a" stop-opacity="0"/><stop offset=".75" stop-color="#3a0a1a" stop-opacity=".18"/><stop offset="1" stop-color="#3a0a1a" stop-opacity=".26"/></radialGradient>
<linearGradient id="fx-rimg"><stop offset="0" stop-color="#000"/><stop offset=".7" stop-color="#000"/><stop offset=".95" stop-color="#fff"/></linearGradient>
<mask id="fx-rim" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#fx-rimg)"/></mask>
<radialGradient id="fx-blush"><stop offset="0" stop-color="#ff5a5a" stop-opacity=".4"/><stop offset="1" stop-color="#ff5a5a" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-contact"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
"""


def sh(d, base, sw=5.5, rim=True, cel="fx-cel"):
    """forma cartoon: contorno grosso + sombra chapada (cel) + luz de contorno fina"""
    o = path(d, base, OUTL, sw)
    o += f'<path d="{d}" fill="url(#{cel})"/>'
    if rim:
        o += f'<path d="{d}" fill="none" stroke="{RIM}" stroke-width="4" mask="url(#fx-rim)" opacity=".85"/>'
    return o


LOOKS = {
    "leo":    dict(shirt="#f2b51e", pants="#2f4f9a", shoe="#d8262c", hair="#24150e", skin="#c98a5e", eyes="#2a170c", acc="cap"),
    "vo":     dict(shirt="#7a3fbf", pants="#5a2c94", shoe="#5b3d8a", hair="#efeef4", skin="#ecbd99", eyes="#3d4e5e", acc="bun",
                   glasses=True, old=True, hoodie=True),
    "canguru": dict(shirt="#2a4fb0", pants="#2a4fb0", shoe="#2a4fb0", hair="#f4f4f4", skin="#efc3a0", eyes="#2c3e5a", acc="nightcap",
                    beard=True, old=True, robe=True, glasses=True),
    "exec":   dict(shirt="#1c1c24", pants="#1c1c24", shoe="#141018", hair="#1c120c", skin="#d9a27c", eyes="#21140a", acc="tie"),
    "girl":   dict(shirt="#f0609e", pants="#f0609e", shoe="#ffffff", hair="#6a3418", skin="#b97a55", eyes="#2a160a", acc="pigtails"),
    "atleta": dict(shirt="#17a596", pants="#2f4f9a", shoe="#ffffff", hair="#1d1410", skin="#8a5a3c", eyes="#1a0e06", acc="band", bare=True),
    "dono":   dict(shirt="#b81f34", pants="#1b1622", shoe="#141018", hair="#2a1d16", skin="#e2b08c", eyes="#21140a", acc="tophat",
                   stache=True, coat=True),
    "guard":  dict(shirt="#22252e", pants="#22252e", shoe="#000000", hair="#0e0c10", skin="#6e4a34", eyes="#000", acc="shades"),
}
LONG_SLEEVE = ("exec", "dono", "guard", "vo", "canguru")


# ------------------------------------------------------------------ rosto
def eye(ex, ey, iris, mode, skin, side):
    """olho grande cartoon: esclera alta, íris escura grande, dois brilhos, pálpebra grossa com 'cílio'"""
    flick = f"M{ex+side*17},{ey-10} l{side*7},-5"
    if mode in ("happy", "closed"):
        return line(f"M{ex-16},{ey+4} Q{ex},{ey-14} {ex+16},{ey+4}", OUTL, 6.5) + line(flick, OUTL, 4)
    w, h = (18, 21) if mode == "shock" else (16, 19)
    d = f"M{ex},{ey-h} C{ex+w},{ey-h} {ex+w},{ey+h} {ex},{ey+h} C{ex-w},{ey+h} {ex-w},{ey-h} {ex},{ey-h} Z"
    o = path(d, "#ffffff", OUTL, 3.2)
    ir = 8 if mode == "shock" else 12
    ix, iy = ex + side * -1.5, ey + 3
    o += circ(ix, iy, ir, iris) + circ(ix, iy, ir * .55, "#050304")
    o += circ(ix + 4, iy - 5, 4.2, "#ffffff") + circ(ix - 4, iy + 5, 1.8, "#ffffff", extra='opacity=".85"')
    if mode in ("determined", "angry"):
        o += path(f"M{ex-w-2},{ey-h-2} L{ex+w+2},{ey-h-2} L{ex+w+2},{ey-5} Q{ex},{ey-9} {ex-w-2},{ey-5} Z", skin)
        top = f"M{ex-w-2},{ey-5} Q{ex},{ey-9} {ex+w+2},{ey-5}"
    elif mode == "sad":
        a, b = (ey - 12, ey - 4) if side > 0 else (ey - 4, ey - 12)
        o += path(f"M{ex-w-2},{ey-h-2} L{ex+w+2},{ey-h-2} L{ex+w+2},{b} L{ex-w-2},{a} Z", skin)
        top = f"M{ex-w-2},{a} L{ex+w+2},{b}"
    else:
        top = f"M{ex-w},{ey-h*.55} Q{ex},{ey-h-6} {ex+w+2},{ey-h*.45}"
    return o + line(top, OUTL, 6) + line(flick, OUTL, 4)


def brows(mode, col):
    sets = {
        "angry": ("M-42,-34 Q-28,-34 -10,-22", "M42,-34 Q28,-34 10,-22"),
        "determined": ("M-42,-36 Q-28,-36 -10,-26", "M42,-36 Q28,-36 10,-26"),
        "sad": ("M-40,-28 Q-26,-38 -10,-40", "M40,-28 Q26,-38 10,-40"),
        "shock": ("M-40,-44 Q-26,-52 -10,-46", "M40,-44 Q26,-52 10,-46"),
    }
    a, b = sets.get(mode, ("M-40,-36 Q-26,-44 -10,-38", "M40,-36 Q26,-44 10,-38"))
    return line(a, col, 8) + line(b, col, 8)


def mouth(mode):
    if mode == "happy":
        return (path("M-20,30 Q0,34 20,30 Q16,52 0,54 Q-16,52 -20,30 Z", "#5a0f18", OUTL, 4) +
                path("M-15,32 Q0,35 15,32 L14,37 Q0,39 -14,37 Z", "#ffffff") + ell(0, 47, 9, 5, "#e2556a"))
    if mode == "smile":
        return line("M-16,32 Q0,44 16,32", OUTL, 5) + line("M-18,30 l-4,-3 M18,30 l4,-3", OUTL, 3.5)
    if mode == "shock":
        return ell(0, 40, 10, 13, "#4e0e16", OUTL, 4) + ell(0, 46, 6, 4, "#e2556a")
    if mode == "sad":
        return line("M-13,40 Q0,30 13,40", OUTL, 5)
    if mode == "angry":
        return path("M-17,38 Q0,28 17,38 Q0,42 -17,38 Z", "#4e0e16", OUTL, 4)
    if mode == "determined":
        return line("M-13,36 Q0,33 13,37", OUTL, 5)
    return line("M-11,36 Q0,39 11,36", OUTL, 4.5)


def face(p, kind, expr, lk):
    em = {"happy": "happy", "smile": "open", "shock": "shock", "sad": "sad", "determined": "determined",
          "angry": "angry"}.get(expr, "open")
    o = '<ellipse cx="-34" cy="22" rx="14" ry="8" fill="url(#fx-blush)"/><ellipse cx="34" cy="22" rx="14" ry="8" fill="url(#fx-blush)"/>'
    o += g(eye(-22, 2, lk["eyes"], em, lk["skin"], -1) + eye(22, 2, lk["eyes"], em, lk["skin"], 1), extra='class="eyes"')
    o += brows(expr, lk["hair"] if not lk.get("old") else "#c9c9d4")
    o += path("M2,14 Q8,24 1,27", "none", OUTL, 3.5)
    o += mouth(expr)
    if lk.get("old"):
        o += line("M-46,14 q5,6 2,12 M46,14 q-5,6 -2,12", OUTL, 2.5, extra='opacity=".6"')
    return o


# ------------------------------------------------------------------ cabeça e cabelo
HEAD_D = "M-60,-4 C-62,-54 -32,-74 0,-74 C32,-74 62,-54 60,-4 C58,32 36,60 0,66 C-36,60 -58,32 -60,-4 Z"


def star(sx, sy, r=8, col="#ffffff"):
    q = r * .3
    return path(f"M{sx},{sy-r} L{sx+q},{sy-q} L{sx+r},{sy} L{sx+q},{sy+q} L{sx},{sy+r} L{sx-q},{sy+q} L{sx-r},{sy} L{sx-q},{sy-q} Z", col)


def head_art(p, kind, expr, alt, lk, helmet):
    acc = lk.get("acc")
    c = lk["hair"]
    o = ""
    if acc == "pigtails":
        o += path("M-56,-40 Q-104,-30 -96,30 Q-90,50 -74,40 Q-84,0 -54,-12 Z", c, OUTL, 5) + circ(-58, -36, 7, "#e2306a", OUTL, 3)
        o += path("M56,-40 Q104,-30 96,30 Q90,50 74,40 Q84,0 54,-12 Z", c, OUTL, 5) + circ(58, -36, 7, "#e2306a", OUTL, 3)
    if acc == "bun":
        o += circ(0, -84, 26, c, OUTL, 5) + line("M-14,-92 Q0,-102 14,-92", "#c8c6d2", 3)
    if acc == "cap":
        o += path("M-60,-10 Q-66,20 -54,34 L-50,6 Z M60,-10 Q66,20 54,34 L50,6 Z", c, OUTL, 4)
    o += ell(-60, 6, 11, 16, lk["skin"], OUTL, 4.5) + ell(60, 6, 11, 16, lk["skin"], OUTL, 4.5)
    o += path(HEAD_D, lk["skin"], OUTL, 6)
    o += f'<path d="{HEAD_D}" fill="url(#fx-headc)"/>'
    o += f'<path d="{HEAD_D}" fill="none" stroke="{RIM}" stroke-width="4" mask="url(#fx-rim)" opacity=".85"/>'
    o += g(face(p, kind, expr, lk), id=f"{p}-fx-{expr}")
    for e in alt:
        o += g(face(p, kind, e, lk), id=f"{p}-fx-{e}", extra='opacity="0"')
    if acc in ("tie", "band", "shades", "pigtails"):
        o += path("M-62,-6 C-68,-58 -34,-86 2,-84 C40,-84 68,-58 62,-6 Q56,-34 40,-44 Q34,-28 16,-40 Q8,-24 -8,-38 "
                  "Q-20,-24 -32,-40 Q-46,-30 -52,-36 Q-60,-22 -62,-6 Z", c, OUTL, 5.5)
        o += line("M-26,-68 Q-6,-78 20,-70", "#ffffff", 3, extra='opacity=".2"')
    if acc == "band":
        o += rect(-62, -42, 124, 16, "#ffffff", rx=6, stroke=OUTL, sw=4)
    if acc == "bun":
        o += path("M-62,0 C-66,-56 -34,-82 0,-80 C34,-82 66,-56 62,0 Q50,-42 0,-46 Q-50,-42 -62,0 Z", c, OUTL, 5.5)
        o += line("M-42,-36 Q-12,-60 34,-48 M-24,-62 Q8,-72 40,-58", "#c8c6d2", 3)
    if acc == "cap":
        o += path("M-50,-30 Q-40,-14 -30,-26 Q-24,-12 -14,-24 L-12,-36 Z", c, OUTL, 4)
        o += sh("M-64,-20 C-68,-70 -32,-92 4,-92 C40,-92 68,-70 64,-20 Q0,-34 -64,-20 Z", "#d8262c", sw=6)
        o += line("M-62,-34 Q0,-46 62,-34", "#9e1a1e", 4) + circ(4, -91, 6, "#9e1a1e", OUTL, 3)
        o += path("M-8,-28 Q46,-40 104,-24 Q96,-8 30,-12 Q4,-12 -8,-20 Z", "#b81e24", OUTL, 5.5)
        o += line("M2,-24 Q48,-32 96,-20", "#ffffff", 3, extra='opacity=".25"')
    if acc == "tophat":
        o += path("M-62,-6 C-66,-44 -34,-62 0,-62 C34,-62 66,-44 62,-6 Q50,-30 0,-32 Q-50,-30 -62,-6 Z", c, OUTL, 5)
        o += ell(0, -62, 88, 14, "#141018", OUTL, 5) + sh("M-52,-64 L-48,-178 L48,-178 L52,-64 Z", "#1c1620", sw=5)
        o += rect(-50, -94, 100, 18, "#b81f34", stroke=OUTL, sw=3)
    if acc == "nightcap":
        o += path("M-62,8 Q-72,-28 -50,-40 Q-56,-12 -52,14 Z M62,8 Q72,-28 50,-40 Q56,-12 52,14 Z", c, OUTL, 4)
        o += sh("M-60,-36 C-50,-96 26,-134 104,-126 Q70,-100 62,-36 Q0,-52 -60,-36 Z", "#2a4fb0", sw=5.5)
        o += star(-20, -70) + star(24, -92) + star(60, -110, 6) + star(-38, -48, 6)
        o += path("M-62,-34 Q0,-56 64,-34 L62,-18 Q0,-40 -62,-18 Z", "#f2f2f2", OUTL, 4)
        o += circ(108, -126, 16, "#ffffff", OUTL, 4)
    if lk.get("glasses"):
        o += circ(-22, 2, 21, "none", OUTL, 5) + circ(22, 2, 21, "none", OUTL, 5) + line("M-2,0 L2,0", OUTL, 5) + \
            line("M-34,-8 l8,-6 M10,-8 l8,-6", "#ffffff", 3, extra='opacity=".6"')
    if acc == "shades":
        o += path("M-48,-14 L48,-14 L44,14 Q24,20 6,8 L-6,8 Q-24,20 -44,14 Z", "#08080c", OUTL, 3) + line("M-36,-6 l16,0", "#ffffff", 3, extra='opacity=".45"')
    if lk.get("beard"):
        o += sh("M-54,10 Q-48,130 0,176 Q48,130 54,10 Q30,48 0,48 Q-30,48 -54,10 Z", "#f6f6f8", sw=5.5)
        o += path("M-34,30 Q-12,20 0,28 Q12,20 34,30 Q14,44 0,36 Q-14,44 -34,30 Z", "#f6f6f8", OUTL, 4)
        o += line("M-18,80 Q-12,120 -4,156 M16,80 Q12,120 4,156", "#c9c9d4", 3)
    if lk.get("stache"):
        o += path("M-40,26 Q-18,8 0,22 Q18,8 40,26 Q18,36 0,28 Q-18,36 -40,26 Z", "#2a1d16", OUTL, 3.5)
    if helmet:
        o += circ(0, -8, 112, "#bfe8ff", "#e8f6ff", 6, extra='fill-opacity=".13"')
        o += line("M-74,-66 Q-50,-96 -8,-106", "#ffffff", 11, extra='opacity=".7"') + line("M72,46 Q86,12 84,-24", "#ffffff", 5, extra='opacity=".35"')
    return o


# ------------------------------------------------------------------ mãos (punho na origem, dedos para +y)
def hand_shapes(p, side, skin):
    s = side
    shapes = {
        "open": (f"M-11,0 L11,0 L13,16 L{18*s},30 Q{20*s},36 {14*s},35 L9,26 L9,40 Q8,46 3,45 L2,30 L-2,44 Q-4,49 -8,46 L-7,30 "
                 f"L-12,40 Q-15,44 -18,40 L-13,22 Z"),
        "fist": "M-13,0 L13,0 Q17,10 15,24 Q12,32 0,32 Q-12,32 -15,24 Q-17,10 -13,0 Z",
        "point": "M-13,0 L13,0 Q17,10 15,22 Q12,28 4,28 L4,52 Q2,58 -3,56 L-4,28 Q-12,28 -15,22 Q-17,10 -13,0 Z",
        "thumb": (f"M-13,0 L13,0 Q17,10 15,24 Q12,32 0,32 Q-12,32 -15,24 Q-17,10 -13,0 Z "
                  f"M{-8*s},22 Q{-14*s},30 {-12*s},52 Q{-6*s},60 {-1*s},52 L{1*s},28 Z"),
        "peace": "M-13,0 L13,0 Q17,10 15,22 Q12,28 8,28 L12,52 Q11,58 6,56 L2,30 L-2,30 L-8,54 Q-12,58 -14,52 L-9,28 Q-14,26 -15,20 Q-17,10 -13,0 Z",
    }
    o = ""
    for k, d in shapes.items():
        inner = path(d, skin, OUTL, 4.5)
        if k in ("fist", "thumb"):
            inner += line("M-8,16 l16,0 M-8,23 l16,0", OUTL, 2.2, extra='opacity=".5"')
        o += g(inner, id=f"{p}-h{'L' if side < 0 else 'R'}-{k}", extra='' if k == "open" else 'opacity="0"')
    return o


# ------------------------------------------------------------------ corpo (peças renderizadas no Blender)
# Os personagens são modelados no Blender (blender/chars3d.py) e renderizados em peças;
# aqui as peças são montadas no esqueleto. A versão 100% SVG anterior ficou em chars_svg_v3.py.
KIND = {"leo": "leo", "vo": "vo", "canguru": "canguru", "exec": "exec", "girl": "bia", "bia": "bia",
        "atleta": "katia", "katia": "katia", "dono": "barao", "barao": "barao", "guard": "seguranca", "seguranca": "seguranca"}
BOX = {"head": (-140, 140, -320, 150), "torso": (-100, 100, -340, -30), "arm": (-34, 34, -30, 86),
       "fore": (-30, 30, -18, 74), "hand": (-44, 44, -38, 74), "thigh": (-36, 36, -20, 100), "shin": (-60, 60, -18, 104)}
EXPRS = ["neutral", "happy", "sad", "shock", "determined", "angry", "smile"]
HANDS = ["open", "fist", "point", "thumb", "peace"]


def img(name, file, part, mirror=False, id=None, hidden=False):
    x0, x1, y0, y1 = BOX[part]
    a = (f' id="{id}"' if id else "") + (' opacity="0"' if hidden else "")
    im = (f'<image{a} href="../assets/chars/{name}/{file}.png" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" '
          f'preserveAspectRatio="none"/>')
    return f'<g transform="scale(-1,1)">{im}</g>' if mirror else im


def person(p, kind="leo", x=0, y=0, s=1.0, expr="neutral", flip=False, shirt=None, umbrella=False,
           briefcase=False, hidden=False, alt=(), helmet=False, pose="rest"):
    name = KIND.get(kind, "exec")
    CREATED.append((p, "umbrella" if umbrella and pose == "rest" else pose))

    def leg(side):
        L = "L" if side < 0 else "R"
        m = side > 0
        knee = g(g(img(name, "shin", "shin", m), id=f"{p}-leg{L}2"), tr="translate(0,84)")
        return g(g(knee + img(name, "thigh", "thigh", m), id=f"{p}-leg{L}"), tr=f"translate({side*16},{HIP})")

    def arm(side):
        L = "L" if side < 0 else "R"
        m = side > 0
        hands = "".join(img(name, f"hand_{h}", "hand", m, id=f"{p}-h{L}-{h}", hidden=(h != "open")) for h in HANDS)
        extra = ""
        if umbrella and side > 0:
            extra += g(line("M0,16 L0,-260", "#222", 6) +
                       path("M-170,-260 Q0,-390 170,-260 Q85,-282 0,-260 Q-85,-282 -170,-260 Z", "#18161f", OUTL, 5) +
                       line("M-100,-322 Q0,-370 100,-322", "#4a4660", 3, extra='opacity=".7"'), tr="rotate(-90)")
        if briefcase and side < 0:
            extra += sh("M-42,30 L42,30 L42,86 L-42,86 Z", "#6b4423", sw=5, rim=False) + rect(-12, 18, 24, 14, "none", stroke=OUTL, sw=3.5)
        wrist = g(g(hands + extra, id=f"{p}-w{L}"), tr="translate(0,58)")
        elbow = g(g(wrist + img(name, "fore", "fore", m), id=f"{p}-arm{L}2"), tr="translate(0,66)")
        return g(g(elbow + img(name, "arm", "arm", m), id=f"{p}-arm{L}"), tr=f"translate({side*38},{SH+2})")

    faces = img(name, f"head_{expr}", "head", id=f"{p}-fx-{expr}")
    for e in alt:
        faces += img(name, f"head_{e}", "head", id=f"{p}-fx-{e}", hidden=True)
    faces += img(name, "blink", "head", id=f"{p}-blink", hidden=True)
    if helmet:
        faces += circ(0, -74, 112, "#bfe8ff", "#e8f6ff", 6, extra='fill-opacity=".13"')
        faces += line("M-74,-132 Q-50,-162 -8,-172", "#ffffff", 11, extra='opacity=".7"') + line("M72,-20 Q86,-54 84,-90", "#ffffff", 5, extra='opacity=".35"')
    head = g(g(g(faces, id=f"{p}-hb"), id=f"{p}-head"), tr=f"translate(0,{NECK})")
    body = leg(-1) + leg(1) + img(name, "torso", "torso") + arm(-1) + arm(1) + head
    inner = '<ellipse cx="0" cy="4" rx="70" ry="12" fill="url(#fx-contact)"/>' + g(g(body, id=f"{p}-br"), id=f"{p}-j")
    sc = f"scale({-s if flip else s},{s})"
    st = f' style="filter:{AMB}"' if AMB else ""
    return g(inner, id=p, tr=f"translate({f(x)},{f(y)}) {sc}", extra=('opacity="0"' if hidden else "") + st)
