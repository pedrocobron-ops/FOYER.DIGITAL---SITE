#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza import/youtube.json com os episódios reais do canal do FOYER.

Usa o feed RSS público de cada playlist (sem chave de API):
    https://www.youtube.com/feeds/videos.xml?playlist_id=<ID>
Cada feed traz os ~15 vídeos mais recentes — suficiente para as páginas.

Uso:  python3 tools/atualiza_youtube.py
"""
import json, os, re, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANAL = 'https://www.youtube.com/@Foyer.digital'

# playlist_id, nome do programa, papel na página
PROGRAMAS = [
    ('PLFPAp2PKrLk2xo9BULjM0wmganFcGd88C', 'Programa do Foyer — 6ª temporada', 'entrevista'),
    ('PLFPAp2PKrLk3jT3v-FXr9O73jhu3_KaC8', 'Programa do Foyer — 5ª temporada', 'entrevista'),
    ('PLFPAp2PKrLk15leURL9x9-HQjDGTeXP2R', 'Críticas Teatrais', 'critica'),
    ('PLFPAp2PKrLk3MV6Gxs3yqncYjycC905VI', 'Teatro a Sangue Frio', 'programa'),
    ('PLFPAp2PKrLk3twR1PzHCo5l7afF0F5dPI', 'Astro em Cena', 'programa'),
    ('PLFPAp2PKrLk13Yccyp7Au8-TJ-R8extiv', 'Trivia Musical Game Show', 'programa'),
    ('PLFPAp2PKrLk0KP-K-Q8qL-LRk9AiAINmy', 'Session Musical', 'programa'),
    ('PLFPAp2PKrLk3dDXvpjoZgBh0obVCPYCmV', 'Coxixo de Coxia', 'programa'),
    ('PLFPAp2PKrLk1JMqCrXQk2_LBXIrJVSLpC', 'Corda Bamba', 'programa'),
    ('PLFPAp2PKrLk2BpCq8k-eOGXHk-WlGZFHm', 'Por Bruno Cavalcanti', 'critica'),
]

NS = {'a': 'http://www.w3.org/2005/Atom',
      'yt': 'http://www.youtube.com/xml/schemas/2015',
      'media': 'http://search.yahoo.com/mrss/'}


def feed(playlist_id):
    url = f'https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        raiz = ElementTree.fromstring(r.read())
    videos = []
    for e in raiz.findall('a:entry', NS):
        vid = e.findtext('yt:videoId', '', NS)
        videos.append({
            'id': vid,
            'titulo': e.findtext('a:title', '', NS),
            'quando': (e.findtext('a:published', '', NS) or '')[:10],
            'thumb': f'https://i.ytimg.com/vi/{vid}/hq720.jpg',
            'url': f'https://www.youtube.com/watch?v={vid}&list={playlist_id}',
        })
    return videos


def main():
    # O retrato anterior é a rede de segurança: nas rodadas das 6h o YouTube
    # vinha devolvendo TUDO vazio, o robô salvava o vazio por cima do retrato
    # bom, e a seção de críticas da capa sumia até a rodada seguinte
    # (pego em 19/08/2026). Playlist que voltar vazia mantém o que já tinha.
    arq = os.path.join(ROOT, 'import/youtube.json')
    try:
        antigo = {p.get('id'): p.get('videos') or []
                  for p in json.load(open(arq)).get('programas', [])}
    except Exception:
        antigo = {}
    saida = {'atualizadoEm': datetime.now(timezone.utc).isoformat(),
             'canal': CANAL, 'programas': []}
    for pid, nome, papel in PROGRAMAS:
        try:
            vids = feed(pid)
        except Exception as e:
            print(f'! {nome}: {e}')
            vids = []
        if not vids and antigo.get(pid):
            vids = antigo[pid]
            print(f'  {nome}: YouTube vazio agora — mantém os {len(vids)} vídeo(s) do retrato anterior')
        saida['programas'].append({
            'id': pid, 'nome': nome, 'papel': papel,
            'urlPlaylist': f'https://www.youtube.com/playlist?list={pid}',
            'videos': vids,
        })
        print(f'• {nome}: {len(vids)} vídeo(s)')
    json.dump(saida, open(os.path.join(ROOT, 'import/youtube.json'), 'w'),
              ensure_ascii=False, indent=1)
    print('import/youtube.json atualizado')


if __name__ == '__main__':
    main()
