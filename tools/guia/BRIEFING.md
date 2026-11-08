# GUIA INTERATIVO DO FOYER: briefing do projeto (08/11/2026, atualizado no mesmo dia com a Fase 1)

Pedido do Pedro Amaral (dono do FOYER.DIGITAL). Este arquivo é a fonte da
verdade do projeto. A sessão dedicada ao guia lê isto antes de tudo e o
mantém atualizado (decisões, fontes testadas, o que mudou).

## 1. O que é

Um guia cultural que entende do que a pessoa gosta e a leva exatamente ao
que ela tem mais chance de gostar de ver, já com o caminho até o ingresso.
Diferencial, nas palavras do Pedro: "ele te ajuda a achar o que você quer
ver". Não é uma lista de eventos: é um sistema de perguntas e preferências
que vai afunilando até o ideal para aquela pessoa, e que monta roteiros
("circuito de arte no fim de semana").

Começa em São Paulo, com recorte por região, por lugar e por gosto.

Áreas, todas desde o desenho inicial:
- **Teatro** (o coração do FOYER), inclusive musicais, dança, circo, ópera.
- **Cinema**: MUITO importante para o Pedro. Programação das salas, mostras
  e festivais, e o lado "Letterboxd" (abaixo).
- **Música** (shows, concertos).
- **Exposições e museus**.
- **Literatura** (lançamentos, feiras, saraus, clubes de leitura, debates).

Para cada programa, quando houver dado público: o que é, onde, quando,
quanto custa, classificação, duração, link oficial de ingresso, como chegar
(tempo até lá), metrô mais perto, e a ficha do lugar (café, estacionamento,
acessibilidade).

### O lado "Letterboxd"
O Pedro sempre quis, já começou num site anterior e descontinuou: as pessoas
registram o que viram (peça, filme, show, exposição) e dão nota, com diário,
resenha curta e listas. Isso alimenta a recomendação (gosto declarado mais
gosto demonstrado) e cria comunidade. Precisa de conta de usuário, então
entra depois do motor de dados (ver fases), e exige atualizar a política de
privacidade (decisão do Pedro; ele é o encarregado de dados).

## 2. Regra de ouro: 100% público, 100% verificável

Palavra do Pedro: "as informações têm que ser 100% do que conseguir pegar de
forma pública. O que não tiver a certeza ou a informação não tiver pública,
a gente não vai usar."

Na prática:
- Todo campo de todo registro guarda de onde veio (URL da fonte e data da
  coleta). Sem fonte, o campo não existe.
- Na dúvida, fica de fora. Nunca preencher por dedução: se o site do teatro
  não diz que tem café, a ficha não fala de café (nem "não tem").
- Horário, preço e data só da fonte primária ou de agenda pública confiável.
  Se duas fontes divergem, vale a mais próxima do lugar (site do teatro >
  bilheteria > agenda agregadora) e a divergência fica registrada.
- Respeitar robots.txt e os termos de uso de cada fonte. Fonte que proíbe
  coleta não entra. Coleta educada: User-Agent identificando o FOYER (nome
  genérico, sem e-mail pessoal), pausas, cache, nada de rajada.
- Nunca copiar texto de divulgação inteiro de terceiros: resumo próprio,
  curto, com link para a fonte. Imagem de terceiro só com licença clara.
- Ingresso: só link para a bilheteria oficial. O FOYER não vende ingresso.

## 3. Fontes: inventário (testado em 08/11/2026)

Teste feito com User-Agent do FOYER, lendo robots.txt e termos de cada uma.
"Rede da sessão" = teste daqui; a sonda diária (sondas.json) repete o teste
de dentro do GitHub, que tem outra rede.

