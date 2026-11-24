# Estudo: Shopify Editions Winter ’26 ("The Renaissance Edition")

Site estudado: `https://www.shopify.com/editions/winter2026` (analisado em 24/11/2026).
Fontes da análise: HTML servido, o CSS do Tailwind, os pacotes JS das cenas 3D, os shaders GLSL embutidos e prints em desktop (1440×900) e celular (iPhone 13).

O modelo que reproduz tudo isso está em [`modelo/`](modelo/). Para trocar as fotos, veja [`modelo/LEIA-ME.md`](modelo/LEIA-ME.md).

---

## 1. Conceito

- **Ideia visual:** pinturas renascentistas (óleo sobre tela, luz de Caravaggio, paisagens de Da Vinci) com **objetos modernos** inseridos: tênis rosa, skate, notebook, máscara roxa, boné, celular, caixa de entrega nas costas de um guepardo. O humor vem do anacronismo.
- **Trocadilho do título:** "The Ren**ai**ssance Edition". O "ai" sai em fonte manuscrita (Imperial Script), no meio de um título em sans-serif bold.
- **Estrutura:** uma abertura e **12 capítulos** (Sidekick, Agentic, Online, Retail, Marketing, Checkout, Operations, Shop app, B2B, Finance, Shipping, Developer), com mais de 150 novidades em 116 cards.
- **Contraste:** cada capítulo abre escuro e cinematográfico (pintura em tela cheia e título gigante) e depois vira papel claro e editorial (fundo bege, grade de cards).

## 2. Pilha técnica (o que tem por baixo)

| Camada | O que usam | Como identifiquei |
|---|---|---|
| Framework | **Shopify Hydrogen** (React + Remix/React Router) hospedado no **Oxygen** | caminhos `cdn.shopify.com/oxygen-v2/...`, `entry.client`, `manifest`, rotas `(_locale).editions.winter2026` |
| CSS | **Tailwind CSS v4** (variáveis `--tw-*`, `@layer`, tokens `--color-*` em oklch) | `tailwind-G-N6aznT.css` (130 KB) |
| Scroll suave | **Lenis** (`duration: 1`, easing `min(1, 1.001 − 2^(−10t))`, `smoothWheel`) | config literal no pacote da rota |
| 3D | **Three.js** + **React Three Fiber**, pós-processamento (`EffectComposer`, Bloom) | `Background-*.js` (1 MB), `Effects-*.js` |
| Animação 3D | **Theatre.js**: cada capítulo tem um arquivo `*Scene.theatre-project-state.json`; o scroll controla `sheet.sequence.position` | `useTheatre({name:"HeroScene", stateUrl})`, `sequence.position = progress * duração` |
| Estado | **zustand** (stores `sectionMap`, `activeSection`, `overlayPosition`, `darkenIntensity`) | código do store no pacote da rota |
| Microanimações | **Rive** (`.riv`, 27 arquivos) nos destaques: Rollouts, Pulse etc. | `rive-*.js`, `RiveInner-*.js` |
| Texturas | **KTX2/Basis** (texturas comprimidas para GPU), uma versão desktop e uma `Fallback_Mobile_*_2x.ktx2` por cena | 40 arquivos `.ktx2` |
| Modelos | **GLB** (37 referências), por exemplo as borboletas e objetos das cenas | `.glb` no HTML |
| Vídeo | `webm` + `mp4` (38 + 72), com o par para cada navegador | HTML |
| Detecção de GPU | **detect-gpu**: celular ou GPU fraca recebem imagem estática em vez de 3D | `detect-gpu.esm-*.js`, `FallbackImageScene` |

## 3. Anatomia da página (separada em partes)

```
┌──────────────────────────────────────────────────────────────┐
│ [A] NAV fixa: marca + edição │ Edições ▾ │ Buscar │ site │ CTA │
├────────────┬─────────────────────────────────────────────────┤
│ [C] BARRA  │ [D] CAPÍTULO (repete 12×)                       │
│  LATERAL   │   D1. Herói: pintura 3D em tela cheia (fixa)     │
│  (fixa,    │       NOME GIGANTE (headline-1)                  │
│   20% da   │       𝒯rase narrativa com capitular manuscrita   │
│   largura) │       + teaser de vídeo                          │
│            │   D2. Destaques: o véu bege sobe por cima da     │
│  Título    │       pintura; título 32px + texto serifado      │
│  Índice    │       + link ↗ + animação Rive grande            │
│  I…XII     │   D3. Grade de cards: fundo #f7f7ee sólido,      │
│  © legal   │       12 colunas, cards com imagem e itens       │
│            │       de lista (título | texto)                  │
├────────────┴─────────────────────────────────────────────────┤
│ [B] ABERTURA (antes de tudo): linhas áureas + caixa 340×464  │
│ [E] RODAPÉ / outras edições                                  │
│ [F] CANVAS WebGL fixo atrás de tudo (z-index 0)              │
└──────────────────────────────────────────────────────────────┘
```

