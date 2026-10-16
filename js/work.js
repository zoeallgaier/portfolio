/* work.js — the home page's projects, one card at a time (css/index.css).

   Every project is a card that pins near the top of the screen while the
   next one slides up over it. This does two things on top of the CSS:
   - runs --cover 0 → 1 on a pinned card as the next one crosses it, so it
     eases back, dims and fades beneath it, then marks it .is-past once it's
     fully buried, hiding it so the browser stops painting it;
   - adds .is-in as a card first shows, so its pieces blur up in sequence
     (staggered with --d), then .is-done once they've landed, dropping the
     animations so no filter stays pinned on the type (WebKit clips its ink).
   Reduced motion keeps the pin and the hiding, and skips the motion. No JS:
   plain cards. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Mirrors the CSS: cards only pin on a desktop window tall enough to hold one.
  const stacked = window.matchMedia('(min-width: 769px) and (min-height: 621px)');

  let cards = [], io = null, ticking = false;

  // How far each card is buried: 0 until the next card starts to cross it,
  // 1 once that card has pinned on top of it.
  function cover() {
    ticking = false;
    const on = stacked.matches;
    cards.forEach((card, i) => {
      const next = cards[i + 1];
      let p = 0;
      if (on && next) {
        const gap = next.getBoundingClientRect().top - card.getBoundingClientRect().top;
        p = Math.min(1, Math.max(0, 1 - gap / card.offsetHeight));
      }
      // Reduced motion: no sink-back, but buried cards still drop out.
      if (!reduced) card.style.setProperty('--cover', p.toFixed(3));
      card.classList.toggle('is-past', p >= 1);
    });
  }
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(cover); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  // Run against whatever <main> is on screen: js/app.js swaps in a fresh one
  // on every route.
  function build(root) {
    if (io) { io.disconnect(); io = null; }
    const stack = root.querySelector('.stack');
    cards = stack ? [...stack.querySelectorAll('.card')] : [];
    if (!stack) return;

    cards.forEach(card => {
      // The entrance order: image, then role, title, summary, each result.
      card.querySelectorAll('.card-role, .card-title, .card-summary, .card-results li')
        .forEach((el, k) => el.style.setProperty('--d', (0.12 + k * 0.07).toFixed(2) + 's'));
    });
    onScroll();

    if (reduced || !('IntersectionObserver' in window)) return;
    stack.classList.add('is-armed');
    io = new IntersectionObserver(entries => {
      entries.forEach(({ target: card, isIntersecting }) => {
        if (!isIntersecting) return;
        io.unobserve(card);
        card.classList.add('is-in');
        setTimeout(() => card.classList.add('is-done'), 1900);
      });
    }, { rootMargin: '0px 0px -18% 0px' });
    cards.forEach(card => io.observe(card));
  }

  build(document);
  document.addEventListener('page:load', e => build(e.detail.main));
}());
