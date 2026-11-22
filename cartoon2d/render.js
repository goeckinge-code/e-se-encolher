// Renderiza a animação quadro a quadro com o Chromium (Playwright).
// Uso: node render.js still 1,5,9.5        -> out/still/t*.png
//      node render.js seq [fps=30]          -> out/frames/*.jpg  (depois: ./montar.sh)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [mode = 'still', arg = '1'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('ERRO NA PÁGINA:', e.message));
  await p.goto('file://' + path.join(__dirname, 'index.html'));
  await p.waitForFunction(() => window.READY);
  await p.evaluate(() => document.fonts.ready);
  if (mode === 'still') {
    fs.mkdirSync(path.join(__dirname, 'out/still'), { recursive: true });
    for (const t of arg.split(',').map(Number)) {
      await p.evaluate(t => render(t), t);
      await p.screenshot({ path: path.join(__dirname, `out/still/t${t.toFixed(2).padStart(5, '0')}.png`) });
    }
  } else {
    const fps = Number(arg) || 30, n = Math.round(30 * fps), dir = path.join(__dirname, 'out/frames');
    fs.mkdirSync(dir, { recursive: true });
    const t0 = Date.now();
    for (let f = 0; f < n; f++) {
      await p.evaluate(t => render(t), f / fps);
      await p.screenshot({ path: `${dir}/${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
      if (f % 60 === 0) console.log(`quadro ${f}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }
  await b.close();
})();
