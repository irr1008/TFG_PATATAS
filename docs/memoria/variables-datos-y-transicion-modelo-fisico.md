# Variables, datos y transición hacia un modelo físico

Sprint 3 · Periodo: 26/10/2026–08/11/2026.

## Objetivo inicial

Definir las variables, unidades y fuentes del balance hídrico, analizar el
motor de referencia y preparar datos complementarios para el proyecto.

## Trabajo realizado

Se analizó Agrobioma v14, se elaboró un glosario de variables y se documentaron
las discrepancias de fórmulas y criterios que necesitaban aclaración.

También se analizó el histórico de sondas, documentando su estructura,
frecuencia, cobertura, duplicados y lecturas sospechosas. Se compararon las
fuentes meteorológicas AEMET OpenData, NASA POWER y Open-Meteo, distinguiendo
las verificaciones realizadas de las comprobaciones pendientes.

Las solicitudes y comunicaciones con los tutores se registraron sin presentar
como recibidas las respuestas que no constaban.

## Reunión y cambio de enfoque

La reunión prevista para el 30/10 se celebró el 06/11/2026. Los tutores
recomendaron iniciar un modelo físico nuevo, independiente de Agrobioma v14,
reutilizando únicamente el trabajo pertinente.

Las preguntas anteriores no se respondieron punto por punto. El análisis
del motor se conserva como antecedente y no como especificación activa.

Tras la reunión se redactaron una especificación inicial del nuevo modelo
y un diseño del núcleo hidráulico con parámetros sintéticos y pruebas
deterministas y temporales. No se implementó el núcleo durante este sprint.

## Limitaciones detectadas

Las profundidades indicadas en las fichas difieren de la hipótesis uniforme
utilizada anteriormente. La correspondencia y el periodo de instalación de
las sondas requieren conciliación.

Los mensajes con recomendaciones de riego no demuestran su ejecución.
Los parámetros calculados por el sistema anterior no se consideran mediciones
independientes para validar el nuevo modelo.

El seguimiento de los datos y metadatos necesarios para la evaluación real
continúa en #16.

## Trabajo no realizado

No se preparó la meteorología diaria de #11 ni se completó la extracción
Sentinel-2 de #12. Ambas tareas permanecen en el backlog.

La revisión bibliográfica original de #14 se cerró como no planificada.
El respaldo de las leyes del nuevo núcleo se aborda en #17.

## Cierre y continuidad

El sprint se cierra anticipadamente el 08/11/2026, en lugar del 13/11 previsto.
La capacidad restante deja de estar comprometida con esta iteración porque
su alcance ha cambiado; no se presenta como un ahorro de horas medido.

El objetivo original se alcanza parcialmente. Se conserva el trabajo útil
y se planifica por separado el desarrollo del núcleo mediante #17 a #22.

Las estimaciones de esas tareas son 4, 8, 16, 12, 8 y 4 horas, respectivamente:
52 horas previstas, sin equivalencia automática con dedicación real.

## Evidencias

- `docs/sprint-03.md`.
- `docs/analisis-motor-referencia.md`.
- `docs/variables-balance-hidrico.md`.
- `docs/analisis-historico-sondas.md`.
- `docs/fuentes-meteorologicas.md`.
- `docs/solicitud-datos-tutores.md`.
- `docs/registro-reunion-06-11-2026.md`.
- `docs/especificación-modelo-físico.md`.
- `docs/diseño-nucleo-hidraulico.md`.
- `notebooks/04_analisis_historico_sondas.ipynb`.
