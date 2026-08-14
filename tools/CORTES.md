# O que os checadores derrubaram

Registro vivo dos erros que a checagem pegou antes de a matéria chegar à mesa.

**Para que serve.** Sem este arquivo, cada rodada começa do zero: o checador
pega o erro, a matéria sai limpa, e no dia seguinte outro redator comete o
mesmo erro. Com ele, o padrão aparece. Se "preço desatualizado" for o item
que mais se repete, o conserto não é pedir mais atenção ao redator: é virar
regra no manual (abrir a tabela oficial antes de escrever qualquer valor) ou
trava no `audita_pauta.py`.

**Como usar, ao fim de cada rodada.** Acrescente a rodada NO TOPO, com uma
linha por corte que valeu a pena. Não registre vírgula fora do lugar: só o
que teria enganado o leitor, envergonhado a casa ou custado dinheiro a
alguém. Uma vez por semana, leia a coluna do tipo e veja o que se repete.

**Os tipos**, para dar para contar depois: `número desatualizado`,
`superlativo sem fonte`, `data errada`, `aspa não literal`, `norma revogada`,
`atribuição errada`, `link quebrado`, `invenção`, `insinuação sem fonte`,
`@ não confirmado`, `direito de foto`.

---

## 14/08/2026, o quente do dia: quatro matérias assinadas Pedro Amaral

Primeira rodada da semana com a esteira completa: pauteiro, redatores, titulador,
dois checadores independentes, dois revisores de leitura fria, chefe. Onze agentes
em quatro matérias. **De novo o portão mecânico não pegou nada do que segue** — e
desta vez a leitura fria pegou um defeito que a checagem, por definição, não podia
pegar.

| Tipo | O que caiu | Por quê | Matéria |
|---|---|---|---|
| `invenção` | "Barnabé Salomé", nome da intérprete | Existe num único parágrafo de um único documento, o release da SMC. A atriz é **Bárbara Salomé**, nome que está na ficha da dona da obra, no Infoteatro, no Sesc e no segundo texto da própria Prefeitura | Cacilda Becker |
| `atribuição errada` | "Não Aprendi **a** Dizer Adeus" | A companhia batizou sem o segundo "a". A grafia com "a" é a que o release erra no quinto parágrafo | Cacilda Becker |
| `data errada` | "O Cade liberou a operação em 1º de agosto" | 1º de agosto é a data da NOSSA matéria. A decisão é o Despacho SG nº 899, de 8 de julho, publicado no DOU em 9 | Paramount-Warner |
| `número desatualizado` | "US$ 7 milhões por dia" | É caracterização do Deadline, não número de contrato. O contrato fixa US$ 0,00277778 **por ação** por dia; com as ações do 10-Q dá US$ 6,97 milhões | Paramount-Warner |
| `data errada` | Datas do julgamento sem o ano | São de **2027**. Só o início da produção de provas, 17/08, é de 2026 | Paramount-Warner |
| `número desatualizado` | "A ocupação caiu 10,94%" | A coluna da Broadway League é em **pontos percentuais** (81,79% → 70,85%). Em termos relativos seria 13,4% | SIX |
| `invenção` | O cenário de 170 dias e US$ 1,19 bilhão | Aritmeticamente certo e materialmente impossível: o balanço da própria Warner registra o compromisso de não fechar antes de 1º/06/2027. Piso documentado: 244 dias | Paramount-Warner |
| `invenção` | "Sessenta horas de tribunal" | Ignorava as duas pausas de quinze minutos que a frase anterior do mesmo texto cita. São 54 | Paramount-Warner |
| `insinuação sem fonte` | "Bruxelas cobrou contrapartidas" | Zero ocorrência de Comissão Europeia nas nove fontes | Paramount-Warner |
| `atribuição errada` | Renée Fleming entre quem cancelou por causa de Trump | O comunicado do próprio Kennedy Center atribui a saída dela a "a scheduling conflict", e ela não respondeu ao pedido de comentário | Kennedy Center |
| `superlativo sem fonte` | "Dinheiro público para restaurar prédio de arte nos EUA é rotina" | **A premissa vinha de matéria nossa, e o link a desmentia**: os US$ 1,75 mi de Pittsburgh são doação da Mellon Foundation, fundação privada | Kennedy Center |
| `atribuição errada` | O placar de 20 a 3 atribuído só à inscrição | A NBC, única fonte com o número, diz que valeu para a inscrição **e** para o batismo da praça. O fechamento foi votado antes, sem placar em nenhuma das sete | Kennedy Center |
| `insinuação sem fonte` | "Todo indicado por Donald Trump", só na legenda do Instagram | A NBC derruba no mesmo parágrafo do placar: os três votos contrários são de membros natos do Congresso | Kennedy Center |
| `atribuição errada` | Aspa traduzida creditada à NPR | A NPR não a tem. Está em Playbill e Deadline | Kennedy Center |
| `link quebrado` | "A ficha está publicada no site da Cia. Mungunzá" | O link ia para uma matéria nossa. Mandava o leitor para o lugar errado | Cacilda Becker |
| `invenção` | "o Canadá" na estreia do filme | Nenhuma fonte lida o nomeia. Playbill escreve "cinemas around the U.S."; "domestic" é jargão, não fato | SIX |
| `atribuição errada` | Sessões com Libras **e** audiodescrição na mesma noite | Não era esta leva, mas o mesmo padrão: recursos que se revezam descritos como coexistentes | (padrão) |

**Padrões novos desta leva:**

- **O defeito que só a leitura fria pega: o pronome que aponta para o contrário.** Sob
  o intertítulo "O nome oficial da casa fica como está" vinha "em dezembro de 2025 o
  conselho tinha feito exatamente isso". O fato estava certo, a fonte estava certa, e
  o checador não tinha por que parar ali. É defeito de leitura, não de apuração, e
  nenhuma outra onda o alcança.
- **A informação do título enterrada no fim do texto.** "Não há data no Brasil" está no
  `title` do SIX e só aparecia no 19º parágrafo. O leitor daqui atravessava a matéria
  sem saber que não pode assistir. Título e corpo têm de concordar na **ordem**, não
  só no fato.
