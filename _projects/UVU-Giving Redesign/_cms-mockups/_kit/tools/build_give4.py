#!/usr/bin/env python3
"""UVU Giving v1.6: fund-directory pages move onto Cesar's June 2026 template (new-format-26):
sidebar tabs + content panels + fund items + search + For More Information.
Our hero (photo, tagline eyebrow, H1, phone layer) and the Give footer stay."""
import os, sys, re, html as H
sys.path.insert(0, '/tmp/gv/tools'); sys.path.insert(0, '/tmp/xr')
import build_give as G
import build_give3 as G3
from build_give import P, OUT, flag, todo, btn, grid, page, footer
from build_give2 import FUNDS, amp, TYPO, GROUP, COLLEGES, hero_x, tile_link, contact_card, directory_todo

NF = []  # slugs on the new format
LEARN = flag('Learn More', 'From Cesar’s template. Needs each department’s page URL.')


def slug_id(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower().replace('&', 'and')).strip('-')
    return s[:48].rstrip('-')


def units(key, skip=()):
    out, seen = [], set()
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
        i = slug_id(u['name'])
        while i in seen: i += '-2'
        seen.add(i)
        img = u['img'] if (u['img'] or '').startswith('http') else 'fund-' + (u['img'] or '').replace('_', '-')
        out.append((i, u['name'], groups, img, u.get('alt') or ''))
    return out


def item(t, href):
    name = TYPO[t][0] if t in TYPO else t
    return (f'<li><a class="fund-item" href="{H.escape(href)}" target="_blank" rel="noopener"><span class="al-nf-name">{name}</span>'
            f'<span class="al-nf-give" aria-hidden="true">{flag("Give", "New label on each fund row.")}</span><span class="sr-only-al"> (opens the giving form in a new tab)</span></a></li>')


def tabs(us, mobile):
    rows = ['<li><a href="#search" class="anchorTab menu-btn noScroll"' + ('' if mobile else ' data-target="search"') + ' aria-controls="search" aria-expanded="false" role="tab"><span class="al-nf-tab">' + flag("Search All Funds", "Cesar’s template: “Search.”") + '</span></a></li>']
    for k, (i, name, groups, _, _) in enumerate(us):
        n = sum(len(l) for _, l in groups)
        on = k == 0
        rows.append(f'<li><a href="#{i}" class="anchorTab menu-btn{" active" if on else ""} noScroll"' + ('' if mobile else f' data-target="{i}"') +
                    f' aria-controls="{i}" aria-expanded="{"true" if on else "false"}" role="tab"><span class="al-nf-tab">{amp(name)}</span></a></li>')
    return '\n                     '.join(rows)


def panels(us, subj):
    out = []
    for k, (i, name, groups, img, alt) in enumerate(us):
        multi = len(groups) > 1
        n = sum(len(l) for _, l in groups)
        parts = [f'{len(l)} {SING.get(g, g.lower()) if len(l) == 1 else g.lower()}' for g, l in groups] if multi else [f'{n} fund{"s" * (n != 1)}']
        lists = ''
        for g, links in groups:
            hh = f'\n                        <h3 class="al-nf-group">{g} <span>{len(links)}</span></h3>' if multi else ''
            lists += hh + '\n                        <ul>\n                           ' + '\n                           '.join(item(t, h) for t, h in links) + '\n                        </ul>'
        out.append(f'''                     <!-- {H.escape(name).upper()} -->
                     <div class="content-panel tab-container{" open" if k == 0 else ""}" id="{i}">
                        <div class="al-nf-head">
                           <img class="al-nf-thumb" src="{img if img.startswith('http') else 'assets/' + img}" data-cms-src="{img.replace('https://www.uvu.edu', '') if img.startswith('http') else '/give/images/funds/' + img}" alt="{H.escape(alt)}" width="600" height="400" loading="lazy"{' onerror="this.remove()"' if img.startswith('http') else ''}>
                           <div>
                              <p class="al-nf-meta">{" · ".join(parts)}</p>
                              <h2>{amp(name)}</h2>
                              <p>{todo(f"COPY: 2 or 3 sentences on what a gift to {name} does for {subj} students.")}</p>
                              <a class="al-nf-learn" href="#">{flag("About " + amp(name), "Cesar’s template: “Learn More” button. Needs the department page URL.")}</a>
                           </div>
                        </div>{lists}
                     </div>''')
    return '\n'.join(out)