### [A] Navegação
- Altura 60px; padding 10/20 (12/8 no desktop). Fundo transparente.
- Botões `navButton`: raio 4px, altura mínima 34px; no hover o fundo fica branco e o texto preto.
- CTA `roundedButton`: pílula de 34px, fundo branco e texto preto. Em áreas claras inverte para fundo preto.
- **Tema automático:** cada bloco declara `data-nav-theme="dark|light"` e a nav troca a cor conforme o que passa por baixo dela.
- **Entrada:** os itens descem de `translateY(-100%)` para 0 (`nav-item-in`).

### [B] Abertura ("linhas da Vinci")
- Uma **caixa de 340×464px** fixa no centro da tela (`top: 50svh`) e, em volta dela, uma **construção geométrica áurea** em SVG: prumos, diagonais, retângulos áureos com subdivisões, dois círculos que tocam o centro e arcos em "lente".
- **Técnica de desenho:** cada traço tem `pathLength="1"`, `stroke-dasharray: 1` e `stroke-dashoffset: 1 → 0`. Os traços acendem em **grupos** (`data-active="1..8"`).
- **Tempos exatos do CSS original:**
  - traços: `3s cubic-bezier(.34,.22,.47,.84)`; depois a cor apaga de `#ffffffbf` para `#ffffff26` em 4s (`line-fade`);
  - borda "carregando": `6s cubic-bezier(.45,.28,.34,.84)` até 80% (`dashoffset .2`) e completa em `1s cubic-bezier(.72,.16,.19,.96)` quando a cena 3D termina de carregar;
  - sumiço no scroll: `.52s cubic-bezier(.25,.46,.45,.94)`;
  - "ai" deslizando: `.6s cubic-bezier(.72,.16,.19,.96)` vindo de `translateX(-898px)`.
- **Estados por atributo no `<html>`/`<body>`:** `data-initiated`, `data-scrolled`, `data-sidebar-loaded`, `data-sidebar-ready`. Todo o CSS da abertura reage a esses atributos; o JS só troca os valores.
- **Depois do carregamento,** a pintura da abertura aparece por trás e a caixa mostra o subtítulo ("A new world of commerce. 150+ product updates.") e o índice I–XII.

### [C] Barra lateral
- Depois do primeiro scroll, o título e o índice saem da caixa central e vão para a **coluna esquerda fixa** (20% da largura, só a partir de 940px).
- O item ativo fica com opacidade 1 e os outros apagados. A cor troca de claro para escuro conforme o fundo.
- **Hover no título:** "Ren" e "ssance" somem e o "ai" desliza (`-465px` / `-898px`, `.3s`).

### [D] Capítulo
- `<section id="online" data-section-index="2">` ocupa `w-4/5` à direita no desktop.
- **D1, herói:** `min-height: 140svh`. Tem o nome em `headline-1` e a frase em `narrative-1` com `drop-cap`. O nome some (opacidade) quando a frase sobe.
- **D2, destaques:** `padding-top: 25vh`. O fundo bege **não é CSS**: é o `overlayColor: #dcdcd0` do pós-processamento WebGL, que sobe com o scroll (`overlayPosition`). Por isso a pintura parece "virar papel".
- **D3, grade:** `bg-light #f7f7ee`, `grid-template-columns: repeat(12, 1fr)`, gap `clamp(12px,1vw,16px)`, `row-gap: 4rem`. Os cards com imagem usam `col-span-6`, a mídia sobre um fundo colorido (`BG-R`, `BG-Y`, `BG-G`, `BG-B`) e o texto em `max-width: 75%`.
- **Link de ação (`cta-link`):** texto `bodycopy-2` bold com um **quadradinho de 13px** e a seta ↗.

