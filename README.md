# E SE você encolhesse pela metade todo dia?

Episódio da série **"E SE…"**: o Léo acorda e encolhe pela metade a cada dia. Na tela ele passa pelo quarto, por um gato, por uma caixa de fósforo, uma formiga, um ácaro, bactérias, um vírus e um átomo. No fim, o público escolhe nos comentários: **continuar encolhendo** ou **tentar voltar**.

▶️ Prévia atual: [`renders/E-se-voce-encolhesse-3D.mp4`](renders/E-se-voce-encolhesse-3D.mp4) (63s, 9:16, sem voz)
🎙️ Narração com tempos: [`narracao.txt`](narracao.txt)

## Como o vídeo é feito

| Parte | Ferramenta | Onde |
|---|---|---|
| Personagem Léo 3D (boné, camiseta com raio, fone, expressões) | Blender (Python/bpy) | `blender/lib.py`, `blender/look.py` |
| 11 cenários 3D e animação de câmera | Blender | `blender/scenes.py` |
| Render de cada cena | Blender | `blender/render.py` |
| Roteiro e tempo de cada palavra | Python | `hyperframes/build/build.py` (`SCENES`) |
| Legendas, folhas de calendário, card final | HyperFrames (HTML → vídeo) | `hyperframes/compositions/` |

## Rodando no seu computador

Precisa de: **Blender 4.x ou mais novo**, **Node 22+**, **ffmpeg** e **Python 3**.

```bash
# 1. renderizar as cenas
scripts/render_todas.sh          # rápido: Workbench, 15fps, 720x1280
scripts/render_todas.sh --hq     # bonito: Eevee com contorno, 30fps, 1080x1920 (use placa de vídeo)

# 2. montar o vídeo final com legendas e o card de escolha
scripts/montar.sh                # ou: scripts/montar.sh --hq
```

Para testar uma cena só: `blender -b -P blender/render.py -- s4 still 0.3,0.85` (salva em `renders/still/`).

## Mudanças comuns

- **Texto da narração ou tempo das falas:** edite `SCENES` em `hyperframes/build/build.py` e rode `python3 hyperframes/build/build.py` para refazer legendas e calendário.
- **Visual do Léo:** cores no topo da classe `Leo` em `blender/lib.py`; expressões em `EXPR_*`.
- **Uma cena:** a função `build_sN` em `blender/scenes.py` (cenário, posições e `keys` da câmera).

## Pendências conhecidas

- Cena 3 (caixa de fósforo): o raio da camiseta atravessa o cobertor.
- Cena 4: a formiga fica parcialmente atrás do cubo de açúcar.
- Cena final: o card cobre parte da etiqueta "VOCÊ".
- Render `--hq` (Eevee) ainda não foi testado com placa de vídeo.

## Outro projeto neste repositório

- [`senna/`](senna/README.md): site biográfico interativo sobre Ayrton Senna, com a abertura de assinatura reaproveitada do Plazza.
