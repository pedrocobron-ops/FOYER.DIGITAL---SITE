# Ensaio dos 4 jornalistas — 17/08/2026

Quatro agentes com perfis muito diferentes trabalharam de verdade dentro da Coxia,
no palco de ensaio (gravações de mentira, nada tocou o site real). Zero erros de
JavaScript nas quatro jornadas. Este é o consolidado; os relatórios individuais
estão resumidos ao fim.

Os perfis:
- **Tomás, 22** — estagiário no primeiro dia (papel Escritor). Escreveu e enviou
  uma matéria de 424 palavras se virando sozinho.
- **Glória, 58** — editora-chefe veterana do impresso, impaciente. Triagem da
  mesa inteira contando cliques; aprovou, agendou, recusou, usou o lote.
- **Rafa, 31** — editor de arte e social media perfeccionista (monitor 1920px).
  Revista (36 páginas folheadas), Instagram, Divulgação, tema escuro. ~40 prints.
- **Dona Marta, 64** — correspondente que cobre estreias à noite pelo celular
  (390×844), com internet ruim. Publicou nota de 333 palavras no telefone.

---

## ERROS GRAVES (3)

**G1. Escritor tem acesso total à Publicidade.** (Tomás)
Entrar como autor → menu → Publicidade: a tela abre inteira, com dados de
anunciantes (contratos, URLs, "VENDIDO") e botões operáveis ("Tirar do ar",
"Salvar e pôr no ar", "Reservar na revista"). As outras áreas da chefia barram
com recado educado; esta ficou fora da cerca. Causa: `aplicarUsuario()` esconde
mi-equipe/mi-revista/mi-metricas/mi-ia mas não `mi-pub`, e `irPara('pub')` não
está na trava `SO_CHEFE`.

**G2. Mesa e Fila "mentem" quando a internet falha pela metade.** (Dona Marta)
Uso normal → rede cai → voltar à mesa ou à Fila: a listagem vem do cache mas os
arquivos falham e caem num `catch(){ return null }` silencioso. Resultado: "Mesa
vazia — nenhuma matéria aguardando aprovação" com 19 matérias esperando; Fila
"Nenhuma matéria por aqui ainda". O chefe fecha o celular achando que está tudo
em dia. Na carga fria o erro honesto com "Tentar de novo" JÁ existe (a Lixeira é
o exemplo) — só o caminho de falha parcial não passa por ele.

**G3. Divulgação exporta arte quebrada sem avisar.** (Rafa)
No formato feed 1080×1080, os itens colidem com a linha de apoio mesmo com 4
itens realistas; com lista longa, atropelam o rodapé nos dois formatos. Dá para
baixar a arte ilegível sem nenhum aviso. Falta o cálculo vertical (medir
título+apoio+itens+rodapé antes de desenhar, reduzir corpo ou avisar "cabem N").

## ERROS MÉDIOS

- **M1. O resumo da triagem esconde as ressalvas do checador.** (Glória) Card
  fechado mostra título/nota/parecer clampado; "CONTATO NÃO TENTADO" e "aspas
  traduzidas" só aparecem no Ver completo — dá para aprovar em 2 cliques sem ver
  o risco. Sugestão: selo curto de ressalva ao lado da nota no card fechado.
- **M2. Métricas: caiu o medidor, só a seção 1 avisa; as seções 2–10 ficam em
  "Carregando…" para sempre.** (Glória + Rafa) Falhou → falhou tudo, com um
  aviso e um Tentar de novo só.
- **M3. Filtros da Fila contam errado a matéria "Na mesa do chefe".** (Tomás)
  Chips dizem "No ar (1)" com 0 cards; "Agendadas (0)" mostra 1. `nAr` não
  desconta itens da mesa e o card da mesa recebe classe de filtro `ag`.
  Sugestão: chip próprio "Na mesa (N)".
- **M4. "Folhear a edição" não aparece depois de salvar edição nova** — só ao
  fechar e reabrir (`salvarEd` não rechama `renderEd`). (Rafa)
- **M5. Prova de gráfica dá 404 sem aviso visível** nos ~2 min até o site
  remontar (o único aviso é tooltip). Sugestão: interstitial "a prova está sendo
  montada (~2 min)" com verificação automática, no padrão do "Ver se a arte nova
  ficou pronta" do Instagram. (Rafa)
- **M6. A barra Salvar/Publicar/Folhear do editor da revista nasce atrás do
  cabeçalho fixo** ao abrir uma edição (auto-scroll sem scroll-margin). (Rafa)
- **M7. Mesa: miniaturas de Instagram de ~94×118px** — o chefe aprova a arte
  sem conseguir vê-la. E o clamp do parecer imprime texto sobre texto na linha
  do corte em alguns cards. (Rafa)
- **M8. Letras abaixo de 12px no celular**: semana da casa (9,6–11,5px), fontes
  apuradas (8,6px), links de fonte (9,6px), rótulo do "↑ topo" (9,9px), selos.
  Piso de 12px (ideal 13–14) para tudo que se lê. (Dona Marta)
- **M9. Menu no celular é fita lateral sem sinal de que continua** — Calendário,
  Publicidade, Divulgação e Conexão ficam fora da tela e só há uma setinha.
  (Dona Marta)
