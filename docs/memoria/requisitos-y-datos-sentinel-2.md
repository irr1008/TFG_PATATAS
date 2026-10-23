# Requisitos, arquitectura y consolidación de datos Sentinel-2

## 1. Objetivo y contexto del sprint

El segundo sprint se desarrolló del 19 al 23 de octubre de 2026. Su objetivo fue
actualizar el alcance y la arquitectura del sistema a partir de los documentos del
tutor, consolidar los datos Sentinel-2 de las cuatro parcelas y revisar los
entregables de la iteración.

La planificación general denominaba esta iteración «Requisitos y revisión
bibliográfica». El alcance se adaptó para revisar el sistema existente, consolidar
la información satelital ya preparada y verificar los entregables. No se ha
realizado una revisión bibliográfica sistemática, por lo que no se presenta como
completada. También se corrigió la asignación inicial de las issues #1 a #4, que
se habían vinculado a otra iteración.

La capacidad de referencia fue de cuatro horas por jornada durante cinco
jornadas, es decir, 20 horas, todas asignadas a las cinco tareas del sprint:

| Issue | Tarea | Estimación (h) |
|---|---|---:|
| #1 | Documentar el alcance y la arquitectura inicial del sistema | 4 |
| #2 | Analizar la estructura del CSV generado por Sentinel-2 | 3 |
| #3 | Representar la evolución temporal de los índices espectrales | 5 |
| #4 | Preparar los datos Sentinel-2 para el simulador | 4 |
| #6 | Revisar los entregables y documentar el cierre del sprint 2 | 4 |

Antes de la planificación existían notebooks y análisis de trabajo sobre los
datos satelitales. Ese trabajo es el punto de partida del sprint. Se revisó,
amplió, documentó y publicó durante la iteración, pero no se presenta como
desarrollado íntegramente en ella.

## 2. Alcance y arquitectura del sistema (issue #1)

El proyecto parte de un motor de decisión de riego para patata, denominado
Agrobioma v14, que combina la lectura de una sonda de humedad, datos
meteorológicos e índices satelitales para emitir una recomendación diaria. Los
documentos del tutor especifican una versión mejorada, a la que contribuye el TFG.

El motor actual utiliza una sonda única a 25 cm, capacidad de campo y punto de
marchitez tomados de la ficha de cada parcela, una evapotranspiración estimada con
una fórmula empírica y una recomendación en dosis con fraccionamiento. El motor
especificado por el tutor se organiza en cuatro módulos:

| Módulo | Función | Entradas principales |
|---|---|---|
| 1. Hidrofísica del suelo | Punto de marchitez y capacidad de campo | Textura, humedad de sondas |
| 2. Crecimiento del cultivo | Profundidad radicular y coeficiente de cultivo dinámicos | Tiempo térmico, NDVI |
| 3. Evapotranspiración de referencia | Penman-Monteith FAO-56 | Temperatura, viento, radiación neta, déficit de presión de vapor |
| 4. Decisión | Humedad ponderada, umbral, agua fácilmente disponible y lámina de riego | Salidas de los módulos 1 a 3 y sondas |

Los componentes que se pretende mejorar son la sustitución de la
evapotranspiración empírica por Penman-Monteith, la incorporación de sondas a
varias profundidades, la estimación del coeficiente de cultivo a partir del NDVI
de Sentinel-2 y la calibración de la capacidad de campo real. Ninguno se
implementa en este sprint.

Las entradas se clasificaron según su disponibilidad. Están disponibles los
índices Sentinel-2 de las cuatro parcelas, el catálogo de parcelas y el histórico
de sondas proporcionado por el profesorado. Están pendientes los riegos aplicados,
la meteorología, la textura del suelo y las fechas agronómicas. Los datos
sintéticos, si se usan, se identificarán como tales. En esta fase el prototipo no
emite recomendaciones operativas de riego: sus salidas son series satelitales
analizadas y datos preparados para un simulador.

Sentinel-2 aporta índices por parcela y semana. El NDVI alimentará la estimación
del coeficiente de cultivo del módulo 2, relación que está especificada y no
implementada. Los índices no miden la humedad del suelo y no sustituyen a las
sondas.