| Fonte | Acesso | Formato | Robots e termos | Muda | Situação |
|---|---|---|---|---|---|
| **Guia OFF** (guiaoff.com.br/guia/) | aberto | página HTML bem organizada: um bloco por espetáculo com lugar, endereço, dias, hora, preço, duração, classificação, temporada, link | liberado; "Content-Signal: search=yes, ai-train=no, use=reference" | mensal, com ajustes no mês | **COLETOR PRONTO** (coleta_guiaoff.py). ~240 espetáculos/mês; ~150 a 190 em cartaz no dia |
| **Cinemateca Brasileira** | aberto | API do calendário (The Events Calendar): título, dia, hora, sala, categoria, link | liberado | diária | **COLETOR PRONTO** (coleta_calendario.py). Preço não vem: o guia não fala de preço |
| **SP Cultura** (Prefeitura) | recusou a conexão (connection reset) na rede da sessão; o site comum da Prefeitura dá 403 | API Mapas Culturais (conhecida) | não deu para ler | ? | **BLOQUEADO daqui.** A sonda diária testa do GitHub. Se abrir, é o próximo coletor |
| Dados Abertos SP (dados.prefeitura) | aberto | planilhas | CC-BY | esporádica | só relatórios passados de uma subprefeitura: não serve para agenda |
| **Sesc SP** | páginas abertas; a API de atividades responde 403 a robôs | páginas de evento com dias e horas; mapa do site (sitemap) com data de atualização de cada página | robots libera tudo; termos não proíbem. O 403 da API é bloqueio de propósito: **não contornar** | diária | **VIÁVEL pelas páginas + sitemap** (só as alteradas desde ontem). Próximo coletor. Cuidado: mistura cursos e esporte, filtrar por categoria |
| IMS (Paulista) | API aberta (mesmo calendário da Cinemateca) | sem sede (SP, Rio ou Poços) e preço "R$1" em quase tudo | liberado | diária | **FORA** pela regra de ouro até dar para confirmar a sede (talvez pela página do evento) |
| Theatro Municipal | API WordPress aberta ("eventos") | só título e link; data e preço na página | liberado | semanal | viável lendo as páginas |
| Reserva Cultural | API aberta ("programacao") | só filmes em cartaz, sem horário | liberado | semanal | horários não estão na API: investigar |
| Belas Artes, Teatro Porto, CineSesc | não responderam da rede da sessão | ? | ? | ? | testar de novo pela sonda |
| MASP, Pinacoteca, MAM, Itaú Cultural, Museu da Língua Portuguesa, CCBB, Japan House, Mostra | páginas abertas | HTML; Museu da Língua tem API de exposições ("exponova"); Pinacoteca e MAM com API fechada | robots liberam | mensal (exposições) | viáveis lendo páginas, um a um (Fase 1b) |
| CCSP | o endereço ccsp.com.br hoje é de outra entidade (Clube de Criação) | | | | achar o endereço certo do Centro Cultural São Paulo |
| Sympla, Ticket360 | abertos | páginas de evento | Ticket360 com "Content-Signal" igual ao Guia OFF | | **só como link de ingresso**, nunca como fonte de agenda (por ora) |
| Ingresso Rápido, Eventim | não responderam (Eventim: tempo esgotado) | | | | idem |
| Wikidata | aberto | API livre, sem chave | liberado | | para a ficha dos filmes (Fase 1b) |

**Primeira rodada no GitHub (08/11/2026, 14h33):** Guia OFF e Cinemateca
ok (187 programas publicados em foyer.digital/guia/). SP Cultura: tempo
esgotado também do GitHub. **Sesc: recusa até o robots.txt para a rede do
GitHub** (o mesmo bloqueio da API). Ou seja, um coletor do Sesc rodando no
Actions não entra. Caminhos a decidir com o Pedro: pedir ao Sesc acesso ou
parceria (eles têm a API pronta), ou rodar a coleta do Sesc de outro lugar
(só se o Sesc não estiver bloqueando de propósito; nunca contornar bloqueio).

