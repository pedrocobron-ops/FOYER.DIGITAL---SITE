# Coletor do Guia OFF (https://guiaoff.com.br/guia/), fonte principal de teatro.
#
# Testado em 08/11/2026: a página /guia/ traz a agenda teatral aberta do mês,
# em HTML organizado (um <article class="guia-item"> por espetáculo, com
# título, texto curto, ficha técnica e "Serviços": lugar, endereço, dias,
# horário, preço, duração, classificação, temporada e link).
# robots.txt: liberado para todos, com "Content-Signal: search=yes,
# ai-train=no, use=reference". Por isso: só listagem com link (como um buscador
# faz), trecho curto, nada de treinar ou resumir com IA. Rodada uma vez por dia.
import re
import sys
import os
import html

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, campo, sem_vazios, slug, limpa, trecho, grava_bruto, agora, agora_iso

FONTE = 'guiaoff'
URL = 'https://guiaoff.com.br/guia/'

AREA = {'teatro': 'teatro', 'dança': 'danca', 'danca': 'danca', 'offinho': 'infantil', 'eventos': 'eventos'}
BILHETERIAS = ('sympla.com.br', 'bileto.sympla', 'uhuu.com', 'ingressorapido', 'eventim', 'ticket360',
               'ticketsforfun', 'bilheteriaexpress', 'ingresse', 'sescsp.org.br', 'shotgun', 'byinti',
               'tudus', 'totalacesso', 'ingressodigital', 'guicheweb', 'compreingressos', 'theatromunicipal')


def _ano_para(dia, mes, ref):
    """O Guia OFF escreve datas sem ano (dd/mm), dentro da edição do mês.
    O ano é o da coleta, ou o seguinte quando o mês já ficou bem para trás
    (dezembro coletado mostrando janeiro). Marcado como deduzido no campo."""
    ano = ref.year
    if mes < ref.month - 6:
        ano += 1
    elif mes > ref.month + 6:
        ano -= 1
    try:
        return '%04d-%02d-%02d' % (ano, mes, dia)
    except ValueError:
        return None


def _datas_explicitas(txt, ref):
    """'Dias 07 e 14/11', 'Dia 26/11', 'Dias 21, 20h; 22/11, 19h' -> datas ISO."""
    datas = []
    for trecho_dia in re.findall(r'\bDias?\s+([^.;]*?(?:\d{1,2}/\d{1,2})[^.]*)', txt):
        nums = re.findall(r'(\d{1,2})(?:/(\d{1,2}))?(?!h|\d|min)', re.sub(r'\d{1,2}h\d{0,2}', ' ', trecho_dia))
        pend = []
        for d, m in nums:
            pend.append(int(d))
            if m:
                for dd in pend:
                    iso = _ano_para(dd, int(m), ref)
                    if iso:
                        datas.append(iso)
                pend = []
    return sorted(set(datas))


def _lugar(linha):
    """'<strong>Nome</strong> / Sala – Endereço, 123. Bairro. T.1234.5678.'"""
    m = re.search(r'<strong>(.*?)</strong>(.*)', linha, re.S)
    if not m:
        return None
    nome = limpa(m.group(1))
    resto = re.sub(r'\s+\.', '.', limpa(m.group(2))).strip()
    sala = None
    partes = re.split(r'\s+[–-]\s+', resto, maxsplit=1)
    if len(partes) == 2:
        antes, endereco_txt = partes
        sala = antes.strip(' /') or None
    else:
        endereco_txt = resto.lstrip(' –-')
    tel = None
    mt = re.search(r'\bT\.\s*([\d][\d.\s/-]{6,})', endereco_txt)
    if mt:
        tel = mt.group(1).strip(' .')
        endereco_txt = endereco_txt[:mt.start()].strip()
    endereco = bairro = None
    me = re.match(r'(.*?,\s*(?:\d+[A-Za-z]?|s/n[º°]?)(?:\s*[-–]\s*[^.]+?)?)\.\s*(.*?)\.?\s*$', endereco_txt)
    if me:
        endereco, bairro = me.group(1).strip(), me.group(2).strip() or None
    return {'nome': nome, 'sala': sala, 'endereco': endereco, 'bairro': bairro, 'telefone': tel,
            'endereco_texto': endereco_txt.strip(' .') or None}


