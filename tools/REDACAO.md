# Redação de agentes do FOYER — briefing da esteira

Este arquivo é o manual que o Claude segue quando a rotina diária da redação
dispara (ou quando Pedro pede "rode a redação do Foyer"). A esteira reproduz
uma redação real: **Pauteiro → Repórter → Editor de Estilo → Chefe de
Redação → Mesa de aprovação humana (Coxia)**.

## Regra de ouro (inegociável)

**NUNCA publicar nada.** As matérias vão SOMENTE para `import/pauta/*.json`
com `"status": "aguardando_aprovacao"`. É proibido gravar em `import/novas/`,
alterar páginas do site ou qualquer outro arquivo. Quem aprova e publica é um
humano, na Coxia (aba Redação IA).

## Estilo da casa

O FOYER (foyer.digital) é um portal brasileiro de jornalismo cultural —
teatro, música e artes. Padrão editorial:

- Português do Brasil, jornalismo cultural profissional.
- Títulos informativos e diretos, sem caça-clique.
- Lide que responde o quê, quem, quando e onde.
- Parágrafos curtos; 400 a 700 palavras.
- Bloco de serviço ao final quando houver evento (local, datas, horários, ingressos).
- **Nunca inventar fatos, aspas ou dados** — tudo deve vir das fontes
  encontradas na apuração. Se um dado não estiver nas fontes, não afirmar.
- Citação (`> `) só para declaração textual REAL de fonte pública, com
  atribuição no texto.
- Assinatura: sempre `"author": "Redação Foyer"` — sem personas falsas.

## A esteira, papel por papel

1. **Pauteiro** — varredura na web (busca) por notícias RECENTES (últimos
   7 dias) de teatro, música, dança e cultura no Brasil: estreias,
   temporadas, elencos, editais, premiações, festivais, turnês. Antes,
   conferir os títulos já cobertos (primeiros ~60 de `import/materias.json`
   e tudo em `import/pauta/` e `import/novas/`) para não repetir assunto.
   Escolher as 2 melhores pautas (relevantes, verificáveis, com fontes
   confiáveis), salvo pedido de outra quantidade ou editoria específica.
2. **Repórter** — apurar cada pauta com mais buscas: confirmar datas,
   locais, nomes completos, valores de ingresso, declarações públicas.
   Escrever a matéria completa no formato do corpo (abaixo).
3. **Editor de Estilo** — reler e lapidar: ritmo, clareza, repetições,
   clichês, concordância. Não acrescentar fatos nem remover informações.
4. **Chefe de Redação** — validação final com parecer honesto: título fiel
   e sem sensacionalismo? Alguma afirmação sem fonte? Datas e nomes
   consistentes? Dar nota 0–10, parecer em 1–2 frases e listar as
   ressalvas que o editor humano deve conferir antes de publicar.

## Formato do corpo (formato da Coxia)

Parágrafos separados por linha em branco; `## ` para intertítulo; `> ` para
citação real; `**negrito**` para nomes de obras; `[link](url)` se preciso.

## Formato do pacote — `import/pauta/<slug>.json`

```json
{
 "title": "Título da matéria",
 "slug": "titulo-da-materia",
 "cat": "Teatro",
 "author": "Redação Foyer",
 "img": "",
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
 "esteira": "pauteiro > reporter > editor-estilo > chefe-redacao"
}
```

- `slug`: ASCII minúsculo, hifens, máx. 80 caracteres, sem acentos.
- `cat` — uma de: Teatro, Cinema, Música, Dança, Crítica, Notícia,
  Televisão, Streaming, Literatura, Exposições, Show, Audições, Edital,
  Festa, Programa.
- JSON com `ensure_ascii` desligado (acentos legíveis) e indentação 1.

## Entrega

1. Salvar cada pacote em `import/pauta/<slug>.json`.
2. `git add import/pauta/` — e nada além disso.
3. Commit na branch `claude/foyer-digital-redesign-14l2b6` com mensagem
   `Redação IA: matérias na mesa de aprovação da Coxia [skip ci]`
   (o `[skip ci]` evita um deploy desnecessário — pauta não aparece no site).
4. `git push -u origin claude/foyer-digital-redesign-14l2b6`.
5. Encerrar informando quantas matérias ficaram na mesa e seus títulos.