- **M10. Busca da Fila sem relevância**: "meia entrada" devolve 34 resultados
  porque busca as palavras no corpo inteiro; título/editoria deviam pesar mais.
  (Glória)
- **M11. Divulgação corta o título no meio da palavra, sem reticências.** (Rafa)

## ERROS LEVES

- Travessão "banido" passa no envio sem barrar nem confirmar (só o alerta
  discreto durante a digitação). (Tomás)
- Balcão de pautas não confirma sucesso (o mural confirma). (Tomás)
- Status do rascunho contradiz o toast ("guardado na nuvem" × "neste
  navegador"); contador "Rascunhos (N)" só atualiza ao reentrar. (Tomás)
- "cabe em: release" ignora intertítulos (release é 0 intertítulo). (Tomás)
- Matéria QUENTE agenda para semana que vem sem o agendador latir. (Glória)
- "Ver completo" não abre o corpo junto ("Ler a matéria inteira" fica a mais um
  clique, e a casa cobra a leitura). (Glória)
- Cards "?" do Palco não explicam o porquê (o Saguão explica). (Tomás + Glória)
- Autor não tem busca nenhuma de temas antes de sugerir pauta. (Tomás)
- "Recusar" deveria chamar "Devolver" quando a matéria é de gente da casa. (Glória)
- Chamadas de capa aceitam mais de 3 sem aviso (a 4ª não imprime). (Rafa)
- Página nova entra DEPOIS da contracapa; sempre exige reordenar. (Rafa)
- BLACKOUT: cartucho da capa da revista quase ilegível (vinho sobre preto). (Rafa)
- Pager "1/36" do folheador cobre as chamadas da capa; pior com cookie banner. (Rafa)
- Celular: "Enviar para o site" sem confirmação; sucesso discreto demais. (Dona Marta)
- Celular: botões de Enviar ficam 3 telas abaixo com o teclado aberto (régua
  sticky resolveria). (Dona Marta)
- Conteúdo (não é código): lede repetido no corpo da Piaf (ed. 4, pág. 9);
  legenda de IG de "As Troianas" repete estreia/local. (Rafa)

## O QUE GANHOU ELOGIO (manter)

- Zero erros de JavaScript nas 4 jornadas; zero rolagem horizontal no celular
  (9 abas medidas); alvos de toque ≥ 44px na mesa e na fila.
- Aviso de falta de chave na Nova matéria com "Ir para Conexão" (Dona Marta:
  "excelente"); barreiras de área com nome de gente ("fale com o Pedro ou a
  Isabel"), não "erro 403".
- Espelho ao vivo, régua com alvo ("faltam 206 palavras para 350–500") e
  Padrão da casa: o estagiário aprendeu sozinho.
- Triagem: aprovar em 2 cliques, agendar em 3–4 vendo a escalação do dia; lote
  real (3 aprovadas em 5 cliques); recusa com motivo registrado. Glória: "o
  melhor que já usei".
- Busca única da Fila cruzando fila + mesa + acervo; "tema livre para você
  lançar ✓".
- A revista em si: "um espetáculo" (capa, sumário, capitular, recortes com fita,
  contracapa); sala de leitura no escuro.
- Rascunhos sem perder nada, com aviso honesto de que a foto não fica no rascunho.
- Trava de assinatura em tudo, inclusive no lote; lixeira de 30 dias com
  confirmações certas.

## CONSERTADO (17/08/2026, a pedido do Pedro: "arrume todos os erros")
- Os 3 GRAVES: cerca da Publicidade (botão escondido + trava com o nome certo
  da aba); mesa/Fila honestas sob falha parcial de rede (aviso + Tentar de
  novo no lugar de "vazia"); Divulgação apara itens e reduz o corpo até caber
  (aviso "couberam N de M"), título com reticências.
- Os 11 MÉDIOS: ressalvas do checador no card resumido; Métricas falhou-falhou-
  tudo; chip "Na mesa (N)" com contas certas; Folhear após o 1º salvamento;
  prova em remontagem explica os ~2 min; barra do editor visível; miniaturas
  IG de 230px + parecer sem sobreposição; piso de letra ~12px; setinha "›" no
  menu do celular (some no fim); busca com peso título/corpo.
- Os LEVES: travessão pergunta antes de enviar; publicar direto confirma com o
  título + toast; "cabe em" confere intertítulos; QUENTE late ao agendar para
  depois de hoje; Ver completo abre o corpo; Palco com traço explicado (e o
  fetch do painel ganhou if(!r.ok)); pauta sugerida confirma; status de
  rascunho coerente (navegador + nuvem) e contador em dia; busca do acervo
  aberta a todos (Editar segue de editor); "Devolver ao autor" com nome de
  devolver; contador "N de 3 chamadas"; página nova antes da contracapa;
  cartucho da capa dourado no BLACKOUT; painel do folheador quase some na
  capa; régua de enviar sticky no celular; lede da Piaf sem eco na ed. 4.
- NÃO reproduzido: a legenda de IG repetida de "As Troianas" (o card que o
  Rafa viu já saiu da mesa; nenhum arquivo atual tem a legenda).
