# Beco 3D: animação de 30s (vertical 9:16)

Animação 3D feita no Blender (Python/bpy) a partir dos primeiros 30 segundos de um vídeo de referência:
um agente de proteção animal confronta um rapaz na escadaria de um beco de comunidade.
**Os personagens são fictícios.** Mantêm as roupas, gestos e expressões da referência, mas sem nomes,
rostos ou acusações das pessoas reais. O vídeo sai **sem áudio** e sem textos; a narração entra depois.

- **Agente:** camisa manga longa azul-marinho, colete tático preto "PROTEÇÃO ANIMAL", calça cáqui, cinto, luvas brancas, sapato preto.
- **Rapaz:** sem camisa, bermuda preta estampada, descalço, cabelo cacheado curto.
- **Cenário:** beco com parede verde-clara e rodapé de caco, escadaria de concreto com corrimão azul,
  casa amarela "34", janelas com grade branca, caixas de luz, vasos, fios, prédios ao fundo. Sol do meio-dia.

## Planos (24 fps, 720 quadros)

| # | Tempo | O que acontece | Câmera |
|---|---|---|---|
| 1 | 0,0–3,2 | Agente vem pelo beco falando e gesticulando, olha para cima | recua na frente dele |
| 2 | 3,2–6,5 | Rapaz sentado no corrimão; agente chega e começa a subir | atrás do agente, avançando |
| 3 | 6,5–12,0 | Confronto na escada: agente segura o braço, rapaz se protege e puxa | baixa, orbitando (mostra o colete) |
| 4 | 12,0–15,0 | Rapaz desce a escada olhando para trás; agente vem atrás | pan rápido acompanhando |
| 5 | 15,0–18,0 | No beco: rapaz de costas, agente explica com as mãos | por cima do ombro do rapaz |
| 6 | 18,0–22,0 | Rapaz com a mão no peito, espantado; agente aponta | frontal, aproximando |
| 7 | 22,0–24,5 | Rapaz espantado, boca aberta, mão espalmada | plano fechado |
| 8 | 24,5–30,0 | Pé da escada, na mureta azul: rapaz gesticula, agente ao lado | arco lento |

## Arquivos

- `pessoas.py`: personagens (corpo de metaballs, esqueleto, roupas, rosto com expressões: sobrancelha, pálpebras, boca)
- `cenario.py`: cenário e luz (céu Nishita + sol)
- `mat.py`: materiais procedurais (reboco manchado, concreto, caco, tecido, pele)
- `anim.py`: poses, caminhada, expressões e câmera de cada plano (tudo em função do tempo)
- `render.py`: render no Cycles

## Como renderizar

Precisa de Python 3.13 + `pip install bpy` (Blender 5.x como módulo) ou do próprio Blender.

```bash
python3 beco3d/render.py -- still 1.5,9,20,27      # quadros de teste em renders/beco/still/
python3 beco3d/render.py -- seq --samples 14       # 720 quadros 540x960 em renders/beco/frames/ (~11s/quadro na CPU)
python3 beco3d/render.py -- seq --hq               # 1080x1920 com mais amostras (bem mais lento)
scripts/montar_beco.sh                             # gera renders/beco-30s-3D.mp4 (1080x1920, sem áudio)
```

O render retoma de onde parou e aceita intervalo (`seq 0 240`) para dividir entre máquinas.
