#!/usr/bin/env bash
# O QUE VAI PARA O AR (12/10/2026, auditoria achados 89, 2, 61 e 76).
#
# Roda na raiz do repositório, depois do build e antes do upload do GitHub
# Pages, nos três fluxos que publicam o site (pages.yml, agendadas.yml e
# youtube.yml). Mexe só na cópia de trabalho da Action: nada sai do
# repositório.
#
# Antes saía a raiz inteira menos a fila e as pautas: o código das funções do
# Supabase (com segredos), as ferramentas, os manuais internos e o
# import/equipe.json (com o sal e o hash das senhas da Coxia) respondiam 200
# em foyer.digital. Agora só sobe o que o leitor e a Coxia buscam pelo próprio
# site. De import/ ficam apenas:
#   import/anuncios/site.json  anuncie.html lê as vagas de anúncio
#   import/materias.json       a Coxia lê o acervo (busca e edição)
#   import/opiniao.json        a Coxia lê a lista de colunistas
#   import/corpo/              a Coxia abre o texto da matéria publicada
# Todo o resto de import/ a Coxia lê pela API do GitHub, e o build_pages.py lê
# do disco antes deste passo. O socorro de login da Coxia deixou de usar a
# cópia do site e lê a equipe do raw.githubusercontent.
#
# Ao acrescentar um fetch('import/...') no site ou na Coxia, inclua o arquivo
# aqui, senão ele dá 404 no ar.
set -euo pipefail

fica=$(mktemp -d)
mkdir -p "$fica/anuncios"
mv import/anuncios/site.json "$fica/anuncios/"
mv import/materias.json import/opiniao.json import/corpo "$fica/"
rm -rf import
mv "$fica" import
chmod 755 import   # o mktemp nasce fechado (700); o Pages precisa ler

# ferramentas, funções do servidor, configuração do repositório e manuais
rm -rf tools supabase .github .gitignore
find . -type f \( -name '*.md' -o -name '*.py' -o -name '*.sh' -o -name '*.ts' \) -not -path './.git/*' -print -delete

# Artes de Instagram (feed e stories, cerca de 200 MB): o leitor não as vê e a
# Coxia já as abre e baixa pelo raw.githubusercontent, em qualidade cheia.
# Fora do site publicado, ele cabe em 1 GB, o limite do GitHub Pages, mesmo
# com as fotos em qualidade maior (15/10/2026). A prévia de link das colunas
# sem foto (*-og.jpg) fica: é ela que aparece no WhatsApp.
find assets/social -type f \( -name '*-feed.jpg' -o -name '*-story.jpg' \) -delete 2>/dev/null || true

# o que o site e a Coxia não podem perder
for f in import/anuncios/site.json import/materias.json import/opiniao.json import/corpo \
         index.html coxia/index.html assets/site.js robots.txt sitemap.xml; do
  test -e "$f" || { echo "faltou $f no site publicado"; exit 1; }
done
echo "site publicado: só o que o leitor e a Coxia usam"
