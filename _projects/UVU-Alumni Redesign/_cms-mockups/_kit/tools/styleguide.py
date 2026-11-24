import os, sys, glob
sys.path.insert(0, '/tmp/xr')
from build2 import *

OUTDIR = f'{OUT}/_styleguide'
os.makedirs(OUTDIR, exist_ok=True)

SW = [('UVU Green', '#185C33', 'Primary. Headings, buttons, icons, links.', '#fff'),
      ('Dark Green', '#1A321C', 'IA. Body text, button hover.', '#fff'),
      ('Wolverine Green', '#008A40', 'Secondary. Sparingly.', '#fff'),
      ('Warm', '#F2F0EB', 'Alternate section background.', '#1A321C'),
      ('Pale Meadow', '#C5D97A', 'Accent. Hero eyebrow, focus ring, footer headings.', '#1A321C'),
      ('Sea Haze', '#C4D6C1', 'Accent. Rules on green.', '#1A321C'),
      ('White', '#FFFFFF', 'Background, text on green.', '#1A321C')]
sw = ''.join(f'<li style="list-style:none"><div style="height:96px;border-radius:12px;background:{h};border:1px solid rgba(26,50,28,.12)"></div><p style="margin:10px 0 0"><strong>{n}</strong><br><span class="al-meta">{h} · {d}</span></p></li>' for n, h, d, _ in SW)

TYPE = [('H1 · Hero', 'Rajdhani Bold 72 / 44 mobile · 1.02', '<span style="font-family:Rajdhani;font-weight:700;font-size:72px;line-height:1;color:#185C33">Show Your School Spirit</span>'),
        ('H2 · Section', 'Rajdhani Bold 46 / 34 · 1.1', '<span style="font-family:Rajdhani;font-weight:700;font-size:46px;line-height:1.1;color:#185C33">Once a Wolverine, Always a Wolverine</span>'),
        ('H3 · Card', 'Rajdhani Bold 26 / 23 · 1.2', '<span style="font-family:Rajdhani;font-weight:700;font-size:26px;color:#185C33">Future UVU Alumni Scholarship</span>'),
        ('H4 · Label', 'Rajdhani Bold 19 · 1.25', '<span style="font-family:Rajdhani;font-weight:700;font-size:19px;color:#185C33">Eligibility</span>'),
        ('Lead', 'Lato Regular 21 / 19 · 1.5', '<span style="font-size:21px;line-height:1.5">The Office of Alumni Relations helps our UVU alumni community thrive.</span>'),
        ('Body', 'Lato Regular 18 / 17 · 1.6 · max 62ch', '<span style="font-size:18px;line-height:1.6">Membership is free for all graduated alumni. Log into your alumni profile to access the benefits.</span>'),
        ('Meta', 'Lato Regular 15 · 1.5 · #4B5D50', '<span class="al-meta" style="font-size:15px">Sept. 1, 2026</span>'),
        ('Button', 'Rajdhani Bold 20 · Title Case · 52px tall', btn('Update Your Profile', '#', ext=False))]
ty = ''.join(f'<tr><td style="padding:18px 24px 18px 0;vertical-align:top;width:200px"><strong>{n}</strong><br><span class="al-meta">{s}</span></td><td style="padding:18px 0;border-bottom:1px solid rgba(26,50,28,.14)">{x}</td></tr>' for n, s, x in TYPE)

used = ['calendar', 'business', 'automotive', 'diploma-3', 'communicate', 'graduation', 'credit-cards', 'cash-1', 'award', 'student-life', 'photography', 'video', 'envelope-1', 'cell', 'ui-check', 'ui-arrow-right', 'ui-chevron-down', 'ui-external', 'ui-play']
ic = ''.join(f'<li style="list-style:none;text-align:center">{icon(n)}<br><span class="al-meta" style="font-size:13px">{n}</span></li>' for n in used)
alln = sorted(os.path.basename(f)[:-4] for f in glob.glob(f'{OUT}/_kit/icons/green/*.svg') if not os.path.basename(f).startswith(('ui-', 'social-')))
icall = ''.join(f'<li style="list-style:none;text-align:center"><img src="../_kit/icons/green/{n}.svg" alt="" width="40" height="40"><br><span style="font-size:11px;color:#4B5D50">{n}</span></li>' for n in alln)

