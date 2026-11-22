// Episódio 1: "Na minha cidade, cada reclamação custa um real."
LINES = [
  [0.3, 2.7, 'Na minha cidade, cada reclamação custa um real.'],
  [2.9, 4.5, 'Seu Jair reclamou do calor.'],
  [4.7, 6.5, 'Dona Cida reclamou do tomate.'],
  [6.6, 8.7, 'Depois, reclamou do preço de reclamar.'],
  [8.9, 11.6, 'Eu sou o Caio, tenho nove anos e cinquenta reais.'],
  [11.85, 12.55, 'Choveu.'],
  [12.65, 13.35, 'Brócolis.'],
  [13.45, 14.15, 'Dever de casa.'],
  [14.25, 14.95, 'A internet caiu.'],
  [15.0, 16.9, 'Em uma semana: três reais.'],
  [17.1, 18.5, 'Aí eu reparei no meu avô.'],
  [18.7, 20.9, 'Ele nunca reclama. E tem um milhão.'],
  [21.0, 22.9, 'O segredo? Uma plaquinha.'],
  [23.0, 25.5, 'Todo mundo paga pra reclamar pra ele.'],
  [25.6, 27.3, 'No outro dia, eu abri a minha.'],
  [27.4, 29.8, 'Ninguém veio. “Que injustiça!” Menos um real.'],
];

// 1. abertura: zoom-out da moeda para a rua
shot(0, 2.8, () => {
  const j = mk('jair'), c = mk('cida'), n = mk('n1');
  const svg = sky() + backBuildings() + house(-40, 420, 560, '#a8d8c7') + house(400, 360, 500, '#f2c29b', { doorCol: '#4a6fa5', winX: 190 }) + house(780, 360, 540, '#c9b6e4') + street()
    + `<g>${j.svg}</g><g>${c.svg}</g><g>${n.svg}</g>`
    + coinSvg('s1c1') + coinSvg('s1c2') + tagSvg('s1t1', '-R$1') + tagSvg('s1t2', '-R$1');
  return {
    svg, cam: lt => ({ s: lerp(4.2, 1, easeOut(lt / .8)), fx: 290, fy: 1290, blur: lt < .8 ? 26 * (1 - lt / .8) : 0 }),
    update(lt) {
      setChar(j.id, { x: 250, y: 1470, scale: .62, t: lt, mouth: lt < 1.4 ? 'shout' : 'frown', talk: lt < 1.4, brow: -1, mad: 1, sweat: 1, armL: 40 + Math.sin(lt * 14) * 25, seed: 1 });
      setChar(c.id, { x: 600, y: 1470, scale: .62, t: lt, mouth: lt > 1.6 && lt < 2.4 ? 'shout' : 'flat', talk: lt > 1.6 && lt < 2.4, brow: lt > 1.6 ? -1 : 0, armR: lt > 1.6 ? 120 : 10, seed: 2 });
      setChar(n.id, { x: 880, y: 1470, scale: .62, t: lt, mouth: 'smug', seed: 3, lookX: -6 });
      flyCoin('s1c1', lt, .2, 285, 1330, 420, 760, .9, 200); popTag('s1t1', lt, .35, 250, 1020);
      flyCoin('s1c2', lt, 1.8, 630, 1330, 760, 760, .9, 200); popTag('s1t2', lt, 1.9, 600, 1020);
    }
  };
});

