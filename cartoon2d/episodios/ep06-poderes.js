// Episódio 6: "Na minha cidade, todo mundo tem um poder." (45s)
// Final do campeonato (prêmio R$ 500): Caio, de borracha, contra o zagueiro Muralha, que vira metal.
// Luta, estilingue humano, gol de cabeça… e a borracha volta: gol contra, metade do prêmio.
DUR = 45;
LINES = [
  [0.3, 3.3, 'Na minha cidade, todo mundo tem um poder.'],
  [3.5, 6.1, 'O meu? Eu sou de borracha.'],
  [6.3, 9.3, 'Hoje é a final do campeonato. Prêmio: quinhentos reais.'],
  [9.5, 12.3, 'Só que o zagueiro deles é o Muralha.'],
  [12.5, 15.3, 'O poder dele? Ele vira metal.'],
  [15.5, 17.9, 'Eu estiquei a perna e chutei com tudo.'],
  [18.1, 20.3, 'A bola bateu nele… e voltou na minha cara.'],
  [20.5, 22.9, 'Ele veio pra cima de mim.'],
  [23.1, 25.5, 'Ele socou. Eu virei elástico.'],
  [25.7, 28.3, 'Aí eu tive uma ideia: estilingue!'],
  [28.5, 31.1, 'Me estiquei pra trás… e me soltei!'],
  [31.3, 33.9, 'Passei voando por cima do Muralha…'],
  [34.1, 36.7, 'E fiz o gol de cabeça!'],
  [36.9, 39.5, 'Gol! Quinhentos reais!'],
  [39.7, 41.9, 'Só que borracha… sempre volta.'],
  [42.1, 44.8, 'Gol contra. Metade do prêmio.'],
];

const MURALHA = { skin: '#c98b62', shirt: '#3b5bb5', stripe: '#2f4a99', shorts: '#f4f4f0', shoe: '#2b2745', hair: 'short', hairCol: '#1c1412', belly: 1 };
const METAL = { skin: '#a9b0bf', shirt: '#8a92a6', stripe: '#c3c9d6', shorts: '#9aa3b5', shoe: '#6f778a', sole: '#c3c9d6', hair: 'short', hairCol: '#7f8799', belly: 1, noCheeks: 1 };
const SALDO = t => t < 37.2 ? 0 : t < 38.4 ? Math.round(500 * easeOut((t - 37.2) / 1.2)) : t < 43.6 ? 500 : Math.round(500 - 250 * easeOut((t - 43.6) / .6));
const card = (id, t0, lt, x, y, s, shake = 0, from = 0) => { const v = SALDO(t0 + lt); showCard(id, lt, from, x, y, v, t0 + lt < 43.4 ? '#2fae60' : '#e8453c', s, shake); };

// ------------------------------------------------------------------ campo, gol, bola, efeitos
let crowd = ''; { const cols = ['#e8453c', '#f28c38', '#ffd23f', '#3b5bb5', '#3fae6a', '#e86fa0', '#fff']; for (let r = 0; r < 5; r++) for (let c = 0; c < 16; c++) crowd += `<circle cx="${20 + c * 68 + (r % 2) * 34}" cy="${430 + r * 90}" r="26" fill="${cols[(r * 7 + c * 3) % 7]}" stroke="${OL}" stroke-width="4"/>`; }
const field = (crowdId = '') => `<rect x="-200" y="-200" width="1480" height="700" fill="#9fd0ea"/>
  <rect x="-200" y="360" width="1480" height="560" fill="#7a7f99" stroke="${OL}" stroke-width="${SW}"/>${[0, 1, 2, 3, 4].map(r => `<rect x="-200" y="${400 + r * 90}" width="1480" height="14" fill="#62677f"/>`).join('')}
  <g ${crowdId ? `id="${crowdId}"` : ''}>${crowd}</g><rect x="-200" y="880" width="1480" height="50" fill="#e8453c" stroke="${OL}" stroke-width="6"/>
  ${[0, 1, 2, 3, 4, 5].map(i => `<text x="${80 + i * 200}" y="918" font-family="Luckiest" font-size="34" fill="#fff">GOL!</text>`).join('')}
  <rect x="-200" y="930" width="1480" height="1200" fill="#5fae4f"/>${[0, 1, 2, 3, 4].map(i => `<rect x="-200" y="${930 + i * 200}" width="1480" height="100" fill="#6dbd5b"/>`).join('')}
  <path d="M-200,1010 L1280,1010" stroke="#fff" stroke-width="10" opacity=".9"/><ellipse cx="540" cy="1500" rx="380" ry="110" fill="none" stroke="#fff" stroke-width="10" opacity=".9"/>`;
