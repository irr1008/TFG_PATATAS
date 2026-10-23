# Análisis de la estructura de los CSV de Sentinel-2

Issue #2 · Sprint 2 · Fecha del análisis: 20/10/2026 (actualizado el 23/10/2026
tras la revisión con los tutores: combinación de teselas, criterio de nube y
sombra de la parcela y periodo hasta el 01/11/2026; issue #6)
Notebook: `01_Exploracion_inicial_datos_sentinel-2.ipynb` (Parte 1)

## 1. Fuente y alcance

El trabajo con los datos satelitales se organiza en tres notebooks:

| Notebook | Función |
|---|---|
| `02_preparacion_parcelas_reales` | Genera el catálogo de parcelas y sus geometrías (GeoJSON) y comprueba su validez |
| `03_extraccion_sentinel2_parcelas_reales` | Usa ese catálogo para extraer Sentinel-2 y genera los CSV de índices, de revisión de calidad y el resumen semanal |
| `01_Exploracion_inicial_datos_sentinel-2` (Parte 1) | Analiza la estructura de los CSV generados por el notebook 03 |

Este documento analiza los CSV generados por el notebook 03 para cuatro parcelas
(`pancostales`, `puri`, `la_culebra` y `los_ceres`), con una extracción
provisional del 01/04/2026 (incluido) al 01/11/2026 (excluido). La fecha de fin
es posterior a la ejecución: las últimas imágenes disponibles son del 22/10/2026
y la última con píxeles válidos es del 14/10/2026. El periodo es provisional y no
se confirma el cultivo presente en cada parcela durante esas fechas.

Parámetros de la extracción: probabilidad de nube inferior a 20 (a nivel de
píxel), máximo del 30 % de píxeles de nube y sombra dentro de la parcela para
seleccionar una observación, y escala de evaluación de 20 m.

Si una parcela cae en más de una tesela de Sentinel-2, el notebook 03 combina las
imágenes de cada fecha en un mosaico antes de generar el CSV, de modo que hay una
sola fila por fecha. Si cae en una sola tesela, cada imagen se procesa por
separado.

El catálogo de parcelas incluye municipio y variedad. Esos datos no se publican
en este repositorio mientras los tutores no autoricen su publicación (apartado
11). La variedad del catálogo no confirma que el cultivo de la campaña sea
patata en el periodo analizado.

Por cada parcela se usan tres archivos generados por el notebook 03: el CSV de
índices (una fila por imagen o mosaico con al menos un píxel válido), el CSV de
revisión de calidad y el resumen semanal.

## 2. Resumen por parcela

| Parcela | Filas | Columnas | Imágenes distintas | Fechas distintas | Fechas con varias filas | Primera fecha | Última fecha |
|---|---:|---:|---:|---:|---:|---|---|
| Pancostales | 42 | 64 | 42 | 42 | 0 | 2026-04-10 | 2026-10-14 |
| Puri | 36 | 64 | 36 | 36 | 0 | 2026-04-10 | 2026-10-14 |
| La Culebra | 41 | 64 | 41 | 41 | 0 | 2026-04-10 | 2026-10-14 |
| Los Ceres | 37 | 64 | 37 | 37 | 0 | 2026-04-10 | 2026-10-14 |

Cada fila del CSV corresponde a una imagen Sentinel-2 (o, en Puri, a un mosaico
diario de dos teselas) con al menos un píxel válido tras la máscara de calidad,
por lo que las filas coinciden con las imágenes distintas. Las imágenes que
intersectan cada parcela son más (ejecución del notebook 03):

| Parcela | Imágenes originales | Con píxeles válidos | Sin ningún píxel válido |
|---|---:|---:|---:|
| Pancostales | 61 | 42 | 19 |
| Puri | 122 (61 mosaicos diarios) | 36 | 25 |
| La Culebra | 61 | 41 | 20 |
| Los Ceres | 61 | 37 | 24 |

Puri se solapa con dos teselas (T30TTL y T30TUL), por lo que tiene el doble de
imágenes originales. Desde la revisión del 23/10/2026 las dos imágenes de cada
fecha se combinan píxel a píxel en un mosaico: en cada píxel se usa la tesela con
dato válido. Con ello hay una fila por fecha y el `image_id` de Puri termina en
`_T30TTL+T30TUL`. Antes de esa revisión, Puri tenía dos filas por fecha, una por
tesela. En las otras tres parcelas, que caen en una sola tesela, hay como máximo
una fila por fecha.

## 3. Columnas y tipos

Los CSV tienen 64 columnas. Las cuatro parcelas comparten las mismas columnas,
en el mismo orden y con los mismos tipos de datos.