// 2. Seu Jair e o calor
shot(2.8, 4.6, () => {
  const j = mk('jair');
  let rays = ''; for (let i = 0; i < 10; i++) rays += `<rect x="-10" y="-210" width="20" height="60" rx="10" fill="#ffd23f" stroke="${OL}" stroke-width="5" transform="rotate(${i * 36})"/>`;
  const svg = sky('#f6e2b8') + backBuildings('#e9c7a6', '#f5dcc4') + house(100, 880, 640, '#f2c29b', { roof: false, doorX: 40, winX: 600 }) + street()
    + `<g id="s2sun" transform="translate(860,330)">${rays}<circle r="120" fill="#ffd23f" stroke="${OL}" stroke-width="8"/></g>`
    + `<g>${j.svg}</g>` + coinSvg('s2c') + tagSvg('s2t', '-R$1', '#e8453c', 120);
  return {
    svg, cam: lt => ({ s: 1 + lt * .02, fx: 540, fy: 1100 }),
    update(lt) {
      $('s2sun').setAttribute('transform', `translate(860,330) rotate(${lt * 30}) scale(${1 + Math.sin(lt * 6) * .04})`);
      setChar(j.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: 'shout', talk: lt < 1.2, brow: -1, mad: 1, sweat: 1, armL: 130 + Math.sin(lt * 16) * 22, armR: 20, seed: 4, lookY: -6, lookX: 6 });
      flyCoin('s2c', lt, .8, 640, 1220, 900, 760, .7, 180); popTag('s2t', lt, .9, 820, 900);
    }
  };
});

// 3. Dona Cida e o tomate
shot(4.6, 6.6, () => {
  const c = mk('cida');
  let tom = ''; for (let i = 0; i < 14; i++) tom += `<circle cx="${130 + (i % 7) * 58}" cy="${1020 - Math.floor(i / 7) * 40}" r="32" fill="#e8453c" stroke="${OL}" stroke-width="6"/><path d="M${120 + (i % 7) * 58},${994 - Math.floor(i / 7) * 40} l10,8 l10,-8" stroke="#3f8f3f" stroke-width="6" fill="none"/>`;
  const svg = sky() + backBuildings() + house(-40, 1160, 600, '#c9e4b5', { roof: false, door: false, win: false })
    + `<rect x="60" y="1040" width="520" height="300" fill="#3f9a5f" stroke="${OL}" stroke-width="${SW}"/>`
    + Array.from({ length: 6 }, (_, i) => `<path d="M${40 + i * 93},620 l93,0 l0,70 q-46,40 -93,0 Z" fill="${i % 2 ? '#fff' : '#e8453c'}" stroke="${OL}" stroke-width="6"/>`).join('')
    + `<rect x="70" y="600" width="20" height="440" fill="#8a5a3a" stroke="${OL}" stroke-width="6"/><rect x="550" y="600" width="20" height="440" fill="#8a5a3a" stroke="${OL}" stroke-width="6"/>` + tom
    + `<g id="s3sign"><rect x="130" y="730" width="400" height="190" rx="16" fill="#fffbe9" stroke="${OL}" stroke-width="${SW}"/><text x="330" y="800" text-anchor="middle" font-family="Luckiest" font-size="58" fill="#2b2745">TOMATE</text><text x="330" y="885" text-anchor="middle" font-family="Luckiest" font-size="78" fill="#e8453c">R$ 12/KG</text></g>`
    + street() + `<g>${c.svg}</g>` + coinSvg('s3c') + tagSvg('s3t', '-R$1', '#e8453c', 110);
  return {
    svg, cam: lt => ({ s: 1 + lt * .02, fx: 540, fy: 1000 }),
    update(lt) {
      $('s3sign').setAttribute('transform', `rotate(${Math.sin(lt * 10) * (lt < .6 ? 2 : 0)},330,820)`);
      setChar(c.id, { x: 790, y: 1480, scale: 1.15, t: lt, mouth: 'shout', talk: 1, brow: -1, mad: 1, armR: 112 + Math.sin(lt * 12) * 10, armL: 30, seed: 5, lookX: -10 });
      flyCoin('s3c', lt, 1.0, 860, 1200, 1000, 700, .7, 160); popTag('s3t', lt, 1.1, 900, 820);
    }
  };
});

