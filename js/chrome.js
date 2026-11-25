/* chrome.js — single source of truth for the site's shared nav + footer, and
   the Menu toggle that opens the nav. Every page carries an empty
   <nav data-chrome="nav"> shell (portfolio pages a
   <footer id="contact" data-chrome="footer"> one too; Marginalia keeps its
   own footer), and this fills them, so the markup lives in one place instead
   of being copy-pasted across every page. Loaded FIRST (before
   backdrop/footer/tabs/reveal.js) so those enhance the built DOM.

   Both shells sit outside <main>, so js/app.js never replaces them: the nav
   and footer are built once for the whole visit and only re-point themselves
   (current page, scroll-spy) when a route lands — see syncNav/watchWork. */
(function () {
  // Projects listed under "Work", in the same order as the home page grid.
  // Short names so they fit the menu on one line.
  const PROJECTS = [
    ['/psb26.html',     'PSB 2026'],
    ['/elysium.html',   'Elysium'],
    ['/tria.html',      'Tria'],
    ['/uvu-web.html',   'UVU Giving & Alumni'],
    ['/evergreen.html', 'EverGREEN'],
    ['/ylac.html',      'YLAC Signage'],
    ['/psb25.html',     'PSB 2025'],
    ['/uvusoccer.html', 'UCCU Stadium'],
    ['/hipower.html',   'HIPOWER'],
    ['/anyhour.html',   'Any Hour'],
    ['/recursia.html',  'Recursia'],
  ];

  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const onHome  = () => location.pathname === '/' || location.pathname === '/index.html';

  const footer = document.querySelector('footer[data-chrome="footer"]');
  if (footer) {
    footer.innerHTML =
      '<p class="footer-prompt">If you\'ve got a project where graphic, motion, and web all need to show up as one thing, I\'d love to hear about it.</p>' +
      '<a href="mailto:zoeallgaier@gmail.com" class="footer-email">zoeallgaier@gmail.com</a>' +
      '<div class="footer-bottom"><span>Zoe Allgaier</span><span>© 2026</span></div>';
  }

  const nav = document.querySelector('nav[data-chrome="nav"]');
  if (!nav) return;

  // One contents page for every size: CSS sets it as a glass drawer on
  // desktop and a full-screen sheet on phones. The monogram is the masthead
  // (and the way Home). "Work" is an in-page anchor on the home page and a
  // cross-page link elsewhere (syncNav), and carries the project index.
  // "Contact" scrolls to the footer of whatever page you're on.
  // aria-current marks the page.
  nav.setAttribute('aria-label', 'Primary');
  nav.innerHTML =
    '<a href="/" class="nav-logo">' +
      '<img src="/icons/mono-dark.png" alt="">' +
      '<span class="nav-label">Home</span></a>' +
    '<div class="nav-links">' +
      '<a href="/#work" class="nav-work">Work</a>' +
      '<div class="nav-sub" role="group" aria-label="Projects">' +
        PROJECTS.map(([href, name], i) =>
          '<a href="' + href + '">' +
            '<span class="nav-num" aria-hidden="true">' + String(i + 1).padStart(2, '0') + '</span>' +
            name + '</a>').join('') +
      '</div>' +
      '<a href="/about.html">About</a>' +
      '<a href="/resume.html">Resume</a>' +
      '<a href="#contact" class="nav-contact">Contact</a>' +
    '</div>';

  const logo        = nav.querySelector('.nav-logo');
  const workLink    = nav.querySelector('.nav-work');
  const contactLink = nav.querySelector('.nav-contact');
  // Everything that can be "the page you're on" — Work and Contact are places
  // within a page, and take their highlight from the scroll-spy instead.
  const pageLinks = [logo, ...nav.querySelectorAll('.nav-sub a, .nav-links > a')]
    .filter(a => a !== workLink && a !== contactLink);

  function syncNav() {
    workLink.setAttribute('href', onHome() ? '#work' : '/#work');
    pageLinks.forEach(a => {
      const here = a === logo ? onHome() : a.getAttribute('href') === location.pathname;
      if (here) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  /* ── Contact: glide to the very end of the page, wherever you are ── */
  contactLink.addEventListener('click', e => {
    e.preventDefault();
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: reduced() ? 'auto' : 'smooth' });
  });

  /* ── Work: on the home page it's an anchor, with a long eased glide down to
     the grid. From anywhere else it's a link to /#work and the router takes
     it (landing on the grid directly). ── */
  workLink.addEventListener('click', e => {
    const target = onHome() && document.getElementById('work');
    if (!target) return;
    e.preventDefault();
    const clear = parseFloat(getComputedStyle(target).scrollMarginTop) || 0;
    if (reduced()) { target.scrollIntoView(); return; }
    const start = window.scrollY;
    const end = target.getBoundingClientRect().top + window.scrollY - clear;
    const t0 = performance.now();
    document.documentElement.style.scrollBehavior = 'auto';
    (function step(now) {
      const t = Math.min((now - t0) / 1200, 1);
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      window.scrollTo(0, start + (end - start) * ease);
      if (t < 1) requestAnimationFrame(step);
      else document.documentElement.style.scrollBehavior = '';
    })(t0);
  });

  /* ── Scroll-spy ──
     While the footer is on screen, "Contact" is the current location; on the
     home page, so is "Work" while the grid fills the middle of the screen. A
     location takes the highlight from the page item (see base.css). Contact
     wins if both are true. */
  const seen = { work: false, contact: false };

  function syncLocation() {
    const loc = seen.contact ? contactLink : seen.work ? workLink : null;
    [workLink, contactLink].forEach(l => {
      if (l === loc) l.setAttribute('aria-current', 'location');
      else l.removeAttribute('aria-current');
    });
  }

  // The grid belongs to the page, so its observer is rebuilt on every route.
  let watching = null;
  function watchWork() {
    if (watching) { watching.disconnect(); watching = null; }
    seen.work = false;
    const work = onHome() && document.getElementById('work');
    if (work && 'IntersectionObserver' in window) {
      watching = new IntersectionObserver(([en]) => { seen.work = en.isIntersecting; syncLocation(); },
        { rootMargin: '-50% 0px -50% 0px' });
      watching.observe(work);
    }
    syncLocation();
  }

  // Footer almost fully on screen = you've reached the end of the page. It
  // outlives every route, so this one is set up once.
  const end = document.getElementById('contact');
  if (end && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => { seen.contact = en.intersectionRatio >= 0.85; syncLocation(); },
      { threshold: [0, 0.85, 1] }).observe(end);
  }

  /* ── Menu ──
     The contents stay out of the way so the work gets the whole window. A
     glass "Menu" toggle opens them over the page — a drawer on desktop, a
     full-screen sheet on phones; choosing anything, Escape, or a click
     elsewhere puts them away again. The toggle sits right before the nav, so
     base.css reads the open state straight off its aria-expanded, and Tab
     moves from it into the contents. */
  const desktop     = window.matchMedia('(min-width: 769px)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  // Row order for the staggered entrance (base.css reads --i).
  nav.querySelectorAll('.nav-links a').forEach((a, i) => a.style.setProperty('--i', i));

  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'nav-toggle';
  nav.id = nav.id || 'site-nav';
  toggle.setAttribute('aria-controls', nav.id);
  toggle.innerHTML = '<span class="nav-toggle-icon" aria-hidden="true"></span>' +
    '<span class="nav-toggle-label">Menu</span>';
  nav.before(toggle);

  const isOpen = () => toggle.getAttribute('aria-expanded') === 'true';
  // Hover-opening stays disarmed after any close until the pointer has left
  // the trigger zones, so shutting the drawer doesn't bounce it straight open.
  let hoverArmed = true;
  let edgeOpened = false, edgeClose = 0;

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    if (!open) {
      hoverArmed = false;
      edgeOpened = false;
      clearTimeout(edgeClose);
    }
  }
  setOpen(false);

  toggle.addEventListener('click', () => {
    setOpen(!isOpen());
    edgeOpened = false;
    clearTimeout(edgeClose);
  });

  // Capture phase: the menu closes (and the phone sheet releases the page's
  // scroll) before a link's own handler starts its glide.
  nav.addEventListener('click', e => { if (e.target.closest('a')) setOpen(false); }, true);
  document.addEventListener('pointerdown', e => {
    if (isOpen() && !nav.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && isOpen()) { setOpen(false); toggle.focus(); }
  });
  // Tabbing out past the last link (or back before the toggle) puts it away.
  [toggle, nav].forEach(el => el.addEventListener('focusout', e => {
    const to = e.relatedTarget;
    if (isOpen() && to && !nav.contains(to) && to !== toggle) setOpen(false);
  }));
  // Crossing the breakpoint swaps drawer for sheet; start it closed.
  desktop.addEventListener('change', () => setOpen(false));
  document.addEventListener('page:navigate', () => setOpen(false));

  /* ── Edge reveal (desktop): bring the pointer within EDGE_ZONE px of the
     left edge of the window and the drawer slides out on its own. Opened that
     way, it tucks itself away again once the pointer wanders off it (a
     click-opened drawer stays put). The Menu button sits inside that strip,
     so the band it occupies is left out: reaching for the button never moves
     it away. ── */
  const EDGE_ZONE = 56;

  function overToggleBand(y) {
    const r = toggle.getBoundingClientRect();
    return y >= r.top - 16 && y <= r.bottom + 16;
  }

  document.addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse' || !desktop.matches || !finePointer.matches) return;
    const inZone = e.clientX <= EDGE_ZONE && !overToggleBand(e.clientY);
    if (!isOpen() && !inZone) hoverArmed = true;
    if (!isOpen() && inZone && hoverArmed) {
      setOpen(true);
      edgeOpened = true;
    } else if (edgeOpened && isOpen()) {
      // The whole strip from the window edge to the drawer's far side counts,
      // so crossing the gap between them doesn't put it away.
      const overDrawer = e.clientX <= nav.getBoundingClientRect().right + 24;
      clearTimeout(edgeClose);
      if (!overDrawer) edgeClose = setTimeout(() => { setOpen(false); edgeOpened = false; }, 350);
    }
  }, { passive: true });

  document.addEventListener('page:load', () => {
    syncNav();
    watchWork();
  });
  syncNav();
  watchWork();
}());
