// Estilo 2 do mundo do Caio (a partir do ep08): desenho mais rico e animação com passada de verdade.
// Referência estudada: cartoon "cada passo custa R$2" — cabeça grande e redonda, sobrancelha grossa,
// bochecha alaranjada, cabelo com textura, roupa com dobras e sombra lateral, tênis de sola grossa,
// andar com o pé que sobe e o corpo que balança; bairro em camadas (céu com nuvens, morro com casinhas,
// casas detalhadas, postes com fios, calçada em perspectiva, asfalto escuro); saldo em balão sobre a cabeça.
// Mantém a mesma API (char / setChar) e os mesmos ids das partes, então o motor e K() funcionam igual.
const OL2 = '#24203d';
const SW2 = 7;

const shade = (hex, f) => { const n = parseInt(hex.slice(1), 16); let r = n >> 16, g = (n >> 8) & 255, b = n & 255; r = Math.round(r * f); g = Math.round(g * f); b = Math.round(b * f); return `rgb(${Math.min(255, r)},${Math.min(255, g)},${Math.min(255, b)})`; };

char = function (id, o) {
  const kid = !!o.kid;
  const R = kid ? 140 : 122;
  const shoeH = 46, shin = o.sit ? 30 : (kid ? 64 : 94), thigh = o.sit ? 26 : (kid ? 70 : 100);
  const torsoH = kid ? 176 : 214;
  const tw = o.belly ? 252 : (kid ? 184 : 198);
  const hipY = -(shoeH + shin + thigh);
  const torsoBot = hipY + 38, torsoTop = torsoBot - torsoH;
  const shY = torsoTop + 32;
  const hy = torsoTop - R + 38;
  const sk = o.skin, skD = shade(sk, .82);
  const lx = kid ? 38 : 44;
  const P = [];
  const st = `stroke="${OL2}" stroke-width="${SW2}" stroke-linejoin="round" stroke-linecap="round"`;
  P.push(`<ellipse cx="0" cy="6" rx="${tw * .6}" ry="18" fill="rgba(36,32,61,.22)"/>`);
  P.push(`<g id="${id}-body">`);
  // ---------------- pernas (coxa + canela + tênis); a perna inteira sobe na passada
  const pantsCol = o.longPants ? (o.pants || o.shorts) : (o.shorts || o.pants || '#3b5bb5');
  for (const s of [-1, 1]) {
    const x = s * lx;
    P.push(`<g id="${id}-leg${s > 0 ? 'L' : 'R'}">`);
    // canela
    const shinCol = o.longPants || o.dress ? (o.dress ? sk : pantsCol) : sk;
    P.push(`<g class="shin"><rect x="${x - 20}" y="${hipY + thigh - 14}" width="40" height="${shin + 22}" rx="16" fill="${shinCol}" ${st}/>`);
    if (o.longPants) P.push(`<path d="M${x - 6},${hipY + thigh + 6} q6,14 0,28" fill="none" stroke="${shade(pantsCol, .7)}" stroke-width="4"/>`);
    // tênis visto de frente/3-4: biqueira arredondada, sola grossa branca, cadarço
    const sc = o.shoe || '#ffffff';
    P.push(`<path d="M${x - 30},${-6} Q${x - 34},${-shoeH + 6} ${x - 6},${-shoeH} L${x + 10},${-shoeH} Q${x + 38},${-shoeH + 4} ${x + 36},${-8} Z" fill="${sc}" ${st}/>`);
    P.push(`<rect x="${x - 34}" y="-14" width="72" height="16" rx="8" fill="${o.sole || '#f4f4f4'}" ${st}/>`);
    P.push(`<path d="M${x - 8},${-shoeH + 12} l16,0 M${x - 8},${-shoeH + 22} l16,0" stroke="${OL2}" stroke-width="4" stroke-linecap="round"/></g>`);
    // coxa (bermuda/calça)
    P.push(`<rect x="${x - 25}" y="${hipY - 18}" width="50" height="${thigh + 26}" rx="18" fill="${o.dress ? sk : pantsCol}" ${st}/>`);
    if (!o.dress && !o.longPants) P.push(`<path d="M${x - 24},${hipY + thigh - 4} L${x + 24},${hipY + thigh - 4}" stroke="${shade(pantsCol, .7)}" stroke-width="5"/>`);
    if (!o.dress) P.push(`<path d="M${x + s * 8},${hipY + 10} q${-s * 6},${thigh * .4} 0,${thigh * .7}" fill="none" stroke="${shade(pantsCol, .72)}" stroke-width="4" stroke-linecap="round"/>`);
    P.push(`</g>`);
  }
  // quadril (bermuda/calça) ou saia
  if (o.dress) P.push(`<path d="M${-tw / 2 + 4},${torsoTop + 40} L${tw / 2 - 4},${torsoTop + 40} L${tw / 2 + 36},${hipY + 66} Q0,${hipY + 84} ${-tw / 2 - 36},${hipY + 66} Z" fill="${o.dress}" ${st}/>` +
    Array.from({ length: 8 }, (_, i) => `<circle cx="${((i * 57) % 200) - 100}" cy="${torsoTop + 90 + ((i * 41) % 140)}" r="7" fill="#fff" opacity=".85"/>`).join('') +
    `<path d="M${tw / 2 - 30},${torsoTop + 60} L${tw / 2 + 10},${hipY + 60}" stroke="${shade(o.dress, .8)}" stroke-width="18" opacity=".5"/>`);
  else P.push(`<path d="M${-tw / 2 + 8},${hipY - 40} L${tw / 2 - 8},${hipY - 40} L${tw / 2 - 2},${hipY + 26} L${-tw / 2 + 2},${hipY + 26} Z" fill="${pantsCol}" ${st}/><path d="M0,${hipY - 30} L0,${hipY + 20}" stroke="${shade(pantsCol, .7)}" stroke-width="4"/>`);
  if (o.sit) P.push(`<rect x="${-tw / 2 - 6}" y="${hipY - 46}" width="${tw + 12}" height="60" rx="28" fill="${o.dress || pantsCol}" ${st}/>`);
  // ---------------- braços (manga + antebraço + mão em luva)
  const arm = side => {
    const sx = side * (tw / 2 - 8), len = kid ? 140 : 162, w = o.belly || o.tank ? 42 : 40;
    const sleeveCol = o.sleeveLong ? o.shirt : o.shirt;
    const fore = o.sleeveLong ? o.shirt : sk;
    return `<g id="${id}-arm${side > 0 ? 'L' : 'R'}">
      <rect x="${sx - w / 2}" y="${shY - 6}" width="${w}" height="${len}" rx="${w / 2}" fill="${fore}" ${st}/>
      ${o.tank ? '' : `<path d="M${sx - 30},${shY - 26} Q${sx},${shY - 40} ${sx + 30},${shY - 26} L${sx + 28},${shY + (o.sleeveLong ? len - 30 : 58)} Q${sx},${shY + (o.sleeveLong ? len - 20 : 66)} ${sx - 28},${shY + (o.sleeveLong ? len - 30 : 58)} Z" fill="${sleeveCol}" ${st}/>
      <path d="M${sx + side * 10},${shY - 10} l0,${o.sleeveLong ? len - 50 : 50}" stroke="${shade(o.shirt, .78)}" stroke-width="10" stroke-linecap="round" opacity=".7"/>`}
      <g transform="translate(${sx},${shY + len})"><path d="M-27,-6 Q-30,26 0,30 Q30,26 27,-6 Q24,-24 0,-24 Q-24,-24 -27,-6 Z" fill="${o.glove || sk}" ${st}/><path d="M${-side * 26},-4 q${-side * 14},4 ${-side * 6},18" fill="${o.glove || sk}" ${st}/></g></g>`;
  };
  P.push(arm(-1), arm(1));
  // ---------------- tronco (camiseta com sombra lateral, dobras, gola, bolso)
  if (!o.dress) {
    const bw = o.belly ? 44 : 0;
    const shirtD = shade(o.shirt, .8);
    P.push(`<path d="M${-tw / 2},${torsoTop + 34} Q${-tw / 2},${torsoTop} ${-tw / 2 + 34},${torsoTop} L${tw / 2 - 34},${torsoTop} Q${tw / 2},${torsoTop} ${tw / 2},${torsoTop + 34} L${tw / 2 + bw},${torsoBot - 36} Q${tw / 2 + bw},${torsoBot + 2} ${tw / 2 - 30},${torsoBot + 2} L${-tw / 2 + 30},${torsoBot + 2} Q${-tw / 2 - bw},${torsoBot + 2} ${-tw / 2 - bw},${torsoBot - 36} Z" fill="${o.shirt}" ${st}/>`);
    P.push(`<path d="M${tw / 2 - 40},${torsoTop + 8} Q${tw / 2 - 8},${torsoTop + 30} ${tw / 2 - 6 + bw},${torsoBot - 30} L${tw / 2 - 30},${torsoBot - 4} Q${tw / 2 - 30},${torsoTop + 60} ${tw / 2 - 40},${torsoTop + 8} Z" fill="${shirtD}" opacity=".65"/>`);
    if (o.stripe) for (let i = 0; i < 3; i++) P.push(`<rect x="${-tw / 2 + 6}" y="${torsoTop + 46 + i * 40}" width="${tw - 12}" height="16" fill="${o.stripe}" opacity=".9"/>`);
    if (o.tank) P.push(`<path d="M${-tw / 2 + 22},${torsoTop} Q0,${torsoTop + 64} ${tw / 2 - 22},${torsoTop}" fill="${sk}" ${st}/>`);
    else P.push(`<path d="M-34,${torsoTop + 2} Q0,${torsoTop + 30} 34,${torsoTop + 2}" fill="${shirtD}" ${st}/>`);
    P.push(`<path d="M${-tw / 2 + 30},${torsoBot - 26} q22,-10 40,0 M${tw / 2 - 74},${torsoBot - 22} q18,-12 34,0" fill="none" stroke="${shirtD}" stroke-width="5" stroke-linecap="round"/>`);
    if (o.pocket) P.push(`<rect x="${-tw / 2 + 30}" y="${torsoTop + 50}" width="44" height="44" rx="8" fill="${o.pocket}" ${st}/><path d="M${-tw / 2 + 30},${torsoTop + 64} l44,0" stroke="${OL2}" stroke-width="4"/>`);
    if (o.logo) P.push(`<circle cx="${-tw / 2 + 56}" cy="${torsoTop + 76}" r="28" fill="#f5c531" ${st}/><text x="${-tw / 2 + 56}" y="${torsoTop + 89}" text-anchor="middle" font-family="Luckiest" font-size="36" fill="${OL2}">${o.logo}</text>`);
    if (o.vest) P.push(`<path d="M${-tw / 2 + 4},${torsoTop + 24} L-18,${torsoTop + 96} L-18,${torsoBot} M${tw / 2 - 4},${torsoTop + 24} L18,${torsoTop + 96} L18,${torsoBot}" fill="none" stroke="${OL2}" stroke-width="6"/>`);
  }
  // ---------------- cabeça
  P.push(`<g id="${id}-head">`);
  for (const s of [-1, 1]) P.push(`<circle cx="${s * (R - 2)}" cy="${hy + 14}" r="30" fill="${sk}" ${st}/><path d="M${s * (R + 4)},${hy + 4} q${-s * 12},10 0,22" fill="none" stroke="${skD}" stroke-width="6" stroke-linecap="round"/>`);
  if (o.hair === 'bun') P.push(`<circle cx="0" cy="${hy - R - 18}" r="48" fill="${o.hairCol}" ${st}/>`);
  if (o.hair === 'curly') for (let i = 0; i < 10; i++) { const a = Math.PI * (1.02 + i * .1); P.push(`<circle cx="${Math.cos(a) * R}" cy="${hy + Math.sin(a) * R}" r="42" fill="${o.hairCol}" ${st}/>`); }
  if (o.hair === 'long') P.push(`<path d="M${-R - 10},${hy - 20} Q${-R - 20},${hy + 150} ${-R + 30},${hy + 170} L${R - 30},${hy + 170} Q${R + 20},${hy + 150} ${R + 10},${hy - 20} Z" fill="${o.hairCol}" ${st}/>`);
  P.push(`<circle cx="0" cy="${hy}" r="${R}" fill="${sk}" ${st}/>`);
  P.push(`<circle id="${id}-red" cx="0" cy="${hy}" r="${R - 4}" fill="#ff3b3b" opacity="0"/>`);
  // sombra suave de um lado do rosto
  P.push(`<path d="M${R * .55},${hy - R * .8} Q${R * 1.02},${hy} ${R * .45},${hy + R * .85} Q${R * .85},${hy} ${R * .55},${hy - R * .8} Z" fill="${skD}" opacity=".5"/>`);
  // cabelo com textura de pontinhos (tranças) / boné
  const dots = (cx, cy, rx, ry, n, col) => { let d = ''; for (let i = 0; i < n; i++) { const a = Math.PI * (1.08 + (i % 9) * .1), rr = .55 + Math.floor(i / 9) * .16; d += `<circle cx="${cx + Math.cos(a) * rx * rr}" cy="${cy + Math.sin(a) * ry * rr}" r="5" fill="${col}"/>`; } return d; };
  if (o.hair === 'cap') {
    for (const s of [-1, 1]) P.push(`<path d="M${s * (R - 6)},${hy - 10} Q${s * (R - 2)},${hy - 60} ${s * (R - 40)},${hy - 74} L${s * (R - 50)},${hy - 20} Z" fill="${o.hairCol}" ${st}/>` + Array.from({ length: 5 }, (_, i) => `<circle cx="${s * (R - 22 - (i % 2) * 12)}" cy="${hy - 22 - i * 10}" r="4" fill="${shade(o.hairCol, 1.9)}"/>`).join(''));
    P.push(`<g id="${id}-cap"><path d="M${-R - 8},${hy - 34} Q${-R + 2},${hy - R - 40} 0,${hy - R - 36} Q${R - 2},${hy - R - 40} ${R + 8},${hy - 34} Q0,${hy - 50} ${-R - 8},${hy - 34} Z" fill="${o.cap}" ${st}/>
      <path d="M0,${hy - R - 34} Q-20,${hy - 90} -30,${hy - 46} M0,${hy - R - 34} Q22,${hy - 90} 34,${hy - 46}" fill="none" stroke="${shade(o.cap, .7)}" stroke-width="5"/>
      <path d="M${R * .2},${hy - R - 30} Q${R * .9},${hy - R} ${R + 8},${hy - 36} Q${R * .6},${hy - 46} ${R * .2},${hy - R - 30} Z" fill="${shade(o.cap, .8)}" opacity=".7"/>
      <path d="M${R - 14},${hy - 52} Q${R + 74},${hy - 64} ${R + 100},${hy - 38} Q${R + 46},${hy - 22} ${R - 10},${hy - 30} Z" fill="${o.cap}" ${st}/>
      <circle cx="0" cy="${hy - R - 34}" r="11" fill="${o.cap}" ${st}/><path d="M${-R * .55},${hy - R + 16} Q${-R * .2},${hy - R - 14} ${R * .1},${hy - R - 6}" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="9" stroke-linecap="round"/></g>`);
  } else if (o.hair === 'short' || o.hair === 'curly' || o.hair === 'bun' || o.hair === 'long') {
    P.push(`<path d="M${-R + 2},${hy - 8} Q${-R + 4},${hy - R - 18} 0,${hy - R - 12} Q${R - 4},${hy - R - 18} ${R - 2},${hy - 8} Q${R - 20},${hy - 66} ${R * .2},${hy - 80} Q0,${hy - 62} ${-R * .3},${hy - 82} Q${-R + 26},${hy - 70} ${-R + 2},${hy - 8} Z" fill="${o.hairCol}" ${st}/>`);
    if (o.hair === 'short') P.push(dots(0, hy - 30, R * .95, R * .95, 27, shade(o.hairCol, 2.2)));
    else P.push(`<path d="M${-R * .5},${hy - R + 6} Q${-R * .2},${hy - R - 8} ${R * .1},${hy - R}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="8" stroke-linecap="round"/>`);
  } else if (o.hair === 'bald') {
    for (const s of [-1, 1]) P.push(`<path d="M${s * (R - 6)},${hy + 6} q${s * 30},-34 ${s * 2},-70 q${s * -20},12 ${s * -24},34 Z" fill="#f2f2f2" ${st}/>`);
    P.push(`<path d="M-34,${hy - R + 28} Q0,${hy - R + 12} 34,${hy - R + 28}" fill="none" stroke="rgba(255,255,255,.45)" stroke-width="9" stroke-linecap="round"/>`);
  }
  // olhos grandes ovais
  const ex = kid ? 50 : 42, ey = hy - 2, erx = kid ? 33 : 27, ery = kid ? 40 : 33;
  P.push(`<g id="${id}-eyes">`);
  for (const s of [-1, 1]) {
    P.push(`<g id="${id}-eye${s > 0 ? 'L' : 'R'}"><ellipse cx="${s * ex}" cy="${ey}" rx="${erx}" ry="${ery}" fill="#fff" ${st}/>
      <g class="pup"><ellipse cx="${s * ex + 4}" cy="${ey + 6}" rx="${erx * .62}" ry="${ery * .62}" fill="#3a2214"/><circle cx="${s * ex + 4}" cy="${ey + 6}" r="${erx * .34}" fill="#120c14"/><circle cx="${s * ex + 12}" cy="${ey - 6}" r="${erx * .26}" fill="#fff"/><circle cx="${s * ex - 4}" cy="${ey + 16}" r="${erx * .1}" fill="#fff"/></g>
      <path class="lid" d="M${s * ex - erx - 4},${ey + 2} A${erx + 4},${ery + 4} 0 0 1 ${s * ex + erx + 4},${ey + 2} Z" fill="${sk}" ${st} display="none"/>
      <path class="happy" d="M${s * ex - erx + 4},${ey + 10} Q${s * ex},${ey - 28} ${s * ex + erx - 4},${ey + 10}" fill="none" stroke="${OL2}" stroke-width="10" stroke-linecap="round" display="none"/>
      <text class="money" x="${s * ex}" y="${ey + 20}" text-anchor="middle" font-family="Luckiest" font-size="${erx * 1.6}" fill="#2fae60" stroke="${OL2}" stroke-width="4" paint-order="stroke" display="none">$</text></g>`);
  }
  P.push(`</g>`);
  if (o.glasses) for (const s of [-1, 1]) P.push(`<circle cx="${s * ex}" cy="${ey}" r="${erx + 10}" fill="rgba(200,230,255,.18)" stroke="${OL2}" stroke-width="6"/>`);
  // sobrancelhas grossas
  for (const s of [-1, 1]) P.push(`<path id="${id}-brow${s > 0 ? 'L' : 'R'}" d="M${s * ex - 24},${ey - ery - 14} Q${s * ex},${ey - ery - 30} ${s * ex + 24},${ey - ery - 14}" fill="none" stroke="${o.browCol || OL2}" stroke-width="13" stroke-linecap="round"/>`);
  if (!o.noCheeks) for (const s of [-1, 1]) P.push(`<ellipse cx="${s * (ex + 34)}" cy="${ey + 50}" rx="26" ry="17" fill="#ff7a52" opacity=".45"/>`);
  P.push(`<path d="M-10,${ey + 40} Q0,${ey + 50} 10,${ey + 40}" fill="none" stroke="${OL2}" stroke-width="6" stroke-linecap="round"/>`);
  P.push(`<g id="${id}-shades" display="none">${[-1, 1].map(s => `<rect x="${s * ex - erx - 6}" y="${ey - 22}" width="${2 * erx + 12}" height="46" rx="16" fill="#1b1730" ${st}/><path d="M${s * ex - erx + 4},${ey - 10} l18,0" stroke="#fff" stroke-width="6" opacity=".6"/>`).join('')}<path d="M${-ex + erx + 6},${ey - 8} L${ex - erx - 6},${ey - 8}" stroke="#1b1730" stroke-width="8"/></g>`);
  // bocas
  const my = hy + (kid ? 70 : 60);
  P.push(`<g id="${id}-mouths">
    <g data-m="smile"><path d="M-40,${my - 10} Q0,${my + 52} 40,${my - 10} Z" fill="#7a1f2b" ${st}/><path d="M-26,${my - 6} L26,${my - 6} L22,${my + 6} L-22,${my + 6} Z" fill="#fff"/><ellipse cx="0" cy="${my + 24}" rx="18" ry="9" fill="#ff6f7f"/></g>
    <g data-m="talk"><path d="M-26,${my - 4} Q0,${my + 28} 26,${my - 4} Z" fill="#7a1f2b" ${st}/></g>
    <g data-m="o"><ellipse cx="0" cy="${my + 8}" rx="17" ry="22" fill="#7a1f2b" ${st}/></g>
    <g data-m="O"><ellipse cx="0" cy="${my + 16}" rx="30" ry="40" fill="#7a1f2b" ${st}/><ellipse cx="0" cy="${my + 38}" rx="18" ry="9" fill="#ff6f7f"/></g>
    <g data-m="yawn"><ellipse cx="0" cy="${my + 20}" rx="36" ry="54" fill="#7a1f2b" ${st}/><ellipse cx="0" cy="${my + 50}" rx="22" ry="14" fill="#ff6f7f"/><path d="M-14,${my - 24} L14,${my - 24}" stroke="#fff" stroke-width="8"/></g>
    <g data-m="shout"><path d="M-30,${my - 6} L30,${my - 6} L48,${my + 50} L-48,${my + 50} Z" fill="#7a1f2b" ${st}/><rect x="-28" y="${my - 4}" width="56" height="11" fill="#fff"/><path d="M-32,${my + 50} Q0,${my + 30} 32,${my + 50} Z" fill="#ff6f7f"/></g>
    <g data-m="flat"><path d="M-22,${my + 6} L22,${my + 6}" stroke="${OL2}" stroke-width="8" stroke-linecap="round"/></g>
    <g data-m="frown"><path d="M-28,${my + 16} Q0,${my - 8} 28,${my + 16}" fill="none" stroke="${OL2}" stroke-width="9" stroke-linecap="round"/></g>
    <g data-m="smug"><path d="M-30,${my} Q0,${my + 24} 30,${my}" fill="none" stroke="${OL2}" stroke-width="9" stroke-linecap="round"/></g>
    <g data-m="puff"><ellipse cx="0" cy="${my + 4}" rx="20" ry="10" fill="#7a1f2b" ${st}/></g>
    <g data-m="yuck"><path d="M-28,${my + 10} Q-14,${my} 0,${my + 10} Q14,${my + 20} 28,${my + 10}" fill="none" stroke="${OL2}" stroke-width="9" stroke-linecap="round"/><path d="M4,${my + 12} q10,26 22,2" fill="#ff6f7f" ${st}/></g>
  </g>`);
  if (o.mustache) P.push(`<path d="M-54,${my - 10} Q-28,${my - 34} 0,${my - 16} Q28,${my - 34} 54,${my - 10} Q28,${my - 2} 0,${my - 12} Q-28,${my - 2} -54,${my - 10} Z" fill="#f4f4f4" ${st}/>`);
  P.push(`<g id="${id}-sweat" display="none"><path d="M${R - 10},${hy - 64} q15,24 0,36 q-15,-12 0,-36 Z" fill="#8fd3ff" stroke="${OL2}" stroke-width="5"/></g>`);
  P.push(`<g id="${id}-tears" display="none">${[-1, 1].map(s => `<path d="M${s * ex - 8},${ey + ery - 4} L${s * ex + 8},${ey + ery - 4} L${s * ex + 10},${ey + 120} Q${s * ex},${ey + 132} ${s * ex - 10},${ey + 120} Z" fill="#7cc6ff" stroke="${OL2}" stroke-width="5"/>`).join('')}</g>`);
  P.push(`<g id="${id}-mad" display="none" transform="translate(${R * .62},${hy - R * .72})">${[0, 90, 180, 270].map(r => `<path d="M8,-30 Q8,-8 30,-8" fill="none" stroke="#e8453c" stroke-width="11" stroke-linecap="round" transform="rotate(${r})"/>`).join('')}</g>`);
  P.push(`</g></g>`);
  return { svg: `<g id="${id}">${P.join('')}</g>`, geo: { R, hy, shY, tw, torsoTop, torsoBot, hipY, kid, ex, ey, lx, v2: 1 } };
};