// 4. close na Dona Cida: reclama do preço de reclamar (duas moedas)
shot(6.6, 8.8, () => {
  const c = mk('cida');
  const svg = sky() + house(-40, 1160, 900, '#c9e4b5', { roof: false, door: false, winX: 760, winY: 120 }) + street()
    + `<g>${c.svg}</g>` + coinSvg('s4c1') + coinSvg('s4c2') + tagSvg('s4t1', '-R$1', '#e8453c', 130) + tagSvg('s4t2', '-R$1', '#e8453c', 130);
  return {
    svg, cam: lt => ({ s: 1.9 + lt * .05, fx: 540, fy: 860 }),
    update(lt) {
      setChar(c.id, { x: 540, y: 1480, scale: 1.15, t: lt, mouth: 'shout', talk: 1, brow: -1, mad: 1, eyes: lt > 1.2 ? 'wide' : 'open', armR: 60 + Math.sin(lt * 9) * 30, armL: 60 + Math.cos(lt * 9) * 30, seed: 6, hop: lt > 1.2 ? 3 : 0 });
      flyCoin('s4c1', lt, .7, 600, 1180, 380, 640, .6, 120); popTag('s4t1', lt, .75, 440, 720, 1.4);
      flyCoin('s4c2', lt, 1.3, 600, 1180, 760, 640, .6, 120); popTag('s4t2', lt, 1.35, 720, 720, .85);
    }
  };
});

// 5. Caio se apresenta + saldo R$ 50
shot(8.8, 11.8, () => {
  const k = mk('caio');
  let sp = ''; [[300, 620, .9], [800, 560, 1.1], [860, 880, .7], [220, 900, .6]].forEach((p, i) => sp += `<g class="sp" id="s5sp${i}">${sparkle(...p)}</g>`);
  const svg = sky() + house(-60, 1200, 1000, '#a8d8c7', { roof: false, doorX: 160, winX: 820, winY: 260 }) + street()
    + `<g>${k.svg}</g>` + sp + cardSvg('s5card');
  return {
    svg, cam: lt => ({ s: 1.15 + lt * .02, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: 'smile', talk: lt < 2.7, armL: lt > .3 && lt < 1.7 ? 150 + Math.sin(lt * 14) * 15 : 12, eyes: lt > 1.7 && lt < 2.1 ? 'happy' : 'open', seed: 7, hop: lt < .4 ? 2.5 : 0 });
      for (let i = 0; i < 4; i++) $('s5sp' + i).setAttribute('opacity', .4 + .6 * Math.abs(Math.sin(lt * 4 + i)));
      showCard('s5card', lt, 1.9, 540, 380, 50, '#2fae60', 1.2);
    }
  };
});

