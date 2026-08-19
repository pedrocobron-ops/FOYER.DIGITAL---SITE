#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor da mesa: confere um pacote de matéria da redação de agentes ANTES
do commit. É o portão mecânico da esteira (a checagem de FATOS é do agente
Checador; aqui entra tudo o que dá para verificar por máquina).

Uso:
  python3 tools/audita_pauta.py import/pauta/<slug>.json [outra.json ...]

Sai com código 1 se qualquer matéria tiver PROBLEMA (não pode ir à mesa).
AVISO não bloqueia, mas deve ser lido pelo chefe de fechamento.

Passe a rodada inteira de uma vez (todos os arquivos numa chamada só): os
avisos de MOLDE só aparecem olhando as matérias juntas, porque o esqueleto
repetido não se vê numa matéria isolada.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# LISTA CANÔNICA DE EDITORIAS. Precisa ser IDÊNTICA à do manual (seção
# "Formato do pacote"); divergência é erro de sistema, e o manual manda
# corrigir entre rodadas. Entenda, Memória e Programa entraram com a versão
# 4.0 do manual, em 04/08/2026. Teatro Musical entrou em 08/08/2026 como
# editoria própria (pedido do Pedro): é a força da casa e merecia vitrine.
CATS_AGENTES = {'Teatro', 'Teatro Musical', 'Notícia', 'Cinema', 'Streaming', 'Música', 'Show',
                'Dança', 'Exposições', 'Literatura', 'Televisão', 'Audições',
                'Edital', 'Festa', 'Programa', 'Guia', 'Bastidores',
                'Entenda', 'Memória'}
CATS_PROIBIDAS = {'Crítica', 'Artigo de Opinião', 'Astrologia', 'Crônicas e Histórias'}

AGENCIAS_PROIBIDAS = ['getty', 'reuters', 'afp', 'folhapress', 'associated press',
                      'shutterstock', 'istock', 'alamy', 'estadão conteúdo',
                      'estadao conteudo', 'epa images', 'zuma press']

CLICHES = ['imperdível', 'vibrante', 'promete emocionar', 'experiência única',
           'sucesso absoluto', 'vem conquistando', 'não poderia ser diferente',
           'é aí que entra', 'prova de que', 'não é detalhe', 'verdadeiro espetáculo',
           'verdadeira celebração']

FECHO_INSTA = 'Para conferir a matéria completa, acesse o site: www.foyer.digital'

BLOCOS_FIXOS = {'serviço', 'servico', 'perguntas rápidas', 'perguntas rapidas'}

# Os quatro portes de matéria (ordem do Pedro, 02/08/2026).
# piso e teto de palavras, mínimo e máximo de intertítulos "## ".
PORTES = {
    # release de peça com serviço: o serviço É a matéria; texto corrido,
    # sem quebra, porque quebrar 400 palavras em seções é encenação.
    'release':          (350,  500, 0, 0),
    # tema quente: notícia do dia, escrita para ser lida agora.
    'quente':           (400,  600, 0, 2),
    # matéria contextualizada: a reportagem com fôlego, o padrão da casa.
    'contextualizada':  (700, 1100, 3, 5),
    # lista, guia e ranking: cada item é uma seção, então intertítulo sobra.
    'lista':            (900, 1500, 5, 14),
}


def _texto_limpo(corpo):
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', corpo)
    # a galeria nova é multilinha (uma foto por linha, com legenda e crédito):
    # o bloco inteiro sai da conta de palavras, não só a primeira linha
    t = re.sub(r'^galeria:[^\n]*(?:\n[ \t]*\S[^\n]*)*', '', t, flags=re.M)
    t = re.sub(r'^(img:|video:|galeria:|botao:|spotify:|#+ |\*\*\*).*$', '', t, flags=re.M)
    return t


def _paragrafos_de_texto(corpo):
    """Parágrafos de prosa, sem intertítulo, bloco de mídia, citação ou
    os blocos fixos do pé (Serviço e Perguntas rápidas)."""
    corte = re.split(r'^## +(?:Serviço|Servico|Perguntas)', corpo, flags=re.M)[0]
    return [p.strip() for p in corte.split('\n\n')
            if p.strip() and not p.strip().startswith(
                ('## ', '#', 'img:', 'video:', 'galeria:', 'botao:', 'spotify:',
                 '> ', '***'))]