// setChar do estilo 2: reaproveita o original e troca a passada (pé que sobe, corpo que balança)
const setChar1 = setChar;
setChar = function (id, st) {
  setChar1(id, { ...st, walk: 0 });
  const g = C[id]; if (!g || !g.v2) return;
  const t = st.t || 0;
  if (st.walk) {
    const ph = t * st.walk * Math.PI * 2, s = Math.sin(ph);
    const upL = Math.max(0, s), upR = Math.max(0, -s);
    for (const [leg, up, side] of [['legL', upL, 1], ['legR', upR, -1]]) {
      $(id + '-' + leg).setAttribute('transform', `translate(${side * up * 4},${-up * 34})`);
      $(id + '-' + leg).querySelector('.shin').setAttribute('transform', `translate(0,${g.hipY}) scale(1,${1 - up * .25}) translate(0,${-g.hipY})`);
    }
    const bob = -Math.abs(Math.cos(ph)) * 10;
    const br = Math.sin(t * 3.2 + (st.seed || 0)) * .01;
    $(id + '-body').setAttribute('transform', `rotate(${(st.lean || 0) + s * 2.5},0,0) translate(0,${bob}) scale(${1 - br},${1 + br + (st.squash || 0)})`);
    const sx = g.tw / 2 - 8, sw = s * 16;
    const stretch = (k, x) => k && k !== 1 ? ` translate(${x},${g.shY}) scale(${Math.pow(k, -.12)},${k}) translate(${-x},${-g.shY})` : '';
    $(id + '-armR').setAttribute('transform', `rotate(${(st.armR ?? 8) + sw},${-sx},${g.shY})${stretch(st.armRlen, -sx)}`);
    $(id + '-armL').setAttribute('transform', `rotate(${-((st.armL ?? 8) - sw)},${sx},${g.shY})${stretch(st.armLlen, sx)}`);
  } else {
    for (const leg of ['legL', 'legR']) { const sh = $(id + '-' + leg).querySelector('.shin'); if (sh) sh.removeAttribute('transform'); }
  }
};

