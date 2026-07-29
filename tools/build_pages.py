#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as páginas HTML do site FOYER a partir de partials compartilhados."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- partials

import html as _html
import urllib.parse as _uq

# Endereço público do site. Na chegada do domínio (03/08), troque para
# 'https://foyer.digital' OU rode o build com FOYER_BASE=https://foyer.digital
BASE = os.environ.get('FOYER_BASE', 'https://pedrocobron-ops.github.io/FOYER.DIGITAL---SITE')

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
<meta name="robots" content="max-image-preview:large">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/logo/pwa-192.png">
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
<link rel="preload" href="fonts/AbrilFatface-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/Archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
{ORG_LD}{ld}
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
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
      <!-- a cortina termina na ribalta; abaixo dela, o piso do palco -->
      <rect y="348" width="600" height="52" fill="#2B0805"/>
      <rect y="336" width="600" height="12" fill="#CEB26A" opacity=".85"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-3" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <rect width="600" height="400" fill="#380A06"/>
      <ellipse cx="300" cy="80" rx="330" ry="130" fill="#E9CB85" opacity=".14"/>
      <rect y="230" width="600" height="170" fill="url(#heads)"/>
      <!-- a pessoa que se destaca na plateia: sentada NUMA cadeira da malha (62x44, centro 31+62k / 28+44m) -->
      <circle cx="341" cy="248" r="16" fill="#CEB26A"/>
      <rect width="600" height="400" filter="url(#grain)" opacity=".12"/>
    </symbol>
    <symbol id="ph-4" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">
      <!-- teatro de arena: plateia completa e alinhada dos dois lados, um ator só no centro -->
      <rect width="600" height="400" fill="#4E0F09"/>
      <g fill="#1F0805">
        <circle cx="30" cy="34" r="12"/><circle cx="84" cy="34" r="12"/><circle cx="138" cy="34" r="12"/><circle cx="192" cy="34" r="12"/><circle cx="246" cy="34" r="12"/><circle cx="300" cy="34" r="12"/><circle cx="354" cy="34" r="12"/><circle cx="408" cy="34" r="12"/><circle cx="462" cy="34" r="12"/><circle cx="516" cy="34" r="12"/><circle cx="570" cy="34" r="12"/>
        <circle cx="30" cy="78" r="12"/><circle cx="84" cy="78" r="12"/><circle cx="138" cy="78" r="12"/><circle cx="192" cy="78" r="12"/><circle cx="246" cy="78" r="12"/><circle cx="300" cy="78" r="12"/><circle cx="354" cy="78" r="12"/><circle cx="408" cy="78" r="12"/><circle cx="462" cy="78" r="12"/><circle cx="516" cy="78" r="12"/><circle cx="570" cy="78" r="12"/>
        <circle cx="30" cy="322" r="12"/><circle cx="84" cy="322" r="12"/><circle cx="138" cy="322" r="12"/><circle cx="192" cy="322" r="12"/><circle cx="246" cy="322" r="12"/><circle cx="300" cy="322" r="12"/><circle cx="354" cy="322" r="12"/><circle cx="408" cy="322" r="12"/><circle cx="462" cy="322" r="12"/><circle cx="516" cy="322" r="12"/><circle cx="570" cy="322" r="12"/>
        <circle cx="30" cy="366" r="12"/><circle cx="84" cy="366" r="12"/><circle cx="138" cy="366" r="12"/><circle cx="192" cy="366" r="12"/><circle cx="246" cy="366" r="12"/><circle cx="300" cy="366" r="12"/><circle cx="354" cy="366" r="12"/><circle cx="408" cy="366" r="12"/><circle cx="462" cy="366" r="12"/><circle cx="516" cy="366" r="12"/><circle cx="570" cy="366" r="12"/>
      </g>
      <rect x="120" y="136" width="360" height="128" fill="#380A06" stroke="#CEB26A" stroke-width="3"/>
      <ellipse cx="300" cy="200" rx="72" ry="34" fill="#E9CB85" opacity=".16"/>
      <circle cx="300" cy="200" r="13" fill="#CEB26A"/>
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
        <a href="principios.html">Princípios Editoriais</a>
        <a href="privacidade.html">Política de Privacidade</a>
        <a href="#" data-lgpd>Preferências de cookies</a>
        <a href="#" data-sino>🔔 Notificações</a>
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
<script src="assets/site.js"></script>
<script src="assets/ads.js"></script>
'''

def ph(sym, cap=True, extra='', href='materia.html'):
    c = '<span class="ph-cap">Foto — Divulgação</span>' if cap else ''
    return (f'<a class="ph" href="{href}" aria-label="Foto da matéria">'
            f'<svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{sym}"/></svg>{extra}{c}</a>')

def ad(slot):
    return f'<div class="ad-slot" data-ad-slot="{slot}"></div>'

# ---------------------------------------------------------------- publicidade da casa
# Anúncios vendidos pelo "Anuncie no FOYER": a Faixa (rodapé fixo), a Cortina
# (abertura, 1x por dia) e o Entreato (no meio da matéria). Tudo controlado
# por import/anuncios/site.json (a Coxia edita) e SEMPRE rotulado Publicidade.
import datetime as _dtmod
import json as _json0
try:
    _ANUN = _json0.load(open(os.path.join(ROOT, 'import/anuncios/site.json')))
except Exception:
    _ANUN = {}

def _anun_ativo(k):
    a = _ANUN.get(k) or {}
    if not (a.get('img') or a.get('texto')):
        return None
    ate = (a.get('ate') or '').strip()
    if ate and _dtmod.date.today().isoformat() > ate:
        return None
    return a

def _monta_ads_casa():
    fx, ct = _anun_ativo('faixa'), _anun_ativo('cortina')
    if not (fx or ct):
        return ''
    css = ['<style>']
    corpo = []
    js = []
    if fx:
        css.append('''.pub-faixa{ position:fixed; left:0; right:0; bottom:0; z-index:80; display:flex;
  align-items:center; gap:12px; background:var(--paper); border-top:2px solid var(--ink);
  padding:9px 14px; box-shadow:0 -6px 22px rgba(0,0,0,.18); }
