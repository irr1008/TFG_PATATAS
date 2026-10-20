# Análisis de la estructura de los CSV de Sentinel-2

Issue #2 · Sprint 2 · Fecha del análisis: 20/10/2026
Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 1)

## 1. Fuente y alcance

El trabajo con los datos satelitales se organiza en tres notebooks:

| Notebook | Función |
|---|---|
| `02_preparacion_parcelas_reales` | Genera el catálogo de parcelas y sus geometrías (GeoJSON) y comprueba su validez |
| `03_extraccion_sentinel2_parcelas_reales` | Usa ese catálogo para extraer Sentinel-2 y genera los CSV de índices, de revisión de calidad y el resumen semanal |
| `01_Exploracion_inicial_datos_sentinel-2` (Parte 1) | Analiza la estructura de los CSV generados por el notebook 03 |

Este documento analiza los CSV generados por el notebook 03 para cuatro parcelas,
con una extracción provisional del 01/04/2026 (incluido) al 01/10/2026
(excluido). El periodo es provisional y no se confirma el cultivo presente en
cada parcela durante esas fechas.

Parámetros de la extracción: probabilidad de nube inferior a 20, cobertura
mínima del 70 % por índice y escala de evaluación de 20 m.

| Parcela | Identificador | Variedad (catálogo) |
|---|---|---|
| Pancostales | `pancostales` | Lady Amarilla |
| Puri | `puri` | Lady Amarilla |
| La Culebra | `la_culebra` | Agria |
| Los Ceres | `los_ceres` | Noha |

La variedad procede del catálogo de parcelas y no confirma que el cultivo de la
campaña sea patata en el periodo analizado.

Por cada parcela se usan tres archivos generados por el notebook 03: el CSV de
índices (una fila por imagen con al menos un píxel válido), el CSV de revisión
de calidad y el resumen semanal.

## 2. Resumen por parcela

| Parcela | Filas | Columnas | Imágenes distintas | Fechas distintas | Fechas con varias filas | Primera fecha | Última fecha |
|---|---:|---:|---:|---:|---:|---|---|
| Pancostales | 39 | 56 | 39 | 39 | 0 | 2026-04-10 | 2026-09-24 |
| Puri | 68 | 56 | 68 | 35 | 33 | 2026-04-10 | 2026-09-24 |
| La Culebra | 39 | 56 | 39 | 39 | 0 | 2026-04-10 | 2026-09-24 |
| Los Ceres | 35 | 56 | 35 | 35 | 0 | 2026-04-10 | 2026-09-24 |

Cada fila del CSV corresponde a una imagen Sentinel-2 con al menos un píxel
válido tras la máscara de calidad, por lo que las filas coinciden con las
imágenes distintas. Las imágenes originales que intersectan cada parcela son más
(ejecución del notebook 03):

| Parcela | Imágenes originales | Con píxeles válidos | Sin ningún píxel válido |
|---|---:|---:|---:|
| Pancostales | 54 | 39 | 15 |
| Puri | 108 | 68 | 40 |
| La Culebra | 54 | 39 | 15 |
| Los Ceres | 54 | 35 | 19 |

Puri tiene el doble de imágenes originales porque la parcela se solapa con dos
teselas (T30TTL y T30TUL). Sus 68 filas se reparten a partes iguales: 34 de cada
tesela. En 33 de sus 35 fechas hay dos filas, una por tesela. En las otras tres
parcelas hay como máximo una fila por fecha.

## 3. Columnas y tipos

Los CSV tienen 56 columnas. Las cuatro parcelas comparten las mismas columnas,
en el mismo orden y con los mismos tipos de datos.

| Grupo | Columnas | Contenido |
|---|---:|---|
| Identificación | 6 | `parcela_id`, `nombre_parcela`, `municipio`, `variedad_catalogo`, `date`, `image_id` |
| Calidad | 4 | `cloud_percentage`, `pixeles_antes`, `pixeles_despues`, `porcentaje_conservado` |
| Contexto de extracción | 6 | `periodo_provisional`, `cultivo_confirmado_en_periodo`, `fecha_inicio_incluida`, `fecha_fin_excluida`, `escala_estadisticas_m`, `umbral_probabilidad_nube` |
| Estadísticas por índice | 40 | 5 índices × 8 estadísticos |

