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
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    WIKI_OK = set(json.load(open(f'{ROOT}/import/enciclopedia-regras.json')).get('wiki_ok', []))
except Exception:
    WIKI_OK = set()
UA = 'FOYER-enciclopedia/1.0 (https://foyer.digital; contato@foyer.digital)'
ARTES = re.compile(r'\b(ator|atriz|atores|diretor|diretora|encenador|dramaturg|teatr|cantor|cantora|m[úu]sic|compositor|'
                   r'cineasta|humorista|comediante|bailarin|coreógraf|coreograf|escritor|poeta|jornalista|apresentador|'
                   r'produtor|cenógraf|figurinista|iluminador|roteirista|maestro|maestrina|pianista|instrumentista|'
                   r'performer|drag|artista|dublador|ilustrador|crítico|crítica|dançarin|circense|palhaç|ópera|opera|'
                   r'musical|novela|televis|cinema|filme|banda|rapper|dj\b|regente|arranjador|libretista|fotógraf|'
                   r'fadista|transformista)', re.I)
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


# descrição curta que denuncia que a página NÃO é de uma pessoa (gênero
# musical, personagem, banda, festival…) — "Bossa nova" e "Homem de Lata"
# passaram na primeira rodada por falarem de música e de cinema (05/10/2026)
#   Auditoria de 10/10/2026: o plural escapava ("distribuidora de filmes" é
# Diamond Films) e faltavam franquia, distribuidora, editora e reality (Star
# Wars, American Idol). Do outro lado, PESSOA casava pedaço de palavra:
# "banda de cantores e compositores" (Barão Vermelho) passava por "cantor".
# Agora PESSOA só vale no singular e com a palavra inteira, porque quem
# descreve uma pessoa diz "cantor", e "cantores" descreve um grupo.
NAO_PESSOA = re.compile(r'\b(personage[mn]|g[êe]nero|estilo|movimento|banda|grupo|dupla|trio|coletivo|festival|'
                        r'[áa]lbum|can[çc][ãa]o|can[çc][õo]es|filme|pe[çc]a|telenovela|s[ée]rie|programa|empresa|teatro|pr[êe]mio|'
                        r'evento|escola|institui[çc][ãa]o|companhia|cia\.|bairro|cidade|munic[íi]pio|livro|romance|'
                        r'revista|jornal|emissora|canal|site|obra|espet[áa]culo|musical|musicais|minis[ée]rie|desenho|jogo|'
                        r'franquia|distribuidora|editora|gravadora|talent show|reality show|reality)s?\b', re.I)
PESSOA = re.compile(r'\b(?:ator|atriz|cantor|cantora|diretor|diretora|dramaturg[oa]|escritor|escritora|poeta|m[úu]sico|'
                    r'musicista|compositor|compositora|humorista|comediante|bailarin[oa]|core[óo]graf[oa]|apresentador|'
                    r'apresentadora|produtor|produtora|cineasta|jornalista|artista|performer|pianista|maestro|'
                    r'roteirista|dublador|dubladora|figurinista|cen[óo]graf[oa]|iluminador|iluminadora|encenador|encenadora|regente|'
                    r'arranjador|arranjadora|ilustrador|ilustradora|fot[óo]graf[oa]|dan[çc]arin[oa]|palha[çc][oa]|drag|'
                    r'intérprete|interprete|empres[áa]ri[oa]|'
                    r'fundador|fundadora|criador|criadora|professor|professora|pesquisador|pesquisadora|historiador|historiadora|'
                    r'crítico|crítica|'
                    r'autor|autora|libretista|ativista|educador|educadora|fadista|transformista|travesti|sambista|violonista|'
                    r'guitarrista|baterista|percussionista|saxofonista|flautista|violinista|cellista|tenor|soprano|bar[íi]tono|'
                    r'rapper|mc|dj|modelo|estilista|arquitet[oa]|pintor|pintora|escultor|escultora|cartunista|quadrinista|'
                    r'nascid[oa]|falecid[oa])\b', re.I)
_UM_DOS = re.compile(r'\bum[a]? d[oa]s((?:\s+[^\s,.;:]+){1,3})', re.I)


def _fala_de_gente(t):
    """A descrição fala de gente: 'atriz brasileira', ou 'um dos grandes
    diretores do teatro brasileiro' (o plural só vale depois de 'um dos')."""
    if PESSOA.search(t):
        return True
    for m in _UM_DOS.finditer(t):
        for w in m.group(1).split():
            for sing in (w[:-2] if w.endswith('es') else '', w[:-1] if w.endswith('s') else ''):
                if sing and PESSOA.fullmatch(sing):
                    return True
    return False


def _palavras_em_comum(a, b):
    """Há alguma palavra (3+ letras, sem acento, minúscula) em comum?"""
    def toks(t):
        t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
        return {w for w in re.findall(r'[a-z]{3,}', t)}
    return bool(toks(a) & toks(b))


