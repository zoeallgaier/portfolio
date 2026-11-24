"""Giving v1.3 imagery: raw heroes (1920x700), phone heroes (1080x1350), photos (1200x900), card images (16:10), quote headshots."""
import sys, os, glob
sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover
from gen_images2 import right_weighted
from gen_images3 import save_jpg
OUT = '/mnt/user-data/outputs/giving-mockups'
N = '/tmp/xr/photos2/'
D = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_work/photos/'
L = '/tmp/gv/old/'
A = lambda pg, f: f'{OUT}/{pg}/assets/{f}'
ld = lambda p: Image.open(p).convert('RGB')
HO = f'{OUT}/_handoff/mobile-headers'
os.makedirs(HO, exist_ok=True)

heroes = {  # page: (source, desktop mode, fx, fy, mobile fx, fy)
    'give-home': (N + 'n11.jpg', ('cover', .58, .42), (.62, .4)),
    'ways-to-give': (D + 'p24.jpg', ('cover', .62, .42), (.66, .4)),
    'annual-giving': (D + 'p05.jpg', ('rw', 1250, .38), (.55, .4)),
    'memorial-gifts': (D + 'p10.jpg', ('rw', 1350, .42), (.36, .4)),
}
for pg, (src, mode, (mx, my)) in heroes.items():
    im = ld(src)
    d = cover(im, 1920, 700, mode[1], mode[2], 1.0, (.7, .45)) if mode[0] == 'cover' else right_weighted(im, mode[1], mode[2])
    save_jpg(d, A(pg, f'{pg}-header.jpg'))
    m = cover(im, 1080, 1350, mx, my)
    save_jpg(m, A(pg, f'{pg}-header-mobile.jpg'))
    save_jpg(m, f'{HO}/{pg}-header-mobile.jpg')

# split photos (4:3)
save_jpg(cover(ld(N + 'n08.jpg'), 1200, 900, .42, .4), A('give-home', 'give-change-lives.jpg'))
save_jpg(cover(ld(D + 'p13.jpg'), 1200, 900, .5, .42), A('annual-giving', 'annual-giving-impact.jpg'))
fl = ld(L + 'Ways to Give _ Utah Valley University_files/memorial-gifts-small.jpg')
save_jpg(cover(fl, 532, 400, .5, .5), A('memorial-gifts', 'memorial-gifts-flowers.jpg'))

# Ways to Give cards (16:10); small live images stay at native size
W = L + 'Ways to Give _ Utah Valley University_files/'
for f in ['giving-priorities-small', 'scholarships-1', 'annual-giving-small', 'memorial-gifts-small', 'gift-securities', 'gift-planning-small',
          'giving_eventsponsorship', 'matching-gifts-small', 'in-kind-donation', 'service-small']:
    im = ld(W + f + '.jpg')
    w = min(1200, im.width); h = round(w * 10 / 16)
    if h > im.height: h = im.height; w = round(h * 16 / 10)
    save_jpg(cover(im, w, h, .5, .45), A('ways-to-give', f.replace('_', '-').replace('-small', '') + '.jpg'))

# I Am UVU headshots cropped from the live graphics (square, 480px)
E = sorted(glob.glob(L + 'EMPLOYEE*_files/*-*.jpg'))
boxes = {'1728d81d': ('kyrsi-zamora', 190, 80), '2e86932d': ('garth-tino', 190, 70), '67c6c95e': ('troy-wilson', 1100, 100),
         '96cb6e50': ('deborah-marrott', 1130, 120), 'b2d87e8f': ('raymundo-yazzie', 190, 60), 'c5bd756d': ('karen-cushing', 190, 90)}
for f in E:
    k = os.path.basename(f)[:8]
    name, x, y = boxes[k]
    save_jpg(ld(f).crop((x, y, x + 340, y + 340)).resize((240, 240), Image.LANCZOS), A('employee-giving', f'iamuvu-{name}.jpg'))
print('done')
