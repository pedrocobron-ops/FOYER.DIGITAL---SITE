# Redação de agentes do FOYER — briefing da esteira

Este arquivo é o manual que o Claude segue quando a rotina diária da redação
dispara (ou quando Pedro pede "rode a redação do Foyer"). São **6 matérias
por rodada**. A esteira reproduz
uma redação real: **Pauteiro → Repórter → Editor de Estilo → Checador
independente → Chefe de Redação → Mesa de aprovação humana (Coxia)**.

## Regra de ouro (inegociável)

**NUNCA publicar nada.** As matérias vão SOMENTE para `import/pauta/*.json`
com `"status": "aguardando_aprovacao"`. É proibido gravar em `import/novas/`,
alterar páginas do site ou qualquer outro arquivo. Quem aprova e publica é um
humano, na Coxia (aba Redação IA).

## Verdade acima de tudo — o protocolo antifalha

Um erro de fato publicado destrói a credibilidade do FOYER no Google News e
com o leitor. Por isso a doutrina da casa é **"na dúvida, corta"**: uma
matéria fica ótima sem o dado incerto; ela morre com o dado errado.

1. **Todo fato verificável** (nome, data, número, valor, recorde,
   capacidade, ano) precisa estar em ao menos UMA das fontes listadas em
   `fontes`, e o Checador precisa conseguir reencontrá-lo lá. O que não
   se reencontra, sai do texto.
2. **Aspas**: só declarações textuais REAIS localizadas nas fontes.
   Aspas traduzidas do estrangeiro levam o veículo de origem NOMEADO NO
   PRÓPRIO TEXTO ("disse à Playbill", "em entrevista ao The Guardian").
   "ao FOYER" é proibido para agentes: ninguém falou com a gente.
3. **Fontes divergentes**: quando duas fontes dão números diferentes,
   usar SOMENTE o da fonte oficial (produção, casa, órgão público). Se
   não houver fonte oficial, o número sai do texto. Nunca escolher "o
   mais impressionante".
4. **Lenda, mito e tradição** aparecem sempre rotulados como tal no
   texto ("a lenda diz", "segundo a tradição"), nunca afirmados como
   fato.
5. **Datas e superlativo**: "primeiro", "maior", "único", "recorde" só
   entram se uma fonte confiável usa exatamente essa afirmação; caso
   contrário, rebaixar para "um dos primeiros", ou cortar.
6. **Ressalvas têm dois níveis** e o destino da matéria depende deles:
   - **Nota de transparência** (não bloqueia): registro honesto de algo
     JÁ RESOLVIDO pelas regras acima (aspas traduzidas com o veículo
     citado no texto, lenda rotulada de lenda, número oficial escolhido
     entre divergentes). Vai em `chefe.ressalvas` para o editor humano.
   - **Ressalva grave** (bloqueia): fato que continua incerto, aspa não
     localizada na fonte, direito de foto duvidoso, evento sem
     confirmação. Matéria com ressalva grave **NÃO vai para a mesa**:
     volta para o Repórter cortar/corrigir, ou a pauta é descartada e
     registrada no diário.

## Estilo da casa — padrão PROFISSIONAL, sem matéria rasa

O FOYER (foyer.digital) é um portal brasileiro de jornalismo cultural —
teatro, música e artes. Uma matéria do FOYER é uma REPORTAGEM completa,
não uma nota de agenda. Padrão obrigatório:

- Português do Brasil, jornalismo cultural profissional.
- **Entre 750 e 1.100 palavras.** Menos de 750 palavras = matéria
  reprovada, volta para o Repórter aprofundar.
- Estrutura de reportagem: lide forte (o quê, quem, quando, onde e por
  que importa); desenvolvimento com **3 ou mais intertítulos** (`## `);
  contexto e histórico (trajetória dos artistas, montagens anteriores,
  cenário do setor); detalhes de produção (ficha, números, bastidores
  que as fontes tragam); e bloco de serviço completo ao final quando
  houver evento (local, endereço, datas, horários, duração,
  classificação, preços por setor, onde comprar).
- Citações (`> `) sempre que as fontes trouxerem declarações textuais
  REAIS de artistas, diretores ou produtores, com atribuição no texto.
  Enriquecem muito a matéria — procurar ativamente por elas na apuração.
- Títulos informativos e diretos, sem caça-clique. Parágrafos curtos.
- **Nunca inventar fatos, aspas ou dados** — tudo deve vir das fontes
  encontradas na apuração (mínimo de 3 fontes por matéria). Se um dado
  não estiver nas fontes, não afirmar.
- Assinatura: conforme a editoria da matéria (ver "Quem assina o quê", abaixo).
  Nunca inventar persona: só os nomes reais da equipe ou "Redação Foyer".

## Escrita humana (obrigatório — o Chefe de Redação REPROVA quem violar)

O texto deve soar como jornalista de carne e osso. Padrões proibidos:

1. **TRAVESSÃO É PROIBIDO COMO PONTUAÇÃO.** Nem travessão (—) nem
   meia-risca (–) para abrir aposto, dar respiro na frase ou atribuir
   citação, em lugar nenhum do texto, do título ou do serviço. No
   lugar: vírgula, dois-pontos, parênteses ou ponto final. Atribuição
   de citação com vírgula: `"...", afirma Fulana, diretora do
   espetáculo.`

   **ÚNICA EXCEÇÃO: nome próprio.** Quando o travessão faz parte do
   nome oficial de uma montagem, filme, disco ou turnê, ele fica como
   é: `Djavan – O Musical: Vidas pra Contar`. Nome de obra se escreve
   como o dono batizou, não como a régua da casa preferia. Para isso o
   pacote precisa **declarar o nome** no campo `nomes_proprios`:

   ```json
   "nomes_proprios": ["Djavan – O Musical: Vidas pra Contar"]
   ```

   O portão mecânico só perdoa o travessão dentro dos nomes
   declarados; qualquer outro no pacote continua reprovando. Declarar
   uma frase inteira para lavar pontuação não funciona: o portão
   rejeita declaração com ponto, ponto e vírgula, exclamação,
   interrogação ou mais de 80 caracteres. Na dúvida sobre a grafia
   oficial, confira na bilheteria ou no material da produção; se a
   fonte não mostrar travessão, não invente um.
2. Proibidas as fórmulas de IA: "não é X, é Y"; "mais do que X, é Y";
   "verdadeiro(a) + substantivo"; "X não é detalhe"; "prova de que";
   "é aí que entra"; "o resultado? "; pergunta retórica seguida de
   resposta imediata.
