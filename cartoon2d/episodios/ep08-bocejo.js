// Episódio 8 (estilo 2): "Na minha cidade, cada bocejo custa dois reais."
// Bocejo pega. Na aula de fotossíntese todo mundo boceja e perde dinheiro… menos a professora,
// porque cada bocejo cai na conta dela. "Agora eu sei por que a aula é tão chata."
LINES = [
  [0.3, 2.8, 'Na minha cidade, cada bocejo custa dois reais.'],
  [3.0, 5.0, 'E o pior: bocejo pega.'],
  [5.2, 7.8, 'Eu sou o Caio, e fui pra escola com vinte reais.'],
  [8.0, 10.4, 'Primeira aula: fotossíntese.'],
  [10.6, 12.4, 'O Bruno bocejou.'],
  [12.6, 14.4, 'A Ana bocejou.'],
  [14.6, 17.2, 'Eu segurei… segurei…'],
  [17.4, 19.4, 'E bocejei.'],
  [19.6, 22.2, 'No fim da aula, a sala inteira tava quebrada.'],
  [22.4, 24.8, 'Menos a professora.'],
  [25.0, 27.4, 'Cada bocejo caía na conta dela.'],
  [27.6, 29.8, 'Agora eu sei por que a aula é tão chata.'],
];

const BRUNO = { kid: 1, skin: '#e0a27a', shirt: '#3fae6a', shorts: '#55556e', shoe: '#fff', hair: 'short', hairCol: '#1c1412', pocket: 0, logo: 'B' };
const ANA = { kid: 1, skin: '#c98b62', shirt: '#7fc8a9', dress: '#7fc8a9', shoe: '#e86fa0', hair: 'bun', hairCol: '#3a2418', pocket: 0 };
const KID2 = { kid: 1, skin: '#8a5636', shirt: '#f5c531', shorts: '#3b5bb5', shoe: '#e8453c', hair: 'curly', hairCol: '#1c1412', pocket: 0 };
const PROF = { skin: '#e8b48c', shirt: '#9b6fd1', dress: '#9b6fd1', shoe: '#2b2745', hair: 'bun', hairCol: '#8a8aa0', glasses: 1 };
// altura do balão de saldo acima dos pés (criança / adulto)
const pillY = (y, s, kid = 1) => y - (kid ? 690 : 720) * s;
const fxSvg = (id, txt, col = '#fff', size = 110) => tagSvg(id, txt, col, size);
// bocejo: espreguiça (braços sobem), olhos fechados, boca enorme
const yawn = (lt, t0, d = 1.3) => { const p = K(lt, [[t0, 0], [t0 + .35, 1], [t0 + d - .3, 1], [t0 + d, 0]]); return { p, on: lt > t0 + .1 && lt < t0 + d - .2 }; };
const yawnSt = (y, base) => y.on ? { ...base, mouth: 'yawn', eyes: 'happy', armL: lerp(base.armL ?? 10, 165, y.p), armR: lerp(base.armR ?? 10, 165, y.p), squash: .05 * y.p, tilt: -6 * y.p } : base;

const classroom = (tag) => room2({ wall: '#f6e6b0', floor: '#c98a52' })
  + `<rect x="-200" y="300" width="300" height="360" fill="#cdeeff" stroke="${OL2}" stroke-width="7"/><path d="M-50,300 L-50,660 M-200,480 L100,480" stroke="${OL2}" stroke-width="6"/>`
  + `<rect x="200" y="250" width="700" height="440" rx="10" fill="#2f6b4f" stroke="${OL2}" stroke-width="9"/><rect x="180" y="690" width="740" height="26" fill="#c98a52" stroke="${OL2}" stroke-width="6"/>
     <text id="${tag}board" x="550" y="440" text-anchor="middle" font-family="Luckiest" font-size="74" fill="#f4f4ee" opacity=".95">FOTOSSÍNTESE</text>
     <path d="M300,520 q60,-40 120,0 t120,0 t120,0" fill="none" stroke="#f4f4ee" stroke-width="6" opacity=".8"/><circle cx="780" cy="560" r="40" fill="none" stroke="#f4f4ee" stroke-width="6" opacity=".8"/>`
  + `<g id="${tag}clock" transform="translate(1000,330)"><circle r="62" fill="#fff" stroke="${OL2}" stroke-width="8"/><path class="mh" d="M0,0 L0,-40" stroke="${OL2}" stroke-width="7" stroke-linecap="round"/><path class="hh" d="M0,0 L26,0" stroke="${OL2}" stroke-width="8" stroke-linecap="round"/></g>`
  + `<rect x="960" y="560" width="150" height="190" fill="#e86f6f" stroke="${OL2}" stroke-width="6"/><circle cx="1035" cy="640" r="40" fill="#ffd23f" stroke="${OL2}" stroke-width="5"/>`;
