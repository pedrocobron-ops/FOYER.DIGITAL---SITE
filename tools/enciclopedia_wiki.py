#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bio e foto dos verbetes da Enciclopédia a partir da Wikipédia em português.

Lê import/enciclopedia.json (os verbetes) e grava import/enciclopedia-wiki.json:
  { "slug": {"titulo", "url", "descricao", "resumo", "foto", "fotoPagina", "quando"} }
  ou {"nao": true, "quando": ...} para quem não tem página (não pergunta de novo
  por 90 dias).

Cuidados (05/10/2026):
- Só aceita página que fale de gente das artes (ator, diretora, cantor, dramaturgo…)
  E que seja brasileira ou tenha presença forte no FOYER (5+ aparições). Isso
  derruba homônimos: "Pedro Amaral" na Wikipédia é um maestro português.
- Desambiguação nunca entra. Equipe do FOYER e colunistas têm bio própria
  (import/equipe.json e import/opiniao.json) e não passam por aqui.
- A foto é a miniatura da própria Wikipédia (Wikimedia Commons), com link
  para a página do arquivo, onde estão autor e licença.
- Pede em lotes de 20 nomes, com User-Agent identificado e pausa, como a
  Wikimedia pede.

Auditoria de 12/10/2026:
- Só entra foto do Wikimedia Commons com licença livre conhecida (CC BY,
  CC BY-SA, CC0, domínio público...). O envio local da Wikipédia lusófona
  (thumb.wikimedia.org/wikipedia/pt/...) é "Conteúdo restrito": vale só dentro
  da Wikipédia, e 24 verbetes usavam essas fotos. Autor e licença saem da API
  (imageinfo/extmetadata) e ficam guardados em fotoAutor, fotoLicenca e
  fotoLicencaUrl, para o verbete creditar "Foto: Autor / Wikimedia Commons
  (licença)". Foto sem esses dados não é usada pelo build.
- Homônimo: a profissão da Wikipédia tem de combinar com o que o acervo diz
  da pessoa (funções deduzidas em import/enciclopedia.json) e não pode ser de
  fora das artes ("monge beneditino", "política brasileira"). Verbete que a
  redação já sabe que é outra pessoa fica em "wiki_nao" nas regras.
Uso: python3 tools/enciclopedia_wiki.py [--todos] [--limite N]
     python3 tools/enciclopedia_wiki.py --revalidar   (regra nova sobre o que já está salvo, sem rede)
     python3 tools/enciclopedia_wiki.py --licencas    (autor e licença das fotos já salvas)
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    _REGRAS = json.load(open(f'{ROOT}/import/enciclopedia-regras.json'))
except Exception:
    _REGRAS = {}
WIKI_OK = set(_REGRAS.get('wiki_ok') or [])
# verbetes cuja página da Wikipédia é de OUTRA pessoa com o mesmo nome
# (auditoria de 12/10/2026: Fernanda Maia, a diretora do Núcleo Experimental,
# saía com a bio de uma apresentadora de TV). Nunca recebem bio nem foto de lá.
WIKI_NAO = set(_REGRAS.get('wiki_nao') or [])
UA = 'FOYER-enciclopedia/1.0 (https://foyer.digital; contato@foyer.digital)'
ARTES = re.compile(r'\b(ator|atriz|atores|diretor|diretora|encenador|dramaturg|teatr|cantor|cantora|m[úu]sic|compositor|'
                   r'cineasta|humorista|comediante|bailarin|coreógraf|coreograf|escritor|poeta|jornalista|apresentador|'
                   r'produtor|cenógraf|figurinista|iluminador|roteirista|maestro|maestrina|pianista|instrumentista|'
                   r'performer|drag|artista|dublador|ilustrador|crítico|crítica|dançarin|circense|palhaç|ópera|opera|'
                   r'musical|novela|televis|cinema|filme|banda|rapper|dj\b|regente|arranjador|libretista|fotógraf|'
                   r'fadista|transformista)', re.I)
