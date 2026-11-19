# Canal "E SE…" — episódios em vídeo vertical

Vídeos verticais 9:16 (1080x1920), 60–70 s, para TikTok/Shorts, sem voz: o dono do canal grava a narração depois.

**Antes de qualquer episódio novo, leia `ESTILO.md`.** É o guia medido quadro a quadro no vídeo de referência
(câmera, cortes, legenda, ritmo, estrutura do roteiro). A câmera dele está pronta em `blender/camera.py`.

## Regras do canal "E SE…"
- O gancho começa sempre com "E se…" + o tema.
- Perto do fim, uma pausa com escolha para o público; os comentários decidem o próximo episódio.
- Entregar o vídeo **sem voz** + o texto da narração com tempos (`narracao.txt`).
- Personagem do canal: o Léo (`blender/lib.py`). Roteiro sempre original: da referência copiamos a linguagem
  (câmera, ritmo, formato), não o texto nem as piadas.
- Estilo: cartoon, personagem central grande, legenda de 1 palavra por vez (centro em y≈1360), câmera
  sempre em zoom lento com whips rápidos nas trocas, close no rosto nas reações, folhas de calendário
  voando nos saltos de tempo.

## Estrutura
- `ESTILO.md` — guia de estilo (ler primeiro).
- `blender/lib.py`, `blender/look.py` — Léo e render Workbench; `blender/camera.py` — gramática de câmera (Rig/Shot).
- `episodios/<tema>/` — um episódio por pasta (modelo atual: `episodios/imortal/`):
  `roteiro.py` (texto, tempos, legendas, calendário, card), `cenas.py` (cenas bpy), `render.py`,
  `render_todas.sh`, `montar.sh`, `hyperframes/` (composição final), `narracao.txt`.
- Episódio 1 (encolher), na raiz: `blender/scenes.py`, `hyperframes/`, `scripts/`, `narracao.txt`.

## Ao mudar algo
- Mudou o roteiro? Rode `python3 episodios/<tema>/roteiro.py` e renderize as cenas de novo (as durações mudam).
- Antes de renderizar tudo, gere stills da cena alterada e confira o enquadramento: o quadro é vertical,
  então empilhe os elementos na vertical (personagem embaixo, coisa grande em cima) em vez de lado a lado.
- Render aqui no container: `bpy` do pip (`pip install bpy==5.3.0`) + `apt-get install libegl1 libegl-mesa0 libgl1-mesa-dri`.
  Custa ~2 s por quadro em 720x1280; o episódio inteiro leva ~1 h.
- Falas em português do Brasil.
