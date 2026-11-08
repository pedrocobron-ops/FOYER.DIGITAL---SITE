# Coletor de exposições dos museus (fonte primária: o próprio museu).
#
# Cada museu tem um site diferente, então cada um tem o seu leitor aqui.
# Testado em 08/11/2026:
# - MASP: masp.org.br/exposicoes, blocos "Em Cartaz" e "Em Breve" com
#   título, período (dd.mm.aaaa — dd.mm.aaaa), foto oficial e legenda/crédito.
# - MAM São Paulo: mam.org.br/exposicoes/em-cartaz/ e /futuras/, cartões com
#   título, período ("12 set 26 - 24 jan 27") e foto.
# Fora por enquanto: Pinacoteca (página de exposições deu 404), Japan House
# (403 para robôs), Itaú Cultural (página montada por JavaScript), CCBB
# (formato a estudar), Museu da Língua Portuguesa (API só com exposições de
# 2021). robots.txt de MASP e MAM liberado.
import sys
import os
import re
import html

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, grava_bruto, agora, agora_iso

MES = {m: i + 1 for i, m in enumerate(['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'])}


def _masp(web):
    s = web.texto('https://masp.org.br/exposicoes')
    out = []
    for sec in ('em-cartaz', 'em-breve'):
        i = s.find('id="%s"' % sec)
        if i < 0:
            continue
        j = s.find('<h2 class="title">', i + 50)
        bloco = s[i:j if j > 0 else len(s)]
        for b in bloco.split('box-image-text-toggle')[1:]:
            mt = re.search(r'<h3 class="title">(.*?)</h3>', b, re.S)
            md = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})\s*[—–-]\s*(\d{1,2})\.(\d{1,2})\.(\d{4})', b)
            ml = re.search(r'href="(https://masp\.org\.br/exposicoes/[^"]+)"', b)
            if not (mt and md and ml):
                continue
            d1, m1, a1, d2, m2, a2 = map(int, md.groups())
            mi = re.search(r'background-image:\s*url\(([^)]+)\)', b)
            mc = re.search(r'class="subtitle-image">(.*?)</span>', b, re.S)
            cat = re.search(r'<h6 class="category">(.*?)</h6>', b)
            out.append({'titulo': limpa(mt.group(1)), 'link': ml.group(1),
                        'de': '%04d-%02d-%02d' % (a1, m1, d1), 'ate': '%04d-%02d-%02d' % (a2, m2, d2),
                        'imagem': mi.group(1).strip('\'"') if mi else None,
                        'credito': limpa(mc.group(1)) if mc else None,
                        'categoria': limpa(cat.group(1)) if cat else None})
    return out


def _mam(web):
    out = []
    for pag in ('em-cartaz', 'futuras'):
        s = web.texto('https://mam.org.br/exposicoes/%s/' % pag)
        for b in re.split(r'<div class="card[ "]', s)[1:]:
            ml = re.search(r'href="(https://mam\.org\.br/exposicao/[^"]+)"', b)
            mt = re.search(r'<h2 class="title">(.*?)</h2>', b, re.S)
            md = re.search(r'(\d{1,2})\s+([a-zç]{3})\s+(\d{2})\s*</span>\s*<span>\s*-\s*</span>\s*<span>\s*(\d{1,2})\s+([a-zç]{3})\s+(\d{2})', b)
            if not (ml and mt and md):
                continue
            d1, m1, a1, d2, m2, a2 = md.groups()
            if m1 not in MES or m2 not in MES:
                continue
            mi = re.search(r'class="image-area">\s*<a[^>]*>\s*<img src="([^"]+)"', b)
            if mi and re.search(r'logo', mi.group(1), re.I):
                mi = None           # régua de patrocinadores não é foto da exposição
            out.append({'titulo': limpa(mt.group(1)), 'link': ml.group(1),
                        'de': '20%s-%02d-%02d' % (a1, MES[m1], int(d1)),
                        'ate': '20%s-%02d-%02d' % (a2, MES[m2], int(d2)),
                        'imagem': mi.group(1) if mi else None, 'credito': None, 'categoria': 'Exposição'})
    return out


MUSEUS = [
    {'fonte': 'masp', 'nome': 'MASP', 'site': 'https://masp.org.br', 'ler': _masp},
    {'fonte': 'mam', 'nome': 'MAM São Paulo', 'site': 'https://mam.org.br', 'ler': _mam},
]


def coleta(m, web):
    hoje = agora().date().isoformat()
    coletado = agora_iso()
    lid = slug(m['nome'])
    lugar = {'id': lid, 'nome': campo(m['nome'], 0), 'cidade': campo('São Paulo', 0), 'site': campo(m['site'], 0),
             'origens': [{'fonte': m['fonte'], 'url': m['site'], 'coletado_em': coletado}]}
    itens, vistos = [], set()
    for x in m['ler'](web):
        if x['ate'] < hoje or x['link'] in vistos:
            continue
        vistos.add(x['link'])
        cred = 'Divulgação / ' + m['nome'] + ((': ' + x['credito'][:160]) if x.get('credito') else '')
        itens.append(sem_vazios({
            'id': m['fonte'] + '-' + slug(x['link'].rstrip('/').rsplit('/', 1)[-1]),
            'area': campo('exposicao', 0), 'titulo': campo(x['titulo'], 0),
            'categoria': campo(x.get('categoria'), 0), 'link_fonte': campo(x['link'], 0),
            'imagem': campo(x.get('imagem'), 0, credito=cred),
            'sessoes': [sem_vazios({'lugar': lid, 'estreia': campo(x['de'], 0), 'ate': campo(x['ate'], 0),
                                    'site': campo(x['link'], 0)})],
            'origens': [{'fonte': m['fonte'], 'url': x['link'], 'coletado_em': coletado}]}))
    if not itens:
        raise RuntimeError('nenhuma exposição lida: o formato da página pode ter mudado')
    return itens, [lugar]


if __name__ == '__main__':
    web = Educado()
    falhou = False
    for m in MUSEUS:
        try:
            itens, lugares = coleta(m, web)
            grava_bruto(m['fonte'], True, itens, lugares)
            print('%s: %d exposições' % (m['nome'], len(itens)))
        except Exception as e:
            grava_bruto(m['fonte'], False, None, erro=e)
            print('%s FALHOU: %s' % (m['nome'], e))
            falhou = True
    sys.exit(1 if falhou else 0)
