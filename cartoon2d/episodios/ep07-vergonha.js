// Episódio 7: "Na minha cidade, cada vez que você fica com vergonha, ganha cinco reais."
// Caio "nunca fica com vergonha": dança na praça, canta no ônibus, veste fantasia de galinha… nada.
// Aí a Ana dá oi: rosto pega fogo, R$ 1.000. Ele responde "mãe"… e vira o Tomate.
LINES = [
  [0.3, 3.0, 'Na minha cidade, cada vez que você fica com vergonha, ganha cinco reais.'],
  [3.2, 5.2, 'Seu Jair rasgou a calça: cinco reais.'],
  [5.4, 7.4, 'O Bruno chamou a professora de mãe: cinco reais.'],
  [7.6, 10.0, 'Eu sou o Caio. E eu nunca fico com vergonha.'],
  [10.2, 12.4, 'Dancei no meio da praça: nada.'],
  [12.6, 14.8, 'Cantei no ônibus: nada.'],
  [15.0, 17.2, 'Vesti fantasia de galinha: nada.'],
  [17.4, 19.6, 'Aí a Ana, da minha sala, me deu oi.'],
  [19.8, 21.8, 'Meu rosto pegou fogo.'],
  [22.0, 24.2, 'Mil reais de vergonha!'],
  [24.4, 26.8, 'Eu fui responder “oi”… e saiu “mãe”.'],
  [27.0, 29.8, 'Mil e cinco reais. E um apelido: Tomate.'],
];