- **Número que a própria matéria precisa desmontar no parágrafo seguinte** é número que
  a apuração encontrou, não que o leitor precisa. Foi assim que caíram as "14,7 semanas
  de Lena Horne".
- **A matéria que cresce na leitura fria.** O Paramount foi de 879 para 926 palavras
  porque sete traduções de jargão custaram mais do que os cortes de cifra renderam.
  Nem toda onda 3 encurta: quando o defeito é vocabulário, cortar prosa deixa o texto
  mais curto e mais difícil.
- **Segurar um número que o título já entregou não cria suspense, cria atrito.** O
  Paramount adiava a cifra até a palavra 190 com um "cada data dessa agenda tem preço".
- **A conta certa com a premissa impossível.** Os 170 dias fechavam na aritmética e não
  podiam existir no mundo. Refazer a conta não teria pego; foi preciso abrir o balanço.
- **A premissa que vem do próprio acervo e se desmente ao ser aberta.** O pior tipo,
  porque o redator confia no link como confiaria numa fonte externa, e ninguém reabre
  matéria da casa para checar matéria da casa.

## 11/08/2026, títulos de alto alcance e a onda 2 das quinze

Rodada de duas metades. Primeiro seis Tituladores reescreveram 26 títulos que
passavam de 90 caracteres; depois três checadores independentes rodaram a onda 2
nas quinze matérias de 08/08, que estavam na mesa sem nenhuma checagem. **De novo
o portão mecânico não pegou nada do que segue.** Um dos cortes é de um título que
os próprios Tituladores tinham acabado de escrever.

| Tipo | O que caiu | Por quê | Matéria |
|---|---|---|---|
| `insinuação sem fonte` | O título "o 19 de setembro **é** comemorado sem o adjetivo da lei" | Afirma prática geral. O contraexemplo estava na própria lista de fontes: comemoração de 18/09/2018 da Secretaria Municipal da Pessoa com Deficiência de SP, com o nome legal inteiro. O corpo dizia "costuma"; o título perdeu a palavra ao caber no teto | Dia Nacional do Teatro Acessível |
| `link quebrado` | O artigo do CELACC/ECA-USP, e tudo que só ele sustentava | 503 em todos os clientes, host inteiro fora do ar, inclusive no espelho paineira.usp.br. Não é 403 de robô nem 200 falso | Willi Ninja |
| `aspa não literal` | Uma aspa do próprio Willi Ninja no documentário | Vinha só da fonte que caiu. Aspa que não se relocaliza não fica de pé, mesmo quando ninguém duvida dela | Willi Ninja |
| `invenção` | "a casa fundada no Harlem" | Nenhuma fonte diz isso. O Harlem é a origem do voguing, meio século antes; Willi Ninja é do Queens, e Livingston só diz "founded in the mid-1980s" | Willi Ninja |
| `número desatualizado` | "o passivo total **passava de** R$ 20 milhões" | O Metrópoles escreve, duas vezes, "as dívidas estão acumuladas em R$ 20 milhões". Num pacote sobre dívida, esse "mais" não se inventa | Dulcina de Moraes |
| `direito de foto` | A identificação da atriz na legenda da capa | O índice iconográfico da dissertação, p. 106 do PDF, chama a foto de "Júlio Gouveia ensaiando com **Emília**": nomeia a personagem. Quem nomeia a atriz é a descrição do Commons, e o Teledramaturgia registra outra intérprete no período | Lúcia Lambertini |
| `atribuição errada` | As sessões de Chico Simões com Libras **e** audiodescrição | Os recursos se revezam: Libras em 20 e 27, AD em 21 e 28. Erro de acessibilidade numa matéria sobre patrimônio | Mamulengo |
| `número desatualizado` | 3.589 e 3.554 registros na função ator/atriz | A base do MTE foi atualizada depois da apuração. A contagem de hoje é 3.605 e 3.572, e bate com o relatório oficial | Dia do Artista de Teatro |
| `atribuição errada` | "Brooks nunca tinha dirigido nada" | O AFI sustenta estreia na direção de **longa**. E faltava que Wilder já aparecera em Bonnie e Clyde, do mesmo 1967 | Gene Wilder |
| `atribuição errada` | "uma terceira campanha foi montada em 2023" | A fonte é de 14/08/2022 e diz "está prevista una nueva campaña", com licenças protocoladas. Pedido não é obra feita | García Lorca |
| `atribuição errada` | "o Bustanoby's" | O Evening Star nomeia o homem e o endereço, não uma casa com esse nome | Rudolph Valentino |
| `superlativo sem fonte` | "o prédio que ela levantou" / "o prédio que ela pagou" | Nenhuma fonte diz que Dulcina bancou o edifício. O que a Agência Câmara sustenta é que ela fundou a faculdade e o teatro | Dulcina de Moraes |
| `insinuação sem fonte` | "a faculdade continuava fechada" | Nenhuma das quinze fontes afirma isso | Dulcina de Moraes |
| `atribuição errada` | O lide dizia sem atribuir que o verde de teatro "não era tingido, era pintado" | Tem uma origem só, a RTS, e nenhuma das outras seis fontes. Passou a vir atribuído | Verde dá azar |
| `atribuição errada` | "tratou do assunto com o historiador Pastoureau" | A RTS não o entrevistou: cita France Inter e o livro dele | Verde dá azar |
| `número desatualizado` | "três entradas, de 1135, 1572 e 1575" no CNRTL | São três itens numerados e **quatro datas**: o item 3 se abre em a) 1575 e b) 1680. Numa matéria de etimologia a lista datada é a prova | Foyer |
| `link quebrado` | A chamada de temporada de 2022 do Sesc, em `fontes` | Abre, mas não sustenta frase nenhuma. Numa matéria perene isso convida o próximo editor a tomar 2022 por programação corrente | Jofre Soares |
| `atribuição errada` | O aposto "Noronha, **o pai**" | A ficha diz só "Jofre Soares / Noronha" | Jofre Soares |
| `norma revogada` | Meia cota do regulamento: "20 espaços mais 1% do excedente" | São 20 espaços **e** 20 assentos. E a aspa estava no art. 49, § 3º, **f**, sem o parágrafo citado | Libras e audiodescrição |
| `invenção` | "a MITsp teve três espetáculos internacionais" com o recurso | Tem mais. História da Violência e Vigiada e Punida seguem o mesmo padrão | Libras e audiodescrição |

