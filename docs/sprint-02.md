# Seguimiento del sprint 2

## Información del sprint

- Sprint: 2 — Requisitos, arquitectura y consolidación de datos.
- Objetivo: actualizar el alcance y la arquitectura del sistema a partir
  de los documentos del tutor, consolidar los datos Sentinel-2 de las
  cuatro parcelas y revisar los entregables del sprint.
- Fecha de inicio: 19/10/2026.
- Fecha objetivo: 23/10/2026.
- Responsable: irr1008.
- Milestone asociado a la issue de revisión: M1 - Preparación y análisis inicial.
- Estado del sprint: cerrado el 23/10/2026, con el trabajo pendiente identificado
  en la revisión del sprint.

### Adaptación de la planificación inicial

La planificación general denominaba esta iteración
«Requisitos y revisión bibliográfica».

El alcance se adapta para revisar el sistema existente, consolidar
la información satelital ya preparada y verificar los entregables.
Esto no implica que se haya completado una revisión bibliográfica
sistemática. Esa actividad se mantendrá identificada si sigue formando
parte del proyecto.

También se corrige la asignación inicial de las issues #1 a #4, que
se habían vinculado a otra iteración. Su trabajo se planifica y revisa
en el sprint 2.

## Capacidad y estimación

- Unidad de estimación: horas de trabajo.
- Capacidad de referencia: cuatro horas por jornada, de lunes a viernes.
- Jornadas planificadas: 19, 20, 21, 22 y 23 de octubre de 2026.
- Capacidad de referencia: 20 horas.
- Esfuerzo previsto en las cinco tareas: 20 horas.
- Margen no asignado: 0 horas.

Las estimaciones representan trabajo restante previsto. No incluyen ni
sustituyen el esfuerzo ya invertido en los notebooks preparados con
anterioridad.

El trabajo realizado el fin de semana se registrará si se produce, pero
no se incorpora automáticamente a la capacidad de referencia.

Al no existir margen libre, cualquier desviación relevante obligará a
registrar una decisión de replanificación o de reducción de alcance.

## Tareas seleccionadas

| Issue | Tarea | Prioridad | Estimación (h) | Fecha de inicio | Fecha objetivo | Estado al planificar |
|---|---|---|---:|---|---|---|
| #1 | Documentar el alcance y la arquitectura inicial del sistema | Alta | 4 | 17/10/2026 | 19/10/2026 | En progreso |
| #2 | Analizar la estructura del CSV generado por Sentinel-2 | Alta | 3 | 20/10/2026 | 20/10/2026 | Por hacer |
| #3 | Representar la evolución temporal de los índices espectrales | Media | 5 | 20/10/2026 | 21/10/2026 | Por hacer |
| #4 | Preparar los datos Sentinel-2 para el simulador | Alta | 4 | 22/10/2026 | 22/10/2026 | Por hacer |
| #6 | Revisar los entregables y documentar el cierre del sprint 2 | Alta | 4 | 23/10/2026 | 23/10/2026 | Por hacer |

Total estimado: 20 horas.

Los estados actuales se mantienen en GitHub Projects. Esta tabla conserva
la situación inicial de la planificación.

Las fechas del tablero son fechas planificadas. La ejecución real, los
retrasos y las desviaciones se registrarán en las issues y en las
secciones de revisión y evidencias.

### Distribución de referencia

| Jornada | Trabajo previsto | Horas |
|---|---|---:|
| Lunes 19/10 | Issue #1 | 4 |
| Martes 20/10 | Issue #2 y comienzo de la issue #3 | 4 |
| Miércoles 21/10 | Continuación de #3 | 4 |
| Jueves 22/10 | Issue #4 | 4 |
| Viernes 23/10 | Issue #6 | 4 |

Las tareas que comparten fecha no se consideran paralelas: se mantiene
el límite de una tarea principal en estado En progreso.

## Trabajo previo disponible

Antes de esta planificación existen análisis y notebooks de trabajo:

- Exploración inicial de datos Sentinel-2.
- Preparación y validación de las cuatro parcelas.
- Extracción automática de imágenes y cálculo de índices.
- Revisión de calidad y cobertura.
- Resúmenes semanales y comparación entre parcelas.
- Control de observaciones seleccionadas por fecha.

Este trabajo es el punto de partida de las issues. Su revisión,
documentación e incorporación al repositorio se registrarán conservando
las fechas reales de su elaboración.

