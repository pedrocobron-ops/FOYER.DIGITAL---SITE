# Peças comuns aos coletores do Guia (tools/guia/). Só biblioteca padrão do
# Python: roda no GitHub Actions sem instalar nada.
#
# Regra de ouro (BRIEFING.md, seção 2): todo campo guarda de onde veio.
# Cada registro tem uma lista "origens" (fonte, url, coletado_em) e cada campo
# é {"v": valor, "o": índice da origem}. Campo sem origem não existe.
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone, timedelta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DADOS = os.path.join(RAIZ, 'import', 'guia')
BRUTOS = os.path.join(DADOS, 'brutos')

# Nome genérico, sem e-mail pessoal (BRIEFING, seção 2)
UA = 'FOYER-Guia/1.0 (agenda cultural; +https://foyer.digital)'
PAUSA = 1.5          # segundos entre pedidos ao mesmo site: nada de rajada
SP = timezone(timedelta(hours=-3))   # São Paulo não tem horário de verão desde 2019


def agora():
    return datetime.now(SP).replace(microsecond=0)


def agora_iso():
    return agora().isoformat()


class Educado:
    """Busca páginas respeitando robots.txt, com pausa e identificação."""

    def __init__(self):
        self._robots = {}
        self._ultimo = {}

    def _pode(self, url):
        m = re.match(r'(https?://[^/]+)', url)
        base = m.group(1)
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                txt = self._baixa(base + '/robots.txt', checa=False)
                rp.parse(txt.splitlines())
            except urllib.error.HTTPError as e:
                # sem robots.txt (404) = liberado. Outro erro (403 etc.) = o site
                # recusa até o robots.txt para esta rede: não arrisca, e diz.
                if e.code not in (404, 410):
                    raise PermissionError('o site recusou o robots.txt (HTTP %d): bloqueia esta rede' % e.code)
                rp.parse([])
            self._robots[base] = rp
        return self._robots[base].can_fetch(UA, url)

    def _baixa(self, url, checa=True, tentativas=3):
        if checa and not self._pode(url):
            raise PermissionError('robots.txt não permite: ' + url)
        base = re.match(r'(https?://[^/]+)', url).group(1)
        espera = PAUSA - (time.time() - self._ultimo.get(base, 0))
        if espera > 0:
            time.sleep(espera)
        erro = None
        for n in range(tentativas):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'pt-BR'})
                with urllib.request.urlopen(req, timeout=40) as r:
                    self._ultimo[base] = time.time()
                    return r.read().decode('utf-8', 'replace')
            except urllib.error.HTTPError as e:
                self._ultimo[base] = time.time()
                if e.code < 500:
                    raise
                erro = e
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                erro = e
            time.sleep(5 * (n + 1))
        raise erro

    def texto(self, url):
        return self._baixa(url)

    def json(self, url):
        return json.loads(self._baixa(url))


def slug(txt):
    t = unicodedata.normalize('NFKD', txt or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:80]


def limpa(html_txt):
    """HTML para texto simples, uma linha."""
    import html as _h
    t = re.sub(r'<br\s*/?>', '\n', html_txt or '')
    t = re.sub(r'<[^>]+>', ' ', t)
    t = _h.unescape(t).replace('\xa0', ' ')
    t = re.sub(r'[ \t]+', ' ', t)
    return '\n'.join(l.strip() for l in t.split('\n') if l.strip())


def trecho(txt, n=220):
    """Trecho curto da fonte (nunca o texto inteiro de divulgação)."""
    t = re.sub(r'\s+', ' ', txt or '').strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(' ', 1)[0] + '…'


def campo(valor, o=0, **extra):
    if valor in (None, '', [], {}):
        return None
    d = {'v': valor, 'o': o}
    d.update(extra)
    return d


def sem_vazios(d):
    return {k: v for k, v in d.items() if v not in (None, '', [], {})}


def grava_bruto(fonte, ok, itens, lugares=None, erro=None, nota=None):
    """Saída de cada coletor: import/guia/brutos/<fonte>.json.
    Se a coleta falhou, NÃO sobrescreve os itens anteriores: só marca o erro
    (o junta.py avisa e deixa de publicar o que ficar velho)."""
    os.makedirs(BRUTOS, exist_ok=True)
    arq = os.path.join(BRUTOS, fonte + '.json')
    anterior = {}
    if os.path.exists(arq):
        with open(arq, encoding='utf-8') as f:
            anterior = json.load(f)
    if ok:
        saida = {'fonte': fonte, 'ok': True, 'rodou_em': agora_iso(), 'coletado_em': agora_iso(),
                 'itens': itens, 'lugares': lugares or []}
    else:
        saida = dict(anterior) if anterior else {'fonte': fonte, 'itens': [], 'lugares': []}
        saida.update({'ok': False, 'rodou_em': agora_iso()})
    if erro:
        saida['erro'] = str(erro)[:500]
    else:
        saida.pop('erro', None)
    if nota:
        saida['nota'] = nota
    with open(arq, 'w', encoding='utf-8') as f:
        json.dump(saida, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    return saida
