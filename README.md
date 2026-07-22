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

## Status

- [x] Direção brutalista aprovada, logo oficial integrada
- [x] Navegação multipágina real
- [x] Revista (leitor online + cadastro demo) e Coxia (admin demo)
- [ ] Hospedagem (GitHub Pages / Vercel)
- [ ] Backend real: publicação de matérias, newsletter, PDF da revista, login seguro
- [ ] Importação das matérias do site antigo (aguardando export)
- [ ] Enciclopédia com banco de dados