BRASIL = re.compile(r'brasileir|são paulo|rio de janeiro|brasil|paulistan|carioca|mineir|baian|gaúch|pernambucan|'
                    r'paranaense|catarinense|capixab|goian|cearense|paraiban|potiguar|sergipan|alagoan|maranhense|'
                    r'piauiense|amazonense|paraense|acrean|rondonien|roraimense|amapaense|tocantinense|mato-grossense|'
                    r'sul-mato-grossense|brasiliense', re.I)


def lote(nomes):
    q = urllib.parse.urlencode({
        'action': 'query', 'prop': 'extracts|pageimages|description|info', 'inprop': 'url',
        'exintro': 1, 'explaintext': 1, 'exsentences': 3, 'exlimit': 'max',
        'piprop': 'thumbnail|name', 'pithumbsize': 480,
        'titles': '|'.join(nomes), 'format': 'json', 'redirects': 1, 'maxlag': 5})
    req = urllib.request.Request('https://pt.wikipedia.org/w/api.php?' + q, headers={'User-Agent': UA})
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            if 'error' in d and d['error'].get('code') == 'maxlag':
                time.sleep(5 * (tentativa + 1)); continue
            return d
        except Exception as e:
            time.sleep(8 * (tentativa + 1))
    return None


# descrição curta que denuncia que a página NÃO é de uma pessoa (gênero
# musical, personagem, banda, festival…) — "Bossa nova" e "Homem de Lata"
# passaram na primeira rodada por falarem de música e de cinema (05/10/2026)
#   Auditoria de 10/10/2026: o plural escapava ("distribuidora de filmes" é
# Diamond Films) e faltavam franquia, distribuidora, editora e reality (Star
# Wars, American Idol). Do outro lado, PESSOA casava pedaço de palavra:
# "banda de cantores e compositores" (Barão Vermelho) passava por "cantor".
# Agora PESSOA só vale no singular e com a palavra inteira, porque quem
# descreve uma pessoa diz "cantor", e "cantores" descreve um grupo.
NAO_PESSOA = re.compile(r'\b(personage[mn]|g[êe]nero|estilo|movimento|banda|grupo|dupla|trio|coletivo|festival|'
                        r'[áa]lbum|can[çc][ãa]o|can[çc][õo]es|filme|pe[çc]a|telenovela|s[ée]rie|programa|empresa|teatro|pr[êe]mio|'
                        r'evento|escola|institui[çc][ãa]o|companhia|cia\.|bairro|cidade|munic[íi]pio|livro|romance|'
                        r'revista|jornal|emissora|canal|site|obra|espet[áa]culo|musical|musicais|minis[ée]rie|desenho|jogo|'
                        r'franquia|distribuidora|editora|gravadora|talent show|reality show|reality)s?\b', re.I)
PESSOA = re.compile(r'\b(?:ator|atriz|cantor|cantora|diretor|diretora|dramaturg[oa]|escritor|escritora|poeta|m[úu]sico|'
                    r'musicista|compositor|compositora|humorista|comediante|bailarin[oa]|core[óo]graf[oa]|apresentador|'
                    r'apresentadora|produtor|produtora|cineasta|jornalista|artista|performer|pianista|maestro|'
                    r'roteirista|dublador|dubladora|figurinista|cen[óo]graf[oa]|iluminador|iluminadora|encenador|encenadora|regente|'
                    r'arranjador|arranjadora|ilustrador|ilustradora|fot[óo]graf[oa]|dan[çc]arin[oa]|palha[çc][oa]|drag|'
                    r'intérprete|interprete|empres[áa]ri[oa]|'
                    r'fundador|fundadora|criador|criadora|professor|professora|pesquisador|pesquisadora|historiador|historiadora|'
                    r'crítico|crítica|'
                    r'autor|autora|libretista|ativista|educador|educadora|fadista|transformista|travesti|sambista|violonista|'
                    r'guitarrista|baterista|percussionista|saxofonista|flautista|violinista|cellista|tenor|soprano|bar[íi]tono|'
                    r'rapper|mc|dj|modelo|estilista|arquitet[oa]|pintor|pintora|escultor|escultora|cartunista|quadrinista|'
                    r'nascid[oa]|falecid[oa])\b', re.I)
_UM_DOS = re.compile(r'\bum[a]? d[oa]s((?:\s+[^\s,.;:]+){1,3})', re.I)