const desk = (x, y, w = 300) => `<rect x="${x - w / 2}" y="${y}" width="${w}" height="34" rx="8" fill="#d6a86a" stroke="${OL2}" stroke-width="7"/><rect x="${x - w / 2 + 14}" y="${y + 34}" width="${w - 28}" height="150" fill="#b88a52" stroke="${OL2}" stroke-width="7"/><rect x="${x - 60}" y="${y - 12}" width="90" height="14" rx="4" fill="#fff" stroke="${OL2}" stroke-width="4"/>`;
const tickClock = (tag, lt, speed = 1) => { const c = $(tag + 'clock'); if (!c) return; c.querySelector('.mh').setAttribute('transform', `rotate(${lt * 40 * speed})`); c.querySelector('.hh').setAttribute('transform', `rotate(${lt * 4 * speed})`); };

// 1. gancho: o moço boceja andando na rua e perde R$ 2
shot(0, 3.0, () => {
  const j = mk('jair');
  const svg = bairro('b1') + `<g>${j.svg}</g>` + pillSvg('p1') + tagSvg('t1', '-R$2', '#e8453c', 90) + fxSvg('fx1', 'AAAH…', '#fff', 100) + titleSvg('ti1', 'CADA BOCEJO', 'CUSTA R$ 2') + coinSvg('k1');
  return {
    svg, cam: lt => ({ s: lerp(2.6, 1.05, easeOut(lt / 1.0)), fx: 540, fy: 1000, blur: lt < .8 ? 22 * (1 - lt / .8) : 0 }),
    update(lt) {
      parallax('b1', lt * 220);
      const y = yawn(lt, .9, 1.6);
      setChar(j.id, yawnSt(y, { x: 540, y: 1560, scale: 1.0, t: lt, mouth: 'flat', eyes: 'half', walk: y.on ? 0 : 1.1, seed: 1 }));
      showPill('p1', lt, .2, 540, pillY(1560, 1, 0) + 20, lt > 1.4 ? 48 : 50, .9, lt > 1.4 ? '#e8453c' : OL2);
      popTag('t1', lt, 1.4, 680, pillY(1560, 1, 0) - 60, .9);
      flyCoin('k1', lt, 1.4, 540, 1200, 1000, 700, .7, 120);
      popTag('fx1', lt, 1.0, 800, 900, 1.2);
      showTitle('ti1', lt, .5, 3.0, 540, 230);
    }
  };
});

// 2. bocejo pega: dominó de bocejos na calçada
shot(3.0, 5.1, () => {
  const ppl = [mk('cida'), mk('n1'), mk('avo', { sit: 0 }), mk('n2')];
  let pills = '', tags = ''; ppl.forEach((_, i) => { pills += pillSvg('p2' + i); tags += tagSvg('t2' + i, '-R$2', '#e8453c', 70); });
  const xs = [150, 400, 660, 920];
  const svg = bairro('b2') + ppl.map(c => `<g>${c.svg}</g>`).join('') + pills + tags;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, .95], [2.1, 1.0]]), fx: K(lt, [[0, 420], [2.1, 640]]), fy: 1150 }),
    update(lt) {
      parallax('b2', 0);
      ppl.forEach((c, i) => {
        const t0 = .15 + i * .42, y = yawn(lt, t0, 1.1);
        setChar(c.id, yawnSt(y, { x: xs[i], y: 1560, scale: .78, t: lt + i, mouth: 'flat', eyes: 'half', seed: 2 + i, lookX: -10 }));
        const lost = lt > t0 + .45;
        showPill('p2' + i, lt, 0, xs[i], pillY(1560, .78, 0), lost ? 18 : 20, .55, lost ? '#e8453c' : OL2);
        popTag('t2' + i, lt, t0 + .45, xs[i] + 40, pillY(1560, .78, 0) - 70, .7);
      });
    }
  };
});

