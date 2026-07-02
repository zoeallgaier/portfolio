/* Progressive enhancement: add a copy-to-clipboard icon beside the footer
   email so visitors without a configured mail client aren't left with a dead
   mailto link. The link itself is untouched and stays the primary action. */
(function () {
  const email = document.querySelector('.footer-email');
  if (!email || !navigator.clipboard) return;

  const address = email.textContent.trim();

  const copyIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="3" width="8" height="4" rx="1.5"/><path d="M16 5h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/></svg>';
  const checkIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'footer-copy';
  btn.innerHTML = copyIcon;
  btn.setAttribute('aria-label', 'Copy email address');

  // Sit the email and copy icon on one line.
  const row = document.createElement('div');
  row.className = 'footer-email-row';
  email.replaceWith(row);
  row.append(email, btn);

  let resetId;
  btn.addEventListener('click', function () {
    navigator.clipboard.writeText(address).then(function () {
      btn.innerHTML = checkIcon;
      btn.setAttribute('aria-label', 'Email copied');
      clearTimeout(resetId);
      resetId = setTimeout(function () {
        btn.innerHTML = copyIcon;
        btn.setAttribute('aria-label', 'Copy email address');
      }, 2000);
    });
  });
}());
