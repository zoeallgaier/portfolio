/* chrome.js — single source of truth for the portfolio's shared nav + footer.
   Each portfolio page carries empty shells — <nav data-chrome="nav"> and
   <footer id="contact" data-chrome="footer"> — and this fills them, so the
   markup lives in one place instead of being copy-pasted across every page.
   Loaded FIRST (before backdrop/footer/tabs/reveal.js) so those enhance the
   built DOM. Marginalia has its own nav (built/enhanced in marginalia/main.js).

   Both shells sit outside <main>, so js/app.js never replaces them: the nav
   and footer are built once for the whole visit and only re-point themselves
   (current page, scroll-spy) when a route lands — see syncNav/watchWork. */
(function () {
  // Line icons (24px / 1.9 stroke, same style as marginalia's tab icons).
  // Shown in the phone tab bar; the editorial desktop sidebar is type-only.
  const icon = paths =>
    '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    paths + '</svg>';
  const WORK_ICON    = icon('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>');
  const ABOUT_ICON   = icon('<circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/>');
  const RESUME_ICON  = icon('<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 16.5h4"/>');
  const CONTACT_ICON = icon('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7.5 8.5 6 8.5-6"/>');

  // Projects listed under "Work" in the desktop sidebar, in the same order as
  // the home page grid. Short names so they fit the sidebar on one line.
  const PROJECTS = [
    ['/evergreen.html', 'EverGREEN'],
    ['/elysium.html',   'Elysium'],
    ['/tria.html',      'Tria'],
    ['/psb26.html',     'PSB 2026'],
    ['/psb25.html',     'PSB 2025'],
    ['/uvusoccer.html', 'UCCU Stadium'],
    ['/hipower.html',   'HIPOWER'],
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

  // One DOM for both shapes: CSS makes it an editorial sidebar on desktop and
  // a bottom tab bar on phones. The monogram is the Home tab's icon on phones
  // and heads the sidebar (with the name) on desktop. "Work" is an in-page
  // anchor on the home page and a cross-page link elsewhere (syncNav), and
  // carries the project index (sidebar only). "Contact" scrolls to the footer
  // of whatever page you're on (sidebar only — phones get Resume in its place,
  // and every page ends in the footer anyway). aria-current marks the page.
  nav.setAttribute('aria-label', 'Primary');
  nav.innerHTML =
    '<a href="/" class="nav-logo">' +
      '<img src="/icons/z-mark-dark.png" alt="">' +
      '<span class="nav-name" aria-hidden="true"></span>' +
      '<span class="nav-label">Home</span></a>' +
    '<div class="nav-links">' +
      '<a href="/#work" class="nav-work">' + WORK_ICON + '<span class="nav-label">Work</span></a>' +
      '<div class="nav-sub" role="group" aria-label="Projects">' +
        PROJECTS.map(([href, name], i) =>
          '<a href="' + href + '">' +
            '<span class="nav-num" aria-hidden="true">' + String(i + 1).padStart(2, '0') + '</span>' +
            name + '</a>').join('') +
      '</div>' +
      '<a href="/about.html">' + ABOUT_ICON + '<span class="nav-label">About</span></a>' +
      '<a href="/resume.html">' + RESUME_ICON + '<span class="nav-label">Resume</span></a>' +
      '<a href="#contact" class="nav-contact">' + CONTACT_ICON + '<span class="nav-label">Contact</span></a>' +
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
     wins if both are true — on the sidebar only, since the tab bar has no
     Contact tab to hand the highlight to. */
  const sidebar = window.matchMedia('(min-width: 769px)');
  const seen = { work: false, contact: false };

  function syncLocation() {
    const loc = seen.contact && sidebar.matches ? contactLink : seen.work ? workLink : null;
    [workLink, contactLink].forEach(l => {
      if (l === loc) l.setAttribute('aria-current', 'location');
      else l.removeAttribute('aria-current');
    });
  }

  sidebar.addEventListener('change', syncLocation);

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
  if (footer && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => { seen.contact = en.intersectionRatio >= 0.85; syncLocation(); },
      { threshold: [0, 0.85, 1] }).observe(footer);
  }

  document.addEventListener('page:load', () => { syncNav(); watchWork(); });
  syncNav();
  watchWork();
}());
