"""Alumni system imagery: 10.25-degree IA photo frames + 1920x700 heroes with the standard green gradient."""
import math, os, sys, json
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/xr')
from xd2svg import XD

OUT = '/mnt/user-data/outputs/cms-mockups'
DUMP = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_work/photos/'
XDS = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_xd-source'
r = XD(XDS)
GREEN = (24, 92, 51)
MEADOW = (197, 217, 122)
ANGLE = 10.25
SCALE = 1.5  # export density for crisp frames on retina


def cover(im, W, H, fx=.5, fy=.5, zoom=1.0, place=(.5, .5)):
    """Crop im to WxH (cover), keeping focal point (fx,fy) at `place` within the frame."""
    iw, ih = im.size
    s = max(W / iw, H / ih) * zoom
    sw, sh = iw * s, ih * s
    left = fx * sw - place[0] * W
    top = fy * sh - place[1] * H
    left = max(0, min(left, sw - W)); top = max(0, min(top, sh - H))
    big = im.resize((round(sw), round(sh)), Image.LANCZOS)
    return big.crop((round(left), round(top), round(left) + W, round(top) + H))


def xd_crop(board, name, W, H):
    """Rectangular crop of an XD image fill using XD's own pattern offsets."""
    it = r.find(r.board(board)[1], name)
    p = it['style']['fill']['pattern']; m = p['meta']['ux']
    im = Image.open(r.img_path(m['uid'])).convert('RGB')
    iw, ih = im.size
    # pattern width/height are original px; res images are downscaled. Work in res px.
    s0 = max(W / iw, H / ih); s = s0 * m.get('scale', 1)
    sw, sh = iw * s, ih * s
    left = (sw - W) / 2 - m.get('offsetX', 0) * iw * s0
    top = (sh - H) / 2 - m.get('offsetY', 0) * ih * s0
    big = im.resize((round(sw), round(sh)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), 'white')
    c.paste(big, (round(-left), round(-top)))
    return c


def frame(photo, out, W=820, H=731):
    """IA 10.25° parallelogram photo + offset Pale Meadow outline, transparent PNG."""
    k = SCALE
    W2, H2 = round(W * k), round(H * k)
    slant = H2 * math.tan(math.radians(ANGLE))
    off = (-32 * k, 30 * k)
    pad = round(8 * k)
    cw = W2 + round(abs(off[0])) + 2 * pad
    ch = H2 + round(off[1]) + 2 * pad
    ox, oy = pad + round(abs(off[0])), pad
    poly = [(ox + slant, oy), (ox + W2, oy), (ox + W2 - slant, oy + H2), (ox, oy + H2)]
    canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    # outline first (behind)
    d = ImageDraw.Draw(canvas)
    opoly = [(x + off[0], y + off[1]) for x, y in poly]
    d.line(opoly + [opoly[0]], fill=MEADOW + (255,), width=round(3 * k), joint='curve')
    ph = photo.resize((W2, H2), Image.LANCZOS) if photo.size != (W2, H2) else photo
    mask = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    layer = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    layer.paste(ph.convert('RGBA'), (ox, oy))
    canvas = Image.alpha_composite(canvas, Image.composite(layer, Image.new('RGBA', (cw, ch), (0, 0, 0, 0)), mask))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, optimize=True)
    return out


def placeholder(out, label='PHOTO TBD', W=820, H=731):
    k = SCALE
    ph = Image.new('RGB', (round(W * k), round(H * k)), (226, 230, 227))
    d = ImageDraw.Draw(ph)
    try:
        from PIL import ImageFont
        f = ImageFont.truetype('/tmp/xr/node_modules/@fontsource/rajdhani/files/rajdhani-latin-700-normal.woff', 44)
    except Exception:
        f = None
    d.text((ph.width / 2, ph.height / 2), label, fill=(93, 107, 99), anchor='mm', font=f)
    return frame(ph, out, W, H)


