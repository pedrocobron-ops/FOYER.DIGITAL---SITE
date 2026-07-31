#!/usr/bin/env bash
# =============================================================================
#  A VIRADA DO DOMÍNIO — 03/08/2026, de manhã cedo
#
#  Um arquivo vira o site inteiro. Criar o CNAME faz duas coisas de uma vez:
#  o GitHub Pages reivindica o domínio, e o gerador passa a assinar canonical,
#  og:url, sitemap e robots com ele (a leitura do CNAME está em
#  tools/build_pages.py, função _endereco_do_site).
#
#  ANTES DE RODAR, confira que o DNS já propagou:
#      dig foyer.digital +short
#  Tem que devolver os quatro endereços 185.199.10x.153. Se não devolver,
#  NÃO rode: o site sai do ar até a propagação terminar.
#
#  Uso:  bash tools/virar-dominio.sh            (vira de verdade)
#        bash tools/virar-dominio.sh --ensaio   (só mostra o que mudaria)
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

DOMINIO="foyer.digital"
ENSAIO="${1:-}"

echo "→ conferindo o DNS de $DOMINIO"
DNS_OK="$(python3 tools/dns-pages.py "$DOMINIO" 2>/dev/null || echo 0)"
if [ "$DNS_OK" -lt 2 ]; then
  echo "  ⚠  o DNS ainda não aponta para o GitHub Pages (achei $DNS_OK dos 4 endereços)."
  echo "     Rodar agora tira o site do ar. Espere a propagação."
  [ "$ENSAIO" = "--ensaio" ] || exit 1
else
  echo "  ✓ DNS propagado ($DNS_OK dos 4 endereços)"
fi

echo "→ criando o CNAME"
echo "$DOMINIO" > CNAME

echo "→ remontando o site com o endereço novo"
python3 tools/atualiza_youtube.py >/dev/null 2>&1 || echo "  (YouTube fora do ar: usa o último retrato salvo)"
python3 tools/build_pages.py >/dev/null

echo "→ conferindo o que ficou assinado"
falhou=0
for arquivo in index.html sitemap.xml robots.txt; do
  if grep -q "https://$DOMINIO" "$arquivo"; then
    echo "  ✓ $arquivo"
  else
    echo "  ✗ $arquivo NÃO recebeu o endereço novo"; falhou=1
  fi
done
if grep -rl "pedrocobron-ops.github.io" index.html sitemap.xml robots.txt >/dev/null 2>&1; then
  echo "  ✗ ainda sobrou endereço antigo"; falhou=1
else
  echo "  ✓ nenhum endereço antigo sobrou"
fi
[ "$falhou" = "0" ] || { echo "PAROU: algo não virou. Nada foi publicado."; exit 1; }

if [ "$ENSAIO" = "--ensaio" ]; then
  echo
  echo "ENSAIO: desfazendo, nada foi publicado."
  rm -f CNAME
  python3 tools/build_pages.py >/dev/null
  exit 0
fi

echo "→ publicando"
git add -A
git commit -q -m "$(cat <<'MSG'
O FOYER estreia em foyer.digital

A virada do domínio. O CNAME faz as duas coisas de uma vez: o GitHub Pages
reivindica o endereço, e o gerador passa a assinar canonical, og:url,
sitemap e robots com ele. Nenhuma página fica dizendo o endereço antigo.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
git push origin HEAD
echo
echo "✓ virada publicada. O deploy leva 2 a 3 minutos."
echo
echo "AGORA, NO GITHUB (só o Pedro pode):"
echo "  1. Settings → Pages → Custom domain: $DOMINIO → Save"
echo "  2. Esperar o certificado (de 15 minutos a 1 hora)"
echo "  3. Marcar 'Enforce HTTPS' quando deixar de estar acinzentado"
echo
echo "SÓ PUBLIQUE OS STORIES DEPOIS DO PASSO 3."
