#!/usr/bin/env python3
"""UVU Giving v1.3 round 2: colleges, programs and centers, student support, athletics, securities.
Imports round 1 (build_give) so every page shares the footer, nav, and helpers, then writes all pages."""
import os, sys, re, json, html as H
sys.path.insert(0, '/tmp/gv/tools'); sys.path.insert(0, '/tmp/xr')
import build_give as G
from build_give import (P, OUT, LIVE, GENSCH, flag, todo, icon, btn, actions, frame, one, split, head, text, hero, xlink, is_ext,
                        link_to, footer, card, contact_card, grid, with_id, page)
from bs4 import BeautifulSoup

FUNDS = json.load(open('/tmp/gv/funds.json'))
OLD = '/tmp/gv/old/'
FORM_NOTE = None  # v1.6: removed per Zoe
TYPO = {'Global Enagement Endowment': ('Global Engagement Endowment', 'Live: “Enagement.”'),
        'Domincan Republic Global Fieldwork': ('Dominican Republic Global Fieldwork', 'Live: “Domincan.”'),
        'Exercise Science & Outdoor Reaction': ('Exercise Science and Outdoor Recreation', 'Live: “Outdoor Reaction.”'),
        'Gary R. Herbert Public Policy': ('Gary R. Herbert Public Policy', None)}
GROUP = {'Program List': 'Programs', 'Scholarship List': 'Scholarships', 'Other': 'Other Funds'}


def hero_x(n, slug, cms, title, eyebrow=None, lead=None, button=None, note=None):
    """Hero with the eyebrow as a tagline ABOVE the H1 (not inside it): the H1 stays the unit's name for search."""
    h = hero(n, f'assets/{slug}-header.jpg', cms, title, lead=lead, button=button, eyebrow=eyebrow, note=note)
    if eyebrow:
        h = h.replace(f'<h1><span class="al-eyebrow">{eyebrow}</span> ', f'<p class="al-eyebrow">{eyebrow}</p>\n            <h1>')
    return h


def amp(name):
    if name in TYPO and TYPO[name][1]:
        return flag(TYPO[name][0], TYPO[name][1])
    return name.replace(' & ', ' and ')


def fund_units(key, pg, skip=()):
    out = []
    for u in FUNDS[key]:
        if not u['groups'] or u['name'] in skip:
            continue
        groups = []
        for label, links in u['groups']:
            cur = [GROUP.get(label, label), []]; groups.append(cur)
            for t, href in links:
                if t in GROUP:  # live bug: a heading entered as a link
                    cur = [GROUP[t], []]; groups.append(cur); continue
                cur[1].append((t, href))
        groups = [g for g in groups if g[1]]
        np = sum(len(g[1]) for g in groups if g[0] == 'Programs'); ns = sum(len(g[1]) for g in groups if g[0] == 'Scholarships')
        no = sum(len(g[1]) for g in groups if g[0] not in ('Programs', 'Scholarships'))
        cnt = ' · '.join(x for x in [f'{np} program{"s" * (np != 1)}' if np else '', f'{ns} scholarship{"s" * (ns != 1)}' if ns else '',
                                       f'{no} other fund{"s" * (no != 1)}' if no else ''] if x)
        body = ''.join(f'''
                        <div><h4>{g}</h4><ul class="al-fund-links">{"".join(f"<li>{xlink(TYPO[t][0] if t in TYPO else t, h)}</li>" for t, h in links)}</ul></div>''' for g, links in groups)
        img = 'fund-' + (u['img'] or '').replace('_', '-')
        out.append(f'''                  <details class="al-fund accordion-unstyled">
                     <summary><img class="al-fund-thumb" src="assets/{img}" data-cms-src="/give/images/funds/{img}" alt="" width="600" height="400" loading="lazy"><span><span class="al-fund-name">{amp(u["name"])}</span><span class="al-fund-count">{cnt}</span></span></summary>
                     <div class="al-fund-body">{body}
                     </div>
                  </details>''')
    return '<div class="al-funds">\n' + '\n'.join(out) + '\n               </div>'


