# Gestión y planificación del proyecto

## 1. Justificación de la metodología

El desarrollo de un sistema inteligente de recomendación de riego para el
cultivo de patata requiere coordinar actividades de análisis de datos,
modelado físico, simulación, aprendizaje automático, aprendizaje por refuerzo,
evaluación y documentación.

La disponibilidad y calidad de los datos, así como la complejidad de los
modelos, introducen incertidumbre en el desarrollo. Por ello, se considera
necesario revisar periódicamente el trabajo, comprobar los resultados
intermedios y adaptar la planificación cuando aparezcan nuevas necesidades.

Se acordó con el profesor utilizar una adaptación individual de Scrum,
complementada con elementos visuales de Kanban.

La gestión se centraliza en GitHub mediante Issues, Milestones y Projects.
Este enfoque permite mantener relacionadas la planificación, las tareas,
la documentación y las evidencias del desarrollo.

## 2. Adaptación de Scrum al entorno individual

El TFG es desarrollado por un único estudiante, con supervisión académica del
profesor. Por este motivo, la metodología no se presenta como una aplicación
íntegra de Scrum con un equipo y responsabilidades separadas.

El estudiante asume la organización del trabajo, la implementación, el
mantenimiento del backlog y la comprobación inicial de los resultados.

El profesor participa en la revisión del alcance, la orientación académica y
la validación de las decisiones relevantes. Su participación no se equipara
automáticamente a una responsabilidad formal de Scrum.

La adaptación mantiene los siguientes elementos:

- Un objetivo general del proyecto.
- Un Product Backlog priorizado.
- Un objetivo definido para cada Sprint.
- Un Sprint Backlog con el trabajo seleccionado.
- Periodos de trabajo delimitados.
- Revisión de los resultados.
- Retrospectiva del proceso.
- Registro de impedimentos y decisiones.

El propósito de esta adaptación es mantener un proceso de trabajo estructurado
y revisable sin reproducir artificialmente la organización de un equipo
multidisciplinar.

## 3. Organización de los Sprints

La planificación inicial se organiza en nueve Sprints principales (que no necesariamente definitivos):

1. Gestión ágil y planificación.
2. Requisitos y revisión bibliográfica.
3. Adquisición y preparación de datos.
4. Modelo físico.
5. Simulador del cultivo.
6. Machine Learning.
7. Aprendizaje por refuerzo.
8. Interfaz de usuario.
9. Evaluación.

Los Sprints tienen una duración prevista de entre una y tres semanas, según
el objetivo y la complejidad del trabajo seleccionado.

La variación de duración entre iteraciones constituye una adaptación acordada
para este TFG. La duración se establece antes del comienzo de cada Sprint y
no se modifica durante su ejecución para ocultar retrasos.

Cuando una tarea no se completa, se registra su situación y se vuelve a
planificar. El cierre del periodo de trabajo no implica necesariamente que
todas las tareas seleccionadas hayan terminado.

Los nombres de los Sprints identifican su objetivo predominante. No implican
que los resultados de una disciplina no puedan revisarse en iteraciones
posteriores.

El primer Sprint se orienta a preparar el entorno de gestión. Su resultado
principal es organizativo y documental, no una nueva funcionalidad del
simulador.

## 4. Product Backlog y Sprint Backlog

El Product Backlog recoge el trabajo identificado para alcanzar los objetivos
del TFG. Se mantiene en GitHub Projects y sus elementos se representan
principalmente mediante issues del repositorio.

Cada issue incluye:

- Objetivo.
- Actividades previstas.
- Criterios de aceptación.
- Información o evidencias necesarias para comprobar su resultado.

Los campos del proyecto permiten completar la información con:

- Estado.
- Prioridad.
- Tipo de trabajo.
- Estimación en horas.
- Sprint.
- Fecha de inicio.
- Fecha objetivo.
- Milestone.

La prioridad se revisa según las dependencias técnicas, la disponibilidad de
datos y el valor del resultado para el proyecto.

El Sprint Backlog reúne las tareas seleccionadas para la iteración activa.
La selección se realiza teniendo en cuenta el objetivo del Sprint y la
capacidad disponible del estudiante.

La asignación de una tarea a un Sprint futuro es provisional y puede revisarse
antes de su comienzo.

## 5. Visualización del trabajo mediante Kanban

El seguimiento operativo se realiza mediante un tablero Kanban con los
siguientes estados:

| Estado | Significado |
|---|---|
| Backlog | Trabajo identificado pendiente de selección. |
| Por hacer | Trabajo seleccionado para el Sprint. |
| En progreso | Tarea que se está ejecutando. |
| En revisión | Trabajo pendiente de comprobación. |
| Bloqueado | Tarea detenida por un impedimento. |
| Hecho | Trabajo completado y verificado. |

Se establece un límite de una tarea principal de trabajo manual en estado
«En progreso».

Esta política pretende reducir la dispersión y los cambios de contexto en
un proyecto individual. El límite se aplica como regla de trabajo, sin
presuponer que la herramienta impida automáticamente superarlo.

El movimiento de una tarjeta refleja el estado real de la tarea. Una tarea
no pasa a «Hecho» únicamente porque se haya escrito el código: también debe
haberse comprobado su resultado y cumplido sus criterios de aceptación.

## 6. Herramientas de gestión

La gestión se centraliza en el repositorio `irr1008/TFG_PATATAS` y en el
GitHub Project asociado.

### 6.1. GitHub Issues

Las issues representan unidades de trabajo y permiten registrar actividades,
criterios de aceptación, dudas, impedimentos y resultados.

