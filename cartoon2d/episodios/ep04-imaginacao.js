// Episódio 4: "Na minha cidade, as brigas se resolvem numa batalha de imaginação." (45s)
// Caio aposta R$ 200 contra o Bruno, perde de 0 a 2 (tigre x leão, dragão x cavaleiro), imagina a mãe do Bruno
// chamando e ganha R$ 400... até a mãe dele, que não é imaginação, aparecer.
DUR = 45;
LINES = [
  [0.3, 3.4, 'Na minha cidade, as brigas se resolvem numa batalha de imaginação.'],
  [3.6, 5.8, 'Funciona assim: você imagina fogo…'],
  [6.0, 7.8, 'O outro imagina água. E apaga o seu fogo.'],
  [8.0, 10.2, 'Tigre contra leão? O leão ganha.'],
  [10.4, 12.2, 'E quem perde… paga.'],
  [12.4, 15.4, 'Eu sou o Caio. E eu nunca perdi uma batalha.'],
  [15.6, 18.4, 'Até que o Bruno, da rua de cima, apostou duzentos reais.'],
  [18.6, 20.4, 'Eu imaginei um tigre.'],
  [20.6, 22.4, 'Ele imaginou um leão.'],
  [22.6, 24.4, 'Eu imaginei um dragão.'],
  [24.6, 26.6, 'Ele imaginou um cavaleiro gigante.'],
  [26.8, 28.8, 'Dois a zero. Eu tava perdendo.'],
  [29.0, 31.6, 'Aí eu imaginei a coisa mais forte do mundo…'],
  [31.8, 34.2, '“BRUNO! JÁ PRA CASA!” A mãe dele.'],
  [34.4, 36.8, 'Ninguém vence mãe chamando. Quatrocentos reais!'],
  [37.0, 39.6, 'Só que eu esqueci de um detalhe…'],
  [39.8, 42.2, '“CAIO! Que aposta é essa?”'],
  [42.4, 44.8, 'A minha mãe não é imaginação.'],
];

const SALDO = t => t < 35.0 ? 200 : t < 36.0 ? Math.round(200 + 200 * easeOut(t - 35.0)) : t < 43.2 ? 400 : Math.max(0, Math.round(400 * (1 - easeOut((t - 43.2) / .8))));
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => { const v = SALDO(t0 + lt); showCard(id, lt, from, x, y, v, v >= 200 ? '#2fae60' : '#e8453c', s, shake); };
const LOOK4 = { bruno: { kid: 1, skin: '#e0a27a', shirt: '#3fae6a', stripe: '#2f8a52', shorts: '#55556e', shoe: '#fff', hair: 'short', hairCol: '#1c1412' },
  maeB: { kid: 0, pocket: 0, skin: '#e8b48c', shirt: '#e86f6f', dress: '#e86f6f', shoe: '#2b2745', hair: 'bun', hairCol: '#c8742c' } };
const mk4 = (l, x = {}) => mk(l in LOOK4 ? 'caio' : l, l in LOOK4 ? { ...LOOK4[l], ...x } : x);

// ------------------------------------------------------------------ desenhos da imaginação (desenhados virados para a direita)
const GL = 'filter="url(#e4glow)"';
const defs4 = `<defs><filter id="e4glow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#fff6a8" flood-opacity="1"/></filter></defs>`;
const fireSvg = id => `<g id="${id}" display="none" ${GL}><path class="f1" d="M0,120 C-150,100 -150,-40 -60,-120 C-70,-40 -20,-40 -10,-90 C10,-160 60,-200 50,-260 C140,-170 170,-40 120,40 C100,90 60,120 0,120 Z" fill="#e8453c" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
  <path class="f2" d="M0,110 C-90,100 -100,10 -40,-50 C-40,0 0,0 10,-50 C30,-110 70,-120 60,-170 C120,-90 120,10 80,60 C60,90 40,110 0,110 Z" fill="#ff9a2e"/><path d="M0,105 C-50,95 -50,40 -10,10 C0,40 20,30 30,0 C60,40 50,95 0,105 Z" fill="#ffd23f"/></g>`;
const waveSvg = id => `<g id="${id}" display="none" ${GL}><path d="M-260,140 C-260,-40 -120,-200 40,-200 C180,-200 250,-90 200,-10 C160,50 70,20 90,-50 C110,-110 30,-130 -20,-90 C-80,-40 -60,80 20,140 Z" fill="#3f8fd6" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
  <path d="M-200,100 C-190,-40 -80,-150 40,-160" fill="none" stroke="#9fd3ff" stroke-width="16" stroke-linecap="round"/>${[[180, -150], [230, -60], [120, -210]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="16" fill="#9fd3ff" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`;
