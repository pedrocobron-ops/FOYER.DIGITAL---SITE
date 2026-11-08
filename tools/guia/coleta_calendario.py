# Coletor dos sites que publicam a programação pelo calendário aberto do
# WordPress ("The Events Calendar": /wp-json/tribe/events/v1/events).
# É a fonte primária, o próprio lugar: vale mais que agenda agregadora.
#
# Testado em 08/11/2026:
# - Cinemateca Brasileira: completo (título, dia, hora, sala, categoria, link).
#   Preço vem vazio: o guia não fala de preço da Cinemateca.
# - IMS: a API não diz em qual sede (Paulista, Rio ou Poços) é cada evento e
#   o preço aparece como "R$1" em quase tudo (cara de campo não preenchido).
#   Pela regra de ouro, fica DE FORA até ter como confirmar a sede.
# Para ligar outro site que use o mesmo calendário: acrescente em SITES,
# depois de conferir robots.txt e se os campos fazem sentido.
import sys
import os
import re
import html
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

SITES = [
    {'fonte': 'cinemateca', 'nome': 'Cinemateca Brasileira', 'base': 'https://cinemateca.org.br',
     'area': 'cinema', 'cidade': 'São Paulo',
     # categoria do site -> área do guia
     'areas': {'Sessão': 'cinema', 'Infantil': 'cinema', 'Evento': 'cinema', 'Cursos e debates': 'cinema'}},
    # MIS (Museu da Imagem e do Som), testado em 08/11/2026: mesmo calendário,
    # com foto; sem preço e sem sala. Categoria quase sempre vazia: a área sai
    # de palavras do título, e o que não casar fica em "eventos".
    {'fonte': 'mis', 'nome': 'MIS - Museu da Imagem e do Som', 'base': 'https://www.mis-sp.org.br',
     'area': 'eventos', 'cidade': 'São Paulo', 'areas': {'Cursos': 'cursos'},
     'palavras': [(r'concerto|estéreo|show|orquestra', 'musica'),
                  (r'cinemat|cinema|sessão|mostra|festival|filme', 'cinema')]},
]
DIAS = 45      # janela: hoje até 45 dias à frente


def _img(e):
    im = e.get('image')
    if not isinstance(im, dict):
        return None
    tam = im.get('sizes') or {}
    for k in ('medium_large', 'large', 'medium'):
        if isinstance(tam.get(k), dict) and tam[k].get('url'):
            return tam[k]['url']
    return im.get('url')


def coleta(site):
    web = Educado()
    hoje = agora().date()
    fim = hoje + timedelta(days=DIAS)
    url = (site['base'] + '/wp-json/tribe/events/v1/events?per_page=50&status=publish'
           '&start_date=%s&end_date=%s' % (hoje.isoformat(), fim.isoformat()))
    eventos, paginas = [], 0
    while url and paginas < 40:
        d = web.json(url)
        eventos += d.get('events', [])
        url = d.get('next_rest_url')
        paginas += 1
    coletado = agora_iso()
    obras, lugares = {}, {}
    for e in eventos:
        if e.get('hide_from_listings') or e.get('status') != 'publish':
            continue
        titulo = limpa(e.get('title', ''))
        v = e.get('venue') if isinstance(e.get('venue'), dict) else {}
        sala = limpa(v.get('venue', '')) or None
        lid = slug(site['nome'])
        if lid not in lugares:
            lugares[lid] = {'id': lid, 'nome': campo(site['nome'], 0), 'cidade': campo(site['cidade'], 0),
                            'site': campo(site['base'], 0),
                            'origens': [{'fonte': site['fonte'], 'url': site['base'], 'coletado_em': coletado}]}
        cats = [c.get('name') for c in e.get('categories', [])]
        area = next((site['areas'][c] for c in cats if c in site['areas']), None)
        if not area:
            area = next((a for rx, a in site.get('palavras', []) if re.search(rx, titulo, re.I)), site['area'])
        # uma obra por título (o mesmo filme em vários dias vira várias sessões)
        chave = slug(titulo)
        o = obras.get(chave)
        if not o:
            o = obras[chave] = {
                'id': site['fonte'] + '-' + chave, 'area': campo(area, 0), 'titulo': campo(titulo, 0),
                'categoria': campo(', '.join(c for c in cats if c), 0),
                'link_fonte': campo(e.get('url'), 0),
                'trecho': campo(trecho(limpa(e.get('excerpt') or e.get('description') or '')), 0),
                # foto oficial publicada pelo próprio lugar: só o endereço (fica
                # no site deles), com crédito e link de volta na página
                'imagem': campo(_img(e), 0, credito='Divulgação / ' + site['nome']),
                'sessoes': [], 'origens': []}
        o['origens'].append({'fonte': site['fonte'], 'url': e.get('url'), 'coletado_em': coletado,
                             'api': e.get('rest_url')})
        oi = len(o['origens']) - 1
        custo = (e.get('cost') or '').strip()
        o['sessoes'].append(sem_vazios({
            'lugar': lid, 'sala': campo(sala, oi),
            'inicio': campo(e['start_date'].replace(' ', 'T')[:16], oi) if e.get('start_date') else None,
            'fim': campo(e['end_date'].replace(' ', 'T')[:16], oi)
            if e.get('end_date') and e.get('end_date') != e.get('start_date') else None,
            'preco': campo(custo, oi) if custo and custo not in ('R$1', '1') else None,
            'ingresso': campo(e.get('website'), oi), 'link': campo(e.get('url'), oi)}))
    for o in obras.values():
        o['sessoes'].sort(key=lambda s: s.get('inicio', {}).get('v', ''))
    return [sem_vazios(o) for o in obras.values()], list(lugares.values()), len(eventos)


if __name__ == '__main__':
    erro_geral = False
    for site in SITES:
        try:
            itens, lugares, n = coleta(site)
            grava_bruto(site['fonte'], True, itens, lugares,
                        nota='%d sessões nos próximos %d dias' % (n, DIAS))
            print('%s: %d obras, %d sessões' % (site['nome'], len(itens), n))
        except Exception as e:
            grava_bruto(site['fonte'], False, None, erro=e)
            print('%s FALHOU: %s' % (site['nome'], e))
            erro_geral = True
    sys.exit(1 if erro_geral else 0)
