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
- Estado del sprint: en curso.

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
| #4 | Preparar los datos Sentinel-2 para el simulador | Alta | 4 | 20/10/2026 | 21/10/2026 | Por hacer |
| #3 | Representar la evolución temporal de los índices espectrales | Media | 5 | 21/10/2026 | 22/10/2026 | Por hacer |
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
| Martes 20/10 | Issue #2 y comienzo de la issue #4 | 4 |
| Miércoles 21/10 | Continuación de #4 y comienzo de #3 | 4 |
| Jueves 22/10 | Continuación de #3 | 4 |
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
- Debe resolverse el alcance de NDRE en la issue #3.
- La planificación no dispone de margen libre de horas.

Estas limitaciones no bloquean automáticamente todas las tareas.
Si alguna impide continuar una actividad concreta, se registrará en la
issue afectada y se utilizará el estado Bloqueado.

## Revisión del sprint

Pendiente de realizar durante la issue #6, al finalizar la iteración.

### Trabajo completado

- Pendiente de registrar con sus evidencias.
- No se contabiliza automáticamente el trabajo previo como trabajo
  terminado durante el sprint.

### Trabajo no completado

### Incremento obtenido


## Retrospectiva

Pendiente de realizar al finalizar la iteración.

### Qué ha funcionado correctamente

- Pendiente de valorar.

### Problemas encontrados

- Pendiente de registrar durante la ejecución.

### Mejoras para el siguiente sprint

- Pendiente de acordar en la retrospectiva.

## Evidencias

- Issues:
  - #1 — Documentar el alcance y la arquitectura inicial del sistema.
  - #2 — Analizar la estructura del CSV generado por Sentinel-2.
  - #3 — Representar la evolución temporal de los índices espectrales.
  - #4 — Preparar los datos Sentinel-2 para el simulador.
  - #6 — Revisar los entregables y documentar el cierre del sprint 2.

- Commits:

- Notebooks:
 

- Resultados:
 
- Documentación:
  - `docs/gestion-agil.md`.
  - `docs/memoria/gestion-del-proyecto.md`.
  - Este documento de seguimiento.
  - Los documentos de alcance y análisis que se actualicen en el sprint.
