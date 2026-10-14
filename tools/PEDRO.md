# A mesa do Pedro: matérias assinadas por Pedro Amaral, publicadas direto

Manual do fluxo em que o Claude pesquisa, escreve e **publica no site** as
matérias assinadas por Pedro Amaral, por ordem dele (14/10/2026). Substitui o
trabalho que ele fazia no ChatGPT e colava à mão na Coxia.

Este fluxo tem dois produtos:

| Produto | Quando | Quantas | Vai ao ar |
|---|---|---|---|
| **Pautas quentes** | todo dia, rodadas das **7h** e das **17h** (Brasília), automáticas, nesta conversa | 1 a 3 por rodada (2 é o normal) | na hora, assim que a matéria passa no portão |
| **Pautas frias** | quando o Pedro pede nesta conversa ("escreva N pautas frias") | o número que ele pedir | agendadas, **uma por dia às 7h**, na fila depois da última já marcada |

Ferramenta de apoio: `tools/mesa_pedro.py` (foto de capa, portão, fila das 7h,
publicação, remoção). Tudo o que ele confere está descrito aqui; o script é o
braço, este manual é a régua.

## 0. O que vale daqui e o que vale de lá

`tools/REDACAO.md` é o manual da **Redação IA** (a mesa de aprovação da Coxia,
que assina "Redação Foyer" e hoje está desligada). Ele continua valendo para o
que é verdade e método: **"Verdade acima de tudo"**, **"Escrita humana"**, os
direitos de **"Foto de capa"** e **"A voz de Pedro Amaral"**. O que NÃO vale
aqui:

- a "regra de ouro" de nunca publicar. Neste fluxo a ordem é a oposta e é do
  próprio Pedro: o que passa no portão **é publicado no nome dele**;
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
- **Pedido fora de hora** ("escreve sobre X agora") segue o mesmo caminho e
  publica na hora.

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
- **uma por dia às 7h.** A fila continua de onde está: a primeira fria nova
  entra no primeiro dia livre depois da última já agendada
  (`python3 tools/mesa_pedro.py proximo-7h --n 5` lista os próximos cinco).
  O relatório diz a data de cada uma. O Pedro pode pedir outra ordem.
- Numa leva de N frias, **portes e formatos variados**: nunca cinco listas
  seguidas, nunca cinco perguntas com a mesma estrutura.

## 3. A régua do tamanho (ordem do Pedro: "n sair com o mesmo tamanho sempre")

O tamanho vem do assunto, e o assunto se declara no campo `porte`. O portão
cobra a faixa e os intertítulos. **Faixa, não meta**: resolvido em 220
palavras está pronto em 220.

| `porte` | Quando | Palavras | Intertítulos |
|---|---|---|---|
| `nota` | o aviso curto: data marcada, elenco confirmado, trailer, temporada estendida, prêmio anunciado, número isolado que fala por si | **160 a 300** | nenhum |
| `quente` | a notícia com consequência: bilheteria com leitura, cancelamento, polêmica com os dois lados, decisão de plataforma, estreia esperada | **350 a 600** | 0 a 2 |
| `contexto` | o fato que só se entende com o antes: disputa judicial, morte e legado, regra nova com efeito no bolso, fenômeno que pede números | **650 a 1.000** | 2 a 4 |
| `resposta` (fria) | a pergunta do público respondida de pé | **250 a 550** | 0 a 2 |
| `lista` (fria) | N itens, cada um com intertítulo próprio | **550 a 1.100** | um por item, de 5 a 12 |
| `explicador` (fria) | o tema que pede contexto: dinheiro, direito, história | **700 a 1.100** | 3 a 5 |

Regras que impedem a fôrma:

- **A divulgação de uma peça é `nota`.** Release de estreia com serviço não
  vira reportagem de 600 palavras; vira 220 palavras com o que importa e o
  serviço em duas linhas.
- **O que precisa de contexto é `contexto`.** Se a matéria só faz sentido
  para quem acompanhou os três capítulos anteriores, ela conta os capítulos,
  e isso é o tamanho dela.
- **Na dúvida entre dois portes, o menor.**
- **Três matérias seguidas do Pedro não podem ter o mesmo porte e a mesma
  conta de intertítulos.** O portão avisa quando a rodada sai com o mesmo
  esqueleto. Variar só o tamanho não quebra a fôrma: 400 palavras cortadas em
  5 seções continuam sendo a mesma fôrma, só menor.
- **`## Serviço` não conta** como intertítulo. Entra só quando a matéria é
  sobre algo com ingresso e data; vai no fim, em ficha curta.

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
quando há venda oficial. Aspas tipográficas (“ ”). Serviço em `## Serviço`,
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

