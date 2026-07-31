/* ==========================================================================
   O BANCO DE ARTES DO FOYER
   As peças de divulgação do portal, desenhadas em canvas com a tipografia e
   as cores da casa. Este arquivo é a ÚNICA fonte do desenho: a Coxia usa
   para a prévia e o download, e a exportação em lote usa o mesmo código,
   então a arte que o Pedro vê na tela é exatamente a que sai em PNG.
   Criado em 31/07/2026 para o lançamento do site novo.
   ========================================================================== */
(function (raiz) {
  'use strict';

  var COR = {
    paper:'#EFE9DB', paper2:'#E6DECB', ink:'#16100D', inkSoft:'#6B6152',
    wine:'#4E0F09', wineDeep:'#380A06', gold:'#CEB26A', goldHi:'#E9CB85'
  };

  var MEDIDAS = {
    stories: { w:1080, h:1920, nome:'Stories', margem:88, topo:290, base:1620 },
    feed:    { w:1080, h:1080, nome:'Feed',    margem:78, topo:110, base:962 }
  };

  // As artes brutalistas da casa (assets/artes/), que entram atrás do texto
  // como marca d'água. Substituíram as listras de veludo em 31/07/2026: o
  // listrado brigava com a leitura e o Pedro tinha razão, não dava para ler.
  var FUNDOS = [
    { id:'refletor',   nome:'O refletor',  arq:'arte-1-refletor'  },
    { id:'cortina',    nome:'A cortina',   arq:'arte-2-cortina'   },
    { id:'plateia',    nome:'A plateia',   arq:'arte-3-plateia'   },
    { id:'arena',      nome:'A arena',     arq:'arte-4-arena'     },
    { id:'urdimento',  nome:'O urdimento', arq:'arte-5-urdimento' },
    { id:'degraus',    nome:'Os degraus',  arq:'arte-6-degraus'   }
  ];
  function arquivoFundo(id, formato) {
    var f = FUNDOS.filter(function (x) { return x.id === id; })[0];
    if (!f) return null;
    return 'assets/artes/' + f.arq + (formato === 'feed' ? '-quadrado' : '-story') + '.png';
  }

  // ---------------------------------------------------------------- desenho
  // Letra espaçada na mão: nem todo navegador tem ctx.letterSpacing, e a
  // caixa-alta espaçada é a assinatura tipográfica da casa.
  function espacado(ctx, txt, x, y, sp, align) {
    var chars = String(txt).split('');
    var larg = 0, i;
    for (i = 0; i < chars.length; i++) larg += ctx.measureText(chars[i]).width + sp;
    larg -= sp;
    var cx = align === 'center' ? x - larg / 2 : (align === 'right' ? x - larg : x);
    for (i = 0; i < chars.length; i++) {
      ctx.fillText(chars[i], cx, y);
      cx += ctx.measureText(chars[i]).width + sp;
    }
    return larg;
  }

  // Quebra o texto em linhas que cabem na largura, sem cortar palavra.
  function quebra(ctx, txt, max) {
    var palavras = String(txt).split(/\s+/), linhas = [], atual = '';
    palavras.forEach(function (p) {
      var teste = atual ? atual + ' ' + p : p;
      if (ctx.measureText(teste).width > max && atual) { linhas.push(atual); atual = p; }
      else atual = teste;
    });
    if (atual) linhas.push(atual);
    return linhas;
  }

  // A luz do refletor, que é como a casa ilumina quem entra.
  function refletor(ctx, cx, cy, r, cor) {
    var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
    g.addColorStop(0, cor); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
  }

  // A marca d'água: a arte brutalista cobrindo a peça, e por cima um véu da
  // cor da casa que empurra o desenho para o fundo. É o véu que garante a
  // leitura: sem ele o texto disputa espaço com a ilustração.
  // Desenha a arte cobrindo a peça, com um desfoque leve. O desfoque é o que
  // transforma a ilustração em TEXTURA: sem ele as arestas duras do desenho
  // brutalista viram emendas atrás das palavras e a leitura sofre.
  function cobre(ctx, m, arte, desfoque) {
    if (!(arte && arte.complete && arte.naturalWidth)) return;
    var ea = Math.max(m.w / arte.naturalWidth, m.h / arte.naturalHeight);
    var dw = arte.naturalWidth * ea, dh = arte.naturalHeight * ea;
    var x = (m.w - dw) / 2, y = (m.h - dh) / 2;
    var temFiltro = typeof ctx.filter === 'string';
    if (temFiltro && desfoque) {
      ctx.save(); ctx.filter = 'blur(' + desfoque + 'px)';
      // desenha maior que a tela para o desfoque não clarear as bordas
      ctx.drawImage(arte, x - 40, y - 40, dw + 80, dh + 80);
      ctx.restore();
    } else {
      ctx.drawImage(arte, x, y, dw, dh);
    }
  }
  function marcaDagua(ctx, m, arte, cor, veu) {
    cobre(ctx, m, arte, 9);
    ctx.globalAlpha = veu; ctx.fillStyle = cor; ctx.fillRect(0, 0, m.w, m.h); ctx.globalAlpha = 1;
    // vinheta: escurece as beiradas e afunila o olho para o miolo
    var g = ctx.createRadialGradient(m.w / 2, m.h * .42, m.w * .25, m.w / 2, m.h * .5, m.h * .72);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.42)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, m.w, m.h);
  }

  var ESTILOS = {
    // vinho fundo com letra dourada: a peça de anúncio, a mais solene
    cortina: function (ctx, m, arte) {
      ctx.fillStyle = COR.wineDeep; ctx.fillRect(0, 0, m.w, m.h);
      marcaDagua(ctx, m, arte, COR.wineDeep, .66);
      ctx.strokeStyle = COR.gold; ctx.lineWidth = 5;
      ctx.strokeRect(28, 28, m.w - 56, m.h - 56);
      return { titulo: COR.paper, texto: 'rgba(239,233,219,.90)', etiqueta: COR.gold,
               regra: COR.gold, rodape: COR.gold, logo: 'gold' };
    },
    // papel de jornal: a arte entra clarinha, como carimbo apagado
    papel: function (ctx, m, arte) {
      ctx.fillStyle = COR.paper; ctx.fillRect(0, 0, m.w, m.h);
      ctx.save(); ctx.globalAlpha = .16; cobre(ctx, m, arte, 26); ctx.restore();
      ctx.strokeStyle = COR.ink; ctx.lineWidth = 5;
      ctx.strokeRect(34, 34, m.w - 68, m.h - 68);
      ctx.lineWidth = 1.5;
      ctx.strokeRect(50, 50, m.w - 100, m.h - 100);
      ctx.fillStyle = COR.gold; ctx.fillRect(50, 50, m.w - 100, 10);
      return { titulo: COR.ink, texto: COR.inkSoft, etiqueta: COR.wine,
               regra: COR.wine, rodape: COR.wine, logo: 'wine' };
    },
    // o palco quase preto: para chamada de ação, com a arte mais presente
    palco: function (ctx, m, arte) {
      ctx.fillStyle = '#120503'; ctx.fillRect(0, 0, m.w, m.h);
      marcaDagua(ctx, m, arte, '#120503', .58);
      refletor(ctx, m.w / 2, m.h * .26, m.w * .95, 'rgba(206,178,106,.16)');
      return { titulo: COR.goldHi, texto: 'rgba(239,233,219,.88)', etiqueta: COR.gold,
               regra: 'rgba(206,178,106,.6)', rodape: COR.gold, logo: 'gold' };
    }
  };

  // ---------------------------------------------------------------- o catálogo
  // Cada peça é um argumento de venda do portal, em uma frase só.
  var PECAS = [
    { id:'estreia', fundo:'refletor', nome:'Véspera (teaser)', estilo:'palco', etiqueta:'Primeiro sinal',
      titulo:'Segunda-feira o FOYER estreia',
      linha:'O saguão do teatro brasileiro ganha casa nova: notícia todo dia, crítica em vídeo, revista toda quinta e a Enciclopédia do Teatro Musical Brasileiro.',
      itens:[], cta:'foyer.digital', recado:'segunda-feira, no ar' },
    { id:'casa-nova', fundo:'cortina', nome:'O anúncio do lançamento', estilo:'cortina', etiqueta:'Terceiro sinal',
      titulo:'O FOYER tem casa nova',
      linha:'Um portal inteiro de teatro, música e cultura. Notícia todo dia, crítica em vídeo, revista toda quinta e a Enciclopédia do Teatro Musical Brasileiro.',
      itens:['Notícias e crítica','Revista semanal','Enciclopédia','Agenda de SP e Rio'],
      cta:'foyer.digital' },
    { id:'noticias', fundo:'degraus', nome:'Notícias', estilo:'papel', etiqueta:'Notícias',
      titulo:'Teatro e cultura, todo dia',
      linha:'Matéria apurada, com fonte citada e crédito de foto. Sem caça-clique e sem release copiado.',
      itens:[], cta:'foyer.digital' },
    { id:'critica', fundo:'refletor', nome:'Crítica em vídeo', estilo:'palco', etiqueta:'Crítica',
      titulo:'A crítica que você assiste',
      linha:'Kyra Piscitelli vê o espetáculo e conta o que achou, em vídeo, com a régua sempre à mostra.',
      itens:[], cta:'foyer.digital/critica' },
    { id:'revista', fundo:'urdimento', nome:'A revista de quinta', estilo:'cortina', etiqueta:'Revista',
      titulo:'Toda quinta, uma revista de verdade',
      linha:'Uma edição fechada, com capa, pôster e acervo permanente. Assinante lê na quinta às 7h; o resto do mundo, na sexta.',
      itens:[], cta:'foyer.digital/revista' },
    { id:'enciclopedia', fundo:'arena', nome:'Enciclopédia', estilo:'papel', etiqueta:'Enciclopédia',
      titulo:'A Enciclopédia do Teatro Musical Brasileiro',
      linha:'Quem fez o quê, em que montagem, em que ano. A memória do musical brasileiro num lugar só.',
      itens:[], cta:'foyer.digital/enciclopedia' },
    { id:'agenda', fundo:'plateia', nome:'Agenda do fim de semana', estilo:'papel', etiqueta:'Agenda',
      titulo:'O que fazer no fim de semana',
      linha:'São Paulo e Rio de Janeiro, toda semana, com endereço, horário e preço. Escolha antes de sair de casa.',
      itens:[], cta:'foyer.digital/agenda' },
    { id:'programas', fundo:'arena', nome:'Programas', estilo:'palco', etiqueta:'Programas',
      titulo:'As conversas de quem faz o palco',
      linha:'Os programas do FOYER, com gente do teatro brasileiro, no YouTube e no Spotify.',
      itens:[], cta:'foyer.digital/programas' },
    { id:'assine', fundo:'plateia', nome:'Assine (captação)', estilo:'palco', etiqueta:'Assine',
      titulo:'Assine de graça',
      linha:'A revista da semana na sua caixa de entrada, antes de todo mundo. Sem spam, e seus dados ficam só com o FOYER.',
      itens:[], cta:'foyer.digital/assine' },
    { id:'anuncie', fundo:'cortina', nome:'Anuncie (produtores)', estilo:'cortina', etiqueta:'Anuncie',
      titulo:'Sua peça no saguão do teatro brasileiro',
      linha:'Monte o anúncio, veja como ele fica no site antes de qualquer compromisso e feche a conversa no WhatsApp, com gente de verdade.',
      itens:['Cortina de entrada','Entreato','Cartaz','Página na revista'],
      cta:'foyer.digital/anuncie' }
  ];

  // ---------------------------------------------------------------- pintura
  // Duas passadas: primeiro MEDE o bloco inteiro, depois desenha centrado na
  // faixa segura. No stories o Instagram cobre uns 250px em cima (nome, hora)
  // e outros 250 embaixo (caixa de resposta), então nada vital pode encostar
  // ali. Foi o erro da primeira versão: logo cortado no topo e um vazio de
  // 700px no meio da peça.
  function pinta(ctx, peca, opts) {
    opts = opts || {};
    var m = MEDIDAS[opts.formato || 'stories'];
    var stories = m.h > 1400;
    var paleta = (ESTILOS[peca.estilo] || ESTILOS.cortina)(ctx, m, opts.arte);
    var meio = m.w / 2, larg = m.w - m.margem * 2;
    ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';

    // ---- 1ª passada: monta a partitura, sem pintar nada ----
    var bloco = [], alturaTitulo = stories ? 660 : 400;
    var logoH = 0, logoW = 0;
    if (opts.logo && opts.logo.complete && opts.logo.naturalWidth) {
      logoW = stories ? 250 : 190;
      logoH = logoW * (opts.logo.naturalHeight / opts.logo.naturalWidth);
      bloco.push({ tipo:'logo', h: logoH + (stories ? 54 : 40) });
    }
    ctx.font = '600 ' + (stories ? 30 : 26) + 'px "IBM Plex Mono", monospace';
    bloco.push({ tipo:'etiqueta', h: stories ? 96 : 80 });

    var tam = stories ? 112 : 82, linhasT;
    while (true) {
      ctx.font = '400 ' + tam + 'px "Abril Fatface", Georgia, serif';
      linhasT = quebra(ctx, peca.titulo, larg);
      if (linhasT.length * tam * 1.04 <= alturaTitulo || tam <= 46) break;
      tam -= 5;
    }
    bloco.push({ tipo:'titulo', tam: tam, linhas: linhasT, h: linhasT.length * tam * 1.04 + (stories ? 46 : 30) });

    var tamL = stories ? 37 : 30;
    ctx.font = '400 ' + tamL + 'px Archivo, Helvetica, Arial, sans-serif';
    var linhasL = quebra(ctx, peca.linha, larg - (stories ? 40 : 20));
    bloco.push({ tipo:'linha', linhas: linhasL, tam: tamL, h: linhasL.length * (tamL * 1.42) });

    var itens = (peca.itens || []).filter(Boolean);
    if (itens.length) bloco.push({ tipo:'itens', h: (stories ? 40 : 26) + itens.length * (stories ? 56 : 44) });

    // ---- 2ª passada: desenha, tudo centrado na faixa segura ----
    var alturaTotal = bloco.reduce(function (a, b) { return a + b.h; }, 0);
    var faixaIni = m.topo, faixaFim = m.base - (stories ? 150 : 110);
    var y = faixaIni + Math.max(0, ((faixaFim - faixaIni) - alturaTotal) / 2);

    bloco.forEach(function (b) {
      if (b.tipo === 'logo') {
        ctx.globalAlpha = .97;
        ctx.drawImage(opts.logo, meio - logoW / 2, y, logoW, logoH);
        ctx.globalAlpha = 1;
      } else if (b.tipo === 'etiqueta') {
        ctx.fillStyle = paleta.etiqueta;
        ctx.font = '600 ' + (stories ? 30 : 26) + 'px "IBM Plex Mono", monospace';
        espacado(ctx, String(peca.etiqueta || '').toUpperCase(), meio, y + (stories ? 34 : 28), 9, 'center');
        ctx.strokeStyle = paleta.regra; ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(meio - 54, y + (stories ? 62 : 52)); ctx.lineTo(meio + 54, y + (stories ? 62 : 52));
        ctx.stroke();
      } else if (b.tipo === 'titulo') {
        ctx.fillStyle = paleta.titulo;
        ctx.font = '400 ' + b.tam + 'px "Abril Fatface", Georgia, serif';
        var yt = y;
        b.linhas.forEach(function (l) { yt += b.tam * 1.02; ctx.fillText(l, meio, yt); });
      } else if (b.tipo === 'linha') {
        ctx.fillStyle = paleta.texto;
        ctx.font = '400 ' + b.tam + 'px Archivo, Helvetica, Arial, sans-serif';
        var yl = y;
        b.linhas.forEach(function (l) { yl += b.tam * 1.42; ctx.fillText(l, meio, yl); });
      } else if (b.tipo === 'itens') {
        var yi = y + (stories ? 44 : 30);
        ctx.font = '600 ' + (stories ? 29 : 24) + 'px "IBM Plex Mono", monospace';
        ctx.fillStyle = paleta.etiqueta;
        itens.forEach(function (it) {
          espacado(ctx, '\u25C6  ' + String(it).toUpperCase(), meio, yi, 6, 'center');
          yi += stories ? 56 : 44;
        });
      }
      y += b.h;
    });

    // ---- o rodapé: o endereço, que é o motivo da peça existir ----
    var yb = m.base;
    ctx.strokeStyle = paleta.regra; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(m.margem + 30, yb - 66); ctx.lineTo(m.w - m.margem - 30, yb - 66); ctx.stroke();
    ctx.fillStyle = paleta.rodape;
    ctx.font = '600 ' + (stories ? 46 : 38) + 'px "IBM Plex Mono", monospace';
    espacado(ctx, String(peca.cta || 'foyer.digital').toUpperCase(), meio, yb, 6, 'center');
    var recado = opts.recado !== undefined ? opts.recado
               : (peca.recado !== undefined ? peca.recado : 'o link está na bio');
    if (recado) {
      ctx.fillStyle = paleta.texto;
      ctx.font = '400 ' + (stories ? 27 : 23) + 'px Archivo, Helvetica, Arial, sans-serif';
      ctx.fillText(recado, meio, yb + (stories ? 48 : 40));
    }
    ctx.textAlign = 'left';
    return m;
  }

  raiz.FoyerArtes = {
    COR: COR, MEDIDAS: MEDIDAS, PECAS: PECAS, ESTILOS: Object.keys(ESTILOS),
    FUNDOS: FUNDOS, arquivoFundo: arquivoFundo,
    pinta: pinta,
    // carrega as fontes da casa antes de desenhar (senão o canvas usa a de sistema)
    prontas: function () {
      if (!raiz.document || !document.fonts) return Promise.resolve();
      var quero = ['400 108px "Abril Fatface"', '400 36px Archivo', '600 30px "IBM Plex Mono"'];
      return Promise.all(quero.map(function (f) { return document.fonts.load(f); }))
        .then(function () { return document.fonts.ready; });
    }
  };
})(typeof window !== 'undefined' ? window : this);
