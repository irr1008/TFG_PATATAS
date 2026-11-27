# Núcleo hidráulico verificable

Sprint 4 · Periodo: 09/11/2026 – 27/11/2026.

## Objetivo inicial

Implementar un núcleo hidráulico por capas, independiente de Agrobioma v14,
y verificar su conservación de masa y su comportamiento temporal con datos
sintéticos. El sprint parte del cambio de enfoque acordado en la reunión del
06/11/2026 y del diseño v0.2 del núcleo.

## Trabajo realizado

El sprint se organizó en seis tareas con dependencias explícitas
(#17 -> #18 -> #19 -> #20 -> #21 -> #22).

**Justificación (#17).** Se documentaron las hipótesis, las unidades y las
leyes del núcleo, distinguiendo los principios de conservación, los cierres
simplificados y las elecciones del experimento. Se derivó el drenaje por
relajación del exceso sobre la capacidad de campo,
`D = max(0, S − S_FC) · [1 − exp(−Δt/τ)]`. Las fuentes (FAO-56 y el ejemplo
modular de DSSAT) se citan como antecedentes metodológicos, no como
validación del núcleo.

**Configuración y estados (#18).** Se implementaron los perfiles de una o más
capas, los estados de almacenamiento, las entradas por intervalo y las
conversiones entre humedad y almacenamiento (`S = 1000 · L · θ`). Los valores
inválidos se rechazan sin corrección silenciosa.

**Paso hidráulico (#19).** Se implementó el paso completo, con este orden:
drenaje inferior, transferencias internas de abajo arriba, infiltración con
salida superficial y extracción. Las transferencias son conservativas y están
limitadas por la capacidad de la capa receptora. La infiltración efectiva es
el mínimo entre el aporte, la capacidad máxima `f_max·Δt` y el espacio
disponible. La extracción no baja del límite `θ_min`. El balance de cada paso
se calcula de forma independiente.

**Ejecutor temporal (#20).** Se implementaron la malla temporal con cambios no
alineados, los eventos de tasa constante y su conversión a acumulados por
solape, y el balance global independiente de la suma de residuales por paso.
Se verificaron dos escenarios sintéticos con pasos de 300, 150, 75 y 37,5 s.

**Demostración (#21).** Se publicó un notebook que importa el paquete, ejecuta
ambos escenarios, representa entradas, humedad por capa, salidas, balances y
errores, y se publica sin salidas.

## Resultados

| Hito | Pruebas superadas | Commit |
|---|---:|---|
| Primer bloque de la #18 | 43 | c541560 |
| Cierre de la #18 | 186 | d24be2f |
| Primer bloque de la #19 | 243 | 721ab41 |
| Infiltración de la #19 | 287 | e18b418 |
| Cierre de la #19 | 329 | 203ee29 |
| Malla y eventos de la #20 | 393 | 1bbe162 |
| Cierre de la #20 | 443 | 581c8bf |
| Revisión de la #22 | 443 | c65337a |

Los ocho balances globales cumplen su tolerancia, con residuales inferiores a
3,1e-12 mm. En el escenario 11.1, la diferencia máxima de humedad entre 75 y
37,5 s es de 8e-6 m³/m³, frente a un umbral de 1e-4 m³/m³. En el escenario
11.2, comparado con la solución analítica del sistema continuo, el error
máximo de humedad de la capa inferior pasa de 1,05e-4 m³/m³ con 300 s a
1,30e-5 m³/m³ con 37,5 s. Cada reducción del paso a la mitad divide el error
aproximadamente por dos, lo que es compatible con primer orden en ese
escenario sin demostrarlo en general.

El cierre de masa no se considera suficiente para aceptar un paso temporal: se
exige también el refinamiento y la comparación analítica. El paso de 300 s se
mantiene como resolución nominal de trabajo, siempre acompañado de sus errores
medidos.

## Limitaciones detectadas

La verificación es numérica y sintética. No constituye calibración ni
validación con parcelas.

El núcleo es un modelo de depósitos por capas, no una solución de la ecuación
de Richards. Solo admite flujo descendente, infiltración máxima constante,
sin depósito superficial, con extracciones prescritas y sin demanda
atmosférica calculada. Tampoco incluye temperatura ni radiación. La salida
inferior no está limitada, por lo que no existe una capa final que actúe como
depósito.

Los dos escenarios temporales no cubren todas las configuraciones. El paquete
declara compatibilidad con Python 3.11 o posterior, pero las pruebas se
ejecutaron solo con Python 3.13.18.

## Trabajo no realizado

No se calibraron parámetros ni se comparó el modelo con observaciones. La
auditoría de datos reales sigue en #16, y la meteorología de #11 y la
ampliación Sentinel-2 de #12 permanecen en el backlog.

## Dificultades y decisiones

El trabajo se interrumpió por motivos de salud durante la semana del 16 al
22/11/2026 y se reanudó el 23/11. La reunión de seguimiento prevista para el
13/11 se celebró el 27/11.

En ese momento se acordó cerrar el sprint con el núcleo actual (v0.1) sin
ampliar su alcance, y planificar un sprint 5 de mejora: aumentar el número de
capas, añadir una capa final que actúe como depósito e incorporar temperatura
y radiación. Estas mejoras se registran como propuestas, no como trabajo
comprometido, hasta que se planifique ese sprint.

La documentación (informe de verificación, guía de uso y plan de trabajo) se
actualizó durante la revisión final para eliminar descripciones obsoletas.

## Cierre y continuidad

El sprint se cierra el 27/11/2026, en la fecha objetivo original. Las
estimaciones previstas (52 horas para las seis tareas) han sido completadas
como se indica en las issues.

## Evidencias

- `docs/sprint-04.md`.
- `docs/justificacion-nucleo-hidraulico.md`.
- `docs/diseño-nucleo-hidraulico.md`.
- `docs/uso-nucleo-hidraulico.md`.
- `docs/verificacion-nucleo-hidraulico.md`.
- `docs/registro-reunion-27-11-2026.md`.
- `src/modelo_fisico/` y `tests/`.
- `notebooks/05_demostracion_nucleo_hidraulico.ipynb`.
