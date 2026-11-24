#!/usr/bin/env python3
"""UVU Giving v1.4: condensed structure. Give becomes the hub; Find a Fund lists every fund;
Annual Giving and Gifts of Securities merge into Ways to Give; the Colleges and Schools index merges into Give."""
import os, sys, re, json, shutil, html as H
sys.path.insert(0, '/tmp/gv/tools'); sys.path.insert(0, '/tmp/xr')
import build_give as G
import build_give2 as G2
from build_give import (P, OUT, LIVE, GENSCH, PAYROLL, flag, todo, icon, btn, actions, frame, one, split, head, text, hero, xlink, is_ext,
                        link_to, footer, card, contact_card, grid, with_id, page, stats)
from build_give2 import FUNDS, amp, TYPO, GROUP, COLLEGES, tile_link, ex, ex_short, ex_long, photo_card, SAF, sports, WC, WHO

# ---------- structure: drop merged pages, add Find a Fund ----------
for gone in ('annual-giving', 'gifts-of-securities', 'colleges-schools'):
    P.pop(gone, None); G.PROD.pop(gone, None)
    shutil.rmtree(f'{OUT}/{gone}', ignore_errors=True)
G.PROD['find-a-fund'] = '/give/find-a-fund.html'
G.PROD['college-health-public-service'] = '/give/colleges-schools/college-health-public-service/index.php'
WAYS = 'ways-to-give'
PLATE = 'https://www.uvu.edu/alumni/make-an-impact/uvu-license-plate.html'
G.NAV[:] = [
    ('Where to Give', [('Find a Fund', 'find-a-fund'), ('Colleges and Schools', '../give-home/index.html#give-by-area'), ('Programs and Centers', 'programs-centers'),
                       ('Student Support', 'student-affairs'), ('Athletics', 'athletics'), ('General Scholarships', GENSCH)]),
    ('Ways to Give', [('All Ways to Give', 'ways-to-give'), ('Employee Giving', 'employee-giving'), ('Memorial Gifts', 'memorial-gifts'),
                      ('Gifts of Stock', '../ways-to-give/index.html#give-stock'), ('Gift Planning', 'https://uvgift.org/'), ('Matching Gifts', LIVE + 'ways-to-give/matching-gifts.html')]),
    ('More', [('Planning a Larger Gift', '../give-home/index.html#larger-gift'), ('UVU License Plate', PLATE), ('Event Sponsorship', 'https://www.uvu.edu/advancement/events/archive/scholarship-ball.html'),
              ('In-Kind Donation', LIVE + 'ways-to-give/in-kind-donation.html'), ('Service', LIVE + 'ways-to-give/service.html')])]

_old_gsitenav = G.gsitenav


def gsitenav2(n, current):
    h = _old_gsitenav(n, current)
    h = h.replace('organization.</p>', f'organization. {todo("TAX ID: add the UVU Foundation EIN here; major donors and advisors look for it.")} <a href="#">{flag("Annual Impact Report", "New link: report URL needed.")}</a> · <a href="#">{flag("IRS Form 990", "New link: 990 URL needed.")}</a></p>')
    return h


G.gsitenav = gsitenav2
G.build2.sitenav = gsitenav2


def a_link(label, target):
    """link_to that also accepts ../page/index.html#anchor targets."""
    if target.startswith('../'):
        return f'<a href="{target}">{label}</a>'
    return link_to(label, target)


# ======================================================================
# FIND A FUND (new): every fund on the Give site in one searchable list
# ======================================================================
rows = []
def add(name, href, kind, area, unit=''):
    if not href or href.endswith('#'): return
    rows.append((name, href, kind, area, unit))

AREA = {key: name for key, slug, name, *_ in COLLEGES}
for key, units in FUNDS.items():
    area = AREA.get(key, 'Programs and Centers')
    for u in units:
        for label, links in u['groups']:
            kind = {'Program List': 'Program', 'Scholarship List': 'Scholarship'}.get(label, 'Fund')
            for t, h in links:
                if t in GROUP: continue
                add(TYPO[t][0] if t in TYPO else t, h, kind, area, u['name'].replace(' & ', ' and ').replace('Outdoor Reaction', 'Outdoor Recreation'))
