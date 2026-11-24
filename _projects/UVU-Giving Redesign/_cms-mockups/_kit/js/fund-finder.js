/* MOCKUP STAND-IN for the CMS dataview search on Find a Fund. Not for production.
   Filters fund rows by text and area, reads ?q= and ?area=, and shows the first 30 until asked for more
   (the dataview component paginates the same way). */
(function () {
  var PAGE = 30;
  function init() {
    var box = document.getElementById('fund-q'), area = document.getElementById('fund-area');
    var rows = Array.prototype.slice.call(document.querySelectorAll('.al-fundrows li'));
    var count = document.getElementById('fund-count'), empty = document.getElementById('fund-empty');
    var more = document.getElementById('fund-more'), moreBtn = more && more.querySelector('button');
    if (!box) return;
    var showAll = false;
    var sp = new URLSearchParams(location.search), q = sp.get('q'), ar = sp.get('area');
    if (q) box.value = q; if (ar) area.value = ar;
    function run() {
      var t = box.value.trim().toLowerCase(), a = area.value, n = 0, shown = 0;
      var filtered = !!(t || a);
      rows.forEach(function (r) {
        var ok = (!t || r.getAttribute('data-text').indexOf(t) > -1) && (!a || r.getAttribute('data-area') === a);
        if (ok) n++;
        var vis = ok && (filtered || showAll || shown < PAGE);
        r.hidden = !vis; if (vis) shown++;
      });
      count.textContent = filtered ? n + (n === 1 ? ' fund' : ' funds') : 'Showing ' + shown + ' of ' + n + ' funds, A to Z';
      empty.hidden = n > 0;
      if (more) more.hidden = filtered || showAll || n <= PAGE;
      if (moreBtn) moreBtn.textContent = 'Show All ' + n + ' Funds';
    }
    box.addEventListener('input', run); area.addEventListener('change', run);
    if (moreBtn) moreBtn.addEventListener('click', function () { showAll = true; run(); });
    run();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
