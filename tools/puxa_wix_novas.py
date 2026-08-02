#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Puxa do site antigo (Wix) as matérias publicadas DEPOIS da importação grande.

O import_wix.py trouxe o acervo inteiro pela API oficial, com chave. Este aqui
serve para o rabo: as matérias que a Isabel publicou lá enquanto o site novo
era construído. Não precisa de chave nenhuma — lê o que o Wix já entrega de
graça para os buscadores:

  1. blog-posts-sitemap.xml diz quais matérias existem lá;
  2. compara com import/materias.json e separa só as que faltam;
  3. blog-feed.xml dá editoria, autor, resumo, capa e data;
  4. a página de cada matéria, pedida como buscador, vem com o texto já montado
     (o Wix só entrega o corpo no HTML quando quem pede é um robô de busca);
  5. o corpo é traduzido para o HTML limpo da casa, igual ao do resto do acervo.

Não apaga nada e não mexe no que já existe: só acrescenta.

Uso:
    python3 tools/puxa_wix_novas.py            # mostra o que falta, sem gravar
    python3 tools/puxa_wix_novas.py --gravar   # grava índice e corpos

Depois de gravar, para trazer as fotos e refazer as páginas:
    python3 tools/migra_imagens.py --reescrever
    python3 tools/build_pages.py
