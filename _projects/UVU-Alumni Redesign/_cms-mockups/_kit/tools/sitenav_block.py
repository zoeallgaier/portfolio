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
       ('Students', [('Graduating Students', 'graduating-students'), ('Student Alumni Ambassadors', 'about-saa')]),
       ('About', [('Alumni Home', 'alumni-home'), ('Alumni Awards', 'alumni-awards'), ('Board of Directors', 'alumni-board')])]

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
                  <p class="al-sitenav-title">UVU Alumni Relations</p>
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
