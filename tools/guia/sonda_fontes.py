# Sonda diária das fontes que AINDA não têm coletor: só pergunta "está no
# ar? deixa entrar?", sem baixar programação. Resultado em
# import/guia/sondas.json. Serve para decidir o próximo coletor com dado do
# próprio GitHub (a rede de lá é diferente da rede de teste da sessão).
import json
import os
import sys
import urllib.error

sys.path.insert(0, os.path.dirname(__file__))
from comum import Educado, DADOS, agora_iso

SONDAS = {
    # SP Cultura (Mapas Culturais da Prefeitura): em 08/11/2026 recusou a
    # conexão a partir da rede de teste. Aqui vê se do GitHub responde.
    'spcultura': 'https://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,name&@limit=1',
    # Sesc SP: a API de atividades responde 403 para robôs (bloqueio de
    # propósito, não contornamos); o mapa do site e as páginas são liberados.
    'sesc_api': 'https://www.sescsp.org.br/wp-json/wp/v1/atividades/filter?intervalo=hoje&ppp=1',
    'sesc_mapa': 'https://www.sescsp.org.br/sitemap_index.xml',
}


def main():
    web = Educado()
    res = {}
    for nome, url in SONDAS.items():
        try:
            txt = web.texto(url)
            res[nome] = {'ok': True, 'bytes': len(txt), 'inicio': txt[:120]}
        except urllib.error.HTTPError as e:
            res[nome] = {'ok': False, 'erro': 'HTTP %d' % e.code}
        except Exception as e:
            res[nome] = {'ok': False, 'erro': '%s: %s' % (type(e).__name__, str(e)[:160])}
        res[nome]['url'] = url
        print(nome, 'ok' if res[nome]['ok'] else res[nome]['erro'])
    os.makedirs(DADOS, exist_ok=True)
    with open(os.path.join(DADOS, 'sondas.json'), 'w', encoding='utf-8') as f:
        json.dump({'em': agora_iso(), 'resultado': res}, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')


if __name__ == '__main__':
    main()
