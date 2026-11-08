# Coletor do Theatro Municipal de São Paulo (fonte primária: o próprio teatro).
#
# Testado em 08/11/2026: a lista de eventos sai da API aberta do WordPress
# (/wp-json/wp/v2/eventos, só título, link e data de alteração). Cada página
# de evento traz "Datas Disponíveis" (dia e hora), Local, Duração,
# Classificação, o botão "Compre seu ingresso" (bilheteria oficial) e a foto
# oficial (og:image). robots.txt liberado.
# Para não pesar no site, só baixa de novo a página que mudou desde a última
# coleta (cache pelo campo "modified" da API).
import sys
import os
import re
import json
import html
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, DADOS, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'municipal'
BASE = 'https://theatromunicipal.org.br'
MESES = {m: i + 1 for i, m in enumerate(['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
                                         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'])}
AREAS = [('ópera', 'opera'), ('opera', 'opera'), ('dança', 'danca'), ('balé', 'danca'), ('bale', 'danca'),
         ('concerto', 'musica'), ('recital', 'musica'), ('música', 'musica'), ('coral', 'musica'),
         ('exposição', 'exposicao'), ('teatro', 'teatro'), ('infantil', 'infantil'), ('criança', 'infantil')]


def _texto_barras(s):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    t = html.unescape(t)
    return re.sub(r'\|[\s|]*\|', '|', t)


def le_pagina(s):
    t = _texto_barras(s)
    r = {}
    m = re.search(r'Datas Disponíveis\|(.*?)(?:Sem datas adicionais|\|Ver Mapa|\|Compartilhar|$)', t, re.S)
    sess = []
    if m:
        for d, mes, ano, hora in re.findall(r'(\d{1,2}) de ([a-zç]+) de (\d{4})\|\s*(\d{1,2}:\d{2})?', m.group(1)):
            if mes in MESES:
                sess.append('%s-%02d-%02dT%s' % (ano, MESES[mes], int(d), hora or '00:00'))
    r['inicios'] = sorted(set(sess))
    for rot, k in (('Local', 'local'), ('Duração', 'duracao'), ('Classificação', 'classificacao')):
        mm = re.search(r'\|\s*' + rot + r':\s*([^|]+)', t)
        if mm:
            r[k] = mm.group(1).strip()
    mc = re.search(r'Descrição do Evento\|\s*([^|]{2,40})\|', t)
    r['categoria'] = mc.group(1).strip() if mc else None
    mi = re.search(r'href="([^"]+)"[^>]*>(?:\s|<[^>]+>)*Compre seu ingresso', s)
    r['ingresso'] = html.unescape(mi.group(1)) if mi else None
    mo = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    r['imagem'] = mo.group(1) if mo else None
    md = re.search(r'<meta property="og:description" content="([^"]*)"', s)
    r['descricao'] = html.unescape(md.group(1)) if md else None
    return r


def coleta():
    web = Educado()
    os.makedirs(os.path.join(DADOS, 'cache'), exist_ok=True)
    cache_arq = os.path.join(DADOS, 'cache', FONTE + '.json')
    cache = json.load(open(cache_arq, encoding='utf-8')) if os.path.exists(cache_arq) else {}
    lista = []
    # só eventos mexidos nos últimos 6 meses: os mais velhos não têm data futura
    corte = (agora() - timedelta(days=180)).strftime('%Y-%m-%dT%H:%M:%S')
    for pag in (1, 2, 3):
        lote = web.json(BASE + '/wp-json/wp/v2/eventos?per_page=100&orderby=modified&page=%d'
                        '&_fields=id,link,title,modified' % pag)
        lista += [e for e in lote if e['modified'] >= corte]
        if len(lote) < 100 or lote[-1]['modified'] < corte:
            break
    hoje = agora().date().isoformat()
    coletado = agora_iso()
    itens, lugares, novos = [], {}, {}
    print('%d eventos para conferir' % len(lista), flush=True)
    for e in lista:
        link, mod = e['link'], e['modified']
        c = cache.get(link)
        if not c or c.get('modified') != mod:
            c = dict(le_pagina(web.texto(link)), modified=mod, lido_em=coletado)
        novos[link] = c
        futuras = [i for i in c['inicios'] if i[:10] >= hoje]
        if not futuras:
            continue
        titulo = limpa(e['title']['rendered'])
        if re.match(r'(evento\s+)?cancelad[oa]', titulo, re.I):
            continue                 # o próprio teatro marcou como cancelado
        cat = (c.get('categoria') or '').lower()
        area = next((a for k, a in AREAS if k in cat or k in titulo.lower()), 'musica' if 'orquestra' in titulo.lower() else 'teatro')
        local = c.get('local') or None
        if local and local.strip().lower() in ('outros', 'outro', 'diversos'):
            local = None             # o site não diz onde: o guia também não
        lid = slug(local) if local else None
        if lid and lid not in lugares:
            lugares[lid] = {'id': lid, 'nome': campo(local, 0), 'cidade': campo('São Paulo', 0),
                            'origens': [{'fonte': FONTE, 'url': link, 'coletado_em': c['lido_em']}]}
        dur = re.match(r'(\d+)\s*min', c.get('duracao') or '')
        sessoes = [sem_vazios({'lugar': lid, 'inicio': campo(i[:16], 0), 'ingresso': campo(c.get('ingresso'), 0),
                               'duracao_min': campo(int(dur.group(1)), 0) if dur else None,
                               'classificacao': campo(c.get('classificacao'), 0)}) for i in futuras]
        itens.append(sem_vazios({
            'id': FONTE + '-' + str(e['id']), 'area': campo(area, 0), 'titulo': campo(titulo, 0),
            'categoria': campo(c.get('categoria'), 0), 'link_fonte': campo(link, 0),
            'trecho': campo(trecho(c.get('descricao') or ''), 0),
            'imagem': campo(c.get('imagem'), 0, credito='Divulgação / Theatro Municipal'),
            'sessoes': sessoes,
            'origens': [{'fonte': FONTE, 'url': link, 'coletado_em': c['lido_em']}]}))
    with open(cache_arq, 'w', encoding='utf-8') as f:
        json.dump(novos, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    if len(lista) < 10:
        raise RuntimeError('lista de eventos veio quase vazia (%d)' % len(lista))
    return itens, list(lugares.values()), len(lista)


if __name__ == '__main__':
    try:
        itens, lugares, n = coleta()
        grava_bruto(FONTE, True, itens, lugares, nota='%d páginas de evento conferidas' % n)
        print('Theatro Municipal: %d programas futuros (%d eventos na lista)' % (len(itens), n))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Theatro Municipal FALHOU:', e)
        sys.exit(1)
