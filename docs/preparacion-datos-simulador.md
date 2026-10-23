# Preparación de los datos Sentinel-2 para el simulador

Issue #4 · Sprint 2 · Fecha: 22/10/2026 (actualizado el 23/10/2026 tras la
revisión con los tutores; issue #6)
Notebooks: `03_extraccion_sentinel2_parcelas_reales` (extracción y preparación) y
`01_Exploracion_inicial_datos_sentinel-2` (análisis y figuras)

## 1. Objetivo y alcance

Dejar documentadas las decisiones con las que los datos Sentinel-2 de las cuatro
parcelas (Pancostales, Puri, La Culebra y Los Ceres) se preparan para un uso
posterior en el simulador de riego. El periodo de extracción es provisional, del
01/04/2026 (incluido) al 01/11/2026 (excluido), y no se confirma el cultivo
presente en cada parcela. La fecha de fin es posterior a la ejecución: las
imágenes disponibles llegan hasta el 22/10/2026. Este documento no genera
recomendaciones de riego.

La preparación está implementada en el notebook 03. Este documento recoge las
reglas aplicadas, justifica las decisiones y registra lo que queda pendiente.

## 2. Resumen de decisiones

| Tarea de la issue | Decisión | Dónde se aplica |
|---|---|---|
| Convertir `date` a formato temporal | Fecha en formato `YYYY-MM-DD`, validada como fecha real y convertida con `pd.to_datetime` sin tolerar errores | Notebook 03 |
| Ordenar cronológicamente | Orden por `date` e `image_id` | Notebook 03 |
| Eliminar filas sin datos esenciales | Las imágenes sin ningún píxel válido no entran en el CSV de índices; las observaciones con demasiada nube y sombra en la parcela se conservan marcadas como no seleccionadas | Notebook 03 |
| Seleccionar los índices relevantes | NDVI, NDRE, NDMI, MSI, EVI y SAVI (apartado 7) | Notebook 03 |
| Analizar observaciones repetidas en la misma fecha | Si más de una tesela interseca la parcela, se combinan las imágenes de cada fecha en un mosaico antes de generar el CSV (una fila por fecha); con una sola tesela se procesa cada imagen como antes. El proceso se detiene si hay más de una imagen seleccionada por fecha | Notebook 03 |
| Decidir si se necesita interpolación | No se interpola | Notebook 03 |
| Diferenciar observado de interpolado | Columnas `interpolado` y `origen_dato` en el resumen semanal | Notebook 03 |
| Incorporar NDRE (trasladado desde la issue #3) | Incorporado el 22/10/2026 (apartado 8) | Notebooks 03 y 01 |
| Criterio de descarte por nube y sombra | Solo cuenta el porcentaje de nube y sombra de la propia parcela (máximo 30 %); revisión del 23/10/2026 | Notebook 03 |
| Periodo de extracción | 01/04/2026 a 01/11/2026; las semanas posteriores a la última imagen se marcan como aún no disponibles | Notebook 03 |
| Documentar las decisiones | Este documento | `docs/` |

## 3. Datos de partida y cadena de generación

1. El notebook 02 prepara el catálogo de parcelas y sus geometrías (lee los
   datos privados de las parcelas de un archivo que no está en el repositorio;
   ver apartado 11).
2. El notebook 03 lee ese catálogo, consulta Sentinel-2 en Google Earth Engine y
   genera, por parcela, el CSV de índices, el CSV de revisión de calidad y el
   resumen semanal.
3. El notebook 01 analiza la estructura de esos CSV (Parte 1) y representa la
   evolución temporal de los índices (Parte 3).

La estructura de los CSV está descrita en `docs/analisis-estructura-csv.md` y la
evolución temporal en `docs/evolucion-temporal-indices.md`.

## 4. Reglas aplicadas

### 4.1 Calidad de píxel

- Se usa la colección Sentinel-2 SR armonizada, filtrada por la geometría de cada
  parcela y por las fechas.
- Se conservan los píxeles con probabilidad de nube inferior a 20 (colección de
  probabilidad de nube de Sentinel-2).
- Se excluyen las clases de la capa de clasificación de escena 0, 1, 3, 8, 9, 10
  y 11 (sin datos, saturado o defectuoso, sombra de nube, nube de probabilidad
  media y alta, cirros y nieve o hielo).
- Se excluyen los píxeles sin valor en las bandas B8A y B9 (bordes).
- Estas máscaras reducen los errores pero no garantizan eliminar toda la nube o
  sombra.

### 4.2 Fechas y orden

La fecha de cada imagen se guarda como texto `YYYY-MM-DD`. Antes de usarla se
comprueba que es una fecha real del calendario y que el inicio del periodo es
anterior al fin. Las tablas se ordenan por `date` e `image_id`.

### 4.3 Imágenes sin datos y filas incompletas

- Para cada imagen (o mosaico) se cuentan los píxeles B8 antes y después de
  aplicar la máscara. Las imágenes sin ningún píxel válido se descartan antes de
  calcular los índices y su recuento queda en el resumen de ejecución: 19, 25, 20
  y 24 en Pancostales, Puri, La Culebra y Los Ceres (en Puri, mosaicos diarios).
- Las imágenes con píxeles válidos entran en el CSV de índices, aunque tengan
  mucha nube y sombra. No se borran las filas no seleccionadas, para poder
  revisarlas.
- Una fila solo se considera seleccionable si todas las medias de los índices
  existen.

### 4.4 Selección técnica provisional

Revisión con los tutores del 23/10/2026: una imagen se descarta solo si el
porcentaje de píxeles de nube y sombra dentro de la propia parcela impide un
estudio correcto, y no por otros factores como los bordes de la imagen o la parte
de la parcela que queda fuera de una tesela.

Una observación se selecciona si cumple a la vez:

- como máximo el 30 % de los píxeles de la parcela son nube o sombra, y
- las medias de todos los índices existen.

Un píxel cuenta como nube si su probabilidad de nube es igual o superior a 20 o
si la clase de escena es 8, 9 o 10, y como sombra si la clase es 3. En parcelas
con varias teselas, un píxel es nube o sombra solo si lo es en todas las teselas
que lo observan. El porcentaje se calcula con la superficie de esos píxeles
respecto a la superficie de la parcela en la cuadrícula de evaluación (20 m). El
umbral del 30 % es provisional y no está validado agronómicamente; equivale al
anterior criterio de cobertura mínima del 70 %.

La cobertura de píxeles válidos (`cobertura_minima_indices_pct`) se conserva en el
CSV de calidad solo como información. En la comprobación del 23/10/2026 con el
periodo hasta el 01/10, el criterio nuevo dio las mismas selecciones que el
anterior: en esas observaciones el porcentaje de nube y sombra y la cobertura
sumaban 100.

Resultado (periodo hasta el 01/11/2026): 26, 33, 28 y 28 observaciones
seleccionadas en Pancostales, Puri, La Culebra y Los Ceres.

### 4.5 Observaciones repetidas y combinación de teselas

Una parcela puede tener imágenes de varias teselas en la misma fecha si se
solapa con ellas. Es el caso de Puri (T30TTL y T30TUL).

- Si más de una tesela interseca la parcela, el notebook aplica primero la máscara
  de calidad a cada tesela y después combina las imágenes de cada fecha en un
  mosaico a nivel de píxel: en cada píxel se usa la tesela con dato válido. El
  CSV tiene así una fila por fecha. El `image_id` del mosaico termina en
  `_T30TTL+T30TUL`.
- Si la parcela cae en una sola tesela, cada imagen se procesa como antes.
- El notebook se detiene si en una misma fecha hay imágenes de adquisiciones
  distintas, para no combinarlas automáticamente.
- Tras la combinación se comprueba que no hay fechas repetidas en el CSV. Si hay
  más de una imagen seleccionada para una fecha, el notebook se detiene antes de
  calcular el resumen semanal. Hay una comprobación adicional sobre el resultado
  del lote.
- En la ejecución realizada hay 0 fechas con varias filas o con varias imágenes
  seleccionadas. En Puri se crean 61 mosaicos diarios a partir de 122 imágenes
  originales y 36 tienen píxeles válidos.

### 4.6 Agregación semanal

El resumen semanal agrupa de lunes (incluido) a lunes siguiente (excluido) y
calcula la media aritmética de las medias de las observaciones seleccionadas de
cada semana. No es una media espacial combinada de todos los píxeles ni una
media continua de todos los días.

- Se incluyen las semanas sin observaciones seleccionadas, con los índices
  ausentes. Hay 31 semanas por parcela; con observaciones seleccionadas, 18, 23,
  19 y 20; sin ellas, 12, 7, 11 y 10.
- Las semanas que empiezan después de la última imagen disponible
  (22/10/2026) se marcan como `periodo_aun_no_disponible` y no se cuentan como
  semanas sin observaciones, porque todavía no ha podido haberlas. Hay una por
  parcela, la del 26/10/2026.
- La primera y la última semana del periodo pueden ser parciales y se marcan en
  `semana_parcial_en_periodo`.
- El valor de una semana se etiqueta con el lunes, pero puede proceder de una
  imagen posterior de esa misma semana. No debe usarse como dato diario en días
  anteriores a la fecha real de la imagen, porque adelantaría información.

## 5. Decisión sobre la interpolación

No se interpola. Motivos:

- Entre observaciones seleccionadas hay huecos de hasta 23 días (23, 20, 23 y 18
  en las cuatro parcelas), y el periodo coincide con el tramo de mayor cambio de
  los índices; interpolar linealmente crearía valores que no se observaron.
- El periodo es provisional y el cultivo no está confirmado, por lo que no hay
  una base agronómica para rellenar.
- Interpolar o no es una decisión del simulador. Lo que se entrega son
  observaciones reales con su calidad, y las semanas sin dato quedan vacías.

Si en el futuro se interpola, deberá marcarse cada valor estimado y distinguirse
de los observados (apartado 6).

## 6. Observado frente a interpolado

El resumen semanal incluye las columnas que permiten distinguirlos:

| Columna | Contenido |
|---|---|
| `interpolado` | Siempre `False` en esta versión |
| `origen_dato` | `agregacion_observaciones_satelitales`, `sin_observaciones_seleccionadas` o `periodo_aun_no_disponible` |
| `metodo_agregacion` | `media_aritmetica` |
| `tiene_observaciones_seleccionadas` | Indica si la semana tiene dato |
| `periodo_aun_no_disponible` | Semana posterior a la última imagen disponible |
| `fecha_ultima_imagen_disponible` | Fecha de la última imagen con información de nubes |
| `n_imagenes_con_datos`, `n_imagenes_seleccionadas`, `n_imagenes_no_seleccionadas` | Recuentos de la semana |
| `fechas_utilizadas`, `imagenes_utilizadas` | Trazabilidad de las observaciones usadas |
| `cobertura_minima_utilizada_pct` | Menor cobertura de píxeles válidos entre las observaciones usadas |
| `nube_sombra_maxima_utilizada_pct` | Mayor porcentaje de nube y sombra entre las observaciones usadas |
| `semana_parcial_en_periodo`, `semana_fin_excluida` | Límites de la semana |
| `parcela_id`, `periodo_provisional` | Identificación y marca de periodo |

El notebook comprueba que el número de imágenes seleccionadas del resumen coincide
con el de la tabla de calidad, que no hay valores en semanas sin observaciones,
que ninguna semana aún no disponible tiene observaciones y que ninguna fila está
marcada como interpolada.

## 7. Índices seleccionados

| Índice | Fórmula | Bandas | Motivo |
|---|---|---|---|
| NDVI | (B8 − B4) / (B8 + B4) | B8, B4 | Vigor de la vegetación; según la especificación del tutor puede alimentar la estimación de Kc (no implementado) |
| NDRE | (B8A − B5) / (B8A + B5) | B8A, B5 | Solicitado en la issue #3; usa la banda de borde rojo |
| NDMI | (B8 − B11) / (B8 + B11) | B8, B11 | Indicador del contenido de agua de la vegetación |
| MSI | B11 / B8 | B11, B8 | Índice de estrés hídrico de la vegetación; lo usa el motor actual |
| EVI | 2,5 · (B8 − B4) / (B8 + 6·B4 − 7,5·B2 + 1) | B8, B4, B2 | Vigor con corrección atmosférica |
| SAVI | 1,5 · (B8 − B4) / (B8 + B4 + 0,5) | B8, B4 | Vigor con corrección del suelo |

Las bandas se convierten a reflectancia multiplicando por 0,0001 y se enmascaran
los denominadores no válidos. Los índices describen la vegetación y no miden la
humedad del suelo. El motor actual (Agrobioma v14) también usa NDWI y RECI, que
no están en la extracción; queda como mejora posible.

## 8. NDRE

NDRE no estaba en la primera extracción de 2026 y se incorporó al extractor el
22/10/2026, dentro del límite de 90 minutos fijado el 21/10/2026.

Cambios en el notebook 03: se añaden las bandas B5 y B8A a la selección de
reflectancia, se calcula `NDRE = (B8A − B5) / (B8A + B5)` con el mismo
tratamiento de denominadores que los demás índices y se añade `NDRE` a la lista
de índices de los parámetros. Se repitió la extracción de las cuatro parcelas
con los mismos parámetros.

Efecto en los datos:

- Los CSV pasan de 56 a 64 columnas (8 estadísticos más) y de 5 a 6 índices.
- En ese momento la selección de observaciones no cambió: 25, 29, 27 y 26
  observaciones seleccionadas en Pancostales, Puri, La Culebra y Los Ceres, con
  las mismas semanas sin dato y los mismos huecos máximos. Los cambios
  posteriores de la selección se deben a la revisión del 23/10/2026
  (apartado 14).
- NDRE tiene la misma cobertura que el resto de índices en cada imagen y no tiene
  medias ausentes.
- Se regeneraron la Parte 1 y la Parte 3 del notebook 01 (con la figura de NDRE)
  y se actualizaron `docs/analisis-estructura-csv.md` y
  `docs/evolucion-temporal-indices.md`.

## 9. Archivos de salida

Los resultados se guardan en Drive, fuera del repositorio, en
`TFG_PATATAS_TRABAJO/resultados/sentinel2_lotes/provisional/`. Cada periodo usa
su propia carpeta (`<inicio>_<fin>`), por lo que los resultados del periodo hasta
el 01/10/2026 no se sobrescriben con los del periodo hasta el 01/11/2026.

| Archivo | Contenido |
|---|---|
| `<parcela>/<inicio>_<fin>/<parcela>_sentinel2_indices_<inicio>_<fin>.csv` | Una fila por imagen (o mosaico) con píxeles válidos: estadísticos de cada índice y calidad |
| `<parcela>/<inicio>_<fin>/<parcela>_sentinel2_indices_calidad_<inicio>_<fin>.csv` | Lo anterior más cobertura por índice, `nube_sombra_parcela_pct`, `apta_nube_sombra` y marca de selección técnica |
| `<parcela>/<inicio>_<fin>/<parcela>_sentinel2_semanal_<inicio>_<fin>.csv` | Resumen semanal sin interpolar |
| `<parcela>/<inicio>_<fin>/revision_calidad_imagenes.csv` | Píxeles antes y después de la máscara por imagen o mosaico |
| `<parcela>/<inicio>_<fin>/resumen_ejecucion.csv` | Recuentos de la ejecución, teselas combinadas y última imagen disponible |
| `<parcela>/<inicio>_<fin>/configuracion_extraccion.json` | Parámetros y momento de la ejecución |
| `comparativas/<inicio>_<fin>/comparativa_parcelas.csv` | Resumen comparativo de las cuatro parcelas |
| `comparativas/<inicio>_<fin>/revision_fechas_seleccionadas.csv` | Control de una imagen por fecha |

Repetir una parcela y un periodo actualiza sus archivos. Una ejecución que falle
puede dejar archivos parciales.

## 10. Dependencias e instrucciones de ejecución

- Dependencias en `requirements.txt`, probadas en Google Colab con Python 3.13.16.
- Orden de ejecución, carpetas de Drive y configuración de Earth Engine en
  `notebooks/README.md`.
- El identificador del proyecto de Earth Engine no se guarda en el notebook: se
  lee del secreto `PROYECTO_EE` de Colab o se pide al ejecutar.

## 11. Publicación y datos sensibles

- El repositorio es público. Los notebooks 02 y 03 se publican sin salidas, y el
  03 también sin el identificador del proyecto de Earth Engine.
- El notebook 02 no contiene las coordenadas, el municipio ni la variedad de las
  parcelas: los lee de `privado/datos_parcelas_privados.py`, un archivo que se
  guarda en Drive y está excluido del repositorio mediante `.gitignore`. La
  plantilla `notebooks/datos_parcelas_privados_ejemplo.py` muestra el formato
  con valores ficticios.
- Los GeoJSON y el catálogo de parcelas también están excluidos del repositorio
  mediante `.gitignore`.
- Los CSV y las coordenadas se guardan en Drive y no se versionan.
- El 22/10/2026 el notebook 03 se subió por error con sus salidas (municipio y
  variedad de las parcelas). Se eliminó y se sustituyó por la versión sin salidas;
  la versión anterior permanece en el historial del repositorio.

## 12. Limitaciones y trabajo posterior

- El periodo es provisional y el cultivo no está confirmado.
- Las imágenes llegan hasta el 22/10/2026 y la última observación con píxeles
  válidos es del 14/10/2026; el resto del periodo hasta el 01/11/2026 requiere
  repetir la extracción.
- Los umbrales de la selección provisional no están validados agronómicamente.
- No se incorporan históricos de sensores, riegos, meteorología ni textura del
  suelo.
- Los índices describen la vegetación y no sustituyen a las mediciones de humedad
  del suelo.
- Los recuentos `*_count` y `pixeles_antes` no son directamente comparables.
- NDWI y RECI, usados por el motor actual, no están en la extracción.
- Las coordenadas, el municipio y la variedad de las parcelas no se publican: el
  notebook 02 solo se puede ejecutar con el archivo privado de datos, que no
  está en el repositorio.

## 13. Evidencias

- Notebooks: `notebooks/02_preparacion_parcelas_reales.ipynb` y
  `notebooks/03_extraccion_sentinel2_parcelas_reales.ipynb` (ambos sin salidas) y
  `notebooks/01_Exploracion_inicial_datos_sentinel-2.ipynb`. Plantilla de datos
  privados: `notebooks/datos_parcelas_privados_ejemplo.py`.
- Documentación: `notebooks/README.md`, `requirements.txt`,
  `docs/analisis-estructura-csv.md` y `docs/evolucion-temporal-indices.md`.

## 14. Cambios de la revisión con los tutores (23/10/2026)

La revisión con los tutores pidió tres cambios en la preparación de los datos.
Cada uno se aplicó y comprobó por separado en el notebook 03.

| Cambio solicitado | Qué se hizo | Resultado |
|---|---|---|
| Parcelas en más de una tesela: combinar los datos antes de generar el CSV | Mosaico diario a nivel de píxel cuando más de una tesela interseca la parcela (apartado 4.5) | Solo afecta a Puri: 68 filas pasan a 35 con el mismo periodo, `pixeles_antes` de 117 y 59 a 117, seleccionadas de 29 a 32, semanas sin dato de 7 a 5 y mayor hueco de 20 a 17 días |
| Descartar solo por nube y sombra de la propia parcela | Se mide el porcentaje de nube y sombra de la parcela y se descarta por encima del 30 % (apartado 4.4) | Con los datos hasta el 01/10, la selección no cambió respecto al criterio anterior: 25, 32, 27 y 26 seleccionadas |
| Periodo del 01/04/2026 al 01/11/2026 | Nueva fecha de fin; las semanas posteriores a la última imagen se marcan como aún no disponibles (apartado 4.6) | 31 semanas por parcela, una aún no disponible; seleccionadas 26, 33, 28 y 28; imágenes hasta el 22/10/2026 |

Resultados finales de la extracción hasta el 01/11/2026:

| Parcela | Filas | Seleccionadas | No seleccionadas | Semanas con datos | Sin datos | Aún no disponibles | Mayor hueco (días) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pancostales | 42 | 26 | 16 | 18 | 12 | 1 | 23 |
| Puri | 36 | 33 | 3 | 23 | 7 | 1 | 20 |
| La Culebra | 41 | 28 | 13 | 19 | 11 | 1 | 23 |
| Los Ceres | 37 | 28 | 9 | 20 | 10 | 1 | 18 |
