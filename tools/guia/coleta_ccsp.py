# Coletor do Centro Cultural São Paulo (CCSP), da Prefeitura. Fonte primária.
#
# Testado em 08/11/2026: o site (centrocultural.sp.gov.br; o ccsp.com.br é de
# outra entidade) publica a agenda pela API aberta do WordPress:
#   /wp/v2/sessao  dia (data_inicio), hora, sala (local_id), preço, ingresso,
#                  recorrência ("diario" até recorrencia_fim, nas exposições)
#   /wp/v2/evento  o programa: resumo, foto, categoria
#   /wp/v2/local   nome das salas
# Sessão e evento se ligam pelo título (o site não guarda o vínculo na API).
# robots.txt liberado.
import sys
import os
import re
import html
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'ccsp'
BASE = 'https://centrocultural.sp.gov.br'
API = BASE + '/wp-json/wp/v2/'
NOME = 'Centro Cultural São Paulo'
AREAS = [('música', 'musica'), ('musica', 'musica'), ('show', 'musica'), ('piano', 'musica'), ('dança', 'danca'),
         ('teatro', 'teatro'), ('cinema', 'cinema'), ('filme', 'cinema'), ('exposiç', 'exposicao'),
         ('literatura', 'literatura'), ('biblioteca', 'literatura'), ('livro', 'literatura'),
         ('curso', 'cursos'), ('oficina', 'cursos'), ('infantil', 'infantil'), ('criança', 'infantil')]


def _todas(web, tipo, campos, paginas=6):
    out = []
    for p in range(1, paginas + 1):
        lote = web.json(API + '%s?per_page=100&orderby=modified&page=%d&_fields=%s' % (tipo, p, campos))
        out += lote
        if len(lote) < 100:
            break
    return out


def coleta():
    web = Educado()
    hoje = agora().date().isoformat()
    coletado = agora_iso()
    locais = {l['id']: limpa(l['title']['rendered']) for l in _todas(web, 'local', 'id,title')}
    cats = {c['id']: c['name'] for c in web.json(API + 'categoria_evento?per_page=100&_fields=id,name')}
    eventos = {}
    for e in _todas(web, 'evento', 'id,title,link,excerpt,featured_media,categoria_evento,meta'):
        eventos.setdefault(slug(limpa(e['title']['rendered'])), e)
    sessoes = _todas(web, 'sessao', 'id,title,meta,link')
    # fotos: um pedido só para todas as do lote
    ids = sorted({e['featured_media'] for e in eventos.values() if e.get('featured_media')})
    fotos = {}
    for i in range(0, len(ids), 100):
        for m in web.json(API + 'media?per_page=100&include=%s&_fields=id,source_url,media_details'
                          % ','.join(map(str, ids[i:i + 100]))):
            tam = (m.get('media_details') or {}).get('sizes') or {}
            fotos[m['id']] = (tam.get('medium_large') or tam.get('large') or {}).get('source_url') or m.get('source_url')
    lid = slug(NOME)
    lugar = {'id': lid, 'nome': campo(NOME, 0), 'cidade': campo('São Paulo', 0), 'site': campo(BASE, 0),
             'origens': [{'fonte': FONTE, 'url': BASE, 'coletado_em': coletado}]}
    obras = {}
    for s in sessoes:
        m = s.get('meta') or {}
        if not m.get('data_inicio'):
            continue
        dia = datetime.fromtimestamp(m['data_inicio'], timezone.utc).date().isoformat()
        fim = datetime.fromtimestamp(m['recorrencia_fim'], timezone.utc).date().isoformat() \
            if m.get('recorrencia_tipo') not in (None, '', 'nenhuma') and m.get('recorrencia_fim') else None
        if (fim or dia) < hoje:
            continue
        titulo = limpa(s['title']['rendered'])
        chave = slug(titulo)
        ev = eventos.get(chave)
        nomes_cat = ' '.join(cats.get(c, '') for c in (ev or {}).get('categoria_evento', [])).lower()
        area = next((a for k, a in AREAS if k in nomes_cat or k in titulo.lower()), 'eventos')
        link = ((ev or {}).get('meta') or {}).get('url_customizada_evento') or (ev or {}).get('link') or BASE + '/agenda/'
        o = obras.get(chave)
        if not o:
            o = obras[chave] = {
                'id': FONTE + '-' + chave, 'area': campo(area, 0), 'titulo': campo(titulo, 0),
                'categoria': campo(', '.join(cats.get(c, '') for c in (ev or {}).get('categoria_evento', [])) or None, 0),
                'link_fonte': campo(link, 0),
                'trecho': campo(trecho(limpa((ev or {}).get('excerpt', {}).get('rendered', ''))), 0),
                'imagem': campo(fotos.get((ev or {}).get('featured_media')), 0, credito='Divulgação / ' + NOME),
                'sessoes': [], 'origens': [{'fonte': FONTE, 'url': BASE + '/agenda/', 'coletado_em': coletado,
                                            'api': API + 'sessao'}]}
        hora = (m.get('horario_inicio') or '').strip()
        sala = locais.get(m.get('local_id'))
        base = {'lugar': lid, 'sala': campo(sala, 0),
                'preco': campo((m.get('valor_ingresso') or '').strip() or None, 0),
                'ingresso': campo((m.get('link_ingresso') or '').strip() or None, 0),
                'duracao_min': campo(m.get('duracao_minutos') or None, 0)}
        if fim:
            base.update({'estreia': campo(dia, 0), 'ate': campo(fim, 0),
                         'quando': campo('Todos os dias%s, de %s a %s' % (
                             (', ' + hora) if hora else '', '/'.join(reversed(dia.split('-'))),
                             '/'.join(reversed(fim.split('-')))), 0, obs='recorrência "diário" como o site registra')})
        else:
            base['inicio'] = campo(dia + ('T' + hora if re.match(r'^\d{1,2}:\d{2}$', hora) else ''), 0)
        o['sessoes'].append(sem_vazios(base))
    itens = [sem_vazios(o) for o in obras.values()]
    for o in itens:
        o['sessoes'].sort(key=lambda x: (x.get('inicio') or x.get('estreia') or {}).get('v', ''))
    if len(sessoes) < 10:
        raise RuntimeError('lista de sessões quase vazia (%d)' % len(sessoes))
    return itens, [lugar], len(sessoes)


if __name__ == '__main__':
    try:
        itens, lugares, n = coleta()
        grava_bruto(FONTE, True, itens, lugares, nota='%d sessões conferidas' % n)
        print('CCSP: %d programas futuros (%d sessões na API)' % (len(itens), n))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('CCSP FALHOU:', e)
        sys.exit(1)
