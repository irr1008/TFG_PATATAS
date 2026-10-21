# Evolución temporal de los índices espectrales

Issue #3 · Sprint 2 · Fecha: 20 y 21/10/2026
Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 3)

## 1. Alcance e índices representados

Se representa la evolución temporal de NDVI, NDMI y EVI para las cuatro parcelas
(Pancostales, Puri, La Culebra y Los Ceres) durante el periodo de extracción
provisional, del 01/04/2026 (incluido) al 01/10/2026 (excluido). El periodo es
provisional y no se confirma el cultivo presente en cada parcela.

## 2. Decisión sobre NDRE

La issue pedía NDVI, NDRE, NDMI y EVI. La extracción de 2026 calcula NDVI, NDMI,
MSI, EVI y SAVI; NDRE no está disponible.

Decisión (21/10/2026): en esta issue se representan los tres índices disponibles
y la incorporación de NDRE se traslada a la issue #4. Allí se evaluará añadirlo al
extractor (bandas B8A y B5), repetir la extracción de las cuatro parcelas y
revisar la selección de observaciones. Si se incorpora, bastará añadir `NDRE` a la 
lista de índices de la Parte 3 del notebook para generar su figura. Si no es viable 
dentro del sprint, se documentará como limitación.

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
cada imagen.

| Parcela | Observaciones | Seleccionadas | No seleccionadas |
|---|---:|---:|---:|
| Pancostales | 39 | 25 | 14 |
| Puri | 68 | 29 | 39 |
| La Culebra | 39 | 27 | 12 |
| Los Ceres | 35 | 26 | 9 |

## 5. Criterio de representación

- Observaciones seleccionadas: puntos unidos por una línea.
- Observaciones no seleccionadas: puntos grises, sin línea, para ver qué se descartó.
- Huecos: la línea se corta cuando entre dos observaciones seleccionadas pasan
  más de 14 días. No se interpola ni se rellena ningún valor.
- Un panel por parcela, con el mismo eje vertical calculado con todas las
  observaciones de las cuatro parcelas, para poder compararlas.
- Eje horizontal limitado al periodo de extracción.
- Título con el índice y el periodo provisional, etiquetas de ejes y leyenda en
  cada figura.
- El orden cronológico se garantiza ordenando cada tabla por fecha antes de
  graficar.

## 6. Figuras

| Figura | Contenido |
|---|---|
| `evolucion_ndvi_cuatro_parcelas.png` | Evolución del NDVI en las cuatro parcelas |
| `evolucion_ndmi_cuatro_parcelas.png` | Evolución del NDMI en las cuatro parcelas |
| `evolucion_evi_cuatro_parcelas.png` | Evolución del EVI en las cuatro parcelas |

## 7. Descripción de los resultados

Valores de las observaciones seleccionadas (tabla de la celda 3.5 del notebook).

| Parcela | Índice | Valor inicial | Máximo | Fecha del máximo | Mínimo | Fecha del mínimo | Valor final |
|---|---|---:|---:|---|---:|---|---:|
| Pancostales | NDVI | 0,238 | 0,815 | 2026-07-04 | 0,126 | 2026-05-20 | 0,222 |
| Pancostales | NDMI | -0,187 | 0,384 | 2026-07-04 | -0,233 | 2026-04-15 | -0,094 |
| Pancostales | EVI | 0,173 | 0,750 | 2026-07-04 | 0,105 | 2026-04-27 | 0,178 |
| Puri | NDVI | 0,175 | 0,816 | 2026-07-04 | 0,095 | 2026-05-20 | 0,207 |
| Puri | NDMI | -0,118 | 0,440 | 2026-07-04 | -0,165 | 2026-04-27 | -0,102 |
| Puri | EVI | 0,149 | 0,807 | 2026-07-04 | 0,091 | 2026-05-20 | 0,160 |
| La Culebra | NDVI | 0,172 | 0,938 | 2026-07-04 | 0,113 | 2026-04-27 | 0,220 |
| La Culebra | NDMI | -0,137 | 0,486 | 2026-07-04 | -0,188 | 2026-04-17 | -0,139 |
| La Culebra | EVI | 0,138 | 0,974 | 2026-07-04 | 0,092 | 2026-04-27 | 0,160 |
| Los Ceres | NDVI | 0,248 | 0,871 | 2026-06-29 | 0,188 | 2026-04-17 | 0,293 |
| Los Ceres | NDMI | -0,110 | 0,415 | 2026-06-29 | -0,164 | 2026-04-15 | -0,091 |
| Los Ceres | EVI | 0,188 | 0,859 | 2026-06-29 | 0,135 | 2026-04-15 | 0,228 |