def _fala_de_gente(t):
    """A descrição fala de gente: 'atriz brasileira', ou 'um dos grandes
    diretores do teatro brasileiro' (o plural só vale depois de 'um dos')."""
    if PESSOA.search(t):
        return True
    for m in _UM_DOS.finditer(t):
        for w in m.group(1).split():
            for sing in (w[:-2] if w.endswith('es') else '', w[:-1] if w.endswith('s') else ''):
                if sing and PESSOA.fullmatch(sing):
                    return True
    return False


def _palavras_em_comum(a, b):
    """Há alguma palavra (3+ letras, sem acento, minúscula) em comum?"""
    def toks(t):
        t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
        return {w for w in re.findall(r'[a-z]{3,}', t)}
    return bool(toks(a) & toks(b))


# ---- homônimos (auditoria de 12/10/2026). Antes bastava a página falar de
# "gente das artes" e do Brasil, e seis verbetes ganharam bio, foto e sameAs
# de outra pessoa: o monge Dom Marcos Barbosa no lugar do dramaturgo, um
# humorista no lugar do estilista João Pimenta. Agora a profissão que a
# Wikipédia dá (descrição curta e o "é um/foi um..." da primeira frase) tem de
# (1) começar por um ofício das artes ou da comunicação e (2) combinar com a
# função que o próprio acervo deduz (Figurino, Direção, Música...).
FORA_ARTES = re.compile(r'\b(pol[íi]tic[oa]|deputad[oa]|vereador[a]?|senador[a]?|governador[a]?|prefeit[oa]|'
                        r'ministr[oa]|presidente|monge|padre|frade|freira|sacerdote|bispo|arcebispo|cardeal|papa|'
                        r'santo|santa|religios[oa]|pastor[a]?|engenheir[oa]|m[ée]dic[oa]|advogad[oa]|jurista|juiz|'
                        r'juíza|futebolista|jogador[a]?|atleta|nadador[a]?|tenista|piloto|militar|general|'
                        r'economista|cientista|f[íi]sic[oa]|qu[íi]mic[oa]|bi[óo]log[oa]|matem[áa]tic[oa]|'
                        r'banqueir[oa]|arque[óo]log[oa]|lutador[a]?|treinador[a]?|policial|'
                        r'delegad[oa]|diplomata|nobre|rei|rainha|imperador|imperatriz|pr[íi]ncipe|princesa)\b', re.I)
# função do acervo -> palavras da Wikipédia que combinam com ela
_COMPAT = [
    (('Direção', 'Diretor', 'Diretora', 'Encenador', 'Encenadora'),
     r'diretor|diretora|encenador|encenadora|cineasta|realizador|realizadora|ator|atriz|actor|actriz|dramaturg|produtor|produtora|core[óo]graf|'
     r'artista|arquitet|cen[óo]graf|designer'),
    (('Dramaturgia', 'Dramaturgo', 'Dramaturga', 'Autor', 'Autora', 'Escritor', 'Escritora', 'Roteirista', 'Poeta', 'Tradução'),
     r'dramaturg|escritor|escritora|autor|autora|roteirista|argumentista|poeta|poetisa|novelista|romancista|letrista|'
     r'compositor|compositora|cronista|ator|atriz|actor|actriz|diretor|diretora|tradutor|tradutora|ensa[íi]sta|fil[óo]sof'),
    (('Figurino', 'Figurinista'), r'figurinista|estilista|designer|cen[óo]graf|artista pl[áa]stic|artista visual|costureir|moda'),
    (('Música', 'Música musical', 'Compositor', 'Compositora', 'Cantor', 'Cantora', 'Músico', 'Musicista', 'Maestro',
      'Maestrina', 'Pianista', 'Regente', 'Arranjador', 'Arranjadora', 'Diretor musical', 'Diretora musical', 'Direção musical'),
     r'm[úu]sic|compositor|compositora|cantor|cantora|maestr|pianista|instrumentista|regente|arranjador|arranjadora|'
     r'violonista|guitarrista|baterista|baixista|percussionista|violinista|cellista|tenor|soprano|bar[íi]tono|rapper|'
     r'letrista|sambista|fadista|\bdj\b|vocalista|int[ée]rprete'),
    (('Atuação', 'Ator', 'Atriz'),
     r'ator|atriz|actor|actriz|humorista|comediante|apresentador|apresentadora|cantor|cantora|bailarin|dan[çc]arin|'
     r'modelo|dublador|dobrador|drag|transformista|performer|palha[çc]|youtuber|influenciador|vedete|showman'),
    (('Coreografia', 'Coreógrafo', 'Coreógrafa', 'Bailarino', 'Bailarina', 'Dançarino', 'Dançarina'),
     r'core[óo]graf|bailarin|dan[çc]arin|dan[çc]a|ator|atriz'),
    (('Jornalista', 'Crítico', 'Crítica', 'Crítica teatral'),
     r'jornalista|cr[íi]tic|escritor|escritora|apresentador|apresentadora|radialista|cronista|colunista'),
    (('Cenografia', 'Cenógrafo', 'Cenógrafa'), r'cen[óo]graf|arquitet|artista|figurinista|diretor de arte|designer'),
    (('Iluminação', 'Iluminador', 'Iluminadora'), r'iluminador|iluminadora|diretor de fotografia|cen[óo]graf'),
    (('Fotografia', 'Fotógrafo', 'Fotógrafa'), r'fot[óo]graf'),
]


