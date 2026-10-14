# A mesa do Pedro: matérias assinadas por Pedro Amaral, publicadas direto

Manual do fluxo em que o Claude pesquisa, escreve, entrega aqui e, **depois
que o Pedro aprova e marca a hora**, publica no site as matérias assinadas
por Pedro Amaral (ordem dele, 14/10/2026). Substitui o trabalho que ele fazia
no ChatGPT e colava à mão na Coxia.

Este fluxo tem dois produtos:

| Produto | Quando | Quantas | Vai ao ar |
|---|---|---|---|
| **Pautas quentes** | todo dia, rodadas das **7h** e das **17h** (Brasília), automáticas, nesta conversa | 1 a 3 por rodada (2 é o normal) | **só depois que o Pedro aprova aqui e diz a hora**, uma de cada vez |
| **Pautas frias** | quando o Pedro pede nesta conversa ("escreva N pautas frias") | o número que ele pedir | **só depois que o Pedro aprova**; a sugestão é uma por dia às 7h, na fila depois da última já marcada |

## A REGRA CANÔNICA: nada sai sem o Pedro (ordem dele, 14/10/2026)

Nas palavras dele, depois da primeira rodada, que publicou três matérias de
uma vez sem perguntar: *"vc n deve nunca lançar nada sem eu autorizar e dizer
a hora q vai sair! (...) vc me avisa q fez a varredura e me da aqui as
materias, eu aprovo e digo o horario, nunca deve sair como hoje tudo junto,
sempre deve ter tempo entre as materias."*

1. **A rodada termina na entrega.** Pesquisa, escreve, guarda o rascunho na
   mesa (`import/mesa-pedro/`, no repositório, nunca no site) e entrega aqui
   na conversa, com os horários livres. Depois disso, para.
