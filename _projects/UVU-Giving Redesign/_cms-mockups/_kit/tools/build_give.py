#!/usr/bin/env python3
"""UVU Giving v1.3 page builder. Reuses the Alumni Web System builder (build2) with a giving footer."""
import os, sys, re
sys.path.insert(0, '/tmp/xr')
import build2
from build2 import H, flag, todo, icon, btn, actions, frame, one, split, head, text, hero, xlink, is_ext, _V

OUT = '/mnt/user-data/outputs/giving-mockups'
GENSCH = 'https://host.nxt.blackbaud.com/donor-form/?svcid=renxt&formId=3ebce5df-6a4a-4f44-89b7-ef3d89fcad79&envid=p-15SOd3UsHUO8MRNYFSnBvg&zone=usa'
PAYROLL = 'https://apps.uvu.edu/employee-form-hub/forms/foundation_deduction_form?bbeml=tp-15SOd3UsHUO8MRNYFSnBvg.jaaFzp9xt9kKWRKc0XU7OXw.rrijxJts6iEiqW-7jAopktA.l9L54vzla_U-Evl_tqKK1Ow'
LIVE = 'https://www.uvu.edu/give/'
PROD = {'give-home': '/give/index.html', 'ways-to-give': '/give/ways-to-give/index.html',
        'annual-giving': '/give/ways-to-give/annual-giving.html', 'employee-giving': '/give/ways-to-give/employeegiving.html',
        'memorial-gifts': '/give/ways-to-give/memorial-gifts.html',
        'gifts-of-securities': '/give/ways-to-give/gifts-of-securities.html', 'colleges-schools': '/give/colleges-schools/index.html',
        'programs-centers': '/give/programs-centers/index.html', 'student-affairs': '/give/student-affairs/index.html',
        'athletics': '/give/athletics/wolverine-club/index.html',
        'smith-college-engineering-technology': '/give/colleges-schools/smith-college-engineering-technology/index.html',
        'college-of-science': '/give/colleges-schools/college-of-science/index.html',
        'school-of-education': '/give/colleges-schools/school-of-education/index.html',
        'woodbury-school-business': '/give/colleges-schools/woodbury-school-business/index.html',
        'college-humanities-social-sciences': '/give/colleges-schools/college-humanities-social-sciences/index.html',
        'school-of-arts': '/give/colleges-schools/school-of-arts/index.html'}
NAV = [('Where to Give', [('Colleges and Schools', 'colleges-schools'), ('Programs and Centers', 'programs-centers'),
                          ('Student Support', 'student-affairs'), ('Athletics', 'athletics'),
                          ('General Scholarships', GENSCH)]),
       ('Ways to Give', [('All Ways to Give', 'ways-to-give'), ('Annual Giving', 'annual-giving'), ('Employee Giving', 'employee-giving'),
                         ('Memorial Gifts', 'memorial-gifts'), ('Gifts of Securities', 'gifts-of-securities')]),
       ('More Ways to Give', [('Gift Planning', 'https://uvgift.org/'), ('Matching Gifts', LIVE + 'ways-to-give/matching-gifts.html'),
                              ('In-Kind Donation', LIVE + 'ways-to-give/in-kind-donation.html'), ('Service', LIVE + 'ways-to-give/service.html'),
                              ('Event Sponsorship', 'https://www.uvu.edu/advancement/events/archive/scholarship-ball.html')])]


def link_to(label, t, current=None):
    if t in PROD:
        cur = ' aria-current="page"' if t == current else ''
        return f'<a href="../{t}/index.html" data-cms-href="{PROD[t]}"{cur}>{label}</a>'
    return xlink(label, t)


