/* Monta o HTML a partir do conteudo.js. Não precisa mexer aqui para trocar fotos/textos. */
(function () {
  const C = window.CONTEUDO;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"];

  // Título: "Cole{çã}o" -> Cole<span class="script">çã</span>o
  function tituloHTML(linhas) {
    return linhas
      .map((l, i) => {
        const partes = esc(l).replace(/\{([^}]*)\}/g, '<span class="titulo__script">$1</span>');
        return `<span class="titulo__linha" style="--i:${i}">${partes}</span>`;
      })
      .join("");
  }

  function midiaHTML(src, extra = "") {
    if (!src) return "";
    if (/\.(mp4|webm)$/i.test(src))
      return `<video class="midia ${extra}" src="${esc(src)}" autoplay muted loop playsinline></video>`;
    return `<img class="midia ${extra}" src="${esc(src)}" alt="" loading="lazy" decoding="async" />`;
  }

  function linkHTML(link, claro) {
    if (!link) return "";
    return `<a class="cta-link ${claro ? "cta-link--claro" : ""}" href="${esc(link.url)}">
      <span>${esc(link.texto)}</span><i aria-hidden="true">↗</i></a>`;
  }

  // ---- nav / marca
  $$("[data-marca-nome]").forEach((e) => (e.textContent = C.marca.nome));
  $$("[data-marca-edicao]").forEach((e) => (e.textContent = C.marca.edicao));
  $$("[data-link-site]").forEach((e) => { e.textContent = C.marca.linkSite.texto; e.href = C.marca.linkSite.url; });
  $$("[data-cta]").forEach((e) => { e.textContent = C.marca.cta.texto; e.href = C.marca.cta.url; });
  $$("[data-titulo]").forEach((e) => (e.innerHTML = tituloHTML(C.abertura.titulo)));
  $$("[data-subtitulo]").forEach((e) => (e.textContent = C.abertura.subtitulo));
  $$("[data-legal]").forEach((e) => (e.innerHTML = C.rodape.links.map((l) => `<a href="${esc(l.url)}">${esc(l.texto)}</a>`).join("<br>")));

  // ---- índice com numeração romana
  const itens = C.capitulos
    .map((c, i) => `<li style="--i:${i}"><a href="#${esc(c.id)}" data-ir="${i}"><span>${esc(c.nome)}</span><em>${ROMANOS[i] || i + 1}</em></a></li>`)
    .join("");
  $$("[data-indice]").forEach((e) => (e.innerHTML = itens));

  // ---- capítulos
  const main = $("#principal");
  C.capitulos.forEach((c, i) => {
    const destaques = (c.destaques || [])
      .map(
        (d, j) => `
      <article class="destaque ${j % 2 ? "destaque--inverso" : ""} revelar">
        <div class="destaque__texto">
          <h3 class="headline-4">${esc(d.titulo)}</h3>
          <p class="narrativa-3">${esc(d.texto)}</p>
          ${linkHTML(d.link)}
        </div>
        <div class="destaque__midia">${midiaHTML(d.midia)}</div>
      </article>`
      )
      .join("");

    const cards = (c.cards || [])
      .map(
        (k) => `
      <article class="card ${k.midia ? "card--midia" : "card--lista"} revelar">
        ${k.midia ? `<div class="card__midia">${midiaHTML(k.midia)}</div>` : ""}
        <h3 class="bodycopy-1">${esc(k.titulo)}</h3>
        <div class="card__corpo">
          <p class="bodycopy-1 texto-cinza">${esc(k.texto)}</p>
          ${linkHTML(k.link)}
        </div>
      </article>`
      )
      .join("");

    const teaser = c.teaser
      ? `<div class="teaser revelar">${midiaHTML(c.teaser.midia)}${c.teaser.video ? '<span class="teaser__play" aria-hidden="true"></span>' : ""}</div>`
      : "";

    const sec = document.createElement("section");
    sec.className = "capitulo";
    sec.id = c.id;
    sec.dataset.indice = i;
    sec.innerHTML = `
      <div class="capitulo__heroi" data-nav-theme="dark">
        <h2 class="headline-1 capitulo__nome"><span>${esc(c.nome)}</span></h2>
        <div class="capitulo__intro">
          <p class="narrativa-1 capitular">${esc(c.frase)}</p>
          ${teaser}
        </div>
      </div>
      <div class="capitulo__destaques" data-nav-theme="light">
        ${c.subtitulo ? `<h3 class="narrativa-1 capitular subtitulo-secao revelar">${esc(c.subtitulo)}</h3>` : ""}
        ${destaques}
      </div>
      ${cards ? `<div class="capitulo__cards" data-nav-theme="light"><div class="grade">${cards}</div></div>` : ""}
    `;
    main.appendChild(sec);
  });

  // ---- rodapé
  $("#rodape").innerHTML = `
    <p class="headline-2">${esc(C.rodape.frase)}</p>
    <div class="rodape__base bodycopy-2">
      <span>© ${new Date().getFullYear()} ${esc(C.marca.nome)}</span>
      ${C.rodape.links.map((l) => `<a href="${esc(l.url)}">${esc(l.texto)}</a>`).join("")}
    </div>`;
})();
