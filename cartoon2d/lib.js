// Biblioteca de desenho: personagens "adesivo" (cabeçona, contorno grosso), cenário plano e interface de dinheiro.
// Tudo em SVG, coordenadas 1080x1920. Animação é função pura do tempo (ver anim.js).
const OL = '#2b2745';          // cor do contorno
const SW = 8;                  // espessura do contorno
const SKIN = { caio: '#b9774e', jair: '#e0a27a', cida: '#8a5636', avo: '#c98b62', n1: '#f0c09a', n2: '#6e4529' };

const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const easeOut = t => 1 - Math.pow(1 - clamp(t), 3);
const easeInOut = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const backOut = (t, s = 2.2) => { t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1; };
const pop = (lt, t0, d = .28) => lt < t0 ? 0 : backOut((lt - t0) / d);
const brl = v => 'R$ ' + Math.round(v).toLocaleString('pt-BR') + (v < 1000 ? ',00' : '');

// ------------------------------------------------------------------ personagem
// o: {kid, skin, shirt, stripe, shorts, shoe, hair, hairCol, cap, belly, tank, dress, glasses, mustache, sit, pocket}
function char(id, o) {
  const kid = !!o.kid;
  const R = kid ? 128 : 112;                   // raio da cabeça
  const shoeH = 40, legLen = o.sit ? 60 : (kid ? 118 : 168);
  const torsoH = kid ? 150 : 195;
  const tw = o.belly ? 236 : (kid ? 168 : 182); // largura do tronco
  const hipY = -(shoeH + legLen);
  const torsoBot = hipY + 30, torsoTop = torsoBot - torsoH;
  const shY = torsoTop + 34;
  const hy = torsoTop - R + 30;               // centro da cabeça
  const sk = o.skin;
  const P = [];
  P.push(`<ellipse cx="0" cy="4" rx="${tw * .62}" ry="20" fill="rgba(40,30,60,.18)"/>`);
  P.push(`<g id="${id}-body">`);
  // pernas + sapatos
  for (const s of [-1, 1]) {
    const lx = s * (kid ? 34 : 40);
    P.push(`<g id="${id}-leg${s > 0 ? 'L' : 'R'}">`);
    P.push(`<rect x="${lx - 19}" y="${hipY - 10}" width="38" height="${legLen + 20}" rx="18" fill="${o.pants || sk}" stroke="${OL}" stroke-width="${SW}"/>`);
    if (o.chinelo) {
      P.push(`<rect x="${lx - 30}" y="${-16}" width="60" height="16" rx="8" fill="#3f8fd6" stroke="${OL}" stroke-width="${SW}"/>`);
      P.push(`<rect x="${lx - 22}" y="${-34}" width="44" height="22" rx="11" fill="${sk}" stroke="${OL}" stroke-width="${SW}"/>`);
    } else {
      P.push(`<path d="M${lx - 30},0 L${lx - 30},${-shoeH + 12} Q${lx - 30},${-shoeH} ${lx - 14},${-shoeH} L${lx + 16},${-shoeH} Q${lx + 34},${-shoeH} ${lx + 34},${-shoeH + 18} L${lx + 34},0 Z" fill="${o.shoe || '#e04a3f'}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
      P.push(`<rect x="${lx - 30}" y="-12" width="64" height="10" fill="${o.sole || '#fff'}" stroke="${OL}" stroke-width="5"/>`);
    }
    P.push(`</g>`);
  }
  // bermuda / calça / vestido
  if (o.dress) {
    P.push(`<path d="M${-tw / 2 + 6},${torsoTop + 20} L${tw / 2 - 6},${torsoTop + 20} L${tw / 2 + 34},${hipY + 70} Q0,${hipY + 86} ${-tw / 2 - 34},${hipY + 70} Z" fill="${o.dress}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
    for (let i = 0; i < 9; i++) { const dx = ((i * 53) % 190) - 95, dy = torsoTop + 60 + ((i * 37) % 150); P.push(`<circle cx="${dx}" cy="${dy}" r="7" fill="#fff" opacity=".85"/>`); }
  } else {
    P.push(`<path d="M${-tw / 2 + 4},${hipY - 40} L${tw / 2 - 4},${hipY - 40} L${tw / 2 + 2},${hipY + (o.longPants ? 0 : 52)} L8,${hipY + (o.longPants ? 0 : 52)} L0,${hipY + 10} L-8,${hipY + (o.longPants ? 0 : 52)} L${-tw / 2 - 2},${hipY + (o.longPants ? 0 : 52)} Z" fill="${o.shorts}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
  }
  // braços (atrás do tronco no ombro) — pivô no ombro
  const arm = (side) => {
    const sx = side * (tw / 2 - 6), len = kid ? 128 : 150, wdt = o.tank || o.belly ? 40 : 38;
    const sleeve = o.tank ? '' : `<rect x="${sx - 26}" y="${shY - 18}" width="52" height="64" rx="24" fill="${o.shirt}" stroke="${OL}" stroke-width="${SW}"/>`;
    return `<g id="${id}-arm${side > 0 ? 'L' : 'R'}"><rect x="${sx - wdt / 2}" y="${shY - 8}" width="${wdt}" height="${len}" rx="${wdt / 2}" fill="${o.sleeveLong ? o.shirt : sk}" stroke="${OL}" stroke-width="${SW}"/>${sleeve}<circle cx="${sx}" cy="${shY + len}" r="${kid ? 25 : 27}" fill="${o.glove || sk}" stroke="${OL}" stroke-width="${SW}"/></g>`;
  };
  P.push(arm(-1), arm(1));
  // tronco
  if (!o.dress) {
    const bw = o.belly ? 40 : 0;
    P.push(`<path d="M${-tw / 2},${torsoTop + 30} Q${-tw / 2},${torsoTop} ${-tw / 2 + 30},${torsoTop} L${tw / 2 - 30},${torsoTop} Q${tw / 2},${torsoTop} ${tw / 2},${torsoTop + 30} L${tw / 2 + bw},${torsoBot - 40} Q${tw / 2 + bw},${torsoBot} ${tw / 2 - 30},${torsoBot} L${-tw / 2 + 30},${torsoBot} Q${-tw / 2 - bw},${torsoBot} ${-tw / 2 - bw},${torsoBot - 40} Z" fill="${o.shirt}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
    if (o.tank) P.push(`<path d="M${-tw / 2 + 20},${torsoTop} Q0,${torsoTop + 60} ${tw / 2 - 20},${torsoTop}" fill="${sk}" stroke="${OL}" stroke-width="${SW}"/>`);
    if (o.stripe) for (let i = 0; i < 3; i++) P.push(`<rect x="${-tw / 2 + 5}" y="${torsoTop + 40 + i * 38}" width="${tw - 10}" height="16" fill="${o.stripe}"/>`);
    if (o.pocket) P.push(`<rect x="${tw / 2 - 66}" y="${torsoTop + 46}" width="38" height="40" rx="6" fill="${o.pocket}" stroke="${OL}" stroke-width="5"/>`);
    if (o.vest) P.push(`<path d="M${-tw / 2 + 2},${torsoTop + 20} L-18,${torsoTop + 90} L-18,${torsoBot - 4} M${tw / 2 - 2},${torsoTop + 20} L18,${torsoTop + 90} L18,${torsoBot - 4}" fill="none" stroke="${OL}" stroke-width="6"/><circle cx="0" cy="${torsoTop + 120}" r="6" fill="${OL}"/><circle cx="0" cy="${torsoTop + 160}" r="6" fill="${OL}"/>`);
    P.push(`<path d="M-30,${torsoTop + 2} Q0,${torsoTop + 26} 30,${torsoTop + 2}" fill="none" stroke="${OL}" stroke-width="6" stroke-linecap="round"/>`);
  }
  if (o.sit) P.push(`<rect x="${-tw / 2 - 6}" y="${hipY - 46}" width="${tw + 12}" height="60" rx="28" fill="${o.shorts}" stroke="${OL}" stroke-width="${SW}"/>`);
  // cabeça
  P.push(`<g id="${id}-head">`);
  for (const s of [-1, 1]) P.push(`<circle cx="${s * (R - 4)}" cy="${hy + 10}" r="26" fill="${sk}" stroke="${OL}" stroke-width="${SW}"/>`);
  // cabelo de trás
  if (o.hair === 'bun') P.push(`<circle cx="0" cy="${hy - R - 22}" r="46" fill="${o.hairCol}" stroke="${OL}" stroke-width="${SW}"/><path d="M${-R - 14},${hy + 40} Q${-R - 30},${hy - R - 10} 0,${hy - R - 8} Q${R + 30},${hy - R - 10} ${R + 14},${hy + 40} Z" fill="${o.hairCol}" stroke="${OL}" stroke-width="${SW}"/>`);
  if (o.hair === 'curly') { for (let i = 0; i < 9; i++) { const a = Math.PI * (1.05 + i * .1); P.push(`<circle cx="${Math.cos(a) * R * .95}" cy="${hy + Math.sin(a) * R * .95}" r="40" fill="${o.hairCol}" stroke="${OL}" stroke-width="${SW}"/>`); } }
  P.push(`<circle cx="0" cy="${hy}" r="${R}" fill="${sk}" stroke="${OL}" stroke-width="${SW}"/>`);
  // cabelo / boné da frente
  if (o.hair === 'cap') {
    for (const s of [-1, 1]) P.push(`<circle cx="${s * (R - 18)}" cy="${hy - 30}" r="26" fill="${o.hairCol}" stroke="${OL}" stroke-width="6"/>`);
    P.push(`<g id="${id}-cap"><path d="M${-R - 6},${hy - 30} Q${-R + 4},${hy - R - 34} 0,${hy - R - 30} Q${R - 4},${hy - R - 34} ${R + 6},${hy - 30} Z" fill="${o.cap}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>
      <path d="M${R - 10},${hy - 44} Q${R + 70},${hy - 52} ${R + 92},${hy - 30} Q${R + 40},${hy - 22} ${R - 6},${hy - 26} Z" fill="${o.cap}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>
      <circle cx="0" cy="${hy - R - 28}" r="10" fill="${o.cap}" stroke="${OL}" stroke-width="6"/><path d="M-40,${hy - R + 6} Q0,${hy - R - 12} 40,${hy - R + 6}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="7" stroke-linecap="round"/></g>`);
  } else if (o.hair === 'short') {
    P.push(`<path d="M${-R + 4},${hy - 20} Q${-R + 8},${hy - R - 12} 0,${hy - R - 6} Q${R - 8},${hy - R - 12} ${R - 4},${hy - 20} Q${R - 30},${hy - 70} 0,${hy - 76} Q${-R + 30},${hy - 70} ${-R + 4},${hy - 20} Z" fill="${o.hairCol}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
  } else if (o.hair === 'bun' || o.hair === 'curly') {
    P.push(`<path d="M${-R + 2},${hy - 10} Q${-R + 10},${hy - R - 14} 0,${hy - R - 8} Q${R - 10},${hy - R - 14} ${R - 2},${hy - 10} Q${R - 30},${hy - 104} 0,${hy - 100} Q${-R + 30},${hy - 104} ${-R + 2},${hy - 10} Z" fill="${o.hairCol}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`);
    P.push(`<path d="M-50,${hy - R + 14} Q-20,${hy - R + 2} 0,${hy - R + 12}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="7" stroke-linecap="round"/>`);
  } else if (o.hair === 'bald') {
    for (const s of [-1, 1]) P.push(`<path d="M${s * (R - 4)},${hy + 4} q${s * 26},-30 ${s * 2},-62 q${s * -18},10 ${s * -22},30 Z" fill="#f2f2f2" stroke="${OL}" stroke-width="6"/>`);
    P.push(`<path d="M-30,${hy - R + 26} Q0,${hy - R + 12} 30,${hy - R + 26}" fill="none" stroke="rgba(255,255,255,.45)" stroke-width="8" stroke-linecap="round"/>`);
  }
  // rosto
  const ex = kid ? 46 : 40, ey = hy - 4, erx = kid ? 31 : 26, ery = kid ? 37 : 31;
  P.push(`<g id="${id}-eyes">`);
  for (const s of [-1, 1]) {
    P.push(`<g id="${id}-eye${s > 0 ? 'L' : 'R'}"><ellipse cx="${s * ex}" cy="${ey}" rx="${erx}" ry="${ery}" fill="#fff" stroke="${OL}" stroke-width="7"/>
      <g class="pup"><circle cx="${s * ex}" cy="${ey + 4}" r="${erx * .66}" fill="#5b3a1e"/><circle cx="${s * ex}" cy="${ey + 4}" r="${erx * .34}" fill="#1b1420"/><circle cx="${s * ex + 7}" cy="${ey - 5}" r="${erx * .24}" fill="#fff"/></g>
      <path class="lid" d="M${s * ex - erx - 3},${ey} A${erx + 3},${ery + 3} 0 0 1 ${s * ex + erx + 3},${ey} Z" fill="${sk}" stroke="${OL}" stroke-width="7" display="none"/>
      <path class="happy" d="M${s * ex - erx + 4},${ey + 8} Q${s * ex},${ey - 26} ${s * ex + erx - 4},${ey + 8}" fill="none" stroke="${OL}" stroke-width="9" stroke-linecap="round" display="none"/>
      <text class="money" x="${s * ex}" y="${ey + 18}" text-anchor="middle" font-family="Luckiest" font-size="${erx * 1.6}" fill="#2fae60" stroke="${OL}" stroke-width="4" paint-order="stroke" display="none">$</text></g>`);
  }
  P.push(`</g>`);
  if (o.glasses) for (const s of [-1, 1]) P.push(`<circle cx="${s * ex}" cy="${ey}" r="${erx + 10}" fill="rgba(200,230,255,.18)" stroke="${OL}" stroke-width="6"/>`);
  if (o.glasses) P.push(`<path d="M${-ex + erx + 10},${ey - 4} Q0,${ey - 14} ${ex - erx - 10},${ey - 4}" fill="none" stroke="${OL}" stroke-width="6"/>`);
  for (const s of [-1, 1]) P.push(`<path id="${id}-brow${s > 0 ? 'L' : 'R'}" d="M${s * ex - 22},${ey - ery - 16} Q${s * ex},${ey - ery - 28} ${s * ex + 22},${ey - ery - 16}" fill="none" stroke="${OL}" stroke-width="9" stroke-linecap="round"/>`);
  if (!o.noCheeks) for (const s of [-1, 1]) P.push(`<ellipse cx="${s * (ex + 30)}" cy="${ey + 44}" rx="22" ry="12" fill="#ff8f9a" opacity=".55"/>`);
  P.push(`<g id="${id}-shades" display="none">${[-1, 1].map(s => `<rect x="${s * ex - erx - 6}" y="${ey - 22}" width="${2 * erx + 12}" height="44" rx="16" fill="#1b1730" stroke="${OL}" stroke-width="6"/><path d="M${s * ex - erx + 4},${ey - 10} l18,0" stroke="#fff" stroke-width="6" opacity=".6"/>`).join('')}<path d="M${-ex + erx + 6},${ey - 8} L${ex - erx - 6},${ey - 8}" stroke="#1b1730" stroke-width="8"/></g>`);
  P.push(`<path d="M-8,${ey + 36} Q0,${ey + 44} 8,${ey + 36}" fill="none" stroke="${OL}" stroke-width="6" stroke-linecap="round"/>`);
  // bocas
  const my = hy + (kid ? 62 : 56);
  P.push(`<g id="${id}-mouths">
    <g data-m="smile"><path d="M-36,${my - 8} Q0,${my + 52} 36,${my - 8} Z" fill="#5a1f2b" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/><rect x="-14" y="${my - 8}" width="12" height="14" fill="#fff"/><rect x="2" y="${my - 8}" width="12" height="14" fill="#fff"/><ellipse cx="0" cy="${my + 24}" rx="16" ry="8" fill="#ff7a8a"/></g>
    <g data-m="talk"><path d="M-24,${my - 4} Q0,${my + 26} 24,${my - 4} Z" fill="#5a1f2b" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/></g>
    <g data-m="o"><ellipse cx="0" cy="${my + 8}" rx="17" ry="22" fill="#5a1f2b" stroke="${OL}" stroke-width="7"/></g>
    <g data-m="O"><ellipse cx="0" cy="${my + 16}" rx="30" ry="40" fill="#5a1f2b" stroke="${OL}" stroke-width="7"/><ellipse cx="0" cy="${my + 38}" rx="18" ry="9" fill="#ff7a8a"/></g>
    <g data-m="shout"><path d="M-28,${my - 6} L28,${my - 6} L46,${my + 50} L-46,${my + 50} Z" fill="#5a1f2b" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/><rect x="-26" y="${my - 4}" width="52" height="11" fill="#fff"/><path d="M-30,${my + 50} Q0,${my + 30} 30,${my + 50} Z" fill="#ff7a8a"/></g>
    <g data-m="flat"><path d="M-22,${my + 6} L22,${my + 6}" stroke="${OL}" stroke-width="8" stroke-linecap="round"/></g>
    <g data-m="frown"><path d="M-26,${my + 16} Q0,${my - 6} 26,${my + 16}" fill="none" stroke="${OL}" stroke-width="8" stroke-linecap="round"/></g>
    <g data-m="smug"><path d="M-28,${my} Q0,${my + 22} 28,${my}" fill="none" stroke="${OL}" stroke-width="8" stroke-linecap="round"/></g>
    <g data-m="yuck"><path d="M-26,${my + 10} Q-12,${my} 0,${my + 10} Q12,${my + 20} 26,${my + 10}" fill="none" stroke="${OL}" stroke-width="8" stroke-linecap="round"/><path d="M4,${my + 12} q10,26 22,2" fill="#ff7a8a" stroke="${OL}" stroke-width="6"/></g>
  </g>`);
  if (o.mustache) P.push(`<path d="M-50,${my - 8} Q-26,${my - 30} 0,${my - 14} Q26,${my - 30} 50,${my - 8} Q26,${my - 2} 0,${my - 10} Q-26,${my - 2} -50,${my - 8} Z" fill="#f4f4f4" stroke="${OL}" stroke-width="6"/>`);
  // suor e lágrimas
  P.push(`<g id="${id}-sweat" display="none"><path d="M${R - 10},${hy - 60} q14,22 0,34 q-14,-12 0,-34 Z" fill="#8fd3ff" stroke="${OL}" stroke-width="5"/><path d="M${-R + 6},${hy - 30} q12,18 0,28 q-12,-10 0,-28 Z" fill="#8fd3ff" stroke="${OL}" stroke-width="5"/></g>`);
  P.push(`<g id="${id}-tears" display="none">${[-1, 1].map(s => `<path d="M${s * ex - 8},${ey + ery - 4} L${s * ex + 8},${ey + ery - 4} L${s * ex + 10},${ey + 120} Q${s * ex},${ey + 132} ${s * ex - 10},${ey + 120} Z" fill="#7cc6ff" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`);
  P.push(`<g id="${id}-mad" display="none" transform="translate(${R * .62},${hy - R * .72})">${[0, 90, 180, 270].map(r => `<path d="M8,-30 Q8,-8 30,-8" fill="none" stroke="#e8453c" stroke-width="11" stroke-linecap="round" transform="rotate(${r})"/>`).join('')}</g>`);
  P.push(`</g></g>`);
  const g = `<g id="${id}">${P.join('')}</g>`;
  return { svg: g, geo: { R, hy, shY, tw, torsoTop, torsoBot, hipY, kid, ex, ey } };
}

// estado do personagem a cada quadro
const C = {};
function regChar(id, geo) { C[id] = geo; }
function setChar(id, st) {
  const g = C[id]; if (!g) return;
  const t = st.t || 0;
  const el = $(id);
  const s = st.scale || 1;
  el.setAttribute('transform', `translate(${st.x},${st.y}) scale(${(st.flip ? -1 : 1) * s},${s})`);
  // respiração (squash leve a partir dos pés) + pulinho
  const br = Math.sin(t * 3.2 + (st.seed || 0)) * .012;
  const hop = st.hop ? -Math.abs(Math.sin(t * st.hop * Math.PI)) * 26 : 0;
  const wb = st.walk ? -Math.abs(Math.sin(t * st.walk * Math.PI * 2)) * 12 : 0;
  $(id + '-body').setAttribute('transform', `rotate(${st.lean || 0},0,0) translate(0,${hop + wb}) scale(${1 - br - (st.squash || 0) * .5},${1 + br + (st.squash || 0)})`);
  // cabeça
  const tilt = (st.tilt || 0) + Math.sin(t * 1.7 + (st.seed || 0)) * 1.2;
  $(id + '-head').setAttribute('transform', `rotate(${tilt},0,${g.torsoTop}) translate(0,${st.headY || 0})`);
  // braços: ângulos (graus) a partir de "pendurado"; positivo abre para fora
  const sx = g.tw / 2 - 6;
  const sw = st.walk ? Math.sin(t * st.walk * Math.PI * 2) * 14 : Math.sin(t * 2.1 + (st.seed || 0)) * 2;
  // braços: ângulo + esticar (armRlen/armLlen = fator de comprimento, efeito borracha)
  const stretch = (k, x) => k && k !== 1 ? ` translate(${x},${g.shY}) scale(${Math.pow(k, -.12)},${k}) translate(${-x},${-g.shY})` : '';
  $(id + '-armR').setAttribute('transform', `rotate(${(st.armR ?? 8) + sw},${-sx},${g.shY})${stretch(st.armRlen, -sx)}`);
  $(id + '-armL').setAttribute('transform', `rotate(${-((st.armL ?? 8) + sw)},${sx},${g.shY})${stretch(st.armLlen, sx)}`);
  // pernas (caminhada)
  const lx = g.kid ? 34 : 40;
  if (st.walk) {
    const w = Math.sin(t * st.walk * Math.PI * 2);
    $(id + '-legL').setAttribute('transform', `rotate(${w * 16},${lx},${g.hipY}) translate(0,${Math.min(0, w) * 8})`);
    $(id + '-legR').setAttribute('transform', `rotate(${-w * 16},${-lx},${g.hipY}) translate(0,${Math.min(0, -w) * 8})`);
  } else if (st.legL || st.legLlen) {   // chute: perna da direita da tela gira para fora e estica
    const k = st.legLlen || 1;
    $(id + '-legL').setAttribute('transform', `rotate(${-(st.legL || 0)},${lx},${g.hipY}) translate(${lx},${g.hipY}) scale(${Math.pow(k, -.12)},${k}) translate(${-lx},${-g.hipY})`);
    $(id + '-legR').removeAttribute('transform');
  } else { $(id + '-legL').removeAttribute('transform'); $(id + '-legR').removeAttribute('transform'); }
  // olhos: piscar + tipo
  const eyes = st.eyes || 'open';
  const ph = ((t + (st.seed || 0) * .7) % 2.9);
  const blk = eyes === 'happy' ? 1 : (ph < .14 ? .1 + .9 * Math.abs(ph - .07) / .07 : 1);
  const bl = blk < .999;
  const k = eyes === 'wide' ? 1.25 : 1;
  for (const e of ['eyeL', 'eyeR']) {
    const ee = $(id + '-' + e);
    const cy = g.ey;
    ee.setAttribute('transform', `translate(0,${cy}) scale(${k},${bl ? Math.max(.08, blk) * k : k}) translate(0,${-cy})`);
    ee.querySelector('.lid').setAttribute('display', eyes === 'half' ? 'inline' : 'none');
    ee.querySelector('.happy').setAttribute('display', eyes === 'happy' ? 'inline' : 'none');
    ee.querySelector('ellipse').setAttribute('display', eyes === 'happy' ? 'none' : 'inline');
    ee.querySelector('.pup').setAttribute('display', eyes === 'happy' || eyes === 'money' ? 'none' : 'inline');
    ee.querySelector('.money').setAttribute('display', eyes === 'money' ? 'inline' : 'none');
    ee.querySelector('.pup').setAttribute('transform', `translate(${st.lookX || 0},${st.lookY || 0})`);
  }
  // sobrancelhas
  const bt = st.brow || 0;   // -1 brava, +1 surpresa
  $(id + '-browL').setAttribute('transform', `translate(0,${-bt * 10 - (bt < 0 ? 4 : 0)}) rotate(${bt < 0 ? bt * 24 : 0},${g.ex},${g.ey - 50})`);
  $(id + '-browR').setAttribute('transform', `translate(0,${-bt * 10 - (bt < 0 ? 4 : 0)}) rotate(${bt < 0 ? -bt * 24 : 0},${-g.ex},${g.ey - 50})`);
  // boca (fala alterna entre a forma e "talk")
  let m = st.mouth || 'smug';
  if (st.talk) {
    const o = Math.sin(t * 23 + (st.seed || 0)) * Math.sin(t * 7.1) > -.15;
    if (!o) m = (m === 'shout' || m === 'O') ? 'o' : (m === 'smile' ? 'talk' : 'flat');
  }
  for (const n of $(id + '-mouths').children) n.setAttribute('display', n.dataset.m === m ? 'inline' : 'none');
  $(id + '-sweat').setAttribute('display', st.sweat ? 'inline' : 'none');
  if (st.sweat) $(id + '-sweat').setAttribute('transform', `translate(0,${(t * 90) % 40})`);
  $(id + '-tears').setAttribute('display', st.tears ? 'inline' : 'none');
  $(id + '-shades').setAttribute('display', st.shades ? 'inline' : 'none');
  const md = $(id + '-mad'); md.setAttribute('display', st.mad ? 'inline' : 'none');
  if (st.mad) md.setAttribute('transform', `translate(${g.R * .62},${g.hy - g.R * .72}) scale(${1 + Math.abs(Math.sin(t * 9)) * .25})`);
  const cap = $(id + '-cap');
  if (cap) cap.setAttribute('transform', `translate(0,${-(st.capUp || 0)}) rotate(${(st.capUp || 0) * .15},0,${g.hy})`);
}

// ------------------------------------------------------------------ cenário
function sky(col = '#d7edf0') { return `<rect x="-200" y="-200" width="1480" height="2400" fill="${col}"/>`; }
function backBuildings(col = '#bdb6da', win = '#d6d1ec', y0 = 1340) {
  let s = '';
  const B = [[-60, 520, 260], [180, 680, 220], [380, 560, 240], [600, 760, 200], [780, 600, 260], [1000, 700, 240]];
  for (const [x, h, w] of B) {
    s += `<rect x="${x}" y="${y0 - h}" width="${w}" height="${h}" fill="${col}" stroke="${OL}" stroke-width="5" opacity=".9"/>`;
    for (let r = 0; r < Math.floor(h / 90) - 1; r++) for (let c = 0; c < Math.floor(w / 70); c++)
      s += `<rect x="${x + 22 + c * 70}" y="${y0 - h + 34 + r * 90}" width="36" height="44" fill="${win}" stroke="${OL}" stroke-width="3" opacity=".9"/>`;
  }
  return s;
}
function house(x, w, h, col, o = {}) {
  const y0 = o.y0 || 1340, top = y0 - h;
  let s = `<rect x="${x}" y="${top}" width="${w}" height="${h}" fill="${col}" stroke="${OL}" stroke-width="${SW}"/>`;
  if (o.roof !== false) s += `<path d="M${x - 30},${top + 4} L${x + w / 2},${top - (o.roofH || 150)} L${x + w + 30},${top + 4} Z" fill="${o.roofCol || '#d9674b'}" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>`;
  if (o.door !== false) {
    const dx = x + (o.doorX ?? w * .18), dw = 150, dh = 300;
    s += `<rect x="${dx}" y="${y0 - dh}" width="${dw}" height="${dh}" fill="${o.doorCol || '#c9773f'}" stroke="${OL}" stroke-width="${SW}"/>
      <rect x="${dx + 22}" y="${y0 - dh + 24}" width="${dw - 44}" height="110" rx="8" fill="none" stroke="${OL}" stroke-width="5"/>
      <rect x="${dx + 22}" y="${y0 - dh + 154}" width="${dw - 44}" height="110" rx="8" fill="none" stroke="${OL}" stroke-width="5"/>
      <circle cx="${dx + dw - 22}" cy="${y0 - dh / 2}" r="11" fill="#f5c531" stroke="${OL}" stroke-width="5"/>`;
  }
  if (o.win !== false) {
    const wx = x + (o.winX ?? w * .58), wy = top + (o.winY ?? 70), ww = 170, wh = 170;
    s += `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="#bfe3f2" stroke="${OL}" stroke-width="${SW}"/>
      <path d="M${wx + 6},${wy + 6} Q${wx + 70},${wy + 70} ${wx + 30},${wy + wh - 6} L${wx + 6},${wy + wh - 6} Z" fill="#fff" stroke="${OL}" stroke-width="5"/>
      <path d="M${wx + ww - 6},${wy + 6} Q${wx + ww - 70},${wy + 70} ${wx + ww - 30},${wy + wh - 6} L${wx + ww - 6},${wy + wh - 6} Z" fill="#fff" stroke="${OL}" stroke-width="5"/>
      <rect x="${wx - 14}" y="${wy + wh}" width="${ww + 28}" height="18" fill="#fff" stroke="${OL}" stroke-width="6"/>`;
  }
  return s;
}
function street(y0 = 1340) {
  let s = `<rect x="-200" y="${y0}" width="1480" height="200" fill="#e7ddcb" stroke="${OL}" stroke-width="${SW}"/>`;
  for (let x = -100; x < 1200; x += 180) s += `<path d="M${x},${y0 + 8} L${x},${y0 + 190}" stroke="#cdc2ae" stroke-width="5"/>`;
  s += `<rect x="-200" y="${y0 + 196}" width="1480" height="30" fill="#c9bea9" stroke="${OL}" stroke-width="${SW}"/>`;
  s += `<rect x="-200" y="${y0 + 226}" width="1480" height="600" fill="#7c83a1"/>`;
  for (let x = -60; x < 1200; x += 220) s += `<rect x="${x}" y="${y0 + 470}" width="120" height="16" rx="6" fill="#e9e6f2" opacity=".8"/>`;
  return s;
}
function floorIn(y0 = 1340, wall = '#a8d8c7', floor = '#e4d6bd') {
  return `<rect x="-200" y="-200" width="1480" height="${y0 + 200}" fill="${wall}"/><rect x="-200" y="${y0 - 40}" width="1480" height="40" fill="#fff" stroke="${OL}" stroke-width="6"/>
    <rect x="-200" y="${y0}" width="1480" height="900" fill="${floor}" stroke="${OL}" stroke-width="${SW}"/>` +
    Array.from({ length: 8 }, (_, i) => `<path d="M${-100 + i * 180},${y0} L${-160 + i * 200},2000" stroke="rgba(0,0,0,.08)" stroke-width="5"/>`).join('');
}
function sparkle(x, y, s = 1, col = '#fff6a8') {
  return `<path d="M${x},${y - 26 * s} Q${x + 4 * s},${y - 4 * s} ${x + 26 * s},${y} Q${x + 4 * s},${y + 4 * s} ${x},${y + 26 * s} Q${x - 4 * s},${y + 4 * s} ${x - 26 * s},${y} Q${x - 4 * s},${y - 4 * s} ${x},${y - 26 * s} Z" fill="${col}" stroke="${OL}" stroke-width="3"/>`;
}

// ------------------------------------------------------------------ dinheiro
function coinSvg(id) {
  return `<g id="${id}" display="none"><circle r="38" fill="#f7c948" stroke="${OL}" stroke-width="7"/><circle r="26" fill="none" stroke="#d29a1c" stroke-width="5"/>
    <text y="15" text-anchor="middle" font-family="Luckiest" font-size="42" fill="#d29a1c">$</text></g>`;
}
// moeda voando: de (x0,y0) num arco até (x1,y1), girando
function flyCoin(id, lt, t0, x0, y0, x1, y1, d = .75, arc = 260) {
  const el = $(id); const p = (lt - t0) / d;
  if (p < 0 || p > 1.05) { el.setAttribute('display', 'none'); return; }
  const q = clamp(p);
  const x = lerp(x0, x1, q), y = lerp(y0, y1, q) - Math.sin(q * Math.PI) * arc;
  const sp = Math.cos(lt * 22);
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y}) scale(${Math.max(.15, Math.abs(sp))},1)`);
}
function tagSvg(id, txt, col = '#e8453c', size = 92) {
  return `<g id="${id}" display="none"><text text-anchor="middle" font-family="Luckiest" font-size="${size}" fill="${col}" stroke="${OL}" stroke-width="12" paint-order="stroke" stroke-linejoin="round">${txt}</text></g>`;
}
function popTag(id, lt, t0, x, y, d = 1.1) {
  const el = $(id); const p = lt - t0;
  if (p < 0 || p > d) { el.setAttribute('display', 'none'); return; }
  const s = backOut(p / .25), up = p * 70, a = p > d - .25 ? (d - p) / .25 : 1;
  el.setAttribute('display', 'inline'); el.setAttribute('opacity', a);
  el.setAttribute('transform', `translate(${x},${y - up}) scale(${s}) rotate(${Math.sin(p * 9) * 4})`);
}
// cartão de saldo (estilo app de banco)
function cardSvg(id, w = 470) {
  return `<g id="${id}" display="none"><rect x="${-w / 2 + 10}" y="-62" width="${w}" height="150" rx="34" fill="rgba(40,30,60,.25)"/>
    <rect x="${-w / 2}" y="-72" width="${w}" height="150" rx="34" fill="#fff" stroke="${OL}" stroke-width="8"/>
    <circle cx="${-w / 2 + 68}" cy="3" r="38" fill="#f7c948" stroke="${OL}" stroke-width="6"/><text x="${-w / 2 + 68}" y="18" text-anchor="middle" font-family="Luckiest" font-size="42" fill="#d29a1c">$</text>
    <text x="${-w / 2 + 124}" y="-22" font-family="Poppins" font-weight="800" font-size="30" fill="#8a86a0" letter-spacing="3">SALDO</text>
    <text class="v" x="${-w / 2 + 122}" y="48" font-family="Luckiest" font-size="72" fill="#2fae60">R$ 50,00</text></g>`;
}
function showCard(id, lt, t0, x, y, val, col, s = 1, shake = 0) {
  const el = $(id); if (lt < t0) { el.setAttribute('display', 'none'); return; }
  const k = backOut((lt - t0) / .3) * s;
  const sh = shake ? Math.sin(lt * 60) * shake * Math.max(0, 1 - (lt - t0) * 2) : 0;
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x + sh},${y}) scale(${k})`);
  const v = el.querySelector('.v'); v.textContent = typeof val === 'string' ? val : brl(val); v.setAttribute('fill', col);
}
function bigNum(id, txt, size = 150, col = '#ffd23f') {
  return `<g id="${id}" display="none"><text text-anchor="middle" font-family="Luckiest" font-size="${size}" fill="${col}" stroke="${OL}" stroke-width="16" paint-order="stroke" stroke-linejoin="round">${txt}</text></g>`;
}
function showPop(id, lt, t0, x, y, s = 1, txt) {
  const el = $(id); if (lt < t0) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y}) scale(${backOut((lt - t0) / .3) * s})`);
  if (txt !== undefined) el.querySelector('text').textContent = txt;
}

// ------------------------------------------------------------------ nota de dinheiro, balão de fala, gato
function noteSvg(id, val = '10', col = '#8fd19e', ink = '#2f8a4e') {
  return `<g id="${id}" display="none"><rect x="-80" y="-42" width="160" height="84" rx="10" fill="${col}" stroke="${OL}" stroke-width="7"/>
    <rect x="-64" y="-28" width="128" height="56" rx="8" fill="none" stroke="${ink}" stroke-width="4"/><circle r="20" fill="none" stroke="${ink}" stroke-width="4"/>
    <text x="-46" y="-6" text-anchor="middle" font-family="Luckiest" font-size="26" fill="${ink}">${val}</text><text x="46" y="26" text-anchor="middle" font-family="Luckiest" font-size="26" fill="${ink}">${val}</text></g>`;
}
// nota voando (sai balançando, como papel ao vento)
function flyNote(id, lt, t0, x0, y0, x1, y1, d = 1.0) {
  const el = $(id); const p = (lt - t0) / d;
  if (p < 0 || p > 1.02) { el.setAttribute('display', 'none'); return; }
  const q = easeOut(p);
  const x = lerp(x0, x1, q) + Math.sin(p * 9) * 40, y = lerp(y0, y1, q);
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y}) rotate(${Math.sin(p * 11) * 28}) scale(${1 - p * .25},${Math.max(.2, Math.abs(Math.cos(p * 7)))})`);
}
function bubbleSvg(id, txt, w = 420, size = 54, tail = 'down') {
  const tl = tail === 'down' ? `<path d="M-20,58 L0,104 L26,58 Z" fill="#fff" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/><rect x="-28" y="46" width="62" height="18" fill="#fff"/>` : '';
  return `<g id="${id}" display="none"><rect x="${-w / 2}" y="-62" width="${w}" height="124" rx="40" fill="#fff" stroke="${OL}" stroke-width="7"/>${tl}
    <text y="${size * .35}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="${size}" fill="${OL}">${txt}</text></g>`;
}
function showBubble(id, lt, t0, t1, x, y, flip = 1) {
  const el = $(id);
  if (lt < t0 || lt > t1) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y}) scale(${backOut((lt - t0) / .22) * flip},${backOut((lt - t0) / .22)})`);
}
function catSvg(id) {
  return `<g id="${id}"><path id="${id}-tail" d="M60,-30 Q150,-40 130,-150" fill="none" stroke="${OL}" stroke-width="34" stroke-linecap="round"/><path d="M60,-30 Q150,-40 130,-150" fill="none" stroke="#f0a04b" stroke-width="20" stroke-linecap="round" id="${id}-tail2"/>
    <ellipse cx="0" cy="-70" rx="95" ry="75" fill="#f0a04b" stroke="${OL}" stroke-width="${SW}"/>
    <path d="M-40,-60 l-6,40 M0,-56 l0,44 M40,-60 l6,40" stroke="#d9822e" stroke-width="10" stroke-linecap="round"/>
    <g id="${id}-head"><path d="M-80,-190 L-90,-270 L-30,-225 Z M80,-190 L90,-270 L30,-225 Z" fill="#f0a04b" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/>
    <circle cx="0" cy="-180" r="88" fill="#f0a04b" stroke="${OL}" stroke-width="${SW}"/>
    <g id="${id}-eyes">${[-1, 1].map(s => `<ellipse cx="${s * 34}" cy="-190" rx="22" ry="28" fill="#fff" stroke="${OL}" stroke-width="6"/><circle cx="${s * 34}" cy="-186" r="13" fill="#2b5a2b"/><circle cx="${s * 34 + 4}" cy="-192" r="5" fill="#fff"/>`).join('')}</g>
    <path d="M-10,-152 L10,-152 L0,-140 Z" fill="#ff8f9a" stroke="${OL}" stroke-width="4"/>
    <path id="${id}-m1" d="M-22,-128 Q-11,-116 0,-132 Q11,-116 22,-128" fill="none" stroke="${OL}" stroke-width="6" stroke-linecap="round"/>
    <ellipse id="${id}-m2" cx="0" cy="-118" rx="14" ry="18" fill="#5a1f2b" stroke="${OL}" stroke-width="6" display="none"/>
    ${[-1, 1].map(s => `<path d="M${s * 40},-150 L${s * 110},-160 M${s * 40},-140 L${s * 110},-136" stroke="${OL}" stroke-width="4"/>`).join('')}</g></g>`;
}
function setCat(id, lt, x, y, s = 1, shocked = false) {
  $(id).setAttribute('transform', `translate(${x},${y}) scale(${s})`);
  $(id + '-tail').setAttribute('transform', `rotate(${Math.sin(lt * 4) * 10},60,-30)`); $(id + '-tail2').setAttribute('transform', `rotate(${Math.sin(lt * 4) * 10},60,-30)`);
  $(id + '-head').setAttribute('transform', shocked ? `translate(0,${-10 - Math.abs(Math.sin(lt * 20)) * 6})` : '');
  $(id + '-eyes').setAttribute('transform', `translate(0,-190) scale(${shocked ? 1.3 : 1},${((lt % 2.6) < .1 && !shocked) ? .1 : (shocked ? 1.3 : 1)}) translate(0,190)`);
  $(id + '-m1').setAttribute('display', shocked ? 'none' : 'inline'); $(id + '-m2').setAttribute('display', shocked ? 'inline' : 'none');
}

// ------------------------------------------------------------------ animação mais fluida: keyframes suaves, corações, cachorro
// K(lt, [[t, v], ...]) interpola números (ou arrays) com easeInOut entre as chaves
function K(lt, keys) {
  if (lt <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, a] = keys[i], [t1, b] = keys[i + 1];
    if (lt <= t1) { const q = easeInOut((lt - t0) / (t1 - t0)); return Array.isArray(a) ? a.map((x, j) => lerp(x, b[j], q)) : lerp(a, b, q); }
  }
  return keys[keys.length - 1][1];
}
function heartSvg(id, col = '#ff6b8a') {
  return `<g id="${id}" display="none"><path d="M0,30 C-60,-10 -40,-60 0,-30 C40,-60 60,-10 0,30 Z" fill="${col}" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/><ellipse cx="-18" cy="-24" rx="9" ry="6" fill="#fff" opacity=".6"/></g>`;
}
// corações subindo e balançando a partir de (x,y)
function floatHearts(prefix, n, lt, t0, x, y, spread = 160, dur = 1.6) {
  for (let i = 0; i < n; i++) {
    const el = $(prefix + i); const p = (lt - t0 - i * .12) / dur;
    if (p < 0 || p > 1) { el.setAttribute('display', 'none'); continue; }
    const hx = x + ((i * 73) % spread - spread / 2) + Math.sin(p * 8 + i) * 30, hy = y - p * 520;
    el.setAttribute('display', 'inline'); el.setAttribute('opacity', p > .75 ? (1 - p) / .25 : 1);
    el.setAttribute('transform', `translate(${hx},${hy}) scale(${backOut(p / .2) * (.7 + (i % 3) * .2)}) rotate(${Math.sin(p * 6 + i) * 15})`);
  }
}
function dogSvg(id) {
  return `<g id="${id}"><path id="${id}-tail" d="M90,-90 Q160,-130 150,-190" fill="none" stroke="${OL}" stroke-width="30" stroke-linecap="round"/><path id="${id}-tail2" d="M90,-90 Q160,-130 150,-190" fill="none" stroke="#c9905a" stroke-width="16" stroke-linecap="round"/>
    ${[-55, 55].map(x => `<rect x="${x - 18}" y="-70" width="36" height="70" rx="16" fill="#c9905a" stroke="${OL}" stroke-width="7"/>`).join('')}
    <ellipse cx="0" cy="-95" rx="110" ry="65" fill="#c9905a" stroke="${OL}" stroke-width="${SW}"/><ellipse cx="-20" cy="-95" rx="40" ry="30" fill="#a86c3a"/>
    <g id="${id}-head"><path d="M-95,-240 Q-140,-200 -110,-140 Q-80,-150 -70,-200 Z M95,-240 Q140,-200 110,-140 Q80,-150 70,-200 Z" fill="#7a4a26" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/>
    <circle cx="0" cy="-200" r="85" fill="#c9905a" stroke="${OL}" stroke-width="${SW}"/><ellipse cx="0" cy="-165" rx="46" ry="34" fill="#e8c49a" stroke="${OL}" stroke-width="6"/>
    <g id="${id}-eyes">${[-1, 1].map(s => `<ellipse cx="${s * 32}" cy="-215" rx="18" ry="22" fill="#fff" stroke="${OL}" stroke-width="6"/><circle cx="${s * 32}" cy="-211" r="11" fill="#2b1a10"/><circle cx="${s * 32 + 4}" cy="-216" r="4" fill="#fff"/>`).join('')}</g>
    <ellipse cx="0" cy="-180" rx="16" ry="11" fill="#2b2745"/><path d="M0,-170 L0,-152 M-18,-150 Q0,-138 18,-150" fill="none" stroke="${OL}" stroke-width="5" stroke-linecap="round"/>
    <path id="${id}-tongue" d="M-10,-150 Q0,-118 10,-150 Z" fill="#ff7a8a" stroke="${OL}" stroke-width="4"/></g></g>`;
}
function setDog(id, lt, x, y, s = 1, mood = 'happy') {
  $(id).setAttribute('transform', `translate(${x},${y}) scale(${s})`);
  const w = Math.sin(lt * (mood === 'happy' ? 14 : 3)) * (mood === 'happy' ? 22 : 6);
  $(id + '-tail').setAttribute('transform', `rotate(${w},90,-90)`); $(id + '-tail2').setAttribute('transform', `rotate(${w},90,-90)`);
  $(id + '-head').setAttribute('transform', `rotate(${mood === 'confuso' ? 14 : Math.sin(lt * 3) * 3},0,-120)`);
  $(id + '-tongue').setAttribute('display', mood === 'happy' ? 'inline' : 'none');
  $(id + '-eyes').setAttribute('transform', `translate(0,-213) scale(1,${(lt % 2.7) < .1 ? .15 : 1}) translate(0,213)`);
}
