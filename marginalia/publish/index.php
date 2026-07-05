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
$CONTENT_JSON  = __DIR__ . '/../content.json';          // the feed data
$IMAGE_DIR     = __DIR__ . '/../../_assets/marginalia';  // where photos are saved
$IMAGE_WEBBASE = '/_assets/marginalia';                 // how the feed references them
$POSTS_DIR     = __DIR__ . '/../posts';                  // where written posts are generated
$SITE          = 'https://zoeallgaier.com';             // for absolute og: URLs
$MAX_WIDTH     = 1600;                                   // resize big phone photos down to this

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

/* Live Markdown preview (AJAX) — session-authed, renders without saving. */
if ($authed && ($_POST['action'] ?? '') === 'preview') {
  header('Content-Type: text/html; charset=utf-8');
  echo md_to_html($_POST['body'] ?? '');
  exit;
}

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

/* Build one entry, save any image, optionally generate a full post page, and
   prepend the entry to content.json. Returns the entry array, or an error. */
function handle_publish() {
  global $CONTENT_JSON, $POSTS_DIR;

  $type = $_POST['type'] ?? '';
  if (!in_array($type, ['post', 'find', 'photo', 'library'], true)) return 'Pick a type.';

  $clean = fn($s) => trim(strip_tags((string)$s));
  $title = $clean($_POST['title'] ?? '');
  $url   = trim((string)($_POST['url'] ?? ''));
  $note  = $clean($_POST['note'] ?? '');
  $date  = trim((string)($_POST['date'] ?? '')) ?: date('Y-m-d');

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

  // Assemble the feed entry
  $entry = ['type' => $type];
  if ($title)   $entry['title'] = $title;
  if ($url)     $entry['url']   = $url;
  if ($imageWeb) $entry['image'] = $imageWeb;
  if ($note)    $entry['note']  = $note;
  if ($type === 'library' && !empty($_POST['reading'])) $entry['reading'] = true;
  $entry['date'] = $date;
  if ($tags)    $entry['tags'] = $tags;

  // A written post generates its own page; the feed card links to it.
  if ($type === 'post') {
    $body = trim((string)($_POST['body'] ?? ''));
    if ($body !== '') {
      $eyebrow = $clean($_POST['eyebrow'] ?? '') ?: 'Essay';
      $desc    = $note !== '' ? $note : plain_excerpt($body);
      $res = write_post_page($title, $eyebrow, $date, $tags, md_to_html($body), $desc, $imageWeb);
      if (isset($res['error'])) return $res['error'];
      $entry['url'] = $res['url'];
      if (!$note) $entry['note'] = $desc;   // give the feed card a teaser
    } elseif ($url === '') {
      return 'Write the post below, or paste a link.';
    }
  }

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

/* ── Markdown → post-body HTML (a small subset mapped to the site's styles) ── */
function md_to_html($md) {
  $lines = explode("\n", str_replace(["\r\n", "\r"], "\n", (string)$md));
  $lines[] = '';                 // sentinel so the final group flushes in-loop
  $out = [];
  $buf = [];                     // current grouped-block lines (markers stripped)
  $mode = '';

  foreach ($lines as $raw) {
    $t = rtrim($raw);

    if ($t === '')                                   { $kind = 'blank'; $m = []; }
    elseif (preg_match('/^###\s+(.*)$/', $t, $m))    { $kind = 'h3'; }
    elseif (preg_match('/^#{1,2}\s+(.*)$/', $t, $m)) { $kind = 'h2'; }
    elseif (preg_match('/^(---|\*\*\*)$/', $t))      { $kind = 'hr'; $m = []; }
    elseif (preg_match('/^>\s?(.*)$/', $t, $m))      { $kind = 'quote'; }
    elseif (preg_match('/^[-*]\s+(.*)$/', $t, $m))   { $kind = 'list'; }
    elseif (preg_match('/^~\s+(.*)$/', $t, $m))      { $kind = 'litany'; }
    else                                             { $kind = 'p'; $m = [1 => $t]; }

    // Flush the running group when the block type changes or a non-group appears.
    $grouped = in_array($kind, ['quote', 'list', 'litany', 'p'], true);
    if ($buf && (!$grouped || $kind !== $mode)) {
      $out[] = md_flush($mode, $buf);
      $buf = []; $mode = '';
    }

    if ($kind === 'blank') continue;
    if ($kind === 'h2') { $out[] = '<h2>' . md_inline($m[1]) . '</h2>'; continue; }
    if ($kind === 'h3') { $out[] = '<h3>' . md_inline($m[1]) . '</h3>'; continue; }
    if ($kind === 'hr') { $out[] = '<hr>'; continue; }

    $mode = $kind;
    $buf[] = $m[1];
  }
  return implode("\n\n", $out);
}

function md_flush($mode, $buf) {
  if ($mode === 'quote')  return '<blockquote>' . implode('<br>', array_map('md_inline', $buf)) . '</blockquote>';
  if ($mode === 'list')   return '<ul>' . implode('', array_map(fn($l) => '<li>' . md_inline($l) . '</li>', $buf)) . '</ul>';
  if ($mode === 'litany') return '<p class="litany">' . implode('<br>', array_map('md_inline', $buf)) . '</p>';
  return '<p>' . implode('<br>', array_map('md_inline', $buf)) . '</p>';
}

/* Inline formatting. Escapes first, then applies markdown, so raw HTML is safe. */
function md_inline($t) {
  $t = htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
  $t = preg_replace_callback('/\[([^\]]+)\]\(([^)\s]+)\)/', function ($m) {
    $ext = preg_match('#^https?://#', html_entity_decode($m[2])) ? ' target="_blank" rel="noopener noreferrer"' : '';
    return '<a href="' . $m[2] . '"' . $ext . '>' . $m[1] . '</a>';
  }, $t);
  $t = preg_replace('/\*\*(.+?)\*\*/', '<strong>$1</strong>', $t);
  $t = preg_replace('/(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)/', '<em>$1</em>', $t);
  $t = preg_replace('/(?<!\w)_([^_\n]+?)_(?!\w)/', '<em>$1</em>', $t);
  return $t;
}

/* Plain-text excerpt for the feed teaser / meta description when none is given. */
function plain_excerpt($md, $len = 160) {
  $t = preg_replace('/\[([^\]]+)\]\([^)]*\)/', '$1', $md);      // links → text
  $t = preg_replace('/[#>*_~`]|^[-]\s+/m', '', $t);            // strip markers
  $t = trim(preg_replace('/\s+/', ' ', $t));
  if (mb_strlen($t) > $len) $t = mb_substr($t, 0, $len - 1) . '…';
  return $t;
}

function make_slug($title) {
  global $POSTS_DIR;
  $base = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($title)), '-') ?: 'post';
  $slug = $base; $i = 2;
  while (file_exists("$POSTS_DIR/$slug.html")) { $slug = "$base-$i"; $i++; }
  return $slug;
}

