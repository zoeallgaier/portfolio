/* carousel.js — the home page's work as a curved, endless reel.

   The cards ride the rim of a large wheel whose hub sits far below the page:
   the centred card stands upright and its neighbours tilt and dip away as they
   travel round. The strip loops, so there's no first or last card.

   Motion
     One critically damped spring drives every settle. It starts from whatever
     speed the reel already has, so a released swipe carries straight on at the
     finger's speed and slows onto a card in one unbroken curve; from rest it
     eases in instead of lurching. It never overshoots and never bounces.

   Input
     drag / swipe   follows the finger 1:1; on release it's thrown on with the
                    finger's speed and lands on the card nearest where that
                    throw would coast to
     tap            on a side card brings it to centre; on the centre card
                    opens it; a tap while the reel is moving just stops it
     trackpad       horizontal two-finger scroll moves it; as soon as macOS's
                    inertia takes over it lands on a card, rather than waiting
                    for the inertia to die and then moving again
     keyboard       ←/→ step a card; tabbing to a card brings it to centre

   Vertical scrolling is never taken over: touch-action: pan-y hands vertical
   swipes to the page, and a vertical wheel gesture is left alone from start to
   finish.

   Without JS .work is the ordinary 2-column grid; .is-reel switches the
   layout over (css/index.css). Re-wires on page:load, since app.js swaps
   <main> in place. */
