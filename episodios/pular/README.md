# E SE o mundo te pagasse pra pular?

Episódio no estilo **cartoon de palito noturno** (`referencias/estilo-cartoon-noturno/ESTILO.md`):
personagens de cabeça grande e membros finos, cidade à noite com chuva, neon, luz de poste e bokeh,
zoom lento em todo plano, legenda de 1-2 palavras e dinheiro verde saltando na tela.

- 1080x1920, 30 fps, ~146 s, **sem voz** (a narração com tempos está em `narracao.txt`)
- 10 cenas, 45 planos, tudo desenhado em código (SVG + GSAP no HyperFrames): dá para mudar qualquer coisa

## Como gerar

```bash
cd episodios/pular
python3 build/build.py                                   # gera compositions/, index.html e narracao.txt
npx --yes hyperframes@0.9.70 preview                     # abre o editor para ver
npx --yes hyperframes@0.9.70 render --quality looks -o ../../renders/E-se-o-mundo-te-pagasse-pra-pular.mp4
```

## Onde mexer

| O quê | Onde |
|---|---|
| Texto da narração e em que palavra cada plano começa | `SCENES` em `build/build.py` |
| Um plano (cenário, personagens, animação) | a função `sN_nome` em `build/build.py` |
| Personagens (Léo, Vó, Canguru, dono do circo…) | `LOOKS` e `person()` em `build/lib.py` |
| Cenários, neon, chuva, painel de ranking, celular, dinheiro | `build/lib.py` |
| Legenda (fonte, tamanho, posição) | `build_captions()` em `build/build.py` |

Os tempos das falas são estimados pelo tamanho das palavras. Depois de gravar a voz, ajuste o ritmo da fala
para os tempos de `narracao.txt`, ou mude `word_dur()` e gere de novo.
