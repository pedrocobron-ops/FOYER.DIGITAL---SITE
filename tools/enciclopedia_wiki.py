#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bio e foto dos verbetes da Enciclopédia a partir da Wikipédia em português.

Lê import/enciclopedia.json (os verbetes) e grava import/enciclopedia-wiki.json:
  { "slug": {"titulo", "url", "descricao", "resumo", "foto", "fotoPagina", "quando"} }
  ou {"nao": true, "quando": ...} para quem não tem página (não pergunta de novo
  por 90 dias).

Cuidados (05/10/2026):
- Só aceita página que fale de gente das artes (ator, diretora, cantor, dramaturgo…)
  E que seja brasileira ou tenha presença forte no FOYER (5+ aparições). Isso
  derruba homônimos: "Pedro Amaral" na Wikipédia é um maestro português.
- Desambiguação nunca entra. Equipe do FOYER e colunistas têm bio própria
  (import/equipe.json e import/opiniao.json) e não passam por aqui.
- A foto é a miniatura da própria Wikipédia (Wikimedia Commons), com link
  para a página do arquivo, onde estão autor e licença.
- Pede em lotes de 20 nomes, com User-Agent identificado e pausa, como a
  Wikimedia pede.
Uso: python3 tools/enciclopedia_wiki.py [--todos] [--limite N]
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = 'FOYER-enciclopedia/1.0 (https://foyer.digital; contato@foyer.digital)'
ARTES = re.compile(r'\b(ator|atriz|atores|diretor|diretora|encenador|dramaturg|teatr|cantor|cantora|m[úu]sic|compositor|'
                   r'cineasta|humorista|comediante|bailarin|coreógraf|coreograf|escritor|poeta|jornalista|apresentador|'
                   r'produtor|cenógraf|figurinista|iluminador|roteirista|maestro|maestrina|pianista|instrumentista|'
                   r'performer|drag|artista|dublador|ilustrador|crítico|crítica|dançarin|circense|palhaç|ópera|opera|'
                   r'musical|novela|televis|cinema|filme|banda|rapper|dj\b|regente|arranjador|libretista|fotógraf)', re.I)
BRASIL = re.compile(r'brasileir|são paulo|rio de janeiro|brasil|paulistan|carioca|mineir|baian|gaúch|pernambucan|'
                    r'paranaense|catarinense|capixab|goian|cearense|paraiban|potiguar|sergipan|alagoan|maranhense|'
                    r'piauiense|amazonense|paraense|acrean|rondonien|roraimense|amapaense|tocantinense|mato-grossense|'
                    r'sul-mato-grossense|brasiliense', re.I)


def lote(nomes):
    q = urllib.parse.urlencode({
        'action': 'query', 'prop': 'extracts|pageimages|description|info', 'inprop': 'url',
        'exintro': 1, 'explaintext': 1, 'exsentences': 3, 'exlimit': 'max',
        'piprop': 'thumbnail|name', 'pithumbsize': 480,
        'titles': '|'.join(nomes), 'format': 'json', 'redirects': 1, 'maxlag': 5})
    req = urllib.request.Request('https://pt.wikipedia.org/w/api.php?' + q, headers={'User-Agent': UA})
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            if 'error' in d and d['error'].get('code') == 'maxlag':
                time.sleep(5 * (tentativa + 1)); continue
            return d
        except Exception as e:
            time.sleep(8 * (tentativa + 1))
    return None


def aceita(pg, aparicoes):
    if 'missing' in pg or 'invalid' in pg:
        return None
    desc = (pg.get('description') or '').lower()
    ext = (pg.get('extract') or '').strip()
    if 'desambigua' in desc or 'desambigua' in ext.lower()[:200] or 'pode referir-se' in ext.lower()[:200]:
        return None
    if not ARTES.search(desc + ' ' + ext):
        return None
    if not (BRASIL.search(desc + ' ' + ext) or aparicoes >= 5):
        return None
    foto = (pg.get('thumbnail') or {}).get('source', '')
    arq = pg.get('pageimage') or ''
    return {'titulo': pg.get('title', ''), 'url': pg.get('fullurl') or ('https://pt.wikipedia.org/wiki/' + urllib.parse.quote(pg.get('title', '').replace(' ', '_'))),
            'descricao': pg.get('description') or '', 'resumo': re.sub(r'\s+', ' ', ext)[:600],
            'foto': foto, 'fotoPagina': ('https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(arq)) if arq else ''}


def main():
    todos = '--todos' in sys.argv
    limite = int(sys.argv[sys.argv.index('--limite') + 1]) if '--limite' in sys.argv else 0
    enc = json.load(open(f'{ROOT}/import/enciclopedia.json'))['pessoas']
    arq = f'{ROOT}/import/enciclopedia-wiki.json'
    try:
        wiki = json.load(open(arq))
    except Exception:
        wiki = {}
    # equipe e colunistas: bio própria, não passam pela Wikipédia
    fora = set()
    for f, chave in (('equipe.json', 'usuarios'), ('opiniao.json', 'colunistas')):
        try:
            for u in json.load(open(f'{ROOT}/import/{f}')).get(chave, []):
                fora.add(re.sub(r'[^a-z0-9]+', '-', __import__('unicodedata').normalize('NFKD', u.get('nome', '')).encode('ascii', 'ignore').decode().lower()).strip('-'))
        except Exception:
            pass
    agora = datetime.now(timezone.utc)
    limite_data = (agora - timedelta(days=90)).isoformat()
    pend = []
    for sp, p in sorted(enc.items(), key=lambda x: -len(x[1]['aparicoes'])):
        if sp in fora:
            continue
        w = wiki.get(sp)
        if w and not todos and (w.get('quando', '') > limite_data or w.get('url')):
            continue
        pend.append((sp, p['nome'], len(p['aparicoes'])))
    if limite:
        pend = pend[:limite]
    print(f'{len(pend)} verbete(s) para consultar')
    achados = 0
    for i in range(0, len(pend), 20):
        grupo = pend[i:i + 20]
        d = lote([n for _, n, _ in grupo])
        if not d:
            print('  (sem resposta; segue)'); continue
        # normalização/redirect: título pedido -> título devolvido
        mapa = {}
        for x in (d.get('query', {}).get('normalized', []) + d.get('query', {}).get('redirects', [])):
            mapa[x['from']] = x['to']
        por_titulo = {pg.get('title'): pg for pg in d.get('query', {}).get('pages', {}).values()}
        for sp, nome, n in grupo:
            t = nome
            while t in mapa:
                t = mapa[t]
            pg = por_titulo.get(t)
            res = aceita(pg, n) if pg else None
            if res:
                res['quando'] = agora.isoformat(); wiki[sp] = res; achados += 1
            else:
                wiki[sp] = {'nao': True, 'quando': agora.isoformat()}
        json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
        print(f'  {min(i + 20, len(pend))}/{len(pend)} · com página: {achados}', flush=True)
        time.sleep(1.5)
    print(f'pronto: {achados} verbete(s) com bio da Wikipédia nesta rodada; total no arquivo: {sum(1 for v in wiki.values() if v.get("url"))}')


if __name__ == '__main__':
    main()