const goalSvg = (id, x, y, s = 1) => `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><g class="net">${Array.from({ length: 9 }, (_, i) => `<path d="M${-260 + i * 65},-360 L${-230 + i * 58},0" stroke="#fff" stroke-width="4" opacity=".75"/>`).join('')}${Array.from({ length: 6 }, (_, i) => `<path d="M-260,${-360 + i * 64} L260,${-360 + i * 64}" stroke="#fff" stroke-width="4" opacity=".75"/>`).join('')}</g>
  <rect x="-284" y="-380" width="24" height="380" fill="#fff" stroke="${OL}" stroke-width="6"/><rect x="260" y="-380" width="24" height="380" fill="#fff" stroke="${OL}" stroke-width="6"/><rect x="-284" y="-392" width="568" height="24" fill="#fff" stroke="${OL}" stroke-width="6"/></g>`;
const ballSvg = id => `<g id="${id}"><circle r="42" fill="#fff" stroke="${OL}" stroke-width="7"/><path d="M0,-16 L15,-5 L9,13 L-9,13 L-15,-5 Z" fill="${OL}"/>${[0, 72, 144, 216, 288].map(a => `<path d="M0,-16 L0,-38" stroke="${OL}" stroke-width="5" transform="rotate(${a})"/><path d="M-10,-40 L10,-40 L6,-32 L-6,-32 Z" fill="${OL}" transform="rotate(${a})"/>`).join('')}</g>`;
const setBall = (id, x, y, rot = 0, s = 1) => $(id).setAttribute('transform', `translate(${x},${y}) rotate(${rot}) scale(${s})`);
const fx = (id, txt, col, size = 120) => tagSvg(id, txt, col, size);
const flashSvg = id => `<rect id="${id}" x="-300" y="-300" width="1680" height="2520" fill="#fff" opacity="0"/>`;
const flash = (id, lt, t0, d = .12) => $(id).setAttribute('opacity', lt >= t0 && lt < t0 + d ? .85 * (1 - (lt - t0) / d) : 0);
const speedLines = id => `<g id="${id}" opacity="0">${Array.from({ length: 18 }, (_, i) => `<rect x="${-200 + (i * 173) % 1400}" y="${150 + (i * 97) % 1500}" width="${220 + (i % 4) * 80}" height="10" rx="5" fill="#fff"/>`).join('')}</g>`;
const scoreBoard = id => `<g id="${id}"><rect x="-300" y="-55" width="600" height="110" rx="24" fill="#2b2745" stroke="#fff" stroke-width="6"/><text class="sc" y="22" text-anchor="middle" font-family="Luckiest" font-size="58" fill="#ffd23f">LARANJA 0 x 0 AZUL</text></g>`;
const setScore = (id, x, y, txt, s = 1) => { $(id).setAttribute('transform', `translate(${x},${y}) scale(${s})`); $(id).querySelector('.sc').textContent = txt; };
const stars = id => `<g id="${id}" display="none">${[0, 1, 2, 3].map(i => `<g class="st">${sparkle(0, 0, .8, '#ffd23f')}</g>`).join('')}</g>`;
function spinStars(id, lt, on, x, y) { const el = $(id); el.setAttribute('display', on ? 'inline' : 'none'); if (!on) return; el.querySelectorAll('.st').forEach((s, i) => { const a = lt * 6 + i * 1.57; s.setAttribute('transform', `translate(${x + Math.cos(a) * 120},${y + Math.sin(a) * 30})`); }); }
const puffs = id => `<g id="${id}">${[0, 1, 2, 3, 4].map(i => `<circle class="pu" r="40" fill="#e8dcc0" stroke="${OL}" stroke-width="5"/>`).join('')}</g>`;
function stompPuffs(id, lt, t0, x, y) { $(id).querySelectorAll('.pu').forEach((c, i) => { const p = (lt - t0) / .6; if (p < 0 || p > 1) { c.setAttribute('display', 'none'); return; } c.setAttribute('display', 'inline'); c.setAttribute('cx', x + (i - 2) * 50 * (1 + p)); c.setAttribute('cy', y - p * 40); c.setAttribute('r', 30 + p * 30); c.setAttribute('opacity', 1 - p); }); }
// Muralha normal + versão de metal por cima, revelada de baixo para cima (clipPath)
function muralha(tag) {
  const m = mk('caio', { ...MURALHA, kid: 0, pocket: 0 }), mt = mk('caio', { ...METAL, kid: 0, pocket: 0 });
  const svg = `<g>${m.svg}</g><clipPath id="${tag}clip"><rect id="${tag}cr" x="-400" y="0" width="1880" height="0"/></clipPath><g clip-path="url(#${tag}clip)"><g>${mt.svg}</g></g><rect id="${tag}edge" x="-400" y="0" width="1880" height="14" rx="7" fill="#fff" opacity="0"/>`;
  return { svg, set(st, metal = 0, lt = 0) { setChar(m.id, st); setChar(mt.id, { ...st, mad: 0 }); const top = st.y - 640 * (st.scale || 1); const h = (st.y + 20 - top) * metal; $(tag + 'cr').setAttribute('y', st.y + 20 - h); $(tag + 'cr').setAttribute('height', h); const e = $(tag + 'edge'); e.setAttribute('x', st.x - 170 * (st.scale || 1)); e.setAttribute('width', 340 * (st.scale || 1)); e.setAttribute('y', st.y + 13 - h); e.setAttribute('opacity', metal > .02 && metal < .98 ? .9 : 0); } };
}

