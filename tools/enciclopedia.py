#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enciclopédia do FOYER — mapeia todas as pessoas que aparecem no acervo.

Varre as 1.500+ matérias (autores e nomes citados no texto) e os episódios
dos programas (apresentadores e convidados nos títulos) e produz
import/enciclopedia.json:

  { "pessoas":   { "slug": {"nome", "aparicoes": [{tipo, papel, titulo, url, data}]} },
    "porMateria":{ "slug-da-materia": ["slug-pessoa", ...] },
    "porVideo":  { "videoId": ["slug-pessoa", ...] } }

Critério de verbete: a pessoa assina matéria, aparece em título de episódio,
ou é citada em 2+ matérias diferentes (corta falso positivo de citação única).
"""
import json, os, re, unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# palavras que nunca fazem parte de nome de pessoa (lugares, instituições, termos)
BLOQUEIO = set('''Teatro Teatros Municipal Festival Prêmio Premio Museu Centro Casa Companhia
Cia Grupo Escola Instituto Shopping Orquestra Sinfônica Sesc Sesi Rua Avenida Praça Praca
Brasil Brasileiro Brasileira Broadway Hollywood Netflix Globo Record YouTube Spotify Instagram
Facebook TikTok Google Estado Estados Unidos Nacional Internacional Mostra Bienal Feira Festa
Semana Virada Secretaria Ministério Ministerio Fundação Fundacao Universidade Faculdade Colégio
Colegio Cidade Vila Jardim Parque Palácio Palacio Edifício Edificio Complexo Arena Estádio
Estadio Ginásio Ginasio Auditório Auditorio Sala Espaço Espaco Galeria Livraria Editora Revista
Jornal Folha Estadão Estadao Musical Musicais Frei Caneca Cultura Cultural Artes Arte Cena
Palco Elenco Temporada Estreia Turnê Turne Prefeitura Câmara Camara Governo Lei Programa
Janeiro Fevereiro Março Marco Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro
Segunda Terça Terca Quarta Quinta Sexta Sábado Sabado Domingo Norte Sul Leste Oeste Zona
Ingressos Ingresso Sessão Sessao Sessões Sessoes Horário Horario Classificação Classificacao
Direção Direcao Produção Producao Realização Realizacao Apresentação Apresentacao Patrocínio
Patrocinio Apoio Entrada Gratuita Grátis Gratis Livre Anos Ano Edição Edicao Especial Noite
Dia Tarde Manhã Manha Hora Vez Gente Show Shows Rio Grande Foyer Digital Oscar Grammy Tony
Oz Bruxas Sonho Verão Verao Reveillon Réveillon Natal Páscoa Pascoa Carnaval
Serviço Servico Espetáculo Espetaculo Espetáculos Espetaculos Sinopse Em Até Ate Melhor Melhores
Sympla Duração Duracao Entretenimento Produções Producoes Eventos Ficha Técnica Tecnica Local
Onde Quando Quanto Vendas Bilheteria Plateia Balcão Balcao Meia Inteira Reais Confira Saiba
Leia Veja Assista Clique Acesse Link Bio Foto Fotos Divulgação Divulgacao Crédito Credito
Créditos Creditos Imagem Imagens Vídeo Video Vídeos Videos Trailer Teaser Data Datas Horários
Horarios Valores Valor Preço Preco Preços Precos Desconto Estudante Idoso Solidário Solidario
Abertura Encerramento Estreias Reestreia Musical Ópera Opera Balé Bale Ballet Cortina Bastidores
Prólogo Prologo Ato Atos Cenas Personagem Personagens Figurino Figurinos Cenário Cenario
Cenografia Iluminação Iluminacao Sonoplastia Coreografia Dramaturgia Roteiro Texto Adaptação
Adaptacao Tradução Traducao Versão Versao Original Baseado Inspirado Livremente Segundo Conforme
Idealização Idealizacao Concepção Concepcao Supervisão Supervisao Coordenação Coordenacao
Assistente Assistência Assistencia Operação Operacao Montagem Equipe Staff Elenco
Crítica Críticas Critica Criticas Teatral Teatrais Por Com Sobre Entre Para Episódio Episodio
Ep Parte Completo Completa Íntegra Integra Live Podcast Cortes Shorts React Reagindo
Bruxa Bruxo Bruxos História Historia Histórias Historias Não Nao Diários Diarios Assossiados
Associados Papel Papéis Papeis Personagens Protagonista Protagonistas Antagonista Vilã Vila
Herói Heroi Heroína Heroina Fada Fadas Príncipe Principe Princesa Rainha Rei Reis'''.split())

# nomes compostos de lugar que passam pelo filtro de palavras
LUGARES = {'são paulo', 'rio de janeiro', 'belo horizonte', 'porto alegre', 'nova york',
           'new york', 'los angeles', 'buenos aires', 'santo amaro', 'san francisco',
           'costa rica', 'porto rico', 'monte carlo', 'las vegas', 'bela vista',
           'campos elíseos', 'campos eliseos', 'américa latina', 'america latina',
           'sangue frio', 'itaim bibi', 'santa cecília', 'santa cecilia', 'vila madalena',
           'higienópolis', 'copacabana palace', 'lapa', 'pinheiros', 'consolação',
           'américa do sul', 'america do sul', 'américa do norte', 'reino unido',
           'oscar freire', 'paulista', 'faria lima', 'south bank', 'west end',
           'off broadway', 'times square', 'la scala', 'covent garden',
           'barra funda', 'paes de barros', 'alameda nothmann', 'água branca',
           'agua branca', 'cerqueira césar', 'cerqueira cesar', 'chucri zaidan',
           'alto da mooca', 'minas gerais', 'santos dumont', 'juscelino kubitschek',
           'brigadeiro luís antônio', 'brigadeiro luis antonio', 'dom casmurro',
           'funny girl', 'rei do rock', 'não perca', 'nao perca', 'quintas e sextas',
           'warner bros', 'bradesco seguros', 'corda bamba', 'coxixo de coxia',
           'núcleo experimental', 'nucleo experimental', 'moulin rouge', 'grande otelo',
           'beco do pinto', 'anhembi morumbi', 'brás cubas', 'bras cubas',
           'nossa senhora', 'santa efigênia', 'santa efigenia', 'bom retiro',
           'jabaquara', 'vila olímpia', 'vila olimpia', 'liberdade', 'barra da tijuca'}


# palavras que VETAM o nome inteiro (contexto de lugar/instituição — "Teatro Sérgio Cardoso"
# homenageia uma pessoa, mas a citação é ao prédio, não à pessoa)
VETO_TOTAL = set('''Teatro Teatros Cine Cinema Museu Centro Casa Companhia Cia Grupo Escola
Instituto Shopping Orquestra Auditório Auditorio Sala Espaço Espaco Galeria Arena Complexo
Palácio Palacio Fundação Fundacao Universidade Faculdade Avenida Rua Alameda Praça Praca Largo
Viaduto Estação Estacao Prêmio Premio Prêmios Premios Festival Mostra Bienal Edifício Edificio
Hospital Aeroporto Estádio Estadio Ginásio Ginasio Biblioteca Livraria Colégio Colegio'''.split())

CONECT = {'de', 'da', 'do', 'das', 'dos', 'del', 'von', 'van', 'di'}

TOKEN = r"[A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇ][a-záâãàéêíóôõúüçñ'\-]+"
NOME_RE = re.compile(rf"\b({TOKEN}(?:\s+(?:(?:{'|'.join(CONECT)})\s+)?{TOKEN}){{1,3}})\b")


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:70]


def nome_valido(nome):
    partes = nome.replace('-', ' ').split()
    if len([p for p in partes if p.lower() not in CONECT]) < 2:
        return False
    for p in partes:
        if p in BLOQUEIO or p.lower() in LUGARES:
            return False
    if nome.lower() in LUGARES:
        return False
    if len(nome) > 40:
        return False
    return True


def extrair_nomes(texto):
    # remove títulos de obras entre aspas — “Assim” "Assim" ‘Assim’
    texto = re.sub(r'[“"‘\'』«][^”"’\'»]{2,90}[”"’\'»]', ' ', texto)
    achados = set()
    for m in NOME_RE.finditer(texto):
        n = re.sub(r'\s+', ' ', m.group(1)).strip()
        partes = n.split()
        # lugar/instituição no meio? o nome inteiro cai (é o prédio, não a pessoa)
        if any(p in VETO_TOTAL for p in partes):
            continue
        # apara palavras bloqueadas do início ("Por Bruno Cavalcanti" -> "Bruno Cavalcanti")
        while partes and (partes[0] in BLOQUEIO or partes[0].lower() in CONECT):
            partes = partes[1:]
        while partes and (partes[-1] in BLOQUEIO or partes[-1].lower() in CONECT):
            partes = partes[:-1]
        n = ' '.join(partes)
        if n and nome_valido(n):
            achados.add(n)
    return achados


def main():
    materias = json.load(open(f'{ROOT}/import/materias.json'))
    # inclui as matérias publicadas pela Coxia (import/novas) que não estão no índice do Wix
    ja = {m['slug'] for m in materias}
    novas_dir = f'{ROOT}/import/novas'
    if os.path.isdir(novas_dir):
        for f in sorted(os.listdir(novas_dir)):
            if not f.endswith('.json'):
                continue
            try:
                n = json.load(open(os.path.join(novas_dir, f)))
            except Exception:
                continue
            if n.get('slug') in ja:
                continue
            materias.insert(0, {'slug': n['slug'], 'title': n['title'],
                                'author': n.get('author', ''), 'desc': '',
                                'iso': (n.get('publishAt') or '')[:10],
                                'cat': n.get('cat', '')})
    try:
        yt = json.load(open(f'{ROOT}/import/youtube.json'))
    except Exception:
        yt = {'programas': []}

    pessoas = defaultdict(lambda: {'nome': '', 'aparicoes': []})
    por_materia = defaultdict(list)
    por_video = defaultdict(list)
    citacoes = defaultdict(set)   # slug-pessoa -> set(slug-materia) p/ regra dos 2+

    def registra(nome, tipo, papel, titulo, url, data, chave_grupo=None):
        sp = slugify(nome)
        if not sp:
            return None
        p = pessoas[sp]
        p['nome'] = p['nome'] or nome
        p['aparicoes'].append({'tipo': tipo, 'papel': papel, 'titulo': titulo,
                               'url': url, 'data': data})
        return sp

    # ---- matérias: autor + citados no texto ----
    for m in materias:
        url = f"post-{m['slug']}.html"
        autor = (m.get('author') or '').strip()
        if autor and autor.lower() not in ('redação foyer', 'redacao foyer') and nome_valido(autor):
            sp = registra(autor, 'materia', 'autor', m['title'], url, m.get('iso', ''))
            if sp:
                por_materia[m['slug']].append(sp)
        corpo_path = f"{ROOT}/import/corpo/{m['slug']}.html"
        texto = m['title'] + '. ' + m.get('desc', '')
        if os.path.exists(corpo_path):
            texto += ' ' + re.sub(r'<[^>]+>', ' ', open(corpo_path).read())
        for nome in extrair_nomes(texto):
            sp = slugify(nome)
            if sp and slugify(autor) == sp:
                continue
            spp = registra(nome, 'materia', 'citado', m['title'], url, m.get('iso', ''))
            if spp:
                por_materia[m['slug']].append(spp)
                citacoes[spp].add(m['slug'])

    # ---- episódios: convidados/nomes nos títulos ----
    APRESENTA = {'Por Bruno Cavalcanti': 'Bruno Cavalcanti'}
    for prog in yt.get('programas', []):
        nome_prog = prog['nome'].split(' — ')[0]
        for v in prog.get('videos', []):
            for nome in extrair_nomes(v['titulo']):
                sp = registra(nome, 'episodio', 'convidado', f"{nome_prog}: {v['titulo']}",
                              v['url'], v.get('quando', ''))
                if sp:
                    por_video[v['id']].append(sp)
        apres = APRESENTA.get(nome_prog)
        if apres and prog.get('videos'):
            registra(apres, 'programa', 'apresenta', nome_prog,
                     prog['urlPlaylist'], prog['videos'][0].get('quando', ''))

    # ---- regra de corte: citação única não vira verbete ----
    finais = {}
    for sp, p in pessoas.items():
        papeis = {a['papel'] for a in p['aparicoes']}
        if papeis - {'citado'} or len(citacoes.get(sp, ())) >= 2:
            # dedup de aparições iguais
            vistos, aps = set(), []
            for a in sorted(p['aparicoes'], key=lambda x: x.get('data', ''), reverse=True):
                k = (a['tipo'], a['url'])
                if k in vistos:
                    continue
                vistos.add(k)
                aps.append(a)
            finais[sp] = {'nome': p['nome'], 'aparicoes': aps}

    por_materia = {k: sorted({s for s in v if s in finais}) for k, v in por_materia.items()}
    por_materia = {k: v for k, v in por_materia.items() if v}
    por_video = {k: sorted({s for s in v if s in finais}) for k, v in por_video.items()}
    por_video = {k: v for k, v in por_video.items() if v}

    saida = {'pessoas': finais, 'porMateria': por_materia, 'porVideo': por_video}
    json.dump(saida, open(f'{ROOT}/import/enciclopedia.json', 'w'),
              ensure_ascii=False, indent=1)
    print(f'pessoas com verbete: {len(finais)}')
    top = sorted(finais.items(), key=lambda x: len(x[1]['aparicoes']), reverse=True)[:25]
    for sp, p in top:
        print(f"  {len(p['aparicoes']):4d}  {p['nome']}")


if __name__ == '__main__':
    main()
