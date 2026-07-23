#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as páginas HTML do site FOYER a partir de partials compartilhados."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- partials

import html as _html

BASE = 'https://pedrocobron-ops.github.io/FOYER.DIGITAL---SITE'

ORG_LD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
          '"@type":"NewsMediaOrganization","name":"FOYER","alternateName":"Foyer Estúdio e Comunicação",'
          f'"url":"{BASE}/","logo":"{BASE}/assets/logo/foyer-stacked-gold.png",'
          '"sameAs":["https://www.youtube.com/@Foyer.digital","https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm"]'
          '}</script>')

def head(title, desc, og_img=None, og_type='website', og_url='', ld=''):
    t = _html.escape(title, quote=True)
    d = _html.escape(desc, quote=True)
    _img_raw = og_img or f'{BASE}/assets/logo/src/foyer-banner.png'
    if not _img_raw.startswith('http'):
        _img_raw = f'{BASE}/{_img_raw}'
    img = _html.escape(_img_raw, quote=True)
    url = _html.escape(f'{BASE}/{og_url}', quote=True)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{d}">
<meta name="theme-color" content="#4E0F09">
<meta property="og:site_name" content="FOYER">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<title>{t}</title>
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="FOYER — Últimas" href="{BASE}/feed.xml">
<link rel="icon" type="image/png" href="assets/logo/foyer-icon.png">
<link rel="stylesheet" href="assets/site.css">
{ORG_LD}{ld}
</head>
<body>
'''

DEFS = '''<!-- artes de palco (placeholders de foto e capas da revista) -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <pattern id="heads" width="62" height="44" patternUnits="userSpaceOnUse">
      <circle cx="31" cy="28" r="16" fill="#170606"/>
    </pattern>
    <pattern id="bulbs" width="46" height="46" patternUnits="userSpaceOnUse">
      <circle cx="23" cy="23" r="6" fill="#CEB26A"/>
    </pattern>
    <symbol id="ph-1" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#380A06"/>
      <polygon points="300,-30 130,400 470,400" fill="#E9CB85" opacity=".2"/>
      <ellipse cx="300" cy="378" rx="160" ry="26" fill="#E9CB85" opacity=".3"/>
      <circle cx="300" cy="278" r="27" fill="#120505"/>
      <rect x="268" y="308" width="64" height="92" rx="10" fill="#120505"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-2" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#4E0F09"/>
      <rect x="18"  width="26" height="400" fill="#380A06"/><rect x="82"  width="30" height="400" fill="#380A06"/>
      <rect x="150" width="24" height="400" fill="#380A06"/><rect x="212" width="32" height="400" fill="#380A06"/>
      <rect x="286" width="26" height="400" fill="#380A06"/><rect x="348" width="30" height="400" fill="#380A06"/>
      <rect x="416" width="24" height="400" fill="#380A06"/><rect x="478" width="32" height="400" fill="#380A06"/>
      <rect x="548" width="26" height="400" fill="#380A06"/>
      <rect y="0" width="600" height="70" fill="#E9CB85" opacity=".14"/>
      <rect y="336" width="600" height="12" fill="#CEB26A" opacity=".85"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-3" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#380A06"/>
      <ellipse cx="300" cy="80" rx="330" ry="130" fill="#E9CB85" opacity=".14"/>
      <rect y="230" width="600" height="170" fill="url(#heads)"/>
      <circle cx="330" cy="258" r="16" fill="#CEB26A"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-4" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#380A06"/>
      <rect width="600" height="52" fill="url(#bulbs)" opacity=".9"/>
      <rect y="348" width="600" height="52" fill="url(#bulbs)" opacity=".9"/>
      <rect x="70" y="110" width="460" height="180" fill="none" stroke="#CEB26A" stroke-width="3"/>
      <rect x="70" y="110" width="460" height="180" fill="#E9CB85" opacity=".1"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-5" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#380A06"/>
      <rect x="96"  width="5" height="400" fill="#CEB26A" opacity=".55"/>
      <rect x="206" width="5" height="400" fill="#CEB26A" opacity=".4"/>
      <rect x="316" width="5" height="400" fill="#CEB26A" opacity=".55"/>
      <rect x="426" width="5" height="400" fill="#CEB26A" opacity=".4"/>
      <rect x="516" width="5" height="400" fill="#CEB26A" opacity=".55"/>
      <rect x="78"  y="210" width="42" height="78" fill="#CEB26A" opacity=".32"/>
      <rect x="298" y="120" width="42" height="78" fill="#CEB26A" opacity=".32"/>
      <rect x="498" y="270" width="42" height="78" fill="#CEB26A" opacity=".32"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-6" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#4E0F09"/>
      <rect x="0"   y="330" width="140" height="70" fill="#CEB26A" opacity=".8"/>
      <rect x="140" y="260" width="140" height="140" fill="#380A06"/>
      <rect x="280" y="190" width="140" height="210" fill="#CEB26A" opacity=".55"/>
      <rect x="420" y="120" width="180" height="280" fill="#380A06"/>
      <circle cx="510" cy="80" r="34" fill="#E9CB85" opacity=".7"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
  </defs>
</svg>
'''

UTIL = '''<div class="util">
  <div class="wrap">
    <span class="cell" id="today">São Paulo, BR</span>
    <span class="right">
      <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">YouTube ↗</a>
      <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Spotify ↗</a>
      <a href="revista.html#assinar">Assine</a>
      <button class="theme-btn" id="theme" aria-label="Alternar tema">Blackout</button>
    </span>
  </div>
</div>
'''

NAV_ITEMS = [
    ('index.html', 'Capa'),
    ('noticias.html', 'Notícias'),
    ('critica.html', 'Crítica'),
    ('revista.html', 'Revista'),
    ('programas.html', 'Programas'),
    ('enciclopedia.html', 'Enciclopédia'),
    ('agenda.html', 'Agenda'),
    ('entrevistas.html', 'Entrevistas'),
]

def nav(current):
    ON = ' class="on" aria-current="page"'
    links = '\n'.join(
        f'    <a href="{href}"{ON if href == current else ""}>{label}</a>'
        for href, label in NAV_ITEMS
    )
    return f'''<nav class="main" aria-label="Seções">
  <div class="row">
    <a href="index.html" class="brand" aria-label="FOYER — capa">
      <img class="only-light" src="assets/logo/foyer-stacked-wine-sm.png" alt="" width="173" height="160">
      <img class="only-dark" src="assets/logo/foyer-stacked-gold-sm.png" alt="" width="173" height="160">
    </a>
{links}
    <a href="busca.html" class="busca">⌕ Buscar</a>
  </div>
</nav>
'''

def band(kicker, h1, note):
    return f'''<header class="page-band">
  <div class="wrap">
    <span class="kicker">{kicker}</span>
    <h1>{h1}</h1>
    <p class="note">{note}</p>
  </div>
</header>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="foot-cols">
      <div class="foot-brand">
        <img class="mini-logo" src="assets/logo/foyer-stacked-gold-sm.png" alt="FOYER" width="173" height="160">
        <p>Portal de teatro, música e cultura — e um canal de programas sobre a arte de quem faz o palco.</p>
      </div>
      <div class="foot-col">
        <h4>Editorias</h4>
        <a href="noticias.html">Notícias</a>
        <a href="critica.html">Crítica</a>
        <a href="entrevistas.html">Entrevistas</a>
        <a href="agenda.html">Agenda</a>
      </div>
      <div class="foot-col">
        <h4>Programas</h4>
        <a href="programas.html">Programa do Foyer</a>
        <a href="programas.html">Críticas Teatrais · Por Bruno Cavalcanti</a>
        <a href="programas.html">Trivia Musical · Astro em Cena</a>
        <a href="programas.html">Session Musical · Coxixo de Coxia</a>
      </div>
      <div class="foot-col">
        <h4>Foyer</h4>
        <a href="revista.html">A Revista</a>
        <a href="enciclopedia.html">Enciclopédia</a>
        <a href="sobre.html">Quem somos</a>
        <a href="contato.html">Contato</a>
        <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">YouTube ↗</a>
        <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Spotify ↗</a>
        <a href="privacidade.html">Política de Privacidade</a>
      </div>
    </div>
    <div class="foot-legal">
      <span>© 2026 Foyer Estúdio e Comunicação — Todos os direitos reservados</span>
      <span>São Paulo — Brasil</span>
    </div>
  </div>
  <div class="foot-giant" aria-hidden="true">
    <img src="assets/logo/foyer-horizontal-gold.png" alt="" width="2000" height="517" loading="lazy">
  </div>
</footer>
<div class="sample-note">Protótipo de design — manchetes, fotos e dados ilustrativos</div>
<script src="assets/site.js"></script>
<script src="assets/ads.js"></script>
'''

def ph(sym, cap=True, extra='', href='materia.html'):
    c = '<span class="ph-cap">Foto — Divulgação</span>' if cap else ''
    return (f'<a class="ph" href="{href}" aria-label="Foto da matéria">'
            f'<svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>{extra}{c}</a>')

def ad(slot):
    return f'<div class="ad-slot" data-ad-slot="{slot}"></div>'

def news_cell(sym, tag, title, meta, desc=None, big=False):
    d = f'\n        <p>{desc}</p>' if desc else ''
    cap = '<span class="ph-cap">Foto — Divulgação</span>' if big else ''
    return f'''    <article class="news-cell{' big' if big else ''}">
      <a class="ph" href="materia.html" aria-label="Foto da matéria">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>{cap}
      </a>
      <div class="cbody">
        <span class="tag">{tag}</span>
        <h3><a href="materia.html">{title}</a></h3>{d}
        <div class="meta-row">
          <span class="meta-l">{meta}</span>
          <button class="share-min" data-share="native" data-title="{title}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

