// A CHAVE DA CASA — o porteiro da Coxia
//
// Até aqui, a chave de publicação do GitHub morava no navegador de cada pessoa,
// e cada computador precisava da sua cópia. Com três pessoas e quatro máquinas,
// isso virou mandar senha por mensagem, que é insustentável e inseguro. Agora a
// chave mora no banco, o chefe a guarda UMA VEZ, e quem grava no site é este
// servidor. Ninguém mais cola chave em navegador nenhum, e a chave nunca sai
// daqui: o navegador recebe o resultado da gravação, nunca o segredo.
//
// verify_jwt fica desligado de propósito: a equipe da Coxia não é usuária do
// Supabase Auth. Quem autentica é este arquivo, com a senha da própria pessoa
// conferida contra import/equipe.json e uma sessão de prazo curto.
//
// Este arquivo é a fonte da verdade da função. Para publicar uma alteração:
//   supabase functions deploy coxia --no-verify-jwt

import { createClient } from 'jsr:@supabase/supabase-js@2';

const DONO = 'pedrocobron-ops';
const REPO = 'FOYER.DIGITAL---SITE';
const RAMO = 'claude/foyer-digital-redesign-14l2b6';
const PREFIXO = `/repos/${DONO}/${REPO}/`;
const DIAS_DE_SESSAO = 7;
const FALHAS_ATE_TRANCAR = 10;

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Expose-Headers': 'x-coxia-erro, x-gh-remaining',
};
const devolve = (corpo: unknown, status = 200, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(corpo), {
    status,
    headers: { ...cors, ...extra, 'Content-Type': 'application/json' },
  });

const db = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  { auth: { persistSession: false } },
);

const hex = (b: ArrayBuffer) =>
  Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, '0')).join('');

async function sha256(txt: string) {
  return hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(txt)));
}

async function pbkdf2(senha: string, saltHex: string, iter: number) {
  const salt = new Uint8Array((saltHex.match(/.{2}/g) || []).map((h) => parseInt(h, 16)));
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(senha), 'PBKDF2', false, ['deriveBits']);
  return hex(await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: iter, hash: 'SHA-256' }, k, 256));
}

// a mesma conferência que a Coxia faz no navegador, inclusive o formato antigo
async function senhaConfere(u: Record<string, string>, senha: string) {
  if (u.kdf === 'pbkdf2') return (await pbkdf2(senha, u.salt || '', Number(u.iter) || 210000)) === u.hash;
  return (await sha256((u.salt || '') + ':' + senha)) === u.hash;
}

// a equipe vem do próprio repositório: é o mesmo arquivo que a Coxia edita, então
// tirar alguém da equipe tira o acesso, sem precisar mexer aqui
async function equipe() {
  const r = await fetch(
    `https://raw.githubusercontent.com/${DONO}/${REPO}/${RAMO}/import/equipe.json`,
    { headers: { 'Cache-Control': 'no-cache' } },
  );
  if (!r.ok) throw new Error('equipe indisponível');
  const d = await r.json();
  return (d.usuarios || []) as Record<string, string>[];
}

async function chaveDaCasa(): Promise<string | null> {
  const { data } = await db.from('coxia_segredo').select('chave').eq('id', 'github').maybeSingle();
  return data?.chave ?? null;
}

async function quemE(sessao: string) {
  if (!sessao) return null;
  const { data } = await db.from('coxia_sessao').select('*').eq('token', sessao).maybeSingle();
  if (!data) return null;
  if (new Date(data.expira_em).getTime() < Date.now()) {
    await db.from('coxia_sessao').delete().eq('token', sessao);
    return null;
  }
  await db.from('coxia_sessao').update({ ultimo_uso: new Date().toISOString() }).eq('token', sessao);
  return data;
}