def tile_link(key, starts):
    for u in FUNDS[key]:
        if not u['groups'] and u['name'].startswith(starts):
            return u['sumlink']


def directory_todo(emp):
    return f"""                  <li class="al-contact-card"><span class="al-contact-badge" aria-hidden="true">?</span><div>
                     <p class="al-contact-name">{todo('CONTACT')}</p>
                     <p class="al-contact-role">{todo(f'DIRECTORY: the live page loads this contact from the directory widget (employee {emp}). Keep the widget or add the name here.')}</p>
                  </div></li>"""


# ======================================================================
# COLLEGE AND SCHOOL PAGES (one template, six pages)
# ======================================================================
COLLEGES = [
    ('Support CHPS Students', 'college-health-public-service', 'College of Health and Public Service', 'Support Future Heroes', 'health and public service', 'CHPS',
     [contact_card('Matt Bloxham', 'Development Director, Development, CHPS', 'cThsQXZPQllrcXdHaDdCcHVybUtUZz09', '801-863-8568', 0)]),
    ('Support CET Students', 'smith-college-engineering-technology', 'Smith College of Engineering and Technology', 'Support Future Innovators', 'engineering and technology', 'SCET',
     [contact_card('Stefan Harlan', 'Assistant Dean, Advancement, SCET', 'dCtYV1NZQVlIVFZWZUlodUhUaWZYQT09', '801-863-8568', 249)]),
    ('Support COS Students', 'college-of-science', 'College of Science', 'Support Future Scientists', 'science', 'COS', [directory_todo('10192452')]),
    ('Support Future Educators', 'school-of-education', 'School of Education', 'Support Future Educators', 'education', 'SOE', [directory_todo('11030256')]),
    ('Support Future Entrepreneurs', 'woodbury-school-business', 'Woodbury School of Business', 'Support Future Entrepreneurs', 'business', 'WSB', [directory_todo('10806932')]),
    ("Support UVU's College of Humanities & Social Sciences", 'college-humanities-social-sciences', 'College of Humanities and Social Sciences', 'Support Future Leaders', 'humanities and social sciences', 'CHSS',
     [contact_card('Jeremy Redd', 'Director, Development, COS and CHSS', 'SmhTSFEveFlsTndwTy9GZXFsU0FMdz09', '801-863-8568', 111)]),
    ('UVU School of the Arts', 'school-of-arts', 'School of the Arts', 'Support Future Artists', 'art', 'SOA',
     [contact_card('Varden Hadfield', 'Director of Development, School of the Arts', 'T0hOSGNQZHB1TkdXVm1Wak8xdkxkUT09', '801-863-8568', 285)]),
]
for key, slug, name, tag, subj, short, contacts in COLLEGES:
    sch = tile_link(key, short + ' Scholar') or tile_link(key, short)
    srch = tile_link(key, 'Search for')
    c = hero_x(1, slug, f'/give/colleges-schools/{slug}/images/{slug}-header.jpg', name, eyebrow=tag,
               lead=f'Your gift impacts UVU {subj} students for a lifetime.',
               button=(f'Give to {short} Scholarships', sch), note=FORM_NOTE)
    c += one(2, head(flag('Choose a Program or Scholarship', 'Placeholder heading. Live: a grid of photo tiles with no heading.'),
                     todo(f'COPY: 3 to 5 short sentences on why to give to the {name}: who it serves, what a gift does, one proof point. Pages with a real reason to give convert far better than lists alone.')) +
             f'\n               {actions(btn(f"Search for a {short} Fund", srch, "secondary")).replace("al-actions", "al-actions al-actions--center", 1)}\n               ' +
             fund_units(key, slug), cls='al-section--warm',
             note='Fund directory: one accordion per department with counts, so the page scans before anything opens. Live: photo tiles that open a gray box below the row. '
                  '“Program List” and “Scholarship List” become Programs and Scholarships. Department names spell out “and” (UVU style); fund names stay as given.')
    c += one(3, head(flag('Questions? Contact Us', 'Live: “For More Information.”'), lead=False) + '\n               ' + grid(contacts, 3, 'al-grid--center'), note='Contact.')
    c += footer(4)
    P[slug] = (f'Support {name}' if not name.startswith('School') else f'Support the {name}',
               f'Give to the UVU {name}: scholarships and programs that support {subj} students.', f'https://www.uvu.edu/give/colleges-schools/{slug}/index.html', c)

