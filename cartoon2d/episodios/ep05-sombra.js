// Episódio 5: "Na minha cidade, a sua sombra pode trabalhar por você."
// Caio põe a sombra pra trabalhar e fica rico na rede; ela pede aumento, ele nega, ela vai trabalhar pro Bruno.
// Sem sombra, ele compra um guarda-chuva… e a sombra do guarda-chuva cobra aluguel.
LINES = [
  [0.3, 2.8, 'Na minha cidade, a sua sombra pode trabalhar por você.'],
  [3.0, 4.8, 'Ela trabalha… e você recebe.'],
  [5.0, 7.4, 'Eu sou o Caio. E mandei a minha sombra trabalhar.'],
  [7.6, 8.4, 'Ela entregou pão.'],
  [8.55, 9.45, 'Passeou com cachorro.'],
  [9.55, 10.4, 'Lavou carro.'],
  [10.6, 12.8, 'E eu, na rede, ficando rico.'],
  [13.0, 15.0, 'Até que ela pediu aumento.'],
  [15.2, 16.8, 'Eu disse: “Não.”'],
  [17.0, 19.4, 'Ela fez as malas… e foi embora.'],
  [19.6, 22.0, 'Agora ela trabalha pro Bruno.'],
  [22.2, 24.6, 'E eu? Fiquei sem sombra.'],
  [24.8, 26.8, 'Comprei um guarda-chuva: cinquenta reais.'],
  [27.0, 29.8, 'E a sombra dele já chegou cobrando aluguel.'],
];

const STEPS = [[8.0, 100], [9.0, 200], [10.0, 300], [25.9, 250], [28.0, 230], [29.1, 210]];
const SALDO = t => { let v = 0; for (const [a, b] of STEPS) if (t >= a) v = b; return v; };
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => { const v = SALDO(t0 + lt); showCard(id, lt, from, x, y, v, v === 0 ? '#8a86a0' : (t0 + lt < 24 ? '#2fae60' : '#e8453c'), s, shake); };
const BRUNO = { kid: 1, skin: '#e0a27a', shirt: '#3fae6a', stripe: '#2f8a52', shorts: '#55556e', shoe: '#fff', hair: 'short', hairCol: '#1c1412', pocket: 0 };

// sombra-personagem: p = 0 deitada no chão (achatada e inclinada) … 1 em pé
const shadowMk = (extra = {}) => mk('sombra', extra);
function setShadow(sh, wrapId, st, p = 1) {
  $(wrapId).setAttribute('transform', `translate(${st.x},${st.y}) skewX(${lerp(-38, 0, p)}) scale(1,${lerp(-.3, 1, p)})`);
  $(wrapId).setAttribute('opacity', .9);
  setChar(sh.id, { ...st, x: 0, y: 0 });
  document.querySelector(`#${sh.id} > ellipse`).setAttribute('display', 'none');
}
const sun = id => { let r = ''; for (let i = 0; i < 10; i++) r += `<rect x="-10" y="-200" width="20" height="56" rx="10" fill="#ffd23f" stroke="${OL}" stroke-width="5" transform="rotate(${i * 36})"/>`; return `<g id="${id}">${r}<circle r="110" fill="#ffd23f" stroke="${OL}" stroke-width="8"/></g>`; };
const spinSun = (id, lt, x, y) => $(id).setAttribute('transform', `translate(${x},${y}) rotate(${lt * 25})`);
const box = (x, y, w = 150, h = 110) => `<rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" rx="8" fill="#d6a86a" stroke="${OL}" stroke-width="7"/><path d="M${x - w / 2},${y - h / 2 + 30} L${x + w / 2},${y - h / 2 + 30} M${x},${y - h / 2} L${x},${y - h / 2 + 30}" stroke="#a87a3e" stroke-width="6"/>`;
const longShadow = (x, y, w = 120, len = 260) => `<path d="M${x - w / 2},${y} L${x + w / 2},${y} L${x + w / 2 + len},${y + 70} L${x - w / 2 + len},${y + 70} Z" fill="#2b2745" opacity=".5"/>`;
const hammock = () => `<rect x="70" y="880" width="40" height="620" fill="#8a5a3a" stroke="${OL}" stroke-width="7"/><rect x="970" y="880" width="40" height="620" fill="#8a5a3a" stroke="${OL}" stroke-width="7"/>
  <circle cx="90" cy="820" r="130" fill="#6fbf6a" stroke="${OL}" stroke-width="${SW}"/><circle cx="990" cy="820" r="130" fill="#6fbf6a" stroke="${OL}" stroke-width="${SW}"/>`;
