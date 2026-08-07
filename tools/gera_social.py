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
OURO = (233, 203, 133)          # o dourado claro dos posts da casa (--gold-hi)
BRANCO = (255, 255, 255)
# 03/08/2026: a foto do feed vai SANGRADA, encostando nas quatro bordas.
# Havia uma moldura preta de 16px em volta dela, e no Instagram aquilo não
# lia como escolha de design: lia como imagem mal exportada, com tarja.


def _fonte(nome, tam):
    return ImageFont.truetype(os.path.join(FONTES, nome), tam)


def _fonte_titulo(tam):
    """A fonte dos títulos dos posts: PT Sans Bold."""
    return _fonte('PTSans-Bold.ttf', tam)


def _cover(img, w, h, foco=0.38):
    """Corta a foto para cobrir w x h.

    - foco número (jeito antigo): viés vertical, 0.38 = terço superior.
    - foco {'x':0..1,'y':0..1} (ajuste feito pelo Pedro na Coxia): ponto de
      interesse da foto; o corte centraliza nele o quanto der sem sair da
      borda. A prévia da Coxia usa exatamente esta conta — se mudar aqui,
      mude lá também (função focoParaPosicao).
    """
    iw, ih = img.size
    esc = max(w / iw, h / ih)
    img = img.resize((round(iw * esc), round(ih * esc)), Image.LANCZOS)
    iw, ih = img.size
    if isinstance(foco, dict):
        fx = min(max(float(foco.get('x', 0.5)), 0), 1)
        fy = min(max(float(foco.get('y', 0.5)), 0), 1)
        x = max(0, min(iw - w, round(fx * iw - w / 2)))
        y = max(0, min(ih - h, round(fy * ih - h / 2)))
    else:
        x = (iw - w) // 2
        y = max(0, min(ih - h, round((ih - h) * foco)))
    return img.crop((x, y, x + w, y + h))


def _carrega_focos():
    """Os ajustes de enquadramento feitos na Coxia: slug -> {'x','y'}."""
    try:
        with open(os.path.join(ROOT, 'import/social-foco.json')) as f:
            return json.load(f).get('focos', {})
    except (OSError, ValueError):
        return {}


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


def _arruma_toks(toks):
    """Cola pontuação solta na palavra anterior e troca aspas retas por curvas."""
    saida = []
    dentro = False
    for w, ouro in toks:
        novo = ''
        for c in w:
            if c == '"':
                novo += '”' if dentro else '“'
                dentro = not dentro
            else:
                novo += c
        w = novo
        if saida and w and w[0] in ',.;:!?…':
            aw, ao = saida[-1]
            saida[-1] = (aw + w, ao)
        else:
            saida.append((w, ouro))
    return saida


def _desenha_titulo(dr, toks, x, y_base, larg, tam, entre=1.14):
    toks = _arruma_toks(toks)
    f = _fonte_titulo(tam)
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
    """FOYER = a logo oficial da casa em branco + .EDITORIA (discreto, como nos posts)."""
    logo = Image.open(os.path.join(ROOT, 'assets/logo/foyer-horizontal-gold.png'))
    alt = 46
    esc = alt / logo.height
    logo = logo.resize((round(logo.width * esc), alt), Image.LANCZOS)
    x = 92
    base.paste(Image.new('RGB', logo.size, BRANCO), (x, y), logo.getchannel('A'))
    f_sans = _fonte('PTSans-Bold.ttf', 32)
    sufixo = '.' + (cat or 'Teatro').upper()
    dr.text((x + logo.width + 6, y + alt - 35), sufixo, font=f_sans, fill=BRANCO)


def gerar(pg, formato='feed'):
    if formato == 'story':
        return _gerar_story(pg)
    w, h = 1080, 1350
    base = Image.new('RGB', (w, h), (6, 4, 4))       # fundo, só aparece sem foto
    caminho = os.path.join(ROOT, pg.get('img', ''))
    if pg.get('img') and os.path.exists(caminho):
        foto = Image.open(caminho).convert('RGB')
        base.paste(_cover(foto, w, h, pg.get('foco') or 0.38), (0, 0))  # sangra nas quatro bordas
    dr = ImageDraw.Draw(base, 'RGB')
    _gradiente(base, 0, 320, 130, 0)
    _gradiente(base, h - 560, h, 0, 235)
    _cabecalho(dr, base, pg.get('cat'), y=150)
    toks = _tokens_titulo(pg)
    tam = 54
    n = sum(len(w) for w, _ in toks)
    if n > 70:
        tam = 50
    if n > 95:
        tam = 46
    _desenha_titulo(dr, toks, 92, h - 128, w - 200, tam)
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
    _cabecalho(dr, base, pg.get('cat'), y=196)
    if foto is not None:
        larg_card = 940
        alt_card = min(round(larg_card * foto.height / foto.width), 1000)
        card = _cover(foto, larg_card, alt_card, foco=pg.get('foco') or 0.3) if \
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
    tam = 56
    if sum(len(t) for t, _ in toks) > 80:
        tam -= 5
    f = _fonte_titulo(tam)
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
    f_mini = _fonte_titulo(34)
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


