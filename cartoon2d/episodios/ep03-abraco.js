// Episódio 3: "Na minha cidade, abraço de verdade vale dez reais. Abraço falso custa dez."
// Caio quer um videogame, abraça todo mundo por interesse e perde dinheiro; no aniversário esquecido do avô,
// abraça de verdade e ganha R$ 1.000. Final: "Vô… mais um?" "Esse aí já é por interesse."
LINES = [
  [0.3, 3.0, 'Na minha cidade, abraço de verdade vale dez reais.'],
  [3.2, 5.0, 'Abraço falso… custa dez.'],
  [5.2, 8.0, 'Eu sou o Caio. E eu queria um videogame de trezentos reais.'],
  [8.2, 9.8, 'Então eu saí abraçando todo mundo.'],
  [10.0, 12.4, 'O carteiro. A professora. Até o cachorro.'],
  [12.6, 14.6, 'Tudo abraço falso. Sobrou vinte.'],
  [14.8, 17.2, 'Aí eu vi o meu avô, sozinho na praça.'],
  [17.4, 19.6, 'Era aniversário dele. Ninguém lembrou.'],
  [19.8, 22.0, 'Eu esqueci o videogame. E só abracei.'],
  [22.2, 24.4, 'Abraço de neto: mil reais!'],
  [24.6, 26.4, '“Vô… mais um?”'],
  [26.6, 29.8, '“Esse aí já é por interesse.” Menos dez.'],
];

const STEPS = [[6.6, 50], [10.3, 40], [11.1, 30], [11.9, 20], [22.6, 20], [27.6, 1010]];
const SALDO = t => {
  let v = 50; for (const [a, b] of STEPS) if (t >= a) v = b;
  if (t >= 22.6 && t < 23.8) v = Math.round(20 + 1000 * easeOut((t - 22.6) / 1.2)); else if (t >= 23.8 && t < 27.6) v = 1020;
  return v;
};
const saldoCol = v => v <= 20 ? '#e8453c' : '#2fae60';
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => showCard(id, lt, from, x, y, SALDO(t0 + lt), saldoCol(SALDO(t0 + lt)), s, shake);
let HC = 0; const hearts = n => { const p = 'h' + (HC++) + '_'; let s = ''; for (let i = 0; i < n; i++) s += heartSvg(p + i); return [p, s]; };
const praca = (dusk = 0) => {
  const skyC = dusk ? '#f3b48a' : '#d7edf0';
  return `<rect x="-200" y="-200" width="1480" height="2400" fill="${skyC}"/>${dusk ? '<circle cx="820" cy="760" r="160" fill="#ffd9a0" opacity=".8"/>' : ''}`
    + backBuildings(dusk ? '#c98fa0' : '#bdb6da', dusk ? '#f2c6a8' : '#d6d1ec')
    + `<g>${[120, 960].map(x => `<rect x="${x - 22}" y="900" width="44" height="440" fill="#8a5a3a" stroke="${OL}" stroke-width="6"/><circle cx="${x}" cy="860" r="150" fill="${dusk ? '#6f9a5a' : '#6fbf6a'}" stroke="${OL}" stroke-width="${SW}"/><circle cx="${x - 70}" cy="800" r="40" fill="${dusk ? '#86ad6c' : '#8fd47f'}"/>`).join('')}</g>`
    + street();
};
const bench = (x, y) => `<rect x="${x - 230}" y="${y - 170}" width="460" height="34" rx="10" fill="#c98a52" stroke="${OL}" stroke-width="6"/><rect x="${x - 230}" y="${y - 120}" width="460" height="34" rx="10" fill="#c98a52" stroke="${OL}" stroke-width="6"/>
  <rect x="${x - 250}" y="${y - 70}" width="500" height="40" rx="12" fill="#c98a52" stroke="${OL}" stroke-width="7"/><rect x="${x - 210}" y="${y - 30}" width="26" height="60" fill="#5a3d2a" stroke="${OL}" stroke-width="5"/><rect x="${x + 184}" y="${y - 30}" width="26" height="60" fill="#5a3d2a" stroke="${OL}" stroke-width="5"/>`;
// abraço: dois personagens se aproximam, braços envolvem, apertam (squash)
const hug = (lt, tIn, tOut = 99) => { const p = K(lt, [[tIn - .3, 0], [tIn, 1], [tOut, 1], [tOut + .3, 0]]); return { p, sq: Math.sin(clamp((lt - tIn) / .5) * Math.PI) * .05 * p }; };