for key, slug, name, tag, subj, short, contacts in COLLEGES:
    add(f'{name} Scholarships', tile_link(key, short + ' Scholar') or tile_link(key, short), 'Scholarship', name, 'General')
add('General Scholarships', GENSCH, 'Scholarship', 'University-wide', 'Where most needed')
add('Student Affairs Scholarships', SAF, 'Scholarship', 'Student Support')
add('UVU Memorial Scholarship', '../memorial-gifts/index.html#give-now', 'Scholarship', 'University-wide', 'Memorial and tribute gifts')
for sp, who, href, im in sports:
    add('Wolverine Club' if sp == 'Wolverine Club' else f'{sp.replace(" & ", " and ")} ({WHO.get(who, who)})', href, 'Team' if sp != 'Wolverine Club' else 'Fund', 'Athletics', '')
seen = set(); uniq = []
for r in rows:
    k = (r[0].lower(), r[1])
    if k in seen: continue
    seen.add(k); uniq.append(r)
uniq.sort(key=lambda r: r[0].lower())
areas = sorted(set(r[3] for r in uniq))


def fundrow(name, href, kind, area, unit):
    ext = is_ext(href)
    tg = ' target="_blank" rel="noopener"' if ext else ''
    sr = '<span class="sr-only-al"> (opens the giving form in a new tab)</span>' if ext else ''
    meta = ' · '.join(x for x in [kind, area, unit] if x)
    txt = H.escape(' '.join([name, kind, area, unit]).lower(), quote=True)
    return f'<li data-area="{H.escape(area, quote=True)}" data-text="{txt}"><a href="{href}"{tg}><span class="al-fundrow-name">{name}</span><span class="al-fundrow-meta">{meta}</span><span class="al-fundrow-go" aria-hidden="true">Give</span>{sr}</a></li>'


opts = ''.join(f'<option value="{H.escape(a, quote=True)}">{a}</option>' for a in areas)
ff = G.hero_plain(1, 'Find a Fund', lead=f'{len(uniq)} funds across UVU. Search by name, program, college, or team.', comment='Compact hero: a utility page.')
ff = ff.replace(f'{len(uniq)} funds across UVU. Search by name, program, college, or team.', flag(f'{len(uniq)} funds across UVU. Search by name, program, college, or team.', 'New microcopy. The count is generated from the fund list.'))
ff += one(2, f'''               <h2 class="sr-only-al">Search Funds</h2>
               <div class="al-finder-tools" role="search">
                  <label class="sr-only-al" for="fund-q">Search funds</label>
                  <input id="fund-q" type="search" placeholder="Try “first generation,” “nursing,” or “wrestling”" autocomplete="off">
                  <label class="sr-only-al" for="fund-area">Filter by area</label>
                  <select id="fund-area"><option value="">All areas</option>{opts}</select>
               </div>
               <p class="al-meta al-finder-count" id="fund-count" aria-live="polite"></p>
               <ul class="al-fundrows">
{chr(10).join("                  " + fundrow(*r) for r in uniq)}
               </ul>
               <div class="al-finder-more" id="fund-more" hidden><button type="button" class="al-btn al-btn--secondary">Show All Funds</button></div>
               <p class="al-finder-empty" id="fund-empty" hidden>No funds match. Try one word, like “nursing,” or <a href="{GENSCH}" target="_blank" rel="noopener">give to General Scholarships<span class="sr-only-al"> (opens in a new tab)</span></a>.</p>
               <p class="al-meta al-center">{todo("PRODUCTION: this list is the CMS dataview component (the same one behind the live per-college “Search for a Fund” pages), fed one spreadsheet of every fund with its Blackbaud form URL. The mockup filters with ../_kit/js/fund-finder.js.")}</p>
               <script src="../_kit/js/fund-finder.js" defer></script>''', cls='al-section--warm',
          note=f'One list of every fund ({len(uniq)}): name, type, area, department, and a direct link to its Blackbaud form (designation pre-filled). Replaces the seven per-college “Search for a Fund” pages. Reads ?q= so the Give page search box lands here filtered.')
