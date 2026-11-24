#!/usr/bin/env python3
"""Alumni Web System v1.1: new pages (Board, Diplomas, Career, Aviation, Job Shadow)."""
import os, html as H
from build2 import OUT, page, flag, todo, icon, btn, actions, frame, one, split, head, text, contact, _sec, hero, xlink, is_ext, _V

LIVE = 'https://www.uvu.edu'


def img_src(slug, cms_path, local_name=None):
    """Local asset if it has been saved into the page's assets folder, else the live URL."""
    name = local_name or os.path.basename(cms_path)
    if os.path.exists(f'{OUT}/{slug}/assets/{name}'):
        return f'assets/{name}'
    return LIVE + cms_path


def hero_plain(n, title, lead=None, button=None, note='', eyebrow=None):
    _V[0] = 0
    if eyebrow:
        title = f'<span class="al-eyebrow">{eyebrow}</span> {title}'
    lp = f'\n            <p class="al-hero-lead">{lead}</p>' if lead else ''
    bt = f'\n            {actions(btn(button[0], button[1], "light"))}' if button else ''
    return f'''
<!-- SECTION {n} · template: header-fullbleed (compact: no hero photo){(" · " + note) if note else ""} -->
<section class="page-header jumbo fullbleed al-hero al-hero--plain" data-uvu-template="header-fullbleed" data-uvu-section="{n}">
   <div class="container-fluid">
      <header class="fullbleed-overlay contain text-invert">
            <h1>{title}</h1>{lp}{bt}
      </header>
   </div>
</section>'''


def hero_live(n, slug, cms, title, lead=None, button=None):
    src = img_src(slug, cms)
    lp = f'\n            <p class="al-hero-lead">{lead}</p>' if lead else ''
    bt = f'\n            {actions(btn(button[0], button[1], "light"))}' if button else ''
    return f'''
<!-- SECTION {n} · template: header-fullbleed · live photo with CSS scrim (al-hero--scrim) until it is re-cut to the 1920x700 hero spec. CMS: {cms} -->
<section class="page-header jumbo fullbleed container-narrow al-hero al-hero--scrim" style="background-image: url({src});" data-cms-bg="{cms}" data-uvu-template="header-fullbleed" data-uvu-section="{n}">
   <div class="container-fluid">
      <header class="fullbleed-overlay contain text-invert">
            <h1>{title}</h1>{lp}{bt}
      </header>
   </div>
</section>'''


def notice(txt, ic='info-1'):
    return f'<div class="al-notice">{icon(ic)}<p>{txt}</p></div>'


P = {}

# ======================================================================
# ALUMNI ASSOCIATION BOARD OF DIRECTORS
# ======================================================================
SLUG = 'alumni-board'
BIMG = '/alumni/about/images/alumni-association-advisory-board/'
board = [
    ('2025-26/jared-finch.png', 'Jared Finch ’01', 'Board President', 'Senior Global Sales Executive, Morris Meetings &amp; Incentives'),
    ('2025-26/matthew-bryson.png', 'Matt Bryson ’17', 'Board Vice President', 'Head of Product and Engineering, Velvet'),
    ('2025-26/mikelle_blackner_2.png', 'Mikelle Blackner ’03', '', 'Educator'),
    ('2025-26/brandon-davies.png', 'Brandon Davies ’15', '', 'Senior Associate Analytical Chemist, Rhyz Labs'),
    ('2025-26/madison-heywood.png', 'Maddie Heywood ’20', '', 'Senior Events Coordinator, Cardone Ventures'),
    ('2025-26/megan-johnson.png', 'Megan Johnson ’08', '', 'President, Spanish Fork Hospital'),
    ('2025-26/andre-jones.png', 'Andre Jones ’18', '', 'Alumni in Residence, DC Wolverines'),
    ('skyler-payne.jpg', flag('Skyler Payne ’19 and ’23, FPA', 'Live: “Skyler Payne ’19 FPA ’23.” Reformatted to the UVU A–Z citation for two degrees. Note: the UVU style guide’s own example lists Skyler Payne as ’18, Personal Financial Planning. Confirm the year.'), '', 'Private Banker, J.P. Morgan'),
    ('2025-26/ben-perkins.png', 'Ben Perkins ’19', '', 'Founder, &amp;Collar'),
    ('2025-26/jordan-perry.png', flag('Jordan Perry', 'No class year on the live page. Confirm whether Jordan is an alum (add the year) or a community member.'), '', flag('Assistant Vice President of Digital Marketing, UCCU', 'Live: “AVP of Digital Marketing.” Spelled out to match the other titles.')),
    ('2025-26/cassidy-read.png', 'Cassidy Read ’13', '', 'Senior Vice President, Goldman Sachs'),
    ('ryan-teeples.jpg', 'Ryan Teeples ’05', '', 'Enterprise Technology and AI Strategy Leader'),
]