// 1. gancho: a bola cai e o braço do Caio estica pela tela inteira (BOING!)
shot(0, 3.5, () => {
  const k = mk('caio');
  const svg = field() + `<g>${k.svg}</g>` + ballSvg('e6b1') + fx('e6fx1', 'BOING!', '#ffd23f', 140) + speedLines('e6sl1');
  return {
    svg, cam: lt => ({ s: lerp(2.4, 1.0, easeOut(lt / 1.1)), fx: 760, fy: 700, blur: lt < .8 ? 24 * (1 - lt / .8) : 0 }),
    update(lt) {
      const reach = K(lt, [[0, 0], [.35, 1], [1.4, 1], [1.9, 0]]);
      const wob = lt > 1.9 ? Math.sin((lt - 1.9) * 25) * Math.exp(-(lt - 1.9) * 4) * .3 : 0;
      setChar(k.id, { x: 300, y: 1560, scale: 1.0, t: lt, mouth: 'smile', eyes: lt < 1.9 ? 'wide' : 'happy', brow: .8, armL: lerp(20, 140, reach), armLlen: 1 + reach * 3.6 + wob, seed: 1, lookX: 10, lookY: -10 });
      const by = K(lt, [[0, -100], [.35, 520], [1.4, 520], [1.9, 1060]]); const bx = K(lt, [[0, 820], [.35, 820], [1.4, 820], [1.9, 470]]);
      setBall('e6b1', bx, by, lt * 400);
      popTag('e6fx1', lt, .35, 760, 380, 1.2);
      $('e6sl1').setAttribute('opacity', lt < .4 ? .6 : 0);
    }
  };
});

// 2. "Eu sou de borracha": braço estica e volta tremendo
shot(3.5, 6.3, () => {
  const k = mk('caio');
  const svg = field() + `<g>${k.svg}</g>` + fx('e6fx2', 'BOING!', '#ffd23f', 130);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.45], [2.8, 1.6]]), fx: 540, fy: 1150 }),
    update(lt) {
      const pull = K(lt, [[.4, 0], [1.0, 1], [1.2, 1]]);
      const wob = lt > 1.2 ? Math.sin((lt - 1.2) * 28) * Math.exp(-(lt - 1.2) * 3.5) : 0;
      setChar(k.id, { x: 540, y: 1560, scale: 1.05, t: lt, mouth: 'smile', talk: lt < 2.4, eyes: lt > 1.3 ? 'happy' : 'open', armL: 90, armLlen: lt < 1.2 ? 1 + pull * 1.6 : 1 + wob * .6, armR: 15, squash: wob * .04, seed: 2 });
      popTag('e6fx2', lt, 1.2, 800, 860, 1.0);
    }
  };
});

