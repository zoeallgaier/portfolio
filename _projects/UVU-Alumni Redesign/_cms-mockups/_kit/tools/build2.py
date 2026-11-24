#!/usr/bin/env python3
"""Alumni Web System v1 page builder: shared shell + section vocabulary."""
import html as H
import re

OUT = '/mnt/user-data/outputs/cms-mockups'
HDR = open(f'{OUT}/_kit/partials/global-header.html').read()
FTR = open(f'{OUT}/_kit/partials/global-footer.html').read()
CSS = ['01-bootstrap.min.css', '02-global.css', '03-component.css', '04-helpers-legacy.css', '05-elements.css', '06-helpers.css',
       '07-wrapper.css', '08-fonts.css', '09-homepage-wrapper.css', '10-homepage-dept.css', '11-fontawesome-pro.css']
I = '../_kit/icons'


def page(slug, title, desc, url, main):
    links = '\n'.join(f'<link rel="stylesheet" href="../_kit/css/{c}">' for c in CSS)
    import re as _re
    main = _re.sub(r'<!--ALSITENAV (\d+)-->', lambda m: sitenav(m.group(1), slug), main)
    ftr = FTR.replace('<ul><li>Utah Valley University</li></ul>', '<ul><li>Office of Alumni Relations</li><li>Utah Valley University</li></ul>')
    return f'''<!DOCTYPE html>
<!-- =====================================================================
     UVU ALUMNI WEB SYSTEM v1 · CMS MOCKUP · {title}
     Live URL: {url}
     Styles: UVU production CSS snapshot + ../_kit/css/12-alumni-system.css
     See ../README.md and ../_kit/styleguide.html
     ===================================================================== -->
<html lang="en" dir="ltr" style="--headroom-height: 123px;">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, user-scalable=yes">
<meta name="color-scheme" content="only light">
<meta name="description" content="{H.escape(desc)}">
<title>{title} | Utah Valley University</title>

<!-- ===== UVU production CSS (snapshot) ===== -->
{links}

<!-- ===== Alumni Web System (the only alumni stylesheet a page needs) ===== -->
<link rel="stylesheet" href="../_kit/css/12-alumni-system.css">
<!-- ===== Mockup-only tools. Not for production. ===== -->
<link rel="stylesheet" href="../_kit/css/99-mockup-tools.css">
<script src="../_kit/js/mockup-tools.js"></script>
</head>
<body id="{slug}" class="UVU_Public_Site utah-valley-university {slug} marketing homepage audience DeptNav DeptFooter">

<!-- ===== GLOBAL HEADER (CMS template; context only) ===== -->
{HDR}
<main id="content-wrap" class="content-wrap">
<!-- ===== CMS CONTENT START · each <section> = one OU section ===== -->
{main}
<!-- ===== CMS CONTENT END ===== -->
</main>
<!-- ===== GLOBAL FOOTER (CMS template; context only) ===== -->
{ftr}
</body>
</html>
'''


# ---------- inline helpers ----------
def flag(text, note, tag='span'):
    return f'<{tag} class="mock-copy-flag" title="{H.escape(note)}">{text}</{tag}>'


def todo(text):
    return f'<span class="mock-todo">{text}</span>'


def icon(name, color='green', cls='', alt=''):
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{I}/{color}/{name}.svg" data-cms-src="/alumni/lib/icons/{color}/{name}.svg" alt="{alt}" width="48" height="48">'


def is_ext(href):
    return href.startswith('http') and not href.startswith('https://www.uvu.edu') and not href.startswith('https://uvu.edu')


def btn(label, href, kind='', ext=None, note=None):
    """ext=None: decide from the URL (anything off uvu.edu opens in a new tab and says so)."""
    if ext is None:
        ext = is_ext(href)
    k = (f' al-btn--{kind}' if kind else '') + (' al-btn--ext' if ext else '')
    t = ' target="_blank" rel="noopener"' if ext else ''
    sr = '<span class="sr-only-al"> (opens in a new tab)</span>' if ext else ''
    nt = f'<p class="al-btn-note">{note}</p>' if note else ''
    return f'<a class="al-btn{k}" href="{href}"{t}>{label}{sr}</a>{nt}'


def xlink(label, href, cls='', ic=None):
    """Inline/list link that follows the same new-tab rule as buttons."""
    ext = is_ext(href)
    t = ' target="_blank" rel="noopener"' if ext else ''
    sr = '<span class="sr-only-al"> (opens in a new tab)</span>' if ext else ''
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{href}"{t}>{ic or ""}{label}{sr}</a>'


def actions(*btns):
    return '<div class="al-actions">' + ''.join(btns) + '</div>'


