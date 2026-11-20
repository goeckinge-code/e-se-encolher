# Estilo de referência: cartoon de palito com cenário noturno "meio realista"

Análise quadro a quadro de um vídeo de referência do TikTok (@historiasdertr, "Nessa cidade, quem rouba ganha um pix
na hora…", 151 s). O vídeo original **não** está no repositório: aqui ficam só as medidas, as regras e algumas folhas
de quadros para consulta. A ideia é usar a *linguagem* (personagens, luz, câmera, legenda, ritmo) para contar
**histórias nossas**: não copiar personagens, nomes ou cenas dele.

- Folhas de quadros (1 quadro por segundo, 24 por folha): `quadros/folha_01.jpg` … `folha_07.jpg`
- Quadros de exemplo: `quadros/exemplo_*.jpg`
- Tempos de todos os cortes: `cortes.txt` · zoom/pan medido por plano: `camera_por_plano.txt`
- Os mesmos números em formato de máquina: `estilo.json`

---

## 1. Formato
- 1080x1920, 30 fps, 2-3 min (aceita 60-90 s para Shorts).
- Narração em 1ª pessoa, contínua, sem pausa. A história é uma escalada: cada cena aumenta o valor, o risco ou o absurdo.
- Som: voz alta e na frente (média −17 dB, pico −1,7 dB), trilha baixa e efeitos curtos (vidro quebrando, moeda, sirene).

## 2. Personagens ("palito" de cabeça grande)
- **Cabeça:** círculo grande, cor de pele chapada `#d4a889`, **contorno preto grosso** (~6 px em 1080). Mais ou menos 1/4 da altura do corpo.
- **Corpo:** tronco estreito (moletom ou camisa), **braços e pernas finos como palitos**, de largura constante, sem cotovelo marcado. Mãos simples de 4 dedos.
- **Rosto:** olhos pretos em ponto (ou meia-lua quando ri), sobrancelha grossa, boca de traço. Expressão muda por **troca de desenho**, sem interpolar.
- **Marca de cada personagem:** um item forte e uma cor sólida (o protagonista de moletom amarelo `#d8ad32` e cabelo espetado; máscara preta de ladrão; vó de óculos redondos; vilão de cartola com lua). Assim dá para reconhecer cada um até bem pequeno.
- **Etiqueta de nome:** caixinha amarela com texto preto, acima ou ao lado da cabeça, quando o personagem aparece pela 1ª vez (ex.: "VÓ", "PROFESSORA").
- Animação "recortada" (cut-out): partes rígidas que giram nas juntas, ciclo de andar simples, poses-chave. Pouca deformação.

## 3. Cenário "meio realista" (é o que dá o charme)
O desenho é chapado, mas a **luz e a atmosfera** são de filme:
- **Noite quase sempre:** fundo roxo-azulado escuro (`#0d0912`, `#201b2b`, `#37364b`) com janelas amarelas acesas.
- **Chuva** em riscos finos semitransparentes por cima de tudo, e **bokeh** (círculos coloridos desfocados) no fundo dos closes.
- **Luz volumétrica:** cones de poste e holofotes com brilho (glow) aditivo; placas de **neon** ("LANCHES 24H", "JOIAS") com halo.
- **Profundidade de campo:** primeiro plano e fundo desfocados; planos de rua em **2,5D** (camadas chapadas espaçadas em 3D e câmera andando entre elas, com paralaxe).
- **Vinheta** escura nas bordas e um degradê escuro em baixo, onde fica a legenda.
- Cores de destaque saturadas sobre o fundo escuro: verde dinheiro `#3cff5a`, amarelo-ouro, vermelho-alarme, rosa-neon.
- Composições simétricas e centralizadas (corredor com tapete vermelho, ponto de fuga no meio, personagem no eixo).

## 4. Câmera e montagem
- **69 planos em 151 s:** média de 2,2 s, mediana de 1,8 s. Corte a cada 1-3 palavras de ênfase.
- **Quase todo plano tem zoom-in lento:** 2-9 % por segundo (mediana em torno de 5 %/s), com leve subida (o quadro desce 40-150 px no plano).
- **Push-in rápido até o rosto** nas revelações: 15-75 %/s em 1,5-3,5 s.
- **Planos de travelling** (5-8 s) andando por uma rua ou corredor em 2,5D para apresentar um lugar novo.
- Cortes **secos** (sem dissolve). De vez em quando um efeito vira a transição (vidro estilhaçando, flash).
- Ritmo: plano aberto do lugar → plano médio da ação → close de reação → painel ou número na tela.

## 5. Legenda (palavra por palavra)
- **1 a 2 palavras por vez**, em CAIXA ALTA, troca seca no ritmo da fala.
- Fonte: sans humanista **ExtraBold** (Open Sans ExtraBold / Nunito Black servem), branco `#ffffff`.
- Contorno escuro fino (~3 px) e sombra suave escura embaixo.
- Altura das maiúsculas ≈ **43 px** em 1080x1920 (fonte de mais ou menos 58 px). É pequena e discreta: a imagem é que manda.
- Centralizada na horizontal, **centro em y ≈ 1374 px (71,5 % da altura)**, sobre o degradê escuro de baixo.

## 6. Gráficos na tela (o "placar" da história)
- **Contador de dinheiro:** "+R$ 2.000" verde neon com contorno escuro e brilho, que aparece por cima do personagem quando algo acontece. Entra com *pop* (escala 0,6→1,1→1) e some subindo.
- **Painel / ranking:** placa de metal com parafusos e tela verde de terminal (fonte condensada bold verde `#3cff5a`, 1º lugar em amarelo com moldura), presa por holofotes no céu. Volta várias vezes e muda conforme a história.
- **Cartaz de alerta:** fundo vermelho com faixas pretas e amarelas de perigo, título em branco.
- **Placas de lugar** ("DELEGACIA", "BANCO CENTRAL", "DEGRAU 249") com moldura, texto grande e legível.
- **Celular na mão** mostrando notificação ("PIX RECEBIDO R$ 1.000.000").
- Toda informação importante vira **texto dentro da cena**, para ser entendida sem som.

## 7. Estrutura de roteiro
1. **Gancho (0-6 s):** regra absurda do mundo + prova visual imediata (crime → "+R$ 2.000" na tela).
2. **Regras e escala (6-40 s):** a regra cresce (carteira → casa → banco); apresenta o placar ou ranking.
3. **Protagonista no fundo do poço (40-60 s):** apresenta o "eu", a família e o motivo.
4. **Escalada em 3-4 golpes** cada vez maiores, sempre com o placar subindo.
5. **Antagonista lendário e lugar final** (torre, cofre, castelo) com obstáculos visuais (tubarão, laser, escada de 249 degraus).
6. **Virada:** o mundo se volta contra o protagonista (novo alvo: ele mesmo).
7. **Final em aberto** ou pergunta, para gerar comentários.

## 8. Como usar no nosso pipeline
- O pipeline atual (`blender/` + `hyperframes/`) serve: Blender com câmera **ortográfica ou de perspectiva leve** e personagens 2D
  (planos com textura ou curvas com contorno) em camadas no eixo Z → paralaxe de 2,5D de graça.
- Chuva, bokeh, glow, vinheta e legenda podem ficar na composição do HyperFrames (HTML/CSS por cima do vídeo), como já fazemos com as legendas.
- Valores de referência para câmera, legenda e cortes: `estilo.json`.
- Regra do canal "E SE…" continua valendo: o gancho começa com "E se…" e a pausa de escolha vai perto do fim.
