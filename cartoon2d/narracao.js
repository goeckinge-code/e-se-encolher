// Gera episodios/<ep>.txt com a narração e os tempos. Uso: node narracao.js ep02-mentira
const fs = require('fs'); const ep = process.argv[2] || 'ep01-reclamacao';
const src = fs.readFileSync(`episodios/${ep}.js`, 'utf8');
const L = eval(src.slice(src.indexOf('LINES =') + 7, src.indexOf('];', src.indexOf('LINES =')) + 1));
const f = t => `${Math.floor(t / 60)}:${(t % 60).toFixed(1).padStart(4, '0')}`;
const title = src.split('\n')[0].replace(/^\/\/ /, '');
let out = `${title}\n\nTEXTO\n${L.map(l => l[2]).join('\n')}\n\nCOM TEMPOS\n`;
for (const [a, b, t] of L) out += `[${f(a)} - ${f(b)}] ${t}\n`;
fs.writeFileSync(`episodios/${ep}.txt`, out); console.log(out);
