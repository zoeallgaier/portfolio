// node render.js <slug...>   -> PNG preview + review PDF (copy edits on) + design PDF
const { chromium } = require('playwright');
const fs = require('fs');
const FS = '/tmp/xr/node_modules/@fontsource';
const FA = '/tmp/xr/node_modules/@fortawesome/fontawesome-free/webfonts';
function faces() {
  let css = '';
  for (const [fam, pkg] of [['Rajdhani','rajdhani'],['Lato','lato'],['Raleway','raleway'],['Montserrat','montserrat'],['Source Sans 3','source-sans-3']]) {
    for (const f of fs.readdirSync(`${FS}/${pkg}/files`)) {
      const m = f.match(/latin-(\d+)-(normal|italic)\.woff2$/); if (!m || f.includes('-ext-')) continue;
      css += `@font-face{font-family:'${fam}';font-weight:${m[1]};font-style:${m[2]};src:url('file://${FS}/${pkg}/files/${f}')}\n`;
    }
  }
  for (const w of [300,400,900]) {
    css += `@font-face{font-family:'Font Awesome 5 Pro';font-weight:${w};src:url('file://${FA}/fa-solid-900.woff2')}\n`;
    css += `@font-face{font-family:'Font Awesome 5 Solid';font-weight:${w};src:url('file://${FA}/fa-solid-900.woff2')}\n`;
  }
  css += `@font-face{font-family:'Font Awesome 5 Brands';src:url('file://${FA}/fa-brands-400.woff2')}\n`;
  return css;
}
async function fitPdf(p, h, path) {
  const { execSync } = require('child_process');
  const setH = (H) => p.evaluate((H) => { let st = document.getElementById('__fitpage'); if (!st) { st = document.createElement('style'); st.id = '__fitpage'; document.head.appendChild(st); } st.textContent = `@page{size:1440px ${H}px;margin:0}`; }, H);
  const pagesAt = async (H) => { await setH(H); const buf = await p.pdf({ preferCSSPageSize: true, printBackground: true }); fs.writeFileSync(path, buf); return +execSync(`pdfinfo "${path}" 2>/dev/null | awk '/^Pages:/{print $2}'`).toString().trim(); };
  let lo = h, hi = Math.round(h * 1.6);
  while (await pagesAt(hi) > 1) hi = Math.round(hi * 1.3);
  while (hi - lo > 24) { const mid = Math.round((lo + hi) / 2); if (await pagesAt(mid) > 1) lo = mid; else hi = mid; }
  await pagesAt(hi);
  return hi;
}
(async () => {
  const OUT = '/mnt/user-data/outputs/cms-mockups';
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const css = faces();
  for (const slug of process.argv.slice(2)) {
    const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
    await p.emulateMedia({ media: 'print' });
    await p.goto(`file://${OUT}/${slug}/index.html`, { waitUntil: 'load' });
    await p.addStyleTag({ content: css });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(600);
    await p.evaluate(() => document.querySelector('.mock-toolbar') && (document.querySelector('.mock-toolbar').style.display = 'none'));
    // design PDF: clean, one continuous page
    let h = await p.evaluate(() => document.documentElement.scrollHeight);
    await p.screenshot({ path: `/tmp/xr/prev/${slug}.png`, fullPage: true });
    await fitPdf(p, h, `/tmp/xr/pdf/${slug}--design.pdf`);
    // copy review PDF: highlights + numbered notes + accordions open
    await p.evaluate(() => window.mockPrepareReview());
    await p.waitForTimeout(200);
    h = await p.evaluate(() => document.documentElement.scrollHeight);
    await fitPdf(p, h, `/tmp/xr/pdf/${slug}--copy-review.pdf`);
    await p.screenshot({ path: `/tmp/xr/prev/${slug}--copy.png`, fullPage: true });
    console.log(slug, h);
    await p.close();
  }
  await b.close();
})();
