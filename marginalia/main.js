(function () {

  /* —— Header height sync —— */
  (function syncHeader() {
    const header = document.querySelector('nav');
    const main   = document.querySelector('main');
    if (!header || !main) return;
    function apply() { main.style.paddingTop = header.offsetHeight + 'px'; }
    new ResizeObserver(apply).observe(header);
    apply();
  }());

  const urlParams = new URLSearchParams(window.location.search);
  const urlFilter = urlParams.get('filter');

  /* —— Active nav link —— */
  (function setActiveNav() {
    const filter = urlFilter || null;
    document.querySelectorAll('.nav-links a').forEach(link => {
      const linkUrl    = new URL(link.href, location.href);
      const linkFilter = linkUrl.searchParams.get('filter') || null;
      const samePath   = linkUrl.pathname.replace(/\/$/, '') === location.pathname.replace(/\/$/, '');
      if (samePath && linkFilter === filter) link.setAttribute('aria-current', 'page');
    });
  }());

  /* —— Feed (index only) —— */
  if (!document.getElementById('feed')) return;

  let activeType = 'all';
  let activeTag  = null;

  if (urlFilter === 'posts') activeType = 'post';
  else if (urlFilter === 'finds') activeType = 'find';
  else if (urlFilter === 'library') activeType = 'library';
  else if (urlFilter === 'photos') activeType = 'photo';

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
      // Compact row: title and author/year share a single line.
      el.innerHTML =
        `<div class="entry-header">` +
          `<span class="entry-badge">${badge}</span>` +
        `</div>` +
        `<div class="entry-libline">` +
          titleEl +
          (item.note ? `<span class="entry-author">${item.note}</span>` : '') +
        `</div>` +
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
        applyFilter();
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
