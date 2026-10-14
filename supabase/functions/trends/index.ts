// O RADAR DE PAUTA: "Em alta agora no Brasil" (14/10/2026)
//
// POR QUE ISTO EXISTE. O Google Trends publica um RSS público com o que o país
// mais busca neste momento (trends.google.com/trending/rss?geo=BR), com o
// termo, o tráfego aproximado e as notícias mais citadas sobre ele. A Coxia
// quer mostrar isso no Palco e ao lado de quem escreve, marcando o que bate com
// a enciclopédia da casa. Só que o navegador não consegue ler esse RSS direto:
// o Google não manda os cabeçalhos de CORS. Então quem lê é este servidor, que
// devolve JSON com os cabeçalhos certos.
//
// O QUE ELE NÃO FAZ. Não usa segredo nenhum (o dado é público), não grava nada
// em lugar nenhum e não lê o banco. Guarda a última resposta em memória por dez
// minutos, para a redação inteira recarregar a Coxia sem bater no Google a cada
// vez. Se o Google falhar, devolve a última leitura que tiver, avisando que é
// antiga; sem leitura nenhuma, devolve erro, e a Coxia mostra "o radar não
// respondeu" e segue funcionando.
//
// Este arquivo é a fonte da verdade da função. Para publicar (quem publica é o
// Pedro; este arquivo foi só escrito, não implantado):
//   supabase functions deploy trends --no-verify-jwt
// (verify_jwt desligado de propósito: a Coxia chama sem sessão do Supabase,
// o dado é público e a função não grava nada.)

const FONTE = 'https://trends.google.com/trending/rss?geo=BR';
const VALIDADE_MS = 10 * 60 * 1000;   // dez minutos de cache em memória
const MAX_ITENS = 20;                  // a Coxia mostra 10; sobra margem para filtrar

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

type Noticia = { titulo: string; url: string; fonte: string };
type Item = { termo: string; trafego: string; noticias: Noticia[] };
type Leitura = { atualizado: string; itens: Item[] };

// a última leitura boa, enquanto o processo viver; cada instância tem a sua
let cache: { em: number; leitura: Leitura } | null = null;

const devolve = (corpo: unknown, status = 200, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(corpo), {
    status,
    headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8', ...extra },
  });

// o RSS do Google é simples e previsível; um leitor por expressão regular
// basta e evita depender de biblioteca de XML no servidor
function texto(bloco: string, tag: string): string {
  const m = bloco.match(new RegExp(`<${tag}(?:\\s[^>]*)?>([\\s\\S]*?)</${tag}>`));
  return m ? limpa(m[1]) : '';
}
function limpa(s: string): string {
  return s
    .replace(/^\s*<!\[CDATA\[([\s\S]*?)\]\]>\s*$/, '$1')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'").replace(/&#39;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ').trim();
}
function numero(trafego: string): number {
  const n = parseInt(trafego.replace(/[^\d]/g, ''), 10);
  return Number.isFinite(n) ? n : 0;
}

function interpreta(xml: string): Item[] {
  const itens: Item[] = [];
  for (const m of xml.matchAll(/<item>([\s\S]*?)<\/item>/g)) {
    const bloco = m[1];
    const termo = texto(bloco, 'title');
    if (!termo) continue;
    const noticias: Noticia[] = [];
    for (const n of bloco.matchAll(/<ht:news_item>([\s\S]*?)<\/ht:news_item>/g)) {
      const url = texto(n[1], 'ht:news_item_url');
      if (!/^https?:\/\//i.test(url)) continue;
      noticias.push({ titulo: texto(n[1], 'ht:news_item_title'), url, fonte: texto(n[1], 'ht:news_item_source') });
      if (noticias.length >= 3) break;
    }
    itens.push({ termo, trafego: texto(bloco, 'ht:approx_traffic'), noticias });
  }
  // o RSS vem por ordem de chegada; "em alta" é por tráfego, do maior para o menor
  itens.sort((a, b) => numero(b.trafego) - numero(a.trafego));
  return itens.slice(0, MAX_ITENS);
}

async function leGoogle(): Promise<Leitura> {
  const r = await fetch(FONTE, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; radar-foyer/1.0; +https://foyer.digital)', 'Accept': 'application/rss+xml, application/xml, text/xml' },
    signal: AbortSignal.timeout(8000),
  });
  if (!r.ok) throw new Error(`google ${r.status}`);
  const itens = interpreta(await r.text());
  if (!itens.length) throw new Error('rss sem itens');
  return { atualizado: new Date().toISOString(), itens };
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
  if (req.method !== 'GET') return devolve({ erro: 'só GET' }, 405);

  const agora = Date.now();
  if (cache && agora - cache.em < VALIDADE_MS) {
    return devolve({ ...cache.leitura, cache: true }, 200, { 'Cache-Control': 'public, max-age=600' });
  }
  try {
    const leitura = await leGoogle();
    cache = { em: agora, leitura };
    return devolve(leitura, 200, { 'Cache-Control': 'public, max-age=600' });
  } catch (e) {
    // sem Google agora: a última leitura boa, marcada como antiga, vale mais que nada
    if (cache) return devolve({ ...cache.leitura, antigo: true }, 200, { 'Cache-Control': 'no-store' });
    return devolve({ erro: 'o radar não respondeu', detalhe: String((e as Error)?.message || e) }, 502, { 'Cache-Control': 'no-store' });
  }
});
