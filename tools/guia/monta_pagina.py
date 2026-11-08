# Página ESCONDIDA de conferência do Guia: foyer.digital/guia/
# noindex + nofollow, fora do sitemap (o sitemap só lista páginas da raiz),
# sem link no menu. Serve para o Pedro e a sessão conferirem os dados, campo
# a campo, com a fonte de cada um. A tela de verdade do guia é a Fase 2.
#
# Chamada pelo tools/build_pages.py no fim da montagem (assim os três fluxos
# que publicam o site levam a página junto). Lê import/guia/agenda.json e
# embute os dados na própria página: o site publicado não leva import/guia/.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import DADOS, RAIZ

PAGINA = r'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Guia FOYER: conferência</title>
<style>
:root{--bg:#faf7f2;--tx:#1d1a16;--mu:#6b645a;--li:#e4ddd2;--ca:#fff;--ac:#9c2a1b;--ok:#2f6b3a;--av:#9a6a00}
@media (prefers-color-scheme:dark){:root{--bg:#141210;--tx:#efe9df;--mu:#a59d90;--li:#332e28;--ca:#1d1a17;--ac:#e0705f;--ok:#7fc08a;--av:#e3b54a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 60px}
h1{font:600 26px/1.2 Georgia,serif;margin:0 0 4px}
.sub{color:var(--mu);margin:0 0 18px}
.fontes{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-bottom:18px}
.fonte{background:var(--ca);border:1px solid var(--li);border-radius:8px;padding:10px 12px;font-size:13px}
.fonte b{font-size:14px}.ok{color:var(--ok)}.ruim{color:var(--ac)}
.barra{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
.barra input{flex:1 1 220px;padding:9px 11px;border:1px solid var(--li);border-radius:8px;background:var(--ca);color:var(--tx);font:inherit}
.chip{border:1px solid var(--li);background:var(--ca);color:var(--tx);border-radius:99px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}
.chip[aria-pressed=true]{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.conta{color:var(--mu);font-size:13px;margin:0 0 10px}
.ev{background:var(--ca);border:1px solid var(--li);border-radius:10px;padding:12px 14px;margin-bottom:10px}
.ev h2{font:600 17px/1.3 Georgia,serif;margin:0 0 2px}
.ev .tag{font-size:12px;color:var(--mu);text-transform:uppercase;letter-spacing:.04em}
.ev p{margin:6px 0}
.ses{border-top:1px dashed var(--li);margin-top:8px;padding-top:8px;font-size:14px}
.ses dl{display:grid;grid-template-columns:max-content 1fr;gap:2px 10px;margin:0}
.ses dt{color:var(--mu)}.ses dd{margin:0;overflow-wrap:anywhere}
a{color:var(--ac)}
sup a{text-decoration:none;font-size:11px;margin-left:2px}
.ded{color:var(--av);font-size:12px}
.foto{margin:-12px -14px 10px;position:relative}
.foto img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px 10px 0 0;background:var(--li)}
.foto figcaption{font-size:11px;color:var(--mu);padding:4px 14px 0}
details{margin-top:24px;font-size:13px;color:var(--mu)}
</style>
</head>
<body>
<main>
<h1>Guia: conferência dos dados</h1>
<p class="sub">Página interna, escondida. Cada dado tem a fonte ao lado (↗) e a data da coleta ao passar o dedo ou o mouse. Montada em <span id="gerado"></span>.</p>
<div class="fontes" id="fontes"></div>
<div class="barra" id="areas"></div>
<div class="barra"><input id="q" type="search" placeholder="Buscar título, lugar, bairro, pessoa da ficha…" aria-label="Buscar"></div>
<p class="conta" id="conta"></p>
<div id="lista"></div>
<details><summary>Divergências entre fontes e mudanças recentes</summary><pre id="extra" style="white-space:pre-wrap"></pre></details>
</main>
<script>
const D = __DADOS__;
const AREAS = {teatro:'Teatro', opera:'Ópera', danca:'Dança', infantil:'Infantil', eventos:'Eventos e festivais', cinema:'Cinema', musica:'Música', exposicao:'Exposições', literatura:'Literatura', cursos:'Cursos e oficinas'};
const NOMES = {guiaoff:'Guia OFF', cinemateca:'Cinemateca Brasileira', municipal:'Theatro Municipal', masp:'MASP', mam:'MAM São Paulo', mis:'MIS'};
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const dt = iso => { try { return new Date(iso).toLocaleString('pt-BR', {dateStyle:'short', timeStyle:'short'}); } catch(e) { return iso; } };
const dia = iso => iso.length > 10 ? new Date(iso).toLocaleString('pt-BR', {weekday:'short', day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit'}) : iso.split('-').reverse().join('/');
document.getElementById('gerado').textContent = dt(D.gerado_em);
document.getElementById('fontes').innerHTML = Object.entries(D.fontes).map(([f, x]) =>
  `<div class="fonte"><b>${esc(NOMES[f] || f)}</b><br>` +
  (x.publicada ? `<span class="ok">no ar</span> · ${x.itens} itens` : `<span class="ruim">FORA: dado velho ou coleta falhou</span>`) +
  `<br>última coleta boa: ${x.ultima_coleta_boa ? dt(x.ultima_coleta_boa) : 'nunca'}` +
  (x.erro ? `<br><span class="ruim">erro: ${esc(x.erro)}</span>` : '') + `</div>`).join('');
function fonte(ev, c) {
  if (!c || c.o === undefined) return '';
  const o = ev.origens[c.o] || {};
  return `<sup><a href="${esc(o.url)}" target="_blank" rel="noopener nofollow" title="${esc((NOMES[o.fonte]||o.fonte) + ', coletado em ' + dt(o.coletado_em))}">↗</a></sup>` +
    (c.obs ? ` <span class="ded" title="${esc(c.obs)}">(ano deduzido)</span>` : '');
}
function lugarFonte(l, c) {
  if (!c) return '';
  const o = l.origens[c.o] || {};
  return `<sup><a href="${esc(o.url)}" target="_blank" rel="noopener nofollow" title="${esc((NOMES[o.fonte]||o.fonte) + ', coletado em ' + dt(o.coletado_em))}">↗</a></sup>`;
}
const val = c => c ? c.v : null;
function linha(rot, ev, c, fmt) {
  if (!c || c.v === null || c.v === undefined || c.v === '') return '';
  const v = fmt ? fmt(c.v) : esc(c.v);
  return `<dt>${rot}</dt><dd>${v}${fonte(ev, c)}</dd>`;
}
const link = u => `<a href="${esc(u)}" target="_blank" rel="noopener nofollow">${esc(u.replace(/^https?:\/\/(www\.)?/, '').slice(0, 60))}</a>`;
function card(ev) {
  const ses = ev.sessoes.map(s => {
    const l = D.lugares[s.lugar];
    let lug = '';
    if (l) {
      lug = `<dt>Lugar</dt><dd>${esc(val(l.nome))}${lugarFonte(l, l.nome)}` +
        (l.endereco ? `<br>${esc(val(l.endereco))}${l.bairro ? ', ' + esc(val(l.bairro)) : ''}${lugarFonte(l, l.endereco)}` :
         (l.endereco_texto ? `<br>${esc(val(l.endereco_texto))}${lugarFonte(l, l.endereco_texto)}` : '')) +
        (l.endereco ? ` · <a href="https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(val(l.nome) + ', ' + val(l.endereco) + ', São Paulo')}" target="_blank" rel="noopener">como chegar</a>` : '') +
        `</dd>`;
    }
    return `<div class="ses"><dl>${lug}` +
      linha('Sala', ev, s.sala) + linha('Atração', ev, s.atracao) +
      linha('Quando', ev, s.inicio, dia) + linha('Até', ev, s.fim, dia) + linha('Quando', ev, s.quando) +
      linha('Datas', ev, s.datas, v => v.map(dia).join(', ')) +
      linha('Estreia', ev, s.estreia, dia) + linha('Até', ev, s.ate, dia) +
      linha('Preço', ev, s.preco) + linha('Duração', ev, s.duracao_min, v => v + ' min') +
      linha('Classificação', ev, s.classificacao) + linha('Ingresso', ev, s.ingresso, link) +
      linha('Site', ev, s.site, link) + linha('Obs.', ev, s.obs) + `</dl></div>`;
  }).join('');
  const foto = ev.imagem ? `<figure class="foto"><img loading="lazy" referrerpolicy="no-referrer" alt="" src="${esc(val(ev.imagem))}" onerror="this.parentNode.remove()">` +
    `<figcaption>${esc(ev.imagem.credito || 'Divulgação')}${fonte(ev, ev.imagem)}</figcaption></figure>` : '';
  return `<article class="ev">${foto}<span class="tag">${esc(AREAS[val(ev.area)] || val(ev.area))}${ev.categoria ? ' · ' + esc(val(ev.categoria)) : ''} · fonte: ${esc(NOMES[ev.fonte] || ev.fonte)}</span>` +
    `<h2><a href="${esc(val(ev.link_fonte))}" target="_blank" rel="noopener nofollow">${esc(val(ev.titulo))}</a>${fonte(ev, ev.titulo)}</h2>` +
    (ev.trecho ? `<p>${esc(val(ev.trecho))}${fonte(ev, ev.trecho)}</p>` : '') +
    (ev.ficha ? `<p style="font-size:13px;color:var(--mu)">${esc(val(ev.ficha))}${fonte(ev, ev.ficha)}</p>` : '') +
    (ev.tambem_em ? `<p class="ded">Também aparece em: ${esc(ev.tambem_em.join(', '))}</p>` : '') + ses + `</article>`;
}
let area = '';
const contagem = {};
D.eventos.forEach(e => { const a = val(e.area); contagem[a] = (contagem[a] || 0) + 1; });
const barra = document.getElementById('areas');
barra.innerHTML = `<button class="chip" data-a="" aria-pressed="true">Tudo (${D.eventos.length})</button>` +
  Object.entries(contagem).map(([a, n]) => `<button class="chip" data-a="${esc(a)}" aria-pressed="false">${esc(AREAS[a] || a)} (${n})</button>`).join('');
barra.addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  area = b.dataset.a; barra.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b)); desenha();
});
const norm = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const indice = D.eventos.map(e => norm([val(e.titulo), val(e.trecho), val(e.ficha),
  ...e.sessoes.map(s => { const l = D.lugares[s.lugar] || {}; return [val(l.nome), val(l.bairro), val(s.sala)].join(' '); })].join(' ')));
const q = document.getElementById('q');
q.addEventListener('input', desenha);
function desenha() {
  const t = norm(q.value.trim());
  const sel = D.eventos.filter((e, i) => (!area || val(e.area) === area) && (!t || indice[i].includes(t)));
  document.getElementById('conta').textContent = sel.length + ' programa(s)';
  document.getElementById('lista').innerHTML = sel.slice(0, 400).map(card).join('');
}
desenha();
document.getElementById('extra').textContent =
  'Divergências (o guia mantém a fonte mais próxima do lugar):\n' + (JSON.stringify(D.divergencias, null, 1) || '[]') +
  '\n\nMudanças recentes de horário, preço ou temporada:\n' + JSON.stringify(D.mudancas || [], null, 1);
</script>
</body>
</html>
'''


def main():
    arq = os.path.join(DADOS, 'agenda.json')
    if not os.path.exists(arq):
        print('guia: sem agenda.json ainda, página não montada')
        return
    d = json.load(open(arq, encoding='utf-8'))
    mud = os.path.join(DADOS, 'mudancas.json')
    d['mudancas'] = json.load(open(mud, encoding='utf-8'))[-40:] if os.path.exists(mud) else []
    dados = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    os.makedirs(os.path.join(RAIZ, 'guia'), exist_ok=True)
    with open(os.path.join(RAIZ, 'guia', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(PAGINA.replace('__DADOS__', dados))
    print('• guia/index.html (escondida, noindex): %d eventos' % len(d['eventos']))


if __name__ == '__main__':
    main()
