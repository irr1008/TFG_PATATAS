# Solicitud de datos y criterios a los tutores

Issue #13 · Sprint 3

## Información

- Fecha de envío de la primera solicitud: 26/10/2026.
- Canal: outlook.
- Segunda solicitud (dudas técnicas del análisis del motor de referencia): 27/10/2026, por outlook.
- Tercera solicitud (preguntas sobre el histórico de sondas): 29/10/2026, por outlook.
- Revisión intermedia: celebrada el 06/11/2026, tras aplazarse desde el 30/10/2026. Se acuerda cambiar el enfoque hacia un modelo físico nuevo, independiente de Agrobioma v14. Las peticiones anteriores no se respondieron punto por punto.
- Registro de la reunión: `docs/registro-reunion-06-11-2026.md`.
- Especificación del nuevo enfoque: `docs/especificación-modelo-físico.md`.
  
## Peticiones

| Nº | Petición | Motivo | Issue que depende | Estado | Fecha de respuesta |
|---|---|---|---|---|---|
| 1 | Campaña y fechas de siembra y emergencia | Días tras emergencia y confirmación del cultivo | #8, #12 | Pendiente | |
| 2 | Textura del suelo y materia orgánica | Saxton y Rawls | #8 | Pendiente | |
| 3 | CC y PMP de la ficha y su unidad | Hidrofísica del suelo | #8 | Pendiente | |
| 4 | Registro de riegos | Balance hídrico | #8, #9 | Pendiente | |
| 5 | Sonda única a 25 cm: identificador y acceso al histórico | Análisis del histórico | #9 | Pendiente | |
| 6 | MAD y parámetros a y b de Kc | Rangos de variables | #8, #14 | Pendiente | |
| 7 | Autorización para publicar constantes y datos | Publicación en el repositorio | #7, #8 | Pendiente | |
| 8 | Criterios técnicos del motor | Definiciones de variables y fórmulas | #8, #14 | Pendiente | |
| 9 | Parcela a la que corresponde cada sonda | Asociar el histórico a cada parcela | #9, #11 | Pendiente | |
| 10 | Causa de los huecos simultáneos del histórico (25 al 30/05 y 01 al 05/06) y posibles lecturas recuperables | Fiabilidad y cobertura del histórico | #9 | Pendiente | |
| 11 | Significado de las lecturas 0,0 del 29/04 | Decidir su exclusión | #9 | Pendiente | |
| 12 | Existencia de lecturas anteriores al 29/04 o posteriores al 11/09 | Cobertura del periodo del estudio | #9, #12 | Pendiente | |
| 13 | Confirmación del identificador de sonda fusionado | Validar la fusión de identificadores | #9 | Pendiente | |

## Revisión de las peticiones tras la reunión del 06/11/2026

Revisión realizada el 07/11/2026.

Las peticiones anteriores no se contestaron punto por punto en la reunión. Se conserva su tabla como registro de las solicitudes originales. La clasificación siguiente indica su utilidad para el nuevo modelo, no una respuesta de los tutores.

Ninguna de estas peticiones impide implementar y verificar el núcleo hidráulico con parámetros sintéticos. Algunas sí condicionan su posterior aplicación, calibración y evaluación con datos reales.