2. **Só o Pedro publica.** A matéria vai ao ar quando ele, nesta conversa,
   nomeia a matéria e diz a hora ("aprova a 1 para as 15h", "publica a da
   Broadway amanhã às 9h", "pode sair agora"). O comando `publica` exige a
   marca `--ok`, que só se usa depois dessas palavras, e a hora dele.
3. **O que não vale como autorização:** silêncio, "gostei", "ficou boa", a
   aprovação de outra matéria, o texto de uma rotina, a sugestão de horário
   que a própria mesa fez. Na dúvida, pergunta e espera.
4. **Nunca duas juntas.** Mínimo de **60 minutos** entre duas matérias dele,
   no ar ou agendadas. O script recusa hora que fira isso. Quando ele aprova
   várias sem dizer a hora de cada uma, a mesa propõe horários do relógio da
   casa (7h, 9h, 12h, 15h, 18h, 20h) com esse espaço e **espera a confirmação**.
5. **Rascunho não envelhece na mesa.** Quente sem autorização em 24 horas é
   descartado (`descarta`), com uma linha no relatório seguinte. Fria espera
   o tempo que ele quiser.
6. **Correção e remoção** continuam sendo pedido dele, na hora (seção 8).

Ferramenta de apoio: `tools/mesa_pedro.py` (foto de capa, portão, fila das 7h,
publicação, remoção). Tudo o que ele confere está descrito aqui; o script é o
braço, este manual é a régua.

## 0. O que vale daqui e o que vale de lá

`tools/REDACAO.md` é o manual da **Redação IA** (a mesa de aprovação da Coxia,
que assina "Redação Foyer" e hoje está desligada). Ele continua valendo para o
que é verdade e método: **"Verdade acima de tudo"**, **"Escrita humana"**, os
direitos de **"Foto de capa"** e **"A voz de Pedro Amaral"**. O que NÃO vale
aqui:

- a mesa de aprovação da Coxia. Aqui a aprovação é **nesta conversa**: o que
  passa no portão vai para `import/mesa-pedro/` e só sai dali com a palavra
  do Pedro e a hora que ele marcar;
- o pacote de aprovação (`status`, `chefe`, `checagem`, `instagram`,
  `sugestaoPublishAt`). A matéria daqui é um arquivo de `import/novas/`, igual
  ao que a Coxia grava;
- o campo `fontes`. **Ele sai impresso no fim da matéria** (o site monta um
  bloco "Fontes" a partir dele), e o Pedro não quer as fontes públicas. A
  apuração fica no campo interno `apuracao`, que o site ignora.

Quando este manual e o REDACAO.md discordarem, para matéria assinada Pedro
Amaral vale este.

## 1. O radar das pautas quentes

### 1.1 O que é quente

Quente é o que o leitor já viu passar, ou vai ver nas próximas horas, e
abriria por vontade própria. Os eixos, nas palavras do Pedro ("temas mais
quentes e do momento, polêmicas, bilheteria de cinema, estreia de séries,
polêmicas nos streamings"), mais a força da casa, que é o teatro musical:

| Eixo | O que entra | O gancho que a matéria dele puxa |
|---|---|---|
| **Teatro musical** | Broadway, West End e Brasil: estreia, elenco confirmado, fechamento, recorde de bilheteria, prêmio, turnê, gravação que vai ao cinema ou ao streaming | quanto custou, quanto faz, quem produz, o que muda para quem trabalha |
| **Bilheteria** | o número do fim de semana, a estreia que estourou ou afundou, a corrida do ano, o filme brasileiro na conta | o tamanho real do número, quem perdeu sala, quanto sobra para quem fez |
| **Estreia** | filme ou série que estreia agora e que as pessoas estão esperando | quem fez, quanto custou, onde assistir, por que importa |
| **Polêmica e disputa** | briga pública com nome e fonte: elenco, cancelamento, processo, boicote, decisão que irritou o público | quem disse o quê, quem responde, o que está em jogo |
| **Decisão de plataforma** | o que entra e some do catálogo, preço, série cancelada, regra nova que o assinante sente | o que muda para quem paga a assinatura |
| **Teatro com repercussão nacional** | morte de artista, prêmio grande (APCA, Shell, APTR), estreia que a cidade comenta, decisão pública com efeito imediato (edital suspenso, teatro fechado, verba cortada) | a consequência concreta, com data |

O dinheiro é o chão de tudo e é o que separa o FOYER do Omelete: ele entra
**depois** do gancho quente, explicando o número que a notícia trouxe. Nunca
como assunto em si. Norma pela norma (Condecine, cota de tela, acordo de
coprodução) não é pauta dele; só entra com porta quente, quando há
consequência que o leitor sente.

### 1.2 Os quatro testes antes de escrever

1. **Por que agora.** Se a resposta é "porque é interessante", não é quente.
   Precisa de data: anunciado em, estreou em, divulgado em, decidido em.
2. **Teste do signatário.** O Pedro explicaria o assunto a um amigo em duas
   frases sem reler o texto? Se não, a pauta não é dele. Cai.
3. **Teste da repercussão.** Ao menos uma das matérias da rodada tem que ser
   assunto que já circula (Deadline, Variety, Playbill, Broadway World, Omelete,
   AdoroCinema, Folha, G1, O Globo, Estadão, Veja, redes). A segunda pode ser
   a que a casa enxergou antes.
4. **Teste do acervo.** Antes de escolher, rode
   `python3 tools/mesa_pedro.py ja-saiu "palavra chave"`. Assunto já
   publicado só volta com **fato novo** (número novo, decisão nova, resposta
   da outra parte). Reescrever o mesmo fato é proibido.

### 1.3 Composição da rodada

- **Duas matérias, de eixos diferentes.** Duas de bilheteria, nunca.
- **Uma com repercussão em curso** (teste 3) é obrigatória quando existe.
- **Portes diferentes.** Se uma é `nota`, a outra é `quente` ou `contexto`.
  Duas do mesmo porte na mesma rodada só se os intertítulos forem diferentes.
- **Uma só** quando o dia é fraco. **Três** quando o dia é forte e as três se
  sustentam sozinhas. **Nenhuma** é resposta válida: o relatório diz quais
  candidatas foram vistas e por que nenhuma passou. Forçar pauta fraca no
  nome dele é pior que a rodada vazia.
- A rodada das **7h** cobre o que aconteceu desde a véspera, inclusive a
  noite americana (Broadway anuncia à noite, bilheteria sai de manhã). A das
  **17h** cobre o dia. A das 17h lê o que a das 7h publicou e não repete.
- **Pedido fora de hora** ("escreve sobre X agora") segue o mesmo caminho:
  entrega na hora, publica quando ele disser.

### 1.4 Onde olhar

Busca na web com data (o `WebSearch` aceita "esta semana", nomes e datas).
Para teatro musical: Playbill, Broadway World, Deadline, Variety, The Stage,
WhatsOnStage, e no Brasil a imprensa diária e a assessoria das produções. Para
cinema e streaming: Deadline, Variety, The Hollywood Reporter, Box Office Mojo,
Filme B (Brasil), Omelete, AdoroCinema, o site oficial de cada plataforma. Para
teatro brasileiro: Folha, Estadão, O Globo, G1, Veja SP, Sesc, Itaú Cultural,
as casas e os prêmios. Sempre **abrir e ler** a página antes de usar um fato;
a ementa do buscador não é fonte.

## 2. As pautas frias

Fria é matéria que o leitor procura no Google sem notícia nenhuma por trás:
**pergunta do público** ("por que dá vontade de chorar no teatro", "como
escolher um lugar no teatro", "o ator pode mudar o texto"), **lista** ("10
filmes conhecidos que têm uma peça na origem", "7 musicais que sobreviveram a
fracassos") e **explicador** ("para onde vai o dinheiro do ingresso", "de quem é
o direito de montar uma peça"). Os temas são os da casa: teatro, teatro
musical, cinema e música, e o olhar do Pedro (dinheiro, trabalho, acesso) entra
quando o assunto o pede.

Como escolher:

- a pergunta tem de ser **como as pessoas digitam** ("Broadway, Off-Broadway e
  West End: qual é a diferença?"). O título de fria é a busca exata;
- `ja-saiu` antes de escolher, sempre: as frias do acervo vão de agosto a
  novembro de 2026 e o Pedro já cobriu muita pergunta óbvia;
- apuração de verdade, com o nome das coisas (lei, obra, ano, número oficial,
  dicionário, estudo com instituição e ano), e nunca "especialistas afirmam";
- **a sugestão é uma por dia às 7h.** A fila continua de onde está: a
  primeira fria nova entraria no primeiro dia livre depois da última já
  agendada (`python3 tools/mesa_pedro.py proximo-7h --n 5` lista os próximos
  cinco). O relatório propõe a data de cada uma; **nada entra na fila sem o
  Pedro confirmar**, e ele pode pedir outra ordem ou outra hora.
- Numa leva de N frias, **portes e formatos variados**: nunca cinco listas
  seguidas, nunca cinco perguntas com a mesma estrutura.

**A fria tem de envelhecer bem (ordem do Pedro, 14/10/2026).** Na primeira
leva, as cinco frias saíram com cara de quente: lide pendurado no caso da
semana, trailer, "ainda não tem data", "até 14 de outubro não havia
votação". O Pedro leu urgência onde devia ler acervo. A regra, a partir daí:

- **o lide abre com a pergunta ou com o mecanismo, nunca com o caso da
  semana.** O caso recente entra como exemplo, no corpo, no passado e
  fechado ("em setembro de 2026, o Prime Video encerrou X cinco meses depois
  de lançar a segunda temporada"), nunca como gancho;
- **o teste é a leitura daqui a um ano:** se uma frase deixa de ser verdade
  em seis meses, ela não entra ou vira passado datado. Proibidos na fria:
  "ainda não", "ainda está", "sem data", "até o momento", "até agora", "por
  enquanto", "no momento", "segue em cartaz", "está em cartaz", "esta
  semana", "este fim de semana", "neste mês", "nos próximos dias", "em
  breve" e contagens com "em DD/MM" ("em 14 de outubro, o JustWatch
  registrava"). Estado presente só para o que é permanente (a lei, o
  contrato, o modelo de negócio). O portão reprova essas expressões em
  `resposta`, `lista` e `explicador` e avisa quando o lide traz data dos
  últimos quatro meses;
- **trailer só em fria de filme ou de lista de filmes**, nunca como gancho
  de atualidade numa pergunta geral;
- os números têm data na frase quando vão mudar ("US$ 540,8 milhões pelo
  Box Office Mojo em outubro de 2026"), para a matéria continuar certa
  depois que o número subir;
- o fecho olha para o leitor, não para a semana: o que ele pode fazer, onde
  olhar, o que a regra diz. Nada de "enquanto a data não sai".

## 3. A régua do tamanho, com base no que o mercado produz (ordem do Pedro, 14/10/2026)

Depois da primeira rodada, o Pedro achou as matérias rasas e curtas e pediu
uma base medida no mercado. A medição é de 14/10/2026, texto do corpo, em
palavras, feita em páginas renderizadas (as mesmas pautas do dia):

| Veículo e tipo de texto | Palavras |
|---|---|
| Omelete, nota de bilheteria e nota de recorde | 230 a 270 |
| The Hollywood Reporter, balanço semanal da Broadway | 300 |
| CNN Brasil, notícia de elenco (Percy Jackson) | 305 |
| AdoroCinema, Papelpop, Alô Alô Bahia, notícia de bilheteria | 270 a 375 |
| Broadway.com, Exame, Ingresso.com, notícia com apuração | 400 a 430 |
| Deadline, balanço da Broadway; NYTG, elenco completo | 475 a 520 |
| Playbill, análise semanal de bilheteria | 600 |
| Agência Brasil, cobertura de premiação (Festival do Rio) | 850 |
| Gazeta do Povo, análise do fenômeno "Minha Melhor Amiga" | 935 |
| CNN Brasil, entrevista com o protagonista de "Percy Jackson" | 2.250 |
| FOYER, acervo 2026, mediana | 490 |
| FOYER, matérias do Pedro pela Coxia, mediana | 590 |
| FOYER, Redação Foyer pela Coxia, mediana | 1.020 |

As réguas das agências e dos jornais dizem o mesmo: a AP (2014) pede 300 a
500 palavras para a notícia comum, 500 a 700 para a principal do dia e mais
de 700 só para a global; a Reuters trabalha com 400 (nota do dia), 800
(matéria principal, exclusiva) e 2.000 (reportagem especial); o Washington
Post (2007) media a notícia do dia em 6 a 15 polegadas de coluna (200 a 500
palavras) e a reportagem em 25 a 35 (900 a 1.250). A lauda brasileira tem
1.400 caracteres, cerca de 230 palavras, e "uma matéria razoável tem duas
laudas". A Pew Research mediu em 2016 que texto de 1.000 palavras ou mais
prende o leitor no celular o dobro do tempo do texto curto (123 segundos
contra 57), e que o tempo cresce com o tamanho até 5.000 palavras.

**A leitura.** O mercado faz a notícia cultural em 250 a 520 palavras, a
análise em 600 a 950 e a entrevista ou o perfil acima de 2.000. O que o FOYER
promete é o tratamento que o mercado não faz: o tamanho real do número, quem
pagou, o que muda para quem trabalha. Por isso a quente do FOYER fica
**acima da notícia do mercado**, e a reportagem **acima da análise dele**.
Curta só quando o assunto é curto.

| `porte` | Quando | Palavras (caracteres) | Intertítulos |
|---|---|---|---|
| `nota` | o aviso curto: data marcada, elenco confirmado, trailer, temporada estendida, prêmio anunciado | **250 a 400** (1.500 a 2.500) | nenhum |
| `quente` | a notícia com consequência: bilheteria com leitura, cancelamento, polêmica com os dois lados, decisão de plataforma, estreia esperada | **600 a 900** (3.600 a 5.500) | 1 a 3 |
| `contexto` | a reportagem com o antes: disputa, morte e legado, regra nova com efeito no bolso, fenômeno que pede números e história | **1.000 a 1.500** (6.000 a 9.000) | 3 a 5 |
| `perfil` | perfil ou memória de alguém, com obra e trajetória documentadas | **1.200 a 2.000** | 3 a 6 |
| `resposta` (fria) | a pergunta do público respondida de pé, com fontes nomeadas | **700 a 1.000** | 2 a 4 |
| `explicador` (fria) | o tema que pede contexto: dinheiro, direito, história | **1.000 a 1.500** | 3 a 5 |
| `lista` (fria) | N itens, cada um com intertítulo próprio e um parágrafo de verdade | **1.200 a 1.800** | um por item, de 7 a 12 |

**O piso é de substância, não de palavras.** Encher para chegar ao piso é
proibido. Se não há material para as camadas da seção 3.1, a pauta é `nota`,
ou não é pauta. O portão cobra a faixa, a cota de intertítulos e a apuração
mínima por porte (nota 2 páginas lidas; quente 4; resposta 4; explicador e
lista 5; contexto e perfil 6).

### 3.1 As camadas: o que o leitor acha numa matéria do FOYER e não acha no Omelete

A matéria rasa tem só a camada 1. A régua do tamanho existe para caber as
outras.

1. **O fato**, com data, sujeito e o número certo. É o lide.
2. **O antes.** Quem é a pessoa, de onde veio a obra, o que aconteceu nas
   edições anteriores, o que o mercado fazia até ontem. Dois parágrafos na
   quente, quatro ou mais na reportagem. Sem o antes, o número não tem
   tamanho.
3. **Gente.** Ao menos uma voz real: declaração publicada (entrevista,
   release, rede oficial), com o veículo nomeado. A matéria sem aspas é
   relatório.
4. **A ponte com o leitor daqui.** O que isso muda para quem compra ingresso
   no Brasil, para a montagem brasileira anunciada, para o artista que
   trabalha aqui. Matéria internacional sem ponte é tradução.
5. **O dinheiro, explicado.** Um número escolhido e explicado vale mais que
   cinco listados. Quem pagou, quanto custa, quanto sobra.
6. **O que falta saber.** O que a fonte não diz, a decisão que ainda vem, a
   data a olhar. É o fecho honesto, e varia de matéria para matéria.

Mínimos: `nota` tem a 1 e uma das outras; `quente` tem 1, 2, 5 e 6 e ao
menos uma entre 3 e 4; `contexto`, `perfil` e `explicador` têm as seis.

### 3.2 Apuração mínima

Antes de escrever a quente: a fonte oficial ou primária, dois veículos
independentes, uma página de contexto (a história, a edição anterior, o
perfil de quem aparece) e uma busca específica por declarações. Para a
reportagem, seis páginas ou mais, com documento quando existir. Página
aberta e lida; a ementa do buscador não é fonte.

## 4. Como o Pedro escreve (e como nunca parecer máquina)

Pedro escreve **quente e perto do leitor**, com apetite pelo concreto. Leia os
três trechos da seção "A voz de Pedro Amaral" do REDACAO.md antes de começar.
O que fazer com a próxima frase:

- **O fato primeiro, com data e sujeito.** Depois o porquê importa. Depois a
  régua (número, documento, exemplo) que mostra o tamanho real da notícia.
- **Frase longa que arma o problema, duas curtas que o resolvem.** "A
  remuneração do ator de teatro no Brasil se conta por sessão, e o valor muda
  conforme o teatro, o número de apresentações na semana, a função em cena e
  quem paga a conta. Boa parte dessas contas nunca vira dado público. Parte
  vira."
- **Quando a casa faz a conta, ela diz que fez.** "Dividir as 2.500 salas pelo
  total da Ancine é conta desta redação, e dá 70%."
- **Número com fonte, período, universo e unidade.** "US$ 6,97 milhões por
  dia a partir de outubro", nunca "quase sete milhões".
- **Aspas só reais**, localizadas na origem, com o veículo nomeado quando
  traduzidas ("disse à Playbill"). "Ao FOYER" é proibido: ninguém falou
  conosco.
- **Fecho num fato, numa consequência ou numa chamada direta** ("vale ficar
  de olho na bilheteria de quinta"). Nunca num resumo do que foi dito, nunca
  numa pergunta retórica, nunca num assunto novo.
- **Sem primeira pessoa do singular.** "Esta redação" quando precisar.
- **A lente dele** (cultura como política pública, quem faz o palco também
  trabalha, acesso, desconfiança de concentração) entra pela **escolha do
  ângulo**, nunca torcendo fato. Matéria factual não leva opinião. Dado que
  contraria a tese entra do mesmo jeito.

### 4.1 As marcas de IA, e o que entra no lugar (o portão barra as que dá para medir)

1. **Travessão e meia-risca são proibidos** em qualquer lugar (título, linha
   fina, corpo, legenda, serviço). No lugar: vírgula, dois-pontos, parênteses
   ou **ponto final**. Quando a frase pedir travessão, quase sempre o certo é
   duas frases. Única exceção: nome oficial de obra ("Djavan – O Musical"),
   declarado em `nomes_proprios`.
2. **Fórmulas proibidas:** "não é X, é Y"; "mais do que X, é Y"; "verdadeiro(a)
   + substantivo"; "X não é detalhe"; "prova de que"; "é aí que entra"; "o
   resultado?"; "vale lembrar"; "vale destacar"; "é importante ressaltar";
   "nesse sentido"; "nesse contexto"; "em suma"; "em resumo"; "por fim";
   "seja X, seja Y"; "não por acaso"; "longe de ser"; "uma espécie de"; "em
   meio a"; "em um cenário"; "com o avanço de"; "desde então" abrindo
   parágrafo; "especialistas afirmam" sem nome.
3. **Clichês de release:** imperdível, vibrante, emocionante, único, icônico,
   mergulhar, celebrar, promete emocionar, experiência única, sucesso
   absoluto, vem conquistando, não poderia ser diferente.
4. **Trio de adjetivos e trio perfeito** ("emociona, diverte e transforma").
   Um adjetivo forte, sustentado por fato, vale mais que três.
5. **Pergunta retórica seguida de resposta.** Se a pergunta é a busca do
   leitor, ela vai no título da fria, e o texto responde sem repeti-la.
6. **Parágrafo final que resume** ("Assim, ...", "Dessa forma, ...",
   "Portanto, ..."). O texto termina quando a informação termina.
7. **Ritmo medido:** ao menos **20% das frases com menos de 12 palavras**;
   **média de até 26 palavras por frase**; parágrafos de 1 a 5 frases, de
   tamanhos diferentes; nunca três parágrafos seguidos começando com a mesma
   palavra ("A peça", "O filme", "A produção").
8. **A simetria é a marca mais traiçoeira.** Frases do mesmo tamanho,
   parágrafos do mesmo tamanho, seções do mesmo tamanho, cada seção fechada
   em si. Uma seção existe porque a anterior deixou uma pergunta aberta: se
   dá para trocar duas de lugar, são gavetas, não seções.
9. **Lista de tópicos no corpo** (`- item`) é proibida nas quentes. Na fria
   só a lista numerada por intertítulo.
10. **Hedge empilhado** ("pode ser que talvez") e **verbo maior que a prova**
    ("garante", "revoluciona", "transforma"). Rebaixar: "cria condições
    para", "amplia a possibilidade de", "torna elegível".
11. **"Hoje", "ontem", "nesta terça"** morrem em 24 horas. Data, sempre. O
    que ainda vai acontecer se escreve em "está marcado para", nunca no
    pretérito.
12. **Negrito** só em nome de obra na primeira menção e nos intertítulos de
    lista. **Nunca o primeiro parágrafo inteiro em negrito**: o site o
    transforma em linha fina e ele some do corpo.
13. **Começo de matéria** varia: pelo fato, pela cena, pelo número, pelo
    nome. Nunca pela definição ("X é um musical que..."), nunca por
    "Em um cenário...".
14. **Repertório não é fôrma (14/10/2026).** "É conta desta redação" e
    "vale ficar de olho" são movimentos do Pedro, e na primeira rodada
    apareceram em duas de três matérias. Cada um entra **no máximo uma vez
    por semana**, somando todas as matérias dele; o portão conta. O mesmo
    vale para qualquer frase que você perceba repetindo de uma matéria para
    outra.
15. **Prosa de planilha é proibida.** "Harry Potter (US$ 2,22 milhões), O
    Rei Leão (US$ 2,22 milhões), MJ (US$ 1,89 milhão)" é tabela disfarçada.
    Um número por frase no lide; no máximo cinco por parágrafo; nunca três
    valores entre parênteses no mesmo parágrafo. Escolha o número que conta
    a história e explique-o; os outros entram em uma frase cada, com o que
    significam, ou não entram.
16. **Staccato também é máquina.** "Vende menos." uma vez é respiro; três
    vezes é tique. Frase de até três palavras: no máximo uma por matéria.
    E toda quente ou reportagem tem ao menos **um parágrafo de fôlego, de
    70 palavras ou mais**, onde a história anda de verdade.
17. **Leitura fria obrigatória.** Depois do texto pronto, uma segunda
    passada, por outro agente quando a rodada roda com agentes, com uma
    pergunta: *um jornalista de cultura, lendo isto, acharia que foi
    escrito por máquina? Em quais frases, e por quê?* A resposta nomeia as
    frases, e elas são reescritas. "Está bom" não é resposta.

### 4.2 Título e linha fina (os últimos a serem escritos)

- **Título:** os primeiros **60 caracteres** funcionam sozinhos (o buscador
  corta ali); teto **90**. O termo que a pessoa digita vem na frente (obra,
  nome, personagem). Sem "entenda", "veja", "confira", "saiba", "descubra"
  como muleta. Sem pergunta de sim ou não. Sem "hoje". Sem travessão. A
  palavra que qualifica ("costuma", "pode", "custará") cabe dentro dos 60. Na
  mesma rodada, títulos com formas diferentes. O título não promete o que o
  texto não entrega.
- **Linha fina (`linhaFina`):** uma frase de **60 a 200 caracteres** que
  acrescenta o que o título não disse (o número, a data, a consequência, o
  limite). Não repete o título. É ela que sai no Google, no WhatsApp e na
  capa.

## 5. A estrutura completa de uma matéria (o pacote)

A matéria é um JSON em `import/novas/<slug>.json`, o mesmo formato que a
Coxia grava. Campos obrigatórios marcados com •.

| Campo | O que é |
|---|---|
| • `title` | o título (regras em 4.2); sem `*` |
| • `linhaFina` | o subtítulo |
| • `slug` | ASCII minúsculo com hifens, até 80 caracteres, único no acervo |
| • `cat` | a **editoria principal**, uma de: Teatro, Teatro Musical, Notícia, Cinema, Streaming, Música, Show, Dança, Exposições, Literatura, Televisão, Audições, Edital, Festa, Programa, Guia, Bastidores, Entenda, Memória |
| • `cats` | até **2 editorias secundárias** da mesma lista (lista vazia se não precisar). `Em Cartaz` só aqui, e só para peça em temporada no momento da publicação |
| • `author` | `Pedro Amaral`, sempre |
| • `porte` | `nota`, `quente`, `contexto`, `resposta`, `lista` ou `explicador` |
| • `corpo` | o texto no formato da Coxia (abaixo) |
| • `img` | `assets/uploads/<slug>-<carimbo>.jpg`, capa 16:9 com até 1600 px |
| `imgOriginal` | `assets/uploads/<slug>-original-<carimbo>.jpg`, a foto inteira (para as artes do Instagram) |
| • `imgCredito` | quem fez a imagem (formato na seção 6) |
| • `imgLegenda` | o **descritivo**: uma frase dizendo o que a imagem mostra |
| • `imgDireito` | por que a imagem pode ser usada (licença conferida, divulgação oficial, arte da casa) |
| `imgFonte` | de onde veio (URL). Interno |
| • `apuracao` | lista de URLs abertas e lidas que sustentam o texto. **Interno: não sai no site.** Nunca usar `fontes` |
| • `publishAt` | ISO UTC com milissegundos (`2026-10-14T13:05:00.000Z`). Quente: a hora da publicação. Fria: o dia da fila às `10:00:00.000Z` (7h de Brasília) |
| • `criadoEm`, • `criadoPor`, • `origem` | o carimbo de criação, `Pedro Amaral`, `mesa-pedro` |
| `evento` | `{inicio, fim, local, cidade}` quando a matéria é sobre algo com data |
| `nomes_proprios` | nomes de obra com travessão oficial |
| `atualizadoEm`, `correcao` | só em correção (seção 8) |

Proibidos no pacote: `fontes`, `status`, `chefe`, `checagem`, `instagram`,
`sugestaoPublishAt`. As artes de Instagram saem sozinhas (o ateliê roda a cada
publicação em `import/novas/`).

**Formato do corpo:** parágrafos separados por linha em branco; `## ` para
intertítulo; `**negrito**` para nome de obra; `*itálico*`; `> ` para citação
real; `[texto](url)` para link (os internos do FOYER entram durante a
leitura, não no fim); `img:caminho | legenda | crédito` para foto no meio;
`video:URL` para trailer oficial no YouTube; `botao:Comprar ingressos | URL`
quando há venda oficial.

**Trailer (ordem do Pedro, 14/10/2026: "matérias de filme podem ter o
trailer junto, gosto de matérias bem completas").** Matéria de filme, série
ou especial leva o trailer oficial embutido (`video:` com o endereço do
YouTube do estúdio, da distribuidora ou da plataforma), logo depois do
trecho que apresenta a obra. Peça ou musical com teaser oficial no YouTube
também leva. O portão avisa quando uma matéria de Cinema, Streaming ou
Televisão sai sem a linha `video:`. Nunca embutir vídeo de terceiros
(reupload, fã, trecho pirata). Aspas tipográficas (“ ”). Serviço em `## Serviço`,
com uma linha por item.

## 6. A imagem: sempre existe uma, sempre com crédito e descritivo

Matéria sem imagem não sai. A hierarquia, do melhor para o de reserva:

1. **Divulgação oficial da obra que a matéria cobre**: sala de imprensa do
   estúdio, da plataforma, da produção ou da assessoria, ou a `og:image` do
   site oficial. Crédito: `Foto: Nome do Fotógrafo / Divulgação` (ou
   `Foto: Divulgação / Nome do Estúdio` quando não há fotógrafo). Baixar com
   `python3 tools/mesa_pedro.py capa --slug <slug> --url <URL>`.
2. **Wikimedia Commons com licença conferida pela API** (o script confere e
   recusa NC, ND e uso justo):
   `python3 tools/mesa_pedro.py capa --slug <slug> --commons "File:Nome.jpg"`.
   Crédito: `Foto: Autor / Wikimedia Commons (CC BY-SA 4.0)`; domínio
   público: `(domínio público)`. O script devolve crédito, fonte e direito
   prontos.
3. **Arte da casa** (`assets/artes/`, as seis artes de palco aprovadas pelo
   Pedro em 29/07/2026): `python3 tools/mesa_pedro.py capa --slug <slug>
   --arte 2`. Crédito `Arte: FOYER`. Serve a qualquer matéria, por isso
   **nunca há matéria sem imagem**. Escolha pelo conceito: 1 refletor (um
   nome, um artista), 2 cortina (estreia, temporada), 3 plateia (público,
   ingresso, bilheteria), 4 arena (disputa, dois lados), 5 urdimento
   (bastidor, dinheiro, trabalho), 6 degraus (carreira, prêmio, estreia de
   alguém).

Nunca: Getty, Reuters, AFP, Folhapress, Shutterstock, Alamy, foto de jornal
concorrente, foto de rede social de pessoa, frame de vídeo sem ser o trailer
oficial. Ilustração gerada por IA só se o Pedro a entregar ou pedir.

**Duas pessoas, duas na capa (ordem do Pedro, 14/10/2026).** Quando a matéria
é sobre duas pessoas famosas, ou gira em torno das duas, a capa leva as duas
lado a lado: `python3 tools/mesa_pedro.py capa-dupla --slug <slug>
--esquerda commons:File:A.jpg --direita commons:File:B.jpg` (ou `url:` para
divulgação). O crédito nomeia as duas fotos ("Fotos: X (esq.) e Y (dir.)"),
o descritivo diz quem está de cada lado. Uma só das duas na capa é erro.

**Matéria de filme, cena do filme (ordem do Pedro, 14/10/2026).** A capa de
matéria sobre filme ou série é uma cena da obra: still do material de
divulgação (sala de imprensa do estúdio ou da distribuidora, página oficial
do filme) ou o quadro do trailer oficial. Crédito "Foto: Divulgação / Nome do
Estúdio" (still) ou "Foto: Reprodução / Nome da Distribuidora" (quadro do
trailer). Retrato de ator em evento é a segunda opção, não a primeira.

O quadro do trailer sai do próprio YouTube, sem baixar o vídeo: cada vídeo
tem três quadros automáticos (`maxres1`, `maxres2`, `maxres3`), que são
cenas reais, ao contrário da miniatura principal, que costuma trazer o
texto "trailer oficial" e não serve de capa. O comando é
`capa --slug X --quadro URL_DO_YOUTUBE --n 2 --distribuidora "Universal
Pictures"`: ele tira as barras pretas, corta marcas do canal no topo com
`--corta-topo 72` quando houver, e põe o quadro de cinema (mais largo que
16:9) inteiro, em moldura, para não cortar ninguém das pontas. Olhe os três
(`--n 1`, `2`, `3`) antes de escolher: quadro com legenda queimada ou com
texto do canal não entra. Quando a matéria junta duas pessoas, o quadro
precisa mostrar as duas (regra da capa dupla).

Regras da capa: **16:9, até 1600 px de largura, rostos preservados.** Foto
em pé (retrato, cartaz) entra **inteira, em moldura**: sobre um fundo 16:9
feito dela mesma, desfocado e escurecido (`--foco auto`, o padrão). Recortar
foto em pé pelo terço superior (`--foco alto`) só quando ela tem corpo
inteiro e o rosto fica no alto; em retrato fechado o corte decapita. O site
não distorce imagem nunca.
**Trocar foto é arquivo novo com nome novo**, nunca sobrescrever (o navegador
guarda a imagem pelo nome).

**O descritivo (`imgLegenda`)** diz o que o leitor está vendo: quem, onde,
quando, em uma frase, sem repetir o título nem o crédito. É a legenda sob a
foto e o texto alternativo (leitor de tela e Google Imagens). Para arte da
casa: "Arte da identidade do FOYER: a cortina e a ribalta".

**O direito (`imgDireito`)** registra por que pode: "Divulgação oficial da
produção, baixada da sala de imprensa X em 14/10/2026", ou a licença com a
data da conferência, ou "arte própria do FOYER".

## 7. Guardar, aprovar e publicar

```
python3 tools/mesa_pedro.py confere pacote.json --rascunho   # o portão, sem hora ainda
python3 tools/mesa_pedro.py guarda pacote.json               # rascunho na mesa; nada no ar
python3 tools/mesa_pedro.py horarios --n 4                   # horários livres do relógio da casa
python3 tools/mesa_pedro.py publica <slug> --ok --em "15/10 09:00"   # SÓ depois da palavra do Pedro
python3 tools/mesa_pedro.py publica <slug> --ok --agora              # só se ele disse "agora"
python3 tools/mesa_pedro.py publica <s1> <s2> --ok --proximo-7h      # frias que ele aprovou, uma por dia
python3 tools/mesa_pedro.py descarta <slug> --motivo "..."           # ele recusou
```

**O `guarda`** grava o pacote em `import/mesa-pedro/<slug>.json` na branch de
produção, com a foto, num commit `[skip ci]`. O site não monta e, mesmo
quando monta, `so-o-site.sh` tira `import/` inteiro do que sobe: **rascunho
nunca aparece para o leitor**. Fica guardado no repositório, por isso
sobrevive à reciclagem deste ambiente. O relatório mostra os horários livres.

**O `publica`** só anda com `--ok` e uma hora. O que ele faz, nesta ordem:

1. **Resolve a cópia de produção.** O site é montado a partir da branch
   `claude/foyer-digital-redesign-14l2b6` (é dela que `pages.yml` publica e é
   nela que a Coxia grava). O script usa a pasta de trabalho atual se ela já
   estiver nessa branch; senão mantém uma cópia dela em `../FOYER-PRODUCAO`
   (worktree) e a atualiza com `fetch` + `rebase` antes de escrever.
2. **Converte a hora** como o Pedro escreve ("15/10 09:00", "09:00", ISO),
   em Brasília quando não há fuso, e recusa hora já passada.
3. **Confere o espaço**: a menos de 60 minutos de outra matéria dele, no ar
   ou agendada, recusa e manda olhar `horarios`. `--espaco 0` só se ele mandar.
4. **Move o rascunho** da mesa para `import/novas/`, carimba `publishAt`,
   roda o portão (reprovou, não publica), commit e push com a mensagem
   `Mesa do Pedro: publica "título"` (ou `agenda "título" para 15/10 às 9h`),
   e a linha "Autorizado pelo Pedro na conversa". Push rejeitado: `fetch`,
   `rebase`, tenta de novo, quatro vezes. Nunca força.
5. **Devolve o endereço**: `https://foyer.digital/post-<slug>.html`. Hora
   passada ou "agora": o `pages.yml` monta o site em 2 a 3 minutos. Hora
   futura: entra pelo relógio de `agendadas.yml`, que roda a cada 30 minutos,
   então sai até meia hora depois da hora marcada.

**Uma matéria por chamada** quando há hora marcada. Cada uma tem a sua, e
nunca duas juntas.

**Reconferir o fato na hora de publicar.** Entre a apuração e a autorização
podem passar horas. Bilheteria muda, elenco desmente, plataforma recua.
Antes do `publica`, abrir de novo a fonte principal da matéria; se o fato
mudou, avisar o Pedro antes de publicar, não depois.

## 8. Correção, troca de foto e remoção

Tudo nesta seção é pedido do Pedro, nunca iniciativa da mesa.

- **Corrigir** ("corrige a matéria X: o valor é Y"): editar o JSON na cópia
  de produção, acrescentar `atualizadoEm` e, quando o erro já foi lido, o
  campo `correcao: {"texto": "Correção: ...", "quando": ISO}` (o site imprime
  a nota no fim da matéria). Depois `publica <slug> --ok --corrige`, que
  aceita o slug existente e mantém o `publishAt` original.
- **Trocar a foto:** `capa` de novo (nome novo), apontar `img` para o novo,
  `publica <slug> --ok --corrige`.
- **Remover** ("tira a matéria X do ar"):
  `python3 tools/mesa_pedro.py remove <slug> --motivo "..."`. A matéria vai
  para `import/lixeira/` com `removidoEm`, `removidoPor` e o motivo, como a
  Coxia faz; o site remonta sem ela.
- **Reagendar:** `publica <slug> --ok --corrige --em "nova hora"`.

## 9. O portão (`confere`): o que reprova e o que avisa

Reprova (não publica): hora a menos de 60 minutos de outra matéria dele;
`publica` sem `--ok` ou sem hora; campo obrigatório faltando (`publishAt`
só no `publica`: o rascunho ainda não tem hora); `author` diferente de
Pedro Amaral; `cat` fora da lista ou `cats` com mais de 2; `fontes` ou
`status` no pacote; travessão fora de `nomes_proprios`; fórmula ou clichê da
seção 4.1; "ao FOYER"; "especialistas afirmam"; palavras fora da faixa do
porte; intertítulos fora da cota; menos de 15% de frases curtas ou média
acima de 28; parágrafo final de resumo; lista de tópicos em quente; primeiro
parágrafo todo em negrito; "hoje/ontem/amanhã/nesta/neste" no título; slug
repetido (fora de `--corrige`); imagem inexistente, fora de 16:9 ou com
agência proibida no crédito; legenda vazia ou igual ao título; menos de 2 URLs
em `apuracao`; fria fora das 10:00Z ou colidindo com outra do Pedro no mesmo
horário.

Avisa (publica, mas lê): título acima de 90 caracteres; frases curtas entre
15% e 20%; média entre 26 e 28; três parágrafos seguidos com o mesmo começo;
foto com menos de 1200 px de largura; só 2 URLs de apuração; travessão no
crédito; rodada inteira com o mesmo porte e a mesma conta de intertítulos
(molde); quente com `publishAt` a mais de uma hora de agora.

## 10. O relatório nesta conversa

A cada rodada (ou pedido de frias), o Pedro recebe aqui, para cada rascunho:

1. **Título** e **linha fina**; editoria principal e secundárias; porte e
   contagem de palavras.
2. **Foto**: crédito, descritivo e origem.
3. **O texto integral**, como vai sair.
4. Uma linha de **"o que ficou de fora"**: a candidata descartada e o motivo
   (sem repercussão, fato não confirmado, já saiu, não é pauta dele).

E, no fim, o bloco de decisão: **"Nada foi publicado."**, a lista dos
horários livres do relógio da casa (`horarios`) e a frase de como aprovar:
*"para publicar, diga qual e a hora: 'aprova a 1 para as 15h e a 2 para as
18h'"*. Depois disso a rodada para e espera.

Nada de descrever o processo: o Pedro lê a matéria, não o diário. Quando a
rodada sai vazia, o relatório diz as candidatas e por que nenhuma passou.

Quando ele responde, a mesa faz o que ele disse e devolve uma linha por
matéria: publicada (ou agendada), a hora e o endereço. Hora que fira o
espaço de 60 minutos: a mesa diz qual matéria está perto e propõe a hora
livre mais próxima, sem publicar.

## 11. Pontas soltas: o que fazer quando

| Se | Então |
|---|---|
| A rodada terminou e o Pedro não respondeu | Nada sai. Os rascunhos ficam na mesa; quente com mais de 24 h é descartado com uma linha no relatório seguinte |
| O Pedro aprova sem dizer a hora | A mesa propõe horários livres do relógio da casa, um por matéria, e espera a confirmação |
| O Pedro aprova duas para a mesma hora | A mesa publica a primeira e devolve a segunda com a hora livre mais próxima; só publica a segunda quando ele confirmar |
| O Pedro diz "agora" | `publica --ok --agora`; se houver matéria dele a menos de 60 min, a mesa avisa e pergunta antes |
| O Pedro diz "pode soltar todas" | Uma por horário do relógio da casa, com o espaço de 60 min; a mesa lista as horas e só então publica |
| Este ambiente foi reciclado entre a rodada e a aprovação | Os rascunhos estão em `import/mesa-pedro/` na branch de produção: `git fetch` e `publica <slug> --ok --em ...` funcionam de qualquer sessão |
| Nenhuma pauta passa nos quatro testes | Rodada vazia, com relatório das candidatas. Não se inventa quente |
| O fato central tem duas fontes com números diferentes | Vale a fonte oficial (produção, estúdio, bilheteria, órgão). Sem oficial, o número sai do texto |
| O fato é só um boato com um veículo | Não sai. Espera confirmação ou a resposta da parte, e entra na rodada seguinte |
| Não há foto de divulgação nem Commons | Arte da casa (seção 6). A matéria sai |
| A mesma pauta já saiu no FOYER (acervo ou fila) | Só com fato novo, e o texto diz o que mudou e linka a matéria anterior |
| A manhã publicou e a tarde tem o desdobramento | A tarde escreve o desdobramento como matéria nova, curta, linkando a da manhã. Não edita a da manhã |
| O Pedro pede frias e a fila das 7h vai longe | Entra depois da última mesmo assim, e o relatório diz as datas. Ele decide se adianta |
| O Pedro pede "publica amanhã às 9h" | `--em` com a hora em UTC (9h de Brasília é `12:00:00Z`) |
| O push é rejeitado quatro vezes | Para, mantém o pacote na cópia de produção, avisa aqui com o erro. Nunca força |
| O portão reprova | Corrige e roda de novo. Matéria reprovada não sai, mesmo que a correção seja "só uma palavra" |
| A rotina dispara e o repositório está numa branch sem este manual | Lê o manual da branch que o tem (`git show origin/<branch>:tools/PEDRO.md`); a publicação continua indo para a branch de produção |
| O evento da matéria ainda vai acontecer | "está marcado para", com dia e hora; nunca pretérito |
| A matéria quente envelhece entre a apuração e a publicação | Reconfere a fonte principal antes do `publica`; número velho não sai |
| Aspas só existem traduzidas | Veículo de origem nomeado no texto. Sem origem, sem aspas |
| O Pedro pede para parar as rodadas | Desligar as duas rotinas (update_trigger com enabled=false); nada mais muda |
| O Pedro escreve "corrige", "tira do ar", "troca a foto" | Seção 8, na hora, e o relatório diz o que mudou |
| O Pedro recusa um rascunho | `descarta <slug> --motivo`, e o motivo entra no registro |

## 12. Checklist de 60 segundos antes do `publica`

- O título diz o que o texto prova, e os 60 primeiros caracteres se sustentam?
- A linha fina acrescenta algo?
- O primeiro parágrafo tem fato, data e por que importa?
- Todo número tem fonte, período e unidade? Toda aspa foi localizada?
- O porte bate com o assunto, e o tamanho com o porte?
- Alguma frase bonita e imprecisa? Alguma seção que dá para trocar de lugar?
- A imagem tem direito, crédito, descritivo e corte 16:9?
- `apuracao` preenchido, `fontes` ausente?
- O fecho fecha o lide sem resumir e sem assunto novo?
- O Pedro explicaria essa matéria a um amigo em duas frases?
- **O Pedro autorizou esta matéria, com esta hora, nesta conversa?** Sem
  isso, o `publica` não roda.
