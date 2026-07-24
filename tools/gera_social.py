#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as artes de Instagram de uma matéria do FOYER (feed 1080x1350 e
stories 1080x1920) no formato clássico da casa: foto em tela cheia, arco
branco, FOYER.<EDITORIA> no topo e título em negrito com destaques dourados.

Uso:
  python3 tools/gera_social.py import/pauta/<slug>.json [outra.json ...]

- Destaques dourados: campo instagram.titulo com *trechos marcados* assim;
  sem o campo, o que estiver entre aspas vira dourado.
- A legenda: usa instagram.legenda se existir; senão monta do corpo
  (2 primeiros parágrafos + fecho padrão) e imprime na tela.
Saída: assets/social/<slug>-feed.jpg e <slug>-story.jpg
"""
import json, os, re, sys, unicodedata
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(ROOT, 'tools/fonts')
SAIDA = os.path.join(ROOT, 'assets/social')
OURO = (206, 178, 106)
BRANCO = (255, 255, 255)


def _fonte(nome, tam):
    return ImageFont.truetype(os.path.join(FONTES, nome), tam)


def _cover(img, w, h, foco=0.38):
    """Corta a foto para cobrir w x h, com viés para o terço superior."""
    iw, ih = img.size
    esc = max(w / iw, h / ih)
    img = img.resize((round(iw * esc), round(ih * esc)), Image.LANCZOS)
    iw, ih = img.size
    x = (iw - w) // 2
    y = max(0, min(ih - h, round((ih - h) * foco)))
    return img.crop((x, y, x + w, y + h))


def _gradiente(base, y0, y1, a0, a1):
    """Faixa vertical de preto com alfa interpolado."""
    faixa = Image.new('L', (1, y1 - y0))
    for i in range(y1 - y0):
        k = i / max(1, y1 - y0 - 1)
        faixa.putpixel((0, i), round(a0 + (a1 - a0) * k))
    faixa = faixa.resize((base.width, y1 - y0))
    preto = Image.new('RGB', (base.width, y1 - y0), (5, 3, 2))
    base.paste(preto, (0, y0), faixa)


def _tokens_titulo(pg):
    """[(palavra, dourada?)] a partir de instagram.titulo (*marcas*) ou aspas."""
    insta = pg.get('instagram') or {}
    t = insta.get('titulo') or pg.get('title', '')
    toks = []
    if '*' in t:
        for i, parte in enumerate(t.split('*')):
            for w in parte.split():
                toks.append((w, i % 2 == 1))
        return toks
    dentro = False
    for w in t.split():
        abre = ('“' in w or '"' in w) and not dentro
        if abre:
            dentro = True
        toks.append((w, dentro))
        if '”' in w or (w.count('"') and not abre) or (abre and w.count('"') == 2) or ('”' in w):
            dentro = False
        if abre and ('”' in w or w.rstrip(',.').endswith('"')):
            dentro = False
    return toks


def _desenha_titulo(dr, toks, x, y_base, larg, tam, entre=1.16):
    f = _fonte('Archivo-Bold.ttf', tam)
    esp = dr.textlength(' ', font=f)
    linhas, atual, cw = [], [], 0
    for w, ouro in toks:
        ww = dr.textlength(w, font=f)
        if atual and cw + ww > larg:
            linhas.append(atual)
            atual, cw = [], 0
        atual.append((w, ouro, ww))
        cw += ww + esp
    if atual:
        linhas.append(atual)
    alt_linha = round(tam * entre)
    y = y_base - alt_linha * len(linhas)
    for linha in linhas:
        cx = x
        for w, ouro, ww in linha:
            dr.text((cx, y), w, font=f, fill=OURO if ouro else BRANCO)
            cx += ww + esp
        y += alt_linha
    return len(linhas)


def _cabecalho(dr, base, cat, y=132):
    f_didone = _fonte('AbrilFatface-Regular.ttf', 84)
    f_sans = _fonte('Archivo-Bold.ttf', 56)
    x = 92
    dr.text((x, y), 'FOYER', font=f_didone, fill=BRANCO)
    lw = dr.textlength('FOYER', font=f_didone)
    sufixo = '.' + unicodedata.normalize('NFKD', cat or 'TEATRO').encode('ascii', 'ignore').decode().upper()
    dr.text((x + lw + 6, y + 26), sufixo, font=f_sans, fill=BRANCO)


def _arco(dr, w, y_ini=138, y_fim=470):
    """O arco branco da casa: entra reto da esquerda e mergulha à direita."""
    pontos = []
    p0, p1, p2 = (-60, y_ini + 14), (int(w * 0.66), y_ini - 26), (w + 40, y_fim)
    for i in range(81):
        t = i / 80
        px = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        py = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pontos.append((px, py))
    dr.line(pontos, fill=BRANCO, width=6, joint='curve')


def gerar(pg, formato='feed'):
    w, h = (1080, 1350) if formato == 'feed' else (1080, 1920)
    base = Image.new('RGB', (w, h), (10, 6, 5))
    caminho = os.path.join(ROOT, pg.get('img', ''))
    if pg.get('img') and os.path.exists(caminho):
        foto = Image.open(caminho).convert('RGB')
        base.paste(_cover(foto, w, h))
    dr = ImageDraw.Draw(base, 'RGB')
    _gradiente(base, 0, 340, 150, 0)
    _gradiente(base, h - 520, h, 0, 225)
    _arco(dr, w, y_ini=140 if formato == 'feed' else 190,
          y_fim=470 if formato == 'feed' else 560)
    _cabecalho(dr, base, pg.get('cat'), y=130 if formato == 'feed' else 176)
    toks = _tokens_titulo(pg)
    tam = 62 if formato == 'feed' else 66
    n = sum(len(w) for w, _ in toks)
    if n > 70:
        tam -= 6
    margem_baixo = 120 if formato == 'feed' else 260
    _desenha_titulo(dr, toks, 92, h - margem_baixo, w - 200, tam)
    if formato == 'story':
        f_mini = _fonte('Archivo-Bold.ttf', 34)
        dr.text((92, h - 190), 'Leia a matéria completa em foyer.digital', font=f_mini, fill=OURO)
    return base


def legenda_de(pg):
    insta = pg.get('instagram') or {}
    if insta.get('legenda'):
        return insta['legenda']
    corpo = pg.get('corpo', '')
    paras = [p.strip() for p in corpo.split('\n\n')
             if p.strip() and not p.startswith(('#', '>', 'img:', 'video:', 'galeria:', 'botao:', '*'))]
    paras = [re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', p).replace('**', '').replace('*', '') for p in paras]
    partes = paras[:2]
    cred = (pg.get('imgCredito') or 'Divulgação').replace('Foto: ', '')
    autor = pg.get('author', 'Redação Foyer')
    return ('\n\n'.join(partes)
            + '\n\nPara conferir a matéria completa, acesse o site: www.foyer.digital'
            + f'\n📷: {cred}'
            + f'\nPor {autor}')


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for arq in sys.argv[1:]:
        pg = json.load(open(arq))
        slug = pg['slug']
        for formato in ('feed', 'story'):
            img = gerar(pg, formato)
            destino = os.path.join(SAIDA, f'{slug}-{formato}.jpg')
            img.save(destino, quality=88)
            print('•', os.path.relpath(destino, ROOT))
        print('--- legenda ---')
        print(legenda_de(pg))
        print()


if __name__ == '__main__':
    main()