"""
import os, re, sys, json, html, subprocess, unicodedata
from html.parser import HTMLParser
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://www.foyer.digital'
CA = '/root/.ccr/ca-bundle.crt'
# o Wix só monta o texto no HTML quando quem pede é um buscador
ROBO = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
GRAVAR = '--gravar' in sys.argv

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
MES_EN = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
          'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def baixa(url):
    cmd = ['curl', '-s', '--max-time', '90', '-A', ROBO]
    if os.path.exists(CA):
        cmd += ['--cacert', CA]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:80]


# ------------------------------------------------------------------ o corpo
# O Wix marca cada bloco do texto com <div type="..." data-hook="rcv-blockN">,
# logo DEPOIS do bloco. Então o conteúdo de um bloco é o pedaço entre a marca
# anterior e a marca dele.
MARCA = re.compile(r'<div type="([a-z-]+)" data-hook="rcv-block([\w-]+)"></div>')
GUARDA = {'strong', 'b', 'em', 'i', 'u', 'a'}


class SoOEssencial(HTMLParser):
    """Deixa só negrito, itálico, sublinhado e link. O resto da pintura do Wix
    (dezenas de <span style>) vai embora — a casa tem o seu próprio estilo."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.pilha = []

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            return
        if tag in GUARDA:
            d = dict(attrs)
            if tag == 'a':
                href = d.get('href') or ''
                if not href or href.startswith('#'):
                    self.pilha.append(None)
                    return
                self.out.append(f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener">')
                self.pilha.append('a')
                return
            t = {'b': 'strong', 'i': 'em'}.get(tag, tag)
            self.out.append(f'<{t}>')
            self.pilha.append(t)

    def handle_endtag(self, tag):
        if tag in GUARDA and self.pilha:
            t = self.pilha.pop()
            if t:
                self.out.append(f'</{t}>')

    def handle_data(self, data):
        self.out.append(html.escape(data, quote=False))

    def texto(self):
        s = ''.join(self.out)
        s = re.sub(r'<(strong|em|u)>\s*</\1>', '', s)
        return re.sub(r'\s+', ' ', s).strip()


def limpa(trecho):
    p = SoOEssencial()
    p.feed(trecho)
    p.close()
    return p.texto()


def dentro(trecho, tags):
    """Devolve o miolo da primeira tag da lista encontrada no trecho."""
    for t in tags:
        m = re.search(r'<%s[^>]*>(.*?)</%s>' % (t, t), trecho, re.S)
        if m:
            return t, m.group(1)
    return None, ''


def media_wix(src):
    """Normaliza a foto para a mesma forma que o importador grande usou, para o
    migra_imagens.py reconhecer e baixar uma vez só."""
    m = re.search(r'static\.wixstatic\.com/media/([^/"\s]+)', src or '')
    if not m:
        return ''
    return f'https://static.wixstatic.com/media/{m.group(1)}/v1/fit/w_1200,al_c,q_85/img.jpg'


def corpo_da_pagina(pagina):
    marcas = list(MARCA.finditer(pagina))
    if not marcas:
        return ''
    saida, fim = [], 0
    for m in marcas:
        tipo, trecho, fim = m.group(1), pagina[fim:m.start()], m.end()
        if tipo in ('first', 'last', 'empty-line'):
            continue
        if tipo == 'image':
            im = re.search(r'<img[^>]+src="(https://static\.wixstatic\.com/media/[^"]+)"', trecho)
            if not im:
                continue
            cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', trecho, re.S)
            legenda = limpa(cap.group(1)) if cap else ''
            texto_legenda = re.sub(r'<[^>]+>', '', legenda)
            fc = f'<figcaption>{texto_legenda}</figcaption>' if texto_legenda else ''
            alt = html.escape(texto_legenda, quote=True)
            saida.append(f'<figure class="art-img"><img src="{media_wix(im.group(1))}" '
                         f'alt="{alt}" loading="lazy">{fc}</figure>')
            continue
        if tipo == 'heading':
            tag, miolo = dentro(trecho, ['h2', 'h3', 'h4'])
            if tag:
                t = limpa(miolo)
                if t:
                    saida.append(f'<{tag}>{t}</{tag}>')
            continue
        if tipo == 'blockquote':
            _, miolo = dentro(trecho, ['blockquote', 'p'])
            t = limpa(miolo)
            if t:
                saida.append(f'<blockquote class="pull"><p>{t}</p></blockquote>')
            continue
        if tipo in ('bulleted-list', 'ordered-list'):
            tag, miolo = dentro(trecho, ['ul', 'ol'])
            if tag:
                itens = ''.join(f'<li>{limpa(x)}</li>'
                                for x in re.findall(r'<li[^>]*>(.*?)</li>', miolo, re.S))
                if itens:
                    saida.append(f'<{tag}>{itens}</{tag}>')
            continue
        if tipo == 'divider':
            saida.append('<hr>')
            continue
        if tipo == 'paragraph':
            _, miolo = dentro(trecho, ['p'])
            t = limpa(miolo)
            if t:
                saida.append(f'<p>{t}</p>')
            continue
        if tipo == 'video':
            v = re.search(r'(?:youtu\.be/|youtube\.com/embed/|v=)([\w-]{11})', trecho)
            if v:
                saida.append(f'<div class="art-video"><iframe src="https://www.youtube.com/embed/{v.group(1)}" '
                             'title="Vídeo" loading="lazy" allowfullscreen></iframe></div>')
            continue
    return '\n'.join(saida)


# ------------------------------------------------------------------ o feed
def le_feed():
    x = baixa(f'{BASE}/blog-feed.xml')
    fichas = {}
    for b in re.findall(r'<item>(.*?)</item>', x, re.S):
        def g(t):
            m = re.search(r'<%s>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>' % (t, t), b, re.S)
            return m.group(1).strip() if m else ''
        link = g('link')
        if not link:
            continue
        cap = re.search(r'<enclosure url="([^"]+)"', b)
        fichas[slugify(unquote(link.split('/post/')[-1]))] = {
            'cat': g('category') or 'Notícia',
            'author': g('dc:creator') or 'Redação Foyer',
            'desc': html.unescape(g('description')).strip(),
            'capa': media_wix(cap.group(1)) if cap else '',
            'pub': g('pubDate'),
        }
    return fichas


def data_do_feed(pub):
    """'Sun, 02 Aug 2026 14:30:04 GMT' -> ('2026-08-02', ordenável)"""
    m = re.search(r'(\d{1,2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2})', pub or '')
    if not m:
        return '', ''
    d, mo, y, hh, mm, ss = m.groups()
    mes = MES_EN.get(mo, 1)
    return f'{y}-{mes:02d}-{int(d):02d}', f'{y}-{mes:02d}-{int(d):02d}T{hh}:{mm}:{ss}'


# ------------------------------------------------------------------ o trabalho
def main():
    caminho = f'{ROOT}/import/materias.json'
    acervo = json.load(open(caminho))
    temos = {m['slug'] for m in acervo}

    mapa = baixa(f'{BASE}/blog-posts-sitemap.xml')
    urls = re.findall(r'<loc>(.*?)</loc>', mapa)
    if not urls:
        sys.exit('não consegui ler o mapa do site antigo')
    faltam = [u for u in urls if '/post/' in u and slugify(unquote(u.split('/post/')[-1])) not in temos]
    print(f'{len(urls)} matérias no site antigo · {len(acervo)} no site novo · {len(faltam)} faltando')
    if not faltam:
        return
    fichas = le_feed()

    novas = []
    for u in faltam:
        slug = slugify(unquote(u.split('/post/')[-1]))
        pagina = baixa(u)
        ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', pagina, re.S)
        dados = {}
        if ld:
            try:
                dados = json.loads(ld.group(1))
            except Exception:
                dados = {}
        titulo = html.unescape(str(dados.get('headline') or '')).strip()
        f = fichas.get(slug, {})
        iso, quando = data_do_feed(f.get('pub'))
        if not iso:
            iso = str(dados.get('datePublished') or '')[:10]
            quando = str(dados.get('datePublished') or '')
        corpo = corpo_da_pagina(pagina)
        if not titulo or not corpo:
            print(f'  ! pulei {slug} (título ou corpo não vieram)')
            continue
        y, mo, dd = iso.split('-')
        capa = f.get('capa') or media_wix(((dados.get('image') or {}).get('url')) or '')
        desc = f.get('desc') or html.unescape(str(dados.get('description') or '')).strip()
        palavras = len(re.sub(r'<[^>]+>', ' ', corpo).split())
        novas.append({
            'ficha': {
                'title': titulo,
                'slug': slug,
                'desc': re.sub(r'\s+', ' ', desc).strip(),
                'cat': f.get('cat') or 'Notícia',
                'author': f.get('author') or str((dados.get('author') or {}).get('name') or 'Redação Foyer'),
                'date': f'{int(dd)} de {MESES[int(mo) - 1]} de {y}',
                'short': f'{dd}.{mo}',
                'iso': iso,
                'img': capa,
                'url': unquote(u),
                'min': max(2, round(palavras / 200)),
            },
            'corpo': corpo,
            'quando': quando or iso,
        })
        print(f'  {iso} · {titulo[:62]}')

    if not GRAVAR:
        print(f'\n{len(novas)} prontas. Rode de novo com --gravar para trazer.')
        return

    novas.sort(key=lambda n: n['quando'], reverse=True)
    os.makedirs(f'{ROOT}/import/corpo', exist_ok=True)
    for n in novas:
        with open(f"{ROOT}/import/corpo/{n['ficha']['slug']}.html", 'w') as fp:
            fp.write(n['corpo'])
    acervo = [n['ficha'] for n in novas] + acervo
    json.dump(acervo, open(caminho, 'w'), ensure_ascii=False, indent=0)

    busca = [{'t': p['title'], 'c': p['cat'], 'u': f"post-{p['slug']}.html"} for p in acervo]
    json.dump(busca, open(f'{ROOT}/assets/busca-index.json', 'w'), ensure_ascii=False)
    print(f'\ngravadas {len(novas)} · acervo agora com {len(acervo)}')


if __name__ == '__main__':
    main()