VARIANTS = ['hatch', 'stairs', 'dot', 'half']
_V = [0]


def frame(src, cms, alt, variant=None, portrait=False):
    """Photo in the uvu.edu image style: plain photo + APFY shapes (CSS). Variants rotate per page."""
    if variant is None:
        variant = VARIANTS[_V[0] % len(VARIANTS)]; _V[0] += 1
    src = src.replace('.png', '.jpg'); cms = cms.replace('.png', '.jpg')
    w, h = (960, 1200) if portrait else (1200, 900)
    pc = ' al-media--portrait' if portrait else ''
    return f'<figure class="al-media al-media--{variant}{pc}"><img src="{src}" data-cms-src="{cms}" alt="{H.escape(alt)}" width="{w}" height="{h}" loading="lazy"></figure>'


def ps(*paras, lead_first=False):
    out = ''
    for i, p in enumerate(paras):
        cls = ' class="al-lead"' if lead_first and i == 0 else ''
        out += f'\n               <p{cls}>{p}</p>'
    return out


# ---------- sections ----------
def _sec(n, tpl, cls, inner, note='', style=''):
    nt = f'\n     {note}' if note else ''
    st = f' style="{style}"' if style else ''
    return f'''
<!-- SECTION {n} · template: {tpl}{nt} -->
<section data-uvu-template="{tpl}" data-uvu-section="{n}" class="al-section{(" " + cls) if cls else ""}"{st}>
   <div class="container-fluid">{inner}
   </div>
</section>'''


def hero(n, img, cms, title, lead=None, button=None, eyebrow=None, note=None):
    """eyebrow: shown small above the title and kept INSIDE the H1, so the H1 still reads
    'UVU Alumni Benefits' for search while the visual title is just 'Benefits'."""
    _V[0] = 0
    mimg = re.sub(r'\.\w+$', '-mobile.jpg', img); mcms = re.sub(r'\.\w+$', '-mobile.jpg', cms)
    if eyebrow:
        title = f'<span class="al-eyebrow">{eyebrow}</span> {title}'
    lp = f'\n            <p class="al-hero-lead">{lead}</p>' if lead else ''
    bt = f'\n            {actions(btn(button[0], button[1], "light", note=note))}' if button else ''
    return f'''
<!-- SECTION {n} · template: header-fullbleed
     ASSET: {img} (1920x700 raw photo; the green fade is CSS). CMS: {cms}
     PHONES: {mimg} (1080x1350 vertical, people centered). CMS: {mcms} -->
<section class="page-header jumbo fullbleed container-narrow al-hero" style="background-image: url({img});" data-cms-bg="{cms}" data-uvu-template="header-fullbleed" data-uvu-section="{n}">
   <div class="al-hero-m" style="background-image: url({mimg});" data-cms-bg="{mcms}" aria-hidden="true"></div>
   <div class="container-fluid">
      <header class="fullbleed-overlay contain text-invert">
            <h1>{title}</h1>{lp}{bt}
      </header>
   </div>
</section>'''


def split(n, text_html, media_html, reverse=False, cls='', note=''):
    rv = ' al-split--reverse' if reverse else ''
    inner = f'''
      <div class="row equal-height flex-row al-split{rv}">
         <div class="col-xs-12 col-sm-6 col-target region" data-uvu-region="1">
{text_html}
         </div>
         <div class="col-xs-12 col-sm-6 col-target region al-split-media" data-uvu-region="2">
               {media_html}
         </div>
      </div>'''
    return _sec(n, 'two-col', cls, inner, note)


def one(n, inner_html, cls='', note='', style=''):
    inner = f'''
      <div class="row">
         <div class="col-xs-12 col-target region" data-uvu-region="1">
{inner_html}
         </div>
      </div>'''
    return _sec(n, 'one-col', cls, inner, note, style)


def head(h2, *paras, lead=True, extra=''):
    p = ''
    for i, x in enumerate(paras):
        p += f'\n                  <p{" class=\"al-lead\"" if lead and i == 0 else ""}>{x}</p>'
    return f'''               <div class="al-section-head">
                  <h2>{h2}</h2>{p}{extra}
               </div>'''


def text(h2, *paras, after=''):
    p = ''
    for i, x in enumerate(paras):
        p += f'\n               <p{" class=\"al-lead\"" if i == 0 else ""}>{x}</p>'
    return f'               <h2>{h2}</h2>{p}{after}'


def contact(n):
    """Alumni footer (section nav + contact). Filled in by page() so it can mark the current page."""
    return f'\n<!--ALSITENAV {n}-->'


