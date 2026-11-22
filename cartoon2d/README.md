# "Na minha cidade, cada reclamação custa um real" (cartoon 2D, 30s)

Animação vertical 1080x1920, 30 fps, **sem voz** (narração em `narracao.txt`), no estilo analisado em `estilo-cartoon/GUIA.md`:
personagens "adesivo" (cabeçona, contorno grosso, olhões), cenário pastel visto de lado com faixa de asfalto,
legenda karaokê embaixo, animação de recorte (respira, pisca, fala, troca de pose), cortes a cada ~1,5 s,
zoom-out borrado na abertura, whip-pan, contadores de dinheiro e cartão de saldo.

- `lib.js`: desenho dos personagens, cenário, moedas, "-R$1", cartão de saldo
- `anim.js`: roteiro (`LINES`, fonte única dos tempos) e os 13 planos
- `render.js`: renderiza no Chromium (Playwright): `node render.js still 1,9.5` ou `node render.js seq`
- `montar.sh`: gera `renders/reclamacao-custa-1-real.mp4`

Mudou o texto? Edite `LINES` em `anim.js`, ajuste os tempos dos planos e rode `./montar.sh` (apague `out/frames` antes).
