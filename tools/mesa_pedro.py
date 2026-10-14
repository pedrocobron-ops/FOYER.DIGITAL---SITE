#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A mesa do Pedro: o braço do manual tools/PEDRO.md.

Matérias assinadas por Pedro Amaral, escritas nesta conversa do Claude,
entregues a ele aqui e publicadas no site só depois que ele aprova e marca a
hora (ordem dele, 14/10/2026).

REGRA CANÔNICA (ordem do Pedro, 14/10/2026): NADA VAI AO AR SEM O PEDRO
AUTORIZAR NESTA CONVERSA E DIZER A HORA. A rodada escreve, guarda o rascunho
em import/mesa-pedro/ (fica no repositório, nunca no site) e entrega aqui.
Publicar exige --ok, que só se usa depois da autorização dele, e uma hora.
Nunca duas matérias juntas: o script recusa publicar a menos de ESPACO_MIN
minutos de outra matéria dele.

Uso:
  python3 tools/mesa_pedro.py capa --slug SLUG (--url URL | --commons "File:X.jpg" | --arte N) [--foco auto|moldura|alto|centro|baixo]
  python3 tools/mesa_pedro.py confere PACOTE.json [...] [--rascunho]
  python3 tools/mesa_pedro.py ja-saiu "palavras chave"
  python3 tools/mesa_pedro.py guarda PACOTE.json [...]            # rascunho na mesa, aguardando o Pedro
  python3 tools/mesa_pedro.py horarios [--n 4]                     # próximos horários livres do relógio da casa
  python3 tools/mesa_pedro.py proximo-7h [--n 5]                   # a fila das frias
  python3 tools/mesa_pedro.py publica SLUG --ok --em "15/10 09:00"  # só depois da autorização do Pedro
  python3 tools/mesa_pedro.py publica SLUG [...] --ok --proximo-7h  # frias aprovadas, uma por dia
  python3 tools/mesa_pedro.py descarta SLUG [...] --motivo "..."   # o Pedro recusou
  python3 tools/mesa_pedro.py remove SLUG --motivo "..."           # tira do ar

A cópia de produção: o site é montado a partir da branch PRODUCAO. Se a pasta
atual já está nela, é ela. Senão, o script mantém um worktree dessa branch em
../FOYER-PRODUCAO (ou em $FOYER_PRODUCAO) e publica por ele. A branch de
desenvolvimento nunca recebe matéria.
"""
import argparse
import glob
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCAO = 'claude/foyer-digital-redesign-14l2b6'
BASE_URL = 'https://foyer.digital'
AUTOR = 'Pedro Amaral'
ORIGEM = 'mesa-pedro'
MESA = 'import/mesa-pedro'           # os rascunhos aguardando o Pedro (nunca vão ao site)
ESPACO_MIN = 60                      # minutos mínimos entre duas matérias dele
RELOGIO = (7, 9, 12, 15, 18, 20)     # as horas cheias da casa, em Brasília
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/128.0 Safari/537.36 FOYER-mesa/1.0 (+https://www.foyer.digital)')
COAUTOR = 'Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>'

CATS = {'Teatro', 'Teatro Musical', 'Notícia', 'Cinema', 'Streaming', 'Música', 'Show',
        'Dança', 'Exposições', 'Literatura', 'Televisão', 'Audições', 'Edital', 'Festa',
        'Programa', 'Guia', 'Bastidores', 'Entenda', 'Memória'}
CATS_SO_SECUNDARIA = {'Em Cartaz'}

# porte: (piso, teto de palavras, mínimo e máximo de intertítulos).
# Régua de 14/10/2026, com base no que o mercado produz (medido): notícia
# cultural de 230 a 520 palavras (Omelete, CNN Brasil, Deadline, Exame),
# análise de 600 a 950 (Playbill, Agência Brasil, Gazeta do Povo), entrevista
# e perfil acima de 2.000 (CNN Brasil). O FOYER promete o tratamento que o
# mercado não faz, então a quente fica acima da notícia do mercado e a
# reportagem acima da análise dele. Piso é de substância: encher é proibido.
PORTES = {
    'nota':       (250, 400, 0, 0),
    'quente':     (600, 900, 1, 3),
    'contexto':   (1000, 1500, 3, 5),
    'perfil':     (1200, 2000, 3, 6),
    'resposta':   (700, 1000, 2, 4),
    'explicador': (1000, 1500, 3, 5),
    'lista':      (1200, 1800, 7, 12),
}
PORTES_FRIOS = {'resposta', 'lista', 'explicador'}
# apuração mínima (URLs lidas) por porte
APURACAO_MIN = {'nota': 2, 'quente': 4, 'contexto': 6, 'perfil': 6, 'resposta': 4, 'explicador': 5, 'lista': 5}
# movimentos do repertório do Pedro: são dele, não são fôrma. No máximo uma
# vez por semana cada um, somando todas as matérias dele.
REPERTORIO = ['conta desta redação', 'vale ficar de olho', 'vale olhar']

AGENCIAS = ['getty', 'reuters', 'afp', 'folhapress', 'associated press', 'shutterstock',
            'istock', 'alamy', 'estadão conteúdo', 'estadao conteudo', 'epa images', 'zuma press']

FORMULAS = [
    r'\bnão é (?:um|uma|o|a)?\s*\w+, (?:é|mas) ', r'\bmais do que (?:um|uma)?\s*\w+, (?:é|são) ',
    r'\bverdadeir[oa]s? \w+', r'\bnão é (?:um )?detalhe\b', r'\bprova de que\b', r'\bé aí que entra\b',
    r'\bo resultado\?', r'\bvale lembrar\b', r'\bvale destacar\b', r'\bvale ressaltar\b',
    r'\bé importante (?:ressaltar|destacar|lembrar)\b', r'\bnesse sentido\b', r'\bneste sentido\b',
    r'\bnesse contexto\b', r'\bneste contexto\b', r'\bem suma\b', r'\bem resumo\b', r'\bpor fim\b',
    r'\bseja \w+, seja \w+', r'\bnão por acaso\b', r'\blonge de ser\b', r'\buma espécie de\b',
    r'\bem meio a\b', r'\bem um cenário\b', r'\bnum cenário\b', r'\bcom o avanço d[aeo]s?\b',
    r'\bespecialistas (?:afirmam|dizem|apontam|alertam|explicam)\b', r'\bao foyer\b',
]
CLICHES = ['imperdível', 'vibrante', 'emocionante', 'icônic', 'mergulh', 'celebra', 'promete emocionar',
           'promete encantar', 'experiência única', 'sucesso absoluto', 'vem conquistando',
           'não poderia ser diferente']
RESUMO_FINAL = r'^(?:assim|dessa forma|desse modo|portanto|em suma|em resumo|por fim|ou seja)\b'
TEMPO_NO_TITULO = r'\b(?:hoje|ontem|amanhã|nest[ae] (?:segunda|terça|quarta|quinta|sexta|sábado|domingo|semana|manhã|tarde|noite))\b'

LICENCAS_OK = re.compile(r'^(cc0|public domain|pd[- ]|cc[- ]by(?:[- ]sa)?(?:[- ]\d(?:\.\d)?)?|attribution)', re.I)
LICENCAS_NAO = re.compile(r'\b(nc|nd|non[- ]?commercial|no[- ]?deriv|fair use|non-free|copyright)\b', re.I)

TAMANHOS_THUMB = (1920, 1280, 960, 500)   # larguras padrão do Wikimedia (mediawiki.org/wiki/Common_thumbnail_sizes); fora delas o servidor responde 400 ou 429


def _thumb_padrao(url_original, largura):
    """A miniatura no maior tamanho padrão menor que a largura original: o
    Wikimedia limita quem baixa o original e pede as miniaturas listadas em
    https://w.wiki/GHai. Vale para JPG e PNG; outros formatos vão no original."""
    # a API devolve o original com ?utm_source=... no fim: a consulta sai antes de casar
    url_original = (url_original or '').split('?')[0]
    m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/commons)/([0-9a-f])/([0-9a-f]{2})/([^/]+\.(?:jpe?g|png|JPE?G|PNG))$', url_original)
    if not m or not largura:
        return url_original
    for t in TAMANHOS_THUMB:
        # 1920 só quando a original é bem maior; abaixo disso, 1280 é a mais segura
        if t < largura:
            return f'{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{m.group(4)}/{t}px-{m.group(4)}'
    return url_original


ARTES = {1: 'arte-1-refletor', 2: 'arte-2-cortina', 3: 'arte-3-plateia',
         4: 'arte-4-arena', 5: 'arte-5-urdimento', 6: 'arte-6-degraus'}
