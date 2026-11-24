import os, sys
sys.path.insert(0, '/tmp/xr')
from build2 import *
from episodes import latest_feature
POD = '../forever-wolverines-podcast/index.html'
EVENTS = 'https://www.uvu.edu/events/index.html'
STORIES = 'https://www.uvu.edu/news/features/index.html#alumni'

P = {}
PROFILE = 'https://alumni.uvu.edu/profile/me'

# ======================================================================
# HOME
# ======================================================================
quick = [('calendar', 'Events', 'https://www.uvu.edu/events/index.html'),
         ('business', 'Alumni Businesses', 'https://alumni.uvu.edu/page/business-directory'),
         ('automotive', 'License Plate', 'https://www.uvu.edu/alumni/make-an-impact/uvu-license-plate.html'),
         ('diploma-3', 'Scholarships', 'https://www.uvu.edu/alumni/make-an-impact/alumni-scholarships.html'),
         ('communicate', 'Alumni Ambassadors', 'https://www.uvu.edu/alumni/students/about-saa.html'),
         ('graduation', 'Graduates', 'https://www.uvu.edu/alumni/students/graduating-students.html'),
         ('credit-cards', 'Alumni Benefits', 'https://www.uvu.edu/alumni/resources/benefits/alumni-benefits.html')]
ql = '\n'.join(f'                  <li>{xlink("<span>" + l + "</span>", u, ic=icon(i))}</li>' for i, l, u in quick)
news = [('UVU Aviation Graduates, Brothers Pilot Inaugural Flight for Breeze Airways', 'Sept. 1, 2026'),
        ('UVU Business Resource Center Company Earns $500K Investment', 'Aug. 30, 2026'),
        ('UVU Alum Thomas Dilworth Brings Hoops Team to Visit UVU and Utah Jazz', 'May 13, 2026'),
        ('UVU Helps Former Sports Journalist Become Award-Winning Teacher', 'June 28, 2025')]
nc = '\n'.join(f'''                  <li><a class="al-news-card" href="https://www.uvu.edu/alumni/connect/alumni-stories/">
                     <img src="assets/news-{i}.jpg" alt="" width="1200" height="750">
                     <div class="al-card-body"><p class="al-meta">{d}</p><h3>{t}</h3></div>
                  </a></li>''' for i, (t, d) in enumerate(news, 1))
h = hero(1, 'assets/alumni-home-header.jpg', '/alumni/images/alumni-home-header.jpg', 'Show Your School Spirit as UVU Alumni',
         button=('Claim Your Alumni Profile', PROFILE))
h += one(2, f'''               <h2 class="sr-only-al">Explore Alumni Relations</h2>
               <ul class="al-quicklinks">
{ql}
               </ul>''', note='Quick links. Icons: UVU Icon Library (green).')
h += one(3, head('Once a Wolverine, Always a Wolverine',
                 'The Office of Alumni Relations helps our UVU alumni community—more than 120,000 strong—thrive. We connect alumni to UVU, current students, and each other through diverse and impactful programs, communications, and volunteer opportunities.'),
         note='Intro statement. Same pattern opens every page that has one.')
h += split(4, text('Stay Connected',
                   'Be the first to know about UVU alumni events, benefits, and volunteer opportunities by making sure your contact information is up to date.',
                   f'Manage your subscriptions and start receiving the Wolverine Minute monthly newsletter through <a href="{PROFILE}">your alumni profile</a>.',
                   after='\n               ' + actions(btn('Update Your Alumni Profile', 'https://alumni.uvu.edu/login', note=flag('You’ll log in on the UVU alumni site.', 'New microcopy: sets the login expectation before the click.')))),
           frame('assets/alumni-home-stayconnected.png', '/alumni/images/alumni-home-stayconnected.png', 'UVU alum working on a laptop by a window overlooking campus'))
h += split(5, text('Wolverine Pride Wherever You Go',
                   'With three unique options to choose from, there’s a card designed to fit your lifestyle. Each one offers distinct advantages to support your financial journey while celebrating your connection to UVU.',
                   after=f'\n               {actions(btn("Apply for the Wolverine Card", "https://uvu.edu/wolverinecard"))}\n               <p class="al-meta">{todo("ROTATING PROMO SLOT · current item: Wolverine Card")}</p>'),
           '<img class="al-product" src="assets/alumni-wolverinecard.png" data-cms-src="/alumni/images/alumni-wolverinecard.png" alt="Green and black UVU Wolverine Visa cards" width="828" height="572">',
           note='Promo band. Replaces the XD "[Rotating CTA]" header: the promo itself is the heading. White now: the podcast band below is warm.')
h += split(6, text('Forever Wolverines Podcast',
                   'The Forever Wolverines podcast is created and produced by the UVU Student Alumni Ambassadors. Each ambassador selects an alum and meets with them on air.',
                   'They ask about the alum’s career, time at school, advice, and more. New episodes drop every other week.',
                   after=f'''
               {actions(btn('Listen to the Podcast', POD))}
               <ul class="al-linklist">
                  <li>{xlink('Read Alumni Stories', STORIES, ic=icon('report'))}</li>
                  <li>{xlink('See Upcoming Events', EVENTS, ic=icon('calendar'))}</li>
               </ul>'''),
           latest_feature('stairs'),
           cls='al-section--warm', note='Latest episode as a linked photo (guest and host, not the show logo; the Spotify show embed displayed the logo artwork). Update with each new episode. Replaces the Alumni Stories card row (per Zoe): the podcast is the alumni-made story channel. Stories now link out to UVU News features (alumni filter), which Central is building anyway. Events link to the university calendar.')
