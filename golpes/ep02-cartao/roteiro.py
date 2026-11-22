"""Roteiro e tempos do episódio 2: CARTÃO CLONADO (30 s, gancho forte no início).

Fonte única do texto, dos tempos de cada palavra e dos gráficos de cada plano.
Rode `python3 golpes/ep01-piramide/roteiro.py` para gerar `narracao.txt`.

Cada plano (SHOT):
  id      nome da cena em cenas.py
  text    fala do plano (vira legenda, 2 palavras por vez, palavra falada em amarelo)
  title   título de capítulo no topo: (texto, palavra em que entra)
  cap     altura da legenda (fração da tela; padrão 0.66)
  pills   etiquetas "• NOME": (texto, objeto 3D que ela segue, palavra em que entra, cor do ponto)
  x       palavra em que aparece o X vermelho (plano que deu errado)
  big     números grandes: (texto, palavra, cor, y)  cor: "g" verde, "r" vermelho, "w" branco
  whip    True = entra com chicote (desfoque) em vez de corte seco
"""
import os

FPS = 30
W, H = 1080, 1920

SHOTS = [
    # ---------------------------------------------------------------- GANCHO (0–3 s)
    dict(id="c01", text="Ele clonou o seu cartão em três segundos. E você nem viu.",
         big=[("3 SEGUNDOS", "três", "r", 0.16)], cap=0.86),
    # ---------------------------------------------------------------- COMO O GOLPE FUNCIONA
    dict(id="c02", text="Primeiro, ele cola um chupa-cabra no caixa eletrônico.",
         title=("CHUPA-CABRA", "chupa-cabra"), pills=[("LEITOR FALSO", "skim", "caixa", "#E74C3C")], whip=True),
    dict(id="c03", text="Você passa o cartão, e a tarja magnética é copiada.",
         pills=[("TARJA COPIADA", "atm", "copiada.", "#E74C3C")]),
    dict(id="c04", text="Uma câmera escondida filma a sua senha.",
         pills=[("CÂMERA ESCONDIDA", "spycam", "câmera", "#E74C3C")], cap=0.86),
    dict(id="c05", text="Aí ele grava tudo num cartão em branco,",
         title=("CARTÃO\nCLONADO", "branco,"), cap=0.86, whip=True),
    dict(id="c06", text="e faz compras e saques no seu nome.",
         big=[("– R$ 4.800", "saques", "r", 0.17)], pills=[("SEU NOME", "hero", "nome.", "#E74C3C")]),
    # ---------------------------------------------------------------- VIRADA + PROTEÇÃO
    dict(id="c07", text="Só que o chip e a aproximação são bem mais difíceis de copiar.",
         title=("CHIP", "chip"), x="copiar.", cap=0.86),
    dict(id="c08", text="Então cubra a senha, prefira o chip e ative o alerta de compras no app.",
         pills=[("COBRE A SENHA", "hand", "cubra", "#27AE60"), ("ALERTA LIGADO", "phone", "alerta", "#27AE60")], whip=True),
    dict(id="c09", text="Viu compra estranha? Bloqueie na hora e conteste no banco.",
         big=[("BLOQUEIE", "Bloqueie", "g", 0.17)], cap=0.86),
    dict(id="c10", text="Você já teve o cartão clonado? Comenta aí.",
         pills=[("COMENTA AQUI", "card", "Comenta", "#27AE60")], cap=0.86, hold=0.6),
]

LEAD, TAIL = 0.08, 0.12

def word_dur(w):
    core = w.strip(".,?!:")
    d = max(0.19, min(0.48, 0.11 + 0.028 * len(core)))
    if core.isdigit() and len(core) == 4: d = 0.75          # ano: "dois mil e treze"
    if w[-1] in ".?!": d += 0.18
    elif w[-1] in ",:": d += 0.1
    return d

def timeline(sh):
    words = sh["text"].split()
    t, out = LEAD, []
    for w in words:
        d = word_dur(w); out.append((round(t, 3), round(t + d, 3), w)); t += d
    return out, round(t + TAIL + sh.get("hold", 0), 3)

T = 0.0
for sh in SHOTS:
    sh["words"], sh["dur"] = timeline(sh)
    sh["start"] = round(T, 3)
    sh["frames"] = int(round(sh["dur"] * FPS))
    T += sh["frames"] / FPS
TOTAL = round(T, 3)

def wt(sh, needle):
    """Tempo (s, relativo ao plano) em que a palavra `needle` começa."""
    for a, b, w in sh["words"]:
        if w.lower().strip(".,?!:") == needle.lower().strip(".,?!:"): return a
    for a, b, w in sh["words"]:
        if needle.lower() in w.lower(): return a
    raise KeyError(f"{sh['id']}: {needle}")

def shot(sid): return next(s for s in SHOTS if s["id"] == sid)

def captions(sh):
    """Grupos de 2 palavras: [(ini, fim, [(palavra, ini, fim), ...])]."""
    ws, groups = sh["words"], []
    for i in range(0, len(ws), 2):
        g = ws[i:i + 2]
        groups.append((g[0][0], g[-1][1], g))
    return groups

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    lines = ["CARTÃO CLONADO — narração (≈%.0fs). Tempos do início de cada plano." % TOTAL, ""]
    for sh in SHOTS:
        lines.append(f"[{int(sh['start']//60)}:{sh['start']%60:04.1f}] {sh['text']}")
    open(os.path.join(here, "narracao.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("planos:", len(SHOTS), "total:", TOTAL)