PROFILE_URL = 'https://alumni.uvu.edu/profile/me'
PROD = {'alumni-home': '/alumni/index.html', 'alumni-benefits': '/alumni/resources/benefits/alumni-benefits.html',
        'graduating-students': '/alumni/students/graduating-students.html', 'alumni-scholarships': '/alumni/make-an-impact/alumni-scholarships.html',
        'about-saa': '/alumni/students/about-saa.html', 'uvu-license-plate': '/alumni/make-an-impact/uvu-license-plate.html',
        'alumni-awards': '/alumni/about/alumni-awards.html', 'alumni-board': '/alumni/about/alumni-association-advisory-board.html',
        'alumni-diplomas': '/alumni/resources/diplomas.html', 'career-networking-resources': '/alumni/connect/career-networking-resources.html',
        'aviation-alumni-chapter': '/alumni/connect/aviation-alumni-chapter.html', 'alumni-job-shadow': '/alumni/volunteer/job-shadow.html',
        'forever-wolverines-podcast': '/alumni/connect/forever-wolverines-podcast.html'}
NAV = [('Connect', [('Events', 'https://www.uvu.edu/events/index.html'), ('Alumni Stories', 'https://www.uvu.edu/news/features/index.html#alumni'),
                    ('Forever Wolverines Podcast', 'forever-wolverines-podcast'), ('Aviation Alumni Chapter', 'aviation-alumni-chapter'),
                    ('Career and Networking Resources', 'career-networking-resources')]),
       ('Benefits', [('Alumni Benefits', 'alumni-benefits'), ('Diplomas', 'alumni-diplomas'), ('Update Your Alumni Profile', PROFILE_URL)]),
       ('Make an Impact', [('Alumni Scholarships', 'alumni-scholarships'), ('UVU License Plate', 'uvu-license-plate'),
                           ('Job Shadow Program', 'alumni-job-shadow'), ('Give to UVU', 'https://www.uvu.edu/give/')]),
       ('Students and About', [('Graduating Students', 'graduating-students'), ('Student Alumni Ambassadors', 'about-saa'),
                               ('Alumni Awards', 'alumni-awards'), ('Board of Directors', 'alumni-board')])]

SOCIAL = [('social-instagram', 'UVU Alumni on Instagram', 'https://www.instagram.com/uvualumni/'),
          ('social-facebook-f', 'UVU Alumni on Facebook', 'https://www.facebook.com/uvualumni'),
          ('social-linkedin-in', 'UVU Alumni on LinkedIn', 'https://www.linkedin.com/showcase/uvualumni'),
          ('social-youtube', 'UVU Alumni on YouTube', 'https://www.youtube.com/@uvualumni')]


def sitenav(n, current):
    groups = ''
    for g, items in NAV:
        lis = ''
        for label, t in items:
            if t in PROD:
                cur = ' aria-current="page"' if t == current else ''
                lis += f'<li><a href="../{t}/index.html" data-cms-href="{PROD[t]}"{cur}>{label}</a></li>'
            else:
                lis += f'<li>{xlink(label, t)}</li>'
        groups += f'\n                  <div class="al-sitenav-group"><h2>{g}</h2><ul>{lis}</ul></div>'
    soc = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{icon(i, "green", alt=a + " (opens in a new tab)")}</a></li>' for i, a, u in SOCIAL)
    return f"""
<!-- SECTION {n} · template: one-col · ALUMNI FOOTER: section nav + contact. Identical on every alumni page
     (the current page gets aria-current). Replaces the old full-height contact band.
     The office name also goes in the CMS dept footer (#globalFooter .footerDept). -->
<section data-uvu-template="one-col" data-uvu-section="{n}" class="al-section al-sitenav">
   <div class="container-fluid">
      <div class="row">
         <div class="col-xs-12 col-target region" data-uvu-region="1">
            <nav class="al-sitenav-nav" aria-label="UVU Alumni">
               <div class="al-sitenav-brand">
                  <p class="al-sitenav-title"><a href="../alumni-home/index.html" data-cms-href="/alumni/index.html"{' aria-current="page"' if current == 'alumni-home' else ''}>UVU Alumni Relations</a></p>
                  <ul class="al-sitenav-contact">
                     <li>{icon("envelope-1", "white")}<a href="mailto:alumni@uvu.edu">alumni@uvu.edu</a></li>
                     <li>{icon("cell", "white")}<a href="tel:+18018638179">801.863.8179</a></li>
                  </ul>
                  <ul class="al-social">{soc}</ul>
               </div>
               <div class="al-sitenav-groups">{groups}
               </div>
               <p class="al-sitenav-fine">A UVU alum is anyone who graduated with a certificate, diploma, or degree from UVU or any of its past eras (CUVS, UTTI, UTC, UVCC, UVSC, or UVU).</p>
            </nav>
         </div>
      </div>
   </div>
</section>"""