def person(path, name, role, meta):
    plain = H.unescape(name.split('>')[1].split('<')[0] if '<' in name else name)
    alt = plain.split(' ’')[0]
    rl = f'<span class="al-person-role">{role}</span>' if role else ''
    return f'''                  <li class="al-person">
                     <img src="{img_src(SLUG, BIMG + path, os.path.basename(path))}" data-cms-src="{BIMG + path}" alt="{alt}" width="400" height="600" loading="lazy">
                     <h3>{name}</h3>
                     <p>{rl}{meta}</p>
                  </li>'''


expect = ['Attend three board meetings per year and participate in task forces, events, and functions as requested.',
          'Review agenda and supporting materials prior to board meetings.',
          'Be familiar with the programs and activities sponsored, organized, and coordinated by the Office of Alumni Relations.',
          'Understand and help contribute to reaching the UVU Alumni goals around engagement and impact.',
          'Make an annual financial contribution to the UVU Foundation.',
          'Volunteer for at least one UVU Alumni program per year to experience the impact of our collective effort and provide feedback and insights on what went well in addition to opportunities for improvement.']

past = [('2022–25', flag('Kara H. North', 'Live: “2022–2025.” Shortened to match every other entry.')), ('2019–22', 'Dru A. Huffaker'),
        ('2016–19', flag('—', 'Gap on the live list: nobody is listed for 2016–19.')),
        ('2013–16', flag('John R. Gappmayer', 'Live lists both Gappmayer and Blair for 2013–16 and nobody for 2016–19. Likely Gappmayer is 2016–19. Confirm.')),
        ('2013–16', 'Curtis B. Blair'), ('2011–13', 'Curtis J. Morley'), ('2009–11', 'T.J. Fund'), ('2008–09', 'J. Scott Jenkins'),
        ('2006–08', 'Thomas C. Powell'), ('2004–06', 'B.J. Wright'), ('2002–04', 'Tom Heal'), ('2000–02', 'Barbara A. Smith'),
        ('1997–2000', 'Dave F. Adams'), ('1995–97', 'Jeffery Kahn'), ('1994–95', 'Geri S. Clements'), ('1993–94', 'Bill A. Brown'),
        ('1992–93', 'Greg S. Nelson'), ('1991–92', 'David D. Halladay'), ('1990–91', 'Brent J. DeMille'), ('1989–90', 'John W. Startup')]

bd = hero_plain(1, flag('Board of Directors', 'Visual title; the H1 still reads “UVU Alumni Association Board of Directors” for search. Naming mismatch on the live page: the H1 says “Board of Directors,” but the browser title and URL say “Advisory Board.” Pick one name and match the title tag (and ideally the URL) to it.'),
                note='Live page uses header-default with no photo. Compact hero keeps the title on the system edge.', eyebrow='UVU Alumni Association')
bd += split(2, text(flag('About the Board', 'Placeholder heading. The live intro has no heading.'),
                    'The UVU Alumni Association (UVUAA) Board of Directors augments the knowledge, understanding, and strategic thinking of the Office of Alumni Relations team in order to help deliver exceptional results with exceptional care for the UVU Alumni Community.',
                    'Experienced board members can provide technical or specialist advice and extend the range of skills and understanding of team members. Board members serve as public advocates for UVU Alumni, support fundraising, and help expand the community of UVU supporters.'),
            f'''<article class="al-card">
                  <div class="al-card-tag">{icon('team', 'white')}{flag('Member Expectations', 'Placeholder label. Live: “Members are expected to:” at the end of the intro.')}</div>
                  <div class="al-card-body">
                     <ul class="al-checklist">
{chr(10).join(f"                        <li>{e}</li>" for e in expect)}
                     </ul>
                  </div>
                  <div class="al-card-foot">{notice('Requests to join are currently closed. Please check back later.')}</div>
               </article>''',
            note='Intro + expectations card. The card replaces the live bullet list so the six commitments scan as a checklist, and the “closed” status sits right under them.')
bd += one(3, head(flag('2025–26 Board of Directors', 'Live: “The Alumni Board of Directors.” Adding the term tells visitors the list is current and reminds editors to update it each year.'), lead=False) + f'''
               <ul class="al-grid al-grid--4 al-grid--people">
{chr(10).join(person(*m) for m in board)}
               </ul>''',
          cls='al-section--warm',
          note='Board grid. Officers first, then A–Z (live order). The live page hides every photo and title inside a closed accordion; cards show them at a glance. Alt text is the name only (live alt “photo of …” repeats what a screen reader already announces).')
