"""Giving round 2 imagery + new /give hero (aerial)."""
import sys, os, glob, shutil
sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover
from gen_images2 import right_weighted
from gen_images3 import save_jpg
OUT = '/mnt/user-data/outputs/giving-mockups'
N = '/tmp/xr/photos2/'
D = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_work/photos/'
L = '/tmp/gv/old/'
I = '/tmp/gv/imgs/'
A = lambda pg, f: f'{OUT}/{pg}/assets/{f}'
ld = lambda p: Image.open(p).convert('RGB')
HO = f'{OUT}/_handoff/mobile-headers'
os.makedirs(HO, exist_ok=True)
AER1 = I + '20260414_Aerial Drone Photos Orem Campus_AM_0333.jpg'
AER2 = I + '20260414_Aerial Drone Photos Orem Campus_AM_0030.jpg'
heroes = {  # page: (source, ('cover', fx, fy) | ('rw', width, fy), (mobile fx, fy))
    'give-home': (AER1, ('cover', .55, .55), (.5, .72)),
    'colleges-schools': (AER2, ('cover', .5, .55), (.55, .72)),
    'programs-centers': (I + '20240517_FL_Lifestyle_JED_0090.jpg', ('cover', .6, .42), (.62, .42)),
    'student-affairs': (I + '20250221_CARE Hub_KE_00172.jpg', ('cover', .6, .4), (.62, .4)),
    'athletics': (L + 'Support UVU Student Athletes _ Utah Valley University_files/womens-basketball.jpg', ('rw', 1450, .45), (.5, .45)),
    'gifts-of-securities': (L + 'Ways to Give _ Utah Valley University_files/gift-securities.jpg', ('cover', .55, .5), (.5, .5)),
    'smith-college-engineering-technology': (D + 'p01.jpg', ('cover', .62, .45), (.62, .45)),
    'college-of-science': (I + '20240618_APFY Chloe_KE_0787.jpg', ('cover', .6, .2), (.6, .3)),
    'school-of-education': (I + '20240618_APFY Chloe_KE_0617.jpg', ('cover', .62, .4), (.66, .4)),
    'woodbury-school-business': (I + '20240529_UMC_APFY_JED_3522.jpg', ('cover', .6, .4), (.62, .4)),
    'college-humanities-social-sciences': (I + '20240329_FL_Lifestyle Shoot_EM_1219.jpg', ('rw', 1350, .42), (.5, .42)),
    'school-of-arts': (L + 'UVU School of the Arts _ Utah Valley University_files/music.jpg', ('rw', 1250, .45), (.3, .4)),
}
for pg, (src, mode, (mx, my)) in heroes.items():
    im = ld(src)
    d = cover(im, 1920, 700, mode[1], mode[2], 1.0, (.7, .45)) if mode[0] == 'cover' else right_weighted(im, mode[1], mode[2])
    save_jpg(d, A(pg, f'{pg}-header.jpg'))
    m = cover(im, 1080, 1350, mx, my)
    save_jpg(m, A(pg, f'{pg}-header-mobile.jpg'))
    save_jpg(m, f'{HO}/{pg}-header-mobile.jpg')

# thumbnails for fund units and cards (3:2, max 600 wide, never upscaled)
def thumb(src, out, w=600, ratio=(3, 2)):
    im = ld(src); tw = min(w, im.width); th = round(tw * ratio[1] / ratio[0])
    if th > im.height: th = im.height; tw = round(th * ratio[0] / ratio[1])
    save_jpg(cover(im, tw, th, .5, .45), out)

PAGES = {'Programs & Centers': 'programs-centers', 'Support CET Students': 'smith-college-engineering-technology', 'Support COS Students': 'college-of-science',
         'Support Future Educators': 'school-of-education', 'Support Future Entrepreneurs': 'woodbury-school-business',
         "Support UVU's College of Humanities & Social Sciences": 'college-humanities-social-sciences', 'UVU School of the Arts': 'school-of-arts'}
for key, pg in PAGES.items():
    for f in glob.glob(L + key + ' _ *_files/*.jpg'):
        if os.path.basename(f) in ('magnify.jpg',): continue
        thumb(f, A(pg, 'fund-' + os.path.basename(f).replace('_', '-')))
ATH = L + 'Support UVU Student Athletes _ Utah Valley University_files/'
for f in glob.glob(ATH + '*.jpg') + glob.glob(ATH + '*.png'):
    thumb(f, A('athletics', 'sport-' + os.path.splitext(os.path.basename(f))[0] + '.jpg'), 800, (16, 10))
SA = L + 'Support UVU Student Affairs _ Utah Valley University_files/'
for f in ['student-success-thumbnail.png', 'access-card2.jpg', 'enrollment-card1.jpg', 'student-development-well-being.jpg']:
    thumb(SA + f, A('student-affairs', 'area-' + os.path.splitext(f)[0] + '.jpg'), 800, (16, 10))
CS = L + 'Giving Opportunities in Colleges & Schools _ UVU_files/'
for f in glob.glob(CS + '*.jpg'):
    thumb(f, A('colleges-schools', 'college-' + os.path.basename(f)), 900, (16, 10))
print('done')