def _frases(corpo):
    """Frases da PROSA, para medir o ritmo.

    Mede só o que o redator escreve por ritmo, e por isso parte dos parágrafos
    de prosa: o bloco de Serviço (endereço, horário, faixa de preço) é uma
    ficha, não redação, e as citações "> " são palavra de outra pessoa, que a
    casa não reescreve. Contar os dois afundava a conta justamente nos
    releases, em que a ficha é grande parte do texto.

    A quebra exige espaço depois do ponto E maiúscula depois dele: sem isso,
    "Lei 6.533" e "R$ 1.200" viravam duas frases e a conta de ritmo mentia.
    """
    saida = []
    for par in _paragrafos_de_texto(corpo):
        # parágrafo a parágrafo: emendar todos num texto só colava o fim de um
        # no começo do outro quando o primeiro terminava em dois-pontos, e a
        # emenda aparecia como uma frase gigante que ninguém escreveu.
        t = _texto_limpo(par).replace('\n', ' ')
        bruto = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-ÚÁÉÍÓÚÂÊÔÃÕÇ“"\*\[])', t)
        saida += [f for f in (x.strip() for x in bruto) if len(f.split()) >= 3]
    return saida


def auditar(caminho):
    problemas, avisos = [], []
    try:
        pg = json.load(open(caminho))
    except Exception as e:
        return [f'JSON INVÁLIDO: {e}'], [], {'inter': -1, 'porte': '?', 'author': '?'}
    slug = pg.get('slug', '')
    corpo = pg.get('corpo', '')
    titulo = pg.get('title', '')
    insta = pg.get('instagram') or {}

    # 0. Sugestão de data (pedido do Pedro, 19/08/2026): toda matéria chega à
    #    mesa com a hora de publicação já sugerida. O chefe aprova nela com um
    #    clique — mas quem decide segue sendo ele.
    sug = pg.get('sugestaoPublishAt', '')
    if not sug:
        problemas.append('SEM sugestaoPublishAt: toda matéria deve chegar com a '
                         'data/hora sugerida de publicação (ISO UTC, ver REDACAO.md)')
    else:
        try:
            from datetime import datetime as _dt, timezone as _tz
            _q = _dt.fromisoformat(str(sug).replace('Z', '+00:00'))
            if _q.tzinfo is None:
                problemas.append(f'sugestaoPublishAt sem fuso ("{sug}"): usar ISO UTC, '
                                 f'ex. 2026-08-20T17:00:00+00:00')
            elif _q <= _dt.now(_tz.utc):
                problemas.append(f'sugestaoPublishAt no passado ("{sug}"): sugerir uma '
                                 f'hora futura')
        except Exception:
            problemas.append(f'sugestaoPublishAt ilegível ("{sug}"): usar ISO UTC')

    # 1. Travessão e meia-risca: proibidos como pontuação em tudo o que chega ao
    #    leitor. Passam só dentro de nome próprio que a matéria declare em
    #    "nomes_proprios" (o nome oficial de uma montagem, filme ou disco),
    #    nunca como respiro de frase.
    campos = {'title': titulo, 'corpo': corpo,
              'instagram.titulo': insta.get('titulo', ''),
              'instagram.legenda': insta.get('legenda', '')}
    pacote = '\n'.join(campos.values())
    nomes = pg.get('nomes_proprios') or []
    if not isinstance(nomes, list):
        problemas.append('NOMES_PROPRIOS deve ser uma lista de nomes')
        nomes = []
    validos = []
    for nome in nomes:
        nome = str(nome).strip()
        if not ('—' in nome or '–' in nome):
            avisos.append(f'NOME PRÓPRIO "{nome}" declarado sem travessão (declaração inútil)')
            continue
        if len(nome) > 80 or re.search(r'[.!?;\n]', nome):
            problemas.append(f'NOME PRÓPRIO "{nome[:60]}" não parece um nome: '
                             f'longo demais ou com pontuação de frase')
            continue
        if nome not in pacote:
            avisos.append(f'NOME PRÓPRIO "{nome}" declarado mas ausente do texto')
            continue
        validos.append(nome)
    for nome, valor in campos.items():
        sobra = valor
        for np in validos:
            sobra = sobra.replace(np, '')
        n = sobra.count('—') + sobra.count('–')
        if n:
            problemas.append(f'TRAVESSÃO em {nome} ({n} ocorrência(s))')

    # 1b. O bloco do chefe também é lido por gente: é o que o editor humano tem
    #     na frente na Coxia quando decide o que fazer com a matéria. Ele não
    #     chega ao leitor, por isso é aviso e não trava. Mas ficou de fora da
    #     varredura até 06/08/2026, e o resultado foi previsível: a única
    #     ocorrência de travessão de uma leva inteira estava justamente na
    #     ressalva que descrevia uma correção de estilo. Trava que só olha onde
    #     a casa já se comporta bem não é trava.
    ch_pg = pg.get('chefe') or {}
    internos = {'chefe.parecer': str(ch_pg.get('parecer') or '')}
    for i, r in enumerate(ch_pg.get('ressalvas') or []):
        internos[f'chefe.ressalvas[{i}]'] = str(r)
    for nome, valor in internos.items():
        sobra = valor
        for np in validos:
            sobra = sobra.replace(np, '')
        n = sobra.count('—') + sobra.count('–')
        if n:
            avisos.append(f'TRAVESSÃO em {nome} ({n} ocorrência(s)): '
                          f'a régua da casa vale também para o que vai à mesa')

    # 2. Tamanho e forma da reportagem, pelo PORTE declarado no pacote.
    #    Uma faixa só para tudo (o antigo 750-1.100) fazia toda matéria sair
    #    do mesmo tamanho e com o mesmo esqueleto de 4 ou 5 intertítulos.
    #    Cada porte agora tem faixa própria E cota própria de intertítulos:
    #    é a segunda que quebra o molde, porque tamanho sozinho não quebra.
    porte = (pg.get('porte') or 'contextualizada').strip().lower()
    if porte not in PORTES:
        problemas.append(f'PORTE desconhecido: "{porte}" '
                         f'(use {", ".join(sorted(PORTES))})')
        porte = 'contextualizada'
    piso, teto, it_min, it_max = PORTES[porte]
    palavras = len(_texto_limpo(corpo).split())
    if palavras < piso:
        problemas.append(f'CURTA: {palavras} palavras '
                         f'(porte "{porte}" pede {piso} a {teto})')
    elif palavras > teto * 1.1:
        # o teto antigo era conselho e ninguém obedecia: 8 das 28 últimas
        # passaram das 1.100. Agora ele barra, com 10% de folga.
        problemas.append(f'LONGA: {palavras} palavras '
                         f'(porte "{porte}" tem teto de {teto}; corte)')
    elif palavras > teto:
        avisos.append(f'ACIMA DO TETO: {palavras} palavras '
                      f'(porte "{porte}" pede até {teto})')

    # "Serviço" e "Perguntas rápidas" são blocos fixos da casa, não o
    # esqueleto narrativo: não entram na conta. Sem isso, um release de 400
    # palavras não poderia levar o serviço, que é justamente a razão dele.
    inter = len([t for t in re.findall(r'^## +(.+)$', corpo, flags=re.M)
                 if t.strip().lower().rstrip(':') not in BLOCOS_FIXOS])
    if inter < it_min or inter > it_max:
        alvo = f'{it_min} a {it_max}' if it_max else 'nenhum'
        problemas.append(f'INTERTÍTULOS: {inter} '
                         f'(porte "{porte}" pede {alvo})')

    # 3. Links internos: 3+, todos existindo no disco
    internos = [l for l in re.findall(r'\]\(([^)]+)\)', corpo) if not l.startswith('http')]
    quebrados = [l for l in internos if not os.path.exists(os.path.join(ROOT, l.split('#')[0]))]
    if len(internos) < 3:
        problemas.append(f'LINKS INTERNOS: só {len(internos)} (mínimo 3)')
    if quebrados:
        problemas.append(f'LINKS QUEBRADOS: {quebrados}')

    # 3a-bis. TÍTULO DE ALTO ALCANCE (ordem do Pedro, 08/08/2026).
    #     O buscador corta o título por volta de 60 caracteres. Nas 15 matérias
    #     de 08/08, oito passavam de 100: metade do título nunca era vista, e a
    #     informação que decide o clique morava justamente na metade cortada.
    #     Aviso, não trava: às vezes o título honesto é longo, e encolher a
    #     verdade para caber é pior. Quem decide é o Titulador.
    if titulo:
        n_tit = len(titulo)
        if n_tit > 90:
            avisos.append(f'TÍTULO LONGO: {n_tit} caracteres (teto 90; o '
                          f'buscador corta perto de 60). Os primeiros 60 '
                          f'precisam funcionar sozinhos: "{titulo[:60]}"')

    # 3b. O FECHO NÃO É UM LINK (ordem do Pedro, 04/08/2026).
    #     Desde que a cota de 3 links entrou, o redator passou a cumpri-la no
    #     lugar mais barato, que é o fim: 38% das matérias na mesa terminavam
    #     apontando para outra matéria, contra 11% antes da regra. A matéria
    #     deixava de terminar e passava a despachar o leitor para outra sala.
    paragrafos = _paragrafos_de_texto(corpo)
    if paragrafos and re.search(r'\]\([^)]+\)[\s.,;]*$', paragrafos[-1]):
        problemas.append('FECHO É UM LINK: o último parágrafo termina apontando '
                         'para outra matéria; feche o assunto com frase da casa '
                         '(links internos entram no meio do texto)')

    # 3c. RITMO, medido (ordem do Pedro, 04/08/2026). "Variar o ritmo" era
    #     conselho e não mudou nada: o acervo deu média de 23,8 palavras por
    #     frase, com textos passando de 30 e um deles sem UMA frase curta.
    #     Com o travessão proibido, o aposto virou vírgula empilhada e o
    #     período cresceu. Agora a régua é número.
    fr = _frases(corpo)
    if len(fr) >= 8:
        # arredonda ANTES de comparar: senão o laudo diz "22% de frases curtas
        # (alvo 20% ou mais)" e parece que o portão se contradiz.
        curtas = round(100.0 * sum(1 for f in fr if len(f.split()) < 12) / len(fr))
        media = sum(len(f.split()) for f in fr) / len(fr)
        if curtas < 15:
            problemas.append(f'TEXTO SEM RESPIRO: só {curtas}% das frases têm '
                             f'menos de 12 palavras (mínimo 15%, alvo 20%)')
        elif curtas < 22:
            avisos.append(f'POUCO RESPIRO: {curtas}% de frases curtas '
                          f'(alvo 20% ou mais)')
        if media > 28:
            problemas.append(f'PERÍODO LONGO DEMAIS: média de {media:.1f} palavras '
                             f'por frase (teto 28). Onde pediria travessão, use '
                             f'ponto final, não mais uma vírgula')

    # 4. Foto: existe, com crédito e fonte; sem agência proibida
    img = pg.get('img', '')
    if not (img and os.path.exists(os.path.join(ROOT, img))):
        problemas.append(f'FOTO AUSENTE: {img or "(sem campo img)"}')
    cred = pg.get('imgCredito', '')
    if not cred:
        problemas.append('SEM imgCredito')
    if not (pg.get('imgFonte') or '').startswith('http'):
        problemas.append('SEM imgFonte (URL de onde a foto veio)')
    for ag in AGENCIAS_PROIBIDAS:
        if ag in cred.lower():
            problemas.append(f'AGÊNCIA PROIBIDA no crédito: "{cred}"')
            break

    # 5. Fontes da apuração: 3+ URLs
    fontes = [f for f in (pg.get('fontes') or []) if str(f).startswith('http')]
    if len(fontes) < 3:
        problemas.append(f'FONTES: só {len(fontes)} URL(s) (mínimo 3)')

    # 6. "ao FOYER": agente nunca ouviu ninguém; só um humano pode escrever isso
    if re.search(r'\bao FOYER\b', corpo, re.I):
        problemas.append('"ao FOYER" no texto: agente não entrevista; atribuir ao veículo de origem')

    # 7. Citações: toda linha "> " precisa de aspas E atribuição nominal
    for linha in corpo.split('\n'):
        if linha.startswith('> '):
            if '"' not in linha and '“' not in linha:
                avisos.append(f'CITAÇÃO SEM ASPAS: {linha[:70]}…')
            elif not re.search(r'(afirm|diz|disse|cont[ao]|explic|resum|declar|escrev|lembr|avali|coment|acrescent|complet|defend|respond|segundo)', linha):
                avisos.append(f'CITAÇÃO SEM ATRIBUIÇÃO na linha: {linha[:70]}…')

    # 8. Editorias
    cat = pg.get('cat', '')
    cats = pg.get('cats') or []
    todas = [cat] + list(cats)
    for c in todas:
        if c in CATS_PROIBIDAS:
            problemas.append(f'EDITORIA PROIBIDA para agentes: {c}')
        elif c not in CATS_AGENTES and c != 'Em Cartaz':
            avisos.append(f'EDITORIA FORA DA LISTA de agentes: {c}')
    # "Em Cartaz" é SELO SECUNDÁRIO (manual 4.0): marca que a peça está em
    # temporada agora, e a página Em Cartaz se abastece pela janela do campo
    # evento. Como editoria principal ele roubaria a cat real da matéria.
    if cat == 'Em Cartaz':
        problemas.append('"Em Cartaz" como editoria PRINCIPAL: é selo secundário, '
                         'só entra em cats. Use a editoria real do assunto em cat')
    if 'Em Cartaz' in cats and not pg.get('evento'):
        problemas.append('"Em Cartaz" sem campo evento (a janela automática precisa dele)')
    if len(cats) > 2:
        problemas.append(f'MAIS DE 2 editorias secundárias: {cats}')

    # 9. Evento: datas no formato certo
    ev = pg.get('evento')
    if ev:
        for k in ('inicio', 'fim'):
            v = ev.get(k, '')
            if v and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
                problemas.append(f'EVENTO com {k} fora do formato AAAA-MM-DD: "{v}"')

    # 10. Instagram completo: título com destaque, legenda com o fecho exato, artes no disco
    if not insta.get('titulo'):
        problemas.append('INSTAGRAM sem titulo')
    elif '*' not in insta['titulo']:
        avisos.append('INSTAGRAM titulo sem *destaque dourado* marcado')
    leg = insta.get('legenda', '')
    if not leg:
        problemas.append('INSTAGRAM sem legenda')
    else:
        if FECHO_INSTA not in leg:
            problemas.append('INSTAGRAM legenda sem o fecho padrão da casa')
        if '📷' not in leg:
            problemas.append('INSTAGRAM legenda sem a linha 📷 de crédito')
        else:
            # A PORTA DOS FUNDOS (trava criada em 05/08/2026, na sétima ocorrência
            # em dois dias). O padrão: alguém corrige o corpo ou o crédito da foto,
            # a legenda do Instagram fica com a versão velha, e ninguém relê a
            # legenda. O CORTES.md já chamava isso de "o pior tipo" de erro, porque
            # parece resolvido na porta da frente e está vivo na dos fundos.
            # Aqui dá para conferir por máquina o caso mais claro: o crédito da
            # foto tem de ser o MESMO nos dois lugares.
            linha = next((l for l in leg.split('\n') if '📷' in l), '')
            cred_leg = linha.split('📷', 1)[-1].lstrip(': ').strip()
            cred_img = re.sub(r'^Foto:\s*', '', cred).strip()

            # Exigir texto IDÊNTICO nos dois seria estrito demais e reprovaria
            # matéria boa: a casa usa imgCredito para crédito MAIS legenda
            # descritiva, enquanto a linha 📷 leva só o crédito. O que denuncia a
            # porta dos fundos é outra coisa: depois de trocar a foto, o crédito
            # velho fica na legenda, e aí os dois textos não têm NADA em comum.
            # Então a régua é sobreposição, não igualdade.
            def _marcas(t):
                t = re.sub(r'[^\wÀ-ÿ ]', ' ', t.lower())
                return {w for w in t.split()
                        if len(w) > 3 and w not in {'foto', 'fotos', 'divulgacao',
                                                    'divulgação', 'imagem', 'como',
                                                    'para', 'pela', 'pelo', 'commons'}}
            a, b = _marcas(cred_img), _marcas(cred_leg)
            if a and b and not (a & b):
                problemas.append(
                    f'CRÉDITO DIVERGENTE entre a foto e a legenda do Instagram, '
                    f'sem uma palavra em comum: imgCredito diz "{cred_img[:70]}" e a '
                    f'linha 📷 diz "{cred_leg[:70]}". Quem troca a foto troca os dois')
    for fmt in ('feed', 'story'):
        if not os.path.exists(os.path.join(ROOT, f'assets/social/{slug}-{fmt}.jpg')):
            problemas.append(f'ARTE FALTANDO: assets/social/{slug}-{fmt}.jpg')

    # 11. Estado do pacote e parecer
    if pg.get('status') != 'aguardando_aprovacao':
        problemas.append(f'STATUS "{pg.get("status")}" (deve ser aguardando_aprovacao)')
    ch = pg.get('chefe') or {}
    if not ch.get('parecer'):
        problemas.append('SEM parecer do chefe de redação')

    # NOTA MÍNIMA 8 (ordem do Pedro, 04/08/2026). Pauta escolhida para ser
    # escrita já nasce com a obrigação de valer 8: se não chega lá depois das
    # três ondas, o erro foi escolher a pauta, e o conserto é no pauteiro, não
    # na mesa. O editor humano abre a Coxia para decidir o que publica, não
    # para consertar matéria fraca.
    nota = ch.get('nota')
    if nota is None:
        problemas.append('SEM nota do chefe de redação (mínimo 8 para ir à mesa)')
    elif not isinstance(nota, (int, float)):
        problemas.append(f'NOTA inválida: {nota!r} (precisa ser número de 0 a 10)')
    elif nota < 8:
        problemas.append(f'NOTA {nota}: abaixo do mínimo 8. A matéria NÃO vai à mesa: '
                         f'volta para o redator até chegar a 8, ou a pauta é '
                         f'descartada com o motivo no diário')
    elif nota > 10:
        problemas.append(f'NOTA {nota} fora da escala (0 a 10)')
    # assinaturas válidas: a coletiva ou uma pessoa real da equipe.
    # Matéria assinada por pessoa só pode ser aprovada por ela na Coxia.
    # a dupla assina os guias de fim de semana (ordem do Pedro, 30/07/2026):
    # qualquer um dos dois pode aprovar na Coxia
    ASSINATURAS = {'Redação Foyer', 'Pedro Amaral', 'Isabel Branquinha',
                   'Pedro Amaral e Isabel Branquinha'}
    if pg.get('author') not in ASSINATURAS:
        problemas.append(f'AUTOR "{pg.get("author")}" fora das assinaturas do FOYER '
                         f'({", ".join(sorted(ASSINATURAS))})')
    if not pg.get('checagem', {}).get('verificada'):
        avisos.append('SEM registro do Checador independente (campo checagem.verificada)')

    # 12. Clichês e fórmulas de IA (aviso: o chefe relê o trecho)
    baixo = corpo.lower()
    achados = [c for c in CLICHES if c in baixo]
    if achados:
        avisos.append(f'CLICHÊS a rever: {achados}')

    return problemas, avisos, {'inter': inter, 'porte': porte,
                               'author': pg.get('author', '?')}