h += contact(7)
P['alumni-home'] = ('Alumni', 'Utah Valley University Alumni Association: events, benefits, scholarships, and ways to stay connected.', 'https://www.uvu.edu/alumni/', h)

# ======================================================================
# BENEFITS
# ======================================================================
b = hero(1, 'assets/alumni-benefits-header.jpg', '/alumni/resources/images/benefits/alumni-benefits-header.png', 'Benefits', eyebrow='UVU Alumni',
         button=(flag('See Your Alumni Benefits', 'Live/XD label “I’m an Alum” doesn’t say what happens (WCAG 2.4.4 link purpose).'), 'https://alumni.uvu.edu/page/alumni-benefits'),
         note=flag('Log in with your alumni profile to see them.', 'New microcopy: sets the login expectation.'))
b += one(2, head('Your Degree Opens Doors. Your Membership Keeps Them Open.',
                 'Register as a UVU Alumni Association member and get access to discounts on Lagoon, sporting events, Quick Quack, and more. Benefits built for people who stayed part of this community.') +
         '\n               <ul class="al-logos" aria-label="Benefit partners">\n                  <li><img src="assets/alumni-benefits-logo-athletics.png" data-cms-src="/alumni/resources/images/benefits/logo-athletics.png" alt="UVU Athletics" width="245" height="179"></li>\n                  <li><img src="assets/alumni-benefits-logo-quickquack.png" data-cms-src="/alumni/resources/images/benefits/logo-quickquack.png" alt="Quick Quack Car Wash" width="413" height="169"></li>\n                  <li><img src="assets/alumni-benefits-logo-lagoon.png" data-cms-src="/alumni/resources/images/benefits/logo-lagoon.png" alt="Lagoon" width="393" height="111"></li>\n                  <li><img src="assets/alumni-benefits-logo-uccu.png" data-cms-src="/alumni/resources/images/benefits/logo-uccu.png" alt="UCCU" width="330" height="167"></li>\n                  <li><img src="assets/alumni-benefits-logo-noorda.png" data-cms-src="/alumni/resources/images/benefits/logo-noorda.png" alt="The Noorda" width="444" height="108"></li>\n               </ul>')
b += split(3, text('Become a Member',
                   'Membership is free for all graduated alumni.',
                   'Log in to your alumni profile to access the benefits and adjust your preferences. Use the email you receive UVU Alumni communications from to avoid delays.',
                   after='\n               ' + actions(btn(flag('Log In to Your Alumni Profile', 'XD label “Access Membership” → says exactly where it goes.'), PROFILE))),
           frame('assets/alumni-benefits-becomeamember.png', '/alumni/resources/images/benefits/alumni-benefits-becomeamember.png', 'UVU graduate doing the UVU hand sign with Willie the Wolverine'))
b += split(4, text('Opportunities for Alumni',
                   'Make sure you’re subscribed to the monthly Wolverine Minute newsletter to be the first to know about all new benefits.',
                   flag('Log in to your alumni profile to see the current perks and discounts.', '“Click the button below” dropped: screen readers and phones don’t have “below,” and the button says it.'),
                   after='\n               ' + actions(btn(flag('See Current Perks and Discounts', 'Was “See Alumni Benefits,” same label as the hero but a different section purpose.'), 'https://alumni.uvu.edu/page/alumni-benefits'))),
           frame('assets/alumni-benefits-opportunities.png', '/alumni/resources/images/benefits/alumni-benefits-opportunities.png', 'Young UVU alumni tailgating with UVU pennants beside an SUV with a UVU license plate'),
           reverse=True)
b += one(5, head(flag('Utah Jazz and Utah Mammoth', 'Monica’s heading: “Utah Jazz and Mammoths.” The NHL team is the Utah Mammoth (singular), so the plural reads as a typo. Confirm the final wording with Monica.'),
                 'Get discounted tickets to certain Utah Jazz and Mammoth games throughout the season.',
                 f'With the discount, Jazz tickets start at $17 and Mammoth tickets start at $59 {flag("plus taxes and fees", "Monica’s text: “(+ taxes and fees)”. AP: spell out “plus” in running copy.")}.',
                 extra='\n                  ' + actions(btn(flag('Purchase Jazz and Mammoth Tickets', 'Monica’s label: “Purchase Jazz &amp; Mammoth Tickets.” “and” matches the rest of the system’s buttons.'), 'https://www.utahjazz.group/uvu2627'))),
         cls='al-section--warm', note='NEW per Monica (Oct. 1): Jazz and Mammoth discount band. Splash Summit does not appear on this page, so nothing to remove here; if it is in the alumni.uvu.edu perks list, remove it there.')
