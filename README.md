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
| Coxia | `coxia.html` | **Área restrita da redação** (não linkada no menu) — painel para criar matérias. Senha do protótipo: `terceirosinal` |

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


## Publicidade (Google AdSense)

A infraestrutura está pronta e **desligada** — nenhum script do Google carrega até você ativar:

1. Crie a conta em [adsense.google.com](https://adsense.google.com) usando o domínio foyer.digital (o site precisa estar hospedado no domínio para a análise do Google).
2. Quando aprovar, copie o seu ID de editor (`ca-pub-…`).
3. Em `assets/ads.js`: cole o ID em `client` e mude `enabled` para `true`.
4. Em `ads.txt` (raiz): descomente a linha e cole o mesmo ID.
5. Publique. Todas as fatias `.ad-slot` (capa, listagens e dentro das matérias) passam a exibir anúncios responsivos automaticamente.

As fatias já estão posicionadas nos pontos de melhor desempenho sem quebrar a leitura: após o bloco de notícias e de crítica na capa, no fim das listagens, e na matéria (após a foto de capa, no meio do texto e após "Leia também").

## Importação do site antigo (Wix)

O Wix expõe o feed do blog em `https://www.foyer.digital/blog-feed.xml`. Baixe esse arquivo no navegador e suba no repositório (pasta `import/`) — o conteúdo das matérias vem dentro dele.

## Status

- [x] Direção brutalista aprovada, logo oficial integrada
- [x] Navegação multipágina real
- [x] Revista (leitor online + cadastro demo) e Coxia (admin demo)
- [x] Páginas de matéria, verbete, espetáculo, busca e privacidade
- [x] AdSense pronto para ativar (assets/ads.js + ads.txt)
- [ ] Hospedagem (GitHub Pages / Vercel)
- [ ] Backend real: publicação de matérias, newsletter, PDF da revista, login seguro
- [ ] Importação das matérias do Wix (aguardando blog-feed.xml)
- [ ] Enciclopédia com banco de dados
