"""Comercial 3D: FEIJÃO GERENTE FICOU LOUCO (vertical 9:16, ~36 s, sem voz).

Fonte única do texto, dos tempos de cada palavra e dos gráficos de cada plano.
Rode `python3 golpes/com01-feijao/roteiro.py` para gerar `narracao.txt` (falas do gerente).

PRODUTO: dados comerciais editáveis. Deixe "" para não aparecer na tela (nada é inventado).
Cada plano (SHOT): id, text (fala; "" = plano sem fala), dur (só para planos sem fala),
title, big, pills, cap, whip — mesmos campos dos episódios da série de golpes.
Nos campos de tempo, a "palavra" também pode ser um número (segundos dentro do plano).
"""
import os

FPS = 30
W, H = 1080, 1920

PRODUTO = {
    "marca": "GERENTE FICOU LOUCO",
    "produto": "FEIJÃO",
    "peso": "",          # ex.: "1 kg"   — vazio = não aparece
    "preco": "",         # ex.: "R$ 0,00" — vazio = não aparece
}

SHOTS = [
    # ---------------------------------------------------------------- 1. A DISPUTA (abre de longe e entra no meio da confusão)
    dict(id="f01", text="", dur=4.2,
         big=[("CONFUSÃO NO MERCADO!", 1.0, "w", 0.15)], pills=[("FEIJÃO", "pack", 2.0, "#C62828")],
         sfx=[(0.2, "briga"), (1.2, "briga"), (2.2, "briga"), (3.2, "briga")]),
    # ---------------------------------------------------------------- 2. ENTRA O GERENTE
    dict(id="f02", text="Gerente Ficou Louco! Baixou o preço do melhor feijão da região e deixou ele quase de graça!",
         title=("GERENTE\nFICOU LOUCO", "Louco!"), big=[("QUASE DE GRAÇA!", "graça!", "g", 0.30)], whip=True),
    dict(id="f03", text="Todo mundo tá querendo, porque além de ser gostoso, tem uma qualidade excepcional!",
         big=[("QUALIDADE EXCEPCIONAL", "excepcional!", "g", 0.17)]),
    dict(id="f04", text="Grãos selecionados, sabor de verdade e um rendimento que enche a panela!",
         pills=[("GRÃOS SELECIONADOS", "b1", "Grãos", "#27AE60"), ("SABOR DE VERDADE", "b2", "sabor", "#E67E22"),
                ("ÓTIMO RENDIMENTO", "b3", "rendimento", "#2E86DE")], cap=0.86, whip=True),
    # ---------------------------------------------------------------- 3. OLHA A CONFUSÃO
    dict(id="f05", text="Olha só o que acontece quando o melhor feijão do mercado entra em promoção!",
         big=[("PROMOÇÃO!", "promoção!", "r", 0.17)], cap=0.86),
    dict(id="f06", text="", dur=2.4, big=[("?!", 0.3, "w", 0.2)],
         sfx=[(0.25, "buzz"), (0.95, "boing"), (1.05, "whoosh"), (1.45, "pop")]),
    # ---------------------------------------------------------------- 4. O GERENTE PEGA O PACOTE
    dict(id="f07", text="", dur=3.4, cap=0.86, sfx=[(1.3, "pop"), (1.7, "fanfare"), (1.7, "boom")]),
    # ---------------------------------------------------------------- 5. FINAL
    dict(id="f08", text="Finalmente! Consegui pegar o melhor feijão do mercado!", cap=0.86),
    dict(id="f09", text="", dur=6.0, packshot=True,
         title=("GERENTE\nFICOU LOUCO", 0.25),
         texts=[("Qualidade excepcional, sabor de verdade e preço de promoção!", 1.2, 0.78, "w"),
                ("Corra para o supermercado e aproveite!", 2.6, 0.91, "g")],
         sfx=[(0.0, "whoosh"), (0.25, "fanfare")]),
]

# preço só aparece se for preenchido em PRODUTO (nada é inventado)
if PRODUTO["preco"]:
    SHOTS[-1].setdefault("big", []).append((PRODUTO["preco"], 1.8, "r", 0.66))

LEAD, TAIL = 0.1, 0.18

def word_dur(w):
    core = w.strip(".,?!:")
    d = max(0.2, min(0.52, 0.12 + 0.03 * len(core)))
    if w[-1] in ".?!": d += 0.22
    elif w[-1] in ",:": d += 0.12
    return d

def timeline(sh):
    words = sh["text"].split()
    if not words: return [], sh["dur"]
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
    """Tempo (s, relativo ao plano) em que a palavra `needle` começa. Número = tempo direto."""
    if isinstance(needle, (int, float)): return float(needle)
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
    lines = ["FEIJÃO GERENTE FICOU LOUCO — falas do gerente (≈%.0fs de vídeo). Tempos do início de cada plano." % TOTAL, ""]
    for sh in SHOTS:
        if sh["text"]: lines.append(f"[{int(sh['start']//60)}:{sh['start']%60:04.1f}] {sh['text']}")
    open(os.path.join(here, "narracao.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("planos:", len(SHOTS), "total:", TOTAL)