FLAGS = [
    ('System', [
        ('Two greens on every page', 'The CMS styles headings and buttons in #275D38. UVU Green is #185C33. The hero overlays already use #185C33, so the live pages mix both. The system uses #185C33 only. Ask the web team to align the global value.'),
        ('LIVE BUG: hero H1 is green on green on phones', 'Confirmed on the live Benefits page at phone width: the title “UVU Alumni Benefits” renders in #275D38 on the green hero and is nearly invisible. Cause: production dept.css sets <code>.jumbo header h1 { color: #275D38 !important }</code> below 768px. Any alumni page using that hero is affected. Send to the web team now; the system already overrides it.'),
        ('Body line-height is 1.2', 'CMS default. Readable body copy needs about 1.5–1.6 (Apple HIG and WCAG reflow both point there). The system sets 1.6 and caps lines at 62 characters.'),
        ('12 paragraph styles, 6 H2 styles', 'Audit of the first mockups: 12 paragraph size/color combos and 6 H2 variants across seven pages. The system has 4 text roles (lead, body, meta, fine print) and one style per heading level.'),
        ('Buttons: 3 looks, 3 heights', 'Weights 400 and 700, sizes 18 and 22, heights 56/60/77 (77 was a wrapped label). Now: primary, secondary, light. All 52px tall (HIG minimum is 44), Title Case, arrow glyph.'),
        ('12 section spacings', 'Mixed 40/60/80 padding combos. Now one rhythm: 96px desktop, 64px mobile, and two white sections in a row share one gap.'),
        ('Three icon systems', 'Custom XD line icons, Font Awesome solid, and brand-colored social circles. Now: the UVU Icon Library only, plus five UI glyphs (check, arrow, chevron, external, play) drawn to its 2.5pt square-cap stroke. Social marks are one-color.'),
        ('Photo frames at ~6°, then 10.25°', 'The XD frames tilted about 6°. v1 re-cut them at the IA 10.25° with an offset outline, which read as a one-off gimmick next to uvu.edu. v1.2 adopts the university site’s image style: plain photos with rounded corners and APFY shapes (circles, half-discs, hatching, stairs, rings, x marks) layered around them in CSS, so editors upload ordinary photos.'),
        ('Zigzag fatigue', 'Benefits and Graduates alternated image/text 3–4 times in a row. Rule now: max two splits in a row, then a band (warm, photo, cards, or centered statement).'),
        ('Buttons that didn’t say where they go', '“I’m an Alum,” “Access Membership,” “Get Your Plates,” and “Click the button below” fail WCAG 2.4.4 (link purpose) and give no warning about logins or leaving UVU. Labels now name the destination; external links show a glyph and announce “opens in a new tab”; a note under the button flags a login, a fee, or another site.'),
        ('A contact band that repeated everything', 'The same tall photo band ended every page (about 850px desktop, 1,000px phone) with grad-specific copy. It’s now one compact alumni footer: section nav, contact, and social, with the current page marked. The alumni section finally has wayfinding.'),
        ('Edges didn’t line up', 'Heroes sat in a 992px container while sections used the full width, so headline and body text started at different x positions on every page. Now one container: 1280px max with a 40px gutter (24px on phones). Every hero headline, heading, and paragraph shares the same left edge.'),
        ('Phones were desktop, shrunk', 'The partner logos were one flat image (unreadable at 390px), person cards squeezed two-up with three-line labels, buttons wrapped awkwardly, and long centered paragraphs were hard to read. Phone rules now: full-width buttons, left-aligned text, logos as a list, person cards as rows, quick links as a list, news as a swipe row.'),
        ('Four buttons where one belongs', 'Graduates (Alumni 101 etc.) and Alumni Awards (photos, videos, recipients) used grids of solid buttons, so nothing was primary. They’re now link lists: one style for secondary actions sitewide.'),
    ]),
    ('Brand', [
        ('All-caps headings', 'Retired for Title Case per the UVU style guide. The university global nav stays uppercase (CMS chrome, out of scope).'),
        ('Athletics Wolverine mark in the Benefits logo strip', 'The Wolverine head is an Athletics-only mark. If it stands in for “sporting events,” confirm Athletics approved it as a partner logo, or swap it for a text label.'),
        ('Stratum isn’t on the web', 'Rajdhani is the approved web fallback, so the system uses it. If UVU’s Adobe Fonts web kit can serve Stratum, it’s a one-variable swap (<code>--al-font-display</code>).'),
        ('Imagery skews current students', 'The photo set is almost all APFY student lifestyle. Fine for Grads, SAA, and Scholarships. Home, Benefits, and Alumni Awards need alumni-aged imagery: GOLD alumni at events, at work, with families. Worth a shoot request.'),
    ]),
    ('Content', [
        ('Duplicate and repeated headings', 'Scholarships repeated the H1 as its first H2 (placeholder swapped in). Graduates had two sections starting “Connect with…” (one shortened). Benefits repeated the hero button label in the first section.'),
        ('Stale and conflicting facts', 'License plate “New design coming July 1, 2026” has passed. SAA application dates are last cycle. SAA eligibility differs between the SAA and Scholarships pages.'),
        ('Missing pieces', 'Nomination form URL, full YouTube playlist URL, plate design graphic, and the alumni stories feed hookup on Home.'),
        ('Style fixes applied', 'AP/UVU: “11:59 pm,” lowercase seasons, “Aug. 15,” “and” for “&amp;” in running copy, comma in “Congratulations, Graduates,” typos (“opportinities,” “lifstyle,” “an Utah”). Each is highlighted in the copy-review PDFs.'),
    ]),
]
fl = ''
for grp, items in FLAGS:
    fl += f'<h3 style="margin-top:48px">{grp}</h3><ol class="al-steps">' + ''.join(f'<li><strong>{t}.</strong> {d}</li>' for t, d in items) + '</ol>'

