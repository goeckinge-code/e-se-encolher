# Projeto: E SE você encolhesse pela metade todo dia?

Vídeo vertical 9:16 (1080x1920), ~63s, para TikTok/Shorts, sem voz: o dono do canal grava a narração depois.

## Regras do canal "E SE…"
- O gancho começa sempre com "E se…" + o tema.
- Perto do fim, uma pausa com escolha para o público; os comentários decidem o próximo episódio.
- Entregar o vídeo **sem voz** + o texto da narração com tempos (`narracao.txt`).
- Estilo de referência: cartoon, personagem central grande, legenda de 1 palavra por vez no meio da tela
  (fonte arredondada branca com contorno escuro), câmera sempre em zoom lento, close no rosto nas reações,
  folhas de calendário voando nos saltos de tempo.
- Guia de estilo completo (os dois vídeos de referência): `referencias/ESTILO.md`.
  Análise do vídeo do @brazza3d: `referencias/brazza3d-fraude-inss/ANALISE.md`.

## Estrutura
- `blender/` — personagem e cenas em bpy. `render.py` roda por cena (`-- sN seq|still [--hq]`).
- `hyperframes/build/build.py` — fonte única do roteiro (`SCENES`) e dos tempos; gera legendas e calendário.
- `hyperframes/` — composição final (vídeo do Blender + legendas + calendário + card de escolha).
- `scripts/` — `render_todas.sh` e `montar.sh`.

## Ao mudar algo
- Mudou o roteiro? Rode `python3 hyperframes/build/build.py` e depois renderize as cenas de novo (as durações mudam).
- Antes de renderizar tudo, gere stills da cena alterada e confira o enquadramento: o quadro é vertical,
  então empilhe os elementos na vertical (personagem embaixo, criatura em cima) em vez de lado a lado.
- Falas em português do Brasil.
