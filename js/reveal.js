/* reveal.js — letter-by-letter blur-in for display titles. ONE implementation
   shared by the home hero (.hero-name) and the project pages (.project-name);
   these used to be two near-identical copies (home's was inline in index.html).
   The band-name generator keeps its own copy — it re-splits on every regenerate.
   Splits each title into word > char-mask > char spans with staggered delays.
   CSS hides these under (scripting: enabled) until this runs, so the plain
   heading never flashes before animating. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Per-title timing, preserved from the original two implementations:
  // hero used a fixed per-char gap and word-wraps even under reduced motion (so
  // "Zoe / Allgaier" still breaks); project pages compute the gap from length.
  const TARGETS = [
    { sel: '.hero-name',    baseDelay: 0.3,  gapFor: () => 0.045, wrapOnReduced: true  },
    { sel: '.project-name', baseDelay: 0.25,
      gapFor: n => Math.max(0.5, Math.min(1.5, n * 0.03)) / Math.max(n, 1),
      wrapOnReduced: false },
  ];

  function wrapWords(el) {
    el.innerHTML = el.textContent.trim().split(' ')
      .map(w => `<span class="word">${w}</span>`).join(' ');
  }

  TARGETS.forEach(({ sel, baseDelay, gapFor, wrapOnReduced }) => {
    document.querySelectorAll(sel).forEach(el => {
      const text = el.textContent.trim();
      if (!text) return;

      if (reduced) {
        if (wrapOnReduced) wrapWords(el);
        el.style.opacity = '1';
        return;
      }

      const charCount = text.replace(/\s/g, '').length;
      const gap = gapFor(charCount);
      el.innerHTML = '';
      let charIdx = 0;

      // Wrap each word so the browser only breaks at spaces, never mid-word.
      text.split(' ').forEach((word, wi, words) => {
        const wordSpan = document.createElement('span');
        wordSpan.className = 'word';
        [...word].forEach(ch => {
          const mask  = document.createElement('span');
          mask.className = 'char-mask';
          const inner = document.createElement('span');
          inner.className = 'char';
          inner.textContent = ch;
          inner.style.animationDelay = `${(baseDelay + charIdx * gap).toFixed(3)}s`;
          mask.appendChild(inner);
          wordSpan.appendChild(mask);
          charIdx++;
        });
        el.appendChild(wordSpan);
        if (wi < words.length - 1) el.appendChild(document.createTextNode(' '));
      });

      el.style.opacity = '1';
    });
  });
}());