## 3. Datos Sentinel-2 de partida

El trabajo con los datos satelitales se organiza en tres notebooks que se
ejecutan en Google Colab y guardan sus resultados en Google Drive:

| Notebook | Función |
|---|---|
| 02. Preparación de parcelas reales | Genera el catálogo de parcelas y sus geometrías y comprueba su validez |
| 03. Extracción Sentinel-2 de parcelas reales | Usa el catálogo para extraer Sentinel-2 con Google Earth Engine y genera los CSV de índices, de calidad y el resumen semanal |
| 01. Exploración inicial de datos Sentinel-2 | Analiza la estructura de los CSV (Parte 1), incluye un ejemplo previo con maíz de 2018 (Parte 2) y representa la evolución temporal de los índices (Parte 3) |

Se trabaja con cuatro parcelas: Pancostales, Puri, La Culebra y Los Ceres. Los
Ceres se unificó a partir de dos registros de geometría, según la confirmación del
estudiante. La extracción es provisional y abarca del 01/04/2026 (incluido) al
01/11/2026 (excluido). Las imágenes disponibles llegan hasta el 22/10/2026 y la
última observación con píxeles válidos es del 14/10/2026. No se confirma el
cultivo presente en cada parcela durante ese periodo, ni la campaña ni las fechas
agronómicas.

Los parámetros de la extracción son una probabilidad de nube inferior a 20 a nivel
de píxel, un máximo del 30 % de píxeles de nube y sombra dentro de la parcela para
seleccionar una observación y una escala de evaluación de 20 m. Los índices
calculados son NDVI, NDRE, NDMI, MSI, EVI y SAVI.

## 4. Estructura de los datos (issue #2)

Los CSV de índices tienen 64 columnas, idénticas en las cuatro parcelas: seis de
identificación, cuatro de calidad, seis de contexto de extracción y 48 de
estadísticas (seis índices con ocho estadísticos cada uno). Cada fila corresponde
a una imagen, o a un mosaico diario en el caso de Puri, con al menos un píxel
válido tras la máscara de calidad.

| Parcela | Filas | Imágenes originales | Sin ningún píxel válido |
|---|---:|---:|---:|
| Pancostales | 42 | 61 | 19 |
| Puri | 36 | 122 (61 mosaicos diarios) | 25 |
| La Culebra | 41 | 61 | 20 |
| Los Ceres | 37 | 61 | 24 |

Los huecos temporales no aparecen como valores nulos: cuando no hay imagen con
píxeles válidos, no hay fila. Las observaciones no son diarias, por lo que
cualquier uso posterior debe tolerar semanas sin dato. El porcentaje de píxeles
conservados varía entre el 3 % y el 100 % dentro de cada parcela, por lo que los
CSV no pueden usarse sin una selección previa.

El análisis distingue qué variables pueden utilizarse en fases posteriores (los
seis índices, la calidad de cada imagen y el resumen semanal sin interpolar) y
cuáles no proporciona este procesamiento: NDWI y RECI, que usa el motor actual, la
humedad del suelo, la meteorología, los riegos, la textura del suelo y las fechas
agronómicas confirmadas.

## 5. Evolución temporal de los índices (issue #3)

Se representó la evolución temporal de NDVI, NDRE, NDMI y EVI en las cuatro
parcelas. La issue solicitaba NDRE, que no estaba en la extracción inicial. El
21/10/2026 se decidió trasladar su incorporación a la issue #4, y el 22/10/2026 
se incorporó al extractor con las bandas B8A y B5. Con ello los CSV pasaron de 56 a 
64 columnas y de cinco a seis índices.

Los gráficos previos, hechos con un CSV de maíz de 2018, se revisaron y se
conservaron solo como ejemplo metodológico. Las figuras nuevas presentan un panel
por parcela con el mismo eje vertical, distinguen las observaciones seleccionadas
de las no seleccionadas, cortan la línea cuando pasan más de 14 días entre
observaciones y no interpolan ningún valor. Incluyen título con el periodo
provisional, ejes y leyenda.

