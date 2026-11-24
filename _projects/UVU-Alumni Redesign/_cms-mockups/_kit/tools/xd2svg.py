#!/usr/bin/env python3
"""Minimal Adobe XD (AGC JSON) -> SVG renderer.

Usage (as a module):
    r = XD(src_dir)                      # dir with agc/, res/
    html = r.artboard_html(name)         # full artboard
    html = r.node_html(artboard_name, node_name, pad=0)  # one group/shape, cropped to its bounds
Images are referenced as file:// paths into res/. Fonts come from local @fontsource files.
"""
import json, os, re, html, glob, math

FONT_DIR = '/tmp/xr/node_modules/@fontsource'
WEIGHTS = {'thin': 100, 'extralight': 200, 'light': 300, 'regular': 400, 'book': 400, 'medium': 500,
           'semibold': 600, 'demibold': 600, 'bold': 700, 'extrabold': 800, 'black': 900, 'heavy': 900}


def font_css():
    css = []
    for fam, pkg in [('Rajdhani', 'rajdhani'), ('Source Sans 3', 'source-sans-3'), ('Lato', 'lato'), ('Montserrat', 'montserrat')]:
        for f in glob.glob(f'{FONT_DIR}/{pkg}/files/{pkg}-latin-*-*.woff2'):
            m = re.search(r'latin-(\d+)-(normal|italic)\.woff2$', f)
            if not m:
                continue
            css.append(f"@font-face{{font-family:'{fam}';font-weight:{m.group(1)};font-style:{m.group(2)};src:url('file://{f}') format('woff2');}}")
    return '\n'.join(css)


def esc(s):
    return html.escape(s, quote=True)


def rgba(c, alpha=None):
    if c is None:
        return 'none', 1
    v = c.get('value', {})
    a = c.get('alpha', 1) if alpha is None else alpha
    return f"rgb({v.get('r', 0)},{v.get('g', 0)},{v.get('b', 0)})", a


def argb_int(n):
    a = (n >> 24) & 255
    r = (n >> 16) & 255
    g = (n >> 8) & 255
    b = n & 255
    return f'rgb({r},{g},{b})', a / 255


def path_bbox(d):
    nums = [float(x) for x in re.findall(r'-?\d*\.?\d+(?:e-?\d+)?', d)]
    xs, ys = nums[0::2], nums[1::2]
    if not xs:
        return 0, 0, 0, 0
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


