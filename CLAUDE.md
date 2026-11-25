# Projeto: E SE você encolhesse pela metade todo dia?

Vídeo vertical 9:16 (1080x1920), ~63s, para TikTok/Shorts, sem voz: o dono do canal grava a narração depois.

## Regras do canal "E SE…"
- O gancho começa sempre com "E se…" + o tema.
- Perto do fim, uma pausa com escolha para o público; os comentários decidem o próximo episódio.
- Entregar o vídeo **sem voz** + o texto da narração com tempos (`narracao.txt`).
- Estilo de referência: cartoon, personagem central grande, legenda de 1 palavra por vez no meio da tela
  (fonte arredondada branca com contorno escuro), câmera sempre em zoom lento, close no rosto nas reações,
  folhas de calendário voando nos saltos de tempo.

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

## Série do Caio (cartoon 2D) — regras fixas
- Sempre o **mesmo protagonista: Caio** (9 anos, boné vermelho virado, camiseta laranja com bolso, bermuda azul, tênis amarelo).
- Padrão de **30 segundos** (900 quadros a 30 fps; se o usuário pedir outra duração, o episódio define `DUR = 45` etc.), vertical 1080x1920, **sem voz**, com legenda karaokê e o texto da narração com tempos.
- **Sempre entregar o roteiro pronto para o ElevenLabs** num bloco de copiar e colar (só o texto, uma fala por linha, **sem códigos de pausa**; `node cartoon2d/narracao.js epNN-tema` gera).
- Tema sempre ligado a **dinheiro: o Caio ganha ou perde** por uma regra do mundo ("Na minha cidade, cada X custa/rende Y") ou por escolha dele.
- **Início chamativo** (regra mágica nos primeiros 3 s, com imagem forte e zoom-out borrado) e história com **começo, meio e fim** + final com piada.
- Dinheiro na tela: cartão de SALDO, notas/moedas voando, "-R$" / "+R$" saltando, contadores grandes.
- Código em `cartoon2d/`: motor `engine.js` + `lib.js`; cada episódio é `cartoon2d/episodios/epNN-tema.js` (LINES + planos).
  Render: `cartoon2d/montar.sh epNN-tema` → `renders/epNN-tema.mp4`; narração: `node cartoon2d/narracao.js epNN-tema`.
- Episódios feitos: ep01 reclamação custa R$ 1; ep02 mentira custa R$ 10; ep03 abraço de verdade vale R$ 10 (falso custa); ep04 batalha de imaginação, aposta R$ 200 (45s); ep05 a sombra trabalha por você (pede aumento, vai embora); ep06 poderes no futebol: Caio de borracha x zagueiro Muralha de metal, prêmio R$ 500 (45s); ep07 vergonha rende R$ 5 (Ana dá oi, R$ 1.000, apelido Tomate); ep08 bocejo custa R$ 2 (estilo 2; a professora fica rica). Não repetir temas.
- Nada de personagens, nomes, visuais ou termos de obras de terceiros (ex.: One Piece); só ideias genéricas recriadas com o Caio.
- Temas preferidos: sentimentos e emoções do dia a dia (com humor), animação fluida (use `K()` para poses suaves, `walk`, `lean`, `hug`).
- **A partir do ep08 o mundo do Caio usa o ESTILO 2 (`cartoon2d/lib2.js`, carregado automaticamente para ep ≥ 08).** Sempre usar:
  - personagens v2: cabeça grande redonda, sobrancelha grossa, olhos ovais com brilho, bochecha alaranjada, cabelo com textura,
    roupa com sombra lateral e dobras, mão em luva, tênis de sola grossa; andar com o pé que sobe (`walk`), corpo balançando;
  - cenário `bairro(tag)` em camadas (céu azul com nuvens, morro com casinhas, casas detalhadas com telhas/venezianas/floreira/
    cerquinha/tijolo, postes com fios, árvores, calçada em perspectiva, asfalto escuro) e `parallax(tag, x)` quando a câmera anda;
    interiores com `room2()`;
  - saldo de cada personagem num balão sobre a cabeça (`pillSvg`/`showPill`) com "-R$" saltando dali; título grande no topo
    no gancho (`titleSvg`/`showTitle`); legenda branca no asfalto (y≈1745) com a palavra falada em amarelo;
  - cortes a cada ~2 s, closes para as reações, câmera sempre se movendo.
  Detalhes em `estilo-cartoon/GUIA.md` (seção "Estilo 2").

## Outros estilos do canal
- `estilo-cartoon/GUIA.md`: análise de dois cartoons 2D narrados (regra mágica, roteiro de 2 min, legenda karaokê) e prompts para refazer.
- `beco3d/`: animação 3D realista de 30s (Blender/Cycles), personagens fictícios.