# ======================================================================
# COLLEGES AND SCHOOLS (index)
# ======================================================================
S = 'colleges-schools'
cols = [('chps-landing', 'College of Health and Public Service', LIVE + 'colleges-schools/college-health-public-service/index.php', 'Health and public service students in uniforms in front of an ambulance and fire truck'),
        ('chss-landing', 'College of Humanities and Social Sciences', 'college-humanities-social-sciences', 'A student reading between library shelves'),
        ('cos-main-landing', 'College of Science', 'college-of-science', 'A science student pipetting in a lab'),
        ('soa-thumbnail', 'School of the Arts', 'school-of-arts', 'School of the Arts'),
        ('soe-thumbnail', 'School of Education', 'school-of-education', 'School of Education'),
        ('scet-thumbnail', 'Smith College of Engineering and Technology', 'smith-college-engineering-technology', 'Smith College of Engineering and Technology'),
        ('wsb-thumbnail', 'Woodbury School of Business', 'woodbury-school-business', 'Woodbury School of Business')]


def photo_card(src, title, target, alt, tagtext=None, cms_dir='/give/images/'):
    href = f'../{target}/index.html' if target in G.PROD else target
    cms = f' data-cms-href="{G.PROD[target]}"' if target in G.PROD else ''
    ext = is_ext(href)
    tg = ' target="_blank" rel="noopener"' if ext else ''
    sr = '<span class="sr-only-al"> (opens in a new tab)</span>' if ext else ''
    tt = f'<p class="al-card-tag-text">{tagtext}</p>' if tagtext else ''
    return f'''                  <li><a class="al-news-card" href="{href}"{cms}{tg}>
                     <img src="assets/{src}" data-cms-src="{cms_dir}{src}" alt="{alt}" width="1200" height="750" loading="lazy">
                     <div class="al-card-body">{tt}<h3>{title}{sr}</h3></div>
                  </a></li>'''


cs = hero_x(1, S, '/give/images/headers/colleges-schools-header.jpg', 'Colleges and Schools', eyebrow='Give to UVU')
cs += one(2, head(flag('Choose a College or School', 'Placeholder heading. Live: tiles only.'), lead=False) + '\n               ' +
          grid([photo_card(f'college-{f}.jpg', t, u, a) for f, t, u, a in cols], 3),
          note='Seven photo cards; the whole card is the link. Names spell out “and.” Health and Public Service links to its live page (not saved for this round).')
cs += footer(3)
P[S] = ('Giving Opportunities in Colleges and Schools', 'Give to a UVU college or school: scholarships and programs for students in every field.', 'https://www.uvu.edu/give/colleges-schools/index.html', cs)

# ======================================================================
# PROGRAMS AND CENTERS
# ======================================================================
S = 'programs-centers'
pc = hero_x(1, S, '/give/programs-centers/images/programs-centers-header.jpg', 'Programs and Centers', eyebrow='Give to UVU',
            lead='Your gift impacts UVU students for a lifetime.')
pc += one(2, head(flag('Choose a Program or Center', 'Placeholder heading.'), lead=False) + '\n               ' + fund_units('Programs & Centers', S, skip=('Baugh Entrepreneurship Institute', 'UVU Museum of Art at Lakemount')), cls='al-section--warm',
          note='Fund directory, same component as the college pages. Baugh Entrepreneurship Institute and the Museum of Art at Lakemount are dropped here: every one of their funds already lives on the Woodbury and School of the Arts pages (Find a Fund still lists them). Culinary Arts and the Center for Autism stay; only some of their funds overlap. The Gary R. Herbert Institute’s live list has a stray “Scholarship List” link (to the First Generation Center form) where a heading belongs; it is a heading here. Confirm the FirstGen link wasn’t meant to be there.')
