/* about.js: the About page's vertical curved reel and pinned copy column.

   Each .reel-item is placed on an arc by its distance from the viewport
   centre: as it scrolls away from the middle it tilts and slides sideways,
   the vertical version of a curved carousel. The arc's side alternates per
   item so the stack sways rather than leans. How far it bends is read from
   CSS (--arc-tilt, --arc-shift on .life-reel), so each breakpoint sets its
   own strength. Items spring in the first time they enter view.

   Works both ways onto the page: a full load, and js/app.js swapping <main>
   in (it loads this script the first time, then page:load re-wires it).
   Without JS the photos simply sit flat and full size: the spring-in only
   arms once .is-armed is on the reel. Reduced motion: none of the motion. */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  let items = [];
  let copy = null;
  let tiltMax = 0;
  let shiftMax = 0;
  let io = null;
  let ro = null;
  let frame = 0;
  let hold = 0;

  // Spring-in on first sight.
  function watch() {
    io?.disconnect();
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { threshold: 0.15 });
    items.forEach((el) => io.observe(el));
  }

  // Read every rect first, then write, so one frame costs one layout.
  // offsetWidth (not the rect's width) so an item's own tilt doesn't feed
  // back into its next shift; the rect's vertical centre is unaffected by
  // the rotate and translateX, so it's safe to read.
  function update() {
    frame = 0;
    if (!items.length || reduce.matches) return;
    const vh = window.innerHeight;
    const mid = vh / 2;
    const reads = items.map((el) => {
      const r = el.getBoundingClientRect();
      return { mid: r.top + r.height / 2, w: el.offsetWidth };
    });
    items.forEach((el, i) => {
      // -1 above centre, 0 at centre, 1 below; clamped past a viewport away
      const d = Math.max(-1.2, Math.min(1.2, (reads[i].mid - mid) / vh));
      const side = i % 2 ? -1 : 1;
      const tilt = d * tiltMax * side;
      const shift = (1 - Math.cos(d * Math.PI / 2)) * reads[i].w * shiftMax * side;
      el.style.setProperty('--tilt', tilt.toFixed(2) + 'deg');
      el.style.setProperty('--shift', shift.toFixed(1) + 'px');
    });
  }

  // The pinned copy column: if it's taller than the viewport, pin it with a
  // negative top so its last lines (signature, links) stay reachable. Re-run
  // whenever it changes size (late fonts, resizes, rotation).
  function pin() {
    if (!copy) return;
    const over = copy.offsetHeight - window.innerHeight;
    copy.style.setProperty('--pin-top', (over > 0 ? -over : 0) + 'px');
  }

  function measure(reel) {
    const cs = getComputedStyle(reel);
    tiltMax = parseFloat(cs.getPropertyValue('--arc-tilt')) || 0;
    shiftMax = parseFloat(cs.getPropertyValue('--arc-shift')) || 0;
  }

  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };

  function wire(root) {
    clearTimeout(hold);
    io?.disconnect();
    ro?.disconnect();
    const reel = root.querySelector('.life-reel');
    items = reel ? [...reel.querySelectorAll('.reel-item')] : [];
    copy = reel ? root.querySelector('.life-copy') : null;
    if (!reel) return;

    measure(reel);
    reel.classList.add('is-armed');
    // The reel fades in after the title (about.css); start the spring-in on
    // the same beat, or the first photos would finish springing unseen.
    clearTimeout(hold);
    hold = setTimeout(watch, (parseFloat(getComputedStyle(reel).animationDelay) || 0) * 1000);
    if (copy && 'ResizeObserver' in window) {
      ro = new ResizeObserver(pin);
      ro.observe(copy);
    }
    pin();
    update();
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', () => {
    const reel = items[0]?.parentElement;
    if (reel) measure(reel);
    pin();
    schedule();
  });
  reduce.addEventListener?.('change', schedule);
  document.addEventListener('page:load', (e) => wire(e.detail.main));

  wire(document.querySelector('main#main-content') || document);
})();
