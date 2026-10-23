# Evolución temporal de los índices espectrales

Issue #3 · Sprint 2 · Fecha: 20 y 21/10/2026 (actualizado el 23/10/2026 con el
periodo hasta el 01/11/2026, la combinación de teselas y el criterio de nube y
sombra; issue #6)
Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 3)

## 1. Alcance e índices representados

Se representa la evolución temporal de NDVI, NDRE, NDMI y EVI para las cuatro
parcelas (Pancostales, Puri, La Culebra y Los Ceres) durante el periodo de
extracción provisional, del 01/04/2026 (incluido) al 01/11/2026 (excluido). Las
imágenes disponibles llegan hasta el 22/10/2026 y la última observación con
píxeles válidos es del 14/10/2026. El periodo es provisional y no se confirma el
cultivo presente en cada parcela.

## 2. Decisión sobre NDRE

La issue pedía NDVI, NDRE, NDMI y EVI. La extracción inicial de 2026 calculaba
NDVI, NDMI, MSI, EVI y SAVI; NDRE no estaba disponible.

Decisión (21/10/2026): la incorporación de NDRE se traslada a la issue #4, con
un límite de 90 minutos. Si no era viable dentro del sprint, se documentaba como
limitación.

Resultado (22/10/2026): NDRE se ha incorporado.

- Se modificó el extractor (notebook 03): se añaden las bandas B8A y B5 y se
  calcula `NDRE = (B8A - B5) / (B8A + B5)` con el mismo tratamiento de
  denominadores no válidos que los demás índices.
- Se repitió la extracción de las cuatro parcelas con los mismos parámetros. NDRE
  tiene la misma cobertura que el resto de índices en cada imagen y no tiene
  medias ausentes.
- Se añadió `NDRE` a la lista de índices de la Parte 3 y se generó su figura.

MSI y SAVI están disponibles pero no se representan porque la issue no los pide.

## 3. Revisión de los gráficos existentes

Los gráficos previos están en la Parte 2 del notebook y se hicieron con un único
CSV de maíz de 2018.

| Gráfico existente | Valoración | Decisión |
|---|---|---|
| Píxeles válidos por fecha | Útil para calidad; usa el criterio de 2018 (50 % del máximo de `NDVI_count`) | No se reutiliza para las parcelas de 2026 |
| NDVI y NDVI según calidad | Una sola parcela, sin referencia al periodo provisional | Se conserva como ejemplo |
| Cuatro índices en un único eje | Mezcla índices con escalas distintas | Se sustituye por una figura por índice |
| Figura guardada del NDVI | Solo maíz 2018 | Se conserva como ejemplo |

Las figuras nuevas mantienen el estilo (rejilla, marcadores, colores) y añaden un
panel por parcela, un eje vertical común, la distinción entre observaciones
seleccionadas y no seleccionadas y el corte de la línea en los huecos.

## 4. Datos de entrada

Se usan los CSV de revisión de calidad generados, que
contienen todas las imágenes con algún píxel válido, las estadísticas de cada
índice y la marca de selección técnica provisional. El valor representado es
`<ÍNDICE>_mean`, la media del índice sobre los píxeles válidos de la parcela en
cada imagen. En Puri cada observación es un mosaico diario de las dos teselas
que la cubren.

Una observación está seleccionada si como máximo el 30 % de los píxeles de la
parcela son nube o sombra y las medias de los índices están completas.

| Parcela | Observaciones | Seleccionadas | No seleccionadas |
|---|---:|---:|---:|
| Pancostales | 42 | 26 | 16 |
| Puri | 36 | 33 | 3 |
| La Culebra | 41 | 28 | 13 |
| Los Ceres | 37 | 28 | 9 |

## 5. Criterio de representación

- Observaciones seleccionadas: puntos unidos por una línea.
- Observaciones no seleccionadas: puntos grises, sin línea, para ver qué se descartó.
- Huecos: la línea se corta cuando entre dos observaciones seleccionadas pasan
  más de 14 días. No se interpola ni se rellena ningún valor.
- Un panel por parcela, con el mismo eje vertical calculado con todas las
  observaciones de las cuatro parcelas, para poder compararlas.
- Eje horizontal limitado al periodo de extracción (hasta el 01/11/2026); el
  tramo posterior a la última imagen disponible queda sin datos.
