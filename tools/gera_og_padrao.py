#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a arte padrão de compartilhamento do site e os logos em tamanho de uso.

12/10/2026 (auditoria): a prévia de link das páginas sem foto própria (capa,
editorias, autores, institucionais) usava o banner de 1128x320, que o
WhatsApp, o Facebook e o X cortam ou mostram com faixas. A arte nova tem
1200x630 (1,91:1), feita só com o logo e as cores da casa, sem texto inventado.

Na mesma passada saem os logos no tamanho em que aparecem na tela: o do topo
da capa era um PNG de 518x480 exibido com até 200 px de altura, e o grande do
rodapé tinha 2000 px de largura para um espaço que no celular mede 350 px.

Uso:  python3 tools/gera_og_padrao.py   (os arquivos vão para assets/logo/)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, 'assets/logo')
VINHO, VINHO_ESC, OURO = (0x4E, 0x0F, 0x09), (0x38, 0x0A, 0x06), (0xCE, 0xB2, 0x6A)


def arte_padrao():
    w, h = 1200, 630
    base = Image.new('RGB', (w, h), VINHO)
    dr = ImageDraw.Draw(base)
    # cortina discreta nas laterais, como os placeholders de palco do site
    for x in list(range(0, 150, 50)) + list(range(w - 150, w, 50)):
        dr.rectangle([x + 10, 0, x + 34, h], fill=VINHO_ESC)
    # ribalta: o filete dourado embaixo
    dr.rectangle([0, h - 70, w, h - 64], fill=OURO)
    dr.rectangle([0, h - 64, w, h], fill=VINHO_ESC)
    logo = Image.open(os.path.join(LOGO, 'foyer-horizontal-gold.png')).convert('RGBA')
    lw = 840
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    y = (h - 70 - logo.height) // 2 - 24
    base.paste(logo, ((w - lw) // 2, y), logo)
    try:
        fonte = ImageFont.truetype(os.path.join(ROOT, 'tools/fonts/Archivo-Bold.ttf'), 26)
    except Exception:
        fonte = ImageFont.load_default()
    frase = 'TEATRO  ·  MÚSICA  ·  CULTURA'
    tw = dr.textlength(frase, font=fonte)
    dr.text(((w - tw) / 2, y + logo.height + 34), frase, font=fonte, fill=OURO)
    base.save(os.path.join(LOGO, 'foyer-og-1200x630.jpg'), 'JPEG', quality=88, optimize=True, progressive=True)


def _png_leve(im, nome):
    # PNG de paleta: medido em 12/10/2026, sai menor que WebP para um logo de
    # duas cores com transparência (8 KB contra 14 KB no tamanho do topo)
    im.quantize(256, method=Image.Quantize.FASTOCTREE).save(os.path.join(LOGO, nome), 'PNG', optimize=True)


def logos_em_uso():
    # topo da capa: altura máxima de 200 px no CSS (.logo-img), 1x e 2x
    st = Image.open(os.path.join(LOGO, 'foyer-stacked-gold.png')).convert('RGBA')
    for alt in (200, 400):
        im = st.resize((round(st.width * alt / st.height), alt), Image.LANCZOS)
        _png_leve(im, f'foyer-stacked-gold-{alt}.png')
    # rodapé grande: 94% da largura do rodapé
    hz = Image.open(os.path.join(LOGO, 'foyer-horizontal-gold.png')).convert('RGBA')
    for lar in (800, 1400):
        im = hz.resize((lar, round(hz.height * lar / hz.width)), Image.LANCZOS)
        _png_leve(im, f'foyer-horizontal-gold-{lar}.png')


if __name__ == '__main__':
    arte_padrao()
    logos_em_uso()
    print('assets/logo: arte padrão 1200x630 e logos em tamanho de uso')