def gsitenav(n, current):
    groups = ''
    for g, items in NAV:
        lis = ''.join(f'<li>{link_to(l, t, current)}</li>' for l, t in items)
        groups += f'\n                  <div class="al-sitenav-group"><h2>{g}</h2><ul>{lis}</ul></div>'
    return f"""
<!-- SECTION {n} · template: one-col · GIVING FOOTER: section nav + contact + mail-a-check. Identical on every Give page
     (the current page gets aria-current). Replaces the "Ways to Give: Give Online / Mail a Check" block the live
     pages repeat at the bottom of Annual Giving, Gifts of Securities, Memorial Gifts, and Ways to Give. -->
<section data-uvu-template="one-col" data-uvu-section="{n}" class="al-section al-sitenav">
   <div class="container-fluid">
      <div class="row">
         <div class="col-xs-12 col-target region" data-uvu-region="1">
            <nav class="al-sitenav-nav" aria-label="Give to UVU">
               <div class="al-sitenav-brand">
                  <p class="al-sitenav-title"><a href="../give-home/index.html" data-cms-href="/give/index.html">Give to UVU</a></p>
                  <ul class="al-sitenav-contact">
                     <li>{icon("envelope-1", "white")}<a href="mailto:giving@uvu.edu">giving@uvu.edu</a></li>
                     <li>{icon("cell", "white")}<a href="tel:+18018638568">801.863.8568</a></li>
                  </ul>
               </div>
               <div class="al-sitenav-groups">{groups}
               </div>
               <p class="al-sitenav-fine"><strong>Mail a check</strong> payable to UVU Foundation, 800 W. University Parkway, MS 111, Orem, UT 84058. All donations are processed through the Utah Valley University Foundation, a 501(c)(3) {flag('nonprofit', 'Live: “non-profit.” AP: nonprofit.')} organization.</p>
            </nav>
         </div>
      </div>
   </div>
</section>"""


build2.sitenav = gsitenav


def page(slug, title, desc, url, main):
    h = build2.page(slug, title, desc, url, main)
    h = h.replace('UVU ALUMNI WEB SYSTEM v1 · CMS MOCKUP', 'UVU GIVING · IA WEB SYSTEM v1.3 · CMS MOCKUP')
    h = h.replace('<ul><li>Office of Alumni Relations</li><li>Utah Valley University</li></ul>', '<ul><li>Institutional Advancement</li><li>Utah Valley University</li></ul>')
    h = h.replace('<!-- ===== Alumni Web System (the only alumni stylesheet a page needs) ===== -->', '<!-- ===== IA Web System (shared with Alumni; the only system stylesheet a page needs) ===== -->')
    return h


def footer(n):
    return f'\n<!--ALSITENAV {n}-->'


def hero_plain(n, title, lead=None, button=None, note=None, eyebrow=None, comment=''):
    _V[0] = 0
    if eyebrow:
        title = f'<span class="al-eyebrow">{eyebrow}</span> {title}'
    lp = f'\n            <p class="al-hero-lead">{lead}</p>' if lead else ''
    bt = f'\n            {actions(btn(button[0], button[1], "light", note=note))}' if button else ''
    return f'''
<!-- SECTION {n} · template: header-fullbleed (compact: no hero photo){(" · " + comment) if comment else ""} -->
<section class="page-header jumbo fullbleed al-hero al-hero--plain" data-uvu-template="header-fullbleed" data-uvu-section="{n}">
   <div class="container-fluid">
      <header class="fullbleed-overlay contain text-invert">
            <h1>{title}</h1>{lp}{bt}
      </header>
   </div>
</section>'''


def with_id(html, n, id_):
    return html.replace(f'data-uvu-section="{n}" class="al-section', f'id="{id_}" data-uvu-section="{n}" class="al-section', 1)


def card(ic, h3, body, act=None):
    a = f'\n                     <div class="al-card-action">{xlink(*act)}</div>' if act else ''
    return f"""                  <li><article class="al-card">
                     <div class="al-card-body">{icon(ic, cls='al-card-icon')}
                        <h3>{h3}</h3>
                        {body}
                     </div>{a}
                  </article></li>"""


def contact_card(name, role, dir_id, phone, ms):
    """Compact contact: initials badge + name, title, phone, directory message link."""
    tel = re.sub(r'\D', '', phone)
    plain = re.sub(r'<[^>]+>', '', name)
    ini = ''.join(w[0] for w in plain.split()[:1] + plain.split()[-1:]).upper()
    return f"""                  <li class="al-contact-card"><span class="al-contact-badge" aria-hidden="true">{ini}</span><div>
                     <p class="al-contact-name">{name}</p>
                     <p class="al-contact-role">{role}</p>
                     <p class="al-contact-links"><a href="tel:+1{tel}">{phone}</a> · <a href="https://www.uvu.edu/directory/message/?id={dir_id}">Message {plain.split()[0]}</a></p>
                  </div></li>"""


def stats(items, cls=''):
    li = '\n'.join(f'                  <li class="al-stat"><span class="al-stat-num">{n}</span><span class="al-stat-label">{l}</span></li>' for n, l in items)
    return f'<ul class="al-stats{(" " + cls) if cls else ""}">\n{li}\n               </ul>'


