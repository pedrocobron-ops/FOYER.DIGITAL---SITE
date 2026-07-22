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

A Coxia grava matérias em `import/novas/*.json` pela API do GitHub (token fine-grained com permissão Contents no repositório, colado uma única vez no painel). O robô de publicação regenera o site a cada mudança; o workflow `agendadas.yml` roda a cada 30 minutos e coloca no ar as matérias cuja hora chegou. Formato de texto: parágrafos separados por linha em branco, `## intertítulo`, `**negrito**`, `*itálico*`, `> citação`, `[link](url)`, `img:URL | legenda`.

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
