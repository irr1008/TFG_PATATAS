# Seguimiento del sprint 3

## Información del sprint

- Sprint: 3 — Variables del balance hídrico y datos complementarios.
- Objetivo: definir las variables, unidades y fuentes del balance hídrico a
  partir del motor de referencia y del documento del tutor, adquirir y preparar
  los datos no satelitales y completar la extracción Sentinel-2 hasta el
  01/11/2026.
- Fecha de inicio: 26/10/2026.
- Fecha objetivo: 06/11/2026.
- Responsable: irr1008.
- Milestone asociado: M2 - Definir variables y unidades del balance hídrico.
- Estado del sprint: en curso desde el 26/10/2026.
  
### Adaptación de la planificación inicial

La planificación general denominaba esta iteración «Adquisición y preparación
de datos». Los datos Sentinel-2 se consolidaron en el sprint 2, por lo que el
alcance se adapta: se definen las variables y unidades del balance hídrico, se
evalúan y preparan los datos no satelitales (sondas y meteorología), se
solicitan a los tutores los datos pendientes y se completa la extracción del
periodo.

La duración es de dos semanas. La revisión bibliográfica pendiente del
sprint 2 se incorpora como tarea acotada a los parámetros del balance hídrico;
no equivale a una revisión sistemática.

## Capacidad y estimación

- Unidad de estimación: horas de trabajo.
- Capacidad de referencia: cuatro horas por jornada, de lunes a viernes.
- Jornadas planificadas: del 26 al 30 de octubre y del 2 al 6 de noviembre de
  2026.
- Capacidad de referencia: 40 horas.
- Esfuerzo previsto en las nueve tareas: 36 horas.
- Margen no asignado: 4 horas (jueves 05/11/2026).

## Tareas seleccionadas

| Issue | Tarea | Prioridad | Estimación (h) | Fecha de inicio | Fecha objetivo | Estado al planificar |
|---|---|---|---:|---|---|---|
| #7 | Analizar el motor de referencia Agrobioma v14 | Alta | 4 | 26/10/2026 | 27/10/2026 | Por hacer |
| #8 | Definir las variables y unidades del balance hídrico | Alta | 5 | 27/10/2026 | 28/10/2026 | Por hacer |
| #9 | Analizar el histórico de sondas de humedad del suelo | Alta | 4 | 29/10/2026 | 29/10/2026 | Por hacer |
| #10 | Evaluar las fuentes de meteorología y radiación para la ETo | Alta | 4 | 30/10/2026 | 30/10/2026 | Por hacer |
| #11 | Preparar la meteorología diaria de las cuatro parcelas | Media | 4 | 02/11/2026 | 02/11/2026 | Por hacer |
| #12 | Repetir la extracción Sentinel-2 hasta el 01/11/2026 | Alta | 5 | 03/11/2026 | 04/11/2026 | Por hacer |
| #13 | Solicitar a los tutores los datos y criterios pendientes | Alta | 3 | 26/10/2026 | 30/10/2026 | Por hacer |
| #14 | Realizar una revisión bibliográfica focalizada de parámetros | Media | 3 | 04/11/2026 | 04/11/2026 | Por hacer |
| #15 | Revisar los entregables y documentar el cierre del sprint 3 | Alta | 4 | 06/11/2026 | 06/11/2026 | Por hacer |

Total estimado: 36 horas.

Los estados actuales se mantienen en GitHub Projects. Esta tabla conserva la
situación inicial de la planificación. Las fechas del tablero son fechas
planificadas; la ejecución real, los retrasos y las desviaciones se registran en
las issues y en las secciones de revisión y evidencias.

### Distribución de referencia

| Jornada | Trabajo previsto | Horas |
|---|---|---:|
| Lunes 26/10 | #13 (3 h) y comienzo de #7 (1 h) | 4 |
| Martes 27/10 | #7 (3 h) y comienzo de #8 (1 h) | 4 |
| Miércoles 28/10 | Continuación de #8 | 4 |
| Jueves 29/10 | #9 | 4 |
| Viernes 30/10 | #10 y revisión intermedia con los tutores | 4 |
| Lunes 02/11 | #11 | 4 |
| Martes 03/11 | #12 | 4 |
| Miércoles 04/11 | Fin de #12 (1 h) y #14 (3 h) | 4 |
| Jueves 05/11 | Margen no asignado | 4 |
| Viernes 06/11 | #15 | 4 |

Las tareas que comparten jornada no se consideran paralelas: se mantiene el
límite de una tarea principal en estado En progreso.

## Trabajo previo disponible

- Datos Sentinel-2 de las cuatro parcelas, preparados en el sprint 2.
- Motor de decisión de referencia (Agrobioma v14) y documento de
  especificación técnica del motor mejorado, proporcionados por el profesorado.
- Artículo de Saxton y Rawls (2006) sobre estimación de las características
  hídricas del suelo.
- Histórico de sondas, proporcionado por el profesorado.

Este material es el punto de partida de las issues. Su análisis y documentación
se registran con las fechas reales de su elaboración.

## Resultado esperado y criterios de comprobación

### Issue #7: motor de referencia

- Tabla del motor v14 frente a la especificación del tutor.
- Ambigüedades registradas con una pregunta concreta, incluida la fórmula de AFD.
- Sin código del motor ni datos de explotaciones en el repositorio.

### Issue #8: variables y unidades