Índices presentes: NDVI, NDMI, MSI, EVI y SAVI. Estadísticos de cada índice:
`mean`, `stdDev`, `min`, `max`, `median`, `p25`, `p75` y `count`. Por ejemplo,
`NDVI_mean`, `NDVI_stdDev` y `NDVI_count`.

Tipos de datos:
- `date`: fecha (`datetime64`).
- Medias, desviaciones, mínimos, máximos, medianas y percentiles: decimales (`float64`).
- Recuentos `*_count`, `pixeles_antes`, `pixeles_despues` y `escala_estadisticas_m`: enteros (`int64`).
- `periodo_provisional` y `cultivo_confirmado_en_periodo`: booleanos.
- Identificadores, nombres, municipio, variedad, `image_id` y fechas de inicio y fin: texto.

## 4. Valores ausentes

Ninguna parcela tiene celdas nulas. Los huecos temporales no aparecen como
valores nulos: cuando no hay una imagen con píxeles válidos, simplemente no hay fila.
Las semanas sin observaciones seleccionadas sí conservan valores ausentes en el
resumen semanal.

## 5. Fechas y huecos

| Parcela | Fechas distintas | Intervalo mínimo | Intervalo mediano | Intervalo medio | Intervalo máximo |
|---|---:|---:|---:|---:|---:|
| Pancostales | 39 | 2 | 4 | 4,39 | 12 |
| Puri | 35 | 2 | 5 | 4,91 | 13 |
| La Culebra | 39 | 2 | 3 | 4,39 | 10 |
| Los Ceres | 35 | 2 | 5 | 4,91 | 10 |

Valores en días entre fechas distintas con imagen válida. No hay huecos de 15
días o más en los CSV de índices.

Los huecos aumentan al aplicar la selección técnica provisional. El mayor
intervalo entre observaciones seleccionadas es de 23 días en Pancostales, 20 en
Puri, 23 en La Culebra y 18 en Los Ceres (ejecución del notebook 03). Las
observaciones no son diarias, por lo que cualquier uso posterior debe tolerar
semanas sin dato.

## 6. Calidad, cobertura y selección

Indicadores en el CSV de índices:
- `cloud_percentage`: porcentaje de píxeles nubosos de la escena Sentinel-2, no de la parcela.
- `pixeles_antes` y `pixeles_despues`: píxeles B8 de 20 m dentro de la parcela antes y después de aplicar la máscara de calidad.
- `porcentaje_conservado`: relación entre ambos.
- `*_count`: píxeles válidos utilizados en cada índice.

| Parcela | Píxeles de la parcela (20 m) | Nube de la escena (media / máximo) | Píxeles conservados (media) | Píxeles conservados (mediana) |
|---|---|---|---:|---:|
| Pancostales | 213 | 13,94 % / 64,60 % | 72,34 % | 86,38 % |
| Puri | 117 (tesela que cubre toda la parcela) y 59 (tesela que cubre parte) | 14,76 % / 86,01 % | 79,55 % | 99,57 % |
| La Culebra | 303 | 15,59 % / 65,36 % | 74,33 % | 86,47 % |
| Los Ceres | 141 | 14,61 % / 65,36 % | 80,49 % | 96,45 % |

El porcentaje conservado varía mucho dentro de cada parcela, desde valores
inferiores al 11 % hasta el 100 %. Por eso el CSV de índices incluye imágenes de
calidad muy distinta y no se pueden usar todas sin una selección previa.

Criterio de selección provisional del notebook 03: cobertura mínima del 70 % de
la parcela en todos los índices y medias completas. Las filas no seleccionadas se
conservan para poder revisarlas.

| Parcela | Observaciones revisadas | Seleccionadas | No seleccionadas | Cobertura mínima entre índices (mediana) | Semanas totales | Con datos | Sin datos |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pancostales | 39 | 25 | 14 | 86,77 % | 27 | 17 | 10 |
| Puri | 68 | 29 | 39 | 50,97 % | 27 | 20 | 7 |
| La Culebra | 39 | 27 | 12 | 86,61 % | 27 | 18 | 9 |
| Los Ceres | 35 | 26 | 9 | 96,10 % | 27 | 18 | 9 |

