/* FOYER — publicidade (Google AdSense)
   ============================================
   COMO LIGAR OS ANÚNCIOS (quando o Google aprovar):
   1. Troque 'ca-pub-0000000000000000' abaixo pelo seu ID de editor
      (aparece no painel do AdSense como "código do editor").
   2. Mude enabled para true.
   3. Edite o arquivo ads.txt na raiz do site com o mesmo ID.
   4. Publique. Pronto — todas as fatias .ad-slot passam a exibir anúncios.

   Enquanto enabled = false, nenhum script do Google é carregado e as
   fatias ficam invisíveis (sem afetar layout nem velocidade).
   ============================================ */

window.FOYER_ADS = {
  enabled: false,
  client: 'ca-pub-0000000000000000'
};

(function(){
  var cfg = window.FOYER_ADS;
  if(!cfg || !cfg.enabled) return;
  if(!/^ca-pub-\d{10,}$/.test(cfg.client)){
    console.warn('FOYER ads: configure o client ID em assets/ads.js');
    return;
  }
  document.body.classList.add('ads-on');

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + cfg.client;
  s.crossOrigin = 'anonymous';
  document.head.appendChild(s);

  var slots = document.querySelectorAll('.ad-slot');
  for(var i = 0; i < slots.length; i++){
    var el = slots[i];
    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.setAttribute('data-ad-client', cfg.client);
    if(el.getAttribute('data-ad-slot')) ins.setAttribute('data-ad-slot', el.getAttribute('data-ad-slot'));
    ins.setAttribute('data-ad-format', el.getAttribute('data-ad-format') || 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    el.appendChild(ins);
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  }
})();
