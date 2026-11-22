// Foto de perfil do Caio (quadrada, sorrindo), tirada da cena de apresentação.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'index.html'));
  await p.waitForFunction(() => window.READY); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => {
    render(9.3);
    const id = document.querySelector('#shot4 [id$="-mouths"]').id.replace('-mouths', '');
    setChar(id, { x: 540, y: 1480, scale: 1.25, t: .5, mouth: 'smile', eyes: 'open', armL: 12, armR: 12, seed: 7, lookY: 2 });
    document.getElementById('capT').textContent = '';
  });
  await p.screenshot({ path: path.join(__dirname, '../renders/caio-perfil.png'), clip: { x: 165, y: 600, width: 750, height: 750 } });
  await b.close();
})();