// 6. montagem: chuva, brócolis, dever, internet (saldo despencando)
const SALDO6 = lt => lt < .3 ? 50 : lt < 1.1 ? 49 : lt < 1.9 ? 48 : lt < 2.7 ? 47 : Math.max(3, Math.round(47 - (lt - 2.7) / .3 * 44));
shot(11.8, 15.0, () => {
  const k1 = mk('caio'), k2 = mk('caio'), k3 = mk('caio'), k4 = mk('caio');
  let rain = ''; for (let i = 0; i < 26; i++) rain += `<rect class="dr" x="${(i * 97) % 1000 + 40}" y="0" width="10" height="56" rx="5" fill="#7cc6ff" stroke="${OL}" stroke-width="3"/>`;
  let broc = ''; for (let i = 0; i < 5; i++) broc += `<rect x="${430 + i * 45}" y="1090" width="22" height="50" fill="#9ccc4e" stroke="${OL}" stroke-width="5"/><circle cx="${441 + i * 45}" cy="1078" r="36" fill="#3f9a3f" stroke="${OL}" stroke-width="6"/>`;
  let papers = ''; for (let i = 0; i < 14; i++) papers += `<rect x="${110 + (i % 3) * 6}" y="${1150 - i * 40}" width="300" height="36" rx="4" fill="#fff" stroke="${OL}" stroke-width="5" transform="rotate(${(i % 4 - 1.5) * 2},260,${1168 - i * 40})"/>`;
  const sub = [
    `<g id="s6a">${sky('#9fb0c4') + backBuildings('#8f8fb3', '#a9a9c9') + street()}<g>${k1.svg}</g><g transform="translate(540,520)"><circle cx="-120" r="110" fill="#d9dde8" stroke="${OL}" stroke-width="8"/><circle cx="40" cy="-40" r="140" fill="#d9dde8" stroke="${OL}" stroke-width="8"/><circle cx="170" cy="10" r="100" fill="#d9dde8" stroke="${OL}" stroke-width="8"/><rect x="-200" y="0" width="420" height="100" fill="#d9dde8"/></g><g id="s6rain">${rain}</g></g>`,
    `<g id="s6b">${floorIn(1340, '#f2d48a', '#e4d6bd')}<g>${k2.svg}</g><rect x="140" y="1140" width="800" height="60" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/><rect x="200" y="1200" width="40" height="320" fill="#a86c3a" stroke="${OL}" stroke-width="6"/><rect x="840" y="1200" width="40" height="320" fill="#a86c3a" stroke="${OL}" stroke-width="6"/><ellipse cx="540" cy="1140" rx="240" ry="40" fill="#fff" stroke="${OL}" stroke-width="7"/>${broc}</g>`,
    `<g id="s6c">${floorIn(1340, '#c9b6e4', '#e4d6bd')}<g>${k3.svg}</g><rect x="140" y="1180" width="800" height="50" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/>${papers}<text x="265" y="560" text-anchor="middle" font-family="Luckiest" font-size="80" fill="#e8453c" stroke="${OL}" stroke-width="10" paint-order="stroke">DEVER</text></g>`,
    `<g id="s6d">${floorIn(1340, '#a8d8c7', '#e4d6bd')}<g>${k4.svg}</g><g transform="translate(540,470)"><path d="M-170,0 A240,240 0 0 1 170,0" fill="none" stroke="#2b2745" stroke-width="34" stroke-linecap="round"/><path d="M-110,60 A155,155 0 0 1 110,60" fill="none" stroke="#2b2745" stroke-width="34" stroke-linecap="round"/><circle cy="130" r="30" fill="#2b2745"/><path d="M-170,-120 L170,240 M170,-120 L-170,240" stroke="#e8453c" stroke-width="40" stroke-linecap="round"/></g></g>`,
  ];
  let coins = ''; for (let i = 0; i < 8; i++) coins += coinSvg('s6k' + i);
  const svg = sub.join('') + coins + tagSvg('s6t0', '-R$1') + tagSvg('s6t1', '-R$1') + tagSvg('s6t2', '-R$1') + tagSvg('s6t3', '-R$44', '#e8453c', 120) + cardSvg('s6card', 470);
  return {
    svg, cam: lt => { const i = Math.min(3, Math.floor(lt / .8)); const l = lt - i * .8; return { s: 1.1 + l * .06, fx: 540, fy: 1000, blur: l < .08 && i > 0 ? 16 : 0 }; },
    update(lt) {
      const i = Math.min(3, Math.floor(lt / .8)), l = lt - i * .8;
      ['s6a', 's6b', 's6c', 's6d'].forEach((n, j) => $(n).setAttribute('display', j === i ? 'inline' : 'none'));
      document.querySelectorAll('#s6rain .dr').forEach((d, j) => d.setAttribute('transform', `translate(0,${600 + ((lt * 1300 + j * 137) % 900)})`));
      setChar(k1.id, { x: 540, y: 1480, scale: 1.2, t: lt, mouth: 'frown', eyes: 'half', brow: -.5, tears: 0, seed: 8, lookY: -8 });
      setChar(k2.id, { x: 540, y: 1300, scale: 1.0, t: lt, mouth: 'yuck', brow: -1, eyes: 'half', seed: 9 });
      setChar(k3.id, { x: 700, y: 1330, scale: 1.0, t: lt, mouth: 'shout', talk: 1, brow: -1, mad: 1, armL: 120, armR: 120, seed: 10, lookY: -6 });
      setChar(k4.id, { x: 540, y: 1480, scale: 1.2, t: lt, mouth: 'shout', talk: 1, brow: -1, mad: 1, eyes: 'wide', armL: 165 + Math.sin(lt * 20) * 8, armR: 165 + Math.cos(lt * 20) * 8, seed: 11, hop: 4 });
      for (let n = 0; n < 3; n++) { flyCoin('s6k' + n, lt, n * .8 + .25, 600, 1250, 900, 380, .55, 140); popTag('s6t' + n, lt, n * .8 + .3, 820, 700, .5); }
      for (let n = 3; n < 8; n++) flyCoin('s6k' + n, lt, 2.5 + (n - 3) * .1, 560 + (n - 5) * 40, 1250, 800 + (n % 3) * 80, 340, .5, 220);
      popTag('s6t3', lt, 2.55, 540, 700, .65);
      const v = SALDO6(lt);
      showCard('s6card', lt, 0, 540, 260, v, v > 20 ? '#2fae60' : '#e8453c', .9, 0);
    }
  };
});

