# Série "Golpes da vida real" — explicados de um jeito simples

Animação vertical de **30 segundos** (9:16, 1080x1920, 30 fps) no estilo de bonecos de blocos: o espectador é colocado no lugar do
golpista ("Se **você** quer ficar rico…") e o golpe é montado degrau por degrau:

```
GANCHO forte nos 3 primeiros segundos (flash + câmera recuando + número-choque) em 2ª pessoa
DEGRAUS:  "Mas <obstáculo>."  →  "Então você <solução>."  →  "Esse é o <NOME>."  (título no topo)
VIRADA:   "Até que…"  (a conta não fecha / a polícia chega)
FATO REAL: lei + caso brasileiro de verdade
REGRA simples para reconhecer o golpe + PERGUNTA + "comenta aqui embaixo"
```

Protagonista fixo: terno cinza-grafite, gravata vermelha, cabelo castanho curto (`kit.hero`).
Guia de estilo: [`../referencias/ESTILO.md`](../referencias/ESTILO.md).

## Episódios

| # | Tema | Pasta |
|---|---|---|
| 1 | Pirâmide financeira (30 s) | [`ep01-piramide/`](ep01-piramide/) — vídeo em `video/Piramide-Financeira-30s.mp4`, narração em `narracao.txt` |
| 2 | Cartão clonado (30 s) | [`ep02-cartao/`](ep02-cartao/) — vídeo em `video/Cartao-Clonado-30s.mp4`, narração em `narracao.txt` |

## Como gerar

Precisa de: Python 3 com o módulo do Blender (`pip install bpy`, Python 3.11) ou o Blender instalado,
Pillow, numpy e ffmpeg. No Linux sem tela, também `libegl1 libgl1-mesa-dri`.

```bash
python3 golpes/ep01-piramide/roteiro.py                 # tempos + narracao.txt
PY=python3 golpes/scripts/render_ep.sh ep01-piramide   # quadros 3D (Workbench) → golpes/renders/ep01-piramide/frames
python3 golpes/montar.py ep01-piramide                  # legendas, títulos, etiquetas, sons → .mp4
```

Teste rápido de um plano: `python3 golpes/blender/render.py -- ep01-piramide s07 still 0.2,0.8`
e da camada de gráficos: `python3 golpes/montar.py ep01-piramide --still 15.2,40`.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `blender/kit.py` | bonecos de blocos (com rosto, expressões e poses), objetos (dinheiro, cofre, carro, avestruz…), luz e câmera |
| `blender/render.py` | renderiza um plano e grava onde cada objeto com etiqueta aparece na tela |
| `<ep>/roteiro.py` | **fonte única** do texto, tempo de cada palavra, títulos, etiquetas, X vermelho e números |
| `<ep>/cenas.py` | uma função por plano: monta o cenário e anima |
| `montar.py` | junta tudo: legenda karaokê (2 palavras, a falada em amarelo), títulos, números, etiquetas, X, chicote, efeitos e trilha |

O vídeo sai **sem voz**: a narração (`narracao.txt`) é gravada depois por cima. Se a fala gravada ficar mais
lenta ou mais rápida, ajuste `word_dur` em `roteiro.py` e renderize de novo.
