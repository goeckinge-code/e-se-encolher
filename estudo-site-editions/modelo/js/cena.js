/* =========================================================================
   CENA WebGL — fundo em tela cheia, fixo atrás do conteúdo.

   No original isto é Three.js + React Three Fiber + Theatre.js, com camadas
   recortadas de cada pintura em profundidade, câmera animada pelo scroll,
   partículas, borboletas e bloom. Aqui reproduzimos os mesmos efeitos com
   WebGL puro (sem dependências), a partir de UMA foto por capítulo:
     - "object-fit: cover" no shader
     - zoom lento + pan controlados pelo scroll (o "dolly" da câmera)
     - transição em "papel queimando": ruído fbm + borda brilhante (x6)
       — mesma técnica do shader de visibilidade do original
     - véu bege (#dcdcd0) que sobe com ruído quando entram os destaques
     - poeira/partículas com brilho suave (mesmo shader de pontos do original)
     - vinheta e grão de filme
   ========================================================================= */
(function () {
  const VERT = `
attribute vec2 aPos;
varying vec2 vUv;
void main(){ vUv = aPos * .5 + .5; gl_Position = vec4(aPos, 0., 1.); }`;

  const FRAG = `
precision highp float;
varying vec2 vUv;
uniform sampler2D uTexA, uTexB;
uniform float uAspA, uAspB, uZoomA, uZoomB, uMix, uTime, uVeu, uIntro, uEscurecer;
uniform vec2 uRes, uPanA, uPanB;
uniform vec3 uBege;

float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p){
  vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3. - 2. * f);
  return mix(mix(hash(i), hash(i + vec2(1., 0.)), u.x), mix(hash(i + vec2(0., 1.)), hash(i + vec2(1., 1.)), u.x), u.y);
}
float fbm(vec2 p){ float v = 0., a = .5; for (int i = 0; i < 5; i++) { v += a * noise(p); p *= 2.03; a *= .5; } return v; }

// object-fit: cover + zoom em torno do centro + pan
vec2 cover(vec2 uv, float imgAsp, float zoom, vec2 pan){
  float scr = uRes.x / uRes.y;
  vec2 r = vec2(min(scr / imgAsp, 1.), min(imgAsp / scr, 1.));
  uv = (uv - .5) / zoom + .5 + pan;
  return vec2(uv.x * r.x + (1. - r.x) * .5, uv.y * r.y + (1. - r.y) * .5);
}

// máscara de dissolução: 1 = revelado. "borda" = faixa que queima
float dissolve(float prog, float t, out float borda){
  float th = prog * 1.25 - .1, w = .045;
  borda = smoothstep(th - w, th, t) * (1. - smoothstep(th, th + w, t));
  return 1. - smoothstep(th - w, th, t);
}

void main(){
  vec2 p = vec2(vUv.x * uRes.x / uRes.y, vUv.y);
  float n = fbm(p * 2.2 + 3.1 + uTime * .015);
  float t = mix(n, length(vUv - .5) * 1.25, .35);

  vec3 a = texture2D(uTexA, cover(vUv, uAspA, uZoomA, uPanA)).rgb;
  vec3 b = texture2D(uTexB, cover(vUv, uAspB, uZoomB, uPanB)).rgb;

  float borda;
  float m = dissolve(uMix, t, borda);
  vec3 col = mix(a, b, m);
  col *= 1. + 5. * borda * step(.001, uMix) * step(uMix, .999);

  // revelação inicial (do preto)
  float bordaI;
  float mi = dissolve(uIntro, t, bordaI);
  col = mix(vec3(0.), col, mi) * (1. + 5. * bordaI * step(uIntro, .999));

  // escurece quando o texto passa por cima (legibilidade)
  col *= 1. - .35 * uEscurecer;

  // vinheta
  col *= mix(1., smoothstep(1.15, .25, length((vUv - .5) * vec2(1.1, 1.3))), .45);

  // véu bege que sobe de baixo com borda irregular
  float y = vUv.y + (fbm(p * 3. + 9.) - .5) * .18;
  float thV = uVeu * 1.3 - .15;
  float veu = 1. - smoothstep(thV - .04, thV, y);
  col = mix(col, uBege, veu);

  // grão de filme
  col += (hash(vUv * uRes + fract(uTime) * 91.7) - .5) * .035;

  gl_FragColor = vec4(col, 1.);
}`;

  // partículas (pontos com brilho suave — mesmo shader de pontos do original)
  const P_VERT = `
attribute vec3 aSeed;
uniform float uTime, uDpr;
varying float vAlpha;
void main(){
  float y = fract(aSeed.y + uTime * .012 * (.4 + aSeed.z));
  float x = fract(aSeed.x + sin(uTime * .15 + aSeed.z * 6.283) * .015);
  vAlpha = sin(3.1416 * y) * (.25 + .75 * aSeed.z);
  gl_PointSize = (1.5 + aSeed.z * aSeed.z * 9.) * uDpr;
  gl_Position = vec4(vec2(x, y) * 2. - 1., 0., 1.);
}`;
  const P_FRAG = `
precision mediump float;
uniform vec3 uColor;
uniform float uOpacity, uBlur;
varying float vAlpha;
void main(){
  vec2 c = gl_PointCoord * 2. - 1.;
  float d = 1. - min(1., length(c));
  float blur = 1. - pow(uBlur, 2.);
  gl_FragColor = vec4(uColor, uOpacity * smoothstep(0., blur, d) * vAlpha);
}`;

  let gl, prog, pprog, buf, pbuf, U = {}, PU = {}, canvas, dpr = 1;
  const N_PART = 140;
  const cache = new Map();          // url -> Promise<{tex, asp}>
  const vazio = { tex: null, asp: 1 };
  const S = {                       // estado controlado pelo app.js
    zoom: 1.04, pan: [0, 0], veu: 0, escurecer: 0, intro: 0,
  };
  let A = vazio, B = vazio, mix = 0, transIni = 0, urlAlvo = null, zoomA = 1.04, panA = [0, 0];
  const DUR_TRANS = 1600;

  function shader(tipo, src) {
    const s = gl.createShader(tipo); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  function programa(v, f, nomes) {
    const p = gl.createProgram();
    gl.attachShader(p, shader(gl.VERTEX_SHADER, v)); gl.attachShader(p, shader(gl.FRAGMENT_SHADER, f));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    const u = {}; nomes.forEach((n) => (u[n] = gl.getUniformLocation(p, n)));
    return [p, u];
  }

  function iniciar(cv) {
    canvas = cv;
    try {
      gl = cv.getContext("webgl", { antialias: false, alpha: false, powerPreference: "high-performance" });
      if (!gl) return false;
      [prog, U] = programa(VERT, FRAG, ["uTexA", "uTexB", "uAspA", "uAspB", "uZoomA", "uZoomB", "uMix", "uTime", "uVeu", "uIntro", "uEscurecer", "uRes", "uPanA", "uPanB", "uBege"]);
      [pprog, PU] = programa(P_VERT, P_FRAG, ["uTime", "uDpr", "uColor", "uOpacity", "uBlur"]);
    } catch (e) { console.warn("WebGL indisponível, usando fundo em CSS.", e); return false; }

    buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const seeds = new Float32Array(N_PART * 3);
    for (let i = 0; i < seeds.length; i++) seeds[i] = Math.random();
    pbuf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, pbuf); gl.bufferData(gl.ARRAY_BUFFER, seeds, gl.STATIC_DRAW);

    // textura preta 1x1 para começar
    const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([0, 0, 0, 255]));
    A = B = { tex: t, asp: 1 };

    redimensionar(); addEventListener("resize", redimensionar);
    return true;
  }

  function redimensionar() {
    dpr = Math.min(devicePixelRatio || 1, innerWidth < 768 ? 1.5 : 2);
    canvas.width = Math.round(innerWidth * dpr); canvas.height = Math.round(innerHeight * dpr);
  }

  function carregar(url) {
    if (!url) return Promise.resolve(null);
    if (cache.has(url)) return cache.get(url);
    const pr = new Promise((ok) => {
      const img = new Image(); img.decoding = "async";
      img.onload = () => {
        let fonte = img;
        const max = gl.getParameter(gl.MAX_TEXTURE_SIZE), lim = Math.min(max, 4096);
        if (img.width > lim || img.height > lim) {          // reduz fotos enormes
          const k = lim / Math.max(img.width, img.height), c = document.createElement("canvas");
          c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
          c.getContext("2d").drawImage(img, 0, 0, c.width, c.height); fonte = c;
        }
        const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, fonte);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        ok({ tex, asp: img.width / img.height });
      };
      img.onerror = () => { console.warn("Foto não encontrada:", url); ok(null); };
      img.src = url;
    });
    cache.set(url, pr);
    return pr;
  }

  // troca o fundo com a transição queimada
  function mostrar(url) {
    if (!url || url === urlAlvo) return;
    urlAlvo = url;
    carregar(url).then((t) => {
      if (!t || urlAlvo !== url) return;
      if (mix > 0) { A = B; zoomA = S.zoom; panA = S.pan.slice(); }  // transição anterior ainda rodando
      else { zoomA = S.zoom; panA = S.pan.slice(); }
      B = t; mix = 0.0001; transIni = performance.now();
    });
  }

  function quadro(agora) {
    if (!gl) return;
    if (mix > 0) {
      mix = Math.min(1, (agora - transIni) / DUR_TRANS);
      if (mix >= 1) { A = B; mix = 0; }
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.disable(gl.BLEND);
    gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    const loc = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, (mix > 0 ? A : B).tex);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, B.tex);
    gl.uniform1i(U.uTexA, 0); gl.uniform1i(U.uTexB, 1);
    gl.uniform1f(U.uAspA, (mix > 0 ? A : B).asp); gl.uniform1f(U.uAspB, B.asp);
    gl.uniform1f(U.uZoomA, mix > 0 ? zoomA : S.zoom); gl.uniform1f(U.uZoomB, S.zoom);
    gl.uniform2f(U.uPanA, ...(mix > 0 ? panA : S.pan)); gl.uniform2f(U.uPanB, ...S.pan);
    gl.uniform1f(U.uMix, mix);
    gl.uniform1f(U.uTime, agora / 1000);
    gl.uniform1f(U.uVeu, S.veu); gl.uniform1f(U.uIntro, S.intro); gl.uniform1f(U.uEscurecer, S.escurecer);
    gl.uniform2f(U.uRes, canvas.width, canvas.height);
    gl.uniform3f(U.uBege, 220 / 255, 220 / 255, 208 / 255);
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    // partículas
    const op = 0.55 * S.intro * (1 - S.veu);
    if (op > 0.01) {
      gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.useProgram(pprog);
      gl.bindBuffer(gl.ARRAY_BUFFER, pbuf);
      const l2 = gl.getAttribLocation(pprog, "aSeed");
      gl.enableVertexAttribArray(l2); gl.vertexAttribPointer(l2, 3, gl.FLOAT, false, 0, 0);
      gl.uniform1f(PU.uTime, agora / 1000); gl.uniform1f(PU.uDpr, dpr);
      gl.uniform3f(PU.uColor, 1, 0.9, 0.75); gl.uniform1f(PU.uOpacity, op); gl.uniform1f(PU.uBlur, 0.7);
      gl.drawArrays(gl.POINTS, 0, N_PART);
      gl.disableVertexAttribArray(l2);
    }
  }

  window.Cena = { iniciar, carregar, mostrar, quadro, estado: S };
})();