class XD:
    def __init__(self, src):
        self.src = src
        self.res = src + '/res'
        self.meta = json.load(open(self.res + '/meta.json'))
        self.resources = json.load(open(src + '/agc/resources.agc'))
        self.boards = self.resources['artboards']
        self.ab = {}
        for f in glob.glob(src + '/agc/artboard-*.agc'):
            bid = os.path.basename(f)[len('artboard-'):-4]
            self.ab[self.boards[bid]['name']] = (bid, json.load(open(f)))
        self.idx = {}
        ux = self.resources['resources']['meta']['ux']
        self._index(ux.get('symbols', []))
        for bid, a in self.ab.values():
            self._index(a['children'][0]['artboard']['children'])
        self.defs = []
        self.n = 0

    def _index(self, items):
        for it in items:
            if 'id' in it:
                self.idx.setdefault(it['id'], it)
            for st in it.get('meta', {}).get('ux', {}).get('states', []) or []:
                self._index([st])
            for key in ('group', 'syncRef'):
                if isinstance(it.get(key), dict):
                    self._index(it[key].get('children', []))

    def uid(self, p='d'):
        self.n += 1
        return f'{p}{self.n}'

    def img_path(self, uid):
        for ext in ('jpg', 'png'):
            p = f'{self.res}/{uid}.{ext}'
            if os.path.exists(p):
                return p
        return None

    # ---------- paint ----------
    def paint(self, fill, bbox, shape_svg):
        """returns (fill attr string, extra svg drawn instead) for a fill"""
        t = (fill or {}).get('type')
        if t in (None, 'none'):
            return 'fill="none"', ''
        if t == 'solid':
            c, a = rgba(fill.get('color'))
            return f'fill="{c}" fill-opacity="{a:.3f}"', ''
        if t == 'gradient':
            g = fill['gradient']
            gr = g.get('meta', {}).get('ux', {}).get('gradientResources', {})
            gid = self.uid('g')
            stops = ''.join(
                f'<stop offset="{s["offset"]}" stop-color="{rgba(s["color"])[0]}" stop-opacity="{s["color"].get("alpha", 1)}"/>'
                for s in gr.get('stops', []))
            if gr.get('type') == 'radial':
                self.defs.append(f'<radialGradient id="{gid}" cx="{g.get("cx", .5)}" cy="{g.get("cy", .5)}" r="{g.get("r", .5)}" '
                                 f'gradientUnits="{g.get("units", "objectBoundingBox")}">{stops}</radialGradient>')
            else:
                self.defs.append(f'<linearGradient id="{gid}" x1="{g.get("x1", 0)}" y1="{g.get("y1", 0)}" x2="{g.get("x2", 1)}" y2="{g.get("y2", 0)}" '
                                 f'gradientUnits="{g.get("units", "objectBoundingBox")}">{stops}</linearGradient>')
            return f'fill="url(#{gid})"', ''
        if t == 'pattern':
            p = fill['pattern']
            m = p.get('meta', {}).get('ux', {})
            uid = m.get('uid')
            path = self.img_path(uid)
            x, y, W, H = bbox
            iw, ih = p.get('width', 1), p.get('height', 1)
            beh = m.get('scaleBehavior', 'fill')
            s0 = max(W / iw, H / ih)
            s = s0 * m.get('scale', 1)
            sw, sh = iw * s, ih * s
            # XD: offsets are measured from center, as a fraction of the cover-fitted (unscaled) image size
            left = (sw - W) / 2 - m.get('offsetX', 0) * iw * s0
            top = (sh - H) / 2 - m.get('offsetY', 0) * ih * s0
            cid = self.uid('c')
            self.defs.append(f'<clipPath id="{cid}">{shape_svg}</clipPath>')
            if not path:
                return 'fill="#ff00aa"', ''
            img = (f'<image href="file://{path}" x="{x - left:.2f}" y="{y - top:.2f}" width="{sw:.2f}" height="{sh:.2f}" '
                   f'preserveAspectRatio="none" clip-path="url(#{cid})"/>')
            return 'fill="none"', img
        return 'fill="none"', ''

    def filters(self, st):
        fl = [f for f in st.get('filters', []) if f.get('visible', True) is not False]
        out = []
        for f in fl:
            if f.get('type') == 'dropShadow':
                for d in f.get('params', {}).get('dropShadows', []):
                    c, a = rgba(d.get('color'))
                    out.append(f'<feDropShadow dx="{d.get("dx", 0)}" dy="{d.get("dy", 0)}" stdDeviation="{d.get("r", 0) / 2}" flood-color="{c}" flood-opacity="{a}"/>')
            if f.get('type') == 'uxdesign#blur' and f.get('params', {}).get('visible', True):
                out.append(f'<feGaussianBlur stdDeviation="{f["params"].get("blurAmount", 0) / 2}"/>')
        if not out:
            return ''
        fid = self.uid('f')
        self.defs.append(f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%">{"".join(out)}</filter>')
        return f' filter="url(#{fid})"'

    # ---------- nodes ----------
    def tf(self, it):
        t = it.get('transform')
        if not t:
            return ''
        return f' transform="matrix({t.get("a", 1)},{t.get("b", 0)},{t.get("c", 0)},{t.get("d", 1)},{t.get("tx", 0)},{t.get("ty", 0)})"'

    def node(self, it, depth=0):
        if depth > 40:
            return ''
        if it.get('visible') is False or it.get('meta', {}).get('ux', {}).get('hidden'):
            return ''
        t = it.get('type')
        st = it.get('style', {})
        op = st.get('opacity')
        attrs = self.tf(it) + (f' opacity="{op}"' if op is not None and op != 1 else '') + self.filters(st)
        if t == 'syncRef':
            src = self.idx.get(it.get('syncSourceGuid'))
            return self.node(src, depth + 1) if src else ''
        if t == 'group':
            kids = it.get('group', {}).get('children', [])
            return f'<g{attrs}>' + ''.join(self.node(k, depth + 1) for k in kids) + '</g>'
        if t == 'shape':
            return f'<g{attrs}>' + self.shape(it) + '</g>'
        if t == 'text':
            return f'<g{attrs}>' + self.text(it) + '</g>'
        return ''

    def shape(self, it):
        sh = it['shape']
        st = it.get('style', {})
        k = sh['type']
        if k == 'rect':
            x, y, w, h = sh.get('x', 0), sh.get('y', 0), sh['width'], sh['height']
            r = sh.get('r', 0)
            r = r[0] if isinstance(r, list) else r
            geo = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(r, w / 2, h / 2)}"/>'
            bbox = (x, y, w, h)
        elif k in ('ellipse', 'circle'):
            cx, cy = sh.get('cx', 0), sh.get('cy', 0)
            rx = sh.get('rx', sh.get('r', 0))
            ry = sh.get('ry', sh.get('r', 0))
            geo = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>'
            bbox = (cx - rx, cy - ry, 2 * rx, 2 * ry)
        elif k == 'line':
            geo = f'<line x1="{sh["x1"]}" y1="{sh["y1"]}" x2="{sh["x2"]}" y2="{sh["y2"]}"/>'
            bbox = (sh['x1'], sh['y1'], sh['x2'] - sh['x1'], sh['y2'] - sh['y1'])
        elif k in ('path', 'compound'):
            d = sh.get('path', '')
            geo = f'<path d="{d}" fill-rule="evenodd"/>'
            bbox = path_bbox(d)
        else:
            return ''
        fill_attr, extra = self.paint(st.get('fill'), bbox, geo)
        stroke = st.get('stroke', {})
        sattr = ''
        if stroke.get('type') == 'solid' and stroke.get('width', 0) > 0:
            c, a = rgba(stroke.get('color'))
            sattr = f' stroke="{c}" stroke-opacity="{a}" stroke-width="{stroke["width"]}"'
            if stroke.get('dash'):
                sattr += f' stroke-dasharray="{",".join(map(str, stroke["dash"]))}"'
            if stroke.get('cap'):
                sattr += f' stroke-linecap="{stroke["cap"]}"'
        if k == 'line':
            fill_attr = 'fill="none"'
        geo_painted = geo.replace('/>', f' {fill_attr}{sattr}/>', 1)
        if extra:
            return extra + (geo.replace('/>', f' fill="none"{sattr}/>', 1) if sattr else '')
        return geo_painted

    def text(self, it):
        tx = it['text']
        raw = tx.get('rawText', '')
        st = it.get('style', {})
        f = st.get('font', {})
        ta = st.get('textAttributes', {})
        ux = it.get('meta', {}).get('ux', {})
        ranged = ux.get('rangedStyles') or []
        base_fill = rgba(st.get('fill', {}).get('color')) if st.get('fill', {}).get('type') == 'solid' else ('rgb(0,0,0)', 1)
        # per-char style table
        styles = []
        if ranged:
            for rs in ranged:
                styles += [rs] * rs.get('length', 0)
        def style_at(i):
            rs = styles[i] if i < len(styles) else (styles[-1] if styles else {})
            fam = rs.get('fontFamily', f.get('family', 'Source Sans 3'))
            sty = rs.get('fontStyle', f.get('style', 'Regular'))
            size = rs.get('fontSize', f.get('size', 16))
            fill = argb_int(rs['fill']['value']) if isinstance(rs.get('fill'), dict) and 'value' in rs['fill'] else base_fill
            tt = rs.get('textTransform', 'none')
            cs = rs.get('charSpacing', ta.get('letterSpacing', 0)) or 0
            ul = rs.get('underline', False)
            return (fam, sty, size, fill, tt, cs, ul)
        align = ta.get('paragraphAlign', 'left')
        frame = tx.get('frame', {})
        fw = frame.get('width')
        out = []
        for para in tx.get('paragraphs', []):
            for line in para.get('lines', []):
                for seg in line:
                    a, b = seg.get('from', 0), seg.get('to', 0)
                    x, y = seg.get('x', 0), seg.get('y', 0)
                    anchor = 'start'
                    if fw and align in ('center', 'right') and abs(x) < 0.01:
                        anchor = 'middle' if align == 'center' else 'end'
                        x = fw / 2 if align == 'center' else fw
                    spans = []
                    i = a
                    while i < b:
                        s0 = style_at(i)
                        j = i
                        while j < b and style_at(j) == s0:
                            j += 1
                        txt = raw[i:j].replace('\n', '')
                        fam, sty, size, fill, tt, cs, ul = s0
                        w = WEIGHTS.get(sty.lower().replace(' ', '').replace('italic', '') or 'regular', 400)
                        it_ = 'italic' if 'italic' in sty.lower() else 'normal'
                        css = (f"font-family:'{fam}';font-weight:{w};font-style:{it_};font-size:{size}px;"
                               f"letter-spacing:{cs / 1000 * size:.2f}px;" + ('text-transform:uppercase;' if tt == 'uppercase' else '') +
                               ('text-decoration:underline;' if ul else ''))
                        if tt == 'uppercase':
                            txt = txt.upper()
                        elif tt == 'lowercase':
                            txt = txt.lower()
                        spans.append(f'<tspan style="{css}" fill="{fill[0]}" fill-opacity="{fill[1]:.3f}">{esc(txt)}</tspan>')
                        i = j
                    out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" xml:space="preserve">{"".join(spans)}</text>')
        return ''.join(out)

    # ---------- entry points ----------
    def find(self, items, name):
        for it in items:
            if it.get('name') == name:
                return it
            ch = it.get('group', {}).get('children') if isinstance(it.get('group'), dict) else None
            if ch:
                r = self.find(ch, name)
                if r:
                    return r
        return None

    def board(self, name):
        bid, a = self.ab[name]
        return self.boards[bid], a['children'][0]['artboard']['children']

    def wrap(self, body, w, h, vb, bg='#ffffff'):
        defs = '<defs>' + ''.join(self.defs) + '</defs>'
        self.defs = []
        return (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}'
                f'html,body{{margin:0;padding:0;background:{bg}}} svg{{display:block}}</style></head><body>'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">{defs}{body}</svg></body></html>')

    def artboard_html(self, name, scale=1.0):
        info, kids = self.board(name)
        body = f'<g transform="translate({-info["x"]},{-info["y"]})">' + ''.join(self.node(k) for k in kids) + '</g>'
        return self.wrap(body, info['width'] * scale, info['height'] * scale, f'0 0 {info["width"]} {info["height"]}')

    def node_html(self, board_name, node_name, box, bg='transparent'):
        """box = (x,y,w,h) in artboard coords to crop to"""
        info, kids = self.board(board_name)
        it = self.find(kids, node_name)
        assert it, node_name
        # render node in context of its ancestors' transforms: we need the absolute matrix.
        path = self._path_to(kids, it) or [it]
        body = ''
        open_g = ''
        for anc in path[:-1]:
            open_g += f'<g{self.tf(anc)}>'
        body = open_g + self.node(it) + '</g>' * (len(path) - 1)
        body = f'<g transform="translate({-info["x"]},{-info["y"]})">{body}</g>'
        x, y, w, h = box
        return self.wrap(body, w, h, f'{x} {y} {w} {h}', bg)

    def _path_to(self, items, target, trail=None):
        trail = trail or []
        for it in items:
            if it is target:
                return trail + [it]
            ch = it.get('group', {}).get('children') if isinstance(it.get('group'), dict) else None
            if ch:
                r = self._path_to(ch, target, trail + [it])
                if r:
                    return r
        return None


