/* FOYER — comportamento compartilhado de todas as páginas */

// tema: Blackout (escuro) / Luz da sala (claro)
(function(){
  var root = document.documentElement;
  var btn = document.getElementById('theme');
  function current(){
    var t = root.getAttribute('data-theme');
    if(t) return t;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function apply(t){
    root.setAttribute('data-theme', t);
    if(btn) btn.textContent = (t === 'dark') ? 'Luz da sala' : 'Blackout';
  }
  apply(current());
  if(btn) btn.addEventListener('click', function(){
    apply(current() === 'dark' ? 'light' : 'dark');
  });
})();

// data corrente em pt-BR no formato industrial
(function(){
  try{
    var dias = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
    var d = new Date();
    var p = function(n){ return (n<10?'0':'')+n; };
    var el = document.getElementById('today');
    if(el) el.textContent = dias[d.getDay()] + ' — ' + p(d.getDate()) + '.' + p(d.getMonth()+1) + '.' + d.getFullYear() + ' — São Paulo, BR';
  }catch(e){}
})();

// revelação ao rolar, com escalonamento por grupo
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sel = '.sec-head, .fp-sub article, .news-cell, .crit, .show, .stat, .ency-row, .giro-item, .quote-card, .agd-row, .ep-cell, .ed-card';
  var els = document.querySelectorAll(sel);
  if(!('IntersectionObserver' in window)){ return; }
  var groups = new Map();
  els.forEach(function(el){
    var parent = el.parentNode;
    var i = groups.get(parent) || 0;
    groups.set(parent, i+1);
    el.classList.add('reveal');
    el.style.transitionDelay = (i % 8) * 70 + 'ms';
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold:.12, rootMargin:'0px 0px -6% 0px' });
  els.forEach(function(el){ io.observe(el); });
})();

// contadores (enciclopédia)
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nums = document.querySelectorAll('.stat .n[data-v]');
  if(!nums.length) return;
  function fmt(v){ return v.toLocaleString('pt-BR'); }
  if(reduce || !('IntersectionObserver' in window)){
    nums.forEach(function(n){ n.textContent = fmt(+n.getAttribute('data-v')); });
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return;
      io.unobserve(e.target);
      var target = +e.target.getAttribute('data-v');
      var t0 = null;
      function step(ts){
        if(!t0) t0 = ts;
        var k = Math.min((ts - t0) / 900, 1);
        k = 1 - Math.pow(1 - k, 3);
        e.target.textContent = fmt(Math.round(target * k));
        if(k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold:.5 });
  nums.forEach(function(n){ io.observe(n); });
})();

// compartilhamento — nativo no celular, redes no desktop
(function(){
  var SITE = 'https://www.foyer.digital/';
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-share]');
    if(!b) return;
    e.preventDefault();
    var kind  = b.getAttribute('data-share');
    var title = b.getAttribute('data-title') || document.title;
    var url   = location.pathname.indexOf('post-') > -1 ? location.href : SITE;
    if(kind === 'copy'){
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(function(){
          var old = b.textContent; b.textContent = 'Copiado ✓';
          setTimeout(function(){ b.textContent = old; }, 1800);
        });
      }
      return;
    }
    if(kind === 'native'){
      if(navigator.share){ navigator.share({ title:title, url:url }).catch(function(){}); return; }
      kind = 'whats';
    }
    var links = {
      whats:'https://wa.me/?text=' + encodeURIComponent(title + ' — ' + url),
      x:'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url),
      face:'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url)
    };
    if(links[kind]) window.open(links[kind], '_blank', 'noopener');
  });
})();