def _assinatura(pg):
    """O que, mudando, exige refazer a arte: foto, enquadramento, título, editoria."""
    insta = pg.get('instagram') or {}
    return {'img': pg.get('img', ''), 'foco': pg.get('foco') or None,
            'titulo': insta.get('titulo') or pg.get('title', ''),
            'cat': pg.get('cat', '')}


def pendentes():
    """Modo do robô: gera arte para toda matéria da Coxia que ainda não tem
    (as escritas à mão entram aqui) e refaz as que mudaram de foto, título ou
    enquadramento. O registro.json guarda com que ingredientes cada arte foi
    feita, para só refazer o que de fato mudou."""
    os.makedirs(SAIDA, exist_ok=True)
    reg_arq = os.path.join(SAIDA, 'registro.json')
    try:
        with open(reg_arq) as f:
            registro = json.load(f)
    except (OSError, ValueError):
        registro = {}
    focos = _carrega_focos()

    novas_dir = os.path.join(ROOT, 'import/novas')
    pgs = {}
    if os.path.isdir(novas_dir):
        for nome in sorted(os.listdir(novas_dir)):
            if nome.endswith('.json'):
                try:
                    pg = json.load(open(os.path.join(novas_dir, nome)))
                except ValueError:
                    continue
                if pg.get('slug'):
                    pgs[pg['slug']] = pg
    # ajuste feito numa matéria do acervo antigo: busca no materias.json
    faltam = set(focos) - set(pgs)
    if faltam:
        try:
            for m in json.load(open(os.path.join(ROOT, 'import/materias.json'))):
                if m.get('slug') in faltam:
                    pgs[m['slug']] = m
        except (OSError, ValueError):
            pass

    feitas, feitas_reg = 0, False
    for slug, pg in pgs.items():
        if slug in focos:
            pg['foco'] = focos[slug]
        cam = os.path.join(ROOT, pg.get('img', ''))
        if not pg.get('img') or not os.path.exists(cam):
            continue
        sig = _assinatura(pg)
        tem_arte = all(os.path.exists(os.path.join(SAIDA, f'{slug}-{f}.jpg'))
                       for f in ('feed', 'story'))
        if tem_arte and slug not in registro:
            # arte feita antes do registro existir: adota como está, sem refazer
            registro[slug] = sig
            feitas_reg = True
            continue
        if tem_arte and registro.get(slug) == sig:
            continue
        for formato in ('feed', 'story'):
            gerar(pg, formato).save(os.path.join(SAIDA, f'{slug}-{formato}.jpg'), quality=88)
        registro[slug] = sig
        feitas += 1
        print('• arte refeita:', slug)
    if feitas or feitas_reg:
        with open(reg_arq, 'w') as f:
            json.dump(registro, f, ensure_ascii=False, indent=1)
    print(f'{feitas} matéria(s) com arte nova.')


def main():
    if '--pendentes' in sys.argv[1:]:
        return pendentes()
    os.makedirs(SAIDA, exist_ok=True)
    focos = _carrega_focos()
    for arq in sys.argv[1:]:
        pg = json.load(open(arq))
        slug = pg['slug']
        if slug in focos and not pg.get('foco'):
            pg['foco'] = focos[slug]
        for formato in ('feed', 'story'):
            img = gerar(pg, formato)
            destino = os.path.join(SAIDA, f'{slug}-{formato}.jpg')
            img.save(destino, quality=88)
            print('•', os.path.relpath(destino, ROOT))
        print('--- legenda ---')
        print(legenda_de(pg))
        arrobas = (pg.get('instagram') or {}).get('arrobas') or []
        if arrobas:
            print('--- perfis para marcar ---')
            for a in arrobas:
                if a.get('arroba'):
                    marca = '' if a.get('confirmado', True) else '  (a confirmar)'
                    print(f"  {a['arroba']}  {a.get('nome', '')}{marca}")
        print()


if __name__ == '__main__':
    main()