(function () {
  const ANGLE = 9 * Math.PI / 180;  // tilt between neighbouring cards
  const SETTLE = 11;                // spring rate (1/s) for landing on a card
  const FOLLOW = 38;                // stiffer spring while a trackpad drives it
  const THROW = 2.2;                // a release coasts THROW·v/SETTLE px
  const NUDGE = 0.12;               // share of a card a drag needs to move one
  const MAX_SKIP = 4;               // a hard throw travels at most this many cards
  const DRAG_START = 6;             // px before a press becomes a drag
  const WHEEL_GAP = 180;            // ms of wheel silence that ends a gesture

  let teardown = null;

  function wire(scope) {
    if (teardown) { teardown(); teardown = null; }
    const root = scope.querySelector('.work');
    if (!root) return;
    const slides = [...root.querySelectorAll(':scope > .work-item')];
    const n = slides.length;
    if (n < 3) return;

    const ac = new AbortController();
    const on = (t, type, fn, opts) => t.addEventListener(type, fn, { ...opts, signal: ac.signal });
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

    root.classList.add('is-reel');
    root.setAttribute('aria-roledescription', 'carousel');

    let step = 1;        // card width + gap, px
    let offset = 0;      // px travelled; card i is centred when offset = i * step
    let vel = 0;         // px/s
    let target = 0;
    let rate = SETTLE;
    let raf = 0;
    let last = 0;
    const drag = { pending: false, active: false, caught: false, mouse: false, id: 0, x0: 0, y0: 0, o0: 0, samples: [] };

    const nearest = v => Math.round(v / step) * step;
    const indexAt = v => ((Math.round(v / step) % n) + n) % n;
    const moving = () => raf !== 0 && (Math.abs(vel) > 30 || Math.abs(target - offset) > 2);

    // Roving tabindex: only the card settling at centre is a Tab stop, so Tab
    // enters on a card that's on screen (never one round the back of the
    // wheel, which would make the page jump to it) and the next Tab leaves.
    let current = -1;
    function setCurrent(i) {
      if (i === current) return;
      current = i;
      slides.forEach((s, j) => { s.tabIndex = j === i ? 0 : -1; });
    }

    function measure() {
      const old = step;
      const gap = parseFloat(getComputedStyle(root).columnGap) || 0;
      step = slides[0].offsetWidth + gap || 1;
      // Keep the same card centred, and the same motion, across a resize.
      const k = step / old;
      offset *= k; target *= k; vel *= k; drag.o0 *= k;
      render();
    }

    // Cards further than PARK places from centre are off screen at every
    // width. They wait at that spot, hidden, rather than carrying on round
    // the wheel: further round they'd hang a thousand px and more below the
    // reel, and since the reel only clips sideways, they'd stretch the page
    // into a long blank run after the footer.
    const PARK = 2.6;
    const z = new Array(n).fill('');
    const shown = new Array(n).fill(true);
    function render() {
      const total = n * step;
      const R = step / ANGLE;
      for (let i = 0; i < n; i++) {
        let x = i * step - offset;
        x -= total * Math.round(x / total);          // loop: the copy nearest centre
        const u = Math.max(-PARK, Math.min(PARK, x / step));
        const a = u * ANGLE;
        const s = slides[i].style;
        s.transform = `translate3d(${(R * Math.sin(a)).toFixed(2)}px, ${(R * (1 - Math.cos(a))).toFixed(2)}px, 0) rotate(${a.toFixed(5)}rad)`;
        const zi = String(n - Math.round(Math.abs(x / step)));
        if (zi !== z[i]) { s.zIndex = zi; z[i] = zi; }
        const show = Math.abs(u) < PARK;
        if (show !== shown[i]) { s.visibility = show ? '' : 'hidden'; shown[i] = show; }
      }
    }

    // Exact step of a critically damped spring, so it behaves the same at
    // 60Hz, 120Hz or after a dropped frame.
    function spring(dt) {
      const w = reduced.matches ? Math.max(rate, 40) : rate;
      const x = offset - target;
      const c = vel + w * x;
      const e = Math.exp(-w * dt);
      offset = target + (x + c * dt) * e;
      vel = (c - w * (x + c * dt)) * e;
      if (Math.abs(offset - target) < 0.25 && Math.abs(vel) < 8) { offset = target; vel = 0; }
    }

    function tick(now) {
      const dt = Math.min((now - last) / 1000, 0.064);
      last = now;
      if (!drag.active && !drag.caught) spring(dt);
      render();
      const busy = drag.active || drag.caught || offset !== target || vel !== 0;
      raf = busy ? requestAnimationFrame(tick) : 0;
    }

    function run() {
      if (raf) return;
      last = performance.now();
      raf = requestAnimationFrame(tick);
    }

    // Land on card `to`, carrying the current speed into it. Speed toward the
    // card is capped at what the spring can absorb without overshooting.
    function landOn(to, r = SETTLE) {
      rate = r;
      target = to * step;
      const x = target - offset;
      if (r === SETTLE && Math.sign(vel) === Math.sign(x)) {
        vel = Math.sign(vel) * Math.min(Math.abs(vel), r * Math.abs(x));
      }
      setCurrent(((to % n) + n) % n);
      run();
    }

    // Where a motion that started at card `from` should end, given where its
    // momentum would carry it: the nearest card to that point, but at least
    // one card on when it was clearly pushed, and no more than MAX_SKIP.
    function landing(from, projected, pushed) {
      let to = Math.round(projected / step);
      if (to === from && Math.abs(pushed) > step * NUDGE) to += Math.sign(pushed);
      return Math.max(from - MAX_SKIP, Math.min(from + MAX_SKIP, to));
    }

    // Centre card i, taking the short way round the loop.
    function centreOn(i) {
      const total = n * step;
      let d = i * step - target;
      d -= total * Math.round(d / total);
      landOn(Math.round((target + d) / step));
    }

    /* ── Drag / swipe ── */
    let suppressClick = false;

    on(root, 'pointerdown', e => {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      suppressClick = false;
      // Pressing a moving reel catches it where it is, the way a scroll view
      // stops under a finger. That press is a stop, not a tap on a card.
      const caught = moving();
      if (caught) { target = offset; vel = 0; }
      Object.assign(drag, {
        pending: true, active: false, caught, mouse: e.pointerType === 'mouse',
        id: e.pointerId, x0: e.clientX, y0: e.clientY, samples: [],
      });
    });

    on(root, 'pointermove', e => {
      if (e.pointerId !== drag.id || !drag.pending) return;
      if (!drag.active) {
        const dx = e.clientX - drag.x0;
        const dy = e.clientY - drag.y0;
        if (Math.abs(dx) < DRAG_START && Math.abs(dy) < DRAG_START) return;
        // A mostly vertical swipe belongs to the page. (A mouse can't scroll
        // the page by dragging, so it only needs to move sideways enough.)
        if (drag.mouse ? Math.abs(dx) < DRAG_START : Math.abs(dy) > Math.abs(dx)) {
          if (!drag.mouse) drag.pending = false;
          return;
        }
        drag.active = true;
        drag.x0 = e.clientX;            // start here, so it doesn't jump by the threshold
        drag.o0 = offset;
        root.classList.add('is-dragging');
        try { root.setPointerCapture(e.pointerId); } catch (_) { /* pointer already gone */ }
        run();
      }
      offset = target = drag.o0 - (e.clientX - drag.x0);
      const now = performance.now();
      drag.samples.push({ t: now, x: e.clientX });
      while (drag.samples.length > 2 && now - drag.samples[0].t > 80) drag.samples.shift();
    });

    function release(e) {
      if (e.pointerId !== drag.id || (!drag.pending && !drag.active && !drag.caught)) return;
      const wasCaught = drag.caught;
      drag.pending = drag.caught = false;
      if (!drag.active) {
        if (wasCaught) { suppressClick = true; landOn(Math.round(offset / step)); }
        return;
      }
      drag.active = false;
      suppressClick = true;
      root.classList.remove('is-dragging');

      // The finger's speed over its last few moves, px/s along the strip.
      // A finger that stopped before lifting throws nothing.
      vel = 0;
      const s = drag.samples;
      if (s.length > 1) {
        const a = s[0], b = s[s.length - 1];
        if (performance.now() - b.t < 60 && b.t > a.t) vel = -(b.x - a.x) / (b.t - a.t) * 1000;
      }
      const from = Math.round(drag.o0 / step);
      landOn(landing(from, offset + vel * THROW / SETTLE, offset - drag.o0));
    }
    on(root, 'pointerup', release);
    on(root, 'pointercancel', release);

    on(root, 'click', e => {
      // A drag, or a press that stopped the reel, mustn't also open a card
      // (app.js honours defaultPrevented).
      if (suppressClick) {
        suppressClick = false;
        e.preventDefault();
        e.stopPropagation();
        return;
      }
      // A side card comes to centre first; the centred one opens. Modified
      // clicks (new tab, etc.) always go through.
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const i = slides.indexOf(e.target.closest('.work-item'));
      if (i < 0 || i === indexAt(target)) return;
      e.preventDefault();
      e.stopPropagation();
      centreOn(i);
    }, { capture: true });

    on(root, 'dragstart', e => e.preventDefault());

    /* ── Trackpad / shift-wheel ──
       Each gesture keeps the axis it started on, so a sideways swipe that
       wobbles never leaks into a page scroll (and a vertical scroll never
       nudges the reel). The reel follows the deltas on a stiff spring; once
       the deltas start dying away on their own (fingers lifted, macOS inertia
       coasting) it lands on the card that inertia would have reached and
       ignores the rest of it. Wheels without inertia land after a pause. */
    const wheel = { t: 0, axis: '', last: 0, falls: 0, peak: 0, ratio: 0.9, from: 0, start: 0, locked: false, idle: 0 };

    function wheelLand(projected) {
      wheel.locked = true;
      landOn(landing(wheel.from, projected, projected - wheel.start));
    }

    on(root, 'wheel', e => {
      const now = performance.now();
      if (now - wheel.t > WHEEL_GAP) {
        Object.assign(wheel, { axis: '', last: 0, falls: 0, peak: 0, ratio: 0.9, locked: false });
      }
      wheel.t = now;
      if (!wheel.axis) {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
          wheel.axis = 'x';
          wheel.from = Math.round(target / step);
          wheel.start = target;
        } else if (e.deltaY) {
          wheel.axis = 'y';
        }
      }
      if (wheel.axis !== 'x') return;
      e.preventDefault();
      if (drag.active) return;

      const unit = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? root.clientWidth : 1;
      const d = e.deltaX * unit;
      const size = Math.abs(d);
      clearTimeout(wheel.idle);

      if (wheel.locked) {
        // Still inertia: swallow it. A fresh push (deltas growing again) means
        // the fingers are back, so hand the reel back to them.
        if (!(size > wheel.last * 1.5 && size > 4)) { wheel.last = size; return; }
        Object.assign(wheel, { locked: false, falls: 0, peak: 0, from: Math.round(target / step), start: target });
      }

      if (wheel.last && size < wheel.last) {
        wheel.falls++;
        wheel.ratio = wheel.ratio * 0.6 + (size / wheel.last) * 0.4;
      } else {
        wheel.falls = 0;
      }
      wheel.peak = Math.max(wheel.peak, size);
      wheel.last = size;

      rate = FOLLOW;
      target += d;
      run();

      if (wheel.falls >= 4 && size < wheel.peak * 0.7) {
        // The rest of a decaying series: d·r + d·r² + … = d·r / (1 − r).
        const r = Math.min(Math.max(wheel.ratio, 0.75), 0.96);
        wheelLand(target + Math.sign(d) * size * r / (1 - r));
      } else {
        wheel.idle = setTimeout(() => { if (!wheel.locked) wheelLand(target); }, 120);
      }
    }, { passive: false });

    /* ── Keyboard ── */
    on(root, 'keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const i = (indexAt(target) + (e.key === 'ArrowLeft' ? n - 1 : 1)) % n;
      slides[i].focus({ preventScroll: true });   // focusin below centres it
    });
    // Keyboard focus only: a mouse press focuses the link too, and centring
    // then would tug the strip just as a drag begins.
    on(root, 'focusin', e => {
      if (!e.target.matches(':focus-visible')) return;
      const i = slides.indexOf(e.target.closest('.work-item'));
      if (i >= 0 && i !== indexAt(target)) centreOn(i);
    });

    /* ── Images ──
       Cards round the back of the wheel are thousands of px off to the side,
       so native lazy-loading would leave them blank as they swing in. Load
       them all once the reel is close to view, and decode them up front so
       the first swing past doesn't hitch on a decode. */
    const io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      root.querySelectorAll('.work-media img').forEach(img => {
        img.loading = 'eager';
        if (img.decode) img.decode().catch(() => {});
      });
      io.disconnect();
    }, { rootMargin: '600px 0px' });
    io.observe(root);

    const ro = new ResizeObserver(measure);
    ro.observe(root);
    setCurrent(0);
    measure();

    teardown = () => {
      ac.abort();
      ro.disconnect();
      io.disconnect();
      cancelAnimationFrame(raf);
      clearTimeout(wheel.idle);
    };
  }

  wire(document);
  document.addEventListener('page:load', e => wire(e.detail.main));
}());
