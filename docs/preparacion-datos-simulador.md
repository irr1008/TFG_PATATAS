# Preparación de los datos Sentinel-2 para el simulador

Issue #4 · Sprint 2 · Fecha: 22/10/2026
Notebooks: `03_extraccion_sentinel2_parcelas_reales` (extracción y preparación) y
`01_Exploracion_inicial_datos_sentinel-2` (análisis y figuras)

## 1. Objetivo y alcance

Dejar documentadas las decisiones con las que los datos Sentinel-2 de las cuatro
parcelas (Pancostales, Puri, La Culebra y Los Ceres) se preparan para un uso
posterior en el simulador de riego. El periodo de extracción es provisional, del
01/04/2026 (incluido) al 01/10/2026 (excluido), y no se confirma el cultivo
presente en cada parcela. Este documento no genera recomendaciones de riego.

La preparación está implementada en el notebook 03. Este documento recoge las
reglas aplicadas, justifica las decisiones y registra lo que queda pendiente.

## 2. Resumen de decisiones

| Tarea de la issue | Decisión | Dónde se aplica |
|---|---|---|
| Convertir `date` a formato temporal | Fecha en formato `YYYY-MM-DD`, validada como fecha real y convertida con `pd.to_datetime` sin tolerar errores | Notebook 03 |
| Ordenar cronológicamente | Orden por `date` e `image_id` | Notebook 03 |
| Eliminar filas sin datos esenciales | Las imágenes sin ningún píxel válido no entran en el CSV de índices; las filas con cobertura insuficiente se conservan marcadas como no seleccionadas | Notebook 03 |
| Seleccionar los índices relevantes | NDVI, NDRE, NDMI, MSI, EVI y SAVI (apartado 7) | Notebook 03 |
| Analizar observaciones repetidas en la misma fecha | Como máximo una imagen seleccionada por parcela y fecha; el proceso se detiene si hay más | Notebook 03 |
| Decidir si se necesita interpolación | No se interpola | Notebook 03 |
| Diferenciar observado de interpolado | Columnas `interpolado` y `origen_dato` en el resumen semanal | Notebook 03 |
| Incorporar NDRE (trasladado desde la issue #3) | Incorporado el 22/10/2026 (apartado 8) | Notebooks 03 y 01 |
| Documentar las decisiones | Este documento | `docs/` |

## 3. Datos de partida y cadena de generación

1. El notebook 02 prepara el catálogo de parcelas y sus geometrías (no está en el
   repositorio; ver apartado 11).
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

- Para cada imagen se cuentan los píxeles B8 antes y después de aplicar la
  máscara. Las imágenes sin ningún píxel válido se descartan antes de calcular
  los índices y su recuento queda en el resumen de ejecución (15, 40, 15 y 19
  imágenes en Pancostales, Puri, La Culebra y Los Ceres).
- Las imágenes con píxeles válidos entran en el CSV de índices, aunque su
  cobertura de parcela sea baja. No se borran las filas no seleccionadas, para
  poder revisarlas.
- Una fila solo se considera seleccionable si todas las medias de los índices
  existen.

### 4.4 Selección técnica provisional

Una observación se selecciona si cumple a la vez:

- cobertura mínima de la parcela del 70 % en todos los índices, y
- medias completas de todos los índices.

La cobertura se calcula con el área de píxeles válidos de cada índice respecto a
una referencia de la parcela en la cuadrícula de evaluación. Los umbrales (nube
20 y cobertura 70 %) son provisionales y no están validados agronómicamente.
Resultado: 25, 29, 27 y 26 observaciones seleccionadas en Pancostales, Puri, La
Culebra y Los Ceres.

### 4.5 Observaciones repetidas en la misma fecha

Una parcela puede tener varias imágenes en una fecha si se solapa con varias
teselas. Es el caso de Puri (T30TTL y T30TUL).

- No se eliminan imágenes por fecha sin revisar su cobertura.
- Si hay más de una imagen seleccionada para una fecha, el notebook se detiene
  con un error antes de calcular el resumen semanal; no resuelve el caso
  automáticamente. Hay una comprobación adicional sobre el resultado del lote.
- En la ejecución realizada no hay ninguna fecha con varias imágenes
  seleccionadas. En Puri, la tesela T30TTL cubre solo parte de la parcela y no
  alcanza el 70 %, por lo que se selecciona la otra.

### 4.6 Agregación semanal

El resumen semanal agrupa de lunes (incluido) a lunes siguiente (excluido) y
calcula la media aritmética de las medias de las observaciones seleccionadas de
cada semana. No es una media espacial combinada de todos los píxeles ni una
media continua de todos los días.

- Se incluyen las semanas sin observaciones seleccionadas, con los índices
  ausentes. Hay 27 semanas por parcela; sin observaciones seleccionadas, 10, 7,
  9 y 9.
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
| `origen_dato` | `agregacion_observaciones_satelitales` o `sin_observaciones_seleccionadas` |
| `metodo_agregacion` | `media_aritmetica` |
| `tiene_observaciones_seleccionadas` | Indica si la semana tiene dato |
| `n_imagenes_con_datos`, `n_imagenes_seleccionadas`, `n_imagenes_no_seleccionadas` | Recuentos de la semana |
| `fechas_utilizadas`, `imagenes_utilizadas` | Trazabilidad de las observaciones usadas |
| `cobertura_minima_utilizada_pct` | Menor cobertura entre las observaciones usadas |
| `semana_parcial_en_periodo`, `semana_fin_excluida` | Límites de la semana |
| `parcela_id`, `periodo_provisional` | Identificación y marca de periodo |

El notebook comprueba que el número de imágenes seleccionadas del resumen coincide
con el de la tabla de calidad, que no hay valores en semanas sin observaciones y
que ninguna fila está marcada como interpolada.

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
- La selección de observaciones no cambia: 25, 29, 27 y 26 observaciones
  seleccionadas en Pancostales, Puri, La Culebra y Los Ceres, con las mismas
  semanas sin dato y los mismos huecos máximos.
- NDRE tiene la misma cobertura que el resto de índices en cada imagen y no tiene
  medias ausentes.
- Se regeneraron la Parte 1 y la Parte 3 del notebook 01 (con la figura de NDRE)
  y se actualizaron `docs/analisis-estructura-csv.md` y
  `docs/evolucion-temporal-indices.md`.

## 9. Archivos de salida

Los resultados se guardan en Drive, fuera del repositorio, en
`TFG_PATATAS_TRABAJO/resultados/sentinel2_lotes/provisional/`.

| Archivo | Contenido |
|---|---|
| `parcela/inicio_fin/parcela_sentinel2_indices_inicio_fin.csv` | Una fila por imagen con píxeles válidos: estadísticos de cada índice y calidad |
| `parcela/inicio_fin/parcela_sentinel2_indices_calidad_inicio_fin.csv` | Lo anterior más cobertura por índice y marca de selección técnica |
| `parcela/inicio_fin/parcela_sentinel2_semanal_inicio_fin.csv` | Resumen semanal sin interpolar |
| `parcela/inicio_fin/revision_calidad_imagenes.csv` | Píxeles antes y después de la máscara por imagen |
| `parcela/inicio_fin/resumen_ejecucion.csv` | Recuentos de la ejecución |
| `parcela/inicio_fin/configuracion_extraccion.json` | Parámetros y momento de la ejecución |
| `comparativas/inicio_fin/comparativa_parcelas.csv` | Resumen comparativo de las cuatro parcelas |
| `comparativas/inicio_fin/revision_fechas_seleccionadas.csv` | Control de una imagen por fecha |

Repetir una parcela y un periodo actualiza sus archivos. Una ejecución que falle
puede dejar archivos parciales.

## 10. Dependencias e instrucciones de ejecución

- Dependencias en `requirements.txt`, probadas en Google Colab con Python 3.13.16.
- Orden de ejecución, carpetas de Drive y configuración de Earth Engine en
  `notebooks/README.md`.
- El identificador del proyecto de Earth Engine no se guarda en el notebook: se
  lee del secreto `PROYECTO_EE` de Colab o se pide al ejecutar.

## 11. Publicación y datos sensibles

- El repositorio es público. El notebook 03 se publica sin salidas y sin el
  identificador del proyecto de Earth Engine.
- El notebook 02 no se publica: contiene las coordenadas de las parcelas y sus
  salidas incluyen datos de las explotaciones. Se publicará una versión saneada
  solo si los tutores autorizan publicar esos datos.
- Los CSV y las coordenadas se guardan en Drive y no se versionan.
- El 22/10/2026 el notebook 03 se subió por error con sus salidas (municipio y
  variedad de las parcelas). Se eliminó y se sustituyó por la versión sin salidas;
  la versión anterior permanece en el historial del repositorio.

## 12. Limitaciones y trabajo posterior

- El periodo es provisional y el cultivo no está confirmado.
- Los umbrales de la selección provisional no están validados agronómicamente.
- No se incorporan históricos de sensores, riegos, meteorología ni textura del
  suelo.
- Los índices describen la vegetación y no sustituyen a las mediciones de humedad
  del suelo.
- Los recuentos `*_count` y `pixeles_antes` no son directamente comparables.
- NDWI y RECI, usados por el motor actual, no están en la extracción.
- Pendiente de los tutores: autorización para publicar coordenadas, municipio y
  variedad.

## 13. Evidencias

- Notebooks: `notebooks/03_extraccion_sentinel2_parcelas_reales.ipynb` (sin
  salidas) y `notebooks/01_Exploracion_inicial_datos_sentinel-2.ipynb`.
- Documentación: `notebooks/README.md`, `requirements.txt`,
  `docs/analisis-estructura-csv.md` y `docs/evolucion-temporal-indices.md`.