b += split(6, text('UVU Resources',
                   'As a UVU alum, you still have access to many of the benefits you had as a student.',
                   f'That includes the {flag("Career &amp; Internship Center", "AP: “and” in running copy. Keep “&amp;” only if that’s the center’s formal name.")} and the Fulton Library. Most of these resources are free or at a discounted price.',
                   after='\n               ' + actions(btn(flag('See Campus Resources for Alumni', 'Was “See Alumni Resources.”'), 'https://www.uvu.edu/alumni/resources/benefits/alum-campus-benefits.html'))),
           frame('assets/alumni-benefits-resources.png', '/alumni/resources/images/benefits/alumni-benefits-uvuresources.png', 'Two people working together at a table in front of a whiteboard'),
           note='Back to white after the warm discount band.')
b += contact(7)
P['alumni-benefits'] = ('UVU Alumni Benefits', 'Explore UVU Alumni Benefits: free access to networking, events, career support, and exclusive discounts.', 'https://www.uvu.edu/alumni/resources/benefits/alumni-benefits.html', b)

# ======================================================================
# GRADUATES
# ======================================================================
gl = [('graduation', flag('Alumni 101 Guide (PDF)', 'File type in the label (WCAG: tell people before they open a PDF).'), 'https://www.uvu.edu/alumni/students/docs/gradfest26_alumni101-guide.pdf'),
      ('calendar', flag('Party Ideas on Pinterest', 'Was “Plan Your Party”; it opens a Pinterest board.'), 'https://pin.it/6pjLdXqJ4'),
      ('student-life', 'Decorations (PDF)', 'https://www.uvu.edu/alumni/students/docs/al-gradpack26-decorations.pdf'),
      ('photography', 'UVU Photo Props (PDF)', 'https://www.uvu.edu/alumni/students/docs/al-grad-pack_photo-props_proof1-accessible.pdf')]
gll = '\n'.join(f'                  <li>{xlink(l, u, ic=icon(i))}</li>' for i, l, u in gl)
g = hero(1, 'assets/alumni-grads-header.jpg', '/alumni/students/images/alumni-graduation-header.jpg',
         flag('Congratulations, Graduates', 'Comma added for direct address (XD: "Congratulations Graduates").'), lead='Welcome to the UVU Alumni Association.')
g += split(2, text('Celebrate the Wolverine Way',
                   'Learn more about the UVU Alumni Association and plan your party with UVU-themed decorations, recipes, and more.',
                   after=f'\n               <ul class="al-linklist">\n{gll}\n               </ul>'),
           frame('assets/alumni-grads-celebrate.png', '/alumni/students/images/alumni-grads-celebrate.png', 'UVU graduates in caps and gowns hugging'),
           note='Four equal actions become a link list (one style for secondary actions sitewide).')
g += split(3, text('Be a Forever Wolverine',
                   flag('UVU is forever a place for you.', 'XD dropped "connected and giving" from the live line that follows.'),
                   'We are a community of over 120,000 alumni, which includes all alumni of Utah Valley University in all of its iterations. Join us on campus or virtually to connect with current students and your fellow alumni.'),
           '<!-- CMS: keep the live YouTube embed. Thumbnail + play badge shown for the mockup. -->\n               <a class="al-video" href="https://www.youtube.com/watch?v=Khkyq67cn7k" target="_blank" rel="noopener"><img src="assets/alumni-grads-spotlight-thumb.jpg" alt="Watch: Alumni Spotlight, Cassidy Read ’13, Goldman Sachs" width="820" height="462"></a>',
           reverse=True)
g += one(4, f'''               <div class="al-section-head al-section-head--left">
                  <h2>{flag('Stay Part of the UVU Community', 'Shortened from “Connect with fellow alumni and stay part of the UVU community.” Two sections on this page started with “Connect with…”.')}</h2>
                  <p class="al-lead">#ForeverWolverines #UVUAlumni</p>
                  <ul class="al-social">
                     <li><a href="https://www.instagram.com/uvualumni/" target="_blank" rel="noopener">{icon('social-instagram', 'green', alt='UVU Alumni on Instagram (opens in a new tab)')}</a></li>
                     <li><a href="https://www.facebook.com/uvualumni" target="_blank" rel="noopener">{icon('social-facebook-f', 'green', alt='UVU Alumni on Facebook (opens in a new tab)')}</a></li>
                     <li><a href="https://www.linkedin.com/showcase/uvualumni" target="_blank" rel="noopener">{icon('social-linkedin-in', 'green', alt='UVU Alumni on LinkedIn (opens in a new tab)')}</a></li>
                  </ul>
               </div>''', cls='al-section--photo', style='background-image: url(assets/alumni-grads-community-bg.jpg);',
         note='Photo band. Social icons: one treatment (green glyph on white circle) instead of brand-colored circles.')
g += split(5, text('Join Us at Upcoming Alumni Events', flag('Explore alumni events and communities happening near you.', 'Exclamation point dropped from the heading (XD: “Join us at upcoming Alumni events!”).'),
                   after='\n               ' + actions(btn('See Upcoming Events', EVENTS))),
           frame('assets/alumni-grads-events.png', '/alumni/students/images/alumni-grads-events.png', 'UVU fans cheering in the stands'))