bd += one(4, head('Past Presidents', lead=False) + f'''
               <ul class="al-roster">
{chr(10).join(f'                  <li><span class="al-roster-key">{y}</span><span>{n}</span></li>' for y, n in past)}
               </ul>''',
          note='Past presidents, most recent first. Live keeps this inside an accordion; 20 short rows read fine open.')
bd += contact(5)
P[SLUG] = ('Alumni Association Board of Directors', 'The UVU Alumni Association Board of Directors: members, expectations, and past presidents.',
           'https://www.uvu.edu/alumni/about/alumni-association-advisory-board.html', bd)


def card(ic, h3, body, act_label, act_href, ext=None):
    return f"""                  <li><article class="al-card">
                     <div class="al-card-body">{icon(ic, cls='al-card-icon')}
                        <h3>{h3}</h3>
                        <p>{body}</p>
                     </div>
                     <div class="al-card-action">{xlink(act_label, act_href)}</div>
                  </article></li>"""


# ======================================================================
# DIPLOMAS
# ======================================================================
SLUG = 'alumni-diplomas'
MS = 'https://www.michaelsutter.com/uvu'
dp = hero(1, 'assets/alumni-diplomas-header.jpg', '/alumni/resources/images/diploma-header.jpg', 'Diplomas', eyebrow='UVU', button=('Order a Reissued Diploma', MS),
          note=flag('$25 through michaelsutter.com, UVU’s diploma printer.', 'New microcopy: price and where the order happens, before the click. Confirm “diploma printer” wording.'))
dp += one(2, head('Your School. Your Diploma.',
                  f'Each UVU graduate is issued one free paper copy of their UVU diploma at the end of their graduating semester. Students who graduated after {flag("fall 2019", "Live: “Fall 2019.” UVU style: seasons are lowercase.")} are also given one free digital copy.'),
          note='Intro statement.')
dp += one(3, f"""               <ul class="al-grid al-grid--3">
{card('diploma-1', 'Reissuing Diplomas', f'Whether you graduated from CUVS, UTTI, UTC, UVCC, UVSC, or UVU with a certificate, associate, {flag("bachelor’s", "Live: “bachelors.” Possessive per AP.")}, or master’s degree, you are eligible to purchase a reissued UVU diploma ($25) to display in your home or office.', 'Order a Reissued Diploma', MS)}
{card('graduation', flag('Check on a Recent Diploma', 'Placeholder heading. Merges the live intro’s status line with the “Any Questions?” section, which repeated the same contact.'), f'If you have recently graduated and would like to check on the status of your diploma, contact the Graduation Office at {flag("801-863-8438", "Phone format: this page uses hyphens, the alumni contact band uses periods (801.863.8179). Pick one sitewide.")}.', 'Email the Graduation Office', 'mailto:graduation@uvu.edu?subject=Diploma%20Question', False)}
{card('paper', flag('Need Proof of Graduation?', 'Placeholder heading for the live transcript note.'), 'Please note that UVU considers UVU transcripts (not diplomas) as official documentation of graduation. If you need proof of graduation for a job or other purpose, you may want to ask if an official UVU transcript would suffice.', flag('Request an Official Transcript ($5)', 'Live: “Information on how to request an official transcript ($5) can be viewed at uvu.edu/registration.” Now the card’s action.'), 'https://www.uvu.edu/registration/', False)}
               </ul>""", cls='al-section--warm', note='Three tasks, three cards: order a reissue, check a recent diploma, prove graduation. Replaces four stacked text blocks.')
dp += split(4, text('For Whatever Comes Next',
                    'The Office of Alumni Relations is here to support you after graduation. Contact us with questions, updates or to learn more about alumni resources and opportunities.',
                    after=f'''
               <ul class="al-linklist">
                  <li>{xlink('Email: alumni@uvu.edu', 'mailto:alumni@uvu.edu', ic=icon('envelope-1'))}</li>
                  <li>{xlink('Phone: 801.863.8179', 'tel:+18018638179', ic=icon('cell'))}</li>
               </ul>'''),
            frame('assets/alumni-relations-team.jpg', '/alumni/resources/images/alumni-relations-team.jpg', 'UVU Alumni Relations team in green shirts doing the UVU hand sign'),
            note='Alumni Relations team photo with the original “For Whatever Comes Next” copy, so diploma questions that aren’t the Graduation Office’s have a face and a contact.')
dp += contact(5)
P[SLUG] = ('Diplomas', 'Order a reissued UVU diploma, check on a recent diploma, or request an official transcript.', 'https://www.uvu.edu/alumni/resources/diplomas.html', dp)

