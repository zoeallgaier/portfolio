"""Give hub (v1.4) imagery: featured fund cards (16:10) and the story portrait."""
import sys, os
sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover
from gen_images3 import save_jpg
OUT = '/mnt/user-data/outputs/giving-mockups'
L = '/tmp/gv/old/'
ld = lambda p: Image.open(p).convert('RGB')
P = L + 'Programs & Centers _ Utah Valley University_files/'
feat = {'scholarships': L + 'Ways to Give _ Utah Valley University_files/scholarships-1.jpg', 'first-gen': P + 'first-gen-card.jpg',
        'wolverine-club': L + 'Support UVU Student Athletes _ Utah Valley University_files/wolverin-club.jpg', 'library': P + 'fulton-library.jpg',
        'social-impact': P + 'center-for-social-impact-card.jpg', 'culinary': P + 'culinary-arts.jpg'}
for k, f in feat.items():
    im = ld(f); w = min(800, im.width); h = round(w * 10 / 16)
    if h > im.height: h = im.height; w = round(h * 1.6)
    save_jpg(cover(im, w, h, .5, .45), f'{OUT}/give-home/assets/feat-{k}.jpg')
# Kyrsi Zamora: real portrait (Oct. 2026 upload) for the Give story and her Employee Giving quote
k = ld('/tmp/gv/imgs/20210701_FYAC_Kyrsi Zamora_EF_0208a.jpg')
save_jpg(cover(k, 960, 1200, .5, .38), f'{OUT}/give-home/assets/story-kyrsi-zamora.jpg')
save_jpg(cover(k, 240, 240, .5, .3, 1.6), f'{OUT}/employee-giving/assets/iamuvu-kyrsi-zamora.jpg')
print('done')

# Employee Giving hero (v1.5): staff member helping a student
e = ld('/tmp/gv/imgs/20240517_FL_Lifestyle_JED_0166.jpg')
save_jpg(cover(e, 1920, 700, .6, .4, 1.0, (.7, .45)), f'{OUT}/employee-giving/assets/employee-giving-header.jpg')
save_jpg(cover(e, 1080, 1350, .72, .4), f'{OUT}/employee-giving/assets/employee-giving-header-mobile.jpg')