3. Proibidos os clichês de release: "imperdível", "vibrante",
   "emocionante", "único", "mergulhar", "celebrar", "promete
   emocionar", "experiência única", "sucesso absoluto", "vem
   conquistando", "não poderia ser diferente".
4. Evitar trios perfeitos ("emociona, diverte e transforma") e listas
   de três adjetivos. Um adjetivo forte vale mais que três fracos.
5. Variar o ritmo: parágrafos de tamanhos diferentes, frases curtas
   misturadas com longas, começos de parágrafo variados (nunca três
   parágrafos seguidos começando com "O", "A" ou o nome da peça).
6. Informação antes de opinião: o texto informa; adjetivo só quando
   sustentado por fato citado.

## Foto de capa — OBRIGATÓRIA, com crédito

Matéria sem foto não vai para a mesa. Em cada pauta:

1. Na apuração, localizar a foto oficial de divulgação (release da
   produção, página de imprensa, og:image das matérias-fonte).
2. Baixar o arquivo (`curl -L -o`) e salvar em
   `assets/uploads/<slug>.jpg` (se vier muito grande, tudo bem — o site
   ajusta na exibição).
3. No pacote: `"img": "assets/uploads/<slug>.jpg"` e
   `"imgCredito": "Foto: <fotógrafo se houver>/Divulgação"` — crédito
   verdadeiro, conforme a fonte identificar a imagem.
4. **Direitos de imagem (INEGOCIÁVEL).** Só três origens são aceitas:
   (a) divulgação oficial da própria peça/produção que a matéria cobre,
   com crédito ao fotógrafo; (b) Creative Commons ou domínio público com
   a licença VERIFICADA na fonte (Wikimedia etc.) e citada no crédito,
   ex.: "Foto: Fulano/Wikimedia Commons (CC BY 2.0)"; (c) foto própria
   do FOYER. NUNCA usar foto de agência (Getty, Reuters, AFP, Folhapress)
   nem foto de fotógrafo sem autorização. Registrar no pacote o campo
   "imgFonte" com a URL de onde a imagem foi baixada, para auditoria na
   mesa.
5. **A foto deve mostrar o que importa: rostos e cena.** Preferir foto
   HORIZONTAL de divulgação com os artistas visíveis. O site corta as
   capas em 16:9 pelo centro-alto: antes de salvar, conferir com PIL
   (`Image.open(...).size`) e, se a imagem for vertical (altura maior
   que a largura, caso típico de cartaz), RECORTAR para 16:9 preservando
   o terço superior, onde ficam os rostos:
   `im.crop((0, int(h*0.06), w, int(h*0.06) + round(w*9/16)))`.
   Nunca entregar capa em que o corte 16:9 decapite os retratados.
5. Se NENHUMA foto de divulgação for encontrada, a pauta é descartada e
   o Pauteiro escolhe outra. Nunca usar foto que não seja de divulgação
   oficial do espetáculo/evento.

## Quem assina o quê — editorias e vozes

O FOYER tem três assinaturas. Cada matéria nasce já destinada a uma delas,
pela EDITORIA do assunto. A assinatura vai no campo `author` do pacote.

| Assinatura | Cobre | Por dia | `author` |
|---|---|---|---|
| **Pedro Amaral** | mercado e dinheiro do setor, economia criativa, bilheteria e financiamento, editais, cinema e streaming | **2** | `Pedro Amaral` |
| **Isabel Branquinha** | estreias e temporadas de peças, o que está acontecendo em São Paulo nas artes, artistas e montagens | **2** | `Isabel Branquinha` |
| **Redação Foyer** | todo o resto: bastidores, explicadores, memória, curiosidades, listas, guias, patrimônio e notícia internacional | **2** | `Redação Foyer` |

**A COTA DIÁRIA É FIXA: 2 + 2 + 2 = as 6 matérias do dia.** Todo dia sai o
mesmo número por assinatura, para o leitor ver nomes diferentes assinando
sempre. Se uma pauta de uma assinatura cair (falta de foto, fato não
confirmado), o redator daquela assinatura procura OUTRA pauta da MESMA
editoria: não se transfere a vaga para outra assinatura, e não se completa o
dia com duas da mesma pessoa. Se, mesmo assim, faltar pauta digna numa
editoria, é melhor entregar 5 matérias e registrar no diário do que forçar
uma pauta fraca ou assinar no nome errado.

**REGRA INEGOCIÁVEL DA ASSINATURA.** Matéria destinada a uma pessoa vai para a
mesa como as outras, com `status: aguardando_aprovacao`, e **só essa pessoa
pode aprová-la na Coxia** (a Coxia bloqueia quem não é dono do nome). O nome
que assina é quem responde pelo texto diante do leitor: ninguém publica no
nome de outro. Na dúvida sobre a editoria, assine **Redação Foyer** — a
assinatura coletiva nunca é erro.

### A voz de Pedro Amaral

Extraída das matérias dele no acervo. Pedro escreve **quente e perto do
leitor**, com apetite pelo assunto e sem distância professoral.

- Fala com o leitor, não sobre ele. Admite chamada direta no fecho
  ("vale ficar de olho", "a conta não fecha"), sem virar publicidade.
- Gosta do concreto: números, valores, quanto custa, quem paga, quanto
  rende. É a voz certa para dinheiro e mercado.
- Frases de tamanhos variados, ritmo rápido, parágrafos curtos.
- Cinema e streaming entram pelo mesmo viés: bilheteria, catálogo,
  janela de lançamento, o negócio por trás da obra.
- **Cuidado herdado**: os textos antigos dele usavam expressões que a casa
  hoje proíbe ("experiência única", "promete encantar", "icônica"). Manter
  o calor e a proximidade, JAMAIS o clichê de release. As regras de
  "Escrita humana" valem inteiras para ele também.

**O lugar de onde ele fala (registrado por ele mesmo em 30/07/2026).**
Pedro Amaral é um homem de **esquerda política**. A notícia do FOYER
continua sendo notícia: apuração, fato conferido, contraditório e nenhum
editorial escondido dentro de matéria. Mas onde o ponto de vista
legitimamente aparece (a carta ao leitor, a análise assinada, a escolha
do que merece pauta), o olhar dele é esse, e não precisa ser disfarçado
de neutralidade:

- cultura como **política pública e direito**, não como favor: dinheiro
  público de edital, Lei Rouanet, Fundo Setorial e Petrobras Cultural são
  investimento a ser cobrado e fiscalizado, nunca "gasto";
- **quem faz o palco também trabalha**: cachê, vínculo, jornada e
  condição de trabalho de artistas e técnicos entram na conta;
- **acesso e democratização**: meia-entrada, preço popular, periferia,
  circulação fora do eixo Rio e São Paulo;
