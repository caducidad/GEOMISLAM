#!/usr/bin/env python3
"""Mide una o varias láminas exportadas por capas.

Para cada lamina.svg informa de:
  - tipos de pieza visibles (clases de forma),
  - pieza visible más pequeña, en mm de diámetro equivalente, descontando el ancho de la cinta,
  - repeticiones de la celda a lo ancho de la página.

Criterios del libro: pieza mínima de 4–5 mm y patrón evidente (varias repeticiones a lo ancho).

Uso: python3 herramientas/medir.py laminas/hilo/*/
"""
import re, math, sys, os

K = 96 / 25.4                          # px por mm
W, H = (210 - 20) * K, (297 - 20) * K  # zona útil de un A4 con margen de 10 mm

def medir(carpeta):
    s = open(os.path.join(carpeta, 'lamina.svg'), encoding='utf-8').read()
    # ancho de la cinta: el trazo claro de la capa de cintas (segundo stroke-width de la capa)
    cin = re.search(r'id="cintas".*?</g>', s, re.S).group(0)
    anchos = [float(x) for x in re.findall(r'stroke-width="([\d.]+)"', cin)]
    banda = (sorted(anchos)[len(anchos) // 2] if anchos else 7) / K
    g = re.search(r'id="piezas".*?</g>', s, re.S).group(0); cls = {}
    for c, d in re.findall(r'data-clase="(-?\d+)"[^>]*d="([^"]+)"', g):
        n = list(map(float, re.findall(r'-?\d+\.?\d*', d))); P = list(zip(n[0::2], n[1::2]))
        if min(p[0] for p in P) < 0 or min(p[1] for p in P) < 0 or max(p[0] for p in P) > W or max(p[1] for p in P) > H: continue
        a = abs(sum(P[i][0] * P[i - 1][1] - P[i - 1][0] * P[i][1] for i in range(len(P)))) / 2 / K / K
        cls.setdefault(c, []).append(2 * math.sqrt(a / math.pi))
    vis = {c: min(v) - banda for c, v in cls.items() if min(v) - banda > 0.3}
    t1, t2 = [tuple(map(float, x.split(','))) for x in re.search(r'data-t1="([^"]+)" data-t2="([^"]+)"', s).groups()]
    per = min(abs(v[0]) for v in (t1, t2, (t1[0] + t2[0],), (t1[0] - t2[0],)) if abs(v[0]) > 5)
    return len(vis), (min(vis.values()) if vis else 0), W / per

if __name__ == '__main__':
    for d in sys.argv[1:]:
        if not os.path.exists(os.path.join(d, 'lamina.svg')): continue
        n, mn, rep = medir(d)
        print(f'{os.path.basename(os.path.normpath(d)):26s} tipos de pieza {n:2d} · pieza mínima {mn:5.1f} mm · repeticiones a lo ancho {rep:4.1f}')