// 1. gancho: abraço de verdade = +R$10 e corações
shot(0, 3.1, () => {
  const a = mk('cida'), b = mk('n2'); const [hp, hs] = hearts(7);
  let notes = ''; for (let i = 0; i < 3; i++) notes += noteSvg('e3n1' + i);
  const svg = praca() + `<g>${b.svg}</g><g>${a.svg}</g>` + hs + notes + tagSvg('e3t1', '+R$10', '#2fae60', 120);
  return {
    svg, cam: lt => ({ s: lerp(3.0, 1.15, easeOut(lt / 1.0)), fx: 540, fy: 1050, blur: lt < .8 ? 22 * (1 - lt / .8) : 0 }),
    update(lt) {
      const h = hug(lt, .7);
      setChar(b.id, { x: K(lt, [[0, 760], [.7, 620]]), y: 1480, scale: .95, t: lt, mouth: 'smile', eyes: h.p > .5 ? 'happy' : 'open', armR: lerp(10, 100, h.p), lean: -6 * h.p, squash: h.sq, seed: 1, walk: lt < .7 ? 1.6 : 0 });
      setChar(a.id, { x: K(lt, [[0, 300], [.7, 450]]), y: 1480, scale: .95, t: lt, mouth: 'smile', eyes: h.p > .5 ? 'happy' : 'open', armL: lerp(10, 100, h.p), lean: 6 * h.p, squash: h.sq, seed: 2, walk: lt < .7 ? 1.6 : 0 });
      floatHearts(hp, 7, lt, .8, 540, 860);
      for (let i = 0; i < 3; i++) flyNote('e3n1' + i, lt, 1.1 + i * .2, 540, 300, 300 + i * 240, 900, 1.2);
      popTag('e3t1', lt, 1.2, 540, 560, 1.5);
    }
  };
});