pc += one(3, head(flag('Questions? Contact Us', 'Live: “For More Information.”'), lead=False) + '\n               ' +
          grid([contact_card('Dan Dimond', flag('Senior Director of Development', 'Live: “Sr Director.”'), 'd2ZyMVZjUkFhbnRrbUt0YnRHSHZ6UT09', '801-863-8568', 111)], 3, 'al-grid--center'), note='Contact.')
pc += footer(4)
P[S] = ('Programs and Centers', 'Give to UVU programs and centers, from the Baugh Entrepreneurship Institute to the Fulton Library.', 'https://www.uvu.edu/give/programs-centers/index.html', pc)

# ======================================================================
# STUDENT SUPPORT (Student Affairs)
# ======================================================================
S = 'student-affairs'
SAF = 'https://host.nxt.blackbaud.com/donor-form?svcid=renxt&formId=cf92e542-a77d-4ce2-bef9-11aba2cbb36a&envid=p-15SOd3UsHUO8MRNYFSnBvg&zone=usa'
areas = [('area-student-success-thumbnail.jpg', 'Student Support Top Initiatives', LIVE + 'student-affairs/student-success.html', 'A student studying with a laptop by a window'),
         ('area-access-card2.jpg', 'Access and Outreach', LIVE + 'student-affairs/access-outreach.html', 'A large group of students posed on the steps of a campus building'),
         ('area-enrollment-card1.jpg', 'Enrollment Management', LIVE + 'student-affairs/enrollment-management.html', 'A crowd of students walking through a campus hallway'),
         ('area-student-development-well-being.jpg', 'Student Development and Wellbeing', LIVE + 'student-affairs/student-development.html', 'Students sitting together in a bright lounge')]
sa = hero_x(1, S, '/give/images/student-support-header.jpg', 'Student Support', eyebrow='Support UVU Students',
            lead='Your gift impacts UVU students for a lifetime.', button=(flag('Give to Student Affairs Scholarships', 'Live tile: “SA Scholarships.”'), SAF), note=FORM_NOTE)
sa += one(2, head(flag('Choose an Area to Support', 'Placeholder heading.'), lead=False) + '\n               ' +
          grid([photo_card(*a, cms_dir='/give/student-affairs/images/') for a in areas], 2) +
          f'\n               {actions(btn("Search for a Student Affairs Fund", LIVE + "student-affairs/sa-give-search.html", "secondary")).replace("al-actions", "al-actions al-actions--center", 1)}',
          cls='al-section--warm', note='Four areas as photo cards; scholarships move to the hero button and fund search to a secondary button (live: six equal tiles, one a clip-art grad cap).')
sa += one(3, head(flag('Questions? Contact Us', 'Live: “For More Information.”'), lead=False) + '\n               ' +
          grid([contact_card('Kari Dennis', 'Director of Development, Student Affairs', 'c1BHa3JVakowS0ZsNlVtdmtlOHJ2QT09', '801-863-8568', 312)], 3, 'al-grid--center'), note='Contact.')
sa += footer(4)
P[S] = ('Support UVU Student Affairs', 'Give to UVU Student Affairs: access and outreach, enrollment, student development and wellbeing, and scholarships.', 'https://www.uvu.edu/give/student-affairs/index.html', sa)

# ======================================================================
# ATHLETICS (Wolverine Club)
# ======================================================================
S = 'athletics'
soup = BeautifulSoup(open(OLD + 'Support UVU Student Athletes _ Utah Valley University.html', encoding='utf-8', errors='ignore').read(), 'html.parser')
sports = []
for a in soup.select('#list a'):
    hh = a.find(['h2', 'h3', 'h4'])
    if not hh: continue
    sport, _, who = [x.strip() for x in hh.get_text(' ', strip=True).partition('|')]
    img = a.find_previous('img')
    sports.append((sport, who, a['href'], os.path.splitext(os.path.basename(img['src']))[0] if img else ''))