En las cuatro parcelas se observa un patrón parecido: valores bajos en abril y
mayo, un aumento durante junio, un máximo a finales de junio o principios de julio
y un descenso posterior. El máximo de NDVI va de 0,815 en Pancostales a 0,938 en La
Culebra. Hay diez huecos de más de 14 días entre observaciones seleccionadas,
concentrados en tres ventanas (finales de abril a mediados de mayo, junio y del
24/09 al 14/10), y el aumento de los índices en junio es el tramo menos muestreado.
En Los Ceres aparece un mínimo local el 24/07/2026 que no se explica por exceso de
nube y sombra; su causa queda sin determinar y no se interpreta. Estas
descripciones se refieren solo al comportamiento de los índices y no permiten
inferir el estado hídrico, la fenología ni el cultivo.

## 6. Preparación de los datos para el simulador (issue #4)

La preparación está implementada en el notebook 03 y documentada en
`docs/preparacion-datos-simulador.md`. Las decisiones principales son:

- **Calidad de píxel.** Se conservan los píxeles con probabilidad de nube inferior
  a 20 y se excluyen varias clases de la clasificación de escena (sin datos,
  sombra de nube, nube, cirros y nieve o hielo).
- **Selección técnica provisional.** Una observación se selecciona si como máximo
  el 30 % de los píxeles de la parcela son nube o sombra y existen las medias de
  todos los índices. Las observaciones no seleccionadas se conservan marcadas para
  poder revisarlas.
- **Observaciones repetidas.** Si una parcela cae en más de una tesela, las
  imágenes de cada fecha se combinan en un mosaico píxel a píxel, de modo que hay
  una fila por fecha. El notebook se detiene si detecta más de una imagen
  seleccionada para una fecha.
- **Agregación semanal.** El resumen agrupa las observaciones seleccionadas de
  lunes a lunes y calcula la media aritmética de sus medias. Incluye las semanas
  sin observaciones, con los índices ausentes.
- **Interpolación.** No se interpola: entre observaciones seleccionadas hay
  huecos de hasta 23 días en un periodo de cambio rápido de los índices, y no hay
  base agronómica para rellenar. El resumen semanal incluye las columnas
  `interpolado` y `origen_dato` para distinguir lo observado de lo estimado.

Los resultados se guardan en Drive, con una carpeta por parcela y periodo, y no se
versionan. También se revisaron las dependencias (`requirements.txt`), las
instrucciones de ejecución (`notebooks/README.md`) y los archivos de salida.

## 7. Revisión con los tutores del 23/10/2026

La revisión con los tutores del 23/10/2026 pidió tres cambios en la preparación de
los datos. Cada uno se aplicó y se comprobó por separado en el notebook 03:

| Cambio solicitado | Qué se hizo | Resultado |
|---|---|---|
| Combinar los datos de las parcelas que caen en más de una tesela antes de generar el CSV | Mosaico diario a nivel de píxel | Solo afecta a Puri: con el mismo periodo, 68 filas pasan a 35, las observaciones seleccionadas de 29 a 32, las semanas sin dato de 7 a 5 y el mayor hueco de 20 a 17 días |
| Descartar una imagen solo por la nube y sombra de la propia parcela | Se mide el porcentaje de nube y sombra de la parcela y se descarta por encima del 30 % | Con los datos hasta el 01/10, la selección no cambió respecto al criterio anterior |
| Modificar el periodo hasta el 01/11/2026 | Nueva fecha de fin; las semanas posteriores a la última imagen se marcan como aún no disponibles | 31 semanas por parcela, una de ellas aún no disponible |

Resultado final de la extracción hasta el 01/11/2026:

| Parcela | Filas | Seleccionadas | No seleccionadas | Semanas con datos | Semanas sin datos | Mayor hueco (días) |
|---|---:|---:|---:|---:|---:|---:|
| Pancostales | 42 | 26 | 16 | 18 | 12 | 23 |
| Puri | 36 | 33 | 3 | 23 | 7 | 20 |
| La Culebra | 41 | 28 | 13 | 19 | 11 | 23 |
| Los Ceres | 37 | 28 | 9 | 20 | 10 | 18 |

Tras estos cambios se regeneraron el notebook 01, las figuras y los documentos de
análisis, evolución temporal y preparación de datos.

