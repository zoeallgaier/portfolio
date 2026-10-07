#!/usr/bin/env python3
"""
optimize-images.py — make the portfolio's imagery fast without touching how
it looks.

Run it after adding or swapping an image on the home grid or a project
gallery:

    python3 scripts/optimize-images.py

What it does, for every image the pages actually use:
  • Shrinks the original in place to at most 2400px on the long edge at JPEG
    quality 82 (only when that meaningfully saves bytes). The original stays
    the `src` — it's the fallback, and what og:image previews point at.
  • Writes WebP copies beside it at display sizes (name-800.webp,
    name-1400.webp, name-2000.webp), never upscaled.
  • Rewrites that <img>'s `srcset` + `sizes`, so a phone downloads an 800px
    WebP instead of a multi-megabyte JPEG, and a retina desktop gets the size
    it really needs.

`sizes` accounts for object-fit: cover — a wide image in a square gallery
cell is sized by its height, so it asks for proportionally more width.

Safe to re-run: existing WebPs are reused unless the original is newer, and
srcset/sizes are replaced rather than duplicated. Needs Pillow
(`python3 -m pip install Pillow`).
"""
import re
from pathlib import Path
from urllib.parse import quote, unquote

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent

MAX_EDGE = 2400
JPEG_QUALITY = 82
WEBP_QUALITY = 78
WIDTHS = (800, 1400, 2000)

# Slot width of each layout (see css/index.css .work, css/project.css
# .gallery). 20rem ≈ the desktop sidebar; phones are one column.
LAYOUTS = {
    # Home work grid: two columns of 16:9 cards with 2rem padding.
    'work':    {'box': 16 / 9, 'phone': '100vw - 3rem', 'desktop': '(100vw - 20rem) / 2 - 4rem'},
    # Project galleries: two columns of square cells, edge to edge.
    'gallery': {'box': 1.0,    'phone': '100vw',        'desktop': '(100vw - 20rem) / 2'},
    # Project heroes: one full-width image at its own aspect (no box to fill).
    'hero':    {'box': None,   'phone': '100vw',        'desktop': '100vw - 20rem'},
}

# Which part of which page holds each layout's images.
BLOCK = {
    'work':    re.compile(r'<section class="work".*?</section>', re.S),
    'gallery': re.compile(r'<div class="gallery">.*?</div>', re.S),
    'hero':    re.compile(r'<figure class="project-hero">.*?</figure>', re.S),
}

IMG = re.compile(r'<img\b[^>]*>')
SRC = re.compile(r'\ssrc="([^"]+)"')


def load(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)  # bake in camera rotation before resizing
    return im


def shrink_original(path):
    """Resize/recompress the original in place if it's oversized."""
    before = path.stat().st_size
    im = load(path)
    icc = im.info.get('icc_profile')
    w, h = im.size
    scale = min(1, MAX_EDGE / max(w, h))
    if scale < 1:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)

    tmp = path.with_name(path.name + '.tmp')
    if path.suffix.lower() in ('.jpg', '.jpeg'):
        if im.mode not in ('RGB', 'L'):
            im = im.convert('RGB')
        im.save(tmp, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True, icc_profile=icc)
    elif path.suffix.lower() == '.png':
        im.save(tmp, 'PNG', optimize=True, icc_profile=icc)
    else:
        return

    after = tmp.stat().st_size
    # Keep the new file only if it's a real saving (or the old one was too big).
    if scale < 1 or after < before * 0.85:
        tmp.replace(path)
        print(f'  shrank  {path.relative_to(ROOT)}  {before // 1024}K → {after // 1024}K')
    else:
        tmp.unlink()


def webp_variants(path):
    """Write name-<w>.webp beside the original; return [(url_path, w, h)]."""
    im = None
    src_w, src_h = load(path).size
    widths = sorted({w for w in WIDTHS if w < src_w} | {min(src_w, WIDTHS[-1])})
    out = []
    for w in widths:
        dest = path.with_name(f'{path.stem}-{w}.webp')
        if not dest.exists() or dest.stat().st_mtime < path.stat().st_mtime:
            im = im or load(path)
            icc = im.info.get('icc_profile')
            has_alpha = im.mode in ('RGBA', 'LA') or 'transparency' in im.info
            frame = im.convert('RGBA' if has_alpha else 'RGB')
            h = round(src_h * w / src_w)
            frame.resize((w, h), Image.LANCZOS).save(
                dest, 'WEBP', quality=WEBP_QUALITY, method=6, icc_profile=icc)
        out.append((dest, w))
    return out, src_w / src_h


def sizes_for(layout, aspect):
    spec = LAYOUTS[layout]
    # object-fit: cover — wider-than-the-box images fill by height.
    f = max(1.0, aspect / spec['box']) if spec['box'] else 1.0
    def slot(expr):
        return f'calc(({expr}) * {f:.2f})' if f > 1.005 else f'calc({expr})'
    return f'(max-width: 768px) {slot(spec["phone"])}, {slot(spec["desktop"])}'


def url_of(path):
    return quote('/' + path.relative_to(ROOT).as_posix())


def process_tag(tag, layout, done):
    m = SRC.search(tag)
    if not m or not m.group(1).startswith('/_assets/'):
        return tag
    path = ROOT / unquote(m.group(1)).lstrip('/')
    if path.suffix.lower() not in ('.jpg', '.jpeg', '.png') or not path.exists():
        return tag

    if path not in done:
        shrink_original(path)
        done[path] = webp_variants(path)
    variants, aspect = done[path]

    srcset = ', '.join(f'{url_of(p)} {w}w' for p, w in variants)
    tag = re.sub(r'\s(srcset|sizes)="[^"]*"', '', tag)
    end = SRC.search(tag).end()
    return tag[:end] + f' srcset="{srcset}" sizes="{sizes_for(layout, aspect)}"' + tag[end:]


def main():
    done = {}
    for page in sorted(ROOT.glob('*.html')):
        html = page.read_text()
        new = html
        for layout, block in BLOCK.items():
            new = block.sub(
                lambda b: IMG.sub(lambda t: process_tag(t.group(0), layout, done), b.group(0)),
                new)
        if new != html:
            page.write_text(new)
            print(f'updated {page.name}')

    # Social preview images: not on screen, but shrink them so link unfurls
    # (iMessage, Slack) are quick.
    for page in sorted(ROOT.glob('*.html')):
        for url in re.findall(r'og:image" content="https://zoeallgaier\.com(/_assets/[^"]+)"', page.read_text()):
            path = ROOT / unquote(url).lstrip('/')
            if path.exists() and path not in done:
                shrink_original(path)
                done[path] = None


if __name__ == '__main__':
    main()