# ======================================================================
# CAREER AND NETWORKING RESOURCES
# ======================================================================
SLUG = 'career-networking-resources'
cr = hero(1, 'assets/career-resources-header.jpg', '/alumni/connect/images/resources-header.jpg', eyebrow='UVU Alumni', title=flag('Career and Networking Resources', 'Live: “Career &amp; Networking Resources.” AP: “and” outside logos and formal names.'),
               lead=flag('Hire a Wolverine. Help a Wolverine.', 'Live: an all-caps H2 with no body copy under it. Moved up to the hero as its lead line.'))
cr += one(2, f"""               <ul class="al-grid al-grid--3">
{card('human-resources', flag('Career and Internship Center', 'Live: “Career &amp; Internship Center (Guidance, Resources, Jobs).” The parenthetical repeats the description.'), 'UVU’s Career and Internship Center (CIC) promotes individual career success and employment potential for students and alumni through comprehensive career counseling services and by fostering community, regional, and national employer relationships.', 'Find CIC Resources for Alumni', 'https://www.uvu.edu/career-internship/alumni/index.html', False)}
{card('university', 'Jobs at UVU', 'UVU’s employment site allows you to search and apply for positions (full/part-time staff, faculty/adjunct, student, temporary) at UVU (main or satellite campuses).', 'Search UVU Jobs', 'https://www.uvu.edu/peopleandculture/jobs/index.html', False)}
{card('connection', 'UVU Alumni on LinkedIn', 'Build your professional community by connecting with UVU alumni and current students.', 'Join the UVU Alumni LinkedIn Group', 'https://www.linkedin.com/groups/61904')}
{card('writing', 'Writing Center', 'The Writing Center is available for all UVU alumni to use. You can register for an online or on-campus appointment for Graduate Writing Center or Main Center services.', 'Make an Appointment', 'https://uvu.mywconline.com/')}
{card('business', 'Small Business Development Center (SBDC)', 'Get a free one-on-one business consultation that is customized to your business and goals.', 'Get Business Advice', 'https://www.uvu.edu/sbdc/', False)}
{card('team', flag('Alumni Chapters and Communities', 'Live: “Alumni Chapters &amp; Communities.”'), 'Some of UVU’s programs have dedicated alumni chapters or communities like the <a href="../aviation-alumni-chapter/index.html">Aviation program</a>. See if your major has one, then learn how to get involved.', 'Find Your Chapter', 'https://www.uvu.edu/alumni/connect/chapters.html', False)}
               </ul>""", cls='al-section--warm',
          note='Six resources as one card grid (was two three-col rows with all-caps buttons). Ordered career first: CIC, jobs, LinkedIn, then skills and business, then chapters. Buttons become one text action per card.')
cr += contact(3)
P[SLUG] = ('Career and Networking Resources', 'Career, job, and networking resources for UVU alumni: the Career and Internship Center, UVU jobs, LinkedIn, the Writing Center, and more.', 'https://www.uvu.edu/alumni/connect/career-networking-resources.html', cr)

# ======================================================================
# AVIATION ALUMNI CHAPTER
# ======================================================================
SLUG = 'aviation-alumni-chapter'
past_ev = [('June 5, 2026', 'UVU Aviation Alumni and Student Networking Lunch', 'Noon–1:30 pm · Provo Airport Campus'),
           ('Oct. 3, 2025', 'UVU Alumni Aviation Chapter Meetup', 'Noon–1:30 pm · Provo Airport Campus'),
           ('June 20, 2025', 'UVU Alumni Aviation Chapter Luncheon', 'Noon–2 pm · Provo Airport Campus'),
           ('Oct. 1, 2024', 'UVU Alumni Aviation Chapter Fall Panel', 'Noon–2 pm · Provo Airport Campus'),
           ('Oct. 6, 2023', 'UVU Alumni Aviation Chapter Fall Networking Luncheon', 'Noon–2 pm · Provo Airport Campus, UVU Hangar Lobby'),
           ('Sept. 30, 2022', 'UVU Alumni Aviation Network Fall Luncheon', '11 am–1 pm · UVU Hangar Classroom HB 203'),
           ('April 26, 2022', 'UVU Alumni and Student Meet and Greet', '10 am–2 pm · Provo Airport Campus, UVU Hangar Lobby'),
           ('March 18, 2021', 'UVU LEAD Aviation Outreach Virtual Discussion With Decker Gaulke: “Professionalism in the Field of Aviation”', '4 pm · Virtual, Microsoft Teams'),
           ('Feb. 18, 2021', 'UVU LEAD Aviation Outreach Virtual Discussion With Jason Gobble: “A Pilot’s Perspective of the FAA Part 121 Training”', '7–8 pm · Virtual, Microsoft Teams'),
           ('Jan. 18, 2021', 'UVU LEAD Aviation Outreach Virtual Discussion With Devin Broadbent: “Take Off Into the 2020 Year With a Pilot’s Perspective”', '6 pm · Virtual, Microsoft Teams'),
           ('Dec. 4–5, 2020', 'UVU Alumni and Student Winter Meet and Greet', '10 am–2 pm · Provo Airport Campus, UVU Hangar Lobby'),
           ('Aug. 16, 2019', 'UVU Alumni Aviation Networking Luncheon', '1–2 pm · Provo Airport Campus, UVU Hangar A')]
