#!/usr/bin/env python3
"""Maquetador del cuaderno de lacería.

Lee una lámina exportada por capas con el Taller de Lacería (lamina.svg) y genera sus páginas:
  I-clave.svg      Movimiento I · Mirar: colorear por clave
  I-solucion.svg   la misma página coloreada (para las soluciones en miniatura)
  II-unidad.svg    Movimiento II · Repetir: la unidad de repetición y puntos para unir
  III-reticula.svg Movimiento III · Reconstruir: del círculo a la retícula y al lazo

Uso: python3 maquetar.py <carpeta de la lámina> <carpeta de salida> "<nombre visible>"
"""
import math, re, sys, os, html
import xml.etree.ElementTree as ET, base64

# Open Sans (licencia SIL OFL, ver fuentes/OFL.txt), incrustada en cada página para que el PDF use la fuente real
_FUENTE_B64 = base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'OpenSans-latin.woff2'), 'rb').read()).decode()
ESTILO_FUENTE = ("<style>@font-face{font-family:'Open Sans';font-weight:300 800;"
                 f"src:url(data:font/woff2;base64,{_FUENTE_B64}) format('woff2');}}</style>")

NS = {'s': 'http://www.w3.org/2000/svg', 'i': 'http://www.inkscape.org/namespaces/inkscape'}
K = 96 / 25.4                                   # px por mm (la escala del taller)
TINTA, GRIS, GRIS_CLARO = '#1c1c1c', '#7a7a7a', '#c4c4c4'
FUENTE = "'Open Sans',sans-serif"
# paleta tradicional para la clave de color (de la pieza mayor a la menor)
CLAVE = [('verde', '#1f6b55'), ('almagra', '#a8452c'), ('melado', '#d6a13f'), ('azul', '#284a7c'),
         ('negro', '#232323'), ('turquesa', '#2f8f95')]

# ---------- lectura de la lámina ----------
def puntos(d):
    n = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', d)))
    return list(zip(n[0::2], n[1::2]))

def subrutas(d):
    """Una ruta con varios M…Z se separa en polígonos."""
    return [puntos(m) for m in re.findall(r'M[^M]+', d)]

def area(P):
    return abs(sum(P[i][0] * P[i - 1][1] - P[i - 1][0] * P[i][1] for i in range(len(P)))) / 2

def centroide(P):
    a = 0; cx = cy = 0
    for i in range(len(P)):
        x0, y0 = P[i - 1]; x1, y1 = P[i]; c = x0 * y1 - x1 * y0
        a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    if abs(a) < 1e-9: return (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
    return (cx / (3 * a), cy / (3 * a))

def dentro(pt, P):
    x, y = pt; r = False
    for i in range(len(P)):
        x0, y0 = P[i - 1]; x1, y1 = P[i]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0): r = not r
    return r

def leer(ruta):
    txt = open(ruta, encoding='utf-8').read()
    raiz = ET.fromstring(txt.encode('utf-8'))
    vb = list(map(float, raiz.get('viewBox').split()))
    capas = {g.get('id'): g for g in raiz.findall('s:g', NS)}
    off = 0.0
    m = re.search(r'translate\(([\d.]+)', capas['fondo'].get('transform') or '')
    if m: off = float(m.group(1))
    L = dict(W=vb[2], H=vb[3], off=off, iw=vb[2] - 2 * off, ih=vb[3] - 2 * off)
    L['piezas'] = [dict(clase=int(p.get('data-clase')), P=puntos(p.get('d'))) for p in capas['piezas'].findall('s:path', NS)]
    L['trazado'] = [dict(P=puntos(p.get('d')), cerrada=p.get('data-cerrada') == '1') for p in capas['trazado'].findall('s:path', NS)]
    L['reticula'] = []
    for p in capas['reticula'].findall('s:path', NS):
        for P in subrutas(p.get('d')): L['reticula'].append(dict(tipo=p.get('data-tipo'), P=P))
    c = capas['celda'].find('s:path', NS)
    L['celda'] = dict(P=puntos(c.get('d')), t1=tuple(map(float, c.get('data-t1').split(','))), t2=tuple(map(float, c.get('data-t2').split(','))))
    # cintas: se copian tal cual (conservan el entrelazado) y se recolorean
    L['cintas'] = ''.join(ET.tostring(e, encoding='unicode') for e in capas['cintas']).replace('ns0:', '').replace(' xmlns:ns0="http://www.w3.org/2000/svg"', '')
    cols = re.findall(r'stroke="(#[0-9a-fA-F]{3,6})"', L['cintas'])
    L['col_borde'], L['col_cinta'] = cols[0], cols[1]
    m = re.search(r'<codigo-diseno>([^<]+)', txt); L['codigo'] = m.group(1) if m else ''
    return L

