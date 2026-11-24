/* =========================================================================
   APP — scroll suave (Lenis), abertura, barra lateral, tema da nav,
   controle do fundo pelo scroll, revelações.
   ========================================================================= */
(function () {
  const C = window.CONTEUDO;
  const body = document.body, html = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduzido = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const S = window.Cena.estado;

  // ---------- 1. Fundo: WebGL ou fallback CSS ----------
  const temGL = window.Cena.iniciar($("#cena"));
  if (!temGL) html.classList.add("sem-webgl");
  const fundoCSS = $("#fundo-css");
  const camadas = new Map();
  let veuCSS;
  if (!temGL) {
    veuCSS = document.createElement("div"); veuCSS.className = "veu";
    fundoCSS.appendChild(veuCSS);
  }
  const fotoDe = (item) => (innerWidth < 768 && item.fotoMobile ? item.fotoMobile : item.foto);
  const SEQ = C.abertura.sequencia;
  const urlsSeq = SEQ ? Array.from({ length: SEQ.quadros }, (_, i) => SEQ.pasta + String(i + 1).padStart(3, "0") + ".jpg") : [];
  let seqPronta = false;
  function mostrarAbertura() {
    if (temGL && seqPronta) return window.Cena.mostrarSeq();
    mostrarFoto(fotoDe(C.abertura));
  }
  if (SEQ) $(".espaco-abertura").style.height = `${SEQ.alturaScroll * 100}svh`;
  function mostrarFoto(url) {
    if (temGL) return window.Cena.mostrar(url);
    if (!camadas.has(url)) {
      const d = document.createElement("div"); d.className = "camada"; d.style.backgroundImage = `url("${url}")`;
      fundoCSS.insertBefore(d, veuCSS); camadas.set(url, d);
    }
    camadas.forEach((d, u) => d.classList.toggle("ativa", u === url));
  }

  // ---------- 2. Scroll suave (mesma configuração do original) ----------
  let lenis = null;
  if (!reduzido && window.Lenis) {
    lenis = new window.Lenis({
      duration: 1,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: "vertical",
      smoothWheel: true,
      wheelMultiplier: 1,
    });
  }
  const irPara = (alvo) => (lenis ? lenis.scrollTo(alvo, { duration: 1.6 }) : $(alvo)?.scrollIntoView({ behavior: "smooth" }));
  $$('a[href^="#"]').forEach((a) =>
    a.addEventListener("click", (e) => {
      const h = a.getAttribute("href");
      if (h.length < 2) return;
      e.preventDefault();
      irPara(h === "#topo" ? 0 : h);
    })
  );

  // ---------- 3. Linhas "da Vinci" (construção áurea) ----------
  const PHI = 1.618034;
  const svg = $("#linhas");
  function construirLinhas() {
    const W = innerWidth, H = innerHeight;
    const w = Math.min(340, W - 24), h = (w * 464) / 340;
    const cx = W / 2, cy = H / 2;
    const x0 = cx - w / 2, x1 = cx + w / 2, y0 = cy - h / 2, y1 = cy + h / 2;
    const el = [];
    const L = (g, ax, ay, bx, by) => el.push(`<line data-g="${g}" pathLength="1" x1="${ax}" y1="${ay}" x2="${bx}" y2="${by}"/>`);
    const O = (g, x, y, r) => el.push(`<circle data-g="${g}" pathLength="1" cx="${x}" cy="${y}" r="${r}"/>`);
    const P = (g, d) => el.push(`<path data-g="${g}" pathLength="1" d="${d}"/>`);
    // reta passando pelo centro e por um canto da caixa, estendida até a borda da tela
    const diag = (g, dx, dy) => { const k = Math.max(W, H) * 2; L(g, cx - dx * k, cy - dy * k, cx + dx * k, cy + dy * k); };

    L(1, cx, 0, cx, H);                       // eixo vertical
    L(1, x0, 0, x0, H); L(1, x1, 0, x1, H);   // prumos da caixa
    diag(2, w, h); diag(2, w, -h);            // diagonais da caixa
    diag(6, 1, 0.58); diag(6, 1, -0.58);      // diagonais longas (30°)

    // retângulos áureos com espiral (canto sup. esq. e inf. dir.)
    function retAureo(g, x, y, rw, rh, dir) {
      let d = `M${x} ${y}h${rw}v${rh}h${-rw}z`;
      let px = x, py = y, pw = rw, ph = rh;
      for (let i = 0; i < 5; i++) {
        const s = Math.min(pw, ph);
        const lado = (i + (dir > 0 ? 0 : 2)) % 4;   // gira o quadrado a cada passo
        // 0 = quadrado à esquerda, 1 = em cima, 2 = à direita, 3 = embaixo
        const qx = lado === 2 ? px + pw - s : px;
        const qy = lado === 3 ? py + ph - s : py;
        d += ` M${qx} ${qy}h${s}v${s}h${-s}z`;
        // arco da espiral dentro do quadrado
        const arcos = [
          `M${qx} ${qy + s}A${s} ${s} 0 0 1 ${qx + s} ${qy}`,
          `M${qx} ${qy}A${s} ${s} 0 0 1 ${qx + s} ${qy + s}`,
          `M${qx + s} ${qy}A${s} ${s} 0 0 1 ${qx} ${qy + s}`,
          `M${qx + s} ${qy + s}A${s} ${s} 0 0 1 ${qx} ${qy}`,
        ];
        P(g + 1, arcos[lado]);
        if (lado === 0) { px += s; pw -= s; } else if (lado === 1) { py += s; ph -= s; } else if (lado === 2) { pw -= s; } else { ph -= s; }
      }
      P(g, d);
    }
    const gw = w / PHI, gh = gw / PHI;
    retAureo(3, x0 - gw, y0, gw, gh, 1);
    retAureo(3, x1, y1 - gh, gw, gh, -1);
    L(3, 0, y0 + gh, x0, y0 + gh); L(3, x0 - gw, 0, x0 - gw, y0 + gh);
    L(3, x1, y1 - gh, W, y1 - gh); L(3, x1 + gw, y1 - gh, x1 + gw, H);

    const R = h * 0.916;                       // círculos que tocam o centro
    O(5, cx, cy - R, R); O(5, cx, cy + R, R);
    const R2 = h * 2.37;                       // arcos em "lente"
    O(7, cx - R2, cy, R2); O(7, cx + R2, cy, R2);

    el.push(`<rect class="borda" pathLength="1" x="${x0 + 0.5}" y="${y0 + 0.5}" width="${w - 1}" height="${h - 1}"/>`);
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.innerHTML = el.join("");
  }
  construirLinhas();
  function acenderLinhas() {
    const grupos = [1, 2, 3, 4, 5, 6, 7];
    grupos.forEach((g, i) =>
      setTimeout(() => $$(`[data-g="${g}"]`, svg).forEach((e) => e.classList.add("on")), reduzido ? 0 : 150 + i * 320)
    );
  }
  let timerResize;
  addEventListener("resize", () => {
    clearTimeout(timerResize);
    timerResize = setTimeout(() => { construirLinhas(); $$("[data-g]", svg).forEach((e) => e.classList.add("on")); medir(); }, 150);
  });

  // ---------- 4. Abertura ----------
  let introIni = 0;
  requestAnimationFrame(() => {
    body.dataset.iniciado = "true";
    acenderLinhas();
  });
  const t0 = performance.now();
  const primeira = !temGL ? Promise.resolve()
    : SEQ ? window.Cena.carregarSeq(urlsSeq).then((r) => { seqPronta = !!r; })
    : window.Cena.carregar(fotoDe(C.abertura));
  primeira.then(() => {
    const espera = Math.max(0, (reduzido ? 0 : 1800) - (performance.now() - t0));
    setTimeout(() => {
      body.dataset.carregado = "true";
      mostrarAbertura();
      introIni = performance.now();
    }, espera);
  });
  // pré-carrega as fotos dos capítulos sem travar a abertura
  if (temGL) setTimeout(() => C.capitulos.forEach((c) => window.Cena.carregar(fotoDe(c))), 2500);

  // ---------- 5. Medidas dos capítulos ----------
  const caps = $$(".capitulo").map((el, i) => ({
    el, i, dados: C.capitulos[i],
    heroi: $(".capitulo__heroi", el), nome: $(".capitulo__nome", el),
    destaques: $(".capitulo__destaques", el), cards: $(".capitulo__cards", el),
    top: 0, alt: 0, heroiAlt: 0,
  }));
  const linksLateral = $$(".lateral .indice a");
  function medir() {
    const y = scrollY;
    caps.forEach((c) => {
      const r = c.el.getBoundingClientRect();
      c.top = r.top + y; c.alt = r.height; c.heroiAlt = c.heroi.offsetHeight;
    });
  }
  medir();
  addEventListener("load", medir);
  new ResizeObserver(medir).observe($("#principal"));

  // ---------- 6. Revelações (cards/mídias entram suavemente) ----------
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("visivel"); io.unobserve(e.target); } }),
    { rootMargin: "0px 0px -10% 0px" }
  );
  $$(".revelar").forEach((e) => io.observe(e));

  // ---------- 7. Mouse (parallax sutil) ----------
  const mouse = { x: 0, y: 0, sx: 0, sy: 0 };
  addEventListener("pointermove", (e) => { mouse.x = e.clientX / innerWidth - 0.5; mouse.y = e.clientY / innerHeight - 0.5; });

  // ---------- 8. Laço principal: tudo que depende do scroll ----------
  let ultimoAtivo = -2, ultimoTema = "", ultimoTemaLat = "";
  const dentro = (el, y) => { if (!el) return false; const r = el.getBoundingClientRect(); return r.top <= y && r.bottom >= y; };

  function atualizar(agora) {
    const y = scrollY, vh = innerHeight;
    body.dataset.rolou = y > 20 ? "true" : "false";

    // capítulo cujo fundo aparece: entra assim que o topo passa de 85% da tela
    let ativo = -1;
    caps.forEach((c) => { if (c.top <= y + vh * 0.85) ativo = c.i; });
    // capítulo do índice lateral: meio da tela
    let ativoIndice = -1;
    caps.forEach((c) => { if (c.top <= y + vh * 0.5) ativoIndice = c.i; });

    if (ativo !== ultimoAtivo) {
      ultimoAtivo = ativo;
      if (body.dataset.carregado === "true") ativo >= 0 ? mostrarFoto(fotoDe(caps[ativo].dados)) : mostrarAbertura();
    }
    linksLateral.forEach((a, i) => a.classList.toggle("ativo", i === ativoIndice));

    // zoom lento da "câmera" + pan, guiados pelo progresso do capítulo
    let prog, veu = 0, escurecer = 0;
    if (ativo < 0) {
      prog = clamp(y / vh, 0, 1.5);
      if (seqPronta) {
        const altSeq = $(".espaco-abertura").offsetHeight - vh * 0.85;
        window.Cena.quadroSeq(y / altSeq);
        prog = 0;   // na sequência o movimento vem dos quadros, não do zoom
      }
    } else {
      const c = caps[ativo];
      prog = clamp((y + vh * 0.85 - c.top) / (c.heroiAlt + vh), 0, 1.6);
      // véu bege sobe quando os destaques entram e desce quando o capítulo acaba
      const rd = c.destaques.getBoundingClientRect();
      const fim = (c.cards || c.destaques).getBoundingClientRect();
      const sobe = clamp((vh - rd.top - vh * 0.15) / (vh * 0.7));
      const desce = clamp(fim.bottom / (vh * 0.6));
      veu = Math.min(sobe, desce);
      // escurece o fundo enquanto a frase passa por cima
      const rh = c.heroi.getBoundingClientRect();
      escurecer = clamp((vh * 0.6 - rh.top) / (vh * 0.8)) * (1 - veu);
      // nome gigante: sobe um pouco mais devagar e some depois da frase
      const p = clamp(-rh.top / c.heroiAlt, -1, 2);
      c.nome.style.transform = `translate3d(0, ${(p * 18).toFixed(2)}vh, 0)`;
      c.nome.style.opacity = (1 - clamp((p - 0.3) / 0.15)).toFixed(3);
    }
    mouse.sx += (mouse.x - mouse.sx) * 0.05; mouse.sy += (mouse.y - mouse.sy) * 0.05;
    const zoom = 1.06 + 0.12 * prog;
    const folga = (1 - 1 / zoom) / 2;           // não deixa o pan sair da foto
    S.zoom = zoom;
    S.pan = [clamp(mouse.sx * 0.03, -folga, folga), clamp(-0.03 * prog - mouse.sy * 0.02, -folga, folga)];
    S.veu = veu;
    S.escurecer = escurecer;
    S.intro = introIni ? clamp((agora - introIni) / 2200) : 0;

    if (!temGL) {
      const cam = camadas.get(fotoDe(ativo >= 0 ? caps[ativo].dados : C.abertura));
      if (cam) cam.style.transform = `scale(${zoom}) translate(${(-S.pan[0] * 100).toFixed(2)}%, ${(S.pan[1] * 100).toFixed(2)}%)`;
      fundoCSS.style.opacity = S.intro;
      veuCSS.style.transform = `scaleY(${veu})`;
    }

    // tema da nav (claro/escuro) conforme o que está atrás dela
    const temaEm = (py) => {
      for (const c of caps) {
        if (dentro(c.cards, py)) return "light";
        if (dentro(c.destaques, py) && veu > 0.6) return "light";
      }
      return "dark";
    };
    const tema = temaEm(30);
    if (tema !== ultimoTema) { html.dataset.navTheme = tema; ultimoTema = tema; }
    const temaLat = temaEm(vh - 160);
    if (temaLat !== ultimoTemaLat) { html.dataset.lateralTheme = temaLat; ultimoTemaLat = temaLat; }
  }

  function laco(agora) {
    if (lenis) lenis.raf(agora);
    atualizar(agora);
    window.Cena.quadro(agora);
    requestAnimationFrame(laco);
  }
  requestAnimationFrame(laco);
})();
