"""Personagens redesenhados: 2D semi-realista (proporções mais naturais, olhos com íris,
sombreado de volume e luz de contorno vinda do fundo). Mesmo "rig" da versão de palito:
pés em (0,0); grupos {p}-j, {p}-armL/R (ombro), {p}-legL/R (quadril), {p}-head, {p}-fx-<expressão>."""
from lib import g, path, circ, ell, rect, line, text, f, FONT_COND

OUTL = "#1a1218"      # contorno marrom-escuro (mais "pintado" que preto puro)
RIM = "#a9c4ff"       # cor da luz de contorno (muda por cena: set_rim)
HIP, SH, HC = -175, -292, -362


AMB = ""              # filtro CSS de luz ambiente da cena (ex.: "brightness(.85) saturate(.9)")


def set_rim(c, amb=None):
    global RIM, AMB
    RIM = c
    if amb is not None:
        AMB = amb


def char_defs():
    """gradientes de volume e máscara da luz de contorno (vão no <defs> de cada cena)"""
    return """
<linearGradient id="fx-vol"><stop offset="0" stop-color="#fff" stop-opacity=".20"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/>
<stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></linearGradient>
<linearGradient id="fx-volv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".5" stop-color="#000" stop-opacity="0"/>
<stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
<radialGradient id="fx-headv" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/>
<stop offset=".8" stop-color="#5a1e1e" stop-opacity=".18"/><stop offset="1" stop-color="#2a0a14" stop-opacity=".42"/></radialGradient>
<linearGradient id="fx-rimg"><stop offset="0" stop-color="#000"/><stop offset=".62" stop-color="#000"/><stop offset=".9" stop-color="#fff"/></linearGradient>
<mask id="fx-rim" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#fx-rimg)"/></mask>
<radialGradient id="fx-blush"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".35"/><stop offset="1" stop-color="#ff6b6b" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-contact"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
"""


def sh(d, base, kind="", sw=4.5, rim=True):
    """forma com contorno + volume (claro à esquerda, escuro à direita) + luz de contorno à direita"""
    o = path(d, base, OUTL, sw)
    o += f'<path d="{d}" fill="url(#fx-vol{kind})"/>'
    if rim:
        o += f'<path d="{d}" fill="none" stroke="{RIM}" stroke-width="5" mask="url(#fx-rim)" opacity=".9"/>'
    return o


LOOKS = {
    "leo":    dict(shirt="#e9b13a", pants="#3b5a92", shoe="#d63a3a", hair="#2b1a12", skin="#c98e66", eyes="#4a2c18", acc="cap"),
    "vo":     dict(shirt="#7e55b8", pants="#4d3778", shoe="#3b2c55", hair="#ecebf2", skin="#e8b896", eyes="#5a6b7a", acc="bun", glasses=True, skirt=True, old=True),
    "canguru": dict(shirt="#a7c6f2", pants="#a7c6f2", shoe="#b84545", hair="#f4f4f4", skin="#efc3a0", eyes="#4c6a8a", acc="nightcap", beard=True, stripes=True, old=True),
    "exec":   dict(shirt="#4f5668", pants="#2f3440", shoe="#141018", hair="#2a1d16", skin="#d9a27c", eyes="#3a2414", acc="tie"),
    "girl":   dict(shirt="#f0609e", pants="#f0609e", shoe="#ffffff", hair="#5a2e16", skin="#b97a55", eyes="#3a2010", acc="pigtails", skirt=True),
    "atleta": dict(shirt="#17a596", pants="#174f8a", shoe="#ffffff", hair="#1d1410", skin="#8a5a3c", eyes="#2a1608", acc="band", bare_arms=True),
    "dono":   dict(shirt="#b81f34", pants="#1b1622", shoe="#141018", hair="#2a1d16", skin="#e2b08c", eyes="#3a2414", acc="tophat", stache=True, coat=True),
    "guard":  dict(shirt="#22252e", pants="#22252e", shoe="#000000", hair="#0e0c10", skin="#6e4a34", eyes="#000", acc="shades"),
}


