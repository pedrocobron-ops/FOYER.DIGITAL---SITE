#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O F do FOYER como selo da notificação, no lugar do sino do Android.

POR QUE O SINO APARECIA. Na barra de status o Android NÃO usa as cores do
desenho: ele joga fora vermelho, verde e azul e fica só com o CANAL ALFA,
pintando de branco tudo o que for opaco. O selo apontado era o pwa-192.png,
que é um quadrado vinho inteiro, sem transparência nenhuma: pelo critério do
Android aquilo é um retângulo cheio, e ele descarta e põe o sino padrão.

O selo certo é uma SILHUETA: a letra opaca e todo o resto transparente.

Sai em 96x96 (o tamanho que o Android pede para o selo, xxhdpi) e a letra
ocupa uns 70% do quadro, com folga em volta — o sistema recorta o selo num
círculo, e letra encostada na borda perde as pontas.
"""
from PIL import Image, ImageDraw, ImageFont

FONTE = 'tools/fonts/AbrilFatface-Regular.ttf'
SAIDA = 'assets/logo/badge-foyer-96.png'
LADO = 96

def desenha(letra='F', lado=LADO, ocupa=0.70):
    # mede a letra grande e reduz depois: assim a curva da Abril não serrilha
    grande = lado * 4
    im = Image.new('L', (grande, grande), 0)      # tons de cinza: 0 = transparente
    d = ImageDraw.Draw(im)
    # acha o corpo de fonte que faz a letra ocupar a fatia pedida
    corpo = grande
    while corpo > 8:
        f = ImageFont.truetype(FONTE, corpo)
        cx0, cy0, cx1, cy1 = d.textbbox((0, 0), letra, font=f)
        if max(cx1 - cx0, cy1 - cy0) <= grande * ocupa:
            break
        corpo = int(corpo * 0.92)
    f = ImageFont.truetype(FONTE, corpo)
    x0, y0, x1, y1 = d.textbbox((0, 0), letra, font=f)
    # centraliza pela caixa REAL da letra, não pela linha de base
    d.text(((grande - (x1 - x0)) / 2 - x0, (grande - (y1 - y0)) / 2 - y0),
           letra, font=f, fill=255)
    im = im.resize((lado, lado), Image.LANCZOS)
    # branco em toda a chapa, e o alfa da letra decidindo o que aparece
    branco = Image.new('L', (lado, lado), 255)
    return Image.merge('RGBA', (branco, branco, branco, im))

selo = desenha()
selo.save(SAIDA)

a = selo.getchannel('A')
mn, mx = a.getextrema()
opacos = sum(1 for p in a.getdata() if p > 200)
print(f'{SAIDA}: {selo.size[0]}x{selo.size[1]}, alfa de {mn} a {mx}, '
      f'{opacos} pontos opacos ({opacos * 100 // (LADO * LADO)}% do quadro)')
if mn != 0:
    raise SystemExit('ERRO: o selo não tem fundo transparente, o Android vai recusar')
if not (10 <= opacos * 100 // (LADO * LADO) <= 45):
    print('AVISO: a letra pode estar grande ou pequena demais para a barra de status')
