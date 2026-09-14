# zoeallgaier.com

Portfolio and **marginalia** (a personal feed of posts, finds, library entries
and photos) for Zoe Allgaier.

Hand-written HTML, CSS and vanilla JS — no framework, no build step, no
dependencies. The repo *is* the site: what's on `main` is what's live.

## How it's hosted

GitHub Pages, deployed by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
on every push to `main`. The custom domain lives in [`CNAME`](CNAME).

The workflow does one thing beyond uploading: it appends the commit SHA to
every local `.css`/`.js` reference (`style.css?v=1a2b3c4d`) so a design change
is never hidden behind a browser's cached copy of the old stylesheet.

`.nojekyll` matters more than it looks — without it GitHub Pages runs Jekyll,
which silently drops every folder starting with an underscore, and all of the
site's imagery lives in `_assets/`.

## Layout

```
index.html            Work grid (the numbered project cards)
about.html            Bio
<project>.html        One page per project — elysium, tria, psb25, psb26, …
css/base.css          Shared chrome + design tokens — edit shared styles HERE
css/*.css             Page-specific styles layered on top of base
js/chrome.js          Injects the shared nav/footer into portfolio pages
js/app.js             Swaps <main> between pages instead of reloading
js/backdrop.js        The one fixed glow + dot grid behind every page
marginalia/           The feed: content.json (data) + main.js (renderer)
marginalia/posts/     Long-form written posts, one HTML file each
_assets/              All imagery, grouped by project
fonts/                Self-hosted Instrument Serif + Oxygen (woff2)
scripts/              optimize-images.py — run after adding imagery
```

Shared chrome is defined once in `css/base.css` and `js/chrome.js` rather than
copy-pasted per page, so nav and footer changes only need making in one place.

## The portfolio as an app

Every portfolio page is a complete HTML document — open any of them directly
and it works. On top of that, `js/app.js` takes over internal links: it fetches
the next page, swaps its `<main>` into the current document and updates the
URL, so the nav, the footer and the background are never rebuilt. Content
blurs out and back in around the swap; the background eases across to the new
page's palette at the same time.

That background is `js/backdrop.js` — one fixed layer for the whole site,
replacing the per-page hero canvas and gradient. A page says which palette it
wants on its `<main>`:

```html
<main id="main-content" data-backdrop="project"
      data-g1="rgba(236, 120, 160, 0.22)" data-g2="rgba(120, 150, 240, 0.2)">
```

`data-backdrop` is `home`, `about`, `project` or `quiet` (the reading pages).
Project pages give their two colours, and the `.next-project` link at the foot
carries the colours of the page it leads to, so the background starts drifting
towards the next project as you scroll into it.

Anything the router can't take — an external link, a file, marginalia, a failed
fetch — falls through to an ordinary page load, so nothing depends on the JS
succeeding.

## Adding to marginalia

The feed renders from [`marginalia/content.json`](marginalia/content.json).
Add a new entry to the **top** of the array and push:

```jsonc
{ "type": "photo", "image": "/_assets/marginalia/my-photo.jpg",
  "note": "Caption goes here.", "date": "2026-08-28" }
```

`type` is one of `post`, `find`, `library`, or `photo`, each with its own
colour treatment. Any entry may carry an `image`; a bare image opens in the
lightbox, one paired with a `url` becomes a link instead.

Drop the image in `_assets/marginalia/` alongside it. Resize before committing
— nothing on the site needs to be wider than about 2400px.

A long-form piece gets its own file in `marginalia/posts/` (copy the nearest
existing post as a starting point) and a `post` entry pointing at it.

## Working locally

Any static server will do; paths are absolute, so open the site at the server
root rather than as `file://`:

```sh
python3 -m http.server 8000
# → http://localhost:8000
```

## Images

The pages never make a visitor download an original. Every image on the home
grid and in a project gallery has WebP copies at display sizes beside it
(`name-800.webp`, `name-1400.webp`, `name-2000.webp`) and a `srcset` pointing
at them, so a phone pulls an 800px WebP instead of a multi-megabyte JPEG.

After adding or replacing an image in a page's `.work` grid or `.gallery`,
just put the plain `<img src="/_assets/…">` in the HTML and run:

```sh
python3 scripts/optimize-images.py
```

It shrinks the original to 2400px / JPEG 82 if it's bigger, writes the WebPs,
and fills in `srcset`/`sizes` for you. Re-running is safe.

Gallery videos should be short, silent, and re-encoded before committing — a
1080px H.264 loop is ~1–2MB, where an export straight from After Effects or
Premiere is often 5–10MB. With ffmpeg:

```sh
ffmpeg -i in.mp4 -an -vf "scale='if(lte(iw,ih),min(1080,iw),-2)':'if(lte(iw,ih),-2,min(1080,ih))'" \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -movflags +faststart out.mp4
ffmpeg -i out.mp4 -frames:v 1 -c:v libwebp -quality 78 out-poster.webp
```

…and give the `<video>` a `poster="…-poster.webp"` so the cell isn't blank
while it loads.

## Fonts

Instrument Serif and Oxygen are served from `/fonts` (declared at the top of
`css/base.css`), not Google Fonts — one less connection to open before the
first screen can paint. Each page preloads the two faces that screen uses.
