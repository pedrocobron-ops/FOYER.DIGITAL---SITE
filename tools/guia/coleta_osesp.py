# Coletor da Osesp e da Sala São Paulo (fonte primária).
#
# Testado em 09/11/2026: osesp.art.br/osesp/pt/concertos-ingressos (concertos
# da Osesp) e salasaopaulo.art.br/salasp/pt/programacao-ingressos (tudo o que
# acontece na Sala São Paulo) trazem cartões com: data e hora (atributo
# datetime, em UTC), título, série, texto curto, local, duração, valor, link
# da bilheteria oficial e foto. Paginação por ?pageconcerts=N.
# robots.txt: "Allow: /" nos dois.
import sys
import os
import re
import html
import urllib.parse
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso, SP

LISTAS = [('https://osesp.art.br', '/osesp/pt/concertos-ingressos'),
          ('https://salasaopaulo.art.br', '/salasp/pt/programacao-ingressos')]
FONTE = 'osesp'


def coleta():
    web = Educado()
    hoje = agora().date().isoformat()
    coletado = agora_iso()
    obras, lugares = {}, {}
    for base, caminho in LISTAS:
        vistos_pag = set()
        for pag in range(1, 15):
            s = web.texto(base + caminho + ('?pageconcerts=%d' % pag if pag > 1 else ''))
            cards = re.split(r'<div class="card"', s)[1:]
            novos = 0
            for c in cards:
                ml = re.search(r'<h3[^>]*><a href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)
                mt = re.search(r'datetime="([^"]+)"', c)
                if not (ml and mt):
                    continue
                link = urllib.parse.urljoin(base, html.unescape(ml.group(1)))
                if link in vistos_pag:
                    continue
                vistos_pag.add(link)
                novos += 1
                quando = datetime.fromisoformat(mt.group(1).replace('Z', '+00:00')).astimezone(SP)
                if quando.date().isoformat() < hoje:
                    continue
                titulo = limpa(ml.group(2))
                serie = re.search(r'class="subheader[^"]*"[^>]*>(.*?)</div>', c, re.S)
                desc = re.search(r'</h3>(.*?)<div class="details"', c, re.S)
                local = re.search(r'Local:\s*(?:<a[^>]*>)?([^<]+)', c)
                dur = re.search(r'Duração:\s*<span[^>]*>\s*(\d+)', c)
                val = re.search(r'Valor:\s*<span[^>]*>([^<]+)</span>', c)
                taxa = re.search(r'(\+\s*\d+%\s*de taxa[^<]*)', c)
                ing = re.search(r'href="(https?://[^"]+)"[^>]*>\s*Comprar ingresso', c)
                img = re.search(r'<img src="/_image\?href=([^&"]+)', c)
                img = urllib.parse.unquote(html.unescape(img.group(1))) if img else None
                nome_local = limpa(local.group(1)) if local else None
                lid = slug(nome_local) if nome_local else None
                if lid and lid not in lugares:
                    lugares[lid] = {'id': lid, 'nome': campo(nome_local, 0), 'cidade': campo('São Paulo', 0),
                                    'origens': [{'fonte': FONTE, 'url': base + caminho, 'coletado_em': coletado}]}
                chave = re.sub(r'\?.*$', '', link)
                o = obras.get(chave)
                if not o:
                    o = obras[chave] = {
                        'id': FONTE + '-' + slug(chave.rsplit('/', 1)[-1] + '-' + titulo)[:60],
                        'area': campo('musica', 0), 'titulo': campo(titulo, 0),
                        'categoria': campo(limpa(serie.group(1)) if serie else None, 0),
                        'link_fonte': campo(link, 0), 'trecho': campo(trecho(limpa(desc.group(1))) if desc else None, 0),
                        'imagem': campo(img, 0, credito='Divulgação / Osesp - Sala São Paulo'),
                        'sessoes': [], 'origens': [{'fonte': FONTE, 'url': base + caminho, 'coletado_em': coletado}]}
                preco = limpa(val.group(1)) if val else None
                if preco and taxa:
                    preco += ' (' + limpa(taxa.group(1)) + ')'
                o['sessoes'].append(sem_vazios({
                    'lugar': lid, 'inicio': campo(quando.strftime('%Y-%m-%dT%H:%M'), 0),
                    'duracao_min': campo(int(dur.group(1)), 0) if dur else None,
                    'preco': campo(preco, 0), 'ingresso': campo(ing.group(1) if ing else None, 0)}))
            if not novos:
                break
    itens = [sem_vazios(o) for o in obras.values()]
    if not itens:
        raise RuntimeError('nenhum concerto lido: o formato da página pode ter mudado')
    return itens, list(lugares.values())


if __name__ == '__main__':
    try:
        itens, lugares = coleta()
        grava_bruto(FONTE, True, itens, lugares)
        print('Osesp / Sala São Paulo: %d programas, %d sessões' % (len(itens), sum(len(i['sessoes']) for i in itens)))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Osesp FALHOU:', e)
        sys.exit(1)