def page(fname, title, desc, current, body, quiet=False, og_img=None, og_type='website', ld=''):
    html = head(title, desc, og_img=og_img, og_type=og_type, og_url=fname, ld=ld) + '\n' + DEFS + '\n' + UTIL + '\n' + nav(current) + '\n' + body + '\n' + FOOTER + '</body>\n</html>\n'
    with open(os.path.join(ROOT, fname), 'w') as f:
        f.write(html)
    if not quiet:
        print('•', fname, len(html)//1024, 'KB')

# ---------------------------------------------------------------- NOTÍCIAS

noticias_body = band('Editoria', 'Notícias', 'Tudo o que acontece no teatro, na música e na cultura — atualizado o dia inteiro') + f'''
<main class="wrap">
  <div class="filters" aria-label="Filtrar por editoria">
    <a href="#" class="on">Todas</a><a href="#">Teatro</a><a href="#">Musicais</a><a href="#">Dança</a>
    <a href="#">Ópera</a><a href="#">Música</a><a href="#">Política cultural</a><a href="#">Mercado</a>
  </div>
  <div class="news-grid">
{news_cell('ph-6','Política cultural','Novo edital federal muda as regras do fomento ao teatro — entenda ponto a ponto','Análise — há 1 h','O que abre de oportunidade e onde estão as armadilhas para grupos independentes.',big=True)}
{news_cell('ph-2','Rio de Janeiro','Casa de espetáculos anuncia temporada dedicada à dramaturgia negra','há 2 h')}
{news_cell('ph-3','Circuito','Interior de SP ganha rota de festivais com curadoria compartilhada','há 3 h')}
{news_cell('ph-1','Dança','Companhia paulista leva espetáculo premiado para turnê europeia','há 4 h')}
{news_cell('ph-5','Ópera','Montagem histórica retorna ao palco 30 anos depois da estreia','há 6 h')}
{news_cell('ph-4','Musicais','Turnê nacional esgota o primeiro lote de ingressos em 40 minutos','há 7 h')}
{news_cell('ph-3','Formação','Escola livre de teatro abre 200 vagas com bolsa integral','há 8 h')}
{news_cell('ph-2','Música','Orquestra jovem abre inscrições gratuitas para instrumentistas','há 9 h')}
{news_cell('ph-5','Bastidores','A profissão invisível que desenha a luz do espetáculo','ontem')}
  </div>
  <button class="load-more" type="button">Carregar mais notícias ↓</button>
  <div class="ad-slot" data-ad-slot="1003"></div>
</main>
'''

# ---------------------------------------------------------------- CRÍTICA

def crit(sym, score, stars, title, quote, meta):
    return f'''    <article class="crit">
      <a class="ph" href="materia.html" aria-label="Foto do espetáculo">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="crit-body">
        <div class="score-row"><span class="score">{score}</span><span class="stars">{stars}</span></div>
        <h3><a href="materia.html">{title}</a></h3>
        <blockquote>{quote}</blockquote>
        <div class="meta-row">
          <span class="meta-l">{meta}</span>
          <button class="share-min" data-share="native" data-title="Crítica: {title}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

critica_body = band('Editoria', 'Crítica', 'A redação assiste, pensa e assina — sem medo de opinião') + f'''
<main class="wrap">
  <div class="crit-grid">
{crit('ph-2','9.1','★★★★★','Uma montagem que ousa reescrever o clássico — e acerta','“A leitura contemporânea encontra o texto sem trair a sua alma. É a produção mais corajosa do ano.”','Teatro — Estreia nacional')}
{crit('ph-4','7.5','★★★★☆','O musical biográfico que canta melhor do que conta','“Números musicais impecáveis sustentam uma dramaturgia que ainda tropeça no segundo ato.”','Musical — Em cartaz em SP')}
{crit('ph-1','8.4','★★★★☆','Dança-teatro que transforma o palco em campo de batalha','“Um elenco em estado de urgência. Saímos do teatro com o corpo alerta.”','Dança — Temporada curta')}
{crit('ph-5','6.8','★★★☆☆','A comédia que ri de si mesma antes do público','“Quando confia no próprio texto, funciona. Quando pisca para a plateia, perde o passo.”','Teatro — Em cartaz no RJ')}
{crit('ph-3','9.4','★★★★★','O monólogo que cala uma sala de oitocentos lugares','“Uma hora e quarenta sem respirar. Interpretação que já nasce referência.”','Teatro — Última semana')}
{crit('ph-6','8.0','★★★★☆','Ópera de câmara encontra o sertão — e o resultado é elétrico','“A partitura conversa com a rabeca como se sempre tivessem sido vizinhas.”','Ópera — Turnê nacional')}
  </div>
</main>
'''

# ---------------------------------------------------------------- ENTREVISTAS

def quote_card(sym, q, who, role):
    return f'''    <article class="quote-card">
      {ph(sym)}
      <div class="qbody">
        <p class="q">“{q}”</p>
        <span class="who">{who}</span>
        <span class="role">{role}</span>
        <div class="meta-row">
          <span class="meta-l">Entrevista</span>
          <button class="share-min" data-share="native" data-title="Entrevista: {who}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

entrevistas_body = band('Editoria', 'Entrevistas', 'Conversas longas com quem faz o palco acontecer') + f'''
<main class="wrap">
  <div class="quote-grid">
{quote_card('ph-1','O palco é o único lugar onde eu digo a verdade inteira','Marina Villas','Atriz — em cartaz com A Cidade Cantada')}
{quote_card('ph-3','O público do interior não é vitrine, é raiz','Téo Andrade','Diretor — turnê nacional 2026')}
{quote_card('ph-5','A coxia ensina mais que qualquer escola','Bia Camargo','Desenhista de luz — 34 produções')}
{quote_card('ph-2','Musical brasileiro não é tradução, é invenção','Lúcia Ferrante','Coreógrafa e pesquisadora')}
{quote_card('ph-4','Rir é o jeito mais rápido de falar sério','Rafael Doming','Ator e comediante')}
{quote_card('ph-6','Produzir cultura no Brasil é um ato de teimosia','Helena Prado','Produtora executiva')}
  </div>
</main>
'''

# ---------------------------------------------------------------- AGENDA

def agd(day, month, what, meta, tag):
    return f'''    <a class="agd-row" href="espetaculo.html">
      <span class="agd-date"><b>{day}</b><small>{month}</small></span>
      <span class="agd-what"><h3>{what}</h3><span class="agd-meta">{meta}</span></span>
      <span class="tag agd-tag">{tag}</span>
    </a>'''

agenda_body = band('Serviço', 'Agenda', 'O que estreia, o que sai de cartaz e o que não dá para perder') + f'''
<main class="wrap">
  <div class="agd">
{agd('24','Jul — Sex','Estreia: A Cidade Cantada','Theatro Municipal — São Paulo · 21h','Musical')}
{agd('25','Jul — Sáb','Última sessão: Noturno','Teatro de Câmara — Rio de Janeiro · 20h','Teatro')}
{agd('26','Jul — Dom','Circuito de teatro de rua ocupa o centro','Praça das Artes — São Paulo · 15h · Grátis','Rua')}
{agd('29','Jul — Qua','Abertura do Festival de Inverno','Palácio das Artes — Belo Horizonte · 19h','Festival')}
{agd('31','Jul — Sex','Cabaré do Fim do Mundo — temporada nova','Teatro Oficina — São Paulo · 22h','Cabaré')}
{agd('02','Ago — Dom','Ópera de câmara no sertão — turnê','Teatro José de Alencar — Fortaleza · 19h','Ópera')}
{agd('05','Ago — Qua','Trivia Musical — gravação com plateia','Estúdio Foyer — São Paulo · 20h','Foyer')}
{agd('08','Ago — Sáb','Mostra de dança contemporânea','Teatro Riachuelo — Natal · 21h','Dança')}
  </div>
</main>
'''

# ---------------------------------------------------------------- PROGRAMAS

def epis(sym, epn, title, meta):
    return f'''    <article class="ep-cell">
      <a class="ph" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener" aria-label="Assistir episódio">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>
        <span class="play">▶</span>
      </a>
      <div class="ep-body">
        <span class="meta-l">{epn}</span>
        <h3>{title}</h3>
        <div class="meta-row">
          <span class="meta-l">{meta}</span>
          <button class="share-min" data-share="native" data-title="{title}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

programas_body = band('O canal', 'Os Programas', 'YouTube &amp; Spotify — novos episódios toda semana') + f'''
<section class="programas first">
  <div class="wrap">
    <div class="prog-grid" style="margin-top:40px">
      <a class="show" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">
        <span class="ep">Talk — Bastidores</span><span class="tri">▶</span>
        <h3>Programa do Foyer</h3>
        <p>Conversas com elencos e os bastidores do teatro musical.</p>
      </a>
      <a class="show" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">
        <span class="ep">Game show</span><span class="tri">▶</span>
        <h3>Trivia Musical</h3>
        <p>Artistas duelam no universo dos musicais. Quem sabe mais?</p>
      </a>
      <a class="show" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">
        <span class="ep">Papo — Astrologia</span><span class="tri">▶</span>
        <h3>Astro em Cena</h3>
        <p>Astrologia e artes em conversas cheias de insights.</p>
      </a>
      <a class="show" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">
        <span class="ep">Economia criativa</span><span class="tri">▶</span>
        <h3>Off Stage</h3>
        <p>Tudo o que move a cultura fora dos palcos.</p>
      </a>
      <a class="show" href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">
        <span class="ep">Coxia — Humor</span><span class="tri">▶</span>
        <h3>Coxixo de Coxia</h3>
        <p>O papo solto de quem vive o teatro por trás da cortina.</p>
      </a>
    </div>
    <div class="prog-cta">
      <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">Assistir no YouTube ↗</a>
      <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Ouvir no Spotify ↗</a>
    </div>
  </div>
</section>
<main class="wrap">
  <div class="sec-head">
    <h2>Últimos episódios</h2>
    <span class="note">Direto do canal</span>
    <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener" class="all">Ver no YouTube ↗</a>
  </div>
  <div class="ep-grid">
{epis('ph-1','Programa do Foyer — EP 087','O elenco de A Cidade Cantada abre o jogo sobre a criação','Esta semana')}
{epis('ph-4','Trivia Musical — EP 042','Duelo: quem sabe mais sobre musicais nacionais?','Esta semana')}
{epis('ph-3','Astro em Cena — EP 035','O mapa astral dos grandes estreantes da temporada','Há 1 semana')}
{epis('ph-5','Off Stage — EP 029','Quanto custa manter um teatro aberto no Brasil','Há 1 semana')}
{epis('ph-2','Coxixo de Coxia — EP 051','Histórias que a cortina não deixou o público ver','Há 2 semanas')}
{epis('ph-6','Programa do Foyer — EP 086','A nova geração da direção musical brasileira','Há 2 semanas')}
  </div>
</main>
'''

# ---------------------------------------------------------------- ENCICLOPÉDIA

def erow(nm, of, ct):
    return f'''    <a class="ency-row" href="artista.html" role="row">
      <span class="nm">{nm}</span><span class="of">{of}</span><span class="ct">{ct}</span><span class="ar">→</span>
    </a>'''

enciclopedia_body = band('Projeto Foyer', 'Enciclopédia do Teatro Musical Brasileiro', 'Memória viva — cada nome clicável leva à trajetória completa') + f'''
<main class="wrap">
  <div class="ency-stats">
    <div class="stat"><span class="n" data-v="312">0</span><span class="l">Espetáculos</span></div>
    <div class="stat"><span class="n" data-v="1240">0</span><span class="l">Artistas &amp; equipes</span></div>
    <div class="stat"><span class="n" data-v="96">0</span><span class="l">Teatros mapeados</span></div>
  </div>
  <form class="ency-search" onsubmit="return false;">
    <input type="search" placeholder="Busque por artista, espetáculo, teatro ou função…" aria-label="Buscar na enciclopédia">
    <button type="submit">Buscar</button>
  </form>
  <div class="ency-table" role="table" aria-label="Índice de artistas">
    <div class="ency-row head" role="row">
      <span>Nome</span><span class="of">Ofício</span><span class="ct">Produções</span><span class="ar"></span>
    </div>
{erow('Marina Villas','Atriz · Diretora musical','012')}
{erow('Téo Andrade','Diretor · Dramaturgo','021')}
{erow('Lúcia Ferrante','Coreógrafa','017')}
{erow('Rafael Doming','Ator · Cantor','009')}
{erow('Bia Camargo','Desenhista de luz','034')}
{erow('Helena Prado','Produtora executiva','026')}
{erow('Caio Bezerra','Diretor musical · Arranjador','019')}
{erow('Duda Marinho','Atriz · Bailarina','011')}
{erow('Otávio Lins','Cenógrafo','023')}
{erow('Sofia Rezende','Figurinista','028')}
  </div>
  <div class="ency-note">
    <span>Fase 2 — banco de dados completo com ficha técnica de cada produção</span>
    <a href="mailto:contato@foyer.digital?subject=Sugest%C3%A3o%20de%20verbete" class="go">Sugerir um verbete →</a>
  </div>
</main>
'''

# ---------------------------------------------------------------- REVISTA

def ed_card(sym, num, date, title, sum_, cover_title):
    return f'''    <article class="ed-card">
      <a class="ed-cover" href="#" data-open-reader aria-label="Ler a edição {num}">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>
        <span class="m">
          <img src="assets/logo/foyer-stacked-gold-sm.png" alt="FOYER">
          <span>Edição {num}<br>{date}</span>
        </span>
        <span class="t">{cover_title}</span>
      </a>
      <div class="ed-body">
        <span class="meta-l"><b>Edição {num}</b> — {date}</span>
        <p class="sum">{sum_}</p>
        <div class="ed-actions">
          <button class="go" data-open-reader type="button">Ler online</button>
          <button class="pdf" type="button" disabled title="Disponível na versão final">PDF — em breve</button>
        </div>
      </div>
    </article>'''

revista_body = band('Newsletter semanal', 'A Revista do Foyer', 'Toda sexta, uma edição fechada — como uma revista impressa, para ler na tela ou baixar') + f'''
<main class="wrap">
  <div class="rev-hero" id="assinar">
    <div class="rev-copy">
      <h2>Uma revista de verdade, entregue toda sexta</h2>
      <p>A semana do teatro brasileiro editada com começo, meio e fim: reportagem de capa, críticas da semana, agenda comentada e os bastidores dos programas — diagramada como uma revista impressa.</p>
      <div class="feats">
        <span>Edição fechada semanal — sem rolagem infinita</span>
        <span>Leia no site como revista ou baixe o PDF</span>
        <span>Grátis no seu e-mail, toda sexta às 7h</span>
      </div>
    </div>
    <form class="signup-card" id="signup">
      <h3>Receba a revista</h3>
      <input type="text" placeholder="Seu nome" aria-label="Seu nome" required>
      <input type="email" placeholder="seu@email.com" aria-label="Seu e-mail" required>
      <button type="submit">Assinar grátis</button>
      <span class="ok" id="signup-ok">Pronto! Você está na lista da próxima edição ✓</span>
      <span class="fine">Sem spam. Cancele quando quiser.</span>
    </form>
  </div>

  <div class="sec-head">
    <h2>Edições anteriores</h2>
    <span class="note">Arquivo completo — uma por semana</span>
  </div>
  <div class="ed-grid">
{ed_card('ph-1','Nº 214','17 Jul 2026','O ano do musical brasileiro','Reportagem de capa sobre a dramaturgia nacional, 3 críticas, agenda de 12 estreias.','O ano do musical brasileiro')}
{ed_card('ph-2','Nº 213','10 Jul 2026','Atrás da cortina','A economia invisível da coxia: quem sustenta o espetáculo quando a luz apaga.','Atrás da cortina')}
{ed_card('ph-3','Nº 212','03 Jul 2026','A plateia voltou','Os números da retomada: ocupação recorde nas casas de espetáculo do país.','A plateia voltou')}
{ed_card('ph-4','Nº 211','26 Jun 2026','Letreiro aceso','Especial: os 10 teatros históricos que voltaram à ativa na última década.','Letreiro aceso')}
{ed_card('ph-5','Nº 210','19 Jun 2026','Ofícios do palco','Da contrarregragem ao desenho de som: os ofícios que ninguém aplaude de pé.','Ofícios do palco')}
{ed_card('ph-6','Nº 209','12 Jun 2026','Degraus','Formação teatral no Brasil: onde estudar, quanto custa, quem está subindo.','Degraus')}
  </div>
</main>

<!-- leitor da revista -->
<div class="reader" id="reader" role="dialog" aria-modal="true" aria-label="Leitor da revista">
  <div class="pg capa on">
    <img src="assets/logo/foyer-stacked-gold.png" alt="FOYER">
    <span class="ed-n">Edição Nº 214 — 17 de julho de 2026</span>
    <h2>O ano do musical brasileiro</h2>
    <span class="ed-n">Reportagem de capa · Crítica · Agenda</span>
  </div>
  <div class="pg">
    <div class="folio"><span>Foyer — Edição Nº 214</span><span>Sumário</span></div>
    <h3>Nesta edição</h3>
    <ul class="sumario">
      <li><span>Carta da redação — o palco como praça</span><span class="n">02</span></li>
      <li><span>Capa: o ano do musical brasileiro</span><span class="n">04</span></li>
      <li><span>Crítica: três estreias, três veredictos</span><span class="n">09</span></li>
      <li><span>Entrevista: Marina Villas abre o jogo</span><span class="n">12</span></li>
      <li><span>Agenda comentada da semana</span><span class="n">15</span></li>
      <li><span>Coxia: o que a cortina escondeu</span><span class="n">18</span></li>
    </ul>
  </div>
  <div class="pg">
    <div class="folio"><span>Reportagem de capa</span><span>04</span></div>
    <h3>O ano do musical brasileiro</h3>
    <div class="cols">
      <p class="drop">Durante décadas, o musical brasileiro viveu de licenças: títulos da Broadway traduzidos, coreografias importadas quadro a quadro, cenografias replicadas sob contrato. A temporada que agora se encerra virou essa página. Das vinte maiores bilheterias do ano, catorze são de dramaturgia original — número impensável há dez anos.</p>
      <p>A virada não aconteceu por acaso. Uma geração inteira de autores, arranjadores e diretores formada nos cursos livres dos anos 2010 chegou à maturidade criativa ao mesmo tempo em que o público demonstrou apetite por histórias com sotaque próprio.</p>
      <p>Os produtores ouvidos pela redação apontam o mesmo dado: o espectador que antes comprava o selo internacional hoje compra o tema — e quer se ver no palco. O resultado está nas casas lotadas e nas filas de espera por ingressos de última hora.</p>
      <p>O desafio da próxima temporada é de fôlego: transformar o momento em movimento, e o movimento em mercado permanente.</p>
    </div>
  </div>
  <div class="pg capa">
    <img src="assets/logo/foyer-stacked-gold.png" alt="FOYER">
    <span class="ed-n">Até sexta que vem</span>
    <h2>A próxima edição já está sendo escrita</h2>
    <span class="ed-n">foyer.digital — São Paulo, Brasil</span>
  </div>
  <div class="reader-ctrl">
    <button type="button" id="rd-prev">← Anterior</button>
    <span id="rd-count">1 / 4</span>
    <button type="button" id="rd-next">Próxima →</button>
    <button type="button" id="rd-close">Fechar ✕</button>
  </div>
</div>

<script>
// leitor da revista — paginação simples
(function(){{
  var reader = document.getElementById('reader');
  var pages = reader.querySelectorAll('.pg');
  var count = document.getElementById('rd-count');
  var i = 0;
  function show(n){{
    i = Math.max(0, Math.min(pages.length - 1, n));
    pages.forEach ? null : null;
    for(var k = 0; k < pages.length; k++) pages[k].classList.toggle('on', k === i);
    count.textContent = (i + 1) + ' / ' + pages.length;
  }}
  document.addEventListener('click', function(e){{
    if(e.target.closest('[data-open-reader]')){{ e.preventDefault(); reader.classList.add('open'); show(0); }}
  }});
  document.getElementById('rd-prev').addEventListener('click', function(){{ show(i - 1); }});
  document.getElementById('rd-next').addEventListener('click', function(){{ show(i + 1); }});
  document.getElementById('rd-close').addEventListener('click', function(){{ reader.classList.remove('open'); }});
  document.addEventListener('keydown', function(e){{
    if(!reader.classList.contains('open')) return;
    if(e.key === 'Escape') reader.classList.remove('open');
    if(e.key === 'ArrowRight') show(i + 1);
    if(e.key === 'ArrowLeft') show(i - 1);
  }});
}})();
// cadastro (demo local até o backend entrar)
(function(){{
  var f = document.getElementById('signup');
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    try{{ localStorage.setItem('foyer-newsletter', f.querySelector('input[type=email]').value); }}catch(err){{}}
    document.getElementById('signup-ok').style.display = 'block';
    f.querySelector('button').textContent = 'Assinado ✓';
  }});
}})();
</script>
'''

# ---------------------------------------------------------------- CAPA (index)

index_body = '''<!-- ===================== TICKER ===================== -->
<div class="ticker" aria-label="Últimas notícias">
  <div class="ticker-inner">
    <div class="ticker-seq">
      <span><b>Últimas</b> Musical brasileiro anuncia turnê em 12 capitais</span>
      <span>Edital federal destina R$ 180 mi às artes cênicas</span>
      <span>Prêmio de teatro divulga os finalistas de 2026</span>
      <span>Estreia: a ópera que reabre o teatro histórico do centro</span>
      <span>Festival de Curitiba confirma datas da próxima edição</span>
    </div>
    <div class="ticker-seq" aria-hidden="true">
      <span><b>Últimas</b> Musical brasileiro anuncia turnê em 12 capitais</span>
      <span>Edital federal destina R$ 180 mi às artes cênicas</span>
      <span>Prêmio de teatro divulga os finalistas de 2026</span>
      <span>Estreia: a ópera que reabre o teatro histórico do centro</span>
      <span>Festival de Curitiba confirma datas da próxima edição</span>
    </div>
  </div>