En Puri, `pixeles_antes` toma dos valores: 117, que corresponde a la tesela que
cubre toda la parcela, y 59, que corresponde a la que cubre algo más de la mitad.
La mediana de cobertura del 50,97 % refleja que la mitad de sus filas pertenecen
a esa segunda tesela, cuya cobertura queda por debajo del 70 % y no se
selecciona. Ese es el motivo principal de sus 39 observaciones no seleccionadas.

Las cifras de selección y de semanas coinciden con las de la ejecución del
notebook 03 (comprobación 1.10 del notebook 01, resultado correcto en las cuatro
parcelas). El filtro orientativo del ejemplo de 2018 (50 % del máximo de
`NDVI_count`) no se aplica a estos datos.

## 7. Variables utilizables y no disponibles

| Elemento | ¿Disponible? | Uso posterior |
|---|---|---|
| NDVI | Sí | Series por parcela; según la especificación del tutor puede alimentar la estimación de Kc (no implementado) |
| NDMI, MSI | Sí | Indicadores del estado hídrico de la vegetación; no miden humedad del suelo |
| EVI, SAVI | Sí | Indicadores de vigor y cobertura vegetal |
| Calidad y cobertura por imagen | Sí | Selección de observaciones |
| Resumen semanal sin interpolar | Sí | Entrada temporal para el simulador |
| NDRE | No | Su tratamiento se decide en la issue #3 |
| NDWI y RECI | No | El motor actual (Agrobioma v14) usa NDVI, MSI, NDWI y RECI; los dos últimos no están en esta extracción |
| Humedad del suelo, meteorología y riegos | No | Fuentes externas pendientes |
| Textura del suelo, cultivo y fechas agronómicas confirmadas | No | Pendientes; el periodo es provisional |

Los índices satelitales no sustituyen a las sondas de humedad del suelo.

## 8. Discrepancias con la descripción de la issue

La descripción de la issue citaba columnas de interés que proceden del CSV de
maíz de 2018:

- `NDRE_mean`: no existe en la extracción de 2026.
- `NDVI_std`: en 2026 la desviación se llama `NDVI_stdDev`.

Además, el CSV de 2018 tiene 123 columnas y 15 índices, mientras que los de 2026
tienen 56 columnas y 5 índices. Los análisis de 2018 se conservan en la Parte 2
del notebook 01 solo como ejemplo metodológico.

## 9. Limitaciones

- El periodo de extracción es provisional y el cultivo no está confirmado.
- La máscara de nubes y sombras reduce los errores pero no garantiza su eliminación completa.
- `cloud_percentage` describe la escena completa, no la parcela.
- Los umbrales de la selección provisional (nube 20, cobertura 70 %) no están validados agronómicamente.
- Las semanas sin observaciones seleccionadas conservan valores ausentes y no se interpolan.
- Puri combina dos teselas con coberturas distintas de la parcela.
- Los índices no sustituyen a las mediciones de humedad del suelo.

## 10. Evidencias

- Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 1).
- Tablas generadas por el notebook 01, guardadas en Drive fuera del repositorio, en `resultados/analisis_estructura_csv/`: `resumen_parcelas`, `comparacion_columnas`, `estructura_columnas`, `resumen_fechas`, `huecos_largos`, `fechas_repetidas`, `seleccion_provisional`, `resumen_semanal`, `contraste_notebook_03` y `disponibilidad_indices`.
- Contraste con la ejecución del notebook 03: coincidencia en filas, fechas distintas, observaciones seleccionadas y semanas sin observaciones de las cuatro parcelas.

## 11. Trazabilidad

Cadena de generación de los datos analizados:

1. El notebook 02 prepara el catálogo de parcelas y sus geometrías.
2. El notebook 03 lee ese catálogo y genera los CSV de índices, de calidad y el
   resumen semanal.
3. El notebook 01 (Parte 1) analiza esos CSV.

Los notebooks 02 y 03 se ejecutan en Google Colab y guardan sus resultados en
Drive. Todavía no están en este repositorio porque el 02 contiene las
coordenadas de las parcelas y ambos incluyen salidas con datos de las
explotaciones. Se publicarán versiones saneadas tras revisar los permisos sobre
los datos (issue #4).

Las cifras de contraste con el notebook 03 están registradas en la celda 1.10 del
notebook 01.