- Cada variable con símbolo, unidad, rango y fuente.
- Discrepancias entre fórmulas registradas, no corregidas en silencio.
- Variables sin dato marcadas como pendientes.

### Issue #9: histórico de sondas

- Resumen de estructura y calidad por sonda.
- Unidades confirmadas o marcadas como pendientes.
- Notebook sin salidas y sin datos de explotaciones.

### Issue #10: fuentes meteorológicas

- Tabla comparativa de AEMET OpenData, NASA POWER y Open-Meteo.
- Decisión justificada o pendiente de los tutores.
- Sin claves de API ni coordenadas en el repositorio.

### Issue #11: meteorología diaria

- Tabla diaria por parcela con unidades documentadas y variables derivadas marcadas.
- Datos ausentes sin interpolar.
- Notebook sin salidas, coordenadas ni claves.

### Issue #12: extracción hasta el 01/11/2026

- Tabla de cifras antes y después de la nueva extracción.
- Documentos sin cifras de la extracción anterior.
- Notebooks sin datos privados.

### Issue #13: datos y criterios de los tutores

- Fecha de envío de la solicitud registrada.
- Respuestas recibidas y no recibidas registradas, sin atribuir validaciones que
  no consten.
- Bloqueos identificados.

### Issue #14: revisión bibliográfica focalizada

- Cada referencia con autor, año y enlace.
- Cada rango de #8 con su respaldo o marcado como pendiente.
- No se presenta como revisión sistemática.

### Issue #15: revisión y cierre

- Revisión, retrospectiva y evidencias completadas en este documento.
- Trabajo no terminado identificado y no presentado como completado.

## Límites del sprint

- No se implementa el balance hídrico, el simulador ni el motor de recomendación.
- No se entrenan modelos de aprendizaje automático ni se emiten recomendaciones
  de riego.
- El periodo de extracción sigue siendo provisional y no se confirma el cultivo.
- No se interpolan los datos ausentes.
- Las coordenadas, el municipio y la variedad de las parcelas permanecen fuera
  del repositorio.

## Impedimentos

### Limitaciones conocidas al inicio

- Faltan por confirmar la campaña y las fechas agronómicas de las parcelas.
- La textura del suelo, los riegos aplicados y la ubicación de las sondas están
  pendientes de los tutores.
- La estación meteorológica del motor v14 no proporciona radiación neta; hay que
  decidir cómo obtenerla o estimarla.
- El documento del tutor presenta el agua fácilmente disponible con (1 − MAD) y
  el umbral de recarga con MAD; se debe aclarar.
- La extracción hasta el 01/11/2026 solo puede repetirse a partir del 02/11/2026.
- El margen de horas es de 4 horas.

Si alguna limitación impide continuar una actividad concreta, se registra en la
issue afectada y se utiliza el estado Bloqueado.

### Limitaciones que siguen abiertas

- Sin registrar.

### Decisiones durante el sprint

- 24/10/2026: planificación del sprint con duración de dos semanas, nueve
  tareas, 36 horas y 4 horas de margen. La revisión bibliográfica se incorpora
  de forma acotada. Las tareas de memoria se identifican con la etiqueta
  «Documentación».
- 26/10/2026: el proyecto utilizará una única sonda de humedad a 25 cm de profundidad.
  La matriz de pesos por profundidad de la especificación no se aplica y la humedad del
  perfil es la lectura de esa sonda. Se contrastará con los tutores en la revisión
  intermedia del 30/10.

## Medidas aplicadas desde el sprint 2

- Este documento se crea al empezar el sprint y se actualiza durante su ejecución.
- Se reserva un margen de horas.
- La confirmación de criterios con los tutores se solicita al inicio y se revisa a
  mitad del sprint (issue #13).
- Antes de subir un archivo a GitHub se comprueba que no tiene salidas, identificadores,
  coordenadas, municipios ni variedades.

## Revisión del sprint

Pendiente de realizar durante la issue #15, al finalizar la iteración.

### Trabajo completado

- Pendiente de registrar con sus evidencias.

### Trabajo no completado

- Pendiente de registrar.

### Incremento obtenido

- Pendiente de registrar.

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
  - #7 — Analizar el motor de referencia Agrobioma v14.
  - #8 — Definir las variables y unidades del balance hídrico.
  - #9 — Analizar el histórico de sondas de humedad del suelo.
  - #10 — Evaluar las fuentes de meteorología y radiación para la ETo.
  - #11 — Preparar la meteorología diaria de las cuatro parcelas.
  - #12 — Repetir la extracción Sentinel-2 hasta el 01/11/2026.
  - #13 — Solicitar a los tutores los datos y criterios pendientes.
  - #14 — Realizar una revisión bibliográfica focalizada de parámetros.
  - #15 — Revisar los entregables y documentar el cierre del sprint 3.

- Commits:
  - Pendiente de registrar al cierre del sprint.

- Notebooks:
  - Pendiente de registrar.

- Resultados:
  - Pendiente de registrar.

- Documentación:
  - `docs/analisis-motor-referencia.md`.
  - `docs/variables-balance-hidrico.md` (prevista).
  - `docs/analisis-historico-sondas.md` (prevista).
  - `docs/fuentes-meteorologicas.md` (prevista).
  - `docs/solicitud-datos-tutores.md`.
  - `docs/revision-bibliografica.md` (prevista).
  - Este documento de seguimiento.
