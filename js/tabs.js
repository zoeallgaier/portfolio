/* Animated tablist controller. Drives any element with role="tablist",
   where each [role="tab"] has aria-controls pointing at its panel id.
   (Reduced-motion is handled in CSS via transition-duration overrides.) */
(function () {
  function wire(root) {
    root.querySelectorAll('[role="tablist"]').forEach(function (tablist) {
      const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
      if (!tabs.length) return;

      function activateTab(tab) {
        const current = tabs.find(t => t.getAttribute('aria-selected') === 'true');
        if (tab === current) return;

        const target     = document.getElementById(tab.getAttribute('aria-controls'));
        const goingRight  = tabs.indexOf(tab) > tabs.indexOf(current);
        const panels      = target.parentElement;

        // Lock the wrapper at its current height so swapping panels of different
        // lengths doesn't jump; it's eased to the incoming height below.
        panels.style.height = panels.offsetHeight + 'px';

        current.setAttribute('aria-selected', 'false');
        current.tabIndex = -1;
        const exiting = document.getElementById(current.getAttribute('aria-controls'));
        exiting.classList.remove('active');
        exiting.style.transform     = goingRight ? 'translateX(-40px)' : 'translateX(40px)';
        exiting.style.opacity       = '0';
        exiting.style.pointerEvents = 'none';
        exiting.style.position      = 'absolute';
        setTimeout(() => {
          exiting.style.transform = '';
          exiting.style.opacity   = '';
          exiting.style.position  = '';
          exiting.hidden = true;
        }, 420);

        tab.setAttribute('aria-selected', 'true');
        tab.tabIndex = 0;
        target.hidden = false;
        target.style.transform     = goingRight ? 'translateX(40px)' : 'translateX(-40px)';
        target.style.opacity       = '0';
        target.style.position      = 'relative';
        target.style.pointerEvents = 'auto';
        target.getBoundingClientRect();
        target.classList.add('active');
        target.style.transform = '';
        target.style.opacity   = '';

        // Ease the wrapper to the incoming panel's height, then release it back
        // to auto so it stays responsive to reflow (font load, viewport resize).
        panels.style.height = target.offsetHeight + 'px';
        setTimeout(() => { panels.style.height = ''; }, 440);
      }

      tabs.forEach((tab, i) => {
        tab.addEventListener('click', () => activateTab(tab));
        tab.addEventListener('keydown', e => {
          let next;
          if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
          if (e.key === 'ArrowLeft')  next = tabs[(i - 1 + tabs.length) % tabs.length];
          if (e.key === 'Home')       next = tabs[0];
          if (e.key === 'End')        next = tabs[tabs.length - 1];
          if (next) { e.preventDefault(); activateTab(next); next.focus(); }
        });
      });
    });
  }

  // Every route brings its own panels (js/app.js replaces <main>), so this
  // re-wires rather than assuming one page per load.
  wire(document);
  document.addEventListener('page:load', e => wire(e.detail.main));
}());
