# Coletor do Itaú Cultural (fonte primária: o próprio instituto).
#
# Testado em 08/11/2026: o site é montado em Next.js e as páginas públicas
# /agenda e /mostras-e-exposicoes/exposicoes já vêm com os dados da lista
# dentro delas (bloco __NEXT_DATA__, que o próprio navegador usa para
# desenhar a página): título, período, tags, foto oficial e crédito da foto.
# Lemos só essas duas páginas públicas. robots.txt: "Allow: /".
# A agenda traz período (de/até), não horário: o horário fica no link.
import sys
import os
import re
import json

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'itaucultural'
BASE = 'https://www.itaucultural.org.br'
NOME = 'Itaú Cultural'
PAGINAS = ['/agenda', '/mostras-e-exposicoes/exposicoes']
AREAS = [('exposição', 'exposicao'), ('ocupação', 'exposicao'), ('dança', 'danca'), ('infantil', 'infantil'),
         ('crianças', 'infantil'), ('teatro', 'teatro'), ('artes cênicas', 'teatro'), ('música', 'musica'),
         ('show', 'musica'), ('filmes', 'cinema'), ('cinema', 'cinema'), ('mostra de cinema', 'cinema'),
         ('literatura', 'literatura'), ('livro', 'literatura'), ('lançamento', 'literatura'),
         ('oficina', 'cursos'), ('mediação', 'cursos')]


def _dados(html_txt):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_txt, re.S)
    if not m:
        raise RuntimeError('página sem __NEXT_DATA__: o formato mudou')
    return json.loads(m.group(1))['props']['pageProps']


def coleta():
    web = Educado()
    hoje = agora().date().isoformat()
    coletado = agora_iso()
    lid = slug(NOME)
    lugar = {'id': lid, 'nome': campo(NOME, 0), 'cidade': campo('São Paulo', 0), 'site': campo(BASE, 0),
             'origens': [{'fonte': FONTE, 'url': BASE, 'coletado_em': coletado}]}
    itens, vistos = [], set()
    for p in PAGINAS:
        pp = _dados(web.texto(BASE + p))
        lista = pp.get('schedules') or pp.get('exhibitions') or []
        for e in lista:
            titulo = limpa(e.get('title', ''))
            fim = (e.get('endDate') or '')[:10]
            ini = (e.get('startDate') or e.get('initDate') or '')[:10]
            if not titulo or not fim or fim < hoje or e['slug'] in vistos:
                continue
            if re.match(r'(confira a (agenda|programação)|cancelad)', titulo, re.I):
                continue      # resumo do mês (repete os outros) ou cancelado
            if e.get('mainCategory', {}).get('slug', e.get('category', 'agenda-cultural')) not in ('agenda-cultural',):
                continue
            vistos.add(e['slug'])
            link = BASE + '/secoes/agenda/' + e['slug']
            tags = ' '.join(e.get('tags') or []).lower() + ' ' + titulo.lower()
            area = next((a for k, a in AREAS if k in tags), 'exposicao' if 'exposi' in p else 'eventos')
            cred = 'Divulgação / ' + NOME + ((': foto ' + e['rights']) if e.get('rights') else '')
            datas = 'De %s a %s' % ('/'.join(reversed(ini.split('-'))), '/'.join(reversed(fim.split('-')))) if ini and ini != fim \
                else 'Dia ' + '/'.join(reversed(fim.split('-')))
            itens.append(sem_vazios({
                'id': FONTE + '-' + str(e['id']), 'area': campo(area, 0), 'titulo': campo(titulo, 0),
                'categoria': campo(', '.join(e.get('tags') or []) or None, 0), 'link_fonte': campo(link, 0),
                'trecho': campo(trecho(limpa(e.get('shortDescription') or '')), 0),
                'imagem': campo(e.get('image'), 0, credito=cred),
                'sessoes': [sem_vazios({'lugar': lid, 'quando': campo(datas, 0),
                                        'estreia': campo(ini, 0) if ini and ini != fim else None,
                                        'ate': campo(fim, 0), 'site': campo(link, 0),
                                        'preco': campo('Gratuito', 0) if 'gratuit' in (e.get('shortDescription') or '').lower() else None})],
                'origens': [{'fonte': FONTE, 'url': BASE + p, 'coletado_em': coletado}]}))
    if not itens:
        raise RuntimeError('nenhum programa futuro lido')
    return itens, [lugar]


if __name__ == '__main__':
    try:
        itens, lugares = coleta()
        grava_bruto(FONTE, True, itens, lugares)
        print('Itaú Cultural: %d programas' % len(itens))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Itaú Cultural FALHOU:', e)
        sys.exit(1)
