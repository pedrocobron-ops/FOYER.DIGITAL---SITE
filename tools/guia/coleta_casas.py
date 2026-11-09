# Coletor de casas que publicam a lista de programas pela API aberta do
# WordPress, com as datas na API ou na página de cada programa. Fonte
# primária: o próprio lugar. Testado em 09/11/2026, robots.txt liberado em
# todos:
# - Blue Note São Paulo: /wp/v2/shows traz dia e hora, sets (hora, sala e
#   link da bilheteria) e "esgotado". Só API, sem abrir página.
# - Teatro Porto: /wp/v2/event lista; a página traz "De 18 de Abril a 13 de
#   Dezembro" (sem ano: deduzido), "HORÁRIOS: ...", ingresso e foto.
# - Instituto Tomie Ohtake: /wp/v2/to_exhibition lista (há versão em inglês
#   em /en/, ignorada); a página traz "de 13 de setembro a 08 de novembro de
#   2026", o prédio, a entrada (R$) e a classificação.
# - MIS, exposições: /wp/v2/mio_exhibition lista; a página traz
#   "Data|28.10 de 06.12.2026" e o horário de visitação.
# Páginas só são baixadas de novo quando o campo "modified" da API muda.
import sys
import os
import re
import json
import html

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, DADOS, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