const hammockNet = `<path d="M110,1040 Q540,1500 970,1040 L970,1080 Q540,1560 110,1080 Z" fill="#e8453c" stroke="${OL}" stroke-width="8"/><path d="M110,1060 Q540,1530 970,1060" fill="none" stroke="#ffd23f" stroke-width="12" stroke-dasharray="30 20"/>`;
const umbrella = id => `<g id="${id}"><path d="M-260,0 Q-250,-210 0,-230 Q250,-210 260,0 Q200,-40 130,0 Q65,-40 0,0 Q-65,-40 -130,0 Q-200,-40 -260,0 Z" fill="#e8453c" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
  <path d="M-130,0 Q-110,-150 0,-230 M130,0 Q110,-150 0,-230" fill="none" stroke="#fff" stroke-width="10" opacity=".7"/><circle cy="-236" r="14" fill="#ffd23f" stroke="${OL}" stroke-width="6"/>
  <path d="M0,-10 L0,360 Q0,400 -36,400 Q-60,400 -60,374" fill="none" stroke="${OL}" stroke-width="14" stroke-linecap="round"/></g>`;

// 1. gancho: o moço cochila, a sombra dele carrega caixas e ganha por ele
shot(0, 2.9, () => {
  const n = mk('n1', { sit: 1 }), sh = shadowMk({ hair: 'short', kid: 0 });
  let coins = ''; for (let i = 0; i < 3; i++) coins += coinSvg('e5k1' + i);
  const svg = sky() + sun('e5sun1') + backBuildings() + house(-40, 420, 560, '#a8d8c7') + house(400, 360, 500, '#f2c29b', { doorCol: '#4a6fa5', winX: 190 }) + house(780, 360, 540, '#c9b6e4') + street()
    + `<rect x="80" y="1360" width="420" height="40" rx="12" fill="#c98a52" stroke="${OL}" stroke-width="6"/><rect x="110" y="1400" width="26" height="80" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/><rect x="444" y="1400" width="26" height="80" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/>`
    + `<g>${n.svg}</g><text id="e5z" x="380" y="900" font-family="Luckiest" font-size="70" fill="#8a86a0" stroke="${OL}" stroke-width="6" paint-order="stroke">Zzz</text>`
    + `<g id="e5w1">${sh.svg}</g><g id="e5bx1">${box(0, 0)}</g>` + coins + tagSvg('e5t1', '+R$10', '#2fae60', 110);
  return {
    svg, cam: lt => ({ s: lerp(3.0, 1.05, easeOut(lt / 1.0)), fx: 700, fy: 1000, blur: lt < .8 ? 22 * (1 - lt / .8) : 0 }),
    update(lt) {
      spinSun('e5sun1', lt, 900, 300);
      setChar(n.id, { x: 290, y: 1400, scale: .85, t: lt, mouth: 'smug', eyes: 'happy', tilt: -8 + Math.sin(lt * 2) * 3, seed: 1 });
      $('e5z').setAttribute('transform', `translate(0,${-((lt * 40) % 60)})`); $('e5z').setAttribute('opacity', .5 + .5 * Math.sin(lt * 4));
      const sx = K(lt, [[0, 700], [2.9, 820]]);
      setShadow(sh, 'e5w1', { x: sx, y: 1500, scale: .85, t: lt, mouth: 'flat', armL: 160, armR: 160, walk: 1.6, seed: 2 });
      $('e5bx1').setAttribute('transform', `translate(${sx},${1500 - 600 * .85 - 20 - Math.abs(Math.sin(lt * 1.6 * 3.14)) * 10})`);
      for (let i = 0; i < 3; i++) flyCoin('e5k1' + i, lt, .9 + i * .5, sx, 1100, 300, 1180, .6, 160);
      popTag('e5t1', lt, 1.2, 290, 820, 1.4);
    }
  };
});