No se presenta como desarrollado íntegramente dentro del sprint 2.

## Resultado esperado y criterios de comprobación

### Issue #1: alcance y arquitectura

- Identificar el motor de decisión existente como sistema de referencia.
- Describir los componentes que se pretende mejorar.
- Diferenciar entradas disponibles, pendientes y sintéticas.
- Definir salidas previstas y limitaciones del prototipo.
- Documentar cómo encaja el procesamiento satelital en la arquitectura.

### Issue #2: estructura de los datos

- Revisar los CSV actuales de las cuatro parcelas.
- Documentar columnas, tipos, fechas y valores ausentes.
- Distinguir imágenes, fechas distintas y observaciones seleccionadas.
- Explicar los indicadores de calidad y cobertura.
- Identificar qué variables pueden utilizarse posteriormente y cuáles
  no proporciona este procesamiento.

### Issue #3: evolución temporal

- Revisar los gráficos existentes y completar los necesarios para las
  parcelas reales.
- Incluir títulos, ejes, leyendas y referencia al periodo provisional.
- Mantener visibles los huecos de observación.
- Resolver explícitamente la diferencia entre el NDRE solicitado y los
  índices del extractor actual.
- No considerar completada la tarea sin documentar esa decisión.

### Issue #4: preparación para el uso posterior

- Revisar los notebooks de parcelas y extracción automática.
- Conservar la trazabilidad de los datos y la selección técnica.
- Verificar el control de varias imágenes seleccionadas por fecha.
- Documentar la agregación semanal sin interpolación.
- Revisar dependencias, instrucciones de ejecución y archivos de salida.
- Antes de publicar entregables, revisar credenciales, salidas sensibles
  y permisos sobre los datos.

### Issue #6: revisión y cierre

- Comprobar la coherencia entre objetivo, issues, notebooks y documentación.
- Verificar evidencias, fechas provisionales y semanas sin observaciones.
- Revisar que no se hayan publicado credenciales ni archivos sin permiso.
- Registrar discrepancias y decisiones.
- Completar la revisión, la retrospectiva y las evidencias finales.

## Límites del sprint

- El periodo de extracción sigue siendo provisional.
- No se confirma el cultivo presente en cada parcela durante ese periodo.
- No se incorporan todavía los históricos de sensores y riego.
- No se implementa el motor completo de recomendación.
- No se entrenan modelos de aprendizaje automático.
- No se emiten recomendaciones operativas de riego.
- Las semanas sin observaciones seleccionadas conservan valores ausentes.

## Impedimentos

### Limitaciones conocidas al inicio

- Falta confirmar la campaña y las fechas agronómicas de las parcelas.
- Los históricos no se incorporan en esta fase.
- Los índices satelitales no sustituyen las mediciones de humedad del suelo.
- Existen huecos temporales en las observaciones seleccionadas.
- NDRE no estaba en la extracción de 2026; se incorporó el 22/10/2026 en la
  issue #4 (ver decisiones del sprint).
- La planificación no dispone de margen libre de horas.

Estas limitaciones no bloquean automáticamente todas las tareas.
Si alguna impide continuar una actividad concreta, se registrará en la
issue afectada y se utilizará el estado Bloqueado.

### Limitaciones que siguen abiertas

- La campaña y las fechas agronómicas de las parcelas siguen sin confirmar.
- La extracción debe repetirse para incorporar las imágenes posteriores al
  22/10/2026 hasta el fin del periodo (01/11/2026).
- Los históricos de sensores y riego no se han incorporado.

### Decisiones durante el sprint

