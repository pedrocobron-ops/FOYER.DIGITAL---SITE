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
