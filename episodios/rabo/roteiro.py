"""E SE você acordasse com um rabo? — roteiro, tempos e camadas do HyperFrames (legendas, calendário, card de escolha).

Fonte única do texto e dos tempos. Rode:  python3 episodios/rabo/roteiro.py
Gera: episodios/rabo/hyperframes/{index.html, compositions/*.html} e episodios/rabo/narracao.txt
"""
import json, math, os, random, sys

EP = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(EP))
sys.path.insert(0, os.path.join(REPO, "hyperframes", "build"))
import build as _B                       # reaproveita o relógio de palavras e o desenho da folha de calendário
from build import calendar_page_svg, INK

TITULO = "E SE VOCÊ ACORDASSE COM UM RABO?"
W, H = 1080, 1920

# jump = texto da folha de calendário que voa na entrada da cena (salto de tempo)
SCENES = [
    dict(id="s0", text="E se você acordasse com um rabo? Ele aparece do nada, bem no meio da noite."),
    dict(id="s1", text="No começo, é fofo. Ele balança sozinho toda vez que você fica feliz."),
    dict(id="s2", text="Mas na escola, todo mundo descobre de quem você gosta. O rabo não sabe mentir."),
    dict(id="s3", text="No ônibus, a porta fecha bem em cima dele. O ônibus inteiro ouve o seu grito."),
    dict(id="s4", text="Pelo menos no futebol, você vira lenda. O primeiro gol de rabo da história."),
    dict(id="s5", text="Rabo de gato ou de cachorro? Comenta aí.", hold=2.0),
]

# ritmo da referência: ~3 palavras/s, narração emendada de uma cena na outra (quase sem respiro)
RATE = 0.84
_wd = _B.word_dur
_B.word_dur = lambda w: _wd(w) * RATE
_B.LEAD, _B.TAIL = 0.12, 0.22
for sc in SCENES:
    sc["chunks"], sc["dur"] = _B.timeline(sc)
T0 = 0
for sc in SCENES:
    sc["start"] = round(T0, 3); T0 += sc["dur"]
TOTAL = round(T0, 3)

def wt(sc, needle, end=False):
    """início (ou fim) do primeiro trecho de legenda que contém needle"""
    for a, b, txt in sc["chunks"]:
        if needle.lower() in txt.lower(): return b if end else a
    raise KeyError(needle)

HF = os.path.join(EP, "hyperframes")

# ------------------------------------------------------------------ legendas (1 palavra por vez, como a referência)
CAP_Y = 1255          # centro em ~1315 px. A referência usa ~1360 (71%); subimos um pouco para fugir dos botões do TikTok/Shorts
def write_captions():
    items, tw = [], []
    for sc in SCENES:
        for a, b, txt in sc["chunks"]:
            a2, b2 = sc["start"]+a, sc["start"]+b
            i = len(items)
            items.append(f'<div id="cap-{i}" class="clip cap" data-layout-allow-safe-zone data-start="{a2:.3f}" data-duration="{b2-a2:.3f}"><span id="capw-{i}" class="w">{txt}</span></div>')
            tw.append(f'tl.fromTo("#capw-{i}",{{scale:1.18}},{{scale:1,duration:0.1,ease:"back.out(2.2)"}},{a2:.3f});')
    html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; top: {CAP_Y}px; width: 100%; text-align: center; overflow: visible; }}
    .w {{ display: inline-block; font-family: Nunito; font-weight: 900; font-size: 96px; line-height: 1.1; color: #FFFFFF;
          -webkit-text-stroke: 16px {INK}; paint-order: stroke fill; letter-spacing: 1px;
          filter: drop-shadow(0 6px 0 rgba(0,0,0,0.35)); }}
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
    open(os.path.join(HF, "compositions", "legendas.html"), "w").write(html)

# ------------------------------------------------------------------ folhas de calendário nos saltos de tempo
def write_calendar():
    """Na referência as folhas entram pelo canto de cima e atravessam a tela girando, ~0,9 s,
    exatamente no whip de troca de cena. Aqui: 9 folhas, saindo de cima à esquerda para baixo à direita."""
    rr = random.Random(11); pages = []
    for i in range(9):
        pages.append([round(rr.uniform(-200, 700)), round(rr.uniform(-420, -120)),       # início
                      round(rr.uniform(900, 1500)), round(rr.uniform(1100, 1700)),       # deslocamento total
                      round(rr.uniform(-0.6, 0.6), 2), round(rr.uniform(-4, 4), 2),      # rotação inicial, giro
                      round(rr.uniform(0.95, 1.4), 2), round(i*0.045, 3)])               # escala, atraso
    cuts = [sc["start"] - 0.18 for sc in SCENES if sc.get("jump")]
    svg = "\n".join(calendar_page_svg(f"pg{i}") for i in range(9))
    html = f"""<template>
  <style>#root {{ position: absolute; inset: 0; pointer-events: none; }} #root svg {{ position:absolute; left:0; top:0; }}</style>
  <div id="root" data-composition-id="calendario" data-width="1080" data-height="1920">
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow>
{svg}
    </svg>
  </div>
  <script>
    const PG={json.dumps(pages)}, CUTS={json.dumps([round(c, 3) for c in cuts])}, D=0.95;
    function frame(t){{
      let c0=null; for(const c of CUTS){{ if(t>=c && t<c+D+0.4) c0=c; }}
      for(let i=0;i<PG.length;i++){{
        const e=document.getElementById('pg'+i), p=PG[i];
        if(c0===null){{ e.setAttribute('opacity',0); continue; }}
        const u=(t-c0-p[7])/D;
        if(u<0||u>1){{ e.setAttribute('opacity',0); continue; }}
        const k=1-Math.pow(1-u,2);
        const x=p[0]+p[2]*k, y=p[1]+p[3]*k;
        e.setAttribute('opacity',1);
        e.setAttribute('transform',`translate(${{x.toFixed(1)}} ${{y.toFixed(1)}}) rotate(${{((p[4]+p[5]*u)*57.3).toFixed(1)}}) scale(${{p[6]}})`);
      }}
    }}
    const tl = gsap.timeline({{ paused: true }});
    const PX={{t:0}};
    tl.to(PX,{{t:{TOTAL},duration:{TOTAL},ease:"none",onUpdate:()=>frame(PX.t)}},0);
    frame(0);
    window.__timelines["calendario"] = tl;
  </script>
</template>
"""
    open(os.path.join(HF, "compositions", "calendario.html"), "w").write(html)