- Título con el índice y el periodo provisional, etiquetas de ejes y leyenda en
  cada figura.
- El orden cronológico se garantiza ordenando cada tabla por fecha antes de
  graficar.

## 6. Figuras

| Figura | Contenido |
|---|---|
| `evolucion_ndvi_cuatro_parcelas.png` | Evolución del NDVI en las cuatro parcelas |
| `evolucion_ndre_cuatro_parcelas.png` | Evolución del NDRE en las cuatro parcelas |
| `evolucion_ndmi_cuatro_parcelas.png` | Evolución del NDMI en las cuatro parcelas |
| `evolucion_evi_cuatro_parcelas.png` | Evolución del EVI en las cuatro parcelas |

## 7. Descripción de los resultados

Valores de las observaciones seleccionadas (tabla de la celda 3.5 del notebook).

| Parcela | Índice | Valor inicial | Máximo | Fecha del máximo | Mínimo | Fecha del mínimo | Valor final |
|---|---|---:|---:|---|---:|---|---:|
| Pancostales | NDVI | 0,238 | 0,815 | 2026-07-04 | 0,126 | 2026-05-20 | 0,248 |
| Pancostales | NDRE | 0,173 | 0,589 | 2026-06-29 | 0,077 | 2026-05-20 | 0,163 |
| Pancostales | NDMI | -0,187 | 0,384 | 2026-07-04 | -0,233 | 2026-04-15 | -0,101 |
| Pancostales | EVI | 0,173 | 0,750 | 2026-07-04 | 0,105 | 2026-04-27 | 0,188 |
| Puri | NDVI | 0,175 | 0,816 | 2026-07-04 | 0,095 | 2026-05-20 | 0,154 |
| Puri | NDRE | 0,111 | 0,580 | 2026-06-29 | 0,048 | 2026-05-20 | 0,101 |
| Puri | NDMI | -0,118 | 0,440 | 2026-07-04 | -0,165 | 2026-04-27 | -0,135 |
| Puri | EVI | 0,149 | 0,807 | 2026-07-04 | 0,091 | 2026-05-20 | 0,109 |
| La Culebra | NDVI | 0,172 | 0,938 | 2026-07-04 | 0,113 | 2026-04-27 | 0,180 |
| La Culebra | NDRE | 0,116 | 0,731 | 2026-06-29 | 0,072 | 2026-04-27 | 0,125 |
| La Culebra | NDMI | -0,137 | 0,486 | 2026-07-04 | -0,188 | 2026-04-17 | -0,161 |
| La Culebra | EVI | 0,138 | 0,974 | 2026-07-04 | 0,092 | 2026-04-27 | 0,126 |
| Los Ceres | NDVI | 0,248 | 0,871 | 2026-06-29 | 0,188 | 2026-04-17 | 0,240 |
| Los Ceres | NDRE | 0,180 | 0,663 | 2026-06-29 | 0,128 | 2026-04-17 | 0,172 |
| Los Ceres | NDMI | -0,110 | 0,415 | 2026-06-29 | -0,201 | 2026-10-14 | -0,201 |
| Los Ceres | EVI | 0,188 | 0,859 | 2026-06-29 | 0,135 | 2026-04-15 | 0,147 |

Lo que muestran las figuras y la tabla:

- Las cuatro parcelas siguen un patrón temporal parecido: valores bajos en abril
  y mayo, un aumento a lo largo de junio, un máximo a finales de junio o
  principios de julio y un descenso posterior.
- Los máximos de NDVI, NDMI y EVI se producen el 04/07/2026 en Pancostales, Puri
  y La Culebra y el 29/06/2026 en Los Ceres, con cinco días de diferencia entre
  los dos grupos. El NDRE alcanza su máximo el 29/06/2026 en las cuatro
  parcelas, es decir, cinco días antes que los otros tres índices en Pancostales,
  Puri y La Culebra.
- El NDVI máximo va de 0,815 (Pancostales) a 0,938 (La Culebra) y el EVI máximo
  de 0,750 (Pancostales) a 0,974 (La Culebra). El NDMI máximo va de 0,384 a 0,486
  y el NDRE máximo, de 0,580 (Puri) a 0,731 (La Culebra).
