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
    dentro, tem_ouro = False, False
    for w in t.split():
        abre = ('“' in w or '"' in w) and not dentro
        if abre:
            dentro = True
        toks.append((w, dentro))
        if dentro:
            tem_ouro = True
        if '”' in w or (w.count('"') and not abre) or (abre and w.count('"') == 2):
            dentro = False
        if abre and ('”' in w or w.rstrip(',.').endswith('"')):
            dentro = False
    if not tem_ouro:
        # sempre há um destaque: a maior sequência de nomes próprios do título
        palavras = [w for w, _ in toks]
        MIUDAS = {'A', 'O', 'As', 'Os', 'Um', 'Uma', 'De', 'Do', 'Da', 'Dos', 'Das',
                  'E', 'Em', 'No', 'Na', 'Nos', 'Nas', 'Com', 'Por', 'Para', 'Que'}
        melhor, atual = (0, 0), None
        for i, w in enumerate(palavras):
            limpo = w.strip('“”"\'.,:;!?')
            proprio = limpo[:1].isupper() and (i > 0) and (limpo not in MIUDAS or atual is not None)
            if proprio and limpo not in MIUDAS or (atual is not None and limpo in MIUDAS
                    and i + 1 < len(palavras) and palavras[i + 1].strip('“”"\'.,:;!?')[:1].isupper()
                    and palavras[i + 1].strip('“”"\'.,:;!?') not in MIUDAS):
                if atual is None:
                    atual = i
            else:
                if atual is not None and i - atual > melhor[1] - melhor[0]:
                    melhor = (atual, i)
                atual = None
        if atual is not None and len(palavras) - atual > melhor[1] - melhor[0]:
            melhor = (atual, len(palavras))
        if melhor[1] > melhor[0]:
            toks = [(w, melhor[0] <= i < melhor[1]) for i, (w, _) in enumerate(toks)]
        else:
            toks = [(w, i < 2) for i, (w, _) in enumerate(toks)]
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
    if formato == 'story':
        return _gerar_story(pg)
    w, h = 1080, 1350
    base = Image.new('RGB', (w, h), (10, 6, 5))
    caminho = os.path.join(ROOT, pg.get('img', ''))
    if pg.get('img') and os.path.exists(caminho):
        foto = Image.open(caminho).convert('RGB')
        base.paste(_cover(foto, w, h))
    dr = ImageDraw.Draw(base, 'RGB')
    _gradiente(base, 0, 340, 150, 0)
    _gradiente(base, h - 520, h, 0, 225)
    _arco(dr, w, y_ini=140, y_fim=470)
    _cabecalho(dr, base, pg.get('cat'), y=130)
    toks = _tokens_titulo(pg)
    tam = 52
    n = sum(len(w) for w, _ in toks)
    if n > 80:
        tam -= 5
    _desenha_titulo(dr, toks, 92, h - 120, w - 200, tam)
    return base


def _gerar_story(pg):
    """Stories 1080x1920: a foto entra INTEIRA, emoldurada, sobre um fundo
    feito dela mesma desfocada (nada de esticar a imagem)."""
    w, h = 1080, 1920
    base = Image.new('RGB', (w, h), (14, 8, 6))
    caminho = os.path.join(ROOT, pg.get('img', ''))
    foto = None
    if pg.get('img') and os.path.exists(caminho):
        foto = Image.open(caminho).convert('RGB')
        fundo = _cover(foto, w, h, foco=0.5).filter(ImageFilter.GaussianBlur(46))
        escuro = Image.new('RGB', (w, h), (10, 5, 4))
        base = Image.blend(fundo, escuro, 0.55)
    dr = ImageDraw.Draw(base, 'RGB')
    _arco(dr, w, y_ini=196, y_fim=560)
    _cabecalho(dr, base, pg.get('cat'), y=182)
    if foto is not None:
        larg_card = 940
        alt_card = min(round(larg_card * foto.height / foto.width), 1000)
        card = _cover(foto, larg_card, alt_card, foco=0.3) if \
            round(larg_card * foto.height / foto.width) > alt_card else \
            foto.resize((larg_card, round(larg_card * foto.height / foto.width)), Image.LANCZOS)
        x0 = (w - larg_card) // 2
        y0 = 420
        dr.rectangle((x0 - 5, y0 - 5, x0 + larg_card + 5, y0 + card.height + 5),
                     outline=OURO, width=4)
        base.paste(card, (x0, y0))
        y_texto_topo = y0 + card.height + 90
    else:
        y_texto_topo = 760
    toks = _tokens_titulo(pg)
    tam = 54
    if sum(len(t) for t, _ in toks) > 80:
        tam -= 5
    f = _fonte('Archivo-Bold.ttf', tam)
    # desenha do topo do bloco (calcula altura primeiro numa passada seca)
    dr2 = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    esp = dr2.textlength(' ', font=f)
    larg = w - 200
    linhas, atual, cw = 1, [], 0
    for t, _ in toks:
        tw = dr2.textlength(t, font=f)
        if atual and cw + tw > larg:
            linhas += 1
            atual, cw = [], 0
        atual.append(t)
        cw += tw + esp
    alt_bloco = round(tam * 1.16) * linhas
    _desenha_titulo(dr, toks, 92, min(y_texto_topo + alt_bloco, h - 250), larg, tam)
    f_mini = _fonte('Archivo-Bold.ttf', 34)
    dr.text((92, h - 170), 'Leia a matéria completa em foyer.digital', font=f_mini, fill=OURO)
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