# ofício central do palco: quem a Wikipédia descreve assim é aceito mesmo que
# a função deduzida do acervo seja outra (atriz que também canta, ator que
# dirige); a função do acervo erra às vezes, e esse não é o caso do homônimo
PALCO = re.compile(r'\b(ator|atriz|actor|actriz|diretor[a]?|encenador[a]?|'
                   r'dramaturg[oa]|cantor[a]?|bailarin[oa]|core[óo]graf[oa]|compositor[a]?|maestr[oa]|maestrina)\b', re.I)


def _oficio(desc, ext):
    """O ofício principal: a descrição curta da Wikipédia, ou, sem ela, o
    trecho da primeira frase depois de 'é um/foi uma'."""
    if (desc or '').strip():
        return desc.lower()
    primeira = re.split(r'(?<=[.!?])\s', ext or '', 1)[0] if ext else ''
    m = re.search(r'\b(?:é|foi|era)\s+(?:um|uma)\s+(.*)$', primeira)
    return (m.group(1) if m else '').lower()


def _fora_das_artes(oficio):
    """O ofício começa fora das artes e é mais de fora do que de dentro
    ('monge beneditino e padre, escritor, poeta'; 'política brasileira';
    'engenheiro, arquiteto, arqueólogo e escritor'). 'Advogado, poeta,
    radialista, compositor e ator' (Mário Lago) continua aceito."""
    f = FORA_ARTES.search(oficio)
    if not f:
        return False
    a = ARTES.search(oficio)
    if a and a.start() < f.start():
        return False
    return len(FORA_ARTES.findall(oficio)) >= len(ARTES.findall(oficio))


def _combina_com_acervo(funcoes, texto):
    """Sem função de ficha no acervo, ou com ao menos uma que tenha palavra
    compatível no texto da Wikipédia."""
    regras = [rx for fs, rx in _COMPAT if any(f in fs for f in (funcoes or []))]
    if not regras:
        return None   # o acervo não diz nada: não decide
    return any(re.search(rx, texto, re.I) for rx in regras)


def ano_da_morte(ext):
    """O ano da morte no primeiro parêntese do resumo ('(Lisboa, 1869 — São
    Paulo, 1940)'); None para quem está vivo ou quando o texto não diz."""
    m = re.match(r'[^(]*\(([^()]*)\)', ext or '')
    if not m:
        return None
    partes = re.split(r'\s[–—]\s|[–—]', m.group(1))
    if len(partes) < 2:
        return None
    anos = re.findall(r'\b(\d{4})\b', partes[-1])
    return int(anos[-1]) if anos else None


