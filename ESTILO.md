# Guia de estilo do canal "E SE…"

Medido quadro a quadro no vídeo de referência "E se você fosse imortal" (70,6 s, 1080x1920, 30 fps, 2119 quadros),
com fluxo óptico (OpenCV) em cada par de quadros e leitura da legenda quadro a quadro.
**Use este guia em todo episódio novo.** A câmera está implementada em `blender/camera.py`.

## 1. Formato
| | |
|---|---|
| Quadro | 1080x1920 (9:16), 30 fps |
| Duração | 60–70 s; ~3 palavras por segundo de narração, sem respiro entre cenas |
| Cortes secos | quase nenhum: em 70 s só houve **3**. Todo o resto é movimento de câmera contínuo |
| Cenas | ~11 "lugares" e ~25 batidas de câmera (uma batida a cada 2–3 s) |

## 2. Câmera (o mais importante)
A câmera **nunca fica parada**. Três estados:

**HOLD (entre batidas):** zoom lento para dentro, contínuo, de **4 a 10% de escala por segundo** (mediana ≈ 6%/s).
Quase nenhum pan (< 5 px/s) e rotação < 0,3°/s: é um "respirar" de câmera, não um balanço.
→ `Shot(..., push=0.06)`

**WHIP (troca de batida):** a cada frase ou ideia nova, um movimento rápido de **0,25–0,4 s**:
- zoom forte para fora *ou* para dentro (picos de 60–200% de escala/s),
- pan de 300–1200 px/s na direção do próximo assunto,
- um "tranco" de rotação de **3–10°** que volta a zero,
- desfoque de movimento forte (a imagem borra — é ele que esconde as trocas de cenário),
- aceleração e freio fortes (curva quíntica), nada linear.
→ `Shot(t, cx, cz, h, roll=±5)` (padrão `kind="whip"`). O whip **termina** no tempo `t` da batida.

**IMPACTO:** em pancadas (raio na referência, piano aqui), tremida curta que decai em ~0,4 s, às vezes com
um flash branco de 1–2 quadros. → `Shot(..., kind="cut", shake=0.07)` ou `rig.impact(t)`.

**Troca de cenário:** acontece *dentro* de um whip: a cena A sai girando/afastando (`exit`) e a cena B entra
terminando o mesmo movimento (`enter`). Em saltos grandes de tempo (100 anos, 1 bilhão de anos) entram as
**folhas de calendário** voando por cima, no mesmo instante. Só uma vez a referência usa fusão (dissolve de ~0,5 s).

### Enquadramento (quadro vertical)
| Plano | Uso | Altura do quadro `h` com o Léo (2,0 de altura) |
|---|---|---|
| Aberto | começo de cena, mostrar o lugar | 5–8 |
| Corpo inteiro | ação | 3–4 |
| Médio | fala, reação leve | 2,4–3 |
| Close | **toda reação forte** (choque, tristeza, piada) | 1,8–2,1 (cabeça ocupa ~70% da largura) |

- Personagem centralizado na horizontal; elementos grandes (sol, buracos negros, foto, prédio) **em cima**,
  personagem **embaixo**. Nada lado a lado.
- A legenda fica sobre o peito/barriga do personagem — não tem problema, a referência faz igual.
- Close nas reações: a referência sempre corta (whip) para o rosto na palavra que carrega a emoção.

## 3. Legenda
- **Uma palavra por vez** (palavras curtas como "de", "o", "a" grudam na seguinte: "do céu", "a última").
- Centro em **y ≈ 1360 px (71% da altura)**, centralizada na horizontal.
- Fonte arredondada bem grossa (Nunito 900), ~96 px, **branca com contorno escuro** e uma sombra curta embaixo.
- Entra com um "pop" (escala 1,18 → 1 em 0,1 s). Troca no ritmo exato da fala.

## 4. Roteiro (estrutura que funciona)
1. **Gancho (0–3 s):** "E se você…" + uma pancada visual absurda logo no primeiro segundo (raio, piano).
2. **Lado bom (3–15 s):** o personagem curtindo a ideia (séries, jogos, livros, viagens).
3. **Escalada de tempo (15–55 s):** cada cena é um salto maior ("100 anos depois", "1 bilhão de anos depois"…),
   cada uma com um fato real + uma piadinha curta no fim da frase.
4. **Fim do mundo / clímax (55–65 s):** o extremo do tema (o universo apagando).
5. **Piada final + escolha:** fecha com humor e, pela regra do canal, pausa com duas opções e "comenta aí".

Frases curtas, sujeito "você", verbo no presente. Uma imagem por frase.

## 5. Personagem e cenário
- Personagem central grande, corpo-pílula, membros finos, cabeça grande, expressões simples
  (olho ponto, olho fechado feliz, olho arregalado, espiral de tontura, boca em onda).
- Expressão muda a cada batida — nunca a mesma cara por mais de ~3 s.
- Acessórios cômicos que mudam com a cena (pipoca, chapéu de festa, lanterna, protetor solar).
- Cores chapadas e quentes, contorno escuro, sombra suave.

## 6. Checklist de um episódio novo
1. Copie `episodios/imortal/` para `episodios/<tema>/` e reescreva `SCENES` em `roteiro.py`.
2. `python3 episodios/<tema>/roteiro.py` (gera legendas, calendário, card e `narracao.txt`).
3. Monte as cenas em `cenas.py` com `Rig` + `Shot` (uma batida por frase; close nas reações).
4. Gere stills e confira o enquadramento: `python3 episodios/<tema>/render.py -- s3 still 0.1,0.5,0.9`.
5. `episodios/<tema>/render_todas.sh` e depois `episodios/<tema>/montar.sh`.

## 7. Os 5 primeiros segundos (gancho) — vale para toda série
Quem decide se assiste é o primeiro segundo. Regras:
1. **Primeiro quadro já é a cena mais forte**: rosto em choque + o objeto/absurdo no mesmo quadro (vira a miniatura).
   Nada de abertura, logo ou plano vazio. A câmera já começa com tremida/zoom (impacto em t=0).
2. **Frase 1 = afirmação surpreendente sobre algo comum** ("Seu micro-ondas esquenta comida sem fogo nenhum").
   **Frase 2 = pergunta curta** ("Sabe como?"). **Frase 3 = promessa da resposta** ("O segredo tá na água").
3. **4 batidas de câmera em 5 s** (uma a cada ~1,2 s): rosto → objeto → close → mergulho no "segredo".
4. **Selo gigante no topo** com a ideia do gancho ("SEM FOGO?!"), vermelho, entra como carimbo e treme.
5. Narração começa em 0,1 s — sem respiro antes da primeira palavra.

## 8. Série "Como funciona" (objetos do dia a dia)
- Mesma câmera e legenda do "E se…". Apresentador: o Léo.
- Linguagem de conversa: frases curtas, palavras do dia a dia, uma comparação caseira por passo
  ("tipo as do wi-fi", "igual esfregar as mãos no frio"). Termo técnico só um por vídeo, e explicado na hora.
- Estrutura: gancho (5 s) → 3–4 passos numerados com selo no topo ("1 · MAGNETRON") → por que isso importa
  no seu dia → escolha do próximo objeto nos comentários.
- Modelo: `episodios/microondas/`.
