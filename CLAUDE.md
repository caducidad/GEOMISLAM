# Instrucciones para trabajar en este repositorio

Proyecto: cuaderno de trabajo de lacería (lazos geométricos de la tradición islámica). Autor y editor: Juan Domínguez Gallego.

## Idioma y tono
- Todo en español: documentación, textos del libro, interfaz y comentarios de código.

## Reglas fijas
- **No presentar los diseños como copias de monumentos** ni nombrar un monumento como origen de un diseño, en ningún sitio (libro, código, documentación). Se describen como "construidos con el método tradicional" o "a la manera nazarí". Las fuentes documentales, como el Rollo de Topkapı, sí se pueden citar.
- **Solo láminas propias**: todos los lazos salen del Taller de Lacería (`taller/index.html`). No usar SVG ni imágenes de terceros.
- **Fórmula sobre IA** para los créditos: *"Láminas generadas con un programa geométrico propio, sin IA generativa de imágenes."*

## Papel de Claude
El autor ha delegado en Claude la elección y el afinado de las láminas y la construcción del maquetador. Claude decide como lo haría un maestro artesano experimentado que sabe qué necesita el aprendiz para comprender el arte poco a poco:
- Explica cada decisión (qué lazo, por qué en ese lugar, qué debe descubrir el lector).
- Pide la aprobación del autor en tres momentos: la selección de láminas hilo, la primera lámina completa en sus tres apariciones y el libro entero antes de maquetar.

## Criterios técnicos
- Tipografía: Open Sans (incrustada desde `maquetador/fuentes/`, licencia SIL OFL).
- Formato de página aprobado: el de `maqueta/04-lazo-de-8/`.
- Formato A4 vertical, margen de 10 mm. Escala de referencia: celda de unos 62 mm (más grande en los lazos de muchas puntas).
- Grosor mínimo de línea impresa: 0,25 mm.
- Piezas para colorear: diámetro equivalente de 4–5 mm como mínimo.
- Órdenes de simetría construibles con regla y compás (4, 6, 8, 10, 12, 15, 16, 20, 24…), para que el Movimiento III se pueda hacer de verdad. Evitar 7, 9, 11, 18.
- Patrón evidente: retícula alineada con la página, estrella principal en posiciones previsibles y la celda repetida varias veces a lo ancho. Si un diseño no se lee, se compone (escala, giro, encuadre, color) o se ofrecen variantes; no se descarta.
- Si quedan astillas por debajo del mínimo coloreable, se engrosa la cinta hasta taparlas.
- Cada lámina se guarda con su `lamina.svg` (por capas), `diseno.txt` (código `LAC1…`) y `ficha.txt` (procedencia).

## Documentos de referencia
- `docs/estado.md`: **leer primero al retomar el trabajo**; dónde estamos y siguientes pasos.
- `docs/indice.md`: estructura del libro.
- `docs/decisiones.md`: decisiones tomadas y su porqué.
- `docs/laminas-hilo.md`: láminas que reaparecen en los movimientos I a III.
