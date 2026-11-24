import re, json, os
from svgelements import SVG, Path, Shape, Use, Group
import html as H
pages = re.split(r'<page ', open('bbox.html').read())[1:]
os.makedirs('out', exist_ok=True)
index = []
SEEN = set()
for pi, pg in enumerate(pages, 1):
    lines = []
    for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', pg, re.S):
        words = re.findall(r'>([^<]+)</word>', m.group(5))
        lines.append([float(m.group(i)) for i in range(1, 5)] + [' '.join(words)])
    # bbox-layout lines may span multiple labels in a row: split by words instead
    words = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)</word>', pg)]
    # cluster words into labels: same row (y within 3) and gap < 9pt
    words.sort(key=lambda w: (round(w[1]), w[0]))
    labels = []
    for w in words:
        for L in labels:
            if abs(L['y0'] - w[1]) < 3 and w[0] - L['x1'] < 9:
                L['x1'] = w[2]; L['t'] += ' ' + w[4]; break
        else:
            labels.append(dict(x0=w[0], y0=w[1], x1=w[2], y1=w[3], t=w[4]))
    # merge second label lines (directly below, overlapping x-center)
    labels.sort(key=lambda L: (L['y0'], L['x0']))
    merged = []
    for L in labels:
        cx = (L['x0'] + L['x1']) / 2
        for M in merged:
            mcx = (M['x0'] + M['x1']) / 2
            if abs(mcx - cx) < 40 and -1 < L['y0'] - M['y1'] < 12:
                M['t'] += ' ' + L['t']; M['y1'] = L['y1']; break
        else:
            merged.append(dict(L))
    svg = SVG.parse(f'pg{pi}.svg')
    shapes = []
    for e in svg.elements():
        if isinstance(e, Shape) and not isinstance(e, Use) and str(e.values.get('fill','')).strip()=='none' and e.values.get('stroke') not in (None,'none'):
            # skip glyphs (they live under defs/use; svgelements expands uses -> detect tiny glyph paths by parent id)
            try:
                bb = e.bbox()
            except Exception:
                continue
            if bb is None:
                continue
            shapes.append((e, bb))
    for M in merged:
        cx = (M['x0'] + M['x1']) / 2
        top = M['y0']
        cell = (cx - 55, top - 85, cx + 55, top - 3)
        mine = [(e, bb) for e, bb in shapes if cell[0] <= (bb[0] + bb[2]) / 2 <= cell[2] and cell[1] <= (bb[1] + bb[3]) / 2 <= cell[3] and (bb[3] - bb[1]) < 90]
        if not mine:
            continue
        x0 = min(b[0] for _, b in mine); y0 = min(b[1] for _, b in mine); x1 = max(b[2] for _, b in mine); y1 = max(b[3] for _, b in mine)
        ds = []
        for e, bb in mine:
            p = Path(e) if not isinstance(e, Path) else e
            p = abs(p) if False else p
            p.reify()
            ds.append((p.d(), False, True, float(e.values.get('stroke-width', 2.5)) * 0.9999))
        name = re.sub(r'[^a-z0-9]+', '-', M['t'].lower()).strip('-')
        base_, k = name, 2
        while name in SEEN:
            name = f'{base_}-{k}'; k += 1
        SEEN.add(name)
        pad = 2.5
        W, Hh = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
        body = ''
        for d, f, s, sw in ds:
            if s and not f:
                body += f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw:.3f}" stroke-linecap="square" stroke-linejoin="miter" stroke-miterlimit="10"/>'
            else:
                body += f'<path d="{d}" fill="currentColor"/>'
        out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - pad:.2f} {y0 - pad:.2f} {W:.2f} {Hh:.2f}" width="48" height="48" aria-hidden="true">{body}</svg>'
        open(f'out/{name}.svg', 'w').write(out)
        index.append(dict(name=name, page=pi, label=M['t'], n=len(mine), fills=sum(1 for d in ds if d[1]), strokes=sum(1 for d in ds if d[2] and not d[1])))
json.dump(index, open('index.json', 'w'), indent=0)
print(len(index))
print(', '.join(i['name'] for i in index))
print('fills/strokes sample', index[:3])