const SALDO = t => t < 22.4 ? 0 : t < 23.4 ? Math.round(1000 * easeOut(t - 22.4)) : t < 25.9 ? 1000 : 1005;
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => { const v = SALDO(t0 + lt); showCard(id, lt, from, x, y, v, v === 0 ? '#8a86a0' : '#2fae60', s, shake); };
const BRUNO = { kid: 1, skin: '#e0a27a', shirt: '#3fae6a', stripe: '#2f8a52', shorts: '#55556e', shoe: '#fff', hair: 'short', hairCol: '#1c1412', pocket: 0 };
const ANA = { kid: 1, skin: '#d9a27a', shirt: '#7fc8a9', dress: '#7fc8a9', shoe: '#e86fa0', hair: 'bun', hairCol: '#3a2418', pocket: 0 };
const KID2 = { kid: 1, skin: '#8a5636', shirt: '#f5c531', shorts: '#3b5bb5', shoe: '#e8453c', hair: 'curly', hairCol: '#1c1412', pocket: 0 };
const nada = id => tagSvg(id, 'NADA', '#8a86a0', 130);
// cabeça do Caio (kid): centro y = -376, topo y = -504 (coordenadas locais, pés em 0)
const HEAD = { y: -376, top: -504, ear: 124 };
const steamSvg = id => `<g id="${id}">${[0, 1, 2, 3].map(i => `<circle class="sm" r="34" fill="#fff" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`;
function steam(id, lt, on, x, y, s) { $(id).querySelectorAll('.sm').forEach((c, i) => { const p = ((lt * 1.2 + i / 4) % 1); const side = i % 2 ? 1 : -1; c.setAttribute('display', on ? 'inline' : 'none'); c.setAttribute('cx', x + side * (HEAD.ear + 30 + p * 80) * s); c.setAttribute('cy', y + (HEAD.y - p * 160) * s); c.setAttribute('r', (20 + p * 30) * s); c.setAttribute('opacity', 1 - p); }); }
const plaza = () => sky() + backBuildings() + `<g>${[150, 930].map(x => `<rect x="${x - 22}" y="900" width="44" height="440" fill="#8a5a3a" stroke="${OL}" stroke-width="6"/><circle cx="${x}" cy="860" r="150" fill="#6fbf6a" stroke="${OL}" stroke-width="${SW}"/>`).join('')}</g>` + street();
const classroom = () => floorIn(1340, '#e9dcc0', '#d9c4a0') + `<rect x="60" y="360" width="960" height="420" fill="#2f6b4f" stroke="${OL}" stroke-width="${SW}"/><rect x="40" y="780" width="1000" height="30" fill="#c98a52" stroke="${OL}" stroke-width="6"/><text x="540" y="620" text-anchor="middle" font-family="Luckiest" font-size="120" fill="#f4f4ee" opacity=".9">2 x 3 = 6</text>`;

// 1. gancho: Dona Cida escorrega na casca de banana — rosto vermelho, +R$ 5
shot(0, 3.1, () => {
  const c = mk('cida');
  let coins = ''; for (let i = 0; i < 3; i++) coins += coinSvg('e7k1' + i);
  const svg = plaza() + `<g id="e7ban"><path d="M-60,0 Q-20,-40 0,-10 Q20,-40 60,0 Q20,-10 0,-20 Q-20,-10 -60,0 Z" fill="#ffd23f" stroke="${OL}" stroke-width="6"/></g>` + `<g>${c.svg}</g>` + steamSvg('e7st1') + coins + tagSvg('e7t1', '+R$5', '#2fae60', 120) + tagSvg('e7fx1', 'ZUPT!', '#ffd23f', 110);
  return {
    svg, cam: lt => ({ s: lerp(2.8, 1.05, easeOut(lt / 1.0)), fx: 540, fy: 1000, blur: lt < .8 ? 22 * (1 - lt / .8) : 0 }),
    update(lt) {
      const slip = K(lt, [[.5, 0], [.8, 1]]);
      const red = K(lt, [[1.0, 0], [1.5, 1]]);
      setChar(c.id, { x: K(lt, [[0, 380], [.5, 520]]), y: 1490 + slip * 40, scale: 1.0, t: lt, mouth: lt > .8 ? 'O' : 'smile', eyes: lt > .8 ? 'wide' : 'open', brow: lt > .8 ? 1 : 0, lean: -slip * 28, armL: lerp(15, 150, slip), armR: lerp(15, 120, slip), red, walk: lt < .5 ? 1.6 : 0, legL: slip * 50, seed: 1 });
      $('e7ban').setAttribute('transform', `translate(${560 + slip * 120},${1480 - slip * 60}) rotate(${slip * 200})`);
      popTag('e7fx1', lt, .5, 760, 1200, .8);
      for (let i = 0; i < 3; i++) flyCoin('e7k1' + i, lt, 1.2 + i * .25, 540, 1250, 300 + i * 220, 760, .7, 150);
      popTag('e7t1', lt, 1.3, 540, 700, 1.4);
    }
  };
});

// 2. Seu Jair rasga a calça (RIIIP!)
shot(3.1, 5.3, () => {
  const j = mk('jair');
  const svg = plaza() + `<g>${j.svg}</g><g id="e7rip" opacity="0"><path d="M-70,-10 L-40,-40 L-10,-5 L20,-40 L50,-5 L75,-30 L75,40 L-70,40 Z" fill="#fff" stroke="${OL}" stroke-width="6"/>${[-40, 0, 40].map(x => `<path d="M${x},20 c-10,-14 -22,0 0,12 c22,-12 10,-26 0,-12 Z" fill="#e8453c"/>`).join('')}</g>`
    + tagSvg('e7fx2', 'RIIIP!', '#e8453c', 130) + coinSvg('e7k2') + tagSvg('e7t2', '+R$5', '#2fae60', 120);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2.2, 1.3]]), fx: 540, fy: 1150 }),
    update(lt) {
      const bend = K(lt, [[.1, 0], [.6, 1], [.9, 1], [1.2, 0]]);
      const rip = lt > .6;
      setChar(j.id, { x: 540, y: 1500, scale: 1.05, t: lt, mouth: rip ? 'O' : 'flat', eyes: rip ? 'wide' : 'half', brow: rip ? 1 : 0, squash: -bend * .12, tilt: bend * 10, armL: 20 + bend * 30, armR: 20 + bend * 30, red: K(lt, [[.7, 0], [1.1, 1]]), sweat: rip, seed: 2 });
      $('e7rip').setAttribute('opacity', rip ? 1 : 0); $('e7rip').setAttribute('transform', `translate(540,${1500 - 210 * 1.05}) scale(1.1)`);
      popTag('e7fx2', lt, .6, 780, 900, .9);
      flyCoin('e7k2', lt, 1.1, 560, 1250, 820, 700, .7, 150); popTag('e7t2', lt, 1.2, 300, 760, .9);
    }
  };
});

// 3. o Bruno chama a professora de mãe
shot(5.3, 7.5, () => {
  const b = mk('caio', BRUNO), p = mk('prof');
  const svg = classroom() + `<g>${p.svg}</g><g>${b.svg}</g>` + bubbleSvg('e7b3', 'Valeu, mãe!', 400, 54) + coinSvg('e7k3') + tagSvg('e7t3', '+R$5', '#2fae60', 120);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.2, 1.15]]), fx: 540, fy: 1100 }),
    update(lt) {
      const oops = lt > .9;
      setChar(p.id, { x: 760, y: 1480, scale: .95, t: lt, mouth: oops ? 'smug' : 'smile', eyes: oops ? 'half' : 'open', brow: oops ? .8 : 0, armR: 100, seed: 3, lookX: -10 });
      setChar(b.id, { x: 320, y: 1480, scale: 1.0, t: lt, mouth: oops ? 'O' : 'smile', talk: lt < .8, eyes: oops ? 'wide' : 'happy', brow: oops ? 1 : 0, red: K(lt, [[.9, 0], [1.3, 1]]), armL: lt < .8 ? 120 : 20, sweat: oops, seed: 4, lookX: 10 });
      showBubble('e7b3', lt, .1, 1.2, 380, 760);
      flyCoin('e7k3', lt, 1.2, 330, 1200, 600, 700, .7, 150); popTag('e7t3', lt, 1.3, 540, 640, .8);
    }
  };
});

// 4. Caio: "eu nunca fico com vergonha" (óculos escuros), saldo R$ 0
shot(7.5, 10.1, () => {
  const k = mk('caio');
  const svg = plaza() + `<g>${k.svg}</g>` + cardSvg('e7c4');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.2], [2.6, 1.3]]), fx: 540, fy: 1100 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1500, scale: 1.1, t: lt, mouth: 'smug', talk: lt < 2.3, shades: 1, armL: 40, armR: 40, tilt: 5, seed: 5 });
      card('e7c4', 7.5, lt, 540, 400, 1.1, 0, 1.0);
    }
  };
});

// 5. dança no meio da praça: NADA
shot(10.1, 12.5, () => {
  const k = mk('caio'), a = mk('n1'), c = mk('cida');
  const svg = plaza() + `<g>${a.svg}</g><g>${c.svg}</g><g>${k.svg}</g>` + nada('e7n5') + cardSvg('e7c5') + [0, 1, 2].map(i => `<g id="e7mn5${i}"><text font-family="Luckiest" font-size="80" fill="#8f6bd1" stroke="${OL}" stroke-width="6" paint-order="stroke">♪</text></g>`).join('');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.4, 1.08]]), fx: 540, fy: 1100 }),
    update(lt) {
      const d = Math.sin(lt * 9);
      setChar(k.id, { x: 540 + d * 30, y: 1500, scale: 1.0, t: lt, mouth: 'smile', eyes: 'happy', armL: 90 + d * 70, armR: 90 - d * 70, lean: d * 12, hop: 4.5, seed: 6 });
      setChar(a.id, { x: 150, y: 1500, scale: .8, t: lt, mouth: 'flat', eyes: 'half', seed: 7, lookX: 12 });
      setChar(c.id, { x: 930, y: 1500, scale: .8, t: lt, mouth: 'flat', eyes: 'half', seed: 8, lookX: -12 });
      for (let i = 0; i < 3; i++) { const p = ((lt * .8 + i / 3) % 1); $('e7mn5' + i).setAttribute('transform', `translate(${380 + i * 150 + Math.sin(p * 6) * 30},${900 - p * 300})`); $('e7mn5' + i).setAttribute('opacity', 1 - p); }
      showPop('e7n5', lt, 1.4, 540, 640, 1); card('e7c5', 10.1, lt, 540, 300, .9);
    }
  };
});

// 6. canta no ônibus: NADA
shot(12.5, 14.9, () => {
  const k = mk('caio'), a = mk('n1', { sit: 1 }), c = mk('cida', { sit: 1, shorts: '#e86fa0' });
  let outside = ''; for (let i = 0; i < 10; i++) outside += `<rect x="${i * 260}" y="${520 + (i % 3) * 40}" width="200" height="400" fill="${['#bdb6da', '#a8d8c7', '#f2c29b'][i % 3]}" stroke="${OL}" stroke-width="5"/>`;
  const svg = `<rect x="-200" y="-200" width="1480" height="2400" fill="#f2d48a"/><clipPath id="e7win"><rect x="0" y="420" width="1080" height="380"/></clipPath><g clip-path="url(#e7win)"><rect x="0" y="420" width="1080" height="380" fill="#cfe6ef"/><g id="e7out">${outside}</g></g>`
    + `${[0, 1, 2, 3].map(i => `<rect x="${i * 270 - 10}" y="420" width="30" height="380" fill="#e8e2d6" stroke="${OL}" stroke-width="6"/>`).join('')}<rect x="-200" y="400" width="1480" height="24" fill="#e8e2d6" stroke="${OL}" stroke-width="6"/><rect x="-200" y="796" width="1480" height="24" fill="#e8e2d6" stroke="${OL}" stroke-width="6"/>`
    + `<rect x="-200" y="1400" width="1480" height="700" fill="#8a8fa8" stroke="${OL}" stroke-width="${SW}"/><rect x="520" y="200" width="26" height="1220" fill="#ffd23f" stroke="${OL}" stroke-width="6"/>`
    + `<rect x="40" y="1150" width="320" height="250" rx="30" fill="#3b5bb5" stroke="${OL}" stroke-width="7"/><rect x="720" y="1150" width="320" height="250" rx="30" fill="#3b5bb5" stroke="${OL}" stroke-width="7"/>`
    + `<g>${a.svg}</g><g>${c.svg}</g><g>${k.svg}</g>` + nada('e7n6') + cardSvg('e7c6') + [0, 1, 2].map(i => `<g id="e7mn6${i}"><text font-family="Luckiest" font-size="80" fill="#e8453c" stroke="${OL}" stroke-width="6" paint-order="stroke">♪</text></g>`).join('');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.4, 1.08]]), fx: 540, fy: 1100, tx: Math.sin(lt * 20) * 2 }),
    update(lt) {
      $('e7out').setAttribute('transform', `translate(${-(lt * 600) % 780},0)`);
      setChar(a.id, { x: 200, y: 1340, scale: .8, t: lt, mouth: 'flat', eyes: 'half', seed: 9, lookX: 12 });
      setChar(c.id, { x: 880, y: 1340, scale: .8, t: lt, mouth: 'frown', eyes: 'half', brow: -.5, seed: 10, lookX: -12 });
      setChar(k.id, { x: 540, y: 1480, scale: 1.0, t: lt, mouth: 'O', talk: 1, eyes: 'happy', armL: 120 + Math.sin(lt * 4) * 20, armR: 40, tilt: Math.sin(lt * 3) * 8, seed: 11 });
      for (let i = 0; i < 3; i++) { const p = ((lt * .8 + i / 3) % 1); $('e7mn6' + i).setAttribute('transform', `translate(${460 + i * 90 + Math.sin(p * 6) * 30},${960 - p * 300})`); $('e7mn6' + i).setAttribute('opacity', 1 - p); }
      showPop('e7n6', lt, 1.4, 540, 640, 1); card('e7c6', 12.5, lt, 540, 300, .9);
    }
  };
});

// 7. fantasia de galinha: NADA
shot(14.9, 17.3, () => {
  const k = mk('caio'), b = mk('caio', BRUNO), d = mk('caio', KID2);
  const chicken = `<g id="e7chk"><g id="e7wingL"><path d="M110,-250 Q230,-210 200,-90 Q150,-120 110,-100 Z" fill="#fff6c8" stroke="${OL}" stroke-width="7"/></g><g id="e7wingR"><path d="M-110,-250 Q-230,-210 -200,-90 Q-150,-120 -110,-100 Z" fill="#fff6c8" stroke="${OL}" stroke-width="7"/></g>
    <ellipse cx="0" cy="-160" rx="135" ry="118" fill="#fff6c8" stroke="${OL}" stroke-width="8"/><path d="M-60,-90 L-40,-60 L-20,-90 L0,-60 L20,-90 L40,-60 L60,-90" fill="none" stroke="#f5c531" stroke-width="8"/>
    <path d="M-40,${HEAD.top + 10} q10,-60 30,-20 q10,-60 30,0 q20,-50 30,10 Z" fill="#e8453c" stroke="${OL}" stroke-width="6"/>
    <path d="M-34,${HEAD.y - 6} L34,${HEAD.y - 6} L0,${HEAD.y + 30} Z" fill="#ff9a2e" stroke="${OL}" stroke-width="6" transform="translate(0,-28)"/></g>`;
  const svg = plaza() + `<g>${b.svg}</g><g>${d.svg}</g><g>${k.svg}</g>` + chicken + nada('e7n7') + cardSvg('e7c7') + tagSvg('e7fx7', 'CÓ CÓ!', '#ffd23f', 110);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.4, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      const f = Math.sin(lt * 14);
      setChar(k.id, { x: 540, y: 1500, scale: 1.0, t: lt, mouth: 'smile', talk: 1, eyes: 'happy', armL: 20, armR: 20, hop: 3, seed: 12 });
      const hop = -Math.abs(Math.sin(lt * 3 * Math.PI)) * 26;
      $('e7chk').setAttribute('transform', `translate(540,${1500 + hop})`);
      $('e7wingL').setAttribute('transform', `rotate(${f * 20},110,-260)`); $('e7wingR').setAttribute('transform', `rotate(${-f * 20},-110,-260)`);
      setChar(b.id, { x: 150, y: 1500, scale: .85, t: lt, mouth: 'smug', eyes: 'half', seed: 13, lookX: 12 });
      setChar(d.id, { x: 930, y: 1500, scale: .85, t: lt, mouth: 'flat', eyes: 'half', seed: 14, lookX: -12 });
      popTag('e7fx7', lt, .3, 800, 900, 1.0);
      showPop('e7n7', lt, 1.4, 540, 640, 1); card('e7c7', 14.9, lt, 540, 300, .9);
    }
  };
});

// 8. a Ana dá oi
shot(17.3, 19.7, () => {
  const k = mk('caio'), a = mk('caio', ANA);
  let sp = ''; [[680, 900], [920, 1000], [760, 1120]].forEach((p, i) => sp += `<g id="e7sp8${i}">${sparkle(...p, .9)}</g>`);
  const svg = floorIn(1340, '#f6d9a8', '#d9c4a0') + `<rect x="0" y="380" width="1080" height="80" fill="#e8453c" stroke="${OL}" stroke-width="6"/>${[0, 1, 2, 3].map(i => `<rect x="${60 + i * 260}" y="560" width="160" height="440" rx="10" fill="#5fb3e0" stroke="${OL}" stroke-width="7"/>`).join('')}`
    + `<g>${k.svg}</g><g>${a.svg}</g>` + sp + bubbleSvg('e7b8', 'Oi, Caio!', 330, 56);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.4, 1.12]]), fx: 600, fy: 1100 }),
    update(lt) {
      setChar(a.id, { x: K(lt, [[0, 1200], [.8, 790]]), y: 1500, scale: 1.0, t: lt, mouth: 'smile', talk: lt > .9 && lt < 1.5, eyes: lt > 1.6 ? 'happy' : 'open', armR: lt > .8 ? 150 + Math.sin(lt * 14) * 15 : 15, walk: lt < .8 ? 1.6 : 0, seed: 15, lookX: -12 });
      const froze = lt > 1.0;
      setChar(k.id, { x: 320, y: 1500, scale: 1.0, t: lt, mouth: froze ? 'flat' : 'smug', eyes: froze ? 'wide' : 'open', brow: froze ? 1 : 0, squash: froze && lt < 1.2 ? -.05 : 0, seed: 16, lookX: 12 });
      for (let i = 0; i < 3; i++) $('e7sp8' + i).setAttribute('opacity', lt > .8 ? Math.abs(Math.sin(lt * 5 + i)) : 0);
      showBubble('e7b8', lt, .9, 2.4, 790, 820);
    }
  };
});

// 9. close: o rosto pega fogo (vermelho + vapor saindo das orelhas)
shot(19.7, 21.9, () => {
  const k = mk('caio');
  const svg = floorIn(1340, '#f6d9a8', '#d9c4a0') + `<g>${k.svg}</g>` + steamSvg('e7st9') + tagSvg('e7fx9', 'FSSSH!', '#fff', 110);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.9], [2.2, 2.25]]), fx: 540, fy: 1060, tx: lt > 1.2 ? Math.sin(lt * 60) * 4 : 0 }),
    update(lt) {
      const red = K(lt, [[.2, 0], [1.3, 1]]);
      setChar(k.id, { x: 540, y: 1500, scale: 1.1, t: lt, mouth: 'flat', eyes: 'wide', brow: 1, red, sweat: 1, squash: Math.sin(lt * 40) * .005, seed: 17 });
      steam('e7st9', lt, red > .6, 540, 1500, 1.1);
      popTag('e7fx9', lt, 1.2, 560, 820, .9);
    }
  };
});

// 10. MIL REAIS de vergonha (chuva de notas)
shot(21.9, 24.3, () => {
  const k = mk('caio');
  let notes = ''; for (let i = 0; i < 12; i++) notes += noteSvg('e7n10' + i, '100', '#9bc6ef', '#2f5f9a');
  const svg = sky('#fff3c4') + `<g id="e7rays">${Array.from({ length: 12 }, (_, i) => `<path d="M540,900 L${540 + Math.cos(i * .5236) * 1600},${900 + Math.sin(i * .5236) * 1600} L${540 + Math.cos(i * .5236 + .2) * 1600},${900 + Math.sin(i * .5236 + .2) * 1600} Z" fill="#ffe27a"/>`).join('')}</g>`
    + floorIn(1340, 'rgba(0,0,0,0)', '#d9c4a0') + `<g>${k.svg}</g>` + steamSvg('e7st10') + notes + bigNum('e7plus', '+R$ 1.000', 170, '#3fbf6a') + cardSvg('e7c10');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.1], [2.4, 1.18]]), fx: 540, fy: 1050 }),
    update(lt) {
      $('e7rays').setAttribute('transform', `rotate(${lt * 15},540,900)`);
      setChar(k.id, { x: 540, y: 1520, scale: 1.1, t: lt, mouth: 'flat', eyes: 'wide', brow: 1, red: 1, sweat: 1, seed: 18 });
      steam('e7st10', lt, true, 540, 1520, 1.1);
      for (let i = 0; i < 12; i++) { const el = $('e7n10' + i); const p = lt - .3 - i * .1; if (p < 0) { el.setAttribute('display', 'none'); continue; } el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${60 + (i * 97) % 960 + Math.sin(p * 5 + i) * 40},${-100 + p * 700}) rotate(${Math.sin(p * 6 + i) * 30})`); }
      showPop('e7plus', lt, .4, 540, 560, 1);
      card('e7c10', 21.9, lt, 540, 300, 1.0, 0, .5);
    }
  };
});

