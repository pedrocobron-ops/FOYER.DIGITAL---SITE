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