pev = '\n'.join(f'                  <li><p class="al-meta">{d}</p><div><h3>{t}</h3><p class="al-meta">{m}</p></div></li>' for d, t, m in past_ev)
av = hero(1, 'assets/aviation-chapter-header.jpg', '/alumni/connect/images/aviation-network.jpg', 'Aviation Alumni Chapter', eyebrow='UVU')
av += one(2, head('Upcoming Chapter Events', lead=False) + f"""
               <div class="al-narrow">
                  {notice(flag('Check back soon for the next chapter event.', 'Placeholder empty state. The live “upcoming” event (June 5, 2026) has passed, so it moved to Past Chapter Events.'), 'calendar')}
                  <p class="al-meta">{todo("ADD NEXT EVENT. Format: date badge + title + time and place + RSVP button (see the styleguide).")}</p>
               </div>""", note='Upcoming events. Empty state until the next event is posted.')
av += one(3, f"""               <ul class="al-grid al-grid--2">
                  <li><article class="al-card">
                     <div class="al-card-body">{icon('team', cls='al-card-icon')}
                        <h3>Alumni Chapter Board</h3>
                        <p>The network volunteer board is comprised of graduates from the UVU School of Aviation. Volunteers give their time to assist with event planning, communications with alumni, and the mentor program.</p>
                        <ul class="al-roster">
                           <li><span class="al-roster-key">President</span><span>Doug Browne ’13</span></li>
                           <li><span class="al-roster-key">Vice President</span><span>Doug Johnsen ’15</span></li>
                           <li><span class="al-roster-key">Vice President</span><span>Devin Broadbent ’13</span></li>
                        </ul>
                     </div>
                     <div class="al-card-action"><a href="https://www.uvu.edu/directory/message/">{flag('Volunteer: Contact Amie Huntsman', 'Live: “If you would like to volunteer, please contact Amie Huntsman.” LINK: copy the full directory message URL from the live page.')}</a></div>
                  </article></li>
                  <li><article class="al-card">
                     <div class="al-card-body">{icon('aviation', cls='al-card-icon')}
                        <h3>Alumni Chapter Mentor Program</h3>
                        <p>The UVU School of Aviation Alumni Chapter has been compiling a robust list of alumni mentors since 2019. If you would like to be added to this list or would like any further information regarding the program, please email Doug Johnsen.</p>
                     </div>
                     <div class="al-card-action"><a href="mailto:douglas.f.johnsen@gmail.com">{flag('Email Doug Johnsen', 'Live link points to a personal Gmail address (and has a stray space: mailto:%20douglas…). Consider routing through alumni@uvu.edu or a UVU address.')}</a></div>
                  </article></li>
               </ul>
               <div class="al-narrow"><ul class="al-linklist"><li>{xlink(flag('Shop UVU Aviation Gear', 'Live: “UVU Aviation Shop Wolverine Online Store.”'), 'https://shopwolverine.com/collections/aviation', ic=icon('aviation'))}</li></ul></div>""",
          cls='al-section--warm', note='Get involved: the board and the mentor program as two cards. The shop link drops to a single link row.')
av += one(4, head(flag('Past Chapter Events', 'Dates and times normalized to AP and UVU style (Oct. 3, 2025 · noon–1:30 pm). “Hanger” → “Hangar” throughout. Live listed summer events in MST; time zones dropped since every event is local or virtual. “&amp;” → “and.”'), lead=False) + f"""
               <ul class="al-events al-events--compact al-narrow">
{pev}
               </ul>""", note='Past events as a compact archive, newest first.')
av += contact(5)
P[SLUG] = ('Aviation Alumni Chapter', 'The UVU Aviation Alumni Chapter: chapter events, the volunteer board, and the alumni mentor program.', 'https://www.uvu.edu/alumni/connect/aviation-alumni-chapter.html', av)

# ======================================================================
# JOB SHADOW
# ======================================================================
SLUG = 'alumni-job-shadow'
VI = '/alumni/volunteer/images/'


def quotes(items):
    return '<ul class="al-quotes">' + ''.join(f'<li><figure class="al-quote"><blockquote><p>“{q}”</p></blockquote><figcaption>{w}</figcaption></figure></li>' for q, w in items) + '</ul>'