MESES = {m: i + 1 for i, m in enumerate(['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
                                         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'])}


def _barras(s):
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>', '', s, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    return html.unescape(re.sub(r'\s*\|[\s|]*\|\s*', '|', t))


def _ano(mes, ref, ano=None):
    if ano:
        return int(ano)
    return ref.year + (1 if mes < ref.month - 6 else 0) - (1 if mes > ref.month + 6 else 0)


def _periodo_extenso(t, ref):
    """'de 13 de setembro a 08 de novembro de 2026' ou 'De 18 de Abril a 13 de Dezembro'."""
    m = re.search(r'\b[Dd]e (\d{1,2}) de ([A-Za-zç]+)(?: de (\d{4}))? a (\d{1,2}) de ([A-Za-zç]+)(?: de (\d{4}))?', t)
    if not m:
        return None, None, False
    d1, m1, a1, d2, m2, a2 = m.groups()
    m1, m2 = m1.lower(), m2.lower()
    if m1 not in MESES or m2 not in MESES:
        return None, None, False
    deduz = not a2
    y2 = _ano(MESES[m2], ref, a2)
    y1 = int(a1) if a1 else (y2 if MESES[m1] <= MESES[m2] else y2 - 1)
    return ('%04d-%02d-%02d' % (y1, MESES[m1], int(d1)), '%04d-%02d-%02d' % (y2, MESES[m2], int(d2)), deduz)


def _img_pagina(s):
    for m in re.finditer(r'<meta property="og:image" content="([^"]+)"', s):
        if not re.search(r'share\.png|logo', m.group(1), re.I):
            return m.group(1)
    m = re.search(r'src="(https://[^"]+/wp-content/uploads/[^"]+\.(?:jpe?g|png|webp))"', s)
    return m.group(1) if m and not re.search(r'logo|share', m.group(1), re.I) else None


class Casa:
    def __init__(self, web, fonte):
        self.web, self.fonte = web, fonte
        os.makedirs(os.path.join(DADOS, 'cache'), exist_ok=True)
        self.arq = os.path.join(DADOS, 'cache', fonte + '.json')
        self.cache = json.load(open(self.arq, encoding='utf-8')) if os.path.exists(self.arq) else {}
        self.novo = {}

    def lista(self, url, paginas=3):
        out = []
        for p in range(1, paginas + 1):
            lote = self.web.json(url + ('&' if '?' in url else '?') + 'per_page=100&orderby=modified&page=%d' % p)
            out += lote
            if len(lote) < 100:
                break
        return out

    def pagina(self, link, mod, ler):
        c = self.cache.get(link)
        if not c or c.get('modified') != mod:
            c = dict(ler(self.web.texto(link)), modified=mod, lido_em=agora_iso())
        self.novo[link] = c
        return c

    def salva(self):
        with open(self.arq, 'w', encoding='utf-8') as f:
            json.dump(self.novo, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')


def _lugar(fonte, nome, site, coletado, **extra):
    l = {'id': slug(nome), 'nome': campo(nome, 0), 'cidade': campo('São Paulo', 0), 'site': campo(site, 0),
         'origens': [{'fonte': fonte, 'url': site, 'coletado_em': coletado}]}
    for k, v in extra.items():
        if v:
            l[k] = campo(v, 0)
    return l


# ---------------------------------------------------------------- Blue Note
def bluenote(web):
    F, BASE, NOME = 'bluenote', 'https://bluenotesp.com', 'Blue Note São Paulo'
    hoje, coletado = agora().date().isoformat(), agora_iso()
    shows = Casa(web, F).lista(BASE + '/wp-json/wp/v2/shows?_fields=id,link,title,featured_media,acf')
    fotos = {}
    ids = sorted({s['featured_media'] for s in shows if s.get('featured_media')})
    for i in range(0, len(ids), 100):
        for m in web.json(BASE + '/wp-json/wp/v2/media?per_page=100&include=%s&_fields=id,source_url'
                          % ','.join(map(str, ids[i:i + 100]))):
            fotos[m['id']] = m.get('source_url')
    itens = []
    for s in shows:
        a = s.get('acf') or {}
        ini = (a.get('data_e_hora_de_inicio') or '')[:10]
        if not ini or ini < hoje:
            continue
        titulo = limpa(s['title']['rendered'])
        sub = (a.get('subtitulo') or '').strip()
        esg = bool(a.get('ingresso_esgotado'))
        sess = []
        for st in a.get('sets') or [{}]:
            h = (st.get('horario_do_set') or a['data_e_hora_de_inicio'][11:16])[:5]
            sess.append(sem_vazios({'lugar': slug(NOME), 'sala': campo(st.get('sala'), 0),
                                    'inicio': campo(ini + 'T' + h, 0), 'ingresso': campo(st.get('link_para_compra'), 0),
                                    'obs': campo('Ingressos esgotados (segundo o site)', 0) if esg else None}))
        itens.append(sem_vazios({
            'id': F + '-' + str(s['id']), 'area': campo('musica', 0),
            'titulo': campo(titulo + ((': ' + sub.title()) if sub else ''), 0),
            'link_fonte': campo(s['link'], 0),
            'imagem': campo(fotos.get(s.get('featured_media')), 0, credito='Divulgação / ' + NOME),
            'sessoes': sess, 'origens': [{'fonte': F, 'url': s['link'], 'coletado_em': coletado,
                                          'api': BASE + '/wp-json/wp/v2/shows'}]}))
    return F, itens, [_lugar(F, NOME, BASE, coletado)]


# -------------------------------------------------------------- Teatro Porto
def teatroporto(web):
    F, BASE, NOME = 'teatroporto', 'https://www.teatroportoseguro.com.br', 'Teatro Porto'
    ref, coletado = agora(), agora_iso()
    hoje = ref.date().isoformat()
    casa = Casa(web, F)
    corte = '%04d-%02d' % (ref.year - 1, ref.month)

    def ler(s):
        t = _barras(s)
        de, ate, deduz = _periodo_extenso(t, ref)
        hor = re.search(r'HOR[ÁA]RIOS?:\s*([^|]+)', t)
        ing = re.search(r'href="([^"]+)"[^>]*>\s*(?:<[^>]+>\s*)*Comprar Ingresso', s)
        desc = re.search(r'<meta name="description" content="([^"]*)"', s) or \
            re.search(r'<meta property="og:description" content="([^"]*)"', s)
        return {'de': de, 'ate': ate, 'deduz': deduz, 'horarios': hor.group(1).strip() if hor else None,
                'ingresso': html.unescape(ing.group(1)) if ing and ing.group(1).startswith('http') else None,
                'imagem': _img_pagina(s), 'descricao': html.unescape(desc.group(1)) if desc else None}
    itens = []
    for e in casa.lista(BASE + '/wp-json/wp/v2/event?_fields=id,link,title,modified'):
        if e['modified'][:7] < corte:
            continue
        c = casa.pagina(e['link'], e['modified'], ler)
        if not c.get('ate') or c['ate'] < hoje:
            continue
        obs = 'ano deduzido: o site escreve dia e mês' if c.get('deduz') else None
        itens.append(sem_vazios({
            'id': F + '-' + str(e['id']), 'area': campo('teatro', 0), 'titulo': campo(limpa(e['title']['rendered']), 0),
            'link_fonte': campo(e['link'], 0), 'trecho': campo(trecho(c.get('descricao') or ''), 0),
            'imagem': campo(c.get('imagem'), 0, credito='Divulgação / ' + NOME),
            'sessoes': [sem_vazios({'lugar': slug(NOME), 'estreia': campo(c['de'], 0, obs=obs) if c.get('de') else None,
                                    'ate': campo(c['ate'], 0, obs=obs), 'quando': campo(c.get('horarios'), 0),
                                    'ingresso': campo(c.get('ingresso'), 0)})],
            'origens': [{'fonte': F, 'url': e['link'], 'coletado_em': c['lido_em']}]}))
    casa.salva()
    return F, itens, [_lugar(F, NOME, BASE, coletado)]


# -------------------------------------------------------- Tomie Ohtake
def tomie(web):
    F, BASE, NOME = 'tomieohtake', 'https://www.institutotomieohtake.org.br', 'Instituto Tomie Ohtake'
    ref, coletado = agora(), agora_iso()
    hoje = ref.date().isoformat()
    casa = Casa(web, F)

    def ler(s):
        t = _barras(s)
        de, ate, deduz = _periodo_extenso(t, ref)
        onde = re.search(r'\|(Casa-ateliê[^|]+|Instituto Tomie Ohtake[^|]*)\|Exposição\|', t)
        ent = re.search(r'\|Entrada:\s*([^|]+)', t)
        cls = re.search(r'CLASSIFICAÇÃO INDICATIVA:\s*([^|]+)', t, re.I)
        func = re.search(r'FUNCIONAMENTO\|([^|]+)', t)
        return {'de': de, 'ate': ate, 'deduz': deduz, 'onde': onde.group(1).strip() if onde else None,
                'entrada': ent.group(1).strip() if ent else None, 'classificacao': cls.group(1).strip().title() if cls else None,
                'funcionamento': func.group(1).strip() if func else None, 'imagem': _img_pagina(s)}
    itens = []
    for e in casa.lista(BASE + '/wp-json/wp/v2/to_exhibition?_fields=id,link,title,modified'):
        if '/en/' in e['link'] or e['modified'][:4] < str(ref.year - 1):
            continue
        c = casa.pagina(e['link'], e['modified'], ler)
        if not c.get('ate') or c['ate'] < hoje:
            continue
        itens.append(sem_vazios({
            'id': F + '-' + str(e['id']), 'area': campo('exposicao', 0), 'titulo': campo(limpa(e['title']['rendered']), 0),
            'link_fonte': campo(e['link'], 0),
            'imagem': campo(c.get('imagem'), 0, credito='Divulgação / ' + NOME),
            'sessoes': [sem_vazios({'lugar': slug(NOME), 'sala': campo(c.get('onde'), 0),
                                    'estreia': campo(c.get('de'), 0), 'ate': campo(c['ate'], 0),
                                    'quando': campo(c.get('funcionamento'), 0), 'preco': campo(c.get('entrada'), 0),
                                    'classificacao': campo(c.get('classificacao'), 0)})],
            'origens': [{'fonte': F, 'url': e['link'], 'coletado_em': c['lido_em']}]}))
    casa.salva()
    return F, itens, [_lugar(F, NOME, BASE, coletado)]


# ------------------------------------------------------ MIS, exposições
def mis_expo(web):
    F, BASE, NOME = 'misexpo', 'https://www.mis-sp.org.br', 'MIS - Museu da Imagem e do Som'
    ref, coletado = agora(), agora_iso()
    hoje = ref.date().isoformat()
    casa = Casa(web, F)

    def ler(s):
        t = _barras(s)
        m = re.search(r'Data\|(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))? (?:de|a|até) (\d{1,2})\.(\d{1,2})\.(\d{4})', t)
        de = ate = None
        if m:
            d1, m1, a1, d2, m2, a2 = m.groups()
            y1 = int(a1) if a1 else (int(a2) if int(m1) <= int(m2) else int(a2) - 1)
            de, ate = '%04d-%02d-%02d' % (y1, int(m1), int(d1)), '%s-%02d-%02d' % (a2, int(m2), int(d2))
        hv = re.search(r'Horário de visitação\|((?:[^|]+\|){1,4})', t)
        horas = ' · '.join(x for x in hv.group(1).split('|') if x and re.search(r'\d', x)) if hv else None
        return {'de': de, 'ate': ate, 'horario': horas, 'imagem': _img_pagina(s)}
    itens = []
    for e in casa.lista(BASE + '/wp-json/wp/v2/mio_exhibition?_fields=id,link,title,modified,excerpt'):
        if e['modified'][:4] < str(ref.year - 1):
            continue
        c = casa.pagina(e['link'], e['modified'], ler)
        if not c.get('ate') or c['ate'] < hoje:
            continue
        itens.append(sem_vazios({
            'id': F + '-' + str(e['id']), 'area': campo('exposicao', 0), 'titulo': campo(limpa(e['title']['rendered']), 0),
            'link_fonte': campo(e['link'], 0), 'trecho': campo(trecho(limpa(e.get('excerpt', {}).get('rendered', ''))), 0),
            'imagem': campo(c.get('imagem'), 0, credito='Divulgação / MIS'),
            'sessoes': [sem_vazios({'lugar': slug(NOME), 'estreia': campo(c.get('de'), 0), 'ate': campo(c['ate'], 0),
                                    'quando': campo(c.get('horario'), 0)})],
            'origens': [{'fonte': F, 'url': e['link'], 'coletado_em': c['lido_em']}]}))
    casa.salva()
    return F, itens, [_lugar(F, NOME, BASE, coletado)]


CASAS = [bluenote, teatroporto, tomie, mis_expo]

if __name__ == '__main__':
    web = Educado()
    falhou = False
    for ler in CASAS:
        try:
            fonte, itens, lugares = ler(web)
            grava_bruto(fonte, True, itens, lugares)
            print('%s: %d programas' % (fonte, len(itens)))
        except Exception as e:
            nome = {bluenote: 'bluenote', teatroporto: 'teatroporto', tomie: 'tomieohtake', mis_expo: 'misexpo'}[ler]
            grava_bruto(nome, False, None, erro=e)
            print('%s FALHOU: %s' % (nome, e))
            falhou = True
    sys.exit(1 if falhou else 0)
