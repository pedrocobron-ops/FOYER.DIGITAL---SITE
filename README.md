# FOYER — Novo site

Redesign do portal [foyer.digital](https://www.foyer.digital/): **brutalismo de instituição de arte** com a identidade oficial da marca (logo empilhada FOy/ER, dourado #CEB26A, vinho #4E0F09).

## Páginas

| Página | Arquivo | O que tem |
|---|---|---|
| Capa | `index.html` | Ticker, masthead com a logo oficial, manchete + O Giro, notícias, crítica, programas, enciclopédia |
| Notícias | `noticias.html` | Grade completa com filtros de editoria |
| Crítica | `critica.html` | Críticas com nota em didone e citação |
| Revista | `revista.html` | Newsletter semanal como revista: edições fechadas com capa, leitor online paginado e cadastro |
| Programas | `programas.html` | Os 5 programas + últimos episódios (YouTube/Spotify) |
| Enciclopédia | `enciclopedia.html` | Busca, estatísticas e índice de artistas (estilo MCDB) |
| Agenda | `agenda.html` | Estreias e eventos com data em didone |
| Entrevistas | `entrevistas.html` | Cards de citação com foto |
| Matéria (modelo) | `materia.html` | Página completa de matéria: capitular, olho em didone, fotos, compartilhamento e fatias de anúncio |
| Artista (verbete) | `artista.html` | Verbete da enciclopédia: trajetória com espetáculos clicáveis |
| Espetáculo | `espetaculo.html` | Ficha técnica completa com nomes clicáveis |
| Busca | `busca.html` | Busca instantânea (client-side; completa com o backend) |
| Privacidade | `privacidade.html` | Política de privacidade/LGPD — obrigatória para o AdSense |
| Coxia | `coxia.html` | **Central de conteúdo** (não linkada no menu) — cria, publica e agenda matérias direto no site via API do GitHub. Acesso restrito à equipe: senha pessoal de cada um, definida na aba Equipe (nunca documentada aqui) |

## Estrutura

- `assets/site.css` — todo o estilo (tokens de cor da marca, temas claro/escuro)
- `assets/site.js` — tema, revelação ao rolar, contadores, compartilhamento (Web Share API)
- `assets/logo/` — logo oficial otimizada (originais em `src/`)
- `fonts/` — Abril Fatface, Archivo (variável), Archivo Black, IBM Plex Mono (locais, sem CDN)
- As páginas são geradas com partials compartilhados; as artes de palco em SVG servem de placeholder das fotos e de capas das edições da revista

## Rodando

Sem build — sirva a pasta:

```
python3 -m http.server
# abra http://localhost:8000
```


## Coxia — publicação e agendamento

A Coxia (v3, em `tools/coxia_body.html`) é a central de controle completa: painel **Palco** (estatísticas + diário de atividades), **Nova matéria** com upload do arquivo da foto de capa (redimensionada no navegador e gravada em `assets/uploads/`), **Fila & agendadas**, **Redação IA** (mesa de aprovação + diário do processo) e **Equipe**.

- **Níveis de acesso**: os usuários vivem em `import/equipe.json` (senha guardada como hash SHA-256 com salt, nunca às claras). O papel `chefe` tem acesso total — inclusive ao painel Equipe, onde cadastra/edita/exclui autores, gera a senha única de cada um e acompanha o diário de atividades (cada publicação sai assinada no histórico: `Coxia [Nome]: …`). O papel `autor` escreve e publica as próprias matérias; a mesa da Redação IA só aparece para quem tem a permissão.
- A Coxia grava matérias em `import/novas/*.json` pela API do GitHub (token fine-grained com permissão Contents, colado uma única vez por navegador — aba Conexão). O robô de publicação regenera o site a cada mudança; o workflow `agendadas.yml` roda a cada 30 minutos e coloca no ar as matérias cuja hora chegou. Formato de texto: parágrafos separados por linha em branco, `## intertítulo`, `**negrito**`, `*itálico*`, `> citação`, `[link](url)`, `img:URL | legenda`.
- Honestidade sobre segurança: é um site estático — o portão de senhas organiza o acesso da equipe, mas a proteção real de escrita é o token do GitHub. Não guarde nada sigiloso no repositório.

## Redação de agentes de IA (com aprovação humana obrigatória)

A redação roda **dentro do Claude Code**, com a assinatura Claude do editor — sem chave de API à parte. O briefing completo da esteira está em `tools/REDACAO.md`: **Pauteiro** (varredura na web por notícias culturais recentes) → **Repórter** (apura e escreve) → **Editor de Estilo** (lapida) → **Chefe de Redação** (valida e dá nota/parecer). O resultado vai para `import/pauta/*.json` com status `aguardando_aprovacao` — **nada é publicado sem aprovação humana**.

- Uma rotina do Claude Code abre uma sessão todo dia às 09h (Brasília), segue o briefing e deixa as matérias na mesa. Para rodar na hora, basta pedir numa sessão do Claude Code: "rode a redação do Foyer".
- A aprovação é feita na Coxia, aba **🤖 Redação IA**: cada matéria aparece com nota e parecer do chefe de redação (agente), ressalvas a conferir e as fontes apuradas. Botões: ler, aprovar e publicar, aprovar e agendar, recusar.
- Ao aprovar, a matéria move de `import/pauta/` para `import/novas/` e entra no fluxo normal de publicação/agendamento. Ao recusar, é descartada.
- Transparência editorial: as matérias saem assinadas como "Redação Foyer" — sem personas falsas de jornalistas (proteção da marca e das políticas do AdSense).

## A mesa do Pedro (matérias assinadas, publicadas direto)

Fluxo criado em 14/10/2026 a pedido do Pedro: o Claude pesquisa, escreve, entrega na conversa e, **só depois que o Pedro aprova e marca a hora**, publica no site as matérias assinadas por Pedro Amaral. Regra canônica dele: nada sai sem autorização, e nunca duas matérias juntas (mínimo de 60 minutos entre elas). Manual completo em `tools/PEDRO.md`; ferramenta em `tools/mesa_pedro.py`.

- **Pautas quentes**: duas rodadas por dia (7h e 17h, Brasília), automáticas, com 1 a 3 rascunhos cada, guardados em `import/mesa-pedro/` (no repositório, nunca no site) até a palavra dele. Eixos: teatro musical, bilheteria, estreias, polêmicas, decisões de plataforma e teatro com repercussão nacional, sempre com o dinheiro como chão.
- **Pautas frias**: sob pedido (perguntas do público, listas, explicadores). Nos dias úteis, uma por dia às 7h, na fila que o Pedro alimenta; no sábado e no domingo saem duas, a dele às 7h e uma segunda às 17h, que é onde entram as frias escritas aqui (`proximo-fds` lista os fins de semana livres). Ele confirma cada data.
- **A régua do tamanho vem do assunto e foi medida no mercado** (14/10/2026: notícia cultural de 230 a 520 palavras no Omelete, CNN, Deadline e Exame; análise de 600 a 950 na Playbill, Agência Brasil e Gazeta do Povo; entrevista acima de 2.000). O FOYER fica acima da notícia do mercado: `nota` 250 a 400, `quente` 600 a 900, `contexto` 1.000 a 1.500, `perfil` 1.200 a 2.000, `resposta` 700 a 1.000, `explicador` 1.000 a 1.500, `lista` 1.200 a 1.800, cada porte com a própria cota de intertítulos e de páginas lidas. O portão também barra prosa de planilha, frase-tique, repertório repetido na semana e matéria sem parágrafo de fôlego.
- **Estrutura completa**: título, linha fina, editoria principal, até 2 secundárias, corpo no formato da Coxia, imagem com crédito e descritivo. A apuração fica no campo interno `apuracao` (o campo `fontes` sai impresso, por isso não é usado).
- **Imagem sempre**: divulgação oficial, Wikimedia Commons com licença conferida pela API, ou uma das seis artes de palco da casa.
- **Publicação**: `publica <slug> --ok --em "15/10 09:00"` só roda com a marca de autorização e a hora que o Pedro deu, recusa hora a menos de 60 minutos de outra matéria dele, move o rascunho para `import/novas/` na branch de produção (`claude/foyer-digital-redesign-14l2b6`, por um worktree em `../FOYER-PRODUCAO` quando a pasta atual está em outra branch), faz commit e push; o `pages.yml` monta o site em 2 a 3 minutos e o `agendadas.yml` solta as marcadas para depois. Correção, troca de foto e remoção estão no manual.

## A Revista (edições reais)

As edições vivem em `import/revista/edicoes/ed-N.json` e são montadas na Coxia (📖 Revista, só chefes): capa com manchete e chamadas, e páginas de tipos variados — matéria da semana (puxada do site), conteúdo exclusivo, editorial, citação, cartaz/divulgação de peças, página patrocinada, página livre e expediente automático. Cada edição guarda um `historico` com quem alterou o quê (visível no editor). Publicar gera `revista-ed-N.html` — leitor com cara de revista (navegação por páginas, setas do teclado, swipe e ⤓ PDF via impressão) — e a listagem em `revista.html`. A IA monta/pole rascunhos seguindo `tools/REVISTA.md`; publicar é sempre humano.

## Saguão (espaço da equipe) e métricas reais

Aba 🎭 Saguão na Coxia, aberta a toda a equipe: **Mural** (recados; posts de chefe destacados "Da direção" e fixáveis), **Palco de honra** (ranking real de matérias por leituras e compartilhamentos, semana/geral) e **Balcão de pautas** (sugestões da equipe). As métricas vêm de uma tabela isolada (`foyer_metricas`) no Supabase — `assets/site.js` registra 1 view por sessão por matéria e cada clique de compartilhar; a chave usada é pública (só permite inserir eventos; leitura apenas do agregado `foyer_ranking`).

## Publicidade (Google AdSense)

A infraestrutura está pronta e **desligada** — nenhum script do Google carrega até você ativar:

1. Crie a conta em [adsense.google.com](https://adsense.google.com) usando o domínio foyer.digital (o site precisa estar hospedado no domínio para a análise do Google).
2. Quando aprovar, copie o seu ID de editor (`ca-pub-…`).
3. Em `assets/ads.js`: cole o ID em `client` e mude `enabled` para `true`.
4. Em `ads.txt` (raiz): descomente a linha e cole o mesmo ID.
5. Publique. Todas as fatias `.ad-slot` (capa, listagens e dentro das matérias) passam a exibir anúncios responsivos automaticamente.

As fatias já estão posicionadas nos pontos de melhor desempenho sem quebrar a leitura: após o bloco de notícias e de crítica na capa, no fim das listagens, e na matéria (após a foto de capa, no meio do texto e após "Leia também").

## Matérias importadas do Wix

Acervo completo: **1.514 matérias** com texto integral, importadas pela API oficial (somente leitura).

- `tools/import_wix.py` — importador (rode com `WIX_API_KEY` e `WIX_SITE_ID` no ambiente; a chave nunca é gravada)
- `tools/build_pages.py` — gerador de todas as páginas a partir do acervo
- `import/wix/*.json.gz` — backup bruto da API
- `import/materias.json` + `import/corpo/*.html` — índice e corpos convertidos
- Notícias paginadas (24 por página) + páginas por editoria (`cat-*.html`) + busca no acervo inteiro (`assets/busca-index.json`)

## Importação do site antigo (Wix)

O Wix expõe o feed do blog em `https://www.foyer.digital/blog-feed.xml`. Baixe esse arquivo no navegador e suba no repositório (pasta `import/`) — o conteúdo das matérias vem dentro dele.

## Status

- [x] Direção brutalista aprovada, logo oficial integrada
- [x] Navegação multipágina real
- [x] Revista (leitor online + cadastro demo) e Coxia (admin demo)
- [x] Páginas de matéria, verbete, espetáculo, busca e privacidade
- [x] AdSense pronto para ativar (assets/ads.js + ads.txt)
- [x] Deploy automático no GitHub Pages (.github/workflows/pages.yml) — ativa quando o repositório ficar público
- [ ] Backend real: publicação de matérias, newsletter, PDF da revista, login seguro
- [x] Importação COMPLETA do Wix: 1.514 matérias com texto integral, fotos, autores reais e 18 editorias
- [ ] Enciclopédia com banco de dados
