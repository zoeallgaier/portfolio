(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvases = document.querySelectorAll('.hero-canvas, .project-canvas');
  if (!canvases.length) return;

  const GAP = 24;
  const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  canvases.forEach(function (canvas) {
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0, cols = 0, rows = 0, t = 0, running = false;

    function resize() {
      W = canvas.offsetWidth;
      H = canvas.offsetHeight;
      if (!W || !H) return;
      const dpr = window.devicePixelRatio || 1;
      canvas.width  = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cols = Math.ceil(W / GAP) + 1;
      rows = Math.ceil(H / GAP) + 1;
      if (!running) { running = true; draw(); }
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const x = c * GAP;
          const y = r * GAP;
          const w1 = 0.5 + 0.5 * Math.sin(c * 0.22 + r * 0.14 - t * 0.7);
          const w2 = 0.5 + 0.5 * Math.sin(c * 0.11 - r * 0.18 - t * 0.43);
          const wave  = w1 * 0.6 + w2 * 0.4;
          const alpha = 0.02 + 0.40 * wave;
          const rad   = 0.55 + 0.45 * wave;
          ctx.beginPath();
          ctx.arc(x, y, rad, 0, Math.PI * 2);
          ctx.fillStyle = dark
            ? `rgba(255,255,255,${(alpha * 1.3).toFixed(3)})`
            : `rgba(0,0,0,${alpha.toFixed(3)})`;
          ctx.fill();
        }
      }
      t += 0.011;
      requestAnimationFrame(draw);
    }

    new ResizeObserver(resize).observe(canvas.parentElement || document.body);
  });
})();