def _tokens(linha):
    """Divide 'Sábado, 20h. R$50. 60min.' nos pontos, sem quebrar parênteses
    nem abreviações de uma letra."""
    toks, atual, prof = [], '', 0
    for i, ch in enumerate(linha):
        prof += (ch == '(') - (ch == ')')
        if ch == '.' and prof <= 0 and (i + 1 == len(linha) or linha[i + 1] == ' ') \
                and not re.search(r'(^|\s)\w$', atual):
            toks.append(atual.strip()); atual = ''
        else:
            atual += ch
    toks.append(atual.strip())
    return [t for t in toks if t]


def _dm(tok):
    return [(int(d), int(m)) for d, m in re.findall(r'(\d{1,2})/(\d{1,2})', tok)]


def _servico(bloco, ref):
    """Um bloco 'Serviços' pode ter mais de um lugar: cada <strong> abre um."""
    linhas = [l.strip() for l in re.split(r'<br\s*/?>|</p>\s*<p>', bloco) if limpa(l)]
    cidade = None
    sessoes, atual = [], None
    for l in linhas:
        txt = limpa(l)
        if '<strong>' in l:
            atual = {'lugar': _lugar(l), 'linhas': [], 'links': []}
            if cidade:
                atual['cidade'] = cidade
            sessoes.append(atual)
            continue
        links = re.findall(r'href="([^"]+)"', l)
        if atual is None:
            cidade = txt            # "Rio de Janeiro" antes do lugar (fora de SP)
            continue
        if links:
            atual['links'] += [html.unescape(u).strip() for u in links]
        else:
            atual['linhas'].append(txt)
    saida = []
    for s in sessoes:
        quando, preco, dur, clas, ate, estreia, obs = [], None, None, None, None, None, []
        for linha in s['linhas']:
            for tok in _tokens(linha):
                mp = re.match(r'^De\s+(\d{1,2})(?:/(\d{1,2}))?\s+a\s+(\d{1,2})/(\d{1,2})$', tok)
                if tok.startswith('http'):
                    s['links'].append(tok)
                elif re.match(r'^(Até|Ate)\s+\d{1,2}/\d{1,2}', tok):
                    d, m = _dm(tok)[0]
                    ate = _ano_para(d, m, ref)
                elif re.match(r'^(Re)?[Ee]streia\s+\d{1,2}/\d{1,2}', tok):
                    d, m = _dm(tok)[0]
                    estreia = _ano_para(d, m, ref)
                elif mp:
                    d1, m1, d2, m2 = mp.groups()
                    estreia = _ano_para(int(d1), int(m1 or m2), ref)
                    ate = _ano_para(int(d2), int(m2), ref)
                elif re.search(r'R\$|^Gratuit|^Grátis|^Pague|^Ingresso', tok, re.I):
                    preco = tok
                elif re.match(r'^\d+\s*(min|mn|minutos)$', tok):
                    dur = int(re.match(r'\d+', tok).group(0))
                elif re.match(r'^(\d{1,2}\s*anos|Livre)\b', tok, re.I):
                    clas = tok
                elif re.search(r'\d{1,2}h|segunda|terça|quarta|quinta|sexta|sábado|domingo|\bDias?\b', tok, re.I):
                    quando.append(tok)
                else:
                    obs.append(tok)
        texto_quando = '. '.join(quando)
        datas = _datas_explicitas(texto_quando, ref)
        ingresso = next((u for u in s['links'] if any(b in u for b in BILHETERIAS)), None)
        site = next((u for u in s['links'] if u != ingresso), None)
        saida.append({'lugar': s['lugar'], 'cidade': s.get('cidade'), 'quando': texto_quando or None,
                      'datas': datas, 'estreia': estreia, 'ate': ate, 'preco': preco, 'duracao_min': dur,
                      'classificacao': clas, 'ingresso': ingresso, 'site': site,
                      'obs': '. '.join(obs) or None,
                      'texto': '\n'.join(s['linhas'])})
    return saida