**Padrões novos desta leva**, todos de família nova:

- **título mais curto que o corpo vira título mais categórico que o corpo.** Quem
  titula corta palavra, e a palavra que qualifica é a mais fácil de cortar: parece
  enfeite e é o que sustenta a frase. Virou regra 8 do Titulador, com um detalhe que
  veio do próprio agente: a qualificação tem de caber **nos 60 primeiros
  caracteres**, senão o snippet truncado devolve a afirmação absoluta.
- **a contagem sem régua.** "Quatro montagens no Brasil" é falso; "quatro montagens
  profissionais no Brasil, de 1965 a 2014" é verdadeiro. E "quatro montagens
  profissionais", sem país, é falso na direção contrária. Régua incompleta erra dos
  dois lados.
- **o Instagram é porta dos fundos do fato.** Três legendas e um `instagram.titulo`
  carregavam fatos que o checador tinha acabado de corrigir no corpo. Quem corrige
  o corpo tem de varrer o bloco `instagram` no mesmo movimento.
- **a fonte que sai leva as frases dela junto.** Quando o artigo da USP caiu, não
  bastou tirar a URL: saíram a tese sobre Paris Is Burning, a leitura do Vogue de
  Madonna, o parágrafo de remuneração e uma aspa. Fonte que sai sem levar o que
  sustentava deixa o texto órfão e ninguém percebe.
- **a URL órfã dentro de `fontes` é bomba, não enfeite.** No 19 de setembro, a URL
  que ninguém tinha aberto era justamente o contraexemplo que derrubava o título.
- **o 503 real do servidor de origem**, sexto sabor de bloqueio: não abre para
  cliente nenhum, nem com navegador, nem no espelho institucional. Diferente do 403
  de robô e do 200 falso.
- **a ressalva do chefe derrubada de novo.** Três nesta rodada: o 200 falso do Sesc
  (não reproduz), a diferença de sete linhas na planilha do MTE (o ministério
  corrigiu) e a suspeita sobre "calunga" no mamulengo (a matéria já estava certa e
  não havia o que cortar). Continua valendo: ressalva é pista, não ordem.

## 06/08/2026, banco de conteúdo perene: 10 matérias da Redação Foyer

A maior leva já checada pela casa. Dez matérias sem data para sair, um checador
independente exclusivo por matéria, um revisor de leitura fria por matéria, e
duas listas que precisaram de três e cinco rodadas para fechar. **Mais de 150
cortes.** Nenhum dos erros graves foi pego pelo portão mecânico: todos vieram de
alguém abrindo a fonte outra vez.

| Tipo | O que caiu | Por quê | Matéria |
|---|---|---|---|
| `invenção` | "Em 1935, em Moscou, assistiu a uma demonstração de Mei Lanfang" | Nem Moscou nem 1935 aparecem em fonte nenhuma do pacote | Quarta parede |
| `atribuição errada` | A frase mais famosa de Brecht sobre a quarta parede | É formulação do tradutor Willett (1964), e a redação declarou não ter aberto a tradução | Quarta parede |
| `atribuição errada` | O capítulo do tratado de Diderot | Lojkine localiza a passagem em "De l'intérêt", não em "De la décoration". O título da página puxou o redator para o capítulo errado | Quarta parede |
| `aspa não literal` | O Prêmio Questão de Crítica "não existe mais" | O editorial diz "decidimos não mais fazê-lo, **pelo menos por um tempo**" e termina esperando "ainda proporcionar outros encontros". Suspensão virou encerramento | Prêmios de teatro |
| `superlativo sem fonte` | O Shell como "o mais longevo em atividade" | A própria matéria dizia, dois parágrafos abaixo, que a APCA nasceu em 1956. O texto se contradizia dentro de si | Prêmios de teatro |
| `atribuição errada` | A descrição da função do designer de luz atribuída ao sindicato | É o anexo do **Decreto 82.385/1978**, que um sindicato nomeia e outro reproduz sem crédito | Designer de luz |
| `superlativo sem fonte` | O lide inteiro | Nenhuma das 12 fontes usa a expressão "designer de luz" | Designer de luz |
| `atribuição errada` | Entrevista de 2013 creditada ao blog que a arquiva | Ela saiu em outro veículo; o blog é o arquivo | Cenógrafo |
| `número desatualizado` | "362 e 361 lugares" | Os números excluíam assentos de PCD, cadeirante, cão-guia e obeso | Cenógrafo |
| `data errada` | A programação de agosto escrita no passado | Matéria fechada em 6/8: dois dos eventos ainda não tinham acontecido | Teatro Guaíra |
| `número desatualizado` | R$ 23 milhões e a data da ordem de início | As páginas oficiais devolvem 404 e não têm cópia no Internet Archive. Numa perene, número que o leitor não confere não fica | Theatro São Pedro |
| `número desatualizado` | 650 lugares | A tabela de valores que a própria fundação publicou para 2026 dá 616 | Theatro São Pedro |
| `atribuição errada` | O governo do Maranhão chamaria o Arthur Azevedo de segundo mais antigo do país | O site oficial da casa não faz essa conta: diz que foi o quarto construído em São Luís entre 1780 e 1816. A conta vive na imprensa local | Teatros mais antigos |
| `invenção` | "Interditado em 2010 por risco de desabamento", 475 lugares e o telão | A interdição foi do Ministério Público após vistoria do telhado. Os outros dois não estão em fonte alguma | Teatros mais antigos |
| `atribuição errada` | Prêmio Shell e Prêmio APCA no item da Elza | A APCA publica o histórico: os prêmios são de **outros espetáculos dos mesmos criadores**. Estavam colados na matéria errada | 10 musicais |
| `invenção` | O coro de crianças dos Saltimbancos, com quatro nomes próprios | Nenhuma fonte. Inventado inteiro | 10 musicais |
| `invenção` | Os invasores agrediram os artistas "em cena" | A fonte diz que a invasão foi depois da apresentação. Dramatização | 10 musicais |
| `atribuição errada` | As entidades de teatro votam nos membros da comissão do Fomento | O art. 11 da Lei 13.279/2002 diz que elas **apresentam listas**; quem **vota** são os proponentes inscritos. Erro de leitura da lei | Pauta em teatro público |
| `atribuição errada` | "e é analisada em rodadas periódicas", atribuído ao edital | O edital não fixa periodicidade nenhuma. Quem fala em análise periódica é a assessoria. E "rodadas" era palavra nossa: rodada é lote fechado, e documento nenhum estabelece isso | Pauta em teatro público |
| `número desatualizado` | Um edital de 2022 escrito no presente | Numa matéria feita para ficar meses no ar | Pauta em teatro público |

