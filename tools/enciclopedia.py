#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enciclopédia do FOYER — mapeia todas as pessoas que aparecem no acervo.

Varre as 1.500+ matérias (autores e nomes citados no texto) e os episódios
dos programas (apresentadores e convidados nos títulos) e produz
import/enciclopedia.json:

  { "pessoas":   { "slug": {"nome", "aparicoes": [{tipo, papel, titulo, url, data}]} },
    "porMateria":{ "slug-da-materia": ["slug-pessoa", ...] },
    "porVideo":  { "videoId": ["slug-pessoa", ...] },
    "convidadosPorVideo": { "videoId": ["slug-convidado", ...] } }

Papel no episódio: 'convidado' (no título, num convite da descrição ou na
lista à mão das regras), 'mencionado' (só citado na descrição) e 'apresenta'.
convidadosPorVideo guarda só os convidados, título primeiro, sem apresentador.

Critério de verbete: a pessoa assina matéria, aparece em título de episódio,
é TEMA de matéria (nome no título, quando o título é no padrão da casa) ou é
citada em 2+ matérias diferentes (corta falso positivo de citação única).
"""
import json, os, re, unicodedata
from collections import defaultdict
from datetime import datetime, timezone

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
Drag Race Longa Curta Filme Filmes Série Serie Séries Series Documentário Documentario Comédia Comedia Tragédia Tragedia Fringe Legalmente Old
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
Hospital Aeroporto Estádio Estadio Ginásio Ginasio Biblioteca Livraria Colégio Colegio
Coletivo Trupe Circo Núcleo Nucleo Coral Rádio Radio Blog Plataforma App Dicionário Dicionario
Presídio Presidio Prédio Predio Multipalco Condecine Ticketmaster Rede Canal Portal Revista Jornal
Programa Podcast Série Serie Novela Filme Clube Hotel Igreja Catedral Parque Praia Ilha Shopping'''.split())

# Texto logo ANTES do nome que diz que é endereço ou lugar, não gente:
# "R. Rui Barbosa", "Av. Roque Petroni Júnior", "teatros Arthur Azevedo, Alfredo
# Mesquita e Paulo Eiró" (vistoria de 06/10/2026: 12 verbetes eram ruas e
# avenidas). Só palavras que o próprio nome capturado não traz: abreviações,
# minúsculas e plurais; "Teatro X" com maiúscula já cai pelo VETO_TOTAL.
#   Metrô e estação também (auditoria de 10/10/2026): o "metrô Jardim São
# Paulo-Ayrton Senna" de uma descrição punha o piloto como convidado de um
# episódio de 2026.
ANTES_LUGAR = re.compile(
    r"(?:\b(?:R|Av|Al|Pç|Pça|Tv|Est|Rod)\.|\b(?:rua|avenida|alameda|praça|praca|largo|travessa|estrada|rodovia|metrô|estação|estacao|"
    r"teatros|salas|cinemas|espaços|espacos|auditórios|auditorios|prêmios|premios|escolas|institutos|fundações|"
    r"fundacoes|galerias|bibliotecas|hospitais|estações|estacoes|aeroportos|colégios|colegios))"
    r"(?:\s+(?:[A-ZÀ-Ú][^\s,]*|de|do|da|dos|das|e)|,)*\s*$", re.I)

CONECT = {'de', 'da', 'do', 'das', 'dos', 'del', 'von', 'van', 'di'}

# preposição/contração que abre frase colada num nome ("Na Espanha", "Em Buenos Aires"):
# apara da ponta, nunca vira parte do verbete
PREP_PONTA = {'na', 'no', 'nas', 'nos', 'em', 'a', 'à', 'ao', 'às', 'aos', 'pela', 'pelo',
              'pelas', 'pelos', 'com', 'sem', 'para', 'por', 'sob', 'sobre', 'entre',
              'até', 'ate', 'desde', 'após', 'apos', 'durante', 'contra', 'segundo',
              'conforme', 'perante', 'já', 'ja', 'e', 'ou', 'mas', 'se', 'quando', 'como',
              # palavra de frase colada na ponta de um nome ("Priscila Prade Depois",
              # "Seu Dinheiro", "Poder Neste"): vistoria de 06/10/2026
              'depois', 'pois', 'neste', 'nesta', 'nisso', 'ela', 'ele', 'eles', 'elas', 'há', 'ha',
              'letra', 'tema', 'volta', 'design', 'venda', 'vem', 'veja', 'seu', 'sua', 'seus', 'suas',
              'minha', 'meu', 'nossa', 'nosso', 'todo', 'toda', 'todos', 'todas', 'nada', 'muito', 'muita',
              'hoje', 'ontem', 'amanhã', 'amanha', 'agora', 'ainda', 'também', 'tambem', 'assim', 'onde',
              'porque', 'porém', 'porem', 'então', 'entao', 'aqui', 'ali', 'lá', 'la', 'cá', 'ca', 'sim',
              'não', 'nao', 'mais', 'menos', 'bem', 'mal', 'só', 'so', 'tudo', 'algo', 'cada', 'outro', 'outra',
              'antes', 'eu', 'nós', 'nos', 'você', 'voce', 'vocês', 'voces', 'primeira', 'primeiro', 'segunda',
              'terceira', 'terceiro', 'última', 'ultima', 'último', 'ultimo', 'um', 'uma', 'dois', 'duas', 'três',
              'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'vindos', 'vindas', 'vindo', 'vinda',
              # verbo que abre a frase colado no nome ("Recebemos Ivan Parente",
              # "Fala de Paulo Gustavo"): auditoria de 10/10/2026
              'recebemos', 'recebe', 'recebem', 'receberam', 'fala', 'falam', 'conversa', 'conversam',
              'conversamos', 'entrevista', 'entrevistamos', 'convida', 'convidamos', 'revela', 'revelam'}

# Primeira palavra que denuncia frase, título ou instituição, nunca gente: o
# nome inteiro cai ("Que Isso Quer Dizer", "Nome da Mãe", "Central de
# Atendimento", "Copa do Mundo", "Pré Indicações"). Auditoria de 10/10/2026.
PRIMEIRA_FORA = set('''Que Nome Projeto Projetos Central Menina Menino Quintal Queda Copa Força Pré
Cemitério Boneca Salão Departamento Fusão Economia Caixa Anatomia Amigas Amigos Aquela Aquele Reprodução'''.split())

# Uma palavra de nome: maiúscula + minúsculas, aceitando emenda por apóstrofo
# (reto ou curvo) ou hífen que recomeça em maiúscula — O'Hara, D'Ávila,
# Ana-Maria. Sem isso, "Eureka O'Hara" nunca virava verbete (05/08/2026).
TOKEN = r"[A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇ][a-záâãàéêíóôõúüçñ]+(?:['’\-][A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇa-záâãàéêíóôõúüçñ][a-záâãàéêíóôõúüçñ]*)*|[A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇ]['’][A-ZÁÂÃÀÉÊÍÓÔÕÚÜÇ][a-záâãàéêíóôõúüçñ]+"
# o (?:...) em volta do TOKEN é obrigatório: ele tem alternativa interna (|),
# e sem o grupo a alternativa quebraria a expressão inteira ao meio
NOME_RE = re.compile(rf"\b((?:{TOKEN})(?:\s+(?:(?:{'|'.join(CONECT)})\s+)?(?:{TOKEN})){{1,3}})\b")

# ---- regras editadas na Coxia (import/enciclopedia-regras.json) ----
try:
    REGRAS = json.load(open(f'{ROOT}/import/enciclopedia-regras.json'))
except Exception:
    REGRAS = {}
BLOQUEAR_NOMES = {n.strip().lower() for n in REGRAS.get('bloquear', []) if n.strip()}
NOMES_CURTOS = [n.strip() for n in REGRAS.get('nomes_curtos', []) if n.strip()]
APELIDOS = {k.strip().lower(): v.strip() for k, v in (REGRAS.get('apelidos') or {}).items() if k.strip() and v.strip()}
# convidados de um episódio escritos à mão (id do vídeo -> nomes), para quando
# o título e a descrição não dizem quem veio
CONVIDADOS_MANUAIS = {k: [n.strip() for n in v if isinstance(n, str) and n.strip()]
                      for k, v in (REGRAS.get('convidados') or {}).items() if isinstance(v, list)}
BLOQUEIO |= set((REGRAS.get('palavras_bloqueio') or []))
# instituições, veículos e termos em inglês que vinham virando "pessoa"
# (Royal Court Theatre, The Guardian, Box Office Mojo), mais os termos de
# lei/edital (Fundo Setorial, Federal de Incentivo) — revisão de 05/10/2026
BLOQUEIO |= set('''Theatre Theater Company College University Institute School Academy Times
Guardian Review Magazine Journal Office Mojo Inter Science Unesco Unicef Award Awards Records
Studio Studios Pictures Entertainment Street Avenue Square Hall House Center Centre Foundation
Group Media News Press Post Daily Weekly Radio Channel Network Music Productions Production Club
Bar Hotel Park Garden Palace Band Orchestra Quartet Trio Duo Ensemble Choir Chorus Collective
Project Lab Gallery Library Museum Archive Mundial Patrimônio Patrimonio Consultivo Setorial
Incentivo Defesa Consumidor Oficial União Uniao Antiguidades Arqueológica Arqueologica Carteira
Cadastro Único Unico Identificação Identificacao Estudantil Sociais Trajetória Trajetoria
Comando Tribunal Diário Diario Lista Comitê Comite Conselho Código Codigo Fundo Federal Estadual
São Sao Santa Santo The Los Las Les Der Die Das Endereço Endereco Codireção Codirecao
Coreografia Coreografias Visagismo Pesquisa Desenho Cenário Cenario Cenários Cenarios Adereços
Aderecos Maquiagem Fotografia Arranjos Preparação Preparacao Assistência Assistencia Sonoplastia
Dramaturgia Figurino Figurinos Iluminação Iluminacao Trilha Sonora Vocal Corporal Executiva
Executivo Operação Operacao Contrarregra Contrarregragem Cenotécnica Cenotecnica Produção Producao
Direção Direcao Realização Realizacao Idealização Idealizacao Coordenação Coordenacao'''.split())
# Palavra bloqueada na ponta do nome: só rótulo de ficha técnica ("Direção
# Kleber Montanheiro") e preposição ("Por Bruno Cavalcanti") são aparados;
# qualquer outra ("Um Inimigo do Povo", "São Paulo Acesso", "Theatre Royal
# Haymarket") derruba o nome inteiro — aparar deixava fragmentos como
# "Inimigo do Povo" e "Paulo Acesso" (05/10/2026).
FICHA_APARA = set('''Direção Direcao Produção Producao Texto Dramaturgia Iluminação Iluminacao Cenografia
Figurino Figurinos Coreografia Trilha Elenco Apresentação Apresentacao Realização Realizacao Idealização
Idealizacao Assistente Assistência Assistencia Operação Operacao Montagem Equipe Desenho Preparação
Preparacao Visagismo Pesquisa Codireção Codirecao Música Musica Cenário Cenario Cenários Cenarios Adereços
Aderecos Maquiagem Fotografia Fotos Foto Vídeo Video Arranjos Sonoplastia Tradução Traducao Versão Versao
Adaptação Adaptacao Supervisão Supervisao Coordenação Coordenacao Concepção Concepcao Contrarregra Endereço
Endereco Musical Geral Executiva Executivo Artística Artistica Vocal Corporal Crédito Credito Créditos Creditos
Divulgação Divulgacao Imagem Imagens Ficha Técnica Tecnica Serviço Servico Local Onde Quando Classificação
Classificacao Duração Duracao Ingressos Ingresso Sinopse Com Por Sobre Entre Para Em'''.split())
ARTIGOS_INICIO = {'um', 'uma', 'uns', 'umas', 'o', 'os', 'as', 'the', 'les', 'los', 'las', 'der', 'die', 'das'}

# caudas de ficha técnica que vinham grudadas no nome ("Nello Marrese Desenho de Luz")
CAUDA_RE = re.compile(r'\s+(?:Desenho de (?:Luz|Som)|Direção de (?:Arte|Movimento|Produção|Cena|Palco)'
                      r'|Preparação (?:Vocal|Corporal)|Trilha Sonora|Assistência de Direção'
                      r'|Produção Executiva|Operação de (?:Luz|Som)|Luz e Som)$')

# pistas de função: "a atriz Fulana", "dirigida por Fulano", "Fulano, dramaturgo,"
FUNCOES = {
    'ator': 'Ator', 'atriz': 'Atriz', 'diretor': 'Diretor', 'diretora': 'Diretora',
    'dramaturgo': 'Dramaturgo', 'dramaturga': 'Dramaturga', 'cantor': 'Cantor', 'cantora': 'Cantora',
    'produtor': 'Produtor', 'produtora': 'Produtora', 'coreógrafo': 'Coreógrafo', 'coreógrafa': 'Coreógrafa',
    'cenógrafo': 'Cenógrafo', 'cenógrafa': 'Cenógrafa', 'figurinista': 'Figurinista',
    'iluminador': 'Iluminador', 'iluminadora': 'Iluminadora', 'compositor': 'Compositor',
    'compositora': 'Compositora', 'escritor': 'Escritor', 'escritora': 'Escritora',
    'jornalista': 'Jornalista', 'crítico': 'Crítico', 'crítica': 'Crítica', 'apresentador': 'Apresentador',
    'apresentadora': 'Apresentadora', 'bailarino': 'Bailarino', 'bailarina': 'Bailarina',
    'humorista': 'Humorista', 'comediante': 'Comediante', 'roteirista': 'Roteirista',
    'cineasta': 'Cineasta', 'maestro': 'Maestro', 'maestrina': 'Maestrina', 'pianista': 'Pianista',
    'músico': 'Músico', 'musicista': 'Musicista', 'poeta': 'Poeta', 'poetisa': 'Poeta',
    'professor': 'Professor', 'professora': 'Professora', 'pesquisador': 'Pesquisador',
    'pesquisadora': 'Pesquisadora', 'fotógrafo': 'Fotógrafo', 'fotógrafa': 'Fotógrafa',
    'performer': 'Performer', 'encenador': 'Encenador', 'encenadora': 'Encenadora',
    'tenor': 'Tenor', 'soprano': 'Soprano', 'barítono': 'Barítono', 'regente': 'Regente',
    'arranjador': 'Arranjador', 'arranjadora': 'Arranjadora', 'dublador': 'Dublador', 'dubladora': 'Dubladora',
    'ilustrador': 'Ilustrador', 'ilustradora': 'Ilustradora', 'artista': 'Artista', 'autor': 'Autor', 'autora': 'Autora',
    'drag queen': 'Drag queen', 'intérprete': 'Intérprete', 'instrumentista': 'Instrumentista',
    'violonista': 'Violonista', 'guitarrista': 'Guitarrista', 'baterista': 'Baterista', 'baixista': 'Baixista',
    'percussionista': 'Percussionista', 'violinista': 'Violinista', 'cellista': 'Cellista', 'dançarino': 'Dançarino',
    'dançarina': 'Dançarina', 'palhaço': 'Palhaço', 'palhaça': 'Palhaça', 'ativista': 'Ativista',
    'historiador': 'Historiador', 'historiadora': 'Historiadora', 'crítica teatral': 'Crítica teatral',
}
# pistas que servem tanto para gente quanto para peça e empresa ("produção de
# Kinky Boots", "idealização da Cia X"): sozinhas não provam que é pessoa
FUNCAO_COISA = {'Produção', 'Idealização', 'Concepção'}
_QUALIF = r'(?:\s+(?:musical|artístico|artística|geral|executiva|executivo|cultural|teatral|de teatro|de cinema|de movimento|de arte|vocal|corporal|de produção|de cena|lírico|lírica|de elenco))?'
_FUNC_ALT = '|'.join(sorted(map(re.escape, FUNCOES), key=len, reverse=True))
# a mesma gramática de nome do NOME_RE, para casar o nome logo depois da pista
_NOME_GRP = r"((?:" + TOKEN + r")(?:\s+(?:(?:" + '|'.join(CONECT) + r")\s+)?(?:" + TOKEN + r")){1,3})"
PISTA_ANTES = re.compile(r"\b(?:[oa]s?|d[oa]s?|pel[oa]s?|com\s+[oa]|e\s+[oa])?\s*(" + _FUNC_ALT + r")" + _QUALIF
                         + r"(?:\s+(?:e|,)\s+(?:" + _FUNC_ALT + r")" + _QUALIF + r")?\s+" + _NOME_GRP + r"\b", re.I)
PISTA_DEPOIS = re.compile(_NOME_GRP + r",\s+(" + _FUNC_ALT + r")" + _QUALIF + r"\b", re.I)
PISTA_DE = re.compile(r"\b(dirigid[oa]s?\s+por|direção\s+(?:geral\s+|musical\s+|artística\s+)?de|texto\s+de|dramaturgia\s+de"
                      r"|escrit[oa]\s+por|música\s+de|músicas\s+de|coreografia\s+de|figurinos?\s+de|cenário\s+de|cenários\s+de"
                      r"|cenografia\s+de|iluminação\s+de|trilha\s+sonora\s+de|protagonizad[oa]\s+por|estrelad[oa]\s+por"
                      r"|interpretad[oa]\s+por|adaptação\s+de|tradução\s+de|produção\s+de|idealização\s+de|concepção\s+de"
                      r"|encenação\s+de|encenad[oa]\s+por|composição\s+de|arranjos\s+de|fotos?\s+de|fotografia\s+de)\s+"
                      + _NOME_GRP + r"\b", re.I)
# crédito de foto na legenda ("Imagem: João Caldas", "Fotos: Priscila Prade"):
# quem assina a foto é gente (prova para o JSON-LD de pessoa; não muda a função)
CREDITO_RE = re.compile(r"\b(?:Imagem|Imagens|Foto|Fotos|Crédito|Créditos)\s*:\s*" + _NOME_GRP + r"(?![\w'’\-])")
PISTA_DE_ROTULO = [
    ('dirigid', 'Direção'), ('direção', 'Direção'), ('texto', 'Dramaturgia'), ('dramaturgia', 'Dramaturgia'),
    ('escrit', 'Dramaturgia'), ('música', 'Música'), ('coreografia', 'Coreografia'), ('figurino', 'Figurino'),
    ('cenário', 'Cenografia'), ('cenografia', 'Cenografia'), ('iluminação', 'Iluminação'), ('trilha', 'Música'),
    ('protagonizad', 'Atuação'), ('estrelad', 'Atuação'), ('interpretad', 'Atuação'), ('adaptação', 'Dramaturgia'),
    ('tradução', 'Tradução'), ('produção', 'Produção'), ('idealização', 'Idealização'), ('concepção', 'Concepção'),
    ('encena', 'Direção'), ('composição', 'Música'), ('arranjos', 'Música'), ('foto', 'Fotografia'),
]
QUOTE_RE = re.compile(r'[“"‘\'』«]([^”"’\'»]{2,90})[”"’\'»]')


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:70]


def canonico(nome):
    """Apelido -> nome do verbete (Zé Celso -> José Celso Martinez Corrêa)."""
    return APELIDOS.get(nome.strip().lower(), nome)


def nome_valido(nome):
    if nome.strip().lower() in BLOQUEAR_NOMES:
        return False
    if nome in NOMES_CURTOS:
        return True
    partes = nome.replace('-', ' ').split()
    if len([p for p in partes if p.lower() not in CONECT]) < 2:
        return False
    if partes[0] in PRIMEIRA_FORA:
        return False
    for p in partes:
        if p in BLOQUEIO or p.lower() in LUGARES:
            return False
    if nome.lower() in LUGARES:
        return False
    if len(nome) > 40:
        return False
    return True


def _titulo_caixa_alta(t):
    """Título Com Toda Inicial Maiúscula (era Wix)? Aí maiúscula não é pista
    de nome, e a promoção a tema fica desligada."""
    ws = [w for w in re.findall(r"[A-Za-zÀ-ÿ'’\-]+", t)[1:] if len(w) > 3]
    if len(ws) < 3:
        return True   # curto demais para julgar: não promove
    return sum(1 for w in ws if w[0].isupper()) / len(ws) > 0.5


def extrair_nomes(texto):
    # remove títulos de obras entre aspas — “Assim” "Assim" ‘Assim’
    texto = re.sub(r'[“"‘\'』«][^”"’\'»]{2,90}[”"’\'»]', ' ', texto)
    achados = set()
    for m in NOME_RE.finditer(texto):
        if ANTES_LUGAR.search(texto[max(0, m.start() - 90):m.start()]):
            continue
        n = re.sub(r'\s+', ' ', m.group(1)).strip()
        n = CAUDA_RE.sub('', n)
        partes = n.split()
        # "Teatro de Leo Lama", "Companhia de Maria Clara": o nome é de quem dá
        # nome à casa — apara a casa e fica a pessoa (05/10/2026). Lugar ou
        # instituição em qualquer outra posição ("Teatro Sérgio Cardoso") segue
        # derrubando o nome inteiro: a citação é ao prédio, não à pessoa.
        while len(partes) >= 3 and partes[0] in VETO_TOTAL and partes[1].lower() in CONECT:
            partes = partes[2:]
        if any(p in VETO_TOTAL for p in partes):
            continue
        # apara rótulo de ficha e preposição do início ("Por Bruno Cavalcanti" ->
        # "Bruno Cavalcanti"); artigo no início é título de obra: cai inteiro
        if partes and partes[0].lower() in ARTIGOS_INICIO:
            continue
        ruim = False
        while partes and (partes[0] in BLOQUEIO or partes[0].lower() in CONECT
                          or partes[0].lower() in PREP_PONTA):
            if partes[0] in BLOQUEIO and partes[0] not in FICHA_APARA:
                ruim = True; break
            partes = partes[1:]
        while not ruim and partes and (partes[-1] in BLOQUEIO or partes[-1].lower() in CONECT
                                       or partes[-1].lower() in PREP_PONTA):
            if partes[-1] in BLOQUEIO and partes[-1] not in FICHA_APARA:
                ruim = True; break
            partes = partes[:-1]
        if ruim:
            continue
        n = ' '.join(partes)
        if n and nome_valido(n):
            achados.add(canonico(n))
    # nomes artísticos de uma palavra só (lista curada nas regras): Molière, Cher…
    for nc in NOMES_CURTOS:
        if re.search(r'(?<![\w-])' + re.escape(nc) + r'(?![\w-])', texto):
            achados.add(canonico(nc))
    return achados


# ---- quem a DESCRIÇÃO do episódio apresenta como convidado (auditoria de
# 10/10/2026). Antes todo nome da descrição virava convidado: o metrô "Ayrton
# Senna", Shakespeare, Rita Lee, a "fala de Paulo Gustavo". Agora só conta o
# nome que vem logo depois de um convite ("Isabel Branquinha recebe a diretora
# Rhena de Faria e a dramaturga Sofia Fransolin", "conversa com", "Convidados:")
# ou que está na lista de convidados da descrição; o resto é só mencionado.
_CONVITE = re.compile(r"\b(?:receb(?:e|em|emos|eram|er)|(?:conversa(?:m|mos)?|bate-papo|papo|entrevista(?:m|mos)?)\s+com"
                      r"|convida(?:m|mos)?|convidad[oa]s?)\b", re.I)
# palavras que, entre o convite e o nome, mostram que a frase fala de outra
# coisa ("recebe o elenco do musical Tim Maia", "conversa com ela sobre")
_CONVITE_VETO = {'sobre', 'para', 'de', 'do', 'da', 'dos', 'das', 'com', 'em', 'na', 'no', 'nas', 'nos', 'pelo',
                 'pela', 'que', 'elenco', 'musical', 'espetáculo', 'espetaculo', 'peça', 'peca', 'montagem', 'livro',
                 'filme', 'obra', 'história', 'historia', 'missão', 'missao'}
_MINUSCULA = re.compile(r"^[a-záâãàéêíóôõúüç][a-záâãàéêíóôõúüç\-]*$")
_NOME_INICIO = re.compile(r"^\s*(" + _NOME_GRP + r")(?![\w'’\-])")
_SEP_NOMES = re.compile(r"^\s*(?:,\s*e\s+|,\s*|\s+e\s+)(.*)$", re.S)


def _so_artigo_e_funcao(t, maximo):
    ws = re.findall(r"[^\s,:]+", t)
    return len(ws) <= maximo and all(_MINUSCULA.match(w) and w.lower() not in _CONVITE_VETO for w in ws)


def convidados_descricao(desc):
    """Nomes que a descrição apresenta como convidados, na ordem do texto."""
    texto = re.sub(r'\s*\([^()]*\)', '', desc or '')                 # "(atriz, dramaturga e pesquisadora)"
    texto = re.sub(r'[“"‘\'』«][^”"’\'»]{2,90}[”"’\'»]', ' ¶ ', texto)  # obra entre aspas corta a frase
    saida = []

    def junta(trecho):
        for nm in sorted(extrair_nomes(trecho)):
            if nm not in saida:
                saida.append(nm)

    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        # lista com título: "🎤 CONVIDADOS" e um nome por linha, às vezes
        # seguido do perfil ("Larissa da Matta, @larissadamatta_")
        if re.match(r"^\W*convidad[oa]s?\W*$", linha, re.I):
            vistos = 0
            for seg in linhas[i + 1:]:
                if not seg.strip():
                    continue
                vistos += 1
                m = _NOME_INICIO.match(seg)
                if m and re.match(r"^\s*(?:$|[\u2014\u2013\-|:,@])", seg[m.end():]):
                    junta(m.group(1))
                elif not re.match(r"^\s*[A-ZÀ-Ú][\w'’\-]*\s*$", seg) or vistos > 12:
                    break      # acabou a lista (a linha seguinte é outro título)
            continue
        for g in _CONVITE.finditer(linha):
            # a frase do convite acaba no ponto, no travessão ou no hífen solto
            resto = re.split(r"[.!?;](?:\s|$)|\s[\u2014\u2013]|\s-\s|¶", linha[g.end():g.end() + 300], 1)[0]
            m = NOME_RE.search(resto)
            if not m:
                continue
            antes = re.sub(r"\bno Foyer\b|\bninguém menos que\b", ' ', resto[:m.start()]).strip()
            if not (antes.endswith(':') and len(antes.split()) <= 14) and not _so_artigo_e_funcao(antes, 8):
                continue
            pos = m.start()
            while True:
                mn = _NOME_INICIO.match(resto[pos:])
                if not mn or not extrair_nomes(mn.group(1)):
                    break
                junta(mn.group(1))
                pos += mn.end()
                # o próximo nome vem depois de vírgula ou "e", com artigo e
                # função no meio ("e a dramaturga", "e os atores")
                ms = _SEP_NOMES.match(resto[pos:])
                if not ms:
                    break
                prox = NOME_RE.search(ms.group(1))
                if not prox or not _so_artigo_e_funcao(ms.group(1)[:prox.start()], 3):
                    break
                pos += ms.start(1) + prox.start()
    return saida


def _em_ordem(nomes, texto):
    """Nomes na ordem em que aparecem no texto (quem vem antes no título primeiro)."""
    def pos(n):
        i = texto.find(n)
        return i if i >= 0 else len(texto)
    return sorted(nomes, key=lambda n: (pos(n), n))


def pistas_funcao(texto):
    """{nome: {rótulo: votos}} a partir das pistas do texto."""
    votos = defaultdict(lambda: defaultdict(int))
    for m in PISTA_ANTES.finditer(texto):
        f = m.group(1).lower(); nome = canonico(re.sub(r'\s+', ' ', m.group(2)))
        q = (m.group(0)[len(m.group(0)) - len(m.group(2)) - 40:].lower() if False else m.group(0).lower())
        rot = FUNCOES.get(f, f.capitalize())
        if 'musical' in q.split(nome.lower())[0]:
            rot += ' musical'
        if nome_valido(nome):
            votos[nome][rot] += 2
    for m in PISTA_DEPOIS.finditer(texto):
        nome = canonico(re.sub(r'\s+', ' ', m.group(1))); f = m.group(2).lower()
        if nome_valido(nome):
            votos[nome][FUNCOES.get(f, f.capitalize())] += 2
    for m in PISTA_DE.finditer(texto):
        pista = m.group(1).lower(); nome = canonico(re.sub(r'\s+', ' ', m.group(2)))
        rot = next((r for k, r in PISTA_DE_ROTULO if pista.startswith(k)), None)
        if rot and nome_valido(nome):
            votos[nome][rot] += 1
    return votos


def _dia_brasilia(iso):
    """O dia da publicação em Brasília, igual ao que a página da matéria mostra
    (auditoria de 10/10/2026: cortado do texto em UTC, o que saiu entre 21h e
    23h59 ganhava a data do dia seguinte)."""
    if len(iso) <= 10:
        return iso
    try:
        from zoneinfo import ZoneInfo
        d = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(ZoneInfo('America/Sao_Paulo')).strftime('%Y-%m-%d')
    except Exception:
        return iso[:10]


def main():
    # verbetes que já estão no ar (o mapeamento anterior): quem só é mencionado
    # em descrição de episódio não ganha verbete novo, mas também não perde o
    # que já tem
    try:
        ja_no_ar = set(json.load(open(f'{ROOT}/import/enciclopedia.json')).get('pessoas', {}))
    except Exception:
        ja_no_ar = set()
    materias = json.load(open(f'{ROOT}/import/materias.json'))
    # inclui as matérias publicadas pela Coxia (import/novas) que não estão no índice do Wix
    ja = {m['slug'] for m in materias}
    novas_dir = f'{ROOT}/import/novas'
    # a mesma hora que o build_pages usa para decidir o que já está no ar
    agora_utc = datetime.now(timezone.utc).isoformat()
    agendadas = 0
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
            # matéria agendada ainda não tem página. Citar o nome dela aqui
            # criaria um link para o vazio na página da pessoa — e a
            # enciclopédia entregaria a pauta antes da hora.
            pub = n.get('publishAt') or ''
            if pub and pub > agora_utc:
                agendadas += 1
                continue
            # o corpo vem DIRETO do pacote. Antes a varredura dependia de
            # import/corpo/<slug>.html, que para matéria recém-publicada ainda
            # não existe na hora em que este script roda no deploy — resultado:
            # só o título era lido, e ninguém citado no corpo entrava na
            # enciclopédia (o Pedro notou em 05/08/2026, na matéria do Divine).
            materias.insert(0, {'slug': n['slug'], 'title': n['title'],
                                'author': n.get('author', ''), 'desc': n.get('desc', ''),
                                'iso': _dia_brasilia(n.get('publishAt') or ''),
                                'cat': n.get('cat', ''),
                                '_corpo': n.get('corpo', '')})
    try:
        yt = json.load(open(f'{ROOT}/import/youtube.json'))
    except Exception:
        yt = {'programas': []}

    pessoas = defaultdict(lambda: {'nome': '', 'aparicoes': []})
    por_materia = defaultdict(list)
    por_video = defaultdict(list)
    citacoes = defaultdict(set)   # slug-pessoa -> set(slug-materia) p/ regra dos 2+
    entre_aspas = defaultdict(int)   # "Sweet Charity": nome que vive entre aspas é obra, não gente
    votos = defaultdict(lambda: defaultdict(int))   # slug-pessoa -> {função: votos}
    creditados = set()   # slug de quem assina foto em legenda

    def registra(nome, tipo, papel, titulo, url, data, chave_grupo=None):
        nome = canonico(nome)
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
        # assinatura dupla ("Fulana e Sicrano") são DUAS pessoas, cada uma com seu verbete
        assinantes = [a.strip() for a in autor.split(' e ')] if ' e ' in autor else ([autor] if autor else [])
        for _as in assinantes:
            if _as and _as.lower() not in ('redação foyer', 'redacao foyer') and nome_valido(_as):
                sp = registra(_as, 'materia', 'autor', m['title'], url, m.get('iso', ''))
                if sp:
                    por_materia[m['slug']].append(sp)
                    votos[sp]['Jornalista'] += 1
        corpo_path = f"{ROOT}/import/corpo/{m['slug']}.html"
        texto = m['title'] + '. ' + m.get('desc', '')
        if m.get('_corpo'):
            # formato da Coxia -> texto puro: fora blocos de mídia e marcação
            t = re.sub(r'^(img:|video:|galeria:|botao:|spotify:).*$', ' ', m['_corpo'], flags=re.M)
            t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)
            texto += ' ' + re.sub(r'[*#>|]', ' ', t)
        elif os.path.exists(corpo_path):
            texto += ' ' + re.sub(r'<[^>]+>', ' ', open(corpo_path).read())
        _slugs_autores = {slugify(canonico(a)) for a in assinantes if a}
        for q in QUOTE_RE.findall(texto):
            entre_aspas[slugify(q.strip())] += 1
        for nm, fs in pistas_funcao(texto).items():
            for rot, n in fs.items():
                votos[slugify(nm)][rot] += n
        for mc in CREDITO_RE.finditer(texto):
            nm = canonico(re.sub(r'\s+', ' ', mc.group(1)))
            if nome_valido(nm):
                creditados.add(slugify(nm))
        # QUEM ESTÁ NO TÍTULO É TEMA da matéria, não citação de passagem:
        # ganha verbete direto, sem esperar a segunda citação (Pedro, 05/08/2026).
        # MAS só em título no padrão da casa (caixa de frase). Os títulos da era
        # Wix eram Com Toda Inicial Maiúscula, e ali o extrator pesca fantasma
        # ("Aborda Ausência Paterna" viraria gente); nesses, vale a regra das 2+.
        _temas = set() if _titulo_caixa_alta(m['title']) else {slugify(nm) for nm in extrair_nomes(m['title'])}
        for nome in extrair_nomes(texto):
            sp = slugify(nome)
            if sp and sp in _slugs_autores:
                continue
            papel = 'tema' if sp in _temas else 'citado'
            spp = registra(nome, 'materia', papel, m['title'], url, m.get('iso', ''))
            if spp:
                por_materia[m['slug']].append(spp)
                citacoes[spp].add(m['slug'])

    # ---- episódios: convidados nos títulos E nas descrições; apresentador
    # de cada programa (import/enciclopedia-regras.json, "apresentadores") ----
    APRESENTA = dict(REGRAS.get('apresentadores') or {'Por Bruno Cavalcanti': 'Bruno Cavalcanti'})
    # Nome tirado só da DESCRIÇÃO de um episódio precisa ter primeiro nome
    # conhecido no acervo (quem já aparece em matéria): é da descrição que
    # saíam "Poder Neste", "Caso Lorena", "Ticketmaster Vem" (vistoria 06/10/2026).
    prenomes = {p['nome'].split()[0].lower() for p in pessoas.values()
                if any(a['tipo'] == 'materia' for a in p['aparicoes'])}
    # CONVIDADO do episódio (auditoria de 10/10/2026) é quem está no título,
    # quem a descrição apresenta como convidado (convidados_descricao) e quem
    # está na lista à mão das regras ("convidados"). Os outros nomes da
    # descrição ficam como MENCIONADOS: aparecem no verbete como "citado no
    # episódio", mas não entram no "Com ..." do card nem em "Quem já passou".
    conv_por_video = defaultdict(list)   # videoId -> convidados, título primeiro
    mencoes = defaultdict(set)           # slug-pessoa -> vídeos em que só é mencionada
    # o nome do programa no título não é gente ("Coxixo de Coxia Temporalmente Vivos")
    nomes_progs = sorted({p['nome'].split(' \u2014 ')[0] for p in yt.get('programas', [])}, key=len, reverse=True)
    for prog in yt.get('programas', []):
        nome_prog = prog['nome'].split(' — ')[0]
        apres = APRESENTA.get(nome_prog)
        sp_apres = slugify(canonico(apres)) if apres else None
        for v in prog.get('videos', []):
            desc = v.get('descricao') or ''
            texto_ep = v['titulo'] + '. ' + desc
            tit = v['titulo']
            for np_ in nomes_progs:
                tit = re.sub(re.escape(np_), ' | ', tit, flags=re.I)
            # No título, convidado é quem vem depois de "com" ou "por" ("Rainha
            # Cult com Gilda Nomacce", "Malu por Yara de Novaes"); o resto é a
            # peça ou a canção ("Passeio Cênico", "Força do Maranhão"). Título
            # sem "com": vale quem a descrição também apresenta como convidado
            # ("Coxixo de Coxia - A Viagem do Jilo" recebe Giba Freitas), ou o
            # título inteiro quando a descrição não diz quem veio. "Com" que só
            # credita o apresentador ("... no Astro em Cena - Com Neusa Romano")
            # não conta.
            conv_desc = convidados_descricao(desc)
            nomes_tit, tem_com = [], False
            for seg in re.split(r"\s+-\s+|\s*[|\u2013\u2014?!]\s*|\s{2,}", tit):
                mc = re.search(r"\b(?:com|por)\s+", seg, re.I)
                if mc:
                    depois = _em_ordem(extrair_nomes(seg[mc.end():]), seg)
                    if depois and all(slugify(canonico(n)) == sp_apres for n in depois):
                        continue
                    tem_com = True
                    nomes_tit += [n for n in depois if n not in nomes_tit]
            if not tem_com:
                nomes_tit = _em_ordem(extrair_nomes(tit), tit)
                if conv_desc:
                    nomes_tit = [n for n in nomes_tit if n in conv_desc]
            # nome que a descrição põe entre aspas é a peça, não o convidado
            # ("Com Elton Towersey - Tom Jobim O Musical")
            obras = ['-' + slugify(q) + '-' for q in QUOTE_RE.findall(desc)]
            nomes_tit = [n for n in nomes_tit if not any('-' + slugify(n) + '-' in o for o in obras)]
            convidados = []
            for nm in nomes_tit + conv_desc + CONVIDADOS_MANUAIS.get(v['id'], []):
                nm = canonico(nm)
                if nm not in convidados:
                    convidados.append(nm)
            mencionados = [nm for nm in _em_ordem(extrair_nomes(desc), desc)
                           if nm not in convidados and (nm in NOMES_CURTOS or nm.split()[0].lower() in prenomes)]
            for nm, fs in pistas_funcao(texto_ep).items():
                for rot, n in fs.items():
                    votos[slugify(nm)][rot] += n
            for nome, papel in [(n, 'convidado') for n in convidados] + [(n, 'mencionado') for n in mencionados]:
                if sp_apres and slugify(canonico(nome)) == sp_apres:
                    continue
                sp = registra(nome, 'episodio', papel, f"{nome_prog}: {v['titulo']}",
                              v['url'], v.get('quando', ''))
                if sp:
                    por_video[v['id']].append(sp)
                    if papel == 'convidado':
                        if sp not in conv_por_video[v['id']]:
                            conv_por_video[v['id']].append(sp)
                    else:
                        mencoes[sp].add(v['id'])
            if apres:
                sp = registra(apres, 'episodio', 'apresenta', f"{nome_prog}: {v['titulo']}",
                              v['url'], v.get('quando', ''))
                if sp:
                    por_video[v['id']].append(sp)
                    votos[sp]['Apresentador' if not apres.endswith('a') else 'Apresentadora'] += 1

    # ---- regra de corte: citação única não vira verbete; nome que vive
    # entre aspas é título de obra (a não ser que o texto diga que é gente) ----
    # Mencionado na descrição de episódio vale como citado: sozinho, uma vez
    # só, não cria verbete; somado a matérias e a outros episódios, conta para
    # a regra das 2+. Verbete que já estava no ar não é apagado por isso.
    finais = {}
    descartados_obra = []
    for sp, p in pessoas.items():
        papeis = {a['papel'] for a in p['aparicoes']}
        n_asp = entre_aspas.get(sp, 0)
        eh_gente = bool(votos.get(sp)) or bool(papeis - {'citado', 'tema', 'mencionado'})
        if n_asp and not eh_gente and n_asp * 2 >= len(p['aparicoes']):
            descartados_obra.append(p['nome'])
            continue
        if (papeis - {'citado', 'mencionado'} or len(citacoes.get(sp, ())) + len(mencoes.get(sp, ())) >= 2
                or (sp in ja_no_ar and sp in mencoes)):
            # dedup de aparições iguais
            vistos, aps = set(), []
            for a in sorted(p['aparicoes'], key=lambda x: x.get('data', ''), reverse=True):
                k = (a['tipo'], a['url'])
                if k in vistos:
                    continue
                vistos.add(k)
                aps.append(a)
            fs = sorted(votos.get(sp, {}).items(), key=lambda x: -x[1])
            finais[sp] = {'nome': p['nome'], 'aparicoes': aps,
                          'funcoes': [f for f, _ in fs[:3]]}
            # o texto dá ofício ("a atriz Fulana", "dirigido por Fulano"), a
            # pessoa assina matéria ou foto, ou apresenta programa: é gente. O
            # site só dá JSON-LD de pessoa a quem tem essa prova ou bio
            # confirmada; "Kinky Boots" ganhava Person com função "Produção"
            # (auditoria de 10/10/2026)
            if sp in creditados or any(r not in FUNCAO_COISA for r in votos.get(sp, {})):
                finais[sp]['gente'] = True

    por_materia = {k: sorted({s for s in v if s in finais}) for k, v in por_materia.items()}
    por_materia = {k: v for k, v in por_materia.items() if v}
    por_video = {k: sorted({s for s in v if s in finais}) for k, v in por_video.items()}
    por_video = {k: v for k, v in por_video.items() if v}
    conv_por_video = {k: [s for s in v if s in finais] for k, v in conv_por_video.items()}
    conv_por_video = {k: v for k, v in conv_por_video.items() if v}

    # moderação: verbetes excluídos pelo chefe na Coxia
    try:
        _exc = set(json.load(open(f'{ROOT}/import/enciclopedia-excluidos.json')).get('slugs', []))
    except Exception:
        _exc = set()
    if _exc:
        finais = {k: v for k, v in finais.items() if k not in _exc}
        por_materia = {k: [x for x in v if x in finais] for k, v in por_materia.items()}
        por_materia = {k: v for k, v in por_materia.items() if v}
        por_video = {k: [x for x in v if x in finais] for k, v in por_video.items()}
        por_video = {k: v for k, v in por_video.items() if v}
        conv_por_video = {k: [x for x in v if x in finais] for k, v in conv_por_video.items()}
        conv_por_video = {k: v for k, v in conv_por_video.items() if v}
        print(f'moderação: {len(_exc)} verbete(s) excluído(s) pelo chefe')

    saida = {'pessoas': finais, 'porMateria': por_materia, 'porVideo': por_video,
             'convidadosPorVideo': conv_por_video}
    json.dump(saida, open(f'{ROOT}/import/enciclopedia.json', 'w'),
              ensure_ascii=False, indent=1)
    if descartados_obra:
        print(f'obras entre aspas que não viram verbete: {len(descartados_obra)} (ex.: ' + ', '.join(descartados_obra[:12]) + ')')
    print(f'pessoas com verbete: {len(finais)}'
          + (f' · {agendadas} matéria(s) agendada(s) fora, ainda sem página' if agendadas else ''))
    top = sorted(finais.items(), key=lambda x: len(x[1]['aparicoes']), reverse=True)[:25]
    for sp, p in top:
        print(f"  {len(p['aparicoes']):4d}  {p['nome']}")


if __name__ == '__main__':
    main()