/* Generate a full static post page from the essay template. Returns
   ['url' => 'posts/<slug>.html'] or ['error' => '…']. */
function write_post_page($title, $eyebrow, $date, $tags, $bodyHtml, $desc, $imageWeb) {
  global $POSTS_DIR, $SITE;
  if (!is_dir($POSTS_DIR))      return ['error' => 'posts/ folder not found on the server.'];
  if (!is_writable($POSTS_DIR)) return ['error' => 'posts/ folder is not writable (check permissions).'];

  $slug   = make_slug($title);
  $url    = "posts/$slug.html";
  $urlAbs = "$SITE/marginalia/$url";
  $imgAbs = $imageWeb ? $SITE . $imageWeb : '';
  $dateFmt = date('F j, Y', strtotime($date) ?: time());
  $e = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');

  $tagHtml = '';
  foreach ($tags as $t) $tagHtml .= '          <span class="tag" style="pointer-events:none">' . $e($t) . "</span>\n";

  $ogImg = $imgAbs ? '  <meta property="og:image" content="' . $e($imgAbs) . "\" />\n" : '';
  $card  = $imgAbs ? 'summary_large_image' : 'summary';

  $html = '<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>' . $e($title) . ' — Marginalia</title>
  <meta name="description" content="' . $e($desc) . '" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="' . $e($title) . ' — Marginalia" />
  <meta property="og:description" content="' . $e($desc) . '" />
  <meta property="og:url" content="' . $e($urlAbs) . '" />
' . $ogImg . '  <meta name="twitter:card" content="' . $card . '" />
  <link rel="stylesheet" href="../style.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Oxygen:wght@300;400;700&display=swap" rel="stylesheet">
</head>

<body>

  <a href="#main-content" class="skip-link">Skip to main content</a>

  <nav>
    <a href="/" class="nav-logo"><img src="/Zmono-dark.png" alt="Zoe Allgaier — Home"></a>
    <div class="nav-links">
      <a href="/marginalia/">All</a>
      <a href="/marginalia/?filter=posts">Posts</a>
      <a href="/marginalia/?filter=finds">Finds</a>
      <a href="/marginalia/?filter=photos">Photos</a>
      <a href="/marginalia/?filter=library">Library</a>
    </div>
  </nav>

  <main id="main-content" tabindex="-1">
    <article class="post-wrap">

      <a href="../" class="back-link">← All entries</a>

      <span class="post-eyebrow">' . $e($eyebrow) . '</span>
      <h1 class="post-title">' . $e($title) . '</h1>

      <div class="post-meta">
        <span class="post-date">' . $e($dateFmt) . '</span>
        <div class="tags">
' . $tagHtml . '      </div>
    </div>

      <div class="post-body">

' . $bodyHtml . '

    </div>

    </article>
  </main>

  <footer id="contact">
    <p class="footer-prompt">If you\'ve got a project where graphic, motion, and web all need to show up as one thing, I\'d love to hear about it.</p>
    <a href="mailto:zoeallgaier@gmail.com" class="footer-email">zoeallgaier@gmail.com</a>
    <div class="footer-bottom">
      <span>Zoe Allgaier</span>
      <span>© 2026</span>
    </div>
  </footer>

  <script src="../main.js"></script>

  <script src="/js/footer.js"></script>
</body>
</html>
';

  if (file_put_contents("$POSTS_DIR/$slug.html", $html) === false)
    return ['error' => 'Could not write the post page.'];
  return ['url' => $url];
}