g += split(6, text('Connect With Your Fellow Alumni',
                   flag('Check out the opportunities to stay engaged through chapters and communities.', 'Typo fixed: "opportinities".'),
                   after='\n               ' + actions(btn(flag('See Volunteer Opportunities', 'Live label “Volunteer With the Alumni Community” reads like the action itself; this says where it goes.'), 'https://www.uvu.edu/alumni/volunteer/volunteer-opportunities.html'))),
           frame('assets/alumni-grads-connect.png', '/alumni/students/images/alumni-grads-connect.png', 'Alumni at a backyard barbecue'), reverse=True)
g += split(7, text('Wolverine Pride Wherever You Go',
                   flag('With three unique options to choose from, there’s a card designed to fit your lifestyle.', 'Typo fixed vs. live: "lifstyle".'),
                   'Each one offers distinct advantages to support your financial journey while celebrating your connection to UVU.',
                   after='\n               ' + actions(btn('Apply for the Wolverine Card', 'https://uvu.edu/wolverinecard'))),
           '<img class="al-product" src="assets/alumni-wolverinecard.png" data-cms-src="/alumni/images/alumni-wolverinecard.png" alt="Green and black UVU Wolverine Visa cards" width="828" height="572">',
           cls='al-section--warm')
g += one(8, head('Looking for Your Transcript or Diploma?', lead=False, extra='\n                  ' + actions(btn('Visit the Registrar’s Office', 'https://www.uvu.edu/registrar/', 'secondary'))),
         note='Utility CTA. Secondary button: it points away from Alumni Relations.')
g += contact(9)
P['graduating-students'] = ('Graduating Students', 'Congratulations, UVU graduates. Welcome to the UVU Alumni Association.', 'https://www.uvu.edu/alumni/students/graduating-students.html', g)

# ======================================================================
# SCHOLARSHIPS
# ======================================================================
SU = 'https://uvu.scholarshipuniverse.com/'
s = hero(1, 'assets/alumni-scholarships-header.jpg', '/alumni/make-an-impact/images/alumni-scholarships-header.jpg', 'Scholarships', eyebrow='UVU Alumni',
         button=('Apply in Scholarship Universe', SU))
s += split(2, text(flag('About Alumni Scholarships', 'XD repeats the hero title (“Alumni Scholarships”) here. Functional placeholder so the H1 isn’t duplicated: your call on final copy.'),
                   'The Alumni Association is pleased to offer scholarships to UVU students.',
                   'These scholarships are funded by the generous contributions of UVU alumni, students, employees, organizations, and community members.'),
           frame('assets/alumni-scholarships-intro.png', '/alumni/make-an-impact/images/alumni-scholarships-intro.png', 'UVU graduate receiving a diploma cover on stage at convocation'))
card1 = f'''<article class="al-card">
                  <div class="al-card-tag">{icon('cash-1', 'white')}{flag('Half Tuition, Fall and Spring', 'Award pulled to the top. Seasons lowercase in running copy per UVU style; Title Case here as a label.')}</div>
                  <div class="al-card-body">
                     <h3>Future UVU Alumni Scholarship</h3>
                     <p class="al-meta">{flag('For the child or ward of a UVU alum.', 'New one-line summary of criteria item 1.')}</p>
                     <h4>{flag('Eligibility', 'New subhead: splits the old 7-item list.')}</h4>
                     <ul class="al-checklist">
                        <li>Child or ward of an alum who graduated from UVU, UVSC, UVCC, UTC at Provo, or UTTI</li>
                        <li>Sophomore at UVU with at least 30 credits (UVU or transfer)</li>
                        <li>Full-time student with a minimum 3.0 GPA</li>
                        <li>Utah resident</li>
                        <li>Seeking a bachelor’s degree at UVU</li>
                     </ul>
                     <h4>{flag('Your Application Must Include', 'New subhead.')}</h4>
                     <ul class="al-checklist">
                        <li>The alum’s name (and the name used while attending, if it changed)</li>
                        <li>The alum’s current address, email, phone number, and UVID if known</li>
                        <li>A written statement describing any barriers to graduation you face</li>
                     </ul>
                  </div>
                  <div class="al-card-foot"><p>Application opens in November. Meeting the criteria doesn’t guarantee an award.</p></div>
               </article>'''
card2 = f'''<article class="al-card">
                  <div class="al-card-tag">{icon('award', 'white')}{flag('Up to $1,750 per Semester', 'Award pulled to the top.')}</div>
                  <div class="al-card-body">
                     <h3>Student Alumni Leadership Scholarship</h3>
                     <p class="al-meta">For appointed members of the <a href="https://www.uvu.edu/alumni/students/about-saa.html">Student Alumni Ambassadors</a>.</p>
                     <h4>Eligibility</h4>
                     <ul class="al-checklist">
                        <li>Appointed member of the Student Alumni Ambassadors</li>
                        <li>Strong leadership abilities</li>
                        <li>Cumulative GPA of 3.0 or better</li>
                        <li>At least one year of full-time attendance at UVU before receiving the scholarship</li>
                        <li>Full-time student (12+ credits)</li>
                     </ul>
                     <h4>{flag('Application Questions', 'These were mixed into “Selection Criteria” on the live page.')}</h4>
                     <ol class="al-steps">
                        <li>Describe the importance of giving to the next generation of UVU students, whether as a volunteer, advocate, donor, or source of advice and career support.</li>
                        <li>{flag('Describe the qualities you possess that will make you an enthusiastic, dependable, and motivated UVU Student Alumni Ambassador.', '“they possess” changed to “you possess”.')}</li>
                        <li>Share your volunteer and leadership experience and the lessons you learned from it.</li>
                        <li>Describe in one sentence why you wish to be a UVU Student Alumni Ambassador.</li>
                     </ol>
                     <p>Finalists will be invited to an interview. Awarded {flag('fall and spring', 'Seasons lowercase per UVU style.')} semesters as funds allow.</p>
                  </div>
                  <div class="al-card-foot"><p>Application opens in November. Meeting the criteria doesn’t guarantee an award.</p></div>
               </article>'''
