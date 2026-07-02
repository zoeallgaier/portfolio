<?php
/* ─────────────────────────────────────────────────────────────────────────
   Marginalia — "post from your phone" page.

   Drop this whole `publish/` folder into your site at /marginalia/publish/
   on SiteGround, then visit  https://YOURSITE/marginalia/publish/
   from your phone and bookmark it.

   The password lives in config.php (right next to this file) so it never gets
   committed to git. First-time setup: copy config.example.php to config.php and
   set your password there.
   ───────────────────────────────────────────────────────────────────────── */
$PUBLISH_PASSWORD = '';
@include __DIR__ . '/config.php';
if ($PUBLISH_PASSWORD === '') {
  http_response_code(500);
  exit('No password set — create marginalia/publish/config.php (see config.example.php).');
}

/* ── Paths (relative to this file, so they work wherever the site lives) ── */
$CONTENT_JSON = __DIR__ . '/../content.json';          // the feed data
$IMAGE_DIR    = __DIR__ . '/../../_assets/marginalia';  // where photos are saved
$IMAGE_WEBBASE = '/_assets/marginalia';                 // how the feed references them
$MAX_WIDTH    = 1600;                                    // resize big phone photos down to this

/* ───────────────────────────── plumbing ───────────────────────────────── */
session_start();
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));

$error   = '';
$success = '';
$added   = null;

/* Handle logout */
if (isset($_GET['logout'])) { session_destroy(); header('Location: ?'); exit; }

/* Handle login */
if (($_POST['action'] ?? '') === 'login') {
  if (hash_equals($PUBLISH_PASSWORD, $_POST['password'] ?? '')) {
    $_SESSION['auth'] = true;
  } else {
    $error = 'Wrong password.';
  }
}

$authed = !empty($_SESSION['auth']);

/* ───────────────────────── handle a new entry ─────────────────────────── */
if ($authed && ($_POST['action'] ?? '') === 'publish') {
  if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    $error = 'Session expired — please try again.';
  } else {
    $result = handle_publish();
    if (is_array($result)) { $success = 'Published!'; $added = $result; }
    else                   { $error   = $result; }
  }
}

/* Build one entry, save any image, and prepend it to content.json.
   Returns the entry array on success, or an error string. */
function handle_publish() {
  global $CONTENT_JSON, $IMAGE_DIR, $IMAGE_WEBBASE, $MAX_WIDTH;

  $type = $_POST['type'] ?? '';
  if (!in_array($type, ['post', 'find', 'photo', 'library'], true)) return 'Pick a type.';

  $clean = fn($s) => trim(strip_tags((string)$s));
  $title = $clean($_POST['title'] ?? '');
  $url   = trim((string)($_POST['url'] ?? ''));
  $note  = $clean($_POST['note'] ?? '');
  $date  = trim((string)($_POST['date'] ?? '')) ?: date('Y-m-d');

  // Basic per-type requirements
  if ($type !== 'photo' && $title === '') return 'This type needs a title.';

  // Tags: comma-separated → lowercase slugs
  $tags = array_values(array_filter(array_map(
    fn($t) => preg_replace('/[^a-z0-9\- ]/', '', strtolower(trim($t))),
    explode(',', (string)($_POST['tags'] ?? ''))
  ), fn($t) => $t !== ''));

  // Optional image (required for photos)
  $imageWeb = '';
  if (!empty($_FILES['image']['name']) && $_FILES['image']['error'] !== UPLOAD_ERR_NO_FILE) {
    $saved = save_image($_FILES['image'], $title ?: $type, $date);
    if (!is_string($saved) || $saved[0] !== '/') return $saved; // error string
    $imageWeb = $saved;
  } elseif ($type === 'photo') {
    return 'A photo entry needs an image.';
  }

  // Assemble entry in the same shape the feed expects
  $entry = ['type' => $type];
  if ($title)   $entry['title'] = $title;
  if ($url)     $entry['url']   = $url;
  if ($imageWeb) $entry['image'] = $imageWeb;
  if ($note)    $entry['note']  = $note;
  if ($type === 'library' && !empty($_POST['reading'])) $entry['reading'] = true;
  $entry['date'] = $date;
  if ($tags)    $entry['tags'] = $tags;

  // Read → prepend → write, with a lock so nothing is clobbered
  if (!is_writable($CONTENT_JSON)) return 'content.json is not writable on the server (check file permissions).';
  $fp = fopen($CONTENT_JSON, 'c+');
  if (!$fp) return 'Could not open content.json.';
  flock($fp, LOCK_EX);
  $raw  = stream_get_contents($fp);
  $data = json_decode($raw, true);
  if (!is_array($data)) { flock($fp, LOCK_UN); fclose($fp); return 'content.json is not valid JSON — aborting so nothing is lost.'; }
  array_unshift($data, $entry);
  $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
  rewind($fp); ftruncate($fp, 0); fwrite($fp, $json . "\n");
  flock($fp, LOCK_UN); fclose($fp);

  return $entry;
}

