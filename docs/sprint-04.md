# Seguimiento del sprint 4

## Información del sprint

- Sprint: 4 — Núcleo hidráulico verificable.
- Objetivo: implementar un núcleo hidráulico por capas, independiente de
  Agrobioma v14, y verificar su conservación de masa y su comportamiento
  temporal con datos sintéticos.
- Fecha de inicio planificada: 09/11/2026.
- Fecha objetivo: 27/11/2026.
- Responsable: irr1008.
- Milestone asociado: M3 - Implementar y verificar el núcleo hidráulico.
- Estado: en ejecución; el detalle de ejecución se registra en las issues
  y los estados actuales se mantienen en GitHub Projects.

## Contexto

El sprint 3 se cerró anticipadamente tras el cambio de enfoque de la reunión
del 06/11/2026. Los análisis anteriores se conservan como antecedentes y se
reutilizan únicamente cuando resultan pertinentes.

La especificación y el diseño inicial están publicados. Este sprint no parte
de una implementación del núcleo ni de parámetros calibrados para las parcelas.

## Capacidad y estimación

- Unidad de estimación: horas.
- Capacidad de referencia: 4 horas por jornada, de lunes a viernes.
- Jornadas de referencia: del 09 al 27/11/2026.
- Capacidad de referencia: 60 horas.
- Estimación de las seis tareas: 52 horas.
- Margen no asignado: 8 horas, inicialmente el 25 y el 26/11.
- Las estimaciones han sido fijadas y se mantienen como
  previsiones, no como dedicación real.
- La disponibilidad efectiva y cualquier desviación se registran durante
  la ejecución.

## Tareas seleccionadas

| Issue | Tarea | Estimación (h) | Inicio previsto | Fin previsto | Prioridad |
|---|---|---:|---|---|---|
| #17 | Justificar las leyes y limitaciones del núcleo | 4 | 09/11/2026 | 09/11/2026 | Alta |
| #18 | Configuración, estados y validaciones | 8 | 10/11/2026 | 11/11/2026 | Alta |
| #19 | Paso hidráulico y pruebas deterministas | 16 | 12/11/2026 | 17/11/2026 | Alta |
| #20 | Ejecutor temporal, conservación y convergencia | 12 | 18/11/2026 | 20/11/2026 | Alta |
| #21 | Demostración sintética reproducible | 8 | 23/11/2026 | 24/11/2026 | Media |
| #22 | Revisión y cierre del sprint | 4 | 27/11/2026 | 27/11/2026 | Alta |

Total estimado: 52 horas.

Las fechas son de planificación. Los estados actuales se mantienen en
GitHub Projects y la ejecución real se registra en las issues.

## Dependencias y orden

- #17: especificación y diseño publicados.
- #18: conclusiones de #17.
- #19: configuración de #18 y leyes revisadas en #17.
- #20: paso hidráulico de #19.
- #21: ejecutor e informe de #20.
- #22: revisión del estado y evidencias de #17 a #21, incluidas las tareas
  que no hayan terminado.

Se mantiene una sola tarea principal en estado En progreso.

## Base de diseño

- `docs/especificación-modelo-físico.md`, versión 0.1.
- `docs/diseño-nucleo-hidraulico.md`, versión 0.2.
- `docs/registro-reunion-06-11-2026.md`.

Un cambio material de las leyes, los parámetros de prueba o los criterios
de aceptación se justifica y documenta antes de implementarlo.

## Incremento esperado

- Núcleo Python independiente de Drive y de APIs.
- Configuración de perfiles con una o más capas.
- Actualización de estados mediante flujos explícitos.
- Pruebas deterministas con resultados esperados.
- Ejecutor temporal y balances por paso y globales.
- Estudio de refinamiento temporal y comparación analítica.
- Notebook que importe el núcleo y demuestre los escenarios sintéticos.
- Instrucciones reproducibles y documentación de limitaciones.

## Criterios de comprobación

### #17 — Justificación

- Referencias identificables y derivación de la ley exponencial.
- Separación entre fundamento físico, cierre simplificado y elección
  del experimento.
- Límites del modelo explícitos.

### #18 — Configuración

- Conversiones y validaciones probadas.
- Parámetros o estados inválidos rechazados sin corrección silenciosa.
- Pruebas ejecutables con instrucciones documentadas.

### #19 — Paso hidráulico

- Casos deterministas A a I del diseño.
- Transferencias conservativas y límites de almacenamiento respetados.
- Sin modificación silenciosa de los objetos de entrada.
- Balance por paso dentro de tolerancia.

### #20 — Ejecución temporal

- Conservación de aportes y tratamiento explícito de intervalos.
- Residual global calculado con estados extremos y flujos acumulados.
- Escenarios 11.1 y 11.2 del diseño evaluados.
- Errores y dependencia del paso temporal documentados.
- Un fallo se investiga; no se cambia el umbral solo para aprobarlo.

### #21 — Demostración

- Notebook que importe el núcleo, sin duplicar sus ecuaciones.
- Ejecución reproducible sin datos privados ni claves.
- Parámetros y resultados identificados como sintéticos.
- Notebook publicado sin salidas.