// 2. outra sombra varre a calçada enquanto a dona toma suco
shot(2.9, 4.9, () => {
  const c = mk('cida', { sit: 1, shorts: '#e86fa0' }), sh = shadowMk({ hair: 'bun', kid: 0, dress: '#3b3558', hairCol: '#3b3558' });
  let coins = ''; for (let i = 0; i < 3; i++) coins += coinSvg('e5k2' + i);
  const svg = sky() + sun('e5sun2') + house(-60, 1200, 900, '#f2c29b', { roof: false, doorX: 760, winX: 120, winY: 220 }) + street()
    + `<rect x="120" y="1300" width="330" height="40" rx="14" fill="#5fb3e0" stroke="${OL}" stroke-width="6"/>` + `<g>${c.svg}</g>`
    + `<g><rect x="370" y="1160" width="56" height="80" rx="10" fill="#ffb02e" stroke="${OL}" stroke-width="6"/><path d="M400,1160 L420,1100" stroke="#e8453c" stroke-width="8"/></g>`
    + `<g id="e5w2">${sh.svg}</g><g id="e5broom"><path d="M0,-260 L0,0" stroke="#8a5a3a" stroke-width="16"/><path d="M-50,0 L50,0 L70,70 L-70,70 Z" fill="#e8c46a" stroke="${OL}" stroke-width="6"/></g>` + coins;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.1], [2, 1.2]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun2', lt, 860, 300);
      setChar(c.id, { x: 280, y: 1380, scale: .85, t: lt, mouth: 'smile', eyes: 'happy', shades: 1, armL: 70, seed: 3 });
      const sw = Math.sin(lt * 6);
      setShadow(sh, 'e5w2', { x: 760, y: 1500, scale: .9, t: lt, mouth: 'flat', armR: 40 + sw * 25, armL: 40 + sw * 25, lean: sw * 3, seed: 4 });
      $('e5broom').setAttribute('transform', `translate(${700 + sw * 60},1500) rotate(${sw * 20})`);
      for (let i = 0; i < 3; i++) flyCoin('e5k2' + i, lt, .3 + i * .5, 760, 1100, 300, 1100, .6, 150);
    }
  };
});

// 3. Caio descola a sombra do chão
shot(4.9, 7.5, () => {
  const k = mk('caio'), sh = shadowMk();
  const svg = sky() + sun('e5sun3') + backBuildings() + house(-60, 1200, 700, '#a8d8c7', { roof: false, doorX: 820, winX: 80, winY: 140 }) + street() + `<g id="e5w3">${sh.svg}</g><g>${k.svg}</g>` + cardSvg('e5c3');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.6, 1.15]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun3', lt, 880, 280);
      const p = K(lt, [[.5, 0], [1.4, 1]]);
      setChar(k.id, { x: 330, y: 1480, scale: 1.0, t: lt, mouth: 'smile', talk: lt < 2.3, eyes: p > .9 ? 'happy' : 'open', armL: K(lt, [[0, 20], [.4, 90], [1.4, 90], [1.8, 30]]), seed: 5, lookX: 10 });
      setShadow(sh, 'e5w3', { x: lerp(340, 760, p), y: 1490, scale: 1.0, t: lt, mouth: 'smile', eyes: 'open', armR: lt > 1.5 ? 160 : 10, seed: 6, lookX: -10 }, p);
      card('e5c3', 4.9, lt, 540, 360, 1.0, 0, 1.6);
    }
  };
});