Los comentarios se utilizan para documentar avances y decisiones relevantes.
Las listas de verificación reflejan las actividades realizadas.

### 6.2. GitHub Milestones

Los milestones agrupan tareas relacionadas con una fase o un objetivo
principal.

Su función es diferente de la de los Sprints: un milestone representa un
objetivo o entregable, mientras que un Sprint representa un periodo de
trabajo. Por tanto, no se exige una correspondencia uno a uno entre ambos.

### 6.3. GitHub Projects

GitHub Projects permite consultar el mismo conjunto de elementos mediante
distintas vistas:

- Tablero Kanban: seguimiento del flujo de trabajo.
- Product Backlog: organización y priorización de las tareas.
- Vista temporal: consulta de las fechas y de las iteraciones planificadas.
- Sprint actual, cuando se utiliza: seguimiento del trabajo seleccionado
  para la iteración activa.

Estas vistas no constituyen sistemas independientes, sino distintas
representaciones del mismo trabajo.

Los campos de fecha reflejan la planificación de las tareas. La información
sobre su ejecución real y las desviaciones se registra mediante comentarios,
documentos de seguimiento y evidencias.

### 6.4. Control de versiones y documentación

Los commits registran cambios reales en el código, los notebooks y la
documentación del repositorio.

Los mensajes de commit describen el trabajo realizado. No se crean cambios
artificiales únicamente para aumentar la actividad visible.

La planificación y el seguimiento se gestionan en GitHub. Google Colab se
utiliza para ejecutar notebooks y Google Drive para conservar datos o archivos
de trabajo que no deban publicarse.

## 7. Estimación y capacidad de trabajo

Las estimaciones se expresan en horas de trabajo.

La planificación utiliza como referencia una dedicación de cuatro horas
por jornada, de lunes a viernes. Esta disponibilidad es una previsión de
capacidad y puede revisarse según las obligaciones académicas y el progreso
real.

La duración de un Sprint se expresa en semanas de calendario, mientras que
la estimación de una tarea representa el esfuerzo previsto. Ambos conceptos
se mantienen separados.

El intervalo entre la fecha de inicio y la fecha objetivo no se interpreta
automáticamente como dedicación continua, ya que puede incluir esperas o
periodos sin trabajo efectivo.

Las actividades de desarrollo, documentación y revisión deben caber en la
capacidad disponible de cada Sprint.

## 8. Redacción transversal de la memoria

La memoria se redacta progresivamente durante los nueve Sprints.

Cada iteración incorpora actividades de documentación relacionadas con sus
resultados, decisiones y limitaciones. Estas actividades consumen parte de
la capacidad disponible y no constituyen un Sprint adicional superpuesto.

Las tareas de memoria se asignan al Sprint en el que se realizan y se
identifican mediante el tipo de trabajo «Documentación» y, cuando procede,
la etiqueta «memoria».

La redacción progresiva permite conservar el contexto de las decisiones y
evita concentrar toda la escritura al final del desarrollo.

La revisión global de la memoria, las correcciones finales y la entrega se
registran como tareas específicas con fechas propias.

## 9. Criterios de finalización

Una tarea se considera terminada cuando:

- Cumple sus criterios de aceptación.
- Su resultado se ha comprobado.
- Los archivos o entregables relevantes están disponibles.
- La documentación necesaria está actualizada.
- Se han registrado las evidencias correspondientes.
- La issue puede cerrarse y pasar al estado «Hecho».

Las tareas que modifican archivos se relacionan con commits descriptivos.

Las actividades de gestión que no generan cambios en archivos pueden
acreditarse mediante comentarios, decisiones, configuración del proyecto y
registros de revisión.

## 10. Gestión de impedimentos y desviaciones

Los impedimentos se registran en las issues y en el documento de seguimiento
del Sprint.

Cuando una tarea no puede continuar, se identifica la causa y se utiliza
el estado «Bloqueado». Se registra qué información o acción es necesaria
para poder retomarla.

Las desviaciones se revisan al comparar el objetivo del Sprint, el trabajo
seleccionado y los resultados obtenidos.

La replanificación se refleja en GitHub Projects y en los documentos de
seguimiento. Los cambios relevantes deben indicar su motivo y su efecto
sobre las tareas pendientes.

El trabajo realizado antes de la creación de esta planificación no se
presenta como si hubiera sido planificado originalmente con ella. Las fechas
históricas verificables se distinguen de las estimaciones futuras.

## 11. Revisión y retrospectiva

Al finalizar cada Sprint se revisan los resultados frente al objetivo y los
criterios de aceptación.

La revisión permite identificar el trabajo completado, las tareas pendientes
y las adaptaciones necesarias para continuar.

La retrospectiva se centra en el proceso de trabajo: qué ha funcionado,
qué dificultades han aparecido y qué acciones concretas pueden mejorar
la siguiente iteración.

Los acuerdos se registran en el documento del Sprint y, cuando requieren
trabajo adicional, se convierten en tareas del backlog.

Las reuniones y validaciones con el profesor se documentan cuando se
realizan, sin presentarlas anticipadamente como completadas.

## 12. Trazabilidad del proyecto

La trazabilidad se establece mediante la relación entre:

- Objetivos del TFG.
- Issues.
- Milestones.
- Sprints.
- Commits.
- Notebooks.
- Resultados.
- Documentación.

Esta relación permite consultar tanto el resultado final como el proceso
seguido para obtenerlo.

El historial del repositorio y los documentos de seguimiento sirven como
evidencias del desarrollo, de las decisiones adoptadas y de la evolución
de la planificación.