ARTES_LEGENDA = {1: 'Arte da identidade do FOYER: o ator sob o refletor',
                 2: 'Arte da identidade do FOYER: a cortina e a ribalta',
                 3: 'Arte da identidade do FOYER: alguém na plateia',
                 4: 'Arte da identidade do FOYER: o teatro de arena',
                 5: 'Arte da identidade do FOYER: as cordas da coxia',
                 6: 'Arte da identidade do FOYER: a subida ao palco'}


# ---------------------------------------------------------------- utilidades

def _git(cwd, *args, check=True, quiet=False):
    r = subprocess.run(['git', '-C', cwd] + list(args), text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: {r.stdout.strip()}')
    if not quiet and r.stdout.strip():
        print(r.stdout.strip())
    return r


def _branch_atual(cwd):
    r = subprocess.run(['git', '-C', cwd, 'rev-parse', '--abbrev-ref', 'HEAD'],
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return r.stdout.strip()


def producao(atualiza=False):
    """A pasta cuja branch é a de produção. Cria o worktree se preciso."""
    if _branch_atual(ROOT) == PRODUCAO:
        pasta = ROOT
    else:
        pasta = os.environ.get('FOYER_PRODUCAO') or os.path.join(os.path.dirname(ROOT), 'FOYER-PRODUCAO')
        if not os.path.isdir(os.path.join(pasta, '.git')) and not os.path.isfile(os.path.join(pasta, '.git')):
            _git(ROOT, 'fetch', 'origin', PRODUCAO, quiet=True)
            # worktree numa branch local com o mesmo nome, seguindo a remota
            r = subprocess.run(['git', '-C', ROOT, 'show-ref', '--verify', '--quiet', f'refs/heads/{PRODUCAO}'])
            if r.returncode == 0:
                _git(ROOT, 'worktree', 'add', pasta, PRODUCAO, quiet=True)
            else:
                _git(ROOT, 'worktree', 'add', '-b', PRODUCAO, pasta, f'origin/{PRODUCAO}', quiet=True)
            _git(pasta, 'branch', f'--set-upstream-to=origin/{PRODUCAO}', PRODUCAO, quiet=True)
        if _branch_atual(pasta) != PRODUCAO:
            raise RuntimeError(f'{pasta} não está em {PRODUCAO}; resolva à mão')
    if atualiza:
        _git(pasta, 'fetch', 'origin', PRODUCAO, quiet=True)
        r = _git(pasta, 'rebase', f'origin/{PRODUCAO}', check=False, quiet=True)
        if r.returncode != 0:
            _git(pasta, 'rebase', '--abort', check=False, quiet=True)
            raise RuntimeError('a cópia de produção divergiu e o rebase falhou: ' + r.stdout.strip())
    return pasta


def _agora():
    return datetime.now(timezone.utc)


def _iso_ms(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def _brt(dt):
    try:
        from zoneinfo import ZoneInfo
        return dt.astimezone(ZoneInfo('America/Sao_Paulo'))
    except Exception:
        return dt.astimezone(timezone(timedelta(hours=-3)))


def _sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).lower()


def _le_json(c):
    with open(c, encoding='utf-8') as f:
        return json.load(f)


def _grava_json(c, d):
    with open(c, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def _slugs_acervo(pasta, exceto=None):
    """Slugs do acervo e da fila. `exceto` é o arquivo que está sendo
    auditado: quando ele já mora em import/novas, não conta contra si mesmo."""
    s = set()
    try:
        for m in _le_json(os.path.join(pasta, 'import/materias.json')):
            if m.get('slug'):
                s.add(m['slug'])
    except Exception:
        pass
    ex = os.path.abspath(exceto) if exceto else None
    for f in glob.glob(os.path.join(pasta, 'import/novas/*.json')):
        if ex and os.path.abspath(f) == ex:
            continue
        s.add(os.path.basename(f)[:-5])
    return s


def _novas(pasta):
    out = []
    for f in sorted(glob.glob(os.path.join(pasta, 'import/novas/*.json'))):
        try:
            d = _le_json(f)
            d['_arquivo'] = f
            out.append(d)
        except Exception:
            pass
    return out


def _abre(url, accept='*/*', tentativas=6):
    """GET com User-Agent de navegador e paciência: 429 e 503 esperam o
    retry-after (até 20 s) e tentam de novo. Devolve (bytes, content-type)."""
    import urllib.error
    import urllib.request
    import random
    espera = 5
    for t in range(tentativas):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept,
                                                   'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get('Content-Type', '')
        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 502) and t < tentativas - 1:
                try:
                    espera = max(espera, int(e.headers.get('Retry-After', 0)))
                except Exception:
                    pass
                espera = min(espera, 45) + random.randint(1, 6)
                print(f'  ({e.code} em {url[:60]}; esperando {espera}s)', file=sys.stderr)
                time.sleep(espera)
                espera = min(espera * 2, 45)
                continue
            raise
    raise RuntimeError('sem resposta')


def _baixa(url, destino=None):
    dados, tipo = _abre(url, accept='image/*,*/*;q=0.8')
    if destino:
        with open(destino, 'wb') as f:
            f.write(dados)
    return dados, tipo


# --------------------------------------------------------------------- capa

def _corta_16_9(im, foco='alto'):
    """Capa exata em 16:9. Foto em pé ou quase quadrada: preserva o alto, onde
    ficam os rostos. Foto deitada: recorta pelo foco pedido."""
    w, h = im.size
    alvo_h = round(w * 9 / 16)
    if alvo_h <= h:
        sobra = h - alvo_h
        if h > w * 0.85:          # em pé: terço superior (regra da Coxia)
            y = min(round(h * 0.06), sobra)
        elif foco == 'centro':
            y = sobra // 2
        elif foco == 'baixo':
            y = sobra
        else:                     # alto: um quarto da sobra, para não decapitar
            y = sobra // 4
        return im.crop((0, y, w, y + alvo_h))
    alvo_w = round(h * 16 / 9)    # mais larga que 16:9: corta as laterais pelo centro
    x = (w - alvo_w) // 2
    return im.crop((x, 0, x + alvo_w, h))


def _moldura_16_9(im):
    """Foto em pé inteira sobre um fundo 16:9 feito dela mesma, desfocado e
    escurecido. É o `contain` que a casa permite (imagem inteira, com sobra),
    e evita decapitar retrato fechado, que o corte pelo topo faz."""
    from PIL import Image, ImageEnhance, ImageFilter
    W = 1600
    H = 900
    fundo = im.convert('RGB')
    esc = max(W / fundo.width, H / fundo.height)
    fundo = fundo.resize((round(fundo.width * esc), round(fundo.height * esc)), Image.LANCZOS)
    x, y = (fundo.width - W) // 2, (fundo.height - H) // 2
    fundo = fundo.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(30))
    fundo = ImageEnhance.Brightness(fundo).enhance(0.5)
    frente = im.convert('RGB')
    esc2 = min(W / frente.width, H / frente.height)
    frente = frente.resize((round(frente.width * esc2), round(frente.height * esc2)), Image.LANCZOS)
    fundo.paste(frente, ((W - frente.width) // 2, (H - frente.height) // 2))
    return fundo


def _commons_info(titulo):
    import urllib.parse
    import urllib.request
    if not titulo.lower().startswith('file:'):
        titulo = 'File:' + titulo
    q = urllib.parse.urlencode({'action': 'query', 'titles': titulo, 'prop': 'imageinfo',
                                'iiprop': 'url|extmetadata|size|mime', 'format': 'json'})
    try:
        bruto, _ = _abre('https://commons.wikimedia.org/w/api.php?' + q, accept='application/json')
        dados = json.loads(bruto.decode('utf-8'))
    except Exception as e:
        print(f'  (API do Commons indisponível: {e}; lendo a página do arquivo)', file=sys.stderr)
        return _commons_pagina(titulo)
    paginas = dados.get('query', {}).get('pages', {})
    for _, p in paginas.items():
        ii = (p.get('imageinfo') or [None])[0]
        if not ii:
            raise RuntimeError(f'Commons não encontrou {titulo}')
        md = ii.get('extmetadata', {})

        def v(k):
            x = md.get(k, {}).get('value', '') or ''
            x = re.sub(r'<[^>]+>', '', html.unescape(x))
            return re.sub(r'\s+', ' ', x).strip()
        return {
            'titulo': p.get('title', titulo),
            'pagina': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(p.get('title', titulo).replace(' ', '_'), safe=':/,()!'),
            'url': _thumb_padrao(ii.get('url'), ii.get('width')),
            'original': (ii.get('url') or '').split('?')[0],
            'largura': ii.get('width'), 'altura': ii.get('height'),
            'licenca': v('LicenseShortName') or v('License'),
            'licenca_url': v('LicenseUrl'),
            'autor': v('Artist') or v('Credit') or 'Autor não identificado',
            'descricao': v('ImageDescription'),
            'data': v('DateTimeOriginal') or v('DateTime'),
            'atribuicao': v('AttributionRequired'),
        }
    raise RuntimeError('resposta vazia do Commons')


def _commons_pagina(titulo):
    """Plano B: a página do arquivo no Commons traz a licença (licensetpl_short),
    se exige atribuição (licensetpl_attr_req), o autor (fileinfotpl_aut) e o
    endereço do original (fullMedia). No HTML servido o sublinhado das classes
    vem escapado (&#95;), por isso o `U` nas expressões."""
    import urllib.parse
    pagina = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(titulo.replace(' ', '_'), safe=':/,()!')
    bruto, _ = _abre(pagina, accept='text/html')
    h = bruto.decode('utf-8', 'replace')
    U = r'(?:_|&#95;)'

    def limpa(x):
        x = re.sub(r'<[^>]+>', '', html.unescape(x or ''))
        return re.sub(r'\s+', ' ', x).strip()
    lic = re.search(r'class="licensetpl' + U + r'short"[^>]*>(.*?)</span>', h, re.S)
    attr = re.search(r'class="licensetpl' + U + r'attr' + U + r'req"[^>]*>(.*?)</span>', h, re.S)
    aut = re.search(r'id="fileinfotpl' + U + r'aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
    if not aut:
        aut = re.search(r'class="exif-artist"[^>]*>.*?<td[^>]*>(.*?)</td>', h, re.S)
    desc = re.search(r'id="fileinfotpl' + U + r'desc"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
    data = re.search(r'id="fileinfotpl' + U + r'date"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
    orig = re.search(r'class="fullMedia"[^>]*>.*?<a[^>]+href="([^"]+)"', h, re.S)
    dim = re.search(r'class="fileInfo"[^>]*>\s*\(?([\d,.]+)\s*[×x]\s*([\d,.]+)', h, re.S)
    if not lic or not orig:
        raise RuntimeError(f'não achei licença ou arquivo em {pagina}')
    url = html.unescape(orig.group(1)).split('?')[0]
    if url.startswith('//'):
        url = 'https:' + url
    w = int(re.sub(r'\D', '', dim.group(1))) if dim else None
    hh = int(re.sub(r'\D', '', dim.group(2))) if dim else None
    thumb = _thumb_padrao(url, w)
    return {
        'titulo': titulo, 'pagina': pagina, 'url': thumb, 'original': url,
        'largura': w, 'altura': hh, 'licenca': limpa(lic.group(1)), 'licenca_url': '',
        'autor': limpa(aut.group(1)) if aut else 'Autor não identificado',
        'descricao': limpa(desc.group(1)) if desc else '', 'data': limpa(data.group(1)) if data else '',
        'atribuicao': limpa(attr.group(1)) if attr else '',
    }


def cmd_capa(a):
    from PIL import Image
    pasta = producao()
    carimbo = str(int(time.time() * 1000))
    uploads = os.path.join(pasta, 'assets/uploads')
    os.makedirs(uploads, exist_ok=True)
    saida = {}
    if a.arte:
        n = int(a.arte)
        if n not in ARTES:
            sys.exit('arte deve ser de 1 a 6')
        src = os.path.join(pasta, 'assets/artes', ARTES[n] + '-paisagem.png')
        im = Image.open(src).convert('RGB')
        saida.update({'imgCredito': 'Arte: FOYER', 'imgLegenda': ARTES_LEGENDA[n],
                      'imgDireito': 'Arte própria do FOYER (conjunto de artes de palco aprovado em 29/07/2026).',
                      'imgFonte': 'assets/artes/' + ARTES[n] + '.svg'})
    else:
        if a.commons:
            info = _commons_info(a.commons)
            lic = info['licenca']
            if not lic or LICENCAS_NAO.search(lic) or not LICENCAS_OK.search(lic):
                sys.exit(f'licença recusada no Commons: "{lic}" ({info["pagina"]}). Só CC0, domínio público, CC BY e CC BY-SA.')
            url = info['url']
            autor = info['autor']
            if len(autor) > 60:
                autor = autor[:57].rstrip() + '...'
            dp = re.match(r'^(cc0|public domain|pd)', lic, re.I)
            saida.update({
                'imgCredito': f'Foto: {autor} / Wikimedia Commons ({"domínio público" if dp else lic})',
                'imgFonte': info['pagina'],
                'imgDireito': (f'Licença {lic} conferida em {_brt(_agora()).strftime("%d/%m/%Y")} na API do Wikimedia Commons '
                               f'(autor: {info["autor"]}; atribuição exigida: {info["atribuicao"] or "não informado"}).'
                               + (f' Descrição no arquivo: {info["descricao"][:200]}' if info['descricao'] else '')),
                'imgLegenda': '',
                '_commons': {'descricao': info['descricao'], 'data': info['data'], 'licenca_url': info['licenca_url'],
                             'tamanho': f'{info["largura"]}x{info["altura"]}'},
            })
        else:
            url = a.url
            saida.update({'imgCredito': 'Foto: Divulgação', 'imgFonte': url, 'imgLegenda': '',
                          'imgDireito': f'Divulgação oficial, baixada de {url} em {_brt(_agora()).strftime("%d/%m/%Y")}. CONFIRA o fotógrafo e ajuste o crédito.'})
        # a miniatura padrão primeiro; se o servidor recusar o tamanho (400) ou
        # a imagem for menor, cai para o original
        candidatos = [url]
        if a.commons and info.get('original') and info['original'] != url:
            candidatos.append(info['original'])
        dados = tipo = None
        for cand in candidatos:
            print(f'  baixando: {cand}' + (f'  (original {info.get("largura")}x{info.get("altura")})' if a.commons else ''), file=sys.stderr)
            try:
                dados, tipo = _baixa(cand)
                url = cand
                break
            except Exception as e:
                if cand is candidatos[-1]:
                    raise
                print(f'  ({e}; tentando o original)', file=sys.stderr)
        if 'image' not in tipo and not dados[:4] in (b'\xff\xd8\xff\xe0', b'\xff\xd8\xff\xe1', b'\x89PNG'):
            sys.exit(f'o endereço não devolveu imagem (Content-Type {tipo})')
        im = Image.open(io.BytesIO(dados))
        if im.mode in ('RGBA', 'LA', 'P'):
            fundo = Image.new('RGB', im.size, (239, 232, 218))
            fundo.paste(im.convert('RGBA'), mask=im.convert('RGBA').split()[-1])
            im = fundo
        im = im.convert('RGB')
        # a original inteira (redimensionada), para as artes do Instagram
        orig = im.copy()
        if orig.width > 1600:
            orig = orig.resize((1600, round(orig.height * 1600 / orig.width)), Image.LANCZOS)
        caminho_orig = f'assets/uploads/{a.slug}-original-{carimbo}.jpg'
        orig.save(os.path.join(pasta, caminho_orig), 'JPEG', quality=86, optimize=True)
        saida['imgOriginal'] = caminho_orig
    em_pe = im.height > im.width * 0.85
    if a.foco == 'moldura' or (a.foco == 'auto' and em_pe and not a.arte):
        capa = _moldura_16_9(im)
        saida['_corte'] = 'moldura: foto inteira sobre fundo desfocado dela mesma'
    else:
        capa = _corta_16_9(im, 'alto' if a.foco == 'auto' else a.foco)
        saida['_corte'] = 'recorte 16:9 (' + ('terço superior' if em_pe else a.foco) + ')'
    if capa.width > 1600:
        capa = capa.resize((1600, 900), Image.LANCZOS)
    caminho = f'assets/uploads/{a.slug}-{carimbo}.jpg'
    capa.save(os.path.join(pasta, caminho), 'JPEG', quality=86, optimize=True)
    saida['img'] = caminho
    saida['_capa'] = f'{capa.width}x{capa.height}'
    if capa.width < 1200:
        saida['_aviso'] = f'capa estreita ({capa.width} px); o Google Discover prefere 1200'
    print(json.dumps(saida, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ confere

def _texto_limpo(corpo):
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', corpo)
    t = re.sub(r'^galeria:[^\n]*(?:\n[ \t]*\S[^\n]*)*', '', t, flags=re.M)
    t = re.sub(r'^(img:|video:|galeria:|botao:|spotify:|#+ |\*\*\*).*$', '', t, flags=re.M)
    return t


def _blocos(corpo):
    return [b.strip() for b in re.split(r'\n\s*\n', corpo.strip()) if b.strip()]


def _e_intertitulo(b):
    if re.match(r'#{1,6}\s', b):
        return True
    # linha única toda em negrito, curta: intertítulo de lista ("**1. Obra (ano)**")
    return bool(re.fullmatch(r'\*\*[^*\n]{3,120}\*\*', b))


def _paragrafos_prosa(corpo):
    corte = re.split(r'^## +(?:Serviço|Servico)', corpo, flags=re.M)[0]
    return [b for b in _blocos(corte)
            if not _e_intertitulo(b) and not b.startswith(('img:', 'video:', 'galeria:', 'botao:', 'spotify:', '> ', '***', '- ', '* '))]


def _frases(corpo):
    out = []
    for par in _paragrafos_prosa(corpo):
        t = _texto_limpo(par).replace('\n', ' ')
        bruto = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-ÚÁÉÍÓÚÂÊÔÃÕÇ“"\*\[])', t)
        out += [f for f in (x.strip() for x in bruto) if len(f.split()) >= 3]
    return out


def _palavras(corpo):
    return len(re.findall(r"[\wÀ-ÿ'’-]+", _texto_limpo(corpo)))


def _intertitulos(corpo):
    n = 0
    for b in _blocos(corpo):
        if re.match(r'#{1,6}\s*(Serviço|Servico)\b', b):
            continue
        if _e_intertitulo(b):
            n += 1
    return n


def _tira_nomes(txt, nomes):
    for n in nomes or []:
        txt = txt.replace(n, ' ')
    return txt


def auditar(caminho, pasta, corrige=False, rascunho=False):
    P, A = [], []
    try:
        pg = _le_json(caminho)
    except Exception as e:
        return [f'JSON inválido: {e}'], [], {}
    titulo = pg.get('title', '') or ''
    corpo = pg.get('corpo', '') or ''
    nomes = pg.get('nomes_proprios') or []
    porte = pg.get('porte', '')
    slug = pg.get('slug', '')

    obrig = ['title', 'linhaFina', 'slug', 'cat', 'author', 'porte', 'corpo', 'img',
             'imgCredito', 'imgLegenda', 'imgDireito', 'apuracao']
    if not rascunho:
        obrig.append('publishAt')
    for k in obrig:
        if not pg.get(k):
            P.append(f'campo obrigatório vazio: {k}')
    if 'cats' not in pg or not isinstance(pg.get('cats'), list):
        P.append('cats precisa existir e ser lista (vazia se não houver secundária)')
    for k in ('fontes', 'status', 'chefe', 'checagem', 'sugestaoPublishAt'):
        if k in pg:
            P.append(f'campo proibido no pacote: {k}' + (' (sai impresso no site)' if k == 'fontes' else ''))
    if pg.get('author') != AUTOR:
        P.append(f'author tem de ser "{AUTOR}"')
    if pg.get('origem') not in (None, ORIGEM):
        A.append(f'origem "{pg.get("origem")}" (esperado {ORIGEM}; o publica carimba)')
    if pg.get('cat') not in CATS:
        P.append(f'cat "{pg.get("cat")}" fora da lista canônica')
    cats = [c for c in (pg.get('cats') or []) if c]
    if len(cats) > 2:
        P.append(f'cats com {len(cats)} editorias; o máximo é 2')
    for c in cats:
        if c not in CATS | CATS_SO_SECUNDARIA:
            P.append(f'editoria secundária "{c}" fora da lista')
        if c == pg.get('cat'):
            P.append(f'"{c}" repetida em cat e cats')
    if porte not in PORTES:
        P.append(f'porte "{porte}" desconhecido ({", ".join(PORTES)})')

    # slug
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug or ''):
        P.append('slug só com a-z, 0-9 e hifens')
    if slug and len(slug) > 80:
        P.append(f'slug com {len(slug)} caracteres (máximo 80)')
    if slug and not corrige and slug in _slugs_acervo(pasta, exceto=caminho):
        P.append(f'slug "{slug}" já existe no acervo ou em import/novas (use --corrige se for correção)')
    if slug and os.path.basename(caminho) != slug + '.json':
        A.append(f'o arquivo deveria chamar {slug}.json')

    # título e linha fina
    if titulo:
        if '*' in titulo:
            P.append('título com asterisco')
        if len(titulo) > 110:
            P.append(f'título com {len(titulo)} caracteres (teto duro 110)')
        elif len(titulo) > 90:
            A.append(f'título com {len(titulo)} caracteres (ideal até 90; os 60 primeiros decidem)')
        if re.search(TEMPO_NO_TITULO, _sem_acento(titulo)):
            P.append('título com "hoje/ontem/amanhã/nesta": use a data')
        if re.search(r'\b(entenda|veja|confira|saiba|descubra)\b', _sem_acento(titulo)) and not re.search(r'\?$', titulo.strip()):
            A.append('título com muleta (entenda/veja/confira/saiba/descubra)')
    lf = pg.get('linhaFina') or ''
    if lf:
        if not 60 <= len(lf) <= 220:
            P.append(f'linha fina com {len(lf)} caracteres (faixa 60 a 220)')
        if _sem_acento(lf).strip('. ') == _sem_acento(titulo).strip('. '):
            P.append('linha fina igual ao título')
        if '**' in lf:
            P.append('linha fina com negrito')

    # travessão e meia-risca
    for campo in ('title', 'linhaFina', 'corpo', 'imgLegenda'):
        v = _tira_nomes(pg.get(campo) or '', nomes)
        if '—' in v or '–' in v:
            P.append(f'travessão ou meia-risca em {campo} (fora de nomes_proprios)')
    if '—' in (pg.get('imgCredito') or '') or '–' in (pg.get('imgCredito') or ''):
        A.append('travessão no crédito da foto; prefira " / " e parênteses')

    # fórmulas, clichês, aspas
    texto_sa = _sem_acento(_texto_limpo(corpo) + ' ' + titulo + ' ' + lf)
    for f in FORMULAS:
        m = re.search(_sem_acento(f), texto_sa)
        if m:
            P.append(f'fórmula proibida: "{m.group(0)}"')
    for c in CLICHES:
        if _sem_acento(c) in texto_sa:
            P.append(f'clichê: "{c}"')
    # trio de adjetivos/termos: "x, y e z" com três palavras curtas seguidas no fim de frase
    for m in re.finditer(r'\b(\w{5,}), (\w{5,}) e (\w{5,})[.,]', corpo):
        a1, a2, a3 = m.groups()
        if all(x.endswith(('nte', 'ado', 'ada', 'oso', 'osa', 'vel', 'ico', 'ica', 'ivo', 'iva')) for x in (a1, a2, a3)):
            A.append(f'trio de adjetivos: "{m.group(0)}"')
    # pergunta retórica seguida de resposta
    for m in re.finditer(r'\?\s+(Sim|Não|A resposta|Depende)\b', corpo):
        A.append(f'pergunta retórica com resposta imediata: "...{m.group(0)}"')
    if re.search(r'^\s*[-*] ', corpo, re.M):
        if porte in PORTES_FRIOS:
            A.append('lista de tópicos no corpo (na fria, prefira intertítulos por item)')
        else:
            P.append('lista de tópicos no corpo de matéria quente')
    if re.search(r'https?://', _texto_limpo(re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', corpo))):
        A.append('URL crua no texto; use [texto](url)')

    # porte, intertítulos, blocos
    blocos = _blocos(corpo)
    if blocos:
        if re.fullmatch(r'\*\*[^*]+\*\*', blocos[0]) and len(blocos[0]) > 40:
            P.append('primeiro parágrafo inteiro em negrito (o site o transforma em linha fina)')
        prosa = _paragrafos_prosa(corpo)
        if prosa and re.match(RESUMO_FINAL, _sem_acento(prosa[-1])):
            P.append('parágrafo final de resumo ("' + prosa[-1][:40] + '...")')
        inicios = [re.sub(r'\W+', ' ', _sem_acento(_texto_limpo(p))).strip().split(' ')[:2] for p in prosa]
        for i in range(2, len(inicios)):
            if inicios[i] and inicios[i] == inicios[i - 1] == inicios[i - 2]:
                A.append(f'três parágrafos seguidos começando com "{" ".join(inicios[i])}"')
                break
    if porte in PORTES:
        piso, teto, imin, imax = PORTES[porte]
        n = _palavras(corpo)
        if n < piso:
            P.append(f'{n} palavras: abaixo do piso do porte {porte} ({piso}-{teto})')
        elif n > teto * 1.1:
            P.append(f'{n} palavras: acima do teto do porte {porte} ({piso}-{teto})')
        elif n > teto:
            A.append(f'{n} palavras: passou do teto do porte {porte} ({teto}) dentro da folga de 10%')
        k = _intertitulos(corpo)
        if k < imin or k > imax:
            P.append(f'{k} intertítulos; o porte {porte} pede de {imin} a {imax}')
    # ritmo
    fr = _frases(corpo)
    if len(fr) >= 6:
        curtas = sum(1 for f in fr if len(f.split()) < 12) / len(fr)
        media = sum(len(f.split()) for f in fr) / len(fr)
        if curtas < 0.15:
            P.append(f'ritmo: só {curtas:.0%} das frases com menos de 12 palavras (mínimo 20%)')
        elif curtas < 0.20:
            A.append(f'ritmo: {curtas:.0%} de frases curtas (meta 20%)')
        if media > 28:
            P.append(f'ritmo: média de {media:.1f} palavras por frase (máximo 28)')
        elif media > 26:
            A.append(f'ritmo: média de {media:.1f} palavras por frase (ideal até 26)')
    # serviço quando há evento
    if pg.get('evento') and porte in ('nota', 'quente') and not re.search(r'^## +Serviço', corpo, re.M):
        A.append('matéria com evento e sem bloco ## Serviço')

    # ---- profundidade e cara de máquina (ordem do Pedro, 14/10/2026)
    prosa = _paragrafos_prosa(corpo)
    texto_sa_corpo = _sem_acento(_texto_limpo(corpo))
    # repertório: os movimentos dele, no máximo uma vez por semana no conjunto
    for mov in REPERTORIO:
        n_aqui = texto_sa_corpo.count(_sem_acento(mov))
        if n_aqui > 1:
            P.append(f'"{mov}" {n_aqui} vezes na mesma matéria: é repertório, não fôrma')
        elif n_aqui == 1:
            limite = _agora() - timedelta(days=7)
            for n in _novas(pasta):
                if n.get('author') != AUTOR or n.get('slug') == slug:
                    continue
                try:
                    d = datetime.fromisoformat((n.get('publishAt') or '').replace('Z', '+00:00'))
                except Exception:
                    continue
                if d >= limite and _sem_acento(mov) in _sem_acento(n.get('corpo', '')):
                    A.append(f'"{mov}" já saiu esta semana em "{n.get("title", "")[:50]}"; use outro movimento')
                    break
    # prosa de planilha: números demais num parágrafo, listas de valores entre parênteses
    for par in prosa:
        t = _texto_limpo(par)
        # conta só o que é número de verdade na leitura: dinheiro, porcentagem,
        # quantidade (mil, milhões) e cifras de quatro dígitos ou mais; dia e ano não contam
        t_sem_datas = re.sub(r'\b\d{1,2} de [a-zç]+(?: de \d{4})?|\(\d{1,2}\)|\b(?:19|20)\d{2}\b', ' ', t)
        nums = re.findall(r'(?:R\$|US\$|€|£)\s?[\d.,]+(?:\s?(?:mil|milh[õo]es|bilh[õo]es))?|\d[\d.,]*\s?(?:%|mil\b|milh[õo]es|bilh[õo]es)|\b\d{1,3}(?:\.\d{3})+\b', t_sem_datas)
        parens = re.findall(r'\((?:R\$|US\$|€|£)\s?[\d.,]+', t)
        if len(parens) >= 3:
            P.append('prosa de planilha: três ou mais valores entre parênteses num parágrafo ("' + t[:50] + '...")')
        elif len(nums) > 5:
            A.append(f'{len(nums)} números num parágrafo ("' + t[:50] + '..."): escolha um e explique')
    # staccato: frase de até três palavras, no máximo uma por matéria
    curtissimas = [f for f in _frases(corpo) if len(f.split()) <= 3]
    if len(curtissimas) > 2:
        P.append(f'{len(curtissimas)} frases de até três palavras: soa máquina ("' + '", "'.join(c[:25] for c in curtissimas[:3]) + '")')
    elif len(curtissimas) == 2:
        A.append('duas frases de até três palavras; uma por matéria basta')
    # parágrafo de fôlego e variedade de tamanho
    if porte in ('quente', 'contexto', 'perfil', 'explicador', 'resposta') and prosa:
        tam = [len(_texto_limpo(x).split()) for x in prosa]
        if max(tam) < 70:
            P.append(f'nenhum parágrafo de fôlego (o maior tem {max(tam)} palavras; a matéria precisa de ao menos um com 70 ou mais)')
        if len(tam) >= 5 and (max(tam) - min(tam)) < 25:
            A.append('parágrafos quase todos do mesmo tamanho: a simetria é a marca mais traiçoeira')
    # voz humana: aspas reais com mais de cinco palavras
    if porte in ('quente', 'contexto', 'perfil'):
        falas = [m for m in re.findall(r'[“"]([^”"]{20,}?)[”"]', corpo) if len(m.split()) >= 6]
        if not falas:
            A.append('nenhuma declaração entre aspas: procure uma voz real (entrevista publicada, release, rede oficial), com o veículo nomeado')
    # apuração mínima por porte
    ap_n = len([u for u in (pg.get('apuracao') or []) if isinstance(u, str)])
    if porte in APURACAO_MIN and ap_n < APURACAO_MIN[porte]:
        P.append(f'apuracao com {ap_n} URLs; o porte {porte} pede ao menos {APURACAO_MIN[porte]} páginas lidas')

    # imagem
    img = pg.get('img') or ''
    if img:
        cam = os.path.join(pasta, img)
        if not img.startswith('assets/uploads/'):
            P.append('img precisa estar em assets/uploads/')
        elif not os.path.isfile(cam):
            P.append(f'imagem não existe na cópia de produção: {img}')
        else:
            try:
                from PIL import Image
                with Image.open(cam) as im:
                    w, h = im.size
                if abs(w / h - 16 / 9) > 0.03:
                    P.append(f'capa {w}x{h} não está em 16:9')
                if w < 1200:
                    A.append(f'capa com {w} px de largura (o Discover prefere 1200)')
            except Exception as e:
                P.append(f'não abri a imagem: {e}')
    cred = (pg.get('imgCredito') or '').lower()
    for ag in AGENCIAS:
        if ag in cred:
            P.append(f'agência proibida no crédito: {ag}')
    if cred and not re.match(r'^(foto|arte|imagem|ilustra|reprodu|frame|cr[eé]dito)', cred):
        A.append('crédito sem rótulo (Foto:, Arte:, Imagem:)')
    leg = pg.get('imgLegenda') or ''
    if leg:
        if len(leg) < 25:
            P.append('descritivo da imagem curto demais')
        if _sem_acento(leg).strip('. ') == _sem_acento(titulo).strip('. '):
            P.append('descritivo igual ao título')
        if len(leg) > 240:
            A.append(f'descritivo com {len(leg)} caracteres; uma frase basta')
    if (pg.get('imgCredito') or '').startswith('Foto: Divulgação') and 'CONFIRA' in (pg.get('imgDireito') or ''):
        A.append('crédito genérico "Foto: Divulgação": confira o fotógrafo')
    if cred and 'divulga' not in cred and 'arte' not in cred and not pg.get('imgFonte'):
        A.append('imgFonte vazio')

    # apuração
    ap = pg.get('apuracao') or []
    if not isinstance(ap, list) or any(not isinstance(u, str) or not u.startswith('http') for u in ap):
        P.append('apuracao precisa ser lista de URLs')
    elif len(ap) < 2:
        P.append(f'apuracao com {len(ap)} URL (mínimo 2)')
    if any('foyer.digital' in u for u in ap if isinstance(u, str)):
        A.append('matéria da casa em apuracao (link interno vai no corpo, não na apuração)')

    # publishAt
    pub = pg.get('publishAt') or ''
    if pub:
        try:
            dtp = datetime.fromisoformat(pub.replace('Z', '+00:00'))
            if porte in PORTES_FRIOS:
                if dtp.strftime('%H:%M:%S') != '10:00:00':
                    P.append(f'fria com publishAt fora das 10:00:00Z (7h de Brasília): {pub}')
                if dtp <= _agora() and not corrige:
                    P.append('fria com publishAt no passado')
                for n in _novas(pasta):
                    if n.get('author') == AUTOR and n.get('slug') != slug and (n.get('publishAt') or '')[:13] == pub[:13]:
                        P.append(f'colide com "{n.get("title", "")[:50]}" no mesmo horário')
            else:
                pass  # quem marca a hora é o Pedro; o espaço entre matérias é conferido no publica
        except Exception:
            P.append(f'publishAt inválido: {pub}')
    if pub and not re.search(r'\.\d{3}Z$', pub):
        A.append('publishAt sem milissegundos (o publica normaliza)')

    info = {'porte': porte, 'inter': _intertitulos(corpo), 'palavras': _palavras(corpo), 'slug': slug}
    return P, A, info


def cmd_confere(a, pasta=None, corrige=False, rascunho=False):
    pasta = pasta or producao()
    total = 0
    esqueletos = []
    for c in a.pacotes:
        P, A, info = auditar(c, pasta, corrige=corrige, rascunho=rascunho)
        total += len(P)
        esqueletos.append((info.get('porte'), info.get('inter')))
        print(f'\n== {os.path.basename(c)}  [{info.get("porte")}, {info.get("palavras")} palavras, {info.get("inter")} intertítulos]')
        for p in P:
            print('  ✗ PROBLEMA:', p)
        for w in A:
            print('  ! aviso:', w)
        if not P and not A:
            print('  ✓ limpo')
        elif not P:
            print('  ✓ passa (com avisos)')
    if len(esqueletos) >= 2 and len(set(esqueletos)) == 1:
        print('\n  ! aviso de MOLDE: todas as matérias desta leva têm o mesmo porte e a mesma conta de intertítulos')
    # as últimas do Pedro em novas, para a régua de três seguidas
    ultimas = [(n.get('porte'), _intertitulos(n.get('corpo', ''))) for n in sorted(_novas(pasta), key=lambda n: n.get('publishAt', ''))
               if n.get('author') == AUTOR][-2:]
    if ultimas and esqueletos and all(e == esqueletos[0] for e in ultimas + esqueletos[:1]) and esqueletos[0][0]:
        print('  ! aviso de MOLDE: as duas últimas do Pedro no site já têm este porte e esta conta de intertítulos')
    return total


# ------------------------------------------------------------ ja-saiu / fila

def cmd_ja_saiu(a):
    pasta = producao()
    chaves = [_sem_acento(p) for p in re.findall(r'\w{4,}', a.termos)]
    if not chaves:
        sys.exit('dê ao menos uma palavra com 4 letras ou mais')
    achados = []
    try:
        for m in _le_json(os.path.join(pasta, 'import/materias.json')):
            t = _sem_acento(m.get('title', '') + ' ' + m.get('desc', ''))
            if all(k in t for k in chaves):
                achados.append((m.get('iso', ''), m.get('author', ''), m.get('title', ''), 'acervo'))
    except Exception:
        pass
    for n in _novas(pasta):
        t = _sem_acento(n.get('title', '') + ' ' + (n.get('linhaFina') or '') + ' ' + n.get('corpo', '')[:600])
        if all(k in t for k in chaves):
            quando = (n.get('publishAt') or '')[:16]
            estado = 'agendada' if (n.get('publishAt') or '') > _iso_ms(_agora()) else 'no ar'
            achados.append((quando, n.get('author', ''), n.get('title', ''), estado))
    achados.sort(reverse=True)
    if not achados:
        print('nada no acervo nem na fila com:', ' + '.join(chaves))
    for q, au, t, e in achados[:25]:
        print(f'{q[:10]:>10} | {e:8} | {au:18} | {t}')


def _proximos_7h(pasta, n=5):
    ocupados = set()
    for m in _novas(pasta):
        if m.get('author') == AUTOR:
            ocupados.add((m.get('publishAt') or '')[:10])
    dia = (_agora() + timedelta(days=1)).date()
    ultimo = max((d for d in ocupados if d), default='')
    if ultimo and ultimo >= dia.isoformat():
        dia = datetime.fromisoformat(ultimo).date() + timedelta(days=1)
    saida = []
    while len(saida) < n:
        if dia.isoformat() not in ocupados:
            saida.append(datetime(dia.year, dia.month, dia.day, 10, 0, tzinfo=timezone.utc))
        dia += timedelta(days=1)
    return saida


def cmd_proximo_7h(a):
    pasta = producao()
    for dt in _proximos_7h(pasta, a.n):
        print(_iso_ms(dt), '  (', _brt(dt).strftime('%a %d/%m 7h'), ')')


# ------------------------------------------------- mesa, horários e publicação

def _hora_pedro(txt):
    """A hora como o Pedro escreve: ISO (com Z ou fuso), "15/10 09:00",
    "15/10/2026 09:00" ou "09:00" (hoje, ou amanhã se já passou). Sem fuso, é
    Brasília. Devolve datetime em UTC."""
    from zoneinfo import ZoneInfo
    br = ZoneInfo('America/Sao_Paulo')
    t = (txt or '').strip().lower().replace('h', ':').replace('às', '').strip()
    agora_br = _agora().astimezone(br)
    m = re.fullmatch(r'(\d{4}-\d{2}-\d{2})[t ](\d{1,2}):(\d{2})(?::\d{2}(?:\.\d+)?)?(z|[+-]\d{2}:?\d{2})?', t)
    if m:
        base = datetime.fromisoformat(m.group(1) + 'T' + m.group(2).zfill(2) + ':' + m.group(3) + ':00')
        if m.group(4):
            dt = datetime.fromisoformat(m.group(1) + 'T' + m.group(2).zfill(2) + ':' + m.group(3) + ':00' + ('+00:00' if m.group(4) == 'z' else m.group(4)))
        else:
            dt = base.replace(tzinfo=br)
        return dt.astimezone(timezone.utc)
    m = re.fullmatch(r'(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\s+(\d{1,2}):(\d{2})', t)
    if m:
        ano = int(m.group(3) or agora_br.year)
        dt = datetime(ano, int(m.group(2)), int(m.group(1)), int(m.group(4)), int(m.group(5)), tzinfo=br)
        if not m.group(3) and dt < agora_br - timedelta(days=1):
            dt = dt.replace(year=ano + 1)
        return dt.astimezone(timezone.utc)
    m = re.fullmatch(r'(\d{1,2}):(\d{2})', t)
    if m:
        dt = agora_br.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0, microsecond=0)
        if dt <= agora_br:
            dt += timedelta(days=1)
        return dt.astimezone(timezone.utc)
    raise RuntimeError(f'não entendi a hora "{txt}": use "15/10 09:00", "09:00" ou ISO')


def _vizinhos(pasta, dtp, slug, minutos=ESPACO_MIN):
    """Outras matérias do Pedro (no ar ou agendadas) a menos de `minutos` da hora dada."""
    out = []
    for n in _novas(pasta):
        if n.get('author') != AUTOR or n.get('slug') == slug:
            continue
        try:
            d = datetime.fromisoformat((n.get('publishAt') or '').replace('Z', '+00:00'))
        except Exception:
            continue
        if abs((d - dtp).total_seconds()) < minutos * 60:
            out.append((n.get('title', ''), d))
    return out


def _horarios_livres(pasta, n=4, a_partir=None):
    """Os próximos horários do relógio da casa com espaço livre em volta."""
    from zoneinfo import ZoneInfo
    br = ZoneInfo('America/Sao_Paulo')
    piso = (a_partir or _agora()) + timedelta(minutes=30)
    dia = piso.astimezone(br).date()
    saida = []
    while len(saida) < n and (dia - piso.astimezone(br).date()).days < 14:
        for h in RELOGIO:
            dt = datetime(dia.year, dia.month, dia.day, h, 0, tzinfo=br).astimezone(timezone.utc)
            if dt < piso or _vizinhos(pasta, dt, None):
                continue
            if any(abs((dt - x).total_seconds()) < ESPACO_MIN * 60 for x in saida):
                continue
            saida.append(dt)
            if len(saida) >= n:
                break
        dia += timedelta(days=1)
    return saida


def cmd_horarios(a):
    pasta = producao()
    for dt in _horarios_livres(pasta, a.n):
        print(_brt(dt).strftime('%a %d/%m %Hh%M'), ' ', _iso_ms(dt))


def _mensagem(acao, titulo, sessao, skip_ci=False):
    msg = f'Mesa do Pedro: {acao} "{titulo}"' + (' [skip ci]' if skip_ci else '') + f'\n\n{COAUTOR}'
    if sessao:
        msg += f'\nClaude-Session: {sessao}'
    return msg


def _push(pasta):
    espera = 2
    for tent in range(5):
        r = _git(pasta, 'push', '-u', 'origin', PRODUCAO, check=False, quiet=True)
        if r.returncode == 0:
            return True
        print(f'push recusado ({tent + 1}/5): {r.stdout.strip()[:300]}')
        if tent == 4:
            break
        _git(pasta, 'fetch', 'origin', PRODUCAO, check=False, quiet=True)
        rb = _git(pasta, 'rebase', f'origin/{PRODUCAO}', check=False, quiet=True)
        if rb.returncode != 0:
            _git(pasta, 'rebase', '--abort', check=False, quiet=True)
            print('rebase falhou; a cópia de produção precisa de conserto à mão')
            return False
        time.sleep(espera)
        espera *= 2
    return False


def _acha_pacote(pasta, ref):
    """Um caminho, ou um slug que mora na mesa (rascunho) ou em import/novas."""
    if os.path.isfile(ref):
        return os.path.abspath(ref)
    for base in (MESA, 'import/novas'):
        c = os.path.join(pasta, base, ref.removesuffix('.json') + '.json')
        if os.path.isfile(c):
            return c
    raise RuntimeError(f'não achei o pacote "{ref}" (nem na mesa, nem em import/novas)')


def _limpa_pacote(pg):
    for k in ('_capa', '_commons', '_corte', '_aviso'):
        pg.pop(k, None)
    pg['author'] = AUTOR
    pg['criadoPor'] = AUTOR
    pg['origem'] = ORIGEM
    return pg


def _imprime_laudo(slug, P, A, info):
    print(f'\n== {slug}  [{info.get("porte")}, {info.get("palavras")} palavras, {info.get("inter")} intertítulos]')
    for p in P:
        print('  ✗ PROBLEMA:', p)
    for w in A:
        print('  ! aviso:', w)


def cmd_guarda(a):
    """O rascunho vai para import/mesa-pedro/ na branch de produção, com
    [skip ci]: fica guardado no repositório e NÃO aparece no site. Dali só sai
    com o `publica --ok`, depois que o Pedro autorizar aqui na conversa."""
    pasta = producao(atualiza=True)
    os.makedirs(os.path.join(pasta, MESA), exist_ok=True)
    guardados = []
    for c in a.pacotes:
        pg = _limpa_pacote(_le_json(c))
        slug = pg.get('slug') or ''
        if not slug:
            sys.exit(f'{c}: sem slug')
        pg.setdefault('criadoEm', _iso_ms(_agora()))
        pg['publishAt'] = ''
        pg['mesa'] = {'status': 'aguardando o Pedro', 'guardadoEm': _iso_ms(_agora())}
        destino = os.path.join(pasta, MESA, slug + '.json')
        _grava_json(destino, pg)
        P, A, info = auditar(destino, pasta, rascunho=True, corrige=a.corrige)
        _imprime_laudo(slug, P, A, info)
        if P:
            os.remove(destino)
            sys.exit('reprovado no portão: o rascunho não foi guardado. Corrija e rode de novo.')
        arquivos = [os.path.relpath(destino, pasta)]
        for k in ('img', 'imgOriginal'):
            if pg.get(k) and os.path.isfile(os.path.join(pasta, pg[k])):
                arquivos.append(pg[k])
        _git(pasta, 'add', '--', *arquivos, quiet=True)
        r = _git(pasta, 'commit', '-q', '-m', _mensagem('rascunho', pg.get('title', slug), a.sessao, skip_ci=True) + '\n\nAguardando a autorização do Pedro na conversa. Não aparece no site.', check=False, quiet=True)
        guardados.append((slug, pg.get('title', slug)))
    if a.sem_push:
        print('(--sem-push: rascunhos commitados só na cópia de produção local)')
    elif not _push(pasta):
        sys.exit('o push não entrou; os rascunhos estão só na cópia de produção local.')
    print('\nRASCUNHOS GUARDADOS (nada no ar). Aguardando o Pedro dizer qual sai e a que hora:')
    for slug, t in guardados:
        print(f'  {slug}\n    {t}')
    print('\nHorários livres do relógio da casa (mínimo de', ESPACO_MIN, 'min entre matérias):')
    for dt in _horarios_livres(pasta, max(3, len(guardados) + 1)):
        print('  ', _brt(dt).strftime('%a %d/%m %Hh%M'))


def cmd_publica(a):
    if not a.ok:
        sys.exit('sem --ok: o Pedro não autorizou esta publicação nesta conversa. Nada foi feito.')
    modos = sum(bool(x) for x in (a.agora, a.proximo_7h, a.em))
    if modos != 1 and not (a.corrige and modos == 0):
        sys.exit('diga a hora que o Pedro mandou: --em "15/10 09:00" (ou --agora, ou --proximo-7h para frias; correção sem hora mantém a original)')
    if (a.em or a.agora) and len(a.pacotes) > 1:
        sys.exit('com --em ou --agora, uma matéria por chamada: cada uma tem a sua hora, e nunca duas juntas')
    pasta = producao(atualiza=True)
    fila = _proximos_7h(pasta, len(a.pacotes) + 2) if a.proximo_7h else []
    publicados = []
    for i, ref in enumerate(a.pacotes):
        origem = _acha_pacote(pasta, ref)
        pg = _limpa_pacote(_le_json(origem))
        slug = pg.get('slug') or ''
        if not slug:
            sys.exit(f'{origem}: sem slug')
        agora = _agora()
        hora_mantida = False
        if a.agora:
            dtp = agora.replace(second=0, microsecond=0)
        elif a.proximo_7h:
            dtp = fila[i]
        elif a.em:
            dtp = _hora_pedro(a.em)
        else:
            # correção sem hora: mantém a hora da matéria já publicada ou agendada
            atual = pg.get('publishAt') or ''
            ja = os.path.join(pasta, 'import/novas', slug + '.json')
            if not atual and os.path.isfile(ja):
                atual = _le_json(ja).get('publishAt') or ''
            if not atual:
                sys.exit('correção sem hora e sem matéria publicada com este slug: diga a hora')
            dtp = datetime.fromisoformat(atual.replace('Z', '+00:00'))
            hora_mantida = True
        if dtp < agora - timedelta(minutes=5) and not a.corrige:
            sys.exit(f'a hora pedida ({_brt(dtp).strftime("%d/%m %Hh%M")}) já passou')
        pg['publishAt'] = _iso_ms(dtp)
        if a.corrige:
            ja = os.path.join(pasta, 'import/novas', slug + '.json')
            if os.path.isfile(ja) and os.path.abspath(ja) != os.path.abspath(origem):
                antigo = _le_json(ja)
                for k in ('criadoEm', 'img', 'imgOriginal', 'imgCredito', 'imgLegenda', 'imgDireito', 'imgFonte'):
                    if not pg.get(k) and antigo.get(k):
                        pg[k] = antigo[k]
                pg.setdefault('criadoEm', antigo.get('criadoEm', _iso_ms(agora)))
        pg.setdefault('criadoEm', _iso_ms(agora))
        pg.pop('mesa', None)
        if a.corrige:
            pg['atualizadoEm'] = _iso_ms(agora)
            if a.correcao:
                pg['correcao'] = {'texto': a.correcao if a.correcao.lower().startswith('corre') else 'Correção: ' + a.correcao,
                                  'quando': agora.isoformat()}
        # o espaço entre matérias: nunca duas juntas
        if a.espaco > 0 and not hora_mantida:
            viz = _vizinhos(pasta, dtp, slug, a.espaco)
            if viz:
                for t, d in viz:
                    print(f'  ✗ a menos de {a.espaco} min de "{t[:60]}" ({_brt(d).strftime("%d/%m %Hh%M")})')
                sys.exit('hora recusada: nunca duas matérias juntas. Escolha outra hora (veja `horarios`) ou passe --espaco 0 se o Pedro mandou assim.')
        destino = os.path.join(pasta, 'import/novas', slug + '.json')
        if os.path.exists(destino) and not a.corrige and os.path.abspath(destino) != os.path.abspath(origem):
            sys.exit(f'{slug}.json já existe em import/novas; use --corrige para substituir')
        if not a.corrige and slug in _slugs_acervo(pasta, exceto=destino):
            sys.exit(f'slug "{slug}" já existe no acervo; escolha outro ou use --corrige')
        _grava_json(destino, pg)
        P, A, info = auditar(destino, pasta, corrige=a.corrige)
        _imprime_laudo(slug, P, A, info)
        if P:
            if os.path.abspath(destino) != os.path.abspath(origem):
                os.remove(destino)
            sys.exit('reprovado no portão: nada foi publicado. Corrija e rode de novo.')
        arquivos = ['import/novas/' + slug + '.json']
        for k in ('img', 'imgOriginal'):
            if pg.get(k) and os.path.isfile(os.path.join(pasta, pg[k])):
                arquivos.append(pg[k])
        if origem.startswith(os.path.join(pasta, MESA)):
            _git(pasta, 'rm', '-q', '--cached', '--', os.path.relpath(origem, pasta), check=False, quiet=True)
            os.remove(origem)
        _git(pasta, 'add', '--', *arquivos, quiet=True)
        futuro = dtp > agora + timedelta(minutes=2)
        acao = 'corrige' if a.corrige else ('agenda' if futuro else 'publica')
        titulo = pg.get('title', slug)
        msg = _mensagem(acao + (f' para {_brt(dtp).strftime("%d/%m às %-Hh%M")}' if futuro and not a.corrige else ''), titulo, a.sessao)
        msg += '\n\nAutorizado pelo Pedro na conversa.'
        r = _git(pasta, 'commit', '-q', '-m', msg, check=False, quiet=True)
        if r.returncode != 0:
            print('nada para commitar?', r.stdout.strip()[:200])
        publicados.append((slug, titulo, dtp, futuro))
    if a.sem_push:
        print('\n(--sem-push: commits feitos na cópia de produção, nada enviado)')
    elif not _push(pasta):
        sys.exit('o push não entrou. Os commits estão na cópia de produção; nada no ar. Avise o Pedro com o erro acima.')
    print()
    for slug, titulo, dtp, futuro in publicados:
        quando = _brt(dtp).strftime('%d/%m/%Y %Hh%M')
        print(('AGENDADA para ' if futuro else 'PUBLICADA às ') + quando + ' (Brasília)')
        print('  ' + titulo)
        print(f'  {BASE_URL}/post-{slug}.html' + ('' if futuro else '   (no ar em 2 a 3 minutos, depois que o pages.yml montar o site)'))


def cmd_descarta(a):
    pasta = producao(atualiza=True)
    fora = []
    for ref in a.slugs:
        c = os.path.join(pasta, MESA, ref.removesuffix('.json') + '.json')
        if not os.path.isfile(c):
            sys.exit(f'não achei o rascunho {ref} na mesa')
        pg = _le_json(c)
        _git(pasta, 'rm', '-q', '--', os.path.relpath(c, pasta), quiet=True)
        fora.append(pg.get('title', ref))
    _git(pasta, 'commit', '-q', '-m', _mensagem('descarta', '; '.join(t[:60] for t in fora), a.sessao, skip_ci=True) + f'\n\nMotivo: {a.motivo}', quiet=True)
    if not _push(pasta):
        sys.exit('o push não entrou; o descarte ficou só na cópia local')
    for t in fora:
        print('DESCARTADO:', t)


def cmd_remove(a):
    pasta = producao(atualiza=True)
    origem = os.path.join(pasta, 'import/novas', a.slug + '.json')
    if not os.path.isfile(origem):
        sys.exit(f'não achei import/novas/{a.slug}.json na cópia de produção')
    pg = _le_json(origem)
    agora = _agora()
    pg['_origem'] = 'import/novas/' + a.slug + '.json'
    pg['removidoPor'] = AUTOR + ' (mesa)'
    pg['removidoEm'] = _iso_ms(agora)
    pg['motivoRemocao'] = a.motivo
    destino = os.path.join(pasta, 'import/lixeira', f'{a.slug}-{int(agora.timestamp() * 1000)}.json')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    _grava_json(destino, pg)
    _git(pasta, 'rm', '-q', '--', 'import/novas/' + a.slug + '.json', quiet=True)
    _git(pasta, 'add', '--', os.path.relpath(destino, pasta), quiet=True)
    _git(pasta, 'commit', '-q', '-m', _mensagem('remove', pg.get('title', a.slug), a.sessao), quiet=True)
    if not _push(pasta):
        sys.exit('o push não entrou; a remoção ficou só na cópia de produção')
    print(f'REMOVIDA: "{pg.get("title", a.slug)}" foi para import/lixeira; o site remonta sem ela em 2 a 3 minutos.')


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('capa', help='baixa e recorta a foto de capa para a cópia de produção')
    c.add_argument('--slug', required=True)
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument('--url', help='imagem de divulgação oficial')
    g.add_argument('--commons', help='nome do arquivo no Wikimedia Commons (File:...)')
    g.add_argument('--arte', help='arte da casa, 1 a 6')
    c.add_argument('--foco', choices=['auto', 'moldura', 'alto', 'centro', 'baixo'], default='auto',
                   help='auto: foto em pé vira moldura (inteira sobre fundo desfocado), deitada recorta pelo alto; alto/centro/baixo forçam o recorte')
    c.set_defaults(fn=cmd_capa)

    c = sub.add_parser('confere', help='o portão: reprova ou avisa')
    c.add_argument('pacotes', nargs='+')
    c.add_argument('--corrige', action='store_true', help='aceita slug já existente')
    c.add_argument('--rascunho', action='store_true', help='rascunho na mesa: publishAt ainda vazio')
    c.set_defaults(fn=lambda a: sys.exit(1 if cmd_confere(a, corrige=a.corrige, rascunho=a.rascunho) else 0))

    c = sub.add_parser('ja-saiu', help='procura o assunto no acervo e na fila')
    c.add_argument('termos')
    c.set_defaults(fn=cmd_ja_saiu)

    c = sub.add_parser('proximo-7h', help='os próximos dias livres às 7h para pautas frias')
    c.add_argument('--n', type=int, default=5)
    c.set_defaults(fn=cmd_proximo_7h)

    c = sub.add_parser('guarda', help='rascunho na mesa (import/mesa-pedro), aguardando o Pedro; nada vai ao site')
    c.add_argument('pacotes', nargs='+')
    c.add_argument('--sessao', default=os.environ.get('CLAUDE_SESSION_URL', ''))
    c.add_argument('--sem-push', action='store_true')
    c.add_argument('--corrige', action='store_true', help='rascunho de reescrita de matéria já publicada (mesmo slug)')
    c.set_defaults(fn=cmd_guarda)

    c = sub.add_parser('horarios', help='próximos horários livres do relógio da casa (7, 9, 12, 15, 18, 20h)')
    c.add_argument('--n', type=int, default=4)
    c.set_defaults(fn=cmd_horarios)

    c = sub.add_parser('publica', help='SÓ depois que o Pedro autorizar na conversa e disser a hora')
    c.add_argument('pacotes', nargs='+', help='slug na mesa, ou caminho do pacote')
    c.add_argument('--ok', action='store_true', help='o Pedro autorizou esta publicação nesta conversa')
    c.add_argument('--em', help='a hora que o Pedro mandou: "15/10 09:00", "09:00" ou ISO (Brasília se sem fuso)')
    c.add_argument('--agora', action='store_true', help='só se o Pedro disse "agora"')
    c.add_argument('--proximo-7h', action='store_true', help='frias aprovadas: próximo 7h livre, uma por dia')
    c.add_argument('--espaco', type=int, default=ESPACO_MIN, help=f'minutos mínimos até outra matéria dele (padrão {ESPACO_MIN}; 0 só se o Pedro mandar)')
    c.add_argument('--corrige', action='store_true', help='correção de matéria já publicada ou agendada')
    c.add_argument('--correcao', help='texto da nota de correção impressa no fim da matéria')
    c.add_argument('--sessao', default=os.environ.get('CLAUDE_SESSION_URL', ''), help='URL da sessão para o rodapé do commit')
    c.add_argument('--sem-push', action='store_true')
    c.set_defaults(fn=cmd_publica)

    c = sub.add_parser('descarta', help='o Pedro recusou: tira o rascunho da mesa')
    c.add_argument('slugs', nargs='+')
    c.add_argument('--motivo', required=True)
    c.add_argument('--sessao', default=os.environ.get('CLAUDE_SESSION_URL', ''))
    c.set_defaults(fn=cmd_descarta)

    c = sub.add_parser('remove', help='tira a matéria do ar (vai para import/lixeira)')
    c.add_argument('slug')
    c.add_argument('--motivo', required=True)
    c.add_argument('--sessao', default=os.environ.get('CLAUDE_SESSION_URL', ''))
    c.set_defaults(fn=cmd_remove)

    a = ap.parse_args()
    try:
        a.fn(a)
    except RuntimeError as e:
        sys.exit(f'erro: {e}')


if __name__ == '__main__':
    main()