# ------------------------------------------------------------------ rosto
def eye(ex, ey, iris, mode, side, skin="#c98e66"):
    """olho semi-realista: esclera, íris, pupila, brilho, pálpebra"""
    if mode == "closed":
        return line(f"M{ex-14},{ey+1} Q{ex},{ey-11} {ex+14},{ey+1}", OUTL, 4.5)
    if mode == "happy":
        return line(f"M{ex-14},{ey+3} Q{ex},{ey-12} {ex+14},{ey+3}", OUTL, 5) + line(f"M{ex-10},{ey+8} Q{ex},{ey+5} {ex+10},{ey+8}", OUTL, 2, extra='opacity=".5"')
    big = mode == "shock"
    h = 13 if big else 10
    w = 14 if not big else 15
    d = f"M{ex-w},{ey} Q{ex},{ey-h-4} {ex+w},{ey} Q{ex},{ey+h} {ex-w},{ey} Z"
    o = path(d, "#f7f3ee", OUTL, 2.5)
    ir = 5.2 if big else 7.6
    o += circ(ex + side, ey + 1, ir, iris) + circ(ex + side, ey + 1, ir * .48, "#0c0808")
    o += circ(ex + side + 2.6, ey - 2.4, 2.2, "#ffffff")
    # pálpebra superior (mais pesada quando triste/determinado)
    if mode in ("sad", "determined", "angry"):
        lid = f"M{ex-w-1},{ey-1} Q{ex},{ey-h-6} {ex+w+1},{ey-1} L{ex+w+1},{ey-3} Q{ex},{ey-3} {ex-w-1},{ey-1} Z"
        o += path(lid, skin, OUTL, 2.5)
    o += line(f"M{ex-w-1},{ey} Q{ex},{ey-h-5} {ex+w+1},{ey}", OUTL, 4.2)
    return o


def brows(mode, col):
    if mode in ("determined", "angry"):
        a = "M-36,-24 Q-24,-26 -8,-16 L-8,-12 Q-24,-20 -36,-19 Z"
        b = "M36,-24 Q24,-26 8,-16 L8,-12 Q24,-20 36,-19 Z"
    elif mode == "sad":
        a = "M-34,-20 Q-22,-28 -8,-30 L-8,-26 Q-22,-24 -34,-16 Z"
        b = "M34,-20 Q22,-28 8,-30 L8,-26 Q22,-24 34,-16 Z"
    elif mode == "shock":
        a = "M-34,-30 Q-22,-38 -8,-33 L-8,-29 Q-22,-33 -34,-26 Z"
        b = "M34,-30 Q22,-38 8,-33 L8,-29 Q22,-33 34,-26 Z"
    else:
        a = "M-34,-24 Q-22,-31 -8,-26 L-8,-22 Q-22,-26 -34,-20 Z"
        b = "M34,-24 Q22,-31 8,-26 L8,-22 Q22,-26 34,-20 Z"
    return path(a, col, OUTL, 1.5) + path(b, col, OUTL, 1.5)


def mouth(mode):
    if mode == "happy":
        return path("M-16,27 Q0,30 16,27 Q12,44 0,45 Q-12,44 -16,27 Z", "#6b1d24", OUTL, 3) + path("M-12,29 Q0,31 12,29 L11,33 Q0,35 -11,33 Z", "#fff")
    if mode == "smile":
        return line("M-13,30 Q0,38 13,30", OUTL, 3.5) + line("M-15,29 l-3,-2 M15,29 l3,-2", OUTL, 2.5)
    if mode == "shock":
        return ell(0, 35, 8, 11, "#4e141b", OUTL, 3)
    if mode == "sad":
        return line("M-11,35 Q0,28 11,35", OUTL, 3.5)
    if mode == "angry":
        return path("M-14,34 Q0,26 14,34 Q0,38 -14,34 Z", "#5a1a20", OUTL, 3)
    if mode == "determined":
        return line("M-11,32 Q0,30 11,33", OUTL, 3.5)
    return line("M-10,32 Q0,34 10,32", OUTL, 3.2)


def face(p, kind, expr, lk):
    eyes_mode = {"happy": "happy", "smile": "open", "shock": "shock", "sad": "sad", "determined": "determined",
                 "angry": "angry"}.get(expr, "open")
    side = 1.5
    o = ""
    o += f'<ellipse cx="-24" cy="16" rx="13" ry="8" fill="url(#fx-blush)"/><ellipse cx="24" cy="16" rx="13" ry="8" fill="url(#fx-blush)"/>'
    o += eye(-19, 0, lk["eyes"], eyes_mode, side, lk["skin"]) + eye(19, 0, lk["eyes"], eyes_mode, side, lk["skin"])
    o += brows(expr, lk["hair"] if not lk.get("old") else "#bdbdc8")
    # nariz com sombra lateral
    o += path("M3,4 Q10,17 3,22 Q-2,23 -6,20", "none", OUTL, 2.6) + path("M3,6 Q9,16 4,21 Q8,15 3,6 Z", "#000", extra='opacity=".18"')
    o += mouth(expr)
    if lk.get("old"):
        o += line("M-34,10 q4,6 2,12 M34,10 q-4,6 -2,12 M-30,-8 l-6,-3 M30,-8 l6,-3", OUTL, 1.8, extra='opacity=".55"')
    return o


