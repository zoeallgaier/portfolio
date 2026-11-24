"""v1.2 imagery.
Heroes: RAW 1920x700 photos (no baked gradient; the fade is CSS), subject in the right half.
Photos: plain JPG crops (4:3, or 4:5 for portrait subjects); the uvu.edu-style accents are CSS."""
import sys, os
sys.path.insert(0, '/tmp/xr')
from PIL import Image
from gen_images import cover, xd_crop, OUT
from gen_images2 import right_weighted, load, N, D, r

A = lambda page, f: f'{OUT}/{page}/assets/{f}'
LW, LH = 1200, 900     # landscape photo
PW, PH = 960, 1200     # portrait photo


def save_jpg(im, out, q=82):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.convert('RGB').save(out, quality=q, optimize=True, progressive=True)


def xdimg(board, name):
    it = r.find(r.board(board)[1], name)
    return load(r.img_path(it['style']['fill']['pattern']['meta']['ux']['uid']))


if __name__ == '__main__':
    # ---------- heroes (raw) ----------
    save_jpg(xd_crop('Alumni Home', '20240502_Comencement 2024_KE_0552', 1920, 700), A('alumni-home', 'alumni-home-header.jpg'))
    save_jpg(right_weighted(load(r.img_path('4e28474a8d55874682eb75e4287cd208')), 1050, .40), A('alumni-benefits', 'alumni-benefits-header.jpg'))
    save_jpg(right_weighted(load(D + 'p18.jpg'), 1500, .40), A('graduating-students', 'alumni-grads-header.jpg'))
    save_jpg(cover(load(D + 'p21.jpg'), 1920, 700, .58, .45, 1.0, (.7, .45)), A('alumni-scholarships', 'alumni-scholarships-header.jpg'))
    save_jpg(right_weighted(load(D + 'p22.jpg'), 1480, .46), A('about-saa', 'alumni-saa-header.jpg'))
    save_jpg(right_weighted(load(N + 'n19.jpg'), 1100, .56), A('uvu-license-plate', 'alumni-licenseplate-header.jpg'))
    save_jpg(xd_crop('Alumni Awards', '20260204_2026 Alumni Awards_EM_00013 (1)', 1920, 700), A('alumni-awards', 'alumni-awards-header.jpg'))
    save_jpg(right_weighted(load(N + 'n09.jpg'), 1400, .40), A('alumni-diplomas', 'alumni-diplomas-header.jpg'))
    save_jpg(right_weighted(load(N + 'n21.jpg'), 1180, .40), A('career-networking-resources', 'career-resources-header.jpg'))
    save_jpg(right_weighted(load(N + 'n22.jpg'), 1250, .58), A('aviation-alumni-chapter', 'aviation-chapter-header.jpg'))

    # ---------- photos (plain crops) ----------
    L = lambda im, fx, fy, z=1.0: cover(im, LW, LH, fx, fy, z)
    P = lambda im, fx, fy, z=1.0: cover(im, PW, PH, fx, fy, z)
    save_jpg(L(load(D + 'p12.jpg'), .40, .45), A('alumni-home', 'alumni-home-stayconnected.jpg'))
    save_jpg(L(load(D + 'p25.jpg'), .50, .40), A('alumni-scholarships', 'alumni-scholarships-intro.jpg'))
    save_jpg(L(load(D + 'p05.jpg'), .50, .45), A('about-saa', 'alumni-saa-what.jpg'))
    save_jpg(P(load(D + 'p16.jpg'), .50, .35), A('about-saa', 'alumni-saa-qualify.jpg'))
    for board, name, page, f in [('Benefits', '20260325_Cap & Gown Photos for Graduates_EM_00289', 'alumni-benefits', 'alumni-benefits-becomeamember.jpg'),
                                 ('Benefits', '20251112_Employee Lifestyle_Pt 2_1012', 'alumni-benefits', 'alumni-benefits-resources.jpg'),
                                 ('Graduates', '20240503_ED_Grad Bash_JED_0480', 'graduating-students', 'alumni-grads-celebrate.jpg'),
                                 ('Graduates', '20240203_MBB vs Grand Canyon_KE_2056', 'graduating-students', 'alumni-grads-events.jpg'),
                                 ('Graduates', '20251021_APFY Joe_KE_0602', 'graduating-students', 'alumni-grads-connect.jpg'),
                                 ('Alumni Awards', '20260204_2026 Alumni Awards_EM_00134', 'alumni-awards', 'alumni-awards-honoring.jpg')]:
        save_jpg(xd_crop(board, name, LW, LH), A(page, f))
    save_jpg(L(load(N + 'n19.jpg'), .47, .55), A('alumni-benefits', 'alumni-benefits-opportunities.jpg'))
    save_jpg(P(load(N + 'n13.jpg'), .52, .62), A('uvu-license-plate', 'alumni-licenseplate-support.jpg'))
    save_jpg(L(load(N + 'n12.jpg'), .60, .62, 1.15), A('uvu-license-plate', 'alumni-licenseplate-look.jpg'))
    save_jpg(P(load(r.img_path('d226c29cab7b8617b73209ebe4698ebe')), .50, .36), A('alumni-awards', 'alumni-awards-tradition.jpg'))
    save_jpg(L(load(r.img_path('c2d2739fa7a62b7e6a57bf65d9646bde')), .48, .53, 1.2), A('alumni-diplomas', 'alumni-relations-team.jpg'))
    print('done')