main = hero(1, '../alumni-home/assets/alumni-home-header.jpg', '', 'Alumni Web System', lead='One system for every UVU Alumni page: type, color, icons, imagery, components, and the rules that hold them together.')
main += one(2, head('Principles', lead=False) + '''
               <div class="al-grid al-grid--3">
                  <article class="al-card"><div class="al-card-body"><h3>One of Everything</h3><p>One green, one heading style per level, one image style, one icon library, one primary button per section.</p></div></article>
                  <article class="al-card"><div class="al-card-body"><h3>CMS-Native</h3><p>Built on OU section templates and UVU's global CSS. One extra stylesheet. Editors type headings and paragraphs; the section class does the rest.</p></div></article>
                  <article class="al-card"><div class="al-card-body"><h3>Readable First</h3><p>Title Case headings, 1.6 line-height, 62-character lines, 52px tap targets, visible focus rings, AA contrast.</p></div></article>
               </div>''')
main += one(3, head('Color', 'UVU Green leads. Accents stay under 20% of any page.') + f'<ul class="al-grid al-grid--4" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">{sw}</ul>', cls='al-section--warm')
main += one(4, head('Type', 'Rajdhani (Stratum’s web fallback) for display. Lato for everything you read. Title Case for every heading and button.') + f'<table style="width:100%;border-collapse:collapse">{ty}</table>')
main += one(5, head('Buttons and Actions', 'One primary per section. Secondary for the second option. Light on photos and green.') +
            '<div class="al-actions" style="justify-content:center">' + btn('Primary', '#', ext=False) + btn('Secondary', '#', 'secondary', False) + btn('Leaves UVU', 'https://example.com', ext=True) + '</div>' +
            '<p class="al-meta" style="text-align:center;margin:16px auto 0">Labels say where the button goes (“See Your Alumni Benefits,” never “I’m an Alum” or “Click Here”). Arrow = stays on uvu.edu. External glyph = leaves UVU; those open in a new tab and carry hidden “(opens in a new tab)” text. When a login, a fee, or another site is on the other side, an <code>al-btn-note</code> line says so under the button. PDFs say “(PDF)” in the label.</p>' +
            '<div style="background:#185C33;border-radius:12px;padding:32px;margin-top:32px;text-align:center">' + btn('Light (on green or photo)', '#', 'light', False) + '</div>' +
            '<div style="max-width:560px;margin:48px auto 0"><h4>Link List (secondary actions)</h4><ul class="al-linklist"><li><a href="#">' + icon('graduation') + 'Alumni 101</a></li><li><a href="#">' + icon('calendar') + 'Plan Your Party</a></li></ul></div>', cls='al-section--warm')
