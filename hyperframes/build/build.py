"""Gera o projeto HyperFrames "E se você encolhesse pela metade todo dia?" (9:16).
Saída: ../index.html, ../compositions/*.html. Rode: python3 build/build.py"""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
INK = "#1E1B2E"

# ------------------------------------------------------------------ roteiro / tempos
SCENES = [
    dict(id="s0", text="E se você encolhesse pela metade todo dia?"),
    dict(id="s1", text="Dia um. Você acorda com oitenta e cinco centímetros. A roupa sobra inteira.", day=1),
    dict(id="s2", text="Dia dois. Quarenta e dois centímetros. E o seu gato começa a te olhar diferente.", day=2),
    dict(id="s3", text="Dia cinco. Cinco centímetros. Sua cama agora é uma caixa de fósforo.", day=5),
    dict(id="s4", text="Dia oito. Sete milímetros. Uma formiga é do seu tamanho, e ela é bem mais forte que você.", day=8),
    dict(id="s5", text="Dia treze. Você vira poeira. Um ácaro parece um monstro.", day=13),
    dict(id="s6", text="Dia vinte. Você é do tamanho de uma bactéria. Uma gota d'água vira um oceano.", day=20),
    dict(id="s7", text="Dia vinte e quatro. Um vírus já é do seu tamanho.", day=24),
    dict(id="s8", text="Dia trinta e três. Você é do tamanho de um átomo. Elétrons passam zunindo pela sua cara.", day=33),
    dict(id="s9", text="E amanhã? Você fica menor que tudo que existe.", day=34),
    dict(id="s10", text="Continua encolhendo ou tenta voltar? Comenta aí.", hold=2.4),
]
LEAD, TAIL = 0.4, 0.35

def word_dur(w):
    core = w.strip(".,?!")
    d = max(0.26, min(0.6, 0.17 + 0.034*len(core)))
    if w[-1] in ".?!": d += 0.32
    elif w[-1] == ",": d += 0.16
    return d

def timeline(sc):
    words = sc["text"].split()
    chunks, t, i = [], LEAD, 0
    while i < len(words):
        grp = [words[i]]
        while len(grp[-1].strip(".,?!")) <= 2 and grp[-1][-1] not in ".,?!" and i+1 < len(words) and len(grp) < 3:
            i += 1; grp.append(words[i])
        d = sum(word_dur(w) for w in grp)
        chunks.append((round(t, 3), round(t+d, 3), " ".join(w.strip(".,") for w in grp)))
        t += d; i += 1
    return chunks, round(t + TAIL + sc.get("hold", 0), 3)

T0 = 0
for sc in SCENES:
    sc["chunks"], sc["dur"] = timeline(sc)
    sc["start"] = round(T0, 3); T0 += sc["dur"]
TOTAL = round(T0, 3)

def wt(sc, needle):
    for a, b, txt in sc["chunks"]:
        if needle.lower() in txt.lower(): return a
    raise KeyError(needle)

# ------------------------------------------------------------------ helpers SVG
def st(fill, sw=6, op=None):
    s = f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"'
    return s + (f' opacity="{op}"' if op is not None else "")

def C(cx, cy, r, fill, sw=6, extra=""): return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {st(fill, sw) if sw else f"fill={chr(34)}{fill}{chr(34)}"} {extra}/>'
def E(cx, cy, rx, ry, fill, sw=6, extra=""): return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" {st(fill, sw) if sw else f"fill={chr(34)}{fill}{chr(34)}"} {extra}/>'
def R(x, y, w, h, rx, fill, sw=6, extra=""): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" {st(fill, sw) if sw else f"fill={chr(34)}{fill}{chr(34)}"} {extra}/>'
def P(d, fill, sw=6, extra=""): return f'<path d="{d}" {st(fill, sw) if sw else f"fill={chr(34)}{fill}{chr(34)}"} {extra}/>'
def L(d, color, w, extra=""): return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def limb(d, color, w=14): return L(d, INK, w+12) + L(d, color, w)

# ------------------------------------------------------------------ personagem: LÉO
SKIN, HAIR, CAP, CAP_D, SHIRT, JEANS, LIMB_C, PHONE = "#DFA57A", "#3B2418", "#E63946", "#B32634", "#FFC93C", "#3D5A99", "#2F3550", "#2EC4B6"

def leo(p):
    """Léo: corpo-pílula, membros de palito, cabeça redonda grande — molde do vídeo de referência.
    Pés em (0,0). Partes com id para o rig: wrap, body, head, armL, armR, olhos e bocas."""
    arm_n = limb("M0,0 C22,60 30,125 28,185", LIMB_C) + E(10, 26, 30, 34, SHIRT, 6) + C(28, 192, 18, SKIN, 5)
    arm_s = L("M0,0 C24,70 34,140 30,215", INK, 58) + L("M0,0 C24,70 34,140 30,215", SHIRT, 44)
    def arm(side):
        return (f'<g id="{p}-arm{side}"><g id="{p}-arm{side}n">{arm_n}</g>'
                f'<g id="{p}-slv{side}" opacity="0">{arm_s}</g></g>')
    eyes = {
        "dot": "".join(C(x, -100, 11, INK, 0) for x in (-42, 42)),
        "happy": "".join(L(f"M{x-15},-96 Q{x},-116 {x+15},-96", INK, 7) for x in (-42, 42)),
        "shock": "".join(C(x, -100, 22, "#FFFFFF", 5) + C(x+2, -98, 8, INK, 0) for x in (-42, 42)),
        "tired": "".join(L(f"M{x-17},-104 L{x+17},-104", INK, 7) + C(x, -96, 7, INK, 0) for x in (-42, 42)),
        "closed": "".join(L(f"M{x-15},-104 Q{x},-90 {x+15},-104", INK, 7) for x in (-42, 42)),
        "dizzy": "".join(L(" ".join(("M" if k == 0 else "L") + f"{x+math.cos(k*0.42)*k*0.48:.1f},{-100+math.sin(k*0.42)*k*0.48:.1f}" for k in range(42)), INK, 4) for x in (-42, 42)),
    }
    mouths = {
        "line": L("M-17,-40 Q0,-30 17,-40", INK, 7),
        "smile": P("M-30,-48 Q0,-4 30,-48 Z", "#C9343F", 6),
        "grin": P("M-34,-50 Q0,0 34,-50 Z", "#C9343F", 6) + P("M-26,-46 L26,-46 L22,-36 L-22,-36 Z", "#FFFFFF", 0),
        "o": E(0, -34, 16, 22, "#6B1E2A", 6),
        "yawn": E(0, -30, 26, 34, "#6B1E2A", 6),
        "wavy": L("M-24,-36 L-16,-44 L-8,-32 L0,-44 L8,-32 L16,-44 L24,-36", INK, 6),
        "flat": L("M-18,-36 L18,-36", INK, 7),
        "small": E(0, -36, 7, 5, INK, 0),
        "teeth": R(-26, -50, 52, 26, 8, "#FFFFFF", 5) + L("M-26,-37 L26,-37", INK, 3),
    }
    g = [f'<g id="{p}-wrap">',
         E(0, 0, 110, 18, "#000000", 0, 'opacity="0.18"'),
         f'<g id="{p}-body">',
         limb("M-30,-165 L-30,-20", "#26324F"), limb("M30,-165 L30,-20", "#26324F"),
         E(-50, -14, 44, 23, "#FFFFFF", 6), L("M-80,-12 L-24,-12", "#E63946", 6),
         E(50, -14, 44, 23, "#FFFFFF", 6), L("M24,-12 L80,-12", "#E63946", 6),
         R(-78, -400, 156, 255, 78, JEANS, 7),
         P("M-78,-322 A78,78 0 0 1 78,-322 L78,-212 Q0,-196 -78,-212 Z", SHIRT, 7),
         P("M-8,-336 L24,-336 L6,-298 L28,-298 L-16,-238 L-2,-284 L-24,-284 Z", "#E8452C", 4),
         f'<g id="{p}-bigshirt" opacity="0">',
         P("M-112,-300 A112,112 0 0 1 112,-300 L118,-60 Q0,-34 -118,-60 Z", SHIRT, 7),
         P("M-14,-330 L36,-330 L8,-262 L42,-262 L-26,-160 L-4,-238 L-38,-238 Z", "#E8452C", 5),
         '</g>',
         L("M-72,-396 Q0,-346 72,-396", INK, 22), L("M-72,-396 Q0,-346 72,-396", "#3A3A48", 11),
         R(-96, -420, 34, 50, 14, PHONE, 6), R(62, -420, 34, 50, 14, PHONE, 6),
         arm("L"), arm("R"),
         '</g>',
         f'<g id="{p}-head">',
         E(0, -150, 132, 104, HAIR, 7),
         C(0, -108, 122, SKIN, 7),
         P("M-118,-140 L-104,-96 L-96,-142 Z", HAIR, 0), P("M118,-140 L104,-96 L96,-142 Z", HAIR, 0),
         E(-72, -58, 24, 14, "#E07A6F", 0, 'opacity="0.55"'), E(72, -58, 24, 14, "#E07A6F", 0, 'opacity="0.55"'),
         P("M-150,-212 Q-196,-222 -214,-196 Q-196,-176 -116,-180 Z", CAP_D, 6),
         P("M-128,-150 A130,128 0 0 1 128,-150 Q0,-124 -128,-150 Z", CAP, 7),
         P("M-34,-140 A34,30 0 0 1 34,-140 Z", HAIR, 5),
         L("M-34,-140 L34,-140", INK, 5),
         C(0, -258, 10, CAP_D, 5),
         L("M-60,-250 Q-40,-200 -44,-150", CAP_D, 4), L("M60,-250 Q40,-200 44,-150", CAP_D, 4),
         f'<rect id="{p}-browL" x="-24" y="-7" width="48" height="14" rx="7" fill="{HAIR}"/>',
         f'<rect id="{p}-browR" x="-24" y="-7" width="48" height="14" rx="7" fill="{HAIR}"/>',
         ]
    for k, v in eyes.items():
        g.append(f'<g id="{p}-e-{k}" opacity="{1 if k == "dot" else 0}">{v}</g>')
    for k, v in mouths.items():
        g.append(f'<g id="{p}-m-{k}" opacity="{1 if k == "line" else 0}">{v}</g>')
    g += ['</g>', '</g>']
    return "\n".join(g)

