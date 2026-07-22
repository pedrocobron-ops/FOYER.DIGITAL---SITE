#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redação de agentes de IA do FOYER.

Esteira: Pauteiro (varredura na web) → Repórter (apura e escreve) →
Editor de Estilo (lapida o texto) → Chefe de Redação (valida) →
Mesa de Aprovação da Coxia (humano aprova antes de publicar).

As matérias produzidas vão para import/pauta/*.json com status
"aguardando_aprovacao" — NADA é publicado sem aprovação humana na Coxia.

Uso (normalmente via GitHub Actions):
    ANTHROPIC_API_KEY=... python3 tools/redacao.py [quantidade] [editoria]
"""
import os, sys, json, re, unicodedata
from datetime import datetime, timezone

import anthropic

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "claude-opus-4-8"
QTD = int(sys.argv[1]) if len(sys.argv) > 1 else 2
EDITORIA = sys.argv[2] if len(sys.argv) > 2 else ""

client = anthropic.Anthropic()

EDITORIAS = ["Teatro", "Cinema", "Música", "Dança", "Crítica", "Notícia",
             "Televisão", "Streaming", "Literatura", "Exposições", "Show",
             "Audições", "Edital", "Festa", "Programa"]

ESTILO_FOYER = """Você trabalha na redação do FOYER (foyer.digital), portal
brasileiro de jornalismo cultural dedicado a teatro, música e artes.
Estilo da casa: jornalismo cultural profissional em português do Brasil;
títulos informativos e diretos (sem caça-clique); lide que responde o quê,
quem, quando e onde; parágrafos curtos; serviço completo ao final quando
houver evento (local, datas, horários, ingressos); nunca inventar fatos,
aspas ou dados — tudo deve vir das fontes apuradas."""


def falar(rotulo, msg):
    print(f"[{rotulo}] {msg}", flush=True)


def extrair_json(texto):
    """Extrai o primeiro bloco JSON válido de uma resposta."""
    m = re.search(r'```(?:json)?\s*([\[{].*?[\]}])\s*```', texto, re.S)
    if m:
        return json.loads(m.group(1))
    m = re.search(r'([\[{].*[\]}])', texto, re.S)
    if m:
        return json.loads(m.group(1))
    raise ValueError("resposta sem JSON")


def texto_da(resp):
    return "\n".join(b.text for b in resp.content if b.type == "text")


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:80]


def titulos_recentes():
    """Títulos já publicados/pauta — para o Pauteiro não repetir assunto."""
    vistos = []
    try:
        idx = json.load(open(f'{ROOT}/import/materias.json'))
        vistos += [p['title'] for p in idx[:60]]
    except Exception:
        pass
    for pasta in ('import/pauta', 'import/novas'):
        d = os.path.join(ROOT, pasta)
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith('.json'):
                    try:
                        vistos.append(json.load(open(os.path.join(d, f)))['title'])
                    except Exception:
                        pass
    return vistos


# ------------------------------------------------------------------ agentes

def pauteiro(qtd, editoria, ja_cobertos):
    """Varre a web atrás de notícias de teatro/cultura no Brasil e propõe pautas."""
    foco = f"da editoria {editoria}" if editoria else "de teatro, música, dança e cultura"
    pedido = f"""Você é o Pauteiro do FOYER. Faça uma varredura na web AGORA em
busca de notícias RECENTES (últimos 7 dias) {foco} no Brasil: estreias,
temporadas, elencos anunciados, editais, premiações, festivais, turnês.

Evite assuntos que o FOYER já cobriu recentemente:
{chr(10).join('- ' + t for t in ja_cobertos[:40])}

Escolha as {qtd} melhores pautas — relevantes, verificáveis e com fontes
confiáveis. Responda SOMENTE com JSON:
[{{"assunto": "...", "resumo": "o que aconteceu, com fatos e datas",
   "editoria": "uma de: {', '.join(EDITORIAS)}",
   "fontes": ["url1", "url2"]}}]"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=ESTILO_FOYER,
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 8,
                "user_location": {"type": "approximate", "country": "BR",
                                  "timezone": "America/Sao_Paulo"}}],
        messages=[{"role": "user", "content": pedido}],
    )
    pautas = extrair_json(texto_da(resp))
    falar("Pauteiro", f"{len(pautas)} pauta(s) levantada(s)")
    return pautas[:qtd]


def reporter(pauta):
    """Apura a pauta na web e escreve a matéria completa."""
    pedido = f"""Você é repórter do FOYER, cobrindo a editoria {pauta['editoria']}.
Apure e escreva uma matéria completa sobre esta pauta:

ASSUNTO: {pauta['assunto']}
RESUMO DA PAUTA: {pauta['resumo']}
FONTES INICIAIS: {', '.join(pauta.get('fontes', []))}

Use a busca na web para confirmar os fatos e colher detalhes (datas, locais,
nomes completos, valores de ingresso, declarações públicas). NUNCA invente
nada — se um dado não estiver nas fontes, não o afirme.

Formato do corpo (formato da Coxia): parágrafos separados por linha em
branco; "## " para intertítulo; "> " para citação textual REAL de fonte
pública (com atribuição no texto); **negrito** para nomes de obras.
Entre 400 e 700 palavras, com bloco de serviço ao final se houver evento.

Responda SOMENTE com JSON:
{{"title": "título da matéria", "corpo": "texto no formato acima",
  "cat": "{pauta['editoria']}", "fontes": ["urls efetivamente usadas"]}}"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=ESTILO_FOYER,
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 6,
                "user_location": {"type": "approximate", "country": "BR",
                                  "timezone": "America/Sao_Paulo"}}],
        messages=[{"role": "user", "content": pedido}],
    )
    m = extrair_json(texto_da(resp))
    falar("Repórter", f"matéria escrita: {m['title'][:60]}")
    return m


def editor_estilo(materia):
    """Lapida o texto: ritmo, clareza e o padrão editorial do FOYER."""
    pedido = f"""Você é o Editor de Estilo do FOYER. Revise a matéria abaixo:
melhore ritmo e clareza, elimine repetições e clichês, confira concordância
e padronize no estilo da casa. NÃO acrescente fatos novos nem remova
informações; preserve o formato (## intertítulo, > citação, **negrito**).

TÍTULO: {materia['title']}
CORPO:
{materia['corpo']}

Responda SOMENTE com JSON: {{"title": "...", "corpo": "..."}}"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=ESTILO_FOYER,
        messages=[{"role": "user", "content": pedido}],
    )
    rev = extrair_json(texto_da(resp))
    materia.update(title=rev['title'], corpo=rev['corpo'])
    falar("Editor de Estilo", "texto lapidado")
    return materia


def chefe_redacao(materia):
    """Validação final: fatos ancorados nas fontes, título fiel, padrão ok."""
    pedido = f"""Você é o Chefe de Redação do FOYER. Avalie a matéria:

TÍTULO: {materia['title']}
EDITORIA: {materia['cat']}
FONTES: {', '.join(materia.get('fontes', []))}
CORPO:
{materia['corpo']}

Verifique: (1) o título é fiel ao conteúdo, sem sensacionalismo;
(2) nenhuma afirmação parece inventada ou sem fonte; (3) datas e nomes são
consistentes; (4) o texto está completo e publicável.

Responda SOMENTE com JSON:
{{"aprovado": true/false, "nota": 0-10,
  "parecer": "avaliação em 1-2 frases para o editor humano",
  "ressalvas": ["pontos que o humano deve conferir antes de publicar"]}}"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=ESTILO_FOYER,
        messages=[{"role": "user", "content": pedido}],
    )
    parecer = extrair_json(texto_da(resp))
    falar("Chefe de Redação", f"nota {parecer.get('nota')} — {'aprovada para a mesa' if parecer.get('aprovado') else 'REPROVADA'}")
    return parecer


# ------------------------------------------------------------------ esteira

def main():
    os.makedirs(f'{ROOT}/import/pauta', exist_ok=True)
    ja = titulos_recentes()
    pautas = pauteiro(QTD, EDITORIA, ja)
    geradas = 0

    for pauta in pautas:
        try:
            materia = reporter(pauta)
            materia = editor_estilo(materia)
            parecer = chefe_redacao(materia)

            slug = slugify(materia['title'])
            pacote = {
                "title": materia['title'],
                "slug": slug,
                "cat": materia.get('cat', pauta['editoria']),
                "author": "Redação Foyer",
                "img": "",
                "corpo": materia['corpo'],
                "fontes": materia.get('fontes', []),
                "status": "aguardando_aprovacao",
                "chefe": parecer,
                "geradoEm": datetime.now(timezone.utc).isoformat(),
                "esteira": "pauteiro > reporter > editor-estilo > chefe-redacao",
            }
            destino = f'{ROOT}/import/pauta/{slug}.json'
            json.dump(pacote, open(destino, 'w'), ensure_ascii=False, indent=1)
            geradas += 1
            falar("Esteira", f"na mesa de aprovação: {slug}")
        except Exception as e:
            falar("Esteira", f"pauta descartada ({pauta.get('assunto','?')[:40]}): {e}")

    falar("Esteira", f"{geradas} matéria(s) aguardando aprovação humana na Coxia")


if __name__ == "__main__":
    main()
