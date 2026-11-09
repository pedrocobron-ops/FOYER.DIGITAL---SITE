# Coletor da Amigos da Arte (amigosdaarte.org.br), a organização social que
# administra equipamentos do Estado: Teatro Sérgio Cardoso e O Mundo do Circo
# SP (o Teatro Estadual de Araras fica fora: não é na capital). O domínio
# teatrosergiocardoso.org.br redireciona para lá. Fonte primária.
#
# Testado em 09/11/2026: a lista sai da API aberta (/wp/v2/agenda-equipamento,
# só título, link, data de alteração e foto); a página de cada programa traz
# as datas ("13/11 a 19/11/2026"), dias e horários, linguagem artística,
# companhia, duração, classificação, ingressos e o endereço. robots.txt
# liberado (só /wp-admin/ fechado). Páginas relidas só quando mudam.
import sys
import os
import re
import json
import html
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, DADOS, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'amigosdaarte'
BASE = 'https://amigosdaarte.org.br'
EQUIP = {'teatro-sergio-cardoso': 'Teatro Sérgio Cardoso', 'o-mundo-do-circo-sp': 'O Mundo do Circo SP'}
AREAS = [('exposi', 'exposicao'), ('circo', 'teatro'), ('dança', 'danca'), ('danca', 'danca'), ('música', 'musica'),
         ('show', 'musica'), ('concerto', 'musica'), ('infantil', 'infantil'), ('teatro', 'teatro'),
         ('oficina', 'cursos'), ('vivência', 'cursos'), ('curso', 'cursos'), ('literatura', 'literatura'),
         ('sarau', 'literatura'), ('cinema', 'cinema')]


def _barras(s):
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>', '', s, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    return html.unescape(re.sub(r'\s*\|[\s|]*\|\s*', '|', t))


def ler(s, ref):
    t = _barras(s)
    r = {}
    m = re.search(r'\|(\d{1,2})/(\d{1,2})(?:\|?/(\d{4}))?\|(?:a (\d{1,2})/(\d{1,2})\|?/(\d{4})\|)?', t)
    if m:
        d1, m1, a1, d2, m2, a2 = m.groups()
        if d2:
            y1 = int(a1) if a1 else (int(a2) if int(m1) <= int(m2) else int(a2) - 1)
            r['de'] = '%04d-%02d-%02d' % (y1, int(m1), int(d1))
            r['ate'] = '%s-%02d-%02d' % (a2, int(m2), int(d2))
        else:
            ano = int(a1) if a1 else ref.year + (1 if int(m1) < ref.month - 6 else 0)
            r['de'] = r['ate'] = '%04d-%02d-%02d' % (ano, int(m1), int(d1))
            r['deduz'] = not a1
        resto = t[m.end():].split('|')
        # depois das datas: título e a linha de dias/horários/ingresso
        if len(resto) > 1 and re.search(r'feira|sábado|domingo|\d{1,2}h', resto[1], re.I):
            r['quando'] = resto[1].strip()
    # sessões exatas, quando o site lista: '25/11/26 -|quarta-feira -|20:30|Título|Sala Nydia Licia'
    r['sessoes'] = sorted({('20%s-%s-%sT%s' % (a, mo, d, h.zfill(5)), sala.strip())
                           for d, mo, a, h, sala in re.findall(
                               r'(\d{2})/(\d{2})/(\d{2}) -\|[^|]+ -\|(\d{1,2}:\d{2})\|[^|]+\|([^|]+)', t)})
    mi = re.search(r'Ingressos:\|(.*?)\|(?:Programação|Localização|Duração|Classificação|Apresentação)\|', t)
    if mi:
        r['ingressos'] = re.sub(r'\s*\|\s*', ' ', mi.group(1)).replace(': ', ': ').strip()[:300]
    for rot, k in (('Linguagem artística', 'linguagem'), ('Companhia/Artista', 'companhia'), ('Duração', 'duracao'),
                   ('Classificação etária', 'classificacao'), ('Localização', 'endereco')):
        mm = re.search(rot + r':?\|([^|]+)', t)
        if mm:
            r[k] = mm.group(1).strip()
    me = re.search(r'equipamentos/([a-z0-9-]+)', s)
    r['equip'] = me.group(1) if me else None
    mi = re.search(r'href="(https?://[^"]*(?:sympla|bileto|ingress|ticket|eventim|uhuu)[^"]*)"', s)
    r['ingresso'] = html.unescape(mi.group(1)) if mi else None
    md = re.search(r'Informações\|([^|]{40,})', t)
    r['descricao'] = md.group(1).strip() if md else None
    return r