- 20/10/2026: los notebooks 02 y 03 no se publican por ahora. El 02
  contiene las coordenadas de las parcelas y ambos incluyen salidas con
  datos de las explotaciones, y el repositorio es público. Se publicarán
  versiones saneadas tras revisar los permisos sobre los datos (issue #4).
  Resolución: ver las decisiones del 22/10/2026 y del 23/10/2026.
- 21/10/2026: la incorporación de NDRE al extractor se traslada de la
  issue #3 a la issue #4.
- 22/10/2026: el notebook 03 se publicó por error con sus salidas
  (municipio y variedad de las parcelas). Se detectó al revisar el contenido
  del archivo, se eliminó y se sustituyó por la versión sin salidas. La
  versión anterior permanece en el historial del repositorio.
- 22/10/2026: NDRE se incorporó al extractor (bandas B8A y B5). Se repitió la
  extracción de las cuatro parcelas y la selección de observaciones no cambió
  (25, 29, 27 y 26). Los CSV pasan de 56 a 64 columnas y de 5 a 6 índices. Se
  regeneraron las Partes 1 y 3 del notebook 01 y se actualizaron los documentos
  asociados.
- 22/10/2026: el notebook 03 se publica sin salidas y sin el identificador del
  proyecto de Earth Engine. El 02 queda sin publicar por los datos de las
  parcelas (resuelto el 23/10/2026).
- 22/10/2026: las reglas de preparación de los datos (sin interpolación, una
  imagen seleccionada por parcela y fecha, agregación semanal y distinción entre
  observado e interpolado) quedan documentadas en
  `docs/preparacion-datos-simulador.md`.
- 23/10/2026: revisión con los tutores. Se combinan en un mosaico las teselas de
  una misma fecha (afecta a Puri), una imagen se descarta solo por el porcentaje
  de nube y sombra de la propia parcela (máximo 30 %) y el periodo de extracción
  pasa a ser del 01/04/2026 al 01/11/2026. Se repitió la extracción de las cuatro
  parcelas (26, 33, 28 y 28 observaciones seleccionadas) y se actualizaron los
  documentos.
- 23/10/2026: a propuesta del profesor, el notebook 02 se publica sin salidas y
  sin coordenadas, municipio ni variedad. Los lee de `datos_parcelas_privados.py`,
  un archivo que se guarda en Drive y está excluido del repositorio mediante
  `.gitignore`. Se publica una plantilla con valores ficticios,
  `notebooks/datos_parcelas_privados_ejemplo.py`. Se actualizaron
  `notebooks/README.md`, `PLAN_TRABAJO.md` y los documentos de análisis y de
  preparación.

## Revisión del sprint

Revisión realizada el 23/10/2026 en la issue #6.

### Estado de las issues

Las issues #1, #2, #3 y #4 están cerradas, igual que la #5 (configuración de la
gestión Scrum-Kanban, fuera de las cinco tareas seleccionadas). La issue #6 se
cierra con la actualización de este documento.

### Comprobaciones realizadas

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Coherencia entre objetivo, notebooks y documentación | Revisada tras los cambios del 23/10/2026. Las cifras de selección (26, 33, 28 y 28 observaciones) coinciden en el análisis de estructura, en el documento de preparación y en la memoria | `docs/analisis-estructura-csv.md`, `docs/preparacion-datos-simulador.md`, `docs/memoria/requisitos-y-datos-sentinel-2.md` |
| Fechas y parámetros provisionales | Indicados: periodo del 01/04/2026 al 01/11/2026, imágenes hasta el 22/10/2026, última observación con píxeles válidos el 14/10/2026, umbrales sin validar agronómicamente | Apartados 1 y 9 del análisis; apartados 4 y 12 de la preparación |
| Semanas sin observaciones | No se presentan como datos reales: conservan valores ausentes, `interpolado` es siempre `False` y la semana del 26/10/2026 se marca como aún no disponible | Apartados 4.6 a 6 de la preparación |
| Credenciales y archivos sin permiso | Los notebooks 02 y 03 se publican sin salidas. El 03 no incluye el identificador del proyecto de Earth Engine. El 02 no incluye coordenadas, municipio ni variedad. `.gitignore` excluye el archivo privado, los GeoJSON y el catálogo. La búsqueda en el repositorio de los municipios y las variedades de las parcelas no dio coincidencias en los archivos que GitHub indexa | `notebooks/README.md`, `.gitignore` |
| Notebook 01 (con salidas) | Revisado: sus salidas muestran solo los nombres de las columnas de municipio y variedad, sin sus valores, y no incluyen coordenadas, identificadores de proyecto ni códigos de verificación | `notebooks/01_Exploracion_inicial_datos_sentinel-2.ipynb` |
| Evidencias identificables | Cada issue enlaza sus documentos, notebooks y figuras (apartado de evidencias) | Este documento |

La versión del notebook 03 publicada con salidas el 22/10/2026 y las versiones
intermedias de los días 22 y 23 permanecen en el historial del repositorio, como
se registra en las decisiones del sprint.

### Discrepancias y decisiones

