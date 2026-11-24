"""v1.1 imagery: re-positioned heroes (subjects clear of the headline), new heroes for utility pages,
and frames from the new photo drop. Uses the same frame/hero recipe as gen_images.py."""
import sys
sys.path.insert(0, '/tmp/xr')
from PIL import Image, ImageFilter
from gen_images import cover, frame, hero, r, OUT, FW, FH, GREEN

N = '/tmp/xr/photos2/'
D = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_work/photos/'
A = lambda page, f: f'{OUT}/{page}/assets/{f}'


def load(p):
    return Image.open(p).convert('RGB')


def right_weighted(photo, wp, fy=.5):
    """1920x700 canvas: the photo scaled to width wp, pinned to the right edge, so the subject
    clears the headline column. The left strip is a blurred stretch of the photo's left edge;
    the hero gradient covers it at ~85-100% green, so it reads as tone, not image."""
    W, H = 1920, 700
    s = wp / photo.width
    ph = photo.resize((wp, round(photo.height * s)), Image.LANCZOS)
    if ph.height < H:
        s2 = H / ph.height
        ph = ph.resize((round(ph.width * s2), H), Image.LANCZOS)
    top = max(0, min(round(fy * ph.height - H / 2), ph.height - H))
    ph = ph.crop((0, top, ph.width, top + H))
    fw = W - ph.width + 400
    src = ph.crop((0, 0, min(fw, ph.width), H)).transpose(Image.FLIP_LEFT_RIGHT)
    canvas = src.resize((fw, H)).filter(ImageFilter.GaussianBlur(24))  # mirrored edge: same tones, no seam
    out = Image.new('RGB', (W, H))
    out.paste(canvas, (0, 0))
    ramp = Image.linear_gradient('L').rotate(90, expand=True).resize((380, H))  # 0 at left -> 255 at right
    ramp = ramp.transpose(Image.FLIP_LEFT_RIGHT) if ramp.getpixel((0, 0)) > ramp.getpixel((379, 0)) else ramp
    mask = Image.new('L', ph.size, 255)
    mask.paste(ramp, (0, 0))
    out.paste(ph, (W - ph.width, 0), mask)
    return out


def hero_from(canvas, out):
    # canvas is already 1920x700; reuse hero() for the standard gradient (fx/fy irrelevant at zoom 1)
    hero(canvas, out, .5, .5)


if __name__ == '__main__':
    # ---------- re-positioned heroes: subjects out from under the H1 ----------
    hero_from(right_weighted(load(r.img_path('4e28474a8d55874682eb75e4287cd208')), 1000, .40), A('alumni-benefits', 'alumni-benefits-header.jpg'))
    hero_from(right_weighted(load(D + 'p22.jpg'), 1480, .46), A('about-saa', 'alumni-saa-header.jpg'))
    hero_from(right_weighted(load(D + 'p18.jpg'), 1500, .40), A('graduating-students', 'alumni-grads-header.jpg'))
    # ---------- new heroes (utility pages) ----------
    hero_from(right_weighted(load(N + 'n09.jpg'), 1400, .40), A('alumni-diplomas', 'alumni-diplomas-header.jpg'))
    hero_from(right_weighted(load(N + 'n21.jpg'), 1180, .40), A('career-networking-resources', 'career-resources-header.jpg'))
    hero_from(right_weighted(load(N + 'n22.jpg'), 1250, .58), A('aviation-alumni-chapter', 'aviation-chapter-header.jpg'))
    # ---------- frames from the new photo drop ----------
    frame(cover(load(N + 'n19.jpg'), FW, FH, .47, .55), A('alumni-benefits', 'alumni-benefits-opportunities.png'))
    frame(cover(load(N + 'n13.jpg'), FW, FH, .52, .64), A('uvu-license-plate', 'alumni-licenseplate-support.png'))
    frame(cover(load(N + 'n12.jpg'), FW, FH, .60, .62, 1.15), A('uvu-license-plate', 'alumni-licenseplate-look.png'))
    # ---------- re-crop: Awards "tradition" had the honoree's head clipped by the frame's top edge ----------
    frame(cover(load(r.img_path('d226c29cab7b8617b73209ebe4698ebe')), FW, FH, .5, .38), A('alumni-awards', 'alumni-awards-tradition.png'))
    print('done')