/* Save an uploaded image: fix rotation, downscale, re-encode. Returns web path or error. */
// Read a JPEG's EXIF Orientation (1-8) without relying on the exif extension,
// which isn't installed on all shared hosts. Returns 1 (normal) if unknown.
function jpeg_orientation($path) {
  if (function_exists('exif_read_data')) {
    $exif = @exif_read_data($path);
    if (!empty($exif['Orientation'])) return (int)$exif['Orientation'];
  }
  $fp = @fopen($path, 'rb');
  if (!$fp) return 1;
  $ori = 1;
  try {
    if (fread($fp, 2) !== "\xFF\xD8") return 1;          // not a JPEG (no SOI)
    while (!feof($fp)) {
      $marker = fread($fp, 2);
      if (strlen($marker) < 2 || $marker[0] !== "\xFF") break;
      $m = ord($marker[1]);
      if ($m === 0xD9 || $m === 0xDA) break;              // EOI or start of scan
      $lenb = fread($fp, 2);
      if (strlen($lenb) < 2) break;
      $len = (ord($lenb[0]) << 8) + ord($lenb[1]);
      if ($len < 2) break;
      $seg = fread($fp, $len - 2);
      if ($m !== 0xE1 || substr($seg, 0, 6) !== "Exif\x00\x00") continue;
      $tiff = substr($seg, 6);
      $le = substr($tiff, 0, 2) === "II";                // byte order
      $u16 = fn($s) => $le ? (ord($s[0]) | (ord($s[1]) << 8)) : ((ord($s[0]) << 8) | ord($s[1]));
      $u32 = fn($s) => $le
        ? (ord($s[0]) | (ord($s[1]) << 8) | (ord($s[2]) << 16) | (ord($s[3]) << 24))
        : ((ord($s[0]) << 24) | (ord($s[1]) << 16) | (ord($s[2]) << 8) | ord($s[3]));
      $ifd = $u32(substr($tiff, 4, 4));
      $n = $u16(substr($tiff, $ifd, 2));
      for ($i = 0; $i < $n; $i++) {
        $entry = substr($tiff, $ifd + 2 + $i * 12, 12);
        if (strlen($entry) < 12) break;
        if ($u16(substr($entry, 0, 2)) === 0x0112) {      // Orientation tag
          $ori = $u16(substr($entry, 8, 2));
          break;
        }
      }
      break;
    }
  } finally { fclose($fp); }
  return ($ori >= 1 && $ori <= 8) ? $ori : 1;
}

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
    // Respect EXIF orientation for JPEGs from phones. exif_read_data isn't
    // guaranteed on shared hosting, so fall back to a byte-level reader — GD
    // never auto-applies orientation, so if we skip this photos come out rotated.
    if ($mime === 'image/jpeg') {
      $o = jpeg_orientation($file['tmp_name']);
      // 5/7 are transpose/transverse (mirror + rotate); mirror first, then rotate.
      if ($o === 2 || $o === 4 || $o === 5 || $o === 7) imageflip($img, IMG_FLIP_HORIZONTAL);
      if ($o === 3 || $o === 4)      $img = imagerotate($img, 180, 0);
      elseif ($o === 6 || $o === 7)  $img = imagerotate($img, -90, 0);
      elseif ($o === 8 || $o === 5)  $img = imagerotate($img, 90, 0);
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
  #body { min-height: 14rem; line-height: 1.6; }
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

  /* Markdown toolbar — formatting buttons read as a squared toolbar; the Preview
     toggle is a distinct round outlined chip that inverts (fills) when active. */
  .md-tools-row { display: flex; justify-content: space-between; align-items: center; margin-top: 1.1rem; margin-bottom: .55rem; }
  .md-tools-row label { margin: 0; }
  .md-preview-toggle {
    font: inherit; font-size: .78rem; letter-spacing: .02em; padding: .34rem .9rem; cursor: pointer;
    color: var(--muted); background: none; border: 1px solid var(--rule); border-radius: 999px;
  }
  .md-preview-toggle:active { opacity: .8; }
  .md-preview-toggle[aria-pressed="true"] { background: var(--text); color: var(--bg); border-color: var(--text); }
  .md-toolbar { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .65rem; }
  .md-toolbar button {
    font: inherit; font-size: .82rem; line-height: 1.35; padding: .38rem .7rem; cursor: pointer;
    color: var(--text); background: var(--field); border: 1px solid var(--rule); border-radius: 8px;
  }
  .md-toolbar button:active { opacity: .8; }

  /* Live preview — approximates the post-body styles */
  .preview { margin-top: .6rem; padding: 1rem 1.1rem; border: 1px dashed var(--rule); border-radius: 8px; }
  .preview:empty::before { content: 'Nothing to preview yet.'; color: var(--muted); font-size: .85rem; }
  .preview p { margin: 0 0 1em; }
  .preview h2 { font-family: 'Instrument Serif', serif; font-style: italic; font-weight: 400;
                font-size: 1.7rem; line-height: 1.15; margin: 1.4rem 0 .8rem; }
  .preview h3 { font-family: 'Instrument Serif', serif; font-weight: 400; font-size: 1.35rem;
                margin: 1.4rem 0 .6rem; }
  .preview blockquote { border-left: 3px solid var(--text); padding-left: 1rem; margin: 1.2rem 0;
                        color: var(--muted); font-style: italic; }
  .preview .litany { font-family: 'Instrument Serif', serif; font-style: italic; font-size: 1.25rem;
                     line-height: 1.4; margin: 1.2rem 0; }
  .preview ul { padding-left: 1.3em; margin: 0 0 1em; }
  .preview a { text-decoration: underline; }
  .cheat { font-size: .82rem; color: var(--muted); margin-top: .5rem; }
  .cheat code { background: var(--field); padding: .05rem .3rem; border-radius: 4px; }
  .cheat div { margin: .2rem 0; }
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
      &nbsp;<a href="/marginalia/" target="_blank">View feed →</a>
      <?php if (!empty($added['url'])): ?>&nbsp;·&nbsp;<a href="/marginalia/<?= htmlspecialchars($added['url']) ?>" target="_blank">Open post →</a><?php endif; ?>
    </div>
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

    <div class="field-group" data-show="post">
      <label for="eyebrow">Kind</label>
      <select id="eyebrow" name="eyebrow">
        <option>Essay</option>
        <option>Rant</option>
        <option>Review</option>
        <option>Note</option>
        <option>Project</option>
      </select>
    </div>

    <div class="field-group" data-show="find,library">
      <label for="url" id="url-label">Link</label>
      <input id="url" type="url" name="url" placeholder="https://…" autocomplete="off">
      <p class="hint" id="url-hint">External link for finds.</p>
    </div>

    <div class="field-group" data-show="post">
      <div class="md-tools-row">
        <label for="body" style="margin:0">Write the post</label>
        <button type="button" class="md-preview-toggle" id="previewToggle" aria-pressed="false">Preview</button>
      </div>
      <div class="md-toolbar" aria-label="Formatting">
        <button type="button" data-md="h2">Statement</button>
        <button type="button" data-md="h3">Heading</button>
        <button type="button" data-md="bold"><b>B</b></button>
        <button type="button" data-md="italic"><i>I</i></button>
        <button type="button" data-md="quote">❝ Quote</button>
        <button type="button" data-md="litany">Litany</button>
        <button type="button" data-md="list">• List</button>
        <button type="button" data-md="link">Link</button>
      </div>
      <textarea id="body" name="body" placeholder="Write in Markdown. Blank line = new paragraph."></textarea>
      <div class="preview" id="preview" hidden></div>
      <details class="cheat">
        <summary class="hint">Formatting cheatsheet</summary>
        <div><code>## Big statement</code> — oversized italic pull-quote</div>
        <div><code>### Section heading</code></div>
        <div><code>**bold**</code> · <code>*italic*</code></div>
        <div><code>&gt; a quote</code></div>
        <div><code>~ line one</code> / <code>~ line two</code> — litany refrain</div>
        <div><code>- a list item</code></div>
        <div><code>[link text](https://…)</code></div>
      </details>
    </div>

    <div class="field-group" data-show="photo,post,find,library">
      <label for="image" id="image-label">Photo</label>
      <input id="image" type="file" name="image" accept="image/*">
      <p class="hint" id="image-hint">Big phone photos get resized automatically. Optional.</p>
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
        t === 'library' ? 'Author / year' : t === 'photo' ? 'Caption'
        : t === 'post' ? 'Feed summary (optional)' : 'Note';
      document.getElementById('image-hint').textContent =
        t === 'post' ? 'Optional cover image (also used as the feed thumbnail).'
        : 'Big phone photos get resized automatically. Optional.';
      document.getElementById('title-label').textContent = t === 'library' ? 'Book title' : 'Title';
    }
    document.querySelectorAll('input[name=type]').forEach(r => r.addEventListener('change', sync));
    sync();

    // ── Markdown toolbar ──
    const body = document.getElementById('body');
    function surround(pre, post, placeholder) {
      const s = body.selectionStart, e = body.selectionEnd;
      const sel = body.value.slice(s, e) || placeholder;
      body.setRangeText(pre + sel + post, s, e, 'end');
      body.focus();
    }
    function linePrefix(prefix) {
      const s = body.selectionStart;
      let lineStart = body.value.lastIndexOf('\n', s - 1) + 1;
      body.setRangeText(prefix, lineStart, lineStart, 'end');
      body.focus();
    }
    document.querySelectorAll('.md-toolbar button').forEach(b => b.addEventListener('click', () => {
      switch (b.dataset.md) {
        case 'bold':   surround('**', '**', 'bold'); break;
        case 'italic': surround('*', '*', 'italic'); break;
        case 'link':   surround('[', '](https://)', 'text'); break;
        case 'h2':     linePrefix('## '); break;
        case 'h3':     linePrefix('### '); break;
        case 'quote':  linePrefix('> '); break;
        case 'list':   linePrefix('- '); break;
        case 'litany': linePrefix('~ '); break;
      }
      if (previewOpen) refreshPreview();
    }));

    // ── Live preview (rendered by the same PHP, so it always matches) ──
    const preview = document.getElementById('preview');
    const toggle = document.getElementById('previewToggle');
    let previewOpen = false, timer = null;
    async function refreshPreview() {
      try {
        const r = await fetch(location.pathname, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'action=preview&body=' + encodeURIComponent(body.value)
        });
        preview.innerHTML = await r.text();
      } catch (_) {}
    }
    toggle.addEventListener('click', () => {
      previewOpen = !previewOpen;
      preview.hidden = !previewOpen;
      toggle.textContent = previewOpen ? 'Hide preview' : 'Preview';
      toggle.setAttribute('aria-pressed', previewOpen ? 'true' : 'false');
      if (previewOpen) refreshPreview();
    });
    body.addEventListener('input', () => {
      if (!previewOpen) return;
      clearTimeout(timer); timer = setTimeout(refreshPreview, 300);
    });
  </script>
<?php endif; ?>

</div>
</body>
</html>