// métricas — visualizações e compartilhamentos (alimenta o ranking da Coxia)
(function(){
  var M = {
    url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
    key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB'
  };
  function bater(tipo){
    var m = location.pathname.match(/post-([a-z0-9-]+)\.html$/);
    var slug = m ? m[1] : (/agenda\.html$/.test(location.pathname) ? 'pagina-agenda' : null);
    if(!slug) return;
    if(tipo === 'view'){
      try{
        if(sessionStorage.getItem('fv-' + slug)) return;
        sessionStorage.setItem('fv-' + slug, '1');
      }catch(e){}
    }
    try{
      fetch(M.url + '/rest/v1/foyer_metricas', {
        method: 'POST',
        headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                   'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
        body: JSON.stringify({ slug: slug, tipo: tipo }),
        keepalive: true
      }).catch(function(){});
    }catch(e){}
  }
  bater('view');
  document.addEventListener('click', function(e){
    if(e.target.closest('[data-share]')) bater('share');
  });
})();


// newsletter da revista — cadastro real (grava no banco do FOYER)
(function(){
  var f = document.getElementById('signup');
  if(!f) return;
  var M = { url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
            key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' };
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var nome = (f.querySelector('input[type=text]') || {}).value || '';
    var email = (f.querySelector('input[type=email]') || {}).value || '';
    var btn = f.querySelector('button'), ok = document.getElementById('signup-ok');
    if(!email) return;
    btn.disabled = true; btn.textContent = 'Enviando…';
    fetch(M.url + '/rest/v1/foyer_newsletter', {
      method: 'POST',
      headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify({ nome: nome.trim(), email: email.trim().toLowerCase() })
    }).then(function(r){
      if(r.ok || r.status === 409){
        ok.textContent = r.status === 409
          ? 'Esse e-mail já está na lista ✓'
          : 'Pronto! Você está na lista da próxima edição ✓';
        ok.style.display = 'block';
        btn.textContent = 'Assinado ✓';
      } else { throw 0; }
    }).catch(function(){
      btn.disabled = false; btn.textContent = 'Assinar grátis';
      ok.textContent = 'Não deu agora — tente de novo em instantes';
      ok.style.display = 'block';
    });
  });
})();

/* ---------- FOYER no celular: instalar como aplicativo (PWA) ---------- */
(function(){
  if('serviceWorker' in navigator){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  }
  var K = 'foyer-app-aviso';
  var padrao = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if(padrao) return;                                  // já está instalado
  if(location.pathname.indexOf('coxia') >= 0) return; // não no admin
  // nunca na primeira página da visita: quem chega do Google lê em paz
  var pv = 1;
  try{
    pv = parseInt(sessionStorage.getItem('foyer-pv') || '0', 10) + 1;
    sessionStorage.setItem('foyer-pv', String(pv));
  }catch(e){}
  if(pv < 2) return;
  var visto = 0;
  try{ visto = parseInt(localStorage.getItem(K) || '0', 10); }catch(e){}
  if(Date.now() - visto < 14 * 864e5) return;         // no máximo a cada 14 dias
  var movel = window.matchMedia('(max-width: 820px)').matches;
  if(!movel) return;

  var esperado = null;
  window.addEventListener('beforeinstallprompt', function(e){
    e.preventDefault();
    esperado = e;
  });
  var iOS = /iphone|ipad|ipod/i.test(navigator.userAgent) && !window.MSStream;

  function abrir(){
    if(!esperado && !iOS) return;   // navegador sem suporte: não incomoda
    var v = document.createElement('div');
    v.className = 'app-veu';
    var arte =
      '<svg class="app-arte" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
        '<filter id="app-grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>' +
        '<rect width="600" height="400" fill="#380A06"/>' +
        '<polygon points="300,-30 130,400 470,400" fill="#E9CB85" opacity=".2"/>' +
        '<ellipse cx="300" cy="378" rx="160" ry="26" fill="#E9CB85" opacity=".3"/>' +
        '<circle cx="300" cy="278" r="27" fill="#120505"/>' +
        '<rect x="268" y="308" width="64" height="92" rx="10" fill="#120505"/>' +
        '<rect width="600" height="400" filter="url(#app-grain)" opacity=".12"/>' +
      '</svg>';
    v.innerHTML =
      '<div class="app-card" role="dialog" aria-label="Instalar o FOYER">' + arte +
        '<div class="app-miolo">' +
        '<span class="app-kick">Entre em cena</span>' +
        '<h3>Leve o FOYER no bolso</h3>' +
        '<p>Instale o site como aplicativo: acesso direto da tela inicial, sem loja e sem ocupar espaço.</p>' +
        (iOS && !esperado
          ? '<p class="app-ios">No Safari: toque em <b>Compartilhar</b> (o quadrado com a seta) e depois em <b>“Adicionar à Tela de Início”</b>.</p>' +
            '<div class="app-acoes"><button class="app-ok" data-fechar>Entendi</button></div>'
          : '<div class="app-acoes"><button class="app-ok" data-instalar>Instalar agora</button>' +
            '<button class="app-nao" data-fechar>Agora não</button></div>') +
        '</div>' +
      '</div>';
    document.body.appendChild(v);
    requestAnimationFrame(function(){ v.classList.add('on'); });
    function fechar(){
      try{ localStorage.setItem(K, String(Date.now())); }catch(e){}
      v.classList.remove('on');
      setTimeout(function(){ v.remove(); }, 250);
    }
    v.addEventListener('click', function(e){
      if(e.target === v || e.target.hasAttribute('data-fechar')) fechar();
      if(e.target.hasAttribute('data-instalar') && esperado){
        esperado.prompt();
        esperado.userChoice.then(function(){ fechar(); });
      }
    });
  }
  setTimeout(abrir, 7000);
})();

