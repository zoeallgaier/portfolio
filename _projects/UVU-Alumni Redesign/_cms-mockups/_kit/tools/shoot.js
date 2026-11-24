// usage: node shoot.js jobs.json   jobs=[{html, png, w, h, scale}]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: Math.ceil(j.w), height: Math.ceil(j.h) }, deviceScaleFactor: j.scale || 1 });
    await p.goto('file://' + j.html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: j.png, omitBackground: !!j.transparent, clip: { x: 0, y: 0, width: j.w, height: j.h } });
    await p.close();
    console.log('ok', j.png);
  }
  await b.close();
})();