/* Save an uploaded image: fix rotation, downscale, re-encode. Returns web path or error. */
function save_image($file, $label, $date) {
  global $IMAGE_DIR, $IMAGE_WEBBASE, $MAX_WIDTH;

  if ($file['error'] !== UPLOAD_ERR_OK) return 'Image upload failed (it may be too large for the server).';
  if (!is_uploaded_file($file['tmp_name'])) return 'Image upload failed.';

  $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
  $slug = preg_replace('/[^a-z0-9]+/', '-', strtolower($label));
  $slug = trim($slug, '-') ?: 'photo';
  $name = $date . '-' . $slug . '-' . substr(bin2hex(random_bytes(3)), 0, 4);

  if (!is_dir($IMAGE_DIR)) return 'Image folder not found on the server.';
  if (!is_writable($IMAGE_DIR)) return 'Image folder is not writable (check permissions).';

  // Try to process with GD (resize + orientation). Falls back to saving the original.
  $info = @getimagesize($file['tmp_name']);
  $mime = $info['mime'] ?? '';
  $img = null;
  if ($mime === 'image/jpeg' && function_exists('imagecreatefromjpeg')) $img = @imagecreatefromjpeg($file['tmp_name']);
  elseif ($mime === 'image/png' && function_exists('imagecreatefrompng')) $img = @imagecreatefrompng($file['tmp_name']);
  elseif ($mime === 'image/webp' && function_exists('imagecreatefromwebp')) $img = @imagecreatefromwebp($file['tmp_name']);

  if ($img) {
    // Respect EXIF orientation for JPEGs from phones
    if ($mime === 'image/jpeg' && function_exists('exif_read_data')) {
      $exif = @exif_read_data($file['tmp_name']);
      $o = $exif['Orientation'] ?? 0;
      if ($o === 3) $img = imagerotate($img, 180, 0);
      elseif ($o === 6) $img = imagerotate($img, -90, 0);
      elseif ($o === 8) $img = imagerotate($img, 90, 0);
    }
    $w = imagesx($img); $h = imagesy($img);
    if ($w > $MAX_WIDTH) {
      $nh = (int)round($h * $MAX_WIDTH / $w);
      $dst = imagecreatetruecolor($MAX_WIDTH, $nh);
      imagecopyresampled($dst, $img, 0,0,0,0, $MAX_WIDTH, $nh, $w, $h);
      imagedestroy($img); $img = $dst;
    }
    $out = "$IMAGE_DIR/$name.jpg";
    imagejpeg($img, $out, 82);
    imagedestroy($img);
    return "$IMAGE_WEBBASE/$name.jpg";
  }

  // Fallback: keep the original file as-is (e.g. HEIC/GIF or no GD)
  $ext = in_array($ext, ['jpg','jpeg','png','gif','webp','heic']) ? ($ext === 'jpeg' ? 'jpg' : $ext) : 'jpg';
  $out = "$IMAGE_DIR/$name.$ext";
  if (!move_uploaded_file($file['tmp_name'], $out)) return 'Could not save the image.';
  return "$IMAGE_WEBBASE/$name.$ext";
}

