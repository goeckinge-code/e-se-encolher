// Episódio 2: "Na minha cidade, cada mentira custa dez reais."
// Caio ganha R$ 100, mente o dia inteiro, sobra a última nota; fala a verdade para a mãe e descobre que verdade dá dinheiro.
LINES = [
  [0.3, 2.6, 'Na minha cidade, cada mentira custa dez reais.'],
  [2.8, 5.0, 'Eu sou o Caio. Meu avô me deu cem reais.'],
  [5.2, 6.7, '“Escovou os dentes?” “Escovei!”'],
  [6.9, 8.4, '“Quem quebrou o vaso?” “O gato!”'],
  [8.6, 10.2, 'E foi assim o dia inteiro.'],
  [10.4, 12.3, 'Sobrou uma nota de dez.'],
  [12.5, 14.6, 'Aí minha mãe fez uma comida nova.'],
  [14.8, 16.4, '“Gostou, filho?”'],
  [16.6, 18.6, 'Era a minha última nota.'],
  [18.8, 20.8, '“Mãe… tá horrível.”'],
  [21.0, 23.4, 'E aí eu descobri: verdade dá dinheiro!'],
  [23.6, 26.6, '“Sua aula é chata.” “Seu presente é feio.”'],
  [26.8, 29.8, 'Agora eu tô rico. E de castigo até o Natal.'],
];

// saldo do Caio ao longo do vídeo (mesmo valor em todos os planos)
const STEPS = [[3.9, 100], [6.1, 90], [7.9, 80], [8.85, 70], [9.1, 60], [9.35, 50], [9.6, 40], [9.8, 30], [10.0, 20], [10.2, 10], [21.6, 60], [24.3, 110], [25.9, 160]];
const SALDO = t => { let v = 100; for (const [a, b] of STEPS) if (t >= a) v = b; return v; };
const saldoCol = v => v <= 20 ? '#e8453c' : '#2fae60';
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => showCard(id, lt, from, x, y, SALDO(t0 + lt), saldoCol(SALDO(t0 + lt)), s, shake);

const bathroom = () => `<rect x="-200" y="-200" width="1480" height="1600" fill="#cfe9f5"/>` +
  Array.from({ length: 14 }, (_, i) => `<path d="M${-100 + i * 100},-200 L${-100 + i * 100},1340" stroke="#b3d6e6" stroke-width="5"/><path d="M-200,${i * 100} L1280,${i * 100}" stroke="#b3d6e6" stroke-width="5"/>`).join('') +
  `<rect x="-200" y="1340" width="1480" height="900" fill="#e8e2d6" stroke="${OL}" stroke-width="${SW}"/>`;
const door = (x, col = '#c9773f') => `<rect x="${x}" y="1000" width="210" height="340" fill="#6b4a3a" stroke="${OL}" stroke-width="${SW}"/><rect x="${x + 14}" y="1010" width="182" height="330" fill="${col}" stroke="${OL}" stroke-width="6"/>`;

// 1. gancho: o moço sentado jura que "tá chegando" e perde R$ 10
shot(0, 2.7, () => {
  const n = mk('n1', { sit: 1 });
  const svg = sky() + backBuildings() + house(-40, 420, 560, '#a8d8c7') + house(400, 360, 500, '#f2c29b', { doorCol: '#4a6fa5', winX: 190 }) + house(780, 360, 540, '#c9b6e4') + street()
    + `<rect x="300" y="1360" width="480" height="40" rx="12" fill="#c98a52" stroke="${OL}" stroke-width="6"/><rect x="330" y="1400" width="26" height="80" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/><rect x="724" y="1400" width="26" height="80" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/>`
    + `<g>${n.svg}</g><rect x="586" y="1150" width="40" height="70" rx="8" fill="#2b2745"/>`
    + bubbleSvg('e2b1', 'Tô chegando!', 430, 56) + noteSvg('e2n1') + tagSvg('e2t1', '-R$10', '#e8453c', 110);
  return {
    svg, cam: lt => ({ s: lerp(3.2, 1.25, easeOut(lt / .9)), fx: 560, fy: 1000, blur: lt < .7 ? 22 * (1 - lt / .7) : 0 }),
    update(lt) {
      setChar(n.id, { x: 540, y: 1400, scale: .85, t: lt, mouth: 'smile', talk: lt < 1.0, armL: 150, eyes: lt > 1.2 ? 'wide' : 'open', brow: lt > 1.2 ? 1 : 0, seed: 1, lookX: 6 });
      showBubble('e2b1', lt, .1, 2.7, 560, 830);
      flyNote('e2n1', lt, 1.1, 600, 1250, 900, 650, 1.2); popTag('e2t1', lt, 1.2, 330, 1060, 1.3);
    }
  };
});