const catBody = (col, stripes, mane) => `
  <path class="tail" d="M-120,10 Q-200,-20 -190,-110" fill="none" stroke="${OL}" stroke-width="28" stroke-linecap="round"/><path d="M-120,10 Q-200,-20 -190,-110" fill="none" stroke="${col}" stroke-width="15" stroke-linecap="round"/>
  ${[-90, -40, 40, 90].map(x => `<rect x="${x - 20}" y="40" width="40" height="90" rx="18" fill="${col}" stroke="${OL}" stroke-width="7"/>`).join('')}
  <ellipse cx="0" cy="20" rx="150" ry="80" fill="${col}" stroke="${OL}" stroke-width="8"/>
  ${stripes ? [-70, -20, 30].map(x => `<path d="M${x},-55 q14,30 0,50" fill="none" stroke="${OL}" stroke-width="12" stroke-linecap="round"/>`).join('') : ''}
  <g class="head">${mane ? Array.from({ length: 14 }, (_, i) => { const a = i / 14 * 6.283; return `<circle cx="${150 + Math.cos(a) * 92}" cy="${-70 + Math.sin(a) * 92}" r="44" fill="#b8621f" stroke="${OL}" stroke-width="7"/>`; }).join('') : ''}
  <path d="M95,-150 L110,-200 L140,-160 Z M185,-160 L215,-200 L225,-145 Z" fill="${col}" stroke="${OL}" stroke-width="7" stroke-linejoin="round"/>
  <circle cx="155" cy="-70" r="88" fill="${col}" stroke="${OL}" stroke-width="8"/>
  ${stripes ? `<path d="M120,-150 q10,25 0,40 M190,-150 q-10,25 0,40" fill="none" stroke="${OL}" stroke-width="10" stroke-linecap="round"/>` : ''}
  <ellipse cx="175" cy="-35" rx="48" ry="34" fill="#fbe7c6" stroke="${OL}" stroke-width="6"/>
  <path d="M120,-100 L150,-90 M200,-100 L170,-90" stroke="${OL}" stroke-width="9" stroke-linecap="round"/>
  <ellipse cx="135" cy="-78" rx="12" ry="14" fill="#1b1420"/><ellipse cx="185" cy="-78" rx="12" ry="14" fill="#1b1420"/>
  <ellipse cx="175" cy="-48" rx="14" ry="10" fill="#2b2745"/>
  <path class="roar" d="M150,-30 L205,-30 Q200,10 178,12 Q156,10 150,-30 Z" fill="#5a1f2b" stroke="${OL}" stroke-width="6"/><path d="M152,-30 l8,12 l8,-12 l8,12 l8,-12 l8,12 l8,-12" fill="#fff"/></g>`;
const tigerSvg = id => `<g id="${id}" display="none" ${GL}>${catBody('#f08a2c', 1, 0)}</g>`;
const lionSvg = id => `<g id="${id}" display="none" ${GL}>${catBody('#e8b04b', 0, 1)}</g>`;
const dragonSvg = id => `<g id="${id}" display="none" ${GL}>
  <path class="wing" d="M-40,-40 L-180,-260 L-140,-150 L-230,-170 L-150,-80 L-220,-60 L-60,0 Z" fill="#8f6bd1" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
  <path d="M-150,40 Q-260,40 -280,-40 Q-230,0 -150,-10 Z" fill="#3fae6a" stroke="${OL}" stroke-width="8"/>
  ${[-70, 50].map(x => `<rect x="${x - 22}" y="40" width="44" height="90" rx="18" fill="#3fae6a" stroke="${OL}" stroke-width="7"/>`).join('')}
  <ellipse cx="-10" cy="10" rx="150" ry="90" fill="#3fae6a" stroke="${OL}" stroke-width="8"/><ellipse cx="0" cy="40" rx="100" ry="45" fill="#bfe58f"/>
  <path d="M90,-20 Q150,-120 170,-160" fill="none" stroke="${OL}" stroke-width="70" stroke-linecap="round"/><path d="M90,-20 Q150,-120 170,-160" fill="none" stroke="#3fae6a" stroke-width="54" stroke-linecap="round"/>
  <g class="head"><path d="M150,-250 l-10,-50 l40,40 Z M200,-250 l10,-55 l20,50 Z" fill="#f5c531" stroke="${OL}" stroke-width="6"/>
  <path d="M120,-220 Q170,-280 250,-230 L300,-190 Q300,-150 250,-150 L150,-140 Q110,-160 120,-220 Z" fill="#3fae6a" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
  <ellipse cx="190" cy="-215" rx="14" ry="16" fill="#fff" stroke="${OL}" stroke-width="5"/><circle cx="194" cy="-213" r="7" fill="#1b1420"/><circle cx="280" cy="-190" r="6" fill="${OL}"/></g>
  <path class="breath" d="M300,-170 Q420,-230 520,-170 Q430,-150 520,-110 Q410,-120 300,-160 Z" fill="#ff9a2e" stroke="${OL}" stroke-width="6" stroke-linejoin="round"/></g>`;
const knightSvg = id => `<g id="${id}" display="none" ${GL}>
  ${[-50, 50].map(x => `<rect x="${x - 34}" y="120" width="68" height="190" rx="14" fill="#a9b0bf" stroke="${OL}" stroke-width="8"/>`).join('')}
  <rect x="-130" y="-140" width="260" height="280" rx="50" fill="#c3c9d6" stroke="${OL}" stroke-width="8"/><path d="M-130,40 L130,40" stroke="${OL}" stroke-width="6"/>
  <g class="sword"><rect x="-188" y="-470" width="34" height="330" rx="6" fill="#e6eaf2" stroke="${OL}" stroke-width="7"/><rect x="-230" y="-160" width="118" height="30" rx="10" fill="#c98a52" stroke="${OL}" stroke-width="6"/></g>
  <circle cx="-170" cy="-110" r="40" fill="#a9b0bf" stroke="${OL}" stroke-width="7"/>
  <path d="M-90,-150 Q-90,-330 0,-330 Q90,-330 90,-150 Z" fill="#a9b0bf" stroke="${OL}" stroke-width="8"/><rect x="-60" y="-250" width="120" height="24" rx="8" fill="#2b2745"/><path d="M0,-330 Q30,-400 70,-380 Q30,-350 20,-320 Z" fill="#e8453c" stroke="${OL}" stroke-width="6"/>
  <g class="shield"><path d="M60,-80 L240,-80 L240,60 Q240,170 150,220 Q60,170 60,60 Z" fill="#3b5bb5" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/><path d="M150,-60 L150,190 M80,40 L220,40" stroke="#f5c531" stroke-width="18"/></g></g>`;