**Ampliação (08/11/2026, pedido do Pedro: "incluir todas as fontes, na
ordem que achar melhor, com imagem"):** entraram Theatro Municipal
(coleta_municipal.py: lista pela API, datas, local, duração, classificação,
ingresso e foto pela página de cada evento, com cache), MASP e MAM
(coleta_exposicoes.py) e MIS (no coleta_calendario.py). Total: 6 fontes,
cerca de 216 programas no dia.
Testados e sem caminho seguro por enquanto: Belas Artes, Cinesala e Reserva
Cultural (horários não legíveis com segurança), Pinacoteca (404), Japan
House, Farol Santander e Teatro Santander (403 para robôs), Itaú Cultural
(página montada por JavaScript), Osesp, Tomie Ohtake, CCSP, Teatro Porto,
Blue Note, Sesi, Museu do Ipiranga, Oficina (sem dado estruturado: um leitor
por site, próximos da fila), Biblioteca Mário de Andrade e TUCA (não
responderam).

**Decisão sobre imagens (08/11/2026, pedido do Pedro):** só a foto oficial
que o próprio lugar publica para divulgar o evento (og:image ou a foto do
calendário dele). A foto não é copiada para o FOYER: a página aponta para o
endereço no site do lugar, mostra o crédito ("Divulgação / MASP: legenda") e
leva de volta à fonte. Se a foto sair do ar, o cartão some com ela. Guia OFF
não publica foto: as peças que só ele traz ficam sem imagem. Quando o guia
abrir ao público, o ideal é guardar as fotos no R2 com autorização dos
lugares ou das assessorias.

Observações importantes:
- **Guia OFF** sinaliza "use=reference" e "ai-train=no": o uso combinado é
  listar com link para eles (como um buscador) e trecho curto. O coletor é
  só código, sem IA. **Recomendação ao Pedro: avisar o Guia OFF / pedir
  parceria antes de abrir o guia ao público** (é trabalho editorial deles).
- Guia OFF escreve datas sem ano ("até 29/11"): o ano é deduzido da data da
  coleta e o campo leva a marca "ano deduzido".
- Os blocos de festival no Guia OFF trazem a atração em negrito, não o lugar:
  o coletor reconhece (sem endereço = atração) e não cria lugar falso.
- Lista de sites ainda não testados: Itaú Cultural/Espaço Itaú, Petra Belas
  Artes, Cinesala, Sesi, Oficina (agenda própria), Teatro Santander, Renault,
  Bradesco, Procópio, Farol Santander, Tomie Ohtake, MAC USP, Museu do
  Ipiranga, livrarias, Casa Guilherme de Almeida, Biblioteca Mário de Andrade,
  metrô (GTFS/OpenStreetMap).

## 4. Como funciona por dentro (proposta inicial, a sessão decide)

- Tudo dentro deste repositório, que já publica foyer.digital pelo GitHub
  Pages a partir da branch claude/foyer-digital-redesign-14l2b6.
- Coletores determinísticos em tools/guia/ (um por fonte), dados em
  import/guia/ (JSON, um formato só), montagem das páginas em guia/.
- Os coletores rodam numa rotina própria do GitHub Actions (por exemplo
  guia.yml, todo dia de madrugada). O repositório é público: Actions é de
  graça. Isso é o que torna o guia autogestado sem gastar os créditos do
  Pedro a cada rodada. O Claude entra em rodadas agendadas para o que exige
  julgamento: curadoria, resumo, ficha de lugar nova, conferência de
  divergências, respostas a leitores.
- Detecção automática de: evento repetido em fontes diferentes, temporada
  encerrada (sai sozinho no dia seguinte ao fim), mudança de horário ou
  preço, fonte que quebrou (avisar em vez de publicar dado velho).
- Recomendação: começa sem login, com o perfil guardado no próprio aparelho
  (perguntas de gosto, região, orçamento, dias livres). Depois, com conta,
  entram notas, diário e histórico.
- Contas e notas: Supabase do FOYER (projeto jcaqjlrzmrtzjyfbljxh), com
  tabelas próprias do guia, segurança por linha, nada que a Coxia use.
- Interação: caixa de mensagens no guia gravando no Supabase; o Claude lê e
  responde em rodadas agendadas, só com base em dado público.
- Fotos e artes: seguem o padrão do site (Cloudflare R2 via FOYER_CDN), para
  não estourar o 1 GB do GitHub Pages.
- Aplicativo próprio instalável, como a Coxia: manifest e escopo em /guia/.

## 4b. Como ficou (Fase 1, 08/11/2026)

- `tools/guia/comum.py`: busca educada (robots.txt, pausa de 1,5 s por site,
  User-Agent "FOYER-Guia/1.0", 3 tentativas) e o formato de campo com fonte.
- `tools/guia/coleta_guiaoff.py` e `tools/guia/coleta_calendario.py`: os dois
  primeiros coletores. Saem em `import/guia/brutos/`.
- `tools/guia/sonda_fontes.py`: testa todo dia SP Cultura e Sesc.
- `tools/guia/junta.py`: junta, tira o que acabou, liga repetidos, registra
  mudanças, segura fonte velha (3 dias). Sai em `import/guia/agenda.json`.
- `tools/guia/monta_pagina.py`: a página escondida `guia/index.html`, chamada
  pelo `build_pages.py` no fim (os três fluxos que publicam levam a página).
  Os dados vão embutidos na página, porque o site publicado não leva
  `import/guia/` (ver `.github/so-o-site.sh`). `guia/index.html` está no
  .gitignore.
- `.github/workflows/guia.yml`: "Relógio do Guia", todo dia 03:17 de SP. Roda
  os coletores, grava com `git pull --rebase` e pede a publicação
  (`gh workflow run pages.yml`). Custo: zero crédito do Claude.
- Formato dos dados: `tools/guia/FORMATO.md`.

## 5. Escondido por enquanto

Em desenvolvimento, o guia mora em foyer.digital/guia/ com noindex, fora do
sitemap, sem link no menu e sem aparecer em busca interna. Vira público só
quando o Pedro decidir. A Agenda atual do site (agenda.html) ainda tem
conteúdo de exemplo: quando o guia estiver confiável, ele pode alimentá-la.

## 6. Marca

Vai virar uma marca dentro do FOYER. A sessão propõe nomes (curtos, em
português, que digam "achar o que ver") e o Pedro escolhe. Até lá, "Guia".

Propostas de 08/11/2026 (aguardando o Pedro): **Deixa**, **Plateia**,
**Bússola**, **Programa**, **Achei**. Ver RELATORIO-FASE1.md.

## 7. Fases

1. **Motor de dados**: inventário e teste das fontes, formato único, um
   coletor por fonte (começar por Guia OFF e SP Cultura), fichas dos lugares
   mais relevantes, rotina diária no Actions, página escondida mínima para
   conferir os dados. Este é o produto de verdade: sem agenda certa, nada
   mais importa.
   *Situação em 08/11/2026*: feitos inventário, formato, coletores Guia OFF e
   Cinemateca, rotina diária e página escondida. Faltam (Fase 1b, nesta
   ordem): Sesc pelas páginas públicas, fichas dos lugares com metrô, museus,
   mais cinemas, ligação dos filmes ao Wikidata.
2. **Produto**: a tela do guia (filtros por área, região, lugar, data,
   preço, gosto), o questionário que afunila, o "monte seu roteiro" do fim
   de semana, aplicativo instalável, cinema completo.
3. **Gente**: contas, notas e diário estilo Letterboxd, listas, alertas,
   caixa de mensagens respondida pelo Claude.
4. **Renda** (decisões do Pedro): destaque pago para produtores e lugares,
   parcerias, afiliação de ingresso onde existir, assinatura com alertas.

## 8. Regras da casa (valem aqui também)

- Falar com o Pedro em português, sem jargão, com passo a passo quando ele
  precisar fazer algo. Ele não é técnico.
- Chaves e senhas nunca passam pelo chat (nem em print). Vão para os segredos
  do GitHub ou para o formulário seguro de credenciais.
- Texto editorial novo: PROIBIDO travessão e meia-risca.
- Nunca inventar @ de rede social, nome, cargo ou dado de pessoa.
- Não mexer nos fluxos da Coxia, em import/novas/, em import/equipe.json, na
  Revista nem na autoria das matérias.
- A Coxia grava na mesma branch o tempo todo: sempre git pull --rebase antes
  de push. HTML gerado não vai para o git (o build gera).
- Commits terminam com as linhas de atribuição pedidas pela sessão. Nenhum
  identificador de modelo em arquivo do repositório.
- Nunca clicar nos próprios anúncios. Nunca usar pkill/pgrep por nome de
  script. Nunca usar sleep para esperar evento externo.
- Créditos do Pedro são curtos: preferir trabalho determinístico no Actions
  a rodadas longas do Claude, e avisar o Pedro do custo de qualquer rotina
  agendada antes de ligá-la.