def grid(items, n=3, cls=''):
    if items and all('al-contact-card' in i for i in items):
        return '<ul class="al-contact-strip">\n' + '\n'.join(items) + '\n               </ul>'
    return f'<ul class="al-grid al-grid--{n}{(" " + cls) if cls else ""}">\n' + '\n'.join(items) + '\n               </ul>'


P = {}

# ======================================================================
# GIVE (home)
# ======================================================================
S = 'give-home'
where = [('athletics', 'Athletics', 'athletics'), ('university', 'Colleges and Schools', 'colleges-schools'),
         ('team', 'Employee Giving', 'employee-giving'), ('diploma-3', 'General Scholarships', GENSCH),
         ('program', 'Programs and Centers', 'programs-centers'), ('student-life', 'Student Support', 'student-affairs')]
ql = '\n'.join(f'                  <li>{link_to(icon(i) + "<span>" + l + "</span>", u)}</li>' for i, l, u in where)
g = hero(1, f'assets/{S}-header.jpg', f'/give/images/headers/{S}-header.jpg', 'Giving to Utah Valley University',
         lead='Transforming classrooms, communities, and futures.',
         button=(flag('Give Now', 'New: the live Give page has no give button. This goes to the General Scholarships form, the only general form on the page. Confirm the default fund, or point it at a form with a fund picker.'), GENSCH))
g += one(2, f'''               <div class="al-section-head"><h2>{flag('Where to Give', 'Placeholder heading. Live tiles have none.')}</h2></div>
               <ul class="al-quicklinks al-quicklinks--6">
{ql}
               </ul>''', note='Six giving areas as icon quick links (UVU Icon Library). Live: six text tiles in caps, “COLLEGES &amp; SCHOOLS.”')
g += one(3, head('How You Can Make an Impact', lead=False) + '\n               ' + stats([
    ('$25', 'Provides access to food, housing, health, and safety through the UVU Care Hub'),
    ('$50', 'Offers support to a student to cover the needed technology for a course'),
    ('$250', 'Ensures a student athlete or artist can purchase a course textbook'),
    ('$500', 'Allows a student to attend a 1-credit course')]) + f'\n               {actions(btn("Give Now", GENSCH)).replace("al-actions", "al-actions al-actions--center", 1)}',
    cls='al-section--warm', note='Impact amounts as stat cards (al-stats). Labels: verb tense evened out (“Provides… Offers… Ensures… Allows”), serial comma added.')
g += split(4, text('Your Gift Can Change Lives', after=f'\n               {actions(btn("Read Student Stories", "https://www.uvu.edu/advancement/make-an-impact/365-stories.html"))}'),
           frame('assets/give-change-lives.jpg', '/give/images/give-change-lives.jpg', 'A smiling UVU graduate in a green lei at commencement'),
           note='Replaces the circle-cropped graduates graphic (ia-cta.png).')
g += one(5, head('Ways to Give', lead=False) + '''
               <ul class="al-linklist al-linklist--2">
''' + '\n'.join(f'                  <li>{link_to(icon(i) + l, t)}</li>' for i, l, t in [
    ('donation', 'All Ways to Give', 'ways-to-give'), ('calendar', 'Annual Giving', 'annual-giving'), ('team', 'Employee Giving', 'employee-giving'),
    ('award', 'Memorial Gifts', 'memorial-gifts'), ('financial-growth', 'Gifts of Securities', 'gifts-of-securities'),
    ('paper', 'Gift Planning', 'https://uvgift.org/')]) + '\n               </ul>',
    note='New: the live Give page never links to Ways to Give. Six routes, link list.')
g += footer(6)
P[S] = ('Give', 'Give to Utah Valley University: support scholarships, students, colleges, programs, and athletics.', 'https://www.uvu.edu/give/index.html', g)

# ======================================================================
# WAYS TO GIVE
# ======================================================================
S = 'ways-to-give'
fin = [('giving-priorities', 'University Giving Priorities', '../give-home/index.html', 'UVU students walking past the large green UVU letters on campus'),
       ('scholarships-1', 'Scholarships', GENSCH, 'Smiling graduates in green caps and gowns at commencement'),
       ('annual-giving', 'Annual Giving', '../annual-giving/index.html', 'The Utah Valley University seal beneath snowy mountains'),
       ('memorial-gifts', 'Memorial Gifts', '../memorial-gifts/index.html', 'A bouquet of white flowers wrapped in paper with a green ribbon'),
       ('gift-securities', 'Gifts of Securities', '../gifts-of-securities/index.html', 'A stock chart on a computer screen'),
       ('gift-planning', 'Gift Planning', 'https://uvgift.org/', 'Hands reviewing paperwork at a desk')]