| Grupo | Columnas | Contenido |
|---|---:|---|
| Identificación | 6 | `parcela_id`, `nombre_parcela`, `municipio`, `variedad_catalogo`, `date`, `image_id` |
| Calidad | 4 | `cloud_percentage`, `pixeles_antes`, `pixeles_despues`, `porcentaje_conservado` |
| Contexto de extracción | 6 | `periodo_provisional`, `cultivo_confirmado_en_periodo`, `fecha_inicio_incluida`, `fecha_fin_excluida`, `escala_estadisticas_m`, `umbral_probabilidad_nube` |
| Estadísticas por índice | 48 | 6 índices × 8 estadísticos |

Índices presentes: NDVI, NDRE, NDMI, MSI, EVI y SAVI. Estadísticos de cada
índice: `mean`, `stdDev`, `min`, `max`, `median`, `p25`, `p75` y `count`. Por
ejemplo, `NDVI_mean`, `NDRE_mean` y `NDVI_count`.

El CSV de revisión de calidad añade, por observación, la cobertura de píxeles
válidos por índice (`<ÍNDICE>_cobertura_pct` y `cobertura_minima_indices_pct`), el
porcentaje de nube y sombra de la parcela (`nube_sombra_parcela_pct`), el umbral
aplicado (`umbral_nube_sombra_parcela_pct`), la marca `apta_nube_sombra` y la
selección técnica provisional (`seleccion_tecnica_provisional`).

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
| Pancostales | 42 | 2 | 5 | 4,56 | 12 |
| Puri | 36 | 2 | 5 | 5,34 | 20 |
| La Culebra | 41 | 2 | 4 | 4,68 | 10 |
| Los Ceres | 37 | 2 | 5 | 5,19 | 13 |

Valores en días entre fechas distintas con imagen válida. Solo hay un hueco de 15
días o más en los CSV de índices: el de Puri entre el 24/09/2026 y el 14/10/2026
(20 días).

Los huecos aumentan al aplicar la selección técnica provisional. El mayor
intervalo entre observaciones seleccionadas es de 23 días en Pancostales, 20 en
Puri, 23 en La Culebra y 18 en Los Ceres (ejecución del notebook 03). Las
observaciones no son diarias, por lo que cualquier uso posterior debe tolerar
semanas sin dato.

## 6. Calidad, cobertura y selección

Indicadores en el CSV de índices:
- `cloud_percentage`: porcentaje de píxeles nubosos de la escena Sentinel-2, no de la parcela. En Puri es la media de las dos teselas del mosaico.
- `pixeles_antes` y `pixeles_despues`: píxeles B8 de 20 m dentro de la parcela antes y después de aplicar la máscara de calidad.
- `porcentaje_conservado`: relación entre ambos.
- `*_count`: píxeles válidos utilizados en cada índice.

| Parcela | Píxeles de la parcela (20 m) | Nube de la escena (media / máximo) | Píxeles conservados (media) | Píxeles conservados (mediana) |
|---|---|---|---:|---:|
| Pancostales | 213 | 15,96 % / 67,17 % | 70,71 % | 82,16 % |
| Puri | 117 (parcela completa, combinando T30TTL y T30TUL) | 14,37 % / 80,30 % | 88,06 % | 100,00 % |
| La Culebra | 303 | 16,29 % / 65,36 % | 73,85 % | 86,47 % |
| Los Ceres | 141 | 15,67 % / 67,17 % | 81,39 % | 96,45 % |

El porcentaje conservado varía mucho dentro de cada parcela, desde el 3 % hasta
el 100 %. Por eso el CSV de índices incluye imágenes de calidad muy distinta y no
se pueden usar todas sin una selección previa.

Criterio de selección provisional del notebook 03 (revisión con los tutores del
23/10/2026): una observación se descarta solo si más del 30 % de los píxeles de
la propia parcela son nube o sombra, y debe tener las medias de todos los índices.
Un píxel cuenta como nube si su probabilidad de nube es igual o superior a 20 o
si la clasificación de escena lo marca como nube o cirro (clases 8, 9 y 10), y
como sombra si la clase es 3. En parcelas con varias teselas, un píxel es nube o
sombra solo si lo es en todas las teselas que lo observan. La cobertura de
píxeles válidos se conserva en el CSV solo como información. Las filas no
seleccionadas se conservan para poder revisarlas.

| Parcela | Observaciones revisadas | Seleccionadas | No seleccionadas | Nube y sombra de la parcela (mediana / máximo) | Semanas totales | Con datos | Sin datos | Aún no disponibles |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Pancostales | 42 | 26 | 16 | 17,40 % / 90,36 % | 31 | 18 | 12 | 1 |
| Puri | 36 | 33 | 3 | 0,48 % / 84,78 % | 31 | 23 | 7 | 1 |
| La Culebra | 41 | 28 | 13 | 13,39 % / 96,91 % | 31 | 19 | 11 | 1 |
| Los Ceres | 37 | 28 | 9 | 3,90 % / 91,32 % | 31 | 20 | 10 | 1 |