// 7. Caio triste: R$ 3,00
shot(15.0, 17.0, () => {
  const k = mk('caio');
  const svg = sky('#c3c9de') + house(-60, 1200, 1000, '#9fc9bb', { roof: false, doorX: 160, winX: 820, winY: 260 }) + street() + `<g>${k.svg}</g>` + cardSvg('s7card', 470);
  return {
    svg, cam: lt => ({ s: 1.35 + lt * .04, fx: 540, fy: 1000 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: 'frown', eyes: 'open', brow: .4, tears: 1, seed: 12, tilt: -4, lookY: 6 });
      showCard('s7card', lt, .15, 540, 470, 3, '#e8453c', 1.25, 14);
    }
  };
});

// 8. chicote para a casa do avô; Caio espiando
shot(17.0, 18.6, () => {
  const k = mk('caio'), a = mk('avo');
  const chair = (x, y) => `<g id="s8chair"><rect x="${x - 150}" y="${y - 520}" width="300" height="300" rx="40" fill="#a86c3a" stroke="${OL}" stroke-width="${SW}"/><path d="M${x - 210},${y + 10} Q${x},${y + 70} ${x + 210},${y + 10}" fill="none" stroke="#7a4a26" stroke-width="22" stroke-linecap="round"/><rect x="${x - 170}" y="${y - 150}" width="340" height="40" rx="18" fill="#a86c3a" stroke="${OL}" stroke-width="6"/></g>`;
  const svg = sky() + backBuildings() + house(220, 860, 700, '#f2c29b', { doorX: 120, doorCol: '#4a6fa5', winX: 520, winY: 140 }) + house(-200, 420, 560, '#c9b6e4', { door: false }) + street()
    + chair(760, 1460) + `<g>${a.svg}</g><g>${k.svg}</g>`;
  return {
    svg, cam: lt => ({ s: 1, fx: 540, fy: 1000, tx: lt < .3 ? (1 - easeOut(lt / .3)) * 700 : 0, blur: lt < .3 ? 40 * (1 - lt / .3) : 0, blurX: 1 }),
    update(lt) {
      setChar(a.id, { x: 760, y: 1380, scale: .8, t: lt, mouth: 'smug', eyes: 'happy', seed: 13, tilt: Math.sin(lt * 2) * 3 });
      setChar(k.id, { x: 210, y: 1520, scale: .9, t: lt, mouth: 'o', eyes: 'wide', seed: 14, lookX: 12, tilt: 8 });
    }
  };
});