# ------------------------------------------------------------------ corpo
def head_shape(lk, kind):
    d = "M-47,-8 C-49,-50 -27,-66 0,-66 C27,-66 49,-50 47,-8 C46,24 31,50 0,58 C-31,50 -46,24 -47,-8 Z"
    o = ell(-47, 2, 9, 14, lk["skin"], OUTL, 3.5) + ell(47, 2, 9, 14, lk["skin"], OUTL, 3.5)
    o += path(d, lk["skin"], OUTL, 4.5)
    o += f'<path d="{d}" fill="url(#fx-headv)"/>'
    o += f'<path d="{d}" fill="none" stroke="{RIM}" stroke-width="5" mask="url(#fx-rim)" opacity=".9"/>'
    return o


def hair_back(lk, acc):
    o = ""
    if acc == "pigtails":
        o += path("M-50,-30 Q-86,-10 -74,30 Q-62,10 -48,-6 Z", lk["hair"], OUTL, 3.5) + path("M50,-30 Q86,-10 74,30 Q62,10 48,-6 Z", lk["hair"], OUTL, 3.5)
    if acc == "bun":
        o += circ(0, -70, 24, lk["hair"], OUTL, 3.5) + line("M-14,-78 Q0,-88 14,-78", "#c8c6d2", 3)
    return o


def hair_front(lk, acc):
    c = lk["hair"]
    o = ""
    if acc in ("tie", "band", "shades", "pigtails", None):
        d = "M-49,-6 C-54,-48 -30,-74 2,-72 C34,-72 54,-50 49,-6 Q44,-30 30,-40 Q22,-28 6,-36 Q-6,-26 -20,-38 Q-32,-26 -42,-30 Q-48,-20 -49,-6 Z"
        o += path(d, c, OUTL, 4) + line("M-20,-58 Q-6,-66 14,-60 M18,-52 Q30,-50 38,-40", "#ffffff", 2.5, extra='opacity=".18"')
    if acc == "bun":
        d = "M-50,-2 C-54,-48 -30,-70 0,-68 C30,-70 54,-48 50,-2 Q42,-36 0,-40 Q-42,-36 -50,-2 Z"
        o += path(d, c, OUTL, 4) + line("M-36,-30 Q-10,-50 30,-40 M-20,-52 Q6,-60 34,-50", "#c8c6d2", 2.5)
    if acc == "cap":
        o += path("M-50,-4 Q-56,8 -48,20 L-44,6 Z M50,-4 Q56,8 48,20 L44,6 Z", c, OUTL, 3)
        cap = "M-52,-14 C-54,-58 -26,-76 2,-76 C30,-76 54,-58 52,-14 Q0,-26 -52,-14 Z"
        o += sh(cap, "#d63a3a", sw=4.5)
        o += line("M0,-75 L0,-20", "#9e2424", 2.5) + circ(0, -74, 5, "#9e2424", OUTL, 2)
        o += path("M-10,-20 Q40,-28 86,-12 Q60,-2 -6,-8 Z", "#a82a2a", OUTL, 4)
    if acc == "tophat":
        o += path("M-49,-8 C-52,-40 -30,-56 0,-56 C30,-56 52,-40 49,-8 Q40,-26 0,-28 Q-40,-26 -49,-8 Z", c, OUTL, 3.5)
        o += ell(0, -54, 74, 12, "#141018", OUTL, 4) + sh("M-44,-56 L-40,-160 L40,-160 L44,-56 Z", "#1c1620", sw=4)
        o += rect(-42, -82, 84, 16, "#b81f34")
    if acc == "nightcap":
        o += path("M-50,4 Q-58,-26 -40,-34 Q-46,-10 -42,10 Z M50,4 Q58,-26 40,-34 Q46,-10 42,10 Z", c, OUTL, 3)
        o += sh("M-48,-30 C-40,-80 20,-112 84,-106 Q56,-84 50,-30 Q0,-44 -48,-30 Z", "#3567c4", sw=4)
        o += path("M-50,-28 Q0,-46 52,-28 L50,-16 Q0,-34 -50,-16 Z", "#f2f2f2", OUTL, 3)
        o += circ(88, -106, 14, "#ffffff", OUTL, 3)
    return o


