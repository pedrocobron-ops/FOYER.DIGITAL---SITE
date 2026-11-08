# Guia: formato único dos dados (decidido em 08/11/2026)

Um formato para todas as fontes. Arquivos em `import/guia/`:

| arquivo | o que é | quem escreve |
|---|---|---|
| `brutos/<fonte>.json` | o que cada coletor trouxe na última coleta boa | `coleta_*.py` |
| `agenda.json` | tudo junto, só o que ainda vai acontecer, só fonte em dia | `junta.py` |
| `mudancas.json` | horário, preço ou temporada que mudou (últimas 300) | `junta.py` |
| `sondas.json` | fontes sem coletor: estão no ar? deixam entrar? | `sonda_fontes.py` |

## Regra da fonte por campo

Todo registro tem `origens`: a lista de onde os dados vieram.

```json
"origens": [
  {"fonte": "guiaoff", "url": "https://guiaoff.com.br/espetaculo/folego/", "coletado_em": "2026-11-08T17:27:00-03:00"},
  {"fonte": "guiaoff", "url": "https://guiaoff.com.br/guia/#teatro",     "coletado_em": "2026-11-08T17:27:00-03:00"}
]
```

Todo campo é `{"v": valor, "o": índice em origens}`. Campo sem origem não
existe. Quando algo foi deduzido (hoje, só o ano das datas do Guia OFF, que
escreve "dd/mm"), o campo leva `"obs"` dizendo o quê.

## Evento (o programa: peça, filme, show, exposição)

```json
{
  "id": "guiaoff-28540",              // fonte + id da fonte (ou título, se a fonte não tem id)
  "fonte": "guiaoff",                  // posto pelo junta.py
  "area":  {"v": "teatro", "o": 1},    // teatro | danca | infantil | eventos | cinema | musica | exposicao | literatura
  "titulo": {"v": "FÔLEGO", "o": 0},
  "categoria": {...},                   // categoria como a fonte chama (opcional)
  "link_fonte": {...},                  // página do programa na fonte
  "trecho": {...},                      // trecho CURTO da fonte (até 220 caracteres), nunca o texto todo
  "ficha": {...},                       // ficha técnica como a fonte escreve
  "tambem_em": ["cinemateca-..."],      // mesmo título achado em outra fonte
  "sessoes": [ ... ],
  "origens": [ ... ]
}
```

## Sessão (quando e onde)

Duas formas, conforme a fonte:
- **sessão exata** (calendários de cinema): `inicio` "2026-11-14T20:00", `fim` opcional;
- **temporada** (Guia OFF): `quando` em texto ("Sexta e sábado, 20h; domingo,
  18h"), `estreia`, `ate`, e `datas` quando a fonte lista dias ("Dias 12 e 13/11").

Demais campos, todos opcionais e todos com fonte: `lugar` (id da ficha do
lugar), `sala`, `atracao` (festivais), `preco` (texto como a fonte escreve),
`duracao_min`, `classificacao`, `ingresso` (só link de bilheteria), `site`,
`link`, `obs`, `texto_fonte` (a linha de serviço original, para conferência).

Sai do ar sozinha no dia seguinte ao `ate` (ou ao `inicio`, ou à última das
`datas` quando não há dia da semana fixo).

## Lugar (ficha)

```json
"teatro-sergio-cardoso": {
  "id": "teatro-sergio-cardoso",
  "nome": {...}, "endereco": {...}, "bairro": {...}, "telefone": {...},
  "endereco_texto": {...},   // quando o endereço não se deixa separar com segurança
  "cidade": {...}, "site": {...},
  "origens": [...]
}
```

Café, estacionamento, acessibilidade, metrô: só entram com fonte (site oficial
do lugar ou etiqueta do OpenStreetMap). Nada disso existe ainda; é a próxima
etapa das fichas. Ficha de lugar vinda de duas fontes: campo novo entra; campo
diferente fica como estava e vai para `divergencias` no agenda.json.

## Obra / filme (próxima etapa)

Para cinema: `obra` = filme, com `wikidata` (Q-id), título original, ano,
direção, país, duração, sempre de Wikidata/Wikipédia (livre, sem chave). O
evento de cinema aponta para a obra. Ainda não implementado: os títulos da
Cinemateca vêm em caixa alta e às vezes em sessão dupla, então a ligação com
o Wikidata precisa de conferência antes de entrar.

## Fonte quebrada

Se um coletor falha, `brutos/<fonte>.json` mantém a última coleta boa e marca
`ok: false` com o erro. Passados 3 dias sem coleta boa, o `junta.py` deixa de
publicar aquela fonte (`publicada: false`) e a página mostra o aviso.