// 3. Caio vai pra escola com R$ 20 (andando, paralaxe)
shot(5.1, 8.0, () => {
  const k = mk('caio');
  const svg = bairro('b3') + `<g>${k.svg}</g>` + pillSvg('p3')
    + `<g id="bag3"><rect x="-70" y="-90" width="140" height="170" rx="30" fill="#3b6fc4" stroke="${OL2}" stroke-width="7"/><rect x="-46" y="-10" width="92" height="56" rx="12" fill="#5f8fe0" stroke="${OL2}" stroke-width="5"/></g>`;
  return {
    svg, cam: lt => ({ s: 1.12, fx: 540, fy: 1200 }),
    update(lt) {
      parallax('b3', 600 + lt * 260);
      setChar(k.id, { x: 540, y: 1580, scale: 1.0, t: lt, mouth: 'smile', talk: lt < 2.4, walk: 1.5, armL: 14, armR: 14, seed: 4 });
      $('bag3').setAttribute('transform', `translate(${540 + 120},${1580 - 300 - Math.abs(Math.cos(lt * 1.5 * Math.PI * 2)) * 10})`);
      showPill('p3', lt, .3, 540, pillY(1580, 1), 20, 1);
    }
  };
});

// 4. a aula de fotossíntese: devagar… (sala inteira)
shot(8.0, 10.5, () => {
  const kids = [mk('caio', { ...BRUNO, sit: 1 }), mk('caio', { ...ANA, sit: 1 }), mk('caio', { sit: 1 }), mk('caio', { ...KID2, sit: 1 })], p = mk('cida', PROF);
  const xs = [170, 410, 670, 910];
  const svg = classroom('c4') + `<g>${p.svg}</g>` + kids.map(k => `<g>${k.svg}</g>`).join('') + xs.map(x => desk(x, 1500, 230)).join('') + fxSvg('fx4', 'zzz', '#8a86a0', 90);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, .92], [2.5, 1.0]]), fx: 540, fy: 1100 }),
    update(lt) {
      tickClock('c4', lt, .3);
      setChar(p.id, { x: 760, y: 1240, scale: .85, t: lt, mouth: 'smug', talk: 1, eyes: 'half', armR: 120, seed: 5 });
      kids.forEach((k, i) => setChar(k.id, { x: xs[i], y: 1560, scale: .72, t: lt + i, mouth: 'flat', eyes: 'half', tilt: Math.sin(lt * 1.3 + i) * 6, seed: 6 + i, lookY: 6 }));
      popTag('fx4', lt, 1.2, 300, 900, 1.2);
    }
  };
});

// 5. o Bruno bocejou (close)  6. a Ana bocejou (close)
for (const [t0, t1, look, name] of [[10.5, 12.5, BRUNO, 'Bruno'], [12.5, 14.5, ANA, 'Ana']]) {
  shot(t0, t1, () => {
    const k = mk('caio', { ...look, sit: 1 }); const tag = 'y' + name;
    const svg = classroom(tag) + `<g>${k.svg}</g>` + desk(540, 1500, 520) + pillSvg(tag + 'p') + tagSvg(tag + 't', '-R$2', '#e8453c', 100) + fxSvg(tag + 'fx', 'AAH!', '#fff', 120) + coinSvg(tag + 'k');
    return {
      svg, cam: lt => ({ s: K(lt, [[0, 1.5], [2, 1.65]]), fx: 540, fy: 1180 }),
      update(lt) {
        tickClock(tag, lt + 5, .3);
        const y = yawn(lt, .25, 1.4);
        setChar(k.id, yawnSt(y, { x: 540, y: 1560, scale: 1.0, t: lt, mouth: 'flat', eyes: 'half', seed: 11 }));
        const lost = lt > .8;
        showPill(tag + 'p', lt, 0, 540, pillY(1560, 1) + 20, lost ? 18 : 20, .8, lost ? '#e8453c' : OL2);
        popTag(tag + 't', lt, .8, 720, pillY(1560, 1) - 40, .9);
        popTag(tag + 'fx', lt, .45, 540, 760, .8);
        flyCoin(tag + 'k', lt, .8, 540, 1250, 1100, 900, .6, 100);
      }
    };
  });
}