const puffSvg = id => `<g id="${id}" display="none">${Array.from({ length: 8 }, (_, i) => `<circle class="pf" r="50" fill="#eef0f6" stroke="${OL}" stroke-width="6" data-a="${i / 8 * 6.283}"/>`).join('')}</g>`;
// aparece com "pop" e flutua; some num "puf"
function proj(id, lt, tIn, tOut, x, y, s = 1, flip = false) {
  const el = $(id);
  if (lt < tIn || lt > tOut) { el.setAttribute('display', 'none'); return 0; }
  const k = backOut((lt - tIn) / .35) * (lt > tOut - .2 ? Math.max(0, (tOut - lt) / .2) : 1);
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y + Math.sin(lt * 3) * 10}) scale(${(flip ? -1 : 1) * s * k},${s * k})`);
  return lt - tIn;
}
function poof(id, lt, t0, x, y, s = 1) {
  const el = $(id); const p = (lt - t0) / .6;
  if (p < 0 || p > 1) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline'); el.setAttribute('opacity', 1 - p * p);
  el.setAttribute('transform', `translate(${x},${y}) scale(${s})`);
  el.querySelectorAll('.pf').forEach(c => { const a = +c.dataset.a; c.setAttribute('cx', Math.cos(a) * 140 * easeOut(p)); c.setAttribute('cy', Math.sin(a) * 100 * easeOut(p)); c.setAttribute('r', 50 + 30 * p); });
}
// trilha de bolinhas de pensamento da cabeça até a imaginação
const trailSvg = id => `<g id="${id}" display="none">${[0, 1, 2].map(i => `<circle class="tb" r="${14 + i * 8}" fill="#fff" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`;
function trail(id, lt, tIn, tOut, x0, y0, x1, y1) {
  const el = $(id); if (lt < tIn || lt > tOut) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline');
  el.querySelectorAll('.tb').forEach((c, i) => { const q = (i + 1) / 4; c.setAttribute('cx', lerp(x0, x1, q)); c.setAttribute('cy', lerp(y0, y1, q) + Math.sin(lt * 5 + i) * 6); c.setAttribute('opacity', clamp((lt - tIn) * 6 - i)); });
}
const arena = () => sky() + backBuildings() + house(-40, 420, 520, '#a8d8c7', { y0: 1250 }) + house(400, 360, 470, '#f2c29b', { y0: 1250, doorCol: '#4a6fa5', winX: 190 }) + house(780, 360, 500, '#c9b6e4', { y0: 1250 })
  + `<rect x="-200" y="1250" width="1480" height="900" fill="#e3cfa2" stroke="${OL}" stroke-width="${SW}"/>${Array.from({ length: 30 }, (_, i) => `<circle cx="${(i * 137) % 1080}" cy="${1300 + (i * 71) % 560}" r="${4 + i % 3}" fill="#c9b386"/>`).join('')}
  <ellipse cx="540" cy="1500" rx="470" ry="120" fill="none" stroke="#fff" stroke-width="12" stroke-dasharray="40 24" opacity=".9"/><path d="M540,1385 L540,1615" stroke="#fff" stroke-width="10" stroke-dasharray="30 20" opacity=".9"/>`;
const banner = id => `<g id="${id}"><rect x="90" y="120" width="900" height="130" rx="30" fill="#e8453c" stroke="${OL}" stroke-width="9"/><text x="540" y="212" text-anchor="middle" font-family="Luckiest" font-size="68" fill="#fff" stroke="${OL}" stroke-width="8" paint-order="stroke">BATALHA DE IMAGINAÇÃO</text></g>`;
const scoreSvg = id => `<g id="${id}" display="none"><rect x="-300" y="-55" width="600" height="110" rx="24" fill="#2b2745" stroke="#fff" stroke-width="6"/><text class="sc" y="24" text-anchor="middle" font-family="Luckiest" font-size="62" fill="#ffd23f">CAIO 0 x 0 BRUNO</text></g>`;
function score(id, lt, x, y, txt) { const el = $(id); el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${x},${y})`); el.querySelector('.sc').textContent = txt; }
function animProj(id, lt) {  // movimentos internos: fogo tremula, rabo, rugido, asas
  const el = $(id); if (!el || el.getAttribute('display') === 'none') return;
  el.querySelectorAll('.f1,.f2').forEach((f, i) => f.setAttribute('transform', `scale(${1 + Math.sin(lt * 17 + i) * .05},${1 + Math.sin(lt * 13 + i) * .08})`));
  el.querySelectorAll('.tail').forEach(f => f.setAttribute('transform', `rotate(${Math.sin(lt * 6) * 12},-120,10)`));
  el.querySelectorAll('.head').forEach(f => f.setAttribute('transform', `rotate(${Math.sin(lt * 4) * 4},120,-60)`));
  el.querySelectorAll('.wing').forEach(f => f.setAttribute('transform', `rotate(${Math.sin(lt * 10) * 14},-40,-20)`));
  el.querySelectorAll('.breath').forEach(f => f.setAttribute('transform', `translate(300,-160) scale(${.8 + Math.abs(Math.sin(lt * 9)) * .4}) translate(-300,160)`));
  el.querySelectorAll('.sword').forEach(f => f.setAttribute('transform', `rotate(${Math.sin(lt * 3) * 8},-170,-140)`));
}

// 1. gancho: fogo contra água na arena (zoom-out borrado)
shot(0, 3.5, () => {
  const a = mk('n1'), b = mk('n2');
  const svg = defs4 + arena() + `<g>${a.svg}</g><g>${b.svg}</g>` + fireSvg('e4f1') + waveSvg('e4w1') + puffSvg('e4p1') + banner('e4ban1') + trailSvg('e4tr1a') + trailSvg('e4tr1b');
  return {
    svg, cam: lt => ({ s: lerp(2.6, 1.0, easeOut(lt / 1.0)), fx: 420, fy: 900, blur: lt < .8 ? 24 * (1 - lt / .8) : 0 }),
    update(lt) {
      setChar(a.id, { x: 200, y: 1520, scale: .8, t: lt, mouth: 'shout', eyes: lt < 2 ? 'open' : 'wide', brow: -1, mad: lt < 2, armL: 140, armR: 40, seed: 1 });
      setChar(b.id, { x: 880, y: 1520, scale: .8, t: lt, mouth: 'smug', eyes: 'half', brow: -.6, armR: 140, armL: 40, seed: 2 });
      proj('e4f1', lt, 0, 2.2, 400, 960, 1.0); animProj('e4f1', lt);
      proj('e4w1', lt, 1.2, 3.5, K(lt, [[1.2, 760], [2.1, 480]]), 980, 1.0, true);
      poof('e4p1', lt, 2.1, 420, 980, 1.2);
      trail('e4tr1a', lt, 0, 2.2, 230, 1160, 400, 1040); trail('e4tr1b', lt, 1.2, 3.5, 850, 1160, 700, 1040);
      $('e4ban1').setAttribute('transform', `translate(540,185) scale(${backOut((lt - .6) / .35)}) translate(-540,-185)`);
    }
  };
});

// 2. as regras: fogo cresce… e a água apaga
shot(3.5, 7.9, () => {
  const a = mk('n1');
  let steam = ''; for (let i = 0; i < 5; i++) steam += `<circle class="e4st" r="40" fill="#f2f2f6" stroke="${OL}" stroke-width="5"/>`;
  const svg = defs4 + arena() + `<g>${a.svg}</g>` + fireSvg('e4f2') + waveSvg('e4w2') + `<g id="e4steam">${steam}</g>` + trailSvg('e4tr2');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.3], [4.4, 1.45]]), fx: 420, fy: 1150 }),
    update(lt) {
      setChar(a.id, { x: 230, y: 1520, scale: .95, t: lt, mouth: lt < 2.6 ? 'smug' : 'O', eyes: lt < 2.6 ? 'half' : 'wide', brow: lt < 2.6 ? -1 : 1, armL: K(lt, [[0, 20], [.5, 150]]), seed: 3 });
      proj('e4f2', lt, .3, 3.2, 560, 1020, K(lt, [[.3, .6], [2.4, 1.3]])); animProj('e4f2', lt);
      trail('e4tr2', lt, .3, 3.2, 290, 1100, 480, 1060);
      proj('e4w2', lt, 2.4, 4.4, K(lt, [[2.4, 1100], [3.2, 600]]), 1000, 1.2, true);
      $('e4steam').setAttribute('display', lt > 3.1 ? 'inline' : 'none');
      document.querySelectorAll('.e4st').forEach((c, i) => { const p = clamp((lt - 3.1) / 1.2); c.setAttribute('cx', 520 + (i - 2) * 70 + Math.sin(p * 6 + i) * 20); c.setAttribute('cy', 980 - p * 400 - i * 20); c.setAttribute('opacity', 1 - p); });
    }
  };
});

// 3. tigre contra leão: o leão ganha
shot(7.9, 10.3, () => {
  const svg = defs4 + arena() + tigerSvg('e4tg3') + lionSvg('e4ln3') + puffSvg('e4p3') + tagSvg('e4win3', 'VENCEU!', '#ffd23f', 100);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.4, 1.08]]), fx: 540, fy: 1000 }),
    update(lt) {
      proj('e4tg3', lt, .05, 1.5, K(lt, [[0, 230], [1.2, 290]]), 1020, .85); animProj('e4tg3', lt);
      proj('e4ln3', lt, .6, 2.4, K(lt, [[.6, 900], [1.3, 760]]), 960, K(lt, [[.6, 1.0], [1.3, 1.25]]), true); animProj('e4ln3', lt);
      poof('e4p3', lt, 1.4, 330, 980, 1.2);
      showPop('e4win3', lt, 1.6, 700, 620, 1);
    }
  };
});

// 4. quem perde paga
shot(10.3, 12.3, () => {
  const a = mk('n1'), b = mk('n2');
  let notes = ''; for (let i = 0; i < 3; i++) notes += noteSvg('e4n4' + i);
  const svg = arena() + `<g>${a.svg}</g><g>${b.svg}</g>` + notes + tagSvg('e4t4a', '-R$10') + tagSvg('e4t4b', '+R$10', '#2fae60');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2, 1.25]]), fx: 540, fy: 1150 }),
    update(lt) {
      setChar(a.id, { x: 280, y: 1520, scale: .95, t: lt, mouth: 'frown', eyes: 'half', tears: lt > .6, armL: K(lt, [[0, 20], [.4, 80]]), seed: 4, lookX: 10 });
      setChar(b.id, { x: 800, y: 1520, scale: .95, t: lt, mouth: 'smile', eyes: 'happy', armR: K(lt, [[0, 20], [.4, 90]]), hop: lt > .8 ? 2 : 0, seed: 5 });
      for (let i = 0; i < 3; i++) flyNote('e4n4' + i, lt, .3 + i * .2, 380, 1200, 720, 1150, .8);
      popTag('e4t4a', lt, .4, 260, 820, 1.4); popTag('e4t4b', lt, .9, 820, 820, 1.1);
    }
  };
});

// 5. Caio: nunca perdeu (troféus) + saldo R$ 200
shot(12.3, 15.5, () => {
  const k = mk('caio'); let tr = '';
  [[150, 1330, .9], [300, 1300, 1.1], [780, 1300, 1.1], [930, 1330, .9]].forEach(([x, y, s], i) => tr += `<g id="e4tr${i}" transform="translate(${x},${y}) scale(${s})"><path d="M-50,-140 L50,-140 Q50,-60 0,-50 Q-50,-60 -50,-140 Z" fill="#ffd23f" stroke="${OL}" stroke-width="7"/><path d="M-50,-125 q-40,0 -30,35 q8,20 30,20 M50,-125 q40,0 30,35 q-8,20 -30,20" fill="none" stroke="${OL}" stroke-width="7"/><rect x="-10" y="-52" width="20" height="30" fill="#ffd23f" stroke="${OL}" stroke-width="6"/><rect x="-40" y="-25" width="80" height="25" rx="6" fill="#c98a52" stroke="${OL}" stroke-width="6"/></g>`);
  const svg = arena() + tr + `<g>${k.svg}</g>` + [0, 1, 2, 3].map(i => `<g id="e4sp5${i}">${sparkle(200 + i * 230, 700 + (i % 2) * 120, .9)}</g>`).join('') + cardSvg('e4c5');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.12], [3.2, 1.22]]), fx: 540, fy: 1100 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1520, scale: 1.1, t: lt, mouth: 'smile', talk: lt < 2.6, eyes: lt > 1.4 && lt < 2 ? 'happy' : 'open', armL: K(lt, [[0, 20], [.4, 150], [1.4, 150], [1.8, 60]]), armR: 60, hop: lt < .5 ? 2.5 : 0, seed: 6 });
      for (let i = 0; i < 4; i++) { $('e4tr' + i).style.opacity = clamp((lt - i * .15) * 4); $('e4sp5' + i).setAttribute('opacity', Math.abs(Math.sin(lt * 4 + i))); }
      card('e4c5', 12.3, lt, 540, 360, 1.1, 0, 1.6);
    }
  };
});

// 6. o desafio do Bruno: aposta R$ 200
shot(15.5, 18.5, () => {
  const k = mk('caio'), b = mk4('bruno');
  let pile = ''; for (let i = 0; i < 4; i++) pile += noteSvg('e4n6' + i);
  const svg = arena() + `<g>${k.svg}</g><g>${b.svg}</g>` + pile + `<g id="e4bet"><rect x="290" y="300" width="500" height="150" rx="30" fill="#ffd23f" stroke="${OL}" stroke-width="9"/><text x="540" y="360" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="${OL}">APOSTA</text><text x="540" y="430" text-anchor="middle" font-family="Luckiest" font-size="72" fill="#e8453c">R$ 200</text></g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [3, 1.1]]), fx: 540, fy: 1100 }),
    update(lt) {
      setChar(b.id, { x: K(lt, [[0, 1150], [1.0, 790]]), y: 1520, scale: 1.12, t: lt, mouth: 'smug', talk: lt > 1.1 && lt < 2.6, eyes: 'half', brow: -1, armR: K(lt, [[1.0, 20], [1.5, 100]]), armL: 20, walk: lt < 1.0 ? 1.6 : 0, seed: 7, lookX: -12 });
      setChar(k.id, { x: 280, y: 1520, scale: 1.0, t: lt, mouth: lt < 1.4 ? 'smile' : 'flat', eyes: lt < 1.4 ? 'open' : 'wide', brow: lt < 1.4 ? 0 : .8, sweat: lt > 1.6, seed: 8, lookX: 12 });
      for (let i = 0; i < 4; i++) { const el = $('e4n6' + i); const p = clamp((lt - 1.6 - i * .12) / .4); el.setAttribute('display', p > 0 ? 'inline' : 'none'); el.setAttribute('transform', `translate(${540 + (i - 1.5) * 30},${lerp(900, 1440 - i * 18, easeOut(p))}) rotate(${(i - 1.5) * 12}) scale(.9)`); }
      $('e4bet').setAttribute('transform', `translate(540,375) scale(${backOut((lt - 1.4) / .35)}) rotate(${Math.sin(lt * 3) * 2}) translate(-540,-375)`);
    }
  };
});