## 8. Publicación y protección de los datos

El repositorio es público y los datos de las explotaciones no deben publicarse sin
autorización. El 22/10/2026 el notebook 03 se subió por error con salidas que
mostraban datos de las parcelas. Se detectó al revisar el contenido del archivo, se
eliminó y se sustituyó por una versión sin salidas. Las versiones anteriores
permanecen en el historial del repositorio.

El notebook 02 no se publicó inicialmente porque contenía las coordenadas de las
parcelas. A propuesta del profesor, el 23/10/2026 se publicó sin salidas y sin
coordenadas, municipio ni variedad. Estos datos se guardan en un archivo
`datos_parcelas_privados.py` en Google Drive, excluido del repositorio mediante
`.gitignore` junto con los GeoJSON y el catálogo de parcelas. El repositorio incluye
una plantilla con valores ficticios, `notebooks/datos_parcelas_privados_ejemplo.py`,
que muestra el formato. Se comprobó que el notebook se ejecuta correctamente con la
plantilla y con los datos reales y que genera los mismos archivos.

## 9. Limitaciones y trabajo pendiente

- El periodo de extracción es provisional y el cultivo no está confirmado.
- Falta confirmar la campaña y las fechas agronómicas de las parcelas.
- La extracción debe repetirse para incorporar las imágenes posteriores al
  22/10/2026.
- No se han incorporado los históricos de sensores y riego, la meteorología ni la
  textura del suelo.
- NDWI y RECI, usados por el motor actual, no están en la extracción.
- Los umbrales de la selección provisional no están validados agronómicamente.
- Los índices describen la vegetación y no sustituyen las mediciones de humedad del
  suelo.
- La revisión bibliográfica sistemática no se ha realizado.
- No se implementa el motor de recomendación, no se entrenan modelos y no se emiten
  recomendaciones de riego.

## 10. Revisión y retrospectiva

La revisión del sprint se realizó el 23/10/2026 y se registra en `docs/sprint-02.md`. 
Las cuatro tareas técnicas (#1 a #4) y la configuración de la gestión (#5) están cerradas, 
y la tarea #6 se cierra con la documentación del sprint.

Lo que funcionó bien fue la corrección de criterios con los tutores antes del
cierre, el contraste de las cifras entre el notebook 03, el notebook 01 y los
documentos, la documentación de cada decisión y la separación de los datos
privados del código.

Las dificultades fueron la publicación del notebook 03 con salidas, varios ciclos
de borrar y volver a subir notebooks y figuras, la llegada de los cambios de
criterio el último día del sprint sin horas de margen y la falta de registro de las
horas reales.

Las mejoras propuestas para el siguiente sprint son aplicar una lista de
comprobación antes de subir un archivo, mantener los datos privados fuera de los
notebooks desde el inicio, pedir a los tutores a mitad del sprint la confirmación
de los criterios que afectan a los datos, reservar un margen de horas, registrar
las horas reales y decidir si la revisión bibliográfica se planifica o se
descarta.

## 11. Trazabilidad

| Elemento | Referencia |
|---|---|
| Issues | #1, #2, #3, #4, #5 y #6 |
| Seguimiento del sprint | `docs/sprint-02.md` |
| Alcance y arquitectura | `docs/alcance-y-arquitectura.md` |
| Estructura de los datos | `docs/analisis-estructura-csv.md` |
| Evolución temporal | `docs/evolucion-temporal-indices.md` y `docs/figuras/` |
| Preparación de datos | `docs/preparacion-datos-simulador.md` |
| Notebooks | `notebooks/01_Exploracion_inicial_datos_sentinel-2.ipynb`, `notebooks/02_preparacion_parcelas_reales.ipynb`, `notebooks/03_extraccion_sentinel2_parcelas_reales.ipynb` y `notebooks/README.md` |
| Datos privados | `notebooks/datos_parcelas_privados_ejemplo.py` (plantilla) y `.gitignore` |
| Dependencias y plan | `requirements.txt` y `PLAN_TRABAJO.md` |

El historial del repositorio y los documentos de seguimiento son las evidencias del
desarrollo, de las decisiones adoptadas y de la evolución de la planificación.
