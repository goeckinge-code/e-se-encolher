// Motor dos episódios do Caio: personagens, planos, câmera, legenda karaokê.
// Cada episódio (episodios/epNN-*.js) define LINES (narração com tempos) e chama shot(t0, t1, build).
let DUR = 30;   // o episódio pode mudar (ex.: DUR = 45)
let LINES = [];
// palavras com tempo proporcional ao tamanho; grupos de até 3 palavras (quebra na pontuação)
let WORDS = [], GROUPS = [];
function buildCaptions() {
  WORDS = []; GROUPS = [];
for (const [a, b, txt] of LINES) {
  const ws = txt.split(' '); const tot = ws.reduce((s, w) => s + w.length + 2, 0); let t = a;
  let grp = [];
  ws.forEach((w, i) => {
    const d = (b - a) * (w.length + 2) / tot; const W = { w, t0: t, t1: t + d }; t += d; WORDS.push(W); grp.push(W);
    if (grp.length === 3 || /[.,:?!”]$/.test(w) || i === ws.length - 1) { GROUPS.push(grp); grp = []; }
  });
}
for (let i = 0; i < GROUPS.length; i++) { const g = GROUPS[i]; g.t0 = g[0].t0; g.t1 = i + 1 < GROUPS.length ? Math.min(GROUPS[i + 1][0].t0, g[g.length - 1].t1 + .6) : DUR; }
}

// ------------------------------------------------------------------ personagens (design próprio)
const LOOK = {
  caio: { kid: 1, skin: SKIN.caio, shirt: '#f28c38', pocket: '#e0702a', shorts: '#3b5bb5', shoe: '#f5c531', hair: 'cap', hairCol: '#2a1c18', cap: '#e04a3f' },
  jair: { skin: SKIN.jair, shirt: '#f4f4f0', tank: 1, belly: 1, shorts: '#4f9a5a', chinelo: 1, hair: 'short', hairCol: '#3a2a22' },
  cida: { skin: SKIN.cida, shirt: '#e86fa0', dress: '#e86fa0', shoe: '#7a3fa0', hair: 'bun', hairCol: '#2a1a14' },
  avo: { skin: SKIN.avo, shirt: '#d8c39a', vest: 1, sleeveLong: 1, shorts: '#7a5a3e', longPants: 1, pants: '#7a5a3e', shoe: '#5a3d2a', hair: 'bald', glasses: 1, mustache: 1, sit: 1 },
  n1: { skin: SKIN.n1, shirt: '#5fb3e0', stripe: '#fff', shorts: '#6b4fa0', shoe: '#e04a3f', hair: 'short', hairCol: '#c8742c' },
  mae: { skin: '#a8693f', shirt: '#4fa3d1', dress: '#4fa3d1', shoe: '#e86fa0', hair: 'curly', hairCol: '#3a2418' },
  prof: { skin: '#e8b48c', shirt: '#7a5fc0', dress: '#7a5fc0', shoe: '#2b2745', hair: 'bun', hairCol: '#9a9aa6', glasses: 1 },
  carteiro: { skin: '#9a6440', shirt: '#f5c531', shorts: '#2f5f9a', shoe: '#2b2745', hair: 'short', hairCol: '#1c1412', mustache: 1 },
  sombra: { kid: 1, skin: '#3b3558', shirt: '#3b3558', pocket: '#3b3558', shorts: '#3b3558', shoe: '#3b3558', sole: '#3b3558', hair: 'cap', hairCol: '#3b3558', cap: '#3b3558', noCheeks: 1 },
  n2: { skin: SKIN.n2, shirt: '#9ccc4e', shorts: '#3b3b55', shoe: '#fff', hair: 'curly', hairCol: '#1c1412' },
};
let UID = 0;
function mk(look, extra = {}) { const id = 'c' + (UID++); const r = char(id, { ...LOOK[look], ...extra }); regChar(id, r.geo); return { id, svg: r.svg, geo: r.geo }; }

const SHOTS = [];
function shot(t0, t1, build) { SHOTS.push({ t0, t1, build }); }
const POCKET = (ch, x, y, s) => [x + ch.geo.tw * .25 * s, y + (ch.geo.torsoBot - 30) * s];

// ------------------------------------------------------------------ montagem do SVG e render(t)
function captionSvg() {
  return `<g id="cap" font-family="Poppins" font-weight="800" font-size="72" text-anchor="middle"><text id="capT" x="540" y="1660" fill="#fff" stroke="${OL}" stroke-width="14" paint-order="stroke" stroke-linejoin="round" filter="url(#shadow)"></text></g>`;
}
function setup() {
  const root = $('stage');
  let html = `<defs>
    <filter id="mb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur id="mbg" stdDeviation="0 0"/></filter>
    <filter id="shadow" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="0" flood-color="#2b2745" flood-opacity=".8"/></filter>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/></filter>
    <radialGradient id="vig" cx="50%" cy="48%" r="75%"><stop offset="55%" stop-color="#2b2745" stop-opacity="0"/><stop offset="100%" stop-color="#2b2745" stop-opacity=".32"/></radialGradient>
  </defs>`;
  SHOTS.forEach((s, i) => { const b = s.build(); s.b = b; html += `<g id="shot${i}" display="none"><g id="cam${i}">${b.svg}</g></g>`; });
  html += `<rect width="1080" height="1920" filter="url(#grain)" opacity=".07" style="mix-blend-mode:multiply"/><rect width="1080" height="1920" fill="url(#vig)"/>` + captionSvg();
  root.innerHTML = html;
}
function render(t) {
  SHOTS.forEach((s, i) => {
    const on = t >= s.t0 && (t < s.t1 || (i === SHOTS.length - 1 && t >= s.t1));
    const g = $('shot' + i); g.setAttribute('display', on ? 'inline' : 'none');
    if (!on) return;
    const lt = t - s.t0;
    s.b.update(lt);
    const c = s.b.cam ? s.b.cam(lt) : { s: 1, fx: 540, fy: 960 };
    $('cam' + i).setAttribute('transform', `translate(${(c.tx || 0)},0) translate(${c.fx},${c.fy}) scale(${c.s}) translate(${-c.fx},${-c.fy})`);
    if (c.blur) { $('mbg').setAttribute('stdDeviation', c.blurX ? `${c.blur} 0` : `${c.blur} ${c.blur}`); g.setAttribute('filter', 'url(#mb)'); }
    else g.removeAttribute('filter');
  });
  // legenda karaokê: grupo atual, palavra falada em amarelo
  const g = GROUPS.find(g => t >= g.t0 && t < g.t1);
  const T = $('capT');
  if (!g) { T.textContent = ''; return; }
  T.innerHTML = g.map(w => `<tspan fill="${t >= w.t0 && t < w.t1 + .05 ? '#f5c531' : '#fff'}">${w.w.replace(/&/g, '&amp;')}</tspan>`).join(' ');
  const k = backOut((t - g.t0) / .18, 1.6);
  T.setAttribute('transform', `translate(540,1640) scale(${k}) translate(-540,-1640)`);
}
window.addEventListener('load', () => { buildCaptions(); setup(); render(0); window.READY = true; });
window.render = render;