// 7. rodada 1: tigre do Caio x leão do Bruno
shot(18.5, 22.5, () => {
  const k = mk('caio'), b = mk4('bruno');
  const svg = defs4 + arena() + `<g>${k.svg}</g><g>${b.svg}</g>` + tigerSvg('e4tg7') + lionSvg('e4ln7') + puffSvg('e4p7') + trailSvg('e4tr7a') + trailSvg('e4tr7b') + scoreSvg('e4sc7');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [4, 1.06]]), fx: 540, fy: 1100 }),
    update(lt) {
      const lost = lt > 3.1;
      setChar(k.id, { x: 200, y: 1560, scale: .85, t: lt, mouth: lost ? 'O' : 'shout', eyes: lost ? 'wide' : 'open', brow: lost ? 1 : -1, mad: !lost, armL: 150, seed: 9 });
      setChar(b.id, { x: 880, y: 1560, scale: .9, t: lt, mouth: lt > 2.1 ? 'shout' : 'smug', eyes: 'half', brow: -1, armR: lt > 2.1 ? 150 : 20, seed: 10 });
      proj('e4tg7', lt, .1, 3.2, K(lt, [[.1, 300], [2.8, 360]]), 1000, .8); animProj('e4tg7', lt);
      proj('e4ln7', lt, 2.1, 4.0, K(lt, [[2.1, 900], [2.9, 720]]), 960, K(lt, [[2.1, .9], [2.9, 1.2]]), true); animProj('e4ln7', lt);
      poof('e4p7', lt, 3.0, 360, 980, 1.2);
      trail('e4tr7a', lt, .1, 3.0, 230, 1200, 330, 1090); trail('e4tr7b', lt, 2.1, 4.0, 850, 1200, 760, 1090);
      score('e4sc7', lt, 540, 330, lost ? 'CAIO 0 x 1 BRUNO' : 'CAIO 0 x 0 BRUNO');
    }
  };
});

