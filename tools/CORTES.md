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
