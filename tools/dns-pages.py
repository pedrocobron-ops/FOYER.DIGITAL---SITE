#!/usr/bin/env python3
"""Quantos dos quatro endereços do GitHub Pages o domínio já devolve.
Serve de trava para a virada do domínio: enquanto for menos de 2, publicar o
CNAME tira o site do ar. Uso: python3 tools/dns-pages.py foyer.digital"""
import socket, sys

PAGES = {'185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153'}

def quantos(dominio):
    try:
        achados = {i[4][0] for i in socket.getaddrinfo(dominio, 80, socket.AF_INET)}
    except Exception:
        achados = set()
    return len(achados & PAGES)

if __name__ == '__main__':
    print(quantos(sys.argv[1] if len(sys.argv) > 1 else 'foyer.digital'))