def mat_mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


def tmat(it):
    t = it.get('transform') or {}
    return (t.get('a', 1), t.get('b', 0), t.get('c', 0), t.get('d', 1), t.get('tx', 0), t.get('ty', 0))


def local_bbox(it):
    sh = it.get('shape', {})
    k = sh.get('type')
    if k == 'rect':
        return sh.get('x', 0), sh.get('y', 0), sh['width'], sh['height']
    if k in ('ellipse', 'circle'):
        rx = sh.get('rx', sh.get('r', 0)); ry = sh.get('ry', sh.get('r', 0))
        return sh.get('cx', 0) - rx, sh.get('cy', 0) - ry, 2 * rx, 2 * ry
    if k in ('path', 'compound'):
        return path_bbox(sh.get('path', ''))
    if k == 'line':
        return min(sh['x1'], sh['x2']), min(sh['y1'], sh['y2']), abs(sh['x2'] - sh['x1']), abs(sh['y2'] - sh['y1'])
    if it.get('type') == 'text':
        fr = it['text'].get('frame', {})
        size = it.get('style', {}).get('font', {}).get('size', 16)
        lines = sum(len(p.get('lines', [])) for p in it['text'].get('paragraphs', []))
        return 0, -size, fr.get('width', size * len(it['text'].get('rawText', '')) * .5), fr.get('height', lines * size * 1.3)
    return None