| Discrepancia | Decisión |
|---|---|
| La planificación hablaba de «revisión bibliográfica» y no se ha realizado | No se presenta como completada. Se mantiene como trabajo posterior |
| NDRE se solicitó en la issue #3 y no estaba en la extracción | Se incorporó al extractor el 22/10/2026 (issue #4) |
| Notebook 03 publicado por error con salidas el 22/10/2026 | Eliminado y sustituido por la versión sin salidas; registrado en las decisiones |
| Los criterios de teselas, nube y sombra y periodo cambiaron el 23/10/2026 | Se repitió la extracción y se actualizaron notebooks, figuras y documentos. La selección pasó de 25, 29, 27 y 26 a 26, 33, 28 y 28 observaciones |
| Figuras de evolución temporal con el periodo anterior | Sustituidas el 23/10/2026 por figuras con el periodo correcto |
| Notebook 02 sin publicar por contener datos de las parcelas | Publicado sin salidas ni datos privados, con los datos en un archivo fuera del repositorio (23/10/2026) |
| El documento de alcance y el de evolución temporal conservaban el periodo anterior y una nota sobre las figuras | Actualizados el 23/10/2026 |

### Revisión con los tutores

Los cambios pedidos en la revisión con los tutores del 23/10/2026 (combinación
de teselas, criterio de nube y sombra de la parcela y periodo hasta el
01/11/2026) están en las decisiones del sprint, en el comentario de la issue #6 y
en el apartado 14 de `docs/preparacion-datos-simulador.md`.

### Trabajo completado