# ------------------------------------------------------------------ JS comum
JS_LIB = r"""
const cl=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=u=>{u=cl(u,0,1);return u*u*(3-2*u)};
const eout=u=>{u=cl(u,0,1);return 1-Math.pow(1-u,3)};
const back=u=>{u=cl(u,0,1);const c=1.7;return 1+(c+1)*Math.pow(u-1,3)+c*Math.pow(u-1,2)};
const lerp=(a,b,u)=>a+(b-a)*u;
const $=id=>document.getElementById(id);
const T=(el,s)=>el.setAttribute('transform',s);
const op=(el,v)=>el.setAttribute('opacity',v);
const camT=(z,fx,fy,sx,sy)=>`translate(${540+(sx||0)} ${864+(sy||0)}) scale(${z}) translate(${-fx} ${-fy})`;
function at(keys,t){let v=keys[0][1];for(const k of keys){if(t>=k[0])v=k[1];}return v}
function lastChange(keys,t){let c=-9;for(const k of keys){if(t>=k[0])c=k[0];}return c}
function Rig(p){
  const G=n=>document.getElementById(p+'-'+n);
  const r={wrap:G('wrap'),body:G('body'),head:G('head'),aL:G('armL'),aR:G('armR'),bl:G('browL'),br:G('browR'),
    big:G('bigshirt'),sL:G('slvL'),sR:G('slvR'),nL:G('armLn'),nR:G('armRn'),eyes:{},mouths:{}};
  ['dot','happy','shock','tired','closed','dizzy'].forEach(k=>r.eyes[k]=G('e-'+k));
  ['line','smile','grin','o','yawn','wavy','flat','small','teeth'].forEach(k=>r.mouths[k]=G('m-'+k));
  const DM={neutral:'line',happy:'smile',worried:'wavy',shock:'o',tired:'flat',sleep:'small',dizzy:'wavy',strain:'teeth'};
  const DE={neutral:'dot',happy:'happy',worried:'dot',shock:'shock',tired:'tired',sleep:'closed',dizzy:'dizzy',strain:'dot'};
  const BR={neutral:[0,0],happy:[-6,0],worried:[-6,-16],shock:[-22,-4],tired:[6,6],sleep:[6,0],dizzy:[-10,12],strain:[4,16]};
  r.draw=function(o){
    const t=o.t, ex=at(o.expr,t), ch=t-lastChange(o.expr,t);
    const sq = ch<0.3 ? 1-0.09*Math.sin(Math.PI*ch/0.3) : 1;
    T(r.wrap,`translate(${o.x} ${o.y}) rotate(${o.rot||0}) scale(${o.s})`);
    const b=1+0.014*Math.sin(t*3.1+(o.seed||0));
    T(r.body,`translate(0 -150) scale(${1/Math.sqrt(b)} ${b}) translate(0 150)`);
    T(r.head,`translate(${Math.sin(t*1.7)*2} ${-400+Math.sin(t*3.1+0.6)*4+(1-b)*-150}) rotate(${(o.tilt||0)+Math.sin(t*1.3+(o.seed||0))*1.6}) scale(${2-sq} ${sq})`);
    const a=o.arms||[8,8];
    T(r.aL,`translate(-64 -340) scale(-1 1) rotate(${-a[0]})`);
    T(r.aR,`translate(64 -340) rotate(${-a[1]})`);
    const eye=DE[ex]; for(const k in r.eyes) op(r.eyes[k], k===eye?1:0);
    const m=(o.mouth?at(o.mouth,t):null)||DM[ex]; for(const k in r.mouths) op(r.mouths[k], k===m?1:0);
    const bb=BR[ex];
    T(r.bl,`translate(-42 ${-146+bb[0]}) rotate(${bb[1]})`); T(r.br,`translate(42 ${-146+bb[0]}) rotate(${-bb[1]})`);
    const bk=(((t+(o.seed||0))%3.3)<0.13 && eye==='dot')?0.12:1;
    T(r.eyes.dot,`translate(0 -100) scale(1 ${bk}) translate(0 100)`);
    if(eye==='dizzy') T(r.eyes.dizzy,`translate(0 -100) rotate(${Math.sin(t*9)*8}) translate(0 100)`);
    const ov=o.over?1:0; op(r.big,ov); op(r.sL,ov); op(r.sR,ov); op(r.nL,1-ov); op(r.nR,1-ov);
  };
  return r;
}
"""

def puff_svg(p, n=7):
    return f'<g id="{p}" opacity="0">' + "".join(f'<circle id="{p}-{i}" r="40" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>' for i in range(n)) + '</g>'

JS_PUFF = r"""
function puff(p,x,y,R,u){const g=$(p); if(u<=0||u>=1){op(g,0);return} op(g,1-u);
  for(let i=0;i<7;i++){const a=i/7*Math.PI*2+0.4, d=R*(0.35+0.9*eout(u)), c=$(p+'-'+i);
    c.setAttribute('cx',x+Math.cos(a)*d); c.setAttribute('cy',y+Math.sin(a)*d*0.8); c.setAttribute('r',R*0.42*(1-0.5*u));}}
"""

def sweat_svg(p): return f'<g id="{p}" opacity="0">' + P("M0,-34 C22,0 18,18 0,18 C-18,18 -22,0 0,-34 Z", "#7EC8F2", 4) + '</g>'
def burst_svg(p, txt="?"):
    pts = " ".join(f"{math.cos(k*math.pi/10)*(70 if k % 2 == 0 else 44):.1f},{math.sin(k*math.pi/10)*(70 if k % 2 == 0 else 44):.1f}" for k in range(20))
    return (f'<g id="{p}" opacity="0"><polygon points="{pts}" {st("#FFD93D", 6)}/>'
            f'<text x="0" y="26" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="78" fill="#4A63E7" stroke="{INK}" stroke-width="4" paint-order="stroke">{txt}</text></g>')