// 2. abraço falso = -R$10
shot(3.1, 5.1, () => {
  const j = mk('jair'), n = mk('n1');
  const svg = praca() + `<g>${n.svg}</g><g>${j.svg}</g>` + noteSvg('e3n2') + tagSvg('e3t2', '-R$10', '#e8453c', 120)
    + `<g id="e3cl"><circle cx="-60" r="60" fill="#9aa3b5" stroke="${OL}" stroke-width="6"/><circle cx="20" cy="-30" r="70" fill="#9aa3b5" stroke="${OL}" stroke-width="6"/><circle cx="90" r="55" fill="#9aa3b5" stroke="${OL}" stroke-width="6"/><rect x="-110" y="0" width="240" height="55" fill="#9aa3b5"/></g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2, 1.25]]), fx: 540, fy: 1050 }),
    update(lt) {
      const h = hug(lt, .35);
      setChar(n.id, { x: 640, y: 1480, scale: .95, t: lt, mouth: 'flat', eyes: 'half', armR: lerp(10, 70, h.p), lean: -3 * h.p, seed: 3, lookX: -8 });
      setChar(j.id, { x: 430, y: 1480, scale: .95, t: lt, mouth: 'smile', eyes: 'open', sweat: 1, armL: lerp(10, 95, h.p), lean: 4 * h.p, squash: h.sq, seed: 4, lookX: 12 });
      flyNote('e3n2', lt, .8, 500, 1200, 900, 560, .9); popTag('e3t2', lt, .9, 760, 860, 1.0);
      $('e3cl').setAttribute('transform', `translate(${K(lt, [[0, 380], [2, 560]])},${560 + Math.sin(lt * 3) * 8}) scale(${backOut(lt / .4)})`);
    }
  };
});

// 3. Caio na vitrine: videogame R$ 300, saldo R$ 50
shot(5.1, 8.1, () => {
  const k = mk('caio'); let sp = ''; for (let i = 0; i < 4; i++) sp += `<g id="e3sp3${i}">${sparkle(200 + i * 230, 520 + (i % 2) * 90, .9)}</g>`;
  const svg = sky() + `<rect x="-60" y="200" width="1200" height="1140" fill="#e86f6f" stroke="${OL}" stroke-width="${SW}"/><rect x="-60" y="200" width="1200" height="150" fill="#2b2745"/><text x="540" y="305" text-anchor="middle" font-family="Luckiest" font-size="92" fill="#ffd23f">BRINQUEDOS</text>`
    + `<rect x="80" y="420" width="920" height="760" rx="16" fill="#cdeaf5" stroke="${OL}" stroke-width="${SW}"/><path d="M140,470 L300,470 L160,640 Z" fill="#fff" opacity=".6"/>`
    + `<g id="e3game"><rect x="330" y="560" width="420" height="300" rx="20" fill="#3b5bb5" stroke="${OL}" stroke-width="${SW}"/><rect x="380" y="600" width="320" height="170" rx="12" fill="#1b1730" stroke="${OL}" stroke-width="6"/><circle cx="470" cy="685" r="34" fill="#e8453c"/><rect x="560" y="660" width="90" height="50" rx="10" fill="#3fbf6a"/>
      <text x="540" y="835" text-anchor="middle" font-family="Luckiest" font-size="44" fill="#fff">SUPER GAME</text></g>
      <g id="e3price"><rect x="640" y="880" width="260" height="130" rx="14" fill="#ffd23f" stroke="${OL}" stroke-width="7"/><text x="770" y="970" text-anchor="middle" font-family="Luckiest" font-size="78" fill="#e8453c">R$ 300</text></g>`
    + street() + `<g>${k.svg}</g>` + sp + cardSvg('e3c3');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [3, 1.12]]), fx: 540, fy: K(lt, [[0, 900], [3, 1000]]) }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.05, t: lt, mouth: lt < 1.4 ? 'O' : 'smile', talk: lt > 1.4, eyes: lt < 1.4 ? 'wide' : 'money', brow: .8, armL: K(lt, [[0, 20], [.5, 130]]), armR: K(lt, [[0, 20], [.5, 130]]), seed: 5, lookY: -12, hop: lt < .5 ? 2 : 0 });
      $('e3game').setAttribute('transform', `translate(540,710) rotate(${Math.sin(lt * 2) * 2}) scale(${1 + Math.sin(lt * 4) * .02}) translate(-540,-710)`);
      $('e3price').setAttribute('transform', `translate(770,945) scale(${backOut((lt - .3) / .3)}) rotate(-6) translate(-770,-945)`);
      for (let i = 0; i < 4; i++) $('e3sp3' + i).setAttribute('opacity', Math.abs(Math.sin(lt * 4 + i)));
      card('e3c3', 5.1, lt, 540, 1300, .9, 0, 1.5);
    }
  };
});

// 4. Caio sai andando decidido, de olho no dinheiro (cenário desliza)
shot(8.1, 9.9, () => {
  const k = mk('caio');
  const svg = sky() + `<g id="e3bg4">${backBuildings()}${house(-40, 420, 560, '#a8d8c7')}${house(400, 360, 500, '#f2c29b', { doorCol: '#4a6fa5', winX: 190 })}${house(780, 360, 540, '#c9b6e4')}${house(1180, 420, 560, '#a8d8c7')}${house(1620, 380, 520, '#f2c29b')}</g>` + street() + `<g>${k.svg}</g>`;
  return {
    svg, cam: lt => ({ s: 1.05, fx: 540, fy: 1000 }),
    update(lt) {
      $('e3bg4').setAttribute('transform', `translate(${-lt * 380},0)`);
      setChar(k.id, { x: 540, y: 1480, scale: 1.0, t: lt, mouth: 'smile', eyes: 'money', armL: 25, armR: 25, walk: 1.8, lean: 3, seed: 6 });
    }
  };
});

// 5. montagem de abraços falsos: carteiro, professora, cachorro
shot(9.9, 12.5, () => {
  const k1 = mk('caio'), c = mk('carteiro'), k2 = mk('caio'), p = mk('prof'), k3 = mk('caio');
  let notes = ''; for (let i = 0; i < 3; i++) notes += noteSvg('e3n5' + i);
  const sub = [
    `<g id="e3s5a">${praca()}<g>${c.svg}</g><rect x="640" y="1150" width="140" height="110" rx="14" fill="#c98a52" stroke="${OL}" stroke-width="6"/><rect x="650" y="1110" width="70" height="40" fill="#fff" stroke="${OL}" stroke-width="5" transform="rotate(-10,685,1130)"/><g>${k1.svg}</g></g>`,
    `<g id="e3s5b">${floorIn(1340, '#e9dcc0', '#d9c4a0')}<rect x="60" y="360" width="960" height="420" fill="#2f6b4f" stroke="${OL}" stroke-width="${SW}"/><text x="540" y="620" text-anchor="middle" font-family="Luckiest" font-size="130" fill="#f4f4ee" opacity=".9">A B C</text><g>${p.svg}</g><g>${k2.svg}</g></g>`,
    `<g id="e3s5c">${praca()}${dogSvg('e3dog')}<g>${k3.svg}</g></g>`,
  ];
  const svg = sub.join('') + notes + tagSvg('e3t5', '-R$10', '#e8453c', 120) + cardSvg('e3c5');
  return {
    svg, cam: lt => { const i = Math.min(2, Math.floor(lt / .8)); const l = lt - i * .8; return { s: 1.1 + l * .06, fx: 540, fy: 1050, blur: l < .07 && i > 0 ? 18 : 0, blurX: 1 }; },
    update(lt) {
      const i = Math.min(2, Math.floor(lt / .8)), l = lt - i * .8;
      ['e3s5a', 'e3s5b', 'e3s5c'].forEach((n, j) => $(n).setAttribute('display', j === i ? 'inline' : 'none'));
      const h = hug(l, .25);
      setChar(c.id, { x: 650, y: 1480, scale: .95, t: lt, mouth: 'flat', eyes: l > .3 ? 'wide' : 'open', brow: .8, armR: lerp(10, 40, h.p), seed: 7, lookX: -10 });
      setChar(k1.id, { x: K(l, [[0, 240], [.25, 440]]), y: 1480, scale: .9, t: lt, mouth: 'smile', eyes: 'money', armL: lerp(30, 100, h.p), lean: 6 * h.p, squash: h.sq, seed: 8, walk: l < .25 ? 2.5 : 0 });
      setChar(p.id, { x: 650, y: 1480, scale: .95, t: lt, mouth: 'O', eyes: l > .3 ? 'wide' : 'open', brow: .8, armR: lerp(10, 50, h.p), seed: 9, lookX: -10 });
      setChar(k2.id, { x: K(l, [[0, 240], [.25, 440]]), y: 1480, scale: .9, t: lt, mouth: 'smile', eyes: 'money', armL: lerp(30, 100, h.p), lean: 6 * h.p, squash: h.sq, seed: 10, walk: l < .25 ? 2.5 : 0 });
      setDog('e3dog', lt, 680, 1480, .95, l > .35 ? 'confuso' : 'happy');
      setChar(k3.id, { x: K(l, [[0, 220], [.3, 470]]), y: 1480, scale: .9, t: lt, mouth: 'smile', eyes: 'money', armL: lerp(30, 110, K(l, [[.1, 0], [.3, 1]])), lean: 10 * K(l, [[.1, 0], [.3, 1]]), seed: 11, walk: l < .3 ? 2.5 : 0 });
      flyNote('e3n5' + i, l, .35, 560, 1150, 880, 520, .6);
      popTag('e3t5', l, .4, 300, 760, .55);
      card('e3c5', 9.9, lt, 540, 260, .9);
    }
  };
});

// 6. sentado na calçada: sobrou R$ 20
shot(12.5, 14.7, () => {
  const k = mk('caio', { sit: 1 });
  const svg = sky('#c3c9de') + backBuildings('#a9a6c4', '#c6c3dc') + house(-60, 1200, 900, '#9fc9bb', { roof: false, doorX: 760, winX: 120, winY: 200 }) + street() + `<g>${k.svg}</g>` + cardSvg('e3c6');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.2], [2.2, 1.35]]), fx: 540, fy: 1100 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1560, scale: 1.1, t: lt, mouth: 'frown', eyes: 'half', brow: .5, tears: lt > .8, seed: 12, tilt: K(lt, [[0, 0], [1, -6]]), lookY: 10, armL: 30, armR: 30 });
      card('e3c6', 12.5, lt, 540, 560, 1.2, 12, .1);
    }
  };
});

// 7. entardecer: o avô sozinho no banco da praça
shot(14.7, 17.3, () => {
  const a = mk('avo'), k = mk('caio');
  let leaves = ''; for (let i = 0; i < 6; i++) leaves += `<ellipse class="e3lf" rx="16" ry="9" fill="#e8a23c" stroke="${OL}" stroke-width="4"/>`;
  const svg = praca(1) + bench(640, 1470) + `<g>${a.svg}</g><g>${k.svg}</g><g id="e3leaves">${leaves}</g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.6, 1.15]]), fx: K(lt, [[0, 540], [2.6, 620]]), fy: 1100 }),
    update(lt) {
      setChar(a.id, { x: 640, y: 1430, scale: .9, t: lt, mouth: 'frown', eyes: 'half', brow: .3, tilt: -5, seed: 13, lookY: 8 });
      setChar(k.id, { x: K(lt, [[0, 80], [1.2, 170]]), y: 1520, scale: .75, t: lt, mouth: 'o', eyes: 'open', brow: .5, seed: 14, lookX: 12, walk: lt < 1.2 ? 1.6 : 0 });
      document.querySelectorAll('.e3lf').forEach((l, i) => { const p = (lt * .35 + i * .17) % 1; l.setAttribute('transform', `translate(${100 + i * 170 + Math.sin(p * 9 + i) * 50},${600 + p * 900}) rotate(${p * 400})`); });
    }
  };
});