more = [('giving-eventsponsorship', 'Event Sponsorship', 'https://www.uvu.edu/advancement/events/archive/scholarship-ball.html', 'A speaker at a podium in front of a Utah Valley Wolverines backdrop'),
        ('matching-gifts', 'Matching Gifts', LIVE + 'ways-to-give/matching-gifts.html', 'Two professionals talking at a table'),
        ('in-kind-donation', 'In-Kind Donation', LIVE + 'ways-to-give/in-kind-donation.html', 'A visitor viewing paintings in a gallery hallway'),
        ('service', 'Service', LIVE + 'ways-to-give/service.html', 'Volunteers in green UVU volunteer shirts')]


def wcard(f, t, u, alt):
    ext = is_ext(u)
    tg = ' target="_blank" rel="noopener"' if ext else ''
    sr = '<span class="sr-only-al"> (opens in a new tab)</span>' if ext else ''
    return f'''                  <li><a class="al-news-card" href="{u}"{tg}>
                     <img src="assets/{f}.jpg" data-cms-src="/give/ways-to-give/images/{f}.jpg" alt="{alt}" width="1200" height="750" loading="lazy">
                     <div class="al-card-body"><h3>{t}</h3><p class="al-meta">{flag("Learn More", "Live: “Learn more about [option]” under every card; the whole card is now the link.")}{sr}</p></div>
                  </a></li>'''


w = hero(1, f'assets/{S}-header.jpg', '/give/ways-to-give/images/ways-to-give-header.jpg', 'Ways to Give')
w += one(2, head('Financial Donations',
                 f'There are many ways you can support UVU. Your financial donations open doors by supporting scholarships, the faculty, academic programs, and athletics. Sponsorship of the {flag("President’s Scholarship Ball", "Stale event name? The event is now the Presidential Scholarship Banquet (PSB). Confirm the name and the 115-student figure.")} helps provide 115 students annually with merit scholarships.',
                 f'{flag("Eighty-seven percent", "Confirm the stat is current.")} of UVU graduates remain in the state. An investment in UVU is not just an investment in our students; it’s an investment in Utah’s future.') +
         '\n               ' + grid([wcard(*c) for c in fin], 3), note='Intro + six financial options as photo cards (whole card is the link).')
w += one(3, head('More Ways to Give', lead=False) + '\n               ' + grid([wcard(*c) for c in more], 4), cls='al-section--warm',
         note='Non-cash options. Same card. The repeated “Give Online / Mail a Check” block moves into the Give footer.')
w += footer(4)
P[S] = ('Ways to Give', 'Ways to give to Utah Valley University: scholarships, annual giving, memorial gifts, securities, gift planning, and more.', 'https://www.uvu.edu/give/ways-to-give/index.html', w)

# ======================================================================
# ANNUAL GIVING
# ======================================================================
S = 'annual-giving'
an = hero(1, f'assets/{S}-header.jpg', '/advancement/images/ways-to-give/annual-giving-header.jpg', 'Annual Giving', eyebrow='UVU',
          button=(flag('See Where You Can Give', 'Live: “Online Giving Areas” link at the bottom of the page.'), '../give-home/index.html'))
an += split(2, text(flag('Why Annual Giving Matters', 'Placeholder heading. Live has none.'),
                    f'Utah Valley University’s (UVU) Annual Giving team plays a vital role in fostering student success and advancing the university’s mission of accessible education, innovation, and building communities. Gifts directly support scholarships, academic programs, and campus resources{flag(", empowering", "Live: hyphen used as a dash (“resources - empowering”).")} UVU students to achieve their dreams and build brighter futures.',
                    f'Your gift exemplifies exceptional care, ensuring every UVU student has access to the tools and opportunities they need to succeed{flag(". UVU", "Live joins three sentences with semicolons; split for reading.")} upholds exceptional accountability by stewarding your generosity with integrity, directing it to initiatives with a tangible impact. Together, we achieve exceptional results by preparing UVU graduates to contribute meaningfully to Utah’s economy and society.',
                    after=f'''
               <ul class="al-linklist">
                  <li>{xlink(icon('diploma-3') + 'Scholarships', LIVE + 'ways-to-give/scholarships.html')}</li>
                  <li>{xlink(icon('donation') + 'Matching Gifts', LIVE + 'ways-to-give/matching-gifts.html')}</li>
                  <li>{link_to(icon('team') + 'Employee Giving', 'employee-giving')}</li>
               </ul>'''),
            frame('assets/annual-giving-impact.jpg', '/give/ways-to-give/images/annual-giving-impact.jpg', 'A UVU student smiling as she walks across campus'),
            note='Live quick links (Scholarships, Matching Gifts, Employee Giving) move under the copy as a link list.')