def bounds(r, it, m=(1, 0, 0, 1, 0, 0), depth=0):
    """absolute bbox (x0,y0,x1,y1) in pasteboard coords"""
    if depth > 40 or it is None:
        return None
    if it.get('type') == 'syncRef':
        return bounds(r, r.idx.get(it.get('syncSourceGuid')), m, depth + 1)
    m2 = mat_mul(m, tmat(it))
    if it.get('type') == 'group':
        bs = [bounds(r, k, m2, depth + 1) for k in it['group'].get('children', [])]
        bs = [b for b in bs if b]
        if not bs:
            return None
        return min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)
    lb = local_bbox(it)
    if not lb:
        return None
    x, y, w, h = lb
    pts = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    a, b, c, d, e, f = m2
    tp = [(a * px + c * py + e, b * px + d * py + f) for px, py in pts]
    sw = it.get('style', {}).get('stroke', {})
    pad = sw.get('width', 0) if sw.get('type') == 'solid' else 0
    return min(p[0] for p in tp) - pad, min(p[1] for p in tp) - pad, max(p[0] for p in tp) + pad, max(p[1] for p in tp) + pad


def has_image(r, it, depth=0):
    if depth > 40 or it is None:
        return False
    if it.get('type') == 'syncRef':
        return has_image(r, r.idx.get(it.get('syncSourceGuid')), depth + 1)
    if it.get('style', {}).get('fill', {}).get('type') == 'pattern':
        return True
    return any(has_image(r, k, depth + 1) for k in it.get('group', {}).get('children', []))


