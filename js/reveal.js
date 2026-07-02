/* Letter-by-letter title reveal for project pages — matches the home hero
   and band-name generator, with a marginalia-style blur-in.
   Splits each .project-name into word > char-mask > char spans with staggered
   delays. CSS hides .project-name (under scripting: enabled) until this runs,
   so the plain heading never flashes before animating. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.project-name').forEach(function (nameEl) {
    const text = nameEl.textContent.trim();

    // Reduced motion (or empty): no split — just reveal the plain heading.
    if (!text || reduced) {
      nameEl.style.opacity = '1';
      return;
    }

    const charCount = text.replace(/\s/g, '').length;
    const total     = Math.max(0.5, Math.min(1.5, charCount * 0.03)); // 0.5s–1.5s
    const gap       = total / Math.max(charCount, 1);
    const baseDelay = 0.25;

    nameEl.innerHTML = '';
    let charIdx = 0;

    // Wrap each word so the browser only breaks at spaces, never mid-word.
    text.split(' ').forEach(function (word, wi, words) {
      const wordSpan = document.createElement('span');
      wordSpan.className = 'word';

      [...word].forEach(function (ch) {
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

      nameEl.appendChild(wordSpan);
      if (wi < words.length - 1) nameEl.appendChild(document.createTextNode(' '));
    });

    // Reveal the container; the chars themselves start hidden and fade/blur in.
    nameEl.style.opacity = '1';
  });
}());