// 4. montagem: pão, cachorro, carro (+R$ 100 cada)
shot(7.5, 10.5, () => {
  const s1 = shadowMk(), s2 = shadowMk(), s3 = shadowMk();
  const bread = `<g id="e5bread"><path d="M-60,-40 L60,-40 L70,90 L-70,90 Z" fill="#d6a86a" stroke="${OL}" stroke-width="7"/>${[-30, 0, 30].map((x, i) => `<rect x="${x - 14}" y="${-120 + i * 10}" width="28" height="110" rx="14" fill="#e8b46a" stroke="${OL}" stroke-width="5" transform="rotate(${(i - 1) * 12},${x},-40)"/>`).join('')}</g>`;
  const car = `<g id="e5car"><path d="M-300,60 L-300,-20 Q-290,-60 -230,-70 L-150,-150 Q-120,-180 -60,-180 L110,-180 Q160,-180 190,-140 L240,-70 Q300,-60 300,0 L300,60 Z" fill="#5fb3e0" stroke="${OL}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M-130,-80 L-80,-150 L20,-150 L20,-80 Z M50,-80 L50,-150 L140,-150 L190,-80 Z" fill="#cdeaf5" stroke="${OL}" stroke-width="6"/>${[-180, 180].map(x => `<circle cx="${x}" cy="60" r="56" fill="#2b2745" stroke="${OL}" stroke-width="6"/><circle cx="${x}" cy="60" r="22" fill="#c3c9d6"/>`).join('')}</g>`;
  let foam = ''; for (let i = 0; i < 8; i++) foam += `<circle class="e5fm" r="${20 + (i % 3) * 8}" fill="#fff" stroke="${OL}" stroke-width="4" opacity=".9"/>`;
  const sub = [
    `<g id="e5s4a">${sky() + backBuildings() + house(-40, 1160, 600, '#f2d48a', { roof: false, door: false, winX: 160, winY: 120 }) + street()}<text x="540" y="900" text-anchor="middle" font-family="Luckiest" font-size="96" fill="#c97a2e" stroke="${OL}" stroke-width="8" paint-order="stroke">PADARIA</text><g id="e5w4a">${s1.svg}</g>${bread}</g>`,
    `<g id="e5s4b">${sky() + backBuildings() + street()}<g id="e5w4b">${s2.svg}</g>${dogSvg('e5dog')}<path id="e5leash" fill="none" stroke="#e8453c" stroke-width="7"/></g>`,
    `<g id="e5s4c">${sky() + backBuildings() + house(-40, 1160, 600, '#c9b6e4', { roof: false, door: false, winX: 760, winY: 120 }) + street()}${car}<g id="e5w4c">${s3.svg}</g><g id="e5foam">${foam}</g></g>`,
  ];
  const svg = sub.join('') + tagSvg('e5t4', '+R$100', '#2fae60', 120) + cardSvg('e5c4');
  return {
    svg, cam: lt => { const i = Math.min(2, Math.floor(lt / 1.0)), l = lt - i; return { s: 1.05 + l * .05, fx: 540, fy: 1100, blur: l < .08 && i > 0 ? 18 : 0, blurX: 1 }; },
    update(lt) {
      const i = Math.min(2, Math.floor(lt / 1.0)), l = lt - i;
      ['e5s4a', 'e5s4b', 'e5s4c'].forEach((n, j) => $(n).setAttribute('display', j === i ? 'inline' : 'none'));
      const x1 = K(l, [[0, 200], [1, 640]]);
      setShadow(s1, 'e5w4a', { x: x1, y: 1490, scale: 1.0, t: lt, mouth: 'smile', armL: 70, walk: 2, seed: 7 });
      $('e5bread').setAttribute('transform', `translate(${x1 + 150},${1240 + Math.abs(Math.sin(lt * 6)) * -8})`);
      const x2 = K(l, [[0, 260], [1, 520]]);
      setShadow(s2, 'e5w4b', { x: x2, y: 1490, scale: 1.0, t: lt, mouth: 'smile', armL: 50, walk: 2, seed: 8 });
      setDog('e5dog', lt, x2 + 300, 1500, .8, 'happy');
      $('e5leash').setAttribute('d', `M${x2 + 110},1240 Q${x2 + 230},1330 ${x2 + 300},1360`);
      const w = Math.sin(lt * 9);
      setShadow(s3, 'e5w4c', { x: 760, y: 1490, scale: 1.0, t: lt, mouth: 'smile', armR: 90 + w * 30, seed: 9 });
      $('e5car').setAttribute('transform', 'translate(380,1420) scale(.9)');
      document.querySelectorAll('.e5fm').forEach((f, j) => { const p = (lt * .8 + j * .13) % 1; f.setAttribute('cx', 200 + j * 60 + Math.sin(p * 6 + j) * 20); f.setAttribute('cy', 1300 - p * 300); f.setAttribute('opacity', 1 - p); });
      popTag('e5t4', l, .45, 760, 760, .55);
      card('e5c4', 7.5, lt, 540, 300, .95);
    }
  };
});