def person(p, kind="leo", x=0, y=0, s=1.0, expr="neutral", flip=False, shirt=None, umbrella=False,
           briefcase=False, hidden=False, alt=(), helmet=False):
    lk = dict(LOOKS.get(kind, LOOKS["exec"]))
    if shirt:
        lk["shirt"] = shirt
    skin = lk["skin"]
    acc = lk.get("acc")
    # ---- pernas
    def leg(side):
        o = sh("M-16,0 C-17,52 -14,112 -12,158 L12,158 C13,112 16,52 16,0 Z", lk["pants"], sw=4)
        o += line("M-8,84 Q0,88 8,84", OUTL, 2, extra='opacity=".45"')
        shoe = f"M-14,150 Q-17,170 -12,176 L{20*side+8 if side>0 else 6},176 Q{side*34},176 {side*32},166 Q{side*22},156 {side*4},150 Z" if False else \
            ("M-14,148 Q-18,170 -12,176 L30,176 Q40,175 37,165 Q30,156 10,150 Z" if side > 0 else
             "M14,148 Q18,170 12,176 L-30,176 Q-40,175 -37,165 Q-30,156 -10,150 Z")
        o += sh(shoe, lk["shoe"], sw=3.5, rim=False)
        o += path(("M-13,170 L36,170 Q36,176 30,177 L-12,177 Z" if side > 0 else "M13,170 L-36,170 Q-36,176 -30,177 L12,177 Z"),
                  "#f4f1ea", OUTL, 2.5)
        return g(g(o, id=f"{p}-leg{'L' if side < 0 else 'R'}"), tr=f"translate({side*17},{HIP})")
    legs = leg(-1) + leg(1)
    # ---- tronco
    if lk.get("skirt"):
        torso = sh(f"M-40,{SH+4} Q-46,{SH-4} -24,{SH-8} L24,{SH-8} Q46,{SH-4} 40,{SH+4} L58,{HIP+40} Q0,{HIP+52} -58,{HIP+40} Z", lk["shirt"])
        torso += line(f"M-20,{HIP} L-26,{HIP+40} M0,{HIP+4} L0,{HIP+46} M20,{HIP} L26,{HIP+40}", OUTL, 2, extra='opacity=".35"')
    else:
        torso = sh(f"M-47,{SH+10} Q-50,{SH-2} -28,{SH-8} L28,{SH-8} Q50,{SH-2} 47,{SH+10} Q44,{SH+60} 37,{SH+80} Q38,{HIP} 41,{HIP+8} Q0,{HIP+16} -41,{HIP+8} Q-38,{HIP} -37,{SH+80} Q-44,{SH+60} -47,{SH+10} Z", lk["shirt"])
        torso += line(f"M-30,{SH+40} Q-20,{SH+60} -26,{SH+86} M28,{SH+70} Q20,{SH+90} 30,{HIP-4}", OUTL, 2.2, extra='opacity=".35"')
    torso += path(f"M-15,{SH-8} Q0,{SH+8} 15,{SH-8}", "none", OUTL, 3)   # gola
    if lk.get("stripes"):
        for k in range(5):
            yy = SH + 16 + k * 22
            torso += line(f"M-42,{yy} L42,{yy}", "#6f97da", 6, extra='opacity=".8"')
    if kind == "leo":
        torso += path(f"M6,{SH+22} L-16,{SH+62} L0,{SH+62} L-8,{SH+98} L20,{SH+48} L3,{SH+48} Z", "#d63a3a", OUTL, 3)
    if acc == "tie":
        torso += path(f"M-16,{SH-8} L0,{SH+40} L16,{SH-8} Z", "#e6e6ea", OUTL, 2.5)
        torso += path(f"M0,{SH-2} L-9,{SH+14} L0,{SH+84} L9,{SH+14} Z", "#b0262f", OUTL, 2.5)
    if kind == "atleta":
        torso += text(0, SH + 82, "10", 46, fill="#ffffff", font=FONT_COND, stroke=OUTL, sw=5)
    if lk.get("coat"):
        torso += line(f"M0,{SH-4} L0,{HIP+12}", OUTL, 3) + "".join(circ(9, SH + 26 + k * 30, 5, "#f0c040", OUTL, 1.5) for k in range(4))
        torso += path(f"M-16,{SH-8} L-4,{SH+30} L-24,{SH+14} Z M16,{SH-8} L4,{SH+30} L24,{SH+14} Z", "#8a1424", OUTL, 2.5)
    if kind == "guard":
        torso += text(0, SH + 70, "SEGURANÇA", 18, fill="#f0c040", font=FONT_COND)
    neck = sh(f"M-12,{SH-30} L12,{SH-30} L13,{SH-4} L-13,{SH-4} Z", skin, sw=3.5, rim=False) + \
        path(f"M-12,{SH-22} Q0,{SH-12} 12,{SH-22} L12,{SH-30} L-12,{SH-30} Z", "#000", extra='opacity=".22"')
    # ---- braços
    def arm(side):
        o = sh("M-10,0 C-12,50 -10,100 -8,136 L8,136 C10,100 12,50 10,0 Z", skin, sw=4)
        if not lk.get("bare_arms"):
            long_sleeve = kind in ("exec", "dono", "guard", "vo", "canguru")
            sl = "M-15,-6 L15,-6 L13,{0} L-13,{0} Z".format(130 if long_sleeve else 56)
            o += sh(sl, lk["shirt"], sw=4)
            if lk.get("stripes"):
                o += "".join(line(f"M-13,{12+k*22} L13,{12+k*22}", "#6f97da", 5) for k in range(5))
        hand = ("M-11,130 Q-16,158 -4,168 Q9,172 13,156 Q15,142 10,130 Z")
        o += sh(hand, skin, sw=3.5, rim=False)
        o += path(f"M{side*8},138 Q{side*18},146 {side*12},154", "none", OUTL, 3)
        if umbrella and side > 0:
            o += line("M0,150 L0,-170", "#222", 6)
            o += path("M-165,-170 Q0,-300 165,-170 Q82,-192 0,-170 Q-82,-192 -165,-170 Z", "#18161f", OUTL, 4) + \
                line("M-100,-232 Q0,-280 100,-232", "#4a4660", 3, extra='opacity=".7"')
        if briefcase and side < 0:
            o += sh("M-42,160 L42,160 L42,214 L-42,214 Z", "#6b4423", sw=4) + rect(-12, 150, 24, 12, "none", stroke=OUTL, sw=3)
        return g(g(o, id=f"{p}-arm{'L' if side < 0 else 'R'}"), tr=f"translate({side*43},{SH+6}) rotate({side*-6})")
    arms = arm(-1) + arm(1)
    # ---- cabeça
    hd = hair_back(lk, acc) + head_shape(lk, kind)
    hd += g(face(p, kind, expr, lk), id=f"{p}-fx-{expr}")
    for e in alt:
        hd += g(face(p, kind, e, lk), id=f"{p}-fx-{e}", extra='opacity="0"')
    hd += hair_front(lk, acc)
    if lk.get("glasses"):
        hd += circ(-19, 0, 16, "none", OUTL, 3.5) + circ(19, 0, 16, "none", OUTL, 3.5) + line("M-3,0 L3,0", OUTL, 3.5) + \
            line("M-30,-8 l8,-4 M10,-8 l8,-4", "#ffffff", 2.5, extra='opacity=".6"')
    if acc == "shades":
        hd += path("M-40,-10 L40,-10 L36,10 Q20,14 6,6 L-6,6 Q-20,14 -36,10 Z", "#0a0a0e", OUTL, 2) + line("M-30,-4 l14,0", "#ffffff", 2, extra='opacity=".4"')
    if lk.get("beard"):
        hd += sh("M-44,12 Q-40,120 0,160 Q40,120 44,12 Q26,44 0,44 Q-26,44 -44,12 Z", "#f4f4f4", sw=4)
        hd += path("M-26,28 Q0,18 26,28 Q0,40 -26,28 Z", "#f4f4f4", OUTL, 3)
        hd += line("M-16,70 Q-10,110 -4,140 M14,70 Q10,110 4,140", "#c9c9d4", 2.5)
    if lk.get("stache"):
        hd += path("M-34,24 Q-16,8 0,20 Q16,8 34,24 Q16,32 0,26 Q-16,32 -34,24 Z", "#2a1d16", OUTL, 2.5)
    if helmet:
        hd += circ(0, -6, 96, "#bfe8ff", "#e8f6ff", 5, extra='fill-opacity=".14"')
        hd += line("M-62,-56 Q-42,-82 -6,-90", "#ffffff", 9, extra='opacity=".7"') + line("M60,40 Q72,10 70,-20", "#ffffff", 4, extra='opacity=".35"')
    head = g(g(hd, id=f"{p}-head"), tr=f"translate(0,{HC})")
    shadow = f'<ellipse cx="0" cy="2" rx="60" ry="10" fill="url(#fx-contact)"/>'
    body = legs + torso + neck + arms + head
    inner = shadow + g(body, id=f"{p}-j")
    sc = f"scale({-s if flip else s},{s})"
    st = f' style="filter:{AMB}"' if AMB else ""
    return g(inner, id=p, tr=f"translate({f(x)},{f(y)}) {sc}", extra=('opacity="0"' if hidden else "") + st)