// 9. o avô na cadeira de balanço: R$ 1.000.000 / 9b Caio de queixo caído
shot(18.6, 21.0, () => {
  const a = mk('avo'), k = mk('caio');
  let sp = ''; for (let i = 0; i < 6; i++) sp += `<g id="s9sp${i}">${sparkle(150 + i * 160, 560 + (i % 2) * 120, .9)}</g>`;
  let coins = ''; for (let i = 0; i < 6; i++) coins += coinSvg('s9k' + i);
  const svg = `<g id="s9a">${sky() + house(-60, 1200, 1000, '#f2c29b', { roof: false, doorX: 80, doorCol: '#4a6fa5', winX: 780, winY: 250 }) + street()}
    <g id="s9rock"><rect x="380" y="900" width="320" height="320" rx="40" fill="#a86c3a" stroke="${OL}" stroke-width="${SW}"/><path d="M300,1490 Q540,1560 780,1490" fill="none" stroke="#7a4a26" stroke-width="26" stroke-linecap="round"/><g>${a.svg}</g><rect x="350" y="1270" width="380" height="44" rx="20" fill="#a86c3a" stroke="${OL}" stroke-width="6"/></g>${coins}${sp}</g>`
    + `<g id="s9b" display="none">${sky() + house(-60, 1200, 1000, '#a8d8c7', { roof: false, door: false, winX: 80, winY: 300 }) + street()}<g>${k.svg}</g></g>`
    + bigNum('s9num', 'R$ 1.000.000', 132);
  return {
    svg, cam: lt => lt < 1.4 ? { s: 1.05 + lt * .03, fx: 540, fy: 1100 } : { s: 2.1 + (lt - 1.4) * .08, fx: 540, fy: 860 },
    update(lt) {
      const b = lt >= 1.4;
      $('s9a').setAttribute('display', b ? 'none' : 'inline'); $('s9b').setAttribute('display', b ? 'inline' : 'none');
      $('s9rock').setAttribute('transform', `rotate(${Math.sin(lt * 3) * 4},540,1520)`);
      setChar(a.id, { x: 540, y: 1430, scale: 1.0, t: lt, mouth: 'smug', eyes: 'happy', seed: 15, armL: 30, armR: 30 });
      for (let i = 0; i < 6; i++) { flyCoin('s9k' + i, lt, .3 + i * .1, 540, 300, 140 + i * 160, 1000, .8, -120); $('s9sp' + i).setAttribute('opacity', lt > .4 ? Math.abs(Math.sin(lt * 5 + i)) : 0); }
      if (!b) showPop('s9num', lt, .35, 540, 420, 1); else showPop('s9num', lt, 99, 0, 0);
      setChar(k.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: 'O', eyes: 'wide', brow: 1, seed: 16, capUp: b ? easeOut((lt - 1.45) / .25) * 90 : 0, squash: b && lt < 1.55 ? -.04 : 0 });
    }
  };
});

// 10. a plaquinha
shot(21.0, 23.0, () => {
  const a = mk('avo', { sit: 0 });
  const svg = sky() + house(-60, 1200, 1000, '#f2c29b', { roof: false, door: false, winX: 860, winY: 200 }) + street()
    + `<g>${a.svg}</g><g id="s10sign"><rect x="330" y="850" width="24" height="560" fill="#8a5a3a" stroke="${OL}" stroke-width="6"/><rect x="40" y="520" width="600" height="380" rx="18" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/><rect x="66" y="546" width="548" height="328" rx="10" fill="#fff6dc" stroke="${OL}" stroke-width="5"/>
      <text x="340" y="640" text-anchor="middle" font-family="Luckiest" font-size="62" fill="#2b2745">OUÇO</text><text x="340" y="712" text-anchor="middle" font-family="Luckiest" font-size="62" fill="#2b2745">RECLAMAÇÃO</text>
      <text x="340" y="840" text-anchor="middle" font-family="Luckiest" font-size="120" fill="#2fae60" stroke="${OL}" stroke-width="10" paint-order="stroke">R$ 2</text></g>`;
  return {
    svg, cam: lt => ({ s: 1.12 + lt * .04, fx: 540, fy: 950 }),
    update(lt) {
      const p = backOut(lt / .35);
      $('s10sign').setAttribute('transform', `translate(340,900) scale(${p}) rotate(${Math.sin(lt * 3) * 1.5}) translate(-340,-900)`);
      setChar(a.id, { x: 820, y: 1480, scale: 1.05, t: lt, mouth: 'smile', talk: lt > .5 && lt < 1.5, eyes: lt > 1.5 ? 'happy' : 'open', armR: lt > .6 ? 150 : 15, seed: 17, lookX: -12 });
    }
  };
});

