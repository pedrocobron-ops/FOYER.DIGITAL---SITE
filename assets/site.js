/* FOYER — comportamento compartilhado de todas as páginas */

// tema: Blackout (escuro) / Luz da sala (claro)
// A casa abre com a LUZ DA SALA em todo aparelho — celular, aplicativo ou
// computador. Antes o site perguntava o modo do sistema, e quem tinha o
// celular no escuro entrava no FOYER de Blackout sem ter pedido. Agora o
// Blackout só acontece quando o leitor aperta o botão, e essa escolha fica
// guardada no aparelho para as próximas páginas e as próximas visitas.
(function(){
  var root = document.documentElement;
  var btn = document.getElementById('theme');
  var CHAVE = 'foyer-tema';
  function guardado(){
    try{
      var t = localStorage.getItem(CHAVE);
      return (t === 'dark' || t === 'light') ? t : null;
    }catch(e){ return null; }
  }
  function current(){
    return root.getAttribute('data-theme') || guardado() || 'light';
  }
  function apply(t){
    root.setAttribute('data-theme', t);
    if(btn) btn.textContent = (t === 'dark') ? 'Luz da sala' : 'Blackout';
  }
  apply(current());
  if(btn) btn.addEventListener('click', function(){
    var novo = current() === 'dark' ? 'light' : 'dark';
    apply(novo);
    try{ localStorage.setItem(CHAVE, novo); }catch(e){}
  });
})();