/* ---------- notificações do aplicativo: convite claro na entrada ---------- */
(function(){
  var suporta = ('Notification' in window) && ('serviceWorker' in navigator) && ('PushManager' in window);
  var K = 'foyer-push-aviso';
  var PUB = 'BHiZh7pcDS8jkCBhcRRDv4onYO7-XUOPUrtRNiNJIXqr9uSmTCdll1HCp8REMHRjFZ89NejDhJj6gDkiJw3qswI';
  var M = { url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
            key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' };

  function b64ParaBytes(b64){
    var pad = '='.repeat((4 - b64.length % 4) % 4);
    var raw = atob((b64 + pad).replace(/-/g, '+').replace(/_/g, '/'));
    var out = new Uint8Array(raw.length);
    for(var i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
    return out;
  }
  function inscrever(){
    return navigator.serviceWorker.ready.then(function(reg){
      return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ParaBytes(PUB) });
    }).then(function(sub){
      return fetch(M.url + '/rest/v1/foyer_push', {
        method: 'POST',
        headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                   'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
        body: JSON.stringify({ endpoint: sub.endpoint, sub: sub.toJSON() })
      });
    });
  }

  function abrirCartao(){
    if(document.getElementById('sino-veu')) return;
    var jaTem = suporta && Notification.permission === 'granted';
    var v = document.createElement('div');
    v.className = 'app-veu'; v.id = 'sino-veu';
    v.innerHTML =
      '<div class="app-card" role="dialog" aria-label="Notificações do FOYER">' +
        '<div class="app-miolo" style="padding-top:26px">' +
        '<div class="sino-ico">🔔</div>' +
        '<span class="app-kick">Primeira fila</span>' +
        '<h3>Fique por dentro das novidades</h3>' +
        (jaTem
          ? '<p>As notificações já estão ativas neste aparelho: uma por dia, sempre com algo que vale a pena.</p>' +
            '<div class="app-acoes"><button class="app-ok" data-fechar>Combinado</button></div>'
          : !suporta
          ? '<p>Este navegador não recebe notificações. No celular, instale o FOYER como aplicativo (no iPhone, pela Tela de Início) e ative por aqui.</p>' +
            '<div class="app-acoes"><button class="app-ok" data-fechar>Entendi</button></div>'
          : '<p>Uma notificação por dia com o melhor do teatro: o guia da quinta, a curiosidade do sábado, a manchete do dia. Só isso, prometido.</p>' +
            '<div class="app-acoes"><button class="app-ok" data-ativar>Ativar notificações</button>' +
            '<button class="app-nao" data-fechar>Agora não</button></div>') +
        '</div>' +
      '</div>';
    document.body.appendChild(v);
    requestAnimationFrame(function(){ v.classList.add('on'); });
    function sair(){ v.classList.remove('on'); setTimeout(function(){ v.remove(); }, 300); }
    v.addEventListener('click', function(e){
      if(e.target === v || e.target.hasAttribute('data-fechar')){
        try{ localStorage.setItem(K, String(Date.now())); }catch(err){}
        sair(); return;
      }
      if(e.target.hasAttribute('data-ativar')){
        var btn = e.target;
        btn.disabled = true; btn.textContent = 'Ativando…';
        Notification.requestPermission().then(function(p){
          if(p !== 'granted'){ sair(); return; }
          inscrever().then(function(r){
            if(r && (r.ok || r.status === 409)){
              var mi = v.querySelector('.app-miolo');
              mi.innerHTML = '<div class="sino-ico">✓</div><span class="app-kick">Combinado</span>' +
                '<h3>Você está na primeira fila</h3>' +
                '<p>Uma por dia, às 11h, sempre com algo que vale a pena. Até amanhã!</p>';
              setTimeout(sair, 2600);
            } else { sair(); }
          }).catch(sair);
        });
      }
    });
  }
  window.foyerSino = abrirCartao;

  // atalho permanente no rodapé
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('[data-sino]');
    if(a){ e.preventDefault(); abrirCartao(); }
  });

  // convite automático: logo depois de abrir o APP instalado (depois da abertura)
  var instalado = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if(!instalado || !suporta) return;
  if(Notification.permission !== 'default') return;
  var visto = 0;
  try{ visto = parseInt(localStorage.getItem(K) || '0', 10); }catch(e){}
  if(Date.now() - visto < 7 * 864e5) return;   // "agora não" vale por 7 dias
  setTimeout(abrirCartao, 2800);
})();

