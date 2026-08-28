(function () {

  /* —— App chrome —— Mobile top bar: monogram (→ portfolio) at top-left; the
     bottom bar stays nav-only. Shown per-context via CSS; runs on feed + posts. */
  (function injectChrome() {
    const main = document.querySelector('main');
    if (main && !document.querySelector('.app-topbar')) {
      main.insertAdjacentHTML('beforebegin',
        '<header class="app-topbar">' +
          '<a class="nav-logo" href="/" aria-label="Zoe Allgaier — Home">' +
            '<img src="/Zmono-dark.png" alt=""></a>' +
        '</header>');
    }
  }());

  /* —— Header height sync —— On desktop the top nav is fixed, so offset main by
     its height. On phones the nav is the bottom tab bar and the top bar scrolls
     in-flow, so main needs no top offset (CSS handles it). —— */
  (function syncHeader() {
    const nav  = document.querySelector('nav');
    const main = document.querySelector('main');
    if (!nav || !main) return;
    const mobile = window.matchMedia('(max-width: 680px)');
    function apply() {
      main.style.paddingTop = mobile.matches ? '' : nav.offsetHeight + 'px';
    }
    new ResizeObserver(apply).observe(nav);
    mobile.addEventListener('change', apply);
    apply();
  }());

  const urlParams = new URLSearchParams(window.location.search);
  const urlFilter = urlParams.get('filter');

  /* —— Nav tab icons —— Inject a small line icon into each filter tab so the
     mobile bottom bar reads as a native app tab bar. Shown only on phones (CSS);
     runs on the feed and on post pages, which share this nav. —— */
  (function navIcons() {
    const ICONS = {
      all:     '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
      posts:   '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5Z"/>',
      finds:   '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
      photos:  '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.6"/><path d="m21 15-5-5L5 21"/>',
      library: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>'
    };
    document.querySelectorAll('.nav-links a').forEach(a => {
      const key = new URL(a.href, location.href).searchParams.get('filter') || 'all';
      if (!ICONS[key]) return;
      a.insertAdjacentHTML('afterbegin',
        '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
        'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        ICONS[key] + '</svg>');
    });
  }());

  /* —— Active nav link —— */
  function updateActiveNav(filter) {
    filter = filter || null;
    document.querySelectorAll('.nav-links a').forEach(link => {
      const linkUrl    = new URL(link.href, location.href);
      const linkFilter = linkUrl.searchParams.get('filter') || null;
      const samePath   = linkUrl.pathname.replace(/\/$/, '') === location.pathname.replace(/\/$/, '');
      if (samePath && linkFilter === filter) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }
  updateActiveNav(urlFilter);

  /* —— Post body: blur-in the whole post on load, cascading in after the title.
     One pass (no scroll observer) to stay light on small devices. —— */
  (function revealPostBody() {
    const body = document.querySelector('.post-body');
    if (!body) return;
    const items   = [...body.children];
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    items.forEach((el, i) => {
      // Start after the header cascade (~0.5s), then stagger — capped so a long
      // post never leaves a block waiting too long.
      if (!reduced) el.style.animationDelay = Math.min(0.5 + i * 0.08, 1.5).toFixed(2) + 's';
      el.classList.add('is-revealed');
    });
  }());

  /* —— Feed (index only) —— */
  if (!document.getElementById('feed')) return;

  const typeForFilter = f =>
    f === 'posts'   ? 'post'    :
    f === 'finds'   ? 'find'    :
    f === 'library' ? 'library' :
    f === 'photos'  ? 'photo'   : 'all';

  let activeTag  = null;
  let activeType = typeForFilter(urlFilter);

  /* —— In-page filtering —— The top filter tabs switch the feed without a full
     page reload (no white flash — feels like an app), while keeping ?filter=
     deep links via pushState. Tapping the tab you're already on scrolls the feed
     back to the top (native tab-bar gesture). —— */
  const currentFilter = () => new URLSearchParams(location.search).get('filter') || null;

  document.querySelectorAll('.nav-links a').forEach(a => {
    const linkUrl  = new URL(a.href, location.href);
    const samePath = linkUrl.pathname.replace(/\/$/, '') === location.pathname.replace(/\/$/, '');
    if (!samePath) return;                    // links that leave the feed navigate normally
    a.addEventListener('click', e => {
      e.preventDefault();
      const f = linkUrl.searchParams.get('filter') || null;
      if (f === currentFilter()) { window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
      history.pushState({ filter: f }, '', a.getAttribute('href'));
      activeType = typeForFilter(f);
      activeTag  = null;
      updateActiveNav(f);
      switchFeed(applyFilter);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  window.addEventListener('popstate', () => {
    const f = currentFilter();
    activeType = typeForFilter(f);
    activeTag  = null;
    updateActiveNav(f);
    switchFeed(applyFilter);
  });

  function applyFilter() {
    entryEls.forEach(entry => {
      const typeOk = activeType === 'all' || entry.dataset.type === activeType;
      const tags   = entry.dataset.tags ? entry.dataset.tags.split(',') : [];
      const tagOk  = !activeTag || tags.includes(activeTag);
      entry.hidden = !(typeOk && tagOk);
    });

    document.querySelectorAll('.tag').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tag === activeTag);
    });

    renderColumns();   // re-flow the masonry over the now-visible cards
  }

  /* Cross-fade the board on a filter change (tab or tag): fade out, re-flow,
     fade back — softer than an instant snap. Skipped under reduced motion. */
  function switchFeed(mutate) {
    const feed    = document.getElementById('feed');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!feed || reduced) { mutate(); return; }
    feed.classList.add('is-switching');
    setTimeout(() => {
      mutate();
      requestAnimationFrame(() => feed.classList.remove('is-switching'));
    }, 160);
  }

  /* —— Masonry board —— */
  let entryEls = [];
  let colCount = 0;

  function columnsForWidth(w) {
    return Math.max(1, Math.min(3, Math.floor(w / 420)));
  }

  /* Distribute the currently-visible cards into N columns, always appending
     to the shortest one (Pinterest-style) so every column fills from the top. */
  function renderColumns() {
    const feed = document.getElementById('feed');
    if (!feed || !entryEls.length) return;
    colCount = columnsForWidth(feed.clientWidth);
    feed.textContent = '';
    const cols = [];
    for (let i = 0; i < colCount; i++) {
      const c = document.createElement('div');
      c.className = 'feed-col';
      feed.appendChild(c);
      cols.push(c);
    }
    entryEls.filter(el => !el.hidden).forEach(el => {
      let min = 0;
      for (let i = 1; i < cols.length; i++) {
        if (cols[i].offsetHeight < cols[min].offsetHeight) min = i;
      }
      cols[min].appendChild(el);
    });
  }

  /* Resize: only re-flow when the column count actually changes. */
  function layoutFeed() {
    const feed = document.getElementById('feed');
    if (!feed || !entryEls.length) return;
    if (columnsForWidth(feed.clientWidth) === colCount && feed.children.length) return;
    renderColumns();
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(layoutFeed, 150);
  });

  /* Load entries */
  // Cache-bust: SiteGround serves content.json with a long browser cache, so a
  // fixed URL would show returning visitors stale posts. A per-load timestamp
  // makes every fetch a fresh URL — the feed is always current.
  fetch('./content.json?t=' + Date.now())
    .then(r => { if (!r.ok) throw r.status; return r.json(); })
    .then(data => {
      data.sort((a, b) => new Date(b.date) - new Date(a.date));
      entryEls = data.map((item, i) => makeEntry(item, i));
      applyFilter();   // sets visibility, then renders the masonry
    })
    .catch(() => {
      document.getElementById('feed').innerHTML =
        '<p class="feed-error">Could not load entries. If opening as a local file in Firefox, run via a local server instead.</p>';
    });

  function makeEntry(item, i) {
    const isFind    = item.type === 'find';
    const isLibrary = item.type === 'library';
    const external  = /^https?:\/\//.test(item.url || '');
    let domain = '';
    if (isFind && item.url) {
      try { domain = new URL(item.url).hostname.replace(/^www\./, ''); } catch {}
    }

    const date = new Date(item.date + 'T12:00:00').toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric'
    });
    const tags = item.tags || [];

    const el = document.createElement('article');
    el.className     = `entry entry--${item.type}`;
    el.dataset.type  = item.type;
    el.dataset.tags  = tags.join(',');
    el.style.animationDelay = `${(i * 0.06).toFixed(2)}s`;

    // Title is optional (e.g. an image-only entry that just links out).
    const titleEl = !item.title ? ''
      : item.url
        ? `<a class="entry-title" href="${item.url}"` +
            (external ? ` target="_blank" rel="noopener noreferrer"` : '') +
          `>${item.title}</a>`
        : `<span class="entry-title entry-title--text">${item.title}</span>`;

    // Optional image on any entry: a link when there's a URL, otherwise a
    // zoomable photo (lightbox wired below).
    let imgHtml = '';
    if (item.image) {
      const imgAttrs = `class="entry-image" loading="lazy" decoding="async" ` +
        `src="${item.image}" alt="${(item.note || item.title || '').replace(/"/g, '&quot;')}"`;
      imgHtml = item.url
        ? `<a class="entry-image-link" href="${item.url}"` +
            (external ? ` target="_blank" rel="noopener noreferrer"` : '') +
          `><img ${imgAttrs}></a>`
        : `<img ${imgAttrs} tabindex="0" role="button" aria-label="Enlarge photo">`;
    }

    const badge = item.reading ? 'now reading' : isLibrary ? 'library' : item.type;

    const metaHtml =
      `<div class="entry-meta">` +
        `<span class="entry-date">${date}</span>` +
        (tags.length
          ? `<div class="tags">${tags.map(t =>
              `<button class="tag" type="button" data-tag="${t}">${t}</button>`
            ).join('')}</div>`
          : '') +
      `</div>`;

    if (isLibrary) {
      // Caption-only: italic book title (proper convention for a title) + author.
      const cap = (item.title ? `<i class="entry-cap-title">${item.title}</i>` : '') +
                  (item.title && item.note ? ', ' : '') +
                  (item.note || '');
      const capHtml = item.url
        ? `<a class="entry-caption" href="${item.url}"` +
            (external ? ` target="_blank" rel="noopener noreferrer"` : '') +
          `>${cap}</a>`
        : `<p class="entry-caption">${cap}</p>`;
      el.innerHTML =
        `<div class="entry-header">` +
          `<span class="entry-badge">${badge}</span>` +
        `</div>` +
        capHtml +
        metaHtml;
    } else if (item.image) {
      // Any entry with an image → full-bleed media tile: image fills the card,
      // badge rides on the image, and title + caption + meta overlay the bottom
      // over a scrim. Linked images (a url) navigate; bare ones (photos) zoom.
      el.classList.add('entry--media');
      el.innerHTML =
        `<div class="entry-media">` +
          imgHtml +
          `<span class="entry-badge">${badge}</span>` +
          `<div class="entry-media-overlay">` +
            titleEl +
            (item.note ? `<p class="entry-note">${item.note}</p>` : '') +
            metaHtml +
          `</div>` +
        `</div>`;
    } else {
      // Text post / find — badge kicker above the title.
      el.innerHTML =
        `<div class="entry-header">` +
          `<span class="entry-badge">${badge}</span>` +
          (domain ? `<span class="entry-domain">${domain}</span>` : '') +
        `</div>` +
        titleEl +
        (item.note ? `<p class="entry-note">${item.note}</p>` : '') +
        metaHtml;
    }

    el.querySelectorAll('.tag').forEach(btn =>
      btn.addEventListener('click', () => {
        activeTag = activeTag === btn.dataset.tag ? null : btn.dataset.tag;
        switchFeed(applyFilter);
      })
    );

    const img = el.querySelector('.entry-image');
    if (img && !img.closest('a')) {   // linked images navigate; only bare ones zoom
      img.addEventListener('click', () => openLightbox(img.src, img.alt, img));
      img.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(img.src, img.alt, img); }
      });
    }

    return el;
  }

  /* —— Lightbox (photo zoom) —— */
  let lightboxEl = null;
  let lightboxReturnFocus = null;

  function openLightbox(src, alt, trigger) {
    lightboxReturnFocus = trigger || null;
    if (!lightboxEl) {
      lightboxEl = document.createElement('div');
      lightboxEl.className = 'lightbox';
      lightboxEl.setAttribute('role', 'dialog');
      lightboxEl.setAttribute('aria-modal', 'true');
      lightboxEl.setAttribute('aria-label', 'Photo viewer');
      lightboxEl.tabIndex = -1;
      lightboxEl.innerHTML = '<img alt="">';
      lightboxEl.addEventListener('click', closeLightbox);
      document.body.appendChild(lightboxEl);
    }
    const imgEl = lightboxEl.querySelector('img');
    imgEl.src = src;
    imgEl.alt = alt || '';
    lightboxEl.classList.add('is-open');
    lightboxEl.focus();
    document.addEventListener('keydown', onLightboxKey);
  }

  function closeLightbox() {
    if (!lightboxEl) return;
    lightboxEl.classList.remove('is-open');
    document.removeEventListener('keydown', onLightboxKey);
    if (lightboxReturnFocus) lightboxReturnFocus.focus();
    lightboxReturnFocus = null;
  }

  function onLightboxKey(e) {
    if (e.key === 'Escape') closeLightbox();
  }

}());
