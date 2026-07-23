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

- **A matéria INTEIRA mora na revista.** O leitor puxa o corpo completo da
  matéria automaticamente (de import/corpo/) — a revista funciona sozinha,
  sem obrigar ninguém a ir ao site. O botão "Abrir esta matéria no site"
  aparece no fim como extra.
- O que a IA escreve PARA a revista: o `titulo` (pode ser mais autoral que o
  do site), a `chamada` (linha fina) e, opcionalmente, um `texto` curto que
  vira o **olho** da página (1 parágrafo de abertura em itálico). NUNCA usar
  `texto` para resumir a matéria: o corpo completo já entra sozinho.
- **Ritmo de folheio.** A revista deve ser gostosa de folhear: intercalar.
  Bom ritmo: editorial → 2 matérias fortes → Na tela → mais matérias →
  citação como respiro → cartazes → expediente. Nunca um bloco só de
  matérias iguais em sequência.
- **Nunca mentir.** Citações com atribuição REAL: só escrever "ao FOYER" se
  a frase foi dita ao FOYER (entrevista nossa). Se veio de release ou de
  outra publicação, dizer a origem verdadeira ou apenas quem disse.
- Padrão de escrita humana do FOYER vale aqui também (tools/REDACAO.md):
  travessão proibido, sem clichês de IA, fatos reais somente.
- **A imagem manda na capa.** A capa mostra a foto quase inteira: as
  chamadas entram sozinhas numa faixa na base, nunca sobre a imagem.
  Escolher foto forte e vertical-amigável (rostos na metade de cima).

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
  {"tipo": "materia", "slug": "slug-no-site", "cat": "Teatro", "img": "…", "titulo": "…", "chamada": "linha fina", "texto": "olho opcional (1 parágrafo) — o corpo completo entra sozinho"},
  {"tipo": "exclusiva", "titulo": "…", "texto": "…", "img": "…", "imgCredito": "Foto: …"},
  {"tipo": "programas"},
  {"tipo": "agenda"},
  {"tipo": "frase-celebre"},
  {"tipo": "citacao", "frase": "…", "autor": "…"},
  {"tipo": "cartaz", "img": "…", "legenda": "…", "link": "https://…"},
  {"tipo": "patrocinio", "img": "…", "legenda": "…", "link": "https://…"},
  {"tipo": "livre", "rotulo": "…", "titulo": "…", "texto": "…"},
  {"tipo": "expediente"}
 ],
 "historico": [{"quando": "ISO", "quem": "Redação IA (Claude)", "acao": "monta o rascunho da edição"}]
}
```

## A redação de agentes da revista (obrigatória na rodada semanal)

A edição NÃO é montada por um agente só. A rodada de quinta escala uma
redação completa de subagentes (ferramenta Task), em três ondas, com DOIS
PORTÕES DE QUALIDADE que reprovam e devolvem o trabalho:

**Onda 1 — Produção (em paralelo):**
1. **Editor de capa** — escolhe a matéria mais forte da semana, escreve
   manchete e as 4 chamadas, garante a foto de capa.
2. **Redatores de página** — um por matéria: título autoral, linha fina e
   olho opcional (o corpo entra sozinho, paginado pelo leitor).
3. **AGENDISTA SP** e **AGENDISTA RIO** — um por cidade: cada um pesquisa na
   web e escreve a SUA página "A semana em cartaz" (`{"tipo": "agenda",
   "cidade": "São Paulo"}` e `{"tipo": "agenda", "cidade": "Rio de
   Janeiro"}`), conteúdo EXCLUSIVO cobrindo de SEXTA a QUINTA (7 dias), 5 a
   7 itens por cidade, cada item com sessão CONFIRMADA na fonte e 1 frase
   de curadoria própria. NUNCA replicar os guias do site (cobrem só
   qui-dom): outra apuração, outro texto. Dia sem sessão confirmada na
   cidade se pula; nunca inventar.
4. **Editorialista** — a carta ao leitor da semana.

**Onda 2 — PORTÃO DE TEXTO (revisão final obrigatória):**
5. **Revisor** — relê TODA a edição pronta: travessão zero, clichês de IA,
   ortografia, atribuições de citação reais, links internos existentes
   (validar com ls), datas e nomes consistentes entre páginas. Reprova e
   corrige antes de seguir.
6. **Checador** — confere os SERVIÇOS contra as fontes (dia, horário,
   teatro, preço, canal de venda de cada item de agenda e de cada matéria).
   O que não confirmar, sai.

**Onda 3 — PORTÃO DE DESIGN (diagramação obrigatória):**
7. **Diagramador** — monta a edição de verdade e OLHA o resultado:
   a) grava o JSON como rascunho e roda `python3 tools/build_pages.py` com
      o status temporariamente em "publicada" numa cópia local (SEM commit)
      para gerar o leitor;
   b) sobe um servidor local (`python3 -m http.server 8077 &`), instala
      playwright-core se preciso (`npm i playwright-core`) e roda o auditor
      da casa: `node tools/checa_revista.js
      http://localhost:8077/revista-ed-<N>.html`;
   c) o auditor reprova ESTOURO (conteúdo passando da página), MUITO-VAZIA
      (página de matéria/agenda com menos de 55% de ocupação) e
      IMAGEM-QUEBRADA. Enquanto houver reprovação: ajustar (encurtar olho,
      trocar foto, reordenar, reduzir itens de agenda) e rodar de novo até
      o laudo sair `"problemas": []`;
   d) restaurar o status "rascunho" e descartar artefatos gerados
      (`git checkout -- .` nos html/xml gerados) antes da entrega.