// 3. a final: placar 0x0, troféu e prêmio R$ 500
shot(6.3, 9.5, () => {
  const k = mk('caio'), a = mk('n1'), b = mk('n2');
  const trophy = `<g id="e6tro"><path d="M-80,-220 L80,-220 Q80,-90 0,-75 Q-80,-90 -80,-220 Z" fill="#ffd23f" stroke="${OL}" stroke-width="8"/><path d="M-80,-200 q-60,0 -45,55 q12,30 45,30 M80,-200 q60,0 45,55 q-12,30 -45,30" fill="none" stroke="${OL}" stroke-width="8"/><rect x="-16" y="-78" width="32" height="44" fill="#ffd23f" stroke="${OL}" stroke-width="7"/><rect x="-60" y="-36" width="120" height="36" rx="8" fill="#c98a52" stroke="${OL}" stroke-width="7"/></g>`;
  const svg = field('e6crowd3') + `<g>${a.svg}</g><g>${b.svg}</g><g>${k.svg}</g>` + trophy + scoreBoard('e6sc3')
    + `<g id="e6prize"><rect x="-240" y="-75" width="480" height="150" rx="30" fill="#ffd23f" stroke="${OL}" stroke-width="9"/><text y="-12" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="36" fill="${OL}">PRÊMIO</text><text y="58" text-anchor="middle" font-family="Luckiest" font-size="72" fill="#2fae60">R$ 500</text></g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [3.2, 1.08]]), fx: 540, fy: 1000 }),
    update(lt) {
      $('e6crowd3').setAttribute('transform', `translate(0,${-Math.abs(Math.sin(lt * 8)) * 12})`);
      setChar(a.id, { x: 160, y: 1600, scale: .8, t: lt, mouth: 'smile', armL: 30, seed: 3 });
      setChar(b.id, { x: 920, y: 1600, scale: .8, t: lt, mouth: 'smile', armR: 30, seed: 4 });
      setChar(k.id, { x: 540, y: 1640, scale: .95, t: lt, mouth: 'smile', eyes: 'money', armL: 150, armR: 150, hop: lt > 1.6 ? 2.5 : 0, seed: 5 });
      setScore('e6sc3', 540, 140, 'LARANJA 0 x 0 AZUL');
      $('e6tro').setAttribute('transform', `translate(540,${1050}) scale(${backOut((lt - .5) / .35) * 1.1}) rotate(${Math.sin(lt * 3) * 3})`);
      $('e6prize').setAttribute('transform', `translate(540,330) scale(${backOut((lt - 1.4) / .35)})`);
    }
  };
});

// 4. entra o Muralha: o chão treme a cada passo
shot(9.5, 12.5, () => {
  const k = mk('caio'), M = muralha('e6m4');
  const svg = field() + `<g>${k.svg}</g>` + M.svg + puffs('e6pu4');
  const steps = [.3, .8, 1.3, 1.8];
  return {
    svg, cam: lt => { const st = steps.find(s => lt >= s && lt < s + .15); return { s: K(lt, [[0, 1.0], [3, 1.1]]), fx: 700, fy: 1100, tx: st !== undefined ? Math.sin(lt * 90) * 14 : 0 }; },
    update(lt) {
      const x = K(lt, [[0, 1250], [2.0, 760]]);
      M.set({ x, y: 1600, scale: 1.25, t: lt, mouth: 'smug', eyes: 'half', brow: -1, armL: 25, armR: 25, walk: lt < 2 ? 1.0 : 0, seed: 6, lookX: -12 }, 0, lt);
      for (const s of steps) if (lt >= s && lt < s + .6) stompPuffs('e6pu4', lt, s, x, 1600);
      setChar(k.id, { x: 250, y: 1600, scale: .9, t: lt, mouth: lt > 1 ? 'o' : 'smile', eyes: lt > 1 ? 'wide' : 'open', brow: lt > 1 ? .9 : 0, sweat: lt > 1.4, seed: 7, lookX: 12, squash: lt > 2.2 && lt < 2.5 ? -.04 : 0 });
    }
  };
});

// 5. a transformação em metal (CLANK!)
shot(12.5, 15.5, () => {
  const M = muralha('e6m5');
  let sp = ''; for (let i = 0; i < 8; i++) sp += `<g class="e6sp">${sparkle(0, 0, .9, '#ffffff')}</g>`;
  const svg = field() + `<circle id="e6halo" cx="540" cy="1100" r="420" fill="#c3c9d6" opacity="0"/>` + M.svg + `<g id="e6sps">${sp}</g>` + fx('e6fx5', 'CLANK!', '#c3c9d6', 150) + flashSvg('e6fl5');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.3], [1.2, 1.15], [3, 1.2]]), fx: 540, fy: 1100, tx: lt > 1.6 && lt < 1.9 ? Math.sin(lt * 80) * 12 : 0 }),
    update(lt) {
      const met = K(lt, [[.4, 0], [1.6, 1]]);
      M.set({ x: 540, y: 1640, scale: 1.4, t: lt, mouth: lt > 1.6 ? 'smug' : 'flat', eyes: lt > 1.6 ? 'half' : 'open', brow: -1, armL: K(lt, [[0, 20], [.4, 150]]), armR: K(lt, [[0, 20], [.4, 150]]), squash: lt > .4 && lt < 1.6 ? Math.sin(lt * 40) * .01 : 0, seed: 8 }, met, lt);
      $('e6halo').setAttribute('opacity', met * .35 * (1 + Math.sin(lt * 10) * .2));
      document.querySelectorAll('.e6sp').forEach((s, i) => { const p = ((lt * .9 + i / 8) % 1); s.setAttribute('transform', `translate(${540 + Math.cos(i * .8) * (200 + p * 260)},${1150 + Math.sin(i * 1.3) * (300 + p * 200)}) scale(${(1 - p) * 1.2})`); s.setAttribute('opacity', met > .2 ? 1 - p : 0); });
      popTag('e6fx5', lt, 1.6, 540, 520, 1.3); flash('e6fl5', lt, 1.6);
    }
  };
});

// 6. Caio estica a perna e chuta com tudo
shot(15.5, 18.1, () => {
  const k = mk('caio'), M = muralha('e6m6');
  const svg = field() + M.svg + `<g>${k.svg}</g>` + ballSvg('e6b6') + speedLines('e6sl6');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.6, 1.1]]), fx: 540, fy: 1150 }),
    update(lt) {
      M.set({ x: 860, y: 1560, scale: 1.1, t: lt, mouth: 'smug', eyes: 'half', brow: -1, armL: 30, armR: 30, seed: 9, lookX: -10 }, 1, lt);
      const wind = K(lt, [[0, 0], [.7, -1], [1.0, 1], [1.6, 1], [2.2, 0]]);
      setChar(k.id, { x: 240, y: 1600, scale: 1.0, t: lt, mouth: 'shout', brow: -1, mad: 1, armL: 40, armR: 70, legL: wind < 0 ? -wind * 25 : wind * 80, legLlen: 1 + Math.max(0, wind) * 1.8, lean: -wind * 8, seed: 10 });
      const p = clamp((lt - 1.0) / .5);
      setBall('e6b6', lt < 1.0 ? 330 : lerp(520, 760, p), lt < 1.0 ? 1560 : lerp(1500, 1180, p), lt * 700, 1 + p * .3);
      $('e6sl6').setAttribute('opacity', lt > 1 && lt < 1.6 ? .6 : 0);
    }
  };
});

// 7. CLANG! a bola volta na cara do Caio (estrelinhas)
shot(18.1, 20.5, () => {
  const k = mk('caio'), M = muralha('e6m7');
  const svg = field() + M.svg + `<g>${k.svg}</g>` + ballSvg('e6b7') + fx('e6fx7', 'CLANG!', '#c3c9d6', 140) + fx('e6fx7b', 'PLOFT!', '#e8453c', 110) + stars('e6st7') + flashSvg('e6fl7');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [.9, 1.05], [1.3, 1.6]]), fx: K(lt, [[0, 600], [1.3, 260]]), fy: K(lt, [[0, 1100], [1.3, 1100]]), tx: lt > .25 && lt < .45 ? Math.sin(lt * 90) * 12 : 0 }),
    update(lt) {
      M.set({ x: 860, y: 1560, scale: 1.1, t: lt, mouth: 'smug', eyes: 'half', brow: -1, armL: 30, armR: 30, seed: 11, lookX: -10 }, 1, lt);
      const hit = lt > 1.0;
      setChar(k.id, { x: 260, y: 1600, scale: 1.0, t: lt, mouth: hit ? 'O' : 'smile', eyes: hit ? 'wide' : 'open', brow: hit ? 1 : 0, squash: hit && lt < 1.3 ? -.12 : 0, tilt: hit ? Math.sin(lt * 12) * 8 : 0, seed: 12 });
      const bx = lt < .3 ? lerp(700, 760, lt / .3) : lerp(760, 260, clamp((lt - .3) / .7)), by = lt < .3 ? 1180 : lerp(1180, 1050, clamp((lt - .3) / .7));
      setBall('e6b7', lt < 1.0 ? bx : 260 + (lt - 1) * 200, lt < 1.0 ? by : 1050 + (lt - 1) * (lt - 1) * 900, lt * 600);
      popTag('e6fx7', lt, .3, 760, 860, 1.0); popTag('e6fx7b', lt, 1.0, 380, 820, .9);
      flash('e6fl7', lt, .3); spinStars('e6st7', lt, lt > 1.1, 260, 900);
    }
  };
});

// 8. o Muralha avança; o Caio estica o corpo pra desviar
shot(20.5, 23.1, () => {
  const k = mk('caio'), M = muralha('e6m8');
  const svg = field() + `<g>${k.svg}</g>` + M.svg + puffs('e6pu8') + speedLines('e6sl8');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.6, 1.08]]), fx: 540, fy: 1150 }),
    update(lt) {
      const mx = K(lt, [[0, 950], [1.4, 600]]);
      M.set({ x: mx, y: 1600, scale: 1.2, t: lt, mouth: 'shout', brow: -1, mad: 1, armL: 60, armR: 60, walk: lt < 1.4 ? 2.2 : 0, lean: -8, seed: 13 }, 1, lt);
      stompPuffs('e6pu8', lt, (Math.floor(lt / .45)) * .45, mx, 1600);
      const dodge = K(lt, [[1.0, 0], [1.4, 1], [2.2, 1], [2.6, 0]]);
      setChar(k.id, { x: 330 - dodge * 50, y: 1600, scale: 1.0, t: lt, mouth: 'O', eyes: 'wide', brow: 1, squash: dodge * .35, lean: -dodge * 14, armL: 150, armR: 150, armLlen: 1 + dodge * .6, armRlen: 1 + dodge * .6, seed: 14 });
      $('e6sl8').setAttribute('opacity', lt < 1.4 ? .5 : 0);
    }
  };
});

// 9. o soco de metal: o Caio vira elástico (BOING!)
shot(23.1, 25.7, () => {
  const k = mk('caio'), M = muralha('e6m9');
  const svg = field() + `<g>${k.svg}</g>` + M.svg + fx('e6fx9', 'BOING!', '#ffd23f', 140) + flashSvg('e6fl9');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.15], [2.6, 1.22]]), fx: 540, fy: 1150, tx: lt > .7 && lt < .9 ? Math.sin(lt * 90) * 14 : 0 }),
    update(lt) {
      const punch = K(lt, [[.3, 0], [.7, 1], [1.4, 1], [1.8, 0]]);
      M.set({ x: 760, y: 1600, scale: 1.2, t: lt, mouth: 'shout', brow: -1, mad: 1, armR: lerp(30, 90, punch), armRlen: 1 + punch * 1.3, armL: 30, lean: -punch * 6, seed: 15 }, 1, lt);
      const dent = lt > .7 ? Math.sin((lt - .7) * 18) * Math.exp(-(lt - .7) * 2.5) : 0;
      setChar(k.id, { x: 330, y: 1600, scale: 1.0, t: lt, mouth: lt > .7 ? 'smile' : 'O', eyes: lt > 1.2 ? 'happy' : 'wide', brow: .8, lean: -30 * Math.max(0, dent) - punch * 10, squash: dent * .2, armL: 150, armR: 150, seed: 16 });
      popTag('e6fx9', lt, .7, 330, 760, 1.2); flash('e6fl9', lt, .7, .08);
    }
  };
});

// 10. a ideia: estilingue! (lâmpada) — agarra as traves do próprio gol
shot(25.7, 28.5, () => {
  const k = mk('caio');
  const svg = field() + goalSvg('e6g10', 540, 1460, 1.3) + `<g>${k.svg}</g>`
    + `<g id="e6bulb"><circle r="60" fill="#ffe27a" stroke="${OL}" stroke-width="7"/><rect x="-26" y="50" width="52" height="40" rx="8" fill="#a9b0bf" stroke="${OL}" stroke-width="6"/>${[0, 1, 2, 3, 4, 5].map(i => `<path d="M0,-80 L0,-120" stroke="#ffd23f" stroke-width="10" stroke-linecap="round" transform="rotate(${-75 + i * 30})"/>`).join('')}</g>`;
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.8, 1.08]]), fx: 540, fy: 1150 }),
    update(lt) {
      $('e6bulb').setAttribute('transform', `translate(540,${760 + Math.sin(lt * 4) * 8}) scale(${backOut((lt - .2) / .3)})`);
      const grab = K(lt, [[1.0, 0], [1.6, 1]]);
      setChar(k.id, { x: 540, y: 1660, scale: 1.0, t: lt, mouth: 'smile', talk: lt < 1.0, eyes: lt < 1 ? 'wide' : 'open', brow: .8, armL: lerp(40, 112, grab), armR: lerp(40, 112, grab), armLlen: 1 + grab * 1.35, armRlen: 1 + grab * 1.35, seed: 17 });
    }
  };
});

// 11. estica pra trás… e solta! (ESTILINGUE!)
shot(28.5, 31.3, () => {
  const k = mk('caio');
  const svg = field() + goalSvg('e6g11', 540, 1300, 1.3) + `<g id="e6w11">${k.svg}</g>` + fx('e6fx11', 'ESTILINGUE!', '#ffd23f', 120) + speedLines('e6sl11');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [1.8, 1.12], [2.0, .95]]), fx: 540, fy: 1100, tx: lt > 1.5 && lt < 1.8 ? Math.sin(lt * 70) * 6 : 0 }),
    update(lt) {
      const pull = K(lt, [[0, 0], [1.7, 1]]);
      const rel = lt > 1.8 ? easeOut((lt - 1.8) / .5) : 0;
      $('e6w11').setAttribute('transform', `translate(0,${rel * -1400})`);
      setChar(k.id, { x: 540, y: 1520 + pull * 260 * (1 - rel), scale: 1.0 - pull * .1, t: lt, mouth: pull > .5 ? 'shout' : 'smile', eyes: 'open', brow: -1, mad: pull > .6, armL: 150 - pull * 15, armR: 150 - pull * 15, armLlen: (1.4 + pull * 1.6) * (1 - rel * .5), armRlen: (1.4 + pull * 1.6) * (1 - rel * .5), squash: pull * .15 * (1 - rel), seed: 18 });
      popTag('e6fx11', lt, 1.8, 540, 640, 1.0);
      $('e6sl11').setAttribute('opacity', rel > 0 ? .7 : 0); $('e6sl11').setAttribute('transform', 'rotate(90,540,960)');
    }
  };
});

// 12. voando por cima do Muralha (câmera lenta)
shot(31.3, 34.1, () => {
  const k = mk('caio'), M = muralha('e6m12');
  const svg = field() + M.svg + `<g id="e6w12">${k.svg}</g>` + ballSvg('e6b12') + speedLines('e6sl12');
  return {
    svg, cam: lt => ({ s: 1.05, fx: 540, fy: 1100 }),
    update(lt) {
      M.set({ x: 600, y: 1640, scale: 1.25, t: lt, mouth: 'O', eyes: 'wide', brow: 1, armL: 60, armR: 60, seed: 19, lookY: -12, lookX: K(lt, [[0, -10], [2.8, 12]]) }, 1, lt);
      const p = lt / 2.8, x = lerp(-200, 1300, p), y = 760 - Math.sin(p * Math.PI) * 160;
      $('e6w12').setAttribute('transform', `translate(${x},${y}) rotate(80)`);
      setChar(k.id, { x: 0, y: 0, scale: .9, t: lt, mouth: 'smile', eyes: 'happy', armL: 175, armR: 175, armLlen: 1.4, armRlen: 1.4, seed: 20 });
      setBall('e6b12', x + 260, y - 30, lt * 500, .9);
      $('e6sl12').setAttribute('opacity', .55); $('e6sl12').setAttribute('transform', `translate(${-(lt * 900) % 400},0)`);
    }
  };
});

// 13. gol de cabeça: a rede estufa, GOOOL!
shot(34.1, 36.9, () => {
  const k = mk('caio'), g = mk('n1');
  const svg = field('e6crowd13') + goalSvg('e6g13', 540, 1400, 1.5) + `<g>${g.svg}</g><g id="e6w13">${k.svg}</g>` + ballSvg('e6b13') + bigNum('e6gol', 'GOOOL!', 210, '#ffd23f') + flashSvg('e6fl13');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [.6, 1.0], [.8, 1.12], [2.8, 1.18]]), fx: 540, fy: 1100, tx: lt > .6 && lt < .9 ? Math.sin(lt * 90) * 10 : 0 }),
    update(lt) {
      const head = lt > .55;
      $('e6w13').setAttribute('transform', `translate(${K(lt, [[0, -300], [.55, 400], [1.2, 540]])},${K(lt, [[0, 780], [.55, 900], [1.2, 1380]])}) rotate(${K(lt, [[0, 80], [1.2, 0]])})`);
      setChar(k.id, { x: 0, y: 0, scale: .95, t: lt, mouth: 'smile', eyes: head ? 'happy' : 'open', armL: head ? 160 : 175, armR: head ? 160 : 175, hop: lt > 1.3 ? 2.5 : 0, seed: 21 });
      setChar(g.id, { x: K(lt, [[0, 560], [.7, 820]]), y: 1440, scale: .9, t: lt, mouth: 'O', eyes: 'wide', brow: 1, lean: K(lt, [[.4, 0], [.8, 40]]), armL: 150, armR: 150, seed: 22 });
      const b = clamp((lt - .55) / .35);
      setBall('e6b13', lt < .55 ? K(lt, [[0, -40], [.55, 660]]) : lerp(660, 380, b), lt < .55 ? K(lt, [[0, 760], [.55, 880]]) : lerp(880, 1150, b), lt * 700, 1 - b * .2);
      $('e6g13').querySelector('.net').setAttribute('transform', lt > .9 ? `translate(0,${-Math.sin((lt - .9) * 14) * Math.exp(-(lt - .9) * 3) * 30}) scale(1,${1 + Math.sin((lt - .9) * 14) * Math.exp(-(lt - .9) * 3) * .08})` : '');
      $('e6crowd13').setAttribute('transform', `translate(0,${lt > .9 ? -Math.abs(Math.sin(lt * 10)) * 18 : 0})`);
      showPop('e6gol', lt, .9, 540, 520, 1); flash('e6fl13', lt, .9);
    }
  };
});

// 14. GOL! +R$ 500 (chuva de notas)
shot(36.9, 39.7, () => {
  const k = mk('caio');
  let notes = ''; for (let i = 0; i < 12; i++) notes += noteSvg('e6n14' + i, '50', '#f2b8a0', '#a8492a');
  const svg = field('e6crowd14') + `<g>${k.svg}</g>` + notes + bigNum('e6plus', '+R$ 500', 170, '#3fbf6a') + scoreBoard('e6sc14') + cardSvg('e6c14');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.05], [2.8, 1.12]]), fx: 540, fy: 1100 }),
    update(lt) {
      $('e6crowd14').setAttribute('transform', `translate(0,${-Math.abs(Math.sin(lt * 10)) * 18})`);
      setChar(k.id, { x: 540, y: 1640, scale: 1.05, t: lt, mouth: 'smile', talk: lt < 2.4, eyes: 'money', armL: 165, armR: 165, hop: 2.6, seed: 23 });
      for (let i = 0; i < 12; i++) { const el = $('e6n14' + i); const p = lt - .2 - i * .1; if (p < 0) { el.setAttribute('display', 'none'); continue; } el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${60 + (i * 97) % 960 + Math.sin(p * 5 + i) * 40},${-100 + p * 700}) rotate(${Math.sin(p * 6 + i) * 30})`); }
      showPop('e6plus', lt, .3, 540, 760, 1);
      setScore('e6sc14', 540, 140, 'LARANJA 1 x 0 AZUL');
      card('e6c14', 36.9, lt, 540, 330, 1.0, 0, .3);
    }
  };
});