### #22 — Cierre

- Coherencia revisada entre diseño, código, pruebas e informe.
- Trabajo terminado, parcial y pendiente diferenciado.
- Revisión, retrospectiva, memoria y plan actualizados.

## Fuera de alcance

- Calibración y validación con parcelas reales.
- Descarga de meteorología y tratamiento de observaciones de campo.
- Autocalibración de los parámetros del suelo.
- Modelo térmico.
- Integración de Sentinel-2.
- Recomendaciones de riego y despliegue operativo.

La #16 continúa como auditoría de datos reales en el backlog. Las limitaciones
de esos datos no bloquean las pruebas sintéticas de este sprint.

## Riesgos y respuesta prevista

- Error de unidades: conversiones explícitas y pruebas.
- Error de conservación: balances independientes y tolerancias documentadas.
- Dependencia excesiva del paso: refinamiento temporal y referencia analítica.
- Simplificación física inadecuada: registrar límites y revisar el diseño,
  sin presentar verificación numérica como validación real.
- Desviación de esfuerzo: usar el margen, registrar el motivo y replanificar
  sin reducir silenciosamente los criterios.

## Seguimiento de ejecución

- 09/11/2026: preparación de la planificación del sprint y configuración
  de fechas, estimaciones, prioridades y dependencias en el tablero.
  Esta preparación precedió al inicio efectivo de la #17, cuya revisión documental
  quedó completada el 09/11/2026.
  
- 09/11/2026: completada la revisión documental de la #17.
  Se publica la justificación de las leyes, sus hipótesis y limitaciones.
  Se considera el diseño v0.2 suficientemente explícito para iniciar
  la implementación y la verificación sintética, sin declarar
  validación con parcelas.
  
- 10/11/2026: primer bloque de la #18 completado.
  Configuración del perfil, opciones de procesos y validaciones básicas.
  Ejecución en Colab: 43 pruebas superadas sobre el commit c541560.
  
- 11/11/2026: completada la implementación prevista en la #18 y realizada
  la comprobación final de configuración, conversiones, estados y entradas.
  El ejemplo de uso se ejecuta correctamente.
  Suite completa: 186 pruebas superadas, código de salida 0,
  sobre el commit d24be2f, con Python 3.13.18 y pytest 8.4.2.
  El cierre administrativo y la dedicación real se registran en la issue.

- 12/11/2026: completado el primer bloque de la #19.
  Se implementan el drenaje potencial, el drenaje inferior y las
  transferencias internas de abajo arriba, con diagnóstico de balance.
  Se comprueban los casos E, F y G de esta fase, la capacidad receptora,
  los procesos desactivados y perfiles de una y tres capas.
  Ejecución en Colab sobre 721ab41: 243 pruebas superadas,
  código de salida 0.
  La #19 permanece en progreso; faltan infiltración, extracción
  e integración del paso completo.

- 13/11/2026: implementada y comprobada la fase de infiltración
  y salida superficial de la #19.
  Se verifica la actualización de la capa superior, los casos B, C y D
  de esta fase, el balance y una composición drenaje → infiltración.
  Ejecución en Colab sobre e18b418: 287 pruebas superadas,
  código de salida 0.
  Quedan pendientes la extracción y la integración y comprobación
  del paso hidráulico completo.

El avance actual incluye drenaje inferior, transferencias internas
e infiltración y salida superficial.
Todavía no incluye la extracción ni una función de paso hidráulico
completo con su balance independiente, ni la ejecución de series temporales.
No constituye calibración ni validación con parcelas.

## Revisión

Pendiente de realizar en #22.

### Trabajo completado

- Pendiente de registrar con evidencias.

### Trabajo parcial o no completado

- Pendiente de registrar.

### Incremento obtenido

- Pendiente de evaluar.

## Retrospectiva

Pendiente de realizar en #22.

### Qué ha funcionado

- Pendiente de valorar.

### Problemas encontrados

- Pendiente de registrar.

### Mejoras

- Pendiente de acordar.

## Evidencias

- Issues: #17, #18, #19, #20, #21 y #22.
  El detalle de ejecución y dedicación real se registra en cada issue.

- Justificación: `docs/justificacion-nucleo-hidraulico.md`.
  Revisión documental completada en la #17.

- Código de configuración, conversiones, estados y entradas:
  `src/modelo_fisico/`.

- Pruebas automatizadas: `tests/`.
  Última comprobación de la #18: 186 pruebas superadas sobre d24be2f.

- Guía de instalación, uso, unidades y tolerancias:
  `docs/uso-nucleo-hidraulico.md`, enlazada desde el README.

- Commits de referencia:
  - c541560: configuración y pruebas básicas.
  - d24be2f: versión utilizada en la comprobación final de la #18.

- Evidencia de ejecución de la #18:
  notebook de trabajo de Colab conservado con sus salidas.
  No sustituye a la demostración prevista en la #21.

- Verificación del núcleo:
  `docs/verificacion-nucleo-hidraulico.md` (prevista).

- Demostración:
  `notebooks/05_demostracion_nucleo_hidraulico.ipynb` (prevista).

- Memoria: pendiente de actualizar al cierre.
