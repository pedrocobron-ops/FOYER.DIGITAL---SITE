// Envia a edição da revista do FOYER aos assinantes, via Brevo.
// Chamada pela Coxia (chefe) com a chave. Requer o secret BREVO_KEY.
//
// O que mudou nesta versão, e por quê:
//
// 1. ERRO COM MOTIVO. Antes, qualquer falha virava um número: "3 falhas". Chave
//    errada, remetente não verificado e caixa cheia do destinatário produziam a
//    mesma tela, e não havia como saber o que consertar. Agora a resposta traz o
//    código HTTP e a mensagem que o Brevo devolveu, e as três falhas mais comuns
//    vêm traduzidas para português com o conserto ao lado.
//
// 2. TRAVA DE ENVIO REPETIDO. E-mail não tem botão de desfazer. Apertar "enviar"
//    duas vezes mandava a mesma edição duas vezes para a mesma pessoa. A tabela
//    foyer_revista_envio guarda o que já saiu, e a função recusa repetir a menos
//    que venha "forcar": true.
//
// 3. REMETENTE VISÍVEL NA RESPOSTA, porque é o que o Brevo mais recusa: antes de
//    o domínio estar verificado, só um e-mail verificado como remetente único
//    funciona, e isso se configura no secret REVISTA_FROM.
//
// Este arquivo é a fonte da verdade. Para publicar:
//   supabase functions deploy enviar-revista --no-verify-jwt

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const CHAVE = 'foyer-nl-terceiro-sinal-2026'
const REMETENTE_NOME = 'Revista do FOYER'
// antes do domínio verificado, aponte REVISTA_FROM para um e-mail verificado no
// Brevo; depois da verificação do domínio, revista@foyer.digital funciona sozinho
const REMETENTE_EMAIL = Deno.env.get('REVISTA_FROM') || 'revista@foyer.digital'
const BASE = Deno.env.get('FOYER_BASE') || 'https://foyer.digital'

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
}
const devolve = (corpo: unknown, status = 200) =>
  new Response(JSON.stringify(corpo), { status, headers: { ...cors, 'Content-Type': 'application/json' } })