def search_panel(short, area):
    return f'''                     <!-- SEARCH -->
                     <div class="tab-container" id="search">
                        <h2>Search All {short} Funds</h2>
                        <!-- Production: Cesar's Blackbaud designation search embed goes here (one per college; the CHPS embed id is dc89e2b3-…).
                             Mockup: the same search as the Give page, filtered to this area on Find a Fund. -->
                        <form class="al-search al-search--left" action="../find-a-fund/index.html" method="get" role="search">
                           <label for="area-q">Search {short} funds</label>
                           <input type="hidden" name="area" value="{area}">
                           <input id="area-q" name="q" type="search" placeholder="Fund, program, or scholarship name">
                           <button type="submit" class="al-btn al-btn--primary">Search</button>
                        </form>
                     </div>'''


def funds_section(n, us, short, area, subj):
    return f'''
<!-- SECTION {n} · template: one-col · Cesar's new-format-26 fund directory (/give/lib/css/new-format-26.css).
     Sidebar tabs (desktop) + MAIN MENU popover (phones) + one content panel per department, each fund a link to its Blackbaud form. -->
<section data-uvu-template="one-col" data-uvu-section="{n}" class="al-section al-nf">
   <div class="container-fluid">
      <div class="row">
         <div class="col-xs-12 col-target region" data-uvu-region="1">
            <!-- MOBILE MENU BAR -->
            <div class="mobile-menu-bar">
               <div class="al-nf-bar"><span class="al-nf-bar-label">{flag("Browse Funds", "Cesar’s template: “MAIN MENU.”")}</span><span class="al-nf-bar-current">{amp(us[0][1])}</span></div>
               <button class="menu-toggle" id="menuToggle" type="button" popovertarget="mobileFundsMenu" popovertargetaction="toggle" aria-label="Open main menu"><span></span><span></span><span></span></button>
            </div>
            <!-- MOBILE-ONLY POPOVER MENU -->
            <nav id="mobileFundsMenu" class="funds-sidebar mobile-funds-sidebar" popover="auto" aria-label="Funds menu">
               <div class="mobile-popover-header">
                  <h2 class="sidebar-title">{flag("Browse Funds", "Cesar’s template: “MAIN MENU.”")}</h2>
                  <button type="button" class="close-menu" popovertarget="mobileFundsMenu" popovertargetaction="hide" aria-label="Close main menu">×</button>
               </div>
               <ul class="tabs">
                     {tabs(us, True)}
               </ul>
            </nav>
            <!-- MAIN LAYOUT -->
            <section class="funds-layout">
               <nav class="funds-sidebar desktop-funds-sidebar" aria-label="Funds menu">
                  <h2 class="sidebar-title">{flag("Browse Funds", "Cesar’s template: “MAIN MENU.”")}</h2>
                  <ul class="tabs">
                     {tabs(us, False)}
                  </ul>
               </nav>
               <section class="funds-content tabs-content">
{panels(us, subj)}
{search_panel(short, area)}
               </section>
            </section>
         </div>
      </div>
   </div>
</section>'''


def info_section(n, contacts, emp=None):
    widget = (f'\n            <!-- Production: Cesar\'s directory widget renders the contact card here: '
              f'<div class="directory"><div class="output employees" data-directory-calltype="emps" data-directory-listtype="advanced" data-directory-val="{emp}," data-directory-style="style1" data-directory-columns="4"></div></div> -->') if emp else ''
    return f'''
<!-- SECTION {n} · template: one-col (header region + region 1), as in Cesar's template -->
<section data-uvu-template="one-col" data-uvu-section="{n}" class="al-section al-section--warm al-nf-info">
   <div class="container-fluid">
      <div class="row">
         <div class="col-xs-12 col-target region padding-bottom-0 container-wide" data-uvu-region="header">
            <h2 class="divider-header">{flag("Questions? Contact Us", "Cesar’s template and live: “For More Information.”")}</h2>
         </div>
      </div>
      <div class="row">
         <div class="col-xs-12 col-target region padding-top-0" data-uvu-region="1">{widget}
            {grid(contacts, 3, 'al-grid--center')}
         </div>
      </div>
   </div>
</section>'''


