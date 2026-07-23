#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migra todas as imagens do Wix para o repositório (assets/acervo/).

1. Varre capas (import/materias.json) e corpos (import/corpo/*.html)
   atrás de URLs static.wixstatic.com.
2. Baixa cada mídia UMA vez, já redimensionada pelo CDN (máx. 1400px,
   qualidade 82) — tamanho de site, não o original gigante.
3. Grava import/imagens-map.json (mídia -> arquivo local + origens).
4. Com --reescrever, troca todas as referências do acervo pelas cópias
   locais (materias.json + corpo/*.html). Sem a flag, só baixa.

Retomável: arquivos já baixados são pulados.
Uso: python3 tools/migra_imagens.py [--reescrever] [--limite N]
"""
import hashlib, json, os, re, sys, glob, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(ROOT, 'assets/acervo')
MAPA_PATH = os.path.join(ROOT, 'import/imagens-map.json')
RE_WIX = re.compile(r'https://static\.wixstatic\.com/media/[^"\s)\\]+')
LIMITE = 0
for i, a in enumerate(sys.argv):
    if a == '--limite':
        LIMITE = int(sys.argv[i + 1])


def media_id(url):
    m = re.match(r'https://static\.wixstatic\.com/media/([^/]+?)(?:/v1/.*)?$', url)
    return m.group(1) if m else None


def coletar():
    urls = set()
    mats = json.load(open(f'{ROOT}/import/materias.json'))
    for m in mats:
        if m.get('img') and 'wixstatic' in m['img']:
            urls.add(m['img'])
    for f in glob.glob(f'{ROOT}/import/corpo/*.html'):
        urls.update(RE_WIX.findall(open(f).read()))
    por_id = {}
    for u in urls:
        mid = media_id(u)
        if mid:
            por_id.setdefault(mid, set()).add(u)
    return por_id


def nome_local(mid):
    h = hashlib.md5(mid.encode()).hexdigest()[:16]
    base = mid.split('~')[0].lower()
    ext = 'png' if base.endswith('.png') else ('gif' if base.endswith('.gif') else 'jpg')
    return f'assets/acervo/{h}.{ext}'


def url_download(mid, ext):
    if ext == 'gif':   # gif animado: original
        return f'https://static.wixstatic.com/media/{mid}'
    arq = 'file.png' if ext == 'png' else 'file.jpg'
    return f'https://static.wixstatic.com/media/{mid}/v1/fit/w_1400,h_1400,q_82/{arq}'


def baixar(mid):
    rel = nome_local(mid)
    alvo = os.path.join(ROOT, rel)
    if os.path.exists(alvo) and os.path.getsize(alvo) > 1024:
        return mid, rel, 'ja-existia'
    ext = rel.rsplit('.', 1)[1]
    for tentativa, u in enumerate([url_download(mid, ext),
                                   f'https://static.wixstatic.com/media/{mid}']):
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=40) as r:
                dados = r.read()
            if len(dados) < 1024:
                continue
            open(alvo, 'wb').write(dados)
            return mid, rel, f'ok ({len(dados)//1024}KB)'
        except Exception as e:
            erro = str(e)[:60]
    return mid, rel, f'FALHA: {erro}'


def main():
    os.makedirs(DESTINO, exist_ok=True)
    por_id = coletar()
    ids = sorted(por_id)
    if LIMITE:
        ids = ids[:LIMITE]
    print(f'{len(ids)} mídias para garantir')
    mapa, falhas, novos = {}, 0, 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(baixar, mid): mid for mid in ids}
        for i, f in enumerate(as_completed(futs), 1):
            mid, rel, st = f.result()
            if st.startswith('FALHA'):
                falhas += 1
                print(f'  ! {mid[:40]} {st}')
            else:
                if st.startswith('ok'):
                    novos += 1
                mapa[mid] = {'local': rel, 'origens': sorted(por_id[mid])}
            if i % 100 == 0:
                print(f'  … {i}/{len(ids)} ({falhas} falhas)')
    json.dump(mapa, open(MAPA_PATH, 'w'), ensure_ascii=False, indent=0)
    tam = sum(os.path.getsize(os.path.join(ROOT, v['local'])) for v in mapa.values()
              if os.path.exists(os.path.join(ROOT, v['local'])))
    print(f'concluído: {len(mapa)} locais ({novos} baixados agora), {falhas} falhas, {tam//1048576} MB no acervo')

    if '--reescrever' not in sys.argv:
        print('(baixa apenas — rode com --reescrever para trocar as referências)')
        return

    # ---- troca as referências ----
    def local_de(url):
        mid = media_id(url)
        return mapa.get(mid, {}).get('local')

    mats = json.load(open(f'{ROOT}/import/materias.json'))
    n_capas = 0
    for m in mats:
        if m.get('img') and 'wixstatic' in m['img']:
            novo = local_de(m['img'])
            if novo:
                m['img'] = novo
                n_capas += 1
    json.dump(mats, open(f'{ROOT}/import/materias.json', 'w'), ensure_ascii=False, indent=0)

    n_corpos = 0
    for f in glob.glob(f'{ROOT}/import/corpo/*.html'):
        s = open(f).read()
        trocado = RE_WIX.sub(lambda mm: local_de(mm.group(0)) or mm.group(0), s)
        if trocado != s:
            open(f, 'w').write(trocado)
            n_corpos += 1
    print(f'reescrito: {n_capas} capas e {n_corpos} corpos apontando para o acervo local')
    sobra = sum(1 for f in glob.glob(f'{ROOT}/import/corpo/*.html')
                if 'wixstatic' in open(f).read())
    print(f'referências wixstatic restantes nos corpos: {sobra}')


if __name__ == '__main__':
    main()
