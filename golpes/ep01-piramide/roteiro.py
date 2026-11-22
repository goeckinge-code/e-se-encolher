"""Roteiro e tempos do episódio 1: PIRÂMIDE FINANCEIRA.

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
    # ---------------------------------------------------------------- GANCHO
    dict(id="s01", text="Se você quer ficar rico sem vender nada,",
         pills=[("VOCÊ", "hero", "você", "#2E86DE")]),
    dict(id="s02", text="chama dez amigos e pede mil reais pra cada um.",
         pills=[("AMIGOS", "f2", "amigos", "#27AE60")], big=[("R$ 1.000", "mil", "g", 0.22)]),
    dict(id="s03", text="Só que eles perguntam: e eu ganho o quê?", x="quê?"),
    # ---------------------------------------------------------------- DEGRAU 1
    dict(id="s04", text="Então você promete dez por cento ao mês, garantido.",
         big=[("10% AO MÊS", "cento", "g", 0.2)]),
    dict(id="s05", text="Esse é o retorno garantido.", title=("RETORNO\nGARANTIDO", "retorno"), cap=0.86),
    # ---------------------------------------------------------------- DEGRAU 2
    dict(id="s06", text="Mas você não tem de onde tirar esse lucro.", x="lucro.",
         pills=[("COFRE", "safe", "tirar", "#7F8C8D")]),
    dict(id="s07", text="Então você paga os primeiros com o dinheiro de quem entrou depois.",
         pills=[("PRIMEIROS", "old", "primeiros", "#27AE60"), ("NOVOS", "new", "entrou", "#E67E22")], cap=0.86, whip=True),
    dict(id="s08", text="Esse é o esquema Ponzi.", title=("ESQUEMA\nPONZI", "esquema"), cap=0.86),
    # ---------------------------------------------------------------- DEGRAU 3
    dict(id="s09", text="Mas pra continuar pagando, você precisa de gente nova o tempo todo.", x="todo.",
         pills=[("FILA VAZIA", "queue", "gente", "#E74C3C")]),
    dict(id="s10", text="Então cada um ganha bônus pra trazer mais gente.",
         pills=[("BÔNUS", "bonus", "bônus", "#F1C40F")], cap=0.86),
    dict(id="s11", text="Essa é a pirâmide financeira.", title=("PIRÂMIDE\nFINANCEIRA", "pirâmide"), cap=0.88),
    # ---------------------------------------------------------------- DEGRAU 4
    dict(id="s12", text="Mas as pessoas começam a desconfiar.", x="desconfiar."),
    dict(id="s13", text="Então você posta carro importado, viagem e print de saque.",
         pills=[("ALUGADO", "car", "importado", "#E74C3C"), ("SAQUE: R$ 50 MIL", "phone", "saque.", "#27AE60")]),
    dict(id="s14", text="Essa é a prova social falsa.", title=("PROVA\nSOCIAL FALSA", "prova"), cap=0.86),
    # ---------------------------------------------------------------- DEGRAU 5
    dict(id="s15", text="Mas a polícia pergunta: o que a empresa vende?", x="vende?",
         pills=[("POLÍCIA", "cop", "polícia", "#34495E")]),
    dict(id="s16", text="Então você inventa um produto: criptomoeda, curso, até avestruz.",
         pills=[("CRIPTO", "coin", "criptomoeda", "#F39C12"), ("CURSO", "book", "curso", "#8E44AD"),
                ("AVESTRUZ", "ostrich", "avestruz.", "#E67E22")], cap=0.86),
    dict(id="s17", text="Esse é o produto de fachada.", title=("PRODUTO\nDE FACHADA", "produto"), cap=0.86),
    # ---------------------------------------------------------------- VIRADA
    dict(id="s18", text="Até que a conta não fecha. Se cada um traz dez, no décimo nível você precisa de dez bilhões de pessoas.",
         big=[("10 BILHÕES", "bilhões", "r", 0.2)], cap=0.88, count=("traz", "bilhões")),
    dict(id="s19", text="O planeta inteiro tem oito.", big=[("PLANETA: 8 BILHÕES", "planeta", "w", 0.2)], cap=0.88),
    dict(id="s20", text="Os novos param de entrar, os saques travam e o site sai do ar.",
         pills=[("SAQUE BLOQUEADO", "laptop", "saques", "#E74C3C")], whip=True),
    dict(id="s21", text="Quem entrou por último perde tudo.", big=[("– TUDO", "perde", "r", 0.2)], cap=0.88),
    # ---------------------------------------------------------------- IRONIA + FATO REAL
    dict(id="s22", text="Parabéns, você montou uma pirâmide financeira.", title=("PIRÂMIDE\nFINANCEIRA", "pirâmide"), cap=0.88),
    dict(id="s23", text="E no Brasil isso é crime contra a economia popular.",
         title=("CRIME", "crime"), cap=0.86),
    dict(id="s24", text="A TelexFree atraiu cerca de um milhão de brasileiros, até a Justiça bloquear tudo em 2013.",
         big=[("~1 MILHÃO", "milhão", "w", 0.2), ("BLOQUEADO", "bloquear", "r", 0.32)], cap=0.88),
    # ---------------------------------------------------------------- REGRA + PERGUNTA
    dict(id="s25", text="Regra simples: se o lucro vem de quem entra depois, é pirâmide.", cap=0.86),
    dict(id="s26", text="Te prometeram lucro garantido pra chamar amigo. Você entraria? Comenta aqui embaixo.",
         pills=[("COMENTA AQUI", "card", "comenta", "#27AE60")], cap=0.86, hold=1.2),
]

LEAD, TAIL = 0.08, 0.12

def word_dur(w):
    core = w.strip(".,?!:")
    d = max(0.2, min(0.52, 0.12 + 0.03 * len(core)))
    if core.isdigit() and len(core) == 4: d = 0.75          # ano: "dois mil e treze"
    if w[-1] in ".?!": d += 0.22
    elif w[-1] in ",:": d += 0.12
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
