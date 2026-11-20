# Formato `patron-periodico/1`

Una regla describe un patrón geométrico periódico como un **grafo dibujado sobre una celda que se repite**. Es un archivo JSON pequeño (unas decenas de líneas) que cualquier programa o modelo puede leer y dibujar sin herramientas especiales.

## Idea

Todo patrón periódico es la repetición de una celda (un paralelogramo) según dos vectores **a** y **b**. Dentro de la celda hay unos cuantos vértices; las aristas unen vértices, y pueden cruzar el borde de la celda y llegar a una copia vecina. Con eso basta para describir el patrón entero, sea del tamaño que sea.

## Campos

```json
{
  "formato": "patron-periodico/1",
  "id": "p06",
  "nombre": "Estrellas de seis puntas y pentágonos",
  "fuente": "Jules Bourgoin, Les Éléments de l'Art Arabe (1879), lámina …",
  "ejes": "x hacia la derecha, y hacia abajo (como SVG); unidad = longitud de a",
  "celda": { "a": [1.0, 0.0], "b": [-0.5, 0.866025] },
  "vertices": [[0.12, 0.40], [0.53, 0.18]],
  "aristas":  [[0, 1, 0, 0], [1, 0, 1, 0]],
  "simetria": { "orden_giro": 6, "grupo": "p6m" },
  "construccion": { "reticula": {"tipo": "triangular", "lado": 0.25, "angulo": 0, "origen": [0, 0]},
                    "descripcion": "texto libre: cómo se traza a mano" },
  "verificacion": { "lamina": "p06.png", "a_px": [191.3, 110.3], "origen_px": [485.0, 425.6] }
}
```

| Campo | Obligatorio | Significado |
|---|---|---|
| `formato` | sí | Siempre `patron-periodico/1`. |
| `celda.a`, `celda.b` | sí | Vectores de repetición en coordenadas cartesianas (x a la derecha, y hacia abajo). Se normalizan para que `a` mida 1. |
| `vertices` | sí | Cada vértice en **coordenadas de celda** `[u, v]`, con 0 ≤ u, v < 1. Su posición cartesiana es `u·a + v·b`. |
| `aristas` | sí | `[i, j, du, dv]`: une el vértice `i` de una celda con el vértice `j` de la celda desplazada `du·a + dv·b`. Un quinto elemento opcional `{"r": radio, "barrido": 0|1}` convierte la arista en un arco de circunferencia (radio en unidades de `a`, `barrido` como en SVG). |
| `simetria` | no | Orden del giro máximo y grupo cristalográfico (`p6m`, `p31m`, `cmm`, …). Informativo. |
| `construccion` | no | Retícula de construcción para el libro y descripción del trazado a mano. |
| `verificacion` | no | Datos de la lámina original (vector `a` y origen en píxeles) para superponer la regla al escaneo y comprobarla. |
| `derivado_de`, `variacion` | no | En las reglas generadas por variación: de qué regla salen y con qué método y parámetros. |

## Cómo se dibuja (algoritmo completo)

```
para cada celda (i, j) que toca el dibujo:
    para cada arista [p, q, du, dv]:
        P = origen + tam · ((V[p].u + i)·a + (V[p].v + j)·b)
        Q = origen + tam · ((V[q].u + i + du)·a + (V[q].v + j + dv)·b)
        trazar P–Q   (o el arco, si la arista lo indica)
```

`tam` es el tamaño en milímetros que se quiere dar al vector `a`. `herramientas/dibujar.py` hace exactamente esto, une los tramos alineados en rectas largas y recorta al marco.

## Por qué este formato

- **Es exacto**: guarda la geometría ideal, no el escaneo.
- **Es mínimo**: el patrón entero cabe en una celda.
- **Se puede variar**: los métodos de variación leen y escriben el mismo formato, así que se pueden encadenar.
- **Es legible**: un modelo de lenguaje puede leerlo, explicarlo y dibujarlo con unas líneas de código.
