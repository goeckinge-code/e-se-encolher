/*
  CONTEÚDO DO SITE — este é o único arquivo que precisa mudar para trocar fotos e textos.

  FOTOS: coloque os arquivos na pasta  fotos/  e aponte o caminho aqui.
    - foto (fundo de cada capítulo): paisagem, 2400x1500 ou maior, JPG. Fica em tela cheia atrás do título,
      com zoom lento conforme o scroll e transição em "queimado" entre um capítulo e outro.
    - fotoMobile (opcional): versão vertical, 1200x2000, usada em telas estreitas.
    - midia dos destaques / cards: qualquer proporção; MP4 também funciona (toca mudo em loop).

  TEXTO DO TÍTULO: o trecho entre { } sai na fonte manuscrita (como o "ai" do original).
  Capítulos: pode ter quantos quiser; a numeração romana e o menu lateral se ajustam sozinhos.
*/
window.CONTEUDO = {
  marca: {
    nome: "Sua Marca",
    edicao: "Inverno ’26",
    linkSite: { texto: "suamarca.com", url: "#" },
    cta: { texto: "Comece agora", url: "#" },
  },

  abertura: {
    titulo: ["A", "Cole{çã}o", "Inverno"],
    subtitulo: "Um novo mundo de coisas boas. 60+ novidades.",
    foto: "fotos/abertura-seq/001.jpg",
    fotoMobile: "",
    // Sequência de quadros: anda conforme o scroll na abertura (apague para usar só a foto)
    sequencia: { pasta: "fotos/abertura-seq/", quadros: 107, alturaScroll: 3 },
  },

  capitulos: [
    {
      id: "colecao",
      nome: "Coleção",
      frase: "Peças pensadas para durar, feitas à mão por quem entende do assunto.",
      foto: "fotos/01-colecao.jpg",
      teaser: { midia: "fotos/card-1.jpg", video: true },
      subtitulo: "Feito para durar",
      destaques: [
        {
          titulo: "Tecidos escolhidos um a um",
          texto: "Cada rolo passa por três mãos antes de virar peça. Nada sai daqui sem ser aprovado.",
          link: { texto: "Ver coleção", url: "#" },
          midia: "fotos/card-2.jpg",
        },
        {
          titulo: "Acabamento de ateliê",
          texto: "Costuras reforçadas, botões de verdade e etiquetas que não pinicam.",
          link: { texto: "Saiba mais", url: "#" },
          midia: "fotos/card-3.jpg",
        },
      ],
      cards: [
        { titulo: "Linha básica", texto: "As peças do dia a dia, em seis cores novas.", link: { texto: "Comprar", url: "#" }, midia: "fotos/card-4.jpg" },
        { titulo: "Edição limitada", texto: "Só 200 unidades de cada, numeradas.", link: { texto: "Comprar", url: "#" }, midia: "fotos/card-5.jpg" },
        { titulo: "Trocas grátis", texto: "Trinta dias para trocar, sem perguntas." },
        { titulo: "Feito no Brasil", texto: "Produção local, de ponta a ponta." },
        { titulo: "Embalagem reciclável", texto: "Papel kraft e fita de algodão." },
        { titulo: "Tabela de medidas", texto: "Medidas reais de cada peça, em centímetros." },
      ],
    },
    {
      id: "atelie",
      nome: "Ateliê",
      frase: "Onde tudo começa: rascunho, tesoura e muito café.",
      foto: "fotos/02-atelie.jpg",
      subtitulo: "Mãos à obra",
      destaques: [
        {
          titulo: "Visite o ateliê",
          texto: "Abrimos as portas no primeiro sábado de cada mês. Traga suas perguntas.",
          link: { texto: "Agendar visita", url: "#" },
          midia: "fotos/card-6.jpg",
        },
      ],
      cards: [
        { titulo: "Oficinas", texto: "Aprenda a costurar a sua primeira peça.", midia: "fotos/card-1.jpg", link: { texto: "Inscrever-se", url: "#" } },
        { titulo: "Sob medida", texto: "Ajustes feitos por quem fez a peça.", midia: "fotos/card-3.jpg", link: { texto: "Pedir ajuste", url: "#" } },
        { titulo: "Bastidores", texto: "Acompanhe o processo nas redes." },
        { titulo: "Equipe", texto: "Conheça quem faz a marca." },
      ],
    },
    {
      id: "loja",
      nome: "Loja",
      frase: "Um lugar para ver, tocar e provar antes de levar.",
      foto: "fotos/03-loja.jpg",
      subtitulo: "Venha nos ver",
      destaques: [
        {
          titulo: "Retire na loja",
          texto: "Compre on-line e retire em duas horas, sem pagar frete.",
          link: { texto: "Ver endereço", url: "#" },
          midia: "fotos/card-4.jpg",
        },
      ],
      cards: [
        { titulo: "Horários", texto: "Segunda a sábado, das 10h às 20h." },
        { titulo: "Estacionamento", texto: "Conveniado, com duas horas grátis." },
        { titulo: "Provador", texto: "Reserve um horário e prove com calma." },
        { titulo: "Café", texto: "Por nossa conta enquanto você escolhe." },
      ],
    },
    {
      id: "historias",
      nome: "Histórias",
      frase: "Clientes, lugares e peças que ganharam vida própria.",
      foto: "fotos/04-historias.jpg",
      subtitulo: "Quem veste conta",
      destaques: [
        {
          titulo: "Diário de viagem",
          texto: "Uma jaqueta, doze países e muitas histórias para contar.",
          link: { texto: "Ler história", url: "#" },
          midia: "fotos/card-5.jpg",
        },
      ],
      cards: [
        { titulo: "Envie a sua", texto: "Mande uma foto e conte a sua história.", midia: "fotos/card-2.jpg", link: { texto: "Enviar", url: "#" } },
        { titulo: "Revista", texto: "Uma edição impressa por estação.", midia: "fotos/card-6.jpg", link: { texto: "Assinar", url: "#" } },
      ],
    },
    {
      id: "entrega",
      nome: "Entrega",
      frase: "Do ateliê até a sua porta, com cuidado em cada etapa.",
      foto: "fotos/05-entrega.jpg",
      subtitulo: "Chega rápido",
      destaques: [
        {
          titulo: "Rastreamento em tempo real",
          texto: "Acompanhe o pedido do ateliê até a sua casa, passo a passo.",
          link: { texto: "Rastrear pedido", url: "#" },
          midia: "fotos/card-3.jpg",
        },
      ],
      cards: [
        { titulo: "Frete grátis", texto: "Para compras acima de R$ 299." },
        { titulo: "Entrega expressa", texto: "Em até 24 horas nas capitais." },
        { titulo: "Presente", texto: "Embrulho e cartão escrito à mão." },
        { titulo: "Devolução", texto: "Coleta grátis na sua casa." },
      ],
    },
    {
      id: "contato",
      nome: "Contato",
      frase: "Fale com a gente do jeito que preferir.",
      foto: "fotos/06-contato.jpg",
      subtitulo: "Estamos aqui",
      destaques: [
        {
          titulo: "Atendimento humano",
          texto: "Nada de robô: quem responde é gente que conhece cada peça.",
          link: { texto: "Chamar no WhatsApp", url: "#" },
          midia: "fotos/card-1.jpg",
        },
      ],
      cards: [
        { titulo: "E-mail", texto: "contato@suamarca.com" },
        { titulo: "Telefone", texto: "(11) 0000-0000" },
        { titulo: "Instagram", texto: "@suamarca" },
        { titulo: "Endereço", texto: "Rua Exemplo, 123 — São Paulo" },
      ],
    },
  ],

  rodape: {
    frase: "Obrigado por chegar até aqui.",
    links: [
      { texto: "Termos de uso", url: "#" },
      { texto: "Privacidade", url: "#" },
    ],
  },
};