### Os padrões novos desta leva

**1. A ressalva do chefe é palpite, e o palpite estava errado oito vezes.**
Oito ressalvas minhas foram derrubadas por checadores que preferiram abrir a
fonte a obedecer o chefe. Duas afirmavam que um dado só existia em fonte
secundária quando havia inventário oficial; uma dizia que os sites de um
governo estadual estavam fora do ar por período eleitoral (não estavam: as dez
páginas abriram e sustentaram quase toda a checagem); uma citava uma
enciclopédia que não diz o que eu disse que ela diz e nem é sobre o assunto;
uma mandava conferir se saíra edição nova de um prêmio quando o desatualizado
era o tempo verbal; uma dava por não localizado um prêmio que estava no texto e
era justamente o que fazia o item cumprir o critério da matéria.
**Virou regra de manual: `chefe.ressalvas` é material a conferir, não ordem a
cumprir.**

**2. O bloco `chefe` envelhece com a checagem, e ninguém reescrevia.**
Descoberto pela leitura fria dos prêmios. O parecer chamava de achado o que o
checador tinha derrubado, e três das cinco ressalvas descreviam um rascunho que
o editor humano nunca veria. Ressalva é o que o humano resolve na mão, na
Coxia: **ressalva sobre texto inexistente é trabalho falso mandado para a
mesa.** Virou obrigação do chefe reler e reescrever o bloco depois da onda 2.

**3. Busca não é fonte.** A lista dos teatros foi reprovada não pelos fatos, que
eram verdadeiros, mas pela lista de fontes: link morto, link de ano errado que
contradizia o texto para quem abrisse, e casas inteiras sem fonte. A causa foi
instalar em `fontes` URL que apareceu na busca e ninguém abriu.

**4. Acervo próprio não é fonte do pacote.** Três fatos de duas matérias
diferentes estavam pendurados em matérias nossas. Uma delas nem endereço externo
tem: quem abrisse o link para conferir encontrava só nosso YouTube e Spotify.

**5. Um 403 tem quatro sabores, e só um deles é morte.** Bloqueio de bot (abre
com User-Agent de navegador), WAF que recusa igual em qualquer cliente, 200
falso que devolve a home no lugar do conteúdo, e 404 de verdade. Uma ordem minha
foi recusada com razão por um repórter que descobriu que o domínio alternativo
redirecionava para o mesmo WAF.

**6. Nomear a mesma régua de dois jeitos.** Numa lista cujo argumento é que o
campeão muda conforme a conta, escrevi "ordena por ano de fundação" onde o
critério declarado era "o ano em que a casa abriu as portas pela primeira vez".
O erro só aparece onde as duas leituras divergem — e divergiam quatro linhas
acima, numa casa de 1819 que substituiu outra de 1770. Onde eu estava olhando,
coincidiam.

**7. O erro de vizinhança.** A reorganização da leitura fria pôs o Prêmio Sesc
dentro do parágrafo de um programa estadual, a três parágrafos de onde o Sesc é
apresentado. Não é erro de fato: é erro de posição, e o leitor corrido conclui
errado. Quem remonta parágrafos tem de reler as fronteiras.

**8. O editor humano continua sendo o único da esteira sem portão.** Registrado
em 04/08 e confirmado agora, com uma variação: a única ocorrência de travessão
da leva inteira estava numa `chefe.ressalvas`, campo que o portão não olhava.
**Trava que só olha onde a casa já se comporta bem não é trava.** O portão passou
a varrer `chefe.parecer` e `chefe.ressalvas` (como aviso, não trava).

### O que a leitura fria mediu, nas dez

Todas cortaram **exatamente 10%** pela régua do portão, e em todas o ritmo
melhorou junto, sem que ninguém fosse atrás disso. **Gaveta em sete das dez**, e
a maioria confessava no próprio intertítulo, com uma vírgula ou um "e"
amarrando dois assuntos sem relação: "Indicado, vencedor, e o prêmio que
parou", "Onde se aprende, e quem premia", "Luz, figurino e o nome do prêmio",
"Chamada pública, cessão e aluguel", "O que o Fomento paga, e o que ele não
reserva" — esta última um intertítulo inteiro para reenunciar o parágrafo de
cima. **Nenhum dos dez fechos terminava em link:** essa trava funciona sozinha.
Mas seis eram resumo do lide, um era tautologia e um tinha um "portanto" que não
decorria de nada.

---

## 05/08/2026, checagem independente: perfil de Gui Ventura (Gil – Andar com Fé)

