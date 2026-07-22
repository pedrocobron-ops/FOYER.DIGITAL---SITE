# A Revista do FOYER — briefing para a IA montar/polir edições

Este arquivo é o manual que o Claude segue quando Pedro pede
**"monte a edição da semana da revista"** ou **"deixe a edição Nº X incrível"**.

## Regra de ouro

A IA só produz **RASCUNHO**. `"status"` é sempre `"rascunho"` — quem publica é
o chefe, no editor da Revista (Coxia → 📖 Revista). Toda mexida da IA entra no
`historico` assinada como `"Redação IA (Claude)"`.

## Onde vivem as edições

`import/revista/edicoes/ed-<numero>.json` — uma edição por arquivo. O número da
nova edição é o maior existente + 1. O site gera `revista-ed-<numero>.html`
(leitor com cara de revista) apenas para edições com status `publicada`.

## Formato da edição

```json
{
 "numero": 2,
 "titulo": "título interno da edição",
 "dataEdicao": "31 Jul 2026",
 "status": "rascunho",
 "capa": {
  "img": "assets/uploads/revista-ed-2-capa.jpg",
  "manchete": "manchete grande da capa",
  "chamadas": ["chamada 1", "chamada 2", "chamada 3"]
 },
 "paginas": [
  {"tipo": "editorial", "titulo": "…", "texto": "formato da Coxia", "assinatura": "A direção do FOYER"},
  {"tipo": "materia", "slug": "slug-no-site", "cat": "Teatro", "img": "…", "titulo": "…", "chamada": "linha fina", "texto": "resumo opcional"},
  {"tipo": "exclusiva", "titulo": "…", "texto": "…", "img": "…", "imgCredito": "Foto: …"},
  {"tipo": "citacao", "frase": "…", "autor": "…"},
  {"tipo": "cartaz", "img": "…", "legenda": "…", "link": "https://…"},
  {"tipo": "patrocinio", "img": "…", "legenda": "…", "link": "https://…"},
  {"tipo": "livre", "rotulo": "…", "titulo": "…", "texto": "…"},
  {"tipo": "expediente"}
 ],
 "historico": [{"quando": "ISO", "quem": "Redação IA (Claude)", "acao": "monta o rascunho da edição"}]
}
```

## Receita de uma boa edição semanal

1. **Capa** — manchete forte tirada da melhor matéria da semana; usar a foto
   dessa matéria como imagem de capa (ou baixar a arte de divulgação para
   `assets/uploads/revista-ed-<n>-capa.jpg`); 3 chamadas.
2. **Editorial** — carta ao leitor (150–250 palavras) costurando a semana:
   o que aconteceu, o que vem aí, um ponto de vista da casa.
3. **4 a 6 matérias da semana** — as melhores de `import/novas/` (da semana)
   e/ou as mais recentes de `import/materias.json`: usar `slug`, `img`, `cat`
   reais; escrever chamada nova (não repetir o excerpt) e um resumo de 2–3
   parágrafos no campo `texto`. Variar editorias.
4. **1 página de citação** — a melhor frase REAL da semana (de matéria ou
   entrevista), com atribuição.
5. **1 exclusiva** (opcional, se houver material): análise ou panorama da
   semana escrito para a revista, no padrão profissional do FOYER
   (ver tools/REDACAO.md — nunca inventar fatos).
6. **Cartazes/patrocínio** — NUNCA criar: só o chefe sobe. Se já existirem
   páginas desses tipos na edição, preservá-las na ordem.
7. **Expediente** — última página, `{"tipo": "expediente"}`.

## Ao polir uma edição existente ("deixe incrível")

- Melhorar manchete, chamadas, chamadas de matérias e editorial (texto).
- Reordenar páginas para ritmo de leitura: capa → editorial → matéria forte →
  variedade → citação como respiro → cartazes → expediente no fim.
- NUNCA remover páginas de cartaz/patrocínio nem trocar imagens que o chefe
  subiu. Nunca mudar `status`.
- Registrar no `historico` o que foi feito.

## Entrega

1. Gravar o JSON da edição e as imagens que tiver baixado.
2. `git add import/revista/ assets/uploads/` — e nada além disso.
3. Commit: `Revista: rascunho da edição N pela IA [skip ci]` e push na branch
   `claude/foyer-digital-redesign-14l2b6`.
4. Avisar o chefe: a edição está na Coxia (📖 Revista) esperando o toque final.