// 8. rodada 2: dragão x cavaleiro gigante
shot(22.5, 26.7, () => {
  const k = mk('caio'), b = mk4('bruno');
  const svg = defs4 + arena() + `<g>${k.svg}</g><g>${b.svg}</g>` + dragonSvg('e4dr8') + knightSvg('e4kn8') + puffSvg('e4p8') + scoreSvg('e4sc8');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [4.2, 1.05]]), fx: 540, fy: 1050, tx: Math.sin(lt * 30) * (lt > 3.2 && lt < 3.5 ? 10 : 0) }),
    update(lt) {
      const lost = lt > 3.4;
      setChar(k.id, { x: 200, y: 1560, scale: .85, t: lt, mouth: lost ? 'frown' : 'shout', eyes: lost ? 'wide' : 'open', brow: lost ? 1 : -1, mad: !lost, sweat: lost, armL: 150, armR: lost ? 10 : 150, seed: 11 });
      setChar(b.id, { x: 920, y: 1560, scale: .9, t: lt, mouth: lt > 2.1 ? 'shout' : 'smug', eyes: 'half', brow: -1, armR: lt > 2.1 ? 150 : 20, armL: lt > 2.1 ? 150 : 20, seed: 12 });
      proj('e4dr8', lt, .1, 3.5, K(lt, [[.1, 250], [2.6, 290]]), 900, .85); animProj('e4dr8', lt);
      proj('e4kn8', lt, 2.1, 4.2, K(lt, [[2.1, 860], [3.0, 650]]), 850, K(lt, [[2.1, .6], [3.0, 1.0]]), true); animProj('e4kn8', lt);
      poof('e4p8', lt, 3.3, 320, 960, 1.4);
      score('e4sc8', lt, 540, 330, lost ? 'CAIO 0 x 2 BRUNO' : 'CAIO 0 x 1 BRUNO');
    }
  };
});

