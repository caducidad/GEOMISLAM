# Estado del proyecto y cómo retomarlo

Última actualización: 20 de noviembre de 2026.

Este documento resume dónde está el trabajo para poder retomarlo en otra conversación. Para el porqué de cada decisión, ver `docs/decisiones.md`; para la estructura del libro, `docs/indice.md`.

## En una frase

El enfoque del libro, el índice de 100 láminas y las 12 láminas hilo están decididos y aprobados; el maquetador ya genera, con formato aprobado, las tres apariciones de una lámina (probado con el lazo de 8). Toca producir el resto.

## Recorrido hasta aquí

1. Se exploró el ataurique (ornamento vegetal) y se descartó para este primer libro: queda para uno posterior.
2. Se eligió la **lacería** y el recorrido **del muro al compás**, en cuatro movimientos: I · Mirar (el alicatador), II · Repetir (el rollo del maestro), III · Reconstruir (el geómetra) y IV · Crear (el maestro).
3. Para evitar derechos de terceros, **todas las láminas se construyen con el Taller de Lacería** del autor (`taller/index.html`), al que se añadió la exportación por capas.
4. Se fijó la extensión en **100 láminas**: 12 láminas hilo que aparecen tres veces y unas 64 de acompañamiento.
5. El autor pidió **patrones visiblemente simétricos y previsibles**; los diseños difíciles no se descartan, se componen (escala, giro, encuadre, color) o se ofrecen variantes.
6. Se eligieron las **12 láminas hilo** (primer punto de aprobación, superado).
7. Se construyó el **maquetador** y se maquetó el lazo de 8 en sus tres apariciones (segundo punto de aprobación, superado). Tipografía: Open Sans.

## Puntos de aprobación del autor

| Momento | Estado |
|---|---|
| 1 · Selección de láminas hilo | Aprobado |
| 2 · Primera lámina completa en sus tres apariciones (`maqueta/04-lazo-de-8/`) | Aprobado, con Open Sans |
| 3 · El libro entero antes de maquetar | Pendiente |

## Qué hay hecho

| Pieza | Dónde | Notas |
|---|---|---|
| Taller de Lacería con exportación por capas | `taller/index.html` | Capas: fondo, estrellas, pintura, retícula, cintas y capas de datos ocultas (piezas con `data-clase`, trazado central, celda con `data-t1`/`data-t2`). Cada SVG lleva su código `LAC1…`. También relieve con luz y sombras (perfil redondeado o con arista, en su propia capa) y descarga en PNG a 300 ppp |
| 12 láminas hilo | `laminas/hilo/NN-nombre/` | `lamina.svg`, `diseno.txt`, `ficha.txt` y `vista.png`. Resumen en `laminas/hilo/resumen.png` |
| Maquetador | `maquetador/maquetar.py` y `maquetador/a_pdf.js` | Genera `I-clave`, `I-solucion`, `II-unidad` y `III-reticula` |
| Maqueta aprobada del lazo de 8 | `maqueta/04-lazo-de-8/` | SVG, PNG y PDF |
| Herramientas | `herramientas/reexportar.js`, `herramientas/medir.py` | Reexportar láminas desde su código; medir piezas y repeticiones |
| Reglas de Bourgoin | `reglas/bourgoin/` y en el Taller | 21 reglas exactas deducidas de las láminas de Bourgoin (1879), dibujables como lacería; p05, p07 y p09 pendientes |

## Próximos pasos, en orden

1. **Revisar el tamaño mínimo de pieza de las láminas 10 y 12.** Con la medición estricta de `herramientas/medir.py`, que descuenta también el borde oscuro de la cinta, la lámina 10 (lazo de 16 y 8) da 3,3 mm y la 12 (lazo de 20 y 10) 3,9 mm, por debajo del mínimo de 4 mm. Opciones: engrosar algo más la cinta o ampliar ligeramente la escala, y volver a medir.
2. **Generar las tres apariciones de las 12 láminas hilo** con el maquetador (36 páginas) y revisar que funciona con todas las retículas (girih, ruedas, roseta).
3. **Construir las variantes de página que faltan** (lista en `maquetador/README.md`): cuarto coloreado, seguir la cinta, reconocer piezas, punteado, calco y volteo, extender más allá del marco, dividir el círculo, estrellas poligonales y entrelazar.
4. **Diseñar las láminas de acompañamiento** (unas 64) en el taller: parientes de las láminas hilo con otro ángulo, separación entre cintas, rosetas o doble trazo.
5. **Textos del libro**: introducción, aperturas de los cuatro movimientos, glosario y fuentes.
6. **Montar el libro completo** y presentarlo al autor (tercer punto de aprobación).

## Unión con el proyecto de las reglas de Bourgoin (20 de noviembre de 2026)

El autor tenía otro proyecto de libro, más centrado en el método de cada patrón: lecciones de 3 o 4 páginas (analizar, completar el color, completar el dibujo, construir) con las reglas exactas sacadas de las láminas de Bourgoin. Se comparan los dos enfoques para decidir cuál se sigue y qué se toma del otro.

Decidido por el autor:
- **No se nombra ningún monumento**, también en los patrones de Bourgoin (se mantiene la regla fija).
- **Los escaneos de Bourgoin no aparecen en el libro** ni se guardan en el repositorio: solo se usan mientras se analiza cada lámina y se eliminan al terminar.
- **Formato KDP** (20,96 × 27,94 cm en tapa dura; 21,59 × 27,94 cm en tapa blanda). El número de páginas está por decidir. El formato A4 de `CLAUDE.md` y de la maqueta del lazo de 8 habrá que adaptarlo.
- Se toman del otro proyecto: las reglas de Bourgoin dentro del Taller (hecho), las convenciones gráficas al estilo de Broug para la construcción, los consejos del compás, las plantillas descargables por QR y la ficha técnica de KDP.

Por decidir más adelante: la organización del libro (lecciones seguidas por patrón o láminas que reaparecen en los movimientos) y cuántos patrones lleva.

## Decisiones abiertas

- **Impresión:** a una cara (unas 245 páginas), a doble cara los ejercicios de lápiz (unas 170) o dos volúmenes más una edición integral, como Hamonshū.
- **Visibilidad del repositorio:** es público. Conviene hacerlo privado antes de subir el libro maquetado.
- **Título del libro:** sin decidir.

## Cómo retomar en otra conversación

1. Pedir a Claude que lea `CLAUDE.md` (las reglas del proyecto) y este documento.
2. Requisitos para trabajar: Python 3, Node y Playwright con Chromium (en las sesiones en la nube de Claude Code ya vienen instalados).
3. Órdenes habituales:

```bash
python3 herramientas/medir.py laminas/hilo/*/
```

```bash
node herramientas/reexportar.js laminas/hilo/04-lazo-de-8
```

```bash
python3 maquetador/maquetar.py laminas/hilo/04-lazo-de-8 maqueta/04-lazo-de-8 "Lazo de 8"
```

```bash
node maquetador/a_pdf.js maqueta/04-lazo-de-8 lazo-de-8.pdf I-clave II-unidad III-reticula I-solucion
```

4. Mensaje sugerido para empezar: *"Lee CLAUDE.md y docs/estado.md del repositorio caducidad/GEOMISLAM y continúa con el siguiente paso pendiente."*