- Alcance y arquitectura documentados (issue #1): `docs/alcance-y-arquitectura.md`.
- Estructura de los CSV de Sentinel-2 analizada (issue #2):
  `docs/analisis-estructura-csv.md` y Parte 1 del notebook 01.
- Evolución temporal de NDVI, NDRE, NDMI y EVI representada (issue #3):
  `docs/evolucion-temporal-indices.md`, `docs/figuras/` y Parte 3 del notebook 01.
- Datos Sentinel-2 preparados para el simulador (issue #4): notebook 03,
  `docs/preparacion-datos-simulador.md`, `requirements.txt` y
  `notebooks/README.md`.
- NDRE incorporado al extractor (bandas B8A y B5).
- Cambios de la revisión con los tutores aplicados y comprobados en el notebook 03.
- Notebooks 01, 02 y 03 publicados, con el 02 y el 03 sin salidas, y datos
  privados de las parcelas fuera del repositorio.
- Plan de trabajo actualizado (`PLAN_TRABAJO.md`).
- Memoria del sprint redactada: `docs/memoria/requisitos-y-datos-sentinel-2.md`.

Los notebooks 01 a 03 existían antes del sprint. En el sprint se revisaron, se
ampliaron (NDRE, mosaico de teselas, criterio de nube y sombra, periodo), se
documentaron y se publicaron. No se presenta el trabajo previo como desarrollado
íntegramente en el sprint.

### Trabajo no completado

- Revisión bibliográfica sistemática: no se ha realizado.
- Confirmación de la campaña y de las fechas agronómicas de las parcelas.
- Repetición de la extracción para incorporar las imágenes posteriores al
  22/10/2026 hasta el 01/11/2026.
- Históricos de sensores y riego.
- NDWI y RECI, que usa el motor actual y no están en la extracción.
- Validación agronómica de los umbrales de la selección provisional.
- Motor de recomendación, modelos de aprendizaje automático y recomendaciones de
  riego: fuera del alcance del sprint.


### Incremento obtenido

Un conjunto de datos Sentinel-2 de cuatro parcelas, listo para un uso posterior en
el simulador. Cubre el periodo provisional del 01/04/2026 al 01/11/2026, con
imágenes hasta el 22/10/2026. Incluye seis índices (NDVI, NDRE, NDMI, MSI, EVI y
SAVI), una selección técnica que descarta una observación solo si más del 30 % de
la parcela es nube o sombra (26, 33, 28 y 28 observaciones seleccionadas de 42,
36, 41 y 37) y un resumen semanal sin interpolar. Las semanas sin dato conservan
valores ausentes y las semanas posteriores a la última imagen se marcan como aún
no disponibles. Los tres notebooks y la documentación están publicados sin datos
privados de las parcelas.

## Retrospectiva

### Qué ha funcionado correctamente

- La revisión con los tutores corrigió criterios importantes antes del cierre y
  los cambios quedaron documentados con las cifras de antes y después.
- Contrastar las cifras del notebook 03 con el notebook 01 y con los documentos
  permitió detectar y corregir incoherencias.
- Documentar cada decisión en `docs/` y en este seguimiento facilitó rehacer los
  resultados tras los cambios.
- Separar los datos privados del código (archivo privado y plantilla) permitió
  publicar el notebook 02 sin exponer las parcelas.

### Problemas encontrados

- El 22/10/2026 se publicó el notebook 03 con salidas que contenían datos de las
  parcelas. Se corrigió, pero las versiones previas permanecen en el historial.
- Los días 22 y 23 hubo varios ciclos de borrar y volver a subir notebooks y
  figuras (notebooks 01 y 03, figuras de evolución temporal) por versiones
  incorrectas o intermedias.
- Los cambios de criterio de la revisión con los tutores llegaron el último día del
  sprint. Obligaron a repetir la extracción y a regenerar notebooks, figuras y
  documentos, sin horas de margen.
- La decisión sobre la publicación del notebook 02 se resolvió el mismo día del
  cierre.

### Mejoras para el siguiente sprint

- Antes de subir un archivo a GitHub, comprobar una lista fija: salidas borradas,
  sin identificadores de proyecto ni credenciales, y sin municipios, variedades ni
  coordenadas. Subir cada versión una sola vez, tras revisarla.
- Mantener los datos privados fuera de los notebooks desde el inicio.
- Decidir si la revisión bibliográfica se planifica en el sprint 3 o se descarta.
- Repetir la extracción cuando haya imágenes hasta el fin del periodo, confirmar la
  campaña y las fechas agronómicas, e incorporar los históricos de sensores y
  riego.

## Evidencias

- Issues:
  - #1 — Documentar el alcance y la arquitectura inicial del sistema.
  - #2 — Analizar la estructura del CSV generado por Sentinel-2.
  - #3 — Representar la evolución temporal de los índices espectrales.
  - #4 — Preparar los datos Sentinel-2 para el simulador.
  - #5 — Configurar la gestión Scrum-Kanban del proyecto.
  - #6 — Revisar los entregables y documentar el cierre del sprint 2.

- Commits (selección; el historial completo está en GitHub):
  - Extracción: `89315a0` (NDRE en el notebook 03), `09d3f0b` (NDRE en el
    notebook 01), `3be06ea` (periodo hasta el 01/11/2026 y semanas aún no
    disponibles), `4972107` (notebook 01 con el periodo hasta el 01/11/2026).
  - Figuras: `cfcbeab` (NDRE), `8daf966` y `9445282` (periodo correcto).
  - Documentación: `eabbcdd` (preparación de datos), `8a606ee` y `83858de`
    (análisis de estructura), `7029dad` (evolución temporal), `577d3d9`,
    `1877032` y `c0d25b8` (preparación de datos), `a58aac8` (alcance), `9a92e69`
    (evolución temporal), `e1c2e7a` y `85aba52` (README de notebooks), `f23395e` y
    `acc4fed` (plan de trabajo), `cb58bfe` (memoria del sprint 2).
  - Datos privados: `7cf8299` (`.gitignore`) y `e6ae7fb` (notebook 02 y plantilla).
  - Dependencias: `cd82968` (`requirements.txt`).

- Notebooks:
  - `notebooks/01_Exploracion_inicial_datos_sentinel-2.ipynb` (Partes 1 y 3).
  - `notebooks/02_preparacion_parcelas_reales.ipynb` (sin salidas ni datos
    privados).
  - `notebooks/03_extraccion_sentinel2_parcelas_reales.ipynb` (sin salidas).
  - `notebooks/datos_parcelas_privados_ejemplo.py` (plantilla con valores
    ficticios).
  - `notebooks/README.md`.

- Resultados:
  - `docs/figuras/` (figuras de evolución temporal, issues #3 y #4, incluida la
    de NDRE).

- Documentación:
  - `PLAN_TRABAJO.md`.
  - `docs/gestion-agil.md`.
  - `docs/memoria/gestion-del-proyecto.md`.
  - `docs/memoria/requisitos-y-datos-sentinel-2.md`.
  - `docs/alcance-y-arquitectura.md`.
  - `docs/analisis-estructura-csv.md`.
  - `docs/evolucion-temporal-indices.md`.
  - `docs/preparacion-datos-simulador.md`.
  - `requirements.txt`.
  - Este documento de seguimiento.
