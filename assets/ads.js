/* FOYER — publicidade de rede (Google AdSense)
   ============================================================
   O que este arquivo faz: preenche com anúncio do Google os espaços que o
   site já reserva no desenho, enquanto a casa não tem anunciante direto.
   O anunciante direto (Entreato, Cartaz, Cortina) NUNCA passa por aqui — ele
   é montado no gerador, com a arte que o produtor mandou.

   PARA LIGAR (quando o AdSense aprovar o foyer.digital):
   1. Troque 'ca-pub-0000000000000000' pelo ID de editor. Ele aparece em
      adsense.google.com → Conta → Informações da conta.
   2. Ponha em 'unidade' o número da unidade criada no AdSense
      (Anúncios → Por unidade de anúncio → Display responsivo).
   3. Mude ligado para true.
   4. Escreva o mesmo ID no arquivo ads.txt, na raiz do site.
   5. Publique.

   PARA ESPIAR ANTES DE LIGAR: abra qualquer página com ?ads=demo no fim do
   endereço (foyer.digital/?ads=demo). Os espaços aparecem hachurados, no
   tamanho que vão ocupar, sem carregar nada do Google — e o leitor comum
   não vê nada disso.

   ONDE NÃO ENTRA: a revista. É o que o assinante ganha por ter deixado o
   e-mail, e é o espaço que a casa vende a preço de capa ao anunciante
   direto. Ordem do Pedro, 02/08/2026.

   LGPD: quem responde "Só o essencial" no aviso de cookies recebe anúncio
   NÃO personalizado. Quem ainda não respondeu também — o padrão é o mais
   conservador, e só afrouxa com um "Aceitar tudo" explícito.
   ============================================================ */

// Uma unidade por LUGAR da página, nunca a mesma duas vezes na mesma tela.
// Com os dois espaços da capa pedindo pela mesma unidade, o Google entendeu
// que era o mesmo lugar e mandou o mesmo anúncio duas vezes — na estreia,
// a Starlink apareceu em cima e embaixo. Blocos distintos resolvem, e é o
// que o próprio Google recomenda: um bloco por posição.
//
// A lista é percorrida na ordem em que os espaços aparecem na página. Como
// nenhuma página do FOYER tem mais de dois, duas unidades já bastam; a
// terceira fica de folga para quando algum lugar novo entrar.
window.FOYER_ADS = {
  ligado: true,
  editor: 'ca-pub-5861702469763970',    // conta programafoyer@gmail.com
  unidades: [
    '5626283619',                       // "FOYER — geral"  (1º espaço da página)
  ]
};

(function(){
  var cfg = window.FOYER_ADS || {};

  // ---- modo espiada: mostra o lugar e o tamanho, sem chamar o Google
  if(/[?&]ads=demo\b/.test(location.search)){
    document.body.classList.add('ads-on', 'ads-demo');
    return;
  }

  if(!cfg.ligado) return;
  if(!/^ca-pub-\d{10,}$/.test(cfg.editor || '')){
    console.warn('FOYER ads: falta o ID de editor em assets/ads.js');
    return;
  }

  // Página sem espaço reservado (a revista) não carrega NADA do Google. Não
  // basta não montar os espaços: a conta do FOYER está com "anúncios
  // automáticos" ligada, e o script sozinho já autoriza o Google a enfiar
  // anúncio onde ele quiser — inclusive no meio do folhear da revista.
  var espacos = document.querySelectorAll('.ad-slot');
  if(!espacos.length) return;

  // sem "Aceitar tudo" explícito, o anúncio roda sem perfilar ninguém
  if(!(window.foyerConsent && window.foyerConsent() === 'tudo')){
    window.adsbygoogle = window.adsbygoogle || [];
    window.adsbygoogle.requestNonPersonalizedAds = 1;
  }
  document.body.classList.add('ads-on');

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + cfg.editor;
  s.crossOrigin = 'anonymous';
  document.head.appendChild(s);

  for(var i = 0; i < espacos.length; i++){
    var el = espacos[i];
    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.setAttribute('data-ad-client', cfg.editor);
    // O número da unidade vem do AdSense. Os números do HTML (1001, 2001…)
    // dizem só a posição no desenho, e o Google não os conhece.
    // Cada espaço da página pega a unidade seguinte da lista; se a lista
    // acabar, ela recomeça — pior caso, volta a repetir, que é o que já
    // acontecia antes.
    var lista = cfg.unidades && cfg.unidades.length ? cfg.unidades : [cfg.unidade];
    var u = el.getAttribute('data-ad-unidade') || lista[i % lista.length];
    if(u) ins.setAttribute('data-ad-slot', u);
    ins.setAttribute('data-ad-format', el.getAttribute('data-ad-format') || 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    el.appendChild(ins);
    vigiaVazio(el, ins);
    try{ (window.adsbygoogle = window.adsbygoogle || []).push({}); }catch(e){}
  }

  // Nem todo espaço é vendido a toda hora. Quando o Google não tem anúncio
  // para aquele lugar, ele marca o bloco como "unfilled" e a caixa fica ali,
  // vazia, com "Publicidade" escrito por cima — cara de site quebrado, num
  // lugar onde o leitor decide se fica. Aqui a caixa some sozinha, e o texto
  // volta a correr como se o espaço nunca tivesse existido.
  function vigiaVazio(caixa, ins){
    function confere(){
      var st = ins.getAttribute('data-ad-status');
      if(st === 'unfilled'){ caixa.style.display = 'none'; return true; }
      return st === 'filled';
    }
    if(confere()) return;
    if(!window.MutationObserver) return;
    var obs = new MutationObserver(function(){ if(confere()) obs.disconnect(); });
    obs.observe(ins, { attributes: true, attributeFilter: ['data-ad-status'] });
    // rede fora do ar, bloqueador de anúncio, resposta que nunca chega: em
    // 12 segundos a caixa vazia sai de cena de qualquer jeito
    setTimeout(function(){
      obs.disconnect();
      if(ins.getAttribute('data-ad-status') !== 'filled' && !ins.offsetHeight)
        caixa.style.display = 'none';
    }, 12000);
  }
})();