def build(slug, key, title, cms_hero, eyebrow, lead, button, note, short, area, subj, contacts, emp, skip=()):
    us = units(key, skip)
    c = hero_x(1, slug, cms_hero, title, eyebrow=eyebrow, lead=lead, button=button, note=note)
    c += funds_section(2, us, short, area, subj)
    c += info_section(3, contacts, emp)
    c += footer(4)
    NF.append(slug)
    return c, sum(len(l) for _, _, gs, _, _ in us for _, l in gs), len(us)


SING = {'Programs': 'program', 'Scholarships': 'scholarship', 'General Funds': 'general fund', 'Other Funds': 'other fund', 'Department Fund': 'department fund'}
TYPO['Capital Reef Fieldwork'] = ('Capitol Reef Fieldwork', 'Live: “Capital Reef.”')
EMP = {'college-health-public-service': '10919463', 'college-of-science': '10192452', 'school-of-education': '11030256', 'woodbury-school-business': '10806932'}
for key, slug, name, tag, subj, short, contacts in COLLEGES:
    sch = tile_link(key, short + ' Scholar') or tile_link(key, short)
    c, nf, nu = build(slug, key, name, f'/give/colleges-schools/{slug}/images/{slug}-header.jpg', tag,
                      f'Your gift impacts UVU {subj} students for a lifetime.', (f'Give to {short} Scholarships', sch), G3.G2.FORM_NOTE,
                      short, name.replace(' ', '+'), subj, contacts, EMP.get(slug))
    P[slug] = (P[slug][0], P[slug][1], P[slug][2], c)
    print(slug, nu, 'departments', nf, 'funds')

S = 'programs-centers'
c, nf, nu = build(S, 'Programs & Centers', 'Programs and Centers', '/give/programs-centers/images/programs-centers-header.jpg', 'Give to UVU',
                  'Your gift impacts UVU students for a lifetime.', None, None, 'Programs and Centers', 'Programs+and+Centers', 'UVU',
                  [contact_card('Dan Dimond', flag('Senior Director of Development', 'Live: “Sr Director.”'), 'd2ZyMVZjUkFhbnRrbUt0YnRHSHZ6UT09', '801-863-8568', 111)], None,
                  skip=('Baugh Entrepreneurship Institute', 'UVU Museum of Art at Lakemount'))
P[S] = (P[S][0], P[S][1], P[S][2], c.replace('Search All Programs and Centers Funds', 'Search All Program and Center Funds'))
print(S, nu, 'departments', nf, 'funds')

if __name__ == '__main__':
    for slug in NF:
        title, desc, url, main = P[slug]
        html = page(slug, title, desc, url, main)
        html = html.replace('<link rel="stylesheet" href="../_kit/css/12-alumni-system.css">',
                            '<!-- Cesar\'s fund-page stylesheet (production: /give/lib/css/new-format-26.css). Loads before the system file so the hero and type stay on system. -->\n'
                            '<link rel="stylesheet" href="../_kit/css/13-give-new-format-26.css">\n<link rel="stylesheet" href="../_kit/css/12-alumni-system.css">')
        html = html.replace('<script src="../_kit/js/mockup-tools.js"></script>',
                            '<script src="../_kit/js/mockup-tools.js"></script>\n<script src="../_kit/js/funds-tabs.js" defer></script>')
        assert '13-give-new-format-26' in html and 'funds-tabs.js' in html, slug
        open(f'{OUT}/{slug}/index.html', 'w').write(html)
        print('wrote', slug)