main += split(6, text('Imagery', 'Photos follow the uvu.edu image style: a plain 4:3 photo (4:5 for a standing person) with 8px corners and APFY shapes from the APFY_Shapes file (_kit/shapes). The shapes are CSS layers (al-media--hatch, --stairs, --dot, --half); the page rotates them so neighbors never match.',
                      'Heroes are raw 1920×700 photos with the subject in the right half. The green fade is CSS. Phones get their own vertical photo (1080×1350, people centered) with the headline on a green fade rising from the bottom. Product shots (cards, plates) sit unframed. Headshots are square with 8px corners.'),
              frame('../graduating-students/assets/alumni-grads-celebrate.jpg', '', 'Example photo: graduates hugging', variant='hatch'))
main += one('6b', '''<ul class="al-grid al-grid--4" style="padding:0">''' + ''.join(f'<li style="list-style:none">' + frame('../graduating-students/assets/alumni-grads-celebrate.jpg', '', 'Example', variant=v) + f'<p class="al-meta" style="text-align:center">al-media--{v}</p></li>' for v in ['hatch', 'stairs', 'dot', 'half']) + '</ul>', note='The four APFY shape compositions.')
main += one(7, head('Icons', 'UVU Icon Library only, in UVU Green on light backgrounds and white on green. 2.5pt stroke, square caps. These are the ones the alumni pages use today.') +
            f'<ul class="al-grid" style="grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:24px">{ic}</ul>' +
            f'<details class="al-accordion accordion-unstyled" style="margin-top:48px"><summary>Full library ({len(alln)} icons, in _kit/icons/)</summary><div class="al-accordion-body"><ul class="al-grid" style="grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:16px">{icall}</ul></div></details>', cls='al-section--warm')
main += one(8, head('Components', 'Everything below is live markup from the pages.') + '''
               <div class="al-grid al-grid--3">
                  <article class="al-card"><div class="al-card-tag">''' + icon('award', 'white') + '''Card Tag</div><div class="al-card-body"><h3>Card</h3><p class="al-meta">al-card · al-card-tag · al-card-body · al-card-foot</p><ul class="al-checklist"><li>Check list</li><li>For requirements</li></ul><ol class="al-steps"><li>Steps</li><li>For sequences</li></ol></div><div class="al-card-foot"><p>Footnote</p></div></article>
                  <ul class="al-grid" style="padding:0"><li class="al-person" style="list-style:none"><img src="../about-saa/assets/saa-callie-ross.jpg" alt="Callie Ross" width="353" height="358"><h3>Person Card</h3><p>Ambassadors, recipients</p><details class="accordion-unstyled"><summary>Read More</summary><p>Optional story or quote.</p></details></li></ul>
                  <ul class="al-grid" style="padding:0"><li style="list-style:none"><a class="al-news-card" href="#"><img src="../alumni-home/assets/news-1.jpg" alt="" width="1200" height="750"><div class="al-card-body"><p class="al-meta">Sept. 1, 2026</p><h3>News Card: the Whole Card Is the Link</h3></div></a></li></ul>
               </div>
               <div style="max-width:820px;margin:64px auto 0"><h4>Accordion</h4><details class="al-accordion accordion-unstyled"><summary>Question in Title Case?</summary><div class="al-accordion-body"><p>Answer in sentence case.</p></div></details><details class="al-accordion accordion-unstyled"><summary>Another Question?</summary><div class="al-accordion-body"><p>Answer.</p></div></details></div>''')