# ---------- composición de página ----------
CAB, PIE = 9.0 * K, 24.0 * K           # franja de cabecera (en el margen) y de pie, en px

def pagina(L, cuerpo, cabecera, pie, extra_pie=''):
    W, H, off = L['W'], L['H'], L['off']
    zona_h = L['ih'] - PIE
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 {W:.1f} {H:.1f}">'
            f'<defs>{ESTILO_FUENTE}<clipPath id="zona"><rect width="{L["iw"]:.1f}" height="{zona_h:.1f}"/></clipPath></defs>'
            f'<rect width="{W:.1f}" height="{H:.1f}" fill="#fff"/>'
            f'<text x="{off:.1f}" y="{off - 3.2 * K:.1f}" font-family="{FUENTE}" font-size="{2.9 * K:.1f}" fill="{GRIS}">{html.escape(cabecera)}</text>'
            f'<g transform="translate({off:.1f},{off:.1f})"><g clip-path="url(#zona)">{cuerpo}</g>'
            f'<rect width="{L["iw"]:.1f}" height="{zona_h:.1f}" fill="none" stroke="{GRIS_CLARO}" stroke-width="0.8"/>'
            f'<text x="0" y="{zona_h + 7.5 * K:.1f}" font-family="{FUENTE}" font-size="{3.3 * K:.1f}" fill="{TINTA}">{html.escape(pie)}</text>'
            f'{extra_pie}</g></svg>')

def poly_d(P, cerrar=True):
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in P) + ('Z' if cerrar else '')

def cintas_en(L, borde, cinta):
    return L['cintas'].replace(f'stroke="{L["col_borde"]}"', f'stroke="{borde}"').replace(f'stroke="{L["col_cinta"]}"', f'stroke="{cinta}"')

def clases_por_tamano(L):
    """Clases de pieza ordenadas de mayor a menor área (letra A = la mayor)."""
    ar = {}
    for p in L['piezas']: ar.setdefault(p['clase'], []).append(area(p['P']))
    orden = sorted(ar, key=lambda c: -max(ar[c]))
    return {c: i for i, c in enumerate(orden)}

def colores_clave(L, rango):
    """Regla de oficio: la pieza mayor (la estrella principal) lleva verde; la clase más numerosa,
    que es el fondo del dibujo, el color más tranquilo (melado); el resto, almagra, azul… como acentos."""
    cuenta = {}
    for p in L['piezas']:
        if pieza_entera(L, p['P']): cuenta[p['clase']] = cuenta.get(p['clase'], 0) + 1
    orden = sorted(rango, key=lambda c: rango[c])
    mayor = orden[0]; numerosa = max((c for c in orden if c != mayor), key=lambda c: cuenta.get(c, 0), default=None)
    paleta = {'verde': '#1f6b55', 'melado': '#d6a13f'}
    acentos = [('almagra', '#a8452c'), ('azul', '#284a7c'), ('turquesa', '#2f8f95'), ('negro', '#232323')]
    col = {mayor: ('verde', paleta['verde'])}
    if numerosa is not None: col[numerosa] = ('melado', paleta['melado'])
    for c in orden:
        if c not in col: col[c] = acentos.pop(0) if acentos else ('blanco', '#ffffff')
    return col

def pieza_entera(L, P, margen=2):
    zh = L['ih'] - PIE
    return all(margen <= x <= L['iw'] - margen and margen <= y <= zh - margen for x, y in P)

