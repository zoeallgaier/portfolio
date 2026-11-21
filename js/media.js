/* media.js — gallery videos play only while they're on screen.

   Videos are written without `autoplay` and with preload="none", so a first
   visit downloads nothing but their posters (an autoplay attribute makes the
   browser fetch every clip up front, even ones far down the page). Each
   [data-autoplay] video starts when it nears the viewport and pauses when it
   leaves. Reduced motion keeps the poster; no-JS visitors get the poster too. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  const io = 'IntersectionObserver' in window && new IntersectionObserver(entries => {
    entries.forEach(({ target: v, isIntersecting }) => {
      if (isIntersecting && !reduced.matches) v.play().catch(() => {});
      else v.pause();
    });
  }, { rootMargin: '200px 0px' });

  // Run against whatever <main> is on screen: js/app.js swaps in a fresh one
  // on every route, so the old page's videos are let go first.
  const watched = new Set();

  function watch(root) {
    watched.forEach(v => {
      if (v.isConnected) return;
      if (io) io.unobserve(v);
      watched.delete(v);
    });
    root.querySelectorAll('video[data-autoplay]').forEach(v => {
      v.muted = true;  // the attribute alone doesn't satisfy every autoplay policy
      watched.add(v);
      if (io) io.observe(v);
      else if (!reduced.matches) v.play().catch(() => {});
    });
  }

  watch(document);
  document.addEventListener('page:load', e => watch(e.detail.main));
}());

/* Live before/after previews (uvu-web.html). Each framed page renders at a
   real device width (390px phone, 1440px laptop) and is scaled down to its
   bezel, so it lays out as it would on that device rather than squeezed.
   The Phone / Desktop switch starts on whichever the visitor is using. */
(function () {
  const WIDTH = { mobile: 390, desktop: 1440 };
  const onPhone = () =>
    (navigator.userAgentData ? navigator.userAgentData.mobile : /Mobi|Android|iPhone/i.test(navigator.userAgent)) ||
    window.matchMedia('(max-width: 768px)').matches;

  function fit(screen, view) {
    const frame = screen.querySelector('iframe');
    const s = screen.clientWidth / WIDTH[view];
    if (!frame || !s) return;  // still a poster: nothing to scale yet
    screen.style.setProperty('--s', s);
    frame.style.width = WIDTH[view] + 'px';
    frame.style.height = screen.clientHeight / s + 'px';
  }

  function wire(root) {
    root.querySelectorAll('.live-compare').forEach(section => {
      const screens = section.querySelectorAll('.live-phone');
      const buttons = section.querySelectorAll('.view-switch button');
      const fitAll = () => screens.forEach(el => fit(el, section.dataset.view));

      function setView(view) {
        section.dataset.view = view;
        buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === view)));
        fitAll();
      }

      buttons.forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
      section.addEventListener('live:mount', e => fit(e.target.closest('.live-phone'), section.dataset.view));
      const ro = new ResizeObserver(fitAll);
      screens.forEach(el => ro.observe(el));
      setView(onPhone() ? 'mobile' : 'desktop');
    });
  }

  wire(document);
  document.addEventListener('page:load', e => wire(e.detail.main));
}());

/* Click-to-play live screens (ylac.html, uvu-web.html). Each .live-poster is
   a screenshot linking to the live page. On a wider window a click swaps in
   the live page as an iframe right there; the poster stays on top until it
   has loaded. On a phone the link just opens the page full size, so a
   visitor never pays for a page they didn't ask for. One listener on the
   document covers every route js/app.js swaps in. */
(function () {
  const phone = window.matchMedia('(max-width: 768px)');

  function play(poster) {
    if (poster.classList.contains('is-loading')) return;
    const hadFocus = document.activeElement === poster;
    const frame = document.createElement('iframe');
    frame.src = poster.dataset.liveSrc;
    frame.title = poster.dataset.liveTitle || '';

    poster.classList.add('is-loading');
    poster.setAttribute('aria-disabled', 'true');
    const label = poster.querySelector('.live-play-full');
    if (label) label.textContent = 'Loading…';

    let done = false;
    const reveal = () => {
      if (done) return;
      done = true;
      poster.remove();
      if (hadFocus) frame.focus();
    };
    frame.addEventListener('load', reveal, { once: true });
    setTimeout(reveal, 12000);  // a slow page still shows up rather than hide forever

    poster.before(frame);
    frame.dispatchEvent(new CustomEvent('live:mount', { bubbles: true }));
  }

  document.addEventListener('click', e => {
    const poster = e.target.closest && e.target.closest('a.live-poster');
    if (!poster || phone.matches) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;  // let "open in new tab" work
    e.preventDefault();
    play(poster);
  });
}());

