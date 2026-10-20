#!/usr/bin/env python3
"""As fotos do site moram no Cloudflare R2 (20/10/2026).

POR QUE. O GitHub Pages aceita no máximo 1 GB por site, e as fotos (envios da
Coxia, acervo do Wix, miniaturas e artes de Instagram) já passavam de 800 MB,
crescendo uns 200 MB por mês. O R2 guarda 10 GB de graça, sem cobrar pela
saída, e serve as fotos de um endereço próprio (img.foyer.digital). O site
publicado no Pages fica só com as páginas, o CSS, o JS, as fontes e os logos.

O QUE ESTE SCRIPT FAZ. Roda nos fluxos que publicam o site, depois do
build_pages.py (que gera as miniaturas) e antes do envio ao Pages. Compara o
que há nas quatro pastas de fotos com o que já está no R2 e sobe só o que
falta ou mudou de tamanho. Nas miniaturas, apaga do R2 o que a montagem não
usa mais (o build já apaga do disco). Nas outras pastas nunca apaga nada: o
repositório continua sendo a cópia de segurança, e o R2 a vitrine.

AS CHAVES vêm só do ambiente (segredos do GitHub Actions): R2_ACCOUNT_ID,
R2_ACCESS_KEY_ID e R2_SECRET_ACCESS_KEY. Sem elas, o script avisa e sai com
erro, para o fluxo não publicar um site apontando para fotos que não subiram.

Uso:  python3 tools/fotos_r2.py            (sobe)
      python3 tools/fotos_r2.py --ensaio   (só conta o que subiria, sem chaves)
"""
import os, sys, mimetypes
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKET = os.environ.get('R2_BUCKET', 'foyer-fotos')

# pasta -> Cache-Control. A miniatura leva largura e tamanho de origem no
# nome: nunca muda, pode ficar guardada um ano. Foto enviada pela Coxia leva a
# hora no nome; a do acervo leva o conteúdo. A arte de Instagram é refeita
# com o mesmo nome, por isso fica só uma hora.
PASTAS = {
    'assets/uploads': 'public, max-age=2592000',
    'assets/acervo':  'public, max-age=2592000',
    'assets/thumbs':  'public, max-age=31536000, immutable',
    'assets/social':  'public, max-age=3600',
}
PODA = {'assets/thumbs'}   # onde o que sumiu do disco sai também do R2
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/avif', '.avif')

def locais():
    tudo = {}
    for pasta in PASTAS:
        base = os.path.join(ROOT, pasta)
        if not os.path.isdir(base):
            continue
        for dp, _, fs in os.walk(base):
            for f in fs:
                if f.startswith('.'):
                    continue
                cam = os.path.join(dp, f)
                rel = os.path.relpath(cam, ROOT).replace(os.sep, '/')
                tudo[rel] = os.path.getsize(cam)
    return tudo

def main():
    ensaio = '--ensaio' in sys.argv
    meus = locais()
    print(f'• {len(meus)} arquivo(s) de foto no disco, {sum(meus.values())//2**20} MB')
    if ensaio:
        for pasta in PASTAS:
            n = sum(1 for k in meus if k.startswith(pasta + '/'))
            print(f'  {pasta}: {n}')
        return 0
    conta, chave, segredo = (os.environ.get(k) for k in ('R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY'))
    if not (conta and chave and segredo):
        print('fotos_r2: faltam R2_ACCOUNT_ID / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY no ambiente', file=sys.stderr)
        return 2
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', endpoint_url=f'https://{conta}.r2.cloudflarestorage.com',
                      aws_access_key_id=chave, aws_secret_access_key=segredo, region_name='auto',
                      config=Config(max_pool_connections=32, retries={'max_attempts': 5, 'mode': 'standard'}))

    # o que já está lá (tamanho por chave)
    la = {}
    pag = s3.get_paginator('list_objects_v2')
    for pasta in PASTAS:
        for pg in pag.paginate(Bucket=BUCKET, Prefix=pasta + '/'):
            for o in pg.get('Contents') or []:
                la[o['Key']] = o['Size']
    print(f'• {len(la)} arquivo(s) já no R2')

    subir = [k for k, t in meus.items() if la.get(k) != t]
    apagar = [k for k in la if k not in meus and any(k.startswith(p + '/') for p in PODA)]
    print(f'• a subir: {len(subir)} ({sum(meus[k] for k in subir)//2**20} MB); a apagar das miniaturas: {len(apagar)}')

    erros = []
    def sobe(k):
        pasta = next(p for p in PASTAS if k.startswith(p + '/'))
        tipo = mimetypes.guess_type(k)[0] or 'application/octet-stream'
        try:
            s3.upload_file(os.path.join(ROOT, k), BUCKET, k,
                           ExtraArgs={'ContentType': tipo, 'CacheControl': PASTAS[pasta]})
        except Exception as e:
            erros.append((k, str(e)))
    with ThreadPoolExecutor(16) as ex:
        list(ex.map(sobe, subir))
    for i in range(0, len(apagar), 1000):
        s3.delete_objects(Bucket=BUCKET, Delete={'Objects': [{'Key': k} for k in apagar[i:i+1000]], 'Quiet': True})
    if erros:
        for k, e in erros[:10]:
            print(f'  falhou {k}: {e}', file=sys.stderr)
        print(f'fotos_r2: {len(erros)} envio(s) falharam', file=sys.stderr)
        return 1
    print(f'• R2 em dia: {len(subir)} enviado(s), {len(apagar)} apagado(s)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