s += one(3, head(flag('Available Scholarships', 'New section heading (functional placeholder).'), lead=False) + f'''
               <div class="al-grid al-grid--2">
               {card1}
               {card2}
               </div>''', cls='al-section--warm', note='Scholarship cards (al-card). Same card anatomy as every other card in the system.')
s += one(4, head('How to Apply',
                 f'The majority of UVU’s scholarship applications open Nov. 1 and close Jan. 31 at {flag("11:59 pm", "UVU style: “11:59 pm” (no periods).")}.',
                 f'Questions about eligibility or the application process? Contact <a href="https://www.uvu.edu/financialaid/">UVU Financial Aid and Scholarships</a>.',
                 extra='\n                  ' + actions(btn('Apply in Scholarship Universe', SU, note=flag('Log in with your UVU ID. Applications open Nov. 1.', 'New microcopy: sets the login expectation and the date at the point of action.')))))
s += one(5, head(flag('Give to Alumni Scholarships', 'Placeholder heading. Monica: giving links to both scholarships on the page.'),
                 f'To learn more about alumni scholarships or how to contribute, contact the <a href="mailto:alumni@uvu.edu">Office of Alumni Relations</a>.') + f'''
               <div class="al-narrow"><ul class="al-linklist">
                  <li><a href="https://www.uvu.edu/give/general-scholarships/wolverine-legacy-opportunities/archive/future-uvu-alumni-endowed-scholarship.html">{icon('donation')}Give to the Future UVU Alumni Endowed Scholarship</a></li>
                  <li><a href="https://www.uvu.edu/give/general-scholarships/wolverine-legacy-opportunities/archive/student-alumni-leadership-scholarship.html">{icon('donation')}Give to the Student Alumni Leadership Scholarship</a></li>
               </ul></div>
               <p class="al-meta al-center">{todo("CONFIRM: both giving pages live under /give/…/archive/. They work, but “archive” in the path suggests they may move.")}</p>''',
         cls='al-section--warm', note='NEW per Monica: giving links for both scholarships. Link list = secondary actions; the page’s one primary stays “Apply.”')
s += contact(6)
P['alumni-scholarships'] = ('Alumni Scholarships', 'UVU Alumni Association scholarships for UVU students: the Future UVU Alumni Scholarship and the Student Alumni Leadership Scholarship.', 'https://www.uvu.edu/alumni/make-an-impact/alumni-scholarships.html', s)

# ======================================================================
# SAA
# ======================================================================
amb = [('savannah-evans', 'Savannah Evans', 'Ambassador, 2024–25', 'I just finished up my year-long ambassador position at Utah Valley University as a Student Alumni Ambassador and absolutely loved it. I learned so much about UVU, how to be a more effective leader, how to record, edit, and post podcasts (check us out on all platforms- Forever Wolverines podcast), network with inspiring alumni and community members, and celebrate school spirit through service and homecoming activities. This role has been such a meaningful part of my college experience. From organizing events and engaging with alumni, to preserving UVU traditions and creating connections that stretch across generations of Wolverines—I’ve grown so much both personally and professionally.'),
       ('callie-ross', 'Callie Ross', 'Ambassador, 2022–25', 'This scholarship has meant so much to me. The connections it allows you to make across campus and with UVU alumni is a great way to start networking for yourself. It is a super fun position to hold on campus and has such vast opportunities for us.'),
       ('makenna-koopmans', 'Makenna Koopmans', 'Ambassador, 2022–24', 'This position of being an alumni ambassador has increased my ability to make more connections and develop networking skills. It has also helped me become more understanding of diversity, students, communication, and inclusion of future and past alums!!'),
       ('max-taylor', 'Max Taylor', 'Ambassador, 2022–23', 'The financial burden that this scholarship helped relieve allowed me to not only finish my bachelors degree with no student debt, but permitted me to focus more of my time and energy into my academic success. Serving as a Student Alumni Ambassador also provided opportunities to build meaningful relationships and see firsthand the success that UVU Alumni have achieved, which encourages me and gives me hope for the future.')]
ambh = '\n'.join(f'''                  <li class="al-person">
                     <img src="assets/saa-{k}.jpg" data-cms-src="/alumni/students/images/ambassadors/{k}.jpg" alt="{n}" width="353" height="358">
                     <h3>{n}</h3>
                     <p>{y}</p>
                     <details class="accordion-unstyled"><summary>Read {n.split()[0]}’s Story</summary><p>“{q}”</p></details>
                  </li>''' for k, n, y, q in amb)