// 5. Caio na rede, de óculos escuros, ficando rico
shot(10.5, 12.9, () => {
  const k = mk('caio', { sit: 1 });
  let coins = ''; for (let i = 0; i < 6; i++) coins += coinSvg('e5k5' + i);
  const svg = sky() + sun('e5sun5') + hammock() + street() + `<g>${k.svg}</g>` + hammockNet + coins + cardSvg('e5c5');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.4, 1.15]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun5', lt, 880, 280);
      setChar(k.id, { x: 540 + Math.sin(lt * 2) * 20, y: 1330, scale: 1.0, t: lt, mouth: 'smile', shades: 1, armL: 150, armR: 150, lean: Math.sin(lt * 2) * 4, seed: 10 });
      for (let i = 0; i < 6; i++) flyCoin('e5k5' + i, lt, .1 + i * .35, 1100, 900, 540, 1200, .6, 200);
      card('e5c5', 10.5, lt, 540, 330, 1.15, 0, 0);
    }
  };
});

// 6. a sombra entra em greve: "QUERO AUMENTO!"
shot(12.9, 15.1, () => {
  const sh = shadowMk();
  const svg = sky() + sun('e5sun6') + backBuildings() + house(-60, 1200, 700, '#a8d8c7', { roof: false, door: false, winX: 80, winY: 120 }) + street()
    + `<g id="e5w6">${sh.svg}</g><g id="e5sign"><rect x="-8" y="0" width="16" height="320" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/><rect x="-220" y="-150" width="440" height="170" rx="12" fill="#fff" stroke="${OL}" stroke-width="8"/>
      <text y="-80" text-anchor="middle" font-family="Luckiest" font-size="60" fill="#e8453c">QUERO</text><text y="-8" text-anchor="middle" font-family="Luckiest" font-size="60" fill="#e8453c">AUMENTO!</text></g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2.2, 1.3]]), fx: 540, fy: 1050 }),
    update(lt) {
      spinSun('e5sun6', lt, 900, 260);
      const up = Math.abs(Math.sin(lt * 5));
      setShadow(sh, 'e5w6', { x: 560, y: 1490, scale: 1.1, t: lt, mouth: 'shout', talk: 1, brow: -1, mad: 1, eyes: 'open', armR: 150 + up * 10, armL: 20, hop: 2.5, seed: 11 });
      $('e5sign').setAttribute('transform', `translate(330,${760 - up * 30}) rotate(${Math.sin(lt * 5) * 5}) scale(${backOut(lt / .3)})`);
    }
  };
});

// 7. "Não."
shot(15.1, 16.9, () => {
  const k = mk('caio', { sit: 1 });
  const svg = sky() + sun('e5sun7') + hammock() + street() + `<g>${k.svg}</g>` + hammockNet + bubbleSvg('e5b7', 'Não.', 240, 66);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.6], [1.8, 1.75]]), fx: 540, fy: 1000 }),
    update(lt) {
      spinSun('e5sun7', lt, 880, 280);
      setChar(k.id, { x: 540, y: 1330, scale: 1.0, t: lt, mouth: 'smug', talk: lt > .2 && lt < .7, shades: 1, armL: 150, armR: 150, seed: 12, tilt: 6 });
      showBubble('e5b7', lt, .2, 1.8, 600, 640);
    }
  };
});

// 8. a sombra faz as malas e vai embora
shot(16.9, 19.5, () => {
  const k = mk('caio', { sit: 1 }), sh = shadowMk();
  const svg = sky('#f3c69a') + backBuildings('#d9a9a0', '#f2d0b8') + hammock() + street() + `<g>${k.svg}</g>` + hammockNet + `<g id="e5w8">${sh.svg}</g>`
    + `<g id="e5bag"><rect x="-70" y="-50" width="140" height="100" rx="14" fill="#8a5a3a" stroke="${OL}" stroke-width="7"/><path d="M-30,-50 Q0,-90 30,-50" fill="none" stroke="${OL}" stroke-width="8"/><rect x="-70" y="-6" width="140" height="12" fill="#e8c46a"/></g>`;
  return {
    svg, cam: lt => ({ s: 1.0, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1330, scale: .9, t: lt, mouth: lt > 1.2 ? 'o' : 'smug', shades: lt < 1.2, eyes: lt > 1.2 ? 'wide' : 'open', armL: lt > 1.2 ? 40 : 150, armR: lt > 1.2 ? 40 : 150, seed: 13, lookX: 12 });
      const x = K(lt, [[0, 560], [2.6, 1060]]);
      setShadow(sh, 'e5w8', { x, y: 1560, scale: .95, t: lt, mouth: 'smug', eyes: 'half', brow: -.5, armL: 20, armR: 30, walk: 1.5, seed: 14, lookX: -8 });
      $('e5bag').setAttribute('transform', `translate(${x - 120},${1450 - Math.abs(Math.sin(lt * 1.5 * 3.14)) * 10})`);
    }
  };
});

// 9. agora ela trabalha pro Bruno (que tem DUAS sombras)
shot(19.5, 22.1, () => {
  const b = mk('caio', { ...BRUNO, sit: 1 }), s1 = shadowMk(), s2 = shadowMk({ hair: 'short', hairCol: '#3b3558' });
  let coins = ''; for (let i = 0; i < 6; i++) coins += coinSvg('e5k9' + i);
  const svg = sky() + sun('e5sun9') + backBuildings() + house(-60, 1200, 700, '#c9e4b5', { roof: false, door: false, winX: 860, winY: 120 }) + street()
    + `<rect x="140" y="1300" width="380" height="40" rx="14" fill="#ffd23f" stroke="${OL}" stroke-width="6"/>` + `<g>${b.svg}</g><g id="e5w9a">${s1.svg}</g><g id="e5w9b">${s2.svg}</g><g id="e5bx9a">${box(0, 0)}</g><g id="e5bx9b">${box(0, 0)}</g>` + coins + bigNum('e5bn', 'BRUNO', 110, '#3fbf6a');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.6, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun9', lt, 900, 280);
      setChar(b.id, { x: 330, y: 1380, scale: .85, t: lt, mouth: 'smile', eyes: 'money', shades: 0, armL: 150, armR: 150, seed: 15 });
      const xa = K(lt, [[0, 640], [2.6, 760]]), xb = K(lt, [[0, 880], [2.6, 960]]);
      setShadow(s1, 'e5w9a', { x: xa, y: 1520, scale: .8, t: lt, mouth: 'flat', eyes: 'half', armL: 160, armR: 160, walk: 1.6, seed: 16 });
      setShadow(s2, 'e5w9b', { x: xb, y: 1520, scale: .8, t: lt + .4, mouth: 'flat', eyes: 'half', armL: 160, armR: 160, walk: 1.6, seed: 17 });
      $('e5bx9a').setAttribute('transform', `translate(${xa},${1520 - 500 * .8 - 40})`); $('e5bx9b').setAttribute('transform', `translate(${xb},${1520 - 500 * .8 - 40})`);
      for (let i = 0; i < 6; i++) flyCoin('e5k9' + i, lt, .2 + i * .35, i % 2 ? xb : xa, 1100, 330, 1150, .6, 170);
      showPop('e5bn', lt, 99, 0, 0);
    }
  };
});

// 10. Caio sem sombra no sol; todo mundo assustado
shot(22.1, 24.7, () => {
  const k = mk('caio'), a = mk('n1'), c = mk('cida');
  const svg = sky() + sun('e5sun10') + backBuildings() + house(-40, 420, 560, '#a8d8c7') + house(400, 360, 500, '#f2c29b', { doorCol: '#4a6fa5', winX: 190 }) + house(780, 360, 540, '#c9b6e4') + street()
    + longShadow(160, 1470, 140, 200) + longShadow(900, 1470, 140, 160) + `<g>${a.svg}</g><g>${c.svg}</g><g>${k.svg}</g>`
    + `<text id="e5q1" x="160" y="900" text-anchor="middle" font-family="Luckiest" font-size="110" fill="#e8453c" stroke="${OL}" stroke-width="8" paint-order="stroke">?!</text><text id="e5q2" x="900" y="900" text-anchor="middle" font-family="Luckiest" font-size="110" fill="#e8453c" stroke="${OL}" stroke-width="8" paint-order="stroke">?!</text>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.6, 1.08]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun10', lt, 540, 260);
      setChar(a.id, { x: 160, y: 1490, scale: .8, t: lt, mouth: 'O', eyes: 'wide', brow: 1, armR: 100, seed: 18, lookX: 12 });
      setChar(c.id, { x: 900, y: 1490, scale: .8, t: lt, mouth: 'O', eyes: 'wide', brow: 1, armL: 100, seed: 19, lookX: -12 });
      setChar(k.id, { x: 540, y: 1490, scale: 1.0, t: lt, mouth: 'frown', eyes: 'open', brow: .6, sweat: 1, seed: 20, lookY: 8 });
      document.querySelector(`#${k.id} > ellipse`).setAttribute('display', 'none');
      for (const q of ['e5q1', 'e5q2']) $(q).setAttribute('transform', `translate(0,${Math.sin(lt * 6) * 8})`), $(q).setAttribute('opacity', clamp((lt - .4) * 3));
    }
  };
});

