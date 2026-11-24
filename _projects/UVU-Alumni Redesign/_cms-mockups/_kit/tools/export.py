import sys, json, os, re
sys.path.insert(0, '/tmp/xr')
from xd2svg import *
r = XD('/mnt/user-data/uploads/Web Page Redesigns/_cms-mockups/_xd-source')
OUT = '/mnt/user-data/outputs/cms-mockups'
jobs = []; post = []
PH = {r'rgb\(255,0,\d+\)': 'rgb(226,230,227)'}

def F(board, name):
    it = r.find(r.board(board)[1], name); assert it, (board, name); return it

def job(board, names, out, box=None, skip_text=False, transparent=True, fmt='png', recolor=None, label=None, scale=1):
    nodes = [F(board, n) if isinstance(n, str) else n for n in names]
    h, b = render_nodes(r, board, nodes, box, skip_text, 'transparent' if transparent else '#ffffff', recolor, label)
    hp = '/tmp/xr/exp/' + os.path.basename(out) + '.html'
    os.makedirs('/tmp/xr/exp', exist_ok=True); os.makedirs(os.path.dirname(out), exist_ok=True)
    open(hp, 'w').write(h)
    png = out if fmt == 'png' else out + '.tmp.png'
    jobs.append(dict(html=hp, png=png, w=b[2], h=b[3], transparent=transparent, scale=scale))
    if fmt == 'jpg':
        post.append((png, out))

def hero(board, names, out):
    job(board, names, out, box=(0, 136, 1920, 700), skip_text=True, transparent=False, fmt='jpg')

S = OUT + '/_shared-assets/'
# shared contact band
job('Benefits', ['Group 67'], S + 'alumni-contact-circle.png')
job('Benefits', ['Group 14'], S + 'alumni-contact-texture.jpg', skip_text=True, transparent=False, fmt='jpg')

hero('Alumni Schlarships', ['20240503_CHSS Convocation_EM_0387', 'Path 35'], OUT + '/alumni-scholarships/assets/alumni-scholarships-header.jpg')
A = OUT + '/alumni-home/assets/'
hero('Alumni Home', ['20240502_Comencement 2024_KE_0552', 'Path 35'], A + 'alumni-home-header.jpg')
job('Alumni Home', ['Group 18'], A + 'alumni-home-stayconnected.png')
job('Alumni Home', ['FloatingCreditCardMockup'], A + 'alumni-wolverinecard.png')

A = OUT + '/uvu-license-plate/assets/'
hero('License Plate', ['Alumni-LicensePlate2026_v2', 'Path 35'], A + 'alumni-licenseplate-header.jpg')
job('License Plate', ['Group 18'], A + 'alumni-licenseplate-support.png')
job('License Plate', ['Group 17'], A + 'placeholder-angled-left.png', recolor=PH, label='PHOTO TBD')
job('License Plate', ['Group 16'], A + 'placeholder-angled-right.png', recolor=PH, label='PHOTO TBD')

A = OUT + '/about-saa/assets/'
hero('Student Alumni Ambassadors', ['20220622_UVU Campus Photos_EM_0098', 'Path 35'], A + 'alumni-saa-header.jpg')
job('Student Alumni Ambassadors', ['Group 18'], A + 'placeholder-angled-right.png', recolor=PH, label='PHOTO TBD')
job('Student Alumni Ambassadors', ['Group 17'], A + 'placeholder-angled-left.png', recolor=PH, label='PHOTO TBD')
for g, nm in [('Group 56', 'savannah-evans'), ('Group 57', 'callie-ross'), ('Group 58', 'makenna-koopmans'), ('Group 59', 'max-taylor')]:
    grp = F('Student Alumni Ambassadors', g)
    img = [c for c in grp['group']['children'] if c.get('style', {}).get('fill', {}).get('type') == 'pattern'][0]
    job('Student Alumni Ambassadors', [img], A + f'saa-{nm}.jpg', transparent=False, fmt='jpg')

A = OUT + '/alumni-awards/assets/'
hero('Alumni Awards', ['Group 66'], A + 'alumni-awards-header.jpg')
job('Alumni Awards', ['Group 68'], A + 'alumni-awards-honoring.png')
job('Alumni Awards', ['Group 69'], A + 'alumni-awards-tradition.png')
for n, nm in [('Jane F. Rhodes Headshot', 'jane-rhodes'), ('20251004_Rich & Marla Linder_AM_0115', 'linder'), ('Heather Headshot 1', 'heather-kahlert'),
              ('20260115_Robbie Bastain Portrait_AM_0095', 'robert-bastian'), ('20251219_Sheldon Smith_NG_0055', 'sheldon-smith')]:
    job('Alumni Awards', [n], A + f'awards-{nm}.jpg', transparent=False, fmt='jpg')

A = OUT + '/alumni-benefits/assets/'
hero('Benefits', ['Group 66'], A + 'alumni-benefits-header.jpg')
job('Benefits', ['Group 18'], A + 'alumni-benefits-becomeamember.png')
job('Benefits', ['Group 17'], A + 'alumni-benefits-opportunities.png')
job('Benefits', ['Group 16'], A + 'alumni-benefits-resources.png')
job('Benefits', ['Group 12'], A + 'alumni-benefits-logos.png', scale=1.5)

A = OUT + '/graduating-students/assets/'
hero('Graduates', ['20240502_WSB_Woodbury School of Business Convocation_IH_2442', 'Path 35'], A + 'alumni-grads-header.jpg')
job('Graduates', ['Group 18'], A + 'alumni-grads-celebrate.png')
job('Graduates', ['Group 16'], A + 'alumni-grads-events.png')
job('Graduates', ['Group 60'], A + 'alumni-grads-connect.png')
job('Graduates', ['AlumniSpotlight-thumbnail_v3-02'], A + 'alumni-grads-spotlight-thumb.jpg', transparent=False, fmt='jpg')
job('Graduates', ['20240607_UMC_APFY_JED_2144', 'Path 76'], A + 'alumni-grads-community-bg.jpg', box=(0, 2560, 1920, 700), skip_text=True, transparent=False, fmt='jpg')
job('Graduates', ['FloatingCreditCardMockup'], A + 'alumni-wolverinecard.png')

# home icons as standalone SVG
icons = {}
info, kids = r.board('Alumni Home')
for i, slug in enumerate(['events', 'businesses', 'license-plate', 'scholarships', 'ambassadors', 'graduates', 'benefits'], 1):
    comp = r.find(kids, f'Component {i} – 1')
    m = tmat(comp)
    icon = None
    for ch in comp['group']['children']:
        src = r.idx.get(ch.get('syncSourceGuid')) if ch.get('type') == 'syncRef' else ch
        if src and src.get('type') != 'text':
            icon = ch; break
    h, b = render_nodes(r, 'Alumni Home', [icon], skip_text=True)
    svg = re.search(r'<svg.*</svg>', h, re.S).group(0)
    p = OUT + f'/alumni-home/assets/icon-{slug}.svg'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(svg)
    icons[slug] = b
json.dump(jobs, open('/tmp/xr/expjobs.json', 'w'))
json.dump(post, open('/tmp/xr/post.json', 'w'))
print(len(jobs), 'jobs', icons)
