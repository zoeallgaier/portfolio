(function () {

  /* —— App chrome —— Mobile top bar: monogram (→ portfolio) at top-left, level
     with the Menu toggle (js/chrome.js builds the shared nav). Shown on phones
     only (style.css); runs on feed + posts. */
  (function injectChrome() {
    const main = document.querySelector('main');
    if (main && !document.querySelector('.app-topbar')) {
      main.insertAdjacentHTML('beforebegin',
        '<header class="app-topbar">' +
          '<a class="nav-logo" href="/" aria-label="Zoe Allgaier — Home">' +
            '<img src="/icons/mono-dark.png" alt=""></a>' +
        '</header>');
    }
  }());

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

  /* —— Shared helpers (feed + Gallery) —— */
  // Cache-bust: SiteGround serves JSON with a long browser cache, so a fixed
  // URL would show returning visitors stale entries. A per-load timestamp makes
  // every fetch a fresh URL.
  const getJSON = url => fetch(url + '?t=' + Date.now())
    .then(r => { if (!r.ok) throw r.status; return r.json(); });

  // Noon, so the date never slips a day across time zones.
  const fmtDate = d => new Date(d + 'T12:00:00').toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric'
  });

  const newestFirst = (a, b) => new Date(b.date) - new Date(a.date);

  const escAttr = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

  // Natural size of an image, or null if the file is missing.
  const measure = src => new Promise(res => {
    const im = new Image();
    im.onload  = () => res(im.naturalWidth ? { w: im.naturalWidth, h: im.naturalHeight } : null);
    im.onerror = () => res(null);
    im.src = src;
  });

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
    // Hide the image until the new file is in, so the last photo opened
    // never flashes up first.
    const imgEl = lightboxEl.querySelector('img');
    imgEl.classList.remove('is-loaded');
    imgEl.onload = () => imgEl.classList.add('is-loaded');
    imgEl.alt = alt || '';
    imgEl.src = src;
    if (imgEl.complete && imgEl.naturalWidth) imgEl.classList.add('is-loaded');
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
    if (e.key === 'Tab') e.preventDefault();   // keep focus in the open viewer
  }

  // Click, Enter, or Space opens the image (or a larger file) in the lightbox.
  function makeZoomable(img, src) {
    const open = () => openLightbox(src || img.src, img.alt, img);
    img.addEventListener('click', open);
    img.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  }

  /* —— Photo gallery (Gallery page) —— Frames come from the JSON file named
     in #gallery's data-src, newest first, packed into three columns (each
     frame drops into the shortest one) so photos keep their own shape with no
     gaps. The date sits on the photo. Each frame zooms in the lightbox. A
     photo whose file is missing is skipped. —— */
  (function gallery() {
    const grid = document.getElementById('gallery');
    if (!grid) return;
    // Three columns, two on phones (same breakpoint as style.css). Crossing the
    // breakpoint re-packs the same frames.
    const phone = window.matchMedia('(max-width: 680px)');
    let frames = [];
    phone.addEventListener('change', () => pack(frames));

    function pack(list) {   // list: [{ el, ratio }]
      frames = list;
      grid.textContent = '';
      const cols = Array.from({ length: phone.matches ? 2 : 3 }, () => {
        const c = document.createElement('div');
        c.className = 'gallery-col';
        grid.appendChild(c);
        return { el: c, h: 0 };
      });
      frames.forEach(f => {
        const col = cols.reduce((min, c) => c.h < min.h ? c : min);
        col.el.appendChild(f.el);
        col.h += f.ratio;
      });
    }

    // No photos (or the JSON failed): blank frames keep the sheet's shape.
    function placeholders(n) {
      pack(Array.from({ length: n }, () => {
        const el = document.createElement('figure');
        el.className = 'frame frame--blank';
        el.setAttribute('aria-hidden', 'true');
        el.innerHTML = '<div class="frame-img"></div>';
        return { el, ratio: 0.75 };
      }));
    }

    function makeFrame(p, size, i) {
      const fig = document.createElement('figure');
      fig.className = 'frame';
      fig.style.animationDelay = Math.min(i * 0.05, 1).toFixed(2) + 's';

      // The grid shows the small thumb; the lightbox opens the full-size file.
      const img = document.createElement('img');
      img.className = 'frame-img';
      img.src = p.thumb || p.src;
      img.width = size.w;
      img.height = size.h;
      img.alt = p.alt || p.caption || '';
      img.decoding = 'async';
      img.tabIndex = 0;
      img.setAttribute('role', 'button');
      img.setAttribute('aria-label', 'Enlarge photo' + (img.alt ? ': ' + img.alt : ''));
      makeZoomable(img, p.src);
      fig.appendChild(img);

      const stamp = [p.caption, p.date && fmtDate(p.date)].filter(Boolean).join(' – ');
      if (stamp) {
        const cap = document.createElement('figcaption');
        cap.className = 'frame-date';
        cap.textContent = stamp;
        fig.appendChild(cap);
      }
      return fig;
    }

    getJSON(grid.dataset.src)
      .then(photos => {
        photos.sort(newestFirst);
        // Read each thumb's size first so the columns balance before anything shows.
        return Promise.all(photos.map(p => measure(p.thumb || p.src))).then(sizes => {
          const shown = photos.map((p, i) => ({ p, size: sizes[i] })).filter(x => x.size);
          if (!shown.length) return placeholders(9);
          pack(shown.map(({ p, size }, i) => ({ el: makeFrame(p, size, i), ratio: size.h / size.w })));
        });
      })
      .catch(() => placeholders(9));
  }());

  /* —— Feed (index only) —— */
  if (!document.getElementById('feed')) return;

  /* —— Filtering by type —— Each card's type word ("post", "find", …) is a
     link to ?filter=…, so tapping it narrows the board to that type, and a
     chip over the board names the filter and clears it. The board switches in
     place (no reload, no white flash) while ?filter= stays a real deep link
     via pushState; the type words on post pages simply navigate here. —— */
  const FILTERS = {            // ?filter= value → entry type + chip label
    posts:   { type: 'post',    label: 'Posts' },
    finds:   { type: 'find',    label: 'Finds' },
    library: { type: 'library', label: 'Library' },
    photos:  { type: 'photo',   label: 'Photos' },
  };
  const filterForType = type => Object.keys(FILTERS).find(f => FILTERS[f].type === type);
  const currentFilter = () => {
    const f = new URLSearchParams(location.search).get('filter');
    return FILTERS[f] ? f : null;
  };

  const feedEl = document.getElementById('feed');
  feedEl.insertAdjacentHTML('beforebegin',
    '<div class="feed-filter" hidden>' +
      '<button type="button" class="feed-filter-clear">' +
        '<span class="feed-filter-label"></span>' +
        '<span class="feed-filter-x" aria-hidden="true"></span>' +
      '</button>' +
    '</div>');
  const chip      = feedEl.previousElementSibling;
  const chipLabel = chip.querySelector('.feed-filter-label');
  chip.querySelector('button').addEventListener('click', () => setFilter(null));

  let activeFilter = currentFilter();

  function setFilter(f) {
    if (f === activeFilter) return;
    history.pushState({ filter: f }, '', f ? `?filter=${f}` : location.pathname);
    activeFilter = f;
    switchFeed(applyFilter);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Tapping the type of the filter you're already in goes back to everything.
  feedEl.addEventListener('click', e => {
    const link = e.target.closest('a.entry-type');
    if (!link) return;
    e.preventDefault();
    const f = new URL(link.href).searchParams.get('filter');
    setFilter(f === activeFilter ? null : f);
  });

  window.addEventListener('popstate', () => {
    activeFilter = currentFilter();
    switchFeed(applyFilter);
  });

  function applyFilter() {
    const type = activeFilter && FILTERS[activeFilter].type;
    entryEls.forEach(entry => { entry.hidden = !!type && entry.dataset.type !== type; });

    chip.hidden = !activeFilter;
    if (activeFilter) {
      chip.dataset.type = type;
      chipLabel.textContent = FILTERS[activeFilter].label;
      chip.querySelector('button').setAttribute('aria-label', `Showing ${FILTERS[activeFilter].label.toLowerCase()} — show all entries`);
    }

    renderColumns();   // re-flow the masonry over the now-visible cards
  }

  /* Cross-fade the board on a filter change: fade out, re-flow,
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
  // An entry with "gallery" (path to a photos JSON) takes that gallery's newest
  // photo as its card image, so the pinned Gallery card always shows the latest
  // shot. Its size is read first so the card holds its height from the start
  // (the masonry measures cards as soon as they're placed). A missing file falls
  // back to the next-newest photo; if none load, the card renders as text.
  async function galleryCover(photos) {
    for (const p of photos.slice().sort(newestFirst)) {
      const src  = p.thumb || p.src;
      const size = await measure(src);
      if (size) return { image: src, imageAlt: p.alt, imageSize: size };
    }
    return null;
  }

  function withGalleryCovers(data) {
    return Promise.all(data.map(item => !item.gallery ? item :
      getJSON(item.gallery)
        .then(galleryCover)
        .then(cover => cover ? { ...item, ...cover } : item)
        .catch(() => item)
    ));
  }

  getJSON('./content.json')
    .then(withGalleryCovers)
    .then(data => {
      // Pinned entries (the Gallery) always lead; the rest run newest first.
      data.sort((a, b) => (b.pinned === true) - (a.pinned === true) || newestFirst(a, b));
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

    const date = fmtDate(item.date);

    const el = document.createElement('article');
    el.className     = `entry entry--${item.type}`;
    el.dataset.type  = item.type;
    el.style.animationDelay = `${(i * 0.06).toFixed(2)}s`;

    // Title is optional (e.g. an image-only entry that just links out).
    const titleEl = !item.title ? ''
      : item.url
        ? `<a class="entry-title" href="${item.url}"` +
            (external ? ` target="_blank" rel="noopener noreferrer"` : '') +
          `>${item.title}</a>`
        : `<span class="entry-title entry-title--text">${item.title}</span>`;

    // Optional image on any entry: a link when there's a URL, otherwise a
    // zoomable photo (lightbox wired below). A known size (the Gallery cover)
    // keeps the photo's own shape instead of the square crop.
    let imgHtml = '';
    if (item.image) {
      const shape = item.imageSize
        ? ` width="${item.imageSize.w}" height="${item.imageSize.h}" ` +
          `style="aspect-ratio: ${item.imageSize.w} / ${item.imageSize.h}"`
        : '';
      const imgAttrs = `class="entry-image" loading="lazy" decoding="async" ` +
        `src="${escAttr(item.image)}" alt="${escAttr(item.imageAlt || item.note || item.title || '')}"` + shape;
      imgHtml = item.url
        ? `<a class="entry-image-link" href="${item.url}"` +
            (external ? ` target="_blank" rel="noopener noreferrer"` : '') +
          `><img ${imgAttrs}></a>`
        : `<img ${imgAttrs} tabindex="0" role="button" aria-label="Enlarge photo">`;
    }

    // Type reads as metadata, set in the date's line: "post – Nov 16, 2026".
    // Pinned cards (the Gallery) carry the date alone, no type word.
    const typeLabel = item.pinned ? '' : item.reading ? 'now reading' : item.type;

    const metaHtml =
      `<div class="entry-meta">` +
        (typeLabel
          ? `<a class="entry-type" href="?filter=${filterForType(item.type)}">${typeLabel}</a>` +
            `<span class="meta-sep" aria-hidden="true">–</span>`
          : '') +
        `<span class="entry-date">${date}</span>` +
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
        capHtml +
        metaHtml;
    } else if (item.image) {
      // Any entry with an image → full-bleed media tile: image fills the card,
      // and title + caption + meta overlay the bottom
      // over a scrim. Linked images (a url) navigate; bare ones (photos) zoom.
      el.classList.add('entry--media');
      if (item.gallery) el.classList.add('entry--gallery');
      el.innerHTML =
        `<div class="entry-media">` +
          imgHtml +
          `<div class="entry-media-overlay">` +
            titleEl +
            (item.note ? `<p class="entry-note">${item.note}</p>` : '') +
            metaHtml +
          `</div>` +
        `</div>`;
    } else {
      // Text post / find — source domain (finds) above the title.
      el.innerHTML =
        (domain ? `<div class="entry-header"><span class="entry-domain">${domain}</span></div>` : '') +
        titleEl +
        (item.note ? `<p class="entry-note">${item.note}</p>` : '') +
        metaHtml;
    }

    const img = el.querySelector('.entry-image');
    if (img && !img.closest('a')) makeZoomable(img);   // linked images navigate; only bare ones zoom

    return el;
  }

}());