main += one('8b', head('Utility Page Components', 'Added in v1.1 for the Board, Diplomas, Career, Aviation, and Job Shadow pages. Same tokens, no new colors or type.') + '''
               <div class="al-grid al-grid--3">
                  <article class="al-card"><div class="al-card-body">''' + icon('human-resources', cls='al-card-icon') + '''<h3>Resource Card</h3><p>Icon, heading, one paragraph. One text action in the foot.</p></div><div class="al-card-action"><a href="#">Text Action</a></div></article>
                  <div><h4 style="margin-top:0">Roster</h4><ul class="al-roster" style="columns:1"><li><span class="al-roster-key">2022–25</span><span>Name</span></li><li><span class="al-roster-key">President</span><span>Name ’13</span></li></ul>
                     <h4>Notice</h4>''' + '<div class="al-notice">' + icon('info-1') + '<p>Applications are currently closed.</p></div>' + '''</div>
                  <figure class="al-quote"><blockquote><p>“Testimonial in the speaker’s words. Typos are flagged, never silently fixed.”</p></blockquote><figcaption>Student</figcaption></figure>
               </div>
               <div style="max-width:820px;margin:48px auto 0"><h4>Event</h4>
                  <ul class="al-events"><li><time class="al-event-date" datetime="2026-11-06"><span>Nov.</span><strong>6</strong><span>2026</span></time><div><h3>Event Title in Title Case</h3><p class="al-meta">Noon–1:30 pm · Place</p><div class="al-actions" style="margin-top:12px"><a class="al-btn al-btn--secondary" href="#">RSVP</a></div></div></li></ul>
                  <h4>Past Events (compact)</h4>
                  <ul class="al-events al-events--compact"><li><p class="al-meta">Oct. 3, 2025</p><div><h3>Event Title</h3><p class="al-meta">Noon–1:30 pm · Place</p></div></li></ul>
                  <h4>Heroes</h4>
                  <p><code>al-hero--plain</code>: compact green hero for pages with no hero photo (Board, Job Shadow). <code>al-hero--scrim</code>: CSS gradient over a raw photo, for heroes not yet re-cut to the 1920×700 spec.</p>
               </div>''', cls='al-section--warm')
main += one(9, head('Page Rhythm', lead=False) + '''
               <ol class="al-steps" style="max-width:780px;margin:0 auto">
                  <li><strong>Hero</strong> (header-fullbleed): H1, optional lead, one light button.</li>
                  <li><strong>Intro</strong> (one-col, centered) or a first split.</li>
                  <li><strong>Splits</strong> (two-col): text in region 1, media in region 2. Alternate with <code>al-split--reverse</code>. Max two in a row.</li>
                  <li><strong>Bands</strong> break the run: warm (<code>al-section--warm</code>), photo (<code>al-section--photo</code>), card grids, or a centered statement.</li>
                  <li><strong>Alumni footer</strong> (<code>al-sitenav</code>): section nav, contact, and social, identical on every page; the current page is marked with <code>aria-current</code>. The CMS dept footer carries the office name.</li>
               </ol>
               <h4 style="max-width:780px;margin:48px auto 8px">Grid and Phones</h4>
               <ol class="al-steps" style="max-width:780px;margin:0 auto">
                  <li><strong>One edge.</strong> Container 1280px max, 40px gutter (24px under 768px). Heroes and sections share it.</li>
                  <li><strong>Breakpoints.</strong> Under 768px is the phone layout; 768px up is two-column; 1100px up opens the 4- and 5-up grids.</li>
                  <li><strong>Phones read left.</strong> Centered section heads turn left-aligned. Buttons go full width. Tap targets stay 44px or taller.</li>
                  <li><strong>Phone patterns.</strong> Quick links become a list with arrows, person cards become rows, news cards swipe sideways, partner logos sit three across.</li>
                  <li><strong>No inline styles.</strong> Use <code>al-center</code>, <code>al-actions--center</code>, <code>al-narrow</code>, and <code>al-section-head--left</code> so phone rules can override them.</li>
               </ol>''', cls='al-section--warm')
main += one(10, head('What Needs Overhauling', 'Found while standardizing. System items are already fixed in the mockups; brand and content items need a decision or an owner.') + f'<div style="max-width:880px;margin:0 auto">{fl}</div>')

html = page('alumni-styleguide', 'Alumni Web System', 'UVU Alumni web design system: type, color, icons, imagery, components, and overhaul flags.', 'n/a', main)
html = html.replace('<!-- SECTION 1 · template: header-fullbleed', '<!-- SECTION 1 · template: header-fullbleed (styleguide, not a CMS page)')
open(f'{OUTDIR}/index.html', 'w').write(html)
print('ok', len(alln))