| Tipo | O que caiu | Onde estava |
|---|---|---|
| `data errada` | "A montagem foi anunciada em junho" — o anúncio da montagem é de fevereiro de 2026; o que saiu em junho foi o nome do protagonista. O link interno também apontava para a matéria errada | `quem-e-gui-ventura-gil-andar-com-fe` |
| `data errada` | "Nove anos depois, foi ele o escolhido": a aspa é de 07/08/2017 e a escolha foi anunciada em 16/06/2026, oito anos e dez meses depois. Nove anos só fecha com a estreia, em 20/08/2026 | idem |
| `invenção` | "Ventura interpreta Gil em fases diferentes da vida": nenhuma fonte diz isso. O release diz que quem aproxima as fases e faz o Gil jovem conversar com o Gil do futuro é o Tempo-Rei | idem |
| `superlativo sem fonte` | Título afirmava "escolhido entre mais de 800 candidatos" como fato apurado. O número é da produção e nenhuma fonte com apuração própria o confirma: virou "que a produção escolheu entre mais de 800 candidatos", com atribuição também no corpo | idem |
| `atribuição errada` | "conforme o perfil profissional que o ator mantém no Elenco Digital" para as três temporadas de Madame Satã: a informação está no release oficial, com os anos 2015 a 2018. A atribuição fraca escondia uma fonte melhor | idem |
| `atribuição errada` | "Em entrevista ao Correio Braziliense": a entrevista está no blog Próximo Capítulo, do jornal, assinada por Patrick Selvatti | idem |
| `número desatualizado` | "Classificação indicativa: 12 anos" sozinho: o release da produção diz 12 anos e a página oficial do Teatro Santander diz "livre, menores de 12 anos acompanhados". Duas fontes oficiais divergindo entre si, e o serviço passou a trazer as duas com a origem de cada uma | idem |
| `@ não confirmado` | @guiventuraoficial estava marcado como não confirmado por falta de checagem: o handle está declarado pelo próprio ator no perfil dele no Elenco Digital. Confirmado e acrescentado @miguelfalabellareal, que faltava | idem |

**O padrão desta checagem:** três releases da MESMA assessoria, sobre o MESMO
espetáculo, com dados diferentes de duração e de número de artistas. Release
não é documento estável: quando houver mais de um, é preciso datar cada um e
usar o mais recente, dizendo qual foi. O redator acertou a escolha e errou a
justificativa que escreveu no campo `checagem`, o que é quase pior: a
justificativa é o que o próximo checador lê.


## 05/08/2026, fim da tarde: a foto certa no git e a errada na tela

O Pedro pediu a troca da capa da Corrida dos Bichos, a troca foi feita, eu
conferi na branch e disse que estava resolvido. Ele voltou com a captura de
tela mostrando o retrato do diretor ainda lá. **Ele estava certo e eu estava
errado sobre o que significa "verificar".**

| Tipo | O que era | O que se achou | Matéria |
|---|---|---|---|
| `direito de foto` | Still oficial gravado POR CIMA do arquivo antigo, com o mesmo nome | Navegador guarda imagem pelo NOME do arquivo. Conteúdo novo em nome velho continua servindo o cache, e a Coxia mostrava a foto antiga com o crédito novo. Arquivo renomeado; o nome antigo saiu do repositório | Corrida dos Bichos |

**As duas regras que entraram no manual por causa disto:**

1. **Trocar foto é RENOMEAR, nunca sobrescrever.** Nome novo, campo `img`
   apontando para ele, arquivo antigo fora do repositório.
2. **Conferir no git não é conferir na tela.** Eu rodei `git show` na branch,
   vi os bytes certos e declarei resolvido. O que manda é o que aparece para
   o editor humano, e entre o repositório e a tela dele existe cache.

E uma terceira, da mesma rodada, sobre como a foto errada foi parar ali:
**um 403 não é "não existe foto de divulgação"**. A página de imprensa da
Amazon MGM recusou o primeiro acesso e eu caí direto para Creative Commons.
A página da Amazon Brasil abre normalmente e tinha cinco stills com a
fotógrafa creditada. Esgotar as portas oficiais vem antes de rebaixar a
origem da imagem.

---

## 05/08/2026, à tarde: a porta dos fundos virou trava

Sétima ocorrência em dois dias, e desta vez o Pedro pegou antes de qualquer
agente. Ele viu que a matéria da **Corrida dos Bichos** estava ilustrada com
retrato do diretor em vez de imagem do filme, e mandou trocar. Ele tinha
razão e o manual concorda: divulgação oficial da própria produção é a
PRIMEIRA origem aceita, e a capa só não era isso porque a página de imprensa
da Amazon MGM devolvia 403 na primeira tentativa. A página da Amazon Brasil
abre normalmente e tem os stills com a fotógrafa creditada.

| Tipo | O que era | O que se achou | Matéria |
|---|---|---|---|
| `direito de foto` | Capa com retrato do diretor de 2012, em Creative Commons | Existe still oficial de divulgação, com Grazi Massafera e Rodrigo Santoro, fotografado por Laura Campanella, na página de imprensa da Amazon Brasil. Trocado; a nota subiu de 8 para 9 | Corrida dos Bichos |
| `atribuição errada` | Trocada a capa, a linha 📷 da legenda do Instagram continuou creditando a foto ANTIGA | **A porta dos fundos pela sétima vez em dois dias.** Desta vez virou trava no portão no mesmo dia | Corrida dos Bichos |

**A TRAVA, e o erro que eu cometi ao escrevê-la.** A primeira versão exigia
que `imgCredito` e a linha 📷 fossem texto IDÊNTICO. Rodei na mesa e ela
reprovou DUAS matérias boas, porque a casa usa `imgCredito` para crédito mais
legenda descritiva, enquanto a linha 📷 leva só o crédito. Igualdade era a
régua errada.

A régua certa é **sobreposição**: o que denuncia a porta dos fundos é que,
depois da troca de foto, os dois créditos não têm NENHUMA palavra em comum.
A trava agora reprova só nesse caso, e foi testada nos dois sentidos: pega o
erro real da Corrida dos Bichos e deixa passar as duas variações legítimas.

Fica a lição, que vale para as próximas travas: **trava estrita demais é
pior que trava nenhuma**, porque ensina a redação a contornar o portão em vez
de escrever melhor. Toda trava nova roda na mesa inteira antes de valer.

---

## 05/08/2026, rodada de teste da régua nova de pauta (quarta)

2 matérias de cinema e streaming, assinatura Pedro Amaral, encomendadas por
ele para ver o que a casa passa a pegar depois da mudança de pauta. **Os
graves foram todos invenção do redator, não erro de fonte.**