def _molde_da_rodada(medidas):
    """Aviso de rodada: o molde não aparece numa matéria só, aparece na
    repetição. A régua dos portes cortou o tamanho e não cortou a forma —
    quase toda 'contextualizada' saía com exatamente 5 intertítulos. Só dá
    para ver isso olhando a rodada inteira, então o aviso mora aqui.
    """
    avisos = []
    por_porte = {}
    for m in medidas:
        por_porte.setdefault(m['porte'], []).append(m['inter'])
    for porte, contas in por_porte.items():
        if len(contas) >= 3 and len(set(contas)) == 1:
            avisos.append(f'MOLDE: as {len(contas)} matérias de porte "{porte}" '
                          f'desta rodada saíram todas com {contas[0]} '
                          f'intertítulos. Dentro da faixa, varie.')
    for autor in {m['author'] for m in medidas}:
        c = [m['inter'] for m in medidas if m['author'] == autor]
        if len(c) >= 2 and len(set(c)) == 1 and c[0] >= 3:
            avisos.append(f'MOLDE: as {len(c)} matérias de {autor} nesta rodada '
                          f'têm o mesmo número de intertítulos ({c[0]}).')
    return avisos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    geral_ok = True
    medidas = []
    # diario.json mora em import/pauta/ e não é matéria: sem isso, o jeito
    # natural de rodar a rodada inteira (import/pauta/*.json) reprova sempre.
    arquivos = [a for a in sys.argv[1:]
                if os.path.basename(a) not in ('diario.json', 'sugestoes.json')]
    for arq in arquivos:
        problemas, avisos, medida = auditar(arq)
        medidas.append(medida)
        nome = os.path.basename(arq)
        if problemas:
            geral_ok = False
            print(f'✗ {nome}: NÃO VAI À MESA')
            for p in problemas:
                print(f'   PROBLEMA: {p}')
        else:
            print(f'✓ {nome}: aprovada no portão mecânico')
        for a in avisos:
            print(f'   aviso: {a}')
    for a in _molde_da_rodada(medidas):
        print(f'aviso da rodada: {a}')
    print('GERAL:', 'aprovado' if geral_ok else 'REPROVADO')
    sys.exit(0 if geral_ok else 1)


if __name__ == '__main__':
    main()