### [F] Cenas 3D (o "uau" do site)
Cada capítulo tem um componente `XxxScene`. Exemplo real (HeroScene):
```jsx
<SheetProvider sheet={useTheatre({ name: "HeroScene", stateUrl })}>
  <Environment/>
  <Camera theatreKey="camera"/>
  <Effects theatreKey="effects"/>          // bloom, overlay bege, escurecer
  <Particles theatreKey="particles"/>      // poeira com brilho
  <Butterflies theatreKey="butterflies"/>  // borboletas instanciadas
  <PointLight theatreKey="light-1" position={[-.5,0,.5]} color="#ff0000"/>
  <PointLight theatreKey="light-2" position={[.5,0,.5]}  color="#0000ff"/>
  {backgroundAssets.map((a, i) => <Asset url={a.url} theatreKey={`asset-${i+1}`}/>)}
</SheetProvider>
```
- **A pintura é feita de camadas** (`asset-1`, `asset-2`…): recortes da imagem em planos com profundidades diferentes. A câmera anda entre eles e isso cria o parallax 3D.
- **O scroll controla a timeline:** o store calcula o `progress` de cada seção e a cena faz `sheet.sequence.position = progress × duração`. Não tem nada no tempo, tudo é "scrubbed".
- **Transição entre cenas:** um shader de visibilidade descarta pixels por **ruído fbm + distância radial** e a borda do recorte fica **8× mais brilhante** (`mix(rgb*8., rgb, edge)`). O efeito é de papel queimando.
- **Partículas:** `gl_PointCoord` com queda suave (`smoothstep(0., blur, dist)`).
- **Borboletas:** geometria instanciada; o vertex shader bate as asas com `sin` (velocidade 4–8, amplitude e assimetria aleatórias por instância); o fragment shader gira o matiz (HSL) e acrescenta um brilho pulsante nas bordas.
- **Pós-processamento:** `bloomIntensity: 8`, `darkenIntensity` (escurece quando o texto passa por cima) e o overlay bege `#dcdcd0`.
- **Celular e GPU fraca:** `FallbackImageScene` mostra uma única imagem KTX2 num plano com "object-fit: cover" calculado no shader.

## 4. Tipografia

| Papel | Fonte original | Tamanho (celular → desktop) | Entrelinha / espaço | Alternativa livre usada no modelo |
|---|---|---|---|---|
| `headline-1` (nome do capítulo) | **NeueMontreal Bold** (Pangram Pangram) | 72px → `clamp(7.5rem, 35.79px + 10.96vw, 13.75rem)` | .9 / −.03em | Inter Tight 700 |
| `headline-2` | NeueMontreal Bold | 64px → `clamp(6.25rem, …, 8.75rem)` | .9 / −.03em | Inter Tight 700 |
| `headline-3` | NeueMontreal Bold | 54px → `clamp(3.375rem, …, 4rem)` | .9 / −.02em | Inter Tight 700 |
| `headline-4` (título de destaque) | NeueMontreal Bold | 32px | .95 / −.03em | Inter Tight 700 |
| `bodycopy-1` / `-2` | NeueMontreal Bold | 16 → 14px / 14 → 11px | 1.1 | Inter Tight 700 |
| `narrative-1` (frase do capítulo) | **HW Cigars** (Heavyweight Type) | 28px → `clamp(2rem, 18.53px + 1.75vw, 3rem)` | .96 / −.05em | Instrument Serif |
| `narrative-2` / `-3` | HW Cigars | 24 → 29px / 20px | .97 / −.05/−.04em | Instrument Serif |
| capitular (`drop-cap::first-letter`) e o "ai" | **Imperial Script** | 70px → `clamp(6rem, 75.79px + 2.63vw, 7.5rem)`, `line-height: 0` | −.02em | **Imperial Script** (é a mesma, gratuita no Google Fonts) |
| Japonês | NotoSansJP | — | — | — |

Detalhes que fazem diferença:
- `text-box: trim-both cap alphabetic` corta o espaço acima da maiúscula e abaixo da linha de base, o que deixa o alinhamento exato.
- A capitular usa `text-indent` negativo e `translate` igual ao gap da grade, então a letra manuscrita "pendura" para fora da coluna.
- `text-wrap: pretty` em tudo.
- **Licenças:** NeueMontreal e HW Cigars são **fontes pagas**. Por isso o modelo usa alternativas livres, que já vêm embutidas em `modelo/fontes/`. Se quiser o visual idêntico, compre a licença e troque os três `@font-face` no começo do `estilo.css`.

## 5. Cores

| Token | Hex | Uso |
|---|---|---|
| preto | `#000` | fundo da página e da abertura |
| `text-light` / `bg-light` | `#f7f7ee` | texto sobre a pintura e fundo da grade de cards |
| `text-dark` / `bg-dark` | `#292919` | texto sobre o claro e fundo do tooltip |
| `text-grey-dark` | `#5c5c4e` | descrição dos cards e links sublinhados |
| overlay bege (WebGL) | `#dcdcd0` | o "papel" que cobre a pintura nos destaques |
| linhas da abertura | `#ffffffbf → #ffffff26` | traços acendendo e depois apagando |
| `text-light/60` | `#f7f7ee99` | itens inativos do índice |

