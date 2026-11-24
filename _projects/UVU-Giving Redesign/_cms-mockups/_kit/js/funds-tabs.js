/* MOCKUP ONLY: stands in for the CMS tab script on Cesar's new-format-26 fund pages.
   Sidebar and mobile-menu links (.anchorTab) show one .content-panel at a time.
   Search is a panel too (the CMS global tab CSS shows only .tab-container.open). */
(function () {
  var links = document.querySelectorAll('.funds-sidebar .anchorTab');
  var panels = document.querySelectorAll('.funds-content .tab-container');
  var pop = document.getElementById('mobileFundsMenu');

  function show(id, scroll) {
    var target = document.getElementById(id);
    if (!target) return;
    {
      panels.forEach(function (p) { p.classList.toggle('active', p === target); p.classList.toggle('open', p === target); });
      links.forEach(function (a) {
        var on = a.getAttribute('aria-controls') === id;
        a.classList.toggle('active', on);
        a.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
    }
    var cur = document.querySelector('.al-nf-bar-current'), h = target.querySelector('h2');
    if (cur && h) cur.textContent = target.id === 'search' ? 'Search All Funds' : h.textContent;
    if (scroll) (document.querySelector('.mobile-menu-bar') || target).scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var id = a.getAttribute('aria-controls');
      if (pop && pop.matches && pop.matches(':popover-open')) pop.hidePopover();
      show(id, window.innerWidth < 768);
    });
  });

  var start = location.hash.slice(1);
  var first = document.querySelector('.funds-content .content-panel.open');
  if (start && document.getElementById(start)) show(start, false);
  else if (first) first.classList.add('active');
})();
