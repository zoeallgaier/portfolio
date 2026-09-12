/* backdrop.js — the site's one living background.

   A single fixed layer sits behind every page: a warm radial glow with the
   animated dot grid over it. It is built once and never torn down, so when
   js/app.js swaps <main> for the next page the background doesn't reload —
   the glow eases across to the new page's palette while the dot grid shifts
   hue, and the content fades over the top of it. Replaces the old per-section
   .hero-canvas / .hero-bg / .project-canvas / .project-title-bg pairs.

   A page declares its palette on <main>:
     data-backdrop="home | about | project | quiet"
     data-g1 / data-g2   (project only — the two gradient colours)
   and a .next-project link carries the palette of the page it points at, so
   the background starts drifting towards it as that bookend scrolls up. */
(function () {
  let main = document.querySelector('main#main-content');
  if (!main) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const darkQ   = window.matchMedia('(prefers-color-scheme: dark)');

  /* ── Palettes ──
     Carried over from the stylesheets these replaced: positions and radii are
     percentages of the viewport, the stop is where the gradient reaches
     transparent. `drift` turns on the slow ambient hue rotation the home hero
     used to run in CSS; `dots` scales the dot grid. */
  const ORANGE = [255, 110, 70];
  const ROSE   = [235,  80, 120];

  const PRESETS = {
    home: {
      dots: 1, band: true,
      g1: { c: [...ORANGE, 0.20], x:  95, y:  0, w: 109, h: 138, s: 70 },
      g2: { c: [...ROSE,   0.20], x:  70, y:  0, w: 109, h:  86, s: 70 },
    },
    about: {
      dots: 1, band: true,
      g1: { c: [...ORANGE, 0.17], x:  50, y: 38, w:  70, h:  70, s: 70 },
      g2: { c: [...ROSE,   0.15], x:  72, y: 80, w:  60, h:  55, s: 70 },
    },
    // Reading pages (resume, 404): the same light, turned most of the way down.
    quiet: {
      dots: 0.5, band: true,
      g1: { c: [...ORANGE, 0.08], x:  95, y:  0, w: 109, h: 138, s: 70 },
      g2: { c: [...ROSE,   0.07], x:  70, y:  0, w: 109, h:  86, s: 70 },
    },
  };

  // Project pages share one geometry and supply their own two colours. The
  // glow pools behind the title and falls away down the page, as it did when
  // it lived inside .project-title. A project can opt into the personal band
  // with data-hue="band" — Recursia does, being Zoe's own work rather than a
  // client's brand.
  const PROJECT = {
    dots: 1,
    g1: { x: 112, y: 30, w: 105, h: 68, s: 88 },
    g2: { x:  86, y: 66, w: 105, h: 62, s: 88 },
  };

  // How far the background recedes once you've scrolled off the first screen,
  // so long stretches of text aren't read over a moving grid.
  const REST_DOTS = 0.4;
  const REST_GLOW = 0.7;
  // How much of the palette's hue the dots take on (the rest stays neutral).
  const TINT = 0.55;

  const GAP = 24;          // dot spacing, unchanged from the old canvases
  const TWEEN = 1100;      // ms for the glow to cross to a new page's palette

  /* The ambient hue shift, on Zoe's own pages (home, about, resume, Recursia —
     the ones marked `band` below). They drift through one band of the wheel
     and back: peach → coral → red → purple, never out of it. The old hero
     rotated a full 360° every 60s, which was fine while each page load reset
     it to the brand orange; nothing reloads now, so a rotation would wander
     off somewhere green and stay there. Project pages don't shift at all —
     their colours are the project's. */
  const BAND = [25, -72];  // degrees: peach at rest, negative wrapping to purple
  const TRAIL = 0.3;       // how far the second pool lags the first, 0–1
  const PERIOD = 80;       // seconds for a full there-and-back
  const cycle = clock => 0.5 - 0.5 * Math.cos(clock * 2 * Math.PI / PERIOD);
  const bandHue = u => BAND[0] + (BAND[1] - BAND[0]) * u;

  /* ── Colour helpers ── */
  function parseColor(str) {
    const m = /rgba?\(([^)]+)\)/.exec(str || '');
    if (!m) return null;
    const n = m[1].split(',').map(v => parseFloat(v));
    return [n[0], n[1], n[2], n.length > 3 ? n[3] : 1];
  }

  function rgb2hsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
    let h = 0;
    if (d) {
      if (max === r)      h = ((g - b) / d) % 6;
      else if (max === g) h = (b - r) / d + 2;
      else                h = (r - g) / d + 4;
      h *= 60;
      if (h < 0) h += 360;
    }
    const l = (max + min) / 2;
    const s = d ? d / (1 - Math.abs(2 * l - 1)) : 0;
    return [h, s, l];
  }

  function hsl2rgb(h, s, l) {
    h = ((h % 360) + 360) % 360;
    const c = (1 - Math.abs(2 * l - 1)) * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = l - c / 2;
    const [r, g, b] =
      h <  60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] :
      h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
    return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
  }

  // Moving the colours themselves through the band (rather than filtering the
  // layer) keeps the dot tint in step with the glow, and lets a page change
  // blend straight from whatever is on screen to the new palette. Each pool
  // keeps its own saturation, lightness and alpha, so they never flatten into
  // the same wash.
  function banded(c, clock) {
    const [, s, l] = rgb2hsl(c[0], c[1], c[2]);
    const [r, g, b] = hsl2rgb(bandHue(cycle(clock)), s, l);
    return [r, g, b, c[3]];
  }

  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp01 = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  // Slow start, long glide out — the same feel as the content's entrance.
  const ease = t => 1 - Math.pow(1 - t, 3);

  /* ── Presets as flat number arrays, so a page change is one lerp ── */
  const KEYS = ['x', 'y', 'w', 'h', 's'];

  function flatten(p, clock) {
    const out = [];
    [p.g1, p.g2].forEach((g, i) => {
      out.push(...(p.band ? banded(g.c, clock + i * TRAIL * PERIOD) : g.c));
      KEYS.forEach(k => out.push(g[k]));
    });
    out.push(p.dots);
    return out;
  }

  function blend(a, b, t) {
    return a.map((v, i) => lerp(v, b[i], t));
  }

  function presetFor(el) {
    const name = (el && el.dataset.backdrop) || 'quiet';
    if (name !== 'project') return PRESETS[name] || PRESETS.quiet;
    const g1 = parseColor(el.dataset.g1) || [...ORANGE, 0.2];
    const g2 = parseColor(el.dataset.g2) || [...ROSE, 0.2];
    return {
      dots: PROJECT.dots,
      band: el.dataset.hue === 'band',
      g1: { ...PROJECT.g1, c: g1 },
      g2: { ...PROJECT.g2, c: g2 },
    };
  }

  /* ── The layer ── */
  const layer = document.createElement('div');
  layer.className = 'backdrop';
  layer.setAttribute('aria-hidden', 'true');
  const glow = document.createElement('div');
  glow.className = 'backdrop-glow';
  const canvas = document.createElement('canvas');
  canvas.className = 'backdrop-dots';
  layer.append(glow, canvas);
  document.body.prepend(layer);

  const ctx = canvas.getContext('2d');

  let W = 0, H = 0, cols = 0, rows = 0;
  function resize() {
    const w = layer.offsetWidth, h = layer.offsetHeight;
    if (!w || !h) return;
    W = w; H = h;
    const dpr = window.devicePixelRatio || 1;
    canvas.width  = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.ceil(W / GAP) + 1;
    rows = Math.ceil(H / GAP) + 1;
    frame();
  }

  /* ── State ── */
  let target   = presetFor(main);   // the page we're on
  let nextEl   = null;              // its .next-project bookend, if any
  let nextPre  = null;              // and the palette that link leads to
  let from     = null;              // what was on screen when a change began
  let started  = 0;                 // when it began
  let shown    = flatten(target, 0);
  let wave = 0, clock = 0, last = 0, running = false, wrote = 0, wroteNear = -1;

  function bindNext() {
    nextEl = main.querySelector('.next-project[data-g1]');
    nextPre = nextEl ? presetFor(nextEl) : null;
  }

  // How far into the next-project bookend the page is scrolled (0 until it
  // starts to appear, 1 once it's well up the screen).
  function nextProgress() {
    if (!nextEl) return 0;
    const vh = window.innerHeight || 1;
    return clamp01((vh - nextEl.getBoundingClientRect().top) / (vh * 0.75));
  }

  // How present the background is: full on the first screen, receding as the
  // page scrolls, and coming back up as that bookend arrives.
  function presence(nextP) {
    const vh = window.innerHeight || 1;
    return Math.max(1 - clamp01(window.scrollY / (vh * 0.75)), nextP);
  }

  function apply(a, near) {
    const glowFade = lerp(REST_GLOW, 1, near);
    const parts = [];
    for (let i = 0; i < 2; i++) {
      const o = i * 9;
      parts.push(
        `radial-gradient(ellipse ${a[o + 6].toFixed(1)}% ${a[o + 7].toFixed(1)}% ` +
        `at ${a[o + 4].toFixed(1)}% ${a[o + 5].toFixed(1)}%, ` +
        `rgba(${a[o] | 0},${a[o + 1] | 0},${a[o + 2] | 0},${(a[o + 3] * glowFade).toFixed(3)}) 0%, ` +
        `transparent ${a[o + 8].toFixed(1)}%)`
      );
    }
    glow.style.backgroundImage = parts.join(',');
  }

  function drawDots(a, near) {
    if (!W || !H) return;
    const dark = darkQ.matches;
    const intensity = a[18] * lerp(REST_DOTS, 1, near) * (dark ? 1.3 : 1);
    // The dots take a little of the palette's hue; the rest stays neutral, so
    // the grid reads as texture rather than colour.
    const [h] = rgb2hsl(a[0], a[1], a[2]);
    const tinted = hsl2rgb(h, dark ? 0.4 : 0.5, dark ? 0.86 : 0.16);
    const base = dark ? 255 : 0;
    const r = lerp(base, tinted[0], TINT) | 0;
    const g = lerp(base, tinted[1], TINT) | 0;
    const b = lerp(base, tinted[2], TINT) | 0;

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const w1 = 0.5 + 0.5 * Math.sin(col * 0.22 + row * 0.14 - wave * 0.7);
        const w2 = 0.5 + 0.5 * Math.sin(col * 0.11 - row * 0.18 - wave * 0.43);
        const mix = w1 * 0.6 + w2 * 0.4;
        ctx.globalAlpha = (0.02 + 0.40 * mix) * intensity;
        ctx.beginPath();
        ctx.arc(col * GAP, row * GAP, 0.55 + 0.45 * mix, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    ctx.globalAlpha = 1;
  }

  function frame(now) {
    const t = now || 0;
    const dt = last ? Math.min((t - last) / 1000, 0.1) : 0;
    last = t;

    if (!reduced.matches) {
      wave += dt * 0.66;          // the old canvas ran +0.011 a frame at 60fps
      clock += dt;
    }

    const nextP = nextProgress();
    let want = flatten(target, clock);
    if (nextP > 0) want = blend(want, flatten(nextPre, clock), nextP);

    let tweening = false;
    if (from) {
      const p = reduced.matches ? 1 : clamp01((t - started) / TWEEN);
      shown = p >= 1 ? want : blend(from, want, ease(p));
      tweening = p < 1;
      if (!tweening) from = null;
    } else {
      shown = want;
    }

    const near = presence(nextP);
    // Repainting a viewport-sized gradient is only worth it while something is
    // actually moving it; the ambient drift is slow enough to write at ~10fps.
    if (tweening || Math.abs(near - wroteNear) > 0.004 || t - wrote > 90) {
      apply(shown, near);
      wrote = t;
      wroteNear = near;
    }
    drawDots(shown, near);

    if (running) requestAnimationFrame(frame);
  }

  function start() {
    if (running) return;
    running = true;
    last = 0;
    requestAnimationFrame(frame);
  }

  function stop() {
    running = false;
    last = 0;
  }

  // Under reduced motion nothing animates on its own: the grid and glow are
  // drawn once, and again whenever the page (or the window) changes.
  function schedule() {
    if (reduced.matches) { stop(); requestAnimationFrame(frame); }
    else start();
  }

  /* ── Page changes ──
     app.js fires page:navigate with the incoming <main> before it swaps it in,
     so the background starts moving while the old content is still fading. */
  function retarget(el) {
    const next = presetFor(el);
    // Compared by value: page:navigate and page:load both land here for the
    // same page, and the second one mustn't restart the tween.
    if (String(flatten(next, 0)) === String(flatten(target, 0))) return;
    from = shown.slice();
    started = performance.now();
    target = next;
    schedule();
  }

  document.addEventListener('page:navigate', e => retarget(e.detail.main));
  document.addEventListener('page:load', e => {
    main = e.detail.main;
    retarget(main);
    bindNext();
    schedule();
  });

  new ResizeObserver(resize).observe(layer);
  darkQ.addEventListener('change', schedule);
  reduced.addEventListener('change', schedule);
  window.addEventListener('scroll', () => { if (!running) schedule(); }, { passive: true });

  bindNext();
  resize();
  schedule();
}());