# ------------------------------------------------------------------ card de escolha (regra do canal)
def write_final():
    sc = SCENES[-1]; tc = wt(sc, "gato")
    html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; font-family: Nunito; font-weight: 900; }}
    #card {{ position:absolute; left:0; top:250px; width:100%; display:flex; flex-direction:column; align-items:center; gap:34px; }}
    .q {{ font-size:96px; color:#FFD93D; -webkit-text-stroke:18px {INK}; paint-order:stroke fill; text-align:center; line-height:1.05 }}
    .row {{ display:flex; gap:40px }}
    .opt {{ width:420px; height:300px; border:8px solid {INK}; border-radius:46px; box-shadow:0 18px 0 {INK};
            display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;
            font-size:54px; line-height:1.1; text-align:center; color:{INK} }}
    .big {{ font-size:110px; line-height:1 }}
    .a {{ background:#FFD93D }} .b {{ background:#7FB2FF }}
    .cta {{ font-size:62px; color:#fff; -webkit-text-stroke:16px {INK}; paint-order:stroke fill }}
    .arw {{ display:inline-block }}
  </style>
  <div id="root" data-composition-id="final" data-width="1080" data-height="1920">
    <div id="card">
      <div class="q">QUAL RABO<br>VOCÊ QUERIA?</div>
      <div class="row">
        <div id="optA" class="opt a"><span class="big">🐱</span><span>DE GATO</span></div>
        <div id="optB" class="opt b"><span class="big">🐶</span><span>DE CACHORRO</span></div>
      </div>
      <div class="cta">COMENTA AÍ <span id="arw" class="arw">▼</span></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo('#card',{{opacity:0,scale:0.6,y:40}},{{opacity:1,scale:1,y:0,duration:0.45,ease:'back.out(1.8)'}},{max(0.15, tc-0.35):.3f});
    tl.fromTo('#optA',{{rotation:-4}},{{rotation:4,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.6)}}},{max(0.15, tc-0.35):.3f});
    tl.fromTo('#optB',{{rotation:4}},{{rotation:-4,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.6)}}},{max(0.15, tc-0.35):.3f});
    tl.fromTo('#arw',{{y:-8}},{{y:14,duration:0.35,ease:'sine.inOut',yoyo:true,repeat:{int(sc['dur']/0.35)}}},{tc:.3f});
    tl.set({{}}, {{}}, {sc['dur']});
    window.__timelines["final"] = tl;
  </script>
</template>
"""
    open(os.path.join(HF, "compositions", "final.html"), "w").write(html)

def write_index():
    s10 = SCENES[-1]
    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/lib/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
<video id="blender" class="clip" src="assets/video/blender.mp4" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="0" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;z-index:1"></video>
<div id="calendario" data-composition-id="calendario" data-composition-src="compositions/calendario.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>
<div id="final" data-composition-id="final" data-composition-src="compositions/final.html" data-start="{s10['start']:.3f}" data-duration="{s10['dur']:.3f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:3"></div>
<div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:4"></div>
</div><script>window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>
"""
    open(os.path.join(HF, "index.html"), "w").write(html)

def write_narration():
    def m(x): return f"{int(x//60)}:{x % 60:04.1f}"
    lines = [f"{TITULO} — narração (≈{TOTAL:.0f}s)", "",
             "Cada linha começa no tempo indicado. A legenda na tela mostra 1 palavra por vez nesse ritmo.", ""]
    for sc in SCENES: lines.append(f"[{m(sc['start']+sc['chunks'][0][0])}] {sc['text']}")
    open(os.path.join(EP, "narracao.txt"), "w").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    os.makedirs(os.path.join(HF, "compositions"), exist_ok=True)
    write_captions(); write_calendar(); write_final(); write_index(); write_narration()
    print("total", TOTAL)
    for s in SCENES: print(f"  {s['id']:4s} início {s['start']:6.2f}  dur {s['dur']:5.2f}")