q24 = [('My match was perfect, and I learned a great deal, not only about my specific field but about the criminal justice field in general. My favorite takeaway was learning about the disposition of evidence and the policies surrounding it.', 'Student'),
       ('This was my best hosting experience yet. The student was very eager and curious about my position, industry and work. They came prepared with great questions for me that I could tell they are really seeking information and guidance/mentorship in my industry.', 'Alum'),
       ('Even though I came into this not really prepared with what I wanted, Jared was very helpful in giving me both insight and feedback from the questions that I asked. And, it was nice to know that there really are other people besides friends and family who want me to succeed.', 'Student'),
       ('I really enjoyed the student that I was matched with! I appreciated that she was studying the field I work in (last year, none of the students I was matched with were studying my field — just somewhat related fields). We actually ended up hiring this student as one of our interns because the job shadow was such a good experience! I am grateful I got to meet her in that setting.', 'Alum')]
q23 = [('The student was very professional and presentable. It was wonderful connecting with a new Wolverine, and I’m grateful to give back to the next generation!', 'Alum'),
       ('The alum was very open and welcoming. Her willingness to share the details of the day-to-day activities of her career really helped me clarify whether fieldwork is something I want to go into. I really appreciate her sharing her time, experience, and knowledge.', 'Student'),
       ('It was an honor and a pleasure to contribute to the education of science students by showing them practical scientific applications of composting at a university level. If I can ever be shadowed by any other students, I would be happy to do so.', 'Alum'),
       ('This experience was amazing, and he spent the time really helping me understand what I wanted to do in the future and how to make that possible with my future career.', 'Student'),
       ('I thought it went well! This is my second year doing it and I love it.', 'Alum'),
       ('I got to experience what a day in the life of a software developer is like and I really enjoyed it. It made me excited to enter the field.', 'Student')]
q22 = [('I had such a great experience. My alum was awesome to work with and really catered the experience to me and what I’m interested in, and introduced me to a lot of people who were also really kind to answer questions I had.', 'Student'),
       (f'I thought the experience was great! The student is a talented kid, willing to listen and learn. I feel like I was able to give him great information on the banking / lending / finance industry {flag("the has", "Likely typo in the original quote (“that has”). Fix only with the alum’s OK.")} real world applicability. I look forward to staying in touch with the student. I also look forward to other job shadow opportunities with UVU students. I think it could also be a mutually beneficial relationship for future employment opportunities. Thanks for the experience.', flag('Alum, Commercial Banking', 'Live: “Alum in the Finance/Banking - Commercial Banking Industry.”')),
       ('I had a wonderful experience shadowing my alum. I got to witness a session with a client, and then she showed me what the behind-the-scenes of a clinical therapist’s job looks like. She was able to help answer my questions about grad school, licensing, and private practice, as well as give me insight into what the life of a therapist is like. I have only positive things to say about the program.', 'Student'),
       (f'Was a great experience. She asked great questions and we both felt like it was productive and a good meeting to have. She asked about what she could do to prepare for the workforce and we talked about what the workload was like. I learned more about what UVU is doing to prepare students for the career I’m in and what to look for when interviewing these students who are {flag("working for work", "Likely typo in the original quote (“looking for work”). Fix only with the alum’s OK.")}.', flag('Alum, Software', 'Live: “Alum in the Technology - Software Industry.”'))]


def year(y, img, alt, paras, qs, opened=False, credit='', wh=(945, 532)):
    src = img_src(SLUG, VI + img, os.path.basename(img))
    cr_ = f'<p class="al-meta">{credit}</p>' if credit else ''
    ps_ = ''.join(f'<p>{p}</p>' for p in paras)
    return f"""                  <details class="al-accordion accordion-unstyled"{' open' if opened else ''}><summary>{y}</summary><div class="al-accordion-body">
                     <img class="al-photo" src="{src}" data-cms-src="{VI + img}" alt="{alt}" width="{wh[0]}" height="{wh[1]}" loading="lazy">{cr_}
                     {ps_}
                     <h3>{flag('Hear About the Experience', 'Unified: 2023 used “Read Participants’ Testimonials.”') if y == '2023' else 'Hear About the Experience'}</h3>
                     {quotes(qs)}
                  </div></details>"""


js = hero(1, 'assets/job-shadow-header.jpg', '/alumni/volunteer/images/job-shadow-header.jpg', 'Job Shadow Program', eyebrow='UVU Alumni', lead=f'The Utah Valley University Alumni Job Shadow Program is an opportunity for students to spend part of their day ({flag("in person", "Live: “in-person.” AP: no hyphen as an adverb.")} or virtually) with UVU alumni working in careers they are interested in pursuing after graduation.',
                note='Live page uses header-default plus a 945px icon-banner image; the banner is retired for the compact hero.')
