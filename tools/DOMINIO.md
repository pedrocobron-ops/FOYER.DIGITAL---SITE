# Chegada do domínio foyer.digital — roteiro do dia 03/08/2026

Checklist na ordem exata. Nada aqui é destrutivo até o passo 4; dá para voltar
atrás a qualquer momento removendo o arquivo CNAME.

## 0. O RETRATO DE ANTES — para desfazer, se precisar

Estado do domínio em 02/08/2026, 12h20 de Brasília, antes de mexer em nada.
Registrador: GoDaddy (vence 24/06/2027). DNS: nameservers da Wix
(`ns4.wixdns.net`, `ns5.wixdns.net`), então quem manda nos registros é o
painel da Wix. TTL de 1 hora — mudanças levam até uma hora para valer para
todo mundo.

| O quê | Valor de antes |
|---|---|
| `A` de `foyer.digital` | `185.230.63.186`, `185.230.63.171`, `185.230.63.107` (Wix) |
| `CNAME` de `www` | `cdn1.wixdns.net` |
| `MX` | `aspmx.l.google.com` (10), `alt1` (20), `alt2` (30), `alt3` (40), `alt4` (50) |
| `TXT` | `v=spf1 include:_spf.google.com ~all` |
| `TXT` | `google-site-verification=JIdgUmQ6Rhk8ZCyaMWJNAX9JUiDGQ6whWs5KxJahbM8` |
| `TXT` | `google-site-verification=D_UqCmCcYkqqKg8YGniJZfd_UAqmfHZolfj5TUKSneE` |
| `CAA` | nenhum |
| `_dmarc` | nenhum |

**Para voltar atrás:** devolver os três `A` e o `CNAME` de `www` acima, e
apagar o arquivo `CNAME` da raiz do repositório. O site antigo volta em até
uma hora.

**Nunca mexer no `MX` nem nos `TXT`:** são o e-mail da empresa
(`pedroamaral@foyer.digital`) e a verificação do Google. Trocar o site não
tem nada a ver com o e-mail — o e-mail continua na Google, onde sempre esteve.

## 1. DNS (no painel onde o domínio está registrado)

- Registro `A` de `foyer.digital` para os IPs do GitHub Pages:
  `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- Registro `CNAME` de `www.foyer.digital` → `pedrocobron-ops.github.io`
- TTL baixo (300s) facilita ajustes no dia.

## 2. GitHub Pages

- Repositório → Settings → Pages → Custom domain: `foyer.digital`
  (isso cria o arquivo `CNAME` na publicação; como o deploy é por Actions,
  TAMBÉM criar o arquivo `CNAME` na raiz do repositório com o conteúdo
  `foyer.digital` para ele ir junto em cada deploy).
- Aguardar o certificado e marcar **Enforce HTTPS**.
- O GitHub redireciona sozinho os endereços antigos
  `pedrocobron-ops.github.io/FOYER.DIGITAL---SITE/...` para o domínio novo
  (importante: preserva os links já indexados).

## 3. O site

- Em `tools/build_pages.py`, trocar a linha do `BASE` para
  `https://foyer.digital` (ou exportar `FOYER_BASE=https://foyer.digital`
  no workflow) e fazer push: canonical, og:url, sitemaps, feed e JSON-LD
  passam todos para o domínio novo num build só.
- Conferir no ar: `curl -s https://foyer.digital/robots.txt` deve listar os
  sitemaps já com o domínio novo.

## 4. Google Search Console

- Criar propriedade **Domínio** (`foyer.digital`) com verificação por DNS TXT.
- Enviar `sitemap.xml` e `sitemap-news.xml`.
- Em seguida (não precisa esperar indexar): Publisher Center.

## 5. Google Publisher Center (Google Notícias)

- publishercenter.google.com → adicionar publicação "FOYER",
  território Brasil, idioma português.
- Fonte: o domínio verificado no Search Console (mesma conta Google).
- Logo quadrada e retangular: `assets/logo/pwa-512.png` e
  `assets/logo/src/foyer-banner.png`.
- Seções sugeridas: Notícias (feed.xml), Em Cartaz (cat-em-cartaz.html),
  Guias (cat-guia.html), Bastidores (cat-bastidores.html).

## 6. AdSense + LGPD (depois do Publisher Center)

- Pedir revisão do site no AdSense com o domínio novo.
- Ativar o banner de consentimento LGPD/cookies antes de rodar anúncios
  (pendência conhecida; implementar quando o AdSense aprovar).

## 7. Supabase e app (nada quebra, mas conferir)

- Métricas/newsletter: continuam funcionando (chamadas saem do navegador
  para o Supabase, independem do domínio).
- Aplicativo instalado: quem instalou pelo endereço antigo continua
  funcionando via redirecionamento; novas instalações já nascem no domínio.
- Notificações: sem mudança (as inscrições são por navegador, não por URL).

## 8. Wix

- Só cancelar o Wix DEPOIS de confirmar o domínio apontado e o site no ar
  (as imagens já são 100% locais desde 23/07; nenhuma dependência restante).