async function anota(u: Record<string, string> | null, acao: string, caminho: string, resultado: number) {
  await db.from('coxia_registro').insert({
    usuario_id: u?.usuario_id ?? null, nome: u?.nome ?? null, acao, caminho, resultado,
  });
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return devolve({ erro: 'método não aceito' }, 405);

  let corpo: Record<string, unknown> = {};
  try { corpo = await req.json(); } catch { return devolve({ erro: 'corpo inválido' }, 400); }
  const acao = String(corpo.acao || '');

  try {
    // ---------- entrar: a senha da pessoa vira sessão ----------
    if (acao === 'entrar') {
      const id = String(corpo.id || '').trim();
      const senha = String(corpo.senha || '');
      if (!id || !senha) return devolve({ erro: 'faltou usuário ou senha' }, 400);

      // trava simples contra força bruta: 10 erros em 15 minutos e a porta fecha
      const desde = new Date(Date.now() - 15 * 60000).toISOString();
      const { count } = await db.from('coxia_registro').select('id', { count: 'exact', head: true })
        .eq('usuario_id', id).eq('acao', 'entrar-negado').gte('quando', desde);
      if ((count ?? 0) >= FALHAS_ATE_TRANCAR) {
        return devolve({ erro: 'Muitas tentativas seguidas. Espere 15 minutos.' }, 429);
      }

      const u = (await equipe()).find((x) => x.id === id);
      if (!u || !(await senhaConfere(u, senha))) {
        await db.from('coxia_registro').insert({ usuario_id: id, acao: 'entrar-negado', resultado: 401 });
        return devolve({ erro: 'Usuário ou senha não conferem' }, 401);
      }

      const token = hex(crypto.getRandomValues(new Uint8Array(32)).buffer);
      const expira = new Date(Date.now() + DIAS_DE_SESSAO * 864e5).toISOString();
      await db.from('coxia_sessao').insert({
        token, usuario_id: u.id, nome: u.nome, papel: u.papel, expira_em: expira,
      });
      return devolve({
        sessao: token, expira_em: expira,
        usuario: { id: u.id, nome: u.nome, papel: u.papel },
        chaveDaCasa: !!(await chaveDaCasa()),
      });
    }

    // daqui para baixo, tudo exige sessão. O cabeçalho x-coxia-erro existe para a
    // Coxia distinguir "a sua sessão morreu" de "o GitHub recusou", que sem ele
    // seriam os dois um 401 igual.
    const u = await quemE(String(corpo.sessao || ''));
    if (!u) return devolve({ erro: 'sessao-invalida' }, 401, { 'x-coxia-erro': 'sessao' });

    // ---------- estado: existe chave da casa? ela ainda vale? ----------
    if (acao === 'estado') {
      const { data } = await db.from('coxia_segredo')
        .select('guardada_em, guardada_por, fim_da_chave').eq('id', 'github').maybeSingle();
      if (!data) return devolve({ temChave: false });
      const r = await fetch(`https://api.github.com/repos/${DONO}/${REPO}`, {
        headers: { Authorization: `Bearer ${await chaveDaCasa()}`, 'User-Agent': 'coxia-foyer' },
      });
      return devolve({
        temChave: true, valendo: r.ok, http: r.status,
        guardada_em: data.guardada_em, guardada_por: data.guardada_por, fim: data.fim_da_chave,
      });
    }

    // ---------- guardar a chave: só o chefe, e só depois de o GitHub aceitar ----------
    if (acao === 'guardar') {
      if (u.papel !== 'chefe') return devolve({ erro: 'Só o chefe de redação guarda a chave da casa.' }, 403);
      const chave = String(corpo.chave || '').replace(/\s+/g, '');
      if (!chave) return devolve({ erro: 'faltou a chave' }, 400);
      const r = await fetch(`https://api.github.com/repos/${DONO}/${REPO}`, {
        headers: { Authorization: `Bearer ${chave}`, 'User-Agent': 'coxia-foyer' },
      });
      if (!r.ok) {
        await anota(u, 'guardar-negado', '', r.status);
        return devolve({ erro: 'github-recusou', http: r.status }, 400);
      }
      await db.from('coxia_segredo').upsert({
        id: 'github', chave, guardada_em: new Date().toISOString(),
        guardada_por: u.nome, fim_da_chave: chave.slice(-4),
      });
      await anota(u, 'guardar', '', 200);
      return devolve({ ok: true, fim: chave.slice(-4) });
    }

    // ---------- gh: a ponte para o GitHub, com a chave que fica aqui ----------
    if (acao === 'gh') {
      const chave = await chaveDaCasa();
      if (!chave) return devolve({ erro: 'sem-chave-da-casa' }, 409, { 'x-coxia-erro': 'sem-chave' });
      const caminho = String(corpo.caminho || '');
      // a ponte serve UM repositório. Sem isto, uma sessão roubada viraria um
      // procurador para o GitHub inteiro em nome do dono da chave.
      if (!caminho.startsWith(PREFIXO)) return devolve({ erro: 'caminho fora do repositório da casa' }, 403);
      const metodo = String(corpo.metodo || 'GET').toUpperCase();
      if (!['GET', 'PUT', 'DELETE'].includes(metodo)) return devolve({ erro: 'método não aceito' }, 400);

      const r = await fetch('https://api.github.com' + caminho, {
        method: metodo,
        headers: {
          Authorization: `Bearer ${chave}`,
          Accept: 'application/vnd.github+json',
          'User-Agent': 'coxia-foyer',
          ...(metodo === 'GET' ? {} : { 'Content-Type': 'application/json' }),
        },
        body: metodo === 'GET' ? undefined : JSON.stringify(corpo.corpo ?? {}),
      });
      const texto = await r.text();
      // gravação sempre deixa rastro: a chave é da casa, mas o autor é a pessoa
      if (metodo !== 'GET') await anota(u, metodo, caminho, r.status);
      return new Response(texto, {
        status: r.status,
        headers: {
          ...cors,
          'Content-Type': 'application/json',
          'x-gh-remaining': r.headers.get('x-ratelimit-remaining') || '',
        },
      });
    }

    // ---------- sair ----------
    if (acao === 'sair') {
      await db.from('coxia_sessao').delete().eq('token', String(corpo.sessao || ''));
      return devolve({ ok: true });
    }

    return devolve({ erro: 'ação desconhecida' }, 400);
  } catch (e) {
    return devolve({ erro: String((e as Error).message || e) }, 500);
  }
});