Lo que muestran las figuras y la tabla:

- Los tres índices siguen un patrón temporal parecido en las cuatro parcelas:
  valores bajos en abril y mayo, un aumento a lo largo de junio, un máximo a
  finales de junio o principios de julio, un descenso en julio y agosto, y
  valores bajos y estables en septiembre.
- Los máximos de las observaciones seleccionadas se producen el 04/07/2026 en
  Pancostales, Puri y La Culebra y el 29/06/2026 en Los Ceres, con cinco días de
  diferencia entre los dos grupos. Los tres índices alcanzan el máximo en la
  misma observación de cada parcela.
- El NDVI máximo va de 0,815 (Pancostales) a 0,938 (La Culebra) y el EVI máximo
  de 0,750 (Pancostales) a 0,974 (La Culebra). El NDMI máximo va de 0,384 a 0,486.
- El NDVI mínimo está entre 0,095 y 0,188 y se da entre mediados de abril y
  finales de mayo. Al final del periodo el NDVI vuelve a valores de 0,207 a
  0,293, próximos a los iniciales.
- El NDMI parte de valores negativos (de -0,187 a -0,110), pasa a positivos en el
  máximo y termina otra vez en negativos (de -0,139 a -0,091).
- Las observaciones no seleccionadas siguen en general la misma curva que las
  seleccionadas, con algunos valores más bajos.

Caso de Los Ceres. A diferencia de las otras tres parcelas, la curva de Los Ceres
presenta, tras el máximo de finales de junio, un mínimo local el 24/07/2026
(NDVI 0,584) y una recuperación hasta 0,781 el 03/08/2026, antes del descenso
final. La comprobación de la celda 3.6 muestra que la observación del 24/07
tiene una cobertura de parcela del 85,0 %, por encima del umbral del 70 %, y que
dos días después, el 26/07, el NDVI es de 0,697 con una cobertura del 96,1 %. Por
tanto, la caída no se explica por una cobertura por debajo del umbral. La causa
queda sin determinar y no se interpreta.

Estas descripciones se refieren solo al comportamiento de los índices. No se
infiere el estado hídrico, la fenología ni el cultivo.

## 8. Huecos de observación

Huecos de más de 14 días entre observaciones seleccionadas:

| Parcela | Desde | Hasta | Días |
|---|---|---|---:|
| Pancostales | 2026-04-27 | 2026-05-20 | 23 |
| Pancostales | 2026-06-09 | 2026-06-29 | 20 |
| Puri | 2026-06-09 | 2026-06-29 | 20 |
| La Culebra | 2026-04-27 | 2026-05-20 | 23 |
| La Culebra | 2026-06-09 | 2026-06-26 | 17 |
| Los Ceres | 2026-04-27 | 2026-05-15 | 18 |
| Los Ceres | 2026-06-09 | 2026-06-24 | 15 |

Los huecos se concentran en dos ventanas: desde finales de abril hasta mediados
de mayo (tres parcelas) y desde principios hasta finales de junio (las cuatro).
Puri no tiene hueco en la primera ventana, con 13 días entre observaciones. El
mayor hueco de cada parcela coincide con el calculado por el notebook 03: 23,
20, 23 y 18 días. La segunda ventana coincide con el tramo de aumento de los
índices, por lo que esa subida está menos muestreada.

## 9. Limitaciones

- El periodo es provisional y el cultivo no está confirmado, por lo que las
  curvas no se interpretan como desarrollo de un cultivo concreto.
- Los índices describen la vegetación y no miden la humedad del suelo.
- Los umbrales de la selección provisional (nube 20, cobertura 70 %) no están
  validados agronómicamente.
- La línea cortada marca huecos de más de 14 días; el umbral es un criterio de
  visualización, no agronómico.
- Puri combina dos teselas; solo se seleccionan las filas de la que cubre toda la
  parcela.
- Los recuentos `*_count` y `pixeles_antes` no son directamente comparables.
- NDRE no se representa en esta issue; su tratamiento se traslada a la issue #4.

## 10. Evidencias

- Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 3).
- Figuras y tablas, guardadas en Drive en
  `resultados/graficas_evolucion_temporal/`: las tres figuras anteriores,
  `huecos_seleccion.csv` y `resumen_indices_seleccionadas.csv`.
