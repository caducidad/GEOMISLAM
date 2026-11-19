# GEOMISLAM · Cuaderno de lacería

Casa del proyecto de un cuaderno de trabajo sobre **lacería**: los lazos de estrellas entrelazadas de la tradición geométrica islámica.

El libro propone un recorrido **del muro al compás**. El lector empieza delante de la obra terminada y retrocede, lámina a lámina, hasta la geometría que la originó: primero colorea, luego repite, después reconstruye desde el círculo y por último crea sus propios lazos.

> **Objetivo:** que el lector aprenda a ver cómo un pequeño fragmento genera un ornamento sin fin, y acabe creando el suyo, disfrutando del proceso y del resultado.

## Estado

| Parte | Estado |
|---|---|
| Índice del libro | Definido · [`docs/indice.md`](docs/indice.md) |
| Decisiones de enfoque | Registradas · [`docs/decisiones.md`](docs/decisiones.md) |
| Taller de diseño (aplicación) | Funcionando, con exportación por capas · [`taller/`](taller/) |
| Láminas hilo | Propuesta de 6, pendiente de aprobación · [`docs/laminas-hilo.md`](docs/laminas-hilo.md) |
| Maquetador | Por construir · [`maquetador/`](maquetador/) |

## Estructura

```
taller/        Taller de Lacería: la aplicación con la que se diseñan todos los lazos
laminas/hilo/  Las láminas que reaparecen en los movimientos I, II y III
               (cada una con su SVG por capas, su código de diseño y su ficha de procedencia)
maquetador/    Herramienta que convierte una lámina en todas sus páginas derivadas
docs/          Índice del libro, decisiones y criterios
```

## El libro en cuatro movimientos

| Movimiento | Figura | Qué hace el lector |
|---|---|---|
| I · Mirar | El alicatador | Colorea por clave, reconoce las piezas y sigue las cintas |
| II · Repetir | El rollo del maestro | Extiende la unidad de repetición: une puntos, calca y voltea |
| III · Reconstruir | El geómetra | Divide el círculo, traza la retícula y llega al lazo |
| IV · Crear | El maestro | Concibe, transmite y ejecuta su propio diseño |

El detalle está en [`docs/indice.md`](docs/indice.md).

## Flujo de trabajo

1. **Diseñar** cada lazo en el Taller de Lacería (`taller/index.html`, se abre en cualquier navegador).
2. **Exportar** en SVG por capas. Cada archivo lleva dentro su código de diseño (`LAC1…`) y su ficha de procedencia.
3. **Maquetar**: el maquetador lee las capas y genera las variantes de página (línea para colorear, clave de color, cuarto coloreado, unidad de repetición, punteado, construcción desde el círculo).

### Capas del SVG exportado

| Capa | Visible | Uso |
|---|---|---|
| Fondo | Sí | Color de fondo |
| Estrellas rellenas | Según ajuste | Relleno de las estrellas |
| Pintura | Sí | Color automático o pintado a mano |
| Retícula de construcción | Oculta salvo que se muestre | Polígonos base, agrupados por tipo (`data-tipo`) |
| Cintas entrelazadas / Líneas | Sí | El dibujo, con el entrelazado |
| Piezas (datos) | Oculta | Cada pieza cerrada, con su clase de forma (`data-clase`) y su número de lados |
| Trazado central (datos) | Oculta | Eje de cada cinta |
| Celda que se repite (datos) | Oculta | La unidad de repetición, con sus vectores (`data-t1`, `data-t2`) |

Las capas son compatibles con Inkscape.

## Origen de las láminas y derechos

- **Todas las láminas se construyen con el Taller de Lacería**, a partir del método de los polígonos en contacto (Hankin, 1925; Kaplan, 2005), que es de dominio público. No se usan dibujos ni reconstrucciones de terceros.
- Los diseños no se presentan como copias de monumentos concretos. Se describen como *construidos con el método tradicional*.
- Fórmula para los créditos del libro: *"Láminas generadas con un programa geométrico propio, sin IA generativa de imágenes."*
- © Juan Domínguez Gallego. Todos los derechos reservados.

> **Aviso:** este repositorio es público. Antes de subir el libro maquetado o material que no deba circular, conviene hacerlo privado desde *Settings → General → Danger Zone → Change visibility* en GitHub.