</div>

<!-- ===================== MASTHEAD ===================== -->
<header class="masthead">
  <div class="wrap">
    <div class="mast-side left">
      <span class="ln">Edição Nº 214</span>
      <span>Ano I — Diária</span>
      <span>Teatro · Música · Cultura</span>
    </div>
    <a class="logo-link" href="index.html" aria-label="FOYER — voltar à capa">
      <img class="logo-img" src="assets/logo/foyer-stacked-gold.png" alt="FOYER" width="518" height="480">
    </a>
    <div class="mast-side right">
      <span class="ln">São Paulo — Brasil</span>
      <span>Portal + Canal</span>
      <span>foyer.digital</span>
    </div>
    <div class="mast-tagline">O saguão do teatro brasileiro</div>
  </div>
</header>
'''

# nota: o masthead vem ANTES da nav na capa; o gerador da capa monta na ordem certa
index_main = '''<main>
<section class="frontpage wrap">
  <div class="fp-grid">
    <article class="manchete">
      <a class="ph cover" href="materia.html" aria-label="Foto da reportagem de capa">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#ph-1"/></svg>
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="manchete-body">
        <div class="tags">
          <span class="tag wine">Em cartaz</span>
          <span class="tag">Reportagem de capa</span>
        </div>
        <h1><a href="materia.html">A temporada em que o musical brasileiro decidiu contar as próprias histórias</a></h1>
        <p class="dek">De biografias a fábulas urbanas, as grandes produções da estação abandonam a tradução literal da Broadway para inventar uma dramaturgia com sotaque nacional — e o público respondeu lotando as casas.</p>
        <div class="share-row" aria-label="Compartilhar esta matéria">
          <button class="sbtn" data-share="whats" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">WhatsApp</button>
          <button class="sbtn" data-share="x" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">X / Twitter</button>
          <button class="sbtn" data-share="face" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">Facebook</button>
          <button class="sbtn" data-share="copy" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">Copiar link</button>
        </div>
        <div class="foot">
          <span>Por Redação Foyer — 8 min de leitura</span>
          <a href="materia.html" class="ler">Ler a reportagem →</a>
        </div>
      </div>
    </article>

    <aside class="giro" aria-label="Notícias em tempo real">
      <div class="giro-head">
        <span class="live"><span class="dot"></span> O Giro</span>
        <span>Atualizado agora</span>
      </div>
      <div class="giro-list">
        <a class="giro-item" href="materia.html"><span class="t">14:20</span><span class="h">Turnê nacional esgota o primeiro lote em 40 minutos</span></a>
        <a class="giro-item" href="materia.html"><span class="t">13:05</span><span class="h">Diretora brasileira é convidada para festival em Avignon</span></a>
        <a class="giro-item" href="materia.html"><span class="t">11:48</span><span class="h">Teatro histórico do centro reabre após cinco anos de restauro</span></a>
        <a class="giro-item" href="materia.html"><span class="t">10:31</span><span class="h">Musical infantil ganha sessão com acessibilidade em Libras</span></a>
        <a class="giro-item" href="materia.html"><span class="t">09:56</span><span class="h">Elenco da nova montagem é anunciado; ensaios começam em agosto</span></a>
        <a class="giro-item" href="materia.html"><span class="t">09:12</span><span class="h">Prêmio da crítica divulga a lista de finalistas do ano</span></a>
        <a class="giro-item" href="materia.html"><span class="t">08:40</span><span class="h">Circuito de teatro de rua ocupa o centro neste fim de semana</span></a>
      </div>
      <a class="giro-more" href="noticias.html">+ 32 notícias hoje →</a>
    </aside>
  </div>

  <div class="fp-sub">
    <article>
      <a class="ph" href="materia.html" aria-label="Foto da matéria">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#ph-5"/></svg>
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="sub-body">
        <span class="num">002 — Bastidores</span>
        <h3><a href="materia.html">A profissão invisível que desenha a luz do espetáculo</a></h3>
        <p>Um ofício que decide o que a plateia enxerga — e o que não.</p>
        <div class="meta-row">
          <span class="meta-l">há 3 h</span>
          <button class="share-min" data-share="native" data-title="A profissão invisível que desenha a luz do espetáculo">Compartilhar ↗</button>
        </div>
      </div>
    </article>
    <article>
      <a class="ph" href="#" aria-label="Foto da matéria">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#ph-4"/></svg>
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="sub-body">
        <span class="num">003 — Mercado</span>
        <h3><a href="materia.html">Quanto custa montar um musical no Brasil em 2026</a></h3>
        <p>Planilhas abertas: produtores detalham o caminho do dinheiro.</p>
        <div class="meta-row">
          <span class="meta-l">há 5 h</span>
          <button class="share-min" data-share="native" data-title="Quanto custa montar um musical no Brasil em 2026">Compartilhar ↗</button>
        </div>
      </div>
    </article>
    <article>
      <a class="ph" href="#" aria-label="Foto da matéria">
        <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#ph-3"/></svg>
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="sub-body">
        <span class="num">004 — Perfil</span>
        <h3><a href="materia.html">A atriz que trocou a televisão pelo teatro de câmara</a></h3>
        <p>Sobre risco, silêncio e o que sobra depois dos aplausos.</p>
        <div class="meta-row">
          <span class="meta-l">ontem</span>
          <button class="share-min" data-share="native" data-title="A atriz que trocou a televisão pelo teatro de câmara">Compartilhar ↗</button>
        </div>
      </div>
    </article>
  </div>
</section>

<!-- ===================== NOTÍCIAS ===================== -->
<section id="noticias" class="wrap">
  <div class="sec-head">
    <h2>Notícias</h2>
    <span class="note">Edição de hoje — 24 publicadas</span>
    <a href="noticias.html" class="all">Ver todas →</a>
  </div>
  <div class="news-grid">
''' + news_cell('ph-6','Política cultural','Novo edital federal muda as regras do fomento ao teatro — entenda ponto a ponto','Análise — há 1 h','O que abre de oportunidade e onde estão as armadilhas para grupos independentes.',big=True) + '\n' + \
news_cell('ph-2','Rio de Janeiro','Casa de espetáculos anuncia temporada dedicada à dramaturgia negra','há 2 h') + '\n' + \
news_cell('ph-3','Circuito','Interior de SP ganha rota de festivais com curadoria compartilhada','há 3 h') + '\n' + \
news_cell('ph-1','Dança','Companhia paulista leva espetáculo premiado para turnê europeia','há 4 h') + '\n' + \
news_cell('ph-5','Ópera','Montagem histórica retorna ao palco 30 anos depois da estreia','há 6 h') + '''
  </div>
  <div class="ad-slot" data-ad-slot="1001"></div>
</section>

<!-- ===================== CRÍTICA ===================== -->
<section id="critica" class="wrap">
  <div class="sec-head">
    <h2>Crítica</h2>
    <span class="note">Em vídeo, por Kyra Piscitelli — os espetáculos em cartaz</span>
    <a href="critica.html" class="all">Todas as críticas →</a>
  </div>
  <div class="ep-grid">
__CRITICA_CAPA__
  </div>
  <div class="ad-slot" data-ad-slot="1002"></div>
</section>

<!-- ===================== PROGRAMAS ===================== -->
<section id="programas" class="programas">
  <div class="wrap">
    <div class="sec-head">
      <h2>Os Programas</h2>
      <span class="note">YouTube &amp; Spotify — novos episódios toda semana</span>
    </div>
    <div class="prog-grid">
      <a class="show" href="programas.html">
        <span class="ep">Talk — Bastidores</span><span class="tri">▶</span>
        <h3>Programa do Foyer</h3>
        <p>Conversas com elencos e os bastidores do teatro musical.</p>
      </a>
      <a class="show" href="programas.html">
        <span class="ep">Game show</span><span class="tri">▶</span>
        <h3>Trivia Musical</h3>
        <p>Artistas duelam no universo dos musicais. Quem sabe mais?</p>
      </a>
      <a class="show" href="programas.html">
        <span class="ep">Papo — Astrologia</span><span class="tri">▶</span>
        <h3>Astro em Cena</h3>
        <p>Astrologia e artes em conversas cheias de insights.</p>
      </a>
      <a class="show" href="programas.html">
        <span class="ep">Economia criativa</span><span class="tri">▶</span>
        <h3>Off Stage</h3>
        <p>Tudo o que move a cultura fora dos palcos.</p>
      </a>
      <a class="show" href="programas.html">
        <span class="ep">Coxia — Humor</span><span class="tri">▶</span>
        <h3>Coxixo de Coxia</h3>
        <p>O papo solto de quem vive o teatro por trás da cortina.</p>
      </a>
    </div>
    <div class="prog-cta">
      <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">Assistir no YouTube ↗</a>
      <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Ouvir no Spotify ↗</a>
    </div>
  </div>
</section>

<!-- ===================== ENCICLOPÉDIA ===================== -->
<section id="enciclopedia" class="wrap">
  <div class="sec-head">
    <h2>Enciclopédia do Teatro Musical Brasileiro</h2>
    <span class="note">Memória viva — em catalogação</span>
    <a href="enciclopedia.html" class="all">Explorar →</a>
  </div>
  <div class="ency-stats">
    <div class="stat"><span class="n" data-v="312">0</span><span class="l">Espetáculos</span></div>
    <div class="stat"><span class="n" data-v="1240">0</span><span class="l">Artistas &amp; equipes</span></div>
    <div class="stat"><span class="n" data-v="96">0</span><span class="l">Teatros mapeados</span></div>
  </div>
  <div class="ency-table" role="table" aria-label="Índice de artistas">
    <div class="ency-row head" role="row">
      <span>Nome</span><span class="of">Ofício</span><span class="ct">Produções</span><span class="ar"></span>
    </div>
''' + erow('Marina Villas','Atriz · Diretora musical','012') + '\n' + \
erow('Téo Andrade','Diretor · Dramaturgo','021') + '\n' + \
erow('Lúcia Ferrante','Coreógrafa','017') + '\n' + \
erow('Bia Camargo','Desenhista de luz','034') + '''
  </div>
  <div class="ency-note">
    <span>Clique em qualquer nome e veja a trajetória inteira — cada papel, cada ficha técnica</span>
    <a href="enciclopedia.html" class="go">Explorar a enciclopédia →</a>
  </div>
</section>
</main>

<!-- ===================== REVISTA ===================== -->
<section class="news-bar">
  <div class="wrap">
    <h2>A Revista do Foyer — toda sexta no seu e-mail</h2>
    <div class="go-rev">
      <a href="revista.html">Conhecer &amp; assinar →</a>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- COXIA (admin)

coxia_body = open(os.path.join(ROOT, 'tools/coxia_body.html'), encoding='utf-8').read()

# ---------------------------------------------------------------- MATÉRIA (modelo)

materia_body = '''<main class="wrap">
<article class="art">
  <div class="art-head">
    <div class="tags">
      <span class="tag wine">Em cartaz</span>
      <span class="tag">Reportagem de capa</span>
    </div>
    <h1>A temporada em que o musical brasileiro decidiu contar as próprias histórias</h1>
    <div class="art-byline">
      <span>Por <b>Redação Foyer</b> — São Paulo</span>
      <span>22.07.2026 · 8 min de leitura</span>
    </div>
    <div class="share-row" aria-label="Compartilhar esta matéria">
      <button class="sbtn" data-share="whats" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">WhatsApp</button>
      <button class="sbtn" data-share="x" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">X / Twitter</button>
      <button class="sbtn" data-share="face" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">Facebook</button>
      <button class="sbtn" data-share="copy" data-title="A temporada em que o musical brasileiro decidiu contar as próprias histórias">Copiar link</button>
    </div>
  </div>
  <figure class="art-cover">
    <span class="ph"><svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#ph-1"/></svg></span>
    <figcaption>O elenco no ensaio aberto da nova temporada — Foto: Divulgação</figcaption>
  </figure>
  <div class="ad-slot" data-ad-slot="2001"></div>
  <div class="art-body">
    <p class="drop">Durante décadas, o musical brasileiro viveu de licenças: títulos da Broadway traduzidos, coreografias importadas quadro a quadro, cenografias replicadas sob contrato. A temporada que agora se encerra virou essa página.</p>
    <h2>O público comprou o tema</h2>
    <p>Os produtores ouvidos pela redação apontam o mesmo dado: o espectador que antes comprava o selo internacional hoje compra o tema — e quer se ver no palco.</p>
    <blockquote class="pull">“O espectador que antes comprava o selo internacional hoje compra o tema — e quer se ver no palco.”</blockquote>
    <div class="ad-slot" data-ad-slot="2002"></div>
    <p>O desafio da próxima temporada: transformar o momento em movimento, e o movimento em mercado permanente.</p>
  </div>
  <div class="art-foot">
    <div class="tags"><span class="tag">Teatro musical</span><span class="tag">Mercado</span></div>
  </div>
</article>
<section>
  <div class="sec-head">
    <h2>Leia também</h2>
    <span class="note">Da mesma editoria</span>
  </div>
  <div class="news-grid three">
''' + news_cell('ph-5','Bastidores','A profissão invisível que desenha a luz do espetáculo','há 3 h') + '\n' + \
news_cell('ph-4','Mercado','Quanto custa montar um musical no Brasil em 2026','há 5 h') + '\n' + \
news_cell('ph-3','Perfil','A atriz que trocou a televisão pelo teatro de câmara','ontem') + '''
  </div>
  <div class="ad-slot" data-ad-slot="2003"></div>
</section>
</main>
'''

# ---------------------------------------------------------------- ARTISTA (verbete)

def credit(prod, fn, teatro, ano):
    return f'''    <a class="ency-row four" href="espetaculo.html" role="row">
      <span class="nm">{prod}</span><span class="of">{fn}</span><span class="of">{teatro}</span><span class="ct">{ano}</span>
    </a>'''

artista_body = band('Enciclopédia — Verbete', 'Marina Villas', 'Atriz · Cantora · Diretora musical — São Paulo, SP') + '''
<main class="wrap">
  <div class="ency-stats">
    <div class="stat"><span class="n" data-v="12">0</span><span class="l">Produções</span></div>
    <div class="stat"><span class="n" data-v="15">0</span><span class="l">Anos de carreira</span></div>
    <div class="stat"><span class="n" data-v="3">0</span><span class="l">Prêmios</span></div>
  </div>
  <div class="sec-head">
    <h2>Trajetória</h2>
    <span class="note">Cada espetáculo é clicável — siga o fio</span>
  </div>
  <div class="ency-table" role="table" aria-label="Produções de Marina Villas">
    <div class="ency-row head four" role="row">
      <span>Espetáculo</span><span class="of">Função</span><span class="of">Teatro</span><span class="ct">Ano</span>
    </div>
''' + credit('A Cidade Cantada','Protagonista','Theatro Municipal — SP','2025') + '\n' + \
credit('Rua de Baixo, o Musical','Direção musical','Teatro Porto — SP','2024') + '\n' + \
credit('Noturno','Elenco','Teatro de Câmara — RJ','2023') + '\n' + \
credit('Cabaré do Fim do Mundo','Solista','Teatro Oficina — SP','2022') + '''
  </div>
  <div class="ad-slot" data-ad-slot="3001"></div>
</main>
'''

