"""Biblioteca de desenho (SVG) no estilo "cartoon de palito noturno".
Ver referencias/estilo-cartoon-noturno/ESTILO.md. Tudo em coordenadas de 1080x1920."""
import random, math

W, H = 1080, 1920
INK = "#110d16"
SKIN = "#e2b38c"
NIGHT = ["#0d0912", "#201b2b", "#37364b", "#5a546c"]
WIN = ["#f6c64f", "#ffd978", "#e8a93a", "#fff0b0"]
MONEY = "#3cff5a"
FONT_CAP = "OSans"      # Open Sans ExtraBold
FONT_COND = "Oswald"    # placas, painel, etiquetas
FONT_ROUND = "Nunito"


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ primitivas
def rect(x, y, w, h, fill, rx=0, stroke=None, sw=6, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}"{s} {extra}/>'


def circ(cx, cy, r, fill, stroke=None, sw=6, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"{s} {extra}/>'


def ell(cx, cy, rx, ry, fill, stroke=None, sw=6, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"{s} {extra}/>'


def path(d, fill, stroke=None, sw=6, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'


def line(d, color, w, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def limb(d, color, w=11):
    """membro de palito: contorno escuro + cor por cima"""
    return line(d, INK, w + 9) + line(d, color, w)


def text(x, y, s, size, fill="#fff", font=FONT_COND, anchor="middle", stroke=None, sw=8, extra="", weight=700):
    extra += " data-layout-allow-overlap=\"\""
    st = f' stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{font}" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}"{st} {extra}>{s}</text>')


def g(inner, id=None, tr=None, extra=""):
    a = (f' id="{id}"' if id else "") + (f' transform="{tr}"' if tr else "")
    return f"<g{a} {extra}>{inner}</g>"


# ------------------------------------------------------------------ defs comuns (um por cena)
def defs(p):
    from chars import char_defs
    CHAR_DEFS = char_defs()
    return f"""<defs>
<radialGradient id="fx-glow"><stop offset="0" stop-color="#fff3c4" stop-opacity=".85"/><stop offset=".35" stop-color="#ffd36b" stop-opacity=".35"/><stop offset="1" stop-color="#ffb84a" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-glowc"><stop offset="0" stop-color="#d9fbff" stop-opacity=".8"/><stop offset=".4" stop-color="#5fe2ff" stop-opacity=".3"/><stop offset="1" stop-color="#5fe2ff" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-glowp"><stop offset="0" stop-color="#ffd1ec" stop-opacity=".8"/><stop offset=".4" stop-color="#ff4fa3" stop-opacity=".3"/><stop offset="1" stop-color="#ff4fa3" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-glowg"><stop offset="0" stop-color="#e6ffe9" stop-opacity=".85"/><stop offset=".4" stop-color="#3cff5a" stop-opacity=".35"/><stop offset="1" stop-color="#3cff5a" stop-opacity="0"/></radialGradient>
<radialGradient id="fx-glowr"><stop offset="0" stop-color="#ffd6d6" stop-opacity=".8"/><stop offset=".4" stop-color="#ff3b3b" stop-opacity=".35"/><stop offset="1" stop-color="#ff3b3b" stop-opacity="0"/></radialGradient>
<linearGradient id="fx-cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c2" stop-opacity=".55"/><stop offset="1" stop-color="#ffd36b" stop-opacity="0"/></linearGradient>
<linearGradient id="fx-conec" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6fbff" stop-opacity=".5"/><stop offset="1" stop-color="#7fe6ff" stop-opacity="0"/></linearGradient>
<linearGradient id="fx-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0812"/><stop offset=".6" stop-color="#211a33"/><stop offset="1" stop-color="#3a2c52"/></linearGradient>
<linearGradient id="fx-wet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2438"/><stop offset="1" stop-color="#15111d"/></linearGradient>
<filter id="fx-neon" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="fx-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
{CHAR_DEFS}<filter id="fx-dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.2"/></filter>
</defs>"""


def glow(p, cx, cy, r, kind="", op=1.0, id=None):
    a = f' id="{id}"' if id else ""
    return f'<circle{a} cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#fx-glow{kind})" opacity="{op}" style="mix-blend-mode:screen"/>'


def cone(p, x, y, top_w, bot_w, h, kind="", op=1.0):
    d = f"M{f(x-top_w/2)},{f(y)} L{f(x+top_w/2)},{f(y)} L{f(x+bot_w/2)},{f(y+h)} L{f(x-bot_w/2)},{f(y+h)} Z"
    return f'<path d="{d}" fill="url(#fx-cone{kind})" opacity="{op}" style="mix-blend-mode:screen"/>'


def neon(p, x, y, s, size, color, rot=0, anchor="middle"):
    tr = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot else ""
    t = text(x, y, s, size, fill="#ffffff", font=FONT_COND, anchor=anchor, extra=f'style="letter-spacing:2px"')
    halo = text(x, y, s, size, fill=color, font=FONT_COND, anchor=anchor, stroke=color, sw=10, extra=f'filter="url(#fx-neon)" style="letter-spacing:2px"')
    edge = text(x, y, s, size, fill="none", font=FONT_COND, anchor=anchor, stroke=color, sw=4, extra='style="letter-spacing:2px"')
    return f"<g{tr}>{halo}{edge}{t}</g>"


# ------------------------------------------------------------------ cenários
def sky(p, h=H):
    return rect(-300, -300, W + 600, h + 600, f"url(#fx-sky)")


def stars(seed, n=120, y1=1300, col="#fff"):
    r = random.Random(seed)
    return "".join(circ(r.uniform(-200, W + 200), r.uniform(-200, y1), r.choice([1.4, 2, 2.6, 3.4]), col,
                        extra=f'opacity="{r.uniform(.35, 1):.2f}"') for _ in range(n))


def building(x, y, w, h, color, seed, win=True, lit=.35, cols=None, edge=None):
    r = random.Random(seed)
    s = rect(x, y, w, h, color)
    if edge:
        s += rect(x, y, w, 10, edge)
    if win:
        cols = cols or max(2, int(w // 70))
        rows = max(2, int(h // 95))
        ww, wh = w / cols * .5, 46
        for i in range(cols):
            for j in range(rows):
                wx = x + (i + .25) * w / cols
                wy = y + 40 + j * 95
                if wy + wh > y + h - 30:
                    continue
                if r.random() < lit:
                    s += rect(wx, wy, ww, wh, r.choice(WIN), rx=2)
                else:
                    s += rect(wx, wy, ww, wh, "#1a1524", rx=2, extra='opacity=".7"')
    return s


def skyline(seed, y, h0, h1, color, n=9, lit=.3, x0=-200, x1=W + 200):
    r = random.Random(seed)
    s, x = "", x0
    while x < x1:
        w = r.uniform(110, 230)
        h = r.uniform(h0, h1)
        s += building(x, y - h, w, h + 400, color, r.random(), lit=lit)
        x += w + r.uniform(-10, 20)
    return s


def lamp(p, x, y_top, ground, side=1, kind=""):
    """poste com cone de luz. side=1 braço para a direita"""
    s = rect(x - 7, y_top, 14, ground - y_top, "#1b1622")
    s += line(f"M{x},{y_top} Q{x},{y_top-40} {x+side*60},{y_top-40}", "#1b1622", 12)
    lx = x + side * 70
    s += path(f"M{lx-30},{y_top-48} L{lx+30},{y_top-48} L{lx+20},{y_top-30} L{lx-20},{y_top-30} Z", "#2a2333")
    s += cone(p, lx, y_top - 30, 40, 520, ground - y_top + 60, kind, .8)
    s += glow(p, lx, y_top - 30, 120, kind)
    s += ell(lx, ground + 10, 230, 34, f"url(#fx-glow{kind})", extra='opacity=".6" style="mix-blend-mode:screen"')
    return s


def street(p, y=1480, color="#241d30"):
    s = rect(-300, y, W + 600, H - y + 300, f"url(#fx-wet)")
    s += rect(-300, y, W + 600, 26, "#3b3248")          # meio-fio
    s += rect(-300, y + 26, W + 600, 8, "#120e18")
    r = random.Random(y)
    for i in range(8):     # poças refletindo
        s += ell(r.uniform(0, W), r.uniform(y + 120, H - 60), r.uniform(60, 160), r.uniform(10, 20), "#4b3f63",
                 extra='opacity=".45"')
    return s


def storefront(p, x, y, w, h, name, ncol, glass="#f7c75a", seed=1, kind=""):
    s = rect(x, y, w, h, "#2c2438")
    s += rect(x + 20, y + 110, w - 40, h - 130, glass, rx=4)
    r = random.Random(seed)
    for i in range(3):     # prateleiras/silhuetas na vitrine
        s += rect(x + 30, y + 160 + i * 70, w - 60, 10, "#c48a2b", extra='opacity=".7"')
        for k in range(int((w - 60) // 40)):
            if r.random() < .6:
                s += rect(x + 36 + k * 40, y + 128 + i * 70, 24, 32, r.choice(["#e0603a", "#5aa0e0", "#7bd56b", "#fff"]),
                          extra='opacity=".75"')
    s += rect(x + 20, y + 110, w - 40, h - 130, "none", stroke="#1a1422", sw=8)
    s += rect(x, y + 10, w, 90, "#1a1422", rx=6)
    s += neon(p, x + w / 2, y + 78, name, 64, ncol)
    s += glow(p, x + w / 2, y + h * .6, w * .8, kind, .55)
    return s


def rain(p, seed, dur, n=90, op=.32):
    """chuva em riscos: um ladrilho de 600 px repetido 2x; o JS desloca em y em loop"""
    r = random.Random(seed)
    tile = ""
    for _ in range(n):
        x, y, L = r.uniform(-100, W + 100), r.uniform(0, 600), r.uniform(40, 90)
        tile += line(f"M{f(x)},{f(y)} l{f(-L*.18)},{f(L)}", "#cfd6ff", r.choice([2, 2.5, 3]),
                     extra=f'opacity="{r.uniform(.35, 1):.2f}"')
    body = "".join(g(tile, tr=f"translate(0,{k*600})") for k in range(-1, 4))
    return g(body, id=f"{p}-rain", extra=f'opacity="{op}"')


def bokeh(p, seed, n=14, cols=("#ff4fa3", "#39e5ff", "#ffd36b", "#3cff5a", "#a77bff")):
    r = random.Random(seed)
    s = ""
    for i in range(n):
        s += circ(r.uniform(0, W), r.uniform(100, 1500), r.uniform(40, 110), r.choice(cols),
                  extra=f'opacity="{r.uniform(.12, .3):.2f}" filter="url(#fx-soft)"')
    return g(s, id=f"{p}-bokeh")


# ------------------------------------------------------------------ gráficos
def money(id, x, y, txt, size=96):
    """+R$ verde neon com contorno escuro"""
    t = text(0, 0, txt, size, fill=MONEY, font=FONT_COND, stroke=INK, sw=16,
             extra='style="letter-spacing:1px"')
    halo = text(0, 0, txt, size, fill="none", font=FONT_COND, stroke=MONEY, sw=18,
                extra='opacity=".35" style="letter-spacing:1px"')
    return g(g(halo + t, id=id, extra='opacity="0"'), tr=f"translate({f(x)},{f(y)})")


def tag(id, x, y, txt, size=46, hidden=True):
    w = len(txt) * size * .52 + 40
    s = rect(-w / 2, -size - 10, w, size + 26, "#ffd23a", rx=6, stroke=INK, sw=6)
    s += text(0, 0, txt, size, fill=INK, font=FONT_COND)
    return g(g(s, id=id, extra='opacity="0"' if hidden else ""), tr=f"translate({f(x)},{f(y)})")


def plate(x, y, txt, size=60, bg="#2b55c9", fg="#fff", border="#e9eefc", w=None):
    w = w or len(txt) * size * .56 + 60
    s = rect(x - w / 2, y - size - 18, w, size + 40, bg, rx=10, stroke=border, sw=6)
    s += text(x, y, txt, size, fill=fg, font=FONT_COND)
    return s


def phone(id, x, y, s=1.0, title="PIX RECEBIDO", value="R$ 40", sub="", clock="23:47", hand=True):
    """celular segurado por uma mão; origem no centro do aparelho"""
    o = ""
    if hand:
        o += path("M-160,260 C-150,120 -120,60 -110,-20 L110,-20 C120,80 140,160 150,260 Z", SKIN, INK, 7)
    o += rect(-150, -300, 300, 560, "#14111a", rx=38, stroke=INK, sw=8)
    o += rect(-132, -282, 264, 524, "#0c3b2c", rx=26)
    o += text(0, -200, clock, 64, fill="#fff", font=FONT_CAP, weight=800)
    o += rect(-118, -150, 236, 200, "#f4fff6", rx=18)
    o += circ(-86, -116, 13, "#21c25e")
    o += text(8, -104, title, 26, fill="#1d3b2a", font=FONT_CAP, weight=800)
    o += text(0, -40, value, 46, fill="#18a64a", font=FONT_COND, extra=f'id="{id}-val"')
    if sub:
        o += text(0, 22, sub, 24, fill="#556", font=FONT_CAP, weight=800)
    if hand:   # dedos por cima
        for i, yy in enumerate((40, 92, 144)):
            o += path(f"M110,{yy} q50,-6 52,22 q-2,24 -52,20 Z", SKIN, INK, 6)
        o += path("M-110,70 q-56,-10 -60,26 q4,28 60,22 Z", SKIN, INK, 6)
    return g(g(o, id=id), tr=f"translate({f(x)},{f(y)}) scale({s})")


def ranking(id, x, y, rows, title="RANKING DO PULO", s=1.0, hi=None, w=760):
    """painel de terminal verde preso por holofotes. rows=[(pos,nome,valor,face)]"""
    rh = 150
    h = 170 + rh * len(rows) + 40
    o = rect(-w / 2 - 24, -24, w + 48, h + 48, "#2b2c33", rx=26, stroke=INK, sw=8)
    for sx in (-w / 2 - 2, 0, w / 2 + 2):
        o += circ(sx, -4, 10, "#666a75", INK, 3)
    o += rect(-w / 2, 0, w, h, "#0b2414", rx=14, stroke="#2ee06a", sw=5)
    o += text(0, 110, title, 74, fill="#3cff5a", font=FONT_COND)
    o += rect(-w / 2 + 40, 140, w - 80, 5, "#3cff5a", extra='opacity=".8"')
    for i, (pos, nome, val, face) in enumerate(rows):
        yy = 170 + i * rh
        gold = (hi == i)
        col = "#ffd23a" if gold else "#3cff5a"
        o += rect(-w / 2 + 20, yy + 6, w - 40, rh - 14, "#ffd23a" if gold else "#103a20", rx=10,
                  extra=f'opacity="{.22 if gold else .65}"')
        if gold:
            o += rect(-w / 2 + 20, yy + 6, w - 40, rh - 14, "none", rx=10, stroke="#ffd23a", sw=5)
        lng = len(pos) >= 5
        o += text(-w / 2 + (130 if lng else 90), yy + (92 if lng else 100), pos, 40 if lng else 62, fill=col, font=FONT_COND)
        tx = -w / 2 + (250 if lng else 190)
        if face:
            o += face_icon(face, tx + 55, yy + rh / 2 - 4)
            tx += 135
        o += text(tx, yy + 70, nome, 56, fill=col, font=FONT_COND, anchor="start")
        o += text(tx, yy + 120, val, 38, fill=col, font=FONT_COND, anchor="start")
    return g(g(o, id=id), tr=f"translate({f(x)},{f(y)}) scale({s})")


def face_icon(kind, cx, cy):
    o = rect(cx - 52, cy - 52, 104, 104, "#3a2a55", rx=6, stroke="#ffd23a", sw=5)
    if kind == "?":
        o += circ(cx, cy + 6, 34, "#1a1524")
        o += text(cx, cy + 22, "?", 50, fill="#ffd23a", font=FONT_COND)
    else:
        col = {"leo": "#8d5a3b", "atleta": "#6e4430", "dono": "#e6b089", "girl": SKIN}.get(kind, SKIN)
        o += circ(cx, cy + 8, 32, col, INK, 4)
        o += circ(cx - 11, cy + 4, 4, INK) + circ(cx + 11, cy + 4, 4, INK)
        o += line(f"M{cx-10},{cy+20} Q{cx},{cy+27} {cx+10},{cy+20}", INK, 4)
        if kind == "leo":
            o += circ(cx, cy - 18, 30, "#1b120d", INK, 3) + rect(cx - 30, cy - 14, 60, 8, "#ff7a1a", rx=3)
    return o


def wanted(id, x, y, title, name, s=1.0):
    o = rect(-190, -260, 380, 520, "#e9d6a7", rx=4, stroke="#6b4a24", sw=6)
    o += text(0, -180, "PROCURADO", 64, fill="#5a2e12", font=FONT_COND)
    o += rect(-130, -150, 260, 210, "#cdb685", stroke="#6b4a24", sw=5)
    # silhueta de homem batendo a cabeça num teto baixo
    o += rect(-130, -150, 260, 30, "#6b4a24")
    o += circ(0, -78, 36, "#5a3a1c") + rect(-40, -40, 80, 90, "#5a3a1c", rx=14)
    for a in (-40, 0, 40):
        o += line(f"M{a*0.9},-118 l{a*0.25},-14", "#c0392b", 5)
    o += text(0, 120, name[0], 40, fill="#5a2e12", font=FONT_COND)
    o += text(0, 168, name[1], 40, fill="#5a2e12", font=FONT_COND)
    o += text(0, 228, "RECOMPENSA: R$ 1.000.000", 26, fill="#8a1c12", font=FONT_COND)
    return g(g(o, id=id), tr=f"translate({f(x)},{f(y)}) scale({s}) rotate(-3)")


def ruler(x, y0, y1, step_cm, px_per_cm, label_every=10):
    """régua vertical (fita métrica) de y1 (chão) para cima"""
    w = 70
    o = rect(x - w / 2, y0, w, y1 - y0, "#ffd23a", rx=4, stroke=INK, sw=5)
    n = int((y1 - y0) / (px_per_cm * step_cm))
    for i in range(n + 1):
        yy = y1 - i * px_per_cm * step_cm
        big = (i * step_cm) % label_every == 0
        o += line(f"M{x-w/2},{f(yy)} l{30 if big else 16},0", INK, 4 if big else 3)
        if big and i:
            o += text(x + 14, yy + 9, str(i * step_cm), 24, fill=INK, font=FONT_COND)
    return o


# ------------------------------------------------------------------ personagens
LOOKS = {
    "leo":    dict(shirt="#ffc93c", pants="#3d5a99", shoe="#e63946", hair="#3b2418", acc="cap"),
    "vo":     dict(shirt="#8e5bc8", pants="#5b3d8a", shoe="#3b2c55", hair="#e8e6ef", acc="bun", glasses=True, skirt=True),
    "canguru": dict(shirt="#9fc5ff", pants="#9fc5ff", shoe="#c94f4f", hair="#f2f2f2", acc="nightcap", beard=True, stripes=True),
    "exec":   dict(shirt="#5d6474", pants="#3a3f4b", shoe="#141018", hair="#2a1d16", acc="tie"),
    "girl":   dict(shirt="#ff6fae", pants="#ff6fae", shoe="#fff", hair="#6b3b1f", acc="pigtails", skirt=True),
    "atleta": dict(shirt="#1fb5a5", pants="#174f8a", shoe="#fff", hair="#1d1410", acc="band", skin="#a8714e"),
    "dono":   dict(shirt="#c8243a", pants="#1b1622", shoe="#141018", hair="#2a1d16", acc="tophat", stache=True),
    "guard":  dict(shirt="#22252e", pants="#22252e", shoe="#000", hair="#000", acc="shades"),
}
CROWD_SHIRTS = ["#d9534f", "#5b8dd9", "#6fbf73", "#c98bd9", "#e0a03a", "#5e6b7d", "#2fa3a0", "#a35a3a"]


def face(p, kind, expr, lk):
    o = ""
    ey = -6
    if expr == "happy":
        o += "".join(line(f"M{x-11},{ey+4} Q{x},{ey-10} {x+11},{ey+4}", INK, 6) for x in (-20, 20))
        o += path("M-20,20 Q0,46 20,20 Z", "#7a1f2b", INK, 4)
    elif expr == "shock":
        o += "".join(circ(x, ey, 12, "#fff", INK, 4) + circ(x, ey, 5, INK) for x in (-21, 21))
        o += ell(0, 30, 10, 14, "#7a1f2b", INK, 4)
    elif expr == "sad":
        o += "".join(circ(x, ey, 6, INK) for x in (-20, 20))
        o += line("M-26,-28 L-12,-22 M26,-28 L12,-22", INK, 5)
        o += line("M-12,30 Q0,20 12,30", INK, 5)
    elif expr == "determined":
        o += "".join(circ(x, ey, 6, INK) for x in (-20, 20))
        o += line("M-32,-30 L-10,-20 M32,-30 L10,-20", INK, 7)
        o += line("M-12,26 L12,26", INK, 5)
    elif expr == "smile":
        o += "".join(circ(x, ey, 6, INK) for x in (-20, 20))
        o += line("M-14,22 Q0,34 14,22", INK, 5)
    elif expr == "angry":
        o += "".join(circ(x, ey, 6, INK) for x in (-20, 20))
        o += line("M-32,-24 L-10,-14 M32,-24 L10,-14", INK, 7)
        o += path("M-16,32 Q0,20 16,32 Z", "#7a1f2b", INK, 4)
    else:  # neutral
        o += "".join(circ(x, ey, 6, INK) for x in (-20, 20))
        o += line("M-10,26 L10,26", INK, 5)
    return o


def person(p, kind="leo", x=0, y=0, s=1.0, expr="neutral", flip=False, shirt=None, umbrella=False,
           briefcase=False, hidden=False, alt=(), helmet=False):
    """Boneco de palito de cabeça grande. Pés em (x,y). Grupos animáveis:
    {p}-j (pulo, origem nos pés) · {p}-armL/{p}-armR (ombro) · {p}-legL/{p}-legR (quadril) · {p}-head · {p}-face-*"""
    lk = dict(LOOKS.get(kind, LOOKS["exec"]))
    if shirt:
        lk["shirt"] = shirt
    skin = lk.get("skin", SKIN)
    hip, sh, hc, hr = -150, -262, -338, 60
    # pernas
    def leg(side):
        sx = side * 13
        d = f"M0,0 L{side*3},150"
        o = limb(d, lk["pants"], 12)
        o += ell(side * 12, 154, 22, 11, lk["shoe"], INK, 5)
        return g(g(o, id=f"{p}-leg{'L' if side < 0 else 'R'}"), tr=f"translate({sx},{hip})")
    legs = leg(-1) + leg(1)
    # tronco
    if lk.get("skirt"):
        torso = path(f"M-34,{sh} L34,{sh} L50,{hip+20} L-50,{hip+20} Z", lk["shirt"], INK, 7)
    else:
        torso = path(f"M-36,{sh} Q-40,{hip} -32,{hip} L32,{hip} Q40,{hip} 36,{sh} Z", lk["shirt"], INK, 7)
    if lk.get("stripes"):
        for k in range(4):
            yy = sh + 22 + k * 26
            torso += line(f"M-34,{yy} L34,{yy}", "#5f8fe0", 6)
    if kind == "leo":   # raio na camiseta (marca do Léo)
        torso += path(f"M4,{sh+24} L-14,{sh+62} L2,{sh+62} L-6,{sh+94} L16,{sh+50} L0,{sh+50} Z", "#e63946", INK, 3)
    if lk.get("acc") == "tie":
        torso += path(f"M0,{sh+4} L-9,{sh+20} L0,{sh+80} L9,{sh+20} Z", "#c0392b", INK, 3)
    if kind == "atleta":
        torso += text(0, sh + 78, "10", 44, fill="#fff", font=FONT_COND, stroke=INK, sw=5)
    if kind == "dono":
        torso += "".join(circ(0, sh + 30 + k * 30, 5, "#ffd23a") for k in range(3))
    if kind == "guard":
        torso += text(0, sh + 66, "SEGURANÇA", 18, fill="#ffd23a", font=FONT_COND)
    # braços
    def arm(side):
        d = f"M0,0 L{side*10},120"
        o = limb(d, lk["shirt"] if kind != "atleta" else skin, 11)
        o += circ(side * 10, 126, 12, skin, INK, 4)
        if umbrella and side > 0:
            o += line(f"M{side*10},126 L{side*10},-150", "#222", 6)
            o += path(f"M{side*10-150},-150 Q{side*10},-260 {side*10+150},-150 Q{side*10+75},-170 {side*10},-150 "
                      f"Q{side*10-75},-170 {side*10-150},-150 Z", "#1c1a24", INK, 5)
        if briefcase and side < 0:
            o += rect(side * 10 - 40, 130, 80, 56, "#6b4423", rx=6, stroke=INK, sw=5)
        return g(g(o, id=f"{p}-arm{'L' if side < 0 else 'R'}"), tr=f"translate({side*34},{sh+10})")
    arms = arm(-1) + arm(1)
    # cabeça
    hd = ""
    acc = lk.get("acc")
    if acc == "pigtails":
        hd += circ(-62, -18, 22, lk["hair"], INK, 5) + circ(62, -18, 22, lk["hair"], INK, 5)
    if acc == "bun":
        hd += circ(0, -66, 26, lk["hair"], INK, 5)
    hd += line("M0,40 L0,70", INK, 12)
    hd += circ(0, 0, hr, skin, INK, 7)
    if acc in (None, "tie", "band", "shades", "pigtails"):
        hd += path(f"M-58,-14 Q-56,-66 0,-64 Q56,-66 58,-14 Q30,-40 0,-36 Q-30,-40 -58,-14 Z", lk["hair"], INK, 5)
    if acc == "bun":
        hd += path("M-60,-6 Q-58,-64 0,-62 Q58,-64 60,-6 Q40,-30 0,-30 Q-40,-30 -60,-6 Z", lk["hair"], INK, 5)
    if acc == "cap":
        hd += path("M-60,-12 Q-58,-70 0,-68 Q58,-70 60,-12 Z", "#e63946", INK, 6)
        hd += path("M20,-22 Q70,-30 92,-12 Q70,-6 20,-10 Z", "#b32634", INK, 5)
    if acc == "band":
        hd += rect(-60, -36, 120, 16, "#fff", rx=4, stroke=INK, sw=4)
    if acc == "tophat":
        hd += rect(-70, -64, 140, 16, "#141018", rx=6, stroke=INK, sw=4)
        hd += rect(-44, -150, 88, 92, "#141018", stroke=INK, sw=4) + rect(-44, -86, 88, 14, "#c8243a")
    if acc == "nightcap":
        hd += path("M-58,-18 Q-50,-70 0,-66 Q50,-66 58,-18 Q30,-34 0,-30 Q-30,-34 -58,-18 Z", "#f2f2f2", INK, 5)  # careca com cabelo branco dos lados
        hd += path("M-46,-40 Q-10,-120 70,-120 Q40,-90 46,-44 Z", "#3d6fd1", INK, 5)
        hd += circ(74, -122, 14, "#fff", INK, 4)
    hd += g(face(p, kind, expr, lk), id=f"{p}-fx-{expr}")
    for e in alt:
        hd += g(face(p, kind, e, lk), id=f"{p}-fx-{e}", extra='opacity="0"')
    if lk.get("glasses"):
        hd += circ(-20, -6, 16, "none", INK, 4) + circ(20, -6, 16, "none", INK, 4) + line("M-4,-6 L4,-6", INK, 4)
    if helmet:
        hd += circ(0, -4, 92, "#bfe8ff", "#e8f6ff", 6, extra='fill-opacity=".16"')
        hd += line("M-60,-50 Q-40,-76 -6,-84", "#ffffff", 8, extra='opacity=".7"')
    if acc == "shades":
        hd += rect(-46, -18, 92, 24, "#000", rx=8)
    if lk.get("beard"):
        hd += path("M-46,14 Q-40,110 0,150 Q40,110 46,14 Q24,40 0,40 Q-24,40 -46,14 Z", "#f4f4f4", INK, 5)
        hd += path("M-24,30 Q0,20 24,30 Q0,40 -24,30 Z", "#f4f4f4", INK, 4)
    if lk.get("stache"):
        hd += path("M-30,22 Q-14,8 0,18 Q14,8 30,22 Q14,30 0,24 Q-14,30 -30,22 Z", "#2a1d16", INK, 3)
    head = g(g(hd, id=f"{p}-head"), tr=f"translate(0,{hc})")
    body = legs + torso + arms + head
    inner = g(body, id=f"{p}-j")
    sc = f"scale({-s if flip else s},{s})"
    return g(inner, id=p, tr=f"translate({f(x)},{f(y)}) {sc}", extra='opacity="0"' if hidden else "")


def crowd(prefix, seed, n, y, x0=-60, x1=W + 60, s=(0.55, 0.75), umbrella=.25, briefcase=.3, hidden=False):
    r = random.Random(seed)
    out, ids = "", []
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    for i, x in enumerate(xs):
        pid = f"{prefix}{i}"
        ids.append(pid)
        out += person(pid, kind=r.choice(["exec", "girl", "atleta", "guard", "exec"]),
                      x=x, y=y + r.uniform(-20, 20), s=r.uniform(*s), expr=r.choice(["happy", "smile", "neutral"]),
                      flip=r.random() < .5, shirt=r.choice(CROWD_SHIRTS),
                      umbrella=r.random() < umbrella, briefcase=r.random() < briefcase, hidden=hidden)
    return out, ids


# personagens redesenhados (2D semi-realista) substituem os de palito
from chars import person, LOOKS, set_rim  # noqa: E402,F401