/* ---------- consentimento de cookies (LGPD) ---------- */
(function(){
  if(location.pathname.indexOf('coxia') >= 0) return;
  var K = 'foyer-consent';
  function escolha(){ try{ return (JSON.parse(localStorage.getItem(K) || 'null') || {}).nivel || ''; }catch(e){ return ''; } }
  window.foyerConsent = escolha;   // ads.js e futuros scripts consultam aqui

  function gravar(nivel){
    try{ localStorage.setItem(K, JSON.stringify({ nivel: nivel, quando: new Date().toISOString() })); }catch(e){}
  }
  function abrir(){
    if(document.getElementById('lgpd')) return;
    var b = document.createElement('div');
    b.id = 'lgpd';
    b.innerHTML =
      '<p><b>🍪 Cookies no FOYER.</b> Usamos armazenamento essencial (tema, sessão) e métricas anônimas de audiência. ' +
      'Com anúncios ativos, parceiros como o Google podem usar cookies de publicidade. ' +
      'Saiba mais na <a href="privacidade.html">Política de Privacidade</a>.</p>' +
      '<div class="lgpd-acoes"><button class="lgpd-sim">Aceitar tudo</button>' +
      '<button class="lgpd-min">Só o essencial</button></div>';
    document.body.appendChild(b);
    requestAnimationFrame(function(){ b.classList.add('on'); });
    function sair(){ b.classList.remove('on'); setTimeout(function(){ b.remove(); }, 300); }
    b.querySelector('.lgpd-sim').addEventListener('click', function(){ gravar('tudo'); sair(); });
    b.querySelector('.lgpd-min').addEventListener('click', function(){ gravar('essencial'); sair(); });
  }
  function tentar(){
    if(document.querySelector('.app-veu')){ setTimeout(tentar, 3000); return; }
    abrir();
  }
  if(!escolha()) setTimeout(tentar, 1200);
  // reabrir pelas preferências no rodapé
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('[data-lgpd]');
    if(a){ e.preventDefault(); try{ localStorage.removeItem(K); }catch(err){} abrir(); }
  });
})();
