/* =====================================================================
   MOCKUP TOOLS. NOT FOR PRODUCTION.
   - Show CMS labels: outlines each OU section/region
   - Show copy edits: highlights + numbers flagged copy, adds a notes list at the end
   - Save as PDF: opens Chrome's print dialog (choose "Save as PDF").
     Turn on "Show copy edits" first for a copywriting-review PDF.
   ===================================================================== */
(function () {
  function buildNotes() {
    var old = document.querySelector('.mock-notes');
    if (old) old.remove();
    document.querySelectorAll('.mock-copy-num').forEach(function (n) { n.remove(); });
    var flags = document.querySelectorAll('.mock-copy-flag');
    if (!flags.length) return;
    var wrap = document.createElement('section');
    wrap.className = 'mock-notes';
    var html = '<div class="container-fluid"><h2>Copy edits on this page</h2><ol>';
    flags.forEach(function (el, i) {
      var num = document.createElement('span');
      num.className = 'mock-copy-num';
      num.textContent = i + 1;
      el.appendChild(num);
      html += '<li>' + (el.getAttribute('title') || 'Edited') + '</li>';
    });
    wrap.innerHTML = html + '</ol></div>';
    var main = document.querySelector('main');
    main.parentNode.insertBefore(wrap, main.nextSibling);
  }

  function openDetails() {
    document.querySelectorAll('main details').forEach(function (d) { d.setAttribute('open', ''); });
  }

  window.mockPrepareReview = function () { document.body.classList.add('mock-copy'); buildNotes(); openDetails(); };

  document.addEventListener('DOMContentLoaded', function () {
    buildNotes();
    // Framed on zoeallgaier.com/uvu-web.html: show the page, not the review toolbar.
    if (window.self !== window.top) return;
    var bar = document.createElement('div');
    bar.className = 'mock-toolbar';
    bar.setAttribute('aria-label', 'Mockup tools');
    bar.innerHTML =
      '<button type="button" data-mock="mock-labels" aria-pressed="false">Show CMS labels</button>' +
      '<button type="button" data-mock="mock-copy" aria-pressed="false">Show copy edits</button>' +
      '<button type="button" data-print>Save as PDF</button>';
    document.body.appendChild(bar);
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      if (b.hasAttribute('data-print')) { openDetails(); window.print(); return; }
      var on = document.body.classList.toggle(b.dataset.mock);
      b.setAttribute('aria-pressed', on);
    });
  });
  window.addEventListener('beforeprint', openDetails);
})();