ff += footer(3)
P['find-a-fund'] = ('Find a Fund', 'Search every fund at Utah Valley University and give directly: scholarships, programs, colleges, and teams.', 'https://www.uvu.edu/give/find-a-fund.html', ff)

# ======================================================================
# GIVE (hub)
# ======================================================================
S = 'give-home'
FG = [r for r in uniq if r[0] == 'First Generation Center'][0][1]
feat = [('feat-scholarships.jpg', 'General Scholarships', 'University-wide', GENSCH, 'Smiling graduates in green caps and gowns'),
        ('feat-first-gen.jpg', 'First Generation Center', 'Programs and Centers', FG, 'First-generation UVU students'),
        ('feat-wolverine-club.jpg', 'Wolverine Club', 'Athletics', WC[2], 'Cheering UVU fans in green'),
        ('feat-library.jpg', 'Fulton Library', 'Programs and Centers', [r for r in uniq if r[0] == 'Library'][0][1], 'A student reading between library shelves'),
        ('feat-social-impact.jpg', 'Center for Social Impact', 'Programs and Centers', [r for r in uniq if r[0] == 'Center for Social Impact'][0][1], 'Center for Social Impact'),
        ('feat-culinary.jpg', 'Culinary Arts', 'Smith College of Engineering and Technology', [r for r in uniq if r[0] == 'Culinary Arts'][0][1], 'A culinary student plating food')]


def featcard(img, name, area, href, alt):
    return f'''                  <li><a class="al-news-card" href="{href}" target="_blank" rel="noopener">
                     <img src="assets/{img}" data-cms-src="/give/images/featured/{img}" alt="{alt}" width="800" height="500" loading="lazy">
                     <div class="al-card-body"><p class="al-card-tag-text">{area}</p><h3>{name}</h3><span class="al-card-give">Give Now<span class="sr-only-al"> (opens the giving form in a new tab)</span></span></div>
                  </a></li>'''


hints = [('first generation', 'First generation'), ('nursing', 'Nursing'), ('aviation', 'Aviation'), ('basketball', 'Basketball'), ('library', 'Library')]
COLL_IC = {'college-health-public-service': 'community-health', 'smith-college-engineering-technology': 'engineering', 'college-of-science': 'science', 'school-of-education': 'education',
           'woodbury-school-business': 'business', 'college-humanities-social-sciences': 'humanities', 'school-of-arts': 'fine-arts'}
coll_links = [f'<li>{link_to(icon(COLL_IC[slug]) + name, slug)}</li>' for key, slug, name, *_ in COLLEGES]
coll_links = sorted(coll_links, key=lambda s: re.sub('<[^>]+>', '', s))
camp_links = [f'<li>{link_to(icon(i) + l, t)}</li>' for i, l, t in [('student-life', 'Student Support', 'student-affairs'), ('athletics', 'Athletics', 'athletics'),
                                                                    ('program', 'Programs and Centers', 'programs-centers'), ('team', 'Employee Giving', 'employee-giving')]] + \
             [f'<li>{xlink(icon("diploma-3") + "General Scholarships", GENSCH)}</li>', f'<li>{link_to(icon("question-1") + "Search All Funds", "find-a-fund")}</li>']
ways_links = [(icon('credit-cards') + 'Give Online', '../find-a-fund/index.html'), (icon('calendar') + flag('Give Monthly', 'New: monthly giving gets its own entry point (NextAfter: a short monthly-giving note lifted new recurring donors 48%).'), '../ways-to-give/index.html#give-today'),
              (icon('cash-2') + 'Payroll Deduction', 'employee-giving'), (icon('award') + 'Memorial and Tribute Gifts', 'memorial-gifts'),
              (icon('financial-growth') + 'Gifts of Stock', '../ways-to-give/index.html#give-stock'), (icon('paper') + 'Gift Planning', 'https://uvgift.org/'),
              (icon('donation') + 'Matching Gifts', LIVE + 'ways-to-give/matching-gifts.html'), (icon('envelope-1') + 'Mail a Check', '../ways-to-give/index.html#give-today'),
              (icon('automotive') + 'UVU License Plate', PLATE)]

