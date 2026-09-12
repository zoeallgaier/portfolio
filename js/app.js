/* app.js — the portfolio as one long-lived page.

   Every page is still a complete, hand-written HTML document (deep links,
   search engines and no-JS visitors get exactly what they always did). On top
   of that this swaps <main> in place when you follow an internal link: the
   nav, the footer and js/backdrop.js's living background are never rebuilt, so
   navigating feels like moving inside an app rather than reloading a site.

   The order of a move:
     tap  → content blurs away (240ms) while the next page is fetched
          → backdrop starts easing to the new palette (page:navigate)
          → stylesheets swapped, <main> replaced, scroll set
          → content blurs back in (560ms) and page:load re-runs the enhancers.

   Anything this can't handle — a cross-origin link, a file, marginalia (its
   own app), a page with no <main>, a failed fetch — falls back to an ordinary
   full-page load, so a broken route is never a dead end. */
(function () {
  if (!document.querySelector('main#main-content')) return;
  if (!window.fetch || !window.DOMParser || !document.body.animate || !window.history.pushState) return;

  const OUT_MS = 240;
  const IN_MS  = 560;
  const BLUR   = '12px';

  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const contentEls = () =>
    [document.querySelector('main#main-content'), document.querySelector('footer')].filter(Boolean);

  // Browsers restore scroll on their own timing, which fights with swapping
  // content in; each history entry carries its own position instead.
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  /* ── Announcing the new page ──
     Nothing reloads, so assistive tech gets no page-change cue of its own. */
  const live = document.createElement('div');
  live.className = 'sr-only';
  live.setAttribute('aria-live', 'polite');
  live.setAttribute('aria-atomic', 'true');
  document.body.append(live);

  /* ── Fetching ── */
  const cache = new Map();

  // Keyed without the hash: /#work and / are the same document.
  function fetchDoc(url) {
    const href = url.origin + url.pathname + url.search;
    if (cache.has(href)) return cache.get(href);
    const job = fetch(href, { credentials: 'same-origin' })
      .then(res => {
        if (!res.ok) throw new Error(res.status);
        if (!(res.headers.get('content-type') || '').includes('text/html')) throw new Error('not html');
        return res.text();
      })
      .then(html => new DOMParser().parseFromString(html, 'text/html'))
      .catch(() => { cache.delete(href); return null; });
    cache.set(href, job);
    return job;
  }

  /* ── Which links this can take over ── */
  function routable(a) {
    if (!a || !a.getAttribute('href')) return false;
    if (a.hasAttribute('download') || (a.target && a.target !== '_self')) return false;
    if (a.dataset.route === 'off') return false;
    let url;
    try { url = new URL(a.href); } catch { return false; }
    if (url.origin !== location.origin) return false;
    // Pages only — never assets (the resume PDF, images), and never marginalia,
    // which is a separate app with its own renderer.
    if (!/(\.html|\/)$/.test(url.pathname)) return false;
    if (url.pathname.startsWith('/marginalia/')) return false;
    return true;
  }

  /* ── Stylesheets ──
     Each page brings its own (index.css, project.css, + about/resume). New
     ones are loaded before the swap so content never lands unstyled; the ones
     the next page doesn't want are dropped straight after, while it's hidden. */
  function syncStyles(doc, base) {
    const want = [...doc.querySelectorAll('head link[rel="stylesheet"]')]
      .map(l => new URL(l.getAttribute('href'), base).href);
    const have = new Map(
      [...document.querySelectorAll('head link[rel="stylesheet"]')].map(l => [l.href, l])
    );

    const pending = [];
    let prev = null;
    want.forEach(href => {
      let link = have.get(href);
      if (!link) {
        link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        pending.push(new Promise(done => {
          link.addEventListener('load', done, { once: true });
          link.addEventListener('error', done, { once: true });
        }));
        // Keep the cascade order the destination page declared (about.css and
        // resume.css both layer on top of index.css).
        if (prev && prev.parentNode) prev.after(link);
        else document.head.append(link);
      }
      prev = link;
    });

    const keep = new Set(want);
    return {
      ready: Promise.all(pending),
      drop: () => have.forEach((link, href) => { if (!keep.has(href)) link.remove(); }),
    };
  }

  /* ── The blur/fade ── */
  let playing = [];
  function fade(dir) {
    playing.forEach(a => a.cancel());
    const out = dir === 'out';
    const frames = out
      ? [{ opacity: 1, filter: 'blur(0px)',   transform: 'translateY(0)' },
         { opacity: 0, filter: `blur(${BLUR})`, transform: 'translateY(-10px)' }]
      : [{ opacity: 0, filter: `blur(${BLUR})`, transform: 'translateY(14px)' },
         { opacity: 1, filter: 'blur(0px)',   transform: 'translateY(0)' }];
    const opts = {
      duration: reduced() ? 1 : (out ? OUT_MS : IN_MS),
      easing: out ? 'cubic-bezier(0.4, 0, 1, 1)' : 'cubic-bezier(0.16, 1, 0.3, 1)',
      // Held on the way out so the old page stays hidden until it's replaced.
      fill: out ? 'forwards' : 'none',
    };
    playing = contentEls().map(el => el.animate(frames, opts));
    return Promise.all(playing.map(a => a.finished.catch(() => {})));
  }

  /* ── Scroll ── */
  function setScroll(url, y) {
    if (typeof y === 'number') return window.scrollTo({ top: y, behavior: 'instant' });
    if (url.hash) {
      const el = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (el) {
        const clear = parseFloat(getComputedStyle(el).scrollMarginTop) || 0;
        return window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - clear, behavior: 'instant' });
      }
    }
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  // Taking scroll restoration off the browser means handing back the one thing
  // it did for free: returning to where you were after a reload.
  window.addEventListener('load', () => {
    const y = history.state && history.state.y;
    if (y && !location.hash && window.scrollY === 0) window.scrollTo({ top: y, behavior: 'instant' });
  });

  // Remember where each entry was left, so Back returns you to the spot.
  let mark;
  window.addEventListener('scroll', () => {
    clearTimeout(mark);
    mark = setTimeout(() => {
      history.replaceState({ ...history.state, y: window.scrollY }, '');
    }, 180);
  }, { passive: true });

  /* ── A move ── */
  let seq = 0;

  async function navigate(href, opts) {
    const url = new URL(href, location.href);
    const token = ++seq;
    const job = fetchDoc(url);
    const leaving = fade('out');

    const doc = await job;
    if (token !== seq) return;                       // a newer tap took over
    const incoming = doc && doc.querySelector('main#main-content');
    if (!incoming) { location.href = url.href; return; }

    // Let the background start moving while the old content is still fading.
    document.dispatchEvent(new CustomEvent('page:navigate', { detail: { main: incoming, url } }));

    const styles = syncStyles(doc, url.href);
    await Promise.all([leaving, styles.ready]);
    if (token !== seq) return;

    if (opts.push) history.pushState({ y: 0 }, '', url.href);

    const next = document.importNode(incoming, true);
    document.querySelector('main#main-content').replaceWith(next);
    styles.drop();
    document.title = doc.title;
    setScroll(url, opts.y);

    document.dispatchEvent(new CustomEvent('page:load', { detail: { main: next, url } }));
    next.focus({ preventScroll: true });
    live.textContent = doc.title;
    fade('in');
  }

  /* ── Links ── */
  document.addEventListener('click', e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest('a[href]');
    if (!routable(a)) return;
    const url = new URL(a.href);
    if (url.pathname === location.pathname) {
      if (url.hash) return;                          // in-page anchor: not ours
      // Already here — behave like tapping the tab you're on.
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduced() ? 'instant' : 'smooth' });
      return;
    }
    e.preventDefault();
    navigate(url.href, { push: true });
  });

  window.addEventListener('popstate', e => {
    const y = e.state && typeof e.state.y === 'number' ? e.state.y : 0;
    navigate(location.href, { push: false, y });
  });

  // Warm the next page up on intent, so most taps have nothing left to wait for.
  const warm = e => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!routable(a)) return;
    const url = new URL(a.href);
    if (url.pathname !== location.pathname) fetchDoc(url);
  };
  document.addEventListener('pointerover', warm, { passive: true });
  document.addEventListener('touchstart', warm, { passive: true });
  document.addEventListener('focusin', warm);
}());