# ---------- I · Mirar: colorear por clave ----------
def pagina_clave(L, nombre, coloreada=False):
    rango = clases_por_tamano(L)
    col = colores_clave(L, rango)
    cuerpo = []
    for p in L['piezas']:
        fill = col[p['clase']][1] if coloreada else '#fff'
        cuerpo.append(f'<path d="{poly_d(p["P"])}" fill="{fill}"/>')
    cuerpo.append(cintas_en(L, TINTA, '#fff'))
    if not coloreada:
        for p in L['piezas']:
            if not pieza_entera(L, p['P']): continue
            cx, cy = centroide(p['P']); d = 2 * math.sqrt(area(p['P']) / math.pi)
            fs = max(2.0 * K, min(3.6 * K, 0.32 * d))
            letra = chr(65 + rango[p['clase']])
            cuerpo.append(f'<text x="{cx:.1f}" y="{cy + fs * 0.36:.1f}" text-anchor="middle" font-family="{FUENTE}" '
                          f'font-size="{fs:.1f}" fill="{GRIS}">{letra}</text>')
    # leyenda: letra, muestra de color y nombre
    zh = L['ih'] - PIE; y = zh + 15 * K; x = 0; leyenda = []
    for c, r in sorted(rango.items(), key=lambda t: t[1]):
        nombre_col, color = col[c]
        leyenda.append(f'<rect x="{x:.1f}" y="{y - 4.2 * K:.1f}" width="{5 * K:.1f}" height="{5 * K:.1f}" rx="{0.8 * K:.1f}" fill="{color}" stroke="{TINTA}" stroke-width="0.6"/>'
                       f'<text x="{x + 6.5 * K:.1f}" y="{y:.1f}" font-family="{FUENTE}" font-size="{3.3 * K:.1f}" fill="{TINTA}">'
                       f'<tspan font-weight="700">{chr(65 + r)}</tspan> {nombre_col}</text>')
        x += 32 * K
    leyenda.append(f'<rect x="{x:.1f}" y="{y - 4.2 * K:.1f}" width="{5 * K:.1f}" height="{5 * K:.1f}" rx="{0.8 * K:.1f}" fill="#fff" stroke="{TINTA}" stroke-width="0.6"/>'
                   f'<text x="{x + 6.5 * K:.1f}" y="{y:.1f}" font-family="{FUENTE}" font-size="{3.3 * K:.1f}" fill="{TINTA}">cinta: sin color</text>')
    if coloreada:
        return pagina(L, ''.join(cuerpo), f'Solución · I · Mirar · Colorear por clave · {nombre}', 'Cada tipo de pieza lleva siempre el mismo color.', ''.join(leyenda))
    return pagina(L, ''.join(cuerpo), f'I · Mirar · Colorear por clave · {nombre}',
                  'Colorea cada pieza con el color de su letra. Deja la cinta en blanco.', ''.join(leyenda))

# ---------- II · Repetir: la unidad y los puntos ----------
def pagina_unidad(L, nombre):
    c = L['celda']; t1, t2 = c['t1'], c['t2']; o = c['P'][0]
    o = (o[0] - (t1[0] + t2[0]) / 2, o[1] - (t1[1] + t2[1]) / 2)          # celda centrada en la estrella
    unidad = [o, (o[0] + t1[0], o[1] + t1[1]), (o[0] + t1[0] + t2[0], o[1] + t1[1] + t2[1]), (o[0] + t2[0], o[1] + t2[1])]
    cuerpo = []
    # cuadrícula de casillas (todas las copias de la unidad)
    lineas = []
    for k in range(-12, 13):
        for (a, b) in ((t1, t2), (t2, t1)):
            p0 = (o[0] + k * a[0] - 20 * b[0], o[1] + k * a[1] - 20 * b[1]); p1 = (p0[0] + 40 * b[0], p0[1] + 40 * b[1])
            lineas.append(f'M{p0[0]:.1f} {p0[1]:.1f}L{p1[0]:.1f} {p1[1]:.1f}')
    cuerpo.append(f'<path d="{"".join(lineas)}" stroke="{GRIS_CLARO}" stroke-width="0.8" stroke-dasharray="4 3" fill="none"/>')
    # puntos: todos los vértices del trazado
    vistos = set(); dots = []
    for t in L['trazado']:
        for x, y in t['P']:
            k = (round(x * 2), round(y * 2))
            if k in vistos or not (-5 < x < L['iw'] + 5 and -5 < y < L['ih'] + 5): continue
            vistos.add(k); dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.7"/>')
    cuerpo.append(f'<g fill="{GRIS}">{"".join(dots)}</g>')
    # la unidad dibujada entera
    tr = ''.join(poly_d(t['P'], t['cerrada']) for t in L['trazado'])
    cuerpo.append(f'<clipPath id="unidad"><path d="{poly_d(unidad)}"/></clipPath>'
                  f'<path d="{poly_d(unidad)}" fill="#f6f1e6"/>'
                  f'<path d="{tr}" clip-path="url(#unidad)" fill="none" stroke="{TINTA}" stroke-width="1.6" stroke-linejoin="round"/>'
                  f'<path d="{poly_d(unidad)}" fill="none" stroke="#9c7a3c" stroke-width="1.4"/>')
    return pagina(L, ''.join(cuerpo), f'II · Repetir · Unir los puntos · {nombre}',
                  'La casilla dibujada es la unidad que se repite. Une los puntos para repetirla en cada casilla.')