an += one(3, head('Contacts', lead=False) + '\n               ' + grid([
    contact_card('Tess Fontanetti-Rice', 'Director of Annual Giving', 'K0NqdWZaMXlvSER0SzJWMmt6NjU1QT09', '801-863-8568', 111),
    contact_card('Zachary Browning', 'Assistant Director, Annual Giving', 'clo4ejdVYjFLaitUTWZQbTRmWWRzUT09', '801-863-8888', 111),
    contact_card('Erin McCarthy', 'Assistant Development Director, Development', 'cjloRjB6a0ZjVkNMUnpoQklvNmN0Zz09', '801-863-8568', 111)], 3),
    cls='al-section--warm', note='Directory contacts as cards. Live pulls these from the directory widget; keep the widget if it stays in sync. Phone formats evened out (live mixes 801-863-8568 and (801) 863-8888).')
an += footer(4)
P[S] = ('Annual Giving', 'UVU Annual Giving supports scholarships, academic programs, and campus resources for Utah Valley University students.', 'https://www.uvu.edu/give/ways-to-give/annual-giving.html', an)

# ======================================================================
# EMPLOYEE GIVING
# ======================================================================
S = 'employee-giving'
iam = [('kyrsi-zamora', 'Kyrsi Zamora', 'Coordinator, UVU Latino Initiative', 'As a first-generation student, I endured many financial challenges, but I got the support from UVU to get through college. I am grateful that I am able to donate to do the same for our students now. Remember, it takes a village to help a student graduate. Be part of that village.'),
       ('garth-tino', 'Garth Tino', 'Program Risk Manager, College of Science', 'I give because I believe in education. Both of my parents were public school teachers and I see the value of education. I like to donate because I know how difficult it can be to balance work and school, and it is nice to know that I can help my students.'),
       ('troy-wilson', 'Chef Troy Wilson', 'Chef, Culinary Arts Institute', 'When it all starts to click for our students, and I can see the ‘light bulb’ turn on by the look in their eyes. That’s when it comes full circle for me. That’s when I know that my small contribution monthly really has made a difference in someone’s life.'),
       ('deborah-marrott', 'Deborah Marrott', 'Associate Dean, College of Humanities and Social Sciences', 'I shifted my payroll deduction in 2020 to the Student Emergency and Care Fund which helps students with basic but essential survival needs. These small, quick emergency grants are so essential to helping students stay at UVU and succeed. If each one of us donated just $5 a month to the SEC Fund, we could raise a significant amount to help students stay in school.'),
       ('raymundo-yazzie', 'Raymundo Yazzie', 'GEAR UP Mentor, Student Affairs', 'Education has helped me to be healthier, think better, and has given me the confidence to face challenges in my life. I give so that someone else can receive similar empowerment in their life.'),
       ('karen-cushing', 'Karen Cushing', 'Executive Assistant, School of Education', 'I have seen firsthand the benefits of giving and creating opportunities for individuals who are in need and it makes me happy knowing I have been able to contribute to the success of others.')]
qh = '<ul class="al-quotes al-quotes--3">' + ''.join(f'''
                  <li><figure class="al-quote al-quote--person"><blockquote><p>“{q}”</p></blockquote><figcaption><img class="al-quote-photo" src="assets/iamuvu-{k}.jpg" data-cms-src="/give/ways-to-give/images/iamuvu-{k}.jpg" alt="" width="240" height="240" loading="lazy"><span class="al-quote-who">{n}<span class="al-quote-role">{r}</span></span></figcaption></figure></li>''' for k, n, r, q in iam) + '\n               </ul>'