WC = [s for s in sports if s[0] == 'Wolverine Club'][0]
WHO = {"Men's": "Men's", "Women's": "Women's", 'Both': "Men's and Women's"}
cards = [photo_card(f'sport-{im}.jpg', amp(sp), href, f'UVU {WHO.get(who, "")} {sp.lower()}'.replace('  ', ' '), WHO.get(who, who), '/give/athletics/wolverine-club/images/')
         for sp, who, href, im in sports if sp != 'Wolverine Club']
cards.insert(0, photo_card('sport-wolverin-club.jpg', 'Wolverine Club', WC[2], 'Cheering UVU fans in green', 'All Teams', '/give/athletics/wolverine-club/images/'))
at = hero_x(1, S, '/give/athletics/wolverine-club/images/wolverine-club-header.jpg', 'UVU Athletics', eyebrow='Wolverine Club',
            lead='Your gift impacts UVU student athletes for a lifetime.', button=('Give to the Wolverine Club', WC[2]), note=FORM_NOTE)
at += one(2, head('Choose Your Impact Zone', lead=False) + '\n               ' + grid(cards, 3), cls='al-section--warm',
          note='Thirteen teams as photo cards with a Men’s / Women’s tag. Live repeats the list three times behind All / Men / Women tabs; one list with tags does the same job. Wolverine Club general moves to the hero button.')
at += one(3, head(flag('Questions? Contact Us', 'Live: “For More Information.”'), lead=False) + '\n               ' + grid([
    contact_card('Matt Potts', 'Deputy Athletic Director, Revenue Generation', 'ejI2QXhraDhmUXlkSVUvczhjcmYwdz09', '801-863-8888', 104),
    contact_card('Julie Shepherd', flag('Assistant Athletic Director, Wolverine Club and Signature Events', 'Live: “Wolverine Club - Sig. Events.”'), 'NUU1UUIrejZJQjRHMm5Ob3NFa2hxQT09', '801-863-8888', 104)], 2), note='Contacts.')
at += footer(4)
P[S] = ('Support UVU Student Athletes', 'Give to UVU Athletics and the Wolverine Club: support student athletes on every team.', 'https://www.uvu.edu/give/athletics/wolverine-club/index.html', at)

# ======================================================================
# GIFTS OF SECURITIES
# ======================================================================
S = 'gifts-of-securities'
ex_short = 'For example, John bought 100 shares of XYZ Corporation in March for $1,000.00 ($10 per share). Three months later, John donated the shares to the UVU Foundation. At the time of the donation, the shares were worth $9 per share. The UVU Foundation receives a benefit of $900, but John can only claim a charitable donation of $900. If the shares increased in price to $11 per share, the UVU Foundation would receive a benefit of $1,100, but John can only claim a charitable donation of $1,000. If John had sold the stock and donated the cash, he would need to recognize the $100 loss or gain and report it on his tax return.'
ex_long = 'For example, John bought 100 shares of XYZ Corporation in March for $1,000.00 ($10 per share). Three years later, John donated the shares to the UVU Foundation. At the time of the donation, the shares were worth $9 per share. UVU Foundation receives a benefit of $900, but John only can claim a charitable donation of $900. If the shares increased in price to $11 per share, UVU Foundation would receive a benefit of $1,100, and John can claim a charitable donation of $1,100. If John had sold the stock and donated the cash, he would need to recognize the $100 loss or gain and report it on his tax return.'


def ex(t):
    return f'<details class="al-accordion accordion-unstyled"><summary>See an Example</summary><div class="al-accordion-body"><p>{t}</p></div></details>'


gs = hero_x(1, S, '/advancement/images/ways-to-give/gifts-of-securities-header.jpg', 'Gifts of Securities',
            button=(flag('Talk to a Gift Officer', 'New: the live page ends without a next step. Points to giving@uvu.edu; confirm the right contact (the Employee Giving FAQ sends stock questions to Vicky Hopper).'), 'mailto:giving@uvu.edu?subject=Gift%20of%20Securities'))