a = hero(1, 'assets/alumni-saa-header.jpg', '/alumni/students/images/alumni-saa-header.jpg',
         flag('Student Alumni Ambassadors', 'XD title “UVU Alumni Ambassadors” dropped “Student”; restored to match the program name.'), eyebrow='UVU', button=('Apply in Scholarship Universe', SU))
a += split(2, text('What Are Student Alumni Ambassadors?',
                   'Student Alumni Ambassadors (SAAs) are current UVU students who connect students across campus to the mission of the Alumni Relations office.',
                   'Our purpose is to create a “Forever Wolverines” attitude through events, programs, and information that enhance the student experience and prepare students to become engaged alumni after graduation.'),
           frame('assets/alumni-saa-what.png', '/alumni/students/images/alumni-saa-what.png', 'Group of smiling UVU students taking a selfie on campus'))
a += split(3, text('Do I Qualify for the Scholarship?',
                   f'If awarded, the scholarship provides up to $1,750 per semester ({flag("fall and spring", "Seasons lowercase per UVU style.")}) as funds allow. Recipients serve as a Student Alumni Ambassador from {flag("Aug. 15 to May 15", "AP dates: was “August 15th to May 15th”.")}.',
                   'To qualify, you must:',
                   after=f'''
               <ol class="al-steps">
                  <li>Have a cumulative GPA of 3.0 or better</li>
                  <li>Have at least 30 credit hours completed at UVU</li>
                  <li>Maintain full-time student status (12+ credits per semester)</li>
                  <li>Submit your application through Scholarship Universe with letters of recommendation</li>
                  <li>{flag('Interview as a finalist, if selected', 'XD numbering skipped 5. Reworded to fit “you must”.')}</li>
               </ol>
               <p class="al-meta">{flag('Applications open Nov. 1, 2025, and close Jan. 31, 2026, at 11:59 pm.', 'Last cycle’s dates from the live page. Update to the 2026–27 cycle.')} {todo("Criteria differ from the Scholarships page. Confirm.")}</p>
               {actions(btn('Apply in Scholarship Universe', SU))}'''),
           frame('assets/alumni-saa-qualify.png', '/alumni/students/images/alumni-saa-qualify.png', 'UVU student smiling in a bright campus building', portrait=True), reverse=True)
a += one(4, head('Hear From Our Ambassadors', lead=False) + f'''
               <ul class="al-grid al-grid--4 al-grid--people">
{ambh}
               </ul>''', cls='al-section--warm', note='Person cards (al-person). Same component as Alumni Awards recipients.')
a += contact(5)
P['about-saa'] = ('About Student Alumni Ambassadors', 'Student Alumni Ambassadors connect UVU students to the Alumni Relations mission and earn up to $1,750 per semester.', 'https://www.uvu.edu/alumni/students/about-saa.html', a)

# ======================================================================
# LICENSE PLATE
# ======================================================================
DMV = 'https://mvp.tax.utah.gov/'
faq = [('What Is the Initial Cost of a License Plate?', '<p>You will need to pay the $21.50 one-time special group plate fee for standard vehicles or $20.50 for trailers (includes postage and handling) plus the $35 annual contribution to the scholarship fund. If you have already renewed your vehicle registration for the year, you won’t need to pay it again.</p>'),
       ('What if I Want to Personalize My UVU Plate?', f'<p>You can order personalized plates with up to five alphanumeric characters.</p><p><strong>Online via DMV:</strong> Select “Change Your Plates” then complete the validation steps. Under plate information for “I want to order a,” choose “Special Group Plate.” Select “Yes” to personalize your plate. For plate type, choose “Utah Valley University Prs.” Enter your desired characters and explanation, then continue through payment and submission.</p><p><strong>At the DMV:</strong> Complete Form TC-817 and submit it with the personalized plate fee. On the form, type “Utah Valley University” under section 3, Plate and Character Selection, in the Utah Special Group Plate field.</p><p>Personalized plates cost a $66 personalized special group plate fee plus the $35 UVU scholarship donation at first. After that, a $10 personalized plate fee and the $35 donation are added to your vehicle registration each year. Learn more on the <a href="https://dmv.utah.gov/plates/personalized" target="_blank" rel="noopener">Utah DMV website<span class="sr-only-al"> (opens in a new tab)</span></a>.</p>'),
       ('Can I Use This as My UVU Parking Permit?', '<p>No. Students and employees still need to purchase a parking permit. Once you have one, you can park in specially marked parking spots.</p>'),
       ('Do I Need Front and Back UVU Plates?', '<p>No. Utah drivers are not required to have a front license plate as of Jan. 1, 2025.</p>')]
faqh = '\n'.join(f'''               <details class="al-accordion accordion-unstyled">
                  <summary>{q}</summary>
                  <div class="al-accordion-body">{x}</div>
               </details>''' for q, x in faq)
