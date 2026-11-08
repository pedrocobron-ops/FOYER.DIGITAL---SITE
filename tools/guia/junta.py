# Junta o que os coletores trouxeram (import/guia/brutos/*.json) num arquivo
# só, import/guia/agenda.json, que a página do guia lê.
#
# O que ele faz sozinho, todo dia:
# - tira o que já acabou (temporada encerrada sai no dia seguinte ao fim);
# - fonte que falhou ou ficou velha (mais de DIAS_VELHA sem coleta boa) NÃO
#   é publicada: aparece no aviso, em vez de mostrar dado velho;
# - registra mudança de horário, preço ou temporada em mudancas.json;
# - marca o mesmo espetáculo achado em duas fontes ("tambem_em");
# - junta a ficha do lugar vinda de fontes diferentes e guarda divergência.
import json
import os
import re
import sys
import glob
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(__file__))
from comum import DADOS, BRUTOS, agora, agora_iso, slug

DIAS_VELHA = 3
SEMANA = re.compile(r'segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo', re.I)
# fonte mais próxima do lugar vale mais (BRIEFING, seção 2)
PESO = {'cinemateca': 3, 'guiaoff': 1}


def _v(c):
    return c.get('v') if isinstance(c, dict) else None


def _ultimo_dia(s):
    """Último dia em que a sessão acontece, pelo que a fonte diz. None = não sabe."""
    if _v(s.get('ate')):
        return _v(s['ate'])
    if _v(s.get('inicio')):
        return _v(s['inicio'])[:10]
    datas = _v(s.get('datas')) or []
    if datas and not SEMANA.search(_v(s.get('quando')) or ''):
        return max(datas)
    return None


def _vale(s, hoje):
    u = _ultimo_dia(s)
    return u is None or u >= hoje


def _assinatura(e):
    return {('%s|%s' % (s.get('lugar'), _v(s.get('inicio')) or _v(s.get('quando')) or '')):
            {k: _v(s.get(k)) for k in ('quando', 'ate', 'preco', 'inicio')} for s in e.get('sessoes', [])}


def main():
    hoje = agora().date().isoformat()
    os.makedirs(DADOS, exist_ok=True)
    arq = os.path.join(DADOS, 'agenda.json')
    anterior = json.load(open(arq, encoding='utf-8')) if os.path.exists(arq) else {'eventos': []}
    ant_por_id = {e['id']: e for e in anterior.get('eventos', [])}

    fontes, eventos, lugares, divergencias = {}, [], {}, []
    for b in sorted(glob.glob(os.path.join(BRUTOS, '*.json'))):
        d = json.load(open(b, encoding='utf-8'))
        f = d['fonte']
        ultima_boa = d.get('coletado_em')
        idade = None
        if ultima_boa:
            idade = (agora() - datetime.fromisoformat(ultima_boa)).days
        publica = bool(ultima_boa) and idade is not None and idade <= DIAS_VELHA
        fontes[f] = {'ok': d.get('ok'), 'rodou_em': d.get('rodou_em'), 'ultima_coleta_boa': ultima_boa,
                     'erro': d.get('erro'), 'nota': d.get('nota'), 'publicada': publica,
                     'itens': len(d.get('itens') or [])}
        if not publica:
            continue
        for l in d.get('lugares', []):
            atual = lugares.get(l['id'])
            if not atual:
                lugares[l['id']] = l
                continue
            # campo novo entra com a origem dele; campo diferente vira divergência
            base = len(atual['origens'])
            atual['origens'] += l['origens']
            for k, c in l.items():
                if k in ('id', 'origens') or not isinstance(c, dict):
                    continue
                if k not in atual:
                    atual[k] = dict(c, o=c['o'] + base)
                elif _v(atual[k]) != c['v']:
                    divergencias.append({'lugar': l['id'], 'campo': k, 'fica': _v(atual[k]), 'outra': c['v'],
                                         'fonte_outra': l['origens'][c['o']]['url']})
        for e in d.get('itens', []):
            sess = [s for s in e.get('sessoes', []) if _vale(s, hoje)]
            if not sess:
                continue
            e = dict(e, sessoes=sess, fonte=f)
            eventos.append(e)

    # mesmo título em fontes diferentes: liga os dois (não apaga nenhum)
    por_titulo = {}
    for e in eventos:
        por_titulo.setdefault(slug(_v(e.get('titulo'))), []).append(e)
    for grupo in por_titulo.values():
        if len({e['fonte'] for e in grupo}) > 1:
            for e in grupo:
                e['tambem_em'] = sorted(x['id'] for x in grupo if x is not e)

    # mudanças desde a última rodada
    mud_arq = os.path.join(DADOS, 'mudancas.json')
    mudancas = json.load(open(mud_arq, encoding='utf-8')) if os.path.exists(mud_arq) else []
    for e in eventos:
        a = ant_por_id.get(e['id'])
        if not a:
            continue
        sa, sn = _assinatura(a), _assinatura(e)
        for k, novo in sn.items():
            velho = sa.get(k)
            if velho and velho != novo:
                for campo_ in novo:
                    if velho.get(campo_) != novo.get(campo_):
                        mudancas.append({'em': agora_iso(), 'evento': e['id'], 'titulo': _v(e.get('titulo')),
                                         'campo': campo_, 'antes': velho.get(campo_), 'agora': novo.get(campo_)})
    mudancas = mudancas[-300:]

    eventos.sort(key=lambda e: (_v(e.get('area')) or '', slug(_v(e.get('titulo')))))
    usados = {s.get('lugar') for e in eventos for s in e['sessoes']}
    saida = {'gerado_em': agora_iso(), 'hoje': hoje, 'fontes': fontes,
             'eventos': eventos, 'lugares': {k: v for k, v in sorted(lugares.items()) if k in usados},
             'divergencias': divergencias}
    with open(arq, 'w', encoding='utf-8') as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write('\n')
    with open(mud_arq, 'w', encoding='utf-8') as fh:
        json.dump(mudancas, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    quebradas = [f for f, x in fontes.items() if not x['publicada']]
    print('agenda: %d eventos, %d lugares, %d divergências; fontes fora: %s'
          % (len(eventos), len(saida['lugares']), len(divergencias), ', '.join(quebradas) or 'nenhuma'))


if __name__ == '__main__':
    main()