| Tipo | O que era | O que a checagem achou | Matéria |
|---|---|---|---|
| `invenção` | "Leandro Firmino, o **Buscapé** de Cidade de Deus" | Firmino interpretou **Zé Pequeno**. Buscapé foi Alexandre Rodrigues. Estava em três lugares: duas vezes no corpo e uma na legenda. É erro que qualquer leitor brasileiro pega na hora | Corrida dos Bichos |
| `invenção` | "O longa não nasceu para o streaming", com o SXSW como prova de um caminho anterior à plataforma | Não é que não se sustente: **inverte-se**. O filme foi anunciado como produção do Prime Video antes de rodar, as filmagens de 2024 já eram Amazon Original, e foi a própria Amazon que anunciou o SXSW como estreia global do seu Original. Caiu a frase e o parágrafo construído sobre ela | Corrida dos Bichos |
| `atribuição errada` | "Na plataforma, o produtor recebe antes, e uma vez só", com "o FOYER já destrinchou em [link]" | A matéria linkada trata de meia-entrada, ISS, Ecad e Condecine, e não diz uma palavra sobre pagamento de plataforma. O redator inventou uma frase e assinou com o nome da casa | Corrida dos Bichos |
| `invenção` | "assédio nas categorias de base" como tema da série | A fonte diz o **contrário**: o tema foi EXCLUÍDO na retomada de 2025. O redator usou a lista de 2023, de quando a série se chamava Mata-mata. Afirmar que uma produção identificável mostra assédio a menores, sem que ela mostre, rende processo | Jogada de Risco |
| `superlativo sem fonte` | O TÍTULO: "é o maior alcance da história do Globoplay" | A fonte impõe dois recortes: obras **originais de ficção** e **sete primeiros dias**. Como estava, a manchete afirmava o maior alcance de tudo o que já passou na plataforma, novela e futebol incluídos. **Ressalva grave: travou a matéria.** O checador não tinha mandato para mexer em título, então bloqueou em vez de deixar passar | Jogada de Risco |
| `invenção` | O lide copiava um dos portais palavra por palavra | Reescrito | Jogada de Risco |
| `superlativo sem fonte` | "Superou todas as séries dos últimos cinco anos" | Faltava o "no mesmo período", que está na fonte. Sem o recorte, vira vitória absoluta em vez de janela de sete dias | Jogada de Risco |
| `link quebrado` | Âncora dizendo que um filme "OCUPOU 2.500 salas" | A matéria de destino gasta um parágrafo dizendo o contrário, que ocupar uma sala não é trancá-la | Corrida dos Bichos |
| `data errada` | "No fim de semana passado", para o número de 2.500 salas | O número é da ESTREIA de quarta, 29 de julho, pelo Filme B | Corrida dos Bichos |
| `@ não confirmado` | @marceloadnet | O perfil verificado é **@marceloadnet0** | Jogada de Risco |
| `invenção` | Unidade "domicílios" na legenda do Instagram | Domicílio é unidade de medição de TV e não aparece em fonte nenhuma do pacote; corpo e fontes falam em usuários e contas. Achado pela leitura fria | Jogada de Risco |
| `invenção` | "volta a uma **favela**", "sessão de terça à tarde", "filme brasileiro de autor", "a desigualdade virou espetáculo", "país arruinado" | Cinco juízos e detalhes que fonte nenhuma sustenta | Corrida dos Bichos |

**DUAS RESSALVAS DO CHEFE ERAM FALSAS, e os checadores desmentiram as duas.**
A suposta divergência sobre quem dirigiu a Corrida dos Bichos não existia: a
Omelete, que já era fonte do pacote, nomeia os três diretores. E "maior
público" x "maior alcance" não são métricas diferentes neste caso, porque os
dois portais definem o indicador do mesmo jeito. Nenhum dos dois inventou
corte para justificar o trabalho. **Ressalva de chefe também precisa ser
checada**, e isso é novo neste registro.

**Pautas derrubadas antes de escrever: 4**, três delas por reprovar no teste
"por que hoje?" da 4.0 (cancelamentos da Netflix dos primeiros meses do ano,
o Tela Brasil de maio, um anúncio sem data confiável).

**O que esta rodada sugere mexer no sistema:**

1. **A PORTA DOS FUNDOS CHEGOU A SEIS OCORRÊNCIAS EM DOIS DIAS.** Buscapé na
   legenda, a lista de parceiros, a atribuição do anúncio, o superlativo do
   Death Note, o "da história" no Globoplay e agora "domicílios". Já era
   sugestão de trava ontem; hoje é dívida. **O portão precisa comparar
   afirmação do corpo com afirmação da legenda.**
2. **A META DE CORTAR 10% ESBARRA NO PISO DO PORTE PELA TERCEIRA VEZ** (7,8%,
   8,2% e, nesta, 10,1% só porque havia folga). O manual manda cortar 10% e
   manda respeitar o piso, e não diz o que fazer quando as duas se encontram.
3. **O CAMPO `eixo` NÃO É EXIGIDO NEM CONFERIDO.** A rodada gravou o eixo de
   temperatura em cada pacote por disciplina, não por obrigação. Se a casa
   quer garantir que as duas do dia não repetem eixo, isso é trava, não
   conselho. Foi a lição de ontem, e ela vale aqui.
4. **RESSALVA DE CHEFE ENTRA NA CHECAGEM.** Duas das minhas eram falsas e
   quase custaram cortes indevidos. O papel do Checador deveria dizer,
   explicitamente, que `chefe.ressalvas` é material a conferir, não instrução
   a obedecer.

---

## 04/08/2026, à tarde: a nota estava medindo a coisa errada

Não é corte de checagem, é conserto de régua, e entra aqui porque é
memória que atravessa rodada.

As duas matérias das 12h foram para a mesa com **nota 6**. O Pedro viu o
selo na Coxia e reagiu: pauta escolhida para ser escrita tem de valer 8 para
cima. Ele está certo, e o diagnóstico é pior do que "nota baixa demais".

O chefe rebaixou as duas **pelos erros que a checagem tinha achado no
rascunho e corrigido antes da entrega**. Ou seja: a esteira funcionou, o
erro morreu antes de chegar ao leitor, e a nota puniu o texto por um defeito
que ele não tem mais. O editor humano recebeu um número que descreve uma
matéria que ele nunca vai ler.

Erro achado e corrigido pela checagem pertence a `checagem.cortes` e a este
arquivo. Não pertence à nota. **A nota mede o texto que chega à mesa.**