# ---------------------------------------------------------------- ESPETÁCULO

def ficha(fn, nome):
    return f'''    <a class="ency-row" href="artista.html" role="row">
      <span class="of">{fn}</span><span class="nm">{nome}</span><span class="ct"></span><span class="ar">→</span>
    </a>'''

espetaculo_body = band('Enciclopédia — Espetáculo', 'A Cidade Cantada', 'Musical original — 2025 · Theatro Municipal, São Paulo') + '''
<main class="wrap">
  <div class="sec-head">
    <h2>Ficha técnica</h2>
    <span class="note">Cada nome é clicável — veja a trajetória completa</span>
  </div>
  <div class="ency-table" role="table" aria-label="Ficha técnica">
    <div class="ency-row head" role="row">
      <span class="of">Função</span><span>Nome</span><span class="ct"></span><span class="ar"></span>
    </div>
''' + ficha('Protagonista','Marina Villas') + '\n' + \
ficha('Direção','Téo Andrade') + '\n' + \
ficha('Coreografia','Lúcia Ferrante') + '\n' + \
ficha('Desenho de luz','Bia Camargo') + '\n' + \
ficha('Direção musical','Caio Bezerra') + '''
  </div>
  <div class="ad-slot" data-ad-slot="3002"></div>
</main>
'''

# ---------------------------------------------------------------- BUSCA

busca_body = band('Ferramenta', 'Buscar', 'Todo o acervo do Foyer — 1.514 matérias, artistas e espetáculos') + '''
<main class="wrap">
  <form class="ency-search" style="border-top:var(--b); margin-top:26px" onsubmit="return false;">
    <input type="search" id="q" placeholder="Digite: espetáculo, artista, teatro…" aria-label="Buscar no site" autofocus>
    <button type="submit">Buscar</button>
  </form>
  <div class="ency-table" id="res" aria-live="polite"></div>
  <p class="meta-l" style="display:block; padding:18px 4px" id="busca-info">Carregando o índice do acervo…</p>
</main>
<script>
(function(){
  var IDX = [];
  var info = document.getElementById('busca-info');
  fetch('assets/busca-index.json').then(function(r){ return r.json(); }).then(function(d){
    IDX = d;
    info.textContent = IDX.length.toLocaleString('pt-BR') + ' matérias no acervo — digite para buscar';
  }).catch(function(){ info.textContent = 'Não foi possível carregar o índice.'; });
  var q = document.getElementById('q'), res = document.getElementById('res');
  function norm(s){ return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,''); }
  function render(){
    var v = norm(q.value.trim());
    if(v.length < 2){ res.innerHTML=''; return; }
    var hits = [];
    for(var i=0; i<IDX.length && hits.length<40; i++){
      if(norm(IDX[i].t + ' ' + IDX[i].c).indexOf(v) !== -1) hits.push(IDX[i]);
    }
    res.innerHTML = hits.length
      ? hits.map(function(i){ return '<a class="ency-row" href="'+i.u+'"><span class="nm">'+i.t+'</span><span class="of">'+i.c+'</span><span class="ct"></span><span class="ar">→</span></a>'; }).join('')
      : '<div class="ency-row"><span class="of">Nada encontrado</span></div>';
  }
  q.addEventListener('input', render);
})();
</script>
'''

# ---------------------------------------------------------------- PRIVACIDADE

privacidade_body = band('Institucional', 'Política de Privacidade', 'Última atualização — julho de 2026') + '''
<main class="wrap">
  <div class="legal">
    <h2>Quem somos</h2>
    <p>O FOYER (foyer.digital) é um portal de jornalismo cultural dedicado ao teatro, à música e às artes no Brasil, com sede em São Paulo, SP.</p>
    <h2>Dados que coletamos</h2>
    <p>Coletamos apenas os dados necessários para operar o site: o e-mail e o nome informados voluntariamente no cadastro da newsletter, e dados anônimos de navegação usados para melhorar o conteúdo.</p>
    <h2>Newsletter</h2>
    <p>O e-mail cadastrado é usado exclusivamente para o envio da Revista do Foyer. Não vendemos nem compartilhamos a lista com terceiros. Todo envio traz um link de cancelamento imediato.</p>
    <h2>Cookies e publicidade</h2>
    <p>O site exibe anúncios fornecidos por terceiros, incluindo o Google AdSense. Esses serviços podem usar cookies para exibir anúncios baseados em visitas anteriores. Você pode desativar a publicidade personalizada nas <a href="https://adssettings.google.com" target="_blank" rel="noopener">configurações de anúncios do Google</a>.</p>
    <h2>Seus direitos (LGPD)</h2>
    <p>Nos termos da Lei nº 13.709/2018, você pode solicitar a qualquer momento o acesso, a correção ou a exclusão dos seus dados pessoais pelo e-mail de contato abaixo.</p>
    <h2>Contato</h2>
    <p>Dúvidas sobre esta política: <b>contato@foyer.digital</b></p>
  </div>
</main>
'''

# ---------------------------------------------------------------- MATÉRIAS REAIS (importadas do Wix)
import json as _json, re as _re
from datetime import datetime, timezone

MATERIAS = _json.load(open(os.path.join(ROOT, 'import/materias.json')))

# ---- matérias criadas na Coxia (publica as que chegaram na hora marcada)
_MESES_PT = ['janeiro','fevereiro','março','abril','maio','junho','julho',
             'agosto','setembro','outubro','novembro','dezembro']

def md_lite(txt):
    """Formato simples da Coxia -> HTML: parágrafos, ## intertítulo,
    > citação, **negrito**, *itálico*, [texto](url), img:URL | legenda"""
    import html as _h
    out = []
    for bloco in _re.split(r'\n\s*\n', txt.strip()):
        b = bloco.strip()
        if not b:
            continue
        if b.startswith('img:'):
            resto = b[4:].strip()
            url, _, cap = resto.partition('|')
            capt = f'<figcaption>{_h.escape(cap.strip())}</figcaption>' if cap.strip() else ''
            out.append(f'<figure class="art-img"><img src="{_h.escape(url.strip())}" alt="" loading="lazy">{capt}</figure>')
            continue
        if b.startswith('## '):
            out.append(f'<h2>{_h.escape(b[3:].strip())}</h2>')
            continue
        e = _h.escape(b)
        e = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', e)
        e = _re.sub(r'\*(.+?)\*', r'<em>\1</em>', e)
        e = _re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', e)
        e = _re.sub(r'\[(.+?)\]\(((?:post-|pessoa-|cat-)[a-z0-9-]+\.html)\)', r'<a href="\2">\1</a>', e)
        e = e.replace('\n', '<br>')
        if b.startswith('&gt; ') or b.startswith('> '):
            e = _re.sub(r'^(&gt;|>)\s*', '', e)
            out.append(f'<blockquote class="pull">{e}</blockquote>')
        else:
            out.append(f'<p>{e}</p>')
    return '\n'.join(out)