Regras da capa: **16:9, até 1600 px de largura, rostos preservados** (foto em
pé é recortada pelo terço superior). O site não distorce imagem nunca.
**Trocar foto é arquivo novo com nome novo**, nunca sobrescrever (o navegador
guarda a imagem pelo nome).

**O descritivo (`imgLegenda`)** diz o que o leitor está vendo: quem, onde,
quando, em uma frase, sem repetir o título nem o crédito. É a legenda sob a
foto e o texto alternativo (leitor de tela e Google Imagens). Para arte da
casa: "Arte da identidade do FOYER: a cortina e a ribalta".

**O direito (`imgDireito`)** registra por que pode: "Divulgação oficial da
produção, baixada da sala de imprensa X em 14/10/2026", ou a licença com a
data da conferência, ou "arte própria do FOYER".

## 7. Publicar

```
python3 tools/mesa_pedro.py confere pacote.json            # o portão
python3 tools/mesa_pedro.py publica pacote.json --agora    # quente: no ar em ~3 min
python3 tools/mesa_pedro.py publica pacote.json --proximo-7h   # fria: entra na fila
python3 tools/mesa_pedro.py publica pacote.json --em 2026-10-20T10:00:00Z
```

O que o `publica` faz, nesta ordem, e por quê:

1. **Resolve a cópia de produção.** O site é montado a partir da branch
   `claude/foyer-digital-redesign-14l2b6` (é dela que `pages.yml` publica e é
   nela que a Coxia grava). A matéria tem de estar lá, ou não existe para o
   leitor. O script usa a pasta de trabalho atual se ela já estiver nessa
   branch; senão mantém uma cópia dela em `../FOYER-PRODUCAO` (worktree) e a
   atualiza com `fetch` + `rebase` antes de escrever. Nunca escreve na branch
   de desenvolvimento.
2. **Roda o portão** (seção 9). Reprovou, não publica. Sem exceção.
3. **Carimba** `publishAt`, `criadoEm`, `criadoPor`, `origem`.
4. **Commit e push** só do JSON e das imagens da matéria, com a mensagem
   `Mesa do Pedro: publica "título"` (ou `agenda "título" para 20/10 às 7h`).
   Push rejeitado: `fetch`, `rebase`, tenta de novo, quatro vezes com espera
   crescente. A Coxia pode ter gravado no meio; a cópia de produção nunca é
   sobrescrita à força.
5. **Devolve o endereço**: `https://www.foyer.digital/post-<slug>.html`. O
   `pages.yml` monta o site em 2 a 3 minutos. Fria agendada entra pelo
   relógio de `agendadas.yml`, que roda a cada 30 minutos: sai entre 7h00 e
   7h30.

**Reconferir o fato na hora de publicar.** Entre a apuração e o push podem
passar 40 minutos. Bilheteria muda, elenco desmente, plataforma recua. Antes
do `publica`, abrir de novo a fonte principal da matéria.

## 8. Correção, troca de foto e remoção

- **Corrigir** ("corrige a matéria X: o valor é Y"): editar o JSON na cópia
  de produção, acrescentar `atualizadoEm` e, quando o erro já foi lido, o
  campo `correcao: {"texto": "Correção: ...", "quando": ISO}` (o site imprime
  a nota no fim da matéria). Depois `publica pacote.json --corrige`, que
  aceita o slug existente e mantém o `publishAt` original.
- **Trocar a foto:** `capa` de novo (nome novo), apontar `img` para o novo,
  `publica --corrige`.
- **Remover** ("tira a matéria X do ar"):
  `python3 tools/mesa_pedro.py remove <slug> --motivo "..."`. A matéria vai
  para `import/lixeira/` com `removidoEm`, `removidoPor` e o motivo, como a
  Coxia faz; o site remonta sem ela.
- **Reagendar fria:** editar `publishAt` na cópia de produção e
  `publica --corrige`.

## 9. O portão (`confere`): o que reprova e o que avisa

Reprova (não publica): campo obrigatório faltando; `author` diferente de
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

A cada rodada (ou pedido de frias), o Pedro recebe aqui, para cada matéria:

1. **Título** e **linha fina**; editoria principal e secundárias; porte e
   contagem de palavras.
2. **Foto**: crédito, descritivo e origem.
3. **Endereço** no site e a hora em que entrou (ou a data da fila, para fria).
4. **O texto integral**, como foi publicado.
5. Uma linha de **"o que ficou de fora"**: a candidata descartada e o motivo
   (sem repercussão, fato não confirmado, já saiu, não é pauta dele).

Nada de descrever o processo: o Pedro lê a matéria, não o diário. Quando a
rodada sai vazia, o relatório diz as candidatas e por que nenhuma passou.

## 11. Pontas soltas: o que fazer quando

| Se | Então |
|---|---|
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
