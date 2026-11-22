"""Roteiro e tempos do episódio 1: PIRÂMIDE FINANCEIRA (versão de 30 s, gancho forte no início).

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
    # ---------------------------------------------------------------- GANCHO (0–4 s): imagem forte + promessa
    dict(id="s01", text="Esse golpe pegou um milhão de brasileiros. E você vai montar ele agora.",
         big=[("1 MILHÃO", "milhão", "g", 0.16)], pills=[("VOCÊ", "hero", "você", "#2E86DE")], cap=0.86),
    # ---------------------------------------------------------------- O GOLPE EM 4 PASSOS
    dict(id="s04", text="Você promete dez por cento ao mês, garantido.",
         big=[("10% AO MÊS", "cento", "g", 0.17)]),
    dict(id="s07", text="Mas paga os primeiros com o dinheiro de quem entrou depois.",
         title=("ESQUEMA\nPONZI", "dinheiro"), cap=0.86, whip=True,
         pills=[("NOVOS", "new", "entrou", "#E67E22")]),
    dict(id="s10", text="E dá bônus pra cada um trazer mais gente.",
         title=("PIRÂMIDE", "bônus"), pills=[("BÔNUS", "bonus", "trazer", "#F1C40F")], cap=0.88),
    dict(id="s13", text="Aí posta carro importado pra ninguém desconfiar.",
         pills=[("ALUGADO", "car", "importado", "#E74C3C")], whip=True),
    # ---------------------------------------------------------------- A CONTA NÃO FECHA
    dict(id="s18", text="Só que a conta não fecha: no décimo nível, você precisa de dez bilhões de pessoas.",
         big=[("10 BILHÕES", "bilhões", "r", 0.17)], cap=0.88, count=("décimo", "bilhões")),
    dict(id="s19", text="O planeta tem oito.", big=[("PLANETA: 8 BI", "planeta", "w", 0.17)], cap=0.88),
    dict(id="s20", text="Os saques travam,", pills=[("SAQUE BLOQUEADO", "laptop", "saques", "#E74C3C")], whip=True),
    dict(id="s21", text="e quem entrou por último perde tudo.", big=[("– TUDO", "perde", "r", 0.17)], cap=0.88),
    # ---------------------------------------------------------------- FATO REAL + PERGUNTA
    dict(id="s24", text="A TelexFree fez isso até a Justiça bloquear tudo, em 2013.",
         big=[("TELEXFREE", "TelexFree", "w", 0.15), ("BLOQUEADO", "bloquear", "r", 0.25)], cap=0.88),
    dict(id="s26", text="Lucro garantido pra chamar amigo. Você entraria? Comenta aí.",
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
    lines = ["PIRÂMIDE FINANCEIRA — narração (≈%.0fs). Tempos do início de cada plano." % TOTAL, ""]
    for sh in SHOTS:
        lines.append(f"[{int(sh['start']//60)}:{sh['start']%60:04.1f}] {sh['text']}")
    open(os.path.join(here, "narracao.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("planos:", len(SHOTS), "total:", TOTAL)