_novas_dir = os.path.join(ROOT, 'import/novas')
_agendadas = 0
if os.path.isdir(_novas_dir):
    _agora = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.join(ROOT, 'import/corpo'), exist_ok=True)
    _novas = []
    for _f in sorted(os.listdir(_novas_dir)):
        if not _f.endswith('.json'):
            continue
        try:
            _n = _json.load(open(os.path.join(_novas_dir, _f)))
        except Exception:
            continue
        _pub = _n.get('publishAt') or ''
        if _pub and _pub > _agora:
            _agendadas += 1
            continue
        _slug = _n['slug']
        _corpo = md_lite(_n.get('corpo', ''))
        open(os.path.join(ROOT, 'import/corpo', _slug + '.html'), 'w').write(_corpo)
        _txt = _re.sub(r'<[^>]+>', '', _corpo)
        _desc = (_re.sub(r'\s+', ' ', _txt).strip()[:230] or _n.get('title',''))
        _iso = (_pub or _agora)[:10]
        _y, _mo, _dd = _iso.split('-')
        _novas.append({
            'title': _n['title'], 'slug': _slug, 'desc': _desc,
            'cat': _n.get('cat', 'Notícia'), 'author': _n.get('author', 'Redação Foyer'),
            'date': f'{int(_dd)} de {_MESES_PT[int(_mo)-1]} de {_y}',
            'short': f'{_dd}.{_mo}', 'iso': _iso,
            'img': _n.get('img', ''), 'credito': _n.get('imgCredito', ''),
            'atualizado': _n.get('atualizadoEm', ''),
            'evento': _n.get('evento') or None,
            'url': '', 'min': max(1, len(_txt)//1100),
        })
    if _novas:
        _slugs_novos = {x['slug'] for x in _novas}
        MATERIAS = [_m for _m in MATERIAS if _m['slug'] not in _slugs_novos]
        MATERIAS = sorted(_novas + MATERIAS, key=lambda x: x.get('iso',''), reverse=True)
        print(f'• {len(_novas)} matéria(s) da Coxia no ar · {_agendadas} agendada(s) aguardando')
    elif _agendadas:
        print(f'• {_agendadas} matéria(s) agendada(s) aguardando a hora')

_MES_N = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
          'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

def short_date(p):
    return p.get('short', '')

def safe(t):
    return t.replace('"', '”')

def wiximg(url, w=1200, h=675):
    if 'static.wixstatic.com/media/' in url and '/v1/' not in url:
        return f'{url}/v1/fill/w_{w},h_{h},al_c,q_82/cover.jpg'
    return url

def real_ph(p, href, cap=True):
    c = '<span class="ph-cap">Foto — Divulgação</span>' if cap else ''
    return (f'<a class="ph" href="{href}" aria-label="Foto da matéria">'
            f'<img src="{wiximg(p["img"], 800, 450)}" alt="{safe(p["title"])}" loading="lazy" onerror="this.style.display=\'none\'">{c}</a>')

def real_cell(p, big=False):
    d = f'\n        <p>{p["desc"][:160]}…</p>' if big else ''
    href = 'post-' + p['slug'] + '.html'
    return f'''    <article class="news-cell{' big' if big else ''}" data-cat="{p['cat']}">
      {real_ph(p, href, cap=big)}
      <div class="cbody">
        <span class="tag">{p['cat']}</span>
        <h3><a href="{href}">{p['title']}</a></h3>{d}
        <div class="meta-row">
          <span class="meta-l">{short_date(p)} — {p['author']}</span>
          <button class="share-min" data-share="native" data-title="{safe(p['title'])}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

# --- ticker com manchetes reais
_tk = ''.join(f'<span>{p["title"]}</span>\n      ' for p in MATERIAS[:5])
TICKER = f'''<div class="ticker" aria-label="Últimas notícias">
  <div class="ticker-inner">
    <div class="ticker-seq">
      <span><b>Últimas</b> {MATERIAS[0]['title']}</span>
      {''.join(f'<span>{p["title"]}</span>' for p in MATERIAS[1:5])}
    </div>
    <div class="ticker-seq" aria-hidden="true">
      <span><b>Últimas</b> {MATERIAS[0]['title']}</span>
      {''.join(f'<span>{p["title"]}</span>' for p in MATERIAS[1:5])}
    </div>
  </div>
</div>'''

# --- capa com conteúdo real
_p0 = MATERIAS[0]
_sub_cards = ''
for _i, _p in enumerate(MATERIAS[1:4]):
    _href = 'post-' + _p['slug'] + '.html'
    _sub_cards += f'''    <article>
      {real_ph(_p, _href)}
      <div class="sub-body">
        <span class="num">00{_i+2} — {_p['cat']}</span>
        <h3><a href="{_href}">{_p['title']}</a></h3>
        <p>{_p['desc'][:120]}…</p>
        <div class="meta-row">
          <span class="meta-l">{short_date(_p)}</span>
          <button class="share-min" data-share="native" data-title="{safe(_p['title'])}">Compartilhar ↗</button>
        </div>
      </div>
    </article>
'''

_giro = ''.join(
    f'''        <a class="giro-item" href="post-{p['slug']}.html"><span class="t">{short_date(p)}</span><span class="h">{p['title']}</span></a>\n'''
    for p in MATERIAS[4:11])

index_body = TICKER + '''

<!-- ===================== MASTHEAD ===================== -->
<header class="masthead">
  <div class="wrap">
    <div class="mast-side left">
      <span class="ln">Edição de hoje</span>
      <span>Diária — desde 2023</span>
      <span>Teatro · Música · Cultura</span>
    </div>
    <a class="logo-link" href="index.html" aria-label="FOYER — voltar à capa">
      <img class="logo-img" src="assets/logo/foyer-stacked-gold.png" alt="FOYER" width="518" height="480">
    </a>
    <div class="mast-side right">
      <span class="ln">São Paulo — Brasil</span>
      <span>Portal + Canal</span>
      <span>foyer.digital</span>
    </div>
    <div class="mast-tagline">O saguão do teatro brasileiro</div>
  </div>
</header>
'''

index_main = f'''<main>
<section class="frontpage wrap">
  <div class="fp-grid">
    <article class="manchete">
      <a class="ph cover" href="post-{_p0['slug']}.html" aria-label="Foto da reportagem de capa">
        <img src="{wiximg(_p0['img'])}" alt="" loading="eager" onerror="this.style.display='none'">
        <span class="ph-cap">Foto — Divulgação</span>
      </a>
      <div class="manchete-body">
        <div class="tags">
          <span class="tag wine">{_p0['cat']}</span>
          <span class="tag">Manchete</span>
        </div>
        <h1><a href="post-{_p0['slug']}.html">{_p0['title']}</a></h1>
        <p class="dek">{_p0['desc']}</p>
        <div class="share-row" aria-label="Compartilhar esta matéria">
          <button class="sbtn" data-share="whats" data-title="{safe(_p0['title'])}">WhatsApp</button>
          <button class="sbtn" data-share="x" data-title="{safe(_p0['title'])}">X / Twitter</button>
          <button class="sbtn" data-share="face" data-title="{safe(_p0['title'])}">Facebook</button>
          <button class="sbtn" data-share="copy" data-title="{safe(_p0['title'])}">Copiar link</button>
        </div>
        <div class="foot">
          <span>Por {_p0['author']} — {_p0['date']}</span>
          <a href="post-{_p0['slug']}.html" class="ler">Ler a matéria →</a>
        </div>
      </div>
    </article>

    <aside class="giro" aria-label="Últimas matérias">
      <div class="giro-head">
        <span class="live"><span class="dot"></span> O Giro</span>
        <span>Últimas do Foyer</span>
      </div>
      <div class="giro-list">
{_giro}      </div>
      <a class="giro-more" href="noticias.html">Todas as matérias →</a>
    </aside>
  </div>

  <div class="fp-sub">
{_sub_cards}  </div>
</section>

<!-- ===================== NOTÍCIAS ===================== -->
<section id="noticias" class="wrap">
  <div class="sec-head">
    <h2>Notícias</h2>
    <span class="note">Direto da redação</span>
    <a href="noticias.html" class="all">Ver todas →</a>
  </div>
  <div class="news-grid">
{real_cell(MATERIAS[4], big=True)}
{real_cell(MATERIAS[5])}
{real_cell(MATERIAS[6])}
{real_cell(MATERIAS[7])}
{real_cell(MATERIAS[8])}
  </div>
  <div class="ad-slot" data-ad-slot="1001"></div>
</section>

<!-- ===================== CRÍTICA ===================== -->
<section id="critica" class="wrap">
  <div class="sec-head">
    <h2>Crítica</h2>
    <span class="note">Em vídeo, por Kyra Piscitelli — os espetáculos em cartaz</span>
    <a href="critica.html" class="all">Todas as críticas →</a>
  </div>
  <div class="ep-grid">
__CRITICA_CAPA__
  </div>
  <div class="ad-slot" data-ad-slot="1002"></div>
</section>

<!-- ===================== PROGRAMAS ===================== -->
<section id="programas" class="programas">
  <div class="wrap">
    <div class="sec-head">
      <h2>Os Programas</h2>
      <span class="note">YouTube &amp; Spotify — novos episódios toda semana</span>
    </div>
    <div class="prog-grid">
__PROGRAMAS_CAPA__
    </div>
    <div class="prog-cta">
      <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">Assistir no YouTube ↗</a>
      <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Ouvir no Spotify ↗</a>
    </div>
  </div>
</section>

<!-- ===================== ENCICLOPÉDIA ===================== -->
<section id="enciclopedia" class="wrap">
  <div class="sec-head">
    <h2>Enciclopédia do FOYER</h2>
    <span class="note">Toda pessoa que passa pelo FOYER, com histórico completo</span>
    <a href="enciclopedia.html" class="all">Explorar →</a>
  </div>
__ENCICLOPEDIA_CAPA__
  <div class="ency-note">
    <span>Clique em qualquer nome e veja a trajetória inteira no FOYER — matérias e programas</span>
    <a href="enciclopedia.html" class="go">Explorar a enciclopédia →</a>
  </div>
</section>
</main>

<!-- ===================== REVISTA ===================== -->
<section class="news-bar">
  <div class="wrap">
    <h2>A Revista do Foyer — toda sexta no seu e-mail</h2>
    <div class="go-rev">
      <a href="revista.html">Conhecer &amp; assinar →</a>
    </div>
  </div>
</section>
'''

# --- notícias paginadas (24 por página) + páginas por editoria
POR_PAGINA = 24

def _cat_slug(c):
    import unicodedata as _u
    x = _u.normalize('NFKD', c).encode('ascii','ignore').decode()
    return _re.sub(r'[^a-zA-Z0-9]+','-',x).strip('-').lower()

_cats = []
for _p in MATERIAS:
    if _p['cat'] not in _cats:
        _cats.append(_p['cat'])

def _filters(active='*'):
    out = f'<a href="noticias.html"{" class=on" if active=="*" else ""}>Todas</a>'
    for c in sorted(_cats):
        cls = ' class="on"' if active == c else ''
        out += f'<a href="cat-{_cat_slug(c)}.html"{cls}>{c}</a>'
    return out

def _pager(base, page, pages):
    if pages <= 1: return ''
    def href(n): return f'{base}.html' if n == 1 else f'{base}-p{n}.html'
    items = ''
    if page > 1: items += f'<a href="{href(page-1)}">← Anterior</a>'
    shown = sorted(set([1,2] + [page-1,page,page+1] + [pages-1,pages]))
    last = 0
    for n in shown:
        if n < 1 or n > pages: continue
        if last and n > last+1: items += '<span>…</span>'
        cls = ' class="on"' if n == page else ''
        items += f'<a href="{href(n)}"{cls}>{n}</a>'
        last = n
    if page < pages: items += f'<a href="{href(page+1)}">Próxima →</a>'
    return f'<nav class="pager" aria-label="Páginas">{items}</nav>'

def listing_body(posts, page, pages, base, titulo, nota, active='*'):
    ini = (page-1)*POR_PAGINA
    chunk = posts[ini:ini+POR_PAGINA]
    grid = real_cell(chunk[0], big=True) + '\n' + '\n'.join(real_cell(x) for x in chunk[1:]) if chunk else ''
    return band('Editoria', titulo, nota) + f"""
<main class="wrap">
  <div class="filters" aria-label="Filtrar por editoria">
    {_filters(active)}
  </div>
  <div class="news-grid">
{grid}
  </div>
  {_pager(base, page, pages)}
  <div class="ad-slot" data-ad-slot="1003"></div>
</main>
"""

# --- uma página por matéria (corpo completo importado do Wix)
def selo_atualizada(p):
    iso = p.get('atualizado', '')
    if not iso:
        return ''
    try:
        from zoneinfo import ZoneInfo as _ZI
        _upd = datetime.fromisoformat(iso).astimezone(_ZI('America/Sao_Paulo'))
        if _upd.strftime('%Y-%m-%d') <= (p.get('iso') or '9999'):
            return ''
    except Exception:
        pass
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.fromisoformat(iso).astimezone(ZoneInfo('America/Sao_Paulo'))
        quando = dt.strftime('%d/%m/%Y às %Hh%M')
    except Exception:
        quando = iso[:10]
    return ('\n    <div style="font-family:var(--mono);font-size:.6rem;font-weight:600;'
            'letter-spacing:.14em;text-transform:uppercase;color:var(--wine);'
            'border:1.5px solid var(--gold);background:var(--paper-2);display:inline-block;'
            f'padding:7px 12px;margin-top:10px">✎ Matéria atualizada em {quando}</div>')

def post_page(i, p):
    _sps = globals().get('POR_MATERIA', {}).get(p['slug'], [])
    _pes = globals().get('PESSOAS', {})
    quem_bloco = ''
    _chips = ''.join(f'<a class="tag" href="pessoa-{s}.html">{_pes[s]["nome"]}</a>'
                     for s in _sps[:14] if s in _pes)
    if _chips:
        quem_bloco = ('<div class="art-foot" style="border-top:1px solid var(--line);padding-top:16px">'
                      '<div class="tags" style="align-items:center">'
                      '<span class="tag wine">Quem aparece nesta matéria</span>' + _chips + '</div></div>')
    corpo_path = os.path.join(ROOT, 'import/corpo', p['slug'] + '.html')
    corpo = open(corpo_path).read() if os.path.exists(corpo_path) else f"<p>{p['desc']}</p>"
    rel = [x for x in MATERIAS if x['cat'] == p['cat'] and x['slug'] != p['slug']][:3]
    if len(rel) < 3:
        rel += [x for x in MATERIAS if x['slug'] != p['slug'] and x not in rel][:3-len(rel)]
    rel_cells = '\n'.join(real_cell(r) for r in rel)
    return f"""<main class="wrap">
<article class="art">
  <div class="art-head">
    <div class="tags">
      <span class="tag wine">{p['cat']}</span>
      <span class="tag">Foyer</span>
    </div>
    <h1>{p['title']}</h1>
    <div class="art-byline">
      <span>Por <b>{p['author']}</b></span>
      <span>{p['date']} · {p['min']} min de leitura</span>
    </div>{selo_atualizada(p)}
    <div class="share-row" aria-label="Compartilhar esta matéria">
      <button class="sbtn" data-share="whats" data-title="{safe(p['title'])}">WhatsApp</button>
      <button class="sbtn" data-share="x" data-title="{safe(p['title'])}">X / Twitter</button>
      <button class="sbtn" data-share="face" data-title="{safe(p['title'])}">Facebook</button>
      <button class="sbtn" data-share="copy" data-title="{safe(p['title'])}">Copiar link</button>
    </div>
  </div>

  <figure class="art-cover">
    <span class="ph"><img src="{wiximg(p['img'])}" alt="{safe(p['title'])}" loading="eager" onerror="this.style.display='none'"></span>
    <figcaption>{safe(p.get('credito') or 'Foto: Divulgação')}</figcaption>
  </figure>

  <div class="ad-slot" data-ad-slot="2001"></div>

  <div class="art-body">
{corpo}
  </div>

  {quem_bloco}
  <div class="art-foot">
    <div class="tags"><span class="tag">{p['cat']}</span><span class="tag">{p['author']}</span></div>
    <div class="share-row" aria-label="Compartilhar">
      <button class="sbtn" data-share="whats" data-title="{safe(p['title'])}">WhatsApp</button>
      <button class="sbtn" data-share="copy" data-title="{safe(p['title'])}">Copiar link</button>
    </div>
  </div>
</article>

<section>
  <div class="sec-head">
    <h2>Leia também</h2>
    <span class="note">Mais de {p['cat']}</span>
  </div>
  <div class="news-grid three">
{rel_cells}
  </div>
  <div class="ad-slot" data-ad-slot="2003"></div>
</section>
</main>
"""

# ---------------------------------------------------------------- REVISTA (edições reais)
import html as _html

def _rvesc(s):
    return _html.escape(str(s or ''))

EDICOES = []
_ed_dir = os.path.join(ROOT, 'import/revista/edicoes')
if os.path.isdir(_ed_dir):
    for _f in sorted(os.listdir(_ed_dir)):
        if _f.endswith('.json'):
            try:
                EDICOES.append(_json.load(open(os.path.join(_ed_dir, _f))))
            except Exception:
                pass
EDICOES.sort(key=lambda e: e.get('numero', 0), reverse=True)
ED_PUB = [e for e in EDICOES if e.get('status') == 'publicada']

_RV_CSS = '''<style>
.rv-stage{ max-width:900px; margin:26px auto 90px; padding:0 16px; }
.rv-pg{ display:none; border:2.5px solid var(--ink); background:var(--paper); min-height:74vh;
  position:relative; overflow:hidden; animation:rvin .3s ease; }
.rv-pg.on{ display:block; }
@keyframes rvin{ from{ opacity:0; transform:translateX(14px);} to{ opacity:1; transform:none;} }
.rv-rotulo{ display:inline-block; font-family:var(--mono); font-size:.58rem; font-weight:600;
  letter-spacing:.22em; text-transform:uppercase; border:1.5px solid var(--ink); padding:6px 12px;
  margin-bottom:18px; background:var(--gold); color:var(--wine); }
.rv-pad{ padding:clamp(22px,5vw,52px); }
.rv-pg h3{ font-family:var(--didone); font-weight:400; font-size:clamp(1.6rem,3.6vw,2.6rem);
  line-height:1.05; margin:0 0 18px; }
.rv-pg .art-body p{ margin:0 0 14px; line-height:1.85; }
.rv-capa{ background:var(--wine); color:var(--gold); }
.rv-capa .rv-capa-top{ display:flex; justify-content:space-between; align-items:center; gap:12px;
  padding:18px 24px; border-bottom:1.5px solid var(--gold); font-family:var(--mono); font-size:.6rem;
  letter-spacing:.2em; text-transform:uppercase; flex-wrap:wrap; }
.rv-capa img.rv-capa-img{ width:100%; max-height:44vh; object-fit:cover; display:block;
  border-bottom:1.5px solid var(--gold); }
.rv-capa .rv-manchete{ font-family:var(--didone); font-weight:400;
  font-size:clamp(2rem,5.4vw,3.6rem); line-height:.98; padding:26px 24px 8px; margin:0; }
.rv-capa .rv-chamadas{ list-style:none; margin:0; padding:10px 24px 28px; }
.rv-capa .rv-chamadas li{ font-family:var(--mono); font-size:.72rem; letter-spacing:.08em;
  text-transform:uppercase; padding:9px 0; border-top:1px solid rgba(206,178,106,.35); }
.rv-img{ width:100%; max-height:46vh; object-fit:cover; display:block; border-bottom:2px solid var(--ink); }
.rv-cred{ position:absolute; right:0; top:0; background:var(--ink); color:var(--gold);
  font-family:var(--mono); font-size:.52rem; letter-spacing:.1em; text-transform:uppercase; padding:5px 10px; }
.rv-cartaz{ display:flex; flex-direction:column; }
.rv-cartaz img{ width:100%; flex:1; object-fit:contain; background:var(--paper-2); max-height:64vh; }
.rv-cartaz .rv-leg{ padding:16px 22px; border-top:2px solid var(--ink); font-family:var(--mono);
  font-size:.66rem; letter-spacing:.1em; text-transform:uppercase; }
.rv-citacao{ background:var(--wine); color:var(--gold); display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center; padding:8vh 8vw; }
.rv-citacao .fr{ font-family:var(--didone); font-size:clamp(1.6rem,4.4vw,3rem); line-height:1.15; }
.rv-citacao .au{ font-family:var(--mono); font-size:.64rem; letter-spacing:.2em;
  text-transform:uppercase; margin-top:26px; }
.rv-ass{ font-family:var(--mono); font-size:.66rem; letter-spacing:.14em; text-transform:uppercase;
  margin-top:26px; }
.rv-leia{ display:inline-block; margin-top:18px; border:2px solid var(--wine); background:var(--wine);
  color:var(--gold); text-decoration:none; font-family:var(--mono); font-weight:600; font-size:.62rem;
  letter-spacing:.16em; text-transform:uppercase; padding:12px 18px; }
.rv-leia:hover{ background:var(--gold); color:var(--wine); border-color:var(--gold); }
.rv-nav{ position:sticky; bottom:18px; display:flex; justify-content:center; gap:8px; margin-top:18px; }
.rv-nav button{ border:2px solid var(--ink); background:var(--paper); color:var(--ink); cursor:pointer;
  font-family:var(--mono); font-weight:600; font-size:.66rem; letter-spacing:.12em;
  text-transform:uppercase; padding:13px 18px; }
.rv-nav button:hover{ background:var(--ink); color:var(--gold); }
.rv-nav .ct{ border:2px solid var(--ink); background:var(--gold); color:var(--wine);
  font-family:var(--mono); font-weight:600; font-size:.66rem; letter-spacing:.12em; padding:13px 16px; }
.rv-pat{ outline:6px double var(--gold); outline-offset:-14px; }
@media print{
  .rv-pg{ display:block !important; min-height:96vh; page-break-after:always; border-width:0 0 2px; }
  .rv-nav, nav.main, .ticker, footer, .warn{ display:none !important; }
}
</style>'''

def _rv_pagina(pg, ed):
    t = pg.get('tipo', 'livre')
    if t == 'editorial':
        return ('<div class="rv-pad"><span class="rv-rotulo">Editorial</span>'
                f'<h3>{_rvesc(pg.get("titulo"))}</h3>'
                f'<div class="art-body">{md_lite(pg.get("texto",""))}</div>'
                f'<p class="rv-ass">— {_rvesc(pg.get("assinatura") or "A direção do FOYER")}</p></div>')
    if t == 'materia':
        img = f'<img class="rv-img" src="{_rvesc(wiximg(pg.get("img",""), 1200, 500))}" alt="" onerror="this.style.display=\'none\'">' if pg.get('img') else ''
        return (img + '<div class="rv-pad">'
                f'<span class="rv-rotulo">{_rvesc(pg.get("cat") or "Na semana do FOYER")}</span>'
                f'<h3>{_rvesc(pg.get("titulo"))}</h3>'
                f'<div class="art-body"><p>{_rvesc(pg.get("chamada",""))}</p>{md_lite(pg.get("texto",""))}</div>'
                + (f'<a class="rv-leia" href="post-{_rvesc(pg.get("slug"))}.html">Leia a matéria completa no site →</a>' if pg.get('slug') else '')
                + '</div>')
    if t == 'exclusiva':
        cred = f'<span class="rv-cred">{_rvesc(pg.get("imgCredito"))}</span>' if pg.get('imgCredito') else ''
        img = f'{cred}<img class="rv-img" src="{_rvesc(pg.get("img",""))}" alt="" onerror="this.style.display=\'none\'">' if pg.get('img') else ''
        return (img + '<div class="rv-pad"><span class="rv-rotulo">Exclusivo da revista</span>'
                f'<h3>{_rvesc(pg.get("titulo"))}</h3>'
                f'<div class="art-body">{md_lite(pg.get("texto",""))}</div></div>')
    if t in ('cartaz', 'patrocinio'):
        rot = 'Publicidade' if t == 'patrocinio' else 'Divulgação'
        leg = _rvesc(pg.get('legenda', ''))
        img = f'<img src="{_rvesc(pg.get("img",""))}" alt="{leg}">'
        if pg.get('link'):
            img = f'<a href="{_rvesc(pg["link"])}" target="_blank" rel="noopener sponsored">{img}</a>'
        klass = 'rv-cartaz rv-pat' if t == 'patrocinio' else 'rv-cartaz'
        return (f'<div class="{klass}" style="min-height:74vh">{img}'
                f'<div class="rv-leg">{rot}{" — " + leg if leg else ""}</div></div>')
    if t == 'citacao':
        return ('<div class="rv-citacao">'
                f'<div class="fr">“{_rvesc(pg.get("frase"))}”</div>'
                f'<div class="au">{_rvesc(pg.get("autor",""))}</div></div>')
    if t == 'expediente':
        try:
            _eq = _json.load(open(os.path.join(ROOT, 'import/equipe.json'))).get('usuarios', [])
        except Exception:
            _eq = []
        nomes = ''.join(f'<li>{_rvesc(u["nome"])} — {"Direção" if u.get("papel")=="chefe" else "Redação"}</li>' for u in _eq)
        return ('<div class="rv-pad"><span class="rv-rotulo">Expediente</span>'
                '<h3>FOYER — jornalismo de cultura</h3>'
                f'<div class="art-body"><ul style="list-style:none;padding:0;line-height:2.4">{nomes}</ul>'
                '<p>Matérias assinadas como Redação Foyer podem contar com apuração assistida por '
                'inteligência artificial, sempre revisadas e aprovadas por um editor humano.</p>'
                f'<p>foyer.digital — edição nº {_rvesc(pg.get("numero",""))}</p></div></div>')
    # livre
    return ('<div class="rv-pad">'
            + (f'<span class="rv-rotulo">{_rvesc(pg.get("rotulo"))}</span>' if pg.get('rotulo') else '')
            + f'<h3>{_rvesc(pg.get("titulo",""))}</h3>'
            f'<div class="art-body">{md_lite(pg.get("texto",""))}</div></div>')

def edicao_page(ed):
    capa = ed.get('capa', {})
    cimg = f'<img class="rv-capa-img" src="{_rvesc(capa.get("img",""))}" alt="" onerror="this.style.display=\'none\'">' if capa.get('img') else ''
    chamadas = ''.join(f'<li>{_rvesc(c)}</li>' for c in (capa.get('chamadas') or []) if c.strip())
    pgs = [(
        '<section class="rv-pg rv-capa on">'
        '<div class="rv-capa-top"><span>A Revista do FOYER</span>'
        f'<span>Nº {_rvesc(ed.get("numero"))} — {_rvesc(ed.get("dataEdicao",""))}</span></div>'
        + cimg +
        f'<h2 class="rv-manchete">{_rvesc(capa.get("manchete") or ed.get("titulo",""))}</h2>'
        f'<ul class="rv-chamadas">{chamadas}</ul></section>'
    )]
    for pg in ed.get('paginas', []):
        pg = dict(pg); pg.setdefault('numero', ed.get('numero'))
        pgs.append(f'<section class="rv-pg">{_rv_pagina(pg, ed)}</section>')
    corpo = '\n'.join(pgs)
    total = len(pgs)
    return (_RV_CSS + f'''
<main class="rv-stage">
{corpo}
  <div class="rv-nav">
    <button type="button" id="rv-ant">← Anterior</button>
    <span class="ct" id="rv-ct">1 / {total}</span>
    <button type="button" id="rv-prox">Próxima →</button>
    <button type="button" onclick="window.print()" title="Imprimir ou salvar em PDF">⤓ PDF</button>
  </div>
</main>
<script>
(function(){{
  var pgs = document.querySelectorAll('.rv-pg'), i = 0;
  function vai(n){{
    i = Math.max(0, Math.min(pgs.length - 1, n));
    pgs.forEach(function(p, k){{ p.classList.toggle('on', k === i); }});
    document.getElementById('rv-ct').textContent = (i + 1) + ' / ' + pgs.length;
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}
  document.getElementById('rv-ant').addEventListener('click', function(){{ vai(i - 1); }});
  document.getElementById('rv-prox').addEventListener('click', function(){{ vai(i + 1); }});
  document.addEventListener('keydown', function(e){{
    if(e.key === 'ArrowRight') vai(i + 1);
    if(e.key === 'ArrowLeft') vai(i - 1);
  }});
  var x0 = null;
  document.addEventListener('touchstart', function(e){{ x0 = e.touches[0].clientX; }}, {{passive:true}});
  document.addEventListener('touchend', function(e){{
    if(x0 == null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if(Math.abs(dx) > 60) vai(dx < 0 ? i + 1 : i - 1);
    x0 = null;
  }}, {{passive:true}});
}})();
</script>''')

def revista_listagem():
    if ED_PUB:
        cards = ''
        for e in ED_PUB:
            capa = e.get('capa', {})
            img = (f'<img src="{_rvesc(capa.get("img",""))}" alt="" loading="lazy" '
                   'style="width:100%;aspect-ratio:3/4;object-fit:cover;display:block" '
                   'onerror="this.style.display=\'none\'">') if capa.get('img') else \
                  '<div style="aspect-ratio:3/4;background:var(--wine);display:flex;align-items:center;justify-content:center"><span style="font-family:var(--didone);color:var(--gold);font-size:3rem">FOY<br>ER</span></div>'
            cards += f'''
    <a href="revista-ed-{e.get("numero")}.html" style="border:2px solid var(--ink);text-decoration:none;color:var(--ink);display:block;background:var(--paper)">
      {img}
      <div style="padding:14px 16px;border-top:2px solid var(--ink)">
        <span style="font-family:var(--mono);font-size:.58rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft)">Nº {e.get("numero")} — {_rvesc(e.get("dataEdicao",""))}</span>
        <span style="display:block;font-family:var(--didone);font-size:1.3rem;line-height:1.1;margin-top:6px">{_rvesc(capa.get("manchete") or e.get("titulo",""))}</span>
      </div>
    </a>'''
        grade = f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px">{cards}\n  </div>'
    else:
        prox = EDICOES[0].get('numero') if EDICOES else 1
        grade = (f'<div style="border:2px dashed var(--line);padding:34px;text-align:center;'
                 'font-family:var(--mono);font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)">'
                 f'A edição Nº {prox} está em produção na redação — assine acima para receber em primeira mão</div>')
    return grade

revista_body = band('Newsletter semanal', 'A Revista do Foyer',
                    'Toda sexta, uma edição fechada — como uma revista impressa, para ler na tela ou baixar') + f'''
<main class="wrap">
  <div class="rev-hero" id="assinar">
    <div class="rev-copy">
      <h2>Uma revista de verdade, entregue toda sexta</h2>
      <p>A semana do teatro brasileiro editada com começo, meio e fim: reportagem de capa, o melhor da semana do site, conteúdo exclusivo, cartazes e agenda — diagramada como uma revista impressa.</p>
      <div class="feats">
        <span>Edição fechada semanal — sem rolagem infinita</span>
        <span>Leia no site como revista ou baixe o PDF</span>
        <span>Grátis no seu e-mail, toda sexta às 7h</span>
      </div>
    </div>
    <form class="signup-card" id="signup">
      <h3>Receba a revista</h3>
      <input type="text" placeholder="Seu nome" aria-label="Seu nome" required>
      <input type="email" placeholder="seu@email.com" aria-label="Seu e-mail" required>
      <button type="submit">Assinar grátis</button>
      <span class="ok" id="signup-ok">Pronto! Você está na lista da próxima edição ✓</span>
      <span class="fine">Sem spam. Cancele quando quiser.</span>
    </form>
  </div>

  <div class="sec-head">
    <h2>Edições</h2>
    <span class="note">Fechadas na Coxia, uma por semana</span>
  </div>
  {revista_listagem()}
  <div class="ad-slot" data-ad-slot="1301"></div>
</main>
'''

# ---------------------------------------------------------------- ENCICLOPÉDIA (pessoas do acervo)
try:
    ENC = _json.load(open(os.path.join(ROOT, 'import/enciclopedia.json')))
except Exception:
    ENC = {'pessoas': {}, 'porMateria': {}, 'porVideo': {}}
PESSOAS = ENC.get('pessoas', {})
POR_MATERIA = ENC.get('porMateria', {})
POR_VIDEO = ENC.get('porVideo', {})

_PAPEL_ROT = {'autor': 'Assina', 'citado': 'Citado(a)', 'convidado': 'Convidado(a)', 'apresenta': 'Apresenta'}

def _papeis_resumo(aps):
    ps = {a['papel'] for a in aps}
    out = []
    if 'autor' in ps: out.append('assina no FOYER')
    if 'apresenta' in ps: out.append('apresenta programa')
    if 'convidado' in ps: out.append('nos programas')
    if 'citado' in ps: out.append('nas matérias')
    return ' · '.join(out) or 'no acervo'

def _enc_data(iso):
    try:
        _y, _m, _d = iso.split('-')
        return f'{_d}.{_m}.{_y[2:]}'
    except Exception:
        return ''

def pessoa_page(sp, p):
    aps = p['aparicoes']
    n_mat = sum(1 for a in aps if a['tipo'] == 'materia')
    n_ep = sum(1 for a in aps if a['tipo'] != 'materia')
    anos = sorted(a['data'][:4] for a in aps if a.get('data'))
    desde = anos[0] if anos else ''
    rows = ''
    for a in aps[:80]:
        ext = ' target="_blank" rel="noopener"' if a['tipo'] != 'materia' else ''
        tag = 'Programa' if a['tipo'] != 'materia' else 'Matéria'
        rows += f'''    <a class="agd-row" href="{_rvesc(a['url'])}"{ext}>
      <span class="agd-date"><b style="font-size:.9rem">{_enc_data(a.get('data',''))}</b><small>{_PAPEL_ROT.get(a['papel'], '')}</small></span>
      <span class="agd-what"><h3 style="font-size:.95rem">{_rvesc(a['titulo'])}</h3></span>
      <span class="tag agd-tag">{tag}</span>
    </a>\n'''
    return f'''<main class="wrap">
  <div class="art" style="max-width:900px; margin:0 auto">
    <div class="art-head" style="padding-top:30px">
      <div class="tags"><span class="tag wine">Enciclopédia do FOYER</span><span class="tag">{_papeis_resumo(aps)}</span></div>
      <h1>{_rvesc(p['nome'])}</h1>
      <div class="art-byline">
        <span><b>{n_mat}</b> matéria(s) · <b>{n_ep}</b> aparição(ões) nos programas</span>
        <span>No FOYER desde {desde}</span>
      </div>
      <div class="share-row" aria-label="Compartilhar este verbete">
        <button class="sbtn" data-share="whats" data-title="{safe(p['nome'])} na Enciclopédia do FOYER">WhatsApp</button>
        <button class="sbtn" data-share="copy" data-title="{safe(p['nome'])}">Copiar link</button>
      </div>
    </div>
    <div class="agd" style="margin-top:26px">
{rows}    </div>
    <div class="filters" style="padding:24px 0 40px">
      <a href="enciclopedia.html">← Enciclopédia</a>
      <a href="busca.html">Buscar no acervo</a>
    </div>
  </div>
</main>
'''

def _yt_pessoas(v):
    sps = POR_VIDEO.get(v.get('id', ''), [])
    if not sps:
        return ''
    links = ' · '.join(f'<a href="pessoa-{sp}.html" style="color:inherit">{_rvesc(PESSOAS[sp]["nome"])}</a>'
                       for sp in sps[:3] if sp in PESSOAS)
    return f'<span class="meta-l" style="display:block;margin-top:6px">Com {links}</span>' if links else ''

# ---------------------------------------------------------------- YOUTUBE (programas, crítica e entrevistas reais)
try:
    YT = _json.load(open(os.path.join(ROOT, 'import/youtube.json')))
except Exception:
    YT = {'programas': []}

def _yt_data(iso):
    try:
        _y, _m, _d = iso.split('-')
        return f'{_d}.{_m}.{_y[2:]}'
    except Exception:
        return iso

def yt_cell(v, rotulo):
    return f'''    <article class="ep-cell">
      <a class="ph" href="{_rvesc(v['url'])}" target="_blank" rel="noopener" aria-label="Assistir no YouTube">
        <img src="{_rvesc(v['thumb'])}" alt="{_rvesc(v['titulo'])}" loading="lazy" onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/{_rvesc(v.get('id',''))}/mqdefault.jpg'">
        <span class="play">▶</span>
      </a>
      <div class="ep-body">
        <span class="meta-l">{_rvesc(rotulo)}</span>
        <h3>{_rvesc(v['titulo'])}</h3>
        {_yt_pessoas(v)}
        <div class="meta-row">
          <span class="meta-l">{_yt_data(v.get('quando',''))}</span>
          <button class="share-min" data-share="native" data-title="{safe(v['titulo'])}">Compartilhar ↗</button>
        </div>
      </div>
    </article>'''

_yt_progs = YT.get('programas', [])
def _yt_por_papel(papel):
    return [p for p in _yt_progs if p.get('papel') == papel]

def _yt_videos(progs, n):
    vids = []
    for p in progs:
        for v in p.get('videos', []):
            vids.append((v.get('quando', ''), p['nome'], v))
    vids.sort(key=lambda x: x[0], reverse=True)
    return vids[:n]

if _yt_progs:
    # ---------- PROGRAMAS ----------
    _PDESC = {
        'Programa do Foyer': ('Talk — 6 temporadas', 'O talk do FOYER: conversas com elencos, criadores e os bastidores do teatro musical.'),
        'Críticas Teatrais': ('Crítica em vídeo', 'A redação assiste, pensa e assina — em vídeo.'),
        'Teatro a Sangue Frio': ('Série', 'O teatro contado com o sangue frio de quem viveu a cena.'),
        'Astro em Cena': ('Papo — Astrologia', 'Astrologia e artes em conversas cheias de insights.'),
        'Trivia Musical Game Show': ('Game show', 'Artistas duelam no universo dos musicais. Quem sabe mais?'),
        'Session Musical': ('Música em estúdio', 'O teatro musical brasileiro canta ao vivo no estúdio do FOYER.'),
        'Coxixo de Coxia': ('Coxia — Humor', 'O papo solto de quem vive o teatro por trás da cortina.'),
        'Corda Bamba': ('Série', 'Novos episódios no canal do FOYER.'),
        'Por Bruno Cavalcanti': ('Crítica', 'A crítica assinada por Bruno Cavalcanti, em vídeo.'),
    }
    _cards, _vistos_nomes = '', set()
    for p in _yt_progs:
        _nome = p['nome'].split(' — ')[0]
        if _nome in _vistos_nomes:
            continue
        _vistos_nomes.add(_nome)
        _rot, _desc = _PDESC.get(_nome, ('Programa', 'Novos episódios no canal do FOYER.'))
        _cards += f'''      <a class="show" href="{_rvesc(p['urlPlaylist'])}" target="_blank" rel="noopener">
        <span class="ep">{_rvesc(_rot)}</span><span class="tri">▶</span>
        <h3>{_rvesc(_nome)}</h3>
        <p>{_rvesc(_desc)}</p>
      </a>\n'''
    _ult = '\n'.join(yt_cell(v, nome.split(' — ')[0]) for _, nome, v in _yt_videos(_yt_progs, 12))
    programas_body = band('O canal', 'Os Programas', 'YouTube &amp; Spotify — novos episódios toda semana') + f'''
<section class="programas first">
  <div class="wrap">
    <div class="prog-grid" style="margin-top:40px">
{_cards}    </div>
    <div class="prog-cta">
      <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">Assistir no YouTube ↗</a>
      <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Ouvir no Spotify ↗</a>
    </div>
  </div>
</section>
<main class="wrap">
  <div class="sec-head">
    <h2>Últimos episódios</h2>
    <span class="note">Direto do canal</span>
    <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener" class="all">Ver no YouTube ↗</a>
  </div>
  <div class="ep-grid">
{_ult}
  </div>
  <div class="ad-slot" data-ad-slot="1401"></div>
</main>
'''

    _kyra = [p for p in _yt_progs if p['nome'] == 'Críticas Teatrais']
    _capa_crit = '\n'.join(yt_cell(v, 'Críticas Teatrais') for _, _n, v in _yt_videos(_kyra, 3))
    index_main = index_main.replace('__CRITICA_CAPA__', _capa_crit)
    _capa_progs, _visto_capa = '', set()
    for _p in _yt_progs:
        _nm = _p['nome'].split(' — ')[0]
        if _nm in _visto_capa: continue
        _visto_capa.add(_nm)
        if len(_capa_progs.split('</a>')) > 5: break
        _rt, _dc = _PDESC.get(_nm, ('Programa', 'Novos episódios no canal do FOYER.'))
        _capa_progs += ('      <a class="show" href="' + _rvesc(_p['urlPlaylist']) + '" target="_blank" rel="noopener">'
                        '<span class="ep">' + _rvesc(_rt) + '</span><span class="tri">▶</span>'
                        '<h3>' + _rvesc(_nm) + '</h3><p>' + _rvesc(_dc) + '</p></a>\n')
    index_main = index_main.replace('__PROGRAMAS_CAPA__', _capa_progs)

    # ---------- CRÍTICA ----------
    _crit_vids = '\n'.join(yt_cell(v, 'Críticas Teatrais') for _, _n, v in _yt_videos(_kyra, 6))
    _bruno = [p for p in _yt_progs if p['nome'] == 'Por Bruno Cavalcanti']
    _bruno_vids = '\n'.join(yt_cell(v, 'Por Bruno Cavalcanti') for _, _n, v in _yt_videos(_bruno, 3))
    _crit_mats = [p for p in MATERIAS if p.get('cat') == 'Crítica'][:12]
    _crit_cells = '\n'.join(real_cell(p) for p in _crit_mats)
    critica_body = band('Editoria', 'Crítica', 'A redação assiste, pensa e assina — sem medo de opinião') + f'''
<main class="wrap">
  <div class="sec-head">
    <h2>Crítica em vídeo</h2>
    <span class="note">Por Kyra Piscitelli — os espetáculos em cartaz, toda semana</span>
    <a href="https://www.youtube.com/playlist?list=PLFPAp2PKrLk15leURL9x9-HQjDGTeXP2R" target="_blank" rel="noopener" class="all">Ver no YouTube ↗</a>
  </div>
  <div class="ep-grid">
{_crit_vids}
  </div>
  <div class="ad-slot" data-ad-slot="1501"></div>
  <div class="sec-head">
    <h2>Do acervo: Por Bruno Cavalcanti</h2>
    <span class="note">Críticas em vídeo de temporadas passadas</span>
  </div>
  <div class="ep-grid">
{_bruno_vids}
  </div>
  <div class="sec-head">
    <h2>Do acervo: crítica escrita</h2>
    <span class="note">Textos de temporadas passadas</span>
    <a href="cat-critica.html" class="all">Todas →</a>
  </div>
  <div class="news-grid three">
{_crit_cells}
  </div>
</main>
'''

    # ---------- ENTREVISTAS ----------
    _ent_vids = '\n'.join(yt_cell(v, 'Programa do Foyer') for _, _n, v in _yt_videos(_yt_por_papel('entrevista'), 9))
    _ent_mats = [p for p in MATERIAS if p.get('cat') == 'Entrevista'][:6]
    _ent_extra = ''
    if _ent_mats:
        _ent_cells = '\n'.join(real_cell(p) for p in _ent_mats)
        _ent_extra = f'''  <div class="sec-head">
    <h2>Entrevistas escritas</h2>
    <span class="note">Do acervo do FOYER</span>
  </div>
  <div class="news-grid three">
{_ent_cells}
  </div>
'''
    entrevistas_body = band('Editoria', 'Entrevistas', 'Conversas longas com quem faz o palco acontecer') + f'''
<main class="wrap">
  <div class="sec-head">
    <h2>No Programa do Foyer</h2>
    <span class="note">O talk do canal — elencos, criadores e bastidores</span>
    <a href="https://www.youtube.com/playlist?list=PLFPAp2PKrLk2xo9BULjM0wmganFcGd88C" target="_blank" rel="noopener" class="all">Temporada atual ↗</a>
  </div>
  <div class="ep-grid">
{_ent_vids}
  </div>
  <div class="ad-slot" data-ad-slot="1601"></div>
{_ent_extra}</main>
'''
    print(f"• YouTube: {sum(len(p.get('videos', [])) for p in _yt_progs)} episódios em {len(_yt_progs)} playlists")

# ---------------------------------------------------------------- AGENDA / SOBRE / CONTATO (conteúdo real)
_MES_ABREV = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

def _agd_linha(p, destaque=''):
    ev = p.get('evento') or {}
    try:
        _y, _m, _d = (ev.get('inicio') or p['iso']).split('-')
        _dia, _mes = str(int(_d)), _MES_ABREV[int(_m) - 1]
    except Exception:
        _dia, _mes = '·', ''
    lugar = ', '.join(x for x in (ev.get('local', ''), ev.get('cidade', '')) if x)
    meta = destaque or lugar or (p['desc'][:100].rsplit(' ', 1)[0] + '…')
    return f'''    <a class="agd-row" href="post-{p['slug']}.html">
      <span class="agd-date"><b>{_dia}</b><small>{_mes}</small></span>
      <span class="agd-what"><h3>{_rvesc(p['title'])}</h3><span class="agd-meta">{_rvesc(meta)}</span></span>
      <span class="tag agd-tag">{_rvesc(p['cat'])}</span>
    </a>\n'''

_hoje = datetime.now(timezone.utc).strftime('%Y-%m-%d')
_hoje7 = (datetime.now(timezone.utc) + __import__('datetime').timedelta(days=7)).strftime('%Y-%m-%d')

_com_evento = [p for p in MATERIAS if p.get('evento') and (p['evento'].get('inicio') or '')]
_ativos = [p for p in _com_evento if not (p['evento'].get('fim') and p['evento']['fim'] < _hoje)]

def _fmt_curta(iso):
    try:
        _y, _m, _d = iso.split('-')
        return f'{int(_d)} de {_MES_ABREV[int(_m)-1]}'
    except Exception:
        return iso

_sec_estreia, _sec_cartaz, _sec_ultimas, _sec_vemai = '', '', '', ''
for p in sorted(_ativos, key=lambda x: x['evento']['inicio']):
    ev = p['evento']
    lugar = ', '.join(x for x in (ev.get('local', ''), ev.get('cidade', '')) if x)
    if ev['inicio'] > _hoje7:
        _sec_vemai += _agd_linha(p, f"a partir de {_fmt_curta(ev['inicio'])} · {lugar}")
    elif ev['inicio'] > _hoje:
        _sec_estreia += _agd_linha(p, f"estreia {_fmt_curta(ev['inicio'])} · {lugar}")
    elif ev.get('fim') and ev['fim'] <= _hoje7:
        _sec_ultimas += _agd_linha(p, f"até {_fmt_curta(ev['fim'])} · {lugar}")
    else:
        ate = f" · até {_fmt_curta(ev['fim'])}" if ev.get('fim') else ''
        _sec_cartaz += _agd_linha(p, f"em cartaz · {lugar}{ate}")

def _agd_sec(titulo, nota, linhas):
    if not linhas:
        return ''
    return (f'<div class="sec-head"><h2>{titulo}</h2><span class="note">{nota}</span></div>'
            f'\n  <div class="agd">\n{linhas}  </div>\n')

_agd_corpo = (_agd_sec('Estreia esta semana', 'garanta o ingresso', _sec_estreia)
              + _agd_sec('Últimas sessões', 'agora ou nunca', _sec_ultimas)
              + _agd_sec('Em cartaz agora', 'rolando neste momento', _sec_cartaz)
              + _agd_sec('Vem aí', 'já anunciado', _sec_vemai))

_AGD_CATS = {'Show', 'Festa', 'Audições', 'Edital', 'Exposições'}
_agd_mats = [p for p in MATERIAS
             if p.get('cat') in _AGD_CATS or 'estreia' in p.get('title', '').lower()][:10]
_cobertura = ''.join(_agd_linha(p) for p in _agd_mats)
if not _agd_corpo:
    _agd_corpo = ('<div class="vazio" style="border:2px dashed var(--line);padding:26px;'
                  'font-family:var(--mono);font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;'
                  'color:var(--ink-soft)">A agenda está em formação: as matérias novas com data de evento '
                  'entram aqui sozinhas, e o que sai de cartaz some sozinho.</div>')

agenda_body = band('Serviço', 'Agenda', 'O que está em cartaz, o que estreia e o que sai de cena, dia a dia') + f'''
<main class="wrap">
  {_agd_corpo}
  <div class="ad-slot" data-ad-slot="1701"></div>
  <div class="sec-head"><h2>Últimas coberturas de eventos</h2><span class="note">do noticiário do FOYER</span></div>
  <div class="agd">
{_cobertura}  </div>
  <div class="filters" style="padding:18px 0 40px">
    <a href="cat-show.html">Shows</a>
    <a href="cat-exposicoes.html">Exposições</a>
    <a href="cat-audicoes.html">Audições</a>
    <a href="cat-edital.html">Editais</a>
    <a href="noticias.html">Todas as notícias →</a>
  </div>
</main>
'''

try:
    _CFG = _json.load(open(os.path.join(ROOT, 'import/site.json')))
except Exception:
    _CFG = {}
try:
    _EQ_PUB = _json.load(open(os.path.join(ROOT, 'import/equipe.json'))).get('usuarios', [])
except Exception:
    _EQ_PUB = []

_eq_linhas = ''.join(
    f'<li><b>{_rvesc(u["nome"])}</b> — {"Direção e edição" if u.get("papel") == "chefe" else "Redação"}</li>'
    for u in _EQ_PUB)
_n_eps = sum(len(p.get('videos', [])) for p in YT.get('programas', []))
sobre_body = band('O Foyer', 'Quem somos', 'Seu veículo de informação artístico') + f'''
<main class="wrap">
  <div class="art" style="max-width:820px; margin:0 auto">
    <div class="art-body" style="padding-top:34px">
      <p class="drop">O FOYER é um veículo de comunicação artístico — um destino online dedicado à cultura, à criatividade e à expressão artística. Nossa missão é proporcionar uma plataforma dinâmica onde artistas, entusiastas da arte e curiosos possam se conectar, explorar e se inspirar.</p>
      <p>Com uma ampla variedade de conteúdo, da música e do teatro à literatura e à dança, abraçamos todas as formas de expressão criativa: somos o ponto de encontro para descobrir talentos emergentes, acompanhar as tendências e mergulhar nas histórias por trás das obras e das performances. Seja você um artista em ascensão, um apreciador de arte ou alguém que busca se envolver no mundo da cultura, o FOYER é o seu guia para explorar, aprender e se conectar.</p>
      <h2>O que fazemos</h2>
      <p>São <b>{len(MATERIAS)} matérias</b> publicadas — notícias, críticas, entrevistas e serviço — e <b>{_n_eps} episódios</b> nos programas do canal, entre eles o <b>Programa do Foyer</b> (nosso talk com elencos e criadores), as críticas em vídeo de <b>Críticas Teatrais</b> e <b>Por Bruno Cavalcanti</b>, o game show <b>Trivia Musical</b> e o <b>Session Musical</b>, em que o teatro musical brasileiro canta em estúdio.</p>
      <h2>Quem fundou</h2>
      <p><b>Isabel Branquinha</b> — Cofundadora. Jornalista, atriz, dramaturga, apresentadora e produtora. Graduada com ênfase na crítica teatral, atuou em diversas áreas — inclusive como tradutora-intérprete de produtores internacionais do Festival Lollapalooza. Atua como social media, assessora de imprensa, redatora, jornalista cultural, diretora de conteúdo e produtora cultural.</p>
      <p><b>Pedro Amaral</b> — Cofundador. Ator, dramaturgo, apresentador e produtor. Nascido em Santos e radicado em São Paulo, é bacharel em atuação pelo Célia Helena Centro de Artes e Educação e pós-graduado em Dramaturgia e Roteiro pela mesma instituição.</p>
      <h2>Como trabalhamos</h2>
      <p>Título sem caça-clique, apuração com fonte e serviço completo ao final. Parte das matérias assinadas como <b>Redação Foyer</b> conta com apuração assistida por inteligência artificial — todas são revisadas, checadas e aprovadas por um editor humano antes de ir ao ar. Fotografias são sempre de divulgação oficial, com o devido crédito. Conteúdo publicitário, quando houver, é identificado como tal.</p>
      <p>Quer falar com a redação? <a href="contato.html">Visite a página de contato</a>.</p>
    </div>
  </div>
</main>
'''

_email = _CFG.get('emailContato', '')
_email_bloco = (f'<p style="font-size:1.1rem">✉ <a href="mailto:{_rvesc(_email)}"><b>{_rvesc(_email)}</b></a></p>'
                if _email else
                '<p>✉ O e-mail da redação será publicado em breve.</p>')
_fones = ''.join(
    f'<p><b>{_rvesc(t["nome"])}</b> — {_rvesc(t["papel"])}<br>☎ {_rvesc(t["fone"])}</p>'
    for t in _CFG.get('telefones', []))
contato_body = band('Fale conosco', 'Contato', 'Quer saber mais sobre o Foyer, sugerir uma pauta ou deixar uma mensagem?') + f'''
<main class="wrap">
  <div class="art" style="max-width:820px; margin:0 auto">
    <div class="art-body" style="padding-top:34px">
      <h2>Fale com a gente</h2>
      <p>Sugestões de pauta, convites para coberturas e estreias, material de divulgação e errata:</p>
      {_email_bloco}
      {_fones}
      <h2>Publicidade e parcerias</h2>
      <p>Anúncios no site, páginas patrocinadas na Revista do FOYER e projetos especiais nos programas do canal — escreva para o e-mail acima com o assunto “Publicidade”.</p>
      <h2>Nossos canais</h2>
      <p>
        <a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">YouTube — @Foyer.digital ↗</a><br>
        <a href="https://open.spotify.com/show/4GBFkc9ZaHC09krfoguHbm" target="_blank" rel="noopener">Spotify — Programa do Foyer ↗</a>
      </p>
    </div>
  </div>
</main>
'''

_top_pessoas = sorted(PESSOAS.items(), key=lambda x: len(x[1]['aparicoes']), reverse=True)
# quem trabalha no FOYER não ocupa o topo do índice (mas segue com verbete e na busca)
def _slug_nome(n):
    import unicodedata as _u
    n = _u.normalize('NFKD', n).encode('ascii', 'ignore').decode()
    return _re.sub(r'[^a-zA-Z0-9]+', '-', n).strip('-').lower()
_CASA = {'pedro-amaral', 'isabel-branquinha', 'pedro-cantelli', 'pedro-cobron', 'gerson-steves'}
_CASA |= {_slug_nome(u.get('nome', '')) for u in _EQ_PUB}
_enc_rows = ''
for _sp, _pp in [x for x in _top_pessoas if x[0] not in _CASA][:60]:
    _enc_rows += f'''    <a class="ency-row" href="pessoa-{_sp}.html" role="row">
      <span class="nm">{_rvesc(_pp['nome'])}</span><span class="of">{_papeis_resumo(_pp['aparicoes'])}</span><span class="ct">{len(_pp['aparicoes'])} aparições</span><span class="ar">→</span>
    </a>\n'''
_capa_enc = ('<div class="ency-stats">'
  f'<div class="stat"><span class="n" data-v="{len(PESSOAS)}">0</span><span class="l">Pessoas mapeadas</span></div>'
  f'<div class="stat"><span class="n" data-v="{len(MATERIAS)}">0</span><span class="l">Matérias no acervo</span></div>'
  f'<div class="stat"><span class="n" data-v="{_n_eps}">0</span><span class="l">Episódios dos programas</span></div>'
  '</div>\n  <div class="ency-table" role="table" aria-label="Índice de pessoas">'
  '<div class="ency-row head" role="row"><span>Nome</span><span class="of">Presença</span><span class="ct">Aparições</span><span class="ar"></span></div>')
for _sp, _pp in [x for x in _top_pessoas if x[0] not in _CASA][:4]:
    _capa_enc += (f'<a class="ency-row" href="pessoa-{_sp}.html" role="row"><span class="nm">{_rvesc(_pp["nome"])}</span>'
                  f'<span class="of">{_papeis_resumo(_pp["aparicoes"])}</span>'
                  f'<span class="ct">{len(_pp["aparicoes"])}</span><span class="ar">→</span></a>')
_capa_enc += '</div>'
index_main = index_main.replace('__ENCICLOPEDIA_CAPA__', _capa_enc)

enciclopedia_body = band('Projeto Foyer', 'Enciclopédia do FOYER', 'Todas as pessoas que passaram pelas matérias e pelos programas — cada nome clicável leva ao histórico completo') + f'''
<main class="wrap">
  <div class="ency-stats">
    <div class="stat"><span class="n" data-v="{len(PESSOAS)}">0</span><span class="l">Pessoas mapeadas</span></div>
    <div class="stat"><span class="n" data-v="{len(MATERIAS)}">0</span><span class="l">Matérias no acervo</span></div>
    <div class="stat"><span class="n" data-v="{_n_eps}">0</span><span class="l">Episódios dos programas</span></div>
  </div>
  <form class="ency-search" onsubmit="return false;">
    <input type="search" id="enc-q" placeholder="Busque uma pessoa — artista, autor, convidado…" aria-label="Buscar pessoa">
    <button type="submit">Buscar</button>
  </form>
  <div class="ency-table" role="table" aria-label="Índice de pessoas" id="enc-res">
{_enc_rows}  </div>
  <p class="note" style="font-family:var(--mono);font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);padding:18px 0 40px">
    Índice montado automaticamente a partir do acervo do FOYER — os 60 nomes mais presentes acima; use a busca para os {len(PESSOAS)} verbetes.
  </p>
</main>
<script>
(function(){{
  var IDX = null, res = document.getElementById('enc-res'), padrao = res.innerHTML;
  function norm(t){{ return t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }}
  document.getElementById('enc-q').addEventListener('input', function(){{
    var v = norm(this.value.trim());
    if(v.length < 2){{ res.innerHTML = padrao; return; }}
    var go = function(){{
      var hits = [];
      for(var i = 0; i < IDX.length && hits.length < 40; i++)
        if(norm(IDX[i].n).indexOf(v) !== -1) hits.push(IDX[i]);
      res.innerHTML = hits.length
        ? hits.map(function(p){{ return '<a class="ency-row" href="' + p.u + '"><span class="nm">' + p.n + '</span><span class="of"></span><span class="ct">' + p.c + ' aparições</span><span class="ar">→</span></a>'; }}).join('')
        : '<div class="ency-row"><span class="nm">Nenhuma pessoa encontrada</span><span class="of"></span><span class="ct"></span><span class="ar"></span></div>';
    }};
    if(IDX) go();
    else fetch('assets/pessoas-index.json').then(function(r){{ return r.json(); }}).then(function(d){{ IDX = d; go(); }});
  }});
}})();
</script>
'''

# ---------------------------------------------------------------- monta tudo

# capa tem ordem própria: ticker+masthead antes da nav
capa_html = (head('FOYER — Teatro, Cultura & Arte',
                  'FOYER — portal de teatro, música e cultura. Notícias, crítica, revista semanal, programas e a Enciclopédia do Teatro Musical Brasileiro.')
             + '\n' + DEFS + '\n' + index_body + '\n' + UTIL + '\n' + nav('index.html')
             + '\n' + index_main + '\n' + FOOTER + '</body>\n</html>\n')
with open(os.path.join(ROOT, 'index.html'), 'w') as f:
    f.write(capa_html)
print('•', 'index.html', len(capa_html)//1024, 'KB')

import glob as _glob
for _f in _glob.glob(os.path.join(ROOT, 'post-*.html')) + _glob.glob(os.path.join(ROOT, 'noticias*.html')) + _glob.glob(os.path.join(ROOT, 'cat-*.html')) + _glob.glob(os.path.join(ROOT, 'pessoa-*.html')):
    os.remove(_f)

_tot = len(MATERIAS)
_pages = (_tot + POR_PAGINA - 1) // POR_PAGINA
for _n in range(1, _pages + 1):
    _fname = 'noticias.html' if _n == 1 else f'noticias-p{_n}.html'
    page(_fname, f'Notícias — página {_n} — FOYER', 'Todas as matérias do FOYER.', 'noticias.html',
         listing_body(MATERIAS, _n, _pages, 'noticias', 'Notícias',
                      f'{_tot} matérias no acervo — página {_n} de {_pages}'))

for _c in _cats:
    _posts = [x for x in MATERIAS if x['cat'] == _c]
    _cp = (len(_posts) + POR_PAGINA - 1) // POR_PAGINA
    _base = 'cat-' + _cat_slug(_c)
    for _n in range(1, _cp + 1):
        _fname = f'{_base}.html' if _n == 1 else f'{_base}-p{_n}.html'
        page(_fname, f'{_c} — FOYER', f'Matérias de {_c} no FOYER.', 'noticias.html',
             listing_body(_posts, _n, _cp, _base, _c,
                          f'{len(_posts)} matérias — página {_n} de {_cp}', active=_c))
page('critica.html', 'Crítica — FOYER', 'Críticas de teatro, musicais, dança e ópera no FOYER.', 'critica.html', critica_body)
page('entrevistas.html', 'Entrevistas — FOYER', 'Entrevistas com artistas e profissionais do palco.', 'entrevistas.html', entrevistas_body)
page('agenda.html', 'Agenda — FOYER', 'Estreias, temporadas e eventos de teatro pelo Brasil.', 'agenda.html', agenda_body)
page('programas.html', 'Programas — FOYER', 'Os programas do canal Foyer no YouTube e Spotify.', 'programas.html', programas_body)
page('enciclopedia.html', 'Enciclopédia — FOYER', 'Enciclopédia do Teatro Musical Brasileiro: artistas, espetáculos e fichas técnicas.', 'enciclopedia.html', enciclopedia_body)
page('revista.html', 'A Revista — FOYER', 'A revista semanal do Foyer: edições fechadas para ler online ou baixar em PDF.', 'revista.html', revista_body)
page('busca.html', 'Buscar — FOYER', 'Busque matérias, críticas, artistas e espetáculos no FOYER.', 'busca.html', busca_body)
page('sobre.html', 'Quem somos — FOYER', 'O FOYER: portal de jornalismo cultural e canal de programas sobre teatro, música e artes.', 'index.html', sobre_body)
page('contato.html', 'Contato — FOYER', 'Fale com a redação do FOYER: pautas, imprensa, parcerias e publicidade.', 'index.html', contato_body)
page('privacidade.html', 'Política de Privacidade — FOYER', 'Política de privacidade e cookies do FOYER.', 'privacidade.html', privacidade_body)

def _ld_materia(p):
    img = wiximg(p['img'], 1200, 630) if p['img'] else f'{BASE}/assets/logo/src/foyer-banner.png'
    if not img.startswith('http'):
        img = f'{BASE}/{img}'
    autor = p.get('author') or 'Redação Foyer'
    tipo_autor = 'Organization' if 'reda' in autor.lower() else 'Person'
    dados = {
        '@context': 'https://schema.org', '@type': 'NewsArticle',
        'headline': p['title'][:110],
        'description': p['desc'][:200],
        'image': [img],
        'datePublished': p.get('iso', ''),
        'dateModified': (p.get('atualizado') or p.get('iso', ''))[:19],
        'author': [{'@type': tipo_autor, 'name': autor}],
        'publisher': {'@type': 'NewsMediaOrganization', 'name': 'FOYER',
                      'logo': {'@type': 'ImageObject', 'url': f'{BASE}/assets/logo/foyer-stacked-gold.png'}},
        'mainEntityOfPage': f"{BASE}/post-{p['slug']}.html",
        'inLanguage': 'pt-BR',
        'articleSection': p.get('cat', ''),
    }
    return '<script type="application/ld+json">' + _json.dumps(dados, ensure_ascii=False) + '</script>'

for _i, _p in enumerate(MATERIAS):
    page('post-' + _p['slug'] + '.html', _p['title'] + ' — FOYER', _p['desc'][:200], 'noticias.html', post_page(_i, _p), quiet=True,
         og_img=wiximg(_p['img'], 1200, 630) if _p['img'] else None, og_type='article', ld=_ld_materia(_p))
print(f'• {len(MATERIAS)} páginas de matéria')

for _sp, _pp in PESSOAS.items():
    page('pessoa-' + _sp + '.html', _pp['nome'] + ' — Enciclopédia FOYER',
         f"{_pp['nome']} na Enciclopédia do FOYER: histórico completo de matérias e programas.",
         'enciclopedia.html', pessoa_page(_sp, _pp), quiet=True)
print(f'• {len(PESSOAS)} verbetes de pessoa')
with open(os.path.join(ROOT, 'assets/pessoas-index.json'), 'w') as _f:
    _json.dump([{'n': _pp['nome'], 'u': 'pessoa-' + _sp + '.html', 'c': len(_pp['aparicoes'])}
                for _sp, _pp in _top_pessoas], _f, ensure_ascii=False)

for _e in ED_PUB:
    _cap = _e.get('capa', {})
    page(f'revista-ed-{_e.get("numero")}.html',
         f'A Revista do FOYER — Nº {_e.get("numero")}',
         (_cap.get('manchete') or _e.get('titulo', 'Edição da Revista do FOYER'))[:200],
         'revista.html', edicao_page(_e), quiet=True,
         og_img=_cap.get('img') or None)
if ED_PUB:
    print(f'• {len(ED_PUB)} edição(ões) da revista no ar')

# coxia: página sem nav de seções (área restrita) — cabeçalho mínimo
coxia_html = (head('Coxia — FOYER', 'Área restrita da redação do Foyer.').replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>')
              + '\n' + coxia_body.replace('__TOTAL__', str(len(MATERIAS))) + '\n'
              + '<script src="assets/site.js"></script></body>\n</html>\n')
with open(os.path.join(ROOT, 'coxia.html'), 'w') as f:
    f.write(coxia_html)
print('•', 'coxia.html', len(coxia_html)//1024, 'KB')

nf_body = band('Erro 404', 'Esta página saiu de cartaz', 'O endereço não existe — mas o espetáculo continua') + '''
<main class="wrap" style="padding-bottom:40px">
  <div class="filters" style="padding-top:28px">
    <a href="index.html" class="on">← Voltar à capa</a>
    <a href="noticias.html">Notícias</a>
    <a href="busca.html">Buscar no acervo</a>
  </div>
</main>
'''
page('404.html', 'Página não encontrada — FOYER', 'Página não encontrada no FOYER.', 'index.html', nf_body)

import glob as _g
urls = sorted(os.path.basename(f) for f in _g.glob(os.path.join(ROOT, '*.html'))
              if os.path.basename(f) not in ('coxia.html', '404.html'))
with open(os.path.join(ROOT, 'assets/busca-index.json'), 'w') as f:
    _json.dump([{'t': _p['title'], 'c': _p.get('cat', ''), 'a': _p.get('author', ''),
                 'u': 'post-' + _p['slug'] + '.html'}
                for _p in MATERIAS]
               + [{'t': _pp['nome'], 'c': 'Enciclopédia', 'u': 'pessoa-' + _sp + '.html'}
                  for _sp, _pp in _top_pessoas], f, ensure_ascii=False)
print(f'busca: {len(MATERIAS)} matérias indexadas')

_hoje_sm = datetime.now(timezone.utc).strftime('%Y-%m-%d')
_mod = {'post-' + p['slug'] + '.html': ((p.get('atualizado') or p.get('iso') or _hoje_sm)[:10])
        for p in MATERIAS}
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        loc = BASE + '/' + ('' if u == 'index.html' else u)
        f.write(f'<url><loc>{loc}</loc><lastmod>{_mod.get(u, _hoje_sm)}</lastmod></url>\n')
    f.write('</urlset>\n')

# sitemap de notícias (Google News): matérias das últimas 48 horas
_corte_news = (datetime.now(timezone.utc) - __import__('datetime').timedelta(days=2)).strftime('%Y-%m-%d')
_news = [p for p in MATERIAS if (p.get('iso') or '') >= _corte_news]
with open(os.path.join(ROOT, 'sitemap-news.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n')
    for p in _news:
        f.write('<url><loc>' + BASE + '/post-' + p['slug'] + '.html</loc>'
                '<news:news><news:publication><news:name>FOYER</news:name>'
                '<news:language>pt</news:language></news:publication>'
                '<news:publication_date>' + p.get('iso', _hoje_sm) + '</news:publication_date>'
                '<news:title>' + _html.escape(p['title']) + '</news:title></news:news></url>\n')
    f.write('</urlset>\n')
from email.utils import format_datetime as _fmt822
with open(os.path.join(ROOT, 'feed.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            '<title>FOYER</title><link>' + BASE + '/</link>'
            '<description>Jornalismo de teatro, música e cultura</description>'
            '<language>pt-BR</language>\n')
    for p in MATERIAS[:30]:
        try:
            _dt = datetime.fromisoformat(p['iso'] + 'T09:00:00+00:00')
            _pub = _fmt822(_dt)
        except Exception:
            _pub = ''
        f.write('<item><title>' + _html.escape(p['title']) + '</title>'
                '<link>' + BASE + '/post-' + p['slug'] + '.html</link>'
                '<guid>' + BASE + '/post-' + p['slug'] + '.html</guid>'
                '<description>' + _html.escape(p['desc'][:220]) + '</description>'
                '<category>' + _html.escape(p.get('cat', '')) + '</category>'
                + (f'<pubDate>{_pub}</pubDate>' if _pub else '') + '</item>\n')
    f.write('</channel></rss>\n')

with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\nDisallow: /coxia.html\n\n'
            f'Sitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap-news.xml\n')
print(f'sitemap: {len(urls)} URLs · news: {len(_news)} matéria(s) recentes')
print('pronto')