// ------------------------------------------------------------------ bairro em camadas
const cloud = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-110,30 Q-130,-20 -70,-30 Q-50,-80 10,-60 Q60,-90 90,-40 Q140,-30 120,30 Z" fill="#fff" opacity=".95"/></g>`;
function skyBlue(id = '') {
  return `<defs><linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb6ec"/><stop offset=".55" stop-color="#9fd6f5"/><stop offset="1" stop-color="#cfeefb"/></linearGradient></defs>
    <rect x="-300" y="-300" width="1700" height="2600" fill="url(#skyg)"/><g ${id ? `id="${id}"` : ''}>${cloud(160, 220, 1.1)}${cloud(820, 160, .9)}${cloud(1300, 260, 1)}${cloud(-300, 180, .8)}</g>`;
}
// morro ao fundo com casinhas desbotadas
function hills(y0 = 980, w = 2600) {
  let s = `<path d="M-400,${y0} Q-200,${y0 - 140} 0,${y0 - 90} Q200,${y0 - 170} 420,${y0 - 100} Q640,${y0 - 180} 860,${y0 - 110} Q1080,${y0 - 160} 1300,${y0 - 100} Q1600,${y0 - 170} ${w},${y0 - 90} L${w},${y0 + 400} L-400,${y0 + 400} Z" fill="#a9d9b4"/>`;
  const cols = ['#f6c7c0', '#f8e2a8', '#cfe3f6', '#f3d0e6', '#e9e2cf'];
  for (let i = 0; i < 22; i++) { const x = -300 + i * 130, y = y0 - 70 - (i * 37) % 60; s += `<g opacity=".75"><rect x="${x}" y="${y}" width="70" height="60" fill="${cols[i % 5]}"/><path d="M${x - 8},${y} L${x + 35},${y - 34} L${x + 78},${y} Z" fill="#e48d78"/><rect x="${x + 24}" y="${y + 18}" width="20" height="20" fill="#fff" opacity=".8"/></g>`; }
  return s;
}
// casa detalhada: telhado com telhas, janela com veneziana, porta, floreira, muro de tijolo ou cerquinha
function house2(x, w, h, col, o = {}) {
  const y0 = o.y0 || 1430, top = y0 - h, rc = o.roofCol || '#d9674b';
  const st = `stroke="${OL2}" stroke-width="6" stroke-linejoin="round"`;
  let s = `<rect x="${x}" y="${top}" width="${w}" height="${h}" fill="${col}" ${st}/>`;
  s += `<rect x="${x + w - 26}" y="${top}" width="26" height="${h}" fill="${shade(col, .85)}"/>`;
  if (o.flat) s += `<rect x="${x - 16}" y="${top - 26}" width="${w + 32}" height="30" fill="${shade(col, .8)}" ${st}/>`;
  else { s += `<path d="M${x - 34},${top + 6} L${x + w / 2},${top - (o.roofH || 150)} L${x + w + 34},${top + 6} Z" fill="${rc}" ${st}/>`; for (let i = 1; i < 5; i++) { const yy = top + 6 - i * (o.roofH || 150) / 5; const half = (w / 2 + 34) * (1 - i / 5); s += `<path d="M${x + w / 2 - half},${yy} L${x + w / 2 + half},${yy}" stroke="${shade(rc, .75)}" stroke-width="5"/>`; } if (o.circle) s += `<circle cx="${x + w / 2}" cy="${top - (o.roofH || 150) * .45}" r="18" fill="#fff" ${st}/>`; }
  const win = (wx, wy, ww = 150, wh = 150) => `<rect x="${wx - 22}" y="${wy}" width="22" height="${wh}" fill="${o.shutter || '#3f9a5f'}" ${st}/><rect x="${wx + ww}" y="${wy}" width="22" height="${wh}" fill="${o.shutter || '#3f9a5f'}" ${st}/>
    <rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="#cdeeff" ${st}/><path d="M${wx + ww / 2},${wy} L${wx + ww / 2},${wy + wh} M${wx},${wy + wh / 2} L${wx + ww},${wy + wh / 2}" stroke="${OL2}" stroke-width="5"/><path d="M${wx + 14},${wy + 14} l30,0" stroke="#fff" stroke-width="7" opacity=".8"/>
    <rect x="${wx - 10}" y="${wy + wh}" width="${ww + 20}" height="20" fill="#fff" ${st}/>${o.flowers ? `<rect x="${wx + 6}" y="${wy + wh + 20}" width="${ww - 12}" height="30" fill="#a8613a" ${st}/>${[0, 1, 2, 3].map(i => `<circle cx="${wx + 22 + i * 36}" cy="${wy + wh + 16}" r="12" fill="${['#e8453c', '#f5c531', '#e86fa0', '#fff'][i]}" stroke="${OL2}" stroke-width="3"/>`).join('')}` : ''}`;
  if (o.win !== false) s += win(x + (o.winX ?? w * .52), top + (o.winY ?? 60), o.winW || 150, o.winH || 150);
  if (o.win2) s += win(x + o.win2[0], top + o.win2[1]);
  if (o.door !== false) { const dx = x + (o.doorX ?? 34), dw = 140, dh = 270; s += `<rect x="${dx}" y="${y0 - dh}" width="${dw}" height="${dh}" fill="${o.doorCol || '#3b6fc4'}" ${st}/><rect x="${dx + 18}" y="${y0 - dh + 20}" width="${dw - 36}" height="100" rx="6" fill="none" stroke="${shade(o.doorCol || '#3b6fc4', .7)}" stroke-width="5"/><rect x="${dx + 18}" y="${y0 - dh + 140}" width="${dw - 36}" height="100" rx="6" fill="none" stroke="${shade(o.doorCol || '#3b6fc4', .7)}" stroke-width="5"/><circle cx="${dx + dw - 20}" cy="${y0 - dh / 2}" r="10" fill="#f5c531" ${st}/>`; }
  if (o.brick) { s += `<rect x="${x - 6}" y="${y0 - 170}" width="${o.brick}" height="170" fill="#c96a4a" ${st}/>`; for (let r = 0; r < 5; r++) for (let c = 0; c < o.brick / 60; c++) s += `<rect x="${x - 6 + c * 60 + (r % 2) * 30}" y="${y0 - 170 + r * 34}" width="56" height="30" fill="none" stroke="#a85438" stroke-width="3"/>`; s += `<rect x="${x - 12}" y="${y0 - 182}" width="${o.brick + 12}" height="16" fill="#e9e2cf" ${st}/>`; }
  if (o.fence) { for (let i = 0; i < o.fence / 34; i++) s += `<path d="M${x + i * 34},${y0} L${x + i * 34},${y0 - 110} L${x + i * 34 + 12},${y0 - 128} L${x + i * 34 + 24},${y0 - 110} L${x + i * 34 + 24},${y0} Z" fill="#fff" ${st}/>`; s += `<rect x="${x}" y="${y0 - 80}" width="${o.fence}" height="14" fill="#fff" ${st}/>`; }
  if (o.bush) s += `<g transform="translate(${x + o.bush},${y0})">${[[-40, -40, 50], [10, -60, 60], [60, -38, 48]].map(([bx, by, r]) => `<circle cx="${bx}" cy="${by}" r="${r}" fill="#4caf5a" ${st}/>`).join('')}<circle cx="0" cy="-80" r="16" fill="#6fd17a" opacity=".7"/></g>`;
  return s;
}
function tree2(x, y0 = 1430, s = 1) {
  return `<g transform="translate(${x},${y0}) scale(${s})"><rect x="-16" y="-300" width="32" height="300" fill="#7a4a26" stroke="${OL2}" stroke-width="6"/>${[[-70, -320, 90], [60, -330, 95], [0, -420, 110]].map(([bx, by, r]) => `<circle cx="${bx}" cy="${by}" r="${r}" fill="#3f9a4f" stroke="${OL2}" stroke-width="7"/>`).join('')}<circle cx="-20" cy="-450" r="34" fill="#6fd17a" opacity=".7"/></g>`;
}
function pole(x, y0 = 1430, h = 900) {
  return `<rect x="${x - 14}" y="${y0 - h}" width="28" height="${h}" fill="#8a8796" stroke="${OL2}" stroke-width="6"/><rect x="${x - 90}" y="${y0 - h + 50}" width="180" height="20" fill="#8a8796" stroke="${OL2}" stroke-width="6"/><circle cx="${x - 70}" cy="${y0 - h + 42}" r="9" fill="#e9e2cf" stroke="${OL2}" stroke-width="4"/><circle cx="${x + 70}" cy="${y0 - h + 42}" r="9" fill="#e9e2cf" stroke="${OL2}" stroke-width="4"/>`;
}
function wires2(xs, y0 = 1430, h = 900) {
  let s = ''; for (let k = 0; k < 3; k++) for (let i = 0; i < xs.length - 1; i++) { const a = xs[i], b = xs[i + 1], y = y0 - h + 46 + k * 16; s += `<path d="M${a},${y} Q${(a + b) / 2},${y + 60} ${b},${y}" fill="none" stroke="${OL2}" stroke-width="4"/>`; }
  return s;
}
// calçada em perspectiva + meio-fio + asfalto escuro com faixas
function street2(y0 = 1430) {
  let s = `<rect x="-400" y="${y0}" width="3600" height="210" fill="#d9dbe3" stroke="${OL2}" stroke-width="6"/>`;
  for (let x = -400; x < 3200; x += 150) s += `<path d="M${x},${y0} L${x - 50},${y0 + 210}" stroke="#b9bcc9" stroke-width="5"/>`;
  s += `<path d="M-400,${y0 + 100} L3200,${y0 + 100}" stroke="#b9bcc9" stroke-width="5"/>`;
  s += `<rect x="-400" y="${y0 + 210}" width="3600" height="26" fill="#f2f2f2" stroke="${OL2}" stroke-width="6"/>`;
  s += `<rect x="-400" y="${y0 + 236}" width="3600" height="800" fill="#4a4b63"/>`;
  for (let x = -380; x < 3200; x += 340) s += `<rect x="${x}" y="${y0 + 420}" width="170" height="20" rx="8" fill="#eeeef4" opacity=".9"/>`;
  for (let i = 0; i < 40; i++) s += `<circle cx="${(i * 191) % 3200 - 300}" cy="${y0 + 260 + (i * 53) % 300}" r="3" fill="#6a6b85"/>`;
  return s;
}
// bairro completo; as camadas têm id para fazer paralaxe (fundo devagar, casas na velocidade da câmera)
function bairro(tag, o = {}) {
  const y0 = o.y0 || 1430;
  const houses = o.houses || [
    [-420, 420, 520, '#f4a7b0', { brick: 300, doorX: 260, winX: 40, flowers: 1, shutter: '#e8453c' }],
    [40, 380, 470, '#a8dcc0', { flat: 1, doorX: 210, winX: 30, bush: 300 }],
    [460, 400, 560, '#f8d77a', { circle: 1, doorX: 40, winX: 210, fence: 160, flowers: 1 }],
    [900, 380, 500, '#9cc6ef', { flat: 1, doorX: 200, winX: 30, shutter: '#3b6fc4', bush: 60 }],
    [1320, 420, 540, '#f2b48c', { doorX: 40, winX: 220, brick: 200, circle: 1 }],
    [1780, 400, 500, '#c9b6e4', { flat: 1, doorX: 220, winX: 30, flowers: 1, fence: 200 }],
    [2220, 400, 540, '#a8dcc0', { doorX: 40, winX: 210, bush: 330 }],
  ];
  let mid = houses.map(([x, w, h, c, oo]) => house2(x, w, h, c, { ...oo, y0 })).join('');
  const px = o.poles || [-300, 380, 1060, 1740, 2420];
  mid += (o.trees || [300, 1240, 2160]).map(x => tree2(x, y0, .95)).join('') + px.map(x => pole(x, y0)).join('') + wires2(px, y0);
  return skyBlue(tag + 'cl') + `<g id="${tag}far">${hills(y0 - 330)}</g><g id="${tag}mid">${mid}</g><g id="${tag}st">${street2(y0)}</g>`;
}
// paralaxe: cam = quanto a câmera andou para a direita
function parallax(tag, cam) {
  const f = $(tag + 'far'), m = $(tag + 'mid'), s = $(tag + 'st'), c = $(tag + 'cl');
  if (f) f.setAttribute('transform', `translate(${-cam * .35},0)`);
  if (m) m.setAttribute('transform', `translate(${-cam},0)`);
  if (s) s.setAttribute('transform', `translate(${-cam},0)`);
  if (c) c.setAttribute('transform', `translate(${-cam * .1},0)`);
}

