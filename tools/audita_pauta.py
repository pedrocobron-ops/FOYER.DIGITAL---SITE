#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor da mesa: confere um pacote de matéria da redação de agentes ANTES
do commit. É o portão mecânico da esteira (a checagem de FATOS é do agente
Checador; aqui entra tudo o que dá para verificar por máquina).

Uso:
  python3 tools/audita_pauta.py import/pauta/<slug>.json [outra.json ...]

Sai com código 1 se qualquer matéria tiver PROBLEMA (não pode ir à mesa).
AVISO não bloqueia, mas deve ser lido pelo chefe de fechamento.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATS_AGENTES = {'Teatro', 'Notícia', 'Cinema', 'Streaming', 'Música', 'Show',
                'Dança', 'Exposições', 'Literatura', 'Televisão', 'Audições',
                'Edital', 'Festa', 'Guia', 'Bastidores'}
CATS_PROIBIDAS = {'Crítica', 'Artigo de Opinião', 'Astrologia', 'Crônicas e Histórias'}

AGENCIAS_PROIBIDAS = ['getty', 'reuters', 'afp', 'folhapress', 'associated press',
                      'shutterstock', 'istock', 'alamy', 'estadão conteúdo',
                      'estadao conteudo', 'epa images', 'zuma press']

CLICHES = ['imperdível', 'vibrante', 'promete emocionar', 'experiência única',
           'sucesso absoluto', 'vem conquistando', 'não poderia ser diferente',
           'é aí que entra', 'prova de que', 'não é detalhe', 'verdadeiro espetáculo',
           'verdadeira celebração']

FECHO_INSTA = 'Para conferir a matéria completa, acesse o site: www.foyer.digital'


def _texto_limpo(corpo):
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', corpo)
    t = re.sub(r'^(img:|video:|galeria:|botao:|spotify:|#+ |\*\*\*).*$', '', t, flags=re.M)
    return t


def auditar(caminho):
    problemas, avisos = [], []
    try:
        pg = json.load(open(caminho))
    except Exception as e:
        return [f'JSON INVÁLIDO: {e}'], []
    slug = pg.get('slug', '')
    corpo = pg.get('corpo', '')
    titulo = pg.get('title', '')
    insta = pg.get('instagram') or {}

    # 1. Travessão e meia-risca: proibidos como pontuação em TODO o pacote.
    #    Passam só dentro de nome próprio que a matéria declare em "nomes_proprios"
    #    (o nome oficial de uma montagem, filme ou disco), nunca como respiro de frase.
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

    # 2. Tamanho da reportagem
    palavras = len(_texto_limpo(corpo).split())
    if palavras < 750:
        problemas.append(f'CURTA: {palavras} palavras (mínimo 750)')
    elif palavras > 1300:
        avisos.append(f'LONGA: {palavras} palavras (alvo 750 a 1.100)')

    # 3. Links internos: 3+, todos existindo no disco
    internos = [l for l in re.findall(r'\]\(([^)]+)\)', corpo) if not l.startswith('http')]
    quebrados = [l for l in internos if not os.path.exists(os.path.join(ROOT, l.split('#')[0]))]
    if len(internos) < 3:
        problemas.append(f'LINKS INTERNOS: só {len(internos)} (mínimo 3)')
    if quebrados:
        problemas.append(f'LINKS QUEBRADOS: {quebrados}')

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
    for fmt in ('feed', 'story'):
        if not os.path.exists(os.path.join(ROOT, f'assets/social/{slug}-{fmt}.jpg')):
            problemas.append(f'ARTE FALTANDO: assets/social/{slug}-{fmt}.jpg')

    # 11. Estado do pacote e parecer
    if pg.get('status') != 'aguardando_aprovacao':
        problemas.append(f'STATUS "{pg.get("status")}" (deve ser aguardando_aprovacao)')
    ch = pg.get('chefe') or {}
    if not ch.get('parecer'):
        problemas.append('SEM parecer do chefe de redação')
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

    return problemas, avisos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    geral_ok = True
    for arq in sys.argv[1:]:
        problemas, avisos = auditar(arq)
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
    print('GERAL:', 'aprovado' if geral_ok else 'REPROVADO')
    sys.exit(0 if geral_ok else 1)


if __name__ == '__main__':
    main()