// 11. fila de gente pagando pra reclamar
shot(23.0, 25.6, () => {
  const q = [mk('jair'), mk('cida'), mk('n1'), mk('n2')], a = mk('avo');
  let coins = ''; for (let i = 0; i < 6; i++) coins += coinSvg('s11k' + i);
  const svg = sky() + backBuildings() + house(560, 640, 640, '#f2c29b', { doorX: 380, doorCol: '#4a6fa5', winX: 60, winY: 120 }) + house(-120, 680, 560, '#a8d8c7', { winX: 380 }) + street()
    + `<rect x="770" y="1150" width="270" height="70" rx="12" fill="#c98a52" stroke="${OL}" stroke-width="6"/><text x="905" y="1200" text-anchor="middle" font-family="Luckiest" font-size="42" fill="#fff6dc">R$ 2</text>`
    + `<g>${a.svg}</g><rect x="610" y="1330" width="90" height="110" rx="14" fill="rgba(200,235,255,.75)" stroke="${OL}" stroke-width="7"/>`
    + q.map(c => `<g>${c.svg}</g>`).join('') + coins + bigNum('s11num', 'R$ 1.000.000', 110) + tagSvg('s11t', '+R$2', '#2fae60', 90);
  return {
    svg, cam: lt => ({ s: 1.02 + lt * .02, fx: 540, fy: 1100 }),
    update(lt) {
      setChar(a.id, { x: 900, y: 1440, scale: .72, t: lt, mouth: 'smug', eyes: 'happy', seed: 18 });
      const xs = [520, 380, 240, 100];
      q.forEach((c, i) => {
        const spk = Math.floor(lt / .55) % 4 === i;
        setChar(c.id, { x: xs[i] + Math.sin(lt * 2 + i) * 6, y: 1490, scale: .68, t: lt + i, mouth: spk ? 'shout' : 'flat', talk: spk, brow: spk ? -1 : 0, mad: spk, armR: spk ? 110 : 10, seed: 20 + i, lookX: 10 });
      });
      for (let i = 0; i < 6; i++) { const who = i % 4; flyCoin('s11k' + i, lt, .2 + i * .4, xs[who] + 20, 1260, 655, 1360, .45, 160); }
      const v = 1000000 + 2 * Math.max(0, Math.floor((lt - .2) / .4) + 1);
      showPop('s11num', lt, 0, 540, 470, 1, 'R$ ' + v.toLocaleString('pt-BR'));
      popTag('s11t', lt, .65 + Math.floor(Math.max(0, lt - .65) / .4) * .4, 760, 1080, .38);
    }
  };
});