// 15. "Só que borracha… sempre volta." — os braços ainda presos nas traves lá atrás
shot(39.7, 42.2, () => {
  const k = mk('caio');
  const svg = field() + `<path id="e6band1" fill="none" stroke="${OL}" stroke-width="48" stroke-linecap="round"/><path id="e6band1b" fill="none" stroke="${SKIN.caio}" stroke-width="34" stroke-linecap="round"/>
    <path id="e6band2" fill="none" stroke="${OL}" stroke-width="48" stroke-linecap="round"/><path id="e6band2b" fill="none" stroke="${SKIN.caio}" stroke-width="34" stroke-linecap="round"/>` + `<g>${k.svg}</g>` + fx('e6fx15', '...', '#fff', 160);
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.25], [2.5, 1.45]]), fx: 540, fy: 1150, tx: lt > 1.6 ? Math.sin(lt * 60) * 5 : 0 }),
    update(lt) {
      const tense = K(lt, [[0, 0], [2.4, 1]]);
      setChar(k.id, { x: 540, y: 1640, scale: 1.05, t: lt, mouth: lt > 1.0 ? 'o' : 'smile', eyes: lt > 1.0 ? 'wide' : 'happy', brow: lt > 1.0 ? 1 : 0, sweat: lt > 1.3, armL: 15, armR: 15, lean: -tense * 10, seed: 24, lookX: -12 });
      $(k.id + '-armL').setAttribute('display', 'none'); $(k.id + '-armR').setAttribute('display', 'none');
      const sh = 1640 - 560 * 1.05;
      const d1 = `M${540 - 95},${sh} Q${300},${sh - 200 - tense * 60} ${-260},${700}`, d2 = `M${540 + 95},${sh} Q${400},${sh - 300 - tense * 60} ${-260},${560}`;
      for (const [a, d] of [['e6band1', d1], ['e6band1b', d1], ['e6band2', d2], ['e6band2b', d2]]) $(a).setAttribute('d', d);
      popTag('e6fx15', lt, .9, 760, 760, 1.4);
    }
  };
});

