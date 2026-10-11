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
