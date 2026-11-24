// node geo.js slug width  -> alignment + mobile audit report
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

(async () => {
  const [slug, W] = [process.argv[2], +process.argv[3]];
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: W, height: 900 }, deviceScaleFactor: 1, isMobile: W < 700, hasTouch: W < 700 });
  await p.route(/^https?:\/\//, r => r.request().resourceType() === 'image' ? r.fulfill({ path: '/tmp/xr/ph-live.png' }) : r.abort());
  await p.goto(`file:///mnt/user-data/outputs/cms-mockups/${slug}/index.html`);
  await p.addStyleTag({ content: faces() + '.mock-toolbar{display:none!important}' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); await new Promise(r => setTimeout(r, 600)); });
  const r = await p.evaluate(() => {
    const out = { overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth, edges: [], small: [], tiny: [], wide: [] };
    const m = document.querySelector('main');
    m.querySelectorAll(':scope > section').forEach((s, i) => {
      const firstText = s.querySelector('h1, h2, .al-quicklinks, p');
      const box = firstText ? firstText.getBoundingClientRect() : null;
      const cont = s.querySelector('.container-fluid').getBoundingClientRect();
      out.edges.push(`${i + 1} ${s.dataset.uvuTemplate}${s.classList.contains('al-hero') ? '(hero)' : ''}: container ${Math.round(cont.left)}–${Math.round(cont.right)} | first text x=${box ? Math.round(box.left) : '-'} | pad ${getComputedStyle(s).paddingTop}/${getComputedStyle(s).paddingBottom} h=${Math.round(s.getBoundingClientRect().height)}`);
    });
    m.querySelectorAll('a, button, summary').forEach(a => { const r = a.getBoundingClientRect(); if (r.width && r.height < 44 && !a.closest('p')) out.small.push(`${a.tagName} "${a.textContent.trim().slice(0, 30)}" ${Math.round(r.width)}x${Math.round(r.height)}`); });
    m.querySelectorAll('p, li, span, h3, h4, summary, a').forEach(e => { const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 14 && e.textContent.trim() && !e.closest('.mock-todo') && !e.classList.contains('mock-todo') && !e.classList.contains('mock-copy-num')) out.tiny.push(`${e.tagName}.${e.className} ${fs}px "${e.textContent.trim().slice(0, 30)}"`); });
    m.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (e.closest('.al-grid--swipe') && !e.classList.contains('al-grid--swipe')) return; if (r.right > window.innerWidth + 1 && r.width > 0) out.wide.push(`${e.tagName}.${e.className.toString().slice(0, 40)} right=${Math.round(r.right)}`); });
    const h=document.querySelector('.al-hero'); if(h){const a=h.getBoundingClientRect(), c=h.querySelector('header').getBoundingClientRect(); out.hero=`hero h=${Math.round(a.height)} text top gap=${Math.round(c.top-a.top)} bottom gap=${Math.round(a.bottom-c.bottom)} display=${getComputedStyle(h).display}`;}
    return out;
  });
  console.log(`== ${slug} @${W}  overflowX=${r.overflowX}`);
  console.log(r.edges.join('\n')); console.log(r.hero);
  if (r.small.length) console.log('SMALL TARGETS:\n  ' + [...new Set(r.small)].slice(0, 15).join('\n  '));
  if (r.tiny.length) console.log('TINY TEXT:\n  ' + [...new Set(r.tiny)].slice(0, 10).join('\n  '));
  if (r.wide.length) console.log('OVERFLOWING:\n  ' + [...new Set(r.wide)].slice(0, 10).join('\n  '));
  await p.screenshot({ path: `/tmp/xr/prev/${slug}@${W}.png`, fullPage: true });
  await b.close();
})();