def _skip_text(it):
    if it is None or it.get('type') == 'text':
        return None
    return it


def render_nodes(r, board, nodes, box=None, skip_text=False, bg='transparent', recolor=None, label=None):
    """nodes: list of node dicts (found via r.find). Each rendered with its ancestor transforms."""
    info, kids = r.board(board)
    body = ''
    bbs = []
    for it in nodes:
        path = r._path_to(kids, it) or [it]
        m = (1, 0, 0, 1, 0, 0)
        for anc in path[:-1]:
            m = mat_mul(m, tmat(anc))
        bb = bounds(r, it, m)
        if bb:
            bbs.append(bb)
        if skip_text:
            orig = r.node
            def node_nt(x, depth=0, _o=orig):
                if x is not None and x.get('type') == 'text':
                    return ''
                return _o(x, depth)
            r.node = node_nt
        frag = r.node(it)
        if skip_text:
            r.node = orig
        body += ''.join(f'<g{r.tf(a)}>' for a in path[:-1]) + frag + '</g>' * (len(path) - 1)
    if box is None:
        x0 = min(b[0] for b in bbs); y0 = min(b[1] for b in bbs); x1 = max(b[2] for b in bbs); y1 = max(b[3] for b in bbs)
        box = (x0 - info['x'], y0 - info['y'], x1 - x0, y1 - y0)
    x, y, w, h = [round(v) for v in box]
    body = f'<g transform="translate({-info["x"]},{-info["y"]})">{body}</g>'
    if label:
        body += (f'<text x="{x + w / 2}" y="{y + h / 2}" text-anchor="middle" dominant-baseline="middle" '
                 f'style="font-family:Rajdhani;font-weight:700;font-size:{max(18, w // 18)}px;letter-spacing:2px" fill="#5d6b63">{esc(label)}</text>')
    html_ = r.wrap(body, w, h, f'{x} {y} {w} {h}', bg)
    if recolor:
        for a, b in recolor.items():
            html_ = re.sub(a, b, html_)
    return html_, (x, y, w, h)