howto = f'''<div class="al-grid al-grid--3">
                  <article class="al-card"><div class="al-card-body">
                     <h3>Online via DMV</h3>
                     <ol class="al-steps">
                        <li>Select Change Your Plates and complete the validation steps.</li>
                        <li>Select Special Group Plate.</li>
                        <li>Choose whether to personalize your plate.</li>
                        <li>For plate type, choose Utah Valley University.</li>
                        <li>Continue through payment and submission.</li>
                     </ol>
                  </div></article>
                  <article class="al-card"><div class="al-card-body">
                     <h3>In Person at the DMV</h3>
                     <p>Request a special group plate for Utah Valley University. Bring a copy of one of these:</p>
                     <ul class="al-checklist"><li>Vehicle registration</li><li>License plate number</li><li>Vehicle Identification Number (VIN)</li></ul>
                  </div></article>
                  <article class="al-card"><div class="al-card-body">
                     <h3>At the Dealership</h3>
                     <p>When purchasing a car, ask the dealership for a Utah Valley University plate. All Utah car dealerships can request UVU plates for you.</p>
                  </div></article>
               </div>'''
l = hero(1, 'assets/alumni-licenseplate-header.jpg', '/alumni/make-an-impact/images/alumni-licenseplate-header.jpg', 'Custom License Plates', eyebrow='UVU',
         button=(flag('Order Your Plate Online', 'Was “Get Your Plates”: now says it’s an online order (it opens the Utah DMV portal).'), DMV))
l += one(2, head(flag('UVU License Plates Show Spirit and Support', '“&amp;” → “and” (AP; ampersands only in graphics).'),
                 'When you get Utah Valley University license plates, not only are you showing your Wolverine spirit, but you’re also giving to scholarships that help current students.',
                 'This is an affordable and stylish way to give back to the university. A UVU license plate is $35 a year, and all proceeds go to scholarships.'))
l += split(3, text('Support UVU',
                   flag('Because the UVU option is a Utah custom license plate, it’s only available for vehicles registered in Utah.', 'Grammar: “an Utah” → “a Utah”; “they are” → “it’s” to match “option”.'),
                   'It’s available to any Utah-based Wolverine fan, including community members, businesses, alumni, and students.',
                   after='\n               ' + actions(btn('Order Your Plate Online', DMV, note=flag('Opens the Utah DMV Motor Vehicle Portal.', 'New microcopy: the button leaves UVU for a state site.')))),
           frame('assets/alumni-licenseplate-support.png', '/alumni/make-an-impact/images/alumni-licenseplate-support.png', 'UVU alum loading an SUV with a UVU license plate in the canyon', portrait=True))
l += split(4, text(flag('What Your Plate Will Look Like', 'XD still had Benefits copy here. Live plate content swapped in.'),
                   flag('The new design features the Wolverine head logo next to a new set of alphanumeric characters.', 'Live copy said “New design coming July 1, 2026!”, which has passed.'),
                   'If you get one for a vehicle you already own, you keep your existing expiration and renewal dates. An annual tax-deductible $35 donation is included when you renew your registration.',
                   after=f'\n               <p class="al-meta">{todo("PHOTO shows a personalized plate (GO UVU) from the July 2026 alumni plate shoot. Swap for a standard-number plate shot if one exists.")}</p>'),
           frame('assets/alumni-licenseplate-look.png', '/alumni/make-an-impact/images/alumni-licenseplate-look.png', 'Close-up of a UVU license plate on the back of a Ford Bronco'), reverse=True)
l += one(5, head('Already Have One?',
                 'If you already have a Utah Valley University license plate, thank you! Your contribution has helped raise thousands of dollars for scholarships, benefiting many students.'),
         cls='al-section--warm', note='Thank-you band. Was a split with a magenta placeholder in XD; no photo needed.')
l += one(6, head(flag('How to Order Your UVU Plate', 'Live heading said “Personalized,” but the steps cover every plate.'), lead=False) + '\n               ' + howto + '\n               ' + actions(btn('Order Your Plate Online', DMV)).replace('al-actions"', 'al-actions al-actions--center"'),
         note='Three ordering methods as cards (al-card).')
l += one(7, '               <div class="al-section-head"><h2>Frequently Asked Questions</h2></div>\n               <div class="al-narrow">\n' + faqh + '\n               </div>',
         note='FAQ (al-accordion).')
l += contact(8)
P['uvu-license-plate'] = ('UVU Custom License Plate', 'Get a UVU custom license plate. $35 a year, and all proceeds go to scholarships.', 'https://www.uvu.edu/alumni/make-an-impact/uvu-license-plate.html', l)

