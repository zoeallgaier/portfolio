"""Parse live Give fund-directory pages (accordion-grid tiles) into JSON."""
import json, re, glob, os
from bs4 import BeautifulSoup
OLD = '/tmp/gv/old/'
out = {}
for f in sorted(glob.glob(OLD + '*.html')):
    soup = BeautifulSoup(open(f, encoding='utf-8', errors='ignore').read(), 'html.parser')
    for c in soup.find_all(string=lambda t: isinstance(t, type(soup.new_string('')).__class__.__bases__[0]) and False): pass
    main = soup.find('main')
    if not main: continue
    tiles = main.select('details.accordion-unstyled')
    if not tiles: continue
    units = []
    for d in tiles:
        sm = d.find('summary')
        img = sm.find('img') if sm else None
        h = sm.find(['h2', 'h3', 'h4']) if sm else None
        name = re.sub(r'\s+', ' ', h.get_text(' ', strip=True)) if h else ''
        if not name and sm: name = re.sub(r'\s+', ' ', sm.get_text(' ', strip=True))
        body = d.find(class_='accordion-content') or d
        groups = []; cur = None
        for el in body.find_all(['h2', 'h3', 'h4', 'a']):
            if el.name in ('h2', 'h3', 'h4'):
                cur = [re.sub(r'\s+', ' ', el.get_text(' ', strip=True)), []]; groups.append(cur)
            elif el.name == 'a' and el.get('href') and el.get('href') != '#':
                t = re.sub(r'\s+', ' ', el.get_text(' ', strip=True))
                if not t or t == 'NAME': continue
                if cur is None: cur = ['', []]; groups.append(cur)
                cur[1].append([t, el['href']])
        groups = [g for g in groups if g[1]]
        units.append({'name': name, 'img': os.path.basename(img['src']) if img else None, 'alt': img.get('alt', '') if img else '',
                      'sumlink': (sm.find('a') or {}).get('href') if sm else None, 'groups': groups})
    contacts = []
    for card in main.select('.directory-card, .dir-card, [class*=directory]'):
        pass
    key = os.path.basename(f).split(' _ ')[0]
    out[key] = units
    print(key, len(units), sum(len(g[1]) for u in units for g in u['groups']))
json.dump(out, open('/tmp/gv/funds.json', 'w'), indent=1, ensure_ascii=False)