// 9. Caio perdendo: suor, saldo tremendo
shot(26.7, 28.9, () => {
  const k = mk('caio');
  const svg = arena() + `<g>${k.svg}</g>` + scoreSvg('e4sc9') + cardSvg('e4c9');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.75], [2.2, 1.95]]), fx: 540, fy: 1050 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1560, scale: 1.1, t: lt, mouth: 'frown', eyes: 'wide', brow: .8, sweat: 1, seed: 13, lookX: Math.sin(lt * 4) * 10, armL: 30, armR: 30 });
      score('e4sc9', lt, 540, 610, 'CAIO 0 x 2 BRUNO');
      card('e4c9', 26.7, lt, 540, 780, .6, 8);
    }
  };
});

// 10. concentração total: aura
shot(28.9, 31.7, () => {
  const k = mk('caio');
  let lines = ''; for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283; lines += `<path d="M${540 + Math.cos(a) * 420},${1000 + Math.sin(a) * 600} L${540 + Math.cos(a) * 900},${1000 + Math.sin(a) * 1300}" stroke="#fff" stroke-width="10" opacity=".7"/>`; }
  const svg = `<rect x="-200" y="-200" width="1480" height="2400" fill="#3c3766"/><g id="e4lines">${lines}</g>`
    + `<g id="e4aura">${[0, 1, 2].map(i => `<ellipse class="au" cx="540" cy="1150" rx="300" ry="440" fill="none" stroke="#ffd23f" stroke-width="${18 - i * 4}" opacity=".7"/>`).join('')}</g><g>${k.svg}</g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.2], [2.8, 1.5]]), fx: 540, fy: 1050, tx: Math.sin(lt * 40) * (lt > 1.5 ? 4 : 0) }),
    update(lt) {
      $('e4lines').setAttribute('transform', `rotate(${lt * 20},540,1000)`);
      document.querySelectorAll('.au').forEach((e, i) => { const p = ((lt * .9 + i / 3) % 1); e.setAttribute('transform', `translate(540,1150) scale(${.7 + p * .6}) translate(-540,-1150)`); e.setAttribute('opacity', (1 - p) * .9); });
      setChar(k.id, { x: 540, y: 1560, scale: 1.1, t: lt, mouth: 'flat', eyes: 'half', brow: -1, mad: lt > 1.2, armL: K(lt, [[0, 30], [.8, 160]]), armR: K(lt, [[0, 30], [.8, 160]]), squash: Math.sin(lt * 30) * .01 * (lt > 1.5 ? 1 : 0), seed: 14 });
    }
  };
});

// 11. a mãe do Bruno gigante: "BRUNO! JÁ PRA CASA!"; o cavaleiro some, o Bruno foge
shot(31.7, 34.3, () => {
  const b = mk4('bruno'), m = mk4('maeB');
  const svg = defs4 + arena() + `<g id="e4mom" ${GL}>${m.svg}</g><g>${b.svg}</g>` + knightSvg('e4kn11') + puffSvg('e4p11') + bubbleSvg('e4b11', 'BRUNO! JÁ PRA CASA!', 720, 60);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.6, 1.05]]), fx: 540, fy: 1000, tx: Math.sin(lt * 35) * (lt > .5 && lt < 1.3 ? 12 : 0) }),
    update(lt) {
      const k = backOut(lt / .45);
      setChar(m.id, { x: 380, y: 1150, scale: 1.9 * k, t: lt, mouth: 'shout', talk: lt > .3 && lt < 1.6, brow: -1, mad: 1, eyes: 'wide', armL: 150, seed: 15 });
      $('e4mom').setAttribute('opacity', .95);
      proj('e4kn11', lt, 0, .9, 820, 980, 1.0, true); animProj('e4kn11', lt);
      poof('e4p11', lt, .8, 820, 960, 1.4);
      const run = lt > 1.2;
      setChar(b.id, { x: K(lt, [[1.2, 860], [2.6, 1300]]), y: 1580, scale: .9, t: lt, mouth: 'O', eyes: 'wide', brow: 1, armL: run ? 150 : 40, armR: run ? 150 : 40, walk: run ? 3 : 0, lean: run ? 10 : 0, sweat: 1, seed: 16 });
      showBubble('e4b11', lt, .35, 2.6, 540, 640);
    }
  };
});

// 12. Caio vence: chuva de dinheiro, R$ 400
shot(34.3, 37.0, () => {
  const k = mk('caio'), f1 = mk('n1'), f2 = mk('n2');
  let notes = ''; for (let i = 0; i < 12; i++) notes += noteSvg('e4n12' + i, '50', '#f2b8a0', '#a8492a');
  const svg = arena() + `<g>${f1.svg}</g><g>${f2.svg}</g><g>${k.svg}</g>` + notes + bigNum('e4plus', '+R$ 200', 160, '#3fbf6a') + scoreSvg('e4sc12') + cardSvg('e4c12');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.7, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      setChar(f1.id, { x: 130, y: 1500, scale: .7, t: lt, mouth: 'smile', eyes: 'happy', armL: 160, armR: 160, hop: 3, seed: 17 });
      setChar(f2.id, { x: 950, y: 1500, scale: .7, t: lt + .3, mouth: 'smile', eyes: 'happy', armL: 160, armR: 160, hop: 3, seed: 18 });
      setChar(k.id, { x: 540, y: 1560, scale: 1.05, t: lt, mouth: 'smile', talk: lt < 2.4, eyes: 'money', armL: 165, armR: 165, hop: 2.6, seed: 19 });
      for (let i = 0; i < 12; i++) { const el = $('e4n12' + i); const p = lt - .2 - i * .1; if (p < 0) { el.setAttribute('display', 'none'); continue; } el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${60 + (i * 97) % 960 + Math.sin(p * 5 + i) * 40},${-100 + p * 700}) rotate(${Math.sin(p * 6 + i) * 30})`); }
      showPop('e4plus', lt, .5, 540, 760, 1);
      score('e4sc12', lt, 540, 140, 'CAIO VENCEU!');
      card('e4c12', 34.3, lt, 540, 330, 1.0, 0, .6);
    }
  };
});