| Nº original | Situación en el nuevo enfoque | Información disponible y acción pendiente |
|---|---|---|
| 1 | Vigente para la aplicación al cultivo y la evaluación | Las fichas contienen referencias de campaña y cultivo, pero no proporcionan de forma suficiente las fechas de siembra y emergencia. Verificar su correspondencia con el periodo simulado. |
| 2 | Parcialmente cubierta por documentación; sigue vigente | Los PDF incluyen clase textural y materia orgánica. No contienen porcentajes completos de arena, limo y arcilla ni porosidad medida. Obtener los análisis completos o documentar qué parámetros se estimarán y con qué incertidumbre. |
| 3 | Parcialmente cubierta por documentación; sigue vigente | Las fichas contienen valores teóricos y algunas estimaciones automáticas de CC. Registrar su procedencia, unidad y método. No tratarlos como mediciones independientes ni como referencia validada del nuevo modelo. |
| 4 | Vigente y prioritaria para evaluar con datos reales | Se necesitan eventos de riego aplicado con fecha, duración o intervalo y lámina o volumen con su área de referencia. Las recomendaciones enviadas a los agricultores no demuestran su ejecución. |
| 5 | Reformulada; parcialmente cubierta | Ya se dispone de un histórico y de identificadores en las fichas. Sustituir la hipótesis universal de 25 cm por la comprobación de profundidad, instalación y periodo de validez de cada sonda. |
| 6 | Diferida y pendiente de reformulación | MAD y la relación Kc–NDVI no son requisitos del primer núcleo hidráulico. Revisar su necesidad cuando se definan la transpiración, el cultivo y una posible recomendación de riego. No se consideran confirmados. |
| 7 | Vigente | Sigue pendiente aclarar los permisos de uso y publicación de datos, documentos y resultados derivados. Mientras tanto se mantienen privados los originales y la información identificativa. |
| 8 | Sustituida como base de implementación | Las dudas específicas sobre las reglas y fórmulas de Agrobioma v14 se conservan como antecedentes. Los criterios del nuevo modelo se definirán en su especificación, sin dar por resueltas las preguntas anteriores. |
| 9 | Parcialmente cubierta por documentación; sigue vigente la comprobación | Las fichas incluyen la asociación entre parcela e identificador de sonda. Conciliarla con los identificadores y alias del histórico, incluidas posibles variaciones de instalación. Mantener la correspondencia en el inventario privado. |
| 10 | Vigente para la calidad y cobertura de los datos | Sigue pendiente conocer la causa de los huecos y si existen lecturas recuperables. No rellenarlos ni atribuirles una causa confirmada sin evidencia. |
| 11 | Vigente para la interpretación de datos | Sigue pendiente aclarar el significado de los valores 0,0. Mantener su marcado de calidad sin afirmar que su causa está confirmada. |
| 12 | Vigente | Los PDF muestran referencias a registros posteriores al histórico analizado, pero no aportan una serie numérica completa. Comprobar si existe una exportación adicional y cuál es su cobertura efectiva. |
| 13 | Vigente para la trazabilidad de la limpieza | La fusión se realizó por la corrección comunicada por el estudiante. La confirmación solicitada al personal de las sondas sigue pendiente; conservar el origen y la justificación de la transformación. |

La disponibilidad de información en los PDF no se registra como respuesta de los tutores a las solicitudes. Las fechas de respuesta solo se completarán cuando exista una contestación o confirmación atribuible a su fuente.

## Registro de comunicaciones

| Fecha | Acción | Resultado |
|---|---|---|
| 26/10/2026 | Envío de la primera solicitud | A la espera de respuesta |
| 27/10/2026 | Envío de la segunda solicitud de criterio técnico | A la espera de respuesta |
| 29/10/2026 | Envío de la tercera solicitud sobre el histórico de sondas (reitera la petición 4) | A la espera de respuesta |
| 30/10/2026 | Los tutores comunican el aplazamiento de la revisión intermedia | Nueva fecha propuesta: 06/11/2026 |
| 06/11/2026 | Celebración de la revisión con los tutores | Cambio de enfoque: iniciar un modelo físico nuevo, independiente de Agrobioma v14. Las solicitudes no se respondieron punto por punto. Registro redactado el 07/11/2026. |

## Bloqueos

- La reunión del 06/11/2026 ya se celebró; su aplazamiento deja de ser un bloqueo.
- La profundidad y el periodo de instalación de cada sonda deben conciliarse antes de comparar la simulación con sus lecturas.
- La calibración y la evaluación con datos reales dependen de disponer de entradas suficientemente conocidas, especialmente del riego aplicado, y de documentar la procedencia de los parámetros del suelo.
- Los permisos de publicación de datos y resultados identificables siguen pendientes de aclaración.
- Estas limitaciones no bloquean el diseño, la implementación ni las pruebas del núcleo hidráulico con datos sintéticos. No se presentan esas pruebas como validación con parcelas reales.

## Decisiones confirmadas

- 06/11/2026: según el registro de la reunión, los tutores recomiendan iniciar un modelo físico nuevo, sin seguir Agrobioma v14 como base de implementación.
- Se reutilizará el trabajo que resulte pertinente y se conservará el resto como antecedente, sin continuar necesariamente su desarrollo.
- Las solicitudes anteriores no se contestaron punto por punto. No se consideran validadas por esta reunión las fórmulas, constantes ni decisiones del enfoque anterior.
- Las ecuaciones, la geometría y los parámetros del nuevo núcleo son propuestas técnicas documentadas; no se presentan como decisiones aprobadas por los tutores.