// data corrente em pt-BR no formato industrial
(function(){
  try{
    var dias = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
    var d = new Date();
    var p = function(n){ return (n<10?'0':'')+n; };
    var el = document.getElementById('today');
    // A cidade é a primeira coisa a sair quando a tarja não cabe. Numa tela
    // de celular a linha inteira era cortada no meio da palavra e o leitor
    // via "SÃO PAU" na primeira linha do site, em toda página. Dia e data
    // são o que interessa ali; a cidade da casa está no rodapé e no "Quem
    // somos". O corte é pela LARGURA da tela, não por aparelho: quem gira o
    // telefone volta a ver a cidade.
    if(el){
      var data = dias[d.getDay()] + ' — ' + p(d.getDate()) + '.' + p(d.getMonth()+1) + '.' + d.getFullYear();
      var escreve = function(){
        el.textContent = window.innerWidth < 560 ? data : data + ' — São Paulo, BR';
      };
      escreve();
      window.addEventListener('resize', escreve);
    }
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
  // O endereço a compartilhar sai do canonical da própria página, que o
  // gerador escreve em toda página com o domínio certo.
  //
  // Antes daqui, quem não estivesse numa página "post-" recebia a CAPA no
  // lugar do endereço da página. Quem compartilhava um verbete da
  // enciclopédia mandava o nome da pessoa com o link da capa: 2.643 páginas
  // mandando o amigo para o lugar errado. E a capa vinha com "www.", que não
  // é o endereço da casa (o CNAME e todos os canonical são foyer.digital,
  // sem www).
  //
  // O botão pode declarar o próprio endereço em data-url. É o caso dos
  // cartões de "leia também": eles carregam o TÍTULO da matéria recomendada,
  // e sem isso levavam o título de uma com o endereço de outra.
  function enderecoDaPagina(){
    var c = document.querySelector('link[rel="canonical"]');
    return (c && c.href) || location.href;
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-share]');
    if(!b) return;
    e.preventDefault();
    var kind  = b.getAttribute('data-share');
    var title = b.getAttribute('data-title') || document.title;
    var url   = b.getAttribute('data-url') || enderecoDaPagina();
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


// métricas — audiência anônima do site (alimenta o painel do chefe na Coxia)
// LGPD: sem dado pessoal; identificador de visitante recorrente só com consentimento total
(function(){
  var M = {
    url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
    key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB'
  };
  // não medir: a Coxia (ferramenta interna) nem quem é da casa (equipe logada neste navegador)
  if(/\/coxia\//.test(location.pathname)) return;
  try{ if(localStorage.getItem('foyer-equipe') === '1') return; }catch(e){}
  function consent(){ try{ return localStorage.getItem('foyer-consent') || ''; }catch(e){ return ''; } }
  function sid(){
    try{
      var s = sessionStorage.getItem('foyer-sessao');
      if(!s){ s = Math.random().toString(36).slice(2, 10) + Date.now().toString(36); sessionStorage.setItem('foyer-sessao', s); }
      return s;
    }catch(e){ return null; }
  }
  function vid(){
    if(consent() !== 'tudo') return null;
    try{
      var v = localStorage.getItem('foyer-vis');
      if(!v){ v = Math.random().toString(36).slice(2, 12) + Date.now().toString(36); localStorage.setItem('foyer-vis', v); }
      return v;
    }catch(e){ return null; }
  }
  function slugDe(){
    var m = location.pathname.match(/post-([a-z0-9-]+)\.html$/);
    return m ? m[1] : (/agenda\.html$/.test(location.pathname) ? 'pagina-agenda' : null);
  }
  function pagina(){
    var s = slugDe();
    if(s) return s;
    var p = location.pathname.replace(/^\//, '').replace(/index\.html$/, '').replace(/\.html$/, '');
    return (p || 'capa').slice(0, 120);
  }
  function origem(){
    try{
      if(!document.referrer) return '';
      var h = new URL(document.referrer).hostname.replace(/^www\./, '');
      return h === location.hostname.replace(/^www\./, '') ? '' : h.slice(0, 80);
    }catch(e){ return ''; }
  }
  function disp(){
    var app = false;
    try{ app = matchMedia('(display-mode: standalone)').matches || !!navigator.standalone; }catch(e){}
    if(app) return 'app';
    return matchMedia('(max-width: 820px)').matches ? 'celular' : 'computador';
  }
  function enviar(extra){
    var corpo = {
      slug: slugDe(), pagina: pagina(), tipo: extra.tipo,
      sessao: sid(), visitante: vid(), ref: origem(),
      utm: (function(){ try{ return (new URLSearchParams(location.search).get('utm_source') || '').slice(0, 60) || null; }catch(e){ return null; } })(),
      disp: disp(), lingua: (navigator.language || '').slice(0, 10) || null
    };
    if(extra.segundos != null){ corpo.segundos = extra.segundos; corpo.rolagem = extra.rolagem; }
    try{
      fetch(M.url + '/rest/v1/foyer_metricas', {
        method: 'POST',
        headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                   'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
        body: JSON.stringify(corpo),
        keepalive: true
      }).catch(function(){});
    }catch(e){}
  }
  // visualização: uma por página por visita
  var jaViu = false;
  try{
    jaViu = !!sessionStorage.getItem('fv-' + pagina());
    if(!jaViu) sessionStorage.setItem('fv-' + pagina(), '1');
  }catch(e){}
  if(!jaViu) enviar({ tipo: 'view' });
  // tempo de leitura + rolagem máxima (enviados quando a pessoa sai da página)
  var t0 = Date.now(), rolMax = 0, fechou = false;
  function medirRolagem(){
    var d = document.documentElement, tot = d.scrollHeight - window.innerHeight;
    if(tot > 40){
      var p = Math.round((window.scrollY / tot) * 100);
      if(p > rolMax) rolMax = Math.min(100, p);
    }
  }
  window.addEventListener('scroll', medirRolagem, { passive: true });
  medirRolagem();
  function fechar(){
    if(fechou) return;
    var seg = Math.round((Date.now() - t0) / 1000);
    if(seg < 3) return;
    fechou = true;
    enviar({ tipo: 'tempo', segundos: Math.min(seg, 1800), rolagem: rolMax });
  }
  window.addEventListener('pagehide', fechar);
  document.addEventListener('visibilitychange', function(){
    if(document.visibilityState === 'hidden') fechar();
  });
  document.addEventListener('click', function(e){
    if(e.target.closest('[data-share]')) enviar({ tipo: 'share' });
  });

  /* ---------- publicidade: a conta que o anunciante recebe ----------
     Cada anúncio marca VISTA (uma por visita) e CLIQUE. O identificador vem
     do próprio anúncio (data-pub), montado com o formato e o protocolo do
     pedido, para o número voltar certinho ao dono na Coxia. */
  function pubEnvia(tipo, chave){
    if(!chave) return;
    var corpo = {
      slug: String(chave).slice(0, 120), pagina: pagina(), tipo: tipo,
      sessao: sid(), visitante: vid(), ref: origem(), disp: disp(),
      lingua: (navigator.language || '').slice(0, 10) || null
    };
    try{
      var pronto = JSON.stringify(corpo);
      var enviouBeacon = false;
      if(tipo === 'pub-clique' && navigator.sendBeacon){
        // o clique leva a pessoa embora: o beacon sobrevive à saída da página
        enviouBeacon = navigator.sendBeacon(
          M.url + '/rest/v1/foyer_metricas?apikey=' + encodeURIComponent(M.key),
          new Blob([pronto], { type: 'application/json' }));
      }
      if(!enviouBeacon){
        fetch(M.url + '/rest/v1/foyer_metricas', {
          method: 'POST',
          headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                     'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
          body: pronto, keepalive: true
        }).catch(function(){});
      }
    }catch(e){}
  }
  window.foyerPubVista = function(chave){
    if(!chave) return;
    try{
      var k = 'fpv-' + chave;
      if(sessionStorage.getItem(k)) return;   // uma vista por visita, por anúncio
      sessionStorage.setItem(k, '1');
    }catch(e){}
    pubEnvia('pub-vista', chave);
  };
  document.addEventListener('click', function(e){
    var al = e.target.closest('[data-pub]');
    if(al) pubEnvia('pub-clique', al.getAttribute('data-pub'));
  }, true);
  /* ------------------------------------------------------------------
     O SORTEIO DOS ANUNCIANTES (ordem do Pedro, 31/07/2026)
     Formato com mais de um contratado não pode ter lugar fixo: a cada vez
     que alguém abre a página, sorteia-se quem vai em cada lugar. Assim
     ninguém fica sempre com o pé da página e todos passam pela capa.
     A página já vem montada do servidor (quem está sem JavaScript vê um
     anúncio de verdade); aqui só trocamos a arte, o link e o nome do
     anúncio nas métricas. Roda ANTES do contador de vistas, para a vista
     ser contada para quem realmente apareceu. */
  function pubSorteia(){
    var fonte = document.getElementById('foyer-pub-elenco');
    if(!fonte) return;
    var elenco; try{ elenco = JSON.parse(fonte.textContent); }catch(e){ return; }
    Object.keys(elenco || {}).forEach(function(fmt){
      var pool = (elenco[fmt] || []).filter(function(a){ return a && a.img; });
      var lugares = [].slice.call(document.querySelectorAll('[data-pub-slot="' + fmt + '"]'));
      if(pool.length < 2 || !lugares.length) return;
      // embaralha o elenco (Fisher-Yates) e distribui um por lugar: enquanto
      // houver anunciante de sobra, ninguém se repete na mesma página
      var ordem = pool.slice();
      for(var i = ordem.length - 1; i > 0; i--){
        var j = Math.floor(Math.random() * (i + 1));
        var t = ordem[i]; ordem[i] = ordem[j]; ordem[j] = t;
      }
      lugares.forEach(function(el, ix){
        var a = ordem[ix % ordem.length];
        var link = el.querySelector('a'), img = el.querySelector('img');
        if(!link || !img) return;
        el.setAttribute('data-pub-chave', a.chave);
        link.setAttribute('href', a.link || '#');
        link.setAttribute('data-pub', a.chave);
        img.setAttribute('src', a.img);
        img.setAttribute('alt', a.legenda || '');
        var leg = el.querySelector('figcaption, .leg, span:not(.ph)');
        if(leg && leg !== img) leg.textContent = a.legenda || '';
      });
    });
  }
  try{ pubSorteia(); }catch(e){}

  // vista de qualquer anúncio que entre em cena (entreato, página da revista)
  try{
    if('IntersectionObserver' in window){
      var ioPub = new IntersectionObserver(function(es){
        es.forEach(function(en){
          // a revista mostra páginas por um instante só para medir a diagramação:
          // quando o retorno chega, elas já sumiram, e aí não é vista de verdade
          if(en.isIntersecting && en.target.getClientRects().length){
            window.foyerPubVista(en.target.getAttribute('data-pub-chave'));
            ioPub.unobserve(en.target);
          }
        });
      }, { threshold: 0.4 });
      var liga = function(){
        document.querySelectorAll('[data-pub-chave]').forEach(function(el){ ioPub.observe(el); });
      };
      liga();
      // a revista monta páginas conforme se folheia: reobserva quando chegam
      document.addEventListener('foyer-pub-nova', liga);
    }
  }catch(e){}
})();


// a conversa da revista — o cadastro como um momento, não um formulário.
// Uma pergunta por tela, com os três sinais do teatro marcando o caminho.
(function(){
  var M = { url: 'https://jcaqjlrzmrtzjyfbljxh.supabase.co',
            key: 'sb_publishable_IeMSoNvrWisQxJg9uP-V1w_jmVMQ0YB' };
  var R = { nome:'', email:'', cidade:'', frequencia:'', interesses:[], conteudos:[] };
  var ov = null, passo = 0;

  var PASSOS = [
    { id:'nome', sinal:'🔔 primeiro sinal', titulo:'Que bom ter você no saguão.',
      sub:'Como a gente te chama?', tipo:'texto', place:'pode ser só o primeiro nome' },
    { id:'email', sinal:'🔔 primeiro sinal', titulo:'Assinante lê na quinta, às 7h. Todo mundo, só na sexta.',
      sub:'Em qual caixa de entrada ela te encontra?', tipo:'email', place:'seu@email.com',
      nota:'De graça, sem spam, e seus dados ficam só com o FOYER. <a href="privacidade.html" target="_blank">Política de privacidade</a>' },
    { id:'cidade', sinal:'🔔🔔 segundo sinal', titulo:'De onde você aplaude?',
      sub:'A agenda certa depende disso.', tipo:'um', outra:true,
      ops:['São Paulo','Rio de Janeiro','Belo Horizonte','Brasília','Curitiba',
           'Porto Alegre','Recife','Salvador','Outra cidade'] },
    { id:'interesses', sinal:'🔔🔔 segundo sinal', titulo:'O que te faz sair de casa?',
      sub:'Marque tudo o que te chama. Vale sonhar.', tipo:'varios',
      ops:['Teatro','Musicais','Dança','Ópera e concertos','Shows e música ao vivo',
           'Cinema','Circo','Stand-up e humor','Exposições e museus'] },
    { id:'conteudos', sinal:'🔔🔔 segundo sinal', titulo:'E entre uma cortina e outra, o que você gosta de ler?',
      sub:'A redação escreve mais do que você marcar.', tipo:'varios',
      ops:['Estreias e o que entra em cartaz','Bastidores e como se faz','Histórias e memória',
           'Mercado e bilheteria','Guias de fim de semana','Entrevistas e perfis','Crítica'] },
    { id:'frequencia', sinal:'🔔🔔🔔 terceiro sinal', titulo:'Com que frequência você vê arte ao vivo?',
      sub:'Teatro, show, dança, o que for. Ao vivo.', tipo:'um',
      ops:['Toda semana','Todo mês','Algumas vezes por ano','Quase nunca. Quero mudar isso'] }
  ];

  function mede(tipo){
    try{
      fetch(M.url + '/rest/v1/foyer_metricas', {
        method: 'POST',
        headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                   'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
        body: JSON.stringify({ tipo: tipo, pagina: 'conversa-revista' }),
        keepalive: true
      }).catch(function(){});
    }catch(e){}
  }
  function abre(){
    if(ov) ov.remove();
    ov = document.createElement('div');
    ov.className = 'cv-overlay';
    ov.innerHTML = '<div class="cv-caixa" role="dialog" aria-modal="true" aria-label="Assinar a revista">' +
      '<button type="button" class="cv-fechar" aria-label="Fechar">✕</button>' +
      '<div class="cv-corpo"></div></div>';
    document.body.appendChild(ov);
    document.body.style.overflow = 'hidden';
    ov.querySelector('.cv-fechar').addEventListener('click', fecha);
    ov.addEventListener('click', function(e){ if(e.target === ov) fecha(); });
    passo = 0;
    pinta(0);
    mede('conversa-abre');
  }
  function fecha(){
    if(ov){ ov.remove(); ov = null; }
    document.body.style.overflow = '';
  }
  function pinta(dir){
    var p = PASSOS[passo];
    var c = ov.querySelector('.cv-corpo');
    c.classList.remove('anima-f', 'anima-b');
    void c.offsetWidth;                       // reinicia a animação da tela
    c.classList.add(dir < 0 ? 'anima-b' : 'anima-f');
    var miolo = '';
    if(p.tipo === 'texto' || p.tipo === 'email'){
      miolo = '<input class="cv-input" type="' + (p.tipo === 'email' ? 'email' : 'text') + '" ' +
        'placeholder="' + p.place + '" value="' + (R[p.id] || '') + '" aria-label="' + p.sub + '">' +
        (p.nota ? '<p class="cv-nota">' + p.nota + '</p>' : '') +
        '<p class="cv-erro" aria-live="polite"></p>';
    } else {
      miolo = '<div class="cv-ops">' + p.ops.map(function(o, k){
        var marcada = p.tipo === 'um' ? R[p.id] === o : R[p.id].indexOf(o) >= 0;
        return '<button type="button" class="cv-op' + (marcada ? ' on' : '') + '" data-op="' + o + '" ' +
          'style="animation-delay:' + (k * 45) + 'ms">' + o + '</button>';
      }).join('') + '</div>';
    }
    c.innerHTML =
      '<span class="cv-sinal">' + p.sinal + '</span>' +
      '<h3 class="cv-t">' + p.titulo + '</h3>' +
      '<p class="cv-s">' + p.sub + '</p>' + miolo +
      '<div class="cv-pe">' +
        (passo > 0 ? '<button type="button" class="cv-volta">← voltar</button>' : '<span></span>') +
        '<span class="cv-onde">' + (passo + 1) + ' de ' + PASSOS.length + '</span>' +
        '<button type="button" class="cv-vai">' + (passo === PASSOS.length - 1 ? 'Abrir a cortina' : 'Continuar →') + '</button>' +
      '</div>';
    var inp = c.querySelector('.cv-input');
    if(inp){
      setTimeout(function(){ inp.focus(); }, 60);
      inp.addEventListener('keydown', function(e){ if(e.key === 'Enter') avanca(); });
    } else {
      var prim = c.querySelector('.cv-op');
      if(prim) setTimeout(function(){ prim.focus(); }, 60);
    }
    c.querySelectorAll('.cv-op').forEach(function(b){
      b.addEventListener('click', function(){
        var o = b.dataset.op;
        if(p.tipo === 'um'){
          R[p.id] = o;
          c.querySelectorAll('.cv-op').forEach(function(x){ x.classList.toggle('on', x === b); });
          if(p.outra && o === 'Outra cidade'){       // conta pra gente qual
            var caixa = c.querySelector('.cv-outra');
            if(!caixa){
              caixa = document.createElement('input');
              caixa.className = 'cv-input cv-outra';
              caixa.placeholder = 'qual? conta pra gente';
              caixa.setAttribute('aria-label', 'Qual cidade?');
              c.querySelector('.cv-ops').after(caixa);
              caixa.addEventListener('keydown', function(e){ if(e.key === 'Enter') avanca(); });
            }
            caixa.focus();
            return;
          }
          var caixaFora = c.querySelector('.cv-outra');
          if(caixaFora) caixaFora.remove();
          setTimeout(avanca, 220);          // escolheu, a conversa segue sozinha
        } else {
          var i = R[p.id].indexOf(o);
          if(i >= 0) R[p.id].splice(i, 1); else R[p.id].push(o);
          b.classList.toggle('on');
        }
      });
    });
    var vv = c.querySelector('.cv-volta');
    if(vv) vv.addEventListener('click', function(){ passo--; pinta(-1); });
    c.querySelector('.cv-vai').addEventListener('click', avanca);
  }
  function avanca(){
    var p = PASSOS[passo];
    var c = ov.querySelector('.cv-corpo');
    if(p.tipo === 'texto' || p.tipo === 'email'){
      var v = (c.querySelector('.cv-input') || {}).value || '';
      v = v.trim();
      var erro = c.querySelector('.cv-erro');
      if(p.tipo === 'texto' && !v){ erro.textContent = 'Pode ser só o primeiro nome.'; return; }
      if(p.tipo === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){
        erro.textContent = 'Confere esse e-mail? É por ele que a revista chega.'; return;
      }
      R[p.id] = v;
    }
    if(p.tipo === 'um' && !R[p.id]){ return; }   // precisa escolher uma
    if(p.outra && R[p.id] === 'Outra cidade'){
      var q = (c.querySelector('.cv-outra') || {}).value || '';
      if(q.trim()) R[p.id] = q.trim();
    }
    if(passo < PASSOS.length - 1){ passo++; pinta(1); return; }
    envia();
  }
  function envia(){
    var c = ov.querySelector('.cv-corpo');
    c.classList.remove('anima-f', 'anima-b'); void c.offsetWidth; c.classList.add('anima-f');
    c.innerHTML = '<span class="cv-sinal">🔔🔔🔔</span><h3 class="cv-t">Reservando a sua cadeira…</h3>';
    fetch(M.url + '/rest/v1/foyer_newsletter', {
      method: 'POST',
      headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify({ nome: R.nome, email: R.email.toLowerCase(), consent: true,
                             cidade: R.cidade === 'Outra cidade' ? 'Outra' : R.cidade,
                             frequencia: R.frequencia.toLowerCase(),
                             interesses: R.interesses, conteudos: R.conteudos })
    }).then(function(r){
      if(r.status === 409){
        // já era da casa: as respostas novas atualizam o retrato
        return fetch(M.url + '/rest/v1/rpc/foyer_atualiza_assinatura', {
          method: 'POST',
          headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key, 'Content-Type': 'application/json' },
          body: JSON.stringify({ p_email: R.email, p_nome: R.nome,
                                 p_cidade: R.cidade === 'Outra cidade' ? 'Outra' : R.cidade,
                                 p_frequencia: R.frequencia.toLowerCase(),
                                 p_interesses: R.interesses, p_conteudos: R.conteudos })
        }).then(function(){ return 'ja'; }).catch(function(){ return 'ja'; });
      }
      if(r.ok) return 'nova';
      throw 0;
    }).then(function(como){
      mede('conversa-fim');
      try{ localStorage.setItem('foyer-cadeira', '1'); }catch(e){}
      try{ window.dispatchEvent(new CustomEvent('foyer-assinou')); }catch(e){}
      var ja = como === 'ja';
      c.classList.remove('anima-f', 'anima-b'); void c.offsetWidth; c.classList.add('anima-f');
      c.innerHTML = '<span class="cv-sinal cv-carimbo">🎟</span>' +
        '<h3 class="cv-t">' + (ja ? 'Você já tinha cadeira marcada.' : ('Cadeira reservada' + (R.nome ? ', ' + R.nome.split(' ')[0] : '') + '.')) + '</h3>' +
        '<p class="cv-s">' + (ja ? 'Atualizamos seus gostos. A próxima revista chega na quinta, às 7h.'
                                 : 'A próxima chega quinta, às 7h, um dia antes de todo mundo. E a cortina desta já está aberta:') + '</p>' +
        '<div class="cv-pe"><span></span><span></span><span style="display:flex;gap:8px;flex-wrap:wrap">' +
          '<button type="button" class="cv-volta" id="cv-sair">voltar ao site</button>' +
          '<a class="cv-vai" style="text-decoration:none" href="revista.html#edicoes">📖 Ler a edição de estreia</a>' +
        '</span></div>';
      var sair = c.querySelector('#cv-sair');
      if(sair) sair.addEventListener('click', fecha);
    }).catch(function(){
      c.innerHTML = '<span class="cv-sinal">✕</span>' +
        '<h3 class="cv-t">A cortina emperrou.</h3>' +
        '<p class="cv-s">Não deu para completar agora. Tenta de novo em instantes?</p>' +
        '<div class="cv-pe"><span></span><span></span><button type="button" class="cv-vai">Tentar de novo</button></div>';
      c.querySelector('.cv-vai').addEventListener('click', envia);
    });
  }
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && ov) fecha();
    if(e.key === 'Tab' && ov){
      var focaveis = ov.querySelectorAll('button, input, a[href]');
      if(!focaveis.length) return;
      var prim = focaveis[0], ult = focaveis[focaveis.length - 1];
      if(e.shiftKey && document.activeElement === prim){ e.preventDefault(); ult.focus(); }
      else if(!e.shiftKey && document.activeElement === ult){ e.preventDefault(); prim.focus(); }
    }
  });
  // gatilhos delegados: valem para botões que nascem depois (a cortina da revista)
  document.addEventListener('click', function(e){
    if(e.target.closest && e.target.closest('[data-conversa]')){ abre(); return; }
    var a = e.target.closest && e.target.closest('a[href$="revista.html#assinar"]');
    if(a){ e.preventDefault(); abre(); }   // o Assine do topo, sem viagem intermediária
  });
})();

/* ---------- "pular para o conteúdo": levar o foco junto com a tela ----------
   O atalho existe e funciona para quem usa Tab, porque o navegador guarda o
   ponto de partida. Para quem usa leitor de tela, não: a tela rolava e o
   cursor de leitura ficava parado no topo, então a pessoa apertava o atalho
   e não ouvia nada mudar. Falta ao alvo poder RECEBER foco, e é o que o
   tabindex negativo faz (recebe por programa, nunca por Tab). */
(function(){
  var alvo = document.getElementById('conteudo');
  if(alvo && !alvo.hasAttribute('tabindex')) alvo.setAttribute('tabindex', '-1');
})();

/* ---------- cortinas: a janela que cobre a tela precisa prender o foco ----------
   Quem navega só de teclado abria um destes cartões e o foco NUNCA entrava
   nele: dez toques de Tab passeavam pela página escurecida atrás da cortina,
   sem nada visível, e o Esc não fechava. Na prática, uma parede.

   O formulário de assinatura da revista já fazia isso certo; esta função é
   aquele comportamento tirado de lá e posto onde faltava. Use assim:

     var solta = prendeFoco(veu, sair);   // ao abrir
     solta();                             // ao fechar, devolve o foco

   `veu` é o elemento que cobre a tela; `sair` é a função que fecha. */
function prendeFoco(veu, sair){
  var voltarPara = document.activeElement;
  var caixa = veu.querySelector('[role="dialog"]') || veu;
  caixa.setAttribute('aria-modal', 'true');
  if(!caixa.hasAttribute('tabindex')) caixa.setAttribute('tabindex', '-1');

  function focaveis(){
    return Array.prototype.filter.call(
      veu.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])'),
      function(el){ return el.offsetWidth || el.offsetHeight || el.getClientRects().length; });
  }
  // o foco entra na primeira coisa acionável; se não houver, na própria caixa
  var primeiros = focaveis();
  (primeiros[0] || caixa).focus();

  function tecla(e){
    if(e.key === 'Escape'){ e.preventDefault(); if(sair) sair(); return; }
    if(e.key !== 'Tab') return;
    var lista = focaveis();
    if(!lista.length){ e.preventDefault(); caixa.focus(); return; }
    var primeiro = lista[0], ultimo = lista[lista.length - 1];
    if(!veu.contains(document.activeElement)){
      e.preventDefault(); (e.shiftKey ? ultimo : primeiro).focus(); return;
    }
    if(e.shiftKey && document.activeElement === primeiro){ e.preventDefault(); ultimo.focus(); }
    else if(!e.shiftKey && document.activeElement === ultimo){ e.preventDefault(); primeiro.focus(); }
  }
  document.addEventListener('keydown', tecla, true);

  return function solta(){
    document.removeEventListener('keydown', tecla, true);
    // devolve o foco a quem abriu, senão a pessoa recomeça do topo da página
    try{ if(voltarPara && voltarPara.focus) voltarPara.focus(); }catch(e){}
  };
}

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
    var solta = prendeFoco(v, function(){ fechar(); });
    function fechar(){
      try{ localStorage.setItem(K, String(Date.now())); }catch(e){}
      solta();
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
  function salvarSub(sub){
    return fetch(M.url + '/rest/v1/foyer_push', {
      method: 'POST',
      headers: { 'apikey': M.key, 'Authorization': 'Bearer ' + M.key,
                 'Content-Type': 'application/json',
                 // se o endpoint já existe, atualiza (não falha com 409): a inscrição fica sempre fresca
                 'Prefer': 'return=minimal,resolution=merge-duplicates' },
      body: JSON.stringify({ endpoint: sub.endpoint, sub: sub.toJSON() })
    });
  }
  function inscrever(){
    return navigator.serviceWorker.ready.then(function(reg){
      return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ParaBytes(PUB) });
    }).then(salvarSub);
  }
  // autocura: se a pessoa JÁ autorizou, garante que existe uma inscrição viva e a
  // reenvia ao servidor (o navegador pode trocar/expirar a inscrição sozinho; sem
  // isso, as notificações silenciosamente param de chegar mesmo com permissão dada).
  function garantirInscricao(){
    if(!suporta || Notification.permission !== 'granted') return;
    navigator.serviceWorker.ready.then(function(reg){
      return reg.pushManager.getSubscription().then(function(sub){
        if(sub) return salvarSub(sub);              // reafirma a inscrição atual
        return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ParaBytes(PUB) }).then(salvarSub);
      });
    }).catch(function(){});
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
    var solta = prendeFoco(v, function(){ sair(); });
    function sair(){ solta(); v.classList.remove('on'); setTimeout(function(){ v.remove(); }, 300); }
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

  // mantém viva a inscrição de quem já autorizou (roda em qualquer navegador, toda visita)
  garantirInscricao();

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
    // A tarja é uma pergunta, e quem usa leitor de tela precisa saber que ela
    // apareceu e do que se trata.
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Cookies no FOYER');
    b.innerHTML =
      '<p><b>🍪 Cookies no FOYER.</b> Usamos armazenamento essencial (tema, sessão) e métricas anônimas de audiência. ' +
      'Com anúncios ativos, parceiros como o Google podem usar cookies de publicidade. ' +
      'Saiba mais na <a href="privacidade.html">Política de Privacidade</a>.</p>' +
      '<div class="lgpd-acoes"><button class="lgpd-sim" type="button">Aceitar tudo</button>' +
      '<button class="lgpd-min" type="button">Só o essencial</button></div>';
    // ENTRA NO COMEÇO DO CORPO, não no fim. A tarja é presa na tela por CSS,
    // então a posição no código não muda nada do que se vê — mas muda tudo
    // para quem anda de Tab: no fim da página, o botão "Aceitar tudo" era a
    // 106ª parada na capa. Quem navega por teclado tinha de atravessar o site
    // inteiro para responder a pergunta que estava na frente dele.
    document.body.insertBefore(b, document.body.firstChild);
    var voltarPara = document.activeElement;
    // O aviso é uma tarja presa no fim da tela. Sem abrir espaço para ela, o
    // que estiver encostado no rodapé fica DEBAIXO do aviso e não recebe
    // clique — foi assim que ele engoliu as setas de virar a página da
    // revista. Aqui a página inteira sobe a altura da tarja enquanto ela
    // estiver no ar, e volta ao normal quando o leitor responde.
    function abreEspaco(){
      var alt = b.offsetHeight || 0;
      if(!alt) return;
      document.documentElement.style.setProperty('--aviso-alt', (alt + 18) + 'px');
      document.documentElement.classList.add('tem-aviso');
    }
    function fechaEspaco(){
      document.documentElement.classList.remove('tem-aviso');
      document.documentElement.style.removeProperty('--aviso-alt');
    }
    requestAnimationFrame(function(){ b.classList.add('on'); abreEspaco(); });
    window.addEventListener('resize', abreEspaco);
    function sair(){
      b.classList.remove('on'); fechaEspaco();
      window.removeEventListener('resize', abreEspaco);
      setTimeout(function(){ b.remove(); }, 300);
      // devolve o foco a onde a pessoa estava lendo: sem isso, responder o
      // aviso jogava o foco no corpo da página e o próximo Tab recomeçava
      // tudo do topo.
      try{ if(voltarPara && voltarPara.focus && document.contains(voltarPara)) voltarPara.focus(); }catch(e){}
    }
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