function esc(s: string){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') }

// traduz a recusa do Brevo para uma frase que diga o que fazer
function explica(status: number, texto: string){
  const t = (texto || '').toLowerCase()
  if (status === 401) return 'O Brevo não aceitou a chave (401). Confira se o secret BREVO_KEY é uma chave da API v3 e se não veio cortada na cópia.'
  if (status === 400 && t.includes('sender')) return `O Brevo recusou o remetente ${REMETENTE_EMAIL} (400). Ele precisa estar verificado no Brevo, em Senders & IP. Enquanto o domínio não estiver verificado, aponte o secret REVISTA_FROM para um e-mail já verificado.`
  if (status === 402) return 'A conta do Brevo está sem crédito de envio (402).'
  if (status === 429) return 'O Brevo limitou o ritmo de envio (429). O plano gratuito manda 300 por dia.'
  return `O Brevo respondeu ${status}: ${String(texto || '').slice(0, 300)}`
}

function corpoEmail(ed: Record<string, unknown>, tokenLink: string){
  const numero = esc(String(ed.numero||''))
  const titulo = esc(String(ed.titulo||('Edição Nº '+numero)))
  const manchete = esc(String(ed.manchete||''))
  const capa = ed.capa ? String(ed.capa) : ''
  const url = esc(String(ed.url || (BASE + '/revista.html')))
  return `<!doctype html><html lang="pt-BR"><body style="margin:0;background:#EFE8DA;font-family:Georgia,serif;color:#1B140F">
  <div style="max-width:560px;margin:0 auto;background:#EFE8DA">
    <div style="background:#4E0F09;color:#CEB26A;padding:26px 28px;text-align:center">
      <div style="font-size:12px;letter-spacing:3px;text-transform:uppercase;color:#E9CB85;font-family:Arial,sans-serif">Revista do FOYER</div>
      <div style="font-size:34px;margin-top:6px">Edição Nº ${numero}</div>
    </div>
    ${capa ? `<a href="${url}"><img src="${esc(capa)}" alt="${titulo}" style="width:100%;display:block"></a>` : ''}
    <div style="padding:26px 28px">
      <h1 style="font-size:24px;line-height:1.2;margin:0 0 12px">${titulo}</h1>
      ${manchete ? `<p style="font-size:16px;line-height:1.6;color:#4a4030;margin:0 0 22px">${manchete}</p>` : ''}
      <a href="${url}" style="display:inline-block;background:#4E0F09;color:#CEB26A;text-decoration:none;font-family:Arial,sans-serif;font-size:14px;letter-spacing:1px;text-transform:uppercase;padding:14px 26px">Ler a edição completa</a>
    </div>
    <div style="padding:18px 28px;border-top:1px solid #D8CEB8;font-family:Arial,sans-serif;font-size:11px;color:#6B6152;line-height:1.6">
      Você recebe este e-mail porque assinou a revista do FOYER, de graça.<br>
      <a href="${BASE}/descadastrar.html?t=${encodeURIComponent(tokenLink)}" style="color:#6B6152">Descadastrar</a> · FOYER.DIGITAL, o saguão do teatro brasileiro
    </div>
  </div></body></html>`
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors })
  try {
    const body = await req.json().catch(() => ({}))
    const url = new URL(req.url)
    const chave = body.chave || url.searchParams.get('chave')
    if (chave !== CHAVE) return devolve({ erro: 'chave invalida' }, 401)

    const BREVO = Deno.env.get('BREVO_KEY')
    if (!BREVO) return devolve({ erro: 'BREVO_KEY nao configurada', pendente: true })

    const ed = body.edicao || {}
    const assunto = body.assunto || `Revista do FOYER · Edição Nº ${ed.numero || ''}`
    const teste = body.teste || null // e-mail único para teste
    const numero = String(ed.numero || '')

    const supa = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)

    // trava do envio repetido: vale só para o envio de verdade, nunca para o teste
    if (!teste && numero && !body.forcar) {
      const { data: ja } = await supa.from('foyer_revista_envio').select('quando, enviados').eq('numero', numero).maybeSingle()
      if (ja) {
        return devolve({
          jaEnviada: true, numero, quando: ja.quando, enviados: ja.enviados,
          erro: `A edição Nº ${numero} já foi enviada em ${new Date(ja.quando).toLocaleString('pt-BR')} para ${ja.enviados} assinante(s). Enviar de novo manda o mesmo e-mail outra vez para as mesmas pessoas.`,
        })
      }
    }

    let destinatarios: { email: string; nome?: string; token?: string }[] = []
    if (teste) {
      destinatarios = [{ email: String(teste).toLowerCase(), nome: 'Teste', token: 'teste' }]
    } else {
      const { data, error } = await supa.from('foyer_newsletter').select('nome,email,token').eq('ativo', true)
      if (error) throw error
      destinatarios = data || []
    }
    if (!destinatarios.length) return devolve({ ok: true, enviados: 0, aviso: 'nenhum assinante ativo' })

    let enviados = 0, falhas = 0
    let motivo = ''            // a primeira recusa, explicada
    const quemFalhou: string[] = []
    for (const d of destinatarios) {
      const html = corpoEmail(ed, d.token || '')
      const r = await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: { 'api-key': BREVO, 'Content-Type': 'application/json', 'accept': 'application/json' },
        body: JSON.stringify({
          sender: { name: REMETENTE_NOME, email: REMETENTE_EMAIL },
          to: [{ email: d.email, name: d.nome || undefined }],
          subject: assunto,
          htmlContent: html,
        }),
      })
      if (r.ok) { enviados++ } else {
        falhas++
        quemFalhou.push(d.email)
        if (!motivo) motivo = explica(r.status, await r.text().catch(() => ''))
      }
    }

    if (!teste && enviados) {
      await supa.from('foyer_newsletter').update({ ultimo_envio: new Date().toISOString() }).eq('ativo', true)
      if (numero) {
        await supa.from('foyer_revista_envio').upsert({
          numero, quando: new Date().toISOString(), enviados, falhas, remetente: REMETENTE_EMAIL,
        })
      }
    }
    return devolve({
      ok: true, enviados, falhas, total: destinatarios.length,
      remetente: REMETENTE_EMAIL,
      motivo: motivo || undefined,
      quemFalhou: quemFalhou.length ? quemFalhou.slice(0, 10) : undefined,
    })
  } catch (e) {
    return devolve({ erro: String((e as Error).message || e) }, 500)
  }
})
