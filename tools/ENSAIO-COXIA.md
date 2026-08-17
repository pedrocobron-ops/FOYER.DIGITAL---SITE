# Ensaio geral da Coxia — 17/08/2026

Relatório de 13 agentes testadores que usaram a Coxia inteira (desktop, celular,
teclado, papéis de chefe e autor, e servidor de métricas em falha). Este arquivo
é o mapa das reformas: o que já foi feito está marcado na seção final.

# RELATÓRIO FINAL DO ENSAIO GERAL DA COXIA
Consolidado a partir de 13 testadores (desktop, celular, teclado, papéis de chefe e de autor, e cenário de servidor de métricas fora do ar)

---

## 1. O QUE ESTÁ BOM (mantenha como está)

- **A cara e a voz da casa.** Papel-creme, vinho e dourado com serifa de teatro; textos em português de gente (\"chave da casa\", \"terceiro sinal\", \"nada entra no ar sem a sua aprovação\"). Praticamente todos os 13 testadores elogiaram — é o maior patrimônio da Coxia.
- **O editor de Nova matéria** é o ponto mais redondo: espelho \"como sai no site\" ao vivo, rascunho salvo sozinho com hora, desfazer/refazer, pré-visualização com checklist honesto. Nota 8/10 do testador dedicado.
- **A busca da Fila** filtra ao vivo, mostra o que está na mesa de aprovação sobre o mesmo tema e tem ótima mensagem de vazio (\"tema livre para você lançar\").
- **O gerador de artes** (Instagram na Fila e banco de artes da Divulgação, com prévia redesenhada letra a letra) economiza trabalho de verdade. A Divulgação foi apontada como \"a tela mais bem acabada — deveria ser o gabarito das outras\".
- **O agendador de data e hora** é o melhor pedaço de desenho do app: sugestões em linguagem humana (\"amanhã às 9h · daqui a 10 horas\"), mapa do dia com o que já sai, e travas reais (choque com a revista de quinta, intervalo de 10 minutos, hora no passado).
- **As travas de segurança do fluxo de aprovação**: matéria sem capa não aprova, matéria assinada só é liberada pelo dono da assinatura, e sem a \"chave da casa\" nada publica.
- **Solidez técnica**: zero erros de JavaScript em TODOS os 13 roteiros, mesmo com o servidor de dados devolvendo erro. No celular nada transborda da tela e os botões principais têm 44px.

---

## 2. BUGS REAIS CONFIRMADOS (do mais grave ao menor)

**B1 — As permissões são cenário, não parede (segurança).** Entrando como autor comum: no Calendário → perguntas de terça → \"montar a página na aba Revista →\" abre a **Revista inteira** (escondida do menu) em 2 cliques; os botões Sim/Não e o checklist do fechamento **gravam decisões editoriais** sem checar o papel; a aba **Publicidade** fica 100% aberta (\"Trocar a arte\", \"Tirar do ar\"); e disparando o clique do item oculto, a **Redação IA abre completa** com \"Aprovar as selecionadas\". *Conserto: conferir o papel DENTRO de cada tela restrita, não só esconder o item do menu.*

**B2 — Revista: despublicação silenciosa.** Passos: sem chave, clicar \"Despublicar\" numa edição publicada → vem o erro de chave (certo), mas o status já mudou na memória. Depois, conectar a chave e clicar só \"Salvar rascunho\" → o arquivo é gravado como rascunho e **a edição sai do site**, com a etiqueta ainda dizendo PUBLICADA. *Conserto: após falha, devolver o status; ou avisar \"esta gravação vai DESPUBLICAR a Nº 4 — continuar?\".*

**B3 — Fila → Editar: o dropdown \"Editoria principal\" abre vazio** para matérias das editorias \"Memória\" e \"Entenda\", porque elas não existem entre as 21 opções da lista. Quem salvar sem notar **grava a matéria sem editoria**. *Conserto: adicionar as duas à lista e bloquear o salvar com editoria vazia.*

**B4 — Revista: o lápis ✎ duplica páginas automáticas** (agenda, programas, frase-célebre, expediente) em vez de editar — a edição Nº 4 do acervo já está com a agenda duplicada (páginas 11 e 12). *Conserto: no ✎ dessas páginas, mostrar \"esta página se monta sozinha\".*

**B5 — Servidor de métricas fora do ar vira mentira confiante (apontado por 6 testadores — o problema mais repetido do ensaio).** Com o Supabase em erro:
- **Métricas** mostra \"0 visitas de gente em 7 dias\" como dado real, \"o pico foi 1\", \"nenhuma passagem de máquina — todo o movimento é de gente\", e o **CSV oficial baixa inteiro de zeros com toast \"Relatório baixado ✓\"** (arquivo que poderia parar na mão de anunciante). Causa: a função de carga não confere se a resposta do servidor veio boa (`response.ok`).
- **Saguão**: \"Placar das assinaturas\" fica em \"Carregando…\" **para sempre** (3 testadores).
- **Revista**: \"Enviar aos assinantes\" diz \"Ainda não há assinantes ativos\" quando na verdade a contagem falhou.
- **Publicidade**: anúncio no ar mostra \"0 vistas, 0 cliques\" e a fileira dos 5 cartões do funil fica vazia sem mensagem.
- **Palco**: dois \"?\" gigantes sem explicação nem botão de tentar de novo.
*Conserto único: distinguir \"zero de verdade\" de \"sem resposta\" (travessão + aviso \"o medidor não respondeu — tentar de novo\") em todos esses painéis.*

**B6 — Fila com rede caída mente: \"Nenhuma matéria por aqui ainda\".** Com o GitHub em erro, a Fila mostra estado vazio (parece que 174 matérias sumiram) enquanto a Lixeira, na mesma tela, mostra \"Erro ao carregar\". Causa: os erros de rede são engolidos por um `catch` que devolve lista vazia — o bloco de erro com \"Tentar de novo\" existe no código e nunca roda.

**B7 — O \"Pular para o conteúdo\" expulsa da Coxia.** Primeiro Tab + Enter navega para a capa do site público (o `<base href=\"../\">` manda o link para fora de /coxia/). Quem usa teclado sai da central no primeiro Enter.

**B8 — Lixeira quebrada no celular**: títulos numa coluna de 79px, uma palavra por linha, cards de 400px. Causa: um estilo fixo dentro do HTML (grid de colunas na linha ~5323) que atropela o ajuste de tela pequena. Conserto de 1 linha.

**B9 — Revista: só de abrir \"Prever o e-mail\", a 4ª chamada de capa é descartada** da edição em memória (\"foram descartadas\", no passado, sem cancelar) — se salvar em seguida, some do arquivo. E qualquer clique marca \"alterações não salvas\" sem o usuário ter digitado nada.

**B10 — Publicar recado no mural / sugerir pauta não confirma nada**: a caixa esvazia, nenhum \"publicado ✓\", e o item pode nem aparecer na lista (a tela depende de reler o GitHub em vez de mostrar o que acabou de gravar). O autor também: matéria \"Enviada para a mesa do chefe ✓\" **não aparece em lugar nenhum** que ele veja depois — parece que sumiu.

**B11 — Sair da edição joga no lugar errado**: \"Cancelar edição\" (no celular) devolve ao Palco perdendo a posição na Fila; \"Salvar edição\" (mesa) aterrissa no meio do Diário sem nenhuma confirmação visível.

**B12 — Equipe: \"Excluir\" uma pessoa não pede confirmação** — um clique errado do chefe apagaria alguém da equipe.

**B13 — Conexão: diagnósticos contraditórios e em dialeto técnico**: com chave inválida, a tela afirma ao mesmo tempo \"A chave é válida, mas…\" e \"Não deu para falar com o GitHub\"; \"Conferir\" com campo vazio manda \"confira a internet\"; falha de servidor responde \"sem sessão\"; \"Desconectar\" não confirma nem limpa o campo.

**B14 — Miudezas confirmadas**: badge \"16\" da Redação IA não acompanha a mesa (conta matérias devolvidas que a mesa esconde); \"INVALID DATE — 0 matéria(s)\" no Diário (uma rodada em formato antigo); \"Conferido pelo checador independente checador independente\" (rótulo duplicado); título cortado sem \"…\" no modal de agendamento; Divulgação promete PNG e baixa JPG; subtítulo da Publicidade cita o formato \"Faixa\", que não existe (chama-se \"O Cartaz\"); calendário deixa navegar para mês inteiro no passado; overlay do Instagram não fecha com Esc no celular.

---

## 3. MELHORIAS DE USO (por impacto no dia a dia do dono)

### Fila & agendadas — a aba mais usada, e a que mais esconde o que ele vem ver
1. **Inverter a ordem dos blocos** (2 testadores mediram): hoje são 2.038px (2,3 telas) até a primeira matéria e mais de 5 telas até a primeira publicada. Nova ordem: **busca → lista de matérias**; a grade da semana e o \"Vão sair\" descem ou nascem **fechados** (o cabeçalho \"VÃO SAIR (28)\" já parece clicável — fazer dele o abre/fecha, mostrando só as próximas 3–5).
2. **Parar de repetir as 28 agendadas duas vezes** (linhas do \"Vão sair\" + os mesmos 28 cards completos). Ou o bloco substitui os cards, ou a lista ganha filtros no topo: **No ar | Agendadas | Lixeira** (2 testadores).
3. **Ordenar agendadas da mais próxima para a mais distante** — hoje a de 02/09 vem antes da que sai amanhã às 10h.
4. **Tornar clicáveis** as linhas do \"Vão sair\" e os itens da grade da semana, levando ao card/Editar (2 testadores: hoje é \"texto morto\").
5. **Subir o \"Buscar no acervo\"** (está a 19.173px do topo — ninguém descobre) ou fundir seus filtros na busca do topo; e o contador \"(28)\" deve acompanhar o filtro da busca (2 testadores).
6. Com 174 cards, **paginar/carregar aos poucos** + botão flutuante \"voltar ao topo\".

### Redação IA — a segunda maior dor
7. **Modo triagem** (2 testadores): cards de 2.400–4.300px transformam 16 matérias em ~50.000px de rolagem. Colapsar parecer/ressalvas/laudo num resumo de 3 linhas com \"ver completo\", e **fixar a régua de ações** (Aprovar/Agendar/Recusar) na tela enquanto o card estiver visível.
8. **Recusar com motivo registrado** — hoje a decisão evapora e não há como devolver uma matéria da IA à esteira com recado.
9. A confirmação \"Aprovar e publicar?\" deve **dizer o título** da matéria.

### Transversais (aparecem em várias abas)
10. **Toda mensagem \"Vá na aba Conexão…\" ganha um botão \"Ir para Conexão\"** (3 testadores) — hoje é beco sem saída; e a Nova matéria deve avisar da falta de chave ANTES de a pessoa escrever 800 palavras.
11. **Todo painel que falha por servidor ganha \"Tentar de novo\"** e a nota \"isso não afeta o site no ar\" (Métricas, Placar, Diário de atividades, funil da Publicidade).
12. **Feedback perto da ação**: \"Salvo ✓\" da Revista colado na barra de botões (não no pé da página); toast com \"Desfazer\" no \"Já postei\" do Instagram; botão \"Atualizar os números\" das Métricas vira \"Buscando…\" e anuncia o resultado.
13. **Palco**: limitar \"Para postar no Instagram\" a 5 cards com \"ver todas as 41\" (2 testadores — hoje são 5.500px engolindo o painel) e mostrar \"Hoje saem 3: 8h, 12h, 18h\".
14. **Nova matéria**: dar acesso permanente à prateleira de rascunhos (botão \"Rascunhos (2)\" — hoje ela só aparece com o formulário vazio, apesar do selo no menu); e a régua de porte dizer o alvo (\"faltam 227 palavras para 350–500\") em vez de \"fora das faixas\".
15. **Celular**: subir a fonte dos campos de busca para 16px (evita o zoom automático do iPhone) e voltar da edição para a Fila, na posição em que estava.
16. **Revista**: um botão \"Folhear a edição\" para ver o rascunho antes de publicar — hoje se publica às cegas.

---

## 4. MELHORIAS DE DESIGN

### As 6 regras gerais que tiram o ar de \"mal acabado\" (aplicar em uma passada, em todas as abas)
1. **Um só padrão de título de aba**: Calendário e Publicidade abrem com título pequeno enquanto Saguão/Revista/Equipe/Conexão têm o serifado gigante (3 testadores) — todas iguais.
2. **Três estilos de botão e ponto** (4 testadores): primário (vinho), secundário (contorno), terciário (texto) — mesma altura, mesma capitalização. Hoje convivem \"LIGAR ESTE APARELHO\" (preto caps), \"Instalar a Coxia como app\" (vinho), \"limpar\" (minúsculo), \"Restaurar\", e os toggles da revista **sem CSS nenhum** (botão cru de navegador).
3. **Nunca cortar texto no meio da palavra** (4 testadores): sempre reticências \"…\" — grade da semana, prateleira de rascunhos, modal de agendamento, placeholder da busca.
4. **Um único componente de vazio/erro**: hoje são cinco versões (\"Carregando…\" eterno, \"?\", zeros, \"sem dados\", \"NÃO DEU PARA CARREGAR\" em caixa alta). Um padrão só: travessão + frase completa + \"tentar de novo\", com erro visualmente distinto de vazio.
5. **Plural de verdade** (5 testadores): \"16 matéria(s)\", \"há 25 dia(s)\", \"9 item(ns)\", \"1 anúncio(s)\" → o código escolhe singular/plural. É a marca de descuido mais citada.
6. **Mono em caixa alta é etiqueta de 1 linha** (SEG 10, PUBLICADA), nunca texto corrido: créditos de foto, pareceres e erros vão em fonte de leitura. E teto de densidade: lista longa corta em N itens com \"ver todas\".

### Os piores detalhes por aba
- **Fila**: coluna de botões desalinha ~100px quando existe \"Versões\"; título \"Fila & agendadas\" nasce decapitado atrás do cabeçalho fixo; botão \"Excluir de vez\" quebra em 2 linhas ao lado do \"Restaurar\" de 1; 174 títulos em CAIXA ALTA gritada.
- **Redação IA**: crédito da foto = muro preto de 7 linhas mono sobre a imagem (\"parece stack trace\"); parecer de 1.627px com frases inteiras em caixa alta; hora \"09:00 AM\" em interface toda 24h.
- **Calendário**: o rótulo \"0 de 9 · 0%\" **clipado por cima da caixa \"Hoje na casa\"** (3 testadores — o defeito visual mais citado); botões de hora colados na borda do modal; botão desabilitado idêntico ao habilitado; ✦ em todos os dias do mês não informa nada.
- **Métricas**: barra da \"régua honesta\" vazia com lasquinhas de 4px e glifo vazando da borda (2 testadores); \"Ainda sem registros\" solto e pequeno; setinha ↗ em cartões que não são clicáveis; numeração 7,9/8,10 embaralhada em duas colunas (2 testadores).
- **Nova matéria**: caixas de ajuda idênticas a campos de digitação; coluna direita vazia por 70% da página; fileira final de botões desalinhada (o \"Enviar\" é um quadrado alto entre retângulos baixos).
- **Equipe/Conexão**: duas larguras de coluna brigando; campo do token sem título, colado no bloco \"Coxia no celular\" (3 testadores); moldura dupla nos cartões de pessoa; erro escondido ABAIXO do botão.
- **Saguão/Palco**: \"✓ Já postei\" é o botão mais chamativo sendo o que menos se quer clicar; topo repete \"16 na mesa\" três vezes; toast cobrindo botões; conflito de nomes \"Palco\" (aba) vs \"Palco de honra\" (quadro).
- **Revista/Publicidade**: aviso sobre aviso (modal em cima da prévia do e-mail); datas ISO (\"2026-08-24\") misturadas com dd/mm na mesma linha (2 testadores); \"VENDIDO\" para vaga ocupada pela própria casa; sidebar com o botão \"Instalar como app\" quebrado em 2 linhas e vão enorme até o relógio (2 testadores).

---

## 5. PLANO EM 3 ETAPAS

### HOJE (consertos pequenos que evitam perda de dados ou vergonha — quase todos de poucas linhas)
1. Adicionar \"Memória\" e \"Entenda\" ao dropdown de editoria (B3).
2. Revista: reverter o status após falha de despublicação (B2) e neutralizar o lápis das páginas automáticas (B4).
3. Métricas: conferir a resposta do servidor — erro mostra aviso + \"Tentar de novo\", nunca zeros; bloquear o CSV sem dados (B5).
4. Fila: remover os `catch` silenciosos para o erro de rede aparecer com o \"Tentar de novo\" que já existe no código (B6).
5. Consertar o \"Pular para o conteúdo\" (B7) e o grid da Lixeira no celular (B8).
6. Reticências na grade da semana e demais cortes de texto; consertar o \"Carregando…\" eterno do Placar.
7. Confirmação antes de excluir pessoa da Equipe (B12) e \"Recado publicado ✓\" no mural (B10).

### ESTA SEMANA (as duas grandes reorganizações + segurança)
1. **Reordenar a Fila**: busca → lista; grade da semana e \"Vão sair\" colapsados; agendadas por proximidade; filtros No ar/Agendadas/Lixeira; linhas clicáveis.
2. **Modo triagem na Redação IA**: cards colapsados + régua de ações fixa + recusa com motivo.
3. **Checar o papel dentro de cada tela restrita** (Revista, Redação IA, Publicidade, Métricas, Equipe) — fechar o vazamento do autor (B1).
4. Botão \"Ir para Conexão\" em toda mensagem de chave; aviso de falta de chave no topo da Nova matéria.
5. Palco: Instagram limitado a 5 + \"hoje saem X às…\"; matéria enviada pelo autor aparece na Fila dele com selo \"na mesa do chefe\".
6. Voltar da edição para o lugar certo (Fila/mesa) com confirmação visível.
7. Reescrever os diagnósticos da Conexão (uma área de status única, sem \"sem sessão\" nem \"confira a internet\" falso).

### DEPOIS (o polimento que muda a nota geral)
1. Aplicar as 6 regras de design numa passada única (títulos, 3 botões, reticências, componente único de vazio/erro, plurais, mono-só-etiqueta) — é o que os testadores estimam levar o acabamento de 5,5 para 8,5 **sem redesign**.
2. Acessibilidade dos modais: prender o Tab dentro, devolver o foco ao fechar, Esc em todos.
3. Revista: \"Folhear a edição\" antes de publicar; prévia que não mexe nos dados (B9); resolver a numeração prometida do Sumário.
4. Paginação da Fila; unificar as duas buscas; guardar a última carga boa das métricas (\"números de ontem às 18h\").
5. Miudezas do B14 (badge, Invalid Date, PNG/JPG, \"Faixa\", datas e horas em padrão brasileiro dd/mm e 24h em tudo).

---

**Resumo em uma frase**: o motor da Coxia é bom e ninguém encontrou uma tela morta — os três males são **ordem errada** (a Fila e a Redação IA escondem o que o dono vem ver atrás de telas de rolagem), **mentiras sob falha** (zeros e \"Carregando…\" quando o servidor cai, o problema mais repetido: 6 de 13 testadores) e **cerca de permissões só de fachada**; tudo consertável em consertos localizados, sem mexer na estrutura.",
    "ensaios": 13
  },
  "workflowProgress": [
    {
      "type": "workflow_phase",
      "index": 1,
      "title": "Ensaios"
    },
    {
      "type": "workflow_phase",
      "index": 2,
      "title": "Síntese"
    },
    {
      "type": "workflow_agent",
      "index": 1,
      "label": "ensaio:fila-desktop",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "af35832373b655916",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786921068832,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Fila & agendadas (data-go=\"fila\"), testada no desktop 1366×…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786921762283,
      "tokens": 99192,
      "toolCalls": 40,
      "durationMs": 693223,
      "resultPreview": "{\"aba\":\"Fila & agendadas (data-go=\\\"fila\\\"), testada no desktop 1366×900 como Pedro Amaral (chefe da casa)\",\"bom\":[\"A busca do topo é ótima: filtra ao vivo enquanto digita, esconde a grade da semana, mostra contagem clara (\\\"16 matéria(s) na fila e agendadas + 1 na mesa\\\") e ainda revela matéria esperando aprovação que nem aparece na visão normal\",\"O gerador de post de Instagram direto do card é u…"
    },
    {
      "type": "workflow_agent",
      "index": 2,
      "label": "ensaio:fila-celular",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "acddec96272365295",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786921067893,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Fila & agendadas (celular 390x844, papel chefe)",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786921634597,
      "tokens": 86290,
      "toolCalls": 44,
      "durationMs": 566702,
      "resultPreview": "{\"aba\":\"Fila & agendadas (celular 390x844, papel chefe)\",\"bom\":[\"Nada transborda na horizontal: com 174 cards carregados, scrollWidth ficou exatamente em 390px em toda a aba — nenhum elemento vaza da tela.\",\"O menu de abas rola de lado com uma sombra em degradê na borda direita avisando que há mais abas depois de 'Fila & agendadas' — a aba cortada não parece defeito.\",\"Os botões dos cards (📱 Inst…"
    },
    {
      "type": "workflow_agent",
      "index": 3,
      "label": "ensaio:nova-materia",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a94db7b75d2cfb7d9",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786921638718,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Nova matéria (data-go=\"nova\")",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786922176574,
      "tokens": 121214,
      "toolCalls": 47,
      "durationMs": 537855,
      "resultPreview": "{\"aba\":\"Nova matéria (data-go=\\\"nova\\\")\",\"bom\":[\"O espelho ao vivo é o ponto alto: escrevi '## Uma temporada de recordes' e '**sessao extra de despedida**' e o painel da direita mostrou na hora o intertítulo com sublinhado dourado e o negrito, com a mesma tipografia do site; e o parágrafo onde está o cursor fica destacado com uma barrinha vinho — dá segurança total para quem não sabe markdown\",\"O …"
    },
    {
      "type": "workflow_agent",
      "index": 4,
      "label": "ensaio:mesa-ia",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "afb3129efab0e3f3c",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786921765389,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Redação IA (data-go=\"ia\") — Mesa de aprovação e Diário da r…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786922605453,
      "tokens": 146036,
      "toolCalls": 62,
      "durationMs": 840064,
      "resultPreview": "{\"aba\":\"Redação IA (data-go=\\\"ia\\\") — Mesa de aprovação e Diário da redação, testada como chefe (Pedro Amaral) em 1366x900, com ~35 screenshots lidos\",\"bom\":[\"O modelo mental é claro logo no topo: 'Pauteiro → Repórter → Editor de Estilo → Chefe de Redação → você. Nada entra no ar sem a sua aprovação' — um leigo entende na hora quem fez o quê.\",\"O card da matéria reúne tudo que um chefe precisa: no…"
    },
    {
      "type": "workflow_agent",
      "index": 5,
      "label": "ensaio:saguao-palco",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a7a065d11e290e9ed",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786922179917,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Saguão + Palco (primeiro olhar do dia)",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786922516396,
      "tokens": 84651,
      "toolCalls": 29,
      "durationMs": 336478,
      "resultPreview": "{\"aba\":\"Saguão + Palco (primeiro olhar do dia)\",\"bom\":[\"A identidade visual é coerente e charmosa: papel bege, vinho e dourado, título serifado grande ('Boa noite, Pedro', 'Saguão') — não parece template genérico.\",\"A linguagem é humana e teatral em tudo: 'Deixe um recado para a equipe…', 'Matéria sua no topo? Print no mural, claro', 'puxa a fila' — um leigo entende sem manual.\",\"A saudação do Pal…"
    },
    {
      "type": "workflow_agent",
      "index": 6,
      "label": "ensaio:revista",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "aa447361de343e9e2",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786922519470,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Revista (data-go=\"revista\")",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786923151239,
      "tokens": 125828,
      "toolCalls": 54,
      "durationMs": 631768,
      "resultPreview": "{\"aba\":\"Revista (data-go=\\\"revista\\\")\",\"bom\":[\"A lista de edições é clara para leigo: Nº + manchete em negrito, contagem de páginas, data de capa e 'última mexida: quem' numa linha só; a pill PUBLICADA (grená) fica evidente à primeira vista.\",\"Os textos são exemplares em linguagem de gente: 'Feche a edição da semana', 'a capa não imprime mais que isso', 'ideal em pé (3×4) — a Coxia ajusta sozinha'…"
    },
    {
      "type": "workflow_agent",
      "index": 7,
      "label": "ensaio:calendario",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a6a8edfffd40fe927",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786922608545,
      "queuedAt": 1786921064901,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Calendário",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786923053887,
      "tokens": 116853,
      "toolCalls": 43,
      "durationMs": 445341,
      "resultPreview": "{\"aba\":\"Calendário\",\"bom\":[\"O trilho \\\"A semana da revista\\\" conta o ritual em linguagem humana (sexta nasce o boneco, terça 12h perguntas, quarta 18h congela, quinta 7h sai) — um leigo entende o fluxo sem manual.\",\"A caixa \\\"Hoje na casa\\\" muda de tom de verdade: simulei quarta-feira 15h e ela ficou vermelha com \\\"3 perguntas de terça sem resposta\\\" e \\\"9 item(ns) do fechamento em aberto — a ediç…"
    },
    {
      "type": "workflow_agent",
      "index": 8,
      "label": "ensaio:publicidade-divulgacao",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a72d986409165ca13",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786923057444,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Publicidade (data-view=\"pub\") e Divulgação (data-view=\"divu…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786923701355,
      "tokens": 139506,
      "toolCalls": 62,
      "durationMs": 643910,
      "resultPreview": "{\"aba\":\"Publicidade (data-view=\\\"pub\\\") e Divulgação (data-view=\\\"divulgacao\\\") — observação: não existe data-go=\\\"publicidade\\\"; a aba real chama-se \\\"pub\\\" no menu\",\"bom\":[\"O funil de anunciantes em 5 cartões (R$ fechado no mês, em negociação, esperando resposta, no ar agora, pedidos no mês) é imediatamente compreensível e o cartão de dinheiro tem destaque dourado correto\",\"A primeira mensagem d…"
    },
    {
      "type": "workflow_agent",
      "index": 9,
      "label": "ensaio:equipe-conexao",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a0db5f7ee3cce336d",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786923154872,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Equipe, Conexão e Portão de entrada (login)",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786923622911,
      "tokens": 92675,
      "toolCalls": 42,
      "durationMs": 468038,
      "resultPreview": "{\"aba\":\"Equipe, Conexão e Portão de entrada (login)\",\"bom\":[\"O portão de entrada é a tela mais bonita da Coxia: metade vinho com o logo FOYER/Coxia em serifa dourada, metade creme com o formulário; o botão 'TERCEIRO SINAL — ENTRAR' é um achado de tema teatral que dá personalidade sem atrapalhar o entendimento\",\"A linguagem quase sempre foge do jargão: 'A chave da casa — guardada uma vez, vale para…"
    },
    {
      "type": "workflow_agent",
      "index": 10,
      "label": "ensaio:metricas",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "ad53e724b1d1627b2",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786923625943,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Métricas (data-go=\"metricas\"), incluindo o painel \"12. Leit…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786923909345,
      "tokens": 84521,
      "toolCalls": 28,
      "durationMs": 283401,
      "resultPreview": "{\"aba\":\"Métricas (data-go=\\\"metricas\\\"), incluindo o painel \\\"12. Leitores cadastrados\\\" — testada como chefe, com o Supabase respondendo erro 500 de propósito, em desktop (1366px) e celular (390px)\",\"bom\":[\"A estrutura editorial das 12 seções numeradas com títulos em linguagem de gente (\\\"1. Quanta gente leu\\\", \\\"2. O quanto disso é certeza\\\", \\\"a régua honesta\\\") é excelente para um dono leigo: …"
    },
    {
      "type": "workflow_agent",
      "index": 11,
      "label": "ensaio:design-geral",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a5201a6efe761aec8",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786923704317,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "todas as 12 abas (Palco, Saguão, Nova matéria, Fila & agend…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786924273176,
      "tokens": 107749,
      "toolCalls": 46,
      "durationMs": 568859,
      "resultPreview": "{\"aba\":\"todas as 12 abas (Palco, Saguão, Nova matéria, Fila & agendadas, Redação IA, Revista, Calendário, Publicidade, Divulgação, Equipe, Métricas, Conexão) — visão de conjunto do diretor de arte, desktop 1366px\",\"bom\":[\"A identidade visual tem personalidade de verdade: papel-creme + vinho + dourado com serifas de cartaz de teatro. Os H1 gigantes de Saguão, Revista, Equipe e Conexão são bonitos e…"
    },
    {
      "type": "workflow_agent",
      "index": 12,
      "label": "ensaio:teclado-erros",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "a8f735c06afbeaf79",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786923912235,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Nova matéria (teclado) + overlays + Fila & agendadas e Reda…",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786924488738,
      "tokens": 108709,
      "toolCalls": 45,
      "durationMs": 576502,
      "resultPreview": "{\"aba\":\"Nova matéria (teclado) + overlays + Fila & agendadas e Redação IA/Mesa (rede cortada) — acessibilidade e estados de erro\",\"bom\":[\"Foco visível consistente em todo o formulário da Nova matéria: anel dourado de 2-3px em cada uma das 28 paradas de Tab (título, selects de editoria, dropzone de foto, os 12 botões da barra de formatação, texto, botões finais) — nenhum ponto cego de foco\",\"Ordem …"
    },
    {
      "type": "workflow_agent",
      "index": 13,
      "label": "ensaio:autor-comum",
      "phaseIndex": 1,
      "phaseTitle": "Ensaios",
      "agentId": "aec003ff4158be90f",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786924276435,
      "queuedAt": 1786921064902,
      "attempt": 1,
      "lastToolName": "StructuredOutput",
      "lastToolSummary": "Experiência do autor comum (papel 'autor'): Palco, Saguão, …",
      "promptPreview": "Você é um testador que USA de verdade a Coxia, a central de controle do portal FOYER (jornalismo de teatro; o dono, Pedro, não é programador). A Coxia roda em http://127.0.0.1:8899/coxia/ com um palco de ensaio pronto: o módulo /tmp/claude-0/-home-user-FOYER-DIGITAL---SITE/f37f0ffb-9910-580a-ab0e-fc5b410d1ab8/scratchpad/ensaio-lib.js exporta abre({papel, viewport}) e devolve {browser, page, errosD…",
      "lastProgressAt": 1786924891614,
      "tokens": 123264,
      "toolCalls": 54,
      "durationMs": 615178,
      "resultPreview": "{\"aba\":\"Experiência do autor comum (papel 'autor'): Palco, Saguão, Nova matéria, Fila, Calendário, Publicidade, Divulgação, Conexão — e tentativas de chegar às abas escondidas (Redação IA, Revista, Equipe, Métricas)\",\"bom\":[\"A linguagem é humana e explica o porquê: a nota lateral da Nova matéria muda para o autor (\\\"Como funciona: sua matéria vai para a mesa do chefe, que aprova e programa a publi…"
    },
    {
      "type": "workflow_agent",
      "index": 14,
      "label": "relator",
      "phaseIndex": 2,
      "phaseTitle": "Síntese",
      "agentId": "a79f7a3ee76de351f",
      "model": "claude-fable-5",
      "state": "done",
      "startedAt": 1786924897520,
      "queuedAt": 1786924893818,
      "attempt": 1,
      "promptPreview": "Você é o relator do ensaio geral da Coxia (central de controle do portal FOYER; o dono, Pedro, não é programador — escreva sem jargão, em português). Abaixo, os relatórios de 13 testadores que usaram cada canto da central. Produza UM relatório final: (1) O QUE ESTÁ BOM (curto); (2) BUGS REAIS confirmados, do mais grave ao menor, com passos; (3) MELHORIAS DE USO priorizadas por impacto no dia a dia…",
      "lastProgressAt": 1786925039479,
      "tokens": 83108,
      "toolCalls": 0,
      "durationMs": 141958,
      "resultPreview": "# RELATÓRIO FINAL DO ENSAIO GERAL DA COXIA
Consolidado a partir de 13 testadores (desktop, celular, teclado, papéis de chefe e de autor, e cenário de servidor de métricas fora do ar)

---

## 1. O QUE ESTÁ BOM (mantenha como está)

- **A cara e a voz da casa.** Papel-creme, vinho e dourado com serifa de teatro; textos em português de gente (\"chave da casa\", \"terceiro sinal\", \"nada entra no ar sem …"
    }
  ],
  "totalTokens": 1519596,
  "totalToolCalls": 596
}

---

## JÁ FEITO (17/08/2026, na sequência do ensaio)
- Fila & agendadas reordenada: busca → filtros (Todas/No ar/Agendadas) → lista;
  grade da semana e "Vão sair" viraram gavetas fechadas com resumo; agendadas
  ordenadas da mais próxima para a mais distante; linhas do "Vão sair" clicáveis
  levam ao card (rolagem até a 1ª matéria: de ~2.038px para ~440px).
- B3: editorias Entenda e Memória adicionadas ao seletor (não grava mais matéria sem editoria).
- B6: Fila sem rede agora mostra o erro com "Tentar de novo" em vez de "Nenhuma matéria por aqui".
- B12 conferido: a exclusão de pessoa da Equipe JÁ pede confirmação (falso positivo do ensaio).

## JÁ FEITO (17/08/2026, lote aprovado pelo Pedro: itens 4-11, 13-16 + design 17-22)
- Itens 6-8: mesa da Redação IA em modo triagem — cards resumidos (capa baixa,
  parecer em 3 linhas, ~430px em vez de ~4.900px) com "Ver completo"; régua de
  decisão fixa no pé da tela com o dossiê aberto; recusa pede motivo e ele fica
  registrado na lixeira; confirmação de aprovar diz o título.
- Item 4: a busca do topo da Fila também conta o acervo completo, com botão que
  leva à busca do acervo já preenchida.
- Item 5: linhas da Fila com content-visibility:auto + botão flutuante "↑ topo".
- Item 9: todo aviso de chave virou diálogo com "Ir para Conexão"; a Nova matéria
  avisa da falta de chave antes de a pessoa escrever.
- Item 10: diagnósticos da Conexão reescritos (sem "chave válida" contraditório,
  sem "confira a internet" falso); Desconectar confirma e limpa tudo.
- Item 11: "Salvo ✓" em toast na revista, perto do botão.
- Item 13: botão permanente "Rascunhos (N)" abre a prateleira mesmo com texto na tela.
- Item 14: régua de porte com alvo ("faltam 250 palavras para 350–500").
- Item 15: autor que envia matéria cai na Fila e vê o selo "Na mesa do chefe".
- Item 16: "Folhear a edição" no editor da revista — rascunho ganha prova de
  gráfica (revista-prova-N.html, noindex, fora do sitemap/estante, some ao publicar).
- Design 17-22: títulos padronizados (Calendário/Publicidade/Divulgação); troca de
  aba volta ao topo; botões no padrão (Conexão sem caps, setas do espelho, Limpar);
  reticências em todo corte (helper corta); erro distinto de vazio com "Tentar de
  novo" (lixeira/diário/mural/sugestões); plural de verdade (helper plural);
  crédito de foto em fonte de leitura; datas sem segundos; barra do calendário sem
  clipe; agendador não navega ao passado; coluna de ações da Fila alinhada.
- Fora do lote (decisão do Pedro): item 12 (limitar o Palco Instagram a 5).