// 8. close: o avô com um bolinho e uma vela
shot(17.3, 19.7, () => {
  const a = mk('avo');
  const svg = praca(1) + bench(540, 1470) + `<g>${a.svg}</g>`
    + `<g transform="translate(0,175)"><g id="e3cake"><rect x="490" y="1110" width="100" height="70" rx="12" fill="#f2b8c6" stroke="${OL}" stroke-width="6"/><path d="M480,1110 Q540,1070 600,1110 Z" fill="#fff" stroke="${OL}" stroke-width="6"/><rect x="532" y="1030" width="16" height="50" fill="#5fb3e0" stroke="${OL}" stroke-width="4"/><path id="e3flame" d="M540,1030 q-14,-20 0,-44 q14,24 0,44 Z" fill="#ffb02e" stroke="${OL}" stroke-width="4"/></g></g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.7], [2.4, 1.9]]), fx: 540, fy: 1060 }),
    update(lt) {
      setChar(a.id, { x: 540, y: 1430, scale: 1.0, t: lt, mouth: 'frown', eyes: 'half', brow: .4, tilt: -3, seed: 15, lookY: 10, armL: 40, armR: 40 });
      $('e3flame').setAttribute('transform', `translate(540,1030) scale(${1 + Math.sin(lt * 18) * .08},${1 + Math.sin(lt * 13) * .1}) translate(-540,-1030)`);
    }
  };
});

// 9. o abraço de verdade (luz quente, corações)
shot(19.7, 22.1, () => {
  const a = mk('avo'), k = mk('caio'); const [hp, hs] = hearts(9);
  const svg = praca(1) + `<circle id="e3glow" cx="540" cy="1050" r="420" fill="#fff1c4" opacity="0"/>` + bench(560, 1470) + `<g>${a.svg}</g><g>${k.svg}</g>` + hs;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2.4, 1.35]]), fx: 560, fy: 1080 }),
    update(lt) {
      const h = hug(lt, .7);
      setChar(a.id, { x: 600, y: 1430, scale: .95, t: lt, mouth: h.p > .5 ? 'smile' : 'o', eyes: h.p > .5 ? 'happy' : 'wide', brow: .6, tears: h.p > .6, armR: lerp(30, 95, h.p), lean: -5 * h.p, seed: 16 });
      setChar(k.id, { x: K(lt, [[0, 180], [.7, 430]]), y: 1500, scale: .88, t: lt, mouth: h.p > .5 ? 'smug' : 'o', eyes: h.p > .5 ? 'happy' : 'open', armL: lerp(20, 105, h.p), lean: 9 * h.p, squash: h.sq, seed: 17, walk: lt < .7 ? 2.2 : 0 });
      $('e3glow').setAttribute('opacity', .55 * h.p);
      floatHearts(hp, 9, lt, .9, 530, 900, 260, 1.4);
    }
  };
});

// 10. +R$ 1.000: o saldo explode
shot(22.1, 24.5, () => {
  const a = mk('avo'), k = mk('caio');
  let notes = ''; for (let i = 0; i < 12; i++) notes += noteSvg('e3n10' + i, '100', '#9bc6ef', '#2f5f9a');
  const svg = sky('#fff3c4') + `<g id="e3rays">${Array.from({ length: 12 }, (_, i) => `<path d="M540,900 L${540 + Math.cos(i * .5236) * 1600},${900 + Math.sin(i * .5236) * 1600} L${540 + Math.cos(i * .5236 + .2) * 1600},${900 + Math.sin(i * .5236 + .2) * 1600} Z" fill="#ffe27a"/>`).join('')}</g>`
    + praca(1).replace(/<rect x="-200" y="-200"[^>]*>/, '').replace('<circle cx="820" cy="760" r="160" fill="#ffd9a0" opacity=".8"/>', '') + bench(560, 1470) + `<g>${a.svg}</g><g>${k.svg}</g>` + notes + bigNum('e3plus', '+R$ 1.000', 160, '#3fbf6a') + cardSvg('e3c10');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.4, 1.12]]), fx: 540, fy: 1050 }),
    update(lt) {
      $('e3rays').setAttribute('transform', `rotate(${lt * 15},540,900)`);
      setChar(a.id, { x: 650, y: 1430, scale: .9, t: lt, mouth: 'O', eyes: 'wide', brow: 1, armL: 60, armR: 60, seed: 18, hop: 2 });
      setChar(k.id, { x: 380, y: 1500, scale: .9, t: lt, mouth: lt > .8 ? 'smile' : 'O', eyes: lt > .8 ? 'money' : 'wide', brow: 1, armL: K(lt, [[0, 40], [.6, 160]]), armR: K(lt, [[0, 40], [.6, 160]]), capUp: K(lt, [[0, 0], [.25, 80], [.6, 0]]), hop: lt > .8 ? 3 : 0, seed: 19 });
      for (let i = 0; i < 12; i++) {
        const el = $('e3n10' + i); const p = lt - .3 - i * .1; if (p < 0) { el.setAttribute('display', 'none'); continue; }
        el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${60 + (i * 97) % 960 + Math.sin(p * 5 + i) * 40},${-100 + p * 650}) rotate(${Math.sin(p * 6 + i) * 30})`);
      }
      showPop('e3plus', lt, .3, 540, 520, 1);
      card('e3c10', 22.1, lt, 540, 300, .95, 0, .5);
    }
  };
});