g = hero(1, f'assets/{S}-header.jpg', f'/give/images/headers/{S}-header.jpg', 'Giving to Utah Valley University',
         lead='Transforming classrooms, communities, and futures.',
         button=(flag('Give Now', 'Goes to the General Scholarships form. Confirm the default fund, or point it at a form with a fund picker.'), GENSCH))
g += with_id(one(2, head(flag('Your Gift Opens Doors', 'Placeholder heading, from the live Ways to Give intro (“Your financial donations open doors”).'),
                         'Gifts directly support scholarships, academic programs, and campus resources, empowering UVU students to achieve their dreams and build brighter futures. Eighty-seven percent of UVU graduates remain in the state, so an investment in UVU is an investment in Utah’s future.') + f'''
               <form class="al-search" action="../find-a-fund/index.html" method="get" role="search">
                  <label for="give-q">Search all funds</label>
                  <input id="give-q" name="q" type="search" placeholder="Search {len(uniq)} funds: a program, college, team, or name">
                  {btn('Find a Fund', '../find-a-fund/index.html').replace('<a ', '<button type="submit" ').replace('</a>', '</button>').replace(' href="../find-a-fund/index.html"', '')}
               </form>
               <ul class="al-search-hints"><li class="al-meta">Popular:</li>{"".join(f'<li><a href="../find-a-fund/index.html?q={q.replace(" ", "+")}">{l}</a></li>' for q, l in hints)}</ul>''',
                 note='Why give (two sentences built from live Annual Giving and Ways to Give copy, merged and flagged as one edit) + fund search. The search box submits to Find a Fund (production: CMS dataview search URL).'), 2, 'find')
g += one(3, head('Featured Funds', lead=False) + '\n               ' + grid([featcard(*f) for f in feat], 3, 'al-grid--swipe') +
         f'\n               {actions(btn(flag("See All " + str(len(uniq)) + " Funds", "New button label."), "../find-a-fund/index.html", "secondary")).replace("al-actions", "al-actions al-actions--center", 1)}',
         cls='al-section--warm', note='Six funds, one click each to a form with the designation pre-filled (University of Utah / ASU pattern). IA picks and rotates these; the six here are placeholders chosen to show range (scholarships, first-gen, athletics, library, a center, a program).')
g += with_id(one(4, head('Give by Area', lead=False) + f'''
               <div class="al-grid al-grid--2">
                  <div><h3>Colleges and Schools</h3><ul class="al-linklist">{"".join(coll_links)}</ul></div>
                  <div><h3>{flag('Across Campus', 'Placeholder subhead.')}</h3><ul class="al-linklist">{"".join(camp_links)}</ul></div>
               </div>''', note='Every area one click from Give. Replaces the Colleges and Schools page (a page that only listed other pages) and the six icon tiles.'), 4, 'give-by-area')
g += split(5, f'''               <h2>{flag('Be Part of That Village', 'Placeholder heading from the quote.')}</h2>
               <blockquote class="al-pullquote"><p>“Remember, it takes a village to help a student graduate. Be part of that village.”</p><cite>Kyrsi Zamora, Coordinator, UVU Latino Initiative, first-generation graduate and monthly donor</cite></blockquote>
               <p>As a first-generation student, I endured many financial challenges, but I got the support from UVU to get through college. I am grateful that I am able to donate to do the same for our students now.</p>
               {actions(btn(flag('Join Kyrsi: Give to the First Generation Center', 'Michigan pattern: “Join [name] and make a gift.” Confirm with Kyrsi before launch; her live quote is in the Employee Giving section.'), FG))}
               <ul class="al-linklist"><li>{xlink(icon('report') + 'Read Student Stories', 'https://www.uvu.edu/advancement/make-an-impact/365-stories.html')}</li></ul>''',
           frame('assets/story-kyrsi-zamora.jpg', '/give/images/story-kyrsi-zamora.jpg', 'Kyrsi Zamora', portrait=True),
           cls='al-section--warm', note='One real story instead of the $25/$50/$250/$500 cards. Quote is Kyrsi Zamora’s, verbatim from the I AM UVU graphic. “Monthly donor” in the caption is inferred from Employee Giving; confirm or cut. Rotate this slot with student and donor stories.')
