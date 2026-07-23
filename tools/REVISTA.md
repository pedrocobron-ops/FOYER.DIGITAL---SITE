# A Revista do FOYER — briefing para a IA montar/polir edições

Este arquivo é o manual que o Claude segue quando a rotina semanal dispara
(**toda quinta-feira**) ou quando Pedro pede **"monte a edição da semana da
revista"** / **"deixe a edição Nº X incrível"**.

## Regra de ouro

A IA só produz **RASCUNHO**. `"status"` é sempre `"rascunho"` — quem publica é
o chefe, no editor da Revista (Coxia → 📖 Revista). Toda mexida da IA entra no
`historico` assinada como `"Redação IA (Claude)"`.

## O que é a revista (leia antes de escrever)

A revista NÃO é uma coleção de páginas de notícia do site. É uma edição
fechada, com cara de revista impressa: capa de banca, sumário, ritmo de
leitura, começo, meio e fim. A regra que o Pedro deu: *"deve pegar as matérias
do site e **transformar em conteúdo de revista**"*. Ou seja:

- **Reescrever, nunca copiar.** A chamada e o `texto` de cada página de
  matéria são escritos PARA a revista: tom de revista (mais autoral, mais
  contexto, menos "hard news"), sem repetir o excerpt do site.
- A página de matéria fecha com "Leia a íntegra no site" automaticamente —
  o `texto` é um aperitivo bem escrito de 2–3 parágrafos, não a matéria inteira.
- Padrão de escrita humana do FOYER vale aqui também (tools/REDACAO.md):
  travessão proibido, sem clichês de IA, fatos reais somente.

## Onde vivem as edições

`import/revista/edicoes/ed-<numero>.json` — uma edição por arquivo. O número da
nova edição é o maior existente + 1. O site gera `revista-ed-<numero>.html`
(leitor em formato de revista impressa) apenas para edições com status
`publicada`.

## O leitor monta sozinho

- **Página 1 = capa** (gerada a partir do bloco `capa`): logo do FOYER sobre a
  imagem, manchete grande, chamadas na lateral e barra de rodapé de banca.
- **Página 2 = Sumário** — montado automaticamente a partir das páginas.
  NÃO criar página de sumário.
- Rodapé corrido (nº da edição, página, data) em todas as páginas internas.

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
  "chamadas": ["chamada 1", "chamada 2", "chamada 3", "chamada 4"]
 },
 "paginas": [
  {"tipo": "editorial", "titulo": "…", "texto": "formato da Coxia", "assinatura": "A direção do FOYER"},
  {"tipo": "materia", "slug": "slug-no-site", "cat": "Teatro", "img": "…", "titulo": "…", "chamada": "linha fina", "texto": "aperitivo reescrito (2–3 parágrafos)"},
  {"tipo": "exclusiva", "titulo": "…", "texto": "…", "img": "…", "imgCredito": "Foto: …"},
  {"tipo": "programas"},
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
   dessa matéria como imagem de capa (foto boa, horizontal, com rosto/cena —
   ela vira o fundo inteiro da capa); **4 chamadas** curtas (viram os selos da
   lateral da capa).
2. **Editorial** — carta ao leitor (150–250 palavras) costurando a semana:
   o que aconteceu, o que vem aí, um ponto de vista da casa.
3. **4 a 6 matérias da semana** — as melhores de `import/novas/` (da semana)
   e/ou as mais recentes de `import/materias.json`: usar `slug`, `img`, `cat`
   reais; chamada nova e `texto` reescrito em linguagem de revista (ver acima).
   Variar editorias.
4. **Na tela** — `{"tipo": "programas"}`: página automática com os programas
   do canal publicados nos últimos 8 dias, clicáveis direto para o YouTube.
   Incluir SEMPRE, depois das matérias. Não tem campos.
5. **1 página de citação** — a melhor frase REAL da semana (de matéria ou
   entrevista), com atribuição.
6. **1 exclusiva** (opcional, se houver material): análise ou panorama da
   semana escrito para a revista, no padrão profissional do FOYER
   (ver tools/REDACAO.md — nunca inventar fatos).
7. **Cartazes/patrocínio** — NUNCA criar: só o chefe sobe. Se já existirem
   páginas desses tipos na edição, preservá-las na ordem.
8. **Expediente** — última página, `{"tipo": "expediente"}`.

Ritmo bom: capa → editorial → matéria forte → variedade → Na tela →
citação como respiro → cartazes → expediente.

## Ao polir uma edição existente ("deixe incrível")

- Melhorar manchete, chamadas, chamadas de matérias e editorial (texto).
- Reordenar páginas para o ritmo acima.
- NUNCA remover páginas de cartaz/patrocínio nem trocar imagens que o chefe
  subiu. Nunca mudar `status`.
- Registrar no `historico` o que foi feito.

## Entrega

1. Gravar o JSON da edição e as imagens que tiver baixado.
2. `git add import/revista/ assets/uploads/` — e nada além disso.
3. Commit: `Revista: rascunho da edição N pela IA [skip ci]` e push na branch
   `claude/foyer-digital-redesign-14l2b6`.
4. A edição fica na Coxia (📖 Revista) esperando o chefe revisar e publicar.