# ---------- III · Reconstruir: del círculo a la retícula y al lazo ----------
def pagina_reticula(L, nombre, theta):
    zh = L['ih'] - PIE; cen = (L['iw'] / 2, zh / 2)
    cuerpo = [f'<path d="{"".join(poly_d(t["P"]) for t in L["reticula"])}" fill="none" stroke="#a9a9a9" stroke-width="0.9"/>']
    # puntos medios de todos los lados: de ahí salen las líneas
    vistos = set(); dots = []
    for t in L['reticula']:
        P = t['P']
        for i in range(len(P)):
            mx, my = (P[i - 1][0] + P[i][0]) / 2, (P[i - 1][1] + P[i][1]) / 2
            k = (round(mx * 2), round(my * 2))
            if k in vistos: continue
            vistos.add(k); dots.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="1.9"/>')
    cuerpo.append(f'<g fill="{TINTA}">{"".join(dots)}</g>')
    # modelo: el polígono mayor que contiene el centro, con su círculo dividido y el lazo ya trazado
    tipos = sorted({t['tipo'] for t in L['reticula']}, key=lambda s: -int(s) if s.isdigit() else 0)
    grande = next(t for t in L['reticula'] if t['tipo'] == tipos[0] and dentro(cen, t['P']))
    gc = centroide(grande['P']); R = math.dist(gc, grande['P'][0])
    vecino = min((t for t in L['reticula'] if t is not grande and centroide(t['P'])[0] > gc[0] + 1),
                 key=lambda t: math.dist(centroide(t['P']), gc))
    radios = ''.join(f'M{gc[0]:.1f} {gc[1]:.1f}L{x:.1f} {y:.1f}' for x, y in grande['P'])
    cuerpo.append(f'<circle cx="{gc[0]:.1f}" cy="{gc[1]:.1f}" r="{R:.1f}" fill="none" stroke="#9c7a3c" stroke-width="1.1" stroke-dasharray="5 3"/>'
                  f'<path d="{radios}" stroke="#9c7a3c" stroke-width="0.8" stroke-dasharray="3 3" fill="none"/>'
                  f'<circle cx="{gc[0]:.1f}" cy="{gc[1]:.1f}" r="2" fill="#9c7a3c"/>')
    tr = ''.join(poly_d(t['P'], t['cerrada']) for t in L['trazado'])
    for i, t in enumerate((grande, vecino)):
        cuerpo.append(f'<clipPath id="modelo{i}"><path d="{poly_d(t["P"])}"/></clipPath>'
                      f'<path d="{tr}" clip-path="url(#modelo{i})" fill="none" stroke="{TINTA}" stroke-width="1.7" stroke-linejoin="round"/>')
    # marca del ángulo en un punto medio del polígono modelo
    a, b = grande['P'][0], grande['P'][1]
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    ex, ey = (b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b)
    nx, ny = -ey, ex
    if (gc[0] - mx) * nx + (gc[1] - my) * ny < 0: nx, ny = -nx, -ny
    th = math.radians(theta); r = 7 * K
    p1 = (mx + ex * r, my + ey * r); p2 = (mx + (math.cos(th) * ex + math.sin(th) * nx) * r, my + (math.cos(th) * ey + math.sin(th) * ny) * r)
    sweep = 1 if ex * ny - ey * nx > 0 else 0
    lx, ly = mx + (math.cos(th / 2) * ex + math.sin(th / 2) * nx) * r * 1.55, my + (math.cos(th / 2) * ey + math.sin(th / 2) * ny) * r * 1.55
    cuerpo.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}A{r:.1f} {r:.1f} 0 0 {sweep} {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="#9c7a3c" stroke-width="1.1"/>'
                  f'<text x="{lx:.1f}" y="{ly + 1.2 * K:.1f}" text-anchor="middle" font-family="{FUENTE}" font-size="{3 * K:.1f}" fill="#7a5a22" '
                  f'stroke="#fff" stroke-width="3" paint-order="stroke">{str(theta).replace(".", ",")}°</text>')
    return pagina(L, ''.join(cuerpo), f'III · Reconstruir · De la retícula al lazo · {nombre}',
                  f'De cada punto salen dos líneas a {str(theta).replace(".", ",")}° del lado. Prolóngalas hasta que se encuentren; el centro es tu modelo.')

def main():
    ent, sal, nombre = sys.argv[1], sys.argv[2], sys.argv[3]
    L = leer(os.path.join(ent, 'lamina.svg'))
    ficha = open(os.path.join(ent, 'ficha.txt'), encoding='utf-8').read()
    theta = float(re.search(r'θ = ([\d.]+)', ficha).group(1)) if 'θ = ' in ficha else 0
    theta = int(theta) if theta == int(theta) else theta
    os.makedirs(sal, exist_ok=True)
    pags = {'I-clave': pagina_clave(L, nombre), 'I-solucion': pagina_clave(L, nombre, True),
            'II-unidad': pagina_unidad(L, nombre), 'III-reticula': pagina_reticula(L, nombre, theta)}
    for k, v in pags.items():
        open(os.path.join(sal, k + '.svg'), 'w', encoding='utf-8').write(v)
    print('Páginas:', ', '.join(pags))

if __name__ == '__main__':
    main()