// 11. "Oi… mãe!" (+R$ 5)
shot(24.3, 26.9, () => {
  const k = mk('caio'), a = mk('caio', ANA);
  const svg = floorIn(1340, '#f6d9a8', '#d9c4a0') + `<g>${k.svg}</g><g>${a.svg}</g>` + steamSvg('e7st11') + bubbleSvg('e7b11', 'Oi… MÃE!', 340, 58)
    + `<text id="e7q11" x="830" y="820" text-anchor="middle" font-family="Luckiest" font-size="120" fill="#3b5bb5" stroke="${OL}" stroke-width="8" paint-order="stroke">?</text>` + coinSvg('e7k11') + tagSvg('e7t11', '+R$5', '#2fae60', 120);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.6, 1.15]]), fx: 560, fy: 1100 }),
    update(lt) {
      const said = lt > 1.2;
      setChar(k.id, { x: 320, y: 1500, scale: 1.0, t: lt, mouth: said ? 'O' : 'flat', talk: lt > .5 && lt < 1.2, eyes: 'wide', brow: 1, red: 1, sweat: 1, squash: said && lt < 1.5 ? -.06 : 0, seed: 19, lookX: 12 });
      steam('e7st11', lt, true, 320, 1500, 1.0);
      setChar(a.id, { x: 790, y: 1500, scale: 1.0, t: lt, mouth: said ? 'o' : 'smile', eyes: said ? 'wide' : 'open', brow: said ? 1 : 0, tilt: said ? 10 : 0, seed: 20, lookX: -12 });
      showBubble('e7b11', lt, .5, 2.6, 380, 820);
      $('e7q11').setAttribute('opacity', said ? 1 : 0); $('e7q11').setAttribute('transform', `translate(0,${Math.sin(lt * 6) * 8})`);
      flyCoin('e7k11', lt, 1.6, 330, 1200, 600, 600, .7, 150); popTag('e7t11', lt, 1.7, 560, 640, .9);
    }
  };
});