La mediana de la cobertura mínima entre índices es de 82,60 % en Pancostales,
99,52 % en Puri, 86,61 % en La Culebra y 96,10 % en Los Ceres; en cada parcela
suma 100 con la mediana de nube y sombra. En la comprobación del 23/10/2026 con
el periodo hasta el 01/10, el criterio nuevo dio las mismas selecciones que el
anterior (cobertura mínima del 70 %): en esos datos los únicos píxeles que se
pierden son nube o sombra. Los cambios de la selección respecto a la primera
versión de este análisis se deben a la combinación de teselas de Puri (de 29 a 32
seleccionadas) y a las observaciones de octubre.

Las cifras de selección y de semanas coinciden con las de la ejecución del
notebook 03 (comprobación 1.10 del notebook 01, resultado correcto en las cuatro
parcelas). La semana aún no disponible es la del 26/10/2026, posterior a la
última imagen (22/10/2026), y no se cuenta como semana sin observaciones. El
filtro orientativo del ejemplo de 2018 (50 % del máximo de `NDVI_count`) no se
aplica a estos datos.

## 7. Variables utilizables y no disponibles

| Elemento | ¿Disponible? | Uso posterior |
|---|---|---|
| NDVI | Sí | Series por parcela; según la especificación del tutor puede alimentar la estimación de Kc (no implementado) |
| NDRE | Sí | Series por parcela; se calcula con las bandas B8A y B5 (borde rojo). Incorporado el 22/10/2026 |
| NDMI, MSI | Sí | Indicadores del estado hídrico de la vegetación; no miden humedad del suelo |
| EVI, SAVI | Sí | Indicadores de vigor y cobertura vegetal |
| Calidad y cobertura por imagen | Sí | Selección de observaciones |
| Resumen semanal sin interpolar | Sí | Entrada temporal para el simulador |
| NDWI y RECI | No | El motor actual (Agrobioma v14) usa NDVI, MSI, NDWI y RECI; los dos últimos no están en esta extracción |
| Humedad del suelo, meteorología y riegos | No | Fuentes externas pendientes |
| Textura del suelo, cultivo y fechas agronómicas confirmadas | No | Pendientes; el periodo es provisional |

Los índices satelitales no sustituyen a las sondas de humedad del suelo.

## 8. Discrepancias con la descripción de la issue

La descripción de la issue citaba columnas de interés que proceden del CSV de
maíz de 2018:

- `NDRE_mean`: no existía en la primera extracción de 2026. Se incorporó al
  extractor el 22/10/2026 (issue #4) y ya está en los CSV.
- `NDVI_std`: en 2026 la desviación se llama `NDVI_stdDev`.

Además, el CSV de 2018 tiene 123 columnas y 15 índices, mientras que los de 2026
tienen 64 columnas y 6 índices. Los análisis de 2018 se conservan en la Parte 2
del notebook 01 solo como ejemplo metodológico.

## 9. Limitaciones

- El periodo de extracción es provisional y el cultivo no está confirmado.
- El periodo llega hasta el 01/11/2026, pero solo hay imágenes hasta el 22/10/2026.
  La extracción debe repetirse para incorporar las siguientes.
- La máscara de nubes y sombras reduce los errores pero no garantiza su eliminación completa.
- `cloud_percentage` describe la escena completa, no la parcela.
- Los umbrales de la selección provisional (probabilidad de nube 20 por píxel y 30 % de nube y sombra en la parcela) no están validados agronómicamente.
- Las semanas sin observaciones seleccionadas conservan valores ausentes y no se interpolan.
- Puri se solapa con dos teselas, que se combinan a nivel de píxel; en la zona común se usa la tesela con dato válido.
- Los índices no sustituyen a las mediciones de humedad del suelo.
- Los recuentos *_count y pixeles_antes no son directamente comparables; no deben interpretarse como intercambiables.

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
Drive. El notebook 03 está publicado en este repositorio sin salidas y sin el
identificador del proyecto de Earth Engine. El notebook 02 no se publica: contiene
las coordenadas de las parcelas y sus salidas incluyen datos de las
explotaciones. Se publicará una versión saneada solo si los tutores autorizan
publicar esos datos. Las reglas de preparación y las decisiones están en
`docs/preparacion-datos-simulador.md`.

Las cifras de contraste con el notebook 03 están registradas en la celda 1.10 del
notebook 01.
