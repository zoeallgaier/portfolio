/* reveal.js — letter-by-letter blur-in for display titles. ONE implementation
   shared by the home hero (.hero-name), the about and resume titles
   (.about-title, .cv-name) and the project pages (.project-name).
   The band-name generator keeps its own copy — it re-splits on every regenerate.
   Splits each title into word > char-mask > char spans with staggered delays.
   CSS hides these under (scripting: enabled) until this runs, so the plain
   heading never flashes before animating. */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // The hero's timing, shared by every title that "speaks" like it: a fixed
  // per-letter gap, so a short title and a long one move at the same pace.
  // Project pages instead fit the whole title into 0.5–1.5s.
  const SPOKEN = { baseDelay: 0.15, gapFor: () => 0.035, wrapOnReduced: true };
  const TARGETS = [
    // The hero speaks: after a word ending in punctuation ("Hi,") the next
    // word waits a beat, read from --speech-pause on the title (index.css).
    { sel: '.hero-name', ...SPOKEN, pauseVar: '--speech-pause' },
    { sel: '.about-title, .cv-name', ...SPOKEN },
    { sel: '.project-name', baseDelay: 0.25,
      gapFor: n => Math.max(0.5, Math.min(1.5, n * 0.03)) / Math.max(n, 1),
      wrapOnReduced: false },
  ];

  function wrapWords(el) {
    el.innerHTML = el.textContent.trim().split(' ')
      .map(w => `<span class="word">${w}</span>`).join(' ');
  }

  // Run against whatever <main> is on screen: js/app.js swaps in a fresh one
  // on every route, and its title arrives unsplit.
  function split(root) {
    TARGETS.forEach(({ sel, baseDelay, gapFor, wrapOnReduced, pauseVar }) => {
      root.querySelectorAll(sel).forEach(el => {
        const text = el.textContent.trim();
        if (!text || el.dataset.split) return;
        el.dataset.split = '';

        if (reduced) {
          if (wrapOnReduced) wrapWords(el);
          el.style.opacity = '1';
          return;
        }

        const charCount = text.replace(/\s/g, '').length;
        const gap = gapFor(charCount);
        const pause = pauseVar ? parseFloat(getComputedStyle(el).getPropertyValue(pauseVar)) || 0 : 0;
        // One letter per span would otherwise be read out letter by letter.
        el.setAttribute('aria-label', text);
        el.innerHTML = '';
        let charIdx = 0, held = 0, last = null;

        // Wrap each word so the browser only breaks at spaces, never mid-word.
        text.split(' ').forEach((word, wi, words) => {
          if (wi > 0 && /[,.!?…]$/.test(words[wi - 1])) held += pause;
          const wordSpan = document.createElement('span');
          wordSpan.className = 'word';
          wordSpan.setAttribute('aria-hidden', 'true');
          [...word].forEach(ch => {
            const mask  = document.createElement('span');
            mask.className = 'char-mask';
            const inner = document.createElement('span');
            inner.className = 'char';
            inner.textContent = ch;
            inner.style.animationDelay = `${(baseDelay + held + charIdx * gap).toFixed(3)}s`;
            mask.appendChild(inner);
            wordSpan.appendChild(mask);
            last = inner;
            charIdx++;
          });
          el.appendChild(wordSpan);
          if (wi < words.length - 1) el.appendChild(document.createTextNode(' '));
        });

        el.style.opacity = '1';

        // Once the last letter has landed, retire every letter's animation
        // and compositor layer in one go. The keyframes already end on
        // filter: none / transform: none (so WebKit never clips a resting
        // letter's ink to its box), so nothing visibly changes; doing it in a
        // single frame rather than letter by letter means one repaint, not a
        // dozen small ones while the wave is still moving.
        last.addEventListener('animationend', () => {
          requestAnimationFrame(() => el.classList.add('is-landed'));
        }, { once: true });
      });
    });
  }

  split(document);
  document.addEventListener('page:load', e => split(e.detail.main));
}());
