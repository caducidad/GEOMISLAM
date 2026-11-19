# Maquetador

Lee el SVG por capas de una lámina (exportado con el Taller de Lacería) y genera sus páginas derivadas para el libro.

## Uso

```bash
python3 maquetador/maquetar.py laminas/hilo/04-lazo-de-8 maqueta/04-lazo-de-8 "Lazo de 8"
```

```bash
node maquetador/a_pdf.js maqueta/04-lazo-de-8 lazo-de-8.pdf I-clave II-unidad III-reticula I-solucion
```

El primero escribe las páginas en SVG; el segundo crea una vista previa PNG de cada una y un PDF A4 con todas (necesita Node y Playwright).

## Páginas que genera ya

| Archivo | Movimiento | Contenido |
|---|---|---|
| `I-clave.svg` | I · Mirar | Lacería en línea, cada pieza con su letra y una leyenda de colores. La cinta queda en blanco |
| `I-solucion.svg` | Soluciones | La misma página coloreada |
| `II-unidad.svg` | II · Repetir | La unidad de repetición dibujada, la cuadrícula de casillas y los puntos para unir |
| `III-reticula.svg` | III · Reconstruir | La retícula, los puntos medios de donde salen las líneas, el polígono central con su círculo dividido, el lazo ya trazado como modelo y el ángulo marcado |

## Regla de color de la clave

La pieza mayor (la estrella principal) lleva verde; la clase más numerosa, que hace de fondo, el color más tranquilo (melado); el resto, almagra, azul, turquesa o negro como acentos. La cinta nunca se colorea.

## Variantes por construir


| Movimiento | Variante | Capas que usa |
|---|---|---|
| I · Mirar | Línea limpia para colorear, con el entrelazado visible | Cintas |
| I · Mirar | Clave de color: cada pieza con su letra o símbolo | Piezas (`data-clase`) |
| I · Mirar | Un cuarto ya coloreado | Piezas, Celda |
| I · Mirar | Seguir la cinta | Trazado central |
| II · Repetir | Unidad de repetición con sus ejes | Celda, Cintas |
| II · Repetir | Punteado y "solo vértices" | Trazado central |
| III · Reconstruir | Círculo dividido, retícula y lazo, paso a paso | Retícula, Trazado central |
| — | Soluciones en miniatura | Todas |

## Criterios de impresión

- Línea mínima: 0,25 mm.
- Pieza mínima para colorear: 4–5 mm de diámetro equivalente.
- A4 vertical con margen de 10 mm.