def star4(x, y, r, fill="#FFFFFF", extra=""):
    pts = []
    for k in range(8):
        rad = r if k % 2 == 0 else r*0.22
        a = -math.pi/2 + k*math.pi/4
        pts.append(f"{x+math.cos(a)*rad:.1f},{y+math.sin(a)*rad:.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" {extra}/>'

def grad(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'
def rgrad(id_, color, a=0.6):
    return f'<radialGradient id="{id_}"><stop offset="0" stop-color="{color}" stop-opacity="{a}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'

BIG = (-800, -800, W+1600, H+1600)
def fullrect(fill): return f'<rect x="{BIG[0]}" y="{BIG[1]}" width="{BIG[2]}" height="{BIG[3]}" fill="{fill}"/>'

# ------------------------------------------------------------------ cenários
def bedroom(p, floor_y=1480):
    s = [f'<defs>{grad(p+"-sky", [(0, "#FF9A62"), (0.55, "#FFD48A"), (1, "#FFE9B8")])}{rgrad(p+"-sun", "#FFF3C4", 0.7)}</defs>',
         fullrect("#F3D6BF")]
    s += [f'<rect x="{k*80}" y="-800" width="34" height="{floor_y+800}" fill="#E7BFA1" opacity="0.6"/>' for k in range(-10, 24)]
    wx, wy, ww, wh = 110, 380, 360, 470
    s += [R(wx-10, wy-10, ww+20, wh+20, 14, "#FFFFFF", 7), R(wx, wy, ww, wh, 8, f"url(#{p}-sky)", 6),
          C(wx+ww*0.55, wy+wh*0.62, 160, f"url(#{p}-sun)", 0), C(wx+ww*0.55, wy+wh*0.62, 60, "#FFF3C4", 0),
          R(wx, wy+wh*0.72, ww, wh*0.28, 0, "#E98A5B", 0),
          L(f"M{wx+ww/2},{wy} L{wx+ww/2},{wy+wh}", "#FFFFFF", 14), L(f"M{wx},{wy+wh/2} L{wx+ww},{wy+wh/2}", "#FFFFFF", 14),
          R(wx-30, wy+wh+5, ww+60, 34, 10, "#FFFFFF", 6)]
    # pôster de foguete
    s += [R(690, 400, 250, 320, 8, "#3B3F7A", 6)] + [star4(730+k*45, 470+(k % 2)*60, 18, "#FFD93D") for k in range(5)]
    s += [P("M815,520 Q855,580 845,660 L785,660 Q775,580 815,520 Z", "#FFFFFF", 5), C(815, 590, 14, "#4FC3E8", 4),
          P("M785,640 L760,690 L792,665 Z", "#E63946", 4), P("M845,640 L870,690 L838,665 Z", "#E63946", 4)]
    s += [R(-800, floor_y, W+1600, 1600, 0, "#C98A4B", 0)]
    s += [L(f"M-800,{floor_y+40+k*k*12} L{W+800},{floor_y+40+k*k*12}", "#7A4A22", 4, 'opacity="0.45"') for k in range(9)]
    s += [L(f"M-800,{floor_y} L{W+800},{floor_y}", INK, 8), E(540, floor_y+170, 430, 120, "#E86A5B", 5)]
    s += [R(760, 1060, 70, 470, 14, "#9A5B2E", 6), R(800, 1250, 420, 230, 30, "#4E8FE0", 6), R(840, 1180, 200, 90, 40, "#FFFFFF", 6),
          R(40, 1240, 220, 250, 10, "#B8743E", 6), R(60, 1300, 180, 70, 8, "#C98A4B", 5), C(150, 1335, 10, "#FFD93D", 4)]
    return "\n".join(s)

def clock_svg(p):
    s = [f'<g id="{p}">', C(-48, -70, 26, "#FFD93D", 6), C(48, -70, 26, "#FFD93D", 6), C(0, 0, 80, "#2EC4B6", 7), C(0, 0, 58, "#FFFFFF", 5),
         L("M0,0 L0,-38", INK, 6), L("M0,0 L28,10", INK, 6), '</g>', f'<g id="{p}-ring" opacity="0">']
    for k in range(3):
        a = -0.9 + k*0.25
        for sx in (-1, 1):
            s.append(L(f"M{sx*math.cos(a)*105:.1f},{math.sin(a)*105:.1f} L{sx*math.cos(a)*140:.1f},{math.sin(a)*140:.1f}", INK, 7))
    s.append('</g>')
    return "\n".join(s)

def calendar_page_svg(id_, day_id=None):
    w, h = 230, 260
    pts = f"M{-w/2},{-h/2} L{w/2},{-h/2} L{w/2},{h/2-14} " + " ".join(f"L{w/2-(k+0.5)*w/9:.1f},{h/2+(12 if k % 2 == 0 else -6)}" for k in range(9)) + f" L{-w/2},{h/2-14} Z"
    s = [f'<g id="{id_}" opacity="0">', f'<path d="{pts}" fill="#FFFFFF" stroke="#33334A" stroke-opacity="0.55" stroke-width="3"/>',
         f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="56" fill="#D9363E"/>', C(-60, -h/2+28, 9, "#3A1015", 0), C(60, -h/2+28, 9, "#3A1015", 0)]
    if day_id:
        s.append(f'<text id="{day_id}" x="0" y="72" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="120" fill="#2A2A35">1</text>')
    else:
        s += [L(f"M{-w/2+30},{-h/2+90+k*36} L{w/2-30-(k % 2)*40},{-h/2+90+k*36}", "#9A9AA6", 5) for k in range(4)]
    s.append('</g>')
    return "\n".join(s)

# ------------------------------------------------------------------ cenas (markup + frame JS)
def scene_bedroom_open(sc):
    p = sc["id"]; tm = wt(sc, "metade")
    svg = (bedroom(p) + f'<g transform="translate(150 1160)">{clock_svg(p+"-clk")}</g>' + leo(p+"-leo") + puff_svg(p+"-pf")
           + f'<g id="{p}-spk" opacity="0">' + "".join(star4(540+math.cos(k*1.6)*190, 1250+math.sin(k*1.6)*110, 26) for k in range(4)) + '</g>')
    js = f"""
const leo=Rig('{p}-leo'); const TM={tm};
function frame(t){{
  const z = t<TM ? lerp(1.04,1.12,ease(t/TM)) : lerp(1.12,1.62,eout((t-TM-0.1)/0.8));
  const fy = t<TM ? 960 : lerp(960,1330,eout((t-TM-0.1)/0.8));
  T($('{p}-cam'), camT(z,540,fy));
  const ring=t<TM; T($('{p}-clk'), `translate(${{ring?Math.sin(t*60)*7:0}} 0) rotate(${{ring?Math.sin(t*60)*1.5:0}})`); op($('{p}-clk-ring'), ring?1:0);
  const s = lerp(1.25,0.6,ease((t-TM)/0.28));
  const yawn = t>0.45 && t<1.5;
  leo.draw({{t,x:540,y:1640,s,expr:[[0,'tired'],[TM+0.12,'shock']],mouth:[[0,null],[0.45,'yawn'],[1.5,null]],
    arms: t<TM ? (yawn?[lerp(8,150,ease((t-0.45)/0.3))-lerp(0,142,ease((t-1.2)/0.3)),lerp(8,150,ease((t-0.5)/0.3))-lerp(0,142,ease((t-1.25)/0.3))]:[8,8]) : [lerp(8,165,eout((t-TM)/0.2)),lerp(8,160,eout((t-TM-0.05)/0.2))]}});
  puff('{p}-pf',540,1640-300*s,220,(t-TM)/0.6);
  op($('{p}-spk'), t>TM+0.15?0.9:0); T($('{p}-spk'), `translate(0 ${{Math.sin(t*3)*10}})`);
}}"""
    return svg, js

def scene_oversize(sc):
    p = sc["id"]; tr = wt(sc, "roupa"); ti = wt(sc, "inteira")
    svg = bedroom(p) + f'<g transform="translate(150 1160)">{clock_svg(p+"-clk")}</g>' + leo(p+"-leo") + sweat_svg(p+"-sw")
    js = f"""
const leo=Rig('{p}-leo'); const TR={tr}, TI={ti};
function frame(t){{
  let z=lerp(1.62,1.42,ease(t/TR)), fy=1460;
  if(t>TI-0.05){{ const u=eout((t-TI+0.05)/0.25); z=lerp(z,2.2,u); fy=lerp(1460,1340,u); }}
  T($('{p}-cam'), camT(z,540,fy)); op($('{p}-clk-ring'),0);
  leo.draw({{t,x:540,y:1660,s:0.6,over:true,expr:[[0,'neutral'],[0.9,'worried']],arms: t>TR?[8,150+Math.sin(t*12)*22]:[8,8]}});
  op($('{p}-sw'), t>TR?1:0); T($('{p}-sw'), `translate(${{540+80}} ${{1660-330+((t*90)%60)*0.7}}) scale(0.8)`);
}}"""
    return svg, js

def living_room(p):
    s = [fullrect("#6E82BC")] + [f'<rect x="{k*90}" y="-800" width="6" height="2320" fill="#FFFFFF" opacity="0.1"/>' for k in range(-8, 20)]
    s += [R(-120, 820, 420, 720, 60, "#C0473F", 7), R(-120, 1080, 520, 440, 50, "#D85A50", 7),
          R(-800, 1520, W+1600, 1600, 0, "#B65A3C", 0)]
    s += [L(f"M{k*70},1520 L{k*70-200},2400", "#000000", 10, 'opacity="0.08"') for k in range(-6, 24)]
    s.append(L(f"M-800,1520 L{W+800},1520", INK, 8))
    return "\n".join(s)

def cat_svg(p, r=430):
    s = [f'<g id="{p}">']
    for sx in (-1, 1):
        s.append(P(f"M{sx*r*0.95:.0f},{-r*0.25:.0f} L{sx*r*0.78:.0f},{-r*1.25:.0f} L{sx*r*0.25:.0f},{-r*0.85:.0f} Z", "#F2973A", 9))
        s.append(P(f"M{sx*r*0.82:.0f},{-r*0.42:.0f} L{sx*r*0.74:.0f},{-r*1.0:.0f} L{sx*r*0.42:.0f},{-r*0.8:.0f} Z", "#F7B3B8", 0))
    s.append(E(0, 0, r*1.05, r*0.92, "#F2973A", 9))
    s += [L(f"M{-r*0.25+k*r*0.25:.0f},{-r*0.88:.0f} L{-r*0.2+k*r*0.2:.0f},{-r*0.55:.0f}", "#C96E1E", 22) for k in range(3)]
    s.append(E(0, r*0.38, r*0.55, r*0.4, "#FFF1DE", 0))
    for sx in (-1, 1):
        ex = sx*r*0.42
        s.append(E(ex, -r*0.05, r*0.25, r*0.29, "#C9E35A", 8))
        s.append(f'<ellipse id="{p}-pup{"L" if sx < 0 else "R"}" cx="{ex:.0f}" cy="{-r*0.05:.0f}" rx="{r*0.21:.0f}" ry="{r*0.26:.0f}" fill="{INK}"/>')
        s.append(C(ex+r*0.08, -r*0.15, r*0.05, "#FFFFFF", 0))
        s += [L(f"M{sx*r*0.4:.0f},{r*0.35+k*r*0.08:.0f} L{sx*r*1.35:.0f},{r*0.25+k*r*0.14:.0f}", INK, 5) for k in range(3)]
    s += [P(f"M{-r*0.1:.0f},{r*0.2:.0f} L{r*0.1:.0f},{r*0.2:.0f} L0,{r*0.32:.0f} Z", "#F27C8A", 6),
          L(f"M0,{r*0.32:.0f} Q0,{r*0.45:.0f} {-r*0.22:.0f},{r*0.42:.0f}", INK, 7), L(f"M0,{r*0.32:.0f} Q0,{r*0.45:.0f} {r*0.22:.0f},{r*0.42:.0f}", INK, 7), '</g>']
    s += [f'<g id="{p}-paw">', E(0, 0, 230, 150, "#F2973A", 9)] + [E(-140+k*20, -80+k*70, 40, 34, "#F7B3B8", 0) for k in range(3)] + ['</g>']
    return "\n".join(s)

def scene_cat(sc):
    p = sc["id"]; tg, to, td = wt(sc, "gato"), wt(sc, "olhar"), wt(sc, "diferente")
    svg = living_room(p) + cat_svg(p+"-cat") + leo(p+"-leo") + sweat_svg(p+"-sw")
    js = f"""
const leo=Rig('{p}-leo'); const TG={tg},TO={to},TD={td};
function frame(t){{
  let z=lerp(1.0,1.08,ease(t/TD)), fx=540, fy=1180;
  if(t>TD+0.35){{ const u=eout((t-TD-0.35)/0.3); z=lerp(z,1.9,u); fx=lerp(540,330,u); fy=lerp(1180,1330,u); }}
  T($('{p}-cam'), camT(z,fx,fy));
  T($('{p}-cat'), `translate(720 ${{720+Math.sin(t*1.5)*8}})`);
  const sl=lerp(1,0.2,ease((t-TO)/0.4));
  ['L','R'].forEach(k=>$('{p}-cat-pup'+k).setAttribute('rx', (430*0.21*sl).toFixed(1)));
  T($('{p}-cat-paw'), `translate(${{lerp(1350,820,ease((t-TD)/0.5))}} ${{720+430*1.25}})`);
  leo.draw({{t,x:300,y:1720,s:0.6,tilt:-8,expr:[[0,'neutral'],[TG,'worried'],[TD+0.15,'shock']],arms:t>TD+0.15?[lerp(8,165,eout((t-TD-0.15)/0.2)),lerp(8,158,eout((t-TD-0.2)/0.2))]:[8,8]}});
  op($('{p}-sw'), t>TG?1:0); T($('{p}-sw'), `translate(${{300+90}} ${{1720-380+((t*90)%60)*0.8}}) scale(0.9)`);
}}"""
    return svg, js

def tabletop(p):
    s = [f'<defs>{rgrad(p+"-lamp", "#FFD48A", 0.4)}</defs>', fullrect("#3A3358"), C(820, 300, 520, f"url(#{p}-lamp)", 0),
         R(-800, 1350, W+1600, 1600, 0, "#A0623A", 0)]
    s += [L(f"M-800,{1380+k*k*14} C400,{1370+k*k*14+20} 700,{1395+k*k*14} {W+800},{1380+k*k*14}", "#5A2E14", 4, 'opacity="0.4"') for k in range(7)]
    s += [L(f"M-800,1350 L{W+800},1350", INK, 8),
          R(-80, 250, 430, 1120, 40, "#F4F1EA", 8), R(-76, 600, 422, 120, 0, "#E63946", 0),
          L("M350,630 A170,170 0 0 1 350,970", INK, 70), L("M350,630 A170,170 0 0 1 350,970", "#F4F1EA", 54)]
    s += [f'<path id="{p}-steam{k}" d="M0,120 C-30,60 30,30 0,-30" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.35"/>' for k in range(3)]
    s += ['<g transform="translate(560 1330) rotate(-3.4)">', R(0, -60, 760, 70, 8, "#FFC93C", 6), R(-60, -60, 60, 70, 4, "#F28B8B", 6), '</g>']
    return "\n".join(s)

def scene_matchbox(sc):
    p = sc["id"]; tf = wt(sc, "fósforo")
    x, y = 540, 1250
    box = [R(x-330, y-250, 660, 300, 14, "#F3E3C3", 8), R(x-300, y-225, 600, 250, 8, "#E3CDA2", 0),
           E(520, 1120, 70, 50, "#FFFFFF", 6)]
    blanket = [P("M640,1030 C700,1010 780,1050 860,1020 L860,1190 C780,1200 700,1180 630,1195 Z", "#F28B8B", 6)] + \
              [C(680+k*50, 1090+(k % 2)*40, 12, "#FFFFFF", 0, 'opacity="0.7"') for k in range(4)]
    front = [R(x-340, y+20, 680, 120, 10, "#D9363E", 8),
             f'<text x="{x}" y="{y+102}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="64" fill="#FFE9B8">FÓSFOROS</text>']
    for k in range(3):
        front += [limb(f"M{x+380+k*60},{y+150} L{x+470+k*60},{y+90}", "#F3D19A", 12), C(x+472+k*60, y+88, 18, "#C0392B", 5)]
    zz = "".join(f'<text id="{p}-z{k}" font-family="Nunito" font-weight="900" font-size="{44+k*14}" fill="#FFFFFF" opacity="0">Z</text>' for k in range(3))
    svg = tabletop(p) + "\n".join(box) + leo(p+"-leo") + "\n".join(blanket) + "\n".join(front) + zz
    js = f"""
const leo=Rig('{p}-leo'); const TF={tf};
function frame(t){{
  let z=lerp(1.45,1.6,ease(t/TF)), fx=540, fy=1180;
  if(t>TF+0.2){{ const u=eout((t-TF-0.2)/0.3); z=lerp(z,2.4,u); fx=lerp(540,560,u); fy=lerp(1180,1120,u); }}
  T($('{p}-cam'), camT(z,fx,fy));
  for(let k=0;k<3;k++){{ const y0=220-((t*80+k*90)%260); T($('{p}-steam'+k), `translate(${{60+k*90}} ${{y0}})`); }}
  leo.draw({{t,x:780,y:1110,s:0.42,rot:-90,expr:[[0,'sleep'],[TF+0.2,'neutral']],mouth:[[0,null],[TF+0.2,'line']],arms:[8,8]}});
  for(let k=0;k<3;k++){{ const ph=(t*0.9+k*0.33)%1, e=$('{p}-z'+k);
    e.setAttribute('x',(560+ph*60+k*28).toFixed(1)); e.setAttribute('y',(1000-ph*110-k*26).toFixed(1)); op(e, t<TF?(1-ph):0); }}
}}"""
    return svg, js

def ground(p):
    s = [f'<defs>{grad(p+"-sky", [(0, "#BFE6F2"), (1, "#E6F4D6")])}</defs>', f'<rect x="-800" y="-800" width="{W+1600}" height="2250" fill="url(#{p}-sky)"/>']
    for k in range(9):
        x = -60 + k*150 + math.sin(k*3)*40
        s.append(f'<path id="{p}-gr{k}" d="M{x:.0f},1460 C{x+30:.0f},900 {x+60:.0f},500 {x+90:.0f},{200+k % 3*120} C{x+90:.0f},600 {x+110:.0f},1000 {x+120:.0f},1460 Z" fill="{["#7CC46A", "#5FAF57", "#8FD27A"][k % 3]}" opacity="0.8"/>')
    s.append(R(-800, 1450, W+1600, 1600, 0, "#8A5A3C", 0))
    r = random.Random(3)
    s += [E(r.uniform(-200, W+200), r.uniform(1470, 2300), r.uniform(10, 40), r.uniform(6, 20), "#6B4129", 0, 'opacity="0.6"') for _ in range(60)]
    s.append(L(f"M-800,1450 C300,1430 700,1470 {W+800},1445", INK, 8))
    return "\n".join(s)

def ant_svg(p):
    s = [f'<g id="{p}">']
    for i, lx in enumerate((-80, 0, 70)):
        for side in (0, 1):
            s.append(f'<path id="{p}-l{i}{side}" d="" fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>')
    s += [E(-150, -95, 95, 70, "#5A2E1C", 7), E(-20, -95, 55, 42, "#6E3A24", 7), C(95, -120, 62, "#6E3A24", 7),
          C(120, -132, 16, "#FFFFFF", 0), C(124, -132, 7, INK, 0),
          L("M110,-175 C140,-260 190,-250 200,-230", INK, 8), L("M120,-175 C170,-260 220,-250 230,-230", INK, 8),
          L("M140,-95 C150,-80 135,-75 125,-88", INK, 5),
          f'<g id="{p}-cube">', R(-110, -110, 220, 200, 18, "#FFFFFF", 7)]
    s += [C(-80+(k*53) % 170, -80+(k*37) % 150, 8, "#DDE6F2", 0) for k in range(10)]
    s += ['</g>', '</g>']
    return "\n".join(s)

def scene_ant(sc):
    p = sc["id"]; ta, tf = wt(sc, "formiga"), wt(sc, "forte")
    crumb = ['<g transform="translate(370 1540) scale(1.35)">', P("M-90,0 C-110,-80 -40,-150 20,-130 C100,-140 120,-50 95,0 Z", "#D9A35B", 7)]
    crumb += [C(-60+k*18, -60-(k % 3)*20, 7, "#B9823E", 0) for k in range(8)] + ['</g>']
    svg = ground(p) + "\n".join(crumb) + leo(p+"-leo") + sweat_svg(p+"-sw") + ant_svg(p+"-ant")
    js = f"""
const leo=Rig('{p}-leo'); const TA={ta},TF={tf};
function frame(t){{
  let z=lerp(1.15,1.05,ease(t/TF)), fx=560, fy=1260;
  if(t>TF){{ const u=eout((t-TF)/0.3); z=lerp(z,1.45,u); fx=lerp(560,420,u); fy=lerp(1260,1330,u); }}
  T($('{p}-cam'), camT(z,fx,fy));
  for(let k=0;k<9;k++) T($('{p}-gr'+k), `skewX(${{Math.sin(t*1.2+k)*1.2}})`);
  const ax=lerp(1450,700,ease((t-TA+0.7)/1.5))+Math.max(0,t-TF-0.3)*190;
  T($('{p}-ant'), `translate(${{ax}} 1580) scale(1.25)`);
  for(let i=0;i<3;i++) for(let s=0;s<2;s++){{ const lx=[-80,0,70][i], o=Math.sin(t*14+i*2+s*Math.PI)*25;
    $('{p}-ant-l'+i+s).setAttribute('d',`M${{lx}},-70 L${{lx+o-40}},-20 L${{lx+o-60}},0`); }}
  T($('{p}-ant-cube'), `translate(40 ${{-310+Math.sin(t*14)*6}}) rotate(3)`);
  const jit=Math.sin(t*40)*2;
  leo.draw({{t,x:200+jit,y:1580,s:0.6,tilt:12,expr:[[0,'strain'],[TF+0.1,'worried']],arms:[-62,72]}});
  op($('{p}-sw'),1); T($('{p}-sw'), `translate(${{200-100}} ${{1580-370+((t*90)%60)*0.7}}) scale(0.8)`);
}}"""
    return svg, js

def dust(p):
    r = random.Random(11)
    s = [fullrect("#33283F")]
    s += [P(f"M{200+k*180},-800 L{520+k*180},-800 L{1200+k*120},2400 L{800+k*120},2400 Z", "#FFE2A8", 0, 'opacity="0.07"') for k in range(4)]
    parts = []
    for k in range(90):
        x, y, rad, a, vx, vy = r.uniform(0, W), r.uniform(0, H), r.uniform(3, 16), r.uniform(0.15, 0.45), r.uniform(-20, 20), r.uniform(5, 30)
        s.append(f'<circle id="{p}-d{k}" r="{rad:.1f}" fill="#FFE9C8" opacity="{a:.2f}"/>')
        parts.append([round(x), round(y), round(vx, 1), round(vy, 1)])
    return "\n".join(s), parts

def mite_svg(p):
    s = [f'<g id="{p}">']
    for k in range(4):
        for sx in (-1, 1):
            s.append(f'<g id="{p}-lg{k}{"a" if sx < 0 else "b"}">' + limb(f"M{-120+k*80},{sx*80} L{-150+k*80},{sx*200} L{-190+k*80},{sx*240}", "#E7CDA8", 16) + '</g>')
    s.append(E(0, 0, 260, 170, "#EED8B6", 9))
    s += [L(f"M{math.cos(a)*240:.0f},{math.sin(a)*155:.0f} L{math.cos(a)*330:.0f},{math.sin(a)*230:.0f}", INK, 5) for a in [k/14*2*math.pi for k in range(14)]]
    s += [E(-60, -40, 110, 50, "#FFFFFF", 0, 'opacity="0.35"'), E(-290, 10, 80, 65, "#D9B98F", 8)]
    s += [f'<path id="{p}-md{"a" if sy < 0 else "b"}" d="M-350,{sy*25} C-420,{sy*30} -430,{sy*14} -400,0" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>' for sy in (-1, 1)]
    for sy in (-1, 1):
        s += [C(-300, sy*28-5, 18, "#FFFFFF", 5), C(-306, sy*28-5, 8, INK, 0)]
    s.append('</g>')
    return "\n".join(s)

def scene_mite(sc):
    p = sc["id"]; tm = wt(sc, "ácaro"); tmo = wt(sc, "monstro")
    bg, parts = dust(p)
    svg = bg + mite_svg(p+"-mite") + leo(p+"-leo")
    js = f"""
const leo=Rig('{p}-leo'); const TM={tm},TMO={tmo}; const PARTS={json.dumps(parts)};
function frame(t){{
  let z=lerp(1.0,1.08,ease(t/TMO)), fx=540, fy=1000;
  if(t>TMO+0.1){{ const u=eout((t-TMO-0.1)/0.3); z=lerp(z,1.35,u); fx=lerp(540,480,u); fy=lerp(1000,1100,u); }}
  T($('{p}-cam'), camT(z,fx,fy));
  PARTS.forEach((q,k)=>{{ const e=$('{p}-d'+k); e.setAttribute('cx',(((q[0]+t*q[2])%{W}+{W})%{W}).toFixed(1)); e.setAttribute('cy',(((q[1]-t*q[3])%{H}+{H})%{H}).toFixed(1)); }});
  const mx=lerp(1300,800,ease((t-TM+0.3)/1.0));
  T($('{p}-mite'), `translate(${{mx}} ${{760+Math.sin(t*2)*15}}) scale(0.95) rotate(-8.6)`);
  for(let k=0;k<4;k++){{ T($('{p}-mite-lg'+k+'a'), `rotate(${{Math.sin(t*8+k)*6}} ${{-120+k*80}} -80)`); T($('{p}-mite-lg'+k+'b'), `rotate(${{Math.sin(t*8+k+1)*6}} ${{-120+k*80}} 80)`); }}
  ['a','b'].forEach((k,i)=>{{ const sy=i?1:-1; $('{p}-mite-md'+k).setAttribute('d',`M-350,${{sy*25}} C-420,${{sy*30}} -430,${{sy*(10+Math.sin(t*10)*12)}} -400,0`); }});
  leo.draw({{t,x:300,y:1440+Math.sin(t*1.7)*25,s:0.68,rot:Math.sin(t*0.8)*11,expr:[[0,'worried'],[TM+0.2,'shock']],arms:t<TM?[80,80]:[lerp(80,165,eout((t-TM-0.2)/0.2)),lerp(80,160,eout((t-TM-0.25)/0.2))]}});
}}"""
    return svg, js

def bact_svg(id_, color):
    s = [f'<g id="{id_}">', f'<path id="{id_}-fl" d="" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>', R(-180, -80, 360, 160, 80, color, 8)]
    s += [C(-120+k*40, -20+(k % 2)*40, 12, "#FFFFFF", 0, 'opacity="0.35"') for k in range(7)]
    for sx in (-1, 1): s += [C(110+sx*22, -10, 12, "#FFFFFF", 0), C(112+sx*22, -10, 6, INK, 0)]
    s += [L("M100,25 C110,38 130,38 140,25", INK, 5), '</g>']
    return "\n".join(s)

JS_FLAG = r"""
function flag(id,t){let d='M-170,0';for(let k=0;k<30;k++){d+=` L${-170-k*12},${(Math.sin(k*0.5-t*12)*22).toFixed(1)}`}$(id).setAttribute('d',d)}
"""

def scene_water(sc):
    p = sc["id"]; tg = wt(sc, "oceano")
    r = random.Random(5)
    s = [f'<defs>{grad(p+"-w", [(0, "#4FC3E8"), (1, "#1A5FA8")])}</defs>', f'<rect x="-800" y="-800" width="{W+1600}" height="{H+1600}" fill="url(#{p}-w)"/>']
    s += [f'<path id="{p}-wv{k}" d="" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="{0.14-k*0.018:.3f}"/>' for k in range(6)]
    bub = []
    for k in range(26):
        x, y, v, rad = r.uniform(0, W), r.uniform(0, H), r.uniform(60, 160), r.uniform(8, 30)
        s.append(f'<g id="{p}-b{k}">' + C(0, 0, rad, "#FFFFFF", 0, 'fill-opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="3"') + C(-rad*0.35, -rad*0.35, rad*0.25, "#FFFFFF", 0, 'opacity="0.7"') + '</g>')
        bub.append([round(x), round(y), round(v)])
    svg = "\n".join(s) + bact_svg(p+"-ba", "#7DDB6A") + bact_svg(p+"-bb", "#B48CF0") + bact_svg(p+"-bc", "#FFB36B") + leo(p+"-leo")
    js = JS_FLAG + f"""
const leo=Rig('{p}-leo'); const TG={tg}; const BUB={json.dumps(bub)};
function frame(t){{
  let z=lerp(1.12,1.0,ease(t/TG)), fy=960;
  if(t>TG+0.15){{ const u=eout((t-TG-0.15)/0.6); z=lerp(z,0.72,u); fy=lerp(960,900,u); }}
  T($('{p}-cam'), camT(z,540,fy));
  for(let k=0;k<6;k++){{ let d=''; for(let x=-800;x<={W}+800;x+=40) d+=(x===-800?'M':'L')+x+','+(120+k*60+Math.sin(x*0.012+t*2+k)*14).toFixed(1)+' '; $('{p}-wv'+k).setAttribute('d',d); }}
  BUB.forEach((q,k)=>T($('{p}-b'+k), `translate(${{(q[0]+Math.sin(t*2+k)*12).toFixed(1)}} ${{((((q[1]-t*q[2])%({H}+100))+({H}+100))%({H}+100)-50).toFixed(1)}})`));
  T($('{p}-ba'), `translate(${{820-t*40}} 420) rotate(14) scale(0.9)`); flag('{p}-ba-fl',t);
  T($('{p}-bb'), `translate(${{120+t*25}} 1500) rotate(-29) scale(0.8)`); flag('{p}-bb-fl',t+1);
  T($('{p}-bc'), `translate(920 ${{1650-t*30}}) rotate(149) scale(0.7)`); flag('{p}-bc-fl',t+2);
  leo.draw({{t,x:540,y:1330+Math.sin(t*2)*20,s:0.72,rot:Math.sin(t*1.3)*7,expr:[[0,'shock'],[TG+0.3,'worried']],mouth:[[0,null],[1.2,'small'],[TG+0.3,null]],arms:[95+Math.sin(t*6)*40,95+Math.sin(t*6+1)*40]}});
}}"""
    return svg, js

def virus_svg(p, r=220):
    s = [f'<g id="{p}-spin">']
    for k in range(16):
        a = k/16*2*math.pi
        s.append(limb(f"M{math.cos(a)*r*0.9:.0f},{math.sin(a)*r*0.9:.0f} L{math.cos(a)*r*1.32:.0f},{math.sin(a)*r*1.32:.0f}", "#F27CA6", 12))
        s.append(C(math.cos(a)*r*1.36, math.sin(a)*r*1.36, r*0.11, "#FFC93C", 6))
    s.append(C(0, 0, r, "#D9367A", 9))
    s += [C(math.cos(k*2.3)*r*(0.3+(k % 3)*0.2), math.sin(k*2.3)*r*(0.3+(k % 3)*0.2), r*0.09, "#A8205A", 0) for k in range(9)]
    s.append('</g>')
    for sx in (-1, 1):
        s += [C(sx*r*0.32, -r*0.1, r*0.16, "#FFFFFF", 6), C(sx*r*0.32-r*0.05, -r*0.08, r*0.07, INK, 0), L(f"M{sx*r*0.15:.0f},{-r*0.32:.0f} L{sx*r*0.5:.0f},{-r*0.4:.0f}", INK, 9)]
    s.append(L(f"M{-r*0.2:.0f},{r*0.32:.0f} C{-r*0.1:.0f},{r*0.2:.0f} {r*0.1:.0f},{r*0.2:.0f} {r*0.2:.0f},{r*0.32:.0f}", INK, 8))
    return f'<g id="{p}">' + "\n".join(s) + '</g>'

def scene_virus(sc):
    p = sc["id"]; tv = wt(sc, "vírus")
    s = [fullrect("#4E2160"), f'<g transform="translate(540 300) rotate(5.7) scale(3.2)">{bact_svg(p+"-big", "#5FAF57")}</g>', fullrect("#33103F").replace('/>', ' opacity="0.45"/>')]
    svg = "\n".join(s) + virus_svg(p+"-vir") + leo(p+"-leo") + f'<g id="{p}-qw">{burst_svg(p+"-q")}</g>'
    js = JS_FLAG + f"""
const leo=Rig('{p}-leo'); const TV={tv};
function frame(t){{
  let z=lerp(1.0,1.08,ease(t/TV)), fx=540, fy=1000;
  if(t>TV+0.9){{ const u=eout((t-TV-0.9)/0.3); z=lerp(z,1.3,u); fx=lerp(540,470,u); fy=lerp(1000,1150,u); }}
  T($('{p}-cam'), camT(z,fx,fy)); flag('{p}-big-fl',t);
  T($('{p}-vir'), `translate(${{lerp(1450,790,eout((t-TV+0.2)/0.9))}} 900)`); T($('{p}-vir-spin'), `rotate(${{t*28}})`);
  leo.draw({{t,x:270,y:1680,s:0.66,tilt:-6,expr:[[0,'neutral'],[TV+0.2,'shock']],arms:t<TV+0.2?[8,8]:[lerp(8,85,eout((t-TV-0.2)/0.2)),lerp(8,160,eout((t-TV-0.25)/0.2))]}});
  op($('{p}-q'), t>TV+0.5?1:0); const pu=back((t-TV-0.5)/0.3);
  T($('{p}-q'), `translate(270 ${{1680-520}}) scale(${{pu}}) rotate(${{Math.sin(t*6)*7}})`);
}}"""
    return svg, js

def scene_atom(sc):
    p = sc["id"]; te = wt(sc, "Elétrons"); cx, cy = 540, 620
    r = random.Random(9)
    s = [f'<defs>{rgrad(p+"-glow", "#7A5CFF", 0.4)}{rgrad(p+"-eg", "#6FE8FF", 0.8)}</defs>', fullrect("#120E30")]
    s += [C(r.uniform(-300, W+300), r.uniform(-300, H+300), r.uniform(1, 3), "#FFFFFF", 0, f'opacity="{r.uniform(0.2, 0.8):.2f}"') for _ in range(160)]
    s.append(C(cx, cy, 420, f"url(#{p}-glow)", 0))
    orbits = [[0.0, 460, 150, 1.6], [1.05, 460, 150, -1.25], [2.1, 460, 150, 1.9]]
    for rot, a, b, sp in orbits:
        s.append(f'<ellipse cx="0" cy="0" rx="{a}" ry="{b}" fill="none" stroke="#8FD8FF" stroke-opacity="0.55" stroke-width="6" transform="translate({cx} {cy}) rotate({math.degrees(rot):.1f})"/>')
    rr_ = random.Random(2)
    s.append(f'<g id="{p}-nuc">')
    for k in range(14):
        a = rr_.uniform(0, 2*math.pi); d = rr_.uniform(0, 60)
        s += [C(cx+math.cos(a)*d, cy+math.sin(a)*d, 42, "#E84A5F" if k % 2 else "#4A7BE8", 6), C(cx+math.cos(a)*d-12, cy+math.sin(a)*d-12, 10, "#FFFFFF", 0, 'opacity="0.6"')]
    s.append('</g>')
    for i in range(3):
        s += [f'<circle id="{p}-tr{i}-{k}" r="{22-k*2}" fill="#6FE8FF" opacity="{0.35-k*0.035:.3f}"/>' for k in range(1, 9)]
        s += [f'<circle id="{p}-eg{i}" r="70" fill="url(#{p}-eg)"/>', f'<circle id="{p}-el{i}" r="24" {st("#B8F6FF", 5)}/>']
    s += [f'<path id="{p}-sl{k}" d="M0,0 L260,0" stroke="#8FD8FF" stroke-opacity="0.6" stroke-width="6" stroke-linecap="round" opacity="0"/>' for k in range(6)]
    svg = "\n".join(s) + leo(p+"-leo") + f'<g id="{p}-fly" opacity="0"><circle r="110" fill="url(#{p}-eg)"/><circle r="34" {st("#B8F6FF", 6)}/></g>'
    js = f"""
const leo=Rig('{p}-leo'); const TE={te}; const OR={json.dumps(orbits)};
function frame(t){{
  let z=lerp(1.0,1.08,ease(t/TE)), fx=540, fy=900, sx=0, sy=0;
  if(t>TE){{ sx=Math.sin(t*47)*6; sy=Math.cos(t*41)*6; }}
  if(t>TE+0.9){{ const u=eout((t-TE-0.9)/0.3); z=lerp(z,1.6,u); fy=lerp(900,1250,u); }}
  T($('{p}-cam'), camT(z,fx,fy,sx,sy));
  T($('{p}-nuc'), `translate(${{Math.sin(t*20)*2}} ${{Math.cos(t*17)*2}})`);
  OR.forEach((o,i)=>{{ const [rot,a,b,sp]=o; const P=th=>{{const ex=Math.cos(th)*a, ey=Math.sin(th)*b; return [{cx}+ex*Math.cos(rot)-ey*Math.sin(rot), {cy}+ex*Math.sin(rot)+ey*Math.cos(rot)]}};
    const th=t*sp*2.2+i*2; const q=P(th);
    for(let k=1;k<9;k++){{ const w=P(th-k*0.06*Math.sign(sp)); const c=$('{p}-tr'+i+'-'+k); c.setAttribute('cx',w[0].toFixed(1)); c.setAttribute('cy',w[1].toFixed(1)); }}
    ['eg','el'].forEach(n=>{{ const c=$('{p}-'+n+i); c.setAttribute('cx',q[0].toFixed(1)); c.setAttribute('cy',q[1].toFixed(1)); }}); }});
  for(let k=0;k<6;k++){{ const ph=(t*3+k*0.17)%1; const e=$('{p}-sl'+k); op(e, t>TE?1:0); T(e, `translate(${{-300+ph*1600}} ${{1180+k*45}})`); }}
  const ph=((t-TE)*0.9)%1; op($('{p}-fly'), t>TE?1:0); T($('{p}-fly'), `translate(${{lerp(-250,{W}+250,ph)}} ${{1300+Math.sin(ph*6)*30}})`);
  leo.draw({{t,x:540,y:1620,s:0.66,expr:[[0,'shock'],[TE+0.6,'dizzy']],arms:[85+Math.sin(t*9)*8,85+Math.sin(t*9+2)*8],tilt:t>TE?Math.sin(t*9)*6:0}});
}}"""
    return svg, js

def scene_void(sc):
    p = sc["id"]; te = wt(sc, "existe")
    r = random.Random(4)
    s = [f'<defs>{rgrad(p+"-g", "#FFD93D", 0.4)}</defs>', fullrect("#0A0818")]
    stars = []
    for k in range(90):
        x, y, rad, a = r.uniform(-200, W+200), r.uniform(-200, H+200), r.uniform(0.8, 2.6), r.uniform(0.1, 0.5)
        s.append(f'<circle id="{p}-st{k}" cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="#FFFFFF" opacity="{a:.2f}"/>'); stars.append(a)
    s.append(f'<circle id="{p}-gl" cx="0" cy="0" r="1" fill="url(#{p}-g)"/>')
    svg = "\n".join(s) + leo(p+"-leo")
    js = f"""
const leo=Rig('{p}-leo'); const TE={te}; const ST={json.dumps([round(a, 2) for a in stars])};
function frame(t){{
  T($('{p}-cam'), camT(lerp(1.0,1.15,ease(t/{sc['dur']})),540,1000));
  ST.forEach((a,k)=>op($('{p}-st'+k),(a*(0.6+0.4*Math.sin(t*3+k))).toFixed(2)));
  const k=ease(t/(TE+0.5)); const s=lerp(0.62,0.04,k), y=lerp(1500,1120,k);
  const g=$('{p}-gl'); g.setAttribute('cx',540); g.setAttribute('cy',y-300*s); g.setAttribute('r',420*s+80);
  leo.draw({{t,x:540,y,s,expr:[[0,'worried'],[0.9,'shock']],arms:[85+Math.sin(t*4)*10,85+Math.sin(t*4+1)*10]}});
}}"""
    return svg, js

def scene_end(sc):
    p = sc["id"]
    svg = (bedroom(p) + f'<g transform="translate(150 1160)">{clock_svg(p+"-clk")}</g>'
           + f'<defs>{rgrad(p+"-dot", "#FFD93D", 0.9)}</defs><circle id="{p}-dot" cx="900" cy="1205" r="40" fill="url(#{p}-dot)"/>'
           + f'<circle cx="900" cy="1205" r="5" fill="#FFF6C8"/>'
           + f'<g id="{p}-tag"><text x="900" y="1130" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="54" fill="#FFFFFF" stroke="{INK}" stroke-width="14" paint-order="stroke">VOCÊ</text>'
           + L("M900,1145 L900,1172", INK, 14) + L("M900,1145 L900,1172", "#FFFFFF", 6) + '</g>')
    html_extra = f"""
<div id="{p}-card" class="card">
  <div class="card-q">E AMANHÃ?</div>
  <div class="card-row">
    <div id="{p}-optA" class="opt optA"><svg viewBox="-40 -40 80 80" width="96" height="96"><path d="M-14,-30 L14,-30 L14,2 L32,2 L0,34 L-32,2 L-14,2 Z" fill="#1E1B2E"/></svg><span>CONTINUAR<br>ENCOLHENDO</span></div>
    <div id="{p}-optB" class="opt optB"><svg viewBox="-40 -40 80 80" width="96" height="96"><path d="M-14,30 L14,30 L14,-2 L32,-2 L0,-34 L-32,-2 L-14,-2 Z" fill="#1E1B2E"/></svg><span>TENTAR<br>VOLTAR</span></div>
  </div>
  <div class="card-cta">COMENTA AÍ <span id="{p}-arw" class="arw">▼</span></div>
</div>
<div id="{p}-fade" class="fadein"></div>"""
    css = f"""
#{p}-card{{position:absolute;left:0;top:300px;width:100%;display:flex;flex-direction:column;align-items:center;gap:34px;font-family:Nunito;font-weight:900;}}
.card-q{{font-size:104px;color:#FFD93D;-webkit-text-stroke:20px {INK};paint-order:stroke fill;letter-spacing:1px}}
.card-row{{display:flex;gap:40px}}
.opt{{width:420px;height:330px;border:8px solid {INK};border-radius:46px;box-shadow:0 18px 0 {INK};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-size:50px;line-height:1.12;text-align:center;color:{INK}}}
.optA{{background:#FFD93D}} .optB{{background:#4FC08D}}
.card-cta{{font-size:62px;color:#fff;-webkit-text-stroke:16px {INK};paint-order:stroke fill}}
.arw{{display:inline-block}}
#{p}-fade{{position:absolute;inset:0;background:#0A0818}}"""
    tc = wt(sc, "Continua")
    js = f"""
function frame(t){{
  T($('{p}-cam'), camT(lerp(0.95,1.0,ease(t/{sc['dur']})),540,1000));
  T($('{p}-clk'), `translate(${{Math.sin(t*60)*7}} 0) rotate(${{Math.sin(t*60)*1.5}})`); op($('{p}-clk-ring'),1);
  const d=$('{p}-dot'); d.setAttribute('r',(40+Math.sin(t*6)*8).toFixed(1)); T($('{p}-tag'), `translate(0 ${{Math.sin(t*5)*8}})`);
}}
tl.fromTo('#{p}-fade',{{opacity:1}},{{opacity:0,duration:0.5,ease:'power2.out'}},0);
tl.fromTo('#{p}-card',{{opacity:0,scale:0.6,y:40}},{{opacity:1,scale:1,y:0,duration:0.45,ease:'back.out(1.8)'}},{max(0.2, tc-0.1)});
tl.fromTo('#{p}-optA',{{rotation:-4}},{{rotation:4,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.6)}}},{max(0.2, tc-0.1)});
tl.fromTo('#{p}-optB',{{rotation:4}},{{rotation:-4,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.6)}}},{max(0.2, tc-0.1)});
tl.fromTo('#{p}-arw',{{y:-8}},{{y:14,duration:0.35,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.35)}}},{max(0.2, tc)});
"""
    return svg, js, html_extra, css

BUILDERS = {"s0": scene_bedroom_open, "s1": scene_oversize, "s2": scene_cat, "s3": scene_matchbox, "s4": scene_ant,
            "s5": scene_mite, "s6": scene_water, "s7": scene_virus, "s8": scene_atom, "s9": scene_void, "s10": scene_end}

SCENE_TPL = """<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}
    #root > svg {{ position: absolute; left: 0; top: 0; }}
    {css}
  </style>
  <div id="root" data-composition-id="{id}" data-width="1080" data-height="1920">
    <svg id="{id}-svg" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow>
      <g id="{id}-cam">
{svg}
      </g>
      <rect width="1080" height="1920" fill="url(#{id}-vig)"/>
      <defs><radialGradient id="{id}-vig" cx="0.5" cy="0.45" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.38"/></radialGradient></defs>
    </svg>
    {html}
  </div>
  <script>
{lib}
    const tl = gsap.timeline({{ paused: true }});
{js}
    const PX = {{ t: 0 }};
    tl.to(PX, {{ t: {dur}, duration: {dur}, ease: "none", onUpdate: () => frame(PX.t) }}, 0);
    frame(0);
    window.__timelines["{id}"] = tl;
  </script>
</template>
"""

def write_scene(sc):
    out = BUILDERS[sc["id"]](sc)
    if len(out) == 2: svg, js = out; html = css = ""
    else: svg, js, html, css = out
    if "tl." in js and "frame(" in js:
        pass
    # scene_end usa tl antes de declarar? -> js vem depois de const tl
    txt = SCENE_TPL.format(id=sc["id"], svg=svg, js=js, lib=JS_LIB + JS_PUFF, dur=sc["dur"], html=html, css=css)
    with open(os.path.join(ROOT, "compositions", sc["id"] + ".html"), "w") as f: f.write(txt)

# ------------------------------------------------------------------ legendas
def write_captions():
    items, tw = [], []
    for sc in SCENES:
        for a, b, txt in sc["chunks"]:
            a2, b2 = sc["start"]+a, sc["start"]+b
            i = len(items)
            items.append(f'<div id="cap-{i}" class="clip cap" data-start="{a2:.3f}" data-duration="{b2-a2:.3f}"><span id="capw-{i}" class="w">{txt}</span></div>')
            tw.append(f'tl.fromTo("#capw-{i}",{{scale:1.22}},{{scale:1,duration:0.12,ease:"back.out(2.4)"}},{a2:.3f});')
    html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; top: 1110px; width: 100%; text-align: center; overflow: visible; }}
    .w {{ display: inline-block; font-family: Nunito; font-weight: 900; font-size: 86px; line-height: 1.1; color: #FFFFFF;
          -webkit-text-stroke: 18px {INK}; paint-order: stroke fill; letter-spacing: 0.5px; }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
    {chr(10).join(items)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join(tw)}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["legendas"] = tl;
  </script>
</template>
"""
    with open(os.path.join(ROOT, "compositions", "legendas.html"), "w") as f: f.write(html)

# ------------------------------------------------------------------ transição: folhas de calendário
def write_calendar():
    rr = random.Random(7); pages = []
    for i in range(13):
        ang = rr.uniform(0, 2*math.pi)
        pages.append([round(W/2+rr.uniform(-260, 260)), round(H*0.42+rr.uniform(-380, 380)), round(math.cos(ang)*rr.uniform(1300, 2200)),
                      round(math.sin(ang)*rr.uniform(1300, 2200)-300), round(rr.uniform(-1, 1), 2), round(rr.uniform(-5, 5), 2), round(rr.uniform(0.9, 1.35), 2)])
    cuts = [[sc["start"], sc["day"]] for sc in SCENES if sc.get("day")]
    svg = "\n".join(calendar_page_svg(f"pg{i}", "pgday" if i == 0 else None) for i in range(13))
    html = f"""<template>
  <style>#root {{ position: absolute; inset: 0; pointer-events: none; }} #root svg {{ position:absolute; left:0; top:0; }}</style>
  <div id="root" data-composition-id="calendario" data-width="1080" data-height="1920">
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow>
{svg}
    </svg>
  </div>
  <script>
    const PG={json.dumps(pages)}, CUTS={json.dumps(cuts)};
    function frame(t){{
      let cut=null; for(const c of CUTS){{ if(t-c[0]>-0.26 && t-c[0]<0.85) cut=c; }}
      for(let i=0;i<PG.length;i++){{
        const e=document.getElementById('pg'+i);
        if(!cut){{ e.setAttribute('opacity',0); continue; }}
        const u=t-cut[0], p=PG[i], k=u<0?0.6:1;
        const x=p[0]+p[2]*u*k, y=p[1]+p[3]*u*k+(u>0?600*u*u:0);
        e.setAttribute('opacity',1);
        e.setAttribute('transform',`translate(${{x.toFixed(1)}} ${{y.toFixed(1)}}) rotate(${{((p[4]+p[5]*u)*57.3).toFixed(1)}}) scale(${{p[6]}})`);
      }}
      if(cut) document.getElementById('pgday').textContent=cut[1];
    }}
    const tl = gsap.timeline({{ paused: true }});
    const PX={{t:0}};
    tl.to(PX,{{t:{TOTAL},duration:{TOTAL},ease:"none",onUpdate:()=>frame(PX.t)}},0);
    frame(0);
    window.__timelines["calendario"] = tl;
  </script>
</template>
"""
    with open(os.path.join(ROOT, "compositions", "calendario.html"), "w") as f: f.write(html)

def write_index():
    hosts = []
    for sc in SCENES:
        hosts.append(f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" data-start="{sc["start"]:.3f}" '
                     f'data-duration="{sc["dur"]:.3f}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:1"></div>')
    html = f"""<!doctype html>
<html lang="pt-BR" data-composition-variables='[{{"id":"color-ink","type":"color","label":"Contorno","default":"{INK}"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/lib/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="calendario" data-composition-id="calendario" data-composition-src="compositions/calendario.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:3"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w") as f: f.write(html)

def write_narration():
    def m(x): return f"{int(x//60)}:{x % 60:04.1f}"
    lines = ["E SE VOCÊ ENCOLHESSE PELA METADE TODO DIA? — narração (≈%.0fs)" % TOTAL, ""]
    for sc in SCENES: lines.append(f"[{m(sc['start']+sc['chunks'][0][0])}] {sc['text']}")
    with open(os.path.join(ROOT, "narracao.txt"), "w") as f: f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    import sys
    if "--2d" in sys.argv:   # versão 2D antiga (cenas em SVG)
        for sc in SCENES: write_scene(sc)
        write_index()
    write_captions(); write_calendar(); write_narration()
    os.replace(os.path.join(ROOT, "narracao.txt"), os.path.join(os.path.dirname(ROOT), "narracao.txt"))
    print("total", TOTAL, [(s["id"], s["start"], s["dur"]) for s in SCENES])
