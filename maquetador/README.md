# Maquetador

Herramienta por construir. Leerá el SVG por capas de una lámina (exportado con el Taller de Lacería) y generará sus páginas derivadas para el libro.

## Variantes previstas

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