// 7. Caio segura o bocejo: bochecha cheia, vermelho, tremendo
shot(14.5, 17.3, () => {
  const k = mk('caio', { sit: 1 });
  const svg = classroom('c7') + `<g>${k.svg}</g>` + desk(540, 1500, 520) + pillSvg('p7');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.6], [2.8, 2.0]]), fx: 540, fy: 1130, tx: lt > 1.4 ? Math.sin(lt * 60) * 4 : 0 }),
    update(lt) {
      tickClock('c7', lt + 9, .3);
      const hold = K(lt, [[.2, 0], [1.2, 1]]);
      setChar(k.id, { x: 540, y: 1560, scale: 1.0, t: lt, mouth: hold > .3 ? 'puff' : 'flat', eyes: hold > .5 ? 'wide' : 'half', brow: hold, red: hold * .55, sweat: hold > .6, tears: lt > 2.0, squash: Math.sin(lt * 40) * .008 * hold, seed: 12 });
      showPill('p7', lt, 0, 540, pillY(1560, 1) + 20, 20, .8);
    }
  };
});

// 8. "E bocejei." — o maior bocejo da história
shot(17.3, 19.5, () => {
  const k = mk('caio', { sit: 1 });
  const svg = classroom('c8') + `<g>${k.svg}</g>` + desk(540, 1500, 520) + pillSvg('p8') + tagSvg('t8', '-R$2', '#e8453c', 110) + fxSvg('fx8', 'AAAH!', '#fff', 120) + coinSvg('k8');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 2.0], [.4, 1.5], [2.2, 1.6]]), fx: 540, fy: 1130, tx: lt > .3 && lt < .6 ? Math.sin(lt * 80) * 8 : 0 }),
    update(lt) {
      tickClock('c8', lt + 12, .3);
      const y = yawn(lt, .1, 1.8);
      setChar(k.id, yawnSt(y, { x: 540, y: 1560, scale: 1.0, t: lt, mouth: 'flat', eyes: 'half', seed: 13 }));
      const lost = lt > .7;
      showPill('p8', lt, 0, 540, pillY(1560, 1) + 20, lost ? 18 : 20, .8, lost ? '#e8453c' : OL2);
      popTag('t8', lt, .7, 730, pillY(1560, 1) - 40, 1.0);
      popTag('fx8', lt, .3, 540, 740, .9);
      flyCoin('k8', lt, .7, 540, 1250, 1100, 900, .6, 100);
    }
  };
});

// 9. fim da aula: a sala inteira quebrada (saldos lá embaixo)
shot(19.5, 22.3, () => {
  const kids = [mk('caio', { ...BRUNO, sit: 1 }), mk('caio', { ...ANA, sit: 1 }), mk('caio', { sit: 1 }), mk('caio', { ...KID2, sit: 1 })];
  const xs = [170, 410, 670, 910], vals = [2, 0, 4, 2];
  let pills = ''; xs.forEach((_, i) => pills += pillSvg('p9' + i));
  const svg = classroom('c9') + kids.map(k => `<g>${k.svg}</g>`).join('') + xs.map(x => desk(x, 1500, 230)).join('') + pills;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, .95], [2.8, 1.02]]), fx: K(lt, [[0, 440], [2.8, 640]]), fy: 1150 }),
    update(lt) {
      tickClock('c9', lt + 20, 3);
      kids.forEach((k, i) => setChar(k.id, { x: xs[i], y: 1560, scale: .72, t: lt + i, mouth: i === 2 ? 'frown' : 'flat', eyes: 'half', tears: i === 1, tilt: -10 + i * 4, seed: 14 + i, lookY: 8 }));
      xs.forEach((x, i) => showPill('p9' + i, lt, .2 + i * .15, x, pillY(1560, .72), vals[i], .55, '#e8453c'));
    }
  };
});