// 12. a turma ri: "TOMATE!" — Caio vermelho com cabinho verde
shot(26.9, 30.0, () => {
  const k = mk('caio'), b = mk('caio', BRUNO), d = mk('caio', KID2), a = mk('caio', ANA);
  const svg = floorIn(1340, '#f6d9a8', '#d9c4a0') + `<g>${b.svg}</g><g>${d.svg}</g><g>${a.svg}</g><g>${k.svg}</g>`
    + `<g id="e7stem"><path d="M0,0 L0,-50" stroke="#3f8f3f" stroke-width="14" stroke-linecap="round"/><path d="M0,-10 q-60,-40 -90,0 q40,30 90,0 M0,-10 q60,-40 90,0 q-40,30 -90,0" fill="#5fae4f" stroke="${OL}" stroke-width="6"/></g>`
    + bubbleSvg('e7b12', 'TOMATE!', 330, 64) + cardSvg('e7c12');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [3.1, 1.1]]), fx: 540, fy: 1100 }),
    update(lt) {
      const laugh = lt > .4;
      setChar(b.id, { x: 140, y: 1500, scale: .85, t: lt, mouth: laugh ? 'smile' : 'smug', talk: laugh, eyes: laugh ? 'happy' : 'half', armL: laugh ? 100 : 20, hop: laugh ? 3 : 0, seed: 21 });
      setChar(d.id, { x: 940, y: 1500, scale: .85, t: lt + .3, mouth: laugh ? 'smile' : 'smug', talk: laugh, eyes: laugh ? 'happy' : 'half', armR: laugh ? 100 : 20, hop: laugh ? 3 : 0, seed: 22 });
      setChar(a.id, { x: 760, y: 1500, scale: .9, t: lt, mouth: 'smug', eyes: 'happy', red: .3, armR: 40, seed: 23 });
      setChar(k.id, { x: 420, y: 1500, scale: 1.0, t: lt, mouth: lt > 2 ? 'smug' : 'flat', eyes: lt > 2 ? 'half' : 'wide', red: 1, seed: 24 });
      $('e7stem').setAttribute('transform', `translate(420,${1500 + HEAD.top - 20}) scale(${backOut((lt - .9) / .3)})`);
      showBubble('e7b12', lt, .4, 3.1, 250, 870);
      card('e7c12', 26.9, lt, 540, 300, 1.0, 0, 1.2);
    }
  };
});
