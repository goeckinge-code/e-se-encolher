// Renderiza a animação quadro a quadro com o Chromium (Playwright).
// Uso: node render.js still 1,5,9.5 --ep ep02-mentira   -> out/<ep>/still/t*.png
//      node render.js seq 30 --ep ep02-mentira        -> out/<ep>/frames/*.jpg  (depois: ./montar.sh <ep>)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const A = process.argv.slice(2); const ei = A.indexOf('--ep'); const EP = ei >= 0 ? A.splice(ei, 2)[1] : 'ep01-reclamacao';
  const [mode = 'still', arg = '1'] = A;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('ERRO NA PÁGINA:', e.message));
  await p.goto('file://' + path.join(__dirname, 'index.html') + '?ep=' + EP);
  await p.waitForFunction(() => window.READY);
  await p.evaluate(() => document.fonts.ready);
  if (mode === 'still') {
    fs.mkdirSync(path.join(__dirname, `out/${EP}/still`), { recursive: true });
    for (const t of arg.split(',').map(Number)) {
      await p.evaluate(t => render(t), t);
      await p.screenshot({ path: path.join(__dirname, `out/${EP}/still/t${t.toFixed(2).padStart(5, '0')}.png`) });
    }
  } else {
    const dur = await p.evaluate(() => DUR);
    const fps = Number(arg) || 30, n = Math.round(dur * fps), dir = path.join(__dirname, `out/${EP}/frames`);
    fs.mkdirSync(dir, { recursive: true });
    const t0 = Date.now();
    for (let f = 0; f < n; f++) {
      if (fs.existsSync(`${dir}/${String(f).padStart(5, '0')}.jpg`) && !process.env.REFAZ) continue;
      await p.evaluate(t => render(t), f / fps);
      await p.screenshot({ path: `${dir}/${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
      if (f % 60 === 0) console.log(`quadro ${f}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }
  await b.close();
})();