.pub-faixa em{ font-style:normal; font-family:var(--mono); font-size:.5rem; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase; color:var(--ink-soft); flex-shrink:0; }
.pub-faixa a{ flex:1; color:var(--ink); font-weight:600; font-size:.85rem; text-decoration:none;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pub-faixa a:hover{ color:var(--wine); }
.pub-faixa button{ border:2px solid var(--ink); background:transparent; cursor:pointer;
  font-family:var(--mono); font-size:.6rem; padding:4px 9px; flex-shrink:0; }
body.tem-faixa{ padding-bottom:52px; }''')
        _l = fx.get('link') or '#'
        corpo.append(f'<div class="pub-faixa" id="pub-faixa" hidden><em>Publicidade</em>'
                     f'<a href="{_html.escape(_l)}" target="_blank" rel="noopener sponsored">{_html.escape(fx.get("texto", ""))}</a>'
                     '<button type="button" id="pub-faixa-x" aria-label="Fechar">✕</button></div>')
        js.append('''(function(){
  var k = 'foyer-pub-faixa-' + new Date().toISOString().slice(0, 10);
  try{ if(localStorage.getItem(k)) return; }catch(e){}
  var f = document.getElementById('pub-faixa');
  f.hidden = false; document.body.classList.add('tem-faixa');
  document.getElementById('pub-faixa-x').addEventListener('click', function(){
    f.hidden = true; document.body.classList.remove('tem-faixa');
    try{ localStorage.setItem(k, '1'); }catch(e){}
  });
})();''')
    if ct:
        css.append('''.pub-cortina{ position:fixed; inset:0; z-index:120; display:flex; align-items:center;
  justify-content:center; background:rgba(20,6,3,.78); padding:20px; }
.pub-cortina .caixa{ position:relative; background:var(--paper); border:3px solid var(--ink);
  max-width:520px; width:100%; box-shadow:0 20px 60px rgba(0,0,0,.5); }
.pub-cortina .rotulo{ display:block; font-family:var(--mono); font-size:.52rem; font-weight:700;
  letter-spacing:.22em; text-transform:uppercase; color:var(--ink-soft); padding:10px 14px 0; }
.pub-cortina img{ display:block; width:100%; height:auto; padding:10px 14px; box-sizing:border-box; }
.pub-cortina .leg{ padding:0 14px 14px; font-size:.85rem; }
.pub-cortina .fechar{ position:absolute; top:-14px; right:-14px; width:34px; height:34px;
  border:2px solid var(--ink); background:var(--gold); color:var(--wine); font-weight:700;
  cursor:pointer; font-size:1rem; line-height:1; }''')
        _lc = ct.get('link') or '#'
        corpo.append(f'<div class="pub-cortina" id="pub-cortina" hidden><div class="caixa">'
                     '<button class="fechar" type="button" id="pub-cortina-x" aria-label="Fechar">✕</button>'
                     '<span class="rotulo">Publicidade</span>'
                     f'<a href="{_html.escape(_lc)}" target="_blank" rel="noopener sponsored">'
                     f'<img src="{_html.escape(ct.get("img", ""))}" alt="{_html.escape(ct.get("legenda", ""))}"></a>'
                     + (f'<div class="leg">{_html.escape(ct["legenda"])}</div>' if ct.get('legenda') else '')
                     + '</div></div>')
        js.append('''(function(){
  var k = 'foyer-pub-cortina-' + new Date().toISOString().slice(0, 10);
  try{ if(localStorage.getItem(k)) return; }catch(e){}
  var c = document.getElementById('pub-cortina');
  setTimeout(function(){ c.hidden = false; }, 900);
  function fecha(){ c.hidden = true; try{ localStorage.setItem(k, '1'); }catch(e){} }
  document.getElementById('pub-cortina-x').addEventListener('click', fecha);
  c.addEventListener('click', function(e){ if(e.target === c) fecha(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !c.hidden) fecha(); });
})();''')
    css.append('</style>')
    return '\n'.join(css) + '\n' + '\n'.join(corpo) + '\n<script>\n' + '\n'.join(js) + '\n</script>\n'

ADS_CASA = _monta_ads_casa()

def _entreato_html():
    en = _anun_ativo('entreato')
    if not en:
        return ''
    _l = en.get('link') or '#'
    leg = f'<figcaption>{_html.escape(en["legenda"])}</figcaption>' if en.get('legenda') else ''
    return ('<aside class="pub-entreato"><em>Publicidade</em>'
            f'<a href="{_html.escape(_l)}" target="_blank" rel="noopener sponsored">'
            f'<img src="{_html.escape(en.get("img", ""))}" alt="{_html.escape(en.get("legenda", ""))}" loading="lazy"></a>'
            f'{leg}</aside>')

def _injeta_entreato(corpo):
    """O Entreato entra depois do 4º parágrafo da matéria, sempre rotulado."""
    bloco = _entreato_html()
    if not bloco:
        return corpo
    partes = corpo.split('</p>', 4)
    if len(partes) < 5:
        return corpo
    return '</p>'.join(partes[:4]) + '</p>\n' + bloco + partes[4]

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
    # a publicidade da casa entra em todo o site, MENOS na Coxia e dentro da
    # revista (a edição fechada não carrega anúncio de site)
    _pub = '' if (fname.startswith('coxia') or fname.startswith('revista-ed-')) else ADS_CASA
    html = head(title, desc, og_img=og_img, og_type=og_type, og_url=fname, ld=ld) + '\n' + DEFS + '\n' + UTIL + '\n' + nav(current) + '\n' + body + '\n' + _pub + FOOTER + '</body>\n</html>\n'
    with open(os.path.join(ROOT, fname), 'w') as f:
        f.write(html)
    if not quiet:
        print('•', fname, len(html)//1024, 'KB')

# ---------------------------------------------------------------- NOTÍCIAS

noticias_body = band('Editoria', 'Notícias', 'Tudo o que acontece no teatro, na música e na cultura — atualizado o dia inteiro') + f'''
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
  <div class="rev-hero" id="assinar">
    <div class="rev-copy">
      <h2>Uma revista de verdade, toda quinta para assinantes</h2>
      <p>A semana do teatro brasileiro editada com começo, meio e fim: reportagem de capa, críticas da semana, agenda comentada e os bastidores dos programas — diagramada como uma revista impressa.</p>
      <div class="feats">
        <span>Edição fechada semanal — sem rolagem infinita</span>
        <span>Leia no site como revista ou baixe o PDF</span>
        <span>Grátis no seu e-mail, toda quinta às 7h — um dia antes de todo mundo</span>
      </div>
    </div>
    <div class="signup-card" id="signup-conversa">
      <h3>Assinante lê na quinta, às 7h</h3>
      <p class="sg-chamada">Uma edição fechada, com começo, meio e fim, na sua caixa de entrada. De graça.</p>
      <button type="button" class="sg-abrir" data-conversa>🎟 Quero a minha</button>
      <span class="fine">Sem spam, cancele quando quiser. Seus dados ficam só com o FOYER.</span>
    </div>
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
index_main = '''<main id="conteudo">
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
    <h2>A Revista do Foyer — assinante lê um dia antes</h2>
    <div class="go-rev">
      <button type="button" data-conversa>🎟 Assinar em um minuto</button>
      <a href="revista.html">conhecer a revista →</a>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- COXIA (admin)

coxia_body = open(os.path.join(ROOT, 'tools/coxia_body.html'), encoding='utf-8').read()

# ---------------------------------------------------------------- MATÉRIA (modelo)

materia_body = '''<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
        if b.startswith('video:'):
            _u = b[6:].strip()
            _m = _re.search(r'(?:youtu\.be/|v=|shorts/|embed/)([A-Za-z0-9_-]{6,20})', _u)
            if _m:
                out.append(f'<div class="art-video"><iframe src="https://www.youtube-nocookie.com/embed/{_m.group(1)}" title="Vídeo" loading="lazy" allowfullscreen frameborder="0"></iframe></div>')
            continue
        if b.startswith('spotify:'):
            _u = b[8:].strip().split('?')[0]
            _u = _u.replace('open.spotify.com/intl-pt/', 'open.spotify.com/').replace('open.spotify.com/', 'open.spotify.com/embed/')
            if 'open.spotify.com/embed/' in _u:
                out.append(f'<div class="art-spotify"><iframe src="{_h.escape(_u)}" title="Spotify" loading="lazy" frameborder="0" allow="encrypted-media"></iframe></div>')
            continue
        if b.startswith('galeria:'):
            _imgs = [x.strip() for x in b[8:].split('|') if x.strip()]
            _cells = ''.join(f'<img src="{_h.escape(u)}" alt="" loading="lazy">' for u in _imgs)
            out.append(f'<div class="art-galeria">{_cells}</div>')
            continue
        if b.startswith('botao:'):
            _rot, _, _url = b[6:].partition('|')
            if _url.strip():
                out.append(f'<p class="art-cta"><a href="{_h.escape(_url.strip())}" target="_blank" rel="noopener">{_h.escape(_rot.strip())}</a></p>')
            continue
        if b.strip('* ') == '' and '*' in b:
            out.append('<div class="art-div" aria-hidden="true">✦ ✦ ✦</div>')
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
        # horário de publicação em Brasília (as antigas do Wix não têm hora registrada)
        _hora = ''
        try:
            from zoneinfo import ZoneInfo as _ZI
            _dtp = datetime.fromisoformat((_pub or _agora).replace('Z', '+00:00'))
            _dtb = _dtp.astimezone(_ZI('America/Sao_Paulo'))
            _hora = f'{_dtb.hour}h{_dtb.minute:02d}'
            _iso_full = _dtb.isoformat(timespec='seconds')
        except Exception:
            _iso_full = ''
        _novas.append({
            'title': _n['title'], 'slug': _slug, 'desc': _desc,
            'cat': _n.get('cat', 'Notícia'), 'author': _n.get('author', 'Redação Foyer'),
            'date': f'{int(_dd)} de {_MESES_PT[int(_mo)-1]} de {_y}',
            'hora': _hora, 'isoFull': _iso_full,
            'short': f'{_dd}.{_mo}', 'iso': _iso,
            'img': _n.get('img', ''), 'credito': _n.get('imgCredito', ''),
            'atualizado': _n.get('atualizadoEm', ''),
            'correcao': _n.get('correcao') or None,
            'evento': _n.get('evento') or None,
            'cats': [c for c in (_n.get('cats') or []) if c][:3],
            'url': '', 'min': max(1, len(_txt)//1100),
        })
    if _novas:
        _slugs_novos = {x['slug'] for x in _novas}
        MATERIAS = [_m for _m in MATERIAS if _m['slug'] not in _slugs_novos]
        MATERIAS = sorted(_novas + MATERIAS, key=lambda x: x.get('iso',''), reverse=True)
        print(f'• {len(_novas)} matéria(s) da Coxia no ar · {_agendadas} agendada(s) aguardando')
    elif _agendadas:
        print(f'• {_agendadas} matéria(s) agendada(s) aguardando a hora')

# crédito real da capa nos CARTÕES: extrai a legenda do fotógrafo do corpo
# (mesma fonte que a página da matéria usa) para valorizar o nome, não "Divulgação"
_n_creds = 0
for _p in MATERIAS:
    if _p.get('credito') or not _p.get('img'):
        continue
    _cf = os.path.join(ROOT, 'import/corpo', _p['slug'] + '.html')
    if not os.path.exists(_cf):
        continue
    _mc = _re.search(r'<figure class="art-img"><img src="' + _re.escape(_p['img']) +
                     r'"[^>]*>(?:<figcaption>(.*?)</figcaption>)?</figure>',
                     open(_cf).read(), _re.S)
    if _mc and _mc.group(1):
        _capc = _re.sub(r'<[^>]+>', '', _mc.group(1)).strip()
        if _capc:
            _p['credito'] = _capc
            _n_creds += 1
if _n_creds:
    print(f'• crédito de fotógrafo herdado do corpo em {_n_creds} capas de cartão')

_MES_N = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
          'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

def short_date(p):
    return p.get('short', '')

def safe(t):
    return t.replace('"', '”')

# assinaturas com página própria (a definição completa fica em AUTORES, mais abaixo)
_AUTOR_PAGINA = {
    'Pedro Amaral': 'autor-pedro-amaral.html',
    'Isabel Branquinha': 'autor-isabel-branquinha.html',
    'Redação Foyer': 'autor-redacao-foyer.html',
}

def _byline_link(nome):
    """Nome de quem assina, com link para a página da assinatura quando existir."""
    n = (nome or 'Redação Foyer').strip()
    alvo = _AUTOR_PAGINA.get(n)
    return f'<a href="{alvo}" rel="author"><b>{n}</b></a>' if alvo else f'<b>{n}</b>'

def wiximg(url, w=1200, h=675):
    if 'static.wixstatic.com/media/' in url and '/v1/' not in url:
        return f'{url}/v1/fill/w_{w},h_{h},al_c,q_82/cover.jpg'
    return url

def _cred_curto(p):
    """Crédito curto para tarjas de cartão: o NOME do fotógrafo vem antes da
    palavra 'Divulgação' (que só aparece quando não há fotógrafo conhecido)."""
    c = (p.get('credito') or '').strip()
    c = _re.sub(r'^(fotos?|reprodução|imagem)\s*:\s*', '', c, flags=_re.I)
    if '/' in c:
        antes = c.split('/')[0].strip()
        if antes and antes.lower() not in ('divulgação', 'divulgacao', 'reprodução', 'reproducao'):
            c = antes
    c = c.strip(' .')
    if len(c) > 38:
        c = c[:38].rsplit(' ', 1)[0].rstrip(',.;:') + '…'
    if not c or _re.fullmatch(r'(fotos?\s+)?(de\s+)?divulga[çc][ãa]o', c, _re.I):
        return 'Divulgação'
    return c

def real_ph(p, href, cap=True):
    c = f'<span class="ph-cap">Foto — {safe(_cred_curto(p))}</span>' if cap else ''
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

index_main = f'''<main id="conteudo">
<section class="frontpage wrap">
  <div class="fp-grid">
    <article class="manchete">
      <a class="ph cover" href="post-{_p0['slug']}.html" aria-label="Foto da reportagem de capa">
        <img src="{wiximg(_p0['img'])}" alt="" loading="eager" fetchpriority="high" decoding="async" onerror="this.style.display='none'">
        <span class="ph-cap">Foto — {safe(_cred_curto(_p0))}</span>
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
    <h2>A Revista do Foyer — assinante lê um dia antes</h2>
    <div class="go-rev">
      <button type="button" data-conversa>🎟 Assinar em um minuto</button>
      <a href="revista.html">conhecer a revista →</a>
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
    for _c in [_p['cat']] + _p.get('cats', []):
        if _c and _c != 'Em Cartaz' and _c not in _cats:
            _cats.append(_c)

_HOJE_EC = datetime.now(timezone.utc).date().isoformat()
def _em_cartaz(x):
    """Editoria Em Cartaz: atribuída na redação/aprovação; o campo evento,
    quando existe, vira janela de exibição (a matéria entra e sai sozinha)."""
    if 'Em Cartaz' not in [x['cat']] + x.get('cats', []):
        return False
    ev = x.get('evento') or {}
    if ev.get('inicio') and ev['inicio'] > _HOJE_EC:
        return False
    if ev.get('fim') and ev['fim'] < _HOJE_EC:
        return False
    return True

def _filters(active='*'):
    out = f'<a href="noticias.html"{" class=on" if active=="*" else ""}>Todas</a>'
    out += f'<a href="cat-em-cartaz.html"{" class=on" if active=="Em Cartaz" else ""}>✦ Em Cartaz</a>'
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
<main id="conteudo" class="wrap">
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

def nota_correcao(p):
    c = p.get('correcao') or {}
    txt = (c.get('texto') or '').strip()
    if not txt:
        return ''
    quando = ''
    try:
        from zoneinfo import ZoneInfo as _ZIc
        _dt = datetime.fromisoformat(c.get('quando', '')).astimezone(_ZIc('America/Sao_Paulo'))
        quando = _dt.strftime(' (%d/%m/%Y)')
    except Exception:
        pass
    if not txt.lower().startswith('corre'):
        txt = 'Correção: ' + txt
    return ('\n    <aside class="art-correcao" style="border-left:3px solid var(--wine);'
            'background:var(--paper-2);padding:12px 16px;margin:22px 0 4px;'
            'font-family:var(--sans);font-size:.92rem;line-height:1.6">'
            f'<b>{safe(txt)}</b><span style="color:var(--ink-soft)">{quando}</span></aside>')

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
    # a capa aparecia de novo dentro do texto (herança do Wix): remove a duplicata
    # e herda a legenda real (crédito do fotógrafo) para a foto de abertura
    credito_real = ''
    if p.get('img'):
        _pat_dup = _re.compile(
            r'<figure class="art-img"><img src="' + _re.escape(p['img']) +
            r'"[^>]*>(?:<figcaption>(.*?)</figcaption>)?</figure>\s*', _re.S)
        _mdup = _pat_dup.search(corpo)
        if _mdup:
            _cap = _re.sub(r'<[^>]+>', '', _mdup.group(1) or '').strip()
            if _cap:
                credito_real = _cap
            corpo = _pat_dup.sub('', corpo, count=1)
    cred_capa = p.get('credito') or credito_real or 'Foto: Divulgação'
    rel = [x for x in MATERIAS if x['cat'] == p['cat'] and x['slug'] != p['slug']][:3]
    if len(rel) < 3:
        rel += [x for x in MATERIAS if x['slug'] != p['slug'] and x not in rel][:3-len(rel)]
    rel_cells = '\n'.join(real_cell(r) for r in rel)
    return f"""<main id="conteudo" class="wrap">
<article class="art">
  <div class="art-head">
    <div class="tags">
      <a class="tag wine" href="cat-{_cat_slug(p['cat'])}.html">{p['cat']}</a>
      {''.join(f'<a class="tag" href="cat-{_cat_slug(c)}.html">{"✦ " if c == "Em Cartaz" else ""}{c}</a>' for c in p.get('cats', [])) or '<span class="tag">Foyer</span>'}
    </div>
    <h1>{p['title']}</h1>
    <div class="art-byline">
      <span>Por {_byline_link(p['author'])}</span>
      <span>{p['date']}{(', às ' + p['hora']) if p.get('hora') else ''} · {p['min']} min de leitura</span>
    </div>{selo_atualizada(p)}
    <div class="share-row" aria-label="Compartilhar esta matéria">
      <button class="sbtn" data-share="whats" data-title="{safe(p['title'])}">WhatsApp</button>
      <button class="sbtn" data-share="x" data-title="{safe(p['title'])}">X / Twitter</button>
      <button class="sbtn" data-share="face" data-title="{safe(p['title'])}">Facebook</button>
      <button class="sbtn" data-share="copy" data-title="{safe(p['title'])}">Copiar link</button>
    </div>
  </div>

  <figure class="art-cover">
    <span class="ph"><img src="{wiximg(p['img'])}" alt="{safe(p['title'])}" loading="eager" fetchpriority="high" decoding="async" onerror="this.style.display='none'"></span>
    <figcaption>{safe(cred_capa)}</figcaption>
  </figure>

  <div class="ad-slot" data-ad-slot="2001"></div>

  <div class="art-body">
{_injeta_entreato(corpo)}
  </div>
  {nota_correcao(p)}
  {quem_bloco}
  <div class="art-foot">
    <div class="tags"><span class="tag">{p['cat']}</span><span class="tag">{p['author']}</span></div>
    <div class="share-row" aria-label="Compartilhar">
      <button class="sbtn" data-share="whats" data-title="{safe(p['title'])}">WhatsApp</button>
      <button class="sbtn" data-share="copy" data-title="{safe(p['title'])}">Copiar link</button>
    </div>
  </div>
  <aside class="cv-band">
    <div class="cv-band-txt">
      <b>Gostou desta leitura?</b>
      <span>A revista do FOYER sai toda quinta, às 7h, para assinantes. Aberta a todos só na sexta. De graça.</span>
    </div>
    <button type="button" data-conversa>🎟 Quero a minha</button>
  </aside>
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
/* ============ A REVISTA — leitor em formato de página impressa ============ */
.rv-stage{ margin:26px auto 90px; padding:0 14px; --rv-papel:#F6F1E6; }
html[data-theme="dark"] .rv-stage{ --rv-papel:var(--paper); }
/* no desktop largo, a revista abre em página dupla */
.rv-palco{ position:relative; overflow:hidden; }
.rv-book{ position:relative; display:flex; justify-content:center; align-items:stretch;
  perspective:2600px; margin:0; width:max-content; transform-origin:top left; }
.rv-pg{ display:none; border:3px solid var(--ink); background:var(--rv-papel);
  width:720px; height:972px; position:relative; overflow:hidden; animation:rvin .3s ease;
  flex-shrink:0; backface-visibility:hidden; }
.rv-pg.on{ display:flex; flex-direction:column; }
@keyframes rvin{ from{ opacity:0; transform:translateX(16px);} to{ opacity:1; transform:none;} }
/* lado esquerdo e direito da página dupla */
body.rv-duplo .rv-pg.on.pg-l{ border-right-width:1.5px; }
body.rv-duplo .rv-pg.on.pg-r{ border-left-width:1.5px; }
/* sombra da dobra central */
body.rv-duplo .rv-pg.on.pg-l::after{ content:''; position:absolute; top:0; bottom:0; right:0; width:56px;
  background:linear-gradient(270deg, rgba(35,8,5,.16), transparent); pointer-events:none; z-index:8; }
body.rv-duplo .rv-pg.on.pg-r::after{ content:''; position:absolute; top:0; bottom:0; left:0; width:56px;
  background:linear-gradient(90deg, rgba(35,8,5,.13), transparent); pointer-events:none; z-index:8; }
/* grão de papel de revista (sutil; some na impressão) */
.rv-pg::before{ content:''; position:absolute; inset:0; z-index:9; pointer-events:none;
  opacity:.5; mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.42 0 0 0 0 0.38 0 0 0 0 0.32 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23g)'/%3E%3C/svg%3E"); }
html[data-theme="dark"] .rv-pg::before{ opacity:.25; }
/* a virada de página */
.rv-pg.vira-sai-dir{ transform-origin:left center; animation:viraSaiDir .24s ease-in forwards; }
.rv-pg.vira-entra-dir{ transform-origin:left center; animation:viraEntraDir .26s ease-out; }
.rv-pg.vira-sai-esq{ transform-origin:right center; animation:viraSaiEsq .24s ease-in forwards; }
.rv-pg.vira-entra-esq{ transform-origin:right center; animation:viraEntraEsq .26s ease-out; }
@keyframes viraSaiDir{ from{ transform:rotateY(0); filter:brightness(1);} to{ transform:rotateY(-88deg); filter:brightness(.72);} }
@keyframes viraEntraDir{ from{ transform:rotateY(88deg); filter:brightness(.72);} to{ transform:rotateY(0); filter:brightness(1);} }
@keyframes viraSaiEsq{ from{ transform:rotateY(0); filter:brightness(1);} to{ transform:rotateY(88deg); filter:brightness(.72);} }
@keyframes viraEntraEsq{ from{ transform:rotateY(-88deg); filter:brightness(.72);} to{ transform:rotateY(0); filter:brightness(1);} }
@media (prefers-reduced-motion:reduce){
  .rv-pg.vira-sai-dir,.rv-pg.vira-entra-dir,.rv-pg.vira-sai-esq,.rv-pg.vira-entra-esq{ animation:none; }
  .rv-pg{ animation:none; } }
/* convite no canto: a pontinha da página dobra ao passar o mouse */
.rv-canto{ position:absolute; right:0; bottom:0; width:64px; height:64px; z-index:11; cursor:pointer;
  background:linear-gradient(315deg, var(--paper-2) 0%, var(--paper-2) 48%, transparent 50%);
  clip-path:polygon(100% 0, 100% 100%, 0 100%); opacity:0; transition:opacity .2s, transform .2s;
  transform:translate(8px,8px); border:0; padding:0; }
.rv-pg:hover .rv-canto{ opacity:.85; transform:none; }
.rv-canto:focus-visible{ opacity:1; transform:none; outline:2px solid var(--gold); }
/* sem mouse (celular), a pontinha fica sempre à vista */
@media (hover:none){ .rv-canto{ opacity:.55; transform:none; } }
/* a espessura: as folhas que faltam (direita) e as já lidas (esquerda) */
.rv-lombo{ position:absolute; top:8px; bottom:8px; width:0; z-index:0; pointer-events:none;
  background:repeating-linear-gradient(90deg, #d5cbb2 0 1px, #f6f1e6 1px 3px);
  border:1px solid var(--ink); border-left:0; transition:width .3s ease; }
.rv-lombo.esq{ right:100%; border:1px solid var(--ink); border-right:0;
  background:repeating-linear-gradient(270deg, #d5cbb2 0 1px, #f6f1e6 1px 3px); }
.rv-lombo.dir{ left:100%; }
html[data-theme="dark"] .rv-lombo{ background:repeating-linear-gradient(90deg, #1c1712 0 1px, #2e2820 1px 3px); }
html[data-theme="dark"] .rv-lombo.esq{ background:repeating-linear-gradient(270deg, #1c1712 0 1px, #2e2820 1px 3px); }
/* a fita marcadora */
.rv-fita{ position:absolute; top:-3px; right:8px; width:16px; height:52px; z-index:12; pointer-events:none;
  background:linear-gradient(180deg, var(--gold) 0%, #b89a55 100%);
  clip-path:polygon(0 0, 100% 0, 100% 100%, 50% 84%, 0 100%);
  box-shadow:0 3px 8px rgba(0,0,0,.3); }
/* o aviso da fita (volta de leitura) */
.rv-toast{ position:fixed; left:50%; bottom:86px; transform:translateX(-50%); z-index:60;
  background:var(--wine); color:var(--gold); border:2px solid var(--gold); padding:12px 20px;
  font-family:var(--mono); font-size:.62rem; letter-spacing:.14em; text-transform:uppercase;
  box-shadow:0 8px 30px rgba(0,0,0,.4); animation:rvToast 4.2s ease forwards; }
@keyframes rvToast{ 0%{ opacity:0; transform:translate(-50%,12px);} 8%{ opacity:1; transform:translate(-50%,0);}
  86%{ opacity:1; } 100%{ opacity:0; } }
/* sala de leitura: só a revista, luz apagada */
body.rv-sala{ background:#17100c; }
body.rv-sala .warn, body.rv-sala nav.main, body.rv-sala .ticker, body.rv-sala footer,
body.rv-sala .band, body.rv-sala .ad-slot, body.rv-sala #ck-bar, body.rv-sala .cookie-bar{ display:none !important; }
body.rv-sala .rv-stage{ margin-top:20px; }
body.rv-sala .rv-lombo{ border-color:#000; }
#rv-sala-sair{ display:none; position:fixed; top:14px; right:14px; z-index:70; border:2px solid var(--gold);
  background:rgba(23,16,12,.85); color:var(--gold); font-family:var(--mono); font-size:.6rem;
  letter-spacing:.14em; text-transform:uppercase; padding:10px 14px; cursor:pointer; }
body.rv-sala #rv-sala-sair{ display:block; }
#rv-sala-sair:hover{ background:var(--gold); color:var(--wine); }
.rv-folio{ position:absolute; left:0; right:0; bottom:0; display:flex; justify-content:space-between;
  align-items:center; padding:10px 62px; border-top:1.5px solid var(--line);
  font-family:var(--mono); font-size:.52rem; letter-spacing:.18em; text-transform:uppercase;
  color:var(--ink-soft); background:var(--rv-papel); z-index:9; }
.rv-folio b{ font-family:var(--didone); font-weight:400; font-size:1.05rem; color:var(--ink); }
.rv-kicker{ display:flex; justify-content:space-between; align-items:center;
  border-bottom:2px solid var(--ink); padding:12px 22px; font-family:var(--mono);
  font-size:.54rem; font-weight:600; letter-spacing:.22em; text-transform:uppercase; }
.rv-kicker .tagz{ background:var(--wine); color:var(--gold); padding:4px 10px; }

/* ---------- CAPA: três zonas numa grade de 24 (cabeçalho, foto, texto) ---------- */
.rv-capa2{ background:var(--rv-papel); }
.rv-capa2 .nameplate{ padding:20px 24px 0; }
.rv-capa2 .nameplate img{ width:100%; display:block; }
.rv-capa2 .linha-ed{ display:flex; justify-content:space-between; align-items:center;
  margin:12px 24px 0; padding:7px 2px; border-top:2px solid var(--ink);
  border-bottom:2px solid var(--ink);
  font-family:var(--mono); font-size:.55rem; font-weight:600;
  letter-spacing:.24em; text-transform:uppercase; color:var(--wine); }
.rv-capa2 .moldura{ flex:1; min-height:440px; margin:14px 24px 0; position:relative;
  border:3px solid var(--ink); background:#14100d; }
.rv-capa2 .moldura img{ position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:center 25%; }
.rv-capa2 .cred{ position:absolute; right:0; bottom:0; font-family:var(--mono); font-size:.5rem;
  letter-spacing:.14em; text-transform:uppercase; color:#efe8da;
  background:rgba(20,6,3,.72); padding:5px 9px; }
.rv-capa2 .manchete{ padding:16px 24px 0; flex:none; }
.rv-capa2 .manchete h2{ font-family:var(--didone); font-weight:400; color:var(--ink);
  font-size:2.2rem; line-height:1.03; margin:0; display:-webkit-box;
  -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.rv-capa2 .faixa{ display:flex; flex-direction:column; justify-content:center; gap:6px;
  margin:14px 24px 0; height:82px; overflow:hidden; padding:8px 2px 6px;
  border-top:1.5px solid var(--line);
  color:var(--ink); font-family:var(--mono); font-size:.56rem; font-weight:600;
  letter-spacing:.12em; text-transform:uppercase; }
.rv-capa2 .faixa .ch{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.rv-capa2 .faixa i{ font-style:normal; color:var(--wine); margin-right:8px; }
.rv-capa2 .rodape-capa{ display:flex; justify-content:space-between; align-items:center;
  margin:0 24px; padding:10px 2px 18px; border-top:2px solid var(--ink);
  color:var(--wine); font-family:var(--mono); font-size:.52rem; letter-spacing:.2em;
  text-transform:uppercase; }
.rv-barcode{ width:74px; height:26px; background:repeating-linear-gradient(90deg,
  var(--wine) 0 2px, transparent 2px 4px, var(--wine) 4px 5px, transparent 5px 8px,
  var(--wine) 8px 11px, transparent 11px 13px); }


/* ---------- SUMÁRIO ---------- */
.rv-sum{ background:var(--rv-papel); }
.rv-sum .cab{ padding:26px 22px 14px; border-bottom:3px solid var(--ink); position:relative; }
.rv-sum .cab h3{ font-family:var(--didone); font-weight:400; font-size:2.6rem; margin:0; line-height:1; }
.rv-sum .cab span{ font-family:var(--mono); font-size:.54rem; letter-spacing:.24em;
  text-transform:uppercase; color:var(--ink-soft); }
.rv-sum .arte{ position:absolute; right:16px; top:14px; width:84px; height:60px;
  border:2px solid var(--ink); opacity:.9; }
.rv-sum ol{ list-style:none; margin:0; padding:8px 0 60px; flex:1; overflow:hidden; }
.rv-sum li{ display:grid; grid-template-columns:60px 1fr; gap:12px; align-items:baseline;
  padding:6px 22px; border-bottom:1px solid var(--line); }
.rv-sum.cheia li{ padding:4px 22px; }
.rv-sum.cheia .pt{ font-size:.72rem; }
.rv-sum.cheia .pnum{ font-size:1.2rem; }
.rv-sum .pnum{ font-family:var(--didone); font-size:1.45rem; color:var(--wine); text-align:right; }
html[data-theme="dark"] .rv-sum .pnum{ color:var(--gold); }
.rv-sum .pt{ font-weight:800; text-transform:uppercase; font-size:.8rem; line-height:1.22; }
.rv-sum .ps{ display:block; font-family:var(--mono); font-size:.54rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-soft); margin-top:3px; }

/* ---------- EDITORIAL ---------- */
.rv-edi{ }
.rv-edi .miolo{ padding:26px 30px 64px; flex:1; overflow:hidden; }
.rv-edi h3{ font-family:var(--didone); font-weight:400; font-size:2rem; line-height:1.05;
  margin:0 0 18px; }
.rv-edi .txt{ column-count:2; column-gap:26px; column-rule:1px solid var(--line);
  font-size:.8rem; line-height:1.75; text-align:justify; hyphens:auto; }
.rv-edi .txt p{ margin:0 0 12px; }
.rv-edi .txt p:first-child::first-letter{ font-family:var(--didone); font-size:3.1em;
  float:left; line-height:.8; padding:4px 8px 0 0; color:var(--wine); }
.rv-edi .miolo{ display:flex; flex-direction:column; }
.rv-edi .arte-edi{ margin-top:18px; width:100%; flex:1; min-height:120px;
  border:2px solid var(--ink); opacity:.9; }
.rv-edi .ass{ font-family:var(--mono); font-size:.6rem; letter-spacing:.18em;
  text-transform:uppercase; margin-top:16px; }

/* ---------- MATÉRIA (a íntegra, quebrada em páginas de tamanho padrão) ---------- */
.rv-mat .foto{ position:relative; aspect-ratio:16/9; flex-shrink:0; border-bottom:3px solid var(--ink); }
.rv-mat .foto img{ width:100%; height:100%; object-fit:cover; object-position:center 22%; }
.rv-mat .foto .cred{ position:absolute; right:0; bottom:0; font-family:var(--mono); font-size:.5rem;
  letter-spacing:.14em; text-transform:uppercase; color:#efe8da;
  background:rgba(20,6,3,.72); padding:5px 9px; z-index:2; }
.rv-mat .foto .cat{ position:absolute; left:0; top:0; background:var(--gold); color:var(--wine);
  font-family:var(--mono); font-size:.56rem; font-weight:700; letter-spacing:.22em;
  text-transform:uppercase; padding:7px 14px; border-right:2px solid var(--ink);
  border-bottom:2px solid var(--ink); }
.rv-mat .miolo{ padding:20px 26px 64px; flex:1; display:flex; flex-direction:column; overflow:hidden; }
.rv-mat .cont-tit{ font-family:var(--mono); font-size:.6rem; font-weight:700; letter-spacing:.18em;
  text-transform:uppercase; color:var(--wine); border-bottom:2px solid var(--gold);
  padding-bottom:8px; margin:0 0 14px; }
html[data-theme="dark"] .rv-mat .cont-tit{ color:var(--gold); }
.rv-mat.aperta .txt{ font-size:.82rem; line-height:1.7; }
.rv-mat.aperta2 .txt{ font-size:.8rem; line-height:1.64; }
.rv-mat .arte-fim{ display:none; }
.rv-mat.compl .arte-fim{ display:block; flex:1; min-height:110px; width:100%;
  border:2px solid var(--ink); opacity:.9; margin:16px 0 4px; }
.rv-mat .segue{ margin-top:auto; padding-top:12px; font-family:var(--mono); font-size:.56rem;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink-soft); }
.rv-mat h3{ font-family:var(--didone); font-weight:400; font-size:1.85rem;
  line-height:1.02; margin:0 0 10px; }
.rv-mat .linhafina{ font-size:.92rem; line-height:1.5; color:var(--ink);
  border-left:4px solid var(--gold); padding-left:12px; margin:0 0 14px; }
.rv-mat .olho{ font-style:italic; font-size:.88rem; line-height:1.65; color:var(--ink-soft);
  margin:0 0 14px; }
.rv-mat .txt{ font-size:.84rem; line-height:1.78; text-align:justify; hyphens:auto; }
.rv-mat .txt p{ margin:0 0 12px; }
.rv-mat:not(.cont) .txt > p:first-child::first-letter{ font-family:var(--didone); font-size:3em;
  float:left; line-height:.8; padding:3px 7px 0 0; color:var(--wine); }
.rv-mat .txt h2{ font-family:var(--didone); font-weight:400; font-size:1.4rem;
  margin:20px 0 8px; line-height:1.1; text-align:left; }
/* a Abril Fatface não tem negrito: strong dentro de título viraria falso-bold */
.rv-mat .txt h2 strong, .rv-mat .txt h2 b, .rv-mat h3 strong, .rv-mat h3 b{ font-weight:400; }
.rv-mat .txt figure{ margin:16px 0; }
.rv-mat .txt img{ max-width:100%; height:auto; display:block; border:2px solid var(--ink); }
.rv-mat .txt figcaption{ font-family:var(--mono); font-size:.54rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-soft); margin-top:6px; }
.rv-mat .txt blockquote{ border-left:4px solid var(--gold); margin:14px 0;
  padding:4px 0 4px 14px; font-style:italic; font-size:.9rem; }
/* a meia página vendida: o pé da última página da matéria, sempre rotulada */
.rv-mat .rv-meia{ margin-top:auto; border:2px solid var(--ink); padding:10px 12px 12px; }
.rv-mat .rv-meia em{ display:block; font-style:normal; font-family:var(--mono); font-size:.5rem;
  font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:8px; }
.rv-mat .rv-meia img{ display:block; width:100%; height:auto; max-height:380px; object-fit:contain; }
.rv-mat .rv-meia span{ display:block; font-size:.74rem; color:var(--ink-soft); margin-top:6px; }
.rv-mat .leia{ margin-top:auto; padding-top:12px; }
.rv-mat .leia a{ display:inline-block; border:2px solid var(--wine); background:var(--wine);
  color:var(--gold); text-decoration:none; font-family:var(--mono); font-weight:600;
  font-size:.56rem; letter-spacing:.18em; text-transform:uppercase; padding:10px 16px; }
.rv-mat .leia a:hover{ background:var(--gold); color:var(--wine); }

/* ---------- NA TELA (programas da semana) ---------- */
.rv-tela{ background:var(--wine); color:var(--paper); }
.rv-tela .cab{ padding:24px 22px 12px; border-bottom:2px solid var(--gold); }
.rv-tela .cab em{ display:block; font-style:normal; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.3em; text-transform:uppercase; color:var(--gold); }
.rv-tela .cab h3{ font-family:var(--didone); font-weight:400; color:var(--gold);
  font-size:2.4rem; margin:4px 0 0; line-height:1; }
.rv-tela .grade{ flex:1; overflow:hidden; display:grid; grid-template-columns:1fr 1fr;
  gap:12px; padding:16px 22px 60px; align-content:start; }
.rv-tela .ep{ border:2px solid var(--gold); text-decoration:none; color:var(--paper);
  background:rgba(0,0,0,.25); display:block; }
.rv-tela .ep img{ width:100%; aspect-ratio:16/9; object-fit:cover; display:block;
  border-bottom:2px solid var(--gold); }
.rv-tela .ep .pr{ font-family:var(--mono); font-size:.5rem; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase; color:var(--gold); padding:8px 10px 2px; display:block; }
.rv-tela .ep .tt{ font-size:.68rem; font-weight:700; line-height:1.3; padding:0 10px 10px; display:block; }
.rv-tela .ep:hover{ background:rgba(206,178,106,.15); }
.rv-tela .canal-cta{ padding:0 22px 54px; }
.rv-tela .canal-cta a{ display:inline-block; border:2px solid var(--gold); color:var(--gold);
  text-decoration:none; font-family:var(--mono); font-size:.58rem; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase; padding:11px 18px; }
.rv-tela .canal-cta a:hover{ background:var(--gold); color:var(--wine); }
.rv-tela .rv-folio{ background:var(--wine); color:var(--gold); border-top-color:var(--gold); }
.rv-tela .rv-folio b{ color:var(--gold); }
/* semana curta: até 3 episódios ganham cartão horizontal com a capa INTEIRA */
.rv-tela .ep .mt{ display:contents; }
.rv-tela .grade.poucos{ grid-template-columns:1fr; align-content:center; gap:16px; }
.rv-tela .grade.poucos .ep{ display:flex; align-items:stretch; }
.rv-tela .grade.poucos .ep img{ width:300px; height:auto; aspect-ratio:16/9; object-fit:cover;
  flex-shrink:0; border-right:2px solid var(--gold); }
.rv-tela .grade.poucos .ep .mt{ display:flex; flex-direction:column; justify-content:center;
  gap:7px; padding:12px 18px; }
.rv-tela .grade.poucos .ep .pr{ font-size:.56rem; padding:0; }
.rv-tela .grade.poucos .ep .tt{ font-size:.92rem; line-height:1.35; padding:0; }
/* thumb que não carrega mostra o pano da casa, não um ícone quebrado */
.rv-tela .ep img{ background:linear-gradient(135deg, #3a0b07 0 40%, #5a1610 40% 60%, #3a0b07 60%);
  color:transparent; }

/* ---------- PROGRAMA DE SALA (o playbill da estreia) ---------- */
.rv-prog{ background:var(--rv-papel); }
.rv-prog .borda{ flex:1; margin:18px; border:3px double var(--gold); outline:1px solid var(--gold);
  outline-offset:-9px; padding:26px 28px 60px; display:flex; flex-direction:column; overflow:hidden; }
.rv-prog em.rot{ font-style:normal; font-family:var(--mono); font-size:.54rem; letter-spacing:.3em;
  text-transform:uppercase; color:var(--wine); text-align:center; }
html[data-theme="dark"] .rv-prog em.rot{ color:var(--gold); }
.rv-prog h3{ font-family:var(--didone); font-weight:400; font-size:2rem; line-height:1.05;
  text-align:center; margin:10px 0 4px; }
.rv-prog .sub{ text-align:center; font-size:.85rem; color:var(--ink-soft); margin:0 0 6px; }
.rv-prog .sinopse{ text-align:center; font-style:italic; font-size:.86rem; line-height:1.6;
  color:var(--ink-soft); max-width:440px; margin:10px auto 4px; }
.rv-prog .colunas{ margin-bottom:auto; }
.rv-prog .colunas{ display:grid; grid-template-columns:1fr 1fr; gap:0 26px; margin-top:14px; }
.rv-prog h4{ font-family:var(--mono); font-size:.56rem; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:var(--wine); border-bottom:2px solid var(--gold);
  padding-bottom:5px; margin:10px 0 8px; }
html[data-theme="dark"] .rv-prog h4{ color:var(--gold); }
.rv-prog ul{ list-style:none; margin:0; padding:0; }
.rv-prog .elenco li{ padding:4px 0; font-size:.8rem; border-bottom:1px dotted rgba(78,15,9,.25); }
.rv-prog .elenco li i{ font-style:normal; color:var(--ink-soft); display:block; font-size:.68rem; }
.rv-prog .fichat li{ display:flex; justify-content:space-between; gap:10px; padding:4px 0;
  font-size:.74rem; border-bottom:1px dotted rgba(78,15,9,.25); }
.rv-prog .fichat em{ font-style:normal; color:var(--ink-soft); flex-shrink:0; }
.rv-prog .fichat span{ text-align:right; font-weight:600; }
.rv-prog .serv{ margin-top:auto; padding-top:14px; text-align:center; font-family:var(--mono);
  font-size:.6rem; letter-spacing:.08em; color:var(--ink-soft); }

/* ---------- CARTAS DA PLATEIA ---------- */
.rv-cartas .cab{ padding:24px 22px 12px; border-bottom:3px solid var(--ink); }
.rv-cartas .cab em{ display:block; font-style:normal; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.26em; text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-cartas .cab em{ color:var(--gold); }
.rv-cartas .cab h3{ font-family:var(--didone); font-weight:400; font-size:2.3rem; margin:4px 0 0; line-height:1; }
.rv-cartas .lista{ flex:1; padding:16px 22px; display:flex; flex-direction:column; gap:14px; overflow:hidden; }
.rv-cartas .carta{ border-left:4px solid var(--gold); padding:8px 0 8px 16px; }
.rv-cartas .carta .tx{ font-size:.85rem; line-height:1.7; margin:0; }
.rv-cartas .carta .ass{ font-family:var(--mono); font-size:.56rem; font-weight:700; letter-spacing:.16em;
  text-transform:uppercase; color:var(--wine); margin:8px 0 0; }
html[data-theme="dark"] .rv-cartas .carta .ass{ color:var(--gold); }
.rv-cartas .carta .resp{ margin:8px 0 0; padding:8px 12px; background:rgba(206,178,106,.14);
  font-size:.78rem; line-height:1.6; }
.rv-cartas .carta .resp span{ display:block; font-family:var(--mono); font-size:.52rem;
  letter-spacing:.2em; text-transform:uppercase; color:var(--ink-soft); margin-top:4px; }
.rv-cartas .convite{ margin:0 22px 54px; padding-top:10px; border-top:2px solid var(--ink);
  font-family:var(--mono); font-size:.58rem; letter-spacing:.06em; color:var(--ink-soft); }

/* ---------- TRÊS PERGUNTAS (exclusiva da revista) ---------- */
.rv-3p .miolo{ flex:1; padding:20px 28px 60px; display:flex; flex-direction:column; overflow:hidden; }
.rv-3p em.rot{ font-style:normal; font-family:var(--mono); font-size:.56rem; letter-spacing:.3em;
  text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-3p em.rot{ color:var(--gold); }
.rv-3p h3{ font-family:var(--didone); font-weight:400; font-size:2.4rem; line-height:1; margin:6px 0 4px; }
.rv-3p .quem{ font-size:.85rem; color:var(--ink-soft); margin:0 0 14px; }
.rv-3p .par{ margin-bottom:14px; }
.rv-3p .pp{ font-family:var(--didone); font-size:1.15rem; line-height:1.25; margin:0 0 6px; color:var(--wine); }
html[data-theme="dark"] .rv-3p .pp{ color:var(--gold); }
.rv-3p .pp b{ font-weight:400; color:var(--gold); margin-right:4px; }
.rv-3p .rr{ font-size:.88rem; line-height:1.7; margin:0; border-left:3px solid var(--gold); padding-left:14px; }
.rv-3p .nota{ margin-top:auto; padding-top:12px; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.1em; color:var(--ink-soft); }

/* ---------- O BILHETE DA SEMANA (abre a agenda) ---------- */
.rv-bsem{ display:flex; align-items:stretch; margin:14px 22px 4px; position:relative;
  border:2px dashed var(--wine); background:rgba(206,178,106,.1); }
.rv-bsem .bs-esq{ flex:1; padding:12px 16px; display:flex; flex-direction:column; gap:3px; }
.rv-bsem .bs-esq em{ font-style:normal; font-family:var(--mono); font-size:.5rem; letter-spacing:.26em;
  text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-bsem .bs-esq em{ color:var(--gold); }
.rv-bsem .bs-esq b{ font-family:var(--didone); font-weight:400; font-size:1.2rem; line-height:1.1; }
.rv-bsem .bs-esq span{ font-family:var(--mono); font-size:.58rem; color:var(--ink-soft); }
.rv-bsem .bs-esq i{ font-style:italic; font-size:.74rem; line-height:1.45; color:var(--ink-soft); margin-top:2px; }
.rv-bsem .bs-dir{ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;
  padding:10px 14px; border-left:2px dashed var(--wine); min-width:96px; text-align:center; }
.rv-bsem .bs-dir em{ font-style:normal; font-family:var(--mono); font-size:.48rem; letter-spacing:.2em;
  text-transform:uppercase; color:var(--ink-soft); }
.rv-bsem .bs-dir strong{ font-family:var(--mono); font-size:.6rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-bsem .bs-dir strong{ color:var(--gold); }

/* ---------- ANUNCIE (expediente) ---------- */
.rv-exp .anuncie{ margin-top:18px; border:2px solid var(--wine); padding:12px 14px; }
.rv-exp .anuncie em{ display:block; font-style:normal; font-family:var(--mono); font-size:.56rem;
  font-weight:700; letter-spacing:.24em; text-transform:uppercase; color:var(--wine); margin-bottom:5px; }
html[data-theme="dark"] .rv-exp .anuncie{ border-color:var(--gold); }
html[data-theme="dark"] .rv-exp .anuncie em{ color:var(--gold); }
.rv-exp .anuncie p{ margin:0; font-size:.72rem; line-height:1.55; }
.rv-exp .anuncie a{ color:var(--wine); font-weight:700; }
html[data-theme="dark"] .rv-exp .anuncie a{ color:var(--gold); }

/* ---------- AGENDA DA SEMANA ---------- */
.rv-agd .cab{ padding:24px 22px 12px; border-bottom:3px solid var(--ink); }
.rv-agd .cab em{ display:block; font-style:normal; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.3em; text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-agd .cab em{ color:var(--gold); }
.rv-agd .cab h3{ font-family:var(--didone); font-weight:400; font-size:2.3rem; margin:4px 0 0; line-height:1; }
.rv-agd .cab h3 .cid{ display:block; color:var(--wine); font-size:1.5rem; margin-top:2px; }
html[data-theme="dark"] .rv-agd .cab h3 .cid{ color:var(--gold); }
.rv-agd .lista{ flex:1; overflow:hidden; padding:6px 0 60px; }
.rv-agd .ag-item{ display:grid; grid-template-columns:74px 1fr; gap:14px; align-items:center;
  padding:12px 22px; border-bottom:1px solid var(--line); text-decoration:none; color:var(--ink); }
.rv-agd .ag-item:hover{ background:var(--paper-2); }
.rv-agd .ag-dia{ font-family:var(--didone); font-size:1.35rem; color:var(--wine); text-align:right;
  border-right:3px solid var(--gold); padding-right:12px; }
html[data-theme="dark"] .rv-agd .ag-dia{ color:var(--gold); }
.rv-agd .ag-oq b{ display:block; font-size:.85rem; line-height:1.3; font-weight:800; }
.rv-agd .ag-item.cur{ align-items:start; }
.rv-agd .ag-item.cur .ag-dia{ font-size:.98rem; line-height:1.25; padding-top:2px; }
.rv-agd .ag-oq i{ display:block; font-style:normal; font-size:.76rem; line-height:1.5;
  color:var(--ink-soft); margin-top:3px; }
.rv-agd .ag-oq small{ display:block; font-family:var(--mono); font-size:.56rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-soft); margin-top:3px; }
.rv-agd .ag-vazio{ padding:22px; font-size:.9rem; color:var(--ink-soft); }
.rv-agd .ag-cta{ padding:10px 22px 54px; }
.rv-agd .ag-cta a{ display:inline-block; border:2px solid var(--wine); color:var(--wine);
  text-decoration:none; font-family:var(--mono); font-size:.58rem; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase; padding:11px 16px; }
.rv-agd .ag-cta a:hover{ background:var(--wine); color:var(--gold); }

/* ---------- ENTRE MESTRES (frase célebre) ---------- */
/* o ator sob o refletor cobre a página como marca d'água; a frase, legível, por cima */
.rv-mestre .fundo{ position:absolute; inset:0; width:100%; height:100%; opacity:.2;
  z-index:0; pointer-events:none; }
.rv-mestre .rv-kicker, .rv-mestre .miolo, .rv-mestre .rv-folio{ position:relative; z-index:1; }
.rv-mestre .miolo{ flex:1; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding:6% 9% 64px; }
.rv-mestre .aspa{ font-family:var(--didone); font-size:6.5rem; line-height:.55; color:var(--gold); }
.rv-mestre .fr{ font-family:var(--didone); font-weight:400; font-size:clamp(1.5rem,4.6vw,2.4rem);
  line-height:1.16; margin-top:8px; }
.rv-mestre .au{ font-family:var(--mono); font-size:.64rem; font-weight:700; letter-spacing:.24em;
  text-transform:uppercase; color:var(--wine); margin-top:26px; }
html[data-theme="dark"] .rv-mestre .au{ color:var(--gold); }
.rv-mestre .bio{ font-size:.8rem; color:var(--ink-soft); margin-top:6px; }

/* ---------- CITAÇÃO ---------- */
.rv-cit{ background:var(--wine); color:var(--gold); align-items:center; justify-content:center;
  text-align:center; padding:8% 9%; }
.rv-cit .aspa{ font-family:var(--didone); font-size:7rem; line-height:.6; opacity:.5; }
.rv-cit .fr{ font-family:var(--didone); font-size:2.2rem; line-height:1.14; }
.rv-cit .au{ font-family:var(--mono); font-size:.58rem; letter-spacing:.22em;
  text-transform:uppercase; margin-top:26px; color:var(--paper); }
.rv-cit .arte{ width:120px; height:80px; border:2px solid var(--gold); margin-top:30px; opacity:.85; }

/* ---------- CARTAZ / PATROCÍNIO ---------- */
.rv-cartaz{ }
.rv-cartaz img{ flex:1; width:100%; object-fit:contain; background:var(--paper-2); min-height:0; }
.rv-cartaz .rv-leg{ padding:12px 22px 42px; border-top:2px solid var(--ink);
  font-family:var(--mono); font-size:.6rem; letter-spacing:.14em; text-transform:uppercase; }
.rv-pat{ outline:8px double var(--gold); outline-offset:-16px; }
/* o bilhete do leitor: cupom destacável dentro do anúncio */
.rv-bilhete{ display:flex; align-items:stretch; margin:0 18px 12px; position:relative;
  border:2px dashed var(--wine); background:var(--paper); }
.rv-bilhete::before{ content:'✂'; position:absolute; top:-13px; left:16px; color:var(--wine);
  background:var(--paper); padding:0 5px; font-size:.85rem; }
.rv-bilhete .rb-esq{ flex:1; padding:14px 16px; display:flex; flex-direction:column; gap:3px; }
.rv-bilhete .rb-esq b{ font-family:var(--didone); font-weight:400; font-size:1.15rem; line-height:1.1; }
.rv-bilhete .rb-esq span{ font-size:.72rem; color:var(--ink-soft); line-height:1.45; }
.rv-bilhete .rb-esq i{ font-style:normal; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin-top:3px; }
.rv-bilhete .rb-dir{ display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:2px; padding:12px 18px; border:0; border-left:2px dashed var(--wine); background:rgba(206,178,106,.16);
  min-width:132px; text-align:center; color:inherit; cursor:pointer; }
.rv-bilhete .rb-dir:hover{ background:rgba(206,178,106,.3); }
.rv-bilhete .rb-dir em{ font-style:normal; font-family:var(--mono); font-size:.5rem;
  letter-spacing:.26em; text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-bilhete .rb-dir em{ color:var(--gold); }
.rv-bilhete .rb-dir strong{ font-family:var(--mono); font-weight:700; font-size:1.05rem;
  letter-spacing:.08em; }

/* ---------- EXPEDIENTE ---------- */
.rv-exp .miolo{ padding:26px 30px 64px; flex:1; overflow:hidden; }
.rv-exp img{ width:120px; margin-bottom:18px; }
.rv-exp img.only-dark{ display:none; }
:root[data-theme="dark"] .rv-exp img.only-light{ display:none; }
:root[data-theme="dark"] .rv-exp img.only-dark{ display:inline-block; }
@media (prefers-color-scheme: dark){
  :root:not([data-theme]) .rv-exp img.only-light{ display:none; }
  :root:not([data-theme]) .rv-exp img.only-dark{ display:inline-block; }
}
.rv-exp h4{ font-family:var(--mono); font-size:.56rem; letter-spacing:.24em;
  text-transform:uppercase; color:var(--ink-soft); margin:18px 0 6px; border-bottom:1px solid var(--line);
  padding-bottom:4px; }
.rv-exp ul{ list-style:none; margin:0; padding:0; line-height:2; font-size:.82rem; }
.rv-exp p{ font-size:.72rem; line-height:1.8; color:var(--ink-soft); }

/* ---------- PÁGINA LIVRE / EXCLUSIVA ---------- */
.rv-livre .miolo{ padding:24px 28px 64px; flex:1; overflow:hidden; }
.rv-livre h3{ font-family:var(--didone); font-weight:400; font-size:1.9rem; line-height:1.05; margin:0 0 12px; }
.rv-livre .txt{ column-count:2; column-gap:24px; column-rule:1px solid var(--line);
  font-size:.78rem; line-height:1.72; text-align:justify; hyphens:auto; }
.rv-livre .txt p{ margin:0 0 11px; }

/* ---------- RECORTES DA SEMANA ---------- */
.rv-rec .cab{ padding:24px 22px 12px; border-bottom:3px solid var(--ink); }
.rv-rec .cab em{ display:block; font-style:normal; font-family:var(--mono); font-size:.54rem;
  letter-spacing:.3em; text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-rec .cab em{ color:var(--gold); }
.rv-rec .cab h3{ font-family:var(--didone); font-weight:400; font-size:2.3rem; margin:4px 0 0; line-height:1; }
.rv-rec .mural{ flex:1; overflow:hidden; padding:22px 26px 64px; display:flex; flex-direction:column;
  gap:18px; justify-content:center; }
.rv-rec .rec{ position:relative; background:#f6f0e2; border:1px solid #d8cdb4; padding:18px 20px 14px;
  box-shadow:2px 3px 10px rgba(35,8,5,.14); max-width:92%; }
html[data-theme="dark"] .rv-rec .rec{ background:#241e16; border-color:#3a3226; }
.rv-rec .rec:nth-child(odd){ transform:rotate(-1.2deg); align-self:flex-start; }
.rv-rec .rec:nth-child(even){ transform:rotate(1deg); align-self:flex-end; }
.rv-rec .rec::before{ content:''; position:absolute; top:-9px; left:50%; transform:translateX(-50%) rotate(-2deg);
  width:74px; height:18px; background:rgba(206,178,106,.4); border:1px solid rgba(158,132,72,.35); }
.rv-rec .rec .fr{ font-family:var(--didone); font-size:1.02rem; line-height:1.34; }
.rv-rec .rec .fr::before{ content:'“'; color:var(--wine); }
.rv-rec .rec .fr::after{ content:'”'; color:var(--wine); }
html[data-theme="dark"] .rv-rec .rec .fr::before, html[data-theme="dark"] .rv-rec .rec .fr::after{ color:var(--gold); }
.rv-rec .rec .qm{ margin-top:8px; font-family:var(--mono); font-size:.55rem; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:var(--wine); }
html[data-theme="dark"] .rv-rec .rec .qm{ color:var(--gold); }
.rv-rec .rec .qm i{ font-style:normal; font-weight:400; color:var(--ink-soft); display:block; margin-top:2px; }
.rv-rec .rec a{ color:inherit; text-decoration:none; }

/* ---------- CONTRACAPA ---------- */
.rv-back{ background:var(--wine); color:var(--paper); }
.rv-back .miolo{ flex:1; display:flex; flex-direction:column; padding:30px 30px 20px; }
.rv-back em.rot{ font-style:normal; font-family:var(--mono); font-size:.56rem; letter-spacing:.3em;
  text-transform:uppercase; color:var(--gold); }
.rv-back h3{ font-family:var(--didone); font-weight:400; color:var(--gold); font-size:2.2rem;
  line-height:1.02; margin:6px 0 18px; }
.rv-back ul.prox{ list-style:none; margin:0; padding:0; }
.rv-back ul.prox li{ padding:10px 0; border-bottom:1px solid rgba(206,178,106,.35);
  font-size:.9rem; line-height:1.4; }
.rv-back ul.prox li::before{ content:'✦ '; color:var(--gold); }
/* a citação é o centro da contracapa: didone grande entre filetes dourados */
.rv-back .desp{ margin-top:auto; margin-bottom:auto; text-align:center; padding:28px 10px; }
.rv-back .desp::before, .rv-back .desp::after{ content:''; display:block; width:120px; height:2px;
  background:var(--gold); margin:0 auto; }
.rv-back .desp::before{ margin-bottom:22px; }
.rv-back .desp::after{ margin-top:22px; }
.rv-back .desp .fr{ font-family:var(--didone); font-size:2.5rem; line-height:1.14; color:var(--paper); }
.rv-back .desp .au{ font-family:var(--mono); font-size:.56rem; letter-spacing:.22em; text-transform:uppercase;
  color:var(--gold); margin-top:16px; }
.rv-back .rodape{ display:flex; justify-content:space-between; align-items:center; margin-top:22px;
  padding-top:14px; border-top:2px solid var(--gold); font-family:var(--mono); font-size:.52rem;
  letter-spacing:.2em; text-transform:uppercase; color:var(--gold); }
.rv-back .rodape img{ height:34px; }

/* as quinas de virar página: voltar na ponta esquerda, avançar na direita */
.rv-quina{ position:absolute; bottom:6px; z-index:12; width:44px; height:44px;
  border:0; background:none; color:var(--ink-soft); cursor:pointer;
  font-size:.8rem; line-height:1; display:flex; align-items:center; justify-content:center;
  transition:color .15s, transform .12s; }
.rv-quina:hover{ color:var(--wine); transform:translateY(-1px); }
.rv-quina:focus-visible{ outline:3px solid var(--gold); }
.rv-quina.esq{ left:10px; }
.rv-quina.dir{ right:10px; }
.rv-quina[hidden]{ display:none; }
html[data-theme="dark"] .rv-quina{ color:var(--gold); }
@media print{ .rv-quina{ display:none !important; } }

/* ---------- A CORTINA (janela do assinante) ---------- */
.rv-cortina{ position:fixed; inset:0; z-index:210; display:flex; align-items:center;
  justify-content:center; padding:18px;
  background:
    radial-gradient(140% 90% at 50% -20%, rgba(0,0,0,.35), transparent 60%),
    repeating-linear-gradient(90deg, #4E0F09 0 46px, #3a0b06 46px 92px);
  animation:ctFundo .3s ease; }
@keyframes ctFundo{ from{ opacity:0; } }
.rv-cortina[hidden]{ display:none; }
.ct-caixa{ width:min(540px, 100%); background:var(--paper); border:3px solid var(--ink);
  box-shadow:0 26px 80px rgba(0,0,0,.55); padding:34px 36px 26px; display:flex;
  flex-direction:column; gap:12px; animation:ctSobe .34s ease; }
@keyframes ctSobe{ from{ opacity:0; transform:translateY(16px); } }
@media (prefers-reduced-motion:reduce){ .rv-cortina, .ct-caixa{ animation:none; } }
.ct-rot{ font-family:var(--mono); font-size:.6rem; letter-spacing:.24em; text-transform:uppercase;
  color:var(--wine); }
.ct-caixa h3{ font-family:var(--didone); font-weight:400; font-size:clamp(1.4rem,4vw,1.9rem);
  line-height:1.08; margin:0; }
.ct-caixa p{ margin:0; font-size:.9rem; line-height:1.55; color:var(--ink-soft); }
.ct-ja label{ display:block; font-family:var(--mono); font-size:.58rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-soft); margin-bottom:6px; }
.ct-linha{ display:flex; gap:8px; }
.ct-linha input{ flex:1; border:2px solid var(--ink); background:var(--paper); color:var(--ink);
  font-family:var(--sans); font-size:.9rem; padding:11px 12px; min-width:0; }
.ct-linha input:focus{ outline:2px solid var(--gold); outline-offset:-2px; }
.ct-linha button{ border:2px solid var(--ink); background:var(--ink); color:var(--gold);
  font-family:var(--mono); font-weight:700; font-size:.64rem; letter-spacing:.14em;
  text-transform:uppercase; padding:11px 18px; cursor:pointer; }
.ct-linha button:hover{ background:var(--wine); border-color:var(--wine); }
.ct-erro{ font-family:var(--mono); font-size:.6rem; color:var(--wine); min-height:1em; }
.ct-ou{ display:flex; align-items:center; gap:10px; color:var(--ink-soft);
  font-family:var(--mono); font-size:.56rem; letter-spacing:.2em; text-transform:uppercase; }
.ct-ou::before, .ct-ou::after{ content:''; flex:1; border-top:1px solid var(--line); }
.ct-assinar{ border:2px solid var(--wine); background:var(--wine); color:var(--gold); cursor:pointer;
  font-family:var(--mono); font-weight:700; font-size:.7rem; letter-spacing:.16em;
  text-transform:uppercase; padding:15px; transition:transform .15s; }
.ct-assinar:hover{ transform:translateY(-2px); background:var(--ink); border-color:var(--ink); }
.ct-voltar{ border:0; background:none; color:var(--ink-soft); cursor:pointer; align-self:center;
  font-family:var(--mono); font-size:.6rem; letter-spacing:.12em; text-transform:uppercase; padding:4px; }
.ct-voltar:hover{ color:var(--wine); }

/* ---------- NAVEGAÇÃO ---------- */
.rv-nav{ position:sticky; bottom:14px; display:flex; justify-content:center; gap:8px;
  width:max-content; max-width:100%; margin:18px auto 0; padding:8px;
  background:var(--paper); border:2px solid var(--ink); box-shadow:0 6px 22px rgba(0,0,0,.22); }
.rv-nav button{ border:2px solid var(--ink); background:var(--paper); color:var(--ink); cursor:pointer;
  font-family:var(--mono); font-weight:600; font-size:.64rem; letter-spacing:.12em;
  text-transform:uppercase; padding:12px 16px; }
.rv-nav button:hover{ background:var(--ink); color:var(--gold); }
.rv-nav .ct{ border:2px solid var(--ink); background:var(--gold); color:var(--wine);
  font-family:var(--mono); font-weight:600; font-size:.64rem; letter-spacing:.12em; padding:12px 14px; }
@media (max-width:560px){
  .rv-edi .txt, .rv-livre .txt{ column-count:1; }
}
@media print{
  /* no papel, as mesmas páginas da tela: 720x972, uma por folha */
  .rv-book{ display:block !important; perspective:none !important; transform:none !important; }
  .rv-palco{ height:auto !important; }
  .rv-stage{ max-width:100% !important; margin:0 !important; padding:0 !important; }
  .rv-pg{ display:flex !important; flex-direction:column !important; page-break-after:always;
    break-inside:avoid; width:720px !important; height:972px !important; margin:0 auto;
    transform:none !important; animation:none !important; position:relative; }
  body.rv-em-janela .rv-pg{ display:none !important; }
  body.rv-em-janela .rv-pg.rv-amostra{ display:flex !important; }
  .rv-pg::before{ display:none; }
  .rv-nav, nav.main, .ticker, footer, .warn, .rv-lombo, .rv-fita, .rv-canto,
  #rv-sala-sair, .rv-toast, .rv-cortina, .cv-overlay, .cv-band, #lgpd{ display:none !important; }
}
</style>'''

def _rv_folio(ed, num, escuro=False):
    return (f'<div class="rv-folio"><span>FOYER · A REVISTA · Nº {_rvesc(ed.get("numero"))}</span>'
            f'<b>{num}</b><span>{_rvesc(ed.get("dataEdicao", ""))}</span></div>')

_RV_ARTES = ['ph-1', 'ph-2', 'ph-3', 'ph-4', 'ph-5', 'ph-6']

def _rv_quebra_corpo(corpo):
    """Divide o corpo em páginas de tamanho padrão. Modelo de ALTURA (px numa
    página de 740px de largura): texto ~95 caracteres por linha de 27px;
    foto no corpo ~430px; vídeo ~450px. O leitor faz o ajuste fino no
    navegador (puxa blocos da página seguinte quando sobra espaço)."""
    partes = _re.split(r'(?<=</p>)|(?<=</h2>)|(?<=</h3>)|(?<=</figure>)|(?<=</blockquote>)', corpo)
    blocos = [p for p in partes if p.strip()]
    def altura(b):
        if '<figure' in b or '<img' in b:
            return 440
        if '<iframe' in b or 'art-video' in b or 'art-spotify' in b:
            return 460
        txt = _re.sub(r'<[^>]+>', '', b)
        linhas = max(1, -(-len(txt) // 95))
        alt = linhas * 27 + 14
        if '<h2' in b or '<h3' in b:
            alt += 46
        if '<blockquote' in b:
            alt += 20
        return alt
    ALT_PRIMEIRA, ALT_CONT = 270, 700
    def eh_titulo(b):
        return bool(_re.match(r'\s*<h[23][\s>]', b))
    # a ficha de Serviço é indivisível: do intertítulo ao fim, tudo na mesma página
    unidade_servico = None
    for i, b in enumerate(blocos):
        if eh_titulo(b) and 'servi' in _re.sub(r'<[^>]+>', '', b).lower():
            resto = blocos[i:]
            if sum(altura(x) for x in resto) <= ALT_CONT:
                # marca os blocos para o leitor não os separar na repaginação fina
                unidade_servico = [_re.sub(r'^(\s*<\w+)', r'\1 data-junto="1"', x) for x in resto]
                blocos = blocos[:i]
            break
    # intertítulo nunca fecha página sozinho: carrega o bloco seguinte consigo
    unidades = []
    i = 0
    while i < len(blocos):
        if eh_titulo(blocos[i]) and i + 1 < len(blocos):
            unidades.append([blocos[i], blocos[i + 1]])
            i += 2
        else:
            unidades.append([blocos[i]])
            i += 1
    if unidade_servico:
        unidades.append(unidade_servico)
    paginas, atual, carga, lim = [], [], 0, ALT_PRIMEIRA
    for u in unidades:
        au = sum(altura(b) for b in u)
        if atual and carga + au > lim:
            paginas.append(''.join(atual))
            atual, carga, lim = [], 0, ALT_CONT
        atual.extend(u)
        carga += au
    if atual:
        paginas.append(''.join(atual))
    return paginas or ['']

def _rv_corpo(slug, img):
    """Corpo completo da matéria (mesmo texto do site), sem repetir a foto de capa."""
    path = os.path.join(ROOT, 'import/corpo', (slug or '') + '.html')
    if not os.path.exists(path):
        return ''
    corpo = open(path).read()
    if img:
        pat = _re.compile(r'<figure class="art-img"><img src="' + _re.escape(img) +
                          r'"[^>]*>(?:<figcaption>.*?</figcaption>)?</figure>\s*', _re.S)
        corpo = pat.sub('', corpo, count=1)
    return corpo

# frases REAIS e verificadas de mestres das artes e da filosofia (rotativas por edição)
_RV_MESTRES = [
    ('O mundo inteiro é um palco, e todos os homens e mulheres não passam de atores.',
     'William Shakespeare', 'Em "Como Gostais", cerca de 1599'),
    ('A vida imita a arte muito mais do que a arte imita a vida.',
     'Oscar Wilde', 'No ensaio "A Decadência da Mentira", 1889'),
    ('Temos a arte para não morrer da verdade.',
     'Friedrich Nietzsche', 'Filósofo alemão, em fragmento de 1888'),
    ('O teatro não é o país da realidade: é o país do verdadeiro.',
     'Victor Hugo', 'Escritor francês, autor de "Os Miseráveis"'),
    ('O dever da comédia é corrigir os homens, divertindo-os.',
     'Molière', 'Dramaturgo francês, no prefácio de "Tartufo", 1664'),
    ('Ame a arte em você, e não você na arte.',
     'Constantin Stanislavski', 'Diretor russo, pai da atuação moderna'),
    ('O sonho é que leva a gente para frente.',
     'Ariano Suassuna', 'Dramaturgo de "O Auto da Compadecida"'),
    ('Toda unanimidade é burra.',
     'Nelson Rodrigues', 'Dramaturgo de "Vestido de Noiva"'),
]

_MES_PT = {'jan': 1, 'fev': 2, 'feb': 2, 'mar': 3, 'abr': 4, 'apr': 4, 'mai': 5, 'may': 5,
           'jun': 6, 'jul': 7, 'ago': 8, 'aug': 8, 'set': 9, 'sep': 9, 'out': 10, 'oct': 10,
           'nov': 11, 'dez': 12, 'dec': 12}

def _rv_iso_edicao(ed):
    """Data de fechamento da edição em ISO. Uma edição fechada é um objeto
    parado no tempo: nada publicado depois dela pode entrar, nem em rebuild."""
    txt = str(ed.get('dataEdicao', '')).strip()
    m = _re.match(r'(\d{1,2})\s+([A-Za-zç]{3})\w*\.?\s+(\d{4})', txt)
    if m and m.group(2).lower()[:3] in _MES_PT:
        return f'{int(m.group(3)):04d}-{_MES_PT[m.group(2).lower()[:3]]:02d}-{int(m.group(1)):02d}'
    return None

def _rv_agenda_itens(ref=None):
    """Agenda dinâmica da revista: eventos reais em cartaz de hoje a quinta que vem
    (ou da data de fechamento da edição, quando ela existe)."""
    _ini = ref or datetime.now(timezone.utc).date()
    _fim = _ini + __import__('datetime').timedelta(days=7)
    itens = []
    for m in MATERIAS:
        ev = m.get('evento') or {}
        if not ev.get('inicio'):
            continue
        e_ini, e_fim = ev['inicio'], ev.get('fim') or ev['inicio']
        if e_fim < _ini.isoformat() or e_ini > _fim.isoformat():
            continue
        itens.append((e_ini, e_fim, m))
    itens.sort(key=lambda x: (x[0], x[1]))
    return itens[:9]

def _rv_data_curta(iso):
    try:
        _y, _m, _d = iso.split('-')
        return f'{_d}/{_m}'
    except Exception:
        return iso

def _rv_rotulo_sumario(pg):
    t = pg.get('tipo')
    if t == 'editorial': return (pg.get('titulo') or 'Carta ao leitor', 'Editorial')
    if t == 'materia': return (pg.get('titulo', ''), 'A semana · ' + (pg.get('cat') or 'FOYER'))
    if t == 'exclusiva': return (pg.get('titulo', ''), 'Exclusivo da revista')
    if t == 'programas': return ('Na tela: os programas da semana', 'YouTube do FOYER')
    if t == 'agenda':
        cid = pg.get('cidade')
        return ((f'A semana em cartaz: {cid}' if cid else 'A semana em cartaz'), 'Agenda')
    if t == 'frase-celebre': return ('Entre mestres: a arte pela palavra', 'Exclusivo')
    if t == 'citacao': return ('A frase da semana', 'Entre aspas')
    if t == 'cartaz': return (pg.get('legenda') or 'Cartaz', 'Divulgação')
    if t == 'patrocinio': return (pg.get('legenda') or 'Página patrocinada', 'Publicidade')
    if t == 'expediente': return ('Expediente', 'Quem faz o FOYER')
    if t == 'recortes': return ('Recortes: o que disseram na semana', 'Entre aspas')
    if t == 'programa-sala': return (pg.get('titulo') or 'Programa de sala', 'Programa de sala')
    if t == 'cartas': return ('Cartas da plateia', 'O correio da revista')
    if t == 'tres-perguntas': return (f'Três perguntas para {pg.get("entrevistado", "")}'.strip(), 'Exclusivo da revista')
    if t == 'contracapa': return ('A cortina desce', 'Contracapa')
    return (pg.get('titulo', 'Página'), pg.get('rotulo', ''))

def _rv_pagina(pg, ed, num):
    t = pg.get('tipo', 'livre')
    fol = _rv_folio(ed, num)
    if t == 'editorial':
        arte_edi = _RV_ARTES[(int(ed.get('numero', 1)) + 2) % len(_RV_ARTES)]
        return (f'<section class="rv-pg rv-edi"><div class="rv-kicker"><span class="tagz">Editorial</span>'
                f'<span>Carta ao leitor</span></div><div class="miolo">'
                f'<h3>{_rvesc(pg.get("titulo"))}</h3>'
                f'<div class="txt">{md_lite(pg.get("texto", ""))}</div>'
                f'<p class="ass">{_rvesc(pg.get("assinatura") or "A direção do FOYER")}</p>'
                f'<svg class="arte-edi" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice">'
                f'<use href="#{arte_edi}"/></svg>'
                f'</div>{fol}</section>')
    if t == 'materia':
        # o crédito da foto de abertura: o expediente promete, a página cumpre
        cred_foto = (pg.get('imgCredito') or '').strip()
        if not cred_foto and pg.get('slug'):
            _mm = next((m for m in MATERIAS if m.get('slug') == pg.get('slug')), None)
            if _mm and (_mm.get('credito') or '').strip():
                cred_foto = _cred_curto(_mm)
        img = (f'<div class="foto"><img src="{_rvesc(wiximg(pg.get("img", ""), 1200, 700))}" alt="" '
               f'onerror="this.style.display=\'none\'"><span class="cat">{_rvesc(pg.get("cat") or "FOYER")}</span>'
               + (f'<span class="cred">Foto — {_rvesc(cred_foto)}</span>' if cred_foto else '')
               + '</div>') if pg.get('img') else ''
        leia = (f'<div class="leia"><a href="post-{_rvesc(pg.get("slug"))}.html">Abrir esta matéria no site →</a></div>'
                ) if pg.get('slug') else ''
        # a matéria INTEIRA mora na revista, quebrada em páginas de tamanho padrão
        corpo = _rv_corpo(pg.get('slug'), pg.get('img'))
        # sem eco na abertura: o h2 inicial do post é o subtítulo do site, e a
        # revista já tem título e linha fina próprios; ele sai sempre
        _m0 = _re.match(r'\s*<h2[^>]*>.*?</h2>\s*', corpo, _re.S)
        if _m0:
            corpo = corpo[_m0.end():]
        olho = ''
        if pg.get('texto'):
            if corpo:
                olho = f'<div class="olho">{md_lite(pg["texto"])}</div>'
            else:
                corpo = md_lite(pg['texto'])
        fatias = _rv_quebra_corpo(corpo)
        # a MEIA PÁGINA vendida: quando existe, o anúncio ocupa o pé da última
        # página da matéria (o lugar da arte da casa), sempre rotulado
        _am = pg.get('anuncioMeia') or {}
        if _am.get('img'):
            _aml = (_am.get('link') or '').strip()
            _ami = ((f'<a style="display:contents" href="{_rvesc(_aml)}" target="_blank" rel="noopener sponsored">' if _aml else '')
                    + f'<img src="{_rvesc(_am["img"])}" alt="{_rvesc(_am.get("legenda", ""))}">'
                    + ('</a>' if _aml else ''))
            fim_arte = ('<div class="rv-meia"><em>Publicidade</em>' + _ami
                        + (f'<span>{_rvesc(_am["legenda"])}</span>' if _am.get('legenda') else '')
                        + '</div>')
        else:
            fim_arte = f'<svg class="arte-fim" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{_RV_ARTES[(int(ed.get("numero", 1)) + 1) % len(_RV_ARTES)]}"/></svg>'
        titulo_curto = pg.get('titulo', '')
        if len(titulo_curto) > 54:
            titulo_curto = titulo_curto[:54].rsplit(' ', 1)[0].rstrip(',.;:') + '…'
        saida = [(f'<section class="rv-pg rv-mat">{img}<div class="miolo">'
                  f'<h3>{_rvesc(pg.get("titulo"))}</h3>'
                  f'<p class="linhafina">{_rvesc(pg.get("chamada", ""))}</p>'
                  + olho
                  + (f'<div class="txt">{fatias[0]}</div>' if fatias[0] else '')
                  + ((fim_arte + leia) if len(fatias) == 1 else '<span class="segue">continua na próxima página →</span>')
                  + f'</div>{fol}</section>')]
        for k, fatia in enumerate(fatias[1:], 2):
            ultima = (k == len(fatias))
            saida.append(
                f'<section class="rv-pg rv-mat cont"><div class="rv-kicker">'
                f'<span class="tagz">{_rvesc(pg.get("cat") or "FOYER")}</span>'
                f'<span>continuação</span></div><div class="miolo">'
                f'<p class="cont-tit">{_rvesc(titulo_curto)}</p>'
                f'<div class="txt">{fatia}</div>'
                + ((fim_arte + leia) if ultima else '<span class="segue">continua na próxima página →</span>')
                + f'</div>{fol}</section>')
        return saida
    if t == 'exclusiva':
        return (f'<section class="rv-pg rv-livre"><div class="rv-kicker">'
                f'<span class="tagz">Exclusivo da revista</span><span>Só aqui</span></div>'
                f'<div class="miolo"><h3>{_rvesc(pg.get("titulo"))}</h3>'
                f'<div class="txt">{md_lite(pg.get("texto", ""))}</div></div>{fol}</section>')
    if t == 'programas':
        # a página congela na data de fechamento da edição: nada publicado
        # depois dela entra, mesmo que o site seja reconstruído meses depois
        _ref = _rv_iso_edicao(ed) or datetime.now(timezone.utc).strftime('%Y-%m-%d')
        _lim = (datetime.strptime(_ref, '%Y-%m-%d') - __import__('datetime').timedelta(days=14)).strftime('%Y-%m-%d')
        # o episódio mais novo de CADA programa dentro da quinzena (garante o Programa do Foyer),
        # completando com os demais lançamentos recentes até 6
        _semana, _vistos = [], set()
        for _p in _yt_progs:
            _vs = sorted([v for v in _p.get('videos', []) if v.get('quando', '') <= _ref],
                         key=lambda v: v.get('quando', ''), reverse=True)
            if _vs and _vs[0].get('quando', '') >= _lim:
                _semana.append((_vs[0]['quando'], _p['nome'], _vs[0]))
                _vistos.add(_vs[0].get('id'))
        _semana.sort(key=lambda x: (x[0], x[1]), reverse=True)
        for q, n, v in _yt_videos(_yt_progs, 60):
            if len(_semana) >= 6:
                break
            if v.get('id') not in _vistos and _lim <= q <= _ref:
                _semana.append((q, n, v))
                _vistos.add(v.get('id'))
        _semana = (sorted(_semana, key=lambda x: (x[0], x[1]), reverse=True)[:6]
                   or [(q, n, v) for q, n, v in _yt_videos(_yt_progs, 60) if q <= _ref][:6])
        def _ep_tit(nome_prog, tit):
            # o rótulo já diz o programa: o título não precisa repeti-lo
            t = tit.strip()
            if t.lower().startswith(nome_prog.lower()):
                t = t[len(nome_prog):].lstrip(' -–—:·|').strip() or tit.strip()
            return t[:90]
        cels = ''.join(
            f'<a class="ep" href="{_rvesc(v["url"])}" target="_blank" rel="noopener">'
            f'<img src="{_rvesc(v["thumb"])}" alt="" loading="lazy" '
            f'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/{_rvesc(v.get("id",""))}/mqdefault.jpg\'">'
            f'<span class="mt"><span class="pr">{_rvesc(n.split(" — ")[0])}</span>'
            f'<span class="tt">{_rvesc(_ep_tit(n.split(" — ")[0], v["titulo"]))}</span></span></a>'
            for q, n, v in _semana)
        _gr = 'grade poucos' if len(_semana) <= 3 else 'grade'
        return (f'<section class="rv-pg rv-tela"><div class="cab"><em>O canal, esta semana</em>'
                f'<h3>Na tela</h3></div><div class="{_gr}">{cels}</div>'
                '<div class="canal-cta"><a href="https://www.youtube.com/@Foyer.digital" target="_blank" rel="noopener">'
                'Assista a tudo no canal do FOYER →</a></div>'
                f'{_rv_folio(ed, num)}</section>')
    if t == 'agenda':
        # conteúdo EXCLUSIVO da revista: itens apurados pela equipe (sexta a quinta).
        # Sem itens apurados, cai na lista automática de eventos das matérias.
        _DIAS_PT = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        if pg.get('itens'):
            linhas = ''
            for it in pg['itens'][:8]:
                try:
                    _dt_i = datetime.strptime(it.get('dia', ''), '%Y-%m-%d')
                    dia_rot = f'{_DIAS_PT[_dt_i.weekday()]} {_dt_i.day:02d}/{_dt_i.month:02d}'
                except Exception:
                    dia_rot = it.get('dia', '')
                onde = ' · '.join(x for x in [it.get('local'), it.get('cidade')] if x)
                link = it.get('link') or ''
                abre = (f'<a class="ag-item cur" href="{_rvesc(link)}"'
                        + (' target="_blank" rel="noopener"' if link.startswith('http') else '') + '>'
                        ) if link else '<div class="ag-item cur">'
                fecha = '</a>' if link else '</div>'
                linhas += (abre
                           + f'<span class="ag-dia">{_rvesc(dia_rot)}</span>'
                           f'<span class="ag-oq"><b>{_rvesc(it.get("titulo", ""))}</b>'
                           + (f'<i>{_rvesc(it.get("texto", ""))}</i>' if it.get('texto') else '')
                           + (f'<small>{_rvesc(onde)}</small>' if onde else '')
                           + '</span>' + fecha)
            cid = pg.get('cidade', '')
            tit_ag = f'A semana em cartaz<span class="cid">{_rvesc(cid)}</span>' if cid else 'A semana em cartaz'
            # o bilhete da semana: a escolha única da redação abre a agenda como um ingresso
            bi = pg.get('bilhete') or {}
            bilhete = ''
            if bi.get('titulo'):
                bilhete = ('<div class="rv-bsem"><div class="bs-esq">'
                           f'<em>O bilhete da semana</em><b>{_rvesc(bi["titulo"])}</b>'
                           + (f'<span>{_rvesc(bi["sessao"])}</span>' if bi.get('sessao') else '')
                           + (f'<i>“{_rvesc(bi["frase"])}” · {_rvesc(bi.get("assinatura") or "A redação")}</i>' if bi.get('frase') else '')
                           + '</div><div class="bs-dir"><em>a escolha</em><strong>da redação</strong></div></div>')
            return (f'<section class="rv-pg rv-agd"><div class="cab"><em>Sete dias pela frente</em>'
                    f'<h3>{tit_ag}</h3></div>'
                    + bilhete +
                    f'<div class="lista">{linhas}</div>'
                    f'<div class="ag-cta"><a href="cat-em-cartaz.html">Tudo que está em cartaz agora →</a></div>'
                    f'{fol}</section>')
        _ref_ag = _rv_iso_edicao(ed)
        itens = _rv_agenda_itens(datetime.strptime(_ref_ag, '%Y-%m-%d').date() if _ref_ag else None)
        linhas = ''
        for e_ini, e_fim, m in itens:
            hoje = _ref_ag or datetime.now(timezone.utc).date().isoformat()
            if e_ini <= hoje and e_fim > hoje:
                quando = f'em cartaz até {_rv_data_curta(e_fim)}'
            elif e_ini == e_fim:
                quando = f'dia {_rv_data_curta(e_ini)}'
            else:
                quando = f'de {_rv_data_curta(e_ini)} a {_rv_data_curta(e_fim)}'
            ev = m.get('evento') or {}
            onde = ' · '.join(x for x in [ev.get('local'), ev.get('cidade')] if x)
            tit = m['title']
            if len(tit) > 72:
                tit = tit[:72].rsplit(' ', 1)[0].rstrip(',.;:') + '…'
            linhas += (f'<a class="ag-item" href="post-{_rvesc(m["slug"])}.html">'
                       f'<span class="ag-dia">{_rvesc(_rv_data_curta(e_ini))}</span>'
                       f'<span class="ag-oq"><b>{_rvesc(tit)}</b>'
                       f'<small>{_rvesc(quando)}{(" · " + _rvesc(onde)) if onde else ""}</small></span></a>')
        if not linhas:
            linhas = '<p class="ag-vazio">A agenda da semana está em formação. Confira as estreias no site.</p>'
        return (f'<section class="rv-pg rv-agd"><div class="cab"><em>Sete dias pela frente</em>'
                f'<h3>A semana em cartaz</h3></div>'
                f'<div class="lista">{linhas}</div>'
                f'<div class="ag-cta"><a href="cat-em-cartaz.html">Tudo que está em cartaz agora →</a></div>'
                f'{_rv_folio(ed, num)}</section>')
    if t == 'frase-celebre':
        _fi = (int(ed.get('numero', 1)) - 1) % len(_RV_MESTRES)
        frase = pg.get('frase') or _RV_MESTRES[_fi][0]
        autor = pg.get('autor') or _RV_MESTRES[_fi][1]
        sobre = pg.get('sobre') or _RV_MESTRES[_fi][2]
        return (f'<section class="rv-pg rv-mestre">'
                f'<svg class="fundo" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><use href="#ph-1"/></svg>'
                f'<div class="rv-kicker">'
                f'<span class="tagz">Entre mestres</span><span>A arte pela palavra</span></div>'
                f'<div class="miolo"><div class="aspa">“</div>'
                f'<div class="fr">{_rvesc(frase)}</div>'
                f'<div class="au">{_rvesc(autor)}</div>'
                f'<div class="bio">{_rvesc(sobre)}</div>'
                f'</div>{_rv_folio(ed, num)}</section>')
    if t in ('cartaz', 'patrocinio'):
        rot = 'Publicidade' if t == 'patrocinio' else 'Divulgação'
        leg = _rvesc(pg.get('legenda', ''))
        link = (pg.get('link') or '').strip()
        # o bilhete do leitor é EXCLUSIVO da página paga (rotulada Publicidade);
        # o cartaz é cortesia da casa e sai limpo, sem cupom
        cupom = ''
        if t == 'patrocinio' and pg.get('cupom'):
            # o código viaja no clique: o anunciante vê de onde o leitor veio
            if link:
                link += ('&' if '?' in link else '?') + 'utm_source=foyer&cupom=' + _uq.quote(str(pg['cupom']))
            cupom = ('<div class="rv-bilhete"><div class="rb-esq">'
                     f'<b>{_rvesc(pg.get("beneficio") or "Vantagem do leitor do FOYER")}</b>'
                     + (f'<span>{_rvesc(pg["comoUsar"])}</span>' if pg.get('comoUsar') else
                        '<span>diga o código na bilheteria ou use na compra on-line</span>')
                     + (f'<i>vale até {_rvesc(pg["validade"])}</i>' if pg.get('validade') else '')
                     + '</div><button type="button" class="rb-dir" data-copia-cupom="'
                     f'{_rvesc(pg["cupom"])}" title="Tocar para copiar o código"><em>código</em>'
                     f'<strong>{_rvesc(pg["cupom"])}</strong></button></div>')
        elif pg.get('cupom'):
            print(f'  AVISO revista: cupom em página "cartaz" foi ignorado — o bilhete do leitor é exclusivo da página de Publicidade (patrocinio)')
        img = f'<img src="{_rvesc(pg.get("img", ""))}" alt="{leg}">'
        if link:
            img = f'<a style="display:contents" href="{_rvesc(link)}" target="_blank" rel="noopener sponsored">{img}</a>'
        klass = 'rv-pg rv-cartaz rv-pat' if t == 'patrocinio' else 'rv-pg rv-cartaz'
        return f'<section class="{klass}">{img}{cupom}<div class="rv-leg">{rot}{" — " + leg if leg else ""}</div>{fol}</section>'
    if t == 'citacao':
        arte = _RV_ARTES[num % len(_RV_ARTES)]
        return (f'<section class="rv-pg rv-cit"><div class="aspa">“</div>'
                f'<div class="fr">{_rvesc(pg.get("frase"))}</div>'
                f'<div class="au">{_rvesc(pg.get("autor", ""))}</div>'
                f'<svg class="arte" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{arte}"/></svg>'
                f'</section>')
    if t == 'expediente':
        try:
            _eq = _json.load(open(os.path.join(ROOT, 'import/equipe.json'))).get('usuarios', [])
        except Exception:
            _eq = []
        nomes = ''.join(f'<li><b>{_rvesc(u["nome"])}</b> · {"Direção e edição" if u.get("papel") == "chefe" else "Redação"}</li>' for u in _eq)
        return (f'<section class="rv-pg rv-exp"><div class="rv-kicker"><span class="tagz">Expediente</span>'
                f'<span>Nº {_rvesc(ed.get("numero"))}</span></div><div class="miolo">'
                f'<img src="assets/logo/foyer-stacked-wine-sm.png" alt="FOYER" class="only-light">'
                f'<img src="assets/logo/foyer-stacked-gold-sm.png" alt="FOYER" class="only-dark">'
                f'<h4>Quem faz</h4><ul>{nomes}</ul>'
                f'<h4>Fotografias</h4><p>Imagens de divulgação das produções, sempre com crédito.</p>'
                f'<h4>Cartas da plateia</h4><p>Escreva para programafoyer@gmail.com. As melhores cartas saem na revista, com nome e cidade.</p>'
                f'<h4>Fale conosco</h4><p>foyer.digital · programafoyer@gmail.com · YouTube @Foyer.digital</p>'
                '<div class="anuncie"><em>Anuncie no FOYER</em>'
                '<p>No site todos os dias ou na revista: página inteira, meia página e o bilhete do leitor com código exclusivo. '
                'Contrate em 5 passos: <a href="anuncie.html">foyer.digital/anuncie</a> · programafoyer@gmail.com</p></div>'
                f'</div>{fol}</section>')
    if t == 'programa-sala':
        # o programa clássico da estreia: moldura dourada, quem é quem, ficha em colunas
        elenco = ''.join(
            f'<li><b>{_rvesc(it.get("quem", ""))}</b>'
            + (f'<i>{_rvesc(it["papel"])}</i>' if it.get('papel') else '') + '</li>'
            for it in (pg.get('quemEQuem') or [])[:16] if it.get('quem'))
        ficha = ''.join(
            f'<li><em>{_rvesc(it.get("funcao", ""))}</em><span>{_rvesc(it.get("nome", ""))}</span></li>'
            for it in (pg.get('ficha') or [])[:14] if it.get('nome'))
        colunas = (
            (f'<div class="pr-col"><h4>Quem está em cena</h4><ul class="elenco">{elenco}</ul></div>' if elenco else '')
            + (f'<div class="pr-col"><h4>Ficha técnica</h4><ul class="fichat">{ficha}</ul></div>' if ficha else ''))
        return (f'<section class="rv-pg rv-prog"><div class="borda">'
                f'<em class="rot">Programa de sala · A estreia da semana</em>'
                f'<h3>{_rvesc(pg.get("titulo", ""))}</h3>'
                + (f'<p class="sub">{_rvesc(pg["subtitulo"])}</p>' if pg.get('subtitulo') else '')
                + (f'<p class="sinopse">{_rvesc(pg["sinopse"])}</p>' if pg.get('sinopse') else '')
                + (f'<div class="colunas">{colunas}</div>' if colunas else '')
                + (f'<p class="serv">{_rvesc(pg["servico"])}</p>' if pg.get('servico') else '')
                + f'</div>{fol}</section>')
    if t == 'cartas':
        # o correio da plateia: cartas reais chegadas ao e-mail da casa
        cs = ''
        for c in (pg.get('itens') or [])[:3]:
            if not (c.get('texto') and c.get('nome')):
                continue
            cs += ('<div class="carta"><p class="tx">' + _rvesc(c['texto']) + '</p>'
                   f'<p class="ass">{_rvesc(c["nome"])}'
                   + (f' · {_rvesc(c["cidade"])}' if c.get('cidade') else '') + '</p>'
                   + (f'<p class="resp"><em>{_rvesc(c["resposta"])}</em><span>A direção</span></p>' if c.get('resposta') else '')
                   + '</div>')
        return (f'<section class="rv-pg rv-cartas"><div class="cab"><em>O correio da revista</em>'
                f'<h3>Cartas da plateia</h3></div><div class="lista">{cs}</div>'
                '<p class="convite">Escreva para a revista: programafoyer@gmail.com · as melhores cartas saem aqui, com nome e cidade</p>'
                f'{fol}</section>')
    if t == 'tres-perguntas':
        # minientrevista exclusiva: as respostas nunca sobem ao site
        qs = ''
        for k, it in enumerate((pg.get('itens') or [])[:3], 1):
            if not (it.get('pergunta') and it.get('resposta')):
                continue
            qs += (f'<div class="par"><p class="pp"><b>{k}.</b> {_rvesc(it["pergunta"])}</p>'
                   f'<p class="rr">{_rvesc(it["resposta"])}</p></div>')
        return (f'<section class="rv-pg rv-3p"><div class="rv-kicker">'
                f'<span class="tagz">Exclusivo da revista</span><span>Só aqui</span></div>'
                f'<div class="miolo"><em class="rot">Três perguntas para</em>'
                f'<h3>{_rvesc(pg.get("entrevistado", ""))}</h3>'
                + (f'<p class="quem">{_rvesc(pg["contexto"])}</p>' if pg.get('contexto') else '')
                + qs
                + (f'<p class="nota">{_rvesc(pg["nota"])}</p>' if pg.get('nota') else '')
                + f'</div>{fol}</section>')
    if t == 'recortes':
        recs = ''
        for it in (pg.get('itens') or [])[:4]:
            quem = _rvesc(it.get('quem', ''))
            onde = _rvesc(it.get('onde', ''))
            fr = f'<div class="fr">{_rvesc(it.get("frase", ""))}</div>'
            meta = (f'<div class="qm">{quem}' + (f'<i>{onde}</i>' if onde else '') + '</div>')
            dentro = fr + meta
            if it.get('slug'):
                dentro = f'<a href="post-{_rvesc(it["slug"])}.html">{dentro}</a>'
            recs += f'<div class="rec">{dentro}</div>'
        return (f'<section class="rv-pg rv-rec"><div class="cab"><em>Entre aspas, com a origem</em>'
                f'<h3>Recortes da semana</h3></div>'
                f'<div class="mural">{recs}</div>{fol}</section>')
    if t == 'contracapa':
        # a contracapa é a despedida: a cortina desce e a citação é o centro da página
        frase, autor = pg.get('frase'), pg.get('autor', '')
        if not frase:
            _fr = _RV_MESTRES[(int(ed.get('numero', 1)) + 3) % len(_RV_MESTRES)]
            frase, autor = _fr[0], _fr[1]
        desped = (f'<div class="desp"><div class="fr">“{_rvesc(frase)}”</div>'
                  + (f'<div class="au">{_rvesc(autor)}</div>' if autor else '')
                  + '</div>')
        return (f'<section class="rv-pg rv-back"><div class="miolo">'
                f'<em class="rot">Fechamos esta edição. A cortina desce.</em>'
                + desped +
                f'<div class="rodape"><img src="assets/logo/foyer-horizontal-gold.png" alt="FOYER">'
                f'<span>foyer.digital · assinante lê na quinta</span><span class="rv-barcode"></span></div>'
                f'</div></section>')
    return (f'<section class="rv-pg rv-livre"><div class="rv-kicker">'
            f'<span class="tagz">{_rvesc(pg.get("rotulo") or "FOYER")}</span><span></span></div>'
            f'<div class="miolo"><h3>{_rvesc(pg.get("titulo", ""))}</h3>'
            f'<div class="txt">{md_lite(pg.get("texto", ""))}</div></div>{fol}</section>')

def edicao_page(ed):
    capa = ed.get('capa', {})
    paginas = list(ed.get('paginas', []))
    # CAPA (página 1)
    _chs = [c for c in (capa.get('chamadas') or []) if c.strip()]
    if len(_chs) > 3:
        print(f'  AVISO revista Nº {ed.get("numero")}: a capa imprime só 3 chamadas — '
              f'{len(_chs) - 3} descartada(s): ' + '; '.join(f'"{c}"' for c in _chs[3:]))
    calls = ''.join(f'<span class="ch"><i>✦</i>{_rvesc(c)}</span>' for c in _chs[:3])
    pg_capa = (
        '<section class="rv-pg rv-capa2 on">'
        '<div class="nameplate"><img src="assets/logo/foyer-horizontal-wine.png" alt="FOYER"></div>'
        f'<div class="linha-ed"><span>A revista da semana</span><span>Nº {_rvesc(ed.get("numero"))} · {_rvesc(ed.get("dataEdicao", ""))}</span></div>'
        '<div class="moldura">'
        + (f'<img src="{_rvesc(capa.get("img", ""))}" alt="">' if capa.get('img') else '')
        + (f'<span class="cred">Foto: {_rvesc(capa["credito"])}</span>' if capa.get('credito') else '')
        + '</div>'
        f'<div class="manchete"><h2>{_rvesc(capa.get("manchete") or ed.get("titulo", ""))}</h2></div>'
        + (f'<div class="faixa">{calls}</div>' if calls else '')
        + '<div class="rodape-capa"><span>foyer.digital · edição gratuita</span><span class="rv-barcode"></span></div>'
        '</section>')
    # toda edição fecha com contracapa; se a Coxia não montou uma, entra a da casa
    if not any(p.get('tipo') == 'contracapa' for p in paginas):
        paginas.append({'tipo': 'contracapa'})
    # miolos primeiro: uma página lógica pode virar várias páginas físicas
    # (matéria longa continua na página seguinte, como revista impressa)
    blocos_por_pg, numeros_sum, prox = [], [], 3
    for pg in paginas:
        out = _rv_pagina(dict(pg), ed, '__NUMPG__')
        blocos = out if isinstance(out, list) else [out]
        numeros_sum.append(prox)
        blocos_por_pg.append(blocos)
        prox += len(blocos)
    # SUMÁRIO (página 2) com os números reais
    linhas_sum = ''
    for i, pg in enumerate(paginas):
        titulo, secao = _rv_rotulo_sumario(pg)
        if len(titulo) > 76:
            titulo = titulo[:76].rsplit(' ', 1)[0].rstrip(',.;:') + '…'
        linhas_sum += (f'<li><span class="pnum">{numeros_sum[i]}</span><span><span class="pt">{_rvesc(titulo)}</span>'
                       f'<span class="ps">{_rvesc(secao)}</span></span></li>')
    arte_sum = _RV_ARTES[int(ed.get('numero', 1)) % len(_RV_ARTES)]
    pg_sum = (
        f'<section class="rv-pg rv-sum{" cheia" if len(paginas) > 10 else ""}">'
        '<div class="cab"><span>O que vem por aí</span><h3>Nesta edição</h3>'
        f'<svg class="arte" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice"><use href="#{arte_sum}"/></svg></div>'
        f'<ol>{linhas_sum}</ol>' + _rv_folio(ed, 2) + '</section>')
    pgs = [pg_capa, pg_sum]
    n = 3
    for bi, blocos in enumerate(blocos_por_pg):
        for k, b in enumerate(blocos):
            if k == 0:      # marca o começo da página lógica: o sumário se corrige no navegador
                b = b.replace('<section class="rv-pg', f'<section data-sum="{bi}" class="rv-pg', 1)
            pgs.append(b.replace('__NUMPG__', str(n)))
            n += 1
    corpo = '\n'.join(pgs)
    total = len(pgs)
    # a janela do assinante: a edição sai quinta para a lista e abre para
    # todos um dia depois. Antes disso, capa, sumário e carta ficam de
    # amostra e a cortina pede o e-mail.
    _iso_ed = _rv_iso_edicao(ed)
    _libera = ''
    if _iso_ed:
        _libera = (datetime.strptime(_iso_ed, '%Y-%m-%d')
                   + __import__('datetime').timedelta(days=1)).strftime('%Y-%m-%d')
    return (_RV_CSS + f'''
<main id="conteudo" class="rv-stage" data-libera="{_libera}">
  <div class="rv-palco" id="rv-palco">
  <div class="rv-book" id="rv-book">
    <div class="rv-lombo esq" id="rv-lombo-esq" aria-hidden="true"></div>
{corpo}
    <div class="rv-lombo dir" id="rv-lombo-dir" aria-hidden="true"></div>
    <button type="button" class="rv-quina esq" id="rv-ant" aria-label="Página anterior">◀</button>
    <button type="button" class="rv-quina dir" id="rv-prox" aria-label="Próxima página">▶</button>
  </div>
  </div>
  <div class="rv-cortina" id="rv-cortina" role="dialog" aria-modal="true" aria-label="Edição para assinantes" hidden>
    <div class="ct-caixa">
      <span class="ct-rot">🎪 Cortina fechada até sexta</span>
      <h3>Esta edição é dos assinantes até amanhã.</h3>
      <p>Capa, sumário e carta são de casa aberta. O resto abre para todo mundo na sexta.
         Assinante lê tudo <b>hoje</b>, de graça.</p>
      <div class="ct-ja">
        <label for="ct-email">Já estou na lista:</label>
        <div class="ct-linha"><input type="email" id="ct-email" placeholder="seu@email.com">
        <button type="button" id="ct-entrar">Entrar</button></div>
        <span class="ct-erro" id="ct-erro" aria-live="polite"></span>
      </div>
      <div class="ct-ou"><span>ou</span></div>
      <button type="button" class="ct-assinar" data-conversa>🎟 Assinar em um minuto e ler agora</button>
      <button type="button" class="ct-voltar" id="ct-voltar">← voltar para a amostra</button>
    </div>
  </div>
  <div class="rv-nav">
    <span class="ct" id="rv-ct">1 / {total}</span>
    <button type="button" id="rv-sala" title="Só a revista, com a luz apagada">◐ Sala de leitura</button>
    <button type="button" onclick="window.print()" title="Imprimir ou salvar em PDF">⤓ PDF</button>
  </div>
  <button type="button" id="rv-sala-sair">✕ Acender a luz</button>
</main>
<script>
(function(){{
  var pgs = document.querySelectorAll('.rv-pg'), i = 0;
  // diagramação fina: equilibra as páginas de matéria no tamanho real da tela
  function diagrama(){{
    function equilibrar(){{
      var mats = document.querySelectorAll('.rv-pg.rv-mat');
      for(var k = 0; k < mats.length - 1; k++){{
        var a = mats[k], b = mats[k + 1];
        if(!b.classList.contains('cont')) continue;
        var ta = a.querySelector('.txt'), tb = b.querySelector('.txt');
        if(!ta || !tb) continue;
        var ma = a.querySelector('.miolo');
        var eraA = a.classList.contains('on'), eraB = b.classList.contains('on');
        a.classList.add('on'); b.classList.add('on');
        var guarda = 0;
        while(tb.firstElementChild && guarda++ < 40){{
          var bloco = tb.firstElementChild;
          if(bloco.hasAttribute('data-junto')){{
            // a ficha de Serviço só muda de página inteira
            var ficha = [];
            while(tb.firstElementChild && tb.firstElementChild.hasAttribute('data-junto')){{
              ficha.push(tb.firstElementChild); ta.appendChild(tb.firstElementChild);
            }}
            if(ma.scrollHeight > ma.clientHeight + 2){{
              for(var fj = ficha.length - 1; fj >= 0; fj--) tb.insertBefore(ficha[fj], tb.firstChild);
            }}
            break;
          }}
          ta.appendChild(bloco);
          if(ma.scrollHeight > ma.clientHeight + 2){{ tb.insertBefore(bloco, tb.firstChild); break; }}
        }}
        guarda = 0;
        while(ma.scrollHeight > ma.clientHeight + 2 && ta.lastElementChild && guarda++ < 40){{
          var volta = ta.lastElementChild;
          tb.insertBefore(volta, tb.firstChild);
          // se o bloco devolvido pertence à ficha, ela volta inteira
          if(volta.hasAttribute('data-junto')){{
            while(ta.lastElementChild && ta.lastElementChild.hasAttribute('data-junto')){{
              tb.insertBefore(ta.lastElementChild, tb.firstChild);
            }}
          }}
        }}
        // intertítulo nunca fecha a página: desce com o texto que anuncia
        if(ta.lastElementChild && /^H[23]$/.test(ta.lastElementChild.tagName)){{
          tb.insertBefore(ta.lastElementChild, tb.firstChild);
        }}
        if(!eraA) a.classList.remove('on');
        if(!eraB) b.classList.remove('on');
      }}
    }}
    equilibrar();
    // remove continuações esvaziadas, herdando botão e ornamento para a página anterior
    document.querySelectorAll('.rv-pg.rv-mat').forEach(function(pg){{
      var t = pg.querySelector('.txt');
      if(pg.classList.contains('cont') && t && !t.firstElementChild){{
        var ant = pg.previousElementSibling;
        if(ant && ant.classList.contains('rv-mat')){{
          var ma2 = ant.querySelector('.miolo');
          var sg = ant.querySelector('.segue');
          if(sg) sg.remove();
          var lv = pg.querySelector('.leia');
          var af = pg.querySelector('.arte-fim');
          if(ma2 && af && !ant.querySelector('.arte-fim')) ma2.appendChild(af);
          if(ma2 && lv) ma2.appendChild(lv);
        }}
        pg.remove();
      }}
    }});
    equilibrar();
    // liga o ornamento de fim de matéria quando sobra espaço na última página
    // (o vão real é a distância entre o fim do texto e o botão, que gruda no pé)
    document.querySelectorAll('.rv-pg.rv-mat').forEach(function(pg){{
      var lv = pg.querySelector('.leia'), tx = pg.querySelector('.txt');
      if(!lv || !tx) return;
      var era2 = pg.classList.contains('on');
      pg.classList.add('on');
      var vao = lv.offsetTop - (tx.offsetTop + tx.offsetHeight);
      if(vao > 150) pg.classList.add('compl');
      if(!era2) pg.classList.remove('on');
    }});
    // última instância: entrelinha mais justa na página que ainda estoura
    document.querySelectorAll('.rv-pg.rv-mat').forEach(function(pg){{
      var era3 = pg.classList.contains('on');
      pg.classList.add('on');
      var m3 = pg.querySelector('.miolo');
      if(m3 && m3.scrollHeight > m3.clientHeight + 2){{
        pg.classList.add('aperta');
        if(m3.scrollHeight > m3.clientHeight + 2) pg.classList.add('aperta2');
      }}
      if(!era3) pg.classList.remove('on');
    }});
    pgs = document.querySelectorAll('.rv-pg');
    pgs.forEach(function(pg2, k2){{ var bb = pg2.querySelector('.rv-folio b'); if(bb) bb.textContent = k2 + 1; }});
    document.getElementById('rv-ct').textContent = (i + 1) + ' / ' + pgs.length;
  }}
  try{{ diagrama(); }}catch(e){{}}

  /* ============ o livro: dupla, virada, pilha, fita, sala ============ */
  var NUM_ED = {_json.dumps(str(ed.get('numero', '')))};
  var mqDuplo = window.matchMedia('(min-width:860px)');
  var mexeMenos = window.matchMedia('(prefers-reduced-motion: reduce)');
  var duplas = [];      // cada item: [idx] ou [idxEsq, idxDir]
  var d = 0;            // dupla atual
  var virando = false;
  var modoLargura = false;   // toque duplo: ler na largura da tela
  var fita = document.createElement('div'); fita.className = 'rv-fita';

  function ehSolo(p){{ return p.classList.contains('rv-capa2') || p.classList.contains('rv-back'); }}
  // o encaixador: em revista, todo conteúdo cabe na página. Mede cada miolo
  // e aperta o corpo (zoom tipográfico) até a página fechar sem sobra.
  function encaixa(){{
    document.querySelectorAll('.rv-pg').forEach(function(pg2){{
      var alvo = pg2.querySelector(':scope > .miolo, :scope > ol, :scope > .lista, :scope > .grade, :scope > .mural');
      if(!alvo) return;
      var era = pg2.classList.contains('on');
      pg2.classList.add('on');
      alvo.style.zoom = '';
      var z = 1, guarda = 0;
      while(alvo.scrollHeight > alvo.clientHeight + 2 && z > 0.66 && guarda++ < 14){{
        z -= 0.03;
        alvo.style.zoom = z;
      }}
      if(!era) pg2.classList.remove('on');
    }});
  }}

  // o sumário aponta a página certa mesmo depois da repaginação fina no navegador
  function renumeraSumario(){{
    var todas = document.querySelectorAll('.rv-pg');
    document.querySelectorAll('.rv-sum ol li').forEach(function(li, k){{
      var alvo = document.querySelector('[data-sum="' + k + '"]');
      if(!alvo) return;
      var pos = Array.prototype.indexOf.call(todas, alvo);
      var el = li.querySelector('.pnum');
      if(el && pos >= 0) el.textContent = pos + 1;
    }});
  }}
  function montaDuplas(){{
    pgs = document.querySelectorAll('.rv-pg');
    duplas = [];
    if(!mqDuplo.matches || !document.body.classList.contains('rv-duplo-ok')){{
      pgs.forEach(function(_, k){{ duplas.push([k]); }});
      return;
    }}
    var k = 0;
    while(k < pgs.length){{
      if(ehSolo(pgs[k])){{ duplas.push([k]); k += 1; continue; }}
      if(k + 1 < pgs.length && !ehSolo(pgs[k + 1])){{ duplas.push([k, k + 1]); k += 2; }}
      else {{ duplas.push([k]); k += 1; }}
    }}
  }}
  function duplaDe(idxPg){{
    for(var s = 0; s < duplas.length; s++) if(duplas[s].indexOf(idxPg) >= 0) return s;
    return 0;
  }}
  function escala(){{
    var livro = document.getElementById('rv-book');
    var palco = document.getElementById('rv-palco');
    var par = duplas[d] || [0];
    var larguraLivro = 726 * par.length;           // 720 + bordas
    var alturaLivro = 978;
    var sala = document.body.classList.contains('rv-sala');
    var w = palco.clientWidth || document.documentElement.clientWidth - 28;
    var h = window.innerHeight - (sala ? 96 : 200);
    var f = Math.min(1, w / larguraLivro, Math.max(0.3, h / alturaLivro));
    // zoom de leitura (toque duplo): amplia o corpo e deixa arrastar a página
    if(modoLargura) f = Math.min(1, (w / larguraLivro) * 1.75);
    // origem no canto: o deslocamento centraliza a revista já na escala final,
    // sem sobrar metade fora da tela no celular
    var desloca = Math.max(0, (w - larguraLivro * f) / 2);
    livro.style.transform = 'translateX(' + desloca + 'px) scale(' + f + ')';
    palco.style.height = Math.ceil(alturaLivro * f) + 'px';
    palco.style.overflowX = modoLargura ? 'auto' : '';
  }}
  function pinta(){{
    var par = duplas[d] || [0];
    pgs.forEach(function(p, k){{
      p.classList.remove('on', 'pg-l', 'pg-r');
      var pos = par.indexOf(k);
      if(pos >= 0){{
        p.classList.add('on');
        if(par.length === 2) p.classList.add(pos === 0 ? 'pg-l' : 'pg-r');
      }}
    }});
    // contador: páginas humanas
    var ini = par[0] + 1, fim = par[par.length - 1] + 1;
    document.getElementById('rv-ct').textContent =
      (ini === fim ? ini : ini + '–' + fim) + ' / ' + pgs.length;
    // a espessura da revista dos dois lados
    var lidas = par[0], faltam = pgs.length - (par[par.length - 1] + 1);
    var le = document.getElementById('rv-lombo-esq'), ld = document.getElementById('rv-lombo-dir');
    var prim = pgs[par[0]], ult = pgs[par[par.length - 1]];
    var wEsq = Math.min(2 + lidas * 1.4, 16), wDir = Math.min(2 + faltam * 1.4, 16);
    le.style.width = wEsq + 'px';
    ld.style.width = wDir + 'px';
    le.style.left = (prim.offsetLeft - wEsq) + 'px';
    ld.style.left = (ult.offsetLeft + ult.offsetWidth) + 'px';
    le.style.display = lidas > 0 ? 'block' : 'none';
    ld.style.display = faltam > 0 ? 'block' : 'none';
    // a fita marca a página em que o leitor está
    if(d > 0 && !ult.classList.contains('rv-back')){{ ult.appendChild(fita); }}
    else if(fita.parentNode){{ fita.parentNode.removeChild(fita); }}
    try{{ localStorage.setItem('rv-fita-' + NUM_ED, String(par[0])); }}catch(e){{}}
    var qe = document.getElementById('rv-ant'), qd = document.getElementById('rv-prox');
    if(qe) qe.hidden = (d === 0);
    if(qd) qd.hidden = (d === duplas.length - 1);
    escala();
  }}
  /* ---- a janela do assinante: hoje é dia de assinante ler primeiro? ---- */
  var SB = {{ url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
             key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' }};
  function temCadeira(){{ try{{ return localStorage.getItem('foyer-cadeira') === '1'; }}catch(e){{ return false; }} }}
  function daCadeira(){{ try{{ localStorage.setItem('foyer-cadeira', '1'); }}catch(e){{}}
    document.body.classList.remove('rv-em-janela'); }}
  try{{ if(new URLSearchParams(location.search).get('cadeira') === '1') daCadeira(); }}catch(e){{}}
  function hojeISO(){{
    var d2 = new Date();
    var p2 = function(n){{ return (n < 10 ? '0' : '') + n; }};
    return d2.getFullYear() + '-' + p2(d2.getMonth() + 1) + '-' + p2(d2.getDate());
  }}
  function emJanela(){{
    var lib = document.querySelector('.rv-stage').dataset.libera || '';
    return !!lib && hojeISO() < lib && !temCadeira();
  }}
  function limiteAmostra(){{
    // a amostra vai até a carta ao leitor (capa e sumário inclusos)
    var todas = document.querySelectorAll('.rv-pg');
    var lim = Math.min(2, todas.length - 1);
    todas.forEach(function(p2, k2){{ if(p2.classList.contains('rv-edi')) lim = Math.max(lim, k2); }});
    return lim;
  }}
  function cortina(){{ return document.getElementById('rv-cortina'); }}
  function abreCortina(){{
    var c2 = cortina();
    if(!c2) return;
    c2.hidden = false;
    var em = document.getElementById('ct-email');
    if(em) setTimeout(function(){{ em.focus(); }}, 80);
  }}
  function fechaCortina(){{ var c2 = cortina(); if(c2) c2.hidden = true; }}
  (function ligaCortina(){{
    var c2 = cortina();
    if(!c2) return;
    if(emJanela()){{
      document.body.classList.add('rv-em-janela');
      var lim0 = limiteAmostra();
      document.querySelectorAll('.rv-pg').forEach(function(p3, k3){{
        if(k3 <= lim0) p3.classList.add('rv-amostra');
      }});
      window.addEventListener('foyer-assinou', function(){{ document.body.classList.remove('rv-em-janela'); }});
    }}
    document.getElementById('ct-voltar').addEventListener('click', fechaCortina);
    var entrar = document.getElementById('ct-entrar'), em = document.getElementById('ct-email');
    var erro = document.getElementById('ct-erro');
    function verifica(){{
      var v = (em.value || '').trim();
      if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v)){{ erro.textContent = 'Confere esse e-mail?'; return; }}
      entrar.disabled = true; entrar.textContent = '…';
      fetch(SB.url + '/rest/v1/rpc/foyer_ja_assina', {{
        method: 'POST',
        headers: {{ 'apikey': SB.key, 'Authorization': 'Bearer ' + SB.key, 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ p_email: v }})
      }}).then(function(r){{ return r.json(); }}).then(function(sim){{
        entrar.disabled = false; entrar.textContent = 'Entrar';
        if(sim === true){{ daCadeira(); fechaCortina(); proxima(); }}
        else {{ erro.textContent = 'Não achei esse e-mail na lista. Assina em um minuto aqui embaixo?'; }}
      }}).catch(function(){{
        entrar.disabled = false; entrar.textContent = 'Entrar';
        erro.textContent = 'Não deu para conferir agora. Tenta de novo?';
      }});
    }}
    entrar.addEventListener('click', verifica);
    em.addEventListener('keydown', function(e){{ if(e.key === 'Enter') verifica(); }});
    // assinou pela conversa: a cadeira é dada na hora e a cortina sobe
    window.addEventListener('foyer-assinou', function(){{ daCadeira(); fechaCortina(); }});
  }})();

  function vaiDupla(s, sentido){{
    if(virando) return;
    s = Math.max(0, Math.min(duplas.length - 1, s));
    if(emJanela()){{
      var lim = limiteAmostra();
      var par2 = duplas[s] || [0];
      if(par2[0] > lim){{ abreCortina(); return; }}
    }}
    if(s === d){{ pinta(); return; }}
    var anima = sentido && !mexeMenos.matches;
    if(!anima){{ d = s; pinta(); window.scrollTo({{ top: 0, behavior: 'smooth' }}); return; }}
    virando = true;
    // rede de segurança: nada pode deixar o leitor travado
    setTimeout(function(){{ virando = false; }}, 620);
    var parVelha = duplas[d];
    var sai = pgs[parVelha[sentido > 0 ? parVelha.length - 1 : 0]];
    sai.classList.add(sentido > 0 ? 'vira-sai-dir' : 'vira-sai-esq');
    setTimeout(function(){{
      sai.classList.remove('vira-sai-dir', 'vira-sai-esq');
      try{{
        // as duplas podem ter sido remontadas no meio da virada (resize)
        d = Math.max(0, Math.min(duplas.length - 1, s));
        pinta();
        var parNova = duplas[d] || [0];
        var entra = pgs[parNova[sentido > 0 ? 0 : parNova.length - 1]];
        if(entra){{
          entra.classList.add(sentido > 0 ? 'vira-entra-esq' : 'vira-entra-dir');
          setTimeout(function(){{
            entra.classList.remove('vira-entra-esq', 'vira-entra-dir');
          }}, 270);
        }}
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}catch(e){{}}
      setTimeout(function(){{ virando = false; }}, 270);
    }}, 230);
  }}
  function proxima(){{ vaiDupla(d + 1, 1); }}
  function anterior(){{ vaiDupla(d - 1, -1); }}

  // o convite no canto da página
  pgs.forEach(function(p){{
    if(p.classList.contains('rv-back')) return;
    var c = document.createElement('button');
    c.className = 'rv-canto'; c.type = 'button';
    c.setAttribute('aria-label', 'Virar a página');
    c.addEventListener('click', proxima);
    p.appendChild(c);
  }});

  document.getElementById('rv-ant').addEventListener('click', anterior);
  document.getElementById('rv-prox').addEventListener('click', proxima);
  // o código do cupom copia com um toque
  document.querySelectorAll('[data-copia-cupom]').forEach(function(bt){{
    bt.addEventListener('click', function(){{
      var cod = bt.getAttribute('data-copia-cupom');
      var em = bt.querySelector('em'), antes = em ? em.textContent : '';
      function avisa(){{ if(em){{ em.textContent = 'copiado!'; setTimeout(function(){{ em.textContent = antes; }}, 1600); }} }}
      if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(cod).then(avisa, avisa);
      else avisa();
    }});
  }});
  document.addEventListener('keydown', function(e){{
    if(e.target.closest && e.target.closest('input, [contenteditable]')) return;
    if(e.key === 'ArrowRight') proxima();
    if(e.key === 'ArrowLeft') anterior();
    if(e.key === 'Escape' && document.body.classList.contains('rv-sala')) salaSai();
  }});
  // toque duplo na página: alterna o modo "largura da tela" (corpo maior, rolagem vertical)
  var tqTrava = 0;
  function alternaLargura(){{
    // no toque, o navegador ainda sintetiza um dblclick: um gesto, uma alternância
    var agoraT = Date.now();
    if(agoraT - tqTrava < 500) return;
    tqTrava = agoraT;
    var palco = document.getElementById('rv-palco');
    var par = duplas[d] || [0];
    var w = palco.clientWidth || document.documentElement.clientWidth - 28;
    var cheia = Math.min(1, w / (726 * par.length));
    var h = window.innerHeight - (document.body.classList.contains('rv-sala') ? 96 : 200);
    var justa = Math.min(cheia, Math.max(0.3, h / 978));
    var ampliada = Math.min(1, cheia * 1.75);
    if(!modoLargura && ampliada - justa < 0.05) return;   // não faria diferença nesta tela
    modoLargura = !modoLargura;
    escala();
    var t = document.createElement('div');
    t.className = 'rv-toast';
    t.textContent = modoLargura ? 'Zoom de leitura: arraste a página · toque duas vezes para voltar'
                                : 'Página inteira de volta';
    document.body.appendChild(t);
    setTimeout(function(){{ t.remove(); }}, 2600);
  }}
  var x0 = null, y0 = null, tqUlt = 0;
  document.addEventListener('touchstart', function(e){{
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }}, {{passive:true}});
  document.addEventListener('touchend', function(e){{
    if(x0 == null) return;
    var dx = e.changedTouches[0].clientX - x0;
    var dy = e.changedTouches[0].clientY - y0;
    if(Math.abs(dx) > 60){{ if(!modoLargura) (dx < 0 ? proxima : anterior)(); tqUlt = 0; }}
    else if(Math.abs(dx) < 24 && Math.abs(dy) < 24 && e.target.closest && e.target.closest('.rv-pg')){{
      var agora = Date.now();
      if(agora - tqUlt < 340){{ alternaLargura(); tqUlt = 0; }}
      else tqUlt = agora;
    }}
    x0 = null; y0 = null;
  }}, {{passive:true}});
  document.addEventListener('dblclick', function(e){{
    if(e.target.closest && e.target.closest('.rv-pg') && !e.target.closest('a, button')) alternaLargura();
  }});

  // sala de leitura
  function salaEntra(){{ document.body.classList.add('rv-sala'); window.scrollTo({{ top: 0 }}); pinta(); }}
  function salaSai(){{ document.body.classList.remove('rv-sala'); pinta(); }}
  document.getElementById('rv-sala').addEventListener('click', function(){{
    document.body.classList.contains('rv-sala') ? salaSai() : salaEntra();
  }});
  document.getElementById('rv-sala-sair').addEventListener('click', salaSai);

  // arranque: mede, monta as duplas e volta para onde a fita ficou
  function arranca(){{
    document.body.classList.add('rv-duplo-ok');
    document.body.classList.toggle('rv-duplo', mqDuplo.matches);
    montaDuplas();
    encaixa();
    renumeraSumario();
    var guardada = 0;
    try{{ guardada = parseInt(localStorage.getItem('rv-fita-' + NUM_ED) || '0', 10) || 0; }}catch(e){{}}
    if(emJanela() && guardada > limiteAmostra()) guardada = 0;   // a fita respeita a cortina
    if(guardada > 0 && guardada < pgs.length){{
      d = duplaDe(guardada);
      var t = document.createElement('div');
      t.className = 'rv-toast';
      t.textContent = 'A fita marcou onde você parou: página ' + (guardada + 1);
      document.body.appendChild(t);
      setTimeout(function(){{ t.remove(); }}, 4400);
    }}
    pinta();
  }}
  function reflui(){{
    // cancela virada pendente: as duplas vão mudar debaixo dela
    virando = false;
    pgs.forEach(function(p){{ p.classList.remove('vira-sai-dir', 'vira-sai-esq', 'vira-entra-dir', 'vira-entra-esq'); }});
    document.body.classList.toggle('rv-duplo', mqDuplo.matches);
    var ancora = (duplas[d] || [0])[0];
    montaDuplas();
    encaixa();
    renumeraSumario();
    d = duplaDe(ancora);
    pinta();
  }}
  if(mqDuplo.addEventListener) mqDuplo.addEventListener('change', reflui);
  window.addEventListener('resize', function(){{ requestAnimationFrame(pinta); }});
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){{ try{{ diagrama(); reflui(); }}catch(e){{}} }});
  window.addEventListener('load', function(){{ try{{ diagrama(); reflui(); }}catch(e){{}} }});
  arranca();
}})();
</script>''')

_ESTANTE_CSS = '''<style>
/* a estante: as edições em pé, como numa prateleira de casa */
.estante{ position:relative; padding:26px 18px 0; }
.est-prateleira{ display:flex; align-items:flex-end; gap:26px; flex-wrap:wrap;
  padding:0 12px 0; min-height:340px; }
.est-rev{ position:relative; display:block; text-decoration:none; color:var(--ink);
  width:214px; transition:transform .22s ease; transform-origin:bottom center; }
.est-rev:hover{ transform:translateY(-14px) rotate(-1deg); }
.est-rev:focus-visible{ outline:3px solid var(--gold); outline-offset:4px; }
.est-capa{ position:relative; display:block; border:3px solid var(--ink); background:var(--wine);
  aspect-ratio:3/4.05; overflow:hidden;
  box-shadow:6px 0 0 -2px #d8cdb4, 9px 0 0 -3px var(--ink), 8px 10px 24px rgba(35,8,5,.3); }
.est-capa img{ width:100%; height:100%; object-fit:cover; display:block; }
.est-capa .veu{ position:absolute; inset:0;
  background:linear-gradient(180deg, rgba(35,8,5,.55), transparent 34%, transparent 62%, rgba(35,8,5,.8)); }
.est-capa .lg{ position:absolute; top:8px; left:10px; right:10px; }
.est-capa .lg img{ width:100%; height:auto; object-fit:contain; filter:drop-shadow(0 1px 6px rgba(0,0,0,.6)); }
.est-selo{ position:absolute; top:10px; right:-8px; z-index:3; background:var(--gold); color:#16100D;
  font-family:var(--mono); font-size:.52rem; font-weight:700; letter-spacing:.12em;
  text-transform:uppercase; padding:6px 10px; box-shadow:2px 3px 0 rgba(0,0,0,.35);
  transform:rotate(3deg); }
.est-capa .mch{ position:absolute; left:12px; right:12px; bottom:10px; color:#fff;
  font-family:var(--didone); font-size:1.05rem; line-height:1.06;
  text-shadow:0 2px 10px rgba(0,0,0,.7); }
.est-rot{ display:block; margin-top:10px; font-family:var(--mono); font-size:.56rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-soft); text-align:center; }
.est-rot b{ color:var(--ink); }
/* a próxima edição: ainda na gráfica */
.est-fantasma{ width:214px; }
.est-fantasma .est-capa{ background:var(--paper-2); border-style:dashed; box-shadow:none;
  display:flex; align-items:center; justify-content:center; text-align:center; }
.est-fantasma .est-capa span{ font-family:var(--mono); font-size:.6rem; letter-spacing:.18em;
  text-transform:uppercase; color:var(--ink-soft); padding:0 18px; line-height:2; }
/* a madeira da prateleira */
.est-tabua{ height:16px; border:3px solid var(--ink); background:var(--wine);
  box-shadow:0 8px 0 -4px rgba(35,8,5,.35); margin-top:-3px; }
@media (max-width:640px){ .est-prateleira{ justify-content:center; } }
</style>'''

def revista_listagem():
    prox = (max(int(e.get('numero', 0)) for e in EDICOES) + 1) if EDICOES else 1
    revs = ''
    for e in ED_PUB:
        capa = e.get('capa', {})
        img = (f'<img src="{_rvesc(capa.get("img", ""))}" alt="" loading="lazy" '
               'onerror="this.style.display=\'none\'">') if capa.get('img') else ''
        _iso_e = _rv_iso_edicao(e)
        _lib_e = ((datetime.strptime(_iso_e, '%Y-%m-%d')
                   + __import__('datetime').timedelta(days=1)).strftime('%Y-%m-%d')
                  if _iso_e else '')
        revs += f'''
      <a class="est-rev" data-libera="{_lib_e}" href="revista-ed-{e.get("numero")}.html" aria-label="Ler a edição {e.get("numero")}">
        <span class="est-capa">{img}<span class="veu"></span>
          <span class="lg"><img src="assets/logo/foyer-horizontal-gold.png" alt="FOYER"></span>
          <span class="mch">{_rvesc(capa.get("manchete") or e.get("titulo", ""))}</span>
        </span>
        <span class="est-rot"><b>Nº {e.get("numero")}</b> · {_rvesc(e.get("dataEdicao", ""))}</span>
      </a>'''
    fantasma = f'''
      <span class="est-rev est-fantasma" aria-hidden="true">
        <span class="est-capa"><span>Nº {prox}<br>em fechamento<br>na redação</span></span>
        <span class="est-rot">assinantes leem quinta</span>
      </span>'''
    selo_js = ('<script>(function(){var d=new Date(),p=function(n){return (n<10?"0":"")+n};'
               'var hoje=d.getFullYear()+"-"+p(d.getMonth()+1)+"-"+p(d.getDate());'
               'document.querySelectorAll(".est-rev[data-libera]").forEach(function(a){'
               'if(a.dataset.libera&&hoje<a.dataset.libera){'
               'var s=document.createElement("span");s.className="est-selo";'
               's.textContent="🎟 assinantes leem hoje";a.querySelector(".est-capa").appendChild(s);}});})();</script>')
    return (_ESTANTE_CSS +
            f'<div class="estante"><div class="est-prateleira">{revs}{fantasma}</div>'
            '<div class="est-tabua"></div></div>' + selo_js)

revista_body = band('Newsletter semanal', 'A Revista do Foyer',
                    'Toda sexta, uma edição fechada — como uma revista impressa, para ler na tela ou baixar') + f'''
<main id="conteudo" class="wrap">
  <div class="rev-hero" id="assinar">
    <div class="rev-copy">
      <h2>Uma revista de verdade, toda quinta para assinantes</h2>
      <p>A semana do teatro brasileiro editada com começo, meio e fim: reportagem de capa, o melhor da semana do site, conteúdo exclusivo, cartazes e agenda — diagramada como uma revista impressa.</p>
      <div class="feats">
        <span>Edição fechada semanal — sem rolagem infinita</span>
        <span>Leia no site como revista ou baixe o PDF</span>
        <span>Grátis no seu e-mail, toda quinta às 7h — um dia antes de todo mundo</span>
      </div>
    </div>
    <div class="signup-card" id="signup-conversa">
      <h3>Assinante lê na quinta, às 7h</h3>
      <p class="sg-chamada">Uma edição fechada, com começo, meio e fim, na sua caixa de entrada. De graça.</p>
      <button type="button" class="sg-abrir" data-conversa>🎟 Quero a minha</button>
      <span class="fine">Sem spam, cancele quando quiser. Seus dados ficam só com o FOYER.</span>
    </div>
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
    return f'''<main id="conteudo" class="wrap">
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

# ---------------------------------------------------------------- PÁGINAS DE AUTOR (assinaturas do FOYER)
# Quem assina responde pelo texto: cada assinatura tem página própria, com o que
# cobre e tudo o que já publicou. Serve ao leitor e à autoridade do site.
AUTORES = {
    'pedro-amaral': {
        'nome': 'Pedro Amaral',
        'cargo': 'Editor-chefe',
        'cobre': 'Mercado e economia criativa, bilheteria e financiamento da cultura, cinema e streaming',
        'bio': ('Editor-chefe do FOYER. Escreve sobre o dinheiro que move a cultura: quanto custa montar '
                'um espetáculo, de onde vem o financiamento, como anda a bilheteria e o que o mercado de '
                'cinema e streaming faz com o que nasce no palco.'),
    },
    'isabel-branquinha': {
        'nome': 'Isabel Branquinha',
        'cargo': 'Editora',
        'cobre': 'Estreias e temporadas de teatro, a cena das artes em São Paulo',
        'bio': ('Editora do FOYER. Acompanha as estreias e temporadas do teatro brasileiro e a agenda das '
                'artes em São Paulo, com atenção à ficha técnica, à trajetória das montagens e ao serviço '
                'completo para quem vai assistir.'),
    },
    'redacao-foyer': {
        'nome': 'Redação Foyer',
        'cargo': 'Assinatura coletiva',
        'cobre': 'Bastidores, explicadores, memória, curiosidades, listas e guias, patrimônio e notícia internacional',
        'bio': ('Assinatura coletiva da redação do FOYER. Reúne o trabalho de apuração da casa em bastidores, '
                'explicadores sobre como o teatro funciona por dentro, memória das artes brasileiras e a '
                'cobertura internacional. Todo texto passa por checagem independente antes de ir ao ar.'),
    },
}
_AUTOR_SLUG = {a['nome']: sp for sp, a in AUTORES.items()}

def autor_page(sp, a, mats):
    rows = ''
    for p in mats[:120]:
        rows += f'''    <a class="agd-row" href="post-{p['slug']}.html">
      <span class="agd-date"><b style="font-size:.9rem">{p.get('short','')}</b><small>{p.get('iso','')[:4]}</small></span>
      <span class="agd-what"><h3 style="font-size:.95rem">{_rvesc(p['title'])}</h3></span>
      <span class="tag agd-tag">{_rvesc(p.get('cat',''))}</span>
    </a>\n'''
    if not rows:
        rows = '    <p class="vazio" style="padding:18px 0">Ainda sem matérias publicadas nesta assinatura.</p>\n'
    total = len(mats)
    anos = sorted(p.get('iso', '')[:4] for p in mats if p.get('iso'))
    desde = anos[0] if anos else ''
    mais = (f'<div class="filters" style="padding:6px 0 0"><a href="busca.html">Ver todas as {total} no acervo →</a></div>'
            if total > 120 else '')
    return f'''<main id="conteudo" class="wrap">
  <div class="art" style="max-width:900px; margin:0 auto">
    <div class="art-head" style="padding-top:30px">
      <div class="tags"><span class="tag wine">Quem assina no FOYER</span><span class="tag">{_rvesc(a['cargo'])}</span></div>
      <h1>{_rvesc(a['nome'])}</h1>
      <div class="art-byline">
        <span><b>{total}</b> matéria(s) publicada(s)</span>
        {f'<span>No FOYER desde {desde}</span>' if desde else ''}
      </div>
      <p class="dek" style="margin-top:14px">{_rvesc(a['bio'])}</p>
      <p class="meta-l" style="display:block;margin-top:10px"><b>Cobre:</b> {_rvesc(a['cobre'])}</p>
      <div class="share-row" aria-label="Compartilhar esta página">
        <button class="sbtn" data-share="copy" data-title="{safe(a['nome'])} no FOYER">Copiar link</button>
      </div>
    </div>
    <div class="agd" style="margin-top:26px">
{rows}    </div>
    {mais}
    <div class="filters" style="padding:24px 0 40px">
      <a href="principios.html">Princípios editoriais</a>
      <a href="sobre.html">Quem somos</a>
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
    f'<li><b>{_rvesc(u["nome"])}</b> · {"Direção e edição" if u.get("papel") == "chefe" else "Redação"}</li>'
    for u in _EQ_PUB)
_n_eps = sum(len(p.get('videos', [])) for p in YT.get('programas', []))
sobre_body = band('O Foyer', 'Quem somos', 'Seu veículo de informação artístico') + f'''
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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
<main id="conteudo" class="wrap">
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

# abertura do aplicativo: uma arte brutalista sorteada a cada entrada (só no app instalado)
_SPLASH = '''<div id="abre" hidden>
<style>
#abre{ position:fixed; inset:0; z-index:999; background:#380A06; opacity:1; transition:opacity .5s; }
#abre.sai{ opacity:0; pointer-events:none; }
#abre svg.fundo{ position:absolute; inset:0; width:100%; height:100%; }
#abre .marca{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; z-index:2; }
#abre.alto .marca{ justify-content:flex-start; padding-top:64px; }
#abre .marca img{ width:150px; filter:drop-shadow(0 4px 22px rgba(0,0,0,.55)); }
#abre .marca span{ margin-top:18px; font-family:var(--mono); font-weight:600; font-size:.6rem;
  letter-spacing:.34em; text-transform:uppercase; color:#CEB26A; text-align:center; padding:0 20px; }
</style>
<svg width="0" height="0" style="position:absolute">
<defs>
<filter id="ab-gr"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<pattern id="ab-cab" width="62" height="44" patternUnits="userSpaceOnUse"><circle cx="31" cy="28" r="16" fill="#170606"/></pattern>
<pattern id="ab-lmp" width="46" height="46" patternUnits="userSpaceOnUse"><circle cx="23" cy="23" r="6" fill="#CEB26A"/></pattern>
<symbol id="ab-1" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#380A06"/><polygon points="195,-40 30,844 360,844" fill="#E9CB85" opacity=".18"/><ellipse cx="195" cy="800" rx="150" ry="26" fill="#E9CB85" opacity=".3"/><circle cx="195" cy="690" r="26" fill="#120505"/><rect x="164" y="719" width="62" height="95" rx="10" fill="#120505"/><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
<symbol id="ab-2" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#4E0F09"/><rect x="10" width="18" height="844" fill="#380A06"/><rect x="54" width="22" height="844" fill="#380A06"/><rect x="100" width="16" height="844" fill="#380A06"/><rect x="142" width="24" height="844" fill="#380A06"/><rect x="192" width="18" height="844" fill="#380A06"/><rect x="234" width="22" height="844" fill="#380A06"/><rect x="280" width="16" height="844" fill="#380A06"/><rect x="322" width="24" height="844" fill="#380A06"/><rect x="366" width="18" height="844" fill="#380A06"/><rect width="390" height="90" fill="#E9CB85" opacity=".14"/><rect y="760" width="390" height="14" fill="#CEB26A" opacity=".85"/><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
<symbol id="ab-3" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#380A06"/><ellipse cx="195" cy="180" rx="300" ry="200" fill="#E9CB85" opacity=".13"/><rect y="560" width="390" height="284" fill="url(#ab-cab)"/><circle cx="217" cy="644" r="16" fill="#CEB26A"/><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
<symbol id="ab-4" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#380A06"/><rect width="390" height="56" fill="url(#ab-lmp)" opacity=".9"/><rect y="788" width="390" height="56" fill="url(#ab-lmp)" opacity=".9"/><rect x="36" y="250" width="318" height="344" fill="none" stroke="#CEB26A" stroke-width="3"/><rect x="36" y="250" width="318" height="344" fill="#E9CB85" opacity=".08"/><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
<symbol id="ab-5" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#380A06"/><rect x="62" width="4" height="844" fill="#CEB26A" opacity=".55"/><rect x="134" width="4" height="844" fill="#CEB26A" opacity=".4"/><rect x="206" width="4" height="844" fill="#CEB26A" opacity=".55"/><rect x="278" width="4" height="844" fill="#CEB26A" opacity=".4"/><rect x="336" width="4" height="844" fill="#CEB26A" opacity=".55"/><rect x="50" y="420" width="34" height="66" fill="#CEB26A" opacity=".32"/><rect x="194" y="240" width="34" height="66" fill="#CEB26A" opacity=".32"/><rect x="322" y="560" width="34" height="66" fill="#CEB26A" opacity=".32"/><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
<symbol id="ab-6" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><rect width="390" height="844" fill="#380A06"/><circle cx="195" cy="320" r="34" fill="#E9CB85" opacity=".18"/><circle cx="195" cy="460" r="34" fill="#E9CB85" opacity=".38"/><circle cx="195" cy="650" r="46" fill="#CEB26A"/><g stroke="#E9CB85" stroke-width="3" opacity=".7"><line x1="195" y1="560" x2="195" y2="530"/><line x1="131" y1="586" x2="110" y2="565"/><line x1="259" y1="586" x2="280" y2="565"/><line x1="105" y1="650" x2="75" y2="650"/><line x1="285" y1="650" x2="315" y2="650"/></g><rect width="390" height="844" filter="url(#ab-gr)" opacity=".12"/></symbol>
</defs>
</svg>
<svg class="fundo" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice"><use id="abre-use" href="#ab-1"/></svg>
<div class="marca"><img src="assets/logo/foyer-stacked-gold-sm.png" alt="FOYER"><span class="abre-frase">O saguão do teatro brasileiro</span></div>
</div>
<script>(function(){try{
  var el = document.getElementById('abre');
  var app = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if(!app || sessionStorage.getItem('foyer-abriu')){ el.remove(); return; }
  sessionStorage.setItem('foyer-abriu', '1');
  var n = 1 + Math.floor(Math.random() * 6);
  document.getElementById('abre-use').setAttribute('href', '#ab-' + n);
  if(n === 6){ el.classList.add('alto'); el.querySelector('.abre-frase').textContent = 'Terceiro sinal: vai começar'; }
  el.hidden = false;
  setTimeout(function(){ el.classList.add('sai'); setTimeout(function(){ el.remove(); }, 550); }, 1400);
}catch(e){}})();</script>'''

# capa tem ordem própria: ticker+masthead antes da nav
capa_html = (head('FOYER — Teatro, Cultura & Arte',
                  'FOYER — portal de teatro, música e cultura. Notícias, crítica, revista semanal, programas e a Enciclopédia do Teatro Musical Brasileiro.')
             + '\n' + _SPLASH + '\n' + DEFS + '\n' + index_body + '\n' + UTIL + '\n' + nav('index.html')
             + '\n' + index_main + '\n' + ADS_CASA + FOOTER + '</body>\n</html>\n')
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
    _posts = [x for x in MATERIAS if x['cat'] == _c or _c in x.get('cats', [])]
    _cp = (len(_posts) + POR_PAGINA - 1) // POR_PAGINA
    _base = 'cat-' + _cat_slug(_c)
    for _n in range(1, _cp + 1):
        _fname = f'{_base}.html' if _n == 1 else f'{_base}-p{_n}.html'
        page(_fname, f'{_c} — FOYER', f'Matérias de {_c} no FOYER.', 'noticias.html',
             listing_body(_posts, _n, _cp, _base, _c,
                          f'{len(_posts)} matérias — página {_n} de {_cp}', active=_c))

_ec_posts = [x for x in MATERIAS if _em_cartaz(x)]
_ec_pages = max(1, (len(_ec_posts) + POR_PAGINA - 1) // POR_PAGINA)
for _n in range(1, _ec_pages + 1):
    _fname = 'cat-em-cartaz.html' if _n == 1 else f'cat-em-cartaz-p{_n}.html'
    page(_fname, 'Em Cartaz — FOYER', 'Peças em temporada agora, cobertas pelo FOYER.', 'noticias.html',
         listing_body(_ec_posts, _n, _ec_pages, 'cat-em-cartaz', 'Em Cartaz',
                      f'{len(_ec_posts)} espetáculo(s) em temporada agora — a página se atualiza sozinha',
                      active='Em Cartaz'))
page('critica.html', 'Crítica — FOYER', 'Críticas de teatro, musicais, dança e ópera no FOYER.', 'critica.html', critica_body)
page('entrevistas.html', 'Entrevistas — FOYER', 'Entrevistas com artistas e profissionais do palco.', 'entrevistas.html', entrevistas_body)
page('agenda.html', 'Agenda — FOYER', 'Estreias, temporadas e eventos de teatro pelo Brasil.', 'agenda.html', agenda_body)
page('programas.html', 'Programas — FOYER', 'Os programas do canal Foyer no YouTube e Spotify.', 'programas.html', programas_body)
page('enciclopedia.html', 'Enciclopédia — FOYER', 'Enciclopédia do Teatro Musical Brasileiro: artistas, espetáculos e fichas técnicas.', 'enciclopedia.html', enciclopedia_body)
page('revista.html', 'A Revista — FOYER', 'A revista semanal do Foyer: edições fechadas para ler online ou baixar em PDF.', 'revista.html', revista_body)
page('busca.html', 'Buscar — FOYER', 'Busque matérias, críticas, artistas e espetáculos no FOYER.', 'busca.html', busca_body)
page('sobre.html', 'Quem somos — FOYER', 'O FOYER: portal de jornalismo cultural e canal de programas sobre teatro, música e artes.', 'index.html', sobre_body)
page('contato.html', 'Contato — FOYER', 'Fale com a redação do FOYER: pautas, imprensa, parcerias e publicidade.', 'index.html', contato_body)
principios_body = band('Institucional', 'Princípios Editoriais', 'Como o FOYER apura, escreve e corrige') + '''
<main id="conteudo" class="wrap">
  <div class="art" style="max-width:820px; margin:0 auto">
    <div class="art-body" style="padding-top:34px">
      <h2>O que publicamos</h2>
      <p>O FOYER cobre teatro, música e artes cênicas no Brasil e no mundo: notícias, guias de programação, explicadores, perfis e memória do palco. Todo conteúdo publicado é baseado em fatos verificáveis, com fontes citadas no próprio texto sempre que a informação não for de apuração direta da casa.</p>
      <h2>Apuração e revisão</h2>
      <p>Matérias assinadas como Redação Foyer podem contar com apuração assistida por inteligência artificial. Nenhuma delas chega ao site sem passar por revisão e aprovação de um editor humano, que responde pelo que foi publicado. Serviço (datas, horários, preços e locais) é conferido na fonte antes da publicação e vale para a data em que a matéria foi ao ar.</p>
      <h2>Correções</h2>
      <p>Erramos? Corrigimos. Matérias corrigidas ou ampliadas exibem o selo "Atualizada em" com data e horário da mudança. Para apontar um erro, escreva para <a href="mailto:programafoyer@gmail.com">programafoyer@gmail.com</a> com o endereço da matéria: respondemos e, quando for o caso, corrigimos com registro visível.</p>
      <h2>Imagens e créditos</h2>
      <p>Usamos fotografias de divulgação oficial das produções que cobrimos, imagens em licença livre (com autor e licença citados) e material próprio. O crédito do fotógrafo acompanha a imagem, no cartão e dentro da matéria.</p>
      <h2>Independência</h2>
      <p>Conteúdo publicitário ou patrocinado, quando existir, é identificado como tal. A curadoria dos guias e da agenda é decisão exclusiva da redação, sem interferência de bilheteiras ou produções.</p>
      <h2>Quem responde</h2>
      <p>O FOYER é dirigido por Pedro Amaral e Isabel Branquinha. Fale com a redação: <a href="mailto:programafoyer@gmail.com">programafoyer@gmail.com</a> ou pela página de <a href="contato.html">contato</a>.</p>
    </div>
  </div>
</main>
'''
page('principios.html', 'Princípios Editoriais — FOYER', 'Como o FOYER apura, escreve, credita imagens e corrige: os princípios editoriais da casa.', 'principios.html', principios_body)
page('privacidade.html', 'Política de Privacidade — FOYER', 'Política de privacidade e cookies do FOYER.', 'privacidade.html', privacidade_body)

# ---- mídia kit: a página comercial da revista, com o retrato agregado do leitor
anuncie_body = band('Comercial', 'Anuncie no FOYER', 'No site todos os dias, na revista toda quinta. Veja como o seu anúncio fica antes de fechar — e feche direto no WhatsApp') + '''
<main id="conteudo" class="wrap">
  <style>
    .az-palco{ position:relative; overflow:hidden; border:3px solid var(--ink); background:#380A06;
      color:var(--paper); margin:26px 0; min-height:240px; display:flex; align-items:center; justify-content:center; }
    .az-palco .luz{ position:absolute; left:50%; top:-40px; width:520px; height:460px; transform:translateX(-50%);
      background:radial-gradient(ellipse at top, rgba(233,203,133,.32), transparent 62%); pointer-events:none; }
    .az-palco .dentro{ position:relative; text-align:center; padding:44px 24px; z-index:2; }
    .az-palco .dentro em{ display:block; font-style:normal; font-family:var(--mono); font-size:.6rem;
      letter-spacing:.3em; text-transform:uppercase; color:var(--gold); }
    .az-palco .dentro h2{ font-family:var(--didone); font-weight:400; font-size:clamp(1.9rem,5vw,2.9rem);
      line-height:1.05; margin:10px 0 8px; color:var(--paper); }
    .az-palco .dentro p{ margin:0; color:rgba(239,232,218,.85); font-size:.95rem; }
    .az-cort{ position:absolute; top:0; bottom:0; width:54%; z-index:4;
      background:repeating-linear-gradient(90deg, #4E0F09 0 26px, #3d0c07 26px 52px);
      box-shadow:0 0 34px rgba(0,0,0,.5); }
    .az-cort.e{ left:0; transform-origin:left center; animation:azAbre 1.2s .35s cubic-bezier(.7,0,.3,1) forwards; }
    .az-cort.d{ right:0; transform-origin:right center; animation:azAbre 1.2s .35s cubic-bezier(.7,0,.3,1) forwards; }
    @keyframes azAbre{ to{ transform:scaleX(.04); } }

    .az-wiz{ border:3px solid var(--ink); background:var(--paper); margin:26px 0 10px; }
    .az-topo{ display:flex; align-items:center; gap:8px; padding:14px 18px; border-bottom:2px solid var(--ink); flex-wrap:wrap; }
    .az-topo b{ font-family:var(--didone); font-weight:400; font-size:1.3rem; }
    .az-pts{ margin-left:auto; display:flex; gap:6px; align-items:center; }
    .az-pts i{ width:10px; height:10px; border:2px solid var(--ink); background:transparent; }
    .az-pts i.on{ background:var(--gold); }
    .az-pts small{ font-family:var(--mono); font-size:.56rem; letter-spacing:.1em; color:var(--ink-soft); margin-left:6px; }
    .az-corpo{ padding:18px; }
    .az-passo{ display:none; }
    .az-passo.on{ display:block; animation:azSobe .35s ease; }
    @keyframes azSobe{ from{ opacity:0; transform:translateY(10px);} to{ opacity:1; transform:none; } }
    .az-passo h4{ font-family:var(--didone); font-weight:400; font-size:1.3rem; margin:0 0 4px; }
    .az-passo .sub{ font-size:.86rem; color:var(--ink-soft); margin:0 0 14px; }

    /* passo 1: os formatos como cartões explicados */
    .az-fgrid{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    @media (max-width:760px){ .az-fgrid{ grid-template-columns:1fr; } }
    .az-fcard{ border:2px solid var(--ink); background:transparent; text-align:left; cursor:pointer;
      padding:12px 14px; font:inherit; color:inherit; transition:transform .15s ease; }
    .az-fcard:hover{ transform:translateY(-2px); }
    .az-fcard.on{ background:var(--wine); color:var(--paper); border-color:var(--wine); }
    .az-fcard.on .fc-onde{ color:var(--gold); }
    .az-fcard b{ font-family:var(--didone); font-weight:400; font-size:1.1rem; display:block; }
    .az-fcard .fc-onde{ font-family:var(--mono); font-size:.54rem; font-weight:700; letter-spacing:.14em;
      text-transform:uppercase; color:var(--wine); display:block; margin-bottom:3px; }
    .az-fcard span{ font-size:.8rem; line-height:1.45; display:block; margin-top:4px; opacity:.9; }
    .az-como{ border-left:4px solid var(--gold); background:rgba(206,178,106,.1); padding:12px 16px; margin-top:14px; display:none; }
    .az-como.on{ display:block; animation:azSobe .3s ease; }
    .az-como h5{ font-family:var(--mono); font-size:.58rem; font-weight:700; letter-spacing:.18em;
      text-transform:uppercase; color:var(--wine); margin:0 0 6px; }
    .az-como p{ margin:0 0 8px; font-size:.88rem; line-height:1.6; }
    .az-como ul{ margin:0; padding-left:16px; font-size:.8rem; color:var(--ink-soft); }
    .az-como li{ margin:3px 0; }
    .az-campo{ margin:0 0 12px; }
    .az-campo label{ display:block; font-family:var(--mono); font-size:.58rem; font-weight:700;
      letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:5px; }
    .az-campo input, .az-campo textarea{ width:100%; box-sizing:border-box; border:2px solid var(--ink);
      background:var(--paper); color:var(--ink); font:inherit; padding:10px 12px; }
    .az-campo small{ display:block; font-size:.74rem; color:var(--ink-soft); margin-top:4px; }
    .az-ops{ display:flex; flex-wrap:wrap; gap:10px; }
    .az-op{ border:2px solid var(--ink); background:transparent; cursor:pointer; padding:10px 14px;
      font:inherit; font-size:.88rem; font-weight:600; color:inherit; }
    .az-op.on{ background:var(--wine); color:var(--gold); border-color:var(--wine); }

    /* passo 2: o provador — a arte aplicada de verdade */
    .az-prova{ display:grid; grid-template-columns:280px 1fr; gap:18px; align-items:start; }
    @media (max-width:760px){ .az-prova{ grid-template-columns:1fr; } }
    .az-envio{ border:2px dashed var(--wine); padding:14px; text-align:center; }
    .az-envio input{ display:none; }
    .az-envio .bt-arte{ display:inline-block; border:2px solid var(--wine); background:var(--wine); color:var(--gold);
      cursor:pointer; padding:11px 16px; font-family:var(--mono); font-weight:700; font-size:.6rem;
      letter-spacing:.12em; text-transform:uppercase; }
    .az-envio p{ font-size:.76rem; color:var(--ink-soft); margin:10px 0 0; line-height:1.5; }
    .az-envio .ok{ display:none; margin-top:8px; font-family:var(--mono); font-size:.6rem; color:#2c5a2e; font-weight:700; }
    .pv-caixa{ display:flex; justify-content:center; }
    .pv-rot{ text-align:center; font-family:var(--mono); font-size:.56rem; letter-spacing:.18em;
      text-transform:uppercase; color:var(--ink-soft); margin:8px 0 0; }
    /* o site em miniatura */
    .pv-site{ position:relative; width:100%; max-width:430px; aspect-ratio:4/5; border:3px solid var(--ink);
      background:var(--paper); overflow:hidden; }
    .pv-site .nav{ height:34px; background:var(--wine); display:flex; align-items:center; padding:0 12px;
      color:var(--gold); font-family:var(--didone); font-size:.95rem; }
    .pv-site .tit{ margin:14px 12px 8px; height:16px; width:70%; background:#d8cdb4; }
    .pv-site .ln{ margin:7px 12px; height:7px; background:#e4dcc6; }
    .pv-site .ln.c{ width:55%; }
    .pv-ent{ margin:12px; border:2px solid var(--ink); padding:8px; display:none; }
    .pv-ent em{ display:block; font-style:normal; font-family:var(--mono); font-size:.44rem; font-weight:700;
      letter-spacing:.2em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:6px; }
    .pv-ent .arte{ aspect-ratio:16/9; }
    .pv-cortina{ position:absolute; inset:0; background:rgba(20,6,3,.72); display:none;
      align-items:center; justify-content:center; padding:16px; }
    .pv-cortina .cx{ background:var(--paper); border:3px solid var(--ink); width:78%; padding:8px;
      box-shadow:0 14px 40px rgba(0,0,0,.5); position:relative; }
    .pv-cortina .cx::after{ content:'✕'; position:absolute; top:-12px; right:-12px; width:26px; height:26px;
      background:var(--gold); color:var(--wine); border:2px solid var(--ink); display:flex; align-items:center;
      justify-content:center; font-weight:700; font-size:.8rem; }
    .pv-cortina em{ display:block; font-style:normal; font-family:var(--mono); font-size:.44rem; font-weight:700;
      letter-spacing:.2em; text-transform:uppercase; color:var(--ink-soft); margin:2px 0 6px; }
    .pv-cortina .arte{ aspect-ratio:4/5; }
    .pv-faixa{ position:absolute; left:0; right:0; bottom:0; background:var(--paper); border-top:2px solid var(--ink);
      display:none; align-items:center; gap:8px; padding:8px 10px; box-shadow:0 -4px 14px rgba(0,0,0,.2); }
    .pv-faixa em{ font-style:normal; font-family:var(--mono); font-size:.4rem; font-weight:700;
      letter-spacing:.16em; text-transform:uppercase; color:var(--ink-soft); }
    .pv-faixa span{ flex:1; font-size:.68rem; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .pv-faixa b{ font-size:.7rem; }
    /* a página da revista em miniatura */
    .pv-pg{ position:relative; width:300px; aspect-ratio:720/972; border:3px solid var(--ink);
      background:#F6F1E6; overflow:hidden; display:none; flex-direction:column; }
    .pv-pg .selo{ position:absolute; top:0; left:0; z-index:3; background:var(--gold); color:var(--wine);
      font-family:var(--mono); font-size:.44rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase;
      padding:4px 8px; }
    .pv-pg .arte-cheia{ flex:1; }
    .pv-pg .folio{ height:26px; border-top:2px solid var(--ink); display:flex; align-items:center;
      justify-content:space-between; padding:0 10px; font-family:var(--mono); font-size:.4rem;
      letter-spacing:.12em; text-transform:uppercase; color:var(--ink-soft); }
    .pv-pg .txts{ padding:12px 12px 6px; }
    .pv-pg .txts .tit{ height:13px; width:80%; background:#d8cdb4; margin-bottom:8px; }
    .pv-pg .txts .ln{ height:6px; background:#e4dcc6; margin:5px 0; }
    .pv-pg .txts .ln.c{ width:60%; }
    .pv-meia{ margin:8px 12px 10px; border:2px solid var(--ink); padding:6px; margin-top:auto; }
    .pv-meia em{ display:block; font-style:normal; font-family:var(--mono); font-size:.42rem; font-weight:700;
      letter-spacing:.18em; text-transform:uppercase; color:var(--ink-soft); margin-bottom:5px; }
    .pv-meia .arte{ aspect-ratio:16/9; }
    .pv-cupom{ position:absolute; left:10px; right:10px; bottom:34px; z-index:3; display:none;
      border:2px dashed var(--wine); background:var(--paper); padding:6px 8px; align-items:center; gap:8px; }
    .pv-cupom i{ font-style:normal; font-size:.6rem; }
    .pv-cupom span{ flex:1; font-size:.56rem; line-height:1.3; }
    .pv-cupom b{ font-family:var(--mono); font-size:.6rem; border-left:2px dashed var(--wine); padding-left:8px; }
    /* a arte (ou o convite a ela) */
    .arte{ position:relative; background:#4E0F09; display:flex; align-items:center; justify-content:center; overflow:hidden; }
    .arte img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
    .arte .ph{ color:var(--gold); font-family:var(--mono); font-size:.5rem; font-weight:700;
      letter-spacing:.18em; text-transform:uppercase; text-align:center; border:2px dashed var(--gold);
      padding:10px 12px; opacity:.85; }

    .az-rev{ border:2px dashed var(--wine); padding:12px 14px; margin-bottom:12px; }
    .az-rev div{ display:flex; gap:10px; padding:3px 0; font-size:.86rem; align-items:flex-start; }
    .az-rev em{ font-style:normal; font-family:var(--mono); font-size:.56rem; letter-spacing:.12em;
      text-transform:uppercase; color:var(--ink-soft); min-width:110px; padding-top:3px; }
    .az-rev img{ max-width:130px; max-height:100px; border:2px solid var(--ink); }
    .az-nav{ display:flex; gap:10px; padding:0 18px 18px; }
    .az-volta{ border:2px solid var(--ink); background:transparent; cursor:pointer; padding:12px 16px;
      font-family:var(--mono); font-weight:700; font-size:.62rem; letter-spacing:.12em; text-transform:uppercase; }
    .az-vai{ margin-left:auto; border:2px solid var(--wine); background:var(--wine); color:var(--gold);
      cursor:pointer; padding:12px 20px; font-family:var(--mono); font-weight:700; font-size:.62rem;
      letter-spacing:.12em; text-transform:uppercase; }
    .az-vai:hover{ background:var(--gold); color:var(--wine); }
    .az-erro{ color:#8a1f14; font-size:.82rem; margin:8px 18px 0; display:none; }
    .az-fim{ text-align:center; padding:34px 18px; display:none; }
    .az-fim.on{ display:block; animation:azSobe .4s ease; }
    .az-fim .carimbo{ display:inline-block; border:3px solid #2c5a2e; color:#2c5a2e; font-family:var(--mono);
      font-weight:700; font-size:.8rem; letter-spacing:.2em; text-transform:uppercase; padding:10px 18px;
      transform:rotate(-3deg); margin-bottom:14px; }
    .az-fim h3{ font-family:var(--didone); font-weight:400; font-size:1.7rem; margin:0 0 8px; }
    .az-fim p{ margin:0; color:var(--ink-soft); }
    .az-nota{ font-family:var(--mono); font-size:.6rem; letter-spacing:.08em; color:var(--ink-soft); margin:10px 0 30px; }
    .mk-leitor{ display:none; border:2px solid var(--wine); padding:18px 20px; margin:0 0 26px; }
    .mk-leitor.mostra{ display:block; }
    .mk-leitor h2{ font-family:var(--didone); font-weight:400; font-size:1.5rem; margin:0 0 4px; }
    .mk-leitor .mk-nota{ font-family:var(--mono); font-size:.62rem; letter-spacing:.08em; color:var(--ink-soft); }
    .mk-tiles{ display:flex; flex-wrap:wrap; gap:14px; margin:14px 0 4px; }
    .mk-tile{ border:2px solid var(--ink); padding:10px 16px; min-width:130px; }
    .mk-tile b{ display:block; font-family:var(--didone); font-size:1.7rem; font-weight:400; color:var(--wine); }
    .mk-tile span{ font-family:var(--mono); font-size:.56rem; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-soft); }
    @media (prefers-reduced-motion:reduce){ .az-cort.e,.az-cort.d{ animation:none; transform:scaleX(.04); } }
  </style>

  <div class="az-palco">
    <div class="az-cort e"></div><div class="az-cort d"></div>
    <div class="luz"></div>
    <div class="dentro">
      <em>Terceiro sinal</em>
      <h2>Veja o seu anúncio no palco antes de fechar</h2>
      <p>Escolha o formato, suba a sua arte e confira a aplicação na hora. O pedido cai direto na mesa da direção.</p>
    </div>
  </div>

  <div class="az-wiz" id="az-wiz">
    <div class="az-topo"><b>Contratar em 5 passos</b><span class="az-pts" id="az-pts"></span></div>
    <div class="az-corpo">

      <div class="az-passo on" data-p="1">
        <h4>1. Onde a sua marca entra?</h4>
        <p class="sub">Toque num formato para ver exatamente onde ele aparece e o que você precisa mandar.</p>
        <div class="az-fgrid" id="az-formatos"></div>
        <div class="az-como" id="az-como"></div>
        <div class="az-campo" id="az-cupom-op" style="display:none;margin-top:12px">
          <label>Bilhete do leitor (só na página inteira)</label>
          <button class="az-op" type="button" id="az-cupom-bt">🎟 Quero o cupom destacável no anúncio</button>
          <small>um código exclusivo seu, que o leitor copia com um toque e você confere na bilheteria; o código é combinado por escrito na conversa</small>
        </div>
      </div>

      <div class="az-passo" data-p="2">
        <h4>2. A arte — veja como fica</h4>
        <p class="sub" id="az-arte-sub">Suba a sua arte e ela entra na aplicação real, na hora.</p>
        <div class="az-prova">
          <div class="az-envio" id="az-envio">
            <label class="bt-arte" for="az-arquivo">Subir a minha arte</label>
            <input type="file" id="az-arquivo" accept="image/*">
            <span class="ok" id="az-arte-ok">✓ arte aplicada — confira ao lado</span>
            <p id="az-arte-spec"></p>
            <p style="margin-top:8px">Ainda não tem a arte? Siga sem ela: a gente acerta na conversa (e fazemos a arte com você, se precisar).</p>
          </div>
          <div>
            <div class="pv-caixa">
              <div class="pv-site" id="pv-site">
                <div class="nav">FOYER</div>
                <div class="tit"></div>
                <div class="ln"></div><div class="ln"></div><div class="ln c"></div>
                <div class="pv-ent" id="pv-ent"><em>Publicidade</em><div class="arte" data-arte><span class="ph">Sua arte aqui</span></div></div>
                <div class="ln"></div><div class="ln"></div><div class="ln c"></div><div class="ln"></div>
                <div class="pv-cortina" id="pv-cortina"><div class="cx"><em>Publicidade</em><div class="arte" data-arte><span class="ph">Sua arte aqui</span></div></div></div>
                <div class="pv-faixa" id="pv-faixa"><em>Publicidade</em><span id="pv-faixa-tx">A sua mensagem, com link para a bilheteria</span><b>✕</b></div>
              </div>
              <div class="pv-pg" id="pv-pg">
                <span class="selo">Publicidade</span>
                <div class="arte arte-cheia" id="pv-pg-cheia" data-arte><span class="ph">Sua arte aqui<br>página inteira</span></div>
                <div class="txts" id="pv-pg-txts" style="display:none"><div class="tit"></div>
                  <div class="ln"></div><div class="ln"></div><div class="ln c"></div><div class="ln"></div><div class="ln"></div><div class="ln c"></div></div>
                <div class="pv-meia" id="pv-meia" style="display:none"><em>Publicidade</em><div class="arte" data-arte><span class="ph">Sua arte aqui</span></div></div>
                <div class="pv-cupom" id="pv-cupom"><i>✂</i><span>O seu benefício para o leitor do FOYER</span><b>SEUCODIGO</b></div>
                <div class="folio"><span>FOYER · A REVISTA</span><span>PÁG. 9</span></div>
              </div>
            </div>
            <p class="pv-rot" id="pv-rot">a aplicação real do seu anúncio</p>
            <div class="az-campo" id="az-faixa-campo" style="display:none;margin-top:10px">
              <label>A sua linha na faixa (o texto é o anúncio)</label>
              <input type="text" id="az-faixa-tx" maxlength="90" placeholder="Peça X em cartaz no Teatro Y — ingressos com 20% off">
            </div>
          </div>
        </div>
      </div>

      <div class="az-passo" data-p="3">
        <h4>3. A temporada</h4>
        <div class="az-campo"><label>Quando você quer estrear?</label>
          <input type="text" id="az-inicio" placeholder="ex.: semana que vem · edição de 6 de agosto · o quanto antes"></div>
        <div class="az-campo"><label>Por quanto tempo?</label>
          <div class="az-ops" id="az-duracao"></div></div>
      </div>

      <div class="az-passo" data-p="4">
        <h4>4. Quem assina</h4>
        <div class="az-campo"><label>Seu nome *</label><input type="text" id="az-nome"></div>
        <div class="az-campo"><label>Produção / empresa</label><input type="text" id="az-empresa" placeholder="ex.: nome do espetáculo, teatro ou produtora"></div>
        <div class="az-campo"><label>E-mail *</label><input type="email" id="az-email"></div>
        <div class="az-campo"><label>WhatsApp (com DDD) *</label><input type="tel" id="az-whats" placeholder="11 90000-0000">
          <small>é por ele que fechamos valores e datas, sem vendedor no meio</small></div>
        <div class="az-campo"><label>Instagram (opcional)</label><input type="text" id="az-insta" placeholder="@suacasa"></div>
        <div class="az-campo"><label>Algo mais sobre o anúncio? (opcional)</label>
          <textarea id="az-msg" rows="3" placeholder="ex.: a temporada vai até setembro; queremos focar nos fins de semana"></textarea></div>
      </div>

      <div class="az-passo" data-p="5">
        <h4>5. Confira e suba ao palco</h4>
        <div class="az-rev" id="az-rev"></div>
        <p style="font-size:.84rem;color:var(--ink-soft);margin:0">Ao enviar, o pedido (com a sua arte) cai direto na mesa da direção do FOYER.
        Valores são fechados na conversa de WhatsApp, sem tabela pública e sem intermediário. Nada vai ao ar sem o seu ok final.</p>
      </div>
    </div>
    <p class="az-erro" id="az-erro"></p>
    <div class="az-nav">
      <button class="az-volta" type="button" id="az-volta" style="visibility:hidden">← Voltar</button>
      <button class="az-vai" type="button" id="az-vai">Avançar →</button>
    </div>
    <div class="az-fim" id="az-fim">
      <span class="carimbo">Pedido na mesa</span>
      <h3>Recebido! Agora é com a gente.</h3>
      <p>A direção do FOYER te chama no WhatsApp para fechar valores e datas.<br>Sem formulário de volta, sem vendedor: uma conversa e pronto.</p>
    </div>
  </div>
  <p class="az-nota">Curadoria editorial não é negociável: anúncio é sempre rotulado, nunca vira matéria. Máximo de 2 páginas pagas por edição da revista.</p>

  <div class="mk-leitor" id="mk-leitor">
    <h2>O leitor da revista</h2>
    <p class="mk-nota">Retrato agregado e anônimo dos assinantes cadastrados, direto do censo da casa.</p>
    <div class="mk-tiles" id="mk-tiles"></div>
  </div>
</main>
<script>
(function(){
  var M = { url:'https://jcaqjlrzmrtzjyfbljxh.supabase.co', key:'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' };
  var FORMATOS = [
    { id:'cortina', canal:'site', nome:'A Cortina de entrada', onde:'No site · na chegada',
      resumo:'A sua arte recebe quem chega ao FOYER, uma vez por dia.',
      como:'Quem abre qualquer página do site vê a sua arte numa caixa central, sobre o conteúdo, com o rótulo Publicidade e um botão de fechar. Aparece UMA vez por dia para cada visitante: presença garantida, sem irritar quem lê.',
      specs:['Arte: imagem na vertical ou quadrada (recomendado 1080×1350, JPG ou PNG)','Onde: todas as páginas do site','Frequência: 1 vez por dia por visitante','Link: a arte inteira clica para o seu endereço'],
      spec:'Imagem na vertical ou quadrada · recomendado 1080×1350' },
    { id:'entreato', canal:'site', nome:'O Entreato', onde:'No site · dentro das matérias',
      resumo:'O seu anúncio no meio da leitura, em todas as matérias.',
      como:'A sua arte entra DENTRO das matérias do site, depois do 4º parágrafo, com o rótulo Publicidade. O leitor encontra o anúncio no meio da leitura, como o intervalo de um espetáculo: é o formato de maior convivência com o conteúdo.',
      specs:['Arte: imagem na horizontal (recomendado 1200×675, JPG ou PNG)','Onde: todas as páginas de matéria do site','Frequência: sempre no ar durante a temporada contratada','Link: a arte clica para o seu endereço'],
      spec:'Imagem na horizontal · recomendado 1200×675' },
    { id:'faixa', canal:'site', nome:'A Faixa de proscênio', onde:'No site · rodapé fixo',
      resumo:'Uma linha sua, fixa no pé de todas as páginas.',
      como:'Uma única linha de texto, sua, fixa no rodapé de TODAS as páginas do site, com link direto para a sua bilheteria. O leitor pode dispensar a faixa; ela volta no dia seguinte. É o formato mais simples: nem precisa de arte.',
      specs:['Arte: NENHUMA — só o texto (até 90 caracteres) e o link','Onde: o rodapé de todas as páginas do site','Frequência: sempre à vista; o leitor pode dispensar por 1 dia','Link: a linha inteira clica para o seu endereço'],
      spec:'Sem imagem: escreva a sua linha abaixo e veja na hora' },
    { id:'pagina-inteira', canal:'revista', nome:'Página inteira', onde:'Na revista · uma página sua',
      resumo:'Uma página da edição é toda sua, para sempre no acervo.',
      como:'Uma página INTEIRA da revista de quinta é sua: a arte ocupa a página toda, com o rótulo Publicidade. As posições têm nome (a ímpar dos Recortes, a face da agenda, a porta da contracapa) e a edição fica na estante para sempre: o seu anúncio não some no feed. Pode carregar o bilhete do leitor: um cupom destacável com código exclusivo.',
      specs:['Arte: imagem na vertical, proporção da página (720×972; mande pelo menos 1440×1944)','Onde: uma página da edição, em posição nomeada','Permanência: a edição fica no acervo para sempre','Extra: o bilhete do leitor (cupom com código que você mede na bilheteria)'],
      spec:'Imagem na vertical, proporção 720×972 · mande pelo menos 1440×1944' },
    { id:'meia-pagina', canal:'revista', nome:'Meia página', onde:'Na revista · fim de matéria',
      resumo:'O leitor termina a matéria e encontra a sua arte.',
      como:'O pé da última página de uma matéria da edição é seu, como nas revistas impressas: o leitor termina o texto e encontra a sua arte, emoldurada e com o rótulo Publicidade. É o formato de entrada da revista, no lugar mais lido de todos: o fim de uma boa matéria.',
      specs:['Arte: imagem na horizontal (recomendado 1400×760, JPG ou PNG)','Onde: o pé da última página de uma matéria da edição','Permanência: a edição fica no acervo para sempre','Link: na revista lida no site, a arte clica para o seu endereço'],
      spec:'Imagem na horizontal · recomendado 1400×760' }
  ];
  var DURACOES = ['1 semana', '2 semanas', '1 mês', '1 edição', '2 edições', 'a combinar'];
  var st = { formato:'', cupom:false, duracao:'', arte:'' };
  var passo = 1, TOTAL = 5;
  var ROT = { 1:'o formato', 2:'a arte', 3:'a temporada', 4:'quem assina', 5:'a revisão' };

  function fmt(){ return FORMATOS.filter(function(x){ return x.id === st.formato; })[0]; }
  var elF = document.getElementById('az-formatos');
  elF.innerHTML = FORMATOS.map(function(f){
    return '<button class="az-fcard" type="button" data-f="' + f.id + '">' +
      '<span class="fc-onde">' + f.onde + '</span><b>' + f.nome + '</b><span>' + f.resumo + '</span></button>';
  }).join('');
  document.getElementById('az-duracao').innerHTML = DURACOES.map(function(d){
    return '<button class="az-op" type="button" data-d="' + d + '">' + d + '</button>';
  }).join('');

  function pintaComo(){
    var f = fmt(), el = document.getElementById('az-como');
    if(!f){ el.classList.remove('on'); return; }
    el.innerHTML = '<h5>Como aparece</h5><p>' + f.como + '</p><ul>' +
      f.specs.map(function(s2){ return '<li>' + s2 + '</li>'; }).join('') + '</ul>';
    el.classList.add('on');
    document.getElementById('az-cupom-op').style.display = f.id === 'pagina-inteira' ? '' : 'none';
  }
  function pintaProva(){
    var f = fmt();
    var site = document.getElementById('pv-site'), pg = document.getElementById('pv-pg');
    site.style.display = f && f.canal === 'site' ? 'block' : 'none';
    pg.style.display = f && f.canal === 'revista' ? 'flex' : 'none';
    document.getElementById('pv-cortina').style.display = f && f.id === 'cortina' ? 'flex' : 'none';
    document.getElementById('pv-faixa').style.display = f && f.id === 'faixa' ? 'flex' : 'none';
    document.getElementById('pv-ent').style.display = f && f.id === 'entreato' ? 'block' : 'none';
    var cheia = f && f.id === 'pagina-inteira';
    document.getElementById('pv-pg-cheia').style.display = cheia ? 'flex' : 'none';
    document.getElementById('pv-pg-txts').style.display = f && f.id === 'meia-pagina' ? 'block' : 'none';
    document.getElementById('pv-meia').style.display = f && f.id === 'meia-pagina' ? 'block' : 'none';
    document.getElementById('pv-cupom').style.display = cheia && st.cupom ? 'flex' : 'none';
    document.getElementById('az-faixa-campo').style.display = f && f.id === 'faixa' ? 'block' : 'none';
    document.getElementById('az-envio').style.display = f && f.id === 'faixa' ? 'none' : 'block';
    document.getElementById('az-arte-spec').textContent = f ? f.spec : '';
    document.getElementById('az-arte-sub').textContent = f && f.id === 'faixa'
      ? 'A faixa não usa imagem: escreva a sua linha e veja como ela fica no site.'
      : 'Suba a sua arte e ela entra na aplicação real, na hora.';
    document.getElementById('pv-rot').textContent = f
      ? (f.canal === 'site' ? 'a aplicação real no site do FOYER' : 'a aplicação real na página da revista')
      : '';
    aplicaArte();
  }
  function aplicaArte(){
    document.querySelectorAll('[data-arte]').forEach(function(cx){
      var img = cx.querySelector('img'), ph = cx.querySelector('.ph');
      if(st.arte){
        if(!img){ img = document.createElement('img'); cx.appendChild(img); }
        img.src = st.arte;
        if(ph) ph.style.display = 'none';
      } else {
        if(img) img.remove();
        if(ph) ph.style.display = '';
      }
    });
    document.getElementById('az-arte-ok').style.display = st.arte ? 'block' : 'none';
  }
  document.getElementById('az-arquivo').addEventListener('change', function(){
    var f = this.files && this.files[0];
    if(!f) return;
    var lr = new FileReader();
    lr.onload = function(){
      var im = new Image();
      im.onload = function(){
        var MAX = 1400, w = im.width, h = im.height;
        if(w > MAX || h > MAX){ var r = Math.min(MAX / w, MAX / h); w = Math.round(w * r); h = Math.round(h * r); }
        var cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        cv.getContext('2d').drawImage(im, 0, 0, w, h);
        st.arte = cv.toDataURL('image/jpeg', 0.85);
        aplicaArte();
      };
      im.src = lr.result;
    };
    lr.readAsDataURL(f);
  });
  document.getElementById('az-faixa-tx').addEventListener('input', function(){
    document.getElementById('pv-faixa-tx').textContent = this.value || 'A sua mensagem, com link para a bilheteria';
  });

  var pts = document.getElementById('az-pts');
  function pinta(){
    pts.innerHTML = '';
    for(var i = 1; i <= TOTAL; i++) pts.innerHTML += '<i class="' + (i <= passo ? 'on' : '') + '"></i>';
    pts.innerHTML += '<small>' + ROT[passo] + '</small>';
    document.querySelectorAll('.az-passo').forEach(function(p){
      p.classList.toggle('on', Number(p.dataset.p) === passo);
    });
    document.getElementById('az-volta').style.visibility = passo > 1 ? 'visible' : 'hidden';
    document.getElementById('az-vai').textContent = passo === TOTAL ? 'Enviar o pedido ✦' : 'Avançar →';
    document.getElementById('az-erro').style.display = 'none';
    if(passo === 2) pintaProva();
    if(passo === TOTAL) montaRevisao();
  }
  function v(id){ return document.getElementById(id).value.trim(); }
  function montaRevisao(){
    var f = fmt();
    var linhas = [
      ['Formato', (f ? f.nome + ' · ' + f.onde : '') + (st.cupom ? ' + bilhete do leitor' : '')],
      ['A arte', st.arte ? '<img src="' + st.arte + '" alt="a sua arte">' :
        (st.formato === 'faixa' ? '“' + (v('az-faixa-tx') || 'a combinar') + '”' : 'a combinar na conversa')],
      ['Estreia', v('az-inicio') || 'a combinar'],
      ['Duração', st.duracao || 'a combinar'],
      ['Quem', v('az-nome') + (v('az-empresa') ? ' · ' + v('az-empresa') : '')],
      ['Contato', v('az-whats') + ' · ' + v('az-email') + (v('az-insta') ? ' · ' + v('az-insta') : '')]
    ];
    if(v('az-msg')) linhas.push(['Observações', v('az-msg')]);
    document.getElementById('az-rev').innerHTML = linhas.map(function(l){
      return '<div><em>' + l[0] + '</em><span>' + (l[0] === 'A arte' ? l[1] : String(l[1]).replace(/</g, '&lt;')) + '</span></div>';
    }).join('');
  }
  function erro(msg){
    var e = document.getElementById('az-erro');
    e.textContent = msg; e.style.display = 'block';
  }
  function valida(){
    if(passo === 1 && !st.formato){ erro('Escolha um formato para seguir.'); return false; }
    if(passo === 4){
      if(!v('az-nome')){ erro('Diga o seu nome.'); return false; }
      if(!/.+@.+\\..+/.test(v('az-email'))){ erro('Confira o e-mail.'); return false; }
      if(v('az-whats').replace(/\\D/g, '').length < 10){ erro('Confira o WhatsApp (com DDD).'); return false; }
    }
    return true;
  }
  function envia(){
    var bt = document.getElementById('az-vai');
    bt.disabled = true; bt.textContent = 'Enviando…';
    var f = fmt();
    var msg = v('az-msg');
    if(st.formato === 'faixa' && v('az-faixa-tx')) msg = ('Linha da faixa: “' + v('az-faixa-tx') + '”' + (msg ? ' — ' + msg : ''));
    fetch(M.url + '/rest/v1/foyer_anuncios', {
      method: 'POST',
      headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        canal: f.canal, formato: st.formato, cupom: st.cupom,
        inicio: v('az-inicio'), duracao: st.duracao,
        nome: v('az-nome'), empresa: v('az-empresa'), email: v('az-email'),
        whatsapp: v('az-whats').replace(/\\D/g, ''), instagram: v('az-insta'),
        mensagem: msg, arte: st.arte || null
      })
    }).then(function(r){
      if(r.status !== 201) throw 0;
      document.querySelectorAll('.az-passo, .az-nav, .az-topo').forEach(function(x){ x.style.display = 'none'; });
      document.getElementById('az-fim').classList.add('on');
    }).catch(function(){
      bt.disabled = false; bt.textContent = 'Enviar o pedido ✦';
      erro('Não foi agora. Tente de novo em instantes ou escreva para programafoyer@gmail.com.');
    });
  }
  document.addEventListener('click', function(e){
    var bf = e.target.closest('.az-fcard');
    if(bf){
      st.formato = bf.dataset.f;
      if(st.formato !== 'pagina-inteira') st.cupom = false;
      document.querySelectorAll('.az-fcard').forEach(function(b){ b.classList.toggle('on', b === bf); });
      document.getElementById('az-cupom-bt').classList.toggle('on', st.cupom);
      pintaComo();
      return;
    }
    if(e.target.closest('#az-cupom-bt')){
      st.cupom = !st.cupom;
      document.getElementById('az-cupom-bt').classList.toggle('on', st.cupom);
      return;
    }
    var bd = e.target.closest('#az-duracao .az-op');
    if(bd){
      st.duracao = bd.dataset.d;
      document.querySelectorAll('#az-duracao .az-op').forEach(function(b){ b.classList.toggle('on', b === bd); });
      return;
    }
    if(e.target.closest('#az-vai')){
      if(!valida()) return;
      if(passo === TOTAL){ envia(); return; }
      passo++; pinta();
      return;
    }
    if(e.target.closest('#az-volta')){ if(passo > 1){ passo--; pinta(); } }
  });
  pinta();

  fetch(M.url + '/rest/v1/rpc/foyer_leitores_resumo', {
    method: 'POST',
    headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ chave: 'foyer-cx-metricas-terceiro-sinal-9427' })
  }).then(function(r){ if(!r.ok) throw 0; return r.json(); }).then(function(d){
    if(!d || !d.total || d.total < 10) return;
    function topo(o){ var ks = Object.keys(o || {}); return ks.length ? ks.sort(function(a, b){ return o[b] - o[a]; })[0] : null; }
    var tiles = [[d.total, 'assinantes']];
    var c1 = topo(d.por_cidade); if(c1) tiles.push([c1, 'cidade nº 1']);
    var c2 = topo(d.por_frequencia); if(c2) tiles.push([c2, 'vão ao vivo']);
    var c3 = topo(d.por_interesse); if(c3) tiles.push([c3, 'linguagem nº 1']);
    document.getElementById('mk-tiles').innerHTML = tiles.map(function(t){
      return '<div class="mk-tile"><b>' + t[0] + '</b><span>' + t[1] + '</span></div>';
    }).join('');
    document.getElementById('mk-leitor').classList.add('mostra');
  }).catch(function(){});
})();
</script>
'''
page('anuncie.html', 'Anuncie no FOYER', 'Anuncie no site e na revista do FOYER: veja a aplicação da sua arte antes de fechar e contrate em 5 passos, sem vendedor.', 'anuncie.html', anuncie_body)

# o endereço antigo segue vivo: midia-kit.html leva ao Anuncie no FOYER
with open(os.path.join(ROOT, 'midia-kit.html'), 'w') as _f:
    _f.write('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
             '<meta http-equiv="refresh" content="0; url=anuncie.html">'
             '<link rel="canonical" href="' + BASE + '/anuncie.html">'
             '<title>Anuncie no FOYER</title></head>'
             '<body><p>O mídia kit virou <a href="anuncie.html">Anuncie no FOYER</a>.</p></body></html>')
print('• anuncie.html + ponte do midia-kit')

descadastrar_body = band('Newsletter', 'Descadastrar', 'Sair da lista da Revista do FOYER') + '''
<main id="conteudo" class="wrap">
  <div class="legal">
    <div id="desc-estado"><p>Confirmando o seu descadastro…</p></div>
    <p style="margin-top:24px"><a href="index.html">Voltar para a capa do FOYER</a></p>
  </div>
</main>
<script>
(function(){
  var M = { url:'https://jcaqjlrzmrtzjyfbljxh.supabase.co', key:'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' };
  var t = new URLSearchParams(location.search).get('t');
  var el = document.getElementById('desc-estado');
  if(!t){ el.innerHTML = '<h2>Link incompleto</h2><p>Use o link de descadastro que veio no rodapé do e-mail.</p>'; return; }
  fetch(M.url + '/rest/v1/rpc/foyer_nl_descadastrar', {
    method:'POST', headers:{ 'apikey':M.key, 'Authorization':'Bearer '+M.key, 'Content-Type':'application/json' },
    body: JSON.stringify({ t: t })
  }).then(function(r){ return r.json(); }).then(function(d){
    if(d && d.ok){ el.innerHTML = '<h2>Pronto, você saiu da lista</h2><p>Não vamos mais enviar a Revista do FOYER para <b>' + (d.email||'') + '</b>. Sentiremos sua falta. Se mudar de ideia, é só assinar de novo no site.</p>'; }
    else { el.innerHTML = '<h2>Não encontramos esse cadastro</h2><p>Talvez você já tenha saído da lista. Se precisar, fale com a gente pela página de <a href="contato.html">contato</a>.</p>'; }
  }).catch(function(){ el.innerHTML = '<h2>Não deu agora</h2><p>Tente de novo em instantes, ou fale com a gente pela página de <a href="contato.html">contato</a>.</p>'; });
})();
</script>'''
page('descadastrar.html', 'Descadastrar — Revista do FOYER', 'Sair da lista de e-mails da Revista do FOYER.', 'descadastrar.html', descadastrar_body)

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
        'datePublished': p.get('isoFull') or p.get('iso', ''),
        'dateModified': (p.get('atualizado') or p.get('isoFull') or p.get('iso', ''))[:25],
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

for _asp, _aa in AUTORES.items():
    _amats = [_m for _m in MATERIAS if _m.get('author') == _aa['nome']]
    page('autor-' + _asp + '.html', _aa['nome'] + ' — FOYER',
         f"{_aa['nome']}, {_aa['cargo'].lower()} do FOYER. {_aa['cobre']}.",
         'sobre.html', autor_page(_asp, _aa, _amats), quiet=True)
print(f'• {len(AUTORES)} páginas de autor')

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
coxia_html = (head('Coxia — FOYER', 'Área restrita da redação do Foyer.')
              .replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>')
              .replace('href="manifest.webmanifest"', 'href="manifest-coxia.webmanifest"')
              .replace('rel="apple-touch-icon" href="assets/logo/pwa-192.png"',
                       'rel="apple-touch-icon" href="assets/logo/pwa-coxia-192.png"')
              + '\n' + coxia_body.replace('__TOTAL__', str(len(MATERIAS))) + '\n'
              + '<script src="assets/site.js"></script></body>\n</html>\n')
# a Coxia mora em /coxia/ (escopo próprio de aplicativo, separado do app do site);
# o <base href="../"> mantém todos os caminhos relativos funcionando
coxia_html = coxia_html.replace('<head>', '<head>\n<base href="../">', 1)
os.makedirs(os.path.join(ROOT, 'coxia'), exist_ok=True)
with open(os.path.join(ROOT, 'coxia/index.html'), 'w') as f:
    f.write(coxia_html)
# o endereço antigo segue vivo, redirecionando
with open(os.path.join(ROOT, 'coxia.html'), 'w') as f:
    f.write('<!DOCTYPE html>\n<html lang="pt-BR"><head><meta charset="UTF-8">'
            '<meta name="robots" content="noindex,nofollow">'
            '<meta http-equiv="refresh" content="0; url=coxia/">'
            '<script>location.replace("coxia/");</script>'
            '<title>Coxia — FOYER</title></head>'
            '<body><p><a href="coxia/">Entrar na Coxia</a></p></body></html>\n')
print('•', 'coxia/index.html', len(coxia_html)//1024, 'KB')

nf_body = band('Erro 404', 'Esta página saiu de cartaz', 'O endereço não existe — mas o espetáculo continua') + '''
<main id="conteudo" class="wrap" style="padding-bottom:40px">
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
                '<news:publication_date>' + (p.get('isoFull') or p.get('iso', _hoje_sm)) + '</news:publication_date>'
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
    f.write(f'User-agent: *\nAllow: /\nDisallow: /coxia.html\nDisallow: /coxia/\n\n'
            f'Sitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap-news.xml\n')
print(f'sitemap: {len(urls)} URLs · news: {len(_news)} matéria(s) recentes')

# ---------------------------------------------------------------- PONTES DO WIX
# Os endereços antigos (foyer.digital/post/<slug-com-acentos>) seguem indexados
# no Google e espalhados pela internet. Quando o domínio apontar para cá, cada
# um deles precisa levar o leitor (e o Google) à matéria nova: página-ponte com
# redirecionamento imediato + canonical, noindex na ponte.
import urllib.parse as _up
_n_pontes = 0
for _m in MATERIAS:
    _u = _m.get('url') or ''
    if '/post/' not in _u:
        continue
    _ws = _up.unquote(_u.split('/post/')[1]).strip('/')
    if not _ws or '/' in _ws:
        continue
    _alvo = f'{BASE}/post-{_m["slug"]}.html'
    _dirp = os.path.join(ROOT, 'post', _ws)
    os.makedirs(_dirp, exist_ok=True)
    with open(os.path.join(_dirp, 'index.html'), 'w') as _fp:
        _fp.write(f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{safe(_m['title'])} — FOYER</title>
<link rel="canonical" href="{_alvo}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={_alvo}">
<script>location.replace({_json.dumps(_alvo)});</script>
</head>
<body>
<p>Esta matéria mudou de endereço: <a href="{_alvo}">{safe(_m['title'])}</a></p>
</body>
</html>
''')
    _n_pontes += 1
print(f'• {_n_pontes} pontes dos endereços antigos do Wix em /post/')
print('pronto')
