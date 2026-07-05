/* chrome.js — single source of truth for the portfolio's shared nav + footer.
   Each portfolio page carries empty shells — <nav data-chrome="nav"> and
   <footer id="contact" data-chrome="footer"> — and this fills them, so the
   markup lives in one place instead of being copy-pasted across every page.
   Loaded FIRST (before canvas.js / footer.js / reveal.js) so those enhance the
   built DOM. Marginalia has its own nav (built/enhanced in marginalia/main.js). */
(function () {
  const path   = location.pathname;
  const onHome = path === '/' || path === '/index.html';
  const onAbout = path === '/about.html';

  const nav = document.querySelector('nav[data-chrome="nav"]');
  if (nav) {
    // "Selected work" is an in-page anchor on the home page, a cross-page link
    // everywhere else. aria-current marks the page you're on.
    const workHref = onHome ? '#work' : '/#work';
    nav.innerHTML =
      '<a href="/" class="nav-logo"' + (onHome ? ' aria-current="page"' : '') + '>' +
        '<img src="/Zmono-dark.png" alt="Zoe Allgaier — Home"></a>' +
      '<div class="nav-links">' +
        '<a href="' + workHref + '">Selected work</a>' +
        '<a href="/about.html"' + (onAbout ? ' aria-current="page"' : '') + '>About</a>' +
      '</div>';
  }

  const footer = document.querySelector('footer[data-chrome="footer"]');
  if (footer) {
    footer.innerHTML =
      '<p class="footer-prompt">If you\'ve got a project where graphic, motion, and web all need to show up as one thing, I\'d love to hear about it.</p>' +
      '<a href="mailto:zoeallgaier@gmail.com" class="footer-email">zoeallgaier@gmail.com</a>' +
      '<div class="footer-bottom"><span>Zoe Allgaier</span><span>© 2026</span></div>';
  }
}());