// 12. a barraquinha do Caio
shot(25.6, 27.4, () => {
  const k = mk('caio');
  let sp = ''; [[250, 560, .9], [860, 620, 1.1]].forEach((p, i) => sp += `<g id="s12sp${i}">${sparkle(...p)}</g>`);
  const svg = sky() + backBuildings() + house(-60, 1200, 700, '#c9b6e4', { roof: false, door: false, winX: 80, winY: 120 }) + street() + `<g>${k.svg}</g>`
    + `<g id="s12box"><rect x="240" y="1150" width="600" height="330" fill="#d6a86a" stroke="${OL}" stroke-width="${SW}"/><path d="M240,1150 L540,1230 L840,1150" fill="none" stroke="#a87a3e" stroke-width="6"/>
      <g transform="rotate(-4,540,1290)"><rect x="300" y="1200" width="480" height="190" fill="#fff" stroke="${OL}" stroke-width="6"/><text x="540" y="1268" text-anchor="middle" font-family="Luckiest" font-size="46" fill="#2b2745">OUÇO RECLAMAÇÃO</text><text x="540" y="1360" text-anchor="middle" font-family="Luckiest" font-size="84" fill="#2fae60">R$ 1</text></g></g>`
    + sp + `<g id="s12tag"><rect x="300" y="170" width="480" height="90" rx="45" fill="#2b2745"/><text x="540" y="232" text-anchor="middle" font-family="Luckiest" font-size="54" fill="#ffd23f">DIA SEGUINTE</text></g>`;
  return {
    svg, cam: lt => ({ s: 1.08 + lt * .03, fx: 540, fy: 1000 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1300, scale: 1.0, t: lt, mouth: 'smile', talk: lt > .3 && lt < 1.5, armL: 60, armR: 60, eyes: lt > 1.4 ? 'happy' : 'open', seed: 30 });
      for (let i = 0; i < 2; i++) $('s12sp' + i).setAttribute('opacity', Math.abs(Math.sin(lt * 4 + i)));
      $('s12tag').setAttribute('transform', `translate(540,215) scale(${backOut(lt / .3)}) translate(-540,-215)`);
    }
  };
});

// 13. ninguém veio: "Que injustiça!" -R$1 → R$ 2,00
shot(27.4, 30.0, () => {
  const k = mk('caio');
  const svg = sky('#e9e0c8') + backBuildings('#d8ccb0', '#e9e0c8') + house(-60, 1200, 640, '#e9d6a8', { roof: false, door: false, winX: 860, winY: 140 }) + street()
    + `<g>${k.svg}</g><rect x="660" y="1300" width="300" height="180" fill="#d6a86a" stroke="${OL}" stroke-width="6"/><text x="810" y="1400" text-anchor="middle" font-family="Luckiest" font-size="44" fill="#2fae60">R$ 1</text>`
    + `<g id="s13tw"><circle r="70" fill="none" stroke="#a8844e" stroke-width="10"/><path d="M-60,-30 Q0,40 60,-20 M-40,40 Q0,-50 50,30 M-70,10 Q0,-10 70,10" fill="none" stroke="#a8844e" stroke-width="8"/></g>`
    + coinSvg('s13c') + tagSvg('s13t', '-R$1', '#e8453c', 130) + cardSvg('s13card', 470);
  return {
    svg, cam: lt => lt < 1.2 ? { s: 1, fx: 540, fy: 1000 } : { s: 1.3 + (lt - 1.2) * .04, fx: 700, fy: 1150 },
    update(lt) {
      const x = -120 + lt * 520;
      $('s13tw').setAttribute('transform', `translate(${x},${1460 - Math.abs(Math.sin(lt * 5)) * 60}) rotate(${lt * 300})`);
      const angry = lt > 1.2;
      setChar(k.id, { x: 810, y: 1400, scale: .75, t: lt, mouth: angry ? 'shout' : 'flat', talk: angry && lt < 2.0, eyes: angry ? 'wide' : 'half', brow: angry ? -1 : 0, mad: angry, armL: angry ? 165 : 10, armR: angry ? 165 : 10, seed: 31, hop: angry && lt < 1.9 ? 4 : 0 });
      flyCoin('s13c', lt, 1.35, 830, 1180, 930, 900, .7, 150); popTag('s13t', lt, 1.45, 640, 1000, .9);
      showCard('s13card', lt, 1.85, 640, 760, 2, '#e8453c', .9, 10);
    }
  };
});