Virou regra no manual (seção "A NOTA MÍNIMA É 8") e trava no
`audita_pauta.py`: abaixo de 8 a matéria não vai à mesa, volta ao redator ou
a pauta é descartada com o motivo no diário. As duas matérias foram
reavaliadas pelo texto entregue e valem 8, com a justificativa escrita no
parecer de cada uma.

---

## 04/08/2026, edição das 12h (terça)

2 matérias de cinema, assinatura Pedro Amaral. Primeira rodada escrita sob a
régua nova. **Os dois checadores derrubaram erro do REDATOR, não da fonte**,
que é exatamente para isso que existe a regra de que quem escreve não checa.

| Tipo | O que era | O que a checagem achou | Matéria |
|---|---|---|---|
| `superlativo sem fonte` | O fim de semana chamado de **recorde**, em três pontos do texto | Não houve recorde: 5,22 milhões de ingressos é MENOS que os 5,39 milhões de julho de 2023. A fonte diz "melhor resultado em 36 meses" e nunca diz recorde. Pior, o intertítulo "O recorde anterior tinha dois donos" afirmava que a marca havia caído e contradizia o parágrafo seguinte, que dizia que ela ficou de pé. Numa matéria cuja tese é a comparação entre os dois fins de semana, errar qual foi o maior é errar o assunto | Melhor fim de semana |
| `superlativo sem fonte` | O mesmo "recorde" vivendo na legenda do Instagram | A porta dos fundos de novo, exatamente como no Death Note de ontem | Melhor fim de semana |
| `atribuição errada` | "A Elo Studios anunciou parceria com a TvZero e com a Dualto" | O Tela Viva escreve "a Elo Studios, a TvZero e a Dualto Produções anunciam parceria". Ninguém anunciou parceria com ninguém: as três anunciaram juntas | Sobre Noix |
| `atribuição errada` | A MESMA formulação sobrevivendo na legenda do Instagram depois de corrigida no corpo | Não foi a checagem que pegou: foi a leitura fria, uma onda depois. Terceira ocorrência do padrão em dois dias | Sobre Noix |
| `invenção` | "O dinheiro público do audiovisual chega quase todo na etapa de produção" | Nenhuma fonte do pacote, nem a nossa própria matéria do FSA, sustenta o "quase todo". Trocado pelo que a matéria de destino de fato diz: a linha de Núcleos Criativos passou nove anos sem edital e reabriu em junho | Sobre Noix |
| `invenção` | "o mercado inteiro passou **o feriado** torcendo por ele" | Não há feriado nacional em julho nem agosto de 2026, e nenhuma fonte cita feriado. Era a janela do fim de semana, que a matéria decidira não afirmar, entrando pela porta dos fundos | Melhor fim de semana |
| `invenção` | "parte dessa gente **volta em setembro**" | Mês escolhido pelo redator, sem fonte. Virou "volta depois" | Melhor fim de semana |
| `atribuição errada` | Lista de parceiros do HBF+Brazil sem a Spcine | O release do IFFR, **que já era fonte do pacote**, lista "Spcine, RioFilme, Projeto Paradiso and Embratur". E a ressalva do chefe justificava a ausência dizendo que a Spcine não constava das fontes recentes: a ressalva era falsa | Sobre Noix |
| `link quebrado` | "a fatia do distribuidor é maior nas **primeiras semanas**" | Inverte a matéria linkada, que diz que ele puxa a fatia maior NA ESTREIA e que já na segunda semana parte dos contratos leva o exibidor a 60% | Melhor fim de semana |
| `link quebrado` | Maricá como exemplo de dinheiro para **desenvolvimento**, com os R$ 20 milhões do pacote | Dos R$ 20 milhões, R$ 17 milhões são produção e só R$ 3 milhões desenvolvimento. A âncora passou a dizer os R$ 3 milhões | Sobre Noix |
| `@ não confirmado` | @filmeb, @portalexibidor, @nosdomorro, @riofilme | Os quatro errados. Os oficiais são @filmebportal, @portal.exibidor, @gruponosdomorrooficial e @_riofilme (com underline). Errar o @ do veículo de onde vieram todos os números seria constrangedor. Os dois primeiros foram corrigidos; os dois últimos ficaram registrados sem inserir, para o Pedro decidir | as duas |
| `data errada` | "Num fim de semana recente" | Numa matéria de agosto, "recente" fica solto. Datado em 23 a 26 de julho | Sobre Noix |
| `insinuação sem fonte` | "criado no Vidigal, **na zona sul do Rio**" | Zona sul não está em fonte nenhuma. O Festival do Rio diz "nascido e criado no Morro do Vidigal" | Sobre Noix |
| `atribuição errada` | "negligência e **violência**" | A fonte diz "negligência e maus-tratos". "Violência" era palavra do redator | Sobre Noix |

**Pautas derrubadas antes de escrever: 5.** Duas merecem registro. A
Instrução Normativa 175 da Cota de Tela apareceu como pauta do dia numa
busca e é de **6 de maio**: notícia velha disfarçada de nova, o mesmo tipo
que derrubou a pauta do FSA ontem. E "Rio de Clarice" caiu por fato em
disputa: parte das fontes dá estreia em 13 de agosto de 2026, outra registra
estreia em Teresópolis em novembro de 2025, com as produtoras ainda
negociando distribuidora.

**O que esta rodada sugere mexer no sistema:**

1. **A PORTA DOS FUNDOS JÁ É PADRÃO, NÃO DESCUIDO.** Três ocorrências em dois
   dias: o superlativo do Death Note ontem, o "recorde" e a atribuição do
   Sobre Noix hoje. Toda vez que a checagem corrige o CORPO, o mesmo erro
   fica vivo no `instagram.legenda`, que ninguém relê. **Vira trava no
   portão**: comparar afirmações do corpo com as da legenda, ou no mínimo
   exigir que quem mexe no corpo declare se mexeu na legenda.