## 6. Grade e espaçamento
- Variável `--spacing-grid-spacing`: 12px no celular e `clamp(12px, 1vw, 16px)` a partir de 769px.
- `.grid-template-with-gaps`: 2 colunas no celular e 12 a partir de 769px; `row-gap` de 2.5rem e depois 4rem.
- Breakpoints: **769px** (`md`), **940px** (`global-lg`: a barra lateral aparece e o conteúdo passa a ocupar 4/5), além de 1080, 1280, 1680 (largura máxima da nav).
- Herói: `min-height: 140svh` no desktop e 70svh no celular. Os destaques começam com 25vh de respiro.

## 7. Catálogo de animações

| # | Animação | Como é feita no original | No modelo |
|---|---|---|---|
| 1 | Linhas áureas se desenhando | SVG `pathLength=1`, `dashoffset 1→0`, grupos em sequência | ✅ igual (`app.js` `construirLinhas`) |
| 2 | Borda da caixa "carregando" | `dashoffset .2` em 6s e depois 0 em 1s | ✅ igual |
| 3 | Título sobe ao carregar | `translate-y: calc(235px - 50%)` → 0 | ✅ |
| 4 | Índice I–XII aparece em cascata | `stagger-fade-in` | ✅ (45ms por item) |
| 5 | Itens da nav descem | `nav-item-in` | ✅ |
| 6 | Tudo some no 1º scroll e vai para a lateral | `data-scrolled` + `.52s` | ✅ |
| 7 | Palavra manuscrita desliza | `@keyframes slide` `translateX(-898px)` | ✅ |
| 8 | Scroll amanteigado | Lenis `duration 1`, easing expo | ✅ mesma config |
| 9 | Câmera 3D andando com o scroll | Theatre.js `sequence.position = progress` | ✅ aproximado: zoom de 1.06→1.25 + pan com o scroll + parallax do mouse |
| 10 | Parallax de camadas | planos recortados em profundidade | ⚠️ o modelo usa 1 foto por capítulo (ver §9) |
| 11 | Transição "papel queimando" | shader fbm + borda ×8 | ✅ mesmo princípio (borda ×6) |
| 12 | Véu bege sobe sobre a pintura | overlay `#dcdcd0` no pós-processamento | ✅ no shader, com borda irregular de ruído |
| 13 | Escurecer atrás do texto | `darkenIntensity` | ✅ |
| 14 | Poeira/partículas | `gl.POINTS` com brilho suave | ✅ mesmo shader |
| 15 | Borboletas | instanced mesh + flap no vertex shader | ❌ não incluído (dá para adicionar) |
| 16 | Luzes coloridas vermelho/azul | `PointLight` animado pelo Theatre | ❌ (precisa das camadas 3D) |
| 17 | Bloom | pós-processamento, intensidade 8 | ➖ substituído por vinheta e grão de filme |
| 18 | Nome gigante some ao subir a frase | `transition-opacity` | ✅ + parallax leve |
| 19 | Mídias e cards aparecem | `media-entrance` (opacidade) | ✅ opacidade + subida de 24px |
| 20 | Microanimações de produto | Rive (`.riv`) | ➖ aceita vídeo MP4 no lugar |
| 21 | Emojis subindo | `emoji-rise`: sobe 200px e some, com escala aleatória | ❌ (específico de um card) |
| 22 | Pontos em órbita | `offset-path` + `orbit-path` com troca de z-index | ❌ (específico de um card) |
| 23 | Tema claro/escuro da nav e da lateral | `data-nav-theme` | ✅ |

## 8. Celular
- A barra lateral não aparece. A nav mostra a marca e a edição em duas linhas, o CTA e um menu ☰.
- A caixa da abertura ocupa quase a tela toda (`min(340px, 100vw − 24px)`), com o índice dentro.
- Em vez das cenas 3D entram imagens estáticas (`Fallback_Mobile_*_2x`) com a mesma lógica de "cover".
- O nome do capítulo diminui para 72px e a frase para 28px.

## 9. Diferenças entre o modelo e o original
1. **Camadas 3D:** o original recorta cada pintura em vários PNGs (fundo, figura, objetos) e anima uma câmera entre eles. O modelo faz zoom, pan, parallax do mouse e as transições sobre **uma foto por capítulo**. É isso que deixa trocar a imagem só mandando a foto. Se você mandar a foto já recortada em camadas (PNG com fundo transparente), dá para ligar o parallax em profundidade.
2. **Fontes pagas** trocadas por equivalentes livres (§4).
3. **Rive** trocado por imagem ou vídeo MP4 nos destaques.
4. **Nada da marca Shopify** foi copiado: nem logo, nem textos, nem imagens, nem os arquivos de fonte. O modelo vem com textos e fotos provisórios.
