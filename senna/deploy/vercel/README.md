# Publicação na Vercel

Projeto `ayrton-senna` (time do Plazza): https://ayrton-senna-ten.vercel.app

A Vercel ainda não tem acesso a este repositório no GitHub, então a publicação é feita só com estes dois arquivos:

- `index.html`: carregador (o mesmo truque do Plazza) que busca a página completa e a escreve;
- `vercel.json`: serve `/assets/*` e a página completa a partir do repositório público, pelo jsDelivr, fixados num commit.

Para publicar uma versão nova: faça o push, troque o commit nas duas URLs do `vercel.json` e envie esta pasta de novo para o projeto `ayrton-senna`.

Para a Vercel publicar sozinha a cada push, conceda ao app da Vercel acesso ao repositório `goeckinge-code/e-se-encolher` no GitHub e conecte o repositório no projeto, com a pasta raiz `senna`.
