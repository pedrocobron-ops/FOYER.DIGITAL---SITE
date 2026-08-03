// FOYER — o relógio das matérias agendadas, agora com pêndulo próprio.
//
// POR QUE ISTO EXISTE. O site já tinha um relógio: a rotina "agendadas" do
// GitHub, marcada para conferir a cada 30 minutos. Só que o horário do GitHub
// é uma INTENÇÃO, não uma promessa: quando a casa dele está cheia, ele atrasa
// a rotina, e às vezes pula de vez. Em 3 de agosto de 2026 ele ficou 2h43 sem
// dar sinal, e uma matéria marcada para as 9h10 só apareceu no site quando
// alguém, por acaso, mexeu em outra coisa e forçou uma publicação.
//
// O relógio do Supabase, esse, bate na hora. Então é ele quem cutuca o GitHub
// aqui: de dez em dez minutos manda a rotina rodar. A rotina em si não mudou,
// e ela mesma decide se há algo vencido; se não houver, não publica nada.
// O repositório é público, então rodar mais vezes não custa nada.
//
// A chave do GitHub NÃO mora aqui: mora na tabela coxia_segredo, guardada
// pelo chefe de redação pela própria Coxia. Esta função só a lê na hora.

const DONO = "pedrocobron-ops";
const REPO = "FOYER.DIGITAL---SITE";
// A chave da casa é a mesma que a Coxia usa para gravar arquivos: ela sabe
// escrever no repositório, mas NÃO tem permissão para acionar rotinas pelo
// nome. O aviso de repositório abaixo é o caminho que ela pode percorrer, e
// a rotina "agendadas" foi ensinada a atender por ele.
const AVISO = "relogio";
const SEGREDO = "foyer-pendulo-2026";

Deno.serve(async (req: Request) => {
  const u = new URL(req.url);
  if (u.searchParams.get("chave") !== SEGREDO) {
    return new Response("nada por aqui", { status: 401 });
  }

  const SB = Deno.env.get("SUPABASE_URL")!;
  const SR = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const cab = { apikey: SR, Authorization: `Bearer ${SR}` };

  const r = await fetch(`${SB}/rest/v1/coxia_segredo?id=eq.github&select=chave`, { headers: cab });
  const linhas = await r.json();
  const chave = Array.isArray(linhas) && linhas[0] ? linhas[0].chave : null;
  if (!chave) {
    return new Response(JSON.stringify({ ok: false, motivo: "sem chave da casa" }), {
      status: 409, headers: { "Content-Type": "application/json" },
    });
  }

  const g = await fetch(`https://api.github.com/repos/${DONO}/${REPO}/dispatches`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${chave}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "User-Agent": "relogio-foyer",
    },
    body: JSON.stringify({ event_type: AVISO }),
  });

  // 204 é o "recebi" do GitHub para esta chamada.
  const ok = g.status === 204;
  return new Response(JSON.stringify({ ok, http: g.status, texto: ok ? "" : await g.text() }), {
    status: ok ? 200 : 502,
    headers: { "Content-Type": "application/json" },
  });
});