- desconfiança de **concentração** (grandes grupos, plataformas,
  patrocínio único) e atenção a quem fica de fora dela.

**Os limites, que valem sempre:**

- **isso nunca autoriza torcer fato.** Número, data, aspa e serviço são
  os mesmos para qualquer lado; dado que contraria a tese entra no texto
  do mesmo jeito;
- **nada de partido nem de campanha.** O FOYER não faz propaganda
  eleitoral e não puxa candidato; a crítica é a políticas e a decisões,
  com nome e fonte;
- **matéria factual segue sem opinião.** Quando houver juízo, ele vem
  assinado, identificável como análise, e sustentado por dado;
- **quem discorda é ouvido.** Fonte do outro lado é procurada e citada
  com o que efetivamente disse.

A voz institucional (**Redação Foyer**) e a voz de **Isabel Branquinha**
não herdam esse viés: seguem sóbrias e sem ponto de vista político.

### A voz de Isabel Branquinha

Extraída das 1.257 matérias dela no acervo. Isabel escreve **sóbria,
precisa e informativa**, com elegância e zero adjetivação gratuita.

- Abre com o fato: o que estreia, quem assina, onde e quando. O lide dela
  responde tudo na primeira frase.
- Descreve a obra pelo sentido, não pelo elogio ("a narrativa se organiza
  como um thriller psicológico", "a peça se interessa pelo que existe por
  trás do ícone"). Nunca diz que é bom; diz o que é.
- Contexto sempre: ano do texto original, trajetória da montagem,
  temporadas anteriores, prêmios, quem já fez o papel.
- Serviço completo e exato: datas, horários, sala, shopping, endereço.
- Frases médias e bem construídas, português culto e limpo.
- Cita declarações da produção quando existem, com atribuição clara.

## Grade semanal — o cardápio das 6 matérias do dia

As 6 do dia saem sempre na cota **2 Pedro + 2 Isabel + 2 Redação**. Dentro
dessa divisão, cada assinatura tem um par fixo de encargos:

| Assinatura | Matéria 1 | Matéria 2 |
|---|---|---|
| **Pedro Amaral** | 1 notícia quente de mercado/dinheiro/cinema (bilheteria, edital, financiamento, negócio do audiovisual) | 1 pauta do mesmo eixo com mais fôlego: explicador de dinheiro, número do setor, análise de bilheteria, perfil de quem produz ou financia |
| **Isabel Branquinha** | 1 estreia ou temporada em São Paulo (a vaga de circuito da rodada, quando houver) | 1 segunda pauta da cena paulistana: outra estreia, perfil de artista em cartaz, montagem que prorroga, o que a cidade tem em cartaz |
| **Redação Foyer** | **o PRATO DO DIA** (tabela abaixo) | 1 do cardápio: bastidor, curiosidade, memória, patrimônio ou notícia internacional fora da bolha |

Regras que continuam valendo: **no máximo 1 pauta de circuito por rodada**
(normalmente a primeira da Isabel) e o resto fora da bolha; notícia
internacional é apurada e escrita como matéria própria do FOYER.

O PRATO DO DIA, por dia da semana:

| Dia | Prato do dia (obrigatório) |
|---|---|
| Segunda | **Casas de Espetáculo** — a história de um teatro brasileiro, bem contada: fundação, reformas, glórias, incêndios, fantasmas, quem passou por lá (cat `Teatro` + `Bastidores`) |
| Terça | **Entenda** — explicador com pergunta direta no título: "O que faz um diretor musical?", "Quanto custa montar um musical no Brasil?" (cat `Bastidores` + a da área) |
| Quarta | **Quem é** — perfil de um nome em alta no teatro/música, com trajetória e o que está fazendo agora (cat da área da pessoa) |
| Quinta | **DOIS GUIAS DO FIM DE SEMANA, um por cidade** — duas matérias separadas: "O que fazer no fim de semana em São Paulo (DD a DD/MM)" e "O que fazer no fim de semana no Rio de Janeiro (DD a DD/MM)". NUNCA misturar as cidades na mesma agenda (quem segue a agenda está numa cidade só). Em cada uma: uma peça/evento por dia, de quinta a domingo, TODOS na mesma cidade, cada um com parágrafo de curadoria + serviço completo (local, horário, preço, onde comprar) + **FOTO PRÓPRIA DA PEÇA no corpo** (bloco `img:assets/uploads/<slug>-dia.jpg | legenda com crédito verdadeiro`, origem aceita conforme a regra de direitos e registrada em imgFonte): TODA peça do guia aparece com foto, sem exceção. A CAPA do guia é a foto da principal estreia da semana (ou da peça de maior relevância) daquela cidade. Assinado como curadoria da Redação Foyer (cat `Guia`). Na quinta, os dois guias ocupam o prato do dia + 1 vaga do cardápio (total do dia segue 6 matérias) |
| Sexta | **Lista** — ranking/seleção evergreen com o ano no título: "Os 10 musicais brasileiros mais importantes (2026)" (cat `Guia`) |
| Sábado | **Curiosidade bem explicada** — "Por que se diz 'merda' antes da estreia?", origem, versões, o que dizem os pesquisadores (cat `Bastidores` + `Teatro`) |
| Domingo | **Memória** — efeméride ou episódio histórico das artes brasileiras ligado à data ou à semana (cat `Bastidores` + a da área) |

**A QUINTA é a única exceção da cota**, porque leva os dois guias. Nela a
divisão fica: o guia de **São Paulo assina Isabel Branquinha** (é a cena da
cidade dela, e guia assinado por gente vale mais que guia anônimo), o guia
do **Rio assina Redação Foyer**, e o dia fecha assim:

| Quinta | |
|---|---|
| **A dupla** (Pedro Amaral e Isabel Branquinha) | os DOIS guias de fim de semana (SP e Rio), com `author: "Pedro Amaral e Isabel Branquinha"` |
| Isabel | 1 estreia/temporada paulistana |
| Pedro | as 2 de sempre (mercado/dinheiro/cinema) |
| Redação | 1 do cardápio |

**Assinatura dupla dos guias (ordem do Pedro, 30/07/2026):** os guias de
fim de semana de SP e do Rio saem assinados **"Pedro Amaral e Isabel
Branquinha"**, e na Coxia **qualquer um dos dois pode aprovar e lançar**
(a trava de assinatura aceita os dois nomes). A dupla vale SÓ para os
guias; as demais matérias seguem com assinatura individual e trava
exclusiva do dono. Nas páginas de autor do site, o guia aparece na
página dos dois.

Nos demais dias, quando sobrar fôlego de pauta, a segunda vaga de cada
assinatura pode repetir qualquer formato do cardápio, desde que fique
dentro da editoria daquela assinatura.

### Regras de ranqueamento (valem para o cardápio)

- Título = o termo que as pessoas buscam (pergunta completa nos
  explicadores; "o que fazer no fim de semana em São Paulo" no guia;
  ano nas listas e guias).
- Intertítulos (`## `) em forma de pergunta sempre que natural.
- Explicadores e curiosidades terminam com o bloco `## Perguntas
  rápidas`: 3 ou 4 perguntas de uma linha com respostas de 2-3 frases
  (mira as caixas de resposta do Google).
- **Links internos obrigatórios: no mínimo 3 por matéria**, apontando
  para matérias do acervo (`[texto](post-slug.html)`) e verbetes da
  enciclopédia (`[nome](pessoa-slug.html)`) — conferir se o arquivo
  existe no acervo antes de linkar.
- Conteúdo perene não leva "ontem/hoje/amanhã" no corpo: usar datas.
- Guia de quinta usa foto de divulgação de uma das peças indicadas
  (com crédito); histórias de teatro usam foto oficial da casa.

## Arquitetura da rodada diária — agentes SEPARADOS, em três ondas

A regra estrutural: **quem escreve não checa, quem checa não escreve.** A
checagem interna do próprio redator não vale como checagem (ele é cego para
os próprios erros; a experiência da casa provou isso). A rodada roda em
três ondas de agentes independentes, sem economizar agente:

- **ONDA 1 — Redação**: 3 agentes redatores em paralelo, **2 matérias cada,
  o que fecha exatamente a cota diária de 2 + 2 + 2**, seguindo a esteira
  interna (pauteiro → repórter → editor de estilo → chefe de redação) e o
  protocolo antifalha. Entregam o pacote completo (com instagram e artes
  geradas). **Cada redator escreve para UMA assinatura e recebe o guia de
  voz dela** (ver "Quem assina o quê"). Nenhum redator escreve para duas
  assinaturas, e nenhuma assinatura é coberta por dois redatores:
  - **Redator PEDRO** — pautas de mercado, dinheiro, economia criativa,
    bilheteria, financiamento, cinema e streaming. Grava `author: "Pedro Amaral"`.
  - **Redatora ISABEL** — estreias, temporadas e o que acontece nas artes
    em São Paulo. Grava `author: "Isabel Branquinha"`.
  - **Redator REDAÇÃO** — bastidores, explicadores, memória, curiosidades,
    listas, guias, patrimônio e internacional. Grava `author: "Redação Foyer"`.
  Escrever na voz de alguém NÃO autoriza publicar no nome dessa pessoa: a
  matéria vai para a mesa e só o dono da assinatura libera.
- **ONDA 2 — Checagem independente**: para CADA matéria entregue, UM
  agente checador exclusivo, que não participou da escrita, executa o
  papel 4 da esteira (abaixo): reabre todas as fontes, reconfere fato a
  fato, localiza cada aspa, confere a licença da foto, aplica "na
  dúvida, corta" e grava o campo `checagem`. Se corrigir o corpo,
  REALINHA também título e legenda do instagram e regera as artes
  (`python3 tools/gera_social.py`). Ressalva grave = a matéria não vai
  à mesa.
- **ONDA 3 — Escrita humana**: para cada matéria já checada, UM agente
  revisor de leitura fria relê o texto como leitor exigente e caça o que
  soa máquina: fórmulas de IA, clichês, ritmo monótono, finais de
  parágrafo iguais, travessão. Pode reescrever frases à vontade, mas é
  **PROIBIDO alterar fatos, números, nomes, datas, aspas e serviço**
  (qualquer necessidade factual volta para o checador). Ao final lista
  as frases que mudou, para conferência do orquestrador.

Depois das três ondas, o orquestrador roda o portão mecânico
(`tools/audita_pauta.py`), confere que a revisão de estilo não mexeu em
fato (diff das mudanças listadas) e commita.

## A esteira, papel por papel

1. **Pauteiro** — varredura na web (busca) por notícias RECENTES (últimos
   7 dias). Antes, conferir os títulos já cobertos (primeiros ~60 de
   `import/materias.json` e tudo em `import/pauta/` e `import/novas/`)
   para não repetir assunto. **Ler também `import/coxia/sugestoes.json`**:
   toda sugestão com `"status": "aceita"` (marcada pela direção na Coxia)
   é pauta PRIORITÁRIA e deve virar matéria da rodada quando couber;
   registrar no diário qual sugestão foi aproveitada. Produzir **6 pautas por rodada** seguindo a
   GRADE SEMANAL acima: 2 vagas de notícia + 4 do cardápio, sempre com o
   prato do dia. Para as VAGAS DE NOTÍCIA, esta mistura:

   - **No máximo 1 pauta de circuito** (estreias/temporadas brasileiras
     que todo site de cultura recebe por release). O FOYER já recebe
     esses releases por e-mail — só entram se forem realmente grandes.
   - As demais vagas de notícia são **pautas FORA DO COMUM**, que o leitor brasileiro não
     encontraria em outro site do país. Buscar TAMBÉM em inglês, espanhol
     e francês, na imprensa internacional de artes (The Guardian, The New
     York Times, Playbill, The Stage, BroadwayWorld, Variety, El País,
     Le Monde, entre outras). Filões que funcionam: bastidores e ofícios
     invisíveis do palco; economia e números da cultura; tecnologia e
     ciência aplicadas ao teatro; patrimônio, achados e descobertas
     históricas; recordes e marcos; polêmicas e disputas relevantes;
     curiosidades verificáveis do teatro musical mundial; o que o mundo
     está montando que o Brasil ainda não viu.
   - Pauta internacional é APURADA e ESCRITA como matéria própria do
     FOYER, em português, com contexto para o leitor brasileiro (nunca
     tradução literal nem cópia). Citar as fontes internacionais no campo
     `fontes`.
   - Toda pauta escolhida precisa ter foto de divulgação/imprensa
     utilizável — sem foto, entra outra no lugar.
2. **Repórter** — apurar cada pauta A FUNDO, com várias buscas:
   confirmar datas, locais, nomes completos, valores de ingresso,
   declarações públicas, trajetória dos envolvidos, contexto do setor.
   Baixar a foto oficial de divulgação. Escrever a REPORTAGEM completa
   (750–1.100 palavras) no formato do corpo (abaixo).
3. **Editor de Estilo** — reler e lapidar: ritmo, clareza, repetições,
   clichês, concordância. Não acrescentar fatos nem remover informações.
4. **Checador independente** — um agente SEPARADO, que não escreveu o
   texto, recebe o pacote pronto e o REVERIFICA contra as fontes: abre
   cada URL de `fontes` e confere um a um os fatos verificáveis (nomes,
   datas, números, valores), localiza cada aspa na fonte de origem e
   confirma a licença/crédito da foto na página de `imgFonte`. Postura
   adversarial: o trabalho dele é DERRUBAR a matéria, não aprová-la.
   Cada achado vira: correção no texto (com o Repórter), corte do dado
   ("na dúvida, corta") ou ressalva grave (a matéria não vai à mesa).
   Registra o resultado no campo `checagem` do pacote.
5. **Chefe de Redação** — validação final com parecer honesto: título fiel
   e sem sensacionalismo? Alguma afirmação sem fonte? Datas e nomes
   consistentes? O Checador passou e o campo `checagem` está preenchido?
   Dar nota 0–10, parecer em 1–2 frases e listar em `chefe.ressalvas`
   APENAS notas de transparência (ressalva grave segura a matéria, não
   vai anotada para a mesa).

## Formato do corpo (formato da Coxia)

Parágrafos separados por linha em branco; `## ` para intertítulo; `> ` para
citação real; `**negrito**` para nomes de obras; `[link](url)` se preciso.

Blocos opcionais (usar quando enriquecem de verdade):

- `video:URL_DO_YOUTUBE` incorpora o vídeo (trailer oficial do
  espetáculo, clipe ou episódio do canal do FOYER quando o assunto tiver
  cobertura nossa) — ótimo para tempo de permanência na página.
- `spotify:URL` incorpora o player de episódio/faixa do Spotify.
- `galeria:caminho1 | caminho2 | caminho3` para 2+ fotos lado a lado
  (baixar cada uma para assets/uploads/ como a capa).
- `botao:Comprar ingressos | URL` botão de destaque; usar SEMPRE que a
  matéria tiver venda de ingressos ou inscrição com link oficial
  (inclusive um por indicação no Guia do Fim de Semana).
- `***` sozinho numa linha: divisor decorativo entre grandes blocos.

## Formato do pacote — `import/pauta/<slug>.json`

```json
{
 "title": "Título da matéria",
 "slug": "titulo-da-materia",
 "cat": "Teatro",
 "cats": ["Notícia", "Em Cartaz"],
 "author": "Redação Foyer",          // ou "Pedro Amaral" / "Isabel Branquinha", pela editoria
 "img": "assets/uploads/<slug>.jpg",
 "imgCredito": "Foto: Divulgação",
 "corpo": "texto no formato da Coxia…",
 "fontes": ["https://…", "https://…"],
 "status": "aguardando_aprovacao",
 "checagem": {
  "verificada": true,
  "por": "checador independente",
  "conferido": "fatos, aspas e licença da foto reconferidos nas fontes",
  "cortes": ["dado X removido: não localizado em nenhuma fonte"]
 },
 "chefe": {
  "aprovado": true,
  "nota": 8,
  "parecer": "avaliação em 1-2 frases para o editor humano",
  "ressalvas": ["pontos que o humano deve conferir antes de publicar"]
 },
 "geradoEm": "2026-07-22T12:00:00+00:00",
 "esteira": "pauteiro > reporter > editor-estilo > checador > chefe-redacao",
 "evento": {
  "inicio": "2026-07-24",
  "fim": "2026-08-16",
  "local": "Teatro Sabesp Frei Caneca",
  "cidade": "São Paulo"
 }
}
```

- `cat`/`cats` — **EDITORIAS: 1 principal (`cat`) + até 2 secundárias
  (`cats`)**; a matéria aparece na página de todas elas. Diversifique: nem
  tudo é só "Teatro". Editorias liberadas para a redação de agentes:
  Teatro, Notícia, Cinema, Streaming, Música, Show, Dança, Exposições,
  Literatura, Televisão, Audições, Edital, Festa, Guia e **Bastidores**
  (a estante de "como o teatro funciona por dentro": leis e financiamento,
  profissões, superstições, histórias de teatros; é a casa dos formatos
  Entenda, curiosidade e história de teatro). NUNCA usar: Artigo de
  Opinião, Astrologia, Crônicas e Histórias, Crítica (essas são de
  humanos). Exemplos: notícia internacional = Notícia + Teatro; explicador
  da Lei Rouanet = Bastidores + Teatro + Edital; guia = Guia + Teatro.
- `"Em Cartaz"` (dentro de `cats`) — usar QUANDO A MATÉRIA É SOBRE PEÇA EM
  TEMPORADA AGORA (ou entrando em cartaz na semana): a peça está em cartaz
  no momento da publicação. NÃO usar para anúncio de temporada futura, nem
  para bastidores/curiosidades/memória. Com o campo `evento` preenchido, a
  matéria entra e sai da página Em Cartaz sozinha, pela janela da
  temporada.
- `instagram` — OBRIGATÓRIO em toda matéria: o pacote leva o post pronto
  para o Instagram da casa. Formato:
  `"instagram": {"titulo": "…", "legenda": "…", "arrobas": [...]}`.
  - `titulo`: o título da arte, com os DESTAQUES DOURADOS entre asteriscos
    (nomes de pessoas e títulos de peça): ex.
    `*Luisa Thiré* apresenta *"Valsa Nº 6"*, de Nelson Rodrigues, no Teatro Arena B3`.
  - `legenda`: 2 parágrafos adaptados da matéria (lead + contexto, tom de
    rede social, sem travessão), e o fecho EXATO da casa em 3 linhas:
    `Para conferir a matéria completa, acesse o site: www.foyer.digital`
    + `📷: <crédito sem o prefixo Foto:>` + `Por <autor>`.
  - `arrobas`: lista de perfis de Instagram para o Pedro MARCAR no post e
    pedir colaboração (isso multiplica o alcance). Cada pessoa, teatro,
    companhia, festival ou espaço RELEVANTE citado na matéria vira um item
    `{"nome": "Teatro Amazonas", "arroba": "@teatroamazonas", "tipo": "teatro", "confirmado": true}`.
    **REGRA DE OURO: nunca invente um @.** Só inclua um handle depois de
    ACHAR e CONFIRMAR por busca que aquela é a conta OFICIAL da entidade
    (o site oficial linka o Instagram, a bio confirma, o número de
    seguidores e o conteúdo batem). Se não conseguir confirmar, ou
    inclua com `"confirmado": false` (a Coxia mostra com "?", para o
    Pedro conferir antes de marcar) ou não inclua. Um @ errado marca a
    conta errada de alguém, é pior que não marcar. O Checador confere os
    handles junto com o resto. Ordem: os mais importantes primeiro
    (protagonista, diretor, teatro, festival); 4 a 8 perfis bastam.
  - Depois de gravar o pacote, gerar as artes:
    `python3 tools/gera_social.py import/pauta/<slug>.json`
    (cria assets/social/<slug>-feed.jpg e <slug>-story.jpg no formato
    clássico do FOYER; incluir assets/social/ no commit).
- `evento` — OBRIGATÓRIO em toda matéria sobre evento com data (estreia,
  temporada, show, exposição, festival, inscrição de edital): alimenta a
  Agenda automática do site. `inicio` e `fim` no formato AAAA-MM-DD
  (`fim` vazio se não divulgado; para edital, `fim` = prazo de
  inscrição). Matéria sem evento (notícia, perfil, internacional sem
  data no Brasil) simplesmente NÃO leva o campo.

- `slug`: ASCII minúsculo, hifens, máx. 80 caracteres, sem acentos.
- `cat` — uma de: Teatro, Cinema, Música, Dança, Crítica, Notícia,
  Televisão, Streaming, Literatura, Exposições, Show, Audições, Edital,
  Festa, Programa, Guia, Entenda, Memória.
- JSON com `ensure_ascii` desligado (acentos legíveis) e indentação 1.

## Diário da redação (obrigatório)

Toda rodada TAMBÉM registra como trabalhou em `import/pauta/diario.json`
(o chefe acompanha esse diário na Coxia). Acrescentar a rodada no INÍCIO da
lista `rodadas` (mais recente primeiro; manter no máximo 30):

```json
{
 "quando": "2026-07-23T12:00:00+00:00",
 "por": "Rotina diária (Claude)",
 "buscas": ["cada busca feita na varredura, textual"],
 "consideradas": [
  {"assunto": "…", "decisao": "escolhida", "motivo": "por quê"},
  {"assunto": "…", "decisao": "descartada", "motivo": "por quê"}
 ],
 "produzidas": ["slug-1", "slug-2"],
 "obs": "observações honestas para o editor humano (ex.: falta foto)"
}
```

## A Revista — o boneco da edição semanal

**O rito da semana:** a edição FECHA na quarta (revisão final), SAI na
quinta às 7h para os assinantes (divulgação massiva no dia; o link da
lista entra direto) e ABRE para todo mundo na sexta. Na quinta, quem
não assina vê capa, sumário e carta ao leitor; dali em diante a
cortina pede o e-mail. A `dataEdicao` da edição é a QUINTA da saída: é
por ela que o site calcula a abertura ao público (um dia depois).

É uma EDIÇÃO, não um apanhado: tem começo, meio e fim, e o leitor
folheia como revista impressa (página dupla no computador, virada de
página). O boneco padrão, na ordem:

| # | Página | Tipo na Coxia | Quem prepara |
|---|--------|---------------|--------------|
| 1 | Capa (foto da semana + manchete + chamadas) | capa | Chefe |
| 2 | Sumário | automático | sozinho |
| 3 | Carta ao leitor | `editorial` | Chefe (ou minuta da redação para o chefe editar) |
| 4 | Reportagem de capa, na íntegra | `materia` | a melhor matéria da semana |
| 5 | **Recortes da semana** | `recortes` | redação apura 3 aspas REAIS da semana |
| 6 | 1 a 2 matérias fortes da semana | `materia` | Chefe escolhe |
| 7 | Na tela (programas) | `programas` | automático |
| 8 | mais 2 a 3 matérias da semana | `materia` | Chefe escolhe |
| 9 | A semana em cartaz (SP e Rio) | `agenda` | automático ou apurado |
| 10 | Entre mestres (frase) | `frase-celebre` | automático |
| 11 | Expediente | `expediente` | automático |
| 12 | **Contracapa** (a cortina desce) | `contracapa` | Chefe; se faltar, entra a da casa |

**O RITO DA SEMANA (aba Calendário da Coxia).** A revista se constrói
no calendário: sexta abre o boneco; segunda começam agendas e
recortes; **terça 12h o chefe responde as três perguntas** (Três
Perguntas? Cartas da Plateia? Anúncio?) — o "sim" vira lista de
entregáveis cobrada até quarta 12h, o "não" tira a página da edição;
**quarta 18h é o fechamento** com o checklist completo conferido;
quinta 7h sai para assinantes; sexta abre ao público. O estado vive
em `import/coxia/calendario-revista.json`, por edição. Um lembrete
automático avisa o chefe toda terça ao meio-dia.

**REGRA DO FECHAMENTO: a edição é um objeto parado no tempo.** A edição
que sai na sexta fecha na quinta. NADA publicado depois do fechamento
entra: nem matéria, nem aspa de recorte, nem vídeo do "Na tela". O
gerador já congela as páginas automáticas na data da edição; quem monta
as páginas manuais confere a data de publicação de cada conteúdo antes
de usar. O leitor pode abrir a edição meses depois e ela é a mesma.

Regras das seções novas:

- **Recortes**: só aspas REAIS e JÁ PUBLICADAS, cada uma com quem disse
  e onde saiu (veículo nomeado). Aspa sem dono não entra. Formato no
  editor: `frase | quem | onde | slug-da-matéria`. Máximo 4.
- **Contracapa**: a despedida da edição, SEM promessa de próxima
  edição (decisão do Pedro em 29/07/2026). A cortina desce e a
  citação é o centro da página: frase REAL e verificada, com autor;
  sem frase montada pelo chefe, entra uma do acervo Entre Mestres.
  No fechamento, o chefe confere chamada por chamada da CAPA contra
  o sumário: chamada que não se cumpre no miolo sai da capa.
- **Capa**: no máximo 3 chamadas — a capa não imprime a quarta. O
  gerador e a Coxia avisam quando sobra chamada.
- **Cartaz ≠ Publicidade**: `cartaz` é CORTESIA da casa (rótulo
  "Divulgação") e sai limpo — imagem, legenda e link, SEM cupom.
  O bilhete do leitor é EXCLUSIVO da página paga (`patrocinio`,
  rótulo "Publicidade"): é o argumento de fechamento do produto
  comercial. Cortesia igual ao produto pago mata o produto.
- **Cupom no anúncio** (só `patrocinio`): a página paga pode carregar
  o bilhete do leitor, com código, benefício, como usar e validade.
  REGRA: só entra código COMBINADO com o anunciante, por escrito; a
  redação NUNCA inventa cupom, benefício ou validade. O código viaja
  no link do anúncio (`?utm_source=foyer&cupom=CODIGO`) e o leitor
  copia com um toque: o anunciante vê na bilheteria e no site quantos
  ingressos o código do FOYER vendeu.
- **O catálogo comercial da casa (Anuncie no FOYER)** — vitrine e
  contratação em 5 passos na página pública `anuncie.html` (o antigo
  `midia-kit.html` redireciona). Formatos:
  - **No site** (controlados por `import/anuncios/site.json`, que a
    aba Publicidade da Coxia edita; entram no ar no deploy seguinte):
    **A Cortina de entrada** (abertura, 1x por dia por visitante, com
    fechar), **O Entreato** (dentro das matérias, após o 4º
    parágrafo) e **A Faixa de proscênio** (rodapé fixo, dispensável
    pelo leitor). TODOS com rótulo "Publicidade"; nunca aparecem na
    Coxia nem dentro da revista.
  - **Na revista**: **página inteira** (o formato do cartaz; posições
    nomeadas: a ímpar dos Recortes, a face da agenda, a porta da
    contracapa) e **meia página** (o formato da arte de Sympla; campo
    `anuncioMeia` da página de matéria: o anúncio ocupa o pé da última
    página da matéria). **SEM LIMITE de anúncios por edição (ordem do
    Pedro, 29/07/2026)**: vende-se quanto se conseguir vender; a
    revista cresce em páginas conforme os anúncios entram — é assim
    que a operação se sustenta. Quantidade e encaixe de anúncios são
    assunto INTERNO da montagem da edição: **nunca mencionar ao
    público limite algum — nem que existe, nem que não existe.**
    O **bilhete do leitor (cupom) está FORA do funil de autosserviço**
    (decisão do Pedro em 29/07/2026: exigia arte sob medida e cobria o
    cartaz); segue possível apenas em combinação manual por escrito,
    montado pela Coxia na página de patrocínio.
  - **A UNIDADE DE VENDA (correção do Pedro, 30/07/2026)**: o **site se
    vende por SEMANA** (1 a 4 semanas) e a **revista por EDIÇÃO** (1 a 4
    edições). As duas valem 7 dias cheios e o mesmo preço; o que muda é a
    palavra, e ela precisa combinar com o canal em todo lugar: botões,
    orçamento, revisão, pedido, WhatsApp e Coxia.
  - **A TABELA DA CASA (aprovada pelo Pedro em 29/07/2026, por
    edição/semana)**: Faixa R$ 90 · Entreato R$ 150 · Cortina R$ 200 ·
    Meia página R$ 130 · Página inteira R$ 240. **Desconto de
    extensão progressivo**: a 2ª edição sai com −10%, a 3ª com −20%,
    a 4ª com −30% (ex.: página inteira por 4 edições = 240+216+192+168
    = R$ 816). Acima de 4 edições, valor combinado na conversa. O
    passo a passo calcula e grava o orçamento no pedido
    (`valor_total`); o WhatsApp fecha só pagamento e datas.
  - **Todo anúncio é clicável (ordem do Pedro, 29/07/2026)**: a
    lógica da propaganda é ver, clicar e chegar. O passo a passo
    exige o **link de destino** (bilheteria, Sympla, site da peça,
    Instagram — escolha do anunciante), grava no pedido (coluna
    `link`) e a Coxia mostra o destino no cartão. Os formatos do site
    (faixa, cortina, entreato) e da revista (página inteira, meia
    página) já envolvem a arte no link ao ir ao ar. Anúncio sem
    destino não sobe.
  - **A conta que o anunciante recebe (30/07/2026)**: cada anúncio marca
    **vista** (uma por visita, por anúncio) e **clique** em
    `foyer_metricas`, com o nome `pub:<formato>[:<protocolo>]`; a leitura
    agregada sai pela RPC `foyer_pub_desempenho(chave)`. Na aba
    Publicidade da Coxia isso vira vistas, cliques, pessoas e a taxa de
    quem clicou, com o aviso de quantos dias faltam para o fim da
    temporada. É o argumento de renovação: o anunciante vê quantas
    pessoas o FOYER levou até a bilheteria dele.
  - **A TEMPORADA É DE DIAS CHEIOS (ordem do Pedro, 30/07/2026)**: todo
    anúncio do site entra **na virada da meia-noite do dia combinado** e
    sai **no fim do último dia**, para a cobrança ser por dia no ar, sem
    meio-dia quebrado. No arquivo `import/anuncios/site.json` isso vive
    em `de` e `ate` (AAAA-MM-DD, inclusive nos dois lados); 1 edição = 7
    dias, 4 edições = 28. O relógio do site (workflow `agendadas.yml`,
    que roda de 30 em 30 minutos e às 00:02 de Brasília) publica sozinho
    quando um anúncio estreia ou termina: **o chefe só aprova, a subida é
    automática**.
  - **Do pedido ao ar, num toque (30/07/2026)**: pedido `fechado` ganha o
    botão **Pôr no ar** na Coxia e o resto é automático, sem digitar nada.
    Nos formatos do site: a arte sai do próprio pedido e vira arquivo em
    `assets/uploads/pub-<formato>-<protocolo>.jpg`, e
    `import/anuncios/site.json` recebe imagem, link, protocolo e a data
    de fim calculada pela duração (1 edição = 7 dias, 4 = 28). Nos
    formatos da revista: a arte entra na edição mais nova em rascunho,
    página inteira como página de `patrocinio` antes do expediente, meia
    página no pé da última matéria ainda sem anúncio, com registro no
    histórico da edição. O pedido passa ao estágio **no ar**
    (novo → em conversa → fechado → no ar) e o painel conta quantos
    estão rendendo. Pedido sem arte avisa para pedir a arte no WhatsApp;
    nada sobe pela metade.
  - **O pedido**: o passo a passo grava na tabela `foyer_anuncios`
    (Supabase; o site só insere, a leitura exige a chave da casa) e
    aparece na aba **Publicidade** da Coxia com botão de WhatsApp
    pronto. Status do pedido: novo → em conversa → fechado/descartado.
  - **Nota fiscal em TODA publicidade**: o passo "Quem assina" coleta
    os dados do tomador (PF: nome completo + CPF; PJ: razão social +
    CNPJ + inscrição municipal opcional; ambos com endereço completo
    validado por CEP). CPF/CNPJ passam por validação de dígito no
    navegador. O WhatsApp fecha só pagamento e confirmação.
  - **Regras de Publicidade, versão 2** (`regras-publicidade.html`, em
    vigor desde 30/07/2026): 22 regras, do princípio editorial ao foro.
    Além do que não entra, a versão 2 fixa o lado comercial que protege a
    casa: pedido é proposta e só vira reserva com pagamento identificado;
    temporada em dias cheios; prazo de 2 dias úteis para a arte, e atraso
    dela não gera devolução nem extensão; a casa garante VEICULAÇÃO, não
    resultado (cliques, vendas, alcance), e os números são estimativas de
    boa-fé; queda de mais de 24h de responsabilidade da casa se compensa
    com EXTENSÃO da temporada, única compensação prevista; **nenhuma
    devolução em dinheiro** (desistência antes da estreia vira crédito de
    90 dias, depois da estreia não gera nada); uma troca de arte por
    temporada, sem estender prazo; sem exclusividade de categoria salvo
    acordo escrito; o anunciante responde por direitos e veracidade e
    mantém a casa a salvo; combinação só vale por escrito. O aceite grava
    a **versão** no pedido (`aceite_versao`), e a versão que vale é a do
    dia do aceite. **Ao mudar as regras, subir o número da versão** em
    `REGRAS_VERSAO` (no funil), no rodapé da página e aqui.
  - **Regras de conteúdo** (dentro da mesma página): o banco de
    regras da casa — o que não entra (ilegal, tabaco, armas, apostas
    e ganho fácil, conteúdo sexual explícito, risco a menores, saúde
    milagrosa, ódio, desinformação, propaganda eleitoral), regras de
    álcool, direitos sobre a arte, padrões da arte (nunca distorcida,
    nunca imitando o editorial) e o direito de recusa da direção. O
    ACEITE é obrigatório no envio e fica registrado com data e hora
    no pedido; a arte só vai ao ar depois da conferência da direção.
- **Programa de sala** (`programa-sala`): o playbill da estreia da
  semana, com moldura dourada, "quem está em cena" e ficha técnica em
  colunas. Só nomes APURADOS na cobertura da casa; personagem sem
  confirmação fica de fora (o elenco sai só com os nomes). Serviço em
  uma linha no pé.
- **O bilhete da semana** (campo `bilhete` da página `agenda`): a
  escolha ÚNICA da redação abrindo a agenda, impressa como ingresso:
  título, sessão recomendada (dia, hora, casa) e uma frase curta
  assinada "A redação". É curadoria da casa: nenhuma produção compra
  o bilhete, e a frase só afirma o que a cobertura já apurou.
- **Cartas da plateia** (`cartas`): 2 a 3 cartas REAIS chegadas ao
  e-mail da casa, com autorização de publicação, nome verdadeiro e
  cidade; resposta curta da direção quando couber. NUNCA inventar
  carta: sem carta real, a página simplesmente não entra na edição.
- **Três perguntas** (`tres-perguntas`): minientrevista EXCLUSIVA da
  revista, que nunca sobe ao site. Só entrevista feita pela própria
  casa, com as respostas guardadas POR ESCRITO (e-mail ou mensagem);
  resposta é aspa: entra literal, nunca ajeitada. A página imprime a
  nota de registro ("respostas enviadas por escrito à redação em
  DD/MM"). Sem registro escrito, a página não entra.

## As artes de palco da casa (conjunto APROVADO)

As 6 artes brutalistas da identidade (vinho/dourado/papel) foram
aprovadas pelo Pedro em 29/07/2026 e estão salvas em `assets/artes/`:
cada uma com o vetor mestre (`.svg`, 600x400) e 5 tamanhos em PNG
(`-paisagem` 1200x675 para cartões e site, `-faixa` 1200x400 para
banners e e-mail, `-vertical` 1080x1350 para feed de redes,
`-quadrado` 1080x1080 para post, `-story` 1080x1920 para stories).
Precisou de um tamanho novo? Exporta-se do vetor mestre, sem
redesenhar nada.

| Nº | Arquivo | Conceito |
|---|---|---|
| 1 | `arte-1-refletor` | O ator sob o refletor: o facho desce, a silhueta no centro da luz |
| 2 | `arte-2-cortina` | A cortina e a ribalta: as dobras terminam na ribalta; abaixo, o piso |
| 3 | `arte-3-plateia` | Alguém na plateia: a pessoa dourada ocupa UMA cadeira da malha |
| 4 | `arte-4-arena` | O teatro de arena: plateia completa dos dois lados, um ator só no centro |
| 5 | `arte-5-urdimento` | As cordas da coxia com os contrapesos alinhados |
| 6 | `arte-6-degraus` | A subida ao palco, com o canhão de luz aceso no alto |

**REGRA ABSOLUTA DA CASA — NENHUMA IMAGEM É DISTORCIDA, NUNCA**
(ordem do Pedro, 29/07/2026). Vale para TODA imagem do site, da
revista e da comunicação: fotos, artes, thumbnails, logos. Imagem
entra na proporção original; quando a caixa tem outra proporção, a
imagem é RECORTADA pelo centro (slice / `object-fit:cover`) ou
exibida inteira com sobra (`contain`), JAMAIS esticada. Em código:
`preserveAspectRatio="none"` é PROIBIDO em SVG; `width` + `height`
fixos num `<img>` exigem `object-fit`. Antes de entregar qualquer
página nova, conferir se nada ficou oval, achatado ou alargado.

As artes são sempre recortadas pelo centro (slice); nos recortes o
padrão pode sangrar para fora do quadro, mas a composição interna
fica inteira (fileiras completas, grades alinhadas). O desenho-fonte
vive em `tools/build_pages.py` (bloco DEFS, símbolos `ph-1` a
`ph-6`); mudar qualquer arte exige NOVA aprovação do Pedro e
re-exportação dos arquivos de `assets/artes/`.

## Entrega

1. Salvar cada pacote em `import/pauta/<slug>.json`.
2. Salvar as fotos de capa em `assets/uploads/`.
3. **Portão mecânico**: rodar
   `python3 tools/audita_pauta.py import/pauta/<slug>.json`
   e só seguir com laudo `✓` (ele confere travessão, tamanho, links,
   foto+crédito+fonte, agências proibidas, fontes, instagram, artes,
   editorias e status). Matéria reprovada NÃO entra no commit: corrigir
   ou descartar com registro no diário.
4. Registrar a rodada em `import/pauta/diario.json` (formato acima).
5. `git add import/pauta/ assets/uploads/ assets/social/` — e nada além disso.
6. Commit na branch `claude/foyer-digital-redesign-14l2b6` com mensagem
   `Redação IA: matérias na mesa de aprovação da Coxia [skip ci]`
   (o `[skip ci]` evita um deploy desnecessário — pauta não aparece no site).
7. `git push -u origin claude/foyer-digital-redesign-14l2b6`.
8. Faxina da lixeira: apagar de `import/lixeira/` os arquivos com
   `removidoEm` há mais de 30 dias (e incluir no commit).
9. Encerrar informando quantas matérias ficaram na mesa e seus títulos.