g += one(6, head('Ways to Give', lead=False) + '\n               <ul class="al-linklist al-linklist--3">' + ''.join(f'<li>{a_link(l, t)}</li>' for l, t in ways_links) + '</ul>',
         note='Nine ways, one line each. Replaces the Ways to Give photo cards as the first stop.')
g += with_id(one(7, f'''               <div class="al-grid al-grid--2 al-grid--middle">
                  <div>
                     <h2>{flag('Planning a Larger Gift?', 'New section for major and planned gifts.')}</h2>
                     <p>{flag('Talk with our development team about endowments, naming opportunities, and gifts of stock, property, or retirement assets. We’ll help you find the right fit for your goals and your family.', 'New copy. Rewrite in IA’s voice.')}</p>
                     <ul class="al-linklist">
                        <li>{xlink(icon('paper') + 'Explore Gift Planning', 'https://uvgift.org/')}</li>
                        <li>{a_link(icon('financial-growth') + 'Give Stock or Securities', '../ways-to-give/index.html#give-stock')}</li>
                        <li><a href="#">{icon('report')}{flag('Read the Annual Impact Report', 'Report URL needed.')}</a></li>
                     </ul>
                  </div>
                  <ul class="al-contact-strip al-contact-strip--card">
{G2.directory_todo('a named leadership contact (AVP of Development or a major gifts officer) with direct phone and email').replace('employee a named', 'a named')}
                  </ul>
               </div>''', cls='al-section--warm', note='For the $10M donor: a person, planned giving, stock, and the impact report on the hub, not three pages deep.'), 7, 'larger-gift')
g += footer(8)
P[S] = ('Give', 'Give to Utah Valley University: search every fund, give in one click, or plan a larger gift.', 'https://www.uvu.edu/give/index.html', g)

# ======================================================================
# WAYS TO GIVE (absorbs Annual Giving + Gifts of Securities)
# ======================================================================
S = WAYS
w = hero(1, f'assets/{S}-header.jpg', '/give/ways-to-give/images/ways-to-give-header.jpg', 'Ways to Give')
w += with_id(one(2, head('Give Today',
                         f'There are many ways you can support UVU. Your financial donations open doors by supporting scholarships, the faculty, academic programs, and athletics. Sponsorship of the {flag("President’s Scholarship Ball", "Stale event name? Now the Presidential Scholarship Banquet (PSB). Confirm the name and the 115-student figure.")} helps provide 115 students annually with merit scholarships.') + '\n               ' + grid([
    card('credit-cards', 'Give Online', '<p>You may direct your gift to many areas in need throughout UVU. Search every fund and give in one step.</p>', ('Find a Fund', '../find-a-fund/index.html')),
    card('calendar', flag('Give Monthly', 'New card.'), f'<p>{flag("A monthly gift, even a small one, gives students support they can count on all year.", "New copy. Confirm the Blackbaud forms offer a recurring monthly option.")}</p>', ('Find a Fund', '../find-a-fund/index.html')),
    card('cash-2', 'Payroll Deduction', '<p>For UVU employees. Donations can be as little as $1 per paycheck.</p>', ('Employee Giving', '../employee-giving/index.html')),
    card('award', 'Memorial and Tribute Gifts', '<p>In lieu of flowers, many people choose to donate in their loved one’s name.</p>', ('Give a Memorial Gift', '../memorial-gifts/index.html')),
    card('donation', 'Matching Gifts', '<p>Many employers will match a charitable contribution and/or volunteer hours.</p>', ('See If Your Employer Matches', LIVE + 'ways-to-give/matching-gifts.html')),
    card('envelope-1', 'Mail a Check', '<p>Make your check payable to UVU Foundation and send it to 800 W. University Parkway, MS 111, Orem, UT 84058.</p>')], 3),
    note='Ways to give now, as icon cards. Live copy where it exists; Give Monthly is new.'), 2, 'give-today')
