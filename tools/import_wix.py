#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa todas as matérias do blog Wix do Foyer via API oficial (somente leitura).

Uso:
    WIX_API_KEY=... WIX_SITE_ID=... python3 tools/import_wix.py

Produz:
    import/wix/posts-NNN.json.gz   — backup bruto da API
    import/materias.json           — índice (título, slug, resumo, data, editoria, foto, autor)
    import/corpo/<slug>.html       — corpo de cada matéria convertido de Ricos para HTML
    assets/busca-index.json        — índice de busca de todo o acervo
"""
import os, sys, json, gzip, re, unicodedata, subprocess, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get('WIX_API_KEY')
SITE = os.environ.get('WIX_SITE_ID')
if not KEY or not SITE:
    sys.exit('defina WIX_API_KEY e WIX_SITE_ID no ambiente')

CA = '/root/.ccr/ca-bundle.crt'

def api(path, body=None):
    cmd = ['curl', '-s', '--max-time', '60', '-H', f'Authorization: {KEY}',
           '-H', f'wix-site-id: {SITE}']
    if os.path.exists(CA):
        cmd += ['--cacert', CA]
    if body is not None:
        cmd += ['-X', 'POST', '-H', 'Content-Type: application/json', '-d', json.dumps(body)]
    cmd.append(f'https://www.wixapis.com{path}')
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return json.loads(out)

# ---------------------------------------------------------------- categorias
cats = {}
cd = api('/blog/v3/categories?paging.limit=100')
for c in cd.get('categories', []):
    cats[c['id']] = c['label']
print(f'{len(cats)} categorias')

# ---------------------------------------------------------------- posts (paginado)
os.makedirs(f'{ROOT}/import/wix', exist_ok=True)
all_posts, offset, total = [], 0, None
while total is None or offset < total:
    d = api('/blog/v3/posts/query', {
        'paging': {'limit': 100, 'offset': offset},
        'fieldsets': ['RICH_CONTENT', 'URL'],
    })
    posts = d.get('posts', [])
    if not posts:
        break
    total = d['metaData']['total']
    with gzip.open(f'{ROOT}/import/wix/posts-{offset:04d}.json.gz', 'wt') as f:
        json.dump(d, f, ensure_ascii=False)
    all_posts += posts
    offset += len(posts)
    print(f'  {offset}/{total}')
print(f'{len(all_posts)} matérias baixadas')

# ---------------------------------------------------------------- autores
members = {}
def author(mid):
    if not mid:
        return 'Redação Foyer'
    if mid not in members:
        try:
            m = api(f'/members/v1/members/{mid}')
            nick = (m.get('member', {}).get('profile', {}) or {}).get('nickname') or ''
            members[mid] = nick or 'Redação Foyer'
        except Exception:
            members[mid] = 'Redação Foyer'
    return members[mid]

# ---------------------------------------------------------------- ricos -> HTML
WIXMEDIA = 'https://static.wixstatic.com/media/'

def esc(t):
    return html.escape(t, quote=False)

def text_html(node):
    t = esc(node.get('textData', {}).get('text', ''))
    link = None
    for d in node.get('textData', {}).get('decorations', []):
        k = d.get('type')
        if k == 'BOLD':
            t = f'<strong>{t}</strong>'
        elif k == 'ITALIC':
            t = f'<em>{t}</em>'
        elif k == 'UNDERLINE':
            t = f'<u>{t}</u>'
        elif k == 'LINK':
            link = ((d.get('linkData') or {}).get('link') or {}).get('url')
    if link:
        t = f'<a href="{html.escape(link)}" target="_blank" rel="noopener">{t}</a>'
    return t

def kids_html(node):
    return ''.join(text_html(n) if n.get('type') == 'TEXT' else '' for n in node.get('nodes', []))

def img_url(idv, w=1200):
    return f'{WIXMEDIA}{idv}/v1/fit/w_{w},al_c,q_85/img.jpg'

def node_html(n):
    t = n.get('type')
    if t == 'PARAGRAPH':
        inner = kids_html(n)
        return f'<p>{inner}</p>' if inner.strip() else ''
    if t == 'HEADING':
        lvl = min(max(n.get('headingData', {}).get('level', 2), 2), 4)
        return f'<h{lvl}>{kids_html(n)}</h{lvl}>'
    if t == 'IMAGE':
        img = n.get('imageData', {})
        src = (img.get('image', {}).get('src', {}) or {}).get('id')
        if not src:
            return ''
        cap = img.get('caption') or img.get('altText') or ''
        capt = f'<figcaption>{esc(cap)}</figcaption>' if cap else ''
        return (f'<figure class="art-img"><img src="{img_url(src)}" alt="{html.escape(cap or "")}" loading="lazy">{capt}</figure>')
    if t in ('BULLETED_LIST', 'ORDERED_LIST'):
        tag = 'ul' if t == 'BULLETED_LIST' else 'ol'
        lis = ''
        for li in n.get('nodes', []):
            inner = ''.join(node_html(x) for x in li.get('nodes', []))
            lis += f'<li>{inner}</li>'
        return f'<{tag}>{lis}</{tag}>'
    if t == 'BLOCKQUOTE':
        inner = ''.join(node_html(x) for x in n.get('nodes', []))
        return f'<blockquote class="pull">{inner}</blockquote>'
    if t == 'DIVIDER':
        return '<hr>'
    if t == 'VIDEO':
        v = n.get('videoData', {})
        url = ((v.get('video') or {}).get('src') or {}).get('url') or (v.get('url') or '')
        m = re.search(r'(?:youtu\.be/|v=)([\w-]{11})', str(url))
        if m:
            return (f'<div class="art-video"><iframe src="https://www.youtube.com/embed/{m.group(1)}" '
                    'title="Vídeo" loading="lazy" allowfullscreen></iframe></div>')
        return ''
    if t == 'GALLERY':
        out = ''
        for item in n.get('galleryData', {}).get('items', []):
            src = ((item.get('image') or {}).get('media') or {}).get('src', {}).get('id')
            if src:
                out += f'<figure class="art-img"><img src="{img_url(src)}" alt="" loading="lazy"></figure>'
        return out
    # tipos não mapeados são ignorados sem quebrar a matéria
    return ''

def ricos_html(rc):
    return '\n'.join(x for x in (node_html(n) for n in rc.get('nodes', [])) if x)

# ---------------------------------------------------------------- índice + corpos
MESES = ['janeiro','fevereiro','março','abril','maio','junho','julho',
         'agosto','setembro','outubro','novembro','dezembro']

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:80]

os.makedirs(f'{ROOT}/import/corpo', exist_ok=True)
seen, index = set(), []
all_posts.sort(key=lambda p: p.get('firstPublishedDate', ''), reverse=True)
for p in all_posts:
    slug = slugify(p.get('slug') or p['title']) or p['id'][:8]
    base, k = slug, 2
    while slug in seen:
        slug = f'{base}-{k}'; k += 1
    seen.add(slug)

    iso = p.get('firstPublishedDate', '')[:10]
    y, mo, dd = (iso.split('-') + ['', '', ''])[:3]
    date_pt = f'{int(dd)} de {MESES[int(mo)-1]} de {y}' if mo else ''
    short = f'{dd}.{mo}' if mo else ''

    media = ((p.get('media') or {}).get('wixMedia') or {}).get('image') or {}
    img = media.get('url') or (img_url(media['id']) if media.get('id') else '')

    cat = next((cats[c] for c in p.get('categoryIds', []) if c in cats), 'Notícia')
    corpo = ricos_html(p.get('richContent') or {})
    open(f'{ROOT}/import/corpo/{slug}.html', 'w').write(corpo)

    url = ''
    u = p.get('url') or {}
    if u:
        url = (u.get('base') or '') + (u.get('path') or '')

    index.append({
        'title': p['title'].strip(),
        'slug': slug,
        'desc': (p.get('excerpt') or '').strip(),
        'cat': cat,
        'author': author(p.get('memberId')),
        'date': date_pt, 'short': short, 'iso': iso,
        'img': img, 'url': url,
        'min': p.get('minutesToRead', 3),
    })

json.dump(index, open(f'{ROOT}/import/materias.json', 'w'), ensure_ascii=False, indent=0)

os.makedirs(f'{ROOT}/assets', exist_ok=True)
busca = [{'t': p['title'], 'c': p['cat'], 'u': f"post-{p['slug']}.html"} for p in index]
json.dump(busca, open(f'{ROOT}/assets/busca-index.json', 'w'), ensure_ascii=False)

print(f'índice: {len(index)} matérias · autores: {sorted(set(members.values()))[:6]}')
print('editorias:', sorted({p["cat"] for p in index}))