// 2. Caio ganha R$ 100 do avô
shot(2.7, 5.1, () => {
  const k = mk('caio'), a = mk('avo', { sit: 0 });
  const svg = sky() + house(-60, 1200, 1000, '#f2c29b', { roof: false, doorX: 440, doorCol: '#4a6fa5', winX: 80, winY: 250 }) + street()
    + `<g>${a.svg}</g><g>${k.svg}</g>` + noteSvg('e2n2', '100', '#9bc6ef', '#2f5f9a') + cardSvg('e2c2');
  return {
    svg, cam: lt => ({ s: 1.12 + lt * .02, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(a.id, { x: 760, y: 1480, scale: .95, t: lt, mouth: 'smile', eyes: 'happy', armR: lt < 1.0 ? 70 : 15, seed: 2 });
      const got = lt > 1.0;
      setChar(k.id, { x: 330, y: 1480, scale: 1.0, t: lt, mouth: 'smile', talk: 1, eyes: got ? 'happy' : 'wide', armL: got ? 150 : 60, hop: got && lt < 1.8 ? 3 : 0, seed: 3 });
      const nt = $('e2n2'); nt.setAttribute('display', 'inline');
      const p = clamp((lt - .5) / .5); const nx = lerp(610, 470, p), ny = lerp(1100, got ? 820 : 1060, p);
      nt.setAttribute('transform', `translate(${got ? 470 : nx},${got ? 800 + Math.sin(lt * 8) * 8 : ny}) rotate(${got ? Math.sin(lt * 6) * 10 : -8}) scale(1.1)`);
      card('e2c2', 2.7, lt, 540, 330, 1.15, 0, 1.2);
    }
  };
});

// 3. banheiro: "Escovou os dentes?" "Escovei!"
shot(5.1, 6.8, () => {
  const k = mk('caio'), m = mk('mae');
  const svg = bathroom() + door(-20) + `<rect x="560" y="640" width="320" height="380" rx="20" fill="#e6f6fb" stroke="${OL}" stroke-width="${SW}"/><path d="M600,700 L660,640 M640,740 L760,640" stroke="#fff" stroke-width="14"/>
    <rect x="560" y="1080" width="360" height="70" rx="16" fill="#fff" stroke="${OL}" stroke-width="${SW}"/><rect x="690" y="1150" width="90" height="190" fill="#fff" stroke="${OL}" stroke-width="7"/>
    <rect x="800" y="1040" width="90" height="16" rx="8" fill="#5fb3e0" stroke="${OL}" stroke-width="5"/><rect x="866" y="1030" width="30" height="28" rx="6" fill="#fff" stroke="${OL}" stroke-width="5"/>`
    + sparkle(850, 1000, .7) + `<g>${m.svg}</g><g>${k.svg}</g>` + bubbleSvg('e2b3a', 'Escovou os dentes?', 560, 48) + bubbleSvg('e2b3b', 'Escovei!', 330, 56)
    + noteSvg('e2n3') + tagSvg('e2t3', '-R$10') + cardSvg('e2c3');
  return {
    svg, cam: lt => ({ s: 1.05 + lt * .03, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(m.id, { x: 130, y: 1480, scale: .9, t: lt, mouth: 'smug', talk: lt < .8, brow: .3, armR: 15, armL: 15, seed: 4, lookX: 10 });
      setChar(k.id, { x: 560, y: 1480, scale: 1.0, t: lt, mouth: 'smile', talk: lt > .8 && lt < 1.4, eyes: lt > .8 ? 'happy' : 'open', armL: 25, seed: 5, lookX: -10 });
      showBubble('e2b3a', lt, .05, .85, 330, 640); showBubble('e2b3b', lt, .85, 1.7, 560, 760);
      flyNote('e2n3', lt, 1.0, 620, 1250, 980, 720, .7); popTag('e2t3', lt, 1.05, 860, 980, .65);
      card('e2c3', 5.1, lt, 540, 240, .9);
    }
  };
});

// 4. sala: "Quem quebrou o vaso?" "O gato!"
shot(6.8, 8.6, () => {
  const k = mk('caio'), m = mk('mae');
  let shards = ''; [[430, 1450, 20], [500, 1470, -30], [560, 1440, 50], [610, 1475, 10]].forEach(([x, y, r]) => shards += `<path d="M${x - 30},${y} L${x},${y - 34} L${x + 30},${y} Z" fill="#4a8fd6" stroke="${OL}" stroke-width="6" transform="rotate(${r},${x},${y})"/>`);
  const svg = floorIn(1340, '#f6d9a8', '#d9c4a0') + `<rect x="80" y="420" width="300" height="220" rx="10" fill="#bfe3f2" stroke="${OL}" stroke-width="${SW}"/><rect x="700" y="1200" width="40" height="140" fill="#8a5a3a" stroke="${OL}" stroke-width="5"/><rect x="620" y="1170" width="200" height="40" rx="8" fill="#c98a52" stroke="${OL}" stroke-width="6"/>`
    + `<g>${m.svg}</g><g>${k.svg}</g>` + shards + catSvg('e2cat') + bubbleSvg('e2b4a', 'Quem quebrou o vaso?', 600, 46) + bubbleSvg('e2b4b', 'O gato!', 300, 56)
    + noteSvg('e2n4') + tagSvg('e2t4', '-R$10') + cardSvg('e2c4');
  return {
    svg, cam: lt => ({ s: 1.0 + lt * .03, fx: 540, fy: 1100 }),
    update(lt) {
      setChar(m.id, { x: 150, y: 1500, scale: .85, t: lt, mouth: lt < .8 ? 'frown' : 'flat', talk: lt < .8, brow: -1, mad: lt < .8, armR: 15, armL: 70, seed: 6, lookX: 10 });
      setChar(k.id, { x: 470, y: 1500, scale: .95, t: lt, mouth: 'smile', talk: lt > .8 && lt < 1.4, armL: lt > .8 ? 95 : 15, seed: 7, lookX: 12 });
      setCat('e2cat', lt, 860, 1500, .85, lt > .95);
      showBubble('e2b4a', lt, .05, .85, 380, 560); showBubble('e2b4b', lt, .85, 1.8, 520, 780);
      flyNote('e2n4', lt, 1.0, 520, 1260, 260, 700, .7); popTag('e2t4', lt, 1.05, 280, 920, .7);
      card('e2c4', 6.8, lt, 540, 240, .9);
    }
  };
});

// 5. montagem: "Fiz!" "Comi!" "Tô dormindo!" (o saldo despenca)
shot(8.6, 10.3, () => {
  const k1 = mk('caio'), k2 = mk('caio'), k3 = mk('caio', { sit: 1 });
  const sub = [
    `<g id="e2s5a">${floorIn(1340, '#c9b6e4', '#e4d6bd')}<g>${k1.svg}</g><rect x="140" y="1180" width="800" height="50" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/><rect x="380" y="1120" width="320" height="64" fill="#fff" stroke="${OL}" stroke-width="6"/><text x="540" y="1166" text-anchor="middle" font-family="Luckiest" font-size="38" fill="#c3c3d6">EM BRANCO</text></g>`,
    `<g id="e2s5b">${floorIn(1340, '#f2d48a', '#e4d6bd')}<g>${k2.svg}</g><rect x="140" y="1140" width="800" height="60" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/><ellipse cx="540" cy="1140" rx="240" ry="40" fill="#fff" stroke="${OL}" stroke-width="7"/>${Array.from({ length: 7 }, (_, i) => `<ellipse cx="${400 + i * 46}" cy="${1118 - (i % 2) * 12}" rx="34" ry="20" fill="#7fc45a" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`,
    `<g id="e2s5c"><rect x="-200" y="-200" width="1480" height="2400" fill="#3c3766"/><rect x="700" y="300" width="260" height="260" fill="#1f1c40" stroke="${OL}" stroke-width="${SW}"/><circle cx="870" cy="380" r="40" fill="#fff6c8"/>
      <rect x="-200" y="1340" width="1480" height="900" fill="#4b4578" stroke="${OL}" stroke-width="${SW}"/><rect x="120" y="1100" width="840" height="260" rx="30" fill="#8f6bd1" stroke="${OL}" stroke-width="${SW}"/><rect x="130" y="980" width="220" height="130" rx="40" fill="#fff" stroke="${OL}" stroke-width="7"/>
      <g>${k3.svg}</g><rect x="200" y="1150" width="760" height="230" rx="40" fill="#5fb3e0" stroke="${OL}" stroke-width="${SW}"/><rect x="500" y="1110" width="120" height="70" rx="20" fill="#2b2745" stroke="${OL}" stroke-width="6"/><circle cx="530" cy="1140" r="10" fill="#e8453c"/><circle cx="590" cy="1140" r="10" fill="#3fbf6a"/>
      <ellipse cx="560" cy="900" rx="260" ry="200" fill="rgba(140,200,255,.18)"/></g>`,
  ];
  let notes = ''; for (let i = 0; i < 6; i++) notes += noteSvg('e2n5' + i);
  const svg = sub.join('') + notes + bubbleSvg('e2b5a', 'Fiz!', 220, 60) + bubbleSvg('e2b5b', 'Comi!', 260, 60) + bubbleSvg('e2b5c', 'Tô dormindo!', 440, 54) + cardSvg('e2c5');
  return {
    svg, cam: lt => { const i = Math.min(2, Math.floor(lt / .57)); const l = lt - i * .57; return { s: 1.1 + l * .08, fx: 540, fy: 1000, blur: l < .07 && i > 0 ? 16 : 0 }; },
    update(lt) {
      const i = Math.min(2, Math.floor(lt / .57));
      ['e2s5a', 'e2s5b', 'e2s5c'].forEach((n, j) => $(n).setAttribute('display', j === i ? 'inline' : 'none'));
      setChar(k1.id, { x: 540, y: 1330, scale: 1.0, t: lt, mouth: 'smile', talk: 1, eyes: 'happy', seed: 8 });
      setChar(k2.id, { x: 540, y: 1300, scale: 1.0, t: lt, mouth: 'smile', talk: 1, armL: 40, seed: 9 });
      setChar(k3.id, { x: 560, y: 1180, scale: .9, t: lt, mouth: 'smug', eyes: 'half', seed: 10, lookY: 6 });
      showBubble('e2b5a', lt, .02, .57, 540, 560); showBubble('e2b5b', lt, .59, 1.14, 540, 560); showBubble('e2b5c', lt, 1.16, 1.8, 560, 560);
      for (let n = 0; n < 6; n++) flyNote('e2n5' + n, lt, .2 + n * .23, 560 + (n % 3 - 1) * 60, 1200, 300 + n * 100, 600, .6);
      card('e2c5', 8.6, lt, 540, 240, .9);
    }
  };
});

// 6. sobrou uma nota de dez
shot(10.3, 12.4, () => {
  const k = mk('caio');
  const svg = sky('#c3c9de') + house(-60, 1200, 1000, '#9fc9bb', { roof: false, doorX: 160, winX: 820, winY: 260 }) + street() + `<g>${k.svg}</g>` + noteSvg('e2n6') + cardSvg('e2c6');
  return {
    svg, cam: lt => ({ s: 1.3 + lt * .04, fx: 540, fy: 1000 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: 'frown', brow: .4, tears: 1, seed: 11, tilt: -4, lookY: 8, armL: 55, armR: 55 });
      const nt = $('e2n6'); nt.setAttribute('display', 'inline'); nt.setAttribute('transform', `translate(540,${1170 + Math.sin(lt * 3) * 6}) rotate(${Math.sin(lt * 30) * 2}) scale(1.2)`);
      card('e2c6', 10.3, lt, 540, 450, 1.25, 14, .15);
    }
  };
});

// 7. a comida nova da mãe
shot(12.4, 14.7, () => {
  const k = mk('caio'), m = mk('mae');
  let bub = ''; for (let i = 0; i < 6; i++) bub += `<circle class="e2bb" cx="${420 + i * 45}" cy="1030" r="${16 + (i % 3) * 6}" fill="#9ccc4e" stroke="${OL}" stroke-width="5"/>`;
  const svg = floorIn(1340, '#f2e2a0', '#d9c4a0') + `<rect x="0" y="1140" width="1080" height="70" fill="#e8e8e8" stroke="${OL}" stroke-width="${SW}"/><rect x="0" y="1210" width="1080" height="130" fill="#c98a52" stroke="${OL}" stroke-width="${SW}"/>`
    + `<g>${m.svg}</g><g>${k.svg}</g>`
    + `<g id="e2pot"><path d="M380,1040 L700,1040 L680,1150 Q540,1180 400,1150 Z" fill="#8a8fa8" stroke="${OL}" stroke-width="${SW}" stroke-linejoin="round"/><rect x="340" y="1050" width="50" height="22" rx="10" fill="#8a8fa8" stroke="${OL}" stroke-width="6"/><rect x="690" y="1050" width="50" height="22" rx="10" fill="#8a8fa8" stroke="${OL}" stroke-width="6"/>
      <ellipse cx="540" cy="1040" rx="160" ry="30" fill="#7fb03a" stroke="${OL}" stroke-width="7"/>${bub}
      <path d="M600,1000 l50,-80 M620,960 l26,10 M612,980 l30,10 M630,940 l24,8" stroke="#f4f0e6" stroke-width="10" stroke-linecap="round"/><circle cx="652" cy="912" r="16" fill="#f4f0e6" stroke="${OL}" stroke-width="5"/></g>
      <path id="e2smoke" d="M480,960 q-40,-60 0,-120 q40,-60 0,-120 M560,950 q-40,-60 0,-120 q40,-60 0,-120" fill="none" stroke="#a678d6" stroke-width="22" stroke-linecap="round" opacity=".75"/>`;
  return {
    svg, cam: lt => ({ s: 1.05 + lt * .03, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(m.id, { x: 260, y: 1500, scale: .95, t: lt, mouth: 'smile', eyes: 'happy', armL: 50, seed: 12 });
      setChar(k.id, { x: 860, y: 1500, scale: .9, t: lt, mouth: 'yuck', brow: -1, eyes: 'half', seed: 13, lookX: -12, tilt: 6 });
      document.querySelectorAll('.e2bb').forEach((b, i) => b.setAttribute('transform', `translate(0,${-((lt * 80 + i * 23) % 50)}) scale(1)`));
      $('e2smoke').setAttribute('transform', `translate(${Math.sin(lt * 4) * 12},${-((lt * 40) % 30)})`);
    }
  };
});

// 8. close na mãe: "Gostou, filho?"
shot(14.7, 16.5, () => {
  const m = mk('mae');
  let sp = ''; [[320, 700, .8], [760, 680, 1.0]].forEach((p, i) => sp += `<g id="e2sp8${i}">${sparkle(...p)}</g>`);
  const svg = floorIn(1340, '#f2e2a0', '#d9c4a0') + `<g>${m.svg}</g>` + sp + bubbleSvg('e2b8', 'Gostou, filho?', 480, 56);
  return {
    svg, cam: lt => ({ s: 1.85 + lt * .05, fx: 540, fy: 900 }),
    update(lt) {
      setChar(m.id, { x: 540, y: 1480, scale: 1.05, t: lt, mouth: 'smile', talk: lt > .1 && lt < .9, eyes: 'wide', brow: .8, armL: 40, armR: 40, seed: 14, tilt: 5 });
      for (let i = 0; i < 2; i++) $('e2sp8' + i).setAttribute('opacity', Math.abs(Math.sin(lt * 5 + i)));
      showBubble('e2b8', lt, .05, 1.8, 540, 640);
    }
  };
});

// 9. Caio suando com a última nota
shot(16.5, 18.7, () => {
  const k = mk('caio');
  const svg = floorIn(1340, '#f2e2a0', '#d9c4a0') + `<g>${k.svg}</g>` + noteSvg('e2n9') + cardSvg('e2c9');
  return {
    svg, cam: lt => ({ s: 1.7 + lt * .12, fx: 540, fy: 980 }),
    update(lt) {
      setChar(k.id, { x: 540, y: 1480, scale: 1.2, t: lt, mouth: 'flat', eyes: 'wide', brow: .6, sweat: 1, seed: 15, lookX: Math.sin(lt * 3) * 8, armL: 55, armR: 55 });
      const nt = $('e2n9'); nt.setAttribute('display', 'inline'); nt.setAttribute('transform', `translate(${540 + Math.sin(lt * 50) * 4},1160) rotate(${Math.sin(lt * 40) * 3}) scale(1.15)`);
      card('e2c9', 16.5, lt, 540, 690, .75, 6);
    }
  };
});

// 10. "Mãe… tá horrível."
shot(18.7, 20.9, () => {
  const k = mk('caio'), m = mk('mae');
  const svg = floorIn(1340, '#f2e2a0', '#d9c4a0') + `<g>${m.svg}</g><g>${k.svg}</g>` + bubbleSvg('e2b10', 'Mãe… tá horrível.', 520, 52);
  return {
    svg, cam: lt => ({ s: 1.12 + lt * .03, fx: 540, fy: 1050 }),
    update(lt) {
      setChar(m.id, { x: 760, y: 1480, scale: 1.0, t: lt, mouth: lt > .9 ? 'O' : 'smile', eyes: lt > .9 ? 'wide' : 'open', brow: lt > .9 ? 1 : .3, seed: 16, lookX: -10, hop: lt > .9 && lt < 1.2 ? 4 : 0 });
      setChar(k.id, { x: 320, y: 1480, scale: 1.0, t: lt, mouth: 'flat', talk: lt > .1 && lt < 1.6, eyes: 'half', brow: 0, seed: 17, lookX: 10 });
      showBubble('e2b10', lt, .1, 2.2, 400, 780);
    }
  };
});

// 11. a virada: +R$ 50 (chuva de dinheiro)
shot(20.9, 23.5, () => {
  const k = mk('caio');
  let notes = ''; for (let i = 0; i < 10; i++) notes += noteSvg('e2n11' + i, '50', '#f2b8a0', '#a8492a');
  const svg = sky('#fff3c4') + `<g id="e2rays">${Array.from({ length: 12 }, (_, i) => `<path d="M540,900 L${540 + Math.cos(i * .5236) * 1600},${900 + Math.sin(i * .5236) * 1600} L${540 + Math.cos(i * .5236 + .2) * 1600},${900 + Math.sin(i * .5236 + .2) * 1600} Z" fill="#ffe27a"/>`).join('')}</g>`
    + house(-60, 1200, 300, '#a8d8c7', { roof: false, door: false, win: false }) + street() + `<g>${k.svg}</g>` + notes + bigNum('e2plus', '+R$ 50', 170, '#3fbf6a') + cardSvg('e2c11');
  return {
    svg, cam: lt => ({ s: 1.08 + lt * .03, fx: 540, fy: 1000 }),
    update(lt) {
      $('e2rays').setAttribute('transform', `rotate(${lt * 12},540,900)`);
      const happy = lt > .9;
      setChar(k.id, { x: 540, y: 1480, scale: 1.25, t: lt, mouth: happy ? 'smile' : 'O', talk: happy, eyes: happy ? 'happy' : 'wide', brow: 1, armL: happy ? 160 : 40, armR: happy ? 160 : 40, hop: happy ? 3 : 0, seed: 18, capUp: !happy ? easeOut(lt / .3) * 70 : 0 });
      for (let i = 0; i < 10; i++) {
        const el = $('e2n11' + i); const p = lt - .4 - i * .12; if (p < 0) { el.setAttribute('display', 'none'); continue; }
        el.setAttribute('display', 'inline');
        el.setAttribute('transform', `translate(${80 + (i * 113) % 940 + Math.sin(p * 5 + i) * 40},${-100 + p * 700}) rotate(${Math.sin(p * 6 + i) * 30})`);
      }
      showPop('e2plus', lt, .5, 540, 520, 1);
      card('e2c11', 20.9, lt, 540, 300, .85, 0, .9);
    }
  };
});

// 12. só a verdade: professora e avô (+50, +50)
shot(23.5, 26.7, () => {
  const k1 = mk('caio'), p = mk('prof'), k2 = mk('caio'), a = mk('avo', { sit: 0 });
  const sub = [
    `<g id="e2s12a">${floorIn(1340, '#e9dcc0', '#d9c4a0')}<rect x="60" y="360" width="960" height="420" fill="#2f6b4f" stroke="${OL}" stroke-width="${SW}"/><rect x="40" y="780" width="1000" height="30" fill="#c98a52" stroke="${OL}" stroke-width="6"/>
      <text x="540" y="620" text-anchor="middle" font-family="Luckiest" font-size="150" fill="#f4f4ee" opacity=".9">2 + 2 = 4</text><g>${p.svg}</g><g>${k1.svg}</g></g>`,
    `<g id="e2s12b">${sky() + house(-60, 1200, 1000, '#c9b6e4', { roof: false, door: false, winX: 80, winY: 260 }) + street()}<g>${a.svg}</g><g>${k2.svg}</g>
      <g id="e2sweater" transform="translate(0,140)"><rect x="590" y="1040" width="300" height="230" rx="30" fill="#a4508b" stroke="${OL}" stroke-width="${SW}"/><path d="M600,1110 l40,40 l40,-40 l40,40 l40,-40 l40,40 l40,-40 l40,40" fill="none" stroke="#f5c531" stroke-width="12"/><circle cx="700" cy="1210" r="20" fill="#3fbf6a" stroke="${OL}" stroke-width="5"/><circle cx="780" cy="1210" r="20" fill="#e8453c" stroke="${OL}" stroke-width="5"/></g></g>`,
  ];
  const svg = sub.join('') + bubbleSvg('e2b12a', 'Sua aula é chata.', 500, 50) + bubbleSvg('e2b12b', 'Seu presente é feio.', 560, 50) + tagSvg('e2t12', '+R$50', '#3fbf6a', 120) + cardSvg('e2c12');
  return {
    svg, cam: lt => { const b = lt >= 1.6; const l = b ? lt - 1.6 : lt; return { s: 1.05 + l * .04, fx: 540, fy: 1050, blur: b && l < .08 ? 16 : 0 }; },
    update(lt) {
      const b = lt >= 1.6, l = b ? lt - 1.6 : lt;
      $('e2s12a').setAttribute('display', b ? 'none' : 'inline'); $('e2s12b').setAttribute('display', b ? 'inline' : 'none');
      setChar(p.id, { x: 780, y: 1480, scale: .95, t: lt, mouth: l > .7 ? 'O' : 'smug', eyes: l > .7 ? 'wide' : 'open', brow: l > .7 ? 1 : 0, armR: 120, seed: 19, lookX: -10 });
      setChar(k1.id, { x: 300, y: 1480, scale: .95, t: lt, mouth: 'smug', talk: l < .8, eyes: 'half', seed: 20, lookX: 10 });
      setChar(a.id, { x: 740, y: 1480, scale: .95, t: lt, mouth: l > .7 ? 'O' : 'smile', eyes: l > .7 ? 'wide' : 'happy', armL: 60, armR: 60, seed: 21, lookX: -10 });
      setChar(k2.id, { x: 300, y: 1480, scale: .95, t: lt, mouth: 'smug', talk: l < .8, eyes: 'half', seed: 22, lookX: 10 });
      showBubble('e2b12a', lt, .05, 1.55, 330, 760); showBubble('e2b12b', lt, 1.65, 3.2, 350, 760);
      popTag('e2t12', l, .8, 820, 560, .75);
      card('e2c12', 23.5, lt, 540, 260, .9);
    }
  };
});

// 13. rico e de castigo até o Natal
shot(26.7, 30.0, () => {
  const k = mk('caio', { sit: 1 }), m = mk('mae');
  const svg = floorIn(1340, '#bfe0d2', '#d9c4a0') + door(40, '#c9773f')
    + `<rect x="640" y="380" width="300" height="330" rx="10" fill="#fff" stroke="${OL}" stroke-width="${SW}"/><rect x="640" y="380" width="300" height="80" fill="#e8453c" stroke="${OL}" stroke-width="${SW}"/><text x="790" y="440" text-anchor="middle" font-family="Luckiest" font-size="52" fill="#fff">DEZEMBRO</text>
      ${Array.from({ length: 20 }, (_, i) => `<rect x="${662 + (i % 5) * 52}" y="${478 + Math.floor(i / 5) * 54}" width="40" height="40" fill="${i === 19 ? '#ffd23f' : '#f2f2ee'}" stroke="${OL}" stroke-width="3"/>`).join('')}
      <text x="890" y="696" text-anchor="middle" font-family="Luckiest" font-size="30" fill="#e8453c">25</text>
      <rect x="420" y="1140" width="640" height="220" rx="30" fill="#8f6bd1" stroke="${OL}" stroke-width="${SW}"/><rect x="440" y="1060" width="200" height="110" rx="40" fill="#fff" stroke="${OL}" stroke-width="7"/>`
    + `<g>${m.svg}</g><g>${k.svg}</g>` + bubbleSvg('e2b13', 'CASTIGO!', 360, 64) + cardSvg('e2c13');
  return {
    svg, cam: lt => ({ s: 1.0 + lt * .03, fx: 600, fy: 1050 }),
    update(lt) {
      setChar(m.id, { x: 150, y: 1500, scale: .95, t: lt, mouth: lt > 1.0 && lt < 1.9 ? 'shout' : 'frown', talk: lt > 1.0 && lt < 1.9, brow: -1, mad: 1, armR: 30, armL: 30, seed: 23, lookX: 12 });
      setChar(k.id, { x: 760, y: 1250, scale: .95, t: lt, mouth: lt > 2.2 ? 'smile' : 'smug', eyes: lt > 2.2 ? 'happy' : 'half', armL: 70, armR: 70, seed: 24, lookX: -8 });
      showBubble('e2b13', lt, 1.0, 3.3, 260, 830);
      card('e2c13', 26.7, lt, 700, 260, 1.15, 0, .3);
    }
  };
});