# ======================================================================
# AWARDS
# ======================================================================
cats = [('UVU Alumni Impact Award', 'Honoring a UVU alum in the early stages of their career who demonstrates:', ['Perseverance and dedication to their field', 'Significant impact through success, innovation, or leadership', 'Contributions to their industry, community, or society at large'], 'This award recognizes emerging talent poised to make a lasting difference.'),
        ('UVU Honorary Alumni Award', 'Honoring a non-graduate who has demonstrated:', ['Deep loyalty to UVU', 'Exceptional service to the university', 'Significant support for UVU’s mission'], 'This award recognizes individuals who embody the spirit of UVU despite not being alumni.'),
        ('University Partner Award', 'Recognizing a business that exemplifies:', ['Pioneering initiatives benefiting the community', 'Alignment with UVU’s mission', 'Excellence in strategic planning and employee development', 'Commitment to community involvement', 'Outstanding customer service and corporate integrity'], 'This award celebrates organizations that enhance both UVU and the broader community.'),
        ('UVU Distinguished Alumni Award', 'Honoring a seasoned UVU graduate who has:', ['Achieved notable long-term success in their career', 'Made significant contributions to their field, industry, or community', 'Enhanced UVU’s reputation through their accomplishments'], 'This prestigious award recognizes alumni who exemplify excellence and have created a lasting impact.'),
        ('Wilson W. Sorensen Lifetime Achievement Award', 'Honoring a UVU employee or volunteer (past or present) who has:', ['Dedicated their life to furthering UVU’s purposes and mission', 'Demonstrated long-term, consistent service to the university', 'Made a lasting impact on UVU’s growth and development'], 'Named after <a href="https://www.uvu.edu/studentcenter/sorensen/">Wilson W. Sorensen</a>, UVU’s president of 36 years, this award recognizes extraordinary lifetime commitment to the institution.')]
catsh = '\n'.join(f'''                  <details class="al-accordion accordion-unstyled">
                     <summary>{t}</summary>
                     <div class="al-accordion-body"><p>{lead}</p><ul class="al-checklist">{"".join(f"<li>{x}</li>" for x in li)}</ul><p>{tail}</p></div>
                  </details>''' for t, lead, li, tail in cats)
rec = [('jane-rhodes', 'Jane F. Rhodes ’15', 'UVU Alumni Impact Award', 'janesmall.png'), ('linder', 'Richard J. and Marla A. Linder', 'UVU Honorary Alumni Award', 'richardsmall.png'),
       ('heather-kahlert', 'Heather Kahlert ’04', 'University Partner Award', 'heathersmall.png'), ('robert-bastian', 'Robert A. Bastian ’12', 'UVU Distinguished Alumni Award', 'robertsmall.png'),
       ('sheldon-smith', 'Sheldon R. Smith', 'Wilson W. Sorensen Lifetime Achievement Award', 'sheldonsmall.png')]
rech = '\n'.join(f'''                  <li class="al-person">
                     <img src="assets/awards-{k}.jpg" data-cms-src="/alumni/images/{f}" alt="{n}" width="353" height="358">
                     <h3>{n}</h3>
                     <p>{w}</p>
                  </li>''' for k, n, w, f in rec)
NOM = '#'
aw = hero(1, 'assets/alumni-awards-header.jpg', '/alumni/images/2026header.png', 'Alumni Awards', eyebrow='UVU', button=('Nominate Someone', NOM))
aw += split(2, text('Honoring Those Who Move Us Forward',
                    'Every year as part of the Homecoming celebration, we honor those who have made a difference at Utah Valley University and in our community.',
                    after=f'''
               <h4>Award Categories</h4>
{catsh}
               {actions(btn('Nominate Someone', NOM))}
               <p class="al-meta">{todo("LINK NEEDED: nomination form URL")}</p>'''),
            frame('assets/alumni-awards-honoring.png', '/alumni/images/group68.png', '2026 Alumni Awards honoree holding their award beside the emcee'),
            note='The XD hover component “Award categories” becomes an accordion: one per award. The nomination button follows the categories so people read what they can nominate for first.')
aw += one(3, head('2026 Alumni Awards Recipients', lead=False) + f'''
               <ul class="al-grid al-grid--5 al-grid--people">
{rech}
               </ul>''', cls='al-section--warm', note='Person cards (al-person). Same as SAA.')
aw += split(4, text('A Tradition Years in the Making',
                    'From this year’s celebration to decades of honorees before them, explore the Wolverines who’ve shaped UVU’s story.',
                    after=f'''
               <ul class="al-linklist">
                  <li>{xlink('See 2026 Event Photos', 'https://uvuphoto.exposure.co/uvu-honors-2026-alumni-awards-recipients', ic=icon('photography'))}</li>
                  <li>{xlink('Watch Award Videos on YouTube', 'https://www.youtube.com/playlist', ic=icon('video'))}</li>
                  <li>{xlink('Read About the 2026 Recipients', 'https://www.uvu.edu/news/2025/uvu-honors-alumni-award-winners-2026.html', ic=icon('award'))}</li>
                  <li>{xlink('See Past Recipients', 'https://www.uvu.edu/alumni/about/past-alumni-awards-recipients.html', ic=icon('calendar'))}</li>
               </ul>
               <p class="al-meta">{todo("LINK NEEDED: full YouTube playlist URL")}</p>'''),
            frame('assets/alumni-awards-tradition.png', '/alumni/images/group69.png', 'Alumni Awards honoree smiling with their award at the 2025 ceremony', portrait=True), reverse=True)
aw += contact(5)
P['alumni-awards'] = ('Alumni Awards', 'UVU Alumni Awards honor those who have made a difference at Utah Valley University and in our community.', 'https://www.uvu.edu/alumni/about/alumni-awards.html', aw)

for slug, (title, desc, url, main) in P.items():
    open(f'{OUT}/{slug}/index.html', 'w').write(page(slug, title, desc, url, main))
    print('wrote', slug)