w += one(3, head(flag('Give Over Time', 'Michigan groups pledges, planned gifts, and monthly giving as “Give Over Time.”'), lead=False) + '\n               ' + grid([
    card('paper', 'Gift Planning', '<p>Many people choose a long-term approach to giving using a bequest, will, annuity, or trust.</p>', ('Explore Gift Planning', 'https://uvgift.org/')),
    card('financial-growth', 'Gifts of Stock', '<p>Donations of stock can offer tax benefits to donors, depending on the time frame in which the stocks were held and their individual tax situation.</p>', ('How to Give Stock', '#give-stock')),
    card('automotive', 'UVU License Plate', f'<p>{flag("A $35 scholarship donation each year, with your registration.", "From the Alumni License Plate page.")}</p>', ('Get a UVU Plate', PLATE)),
    card('presentation', 'Event Sponsorship', '<p>Sponsor a scholarship event and help students earn merit scholarships.</p>', ('Learn About Sponsorship', 'https://www.uvu.edu/advancement/events/archive/scholarship-ball.html')),
], 2) + f'''
               <ul class="al-linklist al-linklist--2 al-narrow">
                  <li>{xlink(icon('chair') + 'In-Kind Donation', LIVE + 'ways-to-give/in-kind-donation.html')}</li>
                  <li>{xlink(icon('community-health') + 'Service', LIVE + 'ways-to-give/service.html')}</li>
               </ul>''',
    cls='al-section--warm', note='Longer-term and non-cash gifts. Sponsorship line condensed from the intro (flag on the intro covers the event name).')
w += with_id(one(4, f'''               <div class="al-notice">{icon('info-1')}<p><strong>Disclaimer:</strong> This information is not to be used as official tax advice. Please contact your personal tax professional before making decisions.</p></div>
''' + head('Give Stock', 'Donations of stock can offer tax benefits to donors, depending on the time frame in which the stocks were held and their individual tax situation.') + f'''
               <div class="al-narrow">
               <p class="al-meta">{todo("TRANSFER INSTRUCTIONS: add the UVU Foundation brokerage, DTC number, account number, and who to notify. Advisors need this first; the live page never says how to transfer.")}</p>
               <details class="al-accordion accordion-unstyled"><summary>Closely Held Stock</summary><div class="al-accordion-body"><p>The fair market value (FMV) of closely held stock can be difficult to determine. Therefore, if the deduction exceeds $10,000, the donor must obtain a qualified appraisal. Even if the donation is less than $10,000, an independent appraisal may be useful to help support the claimed value. If the recipient cannot sell the stock, the gift may have limited value. Also, the donor may not be able to give much stock without giving the recipient control or influence over voting matters.</p></div></details>
               <details class="al-accordion accordion-unstyled"><summary>S Corporation Stock</summary><div class="al-accordion-body"><p>S corporation stock is not publicly traded, so a qualified appraisal is required for donations more than $10,000. Like closely held stock, it may have limited value because of the inability to sell the shares and the recipient may have control or influence over voting matters. In addition, the pass-through income from ownership in S corporation stock is treated as unrelated business income tax (UBIT) to the Foundation. The donation may be unattractive to the Foundation because the income can trigger income tax.</p></div></details>
               <details class="al-accordion accordion-unstyled"><summary>Qualified Appreciated Stock</summary><div class="al-accordion-body"><p>Normally, the charitable deduction for appreciated stock donations is the full fair market value (FMV) of the stock. Qualified appreciated stock is stock for which market quotations are readily available on an established securities market and which would generate long-term capital gain if sold. Mutual fund shares that are not subject to any resale restrictions are considered qualified appreciated stock.</p></div></details>
               <details class="al-accordion accordion-unstyled"><summary>Short-Term Capital Assets</summary><div class="al-accordion-body"><p>Donations of short-term capital assets (assets held less than 12 months) do not offer tax benefits to the donor but are still a valuable and appreciated donation. If the stock has appreciated, meaning the purchase price (basis) is less than the current fair market value (FMV), the donor deducts the basis as a charitable contribution. If the stock has depreciated, meaning the basis is greater than the current FMV, the donor deducts the FMV as a charitable contribution. In essence, the donor deducts the {flag("lesser", "Live: “lessor.”")} of basis or FMV. In addition to the charitable deduction, the donor does not have to recognize any gains (triggering a taxable event) on the transfer of the stock.</p><p>{ex_short}</p></div></details>
               <details class="al-accordion accordion-unstyled"><summary>Long-Term Capital Assets</summary><div class="al-accordion-body"><p>Only donations of long-term appreciated stock offer donors a significant tax benefit. In addition to the charitable deduction, donors avoid the potential of a taxable event if the sale of the stock is followed by the donation of cash.</p><p>If the stock has appreciated, meaning the basis is less than the current FMV, the donor deducts the FMV as a charitable contribution. If the stock has depreciated, meaning the {flag("basis", "Live: “Basis.”")} is greater than the current FMV, the donor deducts the FMV as a charitable contribution. Basically, with long-term capital assets, the donor gets to deduct the FMV of the stock. In addition to the charitable deduction, the donor does not have to recognize any gains (triggering a taxable event) on the transfer of the stock.</p><p>{ex_long}</p></div></details>
               </div>''', note='The Gifts of Securities page, condensed: transfer instructions first (placeholder), tax detail in accordions. Live URL /give/ways-to-give/gifts-of-securities.html should redirect here (#give-stock).'), 4, 'give-stock')
