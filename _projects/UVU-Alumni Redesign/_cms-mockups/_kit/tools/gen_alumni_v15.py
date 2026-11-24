"""Alumni v1.5 heroes: Podcast (p05) and Job Shadow (FL_0090) move from plain heroes to photo heroes."""
import sys; sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover
from gen_images2 import right_weighted
from gen_images3 import save_jpg
A = '/mnt/user-data/outputs/cms-mockups'
D = '/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_work/photos/'
for pg, name, src, (mx, my) in [('forever-wolverines-podcast', 'podcast-header', D + 'p05.jpg', (.55, .4)),
                                ('alumni-job-shadow', 'job-shadow-header', '/tmp/gv/imgs/20240517_FL_Lifestyle_JED_0090.jpg', (.62, .42))]:
    im = Image.open(src).convert('RGB')
    save_jpg(right_weighted(im, 1250, .4), f'{A}/{pg}/assets/{name}.jpg')
    m = cover(im, 1080, 1350, mx, my)
    save_jpg(m, f'{A}/{pg}/assets/{name}-mobile.jpg'); save_jpg(m, f'{A}/_handoff/mobile-headers/{name}-mobile.jpg')
