# GUIA INTERATIVO DO FOYER: briefing do projeto (08/11/2026)

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

## 3. Fontes a investigar (lista inicial, validar cada uma)

Nada aqui foi testado ainda. O primeiro trabalho é testar uma a uma:
acessível daqui? que formato? termos permitem? com que frequência muda?
- **Guia OFF**: indicação do Pedro. Publica todo mês o "livretinho" aberto,
  com a agenda completa do mês teatral de São Paulo. Fonte principal de
  teatro. Ver formato (PDF? página?) e termos.
- **SP Cultura** (agenda da Prefeitura de São Paulo, dados abertos).
- **Sesc São Paulo** (programação pública de todas as unidades).
- Teatros e centros culturais com agenda própria: Theatro Municipal, CCSP,
  Itaú Cultural, IMS Paulista, Teatro Sérgio Cardoso, Teatro Porto, Sesi,
  Oficina, Teatro Santander, Renault, Bradesco, Procópio Ferreira etc.
- Museus: MASP, Pinacoteca, MAM, MAC USP, Museu da Língua Portuguesa, Museu
  do Ipiranga, CCBB SP, Japan House, Farol Santander, Instituto Tomie Ohtake.
- Bilheterias com páginas públicas de evento (Sympla, Ingresso Rápido,
  Eventim, Ticket360, Bilheteria Express): só leitura de páginas públicas e
  só se os termos permitirem.
- Cinema: programação pública das salas (Belas Artes, Reserva Cultural,
  Petra Belas Artes, Cinesala, Espaço Itaú, Cinemateca, CineSesc, redes),
  Mostra Internacional de Cinema de São Paulo, festivais. Dados de filmes:
  preferir Wikidata/Wikipédia (livre, sem chave). TMDB exige chave gratuita:
  se for preciso, pedir ao Pedro pelo formulário seguro de credenciais,
  nunca pelo chat.
- Literatura: Bienal, Flip (fora de SP, só referência), livrarias com agenda
  pública (Megafauna, Martins Fontes, Livraria da Travessa, Blooks), Casa
  Guilherme de Almeida, Biblioteca Mário de Andrade.
- Como chegar: estações de metrô e trem a partir de dado aberto (Metrô SP,
  CPTM ou OpenStreetMap). Tempo de deslocamento: link de rota do Google Maps
  (gratuito, sem API paga). Café, estacionamento e acessibilidade: só do
  site oficial do lugar ou de etiqueta do OpenStreetMap com fonte.

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

## 5. Escondido por enquanto

Em desenvolvimento, o guia mora em foyer.digital/guia/ com noindex, fora do
sitemap, sem link no menu e sem aparecer em busca interna. Vira público só
quando o Pedro decidir. A Agenda atual do site (agenda.html) ainda tem
conteúdo de exemplo: quando o guia estiver confiável, ele pode alimentá-la.

## 6. Marca

Vai virar uma marca dentro do FOYER. A sessão propõe nomes (curtos, em
português, que digam "achar o que ver") e o Pedro escolhe. Até lá, "Guia".

## 7. Fases

1. **Motor de dados**: inventário e teste das fontes, formato único, um
   coletor por fonte (começar por Guia OFF e SP Cultura), fichas dos lugares
   mais relevantes, rotina diária no Actions, página escondida mínima para
   conferir os dados. Este é o produto de verdade: sem agenda certa, nada
   mais importa.
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
