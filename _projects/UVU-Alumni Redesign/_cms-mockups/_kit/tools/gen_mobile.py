"""Vertical (4:5, 1080x1350) phone headers, people centered. Raw photos; the green fade is CSS.
Also writes _handoff/mobile-headers/ for Cesar (raw + a pre-faded fallback)."""
import sys, os, json, shutil
sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover, OUT
from gen_images2 import load
from gen_images3 import save_jpg
S = json.load(open('/tmp/xr/heroes_src.json'))
W, H = 1080, 1350
# key: (page folder, desktop header file, focal x, focal y, zoom)
J = {'home': ('alumni-home', 'alumni-home-header.jpg', .72, .35, 1.0),
     'benefits': ('alumni-benefits', 'alumni-benefits-header.jpg', .63, .4, 1.0),
     'grads': ('graduating-students', 'alumni-grads-header.jpg', .45, .4, 1.0),
     'scholar': ('alumni-scholarships', 'alumni-scholarships-header.jpg', .63, .4, 1.0),
     'saa': ('about-saa', 'alumni-saa-header.jpg', .62, .4, 1.0),
     'plate': ('uvu-license-plate', 'alumni-licenseplate-header.jpg', .55, .4, 1.0),
     'awards': ('alumni-awards', 'alumni-awards-header.jpg', .47, .4, 1.0),
     'diplomas': ('alumni-diplomas', 'alumni-diplomas-header.jpg', .52, .4, 1.0),
     'career': ('career-networking-resources', 'career-resources-header.jpg', .63, .4, 1.0),
     'aviation': ('aviation-alumni-chapter', 'aviation-chapter-header.jpg', .68, .4, 1.0)}
HO = f'{OUT}/_handoff/mobile-headers'
os.makedirs(HO, exist_ok=True)
G = (24, 92, 51)


def faded(im):
    """Same fade as the CSS: solid green at the bottom, clear by 45% from the top."""
    w, h = im.size
    ov = Image.new('RGBA', (w, h))
    px = ov.load()
    for y in range(h):
        t = y / h  # 0 top .. 1 bottom
        a = 0 if t < .45 else (min(1, (t - .45) / .3) ** 1.2 if t < .75 else 1)
        for x in range(w):
            px[x, y] = G + (round(a * 255),)
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')


for k, (pg, f, fx, fy, z) in J.items():
    im = cover(load(S[k]), W, H, fx, fy, z)
    mf = f.replace('-header.jpg', '-header-mobile.jpg')
    out = f'{OUT}/{pg}/assets/{mf}'
    save_jpg(im, out)
    shutil.copy(out, f'{HO}/{mf}')
    save_jpg(faded(im), f'{HO}/faded/{mf.replace(".jpg", "-faded.jpg")}')
    print(mf)