def aceita(pg, aparicoes, funcoes=None, convidado_em=None):
    """convidado_em: o ano mais recente em que o verbete foi convidado de um
    episódio. Quem morreu antes disso não é a mesma pessoa (12/10/2026)."""
    if 'missing' in pg or 'invalid' in pg:
        return None
    desc = (pg.get('description') or '').lower()
    ext = (pg.get('extract') or '').strip()
    morte = ano_da_morte(ext)
    if morte and convidado_em and convidado_em > morte + 1:
        return None
    primeira = re.split(r'(?<=[.!?])\s', ext, 1)[0].lower() if ext else ''
    oficio = _oficio(pg.get('description') or '', ext)
    combina = _combina_com_acervo(funcoes, (pg.get('description') or '') + ' ' + ext)
    # de fora das artes: só passa se o acervo der uma função que o texto da
    # Wikipédia confirma (Gabriel Chalita, "político", escreve as peças citadas)
    if _fora_das_artes(oficio) and not combina:
        return None
    # ofício periférico (apresentadora de TV, humorista, jornalista) que não
    # combina com a função de ficha do acervo: é homônimo
    if combina is False and not PALCO.search(oficio):
        return None
    # a descrição curta (ou a primeira frase) diz o que a página é: se fala de
    # coisa e não de gente, fora
    if NAO_PESSOA.search(desc) and not _fala_de_gente(desc):
        return None
    if not desc and NAO_PESSOA.search(primeira) and not _fala_de_gente(primeira):
        return None
    if 'desambigua' in desc or 'desambigua' in ext.lower()[:200] or 'pode referir-se' in ext.lower()[:200]:
        return None
    if not ARTES.search(desc + ' ' + ext):
        return None
    if not (BRASIL.search(desc + ' ' + ext) or aparicoes >= 5):
        return None
    foto = (pg.get('thumbnail') or {}).get('source', '')
    # a API devolve o arquivo original quando ele é pequeno (thumbnail_unscaled),
    # e esse caminho é limitado por IP (429). Guarda sempre a miniatura de 500 px.
    foto = re.sub(r'^https?://upload\.wikimedia\.org/wikipedia/([a-z]+)/([0-9a-f])/([0-9a-f]{2})/([^/?]+)(\?.*)?$',
                  lambda m: f'https://thumb.wikimedia.org/wikipedia/{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{m.group(4)}/500px-{m.group(4)}' + ('.png' if m.group(4).lower().endswith('.svg') else ''),
                  foto)
    arq = pg.get('pageimage') or ''
    # só o Commons (12/10/2026): o envio local da pt.wikipedia é uso justo
    # restrito à própria Wikipédia, e a página do arquivo no Commons dava 404
    if foto and '/wikipedia/commons/' not in foto:
        foto, arq = '', ''
    return {'titulo': pg.get('title', ''), 'url': pg.get('fullurl') or ('https://pt.wikipedia.org/wiki/' + urllib.parse.quote(pg.get('title', '').replace(' ', '_'))),
            'descricao': pg.get('description') or '', 'resumo': re.sub(r'\s+', ' ', ext)[:600],
            'foto': foto, 'fotoPagina': ('https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(arq.replace(' ', '_'))) if (arq and foto) else ''}


# ---- licença da foto (auditoria de 12/10/2026). CC BY e CC BY-SA pedem
# autor, fonte e licença com link; o verbete dizia só "Foto: Wikimedia
# Commons". Licença livre conhecida: Creative Commons de uso comercial e
# derivado (BY, BY-SA, CC0), domínio público e as licenças livres antigas do
# Commons (GFDL, Free Art, "Attribution"). O resto (ou nada) tira a foto.
LIVRE = re.compile(r'^(?:cc[ -]?by(?:[ -]?sa)?(?:[ -][\d.]+)?(?:[ -][a-z]{2,})?|cc0(?:[ -][\d.]+)?|public domain|'
                   r'dom[íi]nio p[úu]blico|pd(?:[ -].*)?|gfdl(?:[ -].*)?|fal|free art license|attribution|'
                   r'copyrighted free use|no restrictions)$', re.I)


def _arquivo_da_foto(foto):
    """'Fulano.jpg' a partir da miniatura (ou do arquivo original) do Commons;
    None se não for do Commons."""
    m = (re.search(r'/wikipedia/commons/thumb/[0-9a-f]/[0-9a-f]{2}/([^/?]+)/', foto or '')
         or re.search(r'/wikipedia/commons/[0-9a-f]/[0-9a-f]{2}/([^/?]+)(?:\?|$)', foto or ''))
    return urllib.parse.unquote(m.group(1)).replace('_', ' ') if m else None


def _texto(html):
    import html as _h
    t = _h.unescape(re.sub(r'<[^>]+>', ' ', html or ''))
    return re.sub(r'\s+', ' ', t).strip(' ,;')[:120].strip(' ,;')


def autor_limpo(t):
    """Autor do Commons sem o ruído da página ('( talk )', 'Unknown Unknown')."""
    t = re.sub(r'\(\s*(?:talk|discussão|contribs?)\s*\)', '', t or '', flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip(' ,;:')
    if re.match(r'^(?:unknown|desconhecid[oa]|autor desconhecido)\b', t, re.I):
        return 'autor desconhecido'
    return t


def licencas(arquivos):
    """{arquivo: {'autor', 'licenca', 'licencaUrl', 'pagina'} ou None} pela API do
    Commons, 40 arquivos por pedido, com User-Agent e pausa."""
    out = {}
    arquivos = sorted(set(a for a in arquivos if a))
    for i in range(0, len(arquivos), 40):
        grupo = arquivos[i:i + 40]
        q = urllib.parse.urlencode({
            'action': 'query', 'prop': 'imageinfo', 'iiprop': 'extmetadata|url',
            'iiextmetadatafilter': 'Artist|LicenseShortName|LicenseUrl|NonFree|Credit',
            'titles': '|'.join('File:' + a for a in grupo), 'format': 'json', 'maxlag': 5})
        req = urllib.request.Request('https://commons.wikimedia.org/w/api.php?' + q, headers={'User-Agent': UA})
        d = None
        for tentativa in range(4):
            try:
                with urllib.request.urlopen(req, timeout=40) as r:
                    d = json.load(r)
                if 'error' in d and d['error'].get('code') == 'maxlag':
                    d = None; time.sleep(5 * (tentativa + 1)); continue
                break
            except urllib.error.HTTPError as e:
                # 429: a Wikimedia pede calma; espera o que ela mandar
                espera = int(e.headers.get('Retry-After') or 0) if e.code == 429 else 0
                time.sleep(max(espera, 15 * (tentativa + 1)))
            except Exception:
                time.sleep(8 * (tentativa + 1))
        if not d:
            continue   # sem resposta: não decide nada sobre esses arquivos
        mapa = {x['from']: x['to'] for x in d.get('query', {}).get('normalized', [])}
        por_titulo = {pg.get('title'): pg for pg in d.get('query', {}).get('pages', {}).values()}
        for a in grupo:
            t = 'File:' + a
            pg = por_titulo.get(mapa.get(t, t))
            if pg is None:
                continue   # a resposta não trouxe o arquivo: não decide nada
            ii = (pg.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata') or {}
            lic = _texto((em.get('LicenseShortName') or {}).get('value', ''))
            nonfree = str((em.get('NonFree') or {}).get('value', '')).strip().lower() in ('true', '1', 'yes')
            # imagerepository 'local' é o próprio Commons; 'shared' ou vazio é arquivo que não está lá
            if 'missing' in pg or pg.get('imagerepository') not in ('local',) or nonfree or not LIVRE.match(lic):
                out[a] = None
                continue
            out[a] = {'autor': autor_limpo(_texto((em.get('Artist') or {}).get('value', ''))),
                      'licenca': lic,
                      'licencaUrl': (em.get('LicenseUrl') or {}).get('value', '').replace('http://', 'https://'),
                      'pagina': ii.get('descriptionurl') or ('https://commons.wikimedia.org/wiki/' + urllib.parse.quote(t.replace(' ', '_')))}
        time.sleep(3)
    return out


def aplica_licencas(itens):
    """Para cada verbete com foto: guarda autor e licença ou tira a foto."""
    alvo = {}
    for sp, v in itens:
        if v.get('foto'):
            alvo.setdefault(_arquivo_da_foto(v['foto']), []).append(v)
    tiradas = 0
    sem_arquivo = alvo.pop(None, [])
    for v in sem_arquivo:   # não é do Commons (envio local da pt.wikipedia)
        for k in ('foto', 'fotoPagina', 'fotoAutor', 'fotoLicenca', 'fotoLicencaUrl'):
            v.pop(k, None)
        tiradas += 1
    res = licencas(list(alvo))
    for arq, vs in alvo.items():
        if arq not in res:
            continue   # a API não respondeu: fica como estava, sem crédito (o build não usa)
        info = res[arq]
        for v in vs:
            if info is None:
                for k in ('foto', 'fotoPagina', 'fotoAutor', 'fotoLicenca', 'fotoLicencaUrl'):
                    v.pop(k, None)
                tiradas += 1
            else:
                v['fotoPagina'] = info['pagina']
                v['fotoAutor'], v['fotoLicenca'], v['fotoLicencaUrl'] = info['autor'], info['licenca'], info['licencaUrl']
    return tiradas


def _foto_no_ar(url):
    """A miniatura ainda existe no Wikimedia Commons? Arquivo apagado ou
    renomeado responde 404 e deixava ícone de imagem quebrada no verbete, na
    vitrine e no compartilhamento (Myra Ruiz e Diego Martins, auditoria de
    10/10/2026). Só 404 e 410 derrubam a foto: limite de pedidos (429) ou
    rede fora do ar não dizem nada sobre o arquivo."""
    if not url:
        return True
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=20):
            return True
    except urllib.error.HTTPError as e:
        return e.code not in (404, 410)
    except Exception:
        return True


def _ano_convidado(p):
    anos = [int(a['data'][:4]) for a in (p or {}).get('aparicoes', [])
            if a.get('papel') == 'convidado' and (a.get('data') or '')[:4].isdigit()]
    return max(anos) if anos else None


def revalidar():
    arq = f'{ROOT}/import/enciclopedia-wiki.json'
    wiki = json.load(open(arq))
    enc = json.load(open(f'{ROOT}/import/enciclopedia.json'))['pessoas']
    fora = 0
    for sp, v in list(wiki.items()):
        if not v.get('url'):
            continue
        pg = {'title': v.get('titulo', ''), 'description': v.get('descricao', ''), 'extract': v.get('resumo', ''),
              'thumbnail': {'source': v.get('foto', '')} if v.get('foto') else None, 'fullurl': v.get('url', '')}
        # a regra de homônimo (12/10/2026) compara com as funções do acervo, e a
        # lista à mão "wiki_nao" das regras vale sempre. A contagem de
        # aparições não entra aqui: a limpeza do acervo baixou a conta de
        # muita gente de fora do Brasil (Jean Cocteau) abaixo das 5 que a
        # primeira consulta exigia, e isso não faz da página outra pessoa.
        if sp in WIKI_NAO or not aceita(pg, 999, enc.get(sp, {}).get('funcoes'), _ano_convidado(enc.get(sp))):
            print('  fora:', sp, '|', v.get('descricao', '')[:60])
            wiki[sp] = {'nao': True, 'quando': v.get('quando', '')}
            fora += 1
    json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
    print(f'revalidação: {fora} verbete(s) perderam a página da Wikipédia')


def revisa_licencas():
    """Autor e licença de todas as fotos já salvas; tira as que não são
    livres ou não estão no Commons (12/10/2026)."""
    arq = f'{ROOT}/import/enciclopedia-wiki.json'
    wiki = json.load(open(arq))
    itens = [(sp, v) for sp, v in wiki.items() if v.get('foto')]
    print(f'{len(itens)} foto(s) para conferir')
    tiradas = aplica_licencas(itens)
    json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
    print(f'licenças: {sum(1 for v in wiki.values() if v.get("fotoLicenca"))} foto(s) com autor e licença; '
          f'{tiradas} tirada(s) por não serem livres ou não estarem no Commons')


def main():
    if '--revalidar' in sys.argv:
        return revalidar()
    if '--licencas' in sys.argv:
        return revisa_licencas()
    todos = '--todos' in sys.argv
    limite = int(sys.argv[sys.argv.index('--limite') + 1]) if '--limite' in sys.argv else 0
    enc = json.load(open(f'{ROOT}/import/enciclopedia.json'))['pessoas']
    arq = f'{ROOT}/import/enciclopedia-wiki.json'
    try:
        wiki = json.load(open(arq))
    except Exception:
        wiki = {}
    # equipe e colunistas: bio própria, não passam pela Wikipédia
    fora = set()
    for f, chave in (('equipe.json', 'usuarios'), ('opiniao.json', 'colunistas')):
        try:
            for u in json.load(open(f'{ROOT}/import/{f}')).get(chave, []):
                fora.add(re.sub(r'[^a-z0-9]+', '-', __import__('unicodedata').normalize('NFKD', u.get('nome', '')).encode('ascii', 'ignore').decode().lower()).strip('-'))
        except Exception:
            pass
    agora = datetime.now(timezone.utc)
    limite_data = (agora - timedelta(days=90)).isoformat()
    pend = []
    for sp, p in sorted(enc.items(), key=lambda x: -len(x[1]['aparicoes'])):
        if sp in fora:
            continue
        if sp in WIKI_NAO:
            wiki[sp] = {'nao': True, 'quando': agora.isoformat()}
            continue
        w = wiki.get(sp)
        if w and not todos and (w.get('quando', '') > limite_data or w.get('url')):
            continue
        pend.append((sp, p['nome'], len(p['aparicoes']), p.get('funcoes') or [], _ano_convidado(p)))
    if limite:
        pend = pend[:limite]
    print(f'{len(pend)} verbete(s) para consultar')
    achados = 0
    for i in range(0, len(pend), 20):
        grupo = pend[i:i + 20]
        d = lote([x[1] for x in grupo])
        if not d:
            print('  (sem resposta; segue)'); continue
        # normalização/redirect: título pedido -> título devolvido
        mapa = {}
        for x in (d.get('query', {}).get('normalized', []) + d.get('query', {}).get('redirects', [])):
            mapa[x['from']] = x['to']
        por_titulo = {pg.get('title'): pg for pg in d.get('query', {}).get('pages', {}).values()}
        aceitos = []
        for sp, nome, n, funcoes, conv_ano in grupo:
            t = nome
            while t in mapa:
                t = mapa[t]
            pg = por_titulo.get(t)
            res = aceita(pg, n, funcoes, conv_ano) if pg else None
            # Duas guardas de precisão (06/10/2026), depois de Thales Bretas sair
            # com a página do Paulo Gustavo: (a) o título devolvido tem de ter ao
            # menos uma palavra em comum com o nome pedido (redirecionamento para
            # outra pessoa não passa); (b) a mesma página da Wikipédia não serve
            # para dois verbetes (o segundo é homônimo ou grafia alternativa, e
            # se for a mesma pessoa a junção é feita em 'apelidos', não aqui).
            if res and sp not in WIKI_OK and not _palavras_em_comum(nome, res.get('titulo', '')):
                print(f'  fora (título sem relação): {sp} -> {res.get("titulo")}')
                res = None
            if res and any(v.get('url') == res['url'] for k, v in wiki.items() if k != sp):
                print(f'  fora (página já é de outro verbete): {sp} -> {res.get("titulo")}')
                res = None
            if res and res.get('foto') and not _foto_no_ar(res['foto']):
                print(f'  foto fora do ar (fica sem foto): {sp} -> {res["foto"]}')
                res['foto'], res['fotoPagina'] = '', ''
            if res:
                res['quando'] = agora.isoformat(); wiki[sp] = res; achados += 1
                aceitos.append((sp, res))
            else:
                wiki[sp] = {'nao': True, 'quando': agora.isoformat()}
        # autor e licença das fotos novas; a que não for livre sai (12/10/2026)
        aplica_licencas(aceitos)
        json.dump(wiki, open(arq, 'w'), ensure_ascii=False, indent=1)
        print(f'  {min(i + 20, len(pend))}/{len(pend)} · com página: {achados}', flush=True)
        time.sleep(3)
    print(f'pronto: {achados} verbete(s) com bio da Wikipédia nesta rodada; total no arquivo: {sum(1 for v in wiki.values() if v.get("url"))}')


if __name__ == '__main__':
    main()