js += split(2, f"""               <h2>Why Participate</h2>
               <h3>Alumni</h3>
               <p>This is an opportunity for you to host students at your organization for a day (in person or virtually) to provide industry and career insights. Giving your time by volunteering can make a real and positive impact on a student!</p>
               <h3>Students</h3>
               <p>This is your chance to get real-world experience, explore a field of interest, and build your network in a professional environment with a UVU alum!</p>
               {notice(flag('Applications are now closed. Still want to connect with fellow alumni or help students navigate their career journey? Stay tuned to <a href="https://www.uvu.edu/alumni/">uvu.edu/alumni</a> and our <a href="https://www.instagram.com/uvualumni/">social media</a> to learn about other ways to stay involved with UVU.', 'Live repeats a closed notice under both Alumni and Students; merged into one. “involved to UVU” → “involved with UVU.”'))}
               <p class="al-meta">{todo("STATUS: is the program running in 2026? The latest recap is 2024.")}</p>
               <p class="al-meta">For questions about the UVU Alumni Job Shadow Program, contact <a href="https://www.uvu.edu/directory/message/">Tiffany Sheth</a>, assistant director of strategic projects, UVU Office of Alumni Relations. {todo("LINK: full directory message URL")}</p>""",
            f"""<!-- CMS: keep the YouTube embed (ZTJjEBV7IBk). Placeholder thumbnail for the mockup. -->
               <a class="al-video" href="https://www.youtube.com/watch?v=ZTJjEBV7IBk" target="_blank" rel="noopener"><img src="assets/job-shadow-video-placeholder.jpg" alt="Watch on YouTube: why participate in the UVU Alumni Job Shadow Program (opens in a new tab)" width="1280" height="720"></a>""",
            note='Why participate: alumni and student pitches side by side with the video (live stacks three all-caps sections).')
js += one(3, head('See Feedback From Past Years', lead=False) + f"""
               <div class="al-narrow">
{year('2024', 'makenna-k.jpg', 'A male alum and a female student meet virtually.', [todo('PHOTO: live image is a Teams screenshot with the Windows taskbar and clock in frame. Mockup crops the taskbar out; upload the cropped version or a real photo.') + ' ' + flag('The 2024 Job Shadow Program', 'Live: “This year’s Job Shadow Program,” which goes stale.') + ' matched over 100 participants, facilitating numerous valuable connections. Students and alumni from diverse industries from animation to finance reflect the program’s broad reach. While many pairs met in person, others connected virtually, maximizing accessibility. A heartfelt thank you to all who participated in making this program a success!'], q24, opened=True, wh=(900, 474))}
{year('2023', 'job-shadow/job-shadow-2023.jpg', 'Four images from the 2023 Job Shadow Program: two mentor pairs, an airplane fan, and compost.', ['In its second year, the Utah Valley University (UVU) Alumni Job Shadow Program continued to exemplify engaged learning by providing alumni and students the opportunity to connect for career exploration. The program allowed many UVU students to receive industry and career insights from UVU alumni working in their fields of interest.', 'Throughout the month of January, alumni met with students in person or virtually. All were invited to participate, including alumni who live outside of Utah. In fact, alumni across 10 states and 23 industries were represented! A couple of students were even offered a job or internship after participating.'], q23)}
{year('2022', 'job-shadow/job-shadow-2022.png', 'Six images of UVU alumni and students at job shadow', [flag('Our first Job Shadow Program', 'Live: “Our first annual.” AP: an event isn’t annual until it has happened twice.') + ' was a success! With over 200 participants, we matched many students and alumni together to create a meaningful and hands-on experience. Alumni from 28 industries offered their time and experience to over 100 students. Because the program was offered in person as well as virtually, we had alumni participants from 11 states and 2 countries: the US and Jordan. One student was also offered an internship, and alumni let our team know about three more opportunities. Thank you to everyone who participated, and we hope to see you again next year!'], q22, wh=(945, 475), credit='Photos courtesy of Rachel Waters, Skyler Stratford, David Dekker, Mehmet Monis, Krista Winward, and Jill St. Clair.')}
               </div>""", cls='al-section--warm',
          note='Recaps by year. Newest open by default. Attribution labels unified to “Alum” and “Student.” 2022 photo thanks becomes a credit line. “Look below to read…” dropped (the quotes are right there).')
js += contact(4)
P[SLUG] = ('Alumni Job Shadow Program', 'The UVU Alumni Job Shadow Program pairs students with UVU alumni for a day of career exploration, in person or virtually.', 'https://www.uvu.edu/alumni/volunteer/job-shadow.html', js)


