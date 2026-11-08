# Guia do FOYER: relatório da primeira entrega (08/11/2026)

Para o Pedro. Curto e sem jargão.

## O que ficou pronto

1. **Testei as fontes uma a uma.** O resultado completo está no BRIEFING
   (seção 3). Resumo abaixo.
2. **Um formato único** para tudo: cada informação guarda de onde veio e
   quando foi pega. Se não tem fonte, não aparece.
3. **Dois coletores funcionando**: Guia OFF (teatro, dança e infantil) e
   Cinemateca Brasileira (cinema).
4. **Uma rotina diária no GitHub** (de graça, não gasta seus créditos): todo
   dia às 3h17 da manhã ela busca a agenda, tira o que já acabou, anota o que
   mudou de horário ou preço e republica.
5. **Uma página escondida** em foyer.digital/guia/ para conferir os dados.
   Não aparece no Google, no menu nem no mapa do site. Cada dado tem uma
   setinha (↗) que leva à fonte.

Hoje a página mostra cerca de 190 programas em cartaz: uns 150 de teatro,
dança e infantil, e uns 30 filmes e debates da Cinemateca.

## O que dá para ter com dado público

- **Teatro**: muito bom. O Guia OFF traz quase tudo: lugar, endereço, bairro,
  dias, horário, preço, duração, classificação, até quando fica, ficha
  técnica e, em cerca de metade, o link do ingresso.
- **Cinema**: bom onde o próprio cinema publica a grade aberta (Cinemateca).
  Para as outras salas é preciso ler o site de cada uma.
- **Sesc**: dá, lendo as páginas públicas de cada atividade. É o próximo.
- **Museus e exposições**: dá, site por site (MASP, Pinacoteca, MAM, Museu da
  Língua Portuguesa...). Exposição muda pouco, então é trabalho de uma vez.
- **"Como chegar"**: link de rota do Google Maps já funciona na página.

## O que não dá (por enquanto)

- **SP Cultura, da Prefeitura**: o servidor recusou a conexão. Deixei um
  teste automático diário de dentro do GitHub; se abrir, entra.
- **Sesc pela "porta dos fundos"** (a lista de atividades em formato de
  dados): o Sesc bloqueia robôs ali de propósito. Respeitei. Vamos pela
  página pública, que é liberada.
- **IMS**: a lista deles não diz se o evento é em São Paulo, no Rio ou em
  Poços de Caldas, e o preço vem errado. Pela regra de ouro, ficou de fora.
- **Preço da Cinemateca**: o site não informa na grade. O guia não inventa.
- **Café, estacionamento, acessibilidade**: só entram quando o site oficial
  do lugar disser. Ainda não comecei as fichas dos lugares.

## Uma decisão sua

O Guia OFF deixa ler e listar com link para eles, mas pede que o conteúdo
não seja usado para treinar inteligência artificial. Estamos dentro disso:
o coletor é um programa comum, mostra trecho curto e manda o leitor para o
site deles. Mesmo assim, **antes de abrir o guia ao público, recomendo
conversar com o Guia OFF** (avisar ou propor parceria): é o trabalho
editorial deles que sustenta a parte de teatro.

## Propostas de nome

1. **Deixa**: no teatro, a deixa é a fala que dá a vez de entrar em cena. "O
   FOYER te dá a deixa." Curto, de teatro e de cinema.
2. **Plateia**: o lugar de quem assiste. Conversa com FOYER (o hall antes da
   plateia).
3. **Bússola**: diz o que o guia faz: aponta para onde ir.
4. **Programa**: o programa da peça e "qual é o programa hoje?".
5. **Achei**: o que a pessoa sente quando o guia acerta.

Minha preferida: **Deixa**.

## Próximos passos que proponho

1. Coletor do Sesc (páginas públicas, só as que mudaram desde ontem).
2. Fichas dos 30 lugares que mais aparecem, com metrô mais perto.
3. Museus e exposições, começando por MASP, Pinacoteca e Museu da Língua.
4. Mais cinemas (Reserva Cultural, Belas Artes, Itaú, CineSesc).

Tudo isso continua sem rotina do Claude ligada: nada foi agendado que gaste
seus créditos.