DONATE = 'https://www.uvu.edu/give/employee-giving/index.html'
faq = [('Why Should I Give to UVU?', '<p>Your gift will support students and help fulfill UVU’s mission of providing exceptional care when you give to scholarship, program, or building funds.</p><p>It’s an easy way to show your support of UVU as an institution and as an employer.</p><p>Research shows that giving increases your overall happiness.</p>'),
       ('How Can I Donate?', f'<p>The quickest and easiest method is via payroll deduction. You can set up or change your payroll deduction through the {xlink("Employee Payroll Deduction Hub", PAYROLL)}. You can also make a one-time or recurring gift on our <a href="{DONATE}">donation page</a>. If you prefer to give via check or cash, please contact Tess Fontanetti-Rice at <a href="mailto:tessf@uvu.edu">tessf@uvu.edu</a>.</p>'),
       ('What Is the Minimum Amount I Can Donate?', '<p>The minimum amount for payroll deduction is $1 per paycheck and $10 for credit card donations.</p>'),
       ('What Are the Advantages of Payroll Deduction?', f'<p>Payroll deduction is fast and easy. A payroll deduction of just $5 per paycheck adds up to a $120 contribution by the end of the year. If every employee on campus gave just $5 per paycheck, it would equal nearly half {flag("a million dollars", "Live: “half of a million.”")} for the {flag("university", "Live: “University.” UVU style: lowercase on its own.")} to use for scholarships, program development, and building construction.</p>'),
       ('How Do I Set Up, Manage, or Change My Payroll Deduction?', f'<p>Once you complete the {xlink("Employee Payroll Deduction Form", PAYROLL)}, the amount you specify will be automatically deducted from each paycheck. Please note that it may take one or two pay periods for a new or updated deduction to take effect due to the payroll processing cycle and the timing of form submission.</p><p>Your payroll deduction will continue until you choose to make a change. To manage your deduction, whether you want to adjust the amount, add a new gift, or cancel it altogether, revisit the {xlink("Employee Giving Hub", PAYROLL)} and select the appropriate option:</p><ul><li>Terminate my current donation</li><li>Replace it with a new donation</li><li>Keep my existing donation and add an additional one</li></ul><p>A charitable receipt summarizing your payroll deductions will be mailed to you in January for tax purposes.</p>'),
       ('Can Part-Time Employees Donate Using Payroll Deduction?', '<p>Part-time employees may sign up for payroll deduction. If there is a pay period in which you did not receive a paycheck, no donations will be processed. Your usual donation amount will be deducted from your next paycheck. Donations will not be deducted “in arrears” in a cumulative amount.</p>'),
       ('What if I Don’t Want to Give Through Payroll Deduction?', f'<p>One-time or recurring gifts are also appreciated and simple to do on our <a href="{DONATE}">donation page</a>. If you prefer to donate via check, stocks, property, using a donor-advised fund, or utilizing an IRA rollover, please contact Vicky Hopper at <a href="tel:+18018635426">801-863-5426</a> or <a href="mailto:vicky.hopper@uvu.edu">vicky.hopper@uvu.edu</a>.</p>'),
       ('Is My Gift Tax-Deductible?', '<p>Yes. All donations are processed through the Utah Valley University Foundation, a 501(c)(3) nonprofit organization. Please keep the official receipt for your tax records. Contributions are tax-deductible to the extent allowed by law. Please consult with your tax advisor to determine if your gift is tax-deductible as a charitable contribution.</p>'),
       ('When Will I Receive My Receipt?', '<p>For one-time gifts, you will receive an email receipt right away. Please keep this for your records.</p><p>For payroll deductions, you will receive a receipt in January for all gifts made during the previous calendar year.</p>'),
       ('How Is Donating Different Than Giving to PACE?', f'<p>PACE provides an opportunity to create a culture of exceptional care by contributing a non-charitable $0.50 per paycheck through the Goodwill Association. Funds are used to send well wishes and floral baskets for various reasons to UVU employees. {flag("Learn more about the Goodwill Association", "Live link text: “click here.” WCAG 2.4.4: link text names the destination.")} on <a href="https://my.uvu.edu/workplace/pace/involved/goodwill-association.html">myUVU</a>.</p>'),
       ('Does My Donation Qualify for a Matching Gift?', f'<p>Even though UVU does not offer a matching gift program, many employers will match a spouse’s charitable contribution and/or volunteer hours. To find out if a company you have connections with offers a matching gift program, see <a href="https://www.uvu.edu/advancement/ways-to-give/matching-gifts.html">{flag("Matching Gifts", "Live link text: “click here.”")}</a>. If your company is eligible, request a matching gift form and submit it to <a href="mailto:matchinggifts@uvu.edu">matchinggifts@uvu.edu</a>.</p>'),
       ('What’s the Best Way to Leave a Legacy on Campus?', f'<h3>Gift Planning</h3><p>Many people choose a long-term approach to giving using a bequest, will, annuity, or trust. The tax benefits vary depending on the type of gift chosen. Different gift types allow you access to your funds in case you need them, as your donation will take place after you have passed on. If you are interested, please visit us at {xlink("uvgift.org", "https://uvgift.org/")}.</p><h3>Presidential Scholar Commemorative Bench</h3><p>You may also leave a physical imprint on campus by naming a UVU bench. A named bench can also be used to honor the accomplishments of individuals or organizations or can be designated in memoriam of a loved one, professor, colleague, friend, etc. Your gift to the Presidential Commemorative Bench project will {flag("forever", "Live: “FOREVER” in caps.")} improve the campus landscape and help support the academic success of a UVU Presidential Scholar. Learn more about <a href="https://uvu.edu/give/fund/commemorative.html">{flag("commemorative benches", "Live link text: “click here.”")}</a>.</p>')]