- El NDVI mínimo está entre 0,095 y 0,188 y el NDRE mínimo, entre 0,048 y 0,128;
  ambos se dan entre mediados de abril y finales de mayo. Al final de las
  observaciones el NDVI vale entre 0,154 y 0,248, del orden de los valores
  iniciales (de 0,172 a 0,248).
- El NDMI parte de valores negativos (de -0,187 a -0,110), pasa a positivos en el
  máximo y termina otra vez en negativos (de -0,201 a -0,101). En Los Ceres su
  mínimo (-0,201) corresponde a la última observación, del 14/10/2026.
- Las observaciones no seleccionadas siguen en general la misma curva que las
  seleccionadas, con algunos valores más bajos.

Caso de Los Ceres. A diferencia de las otras tres parcelas, la curva de Los Ceres
presenta, tras el máximo de finales de junio, un mínimo local el 24/07/2026
(NDVI 0,584) y una recuperación hasta 0,781 el 03/08/2026, antes del descenso
final. La comprobación de la celda 3.6 muestra que la observación del 24/07
tiene un 15,0 % de nube y sombra en la parcela, por debajo del máximo del 30 %, y
que dos días después, el 26/07, el NDVI es de 0,697 con un 3,9 % de nube y
sombra. Las observaciones con mucha nube y sombra (19/07, 29/07 y 08/08) no están
seleccionadas. Por tanto, el mínimo local no se explica por un exceso de nube y
sombra. La causa queda sin determinar y no se interpreta.

Estas descripciones se refieren solo al comportamiento de los índices. No se
infiere el estado hídrico, la fenología ni el cultivo.

## 8. Huecos de observación

Huecos de más de 14 días entre observaciones seleccionadas:

| Parcela | Desde | Hasta | Días |
|---|---|---|---:|
| Pancostales | 2026-04-27 | 2026-05-20 | 23 |
| Pancostales | 2026-06-09 | 2026-06-29 | 20 |
| Pancostales | 2026-09-24 | 2026-10-14 | 20 |
| Puri | 2026-06-09 | 2026-06-26 | 17 |
| Puri | 2026-09-24 | 2026-10-14 | 20 |
| La Culebra | 2026-04-27 | 2026-05-20 | 23 |
| La Culebra | 2026-06-09 | 2026-06-26 | 17 |
| La Culebra | 2026-09-24 | 2026-10-14 | 20 |
| Los Ceres | 2026-04-27 | 2026-05-15 | 18 |
| Los Ceres | 2026-06-09 | 2026-06-24 | 15 |

Hay diez huecos, concentrados en tres ventanas: desde finales de abril hasta
mediados de mayo (tres parcelas), desde principios hasta finales de junio (las
cuatro) y del 24/09 al 14/10 (Pancostales, Puri y La Culebra). Puri no tiene hueco
en la primera ventana, con 13 días entre observaciones. El mayor hueco de cada
parcela coincide con el calculado por el notebook 03: 23, 20, 23 y 18 días. La
ventana de junio coincide con el tramo de aumento de los índices, por lo que esa
subida está menos muestreada.

## 9. Limitaciones

- El periodo es provisional y el cultivo no está confirmado, por lo que las
  curvas no se interpretan como desarrollo de un cultivo concreto.
- Las imágenes llegan hasta el 22/10/2026 y la última observación con píxeles
  válidos es del 14/10/2026; el resto del periodo hasta el 01/11/2026 queda
  pendiente de nuevas ejecuciones.
- Los índices describen la vegetación y no miden la humedad del suelo.
- Los umbrales de la selección provisional (probabilidad de nube 20 por píxel y
  30 % de nube y sombra en la parcela) no están validados agronómicamente.
- La línea cortada marca huecos de más de 14 días; el umbral es un criterio de
  visualización, no agronómico.
- Puri se solapa con dos teselas, que se combinan a nivel de píxel en un mosaico
  por fecha.
- Los recuentos `*_count` y `pixeles_antes` no son directamente comparables.

## 10. Evidencias

- Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 3).
- Figuras y tablas, guardadas en Drive en
  `resultados/graficas_evolucion_temporal/`: las cuatro figuras anteriores,
  `huecos_seleccion.csv` y `resumen_indices_seleccionadas.csv`.
- Las cuatro figuras actualizadas deben copiarse a `docs/figuras/`.