$csrf = $_SESSION['csrf'];
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Post · Marginalia</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Oxygen:wght@300;400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #e1e1e8; --text: #1f1f28; --muted: rgba(0,0,0,.62); --rule: rgba(0,0,0,.2);
    --field: rgba(255,255,255,.5);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#1a1a22; --text:#e1e1e8; --muted:rgba(255,255,255,.5); --rule:rgba(255,255,255,.14);
            --field: rgba(255,255,255,.05); }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: 'Oxygen', system-ui, sans-serif; font-weight: 300;
    line-height: 1.5; -webkit-text-size-adjust: 100%;
  }
  .wrap { max-width: 34rem; margin: 0 auto; padding: 2rem 1.25rem 4rem; }
  h1 { font-family: 'Instrument Serif', serif; font-weight: 400; font-size: 2.4rem;
       margin: 0 0 .25rem; letter-spacing: .01em; }
  .sub { color: var(--muted); margin: 0 0 1.75rem; font-size: .95rem; }
  label { display: block; font-size: .82rem; letter-spacing: .04em; text-transform: uppercase;
          color: var(--muted); margin: 1.1rem 0 .4rem; }
  input[type=text], input[type=url], input[type=date], input[type=password], textarea, select, input[type=file] {
    width: 100%; padding: .7rem .8rem; font: inherit; font-size: 1rem; color: var(--text);
    background: var(--field); border: 1px solid var(--rule); border-radius: 8px;
  }
  textarea { min-height: 5.5rem; resize: vertical; }
  /* iOS gives date inputs their own native box; normalize it so the padding
     matches every other field and the value isn't shoved off-center. */
  input[type=date] { -webkit-appearance: none; appearance: none; min-height: 2.9rem; }
  input[type=date]::-webkit-date-and-time-value { margin: 0; text-align: left; }
  input[type=date]::-webkit-calendar-picker-indicator { margin-left: auto; }
  input:focus, textarea:focus, select:focus { outline: 2px solid var(--text); outline-offset: 1px; }
  .types { display: grid; grid-template-columns: repeat(2,1fr); gap: .5rem; margin-top: .4rem; }
  .types label { display: flex; align-items: center; justify-content: center; gap: .4rem;
    margin: 0; padding: .8rem; text-transform: none; letter-spacing: 0; font-size: 1rem;
    color: var(--text); border: 1px solid var(--rule); border-radius: 8px; cursor: pointer;
    background: var(--field); }
  .types input { position: absolute; opacity: 0; pointer-events: none; }
  .types label:has(input:checked) { border-color: var(--text); box-shadow: inset 0 0 0 1px var(--text); }
  .row { display: flex; align-items: center; gap: .5rem; margin-top: 1rem; }
  .row input[type=checkbox] { width: 1.1rem; height: 1.1rem; }
  .row label { margin: 0; text-transform: none; letter-spacing: 0; color: var(--text); font-size: 1rem; }
  .hint { font-size: .8rem; color: var(--muted); margin-top: .35rem; }
  button.go {
    margin-top: 1.75rem; width: 100%; padding: .9rem; font: inherit; font-size: 1.05rem;
    background: var(--text); color: var(--bg); border: 0; border-radius: 8px; cursor: pointer;
  }
  button.go:active { opacity: .85; }
  .msg { padding: .85rem 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: .95rem; }
  .msg.ok  { border: 1px solid var(--rule); }
  .msg.err { border: 1px solid #c0392b; color: #c0392b; }
  .field-group[hidden] { display: none; }
  pre { background: var(--field); border: 1px solid var(--rule); border-radius: 8px;
        padding: .8rem; overflow-x: auto; font-size: .8rem; }
  a { color: var(--text); }
  .topbar { display: flex; justify-content: space-between; align-items: baseline; }
  .topbar a { color: var(--muted); font-size: .85rem; text-decoration: none; }
</style>
</head>
<body>
<div class="wrap">

<?php if (!$authed): ?>
  <div class="topbar"><h1>Marginalia</h1></div>
  <?php if ($error): ?><div class="msg err"><?= htmlspecialchars($error) ?></div><?php endif; ?>
  <form method="post">
    <input type="hidden" name="action" value="login">
    <label for="pw">Password</label>
    <input id="pw" type="password" name="password" autofocus autocomplete="current-password">
    <button class="go" type="submit">Enter</button>
  </form>

<?php else: ?>
  <div class="topbar"><h1>New entry</h1><a href="?logout=1">Log out</a></div>

  <?php if ($success): ?>
    <div class="msg ok"><strong><?= htmlspecialchars($success) ?></strong>
      &nbsp;<a href="/marginalia/" target="_blank">View feed →</a></div>
    <details><summary class="hint">What was added</summary>
      <pre><?= htmlspecialchars(json_encode($added, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)) ?></pre>
    </details>
  <?php endif; ?>
  <?php if ($error): ?><div class="msg err"><?= htmlspecialchars($error) ?></div><?php endif; ?>

  <form method="post" enctype="multipart/form-data" id="f">
    <input type="hidden" name="action" value="publish">
    <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">

    <label>Type</label>
    <div class="types">
      <label><input type="radio" name="type" value="photo" checked>📷 Photo</label>
      <label><input type="radio" name="type" value="post">✍️ Post</label>
      <label><input type="radio" name="type" value="find">🔗 Find</label>
      <label><input type="radio" name="type" value="library">📚 Library</label>
    </div>

    <div class="field-group" data-show="post,find,library">
      <label for="title" id="title-label">Title</label>
      <input id="title" type="text" name="title" autocomplete="off">
    </div>

    <div class="field-group" data-show="post,find,library">
      <label for="url" id="url-label">Link</label>
      <input id="url" type="url" name="url" placeholder="https://…" autocomplete="off">
      <p class="hint" id="url-hint">External link for finds; the post's page for posts.</p>
    </div>

    <div class="field-group" data-show="photo,post,find,library">
      <label for="image" id="image-label">Photo</label>
      <input id="image" type="file" name="image" accept="image/*">
      <p class="hint">Big phone photos get resized automatically. Optional for posts &amp; finds.</p>
    </div>

    <div class="field-group" data-show="photo,post,find,library">
      <label for="note" id="note-label">Note</label>
      <textarea id="note" name="note" placeholder="A caption or a few sentences…"></textarea>
    </div>

    <div class="field-group" data-show="library">
      <div class="row"><input type="checkbox" id="reading" name="reading" value="1"><label for="reading">Currently reading</label></div>
    </div>

    <label for="tags">Tags <span style="text-transform:none;letter-spacing:0">(comma-separated)</span></label>
    <input id="tags" type="text" name="tags" placeholder="film, review" autocomplete="off">

    <label for="date">Date</label>
    <input id="date" type="date" name="date" value="<?= date('Y-m-d') ?>">

    <button class="go" type="submit">Publish</button>
  </form>

  <script>
    // Show only the fields relevant to the chosen type, and relabel a couple.
    const groups = document.querySelectorAll('.field-group');
    function sync() {
      const t = document.querySelector('input[name=type]:checked').value;
      groups.forEach(g => g.hidden = !g.dataset.show.split(',').includes(t));
      document.getElementById('note-label').textContent =
        t === 'library' ? 'Author / year' : t === 'photo' ? 'Caption' : 'Note';
      document.getElementById('url-label').textContent = t === 'library' ? 'Link (optional)' : 'Link';
      document.getElementById('title-label').textContent = t === 'library' ? 'Book title' : 'Title';
    }
    document.querySelectorAll('input[name=type]').forEach(r => r.addEventListener('change', sync));
    sync();
  </script>
<?php endif; ?>

</div>
</body>
</html>