8. **Chefe de fechamento** — confere os dois portões cumpridos, ordena o
   ritmo, registra o historico e faz o commit/push final.

## Receita de uma boa edição semanal

1. **Capa** — manchete forte tirada da melhor matéria da semana; usar a foto
   dessa matéria como imagem de capa (foto boa, horizontal, com rosto/cena —
   ela vira o fundo inteiro da capa); **4 chamadas** curtas (viram os selos da
   lateral da capa).
2. **Editorial** — carta ao leitor (150–250 palavras) costurando a semana:
   o que aconteceu, o que vem aí, um ponto de vista da casa.
3. **4 a 6 matérias da semana** — as melhores de `import/novas/` (da semana)
   e/ou as mais recentes de `import/materias.json`: usar `slug`, `img`, `cat`
   reais; chamada nova; o corpo completo entra sozinho. Variar editorias.
4. **Na tela** — `{"tipo": "programas"}`: página automática com o episódio
   mais novo de cada programa do canal (últimos 14 dias), clicável direto
   para o YouTube. Incluir SEMPRE, intercalada entre as matérias (depois da
   2ª ou 3ª). Não tem campos.
5. **A semana em cartaz** — `{"tipo": "agenda", "itens": [{"dia": "AAAA-MM-DD",
   "titulo": "…", "texto": "1 frase de curadoria", "local": "…", "cidade": "…",
   "link": "post-….html ou https://…"}]}`: a página EXCLUSIVA do agendista,
   7 itens (sexta a quinta), um destaque por dia com sessão confirmada.
   Incluir SEMPRE, depois das matérias. Sem "itens", o leitor cai numa lista
   automática de eventos das matérias (só como reserva, não é o padrão).
6. **Entre mestres** — `{"tipo": "frase-celebre"}`: página exclusiva com uma
   frase REAL e verificada de um grande nome das artes ou da filosofia
   (Shakespeare, Wilde, Nietzsche, Victor Hugo, Molière, Stanislavski,
   Suassuna, Nelson Rodrigues), rotativa por edição. Incluir SEMPRE. Sem
   campos (ou frase/autor/sobre manuais, DESDE QUE a citação seja real e
   com fonte, nunca inventada).
7. **1 página de citação** — a melhor frase REAL da semana (de matéria ou
   entrevista), com atribuição.
   (Opcional) **1 exclusiva**, se houver material: análise ou panorama da
   semana escrito para a revista, no padrão profissional do FOYER
   (ver tools/REDACAO.md — nunca inventar fatos).
8. **Cartazes/patrocínio** — NUNCA criar: só o chefe sobe. Se já existirem
   páginas desses tipos na edição, preservá-las na ordem.
9. **Expediente** — última página, `{"tipo": "expediente"}`.

Ritmo bom: capa → editorial → 2 matérias fortes → Na tela → mais matérias →
A semana em cartaz → citação como respiro → Entre mestres → cartazes →
expediente.

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