def aceita(pg, aparicoes):
    if 'missing' in pg or 'invalid' in pg:
        return None
    desc = (pg.get('description') or '').lower()
    ext = (pg.get('extract') or '').strip()
    primeira = re.split(r'(?<=[.!?])\s', ext, 1)[0].lower() if ext else ''
    # a descrição curta (ou a primeira frase) diz o que a página é: se fala de
    # coisa e não de gente, fora
    if NAO_PESSOA.search(desc) and not _fala_de_gente(desc):
        return None
    if not desc and NAO_PESSOA.search(primeira) and not _fala_de_gente(primeira):
        return None
    if 'desambigua' in desc or 'desambigua' in ext.lower()[:200] or 'pode referir-se' in ext.lower()[:200]:
        return None
    if not ARTES.search(desc + ' ' + ext):
        return None
    if not (BRASIL.search(desc + ' ' + ext) or aparicoes >= 5):
        return None
    foto = (pg.get('thumbnail') or {}).get('source', '')
    # a API devolve o arquivo original quando ele é pequeno (thumbnail_unscaled),
    # e esse caminho é limitado por IP (429). Guarda sempre a miniatura de 500 px.
    foto = re.sub(r'^https?://upload\.wikimedia\.org/wikipedia/([a-z]+)/([0-9a-f])/([0-9a-f]{2})/([^/?]+)(\?.*)?$',
                  lambda m: f'https://thumb.wikimedia.org/wikipedia/{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{m.group(4)}/500px-{m.group(4)}' + ('.png' if m.group(4).lower().endswith('.svg') else ''),
                  foto)
    arq = pg.get('pageimage') or ''
    return {'titulo': pg.get('title', ''), 'url': pg.get('fullurl') or ('https://pt.wikipedia.org/wiki/' + urllib.parse.quote(pg.get('title', '').replace(' ', '_'))),
            'descricao': pg.get('description') or '', 'resumo': re.sub(r'\s+', ' ', ext)[:600],
            'foto': foto, 'fotoPagina': ('https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(arq)) if arq else ''}


def _foto_no_ar(url):
    """A miniatura ainda existe no Wikimedia Commons? Arquivo apagado ou
    renomeado responde 404 e deixava ícone de imagem quebrada no verbete, na
    vitrine e no compartilhamento (Myra Ruiz e Diego Martins, auditoria de
    10/10/2026). Só 404 e 410 derrubam a foto: limite de pedidos (429) ou
    rede fora do ar não dizem nada sobre o arquivo."""
    if not url:
        return True
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=20):
            return True
    except urllib.error.HTTPError as e:
        return e.code not in (404, 410)
    except Exception:
        return True


def revalidar():
    arq = f'{ROOT}/import/enciclopedia-wiki.json'
    wiki = json.load(open(arq))
    enc = json.load(open(f'{ROOT}/import/enciclopedia.json'))['pessoas']
    fora = 0
    for sp, v in list(wiki.items()):
        if not v.get('url'):
            continue
        pg = {'title': v.get('titulo', ''), 'description': v.get('descricao', ''), 'extract': v.get('resumo', ''),
              'thumbnail': {'source': v.get('foto', '')} if v.get('foto') else None, 'fullurl': v.get('url', '')}
        n = len(enc.get(sp, {}).get('aparicoes', [])) if sp in enc else 0
        if not aceita(pg, n):
            print('  fora:', sp, '|', v.get('descricao', '')[:60])
            wiki[sp] = {'nao': True, 'quando': v.get('quando', '')}
            fora += 1
    json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
    print(f'revalidação: {fora} verbete(s) perderam a página da Wikipédia')


def main():
    if '--revalidar' in sys.argv:
        return revalidar()
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
            # Duas guardas de precisão (06/10/2026), depois de Thales Bretas sair
            # com a página do Paulo Gustavo: (a) o título devolvido tem de ter ao
            # menos uma palavra em comum com o nome pedido (redirecionamento para
            # outra pessoa não passa); (b) a mesma página da Wikipédia não serve
            # para dois verbetes (o segundo é homônimo ou grafia alternativa, e
            # se for a mesma pessoa a junção é feita em 'apelidos', não aqui).
            if res and sp not in WIKI_OK and not _palavras_em_comum(nome, res.get('titulo', '')):
                print(f'  fora (título sem relação): {sp} -> {res.get("titulo")}')
                res = None
            if res and any(v.get('url') == res['url'] for k, v in wiki.items() if k != sp):
                print(f'  fora (página já é de outro verbete): {sp} -> {res.get("titulo")}')
                res = None
            if res and res.get('foto') and not _foto_no_ar(res['foto']):
                print(f'  foto fora do ar (fica sem foto): {sp} -> {res["foto"]}')
                res['foto'], res['fotoPagina'] = '', ''
            if res:
                res['quando'] = agora.isoformat(); wiki[sp] = res; achados += 1
            else:
                wiki[sp] = {'nao': True, 'quando': agora.isoformat()}
        json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
        print(f'  {min(i + 20, len(pend))}/{len(pend)} · com página: {achados}', flush=True)
        time.sleep(3)
    print(f'pronto: {achados} verbete(s) com bio da Wikipédia nesta rodada; total no arquivo: {sum(1 for v in wiki.values() if v.get("url"))}')


if __name__ == '__main__':
    main()