gs += one(2, f'''               <div class="al-notice">{icon('info-1')}<p><strong>Disclaimer:</strong> This information is not to be used as official tax advice. Please contact your personal tax professional before making decisions.</p></div>
''' + head('Donating Securities', f'Securities or stocks can be separated into three categories: {flag("closely held stock", "Live: “closely held Stock.”")}, S corporation stock, and qualified appreciated stock.') + '\n               ' + grid([
    card('business', 'Closely Held Stock', f'<p>The fair market value (FMV) of closely held stock can be difficult to determine. Therefore, if the deduction exceeds $10,000, the donor must obtain a qualified appraisal. Even if the donation is less than $10,000, an independent appraisal may be useful to help support the claimed value. If the recipient cannot sell the stock, the gift may have limited value. Also, the donor may not be able to give much stock without giving the recipient control or influence over voting matters.</p>'),
    card('structure', 'S Corporation Stock', '<p>S corporation stock is not publicly traded, so a qualified appraisal is required for donations more than $10,000. Like closely held stock, it may have limited value because of the inability to sell the shares and the recipient may have control or influence over voting matters. In addition, the pass-through income from ownership in S corporation stock is treated as unrelated business income tax (UBIT) to the Foundation. The donation may be unattractive to the Foundation because the income can trigger income tax.</p>'),
    card('financial-growth', 'Qualified Appreciated Stock', '<p>Normally, the charitable deduction for appreciated stock donations is the full fair market value (FMV) of the stock. Qualified appreciated stock is stock for which market quotations are readily available on an established securities market and which would generate long-term capital gain if sold. Mutual fund shares that are not subject to any resale restrictions are considered qualified appreciated stock.</p>')], 3),
    note='Disclaimer as a notice up top (live: plain italic line). Three stock types as cards.')
gs += one(3, head('Benefits', 'Donations of stock can offer tax benefits to donors, depending on the time frame in which the stocks were held and their individual tax situation.') + '\n               ' + grid([
    card('time', 'Short-Term Capital Assets', f'<p>Donations of short-term capital assets (assets held less than 12 months) do not offer tax benefits to the donor but are still a valuable and appreciated donation. If the stock has appreciated, meaning the purchase price (basis) is less than the current fair market value (FMV), the donor deducts the basis as a charitable contribution. If the stock has depreciated, meaning the basis is greater than the current FMV, the donor deducts the FMV as a charitable contribution. In essence, the donor deducts the {flag("lesser", "Live: “lessor.” Typo.")} of basis or FMV. In addition to the charitable deduction, the donor does not have to recognize any gains (triggering a taxable event) on the transfer of the stock.</p>{ex(ex_short)}'),
    card('calendar', 'Long-Term Capital Assets', f'<p>Only donations of long-term appreciated stock offer donors a significant tax benefit. In addition to the charitable deduction, donors avoid the potential of a taxable event if the sale of the stock is followed by the donation of cash.</p><p>If the stock has appreciated, meaning the basis is less than the current FMV, the donor deducts the FMV as a charitable contribution. If the stock has depreciated, meaning the {flag("basis", "Live: “Basis.”")} is greater than the current FMV, the donor deducts the FMV as a charitable contribution. Basically, with long-term capital assets, the donor gets to deduct the FMV of the stock. In addition to the charitable deduction, the donor does not have to recognize any gains (triggering a taxable event) on the transfer of the stock.</p>{ex(ex_long)}')], 2),
    cls='al-section--warm', note='Short- vs. long-term side by side; the worked examples fold into “See an Example.”')
gs += footer(4)
P[S] = ('Gifts of Securities', 'Give stock to Utah Valley University: closely held, S corporation, and qualified appreciated stock, and their tax benefits.', 'https://www.uvu.edu/give/ways-to-give/gifts-of-securities.html', gs)

if __name__ == '__main__':
    for slug, (title, desc, url, main) in P.items():
        os.makedirs(f'{OUT}/{slug}/assets', exist_ok=True)
        open(f'{OUT}/{slug}/index.html', 'w').write(page(slug, title, desc, url, main))
        print('wrote', slug)
