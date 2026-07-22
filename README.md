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
| Coxia | `coxia.html` | **Central de conteúdo** (não linkada no menu) — cria, publica e agenda matérias direto no site via API do GitHub. Senha de acesso: `terceirosinal` + token fine-grained do GitHub |

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