def hero(photo, out, fx, fy, zoom=1.0, place=(.7, .45)):
    W, H = 1920, 700
    c = cover(photo, W, H, fx, fy, zoom, place).convert('RGBA')
    stops = [(0, 1.0), (1 - 0.5467979907989502, 0.8313725490196079), (1, 0.0)]
    a = Image.new('L', (W, 1))
    for x in range(W):
        t = min(x / 1780, 1.0); v = 0
        for (p0, a0), (p1, a1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                v = a0 + (a1 - a0) * (t - p0) / (p1 - p0); break
        a.putpixel((x, 0), round(v * 255))
    ov = Image.new('RGBA', (W, H), GREEN + (255,)); ov.putalpha(a.resize((W, H)))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.alpha_composite(c, ov).convert('RGB').save(out, quality=84, optimize=True, progressive=True)


def dump(n):
    return Image.open(f'{DUMP}p{n:02d}.jpg').convert('RGB')


FW, FH = round(820 * SCALE), round(731 * SCALE)
jobs = {
    # page: [(kind, args)]
}
if __name__ == '__main__':
    A = lambda page, f: f'{OUT}/{page}/assets/{f}'
    # ---------- heroes from the photo dump ----------
    hero(dump(18), A('graduating-students', 'alumni-grads-header.jpg'), .62, .40)
    hero(dump(21), A('alumni-scholarships', 'alumni-scholarships-header.jpg'), .58, .45)
    hero(dump(22), A('about-saa', 'alumni-saa-header.jpg'), .64, .45)
    # ---------- frames from the photo dump ----------
    frame(cover(dump(12), FW, FH, .40, .45), A('alumni-home', 'alumni-home-stayconnected.png'))
    frame(cover(dump(25), FW, FH, .50, .40), A('alumni-scholarships', 'alumni-scholarships-intro.png'))
    frame(cover(dump(5), FW, FH, .50, .45), A('about-saa', 'alumni-saa-what.png'))
    frame(cover(dump(16), FW, FH, .50, .35), A('about-saa', 'alumni-saa-qualify.png'))
    # ---------- frames re-cut from XD photos (same crops, new 10.25° frame) ----------
    xd = [('Benefits', '20260325_Cap & Gown Photos for Graduates_EM_00289', 'alumni-benefits', 'alumni-benefits-becomeamember.png'),
          ('Benefits', '20251013_UMC_APFY_JP_JED_0942', 'alumni-benefits', 'alumni-benefits-opportunities.png'),
          ('Benefits', '20251112_Employee Lifestyle_Pt 2_1012', 'alumni-benefits', 'alumni-benefits-resources.png'),
          ('Graduates', '20240503_ED_Grad Bash_JED_0480', 'graduating-students', 'alumni-grads-celebrate.png'),
          ('Graduates', '20240203_MBB vs Grand Canyon_KE_2056', 'graduating-students', 'alumni-grads-events.png'),
          ('Graduates', '20251021_APFY Joe_KE_0602', 'graduating-students', 'alumni-grads-connect.png'),
          ('Alumni Awards', '20260204_2026 Alumni Awards_EM_00134', 'alumni-awards', 'alumni-awards-honoring.png'),
          ('Alumni Awards', '20250219_2025 Alumni Awards_EM_0474', 'alumni-awards', 'alumni-awards-tradition.png'),
          ('License Plate', '20250730_Student Alumni Ambassadors photoshoot_KE_0074', 'uvu-license-plate', 'alumni-licenseplate-support.png')]
    for board, name, page, f in xd:
        frame(xd_crop(board, name, FW, FH), A(page, f))
    # contact band: team photo, same frame system
    team = Image.open(r.img_path('c2d2739fa7a62b7e6a57bf65d9646bde')).convert('RGB')
    frame(cover(team, FW, FH, .5, .55), f'{OUT}/_shared-assets/alumni-contact-team.png')
    placeholder(A('uvu-license-plate', 'placeholder-plate-design.png'), 'PLATE DESIGN TBD')
    print('done')
