# Coletor do Cine Belas Artes (cinebelasartes.com.br; o antigo
# petrabelasartes.com.br redireciona para lá). Fonte primária: o próprio
# cinema.
#
# Testado em 08/11/2026: a página inicial traz a "Programação Regular" da
# semana com um cartão por filme: título, sala, cartaz, sinopse curta,
# "gênero | classificação | duração | país | direção" e, por dia, os
# horários. robots.txt sem restrição de coleta (só os sinais de conteúdo
# padrão, sem "não" marcado). O ingresso é vendido na página do filme.
import sys
import os
import re
import html

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'belasartes'
URL = 'https://www.cinebelasartes.com.br/'
NOME = 'Cine Belas Artes'


def _ano(dia, mes, ref):
    ano = ref.year + (1 if mes < ref.month - 6 else 0)
    return '%04d-%02d-%02d' % (ano, mes, dia)


def coleta():
    web = Educado()
    s = web.texto(URL)
    ref = agora()
    hoje = ref.date().isoformat()
    coletado = agora_iso()
    lid = slug(NOME)
    lugar = {'id': lid, 'nome': campo(NOME, 0), 'cidade': campo('São Paulo', 0), 'site': campo(URL, 0),
             'origens': [{'fonte': FONTE, 'url': URL, 'coletado_em': coletado}]}
    obras = {}
    for card in re.split(r'<div class="c-movie-card">', s)[1:]:
        mt = re.search(r'c-movie-card__info-title">(.*?)</h3>', card, re.S)
        ml = re.search(r'href="(https://www\.cinebelasartes\.com\.br/[^"]+?)\s*"', card)
        if not (mt and ml):
            continue
        titulo, link = limpa(mt.group(1)), ml.group(1).strip().rstrip('/') + '/'
        sala = re.search(r'c-movie-card__info-room">(.*?)</span>', card, re.S)
        sala = limpa(sala.group(1)).split('|')[0].strip() if sala else None
        img = re.search(r'class="c-movie-card__thumb" src="([^"]+)"', card)
        sin = re.search(r'c-movie-card__info-synopsis">(.*?)</p>', card, re.S)
        comp = re.search(r'c-movie-card__info-comp">(.*?)</p>', card, re.S)
        partes = [p.strip() for p in limpa(comp.group(1)).split('|')] if comp else []
        genero = partes[0] if len(partes) > 0 and partes[0] else None
        clas = next((p for p in partes if re.match(r'^(\d{1,2} anos|Livre|L)$', p, re.I)), None)
        dur = next((int(p[:-3]) for p in partes if re.match(r'^\d+min$', p)), None)
        dirc = partes[4] if len(partes) > 4 and partes[4] else None
        pais = partes[3] if len(partes) > 3 and partes[3] else None
        bloco = card.split('c-movie__info-times-content--mobile-home', 1)
        if len(bloco) < 2:
            continue
        bloco = re.split(r'c-movie__info-times-content(?!--mobile-home)', bloco[1])[0]
        inicios = []
        for dm, corpo in re.findall(r'<span>\((\d{1,2}/\d{1,2})\)</span></h4>(.*?)(?=<h4|$)', bloco, re.S):
            d, m = map(int, dm.split('/'))
            dia = _ano(d, m, ref)
            for h, mi in re.findall(r'<span>\s*(\d{1,2})h(\d{2})\s*</span>', corpo):
                inicios.append('%sT%02d:%s' % (dia, int(h), mi))
        inicios = sorted({i for i in inicios if i[:10] >= hoje})
        if not inicios:
            continue
        o = obras.setdefault(link, {
            'id': FONTE + '-' + slug(link.rstrip('/').rsplit('/', 1)[-1]), 'area': campo('cinema', 0),
            'titulo': campo(titulo, 0), 'link_fonte': campo(link, 0),
            'categoria': campo(genero, 0), 'trecho': campo(trecho(limpa(sin.group(1))) if sin else None, 0),
            'ficha': campo(' | '.join(x for x in (('Direção: ' + dirc) if dirc else None, pais) if x), 0),
            'imagem': campo(img.group(1) if img else None, 0, credito='Cartaz / Divulgação / ' + NOME),
            'sessoes': [], 'origens': [{'fonte': FONTE, 'url': URL, 'coletado_em': coletado}]})
        for i in inicios:
            o['sessoes'].append(sem_vazios({
                'lugar': lid, 'sala': campo(sala, 0), 'inicio': campo(i, 0, obs='ano deduzido: o site escreve dia/mês'),
                'classificacao': campo(clas, 0), 'duracao_min': campo(dur, 0), 'ingresso': campo(link, 0)}))
    itens = [sem_vazios(o) for o in obras.values()]
    if not itens:
        raise RuntimeError('nenhum filme lido: o formato da página pode ter mudado')
    return itens, [lugar]


if __name__ == '__main__':
    try:
        itens, lugares = coleta()
        grava_bruto(FONTE, True, itens, lugares)
        print('Belas Artes: %d filmes, %d sessões' % (len(itens), sum(len(i['sessoes']) for i in itens)))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Belas Artes FALHOU:', e)
        sys.exit(1)