// 16. TOING! volta voando pro próprio gol: gol contra, 1x1, metade do prêmio
shot(42.2, 45.0, () => {
  const k = mk('caio'), g = mk('n2');
  const svg = field() + goalSvg('e6g16', 540, 1420, 1.5) + `<g>${g.svg}</g><g id="e6w16">${k.svg}</g>` + ballSvg('e6b16') + bigNum('e6contra', 'GOL CONTRA', 150, '#e8453c') + scoreBoard('e6sc16') + cardSvg('e6c16') + tagSvg('e6t16', '-R$250', '#e8453c', 120) + speedLines('e6sl16');
  return {
    svg, cam: lt => ({ s: K(lt, [[0, 1.0], [2.8, 1.1]]), fx: 540, fy: 1100, tx: lt > .5 && lt < .75 ? Math.sin(lt * 90) * 12 : 0 }),
    update(lt) {
      const fly = clamp(lt / .5);
      $('e6w16').setAttribute('transform', `translate(${lerp(1400, 540, easeOut(fly))},${lerp(900, 1360, easeOut(fly))}) rotate(${lerp(-90, 0, fly)})`);
      setChar(k.id, { x: 0, y: 0, scale: .95, t: lt, mouth: lt > 1.2 ? 'flat' : 'O', eyes: lt > 1.2 ? 'half' : 'wide', brow: lt > 1.2 ? 0 : 1, armL: 150, armR: 150, squash: lt > .5 && lt < .7 ? -.1 : 0, seed: 25 });
      setChar(g.id, { x: 860, y: 1440, scale: .9, t: lt, mouth: 'smile', eyes: 'happy', armL: 160, armR: 160, hop: lt > .8 ? 2.5 : 0, seed: 26 });
      setBall('e6b16', lerp(1500, 420, easeOut(fly)), lerp(820, 1300, easeOut(fly)), lt * 500);
      $('e6g16').querySelector('.net').setAttribute('transform', lt > .5 ? `translate(0,${-Math.sin((lt - .5) * 14) * Math.exp(-(lt - .5) * 3) * 30})` : '');
      $('e6sl16').setAttribute('opacity', lt < .5 ? .6 : 0);
      showPop('e6contra', lt, .55, 540, 760, 1);
      setScore('e6sc16', 540, 140, lt > .55 ? 'LARANJA 1 x 1 AZUL' : 'LARANJA 1 x 0 AZUL');
      card('e6c16', 42.2, lt, 540, 330, 1.0, 10, 1.0);
      popTag('e6t16', lt, 1.4, 540, 560, 1.2);
    }
  };
});