// 13. "Só que eu esqueci de um detalhe…" — uma sombra cobre o Caio
shot(37.0, 39.8, () => {
  const k = mk('caio');
  const svg = arena() + `<g>${k.svg}</g><path id="e4shadow" d="M1300,0 L1300,1920 L700,1920 Q560,1300 760,700 Q820,300 1300,0 Z" fill="#1b1730" opacity="0"/>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.4], [2.8, 1.6]]), fx: 540, fy: 1100 }),
    update(lt) {
      const sh = K(lt, [[.8, 0], [2.2, 1]]);
      setChar(k.id, { x: 540, y: 1560, scale: 1.05, t: lt, mouth: sh > .5 ? 'o' : 'smile', eyes: sh > .5 ? 'wide' : 'happy', brow: sh > .5 ? 1 : 0, armL: lerp(150, 20, sh), armR: lerp(150, 20, sh), sweat: sh > .6, seed: 20, lookX: sh * 14 });
      $('e4shadow').setAttribute('opacity', sh * .55); $('e4shadow').setAttribute('transform', `translate(${(1 - sh) * 500},0)`);
    }
  };
});

// 14. a mãe do Caio: "CAIO! Que aposta é essa?"
shot(39.8, 42.3, () => {
  const k = mk('caio'), m = mk('mae');
  const svg = arena() + `<g>${k.svg}</g><g>${m.svg}</g>` + bubbleSvg('e4b14', 'CAIO! Que aposta é essa?', 640, 50);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.1], [2.5, 1.18]]), fx: 600, fy: 1100 }),
    update(lt) {
      setChar(m.id, { x: K(lt, [[0, 1200], [.6, 780]]), y: 1540, scale: 1.1, t: lt, mouth: 'shout', talk: lt > .6 && lt < 1.8, brow: -1, mad: 1, armR: lt > .6 ? 110 : 20, walk: lt < .6 ? 2 : 0, seed: 21, lookX: -12 });
      setChar(k.id, { x: 300, y: 1560, scale: 1.0, t: lt, mouth: 'O', eyes: 'wide', brow: 1, sweat: 1, squash: lt > .6 && lt < .9 ? -.05 : 0, capUp: K(lt, [[.6, 0], [.8, 60], [1.2, 0]]), seed: 22, lookX: 12 });
      showBubble('e4b14', lt, .6, 2.5, 600, 640);
    }
  };
});

// 15. o dinheiro vai pro cofrinho (com cadeado). Saldo: zero.
shot(42.3, 45.0, () => {
  const k = mk('caio'), m = mk('mae');
  let notes = ''; for (let i = 0; i < 5; i++) notes += noteSvg('e4n15' + i, '50', '#f2b8a0', '#a8492a');
  const pig = `<g id="e4pig"><ellipse cx="0" cy="0" rx="170" ry="120" fill="#ff9fb3" stroke="${OL}" stroke-width="9"/><ellipse cx="170" cy="10" rx="40" ry="48" fill="#ff8aa1" stroke="${OL}" stroke-width="8"/><circle cx="162" cy="0" r="8" fill="${OL}"/><circle cx="182" cy="18" r="8" fill="${OL}"/>
    <path d="M60,-110 L90,-170 L120,-100 Z" fill="#ff9fb3" stroke="${OL}" stroke-width="8"/><circle cx="90" cy="-30" r="12" fill="${OL}"/><rect x="-60" y="-125" width="100" height="16" rx="8" fill="${OL}"/>
    ${[-100, -30, 40, 100].map(x => `<rect x="${x - 20}" y="90" width="40" height="60" rx="14" fill="#ff9fb3" stroke="${OL}" stroke-width="7"/>`).join('')}
    <g id="e4lock" transform="translate(-40,40)"><path d="M-30,0 L-30,-40 Q-30,-75 0,-75 Q30,-75 30,-40 L30,0" fill="none" stroke="#8a8fa8" stroke-width="14"/><rect x="-50" y="-5" width="100" height="80" rx="12" fill="#f5c531" stroke="${OL}" stroke-width="7"/><circle cx="0" cy="30" r="10" fill="${OL}"/></g></g>`;
  const svg = arena() + `<g>${k.svg}</g><g>${m.svg}</g>` + pig + notes + cardSvg('e4c15') + tagSvg('e4t15', '-R$400', '#e8453c', 120);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.7, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      $('e4pig').setAttribute('transform', `translate(560,1330) scale(${backOut(lt / .35) * .8})`);
      $('e4lock').setAttribute('display', lt > 1.2 ? 'inline' : 'none');
      for (let i = 0; i < 5; i++) { const el = $('e4n15' + i); const p = clamp((lt - .3 - i * .12) / .5); el.setAttribute('display', p > 0 && p < 1 ? 'inline' : 'none'); el.setAttribute('transform', `translate(${lerp(330, 540, p)},${lerp(1150, 1220, p) - Math.sin(p * Math.PI) * 200}) rotate(${p * 200}) scale(${1 - p * .5})`); }
      setChar(m.id, { x: 860, y: 1540, scale: 1.1, t: lt, mouth: lt > 1.4 ? 'smug' : 'frown', eyes: lt > 1.4 ? 'happy' : 'half', brow: -.5, armR: 60, seed: 23 });
      setChar(k.id, { x: 270, y: 1560, scale: 1.0, t: lt, mouth: 'flat', eyes: 'half', brow: 0, armL: K(lt, [[0, 80], [.8, 10]]), seed: 24, lookX: 10 });
      card('e4c15', 42.3, lt, 540, 330, 1.05, 10, 0);
      popTag('e4t15', lt, .9, 540, 560, 1.2);
    }
  };
});