// 10. "Menos a professora." — saldo dela subindo
shot(22.3, 24.9, () => {
  const p = mk('cida', PROF);
  const svg = classroom('c10') + `<g>${p.svg}</g>` + pillSvg('p10') + [0, 1, 2].map(i => `<g id="sp10${i}">${sparkle(300 + i * 240, 700 + (i % 2) * 120, 1)}</g>`).join('');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.25], [2.6, 1.4]]), fx: 560, fy: 1150 }),
    update(lt) {
      tickClock('c10', lt + 30, .3);
      setChar(p.id, { x: 560, y: 1560, scale: 1.0, t: lt, mouth: lt > 1 ? 'smile' : 'smug', eyes: lt > 1.6 ? 'money' : 'half', brow: -.3, armL: 40, seed: 18 });
      const v = Math.round(K(lt, [[.3, 20], [2.2, 312]]));
      showPill('p10', lt, .2, 560, pillY(1560, 1, 0) + 10, v, 1.0, '#2fae60');
      for (let i = 0; i < 3; i++) $('sp10' + i).setAttribute('opacity', lt > 1 ? Math.abs(Math.sin(lt * 5 + i)) : 0);
    }
  };
});

// 11. cada bocejo caía na conta dela (moedas voando dos alunos até a bolsa)
shot(24.9, 27.5, () => {
  const p = mk('cida', PROF), kids = [mk('caio', { ...BRUNO, sit: 1 }), mk('caio', { sit: 1 })];
  let coins = ''; for (let i = 0; i < 8; i++) coins += coinSvg('k11' + i);
  const svg = classroom('c11') + `<g>${p.svg}</g>` + kids.map(k => `<g>${k.svg}</g>`).join('') + desk(180, 1500, 230) + desk(420, 1500, 230)
    + `<g id="purse"><path d="M-80,-60 L80,-60 L100,70 L-100,70 Z" fill="#e8453c" stroke="${OL2}" stroke-width="7"/><path d="M-50,-60 Q0,-130 50,-60" fill="none" stroke="${OL2}" stroke-width="9"/><circle cx="0" cy="-30" r="10" fill="#f5c531" stroke="${OL2}" stroke-width="4"/></g>` + coins + bigNum('num11', 'R$ 312', 130, '#3fbf6a');
  return {
    svg, cam: lt => ({ s: 1.0, fx: 540, fy: 1100 }),
    update(lt) {
      tickClock('c11', lt + 40, .3);
      setChar(p.id, { x: 820, y: 1500, scale: .9, t: lt, mouth: 'smile', eyes: 'happy', armL: 60, seed: 19 });
      $('purse').setAttribute('transform', `translate(700,1220) scale(${1 + Math.sin(lt * 8) * .03})`);
      kids.forEach((k, i) => { const y = yawn(lt, .2 + i * .9, 1.1); setChar(k.id, yawnSt(y, { x: [180, 420][i], y: 1560, scale: .72, t: lt + i, mouth: 'flat', eyes: 'half', seed: 20 + i })); });
      for (let i = 0; i < 8; i++) flyCoin('k11' + i, lt, .3 + i * .28, [180, 420][i % 2], 1200, 700, 1200, .55, 180);
      showPop('num11', lt, .2, 540, 880, 1, 'R$ ' + Math.round(K(lt, [[0, 312], [2.6, 326]])));
    }
  };
});

// 12. a professora pisca pra câmera: "Fotossíntese – parte 2"
shot(27.5, 30.0, () => {
  const p = mk('cida', PROF), k = mk('caio', { sit: 1 });
  const svg = classroom('c12') + `<g>${p.svg}</g><g>${k.svg}</g>` + desk(320, 1500, 360) + pillSvg('p12a') + pillSvg('p12b');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.5, 1.15]]), fx: 560, fy: 1150 }),
    update(lt) {
      tickClock('c12', lt + 50, .3);
      $('c12board').textContent = lt > .8 ? 'PARTE 2' : 'FOTOSSÍNTESE';
      const wink = lt > 1.4 && lt < 1.8;
      setChar(p.id, { x: 800, y: 1480, scale: .95, t: lt, mouth: 'smug', eyes: wink ? 'happy' : 'half', brow: -.4, armR: lt > .5 ? 140 : 30, seed: 23, lookX: -6 });
      setChar(k.id, { x: 320, y: 1560, scale: .9, t: lt, mouth: 'flat', eyes: 'half', seed: 24, lookX: 12 });
      showPill('p12a', lt, .1, 800, pillY(1480, .95, 0) + 10, 326, .75, '#2fae60');
      showPill('p12b', lt, .1, 320, pillY(1560, .9) + 10, 4, .7, '#e8453c');
    }
  };
});