def coleta():
    web = Educado()
    pagina = web.texto(URL)
    ref = agora()
    coletado = agora_iso()
    itens, lugares, fora = [], {}, 0
    # cada categoria é um <div class="guia-categoria"> com <h3 class="guia-categoria-titulo">
    for cat in re.split(r'<div\s+class="guia-categoria">', pagina)[1:]:
        mt = re.search(r'guia-categoria-titulo">\s*([^<]+?)\s*<', cat)
        nome_cat = html.unescape(mt.group(1)).strip().lower() if mt else ''
        if nome_cat not in AREA:
            fora += cat.count('class="guia-item"')
            continue
        for art in re.findall(r'<article id="post-(\d+)" class="guia-item">(.*?)</article>', cat, re.S):
            pid, corpo = art
            m_link = re.search(r'href="([^"]+)"[^>]*>\s*<h3 class="guia-item-titulo">(.*?)</h3>', corpo, re.S)
            if not m_link:
                continue
            link, titulo = html.unescape(m_link.group(1)), limpa(m_link.group(2))
            m_txt = re.search(r'class="guia-item-texto">(.*?)</div>', corpo, re.S)
            detalhes = dict()
            for tit, cont in re.findall(r'guia-item-detalhe-titulo">\s*(.*?)\s*</span>(.*?)</div>', corpo, re.S):
                detalhes[slug(limpa(tit))] = cont
            origens = [{'fonte': FONTE, 'url': link, 'coletado_em': coletado},
                       {'fonte': FONTE, 'url': URL + '#' + slug(nome_cat), 'coletado_em': coletado}]
            sessoes = []
            for s in _servico(detalhes.get('servicos', ''), ref):
                lg = s['lugar'] or {}
                if s['cidade']:          # lugar fora de São Paulo dentro de categoria de SP
                    fora += 1
                    continue
                atracao = None
                if lg and not lg.get('endereco') and not lg.get('endereco_texto'):
                    # em festivais o negrito é a atração, não o lugar
                    atracao, lg = lg.get('nome'), {}
                lid = slug(lg.get('nome', ''))
                if lid and lid not in lugares:
                    lugares[lid] = sem_vazios({
                        'id': lid, 'nome': campo(lg.get('nome'), 0), 'endereco': campo(lg.get('endereco'), 0),
                        'bairro': campo(lg.get('bairro'), 0), 'telefone': campo(lg.get('telefone'), 0),
                        'endereco_texto': campo(lg.get('endereco_texto'), 0),
                        'origens': [{'fonte': FONTE, 'url': link, 'coletado_em': coletado}]})
                deduz = 'ano deduzido: a fonte escreve só dia e mês'
                sessoes.append(sem_vazios({
                    'lugar': lid or None, 'sala': campo(lg.get('sala'), 1), 'atracao': campo(atracao, 1),
                    'quando': campo(s['quando'], 1),
                    'datas': campo(s['datas'], 1, obs=deduz) if s['datas'] else None,
                    'estreia': campo(s['estreia'], 1, obs=deduz) if s['estreia'] else None,
                    'ate': campo(s['ate'], 1, obs=deduz) if s['ate'] else None,
                    'preco': campo(s['preco'], 1), 'duracao_min': campo(s['duracao_min'], 1),
                    'classificacao': campo(s['classificacao'], 1),
                    'ingresso': campo(s['ingresso'], 1), 'site': campo(s['site'], 1),
                    'obs': campo(s['obs'], 1), 'texto_fonte': campo(s['texto'], 1)}))
            if not sessoes:
                continue
            itens.append(sem_vazios({
                'id': FONTE + '-' + pid, 'area': campo(AREA[nome_cat], 1),
                'titulo': campo(titulo, 0), 'link_fonte': campo(link, 0),
                'trecho': campo(trecho(limpa(m_txt.group(1)) if m_txt else ''), 0),
                'ficha': campo(trecho(limpa(detalhes.get('ficha-tecnica', '')), 400), 0),
                'sessoes': sessoes, 'origens': origens}))
    if len(itens) < 20:
        # o mês teatral de SP nunca tem menos de 20 espetáculos: a página mudou
        raise RuntimeError('só %d espetáculos lidos: o formato da página pode ter mudado' % len(itens))
    return itens, list(lugares.values()), fora


if __name__ == '__main__':
    try:
        itens, lugares, fora = coleta()
        grava_bruto(FONTE, True, itens, lugares, nota='%d itens fora de SP ou de categoria não usada' % fora)
        print('Guia OFF: %d espetáculos, %d lugares (%d fora de SP ignorados)' % (len(itens), len(lugares), fora))
    except Exception as e:
        grava_bruto(FONTE, False, None, erro=e)
        print('Guia OFF FALHOU:', e)
        sys.exit(1)
