# FOYER — Novo site

Redesign do portal [foyer.digital](https://www.foyer.digital/): **brutalismo de instituição de arte** com a identidade existente da marca.

## Direção de arte

Referências: Whitney Museum (estrutura brutalista + navegação de instituição séria) e a linguagem industrial de catálogo da moda de luxo (Balenciaga/Off-White). Cores do logo oficial do Foyer.

- **Cores**: vinho oxblood `#4A100E` + dourado `#D6B26E` (do logo), papel bone `#EFE9DB`, tinta `#16100D`. Temas claro ("Luz da sala") e escuro ("Blackout").
- **Tipografia** (arquivos em `fonts/`, servidos localmente):
  - *Abril Fatface* — didone pesado que casa com o wordmark FOy/ER; masthead, títulos dos programas, notas de crítica, números
  - *Archivo Black* — manchetes e cabeçalhos de seção em caixa-alta
  - *Archivo* (variável) — texto corrido, navegação, títulos secundários
  - *IBM Plex Mono* — ticker, timestamps, etiquetas, dados, tabela da enciclopédia
- **Estrutura**: grid industrial com bordas expostas (linhas de 1–2px em toda parte), hover com inversão dura (tinta→dourado, vinho→dourado), sem cantos arredondados, sem sombras.

## Seções da capa

1. **Ticker** de últimas notícias (letreiro contínuo, vinho/dourado)
2. **Masthead** — wordmark FOy/ER empilhado em didone dourado sobre vinho, flanqueado por dados de edição em mono
3. **Nav** fixa em barra contínua com separadores
4. **Capa** — manchete em Archivo Black + coluna "O Giro" (fio de notícias com timestamps) = alta densidade de notícia
5. **Notícias** — grade 4 colunas com células de grid exposto
6. **Crítica** — notas em didone sobre bloco vinho + citação
7. **Programas** — faixa vinho com os 5 shows (YouTube/Spotify)
8. **Enciclopédia do Teatro Musical Brasileiro** — estatísticas + índice tabular de artistas (estilo MCDB; fase 2 com banco de dados)
9. Newsletter + footer com FOYER gigante cortado

## Rodando

Arquivo único, sem build — sirva a pasta (as fontes carregam de `fonts/`):

```
python3 -m http.server
# abra http://localhost:8000
```

## Status

- [x] Protótipo da capa com a nova direção brutalista
- [ ] Aprovação da direção visual
- [ ] Páginas internas (matéria, crítica, programa, agenda)
- [ ] Migração para Next.js + CMS
- [ ] Enciclopédia (banco de dados de pessoas/produções)
