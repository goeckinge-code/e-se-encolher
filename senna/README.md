# Ayrton Senna — documentário interativo

Site biográfico estático (HTML, CSS e JavaScript puros, sem dependências) que conta a trajetória de Ayrton Senna em seis capítulos, conforme o visitante rola a página.

## Como abrir

```bash
cd senna
python3 -m http.server 8000   # depois abra http://localhost:8000
```

Qualquer hospedagem estática serve (Vercel, Netlify, GitHub Pages): publique a pasta `senna/` como raiz.

## Roteiro da página

| Momento | Fotografia | O que acontece |
|---|---|---|
| Abertura | — | A assinatura é escrita com a tinta real, em gestos contínuos, e pousa sobre o retrato. |
| Entrada | Retrato de 1994 + capacete | **Rosto e capacete:** um cardume de gotas de vidro (a lógica do CandyShoal, em 2D e sem cores) flutua, respira e se funde sobre o rosto, mostrando o capacete por dentro, sozinho, sem depender de nada. O cursor empurra as gotas; apertar e segurar as junta. Ao rolar, elas crescem e vestem o capacete inteiro. WebGL em `assets/js/capacete.js`. |
| O carro | 1ª (`01-abertura.jpg`, referência da composição) | Quando a seção aparece, as letras de **SENNA** caem e o carro entra pela direita até o centro. |
| Prólogo | — | O texto vai acendendo palavra por palavra conforme a leitura. |
| I · Infância (1960) | 2ª, o capacete | **Aqui começa a narrativa visual principal.** As fotos ficam fixas num palco enquanto os textos rolam. |
| II · Carreira (1984) | 3ª, o retrato | Cada nova foto entra como uma cópia impressa pousando no álbum e se "revela". A anterior fica embaixo, levemente girada. |
| III · Ascensão (1988 · 1990 · 1991) | 4ª, McLaren nº 8 | Zoom lento (Ken Burns) e parallax dentro da foto. Linha do tempo de 1960 a 1994. |
| IV · Conquistas | 5ª, o troféu | Contadores de 41 vitórias, 65 poles e 3 títulos. |
| V · Legado | 6ª | |
| VI · 1º de maio de 1994 | — | A página escurece; uma linha de pista se desenha e para. |
| Epílogo | — | A assinatura é escrita de novo e o carro atravessa a página e estaciona. |

## A assinatura: sistema do Plazza reaproveitado

O código de `assets/js/assinatura.js` foi portado do site principal (`plazza-company`, arquivo `base.html` na Vercel), mantendo o mesmo sistema e o mesmo comportamento:

- `SIG = { vb, d[] }`: traços de **linha central** da assinatura, no mesmo formato do Plazza;
- `fill(svg)` e `write(ps, dur, {gap, step, done})`: velocidade constante por traço, pausas entre traços e início e fim suaves;
- abertura com a estrela cadente que começa a escrita, o traço "quente" que segue a ponta da caneta, o contador de 000 a 100, o brilho, o *swoosh* e a assinatura que voa até o destino (`toHead`);
- `sigWrite()`: a mesma escrita disparada pelo scroll (usada no epílogo);
- grão animado, revelações com `IntersectionObserver` e contadores (`data-n`) também vêm do Plazza.

As mudanças foram só de adaptação: tinta escura sobre papel no lugar de branco sobre preto, o destino passou a ser a assinatura da hero e o *swoosh* corre da direita para a esquerda, como o rastro do carro. Os traços verticais são escritos de cima para baixo.

A `SIG` de Ayrton Senna foi extraída da assinatura real da primeira fotografia por `tools/assinatura_linha_central.py` (esqueletização, junção dos traços nos cruzamentos e suavização em curvas `Q`). Para trocar a assinatura, rode o script com outra imagem e cole o JSON gerado no lugar de `const SIG=` em `assinatura.js`.

## Revelações durante a rolagem

- Títulos sobem letra a letra; parágrafos aparecem palavra a palavra, cada uma saindo de uma máscara.
- Rótulos de capítulo "decodificam" de caracteres aleatórios até o texto final.
- Cada fotografia se revela de cima para baixo como uma impressão saindo, com zoom que assenta e rotação que se acomoda.

## Fotos em HD

`tools/hd.py` amplia uma foto com Real-ESRGAN (rodando em NumPy, sem PyTorch) e mistura o resultado com a ampliação clássica, para a pele não ficar "de cera":

```bash
python3 tools/hd.py realesr-general-x4v3.pth foto.jpg assets/img/foto.webp 1600 0.6
```

Os pesos do modelo estão nos *releases* do projeto Real-ESRGAN no GitHub (`realesr-general-x4v3.pth`, 5 MB). Use mistura 0.55–0.65 para rostos e 0.8–1 para objetos.

## Arquivos

```
senna/
├── index.html
├── assets/css/style.css     papel, impressões fotográficas, layout responsivo
├── assets/js/assinatura.js  sistema de assinatura (Plazza)
├── assets/js/capacete.js    entrada: rosto + capacete com máscara líquida (WebGL)
├── assets/js/main.js        carro, parallax, palco de fotos, linha do tempo, capítulos
├── assets/img/              fotos em WebP, carro recortado com alfa, rodas, textura de papel
└── tools/                   scripts usados para gerar a assinatura e o recorte do carro
```

## Acessibilidade e desempenho

- Com `prefers-reduced-motion`, a abertura é pulada e tudo aparece já no lugar, sem parallax nem zoom.
- A abertura tem o botão "Pular abertura" e também fecha com `Esc`.
- As imagens somam cerca de 1,2 MB em WebP, já em HD. A rolagem tem inércia na roda do mouse e no trackpad, e as camadas fixas de papel e grão não usam `mix-blend-mode`, que obrigaria o navegador a recompor a tela inteira a cada quadro. As animações usam só `transform` e `opacity` num único laço `requestAnimationFrame`, que não recalcula nada quando a página está parada.
- As fotos são da referência enviada; os direitos pertencem aos respectivos autores.