faqh = '\n'.join(f'''               <details class="al-accordion accordion-unstyled">
                  <summary>{q}</summary>
                  <div class="al-accordion-body">{x}</div>
               </details>''' for q, x in faq)
eg = hero(1, f'assets/{S}-header.jpg', '/give/ways-to-give/images/employee-giving-header.jpg', 'Employee Giving', eyebrow='UVU',
          button=(flag('Set Up Payroll Deduction', 'Live: “Payroll Deduction” and “PAYROLL DEDUCTION FORM.” The label now says what you’ll do.'), PAYROLL),
          note=flag('Opens the Employee Form Hub. Gifts start at $1 per paycheck.', 'New microcopy built from the FAQ’s $1 minimum.'))
eg += one(2, head(flag('More Than Colleagues', 'Placeholder heading from the intro’s first line. Live heading repeats “EMPLOYEE GIVING.”'),
                  'At UVU, we are more than just colleagues; we are a community united by a shared mission to shape the future through empowering students to achieve their educational dreams.',
                  'Your time, energy, and passion already make UVU a better place. Employee Giving is an ongoing invitation to amplify your support by giving back to programs and initiatives that matter most to you.',
                  'This is an opportunity to extend your passion further. Every gift, no matter the size, makes a difference in students’ lives now and in the future. This is your chance to make your impact go beyond what you already contribute every day.'),
          note='Intro.')
eg += one(3, head('Employee Giving in 2025', lead=False) + '\n               ' + stats([('2,359', 'gifts'), ('$310,428', 'raised'), ('107', 'semesters of tuition')], 'al-stats--3'),
          cls='al-section--warm', note='Stat cards replace three clip-art PNG icons (gift, letter, backpack).')
eg += one(4, head('Ways to Support UVU Students', lead=False) + '\n               ' + grid([
    card('cash-2', 'Payroll Deduction', '<p>This is the quickest and easiest method to support an area on campus or a community partner that is meaningful to you without incurring a big hit on the wallet. If all UVU employees donate, the cumulative effort will have a significant impact in supporting students. Donations can be as little as $1 per paycheck. We welcome all amounts and are grateful for your contribution!</p>', ('Set Up Payroll Deduction', PAYROLL)),
    card('credit-cards', flag('One-Time Gifts', 'Live: “One-time Gifts.” Title Case.'), f'<p>One-time gifts are also appreciated! You are welcome to make a one-time, recurring, or pledge gift {flag("online", "Live: “by visiting uvu.edu/give.” The card action is now the link.")}. If you prefer to donate using other means, please call the Annual Giving office at <a href="tel:+18018634962">801-863-4962</a> or send an email to <a href="mailto:annualgiving@uvu.edu">annualgiving@uvu.edu</a>.</p>', ('Give Online', DONATE)),
    card('paper', 'Tax-Deductible', '<p>All donations are processed through the Utah Valley University Foundation, a 501(c)(3) nonprofit organization. Please keep the official receipt for your tax records. Contributions are tax-deductible to the extent allowed by law. Please consult with your tax advisor to determine if your gift is tax-deductible as a charitable contribution.</p>')], 3),
    note='Three ways as cards.')
eg += one(5, head('I Am UVU', lead=False) + '\n               ' + qh, cls='al-section--warm',
          note='The six “I AM UVU” graphics had every quote baked into the image (unreadable to screen readers and search, cropped on phones). Now real text with headshots cropped from the same photos. Quotes transcribed verbatim from the graphics.')
eg += one(6, '               <div class="al-section-head"><h2>Employee Giving FAQ</h2></div>\n               <div class="al-narrow">\n' + faqh + '\n               </div>', note='FAQ (al-accordion). Twelve questions, Title Case.')
eg += one(7, head(flag('Questions? Contact Us', 'Live: “QUESTIONS? Contact us!”'), lead=False) + '\n               ' + grid([
    contact_card('Tess Fontanetti-Rice', 'Director of Annual Giving', 'K0NqdWZaMXlvSER0SzJWMmt6NjU1QT09', '801-863-8568', 111)], 3, 'al-grid--center'),
    cls='al-section--warm', note='Contact.')
