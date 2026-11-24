# Modelo "Edição": como usar e trocar as fotos

## Ver funcionando
O site carrega fotos e fontes de arquivos locais, então precisa de um servidor simples (abrir o `index.html` com dois cliques não basta):

```bash
cd estudo-site-editions/modelo
python3 -m http.server 8000
# abra http://localhost:8000
```

Também roda direto em Netlify, Vercel ou GitHub Pages: basta subir a pasta `modelo/` inteira.

## Trocar as fotos (o que você me manda)

| Arquivo | Onde aparece | Formato ideal |
|---|---|---|
| `fotos/00-abertura.jpg` | fundo da abertura, atrás da caixa com as linhas | horizontal, 2400×1500 ou maior |
| `fotos/01-colecao.jpg` … `06-contato.jpg` | fundo de cada capítulo (tela cheia, com zoom lento) | horizontal, 2400×1500 ou maior |
| `fotos/card-1.jpg` … `card-6.jpg` | destaques, teaser e cards | qualquer proporção (os cards cortam em 3:2) |

Dicas para as fotos de fundo ficarem como no original:
- **Deixe espaço livre na metade de baixo e à esquerda,** onde entram o nome gigante e a frase.
- Imagens escuras e com bastante contraste valorizam o texto claro.
- Use JPG com qualidade 80–85. Fotos maiores que 4096px são reduzidas automaticamente.
- Para celular, você pode mandar uma versão vertical e eu preencho o campo `fotoMobile`.
- Vídeo também funciona nos destaques e cards: basta usar um `.mp4` no lugar do `.jpg`.

Para trocar: substitua o arquivo com **o mesmo nome**, ou coloque um novo e mude o caminho em `conteudo.js`.

## Trocar textos, capítulos e links
Tudo fica em **`conteudo.js`**: nome da marca, título da abertura, capítulos, destaques, cards e rodapé.
- No título, o trecho entre `{chaves}` sai em letra manuscrita: `"Cole{çã}o"`.
- Para ter mais ou menos capítulos, basta acrescentar ou apagar blocos. A numeração romana e o menu se ajustam sozinhos.

## Arquivos
```
modelo/
├─ index.html        estrutura (nav, abertura, lateral, área dos capítulos)
├─ conteudo.js       ← TEXTOS E FOTOS (o único arquivo para editar)
├─ css/estilo.css    tipografia, cores, grade, animações em CSS
├─ js/montar.js      gera o HTML dos capítulos a partir do conteudo.js
├─ js/cena.js        fundo WebGL: cover, zoom, transição queimada, véu bege, partículas
├─ js/app.js         Lenis, linhas da abertura, lateral, tema da nav, scroll → cena
├─ vendor/           Lenis 1.1.13
├─ fontes/           Inter Tight, Instrument Serif, Imperial Script (licença OFL)
└─ fotos/            fotos provisórias (troque estas)
```

Sem WebGL (navegador antigo) o fundo usa CSS, com a troca de foto em fade. Com "reduzir movimento" ativado no sistema, as animações são desligadas.