// 11. "Vô… mais um?" (olhos de cifrão)
shot(24.5, 26.5, () => {
  const k = mk('caio');
  const svg = praca(1) + `<g>${k.svg}</g>` + bubbleSvg('e3b11', 'Vô… mais um?', 460, 56);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.7], [2, 1.95]]), fx: 540, fy: 960 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.1, t: lt, mouth: 'smile', talk: lt > .1 && lt < 1.0, eyes: 'money', brow: .7, armL: K(lt, [[0, 20], [.5, 95]]), armR: K(lt, [[0, 20], [.5, 95]]), tilt: 6, seed: 20 });
      showBubble('e3b11', lt, .1, 2.0, 540, 600);
    }
  };
});

// 12. "Esse aí já é por interesse." -R$10 (fim)
shot(26.5, 30.0, () => {
  const a = mk('avo'), k = mk('caio');
  const svg = praca(1) + bench(560, 1470) + `<g>${a.svg}</g><g>${k.svg}</g>` + bubbleSvg('e3b12', 'Esse aí já é por interesse.', 640, 46) + noteSvg('e3n12', '10') + tagSvg('e3t12', '-R$10', '#e8453c', 130) + cardSvg('e3c12');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.1], [3.5, 1.2]]), fx: 560, fy: 1050 }),
    update(lt) {
      const h = hug(lt, .4, .9);
      setChar(a.id, { x: 660, y: 1430, scale: .95, t: lt, mouth: lt < 1.0 ? 'smug' : 'smile', talk: lt > .2 && lt < 1.1, eyes: lt > 1.1 ? 'happy' : 'half', brow: -.3, armR: lerp(20, 60, h.p), seed: 21, hop: lt > 1.6 ? 2 : 0 });
      setChar(k.id, { x: K(lt, [[0, 300], [.4, 440], [1.1, 360]]), y: 1500, scale: .9, t: lt, mouth: lt > 1.1 ? 'flat' : 'smile', eyes: lt > 1.1 ? 'half' : 'money', armL: lerp(30, 100, h.p), lean: 8 * h.p, seed: 22 });
      showBubble('e3b12', lt, .15, 3.5, 620, 700);
      flyNote('e3n12', lt, 1.05, 380, 1150, 140, 560, .8); popTag('e3t12', lt, 1.1, 260, 900, 1.2);
      card('e3c12', 26.5, lt, 540, 280, 1.0, 10, .9);
    }
  };
});