// 11. compra um guarda-chuva: -R$ 50
shot(24.7, 26.9, () => {
  const k = mk('caio'), v = mk('jair');
  const svg = sky() + sun('e5sun11') + backBuildings() + street()
    + `<rect x="560" y="1050" width="460" height="300" fill="#3f9a5f" stroke="${OL}" stroke-width="${SW}"/><rect x="560" y="900" width="460" height="150" rx="10" fill="#fffbe9" stroke="${OL}" stroke-width="${SW}"/>
      <text x="790" y="960" text-anchor="middle" font-family="Luckiest" font-size="50" fill="${OL}">GUARDA-CHUVA</text><text x="790" y="1030" text-anchor="middle" font-family="Luckiest" font-size="64" fill="#e8453c">R$ 50</text>`
    + `<g>${v.svg}</g><g>${k.svg}</g>` + noteSvg('e5n11', '50', '#f2b8a0', '#a8492a') + tagSvg('e5t11', '-R$50') + cardSvg('e5c11');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.2, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      spinSun('e5sun11', lt, 300, 280);
      setChar(v.id, { x: 790, y: 1480, scale: .9, t: lt, mouth: 'smile', eyes: 'happy', armR: 60, seed: 21 });
      setChar(k.id, { x: 330, y: 1490, scale: 1.0, t: lt, mouth: 'flat', eyes: 'half', armL: K(lt, [[0, 20], [.6, 80], [1.4, 20]]), seed: 22, lookX: 12 });
      flyNote('e5n11', lt, .6, 420, 1150, 700, 1100, .7);
      popTag('e5t11', lt, .7, 330, 760, 1.2);
      card('e5c11', 24.7, lt, 540, 320, 1.0, 8, 0);
    }
  };
});

