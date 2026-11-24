/* figures.js — the "By the numbers" row on the home page counts up from zero
   the first time it scrolls into view, left to right.

   The HTML holds the real figures ($1.38M, +147%…), so no-JS and reduced-motion
   visitors simply read them. Each figure keeps its own prefix, suffix and
   decimal places all the way up, so "$792.3K" climbs as $0.0K → $792.3K and
   never changes shape mid-count. The curve is --ease-chrome (css/base.css):
   a quick start that settles slowly, so the last digits ease into place. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !('IntersectionObserver' in window)) return;

  const DURATION = 1600;  // ms per figure
  const STAGGER  = 120;   // ms between neighbouring figures
  const ease = getComputedStyle(document.documentElement)
    .getPropertyValue('--ease-chrome').trim() || 'ease-out';

  // "$1.38M" → { prefix: "$", value: 1.38, places: 2, suffix: "M" }
  function parse(text) {
    const m = text.trim().match(/^([^\d]*)([\d,]*\.?\d+)(.*)$/);
    if (!m) return null;
    const digits = m[2].replace(/,/g, '');
    return {
      prefix: m[1],
      value: parseFloat(digits),
      places: (digits.split('.')[1] || '').length,
      suffix: m[3],
    };
  }

  const format = (f, n) => f.prefix + n.toFixed(f.places) + f.suffix;

  // Timing comes from a target-less KeyframeEffect, so the browser applies
  // the CSS easing and delay itself; each frame just reads its progress.
  function count(el, f, delay) {
    const effect = new KeyframeEffect(null, null,
      { duration: DURATION, delay, easing: ease, fill: 'both' });
    const anim = new Animation(effect, document.timeline);
    const tick = () => {
      const p = effect.getComputedTiming().progress ?? 1;
      el.textContent = format(f, f.value * p);
      if (anim.playState !== 'finished') requestAnimationFrame(tick);
    };
    // Land on the exact authored string, whatever rounding did on the way.
    anim.finished.then(() => { el.textContent = f.text; });
    anim.play();
    requestAnimationFrame(tick);
  }

  // Run against whatever <main> is on screen: js/app.js swaps in a fresh one
  // on every route, so the old page's observer is let go first.
  let io = null;

  function wire(root) {
    if (io) io.disconnect();
    const row = root.querySelector('.figures');
    if (!row) return;

    // The authored figure is kept on the element, so wiring the same <main>
    // twice never mistakes a parked "$0.00M" for the target.
    const nums = [...row.querySelectorAll('.figure-num')]
      .map(el => {
        el.dataset.figure ??= el.textContent.trim();
        const f = parse(el.dataset.figure);
        if (f) f.text = el.dataset.figure;
        return { el, f };
      })
      .filter(({ f }) => f);
    if (!nums.length) return;

    // Park each figure at zero before it's seen.
    nums.forEach(({ el, f }) => { el.textContent = format(f, 0); });

    io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      io.disconnect();
      io = null;
      nums.forEach(({ el, f }, i) => count(el, f, i * STAGGER));
    }, { rootMargin: '0px 0px -15% 0px' });
    io.observe(row);
  }

  wire(document);
  document.addEventListener('page:load', e => wire(e.detail.main));
}());
