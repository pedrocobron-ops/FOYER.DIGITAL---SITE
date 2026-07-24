# Redação de agentes do FOYER — briefing da esteira

Este arquivo é o manual que o Claude segue quando a rotina diária da redação
dispara (ou quando Pedro pede "rode a redação do Foyer"). São **6 matérias
por rodada**. A esteira reproduz
uma redação real: **Pauteiro → Repórter → Editor de Estilo → Chefe de
Redação → Mesa de aprovação humana (Coxia)**.

## Regra de ouro (inegociável)

**NUNCA publicar nada.** As matérias vão SOMENTE para `import/pauta/*.json`
com `"status": "aguardando_aprovacao"`. É proibido gravar em `import/novas/`,
alterar páginas do site ou qualquer outro arquivo. Quem aprova e publica é um
humano, na Coxia (aba Redação IA).

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
- Assinatura: sempre `"author": "Redação Foyer"` — sem personas falsas.

## Escrita humana (obrigatório — o Chefe de Redação REPROVA quem violar)

O texto deve soar como jornalista de carne e osso. Padrões proibidos:

1. **TRAVESSÃO É PROIBIDO.** Nem travessão (—) nem meia-risca (–) em
   lugar nenhum do texto, do título ou do serviço. No lugar: vírgula,
   dois-pontos, parênteses ou ponto final. Atribuição de citação com
   vírgula: `"...", afirma Fulana, diretora do espetáculo.`
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

## Grade semanal — o cardápio das 6 matérias do dia

Das 6 matérias diárias: **2 são notícias quentes** (seguindo a mistura da
varredura abaixo: máximo 1 de circuito de release, o resto fora da bolha)
e **4 vêm do cardápio de formatos**, sempre incluindo o PRATO DO DIA:

| Dia | Prato do dia (obrigatório) |
|---|---|
| Segunda | **Casas de Espetáculo** — a história de um teatro brasileiro, bem contada: fundação, reformas, glórias, incêndios, fantasmas, quem passou por lá (cat `Teatro` + `Bastidores`) |
| Terça | **Entenda** — explicador com pergunta direta no título: "O que faz um diretor musical?", "Quanto custa montar um musical no Brasil?" (cat `Bastidores` + a da área) |
| Quarta | **Quem é** — perfil de um nome em alta no teatro/música, com trajetória e o que está fazendo agora (cat da área da pessoa) |
| Quinta | **DOIS GUIAS DO FIM DE SEMANA, um por cidade** — duas matérias separadas: "O que fazer no fim de semana em São Paulo (DD a DD/MM)" e "O que fazer no fim de semana no Rio de Janeiro (DD a DD/MM)". NUNCA misturar as cidades na mesma agenda (quem segue a agenda está numa cidade só). Em cada uma: uma peça/evento por dia, de quinta a domingo, TODOS na mesma cidade, cada um com parágrafo de curadoria + serviço completo (local, horário, preço, onde comprar) + **FOTO PRÓPRIA DA PEÇA no corpo** (bloco `img:assets/uploads/<slug>-dia.jpg | legenda com crédito verdadeiro`, origem aceita conforme a regra de direitos e registrada em imgFonte): TODA peça do guia aparece com foto, sem exceção. A CAPA do guia é a foto da principal estreia da semana (ou da peça de maior relevância) daquela cidade. Assinado como curadoria da Redação Foyer (cat `Guia`). Na quinta, os dois guias ocupam o prato do dia + 1 vaga do cardápio (total do dia segue 6 matérias) |
| Sexta | **Lista** — ranking/seleção evergreen com o ano no título: "Os 10 musicais brasileiros mais importantes (2026)" (cat `Guia`) |
| Sábado | **Curiosidade bem explicada** — "Por que se diz 'merda' antes da estreia?", origem, versões, o que dizem os pesquisadores (cat `Bastidores` + `Teatro`) |
| Domingo | **Memória** — efeméride ou episódio histórico das artes brasileiras ligado à data ou à semana (cat `Bastidores` + a da área) |

As outras 2 vagas do cardápio: repetir qualquer formato acima ou
reforçar notícia, conforme o que a varredura do dia render de melhor.

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

## A esteira, papel por papel

1. **Pauteiro** — varredura na web (busca) por notícias RECENTES (últimos
   7 dias). Antes, conferir os títulos já cobertos (primeiros ~60 de
   `import/materias.json` e tudo em `import/pauta/` e `import/novas/`)
   para não repetir assunto. Produzir **6 pautas por rodada** seguindo a
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
4. **Chefe de Redação** — validação final com parecer honesto: título fiel
   e sem sensacionalismo? Alguma afirmação sem fonte? Datas e nomes
   consistentes? Dar nota 0–10, parecer em 1–2 frases e listar as
   ressalvas que o editor humano deve conferir antes de publicar.

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
 "author": "Redação Foyer",
 "img": "assets/uploads/<slug>.jpg",
 "imgCredito": "Foto: Divulgação",
 "corpo": "texto no formato da Coxia…",
 "fontes": ["https://…", "https://…"],
 "status": "aguardando_aprovacao",
 "chefe": {
  "aprovado": true,
  "nota": 8,
  "parecer": "avaliação em 1-2 frases para o editor humano",
  "ressalvas": ["pontos que o humano deve conferir antes de publicar"]
 },
 "geradoEm": "2026-07-22T12:00:00+00:00",
 "esteira": "pauteiro > reporter > editor-estilo > chefe-redacao",
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
  `"instagram": {"titulo": "…", "legenda": "…"}`.
  - `titulo`: o título da arte, com os DESTAQUES DOURADOS entre asteriscos
    (nomes de pessoas e títulos de peça): ex.
    `*Luisa Thiré* apresenta *"Valsa Nº 6"*, de Nelson Rodrigues, no Teatro Arena B3`.
  - `legenda`: 2 parágrafos adaptados da matéria (lead + contexto, tom de
    rede social, sem travessão), e o fecho EXATO da casa em 3 linhas:
    `Para conferir a matéria completa, acesse o site: www.foyer.digital`
    + `📷: <crédito sem o prefixo Foto:>` + `Por <autor>`.
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

## Entrega

1. Salvar cada pacote em `import/pauta/<slug>.json`.
2. Salvar as fotos de capa em `assets/uploads/`.
3. Registrar a rodada em `import/pauta/diario.json` (formato acima).
4. `git add import/pauta/ assets/uploads/ assets/social/` — e nada além disso.
5. Commit na branch `claude/foyer-digital-redesign-14l2b6` com mensagem
   `Redação IA: matérias na mesa de aprovação da Coxia [skip ci]`
   (o `[skip ci]` evita um deploy desnecessário — pauta não aparece no site).
6. `git push -u origin claude/foyer-digital-redesign-14l2b6`.
7. Faxina da lixeira: apagar de `import/lixeira/` os arquivos com
   `removidoEm` há mais de 30 dias (e incluir no commit).
8. Encerrar informando quantas matérias ficaram na mesa e seus títulos.
