# Estado de las reglas

21 de 24 reglas verificadas. Cobertura: qué parte de la tinta de la lámina queda bajo la regla. Precisión: qué parte de la regla va sobre tinta. Ambas se miden en el 80 % central de la lámina, a menos de 2,5 píxeles.

| Lámina | Nombre | Estado | Cobertura | Precisión | Simetría | Método |
|---|---|---|---|---|---|---|
| r0 | Estrellas de seis puntas con lados de arco | verificada (construcción) | — | — | p6m | construcción exacta (arcos) |
| r1 | Estrellas de seis puntas y hexágonos alargados | verificada | 97.4 % | 99.9 % | pmm/cmm/pmg/pgg | retícula triangular |
| r2 | Hexágonos y triángulos partidos | verificada | 86.8 % | 91.4 % | p6m | retícula triangular |
| r3 | Rombos en estrella de tres brazos | verificada | 99.6 % | 100.0 % | p6m | extraer.py |
| p01 | Hexágonos con estrella de seis puntas | verificada | 97.8 % | 99.6 % | p6m | extraer.py |
| p02 | Flechas en tres direcciones | verificada | 99.7 % | 100.0 % | p3m1/p31m | extraer.py |
| p03 | Ganchos alrededor de estrellas | verificada | 97.8 % | 99.8 % | p6 | extraer.py |
| p04 | Triángulos entrelazados | verificada | 99.4 % | 99.8 % | p2 | extraer.py |
| p05 | Rectángulos con triángulos y pentágonos | revisar | 81.9 % | 98.0 % | pmm/cmm/pmg/pgg | extraer.py |
| p06 | Estrellas de seis puntas y pentágonos | verificada | 99.2 % | 100.0 % | p6m | extraer.py |
| p07 | Estrellas y cuadrados girados | sin resolver | 2.5 % | 90.2 % | p1 | extraer.py |
| p08 | Cuadrados y estrellas | verificada | 98.9 % | 99.9 % | p6m | a mano por simetría |
| p09 | Cintas entrelazadas | revisar | 87.2 % | 99.7 % | p1 | extraer.py |
| p10 | Pentágonos y estrellas | verificada | 99.1 % | 100.0 % | p6m | a mano por simetría |
| p11 | Estrellas de seis puntas y doble anillo | verificada | 99.5 % | 100.0 % | p6m | a mano por simetría |
| p12 | Cuadrados, flechas y rectas largas | verificada (simetría del grafo sin confirmar) | 99.7 % | 99.9 % | p1 | extraer.py |
| p13 | Estrellas, hexágonos y rombos | verificada (simetría del grafo sin confirmar) | 100.0 % | 100.0 % | p1 | extraer.py |
| p14 | Estrellas pequeñas y hexágonos | verificada | 97.7 % | 99.1 % | p6m | extraer.py |
| p15 | Hexágonos, estrellas y banderas | verificada | 99.6 % | 100.0 % | p6m | nodos_sim.py |
| p16 | Estrellas y triángulos con banderas | verificada | 98.6 % | 99.6 % | p6m | nodos_sim.py |
| p17 | Hexágonos y estrellas alargadas | verificada | 99.9 % | 100.0 % | p6m | nodos_sim.py + regularizar |
| p18 | Círculos y arcos | verificada | 99.8 % | 99.7 % | p6m | arcos_sim.py |
| p19 | Hexágonos grandes y pequeños | verificada | 99.9 % | 100.0 % | p6m | extraer.py |
| p20 | Hexágonos y estrellas de seis puntas | verificada | 97.2 % | 99.9 % | p6m | extraer.py |

Pendientes: p05 (pentágonos mal leídos; simetría de orden 2), p07 (sin leer) y p09 (cintas dobles).