2. **A CORREÇÃO EMPILHA EM VEZ DE SUBSTITUIR.** A leitura fria achou que o
   parágrafo de 2023 dizia três vezes a mesma coisa, porque a correção do
   superlativo foi escrita EM CIMA da frase antiga em vez de trocá-la. Quem
   corrige fato tende a acrescentar. Vale uma linha no papel do Checador:
   depois de corrigir, releia o parágrafo inteiro e apague o que a correção
   tornou redundante.
3. **QUEBRAR A FÓRMULA EM DUAS FRASES NÃO DESFAZ A FÓRMULA.** "O problema
   ali não foi falta de público. Foi falta de tela" é o "não é X, é Y"
   proibido, só com ponto final no meio, e passou pela onda 1 e pela onda 2.
   Quem caça fórmula precisa procurar também a versão fatiada.
4. **O EDITOR HUMANO É O ÚNICO DA ESTEIRA SEM PORTÃO.** A matéria dos acordos
   de coprodução, editada pelo Pedro na Coxia, reprova com 4 travessões,
   1.362 palavras, zero intertítulos `## ` e zero links internos. Os
   intertítulos dele existem, mas saíram como `**negrito**`. **Isso não se
   conserta nesta sala**: é pedido para a conversa do site e da Coxia.

---

## 04/08/2026 (terça)

6 matérias, cota 2+2+2. Os quatro primeiros são os que teriam doído.

| Tipo | O que era | O que a checagem achou | Matéria |
|---|---|---|---|
| `número desatualizado` | Taxa do registro de ator: R$ 165 | O valor vem de documento do sindicato de 2022. A tabela de 2025, que o próprio sindicato manda consultar, cobra R$ 350, R$ 180 ou R$ 90 conforme a função. Um ator iria ao sindicato com o dinheiro errado. Corte: o texto passou a dizer que varia por função, e que a cobrança é do sindicato paulista, não nacional | DRT de ator |
| `invenção` | "o dinheiro do setor segue vindo da bilheteria" | O próprio relatório citado desmente: dos ~R$ 1,2 bi de Condecine em 2024, R$ 1,07 bi vem das teles. Fecho reescrito | CCS / Condecine |
| `link quebrado` | Botão "Comprar ingressos" | Levava à página institucional de regras da bilheteria, que não vende nada. Trocado pela página de compra do concerto | Tan Dun |
| `superlativo sem fonte` | "a primeira montagem em inglês" (era o gancho da pauta) | Nenhuma fonte sustenta: Barbican, produtora e imprensa britânica dizem estreia mundial DESTA produção. E os produtores de 2023 já tinham anunciado o Palladium como a primeira em inglês. O achado do Rio sobreviveu, virando aritmética datada | Death Note |
| `superlativo sem fonte` | O mesmo superlativo, sobrevivendo no lide e na legenda depois de sair do título | Pego pela leitura fria, não pela checagem. Erro corrigido na porta da frente e vivo na dos fundos é o pior tipo, porque parece resolvido | Death Note |
| `atribuição errada` | "34 obras estrangeiras **por ano**" | A fonte não diz periodicidade. O "por ano" era acréscimo do redator | Coprodução China/França |
| `atribuição errada` | As duas autoras do artigo teriam ido à delegação a Xangai | A fonte confirma só uma delas | Coprodução China/França |
| `atribuição errada` | Piso de 10% "para o interior de São Paulo e do Rio" | A norma diz São Paulo e Rio **excetuadas as capitais**. Niterói e Guarulhos não são capital nem interior, e ficariam de fora do jeito que estava escrito | CCS / Condecine |
| `data errada` | "Em abril, o Theatro São Pedro montou Fidelio" e "na temporada recente" | As récitas foram em abril de **2025**; O Navio Fantasma é de 2023 e Mar Aberto de 2024. Numa matéria de agosto de 2026, "em abril" seco lê-se como 2026 | Tan Dun |
| `data errada` | "estreou em 30 de julho" | Era pré-estreia. A estreia oficial é 11 de agosto, e são coisas diferentes | Death Note |
| `número desatualizado` | Release da companhia anuncia 20 anos | Fundada em 2007: faz 19. Duas fontes independentes do release | Capulanas |
| `aspa não literal` | "A rejeição restaura…" | O documento diz "rejeição **que** restaura…". A ligação saiu de dentro das aspas | CCS / Condecine |
| `invenção` | Mar Aberto como "musical", na "mesma sala" | Nossa própria matéria diz Cúpula, e descreve peça metateatral | Tan Dun |
| `invenção` | "o caso do YouTube" na faixa de 0,1% a 0,8% | Nenhuma fonte atribui | CCS / Condecine |
| `invenção` | Art. 7º, II como lista fechada de funções | A lei termina em "**ou outras semelhantes**, reconhecidas na forma da Lei". Sem isso, quem tem certificado em outra função conclui que está fora. O texto tinha ainda trocado o "ou" por "e", que fecha a lista | DRT de ator |
| `@ não confirmado` | @tan_dun, @osmdesp, @escoladeartesfazassim | Nenhum linkado em página oficial; o da orquestra se apresenta como perfil dos músicos, não da instituição. Marcados `confirmado: false` para o Pedro decidir | Tan Dun, Death Note |
| `direito de foto` | Campo `imgDireito` vazio em cinco das seis | Preenchido pelos checadores com a licença auditada. **Vale virar trava no portão** | toda a rodada |

**Pautas derrubadas antes de escrever: 15.** Uma merece registro: uma notícia
do FSA no gov.br parecia de 2026 mas era de setembro de 2025, com a página
apenas remexida. Notícia velha disfarçada de nova.

**O que esta rodada sugere mexer no sistema:**

1. `imgDireito` vazio em 5 de 6 é padrão, não descuido. **O portão deveria
   exigir o campo**, como já exige crédito e fonte.
2. Três dos quatro erros graves eram **número ou data que envelheceu**
   (taxa de 2022, temporada de 2025, pré-estreia). Vale uma linha no manual:
   *todo valor e toda data passam pela fonte oficial mais recente, e o
   redator diz no pacote de quando é o documento que usou.*
3. O superlativo que sobreviveu no lide depois de sair do título mostra que
   **corrigir o título não basta**: quem corrige tem de varrer corpo, lide e
   legenda atrás da mesma afirmação com outras palavras.