// ------------------------------------------------------------------ interior detalhado (sala de aula / casa)
function room2(o = {}) {
  const y0 = o.y0 || 1400, wall = o.wall || '#f8e3a8';
  let s = `<rect x="-300" y="-300" width="1700" height="${y0 + 300}" fill="${wall}"/>`;
  for (let i = 0; i < 12; i++) s += `<rect x="${-200 + i * 120}" y="-300" width="60" height="${y0 + 300}" fill="${shade(wall, .95)}"/>`;
  s += `<rect x="-300" y="${y0 - 60}" width="1700" height="60" fill="${shade(wall, .8)}" stroke="${OL2}" stroke-width="6"/>`;
  s += `<rect x="-300" y="${y0}" width="1700" height="900" fill="${o.floor || '#c98a52'}" stroke="${OL2}" stroke-width="6"/>`;
  for (let i = 0; i < 10; i++) s += `<path d="M-300,${y0 + 40 + i * 60} L1400,${y0 + 40 + i * 60}" stroke="${shade(o.floor || '#c98a52', .85)}" stroke-width="5"/>`;
  return s;
}

// ------------------------------------------------------------------ saldo em balão sobre a cabeça
function pillSvg(id) {
  return `<g id="${id}" display="none"><path d="M-150,-46 L150,-46 Q190,-46 190,0 Q190,46 150,46 L20,46 L0,70 L-20,46 L-150,46 Q-190,46 -190,0 Q-190,-46 -150,-46 Z" fill="#fff" stroke="${OL2}" stroke-width="8" stroke-linejoin="round"/>
    <circle cx="-136" cy="0" r="32" fill="#2fae60" stroke="${OL2}" stroke-width="5"/><text x="-136" y="14" text-anchor="middle" font-family="Luckiest" font-size="40" fill="#fff">$</text>
    <text class="v" x="26" y="18" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="52" fill="${OL2}">R$ 0,00</text></g>`;
}
function showPill(id, lt, t0, x, y, val, s = 1, col = OL2) {
  const el = $(id); if (lt < t0) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline');
  el.setAttribute('transform', `translate(${x},${y + Math.sin(lt * 2.4) * 4}) scale(${backOut((lt - t0) / .25) * s})`);
  const v = el.querySelector('.v'); v.textContent = typeof val === 'string' ? val : brl(val); v.setAttribute('fill', col);
}
// título grande no topo (duas linhas: amarela e branca)
function titleSvg(id, l1, l2) {
  return `<g id="${id}" display="none" font-family="Luckiest" text-anchor="middle" stroke="${OL2}" stroke-width="18" paint-order="stroke" stroke-linejoin="round">
    <text y="0" font-size="118" fill="#ffd23f">${l1}</text><text y="118" font-size="118" fill="#fff">${l2}</text></g>`;
}
function showTitle(id, lt, t0, t1, x = 540, y = 230) {
  const el = $(id); if (lt < t0 || lt > t1) { el.setAttribute('display', 'none'); return; }
  el.setAttribute('display', 'inline'); el.setAttribute('transform', `translate(${x},${y}) scale(${backOut((lt - t0) / .3)}) rotate(${Math.sin(lt * 3) * 1.5})`);
}

// legenda do estilo 2: branca, com contorno e sombra, na altura da calçada (sem cobrir os pés)
window.CAPTION = { y: 1745, size: 66 };