# ======================================================================
# FOREVER WOLVERINES PODCAST
# ======================================================================
SLUG = 'forever-wolverines-podcast'
SPOT = 'https://open.spotify.com/show/0jjnDHtCAWyyTIzDSZYxHp'
plats = [('Spotify', SPOT), ('Apple Podcasts', 'https://podcasts.apple.com/us/podcast/forever-wolverines-podcast/id1791808457'),
         ('Amazon Music', 'https://music.amazon.com/podcasts/0e51ddaf-2ed6-412e-b865-b8e94aab1348/forever-wolverines-podcast'),
         ('iHeartRadio', 'https://www.iheart.com/podcast/269-forever-wolverines-podcast-255472967/'),
         ('Goodpods', 'https://goodpods.com/podcasts/forever-wolverines-podcast-623597'), ('Castbox', 'https://castbox.fm/channel/id6417318')]
chips = ''.join(f'<li>{xlink(n, u)}</li>' for n, u in plats)
from episodes import EP, IMG, latest_feature


def ep_card(e):
    i, guest, tag, date, mins, host, h = e
    hl = f'\n                        <p class="al-episode-host">Hosted by {host}</p>' if host else ''
    return f"""                  <li class="al-episode">
                     <div class="al-episode-media"><img src="{IMG}{h}" data-cms-src="/alumni/connect/images/podcast/{i}.jpg" alt="" width="1280" height="719" loading="lazy"></div>
                     <div class="al-episode-body">
                        <p class="al-episode-meta">{date} · {mins} min</p>
                        <h4><a href="https://open.spotify.com/episode/{i}" target="_blank" rel="noopener">{guest}<span class="sr-only-al"> (opens Spotify in a new tab)</span></a></h4>
                        <p class="al-episode-tag">{tag}</p>{hl}
                     </div>
                  </li>"""


years = {}
for e in EP:
    years.setdefault(e[3][-4:], []).append(e)
grid = ''.join(f"""
               <h3 class="al-episodes-year">{y}</h3>
               <ul class="al-episodes">
{chr(10).join(ep_card(e) for e in eps)}
               </ul>""" for y, eps in years.items())
EMBED = """<div class="al-embed"><img class="al-embed-poster" src="https://i.scdn.co/image/ab6772ab000030ae35c0bd5bcfc91a07732ef3c9" alt="" width="1280" height="719"><iframe src="https://open.spotify.com/embed/show/0jjnDHtCAWyyTIzDSZYxHp/video?utm_source=generator" title="Forever Wolverines Podcast: newest episode on Spotify" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe></div>"""
pc = hero(1, 'assets/podcast-header.jpg', '/alumni/connect/images/podcast-header.jpg', 'Forever Wolverines Podcast', button=('Listen on Spotify', SPOT))
pc += split(2, text(flag('About the Show', 'Placeholder heading. The live page has none.'),
                    'The Forever Wolverines podcast is created and produced by the UVU Student Alumni Ambassadors. Each ambassador selects an alum and meets with them on air. They ask questions about the alum’s career, time at school, advice, and more.',
                    flag('New episodes drop every other week.', 'Live: “Forever Wolverines podcast has episodes drop every other week.” Grammar.'),
                    after=f"""
               <h3>Listen On</h3>
               <ul class="al-chips">{chips}</ul>
               <ul class="al-linklist">
                  <li><a href="../about-saa/index.html" data-cms-href="/alumni/students/about-saa.html">{icon('communicate')}Meet the Student Alumni Ambassadors</a></li>
               </ul>"""),
            latest_feature(),
            note='Latest episode as a linked photo (guest and host on set). The Spotify show embed was cut: its player shows the show artwork, which is the logo. Update with each new episode (copy the top card’s ID, thumbnail, and text).')
pc += one(3, head('All Episodes', lead=False) + grid, cls='al-section--warm',
          note=f'Every episode, newest first, grouped by year. Thumbnails are the Spotify episode covers (guest and host on set), linked from Spotify’s image CDN in this mockup; for production, save each to /alumni/connect/images/podcast/[episode id].jpg (data-cms-src) or keep the CDN link. New episode = copy the top card. {len(EP)} episodes as of Oct. 13, 2026.')
pc += contact(4)
P[SLUG] = ('Forever Wolverines Podcast', 'The Forever Wolverines podcast: UVU Student Alumni Ambassadors interview UVU alumni about careers, campus, and advice. New episodes every other week.',
           'https://www.uvu.edu/alumni/connect/forever-wolverines-podcast.html', pc)

if __name__ == '__main__':
    import sys
    only = sys.argv[1:] or list(P)
    for slug in only:
        title, desc, url, main = P[slug]
        os.makedirs(f'{OUT}/{slug}/assets', exist_ok=True)
        open(f'{OUT}/{slug}/index.html', 'w').write(page(slug, title, desc, url, main))
        print('wrote', slug)