// 12. a sombra do guarda-chuva cobra aluguel
shot(26.9, 30.0, () => {
  const k = mk('caio');
  let notes = ''; for (let i = 0; i < 2; i++) notes += noteSvg('e5n12' + i, '20', '#f2d38a', '#9a6a1a');
  const svg = sky() + sun('e5sun12') + backBuildings() + house(-60, 1200, 700, '#c9b6e4', { roof: false, door: false, winX: 80, winY: 120 }) + street()
    + `<g id="e5ush"><ellipse cx="0" cy="0" rx="270" ry="60" fill="#2b2745" opacity=".85"/>${[-1, 1].map(s => `<ellipse cx="${s * 50}" cy="-8" rx="20" ry="16" fill="#fff"/><circle cx="${s * 50}" cy="-6" r="9" fill="#1b1420"/>`).join('')}
      <g id="e5rent"><rect x="160" y="-210" width="300" height="120" rx="12" fill="#fff" stroke="${OL}" stroke-width="7"/><text x="310" y="-160" text-anchor="middle" font-family="Luckiest" font-size="42" fill="${OL}">ALUGUEL</text><text x="310" y="-108" text-anchor="middle" font-family="Luckiest" font-size="42" fill="#e8453c">R$ 20/DIA</text><path d="M200,-90 L190,-20" stroke="${OL}" stroke-width="7"/></g></g>`
    + `<g>${k.svg}</g>` + umbrella('e5umb') + notes + tagSvg('e5t12a', '-R$20') + tagSvg('e5t12b', '-R$20') + cardSvg('e5c12');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [3.1, 1.16]]), fx: 540, fy: 1150 }),
    update(lt) {
      spinSun('e5sun12', lt, 880, 260);
      setChar(k.id, { x: 470, y: 1460, scale: 1.0, t: lt, mouth: lt > 1.2 ? 'flat' : 'smile', eyes: lt > 1.2 ? 'half' : 'open', armL: 115, seed: 23, lookY: lt > 1.2 ? 8 : 0 });
      document.querySelector(`#${k.id} > ellipse`).setAttribute('display', 'none');
      $('e5umb').setAttribute('transform', `translate(${560 + Math.sin(lt * 2) * 6},${800}) rotate(${Math.sin(lt * 2) * 3})`);
      $('e5ush').setAttribute('transform', `translate(520,1520) scale(${K(lt, [[0, .9], [.6, 1]])})`);
      $('e5rent').setAttribute('transform', `scale(${backOut((lt - .7) / .3)})`);
      flyNote('e5n120', lt, 1.0, 470, 1200, 900, 1450, .7); popTag('e5t12a', lt, 1.1, 300, 760, 1.0);
      flyNote('e5n121', lt, 2.1, 470, 1200, 900, 1450, .7); popTag('e5t12b', lt, 2.2, 300, 760, .8);
      card('e5c12', 26.9, lt, 540, 320, 1.0, 8, 0);
    }
  };
});