w += one(5, head(flag('Questions? Contact Annual Giving', 'From the Annual Giving page, which merges here. Live /give/ways-to-give/annual-giving.html should redirect here.'), lead=False) + '\n               ' + grid([
    contact_card('Tess Fontanetti-Rice', 'Director of Annual Giving', 'K0NqdWZaMXlvSER0SzJWMmt6NjU1QT09', '801-863-8568', 111),
    contact_card('Zachary Browning', 'Assistant Director, Annual Giving', 'clo4ejdVYjFLaitUTWZQbTRmWWRzUT09', '801-863-8888', 111),
    contact_card('Erin McCarthy', 'Assistant Development Director, Development', 'cjloRjB6a0ZjVkNMUnpoQklvNmN0Zz09', '801-863-8568', 111)], 3), note='Contacts.')
w += footer(6)
P[S] = ('Ways to Give', 'Ways to give to Utah Valley University: online, monthly, payroll, memorial gifts, stock, gift planning, and more.', 'https://www.uvu.edu/give/ways-to-give/index.html', w)

# ---------- write ----------
if __name__ == '__main__':
    for slug, (title, desc, url, main) in P.items():
        os.makedirs(f'{OUT}/{slug}/assets', exist_ok=True)
        html = page(slug, title, desc, url, main)
        html = html.replace('href="../annual-giving/index.html"', 'href="../ways-to-give/index.html"')
        for key, cslug, cname, tag, subj, short, contacts in COLLEGES:
            if slug == cslug:
                srch = tile_link(key, 'Search for')
                html = re.sub(r'<a class="al-btn al-btn--secondary[^"]*" href="' + re.escape(srch) + r'"[^>]*>.*?</a>',
                              f'<a class="al-btn al-btn--secondary" href="../find-a-fund/index.html?area={cname.replace(" ", "+")}">Search All {short} Funds</a>', html, flags=re.S)
        if slug == 'student-affairs':
            html = re.sub(r'<a class="al-btn al-btn--secondary[^"]*" href="https://www.uvu.edu/give/student-affairs/sa-give-search.html"[^>]*>.*?</a>',
                          '<a class="al-btn al-btn--secondary" href="../find-a-fund/index.html?area=Student+Support">Search Student Support Funds</a>', html, flags=re.S)
        open(f'{OUT}/{slug}/index.html', 'w').write(html)
        print('wrote', slug)
    print(len(uniq), 'funds')
