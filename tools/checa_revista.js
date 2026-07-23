/* Auditor de diagramação da revista do FOYER.
   Uso: node tools/checa_revista.js <url-do-leitor>
   (requer playwright-core e um Chromium; no container do Claude:
    npm i playwright-core e executablePath /opt/pw-browsers/chromium-*)
   Relata por página: estouro de conteúdo, vazio excessivo e imagem quebrada.
   Sai com código 1 se houver reprovação. */
let chromium;
try { ({ chromium } = require('playwright-core')); }
catch (e) { ({ chromium } = require(require('path').join(process.cwd(), 'node_modules', 'playwright-core'))); }
const { execSync } = require('child_process');

(async () => {
  const url = process.argv[2] || 'http://localhost:8077/revista-ed-1.html';
  let exe = process.env.CHROME_BIN;
  if (!exe) {
    try { exe = execSync('ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1').toString().trim(); } catch (e) {}
  }
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 900, height: 1250 } });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(1200);

  const laudo = await p.evaluate(() => {
    const problemas = [];
    const pgs = [...document.querySelectorAll('.rv-pg')];
    pgs.forEach((pg, i) => {
      const era = pg.classList.contains('on');
      pg.classList.add('on');
      const m = pg.querySelector('.miolo, .lista, ol, .grade');
      if (m) {
        const sobra = m.scrollHeight - m.clientHeight;
        if (sobra > 8) problemas.push({ pagina: i + 1, tipo: 'ESTOURO', px: sobra });
        const vazio = m.clientHeight - m.scrollHeight;
        // páginas de respiro (citação/mestre/capa) podem ter ar; matéria e agenda não
        const eMat = pg.classList.contains('rv-mat');
        const eAgd = pg.classList.contains('rv-agd');
        if ((eMat || eAgd) && m.clientHeight > 0) {
          const conteudo = [...m.children].reduce((a, c) => a + c.offsetHeight, 0);
          const razao = conteudo / m.clientHeight;
          if (razao < 0.55) problemas.push({ pagina: i + 1, tipo: 'MUITO-VAZIA', ocupacao: Math.round(razao * 100) + '%' });
        }
      }
      pg.querySelectorAll('img').forEach(img => {
        if (img.complete && img.naturalWidth === 0 && img.src) {
          problemas.push({ pagina: i + 1, tipo: 'IMAGEM-QUEBRADA', src: img.getAttribute('src') });
        }
      });
      if (!era) pg.classList.remove('on');
    });
    return { totalPaginas: pgs.length, problemas };
  });

  console.log(JSON.stringify(laudo, null, 1));
  await b.close();
  process.exit(laudo.problemas.length ? 1 : 0);
})();
