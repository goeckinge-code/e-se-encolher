# Série do Caio: cartoon 2D de 30s

Animação vertical 1080x1920, 30 fps, **sem voz** (narração em `narracao.txt`), no estilo analisado em `estilo-cartoon/GUIA.md`:
personagens "adesivo" (cabeçona, contorno grosso, olhões), cenário pastel visto de lado com faixa de asfalto,
legenda karaokê embaixo, animação de recorte (respira, pisca, fala, troca de pose), cortes a cada ~1,5 s,
zoom-out borrado na abertura, whip-pan, contadores de dinheiro e cartão de saldo.

- `lib.js`: desenho dos personagens, cenário, moedas, notas, balões, gato, "-R$", cartão de saldo
- `engine.js`: motor comum (personagens da série, câmera, legenda karaokê)
- `episodios/epNN-tema.js`: roteiro (`LINES`, fonte única dos tempos) e os planos de cada episódio; `epNN-tema.txt` é a narração
- `render.js`: `node render.js still 1,9.5 --ep ep02-mentira` ou `node render.js seq 30 --ep ep02-mentira`
- `montar.sh ep02-mentira`: gera `renders/ep02-mentira.mp4` (o ep01 sai como `renders/reclamacao-custa-1-real.mp4`)
- `narracao.js ep02-mentira`: gera o texto da narração com tempos

Episódios: ep01 "cada reclamação custa um real", ep02 "cada mentira custa dez reais", ep03 "abraço de verdade vale dez reais", ep04 "batalha de imaginação" (45s; `DUR = 45` no episódio), ep05 "a sua sombra pode trabalhar por você", ep06 "todo mundo tem um poder" (futebol, borracha x metal, 45s), ep07 "cada vergonha rende cinco reais", ep08 "cada bocejo custa dois reais" (primeiro no estilo 2).

**Estilo 2 (ep08 em diante):** `lib2.js` redesenha os personagens e traz `bairro()`, `parallax()`, `room2()`, `pillSvg/showPill` (saldo sobre a cabeça) e `titleSvg/showTitle`. É carregado automaticamente pelo `index.html` para episódios ≥ 08.
Mudou o texto? Edite `LINES` no episódio, ajuste os planos, apague `out/<ep>/frames` e rode `./montar.sh <ep>`.