eg += footer(8)
P[S] = ('Employee Giving Initiative', 'UVU Employee Giving: support students through payroll deduction or a one-time gift. Gifts start at $1 per paycheck.', 'https://www.uvu.edu/give/ways-to-give/employeegiving.html', eg)

# ======================================================================
# MEMORIAL GIFTS
# ======================================================================
S = 'memorial-gifts'
mg = hero(1, f'assets/{S}-header.jpg', '/give/ways-to-give/images/memorial-gifts.jpg', 'Memorial Gifts', eyebrow='UVU',
          button=(flag('Give a Memorial Gift', 'New: jumps to the giving form, which live buries mid-page.'), '#give-now'))
mg += split(2, text('What Is a Memorial Gift?',
                    'Memorial gifts are a meaningful way to celebrate the life and legacy of a loved one, whether they are no longer with us or still living. Your contribution pays tribute to their impact while supporting Utah Valley University. By giving in their name, you ensure their values and spirit continue to inspire and create positive change for others.',
                    after=f'''
               <ul class="al-linklist">
                  <li>{xlink(icon('cell') + 'Call 801-863-8568', 'tel:+18018638568')}</li>
                  <li>{xlink(icon('envelope-1') + 'Email giving@uvu.edu', 'mailto:giving@uvu.edu')}</li>
               </ul>
               <p class="al-meta">{flag('Questions about a memorial gift? Contact Institutional Advancement.', 'Live: “If you would like to make a memorial gift to UVU, please contact Institutional Advancement.” Shortened; the form below now handles the gift itself.')}</p>'''),
            frame('assets/memorial-gifts-flowers.jpg', '/give/ways-to-give/images/memorial-gifts-small.jpg', 'A bouquet of white flowers wrapped in paper with a green ribbon') +
            f'<p class="al-meta">{todo("PHOTO: live image is 600px wide; needs a higher-resolution version.")}</p>',
            note='Definition + direct contact.')
mg += one(3, grid([
    card('donation', 'In Memoriam', '<p>In lieu of flowers, many people choose to donate in their loved one’s name. In memoriam gifts allow families to remember their loved ones and pay tribute to them while helping the deceased’s legacy live on through a meaningful contribution to a good cause.</p>'),
    card('award', 'In Honor Of', '<p>A thoughtful way to celebrate a special person or occasion while making a difference. Whether marking a birthday, anniversary, achievement, or other milestone, your contribution recognizes their impact.</p>')], 2),
    cls='al-section--warm', note='The two gift types as cards (live: two run-in paragraphs with hyphens as dashes).')
mg += with_id(one(4, head('Honor a Life, Inspire a Future',
                          'If you’re looking to make a meaningful gift in honor or memory of someone special, but don’t have a specific fund in mind, consider supporting the UVU Memorial Scholarship. Your donation not only celebrates their life and legacy, but also opens doors for future students by providing access to education and opportunity at Utah Valley University.') + f'''
               <div class="al-form-embed">
                  <div class="al-form-embed-placeholder">{icon('donation')}
                     <p><strong>UVU Memorial Scholarship giving form</strong></p>
                     <p class="al-meta">{todo("EMBED: keep the live Blackbaud donation form code here (gift type, amount, tribute fields). It does not render in the offline mockup.")}</p>
                  </div>
               </div>''', note='The giving form gets its own section and an anchor (#give-now) so the hero button can jump to it. Live heading “Give Now” becomes the section’s purpose line.'), 4, 'give-now')
mg += one(5, head(flag('Questions? Contact Us', 'Live shows the contact card with no heading.'), lead=False) + '\n               ' + grid([
    contact_card('Tess Fontanetti-Rice', 'Director of Annual Giving', 'K0NqdWZaMXlvSER0SzJWMmt6NjU1QT09', '801-863-8568', 111)], 3, 'al-grid--center'),
    note='Contact.')
mg += footer(6)
P[S] = ('Memorial Gifts', 'Make a memorial gift to Utah Valley University in memory or in honor of someone special.', 'https://www.uvu.edu/give/ways-to-give/memorial-gifts.html', mg)

if __name__ == '__main__':
    for slug, (title, desc, url, main) in P.items():
        os.makedirs(f'{OUT}/{slug}/assets', exist_ok=True)
        open(f'{OUT}/{slug}/index.html', 'w').write(page(slug, title, desc, url, main))
        print('wrote', slug)
