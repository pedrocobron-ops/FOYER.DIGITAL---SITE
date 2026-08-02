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

window.FOYER_ADS = {
  ligado: false,                        // vira true quando 'unidade' estiver preenchida
  editor: 'ca-pub-5861702469763970',    // conta programafoyer@gmail.com
  unidade: ''                           // ← falta: número da unidade criada no AdSense
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

  var espacos = document.querySelectorAll('.ad-slot');
  for(var i = 0; i < espacos.length; i++){
    var el = espacos[i];
    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.setAttribute('data-ad-client', cfg.editor);
    // o número da unidade vem do AdSense. Os números do HTML (1001, 2001…)
    // dizem só a posição no desenho, e o Google não os conhece.
    var u = el.getAttribute('data-ad-unidade') || cfg.unidade;
    if(u) ins.setAttribute('data-ad-slot', u);
    ins.setAttribute('data-ad-format', el.getAttribute('data-ad-format') || 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    el.appendChild(ins);
    try{ (window.adsbygoogle = window.adsbygoogle || []).push({}); }catch(e){}
  }
})();