def coleta():
    web = Educado()
    ref = agora()
    hoje = ref.date().isoformat()
    coletado = agora_iso()
    os.makedirs(os.path.join(DADOS, 'cache'), exist_ok=True)
    arq = os.path.join(DADOS, 'cache', FONTE + '.json')
    cache = json.load(open(arq, encoding='utf-8')) if os.path.exists(arq) else {}
    corte = (ref - timedelta(days=150)).strftime('%Y-%m-%dT%H:%M:%S')
    lista = []
    for p in range(1, 8):
        lote = web.json(BASE + '/wp-json/wp/v2/agenda-equipamento?per_page=100&orderby=modified&page=%d'
                        '&_fields=id,link,title,modified,featured_media' % p)
        lista += [e for e in lote if e['modified'] >= corte]
        if len(lote) < 100 or lote[-1]['modified'] < corte:
            break
    print('%d programas para conferir' % len(lista), flush=True)
    novo, itens, lugares, fotos_ids = {}, [], {}, set()
    for e in lista:
        c = cache.get(e['link'])
        if not c or c.get('modified') != e['modified']:
            c = dict(ler(web.texto(e['link']), ref), modified=e['modified'], lido_em=coletado)
        novo[e['link']] = c
        if not c.get('ate') or c['ate'] < hoje or c.get('equip') not in EQUIP:
            continue
        if c.get('endereco') and 'São Paulo' not in c['endereco']:
            continue
        nome = EQUIP[c['equip']]
        lid = slug(nome)
        if lid not in lugares:
            lugares[lid] = {'id': lid, 'nome': campo(nome, 0), 'cidade': campo('São Paulo', 0),
                            'endereco_texto': campo(c.get('endereco'), 0),
                            'site': campo(BASE + '/equipamentos/' + c['equip'] + '/', 0),
                            'origens': [{'fonte': FONTE, 'url': e['link'], 'coletado_em': c['lido_em']}]}
        ling = (c.get('linguagem') or '') + ' ' + limpa(e['title']['rendered'])
        area = next((a for k, a in AREAS if k in ling.lower()), 'teatro' if c['equip'] == 'teatro-sergio-cardoso' else 'eventos')
        dur = re.match(r'(\d+)\s*min', c.get('duracao') or '')
        obs = 'ano deduzido: o site escreve dia e mês' if c.get('deduz') else None
        fotos_ids.add(e.get('featured_media'))
        itens.append(sem_vazios({
            'id': FONTE + '-' + str(e['id']), 'area': campo(area, 0), 'titulo': campo(limpa(e['title']['rendered']), 0),
            'categoria': campo(c.get('linguagem'), 0), 'link_fonte': campo(e['link'], 0),
            'ficha': campo(('Companhia/artista: ' + c['companhia']) if c.get('companhia') else None, 0),
            'trecho': campo(trecho(c.get('descricao') or ''), 0), '_foto': e.get('featured_media'),
            'sessoes': [sem_vazios({
                'lugar': lid, 'inicio': campo(i, 0), 'sala': campo(None if re.match(r'\d', sala) else sala, 0), 'preco': campo(c.get('ingressos'), 0),
                'classificacao': campo(c.get('classificacao'), 0),
                'duracao_min': campo(int(dur.group(1)), 0) if dur else None,
                'ingresso': campo(c.get('ingresso'), 0)}) for i, sala in c.get('sessoes', []) if i[:10] >= hoje] or [sem_vazios({
                'lugar': lid, 'estreia': campo(c['de'], 0, obs=obs) if c['de'] != c['ate'] else None,
                'ate': campo(c['ate'], 0, obs=obs), 'datas': campo([c['de']], 0, obs=obs) if c['de'] == c['ate'] else None,
                'quando': campo(c.get('quando'), 0), 'preco': campo(c.get('ingressos'), 0),
                'classificacao': campo(c.get('classificacao'), 0),
                'duracao_min': campo(int(dur.group(1)), 0) if dur else None,
                'ingresso': campo(c.get('ingresso'), 0)})],
            'origens': [{'fonte': FONTE, 'url': e['link'], 'coletado_em': c['lido_em']}]}))
    ids = sorted(i for i in fotos_ids if i)
    fotos = {}
    for i in range(0, len(ids), 100):
        for m in web.json(BASE + '/wp-json/wp/v2/media?per_page=100&include=%s&_fields=id,source_url,media_details'
                          % ','.join(map(str, ids[i:i + 100]))):
            tam = (m.get('media_details') or {}).get('sizes') or {}
            fotos[m['id']] = (tam.get('medium_large') or tam.get('large') or {}).get('source_url') or m.get('source_url')
    for it in itens:
        f = fotos.get(it.pop('_foto', None))
        if f:
            it['imagem'] = campo(f, 0, credito='Divulgação / Amigos da Arte')
    with open(arq, 'w', encoding='utf-8') as f:
        json.dump(novo, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    if len(lista) < 5:
        raise RuntimeError('lista quase vazia (%d)' % len(lista))
    return itens, list(lugares.values())


if __name__ == '__main__':
    try:
        itens, lugares = coleta()
        grava_bruto(FONTE, True, itens, lugares)
        print('Amigos da Arte (Sérgio Cardoso, Mundo do Circo): %d programas' % len(itens))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Amigos da Arte FALHOU:', e)
        sys.exit(1)
